# W1-P · Preview as the live product — independent re-check after fix round 1, lens: performance

Italy Legal Entry™ design V5 · V5.4 «EXECUTION MODE» · 5 October 2026, 12:20–13:40 · reviewer label
`w1p-performance-r2` (built nothing) · baseline: my round-1 report `performance.md` (branch at `b3e991c`) · the fixes:
`IMPLEMENTATION_NOTES.md`, «Review fixes — round 1» · plan `docs/design-v5/V5_4_EXECUTION_PLAN.md` §4 (4.1–4.6), §3.3
item 3, §2.2, §2.6, §2.7, §2.8 · DL54-01, DL54-17, DL54-18.

**Reviewed.** Branch `v54-w1-p` at `8f12192`: the seven commits since round 1 (`0dedb7e` the four reviews, `23ca9b6`,
`1ea7d06`, `f7555d1`, `2a05390`, `60196ec`, `8f12192`). I read the whole diff for what bears on speed and the database:
the ceiling's new body pre-read (`middleware.py`), the frame exception with DL54-17's POST (`frames.py`), the persona
switch's privileged-role check (`personas.py`), the census mirror and the per-request reads (`live.py`), the views, the
templates, the hub script's new pending timer (`designpreview.js`, part 3), and `dev.py`'s scratch-copy settings.

**Where.** My own server, `127.0.0.1:8791`, served from `C:/tmp/ile_wt/v54-w1-p` (clean tree at `8f12192`), with database
`ile_v5_l4`, `ILE_DESIGN_PREVIEW=1`, `ILE_DESIGN_PREVIEW_PORT=8791`, `ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`,
`--noreload` and `PGAPPNAME=ile-review-w1p-perf-r2`.
- **Why not 8785 or 8786.** When I started (12:29), other round-2 reviewers were already serving this worktree on both
  ports (one started 12:25, the other 12:28). 8791 is outside every port the plan assigns.
- **The application name.** I gave my server its own name, as LANES.json asks. The brief's query
  (`application_name='ile-design-preview'`) therefore keeps meaning 8780. It read **0 throughout the four bursts and at
  every mark of the persona series**, the two series that recorded it. My server's own count is the same query run with
  my server's name.
- **Two scratch servers, stopped after use.** Both are `git archive` exports outside the repository, under
  `C:/tmp/ile_v5_council/.work/w1p-performance-r2/`, on the same database and loaded with anonymous pages only.
  - 8792 serves `b3e991c`, the round-1 code. It is the A/B reference for every timing in this report.
  - 8793 serves `8f12192` plus a one-line change in `designpreview.js`: the variant measured for finding P-4.
- **The machine was loaded.** CPU sat at 73–76 % throughout: two full `pytest` suites, a browser suite and other
  reviewers' walks were running. `/fr/` alone took about twice round 1's time.
  - So no number below is compared across rounds.
  - Every timing is interleaved and paired, and the comparison with the round-1 code ran in the same session.
- **The lock.** Each benchmark window (bursts, timing series, stalled-body probes, the index A/B) held
  `C:/tmp/ile_locks/PERFORMANCE_BENCHMARK_LOCK` for its own duration only. Every browser series and the test run waited
  for it; the persona series waited 610 s for another agent's window.
- **Never touched:** 8780, 8782, 8770–8772, Chrome 9222/9223. Browsers: headless Chromium (Playwright), profiles under
  `C:/tmp/ile_v5_council/.profiles/w1p-performance-r2/`.
- **Evidence:** `E/w1-p/review-performance-r2/` (E/ = `C:/tmp/ile_v5_council/evidence/v54/`), with every script in its
  `tools/`.

## Verdict — PASS_WITH_FIXES

Every §4.6 item of this lens passes, measured. Round 1's two minors are fixed for the cases they named. Each fix leaves
one narrow gap, written up below as P-3 and P-4. **0 blocking, 0 major, 2 minor.** Neither minor blocks the merge, and
each has a concrete fix of a few lines.

| Asked | Measured now (`8f12192`) | Round 1 (`b3e991c`) |
|---|---|---|
| The database ceiling under a burst of 300 landing / index / frame requests at concurrency 32 | **max 8, 7, 8** connections over three bursts (concurrency 32, 32, 64), and **8** for a persona's burst. **0** at 0.5 s, 1 s and 5 s after each. 1,200 requests, **0 × 503** | max 8; 0 after |
| The frame-pair cap, enforced in code (try opening three) | **never more than 2 frames**, on every path tried. Ten addresses × pair now cost the server **exactly 2 frame documents and 0 «Broken pipe»** lines, in one task and across tasks (P-2 fixed). Connections in the whole series: max **1** | max 2 frames, but the server rendered 18 aborted documents and the ceiling reached 8 |
| Landing time on the lane, relative to the plain `/fr/` | framed home minus `/fr/`, paired medians, warm (n = 15): **+38 / +23 ms** at 1440 / 390 (×1), **−83 ms** LCP at CPU ×4. Against the round-1 code under the same load: head − base **+25 / −14 / −27 ms**, all inside the spread: **no regression** | +8.6 / +13.3 / +30 ms (unloaded machine) |
| Connections after the persona switch | **0** one second after every step, max 1 in between. Steps: entering from the strip and from the index's new one-click form, browsing, the read-only refusal, «Sortir», the product's own «Se déconnecter» in the frame, five HTTP cycles. **0** session rows left | 0 after every step |

