"""
Test URLconf: the project's own routes PLUS the governance mount this lane does not own.

``config/urls.py`` belongs to another lane, so the include that puts the module at
``espace-reserve/forum-permanent/`` is requested as a shared-file change rather than written. The
tests still have to exercise real routes — a module whose views are only called as functions has not
been shown to work — so they mount it here with ``@pytest.mark.urls("forum.tests.governance_urlconf")``.

The governance patterns come FIRST and the project's own patterns follow unchanged: a request that
does not match the governance prefix falls through to the real resolver, so ``{% url 'portal:…' %}``,
``{% safe_url 'legal:privacy' %}`` and the breadcrumb's ``pages:home`` all resolve exactly as they do
in production. Nothing in ``config.urls`` is mutated; the two lists are merely concatenated.

This file is NOT a test module (``python_files = test_*.py``), so pytest never collects it.
"""

from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path

from config.urls import handler400, handler403, handler404, handler500  # noqa: F401 — error views
from config.urls import urlpatterns as project_urlpatterns

GOVERNANCE_PREFIX = "espace-reserve/forum-permanent/"

urlpatterns = [
    *i18n_patterns(
        path(GOVERNANCE_PREFIX, include("forum.governance_urls", namespace="forum_governance")),
        prefix_default_language=True,
    ),
    *project_urlpatterns,
]
