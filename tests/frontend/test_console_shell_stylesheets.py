"""
Every page drawn in the console shell keeps the shell's stylesheets.

`templates/portal/base_portal.html` puts the console's two sheets (`portal.css`, `console.css`) in
its `extra_head` block. A template below it that overrides `extra_head` REPLACES that block unless it
starts with `{{ block.super }}`. The help desk re-added `portal.css` by hand instead; when the shell
gained `console.css` the help desk lost it and rendered unstyled — rail links as plain text — and no
test noticed, because nothing compared a module's head with the shell's (found 26/09/2026).
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SHELL = "portal/base_portal.html"


def _templates() -> dict[str, str]:
    found = {}
    for root in [ROOT / "templates", *(ROOT / "apps").glob("*/templates")]:
        for path in root.rglob("*.html"):
            found[path.relative_to(root).as_posix()] = path.read_text(encoding="utf-8")
    return found


def _parent(text: str) -> str | None:
    match = re.search(r'{%\s*extends\s+"([^"]+)"', text)
    return match.group(1) if match else None


def _in_the_shell(name: str, templates: dict[str, str]) -> bool:
    seen = set()
    while name and name not in seen:
        if name == SHELL:
            return True
        seen.add(name)
        name = _parent(templates.get(name, ""))
    return False


def test_the_shell_declares_its_stylesheets_in_extra_head():
    shell = _templates()[SHELL]
    block = re.search(r"{%\s*block extra_head\s*%}(.*?){%\s*endblock", shell, flags=re.S)
    assert block, "the console shell no longer declares extra_head: update this test"
    assert "portal/console.css" in block.group(1) and "portal/portal.css" in block.group(1)


def test_no_template_in_the_shell_drops_the_shells_stylesheets():
    templates = _templates()
    offenders = []
    for name, text in templates.items():
        if name == SHELL or not _in_the_shell(name, templates):
            continue
        block = re.search(r"{%\s*block extra_head\s*%}(.*?){%\s*endblock", text, flags=re.S)
        if block and "block.super" not in block.group(1):
            offenders.append(name)
    assert not offenders, f"these templates replace the console shell's stylesheets: {offenders}"
