"""
Production settings — hardened. All secrets come from the environment (docs/DEPLOYMENT.md).

Two guard rails, and the second exists because the first was not enough.

**A ``.env`` file is ignored here.** It used to be read whatever the settings module, which meant a
development file copied onto a server did not weaken the configuration so much as *satisfy* it:
``DJANGO_SECRET_KEY`` and ``DJANGO_ALLOWED_HOSTS`` are mandatory in production precisely so that a
deployment must provide them, and a stray file provided them — with development values. The check
below then had nothing to object to. Set ``ILE_READ_ENV_FILE=1`` to opt back in deliberately.

**Production refuses to start on a weakened configuration**: HTTPS redirect off, HSTS below a year,
a short or unvaried secret key, or the second factor disabled. ``ILE_ALLOW_INSECURE_PROD=1`` is the
single, explicit escape hatch — useful behind a TLS-terminating proxy on a private network, and on
the first deployment before staff have enrolled a TOTP device. Both belong in the runbook.
"""

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F401,F403
from .base import LOGGING, env

DEBUG = False
SECRET_KEY = env("DJANGO_SECRET_KEY")  # no default: deployment must provide it
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS = env.list("DJANGO_CSRF_TRUSTED_ORIGINS")

SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=True)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=31536000)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
LANGUAGE_COOKIE_SECURE = True
USE_X_FORWARDED_HOST = True

# Staff MFA is mandatory in production unless explicitly disabled (audited decision).
BACKOFFICE_MFA_ENFORCED = env.bool("BACKOFFICE_MFA_ENFORCED", default=True)

EMAIL_BACKEND = env("EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend")
LOGGING["handlers"]["console"]["formatter"] = "structured"

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
        # weakens TLS. The same file silently switches the second factor OFF, and that opens the
        # case files of real people to a password alone — which is worse. It was only a
        # ``check --deploy`` warning, and a warning is a thing you read if you happen to run the
        # command.
        #
        # There IS a legitimate window with it off: the first deployment, before staff have
        # enrolled a TOTP device. That window uses the same escape hatch as everything else here —
        # explicit, deliberate, and on the record.
        problems.append(
            "BACKOFFICE_MFA_ENFORCED is false: accounts that can read another person's case file "
            "would sign in with a password alone"
        )
    if problems:
        raise ImproperlyConfigured(
            "Insecure production configuration: "
            + "; ".join(problems)
            + ". Fix the environment, or set ILE_ALLOW_INSECURE_PROD=1 to accept it deliberately."
        )

# Never, under any configuration. A production database holds real people; a seed that can
# invent one is a seed that can be mistaken for the truth.
ILE_SEED_DEMONSTRATION_DATA = False
