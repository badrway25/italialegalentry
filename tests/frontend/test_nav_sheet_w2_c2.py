"""
The navbar, part 2 (design V5, V5.4 plan §1.12 item 8, §1.11, §1.14; W2-C2): the sheet below 80rem, the signed-in
targa's account popover and the overlay system on every public page — checked on the rendered pages and on the
sources, without a browser (the behaviour is tests/frontend/test_browser_w2_c2.py's, the Arabic geometry
tests/i18n/test_rtl_browser_w2_c2.py's).

The sheet is the overlay system's modal drawer (docs/design-v5/QA/v54/w2-a/CONTRACT.md), written at the body's level
after the letterhead: «Menu» is a link to it (the no-script path), «Fermer» takes the first focus, the Fase 3 order
holds — the languages, the doors that unfold in place, Forum · Projet, the search, the primary, the anti-fraud line,
the foot pinned on night — and nothing in it links to a page whose gate is closed.
"""

from __future__ import annotations

import re
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
CHROME = ROOT / "static" / "css" / "v5" / "chrome.css"
NAV_JS = ROOT / "static" / "js" / "src" / "nav.js"
SHELL_JS = ROOT / "static" / "js" / "src" / "shell.js"
MAIN_JS = ROOT / "static" / "js" / "main.js"
OVERLAY_JS = ROOT / "static" / "js" / "src" / "overlay.js"


def _read(path: Path) -> str:
    return path.read_bytes().decode("utf-8")


def _get(client, path: str) -> str:
    response = client.get(path)
    assert response.status_code == 200, (path, response.status_code)
    return response.content.decode()


def _sheet(html: str) -> str:
    start = html.index('<dialog class="overlay overlay--drawer nav-sheet"')
    return html[start : html.index("</dialog>", start) + len("</dialog>")]


class _Order(HTMLParser):
    """The sheet's parts in document order, by the class or the hook that names each."""

    PARTS = (
        ("nav-sheet__head", "head"),
        ("lang-seg", "languages"),
        ("nav-sheet__item--door", "door"),
        ("nav-sheet__item--after-doors", "after-doors"),
        ("nav-sheet__search", "search"),
        ("nav-sheet__primary", "primary"),
        ("nav-sheet__fraud", "fraud"),
        ("nav-sheet__foot", "foot"),
    )

    def __init__(self):
        super().__init__()
        self.seen: list[str] = []

    def handle_starttag(self, tag, attrs):
        classes = (dict(attrs).get("class") or "").split()
        for name, part in self.PARTS:
            if name in classes:
                self.seen.append(part)


def _order(sheet: str) -> list[str]:
    parser = _Order()
    parser.feed(sheet)
    return parser.seen


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_sheet_follows_the_letterhead_at_the_bodys_level(client, seeded, phase3_open, lang):
    html = _get(client, f"/{lang}/")
    header = html[html.index('<header class="site-header"') : html.index("</header>")]
    after = html[html.index("</header>") :]
    assert '<dialog class="overlay overlay--drawer nav-sheet" id="nav-sheet" data-overlay="drawer"' in after, (
        "the sheet stands after the letterhead, outside every stacking context of the header"
    )
    assert '<dialog class="overlay overlay--drawer nav-sheet"' not in header
    # «Menu»: a link to the sheet (the overlay system opens it; :target without script) — and its stable test hook
    assert re.search(r'<a class="nav-toggle" href="#nav-sheet" data-overlay-open data-nav-toggle>', header)
    sheet = _sheet(html)
    assert re.search(r'aria-label="[^"]+"', sheet.split(">", 1)[0]), "the sheet has a name"
    # the head line: the lock-up (the home's link) and «Fermer», which takes the first focus and is a link back
    head = sheet[sheet.index("nav-sheet__head") : sheet.index("nav-sheet__body")]
    assert 'class="brand brand--lockup"' in head and 'class="lock' in head
    assert re.search(r'<a class="nav-toggle" href="#site-header" data-overlay-close data-overlay-focus>', head)
    # one width for «Menu» and «Fermer» below 48rem (REVIEW m5): each holds both words, the other one hidden from
    # assistive technology and from the eye — the letterhead's visible word is the sheet's hidden one, and back
    word = r'<span class="nav-toggle__word"><span>([^<]+)</span><span class="nav-toggle__alt" aria-hidden="true">([^<]+)</span></span>'
    menu_words = re.search(word, header[header.index("data-nav-toggle>") :])
    fermer_words = re.search(word, head)
    assert menu_words and fermer_words, "both buttons hold both words"
    assert menu_words.groups() == fermer_words.groups()[::-1], (menu_words.groups(), fermer_words.groups())


