# W4-B — Motion audit: senior review

16 October 2026 · w4-b-review (reviewer; built nothing) · branch `v54-w4-b` at `d63bab3`, from design-v5 `8ab5b89`
(design-v5 is now `11070b5`: the sec-f7 merge, no stylesheet or script changed) · plan §3.6 item 2, §1.5, §2.6, K17;
V5.5 (one review, then fix, then ship).

**Verdict: SHIP_AFTER_FIXES.** Nothing blocks and nothing is major. The library is gone and the hero, «Il varco»,
«Lume», the drawers, the sheet and the popovers move exactly as on design-v5: same animations, same clocks and curves,
0 px of difference on every settled frame. The home's script is under half its budget. Four minor gaps remain in the
area's own checklist: tier 0 from the keyboard in two places, the curve grammar, and one interruption race in the
change this area rewrote. Each takes a few lines to fix. No re-review is needed after the fixes; only a P0 would call
for one.

## How it was checked

- **My own lane:** a dev server on 127.0.0.1:8888 from this worktree, `ile_v5_l8`, `ILE_REFERENCE_DATE=2026-10-03`,
  `DB_CONN_MAX_AGE=0`, `--noreload`, no preview flag. The same lane served a `git archive` of `8ab5b89` as the
  *before* tree.
- **Browsers and sessions:** one headless Chromium at a time, with a fresh context for each load. Sessions were minted
  with `Client.force_login` (no password) and revoked at the end.
- **214 browser loads:** 59 on the before tree and 155 on this branch. They covered fr and ar; 1440, 1366, 390 and
  360; reduced motion on and off.
- **Instrument:** a scratch script, never shipped, recorded every CSS transition, CSS animation, `element.animate()`
  call and CSP report.
- **Evidence:** `C:/tmp/ile_v5_council/evidence/v54/w4-b/review/{base,head}/<scenario>/` (report.json and captures),
  plus `jsweigh-{base,head}.json`.
- **Scripts:** `C:/tmp/ile_v5_council/.work/w4-b/w4-b-review/`.
- **Static checks:**
  - `static/js/dist` and `static/css/dist`, rebuilt from this branch's sources in an isolated copy, are byte for
    byte the committed ones.
  - The targeted non-browser tests passed (199): script gate, the two bundle tests, single submit, the W3-A shell,
    design docs, tokens, rm-flag parity and the static pipeline.

## The brief's checks

