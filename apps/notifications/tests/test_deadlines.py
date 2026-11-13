"""
Deadline monitoring: the right warning, to the right person, exactly once.

The idempotence tests are the point of this file. A scan that re-sends last night's warning every
night is not a bug that shows up in production monitoring — it shows up six months later, as people
who no longer read anything the platform sends them.
"""

from __future__ import annotations

import datetime as dt

import pytest
from django.core import mail
from django.core.management import call_command

from cases import services as case_services
from cases.models import CasePurpose, CaseStatus, ChecklistStatus, ResponsibleActor
from notifications import deadlines, events
from notifications.models import Notification

pytestmark = pytest.mark.django_db


#: Events this file is NOT about. Opening a case file and moving it now notify the person — which is
#: correct and is tested in ``test_notify.py`` — but a deadline test that measured the WHOLE inbox
#: was using it as a proxy for what the scan produced, and the proxy stopped being true the day the
#: case services were wired up. The assertions below are about the scan, so they read the scan's own
#: events and ignore the rest.
NOT_FROM_THE_SCAN = frozenset(
    {
        events.CASE_OPENED,
        events.CASE_TRANSITIONED,
        events.CASE_ASSESSED,
        events.ASSIGNMENT_GRANTED,
        events.ASSIGNMENT_REVOKED,
    }
)


def keys_of(person) -> set[str]:
    """The deadline events this person has received. Everything else belongs to another test."""
    everything = set(Notification.objects.for_recipient(person).values_list("event", flat=True))
    return everything - NOT_FROM_THE_SCAN


def scan_notifications(person):
    """The notification ROWS the scan produced, for the tests that look inside one."""
    return Notification.objects.for_recipient(person).exclude(event__in=NOT_FROM_THE_SCAN)


# ---------------------------------------------------------------------------------------------
# What the scan finds
# ---------------------------------------------------------------------------------------------
def test_an_item_due_within_the_horizon_is_announced(person, item_factory, today):
    item_factory(due_date=today + dt.timedelta(days=3))

    report = deadlines.scan(today=today)

    assert report.examined == 1
    assert report.due_soon == 1
    assert report.overdue == 0
    assert keys_of(person) == {events.CHECKLIST_DUE_SOON}


def test_an_item_past_its_date_is_announced_as_overdue(person, item_factory, today):
    item_factory(due_date=today - dt.timedelta(days=2))

    report = deadlines.scan(today=today)

    assert report.overdue == 1
    assert keys_of(person) == {events.CHECKLIST_OVERDUE}


def test_an_item_beyond_the_horizon_is_left_alone(person, item_factory, today):
    item_factory(due_date=today + dt.timedelta(days=30))

    report = deadlines.scan(today=today)

    assert report.examined == 0
    assert scan_notifications(person).count() == 0


def test_an_item_without_a_date_is_never_chased(person, item_factory, today):
    item_factory(due_date=None)

    assert deadlines.scan(today=today).examined == 0


def test_a_completed_item_is_not_chased(person, item_factory, today):
    item_factory(due_date=today - dt.timedelta(days=5), status=ChecklistStatus.DONE)

    assert deadlines.scan(today=today).examined == 0


def test_the_scan_agrees_with_the_case_file_about_what_is_open(person, case, item_factory, today):
    """
    The definition of "open" is the case file's, not a copy of it.

    Five statuses exist and three of them are open; a scan that hard-coded the list would keep
    chasing a requirement the day somebody adds a sixth, or stop chasing one that still counts.
    """
    for status in ChecklistStatus.values:
        item_factory(due_date=today - dt.timedelta(days=1), status=status, requirement=f"Pièce {status}")

    scanned = {item.pk for item in deadlines.candidates(today=today)}
    open_now = {item.pk for item in case_services.open_items(case) if item.due_date}

    assert scanned == open_now


def test_a_closed_case_stops_producing_warnings(person, case, item_factory, today):
    item_factory(due_date=today - dt.timedelta(days=1))
    case_services.transition(case, CaseStatus.CLOSED)

    assert deadlines.scan(today=today).examined == 0


