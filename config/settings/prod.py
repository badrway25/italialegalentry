"""
Production settings — hardened. All secrets come from the environment: the process environment that
the systemd unit provides (docs/deployment/PRODUCTION_DEPLOYMENT_RUNBOOK.md), never a file in the
checkout.

Two guard rails, and the second exists because the first was not enough.

**A ``.env`` file is ignored here.** It used to be read whatever the settings module, which meant a
development file copied onto a server did not weaken the configuration so much as *satisfy* it:
``DJANGO_SECRET_KEY`` and ``DJANGO_ALLOWED_HOSTS`` are mandatory in production precisely so that a
deployment must provide them, and a stray file provided them — with development values. The check
below then had nothing to object to. Set ``ILE_READ_ENV_FILE=1`` to opt back in deliberately.

**Production refuses to start without its mandatory variables** — the secret key, the hosts, the
trusted origins, the database, the IP-hash salt, and an explicit 0 or 1 for each of
``SECURE_HSTS_INCLUDE_SUBDOMAINS`` and ``SECURE_HSTS_PRELOAD`` — whatever else the environment says,
**and on a weakened configuration**: HTTPS redirect off, HSTS below a year, a short or unvaried
secret key, second-factor enrolment optional, a wildcard host list, a published or short IP-hash salt, an
e-mail backend that writes mail to the logs instead of delivering it, or a value still holding a
``<...>`` placeholder of docs/deployment/production.env.example.
``ILE_ALLOW_INSECURE_PROD=1`` is the single, explicit escape hatch — for a staging-like stack with no
TLS in front of it (docker-compose.staging.yml), never for the public host. The first deployment
does NOT need it: with the second factor enforced, an account that has no device yet is sent to the
enrolment page, which stays reachable (accounts.middleware).

One placement is refused even through the hatch, because it is an exposure rather than a weakening:
``PRIVATE_MEDIA_ROOT`` inside a directory that something serves to the public.
"""

from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F401,F403
from .base import BASE_DIR, EMAIL_HOST, LOGGING, PRIVATE_MEDIA_ROOT, STATIC_ROOT, STATICFILES_DIRS, env

DEBUG = False
SECRET_KEY = env("DJANGO_SECRET_KEY")  # no default: deployment must provide it
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS = env.list("DJANGO_CSRF_TRUSTED_ORIGINS")

# The database, with no development fallback. base.py defaults DATABASE_URL to the local development
# server (127.0.0.1:5439, the development password) so that a fresh checkout runs; a production
# process that inherited that default would not fail at boot but at its first request, against a port
# nothing listens on. Mandatory here, like the three above. Health checks, because connections are
# reused for DB_CONN_MAX_AGE seconds by a fixed number of workers: after a PostgreSQL restart each
# worker would otherwise answer one request with a 500 on its dead connection.
DATABASES = {"default": env.db_url("DATABASE_URL")}
DATABASES["default"]["CONN_MAX_AGE"] = env.int("DB_CONN_MAX_AGE", default=60)
DATABASES["default"]["CONN_HEALTH_CHECKS"] = True
DATABASES["default"]["ATOMIC_REQUESTS"] = True

SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=True)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=31536000)
# includeSubDomains and preload are statements about EVERY host of the domain, not about this
# application: once a browser has read them, each subdomain must answer over valid HTTPS for a year,
# and a preloaded domain takes months to leave the list. So neither has a default: the environment
# says 0 or 1, decided for the domain being deployed. With a default of "on", an environment file
# that lost its two lines (or one built from .env.example) sent includeSubDomains from the apex of a
# domain whose subdomains nobody had inventoried, without a word. Turned off, `check --deploy`
# reports security.W005 / security.W021 — on the record, not silently.
SECURE_HSTS_INCLUDE_SUBDOMAINS = env.bool("SECURE_HSTS_INCLUDE_SUBDOMAINS")
SECURE_HSTS_PRELOAD = env.bool("SECURE_HSTS_PRELOAD")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
LANGUAGE_COOKIE_SECURE = True
USE_X_FORWARDED_HOST = True

