"""
Base settings for Italy Legal Entry™ (AGAMI — Dialogo Giuridico Interculturale APS).

Every environment imports from here. Secrets and environment-specific values come from
environment variables (see .env.example). Nothing secret is stored in this repository.
"""

from __future__ import annotations

import datetime as dt
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent
APPS_DIR = BASE_DIR / "apps"
if str(APPS_DIR) not in sys.path:
    sys.path.insert(0, str(APPS_DIR))

env = environ.Env()
env_file = BASE_DIR / ".env"

# A `.env` sitting next to the code is a development convenience. On a server it is a hazard: the
# file wins over nothing, but it SUPPLIES values, so a development file copied onto a host makes
# variables that production treats as mandatory quietly resolve to development values — a weak
# secret key, a permissive host list, the second factor switched off. `prod.py` then has nothing to
# refuse, because from its point of view the operator provided everything.
#
# Under the production settings the file is therefore ignored, unless the operator asks for it. The
# real process environment is the only source, which is what every container and systemd unit
# provides anyway.
_IS_PROD = "prod" in (env("DJANGO_SETTINGS_MODULE", default="") or "")
_READ_ENV_FILE = env.bool("ILE_READ_ENV_FILE", default=not _IS_PROD)
ENV_FILE_WAS_READ = bool(env_file.exists() and _READ_ENV_FILE)
ENV_FILE_IGNORED = bool(env_file.exists() and not _READ_ENV_FILE)
if ENV_FILE_WAS_READ:
    environ.Env.read_env(str(env_file))

SECRET_KEY = env("DJANGO_SECRET_KEY", default="unsafe-development-key-change-me")
DEBUG = env.bool("DJANGO_DEBUG", default=False)
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])
CSRF_TRUSTED_ORIGINS = env.list("DJANGO_CSRF_TRUSTED_ORIGINS", default=[])

# ---------------------------------------------------------------------------
# Applications
# ---------------------------------------------------------------------------
DJANGO_APPS = [
    "unfold",  # back-office UX layer; must precede django.contrib.admin (ADR-005)
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.humanize",
]
THIRD_PARTY_APPS = [
    "allauth",
    "allauth.account",
    "allauth.mfa",
]
LOCAL_APPS = [
    "core",
    "cms",
    "accounts",
    "consents",
    "audit",
    "notifications",
    "legal",
    "pages",
    "ecosystem",
    "enquiries",
    "pathways",
    "orientation",
    "cases",
    "rules",
    "companies",
    "selection",
    "academy",
    "helpdesk",
    "forum",
    "community",
    "news",
    "faq",
    "glossary",
    "living",
    "partners",
    "documents",
    "portal",
    "integrations",
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # HTML compression, below WhiteNoise so static files (served precompressed) never reach it, and
    # above everything that writes the body or its headers (core.middleware.TextGZipMiddleware).
    "core.middleware.TextGZipMiddleware",
    "core.middleware.RequestIDMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    # Keeps the language cookie aligned with the /<lang>/ prefix being read (I18N-05).
    "core.middleware.LanguageCookieMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    # Back-office MFA policy: must stay after AuthenticationMiddleware/AccountMiddleware and after
    # MessageMiddleware so the redirect can carry a message (accounts.checks.check_backoffice_mfa).
    "accounts.middleware.BackofficeMFAMiddleware",
    # Old WordPress URLs: ?lang= redirects, 410 for WP endpoints, cms.Redirect rows on 404.
    "cms.middleware.LegacyURLMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "csp.middleware.CSPMiddleware",
    # Relaxed policy for the staff-only back-office theme; the public policy stays strict.
    "core.middleware.BackofficeCSPMiddleware",
    "core.middleware.ExtraSecurityHeadersMiddleware",
]

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
SITE_ID = 1

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.template.context_processors.debug",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
                "core.context_processors.site",
            ],
            "builtins": ["core.templatetags.ile_core"],
        },
    }
]

