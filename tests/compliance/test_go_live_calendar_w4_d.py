"""
The release's calendar (W4-D; plan §3.6 item 4, risk 18 / O39 of the execution plan).

From the day the release was prepared (16 October 2026) to sixty days after it, on the database a deployment starts
with — ``seed_all`` and no flag row written by anyone — no page offers a call to action whose date has passed and no
gate opens on its own: the home's Forum banner expired on 2 October 2026 at 00:00 (``forum_banner``), the Forum's
registration closed when its event ended (2 October 2026, 18:00), the Phase 3 pages stay 404 until the owner
authorises Phase 3, and the Virtual Forum stays closed whatever the Morocco Forum's dates (29–30 October 2026), which
no code reads. With the owner's documented schedule instead (Phase 3 authorised, the Forum switched to its permanent
mode after the event), the Forum page loses its registration chapter and its Event markup, and every link the pages
show answers. docs/design-v5/QA/v54/w4-d/GO_LIVE_PHASE.md reads these states page by page.
"""

from __future__ import annotations

import datetime as dt
import re
from zoneinfo import ZoneInfo

import pytest
from django.test import Client
from freezegun import freeze_time

from core import flags, gates

pytestmark = [pytest.mark.compliance, pytest.mark.django_db]

ROME = ZoneInfo("Europe/Rome")
PHASE3_FROM = dt.datetime(2026, 10, 2, 0, 0, tzinfo=ROME)
FORUM_END = dt.datetime(2026, 10, 2, 18, 0, tzinfo=ROME)

#: The release's window: the day it was prepared, the two days of the Morocco Forum, the first night after it (half
#: past midnight in Rome, still the day before in UTC), and the sixtieth day.
MOMENTS = {
    "release-16-oct": dt.datetime(2026, 10, 16, 10, 0, tzinfo=ROME),
    "casablanca-29-oct": dt.datetime(2026, 10, 29, 10, 0, tzinfo=ROME),
    "rabat-30-oct-evening": dt.datetime(2026, 10, 30, 20, 0, tzinfo=ROME),
    "first-night-after-31-oct": dt.datetime(2026, 10, 31, 0, 30, tzinfo=ROME),
    "day-60-15-dec": dt.datetime(2026, 12, 15, 23, 30, tzinfo=ROME),
}

PHASE3_PAGES = ("/fr/institutions/", "/fr/universites-et-formation/", "/fr/projet-pilote/", "/fr/faq/")
HREF = re.compile(r'href="(/(?:fr|ar)/[^"#]*)')
#: The registration's call to action: a button (templates/forum/partials/hero.html and cta_row.html), never the index.
REGISTER_BUTTON = re.compile(r'<a class="btn[^"]*" href="#forum-registration"')


def test_the_registration_button_is_found_while_registration_is_open(client, seeded, legal_published):
    """The control: before the event, with the forms open, the button the checks below look for is on the page — so
    their «not found» means gone, not misspelt."""
    with freeze_time(dt.datetime(2026, 9, 25, 11, 0, tzinfo=ROME).astimezone(dt.UTC)):
        flags.invalidate()
        forum = client.get("/fr/forum/").content.decode()
        assert REGISTER_BUTTON.search(forum) and 'id="forum-registration-form"' in forum
        assert 'data-banner="forum"' in client.get("/fr/").content.decode()


def test_a_fresh_deployment_shows_no_past_call_to_action(client, seeded):
    closed = (
        "legal_pages_available",
        "public_forms_enabled",
        "phase3_public",
        "forum_banner_visible",
        "forum_permanent_mode",
        "virtual_forum_enabled",
        "newsletter_enabled",
    )
    for name, moment in MOMENTS.items():  # one seed for the five moments: the database does not change between them
        with freeze_time(moment.astimezone(dt.UTC)):
            flags.invalidate()
            snapshot = gates.snapshot()
            assert {key: snapshot[key] for key in closed} == dict.fromkeys(closed, False), (name, snapshot)

            home = client.get("/fr/")
            assert home.status_code == 200, name
            assert 'data-banner="forum"' not in home.content.decode(), (name, "the banner of a past event")

            forum = client.get("/fr/forum/").content.decode()
            # The page's index keeps its «INSCRIPTION» entry (a link to the chapter that says it is closed); what must
            # be gone is the button that invites to register — in the entrance and in the page's one action.
            assert not REGISTER_BUTTON.search(forum), (name, "a registration call to action after the event")
            assert 'id="forum-registration-form"' not in forum, name
            assert 'data-registration="closed"' in forum, (name, "the registration chapter says it is closed")
            assert 'data-gate="virtual-forum"' not in forum, name

            register = client.get("/fr/forum/inscription/").content.decode()
            assert 'data-registration="closed"' in register and 'id="forum-registration-form"' not in register, name

            for path in (*PHASE3_PAGES, "/fr/forum-virtuel/"):
                assert client.get(path).status_code == 404, (name, path)


def test_the_owners_schedule_shows_the_permanent_forum_and_no_dead_link(seeded, set_flag):
    """Phase 3 authorised and the Forum switched to its permanent mode after the event (docs/DEPLOYMENT.md §3 item 10,
    the phase console): the event's registration and its schema.org Event leave the page; nothing points to a page
    that does not answer."""
    set_flag("phase3_public", True, enabled_from=PHASE3_FROM)
    set_flag("forum_permanent_mode", True, enabled_from=FORUM_END)
    client = Client()
    for moment in (MOMENTS["release-16-oct"], MOMENTS["day-60-15-dec"]):
        with freeze_time(moment.astimezone(dt.UTC)):
            flags.invalidate()
            forum = client.get("/fr/forum/").content.decode()
            assert "FORUM PERMANENT VÉNÉTIE–MAROC" in forum
            assert 'id="forum-registration"' not in forum and not REGISTER_BUTTON.search(forum)
            assert 'type="application/ld+json"' not in forum, "no Event markup for an event that has passed"
            assert 'data-banner="forum"' not in client.get("/fr/").content.decode()
            for path in PHASE3_PAGES:
                assert client.get(path).status_code == 200, path

    with freeze_time(MOMENTS["release-16-oct"].astimezone(dt.UTC)):
        flags.invalidate()
        pages = (
            "/fr/",
            "/ar/",
            "/fr/forum/",
            "/fr/le-projet/",
            "/fr/parcours/",
            "/fr/entreprises/",
            "/fr/compte/login/",
        )
        links: set[str] = set()
        for page in pages:
            response = client.get(page)
            assert response.status_code == 200, page
            links.update(HREF.findall(response.content.decode()))
        dead = sorted(link for link in links if client.get(link).status_code >= 400)
        assert len(links) > 40, links
        assert not dead, dead
