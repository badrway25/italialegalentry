"""Service layer: dashboard assembly, scoping, defensive sibling access, GDPR hooks, seeds."""

from __future__ import annotations

import datetime as dt

import pytest
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.http import Http404

from accounts import roles
from accounts.models import AccountType
from audit.models import AuditEvent
from cms.models import PublicationStatus
from core import clock
from portal import services
from portal.models import Deadline, Message, PortalNotice

pytestmark = pytest.mark.django_db


def _cards(user) -> dict[str, services.Card]:
    return {card.key: card for card in services.dashboard_context(user)["cards"]}


# ---- dashboard ------------------------------------------------------------------------------
def test_dashboard_context_for_a_fresh_person_is_all_empty_states(alice):
    cards = _cards(alice)
    assert list(cards) == ["requests", "orientation", "documents", "deadlines", "messages"]
    for card in cards.values():
        assert card.available is True
        assert card.count == 0 and card.items == []
        assert card.empty_title, card.key


def test_dashboard_counts_are_the_real_rows_of_the_account(
    alice, bob, make_company_request, make_contact_request, make_document, make_message, make_deadline
):
    for i in range(4):
        make_contact_request(alice, subject=f"Sujet {i}", message=f"Message {i}")
    make_company_request(alice)
    make_document(alice, name="a.pdf")
    make_document(alice, name="b.pdf")
    make_message(alice, subject="M1")
    read = make_message(alice, subject="M2")
    services.mark_message_read(alice, read.pk)
    make_deadline(alice, days=5)
    make_deadline(alice, days=-2)
    # noise that must never be counted
    make_contact_request(bob)
    make_document(bob)
    make_message(bob)
    make_deadline(bob)

    cards = _cards(alice)
    assert cards["requests"].count == 5 and len(cards["requests"].items) == services.DASHBOARD_LATEST
    assert cards["documents"].count == 2
    assert cards["messages"].count == 2 and cards["messages"].badge_label.startswith("1 ")
    assert cards["deadlines"].count == 2 and cards["deadlines"].badge_label.startswith("1 ")
    assert services.unread_count(alice) == 1
    assert services.unread_count(bob) == 1


def test_cards_are_driven_by_account_type_and_roles(alice, company_a, staff_user, user_factory):
    company_user, _org = company_a
    assert "organisation" not in _cards(alice)
    company_cards = _cards(company_user)
    assert "organisation" in company_cards and "orientation" not in company_cards
    assert company_cards["organisation"].count == 1
    university = user_factory("uni@example.test", role=roles.UNIVERSITY, account_type=AccountType.UNIVERSITY)
    uni_cards = _cards(university)
    assert uni_cards["organisation"].count == 0 and uni_cards["organisation"].empty_title


def test_orientation_card_shows_the_latest_saved_result(alice, completed_orientation):
    _session, result = completed_orientation(alice)
    card = _cards(alice)["orientation"]
    assert card.count == 1
    assert card.items[0].title == result.outcome.title_fr
    assert f"v{result.ruleset_version}" in card.items[0].meta


def test_dashboard_survives_a_missing_sibling_app(alice, monkeypatch, caplog):
    """A sibling that disappears/changes yields an honest « indisponible » card, never a 500."""
    real_import = services._import
    monkeypatch.setattr(services, "_import", lambda name: None if name.startswith("orientation") else real_import(name))
    monkeypatch.setattr(
        services, "_get_model", lambda app, model: None if app == "documents" else services.apps.get_model(app, model)
    )
    cards = _cards(alice)
    assert cards["orientation"].available is False
    assert cards["documents"].available is False
    assert cards["requests"].available is True and cards["messages"].available is True
    assert alice.email not in caplog.text


def test_requests_fall_back_to_the_models_when_the_helper_is_gone(alice, bob, make_contact_request, monkeypatch):
    mine = make_contact_request(alice, subject="Sujet Alice")
    make_contact_request(bob, subject="Sujet Bob")
    real_import = services._import
    monkeypatch.setattr(services, "_import", lambda name: None if name == "enquiries.services" else real_import(name))
    items = services.requests_for(alice)
    assert [(i.kind, i.pk) for i in items] == [("contact", mine.pk)]


