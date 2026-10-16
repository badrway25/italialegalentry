"""
What the register shows, assembled once and used by the page, the portal tag and the tests.

Presentation is kept out of the templates because every one of these decisions is a rule, not a
layout choice: which state word appears, which rule sentence goes with it, whether the account is
offered an upload button at all, and whether a link is even generated. A template that computed
those would let a change of markup change an authorisation.

Nothing here runs a query that authorisation has not already narrowed:
``DocumentRequirement.objects.readable_by(user)`` is the entry point, always.

Design V5 (docs/design-v5/V5_4_EXECUTION_PLAN.md §3.5 item 5; W3-C) adds what «Mes pièces» V5.2 draws: the three
groups of the register by whose move it is (``register_groups`` — the strip's runs and the collection's groups are
ONE partition), the page's next piece with its act (``next_piece``, T1's piece when the reader can act on it), the
state filter in the register's own order (``STATE_ORDER``), each row's act and its due word; and F8 — the urgency
ladder stops once a piece is filed: a date is drawn calm when the piece is no longer open.
"""

from __future__ import annotations

from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from accounts.permissions import can
from cases.models import ChecklistStatus, ResponsibleActor
from documents import services
from documents.models import OPEN_STATES, DocumentRequirement, RequirementState
from documents.requirements import (
    ACTOR_GLYPHS,
    STATE_ORDER,
    counts,
    delivery_rule,
    due_urgency,
    health,
    scan_rule,
    sort_key,
    state_css,
    state_label,
    state_reason,
    state_rule,
)

#: A due date's word beside its glyph and its date — never a colour alone (plan §1.2: «soon» is attesa, «overdue»
#: is azione). The catalogue's words of the deadlines page and of the dashboard; nothing new is written here.
DUE_WORDS = {"soon": _("Bientôt"), "overdue": _("En retard")}

#: The register's three groups, by whose move it is — the strip's runs and the collection's groups are the same
#: sets under the same words (DOCUMENT_WORKSPACE §7.2, the dashboard's «il registro», DL54-76). The words are
#: catalogue strings until the copy review signs «À vous · En cours · Réglées» (plan §1.18 D15, B1 item 3).
GROUP_TO_ACT, GROUP_IN_HAND, GROUP_SETTLED = "to-act", "in-hand", "settled"

#: Above this many pieces a run draws its count alone, without one mark per piece (CD §12).
MARKS_UP_TO = 24

#: In the card layout the search field is drawn from this many pieces on (DOCUMENT_WORKSPACE §13, D9): a dozen
#: cards are a few thumb-lengths, and the field cost 56 px of a phone's first screen.
SEARCH_FROM = 13

#: What the register says when nothing at all is required yet. One sentence naming who fills the
#: region and when — never a dashed box with an icon (art direction A §14.4).
EMPTY_REGISTER = _(
    "Aucune pièce ne vous est demandée pour l’instant. Les pièces apparaissent ici lorsque "
    "l’orientation les a identifiées ou lorsqu’un intervenant du dossier les demande."
)


def record_language(lang: str) -> dict[str, str]:
    """The language of a record's own words when it is not the page's: a piece's title is written in French and stays
    French on an Arabic page, isolated so that its direction and its punctuation hold (gate-0 A6; the dashboard's
    rows do the same)."""
    from django.utils import translation

    current = (translation.get_language() or "fr").split("-")[0]
    if not lang or lang == current:
        return {"lang": "", "dir": ""}
    try:
        bidi = translation.get_language_info(lang)["bidi"]
    except KeyError:
        bidi = False
    return {"lang": lang, "dir": "rtl" if bidi else "ltr"}


def present_version(version, *, user, requirement) -> dict:
    """One deposit: its rank, its file, what the scanner said, what a person decided."""
    document = version.document
    readable = document is not None and can(user, "download", document)
    # Two separate questions, asked in order, and the answer to the second is SHOWN.
    #   may this account read this file?      -> the object-level policy (``readable``)
    #   may this file be handed over at all?  -> the scanner gate (``services.delivery_block``)
    # A reviewer on an installation with no antivirus passes the first and fails the second; the
    # row must say so instead of offering a link that answers 403.
    blocked = services.delivery_block(document, user) if readable else ""
    return {
        "version": version,
        "number": version.number,
        "filed_at": version.created_at,
        "filed_by": version.filed_by,
        "is_current": version.is_current,
        "superseded_at": version.superseded_at,
        "expires_on": version.expires_on,
        "decision": version.decision,
        "decision_label": version.get_decision_display(),
        "decision_note": version.decision_note,
        "decided_at": version.decided_at,
        "document": document,
        "file_name": document.original_name if document else "",
        "size": document.size if document else None,
        "sha256_short": (document.sha256[:16] if document else ""),
        "antivirus": services.antivirus_state(document),
        "scan_rule": scan_rule(document.scan_status) if document else "",
        # The link is MINTED here and only when the policy allows it: a template cannot conjure one.
        "download_url": (
            reverse("documents:signed_download", args=[services.signed_download_token(document, user)])
            if readable and not blocked
            else ""
        ),
        "delivery_block": blocked,
        "delivery_rule": delivery_rule(blocked),
        "link_minutes": services.DOWNLOAD_LINK_MINUTES,
        "requirement": requirement,
    }


