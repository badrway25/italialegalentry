"""
Object-level policies of the Forum Permanent governance module (deny by default).

Two defences, in this order and never only the second:

1. The ``readable_by`` querysets in ``forum.governance``. They are the primary defence, because they
   keep unauthorised rows out of lists, counts and autocompletes — a caller never learns that a row
   exists, and the module answers 404 rather than 403 for anything it will not show.

2. These policies, for a single object already in hand (a form's ``instance``, a back-office screen,
   a service asked to act on an object somebody else fetched).

The two must agree. ``apps/forum/tests/test_governance_access.py`` runs every role through both and
fails on any disagreement — which is how the case file found the one it had, rather than deducing it.

    ForumEdition       read for a participant of the edition; changed by the secretariat
    ForumProfile       own profile: view and change. Another profile: VIEW ONLY, and what « view »
                       yields is ``governance_services.public_profile`` — organisation, category,
                       declared interests. There is nothing else on the model to yield.
    Commission         read with a live mandate or by the secretariat; changed by the secretariat
    CommissionMember   read inside the commission; granted and revoked by the secretariat
    Table              read inside the commission; moderated by its live referent
    ForumProposal      read per the queryset; changed by its proposer WHILE IT IS A DRAFT and never
                       after — a decided proposal is part of the record of the edition
    ForumProject       read inside the commission; changed by the referent or the secretariat
    ProjectMilestone   follows its project, plus: the responsible profile may advance its OWN
    MonitoringEntry    follows its project; recorded by the referent or the secretariat
    AnnualReport       read once published; assembled and published by the secretariat only

A mandate that has been revoked or has run out grants NOTHING here: every check goes through
``CommissionMember.is_live`` or ``CommissionMemberQuerySet.live()``, never through the mere
existence of the row. A lapsed mandate that kept reading a commission's proposals would defeat the
only thing a dated mandate is for.
"""

from __future__ import annotations

from accounts import roles
from accounts.permissions import policy
from forum.governance import (
    AnnualReport,
    Commission,
    CommissionMember,
    ForumEdition,
    ForumProfile,
    ForumProject,
    ForumProposal,
    ForumRole,
    MandateRole,
    MilestoneStatus,
    MonitoringEntry,
    ProjectMilestone,
    ProposalStatus,
    Table,
)

#: Who reads the whole module without a Forum profile. Deliberately just the administrator: the
#: Forum's own supervision role is ``ForumRole.SECRETARIAT``, which is bounded by an edition and can
#: be switched off on the profile. ``role:staff`` is absent for the reason the case file records.
BACKOFFICE_VIEW_ROLES = (roles.ADMINISTRATOR,)
BACKOFFICE_MANAGE_ROLES = (roles.ADMINISTRATOR,)

#: Mandate roles that MODERATE rather than merely take part.
MODERATING_MANDATE_ROLES = frozenset({MandateRole.REFERENT})


def _active_profiles(user, edition_id):
    return ForumProfile.objects.active().filter(user=user, edition_id=edition_id)


def is_secretariat(user, edition_id) -> bool:
    return _active_profiles(user, edition_id).filter(role=ForumRole.SECRETARIAT).exists()


def live_mandate(user, commission_id, edition_id) -> CommissionMember | None:
    """The caller's mandate on this commission, only while it is in force."""
    return (
        CommissionMember.objects.live()
        .filter(commission_id=commission_id, profile__in=_active_profiles(user, edition_id))
        .first()
    )


def _reads_commission(user, commission: Commission) -> bool:
    if is_secretariat(user, commission.edition_id):
        return True
    return live_mandate(user, commission.pk, commission.edition_id) is not None


def _moderates_commission(user, commission: Commission) -> bool:
    if is_secretariat(user, commission.edition_id):
        return True
    mandate = live_mandate(user, commission.pk, commission.edition_id)
    return mandate is not None and mandate.role in MODERATING_MANDATE_ROLES


@policy(ForumEdition)
def edition_policy(user, action: str, obj: ForumEdition) -> bool:
    if action == "view":
        if _active_profiles(user, obj.pk).exists():
            return True
        return roles.has_role(user, *BACKOFFICE_VIEW_ROLES)
    if action == "change":
        return is_secretariat(user, obj.pk) or roles.has_role(user, *BACKOFFICE_MANAGE_ROLES)
    return roles.has_role(user, *BACKOFFICE_MANAGE_ROLES) if action == "delete" else False


@policy(ForumProfile)
def profile_policy(user, action: str, obj: ForumProfile) -> bool:
    """
    A participant governs their own profile and may only LOOK at another's.

    There is no « change » on somebody else's profile for anyone but the secretariat, and no action
    at all that yields more than organisation, category and declared interests — because the model
    holds nothing more. FORUM_GOVERNANCE §5: the Forum is not a contact directory.
    """
    if obj.user_id == user.id:
        return action in {"view", "change"}
    if action == "view":
        if is_secretariat(user, obj.edition_id):
            return True
        # Another participant is visible only through a commission the caller sits on, live on
        # both sides. Sharing an edition is not enough: that would be the directory again.
        shared = CommissionMember.objects.live().filter(
            profile=obj,
            commission__in=CommissionMember.objects.live()
            .filter(profile__in=_active_profiles(user, obj.edition_id))
            .values("commission_id"),
        )
        return shared.exists() or roles.has_role(user, *BACKOFFICE_VIEW_ROLES)
    if action == "change":
        return is_secretariat(user, obj.edition_id) or roles.has_role(user, *BACKOFFICE_MANAGE_ROLES)
    return roles.has_role(user, *BACKOFFICE_MANAGE_ROLES) if action == "delete" else False


