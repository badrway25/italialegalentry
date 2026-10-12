"""
Back-office shell: dedicated Content-Security-Policy and the publication-gate dashboard.

Regression (browser QA 2026-09-20): under the strict public policy the admin theme (Alpine.js) could
not evaluate its expressions — every panel, modal and dropdown was rendered at once.
"""

import pytest

pytestmark = pytest.mark.django_db


def _csp(response) -> dict[str, str]:
    header = response["Content-Security-Policy"]
    return {part.strip().split(" ", 1)[0]: part.strip() for part in header.split(";") if part.strip()}


def test_public_pages_keep_the_strict_policy(client, seeded):
    csp = _csp(client.get("/fr/"))
    assert csp["script-src"] == "script-src 'self'"
    assert csp["style-src"] == "style-src 'self'"
    assert "unsafe" not in client.get("/fr/")["Content-Security-Policy"]


@pytest.mark.security
def test_backoffice_policy_is_relaxed_but_same_origin_only(client, seeded):
    csp = _csp(client.get("/backoffice/login/"))
    assert "'unsafe-eval'" in csp["script-src"] and "'unsafe-inline'" in csp["script-src"]
    assert "'unsafe-inline'" in csp["style-src"]
    for directive in ("script-src", "style-src", "img-src", "font-src"):
        assert "http" not in csp[directive], f"{directive} must not allow any external origin"
    assert csp["frame-ancestors"] == "frame-ancestors 'none'"
    assert csp["default-src"] == "default-src 'self'"


@pytest.mark.security
def test_relaxed_policy_does_not_leak_outside_the_backoffice(client, seeded):
    for path in ("/fr/compte/login/", "/fr/forum/", "/fr/privacy-policy/", "/healthz/"):
        header = client.get(path).get("Content-Security-Policy", "")
        assert "unsafe" not in header, path


def test_dashboard_shows_the_publication_gates(client, seeded, superuser):
    client.force_login(superuser)
    html = client.get("/backoffice/").content.decode()
    assert 'id="ile-gates-title"' in html
    assert "BLOCKED_BY_MISSING_OFFICIAL_SOURCE" in html, "editors must see why public forms are disabled"
    assert html.count("CHIUSO") + html.count("FERMÉ") + html.count("CLOSED") >= 1


def test_dashboard_reflects_published_legal_pages(client, seeded, superuser, legal_published):
    client.force_login(superuser)
    html = client.get("/backoffice/").content.decode()
    assert "BLOCKED_BY_MISSING_OFFICIAL_SOURCE" not in html
