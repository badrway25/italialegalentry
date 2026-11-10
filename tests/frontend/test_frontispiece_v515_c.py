"""
V5.15 W3, lane C (label v515-c-build): the frontispiece, the imagery pass, the section compositions, and the two
carry-overs of the W2 review (M-2 the unpublished legal pages, M-3 the photograph's motion contract).

Behaviour only — presentation is judged in headed Chromium (NOTES.md). The guards:
  * every important public page opens with the frontispiece band: one h1, the page's motif (decorative, hidden from
    assistive technology), its page-only sheet linked before the band; main.css carries none of it;
  * the motion of the band is drawn only under no-preference and never on html.rm (the still is the reduced state);
  * each page's new frame is drawn once, one LCP image per page, every body frame lazy and masked (lane A's M2), the
    black-and-white frames on lane A's data-grade, never an own scroll mechanism;
  * an unpublished legal page (C/D) answers 404 outside the preview and nothing links it.
"""

from __future__ import annotations

import gzip
import re
from pathlib import Path

import pytest
from django.conf import settings
from django.test import override_settings

from pages import imagery

ROOT = Path(settings.BASE_DIR)
FRONTE = ROOT / "static" / "css" / "v5" / "_fronte.css"
COMPOSE = ROOT / "static" / "css" / "v5" / "_compose.css"

#: page → (motif, tone, the frame it draws in its band — or "" for a type-led head)
PAGES = {
    "/fr/parcours/": ("route", "", "pathways.hero"),
    "/fr/entreprises/": ("economic", "", "companies.hero"),
    "/fr/institutions/": ("civic", "", "institutions.hero"),
    "/fr/universites-et-formation/": ("learning", "", "universities.hero"),
    "/fr/projet-pilote/": ("mission", "night", "pilot.plain"),
    "/fr/le-projet/": ("mission", "night", "project.hall"),
    "/fr/reseau/": ("network", "night", "network.table"),
    "/fr/contact/": ("contact", "", "contact.square"),
    "/fr/formation/": ("learning", "", "training.hero"),
    "/fr/diplomes-et-titres/": ("learning", "", "diplomas.hero"),
    "/fr/agami/": ("civic", "", ""),
    "/fr/attention-aux-fraudes/": ("legal", "", ""),
}
#: the reading pages: their page header inside the band
WRAPPED = {"/fr/faq/": "route", "/fr/glossaire/": "learning", "/fr/vivre-en-italie/": "territory"}
#: body frames drawn by the section compositions: page → slot
BODY = {
    "/fr/institutions/": "institutions.chamber",
    "/fr/entreprises/": "companies.territory",
    "/fr/formation/": "training.after",
}


def _main(html: str) -> str:
    return html.split('<main id="main-content"', 1)[1].split("</main>", 1)[0]


@pytest.fixture
def get(client, seeded, phase3_open, legal_published):
    def fetch(path: str) -> str:
        response = client.get(path)
        assert response.status_code == 200, (path, response.status_code)
        return response.content.decode("utf-8")

    return fetch


@pytest.mark.django_db
@pytest.mark.parametrize("path", list(PAGES))
def test_every_important_page_opens_with_its_frontispiece(get, path):
    motif, tone, slot = PAGES[path]
    html = get(path)
    main = _main(html)
    head = re.search(r'<header class="ingresso"([^>]*)>(.*?)</header>', main, flags=re.S)
    assert head, path
    attrs, body = head.group(1), head.group(2)
    assert f'data-fronte="{motif}"' in attrs, (path, attrs)
    assert (f'data-tone="{tone}"' in attrs) if tone else ("data-tone" not in attrs), (path, attrs)
    # FINAL MICRO-PASS §2.6, §5 A3 (V5.20 strict rule: the page-header motifs off — the band is its paper or night, its
    # light and its grain): the ground is decoration, hidden, and draws nothing
    assert '<div class="fronte__ground" aria-hidden="true"></div>' in body, path
    assert "fronte__motif" not in body, path
    # its sheet is linked in the <head> (round 1: a link in the body blocked the band's paint and pushed the LCP)
    assert "css/dist/pages/css/fronte.css" in html.split("</head>", 1)[0], path
    assert "css/dist/pages/css/fronte.css" not in main, path
    assert main.count("<h1") == 1, path
    if slot:
        assert f'data-slot="{slot}"' in body, (path, slot)


