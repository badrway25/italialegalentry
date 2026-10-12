from django.urls import path

from legal import views

app_name = "legal"

urlpatterns = [
    path("privacy-policy/", views.privacy, name="privacy"),
    path("cookie-policy/", views.cookies, name="cookies"),
    path("note-legali/", views.notices, name="notices"),
    path("condizioni-di-utilizzo/", views.terms, name="terms"),
    path("avvertenze/", views.disclaimer, name="disclaimer"),
]
