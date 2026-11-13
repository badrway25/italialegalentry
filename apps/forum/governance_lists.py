"""
The Forum permanent's two long registers on the platform's list toolkit (portal.listing; V5.32 lane E, the
PLATFORM=READY round of the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026): the proposals
the member may read and the projects — a search on the title and the reference, the commission, the state, two orders.

Each spec is built for ONE request, over the rows its service already scoped (`governance_services.proposals_for(user)`,
`projects_for(user)` — the commissions where the member holds a live mandate): the commission filter offers the
commissions those rows sit in and nothing else, so a crafted `?commission=` naming a commission the member cannot read
is ignored, and its name is never printed. Every lookup is written here; the query string only names a value offered.
"""

from __future__ import annotations

from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from portal.listing import Filter, ListSpec, Sort

from .governance import ProjectStatus, ProposalStatus


def _distinct(rows, name: str) -> set:
    return set(rows.order_by().values_list(name, flat=True).distinct())


def _commission(scoped) -> Filter:
    def choices():
        pairs = scoped.order_by().values_list("commission_id", "commission__name_fr").distinct()
        return sorted(((str(pk), name) for pk, name in pairs), key=lambda pair: pair[1].casefold())

    return Filter("commission", _("Commission"), choices, apply=lambda rows, value: rows.filter(commission_id=value))


def _state(choices) -> Filter:
    return Filter(
        "etat",
        _("État"),
        choices,
        apply=lambda rows, value: rows.filter(status=value),
        present=lambda rows: _distinct(rows, "status"),
    )


def proposals(scoped) -> ListSpec:
    """«Toutes les propositions que je peux consulter»: the latest first, as the register has always drawn them."""
    return ListSpec(
        "propositions",
        search=lambda rows, q: rows.filter(Q(title_fr__icontains=q) | Q(reference__icontains=q)),
        search_label=_("Rechercher une proposition"),
        filters=(_commission(scoped), _state(ProposalStatus.choices)),
        sorts=(
            Sort("recentes", _("Plus récentes d’abord"), lambda rows: rows.order_by("-created_at", "-pk")),
            Sort("anciennes", _("Plus anciennes d’abord"), lambda rows: rows.order_by("created_at", "pk")),
        ),
    )


def projects(scoped) -> ListSpec:
    """«Les projets que je peux consulter»: the latest first, as the register has always drawn them."""
    return ListSpec(
        "projets",
        search=lambda rows, q: rows.filter(
            Q(title_fr__icontains=q)
            | Q(lead__organisation_label__icontains=q)
            | Q(lead__organisation__name__icontains=q)
        ),
        search_label=_("Rechercher un projet"),
        filters=(_commission(scoped), _state(ProjectStatus.choices)),
        sorts=(
            Sort("recents", _("Plus récents d’abord"), lambda rows: rows.order_by("-created_at", "-pk")),
            Sort("anciens", _("Plus anciens d’abord"), lambda rows: rows.order_by("created_at", "pk")),
        ),
    )
