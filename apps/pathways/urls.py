from django.urls import path

from pathways import views

app_name = "pathways"

urlpatterns = [
    path("parcours/", views.index, name="index"),
    path("diplomes-et-titres/", views.diplomas, name="diplomas"),
    path("formation/", views.training, name="training"),
    path("parcours/<slug:key>/", views.detail, name="detail"),
]
