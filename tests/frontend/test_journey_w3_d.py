"""
The journey «La soglia» — design V5, family W3-D (docs/design-v5/V5_4_EXECUTION_PLAN.md §3.5 item 6, §1.18 D16;
docs/design-v5/QA/v54/w3-d/NOTES.md).

* the SELECTION mapping (OJ2): a file in SELECTION («Phase gérée par un acteur autorisé») stands ON threshold A — no
  step is current, the steps before the threshold are behind it, the one after it ahead; every other active status
  keeps its step; the case file dates the threshold, never a step the file left;
* a status with no place on the line (SUSPENDED, CLOSED): no current item and «Vous êtes ici» nowhere — the header's
  chip says the state; the case file reads the trail: the steps it reached behind the file, dated, the stop marked;
* ONE rail drawing — its vocabulary (apps/portal/static/portal/v5/_journey-nodes.css: one line, three nodes) composed
  by the journey and the timeline (v5/_journey-rail.css) and by the Stepper (v5/_journey-stepper.css) — for the
  console's three journey components — the
  dashboard's «Mon parcours», the «Mon parcours» page's head and the case file's journey
  (components/journey_rail.html), the case file's timeline (components/case_timeline.html, newest first), «Ma
  situation»'s Stepper (components/wizard_stepper.html) — in a page-only sheet (portal/journey.css: the owner's V5.8,
  never the shared bundles), and ONE passage drawing (static/css/v5/_journey-passage.css: «la linea»,
  components/stepper.html) for the public pages — the home and, since the w3-d merge, the door pages, the advice
  pages and the questionnaire (W3-F1's «la linea» homed there: the review's M4); never a third;
* «Ma situation»'s guided form (W3-F1's v5/_wizard.css) in a page-only sheet that page alone links (the w3-d merge);
* the markers (D16): one a column — the step's phase glyph on the rail (through the registry), the numeral on the
  passage; no check anywhere (O14); the holder only when the presenter knows it (A′);
* the phone's journey: a card (what is true now) and a native disclosure; the list exposed once;
* still at load: no animation, no transition, no keyframes, no will-change in either partial; V4's drawing (the
  JourneyRail, the Timeline, the stepper of components.css §16, the sequence's shore crossing) gone with its consumers;
* every word on the four components the catalogue's.

What a browser must show — the level line on one level at 1440, mirrored in Arabic, the card and its disclosure at
390, nothing moving at load, the Stepper's line — is in tests/frontend/test_journey_browser_w3_d.py.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
from django.template.loader import render_to_string
from django.utils import translation

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "apps"))

from accounts import roles  # noqa: E402
from accounts.models import AccountType  # noqa: E402
from core import clock, icons  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
COMPONENTS = ROOT / "templates" / "components"
RAIL = ROOT / "apps" / "portal" / "static" / "portal" / "v5" / "_journey-rail.css"
NODES = ROOT / "apps" / "portal" / "static" / "portal" / "v5" / "_journey-nodes.css"
STEPPER = ROOT / "apps" / "portal" / "static" / "portal" / "v5" / "_journey-stepper.css"
PASSAGE = ROOT / "static" / "css" / "v5" / "_journey-passage.css"
CONSOLE = ROOT / "apps" / "portal" / "static" / "portal" / "console.css"
JOURNEY_SHEET = ROOT / "apps" / "portal" / "static" / "portal" / "journey.css"
SITUATION_SHEET = ROOT / "apps" / "portal" / "static" / "portal" / "situation.css"
HOME_SHEET = ROOT / "apps" / "pages" / "static" / "pages" / "css" / "pages.css"
CATALOGUE = ROOT / "locale" / "ar" / "LC_MESSAGES" / "django.po"
DASHBOARD = "/{lang}/espace-reserve/"


def _css(path: Path) -> str:
    return re.sub(r"/\*.*?\*/", "", path.read_text(encoding="utf-8"), flags=re.S)


def _journey(status: str) -> list[dict]:
    from portal.services import journey_for

    return journey_for(SimpleNamespace(status=status))


# ---- the SELECTION mapping, and every other status ------------------------------------------------------------------
def test_a_file_in_selection_stands_on_threshold_a_and_on_no_step():
    with translation.override("fr"):
        steps = _journey("selection")
        assert [step["is_current"] for step in steps] == [False] * 7, "no step is current: the threshold is"
        assert [step["state"] for step in steps] == ["done"] * 3 + ["upcoming"] * 4
        gate = steps[3]["threshold"]
        assert steps[3]["status"] == "admin_process" and gate["key"] == "a"
        assert gate["state"] == "current" and gate["is_current"] is True
        assert str(gate["label"]) == "Phase gérée par un acteur autorisé", "the file's state, in its own words"
        assert str(gate["caption"]) == "Autorités compétentes : décisions administratives"
        assert steps[5]["threshold"]["key"] == "b" and steps[5]["threshold"]["state"] == "upcoming"
        assert [i for i, step in enumerate(steps) if step["threshold"]] == [3, 5], "two thresholds, never a step"


@pytest.mark.parametrize(
    ("status", "current", "gate_a", "gate_b"),
    [
        ("draft", 0, "upcoming", "upcoming"),
        ("oriented", 1, "upcoming", "upcoming"),
        ("review_required", 1, "upcoming", "upcoming"),
        ("training", 2, "upcoming", "upcoming"),
        ("admin_process", 3, "done", "upcoming"),
        ("pre_departure", 4, "done", "upcoming"),
        ("entered", 5, "done", "done"),
        ("post_entry", 6, "done", "done"),
    ],
)
def test_every_step_status_keeps_its_step_and_the_thresholds_follow(status, current, gate_a, gate_b):
    steps = _journey(status)
    assert [index for index, step in enumerate(steps) if step["is_current"]] == [current]
    assert [step["state"] for step in steps] == ["done"] * current + ["current"] + ["upcoming"] * (6 - current)
    assert (steps[3]["threshold"]["state"], steps[5]["threshold"]["state"]) == (gate_a, gate_b)
    assert not steps[3]["threshold"]["label"] and not steps[5]["threshold"]["label"]
    assert steps[3]["frontier"] is True, "V4's frontier flag stays: threshold A"


@pytest.mark.parametrize("status", ["suspended", "closed"])
def test_a_suspended_or_closed_file_has_no_place_on_the_line_and_nothing_says_here(status):
    """A status with no place on the line (the review's M3): no current item, every item ahead — the status alone knows
    no more —, and the rail says «Vous êtes ici» nowhere, in the card, the level line or the spine: the header's chip
    says the state. V4's mapping put the ring and «Vous êtes ici» on step 1."""
    with translation.override("fr"):
        steps = _journey(status)
        assert [step["is_current"] for step in steps] == [False] * 7
        assert [step["state"] for step in steps] == ["upcoming"] * 7
        assert [step["stop"] for step in steps] == [False] * 7
        assert not steps[3]["threshold"]["is_current"] and not steps[5]["threshold"]["is_current"]
        for descriptive in (False, True):
            html = _rail(steps, descriptive=descriptive)
            assert "Vous êtes ici" not in html and 'aria-current="step"' not in html, descriptive
            assert "journey__step--current" not in html and "journey__threshold--current" not in html


#: transitions (from, to), in their order: the file went as far as the administrative procedure
_TO_ADMIN = (("draft", "oriented"), ("oriented", "training"), ("training", "selection"), ("selection", "admin_process"))


@pytest.mark.parametrize("status", ["suspended", "closed"])
def test_on_the_case_file_a_file_off_the_line_is_past_what_its_trail_reached_dated_and_not_here(case, status):
    """The case file reads the trail: every step up to where the file stopped is behind it and dated, the item there
    marks the stop (no travelled line onward), nothing is current and nothing says «Vous êtes ici»."""
    from audit.services import record
    from cases.presenters import journey_with_dates

    for source, target in (*_TO_ADMIN, ("admin_process", status)):
        record(action="case.transition", target=case, metadata={"from": source, "to": target})
    with translation.override("fr"):
        steps = journey_with_dates(_status(case, status))
        html = _rail(steps, descriptive=True)
    assert [step["state"] for step in steps] == ["done"] * 4 + ["upcoming"] * 3
    assert [bool(step["reached_at"]) for step in steps] == [True] * 4 + [False] * 3, "dated where the trail knows"
    assert [step["stop"] for step in steps] == [False] * 3 + [True] + [False] * 3
    assert steps[3]["threshold"]["state"] == "done" and not steps[3]["threshold"]["stop"]
    assert steps[5]["threshold"]["state"] == "upcoming"
    assert not any(step["is_current"] or step["threshold"] and step["threshold"]["is_current"] for step in steps)
    assert "Vous êtes ici" not in html and 'aria-current="step"' not in html
    assert html.count('class="journey__when"><time datetime=') == 4
    assert "journey__step journey__step--4 journey__step--done journey__step--stop" in html


def test_a_file_suspended_on_threshold_a_stops_there_and_a_resumed_then_closed_file_where_it_last_stood(case):
    from audit.services import record
    from cases.presenters import journey_with_dates

    for source, target in (*_TO_ADMIN[:3], ("selection", "suspended")):
        record(action="case.transition", target=case, metadata={"from": source, "to": target})
    steps = journey_with_dates(_status(case, "suspended"))
    assert [step["state"] for step in steps] == ["done"] * 3 + ["upcoming"] * 4
    assert steps[3]["threshold"]["state"] == "done" and steps[3]["threshold"]["stop"] is True
    assert not any(step["stop"] for step in steps), "the stop is the threshold's, not a step's"
    # resumed into the training, then closed: the file last stood on step 3
    for source, target in (("suspended", "training"), ("training", "closed")):
        record(action="case.transition", target=case, metadata={"from": source, "to": target})
    steps = journey_with_dates(_status(case, "closed"))
    assert [step["state"] for step in steps] == ["done"] * 3 + ["upcoming"] * 4
    assert [step["stop"] for step in steps] == [False, False, True] + [False] * 4
    assert steps[3]["threshold"]["state"] == "upcoming"


def test_every_step_has_a_glyph_in_the_registry_and_no_numeral_or_actor_is_invented():
    steps = _journey("training")
    assert [icons.concept("journey", step["status"]) for step in steps] == [
        "compass",
        "signpost",
        "book-open",
        "scroll-text",
        "clipboard-list",
        "building-2",
        "sprout",
    ]
    assert icons.concept("journey", "threshold_a") == "stamp" and icons.concept("journey", "threshold_b") == "ile-arch"
    assert all(step["actor"] == "" for step in steps), "A′: no holder until the actors' mapping is signed (OJ1, D9)"


@pytest.fixture
def person(user_factory):
    return user_factory(
        "journey.person@example.test",
        role=roles.PERSON,
        full_name="Journey PERSON",
        account_type=AccountType.PERSON,
        terms_accepted_at=clock.now(),
    )


@pytest.fixture
def case(person):
    from cases.models import CasePurpose
    from cases.services import open_case

    return open_case(person, purpose=CasePurpose.WORK, pathway_key="salaried_work")


def _status(case, status):
    from cases.models import CaseFile

    CaseFile.objects.filter(pk=case.pk).update(status=status, status_since=clock.now())
    case.refresh_from_db()
    return case


def test_the_case_file_dates_the_threshold_and_never_a_step_the_file_left(case):
    from audit.services import record
    from cases.presenters import journey_with_dates

    # the trail once reached the administrative procedure, then the file came back to the authorised actor's phase
    for source, target in (("draft", "oriented"), ("oriented", "training"), ("training", "selection")):
        record(action="case.transition", target=case, metadata={"from": source, "to": target})
    record(action="case.transition", target=case, metadata={"from": "selection", "to": "admin_process"})
    record(action="case.transition", target=case, metadata={"from": "admin_process", "to": "selection"})
    steps = journey_with_dates(_status(case, "selection"))
    assert [bool(step["reached_at"]) for step in steps] == [True, True, True, False, False, False, False]
    assert steps[3]["threshold"]["reached_at"], "the threshold the file stands on carries its date"


# ---- the rail: one list, one current, the markers -----------------------------------------------------------------
def _rail(steps, **extra) -> str:
    return render_to_string("components/journey_rail.html", {"steps": steps, "label": "Où j’en suis", **extra})


def _items(html: str) -> list[str]:
    return re.findall(r"<li class=\"(journey__[^\"]+)\"([^>]*)>", html)


def test_on_threshold_a_the_list_exposes_eight_items_and_its_current_one_is_the_threshold():
    with translation.override("fr"):
        html = _rail(_journey("selection"))
    items = _items(html)
    exposed = [(cls, attrs) for cls, attrs in items if 'aria-hidden="true"' not in attrs]
    assert len(exposed) == 8, "seven steps and the threshold the file stands on"
    current = [cls for cls, attrs in items if 'aria-current="step"' in attrs]
    assert current == ["journey__threshold journey__threshold--a journey__threshold--current"]
    assert html.count('aria-current="step"') == 1
    assert '<ol class="journey journey--on-a"' in html
    hidden = [cls for cls, attrs in items if 'aria-hidden="true"' in attrs]
    assert hidden == [
        "journey__shore journey__shore--start",
        "journey__threshold journey__threshold--b journey__threshold--upcoming",
        "journey__shore journey__shore--end",
    ]
    # the threshold that is not the file's place is said in the step it opens; the one it stands on, by itself
    assert '<span class="visually-hidden">Territoire italien : accueil et inclusion. </span>' in html
    assert '<span class="visually-hidden">Autorités compétentes' not in html
    card = html.split('<div class="journey-now">', 1)[1].split("</div>", 1)[0]
    assert "Phase gérée par un acteur autorisé" in card and "journey-now__rank" not in card, "no rank on a threshold"
    # the threshold's caption heads the card: where that phase sits, without opening the list (the review's m5)
    assert '<p class="journey-now__where">Autorités compétentes : décisions administratives</p>' in card
    assert card.index("journey-now__where") < card.index("journey-now__label") < card.index("Vous êtes ici")
    assert card.count("Vous êtes ici") == 1


def test_on_a_step_the_card_says_the_step_its_rank_and_here_and_the_list_seven_items():
    with translation.override("fr"):
        html = _rail(_journey("oriented"))
    items = _items(html)
    assert len([1 for _cls, attrs in items if 'aria-hidden="true"' not in attrs]) == 7
    assert [cls for cls, attrs in items if 'aria-current="step"' in attrs] == [
        "journey__step journey__step--2 journey__step--current"
    ]
    card = html.split('<div class="journey-now">', 1)[1].split("</div>", 1)[0]
    assert "Pré-évaluation et parcours possibles" in card and "Étape 2 sur 7" in card and "Vous êtes ici" in card
    assert "journey-now__where" not in card, "a step's card says its rank, not a caption"
    # the phone's list behind the native disclosure, closed — its summary the list's own name
    assert '<details class="journey-fold">' in html and '<details class="journey-fold" open' not in html
    assert '<summary class="journey-fold__summary">Où j’en suis</summary>' in html


def test_the_rail_draws_one_glyph_a_step_from_the_registry_no_numeral_no_check():
    with translation.override("fr"):
        html = _rail(_journey("training"))
    labels = re.findall(r'<p class="journey__label">(.*?)</p>', html, flags=re.S)
    assert len(labels) == 7
    glyphs = [re.findall(r'#icon-([a-z0-9-]+)"', label) for label in labels]
    assert glyphs == [[icons.concept("journey", step["status"])] for step in _journey("training")]
    assert not re.search(r"#icon-(?:check|circle-check|badge-check|square-check)\b", html), "no check (O14)"
    assert not re.search(r"journey__node[^>]*>\s*\d", html), "no numeral in a node: the numeral is the passage's"
    assert "journey__actor" not in html, "A′: no holder row until the presenter knows one"


def test_the_case_file_journey_is_the_spine_with_dates_and_no_card():
    with translation.override("fr"):
        steps = _journey("selection")
        for step in steps:
            step["reached_at"] = clock.now() if step["state"] == "done" else None
        steps[3]["threshold"]["reached_at"] = clock.now()
        html = render_to_string("components/journey_rail.html", {"steps": steps, "descriptive": True, "label": "x"})
    assert 'class="journey-rail journey-rail--descriptive"' in html
    assert "journey-now" not in html and "<details" not in html, "the case file has no card and no disclosure"
    assert html.count('class="journey__when"><time datetime=') == 4, "three steps behind and the threshold, dated"
    assert html.count("Vous êtes ici") == 1


def test_the_timeline_heads_with_its_latest_event_lit_says_an_actor_once_and_draws_no_check():
    """Newest first, the first row lit — the inspector scrolls inside itself, and its first row is the one in view —;
    an assignment's actor is not said again when it is the role its detail already says (the review's m1)."""
    when = clock.now()
    row = {"when": when, "detail": "", "chip_label": "", "chip_register": "", "actor": "Vous"}
    rows = [
        {**row, "title": "Intervenant assigné", "detail": "Acteur autorisé", "actor": "Acteur autorisé"},
        {**row, "title": "Évènement 1"},
        {**row, "title": "Évènement 0"},
    ]
    html = render_to_string("components/case_timeline.html", {"rows": rows})
    assert html.count('class="tl__row"') == 2 and html.count('class="tl__row tl__row--latest"') == 1
    assert html.index("tl__row--latest") < html.index("Intervenant assigné") < html.index("Évènement 0")
    assert html.count("Acteur autorisé") == 1 and html.count('<span class="tl__actor">Vous</span>') == 2
    assert "#icon-" not in html.split("tl__what")[0]


def test_the_timeline_presenter_gives_the_events_newest_first(case):
    from audit.services import record
    from cases.presenters import timeline

    for source, target in (("draft", "oriented"), ("oriented", "training")):
        record(action="case.transition", target=case, metadata={"from": source, "to": target})
    from cases.models import CaseStatus

    with translation.override("fr"):
        rows = timeline(case)
        states = [str(CaseStatus.TRAINING.label), str(CaseStatus.ORIENTED.label)]
    assert [row["title"] for row in rows] == ["Nouvel état", "Nouvel état", "Dossier ouvert"]
    assert [row["chip_label"] for row in rows[:2]] == states, "the latest transition first"


def test_the_stepper_keeps_its_contract_with_situation_js():
    fields = [SimpleNamespace(name=f"q{n}", label=f"Question {n}") for n in range(1, 4)]
    html = render_to_string("components/wizard_stepper.html", {"fields": fields, "answered": {"q2"}})
    assert html.count("data-wizard-mark=") == 3 and html.count("data-wizard-go=") == 3
    assert 'class="wstep__item wstep__item--current" data-wizard-mark="1" aria-current="step"' in html
    assert 'class="wstep__item wstep__item--done" data-wizard-mark="2"' in html
    script = (ROOT / "static" / "js" / "src" / "situation.js").read_text(encoding="utf-8")
    assert "wstep__item--current" in script and "wstep__item--done" in script


# ---- the pages that draw it ----------------------------------------------------------------------------------------
def test_the_dashboard_draws_the_rail_with_the_file_on_threshold_a(client, case, person):
    _status(case, "selection")
    client.force_login(person)
    html = client.get(DASHBOARD.format(lang="fr")).content.decode("utf-8")
    journey = html.split('<section class="db-journey"', 1)[1].split("</section>", 1)[0]
    assert '<ol class="journey journey--on-a" aria-label="Où j’en suis">' in journey
    assert journey.count('aria-current="step"') == 1 and "journey__threshold--current" in journey
    work = html.split('class="console__workspace"', 1)[1]
    assert work.index("<h1") < work.index("db-now") < work.index('class="db-journey"'), "h1 → NowPanel → journey"


def test_the_case_file_draws_the_descriptive_rail_and_the_timeline(client, case, person):
    _status(case, "training")
    client.force_login(person)
    html = client.get(f"/fr/espace-reserve/dossiers/{case.reference}/").content.decode("utf-8")
    assert '<ol class="journey journey--descriptive" aria-label="Où en est ce dossier">' in html
    assert html.count('aria-current="step"') == 1
    assert '<ol class="tl" role="list">' in html
    assert _sheets(html)[-1].endswith("css/dist/portal/journey.css"), "the journey's sheet, after the shell's two"


@pytest.mark.parametrize("status", ["suspended", "closed"])
def test_the_case_file_of_a_file_off_the_line_says_here_nowhere(client, case, person, status):
    from audit.services import record

    for source, target in (*_TO_ADMIN[:2], ("training", status)):
        record(action="case.transition", target=case, metadata={"from": source, "to": target})
    _status(case, status)
    client.force_login(person)
    html = client.get(f"/fr/espace-reserve/dossiers/{case.reference}/").content.decode("utf-8")
    journey = html.split('<ol class="journey journey--descriptive"', 1)[1].split("</ol>", 1)[0]
    assert "Vous êtes ici" not in journey and 'aria-current="step"' not in journey
    assert (
        journey.count("journey__step--done") == 3
        and "journey__step--3 journey__step--done journey__step--stop" in journey
    )


PATHWAYS = "/{lang}/espace-reserve/mon-parcours/"


def _sheets(html: str) -> list[str]:
    head = html.split("</head>", 1)[0]
    return re.findall(r'<link rel="stylesheet" href="([^"]+)"', head)


def test_mon_parcours_draws_the_dashboards_journey_at_its_head_when_the_person_has_a_file(client, case, person):
    """«Mon parcours» wears the journey's glyph in the rail: the page answers where the person stands (the review's M2)
    — the dashboard's component and words, the pre-assessments under it."""
    _status(case, "selection")
    client.force_login(person)
    html = client.get(PATHWAYS.format(lang="fr")).content.decode("utf-8")
    work = html.split('class="console__workspace"', 1)[1]
    assert '<ol class="journey journey--on-a" aria-label="Où j’en suis">' in work
    assert (
        work.count('aria-current="step"') == 1
        and '<summary class="journey-fold__summary">Où j’en suis</summary>' in work
    )
    assert work.index("<h1") < work.index('class="journey-page"') < work.index('data-result-kind="informational"')
    assert _sheets(html)[-1].endswith("css/dist/portal/journey.css")


def test_without_a_file_no_page_draws_a_journey_or_loads_its_sheet(client, person):
    client.force_login(person)
    for path in (PATHWAYS, DASHBOARD):
        html = client.get(path.format(lang="fr")).content.decode("utf-8")
        assert '<ol class="journey' not in html and "portal/journey.css" not in html, path
    html = client.get("/fr/espace-reserve/communications/").content.decode("utf-8")
    assert "portal/journey.css" not in html, "a console page without a journey keeps the shared payload alone"


def test_the_home_draws_the_orientations_neutral_steps_on_the_public_passage():
    source = (ROOT / "templates" / "pages" / "home" / "_orientation.html").read_text(encoding="utf-8")
    assert '{% include "components/stepper.html" with steps=d.steps lang=d.steps_lang across=True %}' in source
    assert "sequence__" not in source


def test_the_passage_shows_a_flows_place_and_an_explanation_shows_none():
    steps = ["Un", "Deux", "Trois"]
    with translation.override("fr"):
        flow = render_to_string("components/stepper.html", {"steps": steps, "current": 2})
        told = render_to_string("components/stepper.html", {"steps": steps, "across": True})
    assert flow.count('aria-current="step"') == 1 and "linea__step--done" in flow and "Étape 2 sur 3" in flow
    assert 'aria-label="Progression"' in flow
    assert "aria-current" not in told and "linea__rank" not in told and 'class="linea linea--across"' in told
    assert told.count('<span class="linea__num" aria-hidden="true"></span>') == 3


# ---- the two drawings ------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("sheet", [NODES, RAIL, STEPPER, PASSAGE], ids=["nodes", "rail", "stepper", "passage"])
def test_each_drawing_is_still_at_load_on_tokens_and_logical_properties(sheet):
    css = _css(sheet)
    assert "@keyframes" not in css and "animation" not in css and "will-change" not in css, "still at load"
    assert set(re.findall(r"(?<![\w-])transition:\s*([^;]+);", css)) <= {"none"}, "nothing moves"
    assert not re.search(r"#[0-9a-fA-F]{3,8}\b|\brgba?\(|\bhsla?\(|gradient\(", css), "tokens only"
    physical = re.findall(
        r"(?<![\w-])(?:margin|padding|border)-(?:left|right|top|bottom)\b|(?<![\w-])(?:left|right|top|bottom)\s*:", css
    )
    assert not physical, f"logical properties only: {physical}"
    shadows = set(re.findall(r"box-shadow:\s*([^;]+);", css))
    assert shadows <= {"none"}, f"the current node's wash is a disc, not a shadow: {shadows}"
    assert set(re.findall(r"border-radius:\s*([^;]+);", css)) <= {"var(--radius-full)", "var(--radius-sm)", "0"}


#: The pages that draw the journey or the timeline, each linking the journey's page-only sheet after the shell's two
#: («Ma situation» draws its Stepper from its own sheet).
JOURNEY_PAGES = ("portal/dashboard.html", "portal/pathways.html", "cases/detail.html")


def test_the_rail_is_a_page_only_sheet_the_journeys_pages_link_and_the_passage_the_homes_import():
    """The owner's V5.8: the shared bundles' ceilings are hard (main + console + portal on every console page,
    DL54-87). The rail is the journey's own CSS: a page-only sheet, portal/journey.css — the vocabulary, then the
    journey and the timeline — linked after console.css (the place the rail held as its last import) by the three pages
    that draw them, and never in console.css; «Ma situation» draws its Stepper from its own sheet (each page loads only
    what it draws: the orchestrator's definitive ruling)."""
    assert [line.strip() for line in _css(JOURNEY_SHEET).splitlines() if line.strip()] == [
        '@import url("v5/_journey-nodes.css");',
        '@import url("v5/_journey-rail.css");',
    ], "the journey's sheet is its import list and nothing else"
    assert "_journey" not in _css(CONSOLE), "never in the console's shared entry"
    dist = ROOT / "static" / "css" / "dist"
    console = (dist / "portal" / "console.css").read_text(encoding="utf-8")
    assert not re.search(r"\.(?:journey|tl|wstep)(?:__|--|[\s,.{:>)])", console), "no journey rule in the shared bundle"
    journey = (dist / "portal" / "journey.css").read_text(encoding="utf-8")
    assert (
        ".journey-fold" in journey
        and ".tl__row" in journey
        and ".journey-page" in journey
        and ".wstep__link" not in journey
    ), "the journey and the timeline; the Stepper is «Ma situation»'s"
    for name in JOURNEY_PAGES:
        source = (ROOT / "templates" / name).read_text(encoding="utf-8")
        block = re.search(r"{%\s*block extra_head\s*%}(.*?){%\s*endblock", source, flags=re.S)
        assert block, name
        assert block.group(1).index("block.super") < block.group(1).index("css/dist/portal/journey.css"), name
    assert '@import url("../../css/v5/_journey-passage.css");' in _css(HOME_SHEET)
    for partial in (NODES, RAIL, STEPPER, PASSAGE):
        assert partial.name.startswith("_"), "partials: never an output of their own"
    for partial in (NODES, RAIL, STEPPER):
        assert not (dist / "portal" / "v5" / partial.name).exists(), partial.name
    home = (dist / "pages" / "css" / "pages.css").read_text(encoding="utf-8")
    assert ".linea__num" in home


def test_the_stepper_and_the_rails_lines_never_take_the_pointer():
    """The line is a drawing: on the Stepper it crosses its own link, and a tap on it must land on the link (the
    accessibility check's finding 3)."""
    css = _css(NODES)
    base = re.search(r"\.journey > li::before,\s*\.tl__row::before,\s*\.wstep__item::before\s*\{([^}]*)\}", css)
    assert base and "pointer-events: none" in base.group(1)


def test_ma_situation_loads_one_page_only_sheet_its_form_and_its_stepper(client, person):
    """The w3-d merge (the orchestrator's definitive CSS ruling, V5.8): «Ma situation»'s guided form (W3-F1's
    v5/_wizard.css) is that page's own CSS — it left the shared console bundle — and the page loads only what it draws:
    one page-only sheet, portal/situation.css, with the form, then its Stepper on the rail's vocabulary
    (v5/_journey-nodes.css, v5/_journey-stepper.css); never the level line, the card or the timeline. Linked, of the
    product's templates, by templates/portal/situation.html alone, after the shell's two sheets: the place in the
    cascade the form held as console.css's last import (the DEBUG-only design showcase, templates/dev/, links it for
    its specimens, as it links the other families' page sheets)."""
    assert [line.strip() for line in _css(SITUATION_SHEET).splitlines() if line.strip()] == [
        '@import url("v5/_wizard.css");',
        '@import url("v5/_journey-nodes.css");',
        '@import url("v5/_journey-stepper.css");',
    ], "«Ma situation»'s sheet is its import list and nothing else"
    assert "_wizard" not in _css(CONSOLE), "never in the console's shared entry"
    dist = ROOT / "static" / "css" / "dist" / "portal"
    console = (dist / "console.css").read_text(encoding="utf-8")
    assert not re.search(r"\.(?:wiz|opts?)(?:__|--|[\s,.{:>)])", console), "no rule of the form in the shared bundle"
    situation = (dist / "situation.css").read_text(encoding="utf-8")
    assert ".wiz__q" in situation and ".wstep__link" in situation and ".wstep__node" in situation
    assert not re.search(r"\.journey-fold|\.journey__gate|\.journey-page|\.tl__when", situation), (
        "only what the page draws: never the card, the thresholds, the page's head or the timeline"
    )
    linkers = sorted(
        path.relative_to(ROOT / "templates").as_posix()
        for path in (ROOT / "templates").rglob("*.html")
        if "css/dist/portal/situation.css" in path.read_text(encoding="utf-8")
    )
    assert [name for name in linkers if not name.startswith("dev/")] == ["portal/situation.html"], linkers
    client.force_login(person)
    sheets = _sheets(client.get("/fr/espace-reserve/ma-situation/").content.decode("utf-8"))
    assert sheets[-1].endswith("css/dist/portal/situation.css") and not any("journey.css" in s for s in sheets), sheets
    other = _sheets(client.get("/fr/espace-reserve/communications/").content.decode("utf-8"))
    assert not any("situation.css" in s or "journey.css" in s for s in other), other


def test_one_rail_drawing_and_one_passage_drawing_never_a_third():
    """The journey's classes are drawn by the two partials and by no other sheet of the product — elsewhere only a
    page's modifiers of the one passage, never the drawing itself (the w3-d merge's consolidation with W3-F1: the
    senior review's M4)."""
    rail = re.compile(r"\.(?:journey|tl|wstep)(?:__|--|[\s,.{:>)])")
    passage = re.compile(r"\.(?:stepper|linea|timeline__marker)(?:__|--|[\s,.{:>)])")
    drawers = set()
    for sheet in [*(ROOT / "static" / "css").rglob("*.css"), *(ROOT / "apps").glob("*/static/**/*.css")]:
        rel = sheet.relative_to(ROOT).as_posix()
        if "/dist/" in rel or "/dev/" in rel:
            continue
        css = _css(sheet)
        if rail.search(css):
            drawers.add(("rail", rel))
        if passage.search(css):
            drawers.add(("passage", rel))
    partials = {
        # the console's one rail drawing: its vocabulary and its two components
        ("rail", "apps/portal/static/portal/v5/_journey-nodes.css"),
        ("rail", "apps/portal/static/portal/v5/_journey-rail.css"),
        ("rail", "apps/portal/static/portal/v5/_journey-stepper.css"),
        ("passage", "static/css/v5/_journey-passage.css"),
    }
    modifiers = {
        # a page's modifiers of the one passage: «Formation»'s two phases, the diplomas' steps, a fragment's first
        # letter (the pathways); the pilot's eight stations (the spaces); a moment's fragment (the questionnaire)
        ("passage", "apps/pathways/static/pathways/_pathways.css"),
        ("passage", "apps/ecosystem/static/ecosystem/_spaces.css"),
        ("passage", "apps/orientation/static/orientation/wizard.css"),
        # not a drawing: the foundation's one rule that sets the legacy dates in the sans (ILE Mono's one seat)
        ("rail", "static/css/v5/base.css"),
    }
    assert drawers <= partials | modifiers, sorted(drawers - partials - modifiers)
    # the drawing itself — the list, the station, its numeral and ring, the line, the Stepper's nodes and line — is
    # declared by the two partials alone: a page qualifies it, never redraws it
    drawing = re.compile(
        r"(?:^\s*|[},]\s*)(?:\.linea|\.linea__step|\.linea__num(?:::before|::after)?|\.linea__step:not\(:last-child\)::before"
        r"|\.linea__label|\.linea__text|\.wstep|\.wstep__item|\.wstep__link|\.wstep__node|\.wstep__item::before)\s*[,{]",
        flags=re.M,
    )
    for _kind, rel in drawers - partials:
        assert not drawing.search(_css(ROOT / rel)), f"{rel} redraws the journey"


def test_v4s_journey_drawing_left_with_its_consumers():
    workspace = _css(ROOT / "static" / "css" / "v4" / "workspace.css")
    assert ".journey" not in workspace and ".tl" not in workspace, (
        "the JourneyRail and the Timeline left v4/workspace.css"
    )
    components = _css(ROOT / "static" / "css" / "components.css")
    assert ".stepper" not in components and "progress.progress" not in components, "§16 left with stepper.html's redraw"
    # the w3-d merge's consolidation with W3-F1 (the review's M4): §17 and components/timeline.html left with their
    # last caller (the showcase's demo); «la linea» has one home and one markup; the Stepper's rules left the guided
    # form's sheet
    assert ".timeline" not in components and not (COMPONENTS / "timeline.html").exists(), (
        "§17 left with its last caller"
    )
    assert not re.search(r"\.linea\b", _css(ROOT / "static" / "css" / "v5" / "_interior.css")), (
        "«la linea» has one home"
    )
    wizard = _css(ROOT / "apps" / "portal" / "static" / "portal" / "v5" / "_wizard.css")
    assert ".wstep" not in wizard and ".wiz__count" in wizard, (
        "the Stepper is the rail's (§7); its count stays the form's"
    )
    linea = (ROOT / "templates" / "pages" / "partials" / "_linea.html").read_text(encoding="utf-8")
    assert '{% include "components/stepper.html" with current=None %}' in linea and "<ol" not in linea, "one component"
    for sheet in (
        "pathways/static/pathways/pathways.css",
        "ecosystem/static/ecosystem/ecosystem.css",
        "orientation/static/orientation/wizard.css",
    ):
        imports = re.findall(r'@import url\("([^"]+)"\);', _css(ROOT / "apps" / sheet))
        assert imports[1:3] == ["../css/v5/_interior.css", "../css/v5/_journey-passage.css"], (sheet, imports)
    for sheet in ("forum/static/forum/forum.css", "pages/static/pages/css/interior.css"):
        assert "_journey-passage" not in _css(ROOT / "apps" / sheet), f"{sheet} draws no «la linea»"
    register = _css(ROOT / "static" / "css" / "register.css")
    assert ".sequence__crossing" not in register and ".sequence__step--italy" not in register
    assert ".sequence__step" in register, "the sequence stays for its console consumers until W3-E redraws them"
    bundle = (ROOT / "static" / "css" / "dist" / "main.css").read_text(encoding="utf-8")
    for keyframes in ("rail-draw", "rail-draw-y", "tl-light"):
        assert f"@keyframes {keyframes}" not in bundle, keyframes
    dashboard = _css(ROOT / "apps" / "portal" / "static" / "portal" / "v5" / "_dashboard.css")
    assert ".journey" not in dashboard, "W3-B's scoped rule left: the rail is still at load by itself"


# ---- no new copy -----------------------------------------------------------------------------------------------------
def _msgids(source: str) -> set[str]:
    source = re.sub(r"\{% comment %\}.*?\{% endcomment %\}", "", source, flags=re.S)
    found = set(re.findall(r'\{%\s*translate\s+"([^"]+)"', source))
    found |= set(re.findall(r"\{%\s*translate\s+'([^']+)'", source))
    for block in re.findall(r"\{%\s*blocktranslate[^%]*%\}(.*?)\{%\s*endblocktranslate\s*%\}", source, flags=re.S):
        found.add(re.sub(r"\{\{\s*(\w+)\s*\}\}", r"%(\1)s", block.split("{% plural %}")[0]))
    return found


def _catalogue_msgids() -> set[str]:
    known, current, inside = set(), [], False
    for line in CATALOGUE.read_text(encoding="utf-8").splitlines():
        if line.startswith("msgid "):
            current, inside = [line[6:]], True
        elif inside and line.startswith('"'):
            current.append(line)
        else:
            if inside:
                known.add("".join(part.strip()[1:-1] for part in current).replace('\\"', '"'))
            inside = False
    return known


def test_every_word_of_the_journey_is_the_catalogues_no_new_copy():
    known = _catalogue_msgids()
    used: set[str] = set()
    for name in ("journey_rail", "case_timeline", "stepper", "wizard_stepper"):
        used |= _msgids((COMPONENTS / f"{name}.html").read_text(encoding="utf-8"))
    used |= {"Autorités compétentes : décisions administratives", "Territoire italien : accueil et inclusion"}
    missing = sorted(msgid for msgid in used if msgid not in known)
    assert not missing, f"new copy (it goes to the owner's copy packet first): {missing}"