## §4.6 — the items of this lens, one by one

| §4.6 item | Verdict | Measured |
|---|---|---|
| Frames load real pages only under the narrow condition (this lens: the relaxation reaches every framed page and nothing else) | PASS | 400 / 400 frame documents across the four bursts answered `SAMEORIGIN` + `frame-ancestors 'self'`. The matrix (§6) relaxes exactly GET, HEAD and POST framed by this origin (POST per DL54-17). These stay strict, `DENY` + `'none'`: PUT, a top-level load, a cross-site or same-site frame, a proxy header, a foreign `Host`, the back-office, and the landing itself. The rest of the item is the security reviewer's. |
| At most one frame pair at a time, enforced by the hub's script | PASS (see P-4) | Never more than 2 frames over every step of §3. A pointer click behind the open viewer cannot land (the viewer is modal). An injected third kind or ten addresses × pair still give 2 frames; Escape gives 0. P-2 is fixed: the server renders only the pair that remains. |
| The strip paints in ≤ 1 s | PASS | The landing's FCP (the strip), medians (max): warm **68 ms (216)**; cold **176 ms (244)** at 1440 and **128 ms (164)** at 390; cold at CPU ×4 **412 ms (652)**, n = 25. |
| The landing loads exactly one frame | PASS | 1 iframe and 1 child frame, with 0 iframes inside the framed page (the persona pages included). Still 1 after «Telefono 390» and after the frame navigated, with the address bar following (`?page=/fr/entreprises/&frame=phone`). |
| 0 CSP violations | PASS (in my runs) | 0 `securitypolicyviolation` events over every timing and cap series, plus a dedicated run of the flows the fix round changed (§6). One console line, the browser refusing to frame the back-office, is the case the stage's message now explains (the message was shown). |
| (Council lens, §3.3 item 3) the database ceiling | PASS (see P-3) | §1, §2. |
| (Council lens) the frame cap | PASS (see P-4) | §3. |

## 1. The database ceiling under a burst

The protocol is round 1's, unchanged (`tools/burst.py`, `tools/burst_persona.py`).
- **The burst.** 300 requests at 32 workers, a socket each: 100 landings (80 % of them with `?page=`), 100 indexes and
  100 frame documents. The pages come from the index's 86 public addresses (round 1: 70). Half the requests carry an
  unknown `ile_v5_sessionid`.
- **The sampler.** It counts my server's rows in `pg_stat_activity` every 1.2–1.4 ms (median), from 1 s before the burst
  to 5 s after.
- **Burst 4** uses a session minted by the switch (`qa-doc-person`, no password), signed out afterwards. Every one of its
  requests reads the database.

| Burst | Wall | Status | Max connections | After 0.5 s / 1 s / 5 s | Connections opened | p50 / p99 / max, s — landing · index · frame |
|---|---|---|---|---|---|---|
| 300 × 32, anonymous + unknown session | 28.3 s | 298 × 200, 2 × 404¹ | **8** | 0 / 0 / 0 | 200 | 2.36 / 4.16 / 4.28 · 3.64 / 5.59 / 5.79 · 2.16 / 3.70 / 3.74 |
| 300 × 32, the same again | 40.4 s | 298 × 200, 2 × 404¹ | **7** | 0 / 0 / 0 | 200 | 3.56 / 5.94 / 5.99 · 5.26 / 7.66 / 7.90 · 3.13 / 5.30 / 5.40 |
| 300 × 64 (twice the brief) | 39.2 s | 298 × 200, 2 × 404¹ | **8** | 0 / 0 / 0 | 200 | 7.56 / 9.34 / 9.47 · 9.11 / 13.94 / **17.01** · 7.47 / 9.15 / 9.31 |
| 300 × 32, persona `qa-doc-person` | 31.6 s | 300 × 200 | **8** | 0 / 0 / 0 | 300 | 2.68 / 4.80 / 4.86 · 4.06 / 6.59 / 6.65 · 2.77 / 4.53 / 4.94 |

¹ `/fr/forum-virtuel/` and `/ar/forum-virtuel/`, which the community gate answers 404 on this database. The index now
says «404 finché il forum virtuale è chiuso» (round-1 observation O-1, addressed).

- **At most the ceiling, 0 after:** yes, in every burst. Each request that reads the database opens one connection
  (`CONN_MAX_AGE` 0) and closes it when its response leaves the ceiling. None survives a burst. My server read 0 before
  every burst.
