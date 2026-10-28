"""
F-8 — every back-office screen that shows or changes personal data grants no more than the platform's own rules.

The audit of docs/design-v5/QA/v54/sec-f8/NOTES.md §1 crossed every ModelAdmin and inline registered on the back office
with ``accounts.roles.ROLE_PERMISSIONS`` (which grants by APPLICATION) and with the policies of ``accounts.permissions``
(which judge per row, per role). Beside the case file (``apps/cases/tests/test_backoffice_follows_the_policy.py``) it
found a role reading or changing in the back office what its platform policy forbids on these screens — each reproduced
here, then held:

* the help desk: role:operator read the shape of every request, which ``helpdesk.policies`` lets it dispatch and never
  view;
* the public submissions: role:operator read, changed, exported and anonymised every one, which ``enquiries.policies``
  never names it for; the administrator hard-deleted one, which the policy grants nobody;
* the virtual forum: role:staff moderated, and read every membership, hidden post and report — ``community.policies``
  names the moderators: role:moderator, role:administrator, role:superadmin;
* the Forum's governance module: role:staff read every profile, proposal and mandate and granted mandates —
  ``forum.governance_policies`` gives the module without a profile to the administrator alone;
* the notifications: role:operator read every message's content (``portal.policies`` names staff and administration);
  view-only accounts read every mail's body, a newsletter confirmation's bearer link included, and resent or cancelled
  mail; ``resend``, ``cancel`` were offered on a view grant;
* the consents: view-only role:staff recorded the withdrawal of anyone's consent; a subscription's bearer tokens were
  displayed and its evidence editable;
* the audit trail: role:legal_approver read every event (AUDIT_MODEL §6.1: «tutti gli altri ruoli: nessun accesso»);
* the orientation: the administrator read every questionnaire's answers (``orientation.policies``: the owner's only);
* the integrations' outbound events: view-only, the administrator requeued and cancelled them.

And the owner's V5.10 list, each with its DENY and its ALLOW: documents (object-level access, no unrelated document,
the protected download), accounts and person data (no broad staff visibility), selection, companies and the Academy (no
role but the superuser), the back office's sensitive changes recorded in the audit trail.

Accounts are this module's own, created with a test-only password and signed in through minted sessions
(``Client.force_login``); ``roles.ensure_roles()`` gives the roles their model permissions as the production seed does.
"""

from __future__ import annotations

import pytest
from django.contrib import admin
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory

from accounts import roles
from audit.models import AuditEvent
from cases import services as case_services
from cases.models import CasePurpose

pytestmark = [pytest.mark.django_db, pytest.mark.security]

PASSWORD = "Local-Only-F8-2026!"
BO = "/backoffice/"

#: Every back-office role but the administrator, each with the staff flag that opens the back office.
STAFF_ROLES = {
    "operator": roles.OPERATOR,
    "staff": roles.STAFF,
    "moderator": roles.MODERATOR,
    "content_editor": roles.CONTENT_EDITOR,
    "legal_editor": roles.LEGAL_EDITOR,
    "legal_approver": roles.LEGAL_APPROVER,
}


def _not_found(response) -> bool:
    """Django's admin answers an object outside its queryset as it answers an id never issued: back to the index."""
    return response.status_code == 302 and response["Location"] == BO


def _action(client, changelist: str, action: str, pks) -> object:
    return client.post(changelist, {"action": action, "_selected_action": [str(pk) for pk in pks], "index": "0"})


def _offered_actions(model, user) -> set[str]:
    request = RequestFactory().get(BO)
    request.user = user
    return set(admin.site._registry[model].get_actions(request))


def _rows(client, changelist: str) -> int:
    response = client.get(changelist)
    assert response.status_code == 200, (changelist, response.status_code)
    return response.context["cl"].result_count


