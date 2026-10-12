from django.core.management.base import BaseCommand

from documents import services


class Command(BaseCommand):
    help = (
        "Purge private document files whose retention_until has passed and files of soft-deleted rows. "
        "Dry-run by default; pass --apply to delete. Rows are kept as scrubbed tombstones (audit)."
    )

    def add_arguments(self, parser):
        parser.add_argument("--apply", action="store_true", help="Actually remove files (default: dry-run).")

    def handle(self, *args, **options):
        apply = bool(options["apply"])
        counts = services.purge_expired(apply=apply)
        mode = "purged" if apply else "would purge (dry-run)"
        self.stdout.write(f"{mode}: {counts['expired']} expired, {counts['soft_deleted']} soft-deleted")
        if not apply:
            self.stdout.write(self.style.WARNING("Nothing removed. Re-run with --apply to purge."))
