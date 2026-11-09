"""
«Mes dossiers» on the platform's list toolkit (portal.listing; V5.30, stream C —
docs/design-v5/QA/v530/plat/NOTES.md §2). The spec narrows the ONE queryset that decides who sees which file
(`CaseFile.objects.readable_by(user)`, cases.views.index): a state, an objective, whose file it is, a search on the
reference or the person's name — the names the list already shows on an entrusted file — and three orders. Built per
request because «Le mien / Confiés» compares with the reader. Every lookup is written here, never read from the query
string.
"""

from __future__ import annotations

from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from cases.models import CasePurpose, CaseStatus
from portal.listing import Filter, ListSpec, Sort

MINE, ENTRUSTED = "miens", "confies"


def _distinct(rows, name: str) -> set:
    return set(rows.order_by().values_list(name, flat=True).distinct())


def spec(user) -> ListSpec:
    me = user.pk
    return ListSpec(
        "cases",
        search=lambda rows, q: rows.filter(Q(reference__icontains=q) | Q(person__full_name__icontains=q)),
        search_label=_("Rechercher un dossier"),
        filters=(
            Filter(
                "statut",
                _("État"),
                CaseStatus.choices,
                apply=lambda rows, value: rows.filter(status=value),
                present=lambda rows: _distinct(rows, "status"),
            ),
            Filter(
                "objectif",
                _("Objectif"),
                CasePurpose.choices,
                apply=lambda rows, value: rows.filter(purpose=value),
                present=lambda rows: _distinct(rows, "purpose"),
            ),
            Filter(
                "portee",
                _("Dossiers"),
                ((MINE, _("Le mien")), (ENTRUSTED, _("Confiés"))),
                apply=lambda rows, value: rows.filter(person_id=me) if value == MINE else rows.exclude(person_id=me),
                present=lambda rows: {MINE if pk == me else ENTRUSTED for pk in _distinct(rows, "person_id")},
            ),
        ),
        sorts=(
            Sort("etat", _("Dernier changement d’état"), lambda rows: rows.order_by("-status_since", "-created_at")),
            Sort("ouverture", _("Ouverts le plus récemment"), lambda rows: rows.order_by("-created_at")),
            Sort("reference", _("Référence"), lambda rows: rows.order_by("reference")),
        ),
    )
