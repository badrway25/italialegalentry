"""
A CLOSED case file takes no new assignment (W4-D part 2, A4 — F-8's Q-8).

CASE_LIFECYCLE.md §4 rule 5: «Un fascicolo CLOSED è in sola lettura. Si apre un nuovo fascicolo, non si riapre il
vecchio.» ``cases.services.assign`` accepted a new assignment on a CLOSED file (F-8 left it unchanged and asked the
owner, Q-8): a grant that gives an account the reading of a file nobody may work on any more. It is refused now — in
the domain, on the file's row as it stands (a file closed after the caller loaded it is refused too), and in the back
office's add form, which shows the domain's own sentence on the file's field. Narrowing only: ending an assignment on a
closed file stays possible (it takes access away), and an active file is assigned as before.
"""

from __future__ import annotations

import pytest
from django.core.exceptions import ValidationError
from django.utils import translation

from accounts import roles
from audit.models import AuditEvent
from cases import services
from cases.models import AssignmentRole, CaseAssignment, CaseFile, CasePurpose, CaseStatus
from core import clock

pytestmark = [pytest.mark.django_db, pytest.mark.security]

PASSWORD = "Local-Only-W4D-2026!"
ADD = "/backoffice/cases/caseassignment/add/"
REFUSAL = "Un fascicolo concluso non si riapre: se ne apre uno nuovo."  # the msgid (CASE_LIFECYCLE §4 rule 5)
with translation.override("fr"):
    REFUSAL_FR = str(translation.gettext(REFUSAL))  # «Un dossier clôturé ne se rouvre pas : on en ouvre un nouveau.»


@pytest.fixture
def people(django_user_model):
    roles.ensure_roles()

    def make(email, role, **extra):
        user = django_user_model.objects.create_user(email=email, password=PASSWORD, **extra)
        roles.assign_role(user, role)
        return user

    return {
        "owner": make("w4d.q8.owner@example.test", roles.PERSON),
        "professional": make("w4d.q8.pro@example.test", roles.PROFESSIONAL),
        "operator": make("w4d.q8.operator@example.test", roles.OPERATOR, is_staff=True),
        "administrator": make("w4d.q8.admin@example.test", roles.ADMINISTRATOR, is_staff=True),
        "superuser": django_user_model.objects.create_superuser(email="w4d.q8.super@example.test", password=PASSWORD),
    }


@pytest.fixture
def case(people):
    return services.open_case(people["owner"], purpose=CasePurpose.WORK, pathway_key="salaried_work")


def _close(case):
    """Test set-up: the file CLOSED as the lifecycle leaves it (status and closing date), without walking the graph."""
    CaseFile.objects.filter(pk=case.pk).update(
        status=CaseStatus.CLOSED, status_since=clock.now(), closed_at=clock.now()
    )
    case.refresh_from_db()
    return case


def _form(case, assignee, role=AssignmentRole.PROFESSIONAL) -> dict:
    return {
        "case": case.pk,
        "assignee": assignee.pk,
        "role": role,
        "organisation": "",
        "authorisation_reference": "",
        "authorisation_jurisdiction": "",
        "authorisation_valid_until": "",
        "mandate_note": "",
        "_save": "Save",
    }


# ---------------------------------------------------------------------------------------------
# The domain
# ---------------------------------------------------------------------------------------------
def test_the_domain_refuses_a_new_assignment_on_a_closed_file(case, people):
    from notifications.models import Notification

    _close(case)
    events = AuditEvent.objects.count()
    with pytest.raises(ValidationError) as refused:
        services.assign(case, people["professional"], role=AssignmentRole.PROFESSIONAL, actor=people["administrator"])
    assert REFUSAL_FR != REFUSAL, "the catalogue translates the sentence"
    assert " ".join(refused.value.messages) in (REFUSAL, REFUSAL_FR)
    assert not CaseAssignment.objects.filter(case=case).exists()
    assert AuditEvent.objects.count() == events, "a refused grant writes no «case.assigned» event"
    assert not Notification.objects.filter(recipient=people["professional"]).exists()


