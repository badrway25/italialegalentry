"""
Homepage and institutional pages — business logic (views stay thin).

Rules enforced here, not in templates:

* **Prescribed texts** are read only through ``cms.locked_content.get()`` and handed to the templates
  together with their effective language (French fallback is tagged ``lang="fr"``).
* **Gates**: Phase 3 texts are never put in a context while ``core.gates.phase3_public()`` is
  closed, whatever the back-office rows say (defence in depth on top of ``HomeSection.requires_gate``).
* **Composition**: the homepage is the ordered list of live, enabled ``HomeSection`` rows whose gate
  is open and whose builder returned content. A section without content is skipped, never rendered
  as an empty box.
* **Editorial strings** stored in the database go through gettext so untouched defaults follow the
  ``.po`` catalogues; a text containing a forbidden formulation is never rendered.
"""

from __future__ import annotations

import json
import logging
from collections.abc import Callable
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Any

from django.conf import settings
from django.templatetags.static import static
from django.urls import NoReverseMatch, reverse
from django.utils import formats, translation
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from cms import forbidden, locked_content
from cms.models import HeroVariant, HomeHero, MediaAsset
from cms.templatetags.cms_nav import gate_open
from cms.translation import resolve
from core import flags, gates
from core.models import SiteSettings
from pages import content, prescribed
from pages.models import HomeSection, SectionKey

log = logging.getLogger("ile.pages")

FALLBACK_LANGUAGE = settings.CONTENT_FALLBACK_LANGUAGE


# --------------------------------------------------------------------------------------------
# Small helpers
# --------------------------------------------------------------------------------------------
def current_language() -> str:
    return (translation.get_language() or settings.LANGUAGE_CODE).split("-")[0]


def safe_reverse(name: str, **kwargs) -> str:
    """URL of a (possibly not yet available) route; "" when it does not resolve."""
    if not name:
        return ""
    try:
        return reverse(name, kwargs=kwargs or None)
    except NoReverseMatch:
        return ""


def first_url(names: tuple[str, ...] | list[str]) -> str:
    for name in names:
        url = safe_reverse(name)
        if url:
            return url
    return ""


@dataclass(frozen=True)
class Text:
    """A renderable string with the ``lang`` attribute it needs ("" = page language)."""

    value: Any = ""
    lang: str = ""

    def __bool__(self) -> bool:
        return bool(self.value)

    def __str__(self) -> str:
        return str(self.value)


EMPTY = Text()


def locked(key: str, lang: str | None = None) -> Text:
    """Prescribed text (str, list or dict) with its effective language — the only door to the registry."""
    lang = lang or current_language()
    value, effective = locked_content.get(key, lang)
    return Text(value, "" if effective == lang else effective)


def is_clean(value: str) -> bool:
    """False when an editorial string contains a forbidden formulation (cms.forbidden)."""
    return not forbidden.scan(value or "")


def is_publishable(value: str) -> bool:
    """
    False when an editorial string carries Phase 3 prescribed wording while gate G3 is closed.

    Editorial columns (``HomeSection``, ``cms.HomeHero``, translation rows) are free text: a Phase 3
    sentence pasted there must not become public before the gate, whatever the back-office holds.
    The gate is only evaluated when a fragment is actually found.
    """
    if not prescribed.phase3_only(value or ""):
        return True
    return gates.phase3_public()


def editorial(value: Any, lang: str | None = None, default: Any = "") -> Text:
    """
    Editorial (non-prescribed) French source string → text for the current language.

    An untouched seeded default is a gettext msgid and gets translated by the catalogues; an
    editor-written value has no catalogue entry and is shown in French with ``lang="fr"``.
    """
    lang = lang or current_language()
    source = str(value or "").strip()
    if source and not is_clean(source):
        log.warning("Editorial text dropped: forbidden formulation detected.")
        source = ""
    if source and not is_publishable(source):
        log.warning("Editorial text dropped: Phase 3 prescribed wording while gate G3 is closed.")
        source = ""
    if not source:
        source = str(default or "").strip()
    if not source:
        return EMPTY
    if lang == FALLBACK_LANGUAGE:
        with translation.override(FALLBACK_LANGUAGE):
            return Text(gettext(source), "")
    translated = gettext(source)
    if translated != source:
        return Text(translated, "")
    return Text(source, FALLBACK_LANGUAGE)


def ui(message: Any) -> Text:
    """A code-level gettext string (French source) with the right ``lang`` attribute."""
    return editorial(str_source(message))


def str_source(message: Any) -> str:
    """French msgid of a lazy string, whatever the active language."""
    with translation.override(None):
        return str(message)


