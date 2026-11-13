"""
Built-in template tags (loaded automatically via TEMPLATES['OPTIONS']['builtins']).

{% locked "key" %}                → renders the locked text (escaped) with lang attr on fallback — V5.27: on /ar/ the
                                    provisional Arabic rendering of a compositional text, the pointer line of a
                                    substantive
                                    block quoted off its page; the block form adds the identification caption before a
                                    French substantive block on its own page (cms.locked_renderings)
{% locked "key" as var %}         → assigns (str or list/dict) to a context variable
{% locked "p3.faq.items[0].question" %} → one text of a compound key, by its sub-key
{% locked_caption "key" %}        → the identification caption alone, "" when the block needs none here
{% locked_treatment "key" %}      → C-UI / C-SUBST-FR / C-SUBST-IT / C-OFFICIAL
{% locked_is_hidden "key" %}      → True when the block is in its hidden form on this page
{% locked_lang "key" %}           → effective language code of the locked text
{% flag "key" as var %}           → boolean feature flag
{% svg_icon "name" %}             → one symbol of the ILE sprite, through the registry apps/core/icons.py (a <use>
                                    of static/img/icons.svg or icons-domain.svg — icons.SPRITE_OF — served with its
                                    content hash; the closed flip list)
{{ key|concept:"domain" }}        → the registry's symbol for a concept key (card, actor, nav, pathway, living, due…)
{% chapter_mark title_id "cls" %} → the concept glyph of a section (icons.CHAPTER) inside its caller's container, or
                                    nothing; without a class — the bare mark above a title — nothing (V5.22 §0.3)
{{ key|mark_of }}                 → V5.22: an ILE mark's id from its id or its concept (icons.MARKS), "" when none
{{ glyph|folio_mark }}            → V5.22: the T1 mark a head folio draws for its concept glyph (icons.FOLIO), or ""
{{ actor|actor_glyph }}           → the glyph of a responsible actor, "" when unknown
{% chip value "app.Enum" %}…{% endchip %} → THE status chip: its register and its mark from apps/core/chips.py
{% chip register="neutro" %}…{% endchip %} → the same, for a state the template knows by its register
{{ value|chip_mark:"app.Enum" }}  → the sprite symbol of a status mark, for a strip or a filter that draws it bare
{% active "url_name" %}           → "is-active" when the current URL name matches
{{ value|rtl_arrow }}             → mirrors →/← for RTL languages
{% extends request|account_frame %} → an account page's layout: the console for a signed-in account (accounts.shell)
{% account_console as shell %}    → the rail and the trail of an account page in the console
"""

from __future__ import annotations

import functools
import hashlib
import logging
import re
from pathlib import Path

from django import template
from django.conf import settings
from django.contrib.staticfiles import finders
from django.templatetags.static import static
from django.utils import translation
from django.utils.html import escape, format_html
from django.utils.safestring import mark_safe

from cms import locked_content
from core import flags, icons

logger = logging.getLogger(__name__)

register = template.Library()


#: the brand's run inside an Arabic rendering: one left-to-right unit, never broken (AR's M1; T's ``bdi[dir="ltr"]``
#: rule)
_BRAND_RUN = re.compile("Italy Legal Entry™?‎?")


def _isolate_brand(escaped: str) -> str:
    return _BRAND_RUN.sub(lambda m: f'<bdi dir="ltr">{m.group(0)}</bdi>', escaped)


def _caption(key: str, lang: str, effective: str) -> str:
    """V5.27 / R7′ (c): the identification caption of a block shown in its source language on a page of another language
    —
    the French of a substantive text on its own page, the Italian of a legal text — in the label role (``t-label``, no
    CSS of
    its own), before the block. "" for a rendering, a proper name or a French page."""
    from cms import locked_renderings

    if effective == lang.split("-")[0]:
        return ""
    text = locked_renderings.caption_text(key, lang)
    if not text:
        return ""
    return format_html('<p class="t-label locked-caption" data-locked-caption="{}">{}</p>', key, text)


