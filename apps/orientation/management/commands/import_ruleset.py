import json
from pathlib import Path

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError

from orientation import engine
from orientation.services import RulesetInvalid, activate_ruleset, import_ruleset, validate_ruleset


class Command(BaseCommand):
    help = "Import a ruleset JSON document as a new DRAFT version (optionally validate/activate)."

    def add_arguments(self, parser):
        parser.add_argument("path", help="JSON file produced by export_ruleset.")
        parser.add_argument(
            "--ruleset", dest="ruleset", type=int, help="Version number to assign (default: latest + 1)."
        )
        parser.add_argument("--activate", action="store_true", help="Validate and activate after import.")
        parser.add_argument("--notes", default="", help="Notes stored on the ruleset (origin, reviewer).")

    def handle(self, *args, **options):
        path = Path(options["path"])
        if not path.exists():
            raise CommandError(f"{path} not found")
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except ValueError as exc:
            raise CommandError(f"invalid JSON: {exc}") from exc
        try:
            spec = engine.spec_from_dict(data, version=options.get("ruleset") or 0)
        except (engine.InvalidConditions, KeyError, TypeError, ValueError) as exc:
            raise CommandError(f"invalid ruleset document: {exc}") from exc
        report = engine.validate(spec)
        for warn in report.warnings:
            self.stdout.write(self.style.WARNING(f"  WARNING {warn}"))
        if not report.ok:
            for err in report.errors:
                self.stdout.write(self.style.ERROR(f"  ERROR   {err}"))
            raise CommandError("document is not a valid ruleset; nothing imported")
        try:
            ruleset = import_ruleset(data, version=options.get("ruleset"), notes=options.get("notes", ""))
        except ValidationError as exc:
            raise CommandError("; ".join(exc.messages)) from exc
        self.stdout.write(self.style.SUCCESS(f"ruleset v{ruleset.version} imported as draft"))
        if options["activate"]:
            try:
                activate_ruleset(ruleset)
            except RulesetInvalid as exc:
                raise CommandError("; ".join(exc.report.errors)) from exc
            validate_ruleset(ruleset)
            self.stdout.write(self.style.SUCCESS(f"ruleset v{ruleset.version} activated"))
