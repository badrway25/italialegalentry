# W1-P · Preview as the live product — independent review, lens: performance

Italy Legal Entry™ design V5 · V5.4 «EXECUTION MODE» · 5 October 2026, 10:03–10:40 · reviewer label
`w1p-performance` (built nothing) · plan `docs/design-v5/V5_4_EXECUTION_PLAN.md` §4 (4.1–4.6), §3.3 item 3,
§2.2, §2.6, §2.7, §2.8 · DL54-01.

**Reviewed.** Branch `v54-w1-p` at `b3e991c`, five commits on `v54/base` (`f11d131`): `1338303`, `aab76d2`,
`7bb39e5`, `bb1ba5b`, `b3e991c`. The diff read in full for what bears on speed and the database: the ceiling
(`middleware.py`, unchanged), the gate (`access.py`), the frame exception (`frames.py`), the persona switch and its
read-only rule (`personas.py`), `live.py`, the views, the templates, `designpreview.js`, the preview block of
`dev.py`.

**Where.** My own server, `127.0.0.1:8791`, from `C:/tmp/ile_wt/v54-w1-p` (clean tree at `b3e991c`), database
`ile_v5_l4`, `ILE_DESIGN_PREVIEW=1`, `ILE_DESIGN_PREVIEW_PORT=8791`, `ILE_REFERENCE_DATE=2026-10-03`,
`DB_CONN_MAX_AGE=0`, `--noreload`, `PGAPPNAME=ile-review-w1p-perf`.
- Not 8785 / 8786: when I started, both — and 8789 — were already serving this worktree for the other W1-P
  reviewers (a11y, security, UX). 8791 is outside every port the plan assigns.
