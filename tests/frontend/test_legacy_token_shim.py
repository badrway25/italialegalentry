"""
The legacy token shim only shrinks.

`static/css/_legacy-tokens.css` exists so that art direction A could replace the token set without
one unreviewable commit and without a site that is broken for the length of the refactor. It maps
the old names onto the new system while 169 templates and ~6 000 lines of CSS are migrated file by
file.

A shim that is allowed to grow is not a shim: it is a second design system, and the project ends up
maintaining both. These tests hold the countdown. When a migration removes names, LOWER the numbers
here in the same commit — that is the point of them, and the failure message says so.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SHIM = ROOT / "static" / "css" / "_legacy-tokens.css"
CSS_DIR = ROOT / "static" / "css"
TEMPLATES = ROOT / "templates"
APPS = ROOT / "apps"

#: The census taken when the shim was created, 21 September 2026. These are CEILINGS.
#: Lower them whenever a migration removes entries; never raise them.
MAX_SHIM_TOKENS = 153
MAX_SHIM_CLASSES = 14
MAX_LEGACY_USAGES = 1636

#: Files whose job is to talk about the shim rather than to use it.
EXEMPT = {
    "static/css/_legacy-tokens.css",
    "tests/frontend/test_legacy_token_shim.py",
}


def shim_text() -> str:
    return SHIM.read_text(encoding="utf-8")


def shim_tokens() -> set[str]:
    """Names DECLARED by the shim (left-hand side of a custom property)."""
    return set(re.findall(r"^\s*(--[a-z0-9-]+):", shim_text(), flags=re.M))


def shim_classes() -> set[str]:
    return set(re.findall(r"^\.([a-z][a-z0-9-]*)\s*[,{]", shim_text(), flags=re.M))


def css_and_template_files() -> list[Path]:
    files = list(CSS_DIR.glob("*.css"))
    files += list(APPS.rglob("static/**/*.css"))
    files += list(TEMPLATES.rglob("*.html"))
    files += list(APPS.rglob("templates/**/*.html"))
    return [p for p in files if p.relative_to(ROOT).as_posix() not in EXEMPT]


def test_the_shim_exists_and_says_what_it_is() -> None:
    text = shim_text()
    assert "DEMOLITION SCAFFOLD" in text
    assert "ONLY SHRINKS" in text.upper()


def test_the_shim_does_not_grow() -> None:
    count = len(shim_tokens())
    assert count <= MAX_SHIM_TOKENS, (
        f"the shim declares {count} tokens, ceiling is {MAX_SHIM_TOKENS}. "
        "A new name in the shim means new code was written against the retired system: "
        "use a token from tokens.css instead."
    )


def test_the_shim_class_list_does_not_grow() -> None:
    count = len(shim_classes())
    assert count <= MAX_SHIM_CLASSES, f"{count} legacy classes, ceiling {MAX_SHIM_CLASSES}"


def test_every_shim_token_resolves_to_a_real_token() -> None:
    """A shim entry pointing at a name that does not exist is worse than no entry: it is silent."""
    live = set(re.findall(r"^\s*(--[a-z0-9-]+):", (CSS_DIR / "tokens.css").read_text(encoding="utf-8"), flags=re.M))
    declared = shim_tokens()
    dangling = []
    for name, value in re.findall(r"^\s*(--[a-z0-9-]+):\s*([^;]+);", shim_text(), flags=re.M):
        for target in re.findall(r"var\((--[a-z0-9-]+)", value):
            if target not in live and target not in declared:
                dangling.append(f"{name} -> {target}")
    assert dangling == [], dangling


def test_no_new_file_is_written_against_the_retired_system() -> None:
    """
    Files created AFTER the rebase must use the new tokens only. The two written so far are named
    here; if this list needs a third entry, ask why the new code is speaking the old language.
    """
    new_files = ["static/css/register.css"]
    legacy = shim_tokens()
    offenders = []
    for relative in new_files:
        text = (ROOT / relative).read_text(encoding="utf-8")
        for name in re.findall(r"var\((--[a-z0-9-]+)", text):
            if name in legacy:
                offenders.append(f"{relative}: {name}")
    assert offenders == [], offenders


def test_the_legacy_usage_count_does_not_grow() -> None:
    total = 0
    per_file: dict[str, int] = {}
    for path in css_and_template_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        hits = sum(text.count(f"var({name}") for name in shim_tokens())
        if hits:
            per_file[path.relative_to(ROOT).as_posix()] = hits
            total += hits
    assert total <= MAX_LEGACY_USAGES, (
        f"{total} references to retired tokens, ceiling {MAX_LEGACY_USAGES}.\n"
        + "\n".join(f"  {n:5} {f}" for f, n in sorted(per_file.items(), key=lambda r: -r[1])[:10])
    )


@pytest.mark.xfail(reason="the shim is a debt: this test passes only when the migration is finished", strict=False)
def test_the_shim_is_gone() -> None:
    """
    The finish line, stated as a test so it stays visible.

    When this passes, delete the shim, remove its @import from main.css, and delete this file.
    """
    assert not SHIM.exists()