- **0 × 503.** At concurrency 64, though, one index request took **17.0 s**, nearly all of it queueing for a slot. That
  is close to the ceiling's 20 s `WAIT_SECONDS` (round 1: p99 4.5 s). See observation O-6: it is the heavier index on a
  loaded machine, at twice the brief's concurrency.
- **Queries per request** (`tools/querycount_r2.py`: in-process, dev settings, every write rolled back):

  | Request | Queries |
  |---|---|
  | The landing, or the index, without a session cookie | **0** |
  | The landing with an unknown session cookie | 1 |
  | A persona's landing or index | 1 (the session) |
  | The read-only refusal | 1 |
  | «Entrer» (DL54-18's group and permission checks included) | 12 |
  | «Entrer» with `page=`, the index's one-click form | 9 |
  | «Sortir» | 5 |
  | The framed dashboard (the product page, not the preview) | 82 |

- **Warm server time**, in-process, run alternately against both codes (n = 15 each, two rounds):

  | | The landing | The index | `/fr/` |
  |---|---|---|---|
  | The branch head | 20–21 ms | **91–100 ms** | 121–126 ms |
  | The round-1 code | 9–12 ms | **32–38 ms** | 82–96 ms |

  Without a session cookie neither preview page reads the database, yet each holds a ceiling slot while it renders
  (round-1 O-4). The index now costs about 0.7–0.8 of `/fr/`, against 0.4 for the round-1 code measured the same way
  (O-5).

## 2. P-1 re-checked — requests that announce a body and withhold it (`tools/stall_r2.py`)

Each scenario sends eight such requests, then loads the landing while they wait.

| Scenario (8 sockets each) | Landing while they wait | The withheld requests | My connections |
|---|---|---|---|
| A — the round-1 case: `POST /__design-v5/accedi/qa-doc-person/`, CSRF cookie, urlencoded, `Content-Length: 200` | **200 in 0.027 s** (round 1: 503 after 20.03 s) | no answer yet: each waits on its own thread | 0 |
| B — the site's own `POST /fr/compte/login/`, CSRF cookie, 200 B | **200 in 0.021 s** | waiting on their threads | 0 |
| C — control: the switch without a CSRF cookie, 200 B | 200 in 0.023 s | waiting for their bodies before their 403. This is the behaviour change the notes announce, on a thread and never on a slot | 0 |
| D — the login, CSRF cookie, urlencoded, **6 MB** announced | 200 in 0.020 s | `400 Bad Request` at once (`RequestDataTooBig`) | 0 |
| **E — the login, CSRF cookie, multipart, 6 MB announced** | **503 after 20.028 s** («Anteprima occupata …») | waiting, each **holding a slot** | 0 |
| **F — the switch, CSRF cookie, multipart, 6 MB announced** | **503 after 20.012 s** | waiting, each holding a slot | 0 |

Closing the sockets brings the landing back to 200 in 30–46 ms, every time.
- **P-1 is fixed** for the case it named and for every body up to `DATA_UPLOAD_MAX_MEMORY_SIZE` (5 MB here,
  `base.py:256`), and the new test holds that.
- **The same failure remains through the one door the fix leaves open on purpose.** The docstring says «a body too large
  to be read into memory … is read where it always was». For a multipart POST, that is `CsrfViewMiddleware` reading
  `request.POST` inside the slot. This is finding **P-3**.

## 3. The frame-pair cap — trying to open three; P-2 re-checked (`tools/framecap_r2.py`)

How the series counts:
- An observer installed before any script counts the index's `<iframe>`s at every mutation and timestamps every `src`
  it is given.
- Playwright counts child frames and frame documents.
- **New in this round:** the server's own log is sliced per scenario, counting the frame documents rendered and the
  «Broken pipe» lines.
- A sampler counts my server's connections throughout.

| Step | Frames | Most so far | Frame documents the server rendered |
|---|---|---|---|
| The index, loaded (the public fold open by default) | 0 | 0 | — |
| S1.1 «Desktop 1440» of `/fr/` (pointer) | 1 | 1 | 1 |
| S1.2 + the viewer's «Telefono 390» — the pair | 2 | 2 | 1 |
| S1.3 a third: the row's own «Desktop» and «Telefono» links again, scripted past the modal | 2, never doubled | 2 | 0 |
| S1.4 a pointer click on another row behind the open viewer | 2: the click cannot land (Playwright times out) | 2 | 0 |
| S2 scripted, in one task: Desktop of `/fr/entreprises/`, then Telefono of `/ar/institutions/` | 1: the pair went before the next came | 2 | 1 |
| S3 an injected third kind (`tablet`) for one address | 1 (`MAX_FRAMES` unloads the pair) | 2 | 1 |
| **S4a ten addresses × pair, scripted in one task** (186 ms of clicking) | 2 | 2 | **2, 0 broken pipes** (round 1: 18 broken pipes) |
| **S4b ten addresses × pair, across tasks** (one round trip between clicks, 338 ms) | 2 | 2 | **2, 0 broken pipes** |
| S6a a fast keyboard walk, ten rows: focus, Enter, Escape after 100 ms | 0 | 2 | **0** |
| S6b the same walk with Escape after 300 ms | 0 | 2 | 10 (each open lived long enough to load: none aborted) |
| S5 Escape / «Chiudi» | 0 | 2 | — |

- **What the series shows.** The cap holds, and P-2 is fixed: a burst of switches asks the server for the pair that
  remains, nothing on the way. My connections stayed at **max 1 over the whole series** (round 1: the ceiling, 8).
- **The landing**, measured in the same series: 1 iframe, 1 child frame and 0 iframes inside the framed `/fr/`. Still 1
  after «Telefono 390», and 1 after the frame navigated to `/fr/entreprises/`, with the address bar at
  `/__design-v5/?page=/fr/entreprises/&frame=phone`.

**What the timer costs a person's click** (S7, seven addresses, pointer clicks with the viewer closed, 1.5 s between
opens). The measure is the time from the click event to the moment the frame is given its `src`:

