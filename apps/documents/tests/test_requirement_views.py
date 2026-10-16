"""
The register, the piece page, filing, reviewing — and who may do each of them.

Permission tests here are the object-level ones the rebase directive §61 asks for: person A never
reaches person B's piece, a revoked mandate grants nothing, a discovered identifier does not bypass
anything, and the person never reviews their own evidence.
"""

from __future__ import annotations

import datetime as dt
import uuid

import pytest

from audit.models import AuditEvent
from cases.models import ResponsibleActor
from core import clock
from documents import services
from documents.models import DocumentRequirement, RequirementState, VersionDecision
from documents.tests.conftest import upload_file

pytestmark = [pytest.mark.django_db, pytest.mark.security]

MINIMAL_PDF = (
    b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
    b"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
    b"3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 200 200]>>endobj\n"
    b"trailer<</Root 1 0 R>>\n%%EOF\n"
)

REGISTER = "/documents/"


def pdf(name="piece.pdf"):
    return upload_file(name, MINIMAL_PDF, "application/pdf")


def detail(requirement):
    return f"/documents/requirements/{requirement.pk}/"


def file_url(requirement):
    return f"/documents/requirements/{requirement.pk}/file/"


def review_url(requirement):
    return f"/documents/requirements/{requirement.pk}/review/"


# ---------------------------------------------------------------------------------------------
# The register
# ---------------------------------------------------------------------------------------------
def test_anonymous_is_sent_to_the_login_page(client):
    r = client.get(REGISTER)
    assert r.status_code == 302 and "/compte/login/" in r["Location"]


def test_the_register_shows_the_piece_its_state_and_who_is_answerable(client, owner, requirement):
    client.force_login(owner)
    r = client.get(REGISTER)
    body = r.content.decode()
    assert r.status_code == 200
    assert requirement.title in body
    assert "Manquant" in body, "the word, not a colour"
    assert str(ResponsibleActor.PERSON.label) in body
    # design V5 (W3-C): the register is a collection of rows in three groups, not a table — the row is the link
    assert 'class="doc-collection"' in body and 'class="doc-row"' in body and 'class="doc-row__link"' in body


def test_the_register_is_not_a_file_browser(client, owner, requirement):
    """The row is the REQUIREMENT. A stored filename is not what a person came to read."""
    services.file_version(requirement, owner, pdf("mon-passeport-prive.pdf"))
    client.force_login(owner)
    body = client.get(REGISTER).content.decode()
    assert requirement.title in body
    assert "mon-passeport-prive.pdf" not in body


def test_the_register_of_one_person_never_shows_another_persons_piece(client, intruder, requirement):
    client.force_login(intruder)
    body = client.get(REGISTER).content.decode()
    assert requirement.title not in body
    assert "Aucune pièce ne vous est demandée" in body


def test_a_discovered_identifier_does_not_bypass_anything(client, intruder, requirement):
    client.force_login(intruder)
    assert client.get(detail(requirement)).status_code == 404, "indistinguishable from 'does not exist'"
    assert client.post(file_url(requirement)).status_code == 404
    assert client.post(review_url(requirement)).status_code == 404


def test_an_unknown_identifier_answers_exactly_the_same(client, owner):
    client.force_login(owner)
    assert client.get(f"/documents/requirements/{uuid.uuid4()}/").status_code == 404


def test_a_revoked_mandate_grants_nothing(client, revoked_professional, requirement):
    client.force_login(revoked_professional)
    assert client.get(detail(requirement)).status_code == 404
    assert requirement.title not in client.get(REGISTER).content.decode()


def test_a_live_mandate_reads_the_case_pieces(client, professional, requirement):
    client.force_login(professional)
    assert client.get(detail(requirement)).status_code == 200
    assert requirement.title in client.get(REGISTER).content.decode()


def test_a_restricted_piece_is_invisible_to_an_assignee(client, case, professional):
    from documents.models import AccessClass

    restricted = services.declare_requirement(
        case,
        code="civil_record",
        title="Acte d’état civil",
        responsible_actor=ResponsibleActor.PERSON,
        access_class=AccessClass.RESTRICTED,
    )
    client.force_login(professional)
    assert client.get(detail(restricted)).status_code == 404
    assert restricted.title not in client.get(REGISTER).content.decode()


