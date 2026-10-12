"""
Every status this platform can produce has a register, and every register is one of six.

apps/core/chips.py maps enum MEMBERS to the six registers of the status chip. The mapping is a
table typed by hand from the specification, against enums that live in six apps and change on
their own schedule. Two things can go wrong silently: a member is added to an enum and the chip
for it is painted «unmapped» (dotted, void grey) on a page nobody looks at; or a member is renamed
and its row in the table keeps a name that no code produces. These tests import the real enums
and check the table against them in both directions.

The third test is the legal one. `conforme` must take the chapter's ink — no chroma — because no
colour on this platform ever means approved (static/css/tokens.css §STATE). That is enforced in
CSS, and this test pins the side of it that lives in Python: the kinds that used to be «success»
resolve to `conforme`, never to a register of their own.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "apps"))

from core import chips  # noqa: E402

#: producer key in chips.REGISTER → the real enum, imported lazily because Django must be set up.
PRODUCERS = {
    "cases.CaseStatus": ("cases.models", "CaseStatus"),
    "cases.ChecklistStatus": ("cases.models", "ChecklistStatus"),
    "documents.RequirementState": ("documents.models", "RequirementState"),
    "documents.ScanStatus": ("documents.models", "ScanStatus"),
    "companies.NeedStatus": ("companies.models", "NeedStatus"),
    "accounts.VerificationStatus": ("accounts.models", "VerificationStatus"),
    "helpdesk.TicketStatus": ("helpdesk.models", "TicketStatus"),
    "forum.ProposalStatus": ("forum.governance", "ProposalStatus"),
    "forum.ProjectStatus": ("forum.governance", "ProjectStatus"),
    "forum.MilestoneStatus": ("forum.governance", "MilestoneStatus"),
    "forum.CommissionStatus": ("forum.governance", "CommissionStatus"),
    "forum.TableStatus": ("forum.governance", "TableStatus"),
    "forum.EditionStatus": ("forum.governance", "EditionStatus"),
    "academy.EnrolmentStatus": ("academy.models", "EnrolmentStatus"),
    "selection.EvidenceStatus": ("selection.models", "EvidenceStatus"),
    "selection.SelectionStage": ("selection.models", "SelectionStage"),
    "community.InitiativeStatus": ("community.models", "InitiativeStatus"),
}

#: The three selection producers return words from status_word(); their vocabulary is read from
#: the source rather than from an enum, so a new return value is caught too.
SELECTION_WORDS = {
    "selection.actor": {"valid", "suspended", "expired", "withdrawn"},
    "selection.mandate": {"valid", "expired", "withdrawn"},
    "selection.consent": {"valid", "missing", "expired", "invalid"},
    # academy.CompetenceGap.gap_key — three words, read from the property's three returns
    "academy.gap": {"covered", "partial", "missing"},
}


def _enum(module: str, name: str):
    import importlib

    return getattr(importlib.import_module(module), name)


@pytest.mark.parametrize("producer", sorted(PRODUCERS))
def test_every_member_of_every_enum_has_a_register(producer):
    module, name = PRODUCERS[producer]
    members = {str(member.value) for member in _enum(module, name)}
    table = chips.REGISTER[producer]
    missing = sorted(members - set(table))
    assert not missing, f"{producer}: members with no register (they would render unmapped): {missing}"
    stale = sorted(set(table) - members)
    assert not stale, f"{producer}: rows for members the enum no longer has: {stale}"


@pytest.mark.parametrize("producer", sorted(SELECTION_WORDS))
def test_the_selection_vocabulary_is_covered(producer):
    assert set(chips.REGISTER[producer]) == SELECTION_WORDS[producer]


def test_every_register_in_the_table_is_one_of_six():
    for producer, table in chips.REGISTER.items():
        for member, register in table.items():
            assert register in chips.REGISTERS, f"{producer}.{member} → {register!r}"
    assert set(chips.KIND_REGISTER.values()) <= set(chips.REGISTERS)


def test_every_case_status_has_a_stage():
    members = {str(member.value) for member in _enum("cases.models", "CaseStatus")}
    assert set(chips.STAGE) == members
    assert set(chips.STAGE.values()) == {1, 2, 3}


def test_no_register_means_approved():
    """
    «success» becomes `conforme`, whose mark is the chapter's ink; there is no seventh register
    for approval and no green in the vocabulary. CLOSED, on every producer that has it, is a fact
    (neutro or nullo), never conforme: a file can close without success.
    """
    assert chips.register_for_kind("success") == "conforme"
    assert "verde" not in chips.REGISTERS and "approvato" not in chips.REGISTERS
    for producer, table in chips.REGISTER.items():
        if "closed" in table:
            assert table["closed"] in {"neutro", "nullo"}, f"{producer}.closed → {table['closed']}"


def test_unknown_values_get_no_register():
    assert chips.register_for("cases.CaseStatus", "no-such-status") == ""
    assert chips.register_for("no.such.Producer", "draft") == ""
    assert chips.register_for("cases.CaseStatus", None) == ""
    assert chips.register_for_kind("") == "neutro"
    assert chips.register_for_kind(None) == "neutro"


def test_enum_members_are_accepted_as_well_as_their_values():
    status = _enum("cases.models", "CaseStatus")
    assert chips.register_for("cases.CaseStatus", status.REVIEW_REQUIRED) == "azione"
    assert chips.register_for("cases.CaseStatus", "review_required") == "azione"
    assert chips.stage_for(status.ENTERED) == 3
