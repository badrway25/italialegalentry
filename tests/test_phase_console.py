"""
The phase console must describe the gates that exist, and only those.

The console is documentation rendered at runtime, which is the kind of documentation that rots
silently: a gate added to ``core.gates`` and not described here appears in the snapshot with no
explanation, and a description naming a flag that was renamed sends an administrator to a screen
that does not exist. Neither failure announces itself, so it is asserted instead.
"""

from __future__ import annotations

import pytest
from django.conf import settings

from core import gates
from core.phases import GATES, GATES_BY_KEY, console_rows

pytestmark = pytest.mark.django_db

#: Keys of ``gates.snapshot()`` that are not gates: context the console renders elsewhere.
NON_GATE_KEYS = {"now", "public_forms_reason"}


def test_every_gate_in_the_snapshot_is_described():
    described = set(GATES_BY_KEY)
    live = set(gates.snapshot()) - NON_GATE_KEYS
    assert live <= described, f"undescribed gates: {sorted(live - described)}"


def test_no_description_invents_a_gate():
    live = set(gates.snapshot()) - NON_GATE_KEYS
    assert set(GATES_BY_KEY) <= live, f"described but absent: {sorted(set(GATES_BY_KEY) - live)}"


def test_every_named_flag_exists():
    for gate in GATES:
        if gate.flag:
            assert gate.flag in settings.FEATURE_FLAG_DEFAULTS, f"{gate.key} names a flag that does not exist"


def test_every_dependency_names_a_real_gate():
    for gate in GATES:
        for name in gate.depends_on:
            assert name in GATES_BY_KEY, f"{gate.key} depends on an unknown gate {name}"


def test_every_gate_says_what_it_opens_and_why():
    for gate in GATES:
        assert str(gate.opens).strip(), f"{gate.key} does not say what it opens"
        assert str(gate.reason).strip(), f"{gate.key} does not say why it exists"


def test_the_console_reports_the_live_state():
    rows = {row["key"]: row for row in console_rows()}
    snapshot = gates.snapshot()
    for key, row in rows.items():
        assert row["open"] == snapshot[key]


def test_a_gate_blocked_by_a_dependency_says_so(set_flag, db):
    """An administrator who flips a flag and sees no change must be told why before they flip it."""
    rows = {row["key"]: row for row in console_rows()}
    forms = rows["public_forms_enabled"]
    if forms["open"]:
        pytest.skip("the legal pages are published in this database, so nothing is blocked")
    assert forms["blocked_by"], "a closed dependency must be named"


def test_the_legal_gate_is_not_presented_as_a_switch():
    """It is true when the five legal documents are published — not when somebody decides it is."""
    legal = GATES_BY_KEY["legal_pages_available"]
    assert legal.flag == ""
    assert legal.reversible is False
