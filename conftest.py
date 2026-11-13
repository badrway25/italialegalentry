"""
Project-wide pytest configuration (applies to ``tests/`` and to every ``apps/*/tests``).

Test isolation for the ACTIVE LANGUAGE: Django's LocaleMiddleware activates the language of each
request in the current thread and never resets it, so a test that requested ``/ar/…`` left Arabic
active for the next test. Any later ``reverse()`` outside a request then produced ``/ar/…`` URLs and
order-dependent failures (seen on the back-office MFA redirect test once the real-login tests, which
end with Arabic, ran before it).

The browser tests' LIVE SERVER listens on a port Chromium accepts, drawn and bound in a high range
(tests/live_server.py): pytest-django's own fixture let the operating system choose, and this machine's
dynamic range starts at 1024, among the ports Chromium refuses (net::ERR_UNSAFE_PORT).
"""

import pytest
from django.conf import settings
from django.utils import translation

from tests.live_server import live_server, pytest_terminal_summary  # noqa: F401 — the fixture and its summary line


@pytest.fixture(autouse=True)
def _reset_active_language():
    translation.activate(settings.LANGUAGE_CODE)
    yield
    translation.activate(settings.LANGUAGE_CODE)
