from django.urls import path

from living import views

app_name = "living"

urlpatterns = [
    path("", views.index, name="index"),
    path("<slug:slug>/", views.topic, name="topic"),
    path("<slug:topic>/<slug:slug>/", views.sheet, name="sheet"),
]
