"""
The thirteen object-level permission assertions of the rebase directive §61 (PERMISSION_MODEL §6.7).

Every one of them is a sentence about somebody who must NOT see something. They are written against
the real querysets and the real services, never against a hand-built fixture, because the defect this
suite exists to catch is precisely the one where a view or a queryset quietly widens.

Two of the thirteen deserve their own note:

* **"a hand-typed identifier never bypasses the permissions."** Guessing an identifier must answer
  the same way a non-existent one does. A 403 on somebody else's file confirms the file exists,
  which is itself a disclosure — so the answer is 404.
* **"the list and the detail agree."** A row visible in a list but refused in detail, or the reverse,
  means two different authorisation rules are in force for one object. Whichever is the lenient one
  is the bug, and the asymmetry is how you find it.
"""

from __future__ import annotations

import datetime as dt

import pytest
from django.core.exceptions import PermissionDenied

from accounts import roles
from accounts.permissions import can
from cases import services as case_services
from cases.models import AssignmentRole, CaseFile, CasePurpose, ResponsibleActor
from core import clock

pytestmark = [pytest.mark.django_db, pytest.mark.security]


# ---------------------------------------------------------------------------------------------
# Cast
# ---------------------------------------------------------------------------------------------
@pytest.fixture
def cast(django_user_model):
    """One account per role that appears in the assertions. Built once, used by every test."""
    roles.ensure_roles()

    def make(email, role, **extra):
        user = django_user_model.objects.create_user(email=email, password="Local-Only-2026!", **extra)
        if role:
            roles.assign_role(user, role)
        return user

    return {
        "person_a": make("person-a@example.test", roles.PERSON),
        "person_b": make("person-b@example.test", roles.PERSON),
        "company_a": make("company-a@example.test", roles.COMPANY),
        "company_b": make("company-b@example.test", roles.COMPANY),
        "professional": make("professional@example.test", roles.PROFESSIONAL),
        "other_professional": make("professional-2@example.test", roles.PROFESSIONAL),
        "training_body": make("training@example.test", roles.TRAINING_PROVIDER),
        "institution": make("institution@example.test", roles.INSTITUTION),
        "university": make("university@example.test", roles.UNIVERSITY),
        "forum_member": make("forum@example.test", roles.PERSON),
        "staff": make("staff@example.test", roles.STAFF, is_staff=True),
        "legal_editor": make("legal-editor@example.test", roles.LEGAL_EDITOR, is_staff=True),
        "legal_approver": make("legal-approver@example.test", roles.LEGAL_APPROVER, is_staff=True),
    }


@pytest.fixture
def case_a(cast):
    return case_services.open_case(cast["person_a"], purpose=CasePurpose.WORK, pathway_key="salaried_work")


@pytest.fixture
def case_b(cast):
    return case_services.open_case(
        cast["person_b"], purpose=CasePurpose.STUDY, pathway_key="study_and_training_in_italy"
    )


def assign(case, user, *, valid_until=None, role=AssignmentRole.PROFESSIONAL):
    return case_services.assign(
        case,
        assignee=user,
        role=role,
        authorisation_reference="SYNTH-AUTH-0001",
        authorisation_valid_until=valid_until or (clock.today() + dt.timedelta(days=30)),
    )


# ---------------------------------------------------------------------------------------------
# 1 — person A does not reach person B
# ---------------------------------------------------------------------------------------------
def test_1_a_person_does_not_reach_another_persons_case(cast, case_a, case_b):
    readable = CaseFile.objects.readable_by(cast["person_a"])
    assert case_a in readable
    assert case_b not in readable
    assert can(cast["person_a"], "view", case_b) is False


def test_1b_a_person_does_not_reach_another_persons_checklist(cast, case_a, case_b):
    item = case_services.add_checklist_item(case_b, requirement="Passeport", responsible_actor=ResponsibleActor.PERSON)
    assert can(cast["person_a"], "view", item) is False
    assert can(cast["person_b"], "view", item) is True


# ---------------------------------------------------------------------------------------------
# 2 / 3 — company A does not reach company B, and no company browses people
# ---------------------------------------------------------------------------------------------
def test_2_a_company_does_not_reach_another_companys_records(cast):
    pytest.importorskip("companies.models", reason="the company workspace is not installed")
    from companies.models import CompanyProfile

    readable_a = CompanyProfile.objects.readable_by(cast["company_a"])
    readable_b = CompanyProfile.objects.readable_by(cast["company_b"])
    assert set(readable_a) & set(readable_b) == set()


def test_3_a_company_never_reaches_a_persons_case(cast, case_a):
    assert case_a not in CaseFile.objects.readable_by(cast["company_a"])
    assert can(cast["company_a"], "view", case_a) is False


