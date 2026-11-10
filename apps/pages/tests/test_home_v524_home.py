"""
V5.24 — the homepage's professional pass (FINAL_DELIVERY_V2 §3.4; lane HOME, label v524-home). Without a browser (the
browser half is test_home_browser_v524_home.py):

* the material placed on the home's seams as the Director decided (BACKGROUND_MATERIAL_V2 §3.1, §3.2, §5.1; R3): the
  index «l'indice» on stone, «la protezione» on the dressed stone «pietra», the orientation's wash dissolving over its
  last 6 rem into the stone («sfumatura», the velatura at the fade's height), the pilot's gold seam beginning 32 px
  above the night («il raccordo», the primitive as the panel's first child, rising, on the seam's axis, in the thread's
  gold), the night veiling the masonry's first 12 rem («velatura», a night stop at the top of the stone veil, still),
  the promoter's band lit at the arch's sill («carta viva», the recipe's light anchored to the frame) — each from
  v5/_materia.css through v5/_casa.css, tokens only, nothing moving of its own;
* the type contract applied in the home's own sheets (TYPOGRAPHY_V2 §4.2, §6; F-1, F-3, F-4; T's burn-down): the
  statement at the display weight and tracking through the tokens, the primary call's weight through the token, the
  route's caption and the colophon's labels the label role by name, the origin call on the caption step, the phone word
  on the ui leading, no mono, no credit rule, the colophon's name on the title-2 step;
* the budgets (R4 d): the home's five sheets within the §7.1 letter, pages.css and hero.css within their ceilings,
  home.js unchanged; the material partial imported by the home's sheet, never by main.css.
"""

from __future__ import annotations

import gzip
import re
from pathlib import Path

import pytest
from django.conf import settings

from pages.tests.conftest import section_order

pytestmark = pytest.mark.django_db

ROOT = Path(settings.BASE_DIR)
DIST = ROOT / "static" / "css" / "dist"
PAGES = ROOT / "apps" / "pages" / "static" / "pages" / "css" / "pages.css"
HERO = ROOT / "apps" / "pages" / "static" / "pages" / "css" / "hero.css"
CASA = ROOT / "static" / "css" / "v5" / "_casa.css"
MATERIA = ROOT / "static" / "css" / "v5" / "_materia.css"
HOME_TEMPLATES = ROOT / "templates" / "pages" / "home"


def _code(path: Path) -> str:
    return re.sub(r"/\*.*?\*/", "", path.read_text(encoding="utf-8"), flags=re.S)


def _rules(css: str) -> list[tuple[str, str]]:
    """(selector, body) of every rule, the at-rules opened."""
    css = re.sub(r"@(media|supports|container)[^{]*\{", "", _code_text(css))
    return [(" ".join(sel.split()), " ".join(body.split())) for sel, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css)]


def _code_text(css: str) -> str:
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def _rule(css: str, selector: str) -> str:
    bodies = [body for sel, body in _rules(css) if sel == selector]
    assert bodies, selector
    return bodies[0]


def _sections(html: str) -> dict[str, dict]:
    main = html.split('<main id="main-content"', 1)[1].split("</main>", 1)[0]
    out = {}
    for tag in re.findall(r"<section class=\"sez [^>]*>", main):
        attrs = dict(re.findall(r'([a-z-]+)="([^"]*)"', tag))
        out[attrs["data-section"]] = attrs
    return out


# ----------------------------------------------------------------------------------------------- the grounds and seams


@pytest.mark.parametrize("state", ["closed", "open"])
def test_the_index_stands_on_stone_the_protection_on_pietra_and_the_seams_follow_the_grounds(
    request, page, seeded, state
):
    """FINAL_DELIVERY_V2 §3.4 (S3 ground stone; S6 pietra; S2 → S3 sfumatura; S3 → S4 raccordo): in both gate states the
    index band is stone and the wash's foot dissolves into it (`data-sfuma="stone"`); with the gate open «la protezione»
    stands on pietra. V5.30 Fast Visual Variety Correction §5 (V5.20 strict rule; S3 → S4 raccordo left with its gold
    thread):
    no raccordo on the home in either state, the pilot's panel opens on its photographs."""
    if state == "open":
        request.getfixturevalue("phase3_open")
    _response, html = page("/fr/")
    sections = _sections(html)
    assert sections["pathways"]["data-ground"] == "stone"
    assert sections["orientation"]["data-sfuma"] == "stone", sections["orientation"]
    assert "data-sfuma" not in {k for s in sections.values() if s["data-section"] != "orientation" for k in s}
    order = [k for k in section_order(html) if k not in ("hero", "banner")]
    assert order.index("orientation") + 1 == order.index("pathways"), "the fade is into the band that follows"
    if state == "open":
        assert sections["antifraud"]["data-ground"] == "pietra"
        pilot = html.split('data-section="pilot"', 1)[1].split("</section>", 1)[0]
        assert re.match(r'[^>]*>\s*<div class="panorama panorama--coppia pilota">', pilot), pilot[:400]
    else:
        assert "pilot" not in sections
    assert "sez-raccordo" not in html


