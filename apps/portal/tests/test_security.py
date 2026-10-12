"""
Security regression tests of the reserved area (marker ``security``).

* anonymous → login page for EVERY portal route (whatever the HTTP method);
* IDOR: account B never opens account A's request / document / message, even with the right id;
* tenant isolation: a company account sees only its own organisation's data;
* mark-as-read only ever touches the caller's own message;
* a rendered page never contains another account's personal data;
* back-office: a bare ``is_staff`` flag opens nothing; the staff role never reaches admin-only pages.
"""

from __future__ import annotations

import uuid

import pytest
from django.urls import get_resolver, reverse

from accounts import roles
from portal.models import Message
from portal.tests.conftest import DASHBOARD, DEADLINES, DOCUMENTS, LOGIN, MESSAGES, PATHWAYS, REQUESTS

pytestmark = [pytest.mark.django_db, pytest.mark.security]

SITUATION = "/fr/espace-reserve/ma-situation/"
LIST_PAGES = [DASHBOARD, SITUATION, REQUESTS, PATHWAYS, DOCUMENTS, DEADLINES, MESSAGES]


def _portal_route_names() -> set[str]:
    names = set()
    for pattern in get_resolver("portal.urls").url_patterns:
        names.add(pattern.name)
    return names


def _sample_paths() -> dict[str, str]:
    some_uuid = uuid.uuid4()
    return {
        "dashboard": DASHBOARD,
        "situation": SITUATION,
        "requests": REQUESTS,
        "request_detail": f"{REQUESTS}contact/1/",
        "pathways": PATHWAYS,
        "documents": DOCUMENTS,
        "deadlines": DEADLINES,
        "messages": MESSAGES,
        "message_detail": f"{MESSAGES}{some_uuid}/",
        "message_read": f"{MESSAGES}{some_uuid}/lu/",
    }


# ---- anonymous ------------------------------------------------------------------------------
def test_every_portal_route_is_covered_by_the_anonymous_test():
    assert _portal_route_names() == set(_sample_paths()), "new portal route: add it to _sample_paths()"


@pytest.mark.parametrize("name, path", sorted(_sample_paths().items()))
@pytest.mark.parametrize("method", ["get", "post"])
def test_anonymous_is_redirected_to_login_for_every_route(client, seeded, name, path, method):
    response = getattr(client, method)(path)
    assert response.status_code == 302, (name, method, response.status_code)
    assert response["Location"].startswith(LOGIN), (name, response["Location"])
    assert f"next={path}" in response["Location"].replace("%2F", "/")


def test_anonymous_mark_as_read_changes_nothing(client, seeded, alice, make_message):
    message = make_message(alice)
    client.post(f"{MESSAGES}{message.pk}/lu/")
    message.refresh_from_db()
    assert message.is_read is False


def test_inactive_account_cannot_use_the_portal(client, seeded, alice):
    client.force_login(alice)
    alice.is_active = False
    alice.save(update_fields=["is_active"])
    assert client.get(DASHBOARD).status_code == 302


# ---- IDOR -----------------------------------------------------------------------------------
def test_user_b_cannot_open_user_a_request_even_with_the_right_id(
    client, seeded, alice, bob, make_company_request, make_contact_request, make_proposal
):
    rows = {
        "besoins-entreprise": make_company_request(alice, company_name="SECRET-ALPHA-COMPANY"),
        "contact": make_contact_request(alice, subject="SECRET-ALPHA-CONTACT"),
        "collaboration": make_proposal(alice, organisation_name="SECRET-ALPHA-ORG"),
    }
    client.force_login(bob)
    for kind, obj in rows.items():
        response = client.get(f"{REQUESTS}{kind}/{obj.pk}/")
        # 404, not 403: a 403 would confirm that the row exists and belongs to somebody else, which
        # is itself a disclosure. The answer must be the one a non-existent row gets.
        assert response.status_code == 404, kind
        assert "SECRET-ALPHA" not in response.content.decode()
        invented = client.get(f"{REQUESTS}{kind}/99999999/")
        assert invented.status_code == response.status_code, kind
    client.force_login(alice)
    for kind, obj in rows.items():
        assert client.get(f"{REQUESTS}{kind}/{obj.pk}/").status_code == 200, kind


def test_backoffice_roles_do_not_read_foreign_requests_through_the_portal(
    client, seeded, alice, staff_user, superuser, make_contact_request
):
    """Staff use the audited back-office; the portal is a strictly personal space."""
    obj = make_contact_request(alice, subject="SECRET-ALPHA-CONTACT")
    for user in (staff_user, superuser):
        client.force_login(user)
        response = client.get(f"{REQUESTS}contact/{obj.pk}/")
        assert response.status_code == 404
        assert "SECRET-ALPHA-CONTACT" not in response.content.decode()


