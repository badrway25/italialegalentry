"""
Academy URLs.

Every route requires an authenticated account, so none of them is registered in
``core.public_routes`` (the registry of pages that must answer 200 to an anonymous crawler).

The include belongs to ``config/urls.py``, which this lane does not own; it is requested in the
result as a shared-file change:

    path("academy/", include("academy.urls", namespace="academy")),   # inside i18n_patterns
"""

from django.urls import path

from academy import views

app_name = "academy"

urlpatterns = [
    path("", views.catalogue, name="catalogue"),
    path("cours/<slug:slug>/", views.course_detail, name="course"),
    path("cours/<slug:slug>/inscription/", views.enrol, name="enrol"),
    path("mes-formations/", views.mine, name="mine"),
    path("mes-formations/<uuid:uuid>/", views.enrolment_detail, name="enrolment"),
    path("mes-formations/<uuid:uuid>/module/<int:module_pk>/suivi/", views.attend, name="attend"),
    path("mes-formations/<uuid:uuid>/interrompre/", views.withdraw, name="withdraw"),
    path("mes-formations/<uuid:uuid>/reprendre/", views.resume, name="resume"),
    path("plan/<uuid:uuid>/", views.plan_detail, name="plan"),
]
