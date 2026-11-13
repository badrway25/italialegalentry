"""
Synthetic records must be impossible to create by accident.

`core.seeds.demonstration_data_allowed()` separates configuration seeds — taxonomies, flags, menus,
published editorial content — from seeds that manufacture PEOPLE: an account, a case file, a
help-desk request, a training plan. The first are the product. The second are invented, are
indistinguishable from real records once written, and the corrective directive forbids inventing
data to make a screen look populated.

The switch had a defect worth a test of its own: it defaults to DEBUG at the moment ``base`` is
imported, and ``test.py`` sets ``DEBUG = False`` AFTER that import. It therefore stayed True under
test settings — the exact opposite of what it exists for.
"""

from __future__ import annotations

import pytest
from django.conf import settings

from core.seeds import demonstration_data_allowed

pytestmark = pytest.mark.django_db


def test_the_switch_is_off_under_test_settings():
    assert settings.ILE_SEED_DEMONSTRATION_DATA is False
    assert demonstration_data_allowed() is False


def test_an_explicit_setting_wins_over_debug(settings):
    settings.DEBUG = True
    settings.ILE_SEED_DEMONSTRATION_DATA = False
    assert demonstration_data_allowed() is False


def test_it_falls_back_to_debug_when_the_setting_is_absent(settings):
    """A configuration written before the switch existed must keep behaving as it did."""
    del settings.ILE_SEED_DEMONSTRATION_DATA
    settings.DEBUG = False
    assert demonstration_data_allowed() is False
    settings.DEBUG = True
    assert demonstration_data_allowed() is True


def test_seed_all_creates_no_account_when_the_switch_is_off(django_user_model):
    """The assertion that matters: a full seed run invents nobody."""
    from django.core.management import call_command

    before = set(django_user_model.objects.values_list("email", flat=True))
    call_command("seed_all", verbosity=0)
    after = set(django_user_model.objects.values_list("email", flat=True))
    assert after == before, f"seed_all invented accounts: {sorted(after - before)}"


def test_seed_all_creates_no_case_file_when_the_switch_is_off():
    from django.core.management import call_command

    from cases.models import CaseFile

    before = CaseFile.objects.count()
    call_command("seed_all", verbosity=0)
    assert CaseFile.objects.count() == before


def test_the_gated_seeds_say_they_were_skipped():
    """A seed that silently does nothing is indistinguishable from one that is broken."""
    from academy.seeds import seed_demo_plan
    from selection.seeds import seed_selection_chain

    assert "skipped" in str(seed_selection_chain()).lower()
    assert "skipped" in str(seed_demo_plan()).lower()
