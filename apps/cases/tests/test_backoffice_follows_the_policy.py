"""
F-8 — the back office reads and changes a case file only as the platform's own authorisation allows.

Found by sec-f7's review and GitHub checkpoint #3's adversary (docs/design-v5/QA/v54/sec-f8/NOTES.md §1.1): the case
file's screens had no queryset limit, so role:operator — which holds the «cases» view and change model permissions
(``accounts.roles.ROLE_PERMISSIONS``, seeded in production by ``seed_all``) — listed and opened every file in the back
office, read every assignment and every assessment (the person's answers), changed any file's purpose and pathway and
any line of its checklist, CLOSED files included, and a line's status changed there wrote no ``case.checklist.status``
event. On the platform the same account reads its own file and the files it holds a LIVE assignment on
(``CaseFileQuerySet.readable_by``), and PERMISSION_MODEL §5.1 says «assigned».

Every screen is driven through the back office's own pages with a minted session (``Client.force_login``); the accounts
are this module's, with a test-only password. ``roles.ensure_roles()`` gives the roles their model permissions as the
production seed does — the operator reaches the back office with the staff flag, as staff accounts are made.
"""

from __future__ import annotations

import datetime as dt
from html.parser import HTMLParser

import pytest

from accounts import roles
from accounts.permissions import can
from audit.models import AuditEvent
from cases import services
from cases.models import (
    AssignmentRole,
    CaseFile,
    CasePurpose,
    CaseStatus,
    ChecklistStatus,
    PathwayAssessment,
    ResponsibleActor,
)
from core import clock

pytestmark = [pytest.mark.django_db, pytest.mark.security]

PASSWORD = "Local-Only-F8-2026!"
BACKOFFICE = "/backoffice/cases/"
FILES = f"{BACKOFFICE}casefile/"
ASSIGNMENTS = f"{BACKOFFICE}caseassignment/"
ASSESSMENTS = f"{BACKOFFICE}pathwayassessment/"
AUTOCOMPLETE = "/backoffice/autocomplete/"


class _AdminForm(HTMLParser):
    """An admin change form's fields as a browser submits them: inputs, checked boxes, selects, textareas."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.data: dict[str, list[str]] = {}
        self._inside = False
        self._select: str | None = None
        self._chosen: list[str] = []
        self._textarea: str | None = None
        self._text = ""

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "form" and (attributes.get("id") or "").endswith("_form"):
            self._inside = True
        name = attributes.get("name")
        if not self._inside or (tag != "option" and not name):
            return
        if tag == "input":
            kind = (attributes.get("type") or "text").lower()
            if kind in ("submit", "button", "image", "file", "reset"):
                return
            if kind in ("checkbox", "radio") and "checked" not in attributes:
                return
            self.data.setdefault(name, []).append(attributes.get("value") or ("on" if kind == "checkbox" else ""))
        elif tag == "select":
            self._select, self._chosen = name, []
        elif tag == "option" and self._select is not None and "selected" in attributes:
            self._chosen.append(attributes.get("value") or "")
        elif tag == "textarea":
            self._textarea, self._text = name, ""

    def handle_data(self, data):
        if self._textarea is not None:
            self._text += data

    def handle_endtag(self, tag):
        if tag == "select" and self._select is not None:
            self.data[self._select] = self._chosen or [""]
            self._select = None
        elif tag == "textarea" and self._textarea is not None:
            self.data.setdefault(self._textarea, []).append(self._text.lstrip("\n"))
            self._textarea = None
        elif tag == "form":
            self._inside = False


def _form_of(page) -> dict:
    form = _AdminForm()
    form.feed(page.content.decode("utf-8"))
    return {name: values if len(values) != 1 else values[0] for name, values in form.data.items()}


def _admin_post(client, path: str, changes: dict):
    """Fetch an admin change form, change some of its fields as a browser would, post it back."""
    page = client.get(path)
    assert page.status_code == 200, (path, page.status_code)
    data = _form_of(page)
    data.update(changes)
    data["_save"] = "Save"
    return client.post(path, data)


def _line_index(client, case, item) -> int:
    """The checklist inline's form index of ``item`` on ``case``'s change page."""
    data = _form_of(client.get(f"{FILES}{case.pk}/change/"))
    for key, value in data.items():
        if key.startswith("checklist-") and key.endswith("-id") and str(value) == str(item.pk):
            return int(key.split("-")[1])
    raise AssertionError(f"line {item.pk} is not on the page")


def _not_found(response) -> bool:
    """Django's admin answers an object outside its queryset as it answers an id never issued: back to the index."""
    return response.status_code == 302 and response["Location"].rstrip("/").endswith("/backoffice")


