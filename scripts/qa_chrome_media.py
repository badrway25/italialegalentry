"""
Check a page under the two user settings that break layouts silently.

    python scripts/qa_chrome_media.py http://127.0.0.1:8770/_design/
    python scripts/qa_chrome_media.py http://127.0.0.1:8770/fr/ --json

Two failures this looks for, both of which a screenshot in the default mode cannot show:

REDUCED MOTION. A reveal implemented as «start at opacity 0, animate to 1» disappears completely
when the animation is turned off — the element is not merely still, it is never painted. This is
the most common way a page becomes unusable for someone who set the preference, and DESIGN_SYSTEM_V2
requires the opposite: with the preference on, the composition is COMPLETE and stopped. So the
script emulates the preference and reports every perceivable element left under 10% opacity, or
translated more than 4px from where it should rest.

FORCED COLORS. Windows high-contrast replaces every colour with a system pair and DROPS
background-image and box-shadow. A control whose shape comes only from a background fill has no
shape left: the browser paints it the same colour as the page. So the script reports every button
and badge whose computed border resolves to no width or `none` style once forced-colors is active.

It attaches to the Chrome window that is already open and restores the default emulation before
detaching — otherwise the next person to use that window finds it stuck in high contrast and has
no idea why.

It speaks CDP through scripts/cdp.py rather than Playwright, and that is deliberate: Playwright's
`connect_over_cdp` attaches to every target in the window, and the QA window is the user's own, with
their tabs in it. One sign-in page with hCaptcha iframes was enough to make the attach stop
returning. This script opens one socket to one page and cannot be held up by, or disturb, a tab
that has nothing to do with the test.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cdp import CDPError, Page  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]

#: Shared by the probes. `checkVisibility` with all three options is the only call that accounts
#: for opacity, visibility and content-visibility at once; bare checkVisibility() covers neither
#: opacity nor visibility, and an aria-hidden ancestor makes the element irrelevant either way.
#:
#: `probe()` wraps every snippet in a function, and that is not tidiness. Each `Runtime.evaluate`
#: runs in the SAME global context, so a top-level `const VIS = …` stays declared after the call
#: returns, and the next evaluate that repeats it dies with «Identifier VIS has already been
#: declared». It only showed up when a second probe started running without a reload between them.
PERCEIVABLE = """
const VIS = {contentVisibilityAuto: true, opacityProperty: true, visibilityProperty: true};
const perceivable = (el) => {
  if (typeof el.checkVisibility === 'function' && !el.checkVisibility(VIS)) return false;
  return !(el.getAttribute('aria-hidden') === 'true' || el.closest('[aria-hidden="true"]'));
};
const name = (el) => {
  const classes = (typeof el.className === 'string' && el.className)
    ? '.' + el.className.trim().split(/\\s+/).slice(0, 3).join('.')
    : '';
  return el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + classes;
};
"""


def probe(body: str) -> str:
    """One self-contained expression: helpers and body inside a single arrow function."""
    return "\n".join(["(() => {", PERCEIVABLE, body, "})()"])


MOTION_JS = probe(
    """
  return (() => {
  // `scanned` is not decoration. A probe that reports «no problems» without saying how many
  // elements it looked at cannot be distinguished from a probe that looked at nothing — and a
  // selector typo, or an aria-hidden ancestor higher than expected, produces exactly that.
  const invisible = [], displaced = [];
  let scanned = 0, skipped = 0;
  for (const el of document.querySelectorAll('body *')) {
    if (el.getAttribute('aria-hidden') === 'true' || el.closest('[aria-hidden="true"]')) continue;
    const s = getComputedStyle(el);
    if (s.display === 'none' || s.visibility === 'hidden') { skipped++; continue; }
    if (!el.getClientRects().length) { skipped++; continue; }           // nothing to paint
    // Off-canvas by design: a skip link, a honeypot, a visually-hidden caption. They are
    // SUPPOSED to sit outside the viewport until focused, and reporting them as «displaced»
    // buries the one element that really did fail to arrive. Measured: a.skip-link at y -104.
    const box = el.getBoundingClientRect();
    const offCanvas = (getComputedStyle(el).position === 'absolute' || s.position === 'fixed') &&
      (box.bottom < 0 || box.right < 0 || box.top > innerHeight || box.left > innerWidth);
    if (offCanvas) { skipped++; continue; }
    scanned++;
    const opacity = parseFloat(s.opacity);
    if (opacity < 0.1) invisible.push({el: name(el), opacity});
    // `transform` is the string «none» on almost every element, and DOMMatrixReadOnly('none')
    // THROWS — which aborts the whole evaluate and leaves the probe with no result at all.
    if (s.transform && s.transform !== 'none') {
      const t = new DOMMatrixReadOnly(s.transform);
      if (Math.abs(t.m41) > 4 || Math.abs(t.m42) > 4) {
        displaced.push({el: name(el), x: Math.round(t.m41), y: Math.round(t.m42)});
      }
    }
  }
  // Durations that survive the preference: the site zeroes its own tokens, and anything left
  // running is either a third-party rule or a hard-coded value that missed the switch.
  // Only elements that actually DECLARE an animation. A transition-duration on a control is
  // normal and proves nothing until the control is interacted with, so it is not evidence here.
  const running = [];
  for (const el of document.querySelectorAll('body *')) {
    const s = getComputedStyle(el);
    if (s.animationName === 'none') continue;
    // «Effectively off», not «exactly zero». The usual reduced-motion idiom sets a duration of
    // 1e-05s rather than 0s so that `animationend` still fires and script waiting on it does not
    // hang for ever. Chrome reports that literally, as «1e-05s», and a test for «0s» calls it a
    // running animation. Anything under 20ms is below the threshold of perceived motion.
    const longest = Math.max(...s.animationDuration.split(',').map((d) => parseFloat(d) || 0));
    if (longest < 0.02) continue;
    running.push({el: name(el), animation: s.animationName, duration: s.animationDuration});
  }
  return {
      scanned, skipped,
      reveal_elements: document.querySelectorAll('.reveal, [data-reveal], .reveal--stagger').length,
    invisible: invisible.slice(0, 20),
    displaced: displaced.slice(0, 20),
    still_animating: running.slice(0, 20),
  };
  })();
