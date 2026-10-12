"""
Independent-review regression tests of the reserved area (adversarial pass).

Each test pins a gap found while reviewing the builder's work:

* IDOR on the FOURTH request kind (forum registrations), not only on the three enquiry models;
* audit rows / ``__str__`` never carry free text written about a person (they outlive GDPR erasure
  and are copied to the application log by ``audit.services.record``);
* every deletion path of the back-office is audited, including the bulk action;
* the ``role:superadmin`` group is honoured by the portal back-office like ``accounts.permissions.can``;
* stored markup is always escaped; state never changes on a non-POST method;
* the pages also work with the PROJECT-WIDE seed (menus, banners, flags), not only the narrow one.
"""

from __future__ import annotations

import datetime as dt

import pytest
from django.contrib.contenttypes.models import ContentType

from accounts import roles
from audit.models import AuditEvent
from cms.models import PublicationStatus
from portal import services
from portal.models import Deadline, Message, PortalNotice
from portal.tests.conftest import DASHBOARD, DEADLINES, DOCUMENTS, MESSAGES, PATHWAYS, REQUESTS
from tests.conftest import seeded as project_seeded  # noqa: F401 — the project-wide seed, under another name

pytestmark = [pytest.mark.django_db, pytest.mark.security]

ADMIN_MESSAGES = "/backoffice/portal/message/"
ADMIN_DEADLINES = "/backoffice/portal/deadline/"
ADMIN_NOTICES = "/backoffice/portal/portalnotice/"
XSS = "<script>alert('x')</script><img src=x onerror=alert(1)>"


@pytest.fixture
def make_registration(db):
    from consents.services import record_consent
    from forum.models import ForumEvent, ForumRegistration, RegistrationCategory

    counter = {"n": 0}

    def _make(email, user=None, **fields):
        counter["n"] += 1
        event = ForumEvent.objects.create(slug=f"edition-review-{counter['n']}", date=dt.date(2026, 10, 29))
        consent = record_consent(None, "forum_registration", email=email, user=user, language="fr")
        defaults = {"first_name": "Prénom", "last_name": "Nom", "category": RegistrationCategory.OTHER}
        defaults.update(fields)
        return ForumRegistration.objects.create(event=event, email=email, consent=consent, user=user, **defaults)

    return _make


# ---- IDOR: forum registrations ----------------------------------------------------------------
def test_user_b_cannot_open_user_a_forum_registration_even_with_the_right_id(
    client, seeded, alice, bob, make_registration
):
    of_alice = make_registration(alice.email, user=alice, last_name="SECRET-ALPHA-NOM", phone="+212 600 000 001")
    path = f"{REQUESTS}inscription-forum/{of_alice.pk}/"
    client.force_login(bob)
    response = client.get(path)
    # 404 rather than 403 — see get_own_request: "not yours" must read exactly like "not there".
    assert response.status_code == 404
    assert "SECRET-ALPHA-NOM" not in response.content.decode()
    assert "SECRET-ALPHA-NOM" not in client.get(REQUESTS).content.decode()
    client.force_login(alice)
    html = client.get(path).content.decode()
    assert "SECRET-ALPHA-NOM" in html and "+212 600 000 001" in html


def test_registration_with_my_email_but_not_linked_to_my_account_stays_out_of_the_portal(
    client, seeded, bob, make_registration
):
    """Anybody can type somebody else's address in a public form: the e-mail is never an ownership proof."""
    unlinked = make_registration(bob.email, user=None, last_name="USURPATEUR")
    client.force_login(bob)
    assert "USURPATEUR" not in client.get(REQUESTS).content.decode()
    assert client.get(f"{REQUESTS}inscription-forum/{unlinked.pk}/").status_code == 404


