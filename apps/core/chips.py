"""
The REGISTER of a status chip — derived from the enum member, never from the word.

Why a module, and why here
--------------------------
Every status this platform shows is already produced by Python: an enum member, or a
``status_word()`` that returns one of a handful of strings. Those producers then map the member to
a CSS word — ``missing``, ``filed``, ``review``, ``valid``, ``invalid``, ``expired``, ``replace``,
``done`` — through dictionaries that live next to each enum (``documents.requirements.STATE_CSS``,
``companies.models.STATE_MODIFIERS``, ``helpdesk.models.STATE_TONE``, the six
``forum.governance.*_STATE_CLASSES``). Eleven words cover fifty-three members, so a word cannot
carry a meaning: ``expired`` is «a piece that must be filed again» for a document requirement
and «an archived edition that carries nothing» for the forum. docs/design-v3/specs/badges.md §4.3
(defect E14) is the full account.

So the visual REGISTER — what the chip *asserts* — is looked up per producer and per member,
here, and reaches the DOM as ``data-register``. The words of those dictionaries mean nothing to the
stylesheet any more, and the chip no longer writes them.

The eight registers of design V5 (docs/design-v5/V5_4_EXECUTION_PLAN.md §1.2; DESIGN_SYSTEM_V5.md
§3.2): what each one asserts, its material and its mark — «i cerchi», outline = open, filled =
settled (apps/core/icons.py ``STATUS``).

  conforme  the piece received is the piece asked; a step is done    ink         a plain disc, no glyph
  esame     in the hands of an intervener: it moves without you      lapis       a half-filled disc
  neutro    a fact is recorded; nobody must act, nobody judges       slate       a ring and its centre
  attesa    something is due, from someone, and is not late          amber       a dashed ring
  azione    the file does not advance until a named actor acts, NOW  terracotta  a disc and clock hands
  rifiuto   an act was refused, or the piece is invalid              garnet      a disc struck by a cross
  blocco    a dependency: heavy and calm, never an alarm             graphite    the lock
  nullo     withdrawn, not applicable, archived: it carries nothing  ash         a slashed dotted ring

None of them is «approved». ``conforme`` takes the ink, without chroma, and its mark is a plain
filled disc: this platform approves nothing (O14; DESIGN_SYSTEM_2026 §4.3), so a step done is a
fact about the file, never a verdict — no colour says so and no check mark does, anywhere
(tests/frontend/test_o14_lint.py).

Two of the eight are new in V5, and one rule moves the members onto them: every ``in_review``,
``under_review``, ``assigned`` and ``in_progress`` is ``esame`` — somebody other than the reader has
it in hand — and so are a scan and a verification that are ``pending``; every ``blocked`` is
``blocco`` (tests/frontend/test_chips_registry.py holds the rule). «En examen» therefore reads in
lapis.

A value this module does not know gets NO register: ``register_for`` returns ``""``; the chip is
then written without the attribute, drawn on the neutral tone with a dotted edge — visible — and
the tag logs it (apps/core/templatetags/ile_core.py, ``chip``).
"""

from __future__ import annotations

from core import icons

#: The eight registers, in the order of the plan's table (§1.2).
REGISTERS: tuple[str, ...] = ("conforme", "esame", "neutro", "attesa", "azione", "rifiuto", "blocco", "nullo")