@pytest.mark.django_db
@pytest.mark.parametrize("path", list(WRAPPED))
def test_the_reading_pages_head_stands_on_the_band(get, path):
    html = get(path)
    assert "css/dist/pages/css/fronte.css" in html.split("</head>", 1)[0], path
    main = _main(html)
    assert f'<div class="fronte-wrap" data-fronte="{WRAPPED[path]}">' in main, path
    wrap = main.split('<div class="fronte-wrap"', 1)[1]
    assert wrap.index('aria-hidden="true"') < wrap.index("<h1"), path
    assert main.count("<h1") == 1, path


@pytest.mark.django_db
@pytest.mark.parametrize("path", [*PAGES, *WRAPPED])
def test_one_lcp_image_at_most_and_every_body_frame_lazy_and_masked(get, path):
    main = _main(get(path))
    assert main.count('fetchpriority="high"') <= 1, path
    for fig in re.findall(r'<figure class="foto[^"]*"[^>]*>.*?</figure>', main, flags=re.S):
        opening = fig.split(">", 1)[0]
        role = imagery.BY_KEY[re.search(r'data-slot="([^"]+)"', opening).group(1)].role if "data-slot" in opening else ""
        if 'fetchpriority="high"' in fig:
            assert "data-reveal" not in opening, (path, "the LCP frame is never masked")
        elif role == "head":
            # a head's second frame (round 1): eager, never masked, without fetchpriority
            assert "data-reveal" not in opening and 'loading="lazy"' not in fig, (path, opening)
        else:
            assert 'loading="lazy"' in fig and 'data-reveal="mask"' in opening, (path, opening)
        assert "<picture>" in fig and fig.index("<img") > fig.index("<picture>"), "the img stays inside the picture"
        assert "foto--develop" not in opening, "one B/W mechanism: lane A's data-grade"


@pytest.mark.django_db
@pytest.mark.parametrize("path, slot", list(BODY.items()))
def test_the_section_compositions_draw_their_frame(get, path, slot):
    main = _main(get(path))
    fig = re.search(rf'<figure [^>]*data-slot="{re.escape(slot)}"[^>]*>', main)
    assert fig, (path, slot)
    grade = imagery.BY_KEY[slot].treatment
    if grade == "develop":
        assert 'data-grade="bw-scroll"' in fig.group(0)
    elif grade == "bw":
        assert 'data-grade="bw"' in fig.group(0)
    else:
        assert "data-grade" not in fig.group(0)


@pytest.mark.django_db
def test_the_pilot_band_is_a_diptych_with_one_lcp(get):
    main = _main(get("/fr/projet-pilote/"))
    pair = main.split('class="ingresso__aside ingresso__pair"', 1)[1].split("</div>", 1)[0]
    assert pair.count("<figure") == 2 and pair.count('fetchpriority="high"') == 1
    assert pair.index('data-slot="pilot.plain"') < pair.index('data-slot="pilot.fields"')
    # round 1: the head is never masked — the second half is eager, unmasked, without fetchpriority
    assert "data-reveal" not in pair and 'loading="lazy"' not in pair


@pytest.mark.django_db
def test_the_arabic_band_keeps_its_drawing_and_its_one_h1(client, seeded, phase3_open, legal_published):
    html = client.get("/ar/institutions/").content.decode("utf-8")
    assert 'dir="rtl"' in html and 'data-fronte="civic"' in html
    assert _main(html).count("<h1") == 1


def test_the_band_moves_only_under_no_preference_and_never_on_html_rm():
    css = re.sub(r"/\*.*?\*/", "", FRONTE.read_text(encoding="utf-8"), flags=re.S)
    animated = [m.start() for m in re.finditer(r"\banimation\s*:", css)]
    assert animated
    blocks = [m.span() for m in re.finditer(r"@media \(prefers-reduced-motion: no-preference\) \{", css)]
    for at in animated:
        assert any(start < at for start, _end in blocks), "an animation outside no-preference"
        rule_head = css[:at].rsplit("{", 1)[0].rsplit("}", 1)[-1]
        assert ":root:not(.rm)" in rule_head, rule_head.strip()
    # FINAL MICRO-PASS §2.6, §5 A3 (V5.20 strict rule): no head draws its motif any more — a drawing a reading page
    # still includes stands down, so there is nothing to mirror —; nothing mirrors a photograph
    assert re.search(r"(?m)^\.fronte__motif \{\s*display: none;\s*\}", css)
    assert '[dir="rtl"] .fronte__motif' not in css
    assert not re.search(r"\.foto[^{]*\{[^}]*scaleX\(-1\)", css)