# --------------------------------------------------------------------------------------------
# Photography — cms.MediaAsset rows seeded from static/img/photos/manifest.json
# --------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class Photo:
    src: str
    srcset: str
    alt: str
    alt_lang: str
    width: int
    height: int
    share_path: str = ""  # JPG used for social previews
    #: The archive caption. A photograph on this site says where, when, what and by whom — a plate
    #: in a register, not an illustration. ``photo_from_asset`` refuses to build a Photo whose asset
    #: cannot fill these, so an uncaptioned image cannot reach a template at all.
    place: str = ""
    date: object = None
    caption: str = ""
    credit: str = ""


@lru_cache(maxsize=1)
def _manifest() -> dict[str, dict]:
    from cms.seeds_media import MANIFEST_PATH

    try:
        data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return {entry["slug"]: entry for entry in data.get("images", []) if "slug" in entry}


def _note_value(notes: str, name: str) -> str:
    for part in (notes or "").split(";"):
        label, _sep, value = part.strip().partition("=")
        if label == name:
            return value.strip()
    return ""


def asset_for_slot(slot: str) -> MediaAsset | None:
    """The library photo curated for a usage slot (recorded by the media seed in ``license_notes``)."""
    return MediaAsset.objects.filter(license_notes__contains=f"slot={slot};").order_by("pk").first()


def photo_from_asset(asset: MediaAsset | None, lang: str | None = None) -> Photo | None:
    """
    Build a Photo, or refuse.

    An asset that cannot fill its caption apparatus — place, date, a factual sentence, a credit —
    does not become a Photo, so it reaches no template and renders nowhere. Art direction A §6.2
    makes a figure without a figcaption a defect; enforcing it HERE rather than in eleven templates
    is what makes anonymous stock photography structurally impossible instead of discouraged.

    The library inherited from the previous build fills none of those fields: six interchangeable
    frames served fifty-two pages, none captioned, none credited. Those assets therefore render
    nowhere until they are curated, and the pages carry themselves on type — which is the test the
    direction set for itself.
    """
    if asset is None or not asset.file:
        return None
    if not asset.is_publishable:
        log.info("Photo %s is not publishable: its caption apparatus is incomplete.", asset.pk)
        return None
    lang = lang or current_language()
    localized = getattr(asset, f"alt_{lang}", "")
    alt = "" if asset.is_decorative else (localized or asset.alt_fr)
    alt_lang = "" if (localized or lang == FALLBACK_LANGUAGE or not alt) else FALLBACK_LANGUAGE
    entry = _manifest().get(_note_value(asset.license_notes, "slug"))
    if entry:
        try:
            webp = entry["files"]["webp"]
            widths = sorted(int(w) for w in webp)
            srcset = ", ".join(f"{static('img/photos/' + webp[str(w)])} {w}w" for w in widths)
            jpg = "img/photos/" + entry["files"]["jpg"]
            ratio = entry["height"] / entry["width"]
            return Photo(
                src=static(jpg),
                srcset=srcset,
                alt=alt,
                alt_lang=alt_lang,
                width=1440,
                height=round(1440 * ratio),
                share_path=static(jpg),
                place=asset.caption_place,
                date=asset.caption_date,
                caption=asset.caption(lang),
                credit=asset.credit,
            )
        except (KeyError, ValueError, ZeroDivisionError):  # incomplete manifest entry or missing static file
            log.info("Photo derivatives unavailable for asset %s; using the stored file.", asset.pk)
    try:
        url = asset.file.url
    except ValueError:
        return None
    return Photo(
        src=url,
        srcset="",
        alt=alt,
        alt_lang=alt_lang,
        width=asset.width or 1440,
        height=asset.height or 960,
        place=asset.caption_place,
        date=asset.caption_date,
        caption=asset.caption(lang),
        credit=asset.credit,
    )


def photo_for_slot(slot: str, lang: str | None = None) -> Photo | None:
    return photo_from_asset(asset_for_slot(slot), lang)


# --------------------------------------------------------------------------------------------
# Homepage — section builders
# --------------------------------------------------------------------------------------------
@dataclass
class BuildContext:
    request: Any
    lang: str
    phase3: bool


@dataclass
class SectionView:
    key: str
    template: str
    anchor: str
    heading: Text = EMPTY
    intro: Text = EMPTY
    note: Text = EMPTY
    data: dict = field(default_factory=dict)


