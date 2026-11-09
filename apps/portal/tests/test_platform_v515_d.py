"""
V5.15 lane D — the platform's design energy (docs/design-v5/QA/v515/d/NOTES.md; DECISIONS §15 lane D).

* The ATRIUM: every console page of the space opens on one composed head (`data-atrium`), its drawing decorative
  (hidden from assistive technology, never focusable), the page's own h1 unchanged.
* The LATTICE (21st 27082, adapted): the file's progress is the checklist's two counts and a ring drawn from them —
  never a percentage in words, never a figure the system does not hold —; the step the file stands on, in the
  catalogue's words; a held file (suspended, closed) has no «Où j'en suis» cell. The side column is one lattice: the
  dates (the next one set large, decorative) and the communications, each only with rows.
* The organisation space: the identity plate in the head, the calm state composed, «Le projet» as tiles.
* The page-only sheet and module: linked by the pages that draw them, never by the shared bundles; tokens only, no
  inline style (CSP), motion on duration tokens under the reduced-motion guards.
* Terminology: the glossary's rows of this pass, and §9's two corrections («Échanges», «Votre rôle»).
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from django.utils import translation

from accounts import roles
from accounts.models import Membership, MembershipRole, Organisation
from cases import services as case_services
from cases.models import CasePurpose, CaseStatus, ResponsibleActor
from portal import services

pytestmark = pytest.mark.django_db

ROOT = Path(__file__).resolve().parents[3]
SHEET = ROOT / "apps" / "portal" / "static" / "portal" / "v5" / "_platform.css"
ENTRY = ROOT / "apps" / "portal" / "static" / "portal" / "platform.css"
MODULE = ROOT / "static" / "js" / "src" / "platform.js"
DASHBOARD = "/{lang}/espace-reserve/"
LANGS = ("fr", "it", "en", "ar")


@pytest.fixture
def case(alice):
    return case_services.open_case(alice, purpose=CasePurpose.WORK, pathway_key="salaried_work")


@pytest.fixture
def institution(user_factory):
    user = user_factory(
        "v515d.institution@example.test", role=roles.INSTITUTION, full_name="Ufficio", account_type="institution"
    )
    org = Organisation.objects.create(name="Comune di Valfiorita", kind="institution", country="Italia", city="Rovigo")
    Membership.objects.create(user=user, organisation=org, role=MembershipRole.OWNER)
    return user


def _html(client, lang="fr", path=DASHBOARD):
    response = client.get(path.format(lang=lang))
    assert response.status_code == 200
    return response.content.decode("utf-8")


def _head(html):
    """The page's own head (the workspace's first <header>, after the console's bar): the one that carries the h1."""
    match = re.search(r'<header class="(?:ctx|ws-head)[^"]*"[^>]*>.*?</header>', html, flags=re.S)
    assert match, "the page has its head"
    return match.group(0)


# ---- the atrium ----------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("lang", LANGS)
def test_the_dashboard_opens_on_the_atrium_with_a_decorative_drawing(client, alice, case, lang):
    client.force_login(alice)
    html = _html(client, lang)
    head = _head(html)
    assert 'data-atrium="person"' in head
    art = head.split('<div class="atrium__art"', 1)[1].split("</div>", 1)[0]
    assert 'aria-hidden="true"' in art.split(">", 1)[0] and 'focusable="false"' in art
    assert "<text" not in art and "<title" not in art, "the drawing says no word"
    assert html.count("<h1") == 1 and case.reference in head
    with translation.override(lang):
        assert str(roles.space_label(alice)) in head, "the eyebrow is the space's name"


@pytest.mark.parametrize(
    "path",
    [
        "/fr/espace-reserve/mes-demandes/",
        "/fr/espace-reserve/communications/",
        "/fr/espace-reserve/mes-echeances/",
        "/fr/espace-reserve/mon-parcours/",
    ],
)
def test_the_registers_pages_open_on_the_atrium_and_load_the_page_only_sheet(client, alice, path):
    client.force_login(alice)
    response = client.get(path, follow=True)
    assert response.status_code == 200
    html = response.content.decode("utf-8")
    assert "data-atrium=" in _head(html)
    assert html.count("css/dist/portal/platform.css") == 1
    assert html.count("js/dist/platform.js") == 1


