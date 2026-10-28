"""
The rule editor asks ``rules.policies`` — the platform's own answer — before anything moves (finding F-8, review F8R-1).

``rules.policies``: «submit» a drafter's (role:legal_editor, role:administrator), never for a rule in force; «approve»
role:legal_approver's and never the author's; «activate» / «retire» role:legal_approver's; «change» a drafter's, never
for a rule in force; «new_version» a drafter's. PERMISSION_MODEL §2.1 gives the administrator «rules: view» only, and
the legal editor «Redige, non approva». The back office's workflow actions were declared without ``permissions`` and
called ``rules.services.transition``, which checks the four-eyes author rule only: through the rule list a view-only
administrator approved and put a rule in force, and a legal editor approved another editor's rule — the separation of
duties (Technical Blueprint §4) defeated from the back office. Each DENY below failed before the fix; each ALLOW holds
that the workflow still works for the role the policy names.

Accounts are this module's own, created with a test-only password and signed in through minted sessions
(``Client.force_login``); ``roles.ensure_roles()`` gives the roles their model permissions as the production seed does.
"""

from __future__ import annotations

import datetime as dt

import pytest
from django.contrib import admin
from django.contrib.messages import get_messages
from django.test import RequestFactory

from accounts import roles
from audit.models import AuditEvent
from rules import services
from rules.models import LegalRule, LegalSource, ReviewStatus, RuleEffect

pytestmark = [pytest.mark.django_db, pytest.mark.security]

PASSWORD = "Local-Only-F8R1-2026!"
RULES = "/backoffice/rules/legalrule/"
SOURCES = "/backoffice/rules/legalsource/"
WORKFLOW = {"action_submit_for_review", "action_approve", "action_activate", "action_retire"}


@pytest.fixture
def cast(django_user_model):
    roles.ensure_roles()

    def make(key, role=None, **extra):
        user = django_user_model.objects.create_user(email=f"f8r1.{key}@example.test", password=PASSWORD, **extra)
        if role:
            roles.assign_role(user, role)
        return user

    return {
        "editor": make("editor", roles.LEGAL_EDITOR, is_staff=True),
        "author": make("author", roles.LEGAL_EDITOR, is_staff=True),
        "approver": make("approver", roles.LEGAL_APPROVER, is_staff=True),
        "administrator": make("administrator", roles.ADMINISTRATOR, is_staff=True),
        "staff": make("staff", roles.STAFF, is_staff=True),
        "superuser": django_user_model.objects.create_superuser(email="f8r1.super@example.test", password=PASSWORD),
    }


@pytest.fixture
def source(db):
    return LegalSource.objects.create(
        key="f8r1-source",
        title_fr="Source F8R1",
        reference="D.Lgs. 286/1998, art. 22",
        authority="Repubblica Italiana",
        url="https://www.normattiva.it/",
        consulted_on=dt.date(2026, 9, 21),
        consulted_by="Referente giuridico",
    )


def _rule(cast, source, status: str, *, rule_id="R-F8R1-001", by="author") -> LegalRule:
    """A rule written by ``by``, walked to ``status`` through the declared chain (the approval by the approver)."""
    rule = LegalRule.objects.create(
        rule_id=rule_id,
        version=1,
        pathway="salaried_work",
        condition={},
        effect=RuleEffect.WARNING,
        message_key="rules.f8r1",
        message_fr="F8R1 message d'origine",
        valid_from=dt.date(2026, 1, 1),
        created_by=cast[by],
    )
    rule.sources.add(source)
    chain = [ReviewStatus.SOURCE_VERIFIED, ReviewStatus.LEGAL_REVIEW, ReviewStatus.APPROVED, ReviewStatus.ACTIVE]
    for step in chain[: chain.index(status) + 1] if status in chain else []:
        actor = cast["approver"] if step in {ReviewStatus.APPROVED, ReviewStatus.ACTIVE} else cast[by]
        services.transition(rule, step, actor=actor)
    rule.refresh_from_db()
    assert rule.review_status == status
    return rule


def _act(client, action: str, rule: LegalRule):
    return client.post(RULES, {"action": action, "_selected_action": [str(rule.pk)], "index": "0"})


def _offered(user) -> set[str]:
    request = RequestFactory().get(RULES)
    request.user = user
    return set(admin.site._registry[LegalRule].get_actions(request)) & WORKFLOW