def _section_texts(row: HomeSection, lang: str) -> tuple[Text, Text, Text]:
    """Heading / intro / note: PUBLISHED translation row, else the (gettext-aware) French source."""
    if row.is_fully_locked:
        return EMPTY, EMPTY, EMPTY
    translated = None
    if row.pk and lang != FALLBACK_LANGUAGE:
        candidate, effective, is_fallback = resolve(row, lang)
        if candidate is not None and effective == lang and not is_fallback:
            translated = candidate

    def pick(tr_field: str, fr_field: str) -> Text:
        if translated is not None:
            value = (getattr(translated, tr_field, "") or "").strip()
            if value and is_clean(value) and is_publishable(value):
                return Text(value, "")
        # A field blanked by an editor stays blank: defaults are only what the seed wrote.
        return editorial(getattr(row, fr_field, ""), lang)

    heading = EMPTY if row.has_locked_heading else pick("heading", "heading_fr")
    return heading, pick("intro", "intro_fr"), pick("note", "note_fr")


# ---- 2. Hero ---------------------------------------------------------------------------------
CTA_FALLBACKS: dict[str, str] = {
    "ecosystem:companies": "enquiries:company_needs",
    "ecosystem:institutions": "enquiries:institution_proposal",
    "ecosystem:universities": "enquiries:university_proposal",
}
# Locked references an editor may use in the interim hero body: never a Phase 3 key.
INTERIM_LOCKED_PREFIXES: tuple[str, ...] = ("p1.",)


def _hero_row(variant: str) -> HomeHero:
    row = HomeHero.objects.live().filter(variant=variant).select_related("image").first()
    if row is not None:
        return row
    defaults = content.HERO_PHASE3 if variant == HeroVariant.PHASE3 else content.HERO_INTERIM
    return HomeHero(variant=variant, **{name: str_source(value) for name, value in defaults.items()})


def _cta(label: str, url_name: str, lang: str) -> dict | None:
    url = first_url([url_name, CTA_FALLBACKS.get(url_name, "")])
    text = editorial(label, lang)
    if not (url and text):
        return None
    return {"label": text, "url": url}


def _interim_body(raw: str, lang: str) -> tuple[Text, bool]:
    raw = (raw or "").strip()
    if raw.startswith(content.LOCKED_PREFIX):
        key = raw[len(content.LOCKED_PREFIX) :].strip()
        if key.startswith(INTERIM_LOCKED_PREFIXES):
            try:
                value = locked(key, lang)
            except locked_content.LockedContentMissing:
                return EMPTY, False
            if isinstance(value.value, str):
                return value, True
        return EMPTY, False
    return editorial(raw, lang), False


def build_hero(ctx: BuildContext) -> dict | None:
    variant = HeroVariant.PHASE3 if ctx.phase3 else HeroVariant.INTERIM
    row = _hero_row(variant)
    data: dict[str, Any] = {"variant": variant, "eyebrow": editorial(row.eyebrow_fr, ctx.lang)}
    if ctx.phase3:
        data.update(
            title=locked("p3.hero.title", ctx.lang),
            subtitle=locked("p3.hero.subtitle", ctx.lang),
            body=locked("p3.hero.body", ctx.lang),
            body_is_fragment=False,
        )
    else:
        body, is_locked = _interim_body(row.body_fr, ctx.lang)
        data.update(
            title=editorial(row.title_fr, ctx.lang, default=content.HERO_INTERIM["title_fr"]),
            subtitle=editorial(row.subtitle_fr, ctx.lang),
            body=body,
            body_is_fragment=is_locked,
        )
    data["primary"] = _cta(row.primary_cta_label_fr, row.primary_cta_url_name, ctx.lang)
    data["secondary"] = _cta(row.secondary_cta_label_fr, row.secondary_cta_url_name, ctx.lang)
    data["photo"] = photo_from_asset(row.image, ctx.lang) if row.image_id else photo_for_slot("hero", ctx.lang)
    data["exits"] = hero_exits(data["eyebrow"])
    data["legend"] = hero_legend(ctx.lang, ctx.phase3, with_exits=bool(data["exits"]))
    return data


# ---- 2b. The stage of the hero (design V4, docs/design-v4/CREATIVE_DIRECTION.md §4) ----------
# The no-JavaScript drawing of the four routes on the 640×520 stage: origins at the reading edge
# where the legend rows fall, one lane each through the solid navy of the inner arch (x 365–531)
# where the stroke dissolves — or, when the eyebrow names them, on to three exits at x 624.
# static/js/src/home.js re-anchors each route to its legend row once the page is laid out, so
# these values only have to be a sensible drawing when it has not.
STAGE_ORIGINS: tuple[tuple[int, int], ...] = ((34, 348), (34, 394), (34, 440), (34, 486))
# Which exit each actor's route reaches: persons → orientation, universities and training bodies →
# training, companies and institutions → regular mobility. The words are the eyebrow's.
STAGE_EXITS: dict[str, int] = {"person": 1, "university": 2, "company": 3, "institution": 3}
_EXIT_Y = {1: 200, 2: 300, 3: 400}


