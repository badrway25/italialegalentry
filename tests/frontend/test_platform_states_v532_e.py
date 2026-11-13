"""
V5.32 lane E — the platform's states, in the PLATFORM=READY round of the owner's GLOBAL SITE + PLATFORM DESIGN
COMPLETION directive of 12 Nov 2026:

- the list toolkit's count in Arabic says «no result» in words (the catalogue's zero form), never «0 نتيجة»;
- the error pages lead a signed-in person back to their own space first — only while that space is open to them, and
  never from the reserved area's own closed page, which would lead to itself;
- ONE overlay system: every <dialog> of the site is the system's (overlay.js reads `data-overlay`), and every alert of
  the platform has one anatomy — «Annuler», the safe answer that closes and takes the focus, first; the act, primary
  or destructive, last;
- (the correction round, the integration review's P2-8) a signed-in account whose console is open, refused at an
  address of the console — a 403, the Forum permanent's module that is not open yet —, stays in the console: the rail
  the address would have drawn, the console's head, the trail «<space> › <the state>», the one primary, no door;
  everyone else, everywhere else, keeps the public page.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from django.utils import translation
from django.utils.html import escape

from core import views as core_views
from core.models import SiteSettings
from forum import governance_services
from helpdesk import services as helpdesk_services

ROOT = Path(__file__).resolve().parents[2]
TEMPLATES = ROOT / "templates"
TEMPLATE_ROOTS = [TEMPLATES, *sorted((ROOT / "apps").glob("*/templates"))]
MISSING = "/{lang}/page-introuvable-v532/"
COMMENTS = re.compile(r"{%\s*comment\s*%}.*?{%\s*endcomment\s*%}|{#.*?#}|<!--.*?-->", re.S)


def _templates() -> list[Path]:
    files = [p for root in TEMPLATE_ROOTS for p in root.rglob("*.html") if "dev" not in p.relative_to(root).parts]
    assert len(files) > 100
    return sorted(files)


def _way_on(html: str) -> list[str]:
    """The hrefs of the error page's recovery links, in their order (templates/errors/_way_on.html)."""
    block = re.search(r'<ul class="error-page__links-list">(.*?)</ul>', html, re.S)
    assert block, "the way on"
    return re.findall(r'<li><a href="([^"]+)"', block.group(1))


def _crumbs(html: str) -> list[tuple[str, str]]:
    """The console bar's trail after «Accueil»: (its address, or "" for the current page; its words) per crumb."""
    bar = re.search(r'<div class="console-bar__crumbs">(.*?)</ol>', html, re.S)
    assert bar, "the console's context bar"
    crumbs = []
    for item in re.findall(r'<li class="breadcrumbs__item"[^>]*>\s*(.*?)\s*</li>', bar.group(1), re.S)[1:]:
        link = re.fullmatch(r'<a href="([^"]+)">(.*?)</a>', item, re.S)
        crumbs.append((link.group(1), link.group(2)) if link else ("", re.sub(r"<[^>]+>", "", item)))
    return crumbs


def _in_the_console(html: str) -> str:
    """The page stands in the console's frame — the rail, the console's foot — and not in the public one: no header
    of the public shell, no door at rest, not its sheet. Its <main>."""
    assert 'id="console-rail"' in html and 'class="portal-footer console__footer"' in html, "the console's frame"
    assert 'class="site-header"' not in html, "never the public shell's header"
    assert "error-page__door" not in html and "door-stage" not in html and "cms/errori.css" not in html, "no door"
    return html.split('<main id="main-content"', 1)[1].split("</main>", 1)[0]


def _in_public(html: str) -> None:
    """The public page, as before: the public shell's header, the door at rest, the way on — no rail."""
    assert 'class="site-header"' in html and "error-page__door" in html and _way_on(html)
    assert 'id="console-rail"' not in html


def _primaries(main: str) -> list[tuple[str, str]]:
    """Every primary of the page's <main>: (its address, its words)."""
    return re.findall(r'<a class="btn btn--primary[^"]*" href="([^"]+)">(.*?)</a>', main, re.S)


def _switch(enabled: bool) -> None:
    row = SiteSettings.load()
    row.reserved_area_enabled = enabled
    row.save()


