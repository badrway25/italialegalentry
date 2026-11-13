"""
The project URLconf, with the Academy include guaranteed.

``config/urls.py`` belongs to the integrator, not to this lane. It now mounts the Academy at
``espace-reserve/formation/``; this module composes the real project URLconf and adds the include
only if it is absent, so the suite tests the routes as they are actually served and keeps working
if the mount point moves or is temporarily removed.

Used by ``@override_settings(ROOT_URLCONF="academy.tests.urls")`` and by
``pytest.mark.urls("academy.tests.urls")``. Never re-declares a partial URLconf: the platform shell
reverses ``pages:home``, ``portal:dashboard``, the account menu and the language switcher on every
page, so a partial one would test a page nobody will ever see.
"""

from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path

from config.urls import handler400, handler403, handler404, handler500  # noqa: F401
from config.urls import urlpatterns as project_urlpatterns

NAMESPACE = "academy"


def _is_mounted(patterns, depth: int = 2) -> bool:
    """True when ``academy`` is already mounted somewhere in these patterns (two levels is enough)."""
    for entry in patterns:
        if getattr(entry, "namespace", None) == NAMESPACE:
            return True
        nested = getattr(entry, "url_patterns", None) if depth > 0 else None
        if nested and _is_mounted(nested, depth - 1):
            return True
    return False


urlpatterns = list(project_urlpatterns)

if not _is_mounted(urlpatterns):  # pragma: no cover - only while the include is absent
    urlpatterns += i18n_patterns(
        path("espace-reserve/formation/", include("academy.urls", namespace=NAMESPACE)),
        prefix_default_language=True,
    )