| Code | First open of an address («Desktop 1440») | Second frame of the open pair («Telefono 390», 1.2 s later) |
|---|---|---|
| **Branch head `8f12192`** | **median 168.7 ms** (157.6–181.0) | median 17.2 ms (15.2–20.5) |
| One-line variant on 8793 (P-4's fix) | median 24.2 ms (18.8–37.7) | median 19.5 ms (16.7–34.3) |

- **The comment says one thing, the code does another.** `request()`'s comment reads «at once (the next task) when
  nothing was unloaded in the last 300 ms — a person's click is not delayed», and the notes say the same. But `load()`
  calls `unload()` for every new address, and `unload()` stamps `lastUnload = now()` even when it removed nothing.
  Every first open therefore waits the 150 ms. This is finding **P-4**.
- **The variant's price**, measured with the same series on 8793. S4a (one task): 2 documents. S4b (across tasks):
  4 documents, the first pair aborted; the server logged 2 «Broken pipe» lines and my connections reached max 2. S6a
  (100 ms walk): 1 document.

## 4. Landing time on the lane, relative to the plain `/fr/` page

**Protocol** (`tools/ab_timing.py`):
- **Four cells per run, interleaved:** `/fr/` and the landing on 8791 (the branch head), and the same two on 8792 (the
  round-1 code). The order rotates every run and reverses on odd runs. Two unmeasured warm-up rounds.
- **Warm** = one tab per server, viewport and CPU setting, with a warm cache and renderer: the owner's real use.
  **Cold** = a fresh browser context for every load.
- **Throttling:** none, or `Emulation.setCPUThrottlingRate 4`. No network throttle: this is the lane (loopback, the dev
  server, uncompressed static), not 8782.
- **The figure** is the median of the per-run **paired** differences: the framed page's own FCP / LCP, shifted to the
  landing's time origin, minus the `/fr/` of the same server in the same run. Pairing removes the drift of a loaded
  machine; the spread of the paired differences is given in brackets.
- **Why a new protocol.** My first warm run used round 1's protocol: separate medians, head only, n = 11. It gave
  +60.5 / +2.5 / +190 ms with overlapping spreads (`timing2_warm_r2.json`). That is too noisy on this machine to judge,
  so this protocol supersedes it.

**Warm, n = 15 per cell (`ab_warm.json`)**

| Viewport, CPU | head: `/fr/` FCP = LCP | head: framed FCP / LCP | **head Δ paired** | base Δ paired | **head − base** | strip FCP (max), head · base | frame starts at, head · base |
|---|---|---|---|---|---|---|---|
| 1440 × 900, × 1 | 284 (196–384) | 306 / 306 | **+38.2** (−116 … +148) | +12.8 (−65 … +165) | **+25.4** | 68 (108) · 60 (88) | 40.1 · 36.8 |
| 390 × 844, × 1 | 208 (160–348) | 228 / 228 | **+23.0** (−113 … +418) | +37.2 (−140 … +154) | **−14.2** | 68 (216) · 64 (140) | 35.0 · 30.2 |
| 1440 × 900, × 4 | 656 (316–940) | 519 / 560 | **LCP −82.7** (−268 … +209) | LCP −55.8 (−194 … +513) | **LCP −26.9** | 220 (376) · 248 (344) | 87.6 · 89.8 |

**Cold (`ab_cold.json`, n = 11; the ×4 cell re-run with n = 25 in `ab_cold_cpu4_n25.json`)**

| Viewport, CPU | head: `/fr/` FCP / LCP | head: framed FCP / LCP | **head Δ paired** | base Δ paired | **head − base** | strip FCP (max), head · base | frame starts at, head · base |
|---|---|---|---|---|---|---|---|
| 1440 × 900, × 1 | 432 / 432 | 433 / 433 | **+28.9** (−67 … +136) | −0.3 (−120 … +104) | **+29.2** | 176 (244) · 164 (192) | 101.4 · 83.2 |
| 390 × 844, × 1 | 368 / 368 | 331 / 331 | **−9.4** (−160 … +38) | −37.3 (−108 … +62) | **+27.9** | 128 (164) · 128 (160) | 76.8 · 68.0 |
| 1440 × 900, × 4, n = 25 | 588 / 860 | 945 / 956 | **FCP +323, LCP +79.5** (LCP −322 … +323) | FCP +369, LCP +116 (LCP −303 … +456) | **FCP −45.5, LCP −36.4** | 412 (652) · 364 (616) | 179.9 · 158.1 |

- **What the owner sees** (the warm tab): the framed home's first paint is +23 to +38 ms off the plain `/fr/` at ×1,
  and ahead of it at ×4. Every warm median is inside PFR §1's resolution (≤ +50 ms for LCP).
- **The fix round's own effect.** Head minus round-1 code is −27 to +29 ms in every cell, alternating in sign and well
  inside the spreads, so there is **no measurable regression**. The n = 11 cold ×4 cell had first shown +112 / +195 ms;
  with n = 25 it reads −46 / −36 ms. The frame starts 3–5 ms later than in the round-1 code at ×1, warm.
- **Cold at CPU ×4** remains the one large number: the framed page's FCP is +323 ms (LCP +80 ms) after a plain `/fr/`.
  The round-1 code shows +369 / +116 ms under the same load, so this is pre-existing. It is round 1's explanation, now
  heavier because of the machine's load: a new renderer, and about 180 ms of the landing's own parse before the frame
  starts. It is a first open on a slow machine, and not a finding (O-8).
- **Long tasks** (summed per load, top document and frame together). Warm at ×1 there are none in either code. Cold at
  ×1, the longest task (the first render) is 101 vs 98 ms at 1440 and 103 vs 82 ms at 390: +21 ms at 390, within PFR's
  ≤ +30 ms for the first-render task. At ×4 the distributions of the two codes overlap (head 0–627 ms, base 0–457 ms
  at n = 25).
- **What the landing loads.** The number of requests is the same as the round-1 code's: 15 warm, 12–13 cold, beside the
  framed page's 22. What is heavier:

  | Asset | Head | Round-1 code |
  |---|---|---|
  | Landing HTML | 25,170 B (9.8 KB before the `<iframe>`, the data block after it) | 16,857 B |
  | Dev sheet | 56,379 B | 51,032 B |
  | Dev script | 20,764 B (still `defer`) | 12,425 B |

  At rest the strip still runs no animation, timer or `requestAnimationFrame`.

## 5. The persona switch — no connection leak (`tools/persona_leak_r2.py`)

The series ran in the browser, then with a plain HTTP client. The count is read one second after each step, and the
sampler watches in between (2 ms).

| Step | My connections 1 s after | Most since the previous step | Session row left |
|---|---|---|---|
| At rest; the landing, signed out | 0; 0 | 0; 1 | — |
| «Entrer» `qa-doc-person` from the strip (frame: `/fr/espace-reserve/`); two pages in the frame; «Sortir» | 0; 0; 0 | 1; 1; 1 | 0 |
| The same for `qa-person` | 0; 0; 0 | 1; 1; 1 | 0 |
| The same for `qa-fresh-person` | 0; 0; 0 | 1; 1; 1 | 0 |
| The same for `qa-company` (frame: `/fr/espace-reserve/entreprise/`) | 0; 0; 0 | 1; 1; 1 | 0 |
| **The index's one-click form** (`qa-doc-person`, «Mes échéances», ar); «Sortir» | 0; 0 | 1; 1 | 0 |
| `qa-person`: «Ma situation» submitted in the frame, the read-only refusal shown («Anteprima V5 — sola lettura.»); «Sortir» | 0; 0 | 1; 1 | 0 |
| **`qa-company`: the product's own «Se déconnecter» inside the frame**; the landing served again, naming nobody | 0 | 1 | 0 |
| Five HTTP cycles: enter / landing / framed dashboard / exit, each 302 / 200 / 200 / 302 | 0 | 1 | 0 × 5 |
| At rest, 5 s later | 0 | 0 | — |

- **What the series shows.** Whichever way a persona enters (from the strip, or the index's per-page POST form) and
  whichever way it leaves («Sortir», or the product's own sign-out in the frame), the switch leaves no connection
  behind. A persona's pages open one connection per request, and it closes with the response.
- **The brief's query** (`application_name='ile-design-preview'`) read 0 at every mark.
- **The persona burst** of §1 (300 database readers) also ended at 0.

## 6. Supporting checks

- **The frame-policy matrix** (`policy_r2.json`, one request per row):

  | Row | Status | Policy |
  |---|---|---|
  | GET `/fr/`, framed by this origin | 200 | `SAMEORIGIN` + `'self'`, no `upgrade-insecure-requests` |
  | HEAD, framed by this origin | 200 | relaxed, the same |
  | POST of the empty sign-in, framed by this origin (DL54-17) | 200 | relaxed, the same |
  | PUT, framed | 403 | `DENY` + `'none'` |
  | Top-level GET; top-level POST | 200; 200 | `DENY` + `'none'` + `upgrade-insecure-requests` |
  | Framed cross-site; framed same-site | 200; 200 | strict, the same |
  | `X-Forwarded-For`; `Host: localhost:8780` | 200; 200 | strict, the same |
  | The back-office, framed | 302 | `DENY` |
  | The landing, framed or top-level; the index | 200 | `DENY` + `'none'`, no `upgrade-insecure-requests` (DL54-17) |

- **CSP** (`csp_r2.json`). **0 `securitypolicyviolation` events** over 12 steps in every document:
  - signed out, `?page=/fr/espace-reserve/`: the sign-in rendered in the frame, at `?next=`;
  - its empty submission, answered in the frame;
  - a link to `/backoffice/` clicked inside the frame: the stage's message shown;
  - six `qa-doc-person` pages, fr and ar, with 0 nested iframes, then «Sortir»;
  - the index's viewer pair of `/fr/`, and `/ar/compte/login/` in the phone frame.

  The one console line is the browser's own refusal to frame the back-office.
- **Tests re-run** (lock-gated, `pytest_perf_subset_r2.log`). The performance-relevant subset of
  `tests/frontend/test_design_preview.py` gave **17 passed, 0 skipped, 75.7 s**. It covers:
  - the non-atomic views, the two bursts at the `runserver` class, the ceiling's limit, its wait and its 503;
  - file responses, a missing `request_finished`, resets, **the new withheld-body test**, the preview-only install;
  - the landing's one frame, and its FCP ≤ 1 s with one frame in the browser;
  - **the cap test with its new ten-address burst**, a persona entering and leaving;
  - **the redirect and the form's answer in the frame**, the frame-policy test, the dev chain's order.

  It ran on a scratch `test_ile_v5_l9_perfr2`, dropped afterwards: `test_ile_v5_l9` was in use by another reviewer's run
  at that moment (O-3 still applies).
- **`scripts/check_ownership.py w1-p v54/base`:** 30 inside, 3 slice → **PASS** (`ownership_r2.txt`).

## Findings

### Blocking — none.

### Major — none.

### Minor

**P-3 · P-1's failure remains for a multipart body announced above `DATA_UPLOAD_MAX_MEMORY_SIZE`: eight such requests
that withhold their body still make every page of the server, the landing included, answer 503 after 20 s.** Minor:
the class of round 1's P-1, through a narrower door. The code is W1-P's own, in `apps/designpreview/middleware.py`,
`_read_a_small_body` (`23ca9b6`).
- **Failure scenario.** Eight connections send `POST /fr/compte/login/` (or `POST /__design-v5/accedi/qa-doc-person/`)
  with any well-formed `ile_v5_csrftoken` cookie, `Content-Type: multipart/form-data; boundary=…` and
  `Content-Length: 6291456`, then send nothing and stay open.
  - The pre-read skips them, because the length is over the 5 MB limit.
  - `CsrfViewMiddleware`, or the switch's own `csrf_protect`, then reads `request.POST` inside the slot, and the
    multipart parser blocks on the socket.
  - `GET /__design-v5/` waits **20.03 s** and is answered **503**; so does everything else until the sockets close.
    Measured as scenarios E and F of §2, `stalled_body_probe_r2.json`.
  - The urlencoded variant of the same size is harmless: `RequestDataTooBig` is raised before any read (scenario D).
  - As in round 1, no browser does this on loopback; a stuck or half-written script does. The ceiling fails safe (my
    connections stayed 0), but it fails for everyone. And the docstring's «such a client now ties up a thread of its
    own, never a slot» is true only below 5 MB.
- **Fix.** Before the slot, also parse a multipart POST that is too large for memory. Django streams it through the
  upload handlers, so a file above `FILE_UPLOAD_MAX_MEMORY_SIZE` goes to a temporary file and nothing large is held in
  memory. A client that withholds such a body then costs a thread, as the small ones now do. In `middleware.py`:

  ```python
  from django.core.exceptions import BadRequest, RequestDataTooBig, TooManyFieldsSent, TooManyFilesSent
  from django.http.multipartparser import MultiPartParserError

  def _read_a_small_body(request) -> None:  # name it _read_the_body_first
      if request.method in _BODILESS:
          return
      try:
          length = int(request.META.get("CONTENT_LENGTH") or 0)
      except ValueError:
          return
      if length <= 0:
          return
      limit = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
      with contextlib.suppress(RequestDataTooBig, TooManyFieldsSent, TooManyFilesSent, MultiPartParserError, BadRequest, OSError):
          if limit is None or length <= limit:
              request.body  # noqa: B018 - in memory, as now
          elif request.method == "POST" and request.content_type == "multipart/form-data":
              request.POST  # noqa: B018 - streamed through the upload handlers, large files to temporary files
  ```

  - **Error paths change.** A malformed or oversized multipart body leaves `request.POST` empty, as Django's own
    `_mark_post_parse_error` does, and the CSRF check then answers 403 where it answered 400. This happens on the
    preview process only, on error paths only.
  - **Nothing in the codebase sets `request.upload_handlers`** (searched), so parsing early changes no view.
  - **The test.** Beside `test_a_client_that_withholds_its_body_costs_a_thread_never_a_slot`, the same test with
    `Content-Type: multipart/form-data; boundary=x` and `Content-Length: settings.DATA_UPLOAD_MAX_MEMORY_SIZE + 1`. The
    landing must answer 200 within 1.5 s, and closing the sockets must leave 0 connections.
  - **The alternative** I named in round 1 also closes this door, and removes O-4: take the slot at the thread's first
    database connection rather than at the start of the request. But `connection_created` fires after the connect, so it
    needs a hook before `connect()`. It is a larger change to a reviewed module.

**P-4 · The hub's pending timer delays every first open by 150 ms, against its own comment and the notes («a person's
click is not delayed»).** Minor. The code is W1-P's own: `static/js/dev/designpreview.js`, part 3, `unload()` (line 451)
and `request()` (lines 456–471), from `f7555d1`.
- **Failure scenario.** The owner, on the index, clicks «Desktop 1440» on any row.
  - `load()` sees a new address and calls `unload()`.
  - `unload()` stamps `lastUnload = now()` unconditionally, though it removed nothing (the viewer was closed).
  - `request()` then finds the last unload under 300 ms ago, and arms 150 ms instead of the next task.
  - Measured (§3, S7): click to `src` **157.6–181.0 ms** (median 168.7) for every first open, against 15–20 ms for the
    pair's second frame. The frame's page arrives 150 ms later than it needs to, on every open, and the code says the
    opposite.
- **Fix — one line, measured.** Stamp only when a frame was really removed:

  ```js
  function unload(kind) {
    var removed = false;
    held.frames = held.frames.filter(function (item) {
      if (kind && kindOf(item) !== kind) {
        return true;
      }
      removed = true;
      // … unchanged …
    });
    // … unchanged …
    if (removed) {
      lastUnload = now();
    }
    pressed();
    fit();
  }
  ```

  On the scratch server 8793 (§3), this variant does what the comment promises:
  - a first open takes **24.2 ms** median (18.8–37.7);
  - the test's burst in one task still costs **2** documents;
  - a burst scripted across tasks costs 4 documents (the first pair aborted; 2 «Broken pipe» lines, max 2 connections),
    and a 100 ms keyboard walk costs 1. Both stay far under the ceiling.
- **The test.** Add to `test_the_index_never_holds_more_than_one_pair_of_frames`: after the first click, the desktop
  frame is given its `src` less than 100 ms after the click's `event.timeStamp`, timestamped with a MutationObserver as
  `framecap_r2.py` does.
- **The other way, equally acceptable.** If the team prefers the head's stricter behaviour (0 wasted documents in every
  burst, 0 in a 100 ms keyboard walk), keep the code and correct the words, so that they stop promising what the code
  does not do. Change `request()`'s comment, the part-3 header and the notes' «the next task when nothing was unloaded
  in the last 300 ms» to: «every newly opened address waits 150 ms; the second frame of an open pair is asked for at the
  next task».

## Round-1 findings and observations — where they stand

| Round 1 | Now |
|---|---|
| **P-1** — a withheld body held a slot | **Fixed** for every body up to 5 MB (§2, A–D; the new test passes). The multipart door above 5 MB remains: **P-3**. |
| **P-2** — the cap bounded the frames, not the documents the server renders | **Fixed**: ten addresses × pair cost exactly 2 rendered documents, 0 broken pipes, in one task or across tasks; my connections stay at max 1 (§3). Its timer brought **P-4**. |
| O-1 — the closed virtual forum listed without a word | Addressed: the row says «404 finché il forum virtuale è chiuso». |
| O-2 — two reviewer ports were not enough | Still true: 8785 and 8786 were both taken at 12:29, so I used 8791 again. |
| O-3 — one test database for all reviewers, with `--reuse-db` | Still true: `test_ile_v5_l9` was in use, so I used a scratch database and dropped it. |
| O-4 — the landing and the index queue for a slot they do not need | Larger now: see O-5 and O-6. |

## Observations — not findings; for other lenses and the orchestrator

- **O-5 (UX, with numbers).** The index is now the one surface measurably heavier than in round 1. It grew from
  mirroring W1-0's whole census (UX M2) and from per-language persona forms (UX M3).

  | | Branch head | Round-1 code |
  |---|---|---|
  | HTML | 175,967 B (13.4–14.0 KB gzip) | 102,071 B (10.3 KB) |
  | Elements | 2,293 | 1,228 |
  | Forms | 102 | 8 |
  | Server time, in-process | 91–100 ms | 32–38 ms |
  | Cold FCP at ×1 | 476 ms (max 672) | 332 ms |
  | Cold DCL at ×1 | 460 ms | 189 ms |
  | Cold DCL at ×4 | 1,848 ms | 949 ms |

  - **Cost.** FCP is +148 ms cold at ×1 (paired, n = 9; every run later, +4 … +276); at ×4, FCP 780 ms (max 992), and
    81 ms of long tasks against 0 (`index_ab.json`).
  - **Budget.** It still paints within a second, and no budget applies to it.
  - **Where the bytes are.** The 94 one-click forms are 50 KB (29 %), each carrying the same CSRF token and three hidden
    inputs; the 455 hidden-word spans another 30 KB.
  - **Optional, UX's call.** One form per persona card, with `<button name="page" value="…">` per page: a button's name
    and value are submitted with its form. The language follows from the page's prefix (the `lang` field matters only
    for `/documents/`). That brings 94 forms down to 4, about −40 KB and several hundred elements.