def present_requirement(requirement, *, user, with_versions: bool = False) -> dict:
    """One row of the register: the piece, its state, who is answerable, what can be done."""
    version = requirement.current_version
    state = requirement.derived_state()
    # One object-level answer per row, read three times below (``can`` costs queries on every call).
    may_file_here = can(user, "file", requirement)
    may_upload = services.user_may_upload(user)
    row = {
        "requirement": requirement,
        "id": str(requirement.pk),
        "title": requirement.title,
        "detail": requirement.detail,
        "code": requirement.code,
        "mandatory": requirement.mandatory,
        "due_date": requirement.due_date,
        "is_overdue": requirement.is_overdue,
        "state": state,
        "is_open": state in OPEN_STATES,
        "state_label": state_label(state),
        "state_css": state_css(state),
        "state_rule": state_rule(state),
        "state_reason": state_reason(requirement, version, state),
        "responsible": requirement.get_responsible_actor_display(),
        "responsible_actor": requirement.responsible_actor,
        "responsible_note": requirement.responsible_note,
        "responsible_glyph": ACTOR_GLYPHS.get(requirement.responsible_actor, ""),
        # F8 (DOCUMENT_WORKSPACE §9.1 item 2): the urgency ladder runs only while the piece is OPEN. Once it is filed,
        # in review or valid, the clock is no longer the person's — a filed piece due tomorrow is drawn calm.
        "urgency": (due_urgency(requirement.due_date, overdue=requirement.is_overdue) if state in OPEN_STATES else ""),
        "health": health(state, version),
        "is_for_the_person": requirement.responsible_actor == ResponsibleActor.PERSON,
        "source_title": requirement.source_title,
        "source_ref": requirement.source_ref,
        "source_url": requirement.source_url,
        "access_class_label": requirement.get_access_class_display(),
        "current": present_version(version, user=user, requirement=requirement) if version else None,
        # len() over the prefetched cache, not .count(): the register prefetches ``versions`` and a
        # COUNT(*) per row would put one round-trip per line back into a page built to avoid them.
        "version_count": len(requirement.versions.all()),
        # Authorised AND actually able: the Conditions gate is said ON THE ROW it blocks («Bloqué», art direction A
        # §13.3) and in the register's strip, never as a banner above an empty box (design V5, W3-C: no button that
        # promises an acceptance its target cannot make yet — the acceptance flow waits on the legal texts, G1).
        "may_file": may_file_here and may_upload,
        "consent_required": may_file_here and not may_upload,
        "may_review": can(user, "review", requirement) and version is not None,
        # BLOQUÉ belongs where something is actually blocked. A piece that is VALIDE needs nothing
        # from anybody, and a "Bloqué" chip beside "Valide" reads as *your valid passport is
        # blocked* — the exact state confusion this register exists to remove. The consent gate is
        # still stated for every row on the piece's own page and at the foot of the register.
        "action_blocked": may_file_here and not may_upload and state in OPEN_STATES,
        "detail_url": reverse("documents:requirement", args=[requirement.pk]),
        "upload_url": reverse("documents:requirement_file", args=[requirement.pk]),
        "review_url": reverse("documents:requirement_review", args=[requirement.pk]),
        "case": requirement.case,
    }
    row["due_word"] = DUE_WORDS.get(row["urgency"], "")
    row["act"] = row_act(row)
    row["words"] = record_language(getattr(requirement, "language", ""))
    if with_versions:
        row["versions"] = [
            present_version(item, user=user, requirement=requirement)
            for item in requirement.versions.select_related("document", "filed_by", "decided_by").order_by("-number")
        ]
    return row


