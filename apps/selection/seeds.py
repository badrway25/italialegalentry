"""
Synthetic seed of authorised selection.

Everything here is INVENTED. No datum comes from the previous platform, none describes a real
person, a real company or a real authorisation, and the authorisation references are deliberately
marked ``SYNTH`` so that nobody can mistake one for a real entry in a public register.

The seed builds the whole chain once, so the module can be SEEN working:

    company need (synthetic) → authorised actor → mandate → process on a real case file

plus a second actor whose authorisation LAPSED yesterday, because "a lapsed authorisation grants
nothing" is the rule this module exists to enforce, and a rule you cannot see enforced is a rule
nobody trusts.
"""

from __future__ import annotations

import datetime as dt

from django.contrib.auth import get_user_model
from django.utils import timezone

from accounts import roles
from accounts.models import AccountType, Membership, MembershipRole, Organisation, OrganisationKind
from cases.models import CasePurpose, CaseStatus
from core.seeds import demonstration_data_allowed, register_seed

# A fixed password for SYNTHETIC demonstration accounts, created only where
# ``demonstration_data_allowed()`` is true. It never reaches an environment holding real accounts.
SEED_PASSWORD = "Seed-Only-Passw0rd-2026!"  # noqa: S105

#: Synthetic accounts. The domain is ``example.test``, reserved by RFC 6761 and never routable.
ACTOR_OPERATOR_EMAIL = "seed-actor@example.test"
LAPSED_OPERATOR_EMAIL = "seed-actor-lapsed@example.test"
COMPANY_EMAIL = "seed-company@example.test"
PERSON_EMAIL = "seed-person@example.test"


def _user(email: str, *, account_type: str, role: str, full_name: str = ""):
    User = get_user_model()
    user, created = User.objects.get_or_create(
        email=email,
        defaults={"account_type": account_type, "full_name": full_name, "is_active": True},
    )
    if created:
        user.set_password(SEED_PASSWORD)
        user.save(update_fields=["password"])
    # allauth refuses a sign-in until the address is confirmed, and a demonstration account has no
    # inbox to confirm from. The address is marked verified here rather than the requirement being
    # relaxed anywhere: the rule stays intact for real accounts.
    from allauth.account.models import EmailAddress

    EmailAddress.objects.update_or_create(user=user, email=user.email, defaults={"verified": True, "primary": True})
    roles.assign_role(user, role)
    return user


def _organisation(name: str, kind: str, city: str):
    org, _created = Organisation.objects.get_or_create(
        name=name, defaults={"kind": kind, "city": city, "country": "Italie"}
    )
    return org


