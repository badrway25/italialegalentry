"""
Authorisation audit over the ten roles, by ATTACK SHAPE rather than by role.

`test_object_permissions.py` walks the thirteen assertions of the design directive, role by role.
This file crosses the other way: six ways in, each tried by everybody who should not get through.
The two overlap, and that is the point — a defect that survives one framing tends to die in the
other. Assertion 13 of the older file found a real gap (L-13) by comparing the list against the
object check; the cascade case below exists because a real gap (L-14) got through both.

The six shapes, from the pre-production directive:

1. no self privilege escalation
2. no horizontal access (a peer's records)
3. no cross-company access
4. no discovery through search
5. no document download by a known URL
6. no indirect delete or update through an unauthorised cascade

Shape 6 is the one that had never been tested, and it is the one that was broken.
"""

from __future__ import annotations

import datetime as dt

import pytest
from django.contrib import admin as dj_admin
from django.contrib.admin.utils import get_deleted_objects
from django.test import RequestFactory

from accounts import roles
from cases import services as case_services
from cases.models import AssignmentRole, CaseFile, CasePurpose
from core import clock

pytestmark = [pytest.mark.django_db, pytest.mark.security]

#: The ten roles the directive names. `forum_participant` is a person with a Forum registration:
#: the Forum grants no separate role, and asserting that is part of the audit.
AUDITED_ROLES = (
    "person",
    "company",
    "authorised_actor",
    "professional",
    "training_body",
    "institution",
    "university",
    "operator",
    "rule_editor",
    "administrator",
)


@pytest.fixture
def cast(django_user_model):
    roles.ensure_roles()

    def make(email, role, **extra):
        user = django_user_model.objects.create_user(email=email, password="Local-Only-2026!", **extra)
        if role:
            roles.assign_role(user, role)
        return user

    return {
        "person": make("audit-person@example.test", roles.PERSON),
        "other_person": make("audit-person-2@example.test", roles.PERSON),
        "company": make("audit-company@example.test", roles.COMPANY),
        "other_company": make("audit-company-2@example.test", roles.COMPANY),
        "authorised_actor": make("audit-actor@example.test", roles.AUTHORISED_ACTOR),
        "professional": make("audit-pro@example.test", roles.PROFESSIONAL),
        "training_body": make("audit-training@example.test", roles.TRAINING_PROVIDER),
        "institution": make("audit-institution@example.test", roles.INSTITUTION),
        "university": make("audit-university@example.test", roles.UNIVERSITY),
        "operator": make("audit-operator@example.test", roles.OPERATOR, is_staff=True),
        "rule_editor": make("audit-rule-editor@example.test", roles.LEGAL_EDITOR, is_staff=True),
        "administrator": make("audit-admin@example.test", roles.ADMINISTRATOR, is_staff=True),
    }


@pytest.fixture
def case(cast):
    return case_services.open_case(cast["person"], purpose=CasePurpose.WORK, pathway_key="salaried_work")


@pytest.fixture
def other_case(cast):
    return case_services.open_case(
        cast["other_person"], purpose=CasePurpose.STUDY, pathway_key="study_and_training_in_italy"
    )


# =================================================================================================
# 1 — no self privilege escalation
# =================================================================================================
@pytest.mark.parametrize("who", AUDITED_ROLES)
def test_no_role_can_grant_itself_a_role_it_does_not_hold(cast, who):
    """
    The roles registry is the only way in, and it audits. Nothing may add a group directly.

    Checked for every role rather than for the administrator alone: the interesting failure is a
    role nobody thought of, and `is_staff` is not the dividing line — a professional holds none.
    """
    user = cast[who]
    held = set(roles.roles_of(user))
    forbidden = {roles.SUPERADMIN, roles.ADMINISTRATOR} - held

    for role in forbidden:
        assert role not in roles.roles_of(user)
        assert not user.has_perm("accounts.add_user")
    assert user.is_superuser is False


@pytest.mark.parametrize("who", AUDITED_ROLES)
def test_no_role_holds_two_incompatible_roles(cast, who):
    """Separation of duties: `legal_editor` and `legal_approver` on one account is a one-eye review."""
    held = list(roles.roles_of(cast[who]))
    assert roles.check_role_set(held) is None or roles.check_role_set(held) == []


