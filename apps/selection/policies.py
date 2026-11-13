"""
Object-level policies of authorised selection (deny by default — ``accounts.permissions``).

The querysets are the primary defence: ``SelectionProcess.objects.readable_by`` and
``IdentityDisclosure.objects.readable_by`` keep unauthorised rows out of lists, counts and
lookups, so a user never learns that an object exists. These policies are the second defence, for a
single object already in hand.

AuthorizedActor      live operator: view · administrator: view, change, delete
ActorOperator        the account itself and live operators of the actor: view · administrator: all
SelectionMandate     live operator of its actor, member of the company: view · administrator: all
SelectionProcess     live operator: view, change · the person of the case: view ·
                     member of the company that expressed the need: view · administrator: all
SelectionEvidence    follows its process; only a live operator changes one
IdentityDisclosure   the person: view + decide · live operator: view + request ·
                     member of the recipient organisation: view, and read_identity ONLY while the
                     disclosure is in force
SelectionStageEvent  follows its process, read-only for everyone — a movement already recorded is
                     evidence, and evidence is not edited
IdentityAccess       the person and the administrator: view. Not even the organisation that made the
                     access may edit its own trace.

``role:staff`` gets nothing here, exactly as in ``cases.policies``: supervision happens in the
back-office where every access is role-checked and audited. A lapsed authorisation likewise gets
nothing — ``services.is_operator`` checks ``ActorOperator.is_live``, which checks the actor's own
validity window, never the mere existence of the row.
"""

from __future__ import annotations

from accounts import roles
from accounts.permissions import policy
from selection.models import (
    ActorOperator,
    AuthorizedActor,
    IdentityAccess,
    IdentityDisclosure,
    SelectionEvidence,
    SelectionMandate,
    SelectionProcess,
    SelectionStageEvent,
)
from selection.services import is_operator

MANAGE_ROLES = (roles.ADMINISTRATOR,)


def _member_of(user, organisation) -> bool:
    return bool(organisation) and organisation.memberships.filter(user=user).exists()


@policy(AuthorizedActor)
def actor_policy(user, action: str, obj: AuthorizedActor) -> bool:
    if action == "view" and is_operator(user, obj):
        return True
    if action in {"view", "add", "change", "delete"}:
        return roles.has_role(user, *MANAGE_ROLES)
    return False


@policy(ActorOperator)
def operator_policy(user, action: str, obj: ActorOperator) -> bool:
    if action == "view" and (obj.user_id == user.id or is_operator(user, obj.actor)):
        return True
    if action in {"view", "add", "change", "delete"}:
        return roles.has_role(user, *MANAGE_ROLES)
    return False


@policy(SelectionMandate)
def mandate_policy(user, action: str, obj: SelectionMandate) -> bool:
    if action == "view" and (is_operator(user, obj.actor) or _member_of(user, obj.company)):
        return True
    if action in {"view", "add", "change", "delete"}:
        return roles.has_role(user, *MANAGE_ROLES)
    return False


@policy(SelectionProcess)
def process_policy(user, action: str, obj: SelectionProcess) -> bool:
    if is_operator(user, obj.actor):
        if action == "view":
            return True
        if action == "change":
            # A lapsed mandate reads but no longer acts: the authorisation is what carries the act.
            return obj.mandate.is_live and not obj.is_closed
        return False
    # The person always sees the process opened on their own case file, and the company always sees
    # the process attached to its own need. Neither of them can act on it.
    if action == "view" and (obj.case.person_id == user.id or _member_of(user, obj.mandate.company)):
        return True
    if action in {"view", "change", "delete"}:
        return roles.has_role(user, *MANAGE_ROLES)
    return False


@policy(SelectionEvidence)
def evidence_policy(user, action: str, obj: SelectionEvidence) -> bool:
    process = obj.process
    if is_operator(user, process.actor):
        if action == "view":
            return True
        if action == "change":
            return process.mandate.is_live and not process.is_closed
        return False
    if action == "view" and (process.case.person_id == user.id or _member_of(user, process.mandate.company)):
        return True
    if action in {"view", "change", "delete"}:
        return roles.has_role(user, *MANAGE_ROLES)
    return False


@policy(IdentityDisclosure)
def disclosure_policy(user, action: str, obj: IdentityDisclosure) -> bool:
    process = obj.process
    is_subject = process.case.person_id == user.id
    if is_subject:
        if action in {"view", "decide"}:
            return True
        # The subject may always read what was disclosed about them, while it is in force.
        if action == "read_identity":
            return obj.is_active()
        return False
    if is_operator(user, process.actor):
        if action == "view":
            return True
        if action == "request":
            return process.mandate.is_live and not process.is_closed
        # The actor asks and records; it never reads the identity on the company's behalf.
        return False
    if _member_of(user, obj.recipient_organisation):
        if action == "view":
            return True
        if action == "read_identity":
            # The one rule CR-04 exists for: no consent in force, no identity. Not a dimmed field,
            # not a masked string — nothing.
            return obj.is_active()
        return False
    if action == "view":
        return roles.has_role(user, *MANAGE_ROLES)
    return False


@policy(SelectionStageEvent)
def stage_event_policy(user, action: str, obj: SelectionStageEvent) -> bool:
    if action != "view":
        # A recorded movement is evidence. Nobody edits one, not even an administrator: a correction
        # is a new movement, so the history stays honest.
        return False
    return process_policy(user, "view", obj.process)


@policy(IdentityAccess)
def identity_access_policy(user, action: str, obj: IdentityAccess) -> bool:
    if action != "view":
        return False
    if obj.disclosure.process.case.person_id == user.id:
        return True
    return roles.has_role(user, *MANAGE_ROLES)