def _route_path(x0: int, y0: int, lane: int, exit_y: int, with_exits: bool) -> str:
    """The same curve home.js draws: into the arch, through the braid — the lane a route enters
    on is not the one it leaves on, the four cross in the middle of the navy — and out to the
    exit, if named."""
    # The braid sits at the threshold — the foot of the inner navy (its arch ends at y 397), not
    # halfway up the wall (round-2 review, correction 4).
    y_in = 372 + lane * 6
    y_out = 372 + (3 - lane) * 6
    c1 = round(x0 + (365 - x0) * 0.55)
    start = f"M{x0} {y0} C{c1} {y0}, 325 {y_in}, 365 {y_in}"
    if not with_exits:
        return f"{start} C448 {y_in}, 448 {y_out}, 531 {y_out}"
    # With named exits every crossing stays in the navy: the braid is shortened to x 496, each
    # route climbs (or drops) to its exit's height between x 496 and 520 — still inside the arch,
    # right of the key — and leaves the arch level, straight to its node. Round 3 climbed on the
    # stone jamb (x 531–555), where the risers crossed and ran within a casing of each other
    # (round-4 review, defect 13a); a route crossing an exit word's height further right struck
    # the word through (round 3, defect 8).
    return f"{start} C431 {y_in}, 431 {y_out}, 496 {y_out} C508 {y_out}, 508 {exit_y}, 520 {exit_y} H624"


def hero_legend(lang: str, phase3: bool, *, with_exits: bool = False) -> list[dict]:
    """The four entrances, with the geometry of their route on the stage."""
    items = entrances(lang, phase3)
    for lane, item in enumerate(items):
        x0, y0 = STAGE_ORIGINS[lane]
        exit_no = STAGE_EXITS.get(item["actor"], 2)
        item.update(x0=x0, y0=y0, exit=exit_no, path=_route_path(x0, y0, lane, _EXIT_Y[exit_no], with_exits))
    return items


def hero_exits(eyebrow: Any) -> list[dict]:
    """The three exit labels: the eyebrow's words when it has exactly three — else no labels.

    Each label sits above its node, set to end at x 636. A label of more than one word breaks
    before its last word (two lines 14 units apart): on one line «MOBILITÉ RÉGULIÈRE» reached back
    to x 503, into the navy where the four routes braid (round-3 review, defect 8)."""
    parts = [part.strip() for part in str(eyebrow or "").replace("•", "·").split("·") if part.strip()]
    if len(parts) != 3:
        return []
    exits = []
    for n, part in enumerate(parts, start=1):
        words = part.split()
        texts = [" ".join(words[:-1]), words[-1]] if len(words) > 1 else [part]
        base = _EXIT_Y[n] - 10
        lines = [{"text": text, "y": base - 14 * (len(texts) - 1 - k)} for k, text in enumerate(texts)]
        exits.append({"label": part, "y": _EXIT_Y[n], "lines": lines})
    return exits


# ---- 3. Forum banner -------------------------------------------------------------------------
def build_banner(ctx: BuildContext) -> dict | None:
    if not gates.forum_banner_visible():
        return None
    from forum import services as forum_services

    try:
        banner = forum_services.banner_context()
    except NoReverseMatch:  # the forum route is not mounted
        return None
    return {"banner": banner} if banner.get("visible") else None


# ---- 4. Four entrances -----------------------------------------------------------------------
def entrance_url(actor: str, phase3: bool) -> str:
    default = content.ENTRANCES_BY_ACTOR[actor]
    return first_url(default.open_targets if phase3 else default.interim_targets)


def entrances(lang: str, phase3: bool) -> list[dict]:
    """Exactly four entrances, in the prescribed order — prescribed texts only when G3 is open."""
    items = []
    for default in content.ENTRANCES:
        if phase3:
            title = locked(f"p3.entrances.{default.actor}.title", lang)
            text = locked(f"p3.entrances.{default.actor}.text", lang)
            button = locked(f"p3.entrances.{default.actor}.button", lang)
        else:
            title, text, button = ui(default.title), ui(default.text), ui(default.button)
        label = ui(content.ENTRANCE_LABELS[default.actor])
        items.append(
            {
                "actor": default.actor,
                "title": title.value,
                "text": text.value,
                "button": button.value,
                "lang": title.lang,
                "label": label.value,
                # The legend names a row by its label and describes it by its text: each carries
                # its own language (on /ar/ with G3 open the text falls back to French while the
                # label is Arabic — round-4 review, 6b).
                "label_lang": label.lang,
                "text_lang": text.lang,
                "url": entrance_url(default.actor, phase3),
                "icon": default.icon,
                "illustration": static(default.illustration),
            }
        )
    return items


def build_entrances(ctx: BuildContext) -> dict | None:
    return {"entrances": entrances(ctx.lang, ctx.phase3)}


