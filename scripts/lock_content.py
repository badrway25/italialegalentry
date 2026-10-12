"""
Regenerate the checksum file of the locked-content registry.

Run ONLY when a locked text is deliberately updated from a new official transmission:

    .venv/Scripts/python scripts/lock_content.py

The resulting diff of ``apps/cms/locked_content.sha256.json`` must be reviewed in git.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "apps"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

from cms import locked_content  # noqa: E402

OUT = ROOT / "apps" / "cms" / "locked_content.sha256.json"


def main() -> int:
    payload = {lang: locked_content.checksums(lang) for lang in locked_content.LOCKED_TEXTS}
    OUT.write_text(json.dumps(payload, indent=1, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {OUT} — {sum(len(v) for v in payload.values())} checksums")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