- **O-6 (orchestrator).** At concurrency 64, twice the brief, one index request took 17.0 s, nearly all of it queueing
  for a slot, against the ceiling's 20 s `WAIT_SECONDS`.
  - **Why.** The server is a single process under the GIL: a burst costs its total CPU time, whatever the slots. The
    index now costs about 2.5× its round-1 time, on a loaded machine. The semaphore lets a newcomer pass a waiter, so the
    unluckiest request waits longest.
  - **What it means.** Owner-sized use never queues, and at the brief's 32 the worst wait is 7.9 s. But the 503
    fail-safe is close for an index-heavy burst at 64. O-5's lighter index, or P-3's alternative, would widen the margin.
- **O-7 (orchestrator).** Three persona sessions are live on `ile_v5_l4` (two `qa-person`, one `qa-company`), last
  written about 10:18 and 12:41 (Rome), outside every window in which this review signed in. They hold no connection,
  and they expire in eight hours. They are someone's unclosed «Entrer», on the database the lane's reviewers share.
- **O-8.** A cold first open at CPU ×4 frames the home about 320 ms after a plain `/fr/` would paint (FCP; LCP +80 ms),
  in the round-1 code as in the head (§4). Should the owner's first open on a slow machine matter, it is what to shorten,
  by having the frame start before the strip's stylesheets. It is not this round's work.