- The application name is my own, as LANES.json asks of every server that is not 8780, so that the brief's count —
  `select count(*) from pg_stat_activity where application_name='ile-design-preview'` — keeps meaning 8780 alone. It
  read **0 for the whole of every series below** (the owner's server untouched). My server's count is the same
  query with my name.
- Headless Chromium 153 (Playwright 1.63), own profiles under `C:/tmp/ile_v5_council/.profiles/w1p-performance/`.
  Every browser series waited for the lock; every benchmark window (the bursts, the timing series, the stalled-body
  probes) held `C:/tmp/ile_locks/PERFORMANCE_BENCHMARK_LOCK` for its own duration only, as plan §2.8 and the W1-0
  tools do. 8780, 8782, 8770–8772 and Chrome 9222 / 9223 were never loaded.
- Evidence: `E/w1-p/review-performance/` (E/ = `C:/tmp/ile_v5_council/evidence/v54/`); every script in its
  `tools/`.

## Verdict — PASS_WITH_FIXES

Every §4.6 item of this lens passes, measured. **0 blocking, 0 major, 2 minor** — neither blocks the merge; both are
cheap hardening of exactly what this lens is about (the database ceiling, the frame cap).

| Asked | Measured |
|---|---|
| The database ceiling under a burst of 300 landing / index / frame requests at concurrency 32 | **max 8** connections (= the ceiling), **0** half a second after the last response; 4 bursts, 1,200 requests, 0 × 503 |
| The frame-pair cap, enforced in code (try opening three) | **never more than 2 frames** in the index, on every path tried (three, and twenty); 0 after closing; the landing holds **exactly 1** |
| Landing time on the lane, relative to the plain `/fr/` | the framed home's FCP = LCP **+8.6 ms** (1440) / **+13.3 ms** (390) in a warm tab, **+30 ms** at CPU × 4; the strip paints at **32 ms** warm, **140 ms** cold (worst: 396 ms, cold at CPU × 4) |
| Connections after the persona switch | **0** one second after every Entrer, browse, refusal and Sortir; max 1 in between; session rows deleted on Sortir |

## §4.6 — the items of this lens, one by one

| §4.6 item | Verdict | Measured |
|---|---|---|
| frames load real pages only under the narrow condition (this lens: the relaxation reaches every framed page and nothing else) | PASS | 100 / 100 frame documents of each burst answered `X-Frame-Options: SAMEORIGIN` + `frame-ancestors 'self'`; a top-level navigation, a cross-site or same-site frame, a proxy header, a foreign `Host`, a POST and the landing itself all keep `DENY` + `'none'` (matrix in `console_outputs.txt`). The rest of the item is the security reviewer's. |
| at most one frame pair at a time, enforced by the hub's script | PASS (see P-2) | observer maximum 2 over 11 steps (§2); a pointer click behind the open viewer cannot land (the modal makes the page inert); scripted clicks past it, an injected third kind, twenty frames asked for back to back: still 2; Escape: 0. |
| the strip paints in ≤ 1 s | PASS | the landing's FCP (= the strip): warm 32 ms (max 44), cold 140 ms (max 172) at 1440 × 900; cold 112 ms (max 140) at 390 × 844; CPU × 4: warm 88 ms (max 124), cold 316 ms (max 396). |
| the landing loads exactly one frame | PASS | 1 iframe and 1 child frame; 0 iframes inside the framed page (no product template contains an `<iframe>`; persona pages checked too); still 1 after «Telefono 390» and after the frame navigated, the address bar following (`?page=…&frame=phone`). |
| 0 CSP violations | PASS (in my runs) | 0 `securitypolicyviolation` events and 0 console «Content Security Policy» / «Refused to» lines over ~180 top-level loads with their frames (landings, framed public pages, the index and its frames) and six persona pages in the frame, fr and ar (`persona_csp.json`). |
| (council lens, §3.3 item 3) the database ceiling | PASS (see P-1) | §1. |
| (council lens) the frame cap | PASS (see P-2) | §2. |

## 1. The database ceiling under a burst

**Protocol** (`tools/burst.py`). 300 requests, a socket each (`requests`), 32 workers: 100 landings
(`/__design-v5/`, 80 % with `?page=` one of the index's 70 public URLs), 100 indexes, 100 frame documents (a public
page with `Sec-Fetch-Dest: iframe` and `Sec-Fetch-Site: same-origin`); half of them carry an unknown
`ile_v5_sessionid`, which makes the landing and the index read the session as well. A sampler on its own connection
counts my server's rows of `pg_stat_activity` as fast as it can — median interval 0.9 ms, 11,000–16,000 samples per
burst — from 1 s before to 5 s after. Burst 4 is a persona's: a session minted by the switch (`qa-doc-person`, no
password), persona pages in the frame — every request reads the database.

| Burst | Wall | Status | Max connections | After 0.5 s / 1 s / 5 s | Connections opened | p50 / p99, s — landing · index · frame |
|---|---|---|---|---|---|---|
| 300 × 32, anonymous + unknown session | 15.6 s | 297 × 200, 3 × 404¹ | **8** | 0 / 0 / 0 | 200 | 1.55 / 2.04 · 2.07 / 2.78 · 1.41 / 1.99 |
| 300 × 32, the same again | 11.1 s | 297 × 200, 3 × 404¹ | **7** | 0 / 0 / 0 | 200 | 1.07 / 1.33 · 1.49 / 1.88 · 1.00 / 1.72 |
| 300 × 64 (twice the brief) | 13.1 s | 292 × 200, 3 × 404¹, 5 refused² | **7** | 0 / 0 / 0 | 196 | 2.91 / 4.20 · 3.46 / 4.51 · 2.85 / 4.14 |
| 300 × 32, persona `qa-doc-person` | 14.4 s | 300 × 200 | **8** | 0 / 0 / 0 | 300 | 1.33 / 2.04 · 1.87 / 2.57 · 1.37 / 2.19 |

¹ `/fr/forum-virtuel/` and `/ar/forum-virtuel/`: the index lists the virtual forum, which the community gate answers
404 on this database (observation O-1). ² TCP connects refused by runserver's listen backlog at 64 simultaneous
sockets — before the ceiling, never a 503.

- **At most the ceiling, 0 after:** yes, in every burst. One connection per request that reads the database
  (`CONN_MAX_AGE` 0), closed when the response leaves the ceiling; none survives a burst.