# ---- the Arabic zero form ---------------------------------------------------------------------------------------------
@pytest.mark.django_db
def test_the_arabic_count_says_no_result_in_words(client, person_user):
    for subject in ("Validité de mon attestation de langue", "Traduction de mon acte de naissance"):
        helpdesk_services.open_ticket(person_user, subject=subject, question="Une question écrite par la personne.")
    client.force_login(person_user)
    html = client.get("/ar/espace-reserve/guichet/?q=introuvable").content.decode()
    found = re.search(r'<p class="lst__found" role="status">(.*?)</p>', html, re.S)
    assert found and found.group(1) == "لا توجد نتائج", "the catalogue's zero form, the words of «no result»"
    with translation.override("ar"):
        zero = translation.ngettext("%(n)s résultat", "%(n)s résultats", 0)
        many = translation.ngettext("%(n)s résultat", "%(n)s résultats", 12) % {"n": 12}
    assert zero == "لا توجد نتائج" and "12" in many, "the other forms still count"


# ---- the error pages' way back ----------------------------------------------------------------------------------------
@pytest.mark.django_db
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_a_signed_in_persons_way_on_leads_to_their_own_space_first(client, person_user, lang):
    client.force_login(person_user)
    response = client.get(MISSING.format(lang=lang))
    assert response.status_code == 404
    html = response.content.decode()
    with translation.override(lang):
        label = translation.gettext("Espace réservé")
    assert _way_on(html)[0] == f"/{lang}/espace-reserve/"
    assert f'<li><a href="/{lang}/espace-reserve/">{label}</a></li>' in html
    assert lang == "fr" or label != "Espace réservé", "the catalogue holds the words"


@pytest.mark.django_db
def test_an_anonymous_visitor_is_never_offered_the_reserved_area(client):
    response = client.get(MISSING.format(lang="fr"))
    assert response.status_code == 404
    links = _way_on(response.content.decode())
    assert "/fr/espace-reserve/" not in links and links, "the public way on, unchanged"


@pytest.mark.django_db
def test_a_closed_reserved_area_is_never_the_way_back(client, person_user, staff_user):
    _switch(False)
    client.force_login(person_user)
    assert "/fr/espace-reserve/" not in _way_on(client.get(MISSING.format(lang="fr")).content.decode())
    response = client.get("/fr/espace-reserve/")
    assert response.status_code == 503
    assert "/fr/espace-reserve/" not in _way_on(response.content.decode()), "the closed page never leads to itself"
    client.force_login(staff_user)
    assert _way_on(client.get(MISSING.format(lang="fr")).content.decode())[0] == "/fr/espace-reserve/", (
        "staff pass the switch (portal.views.portal_view), and so does their way back"
    )
    closed = (TEMPLATES / "portal" / "unavailable.html").read_text(encoding="utf-8")
    assert '{% include "errors/_way_on.html" %}' in closed and "way_console" not in closed


@pytest.mark.django_db
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_forums_closed_module_offers_the_signed_in_person_their_space(client, person_user, set_flag, lang):
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026: the V5.32
    # integration review's P2-8 — a signed-in person whose console is open no longer meets the module that is not open
    # yet in the public shell, whose way on led to their space first: the page stands inside their console — their
    # space's rail (without the Forum's rows: each would lead to the closed page), their space the trail's root —, with
    # the module's own words, its 503 and its noindex, in French and in Arabic; its one act is the Forum's public page
    # while a live edition opens it (core.gates.forum_public), else their space's «Tableau de bord» — both states read.
    from forum.seeds import seed_forum_event

    set_flag(governance_services.GOVERNANCE_FLAG, False)
    client.force_login(person_user)
    with translation.override(lang):
        url, forum = reverse("forum_governance:participation"), reverse("forum:index")
        space, module = translation.gettext("Espace réservé"), translation.gettext("Forum permanent")
        title = translation.gettext("Espace momentanément indisponible")
        act = translation.gettext("Consulter la page publique du Forum")
        dashboard = translation.gettext("Tableau de bord")
    for edition in (False, True):
        if edition:
            seed_forum_event()
        response = client.get(url)
        assert response.status_code == 503 and response["X-Robots-Tag"] == "noindex, nofollow"
        html = response.content.decode()
        main = _in_the_console(html)
        assert f'<span class="rail__space" data-rail-space>{space}</span>' in html, "their space's rail"
        assert _crumbs(html) == [(f"/{lang}/espace-reserve/", space), ("", module)], "their space, the trail's root"
        for row in ("commissions/", "propositions/", "projets/", "relation-annuelle/"):
            assert f"/forum-permanent/{row}" not in html, f"the Forum's rows are not drawn while it is closed: {row}"
        assert f'<p class="atrium__eyebrow t-label">{module}</p>' in main, "the module's name in the label's seat"
        assert re.findall(r"<h1\b[^>]*>(.*?)</h1>", html, re.S) == [title]
        one = [(forum, act)] if edition else [(f"/{lang}/espace-reserve/", dashboard)]
        assert _primaries(main) == one, "one act: the Forum's public page while it is open, else their dashboard"
        assert html.count('<meta name="robots" content="noindex, nofollow">') == 1
    assert lang == "fr" or module != "Forum permanent", "the catalogue holds the words"


