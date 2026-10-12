"""
Whole-site guards, run on EVERY registered public route (``core.public_routes``) with the gates open, and on
the reserved area for a signed-in person — in Italian, English and Arabic:

* the French-fallback markup of a prescribed text (``<span lang="fr">``) never leaks into ``<head>`` or into an
  attribute — there it would break the page instead of tagging the language;
* no French gettext source string is visible where the catalogue holds a translation (a lazy string evaluated
  at import time, a forgotten ``.mo``, a catalogue that was not loaded…);
* the same guard holds in the state the site is published in TODAY (every gate closed: blocked legal pages,
  « form unavailable » notices, 404 pages of the Phase 3 routes);
* on Arabic pages no Latin-script text is left without a ``lang`` attribute (WCAG 3.1.2 « language of
  parts »): a French or Italian fallback value must say so, for screen readers and for the bidi isolation;
* on Arabic pages every forward icon (``arrow``, ``chevron-end``) carries ``.icon--flip-rtl``;
* the language chosen on the site is kept on the language-neutral pages.

Protocol for a defect that belongs to another owner (docs/I18N_RTL.md §9): list it in a ``KNOWN_…`` table that
the main test skips, keep it visible with an ``xfail`` test whose reason starts with the defect id, and remove
both as soon as the owner has fixed it — the main test then protects the fix. Second review, 20/09/2026:
I18N-02, I18N-03, I18N-05, I18N-07, I18N-08, I18N-09 and RTL-04 were fixed by their owners; no table is left
and the tests below are plain regression tests.
"""

from __future__ import annotations

import html as html_module
import re

import pytest

from core.public_routes import all_routes

from .conftest import TRANSLATED, html_tag, located_strings, region, visible_strings
from .test_ui_translations import ARABIC_LATIN_ALLOWED

pytestmark = [pytest.mark.compliance, pytest.mark.django_db]

#: Blocked legal pages: path → msgid of the page title (written in Italian, like the rest of the legal
#: back-office). I18N-07 (fixed): the titles were built with the eager ``gettext`` at import time.
LEGAL_TITLE_MSGIDS = {
    "note-legali/": "Note legali",
    "condizioni-di-utilizzo/": "Condizioni di utilizzo",
    "avvertenze/": "Avvertenze",
}

RESERVED_AREA = (
    "espace-reserve/",
    "espace-reserve/mes-demandes/",
    "espace-reserve/mon-parcours/",
    "espace-reserve/mes-documents/",
    "espace-reserve/mes-echeances/",
    "espace-reserve/communications/",
    "compte/profil/",
    "compte/profil/suppression/",
    "compte/email/",
    "compte/password/change/",
    "compte/2fa/",
)

_FORWARD_ICONS = ("arrow", "chevron-end")
_ICON = re.compile(r'<svg class="([^"]*)"[^>]*>\s*<use href="[^"#]*#icon-([a-z-]+)"')
_MARKUP_IN_ATTRIBUTE = re.compile(r'\b[a-z-]+="[^"]*(?:<|&lt;)span\b')


@pytest.fixture
def open_site(client, seeded, legal_published, phase3_open):
    """Every gate open, so that each registered route renders its real content (forms included)."""
    return client


def _pages(client, lang: str):
    for route in all_routes():
        response = client.get(f"/{lang}/{route.path}")
        if response.status_code == 200:  # routes behind a gate that stays closed (virtual forum) answer 404
            yield route.path, response.content.decode()


def _french_sources(catalogues, lang: str) -> set[str]:
    """French msgids whose translation differs from the source: seeing one of them on a page is a leak."""
    return {e.msgid for e in catalogues[lang].values() if len(e.msgid) > 3 and e.msgstr[0] != e.msgid}


# ---------------------------------------------------------------------------------------------
# Fallback markup
# ---------------------------------------------------------------------------------------------
def _markup_problems(page: str) -> list[str]:
    head = page.split("</head>", 1)[0]
    problems = [m.group(0)[:80] for m in _MARKUP_IN_ATTRIBUTE.finditer(page)]
    if re.search(r"(?:<|&lt;)span\b", head):
        problems.append("<span> inside <head>")
    title = re.search(r"<title>(.*?)</title>", head, re.S)
    if title and re.search(r"(?:<|&lt;)[a-z]", title.group(1)):
        problems.append("markup inside <title>")
    return problems


