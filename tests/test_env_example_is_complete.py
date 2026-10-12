"""
`.env.example` must list every environment variable the settings read.

`DJANGO_CSRF_TRUSTED_ORIGINS` is required in production and had no default, so `prod.py` refused to
start without it — and it was missing from `.env.example`. Nothing failed in development, because
`base.py` defaults it to an empty list; the first `manage.py check --deploy` against the production
settings died on it. Five more variables were missing for the same reason: they have defaults, so
nobody noticed they were undocumented.

An example file that omits a required variable is not incomplete documentation. It is a file that
tells the next person they have everything when they do not.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

#: `env("NAME")`, `env.bool("NAME", …)`, `env.list("NAME")`, `env.int("NAME", …)` …
READ = re.compile(r"""env(?:\.\w+)?\(\s*["']([A-Z_][A-Z0-9_]*)["']""")
DECLARED = re.compile(r"^([A-Z_][A-Z0-9_]*)=", re.MULTILINE)

#: The settings modules a deployment actually loads. `dev.py` and `test.py` are for this machine.
SETTINGS = ("config/settings/base.py", "config/settings/prod.py")

#: A variable declared in the example that no settings module reads, on purpose, with the files that
#: do read it (V5.4 W1-0: the QA password moved out of the repository into the local `.env`).
QA_PASSWORD_READERS = {"ILE_QA_PASSWORD": ("scripts/qa_prepare_env.py", "apps/helpdesk/seeds.py")}


def _read_names() -> set[str]:
    text = "".join((ROOT / name).read_text(encoding="utf-8") for name in SETTINGS)
    return set(READ.findall(text))


def _declared_names() -> set[str]:
    return set(DECLARED.findall((ROOT / ".env.example").read_text(encoding="utf-8")))


def test_every_variable_the_settings_read_is_in_the_example():
    missing = sorted(_read_names() - _declared_names())
    assert not missing, (
        "read by config/settings but absent from .env.example: "
        + ", ".join(missing)
        + ". Add them, with a line saying what happens when they are wrong."
    )


def test_the_example_declares_nothing_the_settings_ignore():
    """
    The other direction, which rots more quietly.

    A variable in the example that nothing reads is a setting somebody will carefully configure and
    then wonder why it has no effect. `DJANGO_SETTINGS_MODULE` is the exception: it is read by
    Django itself before any settings module exists. `ILE_QA_PASSWORD` is the other, and the next
    test holds it to its readers: the local QA accounts' password, read by two scripts and never by a
    settings module.
    """
    known_outside_settings = {"DJANGO_SETTINGS_MODULE", *QA_PASSWORD_READERS}
    stale = sorted(_declared_names() - _read_names() - known_outside_settings)
    assert not stale, "declared in .env.example but read by nothing in config/settings: " + ", ".join(stale)


def test_the_variables_with_no_default_are_called_out():
    """
    Three variables make production refuse to start. The example must say so, not just list them.

    A reader scanning `.env.example` for what they *must* set has no other way to tell these three
    apart from the twenty-six that have a sensible default.
    """
    text = (ROOT / ".env.example").read_text(encoding="utf-8")
    prod = (ROOT / "config" / "settings" / "prod.py").read_text(encoding="utf-8")

    # No default in prod.py means `env("NAME")` / `env.list("NAME")` with nothing after the name.
    required = set(re.findall(r"""env(?:\.\w+)?\(\s*["']([A-Z_][A-Z0-9_]*)["']\s*\)""", prod))
    assert required >= {"DJANGO_SECRET_KEY", "DJANGO_ALLOWED_HOSTS", "DJANGO_CSRF_TRUSTED_ORIGINS"}

    for name in sorted(required):
        block = text.split(f"{name}=")[0].rsplit("\n\n", 1)[-1]
        assert "OBBLIGATORIA" in block.upper() or "obbligator" in block.lower(), (
            f"{name} has no default and stops production from starting, but .env.example does not say so above it."
        )


def test_the_qa_password_is_read_by_its_scripts_and_never_by_a_settings_module():
    """
    The exception above, held to what it claims. `ILE_QA_PASSWORD` is read where the example says —
    scripts/qa_prepare_env.py and the help desk's demonstration seed — and by no settings module: a
    password that became a setting would sit beside the others on an error page. The example carries
    the name with an empty value, never a value.
    """
    example = (ROOT / ".env.example").read_text(encoding="utf-8")
    for name, readers in QA_PASSWORD_READERS.items():
        assert re.search(rf"^{name}=$", example, flags=re.MULTILINE), f"{name} must be declared empty"
        for reader in readers:
            assert f'"{name}"' in (ROOT / reader).read_text(encoding="utf-8"), f"{reader} no longer reads {name}"
        for settings_module in sorted((ROOT / "config" / "settings").glob("*.py")):
            assert name not in settings_module.read_text(encoding="utf-8"), f"{settings_module.name} reads {name}"
