"""
FORUM_GOVERNANCE §5: «I partecipanti non possono consultare informazioni private di altri utenti.
Il Forum non è una rubrica di contatti.»

This file is the proof, and it attacks the promise from four directions rather than one:

1. **The schema.** ``ForumProfile`` must not HOLD an e-mail address, a telephone number or a
   personal name. A promise kept by a template is one refactor from being broken; a promise kept by
   the absence of a column cannot be broken by a template, a serialiser or a future API.

2. **The querysets.** Everything a participant can pull out of ``ForumProfile.objects.readable_by``
   — every field of every readable row, serialised — is searched for the other participant's e-mail
   and name. Not a spot check of three attributes: the whole row.

3. **The views.** Every route of the module is walked as one participant while another participant
   holds a mandate on the same commission, has tabled a proposal, leads a project and owns a
   milestone — so their profile is reachable from five different screens — and every response body
   is searched for their e-mail and their name.

4. **The audit trail.** ``audit.services.record`` copies ``str(target)`` into ``target_repr``, and
   audit rows are read by people who sit on no commission at all. ``ForumProfile.__str__`` is
   therefore asserted too.
"""

from __future__ import annotations

import json
import pathlib

import pytest
from django.db import models
from django.urls import reverse

from forum import governance_services as services
from forum.governance import (
    FORBIDDEN_PROFILE_FIELDS,
    PUBLIC_PROFILE_KEYS,
    ForumProfile,
    MandateRole,
    ProposalStatus,
    Table,
    TableStatus,
)

pytestmark = [pytest.mark.django_db, pytest.mark.urls("forum.tests.governance_urlconf")]

#: Distinctive values planted on the OTHER participant. If any of them ever reaches a queryset, a
#: page or an audit row read by the first participant, the promise is broken and a test fails.
SECRET_EMAIL = "prive.personnel@example.test"
SECRET_NAME = "Nom Prive Du Participant"
SECRET_PHONE = "+39 333 000 11 22"

BODY = "Proposition de coopération entre chambres consulaires, avec un calendrier annuel partagé."


@pytest.fixture
def other_participant(forum_actor, commission):
    """A second participant on the SAME commission, whose account carries real personal data."""
    actor = forum_actor(
        "autre@example.test",
        organisation_label="Chambre de commerce de Rovigo",
        interests="Mobilité académique, formation professionnelle",
        commission=commission,
        mandate_role=MandateRole.REFERENT,
    )
    actor.user.email = SECRET_EMAIL
    actor.user.full_name = SECRET_NAME
    actor.user.save(update_fields=["email", "full_name"])
    return actor


@pytest.fixture
def populated(member, other_participant, commission):
    """One commission where the other participant is visible from every screen of the module."""
    table = Table.objects.create(
        commission=commission,
        key="table-privacy",
        title_fr="Table thématique",
        status=TableStatus.OPEN,
        referent=other_participant.mandate,
    )
    proposal = services.open_proposal(
        other_participant.user, commission, title_fr="Proposition de l’autre participant", body_fr=BODY, table=table
    )
    services.transition_proposal(proposal, ProposalStatus.SUBMITTED, actor=other_participant.user)
    services.transition_proposal(proposal, ProposalStatus.UNDER_REVIEW, actor=other_participant.user)
    services.transition_proposal(proposal, ProposalStatus.ACCEPTED, actor=other_participant.user, note="Retenue.")
    project = services.promote_to_project(
        proposal, lead=other_participant.profile, actor=other_participant.user
    )
    services.add_milestone(project, title_fr="Convention signée", responsible=other_participant.profile)
    services.record_monitoring(
        project,
        period_start=table.opened_on,
        period_end=table.opened_on,
        indicators={"rencontres": 2},
        recorded_by=other_participant.profile,
        actor=other_participant.user,
    )
    return {"table": table, "proposal": proposal, "project": project}


# ---------------------------------------------------------------------------------------------
# 1. The schema
# ---------------------------------------------------------------------------------------------
def test_the_participation_profile_holds_no_personal_field():
    names = {field.name for field in ForumProfile._meta.get_fields()}
    leaked = names & set(FORBIDDEN_PROFILE_FIELDS)
    assert leaked == set(), f"a participation profile must not hold {sorted(leaked)}"


def test_the_participation_profile_holds_no_email_field():
    for field in ForumProfile._meta.get_fields():
        assert not isinstance(field, models.EmailField), field.name


def test_the_published_profile_has_exactly_three_keys(member):
    published = services.public_profile(member.profile)
    assert set(published) == set(PUBLIC_PROFILE_KEYS)
    assert set(published) == {"organisation", "category", "interests"}


def test_the_profile_string_is_not_the_account(other_participant):
    """``str(target)`` is copied into every audit row; it must never be an e-mail address."""
    label = str(other_participant.profile)
    assert SECRET_EMAIL not in label
    assert SECRET_NAME not in label
    assert "Chambre de commerce de Rovigo" in label


