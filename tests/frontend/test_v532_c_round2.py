"""
V5.32 lane C, round 2 (the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026) — the surfaces this
round adds, measured and scoped:

* the company space: a need's course has its own bundle (companies/course.css), linked by the need's page alone — the
  space's sheet (companies/companies.css) stays at its measure (test_platform_v524_plat.CEILINGS);
* the university proposal (P2-2 of the integration review): its head draws no photograph — the campus frame
  `universities.exchange` belongs to /universites-et-formation/, and a frame is never reused across two pages;
* «Demande transmise»: a request of a family's space returns to that space by name — its crumb and its return action —
  and the contact's receipt is unchanged;
* the register of actors on /institutions/ (P2-6 of the integration review): each row opens on a capital at display
  only — the text untouched, Arabic left alone.

Budgets: gzip -9 (Python gzip.compress(b, 9)) of the dist file; ceiling = the measure of 12 Nov 2026 rounded up, ≤ +3 %.
"""

from __future__ import annotations

import gzip
import re
from pathlib import Path

import pytest
from bs4 import BeautifulSoup
from django.conf import settings

pytestmark = pytest.mark.django_db

ROOT = Path(settings.BASE_DIR)
DIST = ROOT / "static" / "css" / "dist"
TEMPLATES = ROOT / "templates"

#: measured 12 Nov 2026 (664 B) → ceiling ≤ +3 % (round 2's ecosystem/proposta.css retired with the frame, P2-2)
CEILINGS = {"companies/course.css": 674}


@pytest.mark.parametrize("name", sorted(CEILINGS))
def test_the_round_s_new_bundles_hold_their_budget(name):
    assert len(gzip.compress((DIST / name).read_bytes(), 9)) <= CEILINGS[name], name


@pytest.mark.parametrize(
    ("bundle", "templates"),
    [
        ("css/dist/companies/course.css", {"companies/need_detail.html"}),
    ],
)
def test_each_new_bundle_is_linked_only_where_it_draws(bundle, templates):
    found = {p.relative_to(TEMPLATES).as_posix() for p in TEMPLATES.rglob("*.html") if bundle in p.read_text("utf-8")}
    assert found == templates, found


@pytest.fixture
def phase3(set_flag, monkeypatch):
    """Gate G3 open (the institutions' and universities' pages are public: the receipt's way back is gate-aware)."""
    import datetime as dt

    from core import clock, flags

    monkeypatch.setattr(clock, "now", lambda: dt.datetime(2026, 10, 3, 10, 0, tzinfo=dt.UTC))
    set_flag("phase3_public", True, enabled_from=dt.datetime(2026, 10, 2, tzinfo=dt.UTC))
    flags.invalidate()
    yield
    flags.invalidate()


def _head(html: str):
    return BeautifulSoup(html, "html.parser").select_one("header.ingresso")


def test_the_university_proposal_reuses_no_frame_and_the_campus_frame_has_one_page(client, seeded):
    """RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026 (P2-2 of
    the integration review: round 2 seated the campus frame of /universites-et-formation/, the page one click before,
    in this head). The head draws no photograph now; stronger than round 2's test, which held the frame there: the campus
    frame `universities.exchange` is drawn by that landing alone among the public templates (the specimen board aside),
    so no other head — the institution's included — carries it, and the head's own sheet left with it."""
    html = client.get("/fr/collaboration/universites-formation/").content.decode()
    head = _head(html)
    assert head is not None and not head.select("figure, picture, img, [data-slot]"), "no photograph in the head"
    assert "universities.exchange" not in html and "echange-campus" not in html
    assert "ecosystem/proposta.css" not in html and "ecosystem/intesa.css" not in html, "the head's own sheet left"
    assert not (DIST / "ecosystem" / "proposta.css").exists()
    users = {
        p.relative_to(TEMPLATES).as_posix()
        for p in TEMPLATES.rglob("*.html")
        if "dev" not in p.relative_to(TEMPLATES).parts and '"universities.exchange"' in p.read_text("utf-8")
    }
    assert users == {"ecosystem/universities.html"}, users


@pytest.mark.parametrize(
    ("kind", "space", "back"),
    [
        ("company_needs", "Espace Entreprises", "/fr/entreprises/"),
        ("institution_proposal", "Espace Institutions", "/fr/institutions/"),
        ("university_proposal", "Espace Universités et Formation", "/fr/universites-et-formation/"),
    ],
)
def test_a_family_s_receipt_returns_to_its_space_by_name(client, phase3, kind, space, back):
    soup = BeautifulSoup(client.get(f"/fr/demande-transmise/?k={kind}").content.decode(), "html.parser")
    crumbs = [(a.get_text(strip=True), a["href"]) for a in soup.select("nav.breadcrumbs a, .breadcrumbs a")]
    assert (space, back) in crumbs, crumbs
    actions = [(a.get_text(strip=True), a["href"]) for a in soup.select(".receipt__actions a")]
    assert (f"Retour à l’e{space[1:]}", back) in actions, actions
    assert soup.select_one(f'.receipt[data-enquiry-done="{kind}"]')


def test_the_contact_receipt_is_unchanged(client):
    soup = BeautifulSoup(client.get("/fr/demande-transmise/?k=contact").content.decode(), "html.parser")
    actions = [(a.get_text(strip=True), a["href"]) for a in soup.select(".receipt__actions a")]
    assert actions[0] == ("Retour à la page précédente", "/fr/contact/"), actions
    assert [a.get_text(strip=True) for a in soup.select("nav.breadcrumbs a, .breadcrumbs a")] == ["Accueil"]


def test_the_register_of_actors_capitalises_its_rows_at_display_only():
    """P2-6 of the integration review (V5.32): a recipient of the locked sentence that starts in lower case where the
    sentence runs on («organismes publics») opens on a capital once it is a row — by the team's precedent
    (pathways/_diplomas.css `.dossier__definizione::first-letter`), on the row's block box, Arabic left out (no case,
    and no pseudo-element splitting a joined word). Presentation only: the sentence itself is tested as written
    (apps/ecosystem/tests/test_gated_pages.py, test_pages_v522_p1.test_the_recipients_spans_rebuild_the_sentence)."""
    source = (ROOT / "apps/ecosystem/static/ecosystem/_institutions.css").read_text("utf-8")
    rule = r"\.istituzioni-aula \.emiciclo__voce:not\(:lang\(ar\)\)::first-letter \{\s*text-transform: capitalize;\s*\}"
    assert re.search(rule, source)
    assert re.search(r"\.istituzioni-aula \.emiciclo__voce \{[^}]*display: block;", source), "a block box"
    dist = (DIST / "ecosystem" / "institutions.css").read_text("utf-8")
    assert ".istituzioni-aula .emiciclo__voce:not(:lang(ar)):first-letter{text-transform:capitalize}" in dist