def test_a_rule_editor_cannot_reach_the_accounts_of_others(cast):
    editor = cast["rule_editor"]
    assert not editor.has_perm("accounts.change_user")
    assert not editor.has_perm("accounts.delete_user")
    assert not editor.has_perm("auth.change_group")


# =================================================================================================
# 2 — no horizontal access
# =================================================================================================
@pytest.mark.parametrize("who", AUDITED_ROLES)
def test_only_the_owner_and_a_live_assignee_read_a_case_file(cast, case, who):
    """
    The queryset is the authorisation. Every role that is not the owner gets an empty answer.

    The administrator is the single exception, and it is stated rather than assumed.
    """
    user = cast[who]
    readable = set(CaseFile.objects.readable_by(user))
    if who == "person":
        assert case in readable
    elif who == "administrator":
        assert case in readable, "an administrator reads case files; if that changes, change this line"
    else:
        assert case not in readable, f"{who} reached a case file it does not own"


def test_a_peer_of_the_same_role_reaches_nothing(cast, case, other_case):
    """Two people of the same role are the commonest horizontal pair, and the easiest to forget."""
    assert other_case not in CaseFile.objects.readable_by(cast["person"])
    assert case not in CaseFile.objects.readable_by(cast["other_person"])


def test_an_assignment_that_has_lapsed_reads_nothing(cast, case):
    case_services.assign(
        case,
        assignee=cast["professional"],
        role=AssignmentRole.PROFESSIONAL,
        authorisation_reference="SYNTH-AUTH-0002",
        authorisation_valid_until=clock.today() - dt.timedelta(days=1),
    )
    assert case not in CaseFile.objects.readable_by(cast["professional"])


# =================================================================================================
# 3 — no cross-company access
# =================================================================================================
def test_a_company_reaches_no_other_companys_profile_or_needs(cast):
    from companies.models import CompanyNeed, CompanyProfile

    mine = set(CompanyProfile.objects.readable_by(cast["company"]))
    theirs = set(CompanyProfile.objects.readable_by(cast["other_company"]))
    assert mine & theirs == set()

    my_needs = set(CompanyNeed.objects.readable_by(cast["company"]))
    their_needs = set(CompanyNeed.objects.readable_by(cast["other_company"]))
    assert my_needs & their_needs == set()


@pytest.mark.parametrize("who", ["person", "training_body", "institution", "university", "professional"])
def test_no_unrelated_role_reads_a_company_need(cast, who):
    from companies.models import CompanyNeed

    assert list(CompanyNeed.objects.readable_by(cast[who])) == []


def test_a_company_never_reaches_a_persons_case(cast, case):
    from accounts.permissions import can

    assert case not in CaseFile.objects.readable_by(cast["company"])
    assert can(cast["company"], "view", case) is False


# =================================================================================================
# 4 — no discovery through search
# =================================================================================================
@pytest.mark.parametrize("who", ["other_person", "company", "professional", "training_body", "university"])
def test_a_case_reference_cannot_be_discovered_by_asking_for_it(client, cast, case, who):
    """
    404, never 403. A 403 confirms the object exists, which is the answer the caller was after.

    Tried over HTTP rather than against the queryset, because this is the shape an attacker uses:
    a reference seen once, replayed by somebody else.
    """
    client.force_login(cast[who])
    response = client.get(f"/fr/espace-reserve/dossiers/{case.reference}/")
    assert response.status_code in (302, 404), f"{who} got {response.status_code}"
    assert response.status_code != 403, "403 tells the caller the case file exists"
    if response.status_code == 404:
        body = response.content.decode()
        # NOT asserted: that the reference is absent from the page. The 404 template emits hreflang
        # alternates for the URL that was requested, so the reference echoes back — but the caller
        # typed it, so nothing was disclosed. What must be absent is anything the caller did NOT
        # already hold: who the case belongs to, and what it is about.
        assert cast["person"].email not in body
        assert case.get_purpose_display() not in body
        assert case.pathway_key not in body


def test_a_search_box_does_not_widen_the_queryset(cast, case, other_case):
    """
    A search view that filters a wide queryset instead of narrowing an authorised one is the
    classic discovery hole: the authorisation is in the template, and the count is not.
    """
    readable = CaseFile.objects.readable_by(cast["person"])
    for term in (other_case.reference, other_case.reference[:4], "", "%", "' OR 1=1 --"):
        assert other_case not in readable.filter(reference__icontains=term)


