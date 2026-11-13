"""
Verify that every locked text is a verbatim substring of the source document extraction, after
whitespace normalisation. This proves nothing was rewritten between the client's document and the
page that renders it.

    .venv/Scripts/python scripts/verify_locked_against_source.py
    ILE_SOURCE_DIR=D:/altrove .venv/Scripts/python scripts/verify_locked_against_source.py

The extractions live OUTSIDE the repository, next to the PDFs they come from. They used to sit in
`docs/source/` and were removed from the working tree and from every commit on 21 September 2026:
they are the client's documents, and a repository that may be published is not where they belong.
See `docs/security/HISTORY_REWRITE_2026-09-21.md`.

That is why this is a script and not a test. The control it performs is real, but it cannot run on
a machine that does not hold the source documents, and a test suite that fails for that reason
would teach everybody to ignore it. The integrity of the locked texts is covered in the suite by
`apps/cms/locked_content.sha256.json`, which needs no source document.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "apps"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

from cms import locked_content  # noqa: E402

#: Where the extractions are kept. Overridable, because the next person's disk is not this one.
SOURCE_DIR = Path(os.environ.get("ILE_SOURCE_DIR", r"C:\tmp"))

SOURCES = [
    SOURCE_DIR / "ILE_Document_Implementation_FR.txt",
    SOURCE_DIR / "ILE_Annexe_1_Textes_Juridiques_FR.txt",
]


def normalise(text: str) -> str:
    text = re.sub(r"===== PAGE \d+ / \d+ =====", " ", text)
    text = text.replace("­", "")  # soft hyphens
    # join words hyphenated at line end ONLY when the hyphen is a real part of the word: keep "-"
    text = re.sub(r"([-–])\n", r"\1", text)  # hyphen or en-dash at end of a PDF line
    text = re.sub(r"\s+", " ", text)
    return text


def flatten(value) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        out: list[str] = []
        for v in value:
            out.extend(flatten(v))
        return out
    if isinstance(value, dict):
        out = []
        for k, v in value.items():
            if k == "key":  # structural identifier, not source text
                continue
            out.extend(flatten(v))
        return out
    return []


def main() -> int:
    absent = [p for p in SOURCES if not p.exists()]
    if absent:
        print("The source extractions are not on this machine, so this control cannot run:")
        for p in absent:
            print(f"  missing: {p}")
        print(
            "\nThey are deliberately outside the repository (see "
            "docs/security/HISTORY_REWRITE_2026-09-21.md). Put them next to the PDFs and point\n"
            "ILE_SOURCE_DIR at that directory. This is 'not verified', not 'verified clean'."
        )
        return 2

    corpus = normalise("\n".join(p.read_text(encoding="utf-8") for p in SOURCES))
    missing: list[tuple[str, str]] = []
    checked = 0
    for key, value in locked_content.LOCKED_TEXTS["fr"].items():
        for fragment in flatten(value):
            frag = re.sub(r"\s+", " ", fragment).strip()
            if not frag or len(frag) < 3:
                continue
            checked += 1
            if frag not in corpus:
                missing.append((key, frag[:90]))
    print(f"checked {checked} fragments from {len(locked_content.LOCKED_TEXTS['fr'])} keys")
    for key, frag in missing:
        print(f"  NOT FOUND VERBATIM: {key}: {frag}…")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
