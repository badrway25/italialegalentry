"""
Ecosystem spaces — business logic (views stay thin).

* Gate handling: the Espace Entreprises is Phase 1 and never gated; Institutions, Universités et
  Formation and the Projet Pilote answer only while gate G3 (``phase3_public``) is open, or for a
  back-office user asking for ``?preview=1`` (rendered with ``noindex``).
* Prescribed texts are read from the locked registry only (``cms.locked_content``); the helpers
  below never rewrite them. ``split_enumeration`` cuts a prescribed sentence on ``:`` / ``;`` /
  ``,`` for *presentation* (a styled list) and is covered by a word-for-word integrity test.
* Photography comes from ``cms.MediaAsset`` (self-hosted, licence recorded). When the asset is one
  of the curated photos of ``static/img/photos/manifest.json`` the responsive WebP derivatives are
  used inside a ``<picture>``; any other asset falls back to its stored file.
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from functools import lru_cache

from django.conf import settings
from django.templatetags.static import static
from django.urls import NoReverseMatch, reverse
from django.utils.html import escape
from django.utils.safestring import SafeString, mark_safe
from django.utils.translation import gettext_lazy as _

from cms import locked_content, locked_split
from cms.translation import resolve
from core import gates, icons
from core.links import public_url
from ecosystem.models import GATE_PHASE3, PILOT_SEQUENCE_KEY, EcosystemSpace, PilotStep, SpaceKey

log = logging.getLogger("ile.ecosystem")

RECRUITMENT_FAQ_KEY = "faq_recruitment_agency"
PHOTO_SIZES = "(min-width: 64rem) 52rem, 100vw"


# --------------------------------------------------------------------------------------------
# Page registry
# --------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class SpaceSpec:
    key: str
    url_name: str
    path: str  # relative to the language prefix (registered in core.public_routes)
    gate: str  # "" → Phase 1, never gated
    photo_slot: str  # usage_slot of static/img/photos/manifest.json
    nav_label: object  # lazy translation
    order: int


SPACES: dict[str, SpaceSpec] = {
    SpaceKey.COMPANIES: SpaceSpec(
        SpaceKey.COMPANIES, "ecosystem:companies", "entreprises/", "", "entrance_company", _("Entreprises"), 10
    ),
    SpaceKey.INSTITUTIONS: SpaceSpec(
        SpaceKey.INSTITUTIONS,
        "ecosystem:institutions",
        "institutions/",
        GATE_PHASE3,
        "entrance_institution",
        _("Institutions"),
        20,
    ),
    SpaceKey.UNIVERSITIES: SpaceSpec(
        SpaceKey.UNIVERSITIES,
        "ecosystem:universities",
        "universites-et-formation/",
        GATE_PHASE3,
        "entrance_university",
        _("Universités et formation"),
        30,
    ),
    SpaceKey.PILOT: SpaceSpec(
        SpaceKey.PILOT, "ecosystem:pilot", "projet-pilote/", GATE_PHASE3, "workshop", _("Projet pilote"), 40
    ),
}


def ungated_paths() -> list[str]:
    return [spec.path for spec in SPACES.values() if not spec.gate]


def gated_paths() -> list[str]:
    return [spec.path for spec in SPACES.values() if spec.gate]


# --------------------------------------------------------------------------------------------
# Gates
# --------------------------------------------------------------------------------------------
def gate_open(key: str) -> bool:
    """Phase 1 pages are always open; Phase 3 pages follow gate G3 and nothing else."""
    spec = SPACES[key]
    if not spec.gate:
        return True
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


def page_visible(request, key: str) -> tuple[bool, bool]:
    """(visible, is_preview)."""
    if gate_open(key):
        return True, False
    if can_preview(request):
        return True, True
    return False, False


# --------------------------------------------------------------------------------------------
# Locked texts
# --------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class LockedText:
    key: str
    text: str
    lang: str  # effective language of the prescribed text
    lang_attr: str  # value for a ``lang`` attribute: "" when it matches the page language


def _page_lang(lang: str | None) -> str:
    return (lang or settings.LANGUAGE_CODE).split("-")[0]


def locked_text(key: str, lang: str | None) -> LockedText:
    value, effective = locked_content.get(key, lang)
    if not isinstance(value, str):
        raise TypeError(f"Locked key {key!r} is not a plain string")
    return LockedText(key, value, effective, "" if effective == _page_lang(lang) else effective)


@dataclass(frozen=True)
class Enumeration:
    """A prescribed sentence cut for presentation. ``source`` stays the only authoritative text."""

    source: LockedText
    label: str  # part before the colon, colon removed ("" when the sentence has no colon)
    label_items: tuple[str, ...]  # the same part cut on , ;
    items: tuple[str, ...]  # part after the colon cut on , ;


_SEPARATORS = re.compile(r"[;,]")
_WORD = re.compile(r"[^\s,;:.]+")


def _cut(text: str) -> tuple[str, ...]:
    parts = (part.strip().rstrip(".").strip() for part in _SEPARATORS.split(text))
    return tuple(part for part in parts if part)


def words(text: str) -> list[str]:
    """Words of a sentence, punctuation-free — used to prove that a cut never alters the wording."""
    return _WORD.findall(text)


def split_enumeration(source: LockedText) -> Enumeration:
    head, colon, tail = source.text.partition(":")
    if not colon:
        head, tail = "", source.text
    return Enumeration(source=source, label=head.strip(), label_items=_cut(head), items=_cut(tail))


def enumeration(key: str, lang: str | None) -> Enumeration:
    return split_enumeration(locked_text(key, lang))


# --------------------------------------------------------------------------------------------
# Editorial layer (photo + optional note)
# --------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class Photo:
    src: str
    webp_srcset: str
    sizes: str
    alt: str
    alt_lang: str  # "" when the alternative text is in the page language
    width: int
    height: int
    share_image: str  # path for og:image
    #: V5.24 §2 (label v524-px): the entrance's caption draws a byline only when the asset's licence demands it
    #: (``cms.MediaAsset.attribution_required``) — the same contract as ``pages.services.Photo``.
    attribution_required: bool = False


@dataclass(frozen=True)
class Note:
    text: str
    lang_attr: str


def get_space(key: str, *, preview: bool = False) -> EcosystemSpace | None:
    """
    The live editorial row of a page, or None (the page then renders its prescribed texts only).
    A back-office preview also sees a row that is scheduled or still in draft.
    """
    rows = EcosystemSpace.objects.all() if preview else EcosystemSpace.objects.live()
    return rows.filter(key=key).select_related("hero_image").prefetch_related("translations").first()


def editorial_note(space: EcosystemSpace | None, lang: str | None) -> Note | None:
    if space is None:
        return None
    page_lang = _page_lang(lang)
    row, _effective, _is_fallback = resolve(space, page_lang)
    if row is not None and row.language == page_lang and row.intro_note.strip():
        return Note(row.intro_note.strip(), "")
    source = space.intro_note_fr.strip()
    if not source:
        return None
    fallback = settings.CONTENT_FALLBACK_LANGUAGE
    return Note(source, "" if page_lang == fallback else fallback)


@lru_cache(maxsize=1)
def _manifest_by_source_url() -> dict[str, dict]:
    from cms.seeds_media import MediaSeedError, load_manifest

    try:
        return {entry["source_url"]: entry for entry in load_manifest()}
    except (MediaSeedError, OSError, ValueError) as exc:  # unreadable manifest: photos fall back to the stored file
        log.warning("photo manifest unavailable: %s", exc)
        return {}


def manifest_entry_for_slot(slot: str) -> dict | None:
    for entry in _manifest_by_source_url().values():
        if entry["usage_slot"] == slot:
            return entry
    return None


def _static_or_empty(path: str) -> str:
    try:
        return static(path)
    except ValueError:  # manifest storage without that file
        return ""


def photo_for(space: EcosystemSpace | None, lang: str | None) -> Photo | None:
    """
    The space's photograph, or None.

    Same rule as ``pages.services.photo_from_asset``: an asset that cannot fill its caption
    apparatus — place, date, a factual sentence, a credit — renders nowhere. See
    ``cms.MediaAsset.is_publishable`` and art direction A §6.2.
    """
    asset = space.hero_image if space is not None else None
    if asset is None or not asset.file:
        return None
    if not asset.is_publishable:
        return None
    page_lang = _page_lang(lang)
    alt = "" if asset.is_decorative else asset.alt(page_lang)
    own_alt = getattr(asset, f"alt_{page_lang}", "")
    alt_lang = "" if (not alt or own_alt or page_lang == "fr") else "fr"

    entry = _manifest_by_source_url().get(asset.source_url) if asset.source_url else None
    if entry:
        webp = entry["files"].get("webp") or {}
        candidates = [
            (int(width), _static_or_empty(f"img/photos/{name}")) for width, name in sorted(webp.items(), key=_by_width)
        ]
        srcset = ", ".join(f"{url} {width}w" for width, url in candidates if url)
        jpg = _static_or_empty(f"img/photos/{entry['files']['jpg']}")
        if jpg:
            width = 1440
            height = round(width * entry["height"] / entry["width"]) if entry.get("width") else 960
            return Photo(
                jpg,
                srcset,
                PHOTO_SIZES,
                alt,
                alt_lang,
                width,
                height,
                jpg,
                attribution_required=asset.attribution_required,
            )
    try:
        url = asset.file.url
    except ValueError:
        return None
    return Photo(
        url,
        "",
        PHOTO_SIZES,
        alt,
        alt_lang,
        asset.width or 1440,
        asset.height or 960,
        url,
        attribution_required=asset.attribution_required,
    )


def _by_width(item: tuple[str, str]) -> int:
    return int(item[0])


# --------------------------------------------------------------------------------------------
# Navigation and cross-links (other apps' routes resolve lazily: "" while a route is missing)
# --------------------------------------------------------------------------------------------
def safe_reverse(name: str, **kwargs) -> str:
    try:
        return reverse(name, kwargs=kwargs or None)
    except NoReverseMatch:
        return ""


def _with_preview(url: str, preview: bool) -> str:
    return f"{url}?preview=1" if (url and preview) else url


def space_url(key: str, *, preview: bool = False) -> str:
    """URL of a space, "" while its gate is closed (so templates never link to a 404)."""
    spec = SPACES[key]
    if gate_open(key):
        return reverse(spec.url_name)
    return _with_preview(reverse(spec.url_name), True) if preview else ""


def local_nav(current: str, sections: list[tuple], *, preview: bool = False) -> list[dict]:
    """Items for components/local_nav.html: the visible spaces; the current one lists its sections."""
    items = []
    for key, spec in SPACES.items():
        url = space_url(key, preview=preview)
        if not url:
            continue
        item = {"label": spec.nav_label, "url": url, "current": key == current}
        if key == current:
            # a section is (anchor, label) or (anchor, label, lang) when its label is a prescribed French text
            item["children"] = [
                {"label": sec[1], "url": f"#{sec[0]}", "current": False, "lang": sec[2] if len(sec) > 2 else ""}
                for sec in sections
            ]
        items.append(item)
    return items


def related_links(*, preview: bool = False) -> dict[str, str]:
    phase3 = gates.phase3_public()
    return {
        "company_needs": safe_reverse("enquiries:company_needs"),
        "institution_proposal": safe_reverse("enquiries:institution_proposal"),
        "university_proposal": safe_reverse("enquiries:university_proposal"),
        "forum": public_url("forum:index"),  # V5.12 §8: with a live edition
        "partners": public_url("partners:index"),  # V5.12 §8: once a partner is authorised
        "pilot": space_url(SpaceKey.PILOT, preview=preview),
        "institutions": space_url(SpaceKey.INSTITUTIONS, preview=preview),
        "universities": space_url(SpaceKey.UNIVERSITIES, preview=preview),
        "pathways": safe_reverse("pathways:index"),
        # Phase 3 routes of sibling apps: linked only while they answer.
        "training": safe_reverse("pathways:training") if phase3 else "",
        "faq": safe_reverse("faq:index") if phase3 else "",
    }


# --------------------------------------------------------------------------------------------
# Espace Entreprises
# --------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class Guarantee:
    question: str
    answer: str
    lang_attr: str
    faq_url: str


def recruitment_guarantee(lang: str | None) -> Guarantee | None:
    """
    Transparency block of the Espace Entreprises, built from the prescribed FAQ answer
    ``faq_recruitment_agency``. The FAQ is Phase 3 content (§3.8.2): the block exists only while
    gate G3 is open, so no Phase 3 wording is published early.
    """
    if not gates.phase3_public():
        return None
    try:
        entries, effective = locked_content.get("p3.faq.items", lang)
    except locked_content.LockedContentMissing:
        return None
    entry = next((e for e in entries if e.get("key") == RECRUITMENT_FAQ_KEY), None)
    if entry is None:
        return None
    faq_url = safe_reverse("faq:index")
    return Guarantee(
        question=entry["question"],
        answer=entry["answer"],
        lang_attr="" if effective == _page_lang(lang) else effective,
        faq_url=f"{faq_url}#{RECRUITMENT_FAQ_KEY}" if faq_url else "",
    )


def company_moments() -> list[dict]:
    """
    The three neutral moments of the approach (UI wording, French source — never a selection, a
    ranking or a list of candidate profiles). CONTENT_PENDING_LEGAL_REVIEW: wording kept to the
    vocabulary of the prescribed introduction, without any procedural or legal statement.
    """
    return [
        {
            "label": _("Recueil des besoins"),
            "text": _("Votre entreprise décrit ses besoins professionnels au moyen du formulaire."),
        },
        {
            "label": _("Construction des parcours avec les acteurs compétents"),
            "text": _(
                "Les besoins recueillis sont le point de départ des parcours, construits avec les acteurs compétents."
            ),
        },
        {
            "label": _("Formation et mobilité régulière"),
            "text": _("Les parcours portent sur la formation et sur la mobilité régulière."),
        },
    ]


# --------------------------------------------------------------------------------------------
# Projet Pilote — the prescribed sequence
# --------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class FlowStep:
    number: str  # "01" … "08"
    label: str
    locked: bool


@dataclass(frozen=True)
class PilotFlow:
    steps: tuple[FlowStep, ...]
    lang_attr: str
    additions_lang_attr: str = ""
    locked_count: int = 0


def pilot_flow(lang: str | None) -> PilotFlow:
    """
    The diagram data. The eight prescribed labels ALWAYS come from the registry, in the prescribed
    order, whatever the database says (gate G0). Editorial additions (never part of the prescribed
    sequence) follow it, only when an editor made them visible.
    """
    sequence, effective = locked_content.get(PILOT_SEQUENCE_KEY, lang)
    page_lang = _page_lang(lang)
    steps = [FlowStep(f"{index:02d}", label, True) for index, label in enumerate(sequence, start=1)]
    additions = list(PilotStep.objects.visible_additions().order_by("order"))
    for offset, row in enumerate(additions, start=len(steps) + 1):
        steps.append(FlowStep(f"{offset:02d}", row.label_fr, False))
    fallback = settings.CONTENT_FALLBACK_LANGUAGE
    return PilotFlow(
        steps=tuple(steps),
        lang_attr="" if effective == page_lang else effective,
        additions_lang_attr="" if page_lang == fallback else fallback,
        locked_count=len(sequence),
    )


# --------------------------------------------------------------------------------------------
# V5.22 — Page Composition V2 (SECTION_SYSTEM_V2 §3.3, §3.6–§3.8; lane P1): the data the four spaces' compositions
# draw. Every word is the registry's or a catalogue msgid, cut at render on its own separators (cms.locked_split: the
# parts rebuild the text character for character, or there is no cut and the text stands whole) — never retyped. The
# glyphs are the registry's (core.icons: PILOT_STATION, COMPANY_MOMENT, RECIPIENT_SEAT).
# --------------------------------------------------------------------------------------------
def pilot_stations(flow: PilotFlow) -> list[dict]:
    """«la linea V2» of PP-1 (§3.3): each station its label — the locked eight in their order, then any editorial
    addition — and its concept glyph (icons.PILOT_STATION, the eight drawn: a register's glyphs all or none, §4.10;
    the page's T1 seal stands beside the section's title). `lang` only where the label's language is not the page's."""
    stations = []
    for index, step in enumerate(flow.steps):
        glyph = icons.PILOT_STATION[index] if step.locked and index < len(icons.PILOT_STATION) else ""
        stations.append(
            {"label": step.label, "glyph": glyph, "lang": flow.lang_attr if step.locked else flow.additions_lang_attr}
        )
    return stations


def pilot_doors() -> dict:
    """PP-2 «due porte» (§3.3): the team sentence cut at its own full stop — the companies' half on the night door, the
    institutions' on the paper one. A translation that does not cut in two stands whole under both doors."""
    text = str(_("Entreprises : signalez vos besoins professionnels. Institutions : proposez une collaboration."))
    glyphs = {"company_glyph": icons.AUDIENCE["company"], "institution_glyph": icons.AUDIENCE["institution"]}
    parts = locked_split.sentences(text)
    if not parts or len(parts) != 2:  # noqa: PLR2004 — two doors, two halves
        return {"whole": text, **glyphs}
    return {"company": parts[0].strip(), "institution": parts[1].strip(), **glyphs}