# ---------------------------------------------------------------------------
# Database — PostgreSQL only (ADR-001). No SQLite path is provided on purpose.
# ---------------------------------------------------------------------------
DATABASES = {"default": env.db_url("DATABASE_URL", default="postgres://ile:ile-dev-password@127.0.0.1:5439/ile")}
DATABASES["default"]["CONN_MAX_AGE"] = env.int("DB_CONN_MAX_AGE", default=60)
DATABASES["default"]["ATOMIC_REQUESTS"] = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------------------
# Cache
# ---------------------------------------------------------------------------
REDIS_URL = env("REDIS_URL", default="")
if REDIS_URL:
    CACHES = {"default": {"BACKEND": "django.core.cache.backends.redis.RedisCache", "LOCATION": REDIS_URL}}
else:
    CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache", "LOCATION": "ile"}}

# ---------------------------------------------------------------------------
# Authentication / accounts (custom user from day one; RBAC in accounts.roles)
# ---------------------------------------------------------------------------
AUTH_USER_MODEL = "accounts.User"
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
LOGIN_URL = "account_login"
LOGIN_REDIRECT_URL = "portal:dashboard"
LOGOUT_REDIRECT_URL = "pages:home"

# The custom user has NO username field: allauth must be told, otherwise every real login crashes
# while rendering the "signed in as …" message (found by browser QA — tests used force_login).
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USER_DISPLAY = "accounts.utils.user_display"
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_SUBJECT_PREFIX = "[Italy Legal Entry] "
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_SESSION_REMEMBER = False
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = False
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_PASSWORD_MIN_LENGTH = 12
ACCOUNT_RATE_LIMITS = {
    "login_failed": "5/5m/ip,5/5m/key",
    "signup": "10/h/ip",
    "reset_password": "5/h/ip,3/h/key",
    "confirm_email": "3/10m/key",
    "change_password": "5/m/user",
    "manage_email": "10/m/user",
}
ACCOUNT_ADAPTER = "accounts.adapters.AccountAdapter"
# "login", "reset_password" and "reset_password_from_key" are allauth's own forms with their presentation only
# (design V5 «Il varco», W2-B): what the widgets say to the browser, and no placeholder. Authentication,
# validation and the rate limits are allauth's, untouched.
ACCOUNT_FORMS = {
    "signup": "accounts.forms.SignupForm",
    "login": "accounts.forms.LoginForm",
    "reset_password": "accounts.forms.ResetPasswordForm",
    "reset_password_from_key": "accounts.forms.ResetPasswordKeyForm",
}
# The second factor's code on «Il varco»: allauth's form, its presentation only — no placeholder, the digits'
# keyboard (W2-B; a second setting, written for the steward's agreement at the merge).
MFA_FORMS = {"authenticate": "accounts.forms.AuthenticateForm"}
MFA_SUPPORTED_TYPES = ["totp", "recovery_codes"]
MFA_TOTP_ISSUER = "Italy Legal Entry"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 12},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.Argon2PasswordHasher",
]

# ---------------------------------------------------------------------------
# Internationalisation — four languages, real RTL for Arabic (docs/I18N_RTL.md)
# ---------------------------------------------------------------------------
LANGUAGE_CODE = "fr"  # authoritative source language of all supplied texts (ADR-004)
LANGUAGES = [
    ("it", "Italiano"),
    ("fr", "Français"),
    ("en", "English"),
    ("ar", "العربية"),
]
RTL_LANGUAGES = {"ar"}
CONTENT_FALLBACK_LANGUAGE = "fr"
LOCALE_PATHS = [BASE_DIR / "locale"]
TIME_ZONE = "Europe/Rome"
USE_I18N = True
USE_TZ = True
LANGUAGE_COOKIE_NAME = "ile_language"
LANGUAGE_COOKIE_SAMESITE = "Lax"
LANGUAGE_COOKIE_SECURE = not DEBUG

# ---------------------------------------------------------------------------
# Static & media
# ---------------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
# Private documents are NEVER under MEDIA_ROOT; they are served only through authorised views.
PRIVATE_MEDIA_ROOT = Path(env("PRIVATE_MEDIA_ROOT", default=str(BASE_DIR / "private_media")))
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}
WHITENOISE_MAX_AGE = 31536000
DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024
DATA_UPLOAD_MAX_NUMBER_FIELDS = 200

