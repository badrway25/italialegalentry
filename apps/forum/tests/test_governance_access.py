"""
Who reads what — asserted in the QUERY, then asserted again through the real routes.

Two properties are checked here and they are the two that matter:

1. **Authorisation lives in the queryset.** ``readable_by`` decides; the views merely render what it
   returned. A row the caller may not see never reaches the process, so it cannot leak through a
   count, an autocomplete or a differently worded « not found ».

2. **The list and the detail page agree.** For every account, every row its list shows must open,
   and every row its list hides must answer 404 — not 403, because a 403 says « this exists and is
   not yours », which is a disclosure in itself. ``test_the_list_and_the_detail_agree`` walks both
   directions for commissions, proposals and projects rather than trusting that they match.

Routes are mounted through ``forum.tests.governance_urlconf`` because ``config/urls.py`` belongs to
another lane; see that module for why.
"""

from __future__ import annotations

import datetime as dt

import pytest
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse
from django.utils import timezone

from accounts import roles
from forum import governance_services as services
from forum.governance import (
    AnnualReport,
    Commission,
    ForumProfile,
    ForumProject,
    ForumProposal,
    ProposalStatus,
    ReportStatus,
    Table,
    TableStatus,
)

pytestmark = [pytest.mark.django_db, pytest.mark.urls("forum.tests.governance_urlconf")]

BODY = "Proposition de coopération entre les chambres consulaires, avec un calendrier annuel partagé."


@pytest.fixture
def submitted_proposal(member, referent, commission):
    proposal = services.open_proposal(member.user, commission, title_fr="Rencontres consulaires", body_fr=BODY)
    services.transition_proposal(proposal, ProposalStatus.SUBMITTED, actor=member.user)
    return proposal


@pytest.fixture
def accepted_project(member, referent, commission, submitted_proposal):
    services.transition_proposal(submitted_proposal, ProposalStatus.UNDER_REVIEW, actor=referent.user)
    services.transition_proposal(submitted_proposal, ProposalStatus.ACCEPTED, actor=referent.user, note="Retenue.")
    return services.promote_to_project(submitted_proposal, lead=member.profile, actor=referent.user)


# ---------------------------------------------------------------------------------------------
# The querysets
# ---------------------------------------------------------------------------------------------
def test_an_anonymous_user_reads_nothing(governance_edition, commission):
    anonymous = AnonymousUser()
    assert list(Commission.objects.readable_by(anonymous)) == []
    assert list(ForumProposal.objects.readable_by(anonymous)) == []
    assert list(ForumProject.objects.readable_by(anonymous)) == []
    assert list(ForumProfile.objects.readable_by(anonymous)) == []
    assert list(Table.objects.readable_by(anonymous)) == []
    assert list(AnnualReport.objects.readable_by(anonymous)) == []


def test_an_account_without_a_profile_reads_nothing(outsider, commission, submitted_proposal):
    assert list(Commission.objects.readable_by(outsider)) == []
    assert list(ForumProposal.objects.readable_by(outsider)) == []


def test_a_member_reads_only_their_own_commissions(member, commission, other_commission):
    readable = list(Commission.objects.readable_by(member.user))
    assert commission in readable
    assert other_commission not in readable


def test_the_secretariat_reads_the_whole_edition(secretariat, commission, other_commission):
    readable = list(Commission.objects.readable_by(secretariat.user))
    assert commission in readable
    assert other_commission in readable


def test_an_observer_reads_the_perimeter_of_their_mandate(observer, commission, other_commission):
    """« Consultare secondo il perimetro dell'accordo » — the perimeter IS the live mandate."""
    readable = list(Commission.objects.readable_by(observer.user))
    assert readable == [commission]


def test_a_lapsed_mandate_stops_listing_at_read_time(member, commission, submitted_proposal):
    assert submitted_proposal in ForumProposal.objects.readable_by(member.user)
    member.mandate.valid_until = timezone.localdate() - dt.timedelta(days=1)
    member.mandate.save(update_fields=["valid_until"])
    # The proposer still reads their OWN proposal — losing a mandate does not erase authorship.
    assert list(Commission.objects.readable_by(member.user)) == []


