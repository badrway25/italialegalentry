# W2-C1 · «Il portico» — accessibility + performance check (V5.5, one pass)

Role: the family's accessibility + performance check (label `w2-c1-a11y-perf`; built nothing). Branch `v54-w2-c1` at
`dc29569` (clean), lane 9: dev server 8789 on `ile_v5_l9`, `ILE_REFERENCE_DATE=2026-10-03`, headless Chromium with this
role's own profiles, every browser series behind the quiet-machine lock. Baseline: the W1-0 «before» set
(`C:/tmp/ile_v5_council/evidence/v54/w1-0/before/MANIFEST.json`, 8782 at `v54/base`). Evidence:
`C:/tmp/ile_v5_council/evidence/v54/w2-c1/a11y-perf/` (E/ below). Scratch and instruments:
`C:/tmp/ile_v5_council/.work/w2-c1/w2-c1-a11y-perf/`. 8 October 20:49 → 21:03 (captures, desktop / laptop / phone
series) and 9 October 08:03 → 08:35 (reflow, reduced motion, forced colours, the role's own probes, perf, the signed-in
seat, the family's browser tests). The model that did this check is Claude Fable 5.1.

## 1. Verdict: SHIP_AFTER_FIXES

No P0. The navbar is keyboard-complete in both directions, every chrome text passes contrast on pixels, focus is
visible on every stop and never obscured, reduced motion is a real still, forced colours hold, 320 px reflows, the
CSS got lighter and the LCP element is unchanged. Two findings must be fixed before the merge (one WCAG 1.4.12 failure
in the three Latin languages, one long task introduced on every scroll-state switch); five are minor.

| # | Severity | Finding | Where | Fix | Acceptance |
|---|---|---|---|---|---|
| 1 | **major** | **WCAG 1.4.12 text spacing (plan §1.12 item 9: «the bar wraps … it never clips»).** With the standard spacing sheet (line-height 1.5, letter 0.12 em, word 0.16 em) the page overflows horizontally and the bar's end items are pushed past the viewport: fr 1024 → `scrollWidth` 1089 («Menu» half out), 1280 → 1426 («Forum» cut, «Projet» and the targa out), 1440 → 1600 (the targa out); it and en the same at all three widths; **ar passes** (no overflow). The bar neither wraps nor falls back. | `static/css/v5/chrome.css` §3–§4 (`.site-header__inner` and `.main-nav__list` are non-wrapping flex rows of `white-space: nowrap` items) | Let the bar wrap at ≥ 64rem (`flex-wrap: wrap` on the list and/or the inner; the header grows, the panels already hang from the inner's foot, the architrave stays at the nav's foot), or fall back to the 1024 layout when the items no longer fit. | `probe_a11y.py` spacing part: `scrollWidth == clientWidth` and no bar item past the viewport, fr / it / en / ar at 1024 / 1280 / 1440 with the sheet applied (E/chrome/RESULTS-probe-spacing.json, probe-spacing-fr-1440.png). |
| 2 | **major** | **A long task on every 64 ↔ 56 switch of the letterhead** (CPU ×4): each wheel crossing of the 24 px sentinel costs 57–93 ms (fr) / 89–125 ms (ar). Isolated: the `portico:layout` relayout alone is 54–77 / 74–107 ms (the four door panels measured at natural height, out of sight, plus the architrave), the 64 → 56 class toggle alone 25–31 ms (what V4 did). The budget row «long tasks: none beyond the first render» (§2.6) is broken on a frequent gesture; unthrottled it is ≈ 15–25 ms. | `static/js/src/nav.js` — `initHeaderState` dispatches `portico:layout` on every sentinel crossing; `initPortico.layout()` re-measures `--portico-h` each time | Split `layout()`: on `portico:layout` re-read `--portico-lead` (one rect: the lock-up shrinks when scrolled, so the lead does move) and re-place the architrave; measure `--portico-h` only on `resize`, the `BAR` change and `fonts.ready`, or cache it per inner width. | No long task > 50 ms on a wheel crossing at CPU ×4, fr and ar (the protocol of E/chrome/RESULTS-layout-cost.json). |
| 3 | minor | **The targa tooltip (icon-only below 90rem) — WCAG 1.4.13.** It shows on hover and on focus (right), but Esc does not dismiss it while the pointer or the focus stays, and it extends 14–18 px past the letterhead's foot over the page (y 87 → 111 / 115 against a header foot at 97). In forced colours it has no border. | `chrome.css` §6 `.targa__tip` | Keep the tip inside the letterhead (above the plate, or ending above the header's foot) so that it never obscures page content — or hide it on Esc until the pointer leaves; add `border: 1px solid CanvasText` under `forced-colors: active`. | E/chrome/RESULTS-probe-{fr,ar}.json → `targa_tip_1280`. |
| 4 | minor | **Smooth scroll on Tab (plan §1.12 item 5 «no smooth scroll on Tab»).** `html { scroll-behavior: smooth }` (base.css:16) also drives focus-navigation scrolling: a stop below the fold arrives after a smooth scroll (the wrap from the footer to the skip link took > 900 ms at 1440), the ring landing only then. Not a WCAG failure (nothing is obscured once settled), the plan's own item. | `static/css/base.css:16` (not the family's file) / `chrome.css` | One rule, `html:focus-within { scroll-behavior: auto; }` (keyboard and programmatic focus jump, wheel and anchor scrolls stay smooth), in chrome.css as the navigation's rule or in base.css through the steward. | E/chrome/RESULTS-probe-*.json → `tab_walk_settled.flagged` shows only mid-scroll samples; after the fix none. |
| 5 | minor | **+1 JS request before `load` on every public page** (budget §2.6 «requests ≤ the before set»): the home 8 → 9, a door page 6 → 7. `scripts/build_frontend.mjs` takes every top-level file of `static/js/src/` as an entry, so `nav.js` (a module, not an entry) is split into `chunks/chunk-BUUEPXNL.js` (9 277 B, 3 343 B gzip) plus a 112 B `dist/nav.js` stub, instead of being inlined into `shell.js`. Bytes are fine (home JS 36 892 → 37 391 B gzip, +499 B). | `scripts/build_frontend.mjs` (outside the slice; the implementer's notes name it) | An explicit entry list (or modules in a subfolder) in the build script, then `dist/` rebuilt from clean — the steward at the merge or W4-B. | Home fr 1440: 8 JS requests before `load`; no `dist/nav.js`. |
| 6 | minor | **The drawer's language segments are 40 px tall on a coarse pointer** (the track is 44, each link 40 × 85) where §1.11 asks 44 for the language control; WCAG 2.5.8 (24) holds. The bar's names at ≥ 48rem are 44 on a coarse pointer, as asked. | `chrome.css` §2 (the V4 segmented track kept for the drawer, which W2-C2 redraws) | `min-block-size: var(--hit-primary)` on the links under `(pointer: coarse)` now, or leave it to W2-C2's sheet. | E/chrome/RESULTS-phone-*.json → `drawer_open.controls`. |
| 7 | minor | **Forced colours: the door chevron keeps its authored grey** (`--icon-muted`, SVG `forced-color-adjust: preserve-parent-color`): 5.9 : 1 on the light forced canvas, ≈ 3.2 : 1 on a dark one. Everything else in the chrome takes the system colours (architrave `Highlight`, panel border and key `CanvasText`, current entry `Highlight` outline, targa and «Menu» `ButtonText`). | icon system (W1-B) — not this family's rule | `@media (forced-colors: active) { .icon { color: CanvasText } }` or `forced-color-adjust: auto` on the icons, with W1-B. | E/chrome/RESULTS-forced-*.json → `open.colours.chevron`. |

Not findings, explained: (a) the `pageerror: missing ) after argument list` lines in the first-pass RESULTS files are the
instrument's own (its injected init script had a syntax error, found with `node --check`; repaired on 9 October, the
perf series re-run): the capture tool, the role's probes and the perf runs report **0 console errors, 0 page errors,
0 CSP violations** on every load. (b) The architrave's 1.25 : 1 in `contrast_open_pointer` was sampled mid-travel; settled
under the pointer it is 4.98 : 1 against the paper above and 5.29 : 1 against the panel below (`architrave_pointer_settled`).
(c) «Overlapping targets» rose 0 → 1 on `navbar-open fr 1440` (and 0 → 5 at 1366 / 1280, outside the comparison set):
the open panel's last entries over the hero's legend rows below it. The health tool counts an absolutely positioned
panel as the flow layer; the covered rows are under a 570 px panel that closes as soon as focus leaves the navigation,
so nothing is reachable or obscured through it. (d) The skip link is on screen when focused in both languages (it slides
in over 120 ms; a single 400 ms sample that said otherwise was superseded by three timelines).

