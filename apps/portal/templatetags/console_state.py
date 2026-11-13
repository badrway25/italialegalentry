"""
A STATE the console answers in its own frame (V5.32 lane E, correction round P2-8; templates/errors/console_error.html):
a refusal (the 403) or a module that is not open (the Forum permanent's 503), reached at an address of the console by
a signed-in account whose console is open. The frame reads its rail, its trail and its one primary here because the
page that asks for them may be drawn by a handler that gives it nothing but the request (core.views.error_403): the
producers are portal.services.console_state_shell and console_state_dashboard.
"""

from __future__ import annotations

from django import template

from portal import services

register = template.Library()


@register.simple_tag(takes_context=True)
def console_state(context, crumb: str = "") -> dict:
    """The state page's `portal_nav` and `breadcrumbs` — the trail ending on `crumb`, the state's name."""
    return services.console_state_shell(context["request"], str(crumb or ""))


@register.simple_tag(takes_context=True)
def console_state_dashboard(context) -> str:
    """The «Tableau de bord» of the rail the state's page keeps: its one primary."""
    return services.console_state_dashboard(context["request"])