def test_user_b_cannot_open_user_a_message(client, seeded, alice, bob, make_message):
    message = make_message(alice, subject="SECRET-ALPHA-SUBJECT", body="SECRET-ALPHA-BODY")
    client.force_login(bob)
    response = client.get(f"{MESSAGES}{message.pk}/")
    assert "SECRET-ALPHA" not in response.content.decode()
    # Somebody else's message and a message that was never written answer identically.
    assert response.status_code == 404
    assert client.get(f"{MESSAGES}{uuid.uuid4()}/").status_code == response.status_code


def test_superuser_and_staff_do_not_read_or_flip_foreign_messages_through_the_portal(
    client, seeded, alice, staff_user, superuser, make_message
):
    message = make_message(alice, subject="SECRET-ALPHA-SUBJECT")
    for user in (staff_user, superuser):
        client.force_login(user)
        assert client.get(f"{MESSAGES}{message.pk}/").status_code == 404
        assert client.post(f"{MESSAGES}{message.pk}/lu/").status_code == 404
    message.refresh_from_db()
    assert message.is_read is False


def test_scheduled_message_is_not_reachable_before_its_date(client, seeded, alice, make_message):
    import datetime as dt

    from core import clock

    message = make_message(alice, subject="SECRET-FUTURE", visible_from=clock.now() + dt.timedelta(days=2))
    client.force_login(alice)
    assert "SECRET-FUTURE" not in client.get(MESSAGES).content.decode()
    assert "SECRET-FUTURE" not in client.get(DASHBOARD).content.decode()
    # A message scheduled for later is, to its own recipient, a message that does not yet exist.
    assert client.get(f"{MESSAGES}{message.pk}/").status_code == 404
    assert client.post(f"{MESSAGES}{message.pk}/lu/").status_code == 404


def test_mark_as_read_only_affects_the_recipients_own_message(client, seeded, alice, bob, make_message):
    of_alice = make_message(alice)
    of_bob = make_message(bob)
    client.force_login(bob)
    assert client.post(f"{MESSAGES}{of_alice.pk}/lu/").status_code == 404
    of_alice.refresh_from_db()
    assert of_alice.is_read is False and of_alice.read_at is None
    assert client.post(f"{MESSAGES}{of_bob.pk}/lu/").status_code == 302
    of_bob.refresh_from_db()
    of_alice.refresh_from_db()
    assert of_bob.is_read is True
    assert of_alice.is_read is False, "marking one's own message must not touch anybody else's"
    assert Message.objects.filter(is_read=True).count() == 1


def test_user_b_cannot_download_user_a_document(client, seeded, alice, bob, make_document):
    doc = make_document(alice, name="SECRET-ALPHA-passeport.pdf")
    client.force_login(bob)
    assert client.get(reverse("documents:download", kwargs={"pk": doc.pk})).status_code == 403
    html = client.get(DOCUMENTS).content.decode()
    assert "SECRET-ALPHA" not in html and str(doc.pk) not in html


# ---- tenant isolation -----------------------------------------------------------------------
def test_company_account_sees_only_its_own_organisation(
    client, seeded, company_a, company_b, make_document, make_company_request, make_message, make_deadline, user_factory
):
    user_a, org_a = company_a
    user_b, org_b = company_b
    member_b = user_factory("membre@bravo-logistica.example.test", role=roles.COMPANY, full_name="Membre BRAVO")
    org_b.memberships.create(user=member_b)
    make_document(member_b, name="BRAVO-organigramme.pdf", organisation=org_b)
    make_document(user_b, name="BRAVO-bilan.pdf", organisation=org_b)
    make_company_request(user_b, company_name="BRAVO-LOGISTICA besoins")
    make_message(user_b, subject="BRAVO-communication")
    make_deadline(user_b, title="BRAVO-échéance")
    make_document(user_a, name="ALPHA-kbis.pdf", organisation=org_a)

    client.force_login(user_a)
    for path in LIST_PAGES:
        html = client.get(path).content.decode()
        assert "BRAVO" not in html, path
        assert "bravo-logistica" not in html.lower(), path
    assert org_a.name in client.get(DASHBOARD).content.decode()
    assert "ALPHA-kbis.pdf" in client.get(DOCUMENTS).content.decode()

    # and the other way round: B (owner of its organisation) sees its member's document, never A's
    client.force_login(user_b)
    documents_b = client.get(DOCUMENTS).content.decode()
    assert "BRAVO-organigramme.pdf" in documents_b and "ALPHA" not in documents_b


