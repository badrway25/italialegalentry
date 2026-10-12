"""
Business logic of the Espace réservé (views stay thin).

Absolute rule: every function takes the *account* and returns ONLY rows owned by that account.
Nothing here accepts a free-form user id from the request, and the ``get_own_*`` helpers are the
single door to a detail page (404 when the row does not exist, 403 when it belongs to somebody
else — never a silent fallback).

Sibling apps are reached defensively (``apps.get_model`` / ``import_module`` guarded against
``LookupError`` / ``ImportError``) so the reserved area keeps working — with an honest
« section indisponible » card — while another app is being changed. Documented couplings:

* enquiries     ``enquiries.services.submissions_for_user`` (fallback: the three submission models
                filtered by ``owner``), ``PublicSubmission.data_rows()`` and ``.consent``;
* forum         ``forum.ForumRegistration`` filtered by its ``user`` FK (never by e-mail);
* orientation   ``orientation.services.sessions_for_user`` and ``present_result``;
* documents     ``documents.PrivateDocument.objects.for_owner`` and ``services.user_may_upload``;
* accounts      ``Membership`` rows of the account (organisation summary, no other member's data).
"""

from __future__ import annotations

import logging
import re
from collections.abc import Callable
from dataclasses import dataclass, field
from importlib import import_module
from typing import Any

from django.apps import apps
from django.core.exceptions import FieldError, PermissionDenied, ValidationError
from django.core.paginator import Page, Paginator
from django.db import transaction
from django.http import Http404
from django.urls import NoReverseMatch, reverse
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy, ngettext

from accounts import roles
from accounts.models import MembershipRole
from accounts.permissions import can, member_of
from audit.services import record as audit_record
from core import clock, icons
from portal.models import Deadline, DeadlineStatus, Message, PortalNotice
from portal.policies import audiences_of

log = logging.getLogger("ile.portal")

DASHBOARD_LATEST = 3
PAGE_SIZE = 10

#: Failures that mean « a sibling app changed under us » — never database errors (requests are atomic).
SIBLING_ERRORS = (ImportError, LookupError, AttributeError, TypeError, FieldError)

ORGANISATION_ACCOUNT_TYPES = frozenset({"company", "institution", "university"})
ORGANISATION_ROLES = (roles.COMPANY, roles.INSTITUTION, roles.UNIVERSITY)
ORIENTATION_ACCOUNT_TYPES = frozenset({"person", "professional"})


# ---------------------------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------------------------
def safe_reverse(name: str, *args, **kwargs) -> str:
    """Reverse a (possibly foreign) URL name; "" while the sibling route does not exist."""
    try:
        return reverse(name, args=args or None, kwargs=kwargs or None)
    except NoReverseMatch:
        return ""


def _get_model(app_label: str, model_name: str):
    try:
        return apps.get_model(app_label, model_name)
    except LookupError:
        return None


def _import(module: str):
    try:
        return import_module(module)
    except ImportError:
        return None


def paginate(items, page_number, per_page: int = PAGE_SIZE) -> Page:
    """Lenient pagination: a junk or out-of-range ``?page=`` never raises."""
    return Paginator(items, per_page).get_page(page_number)


def reserved_area_enabled() -> bool:
    """Back-office kill switch (``core.SiteSettings.reserved_area_enabled``)."""
    from core.models import SiteSettings

    return bool(SiteSettings.load().reserved_area_enabled)


# ---------------------------------------------------------------------------------------------
# Messages
# ---------------------------------------------------------------------------------------------
def inbox(user):
    return Message.objects.inbox(user)


def unread_messages(user):
    """Unread, already visible messages of the account (QuerySet — ``.count()`` for the badge)."""
    return Message.objects.inbox(user).unread()


def unread_count(user) -> int:
    return unread_messages(user).count()


def get_own_message(user, pk) -> Message:
    """
    The caller's own message, or 404 — never 403 (L-06/L-07, REQ-IAM-06).

    A 403 on somebody else's message says "this message exists and is not yours", which is a
    disclosure in itself: the identifier is sequential enough to walk, and the answer alone maps out
    who is corresponding with the project. A 404 says nothing at all, and says it identically for a
    message that was never created.

    The authorisation is applied IN THE QUERY rather than after the fetch, so the row is never loaded
    for a caller who may not have it. Fetch-then-check is only ever one refactor away from becoming
    fetch-then-forget-to-check.
    """
    message = Message.objects.inbox(user).filter(pk=pk).first()
    if message is None or not can(user, "view", message) or not message.is_visible():
        raise Http404
    return message


@transaction.atomic
def mark_message_read(user, pk, request=None) -> Message:
    """Flip the read state of the caller's OWN message (idempotent). Anything else → 403/404."""
    message = get_own_message(user, pk)
    if not can(user, "mark_read", message):
        # Reached only for a message the caller CAN see, so its existence is already known to them
        # and 403 is the honest answer here. This is the one case where 403 is right.
        raise PermissionDenied
    if not message.is_read:
        message.is_read = True
        message.read_at = clock.now()
        message.save(update_fields=["is_read", "read_at", "updated_at"])
        audit_record(request, action="portal.message.read", target=message, actor=user)
    return message


def send_message(*, recipient, subject: str, body: str, sender=None, related=None, visible_from=None, request=None):
    """Create a staff-authored message (used by the admin and by future CRM hooks) + audit row."""
    message = Message(recipient=recipient, sender=sender, subject=subject, body=body, visible_from=visible_from)
    if related is not None:
        message.related_object = related
    message.full_clean()
    message.save()
    audit_message_created(message, request=request, actor=sender)
    try:
        # The notification ATTACHES to this row rather than writing a second one: the person must
        # see the subject the author chose, once, not a machine paraphrase of it alongside.
        from notifications.services import notify_for_message

        notify_for_message(message, request=request, actor=sender)
    except Exception:  # noqa: BLE001 - the message exists and is audited; announcing it is an extra
        log.exception("message %s could not be announced", message.pk)
    return message


def audit_message_created(message: Message, *, request=None, actor=None) -> None:
    """Audit metadata never contains the subject/body or the recipient's e-mail."""
    audit_record(
        request,
        action="portal.message.created",
        target=message,
        actor=actor,
        metadata={
            "recipient_id": message.recipient_id,
            "scheduled": message.visible_from is not None,
            "related": message.content_type.model if message.content_type_id else "",
        },
    )


def related_link(user, message: Message) -> dict[str, str] | None:
    """
    Link from a message to the record it is about — only when that record belongs to the reader.
    A staff mistake (linking somebody else's record) therefore never leaks anything.
    """
    if not message.content_type_id or not message.object_id:
        return None
    try:
        target = message.related_object
    except (*SIBLING_ERRORS, ValueError, ValidationError):
        return None
    if target is None:
        return None
    for kind in REQUEST_KINDS.values():
        model = kind.model()
        if model is not None and isinstance(target, model):
            if getattr(target, f"{kind.owner_field}_id", None) != user.id:
                return None
            return {
                "label": _("Voir la demande concernée"),
                "url": reverse("portal:request_detail", kwargs={"kind": kind.slug, "pk": target.pk}),
            }
    if isinstance(target, Deadline):
        if target.owner_id != user.id:
            return None
        return {"label": _("Voir mes échéances"), "url": reverse("portal:deadlines")}
    document_model = _get_model("documents", "PrivateDocument")
    if document_model is not None and isinstance(target, document_model):
        if target.owner_id != user.id or target.deleted_at is not None:
            return None
        return {"label": _("Voir mes documents"), "url": reverse("portal:documents")}
    return None


# ---------------------------------------------------------------------------------------------
# Deadlines
# ---------------------------------------------------------------------------------------------
def deadlines_for(user):
    return Deadline.objects.for_owner(user)


def present_deadline(deadline: Deadline, today=None) -> dict[str, Any]:
    today = today or clock.today()
    badge_label, badge_kind = "", ""
    if deadline.is_overdue(today):
        badge_label, badge_kind = _("En retard"), "error"
    elif deadline.is_soon(today):
        badge_label, badge_kind = _("Bientôt"), "warning"
    elif deadline.status == DeadlineStatus.DONE:
        badge_label, badge_kind = deadline.get_status_display(), "success"
    elif deadline.status == DeadlineStatus.CANCELLED:
        badge_label, badge_kind = deadline.get_status_display(), "neutral"
    return {
        "obj": deadline,
        "title": deadline.title,
        "due_on": deadline.due_on,
        "kind_label": deadline.get_kind_display(),
        "status_label": deadline.get_status_display(),
        "description": deadline.description,
        "source_note": deadline.source_note,
        "badge_label": badge_label,
        "badge_kind": badge_kind,
        "is_open": deadline.is_open,
    }


def deadlines_page(user) -> dict[str, Any]:
    today = clock.today()
    rows = list(deadlines_for(user))
    open_rows = [present_deadline(d, today) for d in rows if d.is_open]
    closed_rows = [present_deadline(d, today) for d in rows if not d.is_open]
    closed_rows.sort(key=lambda r: r["due_on"], reverse=True)
    return {"open_deadlines": open_rows, "closed_deadlines": closed_rows}


# ---------------------------------------------------------------------------------------------
# Notices
# ---------------------------------------------------------------------------------------------
def notices_for(user) -> list[PortalNotice]:
    return list(PortalNotice.objects.live().for_audiences(audiences_of(user)).order_by("order", "-created_at"))


# ---------------------------------------------------------------------------------------------
# Requests (« Mes demandes »)
# ---------------------------------------------------------------------------------------------
FORUM_FIELDS = (
    "first_name",
    "last_name",
    "organisation",
    "role",
    "email",
    "phone",
    "country",
    "category",
    "sector_of_interest",
)

STATUS_BADGES = {
    "new": "info",
    "in_progress": "pending",
    "handled": "success",
    "archived": "neutral",
    "pending": "pending",
    "confirmed": "success",
    "cancelled": "neutral",
    "attended": "success",
}


@dataclass(frozen=True)
class RequestKind:
    """One kind of record listed under « Mes demandes » (slug = URL segment)."""

    slug: str
    app_label: str
    model_name: str
    owner_field: str
    title_attr: str = ""
    fields: tuple[str, ...] = ()

    def model(self):
        return _get_model(self.app_label, self.model_name)

    def title_of(self, obj) -> str:
        value = getattr(obj, self.title_attr, "") if self.title_attr else ""
        return str(value) if value else str(obj._meta.verbose_name)


REQUEST_KINDS: dict[str, RequestKind] = {
    k.slug: k
    for k in (
        RequestKind("besoins-entreprise", "enquiries", "CompanyNeedsRequest", "owner", "company_name"),
        RequestKind("collaboration", "enquiries", "CollaborationProposal", "owner", "organisation_name"),
        RequestKind("contact", "enquiries", "ContactRequest", "owner", "subject"),
        RequestKind("inscription-forum", "forum", "ForumRegistration", "user", "", FORUM_FIELDS),
    )
}


def _kind_of(obj) -> RequestKind | None:
    for kind in REQUEST_KINDS.values():
        model = kind.model()
        if model is not None and type(obj) is model:
            return kind
    return None


