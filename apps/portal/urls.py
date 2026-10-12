from django.urls import path

from portal import views

app_name = "portal"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("ma-situation/", views.situation, name="situation"),
    path("mes-demandes/", views.requests_list, name="requests"),
    path("mes-demandes/<slug:kind>/<int:pk>/", views.request_detail, name="request_detail"),
    path("mon-parcours/", views.pathways, name="pathways"),
    path("mes-documents/", views.documents, name="documents"),
    path("mes-echeances/", views.deadlines, name="deadlines"),
    path("communications/", views.messages_list, name="messages"),
    path("communications/<uuid:pk>/", views.message_detail, name="message_detail"),
    path("communications/<uuid:pk>/lu/", views.message_read, name="message_read"),
]