# ---------------------------------------------------------------------------------------------
# 4 — the professional sees only the cases assigned to them
# ---------------------------------------------------------------------------------------------
def test_4_a_professional_sees_only_assigned_cases(cast, case_a, case_b):
    assign(case_a, cast["professional"])
    readable = CaseFile.objects.readable_by(cast["professional"])
    assert case_a in readable
    assert case_b not in readable


def test_4b_a_professional_with_no_assignment_sees_nothing(cast, case_a):
    assert CaseFile.objects.readable_by(cast["other_professional"]).count() == 0


# ---------------------------------------------------------------------------------------------
# 5 — the training body sees only training data
# ---------------------------------------------------------------------------------------------
def test_5_a_training_body_never_reaches_a_case_file(cast, case_a):
    assert case_a not in CaseFile.objects.readable_by(cast["training_body"])
    assert can(cast["training_body"], "view", case_a) is False


# ---------------------------------------------------------------------------------------------
# 6 / 7 — the institution stays inside its agreement, the university holds no private file
# ---------------------------------------------------------------------------------------------
def test_6_an_institution_reaches_no_case_file(cast, case_a):
    assert CaseFile.objects.readable_by(cast["institution"]).count() == 0


def test_7_a_university_reaches_no_private_case_file(cast, case_a):
    assert CaseFile.objects.readable_by(cast["university"]).count() == 0
    assert can(cast["university"], "view", case_a) is False


# ---------------------------------------------------------------------------------------------
# 8 — a Forum participant reaches nobody's private information
# ---------------------------------------------------------------------------------------------
def test_8_a_forum_participant_reaches_no_private_case(cast, case_a):
    assert case_a not in CaseFile.objects.readable_by(cast["forum_member"])


# ---------------------------------------------------------------------------------------------
# 9 / 10 — staff without the permission do not change rules; the legal editor gains nothing else
# ---------------------------------------------------------------------------------------------
def test_9_staff_without_the_role_cannot_change_a_legal_rule(cast):
    from rules.models import LegalRule, RuleEffect

    rule = LegalRule.objects.create(
        rule_id="R-PERM-001",
        version=1,
        pathway="salaried_work",
        effect=RuleEffect.WARNING,
        message_key="k",
        message_fr="m",
        valid_from=dt.date(2026, 1, 1),
    )
    assert can(cast["staff"], "change", rule) is False
    assert can(cast["legal_editor"], "change", rule) is True


def test_10_the_legal_editor_gains_no_unrelated_privilege(cast, case_a):
    from rules.models import LegalRule, RuleEffect

    editor = cast["legal_editor"]
    assert CaseFile.objects.readable_by(editor).count() == 0
    assert can(editor, "view", case_a) is False

    rule = LegalRule.objects.create(
        rule_id="R-PERM-002",
        version=1,
        pathway="salaried_work",
        effect=RuleEffect.WARNING,
        message_key="k",
        message_fr="m",
        valid_from=dt.date(2026, 1, 1),
        created_by=editor,
    )
    # And cannot approve — not even a rule somebody else wrote, because approval is not their role.
    assert can(editor, "approve", rule) is False


def test_10b_the_legal_approver_cannot_approve_their_own_rule(cast):
    from rules.models import LegalRule, RuleEffect

    approver = cast["legal_approver"]
    own = LegalRule.objects.create(
        rule_id="R-PERM-003",
        version=1,
        pathway="salaried_work",
        effect=RuleEffect.WARNING,
        message_key="k",
        message_fr="m",
        valid_from=dt.date(2026, 1, 1),
        created_by=approver,
    )
    someone_elses = LegalRule.objects.create(
        rule_id="R-PERM-004",
        version=1,
        pathway="salaried_work",
        effect=RuleEffect.WARNING,
        message_key="k",
        message_fr="m",
        valid_from=dt.date(2026, 1, 1),
        created_by=cast["legal_editor"],
    )
    assert can(approver, "approve", own) is False
    assert can(approver, "approve", someone_elses) is True


# ---------------------------------------------------------------------------------------------
# 11 — a hand-typed identifier never bypasses the permissions
# ---------------------------------------------------------------------------------------------
def test_11_a_guessed_reference_answers_the_same_as_one_that_does_not_exist(client, cast, case_b):
    """
    404, not 403. A 403 on somebody else's file confirms that the file exists, and the reference is
    short enough to type. The two answers must be indistinguishable.
    """
    client.force_login(cast["person_a"])
    real = client.get(f"/fr/espace-reserve/mes-demandes/dossier/{case_b.reference}/")
    invented = client.get("/fr/espace-reserve/mes-demandes/dossier/ZZZZZZZZZZ/")
    assert real.status_code == invented.status_code
    assert real.status_code in (302, 404)


