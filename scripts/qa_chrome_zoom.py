"""
Walk the zoom levels in the VISIBLE Chrome window: 100, 125, 150, 200, 400 per cent.

    python scripts/qa_chrome_zoom.py docs/qa/chrome/zoom.json

Zoom is emulated the way the browser implements it, and it is worth being exact about what that
means. Browser zoom does not enlarge a picture of the page: it enlarges the CSS pixel, so a window
of fixed physical size holds fewer CSS pixels and the CSS viewport shrinks by the zoom factor.
Media queries re-evaluate against that smaller viewport. Reducing the viewport by the factor, which
is what this script does, reproduces that exactly — 400% in a 1280px window IS a 320px viewport,
which is where WCAG 2.2 §1.4.10's reflow floor comes from.

What it is NOT is `document.body.style.zoom`, which scales the body's boxes and leaves the viewport
alone: every media query keeps answering with the desktop width, the page never reflows, and the
check cannot fail. This script replaced one that did that.

The window is 1280x800 — the commonest laptop, and the one the success criterion is written
against. At 400% the viewport is 320x200, and 200px of height is the honest consequence: a page
that needs a tall viewport to be usable is a page that is not usable at 400%.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from qa_chrome import REVIEW_JS, disable_cache  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

CDP = "http://127.0.0.1:9222"
BASE = os.environ.get("ILE_QA_BASE", "http://127.0.0.1:8771")

WINDOW = (1280, 800)
LEVELS = [100, 125, 150, 200, 400]

PAGES = [
    ("home", "/fr/"),
    ("parcours_detail", "/fr/parcours/salaried_work/"),
    ("contact_form", "/fr/contact/formulaire/"),
    ("faq", "/fr/faq/"),
    ("login", "/fr/compte/login/"),
    ("cruscotto", "/fr/espace-reserve/"),
    ("fascicoli", "/fr/espace-reserve/dossiers/"),
    ("documenti", "/fr/espace-reserve/mes-documents/"),
    ("home_ar", "/ar/"),
    ("cruscotto_ar", "/ar/espace-reserve/"),
]


def main(out_path: str) -> int:
    rows = []
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = context.pages[0] if context.pages else context.new_page()
        disable_cache(context, page)

        for label, path in PAGES:
            for level in LEVELS:
                width = round(WINDOW[0] * 100 / level)
                height = round(WINDOW[1] * 100 / level)
                page.set_viewport_size({"width": width, "height": height})
                try:
                    response = page.goto(BASE + path, wait_until="domcontentloaded", timeout=30000)
                    page.evaluate("async () => { await document.fonts.ready; }")
                    page.wait_for_timeout(250)
                    facts = page.evaluate(REVIEW_JS)
                    status = response.status if response else 0
                except Exception as exc:  # noqa: BLE001
                    facts, status = {"error": str(exc)[:160]}, 0

                problems = []
                if facts.get("horizontal_scroll"):
                    problems.append(f"scorrimento orizzontale ({facts.get('document_width')}px)")
                for el in facts.get("overflowing", [])[:3]:
                    problems.append(f"sborda {el['tag']}.{el['cls'][:28]} -> {el['right']}px")
                rows.append({
                    "page": label, "path": path, "zoom": level,
                    "css_viewport": f"{width}x{height}", "status": status, "findings": problems,
                })
                print(f'{"!" if problems else "."} {label:16s} {level:3d}%  {width:4d}x{height:<4d} '
                      f'{status}  {"; ".join(problems)[:80]}')

    target = ROOT / out_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(rows, indent=1, ensure_ascii=False), encoding="utf-8")
    bad = [r for r in rows if r["findings"] or r["status"] not in (200, 404)]
    print(f"\n{len(rows)} combinazioni, {len(bad)} con un rilievo -> {out_path}")
    for r in bad:
        print(f'  {r["page"]:16s} {r["zoom"]:3d}%  {"; ".join(r["findings"])[:100]}')
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else "docs/qa/chrome/zoom.json"))