def company_flow() -> list[dict]:
    """EN-1 «il flusso» (§3.6): the three moments (team strings, CONTENT_PENDING_LEGAL_REVIEW) on their measured curve,
    each with its registry glyph (icons.COMPANY_MOMENT)."""
    return [
        {"glyph": glyph, "label": moment["label"], "text": moment["text"]}
        for glyph, moment in zip(icons.COMPANY_MOMENT, company_moments(), strict=True)
    ]


def guarantee_split(guarantee: Guarantee | None) -> SafeString | None:
    """EN-4 (§3.6): the prescribed answer cut for the split — its own first word («Non.») as the large keyword, what the
    platform does not do up to and including its colon, then what it does — three spans of ONE paragraph whose
    textContent is the answer itself. None when the answer has no such shape (the template then prints it whole)."""
    if guarantee is None:
        return None
    lead = locked_split.keyword(guarantee.answer)
    if not lead:
        return None
    halves = locked_split.split(lead[1], ":")
    if not halves or len(halves) != 2:  # noqa: PLR2004 — the colon cuts the answer in two
        return None
    parts = (lead[0], *halves)
    if "".join(parts) != guarantee.answer:
        return None
    return locked_split.spans(parts, css="giu")


def recipients_sentence(recipients: Enumeration) -> SafeString:
    """IN-1 «l'emiciclo» (§3.7): the locked sentence whole, its own head («Destinataires :») and each enumerated item
    as spans — the items carry the seat they light (data-seggio 1 … 6, the pattern's own attribute: components/sezioni/
    mappa.html, v5/_sec-emiciclo.css; never Lume's L3 seat, DS 2026 §12 — v522-s2, DL54-182 item 10 b). The textContent
    is the sentence itself; an item not found in order leaves the sentence unwrapped."""
    text = recipients.source.text
    head, colon, _rest = text.partition(":")
    out, at = [], 0
    if colon and recipients.label:
        end = len(head) + len(colon)
        out.append(f'<span class="emiciclo__capo">{escape(text[:end])}</span>')
        at = end
    for number, item in enumerate(recipients.items, start=1):
        found = text.find(item, at)
        if found < 0:
            return escape(text)
        out.append(escape(text[at:found]))
        out.append(f'<span class="emiciclo__voce" data-seggio="{number}">{escape(item)}</span>')
        at = found + len(item)
    out.append(escape(text[at:]))
    return mark_safe("".join(out))  # noqa: S308 — every slice is escaped here


