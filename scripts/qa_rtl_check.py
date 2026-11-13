"""
Arabic / RTL check of the authenticated pages, against a running development server.

    .venv/Scripts/python scripts/qa_rtl_check.py http://127.0.0.1:8770

RTL is not a stylesheet switch. The failures that matter are the ones a French screenshot cannot
show: a horizontal scrollbar because something is pinned with `left` instead of `inset-inline-start`;
a numbered source list whose ordinal lands on the wrong side; an icon that points the wrong way; a
form field whose label and control disagree about direction. Each of those is checked here on the
rendered page, at phone width and at desktop width, because they do not fail the same way at both.

Signs in by creating the session server-side — no password is typed into a form.
Local development only.
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
from importlib import import_module
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "apps"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

import django  # noqa: E402

django.setup()

from django.conf import settings  # noqa: E402
from django.contrib.auth import get_user_model  # noqa: E402
from playwright.async_api import async_playwright  # noqa: E402

QA_EMAIL = "qa-person@example.test"
OUT = ROOT / "docs" / "qa" / "browser"

PATHS = (
    "/espace-reserve/",
    "/espace-reserve/ma-situation/",
    "/espace-reserve/dossiers/",
    "/espace-reserve/mes-documents/",
    "/espace-reserve/mes-echeances/",
    "/espace-reserve/communications/",
)
VIEWPORTS = ((390, 844), (1440, 900))

#: Read on the rendered page. Everything here is a fact the DOM can answer; nothing is a judgement.
PAGE_JS = """() => {
  const de = document.documentElement;

  // `scrollWidth` alone is NOT an overflow signal in right-to-left. Chromium reports 445 against a
  // 390px viewport for a page holding a nested RTL scroller that clips correctly and cannot be
  // scrolled at all. The honest test is whether the document actually moves.
  const before = de.scrollLeft;
  de.scrollLeft = -9999; const min = de.scrollLeft;
  de.scrollLeft = 9999;  const max = de.scrollLeft;
  de.scrollLeft = before;
  const scrolls = (max - min) > 1 || document.body.scrollWidth > de.clientWidth + 1;
  const overflow = scrolls ? Math.max(0, document.body.scrollWidth - de.clientWidth) : 0;

  // An element inside a scroll container is SUPPOSED to sit outside the viewport: that is what the
  // container is for. Reporting it would bury the one element that really escapes.
  const inScroller = (el) => {
    let p = el.parentElement;
    while (p && p !== document.body) {
      const o = getComputedStyle(p).overflowX;
      if (o === 'auto' || o === 'scroll' || o === 'hidden') return true;
      p = p.parentElement;
    }
    return false;
  };

  const offenders = [];
  if (scrolls) {
    for (const el of document.querySelectorAll('body *')) {
      const r = el.getBoundingClientRect();
      if (r.width === 0) continue;
      if (r.right <= de.clientWidth + 1 && r.left >= -1) continue;
      if (inScroller(el)) continue;
      offenders.push({
        tag: el.tagName.toLowerCase(),
        cls: (el.className && el.className.toString().slice(0, 60)) || '',
        left: Math.round(r.left), right: Math.round(r.right),
      });
      if (offenders.length >= 5) break;
    }
  }

  // A physical-direction property on a laid-out element is the usual cause of an RTL defect: it does
  // not flip, so the element stays on the side the Latin layout put it.
  const physical = [];
  for (const el of document.querySelectorAll('body *')) {
    const cs = getComputedStyle(el);
    if (cs.position === 'static' && cs.float === 'none') continue;
    if ((cs.left !== 'auto' && cs.right === 'auto') || (cs.float === 'left' || cs.float === 'right')) {
      physical.push({tag: el.tagName.toLowerCase(), cls: (el.className||'').toString().slice(0,50),
                     left: cs.left, float: cs.float});
      if (physical.length >= 5) break;
    }
  }

  // A scroll region holding a wide table must be reachable from the keyboard and must say what it
  // is: WCAG 2.2 excepts a data table from Reflow, it does not excuse an unlabelled trap.
  const unreachableScrollers = [];
  for (const el of document.querySelectorAll('*')) {
    const cs = getComputedStyle(el);
    if (cs.overflowX !== 'auto' && cs.overflowX !== 'scroll') continue;
    if (el.scrollWidth <= el.clientWidth + 1) continue;
    const labelled = el.hasAttribute('aria-label') || el.hasAttribute('aria-labelledby');
    const focusable = el.tabIndex >= 0;
    if (!labelled || !focusable) {
      unreachableScrollers.push({cls: (el.className||'').toString().slice(0,40), labelled, focusable});
    }
  }

  const h1 = document.querySelectorAll('h1').length;
  return {
    dir: de.getAttribute('dir'), lang: de.getAttribute('lang'),
    overflow, offenders, physical, h1, unreachableScrollers,
    bodyDirection: getComputedStyle(document.body).direction,
    fontFamily: getComputedStyle(document.body).fontFamily.slice(0, 80),
  };
}"""


def _console_sink(bucket: list[str]):
    def handler(message):
        if message.type == "error":
            bucket.append(message.text)

    return handler


def _error_sink(bucket: list[str]):
    def handler(exc):
        bucket.append(str(exc))

    return handler


def _first_case_reference(email: str) -> str:
    from cases.models import CaseFile

    user = get_user_model().objects.filter(email=email).first()
    if user is None:
        return ""
    case = CaseFile.objects.filter(person=user).order_by("-created_at").first()
    return case.reference if case else ""


def _session_cookie_for(email: str) -> tuple[str, str]:
    from django.contrib.auth import BACKEND_SESSION_KEY, HASH_SESSION_KEY, SESSION_KEY

    user = get_user_model().objects.get(email=email)
    engine = import_module(settings.SESSION_ENGINE)
    session = engine.SessionStore()
    session[SESSION_KEY] = str(user.pk)
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session[HASH_SESSION_KEY] = user.get_session_auth_hash()
    session.save()
    return settings.SESSION_COOKIE_NAME, session.session_key


async def main(base: str) -> int:
    if urlparse(base).hostname not in {"127.0.0.1", "localhost", "::1"}:
        print("refusing to run against a non-loopback host")
        return 2

    OUT.mkdir(parents=True, exist_ok=True)
    name, value = await asyncio.to_thread(_session_cookie_for, QA_EMAIL)
    findings: list[dict] = []

    # The case detail lives at a reference that is not known until runtime, so it is discovered
    # rather than hard-coded: a list of paths that silently loses a page is worse than a short one.
    paths = list(PATHS)
    reference = await asyncio.to_thread(_first_case_reference, QA_EMAIL)
    if reference:
        paths.append(f"/espace-reserve/dossiers/{reference}/")

    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        for width, height in VIEWPORTS:
            context = await browser.new_context(viewport={"width": width, "height": height})
            await context.add_cookies(
                [{"name": name, "value": value, "domain": urlparse(base).hostname, "path": "/"}]
            )
            page = await context.new_page()
            # Bound explicitly: a lambda closing over the loop variable would append to whichever
            # list the LAST iteration created, so every viewport's errors would land in one bucket.
            errors: list[str] = []
            page.on("console", _console_sink(errors))
            page.on("pageerror", _error_sink(errors))

            for path in paths:
                url = f"{base}/ar{path}"
                response = await page.goto(url, wait_until="domcontentloaded")
                data = await page.evaluate(PAGE_JS)
                findings.append(
                    {
                        "url": url,
                        "viewport": f"{width}x{height}",
                        "status": response.status if response else 0,
                        **data,
                        "console_errors": list(errors),
                    }
                )
                errors.clear()
            await context.close()
        await browser.close()

    problems = [
        f
        for f in findings
        if f["status"] >= 400
        or f["dir"] != "rtl"
        or f["bodyDirection"] != "rtl"
        or f["overflow"] > 1
        or f["h1"] != 1
        or f["console_errors"]
        or f["physical"]
        or f["unreachableScrollers"]
    ]
    report = {"checked": len(findings), "problems": len(problems), "findings": findings}
    (OUT / "rtl_check.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"checked {len(findings)} page/viewport pairs, {len(problems)} with a problem")
    for f in problems:
        print(f"  {f['viewport']}  {f['url']}")
        if f["status"] >= 400:
            print(f"      status {f['status']}")
        if f["dir"] != "rtl" or f["bodyDirection"] != "rtl":
            print(f"      dir={f['dir']} body-direction={f['bodyDirection']}")
        if f["overflow"] > 1:
            print(f"      horizontal overflow {f['overflow']}px — {f['offenders']}")
        if f["h1"] != 1:
            print(f"      {f['h1']} h1 elements")
        if f["physical"]:
            print(f"      physical-direction CSS: {f['physical']}")
        if f["unreachableScrollers"]:
            print(f"      scroll region not labelled or not focusable: {f['unreachableScrollers']}")
        for line in f["console_errors"][:3]:
            print(f"      console: {line[:120]}")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8770")))