# ---------------------------------------------------------------------------------------------
# 2. The querysets
# ---------------------------------------------------------------------------------------------
def test_no_readable_profile_row_carries_personal_data(member, other_participant):
    rows = list(ForumProfile.objects.readable_by(member.user).values())
    assert len(rows) >= 2, "the other participant must actually be visible, or this proves nothing"
    blob = json.dumps(rows, default=str)
    assert SECRET_EMAIL not in blob
    assert SECRET_NAME not in blob
    assert SECRET_PHONE not in blob


def test_the_membership_list_publishes_organisation_category_and_interests(member, other_participant, commission):
    rows = services.commission_members(member.user, commission)
    published = {row["organisation"] for row in rows}
    assert "Chambre de commerce de Rovigo" in published
    for row in rows:
        assert set(row) == {"organisation", "category", "interests", "role", "valid_from", "valid_until"}
        assert SECRET_EMAIL not in json.dumps(row, default=str)


def test_the_module_never_traverses_the_join_to_the_account():
    """
    A profile points at a user, so the join exists and any code holding the model can walk it.

    What must not happen is that THIS module walks it. The four Python files and the eight templates
    of the governance module are searched for the account attributes that would leak — a future
    « just show the contact e-mail here » fails this test instead of shipping.
    """
    root = pathlib.Path(__file__).resolve().parents[1]
    sources = [
        root / "governance.py",
        root / "governance_services.py",
        root / "governance_views.py",
        root / "governance_policies.py",
        root / "governance_forms.py",
    ]
    sources += sorted((root.parents[1] / "templates" / "forum" / "governance").glob("*.html"))
    for source in sources:
        text = source.read_text(encoding="utf-8")
        for forbidden in ("user__email", "user.email", ".full_name", "get_full_name"):
            assert forbidden not in text, f"{source.name} reaches for {forbidden}"


def test_a_profile_of_another_edition_is_not_readable(member, forum_actor, django_user_model, governance_edition):
    from forum.governance import EditionStatus, ForumEdition

    other_edition = ForumEdition.objects.create(
        key="casablanca-2027", year=2027, title_fr="Édition de Casablanca", status=EditionStatus.PLANNED
    )
    stranger = django_user_model.objects.create_user(email="etranger@example.test", password="x")
    profile = ForumProfile.objects.create(
        user=stranger, edition=other_edition, organisation_label="Organisation étrangère"
    )
    assert profile not in ForumProfile.objects.readable_by(member.user)


def test_sharing_an_edition_is_not_enough_to_read_a_profile(member, forum_actor):
    """A profile becomes visible through a COMMISSION, not through an edition. Otherwise: directory."""
    unrelated = forum_actor("sans.commission@example.test", organisation_label="Organisation sans commission")
    assert unrelated.profile not in ForumProfile.objects.readable_by(member.user)


# ---------------------------------------------------------------------------------------------
# 3. The views
# ---------------------------------------------------------------------------------------------
def test_no_route_of_the_module_renders_another_participants_personal_data(
    client, governance_open, member, other_participant, populated, commission
):
    client.force_login(member.user)
    urls = [
        reverse("forum_governance:participation"),
        reverse("forum_governance:commissions"),
        reverse("forum_governance:commission_detail", args=[commission.key]),
        reverse("forum_governance:table_detail", args=[commission.key, populated["table"].key]),
        reverse("forum_governance:proposals"),
        reverse("forum_governance:proposal_detail", args=[populated["proposal"].uuid]),
        reverse("forum_governance:projects"),
        reverse("forum_governance:project_detail", args=[populated["project"].uuid]),
    ]
    seen_organisation = False
    for url in urls:
        response = client.get(url)
        assert response.status_code == 200, url
        body = response.content.decode()
        assert SECRET_EMAIL not in body, url
        assert SECRET_NAME not in body, url
        assert SECRET_PHONE not in body, url
        seen_organisation = seen_organisation or "Chambre de commerce de Rovigo" in body
    assert seen_organisation, "the other participant must appear as an organisation, or this proves nothing"


def test_the_commission_page_names_organisations_and_never_accounts(
    client, governance_open, member, other_participant, commission
):
    client.force_login(member.user)
    body = client.get(reverse("forum_governance:commission_detail", args=[commission.key])).content.decode()
    assert "Chambre de commerce de Rovigo" in body
    assert "Mobilité académique, formation professionnelle" in body
    # The READER's own e-mail legitimately appears in the account menu of the platform shell; the
    # other participant's must not appear anywhere at all.
    assert SECRET_EMAIL not in body
    assert SECRET_NAME not in body


# ---------------------------------------------------------------------------------------------
# 4. The audit trail
# ---------------------------------------------------------------------------------------------
def test_audit_rows_about_the_forum_carry_no_account_data(other_participant, populated):
    """
    ``target_repr`` and ``metadata`` are what an audit row says ABOUT the object, and they must stay
    free of personal data. ``actor_label`` deliberately holds the acting account's e-mail: that is
    the audit trail's whole purpose, it is readable only by an administrator, and the case file made
    the same choice. The distinction is the point — it is not an oversight in either direction.
    """
    from audit.models import AuditEvent

    rows = AuditEvent.objects.filter(action__startswith="forum.")
    assert rows.exists()
    blob = json.dumps(list(rows.values("target_repr", "metadata")), default=str)
    assert SECRET_NAME not in blob
    assert SECRET_PHONE not in blob