def test_no_raccordo_enters_the_home_s_night_and_the_primitive_stays_in_the_library():
    """V5.30 Fast Visual Variety Correction §5 (V5.20 strict rule; this decision replaces BACKGROUND_MATERIAL_V2 §3.2
    R3 and
    §5.1 S3 on the home): the gold seam and its line into the pilot's night leave «la casa»; the library's primitive
    stays
    for the pages that keep a route (§7 PARCOURS)."""
    casa = re.sub(r"/\*.*?\*/", "", CASA.read_text(encoding="utf-8"), flags=re.S)
    assert "sez-raccordo" not in casa and "identity-light" not in casa
    materia = MATERIA.read_text(encoding="utf-8")
    assert ".sez-raccordo--risale" in materia and "--raccordo-x" in materia and "--sez-raccordo" in materia


def test_the_sfumatura_is_the_velatura_at_six_rem():
    """BACKGROUND_MATERIAL_V2 §3.2 «sfumatura — the velatura recipe with block-size: 6rem»: the one override on the
    library's layer, above the primitive's phone rule by specificity (the fade is 6 rem at every width)."""
    casa = CASA.read_text(encoding="utf-8")
    assert _rule(casa, ".page-home .home-orientation::after") == "block-size: 6rem;"
    assert "data-sfuma" not in _code(CASA), "the attributes are read by the material partial alone (LIB's guard)"
    materia = MATERIA.read_text(encoding="utf-8")
    assert re.search(r'\.sez\[data-sfuma="stone"\] \{ --sez-next: var\(--surface-area\); \}', materia)
    assert re.search(r"\.sez\[data-sfuma\]::after \{[^}]*block-size: 12rem;", materia)


def test_the_night_veils_the_masonry_s_first_twelve_rem_and_nothing_moves():
    """BACKGROUND_MATERIAL_V2 §3.2 «velatura», §5.1 S4 «the night veils the masonry's first 12 rem (8 on phones) —
    .home-trust .strato--foto::before gains the night stop at its top»: the night first, over the stone veil, running
    its 12 rem (--notte-fino; 8 below 48 rem) and front-loaded — two fifths at an eighth of the run, an eighth at a
    third — so the band's head stands on the stone at its contrast (measured in the browser half); a fade is a ground:
    «la casa» holds no animation and no transition."""
    casa = CASA.read_text(encoding="utf-8")
    body = _rule(casa, ".page-home .home-trust .strato--foto::before")
    assert body.startswith("--notte-fino: 12rem; background: linear-gradient( var(--surface-night),"), body
    assert "color-mix(in srgb, var(--surface-night) 40%, transparent) calc(var(--notte-fino) / 8)" in body
    assert "color-mix(in srgb, var(--surface-night) 12%, transparent) calc(var(--notte-fino) / 3)" in body
    assert (
        "transparent var(--notte-fino) ), linear-gradient( "
        "color-mix(in srgb, var(--surface-area) 88%, transparent) 15rem," in body
    )
    phone = [
        b for s, b in _rules(casa) if s == ".page-home .home-trust .strato--foto::before" and b == "--notte-fino: 8rem;"
    ]
    assert len(phone) == 1, "the phone's 8 rem"
    code = _code(CASA)
    assert "animation" not in code and "transition" not in code
    assert not re.search(r"#[0-9a-fA-F]{3,8}\b|\brgba?\(", code), "tokens only"


