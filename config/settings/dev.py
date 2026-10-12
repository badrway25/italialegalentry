from .base import *  # noqa: F401,F403
from .base import DATABASES, LOGGING, STORAGES, env

DEBUG = env.bool("DJANGO_DEBUG", default=True)
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0", "testserver"]  # noqa: S104
STORAGES["staticfiles"] = {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"}
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
LANGUAGE_COOKIE_SECURE = False
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
LOGGING["root"]["level"] = "INFO"

# The development server is runserver: one thread per client socket, no worker limit, and a request
# opens its connection before the view runs (ATOMIC_REQUESTS). base.py's 60 s lifetime kept every one
# of those connections open after its thread had ended, until the shared PostgreSQL ran out of slots
# (preview outage of 2 October 2026). `.env.example` has prescribed 0 since 21 September; this makes
# it the default so a fresh checkout behaves the same. Production keeps 60 s under gunicorn's fixed
# number of workers, where one reused connection per worker is the point.
DATABASES["default"]["CONN_MAX_AGE"] = env.int("DB_CONN_MAX_AGE", default=0)

NOTIFICATIONS_SEND_IMMEDIATELY = True
