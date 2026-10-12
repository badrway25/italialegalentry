# W3-A · Accessibility + performance check — A11Y_PERF

Label `w3-a-a11y-perf`, 10–11 October 2026, one pass (V5.5: implement → review once → fix → ship). Built nothing, changed
nothing in the family's code. Reviewed branch `v54-w3-a` at `9383df1` (merge base with `design-v5` `13ce8c4`), served by
lane 6 from `C:/tmp/ile_wt/v54-w3-a` on `ile_v5_l6`, `ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`, `--noreload`:
the dev server on 8786 for accessibility, then the lane's compressed twin on 8786 for performance (the plan's 8782 shape:
DEBUG off, `CompressedManifestStaticFilesStorage`, hashed URLs, gzip on the wire, `collectstatic` into a scratch root
with `--ignore "portal?console.css"` — the raw console entry that DL54-44 item 4 names; settings outside every
repository). Signed-in pages through sessions minted with `Client.force_login` on `ile_v5_l6` by a scratch script (no
password used, typed or stored; the nine rows revoked at the end). Headless Playwright Chromium (the repository venv's
1.63), one fresh profile per context under `C:/tmp/ile_v5_council/.profiles/w3-a-a11y-perf/`, removed at close; settings
emulated with `reduced_motion="reduce"` and `forced_colors="active"`. One browser and no pytest at a time; every browser
start waited on `PERFORMANCE_BENCHMARK_LOCK` (never present; this role never created it). No run crashed. Never 8780,
8782, 9222 or 9223.

Evidence: `C:/tmp/ile_v5_council/evidence/v54/w3-a/a11y-perf/` — `runs/captures-main.jsonl` + `captures/` (136
captures with the W1-0 tools), `cmp_health.json`, `RESULTS-s1.json` + `s1/` (tree, axe, per state), `RESULTS-s2*.json` +
`s2/` (keyboard), `RESULTS-s3.json` + `s3/` (pixels, targets, modes, reflow), `perf/twin-B/`, `perf/twin-A/`,
`perf/summary-twin-*.json`. Probes: `C:/tmp/ile_v5_council/.work/w3-a/w3-a-a11y-perf/`.

## Verdict — SHIP_AFTER_FIXES

0 blocking · 1 major · 4 minor. No WCAG 2.2 AA failure found in the shell (fr, ar; rail open and compact; the phone
bars and the drawer; 1440, 1366 × 657, 1100, 800, 390, 320, 200 %). No performance regression against the W1-0 before
set: LCP 240–370 ms earlier on every traced cell, the first-render task 30–65 ms where it was 258–500, the longest load
task lower everywhere, CLS ≤ 0.0005, every LCP element unchanged, one request fewer before `load`, nothing loops. The
major is a plan gate, not a WCAG failure: the new one-line console footer draws its three legal links 20 px tall on
every console page.

## Findings

