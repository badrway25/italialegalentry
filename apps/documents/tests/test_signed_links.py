"""
Signed temporary download links (REQ-DOC-02).

A signed link ADDS three constraints and removes none. Every test here exists to keep it that way:
it expires, it cannot be forged, it is inert in anybody else's browser — and the object-level check
still runs on the way out, so a link that leaks grants nothing.
"""

from __future__ import annotations

import time

import pytest
from django.core import signing

from audit.models import AuditEvent
from documents import services
from documents.tests.conftest import MINIMAL_PDF, upload_file

pytestmark = [pytest.mark.django_db, pytest.mark.security]


def pdf(name="piece.pdf"):
    return upload_file(name, MINIMAL_PDF, "application/pdf")


def link(token: str) -> str:
    return f"/documents/link/{token}/"


@pytest.fixture
def filed(requirement, owner):
    return services.file_version(requirement, owner, pdf())


def test_a_signed_link_delivers_the_file_and_is_audited_as_such(client, owner, filed):
    token = services.signed_download_token(filed.document, owner)
    client.force_login(owner)
    r = client.get(link(token))
    assert r.status_code == 200
    assert b"".join(r.streaming_content) == MINIMAL_PDF
    assert r["Content-Disposition"].startswith("attachment;")
    assert r["X-Content-Type-Options"] == "nosniff"
    assert "no-store" in r["Cache-Control"]
    event = AuditEvent.objects.get(action="documents.downloaded")
    assert event.metadata["via"] == "signed_link"


def test_a_link_issued_for_one_account_is_inert_in_another(client, owner, intruder, filed):
    token = services.signed_download_token(filed.document, owner)
    client.force_login(intruder)
    assert client.get(link(token)).status_code == 404
    assert not AuditEvent.objects.filter(action="documents.downloaded").exists()


def test_a_forged_or_tampered_token_is_refused(client, owner, filed):
    token = services.signed_download_token(filed.document, owner)
    client.force_login(owner)
    assert client.get(link(token[:-3] + "aaa")).status_code == 404
    assert client.get(link("not-a-token")).status_code == 404
    # A payload signed with another salt is not this application's token.
    other = signing.dumps({"d": str(filed.document.pk), "u": owner.pk}, salt="documents.other")
    assert client.get(link(other)).status_code == 404


def test_an_expired_link_says_so_and_offers_a_fresh_one(client, owner, filed, monkeypatch):
    token = services.signed_download_token(filed.document, owner)
    monkeypatch.setattr(services, "DOWNLOAD_LINK_TTL", 0)
    time.sleep(1.1)
    client.force_login(owner)
    r = client.get(link(token), follow=True)
    # Never "not found" for a document that is there: the reader is told the link expired and
    # lands on the page where a new one has just been minted.
    assert r.redirect_chain and r.redirect_chain[-1][0] == f"/documents/requirements/{filed.requirement_id}/"
    body = r.content.decode()
    assert "Ce lien temporaire a expiré" in body
    assert "/documents/link/" in body, "a fresh link is on the page"


def test_the_policy_still_runs_on_a_valid_link(client, owner, intruder, filed):
    """Authorisation is recomputed on EVERY delivery; the signature is not a substitute for it."""
    token = services.signed_download_token(filed.document, intruder)
    client.force_login(intruder)
    # The token is genuinely signed and genuinely belongs to this account, yet the account has no
    # business with this file: the object-level check refuses it.
    assert client.get(link(token)).status_code == 403


def test_the_link_validity_is_stated_beside_the_link(client, owner, filed):
    client.force_login(owner)
    body = client.get(f"/documents/requirements/{filed.requirement_id}/").content.decode()
    assert f"Lien valable {services.DOWNLOAD_LINK_MINUTES} minutes" in body
    assert services.DOWNLOAD_LINK_TTL == 600


def test_no_link_is_minted_for_a_file_the_account_may_not_read(client, professional, owner, requirement):
    from documents.models import AccessClass
    from documents.presenters import present_requirement

    services.file_version(requirement, owner, pdf())
    requirement.access_class = AccessClass.RESTRICTED
    requirement.save(update_fields=["access_class"])
    row = present_requirement(requirement, user=professional, with_versions=True)
    assert row["versions"][0]["download_url"] == "", "a template cannot conjure a link the policy refuses"


def test_an_infected_file_is_never_delivered_even_with_a_valid_token(client, owner, filed):
    token = services.signed_download_token(filed.document, owner)
    services.apply_scan_result(filed.document, "infected", note="test")
    client.force_login(owner)
    assert client.get(link(token)).status_code == 403


