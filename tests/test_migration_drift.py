"""
`makemigrations --check` over every app of the project, not one.

`apps/portal/tests/test_compliance.py` already ran this check — for `portal` alone. A label of
`selection.SelectionOutcome` was reworded (a prescribed text had been retyped into a choice) and the
migration was never regenerated: nothing failed, because `choices` never reach the SQL schema. The
drift surfaced only when `makemigrations --check` was run by hand over the whole project.

A model state that no migration describes is a deployment blocker even when the column is unchanged:
the next person to touch that model gets someone else's edit folded into their own migration.
"""

from __future__ import annotations

from io import StringIO

import pytest
from django.core.management import call_command

from config.settings.base import LOCAL_APPS


def _app_label(dotted: str) -> str:
    return dotted.rsplit(".", 1)[-1]


APP_LABELS = sorted(_app_label(app) for app in LOCAL_APPS)


def test_every_local_app_is_covered_by_this_check():
    """Guard the guard: a new app must not be able to join the project unwatched."""
    assert len(APP_LABELS) == len(set(APP_LABELS)), "two apps share a label"
    assert "selection" in APP_LABELS
    assert "portal" in APP_LABELS


@pytest.mark.django_db
def test_no_app_has_unmigrated_model_changes():
    out = StringIO()
    try:
        call_command("makemigrations", *APP_LABELS, "--check", "--dry-run", stdout=out, stderr=out)
    except SystemExit:  # `--check` exits 1 rather than raising something describable
        pytest.fail(
            "Model changes are not described by any migration. Run `manage.py makemigrations`:\n"
            + out.getvalue()
        )
