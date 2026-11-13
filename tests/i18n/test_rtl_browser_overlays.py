"""
RTL check of the overlay system (design V5, family W2-A; V5.4 plan §1.14 O5, §2.5; the contract
docs/design-v5/QA/v54/w2-a/CONTRACT.md). What the static guard cannot see (plan §2.5: a travel written as
`calc(100% * … * var(--dir))`, a place computed by script or by the anchor's own direction):

* the drawers mirror — the navigation comes from the reading edge, the right in Arabic, and a detail from the left —
  and each arrives from its own edge;
* the sheet does not mirror: it rises from the bottom, its inline position unmoved;
* a menu aligns on its trigger's inline end: in Arabic its left edge on the trigger's left edge;
* the top-layer tip of a control whose word is beyond the inline end stands on its left in Arabic, and the CSS tip is
  centred above its control;
* a dialog's head reads from the right: the title at the right, «Fermer» at the left.

Chromium at 1440 × 900 on an Arabic document (`<html lang="ar" dir="rtl">`) made of the real components, rendered by
Django through a URL of this module; the strings are the catalogue's. The document draws dialogs, sheets, drawers with
their heads and a CSS tip, so it links the page-only sheet as CONTRACT §1 says (`css/dist/core/overlay-panels.css`).
"""

from __future__ import annotations

import os

import pytest
from django.http import HttpResponse
from django.template import Context, Template
from django.urls import path
from django.utils import translation
from django.utils.safestring import mark_safe

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

PAGE = """{% load static i18n %}<!doctype html>
<html lang="ar" dir="rtl" class="no-js"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{% translate "Menu" %}</title>
<link rel="stylesheet" href="{% static 'css/dist/main.css' %}">
<link rel="stylesheet" href="{% static 'css/dist/core/overlay-panels.css' %}">
<link rel="stylesheet" href="{% static 'css/dev/overlay-board.css' %}">
<script src="{% static 'js/head.js' %}"></script>
<script type="module" src="{% static 'js/dist/overlay.js' %}"></script>
</head><body>
<main id="main-content" class="container ob__main" tabindex="-1">
  <div class="cluster">
    <a class="btn btn--secondary" href="#nav" data-overlay-open>{% translate "Menu" %}</a>
    <a class="btn btn--secondary" href="#detail" data-overlay-open>{% translate "Mes documents" %}</a>
    <a class="btn btn--secondary" href="#languages" data-overlay-open>{% translate "Langue" %}</a>
    <a class="btn btn--secondary" href="#delete" data-overlay-open>{% translate "Supprimer mon compte" %}</a>
    <button class="btn btn--secondary" type="button" id="account" popovertarget="account-menu">{% translate "Mon compte" %}</button>
  </div>
  {% translate "Rechercher" as search %}{% translate "Consulter" as view %}
  <div class="cluster ob__toolbar" data-tip-group>{% include "components/tooltip.html" with label=search icon="search" %}</div>
  <ul class="ob__scroller" role="list">
    <li class="ob__row"><span>{% translate "Tableau de bord" %}</span>{% include "components/tooltip.html" with label=view icon="eye" layer=True side="inline-end" %}</li>
  </ul>
</main>
{% translate "Menu" as t_menu %}{% translate "Mes documents" as t_docs %}{% translate "Langue" as t_lang %}{% translate "Supprimer mon compte" as t_delete %}
{% include "components/drawer.html" with id="nav" edge="start" title=t_menu body=rows %}
{% include "components/drawer.html" with id="detail" modal=False title=t_docs body=rows %}
{% include "components/sheet.html" with id="languages" title=t_lang body=rows %}
{% include "components/dialog.html" with id="delete" kind="alert" glyph="trash-2" title=t_delete body=sentence actions=actions %}
{% include "components/popover.html" with id="account-menu" body=rows %}
</body></html>"""


def _page(request):
    with translation.override("ar"):
        rows = mark_safe(
            '<ul class="overlay__list" role="list">'
            + "".join(
                f'<li><a class="overlay__item" href="#main-content">{translation.gettext(word)}</a></li>'
                for word in ("Tableau de bord", "Mes dossiers", "Mes documents")
            )
            + "</ul>"
        )
        sentence = mark_safe(f"<p>{translation.gettext('Cette action est définitive.')}</p>")
        actions = mark_safe(
            f'<button class="btn btn--secondary" type="button" data-overlay-close data-overlay-safe>{translation.gettext("Annuler")}</button>'
            f'<button class="btn btn--danger" type="button" data-overlay-close>{translation.gettext("Confirmer la suppression")}</button>'
        )
        html = Template(PAGE).render(Context({"rows": rows, "sentence": sentence, "actions": actions}))
    return HttpResponse(html)


urlpatterns = [path("overlays-ar/", _page)]

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True), pytest.mark.urls(__name__)]