def test_project_staff_do_not_get_a_standing_list_of_case_pieces(client, staff_role_user, requirement):
    """Mirrors cases.CaseFileQuerySet.readable_by: supervision happens in the back-office."""
    client.force_login(staff_role_user)
    assert client.get(detail(requirement)).status_code == 404
    assert requirement.title not in client.get(REGISTER).content.decode()


# ---------------------------------------------------------------------------------------------
# The piece page
# ---------------------------------------------------------------------------------------------
def test_the_piece_page_shows_the_state_its_rule_and_its_source(client, owner, requirement):
    client.force_login(owner)
    body = client.get(detail(requirement)).content.decode()
    assert "Rien n’a encore été déposé" in body, "the word carries a rule"
    assert "D.lgs. 286/1998" in body and "art. 4, comma 1" in body
    assert 'class="sources"' in body


def test_the_deposit_form_is_offered_only_for_a_piece_that_is_the_persons_to_provide(
    client, owner, requirement, authority_requirement
):
    client.force_login(owner)
    assert 'type="file"' in client.get(detail(requirement)).content.decode()
    other = client.get(detail(authority_requirement)).content.decode()
    assert 'type="file"' not in other
    assert "Cette pièce ne dépend pas de vous." in other


def test_the_person_is_never_offered_the_review_form(client, owner, requirement):
    services.file_version(requirement, owner, pdf())
    client.force_login(owner)
    body = client.get(detail(requirement)).content.decode()
    assert "Examen de la version en vigueur" not in body


def test_the_antivirus_line_never_claims_a_scan_that_did_not_happen(client, owner, requirement):
    services.file_version(requirement, owner, pdf())
    client.force_login(owner)
    body = client.get(detail(requirement)).content.decode()
    assert "Aucun antivirus n’est déployé sur cette installation" in body
    assert "Analysé — sain" not in body


# ---------------------------------------------------------------------------------------------
# Filing through the view
# ---------------------------------------------------------------------------------------------
def test_filing_against_a_named_requirement_end_to_end(client, owner, requirement):
    client.force_login(owner)
    expiry = clock.today() + dt.timedelta(days=400)
    r = client.post(file_url(requirement), {"file": pdf(), "expires_on": expiry.isoformat()})
    assert r.status_code == 302 and r["Location"] == detail(requirement)
    requirement.refresh_from_db()
    version = requirement.current_version
    assert version is not None and version.number == 1
    assert version.expires_on == expiry
    assert requirement.display_state == RequirementState.FILED
    assert AuditEvent.objects.filter(action="documents.requirement.filed").exists()


def test_filing_again_supersedes_and_keeps_the_history(client, owner, requirement):
    client.force_login(owner)
    client.post(file_url(requirement), {"file": pdf("v1.pdf")})
    client.post(file_url(requirement), {"file": pdf("v2.pdf")})
    versions = list(requirement.versions.order_by("number"))
    assert len(versions) == 2
    assert versions[0].superseded_at is not None and not versions[0].is_current
    assert versions[1].is_current


def test_the_view_refuses_an_expiry_already_past(client, owner, requirement):
    client.force_login(owner)
    past = (clock.today() - dt.timedelta(days=1)).isoformat()
    client.post(file_url(requirement), {"file": pdf(), "expires_on": past})
    assert requirement.versions.count() == 0


def test_the_view_refuses_a_disguised_file(client, owner, requirement):
    client.force_login(owner)
    client.post(file_url(requirement), {"file": upload_file("faux.pdf", b"<html>nope</html>", "application/pdf")})
    assert requirement.versions.count() == 0


def test_the_person_cannot_file_a_piece_the_authority_must_issue(client, owner, authority_requirement):
    client.force_login(owner)
    r = client.post(file_url(authority_requirement), {"file": pdf()})
    assert r.status_code == 403
    assert authority_requirement.versions.count() == 0


def test_filing_requires_the_conditions_to_have_been_accepted(client, user_factory, case):
    """Consent is a ROW-level blocker with the link that resolves it, never a silent 500."""
    from accounts import roles as role_names

    person = case.person
    person.terms_accepted_at = None
    person.save(update_fields=["terms_accepted_at"])
    requirement = services.declare_requirement(case, code="x", title="Pièce", responsible_actor=ResponsibleActor.PERSON)
    assert role_names.has_role(person, role_names.PERSON)
    client.force_login(person)
    body = client.get(REGISTER).content.decode()
    # design V5 (W3-C): the row says it is blocked and the register's strip says why, in the row's own words — no
    # button promises an acceptance its target cannot do (the acceptance flow waits on the legal texts, G1)
    assert "Bloqué" in body and "Acceptation des Conditions d’utilisation requise." in body
    assert client.post(file_url(requirement), {"file": pdf()}).status_code == 403