@pytest.fixture
def cast(django_user_model):
    roles.ensure_roles()

    def make(email, role=None, **extra):
        user = django_user_model.objects.create_user(email=email, password=PASSWORD, **extra)
        if role:
            roles.assign_role(user, role)
        return user

    people = {key: make(f"f8.{key}@example.test", role, is_staff=True) for key, role in STAFF_ROLES.items()}
    people["administrator"] = make("f8.administrator@example.test", roles.ADMINISTRATOR, is_staff=True)
    people["person"] = make("f8.person@example.test", roles.PERSON)
    people["superuser"] = django_user_model.objects.create_superuser(email="f8.super@example.test", password=PASSWORD)
    return people


# =================================================================================================
# The help desk — the operator dispatches, it never reads (helpdesk.policies)
# =================================================================================================
TICKETS = f"{BO}helpdesk/helpdeskticket/"


@pytest.fixture
def ticket(cast):
    from helpdesk import services

    opened = services.open_ticket(cast["person"], subject="F8 objet", question="F8-QUESTION-SECRET")
    services.request_professional_review(opened, actor=cast["person"])
    return opened


class TestTheHelpDesk:
    def test_the_operator_reads_no_request_in_the_back_office(self, client, cast, ticket):
        client.force_login(cast["operator"])
        assert _rows(client, TICKETS) == 0, "F-8: the operator lists every request's shape"
        never = ticket.pk + 1000
        theirs, nobody = client.get(f"{TICKETS}{ticket.pk}/change/"), client.get(f"{TICKETS}{never}/change/")
        assert _not_found(theirs) and _not_found(nobody)

    def test_the_operator_still_designates_a_professional_on_the_platform(self, client, cast, ticket):
        client.force_login(cast["operator"])
        response = client.get("/fr/espace-reserve/guichet/designation/")
        assert response.status_code == 200
        body = response.content.decode("utf-8")
        assert ticket.reference in body and "F8-QUESTION-SECRET" not in body

    def test_a_superuser_reads_every_request(self, client, cast, ticket):
        client.force_login(cast["superuser"])
        assert _rows(client, TICKETS) == 1
        assert client.get(f"{TICKETS}{ticket.pk}/change/").status_code == 200


# =================================================================================================
# Public submissions — staff and administration; nobody hard-deletes (enquiries.policies)
# =================================================================================================
SUBMISSIONS = ("companyneedsrequest", "collaborationproposal", "contactrequest")
NEEDS = f"{BO}enquiries/companyneedsrequest/"


@pytest.fixture
def submission(db):
    from consents.services import record_consent
    from enquiries.models import CompanyNeedsRequest

    consent = record_consent(None, "company_needs", email="f8.company@example.test", language="fr")
    obj = CompanyNeedsRequest(
        email="f8.company@example.test",
        consent=consent,
        language="fr",
        company_name="F8 Officine S.r.l.",
        sector="Industrie",
        headquarters="Rovigo (RO)",
        contact_name_and_role="F8 Contact — RH",
        phone="+39 0425 000000",
        profiles_needed="Soudeurs",
    )
    obj.duplicate_hash = obj.compute_duplicate_hash()
    obj.save()
    return obj


