"""
The phase console's dependencies are enforced, not only displayed (W4-D part 2, A2 — part 1's F-3).

``core.phases`` declares ``depends_on=("legal_pages_available",)`` for the Virtual Forum (G11) and the newsletter, and
``console_rows`` tells the administrator that a closed dependency blocks the flag («a gate whose dependency is closed
cannot be opened by flipping its own flag»). ``core.gates`` read the two flags alone, so the flag switched on before
the legal pages opened the Virtual Forum — whose «Créer un compte» led to «Inscriptions fermées» — and the newsletter's
chapter. Both gates now also require ``legal_pages_available()``; the forms override (``forms_override_without_legal``)
opens G2's forms and nothing else.
"""

from __future__ import annotations

import pytest

from core import gates, phases

pytestmark = [pytest.mark.compliance, pytest.mark.django_db]

VIRTUAL_FORUM = "/fr/forum-virtuel/"
NEWS = "/fr/actualites/"


# ---------------------------------------------------------------------------------------------
# DENY: the flag alone opens nothing while the legal pages are not published
# ---------------------------------------------------------------------------------------------
def test_the_virtual_forum_stays_closed_without_the_legal_pages(seeded, set_flag, client):
    set_flag("virtual_forum", True)
    assert gates.legal_pages_available() is False
    assert gates.virtual_forum_enabled() is False
    assert client.get(VIRTUAL_FORUM).status_code == 404


def test_the_newsletter_stays_closed_without_the_legal_pages(seeded, set_flag, client):
    set_flag("newsletter", True)
    assert gates.newsletter_enabled() is False
    assert 'id="newsletter"' not in client.get(NEWS).content.decode()


def test_the_forms_override_opens_the_forms_not_these_two(seeded, set_flag):
    set_flag("forms_override_without_legal", True)
    set_flag("virtual_forum", True)
    set_flag("newsletter", True)
    assert gates.public_forms_enabled().open is True
    assert gates.virtual_forum_enabled() is False
    assert gates.newsletter_enabled() is False


# ---------------------------------------------------------------------------------------------
# ALLOW: with the legal pages published, the flag decides
# ---------------------------------------------------------------------------------------------
def test_the_virtual_forum_opens_with_its_flag_once_the_legal_pages_are_published(
    seeded, legal_published, set_flag, client
):
    assert gates.virtual_forum_enabled() is False, "the flag is still off"
    set_flag("virtual_forum", True)
    assert gates.virtual_forum_enabled() is True
    assert client.get(VIRTUAL_FORUM).status_code == 200


def test_the_newsletter_opens_with_its_flag_once_the_legal_pages_are_published(
    seeded, legal_published, set_flag, client
):
    set_flag("newsletter", True)
    assert gates.newsletter_enabled() is True
    html = client.get(NEWS).content.decode()
    assert 'id="newsletter"' in html
    assert 'action="/fr/actualites/lettre-d-information/"' in html, "the form is drawn: G2 is open with the pages"


# ---------------------------------------------------------------------------------------------
# The console and the gates agree
# ---------------------------------------------------------------------------------------------
def test_a_gate_the_console_says_is_blocked_is_closed(seeded, set_flag):
    """Every gate whose description names a dependency and a flag of its own: flag on, dependency closed → the console
    lists it as blocked AND the gate is closed. G2 is the one declared exception — its «flag» is the override that
    opens it without the legal pages (the console's own note on ``forms_override_without_legal``)."""
    checked = []
    for gate in phases.GATES:
        if not gate.depends_on or not gate.flag or gate.key == "public_forms_enabled":
            continue
        set_flag(gate.flag, True)
        row = next(r for r in phases.console_rows() if r["key"] == gate.key)
        assert row["blocked_by"], gate.key
        assert gates.snapshot()[gate.key] is False, f"{gate.key}: the console says blocked, the gate is open"
        checked.append(gate.key)
    assert sorted(checked) == ["newsletter_enabled", "virtual_forum_enabled"], checked
