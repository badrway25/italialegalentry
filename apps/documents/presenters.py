"""
What the register shows, assembled once and used by the page, the portal tag and the tests.

Presentation is kept out of the templates because every one of these decisions is a rule, not a
layout choice: which state word appears, which rule sentence goes with it, whether the account is
offered an upload button at all, and whether a link is even generated. A template that computed
those would let a change of markup change an authorisation.

Nothing here runs a query that authorisation has not already narrowed:
``DocumentRequirement.objects.readable_by(user)`` is the entry point, always.
"""

from __future__ import annotations

from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from accounts.permissions import can
from cases.models import ResponsibleActor
from documents import services
from documents.models import OPEN_STATES, DocumentRequirement, RequirementState
from documents.requirements import (
    ACTOR_GLYPHS,
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

#: What the register says when nothing at all is required yet. One sentence naming who fills the
#: region and when — never a dashed box with an icon (art direction A §14.4).
EMPTY_REGISTER = _(
    "Aucune pièce ne vous est demandée pour l’instant. Les pièces apparaissent ici lorsque "
    "l’orientation les a identifiées ou lorsqu’un intervenant du dossier les demande."
)


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
        "state_label": state_label(state),
        "state_css": state_css(state),
        "state_rule": state_rule(state),
        "state_reason": state_reason(requirement, version, state),
        "responsible": requirement.get_responsible_actor_display(),
        "responsible_actor": requirement.responsible_actor,
        "responsible_note": requirement.responsible_note,
        "responsible_glyph": ACTOR_GLYPHS.get(requirement.responsible_actor, ""),
        "urgency": due_urgency(requirement.due_date, overdue=requirement.is_overdue),
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
        # Authorised AND actually able: the Conditions gate is shown ON THE ROW with the link that
        # resolves it (art direction A §13.3), never as a banner above an empty box.
        "may_file": can(user, "file", requirement) and services.user_may_upload(user),
        "consent_required": can(user, "file", requirement) and not services.user_may_upload(user),
        "may_review": can(user, "review", requirement) and version is not None,
        # BLOQUÉ belongs where something is actually blocked. A piece that is VALIDE needs nothing
        # from anybody, and a "Bloqué" chip beside "Valide" reads as *your valid passport is
        # blocked* — the exact state confusion this register exists to remove. The consent gate is
        # still stated for every row on the piece's own page and at the foot of the register.
        "action_blocked": (
            can(user, "file", requirement) and not services.user_may_upload(user) and state in OPEN_STATES
        ),
        "detail_url": reverse("documents:requirement", args=[requirement.pk]),
        "upload_url": reverse("documents:requirement_file", args=[requirement.pk]),
        "review_url": reverse("documents:requirement_review", args=[requirement.pk]),
        "case": requirement.case,
    }
    if with_versions:
        row["versions"] = [
            present_version(item, user=user, requirement=requirement)
            for item in requirement.versions.select_related("document", "filed_by", "decided_by").order_by("-number")
        ]
    return row


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


def state_filters(counts_per_state: dict) -> list[dict]:
    """The segmented control's entries: every state of the enum, in its order, with its count."""
    from core.chips import register_for

    return [
        {
            "value": value,
            "label": state_label(value),
            "count": counts_per_state.get(value, 0),
            "register": register_for("documents.RequirementState", value),
        }
        for value in RequirementState.values
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
            blocks.append(block)
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