def _put(case, status):
    """Test set-up only: place the file in ``status`` without walking the graph."""
    CaseFile.objects.filter(pk=case.pk).update(status=status, status_since=clock.now())
    case.refresh_from_db()
    return case


@pytest.fixture
def people(django_user_model):
    roles.ensure_roles()

    def make(email, role=None, **extra):
        user = django_user_model.objects.create_user(email=email, password=PASSWORD, **extra)
        if role:
            roles.assign_role(user, role)
        return user

    return {
        "owner": make("f8.owner@example.test", roles.PERSON),
        "other_owner": make("f8.other.owner@example.test", roles.PERSON),
        "operator": make("f8.operator@example.test", roles.OPERATOR, is_staff=True),
        "colleague": make("f8.colleague@example.test", roles.OPERATOR, is_staff=True),
        "administrator": make("f8.administrator@example.test", roles.ADMINISTRATOR, is_staff=True),
        "superuser": django_user_model.objects.create_superuser(email="f8.super@example.test", password=PASSWORD),
    }


@pytest.fixture
def files(people):
    """The operator's file — it holds a live OPERATOR assignment on it — and another person's file it has nothing to
    do with, assigned to a colleague. Each carries a checklist line, and the other one an assessment."""
    mine = services.open_case(people["owner"], purpose=CasePurpose.WORK, pathway_key="salaried_work")
    theirs = services.open_case(people["other_owner"], purpose=CasePurpose.STUDY, pathway_key="study_in_italy")
    own_assignment = services.assign(mine, people["operator"], role=AssignmentRole.OPERATOR)
    foreign_assignment = services.assign(theirs, people["colleague"], role=AssignmentRole.OPERATOR)
    my_line = services.add_checklist_item(
        mine, requirement="Contrat de travail signé", responsible_actor=ResponsibleActor.COMPANY
    )
    their_line = services.add_checklist_item(
        theirs, requirement="Lettre d'admission", responsible_actor=ResponsibleActor.PERSON
    )
    their_assessment = services.record_assessment(
        theirs,
        outcome="possible",
        ruleset_version=1,
        ruleset_snapshot={"rules": []},
        answers={"family_situation": "F8-SYNTHETIC-ANSWER"},
    )
    return {
        "mine": mine,
        "theirs": theirs,
        "own_assignment": own_assignment,
        "foreign_assignment": foreign_assignment,
        "my_line": my_line,
        "their_line": their_line,
        "their_assessment": their_assessment,
    }


