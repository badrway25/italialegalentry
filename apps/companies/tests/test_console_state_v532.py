"""
V5.32 lane E, correction round (the integration review's P2-8): a company refused inside its own space — the
territorial analysis is the project's, never a company's — stays in its space: the rail of «Espace entreprise», the
console's head, the trail «Espace entreprise › Accès non autorisé», the space's own «Tableau de bord» as the one
primary; no door, no public header (templates/errors/console_error.html, portal.services.console_state_shell).
"""

from __future__ import annotations

import re

import pytest
from django.urls import reverse
from django.utils import translation
from django.utils.html import escape

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_a_company_refused_inside_its_space_keeps_its_space(client, company_user, lang):
    client.force_login(company_user)
    with translation.override(lang):
        url, home = reverse("companies:analysis"), reverse("companies:dashboard")
        space, title = translation.gettext("Espace entreprise"), translation.gettext("Accès non autorisé")
        dashboard = translation.gettext("Tableau de bord")
    response = client.get(url)
    assert response.status_code == 403
    html = response.content.decode()
    assert 'id="console-rail"' in html and 'class="site-header"' not in html, "the console's frame, not the public one"
    assert "error-page__door" not in html and "cms/errori.css" not in html, "no door"
    assert f'<span class="rail__space" data-rail-space>{space}</span>' in html, "the company's own rail"
    bar = html.split('<div class="console-bar__crumbs">', 1)[1].split("</ol>", 1)[0]
    assert f'<a href="{home}">{space}</a>' in bar and f"<span>{escape(title)}</span>" in bar, "«<space> › the state»"
    main = html.split('<main id="main-content"', 1)[1].split("</main>", 1)[0]
    assert re.findall(r'<a class="btn btn--primary[^"]*" href="([^"]+)">(.*?)</a>', main, re.S) == [(home, dashboard)]
    assert re.findall(r"<h1\b[^>]*>(.*?)</h1>", html, re.S) == [escape(title)]
    assert lang == "fr" or space != "Espace entreprise", "the catalogue holds the words"
