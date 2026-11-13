from django.urls import path

from accounts import views

app_name = "accounts"

urlpatterns = [
    path("profil/", views.profile, name="profile"),
    path("profil/export/", views.export_data, name="export_data"),
    path("profil/suppression/", views.delete_request, name="delete_request"),
    path("profil/suppression/confirmee/", views.delete_done, name="delete_done"),
]
