from django.conf import settings
from django.core.management.base import BaseCommand

from documents import services


class Command(BaseCommand):
    help = "Run the configured antivirus hook (settings.DOCUMENT_SCANNER) on documents still pending analysis."

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=100)

    def handle(self, *args, **options):
        if not getattr(settings, "DOCUMENT_SCANNER", ""):
            self.stdout.write(self.style.WARNING("DOCUMENT_SCANNER is not configured: nothing scanned."))
            return
        counts = services.run_pending_scans(limit=options["limit"])
        self.stdout.write(", ".join(f"{status}={n}" for status, n in counts.items()))
