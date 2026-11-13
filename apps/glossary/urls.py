from django.urls import path

from glossary import views

app_name = "glossary"

urlpatterns = [
    path("", views.index, name="index"),
    path("<slug:slug>/", views.term, name="term"),
]