def test_the_sheet_keeps_the_fase_3_order(client, seeded, phase3_open, legal_published):
    sheet = _sheet(_get(client, "/fr/"))
    order = _order(sheet)
    assert order[:2] == ["head", "languages"], order
    assert order.count("door") == 4, order
    expected = [
        "head",
        "languages",
        "door",
        "door",
        "door",
        "door",
        "after-doors",
        "search",
        "primary",
        "fraud",
        "foot",
    ]
    assert order == expected, order
    # the doors unfold in place: one exclusive group of <details name>, with main.js's accordion where `name` is
    # not supported; every door carries its night disc, Forum its glyph, Projet unfolds as the doors do
    assert sheet.count('name="nav-sheet-doors"') == 5
    assert 'data-accordion="single"' in sheet
    assert sheet.count('<span class="portico__disc">') == 4
    assert sheet.count("#icon-handshake") == 1
    # the languages by their own names, never «ع»
    for name in ("Italiano", "Français", "English", "العربية"):
        assert name in sheet
    assert ">ع<" not in sheet
    # the search is the FAQ's — the one public search — named by its visible label; the primary and the anti-fraud
    # line are the pages' own live strings
    assert re.search(r'<form class="search-form nav-sheet__search" method="get" action="/fr/faq/" role="search"', sheet)
    assert (
        '<label class="search-form__label" for="nav-sheet-q">Rechercher dans les questions fréquentes</label>' in sheet
    )
    assert 'href="/fr/orientation/' in sheet
    assert "Découvrir le questionnaire d’orientation" in sheet
    assert "Lire la page «\u00a0Attention aux fraudes\u00a0»" in sheet  # through `typo` (W4-A, m2)


def test_before_phase3_the_sheet_carries_no_closed_page(client, seeded):
    """With the default flags the Phase 3 pages are closed: no door of theirs, no FAQ search, no anti-fraud line —
    and no link of the sheet answers 404 (tests/compliance/test_no_links_to_gated_pages.py checks every page)."""
    html = _get(client, "/fr/")
    sheet = _sheet(html)
    assert 'role="search"' not in sheet
    assert "Attention aux fraudes" not in sheet
    for href in re.findall(r'href="(/fr/[^"#?]*)"', sheet):
        assert client.get(href).status_code == 200, href


def test_every_id_of_the_page_is_unique_with_the_bar_and_the_sheet_drawn(client, seeded, phase3_open, person_user):
    client.force_login(person_user)
    html = _get(client, "/fr/")
    ids = Counter(re.findall(r'\sid="([^"]+)"', html))
    assert [i for i, n in ids.items() if n > 1] == []
    # every aria-describedby and aria-controls names an element of the page
    for refs in re.findall(r'aria-(?:describedby|controls)="([^"]+)"', html):
        for ref in refs.split():
            assert ids[ref] == 1, ref