# ---------------------------------------------------------------------------------------------
# F-8, reproduced: the operator reads every file in the back office
# ---------------------------------------------------------------------------------------------
class TestTheOperatorReadsOnlyWhatThePlatformLetsItRead:
    def test_the_list_holds_its_assigned_file_and_not_another(self, client, people, files):
        client.force_login(people["operator"])
        body = client.get(FILES).content.decode("utf-8")
        assert files["mine"].reference in body
        assert files["theirs"].reference not in body, "F-8: an unassigned file is listed"

    def test_an_unassigned_file_does_not_open(self, client, people, files):
        client.force_login(people["operator"])
        response = client.get(f"{FILES}{files['theirs'].pk}/change/")
        assert _not_found(response), "F-8: the operator opens a file it holds no assignment on"
        assert people["other_owner"].email not in response.content.decode("utf-8")

    def test_a_search_does_not_find_an_unassigned_file(self, client, people, files):
        """Searched by its reference or by its owner's address: no row (the search box echoes the term itself, so the
        result is read from the rows — their links — and from the count the page reports)."""
        client.force_login(people["operator"])
        for term in (files["theirs"].reference, people["other_owner"].email):
            response = client.get(FILES, {"q": term})
            assert f"{FILES}{files['theirs'].pk}/change/" not in response.content.decode("utf-8"), term
            assert response.context["cl"].result_count == 0, term
        response = client.get(FILES, {"q": files["mine"].reference})
        assert response.context["cl"].result_count == 1, "the search still finds the operator's own file"

    def test_the_autocomplete_enumerates_no_file(self, client, people, files):
        """Django checks the TARGET screen's view permission, which the operator holds: through the assignment's
        ``case`` autocomplete it read every file's reference."""
        client.force_login(people["operator"])
        response = client.get(
            AUTOCOMPLETE, {"app_label": "cases", "model_name": "caseassignment", "field_name": "case", "term": ""}
        )
        assert response.status_code == 200
        ids = {row["id"] for row in response.json()["results"]}
        assert str(files["theirs"].pk) not in ids, "F-8: the autocomplete lists an unassigned file"
        assert str(files["mine"].pk) in ids

    def test_it_reads_its_own_assignment_and_no_other(self, client, people, files):
        client.force_login(people["operator"])
        body = client.get(ASSIGNMENTS).content.decode("utf-8")
        assert f"{ASSIGNMENTS}{files['own_assignment'].pk}/change/" in body
        assert f"{ASSIGNMENTS}{files['foreign_assignment'].pk}/change/" not in body, "F-8: another file's assignment"
        assert _not_found(client.get(f"{ASSIGNMENTS}{files['foreign_assignment'].pk}/change/"))

    def test_it_reads_no_assessment_of_a_file_it_may_not_read(self, client, people, files):
        client.force_login(people["operator"])
        assessment = files["their_assessment"]
        assert f"{ASSESSMENTS}{assessment.pk}/change/" not in client.get(ASSESSMENTS).content.decode("utf-8")
        response = client.get(f"{ASSESSMENTS}{assessment.pk}/change/")
        assert _not_found(response), "F-8: the operator reads another person's answers"
        assert "F8-SYNTHETIC-ANSWER" not in response.content.decode("utf-8")

    def test_an_assignment_that_has_ended_reads_nothing_there(self, client, people, files):
        """A revoked or expired mandate stops listing the file the same day, in the back office as on the platform."""
        services.revoke_assignment(files["own_assignment"])
        client.force_login(people["operator"])
        assert files["mine"].reference not in client.get(FILES).content.decode("utf-8")
        assert _not_found(client.get(f"{FILES}{files['mine'].pk}/change/"))

    def test_every_page_of_an_unassigned_file_answers_as_an_id_never_issued(self, client, people, files):
        """No enumeration: its form, its history (the LogEntry trail of who changed what) and its delete confirmation
        (the cascade's list) answer exactly as for a file that does not exist — Django checks the delete permission
        before it looks the object up, so that page is the same 403 for every id."""
        client.force_login(people["operator"])
        never = CaseFile.objects.order_by("-pk").first().pk + 1000
        for page in ("change", "history", "delete"):
            theirs = client.get(f"{FILES}{files['theirs'].pk}/{page}/")
            nobody = client.get(f"{FILES}{never}/{page}/")
            assert theirs.status_code != 200, page
            assert (theirs.status_code, theirs.get("Location")) == (nobody.status_code, nobody.get("Location")), page
        client.post(f"{FILES}{files['theirs'].pk}/delete/", {"post": "yes"})
        assert CaseFile.objects.filter(pk=files["theirs"].pk).exists()

    def test_the_operator_deletes_no_file_not_even_its_own(self, client, people, files):
        """No role holds ``cases.delete_*``: the operator's assigned file opens, its deletion does not."""
        client.force_login(people["operator"])
        assert client.get(f"{FILES}{files['mine'].pk}/delete/").status_code == 403
        assert client.post(f"{FILES}{files['mine'].pk}/delete/", {"post": "yes"}).status_code == 403
        assert "delete_selected" not in client.get(FILES).content.decode("utf-8")
        assert CaseFile.objects.filter(pk=files["mine"].pk).exists()

    def test_an_expired_authorisation_reads_nothing_there(self, client, people, files):
        type(files["own_assignment"]).objects.filter(pk=files["own_assignment"].pk).update(
            authorisation_valid_until=clock.today() - dt.timedelta(days=1)
        )
        client.force_login(people["operator"])
        assert _not_found(client.get(f"{FILES}{files['mine'].pk}/change/"))