## 2. Accessibility

**Names, roles, landmarks, language** (E/chrome/RESULTS-desktop-*.json, the accessibility tree through CDP on the FAQ).
`region «Barre institutionnelle»` · `navigation «Choisir la langue»` (four links named in their own language, each with
`lang` / `hreflang` / `dir`, the current one `aria-current`) · `banner` · `navigation «Navigation principale»`: the four
doors and «Projet» are `button[aria-expanded][aria-controls]` whose targets exist (`nav-N-portico`), «Forum» a link, the
targa a link named «Espace réservé» / «الفضاء الخاص» at every width (the label visually hidden below 90rem). In the open
panel every entry is a link; the nine (fr) / six (ar) live second lines reach the tree as the link's **description**
(`aria-describedby`, verified in the AX tree: «Votre parcours» → «Italy Legal Entry ne délivre pas de visas …»); the
photograph and the audience disc are ignored (`aria-hidden`, `alt=""`); the French gloss on an Arabic page is a
`lang="fr" dir="ltr"` run. No duplicate id, every ARIA reference resolves, no inline style, the one inline script is the
JSON-LD (home and FAQ, fr and ar). The two drawings of the menu are never on screen together (the portico `display: none`
below 64rem, the drawer `display: none` from 80rem).

**Keyboard walk, fr and ar at 1440** (desktop series `keyboard_model`, the family's tests re-run). Tab order: skip link
→ the four languages → the lock-up → Personnes · Entreprises · Institutions · Universités & Formation · Forum · Projet →
the targa → the page. ↓ on a door opens its panel instantly with the scrim (from y 97, never over the bar) and enters
the first entry; ↓ / ↑ walk the entries, ↑ on the first returns to the door with the panel open; Home / End inside the
panel; ← / → move between items in the eye's direction (ar: ← is next) and an open panel follows (ar from الأفراد, → wraps
to المشروع and opens it); Enter and Space toggle and keep the focus on the door; Esc closes, returns the focus to the door
and removes the scrim; Esc from the page closes a pointer-opened panel; Tab from a door walks its open panel (entries →
«Voir l'espace» → the anti-fraud link) and on to the next door; focus leaving the navigation closes the panel
(`test_the_keyboard_model_of_the_portico`); hover opens after the intent delay without a scrim, a click pins with the
scrim; nothing is pushed on the history. Phone (390, touch): a tap opens the drawer from the header's real foot (y 57,
787 px, the page held still), the first stop is the targa in the drawer, the sections unfold one at a time, Esc closes
the section then the drawer and returns the focus to «Menu», Tab from the last stop and Shift+Tab from the first return
to «Menu». 1024 (fine pointer): the four doors in the bar, the panel without its photograph (944 × 530), «Menu» with
Forum · Projet · the languages; Esc returns the focus to «Menu».