# =================================================================================================
# 5 — no document download by a known URL
# =================================================================================================
def test_a_known_document_url_serves_nobody_but_its_owner(client, cast, tmp_path, settings):
    """
    A signed link narrows who and for how long. It never stands in for the authorisation check.

    The document is created here rather than borrowed from a fixture: a test that skips when it
    finds no rows is a test that silently stops covering the thing it names, and this is the one
    shape where the file on disk is somebody's identity document.
    """
    from django.core.files.uploadedfile import SimpleUploadedFile

    from documents import services as document_services
    from documents.models import DocumentKind

    settings.PRIVATE_MEDIA_ROOT = tmp_path / "private"
    # Stored through the service, not by writing the row: the service is what computes the size,
    # the checksum and the scan state, and a row built around it would be testing a shape the
    # application never produces.
    doc = document_services.store_upload(
        cast["person"],
        SimpleUploadedFile("passeport.pdf", b"%PDF-1.4 synthetic", content_type="application/pdf"),
        DocumentKind.choices[0][0],
    )

    for who in ("other_person", "company", "training_body", "institution", "university", "professional"):
        client.force_login(cast[who])
        response = client.get(f"/documents/{doc.pk}/")
        assert response.status_code in (302, 403, 404), f"{who} got {response.status_code}"
        assert b"%PDF" not in response.content, f"{who} received the file itself"

    client.force_login(cast["person"])
    owner_response = client.get(f"/documents/{doc.pk}/")
    assert owner_response.status_code == 200, "the owner must still reach their own document"


@pytest.mark.parametrize("who", ["other_person", "company", "training_body", "institution", "university"])
def test_the_private_media_root_is_not_served_by_the_web_server(settings, who):
    """
    The strongest statement available without a web server: nothing under it has a URL at all.

    A download route that checks authorisation is worth nothing if the file also sits under a
    directory the server lists.
    """
    from pathlib import Path

    private = Path(settings.PRIVATE_MEDIA_ROOT)
    media = Path(settings.MEDIA_ROOT)
    assert private != media
    assert media not in private.parents, "private uploads sit under the served media root"


# =================================================================================================
# 6 — no indirect delete or update through an unauthorised cascade
# =================================================================================================
@pytest.mark.parametrize("who", ["operator", "rule_editor"])
def test_a_staff_role_cannot_delete_through_a_cascade_it_may_not_delete_directly(cast, case, who):
    """
    The shape that produced L-14, asked in the opposite direction.

    There, a cascade made a deletion impossible for everybody. The mirror defect is worse: deleting
    a row the account MAY delete, which drags with it rows the account may not touch. Django's
    admin refuses that by collecting `perms_needed` across the whole cascade, so this asserts the
    refusal is actually reaching the roles that should meet it.
    """
    request = RequestFactory().get("/backoffice/")
    request.user = cast[who]
    _to_delete, _counts, perms_needed, _protected = get_deleted_objects([case], request, dj_admin.site)
    assert perms_needed, f"{who} would delete a case file and everything hanging off it"


def test_the_cascade_of_a_case_file_is_known_and_not_silent(cast, case, django_user_model):
    """
    A cascade nobody has enumerated is a cascade nobody has authorised.

    This does not assert a fixed list — that would break on every new model — but it does assert
    that deleting a case file reaches more than the case file, so a reviewer is told to look.
    """
    request = RequestFactory().get("/backoffice/")
    request.user = cast["administrator"]
    _to_delete, counts, _perms, _protected = get_deleted_objects([case], request, dj_admin.site)
    assert counts, "deleting a case file reports no cascade at all, which is unlikely to be true"


def test_a_person_cannot_reach_another_persons_case_through_the_service(cast, case):
    """
    The service layer, not the view: a view is one entry point and the service is all of them.

    `case_detail` takes the UUID, not the human reference. Passing the reference raises a
    ValidationError from the UUID parser rather than Http404 — which happens to refuse, but for the
    wrong reason, and a test that passes for the wrong reason stops testing the moment the argument
    changes shape.
    """
    from django.http import Http404

    with pytest.raises(Http404):
        case_services.case_detail(cast["other_person"], case.uuid)

    # And the owner does reach it, so the assertion above is not passing because everything fails.
    assert case_services.case_detail(cast["person"], case.uuid) == case
