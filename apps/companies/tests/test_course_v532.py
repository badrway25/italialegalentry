"""
V5.32 (lane C, round 2; the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026): where a need
stands — its course on its own page, from the record only (companies.services.need_course, templates/companies/
need_detail.html, the page's own bundle companies/course.css). The declared states in their order; the stations passed
carry the date the history records; a pause is said on the station it holds; a closed need never taken in charge has
no «Pris en charge» station; a withdrawn need has no course.
"""

from __future__ import annotations

import datetime as dt
from types import SimpleNamespace

from bs4 import BeautifulSoup
from django.urls import reverse

from companies import services
from companies.models import CompanyNeed, NeedEvent, NeedStatus

S = NeedStatus


def _ev(src: str, dst: str, day: int) -> SimpleNamespace:
    return SimpleNamespace(from_status=src, to_status=dst, created_at=dt.datetime(2026, 9, day, 9, 0, tzinfo=dt.UTC))


def _course(status: str, events: list) -> list[tuple[str, str, int | None]]:
    rows = services.need_course(SimpleNamespace(status=status), events)
    return [(row["status"], row["state"], row["date"].day if row["date"] else None) for row in rows]


def test_a_draft_stands_on_its_first_station_and_the_rest_are_ahead():
    assert _course(S.DRAFT, [_ev("", S.DRAFT, 1)]) == [
        (S.DRAFT, "current", None),
        (S.SUBMITTED, "todo", None),
        (S.UNDER_REVIEW, "todo", None),
        (S.IN_PROGRESS, "todo", None),
        (S.CLOSED, "todo", None),
    ]


def test_the_stations_passed_carry_the_date_of_their_first_entry_and_only_the_record_speaks():
    events = [_ev("", S.DRAFT, 1), _ev(S.DRAFT, S.SUBMITTED, 2), _ev(S.SUBMITTED, S.UNDER_REVIEW, 3)]
    events += [_ev(S.UNDER_REVIEW, S.SUBMITTED, 4), _ev(S.SUBMITTED, S.UNDER_REVIEW, 5)]
    events += [_ev(S.UNDER_REVIEW, S.IN_PROGRESS, 6)]
    assert _course(S.IN_PROGRESS, events) == [
        (S.DRAFT, "done", 1),
        (S.SUBMITTED, "done", 2),
        (S.UNDER_REVIEW, "done", 3),
        (S.IN_PROGRESS, "current", None),
        (S.CLOSED, "todo", None),
    ]
    # a station the history never records entering keeps no date (never an invented one)
    assert _course(S.UNDER_REVIEW, [_ev(S.SUBMITTED, S.UNDER_REVIEW, 7)])[:2] == [
        (S.DRAFT, "done", None),
        (S.SUBMITTED, "done", None),
    ]


def test_a_pause_is_said_on_the_station_it_holds():
    held = [_ev(S.DRAFT, S.SUBMITTED, 2), _ev(S.SUBMITTED, S.UNDER_REVIEW, 3), _ev(S.UNDER_REVIEW, S.ON_HOLD, 4)]
    assert [state for _status, state, _day in _course(S.ON_HOLD, held)] == ["done", "done", "current", "todo", "todo"]
    # no record of where it paused: the one station a pause always follows (models.ALLOWED_TRANSITIONS)
    assert [state for _status, state, _day in _course(S.ON_HOLD, [])][:3] == ["done", "current", "todo"]


def test_a_closed_need_shows_the_way_it_went_and_a_withdrawn_one_no_course():
    straight = [_ev(S.DRAFT, S.SUBMITTED, 2), _ev(S.SUBMITTED, S.UNDER_REVIEW, 3), _ev(S.UNDER_REVIEW, S.CLOSED, 4)]
    assert [status for status, _state, _day in _course(S.CLOSED, straight)] == [
        S.DRAFT,
        S.SUBMITTED,
        S.UNDER_REVIEW,
        S.CLOSED,
    ], "never taken in charge: no «Pris en charge» station"
    assert _course(S.CLOSED, straight)[-1][1] == "current"
    taken = [*straight[:2], _ev(S.UNDER_REVIEW, S.IN_PROGRESS, 4), _ev(S.IN_PROGRESS, S.CLOSED, 5)]
    assert len(_course(S.CLOSED, taken)) == 5
    assert _course(S.WITHDRAWN, straight) == []


def test_the_need_page_draws_its_course_from_the_record(client, company_factory, need_factory):
    profile, user = company_factory("gamma")
    need = need_factory(profile)
    for src, dst in ((S.DRAFT, S.SUBMITTED), (S.SUBMITTED, S.UNDER_REVIEW), (S.UNDER_REVIEW, S.ON_HOLD)):
        NeedEvent.objects.create(need=need, from_status=src, to_status=dst)
    CompanyNeed.objects.filter(pk=need.pk).update(status=S.ON_HOLD)
    client.force_login(user)
    html = client.get(reverse("companies:need_detail", args=[need.reference])).content.decode()
    soup = BeautifulSoup(html, "html.parser")
    section = soup.select_one("section.need-course-sec[aria-labelledby='need-course-title']")
    assert section and section.select_one("h2#need-course-title")
    stops = section.select("ol.need-course > li.need-course__stop")
    assert [stop["data-state"] for stop in stops] == ["done", "done", "current", "todo", "todo"]
    current = stops[2]
    assert current.get("aria-current") == "step" and [s for s in stops if s.get("aria-current")] == [current]
    assert current.select_one(".chip"), "the pause is said on the station it holds, as a chip"
    assert all(stop.select_one(".visually-hidden") for stop in stops if stop["data-state"] != "current")
    assert all(stop.select_one("time[datetime]") for stop in stops[1:2]), "the stations passed carry their date"
    for stop in stops:
        mark = stop.select_one(".need-course__mark[aria-hidden='true'] svg use")
        assert mark and mark["href"].split("#icon-")[1], "each station's mark is its state's chip mark"
        assert not any(ch.isdigit() for ch in stop.select_one(".need-course__mark").get_text()), "no numeral"
    assert "css/dist/companies/course.css" in html


def test_a_withdrawn_need_has_no_course(client, company_factory, need_factory):
    profile, user = company_factory("delta")
    need = need_factory(profile)
    CompanyNeed.objects.filter(pk=need.pk).update(status=S.WITHDRAWN)
    client.force_login(user)
    html = client.get(reverse("companies:need_detail", args=[need.reference])).content.decode()
    assert "need-course" not in html.split("<main", 1)[1].split("</main>", 1)[0].replace("course.css", "")