@pytest.mark.parametrize("lang", TRANSLATED)
def test_fallback_markup_never_leaks_into_head_or_attributes(open_site, lang):
    """I18N-02 (fixed): {% locked … as var %}{{ var }} in a meta description needs ``|striptags``."""
    seen = 0
    for path, page in _pages(open_site, lang):
        seen += 1
        assert _markup_problems(page) == [], (lang, path)
        assert page.count("<head>") == 1 and page.count("</head>") == 1, (lang, path)
    assert seen >= 55


def test_the_markup_detector_sees_a_span_inside_an_attribute():
    broken = '<html><head><meta name="description" content="<span lang="fr">Texte</span>"></head><body></body></html>'
    assert _markup_problems(broken)
    assert _markup_problems("<html><head><title>&lt;span lang=fr&gt;x</title></head></html>")
    assert _markup_problems('<html><head><title>Titre</title></head><body><p lang="fr">x</p></body></html>') == []


def test_french_pages_never_need_fallback_markup(open_site):
    for path, page in _pages(open_site, "fr"):
        assert _markup_problems(page) == [], path


# ---------------------------------------------------------------------------------------------
# Untranslated interface strings
# ---------------------------------------------------------------------------------------------
def _untranslated(page: str, lang: str, french: set[str]) -> list[str]:
    return sorted(
        {
            text
            for effective, _kind, text in visible_strings(page, lang)
            if effective == lang and html_module.unescape(text) in french
        }
    )


@pytest.mark.parametrize("lang", TRANSLATED)
def test_no_french_interface_string_is_visible_on_a_translated_public_page(open_site, catalogues, lang):
    """Also I18N-03 (fixed): a French CMS value equal to a gettext source must carry ``lang="fr"``."""
    french = _french_sources(catalogues, lang)
    assert len(french) > 1000
    leaks = {}
    for path, page in _pages(open_site, lang):
        found = _untranslated(page, lang, french)
        if found:
            leaks[path] = found
    assert leaks == {}


@pytest.mark.parametrize("lang", TRANSLATED)
def test_no_french_interface_string_is_visible_in_the_reserved_area(open_site, catalogues, person_user, lang):
    open_site.force_login(person_user)
    french = _french_sources(catalogues, lang)
    leaks = {}
    for path in RESERVED_AREA:
        response = open_site.get(f"/{lang}/{path}")
        assert response.status_code == 200, (lang, path, response.status_code)
        page = response.content.decode()
        assert f'lang="{lang}"' in html_tag(page)
        assert len(re.findall(r"<h1\b", page)) == 1, (lang, path)
        found = _untranslated(page, lang, french)
        if found:
            leaks[path] = found
    assert leaks == {}


@pytest.mark.parametrize("lang", TRANSLATED)
def test_no_french_interface_string_is_visible_while_every_gate_is_closed(client, seeded, catalogues, lang):
    """The state the site is published in today: legal pages blocked, forms unavailable, Phase 3 routes → 404."""
    french = _french_sources(catalogues, lang)
    statuses, leaks = set(), {}
    for route in all_routes():
        response = client.get(f"/{lang}/{route.path}")
        statuses.add(response.status_code)
        found = _untranslated(response.content.decode(), lang, french)
        if found:
            leaks[route.path] = found
    assert statuses == {200, 404}, "both the open pages and the 404 page of the gated routes are read"
    assert leaks == {}


def test_blocked_legal_page_titles_follow_the_page_language(client, seeded, catalogues):
    """
    I18N-07 (fixed 20/09/2026 in apps/legal/views.py): PAGE_TITLES was built with the eager ``gettext`` at
    import time, so the <h1> and <title> of the blocked legal pages were frozen in the language active when
    the URLconf was first imported (French) on the it / en / ar sites. The titles are now lazy.
    """
    for lang in TRANSLATED:
        for path, msgid in LEGAL_TITLE_MSGIDS.items():
            expected = catalogues[lang][(None, msgid)].msgstr[0]
            page = client.get(f"/{lang}/{path}").content.decode()
            title = re.search(r"<h1\b[^>]*>(.*?)</h1>", region(page, "main"), re.S).group(1)
            assert html_module.unescape(re.sub(r"<[^>]+>", "", title)).strip() == expected, (lang, path)
            assert html_module.unescape(re.search(r"<title>(.*?)</title>", page, re.S).group(1)).startswith(expected)