def test_membership_in_a_foreign_organisation_is_required_not_the_role(
    client, seeded, company_a, company_b, make_document
):
    """Holding role:company is never enough: only a membership row links an account to an organisation."""
    user_a, _org_a = company_a
    user_b, org_b = company_b
    doc = make_document(user_b, name="BRAVO-contrat.pdf", organisation=org_b)
    client.force_login(user_a)
    assert client.get(reverse("documents:download", kwargs={"pk": doc.pk})).status_code == 403


# ---- no foreign personal data in any rendered page -------------------------------------------
def test_no_personal_data_of_another_account_appears_in_any_page(
    client,
    seeded,
    alice,
    bob,
    make_company_request,
    make_contact_request,
    make_document,
    make_message,
    make_deadline,
    completed_orientation,
):
    marker_a, marker_b = "ZZALPHAZZ", "QQBRAVOQQ"
    for user, marker in ((alice, marker_a), (bob, marker_b)):
        user.full_name = f"Personne {marker}"
        user.save(update_fields=["full_name"])
        make_company_request(user, company_name=f"Société {marker}", notes=f"Notes {marker}")
        make_contact_request(user, subject=f"Sujet {marker}", message=f"Message {marker}")
        make_document(user, name=f"{marker}-document.pdf", description=f"Description {marker}")
        make_message(user, subject=f"Objet {marker}", body=f"Corps {marker}")
        make_deadline(user, title=f"Échéance {marker}", description=f"Détail {marker}", source_note=f"Source {marker}")
        completed_orientation(user)

    def pages_of(user) -> list[str]:
        paths = list(LIST_PAGES)
        paths += [f"{MESSAGES}{m.pk}/" for m in Message.objects.filter(recipient=user)]
        paths += [f"{REQUESTS}contact/{r.pk}/" for r in user.contactrequest_submissions.all()]
        paths += [f"{REQUESTS}besoins-entreprise/{r.pk}/" for r in user.companyneedsrequest_submissions.all()]
        return paths

    for viewer, own, foreign, foreign_user in ((alice, marker_a, marker_b, bob), (bob, marker_b, marker_a, alice)):
        client.force_login(viewer)
        seen_own = False
        for path in pages_of(viewer):
            response = client.get(path)
            assert response.status_code == 200, path
            html = response.content.decode()
            assert foreign not in html, (viewer.email, path)
            assert foreign_user.email not in html, (viewer.email, path)
            seen_own = seen_own or own in html
        assert seen_own, "sanity: the viewer's own marker is rendered somewhere"


# ---- back-office ----------------------------------------------------------------------------
ADMIN_MESSAGES = "/backoffice/portal/message/"
ADMIN_DEADLINES = "/backoffice/portal/deadline/"
ADMIN_NOTICES = "/backoffice/portal/portalnotice/"


def test_person_account_cannot_reach_the_backoffice(client, seeded, alice):
    client.force_login(alice)
    for path in (ADMIN_MESSAGES, ADMIN_DEADLINES, ADMIN_NOTICES):
        assert client.get(path).status_code in (302, 403), path
        assert client.get(path).status_code != 200


def test_is_staff_without_a_role_opens_nothing(client, seeded, user_factory, alice, make_message):
    make_message(alice, subject="SECRET-ALPHA-SUBJECT")
    bare = user_factory("bare-staff@example.test", is_staff=True)
    client.force_login(bare)
    for path in (ADMIN_MESSAGES, ADMIN_DEADLINES, ADMIN_NOTICES, ADMIN_MESSAGES + "add/"):
        response = client.get(path)
        assert response.status_code == 403, path
        assert "SECRET-ALPHA-SUBJECT" not in response.content.decode()


def test_staff_role_cannot_reach_admin_only_or_superadmin_only_pages(client, seeded, staff_user, alice, make_message):
    message = make_message(alice)
    client.force_login(staff_user)
    assert client.get(ADMIN_MESSAGES).status_code == 200
    # administrator-only operations on communications
    assert client.get(f"{ADMIN_MESSAGES}{message.pk}/delete/").status_code == 403
    assert client.post(f"{ADMIN_MESSAGES}{message.pk}/delete/", {"post": "yes"}).status_code == 403
    assert Message.objects.filter(pk=message.pk).exists()
    # superadmin-only areas of the back-office
    for path in ("/backoffice/accounts/user/", "/backoffice/auth/group/", "/backoffice/audit/auditevent/"):
        assert client.get(path).status_code == 403, path


def test_moderator_role_has_no_access_to_portal_admin(client, seeded, user_factory):
    moderator = user_factory("moderator@example.test", role=roles.MODERATOR, is_staff=True)
    client.force_login(moderator)
    for path in (ADMIN_MESSAGES, ADMIN_DEADLINES, ADMIN_NOTICES):
        assert client.get(path).status_code == 403, path