def test_signed_in_the_targa_seat_and_the_sheets_foot_hold_the_account_popover(client, seeded, person_user):
    client.force_login(person_user)
    html = _get(client, "/fr/")
    header = html[html.index('<header class="site-header"') : html.index("</header>")]
    sheet = _sheet(html)
    # the overlay system's popover in both seats — a real button, named by the words it shows then what it opens
    seat = header[header.index('class="targa-seat"') :]
    assert 'popovertarget="account-menu"' in seat
    assert re.search(
        r'<div class="overlay overlay--popover" id="account-menu" data-overlay="popover" popover role="group"', seat
    )
    foot = sheet[sheet.index("nav-sheet__foot") :]
    assert 'popovertarget="account-menu-sheet"' in foot and 'id="account-menu-sheet"' in foot
    assert re.search(r'aria-label="[^"]+ — Mon compte"', seat)
    assert 'action="/fr/compte/logout/"' in seat and 'action="/fr/compte/logout/"' in foot
    # design V4's <details> face left with the move: no disclosure menu on a public page
    assert "data-dropdown" not in html and "account-menu__list" not in html


def test_the_flag_off_leaves_no_targa_in_the_sheet_and_no_hole(client, seeded, set_flag):
    html = _get(client, "/fr/")
    foot = _sheet(html)[_sheet(html).index("nav-sheet__foot") :]
    assert 'class="targa targa--night" href="/fr/compte/login/"' in foot
    set_flag("reserved_area_public_link", False)
    html = _get(client, "/fr/")
    foot = _sheet(html)[_sheet(html).index("nav-sheet__foot") :]
    assert "targa" not in foot
    assert 'class="nav-sheet__promoter"' in foot, "the promoter stays: the foot is never empty"


def test_the_key_alone_is_named_by_the_overlay_systems_tooltip(client, seeded):
    html = _get(client, "/fr/")
    header = html[html.index('<header class="site-header"') : html.index("</header>")]
    assert re.search(
        r'<a class="targa" href="/fr/compte/login/" aria-label="Espace réservé" data-tip="layer" data-tip-side="block-end">',
        header,
    )
    assert "targa__tip" not in html


def test_the_sheets_stylesheet_and_the_retired_drawer():
    chrome = _read(CHROME)
    # the drawer's legacy selectors left with it, here and in components.css; v4/shell.css left the cascade
    for gone in (".nav-drawer", ".nav-overlay", ".drawer-utility", ".main-nav--drawer", "data-nav-open", ".targa__tip"):
        assert gone not in chrome, gone
    assert ".main-nav__panel" not in _read(ROOT / "static" / "css" / "components.css")
    assert '@import url("v4/shell.css")' not in _read(ROOT / "static" / "css" / "main.css")
    assert not (ROOT / "static" / "css" / "v4" / "shell.css").exists()
    # «Quiet» on a phone: the rows rise only where motion is welcome, and tier 0 from the keyboard
    quiet = re.search(
        r"@media \(max-width: 47\.999rem\) and \(prefers-reduced-motion: no-preference\) \{(.*?)\n\}", chrome, re.S
    )
    assert quiet and "translate: 0 12px" in quiet.group(1) and 'html[data-input="key"]' in quiet.group(1)
    # the regression guard of the cold open: under the input flag (and anywhere in the chrome) a subject is named,
    # never the universal selector — `html[data-input="key"] .nav-sheet > *` restyled the whole document at the
    # first press (718 elements, 56 ms at CPU x4)
    for selector in re.findall(r"([^{}\n]*html\[data-input=\"key\"\][^{]*)\{", chrome):
        for part in selector.split(","):
            assert not re.search(r"(^|[\s>+~])\*\s*$", part.strip()), part
    # every target of the sheet holds 44 px: its rows, the doors' 64 px, the night targa, the anti-fraud link
    assert "min-block-size: var(--drawer-row-h)" in chrome
    assert re.search(r"\.nav-sheet__fraud a \{ min-block-size: var\(--hit-primary\); \}", chrome)


