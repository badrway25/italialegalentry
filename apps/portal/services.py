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
from core import clock
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
# Navigation
# ---------------------------------------------------------------------------------------------
def navigation(user, active: str = "") -> list[dict[str, Any]]:
    """
    The reserved area's own navigation.

    The Academy and the help desk are listed HERE, not only on their own pages. Each module used to
    append its row to this list from inside itself, which reads sensibly until you ask how somebody
    reaches the first page of a module they have never opened: the row appeared once you were
    already there. Both surfaces answered 200, had a correct single `h1` and no console errors, and
    were unreachable by clicking — found by walking the mandate's flow
    `… → DOCUMENTI → FORMAZIONE/SPORTELLO` in a browser instead of trusting that each page worked.

    The modules still append their ROLE-SPECIFIC rows — a professional's assigned queue, an
    operator's dispatch desk — and skip the base row when they find it here already.
    """
    unread = unread_count(user)
    messages_label = _("Communications")
    if unread:
        messages_label = _("Communications (%(count)d)") % {"count": unread}
    # In the order of the rail's groups (design V4, CREATIVE_DIRECTION.md §3.9): the journey, the
    # file, the exchanges, the Academy — then the surfaces a role owns.
    entries = [
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
    entries.extend(_role_entries(user))
    return [
        {
            "key": key,
            "label": label,
            "url": url,
            "current": key == active,
            "icon": NAV_GLYPHS.get(key, "chevron-end"),
            "group": str(NAV_GROUPS.get(key, NAV_GROUP_ROLE)),
            "bottom": key in NAV_BOTTOM,
        }
        for key, label, url in entries
    ]


#: The glyph of each entry in the rail (static/img/icons.svg), design V4 §3.9: glyph + word, never
#: the glyph alone.
NAV_GLYPHS: dict[str, str] = {
    "dashboard": "home",
    "situation": "compass",
    "pathways": "map-pin",
    "cases": "briefcase",
    "requests": "list",
    "documents": "document",
    "deadlines": "calendar",
    "messages": "mail",
    "helpdesk": "handshake",
    "academy": "university",
    "selection": "check",
    "company": "building",
    "helpdesk-queue": "list",
}

#: The rail's groups — titles proposed for the copy review (directive §92); the separators stay
#: if the titles go. A role's own surfaces sit under their own title.
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
    "academy": NAV_GROUP_ACADEMY,
}

#: The bottom bar below 64rem shows four entries and «Menu» (design V4 §3.9); the template keeps
#: the first four it finds, so a company sees its own surface among them.
NAV_BOTTOM: frozenset[str] = frozenset({"dashboard", "cases", "documents", "messages", "company"})


#: Surfaces that belong to a role, not to everybody. Each is offered only to the role that can use
#: it — « un module non disponible ne se montre pas », and a menu item that answers 403 tells
#: somebody that something exists.
ROLE_SURFACES: tuple[tuple[str, str, str], ...] = (
    (roles.AUTHORISED_ACTOR, "selection", "selection:workspace"),
    (roles.COMPANY, "company", "companies:dashboard"),
    (roles.PROFESSIONAL, "helpdesk-queue", "helpdesk:queue"),
)

ROLE_SURFACE_LABELS = {
    "selection": gettext_lazy("Processus assignés"),
    "company": gettext_lazy("Mon entreprise"),
    "helpdesk-queue": gettext_lazy("Demandes qui me sont confiées"),
}


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
    entries: list[tuple[str, Any, str]] = []
    for role, key, route in ROLE_SURFACES:
        if not roles.has_role(user, role):
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
                badge_kind=presented["badge_kind"],
            )
        )
    return Card(
        key="deadlines",
        title=_("Mes échéances"),
        icon="calendar",
        count=len(open_rows),
        count_label=ngettext("échéance à venir", "échéances à venir", len(open_rows)),
        badge_label=(_("%(n)d en retard") % {"n": overdue}) if overdue else "",
        badge_kind="error",
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


def card_builders_for(user) -> list[tuple[str, Callable[[Any], Card]]]:
    """Which cards an account gets — driven by its account type and roles (deny by default)."""
    builders: list[tuple[str, Callable[[Any], Card]]] = [("requests", _requests_card)]
    wants_orientation = getattr(user, "account_type", "") in ORIENTATION_ACCOUNT_TYPES or (
        not user.is_superuser and roles.has_role(user, roles.PERSON, roles.PROFESSIONAL)
    )
    if wants_orientation or _has_orientation_sessions(user):
        builders.append(("orientation", _orientation_card))
    builders += [("documents", _documents_card), ("deadlines", _deadlines_card), ("messages", _messages_card)]
    if shows_organisation_card(user) or user.memberships.exists():
        builders.append(("organisation", _organisation_card))
    return builders


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

    return [
        {"title": deadline.title, "date": deadline.due_on, "urgency": due_urgency(deadline.due_on)}
        for deadline in deadlines_for(user).open().order_by("due_on", "id")[:DASHBOARD_LATEST]
    ]


def _with_meter(progress: dict | None) -> dict | None:
    """The five-notch meter of the file panel (design V4 §3.4.2): one notch per element up to
    eight, filled in the real proportion — the words beside it carry the exact count."""
    if not progress:
        return progress
    total = progress.get("total") or 0
    notches = min(total, 8) if total else 0
    filled = round(progress.get("done", 0) / total * notches) if total else 0
    return {**progress, "notches": range(notches), "filled": filled}


def _dashboard_pieces(user) -> dict:
    """The register's counts for the health strip and its three most urgent rows — the same
    presenter and the same authorisation as the register itself."""
    from documents import presenters

    register = presenters.register_context(user)
    block = register["blocks"][0] if register["blocks"] else None
    return {
        "counts": block["counts"] if block else None,
        "filters": block["filters"] if block else [],
        "rows": block["all_rows"][:3] if block else [],
        "more": max(0, len(block["all_rows"]) - 3) if block else 0,
        "reference": block["case"].reference if block else "",
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


def dashboard_context(user) -> dict[str, Any]:
    """Everything the dashboard shows — real rows of THIS account or an explicit empty state."""
    from cases import services as case_services

    cards = [_safe_card(key, builder, user) for key, builder in card_builders_for(user)]
    case = active_case(user)
    assessment = case_services.latest_assessment(case) if case else None
    return {
        "cards": cards,
        "notices": notices_for(user),
        "unread_count": unread_count(user),
        "case": case,
        "responsible": case_services.responsible_for(case) if case else [],
        "progress": _with_meter(case_services.progress(case)) if case else None,
        "next_action": case_services.next_action(case) if case else None,
        "journey": journey_for(case),
        "checklist": list(case.checklist.all()) if case else [],
        "assessment": _dashboard_assessment(cards, assessment),
        "documents": _safe_rows("documents", _dashboard_documents, user),
        # design V4 (CREATIVE_DIRECTION.md §3.4): the pieces' health and the three most urgent rows
        "pieces": _safe_rows("pieces", _dashboard_pieces, user),
        "academy": _safe_rows("academy", _dashboard_academy, user),
        "messages_list": _safe_rows("messages", _dashboard_messages, user),
        "deadlines": _safe_rows("deadlines", _dashboard_deadlines, user),
        "orientation_url": safe_reverse("orientation:start"),
        "documents_url": safe_reverse("portal:documents"),
        "pathways_url": safe_reverse("portal:pathways"),
        "portal_context": case.reference if case else "",
        "is_person": (getattr(user, "account_type", "") == "person") or roles.has_role(user, roles.PERSON),
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