@pytest.mark.parametrize(
    "path",
    [
        "/fr/espace-reserve/mes-demandes/",
        "/fr/espace-reserve/communications/",
        "/fr/espace-reserve/mes-echeances/",
        "/fr/espace-reserve/mon-parcours/",
        "/fr/espace-reserve/ma-situation/",
        "/fr/espace-reserve/dossiers/",
        "/fr/espace-reserve/guichet/",
        "/fr/espace-reserve/formation/",
        "/fr/espace-reserve/formation/mes-formations/",
    ],
)
def test_every_atrium_page_says_its_space_in_the_eyebrow(client, alice, path):
    """Round 1: the eyebrow was drawn on the dashboards only. Round 2: 12 of 19 pages showed the fallback «Espace
    réservé» — every atrium page now says the SAME word as the account's dashboard."""
    client.force_login(alice)
    response = client.get(path, follow=True)
    assert response.status_code == 200
    html = response.content.decode("utf-8")
    head = _head(html)
    assert "data-atrium=" in head and re.search(r'<div class="atrium__art" aria-hidden="true" data-figure="\w+">', head)
    # v524-plat (V5.20; V5.24 §11–§14; TYPOGRAPHY_V2 F-4; FINAL_DELIVERY_V2 §3.7): the eyebrow carries the label role by
    # name — the same word, and the role
    assert '<p class="atrium__eyebrow t-label">Espace Personnes</p>' in head, "the dashboard's word, not the fallback"
    assert html.count("<h1") == 1
    assert html.count("css/dist/portal/platform.css") == 1


ATRIUM_PAGES = [
    "/{lang}/espace-reserve/",
    "/{lang}/espace-reserve/mes-demandes/",
    "/{lang}/espace-reserve/communications/",
    "/{lang}/espace-reserve/mes-echeances/",
    "/{lang}/espace-reserve/mon-parcours/",
    "/{lang}/espace-reserve/ma-situation/",
    "/{lang}/espace-reserve/dossiers/",
    "/{lang}/espace-reserve/mes-documents/",
    "/{lang}/espace-reserve/guichet/",
    "/{lang}/espace-reserve/formation/",
    "/{lang}/espace-reserve/formation/mes-formations/",
]


def _eyebrow(head):
    # v524-plat (V5.20; TYPOGRAPHY_V2 F-4; FINAL_DELIVERY_V2 §3.7): the eyebrow is the label role by name (`t-label`)
    match = re.search(r'<p class="(?:ctx__eyebrow )?atrium__eyebrow t-label">([^<]+)</p>', head)
    assert match, "the head has its eyebrow"
    return match.group(1)


@pytest.mark.parametrize("lang", LANGS)
def test_every_atrium_pages_eyebrow_equals_the_dashboards_in_four_languages(client, alice, case, lang):
    """Round 2's major: the eyebrow is the account's space name on every page — the dashboard's word, in its
    language (portal.services.atrium_space_label), never the fallback."""
    client.force_login(alice)
    dashboard = _eyebrow(_head(_html(client, lang)))
    with translation.override(lang):
        assert dashboard == str(roles.space_label(alice))
        fallback = translation.gettext("Espace réservé")
    for path in ATRIUM_PAGES[1:] + [f"/{{lang}}/espace-reserve/dossiers/{case.reference}/"]:
        response = client.get(path.format(lang=lang), follow=True)
        assert response.status_code == 200, path
        html = response.content.decode("utf-8")
        if "data-atrium=" not in html:
            continue  # a page another route answers for (a redirect to the dashboard)
        assert _eyebrow(_head(html)) == dashboard != fallback, f"{lang} {path}"


@pytest.mark.parametrize("lang", LANGS)
def test_an_organisations_pages_say_the_organisations_space(client, institution, lang):
    client.force_login(institution)
    dashboard = _eyebrow(_head(_html(client, lang)))
    with translation.override(lang):
        assert dashboard == str(services.ORGANISATION_SPACE_LABELS["institution"])
    for path in ("/{lang}/espace-reserve/mon-organisation/", "/{lang}/espace-reserve/communications/"):
        response = client.get(path.format(lang=lang), follow=True)
        assert response.status_code == 200
        assert _eyebrow(_head(response.content.decode("utf-8"))) == dashboard