**Focus visible, never obscured.** Every chrome stop draws a 2 px solid ring: laguna 400 on the night bar (9.93 : 1
against its ground), laguna 550 on paper (3.94 : 1) and on the panel's white (4.11 : 1), the doors' ring inset 4 px.
With the scroll settled (450 ms per Tab, 70 stops, fr and ar) no stop ends under the sticky letterhead or covered by
another element (`scroll-padding-block-start` 80 px measured; `test_focus_is_not_obscured_by_the_sticky_letterhead`
green). The panel's first entry sits at y 117, whole, under the 97 px chrome.

**Contrast on pixels** (the mode colour behind each probed text in the PNG, fr and ar, closed / open / pinned /
scrolled glass). Institutional bar 12 px (14 px ar): 15.33 : 1 and 9.94 : 1 on night. Bar words 15 px 500: 6.87 : 1 on
paper, 15.56 : 1 open or current, **6.07–6.17 : 1 on the scrolled glass** (the darkest 1 % of the glass band has
luminance 0.099, the median 0.839). Panel: gloss 16.23, titles 17 px 16.23, second lines 13 px 7.17, «Voir l'espace»
6.32, the anti-fraud link 16.23. Targa label 13 px 15.56, its hairline 3.59 : 1, the chevron 5.88 : 1, the architrave
4.98 / 5.29 : 1, «Menu» 16.23 with a 3.59 : 1 border, the drawer rows 15.56, the drawer's segmented codes 6.0 (idle) /
16.23 (current). The design system asks 4.5 : 1 (AA) of its small text; nothing in the chrome is below 6 : 1.

