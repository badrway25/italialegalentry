"""
The atrium's eyebrow (V5.15 lane D, round 2; templates/portal/partials/atrium_eyebrow.html): the SPACE'S NAME, the same
word on every console page of the account as on its dashboard — «Espace Personnes», «Espace Institutions», «Espace
Universités et Formation», «Entreprise» … Round 2's major: the eyebrow read ``portal_nav.0.space``, which most pages do
not provide, and 12 of 19 atrium pages showed the fallback «Espace réservé» (repeating the breadcrumb's root and the
rail's brand line). The word is now resolved from the ACCOUNT, as the dashboards resolve it
(portal.services.atrium_space_label).

V5.32 lane E: the console's head draws no figure any more (portal/partials/atrium_art.html renders nothing), so the
drawing's two helpers — `journey_rank` (the route's lit station) and `atrium_glyph` (the seal's glyph in the arcade) —
left with it; the space's name is this library's one tag.
"""

from __future__ import annotations

from django import template

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
