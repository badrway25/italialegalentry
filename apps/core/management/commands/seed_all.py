from django.core.management.base import BaseCommand

from core.seeds import discover


class Command(BaseCommand):
    help = "Run every registered idempotent seed (locked content, flags, menus, initial records)."

    def add_arguments(self, parser):
        parser.add_argument("--only", help="Run only seeds whose name starts with this prefix.")

    def handle(self, *args, **options):
        prefix = options.get("only") or ""
        seeds = [s for s in discover() if s.name.startswith(prefix)]
        for seed in seeds:
            result = seed.func()
            self.stdout.write(f"seed {seed.name}: {result if result is not None else 'ok'}")
        self.stdout.write(self.style.SUCCESS(f"{len(seeds)} seed(s) executed"))
