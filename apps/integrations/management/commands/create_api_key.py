from django.core.management.base import BaseCommand, CommandError

from integrations.models import ApiScope, ExternalSystem
from integrations.services import create_api_key


class Command(BaseCommand):
    help = "Create an API key for the integration API. The key value is printed ONCE and never stored."

    def add_arguments(self, parser):
        parser.add_argument("--name", required=True, help="Human-readable label (e.g. 'CRM production').")
        parser.add_argument(
            "--scopes",
            default=",".join(ApiScope.values),
            help=f"Comma-separated scopes (default: all). Known: {', '.join(ApiScope.values)}",
        )
        parser.add_argument("--system", default="", help="Key of the ExternalSystem the key is bound to (optional).")

    def handle(self, *args, **options):
        scopes = [s.strip() for s in options["scopes"].split(",") if s.strip()]
        unknown = [s for s in scopes if s not in ApiScope.values]
        if unknown:
            raise CommandError(f"Unknown scope(s): {', '.join(unknown)}")
        system = None
        if options["system"]:
            system = ExternalSystem.objects.filter(key=options["system"]).first()
            if system is None:
                raise CommandError(f"Unknown external system '{options['system']}'.")
        key, raw = create_api_key(options["name"], scopes, system=system)
        self.stdout.write(self.style.SUCCESS(f"API key '{key.name}' created (prefix {key.prefix})."))
        self.stdout.write("Store it now — it will not be shown again:")
        self.stdout.write(raw)
