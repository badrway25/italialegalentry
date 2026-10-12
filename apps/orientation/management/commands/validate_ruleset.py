from django.core.management.base import BaseCommand, CommandError

from orientation.models import Ruleset, RulesetStatus
from orientation.services import validate_ruleset


class Command(BaseCommand):
    help = "Validate the integrity of an orientation ruleset (entry question, targets, conditions, termination)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--ruleset", dest="ruleset", type=int, help="Ruleset version (default: the active one, else the latest)."
        )
        parser.add_argument("--strict", action="store_true", help="Treat warnings as errors.")

    def handle(self, *args, **options):
        ruleset = _pick(options.get("ruleset"))
        report = validate_ruleset(ruleset)
        self.stdout.write(
            f"Ruleset v{ruleset.version} [{ruleset.status}]: {report.paths} paths, max depth {report.max_depth}"
        )
        for err in report.errors:
            self.stdout.write(self.style.ERROR(f"  ERROR   {err}"))
        for warn in report.warnings:
            self.stdout.write(self.style.WARNING(f"  WARNING {warn}"))
        if report.errors or (options["strict"] and report.warnings):
            raise CommandError("ruleset is not valid")
        self.stdout.write(self.style.SUCCESS("OK"))


def _pick(version):
    if version is not None:
        try:
            return Ruleset.objects.get(version=version)
        except Ruleset.DoesNotExist as exc:
            raise CommandError(f"ruleset v{version} does not exist") from exc
    ruleset = (
        Ruleset.objects.filter(status=RulesetStatus.ACTIVE).first() or Ruleset.objects.order_by("-version").first()
    )
    if ruleset is None:
        raise CommandError("no ruleset found")
    return ruleset
