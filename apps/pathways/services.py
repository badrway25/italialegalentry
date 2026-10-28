"""
Espace Personnes — business logic (views stay thin).

* Gate handling (Phase 3 + staff preview).
* Merging the locked registry (titles/descriptions, always eight, prescribed order) with the
  editorial rows (icon, publication status, detail content).
* Public rendering rules for reviewable items: an item flagged ``pending_legal_review`` exposes
  only its heading, never its body text (CONTENT_PENDING_LEGAL_REVIEW).
* Static, non-legal skeletons for the diplomas page (headings derived from the locked text).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from urllib.parse import urlsplit

from django.conf import settings
from django.utils import translation
from django.utils.translation import gettext_lazy as _

from cms import locked_content
from cms.translation import resolve
from core import gates, icons
from pathways.models import (
    GENERIC_AUTHORITY_NAMES,
    Pathway,
    PathwayDocument,
    PathwayStep,
    PathwayWarning,
    locked_pathway_entries,
)

# --------------------------------------------------------------------------------------------
# Gate
# --------------------------------------------------------------------------------------------


def phase3_open() -> bool:
    return gates.phase3_public()


def can_preview(request) -> bool:
    """
    Back-office users may preview gated pages with ``?preview=1`` (rendered with noindex) — once the session meets the
    second-factor policy, as anywhere a staff privilege is exercised (``accounts.middleware.require_second_factor``).
    """
    user = getattr(request, "user", None)
    if not (user is not None and user.is_authenticated and user.is_staff):
        return False
    if request.GET.get("preview") != "1":
        return False
    from accounts.middleware import require_second_factor

    require_second_factor(request)
    return True


def gated_pages_visible(request) -> tuple[bool, bool]:
    """(visible, is_preview)."""
    if phase3_open():
        return True, False
    if can_preview(request):
        return True, True
    return False, False


# --------------------------------------------------------------------------------------------
# Registry ↔ rows
# --------------------------------------------------------------------------------------------

# Editorial defaults for the icon of each pathway: the registry's PATHWAY concept map (apps/core/icons.py, design V5
# plan §1.7 — one concept, one glyph), so that no producer here names a V4 id any more (W1-B's review, m2: the V4 ids
# `globe`, `handshake`, `search`, … read as other concepts, and `globe` is an alias that leaves with its last producer).
DEFAULT_ICONS: dict[str, str] = dict(icons.PATHWAY)

# Navigational association between a pathway and the locked glossary terms (p3.glossary.terms).
# Only concepts literally named in the pathway's own locked description are added on top of the
# three general terms; this is a reading aid, not an eligibility statement.
GENERAL_GLOSSARY_TERMS: tuple[str, ...] = ("visto_ingresso", "permesso_di_soggiorno", "codice_fiscale")
GLOSSARY_TERMS_BY_PATHWAY: dict[str, tuple[str, ...]] = {
    "salaried_work": ("decreto_flussi", "nulla_osta", "questura_prefettura"),
    "skilled_work_eu_blue_card": ("carta_blu_ue", "nulla_osta"),
    "training_in_origin_country": (),
    "study_and_training_in_italy": ("dichiarazione_di_valore", "legalizzazione_apostille"),
    "family_reunification": ("ricongiungimento_familiare", "nulla_osta"),
    "self_employment_entrepreneurship": (),
    "scientific_research": ("dichiarazione_di_valore",),
    "other_regular_routes": ("decreto_flussi", "questura_prefettura"),
}


def _safe_reverse(name: str, **kwargs) -> str:
    from core.links import public_url

    return public_url(name, **kwargs)


def glossary_index() -> dict[str, dict]:
    terms, _lang = locked_content.get("p3.glossary.terms", "fr")
    return {t["key"]: t for t in terms}


def glossary_links(key: str) -> list[dict]:
    """Locked glossary terms related to a pathway, with a link when the glossary app is available."""
    index = glossary_index()
    slugs = GENERAL_GLOSSARY_TERMS + tuple(s for s in GLOSSARY_TERMS_BY_PATHWAY.get(key, ()) if s in index)
    links = []
    for slug in slugs:
        term = index.get(slug)
        if not term:
            continue
        links.append({"slug": slug, "term": term["term"], "url": _safe_reverse("glossary:term", slug=slug)})
    return links


@dataclass(frozen=True)
class IndexEntry:
    key: str
    order: int
    title: str
    description: str
    icon: str
    url: str
    is_live: bool


def index_entries(at=None) -> list[IndexEntry]:
    """Always the eight locked pathways in the prescribed order; detail links only when live."""
    rows = {p.key: p for p in Pathway.objects.all()}
    entries: list[IndexEntry] = []
    for position, entry in enumerate(locked_pathway_entries(), start=1):
        row = rows.get(entry["key"])
        live = bool(row and row.is_live(at))
        entries.append(
            IndexEntry(
                key=entry["key"],
                order=position,
                title=entry["title"],
                description=entry["description"],
                icon=(row.icon if row and row.icon else DEFAULT_ICONS.get(entry["key"], "")),
                url=_safe_reverse("pathways:detail", key=entry["key"]) if live else "",
                is_live=live,
            )
        )
    return entries


#: the separator of the locked «Comment ça marche» sentence, as the registry writes it
ARROW = " → "


@dataclass(frozen=True)
class HowItWorks:
    """
    The locked «Comment ça marche» sentence (``p3.persons.how_it_works``) cut on its own separators for layout
    (CREATIVE_DIRECTION_V5 law 8, owner decision D-U4): its opening words up to and including the colon, the four
    steps between its arrows, and the caveat after the last step's full stop. Nothing is retyped: ``text`` — the lead,
    the steps joined by the sentence's own « → », a space, the caveat — is the registry's sentence, character for
    character (the template keeps the arrows as hidden text, so the list reads back whole).
    """

    lead: str
    steps: tuple[str, ...]
    caveat: str
    lang: str  # the language attribute of the words on a page shown in another language, else ""

    @property
    def arrow(self) -> str:
        """The separator's own sign, kept as hidden text between the stations."""
        return ARROW.strip()

    @property
    def text(self) -> str:
        return f"{self.lead}{ARROW.join(self.steps)} {self.caveat}"


