"""
Attach a SYNTHETIC demonstration company, with its needs, to an existing account.

    .venv/Scripts/python manage.py companies_demo --account qa-company@example.test

Everything it writes is invented for the demonstration: the company does not exist, the contact is
not a real person, and nothing is copied from the previous platform — no real entreprise, no real
contact, and above all none of its age bands, which are the defect this vertical exists not to
repeat (previous-platform audit, part 2 §3, private register).

It is a command rather than a seed on purpose: ``seed_all`` runs on every deployment, and a
deployment must not invent an entreprise. It is idempotent — running it twice changes nothing.

It refuses to run wherever ``demonstration_data_allowed()`` is false, which is every environment
holding real people — the production settings pin the switch off. Until 12 October 2026 it had no
such guard: run under ``config.settings.prod`` it created the company and its needs and, through
``--verified`` (on by default), marked the account's verification APPROVED, while the deployment
runbook said it refused (DevOps verification, finding 1).
"""

from __future__ import annotations

import datetime as dt

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from accounts import roles
from accounts.models import (
    AccountType,
    AccountVerification,
    Membership,
    MembershipRole,
    Organisation,
    OrganisationKind,
    VerificationStatus,
)
from companies.models import (
    ActorRole,
    CompanyNeed,
    CompanyProfile,
    CompanySize,
    EngagementType,
    LanguageLevel,
    NeedEvent,
    NeedSkill,
    NeedStatus,
    Sector,
    SkillLevel,
    Territory,
)
from core.seeds import demonstration_data_allowed

DEMO_ORGANISATION = "Demo — Cantiere Adriatico S.r.l. (entreprise fictive)"
DEMO_REGISTRATION = "RM-000000-DEMO"

NEEDS: tuple[dict, ...] = (
    {
        "title": "Maintenance des lignes d’embouteillage",
        "territory": "veneto",
        "sector": "agroalimentaire",
        "work_place": "Rovigo",
        "professional_profile": "Technicien de maintenance industrielle",
        "duties": (
            "Entretien préventif et correctif des lignes d’embouteillage, diagnostic des arrêts, "
            "remplacement des organes d’usure, renseignement du carnet d’intervention."
        ),
        "motivation": (
            "Deux départs en retraite sur l’équipe de maintenance et une troisième ligne mise en service au printemps."
        ),
        "engagement_type": EngagementType.PERMANENT,
        "headcount": 3,
        "experience_years_min": 2,
        "experience_note": "Expérience en environnement de production alimentaire appréciée.",
        "language_code": "it",
        "language_level": LanguageLevel.A2,
        "language_note": "Consignes de sécurité et carnet d’intervention en italien.",
        "safety_training_required": True,
        "safety_training_note": "Formation générale et spécifique (D.lgs. 81/2008), à la charge de l’entreprise.",
        "training_needs": "Mise à niveau en pneumatique et lecture de schémas électriques avant la prise de poste.",
        "timing_note": "Prise de poste échelonnée sur le premier trimestre.",
        "mandatory": ["Mécanique industrielle", "Lecture de plan", "Habilitation électrique BT"],
        "preferred": ["Automatisme Siemens S7", "Soudure TIG"],
        "status": NeedStatus.IN_PROGRESS,
    },
    {
        "title": "Conduite d’engins de chantier",
        "territory": "veneto",
        "sector": "batiment",
        "work_place": "Province de Padoue",
        "professional_profile": "Conducteur d’engins de terrassement",
        "duties": "Conduite de pelle et de chargeuse sur chantiers de voirie, contrôle quotidien de l’engin.",
        "motivation": "Marché de voirie remporté auprès de la province, à exécuter sur dix-huit mois.",
        "engagement_type": EngagementType.FIXED_TERM,
        "headcount": 4,
        "experience_years_min": 1,
        "language_code": "it",
        "language_level": LanguageLevel.A2,
        "safety_training_required": True,
        "safety_training_note": "Attestation de conduite en sécurité exigée avant l’affectation.",
        "training_needs": "Module langue italienne de chantier et sécurité, 60 heures.",
        "mandatory": ["Conduite de pelle hydraulique", "Contrôle quotidien de l’engin"],
        "preferred": ["Conduite de chargeuse", "Lecture de plan de voirie"],
        "status": NeedStatus.UNDER_REVIEW,
    },
    {
        "title": "Préparation de commandes en entrepôt frigorifique",
        "territory": "emilia-romagna",
        "sector": "logistique",
        "work_place": "Modène",
        "professional_profile": "Préparateur de commandes",
        "duties": "Prélèvement, contrôle et palettisation des commandes en température dirigée.",
        "motivation": "Pic saisonnier de la campagne d’automne, sur l’entrepôt de Modène.",
        "engagement_type": EngagementType.SEASONAL,
        "headcount": 8,
        "experience_years_min": 0,
        "language_code": "it",
        "language_level": LanguageLevel.A1,
        "safety_training_required": True,
        "training_needs": "Gestes et postures, travail au froid, italien fonctionnel.",
        "mandatory": ["Travail en température dirigée"],
        "preferred": ["Conduite de transpalette accompagnant"],
        "status": NeedStatus.SUBMITTED,
    },
    {
        "title": "Soudure d’assemblage sur charpente métallique",
        "territory": "lombardia",
        "sector": "metallurgie",
        "work_place": "Brescia",
        "professional_profile": "Soudeur TIG/MIG",
        "duties": "Assemblage et soudure de sous-ensembles de charpente, contrôle visuel des cordons.",
        "motivation": "Ouverture d’un second poste de soudage sur l’atelier de Brescia.",
        "engagement_type": EngagementType.PERMANENT,
        "headcount": 2,
        "experience_years_min": 3,
        "language_code": "it",
        "language_level": LanguageLevel.A2,
        "safety_training_required": True,
        "training_needs": "Qualification de soudage à confirmer avant la prise de poste.",
        "mandatory": ["Soudure TIG", "Soudure MIG", "Lecture de plan de charpente"],
        "preferred": ["Contrôle visuel de cordon"],
        "status": NeedStatus.DRAFT,
    },
)


