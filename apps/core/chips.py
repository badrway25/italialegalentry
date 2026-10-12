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
here, and reaches the DOM as ``data-register``. The class words stay where they are and simply
stop meaning anything to the stylesheet.

The six registers, and what each one asserts:

  neutro    a fact is recorded; nobody must act, nobody judges          (the base line)
  attesa    something is due, from someone, and is not late             (dashed rule)
  azione    the file does not advance until a named actor acts, NOW     (4px rule)
  conforme  the piece received is the piece asked; a step is done       (closing rule below)
  rifiuto   an act was refused, or the piece is invalid                 (struck through)
  nullo     withdrawn, not applicable, archived: it carries nothing     (1px, greyed word)

None of them is «approved». ``conforme`` takes the chapter's ink, without chroma, because this
platform approves nothing (static/css/tokens.css §STATE; DESIGN_SYSTEM_2026 §4.3): a step done is
a fact about the file, never a verdict, and the chip says so with a closing rule and a check, not
with a colour.

A value this module does not know gets NO register: ``register_for`` returns ``""``, the template
writes the attribute only when it is non-empty, and the stylesheet paints an unmapped chip with a
dotted rule — visible, and tested.
"""

from __future__ import annotations

REGISTERS: tuple[str, ...] = ("neutro", "attesa", "azione", "conforme", "rifiuto", "nullo")

#: Producer → member value → register. Keys are the enum's dotted name as a template would say it,
#: so that a template can ask for ``value|chip_register:"cases.CaseStatus"`` without importing.
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
        "in_progress": "neutro",
        "done": "conforme",
        "not_applicable": "nullo",
        "blocked": "attesa",  # a dependency, not a refusal
    },
    "documents.RequirementState": {
        "missing": "attesa",
        "filed": "neutro",
        "in_review": "neutro",
        "valid": "conforme",
        "invalid": "rifiuto",
        "expired": "azione",  # an expired piece must be filed again
        "to_replace": "attesa",  # asked for, not yet late
    },
    "documents.ScanStatus": {
        "not_configured": "neutro",
        "pending": "attesa",
        "clean": "neutro",  # an antivirus issues no conformity
        "infected": "rifiuto",
        "error": "azione",
    },
    "companies.NeedStatus": {
        "draft": "attesa",
        "submitted": "neutro",
        "under_review": "neutro",
        "in_progress": "neutro",
        "on_hold": "attesa",
        "closed": "neutro",
        "withdrawn": "nullo",
    },
    "accounts.VerificationStatus": {
        "approved": "conforme",  # the one place a seal is born (chip--seal, phase 2)
        "pending": "attesa",
        "rejected": "rifiuto",
        "not_required": "neutro",
    },
    "helpdesk.TicketStatus": {
        "information_only": "neutro",
        "needs_clarification": "azione",
        "professional_review_required": "azione",  # outcome CR-11 requires an act
        "assigned": "neutro",
        "in_review": "neutro",
        "response_available": "azione",  # the only transitions left are the person's acts
        "closed": "neutro",
    },
    "forum.ProposalStatus": {
        "draft": "attesa",
        "submitted": "neutro",
        "under_review": "neutro",
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
        "in_progress": "neutro",
        "done": "conforme",
        "blocked": "attesa",
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
        "in_progress": "neutro",
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
        "blocked": "attesa",  # a dependency, not a refusal — the spec's own reading of «bloqué»
    },
    "community.InitiativeStatus": {
        "proposed": "attesa",  # proposed, awaiting the room's take-up
        "active": "neutro",
        "closed": "neutro",
    },
    "selection.SelectionStage": {
        "mandate_confirmed": "neutro",
        "competence_review": "neutro",
        "evidence_review": "neutro",
        "company_review": "neutro",
        "concluded": "neutro",  # closed is a fact, never a verdict
        "suspended": "azione",  # a written suspension_reason is required: somebody must act
    },
}

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

#: Register → sprite glyph (static/img/icons.svg). «neutro» has none on purpose: a recorded fact
#: is the base line, and a dot on it would be the anti-pattern the spec rejects.
GLYPH: dict[str, str] = {
    "attesa": "clock",
    "azione": "warning",
    "conforme": "check",
    "rifiuto": "close",
    "nullo": "minus",
}

#: The legacy ``kind`` of templates/components/badge.html, translated once for all its includes.
KIND_REGISTER: dict[str, str] = {
    "neutral": "neutro",
    "info": "neutro",
    "primary": "neutro",
    "success": "conforme",
    "warning": "azione",
    "error": "rifiuto",
    "pending": "attesa",
}


def register_for(producer: str, value: object) -> str:
    """The register of ``value`` as produced by ``producer``, or ``""`` when unknown."""
    key = getattr(value, "value", value)
    return REGISTER.get(producer, {}).get(str(key) if key is not None else "", "")


def stage_for(value: object) -> int | None:
    key = getattr(value, "value", value)
    return STAGE.get(str(key)) if key is not None else None


def register_for_kind(kind: object) -> str:
    return KIND_REGISTER.get(str(kind or "neutral"), "")