# ---------------------------------------------------------------------------
# E-mail — development never sends real mail (console backend). One destination for all forms.
# ---------------------------------------------------------------------------
EMAIL_BACKEND = env("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = env("EMAIL_HOST", default="")
EMAIL_PORT = env.int("EMAIL_PORT", default=587)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
EMAIL_TIMEOUT = 15
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="Italy Legal Entry <noreply@example.invalid>")
SERVER_EMAIL = DEFAULT_FROM_EMAIL

# ---------------------------------------------------------------------------
# Project constants (single source for gates, dates, addresses)
# ---------------------------------------------------------------------------
ROME = ZoneInfo("Europe/Rome")
ILE = {
    "PROJECT_NAME": "Italy Legal Entry™",
    "PROMOTER": "AGAMI — Dialogo Giuridico Interculturale APS",
    "PUBLIC_CONTACT_EMAIL": env("PUBLIC_CONTACT_EMAIL", default="contact@agamieuromed.org"),
    "FORMS_DESTINATION_EMAIL": env("FORMS_DESTINATION_EMAIL", default="contact@agamieuromed.org"),
    "FORBIDDEN_EMAIL_DOMAIN": "legalitalentry.it",
    "REFERENCE_DATE_OVERRIDE": env("ILE_REFERENCE_DATE", default=""),
    "PHASE1_DEADLINE": dt.date(2026, 9, 17),
    "PHASE2_DEADLINE": dt.date(2026, 9, 25),
    "PHASE3_DATE": dt.datetime(2026, 10, 2, 0, 0, tzinfo=ROME),
    "FORUM_ROVIGO_DATE": dt.date(2026, 10, 2),
    "FORUM_ROVIGO_END": dt.datetime(2026, 10, 2, 18, 0, tzinfo=ROME),
    "FORUM_MOROCCO_DATES": (dt.date(2026, 10, 29), dt.date(2026, 10, 30)),
    "VERSION_LABEL": env("ILE_VERSION_LABEL", default="v2.0.0 — Fase 1"),
    "CONTENT_FALLBACK_LANGUAGE": CONTENT_FALLBACK_LANGUAGE,
    "RETENTION_MONTHS_FORMS": 24,  # from the legal texts (Annexe 1 §7) — never invent other durations
}

# Feature flags: defaults used when no DB row exists (see core.flags). Dates are Europe/Rome.
#: Whether a seed may create SYNTHETIC records that resemble real ones — a demonstration account, a
#: case file, a help-desk request, a training plan. Configuration and published editorial content are
#: always seeded; this governs only invented people. Its own setting rather than ``DEBUG`` so an
#: environment can keep DEBUG on for developer tooling and still refuse to manufacture people; it
#: falls back to DEBUG so an existing configuration behaves as before. See core.seeds.
ILE_SEED_DEMONSTRATION_DATA = env.bool("ILE_SEED_DEMONSTRATION_DATA", default=DEBUG)

FEATURE_FLAG_DEFAULTS = {
    "phase3_public": {
        "enabled": False,
        "enabled_from": ILE["PHASE3_DATE"],
        "note": "Phase 3 content (after 2 Oct 2026) — requires explicit authorisation AND the date",
    },
    "forum_banner": {
        "enabled": True,
        "enabled_until": ILE["PHASE3_DATE"],
        "note": "Homepage Forum banner shown until 2 Oct 2026",
    },
    "forum_permanent_mode": {
        "enabled": False,
        "enabled_from": ILE["FORUM_ROVIGO_END"],
        "note": "Forum page switches to Forum Permanent Vénétie–Maroc after the event",
    },
    "virtual_forum": {
        "enabled": False,
        "note": "Virtual Forum — launch after the Morocco forum (29–30 Oct 2026)",
    },
    "forms_override_without_legal": {
        "enabled": False,
        "note": "DANGER: allow public forms while legal pages are blocked. Every change is audited.",
    },
    "newsletter": {"enabled": False, "note": "Newsletter opt-in block (separate revocable consent)"},
    "reserved_area_public_link": {"enabled": True, "note": "Show the secondary reserved-area access link"},
    "analytics": {"enabled": False, "note": "Privacy-compliant analytics abstraction — NOT enabled"},
}

