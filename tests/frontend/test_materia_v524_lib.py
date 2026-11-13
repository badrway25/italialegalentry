"""
The library's material, transitions, faces, verbs and type roles — V5.24, lane LIB (FINAL_DELIVERY_V2 §3.3, R3, R4 f;
BACKGROUND_MATERIAL_V2 §3.1, §3.2, §3.4, §3.5, §4.2; TYPOGRAPHY_V2 §6 and T's burn-down; V5.20's strict rule: every
assertion here is the audits' letter or stronger, cited). Static, offline, on the sources and the built dist:

* the six ground kinds (paper, stone, pietra, brand, night, photo) and the three material attributes (data-luce,
  data-sfuma, data-incastro) are painted by the shell (v5/_sezioni.css) and the material partial (v5/_materia.css)
  alone; the partial holds tokens and colour-mix of tokens only, logical properties only, no duration, curve or
  animation of its own (a fade is a ground, never a verb), its RTL twins, its forced-colours and print stills, and
  it is never imported by main.css;
* the raccordo, the velatura, the pietra grid, the light and the incastro are written as the audit decided (R3's
  rename: «il raccordo», never «varco» — the entrance's name);
* the protection's field, sill and bookend; the mosaico's tiles ink and its discs settle; the tile that inks lights
  its floor once; the head's label is the role by name;
* the type roles in the library's sheets: T's burn-down emptied for LIB's sheets but the two recorded residues of
  _fronte.css; the numeral role; the keyword and the term title at 600; no credit rule left (V5.24 §2);
* budgets: _materia.css ≤ 800 B gzip -9 minified alone; _sezioni.css at its measure (the shell is in every page sheet:
  the home's total, R4 a); the mosaico sheet at its measure with the light (R4 f); the niche face keeps the glyph
  ≥ 4.5:1 (12.9:1 measured) on the vault's darkest stop.

Improve round (label v524-lib-improve, the reviewer's gate QA.md B1–B6): the raccordo is the first child of the band
it ENTERS (every .sez isolates — hung under the leaving band it was painted over), the incastro drops its top padding,
the bookend stands down by a container query on the field, the light's home is the mosaico sheet, the linea's across
numeral keeps its 36 px row, and `_rule` reads a rule outside every at-rule block.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from django.template import Context, Template

from tests.frontend.test_sezioni_v522_s import _css, _minified_gz, _read
from tests.frontend.test_typography_v2 import measure
from tests.frontend.test_v5_tokens import _colour, _contrast

ROOT = Path(__file__).resolve().parents[2]
V5 = ROOT / "static" / "css" / "v5"
MATERIA = V5 / "_materia.css"
SEZIONI = V5 / "_sezioni.css"
STRATO = V5 / "_sec-strato.css"
#: V5.29 (stream SYS): the plates and «la protezione», split from the strato sheet, which imports it
LASTRE = V5 / "_sec-lastre.css"
MOSAICO = V5 / "_sec-mosaico.css"
SEZ_TPL = ROOT / "templates" / "components" / "sezioni"

pytestmark = pytest.mark.compliance

#: the six ground kinds (BACKGROUND_MATERIAL_V2 §3.1: one new kind — stone and pietra are one kind for adjacency)
GROUNDS = {"paper", "stone", "pietra", "brand", "night", "photo"}
MATERIAL_ATTRIBUTES = ("data-luce", "data-sfuma", "data-incastro")
#: the library's sheets (FINAL_DELIVERY_V2 §3.3 «Files owned»)
LIB_SHEETS = (
    "_materia.css", "_sezioni.css", "_sigillo.css", "_sec-boussole.css", "_sec-campata.css", "_sec-emiciclo.css",
    "_sec-filo.css", "_sec-flusso.css", "_sec-indice.css", "_sec-mappa.css", "_sec-mosaico.css", "_sec-passaggio.css",
    "_sec-racconto.css", "_sec-strato.css", "_sec-tracciato.css", "_sec-lastre.css", "_sec-indice-base.css", "_reveal.css", "_photo.css", "_journey-passage.css",
    "_linea-v2.css", "_servizio.css", "_fronte.css", "_compose.css", "_porta.css",
)
#: T's burn-down residue the Director's letter leaves in _fronte.css: the AGAMI name device's two clamps («.fronte__name
#: takes --track-display and nothing else», §3.3) and the folio label's uppercase, restated through the role's tokens
#: until pages/partials/_ingresso.html (lane PX's file) carries `t-label` (LIB NOTES §4 — a request to CLOSING)
FRONTE_RESIDUE = {"clamp": 2, "uppercase": 1}


def _sheets() -> list[Path]:
    found = [*V5.glob("**/*.css"), *(ROOT / "apps").glob("*/static/**/*.css")]
    return sorted(p for p in found if "dist" not in p.parts)


def _rules(css: str) -> list[tuple[str, str]]:
    """(selector, body) of every rule, the at-rules opened (their closing brace is left behind, harmlessly)."""
    css = re.sub(r"@(media|supports|container|layer)[^{]*\{", "", _css_text(css))
    return [(" ".join(sel.split()), body) for sel, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css) if sel.strip()]


def _css_text(path_or_text) -> str:
    return _css(path_or_text) if isinstance(path_or_text, Path) else re.sub(r"/\*.*?\*/", "", path_or_text, flags=re.S)


def _outside_at_rules(css: str) -> str:
    """The sheet without its at-rule blocks (@media, @supports, @container, @layer { … }), brace-matched — a phone, print
    or forced-colours override of a selector lives inside one and must not be mistaken for the rule itself."""
    out, i = [], 0
    while True:
        opened = re.search(r"@(media|supports|container|layer)[^{;]*\{", css[i:])
        if not opened:
            out.append(css[i:])
            return "".join(out)
        start, j, depth = i + opened.start(), i + opened.end() - 1, 0
        while j < len(css):
            if css[j] == "{":
                depth += 1
            elif css[j] == "}":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        out.append(css[i:start])
        i = j + 1


def _rule(path: Path, selector: str) -> str:
    """The body of the one rule with exactly this selector outside every at-rule block."""
    top = _outside_at_rules(_css_text(path))
    bodies = [body for sel, body in re.findall(r"([^{}]+)\{([^{}]*)\}", top) if " ".join(sel.split()) == selector]
    assert len(bodies) == 1, (path.name, selector, len(bodies))
    return bodies[0]


# ---------------------------------------------------------------------------------------------- the grounds' ownership


def test_the_six_ground_kinds_and_the_material_attributes_are_painted_by_the_shell_and_materia_only():
    """§4.2: the ground kinds and the three attributes are read only by _materia.css and the shell — here: every rule
    that PAINTS a ground (--sez-ground or a background on a [data-ground] subject) lives in one of the two sheets, every
    kind named anywhere is one of the six, and the three attributes appear in no other sheet."""
    kinds, painters, attribute_users = set(), set(), set()
    for sheet in _sheets():
        css = _css(sheet)
        kinds |= set(re.findall(r'data-ground="([a-z]+)"', css))
        for selector, body in _rules(sheet):
            if "[data-ground=" in selector and re.search(r"(?<![\w-])(--sez-ground|background(?:-image)?)\s*:", body):
                painters.add(sheet.name)
        if any(attr in css for attr in MATERIAL_ATTRIBUTES):
            attribute_users.add(sheet.name)
    assert kinds == GROUNDS, kinds ^ GROUNDS
    assert painters == {"_sezioni.css", "_materia.css"}, painters
    assert attribute_users == {"_materia.css"}, attribute_users


#: v524-pub2 (FINAL_DELIVERY_V2 §3.6, R4 a; V5.20 — the same invariant, «the material after the shell», on a route sheet
#: that stands UNDER a shared sheet's shell): Le projet's pages/css/projet.css imports the material without the shell,
#: because the page links the institutional pages' shared sheet (interior.css, which carries the shell) before it — the
#: rendered order is apps/pages/tests/test_interior_v522.py::test_a_route_sheet_sits_between_its_shared_sheet_and_the_frontispiece_s
ROUTE_SHEETS_UNDER_A_SHELL = {"projet.css": ROOT / "apps" / "pages" / "static" / "pages" / "css" / "interior.css"}


def test_materia_is_a_page_only_partial_never_in_main_css():
    main = _read(ROOT / "static" / "css" / "main.css")
    assert "_materia" not in main
    assert MATERIA.name.startswith("_"), "a partial, never a build entry"
    for sheet in _sheets():
        # the imports, never a comment naming the partial (v524-pub2: the sheets that explain where the material lives)
        if "_materia" in _css(sheet) and sheet != MATERIA:
            text = _css(sheet)
            if sheet.name in ROUTE_SHEETS_UNDER_A_SHELL:
                shell = _css(ROUTE_SHEETS_UNDER_A_SHELL[sheet.name])
                assert "_sezioni.css" in shell and "_materia.css" not in shell, (sheet.name, "the shell on the shared sheet")
                assert "_sezioni.css" not in text, (sheet.name, "the shell once, on the shared sheet")
                continue
            assert text.index("_sezioni.css") < text.index("_materia.css"), (sheet.name, "the material after the shell")


def test_materia_holds_tokens_and_colour_mixes_of_tokens_only_logical_properties_and_no_motion_of_its_own():
    css = _css(MATERIA)
    assert not re.search(r"#[0-9a-fA-F]{3,8}\b|\brgba?\(|\bhsla?\(|\boklch\(", css), "no literal colour"
    assert not re.search(r"(?<![\w-])(white|black|gray|grey|red|blue|green|yellow|orange|gold)\b(?![\w-])", css)
    for mix in re.findall(r"color-mix\(([^)]*)\)", css):
        assert "var(--" in mix, mix
    assert not re.search(r"--(?:motion|ease|spring)-[a-z-]+\s*:", css), "no new duration or curve token"
    assert not re.search(r"(?<![\w-])(animation|transition)(?:-[a-z]+)?\s*:", css), "a fade is a ground, never a verb"
    assert not re.search(r"(?<![\w-])(?:margin|padding|inset|border)-(?:left|right)\s*:|(?<![\w-])(?:left|right)\s*:", css)
    assert "CanvasText" in css and "(forced-colors: active), print" in css, "the forced-colours and print stills"


def test_the_rtl_twins_of_the_grid_and_the_light():
    css = _css(MATERIA)
    assert 'mask-image: linear-gradient(to left, var(--p-notte-950) 0%, transparent 62%)' in _rule(MATERIA, '.sez[data-ground="pietra"]::before')
    assert 'to right, var(--p-notte-950) 0%, transparent 62%' in _rule(MATERIA, '[dir="rtl"] .sez[data-ground="pietra"]::before')
    assert "at 0 0," in _rule(MATERIA, '.sez[data-ground="paper"][data-luce="origine"]')
    assert "at 100% 0," in _rule(MATERIA, '[dir="rtl"] .sez[data-ground="paper"][data-luce="origine"]')
    assert "translate" not in css, "the raccordo and the layers are placed by logical insets: nothing to mirror by hand"


# ---------------------------------------------------------------------------------------------- the recipes as decided


def test_pietra_is_dressed_stone_the_grid_on_the_far_side_fading_toward_the_plate():
    assert "--sez-ground: var(--surface-area)" in _rule(MATERIA, '.sez[data-ground="pietra"]')
    grid = _rule(MATERIA, '.sez[data-ground="pietra"]::before')
    assert "color-mix(in srgb, var(--line-rhythm) 70%, transparent)" in grid
    assert grid.count("48px 48px") == 2 and "1px, transparent 1px" in grid, "1 px every 48 px, both axes"
    assert "z-index: -1" in grid and "inset: 0" in grid


def test_carta_viva_is_one_radial_light_at_the_origin_corner_at_ten_percent():
    light = _rule(MATERIA, '.sez[data-ground="paper"][data-luce="origine"]')
    assert "radial-gradient(60% 50% at 0 0, color-mix(in srgb, var(--accent-mark) 10%, transparent), transparent 70%), var(--surface-page)" in light


def test_the_velatura_is_a_ground_at_the_foot_twelve_rem_eight_on_phones_in_the_next_ground_s_colour():
    layer = _rule(MATERIA, ".sez[data-sfuma]::after")
    assert "block-size: 12rem" in layer and "inset-block-end: 0" in layer and "z-index: -1" in layer
    assert "background: linear-gradient(transparent, var(--sez-next))" in layer
    nexts = {
        "stone": "var(--surface-area)", "paper": "var(--surface-page)", "brand": "var(--accent-wash)", "night": "var(--surface-night)",
    }
    for kind, token in nexts.items():
        assert f"--sez-next: {token}" in _rule(MATERIA, f'.sez[data-sfuma="{kind}"]'), kind
    css = _css(MATERIA)
    phone = re.search(r"@media \(max-width: 47\.999rem\) \{(.*?)\n\}", css, re.S).group(1)
    assert ".sez[data-sfuma]::after { block-size: 8rem; }" in phone


def test_the_raccordo_as_the_director_renamed_it():
    """R3: «il raccordo», .sez-raccordo, --sez-raccordo 48 px (32 on phones), data-verb="draw-y", the 6 px --accent-mark
    node, 2 px --line-structure on light / --accent-night entering night, z-index 1, drawn after the band's own line.
    The span is the first child of the band it ENTERS and runs from the seam down (`inset-block-start: 0`): every .sez
    isolates, so a line hung under the leaving band's foot was painted over by the next ground (the gate's B2, the
    reviewer's pixel proof: 0.00 dark as built, 0.50 with the line inside the entered band)."""
    css = _css(MATERIA)
    assert "varco" not in css.lower(), "the entrance's name stays the entrance's (static/css/v5/_varco.css)"
    line = _rule(MATERIA, ".sez-raccordo")
    assert "--sez-raccordo: clamp(var(--s-8), 4vw, var(--s-12))" in line  # 48 at 1440 (4vw = 57.6 → 48), 32 at 390 (15.6 → 32)
    assert "--sez-d: var(--motion-draw)" in line, "after the band's own line"
    assert "inset-block-start: 0" in line and "block-size: var(--sez-raccordo)" in line, "from the seam down, inside the entered band"
    assert "inset-block-end" not in line, "never hung under the leaving band (B2)"
    assert "inline-size: 2px" in line and "background: var(--line-structure)" in line and "z-index: 1" in line
    assert "inset-inline-start: var(--raccordo-x, 0)" in line, "the page places it on its route"
    node = _rule(MATERIA, ".sez-raccordo::after")
    assert "inline-size: 6px" in node and "block-size: 6px" in node and "background: var(--accent-mark)" in node
    assert "border-radius: var(--radius-full)" in node and "inset-block-end: -3px" in node, "centred on the line's end"
    assert "background: var(--accent-night)" in _rule(MATERIA, ".sez-raccordo--notte")
    assert "transform-origin: 0 100%" in _rule(MATERIA, ".sez-raccordo--risale[data-verb]"), "the rising line draws upward"
    assert "inset-block: calc(-1 * var(--sez-raccordo)) auto" in _rule(MATERIA, ".sez-raccordo--risale")
    # the verb is _reveal.css's draw-y: it already holds «wait» (scale 1 0) and «in» (sez-draw-y, --ease-sine, --motion-draw, backwards)
    reveal = _css(V5 / "_reveal.css")
    assert '[data-sec-state="wait"] [data-verb~="draw-y"] { scale: 1 0; }' in reveal
    assert 'animation-name: sez-draw-y; animation-timing-function: var(--ease-sine)' in reveal