@pytest.mark.parametrize(
    ("path", "figure"),
    [
        ("/fr/espace-reserve/", "route"),
        ("/fr/espace-reserve/mon-parcours/", "route"),
        ("/fr/espace-reserve/mes-echeances/", "route"),
        ("/fr/espace-reserve/mes-demandes/", "counter"),
        ("/fr/espace-reserve/guichet/", "counter"),
        ("/fr/espace-reserve/communications/", "exchange"),
        ("/fr/espace-reserve/mes-documents/", "sheets"),
        ("/fr/espace-reserve/formation/", "thresholds"),
        ("/fr/espace-reserve/formation/mes-formations/", "thresholds"),
    ],
)
def test_each_family_of_pages_draws_its_own_figure(client, alice, case, path, figure):
    """Round 2's major: one portico pasted on 30 pages — each family now has its figure in the atrium's grammar (a
    door, its keyhole, the route that reaches it), and on a phone the band (the route, its stations, the door)."""
    client.force_login(alice)
    response = client.get(path, follow=True)
    assert response.status_code == 200
    head = _head(response.content.decode("utf-8"))
    assert f'data-figure="{figure}"' in head
    art = head.split('<div class="atrium__art"', 1)[1].split("</svg></div>", 1)[0]
    parts = ('class="atrium__door"', 'class="atrium__route"', 'class="atrium__light"', '<g class="atrium__keyhole">')
    for part in parts:
        assert art.count(part) == 1, part
    assert '<div class="atrium__band" aria-hidden="true">' in head and 'class="atrium__band-door"' in head
    assert "<text" not in head.split('<div class="atrium__art"', 1)[1], "the drawing says no word"


def test_the_route_figure_lights_the_files_own_step(client, alice, case):
    client.force_login(alice)
    head = _head(_html(client))
    at = services.journey_at(services.journey_for(case))["n"]
    art = head.split('<div class="atrium__art"', 1)[1].split("</svg></div>", 1)[0]
    stations = re.findall(r'<circle class="atrium__station([^"]*)"', art)
    assert len(stations) == 7, "the journey's seven stations"
    assert [i for i, c in enumerate(stations, start=1) if "--here" in c] == [at]
    assert [i for i, c in enumerate(stations, start=1) if "--done" in c] == list(range(1, at))
    # the case file draws the same step
    file_head = _head(_html(client, path=f"/fr/espace-reserve/dossiers/{case.reference}/"))
    file_art = file_head.split('<div class="atrium__art"', 1)[1].split("</svg></div>", 1)[0]
    lit = [i for i, c in enumerate(re.findall(r'<circle class="atrium__station([^"]*)"', file_art), 1) if "--here" in c]
    assert lit == [at]


def test_an_organisations_seal_stands_in_the_central_arch(client, institution):
    from core import icons

    client.force_login(institution)
    head = _head(_html(client))
    assert 'data-figure="seal"' in head
    glyph = re.search(r'<use class="atrium__glyph-icon" href="[^"]+#icon-([\w-]+)" x="150" y="52"', head)
    assert glyph and glyph.group(1) == icons.resolve(icons.AUDIENCE["institution"])


def test_the_case_file_opens_on_the_atrium(client, alice, case):
    client.force_login(alice)
    html = _html(client, path=f"/fr/espace-reserve/dossiers/{case.reference}/")
    head = _head(html)
    assert 'data-atrium="person"' in head and case.reference in head and "atrium__eyebrow" in head
    assert html.count("css/dist/portal/platform.css") == 1


def test_the_guichets_head_keeps_its_action_and_a_short_lead(client, alice):
    """Round 2: the head's lead is the Guichet's first sentence; the second (catalogue copy) closes the page with
    its clause — the phone's head no longer pushes the list to the fold."""
    client.force_login(alice)
    html = _html(client, path="/fr/espace-reserve/guichet/")
    head = _head(html)
    assert 'data-atrium="register"' in head
    assert head.index('class="atrium__art"') < head.index('class="ws-head__action"'), "the action is the head's own"
    assert '<p class="ws-head__lead">Poser une question à une personne, pas à une machine.</p>' in head
    clause = html.split('<p class="reg-note">', 1)[1].split("</p>", 1)[0]
    assert clause.startswith("Aucune réponse n’est produite automatiquement") and "oriente et transmet" in clause


def test_the_academys_counts_are_a_lattice(client, alice, monkeypatch):
    """Round 1: «Où j'en suis» was a flat strip — three cells, each its count set large under its word."""
    monkeypatch.setattr("academy.services.summary", lambda user: {"ongoing": 2, "completed": 1, "plans": 0})
    client.force_login(alice)
    html = _html(client, path="/fr/espace-reserve/formation/")
    counts = html.split('<dl class="lattice__grid lattice__grid--counts">', 1)[1].split("</dl>", 1)[0]
    assert re.findall(r'<dd class="lattice__figure">(\d+)</dd>', counts) == ["2", "1", "0"]
    assert counts.count('class="lattice__cell lattice__cell--link" data-spot') == 3
    # round 2: each count is the way to its register on «Mes formations», a glyph in its container
    links = re.findall(r'<a class="lattice__go" href="([^"]+)">', counts)
    assert links == [
        "/fr/espace-reserve/formation/mes-formations/#mine-ongoing-title",
        "/fr/espace-reserve/formation/mes-formations/#mine-done-title",
        "/fr/espace-reserve/formation/mes-formations/#mine-plans-title",
    ]
    assert counts.count('<span class="lattice__glyph" aria-hidden="true">') == 3
    assert html.count("js/dist/platform.js") == 1


