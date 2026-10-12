"""
Compliance of the rendered wizard pages: locked disclaimer, no forbidden formulations, no promise
wording, informational wording present, accessibility structure, self-only resources.
"""

import re

import pytest
from bs4 import BeautifulSoup

from cms import locked_content
from cms.forbidden import scan
from orientation.models import OrientationSession
from orientation.tests.conftest import walk

pytestmark = [pytest.mark.django_db, pytest.mark.compliance]

DISCLAIMER = locked_content.text("p3.persons.how_it_works", "fr")
PROMISE_PATTERNS = [
    r"visa garanti",
    r"résultat garanti",
    r"\bgaranti[es]?\b",
    r"\bgarantie\b",
    r"entrée assurée",
    r"guaranteed",
    r"visto garantito",
    r"certitude",
    r"approbation",
    r"prévision",
]
INTERNAL_MARKERS = ["CONTENT_PENDING_LEGAL_REVIEW", "lorem ipsum", "TODO", "[ ]"]

PATHS = [
    [("objective", "work"), ("work_profile", "salaried"), ("training_interest", "true")],
    [("objective", "work"), ("work_profile", "highly_qualified"), ("training_interest", "false")],
    [("objective", "work"), ("work_profile", "seasonal"), ("training_interest", "false")],
    [("objective", "work"), ("work_profile", "unsure")],
    [("objective", "study"), ("study_type", "university")],
    [("objective", "study"), ("study_type", "training_before_departure")],
    [("objective", "family"), ("family_member_status", "yes")],
    [("objective", "family"), ("family_member_status", "no")],
    [("objective", "self_employment")],
    [("objective", "research")],
    [("objective", "other")],
]


def _rendered_pages(client, lang="fr"):
    """Yield (label, html) for the intro, every question page and every result page of the v1 ruleset."""
    yield "start", client.get(f"/{lang}/orientation/").content.decode()
    yield "resume", client.get(f"/{lang}/orientation/reprendre/").content.decode()
    for answers in PATHS:
        url = client.post(f"/{lang}/orientation/")["Location"]
        for key, value in answers:
            yield f"step:{key}", client.get(url).content.decode()
            walk(client, url, [(key, value)])
        assert OrientationSession.objects.latest("created_at").is_completed
        yield f"result:{answers}", client.get(f"{url}resultat/").content.decode()


def _without_locked_texts(html: str) -> str:
    text = html.replace(DISCLAIMER, "")
    for entry in locked_content.get("p3.persons.pathways", "fr")[0]:
        text = text.replace(entry["title"], "").replace(entry["description"], "")
    return text


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_no_forbidden_formulations_or_promises(client, active_ruleset, lang):
    for label, html in _rendered_pages(client, lang):
        assert not scan(html), (label, scan(html))
        assert "®" not in html
        stripped = _without_locked_texts(html)
        for pattern in PROMISE_PATTERNS:
            assert not re.search(pattern, stripped, flags=re.IGNORECASE), (label, pattern)
        for marker in INTERNAL_MARKERS:
            assert marker not in html, (label, marker)


def test_result_pages_carry_disclaimer_and_informational_wording(
    client, active_ruleset, phase3_open
):  # prescribed Phase 3 wording is rendered only once gate G3 is open
    for label, html in _rendered_pages(client):
        if not label.startswith("result"):
            continue
        assert DISCLAIMER in html, label
        assert "Pré-évaluation à caractère informatif" in html, label
        assert 'data-result-kind="informational"' in html
        assert "autorités compétentes" in html
        assert "Italy Legal Entry™" in html


def test_every_page_has_single_h1_main_landmark_and_labelled_controls(client, active_ruleset):
    for label, html in _rendered_pages(client):
        soup = BeautifulSoup(html, "html.parser")
        assert len(soup.find_all("h1")) == 1, label
        assert soup.find("main", id="main-content") is not None, label
        assert soup.find("nav", class_="breadcrumbs") is not None, label
        for control in soup.find_all(["input", "select", "textarea"]):
            if control.get("type") in ("hidden", "submit") or control.get("aria-hidden") == "true":
                continue
            assert soup.find("label", {"for": control.get("id")}) is not None or control.get("aria-label"), (
                label,
                control,
            )
        for button in soup.find_all("button"):
            assert button.get_text(strip=True), (label, "button without text")


def test_question_pages_use_fieldset_legend_progressbar_and_help(client, active_ruleset):
    url = client.post("/fr/orientation/")["Location"]
    soup = BeautifulSoup(client.get(url).content, "html.parser")
    fieldset = soup.find("fieldset")
    assert fieldset is not None
    legend = fieldset.find("legend")
    assert legend is not None and legend.get_text(strip=True)
    bar = soup.find(attrs={"role": "progressbar"})
    for attr in ("aria-valuenow", "aria-valuemin", "aria-valuemax", "aria-valuetext", "aria-labelledby"):
        assert bar.get(attr) is not None, attr
    assert soup.find(id=bar["aria-labelledby"]) is not None
    assert soup.find("details", class_="wizard__help") is not None  # explanation toggle, no JS needed
    assert soup.find("input", {"type": "radio"}) is not None
    form = soup.find("form", class_="wizard__form")
    assert form["method"] == "post" and form["hx-post"] == url
    assert 'style="' not in str(soup.find(id="orientation-step"))  # CSP: no inline styles


def test_pages_load_only_self_hosted_resources(client, active_ruleset):
    for label, html in _rendered_pages(client):
        externals = [s for s in re.findall(r'(?:src|href)="(https?://[^"]+)"', html) if "testserver" not in s]
        assert not externals, (label, externals)
        assert "/static/css/dist/orientation/wizard.css" in html, label
        for src in re.findall(r'<script[^>]+src="([^"]+)"', html):
            assert src.startswith("/static/"), (label, src)


def test_public_email_only(client, active_ruleset):
    for label, html in _rendered_pages(client):
        emails = set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}", html))
        assert emails <= {"contact@agamieuromed.org"}, (label, emails)


def test_start_page_registered_as_public_route():
    from core.public_routes import all_routes

    paths = {(r.app, r.path, r.requires_gate) for r in all_routes()}
    assert ("orientation", "orientation/", "") in paths
    assert ("orientation", "orientation/reprendre/", "") in paths
    assert not any(r.path.startswith("orientation/session") for r in all_routes())


def test_sitemap_lists_only_start_page(client, active_ruleset):
    xml = client.get("/sitemap.xml").content.decode()
    assert "/fr/orientation/" in xml
    assert "/orientation/session/" not in xml


def test_robots_disallows_sessions(client):
    body = client.get("/robots.txt").content.decode()
    assert "Disallow: /*/orientation/session/" in body