def test_the_incastro_overlaps_the_band_above_by_sixty_four_pixels_and_paints_its_ground_from_there():
    band = _rule(MATERIA, ".sez[data-incastro]")
    assert "margin-block-start: calc(-1 * var(--s-16))" in band
    assert "padding-block-start: 0" in band, "the doors begin at the raised edge (B4: the band's own padding sank them under the seam)"
    assert "background: linear-gradient(transparent var(--s-16), var(--surface-area) 0)" in band
    assert "z-index: 1" in _rule(MATERIA, ".sez[data-incastro] > *") and "position: relative" in _rule(MATERIA, ".sez[data-incastro] > *")


def test_the_stills_under_forced_colours_and_in_print():
    css = _css(MATERIA)
    stills = re.search(r"@media \(forced-colors: active\), print \{(.*?)\n\}", css, re.S).group(1)
    assert '.sez[data-ground="pietra"]::before' in stills and ".sez[data-sfuma]::after" in stills and "display: none" in stills
    forced = re.search(r"@media \(forced-colors: active\) \{(.*?)\n\}", css, re.S).group(1)
    assert ".sez-raccordo::after { background: CanvasText; }" in forced.replace("\n  ", " ").replace(",\n", ",") or "CanvasText" in forced


# ---------------------------------------------------------------------------------------------- the shell: face, label, verbs