#: Producer → member value → register. Keys are the enum's dotted name as a template says it:
#: ``{% chip case.status "cases.CaseStatus" %}``.
REGISTER: dict[str, dict[str, str]] = {
    "cases.CaseStatus": {
        "draft": "attesa",
        "oriented": "neutro",
        "review_required": "azione",
        "training": "neutro",
        "selection": "neutro",
        "admin_process": "neutro",
        "pre_departure": "neutro",
        "entered": "neutro",
        "post_entry": "neutro",
        # CLOS is a fact about the file, and a file can close without success: never a verdict.
        "closed": "neutro",
        # Case.clean() requires a written suspension_reason: somebody must act.
        "suspended": "azione",
    },
    "cases.ChecklistStatus": {
        "pending": "attesa",
        "in_progress": "esame",
        "done": "conforme",
        "not_applicable": "nullo",
        "blocked": "blocco",  # a dependency, not a refusal
    },
    "documents.RequirementState": {
        "missing": "attesa",
        "filed": "neutro",
        "in_review": "esame",  # «En examen»: an intervener of the file is reading the piece
        "valid": "conforme",
        "invalid": "rifiuto",
        "expired": "azione",  # an expired piece must be filed again
        "to_replace": "attesa",  # asked for, not yet late
    },
    "documents.ScanStatus": {
        "not_configured": "nullo",  # no scanner is deployed: nothing was analysed, nothing is coming
        "pending": "esame",  # the scanner has the file
        "clean": "neutro",  # an antivirus issues no conformity
        "infected": "rifiuto",
        "error": "azione",
    },
    "companies.NeedStatus": {
        "draft": "attesa",
        "submitted": "neutro",
        "under_review": "esame",
        "in_progress": "esame",
        "on_hold": "attesa",
        "closed": "neutro",
        "withdrawn": "nullo",
    },
    "accounts.VerificationStatus": {
        # The project's own «Vérifiée»: a fact the team checked about the legal entity — ink, the plain
        # disc. Never the seal, which is an authority's act (O18; icons.STATUS["seal"]).
        "approved": "conforme",
        "pending": "esame",  # a member of the team is checking the declared elements
        "rejected": "rifiuto",
        "not_required": "nullo",
    },
    "helpdesk.TicketStatus": {
        "information_only": "neutro",
        "needs_clarification": "azione",
        "professional_review_required": "azione",  # outcome CR-11 requires an act
        "assigned": "esame",
        "in_review": "esame",
        "response_available": "azione",  # the only transitions left are the person's acts
        "closed": "neutro",
    },
    "forum.ProposalStatus": {
        "draft": "attesa",
        "submitted": "neutro",
        "under_review": "esame",
        "accepted": "conforme",
        "rejected": "rifiuto",
        "withdrawn": "nullo",
    },
    "forum.ProjectStatus": {
        "preparation": "neutro",
        "active": "neutro",
        "suspended": "azione",
        "completed": "conforme",
        "discontinued": "nullo",
    },
    "forum.MilestoneStatus": {
        "pending": "attesa",
        "in_progress": "esame",
        "done": "conforme",
        "blocked": "blocco",
        "not_applicable": "nullo",
    },
    "forum.CommissionStatus": {
        "active": "neutro",
        "dormant": "attesa",
        "closed": "nullo",
    },
    "forum.TableStatus": {
        "open": "neutro",
        "consolidating": "neutro",
        "closed": "nullo",
    },
    "forum.EditionStatus": {
        "planned": "neutro",
        "open": "neutro",
        "closed": "neutro",  # a closed edition feeds the next one with its report: not void
        "archived": "nullo",
    },
    # The three selection status_word() producers return words, not members; each has its own
    # meaning for the same word, which is exactly why the lookup is per producer.
    "selection.actor": {
        "valid": "conforme",
        "suspended": "azione",
        "expired": "azione",  # a new authorisation is needed
        "withdrawn": "nullo",
    },
    "selection.mandate": {
        "valid": "conforme",
        "expired": "nullo",
        "withdrawn": "nullo",
    },
    "selection.consent": {
        "valid": "conforme",
        "missing": "attesa",
        "expired": "nullo",
        "invalid": "rifiuto",
    },
    # Four producers the specification's table did not list, found by walking the 65 `.state`
    # sites (phase 1b). Same reading as above: a completed enrolment is an attendance fact
    # (academy.EnrolmentStatus docstring: none of the four states is an approval).
    "academy.EnrolmentStatus": {
        "enrolled": "neutro",
        "in_progress": "esame",
        "completed": "conforme",
        "withdrawn": "nullo",
    },
    # CompetenceGap.gap_key: covered = the level asked is the level held; partial = something
    # is due; missing = the pathway does not advance until the competence is acquired.
    "academy.gap": {
        "covered": "conforme",
        "partial": "attesa",
        "missing": "azione",
    },
    "selection.EvidenceStatus": {
        "requested": "attesa",
        "provided": "conforme",
        "not_applicable": "nullo",
        "blocked": "blocco",  # a dependency, not a refusal — the spec's own reading of «bloqué»
    },
    "community.InitiativeStatus": {
        "proposed": "attesa",  # proposed, awaiting the room's take-up
        "active": "neutro",
        "closed": "neutro",
    },
    # The stages of a selection process are positions, like the stages of a case file: a stage named
    # «… review» is where the process stands, not a piece in somebody's hands.
    "selection.SelectionStage": {
        "mandate_confirmed": "neutro",
        "competence_review": "neutro",
        "evidence_review": "neutro",
        "company_review": "neutro",
        "concluded": "neutro",  # closed is a fact, never a verdict
        "suspended": "azione",  # a written suspension_reason is required: somebody must act
    },
}

