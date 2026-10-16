"""
The public interior of design V5.4 — W3-F1, step 2: orientation, the advice pages and the wizard (plan §3.5 item 1;
§1.18 D26; §1.3 three corners a screen; §1.7 the six-icon ceiling; §2.2 the serialized import lists; §2.3 the
deletion map).

What the step promises, read in the rendered HTML and in the sheets:
* «Diplômes et titres», «Formation», the questionnaire's first page and the resume page draw the interior's grammar
  — one entrance, one h1, no side column, no V4 page header, CTA band or timeline — with one primary at most and
  at most six icons in the body (the section device's identity mark apart);
* the five moments of the diplomas stand on «la linea», each open and broken (still being verified), each Italian
  term under the station it belongs to; the two moments of «Formation» are two stations, their words in the
  numeral's seat, and no card;
* the fraud warning is a warning notice of the core components — its mark, its words, its broken rule — on every
  page that draws it, and on its own page the prescribed text stays byte-identical under a visible title;
* the questionnaire's first page holds its one inset and its one action in the entrance, the inset first (the
  fix pass, M4);
* a step of the questionnaire: a compact title (its sentence is said once, on the first page), «Question n sur N au
  maximum» in words and never a percentage or a <progress> (FM12), the question as the legend, plates around native
  controls, ONE primary first in the DOM; an error wired to its group and said in words beside its mark; a
  multiple choice says so before its choices;
* «Ma situation»'s guided form left main.css: v4/wizard.css is gone, v5/_wizard.css is imported by «Ma situation»'s
  page-only sheet (portal/situation.css — the w3-d merge took it out of the shared console entry), its corners the
  console's three and its foot never over the page.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from bs4 import BeautifulSoup
from django.conf import settings
from django.template.loader import render_to_string

pytestmark = pytest.mark.django_db

ROOT = Path(settings.BASE_DIR)
ICON = re.compile(r'<use href="[^"#]*#icon-([a-z0-9-]+)"')
STEP2 = [
    "/fr/diplomes-et-titres/",
    "/fr/formation/",
    "/fr/orientation/",
    "/fr/orientation/reprendre/",
    "/ar/diplomes-et-titres/",
    "/ar/formation/",
    "/ar/orientation/",
]
CALLOUT_PAGES = ["/fr/diplomes-et-titres/", "/fr/formation/", "/fr/parcours/", "/fr/parcours/salaried_work/"]
WIZARD_PARTIAL = ROOT / "apps" / "portal" / "static" / "portal" / "v5" / "_wizard.css"


def _main(html: str) -> str:
    return html.split('<main id="main-content"', 1)[1].split("</main>", 1)[0]


@pytest.fixture
def ruleset(db):
    from orientation.seeds import seed_ruleset_v1

    seed_ruleset_v1()


@pytest.fixture
def get(client, seeded, phase3_open, legal_published, ruleset):
    def _get(path: str) -> str:
        response = client.get(path)
        assert response.status_code == 200, (path, response.status_code)
        return response.content.decode("utf-8")

    return _get


def _step_url(client, lang: str = "fr") -> str:
    response = client.post(f"/{lang}/orientation/")
    assert response.status_code == 302, response.status_code
    return response["Location"]


# ---- the pages ------------------------------------------------------------------------------------------------


@pytest.mark.parametrize("path", STEP2)
def test_the_interior_grammar_one_entrance_one_h1_and_no_v4_layout(get, path):
    main = _main(get(path))
    assert main.count('<header class="ingresso') == 1, path
    assert main.count("<h1") == 1, path
    for legacy in (
        "layout-sidebar",
        'class="local-nav',
        "cta-panel",
        "page-header",
        'class="timeline',
        'training-phase" class="card',
    ):
        assert legacy not in main, (path, legacy)


@pytest.mark.parametrize("path", STEP2)
def test_one_primary_action_and_at_most_six_icons_in_the_body(get, path):
    main = _main(get(path))
    assert len(re.findall(r'class="btn btn--primary\b', main)) <= 1, path
    body_icons = [name for name in ICON.findall(main) if name != "ile-steps"]
    assert len(body_icons) <= 6, (path, body_icons)


@pytest.mark.parametrize("path", ["/fr/diplomes-et-titres/", "/fr/formation/"])
def test_the_advice_pages_end_on_the_one_action_and_say_who_can_help(get, path):
    soup = BeautifulSoup(_main(get(path)), "html.parser")
    chapters = soup.select("section.chapter, div.chapter")
    last = chapters[-1]
    assert "chapter--area" in last["class"] and last.select_one('[data-action="orientation"]'), path
    assert last.select_one('.aiuto a[href="mailto:contact@agamieuromed.org"]'), path
    register = soup.select_one(".registro.registro--two")
    current = "/fr/diplomes-et-titres/" if "diplomes" in path else "/fr/formation/"
    assert not register.select_one(f'a[href="{current}"]'), (
        "the page leaves its own row out of «Dans l'Espace Personnes»"
    )


def test_the_diplomas_five_moments_stand_open_on_the_line_with_their_terms(get):
    soup = BeautifulSoup(_main(get("/fr/diplomes-et-titres/")), "html.parser")
    line = soup.select_one("ol.linea.diploma-steps")
    assert line["data-steps"] == "5"
    stations = line.select(":scope > li")
    assert len(stations) == 5
    assert all("linea__step--pending" in li["class"] for li in stations), (
        "each still being verified: an open, broken ring"
    )
    assert all(li["id"].startswith("etape-") for li in stations), "each station keeps its anchor"
    terms = [tag for li in stations for tag in li.select(".termes__list .tag")]
    assert len(terms) >= 3 and all(tag["lang"] == "it" for tag in terms), "each Italian term under its own station"


def test_formation_draws_its_two_moments_on_the_line_and_no_card(get):
    soup = BeautifulSoup(_main(get("/fr/formation/")), "html.parser")
    line = soup.select_one("ol.linea.linea--phases")
    assert line["data-phases"] == "2"
    stations = line.select(":scope > li")
    assert [li["id"] for li in stations] == ["avant-le-depart", "apres-l-arrivee"]
    assert [li.select_one(".linea__kicker").get_text(strip=True) for li in stations] == [
        "Premier temps",
        "Second temps",
    ]
    assert [li.select_one("h2.linea__label") is not None for li in stations] == [True, True]
    assert not soup.select(".training-phase.card, .card__meta"), "a sequence, not two boxes"


@pytest.mark.parametrize("path", CALLOUT_PAGES)
def test_the_fraud_warning_is_an_amber_notice_said_three_times(get, path):
    soup = BeautifulSoup(_main(get(path)), "html.parser")
    callout = soup.select_one('aside[data-callout="antifraud"]')
    assert "notice--warning" in callout["class"] and "notice--institutional" not in callout["class"], path
    marks = [use["href"].rsplit("#", 1)[1] for use in callout.select("svg.notice__icon use")]
    assert marks == ["icon-shield-alert"], "the anti-fraud entry's mark, once"
    title = callout.select_one(".notice__title")
    assert title.name in ("h2", "h3") and title.get_text(strip=True) == "ATTENTION AUX FRAUDES", "the kind in words"


def test_the_antifraud_page_keeps_its_text_under_a_visible_title(get):
    from cms import locked_content

    soup = BeautifulSoup(_main(get("/fr/attention-aux-fraudes/")), "html.parser")
    inset = soup.select_one('[data-callout="antifraud"]')
    assert "notice--warning" in inset["class"]
    title = inset.select_one(".notice__title")
    assert title.get_text(strip=True) and "visually-hidden" not in title.get("class", [])
    assert [use["href"].rsplit("#", 1)[1] for use in inset.select("use")] == ["icon-shield-alert"]
    body = inset.select_one('[data-locked="p3.antifraud.body"]')
    assert body.get_text() == locked_content.text("p3.antifraud.body", "fr"), "byte-identical"


# ---- the questionnaire ------------------------------------------------------------------------------------------


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_first_page_holds_its_inset_and_its_one_action_in_the_entrance(get, lang):
    """
    The fix pass (W3-F1's review M4): «Commencer» stood under the first screen at every width. The action card takes
    the entrance's end seat (from 64rem; right after the lead on a phone), and «À lire avant de commencer» stays
    before it in the reading order, under the lead; the three moments follow.
    """
    soup = BeautifulSoup(_main(get(f"/{lang}/orientation/")), "html.parser")
    entrance = soup.select_one("header.ingresso")
    notice = entrance.select_one(".ingresso__text .ingresso__meta .wizard-disclaimer")
    action = entrance.select_one(".ingresso__aside .card--action")
    assert notice and action
    assert action.select_one("form.wizard-intro__start button.btn--primary")
    assert action.select_one(f'.wizard-intro__resume-link a[href="/{lang}/orientation/reprendre/"]')
    order = [el for el in entrance.find_all(True) if el in (notice, action)]
    assert order == [notice, action], "the inset is read before the action"
    line = soup.select_one("ol.linea.wizard-intro__steps")
    assert line and len(line.select(":scope > li")) == 3
    assert entrance.find_next("ol", class_="wizard-intro__steps") is line, "the three moments come after"
    assert not soup.select(".chapter--area .card--action"), "no second place for the action"


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_a_step_says_its_place_in_words_never_as_a_percentage(client, seeded, ruleset, lang):
    """
    FM12 (DESIGN_SYSTEM_V5 §11, CREATIVE_DIRECTION_V5 §20, RED_TEAM B4): «Question n sur N» in words — on an adaptive
    questionnaire a percentage jumps, and it opened at 0. No «%» in a rendered step, no <progress>; the count is the
    catalogue's own string, translated, and the quiet line under it stays.
    """
    from django.utils import translation

    with translation.override(lang):
        words = translation.gettext("Question %(n)s sur %(m)s au maximum")
    pattern = re.compile(re.escape(words).replace(re.escape("%(n)s"), r"(\d+)").replace(re.escape("%(m)s"), r"(\d+)"))

    def place(step) -> tuple[int, int]:
        label = step.find(id="wizard-progress-label").get_text(" ", strip=True)
        found = pattern.fullmatch(label)
        assert found, (label, words)
        return int(found.group(1)), int(found.group(2))

    url = _step_url(client, lang)
    soup = BeautifulSoup(client.get(url).content, "html.parser")
    step = soup.find(id="orientation-step")
    assert "%" not in str(step), "no percentage anywhere in the step, its attributes included"
    assert "%" not in soup.select_one("main").get_text(), "no percentage in the page's words"
    assert not soup.find("progress")
    n, most = place(step)
    assert n == 1 and most >= 1
    assert step.select_one(".wizard__progress-bar .wizard__progress-fill"), "the quiet line stays"
    # the next step says its new place, in words
    response = client.post(url, {"question_key": step["data-question"], "action": "answer", "answer": "work"})
    assert response.status_code == 302
    after = BeautifulSoup(client.get(url).content, "html.parser").find(id="orientation-step")
    assert "%" not in str(after)
    assert place(after)[0] == 2


def test_a_step_s_head_is_its_compact_title_alone(client, seeded, ruleset):
    """The fix pass (W3-F1's review m5): the page's sentence is said once, on the first page — not above every question."""
    soup = BeautifulSoup(client.get(_step_url(client)).content, "html.parser")
    head = soup.select_one("main .wizard__header")
    assert head.select_one("h1.wizard__title") and len(head.find_all(True)) == 1
    assert "Vos réponses servent uniquement" not in soup.select_one("main .wizard").get_text()


def test_a_step_is_one_question_with_one_primary_first(client, seeded, ruleset):
    url = _step_url(client)
    soup = BeautifulSoup(client.get(url).content, "html.parser")
    step = soup.find(id="orientation-step")
    bar = step.select_one('.wizard__progress-bar[role="progressbar"]')
    assert bar.select_one(".wizard__progress-fill") and bar["aria-labelledby"] == "wizard-progress-label"
    legend = step.find("fieldset").find("legend")
    assert legend.find(id="wizard-question")["tabindex"] == "-1"
    choices = step.select(".wizard__choice")
    assert choices and all(c.select_one("input.wizard__input") and c.select_one("label.wizard__label") for c in choices)
    buttons = step.find("form").find_all("button", type="submit")
    assert buttons[0]["value"] == "answer" and "btn--primary" in buttons[0]["class"]
    assert all("btn--primary" not in b["class"] for b in buttons[1:])
    assert not step.select('[role="group"]'), "the fieldset is the group: no second one inside it"


def test_an_error_is_wired_to_its_group_and_said_beside_its_mark(client, seeded, ruleset):
    url = _step_url(client)
    soup = BeautifulSoup(client.post(url, {"question_key": "objective", "action": "answer"}).content, "html.parser")
    fieldset = soup.find("fieldset")
    assert fieldset["aria-describedby"] == "answer-error" and fieldset["aria-invalid"] == "true"
    error = soup.find(id="answer-error")
    assert error["role"] == "alert" and error.get_text(strip=True)
    assert [use["href"].rsplit("#", 1)[1] for use in error.select("use")] == ["icon-circle-alert"]
    assert soup.find(id="answer-error").find_next(class_="wizard__choice"), "the words stand before the choices"


def test_a_multiple_choice_says_so_before_its_choices(rf):
    question = {
        "key": "languages",
        "type": "multiple",
        "text": "Quelles langues parlez-vous ?",
        "help": "",
        "lang": "fr",
        "fallback": False,
        "input_type": "checkbox",
        "choices": [{"key": "it", "label": "Italien", "lang": "fr"}, {"key": "fr", "label": "Français", "lang": "fr"}],
    }
    context = {
        "q": question,
        "step_number": 3,
        "progress": 50,
        "max_steps": 5,
        "can_go_back": True,
        "error": "Erreur.",
        "step_url": "/fr/orientation/session/x/",
        "session": {"reference": "ABC"},
    }
    soup = BeautifulSoup(render_to_string("orientation/_step.html", context, request=rf.get("/")), "html.parser")
    assert soup.find("fieldset")["aria-describedby"] == "answer-hint answer-error"
    hint = soup.find(id="answer-hint")
    assert hint.find_next(class_="wizard__choice") and not hint.find_previous(class_="wizard__choice")
    assert all(i["type"] == "checkbox" and not i.has_attr("required") for i in soup.select("input.wizard__input"))


# ---- the sheets ---------------------------------------------------------------------------------------------------


def test_the_orientation_sheet_imports_the_interior_first_and_draws_on_tokens():
    text = (ROOT / "apps" / "orientation" / "static" / "orientation" / "wizard.css").read_text(encoding="utf-8")
    css = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    assert re.findall(r'@import url\("([^"]+)"\);', css) == [
        "../css/v5/_pagina.css",
        "../css/v5/_interior.css",
        "../css/v5/_journey-passage.css",
    ]
    assert css.strip().startswith(
        '@import url("../css/v5/_pagina.css");\n@import url("../css/v5/_interior.css");\n'
        '@import url("../css/v5/_journey-passage.css");'
    )
    assert "!important" not in css and "transition: none" not in css
    radii = set(re.findall(r"border(?:-[a-z-]+)?-radius:\s*([^;]+);", css))
    assert radii <= {"var(--field-radius)", "var(--radius-sm)"}, radii
    assert not re.search(r"(?<![\w-])(?:margin|padding)-(?:left|right)\s*:|(?<![\w-])(?:left|right)\s*:", css), (
        "logical properties only"
    )


def test_v4_wizard_left_main_css_for_a_console_partial():
    main = (ROOT / "static" / "css" / "main.css").read_text(encoding="utf-8")
    assert "v4/wizard.css" not in re.findall(r'@import url\("([^"]+)"\)', main)
    assert not (ROOT / "static" / "css" / "v4" / "wizard.css").exists()
    console = (ROOT / "apps" / "portal" / "static" / "portal" / "console.css").read_text(encoding="utf-8")
    assert "_wizard.css" not in re.findall(r'@import url\("([^"]+)"\)', console), "never in the shared console entry"
    situation = (ROOT / "apps" / "portal" / "static" / "portal" / "situation.css").read_text(encoding="utf-8")
    assert re.findall(r'@import url\("([^"]+)"\)', situation) == [
        "v5/_wizard.css",
        "v5/_journey-nodes.css",
        "v5/_journey-stepper.css",
    ], "«Ma situation»'s page-only sheet: the guided form first, then its Stepper (W3-D)"


def test_the_guided_form_draws_the_console_s_three_corners_and_a_foot_inside_the_page():
    css = re.sub(r"/\*.*?\*/", "", WIZARD_PARTIAL.read_text(encoding="utf-8"), flags=re.S)
    radii = set(re.findall(r"border(?:-[a-z-]+)?-radius:\s*([^;]+);", css))
    assert radii <= {"var(--radius-sm)", "var(--field-radius)", "var(--radius-lg)", "var(--radius-full)"}, radii
    shadows = {value.strip() for value in re.findall(r"box-shadow:\s*([^;]+);", css)}
    assert shadows <= {
        "var(--shadow-2)",
        "none",
        "inset 0 0 0 1px var(--fill-primary)",
        "inset 0 0 0 1px var(--field-edge-invalid)",
        "inset 0 0 0 2px var(--surface-sheet)",
    }, shadows
    foot = re.search(r"\.wiz__foot\s*\{([^}]*)\}", css).group(1)
    assert "sticky" not in foot and "backdrop-filter" not in css, "the foot is part of the page; glass has one seat"
    assert "--light-focus" not in css, "no light behind the question: the glow is retired"
