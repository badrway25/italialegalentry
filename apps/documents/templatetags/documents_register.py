"""
The register, renderable from a page this app does not own.

``portal.views.documents`` builds its own context and cannot be edited from here, so the reserved
area's "Mes documents" entry renders the real register through this tag instead of a second,
divergent copy of the same rules. One presenter, one set of authorisation calls, two pages.
"""

from __future__ import annotations

from django import template

from documents import presenters, services

register = template.Library()


EMPTY = {"blocks": [], "row_count": 0, "open_count": 0, "empty_text": "", "state_filter": "", "primary_action": None}


def state_filter_of(request) -> str:
    """The state filter lives in the URL (design V4 §3.5.3): shareable, back-button-safe, no script."""
    query = getattr(request, "GET", None)
    if query is None:
        return ""
    return query.get("état") or query.get("etat") or ""


@register.simple_tag(takes_context=True)
def register_data(context) -> dict:
    """The register's context, for a page that draws its own header from it before including
    documents/partials/register.html (the portal's «Mes pièces»)."""
    request = context.get("request")
    user = getattr(request, "user", None)
    if user is None or not getattr(user, "is_authenticated", False):
        return dict(EMPTY)
    return presenters.register_context(user, state_filter=state_filter_of(request))


@register.simple_tag
def deposit_rules() -> dict:
    """The Dépôt's client guards read the server's own limits (design V5, W3-C): templates/documents/partials/depot.html
    writes them on its form, where static/js/src/depot.js reads them — never a second copy of the rule in a script."""
    return presenters.deposit_rules()


@register.inclusion_tag("documents/partials/register.html", takes_context=True)
def document_register(context):
    request = context.get("request")
    user = getattr(request, "user", None)
    if user is None or not getattr(user, "is_authenticated", False):
        return {"register": dict(EMPTY), "request": request}
    return {
        "register": presenters.register_context(user, state_filter=state_filter_of(request)),
        "may_upload": services.user_may_upload(user),
        "request": request,
    }