#: The one rule of V5, whatever the producer: a member with one of these names is in somebody's
#: hands — esame — and a blocked one is a dependency — blocco. A verification and a scan that are
#: «pending» are esame by their own rows: elsewhere «pending» is a thing due (attesa).
ESAME_MEMBERS: frozenset[str] = frozenset({"in_review", "under_review", "assigned", "in_progress"})
BLOCCO_MEMBERS: frozenset[str] = frozenset({"blocked"})

#: The phase of the case-file gauge (spec §4.4): before the pathway · under way · entered and after.
STAGE: dict[str, int] = {
    "draft": 1,
    "oriented": 1,
    "review_required": 1,
    "suspended": 1,
    "training": 2,
    "selection": 2,
    "admin_process": 2,
    "pre_departure": 2,
    "entered": 3,
    "post_entry": 3,
    "closed": 3,
}
#: The one producer whose chip carries the gauge: three notches after the word.
STAGE_PRODUCER = "cases.CaseStatus"

#: A member that keeps its register and has a mark of its own (ICON_SEMANTIC_MAP §2): «À remplacer»
#: is due like «Manquant» — one register, one amber, one dashed edge — and the ring with two arrows
#: against the dashed ring is what tells them apart at 16 px.
MEMBER_MARK: dict[tuple[str, str], str] = {
    ("documents.RequirementState", "to_replace"): "st-attesa-replace",
}

#: The legacy ``kind`` of templates/components/badge.html, translated once for all its includes. V5
#: reads two of them as the notices of the same name do (static/css/v5/notice.css): «warning» is
#: amber — due, or needing attention, not late — and «pending» is lapis — in somebody's hands. The
#: two deadline kinds are plan §1.2's: «soon» is attesa, «overdue» is azione; red never means lateness.
KIND_REGISTER: dict[str, str] = {
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


def _key(value: object) -> str:
    key = getattr(value, "value", value)
    return str(key) if key is not None else ""


def register_for(producer: str, value: object) -> str:
    """The register of ``value`` as produced by ``producer``, or ``""`` when unknown."""
    return REGISTER.get(producer, {}).get(_key(value), "")


def stage_for(value: object) -> int | None:
    key = getattr(value, "value", value)
    return STAGE.get(str(key)) if key is not None else None


def register_for_kind(kind: object) -> str:
    return KIND_REGISTER.get(str(kind or "neutral"), "")


def mark_for(register: str, producer: str = "", value: object = None) -> str:
    """
    The sprite symbol a chip draws: its register's mark from the icon registry («i cerchi»), or the
    member's own where it has one. A chip is never drawn without a mark — an unknown register draws
    the neutral one — and no register's mark is a check (O14).
    """
    own = MEMBER_MARK.get((producer, _key(value))) if producer else None
    return own or icons.STATUS.get(register) or icons.STATUS["neutro"]
