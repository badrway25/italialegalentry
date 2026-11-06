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


# The families of the /parcours/ filter (V5.12 DECISIONS §7): the reading of each locked title — work, study and
# training, family, the other regular routes — written once, here. A key not listed reads as «other».
PATHWAY_FAMILIES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("work", ("salaried_work", "skilled_work_eu_blue_card", "self_employment_entrepreneurship")),
    ("study", ("training_in_origin_country", "study_and_training_in_italy", "scientific_research")),
    ("family", ("family_reunification",)),
    ("other", ("other_regular_routes",)),
)
FAMILY_OF: dict[str, str] = {key: family for family, keys in PATHWAY_FAMILIES for key in keys}


def family_counts(entries) -> dict[str, int]:
    """How many of the index's entries each family holds, plus ``all`` — the count line under the filter."""
    counts = {family: 0 for family, _keys in PATHWAY_FAMILIES}
    for entry in entries:
        counts[entry.family] = counts.get(entry.family, 0) + 1
    counts["all"] = len(entries)
    return counts


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
    family: str = "other"  # the /parcours/ filter's family (PATHWAY_FAMILIES)


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
                family=FAMILY_OF.get(entry["key"], "other"),
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
    context = DetailContext(
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
    )
    # V5.12 §8 (W1-C): a chapter with nothing verified to say is not drawn, and the page's index does not name it —
    # never «being verified». The overview stands with its context, or with the training-in-origin-country notice
    # (legally required, Impl. §3.3 note); steps, documents and authorities with their verified items.
    present = {
        "apercu": bool(context.eligibility or context.is_training_in_origin_country),
        "etapes": bool(context.steps),
        "documentation": bool(context.documents),
        "autorites": bool(context.authorities),
    }
    context.sections = [{"id": sid, "label": label} for sid, label in DETAIL_SECTIONS if present.get(sid, True)]
    return context


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
# V5.22 — Page Composition V2 (SECTION_SYSTEM_V2 §3.4, §3.5, §3.9, §3.10; lane P1): the data the Espace Personnes'
# compositions draw. Every word is the registry's (cms.locked_content) or a catalogue msgid; a locked sentence is cut at
# render on its own separators and never retyped; the glyphs are the registry's (core.icons).
# --------------------------------------------------------------------------------------------

#: the route board's lanes (§3.4 PA-1): one per family of PATHWAY_FAMILIES, its name (the filter's own msgids) and its
#: frame (lane M's «select» frames, black and white at rest, colour when the lane is chosen, hovered or focused)
FAMILY_LABELS: dict[str, object] = {
    "work": _("Travail"),
    "study": _("Études et formation"),
    "family": _("Famille"),
    "other": _("Autres voies"),
}
FAMILY_FRAMES: dict[str, str] = {
    "work": "pathways.family.work",
    "study": "pathways.family.study",
    "family": "pathways.family.family",
    "other": "pathways.family.other",
}
#: the width the route board draws a lane's frame at (lane S's _sec-tracciato.css): from 64 rem the lane's head, 3/12 of
#: the lane once the trunk's 48 px and the 32 px gap are taken — (content − 80) / 4 for the container's content of
#: 1 360 / 1 240 / 1 096 px and 100vw − 80 below 75 rem; below 64 rem the lane's width, a 21:9 strip (the page's
#: margins 40 / 24 / 20 px and the trunk's 48 px — 40 px on a phone, round 1: pathways/_index.css). Exact at every step
#: (lane P1's browser test measures it).
FAMILY_SIZES_V2 = (
    "(min-width: 100rem) 20rem, (min-width: 90rem) 18.125rem, (min-width: 75rem) 15.875rem, "
    "(min-width: 64rem) calc(25vw - 2.5rem), (min-width: 48rem) calc(100vw - 8rem), "
    "(min-width: 26.875rem) calc(100vw - 5.5rem), calc(100vw - 5rem)"
)
#: round 2 (QA_ROUND2 m9): the two one-station lanes (Famille, Autres voies) share the board's last row from 48 rem —
#: «the fork» — instead of each leaving two thirds of a row empty. From 64 rem the first of the pair keeps the head's
#: width (its station stands where the rows above have their first card); the second's frame stands where the rows
#: above have their second card, one card wide (the head less 8 px: (content − 112) / 4), its station in the third
#: column. From 48 to 64 rem each of the pair is half the board less the trunk's 48 px: (100vw − 104 px) / 2 − 48 px.
#: Below 48 rem the lanes stack as before. Exact at every step (lane P1's browser test measures it).
FAMILY_SIZES_FORK_START = (
    "(min-width: 100rem) 20rem, (min-width: 90rem) 18.125rem, (min-width: 75rem) 15.875rem, "
    "(min-width: 64rem) calc(25vw - 2.5rem), (min-width: 48rem) calc(50vw - 6.25rem), "
    "(min-width: 26.875rem) calc(100vw - 5.5rem), calc(100vw - 5rem)"
)
FAMILY_SIZES_FORK_END = (
    "(min-width: 100rem) 19.5rem, (min-width: 90rem) 17.625rem, (min-width: 75rem) 15.375rem, "
    "(min-width: 64rem) calc(25vw - 3rem), (min-width: 48rem) calc(50vw - 6.25rem), "
    "(min-width: 26.875rem) calc(100vw - 5.5rem), calc(100vw - 5rem)"
)


