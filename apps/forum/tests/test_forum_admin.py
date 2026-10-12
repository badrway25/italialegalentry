"""Back-office: programme editing/reset, registration actions, CSV export, permissions, warnings."""

from __future__ import annotations

import datetime as dt

import pytest
from django.urls import reverse

from audit.models import AuditEvent
from consents.models import ConsentPurpose, ConsentRecord
from consents.services import ensure_consent_text
from forum.admin import SPEAKER_WARNING
from forum.models import ForumRegistration, RegistrationStatus, SpeakerRole

pytestmark = pytest.mark.django_db


@pytest.fixture
def admin_client(client, superuser):
    client.force_login(superuser)
    return client


def _registration(event, email="r@example.test", **extra):
    text = ensure_consent_text(ConsentPurpose.FORUM_REGISTRATION)
    consent = ConsentRecord.objects.create(
        purpose=ConsentPurpose.FORUM_REGISTRATION,
        consent_text=text,
        email=email,
        given_at=dt.datetime(2026, 9, 21, 9, 30, tzinfo=dt.UTC),
    )
    return ForumRegistration.objects.create(
        event=event,
        first_name="Amina",
        last_name="Test",
        email=email,
        category="company",
        consent=consent,
        **extra,
    )


def test_event_changelist_and_change_form_render(admin_client, event):
    assert admin_client.get(reverse("admin:forum_forumevent_changelist")).status_code == 200
    response = admin_client.get(reverse("admin:forum_forumevent_change", args=[event.pk]))
    assert response.status_code == 200
    html = response.content.decode()
    assert "Accueil et enregistrement" in html
    assert "Sénateur de la République" in html
    assert "Regione del Veneto" in html  # placeholder visible in the back-office only


def test_programme_editable_via_admin_inline(admin_client, event):
    item = event.programme_items.order_by("order").first()
    url = reverse("admin:forum_forumevent_change", args=[event.pk])
    response = admin_client.get(url)
    html = response.content.decode()
    assert 'name="programme_items-0-title_fr"' in html, "programme inline is editable"
    # edit the item as the inline formset would; the public page must reflect it
    item.title_fr = "Accueil modifié"
    item.save()
    html = admin_client.get("/fr/forum/").content.decode()
    assert "Accueil modifié" in html


def test_reset_programme_action(admin_client, event):
    event.programme_items.all().delete()
    event.programme_items.create(order=1, title_fr="Personnalisé")
    response = admin_client.post(
        reverse("admin:forum_forumevent_changelist"),
        {"action": "reset_programme", "_selected_action": [event.pk]},
        follow=True,
    )
    assert response.status_code == 200
    titles = list(event.programme_items.order_by("order").values_list("title_fr", flat=True))
    assert titles[0] == "Accueil et enregistrement" and len(titles) == 8
    assert AuditEvent.objects.filter(action="forum.programme.reset").exists()


def test_registration_changelist_filters_and_search(admin_client, event):
    _registration(event)
    url = reverse("admin:forum_forumregistration_changelist")
    response = admin_client.get(url, {"status": "pending", "category": "company", "q": "Amina"})
    assert response.status_code == 200
    assert "Amina" in response.content.decode()


def test_registration_add_is_disabled(admin_client, event):
    response = admin_client.get(reverse("admin:forum_forumregistration_add"))
    assert response.status_code == 403


def test_csv_export_action(admin_client, event):
    reg = _registration(event)
    response = admin_client.post(
        reverse("admin:forum_forumregistration_changelist"),
        {"action": "export_csv", "_selected_action": [reg.pk]},
    )
    assert response.status_code == 200
    assert response["Content-Type"].startswith("text/csv")
    assert response.content.startswith(b"\xef\xbb\xbf")
    body = response.content.decode("utf-8-sig")
    assert "consent_text_version" in body and "p2.forum.registration.consent@v1" in body
    assert "2026-09-21T09:30:00+00:00" in body
    assert AuditEvent.objects.filter(action="forum.registration.export").exists()


@pytest.mark.parametrize(
    "action, status",
    [("mark_confirmed", RegistrationStatus.CONFIRMED), ("mark_attended", RegistrationStatus.ATTENDED)],
)
def test_status_actions(admin_client, event, action, status):
    reg = _registration(event)
    admin_client.post(
        reverse("admin:forum_forumregistration_changelist"),
        {"action": action, "_selected_action": [reg.pk]},
        follow=True,
    )
    reg.refresh_from_db()
    assert reg.status == status


def test_anonymise_action(admin_client, event):
    reg = _registration(event, phone="0000")
    admin_client.post(
        reverse("admin:forum_forumregistration_changelist"),
        {"action": "anonymise", "_selected_action": [reg.pk]},
        follow=True,
    )
    reg.refresh_from_db()
    assert reg.is_anonymised and reg.phone == "" and "example.invalid" in reg.email
    assert AuditEvent.objects.filter(action="forum.registration.anonymised").exists()


def test_speaker_admin_shows_warning(admin_client, event):
    role = SpeakerRole.objects.filter(event=event).first()
    response = admin_client.get(reverse("admin:forum_speakerrole_change", args=[role.pk]))
    assert response.status_code == 200
    html = response.content.decode()
    assert "aucun nom de personnalité institutionnelle" in html.lower()
    assert str(SPEAKER_WARNING)[:40] in html


def test_speaker_admin_refuses_authorisation_without_reference(admin_client, event):
    role = SpeakerRole.objects.filter(event=event).first()
    response = admin_client.post(
        reverse("admin:forum_speakerrole_change", args=[role.pk]),
        {
            "event": event.pk,
            "order": role.order,
            "role_label_fr": role.role_label_fr,
            "organisation": "",
            "is_visible": "on",
            "person_name": "Nom Test",
            "names_authorized": "on",
            "authorization_reference": "",
        },
    )
    assert response.status_code == 200  # re-rendered with errors
    role.refresh_from_db()
    assert role.names_authorized is False


def test_other_admin_pages_render(admin_client, event):
    for model in (
        "forummedia",
        "forumdocument",
        "forumintervention",
        "forumagreement",
        "forumoutcome",
        "forumnextevent",
        "forumpartner",
    ):
        assert admin_client.get(reverse(f"admin:forum_{model}_changelist")).status_code == 200
        assert admin_client.get(reverse(f"admin:forum_{model}_add")).status_code == 200


def test_staff_role_has_forum_permissions_but_limited(client, staff_user, event, seeded):
    client.force_login(staff_user)
    assert client.get(reverse("admin:forum_forumregistration_changelist")).status_code == 200
    reg = _registration(event)
    response = client.post(reverse("admin:forum_forumregistration_delete", args=[reg.pk]), {"post": "yes"})
    assert response.status_code == 403


def test_registration_policy_deny_by_default(event, person_user, staff_user, user_factory):
    from accounts.permissions import can

    reg = _registration(event, email="other@example.test")
    assert can(person_user, "view", reg) is False
    assert can(staff_user, "view", reg) is True
    assert can(staff_user, "delete", reg) is False
    owner = user_factory("other@example.test")
    assert can(owner, "view", reg) is True
    assert can(owner, "change", reg) is False