| Check | Result |
|---|---|
| The library leaves | `package.json` declares no runtime dependency. `package-lock.json` lost `motion`, `framer-motion`, `motion-dom`, `motion-utils` and `tslib`. No source imports it. Its signatures appear in 1 chunk of the before tree and in 0 files of this branch. |
| Home ≤ 45 KB gzip; no page's JS grows | Measured from the HTML each page serves (static import closure, gzip -9). Home: 51 249 → **24 138 B**, 9 → 7 requests. Door, FAQ, orientation: 43 674 → 16 781 (7 → 6). Login, sign-up: 45 351 → 18 462 (8 → 7). Dashboard, «Mes pièces» at load: 46 070 → 19 178 (9 → 8). «Ma situation»: 47 292 → 20 415 (10 → 9). Every page drops 26.9 KB and one request. |
| Shared CSS ratchet | Measured with the gzip CLI at -9. `main.css` 35 454 → 35 364 B. Console page type (main + console + portal) 44 190 → 44 048. Both go down; the builder's Python figures differ by a few bytes, in the same direction. |
| Every animation through motion.js's gate | Only `motion.js` calls `.animate(` or `requestAnimationFrame` in `static/js/src`. The CSS transitions run on tokens that the reduced-motion block zeroes. |
| No visual regression for bytes | Before and after record identical animations (target, duration, delay, curve, properties): hero discovery (35 / 29 WAAPI; 3 555 ms on desktop, 2 750 / 2 686 ms on phones) and its repeatable flow (1 744 ms); «Il varco»'s arrival (4 × 1 200 ms, staggered 400 ms; none on the band) and focus pass; «Lume» (1 600 ms once, nothing on the second page, 0 ms under the setting); the phone sheet, console drawer and account popover. **0 px** of difference on every settled frame, including «Lume» at 250 ms. |
| «Ma situation»'s change | Same clocks (120 ms out, then 200 ms in) on `--ease-enter`. The arriving question comes 16 px from the right in French and from the left in Arabic. Design-v5's one-frame full-opacity flash is gone (frame samples at ~202 ms). No `style` attribute is left behind. Under the setting it swaps at once. The curve change is the system's (MS-O1) and is accepted. |
| R10 | The rail folds within the press's frame (248 → 64 px; fr and ar; 1440 and 1366) with no transition. A restored fold moves nothing at load. Folded-rail tips still show on hover, fr and ar. |
| Console at load | Dashboard, «Ma situation» and «Mes pièces» × fr and ar × four widths, plus reduced motion at 1440 and 390: only `lume-*` on the first page of a sign-in; every other load is still. |
| A reduced-motion still everywhere | Public pages: 0 motions under the setting. Overlays: one opacity of 80 ms. «Lume»: 0 ms. The question swaps at once. Nothing is running and no `will-change` is left at rest on any load. |
| No text waits for a reveal | Every drawn text node was probed at the top and after scrolling the whole page. The only hits are deliberate: the hero's four per-origin calls (`.he-origin__call`, a line shown under the hand or focus, always in the accessible description, visible on touch screens) and the enquiry form's honeypot label (off-screen, `aria-hidden`). |
| Tier 0 in the public chrome | Esc after a pointer opening: nothing runs (before: the panel's 120 ms exit). Keyboard walk of the portico with the skip link: 0 transitions (before: 8; both trees fade the architrave in once at load, with no travel). A 22-Tab walk of a door page: 0. |
| Forced colours (O2) | At 1440 the rail's current word is underlined; at 390 the bar keeps its lit disc. Focus draws its 2 px ring in fr and ar at 1440 and 390. |
| Hygiene | 0 console errors, 0 CSP reports, no horizontal overflow on any load. The `dir` attribute is correct. The stage, the key and the mark never mirror. |

## Findings

### Minor

**m1 — «Ma situation» animates a change asked from the keyboard (tier 0, R-07).**
- **What happens:** Enter on «Continuer», «Précédent» or a Stepper link runs the full 120 + 200 ms sequence (keyboard
  walk, fr and ar, `keys-situation-*`). The plan's tier 0 is «every keyboard-initiated change».
- **Why it was missed:** the audit fixed the chrome but listed the question change under «click / tap» only.
- **Fix:** in `situation.js`, `const animated = Boolean(travel) && !reducedMotion() && document.documentElement.dataset.input !== "key";`.
  head.js sets `key` on the Enter / Space keydown, before the click.
- **Test:** add a case to `test_motion_browser_w4_b.py`: Tab to «Continuer», press Enter → no `element.animate()`
  call, and the question is swapped in the key's own task.

**m2 — «Ma situation»: returning within the fade leaves no question on screen.**
- **What happens:** «Continuer» then «Précédent» 40 ms later, or a Stepper jump to Q3 then back to Q1 within 40 ms,
  ends with the Stepper on Q1, the counter at «1 / 8» and **no question card** (fr 1440, ar 390;
  `head/situation/interrupt-*`).
- **Cause:** the first change's `enter()` resolves late and hides the question that the second change brought back.
- **History:** design-v5 had the same closure race; there it showed the wrong question with a desynced counter. The
  rewrite fixed the forward double-click (design-v5 left Q3 laid out invisible) but kept the race.
- **Reach:** the window is the 120 ms fade, so this is rare by hand, but it is the one sequence this area
  re-implemented.
- **Fix:**
  1. Keep a generation token: `const turn = ++generation` in `show()`, and `if (turn !== generation) return` at the
     top of `enter()`.
  2. A change asked while another is in flight first lands the old one: cancel the steps' running animations, clear
     their inline opacity, and play the arrival only.
- **Test:** add both reversals to the same test file: exactly the current question visible at opacity 1, no `style`
  left.

**m3 — The console's trail links fade 120 ms when focused from the keyboard.**
- **What happens:** «Accueil» and «Espace réservé» in the console bar run a 120 ms colour transition, with
  `data-input="key"` set. The cause is `v5/base.css`'s `a { transition: color … }` combined with `_shell.css`'s
  `.console-bar .breadcrumbs a:focus-visible` colour.
- **Why it matters:** AUDIT.md §1 records links as instant from the keyboard «through W1-C's rules», but those rules
  cover buttons, fields, tabs and accordions, not plain links.
- **Fix:** one rule, `html[data-input="key"] a { transition-duration: 0ms; }`, in `v5/base.css` (W1-A's file, through
  the steward, as F4 and F5 were).
- **Also:** correct the AUDIT.md line.

**m4 — `--ease-exit` outside its one role (MS-O1 / MS-O2).**
- **Where:** ten declarations, all marked compliant in the audit's tables:
  - the portico's pointer exit (`v5/chrome.css` 419–420);
  - the hover colours of menu items (`v5/overlays.css` 111, `v5/_overlay-panels.css` 79);
  - the rail rows, tools, foot and phone bar (`portal/v5/_shell.css` 228, 316, 387, 446, 1134, 1170).
- **The rule:** MS-O1 puts the way *into* a hover on `--ease-enter`. MS-O2 says a small surface leaves on
  `--ease-enter` at 120 ms, and keeps `--ease-exit` for an object that crosses the view. These rules follow the older
  council table (`council/MOTION.md`, lines 208–291), which the plan superseded.
- **Visible effect:** the portico's 120 ms exit holds near-full opacity for its first ~40 ms, which reads as a lag on
  hover-out. The colour fades barely show.
- **Fix:** a token swap in each declaration (the owners' files, through the steward).

### For the merge step (housekeeping, not findings)

- **Decision-log number:** DL54-132 is taken on design-v5 by the sec-f7 record. Renumber this entry and the three
  mentions in NOTES.md.
- **Ownership check:** `check_ownership.py w4-b design-v5` FAILs by design. Four paths are justified for the manifest:
  `package.json` and `package-lock.json` (steward-only), plus `scripts/build_frontend.mjs` and
  `docs/design-v2/FRONTEND_DEPENDENCIES.md` (no owner).
- **node_modules:** design-v5's `node_modules` keeps the five packages until the steward's next `npm ci`. No build
  imports them.
- **Leftovers for W4-D's sweep:**
  - the dead guard `html.js .page-home .reveal { opacity: 1; }` in `apps/pages/static/pages/css/pages.css:44`, which
    is not in NOTES §7's list;
  - the stale comments that NOTES §7 already names (`v5/tokens.css` l. 468; `console.js`'s line about the rail's
    width).

## Taste, against the bar

- **The right kind of invisible:** where the motion was right, the product moves exactly as before; where the rules
  say it should not move, it is still.
- **The rail:** the fold now reads as a crisp state change rather than a 260 ms reflow, which is the right call for a
  working console.
- **The question change:** it lands faster on the enter curve and lost its flash.
- **Net:** a lighter home (−27 KB of script) with no loss of character. This is credible next to excellent products
  once m1–m4 close the last inconsistencies.
- **Honest limits:**
  - headless Chromium only; Firefox and WebKit are not installed;
  - no person watched the motion at speed;
  - no 8782 trace (W4-C's): performance was judged on bytes, requests and layout work only.
