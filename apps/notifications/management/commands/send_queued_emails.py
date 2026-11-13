from django.core.management.base import BaseCommand

from notifications.services import send_pending


class Command(BaseCommand):
    help = "Deliver queued outbox e-mails through the configured EMAIL_BACKEND (console in development)."

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=100)

    def handle(self, *args, **options):
        sent, failed = send_pending(limit=options["limit"])
        self.stdout.write(self.style.SUCCESS(f"sent={sent} failed={failed}"))
