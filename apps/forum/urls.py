from django.urls import path

from forum import views

app_name = "forum"

urlpatterns = [
    path("", views.index, name="index"),
    path("inscription/", views.register, name="register"),
    path("inscription/confirmation/", views.register_done, name="register_done"),
]
