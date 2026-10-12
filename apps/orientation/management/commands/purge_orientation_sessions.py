from django.core.management.base import BaseCommand

from orientation.constants import ANONYMOUS_SESSION_TTL_DAYS
from orientation.services import purge_expired_sessions


class Command(BaseCommand):
    help = (
        "Retention purge: anonymous orientation sessions inactive for more than N days (default 30) are "
        "deleted; completed ones are anonymised (statistics kept, answers and tokens removed)."
    )

    def add_arguments(self, parser):
        parser.add_argument("--days", type=int, default=ANONYMOUS_SESSION_TTL_DAYS)
        parser.add_argument("--dry-run", action="store_true", help="Report only, change nothing.")

    def handle(self, *args, **options):
        report = purge_expired_sessions(days=options["days"], dry_run=options["dry_run"])
        prefix = "[dry-run] " if report.dry_run else ""
        self.stdout.write(f"{prefix}deleted={report.deleted} anonymised={report.anonymised}")
