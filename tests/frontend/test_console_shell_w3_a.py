"""
The console shell «Tre livelli» — design V5, family W3-A (docs/design-v5/V5_4_EXECUTION_PLAN.md §1.18 D06, §3.5 item 3;
docs/design-v5/QA/v54/w3-a/NOTES.md). What the family's gate asks of the shell, held without a browser:

* ONE builder for every rail (`portal.services.shell_navigation`): the keys of a space's rail are the same on each of
  its URLs, whichever module renders the page; a rail never carries one label for two addresses; at most four
  entries reach the phone's bottom bar, for every role; the registers a role owns come first; the way to the
  account's other space is not a page of the rail;
* who the account is — the glyph and the word of the rail's foot — follows the roles first, then the account type;
* the markup: three levels, the pinned foot (the account, sign-out, the language, «Site public»), the current page
  marked once per rail copy, the two skip links and their targets;
* the sheets: console.css is the console's import list; the shell draws two corners (4 px and full), no shadow but
  its one menu's and its drawer's, no keyframes (the drawer moves on the overlay system's transitions, W2-A), nothing
  that loops; without script the rail is open;
* below 64rem (step 2 — «the rail laid flat»): one «Menu», in the bottom bar, a link to the drawer that the overlay
  system turns into a button; the bar's words are the live labels on one line or two, never cut; three entries where four do
  not hold; the drawer holds the rail's own foot; the safe areas on the logical sides; a page's action bar.

The browser halves — the foot at 1366 × 657, the stored choice before the first frame, the skip links' focus, the
words of the lone glyphs; and, on a phone, the bars' measures, the drawer, Arabic, forced colours — are
tests/frontend/test_console_shell_browser_w3_a.py and tests/frontend/test_console_phone_browser_w3_a.py.
"""

from __future__ import annotations

import re
from html.parser import HTMLParser
from pathlib import Path

import pytest
from django.urls import reverse

from accounts import roles
from core import icons
from portal import services

ROOT = Path(__file__).resolve().parents[2]
PORTAL_STATIC = ROOT / "apps" / "portal" / "static" / "portal"
ENTRY = PORTAL_STATIC / "console.css"
SHELL = PORTAL_STATIC / "v5" / "_shell.css"
CHROME = ROOT / "templates" / "partials" / "portal_chrome.html"
RAIL = ROOT / "templates" / "portal" / "partials" / "rail_nav.html"
BASE = ROOT / "templates" / "portal" / "base_portal.html"
RAIL_PREF = ROOT / "static" / "js" / "rail-pref.js"
CONSOLE_JS = ROOT / "static" / "js" / "src" / "console.js"