# ---- audit rows never carry free text ---------------------------------------------------------
def test_audit_rows_never_contain_the_subject_title_or_body(client, seeded, staff_user, alice, user_factory):
    administrator = user_factory("administrator@example.test", role=roles.ADMINISTRATOR, is_staff=True)
    message = services.send_message(
        recipient=alice, sender=staff_user, subject="Objet CONFIDENTIEL-SUJET", body="Corps CONFIDENTIEL-CORPS"
    )
    services.mark_message_read(alice, message.pk)
    client.force_login(staff_user)
    response = client.post(
        f"{ADMIN_DEADLINES}add/",
        {
            "account_email": alice.email,
            "title": "Rendez-vous CONFIDENTIEL-TITRE",
            "due_on": "2026-11-15",
            "kind": "procedure",
            "status": "open",
            "description": "Détail CONFIDENTIEL-DETAIL",
            "source_note": "",
        },
    )
    assert response.status_code == 302, response.content.decode()[:1500]
    deadline = Deadline.objects.get()
    client.force_login(administrator)
    assert client.post(f"{ADMIN_DEADLINES}{deadline.pk}/delete/", {"post": "yes"}).status_code == 302
    assert client.post(f"{ADMIN_MESSAGES}{message.pk}/delete/", {"post": "yes"}).status_code == 302

    events = AuditEvent.objects.filter(action__startswith="portal.")
    assert {e.action for e in events} >= {
        "portal.message.created",
        "portal.message.read",
        "portal.message.deleted",
        "portal.deadline.created",
        "portal.deadline.deleted",
    }
    for event in events:
        dumped = f"{event.target_repr} {event.metadata}"
        assert "CONFIDENTIEL" not in dumped, (event.action, dumped)
        assert alice.email not in dumped, (event.action, dumped)
    assert "CONFIDENTIEL" not in str(message) and "CONFIDENTIEL" not in str(deadline)
    assert alice.email not in str(message) and alice.email not in str(deadline)


def test_bulk_delete_action_is_audited_row_by_row(client, seeded, user_factory, alice, make_message, make_deadline):
    administrator = user_factory("administrator@example.test", role=roles.ADMINISTRATOR, is_staff=True)
    first, second = make_message(alice, subject="Un"), make_message(alice, subject="Deux")
    deadline = make_deadline(alice)
    client.force_login(administrator)
    response = client.post(
        ADMIN_MESSAGES,
        {"action": "delete_selected", "_selected_action": [str(first.pk), str(second.pk)], "post": "yes"},
    )
    assert response.status_code == 302 and Message.objects.count() == 0
    audited = set(AuditEvent.objects.filter(action="portal.message.deleted").values_list("target_id", flat=True))
    assert audited == {str(first.pk), str(second.pk)}
    response = client.post(
        ADMIN_DEADLINES, {"action": "delete_selected", "_selected_action": [str(deadline.pk)], "post": "yes"}
    )
    assert response.status_code == 302 and Deadline.objects.count() == 0
    assert AuditEvent.objects.filter(action="portal.deadline.deleted", target_id=str(deadline.pk)).count() == 1


def test_staff_role_cannot_bulk_delete(client, seeded, staff_user, alice, make_message):
    message = make_message(alice)
    client.force_login(staff_user)
    client.post(ADMIN_MESSAGES, {"action": "delete_selected", "_selected_action": [str(message.pk)], "post": "yes"})
    assert Message.objects.filter(pk=message.pk).exists()


# ---- back-office roles ------------------------------------------------------------------------
def test_superadmin_role_group_is_honoured_by_the_portal_backoffice(client, seeded, user_factory, alice, make_message):
    """``accounts.permissions.can`` treats role:superadmin like a superuser — so does the admin."""
    message = make_message(alice)
    superadmin = user_factory("superadmin-role@example.test", role=roles.SUPERADMIN, is_staff=True)
    assert superadmin.is_superuser is False
    client.force_login(superadmin)
    for path in (ADMIN_MESSAGES, ADMIN_DEADLINES, ADMIN_NOTICES, f"{ADMIN_MESSAGES}{message.pk}/delete/"):
        assert client.get(path).status_code == 200, path


