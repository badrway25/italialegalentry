"""
Routes of authorised selection. All authenticated, none public, none indexable.

Mounted at ``espace-reserve/selection/`` inside ``i18n_patterns``, before the portal's own
``espace-reserve/`` include so the module's paths are never swallowed by it. Nothing is registered
in ``core.public_routes``: this module must never appear on a public page (CR-03).
"""

from django.urls import path

from selection import views

app_name = "selection"

urlpatterns = [
    path("", views.workspace, name="workspace"),
    path("communications-identite/", views.disclosures, name="disclosures"),
    path("communications-identite/<uuid:uuid>/decision/", views.decide_disclosure, name="decide_disclosure"),
    path("<uuid:uuid>/", views.process_detail, name="process"),
    path("<uuid:uuid>/phase/", views.advance_stage, name="advance"),
    path("<uuid:uuid>/cloture/", views.conclude_process, name="conclude"),
    path("<uuid:uuid>/justificatif/<int:pk>/", views.evidence_status, name="evidence"),
    path("<uuid:uuid>/identite/demande/", views.request_identity, name="request_identity"),
    path("<uuid:uuid>/identite/", views.identity, name="identity"),
]