@dataclass(frozen=True)
class RequestItem:
    kind: str
    pk: Any
    title: str
    kind_label: str
    status_label: str
    status_kind: str
    created_at: Any
    url: str


def _present_request(obj, kind: RequestKind) -> RequestItem:
    status = getattr(obj, "status", "")
    display = getattr(obj, "get_status_display", None)
    return RequestItem(
        kind=kind.slug,
        pk=obj.pk,
        title=kind.title_of(obj),
        kind_label=str(obj._meta.verbose_name),
        status_label=str(display()) if callable(display) else str(status),
        status_kind=STATUS_BADGES.get(status, "neutral"),
        created_at=obj.created_at,
        url=reverse("portal:request_detail", kwargs={"kind": kind.slug, "pk": obj.pk}),
    )


def _enquiry_rows(user) -> list:
    services = _import("enquiries.services")
    helper = getattr(services, "submissions_for_user", None) if services else None
    if callable(helper):
        return list(helper(user))
    # Fallback coupling: the submission models filtered by their ``owner`` FK.
    rows: list = []
    for kind in REQUEST_KINDS.values():
        if kind.app_label != "enquiries":
            continue
        model = kind.model()
        if model is not None:
            rows.extend(model.objects.filter(owner=user, anonymised_at__isnull=True))
    return rows


def _forum_rows(user) -> list:
    model = REQUEST_KINDS["inscription-forum"].model()
    if model is None:
        return []
    # Strictly the linked account — never a match on the e-mail address.
    return list(model.objects.filter(user=user, anonymised_at__isnull=True))


def requests_for(user) -> list[RequestItem]:
    """Every request of the account, newest first. Rows of an unknown model are ignored."""
    if not getattr(user, "is_authenticated", False):
        return []
    items: list[RequestItem] = []
    for obj in [*_enquiry_rows(user), *_forum_rows(user)]:
        kind = _kind_of(obj)
        # Belt and braces: re-check ownership on every row returned by a sibling helper.
        if kind is None or getattr(obj, f"{kind.owner_field}_id", None) != user.id:
            continue
        items.append(_present_request(obj, kind))
    items.sort(key=lambda item: item.created_at, reverse=True)
    return items


def _data_rows(obj, kind: RequestKind) -> list[tuple[str, str]]:
    helper = getattr(obj, "data_rows", None)
    if callable(helper):
        return [(str(label), str(value)) for label, value in helper()]
    rows = []
    for name in kind.fields:
        model_field = obj._meta.get_field(name)
        value = getattr(obj, name)
        if getattr(model_field, "choices", None):
            value = getattr(obj, f"get_{name}_display")()
        rows.append((str(model_field.verbose_name), "" if value is None else str(value)))
    return rows


def _consent_meta(obj) -> dict[str, Any] | None:
    """What the person is entitled to know about their own consent (purpose, version, timestamp)."""
    consent = getattr(obj, "consent", None)
    if consent is None:
        return None
    text = getattr(consent, "consent_text", None)
    purpose_display = getattr(consent, "get_purpose_display", None)
    return {
        "purpose": str(purpose_display()) if callable(purpose_display) else str(getattr(consent, "purpose", "")),
        "version": getattr(text, "version", None),
        "given_at": getattr(consent, "given_at", None),
        "language": getattr(consent, "language", ""),
        "withdrawn_at": getattr(consent, "withdrawn_at", None),
    }


def get_own_request(user, kind_slug: str, pk) -> dict[str, Any]:
    kind = REQUEST_KINDS.get(kind_slug)
    model = kind.model() if kind else None
    if model is None:
        raise Http404
    # Ownership is part of the QUERY, so a row belonging to somebody else is never loaded and the
    # answer for "not yours" is indistinguishable from "does not exist" — the same 404, from the
    # same branch, with no timing difference worth measuring.
    owned = model.objects.filter(pk=pk, **{kind.owner_field: user}).select_related("consent__consent_text")
    obj = owned.first()
    if obj is None or not can(user, "view", obj):
        raise Http404
    if getattr(obj, "anonymised_at", None) is not None:
        # An anonymised record is gone as far as anyone is concerned, including the person it
        # described. Answering 403 would assert that something is still there.
        raise Http404
    return {
        "item": _present_request(obj, kind),
        "rows": [(label, value) for label, value in _data_rows(obj, kind) if value],
        "consent": _consent_meta(obj),
        "language": getattr(obj, "language", ""),
    }


# ---------------------------------------------------------------------------------------------
# Orientation (« Mon parcours »)
# ---------------------------------------------------------------------------------------------
def _own_sessions(user):
    """(orientation.services module, the account's sessions — newest first). One query."""
    module = _import("orientation.services")
    helper = getattr(module, "sessions_for_user", None) if module else None
    if not callable(helper):
        raise LookupError("orientation.services.sessions_for_user is not available")
    # Belt and braces: re-check ownership on every row returned by the sibling helper.
    return module, [session for session in helper(user) if session.user_id == user.id]


def _present_session(session, module, *, with_result: bool = True) -> dict[str, Any]:
    """
    One row of « Mon parcours ». ``with_result=False`` skips ``present_result`` (several queries per
    result: checklist, translations) when the caller only needs the metadata of the session.
    """
    present = getattr(module, "present_result", None)
    result = getattr(session, "result", None) if session.is_completed else None
    row: dict[str, Any] = {
        "reference": session.reference,
        "status_label": session.get_status_display(),
        "is_completed": bool(result),
        "updated_at": session.updated_at,
        "ruleset_version": session.ruleset.version,
        "result": None,
        "url": "",
        "date": session.updated_at,
    }
    if result is not None:
        row["ruleset_version"] = result.ruleset_version
        row["date"] = result.created_at
        row["disclaimer_version"] = result.disclaimer_version
        row["result"] = present(result) if with_result and callable(present) else None
        row["url"] = safe_reverse("orientation:result", session_id=session.id)
    elif session.status == "in_progress":
        row["url"] = safe_reverse("orientation:step", session_id=session.id)
    return row


def pathway_sessions(user, present_first: int | None = None) -> list[dict[str, Any]]:
    """
    The account's orientation sessions; completed ones carry the frozen, presented result.
    ``present_first=N`` presents the result of the first N completed sessions only (the dashboard
    shows one): the cost of a page must not follow the size of the account's history.
    """
    module, sessions = _own_sessions(user)
    rows: list[dict[str, Any]] = []
    presented = 0
    for session in sessions:
        wanted = present_first is None or presented < present_first
        row = _present_session(session, module, with_result=wanted)
        if row["result"] is not None:
            presented += 1
        rows.append(row)
    return rows


def pathways_page(user, page_number=None) -> dict[str, Any]:
    """« Mon parcours »: paginate FIRST, then present only the sessions of the requested page."""
    try:
        module, sessions = _own_sessions(user)
        page_obj = paginate(sessions, page_number)
        page_obj.object_list = [_present_session(session, module) for session in page_obj.object_list]
        available = True
    except SIBLING_ERRORS:
        log.exception("portal pathways unavailable", extra={"event": "portal.pathways_unavailable"})
        page_obj, available = paginate([], None), False
    return {"page_obj": page_obj, "available": available, "orientation_url": safe_reverse("orientation:start")}


# ---------------------------------------------------------------------------------------------
# Documents
# ---------------------------------------------------------------------------------------------
SCAN_BADGES = {"pending": "pending", "clean": "success", "infected": "error", "error": "warning"}


def _present_document(doc, *, own: bool) -> dict[str, Any]:
    downloadable = doc.has_file and not doc.is_infected and (own or doc.is_clean)
    return {
        "name": doc.original_name,
        "description": doc.description,
        "kind_label": doc.get_kind_display(),
        "size": doc.size,
        "created_at": doc.created_at,
        "scan_label": doc.get_scan_status_display(),
        "scan_kind": SCAN_BADGES.get(doc.scan_status, "neutral"),
        "organisation": doc.organisation.name if doc.organisation_id else "",
        "url": safe_reverse("documents:download", pk=doc.pk) if downloadable else "",
    }


def documents_for(user):
    model = _get_model("documents", "PrivateDocument")
    if model is None:
        raise LookupError("documents.PrivateDocument is not available")
    return model.objects.for_owner(user).select_related("organisation")


#: Upper bound of the « Documents de mon organisation » table (most recent first).
ORGANISATION_DOCUMENTS_LIMIT = 50


def organisation_documents_for(user, limit: int = ORGANISATION_DOCUMENTS_LIMIT) -> list[dict[str, Any]]:
    """
    Documents attached to an organisation the account is RESPONSIBLE for (membership role « owner »),
    uploaded by its other members — mirrors ``documents.policies`` so every listed row is one the
    account may actually open. Never another organisation's documents, never the uploader's identity.

    Cost: the object-level policy is consulted ONCE PER ORGANISATION (on its most recent document),
    not once per row — ``accounts.permissions.can`` costs two queries per call, which used to make
    the page cost follow the number of documents. The rows themselves are already restricted by the
    query (alive, organisation owned by the account); a refusal drops the whole organisation. The
    list is bounded to the ``limit`` most recent documents.
    """
    model = _get_model("documents", "PrivateDocument")
    if model is None:
        return []
    organisation_ids = list(
        user.memberships.filter(role=MembershipRole.OWNER).values_list("organisation_id", flat=True)
    )
    if not organisation_ids:
        return []
    docs = (
        model.objects.alive()
        .filter(organisation_id__in=organisation_ids)
        .exclude(owner=user)
        .select_related("organisation")
        .order_by("-created_at")[:limit]
    )
    verdicts: dict[Any, bool] = {}
    rows = []
    for doc in docs:
        if doc.organisation_id not in verdicts:
            verdicts[doc.organisation_id] = can(user, "view", doc)  # deny by default
        if verdicts[doc.organisation_id]:
            rows.append(_present_document(doc, own=False))
    return rows


def may_upload(user) -> bool:
    services = _import("documents.services")
    helper = getattr(services, "user_may_upload", None) if services else None
    return bool(helper(user)) if callable(helper) else False


def documents_page(user) -> dict[str, Any]:
    """Own documents (+ those of an organisation the account is responsible for); upload entry point."""
    try:
        own = [_present_document(d, own=True) for d in documents_for(user)]
        shared = organisation_documents_for(user)
        available = True
    except SIBLING_ERRORS:
        log.exception("portal documents unavailable", extra={"event": "portal.documents_unavailable"})
        own, shared, available = [], [], False
    return {
        "documents": own,
        "organisation_documents": shared,
        "organisation_documents_limit": ORGANISATION_DOCUMENTS_LIMIT
        if len(shared) >= ORGANISATION_DOCUMENTS_LIMIT
        else 0,
        "available": available,
        "may_upload": may_upload(user),
        "upload_url": safe_reverse("documents:upload"),
        "manage_url": safe_reverse("documents:index"),
    }


# ---------------------------------------------------------------------------------------------
# Organisation
# ---------------------------------------------------------------------------------------------
def shows_organisation_card(user) -> bool:
    if getattr(user, "account_type", "") in ORGANISATION_ACCOUNT_TYPES:
        return True
    if user.is_superuser:
        return False
    return roles.has_role(user, *ORGANISATION_ROLES)