class TestPublicSubmissions:
    def test_the_operator_reaches_no_public_submission(self, client, cast, submission):
        client.force_login(cast["operator"])
        for model in SUBMISSIONS:
            assert client.get(f"{BO}enquiries/{model}/").status_code == 403, model
        assert client.get(f"{NEEDS}{submission.pk}/change/").status_code == 403
        for action in ("export_csv", "export_json_single", "mark_handled", "anonymise_selected"):
            assert _action(client, NEEDS, action, [submission.pk]).status_code == 403, action
        submission.refresh_from_db()
        assert submission.anonymised_at is None and submission.handled_at is None
        assert not AuditEvent.objects.filter(action__startswith="enquiries.").exists()

    def test_the_administrator_hard_deletes_no_submission(self, client, cast, submission):
        """Erasure is the anonymisation, which keeps the consent proof: the policy grants «delete» to nobody."""
        client.force_login(cast["administrator"])
        assert "delete_selected" not in _offered_actions(type(submission), cast["administrator"])
        assert client.get(f"{NEEDS}{submission.pk}/delete/").status_code == 403
        assert client.post(f"{NEEDS}{submission.pk}/delete/", {"post": "yes"}).status_code == 403
        _action(client, NEEDS, "delete_selected", [submission.pk])
        assert type(submission).objects.filter(pk=submission.pk).exists()

    def test_staff_and_the_administrator_keep_their_work(self, client, cast, submission):
        client.force_login(cast["staff"])
        assert _rows(client, NEEDS) == 1
        assert _action(client, NEEDS, "mark_handled", [submission.pk]).status_code == 302
        submission.refresh_from_db()
        assert submission.handled_at is not None
        client.force_login(cast["administrator"])
        assert _action(client, NEEDS, "export_csv", [submission.pk]).status_code == 200
        _action(client, NEEDS, "anonymise_selected", [submission.pk])
        submission.refresh_from_db()
        assert submission.anonymised_at is not None
        assert AuditEvent.objects.filter(action="enquiries.export_csv").exists()


# =================================================================================================
# The virtual forum — moderators only (community.policies)
# =================================================================================================
COMMUNITY = ("membership", "room", "discussion", "post", "pendingpost", "report", "moderationaction")


@pytest.fixture
def forum_rows(django_user_model):
    from community.models import (
        Discussion,
        Membership,
        MembershipStatus,
        ParticipantCategory,
        Post,
        PostStatus,
        Report,
        Room,
    )
    from core import clock

    def member(email, **extra):
        user = django_user_model.objects.create_user(email=email, password=PASSWORD)
        roles.assign_role(user, roles.COMPANY)
        return Membership.objects.create(
            user=user,
            category=ParticipantCategory.COMPANY,
            status=MembershipStatus.APPROVED,
            approved_at=clock.now(),
            **extra,
        )

    room, _ = Room.objects.update_or_create(slug="f8-room", defaults={"name_fr": "F8", "published": True})
    hidden_name = member("f8.discreet@example.test", organisation="F8-HIDDEN-ORGANISATION", show_name=False)
    reporter = member("f8.reporter@example.test")
    discussion = Discussion.objects.create(room=room, author=hidden_name, title="F8", last_activity_at=clock.now())
    pending = Post.objects.create(
        discussion=discussion, author=hidden_name, body="F8 pending", status=PostStatus.PENDING_MODERATION
    )
    visible = Post.objects.create(
        discussion=discussion, author=hidden_name, body="F8 visible", status=PostStatus.VISIBLE
    )
    report = Report.objects.create(post=visible, reporter=reporter, reason="F8-REPORT-REASON")
    return {"membership": hidden_name, "pending": pending, "report": report}


class TestTheVirtualForum:
    def test_staff_reaches_no_virtual_forum_screen(self, client, cast, forum_rows):
        client.force_login(cast["staff"])
        for model in COMMUNITY:
            assert client.get(f"{BO}community/{model}/").status_code == 403, model
        assert client.get(f"{BO}community/membership/{forum_rows['membership'].pk}/change/").status_code == 403

    def test_staff_moderates_nothing(self, client, cast, forum_rows):
        from community.models import PostStatus

        client.force_login(cast["staff"])
        assert _action(client, f"{BO}community/pendingpost/", "approve", [forum_rows["pending"].pk]).status_code == 403
        assert _action(client, f"{BO}community/report/", "dismiss", [forum_rows["report"].pk]).status_code == 403
        forum_rows["pending"].refresh_from_db()
        assert forum_rows["pending"].status == PostStatus.PENDING_MODERATION

    def test_moderators_and_the_administrator_keep_moderating(self, client, cast, forum_rows):
        from community.models import PostStatus

        client.force_login(cast["moderator"])
        assert _rows(client, f"{BO}community/membership/") == 2
        _action(client, f"{BO}community/pendingpost/", "approve", [forum_rows["pending"].pk])
        forum_rows["pending"].refresh_from_db()
        assert forum_rows["pending"].status == PostStatus.VISIBLE
        client.force_login(cast["administrator"])
        assert _rows(client, f"{BO}community/report/") == 1

    def test_trusting_a_member_is_recorded(self, client, cast, forum_rows):
        """«Segna come affidabile» lets a member skip the moderation queue: a moderation act, in the audit trail."""
        client.force_login(cast["moderator"])
        _action(client, f"{BO}community/membership/", "mark_trusted", [forum_rows["membership"].pk])
        forum_rows["membership"].refresh_from_db()
        assert forum_rows["membership"].trusted
        event = AuditEvent.objects.get(action="community.membership.trusted")
        assert event.actor_id == cast["moderator"].pk and event.target_id == str(forum_rows["membership"].pk)


