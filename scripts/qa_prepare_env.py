"""
Prepare an isolated QA database that represents the POST-2-October state with forms enabled.

    DATABASE_URL=postgres://ile:ile-dev-password@127.0.0.1:5439/ile_qa \
        .venv/Scripts/python scripts/qa_prepare_env.py

The password of the three QA accounts comes from the environment variable ``ILE_QA_PASSWORD`` — the
local, untracked ``.env`` (see ``.env.example``) or the shell — never from this file. The script
refuses to run without it, and never prints it.

It never touches the development database and never stores fake legal text: public forms are opened
through the audited ``forms_override_without_legal`` flag, which exists precisely for this purpose.
"""

from __future__ import annotations

import datetime as dt
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "apps"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

import django  # noqa: E402

django.setup()

from django.contrib.auth import get_user_model  # noqa: E402
from django.core.management import call_command  # noqa: E402

from accounts import roles  # noqa: E402
from core import flags  # noqa: E402
from core.models import FeatureFlag  # noqa: E402

#: Where the QA accounts' password is read, at run time: the local ``.env`` (read by the settings) or
#: the shell. Local QA only; the value is never printed and never written in this repository.
QA_ACCOUNTS_ENV_VARIABLE = "ILE_QA_PASSWORD"


def qa_password() -> str | None:
    """The QA accounts' password from the environment, or None when it is unset or empty."""
    return os.environ.get(QA_ACCOUNTS_ENV_VARIABLE) or None


def main() -> int:
    if "ile_qa" not in os.environ.get("DATABASE_URL", ""):
        print("Refusing to run: DATABASE_URL must point at the ile_qa database.")
        return 2
    password = qa_password()
    if password is None:
        print(
            f"Refusing to run: {QA_ACCOUNTS_ENV_VARIABLE} is not set. Put it in the local, untracked .env "
            "(see .env.example) or export it for this command; its value is never printed."
        )
        return 2
    call_command("migrate", verbosity=0)
    call_command("seed_all", verbosity=0)
    phase3 = dt.datetime(2026, 10, 2, 0, 0, tzinfo=dt.UTC)
    for key, kwargs in {
        "phase3_public": {"enabled": True, "enabled_from": phase3},
        "forms_override_without_legal": {"enabled": True},
        "newsletter": {"enabled": True},
        "forum_permanent_mode": {"enabled": True, "enabled_from": dt.datetime(2026, 10, 2, 16, 0, tzinfo=dt.UTC)},
    }.items():
        FeatureFlag.objects.update_or_create(key=key, defaults={"note": "QA environment", **kwargs})
    flags.invalidate()
    User = get_user_model()
    if not User.objects.filter(email="qa-admin@example.test").exists():
        User.objects.create_superuser(email="qa-admin@example.test", password=password)
    for email, role in (("qa-person@example.test", roles.PERSON), ("qa-company@example.test", roles.COMPANY)):
        user, created = User.objects.get_or_create(email=email, defaults={"full_name": email.split("@")[0]})
        if created:
            user.set_password(password)
            user.save()
        roles.assign_role(user, role)
        from allauth.account.models import EmailAddress

        EmailAddress.objects.update_or_create(user=user, email=email, defaults={"verified": True, "primary": True})
    print("QA environment ready: flags set, users qa-admin/qa-person/qa-company created.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
