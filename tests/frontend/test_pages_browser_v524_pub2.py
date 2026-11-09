"""
V5.24 — the professional pass on the system, trust and reading pages, lane PUB2, in Chromium (FINAL_DELIVERY_V2 §3.6 and its
gate; BACKGROUND_MATERIAL_V2 §3.2, §4.2, §5.2; TYPOGRAPHY_V2 F-3, F-7; label v524-pub2-build): what the server cannot show
(tests/frontend/test_pages_v524_pub2.py holds the markup's rules).

* the Forum's «raccordo» (§4.2's browser contract): the first child of the band it enters stands drawn from the pair's
  foot to the band's head line — its node within 2 px of the head line, on the station axis from 64 rem (the second
  column's start plus the rings' 11 px, mirrored in Arabic) and on the reading edge below it; it plays once on the
  band's trigger and leaves getAnimations(); under reduced motion the line stands drawn and no state is written;
* Le projet's «incastro»: the doors' arched tops the whole 64 px over the photograph (the band begins 64 px above the
  frame's foot, its padding 0, the first door at the band's top), in French and in Arabic, on a desktop and a phone;
* AGAMI's registers in the label role: Host Grotesk on the Latin pages, Readex Pro on the Arabic one — never ILE Mono
  (F-3), the plate on the stone band;
* the FAQ's explorer on stone: the band's ground is the area's and the answer plate stands raised on it.

Chromium on the live server, the seeded site, gate G3 open, the Forum's seeded edition (the fixtures of
tests/frontend/test_pages_browser_v522_p2.py).
"""

from __future__ import annotations

import datetime as dt
import os

import pytest

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")

pytestmark = [pytest.mark.browser, pytest.mark.django_db(transaction=True)]

RACCORDO = r"""() => {
  const band = document.querySelector('.forum-filo');
  const pair = document.querySelector('.forum-pair').getBoundingClientRect(), bb = band.getBoundingClientRect();
  return {drawn: band.querySelectorAll('.sez-raccordo').length, seam: bb.top, pairBottom: pair.bottom, state: band.dataset.secState || null,
          running: document.getAnimations().filter((a) => a.playState === 'running' && a.effect && a.effect.target === band).length};
}"""

INCASTRO = r"""() => {
  const img = document.querySelector('.projet-panorama img'), band = document.querySelector('.projet-porte');
  const door = band.querySelector('.mosaico__tessera'), h2 = document.getElementById('project-spaces-title');
  const ib = img.getBoundingClientRect(), bb = band.getBoundingClientRect(), db = door.getBoundingClientRect();
  return {over: ib.bottom - db.top, bandUp: ib.bottom - bb.top, padding: getComputedStyle(band).paddingBlockStart,
          incastro: band.hasAttribute('data-incastro'), h2: h2 ? h2.offsetWidth <= 1 && h2.offsetHeight <= 1 : null,
          rule: !!band.querySelector('.testa__rule')};
}"""

FACES = r"""(sels) => sels.map((sel) => [...document.querySelectorAll(sel)].map((e) => getComputedStyle(e).fontFamily.split(',')[0].replace(/"/g, '')))"""


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
def site(live_server, seeded, set_flag, monkeypatch, legal_published, whatsapp_channel):
    from core import clock, flags
    from forum.seeds import seed_forum_event

    fixed = dt.datetime(2026, 10, 3, 10, 0, tzinfo=dt.UTC)
    monkeypatch.setattr(clock, "now", lambda: fixed)
    set_flag("phase3_public", True, enabled_from=dt.datetime(2026, 10, 2, tzinfo=dt.UTC))
    seed_forum_event()
    flags.invalidate()
    yield live_server.url
    flags.invalidate()


def _settle(page, selector: str) -> None:
    page.evaluate(f"document.querySelector('{selector}').scrollIntoView({{block: 'center'}})")
    page.wait_for_timeout(2400)  # the band's own line, then the raccordo's --motion-draw after --sez-d


