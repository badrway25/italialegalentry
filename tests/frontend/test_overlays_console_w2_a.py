"""
The overlay system on the console's rendered pages — design V5, family W2-A, step 2 (the propagation;
docs/design-v5/V5_4_EXECUTION_PLAN.md §1.14, §3.4 item 1; docs/design-v5/QA/v54/w2-a/CONTRACT.md). What Django
renders, without a browser:

* the top bar's account is the system's popover — a real button, the panel a named group of the account's rows, the
  sign-out a form —, in French and in Arabic; the letterhead keeps design V4's details face until W2-C2;
* the drawer is a modal drawer of the system, «Menu» its link opener, the close control its «Fermer»;
* every row of the register has its menu as the system's popover, named by the piece's title, opened by «⋮» named by
  its tooltip; the dashboard's compact rows have none.

The behaviour in a browser is tests/frontend/test_overlays_console_browser_w2_a.py.
"""

from __future__ import annotations

import re

import pytest
from django.urls import reverse
from django.utils import translation

from accounts import roles

pytestmark = pytest.mark.django_db


@pytest.fixture
def person(user_factory):
    return user_factory("w2a-person@example.test", role=roles.PERSON, full_name="Personne de test")


@pytest.fixture
def requirement(person):
    """A piece the person must provide, on a case of their own."""
    from cases.models import CasePurpose, ResponsibleActor
    from cases.services import open_case
    from documents import services
    from documents.models import DocumentKind

    case = open_case(person, purpose=CasePurpose.WORK, pathway_key="salaried_work")
    return services.declare_requirement(
        case,
        code="identity_document",
        title="Passeport en cours de validité",
        responsible_actor=ResponsibleActor.PERSON,
        kind=DocumentKind.IDENTITY,
        source_title="D.lgs. 286/1998",
        source_ref="art. 4, comma 1",
    )


def _bar(html: str) -> str:
    return html.split('<header class="portal-bar console-bar"', 1)[1].split("</header>", 1)[0]


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_top_bar_s_account_is_the_systems_popover(client, seeded, person, lang):
    client.force_login(person)
    with translation.override(lang):
        url = reverse("portal:dashboard")
        account_label = translation.gettext("Mon compte")
        signout = translation.gettext("Se déconnecter")
    html = client.get(url).content.decode()
    bar = _bar(html)
    # named by the words it shows, then what it opens — two live strings (REVIEW m3; WCAG 2.5.3)
    name = f"{person.get_short_name()} — {account_label}"
    assert re.search(
        rf'<button class="account-menu__summary" type="button" popovertarget="console-account" '
        rf'aria-label="{re.escape(name)}">',
        bar,
    ), "the trigger's name: «‹short name› — Mon compte»"
    assert '<span class="account-menu__name">' in bar, "the short name, cut where its seat is short (overlays.css §9)"
    # as a phone sheet the menu says what it is: its name heads its rows, for the eye only (REVIEW M1)
    assert f'<p class="overlay__caption" aria-hidden="true">{account_label}</p>' in bar
    panel = bar.split('id="console-account"', 1)[1].split("</div>\n</div>", 1)[0]
    assert re.search(
        rf'<div class="overlay overlay--popover" id="console-account" data-overlay="popover" popover role="group" '
        rf'aria-label="{re.escape(account_label)}">',
        bar,
    ), "a named group of the account's rows"
    for name in ("portal:dashboard", "accounts:profile", "mfa_index"):
        with translation.override(lang):
            assert f'<a class="overlay__item" href="{reverse(name)}">' in panel, name
    with translation.override(lang):
        assert f'<form method="post" action="{reverse("account_logout")}">' in panel and "csrfmiddlewaretoken" in panel
    assert '<button class="overlay__item" type="submit">' in panel and signout in panel
    assert '<li class="overlay__sep" role="presentation"></li>' in panel
    assert "<details" not in bar and "account-menu__list" not in bar, "no V4 menu in the console"


def test_the_letterhead_holds_the_account_popover_since_w2_c2(client, seeded, person):
    client.force_login(person)
    html = client.get("/fr/").content.decode()
    # the targa's seat and the phone sheet's foot: the system's popover, never V4's <details> (W2-C2)
    assert "<details class=\"account-menu\"" not in html and "data-dropdown" not in html
    assert 'popovertarget="account-menu"' in html and 'popovertarget="account-menu-sheet"' in html
    assert html.count('data-overlay="popover"') == 2 and 'popovertarget="console-account"' not in html


def test_the_console_drawer_is_a_modal_drawer_of_the_system(client, seeded, person):
    client.force_login(person)
    html = client.get(reverse("portal:requests")).content.decode()
    assert re.search(
        r'<dialog class="console-drawer overlay overlay--drawer" id="console-drawer" data-overlay="drawer" '
        r'data-overlay-edge="start" data-console-drawer aria-label="[^"]+">',
        html,
    )
    assert 'href="#console-drawer" data-console-menu data-overlay-open aria-controls="console-drawer"' in html
    assert 'href="#main-content" data-console-close data-overlay-close>' in html
    assert html.count('data-overlay="drawer"') == 1 and "data-overlay-modal" not in html, "one drawer, modal"


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_every_row_of_the_register_opens_its_piece_in_the_systems_drawer(client, seeded, person, requirement, lang):
    """Retargeted by W3-C (intent kept: the register's overlay is the system's): «Mes pièces» V5.2 has no row menu — the
    row is the link (DOCUMENT_WORKSPACE D2) — and the piece opens in the system's drawer, non-modal beside the list."""
    client.force_login(person)
    with translation.override(lang):
        url = reverse("portal:documents")
        close = translation.gettext("Fermer")
    html = client.get(url).content.decode()
    assert "doc-row__more" not in html and "doc-menu" not in html, "no row menu"
    assert re.search(
        r'<dialog class="overlay overlay--drawer doc-drawer" id="piece-drawer" data-overlay="drawer" '
        r'data-overlay-modal="none"',
        html,
    ), "the system's drawer, beside the list"
    assert f'data-overlay-close aria-label="{close}"' in html
    assert f'href="/documents/requirements/{requirement.pk}/"' in html, "the row's title: the link the drawer takes"


def test_the_dashboards_compact_rows_draw_no_menu(client, seeded, person, requirement):
    client.force_login(person)
    html = client.get(reverse("portal:dashboard")).content.decode()
    assert "doc-row__more" not in html and "doc-menu-" not in html
