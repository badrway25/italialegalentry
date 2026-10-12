from django.urls import path

from integrations import views

app_name = "integrations"

urlpatterns = [
    path("v1/health/", views.health, name="health"),
    path("v1/schema/", views.schema, name="schema"),
    path("v1/events/", views.events_list, name="events_list"),
    path("v1/events/<uuid:uuid>/ack/", views.events_ack, name="events_ack"),
    path("v1/webhooks/<slug:system>/", views.inbound_webhook, name="inbound_webhook"),
]
