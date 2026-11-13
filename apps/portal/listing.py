"""
THE PLATFORM'S LIST TOOLKIT — one server-side filter architecture for the console's lists (V5.30, stream C;
docs/design-v5/QA/v530/plat/NOTES.md §1). A list declares a SPEC — its search, its filters, its date range, its sorts —
and its view hands the spec the rows IT ALREADY SCOPES:

    state = SPEC.read(request.GET)                  # the spec's own keys only, each value checked against its whitelist
    rows = SPEC.apply(scoped, state)                # every step NARROWS (filter / exclude / order) — never a wider set
    context["listing"] = SPEC.context(state, scoped=scoped, count=…, total=…, path=request.path)

What the query string can reach, and what it cannot:
  · a filter's value must be one of the spec's choices (else it is ignored), a date must be an ISO day (else ignored;
    two days given the wrong way round are put in order), the search is folded to single spaces and cut at 80
    characters, the sort must be one of the spec's keys (else the default): no field name, lookup, ordering expression
    or operator ever comes from the URL — each step is a callable the LIST declares, with its lookups written in code;
  · every step is applied to the rows the view scoped: a queryset is only ever filtered, excluded or ordered, a list
    only comprehended or sorted — a spec cannot reach a row the view did not already let this account see;
  · unknown parameters are ignored, except the ones the page itself owns (`preserve`: «Mes documents»' `?état=`), which
    ride along unchanged (cut at 80 characters, rendered escaped).
The state lives in the URL alone — bookmarkable, shareable, Back / Forward safe; nothing is stored server-side (saved
views are deferred: the project has no preference store — NOTES §0).

The template side: templates/components/listing/toolbar.html (the bar: the search, the sort, «Filtres» with its count,
the result count, the chips, «Tout effacer») and templates/components/listing/filters.html (the drawer's body and foot,
on the overlay system's drawer, templates/components/drawer.html); the sheet portal/listing.css; the enhancements
static/js/src/listing.js. Every word is the catalogue's.
"""

from __future__ import annotations

import datetime as dt
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urlencode

from django.utils.formats import date_format
from django.utils.translation import gettext_lazy as _

SEARCH_KEY = "q"
SORT_KEY = "tri"
PAGE_KEY = "page"
#: the longest search (and the longest preserved value) the query string may carry
SEARCH_MAX = 80
#: the bar appears where there is something to narrow: two rows or more — or a narrowing already in force
SHOW_FROM = 2


@dataclass(frozen=True)
class Filter:
    """One whitelisted filter: its GET key, its name, its choices (value, label) and the narrowing it applies.

    `present` (optional) says which of the choices the scoped rows actually hold, so the drawer offers only those
    (the one in force is always offered); a filter with fewer than two to offer is not drawn."""

    key: str
    label: Any
    choices: Sequence[tuple[str, Any]] | Callable[[], Sequence[tuple[str, Any]]]
    apply: Callable[[Any, str], Any]
    present: Callable[[Any], Iterable[str]] | None = None

    def options(self) -> list[tuple[str, Any]]:
        return [(str(value), label) for value, label in (self.choices() if callable(self.choices) else self.choices)]


@dataclass(frozen=True)
class DateRange:
    """A period on one date of the rows: «Du» / «Au», inclusive, either bound alone."""

    label: Any
    apply: Callable[[Any, dt.date | None, dt.date | None], Any]
    start: str = "du"
    end: str = "au"


@dataclass(frozen=True)
class Sort:
    """One whitelisted order. The first of a spec's sorts is its default — the list's own order before the toolkit."""

    key: str
    label: Any
    apply: Callable[[Any], Any]


@dataclass
class ListState:
    """What the query string asked for, once checked. Built by `ListSpec.read`, never by hand."""

    query: str = ""
    values: dict[str, str] = field(default_factory=dict)
    start: dt.date | None = None
    end: dt.date | None = None
    sort: str = ""
    kept: dict[str, str] = field(default_factory=dict)

    @property
    def narrowed(self) -> bool:
        return bool(self.query or self.values or self.start or self.end)


def _day(raw) -> dt.date | None:
    try:
        return dt.date.fromisoformat(str(raw or "").strip()[:10]) if raw else None
    except ValueError:
        return None


def _short(value) -> str:
    return " ".join(str(value or "").split())[:SEARCH_MAX]


