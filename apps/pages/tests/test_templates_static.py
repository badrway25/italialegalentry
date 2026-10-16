"""Static compliance of the pages templates, stylesheet and script (no DB needed)."""

from __future__ import annotations

import posixpath
import re
from pathlib import Path

import pytest
from django.contrib.staticfiles import finders

from cms import locked_content
from cms.forbidden import scan

pytestmark = pytest.mark.compliance

ROOT = Path(__file__).resolve().parents[3]
TEMPLATES = sorted((ROOT / "templates" / "pages").rglob("*.html"))
APP_DIR = ROOT / "apps" / "pages"
CSS = APP_DIR / "static" / "pages" / "css" / "pages.css"
# The home's scripts since design V5.4 (W2-D): the one entry and the hero's module, bundled by esbuild into
# static/js/dist/home.js (apps/pages/static/pages/js/home.js moved into the entry and was deleted).
JS = (ROOT / "static" / "js" / "src" / "home.js", ROOT / "static" / "js" / "src" / "hero.js")
# Design V5 (W1-B): the sprite's own ids — static/img/icons.svg is built from static/icons/src by
# scripts/build_icons.py and named by apps/core/icons.py; a literal that is not a symbol fails here and in
# tests/frontend/test_icons.py.
AVAILABLE_ICONS = set(
    re.findall(r'<symbol id="icon-([a-z0-9-]+)"', (ROOT / "static" / "img" / "icons.svg").read_text(encoding="utf-8"))
)


def _prescribed_sentences() -> list[str]:
    out: list[str] = []

    def walk(value):
        if isinstance(value, str):
            if len(value) > 25:
                out.append(value)
        elif isinstance(value, dict):
            for name, item in value.items():
                if name != "key":  # technical identifiers (faq_…, pathway keys) are not prescribed wording
                    walk(item)
        elif isinstance(value, (list, tuple)):
            for item in value:
                walk(item)

    for key, value in locked_content.LOCKED_TEXTS["fr"].items():
        if not key.startswith("legal."):
            walk(value)
    return out


def test_template_set_is_complete():
    names = {p.relative_to(ROOT / "templates" / "pages").as_posix() for p in TEMPLATES}
    expected = {"home.html", "institutional_base.html", "project.html", "agami.html", "network.html", "contact.html"}
    expected |= {"antifraud.html", "partials/_picture.html", "partials/_section_header.html"}
    expected |= {
        f"home/_{key}.html"
        for key in ("hero banner entrances orientation pathways pilot trust antifraud news ecosystem reserved".split())
    }
    assert expected <= names


@pytest.mark.parametrize("path", TEMPLATES, ids=lambda p: p.name)
def test_templates_never_hand_copy_prescribed_texts(path):
    text = path.read_text(encoding="utf-8")
    for sentence in _prescribed_sentences():
        assert sentence not in text, (path.name, sentence[:60])
    for short in ("ATTENTION AUX FRAUDES", "ESPACE RÉSERVÉ", "ITALY LEGAL ENTRY™", "DÉCOUVREZ LE FORUM", "CONNEXION"):
        assert short not in text, (path.name, short)


@pytest.mark.parametrize("path", TEMPLATES, ids=lambda p: p.name)
def test_templates_have_no_forbidden_strings_inline_styles_or_external_hosts(path):
    text = path.read_text(encoding="utf-8")
    assert scan(text) == [], path.name
    assert "®" not in text and "&reg;" not in text
    assert not re.search(r"\sstyle=\"", text), path.name
    assert not re.search(r"\son[a-z]+=\"", text), path.name
    assert not re.search(r"https?://", text), path.name
    assert "legalitalentry.it" not in text
    assert "<iframe" not in text


@pytest.mark.parametrize("path", TEMPLATES, ids=lambda p: p.name)
def test_templates_use_only_existing_icons_and_translated_strings(path):
    text = path.read_text(encoding="utf-8")
    used = set(re.findall(r'svg_icon "([a-z0-9-]+)"', text))
    assert used <= AVAILABLE_ICONS, used - AVAILABLE_ICONS
    # The public address is printed through site.contact_email only.
    assert "agamieuromed" not in re.sub(r"{% comment %}.*?{% endcomment %}", "", text, flags=re.S)


def test_pending_legal_review_is_marked_where_content_is_missing():
    marked = {p.name for p in TEMPLATES if "CONTENT_PENDING_LEGAL_REVIEW" in p.read_text(encoding="utf-8")}
    assert {"agami.html", "antifraud.html", "contact.html", "_ecosystem.html", "_pathways.html"} <= marked


