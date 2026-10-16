"""
`manage.py companies_demo` invents a company, its needs and an APPROVED account verification. It must refuse wherever
demonstration data is not allowed — every environment holding real people; the production settings pin the switch
off, the test settings too.

Until 12 October 2026 it had no guard: run under config.settings.prod it created everything, while the deployment
runbook said it refused (docs/design-v5/QA/v54/devops/VERIFY.md, finding 1).
"""

from __future__ import annotations

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError

from accounts.models import AccountVerification, VerificationStatus
from companies.models import CompanyNeed, CompanyProfile
from core.seeds import demonstration_data_allowed

pytestmark = pytest.mark.django_db


def test_it_refuses_where_demonstration_data_is_not_allowed(django_user_model):
    assert demonstration_data_allowed() is False  # the test settings, like the production ones
    user = django_user_model.objects.create_user(email="demo-target@example.test")
    with pytest.raises(CommandError, match="ILE_SEED_DEMONSTRATION_DATA"):
        call_command("companies_demo", account=user.email, verbosity=0)
    assert not CompanyProfile.objects.filter(organisation__memberships__user=user).exists()
    assert not CompanyNeed.objects.exists()
    assert not AccountVerification.objects.filter(user=user).exists()


def test_it_still_runs_where_demonstration_data_is_allowed(seeded, settings, django_user_model):
    settings.ILE_SEED_DEMONSTRATION_DATA = True
    user = django_user_model.objects.create_user(email="demo-target@example.test")
    call_command("companies_demo", account=user.email, verbosity=0)
    assert CompanyProfile.objects.filter(organisation__memberships__user=user).exists()
    assert CompanyNeed.objects.filter(company__organisation__memberships__user=user).exists()
    assert AccountVerification.objects.get(user=user).status == VerificationStatus.APPROVED
