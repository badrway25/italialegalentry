"""
Project-wide pytest configuration (applies to ``tests/`` and to every ``apps/*/tests``).

Test isolation for the ACTIVE LANGUAGE: Django's LocaleMiddleware activates the language of each
request in the current thread and never resets it, so a test that requested ``/ar/…`` left Arabic
active for the next test. Any later ``reverse()`` outside a request then produced ``/ar/…`` URLs and
order-dependent failures (seen on the back-office MFA redirect test once the real-login tests, which
end with Arabic, ran before it).
"""

import pytest
from django.conf import settings
from django.utils import translation


@pytest.fixture(autouse=True)
def _reset_active_language():
    translation.activate(settings.LANGUAGE_CODE)
    yield
    translation.activate(settings.LANGUAGE_CODE)
