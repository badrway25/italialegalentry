"""
The registry's own invariants, tested without touching the database.

These are the properties that make the rest of the service safe to trust: a closed list of events,
a subject that cannot carry personal data, a body that cannot be half-rendered, and a category that
can actually be switched off. Each of them is the kind of thing that decays silently — a subject
gains a ``{name}`` in a hurry, an event is declared with a category that has no switch — so each is
asserted here rather than left to review.
"""

from __future__ import annotations

import pytest

from notifications import events
from notifications.models import NotificationPreference

EXPECTED_EVENTS = {
    events.CASE_OPENED,
    events.CASE_TRANSITIONED,
    events.CASE_ASSESSED,
    events.CHECKLIST_DUE_SOON,
    events.CHECKLIST_OVERDUE,
    events.DOCUMENT_REJECTED,
    events.DOCUMENT_EXPIRED,
    events.TEAM_MESSAGE,
    events.ASSIGNMENT_GRANTED,
    events.ASSIGNMENT_REVOKED,
}


def test_the_registry_covers_every_declared_event():
    assert set(events.EVENTS) == EXPECTED_EVENTS


def test_the_registry_is_closed():
    """An undeclared key is refused loudly. A silent no-op is a notification nobody ever receives."""
    with pytest.raises(events.UnknownEvent):
        events.get("case.something_someone_invented")


def test_no_subject_carries_a_placeholder():
    """
    The invariant behind "no personal data in a subject": a subject is a constant of its event.

    Nothing can be interpolated into it, so nothing about the person can leak into the mail headers
    that travel between servers, into a bounce report or onto a lock screen.
    """
    for event in events.EVENTS.values():
        assert "{" not in str(event.subject_fr), event.key
        assert "}" not in str(event.subject_fr), event.key


def test_every_event_renders_with_its_declared_fields():
    for event in events.EVENTS.values():
        context = {name: f"valeur-{name}" for name in event.fields}
        body = event.render_body(context)
        assert body.strip()
        assert "{" not in body, event.key
        for name in event.fields:
            assert f"valeur-{name}" in body, f"{event.key} declares {name} but never prints it"


def test_a_body_with_a_hole_is_refused():
    event = events.get(events.CHECKLIST_OVERDUE)
    with pytest.raises(events.MissingContext):
        event.render_body({"case_reference": "AB12CD34EF"})


def test_every_event_belongs_to_a_known_category():
    for event in events.EVENTS.values():
        assert event.category in events.CATEGORIES, event.key


def test_every_category_has_a_switch():
    """
    A category the preference model cannot switch off is a preference screen that lies.

    ``allows_email`` answers True for an unknown category on purpose — losing a notification is
    worse than sending one — so the gap would never show up as a failure anywhere else.
    """
    for category in events.CATEGORIES:
        field = NotificationPreference.field_for(category)
        assert any(f.name == field for f in NotificationPreference._meta.get_fields()), category


def test_the_email_decision_is_data_and_is_documented():
    """
    Which events warrant an e-mail is a field, and each answer carries its reasoning.

    The two events that do NOT send mail are the ones that happen while the person is looking at the
    screen that causes them. That is a judgement about attention, and it is recorded next to the
    decision so the next person to ask "why do we not mail this?" gets an answer instead of a guess.
    """
    silent = {key for key, event in events.EVENTS.items() if not event.email}
    assert silent == {events.CASE_OPENED, events.CASE_ASSESSED}
    for event in events.EVENTS.values():
        assert str(event.email_note).strip(), event.key