def test_no_border_crossing_cliche_imagery_anywhere():
    """
    The cliché imagery of migration stays banned. The project's OWN doorway does not.

    This test used to forbid the word "doorway" outright, with the rest of the border-crossing
    vocabulary, because the build it was written for had no doorway of its own and any door on the
    page would have been the cliché. On 23 September 2026 the client confirmed the opposite: the
    arch, the key and the three steps of legalitalentry.it are the project's mark and its hero
    composition (docs/design-v2/BRAND_ASSETS.md), and the design system makes them the signature
    (DESIGN_SYSTEM_V2.md §8.4). Banning the word now would ban the brand.

    What the rule was protecting is unchanged and still enforced below: no passport, no border
    gate, no generic "entrance door" stock imagery. The second assertion is the new half — if the
    word "doorway" appears, it must be OUR doorway, the one with the key and the steps.
    """
    blob = " ".join(p.read_text(encoding="utf-8") for p in TEMPLATES).lower()
    for word in ("entrance-door", "porte d’entrée", "passport", "passeport", "border gate", "poste-frontière"):
        assert word not in blob, word

    # Since design V4 the door is drawn once, in templates/components/doorway.html, and the pages
    # include it: OUR doorway is the component, so it is read with the pages that name it.
    component = ROOT / "templates" / "components" / "doorway.html"
    if component.exists():
        blob += " " + component.read_text(encoding="utf-8").lower()

    if "doorway" in blob:
        for part in ("doorway__key", "doorway__steps", "doorway__arch"):
            assert part in blob, f"a doorway without its {part}: that is the cliché, not the brand"


def test_stylesheet_and_script_are_discoverable_static_files():
    assert finders.find("pages/css/pages.css")
    assert finders.find("pages/css/hero.css")
    assert finders.find("js/dist/home.js")
    assert not finders.find("pages/js/home.js"), "the home's script is the esbuild entry, not a second request"


def test_stylesheet_uses_tokens_and_logical_properties_only():
    """The home's sheet, and the partials it imports — the passage «la linea», static/css/v5/_journey-passage.css
    (W3-D, DL54-128 item 4) —, use tokens and logical properties only, and load nothing: the source imports local
    partials only, written in the collected tree, and the bundle the page links (css/dist/pages/css/pages.css, built by
    scripts/build_css.mjs) carries them inlined, without an @import."""
    css = CSS.read_text(encoding="utf-8")
    imports = re.findall(r'@import url\("([^"]+)"\);', re.sub(r"/\*.*?\*/", "", css, flags=re.S))
    sheets = {CSS.name: css}
    for target in imports:
        assert posixpath.basename(target).startswith("_") and not re.match(r"[a-z]+:|/", target), target
        found = finders.find(posixpath.normpath(posixpath.join("pages/css", target)))
        assert found, target
        sheets[target] = Path(found).read_text(encoding="utf-8")
    for name, text in sheets.items():
        stripped = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
        assert re.findall(r"#[0-9a-fA-F]{3,8}\b", stripped) == [], f"{name}: no literal colour: use var(--…)"
        assert not re.search(r"\brgba?\(|\bhsla?\(", stripped), name
        physical = re.findall(
            r"(?<![-\w])(?:margin|padding|border)-(?:left|right)\b|(?<![-\w])(?:left|right)\s*:"
            r"|text-align:\s*(?:left|right)|float:\s*(?:left|right)",
            stripped,
        )
        assert physical == [], (name, physical)
        assert not re.search(r"https?://", stripped), name
        assert "!important" not in re.sub(r"@media print\s*{.*", "", stripped, flags=re.S), name
        assert scan(text) == [], name
    assert re.sub(r"/\*.*?\*/", "", css, flags=re.S).count("@import") == len(imports), "an @import is a partial's url"
    bundle = ROOT / "static" / "css" / "dist" / "pages" / "css" / "pages.css"
    assert "@import" not in bundle.read_text(encoding="utf-8"), "the sheet the home links loads nothing more"


def test_stylesheet_motion_relies_on_design_system_durations():
    """Every transition reads a duration token: the V5 names (--motion-*, the home's chapters since W2-D step 3) or the
    legacy shim's (--duration-*, the institutional pages until their family rebuilds them). Both are zeroed under
    reduced motion by the token sheets."""
    css = CSS.read_text(encoding="utf-8")
    for declaration in re.findall(r"transition:[^;]+;", css):
        assert "var(--motion-" in declaration or "var(--duration-" in declaration, declaration
    assert "animation" not in css  # restrained motion: transitions only, collapsed by reduced-motion tokens


@pytest.mark.parametrize("path", JS, ids=lambda p: p.name)
def test_script_is_cookie_free_and_network_free(path):
    js = path.read_text(encoding="utf-8")
    code = re.sub(r"/\*.*?\*/", "", js, flags=re.S)
    code = re.sub(r"//[^\n]*", "", code)
    assert "document.cookie" not in code
    assert "localStorage" not in code
    for network in ("fetch(", "XMLHttpRequest", "sendBeacon", "WebSocket", "import("):
        assert network not in code, network
    assert "sessionStorage" in code  # tab-scoped, never sent to the server
    assert not re.search(r"https?://", js)
    assert scan(js) == []


def test_python_sources_never_hand_copy_prescribed_texts():
    sentences = _prescribed_sentences()
    for path in sorted(APP_DIR.glob("*.py")):
        text = path.read_text(encoding="utf-8")
        for sentence in sentences:
            assert sentence not in text, (path.name, sentence[:60])
        assert "®" not in text, path.name