def row_act(row: dict) -> dict | None:
    """
    The one act a row offers, and only where the reader acts (DOCUMENT_WORKSPACE §6 zone 5, §8, §10): an OPEN piece
    (missing, to replace, expired, not valid) the reader may file is filed or replaced on its page. A filed piece, one
    in review and a valid one offer nothing on the row (a replacement is rare: it waits on the piece's page) — the
    settled row is the quiet one. Where the Conditions gate blocks the filing there is no act either: «Accepter les
    Conditions» led to a page with nothing to accept (the acceptance flow waits on the legal texts, gate G1 — the
    review of W3-B, M1): the row says «Bloqué» beside its chip, and the strip says why (``next_act``). Where there is no
    act the zone stays EMPTY: no «Consulter», no disabled button — the whole row opens the piece.
    """
    if not row["is_open"] or not row["may_file"]:
        return None
    replace = bool(row["current"])
    return {
        "label": _("Remplacer la pièce") if replace else _("Déposer la pièce"),
        "url": row["detail_url"],
        "glyph": "refresh-cw" if replace else "upload",
        "aria_label": "",
        "note": "",
    }


def next_act(row: dict | None) -> dict | None:
    """
    The strip's act for the page's next piece: the row's own act — or, where the Conditions gate blocks the filing,
    the way to the piece's page with the gate said in the register row's own words, as the dashboard's NowPanel says
    it (never a button that promises an act its target cannot do).
    """
    if row is None:
        return None
    if row["act"] is not None:
        return row["act"]
    if row["action_blocked"]:
        return {
            "label": _("Consulter"),
            "url": row["detail_url"],
            "glyph": "",
            "aria_label": "",
            "note": _("Acceptation des Conditions d’utilisation requise."),
        }
    return None


def register_groups(rows: list[dict]) -> list[dict]:
    """
    The register's three groups, by whose move it is (DOCUMENT_WORKSPACE §7.2) — never by the state alone:

    * **to act**  — an open piece (missing, to replace, expired, not valid) the person answers for;
    * **in hand** — everything else that is not settled: an open piece another actor must provide, a filed piece, a
      piece in review;
    * **settled** — a valid piece.

    Each group keeps the register's order (``STATE_ORDER``, then the due date). The strip's runs count these same
    sets and the collection draws these same groups: «ledger counts = group counts» (a test). The dashboard's
    «il registro» partitions the file's pieces by the same rule (W3-B, ``portal.services._dashboard_pieces``).
    """
    to_act = [row for row in rows if row["is_for_the_person"] and row["state"] in OPEN_STATES]
    settled = [row for row in rows if row["state"] == RequirementState.VALID]
    taken = {id(row) for row in to_act} | {id(row) for row in settled}
    in_hand = [row for row in rows if id(row) not in taken]
    return [
        {"key": GROUP_TO_ACT, "label": ChecklistStatus.PENDING.label, "rows": to_act},
        {"key": GROUP_IN_HAND, "label": ChecklistStatus.IN_PROGRESS.label, "rows": in_hand},
        {"key": GROUP_SETTLED, "label": RequirementState.VALID.label, "rows": settled},
    ]


def next_piece(rows: list[dict], case, user) -> dict | None:
    """
    The page's next piece — the strip's one primary (DOCUMENT_WORKSPACE §7.1 «the next act»): the open piece the
    reader answers for now (to file, or blocked by the Conditions gate), with its date. T1 decides first
    (``cases.services.next_action``, W3-B): when the file's one next action is a piece this reader answers for, it is
    that piece, so the dashboard's NowPanel and «Mes pièces» name the same thing. Otherwise T1's own precedence over
    those pieces: an overdue one (the oldest date first), then the nearest date, then the register's order. None when
    nothing is the reader's to do.
    """
    actionable = [row for row in rows if row["act"] is not None or row["action_blocked"]]
    if not actionable:
        return None
    chosen = None
    try:
        from cases.services import next_action

        action = next_action(case, reader=user)
    except Exception:  # noqa: BLE001 - the register stands on its own if the case module changed under it
        action = None
    if action is not None and action.kind == "piece":
        chosen = next((row for row in actionable if row["id"] == action.piece_id), None)
    if chosen is None:
        overdue = sorted((row for row in actionable if row["urgency"] == "overdue"), key=lambda row: row["due_date"])
        dated = sorted((row for row in actionable if row["due_date"]), key=lambda row: row["due_date"])
        chosen = (overdue or dated or actionable)[0]
    return chosen


def register_rows(user, *, case=None) -> list[dict]:
    """
    Every requirement the account may read, ordered worst first.

    Ordering is part of the requirement, not a nicety: art direction A §13.3 puts missing and
    expiring rows at the top because those are the rows a person came to act on.
    """
    queryset = (
        DocumentRequirement.objects.readable_by(user)
        .select_related("case", "checklist_item")
        .prefetch_related("versions__document")
    )
    if case is not None:
        queryset = queryset.filter(case=case)
    rows = sorted(queryset, key=sort_key)
    return [present_requirement(row, user=user) for row in rows]


