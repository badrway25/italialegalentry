"""
Demonstration data for the digital help desk — development and QA only.

The seed is a no-op unless ``core.seeds.demonstration_data_allowed()`` says synthetic records may be
created — true in development and QA, false in production and under the test settings. That is not
squeamishness: a help
desk request is a person's legal question, and a seed that manufactures one on a production database
has manufactured a personal-data record nobody consented to. Other apps seed published editorial
content, which is a different kind of object entirely.

Everything below is synthetic, obviously fictional, written for this file, and never copied from the
previous platform. The demonstration exists so the module can be SEEN working — a state machine
nobody has watched change state is a diagram.
"""

from __future__ import annotations

import datetime as dt
import os

from django.contrib.auth import get_user_model
from django.utils import timezone

from accounts import roles
from core.seeds import demonstration_data_allowed, register_seed

#: A recognisably fictional account. Used only where DEBUG is on, never created in production.
DEMO_PROFESSIONAL_EMAIL = "demo-professionnel@example.test"
DEMO_OPERATOR_EMAIL = "demo-operateur@example.test"
DEMO_PROFESSIONAL_ROLE_LABEL = "Avocat — droit de l’immigration"
#: The demonstration accounts share the local QA accounts' password, read from this environment
#: variable when an account is created (the local, untracked ``.env``, see ``.env.example``) and
#: never written in this repository. Without it the accounts are created with an unusable password:
#: the demonstration still exists, and a session can still be opened server-side, as the QA scripts
#: do; only signing in with a password needs the variable.
DEMO_ACCOUNTS_ENV_VARIABLE = "ILE_QA_PASSWORD"

DEMO_SUBJECT = "Durée de validité de mon attestation de langue"
DEMO_QUESTION = (
    "Mon attestation de langue italienne date de dix-huit mois. Je ne sais pas si elle est encore "
    "recevable pour la démarche qui me concerne, ni s’il faut la refaire avant de constituer mon "
    "dossier. Pouvez-vous me dire ce qui s’applique à ma situation ?"
)
DEMO_MANDATE = (
    "Examiner la recevabilité de l’attestation de langue au regard de la voie envisagée et indiquer "
    "la source applicable."
)
DEMO_RESPONSE = (
    "La durée de validité d’une attestation de langue dépend de la voie et de l’autorité qui la "
    "reçoit ; elle n’est pas fixée de manière uniforme. Dans votre cas, l’attestation reste "
    "recevable, mais elle devra être accompagnée du justificatif d’inscription mentionné dans votre "
    "checklist. Cette réponse est une information juridique ; elle n’engage aucune décision "
    "administrative et ne garantit aucun résultat."
)


@register_seed("helpdesk.demo", order=90)
def seed_helpdesk_demo():
    if not demonstration_data_allowed():
        return "helpdesk demo data skipped (synthetic data is not allowed in this environment)"

    from helpdesk import services
    from helpdesk.models import HelpdeskTicket, TicketStatus

    person = _demo_person()
    if person is None:
        return "helpdesk demo data skipped (no development person account to attach it to)"

    professional = _demo_professional()
    # The operator exists so the designation register can be exercised by the role that actually
    # holds it, rather than by an administrator standing in for one.
    _demo_account(DEMO_OPERATOR_EMAIL, roles.OPERATOR, "Compte de démonstration — opérateur")

    existing = HelpdeskTicket.objects.filter(person=person, subject=DEMO_SUBJECT).first()
    if existing is not None:
        return "helpdesk demo request already present"

    ticket = services.open_ticket(
        person,
        subject=DEMO_SUBJECT,
        question=DEMO_QUESTION,
        case=_open_case_of(person),
        language="fr",
        status=TicketStatus.PROFESSIONAL_REVIEW_REQUIRED,
    )
    services.assign(
        ticket,
        professional,
        mandate_note=DEMO_MANDATE,
        role_label=DEMO_PROFESSIONAL_ROLE_LABEL,
        valid_until=timezone.localdate() + dt.timedelta(days=90),
    )
    services.take_in_review(ticket, actor=professional)
    services.publish_response(ticket, DEMO_RESPONSE, actor=professional)
    return f"helpdesk demo request {ticket.reference} created, assigned and answered"


def _demo_person():
    """A development person account, if one exists. The seed never creates the person."""
    User = get_user_model()
    for email in ("qa-person@example.test", "person@example.test"):
        user = User.objects.filter(email=email).first()
        if user is not None:
            return user
    return User.objects.filter(groups__name=roles.PERSON, is_active=True).order_by("id").first()


def _demo_professional():
    """The fictional professional who answers the demonstration request."""
    return _demo_account(DEMO_PROFESSIONAL_EMAIL, roles.PROFESSIONAL, "Compte de démonstration — professionnel")


def _demo_account(email: str, role: str, label: str):
    """A recognisably fictional account with one role. Created only under DEBUG."""
    User = get_user_model()
    user, created = User.objects.get_or_create(email=email, defaults={"full_name": label, "preferred_language": "fr"})
    if created:
        password = os.environ.get(DEMO_ACCOUNTS_ENV_VARIABLE)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(update_fields=["password"])
    roles.assign_role(user, role)

    # E-mail verification is mandatory, so a demonstration account that cannot sign in would
    # demonstrate nothing. Development and QA only: this whole function is behind DEBUG.
    from allauth.account.models import EmailAddress

    EmailAddress.objects.update_or_create(user=user, email=user.email, defaults={"verified": True, "primary": True})
    return user


def _open_case_of(person):
    try:
        from cases.models import CaseFile
    except ImportError:  # pragma: no cover - the case file is always installed
        return None
    return CaseFile.objects.filter(person=person).active().order_by("-created_at").first()
