"""
Four-language routing: /it/ /fr/ /en/ /ar/ prefixes, html lang/dir, language negotiation, the
``ile_language`` cookie, the language switcher and hreflang alternates.
"""

from __future__ import annotations

import re

import pytest
from django.conf import settings

from core.public_routes import gated_routes, ungated_paths

from .conftest import LANGS, html_tag, region

pytestmark = pytest.mark.django_db


def _assert_lang_dir(html: str, lang: str, where: str) -> None:
    tag = html_tag(html)
    assert f'lang="{lang}"' in tag, (where, tag)
    assert f'dir="{"rtl" if lang == "ar" else "ltr"}"' in tag, (where, tag)


def test_settings_describe_the_four_language_architecture():
    assert [code for code, _name in settings.LANGUAGES] == ["it", "fr", "en", "ar"]
    assert settings.LANGUAGE_CODE == "fr"  # ADR-004: French is the source / fallback language
    assert settings.RTL_LANGUAGES == {"ar"}
    assert settings.LANGUAGE_COOKIE_NAME == "ile_language"
    assert settings.USE_I18N is True
    middleware = settings.MIDDLEWARE
    assert middleware.index("django.contrib.sessions.middleware.SessionMiddleware") < middleware.index(
        "django.middleware.locale.LocaleMiddleware"
    )
    assert middleware.index("django.middleware.locale.LocaleMiddleware") < middleware.index(
        "django.middleware.common.CommonMiddleware"
    )
    assert any(str(path).endswith("locale") for path in settings.LOCALE_PATHS)


@pytest.mark.parametrize("lang", LANGS)
def test_every_ungated_public_route_renders_in_the_language(client, seeded, lang):
    paths = ungated_paths()
    assert len(paths) >= 25
    for path in paths:
        response = client.get(f"/{lang}/{path}")
        assert response.status_code == 200, (lang, path, response.status_code)
        assert response.headers["Content-Language"] == lang, (lang, path)
        _assert_lang_dir(response.content.decode(), lang, f"/{lang}/{path}")


@pytest.mark.parametrize("lang", LANGS)
def test_every_phase3_route_renders_in_the_language_once_the_gate_opens(client, seeded, phase3_open, lang):
    routes = [route for route in gated_routes() if route.requires_gate == "phase3_public"]
    assert len(routes) >= 30
    for route in routes:
        response = client.get(f"/{lang}/{route.path}")
        assert response.status_code == 200, (lang, route.path, response.status_code)
        _assert_lang_dir(response.content.decode(), lang, f"/{lang}/{route.path}")


def test_phase3_routes_stay_closed_in_every_language_before_the_gate(client, seeded, before_phase3):
    for lang in LANGS:
        assert client.get(f"/{lang}/faq/").status_code == 404, lang
        assert client.get(f"/{lang}/attention-aux-fraudes/").status_code == 404, lang


def test_a_path_without_language_prefix_is_redirected_never_served(client, seeded):
    response = client.get("/le-projet/", HTTP_ACCEPT_LANGUAGE="ar")
    assert (response.status_code, response.headers["Location"]) == (302, "/ar/le-projet/")
    response = client.get("/le-projet/", HTTP_ACCEPT_LANGUAGE="de")
    assert (response.status_code, response.headers["Location"]) == (302, "/fr/le-projet/")
    # A language the site does not publish is not a prefix: nothing is served under it.
    assert client.get("/de/").status_code == 404
    assert client.get("/es/le-projet/").status_code == 404


@pytest.mark.parametrize(
    ("header", "expected"),
    [("ar", "/ar/"), ("it-IT,it;q=0.9,en;q=0.5", "/it/"), ("en-GB", "/en/"), ("de-DE,de;q=0.9", "/fr/"), ("", "/fr/")],
)
def test_root_redirects_to_the_negotiated_language(client, header, expected):
    response = client.get("/", HTTP_ACCEPT_LANGUAGE=header)
    assert response.status_code == 302
    assert response.headers["Location"] == expected


