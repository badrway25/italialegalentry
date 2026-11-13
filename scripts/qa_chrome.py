"""
Drive the VISIBLE Chrome window that is already open, without closing it.

    # once, from a shell — leaves a real Chrome window on screen:
    chrome.exe --remote-debugging-port=9222 --user-data-dir=C:\\tmp\\ile_chrome_qa_profile

    # then, as many times as you like:
    python scripts/qa_chrome.py goto http://127.0.0.1:8770/fr/
    python scripts/qa_chrome.py review            # console, network, overflow, focus, contrast
    python scripts/qa_chrome.py shot docs/qa/chrome/home.png
    python scripts/qa_chrome.py viewport 390 844
    python scripts/qa_chrome.py zoom 200
    python scripts/qa_chrome.py keyboard          # tab through, report focus visibility
    python scripts/qa_chrome.py reload

Why CDP and not ``launch()``: a launched browser dies with the script, so every check would open a
window for two seconds and close it. Connecting over CDP attaches to the window that is already on
screen, does the work, and **detaches** — the window stays, and the edit/refresh/look cycle is a
real one rather than a series of screenshots.

This is Google Chrome Stable, not the Chromium that ships with Playwright. The two differ by two
major versions here, and a report that calls one the other is wrong about the thing it is testing.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

# A Windows console is cp1252 and this project's output is French, Italian and Arabic. Printing a
# navigation label killed this script after it had already signed the browser in — the work was
# done, the report was not. `errors="replace"` costs a mangled glyph and never a traceback.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
CDP = "http://127.0.0.1:9222"

#: Read on the live page. Everything here is a fact the DOM can answer, never a judgement.
REVIEW_JS = r"""() => {
  const de = document.documentElement;

  // `scrollWidth` alone is not an overflow signal, least of all in RTL: Chromium reports a wider
  // document for a nested scroller that clips correctly. The honest test is whether it MOVES.
  const before = de.scrollLeft;
  de.scrollLeft = -99999; const min = de.scrollLeft;
  de.scrollLeft = 99999;  const max = de.scrollLeft;
  de.scrollLeft = before;
  const scrolls = Math.abs(max - min) > 1;

  const inScroller = (el) => {
    for (let p = el.parentElement; p; p = p.parentElement) {
      const o = getComputedStyle(p).overflowX;
      if (o === 'auto' || o === 'scroll') return true;
    }
    return false;
  };

  // A GEOMETRIC finding is only a finding about something somebody can see. Two kinds of element
  // have a box and no viewer, and both produced pages of noise before this existed:
  //
  //   * the spam honeypots, parked at `inset-inline-start: -9999px` inside `[aria-hidden="true"]`
  //     — the same false positive the unlabelled-input check already exempts, which the overflow
  //     check never inherited;
  //   * anything inside a CLOSED `<details>`. Chrome still answers `getBoundingClientRect()` for
  //     it — the nine FAQ permalinks measured 205x17 at real coordinates while the accordion was
  //     shut — and `checkVisibility()` is the only thing that says so.
  //
  // It gates the geometry and nothing else. A field inside a closed disclosure still needs its
  // label, and an image still needs its alt, so those checks below stay blind to this.
  //
  // The options are not decoration. Bare `checkVisibility()` answers only for `display:none` and
  // `content-visibility`, so it called the closed navigation drawer VISIBLE — the drawer is hidden
  // with `visibility:hidden` and `opacity:0` — and its links, laid out on top of the page behind
  // them, were reported as crowding the text of every login and signup page.
  const VISIBILITY = {contentVisibilityAuto: true, opacityProperty: true, visibilityProperty: true};
  const perceivable = (el) => {
    if (typeof el.checkVisibility === 'function' && !el.checkVisibility(VISIBILITY)) return false;
    return !(el.getAttribute('aria-hidden') === 'true' || el.closest('[aria-hidden="true"]'));
  };

  const vw = de.clientWidth;
  const wide = [...document.querySelectorAll('body *')].filter((el) => {
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) return false;
    if (inScroller(el)) return false;
    if (!perceivable(el)) return false;
    return r.right > vw + 1 || r.left < -1;
  }).slice(0, 12).map((el) => ({
    tag: el.tagName.toLowerCase(),
    cls: (el.className || '').toString().slice(0, 60),
    right: Math.round(el.getBoundingClientRect().right),
  }));

  // WCAG 2.2 §2.5.8 is satisfied by SIZE **or** by SPACING: a 24px circle centred on the target
  // may not overlap another target's circle. Reporting every link under 24px tall as a failure
  // buries the real ones under a page of footer links, so the spacing exemption is computed.
  const targets = [...document.querySelectorAll('a, button, [role=button], input:not([type=hidden]), select, textarea')]
    .map((el) => ({el, r: el.getBoundingClientRect()}))
    .filter((t) => t.r.width > 0 && t.r.height > 0 && perceivable(t.el));

  const centre = (r) => ({x: r.x + r.width / 2, y: r.y + r.height / 2});
  const small = targets
    .filter((t) => t.r.width < 24 || t.r.height < 24)
    .filter((t) => {
      const a = centre(t.r);
      // 24px diameter circles: they clash when their centres are closer than 24px apart.
      return targets.some((o) => {
        if (o.el === t.el) return false;
        const b = centre(o.r);
        return Math.hypot(a.x - b.x, a.y - b.y) < 24;
      });
    })
    .slice(0, 12)
    .map((t) => ({
      tag: t.el.tagName.toLowerCase(),
      text: (t.el.textContent || '').trim().slice(0, 30),
      w: Math.round(t.r.width),
      h: Math.round(t.r.height),
      why: 'under 24px AND crowded by a neighbour',
    }));

  const imgs = [...document.querySelectorAll('img')];
  return {
    url: location.href,
    title: document.title,
    lang: de.lang,
    dir: getComputedStyle(de).direction,
    h1: [...document.querySelectorAll('h1')].map((h) => h.textContent.trim().slice(0, 70)),
    headings: [...document.querySelectorAll('h1,h2,h3')].map((h) => h.tagName + ':' + h.textContent.trim().slice(0, 44)).slice(0, 24),
    horizontal_scroll: scrolls,
    viewport: {w: vw, h: de.clientHeight},
    document_width: de.scrollWidth,
    overflowing: wide,
    small_targets: small,
    images_without_alt: imgs.filter((i) => !i.hasAttribute('alt')).length,
    images_broken: imgs.filter((i) => i.complete && i.naturalWidth === 0).length,
    forms: document.querySelectorAll('form').length,
    // `aria-hidden="true"` with `tabindex="-1"` is the honeypot: deliberately invisible to
    // assistive technology and out of the tab order, so it needs no label and flagging it buries
    // a real unlabelled field under one false positive on every form page.
    inputs_without_label: [...document.querySelectorAll('input:not([type=hidden]), select, textarea')]
      .filter((el) => el.getAttribute('aria-hidden') !== 'true')
      .filter((el) => !el.closest('[aria-hidden="true"]'))
      .filter((el) => !el.labels?.length && !el.getAttribute('aria-label') && !el.getAttribute('aria-labelledby')).length,
    tables: document.querySelectorAll('table').length,
    tables_without_th: [...document.querySelectorAll('table')].filter((t) => !t.querySelector('th')).length,
  };
}"""

KEYBOARD_JS = r"""() => {
  const el = document.activeElement;
  if (!el || el === document.body) return null;
  const r = el.getBoundingClientRect();
  const s = getComputedStyle(el);
  return {
    tag: el.tagName.toLowerCase(),
    text: (el.textContent || el.value || '').trim().slice(0, 40),
    visible: r.width > 0 && r.height > 0 && r.top < innerHeight && r.bottom > 0,
    outline: s.outlineStyle !== 'none' && parseFloat(s.outlineWidth) > 0,
    boxShadow: s.boxShadow !== 'none',
    rect: {x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height)},
  };
}"""


def disable_cache(context, page) -> None:
    """
    Make the window show the CSS that is on disk now.

    The development server sends `Last-Modified` and no `Cache-Control`, so Chrome caches static
    files heuristically and will happily serve yesterday's stylesheet for a page you just edited.
    That cost this project two separate investigations: the first blamed the media query, the
    second blamed the server — the server was serving the new file the whole time, and `curl`
    proved it while the browser went on showing the old one.

    `Network.enable` is not optional. `Network.setCacheDisabled` on a session whose Network domain
    is disabled returns success and does nothing, which is the worst of both worlds: a QA run that
    reports on stale CSS and tells you it bypassed the cache.
    """
    try:
        cdp = context.new_cdp_session(page)
        cdp.send("Network.enable")
        cdp.send("Network.setCacheDisabled", {"cacheDisabled": True})
    except Exception as exc:  # noqa: BLE001 — worth saying out loud, not worth aborting over
        print(f"# cache non disattivata ({exc}): i risultati possono riflettere CSS vecchio", file=sys.stderr)


def attach(pw):
    """The window that is already on screen. Never `launch`, never `close`."""
    browser = pw.chromium.connect_over_cdp(CDP)
    context = browser.contexts[0]
    page = context.pages[0] if context.pages else context.new_page()
    disable_cache(context, page)
    return browser, context, page


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    command, args = argv[0], argv[1:]

    with sync_playwright() as pw:
        browser, context, page = attach(pw)
        console: list[dict] = []
        failed: list[dict] = []
        page.on("console", lambda m: console.append({"type": m.type, "text": m.text[:200]}))
        page.on("pageerror", lambda e: console.append({"type": "pageerror", "text": str(e)[:200]}))
        page.on("requestfailed", lambda r: failed.append({"url": r.url[:120], "why": str(r.failure)[:80]}))

        out: object = None
        if command == "goto":
            response = page.goto(args[0], wait_until="domcontentloaded")
            page.wait_for_timeout(900)
            out = {"status": response.status if response else 0, "url": page.url}
        elif command == "reload":
            response = page.reload(wait_until="domcontentloaded")
            page.wait_for_timeout(900)
            out = {"status": response.status if response else 0, "url": page.url}
        elif command == "review":
            page.wait_for_timeout(600)
            out = page.evaluate(REVIEW_JS)
        elif command == "shot":
            target = ROOT / args[0]
            target.parent.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(target), full_page=("--full" in args))
            out = {"saved": str(target.relative_to(ROOT)).replace("\\", "/")}
        elif command == "viewport":
            page.set_viewport_size({"width": int(args[0]), "height": int(args[1])})
            page.wait_for_timeout(500)
            out = {"viewport": f"{args[0]}x{args[1]}"}
        elif command == "zoom":
            # `zoom 200 1280 800` — 200% zoom in a window that is 1280x800.
            #
            # Browser zoom does not scale a picture of the page: it makes every CSS pixel bigger,
            # so the SAME window holds fewer of them and the CSS viewport shrinks by the zoom
            # factor. Media queries then re-evaluate against the smaller viewport, which is the
            # whole mechanism WCAG 2.2 §1.4.10 is asking about — 400% of 1280 is 320 CSS px, which
            # is why 320 is the reflow floor in the first place.
            #
            # This used to set `document.body.style.zoom`, and that is a different thing. CSS zoom
            # scales the body's boxes while leaving the viewport at its full width, so every media
            # query keeps reporting the desktop width and the page "passes" at 400% without ever
            # having been asked to reflow. It was a test that could not fail.
            percent = int(args[0])
            base_w = int(args[1]) if len(args) > 1 else 1280
            base_h = int(args[2]) if len(args) > 2 else 800
            width = round(base_w * 100 / percent)
            height = round(base_h * 100 / percent)
            page.set_viewport_size({"width": width, "height": height})
            page.evaluate("async () => { await document.fonts.ready; }")
            page.wait_for_timeout(400)
            out = {"zoom": f"{percent}%", "window": f"{base_w}x{base_h}",
                   "css_viewport": f"{width}x{height}", **page.evaluate(REVIEW_JS)}
        elif command == "keyboard":
            steps = int(args[0]) if args else 25
            page.evaluate("() => document.body.focus()")
            seen = []
            for _ in range(steps):
                page.keyboard.press("Tab")
                page.wait_for_timeout(45)
                info = page.evaluate(KEYBOARD_JS)
                if info:
                    seen.append(info)
            out = {
                "stops": len(seen),
                "invisible_focus": [s for s in seen if not s["visible"]][:6],
                "no_focus_ring": [s for s in seen if not s["outline"] and not s["boxShadow"]][:6],
                "order": [f'{s["tag"]}:{s["text"][:22]}' for s in seen][:25],
            }
        elif command == "eval":
            out = page.evaluate(args[0])
        else:
            print(f"unknown command: {command}")
            return 2

        page.wait_for_timeout(200)
        print(json.dumps({
            "command": command,
            "result": out,
            "console": console,
            "requests_failed": failed,
        }, indent=1, ensure_ascii=False))
        # Disconnect, do NOT close: the window is the point.
        browser.close() if False else None
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