def test_a_suspended_case_stops_producing_warnings(person, case, item_factory, today):
    """Suspension is a decision the team took. Chasing its dates argues with it."""
    item_factory(due_date=today - dt.timedelta(days=1))
    case_services.transition(case, CaseStatus.SUSPENDED, reason="en attente d’un document officiel")

    assert deadlines.scan(today=today).examined == 0


# ---------------------------------------------------------------------------------------------
# Idempotence
# ---------------------------------------------------------------------------------------------
def test_running_the_scan_twice_notifies_once(person, item_factory, today):
    item_factory(due_date=today - dt.timedelta(days=2))

    first = deadlines.scan(today=today)
    second = deadlines.scan(today=today)

    assert first.sent == 1
    assert second.sent == 0
    assert second.already_sent == 1
    assert scan_notifications(person).count() == 1
    assert len(mail.outbox) == 1


def test_running_the_scan_five_times_notifies_once(person, item_factory, today):
    """A crash halfway through, a retried job, two workers: the answer must not depend on luck."""
    item_factory(due_date=today + dt.timedelta(days=1))

    for _run in range(5):
        deadlines.scan(today=today)

    assert scan_notifications(person).count() == 1


def test_a_second_day_does_not_repeat_the_same_warning(person, item_factory, today):
    """The date the scan runs is not part of the key: the STATE announced is."""
    item_factory(due_date=today + dt.timedelta(days=5))

    deadlines.scan(today=today)
    deadlines.scan(today=today + dt.timedelta(days=1))

    assert scan_notifications(person).count() == 1


def test_becoming_overdue_is_a_new_state_and_is_announced(person, item_factory, today):
    item_factory(due_date=today + dt.timedelta(days=1))

    deadlines.scan(today=today)
    deadlines.scan(today=today + dt.timedelta(days=5))

    assert keys_of(person) == {events.CHECKLIST_DUE_SOON, events.CHECKLIST_OVERDUE}
    assert scan_notifications(person).count() == 2


def test_a_corrected_date_re_arms_the_warning(person, item_factory, today):
    """
    A deadline moved by the team is new information, and the person is told again.

    Without the date in the key, the first warning would silence every later one and the person
    would keep the old date in mind — which is the failure this whole mechanism exists to avoid.
    """
    item = item_factory(due_date=today - dt.timedelta(days=1))
    deadlines.scan(today=today)

    item.due_date = today - dt.timedelta(days=4)
    item.save(update_fields=["due_date", "updated_at"])
    deadlines.scan(today=today)

    assert Notification.objects.of_event(events.CHECKLIST_OVERDUE).count() == 2


# ---------------------------------------------------------------------------------------------
# What the warning says
# ---------------------------------------------------------------------------------------------
def test_the_warning_names_who_is_responsible(person, item_factory, today):
    """
    "Votre échéance est dépassée" when the delay is the administration's teaches people to feel at
    fault for waiting. Every body names the responsible actor from the case file's own field.
    """
    item_factory(due_date=today - dt.timedelta(days=3), actor=ResponsibleActor.AUTHORITY)

    deadlines.scan(today=today)

    notification = scan_notifications(person).get()
    assert str(dict(ResponsibleActor.choices)[ResponsibleActor.AUTHORITY]) in notification.body
    assert "Responsable :" in notification.body


def test_the_warning_is_linked_to_the_item_it_is_about(person, item_factory, today):
    item = item_factory(due_date=today - dt.timedelta(days=1))

    deadlines.scan(today=today)

    assert scan_notifications(person).get().related_object == item


def test_the_subject_of_a_deadline_warning_names_nothing(person, item_factory, today):
    item_factory(due_date=today - dt.timedelta(days=1), requirement="Passeport de Madame Amina B.")

    deadlines.scan(today=today)

    notification = scan_notifications(person).get()
    assert "Amina" not in notification.subject
    assert "Passeport" not in notification.subject
    assert notification.subject == str(events.get(events.CHECKLIST_OVERDUE).subject_fr)