| # | Severity | What | Where | Fix |
|---|---|---|---|---|
| M1 | **major** | **The console footer's legal links are 20 px tall** («Privacy Policy», «Conditions d’utilisation», «Avertissement»; ar «تنبيه» 26.5 × 20) on every console page at every width — under SP-8's 24 px floor, and under its 44 px for every target under a coarse pointer. New with the one-line footer (DL54-45): the before set had 0 targets under 24 px at 390 on the console pages, the branch has 3 on all 34 page types; at 1440 it goes from 2 to 4 («Accueil» in the breadcrumb is the baseline's). WCAG 2.5.8 itself passes by the spacing exception (one row, 16 px apart, nothing within 12 px above or below), hence major and not blocking. | `apps/portal/static/portal/v5/_shell.css` §footer (`.console__footer a`) | `.console__footer a { display: inline-flex; align-items: center; min-block-size: 24px; }` and, in the sheet's `@media (pointer: coarse)` block, `min-block-size: var(--control-md)` (44). Re-measure the footer's height at 390 (it grows by 48 px at most). |
| m1 | minor | **The account popover's rows in the phone bar are 36 px under a coarse pointer** («Espace réservé», «Profil», «Sécurité du compte», «Se déconnecter», 222 × 36 at 390 and 320, fr and ar). SP-8 asks 44 for the bars and every coarse-pointer target. The rule is V4's (`v4/shell.css` `.account-menu__link`), the console's use of the popover is W3-A's. The bar's brand tile is fine: 32 drawn, 44 to the finger through its `::after`. | `_shell.css`, the coarse-pointer block | `.console-bar .account-menu__link { min-block-size: var(--control-md); }` under `(pointer: coarse)`. |
| m2 | minor | **The skip links' ring sits on the light page where the rail is compact**: at 1100 and 1366 × 657 compact, the night ring (`#7fd1d8`, 2 px at 2 px offset) is drawn over `#fbfaf8` → 1.68 : 1 on its own pixels (9.93 : 1 where it crosses the dark rail). Not a failure: the link appears as a navy 52 px box (the box is the indicator, `s2/skip-no-preference-1100-1.png`); but the ring adds nothing there. | `_shell.css` (or the skip-link rule the console sets) | Draw the ring inside the box: `.page-portal .skip-link:focus-visible { outline-offset: -4px; }` (on navy: 9.93 : 1 at every width). |
| m3 | minor (to record at the merge) | **The dashboard page type lands over its §2.6 CSS ceiling.** gzip −9: `portal/console.css` 2 936 → 5 167 B (+2 231), `portal/portal.css` 2 687 → 2 263 B (−424), `main.css` −55 B (its `v5/base.css` lines left). On today's `design-v5` (`main.css` 43 104 B) the dashboard's three sheets come to about **50 479 B for a ceiling of 49 860 B (+619 B, 1.2 %)**; the interior and login page types do not load the console sheets. `console.js` 1 676 → 2 037 B gz (+361). Measured effect: none against the before set (below). A/B against the merge base on the same twin (non-interleaved, n = 9 per cell): longest task within ±35 ms both ways, LCP within +76 ms on the dashboard and +52 … +104 ms on «Mes documents» — inside the two series' spreads (they overlap by 200–400 ms) and still 240–370 ms under the before set. | merge step | Record it in the log as DL54-44 did for the home (§2.6 item 5 under V5.5's performance rule, with these figures), or take 0.7 KB of legacy console rules out first. Not a code finding for this area. |
| m4 | minor | **Under WCAG 1.4.12's text spacing the phone bar's account label ellipsises** («Personne», «qa-company» at 390 and 320, fr and ar). The name stays complete in the drawer's foot and the trigger keeps its accessible name; the loss is the visible word. Nothing else of the shell clips or overlaps under the spacing (rail open and folded, drawer, bottom bar, 320 – 1440). | `_shell.css`, the bar's `.account-menu__name` below 64rem | Let the word go rather than cut it: hide the name (keep it as the accessible name) when it does not fit, or allow it to wrap to two lines. |

**Observations (not counted):**

- Compact rail (below 80rem): «Langue» and «Site public» leave the tab order with the words (14 rail stops for 16
  open); both come back with the rail's toggle, which is the second-last rail stop and works with Enter and Space.
- The dashboard animates at load without the release — `rail-draw` on the journey's steps and `strip-fill` on the health
  strip (8 running at peak, all finite, none under reduced motion). W3-B's / V4's, already noted by W1-D; the shell adds
  none (its fold and the drawer are transitions on a user action).
- The W1-0 health tool's «+1 overlapping target» on every console page is the two skip links sharing their off-screen
  box (only one is ever shown); its «+1 clipped text» on four page types is the rail foot's long account name cut by an
  ellipsis at 1440 — the full name shows in the rail's tip on hover and focus (`clipped()` in `console.js`).
- axe `target-size` with the language list open (the list covers the account link above it) is the open popover itself;
  axe `aria-valid-attr-value` (incomplete) on «Menu»'s `aria-controls` is the closed `<dialog>`, which exists.
