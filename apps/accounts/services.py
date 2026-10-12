"""
Account services — every rule about a person's own account lives here (views stay thin).

* profile update (data minimisation: only the fields the reserved area needs)
* data export (GDPR art. 15/20) — JSON of the person's OWN data, sections pluggable by other apps
* deletion request → immediate anonymisation (GDPR art. 17) — keeps the audit trail pseudonymised
* MFA policy helpers used by the back-office middleware / decorator

All functions operate on the user object passed in; callers pass ``request.user`` only.
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Any

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Q
from django.utils.functional import SimpleLazyObject, empty

from accounts import roles
from accounts.models import (
    VERIFIED_ACCOUNT_TYPES,
    AccountVerification,
    Membership,
    PersonProfile,
    User,
    VerificationStatus,
)
from accounts.signals import user_anonymised
from audit.models import AuditEvent
from audit.services import record
from consents.models import ConsentRecord, NewsletterSubscription
from consents.services import withdraw
from core import clock

log = logging.getLogger("ile.accounts")

ANONYMISED_DOMAIN = "anonymised.invalid"
PROFILE_FIELDS = ("full_name", "preferred_language")
PERSON_PROFILE_FIELDS = ("phone", "country_of_residence")

ExportSection = Callable[[User], Any]
_EXPORT_SECTIONS: dict[str, ExportSection] = {}


def concrete_user(user) -> User:
    """Unwrap ``request.user`` (a SimpleLazyObject) so audit rows carry the real model name."""
    if isinstance(user, SimpleLazyObject):
        if user._wrapped is empty:
            user._setup()
        return user._wrapped
    return user


# ---------------------------------------------------------------------------------------------
# Profile
# ---------------------------------------------------------------------------------------------
def get_or_create_profile(user: User) -> PersonProfile:
    profile, _created = PersonProfile.objects.get_or_create(user=user)
    return profile


def update_profile(request, user: User, data: dict[str, Any]) -> User:
    """Apply validated form data to ``user`` (and its PersonProfile). Only the caller's own user."""
    changed: list[str] = []
    for field in PROFILE_FIELDS:
        if field in data and getattr(user, field) != data[field]:
            setattr(user, field, data[field])
            changed.append(field)
    if changed:
        user.save(update_fields=[*changed, "updated_at"])
    profile = get_or_create_profile(user)
    profile_changed: list[str] = []
    for field in PERSON_PROFILE_FIELDS:
        if field in data and getattr(profile, field) != data[field]:
            setattr(profile, field, data[field])
            profile_changed.append(field)
    if profile_changed:
        profile.save(update_fields=[*profile_changed, "updated_at"])
    if changed or profile_changed:
        record(request, action="account.profile_updated", target=user, metadata={"fields": changed + profile_changed})
    return user


def memberships_of(user: User):
    return Membership.objects.filter(user=user).select_related("organisation").order_by("organisation__name")


# ---------------------------------------------------------------------------------------------
# Data export (art. 15 / 20)
# ---------------------------------------------------------------------------------------------
def register_export_section(name: str):
    """Other apps add their own section to the personal data export (documents, orientation, ...)."""

    def decorator(func: ExportSection) -> ExportSection:
        _EXPORT_SECTIONS[name] = func
        return func

    return decorator


def _consents_of(user: User):
    return (
        ConsentRecord.objects.filter(Q(user=user) | Q(email=user.email))
        .select_related("consent_text")
        .order_by("-given_at")
    )


def _exported_profile(profile: PersonProfile | None) -> dict[str, Any] | None:
    if profile is None:
        return None
    return {
        "phone": profile.phone,
        "country_of_residence": profile.country_of_residence,
        "date_of_birth": profile.date_of_birth,
        "nationality": profile.nationality,
        "education_level": profile.education_level,
        "years_of_experience": profile.years_of_experience,
        "languages": list(profile.languages or []),
        "has_job_offer": profile.has_job_offer,
        "has_qualification_recognition": profile.has_qualification_recognition,
        "completed_at": profile.completed_at,
    }