# ---- 5. Orientation --------------------------------------------------------------------------
def build_orientation(ctx: BuildContext) -> dict | None:
    data: dict[str, Any] = {
        "url": safe_reverse("orientation:start"),
        "illustration": static("img/illustrations/orientation.svg"),
    }
    if ctx.phase3:
        data["how_it_works"] = locked("p3.persons.how_it_works", ctx.lang)
    else:
        steps = [ui(step) for step in content.ORIENTATION_STEPS]
        data["steps"] = [s.value for s in steps]
        data["steps_lang"] = steps[0].lang if steps else ""
    return data


# ---- 6. Regular pathways ---------------------------------------------------------------------
def build_pathways(ctx: BuildContext) -> dict | None:
    index_url = safe_reverse("pathways:index")
    if not ctx.phase3:
        families = [ui(label) for label in content.PATHWAY_FAMILIES]
        return {"families": families, "index_url": index_url}
    from pathways import services as pathway_services

    list_lang = locked("p3.persons.pathways", ctx.lang).lang
    items = [
        {"title": entry.title, "text": entry.description, "url": entry.url or index_url, "lang": list_lang}
        for entry in pathway_services.index_entries()
    ]
    if not items:
        return None
    return {"pathway_items": items, "index_url": index_url}


# ---- 7. Pilot project ------------------------------------------------------------------------
def build_pilot(ctx: BuildContext) -> dict | None:
    if not ctx.phase3:
        return None
    title = locked("p3.pilot.title", ctx.lang)
    sequence = locked("p3.pilot.sequence", ctx.lang)
    return {
        "title": title,
        "steps": list(sequence.value),
        "steps_lang": sequence.lang,
        "url": safe_reverse("ecosystem:pilot"),
    }


# ---- 8. Trust / transparency -----------------------------------------------------------------
def faq_entry(key: str, lang: str) -> dict | None:
    """A prescribed FAQ entry (question / answer verbatim) — Phase 3 content."""
    items = locked("p3.faq.items", lang)
    for entry in items.value:
        if entry["key"] == key:
            return {"key": key, "question": entry["question"], "answer": entry["answer"], "lang": items.lang}
    return None


#: The four stretches of the model and who answers for each. This is the data behind the
#: jurisdiction bar (components/jurisdiction.html), the one device all four Design Council judges
#: asked for independently. ``share`` is a RELATIVE weight for the four stretches, not a duration
#: and not a measured quantity — the caption beside the bar says so, because a bar that looks like a
#: timeline while meaning something else is worse than no bar.
#:
#: The owners are deliberately named as functions, never as organisations: "les autorités
#: compétentes", not a ministry. The platform's own stretch is the smallest one, and that is the
#: honest shape of this project.
JURISDICTION_SEGMENTS: tuple[tuple[str, str, int], ...] = (
    ("morocco", _("Pays d’origine : formation et préparation"), 3),
    ("platform", _("Italy Legal Entry™ : information et orientation"), 2),
    ("authority", _("Autorités compétentes : décisions administratives"), 3),
    ("italy", _("Territoire italien : accueil et inclusion"), 2),
)


def jurisdiction_segments() -> list[dict]:
    return [{"owner": owner, "label": label, "share": share} for owner, label, share in JURISDICTION_SEGMENTS]


def build_trust(ctx: BuildContext) -> dict | None:
    if ctx.phase3:
        quotes = [entry for entry in (faq_entry(key, ctx.lang) for key in content.TRUST_FAQ_KEYS) if entry]
        if not quotes:
            return None
        return {"quotes": quotes, "faq_url": safe_reverse("faq:index"), "jurisdiction": jurisdiction_segments()}
    return {
        "does": [locked(key, ctx.lang) for key in content.TRUST_DOES_LOCKED_KEYS],
        "does_not": [ui(statement) for statement in content.TRUST_DOES_NOT],
        "disclaimer_url": safe_reverse("legal:disclaimer"),
        "jurisdiction": jurisdiction_segments(),
    }


# ---- 9. Anti-fraud ---------------------------------------------------------------------------
def build_antifraud(ctx: BuildContext) -> dict | None:
    if not ctx.phase3:
        return None  # no substitute text is invented while the prescribed one is gated
    return {
        "title": locked("p3.antifraud.title", ctx.lang),
        "body": locked("p3.antifraud.body", ctx.lang),
        "url": safe_reverse("pages:antifraud"),
    }


# ---- 10. Latest news -------------------------------------------------------------------------
NEWS_LIMIT = 3


def latest_news(lang: str, limit: int = NEWS_LIMIT) -> list[dict]:
    from news import services as news_services

    cards = []
    for article in news_services.latest_articles(limit):
        texts = article.texts(lang)
        published = article.date_published
        cards.append(
            {
                "title": texts.title,
                "summary": texts.summary,
                "url": article.get_absolute_url(),
                "category": article.category.name(lang),
                "date": formats.date_format(published, "DATE_FORMAT") if published else "",
                "lang": texts.language if texts.is_fallback else "",
            }
        )
    return cards


