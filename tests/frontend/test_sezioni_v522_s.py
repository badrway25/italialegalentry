"""
Section System V2, Icon Treatment V2, Motion Density V2 — the foundation of V5.22 (SECTION_SYSTEM_V2 §2, §4, §5, §7,
§9.1; lane S). Fast checks on the sources, the registry, the built files and a few rendered heads:

* the thirteen ILE marks: one 48-grid source each, their inline T1 partials and their T2 sprite copies current; every
  stroke of a partial drawn on `pathLength="1"`; the marks sprite under its 16 KiB; the registry's maps (MARKS, FOLIO,
  the stations and seats of §3) name registered symbols, never the stair, never `users` where §3 forbids it;
* the head folio: its T1 seal where the page's concept has a mark, a typographic label elsewhere; no bare chapter mark;
* the motion vocabulary V2: every entrance on the section trigger, fill `backwards`, held only under no-preference,
  never on html.rm or the keyboard; no new duration or curve token; the M22 fix and the M21 accent;
* the gold budget of the bodies (§4.5): gold only where the decisions put it; hover equals focus (§4.10);
* the budgets of §7: each pattern sheet under its ceiling (gzip -9), the section modules under theirs, split chunks
  loaded by rise.js only;
* the login's eyebrow key: a T5 mark at 20 px in ink, never gold on paper.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import pytest
from django.template import Context, Template

from core import icons

ROOT = Path(__file__).resolve().parents[2]
V5 = ROOT / "static" / "css" / "v5"
MARKS_SRC = ROOT / "static" / "icons" / "marks"
PARTIALS = ROOT / "templates" / "components" / "sezioni" / "marks"
DIST_JS = ROOT / "static" / "js" / "dist"
SRC_JS = ROOT / "static" / "js" / "src"
#: §2 / §7 ceilings of the pattern sheets, gzip -9 of each partial minified alone (1 KB = 1 024 B)
#: CLOSING (FINAL_DELIVERY_V2 §3.9 c; V5.20, a ratchet): the values below recorded at their measure on v524-closing — only down.
SHEET_CEILINGS = {
    "_sec-campata.css": 973, "_sec-tracciato.css": 1_420, "_sec-racconto.css": 915,
    # v524-lib (FINAL_DELIVERY_V2 R4 f, §3.3; BACKGROUND_MATERIAL_V2 §3.4, §4.1): the tile's face light — the layer, its
    # wait and in rules — lives in the mosaico sheet as the audit placed it (the shell is in every page sheet, R4 a):
    # 1 203 → 1 355 measured (the audited «≈ 120» was an estimate: the same block cost 70 B among the shell's neighbours and
    # costs 152 B alone here; no declaration can go — the layer's corner, its context, its first frame); re-recorded at the
    # measure, never up; no route sheet or page total moves past its ceiling (QA/v524/lib/NOTES.md §6, §10)
    "_sec-mosaico.css": 1_355,
    "_sec-mappa.css": 1_307, "_sec-filo.css": 1_012, "_sec-passaggio.css": 611,
    # V5.29 (stream SYS; V5.20: stronger — the two sheets' ceilings lowered to what they now hold, the two new parts each
    # with its own): «lo strato» and «l'indice» split so the home bundles what it draws — the plates and «la protezione»
    # (_sec-lastre.css), the list, the tabs and the phone's disclosure (_sec-indice-base.css); the strato sheet (the
    # landing, the address and term plates) and the index sheet (the explorer, the native disclosure) import them
    "_sec-strato.css": 654, "_sec-lastre.css": 1_253, "_sec-indice.css": 524, "_sec-indice-base.css": 1_207,
    # the two variants with page-only partials of their own (lane S): «la boussole» (A) and «l'emiciclo» (H)
    "_sec-boussole.css": 651, "_sec-emiciclo.css": 661,
    # round 1 (QA_ROUND1 m2): F's measured variant «il flusso» — a page-only partial of its own, after the passage V2,
    # only where a curve joins real boxes (EN-1): a new sheet, a new ceiling (0.9 KB)
    "_sec-flusso.css": 868,
}
#: §2 D and F: what the panorama adds to _photo.css and the passage V2 (_linea-v2.css) adds to the passage, gzip -9
#: CLOSING (FINAL_DELIVERY_V2 §3.9 c; V5.20, a ratchet — the review's minor): recorded at their measure (716 → 576,
#: 1 229 → 1 225), only down.
INCREMENTS = {("_photo.css", "panorama"): 576, ("_journey-passage.css", "_linea-v2.css"): 1_225}
#: §7.2 ceilings of the section runtime and its modules (gzip -9 of the built files)
#: CLOSING (FINAL_DELIVERY_V2 §3.9 c; V5.20, a ratchet): the values below recorded at their measure on v524-closing — only down.
JS_CEILINGS = {"rise.js": 1_286, "indice": 1_536, "mappa": 1_536, "spia": 1_024, "racconto": 922}


def _read(path: Path) -> str:
    return path.read_bytes().decode("utf-8")


def _css(path: Path) -> str:
    return re.sub(r"/\*.*?\*/", "", _read(path), flags=re.S)


def _gz(data: bytes) -> int:
    return len(gzip.compress(data, 9))


#: The build's record of each budgeted text minified alone by esbuild (scripts/build_css.mjs, writeMeasures).
#: v524-cifix (V5.20 strict rule; FINAL_DELIVERY_V2 R4 — the budgets are gzip -9 of each partial minified alone): these
#: measures ran node_modules/esbuild in the test, and CI installs no Node — it must not rebuild dist (DL54-77) — so 14
#: budgets were red on every runner. The minified text is now part of the committed dist, held to the build by the
#: deterministic-build gate; each entry carries the SHA-256 of the exact text it minified, and a measure whose hash is
#: not the current source's fails here (a sheet edited without `npm run build:css`). Same figure, same ceilings, and one
#: more invariant than before: the committed dist is the build of these sources.
MEASURES = ROOT / "static" / "css" / "dist" / "measures.json"


def _measure(name: str, text: str) -> int:
    """gzip -9 of `text` minified alone, read from the build's record under `name` once its hash is `text`'s."""
    record = json.loads(MEASURES.read_bytes().decode("utf-8"))["measures"]
    assert name in record, f"{name}: not in static/css/dist/measures.json — run `npm run build:css`"
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    assert record[name]["sha256"] == digest, f"{name}: the record is not the current source's — run `npm run build:css`"
    return _gz(record[name]["minified"].encode("utf-8"))


def _minified_gz(path: Path) -> int:
    return _measure(path.relative_to(ROOT / "static").as_posix(), _read(path))


# ---------------------------------------------------------------------------------------------- the ILE marks


def test_the_thirteen_marks_have_one_source_one_partial_and_one_sprite_copy():
    marks = {mark.id for mark in icons.MARKS.values()}
    assert len(marks) == 13 and marks == set(icons.MARK)
    assert {p.stem for p in MARKS_SRC.glob("*.svg")} == marks
    assert {p.stem[1:] for p in PARTIALS.glob("_*.html")} == marks
    sprite = _read(ROOT / "static" / "img" / "icons-marks.svg")
    for mark in marks:
        assert f'<symbol id="icon-{mark}" viewBox="0 0 24 24">' in sprite, mark
        assert icons.SPRITE_OF[mark] == icons.SPRITE_MARKS
    assert len(sprite.encode()) <= icons.MARKS_SPRITE_MAX_BYTES == 16 * 1024
    assert all(mark.floor == 32 and mark.tier in ("T1", "T5") for mark in icons.MARKS.values())
    assert icons.MARKS["access"].tier == "T5", "the key is the identity"


def test_the_build_of_the_marks_is_current():
    result = subprocess.run(  # noqa: S603 — the repository's own build script
        [sys.executable, str(ROOT / "scripts" / "build_icons.py"), "--check"], capture_output=True, text=True, cwd=ROOT
    )
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize("mark", sorted(icons.MARK))
def test_a_mark_s_inline_drawing_draws_every_stroke_once_and_is_decorative(mark):
    html = _read(PARTIALS / f"_{mark}.html")
    svg = html.split("{% endcomment %}", 1)[1]
    assert 'aria-hidden="true"' in svg and 'focusable="false"' in svg and 'viewBox="0 0 48 48"' in svg
    shapes = re.findall(r"<(path|circle)\b([^>]*)/>", svg)
    assert shapes
    for _tag, attrs in shapes:
        if 'class="sg-t"' in attrs:
            assert "pathLength" not in attrs, "the tone is a fill, it fades in"
        else:
            assert 'pathLength="1"' in attrs, (mark, attrs)
    assert not re.search(r"#[0-9a-fA-F]{3,8}\b|style=", svg), "currentColor only"
    assert "<text" not in svg, "no letters (the glossary's «A» is drawn)"


def test_the_registry_of_the_v2_choices():
    assert len(icons.PILOT_STATION) == 8 and icons.PILOT_STATION[5] == "ile-arch"
    for group in (icons.PILOT_STATION, icons.COMPANY_MOMENT, icons.RECIPIENT_SEAT, icons.SHEET_STEP,
                  icons.DIPLOMA_STEP, icons.HOW_STEP, (icons.AUTHORITY_SEAT,)):
        assert set(group) <= set(icons.SYMBOLS), group
        assert "ile-steps" not in group, "the stair is the journey's"
    assert "users" not in icons.COMPANY_MOMENT + icons.RECIPIENT_SEAT, "users is the family pathway's"
    # O14: a sequence never draws a tick. The one check-bearing symbol a V2 sequence holds is the diplomas' seal
    # (`badge-check`, an authority's act, CHECK_BEARING); `list-checks` (two ticks) never stands on a station or step
    for group in (icons.PILOT_STATION, icons.COMPANY_MOMENT, icons.RECIPIENT_SEAT, icons.SHEET_STEP, icons.HOW_STEP,
                  (icons.AUTHORITY_SEAT,)):
        assert not set(group) & set(icons.CHECK_BEARING), (group, "never a check on a station")
    assert set(icons.DIPLOMA_STEP) & set(icons.CHECK_BEARING) == {"badge-check"}, "the seal alone"
    assert not set(icons.PILOT_STATION) & set(icons.PATHWAY.values()) - {"presentation"}, "never a pathway's twin"
    assert set(icons.FOLIO.values()) <= set(icons.MARK)
    assert "users" not in icons.FOLIO and "map-pin" not in icons.FOLIO and "award" not in icons.FOLIO
    assert "reserved-area" not in icons.CHAPTER and "space-links-title" not in icons.CHAPTER_OF, "the ile-key misuse ended"
    for group in icons.TWINS:
        for seq in (icons.PILOT_STATION, icons.RECIPIENT_SEAT, icons.DIPLOMA_STEP, icons.SHEET_STEP):
            assert len(set(seq) & group) <= 1, (seq, group)


def test_the_seal_partial_draws_a_registered_mark_or_nothing():
    def render(source: str) -> str:
        return Template(source).render(Context({}))

    seal = render('{% include "components/sezioni/sigillo.html" with mark="orientation" size="body" %}')
    assert 'data-mark="ile-orienta"' in seal and 'class="sigillo sigillo--body"' in seal and 'aria-hidden="true"' in seal
    assert 'class="sg-g sg-g--needle"' in seal, "the needle is its own moving part"
    assert render('{% include "components/sezioni/sigillo.html" with mark="nothing" %}').strip() == ""
    assert render('{{ "ile-scudo"|mark_of }}|{{ "protection"|mark_of }}|{{ "x"|mark_of }}') == "ile-scudo|ile-scudo|"
    assert render('{{ "factory"|folio_mark }}|{{ "map-pin"|folio_mark }}') == "ile-impresa|"


# ---------------------------------------------------------------------------------------------- the heads


@pytest.mark.django_db
def test_the_head_folios_draw_their_seal_or_stay_typographic(client, seeded, phase3_open, legal_published):
    seals = {"/fr/entreprises/": "ile-impresa", "/fr/institutions/": "ile-istituzione", "/ar/parcours/": "ile-percorso",
             "/fr/formation/": "ile-formazione", "/fr/attention-aux-fraudes/": "ile-scudo"}
    for path, mark in seals.items():
        html = client.get(path).content.decode()
        folio = html.split('class="ingresso__label"', 1)[1].split("</p>", 1)[0]
        assert f'data-mark="{mark}"' in folio and "fronte__glyph" not in folio, path
    for path in ("/fr/contact/", "/fr/reseau/"):
        folio = client.get(path).content.decode().split('class="ingresso__label"', 1)[1].split("</p>", 1)[0]
        assert "<svg" not in folio and "sigillo" not in folio, (path, "typographic")


def test_the_chapter_heads_draw_no_glyph_above_their_title():
    text = _read(ROOT / "templates" / "pages" / "partials" / "_chapter_head.html").split("{% endcomment %}", 1)[1]
    assert "chapter_mark" not in text and "svg_icon" not in text
    # the home's head keeps its concept marks until lane H recomposes the chapters (§9.7; H's test_home.py), naming
    # its class — the one way a mark still draws, since `{% chapter_mark %}` without a class draws nothing
    home = _read(ROOT / "templates" / "pages" / "partials" / "_section_header.html").split("{% endcomment %}", 1)[1]
    assert home.count("chapter_mark") == 2 and home.count('"icon chapter__mark"') == 2 and "svg_icon" not in home
    assert all("_section_header.html" not in p.read_text(encoding="utf-8")
               for p in (ROOT / "templates").rglob("*.html") if "home" not in p.parts), "the home's head alone"
    head = _read(ROOT / "templates" / "components" / "sezioni" / "_testa.html").split("{% endcomment %}", 1)[1]
    assert "svg_icon" not in head and "sigillo" not in head and "sticky" not in head


def test_the_login_key_is_a_t5_mark_in_ink():
    css = _css(ROOT / "apps" / "accounts" / "static" / "accounts" / "entrance.css")
    rule = re.search(r"\.varco__eyebrow \.varco__eyebrow-key \{([^}]*)\}", css).group(1)
    assert "inline-size: 20px" in rule and "block-size: 20px" in rule and "color: var(--text-1)" in rule
    assert "identity-key" not in rule


# ---------------------------------------------------------------------------------------------- the motion vocabulary


def test_every_v2_entrance_runs_on_the_trigger_with_fill_backwards_and_holds_only_under_no_preference():
    css = _css(V5 / "_reveal.css")
    v2 = css.split("V5.22", 1)[1] if "V5.22" in css else css
    for sheet in [v2] + [_css(p) for p in V5.glob("_sec-*.css")] + [_css(V5 / "_linea-v2.css")]:
        for match in re.finditer(r"([^{}]*)\{([^{}]*animation(?:-name)?:[^{}]*)\}", sheet):
            selector, body = match.group(1), match.group(2)
            if "data-sec-state=\"in\"" not in selector:
                continue
            assert ":root:not(.rm)" in selector and ':not([data-input="key"])' in selector, selector
            if re.search(r"animation:\s", body):
                assert "backwards" in body, (selector.strip(), body)
        for match in re.finditer(r"([^{}]*\[data-sec-state=\"wait\"\][^{}]*)\{", sheet):
            selector = match.group(1)
            assert ":root:not(.rm)" in selector and ':not([data-input="key"])' in selector, selector
            before = sheet[: match.start()]
            assert before.rfind("prefers-reduced-motion: no-preference") > before.rfind("@keyframes"), selector


def test_no_new_duration_or_curve_token():
    for path in [V5 / "_sezioni.css", V5 / "_sigillo.css", *V5.glob("_sec-*.css")]:
        css = _css(path)
        assert not re.search(r"--(?:motion|ease|spring)-[a-z-]+\s*:", css), path.name
    assert "--sez-slide: 8px" in _css(V5 / "_sezioni.css") and "--sez-drift: 24px" in _css(V5 / "_sezioni.css")


def test_the_m22_fix_and_the_m21_accent():
    css = _css(V5 / "_reveal.css")
    assert ":root:not(.rm) :is([data-parallax], .bande-foto__frame) :is(img, .foto__img) {" in css, "(0,4,0) > M2's (0,3,2)"
    assert ":root:not(.rm) :is([data-parallax], .bande-foto__frame) > picture { animation: none; }" in css
    spot = re.search(r"\.page-links__link\)::before \{([^}]*)\}", css).group(1)
    assert "--accent-mark" in spot and "--p-oro-300" not in spot
    door = re.search(r"\.porta::before \{([^}]*)\}", css).group(1)
    assert "--p-oro-300" in door, "oro only on the night door plate"


def test_the_section_runtime_writes_no_state_when_calm_and_loads_modules_on_demand():
    rise = _read(SRC_JS / "rise.js")
    assert 'section.dataset.secState = "wait"' in rise and 'section.dataset.secState = "in"' in rise
    assert "if (calm()) return;" in rise.split("export function initSections", 1)[1][:200]
    for name in ("indice", "mappa", "spia", "racconto"):
        assert f'{name}: () => import("./sezioni/{name}.js")' in rise
        assert not (SRC_JS / f"{name}.js").exists(), "a module is a split chunk, never an entry"
    # V5.30 Fast Visual Variety Correction §5, §7 ENTREPRISES (V5.20 strict rule): the measured curve left with its module
    assert "sezioni/flow.js" not in rise and not (SRC_JS / "sezioni" / "flow.js").exists()
    assert "addEventListener(\"scroll\"" not in rise and "requestAnimationFrame" not in rise
    for module in (SRC_JS / "sezioni").glob("*.js"):
        code = _read(module)
        assert "addEventListener(\"scroll\"" not in code and "requestAnimationFrame" not in code, module.name
        assert "prefers-reduced-motion" not in code, module.name


# ---------------------------------------------------------------------------------------------- gold and parity


GOLD = re.compile(r"--(?:p-oro-300|identity-light|identity-key|he-gold[a-z-]*)\b")
#: where gold may stand in the V2 sheets (§4.5): the night seat's light (the one gold of a T1), the boussole's north
#: tip and the passage's end call (a page's one arrival), the home pilot's seam
GOLD_ALLOWED = {
    "_sezioni.css": {"--p-oro-300"},
    "_sec-boussole.css": {"--identity-light"},
    "_linea-v2.css": {"--identity-light"},
    "_photo.css": {"--identity-light"},
}


def test_the_bodies_gold_budget():
    for path in [V5 / "_sezioni.css", V5 / "_sigillo.css", V5 / "_photo.css", V5 / "_linea-v2.css", *V5.glob("_sec-*.css")]:
        used = set(GOLD.findall(_css(path)))
        allowed = GOLD_ALLOWED.get(path.name, set())
        assert used <= allowed, (path.name, used - allowed)


def test_hover_equals_focus_in_the_v2_sheets():
    for path in [V5 / "_sezioni.css", *V5.glob("_sec-*.css")]:
        css = _css(path)
        for match in re.finditer(r"([^{}]+)\{", css):
            selector = match.group(1)
            if ":hover" not in selector or "@media" in selector:
                continue
            before = css[: match.start()]
            in_fine_pointer = before.rfind("(hover: hover)") > before.rfind("}\n}")
            pointer_only = "translate" in css[match.end(): css.find("}", match.end())] and in_fine_pointer
            assert pointer_only or re.search(r":focus-visible|:focus-within|\[aria-selected", selector), (path.name, selector.strip())


# ---------------------------------------------------------------------------------------------- budgets


@pytest.mark.parametrize("sheet", sorted(SHEET_CEILINGS))
def test_each_pattern_sheet_under_its_ceiling(sheet):
    assert _minified_gz(V5 / sheet) <= SHEET_CEILINGS[sheet], sheet


def test_every_pattern_sheet_has_a_ceiling_and_a_measure():
    """v524-cifix: the build records every `_sec-*.css` (scripts/build_css.mjs) and each one has its ceiling here — a new
    pattern sheet is never an unbudgeted one, and the record is never a stale list."""
    sheets = sorted(p.name for p in V5.glob("_sec-*.css"))
    assert sheets == sorted(SHEET_CEILINGS), sheets
    record = json.loads(MEASURES.read_bytes().decode("utf-8"))["measures"]
    assert sorted(name for name in record if name.startswith("css/v5/_sec-")) == [f"css/v5/{s}" for s in sheets]


def test_the_panorama_and_the_passage_v2_add_no_more_than_their_ceilings():
    photo = _read(V5 / "_photo.css")
    before = photo[: photo.rfind("/* ====", 0, photo.index("V5.22 (SECTION_SYSTEM_V2 §2 D"))]
    panorama = _measure("css/v5/_photo.css", photo) - _measure("css/v5/_photo.css before the panorama", before)
    assert panorama <= INCREMENTS[("_photo.css", "panorama")]
    passage = _read(V5 / "_journey-passage.css")
    assert "LA LINEA V2" not in passage, "the questionnaire's sheet imports the passage: V2 is its own partial"
    both = passage + _read(V5 / "_linea-v2.css")
    linea = _measure("css/v5/_journey-passage.css + css/v5/_linea-v2.css", both) - _measure(
        "css/v5/_journey-passage.css", passage
    )
    assert linea <= INCREMENTS[("_journey-passage.css", "_linea-v2.css")]


def test_the_section_runtime_and_its_modules_under_their_ceilings():
    assert _gz((DIST_JS / "rise.js").read_bytes()) <= JS_CEILINGS["rise.js"]
    chunks = list((DIST_JS / "chunks").glob("*.js"))
    assert not [c for c in chunks if c.name.startswith("flow-")], "V5.30 VARIETY §5: the curve's module left no chunk"
    for name in ("indice", "mappa", "spia", "racconto"):
        built = [c for c in chunks if c.name.startswith(f"{name}-")]
        assert len(built) == 1, (name, "one split chunk")
        assert _gz(built[0].read_bytes()) <= JS_CEILINGS[name], name
        assert built[0].name in _read(DIST_JS / "rise.js"), (name, "imported by rise.js only")


# ---------------------------------------------------------------------------------------------- round 1 (v522-s-improve1)


def test_the_flow_is_one_panel_with_no_measured_overlay():
    """F «il flusso». V5.30 Fast Visual Variety Correction §7 ENTREPRISES, «process panels» (V5.20 strict rule; this decision
    replaces «the measured flow draws its overlay in a wrapper»): no script draws over it; the list stands in its field,
    each moment a cell with the registry's company moment's glyph, the end call kept."""
    html = Template(
        '{% include "components/sezioni/flusso.html" with steps=steps end_action=action %}'
    ).render(Context({"steps": [{"glyph": g, "label": f"Temps {i}"} for i, g in enumerate(icons.COMPANY_MOMENT)],
                      "action": {"url": "#", "label": "Agir"}}))
    assert re.search(r'<div class="flusso__campo">\s*<ol class="flusso__tappe"', html), html[:400]
    assert "data-flow" not in html and "data-sec-js" not in html
    assert html.count('<li class="flusso__tappa">') == len(icons.COMPANY_MOMENT)
    assert html.count("flusso__nodo sez-tile") == len(icons.COMPANY_MOMENT) and "data-azione" in html


def test_a_french_run_beside_a_marker_hangs_from_its_edge_on_an_arabic_page():
    """§1 rule 6 and W3-F1's rule (QA_ROUND1 m5): a French run is its own LTR box; in a card, a panel or a tile whose
    numeral or node stands at the reading edge, its words end on that edge — one reading edge for the whole card."""
    css = _css(V5 / "_sezioni.css")
    assert re.search(r'\[dir="rtl"\] \.sez \[lang="fr"\]:not\(html\) \{[^}]*direction: ltr;[^}]*text-align: start;', css)
    rule = re.search(r'\[dir="rtl"\] \.sez :is\(([^)]*)\) \[lang="fr"\]:not\(html\),?[^{]*\{([^}]*)\}', css)
    assert rule and "text-align: end" in rule.group(2)
    assert {".tracciato__carta", ".flusso__lastra", ".mosaico__tessera"} <= {c.strip() for c in rule.group(1).split(",")}
    passage = _css(V5 / "_journey-passage.css")
    assert re.search(r'\[dir="rtl"\] \.linea :is\(\.linea__label, \.linea__text\)\[lang="fr"\] \{[^}]*text-align: end;', passage)