def register_for_case(user, case) -> dict:
    """The register of ONE case: its rows, its honest counts, and who is answerable for the case."""
    requirements = sorted(
        DocumentRequirement.objects.readable_by(user)
        .filter(case=case)
        .select_related("case")
        .prefetch_related("versions__document"),
        key=sort_key,
    )
    return {
        "case": case,
        "rows": [present_requirement(row, user=user) for row in requirements],
        "counts": counts(requirements),
        "responsible": [row for row in case.assignments.select_related("organisation") if row.is_live],
    }


def primary_action(rows: list[dict]) -> dict | None:
    """The one deposit the page offers at its head: the first piece the person can act on, with
    the label the row already carries — or nothing, when nothing is theirs to file."""
    for row in rows:
        if row["may_file"]:
            label = _("Remplacer la pièce") if row["current"] else _("Déposer la pièce")
            return {"label": label, "url": row["detail_url"], "title": row["title"]}
    return None


def deposit_rules() -> dict:
    """
    What the Dépôt's client guards repeat of the server's rules (DOCUMENT_WORKSPACE §11.1, rows 1–3 and 8), read from
    the one place that states them: the size limit and the allow-list of ``documents.services``, and the project's
    clock for the validity date (``core.clock`` — a reference date on a test lane). A courtesy only: the server checks
    everything again, and its answer is the one composed.
    """
    from core import clock

    return {
        "max_bytes": services.MAX_UPLOAD_BYTES,
        "extensions": ",".join(services.ALLOWED_EXTENSIONS),
        "today": clock.today(),
    }


def state_filters(counts_per_state: dict) -> list[dict]:
    """
    The state filter's entries: every state of a piece with its count, in the REGISTER's own order (``STATE_ORDER``:
    expired, not valid, missing, to replace, in review, filed, valid — the order the rows follow), not the enum's.
    The filter is also the key to the marks (DOCUMENT_WORKSPACE §8): each entry draws its state's mark.
    """
    from core.chips import register_for

    values = sorted(RequirementState.values, key=lambda value: STATE_ORDER.get(value, 99))
    return [
        {
            "value": value,
            "label": state_label(value),
            "count": counts_per_state.get(value, 0),
            "register": register_for("documents.RequirementState", value),
        }
        for value in values
    ]


def register_context(user, *, state_filter: str = "") -> dict:
    """
    The whole page: one block per case file the account may read.

    A person may hold several case files (different purposes, different times), so the register is
    grouped by case rather than flattened: "expired" means nothing until you know which file it
    belongs to.
    """
    from cases.models import CaseFile

    if state_filter not in RequirementState.values:
        state_filter = ""
    blocks = []
    for case in CaseFile.objects.readable_by(user).order_by("-created_at"):
        block = register_for_case(user, case)
        if block["rows"]:
            # The counts, the strip and the filters describe the WHOLE file; only the rows shown
            # follow the filter, and the block says how many it holds back.
            block["all_rows"] = block["rows"]
            block["rows"] = [row for row in block["all_rows"] if not state_filter or row["state"] == state_filter]
            block["filters"] = state_filters(block["counts"]["per_state"])
            block["primary_action"] = primary_action(block["all_rows"])
            # Design V5 (W3-C): the strip's three runs count the whole file; the collection draws the same three
            # groups with the rows the filter keeps (a group left with no row is not drawn).
            block["runs"] = register_groups(block["all_rows"])
            block["groups"] = [group for group in register_groups(block["rows"]) if group["rows"]]
            block["marks"] = len(block["all_rows"]) <= MARKS_UP_TO
            block["long"] = len(block["all_rows"]) >= SEARCH_FROM
            block["next"] = next_piece(block["all_rows"], case, user)
            block["next_act"] = next_act(block["next"])
            blocks.append(block)
    # The page's ONE primary is the first file's next piece; a later file's next piece is a secondary act
    # (DOCUMENT_WORKSPACE §10 «Several dossiers»).
    first = next((index for index, block in enumerate(blocks) if block["next"]), None)
    for index, block in enumerate(blocks):
        block["next_is_primary"] = index == first
    all_rows = [row for block in blocks for row in block["all_rows"]]
    return {
        "blocks": blocks,
        "state_filter": state_filter,
        "state_filter_label": state_label(state_filter) if state_filter else "",
        "primary_action": primary_action(all_rows),
        "row_count": len(all_rows),
        "open_count": len(
            [
                row
                for row in all_rows
                if row["state"]
                in {
                    RequirementState.MISSING,
                    RequirementState.INVALID,
                    RequirementState.EXPIRED,
                    RequirementState.TO_REPLACE,
                }
            ]
        ),
        "empty_text": EMPTY_REGISTER,
    }