def test_requests_recheck_ownership_of_rows_returned_by_a_sibling(alice, bob, make_contact_request, monkeypatch):
    """Even a buggy sibling helper returning somebody else's row cannot leak it."""
    foreign = make_contact_request(bob, subject="SECRET-BOB")

    class Leaky:
        @staticmethod
        def submissions_for_user(user):
            return [foreign]

    real_import = services._import
    monkeypatch.setattr(services, "_import", lambda name: Leaky if name == "enquiries.services" else real_import(name))
    assert services.requests_for(alice) == []


# ---- requests -------------------------------------------------------------------------------
def test_get_own_request_returns_rows_and_consent_metadata(alice, make_company_request):
    obj = make_company_request(alice, company_name="Atelier Alpha")
    detail = services.get_own_request(alice, "besoins-entreprise", obj.pk)
    assert detail["item"].title == "Atelier Alpha"
    labels = [label for label, _value in detail["rows"]]
    assert len(labels) >= 5
    assert all(value for _label, value in detail["rows"])
    consent = detail["consent"]
    assert consent["version"] == obj.consent.consent_text.version
    assert consent["given_at"] == obj.consent.given_at
    assert consent["purpose"]


def test_get_own_request_answers_404_for_everything_the_caller_may_not_see(alice, bob, make_contact_request):
    """
    One answer for four different situations, and that is the point.

    Somebody else's row, a row that never existed, a kind that does not exist and an anonymised row
    all raise Http404. It used to be PermissionDenied for the first, which a view renders as 403 —
    and a 403 on somebody else's request confirms that the request exists, which is a disclosure in
    itself (PERMISSION_MODEL L-06/L-07).
    """
    obj = make_contact_request(alice)
    other = make_contact_request(bob, subject="Autre")
    for user, kind, pk in (
        (bob, "contact", obj.pk),
        (alice, "contact", other.pk),
        (alice, "contact", obj.pk + 999),
        (alice, "unknown-kind", obj.pk),
    ):
        with pytest.raises(Http404):
            services.get_own_request(user, kind, pk)


def test_anonymised_request_disappears_from_the_portal(alice, make_contact_request):
    from enquiries.services import anonymise

    obj = make_contact_request(alice)
    anonymise(obj, reason="test")
    assert services.requests_for(alice) == []
    # 404, not 403: an anonymised record is gone as far as anyone is concerned, including the person
    # it described. A 403 would assert that something is still there.
    with pytest.raises(Http404):
        services.get_own_request(alice, "contact", obj.pk)


def test_forum_registration_is_listed_only_through_the_account_link(alice, bob):
    from consents.services import record_consent
    from forum.models import ForumEvent, ForumRegistration, RegistrationCategory

    event = ForumEvent.objects.create(slug="edition-test")
    consent = record_consent(None, "forum_registration", email=alice.email, user=alice, language="fr")
    linked = ForumRegistration.objects.create(
        event=event,
        first_name="Alice",
        last_name="Alpha",
        email=alice.email,
        category=RegistrationCategory.OTHER,
        consent=consent,
        user=alice,
    )
    # same e-mail as Bob but NOT linked to his account → never listed for him
    consent_b = record_consent(None, "forum_registration", email=bob.email, language="fr")
    ForumRegistration.objects.create(
        event=ForumEvent.objects.create(slug="edition-test-2", date=dt.date(2026, 11, 1)),
        first_name="Bob",
        last_name="Bravo",
        email=bob.email,
        category=RegistrationCategory.OTHER,
        consent=consent_b,
    )
    assert [(i.kind, i.pk) for i in services.requests_for(alice)] == [("inscription-forum", linked.pk)]
    assert services.requests_for(bob) == []
    detail = services.get_own_request(alice, "inscription-forum", linked.pk)
    assert ("e-mail", alice.email) in [(label.lower(), value) for label, value in detail["rows"]]
    with pytest.raises(Http404):
        services.get_own_request(bob, "inscription-forum", linked.pk)


