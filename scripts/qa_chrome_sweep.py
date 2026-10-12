"""
Walk a list of routes in the VISIBLE Chrome window, one after another, and report what is wrong.

    python scripts/qa_chrome_sweep.py public   docs/qa/chrome/sweep_public.json
    python scripts/qa_chrome_sweep.py platform docs/qa/chrome/sweep_platform.json
    python scripts/qa_chrome_sweep.py rtl      docs/qa/chrome/sweep_rtl.json

Attaches over CDP to the window that is already on screen, so the pages really appear one by one
and the window is still there at the end. Nothing is launched and nothing is closed.

This is Google Chrome Stable, driven through `connect_over_cdp`, not the Chromium that ships with
Playwright.

What it reports is only what the DOM can answer: console output, failed requests, real horizontal
scrolling, elements outside the viewport that are not inside a scroller, crowded small targets
(WCAG 2.2 §2.5.8 by size OR spacing), missing alt, broken images, unlabelled inputs, heading
structure. Judgement — whether a page looks intentional — is not in here, because a script cannot
make it.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from qa_chrome import REVIEW_JS, disable_cache  # noqa: E402 — one probe, defined once

CDP = "http://127.0.0.1:9222"
#: 8770 has Phase 3 closed, 8771 has it open. `ILE_QA_BASE` picks which one the sweep walks —
#: because half the routes below simply do not exist on the other, and a sweep that reports 404 for
#: a page the gate is supposed to be hiding tells you nothing about either.
BASE = os.environ.get("ILE_QA_BASE", "http://127.0.0.1:8770")

#: The person hub is `/parcours/`, not `/personnes/`. There is no `/personnes/` route at all — the
#: home page's «Personnes» entrance points at the pathways index. Found by clicking it in Chrome
#: after a first sweep reported a 404 that was really a wrong address in this list.
PUBLIC = [
    ("home", "/fr/"),
    ("persone_hub", "/fr/parcours/"),
    ("percorso_lavoro", "/fr/parcours/salaried_work/"),
    ("imprese", "/fr/entreprises/"),
    ("istituzioni", "/fr/institutions/"),
    ("universita", "/fr/universites-et-formation/"),
    ("progetto_pilota", "/fr/projet-pilote/"),
    ("forum", "/fr/forum/"),
    ("forum_iscrizione", "/fr/forum/inscription/"),
    ("faq", "/fr/faq/"),
    ("glossario", "/fr/glossaire/"),
    ("glossario_voce", "/fr/glossaire/nulla_osta/"),
    ("formazione", "/fr/formation/"),
    ("diplomi", "/fr/diplomes-et-titres/"),
    ("vivere_in_italia", "/fr/vivre-en-italie/"),
    ("attualita", "/fr/actualites/"),
    ("progetto", "/fr/le-projet/"),
    ("agami", "/fr/agami/"),
    ("frodi", "/fr/attention-aux-fraudes/"),
    ("contatto", "/fr/contact/"),
    ("contatto_form", "/fr/contact/formulaire/"),
    ("imprese_fabbisogni", "/fr/entreprises/recueil-des-besoins/"),
    ("login", "/fr/compte/login/"),
    ("registrazione", "/fr/compte/signup/"),
    ("reset_password", "/fr/compte/password/reset/"),
    ("404", "/fr/questa-pagina-non-esiste/"),
    ("legali_gate_200", "/fr/note-legali/"),  # 200 con avviso, non 404: il gate spiega invece di sparire
]

PLATFORM = [
    ("cruscotto", "/fr/espace-reserve/"),
    ("situazione", "/fr/espace-reserve/ma-situation/"),
    ("fascicoli", "/fr/espace-reserve/dossiers/"),
    ("documenti", "/fr/espace-reserve/mes-documents/"),
    ("scadenze", "/fr/espace-reserve/mes-echeances/"),
    ("comunicazioni", "/fr/espace-reserve/communications/"),
    ("richieste", "/fr/espace-reserve/mes-demandes/"),
    ("percorso", "/fr/espace-reserve/mon-parcours/"),
    ("academy", "/fr/espace-reserve/formation/"),
    ("sportello", "/fr/espace-reserve/guichet/"),
]

RTL = [
    ("home_ar", "/ar/"),
    ("persone_ar", "/ar/parcours/"),
    ("imprese_ar", "/ar/entreprises/"),
    ("forum_ar", "/ar/forum/"),
    ("cruscotto_ar", "/ar/espace-reserve/"),
    ("fascicoli_ar", "/ar/espace-reserve/dossiers/"),
    ("documenti_ar", "/ar/espace-reserve/mes-documents/"),
    ("academy_ar", "/ar/espace-reserve/formation/"),
]

PLANS = {"public": PUBLIC, "platform": PLATFORM, "rtl": RTL}

#: One representative viewport per sweep, chosen for what the sweep is looking for. The full
#: viewport matrix is a separate pass; running twelve widths over fifty pages produces a number,
#: not a review.
VIEWPORT = {"width": 1440, "height": 900}


def main(plan_name: str, out_path: str) -> int:
    plan = PLANS[plan_name]
    rows = []

    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp(CDP)
        context = browser.contexts[0]
        page = context.pages[0] if context.pages else context.new_page()
        disable_cache(context, page)
        page.set_viewport_size(VIEWPORT)

        # Attached ONCE, outside the loop, writing into buckets that are cleared per page.
        # A listener created inside the loop closes over the LAST iteration's list, so every page's
        # console output lands in one bucket — a trap this project has now met three times — and
        # Playwright's Python API has no `listeners()` to detach them again.
        console: list[dict] = []
        failed: list[dict] = []
        page.on("console", lambda m: console.append({"type": m.type, "text": m.text[:160]}))
        page.on("pageerror", lambda e: console.append({"type": "pageerror", "text": str(e)[:160]}))
        page.on("requestfailed", lambda r: failed.append({"url": r.url[:110], "why": str(r.failure)[:60]}))

        for label, path in plan:
            console.clear()
            failed.clear()

            try:
                response = page.goto(BASE + path, wait_until="domcontentloaded", timeout=30000)
                page.wait_for_timeout(700)
                facts = page.evaluate(REVIEW_JS)
                status = response.status if response else 0
            except Exception as exc:  # noqa: BLE001 — a page that will not load IS the finding
                facts, status = {"error": str(exc)[:200]}, 0

            rows.append({
                "page": label,
                "path": path,
                "status": status,
                **facts,
                "console_errors": [c for c in console if c["type"] in {"error", "pageerror"}],
                "console_warnings": [c for c in console if c["type"] == "warning"][:4],
                "requests_failed": list(failed),
            })
            print(f'{label:24s} {status}  h1={len(facts.get("h1", []))}  '
                  f'overflow={facts.get("horizontal_scroll")}  '
                  f'console={len([c for c in console if c["type"] in {"error", "pageerror"}])}  '
                  f'failed={len(failed)}')

    target = ROOT / out_path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(rows, indent=1, ensure_ascii=False), encoding="utf-8")

    problems = [
        r for r in rows
        if r["status"] not in (200, 302, 404)
        or r.get("horizontal_scroll")
        or r.get("console_errors")
        or r.get("requests_failed")
        or len(r.get("h1", [])) != 1
        or r.get("images_broken")
        or r.get("inputs_without_label")
    ]
    print(f"\n{len(rows)} pagine, {len(problems)} con un rilievo -> {out_path}")
    for p in problems:
        print(f'  {p["page"]}: status={p["status"]} h1={len(p.get("h1", []))} '
              f'overflow={p.get("horizontal_scroll")} console={len(p.get("console_errors", []))} '
              f'failed={len(p.get("requests_failed", []))} broken_img={p.get("images_broken")} '
              f'unlabelled={p.get("inputs_without_label")}')
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1], sys.argv[2]))
