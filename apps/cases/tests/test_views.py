"""
The case file's pages: who reaches them, what they may change, and what they are told.

The list and the detail are served from ONE queryset, so the interesting assertions are the ones
that would catch a second authorisation rule creeping in: a reference that is not yours answers
exactly as a reference that does not exist; a lapsed mandate stops working at read time; and a
control the policy would refuse is neither offered nor honoured.
"""

from __future__ import annotations

import datetime as dt

import pytest

from accounts import roles
from cases import services
from cases.models import (
    AssignmentRole,
    CaseFile,
    CasePurpose,
    CaseStatus,
    ChecklistStatus,
    ResponsibleActor,
)
from core import clock

pytestmark = pytest.mark.django_db

INDEX = "/fr/espace-reserve/dossiers/"


def detail_url(case) -> str:
    return f"{INDEX}{case.reference}/"


@pytest.fixture
def owner(django_user_model):
    roles.ensure_roles()
    user = django_user_model.objects.create_user(email="owner@example.test", password="x", full_name="Owner ONE")
    roles.assign_role(user, roles.PERSON)
    return user


@pytest.fixture
def stranger(django_user_model):
    roles.ensure_roles()
    user = django_user_model.objects.create_user(email="stranger@example.test", password="x")
    roles.assign_role(user, roles.PERSON)
    return user


@pytest.fixture
def professional(django_user_model):
    roles.ensure_roles()
    user = django_user_model.objects.create_user(email="pro@example.test", password="x")
    roles.assign_role(user, roles.PROFESSIONAL)
    return user


@pytest.fixture
def case(owner):
    row = services.open_case(owner, purpose=CasePurpose.WORK, pathway_key="salaried_work")
    services.add_checklist_item(
        row,
        requirement="Passeport en cours de validité",
        responsible_actor=ResponsibleActor.PERSON,
        source_title="Code des visas",
        source_ref="Reg. (CE) n. 810/2009, art. 12",
    )
    services.add_checklist_item(
        row,
        requirement="Nulla osta al lavoro",
        responsible_actor=ResponsibleActor.AUTHORITY,
    )
    return row


def assign(case, user, *, valid_until=None, role=AssignmentRole.PROFESSIONAL):
    return services.assign(
        case,
        assignee=user,
        role=role,
        authorisation_reference="SYNTH-AUTH-0001",
        authorisation_valid_until=valid_until or (clock.today() + dt.timedelta(days=30)),
    )


class TestAccess:
    def test_an_anonymous_visitor_is_sent_to_the_login_page(self, client, case):
        response = client.get(detail_url(case))
        assert response.status_code == 302
        assert "login" in response["Location"]

    def test_the_owner_opens_their_own_file(self, client, owner, case):
        client.force_login(owner)
        response = client.get(detail_url(case))
        assert response.status_code == 200
        assert case.reference in response.content.decode()

    def test_a_stranger_gets_the_same_answer_as_for_a_reference_that_does_not_exist(
        self, client, stranger, case
    ):
        client.force_login(stranger)
        theirs = client.get(detail_url(case))
        invented = client.get(f"{INDEX}ZZZZZZZZZZ/")
        assert theirs.status_code == 404
        assert invented.status_code == theirs.status_code

    def test_a_stranger_never_sees_the_content(self, client, stranger, case):
        client.force_login(stranger)
        body = client.get(detail_url(case)).content.decode()
        assert "Passeport en cours de validité" not in body

    def test_the_pages_are_never_indexed(self, client, owner, case):
        client.force_login(owner)
        for path in (INDEX, detail_url(case)):
            response = client.get(path)
            assert "noindex" in response["X-Robots-Tag"].lower(), path
            assert "no-store" in response["Cache-Control"], path


class TestTheAssigneeWorkspace:
    def test_a_live_mandate_opens_the_file(self, client, professional, case):
        assign(case, professional)
        client.force_login(professional)
        assert client.get(detail_url(case)).status_code == 200

    def test_the_page_says_the_file_is_not_theirs(self, client, professional, case):
        assign(case, professional)
        client.force_login(professional)
        body = client.get(detail_url(case)).content.decode()
        assert "mandat" in body.lower()

    def test_a_lapsed_mandate_closes_it_again(self, client, professional, case):
        assign(case, professional, valid_until=clock.today() - dt.timedelta(days=1))
        client.force_login(professional)
        assert client.get(detail_url(case)).status_code == 404

    def test_a_revoked_mandate_closes_it_again(self, client, professional, case):
        assignment = assign(case, professional)
        services.revoke_assignment(assignment)
        client.force_login(professional)
        assert client.get(detail_url(case)).status_code == 404

    def test_the_list_and_the_detail_agree_for_the_assignee(self, client, professional, case):
        """A row in the list must be openable; a row that is not listed must not be."""
        client.force_login(professional)
        assert case.reference not in client.get(INDEX).content.decode()
        assert client.get(detail_url(case)).status_code == 404

        assign(case, professional)
        assert case.reference in client.get(INDEX).content.decode()
        assert client.get(detail_url(case)).status_code == 200


