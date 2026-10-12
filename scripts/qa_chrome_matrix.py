"""
Walk the viewport matrix in the VISIBLE Chrome window and report what breaks at which width.

    python scripts/qa_chrome_matrix.py public   docs/qa/chrome/matrix_public.json
    python scripts/qa_chrome_matrix.py platform docs/qa/chrome/matrix_platform.json

Twelve widths against every page ARCHETYPE rather than every page. Running twelve viewports over
fifty pages produces six hundred rows and no review; what actually differs between two pathway
detail pages is the prose, and prose does not break a layout. What breaks a layout is a table, a
form, a hero, a card grid, a long unbroken string. One page per archetype, all twelve widths.

The two sensitivity bands are not the same work. Below 768 a layout is being asked to reflow, and
every step matters because the failures cluster at the widths where a breakpoint has just fired or
has not yet. Above 1280 nothing reflows any more and the question is whether the measure grows
uncontrolled — three samples answer that. So the narrow band gets every listed width and the wide
band gets its endpoints; `WIDTHS_FOR` says which archetype gets which, and the JSON records it, so
a reader can see what was not run rather than assume everything was.
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

# A Windows console is cp1252 and this project's output is French, Italian and Arabic. Printing a
# navigation label killed this script after it had already signed the browser in — the work was
# done, the report was not. `errors="replace"` costs a mangled glyph and never a traceback.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

CDP = "http://127.0.0.1:9222"
BASE = os.environ.get("ILE_QA_BASE", "http://127.0.0.1:8770")

#: The twelve widths the directive lists, with the heights that make each of them a real device
#: rather than a number: a 430px viewport 932px tall scrolls differently from one 600px tall, and
#: sticky headers and full-height heroes are judged against the height.
VIEWPORTS = [
    (320, 568),    # iPhone SE, 1st gen — the floor
    (360, 640),    # the commonest Android width in Morocco and Italy alike
    (390, 844),    # iPhone 13/14
    (412, 915),    # Pixel 7
    (430, 932),    # iPhone 15 Pro Max
    (768, 1024),   # iPad portrait — the tablet breakpoint sits here
    (1024, 768),   # iPad landscape — where the desktop navigation takes over
    (1280, 800),   # the commonest laptop
    (1366, 768),   # still the commonest Windows laptop in public administration
    (1440, 900),   # MacBook Air
    (1600, 900),
    (1920, 1080),  # the desk monitor the operators will use
]

NARROW = [v for v in VIEWPORTS if v[0] < 768]
HINGE = [v for v in VIEWPORTS if 768 <= v[0] <= 1280]
WIDE = [v for v in VIEWPORTS if v[0] > 1280]

#: Every listed width for the archetypes whose layout genuinely reflows; endpoints only for the
#: ones whose wide behaviour is a single `max-inline-size` on a text column.
ALL_WIDTHS = VIEWPORTS
REFLOW_BAND = NARROW + HINGE + [WIDE[0], WIDE[-1]]

PUBLIC = [
    # (archetype, label, path, widths) — the archetype is what is being tested, the path is only
    # the specimen that happens to exhibit it.
    ("hero + sezioni", "home", "/fr/", ALL_WIDTHS),
    ("griglia di schede", "parcours", "/fr/parcours/", ALL_WIDTHS),
    ("procedura lunga", "parcours_detail", "/fr/parcours/salaried_work/", ALL_WIDTHS),
    ("prosa editoriale", "le_projet", "/fr/le-projet/", REFLOW_BAND),
    ("modulo", "contact_form", "/fr/contact/formulaire/", ALL_WIDTHS),
    ("modulo lungo", "signup", "/fr/compte/signup/", REFLOW_BAND),
    ("elenco definizioni", "glossaire", "/fr/glossaire/", REFLOW_BAND),
    ("voce singola", "glossaire_voce", "/fr/glossaire/nulla_osta/", REFLOW_BAND),
    ("fisarmonica", "faq", "/fr/faq/", REFLOW_BAND),
    ("pagina di errore", "404", "/fr/questa-pagina-non-esiste/", REFLOW_BAND),
    ("autenticazione", "login", "/fr/compte/login/", REFLOW_BAND),
    ("RTL hero", "home_ar", "/ar/", ALL_WIDTHS),
    ("RTL procedura", "parcours_ar", "/ar/parcours/", REFLOW_BAND),
]

PLATFORM = [
    ("cruscotto", "dashboard", "/fr/espace-reserve/", ALL_WIDTHS),
    ("tabella", "dossiers", "/fr/espace-reserve/dossiers/", ALL_WIDTHS),
    ("tabella di date", "echeances", "/fr/espace-reserve/mes-echeances/", REFLOW_BAND),
    ("elenco documenti", "documents", "/fr/espace-reserve/mes-documents/", REFLOW_BAND),
    ("riepilogo", "situation", "/fr/espace-reserve/ma-situation/", REFLOW_BAND),
    ("messaggi", "communications", "/fr/espace-reserve/communications/", REFLOW_BAND),
    ("RTL tabella", "dossiers_ar", "/ar/espace-reserve/dossiers/", REFLOW_BAND),
]

PLANS = {"public": PUBLIC, "platform": PLATFORM}

#: `document.fonts.ready` before measuring anything. A heading in the fallback face is a different
#: width from the same heading in Newsreader, and measuring in between is measuring a page that
#: exists for 200ms and is not the one anybody sees.
SETTLE = "async () => { await document.fonts.ready; }"


#: With `DEBUG=True` Django answers a missing URL with its own technical page, and that page is not
#: ours: its `<table class="meta">` and its `<code>` overflow below 430px, which the matrix
#: faithfully reported for ten rows before anybody asked whose layout it was. The project's real
#: 404 template only renders with `DEBUG=False`, so on a development server the honest result for
#: this archetype is "not tested here", not a clean row.
DJANGO_TECHNICAL_404 = "pagina tecnica di Django (DEBUG=True) — la 404 del progetto si vede solo con DEBUG=False"


def findings(facts: dict, width: int) -> list[str]:
    """What is wrong, in words, or nothing. A row with an empty list is a row that passed."""
    if "URLconf" in (facts.get("title") or "") or (facts.get("title") or "").startswith("Page not found"):
        return [DJANGO_TECHNICAL_404]
    out = []
    if facts.get("horizontal_scroll"):
        out.append(f"scorrimento orizzontale (documento {facts.get('document_width')}px)")
    for el in facts.get("overflowing", [])[:4]:
        out.append(f"sborda: {el['tag']}.{el['cls'][:34]} fino a {el['right']}px")
    for t in facts.get("small_targets", [])[:4]:
        out.append(f"bersaglio {t['w']}x{t['h']} «{t['text'][:20]}»")
    if facts.get("images_broken"):
        out.append(f"{facts['images_broken']} immagini rotte")
    if facts.get("inputs_without_label"):
        out.append(f"{facts['inputs_without_label']} campi senza etichetta")
    if len(facts.get("h1", [])) != 1:
        out.append(f"{len(facts.get('h1', []))} h1")
    return out


def main(plan_name: str, out_path: str) -> int:
    plan = PLANS[plan_name]
    rows: list[dict] = []

    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = context.pages[0] if context.pages else context.new_page()
        disable_cache(context, page)

        console: list[dict] = []
        page.on("console", lambda m: console.append({"type": m.type, "text": m.text[:160]}))
        page.on("pageerror", lambda e: console.append({"type": "pageerror", "text": str(e)[:160]}))

        for archetype, label, path, widths in plan:
            for width, height in widths:
                console.clear()
                page.set_viewport_size({"width": width, "height": height})
                try:
                    response = page.goto(BASE + path, wait_until="domcontentloaded", timeout=30000)
                    page.evaluate(SETTLE)
                    page.wait_for_timeout(250)
                    facts = page.evaluate(REVIEW_JS)
                    status = response.status if response else 0
                except Exception as exc:  # noqa: BLE001 — a page that will not load IS the finding
                    facts, status = {"error": str(exc)[:160]}, 0

                problems = findings(facts, width)
                errors = [c for c in console if c["type"] in {"error", "pageerror"}]
                rows.append({
                    "archetype": archetype,
                    "page": label,
                    "path": path,
                    "viewport": f"{width}x{height}",
                    "status": status,
                    "findings": problems,
                    "console_errors": errors,
                })
                mark = "." if not problems and not errors else "!"
                print(f"{mark} {label:18s} {width:4d}x{height:<4d} {status} "
                      f"{'; '.join(problems)[:96]}")

    target = ROOT / out_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(rows, indent=1, ensure_ascii=False), encoding="utf-8")

    bad = [r for r in rows if r["findings"] or r["console_errors"] or r["status"] not in (200, 404)]
    widths_run = sorted({int(r["viewport"].split("x")[0]) for r in rows})
    print(f"\n{len(rows)} combinazioni, {len(bad)} con un rilievo -> {out_path}")
    print(f"larghezze percorse: {widths_run}")
    for r in bad:
        print(f"  {r['page']:18s} {r['viewport']:>9s}  {'; '.join(r['findings'])[:110]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1], sys.argv[2]))
