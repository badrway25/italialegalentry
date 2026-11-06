"""
The account pages' atrium in the console (V5.18 P-2, lane B): which space tints the head of «Mon compte».

The console's page head is lane D's atrium (portal/partials/atrium_art.html, portal/v5/_platform.css): its wash is the
account's space — ``data-atrium="person|company|institution|university"``, the same key the space's own dashboard
uses. This tag answers that key for the signed-in account, from the portal's own audience rules (never a second copy).
"""

from __future__ import annotations

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def account_atrium(context) -> str:
    """«institution», «university», «company» or «person» — the space whose wash the account's atrium takes."""
    from portal import services

    request = context.get("request")
    user = getattr(request, "user", None)
    if user is None or not getattr(user, "is_authenticated", False):
        return "person"
    audience = services.organisation_audience(user)
    if audience:
        return audience
    return "company" if services.is_company_audience(user) else "person"
