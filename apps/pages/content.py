"""
Editorial (NON-prescribed) French source strings of the homepage and institutional pages.

* Everything here is a neutral UI / connective string written by the team, wrapped in
  ``gettext_lazy`` (French source, IT/EN/AR through the ``.po`` files).
* Nothing here may copy, shorten or rephrase a prescribed text: prescribed texts are read from
  ``cms.locked_content`` at render time (see ``pages.services``).
* No legal or immigration statement is invented: the few sentences about what the platform does
  not do mirror the meaning of the official Disclaimer and of sentences already public on the
  orientation and Espace Personnes pages.

The seeds store the French msgid in the database (``HomeSection.heading_fr`` …). At render time
``pages.services.editorial()`` passes the stored value through gettext: an untouched default is
therefore translated by the ``.po`` catalogues, while a value rewritten by an editor is shown as
written (tagged ``lang="fr"`` on non-French pages) until a PUBLISHED translation row exists.
"""

from __future__ import annotations

from dataclasses import dataclass

from django.utils.translation import gettext_lazy as _

from pages.models import SectionKey


# --------------------------------------------------------------------------------------------
# Homepage sections — prescribed order (master brief §21), gate and default editorial texts
# --------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class SectionDefault:
    key: str
    order: int
    requires_gate: str = ""
    heading: object = ""
    intro: object = ""
    note: object = ""


SECTION_DEFAULTS: tuple[SectionDefault, ...] = (
    SectionDefault(SectionKey.HERO, 10),
    SectionDefault(SectionKey.BANNER, 20, requires_gate="forum_banner"),
    SectionDefault(
        SectionKey.ENTRANCES,
        30,
        heading=_("Quatre accès à l’écosystème"),
        intro=_(
            "Personnes, entreprises, institutions, universités et organismes de formation : chaque acteur dispose "
            "de son espace."
        ),
    ),
    SectionDefault(
        SectionKey.ORIENTATION,
        40,
        heading=_("Comment fonctionne l’orientation"),
        intro=_("Un questionnaire progressif pour identifier les voies régulières à explorer."),
        note=_(
            "Le résultat du questionnaire est une pré-évaluation à caractère informatif : les décisions relèvent "
            "des autorités compétentes."
        ),
    ),
    SectionDefault(
        SectionKey.PATHWAYS,
        50,
        heading=_("Les parcours réguliers"),
        intro=_(
            "Plusieurs voies régulières existent : le questionnaire d’orientation aide à identifier celles à explorer."
        ),
    ),
    SectionDefault(
        SectionKey.PILOT,
        60,
        requires_gate="phase3_public",
        intro=_("Des besoins des entreprises au suivi : la séquence du projet pilote, étape par étape."),
    ),
    SectionDefault(
        SectionKey.TRUST,
        70,
        heading=_("Ce que fait la plateforme, et ce qu’elle ne fait pas"),
        intro=_(
            "Italy Legal Entry™ informe, oriente et aide à se préparer. Elle ne se substitue jamais aux autorités "
            "compétentes."
        ),
    ),
    SectionDefault(SectionKey.ANTIFRAUD, 80, requires_gate="phase3_public"),
    SectionDefault(SectionKey.NEWS, 90, heading=_("Actualités")),
    SectionDefault(
        SectionKey.ECOSYSTEM,
        100,
        heading=_("Un écosystème institutionnel"),
        intro=_(
            "Le projet est porté par son promoteur et se construit avec des partenaires, présentés uniquement "
            "avec leur accord écrit."
        ),
    ),
    SectionDefault(SectionKey.RESERVED, 110, requires_gate="phase3_public"),
)

SECTION_DEFAULTS_BY_KEY: dict[str, SectionDefault] = {d.key: d for d in SECTION_DEFAULTS}

# Sections that render Phase 3 prescribed texts only: they stay hidden while gate G3 is closed,
# whatever an editor types in ``requires_gate`` (defence in depth).
PHASE3_ONLY_SECTIONS: frozenset[str] = frozenset({SectionKey.PILOT, SectionKey.ANTIFRAUD, SectionKey.RESERVED})