def test_superadmin_role_without_is_staff_opens_nothing(client, seeded, user_factory):
    outsider = user_factory("superadmin-nostaff@example.test", role=roles.SUPERADMIN)
    client.force_login(outsider)
    for path in (ADMIN_MESSAGES, ADMIN_DEADLINES, ADMIN_NOTICES):
        assert client.get(path).status_code in (302, 403), path


# ---- stored markup is always escaped ----------------------------------------------------------
def test_stored_markup_is_escaped_everywhere(
    client, seeded, alice, staff_user, make_message, make_deadline, make_contact_request, make_document
):
    message = make_message(alice, subject=f"Objet {XSS}", body=f"Corps {XSS}")
    make_deadline(alice, title=f"Titre {XSS}", description=f"Détail {XSS}", source_note=f"Origine {XSS}")
    request_row = make_contact_request(alice, subject=f"Sujet {XSS}", message=f"Message {XSS}")
    make_document(alice, name=f"{XSS}.pdf", description=f"Description {XSS}")
    PortalNotice.objects.create(
        heading_fr=f"Avis {XSS}", body_fr=f"Texte {XSS}", status=PublicationStatus.PUBLISHED, author=staff_user
    )
    client.force_login(alice)
    paths = [DASHBOARD, REQUESTS, DOCUMENTS, DEADLINES, MESSAGES, f"{MESSAGES}{message.pk}/"]
    paths.append(f"{REQUESTS}contact/{request_row.pk}/")
    for path in paths:
        response = client.get(path)
        assert response.status_code == 200, path
        html = response.content.decode()
        assert "<script>alert(" not in html, path
        assert "<img src=x" not in html, path
    assert "&lt;script&gt;" in client.get(f"{MESSAGES}{message.pk}/").content.decode()


# ---- HTTP methods -----------------------------------------------------------------------------
@pytest.mark.parametrize("method", ["get", "head", "put", "patch", "delete"])
def test_mark_as_read_accepts_post_only(client, seeded, alice, make_message, method):
    message = make_message(alice)
    client.force_login(alice)
    response = getattr(client, method)(f"{MESSAGES}{message.pk}/lu/")
    assert response.status_code == 405
    message.refresh_from_db()
    assert message.is_read is False


@pytest.mark.parametrize("method", ["post", "put", "delete"])
def test_read_only_pages_refuse_writing_methods(client, seeded, alice, method):
    client.force_login(alice)
    for path in (DASHBOARD, REQUESTS, PATHWAYS, DOCUMENTS, DEADLINES, MESSAGES):
        assert getattr(client, method)(path).status_code == 405, (method, path)


# ---- related link never leaks a foreign document ----------------------------------------------
def test_message_linked_to_a_foreign_document_shows_no_link(client, seeded, alice, bob, staff_user, make_document):
    foreign = make_document(bob, name="SECRET-BRAVO.pdf")
    message = Message.objects.create(
        recipient=alice,
        sender=staff_user,
        subject="Objet",
        body="Corps",
        content_type=ContentType.objects.get_for_model(type(foreign)),
        object_id=str(foreign.pk),
    )
    client.force_login(alice)
    html = client.get(f"{MESSAGES}{message.pk}/").content.decode()
    assert "SECRET-BRAVO" not in html and str(foreign.pk) not in html
    assert services.related_link(alice, message) is None


# ---- project-wide seed ------------------------------------------------------------------------
def test_pages_render_with_the_project_wide_seed_in_four_languages(
    client,
    project_seeded,  # noqa: F811
    alice,
    bob,
    make_message,
    make_deadline,
    make_contact_request,
):
    make_message(alice, subject="Objet ALPHA")
    make_message(bob, subject="Objet QQBRAVOQQ")
    make_deadline(alice)
    make_contact_request(alice)
    client.force_login(alice)
    for lang in ("fr", "it", "en", "ar"):
        for path in (DASHBOARD, REQUESTS, PATHWAYS, DOCUMENTS, DEADLINES, MESSAGES):
            response = client.get(path.replace("/fr/", f"/{lang}/", 1))
            assert response.status_code == 200, (lang, path)
            html = response.content.decode()
            assert "QQBRAVOQQ" not in html and bob.email not in html, (lang, path)
            assert html.count("<h1") == 1, (lang, path)