@register.simple_tag(takes_context=True)
def locked(context, key: str, tag: str = "", css_class: str = ""):
    """
    The prescribed text of ``key`` in the page's language (``cms.locked_content.get``: the official version, the Arabic
    product's provisional rendering or the pointer line of a block hidden off its page — V5.27, R7′ —, else the French
    source) — escaped, and wrapped in its ``lang`` when the words are not the page's. In the block form (``tag`` given)
    a French substantive block on its own page, and an Italian authoritative text, are preceded by their identification
    caption; the inline form carries none (a run inside a sentence). The brand's run inside an Arabic rendering is one
    left-to-right unit (``bdi``).
    """
    lang = translation.get_language() or settings.LANGUAGE_CODE
    value, effective = locked_content.get(key, lang)
    if not isinstance(value, str):
        return value
    needs_lang = effective != lang.split("-")[0]
    rendered = escape(value)
    if effective == "ar":
        rendered = _isolate_brand(rendered)
    if tag:
        attrs = f' class="{escape(css_class)}"' if css_class else ""
        if needs_lang:
            attrs += f' lang="{effective}"'
        block = format_html("<{}{}>{}</{}>", tag, mark_safe(attrs), mark_safe(rendered), tag)  # noqa: S308
        caption = _caption(key, lang, effective)
        return mark_safe(f"{caption}{block}") if caption else block  # noqa: S308
    if needs_lang:
        return format_html('<span lang="{}">{}</span>', effective, mark_safe(rendered))  # noqa: S308
    return mark_safe(rendered)  # noqa: S308


@register.simple_tag
def locked_caption(key: str):
    """The identification caption alone (``{% locked_caption "p3.faq.items[0].answer" %}``) — for a template that
    composes
    a substantive block itself and must say, before it, that the words are the French source pending validation (or the
    Italian authoritative text); "" when the block needs none on this page."""
    lang = translation.get_language() or settings.LANGUAGE_CODE
    _value, effective = locked_content.get(key, lang)
    return _caption(key, lang, effective)


@register.simple_tag
def locked_treatment(key: str) -> str:
    """The class of a prescribed text under the Arabic policy — ``C-UI``, ``C-SUBST-FR``, ``C-SUBST-IT``, ``C-OFFICIAL``
    (cms.locked_renderings) — for a template that composes a compound key part by part."""
    from cms import locked_renderings

    return locked_renderings.treatment(key) or ""


@register.simple_tag
def locked_is_hidden(key: str) -> bool:
    """Whether the block is in its hidden form on this page (a substantive French text quoted off its own page, on
    ``/ar/``): the template then draws the pointer line ``{% locked key %}`` gives it and nothing else."""
    from cms import locked_renderings

    lang = translation.get_language() or settings.LANGUAGE_CODE
    return locked_renderings.is_hidden(key, lang)


@register.simple_tag
def locked_lang(key: str) -> str:
    lang = translation.get_language() or settings.LANGUAGE_CODE
    _value, effective = locked_content.get(key, lang)
    return effective


@register.simple_tag
def locked_is_fallback(key: str) -> bool:
    lang = translation.get_language() or settings.LANGUAGE_CODE
    _value, effective = locked_content.get(key, lang)
    return effective != lang.split("-")[0]


@register.simple_tag
def flag(key: str) -> bool:
    return flags.is_enabled(key)


@functools.lru_cache(maxsize=4)
def _sprite_url(sprite: str = icons.SPRITE) -> str:
    """
    A sprite's URL with a content hash — ``?v=<sha256[:12]>`` of the file — so a new sprite is never drawn
    from a cached one; unless the static storage already hashes the name (the manifest storage of production
    and of the compressed twin), in which case that URL is the hash. Two sprites since V5.12 W2 (DECISIONS §4):
    ``icons.SPRITE_OF`` says which file holds a symbol, so each ``<use>`` points at its own.
    """
    url = static(sprite)
    if re.search(r"\.[0-9a-f]{8,}\.svg$", url):
        return url
    path = finders.find(sprite)
    if not path:
        return url
    digest = hashlib.sha256(Path(path).read_bytes()).hexdigest()[:12]
    return f"{url}?v={digest}"


