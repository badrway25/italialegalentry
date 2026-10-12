"""
Routes of the V5 live preview. Mounted at ``/__design-v5/`` by config/urls.py — inside its
``if settings.DEBUG:`` block and only when ``settings.ILE_DESIGN_PREVIEW`` is true.

Since V5.4 (plan §4): the live product at the root, the index one click away, the persona switch,
the states without a URL of their own, the families' CD decisions, the foundation's specimen
boards — and the research archive under ``research/``, whose old addresses redirect.
"""

from django.urls import path

from designpreview import views

app_name = "designpreview"

urlpatterns = [
    # The live product.
    path("", views.landing, name="landing"),
    path("index/", views.index, name="index"),
    path("accedi/<slug:persona>/", views.persona_enter, name="persona_enter"),
    path("esci/", views.persona_exit, name="persona_exit"),
    path("stati/<slug:code>/", views.state, name="state"),
    path("decisioni/<path:path>", views.decision, name="decision"),
    path("specimens/<slug:board>/", views.specimen, name="specimen"),
    # The research archive (plan §4.2).
    path("research/", views.hub, name="hub"),
    path("research/hero/", views.hero, name="hero"),
    path("research/type/", views.type_systems, name="type"),
    path("research/compare/", views.compare, name="compare"),
    path("research/proof/<path:path>", views.proof, name="proof"),
    # The archive's addresses before V5.4: 302 to their research/ equivalents.
    path("hero/", views.legacy, {"target": "hero"}, name="legacy_hero"),
    path("type/", views.legacy, {"target": "type"}, name="legacy_type"),
    path("compare/", views.legacy, {"target": "compare"}, name="legacy_compare"),
    path("proof/<path:path>", views.legacy, {"target": "proof"}, name="legacy_proof"),
]