# ---- the lattice ---------------------------------------------------------------------------------------------------
def test_progress_figure_is_the_checklist_counts_never_an_invented_percentage():
    assert services.progress_figure(None) is None
    assert services.progress_figure({"total": 0, "done": 0}) is None
    figure = services.progress_figure({"total": 5, "done": 2})
    assert {k: figure[k] for k in ("done", "total", "arc")} == {"done": 2, "total": 5, "arc": 40}
    assert services.progress_figure({"total": 3, "done": 3})["arc"] == 100


def test_the_ring_is_segmented_one_segment_per_item_up_to_twelve():
    """Round 1: at «0 sur 5» an unbroken grey circle read as a spinner — one segment per item, 2-unit gaps."""
    segments = services.progress_figure({"total": 5, "done": 2})["segments"]
    assert [seg["done"] for seg in segments] == [True, True, False, False, False]
    assert {seg["dash"] for seg in segments} == {"18.00 100"}
    assert [seg["offset"] for seg in segments] == ["-1.00", "-21.00", "-41.00", "-61.00", "-81.00"]
    assert len(services.progress_figure({"total": 12, "done": 0})["segments"]) == 12
    assert services.progress_figure({"total": 13, "done": 4})["segments"] == [], "a continuous arc beyond twelve"


def test_journey_at_names_the_current_step_in_the_catalogues_words(alice, case):
    journey = services.journey_for(case)
    at = services.journey_at(journey)
    current = [i for i, step in enumerate(journey, start=1) if step["is_current"]]
    assert at["n"] == current[0] and at["total"] == len(journey) == 7
    assert at["words"] == f"Étape {at['n']} sur 7"
    assert services.journey_at([]) is None


def _line(case, n=0):
    return case_services.add_checklist_item(
        case, requirement=f"Élément {n}", responsible_actor=ResponsibleActor.AUTHORITY
    )


@pytest.mark.parametrize("lang", LANGS)
def test_the_files_lattice_draws_its_ring_and_never_repeats_the_journeys_step(client, alice, case, lang):
    for i in range(4):
        _line(case, i)
    client.force_login(alice)
    html = _html(client, lang)
    lattice = html.split('<section class="db-file lattice"', 1)[1].split("</section>", 1)[0]
    at = services.journey_at(services.journey_for(case))
    with translation.override(lang):
        step = translation.gettext("Étape %(n)s sur %(total)s") % {"n": at["n"], "total": 7}
        assert translation.gettext("Avancement") in lattice
        # round 1: the journey is drawn on this screen — its step is said there, never again in the lattice
        assert 'class="db-journey"' in html and step not in lattice
    assert "lattice__cell--step" not in lattice and "lattice__tick" not in lattice
    assert 'class="lattice__grid lattice__grid--file"' in lattice
    dial = lattice.split('<span class="ring-dial"', 1)[1].split("</svg>", 1)[0]
    assert 'aria-hidden="true"' in dial and dial.count('class="ring__seg"') == 4, "one segment per item, none done"
    # round 2: the count stands in the ring — a dial, never a spinner (decorative: the words beside it say it)
    assert re.search(r'<span class="ring-dial__count">0<span>/4</span></span>', lattice)
    assert "%" not in re.sub(r"<[^>]+>", "", lattice), "no percentage in words"
    assert " style=" not in lattice, "no inline style: the CSP allows none"


def test_a_ring_with_nothing_done_draws_its_segments_as_hairlines(client, alice, case):
    _line(case)
    _line(case, 1)
    client.force_login(alice)
    lattice = _html(client).split('<section class="db-file lattice"', 1)[1].split("</section>", 1)[0]
    assert lattice.count('class="ring__seg"') == 2 and "ring__seg--done" not in lattice
    assert 'class="ring__arc"' not in lattice