- TBT rises against the before set (e.g. dashboard fr 1440 35 → 77 ms) because the page now paints in a 30–65 ms first
  task and finishes in later tasks after FCP; the before set's single 360–500 ms task sat before FCP and never counted.
  The longest load task is lower on every cell; nothing here is W3-A's to change.

## Accessibility — what was measured

**Names, roles, references (s1; 12 cells, 19 states; axe-core 4.13.0, WCAG 2.0–2.2 A/AA run *in* each state: the
language list open, the compact rail, the drawer, the drawer's language list, the account popover).** 0 axe violations
except the open popover's `target-size` above; 0 duplicate ids; 0 unresolved ARIA or `#` references; one `h1` per page;
`aria-current="page"` once per drawn copy of the navigation (rail or bottom bar; the drawer's copy only while it is open);
landmarks: `nav` «Navigation de l’espace réservé», `banner`, `nav` «Mon compte», `nav` «Navigation rapide» (phone),
`main`, `contentinfo`; the drawer is a modal `dialog` named «Navigation de l’espace réservé» holding `nav` «Menu»; every
icon-only control has its word (compact rail: 14 named links and buttons; «Fermer le menu»; «Navigation» with
`aria-expanded`); label-in-name holds for every `aria-label`; 0 inline styles or scripts as served, 0 external hosts, 0 CSP
violations, 0 console errors (all cells, also s2/s3).

**Keyboard (s2; real Tab and Shift+Tab, 13 cells: fr and ar, 1440 open, 1100 compact, 1366 × 657 (person, admin,
«Dossier»), 390, 320, «Mes documents» at 390 and 1366 × 657).** Every stop forward (16–44 per page): **0 without `:focus-visible`, 0 without
a ring on pixels, 0 covered** (5 × 3 points inside every focused box against the sticky bars, the bottom bar and the
rail's pinned foot), 0 hidden behind the bars after the scroll (`scroll-padding-block: 4rem 5.5rem` holds on the long
phone pages). The ring on pixels is the night ring `#7fd1d8` on the rail and the bars (7.65–9.93 : 1 against what it is
drawn over) and the day ring `#1d8a93` on the footer (3.94 : 1); the skip links as m2. Order: skip links → rail (or bar →
bottom bar on phones) → main → footer, the same backward. «Menu» in two keys on every phone page (Tab, Tab, Enter → focus
on «Menu», `:focus-visible`); Enter or Space opens the drawer with focus on the current page's row; Tab cycles inside the
modal (past its last row focus goes to the browser's chrome and comes back to the drawer's first stop — never to the page
behind); Escape and «Fermer le menu» close it and return focus to «Menu» (`aria-expanded` false). The rail's toggle by
Enter and Space folds and opens (248 ↔ 64 px, `aria-expanded` follows, focus stays on the toggle, ringed). In the compact
rail every row's word appears in the tip on focus, and the tip never covers the focused row.

**Contrast on pixels (s3; the glyph method: the text shot as drawn and with its glyphs made transparent; p5 of the
footprint).** Every text of the shell ≥ 4.5 : 1 at the p5, fr and ar, rail open and compact, the bars, the bottom bar,
the drawer, the tip, the footer; the lowest are the 12–14 px section words and the account's role (5.88–6.13 : 1) and the
breadcrumb (6.06–6.25 : 1). DS 2026 asks 4.5 : 1 for small marginalia (its table, `--ink-muted`), not 7 : 1, so these pass.
Forced colours: the current page's row framed, the current disc filled, the tip a framed box, the drawer readable in Arabic
(`s3/*-forced*.png`).

**Reduced motion is a real still.** At load 0 animations under the setting (person dashboard 1440 and 390); the fold of
the rail runs 0 transitions (2 to 6 without the setting); the drawer opens with 0 animations (`console-drawer-in`
without the setting); the skip link stands at its place in the key's own frame (a 120 ms slide without the setting).

**Targets.** Rail rows 44 (40 × 44 compact), the foot's tools 40, the bottom bar's cells 62–112 × 66, the phone bar's
brand 44 to the finger, the account trigger 44; under 24 px only «Accueil» (baseline) and the footer (M1); under a coarse
pointer the popover's rows (m1).

**Reflow and zoom.** No horizontal scroll at 320 (fr, ar), 390, 640 × 400 @ 2 (200 %), 1100, 1366, 1440, with or without
the text spacing; the bottom bar keeps four entries at 320 (the fifth goes to the drawer), its labels on two lines.

## Performance — against `w1-0/before/MANIFEST.json`

**Capture series (136 captures, the before set's `capture.py` / `health.js`, every console page type, fr and ar, 1440 and
390; dev server).** CLS 0 on all 136; 0 running animations at capture; CSS + JS requests before `load` one fewer on every
page type (12 → 11, 11 → 10, 7 → 6: one script fewer, 8 → 7, not this area's); health counts no worse except the items explained
above (M1, the skip-link pair, the ellipsis); 35 clipped texts fewer than before.

**Traced cold loads** — the before set's own `trace.py` `measure()` and `analyse.py` (byte-identical copies), profile A
(150 ms RTT, 1.6 / 0.75 Mbps), CPU × 4, cache off, fresh profile per load, n = 9 per cell interleaved across the cells,
medians (spread), on the compressed twin; «before» = the W1-0 set on 8782 at `v54/base`:

| cell | LCP before → after | first-render task | longest load task | CLS max | LCP element |
|---|---|---|---|---|---|
| dashboard fr 1440 | 1 604 → 1 292 (1 180–1 444) | 405 → 57 | 405 → 127 | 0 | `p.empty` = |
| dashboard fr 412 | 1 584 → 1 248 (1 136–1 296) | 370 → 30 | 370 → 119 | 0 | `p.panel__title` = |
| dashboard ar 1440 | 1 792 → 1 472 (1 416–1 624) | 500 → 59 | 500 → 198 | 0 | `h1.ctx__title` = |
| dashboard ar 412 | 1 740 → 1 448 (1 328–2 012) | 449 → 40 | 449 → 205 | 0 | `p.panel__title` = |
| documents fr 1440 | 1 552 → 1 296 (1 196–1 392) | 354 → 53 | 354 → 110 | 0.0005 | `p.doc-page__lead` = |
| documents fr 412 | 1 564 → 1 184 (1 124–1 396) | 324 → 33 | 324 → 106 | 0 | `p.doc-page__lead` = |
| documents ar 1440 | 1 692 → 1 452 (1 292–1 648) | 435 → 57 | 435 → 142 | 0.0001 | `p.doc-page__lead` = |
| documents ar 412 | 1 672 → 1 412 (1 348–1 684) | 399 → 40 | 399 → 168 | 0 | `p.doc-page__lead` = |
| journey fr 1440 | 1 464 → 1 116 (1 076–1 304) | 292 → 58 | 292 → 61 | 0 | `p` = |
| journey fr 412 | 1 452 → 1 084 (1 044–1 132) | 258 → 31 | 258 → 52 | 0 | `p` = |
| journey ar 1440 | 1 604 → 1 308 (1 256–1 656) | 364 → 61 | 364 → 74 | 0 | `p` = |
| journey ar 412 | 1 552 → 1 292 (1 272–1 332) | 304 → 38 | 304 → 87 | 0 | `p` = |

Every cell inside §2.6 (LCP ≤ before + 50 ms, first-render task ≤ before + 30 ms, LCP ≤ 2.5 s, CLS ≤ 0.05). The
improvement is mostly upstream of W3-A (the A/B in m3: the merge base on the same twin gives the same picture). The
fonts: 23 644 B Latin (3 files), 55 872 B Arabic (4) — inside 32 / 56 KB; the sprite 31 049 B raw (≤ 32 KB). The timing
figures are a lane's screen for regressions, not the Performance Lead's PASS on 8782 (which cannot be rebuilt while
`collectstatic` fails, DL54-44 item 4).

## What this role did not do

No code, no test run, no change to the worktree but this file. The twin's static roots and the merge-base tree were
scratch folders, deleted after the series; the lane's dev server and the twin are stopped; the sessions revoked.
