"""
The service pages on design V5 — «le pagine di servizio» (W3-F2 step 2; docs/design-v5/V5_4_EXECUTION_PLAN.md §3.5
item 2): the error pages and the account pages, in their sources and as the server renders them.

* 400 and 500 are drawn with NO database and NO context processor (core.views renders them without the request, as
  Django's own `bad_request` and `server_error` do), and answer a bare page of the same words if even their template
  fails; what they show of the request is its correlation id, nothing else;
* every error page — 400, 403, 404, 410, 429, 500 — in the four languages: the status as the head's label, one h1 in
  the request's language, one primary, the way back, the recovery navigation, «who can help me», the error pages'
  sheet; no arrow glyph, no path, no stack; the door at rest first in the page (the owner's door stage with the key out
  of the lock, static files only, decorative, no light) — the review's M1;
* the account pages share one frame: the trail, the account's sections with the current one said, at most one
  primary, the danger button behind its own confirmation page, the export's opt-out of the busy face (W1-D); allauth's
  second primaries are secondaries on the management layout only, the entrance's elements are untouched;
* the partial is page-only CSS, tokens only, logical, on the 4 px line; the rules it replaced are gone from main.css;
  the error pages' sheet imports it with the door stage, never main.css; the profile's personal fields say what they
  are for (WCAG 1.3.5, the accessibility check's A2).
"""

from __future__ import annotations

import copy
import html as html_lib
import re
import time
from pathlib import Path

import pytest
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, override_settings
from django.utils import translation
from django.utils.translation import gettext

from core import views as core_views

ROOT = Path(__file__).resolve().parents[2]
PARTIAL = ROOT / "static" / "css" / "v5" / "_servizio.css"
ENTRY = ROOT / "apps" / "cms" / "static" / "cms" / "servizio.css"
ERRORS_ENTRY = ROOT / "apps" / "cms" / "static" / "cms" / "errori.css"
TEMPLATES = ROOT / "templates"
LANGS = ["fr", "it", "en", "ar"]

#: the error pages' words, the msgids of the four catalogues (templates/errors/<status>.html)
TITLES = {
    400: "Requête invalide",
    403: "Accès non autorisé",
    404: "Page introuvable",
    410: "Cette page n’existe plus",
    429: "Trop de requêtes",
    500: "Erreur technique",
}

#: the frames that load the account pages' sheet (cms/servizio.css), and the error pages' frames, which load theirs
#: (cms/errori.css: the same partial and the door stage)
LOADERS = [
    "allauth/layouts/base.html",
    "accounts/delete_done.html",
]
ERROR_FRAMES = [
    "errors/base_error.html",
    "errors/standalone.html",
]


def explode(request):  # pragma: no cover - its whole point is never to run
    """A context processor that fails: a page that needs none never calls it."""
    raise AssertionError("a context processor ran on a page that must need none")


def _read(path: Path) -> str:
    return path.read_bytes().decode("utf-8")


def _main(html: str) -> str:
    return html.split("<main", 1)[1].split("</main>", 1)[0]


def _has(text: str, html: str) -> bool:
    """The words as the template writes them — autoescaped (a straight apostrophe becomes &#x27;) or not."""
    return text in html or html_lib.escape(text, quote=True) in html


def _request(lang: str, path: str = "/") -> object:
    request = RequestFactory().get(f"/{lang}{path}")
    request.request_id = "f20400c3d2d446a6a34878e7c08adf2a"
    return request


def _door(main: str) -> str:
    """The door at rest, as the page draws it (templates/errors/_door.html)."""
    match = re.search(
        r'<div class="door-stage sig error-page__door" aria-hidden="true">.*?</svg></span>\s*</div>', main, re.S
    )
    assert match, "the door at rest"
    return match.group(0)


