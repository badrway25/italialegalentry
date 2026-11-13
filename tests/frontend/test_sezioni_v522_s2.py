"""
The section library's follow-up, on the sources (design V5.22, SECTION_SYSTEM_V2 §2, §4, §5.3; lane S's follow-up,
label v522-s2-build). The browser half is tests/frontend/test_sezioni_browser_v522_s2.py.

* the first keyboard input of a page (html[data-input] absent → «key», lane H's QA_ROUND3 M2): every rule of the
  library that reads the modality is filed under the library's own classes — never a universal subject (Blink then
  restyles the whole document), a rule ending on ::details-content (Blink cannot scope it), an SVG shape's tag (every
  path of the page) or the bare `.icon` (every icon of the page); the stroke verb has no tag-name branch;
* the red guards' product fixes, held on the sources: the hemicycle's own attribute in its contract, the register
  marker of the library's own, the route board's light twinned right to left;
* lane H's requests: the photo credit's space before the colon in French only; «la protezione»'s title carries its
  language; an index glyph never shrinks; the rows' ranks filed under the row's class.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from django.template import Context, Template
from django.utils import translation

ROOT = Path(__file__).resolve().parents[2]
V5 = ROOT / "static" / "css" / "v5"
SEZIONI = ROOT / "templates" / "components" / "sezioni"
#: the library's sheets (SECTION_SYSTEM_V2 §9.7, lane S): the shell, the seat, the photograph's partial, the passage V2,
#: the pattern sheets and the motion vocabulary
LIBRARY = sorted(
    [
        V5 / "_sezioni.css",
        V5 / "_sigillo.css",
        V5 / "_photo.css",
        V5 / "_linea-v2.css",
        V5 / "_reveal.css",
        *V5.glob("_sec-*.css"),
    ]
)
SHAPES = ("path", "circle", "line", "polyline", "polygon", "ellipse", "rect", "g", "svg", "use")


def _read(path: Path) -> str:
    return path.read_bytes().decode("utf-8")


def _rules(css: str) -> list[tuple[str, str]]:
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    return [
        (" ".join(s.split()), b)
        for s, b in re.findall(r"([^{}]+)\{([^{}]*)\}", css)
        if s.strip() and not s.strip().startswith("@")
    ]


def _parts(selector: str) -> list[str]:
    """The comma-separated selectors of a list, commas inside parentheses kept."""
    parts, depth, start = [], 0, 0
    for i, ch in enumerate(selector):
        depth += ch == "("
        depth -= ch == ")"
        if ch == "," and depth == 0:
            parts.append(selector[start:i].strip())
            start = i + 1
    return [*parts, selector[start:].strip()]


def _subject(selector: str) -> str:
    """The rightmost compound of a complex selector (after its last combinator outside parentheses)."""
    depth, last = 0, 0
    for i, ch in enumerate(selector):
        depth += ch == "("
        depth -= ch == ")"
        if depth == 0 and ch in " >+~":
            last = i + 1
    return selector[last:].strip()


@pytest.mark.parametrize("sheet", LIBRARY, ids=lambda p: p.name)
def test_the_modality_s_rules_are_filed_under_the_library_s_own_classes(sheet):
    """Lane H's QA_ROUND3 M2 (NOTES §12.3, §12.5 requests 1–2): the flip of html[data-input] restyles only what its rules
    name. A universal subject (`.mosaico *`) made Blink restyle the whole document; the stroke verb's tag-name branch
    every SVG shape; `.sez-tile .icon` every icon — they are gone, and none comes back."""
    found = []
    for selector, _body in _rules(_read(sheet)):
        for part in _parts(selector):
            if "data-input" not in part:
                continue
            subject = _subject(part)
            bare = re.sub(r"::[\w-]+(\([^)]*\))?$", "", subject)  # a pseudo-element hangs on its element's features
            featureless = re.sub(r":[\w-]+(?!\()", "", bare)  # an argument-less pseudo-class carries none
            if "::details-content" in subject or featureless.strip() in ("", "*") or featureless.startswith("*"):
                found.append(f"{part}: a subject Blink cannot scope")
            shapes = "|".join(SHAPES)
            if re.fullmatch(rf"(?:{shapes})", bare) or re.search(rf":is\([^)]*(?<![\w.#-])(?:{shapes})\b", bare):
                found.append(f"{part}: an SVG shape's tag — every shape of the page")
            if re.fullmatch(r"\.icon", bare) or re.search(r":is\([^)]*\.icon\b", bare):
                found.append(f"{part}: the bare icon class — every icon of the page")
    assert found == [], (sheet.name, found)


def test_the_stroke_verb_passes_its_draw_by_inheritance_never_by_a_tag_branch():
    """The dash properties are inherited: a carrier of the verb holds them and runs the draw, its shapes follow; the
    shapes the verb names itself draw as before (the home's drawings, the fixtures)."""
    css = re.sub(r"/\*.*?\*/", "", _read(V5 / "_reveal.css"), flags=re.S)
    assert (
        ':root:not(.rm):not([data-input="key"]) [data-sec-state="wait"] [data-verb~="stroke"] { stroke-dasharray: 1; stroke-dashoffset: 1; }'
        in css
    )
    assert (
        ':root:not(.rm):not([data-input="key"]) [data-sec-state="in"] [data-verb~="stroke"] { animation-name: sez-stroke;'
        in css
    )
    assert not re.search(r'\[data-verb~="stroke"\]\s+:is\(path', css), "no tag-name branch"


def test_the_tile_s_glyph_and_rule_read_their_tile_s_keyboard_duration():
    css = re.sub(r"/\*.*?\*/", "", _read(V5 / "_sezioni.css"), flags=re.S)
    assert re.search(
        r'html\[data-input="key"\] \.sez-tile,\s*html\[data-input="key"\] \.sez-disc,\s*html\[data-input="key"\] \.sg-g--key \{\s*--sez-t: 0s;',
        css,
    )
    # FINAL MICRO-PASS §2.1, §5 A3 (V5.20 strict rule: the tile's threshold rule left with its vault — its `scale`
    # transition with it): every transition that remains still reads the keyboard's duration, and no rule draws on a
    # tile any more
    for transition in (
        "translate var(--sez-t, var(--motion-standard))",
        "box-shadow var(--sez-t, var(--motion-standard))",
        "rotate var(--sez-t, var(--motion-emphasized))",
    ):
        assert transition in css, transition
    assert "scale var(--sez-t" not in css and ".sez-tile::after" not in css


def test_the_hemicycle_and_the_registers_carry_the_library_s_own_attributes():
    """DL54-182 item 10 b and c: the hemicycle's seats and its sentence's items pair through `data-seggio` (never Lume's
    L3 seat, reserved for the fragment containers loader.js seats); a register of named entities is marked
    `data-registro` (never the chip's `data-register`, which only the chip partial and two legends write).
    FINAL MICRO-PASS §6 B4 (V5.20; was «the seats and the items pair through data-seggio — twelve pairing selectors»):
    the arc's six seats left, so nothing is paired or lit — the sentence's items keep `data-seggio` (rendered by
    ecosystem.services.recipients_sentence, held by tests/frontend/test_pages_v522_p1.py), the arc draws no seat and no
    glyph, the sheet carries no pairing selector, and Lume's L3 `data-seat` is still written nowhere."""
    mappa = _read(SEZIONI / "mappa.html")
    arc = mappa.split('{% if layout == "arc" %}', 1)[1].split("{% else %}", 1)[0]
    assert "emiciclo__seggio" not in arc and "svg_icon" not in arc and "sez-disc" not in arc and "data-seat" not in mappa
    emiciclo = re.sub(r"/\*.*?\*/", "", _read(V5 / "_sec-emiciclo.css"), flags=re.S)
    assert "[data-seggio" not in emiciclo and "emiciclo__seggio" not in emiciclo and "data-seat" not in emiciclo
    for name in ("approdo", "filo", "flusso", "indice", "mappa", "mosaico", "tracciato"):
        source = _read(SEZIONI / f"{name}.html")
        assert "data-registro" in source and not re.search(r"\sdata-register[\s>{]", source), name
    assert "data-registro data-steps" in _read(ROOT / "templates" / "components" / "stepper.html")


def test_the_route_board_s_light_has_its_right_to_left_twin_and_run():
    css = re.sub(r"/\*.*?\*/", "", _read(V5 / "_sec-tracciato.css"), flags=re.S)
    assert '[dir="rtl"] .tracciato__linea::after { translate: 110% 0; }' in css
    assert (
        ':root[dir="rtl"]:not(.rm):not([data-input="key"]) .tracciato__linea::after { animation-name: sez-run-rtl; }'
        in css
    )
    assert re.search(r"@keyframes sez-run-rtl \{\s*from \{ translate: 110% 0; \}\s*to \{ translate: -360% 0; \}", css)


@pytest.mark.parametrize(
    ("lang", "separator"), [("fr", "Photo&nbsp;:"), ("it", "Foto:"), ("en", "Photo:"), ("ar", ":")]
)
def test_the_photo_credit_sets_its_space_before_the_colon_in_french_only(lang, separator):
    """Lane H's QA_ROUND3 m7 (an observation for S): «Foto : …» on an Italian page; the colon takes its (no-break)
    space in French only. V5.24 §2 (FINAL_DELIVERY_V2.md §3.2 D6; V5.20): the stock frame's credit no longer exists
    (components/photo.html draws no caption — asserted), so the rule is held on the markup that still prints a
    byline, the frontispiece's curated caption — and, since v524-px-improve (the reviewer's m2; V5.20, stronger), the
    news article's caption, the second byline lane PX owns; the rendered assertion is unchanged."""
    assert "figcaption" not in _read(ROOT / "templates" / "components" / "photo.html").split("{% endcomment %}", 1)[1]
    for template in ("pages/partials/_ingresso.html", "news/detail.html"):
        source = _read(ROOT / "templates" / template)
        assert '{% translate "Photo" %}{% if credit_lang == "fr" %}&nbsp;:{% else %}:{% endif %}' in source, template
        assert '{% translate "Photo" %} :' not in source, template
    with translation.override(lang):
        html = Template(
            '{% load i18n %}{% get_current_language as credit_lang %}{% translate "Photo" %}'
            '{% if credit_lang == "fr" %}&nbsp;:{% else %}:{% endif %} X'
        ).render(Context())
    assert html.endswith(f"{separator} X") and (lang == "fr") == ("&nbsp;" in html), (lang, html)


@pytest.mark.parametrize("lang", ["fr", "it", "en", "ar"])
def test_the_protection_s_title_carries_its_own_language(lang):
    """Lane H's QA_ROUND3 m5: a French title on another language's page is its own element's language (an h2 lang="fr",
    a left-to-right box on an Arabic page, base.css), never a French span inside a heading of the page's direction; its
    text stays the locked title, byte for byte."""
    from cms import locked_content

    with translation.override(lang):
        html = Template('{% include "components/sezioni/protezione.html" with url="#" %}').render(Context())
    title = re.search(r'<h2 class="protezione__titolo"[^>]*>(.*?)</h2>', html, flags=re.S)
    value, effective = locked_content.get("p3.antifraud.title", lang)
    assert title and title.group(1) == value, (lang, html[:400])
    assert (f'lang="{effective}"' in title.group(0)) == (effective != lang), (lang, title.group(0))
    assert "<span" not in title.group(1)


def test_an_index_glyph_never_shrinks_and_the_ranks_are_filed_under_the_row():
    # V5.29 (stream SYS; V5.20: the same invariant): «l'indice» is two sheets — the base (the list, the tabs, the phone's
    # disclosure) that the home bundles alone, and the whole index importing it; the rules are read across both
    css = re.sub(r"/\*.*?\*/", "", _read(V5 / "_sec-indice-base.css") + _read(V5 / "_sec-indice.css"), flags=re.S)
    assert re.search(r"\.indice__glifo \{\s*flex: none;\s*\}", css)
    assert ".indice__lista > :nth-child" not in css
    assert all(f".indice__riga:nth-child({n}) {{ --sez-i: {n - 1}; }}" in css for n in (2, 3, 4, 5))