- **0 × 503:** the waits (≤ 5 s at concurrency 64) stay far below the ceiling's 20 s `WAIT_SECONDS`.
- **Queries per request** (`tools/querycount.py`: in-process, dev settings, every write rolled back): the landing
  and the index **0** without a session cookie and **1** with one (the session); the read-only refusal 1. Warm
  server time (n = 15): the landing 12.7 ms, the index 35.7 ms, `/fr/` 85 ms.
- Under a burst the landing waits like everything else: it reads nothing, but the ceiling gives every request a slot
  (observation O-4). Owner-sized use — the index, one pair, the landing — never queues.

## 2. The frame-pair cap — trying to open three (`tools/framecap.py`)

An observer installed before any script counts the index's `<iframe>`s at every mutation; Playwright counts child
frames and frame document requests; the sampler counts connections.

| Step | Frames | Most so far |
|---|---|---|
| the index, loaded | 0 | 0 |
| S1.1 «Desktop 1440» of `/fr/` | 1 | 1 |
| S1.2 + the viewer's «Telefono 390» — the pair | 2 | 2 |
| S1.3 a third, from the viewer: «Desktop 1440» again | 2 (never doubled) | 2 |
| S1.4 a pointer click on another row, behind the open viewer | 2 — the click cannot land (modal; Playwright times out) | 2 |
| S2 scripted, one task: Desktop of `/fr/entreprises/`, then Telefono of `/ar/institutions/` | 1 (each pair went before the next came) | 2 |
| S3 a Desktop and an injected third kind (`tablet`) for one address | 1 (`MAX_FRAMES` unloads the pair) | 2 |
| S4 ten addresses × pair, scripted back to back — twenty frames asked for | 2 | 2 |
| S5 Escape | 0 | 2 |

The cap holds in the browser: the script cannot be made to hold a third frame. What it does not bound is the server.
In S4 the browser aborted the documents it unloaded (`net::ERR_ABORTED`; never more than 2 in flight on its side),
but the dev server rendered every one of them to the end — **18 «Broken pipe» lines in 375 ms** of `srv8791.log`
(10:13:30.678–31.053; the two earlier runs of the same series: 18 each) — and my connection count reached the
ceiling, 8, then 0. The ceiling, not the cap, protected the database (finding P-2). No pointer path reaches this at a
person's speed: the viewer is modal.

The landing: 1 iframe, 1 child frame, 0 iframes inside the framed `/fr/`; after «Telefono 390», 1 (no reload); after
the frame navigated to `/fr/entreprises/`, 1, and the address bar read
`/__design-v5/?page=/fr/entreprises/&frame=phone`.

## 3. Landing time on the lane, relative to the plain `/fr/` page

**Protocol** (`tools/landing_timing.py`, `tools/landing_timing_warm.py`). n = 11 per cell; `/fr/` and
`/__design-v5/` interleaved, the order flipped each run; 2 unmeasured warm-up rounds. **Cold** = a fresh browser
context per load (empty cache, a new renderer); **warm** = one tab per row, cache and renderer warm — the owner's
real use. Unthrottled, and `Emulation.setCPUThrottlingRate 4`; no network throttle (loopback, the dev server,
uncompressed static: this is the lane, not 8782). The framed page's FCP and LCP are its own entries, moved to the
landing's time origin. Medians, spread in brackets, ms.

**Warm**

| Viewport, CPU | `/fr/` FCP = LCP | framed `/fr/` FCP = LCP | Δ | `/fr/` load | landing load | Δ | strip FCP (max) | frame starts at |
|---|---|---|---|---|---|---|---|---|
| 1440 × 900, × 1 | 168 (152–240) | 176.6 (156.6–215.1) | **+8.6** | 122.1 | 126.8 | +4.7 | 32 (44) | 20.4 |
| 390 × 844, × 1 | 132 (120–152) | 145.3 (130.0–173.7) | **+13.3** | 115.0 | 137.9 | +22.9 | 32 (44) | 19.1 |
| 1440 × 900, × 4 | 308 (264–352) | 338.0 (321.1–384.8) | **+30.0** | 345.9 | 404.0 | +58.1 | 88 (124) | 57.6 |