def test_the_tile_s_face_is_a_niche_and_keeps_the_glyph_legible():
    # FINAL MICRO-PASS §2.1, §5 A3 (V5.20 strict rule: the vault left — the owner's «not an architecture website»): the
    # glyph is drawn BARE — no face, no ring, no shadow, no threshold rule — in the text's own ink (as legible as the words
    # beside it), the large one in the accent's ink, which still holds 4.5:1 on the raised paper
    tile = _rule(SEZIONI, ".sez-tile")
    assert "background" not in tile and "box-shadow" not in tile and "border" not in tile
    assert "color: var(--tile-ink, currentColor)" in tile
    assert not re.search(r"\.sez-tile(?:--[a-z]+)?::(?:before|after)", _css(SEZIONI)), "no layer, no rule"
    assert "--tile-ink: var(--accent-text)" in _rule(SEZIONI, ".sez-tile--lg")
    assert _contrast(_colour("--accent-text"), _colour("--surface-raised")) >= 4.5


def _state_rules(path: Path) -> list[tuple[str, str]]:
    """(selector, body) of the rules inside the at-rule blocks too (the verb rules live under a media query)."""
    return _rules(path)


def test_a_tile_that_inks_lights_its_floor_once_on_the_trigger_and_the_shell_s_entrances_hold_the_v2_rules():
    """BACKGROUND_MATERIAL_V2 §3.4, §4.1: the tile's face light steps up once over --motion-standard, one step after its
    rule (--motion-slow + the sequence's stagger); the layer and its state rules live in the mosaico sheet as the audit
    placed them (the shell is in every page sheet — R4 a, the gate's B1), the tile's stacking context in the shell (m5);
    the state rules obey §5.1 (no-preference, :root:not(.rm), the keyboard excluded, fill backwards) — the same check
    lane S wrote for the pattern sheets, now over the shell, the material and the mosaico too."""
    # FINAL MICRO-PASS §2.1, §5 A3 (V5.20 strict rule: the tile's face and its floor light left with the vault): no
    # sheet of the library draws a layer on a tile any more — the shell's tile is no stacking context, the mosaico has
    # no floor light, nothing waits on one; the state rules that remain still obey §5.1 (below)
    assert "isolation" not in _rule(SEZIONI, ".sez-tile")
    for sheet in (SEZIONI, MOSAICO):
        assert not re.search(r"\.sez-tile(?:\[[^\]]*\])?::(?:before|after)", _css(sheet)), sheet.name
    for sheet in (SEZIONI, MATERIA, MOSAICO):
        text = _css(sheet)
        for match in re.finditer(r"([^{}]*)\{([^{}]*animation(?:-name)?:[^{}]*)\}", text):
            selector, body = match.group(1), match.group(2)
            if 'data-sec-state="in"' not in selector:
                continue
            assert ":root:not(.rm)" in selector and ':not([data-input="key"])' in selector, selector
            assert "backwards" in body, selector.strip()
        for match in re.finditer(r'([^{}]*\[data-sec-state="wait"\][^{}]*)\{', text):
            before = text[: match.start()]
            assert before.rfind("prefers-reduced-motion: no-preference") > before.rfind("@keyframes"), match.group(1)
    assert "sez-node" not in _css(MOSAICO), "no settle on a grid's tile"


