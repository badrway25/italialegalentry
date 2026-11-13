"""
The Academy's catalogue on the platform's list toolkit (portal.listing; V5.32 lane E, the owner's GLOBAL SITE + PLATFORM
DESIGN COMPLETION directive of 12 Nov 2026: «search, sorting, filters where the backend supports them — compact base
filters, an advanced drawer, active chips, reset, a result count»).

The catalogue already held three narrowings in its service (`academy.services.catalogue`: the domain, the teaching
language, a search on the title and the summary) but drew only the domain, as a row of tabs that wrapped on two lines.
The spec below declares them — and the course's form (online, in person, blended), a column the row already prints — on
the rows `services.catalogue(user)` scopes (`Course.objects.visible_to(user)`): every lookup is written here, never read
from the query string; each step only narrows or orders. The GET keys keep the catalogue's own names (`domaine`,
`langue`), so an address written before this change still means the same list.
"""

from __future__ import annotations

from django.conf import settings
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from portal.listing import Filter, ListSpec, Sort

from .models import CourseFormat, CourseType


def _distinct(rows, name: str) -> set:
    return set(rows.order_by().values_list(name, flat=True).distinct())


CATALOGUE = ListSpec(
    "catalogue",
    search=lambda rows, q: rows.filter(
        Q(title__icontains=q) | Q(summary__icontains=q) | Q(provider__name__icontains=q)
    ),
    search_label=_("Rechercher un cours"),
    filters=(
        Filter(
            "domaine",
            _("Domaine"),
            CourseType.choices,
            apply=lambda rows, value: rows.filter(course_type=value),
            present=lambda rows: _distinct(rows, "course_type"),
        ),
        Filter(
            "modalite",
            _("Modalité"),
            CourseFormat.choices,
            apply=lambda rows, value: rows.filter(course_format=value),
            present=lambda rows: _distinct(rows, "course_format"),
        ),
        Filter(
            "langue",
            _("Langue d’enseignement"),
            lambda: settings.LANGUAGES,
            apply=lambda rows, value: rows.filter(language=value),
            present=lambda rows: _distinct(rows, "language"),
        ),
    ),
    sorts=(
        Sort("domaine", _("Par domaine"), lambda rows: rows.order_by("course_type", "title")),
        Sort("titre", _("Par intitulé"), lambda rows: rows.order_by("title")),
        Sort("duree", _("Les plus courts d’abord"), lambda rows: rows.order_by("duration_hours", "title")),
    ),
)


#: «Mes formations» — the person's own enrolments (`services.enrolments_for(user).filter(person=user)`; V5.32 lane E,
#: the PLATFORM=READY round): the course's title or the body that delivers it, its domain, two orders. The page keeps
#: its registers — in progress, followed to the end, interrupted — and draws each from the narrowed rows.
MINE = ListSpec(
    "formations",
    search=lambda rows, q: rows.filter(Q(course__title__icontains=q) | Q(course__provider__name__icontains=q)),
    search_label=_("Rechercher une formation"),
    filters=(
        Filter(
            "domaine",
            _("Domaine"),
            CourseType.choices,
            apply=lambda rows, value: rows.filter(course__course_type=value),
            present=lambda rows: _distinct(rows, "course__course_type"),
        ),
    ),
    sorts=(
        Sort("recentes", _("Plus récentes d’abord"), lambda rows: rows.order_by("-enrolled_at")),
        Sort("titre", _("Par intitulé"), lambda rows: rows.order_by("course__title", "-enrolled_at")),
    ),
)
