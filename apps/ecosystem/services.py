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
from django.utils.safestring import SafeString, mark_safe
from django.utils.translation import gettext_lazy as _

from cms import locked_content
from cms.translation import resolve
from core import gates
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
            return Photo(jpg, srcset, PHOTO_SIZES, alt, alt_lang, width, height, jpg)
    try:
        url = asset.file.url
    except ValueError:
        return None
    return Photo(url, "", PHOTO_SIZES, alt, alt_lang, asset.width or 1440, asset.height or 960, url)


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
        "forum": safe_reverse("forum:index"),
        "partners": safe_reverse("partners:index"),
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