# ---- the in-product refusal: inside the console (the correction round, P2-8) -----------------------------------------
@pytest.mark.django_db
@pytest.mark.parametrize("lang", ["fr", "ar"])
@pytest.mark.parametrize("page", ["guichet/confiees/", "guichet/designation/"])
def test_a_refusal_at_an_address_of_the_console_keeps_the_console(client, person_user, lang, page):
    """A person refused the professional's queue or the dispatch desk stays in their console: the rail kept, the
    console's head — the status as its label, the title, the one sentence —, the trail «Espace réservé › Accès non
    autorisé», the rail's «Tableau de bord» as the one primary at the head's reading end; no door."""
    client.force_login(person_user)
    response = client.get(f"/{lang}/espace-reserve/{page}")
    assert response.status_code == 403
    html = response.content.decode()
    main = _in_the_console(html)
    with translation.override(lang):
        title, label = translation.gettext("Accès non autorisé"), f"{translation.gettext('Erreur')} 403"
        space, dashboard = translation.gettext("Espace réservé"), translation.gettext("Tableau de bord")
        sentence = translation.gettext(
            "Vous n’avez pas les droits nécessaires pour consulter cette ressource. Si vous pensez qu’il s’agit d’une "
            "erreur, connectez-vous avec le compte approprié ou contactez-nous."
        )
    assert re.findall(r"<h1\b[^>]*>(.*?)</h1>", html, re.S) == [escape(title)], "one heading: the state's title"
    assert f'<p class="atrium__eyebrow t-label" aria-hidden="true">{label}</p>' in main, "the status as the label"
    assert f'<p class="ws-head__lead">{escape(sentence)}</p>' in main, "the one sentence"
    assert f'<span class="rail__space" data-rail-space>{space}</span>' in html, "the rail of the address's space"
    assert _crumbs(html) == [(f"/{lang}/espace-reserve/", space), ("", escape(title))]
    assert _primaries(main) == [(f"/{lang}/espace-reserve/", dashboard)], "one primary: the rail's own dashboard"
    assert "/compte/login/" not in main and "data-history-back" not in main
    assert html.count('<meta name="robots" content="noindex, nofollow">') == 1
    assert lang == "fr" or title != "Accès non autorisé", "the catalogue holds the words"


@pytest.mark.django_db
@pytest.mark.parametrize(
    ("path", "console"),
    [
        ("/fr/espace-reserve/guichet/confiees/", True),
        ("/ar/espace-reserve/forum-permanent/", True),
        ("/fr/espace-reserve", False),  # not the prefix whole
        ("/fr/espace-reservee/", False),
        ("/fr/", False),
        ("/", False),  # shorter than the prefix
        ("/documents/0b6d7e0e-5a3f-4c1e-9d2b-7f1e2a3b4c5d/", False),  # the files' address, outside the console
    ],
)
def test_the_403_chooses_its_frame_by_the_address_and_the_account(rf, person_user, staff_user, path, console):
    """errors/403.html's first line: the console's frame only for a signed-in account whose console is open, refused
    at an address of the console; the public page at every other address, for an anonymous visitor and, while the
    reserved area is switched off, for an account it is closed to — a member of staff passes the switch."""

    def refused(user) -> str:
        request = rf.get(path)
        request.user = user
        with translation.override("fr"):
            return core_views.error_403(request).content.decode()

    for html in (refused(person_user), refused(staff_user)):
        if console:
            _in_the_console(html)
        else:
            _in_public(html)
    _in_public(refused(AnonymousUser()))
    _switch(False)
    if console:
        _in_public(refused(person_user))
        _in_the_console(refused(staff_user))