**Reduced motion** (`emulateMedia`, E/chrome/RESULTS-reduced-*.json, reduced-*.png). Tokens at 0 ms, the panel's
transition `1e-05 s` (components.css §29's universal block still flattens the V5 80 ms rule, as the implementer noted):
a pointer open is at opacity 1 / transform none from the first frame, no entry rise, no photograph cross-fade, no
`is-leaving`, the architrave jumps (`is-jump`), nothing animates at rest, the drawer appears in place. A real still.

**Forced colours** (E/chrome/forced-*.png, by eye and computed). The panel takes a `CanvasText` border, the architrave
`Highlight`, the current entry a `Highlight` outline, the hairline `CanvasText`, the targa and «Menu» `ButtonText`
borders, the key `CanvasText`, the scrim a light veil; the phone drawer's segmented track and sections keep their edges.
Legible in fr and ar; the chevron is finding 7, the tip's border finding 3.

**Reflow and spacing.** 320 × 256 and 320 × 568, fr and ar: no horizontal overflow, the lock-up's words leave by design
(≤ 23rem), «Menu» 46 × 44 with its name kept (the word screen-reader-only), the drawer scrolls within itself
(`overflow-y: auto`, 563 px of content in 199 / 511). Text spacing: finding 1.

**Targets.** Fine pointer: the languages 24 px tall (44–57 wide), the targa 32 × 32 below 90rem and 140 × 32 labelled,
the doors 64 tall, the panel entries 48–110 tall, «Voir l'espace» 44, the anti-fraud link 24, footer links 24. Coarse:
the languages 44 (bar at 1024 touch), the targa 350 × 44 in the drawer, «Menu» 92 × 44, drawer rows 52, sublinks 44,
section toggles 52 × 52; the drawer's language segments 40 (finding 6).

**Signed in** (a session minted on `ile_v5_l9` with `Client.force_login`, revoked after; E/chrome/signed-*.png,
RESULTS-signed.json). The seat holds the account menu's summary named by the account, 136 × 32 at 1440 (44 tall in the
drawer at 390), 15.56 : 1, a 2 px ring on Tab, Enter opens the list (four items of 222 × 36), Esc closes it and keeps
the focus; no targa plate is drawn beside it. Its popover is W2-C2's.

## 3. Performance (lane 9; the budgets are judged on 8782 by the Performance Lead — these are the regressions to flag)