#: F1 «la traversata» (§3.9): the width each frame is drawn at (its two nodes, the origin country's `earth` and Italy's
#: `ile-arch`, are the template's own two symbols), exact at every step: from 64 rem on the page's 12 columns (24 px
#: gutters; the container's content 1 360 / 1 240 / 1 096 px, 100vw − 80 below 75 rem) the first time's frame 4/12
#: (its notice on the 2/12 beside it) and the second's 6/12; below, the text column's width (the node's 48 px and its
#: 20 px gap taken from the page's margins 24 / 20 px), at the 34 rem measure once the column is wider
TRAVERSATA_BEFORE_SIZES = (
    "(min-width: 100rem) 27.3333rem, (min-width: 90rem) 24.8333rem, (min-width: 75rem) 21.8333rem, "
    "(min-width: 64rem) calc(33.3333vw - 2.6667rem), (min-width: 41.25rem) 34rem, "
    "(min-width: 26.875rem) calc(100vw - 7.25rem), calc(100vw - 6.75rem)"
)
TRAVERSATA_AFTER_SIZES = (
    "(min-width: 100rem) 41.75rem, (min-width: 90rem) 38rem, (min-width: 75rem) 33.5rem, "
    "(min-width: 64rem) calc(50vw - 3.25rem), (min-width: 41.25rem) 34rem, "
    "(min-width: 26.875rem) calc(100vw - 7.25rem), calc(100vw - 6.75rem)"
)


def route_board(entries: list[IndexEntry], lang_attr: str = "") -> list[dict]:
    """PA-1 «il tracciato delle famiglie»: the eight locked pathways on their family's lane, in the prescribed order
    (the numerals say it), each station its PATHWAY glyph; a station links its sheet only while the sheet is live."""
    lanes = []
    for family, _keys in PATHWAY_FAMILIES:
        stations = [
            {
                "key": entry.key,
                "num": f"{entry.order:02d}",
                "glyph": entry.icon,
                "title": entry.title,
                "line": entry.description,
                "url": entry.url,
                "lang": lang_attr,
            }
            for entry in entries
            if entry.family == family
        ]
        if stations:
            label, frame = FAMILY_LABELS[family], FAMILY_FRAMES[family]
            lanes.append({"key": family, "label": label, "frame_slot": frame, "stations": stations})
    # the fork (round 2, m9): two one-station lanes in a row share the board's last row from 48 rem — the first of the
    # pair at the trunk, the second continuing its rail; every other lane keeps its row and the head's width
    for lane in lanes:
        lane["fork"], lane["frame_sizes"] = "", FAMILY_SIZES_V2
    for first, second in zip(lanes, lanes[1:], strict=False):
        if len(first["stations"]) == len(second["stations"]) == 1 and not first["fork"]:
            first["fork"], first["frame_sizes"] = "start", FAMILY_SIZES_FORK_START
            second["fork"], second["frame_sizes"] = "end", FAMILY_SIZES_FORK_END
    return lanes


def how_steps(how: HowItWorks | None, links: dict) -> list[dict]:
    """PA-2 (§3.4): the four fragments of the locked sentence as station plates, each its glyph (icons.HOW_STEP);
    station 1 leads to the questionnaire and station 3 to /formation/ (where they answer); 2 and 4 stay text."""
    if how is None:
        return []
    targets = {0: links.get("orientation", ""), 2: links.get("training", "")}
    glyphs = icons.HOW_STEP if len(how.steps) == len(icons.HOW_STEP) else ("",) * len(how.steps)
    return [
        {"text": text, "glyph": glyphs[index], "url": targets.get(index, ""), "last": index == len(how.steps) - 1}
        for index, text in enumerate(how.steps)
    ]