def test_no_module_level_constant_is_translated_at_import_time():
    """
    The defect behind I18N-07, checked statically on every application module: a call of the EAGER ``gettext``
    (``ngettext``, ``pgettext``) outside a function body is evaluated once, at import time, in whichever language
    happens to be active — every visitor then reads that language. Module-level strings need ``gettext_lazy``.
    """
    import ast

    from .conftest import ROOT

    eager_names = {"gettext", "ngettext", "pgettext", "npgettext"}
    offenders = []
    for path in sorted((ROOT / "apps").rglob("*.py")):
        if {"tests", "migrations"} & set(path.parts):
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        eager = {
            alias.asname or alias.name
            for node in ast.walk(tree)
            if isinstance(node, ast.ImportFrom) and node.module == "django.utils.translation"
            for alias in node.names
            if alias.name in eager_names
        }
        if not eager:
            continue
        pending = list(tree.body)
        while pending:
            node = pending.pop()
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
                # Only what runs at import time: decorators and default values.
                defaults = [*node.args.defaults, *[d for d in node.args.kw_defaults if d is not None]]
                pending += [*defaults, *getattr(node, "decorator_list", [])]
                continue
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in eager:
                offenders.append(f"{path.relative_to(ROOT).as_posix()}:{node.lineno}")
            pending += list(ast.iter_child_nodes(node))
    assert offenders == [], "use gettext_lazy for strings evaluated at import time"


def test_the_leak_detector_sees_an_untranslated_string(catalogues):
    french = _french_sources(catalogues, "ar")
    page = (
        '<html lang="ar"><body><p>Retour à l’accueil</p><p lang="fr">Espace réservé</p>'
        '<a aria-label="Se connecter" href="#">x</a><svg><title>Accueil</title></svg></body></html>'
    )
    assert _untranslated(page, "ar", french) == ["Retour à l’accueil", "Se connecter"]


def test_profile_page_shows_no_technical_role_identifier(open_site, person_user, catalogues):
    """I18N-09 (fixed 20/09/2026 by accounts): « Rôles » listed the group names (« role:person »)."""
    open_site.force_login(person_user)
    for lang in TRANSLATED:
        main = region(open_site.get(f"/{lang}/compte/profil/").content.decode(), "main")
        assert "role:" not in main, lang
        assert catalogues[lang][(None, "Personne")].msgstr[0] in main, lang


# ---------------------------------------------------------------------------------------------
# Language of parts (WCAG 3.1.2): Latin-script text on an Arabic page carries its own ``lang``
# ---------------------------------------------------------------------------------------------
_ARABIC_SCRIPT = re.compile(r"[\u0600-\u06FF]")
_LATIN_WORD = re.compile(r"[A-Za-zÀ-ÿ]{2,}")
_EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
#: Strings that cannot carry a ``lang`` attribute (<title>, meta description) — documented limit, §9.
_NO_LANG_POSSIBLE = {"title", "@description", "head"}


def _untagged_latin(page: str, keep_source) -> list[tuple[str, str]]:
    """``[(where, text), …]`` — Latin-script strings that inherit ``lang="ar"`` from the page."""
    found = []
    for effective, kind, text, classes in located_strings(page, "ar"):
        if effective != "ar" or kind in _NO_LANG_POSSIBLE or _ARABIC_SCRIPT.search(text) or text in keep_source:
            continue
        if _LATIN_WORD.search(_EMAIL.sub("", ARABIC_LATIN_ALLOWED.sub("", text))):
            found.append((f"{kind}.{classes[-1]}" if classes else kind, text))
    return found


def _arabic_pages(client, person_user):
    yield from _pages(client, "ar")
    # The error summary of a public form (locked French labels), then the reserved area of a signed-in person.
    response = client.post("/ar/entreprises/recueil-des-besoins/", {})
    assert response.status_code == 200 and 'id="form-errors"' in response.content.decode()
    yield "POST entreprises/recueil-des-besoins/", response.content.decode()
    client.force_login(person_user)
    for path in RESERVED_AREA:
        yield path, client.get(f"/ar/{path}").content.decode()


