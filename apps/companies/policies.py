"""
Object-level policies of the company workspace (deny by default — ``accounts.permissions``).

The querysets (``CompanyProfileQuerySet.readable_by`` / ``CompanyNeedQuerySet.readable_by``) are the
primary defence: they keep another company's rows out of lists, counts and pagination, so a company
never learns that another company's need exists. These policies are the second defence, for a single
object already in hand.

CompanyProfile   member of the organisation: view
                 responsible member (Membership role « owner »): change
                 administrator: view, change, delete
CompanyNeed      member: view; responsible member: change / submit / withdraw while the state allows
                 live assignee (the actor answerable for it): view
                 administrator: everything, plus the project-side transitions
NeedSkill        follows its need
NeedAssignment   follows its need for « view » — a company must always see WHO is answerable.
                 Created and revoked by administrators only: an assignment a company could write
                 itself would be a self-issued authorisation.
NeedEvent        follows its need, read-only for everyone. A history that can be edited is not one.

Project STAFF deliberately gets nothing here. Supervision happens in the back-office, where each
access is role-checked and audited; a platform-side list of every company's needs is not supervision,
it is a standing disclosure. Same reasoning as ``cases.policies``.
"""

from __future__ import annotations

from accounts import roles
from accounts.models import MembershipRole
from accounts.permissions import policy
from companies.models import (
    CompanyNeed,
    CompanyProfile,
    NeedAssignment,
    NeedEvent,
    NeedSkill,
)

BACKOFFICE_MANAGE_ROLES = (roles.ADMINISTRATOR,)


def is_member(user, organisation_id) -> bool:
    if not organisation_id or not getattr(user, "is_authenticated", False):
        return False
    return user.memberships.filter(organisation_id=organisation_id).exists()


def is_responsible(user, organisation_id) -> bool:
    """A « responsable » (Membership role owner) may act for the company; a member may only read."""
    if not organisation_id or not getattr(user, "is_authenticated", False):
        return False
    return user.memberships.filter(organisation_id=organisation_id, role=MembershipRole.OWNER).exists()


def live_assignment(user, need: CompanyNeed) -> NeedAssignment | None:
    for row in need.assignments.all():
        if row.assignee_id == user.id and row.is_live:
            return row
    return None


@policy(CompanyProfile)
def company_profile_policy(user, action: str, obj: CompanyProfile) -> bool:
    organisation_id = obj.organisation_id
    if is_member(user, organisation_id):
        if action == "view":
            return True
        if action == "change":
            return is_responsible(user, organisation_id)
        return False
    if action in {"view", "change", "delete"}:
        return roles.has_role(user, *BACKOFFICE_MANAGE_ROLES)
    return False


@policy(CompanyNeed)
def company_need_policy(user, action: str, obj: CompanyNeed) -> bool:
    organisation_id = obj.company.organisation_id
    if is_member(user, organisation_id):
        if action == "view":
            return True
        if not is_responsible(user, organisation_id):
            return False
        if action == "change":
            return obj.is_editable_by_company
        if action == "submit":
            # Verification is one of the gates, and it is decided by accounts, never here.
            return _can_submit(obj)
        if action == "withdraw":
            return obj.is_withdrawable
        return False
    if live_assignment(user, obj) is not None and action == "view":
        return True
    if action in {"view", "change", "delete", "manage"}:
        return roles.has_role(user, *BACKOFFICE_MANAGE_ROLES)
    return False


def _can_submit(need: CompanyNeed) -> bool:
    from companies.models import NeedStatus

    return need.status == NeedStatus.DRAFT and need.company.is_verified and need.is_complete


@policy(NeedSkill)
def need_skill_policy(user, action: str, obj: NeedSkill) -> bool:
    need = obj.need
    organisation_id = need.company.organisation_id
    if is_member(user, organisation_id):
        if action == "view":
            return True
        if action in {"change", "delete", "add"}:
            return is_responsible(user, organisation_id) and need.is_editable_by_company
        return False
    if live_assignment(user, need) is not None and action == "view":
        return True
    if action in {"view", "change", "delete", "add"}:
        return roles.has_role(user, *BACKOFFICE_MANAGE_ROLES)
    return False


@policy(NeedAssignment)
def need_assignment_policy(user, action: str, obj: NeedAssignment) -> bool:
    if action == "view":
        # The company always sees who is answerable for its need: that is the whole point of naming
        # the responsible actor (ROLE_JOURNEYS §2, CR-03).
        if is_member(user, obj.need.company.organisation_id) or obj.assignee_id == user.id:
            return True
        return roles.has_role(user, *BACKOFFICE_MANAGE_ROLES)
    if action in {"add", "change", "delete"}:
        return roles.has_role(user, *BACKOFFICE_MANAGE_ROLES)
    return False


@policy(NeedEvent)
def need_event_policy(user, action: str, obj: NeedEvent) -> bool:
    if action != "view":
        return False
    need = obj.need
    if is_member(user, need.company.organisation_id) or live_assignment(user, need) is not None:
        return True
    return roles.has_role(user, *BACKOFFICE_MANAGE_ROLES)
