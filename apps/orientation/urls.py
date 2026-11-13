from django.urls import path

from orientation import views

app_name = "orientation"

urlpatterns = [
    path("", views.start, name="start"),
    path("reprendre/", views.resume, name="resume"),
    path("session/<uuid:session_id>/", views.step, name="step"),
    path("session/<uuid:session_id>/resultat/", views.result, name="result"),
    path("session/<uuid:session_id>/enregistrer/", views.save, name="save"),
    path("session/<uuid:session_id>/recommencer/", views.restart, name="restart"),
]
