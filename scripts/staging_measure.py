"""
Measure the staging stack: server timing, payload, and the render metrics a browser can give.

Not Lighthouse, and the report says so. Lighthouse needs a Chrome binary this environment does not
carry for the container's origin, and a Lighthouse score taken against a loopback port on the
machine that is also running the server is a number about this laptop. What Playwright CAN report
honestly is: response time at the socket, transferred bytes, the Navigation Timing marks, First
Contentful Paint and Largest Contentful Paint from the browser's own PerformanceObserver, and the
layout-shift total. Those are the inputs to Core Web Vitals, measured rather than scored.

    python staging_measure.py http://127.0.0.1:8900 out.json
"""

from __future__ import annotations

import json
import statistics
import sys
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

PAGES = [
    ("home_fr", "/fr/"),
    ("home_ar", "/ar/"),
    ("project_fr", "/fr/le-projet/"),
    ("companies_fr", "/fr/entreprises/"),
    ("network_fr", "/fr/reseau/"),
    ("contact_fr", "/fr/contact/"),
    ("forum_fr", "/fr/forum/"),
    ("news_fr", "/fr/actualites/"),
]

VIEWPORTS = {"mobile": (390, 844), "desktop": (1440, 900)}

#: Read inside the page after load. Only facts the browser itself recorded.
METRICS_JS = """() => new Promise((resolve) => {
  const nav = performance.getEntriesByType('navigation')[0] || {};
  let lcp = 0, cls = 0;
  try {
    new PerformanceObserver((list) => {
      for (const e of list.getEntries()) lcp = Math.max(lcp, e.startTime);
    }).observe({type: 'largest-contentful-paint', buffered: true});
    new PerformanceObserver((list) => {
      for (const e of list.getEntries()) if (!e.hadRecentInput) cls += e.value;
    }).observe({type: 'layout-shift', buffered: true});
  } catch (err) { /* an observer this browser does not support */ }
  setTimeout(() => {
    const fcp = (performance.getEntriesByName('first-contentful-paint')[0] || {}).startTime || 0;
    const resources = performance.getEntriesByType('resource');
    resolve({
      ttfb_ms: Math.round(nav.responseStart || 0),
      dom_content_loaded_ms: Math.round(nav.domContentLoadedEventEnd || 0),
      load_ms: Math.round(nav.loadEventEnd || 0),
      fcp_ms: Math.round(fcp),
      lcp_ms: Math.round(lcp),
      cls: Number(cls.toFixed(4)),
      requests: resources.length + 1,
      transferred_bytes: resources.reduce((n, r) => n + (r.transferSize || 0), 0) +
                         (nav.transferSize || 0),
      dom_nodes: document.getElementsByTagName('*').length,
    });
  }, 1200);
})"""


def _console_sink(bucket: list[str]):
    def sink(message) -> None:
        if message.type == "error":
            bucket.append(message.text)

    return sink


def socket_timings(base: str, path: str, rounds: int = 5) -> dict:
    """Server response time without a browser in the way, so the two can be told apart."""
    import time

    times = []
    size = 0
    for _ in range(rounds):
        start = time.perf_counter()
        with urllib.request.urlopen(base + path, timeout=30) as response:  # noqa: S310 - loopback
            body = response.read()
        times.append((time.perf_counter() - start) * 1000)
        size = len(body)
    return {
        "server_ms_median": round(statistics.median(times), 1),
        "server_ms_min": round(min(times), 1),
        "server_ms_max": round(max(times), 1),
        "html_bytes": size,
    }


def main(base: str, out_path: str) -> int:
    results = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for label, path in PAGES:
            socket = socket_timings(base, path)
            for viewport, (width, height) in VIEWPORTS.items():
                context = browser.new_context(viewport={"width": width, "height": height})
                page = context.new_page()
                # Bound explicitly: a lambda closing over the loop variable appends to whichever
                # list the LAST iteration created, so every page's errors land in one bucket.
                console_errors: list[str] = []
                page.on("console", _console_sink(console_errors))
                page.goto(base + path, wait_until="load")
                metrics = page.evaluate(METRICS_JS)
                results.append(
                    {
                        "page": label,
                        "path": path,
                        "viewport": viewport,
                        **socket,
                        **metrics,
                        "console_errors": len(console_errors),
                    }
                )
                context.close()
        browser.close()

    report = {
        "base": base,
        "environment": "staging-like (Linux container, gunicorn 3 workers, whitenoise, DEBUG=False)",
        "not_production_because": [
            "one host, no TLS termination in front, no CDN",
            "loopback: no real network latency, no packet loss",
            "the client browser runs on the same machine as the server",
            "synthetic content only; no rules in force",
        ],
        "measurements": results,
    }
    Path(out_path).write_text(json.dumps(report, indent=1), encoding="utf-8")

    header = (
        f"{'page':16s} {'vp':8s} {'srv ms':>7s} {'TTFB':>6s} {'FCP':>6s} "
        f"{'LCP':>6s} {'CLS':>7s} {'kB':>7s} {'req':>4s}"
    )
    print(header)
    for row in results:
        print(
            f"{row['page']:16s} {row['viewport']:8s} {row['server_ms_median']:7.1f} "
            f"{row['ttfb_ms']:6d} {row['fcp_ms']:6d} {row['lcp_ms']:6d} {row['cls']:7.4f} "
            f"{row['transferred_bytes'] / 1024:7.1f} {row['requests']:4d}"
        )
    worst_lcp = max(r["lcp_ms"] for r in results)
    worst_cls = max(r["cls"] for r in results)
    print(f"\nworst LCP {worst_lcp} ms, worst CLS {worst_cls}")
    print(f"report: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1].rstrip("/"), sys.argv[2]))