def organisations_for(user) -> list[dict[str, Any]]:
    """Membership summary — the organisation's public identity and the account's own role only."""
    rows = []
    for membership in user.memberships.select_related("organisation").order_by("organisation__name"):
        organisation = membership.organisation
        if not member_of(user, organisation.pk):  # accounts.permissions — deny by default
            continue
        place = ", ".join(part for part in (organisation.city, organisation.country) if part)
        rows.append(
            {
                "name": organisation.name,
                "kind_label": organisation.get_kind_display(),
                "place": place,
                "role_label": membership.get_role_display(),
                "since": membership.created_at,
            }
        )
    return rows


# ---------------------------------------------------------------------------------------------
# Navigation — the console's shell
# ---------------------------------------------------------------------------------------------
#: The console's spaces — level 1 of the rail (design V5: V5.4 plan §1.18 D06, §3.5 item 3; W3-A). A space is a
#: set of pages that share ONE rail: «Espace réservé», which every account has, and «Espace entreprise», the
#: company workspace. A page belongs to one space by its route, and to no other: nothing about it is stored.
SPACE_PERSON = "person"
SPACE_COMPANY = "company"

#: A rail entry is a page of its space, or the way to another space — drawn at the rail's head, never in its list.
KIND_PAGE = "page"
KIND_SPACE = "space"


def shell_navigation(user, space: str = SPACE_PERSON, active: str = "", *, company=None) -> list[dict[str, Any]]:
    """
    The rail of one space of the console — the ONE builder of every rail (plan §1.18 D06).

    Three levels, in the shape the rail draws them: the space (``space`` on every entry: its name, and who the
    account is — the glyph and the word of the rail's foot), the section (``group``) and the page (the entry).
    Every producer of a console page asks this function, so the keys of a space's rail are the same on each of
    its URLs — the Academy, the help desk and the selection workspace each used to add or drop rows on their own
    pages, which is how an operator's dispatch desk was reachable from the help desk only and a professional's
    queue was listed twice there.

    * ``space`` — ``SPACE_PERSON`` («Espace réservé») or ``SPACE_COMPANY`` («Espace entreprise», whose own
      entries are companies.services.navigation's: the module decides what a company, a prospect and a project
      reader may be offered, and it is not second-guessed here).
    * ``active`` — the key of the entry the page belongs to; at most one entry is ``current``.
    * an entry of ``kind`` ``KIND_SPACE`` is the way to the account's OTHER space: the rail draws it at its
      head, the bottom bar among its four; it is never a page of this rail.
    * ``bottom`` — at most four entries, for every role (``_bottom_keys``); ``yields`` — on the one of the four
      that leaves the bar where four words and «Menu» do not hold on one row, the width at which it leaves
      (``_bottom_yield``: ``"narrow"``, ``"phone"``; ``""`` on every other entry); ``lines`` — the label of an
      entry of the bar as the one or two runs the bar may put on two lines (``_bar_lines``), and ``stacks`` —
      whether a phone's bar always does (``_bar_stacks``: the bar's words do not hold on one line of a phone).
    """
    if space == SPACE_COMPANY:
        return _company_rail(user, active, company)
    return _person_rail(user, active)


def navigation(user, active: str = "") -> list[dict[str, Any]]:
    """
    The reserved area's own navigation — ``shell_navigation`` for «Espace réservé».

    The Academy and the help desk are listed HERE, not only on their own pages. Each module used to
    append its row to this list from inside itself, which reads sensibly until you ask how somebody
    reaches the first page of a module they have never opened: the row appeared once you were
    already there. Both surfaces answered 200, had a correct single `h1` and no console errors, and
    were unreachable by clicking — found by walking the mandate's flow
    `… → DOCUMENTI → FORMAZIONE/SPORTELLO` in a browser instead of trusting that each page worked.

    The same holds for the surfaces a ROLE owns — a professional's assigned queue, an operator's
    dispatch desk, an authorised actor's processes: they are rows of this rail, on every page.
    """
    return shell_navigation(user, SPACE_PERSON, active)


def shell_space(user, space: str = SPACE_PERSON, *, held: set[str] | None = None) -> dict[str, Any]:
    """
    Level 1 of the rail: the space's name — the line under the name at the rail's head — its own glyph and
    where it starts (``url``: where the mark leads, the phone's tile, the way back from the other space); and
    who the account is, in every space alike (``who``, ``who_icon``: the disc and the word beside the account's
    name at the rail's foot): Persona ≠ Impresa ≠ Istituzione ≠ Università, in the registry's glyphs. The disc
    is drawn from ``who_domain`` and ``who_key`` through the registry's ``concept`` filter (W1-C's O14 lint reads
    the template); ``who_icon`` is the same symbol, resolved here. ``held`` spares a query to a caller that has
    already read the account's roles.
    """
    held = roles.roles_of(user) if held is None else held
    (who_domain, who_key), who = _audience(user, held)
    who_icon = icons.concept(who_domain, who_key)
    if space == SPACE_COMPANY:
        return {
            "key": SPACE_COMPANY,
            "label": str(_("Espace entreprise")),
            "url": safe_reverse("companies:dashboard"),
            "icon": icons.AUDIENCE["company"],
            "who": who,
            "who_icon": who_icon,
            "who_domain": who_domain,
            "who_key": who_key,
        }
    return {
        "key": SPACE_PERSON,
        "label": str(_("Espace réservé")),
        "url": _person_space_start(user, held),
        "icon": SPACE_PERSON_GLYPH,
        "who": who,
        "who_icon": who_icon,
        "who_domain": who_domain,
        "who_key": who_key,
    }


def _person_space_start(user, held: set[str]) -> str:
    """
    Where «Espace réservé» starts for this account — where its rail starts. For an account that holds a role's
    register, the first entry of «Mon rôle»: the dispatch desk, the professional's queue, the assigned processes.
    The mark and the phone's tile took the administrator and every role account to a person's dashboard, whose
    one thing to do is an applicant's questionnaire (the W3-A review's M1): the dashboard stays one key away,
    under «Parcours». For every other account, the dashboard. No query: the roles are the caller's.
    """
    for key, _label, url in _role_surfaces(user, held):
        if key not in ROLE_SPACES:
            return url
    return reverse("portal:dashboard")


#: «Espace réservé» as a destination — the way back from another space: the registry's `ile-key` («Espace
#: réservé: access»), the glyph the public chrome's account menu draws for the same entry.
SPACE_PERSON_GLYPH = "ile-key"

#: Who the account is, for the rail's foot — the first row that holds. The project's team first;
#: then the account's ROLES, because a privilege is a group here whatever the account's type says and the type
#: defaults to «person» (a company's representative, a professional and an operator are all created with it);
#: then the type, for an account that holds no role yet. Each row: the roles that carry it, the account types
#: that do, the registry's concept — its domain and key in apps/core/icons.py, AUDIENCE or ACTOR — and the role
#: whose label names it. The concept, not the glyph, reaches the template: the rail's foot draws it through the
#: registry's `concept` filter, where W1-C's O14 lint can see that the symbol is registry-fed (a variable symbol
#: inside a status context; tests/frontend/test_o14_lint.py).
_AUDIENCES: tuple[tuple[tuple[str, ...], tuple[str, ...], tuple[str, str], str], ...] = (
    ((roles.INSTITUTION,), ("institution",), ("audience", "institution"), roles.INSTITUTION),
    ((roles.UNIVERSITY,), ("university",), ("audience", "university"), roles.UNIVERSITY),
    ((roles.TRAINING_PROVIDER,), (), ("actor", "training_body"), roles.TRAINING_PROVIDER),
    ((roles.AUTHORISED_ACTOR,), (), ("actor", "authorised_actor"), roles.AUTHORISED_ACTOR),
    ((roles.PROFESSIONAL,), ("professional",), ("actor", "professional"), roles.PROFESSIONAL),
    ((roles.PERSON,), ("person",), ("audience", "person"), roles.PERSON),
    ((roles.COMPANY,), ("company",), ("audience", "company"), roles.COMPANY),
)


def _audience(user, held: set[str]) -> tuple[tuple[str, str], str]:
    """((domain, key), word) of who the account is — the registry's concept and its label: see ``_AUDIENCES``."""
    if getattr(user, "is_staff", False) or held & set(roles.BACKOFFICE_ROLES):
        return ("actor", "project_team"), str(roles.ROLE_LABELS[roles.STAFF])
    for carried_by, _types, concept, label_role in _AUDIENCES:
        if held & set(carried_by):
            return concept, str(roles.ROLE_LABELS[label_role])
    account_type = getattr(user, "account_type", "")
    for _carried_by, types, concept, label_role in _AUDIENCES:
        if account_type in types:
            return concept, str(roles.ROLE_LABELS[label_role])
    return ("audience", "person"), str(roles.ROLE_LABELS[roles.PERSON])


def _person_rail(user, active: str) -> list[dict[str, Any]]:
    unread = unread_count(user)
    messages_label = _("Communications")
    if unread:
        messages_label = _("Communications (%(count)d)") % {"count": unread}
    # In the order of the rail's sections (design V4, CREATIVE_DIRECTION.md §3.9): the journey, the
    # file, the exchanges, the Academy. The registers a role owns come BEFORE them (below): they are
    # what that account signs in for, and at the foot of ten rows they sat under the fold of a laptop.
    pages = [
        ("dashboard", _("Tableau de bord"), reverse("portal:dashboard")),
        ("situation", _("Ma situation"), reverse("portal:situation")),
        ("pathways", _("Mon parcours"), reverse("portal:pathways")),
        ("cases", _("Mes dossiers"), reverse("cases:index")),
        ("requests", _("Mes demandes"), reverse("portal:requests")),
        ("documents", _("Mes documents"), reverse("portal:documents")),
        ("deadlines", _("Mes échéances"), reverse("portal:deadlines")),
        ("messages", messages_label, reverse("portal:messages")),
        ("helpdesk", _("Guichet numérique"), reverse("helpdesk:requests")),
        ("academy", _("Academy"), reverse("academy:catalogue")),
    ]
    panel = _identity_panel(user)
    if panel:
        pages.insert(len(pages) - 1, panel)  # the last of «Échanges», before the Academy
    held = roles.roles_of(user)
    registers: list[tuple[str, Any, str, str, str]] = []
    spaces: list[tuple[str, Any, str, str, str]] = []
    for key, label, url in _role_entries(user):
        if key in ROLE_SPACES:
            # Another space of the account: named as that space names itself, drawn at the rail's head.
            other = shell_space(user, ROLE_SPACES[key], held=held)
            spaces.append((key, other["label"], url, other["label"], KIND_SPACE))
        else:
            registers.append((key, label, url, str(NAV_GROUP_ROLE), KIND_PAGE))
    entries = [
        *registers,
        *((key, label, url, str(NAV_GROUPS[key]), KIND_PAGE) for key, label, url in pages),
        *spaces,
    ]
    keys = [key for key, *_rest in entries]
    bottom = _bottom_keys(keys)
    yields, when = _bottom_yield([key for key in keys if key in bottom])
    stacks = _bar_stacks(
        [label for key, label, *_rest in entries if key in bottom and not (key == yields and when == YIELDS_PHONE)]
    )
    plate = shell_space(user, SPACE_PERSON, held=held)
    return [
        {
            "key": key,
            "label": label,
            "url": url,
            "current": key == active,
            "icon": NAV_GLYPHS.get(key, "chevron-end"),
            "group": group,
            "bottom": key in bottom,
            "yields": when if key == yields else "",
            "lines": _bar_lines(label) if key in bottom else [],
            "stacks": stacks and key in bottom,
            "kind": kind,
            "space": plate,
        }
        for key, label, url, group, kind in entries
    ]