class TestTheChecklist:
    def test_the_person_may_advance_their_own_requirement(self, client, owner, case):
        item = case.checklist.get(responsible_actor=ResponsibleActor.PERSON)
        client.force_login(owner)
        response = client.post(f"{detail_url(case)}ligne/{item.pk}/", {"status": ChecklistStatus.DONE})
        assert response.status_code == 302
        item.refresh_from_db()
        assert item.status == ChecklistStatus.DONE

    def test_the_person_may_not_attest_what_an_authority_does(self, client, owner, case):
        """Marking "the consulate has issued the document" is not something the applicant can attest."""
        item = case.checklist.get(responsible_actor=ResponsibleActor.AUTHORITY)
        client.force_login(owner)
        response = client.post(f"{detail_url(case)}ligne/{item.pk}/", {"status": ChecklistStatus.DONE})
        assert response.status_code == 403
        item.refresh_from_db()
        assert item.status == ChecklistStatus.PENDING

    def test_the_control_is_not_offered_for_a_line_the_person_may_not_change(self, client, owner, case):
        item = case.checklist.get(responsible_actor=ResponsibleActor.AUTHORITY)
        client.force_login(owner)
        body = client.get(detail_url(case)).content.decode()
        assert f"ligne/{item.pk}/" not in body

    def test_a_stranger_cannot_advance_a_line(self, client, stranger, case):
        item = case.checklist.first()
        client.force_login(stranger)
        assert client.post(f"{detail_url(case)}ligne/{item.pk}/", {"status": "done"}).status_code == 404

    def test_an_unknown_status_is_refused(self, client, owner, case):
        item = case.checklist.get(responsible_actor=ResponsibleActor.PERSON)
        client.force_login(owner)
        client.post(f"{detail_url(case)}ligne/{item.pk}/", {"status": "fait-je-crois"})
        item.refresh_from_db()
        assert item.status == ChecklistStatus.PENDING

    def test_the_source_of_a_requirement_is_shown(self, client, owner, case):
        client.force_login(owner)
        assert "Reg. (CE) n. 810/2009, art. 12" in client.get(detail_url(case)).content.decode()

    def test_the_responsible_actor_is_shown_for_every_line(self, client, owner, case):
        client.force_login(owner)
        body = client.get(detail_url(case)).content.decode()
        assert str(ResponsibleActor.AUTHORITY.label) in body
        assert str(ResponsibleActor.PERSON.label) in body


class TestTransitions:
    def test_only_permitted_transitions_are_offered(self, client, owner, case):
        from cases.models import transitions_from

        client.force_login(owner)
        body = client.get(detail_url(case)).content.decode()
        offered = {value for value in CaseStatus.values if f'value="{value}"' in body}
        assert offered <= set(transitions_from(case.status))

    def test_a_transition_the_table_forbids_is_refused(self, client, owner, case):
        """
        A draft cannot jump to "entered in Italy".

        CLOSED and SUSPENDED are deliberately reachable from every active state — a person may
        withdraw or pause their own file at any point — so the forbidden transition to assert is one
        that skips the sequence, which is what the table exists to prevent.
        """
        assert case.status == CaseStatus.DRAFT
        client.force_login(owner)
        client.post(f"{detail_url(case)}etat/", {"status": CaseStatus.ENTERED})
        case.refresh_from_db()
        assert case.status == CaseStatus.DRAFT

    def test_closing_is_reachable_from_any_active_state(self, client, owner, case):
        """The universal exit. A person may always withdraw their own file."""
        client.force_login(owner)
        client.post(f"{detail_url(case)}etat/", {"status": CaseStatus.CLOSED})
        case.refresh_from_db()
        assert case.status == CaseStatus.CLOSED

    def test_a_closed_file_does_not_reopen(self, client, owner, case):
        client.force_login(owner)
        client.post(f"{detail_url(case)}etat/", {"status": CaseStatus.CLOSED})
        client.post(f"{detail_url(case)}etat/", {"status": CaseStatus.ORIENTED})
        case.refresh_from_db()
        assert case.status == CaseStatus.CLOSED

    def test_a_suspension_without_a_reason_is_refused(self, client, owner, case):
        services.transition(case, CaseStatus.ORIENTED)
        client.force_login(owner)
        client.post(f"{detail_url(case)}etat/", {"status": CaseStatus.SUSPENDED, "reason": ""})
        case.refresh_from_db()
        assert case.status != CaseStatus.SUSPENDED

    def test_a_stranger_cannot_move_the_state(self, client, stranger, case):
        client.force_login(stranger)
        assert client.post(f"{detail_url(case)}etat/", {"status": CaseStatus.ORIENTED}).status_code == 404

    def test_every_transition_is_audited(self, client, owner, case):
        """
        A move the person may make (CASE_LIFECYCLE.md §4: «qualunque attivo → SUSPENDED: persona…») leaves its event.

        DRAFT → ORIENTED used to stand here, made by the owner — but §4 gives it to the system alone (the orientation
        service), and since finding F-7 the domain refuses it to the person (``test_transition_actors``).
        """
        from audit.models import AuditEvent

        client.force_login(owner)
        client.post(f"{detail_url(case)}etat/", {"status": CaseStatus.SUSPENDED, "reason": "En attente du passeport"})
        event = AuditEvent.objects.get(action="case.transition", target_id=str(case.pk))
        assert (event.metadata["from"], event.metadata["to"]) == (CaseStatus.DRAFT, CaseStatus.SUSPENDED)
        assert event.metadata["reason"] == "En attente du passeport" and event.actor_id == owner.pk


class TestTheEmptyState:
    def test_a_person_with_no_file_is_told_how_one_comes_to_exist(self, client, stranger):
        client.force_login(stranger)
        body = client.get(INDEX).content.decode()
        assert "questionnaire" in body.lower()
        assert CaseFile.objects.filter(person=stranger).count() == 0