def test_a_lapsed_member_loses_other_peoples_proposals(referent, member, commission, submitted_proposal):
    assert submitted_proposal in ForumProposal.objects.readable_by(referent.user)
    referent.mandate.valid_until = timezone.localdate() - dt.timedelta(days=1)
    referent.mandate.save(update_fields=["valid_until"])
    assert submitted_proposal not in ForumProposal.objects.readable_by(referent.user)


def test_a_draft_belongs_to_its_author_alone(member, referent, commission):
    draft = services.open_proposal(member.user, commission, title_fr="Brouillon en cours", body_fr=BODY)
    assert draft in ForumProposal.objects.readable_by(member.user)
    assert draft not in ForumProposal.objects.readable_by(referent.user)
    assert draft not in ForumProposal.objects.readable_by(secretariat_of(commission))


def secretariat_of(commission):
    """A brand-new secretariat account, built inline so the assertion above reads in one line."""
    from django.contrib.auth import get_user_model

    from forum.governance import ForumRole

    user = get_user_model().objects.create_user(email="sec.draft@example.test", password="x")
    ForumProfile.objects.create(
        user=user, edition=commission.edition, role=ForumRole.SECRETARIAT, organisation_label="Secrétariat"
    )
    return user


def test_a_submitted_proposal_is_visible_to_the_commission(member, referent, submitted_proposal):
    assert submitted_proposal in ForumProposal.objects.readable_by(referent.user)


def test_an_administrator_reads_everything(django_user_model, commission, submitted_proposal):
    administrator = django_user_model.objects.create_user(email="admin.forum@example.test", password="x")
    roles.ensure_roles()
    roles.assign_role(administrator, roles.ADMINISTRATOR)
    assert commission in Commission.objects.readable_by(administrator)
    assert submitted_proposal in ForumProposal.objects.readable_by(administrator)


def test_project_staff_do_not_read_the_forum(django_user_model, commission, submitted_proposal):
    """Same reasoning as the case file: a standing read of every workspace is a disclosure."""
    staff = django_user_model.objects.create_user(email="staff.forum@example.test", password="x", is_staff=True)
    roles.ensure_roles()
    roles.assign_role(staff, roles.STAFF)
    assert list(Commission.objects.readable_by(staff)) == []
    assert list(ForumProposal.objects.readable_by(staff)) == []


def test_a_deactivated_profile_grants_nothing(member, commission):
    member.profile.is_active = False
    member.profile.save(update_fields=["is_active"])
    assert list(Commission.objects.readable_by(member.user)) == []


def test_a_draft_report_is_not_readable_by_a_participant(governance_edition, member, secretariat):
    report = services.generate_annual_report(governance_edition, actor=secretariat.user)
    assert report.status == ReportStatus.DRAFT
    assert report not in AnnualReport.objects.readable_by(member.user)
    assert report in AnnualReport.objects.readable_by(secretariat.user)


def test_a_published_report_is_readable_by_every_participant(governance_edition, member, secretariat):
    report = services.generate_annual_report(governance_edition, actor=secretariat.user)
    services.publish_annual_report(report, actor=secretariat.user)
    assert report in AnnualReport.objects.readable_by(member.user)


# ---------------------------------------------------------------------------------------------
# The routes
# ---------------------------------------------------------------------------------------------
def test_an_anonymous_visitor_is_sent_to_the_login_page(client, governance_open, governance_edition):
    response = client.get(reverse("forum_governance:participation"))
    assert response.status_code == 302
    assert "/compte/" in response["Location"] or "login" in response["Location"]


def test_a_member_opens_their_participation_page(client, governance_open, member):
    client.force_login(member.user)
    response = client.get(reverse("forum_governance:participation"))
    assert response.status_code == 200
    assert b"noindex" in response["X-Robots-Tag"].encode()


def test_a_member_opens_a_commission_they_sit_on(client, governance_open, member, commission):
    client.force_login(member.user)
    response = client.get(reverse("forum_governance:commission_detail", args=[commission.key]))
    assert response.status_code == 200


