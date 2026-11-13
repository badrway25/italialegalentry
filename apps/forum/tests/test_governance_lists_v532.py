"""
V5.32 lane E — the Forum governance in the console's product vocabulary (the PLATFORM=READY round of the owner's
GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026): the atrium's head on every page, the platform
sheet, the two long registers (the proposals, the projects) on the platform's list toolkit — narrowing only what the
member may read, the commission filter offering only the commissions those rows sit in — and the module's entries
as rows of the rail (a glyph, their own titled section).
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from django.urls import reverse
from django.utils import translation

from forum import governance_lists
from forum import governance_services as services
from forum.governance import ProposalStatus

pytestmark = [pytest.mark.django_db, pytest.mark.urls("forum.tests.governance_urlconf")]

TEMPLATES = Path(__file__).resolve().parents[3] / "templates" / "forum" / "governance"
BODY = "Proposition de coopération entre les chambres consulaires, avec un calendrier annuel partagé."


def _submitted(member, commission, title):
    proposal = services.open_proposal(member.user, commission, title_fr=title, body_fr=BODY)
    services.transition_proposal(proposal, ProposalStatus.SUBMITTED, actor=member.user)
    return proposal


def _html(client, user, name, query=""):
    client.force_login(user)
    response = client.get(reverse(f"forum_governance:{name}") + query)
    assert response.status_code == 200
    return response.content.decode()


def test_every_page_head_is_the_atriums_and_the_module_links_the_platform_sheet():
    for path in sorted(TEMPLATES.glob("*.html")):
        text = path.read_text(encoding="utf-8")
        if '<header class="ws-head' not in text:
            continue
        head = text.split('<header class="ws-head', 1)[1].split("</header>", 1)[0]
        assert 'data-atrium="register"' in head, path.name
        assert '{% include "portal/partials/atrium_eyebrow.html" %}' in head, path.name
    base = (TEMPLATES / "base_governance.html").read_text(encoding="utf-8")
    assert "css/dist/portal/platform.css" in base and "overlay-panels.css" not in base
    for page in ("proposals.html", "projects.html"):  # the page that draws the drawer links its sheet (CONTRACT §1)
        text = (TEMPLATES / page).read_text(encoding="utf-8")
        assert (
            '{% if listing.show %}<link rel="stylesheet" href="{% static \'css/dist/core/overlay-panels.css\' %}">'
            in text
        )


def test_the_proposals_narrow_by_words_and_state_and_the_mine_register_stays_whole(
    client, governance_open, member, referent, commission
):
    _submitted(member, commission, "Rencontres consulaires")
    draft = services.open_proposal(member.user, commission, title_fr="Calendrier partagé", body_fr=BODY)
    html = _html(client, member.user, "proposals")
    assert 'class="lst__bar"' in html and 'id="lst-propositions-filters"' in html
    html = _html(client, member.user, "proposals", "?q=consulaires")
    table = html.split('id="all-proposals-title"', 1)[1]
    assert "Rencontres consulaires" in table and "Calendrier partagé" not in table
    mine = html.split('id="mine-title"', 1)[1].split("</section>", 1)[0]
    assert "Calendrier partagé" in mine, "«Mes propositions» is never narrowed"
    html = _html(client, member.user, "proposals", "?etat=" + ProposalStatus.DRAFT)
    table = html.split('id="all-proposals-title"', 1)[1]
    assert draft.title_fr in table and "Rencontres consulaires" not in table
    html = _html(client, member.user, "proposals", "?q=introuvable")
    assert 'class="lst-empty"' in html


def test_the_commission_filter_offers_only_the_commissions_the_rows_sit_in(
    client, governance_open, forum_actor, member, commission, other_commission
):
    _submitted(member, commission, "Rencontres consulaires")
    _submitted(member, commission, "Calendrier partagé")
    outside = forum_actor("ailleurs@example.test", commission=other_commission)
    _submitted(outside, other_commission, "Hors de mon mandat")
    scoped = services.proposals_for(member.user)
    spec = governance_lists.proposals(scoped)
    assert [value for value, _label in spec.filters[0].options()] == [str(commission.pk)]
    html = _html(client, member.user, "proposals", f"?commission={other_commission.pk}")
    assert other_commission.name_fr not in html, "a crafted commission is ignored, and its name never printed"
    assert "Hors de mon mandat" not in html


def test_the_rail_draws_the_forums_entries_as_rows_of_its_own_section(member):
    with translation.override("fr"):
        rows = [row for row in services.navigation(member.user, "forum_proposals") if row["key"].startswith("forum_")]
    assert [row["key"] for row in rows][:4] == [
        "forum_participation",
        "forum_commissions",
        "forum_proposals",
        "forum_projects",
    ]
    for row in rows:
        assert row["icon"] and row["group"] == "Forum permanent" and row["kind"] == "page", row["key"]
        assert set(row) >= {"bottom", "yields", "lines", "stacks", "space", "current"}
    assert [row["key"] for row in rows if row["current"]] == ["forum_proposals"]
    assert "Forum — ma participation" not in [str(row["label"]) for row in rows], "the section names the module once"


def test_the_projects_register_is_on_the_toolkit(client, governance_open, member, referent, commission):
    first = _submitted(member, commission, "Rencontres consulaires")
    second = _submitted(member, commission, "Calendrier partagé")
    for proposal in (first, second):
        services.transition_proposal(proposal, ProposalStatus.UNDER_REVIEW, actor=referent.user)
        services.transition_proposal(proposal, ProposalStatus.ACCEPTED, actor=referent.user, note="Retenue.")
        services.promote_to_project(proposal, lead=member.profile, actor=referent.user)
    html = _html(client, member.user, "projects")
    assert 'class="lst__bar"' in html and "js/dist/listing.js" in html
    # one commission, one state: no filter can narrow these two, so none is offered and no drawer is drawn (the
    # toolkit's rule, portal.listing: a filter needs two values present, or one chosen)
    assert 'id="lst-projets-filters"' not in html
    titles = re.findall(r'class="reg-row__link"[^>]*>([^<]+)</a>', html)
    assert len(titles) == 2
    html = _html(client, member.user, "projects", "?q=" + titles[0][:8])
    assert len(re.findall(r'class="reg-row__link"', html)) == 1