# ---- query budget -----------------------------------------------------------------------------
def test_dashboard_query_count_does_not_grow_with_the_number_of_rows(
    client,
    seeded,
    alice,
    make_message,
    make_deadline,
    make_contact_request,
    make_document,
    completed_orientation,
    django_assert_max_num_queries,
):
    """The dashboard shows the latest three rows of each card: its cost must not follow the history size."""
    from django.db import connection
    from django.test.utils import CaptureQueriesContext

    client.force_login(alice)

    def populate(n):
        for i in range(n):
            make_message(alice, subject=f"Objet {i}")
            make_deadline(alice, title=f"Échéance {i}")
            make_contact_request(alice, subject=f"Sujet {i}")
            make_document(alice, name=f"piece-{i}.pdf")
            completed_orientation(alice)

    populate(2)
    client.get(DASHBOARD)  # warm caches (site settings, flags, content types)
    with CaptureQueriesContext(connection) as small:
        assert client.get(DASHBOARD).status_code == 200
    populate(8)
    with CaptureQueriesContext(connection) as large:
        assert client.get(DASHBOARD).status_code == 200
    assert len(large) <= len(small) + 2, (len(small), len(large))


# ---- breadcrumb of the detail pages -------------------------------------------------------------
def test_detail_breadcrumb_is_shortened_but_the_h1_keeps_the_full_wording(client, seeded, alice, make_message):
    import re

    subject = "Convocation " + "W" * 100 + " FIN-DU-SUJET"
    message = make_message(alice, subject=subject)
    client.force_login(alice)
    html = client.get(f"{MESSAGES}{message.pk}/").content.decode()
    crumbs = re.search(r'<nav class="breadcrumbs.*?</nav>', html, flags=re.S).group(0)
    assert "FIN-DU-SUJET" not in crumbs and "…" in crumbs
    heading = re.search(r"<h1[^>]*>(.*?)</h1>", html, flags=re.S).group(1)
    assert subject in heading


# ---- second review pass -----------------------------------------------------------------------
def test_personal_data_export_is_complete_and_includes_scheduled_communications(alice, bob, make_message):
    """GDPR art. 15: a message hidden from the inbox until its date is still data held about the person."""
    from accounts.services import export_user_data
    from core import clock

    later = clock.now() + dt.timedelta(days=3)
    make_message(alice, subject="Visible")
    make_message(alice, subject="Programmée", visible_from=later)
    make_message(bob, subject="Pour Bob", visible_from=later)
    assert [m.subject for m in services.inbox(alice)] == ["Visible"], "the inbox itself still hides it"
    exported = export_user_data(alice)["portal"]["messages"]
    assert sorted(m["subject"] for m in exported) == ["Programmée", "Visible"]
    assert {m["subject"]: m["visible_from"] for m in exported} == {"Visible": None, "Programmée": later}


def test_organisation_documents_cost_does_not_follow_the_number_of_documents(
    client, seeded, company_a, user_factory, make_document
):
    """The object-level policy is consulted once per organisation — it used to cost two queries per row."""
    from django.db import connection
    from django.test.utils import CaptureQueriesContext

    from accounts.models import MembershipRole

    owner, organisation = company_a
    member = user_factory("membre@alpha-industrie.example.test", role=roles.COMPANY)
    organisation.memberships.create(user=member, role=MembershipRole.MEMBER)
    for i in range(3):
        make_document(member, name=f"membre-{i}.pdf", organisation=organisation)
    client.force_login(owner)
    client.get(DOCUMENTS)  # warm caches
    with CaptureQueriesContext(connection) as small:
        assert client.get(DOCUMENTS).content.decode().count("membre-") == 3
    for i in range(3, 23):
        make_document(member, name=f"membre-{i}.pdf", organisation=organisation)
    with CaptureQueriesContext(connection) as large:
        assert client.get(DOCUMENTS).content.decode().count("membre-") == 23
    assert len(large) <= len(small) + 1, (len(small), len(large))