**Cold**

| Viewport, CPU | `/fr/` FCP = LCP | framed `/fr/` FCP = LCP | Δ | `/fr/` load | landing load | Δ | strip FCP (max) | frame starts at |
|---|---|---|---|---|---|---|---|---|
| 1440 × 900, × 1 | 376 (348–528) | 356.8 (337.5–414.1) | −19.2 | 342.8 | 327.7 | −15.1 | 140 (172) | 69.5 |
| 390 × 844, × 1 | 300 (276–364) | 308.9 (276.5–360.7) | +8.9 | 320.3 | 313.3 | −7.0 | 112 (140) | 64.9 |
| 1440 × 900, × 4 | 760 (484–844) | 864.3 (716.0–960.8) | **+104.3** | 1296.7 | 1184.3 | −112.4 | 316 (396) | 127.5 |

- **What the owner sees** — the warm tab — costs the framed home +9 to +13 ms of first paint unthrottled and +30 ms
  at CPU × 4: inside PFR §1's resolution (≤ +50 ms for LCP). The landing's own document is ≈ 9 ms to first byte; the
  frame's navigation starts 19–20 ms after the landing's (58 ms at CPU × 4).
- **The one larger number** — cold at CPU × 4, +104 ms — is the frame starting 127 ms late: a new renderer's commit
  (≈ 60 ms, which `/fr/` alone pays as well, before its first request) plus ≈ 65 ms of parsing before the `<iframe>`
  is inserted (`console_outputs.txt`, insert time: the strip and the iframe inserted at 136 ms, the head's sheets
  already loaded at 83 ms). Unthrottled, the same cold start costs nothing measurable (−19 / +9 ms). A first open on
  a slow machine; not a finding.
- **What the landing adds to the network:** 12 requests of its own — the four token layers (48 KB raw), the dev sheet
  (51 KB raw, 10 KB gzip), the dev script (12 KB), the strip's four fonts (87 KB; the framed page then finds them in
  the cache) and the mark — beside the framed page's 22. Its HTML is 17 KB (3.4 KB gzip): 8.4 KB of strip before
  the frame, the 8.5 KB data block after it.
- **At rest the strip costs nothing:** no animation, no timer, no `requestAnimationFrame` (two hover / toggle
  transitions, one of them behind `prefers-reduced-motion: no-preference`; one `setTimeout(0)` on window blur).
- The index, for completeness (`index_timing.json`): 102 KB of HTML, 1,233 elements, 0 frames at load; FCP 380 ms
  cold (844 ms at CPU × 4).

## 4. The persona switch — no connection leak (`tools/persona_leak.py`)

In the browser, for each of the four personas: «Personas» → «Entrer» (a POST with its CSRF token) → the landing
framing its first page → two more of its pages, navigated inside the frame → «Sortir». Then `qa-person` again: its
«Ma situation» form submitted inside the frame (the read-only refusal shows there), and «Sortir». Then a plain HTTP
client: five enter / landing / framed dashboard / exit cycles back to back. The count is read one second after each
step; the sampler watches in between.

| Step | Connections 1 s after | Most since the previous step |
|---|---|---|
| at rest; the landing, signed out | 0; 0 | 0; 1 |
| Entrer `qa-doc-person` (frame: `/fr/espace-reserve/`); two pages; Sortir | 0; 0; 0 | 1; 1; 1 |
| Entrer `qa-person`; two pages; Sortir | 0; 0; 0 | 1; 1; 1 |
| Entrer `qa-fresh-person`; two pages; Sortir | 0; 0; 0 | 1; 1; 1 |
| Entrer `qa-company` (frame: `/fr/espace-reserve/entreprise/`); two pages; Sortir | 0; 0; 0 | 1; 1; 1 |
| `qa-person`: the POST of «Ma situation» refused in the frame («Anteprima V5 — persona in sola lettura.»); Sortir | 0; 0 | 1; 1 |
| five HTTP cycles (302 / 200 / 200 / 302 each) | 0 | 1 |
| at rest, 5 s later | 0 | 0 |