def test_the_compositions_move_only_under_no_preference():
    css = re.sub(r"/\*.*?\*/", "", COMPOSE.read_text(encoding="utf-8"), flags=re.S)
    for m in re.finditer(r"\btranslate:\s*0 -2px", css):
        assert ":root:not(.rm)" in css[: m.start()].rsplit("{", 1)[0].rsplit("}", 1)[-1]


def test_the_head_photographs_draw_one_print():
    """V5.20 (the test-change audit's V8): the head photograph's drop under its print is ONE value, --fronte-print, at
    the value lane C drew (DL54-172) — the entrance's photograph and the plan's read it instead of two literal copies;
    tests/frontend/test_orientation_browser_w3_f1.py pins the photograph at rest to the token."""
    css = re.sub(r"/\*.*?\*/", "", FRONTE.read_text(encoding="utf-8"), flags=re.S)
    assert re.search(r"--fronte-print:\s*([^;]+);", css).group(1) == (
        "0 2px 4px color-mix(in srgb, var(--p-notte-950) 6%, transparent), "
        "0 28px 56px -24px color-mix(in srgb, var(--p-notte-950) 42%, transparent)"
    )
    assert css.count("box-shadow: var(--fronte-print);") == 2
    assert "6%, transparent), 0 28px 56px -24px" not in css.split("--fronte-print:", 1)[1].split(";", 1)[1]


#: V5.22 (SECTION_SYSTEM_V2 §7.1 — «new section CSS goes into page-only sheets / route-specific bundles with their own
#: recorded budgets», the owner's V5.22 standing constraint; lane S): each page-only sheet its own ceiling (gzip -9),
#: ratcheted to the measure by S-close. The blanket 6 KB of V5.15 W3 for four sheets becomes these ceilings plus the
#: per-page totals below — page-only, each sheet capped, each page capped (V5.20 strict rule: a stronger invariant).
#: CLOSING (FINAL_DELIVERY_V2 §3.9 c; V5.20, a ratchet): the values below recorded at their measure on v524-closing — only down.
SHEETS = {
    "core/reveal.css": 3_526,
    "core/portico.css": 2_989,
    "pages/css/fronte.css": 5_995,
    "pages/css/hero.css": 10_849,
    # V5.30 §7 (the owner's «Italy + Morocco: stronger presence … a homepage cooperation / pilot moment … Réseau»; stream A;
    # V5.20 — re-recorded at the measure, NOTES docs/design-v5/QA/v530/art/NOTES.md §6 «ceilings re-recorded»): the
    # primitive «l'intesa» (v5/_intesa.css + _intesa-atmosfera.css) enters the home's sheet and Réseau's route sheet; paid
    # first with what the change made dead — the ecosystem's arch, its sill's light and its connector, the portico's
    # drawing, the closing band's bookend — the rest is the feature the owner asked for: 11 239 → 11 626, 1 761 → 2 384
    "pages/css/pages.css": 11_626,
    "pages/css/interior.css": 7_842,
    "ecosystem/ecosystem.css": 4_719,
    "pathways/pathways.css": 4_423,
    "cms/lettura.css": 6_543,
    "forum/forum.css": 7_849,
    "core/glyph.css": 1_571,
    # V5.22 lane P2 round 2 (QA_ROUND2 m5; the owner's V5.22 «route-specific bundles with their own recorded budgets»;
    # strict rule V5.20 — new sheets, new ceilings): a page's own compositions in a route sheet of its own
    # V5.29 §10–§13 (the owner's FAQ redesign, an explicit decision; V5.20 — re-recorded at the measure, lane PUB2, NOTES
    # «ceilings re-recorded»: 2 048 → 2 207; nothing in the sheet was dead to pay for the glyph tiles' states and the
    # empty search — every rule is named by faq/index.html or the library's indice.html)
    "cms/faq.css": 2_207,
    "cms/lessico.css": 2_351,
    "pages/css/rete.css": 2_384,
    # V5.30 §7–§8 (the owner's final art direction, an explicit decision; V5.20 — re-recorded at the measure, lane v530-agami,
    # NOTES «ceilings re-recorded»: 1 778 → 2 015; the v530-art merge: 2 015 → 2 166, the one primitive v5/_intesa.css
    # replacing ecosystem/_intesa.css): the page's Italy + Morocco ground joined the sheet; the retired colonnade, its light
    # and sill and the corner brackets (v5/_squadre.css) paid about 470 B of it
    "pages/css/agami.css": 2_166,
    "pages/css/frodi.css": 1_199,
}
#: every sheet a page links on a desktop (the portico's included), summed: page type → (a page of the type, ceiling)
#: CLOSING (FINAL_DELIVERY_V2 §3.9 c; V5.20, a ratchet): the values below recorded at their measure on v524-closing — only down.
PAGE_TOTALS = {
    # V5.30 §7 (stream A; V5.20, re-recorded at the measure — NOTES «ceilings re-recorded»): the Italy + Morocco
    # primitive on the home's cooperation moment and under Réseau's closing band (60 708 → 61 074, 54 218 → 54 553); every
    # other page type fell 70–300 B with the head's grid, offset frame and the bookend gone
    "home": ("/fr/", 61_074),
    "landing (ecosystem)": ("/fr/entreprises/", 53_095),
    "interior (pages)": ("/fr/contact/", 52_457),
    "pathways": ("/fr/parcours/", 55_067),
    "reading": ("/fr/faq/", 53_365),
    "forum": ("/fr/forum/", 46_469),
    # V5.22 lane P2 round 2 (QA_ROUND2 m5): with route sheets the pages of a type no longer link the same sheets — each
    # route held to its type's total
    "reading (glossary)": ("/fr/glossaire/", 53_509),
    "reading (term)": ("/fr/glossaire/nulla_osta/", 53_509),
    "reading (living)": ("/fr/vivre-en-italie/", 53_509),
    "interior (network)": ("/fr/reseau/", 54_553),
    # V5.30 §8 (V5.20, re-recorded at the measure with its route sheet above: 54 235 → 54 472)
    "interior (promoter)": ("/fr/agami/", 54_472),
    "interior (fraud)": ("/fr/attention-aux-fraudes/", 53_656),
}
FORM_SHEETS = {"css/dist/core/forms.css", "css/dist/core/steps.css", "css/dist/core/glyph.css"}
STYLESHEET = re.compile(r'<link rel="stylesheet" href="/static/(css/dist/[^"?]+\.css)[^"]*"')


