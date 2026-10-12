"""Unit tests — models, gates and services (no HTTP)."""

from __future__ import annotations

import datetime as dt

import pytest
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from freezegun import freeze_time

from cms import locked_content
from consents.models import ConsentPurpose, ConsentRecord
from consents.services import ensure_consent_text
from core import flags
from forum import services
from forum.models import (
    ForumEvent,
    ForumMode,
    ForumPartner,
    ForumRegistration,
    ModeOverride,
    RegistrationCategory,
    RegistrationStatus,
    SpeakerRole,
)
from forum.tests.conftest import EVENT_END_ROME, ROME

pytestmark = pytest.mark.django_db


def _consent(email="x@example.test"):
    text = ensure_consent_text(ConsentPurpose.FORUM_REGISTRATION)
    return ConsentRecord.objects.create(
        purpose=ConsentPurpose.FORUM_REGISTRATION,
        consent_text=text,
        email=email,
        given_at=dt.datetime(2026, 9, 20, 10, 0, tzinfo=dt.UTC),
    )


def test_seed_creates_event_programme_roles_and_placeholders(event):
    assert event.date == dt.date(2026, 10, 2)
    assert (event.start_time, event.end_time) == (dt.time(15, 0), dt.time(18, 0))
    assert event.venue == "Sala della Gran Guardia"
    assert event.city == "Rovigo"
    assert event.is_primary is True
    assert event.programme_items.count() == 8
    assert event.speaker_roles.count() == 4
    placeholders = list(event.partners.order_by("order"))
    assert [p.name for p in placeholders] == ["Regione del Veneto", "Comune di Rovigo"]
    assert all(p.authorized is False and p.logo_id is None for p in placeholders)
    assert all(p.note == "loghi da ricevere con autorizzazione" for p in placeholders)


def test_seed_is_idempotent_and_keeps_editorial_changes(event):
    item = event.programme_items.first()
    item.title_fr = "Modifié par la rédaction"
    item.save()
    from forum.seeds import seed_forum_event

    seed_forum_event()
    seed_forum_event()
    assert ForumEvent.objects.count() == 1
    assert event.programme_items.count() == 8
    assert event.programme_items.get(pk=item.pk).title_fr == "Modifié par la rédaction"
    assert event.partners.count() == 2


def test_programme_seed_matches_prescribed_items(event):
    prescribed = locked_content.get("p2.forum.programme.items", "fr")[0]
    items = list(event.programme_items.order_by("order"))
    assert items[0].time_label == "15h00"
    assert items[0].title_fr == "Accueil et enregistrement"
    assert prescribed[0] == f"{items[0].time_label} — {items[0].title_fr}"
    for raw, item in zip(prescribed[1:], items[1:], strict=True):
        assert item.time_label == ""
        assert item.title_fr == raw
        assert item.is_locked_seed is True


def test_reset_programme_restores_prescribed_items(event):
    event.programme_items.all().delete()
    event.programme_items.create(order=1, title_fr="Point ajouté")
    n = services.reset_programme(event)
    assert n == 8
    titles = list(event.programme_items.order_by("order").values_list("title_fr", flat=True))
    assert titles[0] == "Accueil et enregistrement"
    assert titles[-1] == "Conclusions et prochaines étapes"
    assert "Point ajouté" not in titles


def test_speaker_roles_seeded_from_registry_without_names(event):
    roles = list(event.speaker_roles.order_by("order").values_list("role_label_fr", flat=True))
    assert roles == locked_content.get("p2.forum.speakers.roles", "fr")[0]
    assert not event.speaker_roles.exclude(person_name="").exists()


def test_speaker_authorization_requires_reference(event):
    role = event.speaker_roles.first()
    role.person_name = "Nom Test"
    role.names_authorized = True
    role.authorization_reference = "court"
    with pytest.raises(ValidationError):
        role.full_clean()
    role.authorization_reference = "e-mail de l’Avv. Badrane du 2026-09-30"
    role.full_clean()
    role.save()
    assert role.authorized_at is not None


def test_public_name_requires_both_authorisations(event):
    role = event.speaker_roles.first()
    role.person_name = "Nom Test"
    assert role.public_name(True) == ""
    role.names_authorized = True
    role.authorization_reference = "e-mail de l’Avv. Badrane du 2026-09-30"
    assert role.public_name(False) == ""
    assert role.public_name(True) == "Nom Test"
    role.authorization_reference = ""
    assert role.public_name(True) == ""


def test_partner_public_only_when_authorised_with_logo(event):
    partner = event.partners.first()
    assert partner.is_public is False
    partner.authorized = True
    partner.authorization_reference = "trasmissione del 2026-10-01"
    assert partner.is_public is False  # no logo
    partner.authorization_reference = "x"
    with pytest.raises(ValidationError):
        partner.full_clean()


def test_partner_name_unique_per_event(event):
    with pytest.raises(IntegrityError), transaction.atomic():
        ForumPartner.objects.create(event=event, name="Regione del Veneto")


def test_registration_categories_are_exactly_the_prescribed_ones():
    labels = [str(label) for _value, label in RegistrationCategory.choices]
    assert labels == locked_content.get("p2.forum.registration.categories", "fr")[0]
    assert len(labels) == 8