The four browser sessions and the five HTTP ones left **0** rows in `django_session` after «Sortir» (checked by
key). A persona's landing and index read the database once (the session) and close the connection when the response
leaves; §1's burst as `qa-doc-person` — 300 requests, each a database reader — ended at 0 as well.

## 5. Supporting checks

- **Tests re-run** (lock-gated): the performance-relevant subset of `tests/frontend/test_design_preview.py` — the
  bursts at the `runserver` class, the ceiling (the wait and its 503, file responses, resets, `request_finished`
  never coming), the non-atomic views, the landing's one frame and FCP ≤ 1 s, the index's pair, the strip following
  the frame, a persona entering and leaving — **15 passed, 0 skipped, 48 s** (`pytest_perf_subset.log`). Run on a
  scratch `test_ile_v5_l9_perf`, dropped afterwards: `test_ile_v5_l9` was held by another reviewer's run at that
  moment, and `--reuse-db` (pyproject `addopts`) makes two runs on one test database collide (O-3).
- `scripts/check_ownership.py w1-p v54/base`: 24 inside, 2 slice → PASS.

## Findings

### Blocking — none.

### Major — none.

### Minor

**P-1 · A request whose announced body never arrives holds a ceiling slot; eight of them make every page of the
server answer 503 — the landing, which reads nothing, included.** Minor. Pre-existing at `v54/base`
(`apps/designpreview/middleware.py` is unchanged by W1-P), but inside W1-P's slice, and W1-P adds the preview's first
POST routes.
- *Failure scenario.* Eight connections send `POST /__design-v5/accedi/qa-doc-person/` with the `ile_v5_csrftoken`
  cookie and `Content-Length: 200`, then no body, and stay open. `CsrfViewMiddleware` reads `request.POST` — waits
  for the body — inside the slot the ceiling took first. The next request, `GET /__design-v5/`, waits **20.03 s** and
  is answered **503** «Anteprima occupata …»; so is everything else until the sockets close (then 200 in 14 ms). The
  same with the site's own `POST /fr/compte/login/` (the index: 503 after 20.03 s). Control: the same eight POSTs
  without the CSRF cookie are refused before the body is read — the landing 200 in 29 ms
  (`stalled_body_probe.json`). No browser does this on loopback; a stuck or half-written script does. The connection
  count never passes 8 — the ceiling fails safe, but it fails for everyone, and its 503 speaks of «richieste che
  usano il database» to a page that uses none.
- *Fix.* Read a small announced body **before** taking the slot, so that a client that withholds it costs a thread,
  never a slot. In `ConnectionCeilingMiddleware.__call__`, before `self.slots.acquire(...)`:

  ```python
  if request.method not in ("GET", "HEAD", "OPTIONS", "TRACE"):
      try:
          length = int(request.META.get("CONTENT_LENGTH") or 0)
      except ValueError:
          length = 0
      limit = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
      if length > 0 and (limit is None or length <= limit):
          try:
              request.body  # read once and kept by HttpRequest; POST and FILES are parsed from memory
          except (UnreadablePostError, RequestDataTooBig):
              pass  # the chain meets the same error, as it does today
  ```

  (`UnreadablePostError` from `django.http`, `RequestDataTooBig` from `django.core.exceptions`.) And a test beside
  `test_a_client_that_resets_after_its_page_costs_the_server_no_slot`: at the `runserver` class with a ceiling of 2,
  three raw sockets announce a body to the persona switch (CSRF cookie set) and withhold it; a `GET` of the landing
  answers 200 in under a second; closing the sockets leaves 0 connections. One behaviour changes, deliberately: a POST
  without a CSRF cookie that also withholds its body now waits for its body before its 403. (The alternative with
  the same effect, plus no slot at all for pages that read nothing — take the slot at the thread's first database
  connection rather than at the start of the request — is a larger change to a reviewed module.)