def export_user_data(user: User) -> dict[str, Any]:
    """Structured copy of the person's own data. Never includes other people's data."""
    from allauth.account.models import EmailAddress

    profile = PersonProfile.objects.filter(user=user).first()
    data: dict[str, Any] = {
        "exported_at": clock.now(),
        "format_version": 1,
        "project": settings.ILE["PROJECT_NAME"],
        "controller": settings.ILE["PROMOTER"],
        "contact": settings.ILE["PUBLIC_CONTACT_EMAIL"],
        "account": {
            "id": user.pk,
            "email": user.email,
            "full_name": user.full_name,
            "preferred_language": user.preferred_language,
            "account_type": user.account_type,
            "date_joined": user.date_joined,
            "last_login": user.last_login,
            "terms_accepted_at": user.terms_accepted_at,
            "roles": sorted(roles.roles_of(user)),
        },
        # The WHOLE profile, situation fields included. An export that omits what a person told us
        # about their circumstances is not the copy art. 15 requires, and the omission would be
        # invisible: nobody can miss from an export a field they did not know existed.
        "profile": _exported_profile(profile),
        "email_addresses": [
            {"email": e.email, "verified": e.verified, "primary": e.primary}
            for e in EmailAddress.objects.filter(user=user).order_by("email")
        ],
        "memberships": [
            {
                "organisation": m.organisation.name,
                "organisation_kind": m.organisation.kind,
                "role": m.role,
                "since": m.created_at,
            }
            for m in memberships_of(user)
        ],
        "consents": [
            {
                "purpose": c.purpose,
                "text_version": f"{c.purpose}@v{c.consent_text.version}",
                "locked_key": c.consent_text.locked_key,
                "language": c.language,
                "given_at": c.given_at,
                "withdrawn_at": c.withdrawn_at,
            }
            for c in _consents_of(user)
        ],
    }
    for name, func in _EXPORT_SECTIONS.items():
        data[name] = func(user)
    return data


# ---------------------------------------------------------------------------------------------
# Deletion / anonymisation (art. 17)
# ---------------------------------------------------------------------------------------------
def can_request_deletion(user: User) -> bool:
    """Superusers cannot self-delete through the public flow (an administrator must hand over first)."""
    return bool(user.is_authenticated and user.is_active and not user.is_superuser)


def anonymised_email_for(user_id: int) -> str:
    return f"anonymised-{user_id}@{ANONYMISED_DOMAIN}"


def anonymised_label_for(user_id: int) -> str:
    return f"user:{user_id} (anonymised)"


@transaction.atomic
def anonymise_user(user: User, *, request=None, actor=None, reason: str = "") -> User:
    """
    Scrub every personal field of ``user`` while keeping the row (foreign keys and the audit trail
    stay consistent). Consents are withdrawn, memberships/profile/e-mail addresses/MFA devices are
    removed, sessions become invalid (inactive user + unusable password). Audit rows are kept but
    their human labels are pseudonymised. Idempotent.
    """
    from allauth.account.models import EmailAddress
    from allauth.mfa.models import Authenticator

    user_id = user.pk
    original_email = user.email
    anon_email = anonymised_email_for(user_id)
    label = anonymised_label_for(user_id)

    for consent in _consents_of(user):
        if consent.withdrawn_at is None:
            withdraw(consent, note=f"account anonymised ({reason or 'request'})")
        if consent.email != anon_email:
            consent.email = anon_email
            consent.save(update_fields=["email", "updated_at"])
    for sub in NewsletterSubscription.objects.filter(email__iexact=original_email):
        if sub.unsubscribed_at is None:
            sub.unsubscribed_at = clock.now()
        sub.email = anon_email
        sub.save(update_fields=["unsubscribed_at", "email", "updated_at"])
        if sub.consent.withdrawn_at is None:
            withdraw(sub.consent, note="account anonymised")

    Membership.objects.filter(user=user).delete()
    PersonProfile.objects.filter(user=user).delete()
    EmailAddress.objects.filter(user=user).delete()
    Authenticator.objects.filter(user=user).delete()
    user.groups.clear()
    user.user_permissions.clear()

    user.email = anon_email
    user.full_name = ""
    user.is_active = False
    user.is_staff = False
    user.is_superuser = False
    user.last_login = None
    user.set_unusable_password()
    user.save()

    user_anonymised.send(sender=User, user=user, user_id=user_id)
    record(
        request,
        action="account.anonymised",
        target=user,
        actor=actor or user,
        metadata={"user_id": user_id, "reason": reason},
    )
    # Audit rows are kept (append-only trail) but their human labels are pseudonymised.
    AuditEvent.objects.filter(actor_id=user_id).update(actor_label=label)
    AuditEvent.objects.filter(target_type="User", target_id=str(user_id)).update(target_repr=label)
    log.info("account anonymised", extra={"user_id": user_id})
    return user


