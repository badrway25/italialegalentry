from django.core.management.base import BaseCommand, CommandError

from orientation.models import Ruleset
from orientation.services import RulesetInvalid, activate_ruleset


class Command(BaseCommand):
    help = "Validate and activate a ruleset version; the previously active ruleset is retired."

    def add_arguments(self, parser):
        parser.add_argument("--ruleset", dest="ruleset", type=int, required=True)

    def handle(self, *args, **options):
        try:
            ruleset = Ruleset.objects.get(version=options["ruleset"])
        except Ruleset.DoesNotExist as exc:
            raise CommandError(f"ruleset v{options['ruleset']} does not exist") from exc
        try:
            activate_ruleset(ruleset)
        except RulesetInvalid as exc:
            for err in exc.report.errors:
                self.stdout.write(self.style.ERROR(f"  ERROR   {err}"))
            raise CommandError("ruleset is not valid; not activated") from exc
        self.stdout.write(self.style.SUCCESS(f"ruleset v{ruleset.version} is now active"))