def build_news(ctx: BuildContext) -> dict | None:
    articles = latest_news(ctx.lang)
    if not articles and not ctx.phase3:
        return None  # before Phase 3 the block appears only once something is published
    return {"articles": articles, "index_url": safe_reverse("news:index")}


# ---- 11. Institutional ecosystem -------------------------------------------------------------
def authorized_partner_cards(lang: str) -> list:
    from partners import services as partner_services

    return [partner_services.card_for(partner, lang) for partner in partner_services.authorized_partners()]


def build_ecosystem(ctx: BuildContext) -> dict | None:
    return {
        "promoter": settings.ILE["PROMOTER"],
        "promoter_quote": faq_entry(content.PROMOTER_FAQ_KEY, ctx.lang) if ctx.phase3 else None,
        "partners": authorized_partner_cards(ctx.lang),
        "agami_url": safe_reverse("pages:agami"),
        "partners_url": safe_reverse("partners:index"),
    }


# ---- 12. Reserved area -----------------------------------------------------------------------
def reserved_area_link_enabled() -> bool:
    if not flags.is_enabled("reserved_area_public_link"):
        return False
    try:
        return bool(SiteSettings.load().reserved_area_enabled)
    except Exception:  # pragma: no cover - before migrations
        return False


def build_reserved(ctx: BuildContext) -> dict | None:
    if not ctx.phase3 or not reserved_area_link_enabled():
        return None
    user = getattr(ctx.request, "user", None)
    authenticated = bool(user is not None and user.is_authenticated)
    url = first_url(["portal:dashboard", "account_login"] if authenticated else ["account_login"])
    if not url:
        return None
    return {
        "title": locked("p3.reserved.title", ctx.lang),
        "body": locked("p3.reserved.body", ctx.lang),
        "button": locked("p3.reserved.button", ctx.lang),
        "url": url,
        "authenticated": authenticated,
    }


BUILDERS: dict[str, Callable[[BuildContext], dict | None]] = {
    SectionKey.HERO: build_hero,
    SectionKey.BANNER: build_banner,
    SectionKey.ENTRANCES: build_entrances,
    SectionKey.ORIENTATION: build_orientation,
    SectionKey.PATHWAYS: build_pathways,
    SectionKey.PILOT: build_pilot,
    SectionKey.TRUST: build_trust,
    SectionKey.ANTIFRAUD: build_antifraud,
    SectionKey.NEWS: build_news,
    SectionKey.ECOSYSTEM: build_ecosystem,
    SectionKey.RESERVED: build_reserved,
}


# --------------------------------------------------------------------------------------------
# Homepage — composition
# --------------------------------------------------------------------------------------------
def default_sections() -> list[HomeSection]:
    """Unsaved rows in the prescribed order — used only when the table has never been seeded."""
    return [
        HomeSection(
            key=d.key,
            order=d.order,
            requires_gate=d.requires_gate,
            heading_fr=str_source(d.heading),
            intro_fr=str_source(d.intro),
            note_fr=str_source(d.note),
        )
        for d in content.SECTION_DEFAULTS
    ]


def section_rows() -> list[HomeSection]:
    if not HomeSection.objects.exists():
        return default_sections()
    return list(HomeSection.objects.visible().prefetch_related("translations"))


def section_gate_open(row: HomeSection, phase3: bool) -> bool:
    if row.key in content.PHASE3_ONLY_SECTIONS and not phase3:
        return False
    return gate_open(row.requires_gate)


def home_sections(request) -> list[SectionView]:
    ctx = BuildContext(request=request, lang=current_language(), phase3=gates.phase3_public())
    views: list[SectionView] = []
    for row in section_rows():
        builder = BUILDERS.get(row.key)
        if builder is None or not section_gate_open(row, ctx.phase3):
            continue
        data = builder(ctx)
        if data is None:
            continue
        heading, intro, note = _section_texts(row, ctx.lang)
        views.append(
            SectionView(
                key=row.key,
                template=f"pages/home/_{row.key}.html",
                anchor=f"home-{row.key}",
                heading=heading,
                intro=intro,
                note=note,
                data=data,
            )
        )
    return views


_JSON_ESCAPES = {ord(">"): "\\u003E", ord("<"): "\\u003C", ord("&"): "\\u0026"}


def render_jsonld(data: dict) -> str:
    """JSON safe inside <script type="application/ld+json"> (no raw <, > or &)."""
    return json.dumps(data, ensure_ascii=False).translate(_JSON_ESCAPES)