#: Stretch a panel's clocks to 900 ms, so the arrival can be read frame by frame on a busy machine.
SLOW_JS = """(id) => { const d = document.getElementById(id);
  for (const name of ['--overlay-in', '--overlay-out', '--overlay-scrim-in']) d.style.setProperty(name, '900ms'); }"""
BOX_JS = "(id) => { const r = document.getElementById(id).getBoundingClientRect(); return {x: r.x, y: r.y, right: r.right, w: r.width, bottom: r.bottom}; }"


@pytest.fixture(scope="module")
def browser():
    playwright = pytest.importorskip("playwright.sync_api")
    with playwright.sync_playwright() as p:
        try:
            instance = p.chromium.launch()
        except Exception as exc:  # pragma: no cover - browser not installed
            pytest.skip(f"Chromium not available: {exc}")
        yield instance
        instance.close()


@pytest.fixture
def page(browser, live_server):
    context = browser.new_context(viewport={"width": 1440, "height": 900}, device_scale_factor=1, locale="ar-MA")
    page = context.new_page()
    page.goto(f"{live_server.url}/overlays-ar/", wait_until="networkidle")
    page.evaluate("async () => { await document.fonts.ready }")
    assert page.evaluate("document.documentElement.dir") == "rtl"
    try:
        yield page
    finally:
        context.close()


def _arrival(page, panel: str) -> tuple[dict, dict]:
    """The panel's box 150 ms into a stretched opening, and at rest."""
    page.evaluate(SLOW_JS, panel)
    page.click(f'a[href="#{panel}"]')
    page.wait_for_timeout(150)
    moving = page.evaluate(BOX_JS, panel)
    page.wait_for_timeout(1000)
    return moving, page.evaluate(BOX_JS, panel)


def test_the_navigation_drawer_comes_from_the_right_and_a_detail_from_the_left(page):
    moving, rest = _arrival(page, "nav")
    assert abs(rest["right"] - 1440) <= 1, ("the reading edge is the right in Arabic", rest)
    assert moving["x"] > rest["x"] + 4, ("it arrives from the right", moving, rest)
    page.keyboard.press("Escape")
    page.wait_for_timeout(300)
    moving, rest = _arrival(page, "detail")
    assert abs(rest["x"]) <= 1, ("a detail stands at the inline end: the left in Arabic", rest)
    assert moving["right"] < rest["right"] - 4, ("it arrives from the left", moving, rest)


def test_the_sheet_rises_from_the_bottom_and_does_not_mirror(page):
    moving, rest = _arrival(page, "languages")
    assert abs(rest["x"] - (1440 - rest["w"]) / 2) <= 1, ("centred, whatever the direction", rest)
    assert abs(moving["x"] - rest["x"]) <= 0.5 and moving["y"] > rest["y"] + 4, ("a vertical travel only", moving, rest)


def test_a_menu_aligns_on_its_triggers_inline_end(page):
    page.click("#account")
    page.wait_for_timeout(400)
    trigger = page.locator("#account").bounding_box()
    menu = page.evaluate(BOX_JS, "account-menu")
    assert abs(menu["x"] - trigger["x"]) <= 1, ("the menu's left edge on the trigger's left edge", menu, trigger)


def test_the_tips_follow_the_direction(page):
    control = '.ob__scroller [data-tip="layer"]'
    page.hover(control)
    page.wait_for_timeout(700)
    tip = page.evaluate(
        "() => { const r = document.querySelector('.tooltip').getBoundingClientRect(); return {x: r.x, right: r.right}; }"
    )
    scroller = page.locator(".ob__scroller").bounding_box()
    assert tip["right"] <= scroller["x"] + 1, ("beyond the inline end: on the left in Arabic", tip, scroller)
    page.mouse.move(5, 5)
    button = "[data-tip-group] [data-tip]"
    page.hover(button)
    page.wait_for_timeout(700)
    box = page.locator(button).bounding_box()
    hit = page.evaluate(
        "([x, y, sel]) => document.elementFromPoint(x, y) === document.querySelector(sel)",
        [box["x"] + box["width"] / 2, box["y"] - 14, button],
    )
    assert hit, "the CSS tip is centred above its control in Arabic too"


def test_a_dialogs_head_reads_from_the_right(page):
    page.click('a[href="#delete"]')
    page.wait_for_timeout(500)
    title = page.locator("#delete .overlay__title").bounding_box()
    close = page.locator("#delete .overlay__close").bounding_box()
    glyph = page.locator("#delete .overlay__glyph").bounding_box()
    assert glyph["x"] > title["x"] and close["x"] + close["width"] < title["x"], (
        "glyph · title … «Fermer», from the right",
        glyph,
        title,
        close,
    )
    assert page.evaluate("document.activeElement.hasAttribute('data-overlay-safe')"), "the safe answer takes the focus"
