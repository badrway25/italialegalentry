"""
The company journey, through real HTTP.

ROLE_JOURNEYS §2 states the end-to-end test of this vertical:

    landing → exprimer un fabbisogno → compte entreprise → créer le besoin → le modifier
    → en voir l'état

which is what ``test_the_whole_company_journey`` walks, plus the verification gate the client made
an acceptance criterion: an unverified company prepares its needs but transmits nothing.

The routes are the real ones: ``config/urls.py`` mounts this vertical at
``espace-reserve/entreprise/``, under the reserved area and before the portal's own patterns.
"""

from __future__ import annotations

import pytest
from django.urls import reverse

from accounts.models import AccountVerification, VerificationStatus
from companies.models import CompanyNeed, CompanyProfile, NeedStatus

pytestmark = pytest.mark.django_db

PASSWORD = "Str0ng-Passw0rd-2026!"


@pytest.fixture
def logged_in(client):
    def _login(user):
        client.force_login(user)
        return client

    return _login


def test_the_workspace_requires_an_account(client) -> None:
    response = client.get(reverse("companies:dashboard"))
    assert response.status_code == 302
    assert "/compte/" in response["Location"] or "login" in response["Location"]


def test_the_pages_are_never_indexed_and_never_cached(logged_in, company_factory) -> None:
    _profile, user = company_factory("alpha")
    response = logged_in(user).get(reverse("companies:dashboard"))
    assert response.status_code == 200
    assert "noindex" in response.content.decode()
    assert "no-store" in response.headers.get("Cache-Control", "")


def test_the_whole_company_journey(logged_in, seeded, user_factory) -> None:
    """
    compte → déclarer l'entreprise → créer un besoin → le modifier → tenter de le transmettre
    (refusé tant que l'entreprise n'est pas vérifiée) → vérification → transmission → état.
    """
    from accounts import roles
    from companies.models import Sector, Territory

    user = user_factory("journey@example.test", role=roles.COMPANY)
    client = logged_in(user)
    sector = Sector.objects.get(code="batiment")
    territory = Territory.objects.get(code="veneto")

    # 1. an account with no company is told what to do first, and nothing else
    response = client.get(reverse("companies:dashboard"))
    assert response.status_code == 200
    assert "Déclarer mon entreprise" in response.content.decode()

    # 2. declaring the company creates the organisation, the membership and the verification request
    response = client.post(
        reverse("companies:profile_create"),
        {
            "legal_name": "Cantiere di prova S.r.l.",
            "trade_name": "",
            "registration_number": "RM-TEST-01",
            "vat_number": "",
            "sector": sector.pk,
            "size": "small",
            "year_founded": "2004",
            "contact_name": "Référent de test",
            "contact_function": "Responsable des ressources humaines",
            "contact_email": "referent@example.test",
            "contact_phone": "",
            "address_line": "",
            "postal_code": "",
            "city": "Rovigo",
            "province": "",
            "country": "IT",
            "website": "",
        },
        follow=True,
    )
    assert response.status_code == 200
    profile = CompanyProfile.objects.get(legal_name="Cantiere di prova S.r.l.")
    assert profile.organisation.memberships.filter(user=user).exists()
    assert AccountVerification.objects.filter(user=user).exists()
    assert profile.is_verified is False

    # 3. a need is created — as a draft
    response = client.post(
        reverse("companies:need_create"),
        {
            "title": "Conduite d’engins de chantier",
            "territory": territory.pk,
            "work_place": "Province de Rovigo",
            "sector": sector.pk,
            "professional_profile": "Conducteur d’engins",
            "duties": "Conduite de pelle et de chargeuse sur chantiers de voirie.",
            "engagement_type": "fixed_term",
            "headcount": "4",
            "experience_years_min": "1",
            "experience_note": "",
            "language_code": "it",
            "language_level": "a2",
            "language_note": "",
            "safety_training_note": "",
            "training_needs": "Module de sécurité de chantier.",
            "start_from": "",
            "timing_note": "",
            "mandatory_skills": "Conduite de pelle hydraulique\nContrôle quotidien de l’engin",
            "preferred_skills": "Lecture de plan de voirie",
        },
        follow=True,
    )
    assert response.status_code == 200
    need = CompanyNeed.objects.get(company=profile)
    assert need.status == NeedStatus.DRAFT
    assert need.mandatory_skills().count() == 2
    assert need.preferred_skills().count() == 1

    # 4. the need is editable, and the edit is kept
    response = client.post(
        reverse("companies:need_edit", args=[need.reference]),
        {
            "title": "Conduite d’engins de chantier (voirie)",
            "territory": territory.pk,
            "work_place": "Province de Rovigo",
            "sector": sector.pk,
            "professional_profile": "Conducteur d’engins de terrassement",
            "duties": "Conduite de pelle et de chargeuse, contrôle quotidien de l’engin.",
            "engagement_type": "fixed_term",
            "headcount": "6",
            "experience_years_min": "1",
            "experience_note": "",
            "language_code": "it",
            "language_level": "a2",
            "language_note": "",
            "safety_training_required": "on",
            "safety_training_note": "Attestation de conduite en sécurité exigée.",
            "training_needs": "Module de sécurité de chantier.",
            "start_from": "",
            "timing_note": "",
            "mandatory_skills": "Conduite de pelle hydraulique\nContrôle quotidien de l’engin",
            "preferred_skills": "Lecture de plan de voirie",
        },
        follow=True,
    )
    assert response.status_code == 200
    need.refresh_from_db()
    assert need.headcount == 6
    assert need.safety_training_required is True

    # 5. transmission is refused while the company is not verified
    response = client.post(reverse("companies:need_submit", args=[need.reference]))
    assert response.status_code == 403
    need.refresh_from_db()
    assert need.status == NeedStatus.DRAFT

    # 6. the project verifies the company — a decision taken in accounts, never here
    verification = AccountVerification.objects.get(user=user)
    verification.status = VerificationStatus.APPROVED
    verification.save(update_fields=["status"])

    # 7. transmission now works, and the state is visible on the need
    response = client.post(reverse("companies:need_submit", args=[need.reference]), follow=True)
    assert response.status_code == 200
    need.refresh_from_db()
    assert need.status == NeedStatus.SUBMITTED
    body = response.content.decode()
    assert str(NeedStatus.SUBMITTED.label) in body
    assert need.reference in body

    # 8. and the register on the dashboard shows the need with its state
    response = client.get(reverse("companies:dashboard"))
    dashboard = response.content.decode()
    assert "Conduite d’engins de chantier (voirie)" in dashboard
    assert str(NeedStatus.SUBMITTED.label) in dashboard