@policy(Commission)
def commission_policy(user, action: str, obj: Commission) -> bool:
    if action == "view":
        return _reads_commission(user, obj) or roles.has_role(user, *BACKOFFICE_VIEW_ROLES)
    if action == "change":
        return is_secretariat(user, obj.edition_id) or roles.has_role(user, *BACKOFFICE_MANAGE_ROLES)
    return roles.has_role(user, *BACKOFFICE_MANAGE_ROLES) if action in {"add", "delete"} else False


@policy(CommissionMember)
def mandate_policy(user, action: str, obj: CommissionMember) -> bool:
    edition_id = obj.commission.edition_id
    if action == "view":
        if obj.profile.user_id == user.id:
            return True
        return _reads_commission(user, obj.commission) or roles.has_role(user, *BACKOFFICE_VIEW_ROLES)
    if action in {"add", "change", "delete"}:
        # Seating and unseating a member is a secretariat act: a commission cannot enlarge itself.
        return is_secretariat(user, edition_id) or roles.has_role(user, *BACKOFFICE_MANAGE_ROLES)
    return False


@policy(Table)
def table_policy(user, action: str, obj: Table) -> bool:
    if action == "view":
        return _reads_commission(user, obj.commission) or roles.has_role(user, *BACKOFFICE_VIEW_ROLES)
    if action in {"add", "change"}:
        return _moderates_commission(user, obj.commission) or roles.has_role(user, *BACKOFFICE_MANAGE_ROLES)
    return roles.has_role(user, *BACKOFFICE_MANAGE_ROLES) if action == "delete" else False


@policy(ForumProposal)
def proposal_policy(user, action: str, obj: ForumProposal) -> bool:
    own = obj.proposer.user_id == user.id
    if action == "view":
        if own:
            return True
        if obj.status == ProposalStatus.DRAFT:
            # A draft belongs to the person writing it, and to nobody else — not even to the
            # referent of the table it will be tabled at.
            return roles.has_role(user, *BACKOFFICE_VIEW_ROLES)
        return _reads_commission(user, obj.commission) or roles.has_role(user, *BACKOFFICE_VIEW_ROLES)
    if action == "change":
        # Editing stops at the moment the proposal leaves the author's hands. Afterwards the text is
        # what the commission is examining, and it moves by transition, not by rewriting.
        return own and obj.is_editable
    if action == "decide":
        return _moderates_commission(user, obj.commission) or roles.has_role(user, *BACKOFFICE_MANAGE_ROLES)
    return roles.has_role(user, *BACKOFFICE_MANAGE_ROLES) if action == "delete" else False


@policy(ForumProject)
def project_policy(user, action: str, obj: ForumProject) -> bool:
    if action == "view":
        return _reads_commission(user, obj.commission) or roles.has_role(user, *BACKOFFICE_VIEW_ROLES)
    if action in {"add", "change"}:
        return _moderates_commission(user, obj.commission) or roles.has_role(user, *BACKOFFICE_MANAGE_ROLES)
    return roles.has_role(user, *BACKOFFICE_MANAGE_ROLES) if action == "delete" else False


@policy(ProjectMilestone)
def milestone_policy(user, action: str, obj: ProjectMilestone) -> bool:
    commission = obj.project.commission
    if action == "view":
        return _reads_commission(user, commission) or roles.has_role(user, *BACKOFFICE_VIEW_ROLES)
    if action == "change":
        # The answerable organisation may advance ITS OWN milestone: reporting that you have done
        # what you undertook to do is the one thing you can attest without the referent.
        if obj.responsible.user_id == user.id and obj.status != MilestoneStatus.NOT_APPLICABLE:
            return True
        return _moderates_commission(user, commission) or roles.has_role(user, *BACKOFFICE_MANAGE_ROLES)
    if action == "add":
        return _moderates_commission(user, commission) or roles.has_role(user, *BACKOFFICE_MANAGE_ROLES)
    return roles.has_role(user, *BACKOFFICE_MANAGE_ROLES) if action == "delete" else False


@policy(MonitoringEntry)
def monitoring_policy(user, action: str, obj: MonitoringEntry) -> bool:
    commission = obj.project.commission
    if action == "view":
        return _reads_commission(user, commission) or roles.has_role(user, *BACKOFFICE_VIEW_ROLES)
    if action in {"add", "change"}:
        return _moderates_commission(user, commission) or roles.has_role(user, *BACKOFFICE_MANAGE_ROLES)
    return roles.has_role(user, *BACKOFFICE_MANAGE_ROLES) if action == "delete" else False


@policy(AnnualReport)
def report_policy(user, action: str, obj: AnnualReport) -> bool:
    if action == "view":
        if is_secretariat(user, obj.edition_id):
            return True
        if not obj.is_published:
            # A draft relation changes every time it is regenerated; showing it would publish
            # figures the Forum has not yet stood behind.
            return roles.has_role(user, *BACKOFFICE_VIEW_ROLES)
        return _active_profiles(user, obj.edition_id).exists() or roles.has_role(user, *BACKOFFICE_VIEW_ROLES)
    if action in {"generate", "publish", "change"}:
        return is_secretariat(user, obj.edition_id) or roles.has_role(user, *BACKOFFICE_MANAGE_ROLES)
    return roles.has_role(user, *BACKOFFICE_MANAGE_ROLES) if action == "delete" else False
