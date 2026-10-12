from django.urls import path

from consents import views

app_name = "consents"

urlpatterns = [
    path("newsletter/confirmer/<str:token>/", views.newsletter_confirm, name="newsletter_confirm"),
    path("newsletter/desinscription/<str:token>/", views.newsletter_unsubscribe, name="newsletter_unsubscribe"),
]