def test_a_need_of_another_company_answers_404(logged_in, company_factory, need_factory) -> None:
    _alpha, alpha_user = company_factory("alpha")
    beta, _beta_user = company_factory("beta")
    beta_need = need_factory(beta, title="Besoin de beta")
    response = logged_in(alpha_user).get(reverse("companies:need_detail", args=[beta_need.reference]))
    assert response.status_code == 404


def test_a_company_cannot_edit_another_company_s_need(logged_in, company_factory, need_factory) -> None:
    _alpha, alpha_user = company_factory("alpha")
    beta, _beta_user = company_factory("beta")
    beta_need = need_factory(beta)
    response = logged_in(alpha_user).post(
        reverse("companies:need_edit", args=[beta_need.reference]), {"title": "Détourné"}
    )
    assert response.status_code == 404
    beta_need.refresh_from_db()
    assert beta_need.title != "Détourné"


def test_an_age_criterion_typed_into_a_need_is_refused_with_an_explanation(
    logged_in, company_factory, territory, sector
) -> None:
    profile, user = company_factory("alpha")
    response = logged_in(user).post(
        reverse("companies:need_create"),
        {
            "title": "Manœuvre polyvalent",
            "territory": territory.pk,
            "sector": sector.pk,
            "professional_profile": "Manœuvre",
            "duties": "Travaux de manutention. Profil recherché : 20-45.",
            "headcount": "5",
            "experience_years_min": "0",
            "language_level": "none",
            "mandatory_skills": "Manutention",
            "preferred_skills": "",
        },
    )
    assert response.status_code == 200
    body = response.content.decode()
    assert "discrimination" in body
    assert CompanyNeed.objects.filter(company=profile).count() == 0