def _identity_panel(user) -> tuple[str, Any, str] | None:
    """
    «Communications d’identité» — the person's own panel of the selection module — as a page of the rail, for
    the account somebody has asked to know.

    Not an eleventh destination for everybody: the ten are kept (plan §1.18 D06). The module used to list the
    panel in a rail of its own, drawn on its own pages only; under one builder that row is either lost or given
    a place — and a consent that can be withdrawn at any moment has to stay within reach of the person who gave
    it. The keys still do not depend on the page: they depend on the account.
    """
    if not getattr(user, "is_authenticated", False):
        return None
    url = safe_reverse("selection:disclosures")
    selection = _import("selection.services")
    if not url or selection is None:
        return None
    try:
        asked = selection.has_disclosures(user)
    except SIBLING_ERRORS:
        log.exception("identity panel unavailable", extra={"event": "portal.identity_panel_unavailable"})
        return None
    return ("disclosures", _("Communications d’identité"), url) if asked else None


def _company_rail(user, active: str, company) -> list[dict[str, Any]]:
    """
    «Espace entreprise»: the module's own entries (companies.services.navigation), then the way back to
    «Espace réservé», which every account has. A deployment without the module has no such space.
    """
    try:
        from companies import services as company_services

        rail = [dict(item) for item in company_services.navigation(user, active, company=company)]
    except SIBLING_ERRORS:
        log.exception("company rail unavailable", extra={"event": "portal.company_rail_unavailable"})
        rail = []
    held = roles.roles_of(user)
    plate = shell_space(user, SPACE_COMPANY, held=held)
    for item in rail:
        item.setdefault("kind", KIND_PAGE)
        item["space"] = plate
    # The module flags the entries of its own bottom bar (four for a company). The cap is the shell's, and so is
    # the rest of the bar: an account the module offers fewer flagged entries — a project reader without a company
    # has «Analyse territoriale» and «Communications» — keeps its pages on the bar, in the rail's order, while
    # there is room. The page one is on was missing from a bar that showed one entry and «Menu».
    flagged = [item for item in rail if item.get("bottom")]
    for item in flagged[NAV_BOTTOM_MAX:]:
        item["bottom"] = False
    room = NAV_BOTTOM_MAX - min(len(flagged), NAV_BOTTOM_MAX)
    for item in rail:
        if room and not item.get("bottom"):
            item["bottom"] = True
            room -= 1
    yields, when = _bottom_yield([item["key"] for item in rail if item["bottom"]])
    stacks = _bar_stacks(
        [item["label"] for item in rail if item["bottom"] and not (item["key"] == yields and when == YIELDS_PHONE)]
    )
    for item in rail:
        item["yields"] = when if item["key"] == yields else ""
        item["lines"] = _bar_lines(item["label"]) if item["bottom"] else []
        item["stacks"] = stacks and bool(item["bottom"])
    home = shell_space(user, SPACE_PERSON, held=held)
    rail.append(
        {
            "key": "reserved",
            "label": home["label"],
            "url": home["url"],
            "current": False,
            "icon": home["icon"],  # `ile-key`
            "group": home["label"],
            "bottom": False,
            "yields": "",
            "lines": [],
            "stacks": False,
            "kind": KIND_SPACE,
            "space": plate,
        }
    )
    return rail


#: The glyph of each entry in the rail, the bottom bar and the drawer — glyph + word, never the glyph
#: alone. It is the icon registry's map (apps/core/icons.py NAV; design V5, V5.4 plan §1.7): one concept,
#: one glyph — the journey is the steps of the mark, a case its folder, the help desk its bell, the
#: Academy its book; `briefcase`, `handshake`, `university` and `calendar` keep the meaning they have
#: everywhere else (the professional, the Forum, the training body, a date). A key added to the rail is
#: added to the registry first: tests/frontend/test_icons.py holds the two equal, entry by entry.
NAV_GLYPHS: dict[str, str] = dict(icons.NAV)

#: The rail's sections — level 2. The titles were proposed for the copy review (directive §92) and are the
#: catalogue's; a section whose title only repeats its one entry («Academy») is drawn as a rule, without the
#: word (templates/portal/partials/rail_nav.html). A role's own registers sit under their own title.
NAV_GROUP_PARCOURS = gettext_lazy("Parcours")
NAV_GROUP_DOSSIER = gettext_lazy("Dossier")
NAV_GROUP_ECHANGES = gettext_lazy("Échanges")
NAV_GROUP_ACADEMY = gettext_lazy("Academy")
NAV_GROUP_ROLE = gettext_lazy("Mon rôle")
NAV_GROUPS: dict[str, Any] = {
    "dashboard": NAV_GROUP_PARCOURS,
    "situation": NAV_GROUP_PARCOURS,
    "pathways": NAV_GROUP_PARCOURS,
    "cases": NAV_GROUP_DOSSIER,
    "requests": NAV_GROUP_DOSSIER,
    "documents": NAV_GROUP_DOSSIER,
    "deadlines": NAV_GROUP_DOSSIER,
    "messages": NAV_GROUP_ECHANGES,
    "helpdesk": NAV_GROUP_ECHANGES,
    "disclosures": NAV_GROUP_ECHANGES,
    "academy": NAV_GROUP_ACADEMY,
}

#: The bottom bar below 64rem shows FOUR entries and «Menu», for every role (design V4 §3.9; V5.4 plan §3.5
#: item 3, the platform audit's S-4: a company account had five flagged entries, six columns with «Menu»).
#: The first four of this order that the rail holds: the dashboard, the surface the account's role owns — in
#: the place of the cases, when it has one — then the pieces and the communications.
NAV_BOTTOM_MAX = 4
NAV_BOTTOM: tuple[str, ...] = ("dashboard", "documents", "messages", "cases")


def _bottom_keys(keys: list[str]) -> frozenset[str]:
    """The entries of a rail that the bottom bar draws: never more than ``NAV_BOTTOM_MAX``."""
    own = [key for _role, key, _route in ROLE_SURFACES if key in keys][:1]
    wanted = [*(key for key in NAV_BOTTOM[:3] if key in keys), *own, *(key for key in NAV_BOTTOM[3:] if key in keys)]
    return frozenset(wanted[:NAV_BOTTOM_MAX])


#: Four words and «Menu» do not hold on one row at every width. The labels are the live ones — none is
#: shortened — so where the row is too short the bar keeps THREE entries and «Menu», and one entry leaves: the
#: first of this order that the bar holds — the cases for a person (the dashboard opens on the case), the pieces
#: where a role's own register is on the bar, the company's sheet in «Espace entreprise». It stays in the
#: drawer, one press further. Measured on the lane, ten accounts × four languages × six widths:
#:
#: * ``YIELDS_NARROW`` — below 22.5rem (a 320 px phone, a window at 400 %), for every bar: a person's four
#:   words hold from 360 px with air between them, not below;
#: * ``YIELDS_PHONE`` — below 30rem, for a bar that carries a role's register («Demandes qui me sont confiées»,
#:   «Désignation des professionnels», «Processus assignés» and their translations): with four entries its
#:   words stood 4 px apart from 360 to 430 px, and a professional's needed a third line in English.
NAV_BOTTOM_YIELDS: tuple[str, ...] = ("cases", "documents", "profile")
YIELDS_NARROW = "narrow"
YIELDS_PHONE = "phone"


def _bottom_yield(on_the_bar: list[str]) -> tuple[str, str]:
    """(key, when) of the entry that leaves a full bottom bar where the row is too short; ``("", "")`` when the
    bar is not full."""
    if len(on_the_bar) < NAV_BOTTOM_MAX:
        return "", ""
    key = next((key for key in NAV_BOTTOM_YIELDS if key in on_the_bar), on_the_bar[-1])
    registers = {surface for _role, surface, _route in ROLE_SURFACES if surface not in ROLE_SPACES}
    return key, YIELDS_PHONE if registers & set(on_the_bar) else YIELDS_NARROW


def _bar_lines(label) -> list[str]:
    """
    A label of the bottom bar as the one or two runs it may stand on: split at the space that leaves the
    shorter longest run («Tableau» · «de bord», «Demandes qui me» · «sont confiées», «Communications» · «(2)»).

    The words are the live labels, whole — the bar never cuts one and never shortens one. A stylesheet can
    size a seat to a label's longest word or to its whole line, not to its two balanced lines: left to wrap by
    itself, a register's name took three or four lines in a seat that two would have filled. The bar breaks a
    label between these runs and nowhere else (v5/_shell.css §5), so a seat is never narrower than the longer
    run and a label is one line or two, never three.
    """
    words = str(label).split()
    if len(words) < 2:
        return [str(label)]
    head = min(
        range(1, len(words)),
        key=lambda cut: (max(len(" ".join(words[:cut])), len(" ".join(words[cut:]))), cut),
    )
    return [" ".join(words[:head]), " ".join(words[head:])]


#: Whether a phone's bar draws its labels on their two runs AT ONCE (below 30rem), or lets each stand on one line
#: while the row holds. A row that cannot hold its labels on one line makes some of them wrap — and a seat sized
#: for a line it no longer draws kept 30 px of air while «Communications» and «Espace entreprise» stood 4 px apart
#: beside it. So the bar is estimated, once, for the row of a 360 px phone: its labels on one line — 6.3 px a
#: character of Latin at 12 px, 5.6 px of Arabic at 14 px (measured on the live labels of the four languages) —
#: the air of each seat and «Menu»'s own seat. Over the row, every label of the bar stands on its two runs and each
#: seat asks for its longer run; under it — an Arabic bar, a bar of two entries — the labels keep their line.
BAR_ROW = 350
BAR_SEAT_AIR = 16
BAR_MENU_SEAT = 56
BAR_CHARACTER = 6.3
BAR_CHARACTER_ARABIC = 5.6


def _bar_stacks(labels: list) -> bool:
    """Whether the bar that holds these labels draws them on two runs on a phone (see ``BAR_ROW``)."""
    need = BAR_MENU_SEAT
    for label in labels:
        text = str(label)
        arabic = any(0x0600 <= ord(char) <= 0x06FF for char in text)
        need += len(text) * (BAR_CHARACTER_ARABIC if arabic else BAR_CHARACTER) + BAR_SEAT_AIR
    return need > BAR_ROW


#: Surfaces that belong to a role, not to everybody. Each is offered only to the role that can use
#: it — « un module non disponible ne se montre pas », and a menu item that answers 403 tells
#: somebody that something exists. A row may name several roles: any of them opens the surface (the
#: dispatch desk answers an operator and an administrator — helpdesk.views.dispatch).
ROLE_SURFACES: tuple[tuple[str | tuple[str, ...], str, str], ...] = (
    (roles.AUTHORISED_ACTOR, "selection", "selection:workspace"),
    (roles.COMPANY, "company", "companies:dashboard"),
    (roles.PROFESSIONAL, "helpdesk-queue", "helpdesk:queue"),
    ((roles.OPERATOR, roles.ADMINISTRATOR), "helpdesk-dispatch", "helpdesk:dispatch"),
)