def test_the_mosaico_s_tiles_ink_and_its_discs_settle():
    tpl = _read(SEZ_TPL / "mosaico.html").split("{% endcomment %}", 1)[1]
    assert """data-verb="{% if item.disc or variant == 'porte' %}node{% else %}ink{% endif %}\"""" in tpl
    grid = Template('{% include "components/sezioni/mosaico.html" with variant="grid" tiles=tiles %}').render(Context({
        "tiles": [{"href": "#", "title": "A", "glyph": "award", "lead": True}, {"href": "#", "title": "B", "glyph": "sprout"}]}))
    assert grid.count('data-verb="ink"') == 2 and 'data-verb="node"' not in grid
    assert grid.count('class="mosaico__soglia" data-verb="draw"') == 2, "the card's rule draws to its resting 40 %"
    doors = Template('{% include "components/sezioni/mosaico.html" with variant="porte" tiles=tiles %}').render(Context({
        "tiles": [{"href": "#", "title": "A", "glyph": "person", "audience": "person"}]}))
    assert 'data-verb="node"' in doors and 'data-verb="ink"' not in doors, "a door's disc keeps its settle"


def test_the_head_s_label_is_the_label_role_by_name_and_its_title_reads_the_steps():
    head = _read(SEZ_TPL / "_testa.html").split("{% endcomment %}", 1)[1]
    assert 'class="testa__label t-label"' in head
    label = _rule(SEZIONI, ".testa__label")
    assert "text-transform" not in label and "font-family" not in label, "the capitals and the face are the role's alone"
    assert "font-feature-settings" not in label, "the capitals' feature setting is the role's too (B1: the net is four lines)"
    assert "font-size: var(--t-label)" in label and "letter-spacing: var(--track-label)" in label, "the safety net reads the role's tokens"
    title = _rule(SEZIONI, ".testa__title")
    assert "font-size: var(--t-title-2)" in title and "line-height: var(--t-title-2-lh)" in title and "letter-spacing: var(--track-title-2)" in title
    small = _rule(SEZIONI, ".testa--process .testa__title, .testa--router .testa__title")
    assert "font-size: var(--t-band)" in small and "letter-spacing: var(--track-band)" in small
    assert not re.search(r":is\(:lang\(ar\), \[dir=\"rtl\"\]\) \.testa__title", _css(SEZIONI)), "no descendant-form Arabic rule"
    base = _css(V5 / "base.css")
    assert re.search(r"\.t-label, \.eyebrow \{[^}]*font-size: var\(--t-label\)", base), "the role lane T declared"