# ---- messages -------------------------------------------------------------------------------
def test_unread_messages_is_a_scoped_queryset(alice, bob, make_message):
    first = make_message(alice, subject="Un")
    make_message(alice, subject="Programmé", visible_from=clock.now() + dt.timedelta(days=1))
    make_message(bob)
    assert list(services.unread_messages(alice)) == [first]
    services.mark_message_read(alice, first.pk)
    assert services.unread_messages(alice).count() == 0
    assert services.unread_count(bob) == 1


def test_mark_message_read_is_idempotent_and_audited(alice, make_message):
    message = make_message(alice)
    services.mark_message_read(alice, message.pk)
    message.refresh_from_db()
    first_read_at = message.read_at
    assert message.is_read and first_read_at is not None
    services.mark_message_read(alice, message.pk)
    message.refresh_from_db()
    assert message.read_at == first_read_at
    events = AuditEvent.objects.filter(action="portal.message.read", target_id=str(message.pk))
    assert events.count() == 1


def test_send_message_audits_without_personal_content(alice, staff_user, make_deadline):
    deadline = make_deadline(alice)
    message = services.send_message(
        recipient=alice, sender=staff_user, subject="Objet CONFIDENTIEL", body="Corps CONFIDENTIEL", related=deadline
    )
    event = AuditEvent.objects.get(action="portal.message.created", target_id=str(message.pk))
    dumped = f"{event.metadata} {event.target_repr}"
    assert "CONFIDENTIEL" not in dumped and alice.email not in dumped  # neither the body nor the subject
    assert event.metadata["recipient_id"] == alice.pk and event.metadata["related"] == "deadline"


def test_related_link_only_for_records_owned_by_the_reader(alice, bob, staff_user, make_contact_request, make_deadline):
    own = make_contact_request(alice)
    foreign = make_contact_request(bob, subject="De Bob")
    to_own = services.send_message(recipient=alice, sender=staff_user, subject="S", body="B", related=own)
    to_foreign = services.send_message(recipient=alice, sender=staff_user, subject="S", body="B", related=foreign)
    link = services.related_link(alice, to_own)
    assert link and link["url"].endswith(f"/mes-demandes/contact/{own.pk}/")
    assert services.related_link(alice, to_foreign) is None, "a staff mistake must never leak a foreign record"
    about_deadline = services.send_message(
        recipient=alice, sender=staff_user, subject="S", body="B", related=make_deadline(alice)
    )
    assert services.related_link(alice, about_deadline)["url"].endswith("/mes-echeances/")
    dangling = Message.objects.create(
        recipient=alice, subject="S", body="B", content_type=ContentType.objects.get_for_model(Deadline), object_id="x"
    )
    assert services.related_link(alice, dangling) is None


# ---- documents / organisation ---------------------------------------------------------------
def test_documents_page_lists_only_own_and_owned_organisation_documents(
    company_a, company_b, make_document, user_factory
):
    user_a, org_a = company_a
    user_b, org_b = company_b
    member_a = user_factory("membre@alpha-industrie.example.test", role=roles.COMPANY)
    org_a.memberships.create(user=member_a)
    make_document(user_a, name="propre-a.pdf")
    make_document(member_a, name="membre-a.pdf", organisation=org_a)
    make_document(user_b, name="propre-b.pdf", organisation=org_b)

    page_a = services.documents_page(user_a)
    assert [d["name"] for d in page_a["documents"]] == ["propre-a.pdf"]
    assert [d["name"] for d in page_a["organisation_documents"]] == ["membre-a.pdf"]
    # a plain MEMBER is not responsible for the organisation → no organisation documents
    assert services.documents_page(member_a)["organisation_documents"] == []
    page_b = services.documents_page(user_b)
    assert [d["name"] for d in page_b["documents"]] == ["propre-b.pdf"]
    assert page_b["organisation_documents"] == []


def test_infected_or_purged_documents_have_no_download_link(alice, make_document):
    from documents.models import ScanStatus

    make_document(alice, name="sain.pdf")
    make_document(alice, name="infecte.pdf", scan_status=ScanStatus.INFECTED)
    make_document(alice, name="purge.pdf", file_removed_at=clock.now())
    by_name = {d["name"]: d for d in services.documents_page(alice)["documents"]}
    assert by_name["sain.pdf"]["url"].startswith("/documents/")
    assert by_name["infecte.pdf"]["url"] == "" and by_name["purge.pdf"]["url"] == ""