def test_the_aggregate_page_is_closed_to_a_company_and_open_to_the_project(
    logged_in, company_factory, need_factory, staff_user
) -> None:
    profile, user = company_factory("alpha")
    from companies import services

    need = need_factory(profile)
    services.submit(need, actor=user)

    assert logged_in(user).get(reverse("companies:analysis")).status_code == 403

    response = logged_in(staff_user).get(reverse("companies:analysis"))
    assert response.status_code == 200
    body = response.content.decode()
    assert "Vénétie" in body
    # counts only: never a company name, never a need title, never a reference
    assert profile.legal_name not in body
    assert need.title not in body
    assert need.reference not in body


def test_the_analysis_entry_is_absent_from_a_company_s_navigation(logged_in, company_factory) -> None:
    """A module a role cannot use is not shown merely because it exists in the code."""
    _profile, user = company_factory("alpha")
    body = logged_in(user).get(reverse("companies:dashboard")).content.decode()
    assert reverse("companies:analysis") not in body


def test_the_company_s_own_entries_are_absent_from_a_project_reader_s_navigation(
    logged_in, company_factory, need_factory, staff_user
) -> None:
    """
    « Mes besoins » and « Mon entreprise » lead to the declaration form for an account that has no
    company: offering them on the aggregate page invited a project reader to declare an entreprise.
    """
    profile, _user = company_factory("alpha")
    need_factory(profile)
    response = logged_in(staff_user).get(reverse("companies:analysis"))
    keys = [entry["key"] for entry in response.context["portal_nav"]]
    assert "analysis" in keys
    assert "needs" not in keys
    assert "profile" not in keys
    assert "dashboard" not in keys


def test_a_company_keeps_its_own_entries(logged_in, company_factory) -> None:
    _profile, user = company_factory("alpha")
    response = logged_in(user).get(reverse("companies:dashboard"))
    keys = [entry["key"] for entry in response.context["portal_nav"]]
    assert keys[:3] == ["dashboard", "needs", "profile"]
    assert "analysis" not in keys


def test_an_account_with_no_company_is_offered_the_workspace_root_and_nothing_more(logged_in, user_factory) -> None:
    """A prospective company keeps the root — that is where the declaration is offered."""
    from accounts import roles

    user = user_factory("prospect@example.test", role=roles.PERSON)
    response = logged_in(user).get(reverse("companies:dashboard"))
    keys = [entry["key"] for entry in response.context["portal_nav"]]
    assert "dashboard" in keys
    assert "needs" not in keys and "profile" not in keys


def test_the_workspace_renders_in_arabic_with_rtl(logged_in, seeded, company_factory, need_factory) -> None:
    profile, user = company_factory("alpha")
    need_factory(profile)
    client = logged_in(user)
    response = client.get("/ar" + reverse("companies:dashboard")[3:])
    assert response.status_code == 200
    body = response.content.decode()
    assert 'dir="rtl"' in body
    assert "is-rtl" in body


def test_every_page_of_this_vertical_has_exactly_one_h1(logged_in, company_factory, need_factory, staff_user) -> None:
    """One h1 per page, and it names what the page is about — never zero, never two."""
    import re

    profile, user = company_factory("alpha")
    need = need_factory(profile)
    pages = {
        "dashboard": (user, reverse("companies:dashboard")),
        "needs": (user, reverse("companies:needs")),
        "profile": (user, reverse("companies:profile")),
        "profile_edit": (user, reverse("companies:profile_edit")),
        "need_detail": (user, reverse("companies:need_detail", args=[need.reference])),
        "need_create": (user, reverse("companies:need_create")),
        "need_edit": (user, reverse("companies:need_edit", args=[need.reference])),
        "analysis": (staff_user, reverse("companies:analysis")),
    }
    counts = {}
    for key, (account, url) in pages.items():
        response = logged_in(account).get(url)
        assert response.status_code == 200, (key, response.status_code)
        counts[key] = len(re.findall(r"<h1[\s>]", response.content.decode()))
    assert all(value == 1 for value in counts.values()), counts
