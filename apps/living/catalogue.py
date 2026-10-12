"""
Initial thematic topics of « Vivre en Italie » (Implementation document §3.8.4 + master brief §42).

These are category labels created by the team (UI content, not prescribed texts): the French
names are the source strings and are translated through gettext (.po files) like any UI string.
The fiches themselves are NOT seeded: their content is CONTENT_PENDING_LEGAL_REVIEW and only
reaches the public after review (living.models.LivingSheet.legal_review).
"""

from __future__ import annotations

from dataclasses import dataclass

from django.utils.translation import gettext_lazy as _

from core.icons import LIVING


@dataclass(frozen=True)
class TopicSpec:
    slug: str
    name_fr: str
    icon: str
    order: int


# A topic's glyph is the icon registry's (apps/core/icons.py LIVING — design V5, W1-B's map; drawn once, on the topic's
# own page, the index of the ten being typographic): the seed copies it into the row's `icon`, the fallback for a topic
# the registry does not know. The V4 ids the seed wrote before («globe», «home», …) were two of the V4 aliases'
# last producers (W1-B's hand-over to W3-F2); rows already seeded keep them, and the page never reads them for these
# ten slugs (living/topic.html asks the registry first).
INITIAL_TOPICS: tuple[TopicSpec, ...] = (
    TopicSpec("langue-italienne", "Langue italienne", LIVING["langue-italienne"], 10),
    TopicSpec("logement", "Logement", LIVING["logement"], 20),
    TopicSpec("sante", "Santé", LIVING["sante"], 30),
    TopicSpec(
        "service-sanitaire-national", "Service sanitaire national (SSN)", LIVING["service-sanitaire-national"], 40
    ),
    TopicSpec("ecole", "École", LIVING["ecole"], 50),
    TopicSpec("education-civique", "Éducation civique", LIVING["education-civique"], 60),
    TopicSpec("droits-et-devoirs", "Droits et devoirs", LIVING["droits-et-devoirs"], 70),
    TopicSpec("securite-au-travail", "Sécurité au travail", LIVING["securite-au-travail"], 80),
    TopicSpec("fiscalite-de-base", "Fiscalité de base", LIVING["fiscalite-de-base"], 90),
    TopicSpec("services-publics", "Services publics", LIVING["services-publics"], 100),
)

# Translatable labels (gettext source = FR). Kept in a mapping so makemessages collects them
# while the database keeps the French source as ``name_fr``.
TOPIC_LABELS = {
    "langue-italienne": _("Langue italienne"),
    "logement": _("Logement"),
    "sante": _("Santé"),
    "service-sanitaire-national": _("Service sanitaire national (SSN)"),
    "ecole": _("École"),
    "education-civique": _("Éducation civique"),
    "droits-et-devoirs": _("Droits et devoirs"),
    "securite-au-travail": _("Sécurité au travail"),
    "fiscalite-de-base": _("Fiscalité de base"),
    "services-publics": _("Services publics"),
}

TOPIC_SLUGS: tuple[str, ...] = tuple(spec.slug for spec in INITIAL_TOPICS)
TOPIC_BY_SLUG: dict[str, TopicSpec] = {spec.slug: spec for spec in INITIAL_TOPICS}