"""
)

FORCED_JS = probe(
    """
  return (() => {
  const shapeless = [], ok = [];
  const controls = document.querySelectorAll('.btn, .badge, .notice, .card, input, select, textarea, .tabs__tab');
  for (const el of controls) {
    if (!perceivable(el)) continue;
    const s = getComputedStyle(el);
    const w = parseFloat(s.borderTopWidth) || 0;
    const style = s.borderTopStyle;
    const outline = parseFloat(s.outlineWidth) || 0;
    const entry = {
      el: name(el), border: `${style} ${w}px`, outline: `${outline}px`,
      bg: s.backgroundColor, fg: s.color,
    };
    if ((style === 'none' || w === 0) && outline === 0) shapeless.push(entry); else ok.push(entry);
  }
  return {shapeless, with_edge: ok.length, sample: ok.slice(0, 3)};
  })();
"""
)


#: What `FORCED_JS` cannot see. A control keeps its border under high contrast, which is what the
#: first probe checks — but a great deal of this interface's meaning is painted as the BACKGROUND
#: of a pseudo-element: the bar beside the current navigation item, the dot before a field error,
#: the marker of a step. Forced colors overrides background-color and drops background-image, so
#: those indicators can vanish while every border in the page survives. ACCESSIBILITY.md names this
#: as open gate G-26; this probe is how the claim gets measured instead of repeated.
#:
#: It is run TWICE, once in each mode, and the two readings are compared in Python. There is no
#: way to tell from inside forced-colors alone whether a transparent pseudo-element was carrying
#: something a moment ago.
PSEUDO_JS = probe(
    """
  return (() => {
  // EVERY pseudo-element that paints, not a curated list of selectors. The first version of this
  // probe named twelve selectors it expected to matter and found ONE indicator on the home page;
  // the page actually has eighteen. A hand-written list of what to check is a hand-written list of
  // what to miss, and «0 lost» out of 1 is not a result.
  const out = [];
  for (const el of document.querySelectorAll('body *')) {
    if (el.getAttribute('aria-hidden') === 'true' || el.closest('[aria-hidden="true"]')) continue;
    if (!el.getClientRects().length) continue;
    for (const pseudo of ['::before', '::after']) {
      const s = getComputedStyle(el, pseudo);
      if (s.content === 'none') continue;
      const paints = s.backgroundColor !== 'rgba(0, 0, 0, 0)' ||
        s.backgroundImage !== 'none' ||
        (parseFloat(s.borderTopWidth) || 0) > 0;
      out.push({
        key: out.length,
        el: name(el) + pseudo,
        paints,
        w: parseFloat(s.width) || 0,
        h: parseFloat(s.height) || 0,
        bg: s.backgroundColor,
        img: s.backgroundImage,
        border: s.borderTopStyle + ' ' + s.borderTopWidth,
        outline: s.outlineWidth,
        // The colour BEHIND it. Forced colors does not make a background transparent, it
        // replaces it with a system colour — so «lost» means «the same colour as what it sits
        // on», never «transparent». Walk up until something actually paints, because a chain of
        // transparent wrappers says nothing about what the eye sees.
        behind: (() => {
          let node = el;
          while (node && node !== document.documentElement) {
            const bg = getComputedStyle(node).backgroundColor;
            if (bg && bg !== 'rgba(0, 0, 0, 0)') return bg;
            node = node.parentElement;
          }
          return getComputedStyle(document.body).backgroundColor;
        })(),
      });
    }
  }
  return out;
  })();
