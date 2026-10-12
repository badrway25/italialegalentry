"""
``{% load entrance %}`` — the entrance release's consumer (design V5, V5.4 plan §1.9; DL54-07; W1-D).

    {% entrance_release as lume_release %}

True on the first console page after a successful sign-in, False on every other page: the flag that
``accounts.signals.mark_entrance_release`` left in the session on ``user_logged_in`` is removed as it is
read, so the lit doorway (templates/components/loader.html with ``release=True``) plays once per session
and never twice — not on a reload, not on a page restored from history. The one consumer is
templates/partials/portal_chrome.html, the console's chrome; a template without a request (a specimen
board, an e-mail) reads False.
"""

from __future__ import annotations

from django import template

from accounts.signals import consume_entrance_release

register = template.Library()


@register.simple_tag(takes_context=True)
def entrance_release(context) -> bool:
    request = context.get("request")
    return consume_entrance_release(request) if request is not None else False
