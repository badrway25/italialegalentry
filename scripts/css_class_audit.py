"""
Which classes do the templates name that no stylesheet defines?

    .venv/Scripts/python scripts/css_class_audit.py            # report; exit 1 above the ceiling
    .venv/Scripts/python scripts/css_class_audit.py --list     # every orphan, with its files
    .venv/Scripts/python scripts/css_class_audit.py --json

A class in a template with no rule behind it is not always a defect — a hook read by JavaScript or a
test is legitimate, and the prefixes in ``BEHAVIOUR_PREFIXES`` are treated as such. Everything else
is a declared structure that the stylesheet does not express, and two of them turned out to matter:

* ``.gloss`` was used on fourteen pages and matched nothing, so every aside rendered at running-prose
  size in the ink colour and read as a second paragraph of the argument.
* ``.faq-item__links`` was used on the FAQ and matched nothing, so its links sat 22 px apart —
  measured — and failed WCAG 2.2 §2.5.8, which needs 24 px of separation for a target under 24 px.

Neither was visible as a broken page. Both were visible as a number.

The ceiling exists so the figure can only go down. Raising it is a decision someone has to make on
purpose, in a commit message.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

#: Prefixes that mark a class as a hook rather than a style: JavaScript, a utility, a state set by
#: script, or a selector a test uses to find something.
BEHAVIOUR_PREFIXES = ("js-", "u-", "no-", "is-", "has-")

#: The number of orphans on 21 September 2026, after `.gloss`, `.faq-item__links` and
#: `.related-links__list` were given rules. THIS ONLY GOES DOWN.
CEILING = 382


def defined_classes() -> set[str]:
    css = []
    for pattern in ("static/css/*.css", "apps/*/static/*/*.css"):
        for path in ROOT.glob(pattern):
            css.append(path.read_text(encoding="utf-8", errors="replace"))
    return set(re.findall(r"\.([a-zA-Z][\w-]*)", "\n".join(css)))


def used_classes() -> dict[str, set[str]]:
    used: dict[str, set[str]] = {}
    for pattern in ("templates/**/*.html", "apps/*/templates/**/*.html"):
        for path in ROOT.glob(pattern):
            text = path.read_text(encoding="utf-8", errors="replace")
            # Skip attributes holding a template expression: the class is computed, not literal.
            for attr in re.findall(r'class="([^"{}]*)"', text):
                for token in attr.split():
                    if token:
                        used.setdefault(token, set()).add(str(path.relative_to(ROOT)))
    return used


def orphans() -> dict[str, set[str]]:
    defined = defined_classes()
    return {
        name: files
        for name, files in used_classes().items()
        if name not in defined and not name.startswith(BEHAVIOUR_PREFIXES)
    }


def main(argv: list[str]) -> int:
    found = orphans()
    if "--json" in argv:
        print(json.dumps({k: sorted(v) for k, v in sorted(found.items())}, indent=2))
        return 0 if len(found) <= CEILING else 1

    print(f"{len(found)} class(es) used in a template with no CSS rule (ceiling {CEILING})")
    rows = sorted(found.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    for name, files in rows if "--list" in argv else rows[:20]:
        print(f"  {name:36s} {len(files):2d} file(s)  e.g. {sorted(files)[0]}")
    if "--list" not in argv and len(rows) > 20:
        print(f"  … and {len(rows) - 20} more (--list for all)")

    if len(found) > CEILING:
        print(f"\nFAIL: {len(found) - CEILING} more than the ceiling. Add the rule, or the class is wrong.")
        return 1
    if len(found) < CEILING:
        print(f"\n{CEILING - len(found)} fewer than the ceiling — lower CEILING to {len(found)} in this commit.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
