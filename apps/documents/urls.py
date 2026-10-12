"""
Document URLs — language-neutral (config.urls mounts them outside ``i18n_patterns``).

Two entry points and two exits, and no others:
  in   POST /documents/requirements/<uuid>/file/   (against a named requirement)
       POST /documents/upload/                     (a personal file answering no requirement)
  out  GET  /documents/<uuid>/                     (direct, authorised)
       GET  /documents/link/<token>/               (signed, time-limited, account-bound)
"""

from django.urls import path

from documents import views

app_name = "documents"

urlpatterns = [
    path("", views.index, name="index"),
    path("upload/", views.upload, name="upload"),
    path("requirements/<uuid:pk>/", views.requirement_detail, name="requirement"),
    path("requirements/<uuid:pk>/file/", views.requirement_file, name="requirement_file"),
    path("requirements/<uuid:pk>/review/", views.requirement_review, name="requirement_review"),
    path("link/<str:token>/", views.signed_download, name="signed_download"),
    path("<uuid:pk>/", views.download, name="download"),
    path("<uuid:pk>/delete/", views.delete, name="delete"),
]