def test_without_a_checklist_no_ring_is_drawn(client, alice, case):
    client.force_login(alice)
    lattice = _html(client).split('<section class="db-file lattice"', 1)[1].split("</section>", 1)[0]
    assert '<svg class="ring"' not in lattice


@pytest.mark.parametrize("state", ["suspended", "closed"])
def test_a_held_file_has_no_step_cell(client, alice, case, state):
    case_services.transition(case, CaseStatus.ORIENTED)
    if state == "suspended":
        case_services.transition(case, CaseStatus.SUSPENDED, actor=alice, reason="En attente")
    else:
        case_services.transition(case, CaseStatus.CLOSED, actor=alice)
    client.force_login(alice)
    html = _html(client)
    assert "lattice__cell--step" not in html and "lattice__tick--here" not in html


def test_the_side_lattice_sets_the_next_date_large_and_keeps_the_list(client, alice, case, make_deadline, make_message):
    make_deadline(alice, title="Dépôt Alice", days=3)
    make_deadline(alice, title="Rendez-vous Alice", days=20)
    make_message(alice, subject="Convocation Alice")
    client.force_login(alice)
    html = _html(client)
    # V5.20 strict rule, V5.30 §13 (the role dashboards' recent activity): the panel may carry db-side--tall beside its
    # own class, so the anchor stops at the class name; the same invariant on the same panel
    side = html.split('<div class="db-side db-side--lattice', 1)[1]
    nxt = side.split('<p class="db-next', 1)[1].split("</p>", 1)[0]
    assert 'aria-hidden="true"' in nxt, "the large date is decorative: the list says it"
    assert "Dépôt Alice" in side and "Rendez-vous Alice" in side and "Convocation Alice" in side
    assert side.count('<section class="db-dates" aria-labelledby="db-dates-title" data-spot>') == 1
    assert side.count('<section class="db-messages" aria-labelledby="db-messages-title" data-spot>') == 1
    assert "db-calm-cell" not in side


def test_the_side_lattice_with_nothing_is_one_calm_cell(client, alice):
    # a fresh account: no file (opening one sends a communication), no date, no communication
    client.force_login(alice)
    html = _html(client)
    side = html.split('<div class="db-side db-side--lattice"', 1)[1].split('<div class="db-folds">', 1)[0]
    assert side.count('<div class="db-calm-cell" data-spot>') == 1
    assert 'id="db-dates-title"' not in side and 'id="db-messages-title"' not in side


# ---- the organisation space ----------------------------------------------------------------------------------------
@pytest.mark.parametrize("lang", LANGS)
def test_the_organisation_head_carries_its_identity_plate_and_the_tiles(client, institution, lang):
    client.force_login(institution)
    html = _html(client, lang)
    head = _head(html)
    assert 'data-atrium="institution"' in head
    assert 'class="org-head__name atrium__plate"' in head and "Comune di Valfiorita" in head
    assert 'class="atrium__seal" aria-hidden="true"' in head
    assert "org-calm" in html and 'class="org-calm__art"' in html
    tiles = html.split("org-refs--tiles", 1)[1].split("</nav>", 1)[0]
    indices = re.findall(r'class="org-refs__index" aria-hidden="true">(\d\d)<', tiles)
    assert indices == [f"{n:02d}" for n in range(1, len(indices) + 1)] and indices, "01, 02 … in order"
    assert len(indices) == tiles.count('class="org-refs__link"'), "one index per open public page"


@pytest.mark.parametrize("lang", LANGS)
def test_the_organisations_presentation_is_folded_verbatim_under_its_word(client, institution, lang):
    from cms import locked_content

    client.force_login(institution)
    html = _html(client, lang)
    head = _head(html)
    with translation.override(lang):
        word = translation.gettext("Présentation")
    assert f'<details class="atrium__intro"><summary>{word}</summary>' in head
    text = locked_content.text("p3.institutions.intro", lang)
    if lang == "ar":
        # V5.27 (FINAL_DELIVERY_V2 R7′; V5.20, the steward's amendment at the v524-ar merge): a compositional text
        # (C-UI) — its provisional Arabic rendering, drawn by {% locked %} with the brand's run as one LTR unit (bdi);
        # the same rendering, once, never retyped
        from django.template import engines

        from cms import locked_renderings

        assert text == locked_renderings.rendering("p3.institutions.intro")
        with translation.override(lang):
            text = engines["django"].from_string('{% locked "p3.institutions.intro" %}').render({})
        assert '<bdi dir="ltr">' in text
    assert head.count(text) == 1 and html.count(text) == 1, "the locked text, once, never retyped"