ROLE_SURFACE_LABELS = {
    "selection": gettext_lazy("Processus assignés"),
    "company": gettext_lazy("Mon entreprise"),
    "helpdesk-queue": gettext_lazy("Demandes qui me sont confiées"),
    "helpdesk-dispatch": gettext_lazy("Désignation des professionnels"),
}

#: The role surfaces that are a SPACE of their own, with its own rail: the entry is the way there.
ROLE_SPACES: dict[str, str] = {"company": SPACE_COMPANY}


def _role_entries(user) -> list[tuple[str, Any, str]]:
    """
    The way BACK to a role's own surface.

    Each role lands on its own screen at sign-in, and each of those screens links here. None of
    them was linked FROM here — so an authorised actor who followed «Tableau de bord» once had no
    route back to the only surface their role exists for, short of signing in again. The modules
    could not fix this from their own side: they are not rendered on this page.

    Defensive by design. A deployment without one of these apps must not break the reserved area
    for everybody, so a route that does not resolve is simply not offered.
    """
    if not getattr(user, "is_authenticated", False):
        return []
    # One read of the account's roles for every row; a superuser is offered each surface, as
    # ``roles.has_role`` answers for it.
    return _role_surfaces(user, set() if user.is_superuser else roles.roles_of(user))


def _role_surfaces(user, held: set[str]) -> list[tuple[str, Any, str]]:
    """The role surfaces offered to an account whose roles are already read (``held``): ``_role_entries``'s rows,
    and where «Espace réservé» starts (``_person_space_start``) — one rule for both."""
    if not getattr(user, "is_authenticated", False):
        return []
    superuser = bool(getattr(user, "is_superuser", False))
    entries: list[tuple[str, Any, str]] = []
    for role, key, route in ROLE_SURFACES:
        wanted = {role} if isinstance(role, str) else set(role)
        if not (superuser or held & wanted):
            continue
        try:
            entries.append((key, ROLE_SURFACE_LABELS[key], reverse(route)))
        except NoReverseMatch:  # pragma: no cover - a module that is not installed
            continue
    return entries


# ---------------------------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------------------------
@dataclass
class CardItem:
    title: str
    url: str = ""
    meta: str = ""
    date: Any = None
    badge_label: str = ""
    badge_kind: str = ""
    lang: str = ""


@dataclass
class Card:
    key: str
    title: str
    icon: str
    available: bool = True
    count: int = 0
    count_label: str = ""
    badge_label: str = ""
    badge_kind: str = ""
    items: list[CardItem] = field(default_factory=list)
    url: str = ""
    url_label: str = ""
    empty_title: str = ""
    empty_text: str = ""
    empty_action_label: str = ""
    empty_action_url: str = ""


def _requests_card(user) -> Card:
    items = requests_for(user)
    return Card(
        key="requests",
        title=_("Mes demandes"),
        icon="list",
        count=len(items),
        count_label=ngettext("demande transmise", "demandes transmises", len(items)),
        items=[
            CardItem(
                title=i.title,
                url=i.url,
                meta=i.kind_label,
                date=i.created_at,
                badge_label=i.status_label,
                badge_kind=i.status_kind,
            )
            for i in items[:DASHBOARD_LATEST]
        ],
        url=reverse("portal:requests"),
        url_label=_("Toutes mes demandes"),
        empty_title=_("Aucune demande"),
        empty_text=_("Les demandes transmises depuis votre compte apparaîtront ici."),
    )


def _orientation_card(user) -> Card:
    sessions = pathway_sessions(user, present_first=1)
    completed = [s for s in sessions if s["is_completed"]]
    latest = (completed or sessions)[:1]
    items = []
    for row in latest:
        result = row["result"] or {}
        items.append(
            CardItem(
                title=result.get("title") or _("Questionnaire en cours"),
                url=reverse("portal:pathways"),
                meta=_("Pré-évaluation à caractère informatif — règles v%(version)s")
                % {"version": row["ruleset_version"]},
                date=row["date"],
                lang=result.get("lang", ""),
            )
        )
    return Card(
        key="orientation",
        title=_("Mon orientation"),
        icon="compass",
        count=len(completed),
        count_label=ngettext("pré-évaluation enregistrée", "pré-évaluations enregistrées", len(completed)),
        items=items,
        url=reverse("portal:pathways"),
        url_label=_("Mon parcours"),
        empty_title=_("Aucune pré-évaluation enregistrée"),
        empty_text=_("Le questionnaire d’orientation vous indique, à titre informatif, une famille de parcours."),
        empty_action_label=_("Commencer l’orientation"),
        empty_action_url=safe_reverse("orientation:start"),
    )


def _documents_card(user) -> Card:
    docs = documents_for(user)
    total = docs.count()
    return Card(
        key="documents",
        title=_("Mes documents"),
        icon="document",
        count=total,
        count_label=ngettext("document privé", "documents privés", total),
        items=[
            CardItem(
                title=d.original_name,
                meta=d.get_kind_display(),
                date=d.created_at,
                badge_label=d.get_scan_status_display(),
                badge_kind=SCAN_BADGES.get(d.scan_status, "neutral"),
            )
            for d in docs[:DASHBOARD_LATEST]
        ],
        url=reverse("portal:documents"),
        url_label=_("Tous mes documents"),
        empty_title=_("Aucun document"),
        empty_text=_("Ne téléversez que les documents qui vous sont demandés dans le cadre de votre parcours."),
    )


def _deadlines_card(user) -> Card:
    today = clock.today()
    open_rows = list(deadlines_for(user).open().order_by("due_on", "id"))
    overdue = sum(1 for d in open_rows if d.is_overdue(today))
    items = []
    for deadline in open_rows[:DASHBOARD_LATEST]:
        presented = present_deadline(deadline, today)
        items.append(
            CardItem(
                title=deadline.title,
                meta=presented["kind_label"],
                date=deadline.due_on,
                badge_label=presented["badge_label"],
                # a date past due speaks azione on a dashboard, as on the person's (plan §1.2: terracotta, never the
                # red of a refusal); the deadlines page keeps its own register (W3-C)
                badge_kind="overdue" if presented["badge_kind"] == "error" else presented["badge_kind"],
            )
        )
    return Card(
        key="deadlines",
        title=_("Mes échéances"),
        icon="calendar",
        count=len(open_rows),
        count_label=ngettext("échéance à venir", "échéances à venir", len(open_rows)),
        badge_label=(_("%(n)d en retard") % {"n": overdue}) if overdue else "",
        badge_kind="overdue",
        items=items,
        url=reverse("portal:deadlines"),
        url_label=_("Toutes mes échéances"),
        empty_title=_("Aucune échéance"),
        empty_text=_("Les dates qui vous sont communiquées par l’équipe apparaîtront ici."),
    )


def _messages_card(user) -> Card:
    messages = inbox(user)
    total = messages.count()
    unread = unread_count(user)
    return Card(
        key="messages",
        title=_("Communications"),
        icon="mail",
        count=total,
        count_label=ngettext("communication reçue", "communications reçues", total),
        badge_label=(ngettext("%(n)d non lue", "%(n)d non lues", unread) % {"n": unread}) if unread else "",
        badge_kind="primary",
        items=[
            CardItem(
                title=m.subject,
                url=reverse("portal:message_detail", kwargs={"pk": m.pk}),
                date=m.created_at,
                badge_label="" if m.is_read else _("Non lue"),
                badge_kind="primary",
            )
            for m in messages[:DASHBOARD_LATEST]
        ],
        url=reverse("portal:messages"),
        url_label=_("Toutes mes communications"),
        empty_title=_("Aucune communication"),
        empty_text=_("Les messages que l’équipe vous adresse apparaîtront ici."),
    )


def _organisation_card(user) -> Card:
    rows = organisations_for(user)
    return Card(
        key="organisation",
        title=_("Mon organisation"),
        icon="building",
        count=len(rows),
        count_label=ngettext("organisation rattachée", "organisations rattachées", len(rows)),
        items=[
            CardItem(
                title=row["name"],
                meta=" · ".join(part for part in (row["kind_label"], row["place"]) if part),
                badge_label=row["role_label"],
                badge_kind="info",
            )
            for row in rows
        ],
        url=safe_reverse("accounts:profile"),
        url_label=_("Mon profil"),
        empty_title=_("Aucune organisation rattachée"),
        empty_text=_("Le rattachement de votre compte à une organisation est effectué par l’équipe du projet."),
    )


_CARD_TITLES: dict[str, tuple[Callable[[], str], str]] = {
    "requests": (lambda: _("Mes demandes"), "list"),
    "orientation": (lambda: _("Mon orientation"), "compass"),
    "documents": (lambda: _("Mes documents"), "document"),
    "deadlines": (lambda: _("Mes échéances"), "calendar"),
    "messages": (lambda: _("Communications"), "mail"),
    "organisation": (lambda: _("Mon organisation"), "building"),
}


def _safe_card(key: str, builder: Callable[[Any], Card], user) -> Card:
    try:
        return builder(user)
    except SIBLING_ERRORS:
        # No personal data in logs: only the card key and the exception type.
        log.exception("portal card unavailable", extra={"event": "portal.card_unavailable", "card": key})
        title, icon = _CARD_TITLES[key]
        return Card(key=key, title=title(), icon=icon, available=False)


def _wants_orientation(user) -> bool:
    """Whether an account is offered the orientation — its card on the bridge, the legacy pre-assessment on a person's
    dashboard: by its account type and its roles, or because it already holds a session (deny by default)."""
    wants = getattr(user, "account_type", "") in ORIENTATION_ACCOUNT_TYPES or (
        not user.is_superuser and roles.has_role(user, roles.PERSON, roles.PROFESSIONAL)
    )
    return wants or _has_orientation_sessions(user)


def card_builders_for(user) -> list[tuple[str, Callable[[Any], Card]]]:
    """Which cards an account gets — driven by its account type and roles (deny by default)."""
    builders: list[tuple[str, Callable[[Any], Card]]] = [("requests", _requests_card)]
    if _wants_orientation(user):
        builders.append(("orientation", _orientation_card))
    builders += [("documents", _documents_card), ("deadlines", _deadlines_card), ("messages", _messages_card)]
    if shows_organisation_card(user) or user.memberships.exists():
        builders.append(("organisation", _organisation_card))
    return builders


def bridge_cards(user) -> list[Card]:
    """
    The card grid of the accounts that are not a person — company, institution, university, professional — kept as
    a bridge until their own workspaces exist (templates/portal/dashboard.html). A person's dashboard never draws
    it, so it is never built for a person (the platform map's F9, W3-B): six presenters and their queries ran on
    every person's dashboard for a grid nobody saw.
    """
    return [_safe_card(key, builder, user) for key, builder in card_builders_for(user)]


def is_person_account(user) -> bool:
    """The dashboard of a person: the account type, or the person's role on an account of another type (the QA
    persona «personne avec dossier» is typed company and holds the person's role — DL54-59)."""
    return (getattr(user, "account_type", "") == "person") or roles.has_role(user, roles.PERSON)


