"""
The digital help desk's registers on the platform's list toolkit (portal.listing; V5.32 lane E, the coordinator's
PLATFORM=READY round of the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026: «search, sort,
filters drawer, chips, reset, count, no-result — where the backend supports it, real data and real GET keys only»).

Three registers, three audiences, each narrowed AFTER its own service scoped it:

* the person's requests (`services.tickets_for(user)` — their own) and the professional's queue
  (`services.queue_for(user)` — the live mandates only): a search on the subject and the references, the state, the
  period the request was opened in, two orders. The state is the one the chip says — ``effective_status``, what is
  true today (a lapsed mandate is not work in progress) —, so these two narrow a list of tickets, never the stored
  column;
* the dispatch register (`services.dispatch_queue(user)` — the question deferred): the references only — designating a
  professional does not require reading the request, and the search never reaches its subject or its text —, where
  the request came from and the language it was written in, two orders on the day it started waiting.

Every lookup is written here; the query string only ever names one of the values offered.
"""

from __future__ import annotations

from django.conf import settings
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from portal.listing import DateRange, Filter, ListSpec, Sort

from .models import TicketOrigin, TicketStatus

STATE = _("État")
PERIOD = _("Période")


def _fold(value) -> str:
    return " ".join(str(value or "").split()).casefold()


def _search(rows, query):
    """The subject, the request's reference and its file's: what the row itself prints."""
    needle = _fold(query)
    return [
        ticket
        for ticket in rows
        if needle in _fold(ticket.subject)
        or needle in _fold(ticket.reference)
        or (ticket.case_id is not None and needle in _fold(ticket.case.reference))
    ]


def _opened_between(rows, start, end):
    def day(ticket):
        return timezone.localtime(ticket.created_at).date()

    return [ticket for ticket in rows if (not start or day(ticket) >= start) and (not end or day(ticket) <= end)]


def _state_filter() -> Filter:
    return Filter(
        "etat",
        STATE,
        TicketStatus.choices,
        apply=lambda rows, value: [ticket for ticket in rows if ticket.effective_status == value],
        present=lambda rows: {ticket.effective_status for ticket in rows},
    )


#: «Guichet numérique» — the person's own requests, newest first (the page's order before the toolkit)
REQUESTS = ListSpec(
    "guichet",
    search=_search,
    search_label=_("Rechercher une demande"),
    filters=(_state_filter(),),
    dates=DateRange(PERIOD, _opened_between),
    sorts=(
        Sort(
            "recentes", _("Plus récentes d’abord"), lambda rows: sorted(rows, key=lambda t: t.created_at, reverse=True)
        ),
        Sort("anciennes", _("Plus anciennes d’abord"), lambda rows: sorted(rows, key=lambda t: t.created_at)),
    ),
)

#: «Demandes qui me sont confiées» — the longest in their state first (the queue's order before the toolkit)
QUEUE = ListSpec(
    "file",
    search=_search,
    search_label=_("Rechercher une demande"),
    filters=(_state_filter(),),
    dates=DateRange(PERIOD, _opened_between),
    sorts=(
        Sort("anciennes", _("Plus anciennes d’abord"), lambda rows: sorted(rows, key=lambda t: t.status_since)),
        Sort(
            "recentes",
            _("Plus récentes d’abord"),
            lambda rows: sorted(rows, key=lambda t: t.status_since, reverse=True),
        ),
    ),
)


def _languages():
    return settings.LANGUAGES


def _distinct(rows, name: str) -> set:
    return set(rows.order_by().values_list(name, flat=True).distinct())


#: «Désignation des professionnels» — waiting the longest first (the register's order before the toolkit)
DISPATCH = ListSpec(
    "designation",
    search=lambda rows, q: rows.filter(Q(reference__icontains=q) | Q(case__reference__icontains=q)),
    search_label=_("Rechercher une référence"),
    filters=(
        Filter(
            "origine",
            _("Origine"),
            TicketOrigin.choices,
            apply=lambda rows, value: rows.filter(origin=value),
            present=lambda rows: _distinct(rows, "origin"),
        ),
        Filter(
            "langue",
            _("Langue de la demande"),
            _languages,
            apply=lambda rows, value: rows.filter(language=value),
            present=lambda rows: _distinct(rows, "language"),
        ),
    ),
    sorts=(
        Sort("anciennes", _("Plus anciennes d’abord"), lambda rows: rows.order_by("status_since", "pk")),
        Sort("recentes", _("Plus récentes d’abord"), lambda rows: rows.order_by("-status_since", "-pk")),
    ),
)
