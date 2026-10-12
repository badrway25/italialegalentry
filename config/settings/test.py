from .base import *  # noqa: F401,F403
from .base import BASE_DIR, DATABASES, LOGGING, STORAGES, env

DEBUG = False
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "testserver"]
SECRET_KEY = "test-only-secret-key-not-for-production"  # noqa: S105
DATABASES["default"] = env.db_url("TEST_DATABASE_URL", default="postgres://ile:ile-dev-password@127.0.0.1:5439/ile")
DATABASES["default"]["ATOMIC_REQUESTS"] = True
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
STORAGES["staticfiles"] = {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"}
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache", "LOCATION": "ile-test"}}
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
LANGUAGE_COOKIE_SECURE = False
WHITENOISE_AUTOREFRESH = True
MEDIA_ROOT = BASE_DIR / "tmp" / "test_media"
PRIVATE_MEDIA_ROOT = BASE_DIR / "tmp" / "test_private_media"
LOGGING["root"]["level"] = "WARNING"

NOTIFICATIONS_SEND_IMMEDIATELY = True

# Never manufacture people in a test run: the switch is derived from DEBUG at the moment
# ``base`` is imported, and setting DEBUG=False above does not reach back to change it.
ILE_SEED_DEMONSTRATION_DATA = False