def test_language_cookie_wins_over_the_browser_language(client):
    client.cookies[settings.LANGUAGE_COOKIE_NAME] = "ar"
    response = client.get("/", HTTP_ACCEPT_LANGUAGE="it")
    assert response.headers["Location"] == "/ar/"
    client.cookies[settings.LANGUAGE_COOKIE_NAME] = "xx"  # tampered cookie → negotiation falls back
    assert client.get("/", HTTP_ACCEPT_LANGUAGE="it").headers["Location"] == "/it/"


def test_set_language_view_stores_the_cookie_and_translates_the_url(client, seeded):
    response = client.post("/i18n/setlang/", {"language": "ar", "next": "/fr/le-projet/"})
    assert response.status_code == 302
    assert response.headers["Location"] == "/ar/le-projet/"
    cookie = response.cookies[settings.LANGUAGE_COOKIE_NAME]
    assert cookie.value == "ar"
    assert cookie["samesite"] == "Lax"
    assert client.get("/").headers["Location"] == "/ar/"


def test_set_language_refuses_an_external_redirect_and_changes_nothing_on_get(client, seeded):
    response = client.post("/i18n/setlang/", {"language": "it", "next": "https://evil.example/it/"})
    assert response.status_code == 302
    assert "evil.example" not in response.headers["Location"]
    response = client.get("/i18n/setlang/", {"language": "ar", "next": "/fr/"})
    assert response.status_code == 302
    assert settings.LANGUAGE_COOKIE_NAME not in response.cookies, "a GET must never switch the language"
    response = client.post("/i18n/setlang/", {"language": "xx", "next": "/fr/"})
    assert settings.LANGUAGE_COOKIE_NAME not in response.cookies, "unknown language codes are ignored"


def test_set_language_is_csrf_protected(seeded):
    from django.test import Client

    strict = Client(enforce_csrf_checks=True)
    assert strict.post("/i18n/setlang/", {"language": "ar", "next": "/fr/"}).status_code == 403


@pytest.mark.parametrize("lang", LANGS)
def test_language_switcher_links_to_the_same_page_in_the_four_languages(client, seeded, lang):
    html = client.get(f"/{lang}/le-projet/").content.decode()
    # The segmented control of design V4 (components/language_segmented.html): the first one on the
    # page is the institutional bar's; the drawer carries a second, identical one.
    switcher = re.search(r'<nav class="lang-seg".*?</nav>', html, re.S).group(0)
    for code, name in settings.LANGUAGES:
        direction = "rtl" if code == "ar" else "ltr"
        link = re.search(rf'<a class="lang-seg__link" href="/{code}/le-projet/"[^>]*>', switcher)
        assert link, (lang, code)
        assert f'lang="{code}"' in link.group(0) and f'hreflang="{code}"' in link.group(0)
        assert f'dir="{direction}"' in link.group(0)
        assert name in switcher  # each language is named in its own language (endonym)
    current = re.findall(r'<a class="lang-seg__link"[^>]*aria-current="true"[^>]*>', switcher)
    assert len(current) == 1 and f'hreflang="{lang}"' in current[0]


@pytest.mark.parametrize("lang", LANGS)
def test_hreflang_alternates_and_canonical_follow_the_language(client, seeded, lang):
    html = client.get(f"/{lang}/le-projet/").content.decode()
    for code in LANGS:
        assert re.search(rf'<link rel="alternate" hreflang="{code}" href="http://testserver/{code}/le-projet/">', html)
    assert 'hreflang="x-default"' in html
    assert f'<link rel="canonical" href="http://testserver/{lang}/le-projet/">' in html


def test_menu_links_carry_the_prefix_of_the_page_language(client, seeded):
    for lang in LANGS:
        header = region(client.get(f"/{lang}/").content.decode(), "header")
        # The language control lives in the header (design V4): its links point, by definition, at
        # the OTHER languages. They carry hreflang, and only they may.
        header = re.sub(r'<a [^>]*hreflang="[^"]*"[^>]*>', "", header)
        hrefs = [href for href in re.findall(r'href="(/[^"]*)"', header) if not href.startswith("/static/")]
        assert hrefs, lang
        assert all(href.startswith(f"/{lang}/") for href in hrefs), (lang, hrefs)


def test_only_technical_cookies_are_set_when_browsing_in_arabic(client, seeded):
    response = client.get("/ar/")
    assert set(response.cookies) <= {"csrftoken", "sessionid", settings.LANGUAGE_COOKIE_NAME}