def request_deletion(request, user: User) -> User:
    """
    Self-service deletion: the caller has confirmed with their password. The account is deactivated
    and anonymised immediately (no task queue in this deployment — see report). Only ``request.user``.
    """
    if not can_request_deletion(user):
        raise PermissionDenied
    with transaction.atomic():
        record(request, action="account.deletion_requested", target=user, metadata={"user_id": user.pk})
        user.is_active = False
        user.save(update_fields=["is_active", "updated_at"])
        anonymise_user(user, request=request, actor=user, reason="self-service deletion request")
    return user


# ---------------------------------------------------------------------------------------------
# MFA policy for the back-office
# ---------------------------------------------------------------------------------------------
def has_active_totp(user) -> bool:
    from allauth.mfa.models import Authenticator

    if not getattr(user, "is_authenticated", False):
        return False
    return Authenticator.objects.filter(user=user, type=Authenticator.Type.TOTP).exists()


def backoffice_mfa_enforced() -> bool:
    return bool(getattr(settings, "BACKOFFICE_MFA_ENFORCED", False))


#: Roles that read OTHER PEOPLE'S files, and must therefore carry a second factor.
#:
#: Tying the requirement to ``is_staff`` was the wrong test: it describes who reaches the Django
#: admin, not who reaches personal data. A professional assigned to a case file reads a person's
#: legal situation, their documents and their history, and holds no staff flag at all — so a stolen
#: password was the whole of the protection standing between an attacker and that file (L-10).
MFA_REQUIRED_ROLES = (
    roles.PROFESSIONAL,
    roles.AUTHORISED_ACTOR,
    roles.OPERATOR,
    roles.LEGAL_EDITOR,
    roles.LEGAL_APPROVER,
    roles.CONTENT_EDITOR,
    roles.MODERATOR,
    roles.STAFF,
    roles.ADMINISTRATOR,
    roles.SUPERADMIN,
)


def reads_other_peoples_data(user) -> bool:
    """Whether this account's roles let it read data that is not its own."""
    return bool(user.is_staff or user.is_superuser or roles.has_role(user, *MFA_REQUIRED_ROLES))


def needs_backoffice_mfa(user) -> bool:
    """
    True when ``user`` must enrol a TOTP device before continuing.

    The name is historical: the rule is no longer about the back-office but about responsibility. An
    account that can open somebody else's case file is the account an attacker wants, whichever URL
    it uses to do it.
    """
    if not backoffice_mfa_enforced():
        return False
    if not getattr(user, "is_authenticated", False):
        return False
    if not reads_other_peoples_data(user):
        return False
    return not has_active_totp(user)


# ---------------------------------------------------------------------------------------------
# Account type verification
# ---------------------------------------------------------------------------------------------
def register_declared_account_type(user: User, account_type: str, *, request=None) -> AccountVerification | None:
    """
    Record what the visitor declared, and grant only what is safe to grant on a declaration.

    ``role:person`` is granted immediately: claiming to be a person claims nothing, and the role
    carries only access to one's own data. Every other type opens a verification request and grants
    nothing until a human approves it. Before this separation the signup form granted the declared
    role on the spot, which was harmless only for as long as those roles carried no permissions.
    """
    from accounts.forms import ROLE_BY_ACCOUNT_TYPE

    if account_type not in VERIFIED_ACCOUNT_TYPES:
        roles.assign_role(user, ROLE_BY_ACCOUNT_TYPE.get(account_type, roles.PERSON))
        return None

    verification, _created = AccountVerification.objects.get_or_create(
        user=user,
        defaults={"declared_type": account_type, "status": VerificationStatus.PENDING},
    )
    record(
        request,
        action="account.verification_requested",
        target=user,
        metadata={"declared_type": account_type},
    )
    return verification


@transaction.atomic
def approve_account_verification(
    verification: AccountVerification, *, decided_by: User, note: str = "", request=None
) -> AccountVerification:
    """Approve a declared account type and grant the matching role. Four eyes: not the account itself."""
    from accounts.forms import ROLE_BY_ACCOUNT_TYPE

    if decided_by.pk == verification.user_id:
        raise PermissionDenied("un account non verifica se stesso")
    verification.status = VerificationStatus.APPROVED
    verification.decided_by = decided_by
    verification.decided_at = clock.now()
    verification.decision_note = note
    verification.save(update_fields=["status", "decided_by", "decided_at", "decision_note", "updated_at"])

    role = ROLE_BY_ACCOUNT_TYPE.get(verification.declared_type)
    if role:
        roles.assign_role(verification.user, role)
    record(
        request,
        actor=decided_by,
        action="account.verification_approved",
        target=verification.user,
        metadata={"declared_type": verification.declared_type, "role": role or ""},
    )
    return verification