def test_organisation_summary_never_mentions_other_organisations(company_a, company_b):
    user_a, org_a = company_a
    rows = services.organisations_for(user_a)
    assert [r["name"] for r in rows] == [org_a.name]


# ---- notices --------------------------------------------------------------------------------
def test_notices_for_filters_by_audience_and_publication(alice, company_a):
    company_user, _org = company_a
    PortalNotice.objects.create(audience="all", heading_fr="Tous", body_fr="x", status=PublicationStatus.PUBLISHED)
    PortalNotice.objects.create(audience="company", heading_fr="Ent.", body_fr="x", status=PublicationStatus.PUBLISHED)
    PortalNotice.objects.create(audience="all", heading_fr="Brouillon", body_fr="x")
    assert [n.heading_fr for n in services.notices_for(alice)] == ["Tous"]
    assert sorted(n.heading_fr for n in services.notices_for(company_user)) == ["Ent.", "Tous"]


# ---- GDPR hooks -----------------------------------------------------------------------------
def test_personal_data_export_contains_only_own_portal_rows(alice, bob, make_message, make_deadline):
    from accounts.services import export_user_data

    make_message(alice, subject="Pour Alice")
    make_message(bob, subject="Pour Bob")
    make_deadline(alice, title="Échéance Alice")
    make_deadline(bob, title="Échéance Bob")
    section = export_user_data(alice)["portal"]
    assert [m["subject"] for m in section["messages"]] == ["Pour Alice"]
    assert [d["title"] for d in section["deadlines"]] == ["Échéance Alice"]


def test_account_anonymisation_erases_messages_and_deadlines(alice, bob, make_message, make_deadline):
    from accounts.services import anonymise_user

    make_message(alice)
    make_deadline(alice)
    keep = make_message(bob)
    anonymise_user(alice, reason="test")
    assert Message.objects.filter(recipient_id=alice.pk).count() == 0
    assert Deadline.objects.filter(owner_id=alice.pk).count() == 0
    assert Message.objects.filter(pk=keep.pk).exists()


# ---- seeds / misc ---------------------------------------------------------------------------
def test_seed_is_idempotent_and_never_publishes(db):
    call_command("seed_all", "--only", "portal.", verbosity=0)
    notice = PortalNotice.objects.get()
    notice.heading_fr = "Titre modifié par la rédaction"
    notice.save()
    call_command("seed_all", "--only", "portal.", verbosity=0)
    assert PortalNotice.objects.count() == 1
    notice.refresh_from_db()
    assert notice.heading_fr == "Titre modifié par la rédaction"
    assert notice.status == PublicationStatus.DRAFT and PortalNotice.objects.live().count() == 0


def test_paginate_is_lenient():
    page = services.paginate(list(range(25)), "not-a-number")
    assert page.number == 1 and len(page.object_list) == services.PAGE_SIZE
    assert services.paginate(list(range(25)), "999").number == 3


def test_navigation_shows_unread_count_and_current_entry(alice, make_message):
    make_message(alice)
    nav = services.navigation(alice, "messages")
    current = [entry for entry in nav if entry["current"]]
    assert len(current) == 1 and "(1)" in current[0]["label"]
    # The ORDER of the reserved area's own entries, which is a reading order and not an accident.
    # Since design V4 (docs/design-v4/CREATIVE_DIRECTION.md §3.9) it is the order of the rail's
    # groups: the journey (where you are, who you are, your path), then the file (cases, requests,
    # documents, what is owed and by when), then the exchanges.
    #
    # Asserted as a PREFIX, not as the whole list. The help desk and the Academy follow, and the
    # complete set of reachable surfaces is the subject of
    # `test_navigation_reaches_every_surface.py` — which exists because both of those were
    # unreachable by clicking while every test here was green.
    assert [e["key"] for e in nav][:8] == [
        "dashboard",
        "situation",
        "pathways",
        "cases",
        "requests",
        "documents",
        "deadlines",
        "messages",
    ]
    # Each entry carries what the rail draws: a glyph of the sprite and a group.
    assert all(entry["icon"] and entry["group"] for entry in nav)