def _has_orientation_sessions(user) -> bool:
    model = _get_model("orientation", "OrientationSession")
    if model is None:
        return False
    try:
        return model.objects.filter(user=user).exists()
    except FieldError:
        return False


#: The case lifecycle as a person reads it. Not the eleven internal states — a person does not need
#: to know that SUSPENDED and CLOSED exist until one applies to them — but the spine of the model,
#: which is also the spine of the public site: need, skills, training, legal pathway, entry,
#: inclusion. ``side`` says which shore is answerable, so the sequence can draw the crossing.
JOURNEY_STEPS: tuple[tuple[str, str, object], ...] = (
    ("draft", "morocco", gettext_lazy("Votre situation et votre objectif")),
    ("oriented", "morocco", gettext_lazy("Pré-évaluation et parcours possibles")),
    ("training", "morocco", gettext_lazy("Préparation et formation avant le départ")),
    ("admin_process", "italy", gettext_lazy("Procédures auprès des autorités compétentes")),
    ("pre_departure", "italy", gettext_lazy("Préparation du départ")),
    ("entered", "italy", gettext_lazy("Arrivée et premières démarches")),
    ("post_entry", "italy", gettext_lazy("Accompagnement et inclusion")),
)


def journey_for(case) -> list[dict]:
    """
    The case lifecycle rendered as a sequence, with the current step marked.

    A person asks "where am I", and the honest answer is a position in a named sequence — not a
    percentage, and not a state machine diagram.
    """
    if case is None:
        return []
    from cases.models import CaseStatus

    reached = {CaseStatus.DRAFT: 0, CaseStatus.ORIENTED: 1, CaseStatus.REVIEW_REQUIRED: 1}
    for index, (status, _side, _label) in enumerate(JOURNEY_STEPS):
        reached.setdefault(status, index)
    current_index = reached.get(case.status, 0)
    # The frontier MA→IT sits before the first step of the Italian side (design V4 JourneyRail).
    first_italy = next((i for i, (_s, side, _l) in enumerate(JOURNEY_STEPS) if side == "italy"), None)
    return [
        {
            "label": label,
            "side": side,
            "is_current": index == current_index,
            "frontier": index == first_italy,
            "detail": "",
            "actor": "",
        }
        for index, (status, side, label) in enumerate(JOURNEY_STEPS)
    ]


def active_case(user):
    """The person's case file, or None. Authorisation is applied in the queryset, as always."""
    from cases.models import CaseFile

    return CaseFile.objects.readable_by(user).filter(person=user).active().order_by("-created_at").first()


#: Scan status -> the seven user-visible document states of art direction A §13.3. The scanner
#: reports on a file; the person needs to know what it means for their file, which is not the same
#: question. Never a raw technical status in front of someone assembling a legal dossier.
#: `ScanStatus` -> the `.state--*` modifier of static/css/register.css.
#:
#: "skipped" is not a scan status and never was — `ScanStatus` reads NOT_CONFIGURED, PENDING,
#: CLEAN, INFECTED, ERROR — so that key had matched nothing since the status was renamed, and an
#: unscanned file fell through to the default. It now says so by name.
DOCUMENT_STATES = {
    "not_configured": "review",
    "pending": "review",
    "clean": "valid",
    "infected": "invalid",
    "error": "review",
}


def _scan_chip(status: str) -> object:
    """
    The scanner's state as ONE WORD, for the chip on the dashboard.

    Imported here and not at the top of the module for the reason every other reference to the
    documents app in this file is late: the portal renders without that sibling installed, and a
    module-level import would make the whole dashboard depend on it. If it is missing, the status
    key is shown as it is — ugly, and still true.
    """
    try:
        from documents.requirements import scan_chip
    except SIBLING_ERRORS:
        return status
    return scan_chip(status)


def _safe_rows(key: str, builder, user) -> list[dict]:
    """
    Rows for one register of the dashboard, or an empty list.

    A sibling app that disappears or changes shape must produce an honest empty region, never a 500
    on the page a person opens to find their next action. The cards this replaced had that guarantee
    through ``_safe_card``; the registers need it just as much, and for the same reason.

    No personal data in the log: the register key and the exception type, nothing else.
    """
    try:
        return builder(user)
    except SIBLING_ERRORS:
        log.exception("portal register unavailable", extra={"event": "portal.register_unavailable", "register": key})
        return []


def _dashboard_documents(user) -> list[dict]:
    return [
        {
            "label": document.original_name,
            "detail": document.get_kind_display(),
            "state": DOCUMENT_STATES.get(document.scan_status, "review"),
            # The raw member, for the chip's register (core.chips, keyed on documents.ScanStatus):
            # the CSS word above is a colour with extra steps and cannot say what the scan found.
            "scan_status": document.scan_status,
            # The chip word, not the field's verbose label: one of those labels is a whole
            # sentence and this slot is drawn on one line. See documents.requirements.SCAN_CHIPS.
            "state_label": _scan_chip(document.scan_status),
        }
        for document in documents_for(user)[:DASHBOARD_LATEST]
    ]


def _dashboard_messages(user) -> list[dict]:
    return [
        {
            "subject": message.subject,
            "date": message.created_at,
            "is_unread": message.read_at is None,
            "url": safe_reverse("portal:message_detail", message.pk),
        }
        for message in inbox(user)[:DASHBOARD_LATEST]
    ]


def _dashboard_deadlines(user) -> list[dict]:
    from documents.requirements import due_urgency

    rows = []
    for deadline in deadlines_for(user).open().order_by("due_on", "id")[:DASHBOARD_LATEST]:
        urgency = due_urgency(deadline.due_on)
        rows.append(
            {
                "pk": deadline.pk,
                "title": deadline.title,
                "date": deadline.due_on,
                "urgency": urgency,
                "word": _due_word(urgency),
                "kind_label": deadline.get_kind_display(),
                "source_note": deadline.source_note,
            }
        )
    return rows


def _due_word(urgency: str) -> str:
    """A due date's word beside its glyph and its date — «Bientôt», «En retard» — never a colour alone (plan §1.2:
    «soon» is attesa, «overdue» is azione); the catalogue's words of the deadlines page, nothing new."""
    return {"soon": _("Bientôt"), "overdue": _("En retard")}.get(urgency, "")


def _with_meter(progress: dict | None) -> dict | None:
    """The five-notch meter of the file panel (design V4 §3.4.2): one notch per element up to
    eight, filled in the real proportion — the words beside it carry the exact count."""
    if not progress:
        return progress
    total = progress.get("total") or 0
    notches = min(total, 8) if total else 0
    filled = round(progress.get("done", 0) / total * notches) if total else 0
    return {**progress, "notches": range(notches), "filled": filled}


#: How many of the file's pieces the dashboard lists — every piece the person must act on is listed, then the ones
#: in somebody else's hands until the list holds this many; the register holds the rest («Voir mes documents»).
DASHBOARD_PIECES = 5


def _dashboard_pieces(user, case, skip: str = "") -> dict:
    """
    The file's pieces as the dashboard shows them — the same presenter and the same authorisation as the register
    itself (documents.presenters.register_for_case):

    * ``marks``: one per piece, the register's order — «il registro» drawn as the chips' marks, decoration over the
      counts' words (``counts``, the register's own);
    * ``rows``: every piece the person must act on (an open state, the person answerable), then the pieces in
      somebody else's hands — filed, in review, or asked of another actor — up to DASHBOARD_PIECES; a settled piece
      is counted, not listed;
    * ``now``: the row of the piece the NowPanel draws (``skip``), which no list draws again — one piece, drawn once.

    «Il registro» (O62): the pieces by who holds them — the colour is the group, the shape is the state. The group
    words are the catalogue's until the copy review signs «À vous · En cours · Réglées» (plan §1.18 D15): «À faire»
    and «En cours» (the checklist's own states), «Valide» (the piece's).
    """
    from cases.models import ChecklistStatus
    from documents import presenters
    from documents.models import OPEN_STATES, RequirementState

    if case is None:
        return {}
    register = presenters.register_for_case(user, case)
    rows = register["rows"]
    if not rows:
        return {}
    to_act = [row for row in rows if row["is_for_the_person"] and row["state"] in OPEN_STATES]
    settled = [row for row in rows if row["state"] == RequirementState.VALID]
    in_hand = [row for row in rows if row not in to_act and row not in settled]
    now = next((row for row in rows if skip and row["id"] == skip), None)
    yours = [row for row in to_act if row is not now]
    others = [row for row in in_hand if row is not now]
    shown = yours + others[: max(0, DASHBOARD_PIECES - len(yours))]
    for row in shown:
        row["is_yours"] = row in yours
        row["due_word"] = _due_word(row["urgency"])
        row["words"] = _data_lang(getattr(row["requirement"], "language", ""))
    groups = [
        {"key": key, "label": label, "states": [row["state"] for row in members]}
        for key, label, members in (
            ("to-act", ChecklistStatus.PENDING.label, to_act),
            ("in-hand", ChecklistStatus.IN_PROGRESS.label, in_hand),
            ("settled", RequirementState.VALID.label, settled),
        )
        if members
    ]
    return {
        "counts": register["counts"],
        "groups": groups,
        "rows": shown,
        "more": len(yours) + len(others) - len(shown),
        "now": now,
    }


def _dashboard_academy(user) -> dict | None:
    """The person's current enrolment, if any — real progress only, never an invented one."""
    try:
        from academy import services as academy_services
    except ImportError:  # pragma: no cover - the Academy is optional in a deployment
        return None
    enrolments = list(academy_services.enrolments_for(user)[:1])
    if not enrolments:
        return None
    enrolment = enrolments[0]
    return {
        "course": enrolment.course.title,
        "status": enrolment.status,
        "status_label": enrolment.get_status_display(),
        "url": safe_reverse("academy:enrolment", enrolment.uuid) if safe_reverse("academy:catalogue") else "",
    }


def _dashboard_assessment(cards, assessment) -> dict | None:
    """
    The pre-assessment shown on the dashboard: the outcome, the rules behind it, and its sources.

    Two paths, for one transition. The questionnaire now opens a ``CaseFile`` and freezes a
    ``PathwayAssessment``, which is the path that matters. A person who completed the questionnaire
    BEFORE the case file existed still has only an ``OrientationSession``, and must still see their
    result, so the legacy session is read as a fallback until those sessions age out.

    Both paths carry the ruleset version and the evaluation date, because an outcome without them
    cannot be reproduced and should not be trusted. Only the first can carry SOURCES, and that is the
    whole difference between the two: an outcome that cites the provisions behind it is a finding,
    and one that cannot is an opinion. Neither path ever prints a word that could be read as an
    administrative decision.
    """
    if assessment is not None:
        return {
            "outcome_kind": assessment.outcome.replace("_requirement", "").replace("review_required", "review"),
            "outcome_label": assessment.get_outcome_display(),
            "rationale": assessment.rationale,
            "ruleset_version": assessment.ruleset_version,
            "assessed_at": assessment.assessed_at,
            "sources": assessment.sources,
            # The rules are named, not just counted: "three rules in force were applied" is a claim,
            # and a person disputing the outcome needs to be able to ask about a specific one.
            "applied_rules": [
                {"rule_id": applied.get("rule_id", ""), "message": applied.get("message", "")}
                for applied in (assessment.applied_rules or [])
            ],
            "missing_count": len(assessment.missing_requirements or []),
        }

    # Read from the card already built rather than querying again: ``pathway_sessions`` is the
    # dashboard's most expensive call and it must run once per request, which
    # test_pathways_page_presents_only_the_requested_page guards.
    card = next((c for c in cards if c.key == "orientation" and c.available), None)
    if card is None or not card.items:
        return None
    item = card.items[0]
    version = ""
    if item.meta:
        _, _, tail = item.meta.rpartition("v")
        version = tail.strip()
    return {
        # A legacy session records a pathway family, not one of the five outcome kinds: presenting
        # it as an outcome would claim more than the row contains.
        "outcome_kind": "possible",
        "outcome_label": item.title,
        "rationale": "",
        "ruleset_version": version,
        "assessed_at": item.date,
        "sources": [],
        "applied_rules": [],
        "missing_count": 0,
    }