**CSS.** `dist/main.css` 238 603 → 233 969 B raw, **42 646 → 42 505 B gzip (−141 B)** across this family's commits
(`6ed38b3` → `dc29569`); the home's total 45 325 B gzip against its Wave-1 ceiling of 47 306, a door page 42 505 against
44 486, `main.css` under the 45 KB line. No CSS regression; the legacy chrome (v2/shell.css, components.css §5–§7 / §25,
v4/shell.css's chrome) left the cascade.

**JS.** `nav.js` 3 343 B gzip (budget ≤ 4 KB); `shell.js` 1 486 → 720; `main.js` 6 244 → 4 166; the home's JS in all
36 892 → 37 391 B gzip (≤ 45 KB). Requests before `load`: CSS 2 (= before), **JS 9 (before 8)** — finding 5; fonts 2
Latin / 3 Arabic preloads (21.0 / 53.2 KB; W1-A's); images 5 (= before).

**Images.** The four door photographs are fetched only after `load`, at idle, from 80rem: 0 before `load` on every
capture; 4 × 640 webp (109 KB in all) at 1280–1920, **none at 1024 and on phones** (40 captures); `fetchpriority=low`,
`decoding=async`, the graded mean behind them. `test_the_photographs_follow_the_loading_policy` green.

**CLS.** 0.0 on all 72 after captures (home, navbar-open, door-persons, project, antifraud, faq; fr + ar; the standard
set, reduced motion and forced colours) against 0.0004–0.0278 before. Under CPU ×4 one of twelve cold home loads showed
0.0176 (`nav.main-nav` at 578 ms, the font arriving late in a cold throttled profile); each 64 ↔ 56 switch moves the bar's
content by 0.0018 (fr) / 0.0008 (ar) — inherent to the two heights V4 already had. Flagship ≤ 0.05 holds.

**LCP element.** Unchanged: `image.doorway__img` (the hero's arch) at 1440, `p.hero__body` at 412, fr and ar — the
chrome adds nothing to the critical path. Lane timings (no network throttle) are not the baseline's and are not compared.

**Long tasks and interactions, CPU ×4, n = 3 per cell** (E/chrome/RESULTS-perf-*.json, RESULTS-layout-cost.json).
After `load` and 3.5 s of idle: **none** (the nav init and the idle prefetch leave no task). Scroll: finding 2. A pointer
sweep across the bar (the architrave following the nearest item): none. The first pointer open of a door: one task of
50–71 ms in 4 of 6 desktop runs (the panel's first paint with its photograph decode), none on a switch, none on Esc,
none on a keyboard open. Event Timing durations: pointer open 64–112 ms, switch 40–72, keyboard open 24–48, Esc 32–48,
drawer tap 40–64, section unfold 24–40 — all under the 200 ms INP line even throttled ×4. At rest: 0 animations in the
chrome (the 7 running ones are the hero's), 0 `will-change`.

## 4. «No page worse» — the touched page types, fr + ar, 1440 × 900 and 390 × 844 (E/COMPARE_HEALTH.json)

| Metric (before → after, 24 cells) | Result |
|---|---|
| horizontal overflow · overflow offenders · clipped text | 0 → 0 everywhere |
| overlapping targets (same layer) | 0 → 0, except navbar-open fr 1440: 0 → 1 (explained above, (c)) |
| across a fixed layer (navbar-open phones) | 5 → 2 |
| targets under 24 px | 0 → 0 (door-persons / faq ar 1440 had 1 before: gone) |
| CLS of the capture load | ≤ 0.0278 → 0.0 |
| CSP violations · console errors · page errors | 0 → 0 |
| interactive targets at 1440 | 60 → 56 on the home (the four per-entry glyph links of the V4 mega-menu are gone, DE-2); 68 → 64 open |

The after captures were taken by the W1-0 tools (`capture.py`, `health.js`) re-pointed at lane 9: axe and the
instrument's focus walk did not run in this re-run (the facts carry no `axe` / `focus` block), so the axe-contrast and
focus-missing columns of the baseline are answered here by the pixel probes and the settled Tab walk above instead.

## 5. Instruments, protocol, caveats

- Captures: 40 (home + navbar-open on the standard set with the flagship extras) + 16 (door-persons, project, antifraud,
  faq at 1440 / 390) + 8 reduced motion + 8 forced colours, fr and ar, one fresh profile each, DPR 1 — E/after/.
- Series: `chrome_a11y.py` desktop · laptop · phone (8 Oct) · reflow · reduced · forced · perf (9 Oct); the role's
  `probe_a11y.py` (settled Tab walk, skip link, architrave under the pointer, targa tip, text spacing in four
  languages), `probe_signed.py`, the layout-cost probe — E/chrome/RESULTS-*.json and PNGs.
- The lane serves uncompressed files with `DEBUG` on and no network throttle: bytes are compared from the committed
  bundles (gzip −9) and requests by count; timings are indicative; the budgets' PASS is measured on 8782 (§2.6, §2.8).
- Emulated phones and media (`is_mobile`, `has_touch`, `reduced_motion`, `forced_colors`); no Safari, no real device.
- The previous pass's instrument carried a syntax error in its injected observers (see «not findings» (a)); repaired,
  the perf series re-run; the desktop / laptop / phone RESULTS files keep their `pageerror` lines as a record.
- Data writes: one session row on `ile_v5_l9` for the signed-in probe, deleted (`revoked: 1 session rows deleted`); the
  cookie lived only in this role's profile folder and is gone. Nothing typed, no password used.

## 6. Tests run by this role

`tests/frontend/test_browser_w2_c1.py` and `tests/i18n/test_rtl_browser_nav.py` on `test_ile_v5_l9` — **10 passed in
91 s** (the keyboard model, hover intent and the pin, the safe triangle for doors 2–4, the photographs' loading policy,
the no-script fallback with the header no longer sticky, 2.4.11 under the letterhead; N19 in ar and fr, the arrows
following the eye). Not run: the full suite (V5.5: the integration checkpoints run it).