def _assert_the_door_at_rest(main: str) -> None:
    door = _door(main)
    assert main.count("error-page__door") == 1, "one door"
    assert main.index("error-page__door") < main.index('class="error-page__head"'), "first: above the label on a phone"
    # the owner's photograph as served (the home's and the login's registration), static files only
    assert (
        '<picture class="door-stage__photo"><source type="image/avif" srcset="/static/brand/v5/doorway-arch-400' in door
    )
    assert '<img src="/static/brand/v5/doorway-arch-400.webp" width="400" height="533" alt="" decoding="async">' in door
    # the arch, the inner door, the three steps, the outline — and the key out of the lock
    for part in ("doorway__arch-inset", "doorway__inner", "doorway__steps", 'class="doorway__arch"'):
        assert part in door, part
    assert re.search(r'<g class="doorway__steps">(.*?)</g>', door, re.S).group(1).count("<rect ") == 3, "three steps"
    assert 'class="sig__l door-stage__key error-page__key"' in door
    # at rest: no light (no glow at the keyhole, no lit frame, no lit steps), nothing focusable
    for light in ("doorway__glow", "door-stage__frame", "door-stage__step", "sig__turn", "data-loader"):
        assert light not in door, light
    assert not re.search(r"<(a|button|input)\b|tabindex", door), "decorative: nothing to reach"


# ---------------------------------------------------------------------------------------------- 400 and 500


@pytest.mark.parametrize("status", [400, 500])
def test_400_and_500_render_without_the_database_or_a_context_processor(status):
    """No `django_db` mark: a query raises. The exploding processor proves no processor runs."""
    templates = copy.deepcopy(settings.TEMPLATES)
    templates[0]["OPTIONS"]["context_processors"] = [
        *templates[0]["OPTIONS"]["context_processors"],
        "tests.frontend.test_service_pages_w3_f2.explode",
    ]
    view = getattr(core_views, f"error_{status}")
    with override_settings(TEMPLATES=templates), translation.override("fr"):
        response = view(_request("fr", "/une-adresse/"))
    html = response.content.decode()
    assert response.status_code == status
    assert '<html lang="fr" dir="ltr"' in html and html.count("<h1") == 1
    assert f'<h1 id="error-title" class="error-page__title">{TITLES[status]}</h1>' in html
    assert f'<p class="error-page__code" aria-hidden="true">Erreur {status}</p>' in html
    assert "css/dist/main.css" in html and "css/dist/cms/errori.css" in html, "the bundle and the error pages' sheet"
    assert 'class="skip-link"' in html and "data-history-back" in html and 'href="/fr/"' in html
    _assert_the_door_at_rest(_main(html))
    assert f"mailto:{settings.ILE['PUBLIC_CONTACT_EMAIL']}" in html, "the address from settings, not the database"
    # nothing that reads the database: no menu, no switch of language, no reserved-area entrance
    for part in ("main-nav", "site-header__end", "lang-seg", "utility-bar", "site-footer"):
        assert part not in html, part
    reference = "f20400c3d2d446a6a34878e7c08adf2a"
    assert (reference in html) is (status == 500), "the 500 gives the request's correlation id, the 400 nothing"


@pytest.mark.parametrize("status", [400, 500])
def test_a_self_sufficient_page_whose_template_fails_answers_a_bare_page_of_its_own_words(status, monkeypatch):
    def broken(*args, **kwargs):
        raise RuntimeError("manifest entry lost: secret/detail.css")

    monkeypatch.setattr(core_views.loader, "render_to_string", broken)
    with translation.override("ar"):
        response = getattr(core_views, f"error_{status}")(_request("ar", "/x/"))
        title = gettext(TITLES[status])
    html = response.content.decode()
    assert response.status_code == status
    assert '<html lang="ar" dir="rtl">' in html and f"<h1>{html_lib.escape(title)}</h1>" in html
    assert "secret" not in html and "manifest" not in html and "Traceback" not in html, "the failure is never told"


# ---------------------------------------------------------------------------------------------- every status, four languages


def _render_error(status: int, lang: str, client) -> tuple[int, str]:
    """The page as a visitor meets it: the real paths for 404 and 410, the handlers for the others."""
    if status == 404:
        response = client.get(f"/{lang}/page-inexistante-w3f2/")
    elif status == 410:
        response = client.get("/hello-world/", HTTP_ACCEPT_LANGUAGE=lang)
    else:
        request = _request(lang)
        request.user = AnonymousUser()
        with translation.override(lang):
            response = getattr(core_views, f"error_{status}")(request)
    return response.status_code, response.content.decode()


