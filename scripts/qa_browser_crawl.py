"""
Breadth browser QA with Playwright (Chromium): every registered public route, four languages, three
viewports, against a running server.

    .venv/Scripts/python scripts/qa_browser_crawl.py http://127.0.0.1:8770 interim
    .venv/Scripts/python scripts/qa_browser_crawl.py http://127.0.0.1:8771 phase3

For each page: HTTP status, html lang/dir, exactly one h1, horizontal overflow, console errors,
failed and external requests, images without alt, tap targets under 24px, text under 12px.
Then every internal link found is requested once. Output: docs/qa/browser/crawl_<label>.json
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path
from urllib.parse import urljoin, urlparse

# The report names URLs and page titles, which contain «, », — and → . On Windows the console
# encoding is cp1252 and printing one of those raises, which killed a forty-minute crawl at its
# final line. The data was never the problem; the writer was.
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "apps"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

import django  # noqa: E402

django.setup()

from django.conf import settings  # noqa: E402
from playwright.async_api import async_playwright  # noqa: E402

from core.public_routes import all_routes  # noqa: E402

VIEWPORTS = [(360, 780), (768, 1024), (1440, 900)]
PAGE_JS = """() => {
  const de = document.documentElement;
  const small = Array.from(document.querySelectorAll('p, li, span, a, label, td, th, button'))
    .filter(e => e.offsetParent && e.innerText && e.innerText.trim().length > 3 && parseFloat(getComputedStyle(e).fontSize) < 12).length;
  const taps = Array.from(document.querySelectorAll('a, button, input, select, textarea'))
    .filter(e => { const r = e.getBoundingClientRect(); const cs = getComputedStyle(e);
      return e.offsetParent && cs.visibility !== 'hidden' && r.width > 0 && (r.width < 24 || r.height < 24) && !e.closest('p, li, .prose, .breadcrumbs') && e.type !== 'hidden' && !e.classList.contains('hp-field'); })
    .map(e => (e.className || e.tagName).toString().slice(0, 40));
  return {lang: de.lang, dir: de.dir, h1: document.querySelectorAll('h1').length,
    overflow: de.scrollWidth > de.clientWidth ? de.scrollWidth - de.clientWidth : 0,
    imgNoAlt: Array.from(document.images).filter(i => !i.hasAttribute('alt')).length,
    smallText: small, smallTaps: taps.slice(0, 8), title: document.title,
    links: Array.from(document.querySelectorAll('a[href]')).map(a => a.getAttribute('href'))};
}"""


async def main(base: str, label: str) -> int:
    langs = [code for code, _ in settings.LANGUAGES]
    routes = all_routes()
    out_dir = ROOT / "docs" / "qa" / "browser"
    out_dir.mkdir(parents=True, exist_ok=True)
    results, internal_links = [], set()
    host = urlparse(base).netloc
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        for width, height in VIEWPORTS:
            ctx = await browser.new_context(viewport={"width": width, "height": height})
            page = await ctx.new_page()
            console, failed, external = [], [], []
            page.on("console", lambda m, sink=console: sink.append(m.text[:200]) if m.type == "error" else None)
            page.on("requestfailed", lambda r, sink=failed: sink.append(r.url[:160]))
            page.on(
                "request",
                lambda r, sink=external: sink.append(r.url[:160]) if urlparse(r.url).netloc not in (host, "") else None,
            )
            for lang in langs:
                for route in routes:
                    url = f"{base}/{lang}/{route.path}"
                    console.clear(), failed.clear(), external.clear()
                    try:
                        response = await page.goto(url, wait_until="networkidle", timeout=45000)
                        status = response.status if response else 0
                        data = await page.evaluate(PAGE_JS) if status == 200 else {}
                    except Exception as exc:  # noqa: BLE001 - QA script records every failure
                        status, data = -1, {"error": str(exc)[:200]}
                    for href in data.pop("links", []):
                        if href.startswith("/") and not href.startswith("//"):
                            internal_links.add(href.split("#")[0])
                    results.append(
                        {
                            "url": url,
                            "w": width,
                            "lang": lang,
                            "gate": route.requires_gate,
                            "status": status,
                            "console": list(console),
                            "failed": list(failed),
                            "external": list(external),
                            **data,
                        }
                    )
            await ctx.close()
        ctx = await browser.new_context()
        link_status = {}
        for href in sorted(internal_links):
            try:
                r = await ctx.request.get(urljoin(base, href), max_redirects=5, timeout=30000)
                link_status[href] = r.status
            except Exception as exc:  # noqa: BLE001
                link_status[href] = str(exc)[:80]
        await browser.close()

    problems = []
    for r in results:
        # A gated page must answer 200 only when ITS gate is the one opened by this run
        # (phase3 run → phase3_public); other gates (virtual_forum, …) may legitimately be 404.
        must_be_open = not r["gate"] or (label == "phase3" and r["gate"] == "phase3_public")
        expected = (200,) if must_be_open else (200, 404)
        issues = []
        if r["status"] not in expected:
            issues.append(f"status {r['status']}")
        if r["status"] == 200:
            rtl = r["lang"] in settings.RTL_LANGUAGES
            if r.get("lang") and r["lang"] != r["url"].split("/")[3]:
                issues.append("html lang mismatch")
            if r.get("dir") != ("rtl" if rtl else "ltr"):
                issues.append(f"dir={r.get('dir')}")
            if r.get("h1") != 1:
                issues.append(f"h1 count {r.get('h1')}")
            if r.get("overflow"):
                issues.append(f"horizontal overflow {r['overflow']}px")
            if r.get("imgNoAlt"):
                issues.append(f"{r['imgNoAlt']} img without alt")
            if r.get("smallText"):
                issues.append(f"{r['smallText']} text nodes < 12px")
            if r.get("smallTaps"):
                issues.append(f"small tap targets: {r['smallTaps']}")
        for key in ("console", "failed", "external"):
            values = r.get(key) or []
            if key == "console" and r["status"] == 404:
                # the browser logs the expected 404 of a gated page itself: not a defect
                values = [v for v in values if "status of 404" not in v]
            if values:
                issues.append(f"{key}: {values[:3]}")
        if issues:
            problems.append({"url": r["url"], "w": r["w"], "issues": issues})
    broken = {h: s for h, s in link_status.items() if s not in (200, 301, 302)}
    summary = {
        "label": label,
        "base": base,
        "pages_checked": len(results),
        "links_checked": len(link_status),
        "pages_with_issues": len(problems),
        "broken_links": broken,
        "problems": problems,
    }
    (out_dir / f"crawl_{label}.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False), encoding="utf-8")
    print(
        f"[{label}] pages={len(results)} links={len(link_status)} pages_with_issues={len(problems)} broken_links={len(broken)}"
    )
    for prob in problems[:40]:
        print("  ", prob["w"], prob["url"].replace(base, ""), "|", "; ".join(prob["issues"])[:220])
    for href, status in list(broken.items())[:20]:
        print("   BROKEN", status, href)
    return 0


if __name__ == "__main__":
    # The label names the output file, so it is required — but a missing argument used to end in an
    # IndexError traceback, which reads like a fault in the crawler rather than in the command.
    if len(sys.argv) != 3:
        print(f"usage: {Path(sys.argv[0]).name} <base-url> <label>", file=sys.stderr)
        print("   e.g. scripts/qa_browser_crawl.py http://127.0.0.1:8771 phase3", file=sys.stderr)
        raise SystemExit(2)
    raise SystemExit(asyncio.run(main(sys.argv[1].rstrip("/"), sys.argv[2])))
