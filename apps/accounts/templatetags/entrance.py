"""
``{% load entrance %}`` — the entrance release's consumer (design V5, V5.4 plan §1.9; DL54-07; W1-D).

    {% entrance_release space.key as lume_release %}

True on the first console page after a successful sign-in, False on every other page: the flag that
``accounts.signals.mark_entrance_release`` left in the session on ``user_logged_in`` is removed as it is
read, so the lit doorway (templates/components/loader.html with ``release=True``) plays once per session
and never twice — not on a reload, not on a page restored from history. The one consumer is
templates/partials/portal_chrome.html, the console's chrome; a template without a request (a specimen
board, an e-mail) reads False. With the page's space key the release also plays once on the first page of each
further space of the session (V5.12 §4; the Director's DECISIONS §1 T3; ``accounts.signals.consume_space_release``).
"""

from __future__ import annotations

from django import template

from accounts.signals import consume_space_release

register = template.Library()


@register.simple_tag(takes_context=True)
def entrance_release(context, space: str = "") -> bool:
    request = context.get("request")
    return consume_space_release(request, space or "") if request is not None else False
