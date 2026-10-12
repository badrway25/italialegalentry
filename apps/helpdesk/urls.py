"""
URLs of the digital help desk.

Mounted under the reserved area (``/espace-reserve/guichet/``) because the help desk is a platform
module, not a public page: nothing here is reachable without an account, and nothing here is
indexed. Identifiers in the path are UUIDs, never primary keys — a sequential identifier in a URL
both leaks volume and invites the hand-typed probe the permission tests exist to defeat.
"""

from django.urls import path

from helpdesk import views

app_name = "helpdesk"

urlpatterns = [
    path("", views.requests_list, name="requests"),
    path("nouvelle-demande/", views.open_request, name="open"),
    path("confiees/", views.queue, name="queue"),
    path("designation/", views.dispatch, name="dispatch"),
    path("<uuid:uuid>/", views.detail, name="detail"),
    path("<uuid:uuid>/message/", views.add_message, name="message"),
    path("<uuid:uuid>/verification-professionnelle/", views.escalate, name="escalate"),
    path("<uuid:uuid>/prise-en-charge/", views.take, name="take"),
    path("<uuid:uuid>/reponse/", views.respond, name="respond"),
    path("<uuid:uuid>/note/", views.add_note, name="note"),
    path("<uuid:uuid>/cloture/", views.close_request, name="close"),
]