def test_mon_organisation_opens_on_the_atrium_with_its_tiles(client, institution):
    client.force_login(institution)
    html = _html(client, path="/fr/espace-reserve/mon-organisation/")
    assert 'data-atrium="institution"' in _head(html)
    assert "org-id--lattice" in html and "org-refs--tiles" in html


# ---- the sheet and the module --------------------------------------------------------------------------------------
def test_the_platform_sheet_is_page_only_and_never_in_a_shared_bundle():
    assert '@import url("v5/_platform.css");' in ENTRY.read_text(encoding="utf-8")
    for shared in (
        ROOT / "static" / "css" / "main.css",
        ROOT / "apps" / "portal" / "static" / "portal" / "console.css",
    ):
        assert "_platform.css" not in shared.read_text(encoding="utf-8")
    built = ROOT / "static" / "css" / "dist" / "portal" / "platform.css"
    assert built.exists() and ".lattice__grid" in built.read_text(encoding="utf-8")


def test_the_platform_motion_is_guarded_and_on_tokens():
    css = SHEET.read_text(encoding="utf-8")
    assert "!important" not in css
    motion = css.split("/* ---- 6 · Motion", 1)[1].split("/* ---- 7 · States", 1)[0]
    guarded = motion.split("@media (prefers-reduced-motion: no-preference) {", 1)[1]
    for animation in re.findall(r"animation:\s*([^;]+);", guarded):
        assert "html:not(.rm)" in guarded
        assert re.search(r"var\(--motion-[a-z-]+\)", animation) or animation.startswith("plat-rise linear"), animation
    # nothing animates outside the guard
    assert not re.findall(r"animation:", motion.split("@media (prefers-reduced-motion: no-preference) {", 1)[0])
    assert "@media (forced-colors: active)" in css and "@media print" in css
    # the envelope is finite: nothing loops, nothing is scroll-linked (a view() timeline never ends: the page would
    # never be at rest for its pointer); the NowPanel, the screen's action, never fades in
    assert "infinite" not in css and "animation-timeline" not in css
    assert ".db-now" not in guarded
    # SH-2 / SH-8 and plan §1.3: no shadow at rest (a tile's depth is a hover state); corners 8 · 4 · full
    # round 1: not even on hover — a tile answers with its border's step and the spotlight; the NowPanel stays the one
    # raised plane. Corners 8 · 4 · full, never a raw radius; colours from tokens (no raw rgba)
    assert "box-shadow: var(--shadow" not in css
    assert not re.search(r"org-refs__link:hover \{[^}]*transform", css), "a tile never lifts"
    assert "--radius-xl" not in css and "--radius-md" not in css
    assert not re.findall(r"border-radius:\s*[1-9]\d*px", css), "a raw radius"
    assert "rgba(" not in css


def test_a_dashed_stroke_never_carries_a_non_scaling_stroke():
    """Round 1's major: with `vector-effect: non-scaling-stroke` Chromium reads a dash in screen pixels, not on
    pathLength — the arches lost their legs at rest, the door stood open, the route stopped short. Only the undashed
    strokes (the grid, the stations) keep it; the light is not drawn at rest; the keyhole is its own group."""
    css = re.sub(r"/\*.*?\*/", "", SHEET.read_text(encoding="utf-8"), flags=re.S)
    for selector, body in re.findall(r"([^{}]+)\{([^{}]*)\}", css):
        if "vector-effect" in body:
            assert "stroke-dasharray" not in body, selector
            assert {part.strip() for part in selector.split(",")} <= {
                ".atrium__grid path",
                ".atrium__stations circle",
                ".atrium__band-stations circle",
                ".atrium__halo",
            }
    light = re.search(r"\n\.atrium__light,\n\.atrium__band-light \{([^}]*)\}", css).group(1)
    assert "opacity: 0;" in light
    art = (ROOT / "templates" / "portal" / "partials" / "atrium_art.html").read_text(encoding="utf-8")
    assert "vector-effect" not in art.split("{% endcomment %}", 1)[1]
    assert '<g class="atrium__keyhole">' in art


def test_the_spotlight_module_writes_only_two_properties_and_ignores_touch_and_keys():
    js = MODULE.read_text(encoding="utf-8")
    assert re.findall(r'setProperty\("([^"]+)"', js) == ["--spot-x", "--spot-y"]
    assert 'event.pointerType !== "mouse"' in js
    assert "keydown" not in js and "focus" not in js.split("*/", 1)[1]