def home_jsonld(request, lang: str | None = None) -> dict:
    """
    Organization (the promoter, a private association — never a public authority) + WebSite.
    Deliberately absent: GovernmentOrganization, logo of a public body, sameAs, any authority claim.
    """
    lang = lang or current_language()
    home_url = request.build_absolute_uri(reverse("pages:home"))
    try:
        email = SiteSettings.load().public_contact_email
    except Exception:  # pragma: no cover - before migrations
        email = settings.ILE["PUBLIC_CONTACT_EMAIL"]
    organization_id = f"{home_url}#promoter"
    return {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization",
                "@id": organization_id,
                "name": settings.ILE["PROMOTER"],
                "url": home_url,
                "email": email,
            },
            {
                "@type": "WebSite",
                "@id": f"{home_url}#website",
                "name": locked_content.text("p1.trademark.mark", "fr"),
                "url": home_url,
                "inLanguage": lang,
                "publisher": {"@id": organization_id},
            },
        ],
    }


def home_context(request) -> dict:
    lang = current_language()
    sections = home_sections(request)
    hero = next((s for s in sections if s.key == SectionKey.HERO), None)
    description = str(hero.data["subtitle"] or hero.data["body"] or "") if hero is not None else ""
    description = description or str(ui(content.HERO_INTERIM["subtitle_fr"]))
    return {
        "sections": sections,
        "has_hero": hero is not None,
        "phase3": gates.phase3_public(),
        "meta_description": description,
        # No "image": the homepage keeps the project-wide social card (static img/og-default.png).
        "seo": {"title": settings.ILE["PROJECT_NAME"], "description": description},
        "jsonld": render_jsonld(home_jsonld(request, lang)),
    }


# --------------------------------------------------------------------------------------------
# Institutional pages
# --------------------------------------------------------------------------------------------
INSTITUTIONAL_NAV: tuple[tuple[str, Any, str], ...] = (
    ("pages:project", _("Le projet"), ""),
    ("pages:agami", _("AGAMI, le promoteur"), ""),
    ("pages:network", _("Le réseau"), ""),
    ("pages:contact", _("Contact"), ""),
    ("pages:antifraud", _("Attention aux fraudes"), "phase3_public"),
)


def institutional_nav(current: str) -> list[dict]:
    items = []
    for url_name, label, gate in INSTITUTIONAL_NAV:
        if not gate_open(gate):
            continue
        url = safe_reverse(url_name)
        if url:
            items.append({"label": str(label), "url": url, "current": url_name == current})
    return items


def can_preview(request) -> bool:
    """Back-office users may preview a gated page with ``?preview=1`` (rendered noindex)."""
    user = getattr(request, "user", None)
    return bool(user is not None and user.is_authenticated and user.is_staff and request.GET.get("preview") == "1")


def _page_seo(title: str, description: str, photo: Photo | None = None) -> dict:
    return {"title": title, "description": description, "image": photo.share_path if photo else ""}


def space_links(lang: str, phase3: bool) -> list[dict]:
    """The four spaces of the ecosystem, with the same targets as the homepage entrances."""
    links = []
    for actor in content.NETWORK_ACTORS:
        if not actor.entrance:
            continue
        url = entrance_url(actor.entrance, phase3)
        if url:
            links.append({"label": ui(actor.link_label), "url": url, "icon": actor.icon})
    return links


def project_context(request) -> dict:
    lang, phase3 = current_language(), gates.phase3_public()
    photo = photo_for_slot("workshop", lang)
    lead = ui(content.HERO_INTERIM["subtitle_fr"])
    return {
        "nav": institutional_nav("pages:project"),
        "phase3": phase3,
        "lead": lead,
        "why_title": locked("p2.forum.why.title", lang),
        "why_body": locked("p2.forum.why.body", lang),
        "presentation": locked("p3.hero.body", lang) if phase3 else None,
        "promoter_quote": faq_entry(content.PROMOTER_FAQ_KEY, lang) if phase3 else None,
        "promoter": settings.ILE["PROMOTER"],
        "trademark_mark": locked_content.text("p1.trademark.mark", "fr"),
        "trademark_words": (
            Text(locked_content.text("p1.trademark.words_it", "fr"), "")
            if lang == "it"
            else Text(locked_content.text("p1.trademark.words_fr", "fr"), "" if lang == "fr" else "fr")
        ),
        "spaces": space_links(lang, phase3),
        "links": {
            "agami": safe_reverse("pages:agami"),
            "network": safe_reverse("pages:network"),
            "forum": safe_reverse("forum:index"),
            "orientation": safe_reverse("orientation:start"),
            "contact": safe_reverse("pages:contact"),
        },
        "photo": photo,
        "meta_description": str(lead),
        "seo": _page_seo(settings.ILE["PROJECT_NAME"], str(lead), photo),
    }


