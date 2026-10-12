import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from orientation.models import Ruleset, RulesetStatus
from orientation.services import export_ruleset


class Command(BaseCommand):
    help = "Export an orientation ruleset as JSON (stdout or --output file) for versioning/review."

    def add_arguments(self, parser):
        parser.add_argument("--ruleset", dest="ruleset", type=int, help="Ruleset version (default: the active one).")
        parser.add_argument("--output", help="Write to this file instead of stdout.")

    def handle(self, *args, **options):
        version = options.get("ruleset")
        ruleset = (
            Ruleset.objects.filter(version=version).first()
            if version is not None
            else Ruleset.objects.filter(status=RulesetStatus.ACTIVE).first()
        )
        if ruleset is None:
            raise CommandError("ruleset not found")
        payload = json.dumps(export_ruleset(ruleset), ensure_ascii=False, indent=2)
        if options.get("output"):
            Path(options["output"]).write_text(payload + "\n", encoding="utf-8")
            self.stdout.write(self.style.SUCCESS(f"ruleset v{ruleset.version} exported to {options['output']}"))
        else:
            self.stdout.write(payload)