def _gz(relative: str) -> int:
    return len(gzip.compress((ROOT / "static" / relative).read_bytes(), 9))


def test_the_new_sheets_are_page_only_and_inside_their_own_budgets():
    main = (ROOT / "static" / "css" / "main.css").read_text(encoding="utf-8")
    assert "_fronte.css" not in main and "_compose.css" not in main
    for partial in ("_sezioni.css", "_sigillo.css", "_sec-"):
        assert partial not in main, f"{partial}: a V2 sheet is page-only, never in main.css"
    assert _gz("css/dist/main.css") <= 32_105, "main.css never rises above 32 105 B (the V5.20 ratchet, recorded at the measure by CLOSING, FINAL_DELIVERY_V2 §3.9 c)"
    for sheet, ceiling in SHEETS.items():
        assert _gz(f"css/dist/{sheet}") <= ceiling, (sheet, _gz(f"css/dist/{sheet}"), ceiling)


@pytest.mark.django_db
@pytest.mark.parametrize("kind", list(PAGE_TOTALS))
def test_each_page_type_stays_inside_its_total(get, kind):
    path, ceiling = PAGE_TOTALS[kind]
    sheets = sorted(set(STYLESHEET.findall(get(path))))
    assert "css/dist/main.css" in sheets, (path, sheets)
    # the premium forms' own sheets (preserved, V5.22 §9.8; their budgets are tests/frontend/test_forms_v515_b.py's)
    # are the form's, not the composition's: a page that holds a form adds them on top of its type's total
    total = sum(_gz(sheet) for sheet in sheets if sheet not in FORM_SHEETS)
    assert total <= ceiling, (kind, path, total, ceiling, sheets)


