"""
Every surface of the reserved area must be reachable by CLICKING, not only by typing its URL.

The Academy and the help desk each appended their own row to the reserved area's navigation from
inside themselves. That reads sensibly until you ask how somebody reaches the first page of a
module they have never opened: the row appeared once you were already there.

Both answered 200, had exactly one `h1`, and raised no console error. Every unit test passed. The
modules were simply unreachable — found by walking the mandate's flow
`… → DOCUMENTI → FORMAZIONE/SPORTELLO` in a browser instead of trusting that each page worked on
its own.

That is the shape of defect this file exists for: not a broken page, a missing path to it.
"""

from __future__ import annotations

import pytest
from django.urls import reverse

from portal import services
from portal.tests.conftest import *  # noqa: F401,F403 — seeded, alice, private media root

pytestmark = pytest.mark.django_db

#: Every surface a signed-in person is meant to reach from the reserved area.
EXPECTED_KEYS = {
    "dashboard",
    "situation",
    "cases",
    "requests",
    "pathways",
    "documents",
    "deadlines",
    "messages",
    "academy",
    "helpdesk",
}


def test_the_navigation_lists_every_surface_a_person_can_reach(alice):
    keys = {item["key"] for item in services.navigation(alice)}
    missing = EXPECTED_KEYS - keys
    assert not missing, f"unreachable by clicking: {sorted(missing)}"


def test_every_navigation_url_resolves_and_is_unique(alice):
    items = services.navigation(alice)
    urls = [item["url"] for item in items]
    assert all(urls), "a navigation row has no URL"
    assert len(set(urls)) == len(urls), "two rows point at the same page"
    assert urls == sorted(urls, key=lambda u: urls.index(u)), "order is not stable"


def test_the_dashboard_page_really_links_to_the_academy_and_the_help_desk(client, seeded, alice):
    """
    The service is not the page. Asserted on the rendered HTML, because a row the template drops —
    a permission guard, a truncation, a `slice` filter — would leave this service test green and
    the user still stuck.
    """
    client.force_login(alice)
    html = client.get(reverse("portal:dashboard")).content.decode()
    assert reverse("academy:catalogue") in html
    assert reverse("helpdesk:requests") in html


@pytest.mark.parametrize("key", sorted(EXPECTED_KEYS))
def test_each_surface_answers_from_a_signed_in_person(client, seeded, alice, key):
    """Reachable AND alive: a link to a 500 is not a path."""
    client.force_login(alice)
    url = next(item["url"] for item in services.navigation(alice) if item["key"] == key)
    response = client.get(url)
    assert response.status_code in (200, 302), f"{key} answered {response.status_code}"


def test_the_help_desk_does_not_list_itself_twice(client, seeded, alice):
    """
    Its own view still appends a fallback row. With the portal listing it, that would duplicate.

    The Academy already guarded against this; the help desk did not, and only did not break because
    the portal never listed it.
    """
    from helpdesk.views import _navigation

    keys = [item["key"] for item in _navigation(alice, "helpdesk")]
    assert keys.count("helpdesk") == 1, keys


def test_the_current_entry_is_marked_exactly_once(alice):
    for key in sorted(EXPECTED_KEYS):
        marked = [item["key"] for item in services.navigation(alice, key) if item["current"]]
        assert marked == [key], (key, marked)


# ---- the way back to a role's own surface -------------------------------------------------------
@pytest.mark.parametrize(
    ("role_attr", "expected_key", "route"),
    [
        ("AUTHORISED_ACTOR", "selection", "selection:workspace"),
        ("COMPANY", "company", "companies:dashboard"),
        ("PROFESSIONAL", "helpdesk-queue", "helpdesk:queue"),
    ],
)
def test_a_role_can_get_back_to_its_own_surface(user_factory, role_attr, expected_key, route):
    """
    Each role LANDS on its own screen at sign-in, and each of those screens links to the dashboard.
    None of them was linked from the dashboard — so following that one link was a one-way trip, and
    the way back was signing in again.

    The modules could not fix this from their side: they are not rendered on this page.
    """
    from accounts import roles

    user = user_factory(f"back-{expected_key}@example.test", role=getattr(roles, role_attr))
    items = services.navigation(user)
    keys = {item["key"] for item in items}
    assert expected_key in keys, f"{role_attr} has no route back to {route}"
    assert next(i["url"] for i in items if i["key"] == expected_key) == reverse(route)


def test_a_person_is_offered_no_surface_their_role_cannot_use(alice):
    """
    « Un module non disponible ne se montre pas. » A menu item that answers 403 is a way of telling
    somebody that something exists.
    """
    keys = {item["key"] for item in services.navigation(alice)}
    assert keys & {"selection", "company", "helpdesk-queue"} == set()
    assert keys == EXPECTED_KEYS


def test_every_role_surface_answers_for_the_role_that_is_offered_it(client, seeded, user_factory):
    from accounts import roles

    for role_attr, key in (("AUTHORISED_ACTOR", "selection"), ("COMPANY", "company")):
        user = user_factory(f"alive-{key}@example.test", role=getattr(roles, role_attr))
        client.force_login(user)
        url = next(i["url"] for i in services.navigation(user) if i["key"] == key)
        assert client.get(url).status_code in (200, 302), key