@register.simple_tag
def svg_icon(name: str, css_class: str = "icon", label: str = ""):
    """
    One symbol of the ILE sprite, through the registry (apps/core/icons.py, plan §1.7): a V4 alias resolves to
    its V5 symbol, so the page's markup carries the V5 id; a symbol of the closed flip list (``FLIP_RTL``)
    carries ``icon--flip-rtl`` and no other symbol does, whatever the call site wrote; an empty name draws
    nothing (a row carries a glyph only when it says something); an unknown name draws nothing and is logged —
    the tests keep every literal honest (tests/frontend/test_icons.py).
    """
    try:
        symbol = icons.resolve(name)
    except icons.UnknownIcon:
        if name:
            logger.warning("svg_icon: no icon called %r", name)
        return ""
    classes = [c for c in str(css_class or "").split() if c != "icon--flip-rtl"]
    if symbol in icons.FLIP_RTL:
        classes.append("icon--flip-rtl")
    aria = format_html(' role="img" aria-label="{}"', label) if label else mark_safe(' aria-hidden="true"')  # noqa: S308
    return format_html(
        '<svg class="{}"{} focusable="false"><use href="{}#icon-{}"></use></svg>',
        " ".join(classes),
        aria,
        _sprite_url(icons.SPRITE_OF[symbol]),
        symbol,
    )


@register.filter
def concept(key, domain: str) -> str:
    """
    The registry's symbol for ``key`` in a concept domain — ``{{ card.key|concept:"card" }}``,
    ``{{ deadline.urgency|concept:"due" }}`` — and "" when the domain has no such key: a concept glyph reaches a
    template through the registry, never as a literal (plan §1.7).
    """
    try:
        return icons.concept(domain, key)
    except icons.UnknownIcon:
        return ""


@register.simple_tag
def chapter_mark(key: str = "", css_class: str = ""):
    """
    The glyph of a section's concept (V5.12 §7), through the registry's CHAPTER map — ``{% chapter_mark title_id "icon
    chapter__mark" %}`` with the section's anchor or a concept — drawn inside its caller's own container (the premium
    forms' glyph tiles, V5.15 W3: preserved), and nothing when the section says no concept.

    V5.22 (SECTION_SYSTEM_V2 §0 item 3, §4.1 rule 1, §4.10; lane S): the BARE mark — the tag without a class, a 24 px
    glyph stacked above a title — is retired everywhere: it draws nothing. A theme is a T1 seal integrated in its
    section's composition (components/sezioni/sigillo.html), or it is not drawn. CHAPTER / CHAPTER_OF stay the concept
    registry.
    """
    if not css_class:
        return ""
    symbol = icons.chapter_glyph(key)
    return svg_icon(symbol, css_class) if symbol else ""


@register.filter
def mark_of(key) -> str:
    """
    V5.22 (SECTION_SYSTEM_V2 §4.9–§4.10): the id of an ILE mark — ``{{ "orientation"|mark_of }}`` with a concept of
    ``icons.MARKS``, or ``{{ "ile-scudo"|mark_of }}`` with the id itself — and "" for anything else, so a seat is drawn
    for a registered mark or not at all (components/sezioni/sigillo.html).
    """
    key = str(key or "")
    if key in icons.MARK:
        return key
    mark = icons.MARKS.get(key)
    return mark.id if mark else ""


@register.filter
def folio_mark(glyph) -> str:
    """
    V5.22 (§0.1 «Folio seals in the heads»): the T1 mark the head folio's small seat draws for the concept glyph a page
    passes its frontispiece (``icons.FOLIO``), or "" — then the folio is typographic: a Lucide disc in the folio's
    seat would be the old device.
    """
    return icons.FOLIO.get(str(glyph or ""), "")


@register.simple_tag
def icon_registry():
    """The icon registry itself (apps/core/icons.py) — its groups, floors and lists — for the dev specimen board
    (templates/dev/designpreview/specimens/icons.html), which draws the sheet from it rather than from literals."""
    return icons