@pytest.mark.django_db
@pytest.mark.parametrize("lang", LANGS)
@pytest.mark.parametrize("status", [400, 403, 404, 410, 429, 500])
def test_every_error_page_is_one_quiet_page_in_the_request_s_language(client, seeded, status, lang):
    code, html = _render_error(status, lang, client)
    assert code == status
    direction = "rtl" if lang == "ar" else "ltr"
    assert f'<html lang="{lang}" dir="{direction}"' in html
    with translation.override(lang):
        title, label = gettext(TITLES[status]), f"{gettext('Erreur')} {status}"
        back, recovery = gettext("Retour à l’accueil"), gettext("Navigation de secours")
        helpline, way_on = gettext("Besoin d’aide ? Écrivez-nous :"), gettext("Poursuivre la navigation")
    if lang != "fr":
        assert title != TITLES[status], f"{lang}: the catalogue holds the title"
    main = _main(html)
    assert re.findall(r"<h1\b[^>]*>(.*?)</h1>", html, re.S) == [html_lib.escape(title, quote=True)]
    assert f'<p class="error-page__code" aria-hidden="true">{label}</p>' in main, "the status as the head's label"
    assert main.count("btn--primary") == 1, "one primary"
    assert _has(back, main) and f'aria-label="{recovery}"' in main and _has(way_on, main)
    assert _has(helpline, main) and 'class="aiuto"' in main and "mailto:" in main
    assert "css/dist/cms/errori.css" in html and "css/dist/cms/servizio.css" not in html
    _assert_the_door_at_rest(main)
    # the policy's English name says so (WCAG 3.1.2; the accessibility check's A4)
    assert '" lang="en">Privacy Policy</a>' in main
    # one forward arrow, on the one primary (it goes on: home, or the sign-in); the way back has none
    primary = re.search(r'<a class="btn btn--primary btn--arrow"[^>]*>(.*?)</a>', main, re.S)
    assert primary and "icon--flip-rtl" in primary.group(1), "the primary carries the forward arrow"
    assert main.count("icon--flip-rtl") == 1 and "link-arrow" not in main, "one arrow a block"
    assert "Traceback" not in html and "page-inexistante-w3f2" not in main, "no stack, no path"


@pytest.mark.django_db
def test_the_403_offers_the_sign_in_first_to_a_person_who_is_not_signed_in(rf, seeded, person_user):
    request = rf.get("/fr/")
    request.user = AnonymousUser()
    with translation.override("fr"):
        html = core_views.error_403(request).content.decode()
    actions = _main(html).split('class="error-page__actions"', 1)[1].split("</div>", 1)[0]
    assert re.findall(r'class="btn (btn--\w+)[^"]*"', actions) == ["btn--primary", "btn--secondary"]
    assert 'class="btn btn--primary btn--arrow" href="/fr/compte/login/?next=/fr/"' in actions, "the one primary"
    # it carries the refused address, encoded (allauth goes there after the sign-in, and only to this site's)
    refused = rf.get("/fr/espace-reserve/x/", {"vue": "a&b"})
    refused.user = AnonymousUser()
    with translation.override("fr"):
        html = core_views.error_403(refused).content.decode()
    assert 'href="/fr/compte/login/?next=/fr/espace-reserve/x/%3Fvue%3Da%2526b"' in html, "the review's m9"
    request.user = person_user
    with translation.override("fr"):
        html = core_views.error_403(request).content.decode()
    actions = _main(html).split('class="error-page__actions"', 1)[1].split("</div>", 1)[0]
    assert "/compte/login/" not in actions and "data-history-back" in actions, "a signed-in person goes back"


def test_the_error_templates_are_one_family_and_the_two_frames_need_nothing_else():
    for status in (403, 404, 410, 429):
        assert _read(TEMPLATES / "errors" / f"{status}.html").startswith('{% extends "errors/base_error.html" %}')
    for status in (400, 500):
        assert _read(TEMPLATES / "errors" / f"{status}.html").startswith('{% extends "errors/standalone.html" %}')
    standalone = re.sub(
        r"\{% comment %\}.*?\{% endcomment %\}", "", _read(TEMPLATES / "errors" / "standalone.html"), flags=re.S
    )
    assert "{% extends" not in standalone and "<!DOCTYPE html>" in standalone, "a document of its own"
    for reads_the_database in ("site.settings", "user.", "{% flag", "main_menu", '{% include "partials/'):
        assert reads_the_database not in standalone, reads_the_database
    for name in ("base_error.html", "standalone.html", "_actions.html", "_way_on.html"):
        source = _read(TEMPLATES / "errors" / name)
        assert "\r" not in source and not re.search(r"\sstyle=|<style|<script>", source), name