# ---- terminology ---------------------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    ("lang", "word"), [("it", "Comunicazioni"), ("en", "Communications"), ("ar", "التبادلات"), ("fr", "Échanges")]
)
def test_the_rails_exchanges_section_has_its_glossary_name(lang, word):
    with translation.override(lang):
        assert translation.gettext("Échanges") == word


def test_votre_role_speaks_the_lei_register_in_italian():
    with translation.override("it"):
        assert translation.gettext("Votre rôle") == "Il suo ruolo"


# ---- finishing round F1 ----------------------------------------------------------------------------------------------
@pytest.fixture
def company(user_factory):
    user = user_factory(
        "v515d.company@example.test", role=roles.COMPANY, full_name="Giulia", account_type="company"
    )
    org = Organisation.objects.create(name="Cantiere Adriatico S.r.l.", kind="company", country="Italia", city="Rovigo")
    Membership.objects.create(user=user, organisation=org, role=MembershipRole.OWNER)
    return user


def _figure_html(figure, atrium_at=None):
    from django.template.loader import render_to_string

    return render_to_string("portal/partials/atrium_art.html", {"figure": figure, "atrium_at": atrium_at})


def _end_point(d):
    """The last point of an absolute SVG path (M, L, H, V, C, A — the drawing's own commands)."""
    x = y = 0.0
    for cmd, args in re.findall(r"([MLHVCA])([^MLHVCA]*)", d):
        nums = [float(n) for n in re.findall(r"-?\d+(?:\.\d+)?", args)]
        if cmd == "H":
            x = nums[-1]
        elif cmd == "V":
            y = nums[-1]
        elif nums:
            x, y = nums[-2], nums[-1]
    return x, y


@pytest.mark.parametrize("figure", ["route", "counter", "thresholds", "sheets", "exchange", "seal", ""])
def test_every_figures_route_and_light_arrive_at_the_doors_threshold(figure):
    """F1: the counter's route ended 27–40 px under the door, between the counter's legs — the light arrived at
    nothing. On every figure the route and the light end on the door's threshold (|Δy| ≤ 2), between its legs."""
    art = _figure_html(figure, 3).split('<div class="atrium__band"', 1)[0]
    door = re.search(r'class="atrium__door" d="([^"]+)"', art).group(1)
    legs = [float(v) for v in re.findall(r"M(-?[\d.]+) ", door)] + [_end_point(door)[0]]
    threshold = max(float(v) for v in re.findall(r"V(-?[\d.]+)", door))
    for cls in ("atrium__route", "atrium__light"):
        end_x, end_y = _end_point(re.search(rf'class="{cls}" d="([^"]+)"', art).group(1))
        assert abs(end_y - threshold) <= 2, (figure, cls, end_y, threshold)
        assert min(legs) < end_x < max(legs), (figure, cls, end_x, legs)


@pytest.mark.parametrize(
    ("figure", "motif"),
    [("counter", "M130 18 V10 H194"), ("thresholds", "M120 18 V14 H146"), ("sheets", "M146 18 V7"),
     ("exchange", "M150 22 V11"), ("seal", "M168 11"), ("", "M140 22 V12")],
)
def test_the_phones_band_draws_the_familys_motif_and_never_a_done_station_without_data(figure, motif):
    """F1: phones drew the same seven-station journey on every family, station 1 «done» with no data."""
    band = _figure_html(figure).split('<div class="atrium__band"', 1)[1]
    assert f'class="atrium__band-motif" d="{motif}' in band
    assert "atrium__station--done" not in band and "atrium__station--here" not in band
    assert band.count('<circle class="atrium__station') < 7


def test_the_route_band_marks_only_the_files_own_steps_and_rings_the_current_one():
    band = _figure_html("route").split('<div class="atrium__band"', 1)[1]
    assert band.count('<circle class="atrium__station') == 7 and "--done" not in band and "atrium__halo" not in band
    lit = _figure_html("route", 3)
    assert lit.count('class="atrium__halo" data-at="3"') == 2, "the drawing's and the band's ring"
    band = lit.split('<div class="atrium__band"', 1)[1]
    assert band.count("atrium__station--done") == 2 and band.count("atrium__station--here") == 1