def test_organisation_documents_are_bounded_and_the_page_says_so(
    client, seeded, company_a, user_factory, make_document
):
    from accounts.models import MembershipRole

    owner, organisation = company_a
    member = user_factory("membre@alpha-industrie.example.test", role=roles.COMPANY)
    organisation.memberships.create(user=member, role=MembershipRole.MEMBER)
    for i in range(4):
        make_document(member, name=f"membre-{i}.pdf", organisation=organisation)
    assert len(services.organisation_documents_for(owner, limit=3)) == 3
    client.force_login(owner)
    assert "les plus récents sont affichés" not in client.get(DOCUMENTS).content.decode()
    # a plain member never gets the organisation table, whatever the number of documents
    client.force_login(member)
    make_document(owner, name="ALPHA-RESPONSABLE.pdf", organisation=organisation)
    html = client.get(DOCUMENTS).content.decode()
    assert "ALPHA-RESPONSABLE" not in html and "org-documents-title" not in html
    assert services.organisation_documents_for(member) == []


def test_organisation_refused_by_the_documents_policy_is_dropped_entirely(
    company_a, user_factory, make_document, monkeypatch
):
    """Deny by default: when the sibling policy says no, no row of that organisation is listed."""
    from accounts.models import MembershipRole

    owner, organisation = company_a
    member = user_factory("membre@alpha-industrie.example.test", role=roles.COMPANY)
    organisation.memberships.create(user=member, role=MembershipRole.MEMBER)
    make_document(member, name="membre.pdf", organisation=organisation)
    assert [d["name"] for d in services.organisation_documents_for(owner)] == ["membre.pdf"]
    monkeypatch.setattr(services, "can", lambda *a, **k: False)
    assert services.organisation_documents_for(owner) == []


def test_account_panel_never_prints_the_email_address_twice(client, seeded, user_factory):
    nameless = user_factory("sans-nom@example.test", role=roles.PERSON)
    client.force_login(nameless)
    import re

    html = client.get(DASHBOARD).content.decode()
    panel = re.search(r'<p class="portal-account__identity">.*?</p>', html, flags=re.S).group(0)
    assert panel.count("sans-nom@example.test") == 1 and "<strong" not in panel


def test_request_detail_marks_the_language_of_the_values_not_of_the_ui_labels(
    client, seeded, alice, make_contact_request
):
    row = make_contact_request(alice, subject="Sujet", message="Bonjour.")
    client.force_login(alice)
    html = client.get(f"/it/espace-reserve/mes-demandes/contact/{row.pk}/").content.decode()
    assert '<dl class="portal-facts" lang=' not in html
    assert '<dd dir="auto" lang="fr">' in html


def test_pathways_page_presents_only_the_requested_page(alice, completed_orientation, monkeypatch):
    """Paginate first, present afterwards: eleven saved results never cost eleven presentations."""
    import orientation.services as orientation_services

    for _ in range(services.PAGE_SIZE + 1):
        completed_orientation(alice)
    calls = []
    original = orientation_services.present_result
    monkeypatch.setattr(orientation_services, "present_result", lambda r, *a, **k: calls.append(r) or original(r))
    second = services.pathways_page(alice, "2")
    assert second["available"] and len(second["page_obj"].object_list) == 1 and len(calls) == 1
    calls.clear()
    card = {c.key: c for c in services.dashboard_context(alice)["cards"]}["orientation"]
    assert card.count == services.PAGE_SIZE + 1 and len(card.items) == 1 and len(calls) == 1