def _status(rule: LegalRule) -> str:
    rule.refresh_from_db()
    return rule.review_status


#: (action, the state it starts from, the state it would reach)
MOVES = [
    ("action_submit_for_review", ReviewStatus.SOURCE_VERIFIED, ReviewStatus.LEGAL_REVIEW),
    ("action_approve", ReviewStatus.LEGAL_REVIEW, ReviewStatus.APPROVED),
    ("action_activate", ReviewStatus.APPROVED, ReviewStatus.ACTIVE),
    ("action_retire", ReviewStatus.ACTIVE, ReviewStatus.RETIRED),
]


# =================================================================================================
# DENY — the back office moves no rule the policy does not let the account move
# =================================================================================================
class TestNobodyMovesARuleThePolicyKeeps:
    def test_the_view_only_administrator_is_offered_no_workflow_action(self, cast):
        assert _offered(cast["administrator"]) == set(), "F8R-1: a view grant was offered every workflow action"

    @pytest.mark.parametrize("action,start,target", MOVES, ids=[m[0] for m in MOVES])
    def test_the_view_only_administrator_moves_no_rule(self, client, cast, source, action, start, target):
        rule = _rule(cast, source, start)
        client.force_login(cast["administrator"])
        _act(client, action, rule)
        assert _status(rule) == start, f"F8R-1: the administrator (rules: view) ran {action}"

    def test_a_legal_editor_is_offered_submission_only(self, cast):
        assert _offered(cast["editor"]) == {"action_submit_for_review"}

    @pytest.mark.parametrize("action,start,target", MOVES[1:], ids=[m[0] for m in MOVES[1:]])
    def test_a_legal_editor_neither_approves_nor_puts_in_force_nor_retires(
        self, client, cast, source, action, start, target
    ):
        rule = _rule(cast, source, start)  # another editor's rule: the four-eyes rule alone would let this through
        client.force_login(cast["editor"])
        _act(client, action, rule)
        assert _status(rule) == start, f"F8R-1: a legal editor ran {action} on another editor's rule"

    def test_the_legal_approver_does_not_submit_for_review(self, client, cast, source):
        rule = _rule(cast, source, ReviewStatus.SOURCE_VERIFIED)
        assert "action_submit_for_review" not in _offered(cast["approver"])
        client.force_login(cast["approver"])
        _act(client, "action_submit_for_review", rule)
        assert _status(rule) == ReviewStatus.SOURCE_VERIFIED

    def test_the_approver_never_approves_a_rule_it_wrote_and_is_told_why(self, client, cast, source):
        rule = _rule(cast, source, ReviewStatus.LEGAL_REVIEW)
        LegalRule.objects.filter(pk=rule.pk).update(created_by=cast["approver"])
        client.force_login(cast["approver"])
        response = _act(client, "action_approve", rule)
        assert _status(rule) == ReviewStatus.LEGAL_REVIEW, "four eyes: the author approved its own rule"
        errors = [str(m) for m in get_messages(response.wsgi_request) if m.level_tag == "error"]
        assert errors and rule.rule_id in errors[0]

    def test_a_refused_action_records_no_transition(self, client, cast, source):
        rule = _rule(cast, source, ReviewStatus.LEGAL_REVIEW)
        transitions = AuditEvent.objects.filter(action="rule.transition")
        before = transitions.count()
        for who in ("administrator", "editor"):
            client.force_login(cast[who])
            _act(client, "action_approve", rule)
        assert transitions.count() == before


