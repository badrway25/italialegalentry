"""Models, querysets and object-level policies of the reserved area (deny by default)."""

from __future__ import annotations

import datetime as dt

import pytest
from django.contrib.auth.models import AnonymousUser
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction

from accounts import roles
from accounts.permissions import can
from cms.models import PublicationStatus
from core import clock
from portal.models import Deadline, DeadlineStatus, Message, NoticeAudience, PortalNotice
from portal.policies import audiences_of

pytestmark = pytest.mark.django_db


# ---- Message --------------------------------------------------------------------------------
def test_message_uses_uuid_pk_and_str_never_leaks_the_recipient(make_message, alice):
    message = make_message(alice, subject="Votre dossier")
    assert len(str(message.pk)) == 36
    assert alice.email not in str(message)
    # Review hardening: __str__ is copied into audit rows, logs and the admin LogEntry, which outlive
    # the erasure of the message — it carries the neutral reference, never the subject.
    assert "Votre dossier" not in str(message)
    assert message.reference in str(message)
    assert message.reference == str(message.pk)[:8].upper()


def test_deadline_str_is_neutral(make_deadline, alice):
    deadline = make_deadline(alice, title="Rendez-vous au consulat")
    assert "consulat" not in str(deadline) and alice.email not in str(deadline)
    assert str(deadline.pk) in str(deadline)


def test_message_inbox_is_scoped_to_the_recipient(make_message, alice, bob):
    mine = make_message(alice, subject="Pour Alice")
    make_message(bob, subject="Pour Bob")
    assert list(Message.objects.inbox(alice)) == [mine]
    assert Message.objects.inbox(AnonymousUser()).count() == 0


def test_message_visible_from_hides_scheduled_messages(make_message, alice):
    now = clock.now()
    shown = make_message(alice, subject="Visible", visible_from=now - dt.timedelta(hours=1))
    hidden = make_message(alice, subject="Programmé", visible_from=now + dt.timedelta(days=2))
    assert list(Message.objects.inbox(alice)) == [shown]
    assert hidden.is_visible() is False
    assert hidden.is_visible(at=now + dt.timedelta(days=3)) is True


def test_message_read_state_is_consistent_at_database_level(make_message, alice):
    message = make_message(alice)
    message.is_read = True  # read_at missing
    with pytest.raises(IntegrityError), transaction.atomic():
        message.save()


def test_message_related_object_pair_is_validated(alice, staff_user, make_deadline):
    deadline = make_deadline(alice)
    message = Message(recipient=alice, sender=staff_user, subject="S", body="B", object_id=str(deadline.pk))
    with pytest.raises(ValidationError):
        message.full_clean()
    message.content_type = ContentType.objects.get_for_model(Deadline)
    message.full_clean()
    message.save()
    assert message.related_object == deadline


# ---- Deadline -------------------------------------------------------------------------------
def test_deadline_overdue_and_soon(make_deadline, alice):
    late = make_deadline(alice, days=-1)
    soon = make_deadline(alice, days=3)
    far = make_deadline(alice, days=40)
    done = make_deadline(alice, days=-5, status=DeadlineStatus.DONE)
    assert late.is_overdue() and not late.is_soon()
    assert soon.is_soon() and not soon.is_overdue()
    assert not far.is_soon() and not far.is_overdue()
    assert not done.is_overdue()
    assert set(Deadline.objects.for_owner(alice).overdue()) == {late}
    assert set(Deadline.objects.for_owner(alice).upcoming()) == {soon, far}


def test_deadline_queryset_is_scoped_to_the_owner(make_deadline, alice, bob):
    mine = make_deadline(alice)
    make_deadline(bob)
    assert list(Deadline.objects.for_owner(alice)) == [mine]
    assert Deadline.objects.for_owner(AnonymousUser()).count() == 0


# ---- PortalNotice ---------------------------------------------------------------------------
def _notice(audience, status=PublicationStatus.PUBLISHED, **fields):
    return PortalNotice.objects.create(
        audience=audience, heading_fr=f"Avis {audience}", body_fr="Texte", status=status, **fields
    )


def test_notice_audiences_follow_account_type_and_roles(alice, company_a, user_factory):
    company_user, _org = company_a
    assert audiences_of(alice) == {"all", "person"}
    assert audiences_of(company_user) == {"all", "company"}
    mixed = user_factory("mixed@example.test", role=roles.UNIVERSITY)  # account_type stays « person »
    assert audiences_of(mixed) == {"all", "person", "university"}


def test_notice_queryset_live_and_audience(alice):
    everyone = _notice(NoticeAudience.ALL)
    persons = _notice(NoticeAudience.PERSON)
    _notice(NoticeAudience.COMPANY)
    _notice(NoticeAudience.ALL, status=PublicationStatus.DRAFT)
    _notice(NoticeAudience.ALL, unpublish_at=clock.now() - dt.timedelta(days=1))
    rows = set(PortalNotice.objects.live().for_audiences(audiences_of(alice)))
    assert rows == {everyone, persons}


# ---- Policies -------------------------------------------------------------------------------
def test_message_policy_recipient_staff_and_strangers(make_message, alice, bob, staff_user, superuser, user_factory):
    message = make_message(alice)
    assert can(alice, "view", message) and can(alice, "mark_read", message)
    assert not can(alice, "change", message) and not can(alice, "delete", message)
    assert not can(bob, "view", message) and not can(bob, "mark_read", message)
    assert not can(AnonymousUser(), "view", message)
    assert can(staff_user, "view", message)
    assert not can(staff_user, "mark_read", message), "staff must never flip somebody else's read state"
    assert not can(staff_user, "delete", message)
    administrator = user_factory("administrator@example.test", role=roles.ADMINISTRATOR, is_staff=True)
    assert can(administrator, "delete", message) and can(administrator, "change", message)
    assert can(superuser, "delete", message)
    bare_staff = user_factory("bare@example.test", is_staff=True)  # is_staff alone opens nothing
    assert not can(bare_staff, "view", message)


def test_message_policy_hides_scheduled_message_from_recipient(make_message, alice):
    message = make_message(alice, visible_from=clock.now() + dt.timedelta(days=1))
    assert not can(alice, "view", message)
    assert not can(alice, "mark_read", message)


def test_deadline_policy(make_deadline, alice, bob, staff_user):
    deadline = make_deadline(alice)
    assert can(alice, "view", deadline)
    assert not can(alice, "change", deadline)
    assert not can(bob, "view", deadline)
    assert can(staff_user, "view", deadline) and can(staff_user, "change", deadline)
    assert not can(staff_user, "delete", deadline)


def test_notice_policy(alice, company_a, staff_user):
    company_user, _org = company_a
    for_companies = _notice(NoticeAudience.COMPANY)
    draft = _notice(NoticeAudience.ALL, status=PublicationStatus.DRAFT)
    assert can(company_user, "view", for_companies)
    assert not can(alice, "view", for_companies)
    assert not can(alice, "view", draft)
    assert can(staff_user, "view", draft) and can(staff_user, "change", draft)


def test_inactive_account_is_denied_everything(make_message, alice):
    message = make_message(alice)
    alice.is_active = False
    assert not can(alice, "view", message)
