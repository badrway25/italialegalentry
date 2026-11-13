"""
Nightly deadline scan: warn about what is about to be due, and about what already is.

Run it once a day. Running it twice, or running it again after a crash halfway through, sends
nothing that was already sent — idempotence is a property of the notification keys, not of this
command remembering when it last ran (see ``notifications.deadlines``). That is deliberate: a job
that keeps its own "last run" marker re-announces everything after a failed run and skips a day
after a late one, and both mistakes are made at three in the morning where nobody sees them.

``--today`` exists for the same reason ``core.clock`` exists: to look at what the platform would say
on a given date without waiting for it, and to let the tests be about dates rather than about now.
"""

from __future__ import annotations

import datetime as dt

from django.core.management.base import BaseCommand, CommandError

from core import clock
from notifications import deadlines


class Command(BaseCommand):
    help = "Notify people of the checklist requirements that are due soon or overdue (once per state)."

    def add_arguments(self, parser) -> None:
        parser.add_argument("--today", help="ISO date to scan as (default: core.clock.today()).")
        parser.add_argument(
            "--days",
            type=int,
            default=deadlines.DUE_SOON_DAYS,
            help=f"How many days ahead counts as « bientôt » (default: {deadlines.DUE_SOON_DAYS}).",
        )
        parser.add_argument("--limit", type=int, default=None, help="Examine at most N requirements.")
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="List what would be sent and write nothing.",
        )

    def handle(self, *args, **options):
        today = self._parse_date(options["today"])
        horizon = options["days"]
        if horizon < 0:
            raise CommandError("--days cannot be negative.")

        if options["dry_run"]:
            return self._preview(today=today, horizon=horizon, limit=options["limit"])

        report = deadlines.scan(today=today, horizon_days=horizon, limit=options["limit"])
        for label, value in report.as_dict().items():
            self.stdout.write(f"{label}: {value}")
        if report.skipped:
            # Never silent: a skipped row is a person who was not warned, and the only place that
            # can be noticed is here.
            self.stderr.write(self.style.WARNING(f"{report.skipped} requirement(s) could not be notified."))
        self.stdout.write(self.style.SUCCESS(f"{report.sent} notification(s) sent."))

    def _preview(self, *, today, horizon: int, limit: int | None) -> None:
        """Same query, no writes. Prints identifiers only — never a requirement's text."""
        from notifications import events
        from notifications.models import Notification

        today = today or clock.today()
        rows = deadlines.candidates(today=today, horizon_days=horizon)
        if limit:
            rows = rows[:limit]
        pending = 0
        for item in rows:
            overdue = item.due_date < today
            key = deadlines.dedupe_key_for(events.CHECKLIST_OVERDUE if overdue else events.CHECKLIST_DUE_SOON, item)
            sent = Notification.objects.filter(dedupe_key=key).exists()
            if not sent:
                pending += 1
            state = "overdue" if overdue else "due_soon"
            self.stdout.write(f"  {'·' if sent else '→'} {state:9} {key}  case:{item.case_id}")
        self.stdout.write(self.style.SUCCESS(f"{pending} notification(s) would be sent."))

    @staticmethod
    def _parse_date(value: str | None):
        if not value:
            return None
        try:
            return dt.date.fromisoformat(value)
        except ValueError as exc:
            raise CommandError(f"--today expects an ISO date (YYYY-MM-DD), got {value!r}.") from exc
