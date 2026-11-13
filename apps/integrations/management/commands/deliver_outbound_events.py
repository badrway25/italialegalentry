from django.core.management.base import BaseCommand

from integrations.services import deliver_pending
from integrations.transports import get_transport


class Command(BaseCommand):
    help = "Push queued outbound events through INTEGRATIONS_TRANSPORT (default: logging, no network)."

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=100)

    def handle(self, *args, **options):
        transport = get_transport()
        counters = deliver_pending(limit=options["limit"])
        summary = " ".join(f"{k}={v}" for k, v in counters.items())
        self.stdout.write(self.style.SUCCESS(f"transport={transport.name} {summary}"))