def test_a_get_on_the_filing_endpoint_is_refused(client, owner, requirement):
    client.force_login(owner)
    assert client.get(file_url(requirement)).status_code == 405


# ---------------------------------------------------------------------------------------------
# Review through the view
# ---------------------------------------------------------------------------------------------
def test_an_assignee_reviews_and_the_state_follows(client, owner, requirement, professional):
    services.file_version(requirement, owner, pdf())
    client.force_login(professional)
    r = client.post(review_url(requirement), {"decision": "accept", "note": ""})
    assert r.status_code == 302
    requirement.refresh_from_db()
    assert requirement.display_state == RequirementState.VALID
    assert requirement.current_version.decision == VersionDecision.ACCEPTED
    assert AuditEvent.objects.filter(action="documents.requirement.reviewed").exists()


def test_the_person_may_never_review_their_own_evidence(client, owner, requirement):
    services.file_version(requirement, owner, pdf())
    client.force_login(owner)
    assert client.post(review_url(requirement), {"decision": "accept"}).status_code == 403
    requirement.refresh_from_db()
    assert requirement.display_state == RequirementState.FILED


def test_a_refusal_without_a_motive_is_rejected_by_the_form(client, owner, requirement, professional):
    services.file_version(requirement, owner, pdf())
    client.force_login(professional)
    client.post(review_url(requirement), {"decision": "refuse", "note": ""})
    requirement.refresh_from_db()
    assert requirement.display_state == RequirementState.FILED


def test_requesting_a_replacement_through_the_view(client, owner, requirement, professional):
    services.file_version(requirement, owner, pdf())
    client.force_login(professional)
    client.post(review_url(requirement), {"decision": "replace", "note": "Scan illisible."})
    requirement.refresh_from_db()
    assert requirement.display_state == RequirementState.TO_REPLACE
    assert requirement.state_note == "Scan illisible."


def test_reviewing_a_requirement_with_nothing_filed_is_a_404(client, requirement, professional):
    client.force_login(professional)
    assert client.post(review_url(requirement), {"decision": "accept"}).status_code == 404


# ---------------------------------------------------------------------------------------------
# The file behind the piece
# ---------------------------------------------------------------------------------------------
def test_a_filed_piece_cannot_be_quietly_deleted_by_its_uploader(client, owner, requirement):
    version = services.file_version(requirement, owner, pdf())
    client.force_login(owner)
    r = client.post(f"/documents/{version.document.pk}/delete/")
    assert r.status_code == 403, "evidence is superseded or purged by retention, never quietly removed"
    version.document.refresh_from_db()
    assert version.document.deleted_at is None


def test_a_loose_file_is_still_the_accounts_to_delete(client, owner):
    doc = services.store_upload(owner, pdf("perso.pdf"), "other")
    client.force_login(owner)
    assert client.post(f"/documents/{doc.pk}/delete/").status_code == 302
    doc.refresh_from_db()
    assert doc.deleted_at is not None


def test_an_assignee_may_download_the_file_of_a_piece_they_may_read(client, owner, requirement, professional):
    version = services.file_version(requirement, owner, pdf())
    services.apply_scan_result(version.document, "clean", note="test")
    client.force_login(professional)
    assert client.get(f"/documents/{version.document.pk}/").status_code == 200


def test_an_intruder_never_reaches_the_file(client, intruder, owner, requirement):
    version = services.file_version(requirement, owner, pdf())
    services.apply_scan_result(version.document, "clean", note="test")
    client.force_login(intruder)
    assert client.get(f"/documents/{version.document.pk}/").status_code == 403
    assert not AuditEvent.objects.filter(action="documents.downloaded").exists()


def test_project_staff_do_not_reach_a_case_file_through_the_documents_app(client, staff_role_user, owner, requirement):
    version = services.file_version(requirement, owner, pdf())
    services.apply_scan_result(version.document, "clean", note="test")
    client.force_login(staff_role_user)
    assert client.get(f"/documents/{version.document.pk}/").status_code == 403


def test_an_unscanned_file_is_never_handed_to_a_third_party(client, owner, requirement, professional):
    version = services.file_version(requirement, owner, pdf())
    assert version.document.scan_status == "not_configured"
    client.force_login(professional)
    assert client.get(f"/documents/{version.document.pk}/").status_code == 403
    client.force_login(owner)
    assert client.get(f"/documents/{version.document.pk}/").status_code == 200