# ---------------------------------------------------------------------------------------------
# What only the domain writes, and the checklist's statuses
# ---------------------------------------------------------------------------------------------
class TestWhatTheBackOfficeMayChange:
    def test_the_purpose_and_the_pathway_are_the_domains(self, client, people, files):
        """The orientation writes them (``cases.intake``): the pathway is what the rule engine evaluates at the next
        reassessment, the purpose what keeps one active file per purpose."""
        case = files["mine"]
        client.force_login(people["superuser"])
        _admin_post(client, f"{FILES}{case.pk}/change/", {"purpose": CasePurpose.FAMILY, "pathway_key": "invented"})
        case.refresh_from_db()
        assert (case.purpose, case.pathway_key) == (CasePurpose.WORK, "salaried_work")

    def test_a_lines_status_changed_there_is_recorded_by_the_domain(self, client, people, files):
        case, line = files["mine"], files["my_line"]
        client.force_login(people["operator"])
        index = _line_index(client, case, line)
        response = _admin_post(client, f"{FILES}{case.pk}/change/", {f"checklist-{index}-status": ChecklistStatus.DONE})
        assert response.status_code == 302, response.content.decode("utf-8")[:2000]
        line.refresh_from_db()
        assert line.status == ChecklistStatus.DONE
        event = AuditEvent.objects.filter(action="case.checklist.status", target_id=str(case.pk)).get()
        assert event.actor_id == people["operator"].pk
        assert event.metadata == {"item": line.pk, "from": ChecklistStatus.PENDING, "to": ChecklistStatus.DONE}

    def test_a_lines_other_fields_still_save_and_an_unchanged_status_records_nothing(self, client, people, files):
        case, line = files["mine"], files["my_line"]
        client.force_login(people["operator"])
        index = _line_index(client, case, line)
        response = _admin_post(client, f"{FILES}{case.pk}/change/", {f"checklist-{index}-due_date": "2026-12-01"})
        assert response.status_code == 302
        line.refresh_from_db()
        assert line.due_date == dt.date(2026, 12, 1)
        assert not AuditEvent.objects.filter(action="case.checklist.status").exists()

    def test_who_is_responsible_for_a_line_is_not_rewritten_there(self, client, people, files):
        """«Who is responsible» decides who may tick the line (the person ticks PERSON lines only): an authority field
        (PERMISSION_MODEL §6 rule 5), handed out by nobody in the back office."""
        case, line = files["mine"], files["my_line"]
        client.force_login(people["operator"])
        index = _line_index(client, case, line)
        _admin_post(
            client, f"{FILES}{case.pk}/change/", {f"checklist-{index}-responsible_actor": ResponsibleActor.PERSON}
        )
        line.refresh_from_db()
        assert line.responsible_actor == ResponsibleActor.COMPANY

    def test_a_closed_files_lines_are_read_only_for_everybody(self, client, people, files):
        """§4 rule 5: «Un fascicolo CLOSED è in sola lettura» — a superuser included: no editable line on its page."""
        case, line = files["mine"], files["my_line"]
        _put(case, CaseStatus.CLOSED)
        client.force_login(people["superuser"])
        data = _form_of(client.get(f"{FILES}{case.pk}/change/"))
        assert not any(key.startswith("checklist-") and key.endswith("-status") for key in data), "an editable line"
        client.post(
            f"{FILES}{case.pk}/change/",
            {
                **data,
                "checklist-TOTAL_FORMS": "1",
                "checklist-INITIAL_FORMS": "1",
                "checklist-0-id": str(line.pk),
                "checklist-0-case": str(case.pk),
                "checklist-0-status": ChecklistStatus.DONE,
                "_save": "Save",
            },
        )
        line.refresh_from_db()
        assert line.status == ChecklistStatus.PENDING
        assert not AuditEvent.objects.filter(action="case.checklist.status").exists()

    def test_the_operator_changes_nothing_on_its_own_file_once_closed(self, client, people, files):
        case, line = _put(files["mine"], CaseStatus.CLOSED), files["my_line"]
        client.force_login(people["operator"])
        response = client.get(f"{FILES}{case.pk}/change/")
        assert response.status_code == 200, "a closed file it was assigned to still opens, read-only"
        assert not any(key.endswith("-status") for key in _form_of(response))
        assert client.post(f"{FILES}{case.pk}/change/", {"_save": "Save"}).status_code == 403
        line.refresh_from_db()
        assert line.status == ChecklistStatus.PENDING

    def test_an_operator_who_owns_a_file_does_not_act_on_it_there(self, client, people, files):
        """The back office is never where a person acts on their own file: the checklist policy lets an owner tick
        PERSON lines only, and on the platform."""
        own = services.open_case(people["operator"], purpose=CasePurpose.FAMILY, pathway_key="family")
        services.add_checklist_item(own, requirement="Acte de mariage", responsible_actor=ResponsibleActor.AUTHORITY)
        client.force_login(people["operator"])
        data = _form_of(client.get(f"{FILES}{own.pk}/change/"))
        assert not any(key.startswith("checklist-") and key.endswith("-status") for key in data)