## What this review wrote, and its limits

**What it wrote.**
- **To `ile_v5_l4`, only what the persona switch writes for a sign-in and a sign-out.** There were 14 sign-ins, each
  signed out, its session row deleted and checked by key:
  - one for the persona burst;
  - seven in the browser for §5: four from the strip, one by the index's form, one for the refusal, one ended by the
    product's own sign-out;
  - five HTTP cycles;
  - one for the CSP run.

  The audit row of `user_logged_in` and `last_login` remain, as after any sign-in.
- **The in-process query count** ran inside a transaction that was rolled back. The withheld-body probes never reached
  a view.
- **Untouched:** `ile_v5`, `ile` and `ile_qa`.
- **The scratch servers 8792 and 8793 are stopped**; their exports stay under
  `C:/tmp/ile_v5_council/.work/w1p-performance-r2/`. **The scratch test database is dropped.** My server and its
  connections were at 0 at rest at the end, and my server is stopped.
- **No commit.** This report is left in the family's QA folder, as round 1's was.

**Limits.**
- **Lane conditions:** the dev server, uncompressed static, DEBUG. Performance PASS for product pages is 8782's (§2.6),
  where the preview cannot run.
- **A loaded machine:** absolute times are not comparable with round 1's. The paired A/B against the round-1 code is the
  comparison, and it is still noisy, with spreads of ±100 ms and more on single cells.