@pytest.mark.django_db
def test_a_refusal_inside_the_open_forum_keeps_the_forums_rail(rf, person_user, set_flag, legal_published):
    """While the Forum permanent's module is open, a refusal under its prefix keeps the Forum's own rail — its rows
    after the account's, the row of the page refused marked — and the trail starts at the Forum."""
    from portal import services as portal_services

    set_flag(governance_services.GOVERNANCE_FLAG, True)
    with translation.override("fr"):
        root = reverse("forum_governance:participation")
        request = rf.get(reverse("forum_governance:proposals"))
        request.user = person_user
        request.forum_governance_active = "forum_proposals"
        shell = portal_services.console_state_shell(request, "Accès non autorisé")
        module = translation.gettext("Forum permanent")
    keys = [item["key"] for item in shell["portal_nav"]]
    assert {"dashboard", "forum_participation", "forum_commissions", "forum_proposals"} <= set(keys), keys
    assert [item["key"] for item in shell["portal_nav"] if item["current"]] == ["forum_proposals"]
    assert shell["breadcrumbs"] == [{"label": module, "url": root}, {"label": "Accès non autorisé", "url": ""}]


@pytest.mark.django_db
def test_everyone_else_meets_the_forums_closed_module_in_public(client, person_user, staff_user, set_flag):
    """An anonymous visitor, and a person while the reserved area is switched off, meet the module that is not open
    yet on its public page, unchanged — the door at rest, the way on; a member of staff passes the switch."""
    set_flag(governance_services.GOVERNANCE_FLAG, False)
    with translation.override("fr"):
        url = reverse("forum_governance:participation")
    response = client.get(url)
    assert response.status_code == 503
    _in_public(response.content.decode())
    _switch(False)
    client.force_login(person_user)
    response = client.get(url)
    assert response.status_code == 503
    _in_public(response.content.decode())
    client.force_login(staff_user)
    response = client.get(url)
    assert response.status_code == 503
    _in_the_console(response.content.decode())


# ---- one overlay system, one alert anatomy ----------------------------------------------------------------------------
def test_every_dialog_of_the_site_is_the_overlay_systems():
    dialogs = 0
    for path in _templates():
        text = COMMENTS.sub("", path.read_text(encoding="utf-8"))
        for tag in re.findall(r"<dialog\b[^>]*>", text):
            dialogs += 1
            assert 'data-overlay="' in tag and re.search(r'class="[^"]*\boverlay overlay--', tag), f"{path}: {tag}"
    assert dialogs >= 6, dialogs  # the dialog, the drawer, the sheet; the site's menu, the console's, the piece's


def test_every_alert_of_the_platform_has_one_anatomy():
    include = re.compile(r'{%\s*include\s+"components/dialog\.html"\s+with\s+([^%]*)%}')
    alerts = 0
    for path in _templates():
        for arguments in include.findall(path.read_text(encoding="utf-8")):
            if 'kind="alert"' not in arguments:
                continue
            alerts += 1
            actions = re.search(r'actions_template="([^"]+)"', arguments)
            assert actions, f"{path}: an alert's foot is its own template, the safe answer named in it"
            foot = (TEMPLATES / actions.group(1)).read_text(encoding="utf-8").rsplit("{% else %}", 1)[1]
            buttons = re.findall(r"<button\b[^>]*>.*?</button>", foot, re.S)
            assert len(buttons) == 2, f"{actions.group(1)}: one safe answer, one act"
            safe, act = buttons
            assert safe.startswith(
                '<button class="btn btn--secondary" type="button" data-overlay-close data-overlay-safe>'
            )
            assert '{% translate "Annuler" %}' in safe, actions.group(1)
            assert re.match(r'<button class="btn btn--(primary|danger)" type="submit"', act), actions.group(1)
            assert "data-overlay-close" not in act and "data-overlay-safe" not in act, actions.group(1)
    assert alerts >= 6, alerts
