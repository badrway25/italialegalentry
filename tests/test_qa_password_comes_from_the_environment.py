"""
The local QA password lives in the environment, never in the repository (V5.4 W1-0, the hygiene task).

``scripts/qa_prepare_env.py`` and the help desk's demonstration seed carried the same password as a
string literal. It now comes from ``ILE_QA_PASSWORD`` — the local, untracked ``.env`` or the shell —
and these tests hold what makes that true: the script refuses to run without it, before it touches
any database, and nothing it prints can carry it; the seed never needs it (without it, the accounts
get an unusable password); and neither file writes a password literal again. The value itself is
named nowhere, not even here: a guard that carries the secret to find the secret is not a guard.
"""

from __future__ import annotations

import ast
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "qa_prepare_env.py"
SEED = ROOT / "apps" / "helpdesk" / "seeds.py"
VARIABLE = "ILE_QA_PASSWORD"

#: A name that holds, takes or prints a password.
PASSWORD_LIKE = re.compile(r"pass(word)?|pwd|secret", re.IGNORECASE)


def _run_the_script(**overrides: str) -> subprocess.CompletedProcess:
    """
    The script in a fresh interpreter, on the development settings, with the ``.env`` ignored (so this
    machine's file cannot supply the variable) and a database URL that names ``ile_qa`` — the script's
    first guard — on a port where nothing listens: a run that got past the refusal and reached the
    database would fail loudly instead of touching one.
    """
    env = {k: v for k, v in os.environ.items() if k not in {VARIABLE, "TEST_DATABASE_URL", "DJANGO_SETTINGS_MODULE"}}
    env.update(
        DJANGO_SETTINGS_MODULE="config.settings.dev",
        ILE_READ_ENV_FILE="0",
        DJANGO_DEBUG="1",
        DATABASE_URL="postgres://ile:unused@127.0.0.1:1/ile_qa_unreachable",
    )
    env.update(overrides)
    return subprocess.run(  # noqa: S603 — this interpreter, a file of this repository
        [sys.executable, str(SCRIPT)], cwd=ROOT, env=env, capture_output=True, text=True, timeout=180, check=False
    )


@pytest.mark.parametrize("value", [None, ""], ids=["unset", "empty"])
def test_the_qa_script_refuses_to_run_without_the_variable(value):
    result = _run_the_script(**({} if value is None else {VARIABLE: value}))
    assert result.returncode == 2, (result.stdout[-1000:], result.stderr[-2000:])
    assert f"Refusing to run: {VARIABLE} is not set." in result.stdout
    assert ".env.example" in result.stdout
    assert "Traceback" not in result.stderr, "the refusal must come before any database access"


def _calls(tree: ast.AST):
    return [node for node in ast.walk(tree) if isinstance(node, ast.Call)]


def _names_in(node: ast.AST) -> set[str]:
    found = set()
    for child in ast.walk(node):
        if isinstance(child, ast.Name):
            found.add(child.id)
        elif isinstance(child, ast.Call) and isinstance(child.func, ast.Name):
            found.add(child.func.id)
    return found


def test_nothing_the_qa_script_prints_can_carry_the_password():
    """The password is read into ``password`` by ``qa_password()``; no print, write or log call sees either."""
    tree = ast.parse(SCRIPT.read_text(encoding="utf-8"))
    outputs = 0
    for call in _calls(tree):
        func = call.func
        name = func.id if isinstance(func, ast.Name) else func.attr if isinstance(func, ast.Attribute) else ""
        if name in {"print", "write", "debug", "info", "warning", "error", "exception", "critical", "log"}:
            outputs += 1
            for argument in [*call.args, *(keyword.value for keyword in call.keywords)]:
                assert not {"password", "qa_password"} & _names_in(argument), ast.unparse(call)
    assert outputs >= 3, "the script's messages are where this test looks"


@pytest.mark.parametrize("path", [SCRIPT, SEED], ids=["qa_prepare_env", "helpdesk_seed"])
def test_no_password_literal_is_written_in_the_file(path):
    """
    No string literal is bound to a password-like name, handed to ``set_password`` or passed as a
    password-like keyword. The only string a password-like name may hold is the NAME of an environment
    variable (upper case, underscores), which is what both files now keep.
    """
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign)) and isinstance(node.value, ast.Constant):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            names = [target.id for target in targets if isinstance(target, ast.Name)]
            if any(PASSWORD_LIKE.search(name) for name in names) and isinstance(node.value.value, str):
                assert re.fullmatch(r"[A-Z][A-Z0-9_]*", node.value.value), f"{path.name}: {names}"
    for call in _calls(tree):
        if isinstance(call.func, ast.Attribute) and call.func.attr == "set_password":
            assert not any(isinstance(argument, ast.Constant) for argument in call.args), path.name
        for keyword in call.keywords:
            if keyword.arg and PASSWORD_LIKE.search(keyword.arg):
                assert not isinstance(keyword.value, ast.Constant), f"{path.name}: {keyword.arg}="
    assert f'"{VARIABLE}"' in path.read_text(encoding="utf-8"), f"{path.name} no longer reads {VARIABLE}"


@pytest.mark.django_db
def test_a_demonstration_account_without_the_variable_gets_an_unusable_password(monkeypatch):
    from accounts import roles
    from helpdesk.seeds import _demo_account

    monkeypatch.delenv(VARIABLE, raising=False)
    user = _demo_account("demo-sans-variable@example.test", roles.PROFESSIONAL, "Compte de démonstration")
    user.refresh_from_db()
    assert not user.has_usable_password()


@pytest.mark.django_db
def test_a_demonstration_account_with_the_variable_takes_its_value(monkeypatch):
    from accounts import roles
    from helpdesk.seeds import _demo_account

    monkeypatch.setenv(VARIABLE, "only-a-value-for-this-test")
    user = _demo_account("demo-avec-variable@example.test", roles.PROFESSIONAL, "Compte de démonstration")
    user.refresh_from_db()
    assert user.check_password("only-a-value-for-this-test")