# =================================================================================================
# The Forum's governance module — the administrator's alone without a profile (forum.governance_policies)
# =================================================================================================
GOVERNANCE = (
    "forumedition",
    "commission",
    "forumprofile",
    "commissionmember",
    "table",
    "forumproposal",
    "forumproject",
    "annualreport",
)


@pytest.fixture
def governance(cast):
    from forum.governance import Commission, ForumEdition, ForumProfile, ForumRole, ParticipantCategory
    from forum.governance_seeds import EDITION_KEY, seed_forum_governance

    seed_forum_governance()
    edition = ForumEdition.objects.get(key=EDITION_KEY)
    own = ForumProfile.objects.create(
        user=cast["staff"],
        edition=edition,
        role=ForumRole.PARTICIPANT,
        organisation_label="F8 staff organisation",
        category=ParticipantCategory.INSTITUTION,
    )
    return {"edition": edition, "commission": Commission.objects.filter(edition=edition).first(), "own": own}


class TestTheForumGovernance:
    def test_staff_reaches_no_governance_screen(self, client, cast, governance):
        client.force_login(cast["staff"])
        for model in GOVERNANCE:
            assert client.get(f"{BO}forum/{model}/").status_code == 403, model

    def test_staff_grants_itself_no_mandate(self, client, cast, governance):
        """A live mandate reads a commission's proposals on the platform: «granted and revoked by the secretariat»."""
        from forum.governance import CommissionMember, MandateRole

        client.force_login(cast["staff"])
        response = client.post(
            f"{BO}forum/commissionmember/add/",
            {
                "commission": governance["commission"].pk,
                "profile": governance["own"].pk,
                "role": MandateRole.REFERENT,
                "valid_from": "2026-01-01",
                "_save": "Save",
            },
        )
        assert response.status_code == 403
        assert not CommissionMember.objects.filter(profile=governance["own"]).exists()

    def test_staff_keeps_the_forum_events_screens_and_the_administrator_the_module(self, client, cast, governance):
        client.force_login(cast["staff"])
        assert client.get(f"{BO}forum/forumregistration/").status_code == 200
        client.force_login(cast["administrator"])
        for model in GOVERNANCE:
            assert client.get(f"{BO}forum/{model}/").status_code == 200, model


# =================================================================================================
# Notifications — the content belongs to the message policy; a view grant never writes
# =================================================================================================
OUTBOX = f"{BO}notifications/emailoutbox/"
TOKEN = "F8-BEARER-TOKEN-dGhpcy1pcy1hLXRva2Vu"


@pytest.fixture
def mail(db):
    from notifications.models import EmailOutbox, OutboxStatus

    return EmailOutbox.objects.create(
        to_email="f8.person@example.test",
        subject="Confirmez votre inscription",
        body_text=f"F8-MAIL-BODY https://testserver/fr/consentements/newsletter/confirmer/{TOKEN}/",
        status=OutboxStatus.FAILED,
        last_error="F8 refused",
    )