def test_registration_duplicate_email_case_insensitive(event):
    consent = _consent()
    ForumRegistration.objects.create(
        event=event, first_name="A", last_name="B", email="Dup@Example.test", category="other", consent=consent
    )
    with pytest.raises(IntegrityError), transaction.atomic():
        ForumRegistration.objects.create(
            event=event, first_name="C", last_name="D", email="dup@example.TEST", category="other", consent=consent
        )
    assert ForumRegistration.objects.get().email == "dup@example.test"


def test_mode_override_wins_over_flag(event, set_flag):
    assert event.effective_mode() == ForumMode.EVENT
    event.mode_override = ModeOverride.PERMANENT
    assert event.effective_mode() == ForumMode.PERMANENT
    set_flag("forum_permanent_mode", True)
    event.mode_override = ModeOverride.EVENT
    assert event.effective_mode() == ForumMode.EVENT
    event.mode_override = ModeOverride.AUTO
    assert event.effective_mode() == ForumMode.PERMANENT


def test_mode_switches_by_flag_at_event_end(event, set_flag):
    set_flag("forum_permanent_mode", True, enabled_from=EVENT_END_ROME)
    with freeze_time(dt.datetime(2026, 10, 2, 17, 59, tzinfo=ROME)):
        flags.invalidate()
        assert event.effective_mode() == ForumMode.EVENT
    with freeze_time(dt.datetime(2026, 10, 2, 18, 1, tzinfo=ROME)):
        flags.invalidate()
        assert event.effective_mode() == ForumMode.PERMANENT


def test_registration_open_rules(event, set_flag):
    with freeze_time(dt.datetime(2026, 9, 20, 12, 0, tzinfo=ROME)):
        assert event.registration_is_open() is True
        event.registration_open = False
        assert event.registration_is_open() is False
        event.registration_open = True
        event.registration_deadline = dt.datetime(2026, 9, 19, 12, 0, tzinfo=ROME)
        assert event.registration_is_open() is False
        event.registration_deadline = None
        event.capacity = 1
        ForumRegistration.objects.create(
            event=event, first_name="A", last_name="B", email="one@example.test", category="other", consent=_consent()
        )
        assert event.registration_is_open() is False
        event.capacity = None
    with freeze_time(dt.datetime(2026, 10, 2, 18, 30, tzinfo=ROME)):
        assert event.registration_is_open() is False, "closed once the event has ended"
    with freeze_time(dt.datetime(2026, 9, 20, 12, 0, tzinfo=ROME)):
        event.mode_override = ModeOverride.PERMANENT
        assert event.registration_is_open() is False, "closed in permanent mode"


def test_current_event_prefers_primary_live_edition(event):
    other = ForumEvent.objects.create(slug="other", date=dt.date(2027, 1, 1), status="published")
    assert services.current_event() == event
    event.status = "draft"
    event.save()
    assert services.current_event() == other


def test_jsonld_event_structure(event):
    payload = services.jsonld_event(event)
    assert '"@type": "Event"' in payload
    assert '"startDate": "2026-10-02T15:00:00+02:00"' in payload
    assert '"endDate": "2026-10-02T18:00:00+02:00"' in payload
    assert "Sala della Gran Guardia" in payload and "Rovigo" in payload
    assert "AGAMI" in payload
    assert "image" not in payload and "offers" not in payload


def test_anonymise_registration(event):
    reg = ForumRegistration.objects.create(
        event=event,
        first_name="Amina",
        last_name="Test",
        email="amina@example.test",
        phone="123",
        category="other",
        consent=_consent(),
        ip_hash="abc",
    )
    services.anonymise_registration(reg)
    reg.refresh_from_db()
    assert reg.is_anonymised
    assert "amina" not in reg.email and reg.first_name == "—" and reg.phone == "" and reg.ip_hash == ""
    assert reg.email.endswith("@example.invalid")


def test_csv_export_has_bom_consent_version_and_timestamp(event):
    reg = ForumRegistration.objects.create(
        event=event,
        first_name="Amina",
        last_name="Test",
        email="a@example.test",
        category="company",
        consent=_consent(),
    )
    payload = services.export_csv(ForumRegistration.objects.all())
    assert payload.startswith(b"\xef\xbb\xbf")
    text = payload.decode("utf-8-sig")
    header, row = text.splitlines()[:2]
    assert "consent_text_version" in header and "consent_given_at" in header
    assert "p2.forum.registration.consent@v1" in row
    assert "2026-09-20T10:00:00+00:00" in row
    assert reg.get_category_display() in row


def test_set_status_audits(event):
    reg = ForumRegistration.objects.create(
        event=event, first_name="A", last_name="B", email="s@example.test", category="other", consent=_consent()
    )
    from audit.models import AuditEvent

    assert services.set_status(ForumRegistration.objects.all(), RegistrationStatus.CONFIRMED) == 1
    reg.refresh_from_db()
    assert reg.status == RegistrationStatus.CONFIRMED
    assert AuditEvent.objects.filter(action="forum.registration.status").exists()


def test_speaker_role_str_and_program_item_str(event):
    assert str(event.speaker_roles.first()) == "Sénateur de la République"
    assert str(event.programme_items.first()) == "15h00 — Accueil et enregistrement"


def test_speaker_role_unauthorised_never_exposes_name_even_with_flag(event, speaker_names_flag):
    speaker_names_flag(True)
    role = SpeakerRole.objects.filter(event=event).first()
    role.person_name = "Nom Caché"
    role.save()
    assert all(s.person_name == "" for s in services.public_speakers(event))
