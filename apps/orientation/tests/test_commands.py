"""Management commands: validate, export, import, activate, purge."""

import io
import json

import pytest
from django.core.management import CommandError, call_command
from freezegun import freeze_time

from orientation import services
from orientation.models import OrientationSession, Ruleset, RulesetStatus

pytestmark = pytest.mark.django_db


def test_validate_ruleset_ok_and_errors(active_ruleset):
    out = io.StringIO()
    call_command("validate_ruleset", stdout=out)
    assert "OK" in out.getvalue() and "Ruleset v1 [active]" in out.getvalue()
    Ruleset.objects.create(version=2)
    with pytest.raises(CommandError):
        call_command("validate_ruleset", ruleset=2, stdout=io.StringIO())
    with pytest.raises(CommandError):
        call_command("validate_ruleset", ruleset=42, stdout=io.StringIO())


def test_validate_ruleset_strict_treats_warnings_as_errors(active_ruleset):
    from orientation.models import Outcome

    Outcome.objects.create(
        ruleset=active_ruleset, key="orphan", pathway_key="scientific_research", title_fr="x", explanation_fr="x"
    )
    call_command("validate_ruleset", stdout=io.StringIO())
    with pytest.raises(CommandError):
        call_command("validate_ruleset", strict=True, stdout=io.StringIO())


def test_export_import_round_trip(active_ruleset, tmp_path):
    out = io.StringIO()
    call_command("export_ruleset", ruleset=1, stdout=out)
    data = json.loads(out.getvalue())
    assert data["version"] == 1 and len(data["rules"]) == 15
    path = tmp_path / "ruleset.json"
    call_command("export_ruleset", output=str(path), stdout=io.StringIO())
    assert json.loads(path.read_text(encoding="utf-8")) == data
    out = io.StringIO()
    call_command("import_ruleset", str(path), notes="reimport", stdout=out)
    assert "v2 imported as draft" in out.getvalue()
    v2 = Ruleset.objects.get(version=2)
    assert v2.status == RulesetStatus.DRAFT and v2.notes == "reimport"
    exported_v2 = services.export_ruleset(v2)
    for section in ("questions", "outcomes", "rules"):
        assert exported_v2[section] == data[section]
    with pytest.raises(CommandError):
        call_command("import_ruleset", str(path), ruleset=1, stdout=io.StringIO())


def test_import_refuses_invalid_document(active_ruleset, tmp_path):
    path = tmp_path / "bad.json"
    path.write_text(json.dumps({"questions": [], "outcomes": [], "rules": []}), encoding="utf-8")
    with pytest.raises(CommandError):
        call_command("import_ruleset", str(path), stdout=io.StringIO())
    assert Ruleset.objects.count() == 1
    path.write_text("{not json", encoding="utf-8")
    with pytest.raises(CommandError):
        call_command("import_ruleset", str(path), stdout=io.StringIO())
    with pytest.raises(CommandError):
        call_command("import_ruleset", str(tmp_path / "missing.json"), stdout=io.StringIO())


def test_import_with_activate(active_ruleset, tmp_path):
    path = tmp_path / "ruleset.json"
    call_command("export_ruleset", output=str(path), stdout=io.StringIO())
    call_command("import_ruleset", str(path), activate=True, stdout=io.StringIO())
    assert services.active_ruleset().version == 2
    active_ruleset.refresh_from_db()
    assert active_ruleset.status == RulesetStatus.RETIRED


def test_activate_ruleset_command(active_ruleset):
    v2 = services.import_ruleset(services.export_ruleset(active_ruleset), version=2)
    call_command("activate_ruleset", ruleset=2, stdout=io.StringIO())
    assert services.active_ruleset() == v2
    Ruleset.objects.create(version=3)
    with pytest.raises(CommandError):
        call_command("activate_ruleset", ruleset=3, stdout=io.StringIO())
    with pytest.raises(CommandError):
        call_command("activate_ruleset", ruleset=99, stdout=io.StringIO())
    assert services.active_ruleset() == v2


def test_purge_command(active_ruleset):
    from django.contrib.auth.models import AnonymousUser
    from django.test import RequestFactory

    request = RequestFactory().get("/")
    request.user = AnonymousUser()
    with freeze_time("2026-08-01 10:00:00"):
        services.start_session(request)
    with freeze_time("2026-10-01 10:00:00"):
        out = io.StringIO()
        call_command("purge_orientation_sessions", dry_run=True, stdout=out)
        assert "[dry-run] deleted=1 anonymised=0" in out.getvalue()
        assert OrientationSession.objects.count() == 1
        out = io.StringIO()
        call_command("purge_orientation_sessions", stdout=out)
        assert "deleted=1 anonymised=0" in out.getvalue()
        assert OrientationSession.objects.count() == 0
