# W4-C — Performance sanity check on the compressed twin 8782 (w4-c-impl-1, 16 October 2026)

Plan §2.6 (the budgets and their protocol), §2.8 (8782), §3.6 item 3; the owner's V5.5 («PERFORMANCE: do not chase
perfection; fix only real regressions, serious blocks, important long tasks, evident LCP/CLS problems»), V5.9 §15
(«performance sanity check») and V5.10 (the release gates).

## The twin and the protocol

- **Server.** 8782 exactly as `C:/tmp/ile_v5_council/evidence/v54/SERVERS.md` §8782 describes, serving **this
  worktree** (`C:/tmp/ile_wt/v54-w4-c` at `dd61b21` for the series — design-v5 at `v54/w4-b`, collected at 09:28 before this area's first commit; the twin's cached templates kept that tree's — and `3ca0b0c` for P1's re-measure, the same tree with this area's two fixes): `collectstatic --clear`
  from the worktree into the twin's own `STATIC_ROOT` (617 files copied, 1 455 post-processed), `settings_8782`
  (`DEBUG = False`, WhiteNoise's `CompressedManifestStaticFilesStorage`, `WHITENOISE_USE_FINDERS = False`), `ile_v5_perf`,
  the reference date 2026-10-03, `CONN_MAX_AGE` 0, `--noreload --nostatic`, the preview flag unset; switched under
  `C:/tmp/ile_locks/PERFORMANCE_BENCHMARK_LOCK` and returned to design-v5's tree at the end (12:25: collectstatic from `C:/tmp/ile_wt/design-v5`, 617 / 1 455, 8782 started from it). Every static
  reference hashed and gzip-encoded on the wire (`main.css` 31 865 B, `immutable`). Signed-in pages through sessions
  minted on `ile_v5_perf` with `Client.force_login` (no password used, typed or stored; revoked at the end). One
  deliberate difference from what ships, said: since devops-2 (DL54-152) the product's storage is
  `core.storage.CompressedManifestModulesStorage` (the ES modules' imports rewritten to hashed names), while
  `settings_8782` keeps WhiteNoise's own class — the same files, bytes and requests on a cold load; only the cache
  lifetime of the unhashed chunk names differs, which a cold load never sees.
- **Cells.** Every page type of `live_status.json` «surfaces» (one page each, by the census's example — the same list as
  A11Y_SWEEP.md, less the states that are not a load: the open menu, a questionnaire step, and the 400 / 500, which
  have no route with DEBUG off), plus the staff's pages and the bridge (a company's declaration; the institution's and
  the university's bridge is the same template and sheets): **78 page types × fr, ar × 1440 × 900 @1 (desktop) and
  390 × 844 @2 (phone, touch) = 312 cells**.
- **One load.** Profile A — 150 ms RTT, 1.6 Mbps down, 750 kbps up (CDP `Network.emulateNetworkConditions`) — and
  CPU × 4 (`Emulation.setCPUThrottlingRate`); cache disabled; a fresh browser context per load (an empty HTTP cache, a
  new renderer); Chromium headless shell 1243 (Playwright 1.63). `goto` to `load`, then rest to ≥ 1.5 s after `load`
  and ≥ 4 s after the navigation start; read from observers registered at document start (buffered): **LCP** (the last
  candidate), **FCP**, **CLS** (the largest session window, input-excluded), the **long tasks** (≥ 50 ms; «after the
  first render» = starting after FCP, the task holding FCP excluded), the long animation frames (their script
  attribution), and Resource Timing: **CSS and JS requests started before `load`**, the encoded bytes per kind (gzip on
  the wire for CSS / JS; woff2 as they are).
- **Statistics (V5.5's sanity rule).** **n = 5 cold loads per cell**, interleaved (run 1 of every cell, then run 2, …,
  the start rotating), median and min–max per cell; the full §2.6 protocol (n ≥ 9 interleaved) owed only where a cell's
  median is within 10 % of a budget or over it.
- **The quiet-machine lock (W1-0's protocol).** Each window: wait while the lock exists; create it atomically; 45 s
  for the gated processes to pause; no new load after 14 min; delete it in a `finally`; 90 s pause. Nine windows, 09:28–11:52 (189 loads each, 48 in the last; `windows.jsonl`), this role's accessibility re-runs and builds holding the lock in the pauses so that they never overlapped a window; then one window each for the overlays' cold opens, the traced loads, the HTTP/2 comparison, the series' one gap (a load whose read failed, refilled) and P1's re-measure. The
  machine was shared (other projects' work: 16 logical cores, 30–45 % busy at the windows' start, ≈ 5 GB free) — the
  medians and spreads below carry that; no run crashed.
- **INP.** W2-A's method on the twin: the page loaded at full speed in a fresh context, 2.5 s of rest, then CPU × 4 and
  the REAL opener pressed (tap on a phone, click on a desktop), 1.1 s, then its close; latency = the longest Event
  Timing entry of the interaction (INP's definition); n = 11 interleaved per cell, p90.
- **HTTP/2.** Plan §2.6's one HTTP/2 measurement, behind a local TLS reverse proxy: Node's own `http2` and `http`
  modules (no package) on 127.0.0.1:8443 in front of 8782, a self-signed loopback certificate (Git's openssl),
  Chromium told to ignore it. The same loads, HTTP/1.1 and HTTP/2 back to back, the order alternating.
- **Cross-engine: not run** — no Playwright WebKit or Firefox binary on this machine, none downloaded; no Safari, no
  real device. Every number is Chromium's.

Evidence: `C:/tmp/ile_v5_council/evidence/v54/w4-c/perf/` (`runs.jsonl` one line per load, `windows.jsonl`,
`summary.json`, `inp.json`, `h2.jsonl`, `trace_lt.json` and its traces); tools: `C:/tmp/ile_v5_council/.work/w4-c/w4-c-impl-1/`
(`twin.py`, `perf.py`, `inp.py`, `trace_lt.py`, `h2proxy.mjs`, `perf_report.py`).

## Verdict — the release gate «performance sanity check» (V5.9 §15): PASS, with one evident CLS problem found and fixed

- **LCP ≤ 2.5 s — PASS on all 312 cells**: the slowest median **1 508 ms** (the home, Arabic, 390), the median of the
  medians 1 140 ms, the slowest single load of 1 559 good loads 1 956 ms; no cell within 10 % of the budget, so the full
  §2.6 protocol is owed nowhere. FCP medians ≤ 1 232 ms.
- **CLS ≤ 0.10, ≤ 0.05 on flagship pages — PASS on 309 cells; FAIL on 3 cells, fixed (P1).** The upload page (W3-C, a
  flagship family) shifted on **every** load — 0.059 / 0.067 / 0.071 at fr 1440, ar 1440, ar 390 (0.042 at fr 390), and
  a piece's page 0.034 in Arabic: the Dépôt's zone, drawn as the browser's own control until `depot.js` (a dynamic
  import) marked it enhanced, then shrinking under the fields that follow it. P1 draws the zone at its final size from
  the first frame (`html.js` instead of `[data-enhanced]`, `_depot.css`; NOTES.md §1): re-measured on the same twin at **n = 9 per cell: CLS 0.000 (max 0.000) on the four
  upload cells** (was 0.042–0.071) and on the four cells of a piece's page (was 0.023–0.035), «Mes pièces» unchanged
  (0.000), the LCP medians within −52 / +44 ms. **After the review fix M2** (the lost-module fallback, `a3613b3`),
  re-measured on a compressed build of the branch (the twin's settings, its own `STATIC_ROOT`, `ile_v5_l4`; the same
  protocol under the lock; n = 9 on the four upload cells, n = 5 on a piece's four): **CLS 0.000 on every cell (max
  0.0005)**, LCP medians 1 040–1 244 ms on the upload page and 1 032–1 308 ms on a piece's, equal to or under the
  review's on `5ea1ce2` (NOTES.md «Review fixes»). Elsewhere: every
  median ≤ 0.035; the letterhead's intermittent shift W3-F2 saw (O1) is still there on public pages — 11 of 860 public
  loads with a shift through `nav.main-nav` above 0.03, one of them over 0.10 (`training`, ar 1440: 0.109), medians ≤
  0.02 — **for W2-C1** (the menu's one-row box reserved before the fonts and the enhancement), not over the budget.
- **INP ≤ 200 ms; an overlay's cold open p90 ≤ 200 ms on the heaviest page — PASS**: seven real openers measured cold
  (n = 11 each, CPU × 4): the console drawer on the Arabic «Mes documents» opens at **p90 112 ms** (390) and 112 ms on
  W2-A's own cell (412 @1.75; W2-A measured 168 ms on a busy lane — its REVIEW m1 «on the INP edge» is answered: no
  change needed); the public phone sheet p90 120 ms; the door panel 112 ms; the piece drawer 88 ms; the case file's
  state dialog 96 ms; the account popover 64 ms; **0 of 154 interactions over 200 ms**, every one checked open and closed.
- **Long tasks «beyond the first render» — none that is not the first render's own.** 809 of 1 559 loads show a task
  ≥ 50 ms starting after the first contentful paint (at CPU × 4: up to 315 ms; the median of the per-cell TBT after FCP
  ≤ 173 ms). Traced (12 cells × 3, W1-0's analysis): they are **the rest of the document's first layout** — the first
  paint now comes early, on the head of a streamed page, and the remainder is styled and laid out in the next one or two
  tasks (e.g. the Arabic home at 390: first paint at 1 206 ms, then 69 ms and 241 ms of style and layout over 98 and 687
  layout objects, **116 ms of it Arabic text shaping**; a door page in Arabic: 217 ms, 138 ms shaping); the fonts had
  arrived before the first paint. Of the 452 long animation frames after the first paint, 337 name no script; the
  other 115 carry the modules' own evaluation at load — `shell.js` with its shared chunk `chunk-VLJVWRTF` (70), the overlay
  core (39: its wiring, up to 174 ms at CPU × 4 on a console phone page). What D27 budgets is the first render, and it
  is lighter than V4's even counted whole: W1-0's single first-render task was 710–938 ms on the same home and
  370–500 ms on the login and the dashboard at CPU × 4; V5's task holding the first paint is under 50 ms on most traced
  cells and ≤ 95 ms on all, and the tasks over 50 ms that follow it add 275–549 ms on the home, 114–217 ms on the
  login, 212–229 ms on the dashboard. **Not a regression, not a serious block; not changed — an accepted exception to
  D27's letter** («none beyond the first render»: these tasks follow the first paint; REVIEW m4, written as such in
  DL54-159 and the release notes' known limits), with no measured cost (LCP ≤ 1.6 s, INP ≤ 152 ms on the review's
  re-measure) — a lead for W2-A / W4-D, not a defect: the overlay core could wire its panels on first use rather than
  at load.
- **Requests (CSS + JS before `load`)** — over W1-0's count on 224 cells, each by what the owner's V5.8 ruling allows
  or by a build question: **+1 CSS** on 172 cells, +2 on the journey's 12, +4 on the case file (3 + 8 → 7 + 8), +1 CSS
  and +1 JS on the documents' 8 (the page-only sheets V5.8 prefers to growing the shared bundles — W3-F1's interior,
  W3-B's dashboards, W3-C's documents, W3-D's journey, W3-E's registers and case file — and the drawer's module);
  **+1 JS** on the 28 entrance cells (esbuild's 394 B runtime-helpers chunk, W4-B's O3) — **an accepted exception to
  the request ratchet's letter** (REVIEW m4; DL54-159; the release notes' known limits), inlining it a build change for
  the steward; the home +1 CSS and −1 JS, the company's dashboard −1 CSS.
  Their cost, measured: none on LCP (the case file's medians 1 108–1 408 ms with its 7 + 8 requests; the login's
  1 136–1 356 ms) — and over HTTP/2: the same loads behind a local TLS proxy move LCP by a median +8 ms (−104 to +160
  ms over 24 cells, n = 3 each: noise). **W3-E's budget letter — the case file's seven stylesheets — answered:
  keep them** (no measured cost; the one-sheet variant would trade one request for 2.6 KB that other pages could no
  longer reuse from cache).
- **Fonts — PASS where the plan sets them**: Latin public **20 956 B** (≤ 25 KB); Latin console ≤ **30 916 B** (≤ 32 KB:
  + ILE Mono, the references' face); Arabic public **53 184 B** (≤ 56 KB). Arabic console pages load **63 144 B**: the
  plan's Arabic figure (set on a public page, «B measured 51.9») plus the same ILE Mono the Latin console budget allows
  for — **an accepted exception to the 56 KB Arabic budget** (REVIEW m4; DL54-159; the release notes' known limits;
  55 872 B without ILE Mono), no LCP cost (the Arabic console medians ≤ 1 460 ms).
- **JS — PASS on the page budgets; the overlay core an accepted exception to the per-module one**: the home
  **24 138 B** gzip (≤ 45 KB, W4-B's figure confirmed on the wire), every public page 16 781 –
  24 138 B, the heaviest console page («Mes pièces») 27 510 B. Per module: the loader 1 521 B, the navigation inlined in
  `shell.js` (3 785 B with it), the overlay core **6 523 B** against §2.6's 4 KB — the figure DL54-95 recorded as «not
  met» (6 466 B then, 6 523 B with the later fixes inside it), with no measured INP cost (above) — accepted, not a
  PASS (REVIEW m4; DL54-159; the release notes' known limits). The Dépôt's chunk 3 702 → 3 751 B with the review fix
  M2 (a console page's JS +49 B: the upload page 24 491 → 24 540 B on the wire).
- **CSS — the ratchet holds**: `main.css` 31 799 B and the console page types 39 978 B gzip −9, unchanged by this area;
  «Mes pièces» 45 475 → 45 472 B (P1, −3 B) → **45 474 B** after the review fix M2: its fallback (+42 B) paid in the same
  page sheet (−40 B: the Dépôt's four `[hidden]` rules made one, its two script-focused elements' four focus rules — a
  restatement of the one focus system — deleted), `documents.css` 5 494 → 5 496 B against design-v5's 5 497; the
  documents' registers with their panels 47 534 B (ceiling 47 535). **Sprite** 31 049 B raw (≤ 32 KB). **Images**: the door row 33 418 B (400 w,
  AVIF) / 47 115 B (576 w) — ≤ 40 kB and ≤ 110 kB.

## Page type × cell — the medians against the budgets

n = the good cold loads of the cell (5; the one cell with 4 had its fifth refilled in P1's window, `runs.jsonl`).
**LCP / CLS** judged on the cell's median: LCP ≤ 2 500 ms; CLS ≤ 0.10, ≤ 0.05 on the pages the flagship families compose
(the entrance, the home, the dashboards and the bridge, the document workspace, the journey and «Ma situation»).
**Long tasks after FCP**: how many of the cell's loads have one, and the longest (CPU × 4) — what they are: below.
**CSS + JS before load**: the cell's count, W1-0's in brackets (↑ = above it: the page sheets V5.8 allows, or the helpers
chunk; the measured cost: none — the verdict). **JS gz** and **fonts**: bytes on the wire (the medians).

| Page type | Cell | n | LCP ms median (min–max) | FCP ms | CLS median / max (budget) | long tasks after FCP: n loads with one / max ms | CSS + JS before load (W1-0) | JS gz B | fonts B | LCP / CLS |
|---|---|---|---|---|---|---|---|---|---|---|
| home | fr 1440 | 5 | 1 304 (1 280–1 944) | 1 088 | 0.016 / 0.020 (0.05) | 3 / 132 | 3 + 7 (2 + 8) | 24 138 | 20 956 | PASS |
| home | ar 1440 | 5 | 1 484 (1 424–1 548) | 1 220 | 0.018 / 0.018 (0.05) | 5 / 129 | 3 + 7 (2 + 8) | 24 138 | 53 184 | PASS |
| home | fr 390 | 5 | 1 320 (1 172–1 348) | 1 072 | 0.000 / 0.000 (0.05) | 4 / 146 | 3 + 7 (2 + 8) | 24 138 | 20 956 | PASS |
| home | ar 390 | 5 | 1 508 (1 336–1 656) | 1 200 | 0.000 / 0.000 (0.05) | 5 / 213 | 3 + 7 (2 + 8) | 24 138 | 53 184 | PASS |
| login | fr 1440 | 5 | 1 144 (1 140–1 436) | 1 048 | 0.000 / 0.020 (0.05) | 2 / 79 | 2 + 7 (2 + 6) ↑ | 18 462 | 20 956 | PASS |
| login | ar 1440 | 5 | 1 324 (1 288–1 356) | 1 200 | 0.000 / 0.000 (0.05) | 5 / 69 | 2 + 7 (2 + 6) ↑ | 18 462 | 53 184 | PASS |
| login | fr 390 | 5 | 1 136 (1 076–1 252) | 1 032 | 0.000 / 0.000 (0.05) | 2 / 105 | 2 + 7 (2 + 6) ↑ | 18 462 | 20 956 | PASS |
| login | ar 390 | 5 | 1 356 (1 332–1 432) | 1 192 | 0.000 / 0.000 (0.05) | 1 / 91 | 2 + 7 (2 + 6) ↑ | 18 462 | 53 184 | PASS |
| signup | fr 1440 | 5 | 1 280 (1 244–1 392) | 1 056 | 0.000 / 0.016 (0.05) | 4 / 105 | 2 + 7 (2 + 6) ↑ | 18 462 | 20 956 | PASS |
| signup | ar 1440 | 5 | 1 348 (1 312–1 744) | 1 212 | 0.000 / 0.018 (0.05) | 5 / 96 | 2 + 7 (2 + 6) ↑ | 18 462 | 53 184 | PASS |
| signup | fr 390 | 5 | 1 112 (1 052–1 276) | 1 024 | 0.000 / 0.000 (0.05) | 0 / — | 2 + 7 (2 + 6) ↑ | 18 462 | 20 956 | PASS |
| signup | ar 390 | 5 | 1 348 (1 308–1 472) | 1 200 | 0.000 / 0.000 (0.05) | 1 / 135 | 2 + 7 (2 + 6) ↑ | 18 462 | 53 184 | PASS |
| password-reset | fr 1440 | 5 | 1 188 (1 108–1 396) | 1 048 | 0.010 / 0.023 (0.05) | 2 / 87 | 2 + 7 (2 + 6) ↑ | 18 462 | 20 956 | PASS |
| password-reset | ar 1440 | 5 | 1 364 (1 272–1 744) | 1 208 | 0.009 / 0.018 (0.05) | 5 / 110 | 2 + 7 (2 + 6) ↑ | 18 462 | 53 184 | PASS |
| password-reset | fr 390 | 5 | 1 092 (1 088–1 140) | 1 020 | 0.000 / 0.000 (0.05) | 1 / 61 | 2 + 7 (2 + 6) ↑ | 18 462 | 20 956 | PASS |
| password-reset | ar 390 | 5 | 1 248 (1 232–1 372) | 1 168 | 0.000 / 0.000 (0.05) | 1 / 81 | 2 + 7 (2 + 6) ↑ | 18 462 | 53 184 | PASS |
| password-reset-done | fr 1440 | 5 | 1 140 (1 120–1 164) | 1 032 | 0.000 / 0.004 (0.05) | 0 / — | 2 + 7 (2 + 6) ↑ | 18 462 | 20 956 | PASS |
| password-reset-done | ar 1440 | 5 | 1 332 (1 320–1 524) | 1 216 | 0.000 / 0.016 (0.05) | 5 / 118 | 2 + 7 (2 + 6) ↑ | 18 462 | 53 184 | PASS |
| password-reset-done | fr 390 | 5 | 1 096 (1 052–1 240) | 1 016 | 0.000 / 0.000 (0.05) | 1 / 100 | 2 + 7 (2 + 6) ↑ | 18 462 | 20 956 | PASS |
| password-reset-done | ar 390 | 5 | 1 248 (1 240–1 408) | 1 152 | 0.000 / 0.000 (0.05) | 1 / 65 | 2 + 7 (2 + 6) ↑ | 18 462 | 53 184 | PASS |
| email-verification-sent | fr 1440 | 5 | 1 156 (1 124–1 368) | 1 048 | 0.000 / 0.010 (0.05) | 3 / 97 | 2 + 7 (2 + 6) ↑ | 18 462 | 20 956 | PASS |
| email-verification-sent | ar 1440 | 5 | 1 332 (1 320–1 624) | 1 208 | 0.000 / 0.018 (0.05) | 4 / 140 | 2 + 7 (2 + 6) ↑ | 18 462 | 53 184 | PASS |
| email-verification-sent | fr 390 | 5 | 1 096 (1 080–1 376) | 1 020 | 0.000 / 0.000 (0.05) | 1 / 55 | 2 + 7 (2 + 6) ↑ | 18 462 | 20 956 | PASS |
| email-verification-sent | ar 390 | 5 | 1 308 (1 292–1 488) | 1 192 | 0.000 / 0.000 (0.05) | 2 / 94 | 2 + 7 (2 + 6) ↑ | 18 462 | 53 184 | PASS |
| pathways | fr 1440 | 5 | 984 (956–1 084) | 872 | 0.000 / 0.024 (0.1) | 3 / 120 | 2 + 6 (1 + 6) ↑ | 16 781 | 20 956 | PASS |
| pathways | ar 1440 | 5 | 1 208 (1 148–1 396) | 1 044 | 0.000 / 0.018 (0.1) | 5 / 185 | 2 + 6 (1 + 6) ↑ | 16 781 | 53 184 | PASS |
| pathways | fr 390 | 5 | 952 (936–1 076) | 844 | 0.000 / 0.000 (0.1) | 1 / 111 | 2 + 6 (1 + 6) ↑ | 16 781 | 20 956 | PASS |
| pathways | ar 390 | 5 | 1 192 (1 104–1 364) | 1 016 | 0.000 / 0.000 (0.1) | 2 / 186 | 2 + 6 (1 + 6) ↑ | 16 781 | 53 184 | PASS |
| companies | fr 1440 | 5 | 968 (932–1 004) | 876 | 0.000 / 0.000 (0.1) | 3 / 79 | 2 + 6 (2 + 6) | 16 781 | 20 956 | PASS |
| companies | ar 1440 | 5 | 1 140 (1 108–1 384) | 1 040 | 0.000 / 0.002 (0.1) | 5 / 226 | 2 + 6 (2 + 6) | 16 781 | 53 184 | PASS |
| companies | fr 390 | 5 | 924 (896–1 928) | 852 | 0.000 / 0.000 (0.1) | 2 / 91 | 2 + 6 (2 + 6) | 16 781 | 20 956 | PASS |
| companies | ar 390 | 5 | 1 136 (1 096–1 260) | 1 000 | 0.000 / 0.000 (0.1) | 1 / 131 | 2 + 6 (2 + 6) | 16 781 | 53 184 | PASS |
| institutions | fr 1440 | 5 | 960 (932–1 088) | 884 | 0.000 / 0.016 (0.1) | 4 / 87 | 2 + 6 (2 + 6) | 16 781 | 20 956 | PASS |
| institutions | ar 1440 | 5 | 1 164 (1 124–1 232) | 1 056 | 0.000 / 0.002 (0.1) | 5 / 91 | 2 + 6 (2 + 6) | 16 781 | 53 184 | PASS |
| institutions | fr 390 | 5 | 936 (900–1 084) | 848 | 0.000 / 0.000 (0.1) | 1 / 113 | 2 + 6 (2 + 6) | 16 781 | 20 956 | PASS |
| institutions | ar 390 | 5 | 1 176 (1 140–1 316) | 1 024 | 0.000 / 0.000 (0.1) | 1 / 169 | 2 + 6 (2 + 6) | 16 781 | 53 184 | PASS |
| universities | fr 1440 | 5 | 972 (940–1 128) | 872 | 0.000 / 0.023 (0.1) | 2 / 80 | 2 + 6 (2 + 6) | 16 781 | 20 956 | PASS |
| universities | ar 1440 | 5 | 1 144 (1 072–1 228) | 1 040 | 0.000 / 0.009 (0.1) | 5 / 97 | 2 + 6 (2 + 6) | 16 781 | 53 184 | PASS |
| universities | fr 390 | 5 | 964 (896–1 128) | 856 | 0.000 / 0.000 (0.1) | 3 / 133 | 2 + 6 (2 + 6) | 16 781 | 20 956 | PASS |
| universities | ar 390 | 5 | 1 104 (1 100–1 140) | 1 016 | 0.000 / 0.000 (0.1) | 1 / 87 | 2 + 6 (2 + 6) | 16 781 | 53 184 | PASS |
| forum | fr 1440 | 5 | 1 048 (976–1 152) | 880 | 0.000 / 0.023 (0.1) | 4 / 102 | 2 + 6 (2 + 6) | 16 781 | 20 956 | PASS |
| forum | ar 1440 | 5 | 1 176 (1 148–1 288) | 1 044 | 0.000 / 0.013 (0.1) | 4 / 104 | 2 + 6 (2 + 6) | 16 781 | 53 184 | PASS |
| forum | fr 390 | 5 | 944 (928–1 060) | 852 | 0.000 / 0.000 (0.1) | 1 / 61 | 2 + 6 (2 + 6) | 16 781 | 20 956 | PASS |
| forum | ar 390 | 5 | 1 168 (1 104–1 240) | 1 012 | 0.000 / 0.000 (0.1) | 1 / 145 | 2 + 6 (2 + 6) | 16 781 | 53 184 | PASS |
| project | fr 1440 | 5 | 1 020 (940–1 096) | 864 | 0.002 / 0.023 (0.1) | 3 / 73 | 2 + 6 (2 + 6) | 16 781 | 20 956 | PASS |
| project | ar 1440 | 5 | 1 148 (1 108–1 300) | 1 048 | 0.000 / 0.016 (0.1) | 5 / 94 | 2 + 6 (2 + 6) | 16 781 | 53 184 | PASS |
| project | fr 390 | 5 | 920 (896–1 072) | 836 | 0.000 / 0.000 (0.1) | 1 / 50 | 2 + 6 (2 + 6) | 16 781 | 20 956 | PASS |
| project | ar 390 | 5 | 1 120 (1 096–1 252) | 1 000 | 0.000 / 0.000 (0.1) | 2 / 134 | 2 + 6 (2 + 6) | 16 781 | 53 184 | PASS |
| pilot | fr 1440 | 5 | 984 (916–1 076) | 868 | 0.002 / 0.020 (0.1) | 3 / 112 | 2 + 6 (2 + 6) | 16 781 | 20 956 | PASS |
| pilot | ar 1440 | 5 | 1 148 (1 092–1 192) | 1 036 | 0.000 / 0.002 (0.1) | 5 / 91 | 2 + 6 (2 + 6) | 16 781 | 53 184 | PASS |
| pilot | fr 390 | 5 | 936 (920–972) | 856 | 0.000 / 0.000 (0.1) | 2 / 60 | 2 + 6 (2 + 6) | 16 781 | 20 956 | PASS |
| pilot | ar 390 | 5 | 1 140 (1 124–1 404) | 1 008 | 0.000 / 0.000 (0.1) | 0 / — | 2 + 6 (2 + 6) | 16 781 | 53 184 | PASS |
| agami | fr 1440 | 5 | 924 (912–1 028) | 860 | 0.000 / 0.016 (0.1) | 2 / 77 | 2 + 6 (2 + 6) | 16 781 | 20 956 | PASS |
| agami | ar 1440 | 5 | 1 140 (1 112–1 332) | 1 032 | 0.000 / 0.009 (0.1) | 5 / 120 | 2 + 6 (2 + 6) | 16 781 | 53 184 | PASS |
| agami | fr 390 | 5 | 928 (904–972) | 832 | 0.000 / 0.000 (0.1) | 2 / 91 | 2 + 6 (2 + 6) | 16 781 | 20 956 | PASS |
| agami | ar 390 | 5 | 1 140 (1 108–1 224) | 1 016 | 0.000 / 0.000 (0.1) | 1 / 128 | 2 + 6 (2 + 6) | 16 781 | 53 184 | PASS |
| network | fr 1440 | 5 | 1 024 (956–1 148) | 880 | 0.002 / 0.010 (0.1) | 4 / 115 | 2 + 6 (2 + 6) | 16 781 | 20 956 | PASS |
| network | ar 1440 | 5 | 1 200 (1 152–1 284) | 1 048 | 0.000 / 0.009 (0.1) | 5 / 145 | 2 + 6 (2 + 6) | 16 781 | 53 184 | PASS |
| network | fr 390 | 5 | 920 (864–984) | 840 | 0.000 / 0.000 (0.1) | 2 / 96 | 2 + 6 (2 + 6) | 16 781 | 20 956 | PASS |
| network | ar 390 | 5 | 1 160 (1 048–1 280) | 1 000 | 0.000 / 0.000 (0.1) | 2 / 163 | 2 + 6 (2 + 6) | 16 781 | 53 184 | PASS |
| antifraud | fr 1440 | 5 | 980 (924–1 080) | 888 | 0.000 / 0.020 (0.1) | 3 / 94 | 2 + 6 (2 + 6) | 16 781 | 20 956 | PASS |
| antifraud | ar 1440 | 5 | 1 140 (1 100–1 144) | 1 040 | 0.000 / 0.009 (0.1) | 5 / 87 | 2 + 6 (2 + 6) | 16 781 | 53 184 | PASS |
| antifraud | fr 390 | 5 | 928 (912–976) | 840 | 0.000 / 0.000 (0.1) | 2 / 94 | 2 + 6 (2 + 6) | 16 781 | 20 956 | PASS |
| antifraud | ar 390 | 5 | 1 144 (1 092–1 344) | 1 020 | 0.000 / 0.000 (0.1) | 1 / 154 | 2 + 6 (2 + 6) | 16 781 | 53 184 | PASS |
| orientation | fr 1440 | 5 | 968 (936–1 140) | 876 | 0.010 / 0.020 (0.1) | 2 / 90 | 2 + 6 (2 + 6) | 16 781 | 20 956 | PASS |
| orientation | ar 1440 | 5 | 1 252 (1 144–1 384) | 1 052 | 0.009 / 0.016 (0.1) | 5 / 177 | 2 + 6 (2 + 6) | 16 781 | 53 184 | PASS |
| orientation | fr 390 | 5 | 940 (932–1 028) | 848 | 0.000 / 0.000 (0.1) | 1 / 94 | 2 + 6 (2 + 6) | 16 781 | 20 956 | PASS |
| orientation | ar 390 | 5 | 1 180 (1 152–1 304) | 1 028 | 0.000 / 0.000 (0.1) | 2 / 166 | 2 + 6 (2 + 6) | 16 781 | 53 184 | PASS |
| orientation-resume | fr 1440 | 5 | 964 (952–1 068) | 884 | 0.000 / 0.023 (0.1) | 0 / — | 2 + 6 (2 + 6) | 16 781 | 20 956 | PASS |
| orientation-resume | ar 1440 | 5 | 1 152 (1 120–1 168) | 1 064 | 0.000 / 0.000 (0.1) | 5 / 85 | 2 + 6 (2 + 6) | 16 781 | 53 184 | PASS |
| orientation-resume | fr 390 | 5 | 944 (916–1 088) | 856 | 0.000 / 0.000 (0.1) | 2 / 95 | 2 + 6 (2 + 6) | 16 781 | 20 956 | PASS |
| orientation-resume | ar 390 | 5 | 1 124 (1 080–1 188) | 1 016 | 0.000 / 0.000 (0.1) | 2 / 98 | 2 + 6 (2 + 6) | 16 781 | 53 184 | PASS |
| pathway-detail | fr 1440 | 5 | 960 (948–1 116) | 880 | 0.002 / 0.010 (0.1) | 5 / 122 | 2 + 6 (1 + 6) ↑ | 16 781 | 20 956 | PASS |
| pathway-detail | ar 1440 | 5 | 1 220 (1 100–1 384) | 1 056 | 0.002 / 0.013 (0.1) | 5 / 217 | 2 + 6 (1 + 6) ↑ | 16 781 | 53 184 | PASS |
| pathway-detail | fr 390 | 5 | 980 (900–1 168) | 860 | 0.000 / 0.000 (0.1) | 3 / 178 | 2 + 6 (1 + 6) ↑ | 16 781 | 20 956 | PASS |
| pathway-detail | ar 390 | 5 | 1 220 (1 196–1 428) | 1 020 | 0.000 / 0.000 (0.1) | 1 / 220 | 2 + 6 (1 + 6) ↑ | 16 781 | 53 184 | PASS |
| diplomas | fr 1440 | 5 | 988 (948–1 160) | 880 | 0.000 / 0.010 (0.1) | 2 / 146 | 2 + 6 (1 + 6) ↑ | 16 781 | 20 956 | PASS |
| diplomas | ar 1440 | 5 | 1 332 (1 160–1 372) | 1 044 | 0.000 / 0.016 (0.1) | 5 / 222 | 2 + 6 (1 + 6) ↑ | 16 781 | 53 184 | PASS |
| diplomas | fr 390 | 5 | 976 (952–1 092) | 852 | 0.000 / 0.000 (0.1) | 2 / 134 | 2 + 6 (1 + 6) ↑ | 16 781 | 20 956 | PASS |
| diplomas | ar 390 | 5 | 1 192 (1 120–1 280) | 1 004 | 0.000 / 0.000 (0.1) | 1 / 172 | 2 + 6 (1 + 6) ↑ | 16 781 | 53 184 | PASS |
| training | fr 1440 | 5 | 1 004 (964–1 016) | 872 | 0.000 / 0.000 (0.1) | 2 / 53 | 2 + 6 (1 + 6) ↑ | 16 781 | 20 956 | PASS |
| training | ar 1440 | 5 | 1 200 (1 176–1 408) | 1 048 | 0.000 / 0.109 (0.1) | 5 / 226 | 2 + 6 (1 + 6) ↑ | 16 781 | 53 184 | PASS |
| training | fr 390 | 5 | 956 (916–992) | 852 | 0.000 / 0.000 (0.1) | 0 / — | 2 + 6 (1 + 6) ↑ | 16 781 | 20 956 | PASS |
| training | ar 390 | 5 | 1 180 (1 088–1 212) | 1 012 | 0.000 / 0.000 (0.1) | 0 / — | 2 + 6 (1 + 6) ↑ | 16 781 | 53 184 | PASS |
| living | fr 1440 | 5 | 1 004 (948–1 068) | 884 | 0.016 / 0.020 (0.1) | 3 / 69 | 2 + 6 (1 + 6) ↑ | 16 781 | 20 956 | PASS |
| living | ar 1440 | 5 | 1 180 (1 152–1 256) | 1 048 | 0.000 / 0.018 (0.1) | 5 / 97 | 2 + 6 (1 + 6) ↑ | 16 781 | 53 184 | PASS |
| living | fr 390 | 5 | 944 (904–976) | 848 | 0.000 / 0.000 (0.1) | 2 / 72 | 2 + 6 (1 + 6) ↑ | 16 781 | 20 956 | PASS |
| living | ar 390 | 5 | 1 152 (1 124–1 248) | 1 040 | 0.000 / 0.000 (0.1) | 2 / 123 | 2 + 6 (1 + 6) ↑ | 16 781 | 53 184 | PASS |
| living-topic | fr 1440 | 5 | 1 036 (940–1 064) | 884 | 0.002 / 0.016 (0.1) | 4 / 80 | 2 + 6 (1 + 6) ↑ | 16 781 | 20 956 | PASS |
| living-topic | ar 1440 | 5 | 1 196 (1 136–1 208) | 1 048 | 0.000 / 0.050 (0.1) | 5 / 82 | 2 + 6 (1 + 6) ↑ | 16 781 | 53 184 | PASS |
| living-topic | fr 390 | 5 | 936 (920–1 072) | 856 | 0.000 / 0.000 (0.1) | 2 / 96 | 2 + 6 (1 + 6) ↑ | 16 781 | 20 956 | PASS |
| living-topic | ar 390 | 5 | 1 088 (1 076–1 192) | 1 016 | 0.000 / 0.000 (0.1) | 1 / 88 | 2 + 6 (1 + 6) ↑ | 16 781 | 53 184 | PASS |
| news | fr 1440 | 5 | 964 (936–1 068) | 876 | 0.000 / 0.049 (0.1) | 1 / 73 | 2 + 6 (1 + 6) ↑ | 16 781 | 20 956 | PASS |
| news | ar 1440 | 5 | 1 164 (1 156–1 232) | 1 056 | 0.000 / 0.000 (0.1) | 5 / 88 | 2 + 6 (1 + 6) ↑ | 16 781 | 53 184 | PASS |
| news | fr 390 | 5 | 904 (876–1 004) | 864 | 0.000 / 0.000 (0.1) | 2 / 61 | 2 + 6 (1 + 6) ↑ | 16 781 | 20 956 | PASS |
| news | ar 390 | 5 | 1 148 (1 100–1 244) | 1 036 | 0.000 / 0.000 (0.1) | 2 / 133 | 2 + 6 (1 + 6) ↑ | 16 781 | 53 184 | PASS |
| faq | fr 1440 | 5 | 964 (956–1 088) | 892 | 0.000 / 0.002 (0.1) | 2 / 94 | 2 + 6 (1 + 6) ↑ | 16 781 | 20 956 | PASS |
| faq | ar 1440 | 5 | 1 260 (1 136–1 348) | 1 048 | 0.009 / 0.009 (0.1) | 5 / 151 | 2 + 6 (1 + 6) ↑ | 16 781 | 53 184 | PASS |
| faq | fr 390 | 5 | 940 (920–1 028) | 856 | 0.000 / 0.000 (0.1) | 3 / 102 | 2 + 6 (1 + 6) ↑ | 16 781 | 20 956 | PASS |
| faq | ar 390 | 5 | 1 112 (1 096–1 336) | 1 032 | 0.000 / 0.000 (0.1) | 2 / 143 | 2 + 6 (1 + 6) ↑ | 16 781 | 53 184 | PASS |
| glossary | fr 1440 | 5 | 1 032 (976–1 124) | 888 | 0.002 / 0.010 (0.1) | 3 / 115 | 2 + 6 (1 + 6) ↑ | 16 781 | 20 956 | PASS |
| glossary | ar 1440 | 5 | 1 272 (1 164–1 408) | 1 048 | 0.002 / 0.016 (0.1) | 5 / 177 | 2 + 6 (1 + 6) ↑ | 16 781 | 53 184 | PASS |
| glossary | fr 390 | 5 | 960 (936–1 080) | 844 | 0.000 / 0.000 (0.1) | 3 / 126 | 2 + 6 (1 + 6) ↑ | 16 781 | 20 956 | PASS |
| glossary | ar 390 | 5 | 1 316 (1 164–2 104) | 1 064 | 0.000 / 0.000 (0.1) | 3 / 164 | 2 + 6 (1 + 6) ↑ | 16 781 | 53 184 | PASS |
| glossary-term | fr 1440 | 5 | 988 (976–1 072) | 892 | 0.010 / 0.086 (0.1) | 4 / 71 | 2 + 6 (1 + 6) ↑ | 16 781 | 20 956 | PASS |
| glossary-term | ar 1440 | 5 | 1 260 (1 124–1 344) | 1 048 | 0.011 / 0.018 (0.1) | 4 / 100 | 2 + 6 (1 + 6) ↑ | 16 781 | 53 184 | PASS |
| glossary-term | fr 390 | 5 | 976 (888–1 308) | 868 | 0.000 / 0.000 (0.1) | 2 / 246 | 2 + 6 (1 + 6) ↑ | 16 781 | 20 956 | PASS |
| glossary-term | ar 390 | 5 | 1 168 (1 116–1 268) | 1 028 | 0.000 / 0.000 (0.1) | 2 / 129 | 2 + 6 (1 + 6) ↑ | 16 781 | 53 184 | PASS |
| partners | fr 1440 | 5 | 1 056 (940–1 100) | 900 | 0.020 / 0.027 (0.1) | 4 / 72 | 2 + 6 (1 + 6) ↑ | 16 781 | 20 956 | PASS |
| partners | ar 1440 | 5 | 1 300 (1 120–1 352) | 1 092 | 0.008 / 0.084 (0.1) | 5 / 99 | 2 + 6 (1 + 6) ↑ | 16 781 | 53 184 | PASS |
| partners | fr 390 | 5 | 996 (880–1 056) | 868 | 0.000 / 0.000 (0.1) | 3 / 79 | 2 + 6 (1 + 6) ↑ | 16 781 | 20 956 | PASS |
| partners | ar 390 | 5 | 1 156 (1 080–1 284) | 1 040 | 0.000 / 0.000 (0.1) | 3 / 113 | 2 + 6 (1 + 6) ↑ | 16 781 | 53 184 | PASS |
| contact | fr 1440 | 5 | 1 096 (980–1 120) | 904 | 0.010 / 0.016 (0.1) | 5 / 88 | 2 + 6 (2 + 6) | 16 781 | 20 956 | PASS |
| contact | ar 1440 | 5 | 1 272 (1 148–1 328) | 1 060 | 0.000 / 0.012 (0.1) | 5 / 127 | 2 + 6 (2 + 6) | 16 781 | 53 184 | PASS |
| contact | fr 390 | 5 | 924 (876–996) | 832 | 0.000 / 0.000 (0.1) | 1 / 92 | 2 + 6 (2 + 6) | 16 781 | 20 956 | PASS |
| contact | ar 390 | 5 | 1 136 (1 104–1 260) | 1 016 | 0.000 / 0.000 (0.1) | 2 / 140 | 2 + 6 (2 + 6) | 16 781 | 53 184 | PASS |
| contact-form | fr 1440 | 5 | 1 068 (960–1 128) | 900 | 0.010 / 0.023 (0.1) | 4 / 108 | 2 + 6 (1 + 6) ↑ | 16 781 | 20 956 | PASS |
| contact-form | ar 1440 | 5 | 1 156 (1 148–1 288) | 1 052 | 0.000 / 0.016 (0.1) | 5 / 123 | 2 + 6 (1 + 6) ↑ | 16 781 | 53 184 | PASS |
| contact-form | fr 390 | 5 | 952 (940–1 052) | 864 | 0.000 / 0.000 (0.1) | 2 / 106 | 2 + 6 (1 + 6) ↑ | 16 781 | 20 956 | PASS |
| contact-form | ar 390 | 5 | 1 224 (1 088–1 260) | 1 040 | 0.000 / 0.000 (0.1) | 3 / 118 | 2 + 6 (1 + 6) ↑ | 16 781 | 53 184 | PASS |
| company-needs | fr 1440 | 5 | 1 028 (920–1 092) | 892 | 0.000 / 0.020 (0.1) | 4 / 101 | 2 + 6 (1 + 6) ↑ | 16 781 | 20 956 | PASS |
| company-needs | ar 1440 | 5 | 1 132 (1 108–1 212) | 1 048 | 0.009 / 0.013 (0.1) | 5 / 103 | 2 + 6 (1 + 6) ↑ | 16 781 | 53 184 | PASS |
| company-needs | fr 390 | 5 | 996 (912–1 096) | 852 | 0.000 / 0.000 (0.1) | 3 / 123 | 2 + 6 (1 + 6) ↑ | 16 781 | 20 956 | PASS |
| company-needs | ar 390 | 5 | 1 184 (1 136–1 344) | 1 032 | 0.000 / 0.000 (0.1) | 3 / 146 | 2 + 6 (1 + 6) ↑ | 16 781 | 53 184 | PASS |
| institution-proposal | fr 1440 | 5 | 1 016 (952–1 084) | 892 | 0.000 / 0.023 (0.1) | 4 / 89 | 2 + 6 (1 + 6) ↑ | 16 781 | 20 956 | PASS |
| institution-proposal | ar 1440 | 5 | 1 156 (1 136–1 320) | 1 044 | 0.000 / 0.016 (0.1) | 4 / 142 | 2 + 6 (1 + 6) ↑ | 16 781 | 53 184 | PASS |
| institution-proposal | fr 390 | 5 | 1 004 (956–1 100) | 872 | 0.000 / 0.000 (0.1) | 3 / 122 | 2 + 6 (1 + 6) ↑ | 16 781 | 20 956 | PASS |
| institution-proposal | ar 390 | 5 | 1 148 (1 092–1 348) | 1 024 | 0.000 / 0.000 (0.1) | 1 / 158 | 2 + 6 (1 + 6) ↑ | 16 781 | 53 184 | PASS |
| enquiry-done | fr 1440 | 5 | 980 (916–1 116) | 884 | 0.016 / 0.059 (0.1) | 3 / 74 | 2 + 6 (1 + 6) ↑ | 16 781 | 20 956 | PASS |
| enquiry-done | ar 1440 | 5 | 1 232 (1 100–1 528) | 1 052 | 0.013 / 0.062 (0.1) | 5 / 120 | 2 + 6 (1 + 6) ↑ | 16 781 | 53 184 | PASS |
| enquiry-done | fr 390 | 5 | 948 (876–1 004) | 864 | 0.000 / 0.000 (0.1) | 2 / 91 | 2 + 6 (1 + 6) ↑ | 16 781 | 20 956 | PASS |
| enquiry-done | ar 390 | 5 | 1 248 (1 092–1 308) | 1 056 | 0.000 / 0.000 (0.1) | 3 / 123 | 2 + 6 (1 + 6) ↑ | 16 781 | 53 184 | PASS |
| forum-register | fr 1440 | 5 | 1 032 (960–1 156) | 884 | 0.010 / 0.016 (0.1) | 3 / 82 | 2 + 6 (2 + 6) | 16 781 | 20 956 | PASS |
| forum-register | ar 1440 | 5 | 1 212 (1 104–1 444) | 1 056 | 0.000 / 0.018 (0.1) | 5 / 103 | 2 + 6 (2 + 6) | 16 781 | 53 184 | PASS |
| forum-register | fr 390 | 5 | 932 (900–1 024) | 848 | 0.000 / 0.000 (0.1) | 2 / 89 | 2 + 6 (2 + 6) | 16 781 | 20 956 | PASS |
| forum-register | ar 390 | 5 | 1 116 (1 108–1 244) | 1 008 | 0.000 / 0.000 (0.1) | 2 / 100 | 2 + 6 (2 + 6) | 16 781 | 53 184 | PASS |
| privacy | fr 1440 | 5 | 1 016 (940–1 120) | 892 | 0.020 / 0.060 (0.1) | 5 / 103 | 2 + 6 (1 + 6) ↑ | 16 781 | 20 956 | PASS |
| privacy | ar 1440 | 5 | 1 216 (1 120–1 284) | 1 052 | 0.009 / 0.086 (0.1) | 5 / 148 | 2 + 6 (1 + 6) ↑ | 16 781 | 53 184 | PASS |
| privacy | fr 390 | 5 | 976 (904–1 088) | 872 | 0.000 / 0.000 (0.1) | 3 / 87 | 2 + 6 (1 + 6) ↑ | 16 781 | 20 956 | PASS |
| privacy | ar 390 | 5 | 1 180 (1 072–1 264) | 1 040 | 0.000 / 0.000 (0.1) | 3 / 109 | 2 + 6 (1 + 6) ↑ | 16 781 | 53 184 | PASS |
| qa-doc-person:dashboard | fr 1440 | 5 | 1 272 (1 180–1 512) | 1 088 | 0.000 / 0.000 (0.05) | 4 / 128 | 4 + 8 (3 + 8) ↑ | 19 168 | 23 644 | PASS |
| qa-doc-person:dashboard | ar 1440 | 5 | 1 284 (1 208–1 444) | 1 104 | 0.000 / 0.000 (0.05) | 1 / 148 | 4 + 8 (3 + 8) ↑ | 19 168 | 55 872 | PASS |
| qa-doc-person:dashboard | fr 390 | 5 | 1 092 (968–1 240) | 984 | 0.000 / 0.000 (0.05) | 4 / 99 | 4 + 8 (3 + 8) ↑ | 19 168 | 23 644 | PASS |
| qa-doc-person:dashboard | ar 390 | 5 | 1 368 (1 164–1 544) | 1 232 | 0.000 / 0.000 (0.05) | 5 / 188 | 4 + 8 (3 + 8) ↑ | 19 168 | 55 872 | PASS |
| qa-doc-person:cases | fr 1440 | 5 | 1 048 (1 012–1 144) | 928 | 0.000 / 0.000 (0.1) | 0 / — | 4 + 8 (3 + 8) ↑ | 19 168 | 23 644 | PASS |
| qa-doc-person:cases | ar 1440 | 5 | 1 260 (1 240–1 328) | 1 116 | 0.000 / 0.000 (0.1) | 0 / — | 4 + 8 (3 + 8) ↑ | 19 168 | 55 872 | PASS |
| qa-doc-person:cases | fr 390 | 5 | 1 080 (1 016–1 088) | 972 | 0.000 / 0.000 (0.1) | 4 / 68 | 4 + 8 (3 + 8) ↑ | 19 168 | 23 644 | PASS |
| qa-doc-person:cases | ar 390 | 5 | 1 236 (1 220–1 292) | 1 128 | 0.000 / 0.000 (0.1) | 4 / 100 | 4 + 8 (3 + 8) ↑ | 19 168 | 55 872 | PASS |
| qa-doc-person:case | fr 1440 | 5 | 1 216 (1 168–1 264) | 984 | 0.000 / 0.000 (0.1) | 3 / 135 | 7 + 8 (3 + 8) ↑ | 20 765 | 23 644 | PASS |
| qa-doc-person:case | ar 1440 | 5 | 1 408 (1 324–1 476) | 1 132 | 0.000 / 0.000 (0.1) | 2 / 219 | 7 + 8 (3 + 8) ↑ | 20 765 | 55 872 | PASS |
| qa-doc-person:case | fr 390 | 5 | 1 108 (1 012–1 224) | 956 | 0.000 / 0.000 (0.1) | 4 / 135 | 7 + 8 (3 + 8) ↑ | 20 765 | 23 644 | PASS |
| qa-doc-person:case | ar 390 | 5 | 1 292 (1 176–1 408) | 1 088 | 0.000 / 0.000 (0.1) | 4 / 91 | 7 + 8 (3 + 8) ↑ | 20 765 | 55 872 | PASS |
| qa-doc-person:documents | fr 1440 | 5 | 1 156 (1 100–1 324) | 1 004 | 0.000 / 0.002 (0.05) | 2 / 137 | 5 + 9 (4 + 8) ↑ | 27 510 | 23 644 | PASS |
| qa-doc-person:documents | ar 1440 | 5 | 1 256 (1 212–1 388) | 1 080 | 0.000 / 0.002 (0.05) | 2 / 179 | 5 + 9 (4 + 8) ↑ | 27 510 | 55 872 | PASS |
| qa-doc-person:documents | fr 390 | 5 | 1 088 (1 080–1 196) | 968 | 0.000 / 0.000 (0.05) | 5 / 121 | 5 + 9 (4 + 8) ↑ | 27 510 | 23 644 | PASS |
| qa-doc-person:documents | ar 390 | 5 | 1 340 (1 248–1 500) | 1 088 | 0.000 / 0.000 (0.05) | 5 / 226 | 5 + 9 (4 + 8) ↑ | 27 510 | 55 872 | PASS |
| qa-doc-person:documents-app | fr 1440 | 5 | 1 112 (1 096–1 232) | 1 076 | 0.002 / 0.002 (0.05) | 0 / — | 5 + 9 (4 + 8) ↑ | 27 510 | 23 644 | PASS |
| qa-doc-person:documents-app | ar 1440 | 5 | 1 304 (1 232–1 332) | 1 116 | 0.000 / 0.002 (0.05) | 2 / 152 | 5 + 9 (4 + 8) ↑ | 27 510 | 55 872 | PASS |
| qa-doc-person:documents-app | fr 390 | 5 | 1 096 (996–1 116) | 996 | 0.000 / 0.000 (0.05) | 5 / 93 | 5 + 9 (4 + 8) ↑ | 27 510 | 23 644 | PASS |
| qa-doc-person:documents-app | ar 390 | 5 | 1 296 (1 256–1 420) | 1 132 | 0.000 / 0.000 (0.05) | 3 / 84 | 5 + 9 (4 + 8) ↑ | 27 510 | 55 872 | PASS |
| qa-doc-person:document-requirement | fr 1440 | 5 | 1 148 (1 076–1 332) | 936 | 0.030 / 0.030 (0.05) | 5 / 101 | 4 + 9 (4 + 8) ↑ | 24 491 | 30 916 | PASS |
| qa-doc-person:document-requirement | ar 1440 | 5 | 1 344 (1 332–1 612) | 1 180 | 0.035 / 0.035 (0.05) | 0 / — | 4 + 9 (4 + 8) ↑ | 24 491 | 63 144 | PASS |
| qa-doc-person:document-requirement | fr 390 | 5 | 1 172 (1 152–1 220) | 984 | 0.023 / 0.023 (0.05) | 5 / 140 | 4 + 9 (4 + 8) ↑ | 24 491 | 30 916 | PASS |
| qa-doc-person:document-requirement | ar 390 | 5 | 1 316 (1 208–1 728) | 1 208 | 0.034 / 0.034 (0.05) | 5 / 315 | 4 + 9 (4 + 8) ↑ | 24 491 | 63 144 | PASS |
| qa-doc-person:document-upload | fr 1440 | 5 | 1 064 (1 048–1 176) | 940 | 0.059 / 0.059 (0.05) | 0 / — | 4 + 9 (4 + 8) ↑ | 24 491 | 20 956 | **FAIL** CLS |
| qa-doc-person:document-upload | ar 1440 | 5 | 1 316 (1 252–1 456) | 1 116 | 0.067 / 0.068 (0.05) | 1 / 53 | 4 + 9 (4 + 8) ↑ | 24 491 | 53 184 | **FAIL** CLS |
| qa-doc-person:document-upload | fr 390 | 5 | 1 068 (996–1 144) | 968 | 0.042 / 0.042 (0.05) | 4 / 69 | 4 + 9 (4 + 8) ↑ | 24 491 | 20 956 | PASS |
| qa-doc-person:document-upload | ar 390 | 5 | 1 316 (1 240–1 460) | 1 192 | 0.071 / 0.071 (0.05) | 3 / 128 | 4 + 9 (4 + 8) ↑ | 24 491 | 53 184 | **FAIL** CLS |
| qa-doc-person:situation | fr 1440 | 5 | 1 080 (1 044–1 268) | 956 | 0.001 / 0.002 (0.05) | 3 / 86 | 4 + 9 (3 + 9) ↑ | 20 537 | 20 956 | PASS |
| qa-doc-person:situation | ar 1440 | 5 | 1 336 (1 200–1 716) | 1 112 | 0.000 / 0.001 (0.05) | 2 / 136 | 4 + 9 (3 + 9) ↑ | 20 537 | 53 184 | PASS |
| qa-doc-person:situation | fr 390 | 5 | 1 048 (992–1 116) | 964 | 0.000 / 0.000 (0.05) | 3 / 79 | 4 + 9 (3 + 9) ↑ | 20 537 | 20 956 | PASS |
| qa-doc-person:situation | ar 390 | 5 | 1 332 (1 216–1 356) | 1 144 | 0.000 / 0.002 (0.05) | 4 / 122 | 4 + 9 (3 + 9) ↑ | 20 537 | 53 184 | PASS |
| qa-doc-person:requests | fr 1440 | 5 | 1 024 (984–1 152) | 932 | 0.000 / 0.001 (0.1) | 0 / — | 4 + 8 (3 + 8) ↑ | 19 168 | 20 956 | PASS |
| qa-doc-person:requests | ar 1440 | 5 | 1 252 (1 200–1 440) | 1 096 | 0.000 / 0.001 (0.1) | 0 / — | 4 + 8 (3 + 8) ↑ | 19 168 | 53 184 | PASS |
| qa-doc-person:requests | fr 390 | 5 | 1 048 (996–1 156) | 976 | 0.000 / 0.000 (0.1) | 1 / 53 | 4 + 8 (3 + 8) ↑ | 19 168 | 20 956 | PASS |
| qa-doc-person:requests | ar 390 | 5 | 1 216 (1 164–1 276) | 1 152 | 0.000 / 0.000 (0.1) | 1 / 65 | 4 + 8 (3 + 8) ↑ | 19 168 | 53 184 | PASS |
| qa-doc-person:journey | fr 1440 | 5 | 1 136 (1 044–1 264) | 944 | 0.000 / 0.000 (0.05) | 5 / 90 | 5 + 8 (3 + 8) ↑ | 19 168 | 20 956 | PASS |
| qa-doc-person:journey | ar 1440 | 5 | 1 356 (1 292–1 364) | 1 112 | 0.000 / 0.000 (0.05) | 2 / 128 | 5 + 8 (3 + 8) ↑ | 19 168 | 53 184 | PASS |
| qa-doc-person:journey | fr 390 | 5 | 1 100 (1 020–1 168) | 976 | 0.000 / 0.000 (0.05) | 3 / 85 | 5 + 8 (3 + 8) ↑ | 19 168 | 20 956 | PASS |
| qa-doc-person:journey | ar 390 | 5 | 1 252 (1 216–1 496) | 1 140 | 0.000 / 0.000 (0.05) | 3 / 121 | 5 + 8 (3 + 8) ↑ | 19 168 | 53 184 | PASS |
| qa-doc-person:deadlines | fr 1440 | 5 | 1 068 (1 028–1 116) | 948 | 0.000 / 0.000 (0.1) | 0 / — | 4 + 8 (3 + 8) ↑ | 19 168 | 20 956 | PASS |
| qa-doc-person:deadlines | ar 1440 | 5 | 1 224 (1 168–1 368) | 1 104 | 0.000 / 0.000 (0.1) | 0 / — | 4 + 8 (3 + 8) ↑ | 19 168 | 53 184 | PASS |
| qa-doc-person:deadlines | fr 390 | 5 | 1 020 (988–1 040) | 956 | 0.000 / 0.000 (0.1) | 0 / — | 4 + 8 (3 + 8) ↑ | 19 168 | 20 956 | PASS |
| qa-doc-person:deadlines | ar 390 | 5 | 1 192 (1 152–1 256) | 1 152 | 0.000 / 0.000 (0.1) | 1 / 51 | 4 + 8 (3 + 8) ↑ | 19 168 | 53 184 | PASS |
| qa-doc-person:messages | fr 1440 | 5 | 1 024 (1 020–1 156) | 944 | 0.000 / 0.000 (0.1) | 0 / — | 4 + 8 (3 + 8) ↑ | 19 168 | 20 956 | PASS |
| qa-doc-person:messages | ar 1440 | 5 | 1 192 (1 184–1 376) | 1 120 | 0.000 / 0.000 (0.1) | 1 / 50 | 4 + 8 (3 + 8) ↑ | 19 168 | 53 184 | PASS |
| qa-doc-person:messages | fr 390 | 5 | 1 052 (1 004–1 100) | 988 | 0.000 / 0.000 (0.1) | 2 / 52 | 4 + 8 (3 + 8) ↑ | 19 168 | 20 956 | PASS |
| qa-doc-person:messages | ar 390 | 5 | 1 212 (1 192–1 300) | 1 140 | 0.000 / 0.000 (0.1) | 1 / 57 | 4 + 8 (3 + 8) ↑ | 19 168 | 53 184 | PASS |
| qa-doc-person:academy | fr 1440 | 5 | 1 076 (996–1 220) | 940 | 0.000 / 0.001 (0.1) | 2 / 55 | 5 + 8 (4 + 8) ↑ | 19 168 | 20 956 | PASS |
| qa-doc-person:academy | ar 1440 | 5 | 1 296 (1 180–1 956) | 1 088 | 0.000 / 0.000 (0.1) | 1 / 115 | 5 + 8 (4 + 8) ↑ | 19 168 | 53 184 | PASS |
| qa-doc-person:academy | fr 390 | 5 | 1 072 (1 008–1 176) | 972 | 0.000 / 0.000 (0.1) | 3 / 85 | 5 + 8 (4 + 8) ↑ | 19 168 | 20 956 | PASS |
| qa-doc-person:academy | ar 390 | 5 | 1 320 (1 192–1 396) | 1 188 | 0.000 / 0.000 (0.1) | 4 / 109 | 5 + 8 (4 + 8) ↑ | 19 168 | 53 184 | PASS |
| qa-doc-person:academy-course | fr 1440 | 5 | 1 132 (1 100–1 224) | 940 | 0.000 / 0.000 (0.1) | 5 / 104 | 5 + 8 (4 + 8) ↑ | 19 168 | 23 644 | PASS |
| qa-doc-person:academy-course | ar 1440 | 5 | 1 332 (1 288–1 480) | 1 100 | 0.000 / 0.001 (0.1) | 2 / 174 | 5 + 8 (4 + 8) ↑ | 19 168 | 55 872 | PASS |
| qa-doc-person:academy-course | fr 390 | 5 | 1 084 (1 032–1 328) | 1 012 | 0.000 / 0.000 (0.1) | 3 / 92 | 5 + 8 (4 + 8) ↑ | 19 168 | 23 644 | PASS |
| qa-doc-person:academy-course | ar 390 | 5 | 1 460 (1 292–1 588) | 1 188 | 0.000 / 0.000 (0.1) | 4 / 226 | 5 + 8 (4 + 8) ↑ | 19 168 | 55 872 | PASS |
| qa-doc-person:profile | fr 1440 | 5 | 1 096 (964–1 260) | 896 | 0.009 / 0.020 (0.1) | 3 / 114 | 2 + 6 (1 + 6) ↑ | 18 378 | 20 956 | PASS |
| qa-doc-person:profile | ar 1440 | 5 | 1 248 (1 168–1 288) | 1 032 | 0.000 / 0.013 (0.1) | 5 / 148 | 2 + 6 (1 + 6) ↑ | 18 378 | 53 184 | PASS |
| qa-doc-person:profile | fr 390 | 5 | 968 (932–1 004) | 836 | 0.000 / 0.000 (0.1) | 2 / 104 | 2 + 6 (1 + 6) ↑ | 18 378 | 20 956 | PASS |
| qa-doc-person:profile | ar 390 | 5 | 1 172 (1 092–1 320) | 1 012 | 0.000 / 0.000 (0.1) | 1 / 136 | 2 + 6 (1 + 6) ↑ | 18 378 | 53 184 | PASS |
| qa-doc-person:account-email | fr 1440 | 5 | 1 056 (984–1 140) | 896 | 0.004 / 0.023 (0.1) | 4 / 88 | 2 + 8 (1 + 8) ↑ | 18 932 | 20 956 | PASS |
| qa-doc-person:account-email | ar 1440 | 5 | 1 212 (1 120–1 284) | 1 052 | 0.009 / 0.016 (0.1) | 5 / 94 | 2 + 8 (1 + 8) ↑ | 18 932 | 53 184 | PASS |
| qa-doc-person:account-email | fr 390 | 5 | 988 (892–1 080) | 860 | 0.000 / 0.000 (0.1) | 2 / 84 | 2 + 8 (1 + 8) ↑ | 18 932 | 20 956 | PASS |
| qa-doc-person:account-email | ar 390 | 5 | 1 100 (1 080–1 220) | 1 024 | 0.000 / 0.000 (0.1) | 2 / 108 | 2 + 8 (1 + 8) ↑ | 18 932 | 53 184 | PASS |
| qa-doc-person:account-password | fr 1440 | 5 | 948 (924–1 040) | 876 | 0.000 / 0.010 (0.1) | 2 / 67 | 2 + 6 (1 + 6) ↑ | 18 378 | 20 956 | PASS |
| qa-doc-person:account-password | ar 1440 | 5 | 1 220 (1 152–1 552) | 1 024 | 0.005 / 0.018 (0.1) | 5 / 132 | 2 + 6 (1 + 6) ↑ | 18 378 | 53 184 | PASS |
| qa-doc-person:account-password | fr 390 | 5 | 976 (896–1 032) | 844 | 0.000 / 0.000 (0.1) | 3 / 113 | 2 + 6 (1 + 6) ↑ | 18 378 | 20 956 | PASS |
| qa-doc-person:account-password | ar 390 | 5 | 1 168 (1 092–1 432) | 1 004 | 0.000 / 0.000 (0.1) | 2 / 124 | 2 + 6 (1 + 6) ↑ | 18 378 | 53 184 | PASS |
| qa-doc-person:account-mfa | fr 1440 | 5 | 988 (924–1 184) | 872 | 0.000 / 0.020 (0.1) | 4 / 76 | 2 + 6 (1 + 6) ↑ | 18 378 | 20 956 | PASS |
| qa-doc-person:account-mfa | ar 1440 | 5 | 1 120 (1 120–1 384) | 1 024 | 0.000 / 0.016 (0.1) | 5 / 103 | 2 + 6 (1 + 6) ↑ | 18 378 | 53 184 | PASS |
| qa-doc-person:account-mfa | fr 390 | 5 | 972 (908–1 076) | 840 | 0.000 / 0.000 (0.1) | 2 / 76 | 2 + 6 (1 + 6) ↑ | 18 378 | 20 956 | PASS |
| qa-doc-person:account-mfa | ar 390 | 5 | 1 112 (1 084–1 352) | 988 | 0.000 / 0.000 (0.1) | 3 / 85 | 2 + 6 (1 + 6) ↑ | 18 378 | 53 184 | PASS |
| qa-doc-person:account-delete | fr 1440 | 5 | 1 004 (936–1 172) | 868 | 0.000 / 0.020 (0.1) | 3 / 75 | 2 + 6 (1 + 6) ↑ | 18 378 | 20 956 | PASS |
| qa-doc-person:account-delete | ar 1440 | 5 | 1 244 (1 132–1 484) | 1 040 | 0.000 / 0.018 (0.1) | 5 / 124 | 2 + 6 (1 + 6) ↑ | 18 378 | 53 184 | PASS |
| qa-doc-person:account-delete | fr 390 | 5 | 952 (916–1 140) | 844 | 0.000 / 0.000 (0.1) | 1 / 78 | 2 + 6 (1 + 6) ↑ | 18 378 | 20 956 | PASS |
| qa-doc-person:account-delete | ar 390 | 5 | 1 172 (1 048–1 296) | 1 000 | 0.000 / 0.000 (0.1) | 3 / 98 | 2 + 6 (1 + 6) ↑ | 18 378 | 53 184 | PASS |
| qa-doc-person:logout | fr 1440 | 5 | 1 036 (944–1 204) | 876 | 0.010 / 0.034 (0.1) | 4 / 67 | 2 + 6 (1 + 6) ↑ | 18 378 | 20 956 | PASS |
| qa-doc-person:logout | ar 1440 | 5 | 1 232 (1 108–1 288) | 1 044 | 0.009 / 0.016 (0.1) | 5 / 105 | 2 + 6 (1 + 6) ↑ | 18 378 | 53 184 | PASS |
| qa-doc-person:logout | fr 390 | 5 | 912 (880–1 112) | 832 | 0.000 / 0.000 (0.1) | 1 / 76 | 2 + 6 (1 + 6) ↑ | 18 378 | 20 956 | PASS |
| qa-doc-person:logout | ar 390 | 5 | 1 224 (1 072–1 940) | 1 024 | 0.000 / 0.000 (0.1) | 2 / 116 | 2 + 6 (1 + 6) ↑ | 18 378 | 53 184 | PASS |
| qa-person:dashboard | fr 1440 | 5 | 1 140 (1 096–1 344) | 960 | 0.000 / 0.000 (0.05) | 3 / 106 | 4 + 8 (3 + 8) ↑ | 19 168 | 30 916 | PASS |
| qa-person:dashboard | ar 1440 | 5 | 1 324 (1 276–1 576) | 1 120 | 0.000 / 0.000 (0.05) | 1 / 88 | 4 + 8 (3 + 8) ↑ | 19 168 | 63 144 | PASS |
| qa-person:dashboard | fr 390 | 5 | 1 152 (1 008–1 200) | 1 008 | 0.000 / 0.000 (0.05) | 5 / 135 | 4 + 8 (3 + 8) ↑ | 19 168 | 30 916 | PASS |
| qa-person:dashboard | ar 390 | 5 | 1 296 (1 244–1 484) | 1 152 | 0.000 / 0.000 (0.05) | 5 / 174 | 4 + 8 (3 + 8) ↑ | 19 168 | 63 144 | PASS |
| qa-person:document-upload | fr 1440 | 5 | 1 012 (988–1 128) | 944 | 0.000 / 0.000 (0.05) | 0 / — | 4 + 8 (4 + 8) | 19 168 | 20 956 | PASS |
| qa-person:document-upload | ar 1440 | 5 | 1 256 (1 200–1 340) | 1 124 | 0.000 / 0.001 (0.05) | 0 / — | 4 + 8 (4 + 8) | 19 168 | 53 184 | PASS |
| qa-person:document-upload | fr 390 | 5 | 1 036 (972–1 140) | 972 | 0.000 / 0.000 (0.05) | 1 / 51 | 4 + 8 (4 + 8) | 19 168 | 20 956 | PASS |
| qa-person:document-upload | ar 390 | 5 | 1 176 (1 148–1 244) | 1 124 | 0.000 / 0.000 (0.05) | 0 / — | 4 + 8 (4 + 8) | 19 168 | 53 184 | PASS |
| qa-person:request-detail | fr 1440 | 5 | 1 076 (1 004–1 176) | 932 | 0.000 / 0.001 (0.1) | 3 / 87 | 4 + 8 (3 + 8) ↑ | 19 168 | 30 916 | PASS |
| qa-person:request-detail | ar 1440 | 5 | 1 272 (1 248–1 348) | 1 104 | 0.000 / 0.000 (0.1) | 0 / — | 4 + 8 (3 + 8) ↑ | 19 168 | 63 144 | PASS |
| qa-person:request-detail | fr 390 | 5 | 1 068 (992–1 168) | 980 | 0.000 / 0.000 (0.1) | 2 / 78 | 4 + 8 (3 + 8) ↑ | 19 168 | 30 916 | PASS |
| qa-person:request-detail | ar 390 | 5 | 1 244 (1 208–1 316) | 1 128 | 0.000 / 0.000 (0.1) | 3 / 88 | 4 + 8 (3 + 8) ↑ | 19 168 | 63 144 | PASS |
| qa-person:journey | fr 1440 | 5 | 1 168 (1 132–1 316) | 936 | 0.000 / 0.000 (0.05) | 4 / 97 | 5 + 8 (3 + 8) ↑ | 19 168 | 23 644 | PASS |
| qa-person:journey | ar 1440 | 5 | 1 284 (1 280–1 428) | 1 100 | 0.000 / 0.000 (0.05) | 0 / — | 5 + 8 (3 + 8) ↑ | 19 168 | 55 872 | PASS |
| qa-person:journey | fr 390 | 5 | 1 100 (1 060–1 180) | 972 | 0.000 / 0.000 (0.05) | 5 / 102 | 5 + 8 (3 + 8) ↑ | 19 168 | 23 644 | PASS |
| qa-person:journey | ar 390 | 5 | 1 276 (1 160–1 316) | 1 140 | 0.000 / 0.000 (0.05) | 4 / 149 | 5 + 8 (3 + 8) ↑ | 19 168 | 55 872 | PASS |
| qa-person:helpdesk | fr 1440 | 5 | 1 068 (1 060–1 140) | 924 | 0.000 / 0.000 (0.1) | 5 / 124 | 5 + 8 (4 + 8) ↑ | 19 168 | 30 916 | PASS |
| qa-person:helpdesk | ar 1440 | 5 | 1 276 (1 256–1 300) | 1 112 | 0.000 / 0.001 (0.1) | 1 / 148 | 5 + 8 (4 + 8) ↑ | 19 168 | 63 144 | PASS |
| qa-person:helpdesk | fr 390 | 5 | 1 072 (1 016–1 164) | 972 | 0.000 / 0.000 (0.1) | 3 / 102 | 5 + 8 (4 + 8) ↑ | 19 168 | 30 916 | PASS |
| qa-person:helpdesk | ar 390 | 5 | 1 216 (1 184–1 500) | 1 184 | 0.000 / 0.000 (0.1) | 3 / 190 | 5 + 8 (4 + 8) ↑ | 19 168 | 63 144 | PASS |
| qa-person:helpdesk-detail | fr 1440 | 5 | 1 056 (1 044–1 788) | 984 | 0.000 / 0.000 (0.1) | 3 / 120 | 6 + 8 (4 + 8) ↑ | 20 765 | 23 644 | PASS |
| qa-person:helpdesk-detail | ar 1440 | 5 | 1 284 (1 248–1 668) | 1 048 | 0.000 / 0.000 (0.1) | 4 / 258 | 6 + 8 (4 + 8) ↑ | 20 765 | 55 872 | PASS |
| qa-person:helpdesk-detail | fr 390 | 5 | 1 084 (1 052–1 588) | 936 | 0.000 / 0.000 (0.1) | 5 / 111 | 6 + 8 (4 + 8) ↑ | 20 765 | 23 644 | PASS |
| qa-person:helpdesk-detail | ar 390 | 5 | 1 264 (1 156–1 368) | 1 144 | 0.000 / 0.000 (0.1) | 5 / 126 | 6 + 8 (4 + 8) ↑ | 20 765 | 55 872 | PASS |
| qa-person:helpdesk-new | fr 1440 | 5 | 1 056 (992–1 236) | 936 | 0.000 / 0.000 (0.1) | 1 / 61 | 5 + 8 (4 + 8) ↑ | 19 168 | 20 956 | PASS |
| qa-person:helpdesk-new | ar 1440 | 5 | 1 240 (1 212–1 292) | 1 072 | 0.000 / 0.000 (0.1) | 2 / 122 | 5 + 8 (4 + 8) ↑ | 19 168 | 53 184 | PASS |
| qa-person:helpdesk-new | fr 390 | 5 | 1 020 (1 004–1 128) | 964 | 0.000 / 0.000 (0.1) | 3 / 68 | 5 + 8 (4 + 8) ↑ | 19 168 | 20 956 | PASS |
| qa-person:helpdesk-new | ar 390 | 5 | 1 188 (1 172–1 372) | 1 172 | 0.000 / 0.000 (0.1) | 1 / 61 | 5 + 8 (4 + 8) ↑ | 19 168 | 53 184 | PASS |
| qa-person:academy-mine | fr 1440 | 5 | 1 148 (1 020–1 196) | 944 | 0.000 / 0.001 (0.1) | 1 / 79 | 5 + 8 (4 + 8) ↑ | 19 168 | 30 916 | PASS |
| qa-person:academy-mine | ar 1440 | 5 | 1 272 (1 204–1 484) | 1 100 | 0.000 / 0.001 (0.1) | 1 / 167 | 5 + 8 (4 + 8) ↑ | 19 168 | 63 144 | PASS |
| qa-person:academy-mine | fr 390 | 5 | 1 052 (1 044–1 120) | 944 | 0.000 / 0.000 (0.1) | 3 / 105 | 5 + 8 (4 + 8) ↑ | 19 168 | 30 916 | PASS |
| qa-person:academy-mine | ar 390 | 5 | 1 256 (1 228–1 652) | 1 120 | 0.000 / 0.000 (0.1) | 5 / 187 | 5 + 8 (4 + 8) ↑ | 19 168 | 63 144 | PASS |
| qa-person:academy-enrolment | fr 1440 | 5 | 1 108 (1 032–1 284) | 940 | 0.000 / 0.000 (0.1) | 3 / 85 | 5 + 8 (4 + 8) ↑ | 19 168 | 23 644 | PASS |
| qa-person:academy-enrolment | ar 1440 | 5 | 1 272 (1 252–1 484) | 1 092 | 0.000 / 0.000 (0.1) | 2 / 153 | 5 + 8 (4 + 8) ↑ | 19 168 | 55 872 | PASS |
| qa-person:academy-enrolment | fr 390 | 5 | 1 132 (1 072–1 380) | 968 | 0.000 / 0.000 (0.1) | 5 / 104 | 5 + 8 (4 + 8) ↑ | 19 168 | 23 644 | PASS |
| qa-person:academy-enrolment | ar 390 | 5 | 1 280 (1 160–1 380) | 1 160 | 0.000 / 0.000 (0.1) | 3 / 122 | 5 + 8 (4 + 8) ↑ | 19 168 | 55 872 | PASS |
| qa-fresh-person:dashboard | fr 1440 | 5 | 1 072 (1 036–1 300) | 928 | 0.001 / 0.001 (0.05) | 0 / — | 3 + 8 (3 + 8) | 19 168 | 20 956 | PASS |
| qa-fresh-person:dashboard | ar 1440 | 5 | 1 196 (1 144–1 292) | 1 088 | 0.000 / 0.001 (0.05) | 2 / 86 | 3 + 8 (3 + 8) | 19 168 | 53 184 | PASS |
| qa-fresh-person:dashboard | fr 390 | 5 | 992 (952–1 064) | 940 | 0.000 / 0.000 (0.05) | 2 / 63 | 3 + 8 (3 + 8) | 19 168 | 20 956 | PASS |
| qa-fresh-person:dashboard | ar 390 | 5 | 1 184 (1 156–1 272) | 1 092 | 0.000 / 0.000 (0.05) | 1 / 101 | 3 + 8 (3 + 8) | 19 168 | 53 184 | PASS |
| qa-company:company | fr 1440 | 5 | 1 084 (1 004–1 228) | 904 | 0.000 / 0.001 (0.05) | 2 / 122 | 3 + 8 (4 + 8) | 19 168 | 23 644 | PASS |
| qa-company:company | ar 1440 | 5 | 1 268 (1 216–1 888) | 1 104 | 0.000 / 0.000 (0.05) | 0 / — | 3 + 8 (4 + 8) | 19 168 | 55 872 | PASS |
| qa-company:company | fr 390 | 5 | 1 020 (972–1 884) | 1 008 | 0.000 / 0.000 (0.05) | 2 / 127 | 3 + 8 (4 + 8) | 19 168 | 23 644 | PASS |
| qa-company:company | ar 390 | 5 | 1 284 (1 152–1 328) | 1 136 | 0.000 / 0.000 (0.05) | 3 / 112 | 3 + 8 (4 + 8) | 19 168 | 55 872 | PASS |
| qa-company:company-profile | fr 1440 | 5 | 1 076 (1 032–1 316) | 952 | 0.000 / 0.001 (0.1) | 2 / 135 | 4 + 8 (4 + 8) | 19 168 | 23 644 | PASS |
| qa-company:company-profile | ar 1440 | 5 | 1 240 (1 224–1 456) | 1 100 | 0.000 / 0.001 (0.1) | 1 / 155 | 4 + 8 (4 + 8) | 19 168 | 55 872 | PASS |
| qa-company:company-profile | fr 390 | 5 | 1 068 (996–1 212) | 996 | 0.000 / 0.000 (0.1) | 3 / 94 | 4 + 8 (4 + 8) | 19 168 | 23 644 | PASS |
| qa-company:company-profile | ar 390 | 5 | 1 228 (1 184–1 376) | 1 184 | 0.000 / 0.000 (0.1) | 2 / 88 | 4 + 8 (4 + 8) | 19 168 | 55 872 | PASS |
| qa-company:company-needs-list | fr 1440 | 5 | 1 024 (972–1 104) | 916 | 0.000 / 0.000 (0.1) | 1 / 62 | 4 + 8 (4 + 8) | 19 168 | 30 916 | PASS |
| qa-company:company-needs-list | ar 1440 | 5 | 1 260 (1 228–1 520) | 1 100 | 0.000 / 0.000 (0.1) | 1 / 170 | 4 + 8 (4 + 8) | 19 168 | 63 144 | PASS |
| qa-company:company-needs-list | fr 390 | 5 | 1 012 (964–1 236) | 1 012 | 0.000 / 0.000 (0.1) | 2 / 79 | 4 + 8 (4 + 8) | 19 168 | 30 916 | PASS |
| qa-company:company-needs-list | ar 390 | 5 | 1 260 (1 160–1 376) | 1 160 | 0.000 / 0.000 (0.1) | 4 / 71 | 4 + 8 (4 + 8) | 19 168 | 63 144 | PASS |
| qa-company:company-need-form | fr 1440 | 5 | 1 024 (976–1 088) | 920 | 0.000 / 0.000 (0.1) | 2 / 76 | 4 + 8 (4 + 8) | 19 168 | 20 956 | PASS |
| qa-company:company-need-form | ar 1440 | 5 | 1 316 (1 228–1 352) | 1 096 | 0.000 / 0.000 (0.1) | 2 / 132 | 4 + 8 (4 + 8) | 19 168 | 53 184 | PASS |
| qa-company:company-need-form | fr 390 | 5 | 1 028 (984–1 064) | 1 016 | 0.000 / 0.000 (0.1) | 3 / 84 | 4 + 8 (4 + 8) | 19 168 | 20 956 | PASS |
| qa-company:company-need-form | ar 390 | 5 | 1 252 (1 164–1 328) | 1 144 | 0.000 / 0.000 (0.1) | 2 / 143 | 4 + 8 (4 + 8) | 19 168 | 53 184 | PASS |
| qa-company:company-analysis | fr 1440 | 5 | 1 144 (1 092–1 164) | 1 020 | 0.000 / 0.016 (0.1) | 2 / 63 | 2 + 6 (1 + 6) ↑ | 18 378 | 20 956 | PASS |
| qa-company:company-analysis | ar 1440 | 5 | 1 272 (1 152–1 360) | 1 132 | 0.000 / 0.009 (0.1) | 5 / 106 | 2 + 6 (1 + 6) ↑ | 18 378 | 53 184 | PASS |
| qa-company:company-analysis | fr 390 | 5 | 1 088 (1 060–1 184) | 988 | 0.000 / 0.000 (0.1) | 1 / 57 | 2 + 6 (1 + 6) ↑ | 18 378 | 20 956 | PASS |
| qa-company:company-analysis | ar 390 | 5 | 1 248 (1 200–1 340) | 1 108 | 0.000 / 0.000 (0.1) | 1 / 117 | 2 + 6 (1 + 6) ↑ | 18 378 | 53 184 | PASS |
| error-404 | fr 1440 | 5 | 1 120 (1 088–1 240) | 1 036 | 0.000 / 0.016 (0.1) | 1 / 66 | 2 + 6 (1 + 6) ↑ | 16 781 | 20 956 | PASS |
| error-404 | ar 1440 | 5 | 1 288 (1 240–1 560) | 1 140 | 0.000 / 0.018 (0.1) | 5 / 112 | 2 + 6 (1 + 6) ↑ | 16 781 | 53 184 | PASS |
| error-404 | fr 390 | 5 | 1 076 (1 060–1 132) | 988 | 0.000 / 0.000 (0.1) | 0 / — | 2 + 6 (1 + 6) ↑ | 16 781 | 20 956 | PASS |
| error-404 | ar 390 | 5 | 1 232 (1 196–1 264) | 1 100 | 0.000 / 0.000 (0.1) | 1 / 92 | 2 + 6 (1 + 6) ↑ | 16 781 | 53 184 | PASS |
| error-410 | fr 1440 | 5 | 1 112 (1 104–1 236) | 1 028 | 0.000 / 0.020 (0.1) | 1 / 51 | 2 + 6 (1 + 6) ↑ | 16 781 | 20 956 | PASS |
| error-410 | ar 1440 | 5 | 1 248 (1 244–1 280) | 1 128 | 0.000 / 0.013 (0.1) | 4 / 70 | 2 + 6 (1 + 6) ↑ | 16 781 | 53 184 | PASS |
| error-410 | fr 390 | 5 | 1 084 (1 068–1 192) | 1 012 | 0.000 / 0.000 (0.1) | 1 / 85 | 2 + 6 (1 + 6) ↑ | 16 781 | 20 956 | PASS |
| error-410 | ar 390 | 5 | 1 260 (1 192–1 500) | 1 124 | 0.000 / 0.000 (0.1) | 1 / 87 | 2 + 6 (1 + 6) ↑ | 16 781 | 53 184 | PASS |
| seed-company:org-bridge | fr 1440 | 5 | 1 004 (968–1 280) | 928 | 0.000 / 0.000 (0.05) | 1 / 52 | 3 + 8 (3 + 8) | 19 168 | 20 956 | PASS |
| seed-company:org-bridge | ar 1440 | 5 | 1 196 (1 136–1 320) | 1 084 | 0.000 / 0.001 (0.05) | 1 / 61 | 3 + 8 (3 + 8) | 19 168 | 53 184 | PASS |
| seed-company:org-bridge | fr 390 | 5 | 960 (928–1 124) | 960 | 0.000 / 0.000 (0.05) | 0 / — | 3 + 8 (3 + 8) | 19 168 | 20 956 | PASS |
| seed-company:org-bridge | ar 390 | 5 | 1 188 (1 112–1 384) | 1 112 | 0.000 / 0.000 (0.05) | 2 / 140 | 3 + 8 (3 + 8) | 19 168 | 53 184 | PASS |
| helpdesk-queue | fr 1440 | 5 | 1 068 (968–1 936) | 924 | 0.000 / 0.000 (0.1) | 3 / 70 | 5 + 8 (4 + 8) ↑ | 19 168 | 30 916 | PASS |
| helpdesk-queue | ar 1440 | 5 | 1 240 (1 204–1 428) | 1 096 | 0.000 / 0.001 (0.1) | 1 / 135 | 5 + 8 (4 + 8) ↑ | 19 168 | 63 144 | PASS |
| helpdesk-queue | fr 390 | 5 | 1 036 (988–1 196) | 988 | 0.000 / 0.000 (0.1) | 3 / 71 | 5 + 8 (4 + 8) ↑ | 19 168 | 30 916 | PASS |
| helpdesk-queue | ar 390 | 5 | 1 228 (1 168–1 320) | 1 116 | 0.000 / 0.000 (0.1) | 2 / 83 | 5 + 8 (4 + 8) ↑ | 19 168 | 63 144 | PASS |
| console-unavailable | fr 1440 | 5 | 1 140 (1 076–1 344) | 1 032 | 0.000 / 0.020 (0.1) | 2 / 73 | 2 + 6 (1 + 6) ↑ | 18 378 | 20 956 | PASS |
| console-unavailable | ar 1440 | 5 | 1 236 (1 148–1 368) | 1 124 | 0.000 / 0.013 (0.1) | 5 / 93 | 2 + 6 (1 + 6) ↑ | 18 378 | 53 184 | PASS |
| console-unavailable | fr 390 | 5 | 1 104 (1 084–1 188) | 996 | 0.000 / 0.000 (0.1) | 2 / 84 | 2 + 6 (1 + 6) ↑ | 18 378 | 20 956 | PASS |
| console-unavailable | ar 390 | 5 | 1 228 (1 204–1 364) | 1 108 | 0.000 / 0.000 (0.1) | 0 / — | 2 + 6 (1 + 6) ↑ | 18 378 | 53 184 | PASS |
| helpdesk-dispatch | fr 1440 | 5 | 1 040 (1 020–1 200) | 928 | 0.000 / 0.004 (0.1) | 2 / 74 | 5 + 8 (4 + 8) ↑ | 19 168 | 23 644 | PASS |
| helpdesk-dispatch | ar 1440 | 5 | 1 232 (1 204–1 268) | 1 088 | 0.000 / 0.001 (0.1) | 0 / — | 5 + 8 (4 + 8) ↑ | 19 168 | 55 872 | PASS |
| helpdesk-dispatch | fr 390 | 5 | 1 024 (1 008–1 056) | 1 008 | 0.000 / 0.000 (0.1) | 1 / 73 | 5 + 8 (4 + 8) ↑ | 19 168 | 23 644 | PASS |
| helpdesk-dispatch | ar 390 | 5 | 1 212 (1 180–1 292) | 1 104 | 0.000 / 0.000 (0.1) | 4 / 104 | 5 + 8 (4 + 8) ↑ | 19 168 | 55 872 | PASS |
| selection-workspace | fr 1440 | 5 | 1 020 (992–1 056) | 920 | 0.000 / 0.001 (0.1) | 0 / — | 5 + 8 (4 + 8) ↑ | 19 168 | 20 956 | PASS |
| selection-workspace | ar 1440 | 5 | 1 220 (1 188–1 408) | 1 104 | 0.000 / 0.000 (0.1) | 1 / 62 | 5 + 8 (4 + 8) ↑ | 19 168 | 53 184 | PASS |
| selection-workspace | fr 390 | 5 | 992 (948–1 052) | 956 | 0.000 / 0.000 (0.1) | 0 / — | 5 + 8 (4 + 8) ↑ | 19 168 | 20 956 | PASS |
| selection-workspace | ar 390 | 5 | 1 156 (1 140–1 244) | 1 140 | 0.000 / 0.000 (0.1) | 1 / 50 | 5 + 8 (4 + 8) ↑ | 19 168 | 53 184 | PASS |
| operator-dashboard | fr 1440 | 5 | 1 024 (1 000–1 116) | 912 | 0.000 / 0.001 (0.1) | 1 / 52 | 3 + 8 (—) | 19 168 | 20 956 | PASS |
| operator-dashboard | ar 1440 | 5 | 1 184 (1 140–1 448) | 1 096 | 0.000 / 0.001 (0.1) | 2 / 81 | 3 + 8 (—) | 19 168 | 53 184 | PASS |
| operator-dashboard | fr 390 | 5 | 1 008 (964–1 052) | 944 | 0.000 / 0.000 (0.1) | 3 / 70 | 3 + 8 (—) | 19 168 | 20 956 | PASS |
| operator-dashboard | ar 390 | 5 | 1 184 (1 124–1 216) | 1 116 | 0.000 / 0.000 (0.1) | 1 / 88 | 3 + 8 (—) | 19 168 | 53 184 | PASS |

### INP — the overlays' cold open

| Overlay · page · cell | n | open median / p90 / max ms | close median / p90 ms | > 200 ms | state checked |
|---|---|---|---|---|---|
| console drawer · Mes documents · ar · 390 | 11 | 96 / 112 / 136 | 72 / 88 | 0 | open and closed, every load |
| console drawer · Mes documents · ar · 412@1.75 (W2-A's cell) | 11 | 104 / 112 / 128 | 72 / 96 | 0 | open and closed, every load |
| account popover · Mes documents · ar · 390 | 11 | 48 / 64 / 64 | 32 / 40 | 0 | open and closed, every load |
| public sheet · home · ar · 390 | 11 | 104 / 120 / 128 | 56 / 64 | 0 | open and closed, every load |
| door panel · home · ar · 1440 | 11 | 96 / 112 / 120 | 48 / 56 | 0 | open and closed, every load |
| piece drawer · Mes documents · fr · 1440 | 11 | 80 / 88 / 112 | 56 / 72 | 0 | open and closed, every load |
| state dialog · case file · fr · 1440 | 11 | 88 / 96 / 96 | 40 / 56 | 0 | open and closed, every load |

### HTTP/1.1 and HTTP/2, the same loads back to back

| Cell | n (h1 / h2) | LCP ms h1 → h2 (medians) | FCP ms h1 → h2 | `load` ms h1 → h2 | CSS + JS before load |
|---|---|---|---|---|---|
| home · fr · 1440 | 3 / 3 | 1 412 → 1 308 | 1 112 → 1 108 | 1 758 → 1 752 | 3 + 7 |
| home · ar · 1440 | 3 / 3 | 1 608 → 1 612 | 1 240 → 1 292 | 2 065 → 2 016 | 3 + 7 |
| home · fr · 390 | 3 / 3 | 1 204 → 1 220 | 1 076 → 1 088 | 1 704 → 1 671 | 3 + 7 |
| home · ar · 390 | 3 / 3 | 1 408 → 1 568 | 1 208 → 1 240 | 1 866 → 1 888 | 3 + 7 |
| login · fr · 1440 | 3 / 3 | 1 268 → 1 248 | 1 052 → 1 040 | 1 495 → 1 505 | 2 + 7 |
| login · ar · 1440 | 3 / 3 | 1 436 → 1 484 | 1 224 → 1 232 | 1 666 → 1 694 | 2 + 7 |
| login · fr · 390 | 3 / 3 | 1 160 → 1 172 | 1 024 → 1 032 | 1 406 → 1 447 | 2 + 7 |
| login · ar · 390 | 3 / 3 | 1 356 → 1 424 | 1 192 → 1 196 | 1 615 → 1 647 | 2 + 7 |
| pathways · fr · 1440 | 3 / 3 | 944 → 1 008 | 892 → 868 | 1 360 → 1 301 | 2 + 6 |
| pathways · ar · 1440 | 3 / 3 | 1 240 → 1 188 | 1 032 → 1 036 | 1 535 → 1 525 | 2 + 6 |
| pathways · fr · 390 | 3 / 3 | 944 → 988 | 832 → 832 | 1 272 → 1 229 | 2 + 6 |
| pathways · ar · 390 | 3 / 3 | 1 272 → 1 204 | 1 012 → 992 | 1 495 → 1 494 | 2 + 6 |
| qa-doc-person:dashboard · fr · 1440 | 3 / 3 | 1 140 → 1 184 | 920 → 896 | 1 397 → 1 450 | 4 + 8 |
| qa-doc-person:dashboard · ar · 1440 | 3 / 3 | 1 324 → 1 300 | 1 128 → 1 076 | 1 643 → 1 647 | 4 + 8 |
| qa-doc-person:dashboard · fr · 390 | 3 / 3 | 1 064 → 1 048 | 984 → 924 | 1 364 → 1 353 | 4 + 8 |
| qa-doc-person:dashboard · ar · 390 | 3 / 3 | 1 256 → 1 228 | 1 124 → 1 088 | 1 634 → 1 601 | 4 + 8 |
| qa-doc-person:case · fr · 1440 | 3 / 3 | 1 208 → 1 148 | 1 008 → 932 | 1 394 → 1 407 | 7 + 8 |
| qa-doc-person:case · ar · 1440 | 3 / 3 | 1 364 → 1 432 | 1 064 → 1 228 | 1 602 → 1 657 | 7 + 8 |
| qa-doc-person:case · fr · 390 | 3 / 3 | 1 124 → 1 100 | 928 → 976 | 1 384 → 1 452 | 7 + 8 |
| qa-doc-person:case · ar · 390 | 3 / 3 | 1 320 → 1 344 | 1 100 → 1 136 | 1 609 → 1 736 | 7 + 8 |
| qa-doc-person:documents · fr · 1440 | 3 / 3 | 1 164 → 1 100 | 1 076 → 904 | 1 461 → 1 439 | 5 + 9 |
| qa-doc-person:documents · ar · 1440 | 3 / 3 | 1 276 → 1 320 | 1 108 → 1 204 | 1 650 → 1 791 | 5 + 9 |
| qa-doc-person:documents · fr · 390 | 3 / 3 | 1 072 → 1 056 | 964 → 940 | 1 428 → 1 397 | 5 + 9 |
| qa-doc-person:documents · ar · 390 | 3 / 3 | 1 400 → 1 424 | 1 248 → 1 120 | 1 639 → 1 684 | 5 + 9 |

LCP difference HTTP/2 − HTTP/1.1, median over the cells: **8 ms** (min -104, max 160).

### What the long tasks after the first paint are made of (traced, W1-0's analysis)

- **the first render** (13 tasks): layout 51%, style 40%, other 3%, paint 2%, prepaint 1%, commit 1%
- **after the first paint** (105 tasks): layout 54%, style 32%, paint 6%, script 2%, prepaint 2%, other 1%
- **before the first paint** (39 tasks): other 65%, layout 18%, style 8%, task-self 7%, paint 1%, prepaint 0%

  - home · fr · 1440: 1001.8 ms +76.5 ms (the first render: layout 42, style 29, other 2); 1104.2 ms +82.3 ms (after the first paint: layout 49, style 32, other 1); 1262.5 ms +70.5 ms (after the first paint: style 40, layout 15, paint 7); 1358.6 ms +101.3 ms (after the first paint: layout 47, style 37, paint 8)
  - home · ar · 1440: 1148.7 ms +92.6 ms (the first render: layout 51, style 33, other 3); 1312.6 ms +91.2 ms (after the first paint: layout 49, style 25, paint 10); 1544.3 ms +139.8 ms (after the first paint: style 64, layout 56, paint 11); 1698.8 ms +137.2 ms (after the first paint: layout 89, style 32, paint 8)
  - home · fr · 390: 1102.1 ms +61.4 ms (after the first paint: layout 46, style 15, other 0); 1202.1 ms +102.2 ms (after the first paint: layout 55, style 32, paint 8); 1339.1 ms +101.4 ms (after the first paint: layout 61, style 26, paint 8); 2221.5 ms +69.4 ms (after the first paint: script 44, style 11, layerize 6)
  - home · ar · 390: 221.7 ms +54.1 ms (before the first paint: other 48, task-self 5, layout 1); 1244.3 ms +68.6 ms (after the first paint: layout 52, style 16, other 0); 1362.9 ms +241.4 ms (after the first paint: layout 152, style 64, paint 15); 223.9 ms +71.5 ms (before the first paint: other 63, task-self 7, layout 1)
  - login · fr · 1440: 975.4 ms +81.2 ms (the first render: layout 44, style 29, other 3); 1078.8 ms +114.4 ms (after the first paint: layout 60, style 52, task-self 1); 226.9 ms +52.0 ms (before the first paint: other 47, task-self 5, style 0); 995.1 ms +75.2 ms (the first render: layout 42, style 26, other 2)
  - login · ar · 390: 243.3 ms +58.6 ms (before the first paint: other 52, task-self 6, layout 1); 1334.4 ms +133.8 ms (after the first paint: layout 60, style 40, paint 25); 221.3 ms +58.8 ms (before the first paint: other 52, task-self 6, layout 1); 1164.5 ms +54.4 ms (the first render: style 28, layout 21, other 2)
  - door · ar · 390: 218.2 ms +60.8 ms (before the first paint: other 53, task-self 6, style 1); 1073.1 ms +216.8 ms (after the first paint: layout 171, style 45, other 0); 231.1 ms +67.3 ms (before the first paint: other 60, task-self 6, layout 1); 1017.6 ms +51.5 ms (the first render: style 26, layout 20, other 3)
  - dashboard · fr · 1440: 244.6 ms +57.8 ms (before the first paint: other 51, task-self 6, style 0); 951.3 ms +73.5 ms (before the first paint: layout 44, style 22, paint 3); 1086.8 ms +101.2 ms (after the first paint: layout 81, style 19, task-self 1); 1268.5 ms +75.8 ms (after the first paint: layout 31, style 30, paint 8)
  - dashboard · ar · 390: 242.5 ms +72.8 ms (before the first paint: other 65, task-self 7, layout 1); 1183.9 ms +204.8 ms (after the first paint: layout 159, style 44, other 1); 1507.2 ms +98.2 ms (after the first paint: style 52, paint 23, layout 18); 1849.1 ms +50.9 ms (after the first paint: style 36, layout 9, script 5)
  - documents · ar · 390: 211.7 ms +56.8 ms (before the first paint: other 49, task-self 6, gc 1); 1157.1 ms +96.6 ms (after the first paint: layout 82, style 14, task-self 1); 1331.8 ms +116.5 ms (after the first paint: layout 61, style 36, paint 14); 1466.9 ms +64.7 ms (after the first paint: layout 33, style 32, other 0)
  - case · fr · 1440: 218.9 ms +54.0 ms (before the first paint: other 48, task-self 6, style 0); 914.8 ms +66.9 ms (before the first paint: layout 40, style 20, paint 3); 1054.1 ms +55.7 ms (after the first paint: layout 42, style 13, task-self 1); 1193.8 ms +62.3 ms (after the first paint: layout 34, style 20, paint 4)
  - journey · ar · 1440: 214.8 ms +56.7 ms (before the first paint: other 50, task-self 6, style 0); 1086.9 ms +80.4 ms (before the first paint: layout 48, style 25, paint 3); 1196.1 ms +163.1 ms (after the first paint: layout 141, style 21, other 1); 216.4 ms +63.2 ms (before the first paint: other 56, task-self 6, style 1)

### The Dépôt before and after P1 (the same twin, the same protocol)

| Cell | before: n, CLS median / max | after: n, CLS median / max | LCP ms before → after (medians) |
|---|---|---|---|
| qa-doc-person:document-requirement · ar · 1440 | 5, 0.035 / 0.035 | 9, 0.000 / 0.000 | 1 344 → 1 332 |
| qa-doc-person:document-requirement · ar · 390 | 5, 0.034 / 0.034 | 9, 0.000 / 0.000 | 1 316 → 1 360 |
| qa-doc-person:document-requirement · fr · 1440 | 5, 0.030 / 0.030 | 9, 0.000 / 0.000 | 1 148 → 1 132 |
| qa-doc-person:document-requirement · fr · 390 | 5, 0.023 / 0.023 | 9, 0.000 / 0.000 | 1 172 → 1 136 |
| qa-doc-person:document-upload · ar · 1440 | 5, 0.067 / 0.068 | 9, 0.000 / 0.000 | 1 316 → 1 264 |
| qa-doc-person:document-upload · ar · 390 | 5, 0.071 / 0.071 | 9, 0.000 / 0.000 | 1 316 → 1 276 |
| qa-doc-person:document-upload · fr · 1440 | 5, 0.059 / 0.059 | 9, 0.000 / 0.000 | 1 064 → 1 044 |
| qa-doc-person:document-upload · fr · 390 | 5, 0.042 / 0.042 | 9, 0.000 / 0.000 | 1 068 → 1 072 |
| qa-doc-person:documents · ar · 1440 | 5, 0.000 / 0.002 | 9, 0.000 / 0.000 | 1 256 → 1 268 |
| qa-doc-person:documents · ar · 390 | 5, 0.000 / 0.000 | 9, 0.000 / 0.000 | 1 340 → 1 380 |
| qa-doc-person:documents · fr · 1440 | 5, 0.000 / 0.002 | 9, 0.000 / 0.002 | 1 156 → 1 168 |
| qa-doc-person:documents · fr · 390 | 5, 0.000 / 0.000 | 9, 0.000 / 0.000 | 1 088 → 1 096 |


## Limits, said

- Chromium only (headless shell 1243): no Playwright WebKit or Firefox binary on this machine, none downloaded; no
  Safari, no real device. The plan's «Playwright WebKit and Firefox on every page type, where available» is not
  available here (W2-A's O10, W3-C's and W3-D's m6, W4-B's «at speed», for a machine that has them).
- CDP's throttling adds its latency per request, not per connection: HTTP/2's gain from multiplexing is understated by
  the emulation, so the HTTP/2 comparison says «no cost», not «HTTP/2's gain». The production server's own stack
  (TLS, HTTP/2, compression) is the owner's and was never touched.
- A shared machine (16 logical cores, 17–80 % busy at the windows' start, 1.6–5.2 GB free): the spreads above carry
  it; V5.5's sanity rule is what this is, not §2.6's «no worse than before» proof — no cell came near a budget, so the
  n ≥ 9 interleaved protocol was owed only for P1's cells, and run there.
- The twin keeps WhiteNoise's own manifest storage, not the product's `core.storage` subclass (devops-2): the same files
  and bytes on a cold load.