- **Browsers:** headless Chromium on Windows only. No WebKit, no Firefox, no real phone.
- **The burst client** opens a socket per request, which is harsher on accept than a browser's keep-alive sockets.

## Evidence (E/w1-p/review-performance-r2/)

- **Bursts:** `burst1_300x32.json` + `_samples.csv`, `burst2_300x32`, `burst3_300x64`, `burst4_persona_300x32`.
- **P-1 re-check:** `stalled_body_probe_r2.json`.
- **The cap:** `framecap_r2.json` (head) and `framecap_variant_8793.json` (P-4's variant).
- **Timing:**
  - `ab_warm.json`, `ab_cold.json` and `ab_cold_cpu4_n25.json`, the A/B behind every number in §4;
  - `timing2_warm_r2.json`, the round-1 protocol, superseded;
  - `index_ab.json`.
- **Persona switch and policy:** `persona_leak_r2.json`, `csp_r2.json`, `policy_r2.json`.
- **First requests and queries:** `probe_r2.txt` (first requests, headers, warm latency over HTTP) and
  `querycount_r2.txt`.
- **Tests and ownership:** `pytest_perf_subset_r2.log`, `ownership_r2.txt`.
- **Server logs:** `srv8791.log` (mine), `srv8792_base_b3e991c.log`, `srv8793_variant.log`.
- **Pages:** `landing.html` and `index.html`, as served.
- **Scripts:** `tools/`, every script above, LF. It also holds `run_locked.py` and `lockutil.py`, the lock windows.