def test_the_promoter_s_band_is_lit_at_the_arch_s_sill():
    """BACKGROUND_MATERIAL_V2 §3.1 «carta viva», §5.1 S7 lit the promoter's band at the arch's sill (a layer under the
    frame). RESTATED under V5.20 (the strict test-update rule) for the owner's V5.30 (7 Nov 2026, «geometry saturation»:
    arches and door forms «as BRAND SIGNATURES, stop using them as the default»; §7 Italy + Morocco on «a homepage
    cooperation / pilot moment»; stream A): the arch and its sill left the frame, so the light anchored to the sill went
    with them — asserted ABSENT, so it cannot silently return. The band's ground is now the Italy + Morocco field: the
    primitive «l'intesa» in its «atmosfera» variant (ecosystem/partials/intesa.html, aria-hidden), its two partials
    imported by pages.css after the material partial and before «la casa»; the band still carries no data-luce (the
    recipe whose anchor is the band's corner), and the material recipe stands as it was."""
    casa = CASA.read_text(encoding="utf-8")
    assert ".home-ecosystem .campata__media::before" not in casa, "the sill's light left with the arch"
    ecosystem = (HOME_TEMPLATES / "_ecosystem.html").read_text(encoding="utf-8").split("{% endcomment %}", 1)[1]
    assert "data-luce" not in ecosystem
    # FINAL MICRO-PASS §5 A3 (V5.20 strict rule: the band's lines, triangles and blurred fields left the home): the
    # band draws no «intesa» and the home's sheet imports neither of its partials; the material partial still stands
    # before «la casa»
    assert "intesa" not in ecosystem
    imports = re.findall(r'@import url\("\.\./\.\./css/v5/(_[a-z0-9-]+)\.css"\);', PAGES.read_text(encoding="utf-8"))
    assert "_intesa" not in imports and "_intesa-atmosfera" not in imports
    assert imports.index("_materia") < imports.index("_casa")
    materia = MATERIA.read_text(encoding="utf-8")
    assert 'data-luce="origine"' in materia and "radial-gradient(60% 50% at 0 0" in materia, "the recipe stands"


# ------------------------------------------------------------------------------------------------- the type contract


def test_the_statement_and_the_primary_call_take_their_weight_through_the_tokens_alone():
    """TYPOGRAPHY_V2 F-1 and §4.2; FINAL_DELIVERY_V2 §3.4 row 0 «the display weight and the primary call's weight arrive
    through T's tokens only»: `.he__promise` reads --w-display and --track-display (its size, --promise-fs, and its
    positions are the preserved first screen's); `.btn.cta-b` no longer restates a weight, so .btn--primary's 600
    reaches the call, whose size stays the hero's own (.he__primary on --t-ui)."""
    hero = HERO.read_text(encoding="utf-8")
    promise = _rule(hero, ".he__promise")
    assert "font-weight: var(--w-display);" in promise and "letter-spacing: var(--track-display);" in promise, promise
    assert "font-size: var(--promise-fs);" in promise
    assert not re.search(r"font-weight: 500|letter-spacing: -0\.028em", promise)
    cta = _rule(hero, ".btn.cta-b")
    assert "font-weight" not in cta and "line-height: var(--t-ui-lh);" in cta, cta
    assert "font-size: var(--t-ui);" in _rule(hero, ".he__primary")
    buttons = (ROOT / "static" / "css" / "v5" / "buttons.css").read_text(encoding="utf-8")
    assert re.search(r"\.btn--primary \{[^}]*font-weight: var\(--w-title\);", buttons), "T's primary call at 600"


def test_the_home_s_sheets_read_the_twelve_steps_and_the_roles():
    """TYPOGRAPHY_V2 F-3 / F-4, §6 (T's burn-down, FINAL_DELIVERY_V2 §3.1): no mono in the home's sheets (the route's
    caption and the colophon's labels are the label role by name — `t-label` in the templates), the origin call on the
    caption step (12/16; 14/20 in Arabic: the floor), the phone word at 1.2, 1.3 in Arabic by the tokens' increment
    (never under 1.3 em), the colophon's name on the title-2 step, no credit rule (V5.24 §2), the fragments' first
    letter a capital (not a label's capitals), the landscape promise's clamp the hero's own property."""
    pages, hero = PAGES.read_text(encoding="utf-8"), HERO.read_text(encoding="utf-8")
    for sheet in (pages, hero, CASA.read_text(encoding="utf-8")):
        assert "var(--f-mono)" not in _code_text(sheet)
        assert "foto__credit" not in sheet
    # FINAL MICRO-PASS §5 A1 (V5.20 strict rule: the route's caption drawn for the eye left — the section's head says
    # it): no rule and no markup draw it; the whole sentence is still said once (test_home.py)
    assert ".orienta__didascalia" not in _code_text(pages)
    orientation = (HOME_TEMPLATES / "_orientation.html").read_text(encoding="utf-8")
    assert "orienta__didascalia" not in orientation.split("{% endcomment %}", 1)[1]
    colophon = (HOME_TEMPLATES / "_ecosystem_colophon.html").read_text(encoding="utf-8")
    assert colophon.count('class="testa__label colofone__label t-label"') == 2
    assert _rule(pages, ".colofone__nome") == (
        "font-size: var(--t-title-2); line-height: var(--t-title-2-lh); letter-spacing: var(--track-title-2);"
    )
    assert _rule(pages, ".home-reserved__title").endswith("letter-spacing: var(--track-label);")
    assert _rule(pages, ".pilota__titolo:lang(ar)") == "letter-spacing: 0;", "the Arabic display leading is the tokens'"
    assert re.search(r"::first-letter \{\s*text-transform: capitalize;\s*\}", pages)
    assert "text-transform: uppercase" not in _code_text(pages)
    call = _rule(hero, ".he-origin__call")
    assert "font-size: var(--t-caption); line-height: var(--t-caption-lh);" in call, call
    assert "0.75rem" not in call, (
        "the origin call's literal 12 px is gone (the preserved stations keep theirs, row 0 KEEP)"
    )
    words = [b for s, b in _rules(hero) if s == ".he-origin__word" and "padding-block-end: 1.125rem" in b]
    assert len(words) == 1 and "line-height: calc(1.2 + var(--ar-lh-plus));" in words[0], words  # 1.2; 1.3 in Arabic
    assert not re.search(r"\.he__promise \{ font-size: clamp", _code_text(hero)), "folded into --promise-fs"
    assert "--promise-fs: clamp(1.375rem, 4.6vh, 1.75rem); --promise-lh: 1.1;" in hero
    narrow = hero.split("@media (max-width: 22.5rem) {", 1)[1].split("}", 1)[0]
    assert " ".join(narrow.split()) == ".he__primary { font-size: 0.9375rem;", narrow