# ---------------------------------------------------------------------------------------------- the protection


def test_the_protection_is_one_compact_trust_band_and_keeps_its_text_whole():
    """V5.29 (owner, 6 Nov 2026: «protezione__campo too dominant … ONE global refined compact treatment … never dominates
    a page» — an explicit owner decision; stream SYS; V5.20: the invariants kept or made stronger — the locked text whole,
    visible, never collapsed, its seal once, its band's one field; V5.24's drawing table (the sill to the container's
    edge, the far shield) left with the size it gave the band): the seal at the reading edge beside the label-role
    title and the body in the legal ink, two columns from 80 rem, the call at the far end, a plain plate.
    RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026 (the
    senior review's P2-5: the warning's third sentence broke between the columns): the columns start at 80 rem, where
    each one holds a sentence whole, and every sentence after the lead is now kept whole - a stronger invariant."""
    html = Template('{% include "components/sezioni/protezione.html" with url="#" %}').render(Context({}))
    assert html.count("protezione__campo") == 1 and html.strip().endswith("</div>")
    assert html.index('class="protezione__campo"') < html.index("<aside")
    # FINAL MICRO-PASS §5 A3 (V5.20 strict rule): the shield is drawn bare — no seal's seat, so no seal's scope
    assert 'data-callout="antifraud"' in html and "data-sigillo-scope" not in html and 'data-locked="p3.antifraud.body"' in html
    assert "<details" not in html and " hidden" not in html, "legally required: always visible, never collapsed"
    assert "protezione__davanzale" not in html and "sez-fondale" not in html and "sez-plate--raised" not in html
    assert 'class="sigillo' not in html and html.count("#icon-ile-scudo") == 1, "the shield, once, bare"
    assert '@import url("_sec-lastre.css");' in _read(STRATO), "every importer of the strato sheet keeps the band"
    css = _css(LASTRE)
    assert "@container" not in css and "davanzale" not in css and "sez-fondale" not in css
    plate = _rule(LASTRE, ".protezione")
    assert "display: grid" in plate and re.search(r"@media \(min-width: 48rem\) \{\s*\.protezione \{\s*grid-template-columns: auto minmax\(0, 1fr\);", css)
    assert "max-inline-size" not in plate and "margin-block-start" not in plate, "the band spans its field, no stand"
    assert "color-mix(in srgb, var(--accent-wash) 30%, var(--surface-raised))" in plate, "a restrained tint"
    title = _rule(LASTRE, ".protezione__titolo")
    assert "font-size: var(--t-label)" in title and "font-weight: var(--w-label)" in title and "color: var(--text-legal)" in title
    body = _rule(LASTRE, ".protezione__testo")
    assert "font-size: var(--t-small)" in body and "color: var(--text-legal)" in body
    assert re.search(r"@media \(min-width: 80rem\) \{[^@]*\.protezione__testo \{\s*columns: 2;", css), "two columns on a desktop"
    assert re.search(r"\.protezione__testo \.ls-1 \{\s*column-span: all;", css), "the first sentence across both"
    two = css[css.index("@media (min-width: 80rem)"):]
    assert re.search(r"\.protezione__testo \.ls-2 \{\s*display: block;\s*column-span: all;", two), "the rule across both"
    assert re.search(r"\.protezione__testo :is\(\.ls-3, \.ls-4\) \{[^}]*break-inside: avoid;", two), "each one whole"
    assert not re.search(r"(?<![\w-])columns:", css[: css.index("@media (min-width: 80rem)")]), "no narrower columns"
    seal = _rule(LASTRE, ".protezione__sigillo")
    assert "--sg-w" not in seal and "position" not in seal and "color: var(--text-1)" in seal, "bare, in the band's flow"
    assert "inline-size: 1.5rem" in _rule(LASTRE, ".protezione__sigillo .icon"), "a glyph's size, never a seat's"
    assert "padding-block: clamp(var(--s-8), 4vw, var(--s-12))" in _rule(LASTRE, ".sez:has(> .container > .protezione__campo:only-child)")