def test_a_commission_outside_the_mandate_answers_404_not_403(client, governance_open, member, other_commission):
    client.force_login(member.user)
    response = client.get(reverse("forum_governance:commission_detail", args=[other_commission.key]))
    assert response.status_code == 404


def test_a_proposal_outside_the_perimeter_answers_404(client, governance_open, outsider, submitted_proposal):
    client.force_login(outsider)
    response = client.get(reverse("forum_governance:proposal_detail", args=[submitted_proposal.uuid]))
    assert response.status_code == 404


def test_someone_elses_draft_answers_404(client, governance_open, member, referent, commission):
    draft = services.open_proposal(member.user, commission, title_fr="Brouillon privé", body_fr=BODY)
    client.force_login(referent.user)
    assert client.get(reverse("forum_governance:proposal_detail", args=[draft.uuid])).status_code == 404
    client.force_login(member.user)
    assert client.get(reverse("forum_governance:proposal_detail", args=[draft.uuid])).status_code == 200


def test_the_list_and_the_detail_agree(client, governance_open, member, referent, secretariat, accepted_project):
    """
    Every row a list shows must open, and every row it hides must answer 404. Both directions.

    This is the assertion that caught the staff/queryset disagreement in the case file: a policy and
    a queryset that answer the same question differently are a security bug waiting for a view that
    checks the wrong one.
    """
    routes = (
        (Commission.objects.all(), "forum_governance:commission_detail", lambda row: [row.key], Commission),
        (ForumProposal.objects.all(), "forum_governance:proposal_detail", lambda row: [row.uuid], ForumProposal),
        (ForumProject.objects.all(), "forum_governance:project_detail", lambda row: [row.uuid], ForumProject),
    )
    for actor in (member, referent, secretariat):
        client.force_login(actor.user)
        for queryset, route, args, model in routes:
            readable = set(model.objects.readable_by(actor.user).values_list("pk", flat=True))
            for row in queryset:
                expected = 200 if row.pk in readable else 404
                response = client.get(reverse(route, args=args(row)))
                assert response.status_code == expected, f"{actor.user.email} · {route} · {row.pk}"


def test_a_table_follows_its_commission(client, governance_open, member, referent, commission, other_commission):
    mine = Table.objects.create(commission=commission, key="table-a", title_fr="Table A", status=TableStatus.OPEN)
    theirs = Table.objects.create(
        commission=other_commission, key="table-b", title_fr="Table B", status=TableStatus.OPEN
    )
    client.force_login(member.user)
    assert client.get(reverse("forum_governance:table_detail", args=[commission.key, mine.key])).status_code == 200
    assert (
        client.get(reverse("forum_governance:table_detail", args=[other_commission.key, theirs.key])).status_code
        == 404
    )


def test_an_observer_may_not_open_the_proposal_form(client, governance_open, observer, commission):
    """The observer CAN see the commission, so refusing out loud discloses nothing new: 403."""
    client.force_login(observer.user)
    assert client.get(reverse("forum_governance:commission_detail", args=[commission.key])).status_code == 200
    assert client.get(reverse("forum_governance:proposal_create", args=[commission.key])).status_code == 403


def test_a_member_drafts_a_proposal_through_the_form(client, governance_open, member, commission):
    client.force_login(member.user)
    response = client.post(
        reverse("forum_governance:proposal_create", args=[commission.key]),
        {"title_fr": "Programme de stages croisés", "body_fr": BODY, "table": ""},
    )
    assert response.status_code == 302
    proposal = ForumProposal.objects.get(title_fr="Programme de stages croisés")
    assert proposal.status == ProposalStatus.DRAFT
    assert proposal.proposer_id == member.profile.pk