#: The glyph of each section of a person's dashboard — the registry's symbol of its domain (apps/core/icons.py), the
#: same as the rail's entry for that domain: one concept, one glyph (plan §1.7).
DASHBOARD_GLYPHS: dict[str, str] = {
    "journey": icons.concept("nav", "pathways"),
    "file": icons.concept("nav", "cases"),
    "pieces": icons.concept("card", "documents"),
    "dates": icons.concept("card", "deadlines"),
    "messages": icons.concept("card", "messages"),
    "academy": icons.concept("nav", "academy"),
    "assessment": icons.concept("journey", "oriented"),
    "deposits": "history",
}


# ---- The NowPanel: the person's dashboard's one raised panel, chosen by the system --------------------------
#: Its four variants (plan §1.15 item 1): the system orders priority — nobody arranges a board.
NOW_YOURS = "yours"  # «à vous» — the next action is the person's
NOW_THIRD = "third"  # «en attente d'un tiers» — it is in somebody else's hands
NOW_NOTHING = "nothing"  # «rien à faire» — the file asks nothing of anybody now
NOW_NO_CASE = "no-case"  # «pas encore de dossier» — the questionnaire opens the file


def _data_lang(lang: str) -> dict[str, str]:
    """The language of a record's own words when it is not the page's: a piece's title is written in French and stays
    French on an Arabic page, isolated so its direction and its punctuation hold (gate-0 A6)."""
    from django.utils import translation

    current = (translation.get_language() or "fr").split("-")[0]
    if not lang or lang == current:
        return {"lang": "", "dir": ""}
    try:
        bidi = translation.get_language_info(lang)["bidi"]
    except KeyError:
        bidi = False
    return {"lang": lang, "dir": "rtl" if bidi else "ltr"}


def _overdue_deadline(deadlines: list[dict], action) -> dict | None:
    """An overdue date of the account takes over the NowPanel (plan §1.15 item 1) — unless the next action is already
    overdue or a blocking outcome stops the path: the precedence's first rungs stay first."""
    if action is not None and action.urgency in ("overdue", "blocked"):
        return None
    return next((row for row in deadlines if row["urgency"] == "overdue"), None)


def _now_acts(case, action, piece: dict | None) -> tuple[dict | None, dict | None]:
    """
    The NowPanel's acts: ONE primary — the act itself, on the obligation's own page — or none when nothing is the
    person's to do; in somebody else's hands, a quiet way to read the piece. The words are the register's
    (components/document_row.html) and the catalogue's: nothing new is written here.

    A piece whose filing the Conditions gate blocks is read on its own page («Consulter», the dashboard's rows say
    the same), which states the gate; the panel's note says why (``_now_gate_note``). Never a button that promises
    an act its target cannot do: the terms page has nothing to accept until the acceptance flow exists (G1).
    """
    from core.links import public_url

    if action.is_for_someone_else:
        if action.kind == "piece" and action.url:
            return None, {"label": _("Consulter"), "url": action.url}
        return None, None
    if action.kind == "piece":
        if piece is not None and piece.get("may_file"):
            label = _("Remplacer la pièce") if piece.get("current") else _("Déposer la pièce")
            return {"label": label, "url": action.url}, None
        return ({"label": _("Consulter"), "url": action.url} if action.url else None), None
    if action.kind == "item":
        # a checklist item has no page of its own: it is worked from the case file, which lists it
        url = public_url("cases:detail", case.reference)
        return ({"label": _("Continuer"), "url": url} if url else None), None
    if action.kind == "outcome" and action.url:
        return {"label": _("Voir le détail de la pré-évaluation"), "url": action.url}, None
    if action.url:
        return {"label": action.cta_label or _("Continuer"), "url": action.url}, None
    return None, None


#: The registry's glyph of what the NowPanel is about (apps/core/icons.py): a piece, a checklist item of the file,
#: the pre-assessment's outcome, the orientation.
_NOW_GLYPHS = {
    "piece": ("card", "documents"),
    "item": ("nav", "cases"),
    "outcome": ("journey", "oriented"),
    "orientation": ("card", "orientation"),
}


def _now_gate_note(action, piece: dict | None) -> str:
    """The note of a NowPanel whose piece the Conditions gate blocks — the register's own words
    (templates/components/document_row.html) —, or ''."""
    if action.kind == "piece" and piece is not None and piece.get("action_blocked"):
        return _("Acceptation des Conditions d’utilisation requise.")
    return ""


def _now_holder(assignments) -> dict[str, str] | None:
    """Whose hands the file is in, for a NowPanel that asks nothing («rien à faire»): the file's most recent live
    assignment (``cases.services.responsible_for``, newest first) — its role, and its organisation when it has one
    (a record's own words, isolated by the partial), as the file's own strip says them («Qui intervient sur ce
    dossier»). None when nobody is assigned."""
    assignment = next(iter(assignments or ()), None)
    if assignment is None:
        return None
    organisation = assignment.organisation.name if assignment.organisation_id else ""
    return {"actor": assignment.role, "label": assignment.get_role_display(), "organisation": organisation}


#: The words of a record whose language the data does not hold — a date the team wrote, its source note —: their
#: direction is the text's own (``dir="auto"``), so on an Arabic page a French title keeps its brackets and its final
#: point where it wrote them, and its box stands on the panel's reading edge.
_OWN_WORDS = {"lang": "", "dir": "auto"}


def _now_base() -> dict[str, Any]:
    """Every key the NowPanel's partial reads (templates/portal/partials/now_panel.html), empty."""
    return {
        "takeover": "",
        "words": {"lang": "", "dir": ""},
        "text_label": "",
        "state": None,
        "due": None,
        "responsible": None,
        "note": "",
        "primary": None,
        "secondary": None,
        "piece_id": "",
        "need_ref": "",
        "deadline_pk": None,
    }


def now_panel(
    user, case, action, *, takeover: dict | None = None, piece: dict | None = None, assignments=None
) -> dict[str, Any]:
    """
    What the person's dashboard puts first, in its one raised panel: the next action with its piece, its date and
    who answers for it, and the ONE primary that does it — composed from ``cases.services.next_action`` (T1) and
    the account's dates, never chosen by the person and never remembered (plan §1.15).

    The variant says whose move it is: «à vous» (NOW_YOURS), «en attente d'un tiers» (NOW_THIRD), «rien à faire»
    (NOW_NOTHING — with whose hands the file is in, from the file's live ``assignments``), «pas encore de dossier»
    (NOW_NO_CASE); an overdue date takes the panel over (``takeover``): its title and its source note — under the
    deadlines page's «Origine :» — are the team's own words, drawn in their own direction.
    """
    from core.links import public_url
    from documents.requirements import due_urgency, state_label

    base = _now_base()
    if takeover is not None:
        deadlines_url = public_url("portal:deadlines")
        return {
            **base,
            "variant": NOW_YOURS,
            "takeover": "overdue",
            "eyebrow": _("Votre prochaine action"),
            "glyph": icons.concept("due", "overdue"),
            "title": takeover["title"],
            "text": takeover["source_note"],
            "text_label": _("Origine :") if takeover["source_note"] else "",
            "words": dict(_OWN_WORDS),
            "due": {"date": takeover["date"], "urgency": "overdue", "word": _due_word("overdue")},
            "primary": {"label": _("Toutes mes échéances"), "url": deadlines_url} if deadlines_url else None,
            "deadline_pk": takeover["pk"],
        }
    if case is None:
        start = public_url("orientation:start")
        return {
            **base,
            "variant": NOW_NO_CASE,
            "eyebrow": _("Votre prochaine action"),
            "glyph": icons.concept("card", "orientation"),
            "title": _("Le questionnaire d’orientation"),
            "text": _(
                "Vous n’avez pas encore de dossier. Il s’en ouvre un lorsque vous terminez le questionnaire "
                "d’orientation, et il conserve alors votre résultat, votre liste de pièces et les personnes "
                "responsables de chaque étape."
            ),
            "primary": {"label": _("Commencer le questionnaire"), "url": start} if start else None,
        }
    if action is None:
        return {
            **base,
            "variant": NOW_NOTHING,
            "eyebrow": _("Prochaine étape"),
            "glyph": icons.concept("nav", "cases"),
            "title": _("Aucune action ne vous est demandée pour l’instant."),
            "text": "",
            "responsible": _now_holder(assignments),
        }
    state = None
    if action.kind == "piece" and action.state:
        state = {"value": action.state, "producer": "documents.RequirementState", "label": state_label(action.state)}
    elif action.kind == "item" and action.state:
        from cases.models import ChecklistStatus

        state = {
            "value": action.state,
            "producer": "cases.ChecklistStatus",
            "label": ChecklistStatus(action.state).label,
        }
    due = None
    if action.due_date:
        urgency = due_urgency(action.due_date, overdue=action.urgency == "overdue")
        due = {"date": action.due_date, "urgency": urgency, "word": _due_word(urgency)}
    primary, secondary = _now_acts(case, action, piece)
    yours = not action.is_for_someone_else
    domain, key = _NOW_GLYPHS.get(action.kind, ("nav", "cases"))
    return {
        **base,
        "variant": NOW_YOURS if yours else NOW_THIRD,
        "takeover": "overdue" if action.urgency == "overdue" else "",
        "eyebrow": _("Votre prochaine action") if yours else _("Prochaine étape"),
        "glyph": icons.concept(domain, key),
        "title": action.label,
        "text": action.detail,
        "words": _data_lang(action.lang),
        "state": state,
        "due": due,
        "responsible": {"actor": action.responsible_actor, "label": action.get_responsible_display()},
        "note": _now_gate_note(action, piece) if yours else _("Cette étape ne dépend pas de vous."),
        "primary": primary,
        "secondary": secondary,
        "piece_id": action.piece_id,
    }


def _safe_pieces(user, case, skip: str) -> dict:
    """The dashboard's pieces, or an honest empty region when the documents sibling changed under us."""
    try:
        return _dashboard_pieces(user, case, skip)
    except SIBLING_ERRORS:
        log.exception(
            "portal register unavailable", extra={"event": "portal.register_unavailable", "register": "pieces"}
        )
        return {}


