"""
The development settings must not keep database connections alive between requests.

``runserver`` serves every client socket on its own thread, without a limit, and ``ATOMIC_REQUESTS``
opens the connection before the view runs. With ``base.py``'s 60 s lifetime, a connection outlived
the thread that opened it — nothing closes a dead thread's connection — and on 2 October 2026 five
headless browsers reviewing the design preview asked the shared PostgreSQL for more connections than
it has (``max_connections`` 300): every development server on it answered 500 for twenty minutes.
``.env.example`` had prescribed ``DB_CONN_MAX_AGE=0`` since 21 September; the ``.env`` files in use
predated it, so the prescription protected nobody. The default now lives in the code.

Production is not changed: gunicorn runs a fixed number of workers, each reusing one connection.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

#: Loads a settings module in a fresh interpreter with the `.env` file ignored, so the value read is
#: the code's default (or the explicit environment), never whatever this machine's `.env` says.
PROBE = """
import environ
environ.Env.read_env = staticmethod(lambda *a, **k: None)
from django.conf import settings
print(settings.DATABASES["default"]["CONN_MAX_AGE"])
"""


def _lifetime(settings_module: str, **extra_env: str) -> int:
    env = {k: v for k, v in os.environ.items() if k != "DB_CONN_MAX_AGE"}
    env.update(DJANGO_SETTINGS_MODULE=settings_module, **extra_env)
    result = subprocess.run(  # noqa: S603 — this interpreter, a literal program
        [sys.executable, "-c", PROBE], cwd=ROOT, env=env, capture_output=True, text=True, timeout=120, check=False
    )
    assert result.returncode == 0, result.stderr[-2000:]
    return int(result.stdout.strip().splitlines()[-1])


@pytest.mark.parametrize(
    ("settings_module", "expected"),
    [("config.settings.dev", 0), ("config.settings.base", 60)],
    ids=["dev-does-not-reuse", "base-keeps-the-production-default"],
)
def test_default_connection_lifetime(settings_module: str, expected: int) -> None:
    assert _lifetime(settings_module) == expected


def test_the_environment_still_decides() -> None:
    """The variable keeps its meaning: an operator who wants reuse on a dev server can ask for it."""
    assert _lifetime("config.settings.dev", DB_CONN_MAX_AGE="45") == 45