#: The ten destinations of «Espace réservé», in the rail's order (plan §1.18 D06: «the ten destinations are kept»).
TEN = [
    "dashboard",
    "situation",
    "pathways",
    "cases",
    "requests",
    "documents",
    "deadlines",
    "messages",
    "helpdesk",
    "academy",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _css(path: Path) -> str:
    return re.sub(r"/\*.*?\*/", "", _read(path), flags=re.S)


def _template(path: Path) -> str:
    return re.sub(r"{%\s*comment\s*%}.*?{%\s*endcomment\s*%}", "", _read(path), flags=re.S)


# ---------------------------------------------------------------------------------------------- the sheets


def test_the_console_entry_is_an_import_list_the_light_sheet_first_then_the_shell():
    entry = _css(ENTRY).strip()
    statements = [line.strip() for line in entry.splitlines() if line.strip()]
    assert statements[:2] == [
        '@import url("../css/v5/_loader-light.css");',
        '@import url("v5/_shell.css");',
    ], "console.css is the console's import list: each family adds its partial's import, and writes its rules there"
    # after the shell, each Wave-3 family's own partial — imported from the app's static folder, `_`-prefixed (W3-B on)
    for statement in statements[2:]:
        partial = re.fullmatch(r'@import url\("(v5/_[a-z-]+\.css)"\);', statement)
        assert partial and (ENTRY.parent / partial.group(1)).exists(), statement
    assert SHELL.exists() and SHELL.name.startswith("_"), "the shell is a partial: never an output of its own"
    assert not (ROOT / "static" / "css" / "dist" / "portal" / "v5" / "_shell.css").exists()
    bundle = _read(ROOT / "static" / "css" / "dist" / "portal" / "console.css")
    assert ".rail__foot" in bundle and "lume-light-o" in bundle, "the bundle carries the shell and the light sheet"


def test_the_shell_draws_two_corners_and_no_shadow_but_its_menu_s():
    css = _css(SHELL)
    radii = set(re.findall(r"border(?:-[a-z-]+)?-radius:\s*([^;]+);", css))
    assert radii <= {"var(--radius-sm)", "var(--radius-full)", "var(--drawer-radius)", "0"}, (
        f"the shell draws 4 px and full only — two of a console screen's three corners (plan §1.3): {sorted(radii)}"
    )
    shadows = re.findall(r"([^{}]+)\{[^{}]*box-shadow:\s*([^;]+);", css)
    carried = {(" ".join(selector.split()), value.strip()) for selector, value in shadows if value.strip() != "none"}
    assert carried == {
        (".rail__lang .lang-seg", "var(--shadow-3-dark)"),
        (".console-drawer.overlay--drawer", "var(--shadow-4-dark)"),
    }, f"navigation never carries a shadow (SH-2); the rail's one menu and the phone's drawer are overlays: {carried}"
    assert "gradient(" not in css and not re.search(r"#[0-9a-fA-F]{3,8}\b|\brgba?\(", css), "tokens only"
    assert "--mesh-dark" not in css, "the rail is flat night: the V4 mesh is gone"


def test_nothing_of_the_shell_loops_or_moves_at_load():
    css = _css(SHELL)
    assert "infinite" not in css
    assert not re.findall(r"@keyframes ([a-z0-9-]+)", css), (
        "the shell keyframes nothing: the drawer slides in and out on the overlay system's transitions (W2-A), on the "
        "person's own act"
    )
    animated = {
        " ".join(selector.split())
        for selector, _ in re.findall(r"([^{}]+)\{[^{}]*\banimation(?:-name)?:\s*([^;]+);", css)
    }
    assert animated == set(), animated
    # the one layout transition — the rail's width — waits for the first frame and for the person's own act
    moving = re.findall(r"([^{}]+)\{[^{}]*transition:\s*([^;]*(?:inline-size|padding)[^;]*);", css)
    assert [" ".join(selector.split()) for selector, _ in moving] == [
        "body.console.is-ready",
        "body.is-ready .rail:not(.rail--drawer)",
    ], moving
    for _selector, value in re.findall(r"([^{}]+)\{[^{}]*transition:\s*([^;]+);", css):
        # `none` is no duration at all: it is how the print block silences the rail's glide
        assert value == "none" or "var(--motion-" in value, (
            f"a duration that is not a token escapes reduced motion: {value}"
        )
    script = _read(CONSOLE_JS)
    assert 'afterPaint().then(() => document.body.classList.add("is-ready"))' in script
    assert "requestAnimationFrame" not in script and ".animate(" not in script, "frame waits go through motion.js"


def test_without_script_the_rail_is_open_and_the_choice_is_written_before_the_first_frame():
    css = _css(SHELL)
    base = re.search(r"body\.console \{([^}]*)\}", css).group(1)
    assert "--rail-current: var(--rail-w-open);" in base, (
        "no script, no attribute: the rail is open — never icon-only by default"
    )
    assert re.search(r'body\.console\[data-rail="closed"\] \{\s*--rail-current: var\(--rail-compact\);', css)
    assert "html.no-js .rail__toggle" in css, "a control that needs script is not offered without it"
    pref = _read(RAIL_PREF)
    code = re.sub(r"/\*.*?\*/", "", pref, flags=re.S)
    assert "import " not in code and "export " not in code, (
        "a classic, blocking script: it runs before the rail is parsed"
    )
    assert '"ile.rail"' in code and '"(min-width: 80rem)"' in code and 'setAttribute("data-rail", state)' in code
    base_html = _template(BASE)
    chrome = base_html.split("{% block chrome %}", 1)[1].split("{% endblock %}", 1)[0]
    assert chrome.index("js/rail-pref.js") < chrome.index("partials/portal_chrome.html"), "before the rail is parsed"
    assert '"(min-width: 80rem)"' in _read(CONSOLE_JS) and 'const KEY = "ile.rail"' in _read(CONSOLE_JS)


def test_the_short_screen_step_is_one_and_it_asks_a_fine_pointer():
    css = _css(SHELL)
    steps = re.findall(r"@media \(min-width: 64rem\) and \(max-height: ([0-9.]+rem)\) and \(pointer: fine\)", css)
    assert steps == ["47.5rem"], (
        "one density step, under 760 px of height, with a fine pointer (plan §1.8; the audit's S-1)"
    )
    block = css.split("@media (min-width: 64rem) and (max-height: 47.5rem) and (pointer: fine)", 1)[1]
    assert "--rail-row: 40px;" in block.split("@media", 1)[0]
    assert re.search(r"@media \(pointer: coarse\) \{[^@]*\.rail__tool[^@]*var\(--hit-primary\)", css, flags=re.S), (
        "under a coarse pointer the shell's controls are 44 px (SP-8)"
    )


def test_a_page_title_hugs_its_words_and_never_exceeds_the_frame():
    css = _css(SHELL)
    title = re.search(r"\.console \.page-header__title \{([^}]*)\}", css).group(1)
    lead = re.search(r"\.console \.page-header__lead \{([^}]*)\}", css).group(1)
    assert re.search(
        r"\.console \.page-header__title,\s*\.console \.page-header__lead \{\s*inline-size: fit-content;", css
    ), "a title written in another language than the page stays on the frame's reading edge: its box hugs its words"
    assert "max-inline-size: min(44rem, 100%);" in title, (
        "a hugging box is as wide as its longest word: bounded by the frame, a 100-character word wraps on a phone "
        "(apps/portal/tests/test_browser.py holds the measured half)"
    )
    assert "max-inline-size: min(var(--measure-body), 100%);" in lead


# ---------------------------------------------------------------------------------------------- the markup


def test_the_two_skip_links_follow_the_content_s_and_their_targets_exist():
    base_html = _template(BASE)
    chrome_block = base_html.split("{% block chrome %}", 1)[1].split("{% endblock %}", 1)[0]
    links = re.findall(r'<a class="skip-link ([a-z-]+)" href="#([a-z-]+)">', chrome_block)
    assert links == [("skip-link--rail", "console-rail"), ("skip-link--menu", "console-menu")], links
    assert chrome_block.lstrip().startswith('<a class="skip-link skip-link--rail"'), (
        "the navigation's skip links are the first things of the chrome: right after «Aller au contenu principal»"
    )
    chrome = _template(CHROME)
    assert re.search(r'<nav class="rail" id="console-rail"[^>]*tabindex="-1"', chrome), "the rail can take the focus"
    assert re.search(
        r'<a class="console-bottom__item console-bottom__menu" id="console-menu" href="#console-drawer" data-console-menu',
        chrome,
    ), "«Menu» is a link to the drawer: it leads somewhere without script, and says what it is"
    assert 'role="button"' not in chrome, "the role of a button is given by the script that makes it one"
    assert chrome.count("data-console-menu") == 1, "one «Menu», in the thumb's zone: no «≡» in the top bar"
    css = _css(SHELL)
    assert re.search(r"\.skip-link--menu \{\s*display: none;", css), "«Menu» is offered where the rail is not drawn"
    phone = css.split("@media (max-width: 63.999rem)", 1)[1]
    assert re.search(r"\.skip-link--rail \{\s*display: none;", phone) and re.search(
        r"\.skip-link--menu \{\s*display: block;", phone
    )


def test_the_rail_has_a_head_a_list_and_a_pinned_foot_with_the_account_the_language_and_sign_out():
    chrome = _template(CHROME)
    rail = chrome.split('<nav class="rail" id="console-rail"', 1)[1].split("</nav>\n\n<header", 1)[0]
    head, listing = rail.split('<div class="rail__scroll" data-rail-scroll>', 1)
    # level 1 — the space, under the name
    assert '<span class="rail__space" data-rail-space>' in head and 'part="space"' in head
    assert "{{ space.label }}" in head and '{% brand "rail__wm" %}' in head
    # levels 2 and 3 — the partial, once in the rail and once in the drawer
    assert 'id_prefix="rail"' in listing and chrome.count('id_prefix="drawer"') == 1
    # the foot — the partial's third part, once under the rail's list and once under the drawer's
    assert listing.rstrip().endswith('{% include "portal/partials/rail_nav.html" with part="foot" where="rail" %}')
    assert chrome.count('part="foot" where="drawer"') == 1 and chrome.count('part="foot"') == 2
    foot = _template(RAIL).split('{% elif part == "foot" %}', 1)[1].split("{% else %}{% regroup", 1)[0]
    assert '<div class="rail__foot"{% if where == "rail" %} data-rail-foot{% endif %}>' in foot
    assert "{% safe_url 'accounts:profile' as profile_url %}" in foot and 'class="rail__who"' in foot
    assert "{{ space.who }}" in foot, "who the account is: its glyph and its word"
    # the glyph goes through the registry's concept filter, where W1-C's O14 lint sees it is registry-fed
    assert 'space.who_key|concept:"actor"' in foot and 'space.who_key|concept:"audience"' in foot
    assert re.search(r'<form class="rail__signout" method="post" action="{{ logout_url }}">{% csrf_token %}', foot)
    assert '<span class="rail__tool-word">{% translate "Se déconnecter" %}</span>' in foot, (
        "the word of sign-out: kept for a reader in the rail, drawn beside the glyph in the drawer"
    )
    assert '{% include "components/language_segmented.html" with lang_names=True %}' in foot, (
        "the languages by their own names"
    )
    assert "{% url 'pages:home' %}" in foot and '{% translate "Site public" %}' in foot
    assert re.search(
        r'{% if where == "rail" %}<button class="rail__tool rail__toggle"[^>]*data-rail-toggle[^>]*aria-controls="console-rail"[^>]*aria-expanded="true"',
        foot,
    ), "the rail's own control is the rail's: nothing folds in the drawer"
    grid = re.search(r"\.rail:not\(\.rail--drawer\) \{([^}]*)\}", _css(SHELL)).group(1)
    assert "grid-template-rows: auto minmax(0, 1fr) auto;" in grid, (
        "the head and the foot are pinned: the list scrolls between them"
    )
    # from 64rem the bar is the level of the page and nothing else
    bar = chrome.split('<header class="portal-bar console-bar"', 1)[1].split("</header>", 1)[0]
    assert "language_segmented" not in bar and "Site public" not in bar
    assert re.search(r"\.console-bar__actions \{\s*display: none;", _css(SHELL)) or ".console-bar__actions" in _css(
        SHELL
    )


def test_the_rail_partial_draws_the_other_space_at_the_head_and_never_in_the_list():
    partial = _template(RAIL)
    space_part, list_part = partial.split("{% else %}{% regroup portal_nav by group as rail_groups %}", 1)
    space_part = space_part.split('{% elif part == "foot" %}', 1)[0]
    assert '{% if kind.grouper == "space" %}' in space_part and 'class="rail__switch"' in space_part
    assert "data-rail-item" not in space_part, "the way to another space is not a page of the rail"
    assert '{% if first.kind != "space" %}' in list_part
    assert list_part.count("data-rail-item") == 1 and 'aria-current="page"' in list_part
    assert "group.grouper == first.space.label" in list_part and "group.grouper == first.label" in list_part, (
        "a section whose word would repeat the space's name or its one entry is a rule, without the word"
    )


# ---------------------------------------------------------------------------------------------- the builder


@pytest.fixture
def people(user_factory, superuser):
    """One account per kind the shell tells apart."""
    return {
        "person": user_factory("w3a-person@example.test", role=roles.PERSON),
        "bare": user_factory("w3a-bare@example.test"),
        "company": user_factory("w3a-company@example.test", role=roles.COMPANY),
        "professional": user_factory("w3a-professional@example.test", role=roles.PROFESSIONAL),
        "operator": user_factory("w3a-operator@example.test", role=roles.OPERATOR),
        "administrator": user_factory("w3a-administrator@example.test", role=roles.ADMINISTRATOR),
        "actor": user_factory("w3a-actor@example.test", role=roles.AUTHORISED_ACTOR),
        "institution": user_factory("w3a-institution@example.test", account_type="institution"),
        "university": user_factory("w3a-university@example.test", role=roles.UNIVERSITY),
        "staff": user_factory("w3a-staff@example.test", role=roles.STAFF, is_staff=True),
        "superuser": superuser,
    }


@pytest.mark.django_db
def test_a_person_s_rail_is_the_ten_in_three_levels(people):
    rail = services.shell_navigation(people["person"])
    assert [entry["key"] for entry in rail] == TEN
    assert rail == services.navigation(people["person"]), "navigation() is the builder, for «Espace réservé»"
    for entry in rail:
        assert entry["kind"] == services.KIND_PAGE and entry["group"] and entry["icon"] == icons.NAV[entry["key"]]
        assert entry["space"]["key"] == services.SPACE_PERSON and entry["space"]["label"] == "Espace réservé"
        assert entry["space"]["url"] == reverse("portal:dashboard")
    assert [entry["group"] for entry in rail] == ["Parcours"] * 3 + ["Dossier"] * 4 + ["Échanges"] * 2 + ["Academy"]


@pytest.mark.django_db
def test_the_keys_do_not_depend_on_the_page_and_one_entry_at_most_is_current(people):
    for who, user in people.items():
        keys = [entry["key"] for entry in services.shell_navigation(user)]
        for active in [*keys, "", "no-such-key"]:
            rail = services.shell_navigation(user, active=active)
            assert [entry["key"] for entry in rail] == keys, (who, active)
            marked = [entry["key"] for entry in rail if entry["current"]]
            assert marked == ([active] if active in keys else []), (who, active, marked)


@pytest.mark.django_db
def test_no_rail_carries_one_label_for_two_addresses_and_four_entries_at_most_reach_the_bottom_bar(people):
    for who, user in people.items():
        for space in (services.SPACE_PERSON, services.SPACE_COMPANY):
            rail = services.shell_navigation(user, space)
            labels = [str(entry["label"]) for entry in rail]
            urls = [entry["url"] for entry in rail]
            assert len(set(labels)) == len(labels), (who, space, labels)
            assert len(set(urls)) == len(urls) and all(urls), (who, space, urls)
            assert sum(1 for entry in rail if entry["bottom"]) <= services.NAV_BOTTOM_MAX == 4, (who, space)
    person = [entry["key"] for entry in services.shell_navigation(people["person"]) if entry["bottom"]]
    assert person == ["dashboard", "cases", "documents", "messages"]
    for who, surface in (("company", "company"), ("professional", "helpdesk-queue"), ("actor", "selection")):
        flagged = {entry["key"] for entry in services.shell_navigation(people[who]) if entry["bottom"]}
        assert flagged == {"dashboard", "documents", "messages", surface}, (who, flagged)


@pytest.mark.django_db
def test_a_role_s_registers_come_first_and_the_other_space_is_not_a_page(people):
    professional = services.shell_navigation(people["professional"])
    assert [entry["key"] for entry in professional] == ["helpdesk-queue", *TEN]
    assert professional[0]["group"] == "Mon rôle" and professional[0]["kind"] == services.KIND_PAGE
    for who in ("operator", "administrator"):
        rail = services.shell_navigation(people[who])
        assert rail[0]["key"] == "helpdesk-dispatch" and rail[0]["url"] == reverse("helpdesk:dispatch"), who
        assert rail[0]["icon"] == icons.NAV["helpdesk-dispatch"]
    assert "helpdesk-dispatch" not in {entry["key"] for entry in professional}, (
        "a module a role cannot use is not shown"
    )
    company = services.shell_navigation(people["company"])
    assert [entry["key"] for entry in company] == [*TEN, "company"]
    way = company[-1]
    assert way["kind"] == services.KIND_SPACE and way["label"] == "Espace entreprise"
    assert way["url"] == reverse("companies:dashboard") and way["icon"] == icons.NAV["company"]
    everything = [entry["key"] for entry in services.shell_navigation(people["superuser"])]
    assert everything == ["selection", "helpdesk-queue", "helpdesk-dispatch", *TEN, "company"]


@pytest.mark.django_db
def test_the_company_space_keeps_the_module_s_entries_and_offers_the_way_back(people):
    from companies import services as company_services

    user = people["company"]
    rail = services.shell_navigation(user, services.SPACE_COMPANY, "dashboard")
    module = company_services.navigation(user, "dashboard", company=None)
    assert [entry["key"] for entry in rail] == [*(entry["key"] for entry in module), "reserved"]
    for entry in rail:
        assert entry["space"]["key"] == services.SPACE_COMPANY and entry["space"]["label"] == "Espace entreprise"
    back = rail[-1]
    assert back["kind"] == services.KIND_SPACE and back["label"] == "Espace réservé"
    assert back["url"] == reverse("portal:dashboard") and back["icon"] == services.SPACE_PERSON_GLYPH == "ile-key"
    assert not back["bottom"] and not back["current"]
    assert [entry["key"] for entry in rail if entry["current"]] == ["dashboard"]


@pytest.mark.django_db
def test_who_the_account_is_follows_its_roles_then_its_type(people, user_factory):
    expected = {
        "person": (icons.AUDIENCE["person"], "Personne"),
        "bare": (icons.AUDIENCE["person"], "Personne"),
        "company": (icons.AUDIENCE["company"], "Entreprise"),
        "professional": (icons.ACTOR["professional"], "Professionnel"),
        "operator": (icons.ACTOR["project_team"], "Équipe du projet"),
        "administrator": (icons.ACTOR["project_team"], "Équipe du projet"),
        "actor": (icons.ACTOR["authorised_actor"], "Acteur autorisé"),
        "institution": (icons.AUDIENCE["institution"], "Institution"),
        "university": (icons.AUDIENCE["university"], "Université ou organisme de formation"),
        "staff": (icons.ACTOR["project_team"], "Équipe du projet"),
        "superuser": (icons.ACTOR["project_team"], "Équipe du projet"),
    }
    for who, user in people.items():
        for space in (services.SPACE_PERSON, services.SPACE_COMPANY):
            plate = services.shell_space(user, space)
            assert (plate["who_icon"], plate["who"]) == expected[who], (who, space)
    assert len({icons.AUDIENCE[key] for key in ("person", "company", "institution", "university")}) == 4, (
        "Persona ≠ Impresa ≠ Istituzione ≠ Università"
    )
    # a role says more than the type, which defaults to «person»: the QA persona «personne avec dossier» is
    # typed `company` and holds the person's role — it is a person
    typed_company = user_factory("w3a-typed@example.test", role=roles.PERSON, account_type="company")
    assert services.shell_space(typed_company)["who"] == "Personne"
    typed_only = user_factory("w3a-typed-only@example.test", account_type="company")
    assert services.shell_space(typed_only)["who"] == "Entreprise"


def test_the_builder_answers_a_stranger_without_a_query():
    """The icon registry's test calls the builder with ``object()``: no account, no role, no query."""
    plate = services.shell_space(object())
    assert plate["who"] == "Personne" and plate["key"] == services.SPACE_PERSON
    assert services._role_entries(object()) == []
    assert services._bottom_keys(TEN) == frozenset({"dashboard", "documents", "messages", "cases"})


@pytest.mark.django_db
def test_the_identity_panel_is_a_page_of_the_rail_for_the_account_somebody_has_asked(people, monkeypatch):
    """«Communications d’identité» was a row of the selection module's own rail, on its own pages only: under one
    builder it is a page of «Échanges» for the account somebody has asked — the ten are kept for everybody else."""
    from selection import services as selection_services

    person = people["person"]
    assert selection_services.has_disclosures(person) is False, "the real query, on an account nobody has asked"
    assert selection_services.disclosures_for_person(person) == []
    assert [entry["key"] for entry in services.shell_navigation(person)] == TEN
    assert services._identity_panel(object()) is None, "a stranger: no query, no row"

    monkeypatch.setattr(selection_services, "has_disclosures", lambda user: user.pk == person.pk)
    rail = services.shell_navigation(person, active="disclosures")
    assert [entry["key"] for entry in rail] == [*TEN[:9], "disclosures", "academy"]
    panel = rail[9]
    assert panel["url"] == reverse("selection:disclosures") and panel["kind"] == services.KIND_PAGE
    assert str(panel["label"]) == "Communications d’identité" and panel["group"] == "Échanges"
    assert panel["icon"] == icons.NAV["disclosures"] == "pen-line", "the registry's glyph for that consent"
    assert panel["current"] and not panel["bottom"]
    assert sorted(entry["key"] for entry in rail if entry["bottom"]) == ["cases", "dashboard", "documents", "messages"]
    assert [entry["group"] for entry in rail[7:]] == ["Échanges"] * 3 + ["Academy"], "one section, no new word"
    # the module's own producer marks the panel for that account, and its own register for an actor nobody asked
    assert [e["key"] for e in selection_services.navigation(person, "disclosures") if e["current"]] == ["disclosures"]
    actor = people["actor"]
    assert [e["key"] for e in selection_services.navigation(actor, "disclosures") if e["current"]] == ["selection"]
    assert [e["key"] for e in selection_services.navigation(actor, "workspace") if e["current"]] == ["selection"]
    assert "disclosures" not in [entry["key"] for entry in services.shell_navigation(people["company"])]


@pytest.mark.django_db
def test_the_identity_panel_s_page_marks_its_own_row_once_per_copy(client, seeded, people, monkeypatch):
    from selection import services as selection_services

    person = people["person"]
    monkeypatch.setattr(selection_services, "has_disclosures", lambda user: user.pk == person.pk)
    client.force_login(person)
    seen = {}
    for name in ("selection:disclosures", "portal:dashboard", "academy:catalogue", "helpdesk:requests"):
        response = client.get(reverse(name))
        assert response.status_code == 200, name
        rails = _rails(response.content.decode())
        seen[name] = rails.entries
        for copy in ("rail", "drawer"):
            assert [key for key, _current in rails.entries[copy]] == [*TEN[:9], "disclosures", "academy"], (name, copy)
            assert sum(1 for _key, current in rails.entries[copy] if current) == 1, (name, copy)
    for copy in ("rail", "drawer"):
        assert [key for key, current in seen["selection:disclosures"][copy] if current] == ["disclosures"]


# ---------------------------------------------------------------------------------------------- every producer


class _Rails(HTMLParser):
    """The entries of each copy of the rail in a rendered page: the fixed rail and the drawer's."""

    def __init__(self):
        super().__init__()
        self.copy: str | None = None
        self.depth = 0
        self.entries: dict[str, list[tuple[str, bool]]] = {"rail": [], "drawer": []}
        self.switches: dict[str, list[str]] = {"rail": [], "drawer": []}

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        classes = (attributes.get("class") or "").split()
        if tag == "nav" and "rail" in classes:
            self.copy = "drawer" if "rail--drawer" in classes else "rail"
            self.depth = 0
        if self.copy is None:
            return
        if tag == "nav":
            self.depth += 1
        if tag == "a" and "data-rail-item" in attributes:
            self.entries[self.copy].append((attributes.get("data-key", ""), attributes.get("aria-current") == "page"))
        if tag == "a" and "rail__switch" in classes:
            self.switches[self.copy].append(attributes.get("href", ""))

    def handle_endtag(self, tag):
        if self.copy is not None and tag == "nav":
            self.depth -= 1
            if self.depth == 0:
                self.copy = None


def _rails(html: str) -> _Rails:
    parser = _Rails()
    parser.feed(html)
    return parser


#: Pages of «Espace réservé» rendered by six different modules: every one must draw the same rail.
RESERVED = (
    ("portal:dashboard", "dashboard"),
    ("portal:situation", "situation"),
    ("portal:pathways", "pathways"),
    ("portal:requests", "requests"),
    ("portal:documents", "documents"),
    ("portal:deadlines", "deadlines"),
    ("portal:messages", "messages"),
    ("cases:index", "cases"),
    ("documents:index", "documents"),
    ("academy:catalogue", "academy"),
    ("academy:mine", "academy"),
    ("helpdesk:requests", "helpdesk"),
    ("helpdesk:open", "helpdesk"),
    ("selection:workspace", "selection"),
    ("selection:disclosures", "selection"),
)


@pytest.mark.django_db
@pytest.mark.parametrize("who", ["person", "company", "professional", "operator", "actor", "superuser"])
def test_the_same_keys_on_every_url_of_espace_reserve_and_the_current_page_marked_once_per_copy(
    client, seeded, people, who
):
    user = people[who]
    client.force_login(user)
    expected = [entry["key"] for entry in services.shell_navigation(user) if entry["kind"] == services.KIND_PAGE]
    ways = [entry["url"] for entry in services.shell_navigation(user) if entry["kind"] == services.KIND_SPACE]
    for name, active in RESERVED:
        response = client.get(reverse(name))
        assert response.status_code == 200, (who, name, response.status_code)
        assert [entry["key"] for entry in response.context["portal_nav"]] == [
            entry["key"] for entry in services.shell_navigation(user)
        ], (who, name)
        rails = _rails(response.content.decode())
        for copy in ("rail", "drawer"):
            assert [key for key, _current in rails.entries[copy]] == expected, (who, name, copy)
            marked = [key for key, current in rails.entries[copy] if current]
            assert marked == ([active] if active in expected else []), (who, name, copy, marked)
            assert rails.switches[copy] == ways, (who, name, copy)


@pytest.mark.django_db
def test_the_same_keys_on_every_url_of_espace_entreprise(client, seeded, people):
    user = people["company"]
    client.force_login(user)
    seen = {}
    for name in ("companies:dashboard", "companies:profile_create"):
        response = client.get(reverse(name))
        assert response.status_code == 200, name
        rails = _rails(response.content.decode())
        seen[name] = [key for key, _current in rails.entries["rail"]]
        assert rails.entries["drawer"] and [key for key, _ in rails.entries["drawer"]] == seen[name]
        assert rails.switches["rail"] == [reverse("portal:dashboard")], "the way back to «Espace réservé», at the head"
        assert [entry["key"] for entry in response.context["portal_nav"]][-1] == "reserved"
    assert len({tuple(keys) for keys in seen.values()}) == 1 and seen["companies:dashboard"], seen


@pytest.mark.django_db
def test_the_rendered_shell_names_the_space_draws_the_foot_and_offers_the_two_skip_links(client, seeded, people):
    client.force_login(people["person"])
    html = client.get(reverse("portal:requests")).content.decode()
    body = html.split("<body", 1)[1]
    skip = re.findall(r'<a class="skip-link[^"]*" href="(#[a-z-]+)">([^<]+)</a>', body)
    assert skip == [
        ("#main-content", "Aller au contenu principal"),
        ("#console-rail", "Navigation de l’espace réservé"),
        ("#console-menu", "Menu"),
    ], skip
    assert 'id="console-rail"' in html and 'id="console-menu"' in html and 'id="main-content"' in html
    rail = html.split('<nav class="rail" id="console-rail"', 1)[1].split("</nav>", 1)[0]
    assert '<span class="rail__space" data-rail-space>Espace réservé</span>' in rail
    assert re.findall(r'<p class="rail__group-title"[^>]*>([^<]+)</p>', rail) == ["Parcours", "Dossier", "Échanges"], (
        "«Academy» would only repeat its one entry: a rule, without the word"
    )
    assert rail.count("rail__group--rule") == 1
    foot = html.split('<div class="rail__foot" data-rail-foot>', 1)[1].split('<header class="portal-bar', 1)[0]
    assert f'href="{reverse("accounts:profile")}"' in foot and "icon-person" in foot and "Personne" in foot
    assert re.search(rf'<form class="rail__signout" method="post" action="{reverse("account_logout")}">', foot)
    assert "csrfmiddlewaretoken" in foot and "Se déconnecter" in foot
    assert re.findall(r'hreflang="([a-z]{2})"', foot) == ["it", "fr", "en", "ar"], (
        "the four languages, by their own names"
    )
    assert "Italiano" in foot and "Français" in foot and "English" in foot and "العربية" in foot
    assert f'href="{reverse("pages:home")}"' in foot and "Site public" in foot
    # the level of the page is the bar's breadcrumb; the workspace opens with the page's one header
    assert 'class="breadcrumbs' in html.split('<header class="portal-bar console-bar"', 1)[1].split("</header>", 1)[0]
    workspace = html.split('<div class="console__workspace">', 1)[1]
    assert workspace.lstrip().startswith('<header class="page-header'), "the page header is the frame's first block"


@pytest.mark.django_db
def test_a_company_account_sees_its_space_named_and_the_way_to_the_other(client, seeded, people):
    client.force_login(people["company"])
    reserved = client.get(reverse("portal:dashboard")).content.decode()
    rail = reserved.split('<nav class="rail" id="console-rail"', 1)[1].split("</nav>", 1)[0]
    assert '<span class="rail__space" data-rail-space>Espace réservé</span>' in rail
    assert re.search(
        rf'<a class="rail__switch" href="{reverse("companies:dashboard")}"[^>]*>.*?Espace entreprise', rail, flags=re.S
    )
    assert "icon-building" in rail.split('<div class="rail__foot"', 1)[1], "who the account is: Impresa"
    company = client.get(reverse("companies:dashboard")).content.decode()
    rail = company.split('<nav class="rail" id="console-rail"', 1)[1].split("</nav>", 1)[0]
    assert '<span class="rail__space" data-rail-space>Espace entreprise</span>' in rail
    assert f'<a class="rail__brand" href="{reverse("companies:dashboard")}"' in rail, (
        "the name leads to the space's first page"
    )
    assert re.search(
        rf'<a class="rail__switch" href="{reverse("portal:dashboard")}"[^>]*>.*?Espace réservé', rail, flags=re.S
    )
    assert "rail__group-title" not in rail.split('<div class="rail__foot"', 1)[0], (
        "the module's one section is named as the space is: no word is drawn twice"
    )


# ---------------------------------------------------------------------------------------------- below 64rem (step 2)
#
# «The rail laid flat»: the top bar is the rail's head, the bottom bar its pages, the drawer the whole rail
# (DL54-66 … DL54-71). What a sheet, a template and the builder can be held to without a browser; the measured half
# is tests/frontend/test_console_phone_browser_w3_a.py.

BASE_CSS = ROOT / "static" / "css" / "v5" / "base.css"
CASE_DETAIL = ROOT / "templates" / "cases" / "detail.html"
SITUATION = ROOT / "templates" / "portal" / "situation.html"


def _block(css: str, opening: str) -> str:
    """The body of the first top-level block that opens with ``opening`` (an at-rule's prelude, brace included)."""
    start = css.index(opening) + len(opening)
    depth, end = 1, start
    while depth:
        depth += {"{": 1, "}": -1}.get(css[end], 0)
        end += 1
    return css[start : end - 1]


def _rule(css: str, selector: str) -> str:
    """The declarations of the first rule whose selector is exactly ``selector``."""
    match = re.search(r"(?:^|[};{])\s*" + re.escape(selector) + r"\s*\{([^{}]*)\}", css)
    assert match, f"no rule for {selector!r}"
    return match.group(1)


def test_below_64rem_the_two_bars_are_the_rail_s_night_without_glass_and_the_top_bar_is_48_px():
    css = _css(SHELL)
    phone = _block(css, "@media (max-width: 63.999rem) {")
    top, bottom = _rule(phone, ".console-bar"), _rule(phone, ".console-bottom")
    for name, bar in (("top", top), ("bottom", bottom)):
        assert "background: var(--rail-bg);" in bar, (
            f"the {name} bar is the rail's own night (O13: «the same night chrome»)"
        )
    assert "backdrop-filter: none;" in top and "border-block-end: 0;" in top, "no glass on a phone, and no edge"
    assert "backdrop-filter" not in bottom and "box-shadow" not in bottom, "navigation carries neither glass nor shadow"
    base = re.search(r"body\.console \{([^}]*)\}", css).group(1)
    assert "--bar-top: 48px;" in base, "the phone's top bar: 48 px — with a bar of two-line words, 114 px of chrome"
    band = _block(css, "@media (min-width: 48rem) and (max-width: 63.999rem) {")
    assert "--bar-top: var(--ctx-h);" in _rule(band, "body.console"), "56 px in the band: the bar there holds one row"
    assert "min-block-size: var(--bar-top);" in _rule(phone, ".console-bar__inner")
    assert "scroll-padding-block: 4rem 5.5rem;" in _rule(phone, "html:has(body.console)"), (
        "what scrolls into view stops clear of both bars (WCAG 2.4.11)"
    )
    # the mark's tile, 32 px drawn and 44 to the finger; the account, 44 px
    assert "inset: -6px;" in _rule(phone, ".console-bar__tile::after") and "inline-size: 32px;" in _rule(
        phone, ".console-bar__tile"
    )
    summary = _rule(phone, ".console-bar .account-menu__summary")
    assert "min-inline-size: var(--hit-primary);" in summary and "min-block-size: var(--hit-primary);" in summary
    assert ".console-bar__menu" not in css, "the «≡» of the top bar is gone: «Menu» stands once, in the bottom bar"


def test_where_the_viewport_is_short_or_very_narrow_the_top_bar_leaves_with_the_page():
    css = _css(SHELL)
    leaves = _block(css, "@media (max-width: 22.499rem), (max-width: 63.999rem) and (max-height: 30rem) {")
    assert "position: static;" in _rule(leaves, ".console-bar"), (
        "a phone on its side, a window at 400 % (WCAG 1.4.10): the bottom bar alone stays on screen"
    )
    short = _block(css, "@media (max-width: 63.999rem) and (max-height: 30rem) {")
    assert "overflow-y: auto;" in _rule(short, ".rail--drawer"), "and the drawer's foot is not pinned there"


def test_the_bar_s_words_are_the_live_labels_whole_and_never_under_the_scale_s_floor():
    css = _css(SHELL)
    phone = _block(css, "@media (max-width: 63.999rem) {")
    item = _rule(phone, ".console-bottom__item")
    assert "font-size: 0.75rem;" in item and "line-height: 0.875rem;" in item, "12 / 14: the floor of the Latin scale"
    arabic = _rule(phone, ":lang(ar) .console-bottom__item")
    assert "font-size: 0.875rem;" in arabic, "never under 14 px in Arabic (D21)"
    assert "white-space: nowrap;" in _rule(phone, ".console-bottom__line"), (
        "a label breaks between its two runs and nowhere else"
    )
    label = _rule(phone, ".console-bottom__label")
    assert "overflow-wrap: normal;" in label and "hyphens: manual;" in label
    for banned in ("hyphens: auto", "-webkit-line-clamp", "text-overflow", "overflow: hidden", "word-break: break"):
        assert banned not in label and banned not in item, f"a word of the bar is never cut: {banned}"
    # the air gives way before a word does
    assert "flex: 0 10000 6px;" in _rule(phone, ".console-bottom__item::before,\n  .console-bottom__item::after")
    # and a row wider than the screen (under the gate's 320 px) scrolls inside the bar: the page does not
    bar = _rule(phone, ".console-bottom")
    assert "overflow-x: auto;" in bar and "overscroll-behavior-x: contain;" in bar, (
        "«Menu», the last entry of the row, stays within reach"
    )
    # three entries where four words and «Menu» do not hold
    narrow = _block(css, "@media (max-width: 22.499rem) {")
    assert "display: none;" in _rule(narrow, ".console-bottom__cell--yields-narrow")
    phones = _block(css, "@media (max-width: 29.999rem) {")
    assert "display: none;" in _rule(phones, ".console-bottom__cell--yields-phone")
    assert "display: block;" in _rule(phones, ".console-bottom__label--stacks .console-bottom__line")
    # the foundation's two patches for V4's bar left with the bar (DL54-71)
    foundation = _css(BASE_CSS)
    assert ".console-bottom__item" not in foundation and ".console-bar__title" not in foundation


def test_il_lume_on_the_bar_is_the_rail_s_lit_disc_and_never_a_bar_at_the_edge():
    css = _css(SHELL)
    phone = _block(css, "@media (max-width: 63.999rem) {")
    disc = _rule(phone, '.console-bottom__item[aria-current="page"] .console-bottom__disc')
    assert "background: var(--surface-raised);" in disc and "color: var(--text-1);" in disc
    rail = _rule(css, '.rail__item[aria-current="page"] .rail__disc')
    assert "background: var(--surface-raised);" in rail, "one drawing: the rail's lit paper disc"
    assert "inline-size: var(--glyph-disc-md);" in _rule(phone, ".console-bottom__disc")
    current = _rule(phone, '.console-bottom__item[aria-current="page"]')
    assert "font-weight" not in current, "the weight stays: a word never changes lines when its page is the current one"
    assert not re.search(r"\.console-bottom__item\[aria-current=\"page\"\]::(?:before|after)", css), (
        "no bar at the edge"
    )


def test_the_safe_areas_are_read_once_on_the_logical_sides():
    css = _css(SHELL)
    base = re.search(r"body\.console \{([^}]*)\}", css).group(1)
    for name, side in (("top", "top"), ("bottom", "bottom"), ("start", "left"), ("end", "right")):
        assert f"--safe-{name}: env(safe-area-inset-{side}, 0px);" in base
    mirrored = _rule(css, '[dir="rtl"] body.console')
    assert "--safe-start: env(safe-area-inset-right, 0px);" in mirrored
    assert "--safe-end: env(safe-area-inset-left, 0px);" in mirrored
    assert css.count("env(") == 6, "env() only knows left and right: read once, then used by its logical name"
    phone = _block(css, "@media (max-width: 63.999rem) {")
    assert "padding-block-start: var(--safe-top);" in _rule(phone, ".console-bar")
    assert "padding-block-end: var(--safe-bottom);" in _rule(phone, ".console-bottom")
    assert "padding-inline: var(--safe-start) var(--safe-end);" in _rule(phone, ".console-bottom")
    assert "var(--safe-start)" in _rule(phone, ".console-bar__inner") and "var(--safe-end)" in _rule(
        phone, ".console-bar__inner"
    )
    assert "var(--safe-bottom)" in _rule(phone, ".rail--drawer .rail__foot")
    assert "padding-block-end: calc(var(--bottom-clear) + var(--safe-bottom));" in _rule(
        phone, 'body.console,\n  body.console[data-rail="closed"]'
    )
    assert "viewport-fit=cover" in _read(ROOT / "templates" / "base.html"), (
        "the insets are live: the page draws to the edge"
    )


def test_menu_is_a_link_that_script_turns_into_a_button_and_without_script_it_still_shows_the_drawer():
    chrome = _template(CHROME)
    assert re.search(
        r'<a class="console-drawer__close" href="#main-content" data-console-close data-overlay-close>', chrome
    ), "the close control leads back to the page without script; with it, it is the overlay system's «Fermer»"
    assert "console-bar__menu" not in chrome and chrome.count('href="#console-drawer"') == 1
    assert re.search(r'<nav class="console-bottom"[^>]*>\s*<ul class="console-bottom__list" role="list">', chrome), (
        "a list of links, never a tablist (DS V5 SC04)"
    )
    # the drawer is a modal drawer of the overlay system (W2-A): its hooks, and «Menu» its link opener
    assert re.search(
        r'<dialog class="console-drawer overlay overlay--drawer" id="console-drawer" data-overlay="drawer" '
        r'data-overlay-edge="start" data-console-drawer',
        chrome,
    ), "from the reading edge, on the system's hooks"
    assert re.search(
        r'href="#console-drawer" data-console-menu data-overlay-open aria-controls="console-drawer"', chrome
    )
    overlays_css = _read(ROOT / "static" / "css" / "v5" / "overlays.css")
    assert re.search(r"html\.no-js \.overlay:target \{\s*display: flex;", overlays_css), (
        "without script the link's target is the drawer, and the system's stylesheet shows it"
    )
    script = _read(CONSOLE_JS)
    assert 'import { close, isOpen } from "./overlay.js";' in script, "console.js imports the overlay system"
    system = _read(ROOT / "static" / "js" / "src" / "overlay.js")
    assert (
        "event.preventDefault();" in system
        and 'if (event.key === " " && event.target instanceof HTMLAnchorElement' in system
    ), "with script «Menu» is a button: Space presses it as Enter does, and nothing is added to the address"
    assert (
        'opener.setAttribute("role", "button");' in system
        and 'opener.setAttribute("aria-haspopup", "dialog");' in system
    ), "the role comes with the behaviour: without script a link is a link"
    assert 'window.matchMedia("(min-width: 64rem)").addEventListener("change"' in script, (
        "a window widened past 64rem puts the drawer away"
    )
    assert "close(panel, { focus: rail })" in script and "showModal" not in script, (
        "the overlay system's modal drawer: no dialog of the shell's own"
    )


def test_a_page_declares_its_phone_action_bar_and_the_questionnaire_s_foot_is_part_of_its_page():
    css = _css(SHELL)
    phone = _block(css, "@media (max-width: 63.999rem) {")
    bar = _rule(phone, ".console :is([data-console-action], [data-file-action-bar])")
    assert "position: fixed;" in bar and "inset-block-end: 0;" in bar, (
        "where the four entries stood: one bar, never two"
    )
    assert "min-block-size: calc(var(--action-bar-h) + var(--safe-bottom));" in bar
    assert "padding-inline: max(var(--page-pad), var(--safe-start)) calc(var(--menu-seat) + var(--safe-end));" in bar, (
        "the bar leaves «Menu» its seat at the reading end (O63)"
    )
    has = ".console:has(:is([data-console-action], [data-file-action-bar]))"
    assert "display: none;" in _rule(phone, f"{has} .console-bottom__cell:not(.console-bottom__cell--menu)")
    assert "background: transparent;" in _rule(phone, f"{has} .console-bottom")
    foot = _rule(phone, ".console [data-wizard-foot]")
    assert "position: static;" in foot and "flex-wrap: wrap;" in foot, (
        "five controls are not an action bar: the questionnaire's foot closes its form and its controls wrap"
    )
    # the two hooks are the pages' own: the day a family renames one, this test says so
    assert "data-file-action-bar" in _read(CASE_DETAIL) and "data-wizard-foot" in _read(SITUATION)


def test_the_drawer_draws_the_rail_s_own_foot_with_sign_out_as_a_row():
    chrome = _template(CHROME)
    drawer = chrome.split('<dialog class="console-drawer overlay overlay--drawer"', 1)[1]
    assert re.search(
        r'<nav class="rail rail--drawer"[^>]*>\s*<div class="rail__scroll">.*?</div>\s*'
        r'{% include "portal/partials/rail_nav.html" with part="foot" where="drawer" %}\s*</nav>',
        drawer,
        flags=re.S,
    ), "the list scrolls between the drawer's head and the rail's own foot"
    assert "language_segmented" not in drawer and "console-drawer__foot" not in chrome, (
        "V4's segmented track is gone from the drawer: the languages by their own names (D21)"
    )
    foot = _template(RAIL).split('{% elif part == "foot" %}', 1)[1].split("{% else %}{% regroup", 1)[0]
    assert (
        '{% if where == "drawer" %}<span class="rail__disc">{% svg_icon "languages" "icon rail__glyph" %}</span>'
        in foot
    )
    assert icons.SYMBOLS["languages"], "the registry's glyph of the language control"
    css = _css(SHELL)
    phone = _block(css, "@media (max-width: 63.999rem) {")
    row = _rule(phone, ".rail--drawer .rail__signout .rail__tool")
    assert "inline-size: 100%;" in row and "min-block-size: var(--rail-row);" in row
    hidden = _rule(css, ".rail:not(.rail--drawer) .rail__tool-word")
    assert "clip-path: inset(50%);" in hidden, (
        "in the rail the word stays a reader's; console.js shows it beside the glyph"
    )
    assert "grid-template-rows: minmax(0, 1fr) auto;" in _rule(phone, ".rail--drawer")


def test_forced_colours_give_the_phone_s_bars_an_edge_and_the_bar_s_current_page_its_disc():
    forced = _block(_css(SHELL), "@media (forced-colors: active) {")
    assert "border-block-end: 1px solid CanvasText;" in _rule(forced, ".console-bar")
    assert "border-block-start: 1px solid CanvasText;" in _rule(forced, ".console-bottom")
    current = _rule(forced, '.rail__item[aria-current="page"],\n  .console-bottom__item[aria-current="page"]')
    assert "outline: 2px solid Highlight;" in current
    disc = _rule(
        forced,
        '.rail__item[aria-current="page"] .rail__disc,\n  .console-bottom__item[aria-current="page"] .console-bottom__disc',
    )
    assert "background: Highlight;" in disc and "forced-color-adjust: none;" in disc


def test_on_paper_the_page_is_the_page_no_rail_no_bar_no_drawer():
    printed = _block(_css(SHELL), "@media print {")
    hidden = _rule(
        printed,
        "body.console .rail,\n  body.console .console-bar,\n  body.console .console-bottom,\n  body.console .console-drawer",
    )
    assert "display: none;" in hidden, "a fixed bar is printed again on every sheet"
    room = _rule(printed, "body.console,\n  body.console[data-rail]")
    assert "padding-inline-start: 0;" in room and "padding-block-end: 0;" in room, (
        "and the page gives back the room it kept for them"
    )
    css = _css(SHELL)
    assert "transition: none;" in _rule(printed, "body.console.is-ready"), "at once: nothing glides on its way to paper"
    assert css.index("@media print {") > css.index("body.console.is-ready {\n  transition: padding-inline-start"), (
        "the print block stands after the transition it silences: the two rules weigh the same"
    )
    assert "!important" not in _css(SHELL), "by its own weight, never by force"


# -- the builder


def test_a_label_of_the_bar_stands_on_one_run_or_two_split_where_the_longer_run_is_shortest():
    assert services._bar_lines("Menu") == ["Menu"]
    assert services._bar_lines("Communications") == ["Communications"]
    assert services._bar_lines("Tableau de bord") == ["Tableau", "de bord"]
    assert services._bar_lines("Mes documents") == ["Mes", "documents"]
    assert services._bar_lines("Communications (12)") == ["Communications", "(12)"]
    assert services._bar_lines("Demandes qui me sont confiées") == ["Demandes qui me", "sont confiées"]
    assert services._bar_lines("Désignation des professionnels") == ["Désignation des", "professionnels"]
    assert services._bar_lines("Requests entrusted to me") == ["Requests", "entrusted to me"]
    assert services._bar_lines("لوحة المتابعة") == ["لوحة", "المتابعة"]
    for label in ("Tableau de bord", "Demandes qui me sont confiées", "Pannello di riepilogo", "الطلبات المعهودة إليّ"):
        assert " ".join(services._bar_lines(label)) == label, "the words are the live label's, whole, in their order"


def test_a_bar_whose_words_do_not_hold_on_one_line_of_a_phone_draws_them_on_two_runs():
    person_fr = ["Tableau de bord", "Mes dossiers", "Mes documents", "Communications"]
    assert services._bar_stacks(person_fr), "a person's four words need 460 px on one line: two runs each"
    assert services._bar_stacks(["Dashboard", "My case files", "My documents", "Communications"])
    assert not services._bar_stacks(["لوحة المتابعة", "ملفاتي", "وثائقي", "المراسلات"]), "an Arabic bar keeps its line"
    assert not services._bar_stacks(["Tableau de bord", "Communications"]), "and so does a bar of two entries"
    assert not services._bar_stacks(["Analyse territoriale", "Communications"])
    assert not services._bar_stacks([])


@pytest.mark.django_db
def test_one_entry_leaves_a_full_bar_where_the_row_is_too_short_and_a_register_s_bar_sooner(people):
    def bar(who, space=services.SPACE_PERSON):
        return [entry for entry in services.shell_navigation(people[who], space) if entry["bottom"]]

    person = bar("person")
    assert {entry["key"]: entry["yields"] for entry in person} == {
        "dashboard": "",
        "cases": services.YIELDS_NARROW,
        "documents": "",
        "messages": "",
    }, "below 22.5rem a person's bar keeps three: the cases leave (the dashboard opens on the case)"
    for who, register in (
        ("professional", "helpdesk-queue"),
        ("operator", "helpdesk-dispatch"),
        ("actor", "selection"),
    ):
        entries = {entry["key"]: entry["yields"] for entry in bar(who)}
        assert entries == {register: "", "dashboard": "", "documents": services.YIELDS_PHONE, "messages": ""}, (
            f"{who}: with a register's long name on the bar the pieces leave below 30rem, on every phone"
        )
    company = {entry["key"]: entry["yields"] for entry in bar("company")}
    assert company == {"dashboard": "", "documents": services.YIELDS_NARROW, "messages": "", "company": ""}
    for who in people:
        for space in (services.SPACE_PERSON, services.SPACE_COMPANY):
            entries = bar(who, space)
            assert sum(1 for entry in entries if entry["yields"]) == (1 if len(entries) == 4 else 0), (who, space)
            for entry in entries:
                assert " ".join(entry["lines"]) == str(entry["label"]) and 1 <= len(entry["lines"]) <= 2, entry["key"]
                assert entry["stacks"] is services._bar_stacks(
                    [str(e["label"]) for e in entries if e["yields"] != services.YIELDS_PHONE]
                ), (who, space, entry["key"])
            for entry in services.shell_navigation(people[who], space):
                if not entry["bottom"]:
                    assert not entry["yields"] and entry["lines"] == [] and entry["stacks"] is False, entry["key"]
    assert services._bottom_yield(["dashboard", "documents", "messages"]) == ("", "")
    assert services._bottom_yield(["dashboard", "needs", "profile", "messages"]) == ("profile", services.YIELDS_NARROW)


@pytest.mark.django_db
def test_the_company_space_s_bar_is_capped_and_completed_by_the_shell(people, monkeypatch):
    from companies import services as company_services

    # a project reader without a company: the module flags «Communications» alone — the page one is on was missing
    reader = services.shell_navigation(people["superuser"], services.SPACE_COMPANY, "analysis")
    assert [(entry["key"], bool(entry["bottom"])) for entry in reader] == [
        ("analysis", True),
        ("messages", True),
        ("reserved", False),
    ]
    assert [entry["key"] for entry in reader if entry["current"]] == ["analysis"]
    # an account that may still declare its company: the workspace's root and the communications
    bare = services.shell_navigation(people["company"], services.SPACE_COMPANY, "dashboard")
    assert [entry["key"] for entry in bare if entry["bottom"]] == ["dashboard", "messages"]
    assert not any(entry["yields"] for entry in bare), "nothing leaves a bar of two"

    # a module that flagged five: the cap is the shell's
    def five(user, active="", company=None):
        return [
            {
                "key": key,
                "label": key.title(),
                "url": f"/{key}/",
                "current": key == active,
                "icon": "circle",
                "group": "x",
                "bottom": True,
            }
            for key in ("dashboard", "needs", "profile", "analysis", "messages")
        ]

    monkeypatch.setattr(company_services, "navigation", five)
    capped = services.shell_navigation(people["company"], services.SPACE_COMPANY)
    assert [entry["key"] for entry in capped if entry["bottom"]] == ["dashboard", "needs", "profile", "analysis"]
    assert {entry["key"]: entry["yields"] for entry in capped if entry["yields"]} == {"profile": services.YIELDS_NARROW}


# -- every producer, rendered


class _Bar(HTMLParser):
    """The phone's bottom bar of a rendered page: its entries in order, and «Menu»."""

    def __init__(self):
        super().__init__()
        self.inside = False
        self.cell: list[str] = []
        self.entries: list[dict] = []
        self.open: dict | None = None
        self.lists = 0

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        classes = (attributes.get("class") or "").split()
        if tag == "nav" and "console-bottom" in classes:
            self.inside = True
        if not self.inside:
            return
        if tag == "ul" and "console-bottom__list" in classes:
            self.lists += 1
        if tag == "li":
            self.cell = classes
        if tag == "a" and "console-bottom__item" in classes:
            self.open = {
                "href": attributes.get("href", ""),
                "id": attributes.get("id", ""),
                "key": attributes.get("data-key", ""),
                "current": attributes.get("aria-current") == "page",
                "menu": "data-console-menu" in attributes,
                "role": attributes.get("role", ""),
                "cell": self.cell,
                "text": "",
                "runs": 0,
                "stacks": False,
            }
        if self.open is not None and tag == "span" and "console-bottom__line" in classes:
            self.open["runs"] += 1
        if self.open is not None and tag == "span" and "console-bottom__label--stacks" in classes:
            self.open["stacks"] = True

    def handle_data(self, data):
        if self.open is not None:
            self.open["text"] += data

    def handle_endtag(self, tag):
        if self.open is not None and tag == "a":
            self.open["text"] = " ".join(self.open["text"].split())
            self.entries.append(self.open)
            self.open = None
        if self.inside and tag == "nav":
            self.inside = False


def _bar(html: str) -> _Bar:
    parser = _Bar()
    parser.feed(html)
    return parser


@pytest.mark.django_db
@pytest.mark.parametrize(
    "who",
    [
        "person",
        "bare",
        "company",
        "professional",
        "operator",
        "administrator",
        "actor",
        "institution",
        "university",
        "staff",
        "superuser",
    ],
)
def test_every_account_s_bar_holds_four_entries_at_most_and_one_menu_at_its_end(client, seeded, people, who):
    user = people[who]
    client.force_login(user)
    pages = [
        (reverse("portal:dashboard"), services.SPACE_PERSON, "dashboard"),
        (reverse("portal:requests"), services.SPACE_PERSON, "requests"),
    ]
    if who in ("company", "superuser"):
        pages.append((reverse("companies:dashboard"), services.SPACE_COMPANY, "dashboard"))
    for url, space, active in pages:
        response = client.get(url)
        if response.status_code in (301, 302):
            continue  # the company workspace sends an account that cannot use its root elsewhere: not the bar's matter
        assert response.status_code == 200, (who, url, response.status_code)
        html = response.content.decode()
        bar = _bar(html)
        assert bar.lists == 1, "one list in the bar"
        expected = [entry for entry in response.context["portal_nav"] if entry["bottom"]]
        entries, menu = bar.entries[:-1], bar.entries[-1]
        assert len(entries) <= services.NAV_BOTTOM_MAX == 4, (who, url, [entry["text"] for entry in entries])
        assert [entry["key"] for entry in entries] == [entry["key"] for entry in expected], (who, url)
        assert [entry["text"] for entry in entries] == [str(entry["label"]) for entry in expected], (
            "the bar's words are the rail's own labels, whole"
        )
        assert [entry["href"] for entry in entries] == [entry["url"] for entry in expected]
        assert sum(1 for entry in entries if entry["current"]) <= 1, (who, url)
        for entry, source in zip(entries, expected):
            assert entry["runs"] == len(source["lines"]) and entry["stacks"] is bool(source["stacks"]), entry["key"]
            wanted = f"console-bottom__cell--yields-{source['yields']}" if source["yields"] else ""
            assert [name for name in entry["cell"] if "yields" in name] == ([wanted] if wanted else []), entry["key"]
        assert (menu["id"], menu["href"], menu["role"], menu["menu"], menu["text"]) == (
            "console-menu",
            "#console-drawer",
            "",
            True,
            "Menu",
        ), (who, url, menu)
        assert "console-bottom__cell--menu" in menu["cell"], "«Menu» closes the row, at the reading end"
        assert html.count("data-console-menu") == 1, "one control named «Menu» opens the drawer"
        assert html.count('id="console-drawer"') == 1 and 'href="#main-content" data-console-close' in html


@pytest.mark.django_db
def test_the_rendered_drawer_holds_the_whole_rail_and_its_foot(client, seeded, people):
    client.force_login(people["person"])
    html = client.get(reverse("portal:requests")).content.decode()
    drawer = html.split('<dialog class="console-drawer overlay overlay--drawer"', 1)[1].split("</dialog>", 1)[0]
    rails = _rails(html)
    assert [key for key, _current in rails.entries["drawer"]] == TEN and rails.entries["drawer"] == rails.entries[
        "rail"
    ]
    foot = drawer.split('<div class="rail__foot">', 1)[1]
    assert "data-rail-foot" not in drawer and "data-rail-toggle" not in drawer, "the rail's own control is the rail's"
    assert f'href="{reverse("accounts:profile")}"' in foot and "icon-person" in foot and "Personne" in foot
    assert re.search(rf'<form class="rail__signout" method="post" action="{reverse("account_logout")}">', foot)
    assert "csrfmiddlewaretoken" in foot and '<span class="rail__tool-word">Se déconnecter</span>' in foot
    assert re.findall(r'hreflang="([a-z]{2})"', foot) == ["it", "fr", "en", "ar"]
    assert "icon-languages" in foot and f'href="{reverse("pages:home")}"' in foot and "Site public" in foot
    # the top bar: the mark's tile, the level of the page, the account — and no «≡»
    bar = html.split('<header class="portal-bar console-bar"', 1)[1].split("</header>", 1)[0]
    assert re.search(rf'<a class="console-bar__tile" href="{reverse("portal:dashboard")}"', bar)
    assert '<p class="console-bar__title">Mes demandes</p>' in bar and "account-menu" in bar
    assert "data-console-menu" not in bar and "<button" not in bar.split('<div class="account-menu">', 1)[0]
    assert re.search(r'<button class="account-menu__summary" type="button" popovertarget="console-account"[ >]', bar), (
        "the account is the overlay system's popover (W2-A)"
    )


# ---------------------------------------------------------------------------------------------- the review's fixes
#
# The family's one review (docs/design-v5/QA/v54/w3-a/REVIEW.md) and its accessibility and performance check
# (A11Y_PERF.md), held without a browser; the measured halves are in the two browser files.


@pytest.mark.django_db
def test_a_space_starts_where_its_rail_does_a_role_s_register_before_a_person_s_dashboard(people):
    """Review M1: the mark and the phone's tile took the administrator and every role account to a person's
    dashboard, whose one thing to do is «Commencer le questionnaire». «Espace réservé» starts where its rail does:
    at the first entry of «Mon rôle» for an account that holds a register, at the dashboard for every other one."""
    dashboard = reverse("portal:dashboard")
    registers = {
        "professional": reverse("helpdesk:queue"),
        "operator": reverse("helpdesk:dispatch"),
        "administrator": reverse("helpdesk:dispatch"),
        "actor": reverse("selection:workspace"),
        "superuser": reverse("selection:workspace"),  # offered every register: the rail's first
    }
    for who, user in people.items():
        start = registers.get(who, dashboard)
        rail = services.shell_navigation(user)
        assert services.shell_space(user)["url"] == start, who
        assert {entry["space"]["url"] for entry in rail} == {start}, (who, "one start for every entry's plate")
        first = next(entry for entry in rail if entry["kind"] == services.KIND_PAGE)
        assert first["url"] == start, (who, "the mark leads where the rail starts")
        if who in registers:
            assert first["group"] == "Mon rôle", who
            assert [entry["url"] for entry in rail if entry["key"] == "dashboard"] == [dashboard], (
                who,
                "the dashboard stays one key away, under «Parcours»",
            )
    back = services.shell_navigation(people["company"], services.SPACE_COMPANY)[-1]
    assert (back["kind"], back["url"]) == (services.KIND_SPACE, dashboard), "the way back is the same start"


@pytest.mark.django_db
def test_where_the_space_starts_costs_no_query_once_the_roles_are_read(people, django_assert_num_queries):
    held = roles.roles_of(people["operator"])
    with django_assert_num_queries(0):
        plate = services.shell_space(people["operator"], held=held)
    assert plate["url"] == reverse("helpdesk:dispatch")


@pytest.mark.django_db
def test_the_mark_the_tile_and_the_drawer_s_mark_lead_to_the_space_s_start(client, seeded, people):
    for who, start in (("operator", reverse("helpdesk:dispatch")), ("person", reverse("portal:dashboard"))):
        client.force_login(people[who])
        html = client.get(reverse("portal:requests")).content.decode()
        marks = re.findall(r'<a class="(rail__brand|console-bar__tile)" href="([^"]+)"', html)
        assert marks == [("rail__brand", start), ("console-bar__tile", start), ("rail__brand", start)], (who, marks)


@pytest.mark.django_db
def test_a_space_s_first_page_ends_its_trail_on_itself_and_never_links_to_the_page_one_is_on(client, seeded, people):
    """Review m3: on a space's first page the rail lit «Tableau de bord» while the trail ended on the space's name.
    The trail ends on the page, as it does everywhere else; the space's name is no link to the page one is on."""
    client.force_login(people["company"])
    for name, space in (("portal:dashboard", "Espace réservé"), ("companies:dashboard", "Espace entreprise")):
        response = client.get(reverse(name))
        assert response.context["breadcrumbs"] == [
            {"label": space, "url": ""},
            {"label": "Tableau de bord", "url": ""},
        ], name
        assert [entry["key"] for entry in response.context["portal_nav"] if entry["current"]] == ["dashboard"], name
        bar = response.content.decode().split('<header class="portal-bar console-bar"', 1)[1].split("</header>", 1)[0]
        assert re.search(r'<li class="breadcrumbs__item" aria-current="page">\s*<span>Tableau de bord</span>', bar), (
            name
        )
        assert f'<a href="{reverse(name)}">' not in bar, (name, "no link to the page one is on")
        assert '<p class="console-bar__title">Tableau de bord</p>' in bar, (name, "the phone's top bar says the page")
    trail = client.get(reverse("portal:requests")).context["breadcrumbs"]
    assert trail[0] == {"label": "Espace réservé", "url": reverse("portal:dashboard")}, "a link on every other page"


def test_the_sheet_holds_the_review_s_fixes():
    css = _css(SHELL)
    # m1 — the list's scroll edge: two images named in the night's own tokens (an app sheet draws no gradient), the
    # rail's night travelling with the list's end (`local`) over a band fixed to the box's end (`scroll`); no script
    # reads it and nothing of it moves
    edge = re.search(r"\.rail__scroll \{\s*background:([^}]*)\}", css).group(1)
    layers = [" ".join(layer.split()) for layer in edge.strip().rstrip(";").split(",")]
    assert layers == [
        "var(--rail-scroll-cover) center bottom / 100% calc(var(--s-6) + var(--s-4)) no-repeat local",
        "var(--rail-scroll-edge) center bottom / 100% var(--s-6) no-repeat scroll",
    ], layers
    tokens = re.sub(r"/\*.*?\*/", "", _read(ROOT / "static" / "css" / "v5" / "tokens.css"), flags=re.S)
    assert "--rail-scroll-edge: linear-gradient(transparent, var(--surface-night-sheet));" in tokens
    assert "--rail-scroll-cover: linear-gradient(transparent, var(--rail-bg) var(--s-4));" in tokens, (
        "the cover's solid run (24 px) is the band's height: at the list's end nothing of the band shows"
    )
    # m2 — the ContextHeader's line above its title hugs its words, bounded by the frame
    greeting = re.search(r"\.console__workspace > \.ctx \.ctx__greeting \{([^}]*)\}", css).group(1)
    assert "inline-size: fit-content;" in greeting and "max-inline-size: 100%;" in greeting
    # A11Y M1 — the footer's legal pages are targets: 24 px at least, 44 under a finger
    footer = re.search(r"\.console__footer a \{([^}]*)\}", css).group(1)
    assert "display: inline-flex;" in footer and "min-block-size: 24px;" in footer
    touch = re.search(r"@media \(pointer: coarse\) \{(.*?)\n\}", css, flags=re.S).group(1)
    footer_touch = re.search(r"\.console__footer a \{([^}]*)\}", touch).group(1)
    assert (
        "min-block-size: var(--control-md);" in footer_touch and "min-inline-size: var(--control-md);" in footer_touch
    )
    # A11Y m1 — the rows of the account's menu in the phone's top bar, 44 under a finger: the overlay system's
    # popover since W2-A (its rows `.overlay__item`, 44 px under a coarse pointer)
    assert '{% include "components/account_menu.html" with popover=True menu_id="console-account" %}' in _read(CHROME)
    overlays_css = re.sub(r"/\*.*?\*/", "", _read(ROOT / "static" / "css" / "v5" / "overlays.css"), flags=re.S)
    assert re.search(
        r"@media \(pointer: coarse\) \{\s*\.overlay__item \{ min-block-size: var\(--hit-primary\); \}", overlays_css
    )
    # A11Y m2 — a skip link's ring is drawn inside its navy box
    assert re.search(
        r"\.console \.skip-link:focus-visible \{\s*outline-offset: calc\(-2 \* var\(--focus-ring-width\)\);", css
    )
    # A11Y m4 — in the band the account's name beside its glyph goes on a second line rather than lose its end
    band = re.search(r"@media \(min-width: 48rem\) and \(max-width: 63\.999rem\) \{(.*?)\n\}", css, flags=re.S).group(1)
    name = re.search(r"\.console-bar \.account-menu__name \{([^}]*)\}", band).group(1)
    assert "white-space: normal;" in name and "overflow-wrap: anywhere;" in name