# ---- The company's dashboard (design V5, W3-B step 2) ---------------------------------------------------------
#: The glyph of each section of the company's dashboard — the rail's own glyph for that page (icons.COMPANY_NAV):
#: one concept, one glyph (plan §1.7).
COMPANY_GLYPHS: dict[str, str] = {
    "company": icons.concept("company_nav", "profile"),
    "needs": icons.concept("company_nav", "needs"),
    "messages": icons.concept("company_nav", "messages"),
}

#: How many of the company's needs the dashboard lists — its own drafts first, then the needs in somebody else's
#: hands, then the closed ones; the ledger counts them all and the register («Tous mes besoins») lists them all.
DASHBOARD_NEEDS = DASHBOARD_PIECES


def _action_need(action, needs):
    """The need a company's next action is about — the need whose page its act opens — or None (the declaration, the
    verification, the needs under review: no need of their own)."""
    if action is None or not action.url:
        return None
    for need in needs:
        if action.url in (
            safe_reverse("companies:need_detail", need.reference),
            safe_reverse("companies:need_edit", need.reference),
        ):
            return need
    return None


def company_now_panel(company, action, need=None, *, transmit: bool = False) -> dict[str, Any]:
    """
    The company dashboard's NowPanel — the person's raised plane, with the company's one next action
    (``companies.services.next_action``, unchanged): «à vous» when the act is the company's — declare the company,
    complete or transmit a need, express the first one — with its ONE primary, the presenter's own words; «en attente
    d'un tiers» when the project team verifies the company or examines the needs (no primary); «rien à faire». The
    need the act is about lends its state and its reference, and is drawn here only (``need_ref``).

    ``transmit`` — the account may transmit that need now (``can(user, "submit", need)``): the primary is then the
    need page's own act, its POST form and its words («Transmettre au projet»), with the need in view — its title,
    its state, its reference —, and «Ouvrir le besoin» stays beside it, quiet, for a last reading. One verb, one
    click; the link is never relabelled as the act (the W3-B review's m4).
    """
    base = _now_base()
    if action is None:
        return {
            **base,
            "variant": NOW_NOTHING,
            "eyebrow": _("Prochaine étape"),
            "glyph": COMPANY_GLYPHS["needs"],
            "title": _("Aucune action ne vous est demandée pour l’instant."),
            "text": "",
        }
    yours = not action.is_for_someone_else
    state = None
    if need is not None:
        state = {"value": need.status, "producer": "companies.NeedStatus", "label": need.get_status_display()}
    about_needs = need is not None or (company is not None and company.is_verified)
    primary = {"label": action.cta_label or _("Continuer"), "url": action.url} if yours and action.url else None
    secondary = None
    submit_url = safe_reverse("companies:need_submit", need.reference) if transmit and need is not None else ""
    if yours and submit_url:
        primary, secondary = {"label": _("Transmettre au projet"), "url": submit_url, "method": "post"}, primary
    return {
        **base,
        "variant": NOW_YOURS if yours else NOW_THIRD,
        "eyebrow": _("Votre prochaine action") if yours else _("Prochaine étape"),
        "glyph": COMPANY_GLYPHS["needs" if about_needs else "company"],
        "title": action.label,
        "text": action.detail,
        "state": state,
        "responsible": {
            "actor": action.responsible_actor,
            "label": _("Votre entreprise") if yours else action.get_responsible_display(),
        },
        "note": "" if yours else _("Cette étape ne dépend pas de vous."),
        "primary": primary,
        "secondary": secondary,
        "need_ref": need.reference if need is not None else "",
    }


def _company_needs(needs, skip=None) -> dict[str, Any]:
    """
    «Il registro» of the company's needs — by who holds them, as the person's pieces (O62: the colour is the group,
    the shape is the state): to act (its drafts), in hand (transmitted, under review, taken over, on hold — the
    project's or an actor's), closed (closed, withdrawn). The group words are the catalogue's: «À faire», «En cours»
    (the checklist's own states, as on the person's dashboard) and «Clos» (the need's). Then the rows, in that order,
    up to DASHBOARD_NEEDS — the need of the NowPanel (``skip``) is drawn there and only there.
    """
    from cases.models import ChecklistStatus
    from companies.models import NeedStatus

    settled_states = (NeedStatus.CLOSED, NeedStatus.WITHDRAWN)
    to_act = [need for need in needs if need.status == NeedStatus.DRAFT]
    settled = [need for need in needs if need.status in settled_states]
    in_hand = [need for need in needs if need.status != NeedStatus.DRAFT and need.status not in settled_states]
    groups = [
        {"key": key, "label": label, "states": [need.status for need in members]}
        for key, label, members in (
            ("to-act", ChecklistStatus.PENDING.label, to_act),
            ("in-hand", ChecklistStatus.IN_PROGRESS.label, in_hand),
            ("settled", NeedStatus.CLOSED.label, settled),
        )
        if members
    ]
    ordered = [need for need in to_act + in_hand + settled if need is not skip]
    return {"groups": groups, "rows": ordered[:DASHBOARD_NEEDS], "more": max(0, len(ordered) - DASHBOARD_NEEDS)}


def company_dashboard(company, needs, action, *, user=None) -> dict[str, Any]:
    """
    What the company's dashboard draws beside the workspace's own context (design V5, W3-B step 2): the NowPanel,
    the needs by who holds them and the sections' glyphs. Read-only: the company app decides what the account may
    see and do (``companies.services``, ``companies.policies``), this only composes it — the NowPanel offers to
    transmit a need only when the next action opens that need's page and ``user`` may submit it now.
    """
    need = _action_need(action, needs)
    transmit = bool(
        user is not None
        and need is not None
        and action.url == safe_reverse("companies:need_detail", need.reference)
        and can(user, "submit", need)
    )
    return {
        "now": company_now_panel(company, action, need, transmit=transmit),
        "needs_ledger": _company_needs(needs, skip=need) if needs else {},
        "glyphs": COMPANY_GLYPHS,
    }


#: Two figures and the word between them — «0 sur 5», «0 من 5», «0 of 5» — kept on one line.
_FIGURES = re.compile(r"(\d+) (\S+) (\d+)")


def _progress_words(progress: dict | None) -> str:
    """The file's progress in the catalogue's words («%(done)s sur %(total)s éléments complétés»), its two figures
    and the word between them tied by no-break spaces: in the summary strip's narrow cell the Arabic line left its
    total alone on the next line («العناصر المكتملة: 0 من» / «5»). Nothing else changes: no word, no digit."""
    if not progress or not progress.get("total"):
        return ""
    words = _("%(done)s sur %(total)s éléments complétés") % {"done": progress["done"], "total": progress["total"]}
    return _FIGURES.sub("\\1\u00a0\\2\u00a0\\3", words)


def _bridge_space(user) -> dict[str, str] | None:
    """
    Where the work of an account that is not a person lives, for the bridge's one quiet link (the W3-B review's m10):
    the account's first role surface, named as the rail names it — another space by the space's own name («Espace
    entreprise»), a role's register by its entry («Processus assignés», «Demandes qui me sont confiées»,
    «Désignation des professionnels»). None for an account that holds none (an institution, a university): the
    page claims nothing the system does not know.
    """
    held = roles.roles_of(user)
    surfaces = _role_surfaces(user, held)
    if not surfaces:
        return None
    key, label, url = surfaces[0]
    if key in ROLE_SPACES:
        label = shell_space(user, ROLE_SPACES[key], held=held)["label"]
    return {"label": str(label), "url": url}


def dashboard_context(user) -> dict[str, Any]:
    """
    Everything the dashboard shows — real rows of THIS account or an explicit empty state.

    A person's dashboard (design V5, W3-B): the NowPanel (``now``) composed from the one next action (T1) and the
    account's dates; the journey; the file's facts; its pieces, each drawn once; the dates and the communications;
    what is secondary folds. The card grid is built only for the accounts that draw it (``bridge_cards``, F9).
    """
    from cases import services as case_services

    person = is_person_account(user)
    case = active_case(user)
    assessment = case_services.latest_assessment(case) if case else None
    action = case_services.next_action(case, reader=user) if case else None
    responsible = case_services.responsible_for(case) if case else []
    progress = case_services.progress(case) if case else None
    deadlines = _safe_rows("deadlines", _dashboard_deadlines, user)
    space = None
    if person:
        takeover = _overdue_deadline(deadlines, action)
        pieces = _safe_pieces(user, case, "" if takeover or action is None else action.piece_id)
        now = now_panel(user, case, action, takeover=takeover, piece=pieces.get("now"), assignments=responsible)
        if takeover is not None:
            deadlines = [row for row in deadlines if row is not takeover]
        cards: list[Card] = []
        # the legacy pre-assessment (an orientation session from before the case file) is read from its card alone
        legacy = (
            [_safe_card("orientation", _orientation_card, user)]
            if assessment is None and _wants_orientation(user)
            else []
        )
    else:
        pieces, now, cards = {}, None, bridge_cards(user)
        legacy = cards
        space = _bridge_space(user)
    return {
        "cards": cards,
        "notices": notices_for(user),
        "unread_count": unread_count(user),
        "case": case,
        "responsible": responsible,
        "progress": progress,
        "progress_words": _progress_words(progress),
        "next_action": action,
        "now": now,
        "space": space,
        "journey": journey_for(case),
        "assessment": _dashboard_assessment(legacy, assessment),
        "documents": _safe_rows("documents", _dashboard_documents, user),
        "pieces": pieces,
        "academy": _safe_rows("academy", _dashboard_academy, user),
        "messages_list": _safe_rows("messages", _dashboard_messages, user),
        "deadlines": deadlines,
        "orientation_url": safe_reverse("orientation:start"),
        "documents_url": safe_reverse("portal:documents"),
        "deadlines_url": safe_reverse("portal:deadlines"),
        "messages_url": safe_reverse("portal:messages"),
        "case_url": safe_reverse("cases:detail", case.reference) if case else "",
        "pathways_url": safe_reverse("portal:pathways"),
        "portal_context": case.reference if case else "",
        "is_person": person,
        "glyphs": DASHBOARD_GLYPHS,
        "account": {
            # ``get_full_name()`` falls back to the e-mail address: never print the address twice.
            "name": (getattr(user, "full_name", "") or "").strip(),
            "email": user.email,
            "type_label": user.get_account_type_display(),
            "last_login": user.last_login,
            "profile_url": safe_reverse("accounts:profile"),
            "mfa_url": safe_reverse("mfa_index"),
            "backoffice_url": safe_reverse("admin:index") if user.is_staff else "",
        },
    }


def reassess_person(user, *, request=None):
    """
    Re-run the legal rules on the person's open case after their situation changed.

    Returns the new assessment, or None when nothing moved — the caller uses that to decide whether
    to tell the person their orientation was recalculated, and saying so when nothing changed would
    be a small lie that teaches them to distrust the bigger statements.
    """
    case = active_case(user)
    if case is None:
        return None
    try:
        from cases.intake import reassess

        return reassess(case, request=request, reason="situation_updated")
    except Exception:  # noqa: BLE001 - a failed recomputation must not lose what the person just saved
        log.exception("reassessment failed for case %s", getattr(case, "reference", "?"))
        return None