class TestNotifications:
    def test_the_operator_reaches_no_notification_screen(self, client, cast, mail):
        client.force_login(cast["operator"])
        for model in ("notification", "emailoutbox", "notificationpreference"):
            assert client.get(f"{BO}notifications/{model}/").status_code == 403, model
        assert client.get(f"{OUTBOX}{mail.pk}/change/").status_code == 403

    def test_a_view_only_account_reads_the_delivery_record_and_no_body(self, client, cast, mail):
        client.force_login(cast["staff"])
        assert _rows(client, OUTBOX) == 1
        page = client.get(f"{OUTBOX}{mail.pk}/change/")
        assert page.status_code == 200
        body = page.content.decode("utf-8")
        assert "F8-MAIL-BODY" not in body and TOKEN not in body
        assert "F8 refused" in body, "the delivery record stays: did it leave, and why not"

    def test_a_view_only_account_resends_and_cancels_nothing(self, client, cast, mail):
        from notifications.models import EmailOutbox, OutboxStatus

        assert not {"resend", "cancel"} & _offered_actions(EmailOutbox, cast["staff"])
        client.force_login(cast["staff"])
        for action in ("resend", "cancel"):
            _action(client, OUTBOX, action, [mail.pk])
        mail.refresh_from_db()
        assert mail.status == OutboxStatus.FAILED

    def test_the_administrator_reads_the_body_and_resends_with_a_record(self, client, cast, mail):
        from notifications.models import OutboxStatus

        client.force_login(cast["administrator"])
        assert "F8-MAIL-BODY" in client.get(f"{OUTBOX}{mail.pk}/change/").content.decode("utf-8")
        _action(client, OUTBOX, "resend", [mail.pk])
        mail.refresh_from_db()
        assert mail.status == OutboxStatus.QUEUED
        event = AuditEvent.objects.get(action="notifications.outbox.resent")
        assert event.actor_id == cast["administrator"].pk and event.target_id == str(mail.pk)


# =================================================================================================
# Consents — a view grant withdraws nothing; nobody reads a subscriber's bearer tokens
# =================================================================================================
CONSENTS = f"{BO}consents/consentrecord/"
SUBSCRIPTIONS = f"{BO}consents/newslettersubscription/"


@pytest.fixture
def subscription(db):
    from consents.models import NewsletterSubscription
    from consents.services import record_consent

    consent = record_consent(None, "newsletter", email="f8.reader@example.test", language="fr")
    return NewsletterSubscription.objects.create(email="f8.reader@example.test", language="fr", consent=consent)


class TestConsents:
    def test_staff_withdraws_no_consent(self, client, cast, subscription):
        from consents.models import ConsentRecord

        consent = subscription.consent
        assert "withdraw_selected" not in _offered_actions(ConsentRecord, cast["staff"])
        client.force_login(cast["staff"])
        _action(client, CONSENTS, "withdraw_selected", [consent.pk])
        consent.refresh_from_db()
        assert consent.withdrawn_at is None

    def test_nobody_reads_a_subscribers_tokens_there(self, client, cast, subscription):
        """The links confirm a subscription or end it in the subscriber's name: bearer secrets of the person."""
        for who in ("staff", "administrator", "superuser"):
            client.force_login(cast[who])
            body = client.get(f"{SUBSCRIPTIONS}{subscription.pk}/change/").content.decode("utf-8")
            assert subscription.confirm_token not in body and subscription.unsubscribe_token not in body, who

    def test_the_administrator_rewrites_no_subscription_evidence(self, client, cast, subscription):
        client.force_login(cast["administrator"])
        client.post(
            f"{SUBSCRIPTIONS}{subscription.pk}/change/",
            {"email": "f8.someone.else@example.test", "language": "it", "_save": "Save"},
        )
        subscription.refresh_from_db()
        assert (subscription.email, subscription.language) == ("f8.reader@example.test", "fr")

    def test_the_administrator_records_a_withdrawal_in_the_audit_trail(self, client, cast, subscription):
        consent = subscription.consent
        client.force_login(cast["administrator"])
        _action(client, CONSENTS, "withdraw_selected", [consent.pk])
        consent.refresh_from_db()
        assert consent.withdrawn_at is not None
        event = AuditEvent.objects.get(action="consents.withdrawn")
        assert event.actor_id == cast["administrator"].pk and event.target_id == str(consent.pk)


