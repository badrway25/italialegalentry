"""Publication gates behave as real feature gates, not notes (G1, G2, G3, G4)."""

import datetime as dt

import pytest
from freezegun import freeze_time

from core import flags, gates

pytestmark = [pytest.mark.compliance, pytest.mark.django_db]


def test_forms_closed_while_legal_pages_blocked(seeded):
    assert gates.legal_pages_available() is False
    status = gates.public_forms_enabled()
    assert status.open is False


def test_forms_open_once_legal_pages_published(seeded, legal_published):
    assert gates.legal_pages_available() is True
    assert gates.public_forms_enabled().open is True


def test_forms_override_flag_is_explicit_and_audited(seeded, set_flag, superuser):
    from django.contrib.admin.sites import AdminSite
    from django.test import RequestFactory

    from audit.models import AuditEvent
    from core.admin import FeatureFlagAdmin
    from core.models import FeatureFlag

    row = set_flag("forms_override_without_legal", True)
    request = RequestFactory().post("/backoffice/")
    request.user = superuser
    FeatureFlagAdmin(FeatureFlag, AdminSite()).save_model(request, row, None, True)
    assert gates.public_forms_enabled().open is True
    assert AuditEvent.objects.filter(action="feature_flag.changed").exists()


def test_signup_is_closed_while_forms_gated(client, seeded):
    r = client.get("/fr/compte/signup/")
    assert r.status_code == 200
    assert "Inscriptions ferm" in r.content.decode()


def test_phase3_requires_flag_and_date(seeded, set_flag):
    set_flag("phase3_public", True, enabled_from=dt.datetime(2026, 10, 2, tzinfo=dt.UTC))
    with freeze_time("2026-09-25 12:00:00"):
        flags.invalidate()
        assert gates.phase3_public() is False
    with freeze_time("2026-10-02 12:00:00"):
        flags.invalidate()
        assert gates.phase3_public() is True
    set_flag("phase3_public", False, enabled_from=dt.datetime(2026, 10, 2, tzinfo=dt.UTC))
    with freeze_time("2026-10-10 12:00:00"):
        flags.invalidate()
        assert gates.phase3_public() is False, "date alone must not publish Phase 3 without authorisation"


def test_default_flags_without_db_rows():
    """Defaults from settings apply when no row exists (fresh deploy)."""
    with freeze_time("2026-09-20 12:00:00"):
        flags.invalidate()
        assert flags.is_enabled("forum_banner") is True
        assert flags.is_enabled("phase3_public") is False
        assert flags.is_enabled("virtual_forum") is False
    with freeze_time("2026-10-03 12:00:00"):
        flags.invalidate()
        assert flags.is_enabled("forum_banner") is False, "banner expires on 2 Oct 2026"