@register.filter
def actor_glyph(actor: str) -> str:
    """The glyph of a responsible actor (the registry's ACTOR map), '' when unknown: the Glyph component then
    draws its dashed disc."""
    try:
        return icons.concept("actor", actor)
    except icons.UnknownIcon:
        return ""


@register.simple_tag(takes_context=True)
def active(context, *url_names: str, css_class: str = "is-active") -> str:
    request = context.get("request")
    match = getattr(request, "resolver_match", None) if request else None
    if not match:
        return ""
    current = match.view_name or ""
    for name in url_names:
        if current == name or (name.endswith(":") and current.startswith(name)):
            return css_class
    return ""


@register.filter
def rtl_arrow(value: str) -> str:
    lang = translation.get_language() or settings.LANGUAGE_CODE
    if lang in settings.RTL_LANGUAGES:
        return value.replace("→", "←").replace("←", "→")
    return value


@register.filter
def get_item(mapping, key):
    try:
        return mapping.get(key)
    except AttributeError:
        return None


@register.simple_tag
def project_email() -> str:
    return settings.ILE["PUBLIC_CONTACT_EMAIL"]


@register.simple_tag
def safe_url(name: str, *args, **kwargs) -> str:
    """
    Reverse a URL name for a cross-app link. Returns "" when the name does not resolve OR when the
    target page is registered behind a gate that is currently closed — a menu, a CTA or a breadcrumb
    must never point at a page that answers 404 (core.links.public_url).
    """
    from core.links import public_url

    return public_url(name, *args, **kwargs)


@register.simple_tag
def voyage_route(count: int, width: int = 1200, height: int = 140) -> dict:
    """
    The route of a sequence, drawn between two shores — the path and the station coordinates.

    Computed here rather than written by hand because the station dots must sit ON the line, and
    the number of stations comes from the locked content: the pilot sequence is eight steps today
    and a different length the day the client's text changes. A hand-drawn curve with hand-placed
    dots drifts the moment that happens, and a drifted dot on a diagram about a legal pathway is
    not a small thing.

    The line rises from the south shore to the north one — the geography of the project, not a
    growth chart: the vertical axis is a shore, never a quantity. Stations are evenly spaced along
    the width; the curve is a cosine ease so the rise is steepest in the middle, where the crossing
    happens. Returns {"d": …, "stations": [{"x": "…", "y": "…", "index": …}], "width": …, "height": …};
    the coordinates are strings — see the note where they are built.
    """
    import math

    n = max(2, int(count or 0))
    pad = width / (n * 2)
    span = width - pad * 2
    top, bottom = height * 0.18, height * 0.82
    stations = []
    for i in range(n):
        t = i / (n - 1)
        x = pad + span * t
        # cosine ease-in-out: flat at both shores, steep at the crossing
        y = bottom - (bottom - top) * (0.5 - 0.5 * math.cos(math.pi * t))
        # STRINGS, not floats. Django localises numbers in templates, and on a French page
        # `{{ st.x }}` renders «75,0» — which an SVG length attribute rejects outright
        # («Expected length»), silently losing every station dot. Formatting here keeps the
        # drawing independent of the reader's locale.
        stations.append({"x": f"{x:.1f}", "y": f"{y:.1f}", "index": i + 1})

    # A smooth curve through the stations: horizontal control points, so the line leaves and meets
    # every dot level — the dots are stations on a route, not corners of a chart.
    d = f"M{stations[0]['x']} {stations[0]['y']}"
    for a, b in zip(stations, stations[1:], strict=False):
        cx = (float(a["x"]) + float(b["x"])) / 2
        d += f"C{cx:.1f} {a['y']} {cx:.1f} {b['y']} {b['x']} {b['y']}"
    return {"d": d, "stations": stations, "width": width, "height": height}


# --------------------------------------------------------------------------- status chips
# Design V5 «i cerchi» (V5.4 plan §1.2; static/css/v5/chip.css). The register of a chip is decided in
# apps/core/chips.py from the enum MEMBER, per producer, because the same word means different things to
# different producers (docs/design-v3/specs/badges.md §4.3) — and its mark, the sign that says the state
# without colour, comes from the icon registry through that module. A chip therefore has ONE producer: the
# {% chip %} pair below, which renders templates/components/chip.html. A template never writes the element by
# hand, never chooses a mark, and never includes the partial itself
# (tests/frontend/test_state_chips_carry_a_register.py).

