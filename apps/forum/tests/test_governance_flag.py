"""
Gate G11: while ``virtual_forum`` is closed, the governance module does not exist for anybody.

« Nobody » is the whole point of this file, so it is enumerated rather than assumed: anonymous, a
participant, a member with a live mandate, a table referent, the secretariat of the edition, an
institutional observer, a STAFF account that is not a superadmin, an administrator, and a superuser.
A gate that every role respects except the one with the most privileges is not a gate.

The refusal is the one the reserved area gives for a closed module — HTTP 503 with the « espace
momentanément indisponible » page — and it is given BEFORE authentication, so an anonymous visitor
is not sent to a login page that opens onto nothing.

The last test in the file opens the flag and walks the same routes, so a green run here is evidence
that the routes are closed rather than merely broken.
"""

from __future__ import annotations

import pytest
from django.urls import reverse

from accounts import roles
from core import flags, gates
from forum import governance_services as services
from forum.governance import Table, TableStatus

pytestmark = [pytest.mark.django_db, pytest.mark.urls("forum.tests.governance_urlconf")]

BODY = "Proposition de coopération entre les chambres consulaires, avec un calendrier annuel partagé."


@pytest.fixture
def every_route(member, referent, commission):
    """One concrete URL per declared route of the module — nothing skipped, nothing invented."""
    table = Table.objects.create(commission=commission, key="table-g11", title_fr="Table", status=TableStatus.OPEN)
    proposal = services.open_proposal(member.user, commission, title_fr="Proposition de test", body_fr=BODY)
    services.transition_proposal(proposal, "submitted", actor=member.user)
    services.transition_proposal(proposal, "under_review", actor=referent.user)
    services.transition_proposal(proposal, "accepted", actor=referent.user, note="Retenue.")
    project = services.promote_to_project(proposal, lead=member.profile, actor=referent.user)
    return [
        reverse("forum_governance:participation"),
        reverse("forum_governance:commissions"),
        reverse("forum_governance:commission_detail", args=[commission.key]),
        reverse("forum_governance:proposal_create", args=[commission.key]),
        reverse("forum_governance:table_detail", args=[commission.key, table.key]),
        reverse("forum_governance:proposals"),
        reverse("forum_governance:proposal_detail", args=[proposal.uuid]),
        reverse("forum_governance:projects"),
        reverse("forum_governance:project_detail", args=[project.uuid]),
        reverse("forum_governance:annual_report"),
        reverse("forum_governance:annual_report_year", args=[2026]),
    ]


@pytest.fixture
def every_role(django_user_model, member, referent, secretariat, observer, outsider):
    roles.ensure_roles()
    staff = django_user_model.objects.create_user(email="staff.g11@example.test", password="x", is_staff=True)
    roles.assign_role(staff, roles.STAFF)
    administrator = django_user_model.objects.create_user(email="admin.g11@example.test", password="x", is_staff=True)
    roles.assign_role(administrator, roles.ADMINISTRATOR)
    root = django_user_model.objects.create_superuser(email="root.g11@example.test", password="x")
    return {
        "member": member.user,
        "referent": referent.user,
        "secretariat": secretariat.user,
        "observer": observer.user,
        "outsider": outsider,
        "staff": staff,
        "administrator": administrator,
        "superuser": root,
    }


def test_the_gate_is_closed_by_default(db):
    assert gates.virtual_forum_enabled() is False
    assert services.governance_enabled() is False


def test_the_module_is_unreachable_for_anonymous_visitors(client, every_route, commission):
    """
    503 everywhere, and no governance CONTENT in the body.

    The path itself does appear — the language switcher rewrites the current URL into the other
    three languages, on every page of the site — so the assertion is about what the page SAYS: no
    commission name, no proposal, nothing the gate exists to keep shut.
    """
    for url in every_route:
        response = client.get(url)
        assert response.status_code == 503, url
        body = response.content.decode()
        assert commission.name_fr not in body
        assert "Proposition de test" not in body


def test_the_module_is_unreachable_for_every_role(client, every_route, every_role):
    for label, user in every_role.items():
        client.force_login(user)
        for url in every_route:
            response = client.get(url)
            assert response.status_code == 503, f"{label} reached {url}"
        client.logout()


def test_a_post_is_refused_too(client, every_route, member, commission):
    """A closed module refuses writes as well as reads, and refuses them the same way."""
    client.force_login(member.user)
    response = client.post(reverse("forum_governance:proposal_create", args=[commission.key]), {})
    assert response.status_code == 503


def test_the_closed_page_is_honest_about_why(client, every_route):
    """
    « Pas encore ouvert », not « en maintenance ».

    The reserved area's own page says maintenance because the reserved area HAS been available; this
    module never has, and calling that maintenance would be a small lie told at scale. No date is
    announced either: the gate depends on a decision and on the legal pages, not on a calendar entry.
    """
    body = client.get(every_route[0]).content.decode()
    assert "momentanément indisponible" in body
    assert "n’est pas encore ouvert" in body
    assert "maintenance" not in body


def test_the_closed_response_is_noindex(client, every_route):
    response = client.get(every_route[0])
    assert response["X-Robots-Tag"] == "noindex, nofollow"


def test_opening_the_flag_opens_the_module(client, every_route, secretariat, set_flag, governance_edition):
    """The control: with the gate open the same routes answer, so the 503s above are the gate."""
    set_flag(services.GOVERNANCE_FLAG, True)
    flags.invalidate()
    services.generate_annual_report(governance_edition, actor=secretariat.user)
    client.force_login(secretariat.user)
    for url in every_route:
        response = client.get(url)
        assert response.status_code == 200, f"{url} answered {response.status_code}"