**P-2 · The index's cap bounds the frames the browser holds, not the documents the server renders.** Minor. W1-P's
own code: `static/js/dev/designpreview.js`, part 3.
- *Failure scenario.* Addresses opened faster than a page renders — S4 in §2, ten addresses × pair, scripted: the
  script holds ≤ 2 frames at every moment and aborts the rest, but the dev server renders each aborted document to
  the end (18 «Broken pipe» in 375 ms) and the server's connections reach the ceiling (8). The plan's reason for the
  cap — «8780's database ceiling is 8 slots» (RTE-m9) — is met by the ceiling, not by the cap. Not reachable by
  pointer at a person's speed (the viewer is modal); reachable by any script, or by Escape / Enter in quick
  succession on the rows.
- *Fix.* Request a frame only while it is still wanted. In `load()`, create the `<iframe>` with its address in
  `data-dp-src`, and set `src` from a single pending timer that `unload()` clears: at once when nothing was unloaded
  in the last 300 ms (a person's click is not delayed), after ≈ 150 ms otherwise — so a burst of switches requests
  only the pair that remains. Adjust `test_the_index_never_holds_more_than_one_pair_of_frames` (it reads `src`
  synchronously after a scripted click) and add to it: ten addresses back to back → at most 2 frame document requests
  seen by `page.on("request")`.

## Observations — not findings; for other lenses and the orchestrator

- **O-1 (UX / content).** The index lists «Il forum virtuale» (`community:index` → `/fr/forum-virtuel/`,
  `/ar/forum-virtuel/`), which the community gate (`gates.virtual_forum_enabled()`) answers 404 on `ile_v5_l4`; its
  frames show the 404 page. Mark gated pages in the index, or leave them out while their gate is closed.
- **O-2 (orchestrator).** Two reviewer ports were not enough: 8785, 8786 and 8789 were all serving this worktree for
  the other reviewers when I started, so I used 8791. One port per reviewer keeps a burst off somebody else's server.
- **O-3 (orchestrator).** One test database for all reviewers (`test_ile_v5_l9`) with `--reuse-db` in `addopts`: two
  reviewers' runs collide. One per reviewer — or a scratch name dropped afterwards, as here.
- **O-4.** The strip under artificial load: at concurrency 32 the landing's own response has a p50 of 1.07–1.55 s,
  queueing for a slot it does not need. At owner-sized load there is no queue (§1). P-1's alternative would remove it.

## What this review wrote, and its limits

- **Writes to `ile_v5_l4`:** only what the persona switch writes for a sign-in and a sign-out — 12 sign-ins (5 in the
  browser for §4, 1 for the CSP check of the persona pages, 5 HTTP cycles, 1 for the persona burst), each signed out:
  its session row deleted; the audit row of `user_logged_in` and `last_login` remain, as after any sign-in. The
  in-process query count ran inside a transaction that was rolled back. Nothing else; `ile_v5`, `ile`, `ile_qa`
  untouched; the scratch test database dropped. My server and my connections: 0 at rest at the end.
- **Limits:** lane conditions — the dev server, uncompressed static, DEBUG. Performance PASS for product pages is
  8782's (§2.6), where the preview cannot run (its flag is unset there). Headless Chromium on Windows only: no
  WebKit or Firefox, no real phone. The burst client opens a socket per request, harsher on accept than a browser's
  six keep-alive sockets per host. Medians of n = 11 with their spread, judged against PFR §1's resolution; no other
  statistics.

## Evidence (E/w1-p/review-performance/)

`burst1_300x32.json` and `burst1_300x32_samples.csv`, the same for `burst2_300x32`, `burst3_300x64`,
`burst4_persona_300x32` · `framecap.json` · `timing1.json` (cold), `timing2_warm.json` (warm) · `persona_leak.json` ·
`persona_csp.json` · `stalled_body_probe.json` · `index_timing.json` · `pytest_perf_subset.log` ·
`console_outputs.txt` (first requests and warm latency, the iframe's insertion time, a waterfall, the frame-policy
matrix, the query counts, the ownership check) · `srv8791.log` (the server's own log) · `tools/` (every script above,
LF).