# ---------------------------------------------------------------------------------------------- the account pages


def _nav(html: str) -> str:
    return html.split('<nav class="conto-nav"', 1)[1].split("</nav>", 1)[0]


ACCOUNT_PAGES = [
    # (path, the section whose link is current, its aria-current, the trail's current words)
    ("/fr/compte/profil/", "Profil", "page", "Mon compte"),
    ("/fr/compte/profil/suppression/", "Profil", "true", "Supprimer mon compte"),
    ("/fr/compte/email/", "Adresses e-mail", "page", "Adresses e-mail"),
    ("/fr/compte/password/change/", "Mot de passe", "page", "Mot de passe"),
    ("/fr/compte/2fa/", "Authentification à deux facteurs", "page", "Authentification à deux facteurs"),
    ("/fr/compte/logout/", None, None, "Se déconnecter"),
]


@pytest.mark.django_db
@pytest.mark.parametrize(("path", "section", "current", "trail"), ACCOUNT_PAGES)
def test_every_account_page_stands_in_one_frame(client, seeded, person_user, path, section, current, trail):
    client.force_login(person_user)
    response = client.get(path)
    html = response.content.decode()
    assert response.status_code == 200
    assert 'class="container conto"' in html and "css/dist/cms/servizio.css" in html
    assert html.count("<h1") == 1 and 'name="robots" content="noindex' in html
    nav = _nav(html)
    marked = re.findall(r'<a class="conto-nav__link" href="[^"]+" aria-current="(\w+)">([^<]+)</a>', nav)
    assert marked == ([(current, section)] if section else []), marked
    crumbs = html.split('class="breadcrumbs container"', 1)[1].split("</nav>", 1)[0]
    assert re.search(rf'aria-current="page"><span>{re.escape(trail)}</span>', crumbs), crumbs
    assert "Espace réservé" in crumbs, "the account belongs to the reserved area"
    assert _main(html).count("btn--primary") <= 1, "one primary at most"
    assert 'class="account-menu__list"' not in _main(html), "the header menu's class names never draw the page"


@pytest.mark.django_db
def test_the_profile_keeps_its_contract(client, seeded, person_user):
    client.force_login(person_user)
    main = _main(client.get("/fr/compte/profil/").content.decode())
    export = re.search(r'<form\b[^>]*action="/fr/compte/profil/export/"[^>]*>', main).group(0)
    assert 'data-loader="none"' in export and "data-single-submit" not in export, "an attachment never waits"
    assert '<a class="btn btn--danger" href="/fr/compte/profil/suppression/">' in main, (
        "the danger button, its own page"
    )
    assert 'href="/documents/"' in main and 'class="conto-facts"' in main
    assert (
        main.count("btn--primary") == 1 and "Enregistrer" in main.split("btn--primary", 1)[1].split("</button>", 1)[0]
    )


@pytest.mark.django_db
def test_the_deletion_is_confirmed_on_its_own_page_with_the_destructive_answer_last(client, seeded, person_user):
    client.force_login(person_user)
    main = _main(client.get("/fr/compte/profil/suppression/").content.decode())
    assert 'class="notice notice--warning"' in main and "Cette action est définitive." in main
    actions = main.split('class="form__actions"', 1)[1].split("</div>", 1)[0]
    assert actions.index("Annuler") < actions.index("Confirmer la suppression"), "the destructive action last"
    assert '<button type="submit" class="btn btn--danger">' in actions and "btn--primary" not in main
    assert 'type="password"' in main and 'type="checkbox"' in main, "the password and the box confirm"


@pytest.mark.django_db
def test_allauth_s_second_primary_is_a_secondary_on_the_management_layout(client, seeded, person_user):
    from allauth.account.models import EmailAddress

    EmailAddress.objects.create(user=person_user, email=person_user.email, verified=True, primary=True)
    client.force_login(person_user)
    main = _main(client.get("/fr/compte/email/").content.decode())
    assert re.search(r'<button class="btn btn--secondary"[^>]* name="action_primary"', main)
    assert re.search(r'<button class="btn btn--danger"[^>]* name="action_remove"', main)
    assert (
        re.search(r'<button class="btn btn--primary"[^>]* name="action_add"', main) and main.count("btn--primary") == 1
    )