# =================================================================================================
# The audit trail — the administration reads it all; the legal approver its rules' trail only
# =================================================================================================
EVENTS = f"{BO}audit/auditevent/"


@pytest.fixture
def trail(cast):
    case_services.open_case(cast["person"], purpose=CasePurpose.WORK, pathway_key="salaried_work")
    case_event = AuditEvent.objects.get(action="case.opened")
    rule_event = AuditEvent.objects.create(
        action="rule.transition", target_type="LegalRule", target_id="1", target_repr="F8-RULE v1"
    )
    return {"case": case_event, "rule": rule_event}


class TestTheAuditTrail:
    def test_the_legal_approver_reads_its_rules_trail_and_nothing_else(self, client, cast, trail):
        client.force_login(cast["legal_approver"])
        body = client.get(EVENTS).content.decode("utf-8")
        assert f"{EVENTS}{trail['rule'].pk}/change/" in body
        assert f"{EVENTS}{trail['case'].pk}/change/" not in body, "F-8: every file's events"
        assert _not_found(client.get(f"{EVENTS}{trail['case'].pk}/change/"))
        assert not client.get(EVENTS, {"q": cast["legal_approver"].email}).context["cl"].result_count, "its login"

    def test_the_administration_reads_the_whole_trail(self, client, cast, trail):
        client.force_login(cast["administrator"])
        assert client.get(f"{EVENTS}{trail['case'].pk}/change/").status_code == 200
        assert client.get(f"{EVENTS}{trail['rule'].pk}/change/").status_code == 200

    @pytest.mark.parametrize("who", ["operator", "staff", "moderator", "content_editor", "legal_editor"])
    def test_no_other_role_reads_it(self, client, cast, trail, who):
        client.force_login(cast[who])
        assert client.get(EVENTS).status_code == 403


# =================================================================================================
# Orientation — the answers are the owner's (orientation.policies); the shape is the administration's
# =================================================================================================
@pytest.fixture
def questionnaire(cast):
    from orientation.models import OrientationResult, OrientationSession, Ruleset, SessionStatus
    from orientation.seeds import seed_ruleset_v1

    seed_ruleset_v1()
    ruleset = Ruleset.objects.get(version=1)
    session = OrientationSession.objects.create(
        ruleset=ruleset,
        user=cast["person"],
        status=SessionStatus.COMPLETED,
        state={"answers": {"family": "F8-ANSWER-IN-PROGRESS"}, "history": []},
    )
    result = OrientationResult.objects.create(
        session=session,
        outcome=ruleset.outcomes.first(),
        ruleset_version=1,
        answers_snapshot={"family": "F8-ANSWER-SNAPSHOT"},
    )
    return {"session": session, "result": result}


class TestOrientation:
    def test_the_administrator_reads_no_answer(self, client, cast, questionnaire):
        client.force_login(cast["administrator"])
        session = client.get(f"{BO}orientation/orientationsession/{questionnaire['session'].pk}/change/")
        result = client.get(f"{BO}orientation/orientationresult/{questionnaire['result'].pk}/change/")
        assert session.status_code == 200 and result.status_code == 200, "the shape stays"
        assert "F8-ANSWER-IN-PROGRESS" not in session.content.decode("utf-8")
        assert "F8-ANSWER-SNAPSHOT" not in result.content.decode("utf-8")

    def test_the_administrator_still_anonymises_on_request(self, client, cast, questionnaire):
        client.force_login(cast["administrator"])
        sessions = f"{BO}orientation/orientationsession/"
        assert _rows(client, sessions) == 1
        _action(client, sessions, "anonymise_action", [questionnaire["session"].pk])
        assert AuditEvent.objects.filter(action="orientation.session.anonymised").exists()

    def test_a_superuser_reads_the_answers(self, client, cast, questionnaire):
        client.force_login(cast["superuser"])
        result = client.get(f"{BO}orientation/orientationresult/{questionnaire['result'].pk}/change/")
        assert "F8-ANSWER-SNAPSHOT" in result.content.decode("utf-8")


