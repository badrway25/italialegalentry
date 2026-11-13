"""
A public page must never link to a page that answers 404 because its gate is closed.

Found by browser QA (2026-09-20): the collaboration forms linked back to ``/institutions/`` and
``/universites-et-formation/`` while those Phase 3 pages were still gated.
"""

import re

import pytest
from django.conf import settings

from core.links import gate_is_open, path_is_open, public_url
from core.public_routes import all_routes, gated_routes, ungated_paths

pytestmark = [pytest.mark.compliance, pytest.mark.django_db]

LANGS = [code for code, _ in settings.LANGUAGES]
HREF = re.compile(r'href="(/[a-z]{2}/[^"#?]*)')


def test_public_url_hides_gated_targets_until_the_gate_opens(seeded, set_flag):
    assert gate_is_open("") is True
    gated = [r for r in gated_routes() if r.requires_gate == "phase3_public"]
    assert gated, "Phase 3 routes must be registered with requires_gate"
    assert path_is_open(f"/fr/{gated[0].path}") is False
    assert public_url("ecosystem:institutions") == ""
    assert public_url("does:not_exist") == ""
    assert public_url("legal:privacy") == "/fr/privacy-policy/"


def test_public_url_returns_the_url_once_phase3_is_open(seeded, phase3_open):
    assert public_url("ecosystem:institutions").endswith("/institutions/")
    assert public_url("faq:index").endswith("/faq/")


def _closed_paths() -> set[str]:
    return {r.path for r in all_routes() if r.requires_gate and not gate_is_open(r.requires_gate)}


@pytest.mark.parametrize("lang", LANGS)
def test_no_open_page_links_to_a_closed_page(client, seeded, lang):
    closed = _closed_paths()
    assert closed, "with default flags the Phase 3 pages are closed"
    offenders = []
    for path in ungated_paths():
        response = client.get(f"/{lang}/{path}")
        if response.status_code != 200:
            continue
        for href in HREF.findall(response.content.decode()):
            relative = href.split("/", 2)[2] if href.count("/") >= 2 else ""
            if relative in closed:
                offenders.append((f"/{lang}/{path}", href))
    assert not offenders, offenders[:10]