def test_an_anonymous_visitor_with_a_valid_token_gets_the_login_page(client, owner, filed):
    token = services.signed_download_token(filed.document, owner)
    r = client.get(link(token))
    assert r.status_code == 302 and "/compte/login/" in r["Location"]


def test_the_token_carries_no_readable_personal_data(owner, filed):
    token = services.signed_download_token(filed.document, owner)
    assert owner.email not in token
    assert filed.document.original_name not in token
    payload = signing.loads(token, salt=services.DOWNLOAD_SALT)
    assert set(payload) == {"d", "u"}, "the token names an object and an account, nothing else"


# ---------------------------------------------------------------------------------------------
# The page must never offer a delivery the view will refuse
#
# Regression: ``present_version`` minted a signed link whenever the object-level policy allowed a
# READ, while ``_serve`` additionally refused any file no scanner had cleared to anybody but its
# depositor. On this deployment no scanner is configured, so every reviewer of every case was shown
# a "Télécharger" link that answered 403 — a dead link reads as the reader's mistake, not a rule.
# ---------------------------------------------------------------------------------------------
def test_a_reviewer_is_not_offered_a_link_for_an_unscanned_file(client, professional, owner, requirement, filed):
    from documents.presenters import present_requirement

    row = present_requirement(requirement, user=professional, with_versions=True)
    version = row["versions"][0]
    assert filed.document.scan_status == "not_configured"
    assert version["download_url"] == "", "the view would refuse this delivery"
    assert version["delivery_block"] == "unscanned"
    assert "Aucun antivirus n’est déployé" in str(version["delivery_rule"])


def test_the_reviewer_page_states_the_reason_instead_of_a_dead_link(client, professional, owner, requirement, filed):
    client.force_login(professional)
    body = client.get(f"/documents/requirements/{requirement.pk}/").content.decode()
    assert "/documents/link/" not in body
    assert "Aucun antivirus n’est déployé sur cette installation : le fichier n’est remis" in body


def test_once_a_file_is_cleared_the_reviewer_gets_a_working_link(client, professional, owner, requirement, filed):
    """The rule is a gate, not a wall: a documented manual review opens it."""
    services.apply_scan_result(filed.document, "clean", note="manual review (test)")
    filed.document.refresh_from_db()
    client.force_login(professional)
    body = client.get(f"/documents/requirements/{requirement.pk}/").content.decode()
    assert "/documents/link/" in body
    token = services.signed_download_token(filed.document, professional)
    assert client.get(link(token)).status_code == 200


def test_the_depositor_is_still_offered_their_own_unscanned_file(client, owner, requirement, filed):
    from documents.presenters import present_requirement

    row = present_requirement(requirement, user=owner, with_versions=True)
    assert row["versions"][0]["download_url"] != ""
    assert row["versions"][0]["delivery_block"] == ""


def test_every_link_the_register_mints_is_one_the_view_honours(client, owner, professional, case):
    """
    The invariant, stated once: for every version of every row either the page shows no link, or
    following it delivers the file. No state of the system may produce a link that answers 403.
    """
    from cases.models import ResponsibleActor
    from documents.presenters import register_rows

    for code, clean in (("a", True), ("b", False)):
        requirement = services.declare_requirement(
            case, code=code, title=code.upper(), responsible_actor=ResponsibleActor.PERSON
        )
        version = services.file_version(requirement, owner, pdf(f"{code}.pdf"))
        if clean:
            services.apply_scan_result(version.document, "clean", note="test")

    for reader in (owner, professional):
        client.force_login(reader)
        for row in register_rows(reader):
            current = row["current"]
            if current and current["download_url"]:
                assert client.get(current["download_url"]).status_code == 200, (row["code"], reader.email)


def test_the_admin_never_prints_a_link_it_cannot_honour(owner, requirement, filed):
    from documents.admin import PrivateDocumentAdmin
    from documents.models import PrivateDocument

    rendered = str(PrivateDocumentAdmin(PrivateDocument, None).download_link(filed.document))
    assert "<a href" not in rendered
    assert "antivirus" in rendered.lower()

    services.apply_scan_result(filed.document, "clean", note="test")
    filed.document.refresh_from_db()
    rendered = str(PrivateDocumentAdmin(PrivateDocument, None).download_link(filed.document))
    assert "<a href" in rendered
