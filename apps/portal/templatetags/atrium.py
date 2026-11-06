"""
The atrium's eyebrow (V5.15 lane D, round 2; templates/portal/partials/atrium_eyebrow.html): the SPACE'S NAME, the same
word on every console page of the account as on its dashboard — «Espace Personnes», «Espace Institutions», «Espace
Universités et Formation», «Entreprise» … Round 2's major: the eyebrow read ``portal_nav.0.space``, which most pages do
not provide, and 12 of 19 atrium pages showed the fallback «Espace réservé» (repeating the breadcrumb's root and the
rail's brand line). The word is now resolved from the ACCOUNT, as the dashboards resolve it
(portal.services.atrium_space_label).
"""

from __future__ import annotations

from django import template
from django.utils import translation
from django.utils.html import format_html

from core import icons
from core.templatetags.ile_core import _sprite_url
from portal import services

register = template.Library()


@register.simple_tag(takes_context=True)
def atrium_space(context) -> str:
    """The viewing account's space name, translated; «» without an account (the partial then says «Espace réservé»)."""
    request = context.get("request")
    user = getattr(request, "user", None)
    if user is None or not getattr(user, "is_authenticated", False):
        return ""
    return services.atrium_space_label(user)


@register.filter
def journey_rank(journey) -> int:
    """The rank of the step the file stands on (1…n), for the route figure's lit station; 0 when nothing is current (a
    held file, no journey): the drawing then lights no station — a place the system does not know is never shown."""
    at = services.journey_at(list(journey or []))
    return at["n"] if at else 0


@register.simple_tag
def atrium_glyph(name: str, x: int, y: int, size: int = 20):
    """
    The seal's glyph inside the drawing (an organisation's space): the registry's symbol as an SVG ``<use>`` placed
    in the drawing's own units — a nested ``<svg>`` takes no CSS size in Chromium and was drawn at the drawing's
    full size. Decorative (the drawing is ``aria-hidden``); an unknown name draws nothing.
    """
    try:
        symbol = icons.resolve(name)
    except icons.UnknownIcon:
        return ""
    use = format_html(
        '<use class="atrium__glyph-icon" href="{}#icon-{}" x="{}" y="{}" width="{}" height="{}"></use>',
        _sprite_url(icons.SPRITE_OF[symbol]),
        symbol,
        x,
        y,
        size,
        size,
    )
    if not translation.get_language_bidi():
        return use
    # V5.15 W3 lane D, finishing round F1 (the F2 review's major): in Arabic the drawing is mirrored as a whole
    # (.atrium__art, scaleX(-1)) and a glyph is not, so the glyph is mirrored back about its OWN centre. A CSS
    # `transform-box: fill-box` on the <use> is not that centre in Chromium (it resolves the box without the use's
    # x/y, about 7.9 px 5.6 px), which threw the glyph ~150 drawing units out of its seal; the mirror is now an SVG
    # attribute in the drawing's own units, x' = 2·cx − x, on a wrapper — no CSS box involved.
    return format_html(
        '<g class="atrium__glyph-flip" transform="matrix(-1 0 0 1 {} 0)">{}</g>', 2 * x + size, use
    )
