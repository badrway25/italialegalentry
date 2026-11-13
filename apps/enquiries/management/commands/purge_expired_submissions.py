from django.conf import settings
from django.core.management.base import BaseCommand

from enquiries.services import purge_expired


class Command(BaseCommand):
    help = (
        "Delete public form submissions older than the retention period "
        "(settings.ILE['RETENTION_MONTHS_FORMS'] = 24 months from the last contact). Dry-run by default."
    )

    def add_arguments(self, parser):
        parser.add_argument("--apply", action="store_true", help="Actually delete (default: dry-run, count only).")
        parser.add_argument(
            "--months",
            type=int,
            default=None,
            help="Override the retention period in months (default: settings value from the legal texts).",
        )

    def handle(self, *args, **options):
        months = options["months"] or settings.ILE["RETENTION_MONTHS_FORMS"]
        dry_run = not options["apply"]
        counts = purge_expired(months=months, dry_run=dry_run)
        mode = "DRY-RUN" if dry_run else "APPLIED"
        for label, count in counts.items():
            self.stdout.write(f"{mode} {label}: {count} expired submission(s)")
        total = sum(counts.values())
        if dry_run:
            self.stdout.write(self.style.WARNING(f"{total} submission(s) would be deleted (use --apply)."))
        else:
            self.stdout.write(self.style.SUCCESS(f"{total} submission(s) deleted (retention {months} months)."))