# ---------------------------------------------------------------------------------------------- the type roles in the library


def test_t_s_burn_down_is_emptied_for_the_library_s_sheets_but_the_two_recorded_residues():
    """FINAL_DELIVERY_V2 §3.3 gate 4; TYPOGRAPHY_V2 §6: no clamp, literal, mono seat, descendant-form Arabic rule or
    stray uppercase in LIB's sheets — except _fronte.css's name device (two clamps, R3.3) and its folio label's uppercase
    (until _ingresso.html carries `t-label`)."""
    for name in LIB_SHEETS:
        counts = {k: v for k, v in measure(V5 / name).items() if v}
        assert counts == (FRONTE_RESIDUE if name == "_fronte.css" else {}), (name, counts)
    fronte = _css(V5 / "_fronte.css")
    assert "letter-spacing: var(--track-display)" in _rule(V5 / "_fronte.css", ".fronte__name")
    assert "font-weight: 700" in _rule(V5 / "_fronte.css", ".fronte__name"), "«and nothing else»"
    assert fronte.count("font-size: clamp(") == 2, "the name device's two (a padding's clamp is not a type size)"
    label = _rule(V5 / "_fronte.css", "[data-fronte] .ingresso__label")
    assert "font-size: var(--t-label)" in label and "font-weight: var(--w-label)" in label and "letter-spacing: var(--track-label)" in label
    assert "text-transform: none" in _rule(V5 / "_fronte.css", "[data-fronte] .ingresso__label:lang(ar)")
    assert "Vazirmatn" not in fronte