class Command(BaseCommand):
    help = "Attach a synthetic demonstration company and its needs to an existing account."

    def add_arguments(self, parser) -> None:
        parser.add_argument("--account", required=True, help="e-mail of the account to attach the company to")
        parser.add_argument(
            "--verified",
            action="store_true",
            default=True,
            help="mark the account verification APPROVED so transmission is possible (default)",
        )

    @transaction.atomic
    def handle(self, *args, **options) -> None:
        if not demonstration_data_allowed():
            raise CommandError(
                "This environment does not allow demonstration data (ILE_SEED_DEMONSTRATION_DATA).\n"
                "The command invents a company and its needs and approves the account's verification: where "
                "real people are, that is a false record. A real company is declared and verified through the "
                "platform, by a person who answers for it."
            )
        User = get_user_model()
        email = options["account"].strip().lower()
        user = User.objects.filter(email=email).first()
        if user is None:
            raise CommandError(f"no account {email}")

        organisation, _created = Organisation.objects.get_or_create(
            name=DEMO_ORGANISATION,
            defaults={"kind": OrganisationKind.COMPANY, "country": "IT", "city": "Rovigo", "created_by": user},
        )
        Membership.objects.get_or_create(user=user, organisation=organisation, defaults={"role": MembershipRole.OWNER})
        roles.assign_role(user, roles.COMPANY)

        profile, created_profile = CompanyProfile.objects.get_or_create(
            organisation=organisation,
            defaults={
                "legal_name": "Cantiere Adriatico S.r.l.",
                "trade_name": "Cantiere Adriatico",
                "registration_number": DEMO_REGISTRATION,
                "vat_number": "IT00000000000",
                "sector": Sector.objects.filter(code="batiment").first(),
                "size": CompanySize.MEDIUM,
                "year_founded": 1998,
                "contact_name": "Référent démonstration",
                "contact_function": "Responsable des ressources humaines",
                "contact_email": "referent@example.test",
                "contact_phone": "+39 0000 000000",
                "address_line": "Via della Dimostrazione 1",
                "postal_code": "45100",
                "city": "Rovigo",
                "province": "Rovigo",
                "country": "IT",
            },
        )

        if options["verified"]:
            AccountVerification.objects.update_or_create(
                user=user,
                defaults={
                    "declared_type": AccountType.COMPANY,
                    "status": VerificationStatus.APPROVED,
                    "evidence_note": "Environnement de démonstration — vérification simulée.",
                    "decided_at": timezone.now(),
                },
            )

        created_needs = 0
        for spec in NEEDS:
            if CompanyNeed.objects.filter(company=profile, title=spec["title"]).exists():
                continue
            need = CompanyNeed(
                company=profile,
                title=spec["title"],
                territory=Territory.objects.filter(code=spec["territory"]).first(),
                sector=Sector.objects.filter(code=spec["sector"]).first(),
                work_place=spec.get("work_place", ""),
                professional_profile=spec["professional_profile"],
                duties=spec["duties"],
                motivation=spec.get("motivation", ""),
                engagement_type=spec["engagement_type"],
                headcount=spec["headcount"],
                experience_years_min=spec["experience_years_min"],
                experience_note=spec.get("experience_note", ""),
                language_code=spec.get("language_code", ""),
                language_level=spec.get("language_level", LanguageLevel.NONE),
                language_note=spec.get("language_note", ""),
                safety_training_required=spec.get("safety_training_required", False),
                safety_training_note=spec.get("safety_training_note", ""),
                training_needs=spec.get("training_needs", ""),
                timing_note=spec.get("timing_note", ""),
                start_from=timezone.localdate() + dt.timedelta(days=60),
                status=spec["status"],
                submitted_at=None if spec["status"] == NeedStatus.DRAFT else timezone.now(),
            )
            need.full_clean(exclude=["reference"])
            need.save()
            NeedSkill.objects.bulk_create(
                [
                    NeedSkill(need=need, label=label, level=SkillLevel.MANDATORY, order=order)
                    for order, label in enumerate(spec["mandatory"])
                ]
                + [
                    NeedSkill(need=need, label=label, level=SkillLevel.PREFERRED, order=order)
                    for order, label in enumerate(spec["preferred"])
                ]
            )
            NeedEvent.objects.create(
                need=need,
                from_status="",
                to_status=NeedStatus.DRAFT,
                note="Besoin créé.",
                responsible_label=profile.legal_name,
            )
            if spec["status"] != NeedStatus.DRAFT:
                NeedEvent.objects.create(
                    need=need,
                    from_status=NeedStatus.DRAFT,
                    to_status=spec["status"],
                    note="Démonstration : état positionné par la commande companies_demo.",
                    responsible_label="Équipe du projet",
                )
            created_needs += 1

        # The need shown as « pris en charge » must carry a live, referenced authorisation: the
        # domain refuses that state without one, and the demonstration must not pretend otherwise.
        taken = CompanyNeed.objects.filter(company=profile, status=NeedStatus.IN_PROGRESS).first()
        if taken is not None and not taken.assignments.exists():
            actor_organisation, _made = Organisation.objects.get_or_create(
                name="Demo — Agenzia per il lavoro autorizzata (fictive)",
                defaults={"kind": OrganisationKind.OTHER, "country": "IT", "city": "Venezia"},
            )
            # A separate account, because the company is never its own authorised actor: the whole
            # point of CR-03 is that the two are different parties. Password unusable — this account
            # is a demonstration placeholder, not a way in.
            actor_user, actor_created = User.objects.get_or_create(
                email="demo-acteur-autorise@example.test",
                defaults={"full_name": "Acteur autorisé (démonstration)", "account_type": AccountType.PROFESSIONAL},
            )
            if actor_created:
                actor_user.set_unusable_password()
                actor_user.save(update_fields=["password"])
            roles.assign_role(actor_user, roles.AUTHORISED_ACTOR)
            Membership.objects.get_or_create(
                user=actor_user, organisation=actor_organisation, defaults={"role": MembershipRole.OWNER}
            )
            taken.assignments.create(
                assignee=actor_user,
                role=ActorRole.AUTHORISED_ACTOR,
                organisation=actor_organisation,
                authorisation_reference="Albo informatico — prot. DEMO/0000/2026",
                authorisation_jurisdiction="IT",
                authorisation_valid_until=timezone.localdate() + dt.timedelta(days=365),
                mandate_note="Démonstration : autorisation fictive.",
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"demonstration company {'created' if created_profile else 'already present'}; "
                f"{created_needs} need(s) created for {email}"
            )
        )