#: «Dans l'Espace Personnes» as a grid (§3.4 PA-3, §3.9 F2, §3.10 D3): the space's other areas, their concept glyphs
SPACE_TILES: tuple[tuple[str, object, object, str], ...] = (
    ("training", _("Formation"), _("avant le départ et après l’arrivée"), "presentation"),
    ("diplomas", _("Diplômes et titres étrangers"), "", "award"),
    ("living", _("Vivre en Italie"), "", "sprout"),
    ("faq", _("Questions fréquentes"), "", "circle-help"),
    ("glossary", _("Glossaire"), _("les termes italiens expliqués"), "book-a"),
)


def space_tiles(links: dict, current: str = "", lead: str = "training") -> list[dict]:
    """The grid's tiles: the areas whose app answers, the page's own left out, `lead` the wide tile, first."""
    tiles = [
        {"key": key, "href": links.get(key, ""), "title": title, "line": line, "glyph": glyph, "lead": key == lead}
        for key, title, line, glyph in SPACE_TILES
        if links.get(key) and key != current
    ]
    return sorted(tiles, key=lambda tile: not tile["lead"])


def sheet_milestones(steps: list[PublicItem], page_lang: str) -> list[dict]:
    """PS-1 «il filo»: a sheet's steps as milestones (the CMS seed headings, pending: headings only), each with its
    glyph when the sheet has the five generic steps (icons.SHEET_STEP) — a register's glyphs are all or none."""
    glyphs = icons.SHEET_STEP if len(steps) == len(icons.SHEET_STEP) else ("",) * len(steps)
    return [
        {
            "num": f"{index:02d}",
            "glyph": glyphs[index - 1],
            "heading": step.heading,
            "lang": step.lang if step.lang != page_lang else "",
            "body": step.body,
            "pending": step.pending,
        }
        for index, step in enumerate(steps, start=1)
    ]


def glossary_terms(slugs, page_lang: str) -> list[dict]:
    """PS-4 / D1 (§3.5, §3.10): the locked terms with their locked definitions (p3.glossary.terms, verbatim: the term in
    Italian, the definition in its own language), each with its term page."""
    terms, effective = locked_content.get("p3.glossary.terms", page_lang)
    index = {term["key"]: term for term in terms}
    out = []
    for slug in slugs:
        term = index.get(slug)
        if not term:
            continue
        out.append(
            {
                "slug": slug,
                "term": term["term"],
                "definition": term.get("definition", ""),
                "definition_lang": "" if effective == page_lang else effective,
                "url": _safe_reverse("glossary:term", slug=slug),
            }
        )
    return out


def diploma_dossier(page_lang: str) -> list[dict]:
    """D1 «le dossier, pièce par pièce» (§3.10): the five pending stations (headings only — DIPLOMA_STEPS), each its
    glyph (icons.DIPLOMA_STEP); stations 3–5 carry the locked definition of their term, stations 1–2 none; the first
    station with a definition stands open at load."""
    steps = []
    for index, step in enumerate(DIPLOMA_STEPS):
        steps.append(
            {
                "id": step["id"],
                "label": step["label"],
                "glyph": icons.DIPLOMA_STEP[index] if index < len(icons.DIPLOMA_STEP) else "",
                "terms": glossary_terms(step["glossary"], page_lang),
                "pending": True,
                "open": False,
            }
        )
    first = next((step for step in steps if step["terms"]), None)
    if first:
        first["open"] = True
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
    "FAMILY_SIZES_FORK_END",
    "FAMILY_SIZES_FORK_START",
    "FAMILY_SIZES_V2",
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
    "diploma_dossier",
    "diploma_steps",
    "eligibility_context",
    "gated_pages_visible",
    "generic_authority_names",
    "glossary_terms",
    "get_live_pathway",
    "get_pathway_for_preview",
    "glossary_links",
    "how_it_works",
    "how_steps",
    "index_entries",
    "phase3_open",
    "public_documents",
    "public_steps",
    "public_warnings",
    "related_links",
    "route_board",
    "sheet_milestones",
    "space_tiles",
]
