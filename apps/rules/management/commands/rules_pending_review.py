"""
Governance report: for every rule, what it stands on and who stands behind it.

The directive asks for nine facts per rule — source, reference/URL, jurisdiction, valid_from,
valid_to, version, reviewer, approval status, and (added here, because the other eight are
meaningless without it) where the content came from. This prints all nine and says what each rule
is still missing.

    manage.py rules_pending_review            the whole matrix
    manage.py rules_pending_review --strict   exit 1 if anything is in force it should not be

Exit 1 is deliberately narrow. It fires on a rule that is APPROVED or ACTIVE without a named
approver, or ACTIVE on a source nobody has verified — states the database and the service now
refuse to create, so a non-zero exit here means something got in another way and wants looking at.
A long queue of candidates is not a failure: it is the queue doing its job.
"""

from __future__ import annotations

from django.core.management.base import BaseCommand

from rules.models import (
    APPROVED_STATUSES,
    LEGACY_PROVENANCES,
    LegalRule,
    LegalSource,
    ReviewStatus,
    is_demonstration_approval,
)


def _missing(rule) -> list[str]:
    """What stands between this rule and the next step of the chain."""
    gaps = []
    if not rule.sources.exists():
        gaps.append("nessuna fonte")
    else:
        unverified = rule.unverified_sources
        if unverified:
            gaps.append(f"{len(unverified)} fonti non verificate")
    if rule.review_status in APPROVED_STATUSES and not rule.approved_by_label.strip():
        gaps.append("nessun approvatore")
    if rule.review_status in APPROVED_STATUSES and rule.created_by_id and rule.approved_by_id == rule.created_by_id:
        gaps.append("autore = approvatore")
    return gaps


class Command(BaseCommand):
    help = "Per ogni regola: fonte, riferimento, giurisdizione, validità, versione, revisore, stato."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--strict",
            action="store_true",
            help="Esce con 1 se una regola è in vigore senza approvatore o su fonti non verificate.",
        )

    def handle(self, *args, **options):
        # Console encoding is handled once in manage.py: this report writes em dashes and arrows,
        # and a cp1252 console used to kill it on the third line.
        rules = list(LegalRule.objects.prefetch_related("sources").order_by("review_status", "pathway", "rule_id"))
        sources = list(LegalSource.objects.order_by("reference"))

        self.stdout.write(self.style.MIGRATE_HEADING("REGOLE"))
        if not rules:
            self.stdout.write("  nessuna")
        current = None
        for rule in rules:
            if rule.review_status != current:
                current = rule.review_status
                label = dict(ReviewStatus.choices)[current]
                count = sum(1 for r in rules if r.review_status == current)
                self.stdout.write(f"\n  {label.upper()}  ({count})")
            legacy = "EREDITATA" if rule.provenance in LEGACY_PROVENANCES else "da fonte"
            window = f"{rule.valid_from}→{rule.valid_to or '—'}"
            approver = rule.approved_by_label or "—"
            self.stdout.write(
                f"    {rule.rule_id:14s} v{rule.version}  {rule.jurisdiction:3s} {legacy:9s} "
                f"{window:24s} {rule.pathway:34s} {approver[:46]}"
            )
            gaps = _missing(rule)
            if gaps:
                self.stdout.write(self.style.WARNING(f"      manca: {', '.join(gaps)}"))

        self.stdout.write(self.style.MIGRATE_HEADING("\nFONTI"))
        for source in sources:
            # A demonstration verification satisfies `is_verified` on purpose, so that the chain
            # can be walked locally. It must not READ as a real one here: this report is where
            # somebody decides whether the ruleset is fit to bind people.
            pretend = is_demonstration_approval(source.consulted_by)
            mark = "?? " if pretend else ("OK " if source.is_verified else "!! ")
            style = self.style.WARNING if (pretend or not source.is_verified) else self.style.SUCCESS
            consulted = (
                f"{source.consulted_on} · {source.consulted_by[:34]}"
                if source.consulted_on
                else "mai consultata"
            )
            self.stdout.write(
                style(f"  {mark}{source.jurisdiction:3s} {source.reference[:46]:48s} {consulted}")
            )
            if not source.url:
                self.stdout.write("        nessun URL pubblico registrato")

        in_force = [r for r in rules if r.review_status == ReviewStatus.ACTIVE]
        unapproved = [r for r in rules if r.review_status in APPROVED_STATUSES and not r.approved_by_label.strip()]
        on_unverified = [r for r in in_force if r.unverified_sources]
        unverified_sources = [s for s in sources if not s.is_verified]

        self.stdout.write(self.style.MIGRATE_HEADING("\nRIASSUNTO"))
        self.stdout.write(f"  regole totali                       {len(rules)}")
        self.stdout.write(f"  in vigore                           {len(in_force)}")
        inherited = sum(1 for r in rules if r.provenance in LEGACY_PROVENANCES)
        self.stdout.write(f"  ereditate dalla piattaforma vecchia {inherited}")
        self.stdout.write(f"  fonti non verificate                {len(unverified_sources)} / {len(sources)}")

        problems = []
        if unapproved:
            problems.append(f"{len(unapproved)} regole approvate o in vigore senza approvatore")
        if on_unverified:
            problems.append(f"{len(on_unverified)} regole in vigore su fonti non verificate")

        if problems:
            self.stdout.write(self.style.ERROR("\n  " + "\n  ".join(problems)))
            if options["strict"]:
                raise SystemExit(1)
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    "\n  nessuna regola in vigore senza approvatore o su fonte non verificata"
                )
            )