def test_the_overlay_system_is_on_every_public_page_and_the_old_scripts_left():
    shell = _read(SHELL_JS)
    nav = _read(NAV_JS)
    main = _read(MAIN_JS)
    assert re.search(r'^import "\./overlay\.js";$', shell, re.M), "shell.js imports the overlay system"
    assert re.search(r'^import \{ close as closeOverlay \} from "\./overlay\.js";$', nav, re.M)
    for gone in ("function initDrawer", "data-nav-drawer", "data-nav-overlay", "navOpen", "tip-off"):
        assert gone not in nav, gone
    # «la targa»'s key alone: the system's top-layer tip names it; nav.js only refuses it where the plate says its word
    targa = nav[nav.index("function initTarga") :]
    targa = targa[: targa.index("\n}\n")]
    assert '"overlay:tip"' in targa and "event.preventDefault()" in targa and "(min-width: 100rem)" in targa
    assert "function initDropdowns" not in main and "initDropdowns()" not in main


def test_the_review_fixes_hold_in_the_sources():
    """The fix pass of the family's review and accessibility check (docs/design-v5/QA/v54/w2-c2/NOTES.md «Review fixes»),
    on the sources: what the browser tests measure, held where a refactor would undo it."""
    chrome = _read(CHROME)
    # M1: the 64–80rem band draws the lock-up at the compact 32/17, as the laptop band does
    band = re.search(r"@media \(min-width: 64rem\) and \(max-width: 89\.999rem\) \{(.*?)\n\}", chrome, re.S)
    assert band and ".site-header .lock__wm { font-size: 17px; }" in band.group(1)
    assert ".site-header .lock__mark { inline-size: 32px; block-size: 32px; }" in band.group(1)
    # M2: from 48rem the side sheet keeps its foot — only the head's lock-up goes; m3: its own 24 px margin
    side = re.search(
        r"@media \(min-width: 48rem\) \{\n  \.nav-sheet \{ --grid-margin: var\(--s-6\); \}\n(.*?)\n\}", chrome, re.S
    )
    assert (
        side
        and ".nav-sheet__head > .brand { display: none; }" in side.group(1)
        and "nav-sheet__foot" not in side.group(1)
    )
    # A11Y_PERF M2: the foot is not a night context — its own controls take the night's ring, its menu keeps the paper's
    assert "nav-sheet__foot on-inverse" not in _read(ROOT / "templates" / "partials" / "main_nav.html")
    assert (
        ".nav-sheet__foot :is(.targa, .account-menu__summary) { --focus-ring: var(--focus-ring-night); "
        "--focus-halo: var(--focus-halo-night); }" in chrome
    )
    # m4: the unfolded door's gloss in the lede's voice — ink, a step above the entries' 13 px second lines
    gloss = re.search(r"\.nav-sheet__gloss \{([^}]*)\}", chrome).group(1)
    assert "color: var(--text-1)" in gloss and "font-size: var(--t-ui)" in gloss
    # m6: the account menu's wrapper is a flex box in both seats
    assert ":is(.targa-seat, .nav-sheet__foot) .account-menu { display: flex; }" in chrome
    # m7: no browser tint on a press anywhere in the public chrome
    assert (
        ":is(.site-header, .utility-bar, .nav-sheet) :is(a, button, summary) { -webkit-tap-highlight-color: transparent; }"
        in chrome
    )
    # A11Y_PERF m1: a short viewport does not pin the foot; a focused stop never stands under the sticky head
    short = re.search(r"@media \(max-height: 30rem\) \{(.*?)\n\}", chrome, re.S)
    assert (
        short
        and "overflow-y: auto" in short.group(1)
        and "scroll-padding-block-start: var(--header-h)" in short.group(1)
    )
    assert "position: sticky" in short.group(1)
    # A11Y_PERF M1: a press held on the scrim keeps its place over a trapped panel until the press ends
    overlay = _read(OVERLAY_JS)
    assert 'if (!scrim.hasAttribute("data-held")) scrim.style.setProperty("z-index"' in overlay
    release = overlay[overlay.index("const release = () => {") :]
    assert "syncScrim();" in release[: release.index("};")]
    # REVIEW m2: any opening of the overlay system puts an open door's panel away
    assert 'document.addEventListener("overlay:open", () => close(false));' in _read(NAV_JS)
