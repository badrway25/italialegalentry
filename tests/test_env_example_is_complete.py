"""
`.env.example` must list every environment variable the application reads, and the production template must hold
every variable a production process reads.

`DJANGO_CSRF_TRUSTED_ORIGINS` is required in production and had no default, so `prod.py` refused to start without
it — and it was missing from `.env.example`. Nothing failed in development, because `base.py` defaults it to an
empty list; the first `manage.py check --deploy` against the production settings died on it. Five more variables
were missing for the same reason: they have defaults, so nobody noticed they were undocumented.

An example file that omits a required variable is not incomplete documentation. It is a file that tells the next
person they have everything when they do not.

Since 12 October 2026 the rule covers three readers and two files:

* every variable read by `config/settings/base.py` and `prod.py` is declared or documented in `.env.example`, and
  every one is in `docs/deployment/production.env.example` — the template of the server's environment file;
* every variable read by `dev.py` and `test.py`, by the application's code and by the repository's scripts and tests
  is documented in `.env.example`, the development-only ones in its NOT FOR PRODUCTION section and never declared —
  and so is every variable the compose files interpolate (`docker-compose*.yml`);
* the other direction: nothing is declared or documented that nothing reads.

And one trap closed: with django-environ an EMPTY value is not "unset" — a boolean becomes false, a number fails to
parse, a path becomes the current directory. `PRIVATE_MEDIA_ROOT=` (empty) used to put identity documents in the
root of the checkout. A variable is declared empty only when empty is its default.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / ".env.example"
PRODUCTION_TEMPLATE = ROOT / "docs" / "deployment" / "production.env.example"

#: `env("NAME")`, `env.bool("NAME", …)`, `env.list("NAME")`, `env.int("NAME", …)`, `env.db_url("NAME")` …
READ = re.compile(r"""\benv(?:\.\w+)?\(\s*["']([A-Z_][A-Z0-9_]*)["']""")
#: `os.environ.get("NAME")`, `os.environ["NAME"]`, `os.getenv("NAME")`, `os.environ.setdefault("NAME", …)`.
OS_READ = re.compile(r"""os\.(?:environ(?:\.get|\.setdefault)?\s*[\[(]|getenv\()\s*["']([A-Z_][A-Z0-9_]*)["']""")
#: A module constant that names a variable: `QA_ACCOUNTS_ENV_VARIABLE = "ILE_QA_PASSWORD"`, `TABLE_ENV = "…"`,
#: `api_key_env="PEXELS_API_KEY"`.
CONSTANT = re.compile(r"""\b(?:[A-Z_]*(?:ENV|VARIABLE)|api_key_env)\s*=\s*["']([A-Z_][A-Z0-9_]*)["']""")
#: `os.environ.get(<expression>)` — a name decided at run time.
DYNAMIC = re.compile(r"""os\.environ\.get\(\s*(?!["'])([\w.\[\]"']+)""")
#: `${NAME}`, `${NAME:-default}`, `${NAME:?message}` — what `docker compose` fills from the shell or the local `.env`.
COMPOSE_READ = re.compile(r"\$\{([A-Z_][A-Z0-9_]*)(?::?[-?+][^}]*)?\}")

DECLARED = re.compile(r"^([A-Z_][A-Z0-9_]*)=(.*)$", re.MULTILINE)
COMMENTED = re.compile(r"^#\s*([A-Z_][A-Z0-9_]*)=", re.MULTILINE)

#: The settings modules a deployment actually loads. `dev.py` and `test.py` are for this machine.
SETTINGS = ("config/settings/base.py", "config/settings/prod.py")
DEVELOPMENT_SETTINGS = ("config/settings/dev.py", "config/settings/test.py")

#: Read before any settings module exists — by Django, manage.py, wsgi.py, asgi.py, the scripts and the tests.
OUTSIDE_SETTINGS = {"DJANGO_SETTINGS_MODULE"}
#: Set by the browser tests themselves (`os.environ.setdefault`), or the interpreter's or the operating system's own
#: (Windows' LOCALAPPDATA, where Playwright keeps its browsers): never project configuration.
SELF_SET = {"DJANGO_ALLOW_ASYNC_UNSAFE", "PYTHONPATH", "LOCALAPPDATA"}

#: A variable declared in the example that no settings module reads, on purpose, with the files that do read it
#: (V5.4 W1-0: the QA password moved out of the repository into the local `.env`).
QA_PASSWORD_READERS = {"ILE_QA_PASSWORD": ("scripts/qa_prepare_env.py", "apps/helpdesk/seeds.py")}

#: The marker of the NOT FOR PRODUCTION section of `.env.example`.
DEVELOPMENT_SECTION = "NOT FOR PRODUCTION"


def _text(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def _names(pattern: re.Pattern, text: str) -> set[str]:
    return set(pattern.findall(text))


def _settings_reads(modules=SETTINGS) -> set[str]:
    return _names(READ, "".join(_text(name) for name in modules))


def _python_files(*folders: str) -> list[Path]:
    return [p for folder in folders for p in (ROOT / folder).rglob("*.py") if "migrations" not in p.parts]


def _code_reads(files: list[Path]) -> set[str]:
    names: set[str] = set()
    for path in files:
        text = path.read_text(encoding="utf-8")
        names |= _names(READ, text) | _names(OS_READ, text)
        if "environ" in text:
            names |= _names(CONSTANT, text)
    return names - SELF_SET


def _application_files() -> list[Path]:
    return [p for p in _python_files("apps", "config") if "tests" not in p.parts] + [ROOT / "manage.py"]


def _tool_files() -> list[Path]:
    """Scripts and tests — this module excepted: its docstrings and patterns name `NAME` on purpose."""
    files = _python_files("scripts", "tests") + [p for p in _python_files("apps") if "tests" in p.parts]
    return [p for p in files if p.resolve() != Path(__file__).resolve()] + [ROOT / "conftest.py"]


def _compose_reads() -> set[str]:
    """The variables the repository's compose files interpolate (docker-compose*.yml)."""
    names: set[str] = set()
    for path in sorted(ROOT.glob("docker-compose*.yml")):
        names |= _names(COMPOSE_READ, path.read_text(encoding="utf-8"))
    return names


def _example() -> str:
    return EXAMPLE.read_text(encoding="utf-8")


def _declared(text: str) -> dict[str, str]:
    return dict(DECLARED.findall(text))


def _documented(text: str) -> set[str]:
    """Declared or commented-out (`# NAME=…`)."""
    return set(_declared(text)) | _names(COMMENTED, text)


def _required_in_production() -> set[str]:
    """No default in prod.py: `env("NAME")` / `env.list("NAME")` / `env.db_url("NAME")` with nothing after the name."""
    return set(re.findall(r"""\benv(?:\.\w+)?\(\s*["']([A-Z_][A-Z0-9_]*)["']\s*\)""", _text("config/settings/prod.py")))


def _defaults_to_empty() -> set[str]:
    """Variables the settings read with `default=""` — the only ones an empty declaration leaves at their default."""
    text = "".join(_text(name) for name in SETTINGS)
    return set(re.findall(r"""\benv(?:\.str)?\(\s*["']([A-Z_][A-Z0-9_]*)["']\s*,\s*default=""\s*\)""", text))


# -------------------------------------------------------------------------------------------------------------------
# .env.example
# -------------------------------------------------------------------------------------------------------------------
def test_every_variable_the_settings_read_is_in_the_example():
    missing = sorted(_settings_reads() - _documented(_example()))
    assert not missing, (
        "read by config/settings but absent from .env.example: "
        + ", ".join(missing)
        + ". Add them, with a line saying what happens when they are wrong."
    )


def test_every_variable_the_development_settings_read_is_documented_and_never_declared():
    """dev.py and test.py variables live in the NOT FOR PRODUCTION section, commented out: declaring one empty breaks
    the settings that read it (`env.int("ILE_DESIGN_PREVIEW_DB_CEILING")` fails on an empty value)."""
    text = _example()
    development_only = _settings_reads(DEVELOPMENT_SETTINGS) - _settings_reads()
    section = text.split(DEVELOPMENT_SECTION, 1)[-1]
    missing = sorted(development_only - _names(COMMENTED, section))
    assert not missing, "read by dev.py/test.py, absent from the NOT FOR PRODUCTION section: " + ", ".join(missing)
    declared = sorted(development_only & set(_declared(text)))
    assert not declared, "development-only variables declared (they would be set by copying the file): " + ", ".join(
        declared
    )


def test_every_variable_the_application_and_its_tools_read_is_documented():
    names = _code_reads(_application_files()) | _code_reads(_tool_files())
    missing = sorted(names - _documented(_example()))
    assert not missing, "read by the code but absent from .env.example: " + ", ".join(missing)


def test_every_variable_the_compose_files_interpolate_is_documented():
    """
    docker-compose.staging.yml refuses to start without POSTGRES_PASSWORD (`${…:?…}`) and says it comes from the local
    `.env` — and `.env.example` did not name it, because this test read Python files only (DevOps verification,
    finding 12). The compose files are readers too.
    """
    names = _compose_reads()
    assert "POSTGRES_PASSWORD" in names, "the staging stack no longer reads POSTGRES_PASSWORD: update this test"
    missing = sorted(names - _documented(_example()))
    assert not missing, "interpolated by docker-compose*.yml but absent from .env.example: " + ", ".join(missing)


def test_a_variable_named_at_run_time_is_explained():
    """`os.environ.get(system.inbound_secret_env)`: the NAME is data in the back-office. The example must say so."""
    text = _example()
    for path in _application_files():
        for expression in DYNAMIC.findall(path.read_text(encoding="utf-8")):
            attribute = expression.rsplit(".", 1)[-1]
            if attribute.isupper():  # a module constant, resolved by the test above
                continue
            assert attribute in text, f"{path.relative_to(ROOT)} reads a variable named by {expression}: explain it"


def test_the_example_declares_nothing_the_code_ignores():
    """
    The other direction, which rots more quietly.

    A variable in the example that nothing reads is a setting somebody will carefully configure and then wonder why
    it has no effect. `DJANGO_SETTINGS_MODULE` is read by Django itself before any settings module exists.
    `ILE_QA_PASSWORD` is held to its readers by the last test.
    """
    read = (
        _settings_reads()
        | _settings_reads(DEVELOPMENT_SETTINGS)
        | _code_reads(_application_files())
        | _code_reads(_tool_files())
        | _compose_reads()
        | OUTSIDE_SETTINGS
        | set(QA_PASSWORD_READERS)
    )
    stale = sorted(_documented(_example()) - read)
    assert not stale, "named in .env.example but read by nothing: " + ", ".join(stale)


def test_the_variables_with_no_default_are_called_out():
    """
    The variables that make production refuse to start. The example must say so, not just list them — and declare
    them with a value, so that a copied file runs.

    A reader scanning `.env.example` for what they *must* set has no other way to tell these apart from the ones
    that have a sensible default.
    """
    text = _example()
    required = _required_in_production()
    assert required >= {
        "DJANGO_SECRET_KEY",
        "DJANGO_ALLOWED_HOSTS",
        "DJANGO_CSRF_TRUSTED_ORIGINS",
        "DATABASE_URL",
        "IP_HASH_SALT",
    }
    declared = _declared(text)
    for name in sorted(required):
        assert declared.get(name), f"{name} is required in production: declare it, with a development value"
        comment = text.split(f"\n{name}=")[0].rsplit("\n", 1)[-1]
        assert "REQUIRED IN PRODUCTION" in comment, (
            f"{name} has no default and stops production from starting, but .env.example does not say so above it."
        )


def test_nothing_is_declared_empty_unless_empty_is_its_default():
    empty = {name for name, value in _declared(_example()).items() if not value.strip()}
    trapped = sorted(empty - _defaults_to_empty() - set(QA_PASSWORD_READERS))
    assert not trapped, (
        "declared empty although their default is not empty (django-environ reads '' as a value: false, a parse "
        "error, or the current directory): " + ", ".join(trapped)
    )


def test_every_variable_has_a_comment_above_it():
    lines = _example().splitlines()
    for index, line in enumerate(lines):
        if DECLARED.match(line) or re.match(r"^#\s*[A-Z_][A-Z0-9_]*=", line):
            above = lines[index - 1] if index else ""
            in_list = re.match(r"^#\s*[A-Z_][A-Z0-9_]*=", above) or above.startswith("# Read by")
            assert above.startswith("#") or in_list, f"no comment above line {index + 1}: {line}"


# -------------------------------------------------------------------------------------------------------------------
# docs/deployment/production.env.example — the server's environment file
# -------------------------------------------------------------------------------------------------------------------
def _template() -> str:
    return PRODUCTION_TEMPLATE.read_text(encoding="utf-8")


def test_the_production_template_holds_every_variable_the_production_settings_read():
    missing = sorted(_settings_reads() - _documented(_template()) - OUTSIDE_SETTINGS)
    assert not missing, "read by config/settings/{base,prod}.py, absent from the production template: " + ", ".join(
        missing
    )


def test_the_production_template_declares_every_required_variable_with_a_placeholder_or_value():
    declared = _declared(_template())
    assert declared.get("DJANGO_SETTINGS_MODULE") == "config.settings.prod"
    for name in sorted(_required_in_production()):
        assert declared.get(name), f"{name} is required in production and not declared in the template"


def test_the_production_template_never_sets_a_development_switch():
    declared = _declared(_template())
    development_only = _settings_reads(DEVELOPMENT_SETTINGS) - _settings_reads()
    forbidden = development_only | {"DJANGO_DEBUG", "ILE_READ_ENV_FILE", "ILE_ALLOW_INSECURE_PROD", "ILE_QA_PASSWORD"}
    assert not sorted(forbidden & set(declared)), sorted(forbidden & set(declared))
    assert declared.get("BACKOFFICE_MFA_ENFORCED") == "1"
    assert declared.get("EMAIL_BACKEND") == "django.core.mail.backends.smtp.EmailBackend"
    assert declared.get("NOTIFICATIONS_SEND_IMMEDIATELY") == "0"
    assert declared.get("REDIS_URL") == "", "REDIS_URL must stay empty: the Redis client library is not installed"


def test_the_templates_carry_no_secret_and_no_server_address():
    """
    Placeholders only. A value that looks generated (a long unbroken run of URL-safe characters) is a secret that
    was pasted in; an IPv4 address other than loopback names a real machine, which a public repository must not.
    """
    for path in (EXAMPLE, PRODUCTION_TEMPLATE):
        text = path.read_text(encoding="utf-8")
        for name, value in _declared(text).items():
            for run in re.findall(r"[A-Za-z0-9_\-]{24,}", value):
                generated = re.search(r"[a-z]", run) and re.search(r"[A-Z]", run) and re.search(r"[0-9]", run)
                assert not generated, f"{path.name}: {name} looks like a real secret"
        for address in re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", text):
            assert address.startswith("127.") or address == "0.0.0.0", f"{path.name} names the address {address}"


# -------------------------------------------------------------------------------------------------------------------
# The QA password (V5.4 W1-0)
# -------------------------------------------------------------------------------------------------------------------
def test_the_qa_password_is_read_by_its_scripts_and_never_by_a_settings_module():
    """
    The exception above, held to what it claims. `ILE_QA_PASSWORD` is read where the example says —
    scripts/qa_prepare_env.py and the help desk's demonstration seed — and by no settings module: a
    password that became a setting would sit beside the others on an error page. The example carries
    the name with an empty value, never a value.
    """
    example = _example()
    for name, readers in QA_PASSWORD_READERS.items():
        assert re.search(rf"^{name}=$", example, flags=re.MULTILINE), f"{name} must be declared empty"
        for reader in readers:
            assert f'"{name}"' in (ROOT / reader).read_text(encoding="utf-8"), f"{reader} no longer reads {name}"
        for settings_module in sorted((ROOT / "config" / "settings").glob("*.py")):
            assert name not in settings_module.read_text(encoding="utf-8"), f"{settings_module.name} reads {name}"