# ---------------------------------------------------------------------------------------------
# The policies' administrator branch and CLOSED (§4 rule 5)
# ---------------------------------------------------------------------------------------------
class TestAClosedFileIsReadOnlyForTheAdministratorToo:
    def test_the_administrator_changes_neither_a_closed_file_nor_its_lines(self, people, files):
        case, line = _put(files["theirs"], CaseStatus.CLOSED), files["their_line"]
        administrator = people["administrator"]
        assert can(administrator, "view", case) and can(administrator, "view", line)
        assert not can(administrator, "change", case), "rule 5: a CLOSED file is read-only"
        assert not can(administrator, "change", line), "rule 5: its lines with it"

    def test_the_administrator_still_changes_an_active_file_and_deletes_a_closed_one(self, people, files):
        """Deletion is not a change of a read-only file: it is how retention ends one (the deliberate exception)."""
        administrator = people["administrator"]
        assert can(administrator, "change", files["theirs"]) and can(administrator, "change", files["their_line"])
        assert can(administrator, "delete", _put(files["theirs"], CaseStatus.CLOSED))


# ---------------------------------------------------------------------------------------------
# The legitimate work stays possible, and nobody is widened
# ---------------------------------------------------------------------------------------------
class TestTheLegitimateWorkStays:
    def test_the_operator_opens_and_works_on_its_assigned_file(self, client, people, files):
        client.force_login(people["operator"])
        response = client.get(f"{FILES}{files['mine'].pk}/change/")
        assert response.status_code == 200
        assert any(key.endswith("-status") for key in _form_of(response)), "its file's lines are editable"

    def test_a_superuser_reads_every_file(self, client, people, files):
        client.force_login(people["superuser"])
        body = client.get(FILES).content.decode("utf-8")
        assert files["mine"].reference in body and files["theirs"].reference in body
        assert client.get(f"{FILES}{files['theirs'].pk}/change/").status_code == 200

    def test_the_administrator_role_gains_no_case_screen(self, client, people, files):
        """role:administrator holds no «cases» model permission: it reads case files on the platform, and the fix
        widens nobody."""
        client.force_login(people["administrator"])
        assert client.get(FILES).status_code == 403
        assert client.get(ASSESSMENTS).status_code == 403

    def test_the_lists_count_only_readable_rows(self, people, files):
        """The queryset is the defence, so counts, pagination and every filter see the same rows (PERMISSION_MODEL
        §3.1) — never a list filtered after it was read."""
        from django.contrib import admin
        from django.test import RequestFactory

        from cases.models import CaseAssignment

        request = RequestFactory().get(FILES)
        request.user = people["operator"]
        assert list(admin.site._registry[CaseFile].get_queryset(request)) == [files["mine"]]
        assert list(admin.site._registry[CaseAssignment].get_queryset(request)) == [files["own_assignment"]]
        assert not admin.site._registry[PathwayAssessment].get_queryset(request).exists()
        request.user = people["superuser"]
        assert admin.site._registry[CaseFile].get_queryset(request).count() == CaseFile.objects.count()