# =================================================================================================
# Integrations — a view grant requeues and cancels nothing
# =================================================================================================
OUTBOUND = f"{BO}integrations/outboundevent/"


@pytest.fixture
def outbound(db):
    from integrations.models import OutboundEvent, OutboundEventStatus

    return OutboundEvent.objects.create(
        event_type="case.updated", idempotency_key="f8-outbound-1", status=OutboundEventStatus.FAILED
    )


class TestIntegrations:
    def test_the_administrator_requeues_and_cancels_nothing(self, client, cast, outbound):
        from integrations.models import OutboundEvent, OutboundEventStatus

        assert not {"requeue", "cancel"} & _offered_actions(OutboundEvent, cast["administrator"])
        client.force_login(cast["administrator"])
        assert _rows(client, OUTBOUND) == 1, "it still reads them"
        for action in ("requeue", "cancel"):
            _action(client, OUTBOUND, action, [outbound.pk])
        outbound.refresh_from_db()
        assert outbound.status == OutboundEventStatus.FAILED

    def test_a_superuser_requeues_with_a_record(self, client, cast, outbound):
        from integrations.models import OutboundEventStatus

        client.force_login(cast["superuser"])
        _action(client, OUTBOUND, "requeue", [outbound.pk])
        outbound.refresh_from_db()
        assert outbound.status == OutboundEventStatus.QUEUED
        assert AuditEvent.objects.filter(action="integrations.outbound.requeued", target_id=str(outbound.pk)).exists()


# =================================================================================================
# Documents — metadata for the administration, a file only through the documents app's own view
# =================================================================================================
DOCUMENTS = f"{BO}documents/privatedocument/"
REQUIREMENTS = f"{BO}documents/documentrequirement/"


@pytest.fixture
def documents(cast, tmp_path, settings):
    from documents import services as document_services
    from documents.models import DocumentKind

    settings.PRIVATE_MEDIA_ROOT = tmp_path / "private"

    def upload(name):
        return document_services.store_upload(
            cast["person"],
            SimpleUploadedFile(name, b"%PDF-1.4 F8 synthetic", content_type="application/pdf"),
            DocumentKind.choices[0][0],
        )

    pending, deleted = upload("f8-pending.pdf"), upload("f8-deleted.pdf")
    document_services.soft_delete(deleted, actor=cast["person"])
    return {"pending": pending, "deleted": deleted}