def how_it_works(lang: str | None = None) -> HowItWorks | None:
    """The sentence cut for «la linea», or None when its shape is not the one the cut knows (then it stands whole)."""
    lang = lang or _lang()
    text, effective = locked_content.get("p3.persons.how_it_works", lang)
    if not isinstance(text, str):
        return None
    head, colon, rest = text.partition(": ")
    *steps, last = rest.split(ARROW)
    stop = last.find(". ")
    if not colon or len(steps) < 2 or stop < 0:
        return None
    cut = HowItWorks(
        lead=head + colon,
        steps=(*steps, last[: stop + 1]),
        caveat=last[stop + 2 :],
        lang=effective if effective != lang.split("-")[0] else "",
    )
    return cut if cut.text == text else None


def get_live_pathway(key: str) -> Pathway | None:
    return (
        Pathway.objects.live()
        .filter(key=key)
        .select_related("hero_image", "reviewer")
        .prefetch_related("steps__translations", "documents__translations", "warnings__translations", "translations")
        .first()
    )


def get_pathway_for_preview(key: str) -> Pathway | None:
    return (
        Pathway.objects.filter(key=key)
        .select_related("hero_image", "reviewer")
        .prefetch_related("steps__translations", "documents__translations", "warnings__translations", "translations")
        .first()
    )


# --------------------------------------------------------------------------------------------
# Public rendering of reviewable items
# --------------------------------------------------------------------------------------------


def _lang() -> str:
    return (translation.get_language() or settings.LANGUAGE_CODE).split("-")[0]


def _translated(obj, fr_field: str, tr_field: str, lang: str) -> tuple[str, str]:
    """(text, effective_language) using PUBLISHED translations, else the French source."""
    row, effective, _fallback = resolve(obj, lang)
    if row is not None:
        value = getattr(row, tr_field, "") or ""
        if value:
            return value, effective
    return getattr(obj, fr_field, "") or "", settings.CONTENT_FALLBACK_LANGUAGE


@dataclass(frozen=True)
class PublicItem:
    order: int
    heading: str
    body: str
    lang: str
    pending: bool


def public_steps(pathway: Pathway, lang: str | None = None) -> list[PublicItem]:
    lang = lang or _lang()
    items = []
    for step in pathway.steps.all():
        heading, eff = _translated(step, "title_fr", "title", lang)
        body, body_lang = _translated(step, "text_fr", "text", lang)
        items.append(
            PublicItem(
                order=step.order,
                heading=heading,
                body="" if step.pending_legal_review else body,
                lang=eff if step.pending_legal_review else body_lang,
                pending=step.pending_legal_review,
            )
        )
    return sorted(items, key=lambda i: i.order)


def public_documents(pathway: Pathway, lang: str | None = None) -> list[PublicItem]:
    lang = lang or _lang()
    items = []
    for doc in pathway.documents.all():
        heading, eff = _translated(doc, "label_fr", "label", lang)
        body, body_lang = _translated(doc, "note_fr", "note", lang)
        items.append(
            PublicItem(
                order=doc.order,
                heading=heading,
                body="" if doc.pending_legal_review else body,
                lang=eff if doc.pending_legal_review else body_lang,
                pending=doc.pending_legal_review,
            )
        )
    return sorted(items, key=lambda i: i.order)


def public_warnings(pathway: Pathway, lang: str | None = None) -> list[PublicItem]:
    """Warnings have no heading: pending ones are not rendered at all."""
    lang = lang or _lang()
    items = []
    for warning in pathway.warnings.all():
        if warning.pending_legal_review:
            continue
        body, eff = _translated(warning, "text_fr", "text", lang)
        items.append(PublicItem(order=warning.order, heading="", body=body, lang=eff, pending=False))
    return sorted(items, key=lambda i: i.order)


def eligibility_context(pathway: Pathway, lang: str | None = None) -> tuple[str, str]:
    lang = lang or _lang()
    return _translated(pathway, "eligibility_context_fr", "eligibility_context", lang)