@pytest.mark.parametrize("lang", LANGS)
def test_a_companys_dashboard_is_composed_never_a_bare_list(client, company, lang):
    """F1 (major): under a composed atrium the company persona's dashboard was one link, one sentence and two lines
    between hairlines. Now: the seal figure with the company's glyph, the calm panel whose way on is «Espace
    entreprise», the identity sheet (seal, name, facts), the account line as the sheet's foot — once."""
    from core import icons

    client.force_login(company)
    html = _html(client, lang)
    head = _head(html)
    assert 'data-atrium="company"' in head and 'data-figure="seal"' in head
    glyph = re.search(r'<use class="atrium__glyph-icon" href="[^"]+#icon-([\w-]+)"', head)
    assert glyph and glyph.group(1) == icons.resolve(icons.AUDIENCE["company"])
    with translation.override(lang):
        assert _eyebrow(head) == str(services.COMPANY_SPACE_LABEL) == translation.gettext("Espace Entreprises")
    calm = html.split('<div class="org-calm" data-spot>', 1)[1].split("</div>", 1)[0]
    assert 'class="org-calm__art"' in calm and 'class="btn btn--primary"' in calm
    side = html.split('<div class="db-side">', 1)[1]
    assert 'class="org-id org-id--lattice org-id--company"' in side and "Cantiere Adriatico S.r.l." in side
    assert side.count('class="org-id__fact"') >= 4
    assert html.count('id="db-account-title"') == 1 and 'class="db-account db-account--foot"' in side
    assert html.count("css/dist/portal/organisation.css") == 1
    assert 'class="db-space"' not in html, "the lone link is now the calm panel's way on"


def test_a_companys_eyebrow_is_its_space_on_every_atrium_page(client, company):
    client.force_login(company)
    dashboard = _eyebrow(_head(_html(client)))
    assert dashboard == "Espace Entreprises"
    response = client.get("/fr/espace-reserve/communications/", follow=True)
    assert _eyebrow(_head(response.content.decode("utf-8"))) == dashboard


def test_the_organisations_cta_is_the_identity_sheets_foot_when_registers_are_drawn(client, institution, make_message):
    """F1: the CTA floated alone between «Communications» and «Le projet» — it is now the sheet's foot action."""
    client.force_login(institution)
    calm = _html(client)
    assert 'class="org-id__act"' not in calm and 'class="org-act"' not in calm
    make_message(institution, subject="Coordination")
    html = _html(client)
    assert 'class="org-act"' not in html and '<div class="org-calm"' not in html
    side = html.split('<div class="db-side">', 1)[1]
    if 'class="org-id__act"' in side:  # the public form is open (G2): the approved CTA stands in the sheet's foot
        assert side.index('class="org-id__sheet"') < side.index('class="org-id__act"')


def test_an_empty_communications_register_is_the_calm_panel(client, alice):
    """F1: an icon, a heading and a sentence over ~500 px of nothing — now the calm panel, its words the register's."""
    client.force_login(alice)
    html = _html(client, path="/fr/espace-reserve/communications/")
    panel = html.split('<div class="org-calm reg-calm" role="status" data-spot>', 1)[1].split("\n  </div>", 1)[0]
    assert 'class="org-calm__art"' in panel
    assert "Aucune communication" in panel and "Les messages que l’équipe vous adresse apparaîtront ici." in panel
    assert 'class="empty-state"' not in html


def test_the_identity_sheets_facts_never_split_a_word():
    """F1 (major): «Responsabl|e», «28.10.202|6» at 1024–1280 — a lattice decided by the sheet's width, a value broken
    only between words, a date never."""
    css = SHEET.read_text(encoding="utf-8")
    assert "container: org-id / inline-size;" in css and "@container org-id (min-width: 21rem)" in css
    dd = re.search(r"\n\.org-id--lattice \.org-id__fact > dd \{([^}]*)\}", css).group(1)
    assert "overflow-wrap: break-word;" in dd
    time = re.search(r"\n\.org-id__fact time \{([^}]*)\}", css).group(1)
    # v524-plat (V5.20; V5.24 §11–§14; TYPOGRAPHY_V2 F-3; FINAL_DELIVERY_V2 §3.7, R8 «refs stay in the mono»): a date
    # is not a reference — the sans with tabular figures; the invariant (a date never splits) stays
    assert "white-space: nowrap;" in time and "var(--numeric-data)" in time and "var(--f-mono)" not in time


def test_the_deposits_gate_links_the_terms_only_when_they_are_published():
    """Lane C's carry-over M-2 / m-12: the Dépôt's gate linked legal:terms unconditionally — a 404 while closed."""
    for name in ("documents/partials/depot.html", "documents/terms_required.html"):
        source = (ROOT / "templates" / name).read_text(encoding="utf-8")
        assert "legal:terms" not in source, name
        assert '{% legal_links "terms" as terms_links %}' in source, name