def test_the_preserved_hero_keeps_its_glints_and_the_home_s_sheets_have_no_empty_rule():
    """FINAL_DELIVERY_V2 §3.4 row 0 KEEP (the v524-home targeted check's blocker 2): on the desktop the three inner
    stations' glint is centred on its node (`calc(50% - 10.5px)`; without it the glint fell back to the label's start
    edge, 47–63 px off its node at 1280 and 1440 during the travelling light), the first and the last keep their edge
    offsets; and no rule of the home's sheets is left empty by the redundancy pass (the check's minor 4)."""
    hero = HERO.read_text(encoding="utf-8")
    desktop = hero.split("@media (min-width: 64rem) {", 1)[1]
    assert re.search(
        r"\.he-station:is\(:nth-child\(2\), :nth-child\(3\), :nth-child\(4\)\) \.he-station__lit \{ "
        r"inset-inline-start: calc\(50% - 10\.5px\); \}",
        desktop,
    ), "the inner stations' glint on its node"
    assert re.search(r"\.he-station__lit \{ [^}]*inset-inline-start: calc\(var\(--node\) / 2 - 10\.5px\);", desktop)
    assert (
        ".he-station:nth-child(5) .he-station__lit { inset-inline-start: auto; "
        "inset-inline-end: calc(var(--node) / 2 - 10.5px); }" in desktop
    )
    for sheet in (PAGES, HERO, CASA):
        empty = [sel for sel, body in _rules(sheet.read_text(encoding="utf-8")) if not body.strip()]
        assert not empty, (sheet.name, empty)


# ------------------------------------------------------------------------------------------------- the budgets


def _gz(path: Path) -> int:
    return len(gzip.compress(path.read_bytes(), 9))


def test_the_home_total_holds_the_letter_with_the_material_in_it():
    """FINAL_DELIVERY_V2 R4 (a) and (d): the home's five sheets (main, pages, hero, reveal, portico) ≤ 61 440 B gzip -9
    with v5/_materia.css imported by pages.css (after the shell, before «la casa», never by main.css); pages.css ≤ 12
    288, hero.css ≤ 11 264, home.js unchanged ≤ 8 192. Never raised: the material's bytes were paid inside the home's
    sheets."""
    sheets = ["main.css", "pages/css/pages.css", "pages/css/hero.css", "core/reveal.css", "core/portico.css"]
    total = sum(_gz(DIST / s) for s in sheets)
    assert total <= 61_440, total
    assert _gz(DIST / "pages" / "css" / "pages.css") <= 12_288
    assert _gz(DIST / "pages" / "css" / "hero.css") <= 11_264
    assert _gz(ROOT / "static" / "js" / "dist" / "home.js") <= 8_192
    source = PAGES.read_text(encoding="utf-8")
    imports = re.findall(r'@import url\("\.\./\.\./css/v5/(_[a-z0-9-]+)\.css"\);', source)
    assert imports.index("_sezioni") < imports.index("_materia") < imports.index("_casa"), imports
    assert "_materia" not in (ROOT / "static" / "css" / "main.css").read_text(encoding="utf-8")
    dist = (DIST / "pages" / "css" / "pages.css").read_text(encoding="utf-8")
    assert "data-ground=pietra" in dist and ".sez-raccordo" in dist and "data-sfuma" in dist, (
        "the material in the bundle"
    )