@register_seed("selection.chain", order=240)
def seed_selection_chain() -> dict:
    """Idempotent: re-running it never duplicates the chain and never overwrites a decision."""
    if not demonstration_data_allowed():
        # This seed manufactures accounts, an organisation and a CASE FILE. Those are records about
        # people, indistinguishable from real ones once written, so they exist only where synthetic
        # data is explicitly allowed. `manage.py seed_all` on any other environment leaves nothing.
        return {"skipped": "demonstration data is not allowed in this environment"}
    from cases import services as case_services
    from selection import services
    from selection.models import AuthorizedActor, SelectionMandate, SelectionProcess

    today = timezone.localdate()
    counters = {"actors": 0, "mandates": 0, "processes": 0}

    # -- the organisations ----------------------------------------------------------------------
    agency = _organisation("Agenzia Mediterranea per il Lavoro (données de test)", OrganisationKind.COMPANY, "Rovigo")
    lapsed_agency = _organisation(
        "Studio Ponte Adriatico (données de test)", OrganisationKind.PROFESSIONAL_FIRM, "Padoue"
    )
    company = _organisation("Metalmeccanica Polesine S.r.l. (données de test)", OrganisationKind.COMPANY, "Rovigo")

    # -- the accounts ---------------------------------------------------------------------------
    operator = _user(
        ACTOR_OPERATOR_EMAIL,
        account_type=AccountType.PROFESSIONAL,
        role=roles.AUTHORISED_ACTOR,
        full_name="Responsable de processus (compte de test)",
    )
    lapsed_operator = _user(
        LAPSED_OPERATOR_EMAIL,
        account_type=AccountType.PROFESSIONAL,
        role=roles.AUTHORISED_ACTOR,
        full_name="Responsable de processus échu (compte de test)",
    )
    company_user = _user(
        COMPANY_EMAIL,
        account_type=AccountType.COMPANY,
        role=roles.COMPANY,
        full_name="Référent entreprise (compte de test)",
    )
    person = _user(
        PERSON_EMAIL,
        account_type=AccountType.PERSON,
        role=roles.PERSON,
        full_name="Personne de démonstration (compte de test)",
    )
    Membership.objects.get_or_create(user=company_user, organisation=company, defaults={"role": MembershipRole.OWNER})
    Membership.objects.get_or_create(user=operator, organisation=agency, defaults={"role": MembershipRole.OWNER})

    # -- the authorisations ----------------------------------------------------------------------
    actor = AuthorizedActor.objects.filter(organisation=agency).first()
    if actor is None:
        actor = services.register_actor(
            organisation=agency,
            actor_type="employment_agency",
            jurisdiction="IT-VEN",
            authorisation_reference="SYNTH-AUT-2026-0148 (donnée de test)",
            authorisation_register="Registre de test — aucun registre public réel",
            valid_from=today - dt.timedelta(days=200),
            valid_until=today + dt.timedelta(days=400),
            scope_note="Intermédiation et sélection pour le secteur métallurgique, Vénétie.",
        )
        counters["actors"] += 1

    lapsed = AuthorizedActor.objects.filter(organisation=lapsed_agency).first()
    if lapsed is None:
        # Registered with a validity window that has already closed: the seed writes the row
        # directly, because ``register_actor`` would rightly accept it and ``issue_mandate`` would
        # rightly refuse to build anything on it. That refusal is the point of this row.
        lapsed = AuthorizedActor(
            organisation=lapsed_agency,
            actor_type="authorised_professional",
            jurisdiction="IT",
            authorisation_reference="SYNTH-AUT-2024-0007 (donnée de test, échue)",
            authorisation_register="Registre de test — aucun registre public réel",
            valid_from=today - dt.timedelta(days=800),
            valid_until=today - dt.timedelta(days=1),
            scope_note="Autorisation échue : conservée pour montrer qu’elle n’ouvre plus rien.",
        )
        lapsed.full_clean(exclude=["uuid"])
        lapsed.save()
        counters["actors"] += 1

    services.add_operator(actor, operator, function_note="Responsable du processus")
    services.add_operator(lapsed, lapsed_operator, function_note="Responsable du processus (autorisation échue)")

    # -- the case file the process attaches to ----------------------------------------------------
    case = person.case_files.first()
    if case is None:
        case = case_services.open_case(person, purpose=CasePurpose.WORK, pathway_key="work.subordinate")
    if case.status == CaseStatus.DRAFT:
        case_services.transition(case, CaseStatus.ORIENTED)
    if case.status == CaseStatus.ORIENTED:
        case_services.transition(case, CaseStatus.TRAINING)

    # -- the mandate ------------------------------------------------------------------------------
    mandate = SelectionMandate.objects.filter(actor=actor, company=company).first()
    if mandate is None:
        mandate = services.issue_mandate(
            actor=actor,
            company=company,
            need_source="companies.CompanyNeed",
            need_id="",
            need_reference="BESOIN-TEST-014",
            need_profile="Soudeur qualifié procédé MIG/MAG",
            need_sector="Métallurgie",
            need_territory="Rovigo, Vénétie",
            need_headcount=3,
            need_competences=[
                {"label": "Soudure MIG/MAG", "level": "Autonome"},
                {"label": "Lecture de plans mécaniques", "level": "Autonome"},
                {"label": "Sécurité au travail — formation générale", "level": "Acquis"},
            ],
            need_language_requirement="Italien — niveau A2 visé en fin de parcours",
            need_timeframe="Besoin exprimé pour le premier trimestre 2027",
            need_snapshot={
                "note": "Instantané synthétique du besoin, figé à la délivrance du mandat.",
                "conditions": "Contrat à durée indéterminée, convention collective métallurgie.",
            },
            valid_until=today + dt.timedelta(days=180),
            scope_note="Mandat limité au besoin ci-dessus et à sa durée.",
        )
        counters["mandates"] += 1

    # -- the process --------------------------------------------------------------------------------
    if not SelectionProcess.objects.filter(mandate=mandate, case=case).exists():
        services.open_process(mandate=mandate, case=case, operator=operator)
        counters["processes"] += 1

    return counters
