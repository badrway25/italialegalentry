"""
Object-level policy for public submissions (deny by default, see accounts.permissions).

* the owner (authenticated submitter) may *view* their own submissions;
* back-office roles (staff, administrator, superadmin) may view and change every submission;
* everybody else is denied (IDOR protection for the future portal views).
"""

from __future__ import annotations

from accounts import roles
from accounts.permissions import owns, policy
from enquiries.models import PublicSubmission

BACKOFFICE_VIEW_ROLES = (roles.STAFF, roles.ADMINISTRATOR, roles.SUPERADMIN)


@policy(PublicSubmission)
def submission_policy(user, action: str, obj: PublicSubmission) -> bool:
    if action in ("view", "change", "export", "anonymise") and roles.has_role(user, *BACKOFFICE_VIEW_ROLES):
        return True
    return action == "view" and owns(user, obj) and not obj.is_anonymised
