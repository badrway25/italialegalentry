"""
Routes of the digital case file.

Mounted under the reserved area. A case is addressed by its REFERENCE, which is a non-sequential
ten-character string: a sequential identifier in a URL both leaks volume and invites the hand-typed
probe that `tests/security/test_object_permissions.py` §11 exists to defeat.

The include belongs in ``config/urls.py``, before the portal's own include:

    path("espace-reserve/dossiers/", include("cases.urls", namespace="cases")),
"""

from django.urls import path

from cases import views

app_name = "cases"

urlpatterns = [
    path("", views.index, name="index"),
    path("<slug:reference>/", views.detail, name="detail"),
    path("<slug:reference>/etat/", views.transition, name="transition"),
    path("<slug:reference>/ligne/<int:pk>/", views.set_item_status, name="set_item_status"),
    path("<slug:reference>/pre-evaluation/<int:pk>/", views.assessment_detail, name="assessment"),
]