class ListSpec:
    """The declaration of one list's search, filters, period and orders (see the module's docstring)."""

    def __init__(
        self,
        name: str,
        *,
        search: Callable[[Any, str], Any] | None = None,
        search_label: Any = "",
        filters: Sequence[Filter] = (),
        dates: DateRange | None = None,
        sorts: Sequence[Sort] = (),
        preserve: Sequence[str] = (),
    ):
        keys = [f.key for f in filters] + ([dates.start, dates.end] if dates else [])
        reserved = {SEARCH_KEY, SORT_KEY, PAGE_KEY, *preserve}
        if len(set(keys)) != len(keys) or reserved & set(keys):
            raise ValueError(f"{name}: a filter key is repeated or reserved")
        self.name = name
        self.search = search
        self.search_label = search_label
        self.filters = tuple(filters)
        self.dates = dates
        self.sorts = tuple(sorts)
        self.preserve = tuple(preserve)

    # ---- reading ------------------------------------------------------------------------------------------------
    def read(self, params) -> ListState:
        state = ListState(sort=self.sorts[0].key if self.sorts else "")
        if self.search is not None:
            state.query = _short(params.get(SEARCH_KEY, ""))
        for spec in self.filters:
            value = str(params.get(spec.key, "") or "")
            if value and value in {v for v, _label in spec.options()}:
                state.values[spec.key] = value
        if self.dates is not None:
            state.start, state.end = _day(params.get(self.dates.start)), _day(params.get(self.dates.end))
            if state.start and state.end and state.start > state.end:
                state.start, state.end = state.end, state.start
        sort = str(params.get(SORT_KEY, "") or "")
        if sort in {s.key for s in self.sorts}:
            state.sort = sort
        for key in self.preserve:
            value = _short(params.get(key, ""))
            if value:
                state.kept[key] = value
        return state

    # ---- narrowing ----------------------------------------------------------------------------------------------
    def apply(self, rows, state: ListState):
        """The scoped rows, narrowed by the state and put in its order. Each step only narrows or orders."""
        for spec in self.filters:
            if spec.key in state.values:
                rows = spec.apply(rows, state.values[spec.key])
        if self.dates is not None and (state.start or state.end):
            rows = self.dates.apply(rows, state.start, state.end)
        if state.query and self.search is not None:
            rows = self.search(rows, state.query)
        for sort in self.sorts:
            if sort.key == state.sort:
                rows = sort.apply(rows)
                break
        return rows

    # ---- the URL ------------------------------------------------------------------------------------------------
    def _pairs(self, state: ListState, *, without: Iterable[str] = ()) -> list[tuple[str, str]]:
        """The state as query-string pairs, in a stable order: the page's own keys, the search, the filters, the
        period, the sort when it is not the default — never the page number (a new narrowing starts at page 1)."""
        drop = set(without)
        pairs = [(k, v) for k, v in state.kept.items() if k not in drop]
        if state.query and SEARCH_KEY not in drop:
            pairs.append((SEARCH_KEY, state.query))
        pairs += [(f.key, state.values[f.key]) for f in self.filters if f.key in state.values and f.key not in drop]
        if self.dates is not None:
            if state.start and self.dates.start not in drop:
                pairs.append((self.dates.start, state.start.isoformat()))
            if state.end and self.dates.end not in drop:
                pairs.append((self.dates.end, state.end.isoformat()))
        if self.sorts and state.sort != self.sorts[0].key and SORT_KEY not in drop:
            pairs.append((SORT_KEY, state.sort))
        return pairs

    @staticmethod
    def _url(path: str, pairs: list[tuple[str, str]]) -> str:
        return f"{path}?{urlencode(pairs)}" if pairs else path

    # ---- the template's contract ----------------------------------------------------------------------------------
    def context(self, state: ListState, *, scoped, count: int, total: int, path: str) -> dict[str, Any]:
        """What templates/components/listing/*.html draw. `scoped` = the rows before the narrowing (for the choices the
        drawer offers), `count` = the rows after it, `total` = the rows before it."""
        chips = []
        if state.query:
            chips.append(
                {
                    "label": _("Votre recherche"),
                    "value": state.query,
                    "remove": self._url(path, self._pairs(state, without=[SEARCH_KEY])),
                }
            )
        fields = []
        for spec in self.filters:
            options = spec.options()
            labels = dict(options)
            chosen = state.values.get(spec.key, "")
            if chosen:
                chips.append(
                    {
                        "label": spec.label,
                        "value": labels[chosen],
                        "remove": self._url(path, self._pairs(state, without=[spec.key])),
                    }
                )
            held = {str(v) for v in spec.present(scoped)} if spec.present is not None else set(labels)
            offered = [(v, label) for v, label in options if v in held or v == chosen]
            if len(offered) >= 2 or chosen:
                fields.append(
                    {
                        "key": spec.key,
                        "label": spec.label,
                        "value": chosen,
                        "options": [{"value": v, "label": label, "checked": v == chosen} for v, label in offered],
                    }
                )
        dates = None
        if self.dates is not None:
            for key, day, label in (
                (self.dates.start, state.start, _("Depuis le")),
                (self.dates.end, state.end, _("Jusqu’au")),
            ):
                if day:
                    chips.append(
                        {
                            "label": label,
                            "value": date_format(day, "d.m.Y"),
                            "remove": self._url(path, self._pairs(state, without=[key])),
                        }
                    )
            dates = {
                "label": self.dates.label,
                "start_key": self.dates.start,
                "end_key": self.dates.end,
                "start": state.start.isoformat() if state.start else "",
                "end": state.end.isoformat() if state.end else "",
            }
        return {
            "id": f"lst-{self.name}",
            "path": path,
            "show": total >= SHOW_FROM or state.narrowed,
            "query": state.query,
            "search": self.search is not None,
            "search_label": self.search_label,
            "kept": list(state.kept.items()),
            # the bar's own form carries what the drawer set (its fields are not in the bar), the drawer's form what the
            # bar set: each submits the whole state
            "bar_hidden": [p for p in self._pairs(state, without=[SEARCH_KEY, SORT_KEY]) if p[0] not in state.kept],
            "drawer_hidden": [p for p in self._pairs(state) if p[0] in (SEARCH_KEY, SORT_KEY)],
            "sort": state.sort,
            "sorts": [{"key": s.key, "label": s.label, "selected": s.key == state.sort} for s in self.sorts],
            "fields": fields,
            "dates": dates,
            "has_filters": bool(fields or dates),
            "chips": chips,
            "narrowed": state.narrowed,
            "filter_count": len(state.values) + (1 if state.start else 0) + (1 if state.end else 0),
            "count": count,
            "total": total,
            "clear_url": self._url(path, list(state.kept.items())),
            # the pagination's companion: every parameter of the state but the page (components/pagination.html `query`)
            "page_query": urlencode(self._pairs(state)),
        }