# The reverse proxy, as allauth sees it. The settings above already trust exactly one proxy in front
# of the application (X-Forwarded-Proto, X-Forwarded-Host). allauth keys its rate limits — failed
# sign-ins, sign-ups, password resets — on the client address, and by default trusts no proxy: behind
# nginx it then sees every visitor as 127.0.0.1 (one shared bucket: five failed sign-ins by anyone
# lock everyone out) or, on a unix socket, sees no address at all and refuses the request with a 403.
# One trusted proxy makes it read the address nginx appends to X-Forwarded-For (the right-most entry),
# which a client cannot forge. The runbook's nginx sets that header to $remote_addr.
ALLAUTH_TRUSTED_PROXY_COUNT = env.int("ALLAUTH_TRUSTED_PROXY_COUNT", default=1)

# Public media — the media library's photographs (seed_all copies them here), the Forum's public
# photos, videos and PDFs, the optional logo — uploaded through the back-office and served by the
# reverse proxy under MEDIA_URL. Configurable so that it lives outside the checkout, which a release
# replaces; the default is base.py's.
MEDIA_ROOT = Path(env("MEDIA_ROOT", default="") or BASE_DIR / "media")  # empty = the default, never "."

# Second-factor enrolment is mandatory in production unless explicitly disabled (audited decision). The flag makes
# enrolment mandatory; a device an account holds is asked for in every session whatever it says (F-5).
BACKOFFICE_MFA_ENFORCED = env.bool("BACKOFFICE_MFA_ENFORCED", default=True)

EMAIL_BACKEND = env("EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend")

# The salt of the one-way hash every stored IP address goes through (core.privacy). base.py's default
# is published in this repository: with it, the hashes in the audit trail, the consents and the forms
# could be reversed by hashing the whole IPv4 space. No default here.
IP_HASH_SALT = env("IP_HASH_SALT")

LOGGING["handlers"]["console"]["formatter"] = "structured"

#: Backends that do not deliver: they write the message — account-verification and password-reset
#: links included — to the console (journald), to files, or to memory, or drop it.
NON_DELIVERING_EMAIL_BACKENDS = frozenset(
    {
        "django.core.mail.backends.console.EmailBackend",
        "django.core.mail.backends.filebased.EmailBackend",
        "django.core.mail.backends.locmem.EmailBackend",
        "django.core.mail.backends.dummy.EmailBackend",
    }
)
#: Salt values that are published: base.py's default and .env.example's placeholder.
PUBLISHED_SALTS = frozenset({"dev-salt-change-me", "change-me-dev-only-not-for-production"})