# ---- the Forum's raccordo ------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("lang", ["fr", "ar"])
@pytest.mark.parametrize("width, height", [(1440, 900), (390, 844)])
def test_no_raccordo_crosses_into_the_forum_s_story_and_the_band_enters_once(browser, site, lang, width, height):
    """V5.30 Fast Visual Variety Correction §5 (V5.20 strict rule; this decision replaces the raccordo that landed on the head
    line): no line crosses the seam; the band follows the pair and enters once."""
    context = browser.new_context(viewport={"width": width, "height": height}, reduced_motion="no-preference")
    try:
        page = context.new_page()
        page.goto(f"{site}/{lang}/forum/", wait_until="networkidle")
        _settle(page, ".forum-filo")
        got = page.evaluate(RACCORDO)
        assert got["drawn"] == 0, got
        assert abs(got["seam"] - got["pairBottom"]) <= 1, got
        assert got["running"] == 0 and got["state"] == "in", got
    finally:
        context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_under_reduced_motion_the_story_band_stands_still_and_no_state_is_written(browser, site, lang):
    """V5.30 Fast Visual Variety Correction §5 (V5.20 strict rule): as above, under reduced motion."""
    context = browser.new_context(viewport={"width": 1440, "height": 900}, reduced_motion="reduce")
    try:
        page = context.new_page()
        page.goto(f"{site}/{lang}/forum/", wait_until="networkidle")
        page.evaluate("document.querySelector('.forum-filo').scrollIntoView({block: 'center'})")
        page.wait_for_timeout(500)
        got = page.evaluate(RACCORDO)
        assert got["drawn"] == 0 and got["state"] is None and got["running"] == 0, got
    finally:
        context.close()


# ---- Le projet's incastro ------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("lang", ["fr", "ar"])
@pytest.mark.parametrize("width, height", [(1440, 900), (1024, 768), (390, 844)])
def test_le_projet_s_doors_stand_64px_over_the_volumes(browser, site, lang, width, height):
    context = browser.new_context(viewport={"width": width, "height": height}, reduced_motion="reduce")
    try:
        page = context.new_page()
        page.goto(f"{site}/{lang}/le-projet/", wait_until="networkidle")
        page.evaluate("document.querySelector('.projet-porte').scrollIntoView({block: 'center'})")
        page.wait_for_timeout(400)
        got = page.evaluate(INCASTRO)
        assert got["incastro"] and got["padding"] == "0px" and got["rule"] is False and got["h2"] is True, got
        assert abs(got["over"] - 64) <= 1 and abs(got["bandUp"] - 64) <= 1, got
    finally:
        context.close()


# ---- AGAMI's registers and the FAQ's stone ------------------------------------------------------------------------------
@pytest.mark.parametrize("lang, face", [("fr", "Host Grotesk"), ("ar", "Readex Pro")])
@pytest.mark.parametrize("width, height", [(1440, 900), (390, 844)])
def test_agami_s_registers_are_in_the_label_role_s_face_never_the_mono(browser, site, lang, face, width, height):
    context = browser.new_context(viewport={"width": width, "height": height})
    try:
        page = context.new_page()
        page.goto(f"{site}/{lang}/agami/", wait_until="networkidle")
        page.evaluate("document.fonts.ready")
        faces = page.evaluate(
            FACES, [".agami-id__etichetta", ".agami-id__voce > dt:not([lang])", ".agami-id__etichetta-voce"]
        )
        assert faces[0] and faces[2], faces
        for group in faces:
            assert "ILE Mono" not in group and all(f in (face, "Host Grotesk") for f in group), (lang, group)
        assert faces[0] == [face] and faces[2] == [face, face], faces
        plate = page.evaluate("getComputedStyle(document.querySelector('.agami-identita__lastra')).backgroundColor")
        band = page.evaluate("getComputedStyle(document.querySelector('.agami-identita')).backgroundColor")
        assert plate != band, (plate, band)
    finally:
        context.close()


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_faq_explorer_stands_on_stone_with_its_plate_raised(browser, site, lang):
    context = browser.new_context(viewport={"width": 1440, "height": 900})
    try:
        page = context.new_page()
        page.goto(f"{site}/{lang}/faq/", wait_until="networkidle")
        got = page.evaluate("""() => { const root = document.documentElement, cs = getComputedStyle(root);
            const band = getComputedStyle(document.querySelector('.faq-esploratore')).backgroundColor;
            const pcs = getComputedStyle(document.querySelector('.indice__palco'));
            const plate = pcs.backgroundColor, plateImage = pcs.backgroundImage;
            const rimando = getComputedStyle(document.querySelector('.faq-rimando')).backgroundColor;
            const probe = document.createElement('div'); document.body.appendChild(probe);
            probe.style.background = 'var(--surface-area)'; const area = getComputedStyle(probe).backgroundColor;
            probe.style.background = 'var(--surface-page)'; const paper = getComputedStyle(probe).backgroundColor; probe.remove();
            return {band, plate, plateImage, rimando, area, paper}; }""")
        assert got["band"] == got["area"] and got["rimando"] == got["paper"], got
        # the plate is painted, never the band's ground showing through: a face of its own colour, or SYS's layered
        # material (V5.29 stream SYS, merged: the plate's face a gradient lit from above, its colour transparent)
        painted = got["plate"] not in (got["area"], "rgba(0, 0, 0, 0)") or "gradient" in got["plateImage"]
        assert painted, got
    finally:
        context.close()