# --------------------------------------------------------------------------------------------
# Interim hero (before Phase 3) — editorial, never a Phase 3 sentence
# --------------------------------------------------------------------------------------------
LOCKED_PREFIX = "locked:"

HERO_INTERIM = {
    "eyebrow_fr": _("Orientation · Formation · Mobilité régulière"),
    "title_fr": _("Un écosystème pour les parcours réguliers vers l’Italie"),
    "subtitle_fr": _("Orientation, formation avant le départ et accompagnement, avec les acteurs compétents."),
    # The body is a Phase 1 prescribed fragment: stored as a reference, resolved through the registry.
    "body_fr": f"{LOCKED_PREFIX}p1.persons.replacement_1",
    "primary_cta_label_fr": _("Découvrir le questionnaire d’orientation"),
    "primary_cta_url_name": "orientation:start",
    "secondary_cta_label_fr": _("Espace entreprises"),
    "secondary_cta_url_name": "enquiries:company_needs",
}

# Phase 3 hero: title / subtitle / body are locked (p3.hero.*); only the calls to action are editorial.
HERO_PHASE3 = {
    "eyebrow_fr": "",
    "title_fr": "",
    "subtitle_fr": "",
    "body_fr": "",
    "primary_cta_label_fr": _("Découvrir le questionnaire d’orientation"),
    "primary_cta_url_name": "orientation:start",
    "secondary_cta_label_fr": _("Espace entreprises"),
    "secondary_cta_url_name": "ecosystem:companies",
}


# --------------------------------------------------------------------------------------------
# Four entrances — neutral interim copy (gate G3 closed). Exactly four, never more.
# --------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class EntranceDefault:
    actor: str  # person | company | institution | university (suffix of p3.entrances.<actor>.*)
    title: object
    text: object
    button: object
    illustration: str
    icon: str
    open_targets: tuple[str, ...]  # URL names tried in order when gate G3 is open
    interim_targets: tuple[str, ...]  # URL names tried in order while gate G3 is closed


ENTRANCES: tuple[EntranceDefault, ...] = (
    EntranceDefault(
        "person",
        _("Personnes"),
        _("S’orienter vers une voie régulière et se préparer avant le départ."),
        _("Découvrir l’espace"),
        "img/illustrations/entrance-person.svg",
        "person",
        ("pathways:index",),
        ("pathways:index",),
    ),
    EntranceDefault(
        "company",
        _("Entreprises"),
        _("Exprimer les besoins de votre entreprise en métiers et en compétences."),
        _("Signaler vos besoins"),
        "img/illustrations/entrance-company.svg",
        "building",
        ("ecosystem:companies", "enquiries:company_needs"),
        ("enquiries:company_needs", "ecosystem:companies"),
    ),
    EntranceDefault(
        "institution",
        _("Institutions"),
        _("Construire des coopérations institutionnelles autour de la formation et de la mobilité régulière."),
        _("Proposer une collaboration"),
        "img/illustrations/entrance-institution.svg",
        "institution",
        ("ecosystem:institutions", "enquiries:institution_proposal"),
        ("enquiries:institution_proposal", "ecosystem:institutions"),
    ),
    EntranceDefault(
        "university",
        _("Universités et organismes de formation"),
        _("Développer des partenariats de formation, de stages et d’échanges."),
        _("Proposer un partenariat"),
        "img/illustrations/entrance-university.svg",
        "university",
        ("ecosystem:universities", "enquiries:university_proposal"),
        ("enquiries:university_proposal", "ecosystem:universities"),
    ),
)

ENTRANCES_BY_ACTOR: dict[str, EntranceDefault] = {e.actor: e for e in ENTRANCES}

# The word each entrance goes by in the hero's legend (design V4, CREATIVE_DIRECTION.md §4.2):
# the navigation's own labels, one or two words, never the prescribed question, which is a title
# and a sentence. Translated through the catalogues like the navigation.
ENTRANCE_LABELS: dict[str, object] = {
    "person": _("Personnes"),
    "company": _("Entreprises"),
    "institution": _("Institutions"),
    "university": _("Universités & Formation"),
}