def _apart_as_counters(first: str, second: str) -> int | None:
    """How far apart two references are read as a counter, in decimal or in hex (None: neither reading)."""
    gaps = []
    for base in (10, 16):
        try:
            gaps.append(abs(int(second, base) - int(first, base)))
        except ValueError:
            continue
    return min(gaps, default=None)


def test_11b_the_case_reference_is_not_sequential(cast, case_a, case_b):
    """A sequential identifier both leaks volume and makes the hand-typed probe worth attempting."""
    assert case_a.reference != case_b.reference
    # Not the row number, padded or not. (« not all digits » failed by chance once run in 110: a random
    # draw of ten hex digits is all decimal that often, and is no more guessable for it.)
    assert case_a.reference.lstrip("0") not in {str(case_a.pk), str(case_b.pk)}
    # Nor the next value of a counter, written in decimal or in hex: two cases opened one after the other
    # are 1 apart on a counter (a few more if other rows were numbered in between), while two random draws
    # of ten hex digits come within 1,000 of each other about once in 550 million runs.
    gap = _apart_as_counters(case_a.reference, case_b.reference)
    assert gap is None or gap > 1000, f"references {gap} apart: a counter, not a random draw"
    assert len(case_a.reference) >= 10


# ---------------------------------------------------------------------------------------------
# 12 — a revoked or lapsed assignment grants nothing
# ---------------------------------------------------------------------------------------------
def test_12_a_revoked_assignment_grants_nothing(cast, case_a):
    assignment = assign(case_a, cast["professional"])
    assert case_a in CaseFile.objects.readable_by(cast["professional"])

    case_services.revoke_assignment(assignment)
    assert case_a not in CaseFile.objects.readable_by(cast["professional"])
    assert can(cast["professional"], "view", case_a) is False


def test_12b_a_lapsed_authorisation_grants_nothing(cast, case_a):
    """
    The authorisation's validity is checked at READ time, not at assignment time.

    An authorisation that expired yesterday and a row nobody ever created must give the same access:
    none. Checking only on the way in would leave the access alive for as long as the row is.
    """
    assign(case_a, cast["professional"], valid_until=clock.today() - dt.timedelta(days=1))
    assert case_a not in CaseFile.objects.readable_by(cast["professional"])
    assert can(cast["professional"], "view", case_a) is False


# ---------------------------------------------------------------------------------------------
# 13 — the list and the detail agree
# ---------------------------------------------------------------------------------------------
@pytest.mark.parametrize("who", ["person_a", "person_b", "professional", "company_a", "staff"])
def test_13_the_list_and_the_object_check_agree(cast, case_a, case_b, who):
    """
    Whatever a role can list, it can open; whatever it cannot open, it cannot list.

    A disagreement means two authorisation rules are in force for one object, and the lenient one is
    the defect. Running it over every role is what makes the assertion worth having.
    """
    user = cast[who]
    listed = set(CaseFile.objects.readable_by(user).values_list("pk", flat=True))
    for case in (case_a, case_b):
        assert (case.pk in listed) == can(user, "view", case), (
            f"{who}: list says {case.pk in listed}, object check says {can(user, 'view', case)}"
        )


def test_13b_staff_get_nothing_from_the_case_queryset(cast, case_a, case_b):
    """
    Being back-office is not a reason to read a person's legal file.

    The previous platform's staff accounts all carried full administration, which is the defect this
    inverts: access to a case file comes from a live, referenced assignment or from owning it.
    """
    assert CaseFile.objects.readable_by(cast["staff"]).count() == 0


# ---------------------------------------------------------------------------------------------
# The default itself
# ---------------------------------------------------------------------------------------------
def test_the_registry_denies_an_unregistered_model(cast):
    from accounts.models import Organisation

    unregistered = Organisation.objects.create(name="Some organisation", kind="company")
    assert can(cast["staff"], "view", unregistered) is False


def test_an_inactive_account_can_do_nothing(cast, case_a):
    person = cast["person_a"]
    person.is_active = False
    person.save(update_fields=["is_active"])
    assert can(person, "view", case_a) is False


def test_an_anonymous_caller_can_do_nothing(case_a):
    from django.contrib.auth.models import AnonymousUser

    assert can(AnonymousUser(), "view", case_a) is False


def test_require_raises_rather_than_returning_false(cast, case_b):
    from accounts.permissions import require

    with pytest.raises(PermissionDenied):
        require(cast["person_a"], "view", case_b)
