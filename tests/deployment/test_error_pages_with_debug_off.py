"""
The error pages, reached the way production reaches them: DEBUG off, a view that fails, Django's exception handling,
the project's handlers (config.urls handler400/403/404/500, core.views.error_429).

tests/frontend/test_layout.py renders the templates directly; this module proves the path a visitor takes. Each
answer must carry the right status, the product's page (not Django's technical page or a bare server page) and no
trace of the failure: no traceback, no request dump, no settings — the DEBUG-leak half of the release gate.
"""

from __future__ import annotations

import pytest
from django.test import Client, override_settings

pytestmark = [pytest.mark.django_db, pytest.mark.security]

URLCONF = "tests.deployment.error_urls"

#: What Django's technical pages print and the product's pages never do.
LEAKS = ("Traceback", "Request Method", "Exception Value", "SECRET_KEY", "synthetic failure", "INSTALLED_APPS")


@override_settings(ROOT_URLCONF=URLCONF, DEBUG=False)
def test_every_error_page_is_the_products_own_with_debug_off(seeded):
    client = Client(raise_request_exception=False)
    for path, status in (
        ("/__errors__/400/", 400),
        ("/__errors__/403/", 403),
        ("/fr/page-inesistente/", 404),
        ("/__errors__/429/", 429),
        ("/__errors__/500/", 500),
    ):
        response = client.get(path)
        html = response.content.decode("utf-8")
        assert response.status_code == status, (path, response.status_code)
        assert 'class="container error-page"' in html, f"{path}: not the product's error page"
        assert html.count("<h1") == 1, path
        for leak in LEAKS:
            assert leak not in html, f"{path} leaks {leak!r}"
    # The 500 page names the request id, so support can find the log line without any personal data.
    response = client.get("/__errors__/500/", HTTP_X_REQUEST_ID="abc123def456")
    assert "abc123def456" in response.content.decode("utf-8")


@override_settings(ROOT_URLCONF=URLCONF, DEBUG=False)
def test_a_request_for_an_unknown_host_gets_the_400_page(seeded):
    """
    A Host outside ALLOWED_HOSTS: Django answers 400 through the project's handler, and the page renders.

    Until W3-F2 it did not: templates/partials/seo_head.html computes request.get_host, so the 400 page raised
    DisallowedHost again, then the 500 handler did, and the WSGI server answered with its own bare 500 (the DevOps
    lane's finding F-6, held here as a strict xfail until the devops merge). W3-F2 draws the 400 and 500 pages
    without the request (core.views._self_sufficient), so they no longer ask for its host. nginx's catch-all
    server (runbook, step 11) still keeps such requests away from Django.
    """
    response = Client(raise_request_exception=False).get("/fr/", HTTP_HOST="unknown-host.invalid")
    html = response.content.decode("utf-8")
    assert response.status_code == 400
    assert 'class="container error-page"' in html
    for leak in LEAKS:
        assert leak not in html, f"the 400 page leaks {leak!r}"