"""
)


def transparent(colour: str) -> bool:
    """
    True only when the ALPHA is zero.

    The obvious shortcut — «ends with `, 0)`» — reads pure black as transparent, because
    `rgb(0, 0, 0)` ends with exactly those characters. Under forced colors black is CanvasText,
    the single most common colour on the page, so that shortcut would have called every black
    indicator invisible. Found by tests/frontend/test_forced_colors_probe.py, which exists because
    a detector that has never once fired is not evidence of anything.
    """
    if colour in ("transparent", ""):
        return True
    if not colour.startswith("rgba("):
        return False  # rgb(...) always has alpha 1
    parts = colour[len("rgba(") : -1].split(",")
    if len(parts) != 4:
        return False
    try:
        return float(parts[3]) == 0
    except ValueError:
        return False


def lost_indicators(normal: list[dict], forced: list[dict]) -> list[dict]:
    """
    An indicator is LOST when it painted something in normal mode and paints nothing in forced
    colors: no background, no background image, and no border of its own to fall back on.

    Keyed by position in the two lists rather than by selector, because the same selector matches
    many elements and the DOM is identical between the two reads — the page is only reloaded, not
    rebuilt.
    """
    lost = []
    for before, after in zip(normal, forced, strict=False):
        if before["key"] != after["key"] or before["el"] != after["el"]:
            continue  # the two reads drifted; say nothing rather than something wrong
        if not before["paints"]:
            continue
        # Two ways to disappear: painting nothing at all, or painting exactly the colour of what
        # is behind you. Under forced colors the second is the common one, because the browser
        # rewrites the fill to a system colour rather than removing it.
        blank = transparent(after["bg"]) and after["img"] == "none"
        same_as_ground = after["img"] == "none" and after["bg"] == after["behind"]
        no_edge = (after["border"].startswith("none") or after["border"].endswith(" 0px")) and (
            after["outline"] in ("0px", "")
        )
        if (blank or same_as_ground) and no_edge:
            lost.append(
                {
                    "el": before["el"],
                    "size": f"{before['w']}x{before['h']}",
                    "was": before["img"] if before["img"] != "none" else before["bg"],
                    "now": after["bg"],
                    "behind": after["behind"],
                }
            )
    return lost


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    url = argv[0]
    as_json = "--json" in argv
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    try:
        # Match on the HOST, not the path: the QA tab is whichever one is already pointed at the
        # dev server, and this script then navigates it wherever it was asked to look. Matching on
        # the path would refuse every page that is not already open, which is all of them.
        with Page.attach(url_contains=urlparse(url).netloc) as page:
            report: dict[str, object] = {"url": url}
            page.navigate(url, settle=0.4)
            pseudo_normal = page.evaluate(PSEUDO_JS)
            try:
                page.emulate(reduced_motion="reduce")
                page.reload(settle=1.4)  # long enough for an IntersectionObserver to have fired
                report["reduced_motion"] = page.evaluate(MOTION_JS)

                page.emulate(forced_colors="active")
                page.reload(settle=0.9)
                forced = page.evaluate(FORCED_JS)
                forced["indicators_checked"] = len(pseudo_normal)
                forced["indicators_lost"] = lost_indicators(pseudo_normal, page.evaluate(PSEUDO_JS))
                report["forced_colors"] = forced
            finally:
                # Always, even on an exception: a window left in high contrast is a booby trap for
                # whoever looks at it next, and they will not connect it to this script.
                page.emulate()
                page.reload(settle=0.3)
    except CDPError as exc:
        print(f"# CDP: {exc}", file=sys.stderr)
        print("# apri prima la pagina in Chrome, oppure passa un URL gia aperto", file=sys.stderr)
        return 2

    print(json.dumps(report, indent=1, ensure_ascii=False))
    rm = report.get("reduced_motion", {})
    fc = report.get("forced_colors", {})
    problems = (
        len(rm.get("invisible", []))
        + len(rm.get("still_animating", []))
        + len(fc.get("shapeless", []))
        + len(fc.get("indicators_lost", []))
    )
    if not as_json:
        print(f"\n# {problems} rilievi", file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
