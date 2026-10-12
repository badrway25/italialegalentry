"""
Root URL configuration.

Public pages live under i18n_patterns (/it/, /fr/, /en/, /ar/). Technical endpoints
(health, robots, sitemap, admin, private document download) are language-neutral.
"""

from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.i18n import set_language

from core import views as core_views
from core.sitemaps import SITEMAPS

handler400 = "core.views.error_400"
handler403 = "core.views.error_403"
handler404 = "core.views.error_404"
handler500 = "core.views.error_500"

urlpatterns = [
    path("healthz/", core_views.healthz, name="healthz"),
    path("robots.txt", core_views.robots_txt, name="robots_txt"),
    path("sitemap.xml", sitemap, {"sitemaps": SITEMAPS}, name="django.contrib.sitemaps.views.sitemap"),
    path("i18n/setlang/", set_language, name="set_language"),
    path("backoffice/", admin.site.urls),
    path("documents/", include("documents.urls", namespace="documents")),
    path("api/", include("integrations.urls", namespace="integrations")),
    path("", core_views.root_redirect, name="root"),
]

urlpatterns += i18n_patterns(
    path("", include("pages.urls", namespace="pages")),
    path("", include("legal.urls", namespace="legal")),
    path("", include("ecosystem.urls", namespace="ecosystem")),
    path("", include("enquiries.urls", namespace="enquiries")),
    path("", include("pathways.urls", namespace="pathways")),
    path("orientation/", include("orientation.urls", namespace="orientation")),
    path("forum/", include("forum.urls", namespace="forum")),
    path("forum-virtuel/", include("community.urls", namespace="community")),
    path("actualites/", include("news.urls", namespace="news")),
    path("faq/", include("faq.urls", namespace="faq")),
    path("glossaire/", include("glossary.urls", namespace="glossary")),
    path("vivre-en-italie/", include("living.urls", namespace="living")),
    path("partenaires/", include("partners.urls", namespace="partners")),
    # The platform modules mount UNDER the reserved area and BEFORE the portal's own catch-all
    # routes, so a module path is never swallowed by the portal. None of them is public, none is
    # indexed, and each enforces its own object-level authorisation — the mount point grants nothing.
    path("espace-reserve/dossiers/", include("cases.urls", namespace="cases")),
    path("espace-reserve/entreprise/", include("companies.urls", namespace="companies")),
    path("espace-reserve/selection/", include("selection.urls", namespace="selection")),
    path("espace-reserve/guichet/", include("helpdesk.urls", namespace="helpdesk")),
    path("espace-reserve/formation/", include("academy.urls", namespace="academy")),
    path("espace-reserve/forum-permanent/", include("forum.governance_urls", namespace="forum_governance")),
    path("espace-reserve/", include("portal.urls", namespace="portal")),
    path("compte/", include("accounts.urls", namespace="accounts")),
    path("compte/", include("allauth.urls")),
    path("consentements/", include("consents.urls", namespace="consents")),
    prefix_default_language=True,
)

if settings.DEBUG:
    # The import is INSIDE the guard, and that is the point: with DEBUG off, `core.dev` is never
    # imported, so the showcase view does not exist in the process at all. It is not a route that
    # answers 404 — it is code that was never loaded. The view checks `settings.DEBUG` a second
    # time regardless, because a URLconf is a file, and files get edited.
    from core import dev as core_dev

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path("_errors/400/", core_views.error_400),
        path("_errors/403/", core_views.error_403),
        path("_errors/404/", core_views.error_404),
        path("_errors/500/", core_views.error_500),
        path("_design/", core_dev.design_showcase, name="dev_design_showcase"),
    ]
