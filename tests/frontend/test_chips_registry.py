"""
Every status this platform can produce has a register, and every register is one of eight.

apps/core/chips.py maps enum MEMBERS to the eight registers of the status chip (design V5, V5.4 plan §1.2). The
mapping is a table typed by hand from the specification, against enums that live in six apps and change on their
own schedule. Two things can go wrong silently: a member is added to an enum and the chip for it is painted
«unmapped» (dotted, neutral) on a page nobody looks at; or a member is renamed and its row in the table keeps a
name that no code produces. These tests import the real enums and check the table against them in both directions.

Three more things are held here, because they live in Python:

* the one rule that moves members onto V5's two new registers — whatever is «in somebody's hands» is `esame`,
  whatever is blocked is `blocco` — so that «En examen» reads in lapis on every producer, not on the ones somebody
  remembered;
* the legal one: `conforme` takes the ink — no chroma — because no colour on this platform ever means approved
  (static/css/v5/tokens.css §3.2), and the kinds that used to be «success» resolve to `conforme`, never to a
  register of their own;
* the marks: every register draws a symbol of the sprite, through the icon registry, and none of them is a check
  (O14; tests/frontend/test_o14_lint.py holds the templates, the sheets and the scripts to the same rule).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "apps"))

from core import chips, icons  # noqa: E402

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


def test_the_registers_are_the_eight_of_the_plan():
    assert chips.REGISTERS == ("conforme", "esame", "neutro", "attesa", "azione", "rifiuto", "blocco", "nullo")
    assert set(chips.REGISTER) == set(PRODUCERS) | set(SELECTION_WORDS), "a producer without its enum in this test"


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


def test_every_register_in_the_table_is_one_of_eight():
    for producer, table in chips.REGISTER.items():
        for member, register in table.items():
            assert register in chips.REGISTERS, f"{producer}.{member} → {register!r}"
    assert set(chips.KIND_REGISTER.values()) <= set(chips.REGISTERS)
    used = {register for table in chips.REGISTER.values() for register in table.values()}
    assert used == set(chips.REGISTERS), f"a register no member produces: {sorted(set(chips.REGISTERS) - used)}"


def test_what_is_in_somebodys_hands_is_esame_and_what_is_blocked_is_blocco():
    """The one rule of V5 (plan §1.2; the council's status table): every `in_review`, `under_review`, `assigned`
    and `in_progress` is esame, every `blocked` is blocco — on every producer, the ones added after today included.
    «En examen» is the document state the owner named: it is the lapis register, and no longer shares DÉPOSÉ's."""
    for producer, table in chips.REGISTER.items():
        for member, register in table.items():
            if member in chips.ESAME_MEMBERS:
                assert register == "esame", f"{producer}.{member} → {register}"
            if member in chips.BLOCCO_MEMBERS:
                assert register == "blocco", f"{producer}.{member} → {register}"
    assert chips.register_for("documents.RequirementState", "in_review") == "esame"
    assert chips.register_for("documents.RequirementState", "filed") == "neutro"
    # a human or a machine at work on a «pending» thing: esame; a «pending» thing that is merely due: attesa
    assert chips.register_for("accounts.VerificationStatus", "pending") == "esame"
    assert chips.register_for("documents.ScanStatus", "pending") == "esame"
    assert chips.register_for("cases.ChecklistStatus", "pending") == "attesa"
    # what carries nothing says so: no scanner deployed, no verification required
    assert chips.register_for("documents.ScanStatus", "not_configured") == "nullo"
    assert chips.register_for("accounts.VerificationStatus", "not_required") == "nullo"


def test_every_case_status_has_a_stage():
    members = {str(member.value) for member in _enum("cases.models", "CaseStatus")}
    assert set(chips.STAGE) == members
    assert set(chips.STAGE.values()) == {1, 2, 3}
    assert chips.STAGE_PRODUCER in chips.REGISTER, "the gauge belongs to a producer of the table"


def test_no_register_means_approved():
    """
    «success» becomes `conforme`, whose mark is the ink; there is no ninth register for approval and no
    green in the vocabulary. CLOSED, on every producer that has it, is a fact (neutro or nullo), never
    conforme: a file can close without success.
    """
    assert chips.register_for_kind("success") == "conforme"
    assert "verde" not in chips.REGISTERS and "approvato" not in chips.REGISTERS
    for producer, table in chips.REGISTER.items():
        if "closed" in table:
            assert table["closed"] in {"neutro", "nullo"}, f"{producer}.closed → {table['closed']}"


def test_the_kinds_read_as_the_notices_of_the_same_name_do():
    """components/badge.html's `kind`: «warning» is amber — due, never late — and «pending» is lapis, like the
    notices (static/css/v5/notice.css); the two deadline kinds are plan §1.2's: soon = attesa, overdue = azione —
    red never means lateness."""
    assert chips.KIND_REGISTER == {
        "neutral": "neutro",
        "info": "neutro",
        "primary": "neutro",
        "success": "conforme",
        "warning": "attesa",
        "error": "rifiuto",
        "pending": "esame",
        "soon": "attesa",
        "overdue": "azione",
    }
    assert chips.register_for_kind("overdue") != "rifiuto"


def test_unknown_values_get_no_register():
    assert chips.register_for("cases.CaseStatus", "no-such-status") == ""
    assert chips.register_for("no.such.Producer", "draft") == ""
    assert chips.register_for("cases.CaseStatus", None) == ""
    assert chips.register_for_kind("") == "neutro"
    assert chips.register_for_kind(None) == "neutro"
    assert chips.register_for_kind("no-such-kind") == ""


def test_enum_members_are_accepted_as_well_as_their_values():
    status = _enum("cases.models", "CaseStatus")
    assert chips.register_for("cases.CaseStatus", status.REVIEW_REQUIRED) == "azione"
    assert chips.register_for("cases.CaseStatus", "review_required") == "azione"
    assert chips.stage_for(status.ENTERED) == 3
    state = _enum("documents.models", "RequirementState")
    assert chips.mark_for("attesa", "documents.RequirementState", state.TO_REPLACE) == "st-attesa-replace"


def test_every_register_draws_a_mark_of_the_sprite_and_none_is_a_check():
    """«i cerchi» (ICON_SEMANTIC_MAP §2): the mark is the register's, from the icon registry — never chosen by a
    template — and a chip is never drawn without one. `conforme` is a plain disc: the four check-bearing symbols
    of the sprite (icons.CHECK_BEARING) are nobody's status mark (O14)."""
    marks = {register: chips.mark_for(register) for register in chips.REGISTERS}
    assert marks == {register: icons.STATUS[register] for register in chips.REGISTERS}
    assert len(set(marks.values())) == len(chips.REGISTERS), "two registers with one mark"
    assert marks["conforme"] == "st-conforme" and marks["blocco"] == "lock"
    for (producer, member), mark in chips.MEMBER_MARK.items():
        assert member in chips.REGISTER[producer], (producer, member)
        marks[f"{producer}.{member}"] = mark
    for owner, mark in marks.items():
        assert mark in icons.SYMBOLS, f"{owner}: {mark!r} is not in the sprite"
        assert mark not in icons.CHECK_BEARING, f"{owner}: {mark} draws a check"
        assert icons.MIN_SIZE[mark] <= 14, f"{owner}: {mark} cannot be drawn in the 20 px chip"
    # an unknown register still draws: the neutral mark, never nothing
    assert chips.mark_for("") == icons.STATUS["neutro"] == chips.mark_for("no-such-register")
    # the same member under another producer keeps its register's mark
    assert chips.mark_for("attesa", "documents.RequirementState", "missing") == "st-attesa"
    assert not hasattr(chips, "GLYPH"), "the V3 table that drew «conforme» with a check is gone"
