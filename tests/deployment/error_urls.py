"""
URLconf of tests/deployment/test_error_pages_with_debug_off.py: the project's own patterns and handlers, plus four
views that fail on purpose, so that each error page is reached the way production reaches it — through Django's
exception handling and the project's handlers — rather than by rendering its template directly.
"""

from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.urls import path

from config.urls import handler400, handler403, handler404, handler500  # noqa: F401 — the handlers under test
from config.urls import urlpatterns as project_urlpatterns
from core.views import error_429


def fails_with_500(request):
    raise RuntimeError("synthetic failure: tests/deployment/test_error_pages_with_debug_off.py")


def fails_with_403(request):
    raise PermissionDenied


def fails_with_400(request):
    raise SuspiciousOperation("synthetic: tests/deployment/test_error_pages_with_debug_off.py")


def answers_429(request):
    return error_429(request)


urlpatterns = [
    path("__errors__/500/", fails_with_500),
    path("__errors__/403/", fails_with_403),
    path("__errors__/400/", fails_with_400),
    path("__errors__/429/", answers_429),
    *project_urlpatterns,
]