def agami_context(request) -> dict:
    lang, phase3 = current_language(), gates.phase3_public()
    photo = photo_for_slot("entrance_institution", lang)
    description = ui(_("AGAMI — Dialogo Giuridico Interculturale APS est le promoteur du projet Italy Legal Entry™."))
    return {
        "nav": institutional_nav("pages:agami"),
        "phase3": phase3,
        "promoter": settings.ILE["PROMOTER"],
        "who_body": locked("p2.forum.who.body", lang),
        "promoter_quote": faq_entry(content.PROMOTER_FAQ_KEY, lang) if phase3 else None,
        "links": {
            "project": safe_reverse("pages:project"),
            "network": safe_reverse("pages:network"),
            "partners": safe_reverse("partners:index"),
            "forum": safe_reverse("forum:index"),
            "notices": safe_reverse("legal:notices"),
            "contact": safe_reverse("pages:contact"),
        },
        "photo": photo,
        "meta_description": str(description),
        "seo": _page_seo(settings.ILE["PROMOTER"], str(description), photo),
    }


def network_context(request) -> dict:
    lang, phase3 = current_language(), gates.phase3_public()
    photo = photo_for_slot("forum_event", lang)
    actors = []
    for actor in content.NETWORK_ACTORS:
        url = entrance_url(actor.entrance, phase3) if actor.entrance else safe_reverse(actor.url_name)
        actors.append(
            {
                "key": actor.key,
                "icon": actor.icon,
                "title": ui(actor.title),
                "text": ui(actor.text),
                "link_label": ui(actor.link_label),
                "url": url,
            }
        )
    description = ui(
        _(
            "Les acteurs de l’écosystème Italy Legal Entry™ : personnes, entreprises, institutions, "
            "universités et organismes de formation, professionnels."
        )
    )
    return {
        "nav": institutional_nav("pages:network"),
        "phase3": phase3,
        "presentation": locked("p3.hero.body", lang) if phase3 else None,
        "actors": actors,
        "partners": authorized_partner_cards(lang),
        "links": {
            "partners": safe_reverse("partners:index"),
            "forum": safe_reverse("forum:index"),
            "agami": safe_reverse("pages:agami"),
        },
        "photo": photo,
        "meta_description": str(description),
        "seo": _page_seo(str(ui(_("Le réseau"))), str(description), photo),
    }


def contact_context(request) -> dict:
    phase3 = gates.phase3_public()
    forms_gate = gates.public_forms_enabled()
    # The address itself is printed by the template through site.contact_email only.
    description = ui(
        _("Contacter Italy Legal Entry™ : une adresse unique pour toutes les demandes relatives au projet.")
    )
    dedicated = [
        {"label": ui(_("Entreprises : signaler vos besoins professionnels")), "url_name": "enquiries:company_needs"},
        {
            "label": ui(_("Institutions : proposer une collaboration")),
            "url_name": "enquiries:institution_proposal",
        },
        {
            "label": ui(_("Universités et organismes de formation : proposer un partenariat")),
            "url_name": "enquiries:university_proposal",
        },
    ]
    return {
        "nav": institutional_nav("pages:contact"),
        "phase3": phase3,
        "forms_open": forms_gate.open,
        "contact_form_url": safe_reverse("enquiries:contact"),
        "dedicated_forms": [
            {"label": item["label"], "url": safe_reverse(item["url_name"])}
            for item in dedicated
            if safe_reverse(item["url_name"])
        ],
        "links": {"privacy": safe_reverse("legal:privacy"), "forum": safe_reverse("forum:index")},
        "meta_description": str(description),
        "seo": _page_seo(str(ui(_("Contact"))), str(description)),
    }


def antifraud_context(request, is_preview: bool = False) -> dict:
    lang = current_language()
    title = locked("p3.antifraud.title", lang)
    body = locked("p3.antifraud.body", lang)
    faq_url = safe_reverse("faq:index")
    return {
        "nav": institutional_nav("pages:antifraud"),
        "title": title,
        "body": body,
        "is_preview": is_preview,
        "noindex": is_preview,
        # The FAQ link is labelled with the prescribed question itself (never a paraphrase of it).
        "faq_question": faq_entry(content.ANTIFRAUD_FAQ_KEY, lang),
        "links": {
            "faq": f"{faq_url}#{content.ANTIFRAUD_FAQ_KEY}" if faq_url else "",
            "pathways": safe_reverse("pathways:index"),
            "glossary": safe_reverse("glossary:index"),
            "orientation": safe_reverse("orientation:start"),
        },
        # The prescribed body is used whole (never shortened) as the page description.
        "meta_description": str(body.value),
        "seo": _page_seo(str(title.value), str(body.value)),
    }
