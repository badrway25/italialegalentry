# W4-A · Mobile + RTL sweep — accessibility + performance check (one pass)

Label `w4-a-a11y-perf`, 16 October 2026 — the area's one accessibility/performance check (V5.5: implement → review once
→ fix → ship). Built nothing, changed nothing in the area's code. Checked branch `v54-w4-a` at `844ce81` — its code as
of `a0f733b` (`12955a0`, `4b61dcc` and the senior review's three commits add notes only) — against the merge base,
design-v5 at `b06ea1e`, which stayed design-v5's tip for the whole check.

**The lane, and the database that was not there.** The shared PostgreSQL in Docker (`127.0.0.1:5439`, `ile_v5_l6`)
stopped answering at about 15:35 (NOTES §5), before this check began, and never came back: probed every 20 s from
16:41 to 19:48, every probe timed out; another session's `wsl --shutdown` attempts (16:55–17:10) left Docker Desktop
stopped. Nothing was restarted from this lane — other lanes and the owner's preview depend on that engine. So, as the
senior review did, this check could not load `ile_v5_l6`. Unlike the review, it did not stop at the captures:

- **Every page was served by the lane's own server**, 127.0.0.1:8786 from this worktree (`--noreload`,
  `ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`, no preview flag), **on a scratch PostgreSQL 17.2 cluster** in this
  role's scratch folder (the machine's own binaries, `initdb`, 127.0.0.1:5469 only): `manage.py migrate` + `seed_all`
  (the project's 30 seeds; no QA script, no password set anywhere). Signed-in pages through `Client.force_login` for the
  seed accounts — `seed-person` (a file, `29B2305E54`), `seed-company`, `seed-actor` — sessions revoked and the cluster
  stopped at the end. The worktree was left clean.
- **That base is the go-live state**, the one the lane's QA clone never shows: `scripts/qa_prepare_env.py` opens the
  public forms with `forms_override_without_legal`, while `docs/design-v5/QA/v54/w4-d/GO_LIVE_PHASE.md` ships with G2
  closed («Formulaire temporairement indisponible» on every public form), the legal pages pending, the sign-up and the
  Forum registration closed. The check therefore complements the sweep — and found there the defect the sweep could not
  see (finding 1). Six CMS pages are unpublished on that base (`institutions`, a pathway, diplomas, training, FAQ,
  glossary: Django's DEBUG 404) and are left out of every count below.
- **Not re-measured here, for want of QA records:** D7 (the documents' foot links and «Télécharger»), D8 (a company's
  phone), D16 (a French course title in the phone bar), D18 (a long company name), D22 / D23 (the registers' references,
  dates and saved results), the staff queue; D13 / D24 are the dev showcase's. For those this check re-aggregated the
  implementer's raw probe rows itself (`after/` with `after2/` and `after3/` replacing what they re-measured: 1 908 rows,
  0 errors — no overflow on a product page, under 44 px under a finger only «Ma situation»'s Stepper at 320 (40 px), one
  glossary term in landscape and the dev showcase, chrome ≤ 114 px, every title in the first screen: NOTES §5 holds),
  and the area's browser tests ran green before the outage (26 passed at `4b61dcc`). The ten other browser files did not
  run — the senior review's M2, unchanged.

One headless Chromium at a time (Playwright 1.63, the venv's), each on its own profile under
`C:/tmp/ile_v5_council/.profiles/w4-a-a11y-perf-<mode>/`; the benchmark lock checked before every page (never present);
no pytest. **No browser run crashed.** Never 8780, 8782, 9222 or 9223.

## Verdict — SHIP_AFTER_FIXES

**0 blocking · 0 major of this check's own · 3 minor** (one a hand-off). **No WCAG 2.2 AA failure found** on 37 page
states in fr and ar — keyboard, focus visible and never covered, names and roles, contrast on pixels, reduced motion as a
real still, forced colours, reflow at 320, targets. **The area's fixes hold where this base can draw them** — D1, D2,
D3, D4, D5, D6, D9, D10, D11, D12, D15 (the 500), D20, D21 and W4-B's O1, measured on served pages, fr and ar; D3 and D6
in the very state they were written for. **No performance regression:** both shared bundles lighter, every page type
lighter, no script changed, the dist the sources' exact build; on 450 cold loads A/B against design-v5 the LCP element is
the same in every cell, CLS ≤ 0.0097 on the flagships, no long task or loop introduced.

Two minors are this area's own defect classes, one CSS rule each, and belong in the fix pass with the review's M1:

1. **The go-live notice's e-mail link** — 20 px (fr) / 23 px (ar) tall, under SP-8 under a finger and, in French,
   under the 24 px floor under a mouse, on every public form page of the shipping state (D3 / D6's class).
2. **The console phone bar's account button** loses the top side of its focus ring to the screen's edge, on every
   console page, fr and ar (O1's class).

The third (3: the Academy's filter row lets a focused filter stay clipped) is W3-E's script; handed off. The review's M2
stands as it is: the ten browser files and a lane look at the data-dependent fixes when the database answers — never a
merge on the unrun set.

## What was checked

| Set | Account | Page states (× fr, ar) | Passes |
|---|---|---|---|
| Public, go-live state | — | the home, the phone menu open, the login, the persons' and the companies' doors, the Forum and its (closed) registration, the project, orientation and its resume, the contact form, «Recueil des besoins», two pending legal pages, 404, 500 (16) | under a finger (is_mobile + has_touch, DPR 2): 390 × 844 full, 360 × 800 and 320 × 640 targets + overflow, 844 × 390 landscape; under a mouse: 1440 × 900 full, 320 × 800 (1280 at 400 %); 1366 × 768 full for 16 of the 37 states (nine public, seven console) |
| Console | `seed-person` | dashboard, files, the file, «Mes pièces» (both routes), «Ma situation», «Mon parcours», «Mes demandes», the help desk and a new request, Academy, «Mes échéances», the account page, and four overlay states — drawn open: the console drawer and the account menu at 390, the public account menu at 1440; the documents' filter sheet has no pieces to filter on this base (17) | the same |
| Console | `seed-company`, `seed-actor` | the organisations' bridge (both accounts), the company space, the company's declaration form (4) | the same |

«Full» = the chrome at rest and at three depths, the first object, overflow (page and offenders), every target measured
by `elementFromPoint` through its middle (its own `::before` / `::after` counts, a neighbour's does not; 44 px under a
finger, 24 px under a mouse with WCAG 2.5.8's spacing exception; a link inside a sentence counted apart, as DL54-157
reads SP-8), axe-core 4.13.0 (W1-0's copy; `wcag2a/2aa/21a/21aa/22aa`), pixel contrast on the touched components,
chips and labels, a keyboard walk (each stop: indicator, visibility, covered points, ring cut by the screen), the
reload under `prefers-reduced-motion: reduce` (running animations at rest), the reload under `forced-colors: active`
(capture + a 30-stop walk), and in Arabic every flipped element. Totals: **436 probed loads** (+ 160 reduced-motion and
160 forced-colours reloads), **7 372 targets**, **4 592 keyboard stops** (+ 3 898 under forced colours), **180 axe runs**.
Targeted probes: the overlays opened from the keyboard and left with Tab (both widths), the account ring on pixels, the
date field focused, the Stepper's labels, the chips' words, the flipped icons by sprite id, the Academy's filters.

## Accessibility — results

| Check | Result |
|---|---|
| Keyboard walk, fr + ar | Every stop reached in order, each with a visible ring (2 px outline, `:focus-visible`); none lands on an invisible element. One false alarm cleared on pixels: «Ma situation»'s date field draws its ring ~150 ms after the key (the probe read it at 60 ms; `datefocus/`). **Finding 2** (the console's account button) and **finding 3** (the Academy's filters). |
| Focus never covered | Public pages: 1 596 stops at 390 and 1440, none under the letterhead and **no ring cut at the screen's foot** (O1 holds: 86 → 0 per NOTES, 0 here). Console phones: the top bar and the bottom bar never cover a stop (`scroll-padding-block: 4rem 5.5rem`); the bottom bar's own items draw an inset ring (−2 px). From the keyboard (`overlay_keys.json`): the console drawer takes the focus and keeps it; the account menu takes it and closes when Tab leaves it; nothing focused ever sits under a scrim. One tall textarea («Ouvrir une demande») keeps its foot 20 px under the bottom bar while its caret line is in view (2.4.12, not 2.4.11). |
| Names and roles | axe: **0 violations in 180 runs** (37 states × fr, ar × 1440 / 390 / 1366). |
| Contrast (pixels and computed) | Labels 14.6 : 1 computed (ink on paper; no pixel reading under 4.56); chips' words **7.23 : 1** on their own body (the system wants ≥ 7 for every tone but nullo — `chips_seed-person.json`); the colophon's links 10.7; the passage's station words ≥ 6.46; help and consent links ≥ 5.29; the dashboard's account links 6.05; register meta 6.87; the documents' links 6.05; the phone bar's title 15.3; the Stepper's labels 6.87 (future) and 15.6 (current). Two pixel artefacts corrected before counting: a chip's 1 px edge read as its ground (4.45 → 7.23) and visually hidden labels (the Stepper's on a phone). |
| Reduced motion | **0 running animations at rest on 160 loads** under `reduce`. W4-A adds no motion (no `transition`, `animation`, `@keyframes` or `will-change` in its diff). |
| Forced colours | Every walked stop keeps an outline (3 898 stops; the date field's comes ~150 ms after the key, as above); the captures at 390 read whole — words, borders, CTAs as outlined boxes, the door stage. |
| Reflow (320 under a mouse = 1280 at 400 %) | 0 overflow, every title in the first screen; targets as at 1440. |
| Targets | Under a finger: ≥ 44 × 44 everywhere but the Stepper at 320 (40 × 44, the area's recorded residue) and **finding 1**. Under a mouse: ≥ 24 everywhere but finding 1 (fr) and the console bar's trail at 1366 / 1440 (seen on the way). |
| Phone chrome ≤ 120 px | **114 px at most** (the console's 48 px bar + the two-line bottom bar, fr, 390); the public letterhead 57; 844 × 390: 56 (the bottom bar alone). |
| First object | The `h1` in the first screen in every load, landscape included (D12: the 404's title at 205–255 of 390). |
| Overflow | **0** on every product page, 320 → 1440, fr and ar. |
| RTL | `lang` / `dir` right on every page. In Arabic exactly the closed flip list is flipped — `arrow`, `chevron-end`, `logout`, `send`, `signpost`, `panel-left-close` (`apps/core/icons.py` `FLIP_RTL`) — and nothing else: `ile-arch`, `ile-steps`, the status marks and the lock-up never (`mirrors.json`; the login's converging routes are rotations, not mirrors). |
| W4-A's fixes on served pages | D1 the colophon 44 × ≥ 44 under a finger (24 under a mouse); D20 the lock-up 44 × 44 at 320; D9 the Stepper 44 × 44 at 360, no overflow; D21 the station words 17 px below 64rem, 15 px at 1440; D12 above; D3 / D6 / D2 / D4 / D5 / D10 / D11 no failing target on their pages; D15 the 500's «;» bound to its word (U+00A0 through `typo`, in the capture) (`spot.json`: D1, D9, D12, D20, D21). |

## Performance — results

**Bytes** (gzip −9 per file, summed; each page's sheets as its served HTML links them; `weigh_refs.txt`,
`perf_compare_scratch.txt`). The 13 changed dist files: `main.css` 31 799 → **31 716** (−83) and `portal/console.css`
7 134 → 7 126 (−8); 11 page-only sheets +4 … +80 B (`_pagina.css`, `_journey-passage.css`, the registers', the forum's,
pathways', wizard's…). **Every page type is lighter than design-v5's**, so under every ceiling DL54-154 recorded:

| Page type | V4 (W1-0 «before») | design-v5 = ceiling | W4-A |
|---|---|---|---|
| the home (+ pages + hero) | 39 114 | 46 160 | **46 081** |
| the login (+ entrance) | 37 502 | 36 660 | **36 577** |
| the companies' door (+ ecosystem) | 38 226 | 35 226 | **35 187** |
| the Forum (+ forum) | 38 441 | 34 820 | **34 817** |
| a form page (+ lettura) | 36 294 | 35 900 | **35 850** |
| an error page (+ errori) | 36 294 | 35 428 | **35 363** |
| the dashboard (console + portal + journey) | 41 668 | 42 399 | **42 308** |
| «Mes pièces» (+ documents + panels) | 42 839 | 47 535 | **47 459** |
| «Ma situation» (+ situation) | 41 668 | 42 184 | **42 130** |
| the file with its dialogs (+ registers, case, journey, panels) | 41 668 | 48 289 | **48 269** |

(The rises over V4 are the earlier families' recorded page-only sheets, not this area's.) **JS: unchanged** — no script
in the diff; per page 24 138 B (the home) · 16 781 (a public page) · 18 462 (the login) · 19 168 (a console page) ·
20 537 («Ma situation»), as DL54-154. Requests: the same CSS and JS lists on both trees. **The committed dist is the
sources' exact build:** rebuilt from a clean export of the branch, the whole `static/css/dist/` is byte-identical.

**A/B against design-v5** (the branch point served on the same port from an export of `b06ea1e` in this role's scratch
folder; the same scratch base and sessions; cold cache, CPU × 4, no network throttling — the dev server, so ms are
comparative, not §2.6 budgets): 10 page types × fr, ar × 1440 / 390, n = 3 per tree; then, where the first pass
differed most, an ABAB at 1440 (7 page types, n = 6 per tree pooled), a BAAB at 390 (4 page types, n = 9 per tree
pooled) and 30 more loads of the contact form — **450 loads**:

- **the LCP element is the same in all 40 cells** (the door photograph on the home and the login, the lead or the empty
  state elsewhere);
- LCP, W4-A − design-v5, the per-cell median difference: **+12 ms** at 1440 (−12 … +64) and **+2 ms** at 390
  (−20 … +60), against PFR's ±50 ms; the longest task's and TBT's median differences **0 ms** at both widths (the
  home's first-render task in French at 390: 70 vs 74 ms, over 50 ms in 6 of 9 loads on both trees) — no long task
  introduced;
- **CLS ≤ 0.0097 on the flagships** measured (home, login, dashboard, «Mes pièces»; «Ma situation» and the file too); two
  isolated footer shifts on the contact form in W4-A loads (0.0076, 0.036, at first paint + 16 ms) did not recur in the
  next 20 W4-A loads, and no W4-A rule applies on that page at 1440 — font-swap noise, under 0.10;
- **nothing loops:** 0 `requestAnimationFrame` calls and 0 requests in a 3 s idle window after the settle, every load.

## Findings

### Minor

**1 — The go-live notice's e-mail link is under SP-8 (under a finger; in French under a mouse too).**
- Where: `templates/components/form_unavailable.html` — the notice every public form shows while G2 is closed, which is
  the release state (GO_LIVE_PHASE.md); measured on the companies' door page, «Recueil des besoins» and the contact form,
  drawn by the same include on the collaboration forms, the Forum's registration when it opens, the news' «Restez
  informés», orientation's save and result, the community's join page.
- What: its one link stands alone in its paragraph but is a bare inline run — **20 px tall in French, 23 px in Arabic,
  no hit area**: under 44 px under a finger (fr, ar) and under the 24 px floor under a mouse (fr). WCAG 2.5.8 passes on
  its spacing; SP-8 does not. Captured: `golive-scratchdb/coarse/*/companies_390x844*.png`, `contact-form_*`.
- Why the sweep missed it: the lane's QA clone opens the forms (`forms_override_without_legal`), so the notice was never
  drawn there. Same class as D3 (the pending legal notice's address) and D6 (the closed registration's link).
- Fix: draw a notice body's stand-alone link once — e.g. `.notice__body > p > a:only-child` (or
  `.form-unavailable .notice__body a`): `display: inline-block; padding-block: 2px`, and under `(pointer: coarse)` the
  same −10 px `::after` band as D3 / D6 (which it can then absorb). Where it lands must keep V5.8 (`main.css` never
  rises: pay it with a deletion in the same bundle, or put it in the page-only sheets that draw forms). Re-probe the
  go-live state's form pages at 320 / 360 / 390 and 1440, fr and ar.

**2 — The console phone bar's account button loses the top of its focus ring.**
- Where: every console page that shows the phone bar, fr and ar (390: 34 of 34 walks that reach it).
- What: the button sits 2 px from the screen's top in the 48 px bar; its ring (2 px at +2 px) runs from −2 to 0 px, off
  screen: **0 ring pixels on the top side, 334–338 on each of the other three** (`golive-scratchdb/ring/`,
  `account_ring.json`); its foot also spills 2 px onto the paper below the bar. Visible on three sides, so 2.4.7 passes;
  the plan's ring is whole. W4-B's O1, which this area took for the public pages' foot.
- Fix (`apps/portal/static/portal/v5/_shell.css`, the phone bar): an inset ring for that button, as the bottom bar's
  items already have (`outline-offset: −4px`, inside its 44 px box), or 4 px of block room in the bar. A few bytes in
  `console.css`, which W4-A's −8 / −91 B leave room for under design-v5's ceiling.

**3 — The Academy's filter row lets a focused filter stay clipped (hand-off: W3-E's script).**
- Where: `.reg-filter__list` (the registers' horizontal filter scroller) on Academy, phone, fr and ar
  (`academy_filters.json`).
- What: Tab onto a filter link that lies partly past the scroller's edge does not scroll it — Chromium scrolls a focused
  element only when it is wholly hidden: «Droits et devoirs» shows 47 of its 153 px, «Sécurité au travail» 94 of 163,
  «Formation professionnelle» 97 of 217; in Arabic «الحقوق والواجبات» loses 36 px at the start; the next Tab, onto a
  hidden one, centres it. Never wholly hidden (2.4.11 holds), but the focused name is cut — also at 400 % zoom.
- Fix: in W3-E's registers script, on `focusin` inside a filter scroller, `scrollIntoView({inline: 'nearest',
  block: 'nearest'})`, instant from the keyboard; the same for the needs' state filters. Not this area's code: W3-E, or
  W4-C's keyboard pass.

### Seen on the way — desktop, not this area (W4-C)

- **The console at 1366 / 1440 has no foot scroll padding:** a stop that Tab brings in at the screen's foot keeps its
  ring cut by ~4 px («Toutes mes communications», the dashboard's Academy accordion, the footer's links, «Continuer» and
  «Enregistrer et recalculer», the new request's actions). The public pages have had 8 px since O1.
- **The console bar's trail links are 20 px (fr) / 22 px (ar) tall under a mouse**, under SP-8's 24 px floor (WCAG
  2.5.8 passes on spacing).

## For the fix pass and the merge step

1. Findings 1 and 2 with the review's M1; re-probe those pages (fr, ar; 320–430 under a finger, 1366 / 1440 under a
   mouse); rebuild `static/css/dist` from clean and re-weigh (`main.css` ≤ 31 799 B, console page types ≤ 39 978 B).
2. When the database answers (the review's M2): the ten browser files; this check's lane pass on the QA data — the same
   scripts against `ile_v5_l6`: `mint.py` (lane sessions), `run_a11y.py coarse|fine` with `pages_check.json` (36 states
   incl. D7 / D8 / D16 / D22 / D23's pages), `run_perf.py w4a-lane` then `base-lane` with the branch point served from
   `base_b06ea1e/` (`start_server.py base lane`).
3. Finding 3 to W3-E / W4-C; the two desktop items to W4-C.

## Evidence

`C:/tmp/ile_v5_council/evidence/v54/w4-a/a11y-perf/` — `golive-scratchdb/{coarse,fine}/results.jsonl` and the captures
(`fr/`, `ar/`: each state at 390 and 1440, `*_forced.png`), `golive-scratchdb-1366/`, `golive-scratchdb/perf_*.jsonl`
(the A/B: `w4a-scratch`, `base-scratch`, `w4a2-scratch`, `base2-scratch`, `base3-390`, `w4a3-390`, `base4-390`,
`cf-base3`, `cf-w4a3`), `overlay_keys.json`,
`ring/`, `datefocus/`, `mirrors.json`, `academy_filters.json`, `spot.json`, `chips_seed-person.json`;
`aggregate_{public,console}_{coarse,fine}.txt`, `aggregate_1366.txt`, `weigh_refs.txt`, `perf_compare_scratch.txt`,
`perf_abab_1440.txt`, `perf_baab_390.txt`. Scripts (this check's own — not the implementer's probe): `C:/tmp/ile_v5_council/.work/w4-a/w4-a-a11y-perf/`
(`probe_a11y.js`, `run_a11y.py`, `run_perf.py`, `aggregate.py`, `perf_compare.py`, `abab.py`, `weigh_refs.py`,
`overlay_keys.py`, `ringcheck.py`, `filtercheck.py`, `spot.py`, `chipcheck.py`, `mirrors_check.py`, `start_server.py`,
`mint.py`, `mint_scratch.py`, `pages_*.json`; the scratch cluster in `pg/`, the branch point's export in `base_b06ea1e/`).