def test_the_domain_reads_the_file_as_it_stands_not_as_the_caller_loaded_it(case, people):
    stale = CaseFile.objects.get(pk=case.pk)
    _close(case)
    assert stale.status != CaseStatus.CLOSED
    with pytest.raises(ValidationError):
        services.assign(stale, people["professional"], role=AssignmentRole.PROFESSIONAL)
    assert not CaseAssignment.objects.filter(case=case).exists()


def test_the_domain_still_assigns_an_active_file(case, people):
    row = services.assign(case, people["professional"], role=AssignmentRole.PROFESSIONAL, actor=people["administrator"])
    assert row.is_live and row.case_id == case.pk
    assert AuditEvent.objects.filter(action="case.assigned", target_id=str(case.pk)).count() == 1


def test_a_suspended_file_is_not_read_only_and_is_still_assigned(case, people):
    """Rule 5 speaks of CLOSED only: a suspended file waits, and someone may have to be named to resolve it."""
    CaseFile.objects.filter(pk=case.pk).update(status=CaseStatus.SUSPENDED, previous_status=case.status)
    case.refresh_from_db()
    assert services.assign(case, people["professional"], role=AssignmentRole.PROFESSIONAL).is_live


def test_an_assignment_on_a_file_closed_since_can_still_be_ended(case, people):
    """Narrowing only: taking access away from a closed file stays possible."""
    row = services.assign(case, people["professional"], role=AssignmentRole.PROFESSIONAL)
    _close(case)
    services.revoke_assignment(row, actor=people["administrator"])
    row.refresh_from_db()
    assert row.revoked_at is not None and not row.is_live


# ---------------------------------------------------------------------------------------------
# The back office's add form
# ---------------------------------------------------------------------------------------------
def test_the_back_office_refuses_the_grant_on_a_closed_file_with_the_domains_sentence(client, case, people):
    _close(case)
    client.force_login(people["superuser"])
    response = client.post(ADD, _form(case, people["professional"]))
    assert response.status_code == 200, "the form is shown again with its error, never a crash"
    html = response.content.decode("utf-8")
    assert REFUSAL in html or REFUSAL_FR in html
    assert not CaseAssignment.objects.filter(case=case).exists()
    assert not AuditEvent.objects.filter(action="case.assigned", target_id=str(case.pk)).exists()


def test_the_back_office_still_grants_on_an_active_file(client, case, people):
    client.force_login(people["superuser"])
    response = client.post(ADD, _form(case, people["professional"]))
    assert response.status_code == 302
    assert CaseAssignment.objects.filter(case=case, assignee=people["professional"]).count() == 1


@pytest.mark.parametrize("closed", [False, True])
def test_the_administrator_role_still_grants_nothing_there(client, case, people, closed):
    """Unchanged by this fix: only a superuser grants an assignment in the back office (F-8's Q-5, still open)."""
    if closed:
        _close(case)
    client.force_login(people["administrator"])
    response = client.post(ADD, _form(case, people["professional"]))
    assert response.status_code == 403
    assert not CaseAssignment.objects.filter(case=case).exists()


def test_the_back_office_still_ends_an_assignment_on_a_closed_file(client, case, people):
    row = services.assign(case, people["professional"], role=AssignmentRole.PROFESSIONAL)
    _close(case)
    client.force_login(people["superuser"])
    change = f"/backoffice/cases/caseassignment/{row.pk}/change/"
    page = client.get(change)
    assert page.status_code == 200 and 'name="revoked_at_0"' in page.content.decode("utf-8")
    data = dict.fromkeys(("organisation", "authorisation_reference", "authorisation_jurisdiction"), "")
    data.update({"revoked_at_0": "2026-10-17", "revoked_at_1": "10:00:00", "_save": "Save"})
    response = client.post(change, data)
    assert response.status_code == 302, response.content.decode("utf-8")[:500]
    row.refresh_from_db()
    assert row.revoked_at is not None


def test_the_operator_still_grants_nothing_there(client, case, people):
    """Unchanged by this fix: only the administration creates an assignment outside the services."""
    client.force_login(people["operator"])
    response = client.post(ADD, _form(case, people["professional"]))
    assert response.status_code == 403
    assert not CaseAssignment.objects.filter(case=case).exists()
