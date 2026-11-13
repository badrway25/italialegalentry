"""
V5.32 lane B — the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026: the orientation result
draws the pre-evaluated family beside its pathway's photograph — the site's one pairing (pathways.services.pathway_frame
over pages.services.PATHWAY_FRAMES: the frame the Parcours explorer, the sheet's head and the home draw), decorative
(alt="": the family's title stands beside it), lazy, its box reserved, its `sizes` the one the view states. No
photograph for a situation to examine individually, for the family-reunification pathway (no rights-safe family
photograph: its sheet draws a semantic plate) or before gate G3 (the pathways' presentation is not public yet).
"""

import pytest
from bs4 import BeautifulSoup
from django.urls import reverse

from orientation.models import OrientationResult
from orientation.tests.conftest import walk
from orientation.views import RESULT_FRAME_SIZES

pytestmark = pytest.mark.django_db

FRAME = ".wizard-result__percorso--foto picture.wizard-result__foto img"


def _result(client, answers):
    response = client.post("/fr/orientation/")
    assert response.status_code == 302
    walk(client, response["Location"], answers)
    result = OrientationResult.objects.latest("created_at")
    page = client.get(reverse("orientation:result", kwargs={"session_id": result.session_id}))
    assert page.status_code == 200
    return result, BeautifulSoup(page.content, "html.parser")


def test_the_result_draws_the_pathway_s_own_frame_beside_its_family(client, active_ruleset, phase3_open):
    from pathways.services import pathway_frame

    result, soup = _result(client, [("objective", "work"), ("work_profile", "salaried"), ("training_interest", "true")])
    assert result.outcome.pathway_key == "salaried_work"
    imgs = soup.select(FRAME)
    assert len(imgs) == 1
    img = imgs[0]
    frame = pathway_frame("salaried_work", RESULT_FRAME_SIZES)
    assert img["src"] == frame.src and img["sizes"] == RESULT_FRAME_SIZES
    assert img["alt"] == "" and img["loading"] == "lazy" and img.get("width") and img.get("height")
    # the frame stands beside the family's row, inside the same block — never a second heading or a link
    row = soup.select_one(".wizard-result__percorso--foto")
    assert row.select_one("ul.registro.wizard-result__family > li.registro__row[data-pathway='salaried_work']")
    assert not row.select("picture a, picture h2, picture h3")


@pytest.mark.parametrize(
    "answers",
    [
        [("objective", "family"), ("family_member_status", "unsure")],
        [("objective", "family"), ("family_member_status", "yes")],
    ],
    ids=["individual-analysis", "family-reunification"],
)
def test_no_frame_where_no_relevant_photograph_exists(client, active_ruleset, phase3_open, answers):
    _result_, soup = _result(client, answers)
    assert not soup.select(".wizard-result__foto, .wizard-result__percorso--foto")


def test_no_frame_before_the_gate(client, active_ruleset):
    result, soup = _result(client, [("objective", "work"), ("work_profile", "salaried"), ("training_interest", "true")])
    assert result.outcome.pathway_key == "salaried_work"
    assert not soup.select(".wizard-result__foto, .wizard-result__percorso--foto")