class TestDocuments:
    @pytest.mark.parametrize("who", sorted(STAFF_ROLES))
    def test_no_role_but_the_administration_reaches_the_documents(self, client, cast, documents, who):
        client.force_login(cast[who])
        assert client.get(DOCUMENTS).status_code == 403
        assert client.get(REQUIREMENTS).status_code == 403
        assert client.get(f"{DOCUMENTS}{documents['pending'].pk}/change/").status_code == 403

    def test_the_administrator_reads_metadata_and_no_file(self, client, cast, documents):
        client.force_login(cast["administrator"])
        listing = client.get(DOCUMENTS).content.decode("utf-8")
        page = client.get(f"{DOCUMENTS}{documents['pending'].pk}/change/").content.decode("utf-8")
        assert "f8-pending.pdf" in listing
        for body in (listing, page):
            assert f"/documents/{documents['pending'].pk}/" not in body, "a download link"
        assert client.get(f"/documents/{documents['pending'].pk}/").status_code == 403, "unscanned: not deliverable"

    def test_a_deleted_document_is_nobodys_to_read_there_but_a_superusers(self, client, cast, documents):
        """``private_document_policy`` refuses a deleted document to everybody; the superuser stays the last resort."""
        client.force_login(cast["administrator"])
        assert "f8-deleted.pdf" not in client.get(DOCUMENTS, {"deleted": "yes"}).content.decode("utf-8")
        assert _not_found(client.get(f"{DOCUMENTS}{documents['deleted'].pk}/change/"))
        client.force_login(cast["superuser"])
        assert "f8-deleted.pdf" in client.get(DOCUMENTS, {"deleted": "yes"}).content.decode("utf-8")

    def test_the_superusers_link_is_the_documents_own_checked_view(self, client, cast, documents):
        """The model holds no file field: the one way out is ``documents.views._serve`` — the policy, the delivery
        rule (an unscanned file goes to nobody but its depositor), the throttle and the audit event."""
        from documents import services as document_services
        from documents.models import ScanStatus

        doc = documents["pending"]
        client.force_login(cast["superuser"])
        assert f"/documents/{doc.pk}/" not in client.get(f"{DOCUMENTS}{doc.pk}/change/").content.decode("utf-8")
        assert client.get(f"/documents/{doc.pk}/").status_code == 403
        document_services.apply_scan_result(doc, ScanStatus.CLEAN, request=None, note="F8 test")
        assert f"/documents/{doc.pk}/" in client.get(f"{DOCUMENTS}{doc.pk}/change/").content.decode("utf-8")
        response = client.get(f"/documents/{doc.pk}/")
        assert response.status_code == 200
        assert {"private", "no-store"} <= {part.strip() for part in response["Cache-Control"].split(",")}
        assert AuditEvent.objects.filter(action="documents.downloaded", target_id=str(doc.pk)).exists()

    def test_the_export_of_the_register_is_recorded(self, client, cast, documents):
        client.force_login(cast["administrator"])
        response = _action(client, DOCUMENTS, "export_csv", [documents["pending"].pk])
        assert response.status_code == 200
        event = AuditEvent.objects.get(action="documents.exported")
        assert event.actor_id == cast["administrator"].pk and event.metadata["count"] == 1


# =================================================================================================
# Accounts and person data — the administration's, nobody else's (PERMISSION_MODEL §5.10)
# =================================================================================================
ACCOUNT_SCREENS = (
    "accounts/user/",
    "accounts/personprofile/",
    "accounts/organisation/",
    "account/emailaddress/",
    "mfa/authenticator/",
    "auth/group/",
)


class TestAccounts:
    @pytest.mark.parametrize("who", sorted(STAFF_ROLES))
    def test_no_staff_role_reads_the_accounts(self, client, cast, who):
        client.force_login(cast[who])
        for screen in ACCOUNT_SCREENS:
            assert client.get(f"{BO}{screen}").status_code == 403, screen
        assert client.get(f"{BO}accounts/user/{cast['person'].pk}/change/").status_code == 403

    def test_the_administrator_reads_the_accounts_and_not_their_factors(self, client, cast):
        client.force_login(cast["administrator"])
        assert client.get(f"{BO}accounts/user/{cast['person'].pk}/change/").status_code == 200
        for screen in ("account/emailaddress/", "mfa/authenticator/", "auth/group/"):
            assert client.get(f"{BO}{screen}").status_code == 403, screen


# =================================================================================================
# Selection, companies, the Academy — no role holds them: the superuser's last resort only
# =================================================================================================
SUPERUSER_ONLY = (
    "selection/selectionprocess/",
    "selection/selectionmandate/",
    "selection/identitydisclosure/",
    "selection/authorizedactor/",
    "companies/companyneed/",
    "companies/companyprofile/",
    "academy/enrolment/",
    "academy/trainingplan/",
)


class TestSuperuserOnlyScreens:
    @pytest.mark.parametrize("who", [*sorted(STAFF_ROLES), "administrator"])
    def test_no_role_reaches_them(self, client, cast, who):
        client.force_login(cast[who])
        for screen in SUPERUSER_ONLY:
            assert client.get(f"{BO}{screen}").status_code == 403, (who, screen)

    def test_the_superuser_does(self, client, cast):
        client.force_login(cast["superuser"])
        for screen in SUPERUSER_ONLY:
            assert client.get(f"{BO}{screen}").status_code == 200, screen