def test_the_register_renders_on_the_platform_shell_not_the_public_one(client, owner, requirement):
    client.force_login(owner)
    body = client.get(REGISTER).content.decode()
    assert "portal-bar" in body, "the platform chrome"
    assert "portal/portal.css" in body
    assert 'class="site-header"' not in body


def test_the_reserved_area_entry_renders_the_same_register(client, owner, requirement, legal_published):
    client.force_login(owner)
    r = client.get("/fr/espace-reserve/mes-documents/")
    assert r.status_code == 200
    body = r.content.decode()
    assert requirement.title in body
    assert "doc-collection" in body and "doc-row" in body


def test_no_forbidden_promise_anywhere_on_the_register(client, owner, requirement):
    from cms.forbidden import scan

    client.force_login(owner)
    for url in (REGISTER, detail(requirement)):
        assert not scan(client.get(url).content.decode()), url


def test_no_state_ever_says_approved(client, owner, requirement, professional):
    version = services.file_version(requirement, owner, pdf())
    services.set_decision(version, VersionDecision.ACCEPTED, actor=professional)
    client.force_login(owner)
    body = client.get(detail(requirement)).content.decode().lower()
    for forbidden in ("approuvé", "approuvée", "éligible", "autorisé à entrer"):
        assert forbidden not in body, forbidden
    assert "ceci n’est pas une décision" in body


def test_the_requirement_can_be_attached_to_a_checklist_item(case, owner):
    from cases.services import add_checklist_item

    item = add_checklist_item(
        case, requirement="Réunir les pièces d’identité", responsible_actor=ResponsibleActor.PERSON
    )
    piece = services.declare_requirement(
        case,
        code="id",
        title="Passeport",
        responsible_actor=ResponsibleActor.PERSON,
        checklist_item=item,
    )
    assert piece.checklist_item_id == item.pk
    assert list(item.document_requirements.all()) == [piece]
    assert DocumentRequirement.objects.get(pk=piece.pk).checklist_item.case_id == case.pk


# ---------------------------------------------------------------------------------------------
# The consent gate says BLOQUÉ where something is blocked, and nowhere else
# ---------------------------------------------------------------------------------------------
def test_the_consent_blocker_is_not_shown_beside_a_piece_that_needs_nothing(client, owner, case, professional):
    """A "Bloqué" chip beside "Valide" is the state confusion this register exists to remove."""
    settled = services.declare_requirement(
        case, code="passport", title="Passeport", responsible_actor=ResponsibleActor.PERSON
    )
    services.set_decision(services.file_version(settled, owner, pdf()), VersionDecision.ACCEPTED, actor=professional)
    services.declare_requirement(case, code="diploma", title="Diplôme", responsible_actor=ResponsibleActor.PERSON)
    owner.terms_accepted_at = None
    owner.save(update_fields=["terms_accepted_at"])

    from documents.presenters import register_rows

    rows = {row["code"]: row for row in register_rows(owner)}
    assert rows["passport"]["state"] == RequirementState.VALID
    assert rows["passport"]["action_blocked"] is False
    assert rows["diploma"]["state"] == RequirementState.MISSING
    assert rows["diploma"]["action_blocked"] is True

    client.force_login(owner)
    body = client.get(REGISTER).content.decode()
    # Exactly one blocked row: the one that still needs a deposit (design V5: counted on the rows — the register's
    # strip names that same piece and says why).
    rows = [part.split("</li>")[0] for part in body.split('<li class="doc-row"')[1:]]
    assert sum("Bloqué" in row for row in rows) == 1
    # And the gate is still stated once for the page, so nothing about it is hidden.
    assert "Le dépôt de fichiers nécessite l’acceptation des Conditions" in body


def test_the_piece_page_still_explains_the_consent_gate_on_every_row_it_governs(client, owner, case, professional):
    settled = services.declare_requirement(
        case, code="passport", title="Passeport", responsible_actor=ResponsibleActor.PERSON
    )
    services.set_decision(services.file_version(settled, owner, pdf()), VersionDecision.ACCEPTED, actor=professional)
    owner.terms_accepted_at = None
    owner.save(update_fields=["terms_accepted_at"])
    client.force_login(owner)
    body = client.get(detail(settled)).content.decode()
    assert "nécessite l’acceptation des Conditions d’utilisation" in body
    assert 'type="file"' not in body