def recipient_seats(recipients: Enumeration) -> list[dict]:
    """The hemicycle's seats: one a recipient, its glyph the registry's (icons.RECIPIENT_SEAT), never more seats than
    the sentence names."""
    return [{"glyph": glyph, "audience": "institution"} for glyph in icons.RECIPIENT_SEAT[: len(recipients.items)]]


#: U1's arrival node: the brand's arch, the page's one gold arrival (§3.8, §4.5)
ARRIVAL = "ile-arch"
#: U1's destination frame (`universities.exchange`): the slot's own 6/12 track from 64 rem (imagery.py); from 48 to
#: 64 rem three quarters of the container, smaller than the slot's full width (lane M's note, QA/v522/m §9.10: the
#: gesture read at 768); the column below — the width the composition really draws, for the browser's choice
DESTINATION_SIZES = (
    "(min-width: 100rem) 41.75rem, (min-width: 90rem) 38rem, (min-width: 75rem) 33.5rem, "
    "(min-width: 64rem) calc(50vw - 3.25rem), (min-width: 48rem) calc(75vw - 3.75rem), "
    "(min-width: 26.875rem) calc(100vw - 3rem), calc(100vw - 2.5rem)"
)


def universities_route(lang: str | None, links: dict) -> list[dict]:
    """U1 «la filiera di formazione» (§3.8): three stations of the persons' learning path — before the departure, in
    Italy (the research pathway branching off), after the arrival — each with its team kicker, the locked title and
    its one locked line, and its links (a pathway sheet only while it is live)."""
    from pathways import services as pathways

    page_lang = _page_lang(lang)
    entries = {entry.key: entry for entry in pathways.index_entries()}
    _pathways, pathways_lang = locked_content.get("p3.persons.pathways", page_lang)
    entry_lang = "" if pathways_lang == page_lang else pathways_lang
    after_title, after_lang = locked_content.get("p3.training_after.title", page_lang)
    after_body, _body_lang = locked_content.get("p3.training_after.body", page_lang)
    first = locked_split.sentences(after_body)
    training = links.get("training", "")

    def station(key: str) -> dict:
        entry = entries[key]
        return {"title": entry.title, "line": entry.description, "lang": entry_lang, "url": entry.url, "glyph": ""}

    before = station("training_in_origin_country") | {
        "kicker": _("Avant le départ"),
        "glyph": "earth",
        "more": {"url": f"{training}#avant-le-depart", "label": _("Formation avant le départ")} if training else None,
    }
    italy = station("study_and_training_in_italy") | {
        "kicker": _("En Italie"),
        "glyph": icons.PATHWAY["study_and_training_in_italy"],
        "branch": station("scientific_research") | {"glyph": icons.PATHWAY["scientific_research"]},
    }
    after = {
        "kicker": _("Après l’arrivée"),
        "glyph": icons.PATHWAY["training_in_origin_country"],
        "title": after_title,
        "line": first[0].strip() if first else "",
        "lang": "" if after_lang == page_lang else after_lang,
        "url": f"{training}#apres-l-arrivee" if training else "",
    }
    return [before, italy, after]


# --------------------------------------------------------------------------------------------
# SEO
# --------------------------------------------------------------------------------------------
def seo(title: str, description: str, photo: Photo | None) -> dict:
    data = {"title": title, "description": description, "type": "website"}
    if photo is not None and photo.share_image:
        data["image"] = photo.share_image
    return data


def page_jsonld(request, *, name: str, description: str, crumbs: list[dict], lang: str | None) -> SafeString:
    """schema.org WebPage + BreadcrumbList. No organisation type is asserted here (never a public body)."""
    origin = f"{request.scheme}://{request.get_host()}"
    trail = [{"label": str(_("Accueil")), "url": safe_reverse("pages:home") or f"/{_page_lang(lang)}/"}]
    trail += [{"label": str(c["label"]), "url": c.get("url") or request.path} for c in crumbs]
    data = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": name,
        "description": description,
        "inLanguage": _page_lang(lang),
        "url": f"{origin}{request.path}",
        "breadcrumb": {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": position, "name": crumb["label"], "item": f"{origin}{crumb['url']}"}
                for position, crumb in enumerate(trail, start=1)
            ],
        },
    }
    dumped = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    dumped = dumped.replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
    return mark_safe(dumped)  # noqa: S308 - escaped above
