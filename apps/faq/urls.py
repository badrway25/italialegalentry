from django.urls import path

from faq import views

app_name = "faq"

urlpatterns = [
    path("", views.index, name="index"),
]
