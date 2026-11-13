"""
Object-level authorisation for the legal rule engine. Deny by default, like everything else.

The interesting rule is not who may read a rule — everyone in the back-office may — but who may
approve one. That answer depends on the OBJECT, not only on the role: a legal approver may approve
any rule except one they wrote themselves. A permission system that can only answer "may this role
approve rules?" cannot express that, which is exactly why this project has object-level policies.
"""

from __future__ import annotations

from accounts import roles
from accounts.permissions import policy
from rules.models import LegalRule, LegalSource

READERS = (roles.LEGAL_EDITOR, roles.LEGAL_APPROVER, roles.ADMINISTRATOR, roles.STAFF)


def may_draft(user) -> bool:
    return roles.has_role(user, roles.LEGAL_EDITOR, roles.ADMINISTRATOR)


def may_review(user) -> bool:
    """
    The role that approves a rule, puts it in force and retires it: role:legal_approver.

    The back office's workflow actions are offered on this answer (finding F-8): the rule editor asks the policy the
    platform asks, never the model permission alone.
    """
    return roles.has_role(user, roles.LEGAL_APPROVER)


def may_approve(user, rule: LegalRule) -> bool:
    """
    A legal approver, who is not the author.

    The second half is the whole point. Without it the role separation is decorative: one account
    holding both hats produces a rule whose review records the same judgement twice.
    """
    if not may_review(user):
        return False
    return rule.created_by_id is None or rule.created_by_id != user.pk


@policy(LegalRule)
def _legal_rule(user, action: str, obj: LegalRule) -> bool:
    if action == "view":
        return roles.has_role(user, *READERS)
    if action == "approve":
        return may_approve(user, obj)
    if action in {"change", "submit"}:
        # A rule in force is never edited: assessments already given depend on it reading the way it
        # read when they were given. Changing it means opening a new version.
        from rules.models import ReviewStatus

        if obj.review_status in {ReviewStatus.ACTIVE, ReviewStatus.RETIRED}:
            return False
        return may_draft(user)
    if action in {"activate", "retire"}:
        return may_review(user)
    if action == "new_version":
        return may_draft(user)
    return False


@policy(LegalSource)
def _legal_source(user, action: str, obj: LegalSource) -> bool:
    if action == "view":
        return roles.has_role(user, *READERS)
    if action in {"change", "add"}:
        return may_draft(user)
    return False