# ---------------------------------------------------------------------------
# Security headers (production values are hardened further in prod.py)
# ---------------------------------------------------------------------------
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_AGE = 60 * 60 * 8
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = "Lax"
PERMISSIONS_POLICY = "camera=(), microphone=(), geolocation=(), payment=(), usb=(), interest-cohort=()"

# django-csp 4.x — self-hosted everything; no third-party scripts, fonts or images.
CONTENT_SECURITY_POLICY = {
    "DIRECTIVES": {
        "default-src": ("'self'",),
        "script-src": ("'self'",),
        "style-src": ("'self'",),
        "img-src": ("'self'", "data:"),
        "font-src": ("'self'",),
        "connect-src": ("'self'",),
        "frame-ancestors": ("'none'",),
        "form-action": ("'self'",),
        "base-uri": ("'self'",),
        "object-src": ("'none'",),
        "upgrade-insecure-requests": True,
    }
}

# ---------------------------------------------------------------------------
# Throttling of public forms (core.throttle) — privacy friendly: IP is hashed, never stored raw.
# ---------------------------------------------------------------------------
PUBLIC_FORM_THROTTLE = {"limit": 5, "window_seconds": 600}

# ---------------------------------------------------------------------------
# Pluggable security / integration hooks (see docs/SECURITY.md, docs/CRM_INTEGRATION_CONTRACT.md)
# ---------------------------------------------------------------------------
# TOTP mandatory for every staff account entering /backoffice/ (accounts.middleware).
# Off by default so a fresh local install can reach the back-office; production must enable it.
BACKOFFICE_MFA_ENFORCED = env.bool("BACKOFFICE_MFA_ENFORCED", default=False)
# Dotted path of a callable(path) -> ScanStatus used to scan private uploads. Empty = files stay
# "pending" and are downloadable only by their owner (documents.services.scan_file).
DOCUMENT_SCANNER = env("DOCUMENT_SCANNER", default="")
# Dotted path of the outbound transport for CRM events. The default logs and never leaves the host;
# no external endpoint is contacted until an integration is explicitly configured.
INTEGRATIONS_TRANSPORT = env("INTEGRATIONS_TRANSPORT", default="integrations.transports.LoggingTransport")
IP_HASH_SALT = env("IP_HASH_SALT", default="dev-salt-change-me")

# ---------------------------------------------------------------------------
# Back-office (django-unfold)
# ---------------------------------------------------------------------------
UNFOLD = {
    "SITE_TITLE": "Italy Legal Entry — Back-office",
    "SITE_HEADER": "Italy Legal Entry™",
    "SITE_SUBHEADER": "Back-office editoriale · AGAMI",
    "SITE_URL": "/",
    "SITE_SYMBOL": "account_balance",
    "SHOW_HISTORY": True,
    "SHOW_LANGUAGES": True,
    "BORDER_RADIUS": "4px",
    "COLORS": {
        "primary": {
            "50": "238 243 250",
            "100": "214 226 243",
            "200": "176 199 230",
            "300": "128 161 210",
            "400": "78 116 176",
            "500": "36 78 142",
            "600": "24 60 118",
            "700": "16 46 94",
            "800": "12 34 70",
            "900": "9 24 50",
            "950": "6 16 34",
        },
    },
    "SIDEBAR": {"show_search": True, "show_all_applications": True},
    "ENVIRONMENT": "core.admin_base.environment_badge",
    "DASHBOARD_CALLBACK": "core.admin_base.dashboard_callback",
}

# ---------------------------------------------------------------------------
# Logging — structured, with request id correlation
# ---------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {"request_id": {"()": "core.logging.RequestIDFilter"}},
    "formatters": {
        "structured": {"()": "core.logging.StructuredFormatter"},
        "plain": {"format": "%(levelname)s %(name)s [%(request_id)s] %(message)s"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "filters": ["request_id"],
            "formatter": "plain",
        },
    },
    "root": {"handlers": ["console"], "level": "INFO"},
    "loggers": {
        "django.security": {"level": "WARNING", "propagate": True},
        "ile.security": {"level": "INFO", "propagate": True},
        "ile.audit": {"level": "INFO", "propagate": True},
    },
}

MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

NOTIFICATIONS_SEND_IMMEDIATELY = env.bool("NOTIFICATIONS_SEND_IMMEDIATELY", default=False)
