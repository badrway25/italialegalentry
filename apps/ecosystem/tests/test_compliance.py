"""
Compliance of the four ecosystem pages, in every language and in both states of gate G3:
forbidden formulations, trademark, public e-mail, external resources, inline styles, internal
markers, single h1 — plus static checks of the app's own sources (templates, CSS, Python).
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from django.conf import settings

from cms import locked_content
from cms.forbidden import scan

from .conftest import COMPANIES_PATH, GATED_PATHS, LANGS

pytestmark = [pytest.mark.compliance, pytest.mark.django_db]

BASE = Path(settings.BASE_DIR)
TEMPLATES = BASE / "templates" / "ecosystem"
APP = BASE / "apps" / "ecosystem"
INTERNAL_MARKERS = ("CONTENT_PENDING_LEGAL_REVIEW", "lorem ipsum", "TODO", "[ ]", "PENDING_CLIENT")
PROMISE_TOKENS = (
    "visa garanti",
    "visto garantito",
    "guaranteed",
    "entrée assurée",
    "canal actif",
    "corridoio operativo",
    "ingressi garantiti",
    "approbation ministérielle",
    "approvazione ministeriale",
)
EXPLICITLY_FORBIDDEN = ("Recruit in Morocco", "Find Qualified Profiles", "profils à recruter")


def _assert_compliant(lang: str, path: str, html: str) -> None:
    where = (lang, path)
    assert scan(html) == [], (where, scan(html))
    assert not re.search(r"\bmatching\b", html, flags=re.I), where
    lowered = html.lower()
    for phrase in EXPLICITLY_FORBIDDEN:
        assert phrase.lower() not in lowered, (where, phrase)
    assert "®" not in html and "&reg;" not in lowered, where
    assert "Italy Legal Entry™" in html, where
    emails = set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}", html))
    assert emails <= {"contact@agamieuromed.org"}, (where, emails)
    externals = [
        u
        for u in re.findall(r'(?:src|href|srcset|content|action)="(https?://[^"]+)"', html)
        if "testserver" not in u and "localhost" not in u
    ]
    assert externals == [], (where, externals)
    assert not re.search(r"<[a-z][^>]*\sstyle=", html), (where, "inline style (CSP: style-src 'self')")
    assert not re.search(r"<[a-z][^>]*\son[a-z]+=\"", html), (where, "inline event handler")
    assert not re.search(r"<script(?![^>]*\ssrc=)(?![^>]*application/ld\+json)[^>]*>\s*\S", html), where
    assert html.count("<h1") == 1, where
    for marker in INTERNAL_MARKERS:
        assert marker not in html, (where, marker)
    for token in PROMISE_TOKENS:
        assert token not in lowered, (where, token)
    # Design V5.4 (W3-F1): the interior's entrance is the page's one header; no side column (the doors are the chrome's)
    assert '<main id="main-content"' in html and '<header class="ingresso"' in html, where
    assert '<nav class="local-nav"' not in html, where
    assert '<nav class="breadcrumbs container"' in html, where


@pytest.mark.parametrize("lang", LANGS)
def test_companies_page_is_compliant_before_phase3(get_html, seeded, lang):
    _assert_compliant(lang, COMPANIES_PATH, get_html(lang, COMPANIES_PATH))


@pytest.mark.parametrize("lang", LANGS)
def test_companies_page_is_compliant_with_the_form_open(get_html, seeded, legal_published, lang):
    _assert_compliant(lang, COMPANIES_PATH, get_html(lang, COMPANIES_PATH))


@pytest.mark.parametrize("lang", LANGS)
def test_all_four_pages_are_compliant_after_phase3(get_html, seeded, phase3_open, lang):
    for path in [COMPANIES_PATH, *GATED_PATHS.values()]:
        _assert_compliant(lang, path, get_html(lang, path))


def test_editorial_note_is_rendered_escaped_and_tagged(get_html, seeded):
    from ecosystem.models import EcosystemSpace

    space = EcosystemSpace.objects.get(key="companies")
    space.intro_note_fr = "Une note <b>éditoriale</b>.\n\nSecond paragraphe."
    space.save()
    html = get_html("it", COMPANIES_PATH)
    assert '<div class="ecosystem-note prose" lang="fr">' in html
    assert "&lt;b&gt;éditoriale&lt;/b&gt;" in html and "<b>éditoriale</b>" not in html
    assert "<p>Second paragraphe.</p>" in html


def test_no_block_waits_for_a_scroll_to_be_seen(get_html, seeded, phase3_open):
    """
    The design system hides ``.reveal`` blocks until they scroll into view. Design V5.4 (W3-F1): the spaces draw
    their sequences on «la linea», still at load — no block of these pages carries ``.reveal`` any more.
    """
    for path in [COMPANIES_PATH, *GATED_PATHS.values()]:
        html = get_html("fr", path)
        main = html.split('<main id="main-content"', 1)[1].split("</main>", 1)[0]
        assert re.findall(r'<(\w+) class="([^"]*\breveal\b[^"]*)"', main) == [], path


# ---------------------------------------------------------------------------------------------
# Static checks on the sources owned by this app
# ---------------------------------------------------------------------------------------------
def _template_files() -> list[Path]:
    files = sorted(TEMPLATES.rglob("*.html"))
    assert len(files) >= 5
    return files


def test_templates_have_no_forbidden_strings_inline_styles_or_external_hosts():
    for path in _template_files():
        text = path.read_text(encoding="utf-8")
        assert scan(text) == [], (path.name, scan(text))
        assert not re.search(r"\sstyle=\"", text), path.name
        assert not re.search(r"\son[a-z]+=\"", text), path.name
        assert not re.search(r"https?://", text), path.name
        assert "®" not in text and "@legalitalentry" not in text, path.name
        assert "agamieuromed" not in text, (path.name, "the public address comes from site.contact_email")


def test_prescribed_texts_are_never_hand_copied_in_templates_or_python():
    """Every prescribed sentence enters through the registry, never as a literal."""
    keys = [k for k in locked_content.keys() if k.startswith(("p1.companies.", "p3.institutions.", "p3.universities."))]
    keys += ["p3.pilot.title", "p3.pilot.body", "p2.forum.registration.button_secondary_pilot"]
    samples: list[str] = []
    for key in keys:
        value = locked_content.get(key, "fr")[0]
        samples += [value] if isinstance(value, str) else [v for v in value if isinstance(v, str)]
    samples += locked_content.get("p3.pilot.sequence", "fr")[0]
    samples += [e["answer"] for e in locked_content.get("p3.faq.items", "fr")[0]]
    samples = [s for s in samples if len(s) > 12]
    sources = _template_files() + sorted(APP.glob("*.py")) + sorted((APP / "static").rglob("*.css"))
    for path in sources:
        text = path.read_text(encoding="utf-8")
        for sample in samples:
            assert sample not in text, (path.name, sample[:50])


def test_templates_use_only_icons_of_the_sprite():
    sprite = (BASE / "static" / "img" / "icons.svg").read_text(encoding="utf-8")
    ids = set(re.findall(r'<symbol id="icon-([a-z0-9-]+)"', sprite))
    used: set[str] = set()
    for path in _template_files():
        text = path.read_text(encoding="utf-8")
        used |= set(re.findall(r'svg_icon "([a-z0-9-]+)"', text))
        used |= set(re.findall(r'icon="([a-z0-9-]+)"', text))
    assert used and used <= ids, used - ids


def test_ui_strings_are_wrapped_for_translation():
    """Visible French wording in the templates goes through {% translate %} / _()."""
    for path in _template_files():
        text = path.read_text(encoding="utf-8")
        text = re.sub(r"{% comment %}.*?{% endcomment %}", "", text, flags=re.S)
        text = re.sub(r"{#.*?#}", "", text)
        text = re.sub(r"{% block body_class %}.*?{% endblock %}", "", text, flags=re.S)  # CSS class names
        text = re.sub(r"{%.*?%}|{{.*?}}", "", text, flags=re.S)
        text = re.sub(r"<[^>]+>", " ", text)
        leftovers = re.findall(r"[A-Za-zÀ-ÿ’]{4,}", text)
        assert leftovers == [], (path.name, leftovers[:5])


def test_stylesheet_uses_tokens_logical_properties_and_no_motion():
    """
    Design V5.4 (W3-F1): the page sheet is a plain list of imports written in the collected tree (DS 2026 §2) — the
    shared page of the public interior (static/css/v5/_pagina.css, the budget pass), W3-F1's own parts of the
    interior's grammar (static/css/v5/_interior.css), the public passage «la linea» (static/css/v5/_journey-passage.css,
    W3-D's — the w3-d merge), the door card (static/css/v5/_porta.css) and the spaces' own partial; read together, they
    use tokens
    only, logical properties only, and nothing moves (the sequences are drawn still).
    """
    sheet = (APP / "static" / "ecosystem" / "ecosystem.css").read_text(encoding="utf-8")
    imports = re.findall(r'@import url\("([^"]+)"\);', sheet)
    assert imports == [
        "../css/v5/_pagina.css",
        "../css/v5/_interior.css",
        "../css/v5/_journey-passage.css",
        "../css/v5/_porta.css",
        "_spaces.css",
    ], imports
    css = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (
            BASE / "static" / "css" / "v5" / "_pagina.css",
            BASE / "static" / "css" / "v5" / "_interior.css",
            BASE / "static" / "css" / "v5" / "_journey-passage.css",
            BASE / "static" / "css" / "v5" / "_porta.css",
            APP / "static" / "ecosystem" / "_spaces.css",
        )
    )
    assert re.findall(r"#[0-9a-fA-F]{3,8}\b", css) == [], "no hard-coded colour: tokens only"
    assert not re.search(r"\brgba?\(|\bhsla?\(", css)
    physical = re.findall(r"(?<![-\w])(?:margin|padding|border)-(?:left|right)\b|(?<![-\w])(?:left|right)\s*:", css)
    assert physical == [], physical
    assert "text-align: left" not in css and "text-align: right" not in css
    assert "decimal-leading-zero" in css, "the sequences are numbered 01, 02 …"
    assert "@keyframes" not in css and "animation" not in css and "opacity: 0;" not in css
    assert not re.search(r"https?://", css)
    assert scan(css) == []


def test_stylesheet_is_served(client):
    from django.contrib.staticfiles import finders

    assert finders.find("ecosystem/ecosystem.css")


def test_python_sources_have_no_forbidden_formulations():
    for path in APP.glob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert not re.search(r"\bmatching\b", text, flags=re.I), path.name
        assert "®" not in text and "@legalitalentry" not in text, path.name
