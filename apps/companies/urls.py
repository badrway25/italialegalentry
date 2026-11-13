"""
Routes of the company workspace.

Every route is scoped to the caller's own company. A need is addressed by its REFERENCE, which is
non-sequential, and the lookup still runs through ``readable_by``: guessing a reference does not
reach another company's need, it returns the same 404 as a reference that does not exist.

There is deliberately no route that takes a person identifier, and no route that lists persons.
"""

from django.urls import path

from companies import views

app_name = "companies"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("mon-entreprise/", views.profile, name="profile"),
    path("mon-entreprise/declarer/", views.profile_create, name="profile_create"),
    path("mon-entreprise/modifier/", views.profile_edit, name="profile_edit"),
    path("mes-besoins/", views.needs, name="needs"),
    path("mes-besoins/nouveau/", views.need_create, name="need_create"),
    path("mes-besoins/<slug:reference>/", views.need_detail, name="need_detail"),
    path("mes-besoins/<slug:reference>/modifier/", views.need_edit, name="need_edit"),
    path("mes-besoins/<slug:reference>/transmettre/", views.need_submit, name="need_submit"),
    path("mes-besoins/<slug:reference>/retirer/", views.need_withdraw, name="need_withdraw"),
    path("analyse-territoriale/", views.analysis, name="analysis"),
]