# ---- the W2 review's M-2: an unpublished legal page is never shown to the public ------------------------------------
@pytest.mark.django_db
@pytest.mark.parametrize("path", ["/fr/note-legali/", "/fr/condizioni-di-utilizzo/", "/fr/avvertenze/"])
def test_an_unpublished_legal_page_answers_404_outside_the_preview(client, seeded, path):
    from legal import services
    from legal.models import LegalDocument

    kind = {"note-legali": "notices", "condizioni-di-utilizzo": "terms", "avvertenze": "disclaimer"}[path.split("/")[2]]
    services.invalidate()
    with override_settings(ILE_LEGAL_OPEN_FIELDS_ALLOWED=False):
        doc = LegalDocument.objects.filter(kind=kind).first()
        if doc is not None and doc.is_available:
            pytest.skip("this database publishes the document")
        assert client.get(path).status_code == 404
    with override_settings(ILE_LEGAL_OPEN_FIELDS_ALLOWED=True):
        assert client.get(path).status_code == 200, "the preview still reaches it"


def test_no_template_links_an_unpublished_substantive_legal_page_unconditionally():
    # the terms (category D) only through {% legal_links %}; the privacy notice (A) stays linked: it is never hidden
    text = (ROOT / "templates" / "community" / "join.html").read_text(encoding="utf-8")
    assert "{% url 'legal:terms'" not in text and '{% legal_links "terms"' in text


@pytest.mark.django_db
def test_the_privacy_notice_is_never_turned_into_a_404(client, seeded):
    from legal import services

    services.invalidate()
    with override_settings(ILE_LEGAL_OPEN_FIELDS_ALLOWED=False):
        assert client.get("/fr/privacy-policy/").status_code == 200


# ---- round 1 of W3 (label v515-c-improve1): the composed heads, one section per page, the second-time frame ------------
#: page → the head's composition (data-compose) and what must stand inside the head
COMPOSED = {
    "/fr/parcours/": ("route", ['class="via__action"']),
    "/fr/reseau/": ("network", ['class="ingresso__aside fronte-rete"', 'data-slot="network.table"']),
    "/fr/contact/": ("contact", ['class="ingresso__aside fronte-piano"', 'data-slot="contact.square"', 'href="mailto:']),
    "/fr/le-projet/": ("arch", ['class="ingresso__aside fronte-arco"', 'data-slot="project.hall"']),
    "/fr/attention-aux-fraudes/": ("notice", ['data-callout="antifraud"', 'data-locked="p3.antifraud.body"']),
    "/fr/agami/": ("name", ['class="fronte__name"']),
}


def _head(main: str) -> tuple[str, str]:
    head = re.search(r'<header class="ingresso"([^>]*)>(.*?)</header>', main, flags=re.S)
    return head.group(1), head.group(2)


@pytest.mark.django_db
@pytest.mark.parametrize("path", list(COMPOSED))
def test_the_drawing_composes_the_head_on_the_pages_whose_meaning_is_a_drawing(get, path):
    compose, inside = COMPOSED[path]
    attrs, body = _head(_main(get(path)))
    assert f'data-compose="{compose}"' in attrs, (path, attrs)
    for needle in inside:
        assert needle in body, (path, needle)


@pytest.mark.django_db
def test_the_companies_head_is_words_and_a_workplace_photograph_no_skyline(get):
    """V5.30 Fast Visual Variety Correction §7 ENTREPRISES, «workplace imagery, less decorative architecture» (V5.20 strict
    rule; this decision replaces the skyline's row in COMPOSED): the head composes no drawing, its photograph stays in it."""
    attrs, body = _head(_main(get("/fr/entreprises/")))
    assert "data-compose" not in attrs, attrs
    assert 'data-slot="companies.hero"' in body


@pytest.mark.django_db
def test_the_network_diagram_names_the_five_actors_for_the_eye_only(get):
    """V5.22 (SECTION_SYSTEM_V2 §3.11 RE-0 + RE-1 + RE-2; strict rule V5.20): the ring's five nodes become the map's
    controls — links to the actors' entries, docked in the head (tabs once sezioni/mappa.js runs) — and the register
    that told the same five actors again below is gone (words once). The drawing stays for the eye only (its lines and
    circles aria-hidden); what a screen reader reads is the five named links and the five entries, each its h2, every
    entry in the page without script."""
    _attrs, body = _head(_main(get("/fr/reseau/")))
    assert re.search(r'<svg class="fronte-rete__lines"[^>]*aria-hidden="true"', body)
    nodes = re.search(r'<ul class="fronte-rete__nodes[^"]*" role="list">(.*?)</ul>', body, flags=re.S).group(1)
    links = re.findall(r'<a class="mappa__tasto fronte-rete__tasto" id="rete-([a-z]+)-tab" href="#rete-\1"', nodes)
    assert links == ["persons", "companies", "institutions", "universities", "professionals"]
    for key in links:
        entry = re.search(rf'<section class="rete__pannello" id="rete-{key}"[^>]*>(.*?)</section>', body, flags=re.S)
        assert entry and f'id="rete-{key}-title"' in entry.group(1), key
    assert "actor-list" not in get("/fr/reseau/")


