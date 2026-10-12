"""
Reconcile the cached ``state`` column of every document requirement, and audit what changed.

A document expires on its own. The register does not wait for this command — it derives the state
on every render, so a piece that lapsed overnight reads EXPIRÉ the next morning whether or not a
job ran. This command exists so that the STORED value (which the dashboards, counts and queries
use) agrees with the derivation, and so the transition leaves a trace in the audit trail.

Run it daily. It is idempotent and writes only the rows whose state actually moved.
"""

from django.core.management.base import BaseCommand

from documents import services


class Command(BaseCommand):
    help = "Recompute the state of every document requirement (expiry, replacement, review) and audit changes."

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=None, help="Process at most N requirements.")

    def handle(self, *args, **options):
        changed = services.refresh_all_states(limit=options["limit"])
        if not changed:
            self.stdout.write("No requirement changed state.")
            return
        for transition, count in sorted(changed.items()):
            self.stdout.write(f"{transition}: {count}")
        self.stdout.write(self.style.SUCCESS(f"{sum(changed.values())} requirement(s) moved."))