# --------------------------------------------------------------------------------------------
# Orientation — neutral four-step explanation used while gate G3 is closed
# --------------------------------------------------------------------------------------------
ORIENTATION_STEPS: tuple = (
    _("Répondre aux questions d’orientation"),
    _("Recevoir une pré-évaluation informative"),
    _("Se préparer avant le départ"),
    _("Suivre la procédure régulière"),
)

# --------------------------------------------------------------------------------------------
# Pathway families — neutral labels shown while gate G3 is closed (no prescribed title, no
# description, no eligibility statement: labels only, all pointing to the Espace Personnes).
# --------------------------------------------------------------------------------------------
PATHWAY_FAMILIES: tuple = (
    _("Travail"),
    _("Formation avant le départ"),
    _("Études et formation"),
    _("Famille"),
    _("Recherche"),
)

# --------------------------------------------------------------------------------------------
# Trust / transparency
# --------------------------------------------------------------------------------------------
# Prescribed FAQ entries quoted when gate G3 is open (answers rendered verbatim from p3.faq.items).
TRUST_FAQ_KEYS: tuple[str, ...] = (
    "faq_visas",
    "faq_recruitment_agency",
    "faq_preassessment_guarantee",
    "faq_diplomas",
)
# Phase 1 prescribed fragments shown as "what the platform does" while gate G3 is closed.
TRUST_DOES_LOCKED_KEYS: tuple[str, ...] = ("p1.persons.replacement_1", "p1.persons.replacement_2")
# Neutral statements mirroring the meaning of the official Disclaimer (no legal text invented).
TRUST_DOES_NOT: tuple = (
    _("Elle ne délivre aucun visa, permis ou autorisation : ces décisions relèvent des autorités compétentes."),
    _("Elle ne promet ni ne garantit aucun résultat administratif."),
    _("Ses pré-évaluations ont un caractère informatif et ne constituent pas un conseil juridique individualisé."),
)

# Prescribed FAQ entry presenting the promoter (rendered only when gate G3 is open).
PROMOTER_FAQ_KEY = "faq_who"
# Prescribed FAQ entry the anti-fraud page points to.
ANTIFRAUD_FAQ_KEY = "faq_guaranteed_visa_offer"


# --------------------------------------------------------------------------------------------
# Network page — the actors of the ecosystem (neutral, derived from the list of actors that the
# prescribed presentation texts enumerate; no role, power or promise is attributed to anyone).
# --------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class ActorDefault:
    key: str
    icon: str
    title: object
    text: object
    link_label: object
    entrance: str = ""  # reuse the target of the corresponding entrance
    url_name: str = ""


NETWORK_ACTORS: tuple[ActorDefault, ...] = (
    ActorDefault(
        "persons",
        "person",
        _("Personnes"),
        _("Elles s’informent, s’orientent vers une voie régulière et se préparent avant le départ."),
        _("Espace Personnes"),
        entrance="person",
    ),
    ActorDefault(
        "companies",
        "building",
        _("Entreprises"),
        _("Elles font connaître leurs besoins professionnels, point de départ des parcours de formation."),
        _("Espace Entreprises"),
        entrance="company",
    ),
    ActorDefault(
        "institutions",
        "institution",
        _("Institutions"),
        _("Elles participent à la construction de coopérations et de partenariats entre les territoires."),
        _("Espace Institutions"),
        entrance="institution",
    ),
    ActorDefault(
        "universities",
        "university",
        _("Universités et organismes de formation"),
        _("Ils contribuent à la formation, aux stages, aux échanges et à la coopération académique."),
        _("Espace Universités et Formation"),
        entrance="university",
    ),
    ActorDefault(
        "professionals",
        "briefcase",
        _("Professionnels"),
        _("Ils apportent leurs compétences à l’accompagnement des parcours, chacun dans son domaine."),
        _("Contacter le projet"),
        url_name="pages:contact",
    ),
)