# ---------------------------------------------------------------------------------------------
# "What is due" for one person
# ---------------------------------------------------------------------------------------------
def test_what_is_due_sorts_into_three_buckets(person, item_factory, today):
    item_factory(due_date=today - dt.timedelta(days=2), requirement="Pièce en retard")
    item_factory(due_date=today + dt.timedelta(days=2), requirement="Pièce bientôt due")
    item_factory(due_date=today + dt.timedelta(days=60), requirement="Pièce lointaine")
    item_factory(due_date=None, requirement="Pièce sans date")

    summary = deadlines.what_is_due(person, today=today)

    assert [row.requirement for row in summary.overdue] == ["Pièce en retard"]
    assert [row.requirement for row in summary.due_soon] == ["Pièce bientôt due"]
    assert [row.requirement for row in summary.later] == ["Pièce lointaine"]
    assert summary.total == 3
    assert summary.needs_attention == 2
    assert summary.nearest.requirement == "Pièce en retard"


def test_what_is_due_shows_nobody_elses_case(other_person, item_factory, today):
    item_factory(due_date=today - dt.timedelta(days=1))

    assert deadlines.what_is_due(other_person, today=today).total == 0


def test_what_is_due_carries_the_urgency_vocabulary_of_the_case_file(person, item_factory, today):
    item_factory(due_date=today - dt.timedelta(days=1))
    item_factory(due_date=today + dt.timedelta(days=1), requirement="Pièce bientôt due")

    summary = deadlines.what_is_due(person, today=today)

    assert summary.overdue[0].urgency == "overdue"
    assert summary.due_soon[0].urgency == "soon"
    assert summary.overdue[0].is_overdue is True


def test_what_is_due_says_when_the_work_belongs_to_someone_else(person, item_factory, today):
    item_factory(due_date=today + dt.timedelta(days=1), actor=ResponsibleActor.TRAINING_BODY)

    row = deadlines.what_is_due(person, today=today).due_soon[0]

    assert row.is_for_someone_else is True
    assert row.responsible_display


def test_what_is_due_covers_every_open_case_of_the_person(person, item_factory, today):
    second_case = case_services.open_case(person, purpose=CasePurpose.STUDY)
    item_factory(due_date=today + dt.timedelta(days=1))
    item_factory(due_date=today + dt.timedelta(days=2), target=second_case, requirement="Inscription")

    assert len(deadlines.what_is_due(person, today=today).due_soon) == 2


# ---------------------------------------------------------------------------------------------
# The management command
# ---------------------------------------------------------------------------------------------
def test_the_command_scans_and_is_idempotent(person, item_factory, today, capsys):
    item_factory(due_date=today - dt.timedelta(days=1))

    call_command("notifications_scan_deadlines", "--today", today.isoformat())
    call_command("notifications_scan_deadlines", "--today", today.isoformat())

    assert scan_notifications(person).count() == 1
    assert "already_sent: 1" in capsys.readouterr().out


def test_the_command_dry_run_writes_nothing(person, item_factory, today, capsys):
    item_factory(due_date=today - dt.timedelta(days=1))

    call_command("notifications_scan_deadlines", "--today", today.isoformat(), "--dry-run")

    assert scan_notifications(person).count() == 0
    assert "would be sent" in capsys.readouterr().out


def test_the_command_refuses_a_junk_date(person):
    from django.core.management.base import CommandError

    with pytest.raises(CommandError):
        call_command("notifications_scan_deadlines", "--today", "hier")


def test_the_dry_run_prints_no_requirement_text(person, item_factory, today, capsys):
    """Console output is copied into terminals, tickets and screenshots. Identifiers only."""
    item_factory(due_date=today - dt.timedelta(days=1), requirement="Passeport de Madame Amina B.")

    call_command("notifications_scan_deadlines", "--today", today.isoformat(), "--dry-run")

    assert "Amina" not in capsys.readouterr().out