class TestTheTextARuleSaysIsTheDraftersOnly:
    def test_the_legal_approver_reads_a_rule_and_cannot_rewrite_it(self, client, cast, source):
        rule = _rule(cast, source, ReviewStatus.LEGAL_REVIEW)
        client.force_login(cast["approver"])
        page = client.get(f"{RULES}{rule.pk}/change/")
        assert page.status_code == 200
        assert 'name="message_fr"' not in page.content.decode("utf-8"), "F8R-1: the approver edits the text it approves"
        posted = client.post(f"{RULES}{rule.pk}/change/", {"message_fr": "Réécrit par l'approbateur"})
        assert posted.status_code == 403
        rule.refresh_from_db()
        assert rule.message_fr == "F8R1 message d'origine"

    def test_the_legal_approver_cannot_rewrite_a_source(self, client, cast, source):
        client.force_login(cast["approver"])
        page = client.get(f"{SOURCES}{source.pk}/change/")
        assert page.status_code == 200 and 'name="reference"' not in page.content.decode("utf-8")
        assert client.post(f"{SOURCES}{source.pk}/change/", {"reference": "Autre"}).status_code == 403
        source.refresh_from_db()
        assert source.reference == "D.Lgs. 286/1998, art. 22"

    def test_the_view_only_administrator_writes_no_new_version(self, client, cast, source):
        rule = _rule(cast, source, ReviewStatus.ACTIVE)
        client.force_login(cast["administrator"])
        response = client.post(f"{RULES}{rule.pk}/new-version/")
        assert response.status_code == 403, "F8R-1: a view grant wrote a new version"
        assert LegalRule.objects.filter(rule_id=rule.rule_id).count() == 1

    def test_a_role_without_the_rules_screens_reads_neither_the_diff_nor_the_preview(self, client, cast, source):
        rule = _rule(cast, source, ReviewStatus.LEGAL_REVIEW)
        client.force_login(cast["staff"])
        assert client.get(RULES).status_code == 403
        for page in ("diff", "preview"):
            assert client.get(f"{RULES}{rule.pk}/{page}/").status_code == 403, page


# =================================================================================================
# ALLOW — the workflow still works for the roles the policy names
# =================================================================================================
class TestTheWorkflowStillWorks:
    def test_the_legal_approver_approves_puts_in_force_and_retires(self, client, cast, source):
        rule = _rule(cast, source, ReviewStatus.LEGAL_REVIEW)
        assert _offered(cast["approver"]) == {"action_approve", "action_activate", "action_retire"}
        transitions = AuditEvent.objects.filter(action="rule.transition", actor=cast["approver"])
        client.force_login(cast["approver"])
        _act(client, "action_approve", rule)
        assert _status(rule) == ReviewStatus.APPROVED
        rule.refresh_from_db()
        assert rule.approved_by == cast["approver"]
        _act(client, "action_activate", rule)
        assert _status(rule) == ReviewStatus.ACTIVE
        _act(client, "action_retire", rule)
        assert _status(rule) == ReviewStatus.RETIRED
        assert transitions.count() == 3, "each move recorded, naming the approver"

    def test_a_legal_editor_submits_for_review_edits_a_draft_and_opens_a_new_version(self, client, cast, source):
        verified = _rule(cast, source, ReviewStatus.SOURCE_VERIFIED, by="editor")
        client.force_login(cast["editor"])
        _act(client, "action_submit_for_review", verified)
        assert _status(verified) == ReviewStatus.LEGAL_REVIEW
        draft = _rule(cast, source, ReviewStatus.DRAFT, rule_id="R-F8R1-002", by="editor")
        assert 'name="message_fr"' in client.get(f"{RULES}{draft.pk}/change/").content.decode("utf-8")
        in_force = _rule(cast, source, ReviewStatus.ACTIVE, rule_id="R-F8R1-003")
        response = client.post(f"{RULES}{in_force.pk}/new-version/")
        assert response.status_code == 302
        assert LegalRule.objects.filter(rule_id="R-F8R1-003", version=2, review_status=ReviewStatus.DRAFT).exists()

    def test_the_administrator_still_reads_every_rule_and_its_preview(self, client, cast, source):
        rule = _rule(cast, source, ReviewStatus.LEGAL_REVIEW)
        client.force_login(cast["administrator"])
        assert client.get(RULES).status_code == 200
        assert client.get(f"{RULES}{rule.pk}/change/").status_code == 200
        assert client.get(f"{RULES}{rule.pk}/preview/").status_code == 200
        assert client.get(f"{RULES}{rule.pk}/diff/").status_code == 200

    def test_a_superuser_is_offered_every_action_and_the_service_keeps_its_refusals(self, client, cast, source):
        assert _offered(cast["superuser"]) == WORKFLOW
        approved = _rule(cast, source, ReviewStatus.APPROVED)
        approved.sources.clear()
        client.force_login(cast["superuser"])
        _act(client, "action_activate", approved)
        assert _status(approved) == ReviewStatus.APPROVED, "the service still refuses a rule in force without a source"
