from django.urls import path

from news import views

app_name = "news"

urlpatterns = [
    path("", views.index, name="index"),
    path("lettre-d-information/", views.newsletter_subscribe, name="newsletter_subscribe"),
    path("<slug:slug>/", views.detail, name="detail"),
]