def test_latin_text_on_arabic_pages_carries_its_own_lang_attribute(open_site, person_user, audit):
    """
    I18N-08 (fixed 20/09/2026): French prescribed titles, Italian legal terms and French CMS values were printed
    without ``lang`` in the breadcrumb, the local navigation, the error summary of the forms, the authority
    lists and the glossary sources — wrong screen-reader voice and no left-to-right isolation in Arabic.
    """
    untagged, pages = {}, 0
    for path, page in _arabic_pages(open_site, person_user):
        pages += 1
        found = sorted(set(_untagged_latin(page, audit.KEEP_SOURCE)))
        if found:
            untagged[path] = found
    assert pages >= 65
    assert untagged == {}, 'wrap the fallback value in an element with lang="fr" / lang="it" (or translate it)'


def test_the_language_of_parts_detector(audit):
    page = (
        '<html lang="ar"><head><title>Travail salarié · Italy Legal Entry™</title></head><body>'
        '<nav class="breadcrumbs"><ol><li><span>Travail salarié</span></li></ol></nav>'
        '<p lang="fr">Texte prescrit.</p><p>Questura</p><p>عرض مسار «Travail salarié»</p>'
        "<p>Italy Legal Entry™</p><p>person@example.test</p></body></html>"
    )
    assert _untagged_latin(page, audit.KEEP_SOURCE) == [("span.breadcrumbs", "Travail salarié"), ("p", "Questura")]


# ---------------------------------------------------------------------------------------------
# Semantic mirroring of forward icons
# ---------------------------------------------------------------------------------------------
def _unflipped(page: str) -> list[str]:
    return [
        f"{name}: {classes}"
        for classes, name in _ICON.findall(page)
        if name in _FORWARD_ICONS and "icon--flip-rtl" not in classes.split()
    ]


def test_forward_icons_are_mirrored_on_every_arabic_page(open_site):
    """Also RTL-04 (fixed): the Espace Personnes arrows were rendered without ``icon--flip-rtl``."""
    icons = 0
    for path, page in _pages(open_site, "ar"):
        icons += sum(1 for _classes, name in _ICON.findall(page) if name in _FORWARD_ICONS)
        assert _unflipped(page) == [], path
    assert icons >= 50, "the forward icons of the design system were not found: has the sprite markup changed?"


# ---------------------------------------------------------------------------------------------
# Language continuity on the language-neutral pages
# ---------------------------------------------------------------------------------------------
def test_language_neutral_pages_follow_the_language_cookie(open_site, person_user):
    """/documents/ lives outside i18n_patterns: the ``ile_language`` cookie decides, then Accept-Language."""
    open_site.force_login(person_user)
    open_site.post("/i18n/setlang/", {"language": "ar", "next": "/ar/espace-reserve/"})
    page = open_site.get("/documents/", HTTP_ACCEPT_LANGUAGE="fr").content.decode()
    assert 'lang="ar"' in html_tag(page) and 'dir="rtl"' in html_tag(page)
    assert "Mes documents" not in region(page, "main")


def test_language_chosen_by_browsing_is_kept_on_language_neutral_pages(open_site, person_user):
    """
    I18N-05 (fixed 20/09/2026, core.middleware.LanguageCookieMiddleware): the switcher is a list of links, so
    the cookie is written when a prefixed page is served — a visitor who reads the site in Arabic with a French
    browser gets /documents/ (outside i18n_patterns) in Arabic.
    """
    from django.conf import settings

    open_site.force_login(person_user)
    response = open_site.get("/ar/espace-reserve/", HTTP_ACCEPT_LANGUAGE="fr")
    assert response.status_code == 200
    cookie = response.cookies[settings.LANGUAGE_COOKIE_NAME]
    assert cookie.value == "ar" and cookie["samesite"] == "Lax" and cookie["httponly"]
    page = open_site.get("/documents/", HTTP_ACCEPT_LANGUAGE="fr").content.decode()
    assert 'lang="ar"' in html_tag(page)


def test_language_cookie_is_only_written_for_a_published_language_and_a_served_page(client, seeded):
    from django.conf import settings

    name = settings.LANGUAGE_COOKIE_NAME
    assert name not in client.get("/ar/cette-page-n-existe-pas/").cookies, "a 404 must not switch the language"
    assert name not in client.get("/de/").cookies
    assert name not in client.get("/robots.txt").cookies
    assert client.get("/it/").cookies[name].value == "it"
    assert name not in client.get("/it/le-projet/").cookies, "the cookie is not rewritten when it already matches"