def test_the_management_button_maps_the_recovery_codes_second_primary(db):
    from django.template.loader import render_to_string
    from django.urls import reverse

    generate = reverse("mfa_generate_recovery_codes")
    cases = [
        ({"href": generate, "tags": []}, "btn--secondary"),
        ({"href": "/fr/compte/2fa/recovery-codes/download/", "tags": []}, "btn--primary"),
        ({"type": "submit", "name": "action_primary", "tags": []}, "btn--secondary"),
        ({"type": "submit", "tags": ["danger", "delete"]}, "btn--danger"),
        ({"type": "submit", "tags": ["secondary"]}, "btn--secondary"),
    ]
    for attrs, variant in cases:
        out = render_to_string("allauth/elements/button__manage.html", {"attrs": attrs, "slots": {"default": ["x"]}})
        assert f'class="btn {variant}"' in out, (attrs, out)
    # the entrance keeps allauth's mapping as it was (W2-B's pages are not this family's)
    entrance = render_to_string(
        "allauth/elements/button.html", {"attrs": {"href": generate, "tags": []}, "slots": {"default": ["x"]}}
    )
    assert 'class="btn btn--primary"' in entrance


@pytest.mark.django_db
def test_the_authenticator_s_set_up_stands_in_the_frame(client, seeded, person_user):
    from allauth.account.models import EmailAddress

    EmailAddress.objects.create(user=person_user, email=person_user.email, verified=True, primary=True)
    client.force_login(person_user)
    session = client.session
    session["account_authentication_methods"] = [{"method": "password", "at": time.time(), "email": person_user.email}]
    session.save()
    response = client.get("/fr/compte/2fa/totp/activate/")
    html = response.content.decode()
    assert response.status_code == 200
    main = _main(html)
    assert 'class="account-page__img"' in main and 'id="authenticator_secret"' in main
    assert main.count("btn--primary") == 1 and 'aria-current="true"' in _nav(html)


# ---------------------------------------------------------------------------------------------- the sheet


def test_every_service_page_loads_its_page_sheet():
    for name in LOADERS:
        source = _read(TEMPLATES / name)
        assert "{% static 'css/dist/cms/servizio.css' %}" in source, name
        assert "{% static 'css/dist/cms/errori.css' %}" not in source, name
    for name in ERROR_FRAMES:
        source = _read(TEMPLATES / name)
        assert "{% static 'css/dist/cms/errori.css' %}" in source, name
        assert "{% static 'css/dist/cms/servizio.css' %}" not in source, name
        assert '{% include "errors/_door.html" %}' in source, name
    for name in ("accounts/profile.html", "accounts/delete_request.html"):
        assert _read(TEMPLATES / name).startswith('{% extends "allauth/layouts/manage.html" %}'), name


def test_the_partial_is_page_only_css_imported_by_its_entries():
    assert '@import url("../css/v5/_servizio.css");' in _read(ENTRY), (
        "the entry imports the partial from the collected tree"
    )
    errors = re.findall(r'@import url\("([^"]+)"\);', _read(ERRORS_ENTRY))
    assert errors == ["../css/v5/_door.css", "../css/v5/_servizio.css"], "the door stage, then the service pages' rules"
    main = _read(ROOT / "static" / "css" / "main.css")
    assert "_servizio.css" not in main and "_door.css" not in main, "page-only CSS never enters main.css"
    assert "_door.css" not in _read(ENTRY), "the account pages carry no door (V5.8: a surface's CSS where it is used)"
    for name in ("servizio.css", "errori.css"):
        assert (ROOT / "static" / "css" / "dist" / "cms" / name).is_file(), "npm run build:css"


