"""
Put the seeded ruleset in force **for a demonstration**, visibly and only where that is allowed.

The engine has to be seen working: a case file with no findings, no sources and no checklist proves
nothing to anybody evaluating this build. The previous answer was to seed eleven rules straight to
``ACTIVE`` with no approver, and it had two faults. The database accepted a rule in force that
nobody had approved, which is the exact defect the governance model exists to prevent; and the
demonstration was indistinguishable, in the data, from the real thing.

This command replaces that. It walks each rule through the real chain — the same
``services.transition`` an operator uses, with the same refusals — and stamps an approver label
that says, in words, that no jurist approved it. The label travels into the snapshot of every
assessment, so a result produced this way carries its own disclaimer.

    manage.py rules_activate_demonstration
    manage.py rules_activate_demonstration --undo

It refuses to run wherever ``demonstration_data_allowed()`` is false, which is every environment
holding real people.
"""

from __future__ import annotations

import datetime as dt

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from core.seeds import demonstration_data_allowed
from rules import services
from rules.models import DEMONSTRATION_APPROVAL_PREFIX, LegalRule, LegalSource, ReviewStatus

#: Two accounts, because the four-eyes rule is enforced and a demonstration must not be the thing
#: that makes an exception to it. Both are on a domain RFC 6761 reserves and never routes.
DEMO_AUTHOR_EMAIL = "demo-legal-editor@example.test"
DEMO_APPROVER_EMAIL = "demo-legal-approver@example.test"

#: Written into `approved_by_label`, which the snapshot of every assessment carries.
DEMO_APPROVER_LABEL = f"{DEMONSTRATION_APPROVAL_PREFIX} — nessun giurista ha approvato questa regola"

DEMO_CONSULTED_BY = f"{DEMONSTRATION_APPROVAL_PREFIX} — fonte non verificata alla fonte ufficiale"


class Command(BaseCommand):
    help = "Puts the seeded ruleset in force for a local demonstration, with a fictional approver."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--undo",
            action="store_true",
            help="Retire the demonstration rules and clear the fictional verification from the sources.",
        )

    def handle(self, *args, **options):
        if not demonstration_data_allowed():
            raise CommandError(
                "Questo ambiente non ammette dati dimostrativi (ILE_SEED_DEMONSTRATION_DATA).\n"
                "Mettere in vigore una regola qui significa affermare che un giurista l'ha "
                "approvata. Se è vero, va fatto dal back-office, da una persona che se ne assume "
                "la responsabilità."
            )
        if options["undo"]:
            return self._undo()
        return self._activate()

    # ------------------------------------------------------------------ activate
    @transaction.atomic
    def _activate(self) -> None:
        author, approver = self._accounts()
        today = timezone.localdate()

        marked = 0
        for source in LegalSource.objects.all():
            if source.is_verified:
                continue
            source.consulted_on = source.consulted_on or today
            source.consulted_by = DEMO_CONSULTED_BY
            source.authority = source.authority or DEMONSTRATION_APPROVAL_PREFIX
            source.save(update_fields=["consulted_on", "consulted_by", "authority", "updated_at"])
            marked += 1

        chain = [
            ReviewStatus.SOURCE_VERIFIED,
            ReviewStatus.LEGAL_REVIEW,
            ReviewStatus.APPROVED,
            ReviewStatus.ACTIVE,
        ]
        moved, refused = 0, []
        candidates = LegalRule.objects.filter(
            review_status__in=[ReviewStatus.LEGACY_CANDIDATE, ReviewStatus.DRAFT]
        ).order_by("pathway", "rule_id")

        for rule in candidates:
            if rule.created_by_id is None:
                rule.created_by = author
                rule.save(update_fields=["created_by", "updated_at"])
            try:
                for target in chain:
                    services.transition(
                        rule,
                        target,
                        actor=approver,
                        approver_label=DEMO_APPROVER_LABEL,
                    )
                moved += 1
            except Exception as exc:  # noqa: BLE001 — the refusal text is the useful part
                refused.append(f"{rule.rule_id} v{rule.version}: {exc}")

        self.stdout.write(self.style.SUCCESS(f"{moved} regole in vigore (dimostrazione)"))
        self.stdout.write(f"{marked} fonti marcate come verificate per finta")
        for line in refused:
            self.stdout.write(self.style.ERROR(f"  rifiutata  {line}"))
        self.stdout.write(
            self.style.WARNING(
                "\nOgni regola porta l'approvatore «"
                + DEMO_APPROVER_LABEL
                + "»,\nche finisce nello snapshot di ogni pre-valutazione prodotta da qui."
            )
        )

    # ------------------------------------------------------------------ undo
    @transaction.atomic
    def _undo(self) -> None:
        """
        Take the demonstration out of force, and leave the ruleset able to demonstrate again.

        The first version of this only retired. That was right as far as it went — a rule leaves
        service by being retired, so the assessments that used it stay explainable — but RETIRED is
        a terminal state, so `--undo` was one-way: sixteen retired rules, nothing left to activate,
        and no way back short of rebuilding the database. A flag called `--undo` has to undo.

        So it retires AND opens a fresh version, which is what actually happens to a real rule that
        leaves service and is replaced. The version number climbs each cycle, and that is honest:
        the demonstration really did put a version in force and really did retire it.
        """
        author, approver = self._accounts()
        retired, reopened = 0, 0
        for rule in LegalRule.objects.filter(
            review_status=ReviewStatus.ACTIVE, approved_by_label=DEMO_APPROVER_LABEL
        ).order_by("pathway", "rule_id"):
            services.transition(rule, ReviewStatus.RETIRED, actor=approver)
            retired += 1
            services.new_version(rule, actor=author)
            reopened += 1

        cleared = LegalSource.objects.filter(consulted_by=DEMO_CONSULTED_BY).update(
            consulted_on=None, consulted_by="", updated_at=timezone.now()
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"{retired} regole ritirate, {reopened} riaperte in una nuova versione, "
                f"{cleared} fonti ripulite"
            )
        )
        self.stdout.write(
            "Ritirate, non riportate indietro: una regola esce di servizio venendo ritirata, così "
            "le pre-valutazioni che l'hanno usata restano spiegabili."
        )
        self.stdout.write(
            "La versione nuova riparte da dove la sua provenienza dice — candidata se ereditata, "
            "bozza se redatta dalla norma — e deve ripercorrere la catena, perché una versione "
            "nuova è testo nuovo."
        )

    # ------------------------------------------------------------------ accounts
    def _accounts(self):
        """
        Two distinct accounts, because `transition` refuses an author who approves their own rule.

        A demonstration that had to bypass that refusal would be demonstrating the wrong thing.
        """
        User = get_user_model()
        author, _ = User.objects.get_or_create(
            email=DEMO_AUTHOR_EMAIL,
            defaults={"full_name": "Redattore giuridico (dimostrazione)", "is_active": False},
        )
        approver, _ = User.objects.get_or_create(
            email=DEMO_APPROVER_EMAIL,
            defaults={"full_name": "Revisore giuridico (dimostrazione)", "is_active": False},
        )
        if author.pk == approver.pk:  # pragma: no cover - defensive
            raise CommandError("Author and approver resolved to the same account.")
        return author, approver


#: Kept next to the command so a reader of the code sees the shape of a real consultation date.
EXAMPLE_REAL_CONSULTATION = dt.date(2026, 9, 21)