@pytest.mark.django_db
def test_the_fraud_notice_is_the_head_s_panel_and_appears_once(get):
    main = _main(get("/fr/attention-aux-fraudes/"))
    assert main.count('data-callout="antifraud"') == 1 and main.count('data-locked="p3.antifraud.body"') == 1
    _attrs, body = _head(main)
    assert 'class="ingresso__label"' in body and "<h1" in body


@pytest.mark.django_db
def test_the_promoter_s_name_keeps_every_character_in_two_weights(get, settings):
    _attrs, body = _head(_main(get("/fr/agami/")))
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", body, flags=re.S).group(1)
    text = re.sub(r"<[^>]+>", "", h1)
    from django.utils.html import escape

    assert text == escape(settings.ILE["PROMOTER"]), text


@pytest.mark.django_db
def test_the_promoter_name_reads_ltr_in_arabic(get):
    # round 2 (MJ-2): the Italian legal name is tagged and isolated left-to-right in both parts, so in an RTL h1 its
    # dash stays before «Dialogo …» (WCAG 3.1.2 for the Latin name on an Arabic page)
    _attrs, body = _head(_main(get("/ar/agami/")))
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", body, flags=re.S).group(1)
    assert '<span class="fronte__name" lang="it" dir="ltr">AGAMI</span>' in h1, h1
    assert re.search(r'<span class="fronte__name-rest" lang="it" dir="ltr">— Dialogo', h1), h1
    css = FRONTE.read_text(encoding="utf-8")
    assert re.search(r'\[dir="rtl"\] \.ingresso__title > :is\(\.fronte__name, \.fronte__name-rest\) \{\s*text-align: end;', css)


@pytest.mark.django_db
@pytest.mark.parametrize(
    "path, section",
    [("/fr/projet-pilote/", "Projet"), ("/fr/formation/", "Personnes"), ("/fr/attention-aux-fraudes/", "Personnes")],
)
def test_a_page_linked_from_two_panels_marks_one_section(get, path, section):
    nav = get(path).split('<main id="main-content"', 1)[0]
    # the row's sections (the desktop doors, the sheet's rows, the plain links) that carry aria-current
    marked = re.findall(
        r'<(?:button|summary|a) class="(?:main-nav__link[^"]*|nav-sheet__row)"[^>]*aria-current="[^"]+"[^>]*>(.*?)</(?:button|summary|a)>',
        nav,
        flags=re.S,
    )
    labels = {re.sub(r"<[^>]+>", "", m).strip() for m in marked}
    assert labels == {section}, (path, labels)


def test_the_second_time_frame_has_its_own_column_never_over_the_text():
    css = re.sub(r"/\*.*?\*/", "", COMPOSE.read_text(encoding="utf-8"), flags=re.S)
    rule = re.search(r"\.training-phase > \.training-phase__photo \{([^}]*)\}", css.split("@media (min-width: 64rem)")[-1])
    assert rule and "grid-column: 3" in rule.group(1) and "position: absolute" not in rule.group(1)


def test_the_drawn_width_is_declared_for_the_heads():
    # `sizes` states the track the frame is drawn in (the 6/6 heads 38 rem at 80 rem, the 4:5 heads 32 rem)
    for key in ("training.hero", "diplomas.hero", "companies.hero"):
        assert imagery.BY_KEY[key].sizes.startswith("(min-width: 80rem) 38rem"), key
    for key in ("pathways.hero", "institutions.hero", "universities.hero"):
        assert imagery.BY_KEY[key].sizes.startswith("(min-width: 80rem) 32rem"), key
    # the assembly hall develops as it enters: touch and keyboard see its colour too
    assert imagery.BY_KEY["institutions.chamber"].treatment == "develop"