def test_the_numerals_are_the_sans_at_600_tabular_and_the_keyword_and_the_term_title_at_their_weights():
    numeral = _rule(SEZIONI, ".sez-numeral")
    assert "font-family: var(--f-sans)" in numeral and "font-size: var(--t-numeral-lg)" in numeral
    assert "line-height: var(--t-numeral-lg-lh)" in numeral and "font-weight: var(--w-title)" in numeral and "var(--numeric-data)" in numeral
    # FINAL MICRO-PASS §5 A2 (V5.20 strict rule: the display numerals gave way to the quiet sequence marker, 21st.dev
    # 26891): every sequence marker of the library — the board's station, the large line's, the filo's — is a small
    # figure in the quiet ink (--t-small, --text-3, the sans inherited), never the numeral role
    assert '<span class="tracciato__num" aria-hidden="true">' in _read(SEZ_TPL / "tracciato.html")
    station = _rule(V5 / "_sec-tracciato.css", ".tracciato__num")
    assert "font-family" not in station and "font-size: var(--t-small)" in station and "color: var(--text-3)" in station
    down = _rule(V5 / "_linea-v2.css", ".linea--large .linea__num::before")
    assert "font-size: var(--t-small)" in down and "color: var(--text-3)" in down and "font-family" not in down
    for name in ("_linea-v2.css", "_sec-filo.css"):
        assert "var(--t-numeral" not in _css(V5 / name), name
    assert "font-size: var(--t-small)" in _rule(V5 / "_sec-filo.css", ".filo__num")
    # FINAL MICRO-PASS §5 A3/A4 (V5.20 strict rule): the keyword at the floor weight on its step; «Non.» lighter — the
    # entry step at the floor weight
    keyword = _rule(SEZIONI, ".sez-keyword")
    assert "font-weight: var(--w-body)" in keyword and "font-size: var(--t-title-2)" in keyword
    parola = _rule(LASTRE, ".strato__corpo--parola .ls-1")
    assert "font-weight: var(--w-body)" in parola and "font-size: var(--t-entry)" in parola
    scheda = _rule(STRATO, ".strato__lastra--scheda .strato__titolo")
    assert "font-weight: var(--w-display)" in scheda and "letter-spacing: var(--track-display)" in scheda
    servizio = _css(V5 / "_servizio.css")
    assert "var(--f-mono)" not in servizio and "--ar-title-lh" not in servizio and "--track-folio" not in servizio


