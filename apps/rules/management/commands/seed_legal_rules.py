"""Create the initial legal ruleset as candidates. Idempotent: running it twice adds nothing."""

from __future__ import annotations

from django.core.management.base import BaseCommand

from rules import seeds


class Command(BaseCommand):
    help = "Seeds the legal sources and rules of the versioned rule engine. Nothing is put in force."

    def handle(self, *args, **options):
        counts = seeds.seed()
        self.stdout.write(
            self.style.SUCCESS(
                "fonti +{sources}  bozze +{drafted}  candidate ereditate +{legacy_candidates}".format(**counts)
            )
        )
        self.stdout.write(
            "Nessuna regola è in vigore. Il seed scrive candidate: una regola vincola qualcuno solo\n"
            "dopo LEGACY_CANDIDATE/DRAFT → SOURCE_VERIFIED → LEGAL_REVIEW → APPROVED → ACTIVE,\n"
            "percorso che esige una fonte verificata con data e nome, e un approvatore diverso\n"
            "dall'autore.\n"
            "\n"
            "  manage.py rules_pending_review          lo stato di ogni regola e che cosa le manca\n"
            "  manage.py rules_activate_demonstration  mette in vigore in locale, con un approvatore\n"
            "                                          dichiaratamente fittizio (solo dove i dati\n"
            "                                          dimostrativi sono ammessi)"
        )