def authorities(pathway: Pathway) -> list[dict]:
    out = []
    for item in pathway.authorities or []:
        if not isinstance(item, dict):
            continue
        name = str(item.get("name", "")).strip()
        url = str(item.get("url", "") or "").strip()
        if name:
            # `lang`: language the name is written in (editors may set "it" for Italian office names);
            # CMS values default to the content source language, so templates can mark the fallback.
            lang = str(item.get("lang", "") or settings.CONTENT_FALLBACK_LANGUAGE)[:5]
            url = url if url.startswith("https://") else ""
            # `host`: where the link leads, shown beside it (design V5.4 D26: «an authority link's host made visible»)
            host = (urlsplit(url).hostname or "").removeprefix("www.") if url else ""
            out.append({"name": name, "url": url, "lang": lang, "host": host})
    return out


@dataclass
class DetailContext:
    pathway: Pathway
    title: str
    description: str
    eligibility: str
    eligibility_lang: str
    steps: list[PublicItem]
    documents: list[PublicItem]
    warnings: list[PublicItem]
    authorities: list[dict]
    glossary: list[dict]
    is_training_in_origin_country: bool
    sections: list[dict] = field(default_factory=list)


DETAIL_SECTIONS: tuple[tuple[str, str], ...] = (
    ("apercu", _("Aperçu")),
    ("etapes", _("Étapes")),
    ("documentation", _("Documentation")),
    ("autorites", _("Autorités")),
    ("avertissements", _("Avertissements")),
    ("ressources", _("Ressources")),
    ("orientation", _("Orientation")),
)


def detail_context(pathway: Pathway, lang: str | None = None) -> DetailContext:
    lang = lang or _lang()
    eligibility, eligibility_lang = eligibility_context(pathway, lang)
    return DetailContext(
        pathway=pathway,
        title=pathway.title,
        description=pathway.description,
        eligibility=eligibility,
        eligibility_lang=eligibility_lang,
        steps=public_steps(pathway, lang),
        documents=public_documents(pathway, lang),
        warnings=public_warnings(pathway, lang),
        authorities=authorities(pathway),
        glossary=glossary_links(pathway.key),
        is_training_in_origin_country=pathway.key == "training_in_origin_country",
        sections=[{"id": sid, "label": label} for sid, label in DETAIL_SECTIONS],
    )


# --------------------------------------------------------------------------------------------
# Diplomas page skeleton — headings only, derived from the locked p3.diplomas.body wording.
# CONTENT_PENDING_LEGAL_REVIEW: no procedure detail is written by the technical team.
# --------------------------------------------------------------------------------------------

DIPLOMA_STEPS: tuple[dict, ...] = (
    {"id": "documentation", "label": _("Documentation"), "glossary": ()},
    {"id": "traductions", "label": _("Traductions"), "glossary": ()},
    {"id": "legalisation", "label": _("Légalisation ou apostille"), "glossary": ("legalizzazione_apostille",)},
    {"id": "declaration", "label": _("Déclaration de valeur"), "glossary": ("dichiarazione_di_valore",)},
    {
        "id": "procedures",
        "label": _("Procédures auprès des autorités compétentes"),
        "glossary": ("questura_prefettura",),
    },
)


def diploma_steps() -> list[dict]:
    index = glossary_index()
    steps = []
    for step in DIPLOMA_STEPS:
        links = [
            {"slug": slug, "term": index[slug]["term"], "url": _safe_reverse("glossary:term", slug=slug)}
            for slug in step["glossary"]
            if slug in index
        ]
        steps.append({"id": step["id"], "label": step["label"], "glossary": links, "pending": True})
    return steps


# --------------------------------------------------------------------------------------------
# Shared context bits (side links, CTA targets)
# --------------------------------------------------------------------------------------------


def related_links() -> dict[str, str]:
    """URLs of sibling areas; empty string while the owning app is not yet available."""
    return {
        "orientation": _safe_reverse("orientation:start"),
        "training": _safe_reverse("pathways:training"),
        "diplomas": _safe_reverse("pathways:diplomas"),
        "living": _safe_reverse("living:index"),
        "antifraud": _safe_reverse("pages:antifraud"),
        "faq": _safe_reverse("faq:index"),
        "glossary": _safe_reverse("glossary:index"),
        "index": _safe_reverse("pathways:index"),
    }


def generic_authority_names() -> tuple[str, ...]:
    return GENERIC_AUTHORITY_NAMES


__all__ = [
    "DIPLOMA_STEPS",
    "GLOSSARY_TERMS_BY_PATHWAY",
    "DetailContext",
    "HowItWorks",
    "IndexEntry",
    "PathwayDocument",
    "PathwayStep",
    "PathwayWarning",
    "PublicItem",
    "authorities",
    "can_preview",
    "detail_context",
    "diploma_steps",
    "eligibility_context",
    "gated_pages_visible",
    "generic_authority_names",
    "get_live_pathway",
    "get_pathway_for_preview",
    "glossary_links",
    "how_it_works",
    "index_entries",
    "phase3_open",
    "public_documents",
    "public_steps",
    "public_warnings",
    "related_links",
]
