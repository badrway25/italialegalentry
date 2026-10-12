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


@dataclass(frozen=True)
class TopicSpec:
    slug: str
    name_fr: str
    icon: str
    order: int


# Icon names refer to the design-system sprite (static/img/icons.svg); decorative only.
INITIAL_TOPICS: tuple[TopicSpec, ...] = (
    TopicSpec("langue-italienne", "Langue italienne", "globe", 10),
    TopicSpec("logement", "Logement", "home", 20),
    TopicSpec("sante", "Santé", "plus", 30),
    TopicSpec("service-sanitaire-national", "Service sanitaire national (SSN)", "institution", 40),
    TopicSpec("ecole", "École", "university", 50),
    TopicSpec("education-civique", "Éducation civique", "compass", 60),
    TopicSpec("droits-et-devoirs", "Droits et devoirs", "document", 70),
    TopicSpec("securite-au-travail", "Sécurité au travail", "shield", 80),
    TopicSpec("fiscalite-de-base", "Fiscalité de base", "briefcase", 90),
    TopicSpec("services-publics", "Services publics", "building", 100),
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
