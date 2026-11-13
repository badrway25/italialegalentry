from django.urls import path

from ecosystem import views
from ecosystem.models import SpaceKey
from ecosystem.services import SPACES

app_name = "ecosystem"

urlpatterns = [
    path(SPACES[SpaceKey.COMPANIES].path, views.companies, name="companies"),
    path(SPACES[SpaceKey.INSTITUTIONS].path, views.institutions, name="institutions"),
    path(SPACES[SpaceKey.UNIVERSITIES].path, views.universities, name="universities"),
    path(SPACES[SpaceKey.PILOT].path, views.pilot, name="pilot"),
]