@transaction.atomic
def reject_account_verification(
    verification: AccountVerification, *, decided_by: User, note: str = "", request=None
) -> AccountVerification:
    from accounts.forms import ROLE_BY_ACCOUNT_TYPE

    verification.status = VerificationStatus.REJECTED
    verification.decided_by = decided_by
    verification.decided_at = clock.now()
    verification.decision_note = note
    verification.save(update_fields=["status", "decided_by", "decided_at", "decision_note", "updated_at"])

    # A rejection also withdraws the role, in case it was granted by an earlier approval.
    role = ROLE_BY_ACCOUNT_TYPE.get(verification.declared_type)
    if role:
        roles.revoke_role(verification.user, role)
    record(
        request,
        actor=decided_by,
        action="account.verification_rejected",
        target=verification.user,
        metadata={"declared_type": verification.declared_type},
    )
    return verification


#: The situation fields — what the person tells us about their circumstances, as distinct from their
#: identity and contact details. They are listed separately because they are read by something else
#: (the legal rule engine) and because changing one has a consequence: the orientation is recomputed.
SITUATION_FIELDS = (
    "date_of_birth",
    "nationality",
    "country_of_residence",
    "education_level",
    "years_of_experience",
    "languages",
    "has_job_offer",
    "has_qualification_recognition",
)


def update_situation(request, user: User, data: dict[str, Any]) -> tuple[object, list[str]]:
    """
    Record what a person has told us about their situation, and return what changed.

    Returning the changed field names is not bookkeeping: the caller re-runs the orientation only
    when something a rule could read has actually moved. A form submitted unchanged must not produce
    a second assessment, because an assessment is evidence and a record full of identical evidence
    is harder to read, not richer.

    The audit event records the FIELD NAMES only. That a person updated their nationality is an
    event an auditor may need; what they changed it to is personal data that belongs in the profile,
    which is access-controlled, and not in a log that is shipped elsewhere.
    """
    from django.utils import timezone

    profile = get_or_create_profile(user)
    changed: list[str] = []
    for field in SITUATION_FIELDS:
        if field not in data:
            continue
        if getattr(profile, field) != data[field]:
            setattr(profile, field, data[field])
            changed.append(field)
    if not changed:
        return profile, []

    profile.completed_at = timezone.now() if profile.is_complete else profile.completed_at
    profile.save(update_fields=[*changed, "completed_at", "updated_at"])
    record(request, action="account.situation_updated", target=user, metadata={"fields": changed})
    return profile, changed


# ---------------------------------------------------------------------------------------------
# Session revocation
# ---------------------------------------------------------------------------------------------
def revoke_sessions(user: User, *, request=None, reason: str = "") -> int:
    """
    End every open session of ``user`` and return how many were ended.

    Revoking a role or an assignment must take effect NOW, not at the next login. Without this, an
    account whose authorisation was withdrawn keeps the access it had until its cookie expires —
    which is exactly the window an urgent revocation exists to close (L-08, REQ-IAM-08).

    Sessions are matched by decoding each one and comparing the authenticated user id. The session
    store is not indexed by user, so there is nothing cheaper to do; the operation is rare, and the
    alternative — leaving an ended mandate usable — is not a saving worth making.
    """
    from django.contrib.auth import SESSION_KEY
    from django.contrib.sessions.models import Session

    from core import clock

    ended = 0
    target = str(user.pk)
    for session in Session.objects.filter(expire_date__gte=clock.now()).iterator():
        try:
            data = session.get_decoded()
        except Exception:  # noqa: BLE001 - a session we cannot decode is one we cannot attribute
            log.warning("undecodable session skipped during revocation", extra={"user_id": user.pk})
            continue
        if data.get(SESSION_KEY) == target:
            session.delete()
            ended += 1
    if ended:
        record(
            request,
            action="account.sessions_revoked",
            target=user,
            metadata={"user_id": user.pk, "sessions": ended, "reason": reason[:200]},
        )
    return ended
