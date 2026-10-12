"""
Deadline monitoring: what is due, who is told, and why they are told only once.

The case file already knows its dates — ``ChecklistItem.due_date``, entered by the team from a
written source, never computed by the platform. What was missing is the part that happens while
nobody is looking at the screen: a requirement that becomes due next week, and one that quietly
passed its date last night.

Two rules shape everything here.

**Once per item per state change.** A warning that arrives every night stops being a warning: people
learn the shape of it, filter it, and then miss the one that mattered. So each notification carries
a ``dedupe_key`` built from the event, the item and the date it is about
(``checklist.overdue:412:2026-10-02``), and the unique constraint on ``Notification`` refuses the
second one. Two consequences fall out of that, both wanted: running the scan twice in an evening
sends nothing the second time, and a date CHANGED by the team re-arms the warning, because the key
changes with the date. An item that goes from "due soon" to "overdue" is a different state, hence a
different event, hence one more notification — which is exactly the moment worth interrupting
somebody for.

**The person is told, and told who is responsible.** The recipient is the person whose case it is,
because that is the account guaranteed to exist and the one that reads the checklist. But a
requirement is frequently somebody else's to satisfy — the competent authority, the training body,
the employer — and a notification that says "your deadline is overdue" when the delay is the
administration's teaches people to feel at fault for waiting. Every body therefore names the
responsible actor, from the case file's own field.
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field

from cases.models import ACTIVE_STATUSES, CaseFile, ChecklistItem, ChecklistStatus
from cases.services import open_items
from core import clock
from notifications import events
from notifications.models import Notification
from notifications.services import notify_quietly

#: How far ahead "bientôt" reaches. Same horizon as ``portal.Deadline.SOON_DAYS``: two different
#: definitions of "soon" in one reserved area is one too many.
DUE_SOON_DAYS = 7

#: The statuses the case file itself calls open — derived from the model rather than copied, so this
#: scan cannot drift away from ``ChecklistItem.is_open`` and ``cases.services.open_items`` the day
#: somebody adds a sixth status.
OPEN_STATUSES: tuple[str, ...] = tuple(
    status for status in ChecklistStatus.values if ChecklistItem(status=status).is_open
)


# ---------------------------------------------------------------------------------------------
# "What is due" — the reading side
# ---------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class DueItem:
    """One open requirement with a date, ready to be printed. No model leaks into the template."""

    item_id: int
    case_reference: str
    case_uuid: str
    requirement: str
    detail: str
    due_date: dt.date
    days_left: int
    responsible_actor: str
    responsible_display: str

    @property
    def is_overdue(self) -> bool:
        return self.days_left < 0

    @property
    def urgency(self) -> str:
        """The vocabulary of ``cases.services.NextAction``, so one screen speaks one language."""
        if self.days_left < 0:
            return "overdue"
        return "soon" if self.days_left <= DUE_SOON_DAYS else "normal"

    @property
    def is_for_someone_else(self) -> bool:
        return self.responsible_actor not in ("", "person")


@dataclass(frozen=True)
class DueSummary:
    """What one account has to watch, in three buckets that are ordered by what they cost to miss."""

    overdue: list[DueItem] = field(default_factory=list)
    due_soon: list[DueItem] = field(default_factory=list)
    later: list[DueItem] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.overdue) + len(self.due_soon) + len(self.later)

    @property
    def needs_attention(self) -> int:
        return len(self.overdue) + len(self.due_soon)

    @property
    def nearest(self) -> DueItem | None:
        return (self.overdue or self.due_soon or self.later or [None])[0]


def _due_item(item: ChecklistItem, today: dt.date) -> DueItem:
    return DueItem(
        item_id=item.pk,
        case_reference=item.case.reference,
        case_uuid=str(item.case.uuid),
        requirement=item.requirement,
        detail=item.detail,
        due_date=item.due_date,
        days_left=(item.due_date - today).days,
        responsible_actor=item.responsible_actor,
        responsible_display=item.get_responsible_actor_display(),
    )


def what_is_due(user, *, today: dt.date | None = None, horizon_days: int = DUE_SOON_DAYS) -> DueSummary:
    """
    Everything dated and still open on the cases this account may read.

    Built on ``CaseFile.objects.readable_by`` and ``cases.services.open_items`` rather than on a
    query of its own, for two reasons that are really one. The authorisation lives in that queryset
    — a professional sees the cases their live mandate covers and nothing else — and re-querying
    here would mean re-deciding it here, which is how a listing ends up one refactor behind the
    rule it is supposed to apply. The definition of "open" comes from the same place, so this view
    and the case file always agree on what is outstanding.
    """
    today = today or clock.today()
    summary = DueSummary()
    cases = CaseFile.objects.readable_by(user).active().order_by("-created_at")
    for case in cases:
        for item in open_items(case):
            if not item.due_date:
                continue
            due = _due_item(item, today)
            if due.days_left < 0:
                summary.overdue.append(due)
            elif due.days_left <= horizon_days:
                summary.due_soon.append(due)
            else:
                summary.later.append(due)
    summary.overdue.sort(key=lambda row: row.due_date)
    summary.due_soon.sort(key=lambda row: row.due_date)
    summary.later.sort(key=lambda row: row.due_date)
    return summary


# ---------------------------------------------------------------------------------------------
# The scan — the writing side
# ---------------------------------------------------------------------------------------------
@dataclass
class ScanReport:
    """What a run did. ``already_sent`` is the number that proves the scan is idempotent."""

    examined: int = 0
    overdue: int = 0
    due_soon: int = 0
    already_sent: int = 0
    skipped: int = 0

    @property
    def sent(self) -> int:
        return self.overdue + self.due_soon

    def as_dict(self) -> dict[str, int]:
        return {
            "examined": self.examined,
            "overdue": self.overdue,
            "due_soon": self.due_soon,
            "already_sent": self.already_sent,
            "skipped": self.skipped,
        }


def dedupe_key_for(event_key: str, item: ChecklistItem) -> str:
    """
    The key that makes the scan idempotent: the event, the item, and the DATE it is about.

    The date belongs in the key. Without it, a deadline the team corrects — moved a fortnight later
    because the prefecture wrote — would never be announced again, and the person would keep the
    first date in mind. With it, the correction is a new state and says so.
    """
    return f"{event_key}:{item.pk}:{item.due_date.isoformat()}"


def candidates(*, today: dt.date, horizon_days: int = DUE_SOON_DAYS):
    """
    Open, dated requirements of ACTIVE cases, nearest date first.

    Closed and suspended cases are excluded deliberately. A suspended case is one everyone has
    agreed to stop working on, usually for a reason the person already knows; continuing to chase
    its dates would be the platform arguing with a decision the team took.
    """
    return (
        ChecklistItem.objects.filter(
            status__in=OPEN_STATUSES,
            due_date__isnull=False,
            due_date__lte=today + dt.timedelta(days=horizon_days),
            case__status__in=ACTIVE_STATUSES,
        )
        .select_related("case", "case__person")
        .order_by("due_date", "case_id", "order", "id")
    )


def scan(*, today: dt.date | None = None, horizon_days: int = DUE_SOON_DAYS, limit: int | None = None) -> ScanReport:
    """
    Notify every requirement that became due soon or overdue — each one exactly once.

    Idempotence is not attempted here with a "last run" timestamp, which would be wrong in both
    directions: a run that fails halfway would re-announce everything it already sent, and a run
    that starts a minute late would skip a day. It is a property of the DATA instead — the key of
    the state being announced — so running this twice, or five times, or after a crash, sends what
    has not been sent and nothing else.

    The scan never raises on one bad row: ``notify_quietly`` isolates each notification in its own
    savepoint, so a single unrenderable item cannot cost the other nine hundred their warning.
    """
    today = today or clock.today()
    report = ScanReport()
    queryset = candidates(today=today, horizon_days=horizon_days)
    if limit:
        queryset = queryset[:limit]

    planned: list[tuple[ChecklistItem, str, str, bool]] = []
    for item in queryset:
        overdue = item.due_date < today
        event_key = events.CHECKLIST_OVERDUE if overdue else events.CHECKLIST_DUE_SOON
        planned.append((item, event_key, dedupe_key_for(event_key, item), overdue))
    report.examined = len(planned)

    # What has already been announced, in ONE query rather than one per row. ``notify`` would refuse
    # the duplicates on its own — the constraint is what guarantees it — but a scan of a few thousand
    # requirements should not pay a round trip each to be told nothing has changed, and the report
    # can then say honestly how many were already sent.
    already = set(
        Notification.objects.filter(dedupe_key__in=[key for _item, _event, key, _overdue in planned]).values_list(
            "dedupe_key", flat=True
        )
    )

    for item, event_key, key, overdue in planned:
        if key in already:
            report.already_sent += 1
            continue
        notification = notify_quietly(
            item.case.person,
            event_key,
            context={
                "case_reference": item.case.reference,
                "requirement": item.requirement,
                "due_date": f"{item.due_date:%d/%m/%Y}",
                "days": abs((item.due_date - today).days),
                "responsible": item.get_responsible_actor_display(),
            },
            related=item,
            dedupe_key=key,
        )
        if notification is None:
            report.skipped += 1
        elif overdue:
            report.overdue += 1
        else:
            report.due_soon += 1
    return report