def test_a_transition_goes_through_the_service_and_is_audited(client, governance_open, member, commission):
    from audit.models import AuditEvent

    proposal = services.open_proposal(member.user, commission, title_fr="À déposer maintenant", body_fr=BODY)
    client.force_login(member.user)
    response = client.post(
        reverse("forum_governance:proposal_transition", args=[proposal.uuid]),
        {"target": ProposalStatus.SUBMITTED, "note": ""},
    )
    assert response.status_code == 302
    proposal.refresh_from_db()
    assert proposal.status == ProposalStatus.SUBMITTED
    assert AuditEvent.objects.filter(action="forum.proposal.transition", target_id=str(proposal.pk)).exists()


def test_a_transition_the_caller_may_not_ask_for_is_refused_by_the_form(
    client, governance_open, member, referent, commission
):
    """The form only offers what the service would accept; posting anything else fails validation."""
    proposal = services.open_proposal(member.user, commission, title_fr="Tentative de raccourci", body_fr=BODY)
    services.transition_proposal(proposal, ProposalStatus.SUBMITTED, actor=member.user)
    client.force_login(member.user)
    response = client.post(
        reverse("forum_governance:proposal_transition", args=[proposal.uuid]),
        {"target": ProposalStatus.ACCEPTED, "note": "Je me retiens moi-même."},
    )
    assert response.status_code == 302
    proposal.refresh_from_db()
    assert proposal.status == ProposalStatus.SUBMITTED


def test_the_proposal_transition_route_refuses_get(client, governance_open, member, commission):
    proposal = services.open_proposal(member.user, commission, title_fr="Méthode interdite", body_fr=BODY)
    client.force_login(member.user)
    assert client.get(reverse("forum_governance:proposal_transition", args=[proposal.uuid])).status_code == 405


def test_the_annual_report_route_answers_404_without_a_readable_report(client, governance_open, member):
    client.force_login(member.user)
    assert client.get(reverse("forum_governance:annual_report")).status_code == 404


def test_every_governance_response_is_noindex(client, governance_open, member, commission):
    client.force_login(member.user)
    for url in (
        reverse("forum_governance:participation"),
        reverse("forum_governance:commissions"),
        reverse("forum_governance:proposals"),
        reverse("forum_governance:projects"),
    ):
        response = client.get(url)
        assert response.status_code == 200
        assert response["X-Robots-Tag"] == "noindex, nofollow"


# ---------------------------------------------------------------------------------------------
# The queryset and the policy must answer the same question the same way
# ---------------------------------------------------------------------------------------------
def test_the_queryset_and_the_object_policy_agree(
    member, referent, secretariat, observer, outsider, lapsed_member, accepted_project, commission, django_user_model
):
    """
    Every account × every row × both defences.

    ``readable_by`` keeps rows out of lists; ``accounts.permissions.can`` answers for one row in
    hand. A view that checked the second where it should have checked the first would hand out a
    row the list was hiding, so the two must never disagree. This is the test that found the
    staff/queryset discrepancy in the case file — it is run here for the same reason.
    """
    from accounts.permissions import can
    from forum.governance import CommissionMember, Table

    roles.ensure_roles()
    administrator = django_user_model.objects.create_user(email="admin.agree@example.test", password="x")
    roles.assign_role(administrator, roles.ADMINISTRATOR)
    staff = django_user_model.objects.create_user(email="staff.agree@example.test", password="x", is_staff=True)
    roles.assign_role(staff, roles.STAFF)
    Table.objects.create(commission=commission, key="table-agree", title_fr="Table", status=TableStatus.OPEN)
    services.generate_annual_report(commission.edition, actor=secretariat.user)

    accounts = {
        "member": member.user,
        "referent": referent.user,
        "secretariat": secretariat.user,
        "observer": observer.user,
        "lapsed": lapsed_member.user,
        "outsider": outsider,
        "administrator": administrator,
        "staff": staff,
    }
    models = (Commission, Table, CommissionMember, ForumProposal, ForumProject, ForumProfile, AnnualReport)
    for label, user in accounts.items():
        for model in models:
            readable = set(model.objects.readable_by(user).values_list("pk", flat=True))
            for row in model.objects.all():
                in_list = row.pk in readable
                by_policy = can(user, "view", row)
                assert in_list == by_policy, f"{label} · {model.__name__} #{row.pk}: list={in_list} policy={by_policy}"