def test_the_door_at_rest_is_static_never_mirrored_and_seated_by_the_errors_sheet():
    """The key out of the lock: the stage's key box moved onto the threshold and turned on its side; nothing moves,
    nothing is lit; the seat (the head's end seat from 64rem) follows the page while the stage stays left to right."""
    css = re.sub(r"/\*.*?\*/", "", _read(ERRORS_ENTRY), flags=re.S)
    key = re.search(r"\.error-page__door \.error-page__key \{([^}]*)\}", css).group(1)
    assert "--x: 429.333;" in key and "--y: 414.467;" in key and "transform: rotate(90deg);" in key
    for motion in ("animation", "transition", "@keyframes", "--door-frame", "--door-steps", "will-change"):
        assert motion not in css, motion
    assert re.search(r"@media \(min-width: 64rem\) \{.*?\.error-page__door \{[^}]*grid-column: 9 / -1;", css, re.S)
    assert '[dir="rtl"] .error-page__door' in css, "the arch pulled onto the reading edge in either direction"
    assert not re.search(r"#[0-9a-fA-F]{3,8}\b|rgba?\(|gradient\(", css), "tokens only"
    assert not re.search(r"(?<![\w-])(margin|padding|border|inset)-(left|right)\s*:|(?<![\w-])(left|right)\s*:", css)
    door = _read(TEMPLATES / "errors" / "_door.html")
    assert "{% static 'brand/v5/doorway-arch-400.webp' %}" in door and "{% url" not in door and "{% if" not in door, (
        "static files only: the 400 and the 500 draw it without a request"
    )


@pytest.mark.django_db
def test_the_profile_s_personal_fields_say_what_they_are_for(client, seeded, person_user):
    """WCAG 2.2 AA 1.3.5 (the accessibility check's A2), as the signup's name does."""
    client.force_login(person_user)
    main = _main(client.get("/fr/compte/profil/").content.decode())
    assert re.search(r'<input type="text" name="full_name" autocomplete="name"', main)
    assert re.search(r'<input type="tel" name="phone" autocomplete="tel" inputmode="tel"', main)
    assert re.search(r'<input type="text" name="country_of_residence" autocomplete="country-name"', main)
    assert re.search(r'<select name="preferred_language" autocomplete="language"', main)


def test_the_partial_uses_tokens_only_and_logical_properties():
    css = re.sub(r"/\*.*?\*/", "", _read(PARTIAL), flags=re.S)
    assert not re.search(r"#[0-9a-fA-F]{3,8}\b", css), "no literal colour"
    assert "rgba(" not in css and "rgb(" not in css and "gradient(" not in css
    physical = re.findall(r"(?<![\w-])(margin|padding|border)-(left|right|top|bottom)\s*:", css)
    assert physical == [], physical
    assert not re.search(r"(?<![\w-])(left|right|top|bottom)\s*:", css), "insets are logical too"
    for value in re.findall(r"line-height:\s*([0-9.]+)rem", css):
        assert (float(value) * 16) % 4 == 0, value
    tokens = _read(ROOT / "static" / "css" / "v5" / "tokens.css")
    declared = set(re.findall(r"(--[a-z0-9-]+)\s*:", tokens + css))
    used = set(re.findall(r"var\((--[a-z0-9-]+)", css))
    assert used <= declared, sorted(used - declared)
    assert "box-shadow" not in css, "no shadow at rest: hairlines before boxes"
    radii = set(re.findall(r"border-radius:\s*([^;]+);", css))
    assert radii <= {"var(--radius-sm)", "var(--radius-full)", "0"}, radii


def test_the_legacy_rules_the_service_pages_retired_are_gone():
    components = re.sub(r"/\*.*?\*/", "", _read(ROOT / "static" / "css" / "components.css"), flags=re.S)
    for gone in (
        ".error-page",
        ".js-only",
        ".account-page {",
        ".account-page__card",
        ".account-page__aside",
        ".account-page--manage",
        ".account-panel {",
        ".account-panel:first-of-type",
        ".account-panel__actions",
        ".account-page .form-field",
    ):
        assert gone not in components, gone
    # what the entrance and the console still read stays
    assert ".account-panel__title {" in components and ".account-table {" in components
    numbered = re.findall(r"^   (\d+)\. ", _read(ROOT / "static" / "css" / "components.css"), flags=re.M)
    assert "26" not in numbered, numbered
    assert not (TEMPLATES / "accounts" / "partials" / "account_menu.html").exists()
    for path in TEMPLATES.rglob("*.html"):
        assert '{% include "accounts/partials/account_menu.html"' not in _read(path), path
