from django.urls import path

from pages import views

app_name = "pages"

# Paths relative to the language prefix — also used by AppConfig.ready() and the sitemap.
PUBLIC_PATHS = {
    "home": "",
    "project": "le-projet/",
    "agami": "agami/",
    "network": "reseau/",
    "contact": "contact/",
}
GATED_PATHS = {
    "antifraud": "attention-aux-fraudes/",
}

urlpatterns = [
    path(PUBLIC_PATHS["home"], views.home, name="home"),
    path(PUBLIC_PATHS["project"], views.project, name="project"),
    path(PUBLIC_PATHS["agami"], views.agami, name="agami"),
    path(PUBLIC_PATHS["network"], views.network, name="network"),
    path(PUBLIC_PATHS["contact"], views.contact, name="contact"),
    path(GATED_PATHS["antifraud"], views.antifraud, name="antifraud"),
]
