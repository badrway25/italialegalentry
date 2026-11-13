"""
The portal's lists on the platform's list toolkit (portal.listing; V5.30, stream C —
docs/design-v5/QA/v530/plat/NOTES.md §2): «Communications» and the account's files on «Mes documents». Each spec
narrows the queryset its view already scopes (`portal.services.inbox(user)` — own and visible —,
`portal.services.documents_for(user)` — own and alive); every lookup below is written here, never read from the query
string.

V5.32 lane E (the PLATFORM=READY round of the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive):
«Mes demandes» — the account's own requests of every kind (`portal.services.requests_for(user)`, a list: each row
re-checked as the account's) — and «Mes échéances» — the account's dates (`portal.services.deadlines_for(user)`) — on
the same toolkit.
"""

from __future__ import annotations

from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from portal.listing import DateRange, Filter, ListSpec, Sort


def _created_between(rows, start, end):
    if start:
        rows = rows.filter(created_at__date__gte=start)
    if end:
        rows = rows.filter(created_at__date__lte=end)
    return rows


def _distinct(rows, name: str) -> set:
    """The values one column of the scoped rows holds (the order cleared, so DISTINCT is the column's own)."""
    return set(rows.order_by().values_list(name, flat=True).distinct())


PERIOD = _("Période")

# ---- «Communications» --------------------------------------------------------------------------------------------
READ_STATES = (("non-lues", _("Non lues")), ("lues", _("Lues")))

MESSAGES = ListSpec(
    "messages",
    search=lambda rows, q: rows.filter(Q(subject__icontains=q) | Q(body__icontains=q)),
    search_label=_("Rechercher dans vos communications"),
    filters=(
        Filter(
            "lecture",
            _("État"),
            READ_STATES,
            apply=lambda rows, value: rows.filter(is_read=(value == "lues")),
            present=lambda rows: {"lues" if read else "non-lues" for read in _distinct(rows, "is_read")},
        ),
    ),
    dates=DateRange(PERIOD, _created_between),
    sorts=(
        Sort("recentes", _("Plus récentes d’abord"), lambda rows: rows.order_by("-created_at")),
        Sort("anciennes", _("Plus anciennes d’abord"), lambda rows: rows.order_by("created_at")),
        Sort("non-lues", _("Non lues d’abord"), lambda rows: rows.order_by("is_read", "-created_at")),
    ),
)


# ---- «Mes documents»: the account's files ---------------------------------------------------------------------------
def _kinds():
    from documents.models import DocumentKind

    return DocumentKind.choices


FILES = ListSpec(
    "files",
    search=lambda rows, q: rows.filter(Q(original_name__icontains=q) | Q(description__icontains=q)),
    search_label=_("Rechercher un fichier"),
    filters=(
        Filter(
            "type",
            _("Type"),
            _kinds,
            apply=lambda rows, value: rows.filter(kind=value),
            present=lambda rows: _distinct(rows, "kind"),
        ),
    ),
    dates=DateRange(PERIOD, _created_between),
    sorts=(
        Sort("recents", _("Plus récents d’abord"), lambda rows: rows.order_by("-created_at", "-pk")),
        Sort("anciens", _("Plus anciens d’abord"), lambda rows: rows.order_by("created_at", "pk")),
        Sort("nom", _("Nom de A à Z"), lambda rows: rows.order_by("original_name", "pk")),
        Sort("taille", _("Les plus lourds d’abord"), lambda rows: rows.order_by("-size", "-created_at")),
    ),
    # the register above the files owns `?état=` (documents/partials/state_filter.html): it rides along untouched
    preserve=("état",),
)


# ---- «Mes demandes»: the account's requests, every kind (a list of portal.services.RequestItem) ----------------------
def _fold(value) -> str:
    return " ".join(str(value or "").split()).casefold()


def _request_kinds():
    from portal.services import REQUEST_KINDS

    kinds = []
    for slug, kind in REQUEST_KINDS.items():
        model = kind.model()
        if model is not None:
            kinds.append((slug, model._meta.verbose_name))
    return kinds


def _request_states():
    from enquiries.models import SubmissionStatus
    from forum.models import RegistrationStatus

    # two registers, two vocabularies, no value in common: a Forum registration is «Reçue», a form «Nouvelle»
    return [*SubmissionStatus.choices, *RegistrationStatus.choices]


def _sent_between(rows, start, end):
    def day(item):
        return timezone.localtime(item.created_at).date()

    return [item for item in rows if (not start or day(item) >= start) and (not end or day(item) <= end)]


REQUESTS = ListSpec(
    "demandes",
    search=lambda rows, q: [
        item for item in rows if _fold(q) in _fold(item.title) or _fold(q) in _fold(item.reference)
    ],
    search_label=_("Rechercher une demande"),
    filters=(
        Filter(
            "type",
            _("Type"),
            _request_kinds,
            apply=lambda rows, value: [item for item in rows if item.kind == value],
            present=lambda rows: {item.kind for item in rows},
        ),
        Filter(
            "etat",
            _("État"),
            _request_states,
            apply=lambda rows, value: [item for item in rows if item.status == value],
            present=lambda rows: {item.status for item in rows},
        ),
    ),
    dates=DateRange(PERIOD, _sent_between),
    sorts=(
        Sort(
            "recentes", _("Plus récentes d’abord"), lambda rows: sorted(rows, key=lambda i: i.created_at, reverse=True)
        ),
        Sort("anciennes", _("Plus anciennes d’abord"), lambda rows: sorted(rows, key=lambda i: i.created_at)),
    ),
)


# ---- «Mes échéances»: the account's dates (the page keeps its order: the open ones by date, then the closed) ---
def _due_between(rows, start, end):
    if start:
        rows = rows.filter(due_on__gte=start)
    if end:
        rows = rows.filter(due_on__lte=end)
    return rows


def _deadline_kinds():
    from portal.models import DeadlineKind

    return DeadlineKind.choices


def _deadline_states():
    from portal.models import DeadlineStatus

    return DeadlineStatus.choices


DEADLINES = ListSpec(
    "echeances",
    search=lambda rows, q: rows.filter(
        Q(title__icontains=q) | Q(description__icontains=q) | Q(source_note__icontains=q)
    ),
    search_label=_("Rechercher une échéance"),
    filters=(
        Filter(
            "type",
            _("Type"),
            _deadline_kinds,
            apply=lambda rows, value: rows.filter(kind=value),
            present=lambda rows: _distinct(rows, "kind"),
        ),
        Filter(
            "etat",
            _("État"),
            _deadline_states,
            apply=lambda rows, value: rows.filter(status=value),
            present=lambda rows: _distinct(rows, "status"),
        ),
    ),
    dates=DateRange(PERIOD, _due_between),
)
