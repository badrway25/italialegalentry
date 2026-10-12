"""
Object-level policies of the digital case file (deny by default — ``accounts.permissions``).

The queryset in ``CaseFileQuerySet.readable_by`` is the primary defence: it keeps unauthorised rows
out of lists, counts and search results, so a user never learns that an object exists. These
policies are the second defence, for a single object already in hand.

CaseFile        person (owner): view, and change while the case is active
                live assignee: view; professional and operator may also change
                administrator: view, change, delete — and nobody else, whatever their role
ChecklistItem   follows its case, plus: the person may mark their OWN items
CaseAssignment  follows its case; only administrators create or revoke outside the services
PathwayAssessment  follows its case, read-only for everyone (an assessment is frozen evidence)

An assignment that is revoked or whose authorisation has expired grants nothing: ``is_live`` is
checked, never the mere existence of the row. Otherwise a lapsed authorisation would keep reading
personal data, which is exactly what the mandate is supposed to bound.
"""

from __future__ import annotations

from accounts import roles
from accounts.permissions import policy
from cases.models import (
    AssignmentRole,
    CaseAssignment,
    CaseFile,
    ChecklistItem,
    PathwayAssessment,
    ResponsibleActor,
)

#: Who may read a case file WITHOUT owning it and WITHOUT an assignment.
#:
#: ``role:staff`` used to be here, and it was the lenient half of a disagreement: the queryset gives
#: project staff nothing, while this policy said yes to the same account and the same file. Any view
#: that checked the policy instead of going through the queryset would have handed a staff account
#: somebody's legal file. The queryset's reasoning is the right one — a standing ability to read
#: every case file is a disclosure, not supervision — so the policy now agrees with it.
#:
#: An operator handles case files through an ASSIGNMENT, like a professional, because "who is
#: responsible for this file" has to be answerable by name and by date.
BACKOFFICE_VIEW_ROLES = (roles.ADMINISTRATOR,)
BACKOFFICE_MANAGE_ROLES = (roles.ADMINISTRATOR,)

#: Assignment roles allowed to change a case they are assigned to. An authorised actor acts on the
#: selection process, not on the case file as a whole; a training body sees training data only.
ASSIGNEE_CAN_CHANGE = frozenset({AssignmentRole.PROFESSIONAL, AssignmentRole.OPERATOR})


def live_assignment(user, case: CaseFile) -> CaseAssignment | None:
    for row in case.assignments.all():
        if row.assignee_id == user.id and row.is_live:
            return row
    return None


@policy(CaseFile)
def case_policy(user, action: str, obj: CaseFile) -> bool:
    if obj.person_id == user.id:
        if action == "view":
            return True
        if action == "change":
            return not obj.is_read_only
        return False
    assignment = live_assignment(user, obj)
    if assignment is not None:
        if action == "view":
            return True
        if action == "change":
            return assignment.role in ASSIGNEE_CAN_CHANGE and not obj.is_read_only
        return False
    if action == "view":
        return roles.has_role(user, *BACKOFFICE_VIEW_ROLES)
    if action in {"change", "delete"}:
        return roles.has_role(user, *BACKOFFICE_MANAGE_ROLES)
    return False


@policy(ChecklistItem)
def checklist_policy(user, action: str, obj: ChecklistItem) -> bool:
    case = obj.case
    if case.person_id == user.id:
        if action == "view":
            return True
        # The person may only advance items that are theirs to act on: marking "the authority has
        # issued the document" is not something the applicant can attest.
        if action == "change":
            return not case.is_read_only and obj.responsible_actor == ResponsibleActor.PERSON
        return False
    assignment = live_assignment(user, case)
    if assignment is not None:
        if action == "view":
            return True
        if action == "change":
            return assignment.role in ASSIGNEE_CAN_CHANGE and not case.is_read_only
        return False
    if action == "view":
        return roles.has_role(user, *BACKOFFICE_VIEW_ROLES)
    if action in {"change", "delete"}:
        return roles.has_role(user, *BACKOFFICE_MANAGE_ROLES)
    return False


@policy(CaseAssignment)
def assignment_policy(user, action: str, obj: CaseAssignment) -> bool:
    if action == "view":
        if obj.case.person_id == user.id or obj.assignee_id == user.id:
            # The person always sees WHO is working on their case: that is the whole point of
            # naming the responsible actor.
            return True
        return roles.has_role(user, *BACKOFFICE_VIEW_ROLES)
    if action in {"add", "change", "delete"}:
        return roles.has_role(user, *BACKOFFICE_MANAGE_ROLES)
    return False


@policy(PathwayAssessment)
def assessment_policy(user, action: str, obj: PathwayAssessment) -> bool:
    # An assessment is frozen evidence: nobody edits one, not even an administrator. A new
    # assessment is recorded instead, so the history stays honest.
    if action != "view":
        return False
    case = obj.case
    if case.person_id == user.id or live_assignment(user, case) is not None:
        return True
    return roles.has_role(user, *BACKOFFICE_VIEW_ROLES)


# ``BACKOFFICE_VIEW_ROLES`` and ``CaseFileQuerySet.readable_by`` must answer the same question the
# same way. ``tests/security/test_object_permissions.py::test_13_the_list_and_the_object_check_agree``
# runs every role through both and fails on any disagreement, which is how the staff discrepancy
# above was found rather than deduced.
