"""
Built-in template tags (loaded automatically via TEMPLATES['OPTIONS']['builtins']).

{% locked "key" %}                → renders the locked text (escaped) with lang attr on fallback
{% locked "key" as var %}         → assigns (str or list/dict) to a context variable
{% locked_lang "key" %}           → effective language code of the locked text
{% flag "key" as var %}           → boolean feature flag
{% svg_icon "name" %}             → inline SVG icon from static/icons/sprite (via <use>)
{% active "url_name" %}           → "is-active" when the current URL name matches
{{ value|rtl_arrow }}             → mirrors →/← for RTL languages
"""

from __future__ import annotations

from django import template
from django.conf import settings
from django.utils import translation
from django.utils.html import escape, format_html
from django.utils.safestring import mark_safe

from cms import locked_content
from core import flags

register = template.Library()


@register.simple_tag(takes_context=True)
def locked(context, key: str, tag: str = "", css_class: str = ""):
    lang = translation.get_language() or settings.LANGUAGE_CODE
    value, effective = locked_content.get(key, lang)
    if not isinstance(value, str):
        return value
    needs_lang = effective != lang.split("-")[0]
    rendered = escape(value)
    if tag:
        attrs = f' class="{escape(css_class)}"' if css_class else ""
        if needs_lang:
            attrs += f' lang="{effective}"'
        return format_html("<{}{}>{}</{}>", tag, mark_safe(attrs), mark_safe(rendered), tag)  # noqa: S308
    if needs_lang:
        return format_html('<span lang="{}">{}</span>', effective, mark_safe(rendered))  # noqa: S308
    return mark_safe(rendered)  # noqa: S308


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


@register.simple_tag
def svg_icon(name: str, css_class: str = "icon", label: str = ""):
    aria = format_html(' role="img" aria-label="{}"', label) if label else mark_safe(' aria-hidden="true"')  # noqa: S308
    return format_html(
        '<svg class="{}"{} focusable="false"><use href="{}#icon-{}"></use></svg>',
        css_class,
        aria,
        settings.STATIC_URL + "img/icons.svg",
        name,
    )


@register.filter
def actor_glyph(actor: str) -> str:
    """The glyph of a responsible actor (documents.requirements.ACTOR_GLYPHS), '' when unknown:
    the Glyph component then draws its dashed disc."""
    from documents.requirements import ACTOR_GLYPHS

    return ACTOR_GLYPHS.get(str(actor or ""), "")


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
# The register of a chip is decided in apps/core/chips.py from the enum MEMBER, per producer,
# because the same word means different things to different producers (spec badges.md §4.3).
# A template names the producer: `{{ case.status|chip_register:"cases.CaseStatus" }}`. An
# unknown value yields "" and the template must then omit the attribute, which the stylesheet
# paints dotted — «unmapped», visible, tested.


@register.filter
def chip_register(value, producer: str) -> str:
    from core import chips

    return chips.register_for(producer, value)


@register.filter
def chip_stage(value) -> int | str:
    """
    The gauge phase, or "" — never None, which a template would print as the word «None».

    chip.css only reads the values 1, 2 and 3; an empty attribute matches none of them and the
    chip keeps its full rule, which is what a status without a phase must show.
    """
    from core import chips

    stage = chips.stage_for(value)
    return stage if stage is not None else ""


@register.filter
def badge_register(kind) -> str:
    """The legacy `kind` of components/badge.html, translated to a register once for all includes."""
    from core import chips

    return chips.register_for_kind(kind)