def test_no_credit_rule_is_left_in_the_library_s_sheets():
    """V5.24 §2, IMAGERY_ATTRIBUTION D1–D8 (lane PX took the figcaption; each sheet's owner its rules): the five partials
    the Director named and every other sheet of static/css/v5."""
    for sheet in V5.glob("*.css"):
        assert "foto__credit" not in _read(sheet), sheet.name


# ---------------------------------------------------------------------------------------------- budgets


def test_materia_under_its_ceiling_and_the_shell_within_its_audited_increment():
    # v524-cifix (V5.20; FINAL_DELIVERY_V2 R4): the minified-alone figures are read from the build's record in the
    # committed dist (static/css/dist/measures.json, hash-checked against the source) — CI has no Node; same ceilings
    assert _minified_gz(MATERIA) <= 800, "R4 f / §3.3: ≤ 800 B gzip -9 per importing sheet (788 measured)"
    # the shell: 2 444 B on 554c82d2; + the niche face (audited ≈ 45) + the label's safety net (four lines) − the mono folio
    # and the clamps: 2 382 measured (the light's home is the mosaico sheet — B1: the shell is in every page sheet and the
    # home's total is the §7.1 letter, R4 a); never up
    assert _minified_gz(SEZIONI) <= 2_382
    # the mosaico sheet: 1 203 + the light (152 B here, the audited «≈ 120» an estimate): 1 355 measured, R4 f; never up —
    # lane S's SHEET_CEILINGS carries the same figure
    assert _minified_gz(MOSAICO) <= 1_355