_CHIP_SIZES = ("s", "l")


@register.simple_block_tag
def chip(content, value="", producer="", register="", size="", css_class="", role="", lang="", title=""):
    """
    The status chip: a mark, a word, an edge.

        {% chip row.state "documents.RequirementState" %}{{ row.state_label }}{% endchip %}
        {% chip register="neutro" %}{% translate "Nouveau" %}{% endchip %}

    ``value`` + ``producer``: the member and the name of its enum in ``chips.REGISTER`` — the register is the
    member's, and so is the mark. ``register``: one of the eight words, for a state the template itself knows
    (a row that is unread, a count of late items). A value the module does not know is drawn without a
    register — neutral, dotted, visible — and logged; a word that is not a register is refused the same way.
    The block is the chip's word: with no word there is no chip.

    ``size``: "s" (20 px) or "l" (28 px); 24 px otherwise. ``css_class``: the classes that PLACE the chip in its
    page (``entry__actor``), never one that paints it. ``role``, ``lang``, ``title``: written on the element as
    they are. A case status carries its phase as three notches after the word (``chips.STAGE``).
    """
    from django.template.loader import render_to_string

    from core import chips

    label = str(content).strip()
    if not label:
        return ""
    if producer:
        found = chips.register_for(producer, value)
        if not found:
            logger.warning("chip: no register for %r in %r", getattr(value, "value", value), producer)
    else:
        found = str(register or "")
        if found not in chips.REGISTERS:
            logger.warning("chip: %r is not a register", found)
            found = ""
    stage = chips.stage_for(value) if producer == chips.STAGE_PRODUCER else None
    html = render_to_string(
        "components/chip.html",
        {
            # the block is already rendered, and escaped where it had to be: it is not escaped twice
            "label": mark_safe(label),  # noqa: S308
            "register": found,
            "mark": chips.mark_for(found, producer, value),
            "size": size if size in _CHIP_SIZES else "",
            "notches": [notch <= stage for notch in (1, 2, 3)] if stage else None,
            "css_class": css_class,
            "role": role,
            "lang": lang,
            "title": title,
        },
    )
    return mark_safe(html.strip())  # noqa: S308


@register.filter
def chip_register(value, producer: str) -> str:
    """The register of a member, for an element that is not a chip and still speaks the registers: a segment of
    the health strip, a legend. "" when unknown — the template then omits the attribute."""
    from core import chips

    return chips.register_for(producer, value)


@register.filter
def chip_mark(value, producer: str = "") -> str:
    """
    The sprite symbol of a status mark, for the places that draw it bare — a filter's entry, a legend, a strip:
    ``{% svg_icon f.value|chip_mark:"documents.RequirementState" "icon chip__g" %}`` on an element that carries
    the member's ``data-register`` (the mark takes its colour from it). Without a producer the value is a register.
    """
    from core import chips

    if producer:
        return chips.mark_for(chips.register_for(producer, value), producer, value)
    return chips.mark_for(str(value or ""))


@register.filter
def badge_register(kind) -> str:
    """The legacy `kind` of components/badge.html, translated to a register once for all includes."""
    from core import chips

    return chips.register_for_kind(kind)


@register.filter
def account_frame(request) -> str:
    """The layout of an account page (V5.12 W2): the console's for a signed-in account whose reserved area is open,
    the public one otherwise — ``{% extends request|account_frame %}`` in allauth/layouts/manage.html (accounts.shell).
    A builtin filter, because ``{% extends %}`` must be a template's first tag and no ``{% load %}`` may precede it."""
    from accounts import shell

    return shell.frame(request)


@register.simple_tag(takes_context=True)
def account_console(context) -> dict:
    """The rail and the trail of an account page in the console (accounts.shell.console_context)."""
    from accounts import shell

    return shell.console_context(context["request"])
