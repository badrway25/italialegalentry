"""
Object-level policies for private documents (deny by default — ``accounts.permissions``).

Three objects, three questions:

``PrivateDocument``      may this account be handed THIS FILE?
``DocumentRequirement``  may this account see, file against, or review THIS REQUIREMENT of a case?
``DocumentVersion``      follows its requirement.

The primary defence is the queryset (``DocumentRequirementQuerySet.readable_by``): an account must
never learn that an object exists through a count, an autocomplete or a differently worded "not
found". These policies are the second defence, for a single object already in hand.

One deliberate narrowing, and the reason for it
-----------------------------------------------
``role:staff`` may read a private document that belongs to nobody's case file — the legacy personal
uploads of the reserved area. It may **not** read a document attached to a case requirement, unless
it also holds ``role:administrator``.

That mirrors ``cases.CaseFileQuerySet.readable_by``, which gives project staff nothing: supervision
happens in the back-office, where each access is role-checked and audited. Without this narrowing,
the documents app would be a back door around exactly the boundary the case file draws — and the
documents at stake are, very often, copies of somebody's identity papers.
"""

from __future__ import annotations

from accounts import roles
from accounts.models import MembershipRole
from accounts.permissions import policy
from cases.models import AssignmentRole, ResponsibleActor
from documents.models import AccessClass, DocumentRequirement, DocumentVersion, PrivateDocument

READ_ACTIONS = frozenset({"view", "download"})

#: Assignment roles whose mandate covers acting on the pieces of a case file. An authorised actor
#: works on the selection process and a training body on training data; neither files or reviews a
#: person's identity papers, so neither is here (CR-03, CR-04).
ASSIGNEE_MAY_ACT = frozenset({AssignmentRole.PROFESSIONAL, AssignmentRole.OPERATOR})


def is_organisation_owner(user, organisation_id) -> bool:
    if not organisation_id:
        return False
    return user.memberships.filter(organisation_id=organisation_id, role=MembershipRole.OWNER).exists()


def _live_assignment(user, case):
    for row in case.assignments.all():
        if row.assignee_id == user.id and row.is_live:
            return row
    return None


def _requirements_of(doc: PrivateDocument):
    """The case requirements this file was filed against, if any."""
    return DocumentRequirement.objects.filter(versions__document=doc).distinct()


@policy(PrivateDocument)
def private_document_policy(user, action: str, doc: PrivateDocument) -> bool:
    if doc.deleted_at is not None:
        return False
    if action in READ_ACTIONS:
        if doc.owner_id == user.id:
            return True
        if is_organisation_owner(user, doc.organisation_id):
            return True
        attached = list(_requirements_of(doc))
        if attached:
            # A case document is governed by the case, never by a blanket role.
            readable = DocumentRequirement.objects.readable_by(user)
            return readable.filter(pk__in=[row.pk for row in attached]).exists()
        return roles.has_role(user, roles.STAFF, roles.ADMINISTRATOR)
    if action == "delete":
        # A piece filed against a requirement is evidence in a case file: it is superseded by a new
        # version or purged by retention, never quietly deleted by its uploader.
        if _requirements_of(doc).exists():
            return False
        return doc.owner_id == user.id
    return False


@policy(DocumentRequirement)
def requirement_policy(user, action: str, obj: DocumentRequirement) -> bool:
    case = obj.case
    restricted = obj.access_class == AccessClass.RESTRICTED
    is_person = case.person_id == user.id
    assignment = _live_assignment(user, case)
    may_act = assignment is not None and assignment.role in ASSIGNEE_MAY_ACT and not restricted

    if action == "view":
        if is_person:
            return True
        if assignment is not None and not restricted:
            return True
        return roles.has_role(user, roles.ADMINISTRATOR)

    if action == "file":
        # Depositing a piece. The person may file what is THEIRS to provide: a nulla osta issued by
        # an authority is not something an applicant can attest, and offering them the button would
        # be a small lie that wastes their time.
        if case.is_read_only:
            return False
        if is_person:
            return obj.responsible_actor == ResponsibleActor.PERSON
        if may_act:
            return True
        return roles.has_role(user, roles.ADMINISTRATOR)

    if action == "review":
        # Never the person: nobody validates their own evidence, whatever the interface allows.
        if is_person:
            return False
        if case.is_read_only:
            return False
        if may_act:
            return True
        return roles.has_role(user, roles.ADMINISTRATOR)

    if action in {"change", "delete"}:
        return roles.has_role(user, roles.ADMINISTRATOR)
    return False


@policy(DocumentVersion)
def version_policy(user, action: str, obj: DocumentVersion) -> bool:
    from accounts.permissions import can

    if action in READ_ACTIONS:
        return can(user, "view", obj.requirement)
    if action == "review":
        return can(user, "review", obj.requirement)
    return False