ALLOW_INSECURE_PROD = env.bool("ILE_ALLOW_INSECURE_PROD", default=False)
if not ALLOW_INSECURE_PROD:
    problems = []
    if not SECURE_SSL_REDIRECT:
        problems.append("SECURE_SSL_REDIRECT is false")
    if SECURE_HSTS_SECONDS < 31536000:
        problems.append(f"SECURE_HSTS_SECONDS is {SECURE_HSTS_SECONDS} (expected at least 31536000)")
    if len(set(SECRET_KEY)) < 5 or len(SECRET_KEY) < 50:
        problems.append("DJANGO_SECRET_KEY is too short or not random enough (50+ varied characters)")
    if not BACKOFFICE_MFA_ENFORCED:
        # The guard rail above exists because a development ``.env`` copied onto a server silently
        # weakens TLS. The same file silently makes the second factor OPTIONAL, and that opens the
        # case files of real people to a password alone for every account that has not enrolled —
        # which is worse. It was only a ``check --deploy`` warning, and a warning is a thing you read
        # if you happen to run the command. (A device an account holds is asked for in every session
        # whatever the flag says: the flag decides whether enrolment is mandatory.)
        #
        # There is no first-deployment window that needs it off: with enforcement on, an account
        # without a device is redirected to the enrolment page, which stays reachable — no guarded
        # perimeter covers it, and the Present rule on allauth's second-factor pages concerns only an
        # account that already holds a device (accounts.middleware). The escape hatch remains,
        # explicit and on the record.
        problems.append(
            "BACKOFFICE_MFA_ENFORCED is false: accounts that can read another person's case file "
            "and have not enrolled a second factor would sign in with a password alone"
        )
    if "*" in ALLOWED_HOSTS:
        problems.append(
            "DJANGO_ALLOWED_HOSTS contains '*': any Host header would be accepted, and the links the "
            "platform e-mails (verification, password reset) could name a host chosen by the requester"
        )
    if IP_HASH_SALT in PUBLISHED_SALTS or len(IP_HASH_SALT) < 32:
        problems.append(
            "IP_HASH_SALT is a published placeholder or shorter than 32 characters: the hashed IP "
            "addresses of the audit trail could be reversed"
        )
    if EMAIL_BACKEND in NON_DELIVERING_EMAIL_BACKENDS:
        problems.append(
            f"EMAIL_BACKEND is {EMAIL_BACKEND}: e-mail — account-verification and password-reset links "
            "included — would be written to the logs or dropped instead of delivered"
        )
    # docs/deployment/production.env.example marks every value to replace as <...>. A value that still
    # holds one is a template that was installed and never filled in — and a placeholder salt or host
    # list would otherwise pass every test above.
    unfilled = [
        name
        for name, value in (
            ("DJANGO_SECRET_KEY", SECRET_KEY),
            ("IP_HASH_SALT", IP_HASH_SALT),
            ("DATABASE_URL", env.str("DATABASE_URL")),
            ("DJANGO_ALLOWED_HOSTS", ",".join(ALLOWED_HOSTS)),
            ("DJANGO_CSRF_TRUSTED_ORIGINS", ",".join(CSRF_TRUSTED_ORIGINS)),
            ("EMAIL_HOST", EMAIL_HOST),
        )
        if "<" in value or ">" in value
    ]
    if unfilled:
        problems.append("still holding a placeholder of the template (<...>): " + ", ".join(unfilled))
    if problems:
        raise ImproperlyConfigured(
            "Insecure production configuration: "
            + "; ".join(problems)
            + ". Fix the environment, or set ILE_ALLOW_INSECURE_PROD=1 to accept it deliberately."
        )


def _served_directories():
    """Every directory whose content is published: the reverse proxy serves MEDIA_ROOT under MEDIA_URL,
    WhiteNoise serves STATIC_ROOT, and collectstatic copies STATICFILES_DIRS into it."""
    yield "MEDIA_ROOT", MEDIA_ROOT
    yield "STATIC_ROOT", STATIC_ROOT
    for entry in STATICFILES_DIRS:
        yield "STATICFILES_DIRS", entry[1] if isinstance(entry, tuple | list) else entry


# Never, under any configuration — not even with the escape hatch. documents.storage.private_root()
# refuses MEDIA_ROOT at the first upload; this refuses every served directory at boot. WhiteNoise in
# particular indexes everything under STATIC_ROOT when the process starts, so a private file placed
# there would be public after the next restart.
_private = Path(PRIVATE_MEDIA_ROOT).resolve()
for _label, _served in _served_directories():
    _served = Path(_served).resolve()
    if _private == _served or _served in _private.parents or _private in _served.parents:
        raise ImproperlyConfigured(
            f"PRIVATE_MEDIA_ROOT ({_private}) overlaps {_label} ({_served}), which is served to the "
            "public. Private documents must live in a directory of their own, outside every served one."
        )

# Never, under any configuration. A production database holds real people; a seed that can
# invent one is a seed that can be mistaken for the truth.
ILE_SEED_DEMONSTRATION_DATA = False