# ---- round 2 of W3 (label v515-c-improve2) ---------------------------------------------------------------------------
@pytest.mark.django_db
@pytest.mark.parametrize("path, inside", [("/fr/le-projet/", "fronte-arco"), ("/fr/reseau/", "fronte-rete"), ("/fr/agami/", "fronte__name")])
def test_a_curated_library_photograph_never_replaces_a_composed_head(get, monkeypatch, path, inside):
    # m-7: the media seed may curate «workshop», «forum_event» or «entrance_institution»; the composed heads keep their
    # drawing and AGAMI never shows a library photograph (Q5). The view still holds the photo for the page's SEO.
    from pages import services

    curated = services.Photo(src="/media/curated.jpg", srcset="", alt="curated", alt_lang="", width=1200, height=800,
                             caption="Curated", place="Roma", credit="Archive")
    monkeypatch.setattr(services, "photo_for_slot", lambda slot, lang=None: curated)
    _attrs, body = _head(_main(get(path)))
    assert "/media/curated.jpg" not in body, path
    assert 'class="ingresso__aside figura"' not in body, path
    assert inside in body, path


#: finishing round F1: the heads whose source title is long and set in capitals lay out words-first on a phone
WORDS_FIRST = {"parcours/", "entreprises/", "diplomes-et-titres/", "projet-pilote/"}


@pytest.mark.django_db
@pytest.mark.parametrize("lang", ["fr", "ar"])
@pytest.mark.parametrize("slug", ["parcours/", "entreprises/", "diplomes-et-titres/", "projet-pilote/", "institutions/", "universites-et-formation/", "formation/", "reseau/"])
def test_the_head_s_layout_follows_the_page_not_the_case_of_the_string(get, lang, slug):
    # F1: an Arabic title has no case, so `upper == itself` held for every Arabic h1 and each Arabic head took the
    # capitals layout the French page did not; the page now names it (`words_first`), the same in every language
    attrs, body = _head(_main(get(f"/{lang}/{slug}")))
    assert ("data-words-first" in attrs) == (slug in WORDS_FIRST), (lang, slug, attrs)
    h1 = re.search(r'<h1 class="([^"]*)"[^>]*>(.*?)</h1>', body, flags=re.S)
    words = re.sub(r"<[^>]+>", "", h1.group(2))
    cased = any(ch.isalpha() and ch.upper() != ch.lower() for ch in words)
    assert ("ingresso__title--caps" in h1.group(1)) == (cased and words.upper() == words), (lang, slug, h1.group(0)[:160])
    css = FRONTE.read_text(encoding="utf-8")
    assert ":has(.ingresso__title--caps)" not in css


@pytest.mark.django_db
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_a_capitals_chapter_title_is_tracked_and_an_arabic_one_is_not_marked(get, lang):
    # F1: «POURQUOI ITALY LEGAL ENTRY» is tracked and one optical step down; the Arabic «بإيجاز» carries no capitals class
    # V5.22 (SECTION_SYSTEM_V2 §3.2 LP-1 + LP-2 + LP-3; strict rule V5.20): the chapters are the steps of «il racconto»,
    # each heading the story's own (`racconto__titolo`) under its chapter's anchor, kept — the capitals step is tracked
    # by its anchor in the family's sheet (pages/css/_projet.css), the same rule, never on an Arabic title
    main = _main(get(f"/{lang}/le-projet/"))
    assert re.search(r'<h2 class="racconto__titolo" id="project-why-title"', main) is not None
    projet = re.sub(r"/\*.*?\*/", "", (ROOT / "apps" / "pages" / "static" / "pages" / "css" / "_projet.css").read_text(encoding="utf-8"), flags=re.S)
    assert re.search(r'\.racconto__titolo\[id="project-why-title"\]:not\(:lang\(ar\)\) \{\s*letter-spacing: var\(--track-display-caps\);', projet)
    assert re.search(r'@media \(min-width: 48rem\) \{\s*\.racconto \.racconto__titolo\[id="project-why-title"\]:not\(:lang\(ar\)\) \{\s*font-size: 1\.5rem;', projet)
    assert "project-presentation-title" not in projet, "«En bref» is never tracked as capitals"
    assert re.search(r'class="chapter__title chapter__title--caps" id="project-presentation-title"', main) is None
    css = re.sub(r"/\*.*?\*/", "", COMPOSE.read_text(encoding="utf-8"), flags=re.S)
    assert re.search(r"\.chapter__title\.chapter__title--caps:not\(:lang\(ar\)\) \{\s*letter-spacing: var\(--track-display-caps\);", css)
