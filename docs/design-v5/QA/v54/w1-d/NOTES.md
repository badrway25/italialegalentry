# W1-D · Motion and the loader «Lume» — implementation notes

The family's implementer (label w1-d-impl-1). Append-only: each step adds a dated section. Heavy evidence (captures,
probe logs) under `C:/tmp/ile_v5_council/evidence/v54/w1-d/` (E/ below), outside every repository; scratch tools under
`C:/tmp/ile_v5_council/.work/w1-d/w1-d-impl-1/`. Lane 7: dev server 8787 on `ile_v5_l7`, `ILE_REFERENCE_DATE=2026-10-03`,
`DB_CONN_MAX_AGE=0`, `--noreload`; pytest on `test_ile_v5_l7`; signed-in pages through sessions minted by
`Client.force_login` on `ile_v5_l7` (`mint_sessions_l7.py`, outside the repository; no password used, typed or stored;
`SESSION_COOKIE_AGE` is 8 h, so a sitting re-mints). Branch `v54-w1-d` from `v54-w1-a` (`304c587`); plan
`docs/design-v5/V5_4_EXECUTION_PLAN.md` §1.5, §1.9, §3.3 item 6, under V5.5 delivery mode (implement → review once →
fix → ship; no council, no scoring cycle). Until its own family passes, every page is «V4 + fondation» (plan §2.1).
Commits of 5 October carry «Co-Authored-By: Claude Opus 5.5»; those of 8 October «Claude Fable 5.1» — the model that
wrote each.

---

## Step 1 of 2 — the motion foundation (5 October 2026; resumed 8 October after a usage cut)

### What was done — the commits, oldest first

| Commit | What |
|---|---|
| `d158e1d` | `static/js/src/motion.js`: **the one gate** `reducedMotion()` (the setting, read live, or the preview's `html.rm`), `onReducedMotionChange()`, `withMotion()`, and the gated helpers `play()` (WAAPI), `nextFrame()`, `afterPaint()`, `tween()`; `settled()` waits on the animations really running, raced with a timeout (default 1000 ms) — never on `transitionend` / `animationend`; `durationToken()` / `easingToken()` read the tokens for WAAPI. `console.js`'s two-frame wait → `afterPaint()`; `situation.js`'s private media query, Motion import and frame wait → the gate. Bundles rebuilt from a clean `static/js/dist`: one shared chunk instead of three, +0.1 KB gzip per page, two fewer script requests |
| `07fb183` | `static/js/head.js`: the input modality — `html[data-input]` is `key` after a navigation key (Tab, arrows, Home / End, Page Up / Down, Enter, Space, Escape, the context-menu keys, Ctrl / ⌘ K), `pointer` after a press or a mouse movement; absent until the first input, written only on a change, untouched by typing (R-07, tier 0) |
| `e62805e` | **Reduced motion is a state**: V1's universal `0.01ms !important` block leaves `static/css/components.css` (two targeted guards stay: `.reveal` visible; the menu-panel and `dialog` keyframes off); `static/css/v5/tokens.css` zeroes **every** duration it declares under the setting — `--motion-key`, `--motion-door`, `--motion-luce` and the two staggers too, since nothing in V5 loops — keeping `--motion-wait` (a threshold) and `--motion-reduced` (the one 80 ms opacity, MS-O4); `html.rm` declares exactly the same list (MS7) |
| `419d787` | Tests: `test_script_motion_gate.py` (one gate; no `.animate(` / `requestAnimationFrame` outside motion.js's gated helpers; Motion only through motion.js; no wait on a transition or animation event in any product script); `test_rm_flag_parity.py` (under the flag every custom property resolves as under the setting; the twin is the media block exactly — it prints the block to paste); `test_v5_tokens.py`'s reduced-motion rule (every duration token at 0 ms, thresholds and `--motion-reduced` kept, the legacy names follow; `--motion-reduced` on opacity inside a reduced-motion block only; `test_v4_tokens.py:90` retired into it); `test_design_docs.py`'s motion half retargeted; `test_reduced_motion_w1_d.py` (browser: nothing moves at rest under the emulated setting on the home, a door, the login and the console at 1440 and 390; the flag gives the setting's tokens; the helpers' contract in a page; head.js's modality) |
| `6a3771e` | Merge of `design-v5` — the clock fix (`2e3d602`, `e16e811`) and W1-K's calibration record (8 Oct) |
| `7dab286` | Merge of `v54-w1-a`'s four newer commits (the «no page worse» corrections in `v5/base.css`, A11Y §13 G-15 on `v5/fonts.css`, DS 2026 §2's row, its own design-v5 merge). Only conflict: the binary `static/css/dist/main.css`, resolved by rebuilding from the merged sources (`npm run build:css`; the other dist sheets came out byte-identical). The merge base with `v54-w1-a` is now its tip, so `scripts/check_ownership.py w1-d v54-w1-a` lists W1-D's own diff |
| `716f494` | `docs/ACCESSIBILITY.md` §7 rewritten for the V5 rule; DS 2026 §3.19's reduced-motion row says the same in one cell |

### The rule as built (plan §1.5 «Reduced motion, built as a state») → where it lives

- **Tokens zeroed, not forced.** `v5/tokens.css` lines 482–499: the media block and its `html.rm` twin, fourteen names
  each. `--motion-reduced` is read in a reduced-motion block only and on `opacity` only (held by `test_v5_tokens`).
- **No universal `!important`.** `components.css` §29 keeps its two guards; `base.css` keeps `scroll-behavior: auto`.
- **One gate for script.** Every `.animate(` and `requestAnimationFrame` under `static/js/src/` sits in motion.js's
  exported helpers, each asking `reducedMotion()` first (held by `test_script_motion_gate`).
- **No hang at 0 ms.** State is set at t = 0 by the caller; `settled()` has a timeout; no product script contains the
  strings `transitionend` / `animationend` (the gate test scans `static/js/**` and `apps/*/static/**`).
- **The flag is not the state's evidence.** `html.rm` is for review; evidence is taken with Playwright
  `reduced_motion="reduce"` (the browser test and the lane probes).
- **The keyboard never animates.** `head.js` writes `html[data-input]`; each family adds its one rule
  `html[data-input="key"] <selector> { transition-duration: 0ms; }`.

### Measures

- **Static suites (8 Oct, after both merges, `test_ile_v5_l7`):** `test_rm_flag_parity`, `test_script_motion_gate`,
  `test_frontend_bundle_is_current`, `test_css_bundle_is_current`, `test_v5_tokens`, `test_v4_tokens`,
  `test_css_tokens_exist`, `test_design_docs`, `test_regen_design_inventory`, `apps/accounts` — the first run (before the
  `v54-w1-a` merge) was 674 passed, 1 failed on `test_cited_paths_exist` (`static/css/fonts.css`, removed by W1-A and
  re-cited until its `047e2e2`); after the merge and the rebuild: 581 passed (CSS currency and tokens) and 46 passed
  (the docs), 0 failed. `E/../pytest-targeted-*.log` in the scratch directory.
- **Lane 7, 5 Oct, `E/smoke-1/`** (`probe.json`, 59 captures): 221 page loads over the whole page-type list
  (public, account, console; fr and ar; 1440 × 900 and 390 × 844), 138 of them under the emulated setting — **0 running
  animations at rest, 0 elements or pseudo-elements with a transition or an animation longer than 0 s**; without the
  setting the same pages carry transitions (the probe reads something); `html.rm` gives the root the setting's tokens;
  `data-input` → `key` after Tab, `pointer` after a click. The only console errors are the three error pages reporting
  their own status (403 / 404 / 410).
- **Lane 7, 8 Oct, `E/smoke-2/`** (after the two merges and the lane server restarted on the merged code):
  the same probe (`probe_motion.py`, `probe.json`, 56 captures): **221 page loads, 138 under the emulated setting —
  0 running animations at rest, 0 moving elements or pseudo-elements**; no exception; the only console errors the
  three error pages' own status; under `html.rm` the root reads `--motion-fast` / `-standard` / `-key` / `-stagger` /
  `--spring-snappy-duration` / `--motion-base` / `--duration-base` = `0ms` with `--motion-wait` 400 ms and
  `--motion-reduced` 80 ms kept, exactly the setting's values; at rest without the setting 120 / 200 / 1200 / 60 /
  470 / 200 / 200 ms; `data-input` → `key` after Tab, `pointer` after a click (home and person dashboard). Identical
  to the 5 October numbers: the two merges changed nothing the probe reads.
- **Browser tests (8 Oct, `-m browser -rs`, `test_reduced_motion_w1_d.py` + `apps/portal/tests/test_browser.py`):**
  **15 passed, 0 skipped, in 136 s** (`pytest-browser-1.log`, run behind the lock after smoke-2): the reduced-motion
  state in Chromium (nothing moves at rest under the emulated setting on the home, a door, the login and the console at
  1440 and 390; the same pages carry transitions without it; the flag gives the setting's tokens; the helpers' contract
  from the built bundle under both settings; head.js's modality) and the portal browser tests, the no-JS submit among
  them.
- **Interaction smoke on the merged code** (`probe_interact_smoke2.py`; `E/smoke-2/situation_step2_fr_1440_*.png`):
  the wizard's «Continuer» swaps the question — 14 animations mid-swap under no-preference, 0 under reduce — and leaves
  no `style` attribute behind, the hash follows (`#q-nationality`); the rail toggle flips `data-rail` open → closed in
  both; from the bundle, `play()` returns an animation / null, `tween(300)` runs 19 frames / lands in one call,
  `afterPaint()` 34 ms / 0 ms, `settled()` 0 ms on a 0 s transition, `durationToken('--motion-fast')` 120 / 0,
  `easingToken('--ease-turn')` = `cubic-bezier(.77, 0, .175, 1)`, the gate true under the flag; no console error.
  One reading to know about: `body.is-ready` (the console's «the rail's width moves only after the first frame») read
  **false right at `networkidle` under no-preference** in that probe. Traced (`probe_ready.py`, `raf_diag.py`):
  headless Chromium can defer the first frame after a navigation while nothing invalidates — a plain
  `requestAnimationFrame` requested at `load` on the public home did not run for 1.5 s and then ran in 8 ms; on the
  console in the same diagnostic it ran in 6 ms and `is-ready` was true at load. It is the same two-frame wait as
  before W1-D (`afterPaint()` is the former nested `requestAnimationFrame` pair plus one microtask); under reduce the
  class is set synchronously. Not a defect — a transition that waits for the first paint is the intent, and a headed
  browser paints continuously — but a probe must wait a frame before reading it (the browser test waits 600 ms).
- **Looked at** (`E/smoke-2/`, under the setting): `home_fr_1440`, `home_fr_390`, `home_ar_1440`, `login_fr_1440`,
  `dashboard-person_fr_390`, `documents-portal_fr_1440` — every page at its still: the hero's stage and the four
  entrances fully drawn with their lines, the key held; the Arabic home mirrored in layout with the stage unmirrored;
  the login stage lit and still beside the form; the console rail and the phone bar at their final geometry; nothing
  left invisible by a stalled reveal or a counter. Without the setting, at rest after 1.2 s: `home_fr_1440_no-preference` is pixel-for-pixel the same picture as
  under the setting (the hero's one-shot has landed on the same still); `door-companies_ar_390_no-preference` shows
  the RTL chrome (menu on the inline start, brand on the inline end), the Arabic eyebrow and breadcrumb over the
  locked French copy, no overflow.

### Ownership — for the steward's merge step (`scripts/check_ownership.py w1-d v54-w1-a`)

- **Inside:** `static/js/src/motion.js`; `tests/frontend/test_{script_motion_gate,rm_flag_parity}.py`;
  `tests/frontend/test_reduced_motion_w1_d.py` (the per-family glob); `docs/design-v5/QA/v54/w1-d/**`.
- **Slices, as the manifest names them:** `static/js/head.js` (the modality flag only); `static/css/components.css` (the
  universal reduced-motion block only); `tests/frontend/test_design_docs.py` (the motion half of
  `test_focus_and_motion_claims_match_the_stylesheets`); `tests/frontend/test_v4_tokens.py` (the retired reduced-motion
  test); `tests/frontend/test_v5_tokens.py` (the reduced-motion rule, two tests and their helpers);
  `docs/ACCESSIBILITY.md` §7; `docs/design/DESIGN_SYSTEM_2026.md` (§3.19's reduced-motion row — «the prose of the
  reduced-motion rule»; §12 untouched, it is W1-A's in Wave 1).
- **Justified extra paths — the manifest entries to add at the merge, not to ignore:**
  1. `static/css/v5/tokens.css`, the reduced-motion block and its `html.rm` twin only (`e62805e`). Plan §1.5: «the
     duration tokens are zeroed in the `prefers-reduced-motion` block» is W1-D's rule, and W1-A's own DS 2026 §12 note
     hands it over («L'uso della regola … e i suoi test sono di W1-D»). Not an appended named block: the rewrite of the
     one block W1-A had written. Proposed slice: «the reduced-motion media block and its html.rm twin».
  2. `static/js/src/console.js`, one import and one line (`d158e1d`): the two-frame `requestAnimationFrame` wait before
     `body.is-ready` → `afterPaint()`. Required by `test_script_motion_gate` (no frame loop outside motion.js). W3-A owns
     the file later, W2-A its drawer code; this hunk touches neither. Proposed slice: «the is-ready frame wait».
  3. `static/js/src/situation.js` (`d158e1d`): Motion imported through `./motion.js`, the private media query →
     `reducedMotion()`, one `requestAnimationFrame` → `nextFrame()`. In no family's slice: the steward assigns it
     (proposed: W1-D, «the motion gate and frame wait», until W3-D's journey work takes the file).
- **Generated:** `static/js/dist/**` (rebuilt from clean), `static/css/dist/main.css` (rebuilt at `7dab286`).

### Decisions met during the build (for the CD's DL54 entries; none needs the owner)

- **Every duration token lands at 0 ms** — `--motion-key`, `--motion-door`, `--motion-luce` and the two staggers
  included. W1-A's §12 note had kept the three signature durations «because a 0 ms loop spins on itself»; nothing in V5
  loops (plan §1.5 «Nothing loops»), and a one-shot at 0 ms lands on its still, which is the designed state.
- **`settled()`'s default timeout is 1000 ms**, above the longest tier-2 sequence (600 ms) and below any wait a person
  would notice; a caller that waits on the loader passes its own.
- **`head.js` writes the modality only on a change**, treats Ctrl / ⌘ K as a key and never reacts to typed text; the
  attribute is absent until the first input, so a page that is never touched carries no state.

### What is left

**Step 2 — the loader «Lume» (plan §1.9; the whole of it):** `static/js/src/loader.js` (one state machine rest → engaged
→ open → rest, a singleton, `MIN_SHOWN` 480 ms, words at 1 s and 10 s with «Réessayer», nothing loops), imported
dynamically by `shell.js` on the first submit; `static/css/v5/loader.css` (L2 and L3, in `main.css`);
`scripts/gen_loader_light.py` → `static/css/v5/_loader-light.css` (the L1 release's generated light sheet, with its
currency test, imported by the console entry only); `templates/components/{loader,busy_key}.html`; the one shared
key-turn primitive (the `.sig__l` layers, `--ease-turn`, rotateY about the shaft; the key is never held, drawn or served
mirrored — DL54-08); `initMisc`'s submit guard → L2 in `static/js/main.js`; the release — a `user_logged_in` receiver in
`apps/accounts/signals.py` setting a session flag, consumed once by the first console page on the rail's mark (below
64 rem, the top bar's mark), never over painted content, its end state shown without travel under reduced motion; the
release hook in `templates/partials/portal_chrome.html` and the `_loader-light.css` import line in
`apps/portal/static/portal/console.css`; L1 only in its allow-listed templates and never on an `OUTCOME_BEARING` form;
L3 only on fragment containers; `test_loader_rules.py`; the specimen `templates/dev/designpreview/specimens/loader.html`;
the one-line pointer to DL54-07 in BA §1; the muddy grey-beige fix at +40–80 ms before any measurement; the ten
re-measurements of `surfaces.md` §3.3 under the lock, the three fallback conditions read on filmstrips at 1× and 0.25×.
Note for step 2: `will-change` «removed on `animationend`» (plan §1.5) must be done on the run's `animation.finished`
(or `settled()`), since the gate test refuses the event's name in any product script.

**Honest limits of step 1:**
- `static/js/main.js` (V1) still reads the media query itself for `.reveal` and the counters and does not read
  `html.rm`: `initReveal` is W4-B's slice; the counters' `requestAnimationFrame` has no owner in the manifest — the
  steward should assign it (W4-B with the reveal is the natural seat). Under the flag their *tokens* are zeroed, so the
  reveal lands at once; only the counters would still count under the flag (not under the setting).
- DS 2026 §12's V4 paragraph on the «tre livelli» (≈ lines 2740–2750: `components.css` §29's `0.01ms !important`,
  «resta esattamente com'è scritto») is stale; §12 is W1-A's in Wave 1. Proposed replacement, for the steward or
  W1-A to paste as a dated blockquote at the top of §12: «**Design V5 (8 ottobre 2026, W1-D)** — il moto ridotto è uno
  stato, non un interruttore: `static/css/v5/tokens.css` azzera ogni durata V5 nel blocco `prefers-reduced-motion:
  reduce` e `html.rm` ne è il gemello di revisione; la rete di sicurezza universale `0.01ms !important` di
  `components.css` §29 è stata rimossa (restano le due guardie di `.reveal` e dei keyframe di mega-menu e `dialog`);
  `--motion-reduced` vale per la sola opacità di un overlay; il moto via script passa dall'unico cancello
  `static/js/src/motion.js` (`play`, `nextFrame`, `afterPaint`, `tween`, `settled` con timeout); `static/js/head.js`
  scrive `html[data-input]` perché la tastiera non animi (R-07). Regola e misure in `docs/ACCESSIBILITY.md` §7.»
- No person has watched the motion at speed (plan §1.5 — the honest limit stands until the owner has).
- The specimen board `specimens/loader.html` does not exist yet (step 2).
---

## Step 2 of 2 — the loader «Lume» (8 October 2026; finished 9 October after a network outage)

Lane 7 as in step 1; evidence `E/step2/` (the 8 October series: `release/`, `smoke-3/`) and `E/step2/final/` (9 October,
on the final sources: `release/`, `l2_board/`, `submit/`, `trace_delta/`, `cls/`, `l1_words/`); the probes under the scratch
directory (`probe_release.py` + `probe_release_analyse.py`, `probe_l2_board.py`, `probe_submit_timing.py`,
`probe_trace_delta.py`, `probe_cls_sources.py`, `probe_l1_words.py`, `mint_sessions_l7_multi.py` — several sessions per
persona, because the first console page of each consumes the release). Signed-in pages through `Client.force_login`
sessions on `ile_v5_l7`; the login's submit measured with the form EMPTY (allauth answers the page again with its field
errors): no credential of anyone was typed. Commits of 8 and 9 October carry «Co-Authored-By: Claude Fable 5.1».

### What was done — the commits, oldest first

| Commit | What |
|---|---|
| `fa07163` | `static/css/v5/loader.css` — **the mark in layers** (`.sig` host in mark units, `.sig__l` layer formula, the base / room / key layers from one origin, pixel-identical to the one-file mark at rest) and **the key-turn primitive** (`.sig__turn`, `sig-turn` 0 → 360° about the shaft on `--ease-turn`; the host `direction: ltr`, never held, drawn or served mirrored — DL54-08); **L2** drawn on every `.btn.is-busy::after` (key.svg as a mask in the button's own ink, inside the inline-end padding, one turn of `--motion-emphasized`, dim 55 % → lit); **L3's seat** (`[data-seat].is-seating > *`, 4 px on `--motion-standard`, `--motion-stagger` apart, capped at the 8th row); forced colours (the mark keeps its colours, no light, no ink; the busy key in `ButtonText`). `scripts/gen_loader_light.py` → `static/css/v5/_loader-light.css`, the release's generated sheet, imported by `apps/portal/static/portal/console.css` only; `v5/loader.css` imported by `static/css/main.css` after `v5/base.css` |
| `4abca6d` | **The release is served, not scripted**: `apps/accounts/signals.py` (`mark_entrance_release` on `user_logged_in`, connected in `AccountsConfig.ready` with a `dispatch_uid`; `consume_entrance_release` pops the flag), `apps/accounts/templatetags/entrance.py` (`{% entrance_release as lume_release %}`), the hook in `templates/partials/portal_chrome.html` (the rail's tile, and below 64 rem the top bar's, render `components/loader.html` with `release=True` once; every later page and the drawer keep the `<img>`); `templates/components/loader.html` (the layers, the contract, the words passed in by the including template) and `templates/components/busy_key.html` (L2 as markup for a row that waits) |
| `a205ad7` | `static/js/src/loader.js` — the state machine (busy / settle / rest; engage with the word at 1 s and the sentence + «Réessayer» at 10 s; release of an in-page host; seat; `MIN_SHOWN` 480; `OUTCOME_BEARING` refused; a singleton; the one wait on motion through `settled()`); `shell.js` sets `.is-busy` + `aria-busy` in the submit's own task on every form of the site and imports the loader then, never before; `initMisc`'s guard refuses the second submit and sets `aria-disabled`, never `disabled`; bundles rebuilt from clean |
| `29ca5aa` | `tests/frontend/test_loader_rules.py` (the generated sheet current; nothing loops, one duration token per phase, no typed duration, every literal curve a declared `--ease-*`; L1 only in its allow-list and never on an outcome-bearing form; L3 on no server-rendered region; the release's two seats with the `<img>` elsewhere; the console import first and never in `main.css`; the scripts' constants, the singleton, the dynamic import; the layers verbatim; the busy key without markup), `tests/frontend/test_loader_w1_d.py` (the flag through allauth's real sign-in, `force_login` and a refused sign-in; a public page neither shows nor consumes it; the Arabic console; in Chromium the release once at load and the rest after, the still under the setting, the busy face in the click's task); the two cascade pins admit the V5 component sheets; W1-P's index links the board |
| `bbdc6c4` | The filmstrip board `/__design-v5/specimens/loader/` (`templates/dev/designpreview/specimens/loader.html`, `static/css/dev/loader-board.css`): every live cell plays once at load, the frames are the product's own animations paused at t, a real GET submit for L2 |
| `5a0d390` | DS 2026 §2 (`loader.css`), §10 (`loader.html`, `busy_key.html`), §12 (`sig-turn`, `sig-seat`, the release's keyframes), §16 (`loader.js`; `initMisc` without `disabled`); A11Y §7 (the loader's stills, 2.2.2, 2.3.1, 4.1.3, focus, forced colours); BA §1's pointer to DL54-07; DL54-20 (the build decisions), DL54-21 |
| `dd20d3f` | **The review-once fix (9 Oct):** the light **withdraws into the key's eye** on the way out (scale 1 → 0.08 on `--ease-sine`, 1000 → 1400 ms; opacity 1 until 1320, gone at 1400 over the bow alone) instead of fading over the navy — the 8 October filmstrip showed the grey-beige of LS §6 on the way out; the key reads in ink from 40 ms (the moment the light is under it) to 1360. One phase, the same three animations and tokens. DL54-20 addendum; `test_the_generator_is_the_plan_s_phase` holds «the light leaves the way it came» |
| `03779e0` | Merge of `design-v5` (W1-A shipped, `474ced9`): documents, the manifest, W1-A's QA records; no conflict, the dist already identical |

### The loader as built → where it lives (plan §1.9)

- **L1, the release** — served by the first console page after a successful sign-in, once per session, on the rail's
  mark (below 64 rem the top bar's), as a CSS animation that starts at the first paint with or without script, never
  over painted content (the tile is a 40 × 40 fixed seat; the `<img>` → layers swap is server-side). Refused sign-in →
  no flag → the error page at rest (`test_a_refused_sign_in_leaves_no_flag`). Public pages never download the sheet.
- **L1, the engage** — the primitive and the machine ship (`.sig.is-engaged .sig__turn` on `--motion-slow` /
  `--ease-turn`; `loader.js` `engage()`, the words, «Réessayer», `release()`); **the login's wiring is W2-B's** (plan
  §3.3 item 6: «the login's engage is wired by W2-B on W1-D's primitive»). What W2-B adds: the `.sig` host with an `id`
  in the stage (`{% include "components/loader.html" with id="…" word="…" slow="…" retry="…" %}`, its own
  translations) and `data-loader-host="<id>"` on the login's form; `test_loader_rules` already allow-lists
  `templates/allauth/layouts/entrance.html`. Today the login's submit shows L2 on the CTA — the neutral gesture.
- **L2** — on every submit button of the site, without markup; `aria-busy` in the click's task, `aria-disabled` 300 ms
  later from `loader.js`; the focus stays; a page back from the cache is at rest.
- **L3** — the primitive (`seat()` + the sheet) and the board. **No product region fetches asynchronously today** (no
  `fetch(` in any product script): the Wave-3 families attach `data-seat` to their containers (RTD-m2 held by
  `test_l3_attaches_only_to_fragment_containers`).
- **Reduced motion is the still**: every token the loader moves on is 0 ms under the setting (and under `html.rm`);
  `fill-mode: both` lands each layer on its last keyframe = the rest; the words at 1 s and 10 s still come (timers, not
  motion); `MIN_SHOWN` still holds (a floor against flicker, not motion). **Forced colours**: no light and no ink, the
  mark in its own colours, the busy key in `ButtonText`. **RTL**: the host is `direction: ltr` in every locale; the busy
  key sits at the inline end (left in Arabic).

### Measures — 9 October, lane 7, the final sources (`E/step2/final/`)

**The release's three conditions** (plan §1.9; frames every 40 ms of animation time by pausing and seeking the host's
animations — deterministic, 41 frames per case — the host clipped at device scale 4; `probe_release_analyse.py`:
interior x 78.5–121.5 / y 82.5–153.5 in mark units, the doorway's stroked box outside it):

| Seat (served size) | 1 · visibility: changed > ΔE00 6, hold ≥ 0.5 of the interior | 2 · muddy tone 40–120 ms (C* at 0 / lit / early / dip) | 3 · glow outside the doorway | rest vs the `<img>` mark |
|---|---|---|---|---|
| rail, 24 px, ×4 (680 px) | peak 0.91, **hold 1240 ms** (40–1240) — PASS | 25.6 / 23.5 / 31.7 · 29.1 · 26.7 / −3.2 — PASS | max ΔE00 **0.00**, 0 frames — PASS | max channel 5/255, 0 px > 8 of 16 384 |
| bar, 20 px, ×4 (504 px) | 0.83, 1240 — PASS | 25.0 / 20.4 / 29.8 · 27.6 · 23.0 / −2.6 — PASS | 0.00 — PASS | max 15, 2 px > 8 of 12 544 |
| rail, 24 px, ×1 and ×2; ar; the company persona | 0.96 / 0.91, 1240 — PASS | dip −10.7 / −4.5 — PASS | 0.00 — PASS | max 4 (×1), 8 (×2); 0 px |
| bar, 20 px, ar 390 ×1; 200 % zoom (720 × 450 @ 2) | 1.00 / 0.92, 1280 / 1240 — PASS | dip −7.1 / −4.3 — PASS | 0.00 — PASS | 2 px of 784 / of 3136 (antialiasing at 20 px) |
| reduced motion (1440, 390); forced colours | no light, no ink: durations 0 s / `animation: none` — the still, by design | — | 0.00 | the still = the `<img>` (max 4 / 12) |

No fallback condition fired; «Mandata»'s frame light stays unused. The second page of every session carries the
`<img>` and no `data-lume` (11 of 11 cases).

**The muddy tone, before and after the exit fix** (muddy = chroma more than 5 C* below the lower end colour AND
30 < L < 80, the cream-over-navy blend; the fraction of the interior): rail ×4 — on the way in max 0.12 → 0.14 (the
feathered rim), **on the way out 0.785 → 0.129**; bar ×4 — 0.095 → 0.137 in, **0.770 → 0.137 out**. Before, frames
1160–1240 ms were grey (`E/step2/release/frames_fr_1440_x4`, and the side-by-side
`final/release/exit_before_after_fr_1440_x4.png`); after, the cream disc shrinks into the bow with the navy returning
around it. The 1× cases read 0.375 in every frame including the still: the white stroke's antialiased pixels, the
measure's floor at that size.

**Cost at CPU ×4** (`probe_trace_delta.py`, 3 cold contexts per arm, the dashboard, `devtools.timeline` +
`blink.animations`): busy main thread in the 2 s after first paint **with** the release 563 / 700 / 742 ms, **without**
569 / 578 / 277 (median +131 ms, inside the arms' own spread of ±230); inside the hold (400–1000 ms, when only the
light moves) 70 / 65 / 98 vs 74 / 73 / 57 ms busy, 11 / 10 / 14 vs 12 / 12 / 12 main frames, **36 compositor frames in
both** (60 fps); Animation trace events 33 vs 24 — the release's nine — **compositeFailed 0**; the longest task 119 ms
with vs 228 ms without: the dashboard's own load tasks at ×4, present in both arms; none attributable to the loader.
Running animations: 3 right after commit, 0 at 2.4 s; under the setting 0 and 0 s.

**CLS**: 0 in the three attributed runs (1440 ×4, 1440 ×1, 390 ×4: no layout-shift entry, fonts loaded, the rail tile
at 12, 12, 40 × 40) and in the live 390 and reduce runs; one earlier 1440 ×4 run read 0.0014 (one entry) that did not
reproduce — not the mark, whose seat is fixed.

**L2 on a real submit** (`probe_l2_board.py l2`, the login, scale 3: fr 1440, fr ×4, ar, 390, reduce, forced colours,
200 % zoom): in the submit's own task `is-busy` + `aria-busy`, the focus on the control, button width / height delta 0,
label delta **0 px**, `sig-turn` 0.32 s × 1 on `cubic-bezier(0.77, 0, 0.175, 1)` (0 s under the setting), the key box
7.66 × 18 px at opacity 0.55, the mask key.svg; the handler 2.3–3.6 ms (20.5 at ×4); 300 ms later `aria-disabled`,
`data-submitted`, the second submit refused; the label white on the primary (black `ButtonText` under forced colours);
0 long tasks. **The label's raster** at rest vs busy (clipped at scale 2): **0 of 8 944 device px differ** (fr; ×4;
reduce) and 0 of 12 720 (ar) — the key's `perspective` re-rasters nothing. **INP proxy** (Event Timing on a real click,
`probe_submit_timing.py`): 32 ms at ×1, 64 at ×4, 24 under the setting, 32 in Arabic.

**Submit → the next page's first paint** (§3.3 item 8, the empty login form, N = 4 each, alternating): no-preference
140 / 105 / 112 / 114 ms, **median 113**; under the setting 130 / 120 / 149 / 121, **median 126**; `responseStart`
medians 53 / 55 ms; every answer 200 with the four field errors at rest, no busy class left. The key delays nothing.

**The state machine, live** (`probe_l1_words.py` on the console page, the built module imported, a host built as an
including template writes it): `engage()` refused on `eligibility` and for a second host while one is engaged; at
t = 0 `is-engaged`, `sig-turn` 0.48 s × 1 on `--ease-turn`, 1 animation running; at 700 ms the transform is the
identity and nothing runs (one turn, then the hold); at 1.15 s `is-worded` and the word announced; at 10.15 s `is-slow`,
the sentence, «Réessayer» shown, the control still busy; the retry leaves host, form (`data-submitted` gone) and
control (no `aria-busy`, no `aria-disabled`) at rest, and a new engage is accepted; `release()` resolves in 1617 ms
with the light at 0 and the classes gone; `settle()` 616 ms (the 480 ms floor + the lit fade); `seat()` on nine rows:
delays 0 … 0.42 s (capped at the 8th), 0.2 s each, resolved in 632 ms, a second arrival 0 ms and no seat. Under the
setting: the same states, every motion 0 s, release 31 ms, settle 480, seat 0.

**The board** (`/__design-v5/specimens/loader/`, the lane briefly on `ILE_DESIGN_PREVIEW=1`, then back): 1440, 390,
reduce, forced colours, 200 % zoom — 200, 33 hosts, **0 running animations 2.2 s after load**, 80 paused frames (32
under forced colours: the release frames are `none` there), 10 busy buttons, **0 console errors**, no horizontal
overflow, the CSP header on.

**Bytes** (gzip −9): `loader.js` 1 193 B (new, loaded on the first submit only); `shell.js` +95 B; `v5/loader.css`
3 854 B → `main.css` 42 685 → 43 923 B (+1 238); `_loader-light.css` 1 299 B → `console.css` 2 687 → 2 936 B (+249).
«Mandata»'s research sheet was 2.5 KB.

**Looked at** (`E/step2/final/`): the console at t = 360 ms in fr and ar at 1440 (the mark lit in the rail's tile, the
Arabic layout mirrored with the mark unmirrored), at 390 and at 200 % zoom (the top bar's tile), under forced colours
(the mark in its colours, no light); the two 4× filmstrips before and after the exit fix; the L2 key frames at 0 / 80 /
160 / 240 / 320 ms (upright → edge-on at 160 → upright; white at 55 % on the teal); the login busy in fr, in ar (the key
at the left end of the RTL button) and under forced colours (black key in the outlined button); the refused sign-in at
rest with its error summary; the board at 1440, 390 and forced colours.

**Smoke on the whole page-type list**: `E/step2/smoke-3/` (8 Oct, the step-2 sources — only the exit keyframes differ
from today's, which the release series above re-measured): 221 loads, 138 under the setting, **0 running animations at
rest, 0 moving elements**, no console error but the three error pages' own status.

**Tests**: static targeted set (`pytest-targeted-3.log`, before the exit fix): **685 passed, 0 failed** (loader rules,
rm parity, script gate, both bundle currency tests, loader w1-d, v5 tokens, design docs, `apps/accounts`); after the
fix the loader rules 12 / 12 with the new «leaves the way it came»; on the merged code `pytest-targeted-4.log`:
**982 passed, 0 failed** in 254 s (the same set plus `test_design_preview.py`). Browser (`-m browser`): the first run (`pytest-browser-2.log`, concurrent with the board phase and two
lane restarts) 18 passed, 2 failed — its detail was lost to my own `tail`; the re-run on the merged code
`pytest-browser-3.log`: 18 passed, the same 2 failed — `test_the_release_plays_once_at_load_and_lands_on_the_rest[1440]` and `[390]`, written minutes
before the outage and never run until today: at 390 it waited for the release host to be *visible*, and the first match is
the rail's, not displayed below 64 rem (now `state="attached"`); at 1440 it expected two `<img>` marks on the second page
where the chrome has three (the drawer's tile is a `.rail__tile` too and always keeps the `<img>`, as the Django-client
test already said). The product was right, the test was not; corrected in `tests/frontend/test_loader_w1_d.py` and re-run:
`pytest-browser-4.log` **5 passed** in 37 s — with the 18 of `pytest-browser-3.log`, the browser set is **20 / 20** (the
reduced-motion state, the release once at load and the still, the busy face in the click's task, the portal's browser
tests with the no-JS mark-as-read submit).

### Ownership — for the steward's merge step (`scripts/check_ownership.py w1-d design-v5` after `03779e0`: 14 inside, 13 slice, 12 generated, 10 outside)

- **Inside:** `static/js/src/{motion,loader}.js`; `static/css/v5/{loader,_loader-light}.css`; `scripts/gen_loader_light.py`;
  `templates/components/{loader,busy_key}.html`; `templates/dev/designpreview/specimens/loader.html`;
  `tests/frontend/test_{loader_rules,loader_w1_d,reduced_motion_w1_d,rm_flag_parity,script_motion_gate}.py`;
  `docs/design-v5/QA/v54/w1-d/**`.
- **Slices, as the manifest names them:** `apps/accounts/signals.py` (the release flag); `apps/portal/static/portal/console.css`
  (the import line); `templates/partials/portal_chrome.html` (the two tiles' hook and the `{% load %}` / `{% entrance_release %}`
  lines); `static/js/main.js` (`initMisc`'s guard + its `pageshow` reset); `static/js/head.js`; `static/css/components.css`;
  A11Y §7; BA §1's pointer; DL54's own entries (DL54-20 + addendum, DL54-21); DS 2026 (the loader's prose in §2, §10, §12,
  §16; §12's inventory lines are the steward's to regenerate); `test_v4_tokens.py`, `test_design_docs.py`, `test_v5_tokens.py`.
  **Two slice overreaches to check:** in `test_design_docs.py` and `test_v5_tokens.py` the cascade pins
  (`test_breakpoints_keyframes_and_stylesheets_are_documented`, `test_v5_closes_the_cascade_and_reaches_the_browser_in_the_bundle`)
  now admit V5 component sheets after the four foundation sheets (plan §2.3's order) — 4 + 3 lines, needed by the
  `v5/loader.css` import; W1-A's functions otherwise untouched.
- **Justified extra paths — manifest entries to add at the merge, not to ignore:**
  1. `apps/accounts/apps.py` — the receiver connected in `ready()` (7 lines); `apps/accounts/templatetags/{__init__,entrance}.py` —
     the consumer tag. In no slice: the release flag's own plumbing (plan §3.3 item 6 names `signals.py`). Proposed: W1-D,
     «the entrance release's receiver and tag».
  2. `static/js/src/shell.js` — the submit hook (one listener, the dynamic import). Plan §2.3 / §2.2: «the loader and the
     navigation load through shell.js». W2-C1 owns the file later; the hunk is a separate section. Proposed slice: «the
     submit hook of the loader».
  3. `static/css/main.css` — one import line, `v5/loader.css`, after `v5/base.css` (plan §2.3's order; the serialized
     table gives W1-A Wave 1 — W1-A has shipped).
  4. `static/css/dev/loader-board.css` — the board's dev sheet (never in the cascade; `test_the_dev_stylesheet_stays_out_of_the_production_cascade`).
  5. `tests/frontend/test_design_preview.py` — two lines: W1-P's index links the board the moment its template exists.
  6. From step 1, unchanged: `static/css/v5/tokens.css` (the reduced-motion block and its `html.rm` twin),
     `static/js/src/console.js` (the `is-ready` frame wait), `static/js/src/situation.js` (the motion gate and frame wait).
- **Generated:** `static/js/dist/**`, `static/css/dist/**` (rebuilt from clean; `console.css` rebuilt at `dd20d3f`).

### Decisions met during the build (DL54-20, its addendum, DL54-21 — none needs the owner)

The release served, not scripted (the flag + the tag); one phase `--motion-door` with the ramp over the bow alone and,
since 9 October, the exit by withdrawal; L2 drawn by CSS with no markup, its «260 ms» = `--motion-emphasized`, `aria-disabled`
never `disabled`; L3's «40 ms» = `--motion-stagger`; the engage's 480 ms = `--motion-slow`, a keyboard submit plays the
same turn (an activation, not a navigation key — the reviewer may rule otherwise with one `html[data-input="key"]` rule);
the words belong to the including template; the layered mark rasterises as the one-file mark; every duration at 0 ms
under reduced motion.

### What is left, and the honest limits

- **The login's engage** is W2-B's wiring (above); until then the sign-in shows L2 on the CTA and the release on arrival.
- **L3 has no product container yet**; the primitive is measured on the board and live.
- **Method**: the filmstrips are deterministic seeks every 40 ms, not a 60 fps recording at 1× and 0.25×; the live runs
  confirm the clock (3 running after commit, 0 at 2.4 s). **No person has watched the motion at speed** (plan §1.5).
- **§3.3 item 2's «0 long tasks»** is not true of the dashboard page at CPU ×4 with or without the release (its own
  119–237 ms tasks); the release adds none that can be attributed and nothing inside the hold.
- **Item 9** (the text raster beside the stage) is measured for L2's label (0 px); the stage's is W2-B's to measure.
- **Item 10**: no Safari or Firefox exists locally — Chromium only.
- The identity at the bar seat shows 2 antialiased pixels of 784; at 200 % zoom 2 of 3 136 (max 32/255 on one edge).
- `DS 2026 §12`'s stale V4 «tre livelli» paragraph (step 1's note) is still W1-A's / the steward's to replace.

---

## Review fixes — the fix pass after the review-once and the accessibility check (9 October 2026; label w1-d-fix)

One pass, resumed twice: the same label's two earlier sittings (09:56–10:16) were cut and left 15 uncommitted files and no
evidence; this sitting read them, kept what was right, withdrew what was not (below), merged `design-v5` and finished.
V5.5: implement → review once → **fix** → ship. Reports read in full: `REVIEW.md` (0 blocking · 1 major · 5 minor) and
`A11Y_PERF.md` (0 blocking · 2 major · 4 minor). Lane 7 as before (8787, `ile_v5_l7`, `ILE_REFERENCE_DATE=2026-10-03`,
`DB_CONN_MAX_AGE=0`, `--noreload`); evidence `C:/tmp/ile_v5_council/evidence/v54/w1-d/fix/` (F/ below); probes and the
edit scripts under `C:/tmp/ile_v5_council/.work/w1-d/w1-d-fix/`. Commits carry «Co-Authored-By: Claude Opus 5.5».

### The commits, oldest first

| Commit | What |
|---|---|
| `1053f16` | Checkpoint of the two cut sittings, as found, so that the merge had one committed side to meet. Not kept: the sentence they had added to W1-P's `templates/dev/designpreview/index.html` (another family's file — handed over below) |
| `e94b7ff` | **Merge of `design-v5`** (`a906d6d`: 20 commits — the publication commits and W2-C1's navbar «Il portico»), both sides kept: `main.css` imports `v5/loader.css` then `v5/chrome.css` (plan §2.3's order); `shell.js` and `main.js` merged without conflict (the submit hook in the shell W2-C1 rewrote, the guard beside the navigation's move to `nav.js`); A11Y §7 keeps W1-D's section with W2-C1's sentence on the portico's 80 ms opacity; DS 2026 §2 / §16 rows united and the figures regenerated by `scripts/regen_design_inventory.py --write`; the two cascade pins take design-v5's wording; `dist/` rebuilt from clean. **DL54: W2-C1's DL54-20 … 25 reached design-v5 first, so W1-D's two entries are now DL54-26 (the loader as built) and DL54-27 (every duration at 0 ms), content unchanged — `REVIEW.md`, `A11Y_PERF.md` and the notes above cite them as «DL54-20» and «DL54-21»** |
| `11f0dfe` | **The merge's two meetings.** (1) W2-C1's `nav.js` predated the script motion gate — it asked the media query itself and called `requestAnimationFrame` (`test_script_motion_gate`; plan §1.5 names the architrave among the sequences that pass through the gate): it now imports `reducedMotion()` and `nextFrame()` from `motion.js` (three reads of the setting; the layout's frame, the last request winning) — so the preview's `html.rm` flag reaches the architrave and the panels too. (2) `v5/chrome.css` §9 keeps MS-O4's one fade under the setting: the reduced-motion rule of `test_v5_tokens` admits the discrete companion (`display … allow-discrete`) of an opacity fade, and `test_reduced_motion_w1_d` admits exactly that fade — opacity for `--motion-reduced` — and still fails on anything else that lasts |
| `812ac12` | **The review fixes**: `loader.js`, `shell.js`, `v5/loader.css`, the board, `test_loader_rules.py`, `test_loader_w1_d.py`, bundles |
| `6066676` | The fix in the family's prose: DS 2026 §2 / §10 / §16, A11Y §7, DL54-26's second addendum (rewritten: it described the first cut sitting's design, never merged) |
| `ff30c56` | `test_loader_w1_d`: Enter in a field makes the form's own button wait, the focus stays in the field |
| `c43ca82` | `loader.js`: «Réessayer» is listened to once per control, not once per long wait (a wait that ended by itself left a `once` listener behind; the next long wait added a second) |

### Finding → change → evidence

| Finding | Change | Evidence (F/`final/…`) |
|---|---|---|
| **REVIEW M1 (major)** — a form whose answer does not replace the page keeps `is-busy`, `aria-busy`, `aria-disabled` for ever (the account's «Exporter mes données (JSON)»); A11Y cross-reference: 4.1.3, a state announced that never ends | **No wait is for ever.** `shell.js`: a form `data-loader="none"` (the export form, `templates/accounts/profile.html`), a form with a `target` or `method="dialog"` never waits and loads nothing; only a `.btn` waits; the control is the event's submitter itself. `loader.js`: a wait is a **lease** — `SLOW_AFTER` (10 s, the loader's own timeout, the moment «Réessayer» is offered) plus the time the form's files need at 16 KiB/s — at whose end the form is at rest and can be sent again; where a host offers «Réessayer» the person decides (the lease stays on the books until the retry or a return from the cache). A submit cancelled by a listener after the hook (an answer in the page) is at rest in the next task. `pageshow` (persisted) puts everything at rest in `loader.js`, `shell.js`, `main.js`. No event tells a script that an answer was a download or a 204: hence the declaration for the known case and the lease for the rest | `wait/wait.json`. **B1** the declared export, fr and ar: 2 downloads each, no class, no `aria-busy`, cursor `pointer`, 0 requests for `loader.js`. **B2** a file nobody declared (the profile form answered with an attachment): waiting at 1 s and 9 s, **at rest at 10.8 s**, focus kept, the next submit sent. **B3** 204 on the guarded login: `aria-busy` + `aria-disabled` + `data-submitted` at 1 s and 9 s, the second submit refused (0 sent), at rest at 10.8 s with the guard lifted, the third accepted; the same on the link-styled «Marquer comme lue». **B4** a submit answered in the page (guarded and not): busy in its task, at rest 300 ms later, the second accepted. **B5** a real slow page (4 s), fr and ar: busy, key drawn, focus kept at 0 / 60 / 400 / 1500 / 3000 ms, replaced at 4.1 s (`sheet_pending.png`). **B6** the real back/forward cache: `/fr/orientation/` left busy (`pagehide persisted=true`), back with `pageshow persisted=true` **at rest**, restored from the cache (page state kept), the next submit waits again; the login (`no-store`) is not cached and reloads at rest. **B7** an upload of 64 KiB: waiting at 10.8 and 13.2 s, at rest at 14.8 s. **B8** an L1 host with its words: the word at 1.2 s, the sentence and «Réessayer» at 10.4 s, the control still waiting at 13 s; the retry → host, form and guard at rest, focus on the submit control; a second long wait and a second retry behave the same |
| **A11Y 1 (major)** — the busy key's dim face reads 2.69 : 1 on the primary (WCAG 1.4.11: it is the one visual indicator of the state) | The dim face is **80 %** of the button's ink (`.btn.is-busy::after`, `.busy-key`). The check proposed 65 % (3.2 on the teal); 80 % was taken because the indicator must hold on **every variant**: today V4's busy rule gives every busy button the primary's teal, but each variant's own ink and ground was read too, for the day a busy button keeps its surface (W1-C) — at 65 % the ghost's pair reads 2.9, at 80 % none is under 3.9 | `variants/variants.json`, `sheet_keyed.png`: **26 keyed cases on the real path** (table below) — key `rgb(207,227,229)` on `rgb(18,119,127)`: **3.97–4.0 : 1** (median of the fully covered pixels), **3.6 at the weakest pixel**; fr and ar; pointer, keyboard focus, tap; 1440 and 390. `board/board.json`: 10 samples × rest / pointer / focus = 30 measures, the same 3.97–4.0 (min 3.6), ghost and soft included; forced colours: `ButtonText` at 80 % on `ButtonFace`, 12.6 : 1. `own-pairs.json`: the variants' own pairs at 80 % — primary 4.0, secondary 8.3, danger 5.2, soft 4.5, ghost 3.9 (at 65 %: 3.2 / 5.0 / 3.7 / 3.2 / **2.9**) |
| **A11Y 2 (major)** — on a link-styled submit (`.btn--link`, `--btn-pad: 0`) the key box covers the label's last glyphs («Marquer comme lue») | **Where the key has no place there is no key** — the second of the two options («omit it there and keep `aria-busy`»), and DS V5 §10.1's own table (LINK: no loading face). `shell.js` gives the `.btn` variants without inline padding — tertiary, link, text, inline, icon: `KEYLESS`, read by `test_loader_rules` against the sheets — no `.is-busy`, so **neither the key nor V4's busy slab**, and `aria-busy`; `v5/loader.css`: `.btn[aria-busy="true"] { cursor: progress }`. **Withdrawn:** the first sitting's rule that drew the key after the label, outside the box (`.btn--link.is-busy::after`, a negative inset): under V4's busy rule the link is a teal slab and a key outside it is drawn in the slab's white ink on the page's ground; and the box of such a button ends where its neighbour or its container begins (the label of «Marquer comme lue» is flush with the list's edge, `smoke/messages_wait_fr_1440.png`) | `variants.json`, `sheet_link.png`: the real «Marquer comme lue» / «وضع علامة «مقروءة»», fr and ar, pointer / keyboard / tap, 1440 and 390 — `aria-busy="true"`, class `btn btn--link btn--sm` unchanged, cursor `progress`, no key; **0 px differ** between the control at rest (pointer over it, or focused) and waiting, at device scale 3. `board.json`: link and text samples — their own rule (1 px), transparent fill, own ink |
| *Found in this pass, same defect as A11Y 2:* at a fixed 8 px from the edge the key stood **1.2 px from the label of a small button, 0.3 px in Arabic** («Transmettre au projet» / «الإرسال إلى المشروع», `btn--sm`, padding 16 px) | The key sits **in the middle of the inline-end padding**, whatever the size: `inset-inline-end: calc((var(--btn-pad-end, var(--btn-pad, var(--btn-pad-md))) - var(--key-inline)) / 2)` — the slab's own padding expression | `sm-before/` (old rule put back by an adopted sheet for the reading): 1.21 → **5.21 px** (fr), 0.33 → **3.33 px** (ar); `sm-before/sheet_sm.png`. `variants.json`: label → key 6–9.5 px in a button or a large one, 4.9–5.5 px in a small one, 3.3 px in a small Arabic one; key → edge ≥ 4.5 px; every key inside its button; label shift 0 px, box shift 0 px in the 32 cases |
| **A11Y 3 (minor)** — focus lost when «Réessayer» is pressed | `retryFrom()` focuses the control that waited (else the form's submit) before the retry hides | B8: `focus before: retry → after: submit`, twice |
| **A11Y 4 (minor)** — the forced-colours rule does not reach the ink layer | `.sig__turn > .sig__face--ink { display: none }` (beats `.sig__turn > svg`) | `test_under_forced_colours_the_release_shows_neither_room_nor_ink`: `room: none, ink: none, running: 0` |
| **REVIEW m5 (minor)** — `aria-disabled` on controls nothing refuses | `busy(control, { refuses })`: only on `form[data-single-submit]` | `variants.json`: `aria-disabled` is `true` in the 7 guarded cases and absent in the 19 others |
| **A11Y 6 (minor)** — the account menu's logout hears `aria-busy` and shows nothing | Only a `.btn` waits: no class, no `aria-busy` on a plain button (a face for that item is W2-A's, if it wants one) | `test_a_submit_control_that_is_not_a_button_of_the_system_declares_no_state` |
| *Read in the code in this pass, not observed:* a long wait that ended without the retry left its `once` listener on «Réessayer», and the next long wait added a second — a press would have run the retry twice | One listener per control (`c43ca82`) | B8 after the fix: two long waits in a row on the same host, each retry leaves host, form and guard at rest |

**The 32 cases of the real path** (`final/variants/`; key : ground = weakest core pixel · median; gaps in CSS px from the
two captures; the last column `aria-busy` / `aria-disabled` after the activation):

| Control | Page | | Activation | Key : ground | Label → key | Key → edge | State |
|---|---|---|---|---|---|---|---|
| primary · guarded | /fr/compte/login/ | fr 1440 | pointer | 3.6 · 3.97 | 144.1 | 6.67 | true / true |
| primary · guarded | /fr/compte/login/ | fr 1440 | keyboard | 3.6 · 3.97 | 144.1 | 6.67 | true / true |
| primary · guarded | /ar/compte/login/ | ar 1440 | pointer | 3.6 · 3.97 | 132.11 | 8.67 | true / true |
| primary · guarded | /ar/compte/login/ | ar 1440 | keyboard | 3.6 · 3.97 | 132.11 | 8.67 | true / true |
| primary · guarded | /fr/compte/login/ | fr 390 | tap | 3.62 · 4.0 | 98.77 | 7.0 | true / true |
| primary · guarded | /ar/compte/login/ | ar 390 | tap | 3.62 · 4.0 | 87.78 | 8.0 | true / true |
| primary | /fr/compte/profil/ | fr 1440 | pointer | 3.6 · 3.97 | 7.05 | 6.95 | true / — |
| primary | /ar/compte/profil/ | ar 1440 | keyboard | 3.62 · 4.0 | 30.44 | 8.0 | true / — |
| primary | /documents/upload/ | fr 1440 | pointer | 3.6 · 3.97 | 7.64 | 6.36 | true / — |
| primary large | /fr/orientation/ | fr 1440 | pointer | 3.62 · 4.0 | 9.45 | 8.55 | true / — |
| primary large | /ar/orientation/ | ar 1440 | keyboard | 3.62 · 4.0 | 32.33 | 10.0 | true / — |
| primary large | /ar/orientation/ | ar 390 | tap | 3.6 · 3.97 | 32.33 | 10.0 | true / — |
| primary sm | /fr/espace-reserve/entreprise/mes-besoins/BD1F1C30DB/ | fr 1440 | pointer | 3.6 · 3.97 | 5.21 | 4.79 | true / — |
| primary sm | /ar/espace-reserve/entreprise/mes-besoins/BD1F1C30DB/ | ar 1440 | keyboard | 3.6 · 3.97 | 3.33 | 6.67 | true / — |
| secondary | /fr/espace-reserve/ma-situation/ | fr 1440 | pointer | 3.6 · 3.97 | 6.97 | 7.03 | true / — |
| secondary | /fr/espace-reserve/ma-situation/ | fr 1440 | keyboard | 3.6 · 3.97 | 6.97 | 7.03 | true / — |
| secondary | /ar/espace-reserve/ma-situation/ | ar 1440 | pointer | 3.6 · 3.97 | 6.0 | 8.0 | true / — |
| secondary | /ar/espace-reserve/ma-situation/ | ar 390 | tap | 3.6 · 3.97 | 36.73 | 8.0 | true / — |
| secondary · guarded | /fr/compte/email/ | fr 1440 | pointer | 3.6 · 3.97 | 7.57 | 6.43 | true / true |
| secondary sm | /fr/espace-reserve/dossiers/E46E03B461/ | fr 1440 | pointer | 3.6 · 3.97 | 5.21 | 4.79 | true / — |
| secondary sm | /ar/espace-reserve/dossiers/E46E03B461/ | ar 1440 | keyboard | 3.62 · 4.0 | 26.14 | 6.0 | true / — |
| secondary sm | /fr/espace-reserve/dossiers/E46E03B461/ | fr 390 | tap | 3.6 · 3.97 | 4.88 | 5.12 | true / — |
| secondary sm | /fr/espace-reserve/entreprise/mes-besoins/BD1F1C30DB/ | fr 1440 | pointer | 3.62 · 4.0 | 5.52 | 4.48 | true / — |
| danger | /fr/compte/profil/suppression/ | fr 1440 | pointer | 3.6 · 3.97 | 6.94 | 7.06 | true / — |
| danger | /fr/compte/profil/suppression/ | fr 1440 | keyboard | 3.6 · 3.97 | 6.94 | 7.06 | true / — |
| danger | /ar/compte/profil/suppression/ | ar 1440 | pointer | 3.62 · 4.0 | 8.61 | 8.0 | true / — |
| danger · guarded | /fr/compte/email/ | fr 1440 | pointer | no key | — | — | — / — |
| link sm | /fr/espace-reserve/communications/ | fr 1440 | pointer | no key | — | — | true / — |
| link sm | /fr/espace-reserve/communications/ | fr 1440 | keyboard | no key | — | — | true / — |
| link sm | /ar/espace-reserve/communications/ | ar 1440 | pointer | no key | — | — | true / — |
| link sm | /fr/espace-reserve/communications/ | fr 390 | tap | no key | — | — | true / — |
| link sm | /ar/espace-reserve/communications/ | ar 390 | tap | no key | — | — | true / — |

The guarded «Enlever» of the e-mail page shows nothing because allauth's own script asks `confirm()` on the click and the
probe's browser dismisses it: no submit, so nothing waits — the «validation answered in place» that happens before the hook.

### Measures besides the table

- **Smoke** (`final/smoke/`, 56 loads: 13 pages × fr / ar × 1440 / 390, the case page re-run once — my script read a box
  while the page still scrolled): every load 200, **0 console errors, 0 horizontal overflow**; the only looping animation
  is the home hero's `route-current` (V4's, W2-D's — the accessibility check's observation). Looked at: the login waiting
  (fr 1440 with the focus ring, ar 390), «Marquer comme lue» waiting (fr 1440, ar 390), the company's need in Arabic
  (small primary, key at the left end), the home with the «Personnes» door open at 1440 and the drawer open at 390 in
  Arabic (`nav.js` through the gate), the contact sheets `sheet_keyed.png`, `sheet_link.png`, `sheet_pending.png`, and the
  board's L2 section at 1440 and under forced colours.
- **Reduced motion on the merged tree** (`reduced-motion-merged.json`, the setting emulated): 20 loads — fr, ar; public,
  account, console; 1440, 390 — 0 running, 0 moving; 9 elements carry MS-O4's fade on the pages with the public chrome
  (five panels, four photographs), none in the console.
- **The board** (`final/board/`): 200, 33 hosts, **0 running animations 2.6 s after the load, 0 infinite**, no overflow,
  0 console errors at 1440, 390, reduced motion and forced colours; the live form — a real GET of the board to itself:
  `is-busy`, `aria-busy`, `aria-disabled` in the submit's task, the page reloaded, at rest.
- **Bytes** (gzip −9; design-v5 `a906d6d` → HEAD): `dist/main.css` 42 712 → 43 840 (+1 128, the loader's whole share:
  the fix adds about 160 B to the sheet, 43 B gzipped); `portal/console.css` 2 687 → 2 936 (unchanged by the fix);
  `dist/shell.js` 721 → 1 069 (the hook); `dist/loader.js` 1 193 → 1 504 against the reviewed build (+311: the lease),
  still loaded on the first submit only; the shared chunks 30 090 (four files) → 30 186 (two files: the navigation's
  chunk now shares `motion.js`'s). `v5/loader.css` is 11.7 KB of source with its comments, 4.8 KB without. Against
  §2.6's Wave-1 ceilings, on the merged tree with W2-C1: home (`main.css` + `pages.css`) 46 660 ≤ 47 306; an interior
  page 43 840 ≤ 44 486; the login (+ `entrance.css`) 45 048 ≤ 45 694; the dashboard (+ `console.css` + `portal.css`)
  49 463 ≤ 49 860.

### Handed to — findings that lie in another family's slice (not fixed here)

| To | What | Where it is said |
|---|---|---|
| **W1-C** (buttons) | **V4's busy rule repaints every busy button as the primary** (`v4/buttons.css` §BUSY: `--btn-fill`, `--btn-ink`, `--btn-lighting`): a secondary, danger, ghost or soft button turns teal with a white label while it waits (`sheet_keyed.png`: «Mettre à jour», «Confirmer la suppression»), against DS V5 §10.1 («as primary (key in `currentColor`)») and DL54-13. With `v5/buttons.css`: drop the override — the key already takes the button's ink (`color: var(--btn-ink, var(--accent))`) and reads ≥ 3.9 : 1 at 80 % on every variant's own pair (`own-pairs.json`) — and delete the dead `btn-busy … infinite` keyframes. Not neutralised from `v5/loader.css`: `--btn-fill: initial` would strip the variant's own fill (the busy rule's specificity beats the variant's). Two latent traps in the same rule: it does not reset `--btn-fill-hover` (under the pointer or the keyboard's focus the background-colour of a busy button is the variant's hover fill — the disabled grey on a guarded form — hidden only by the opaque `--btn-lighting`); and in a dark context `:is(.hero, …) .btn--primary:hover` (0,3,0) beats it, so a busy primary there would show the white busy ink on the light night-hover fill — **not served today** (the crawl of 276 pages, `discover.json`, finds no submit `.btn` in a dark context). The ICON button's busy face (DS V5 §10.1: the key replaces the glyph) is W1-C's to draw: until then `KEYLESS` holds `.btn--icon` | REVIEW m3; A11Y 5 |
| **W3-B / W3-D** | The dashboard still animates at load beside the release: `rail-draw` on the journey's steps (900 ms) and `strip-fill` on the health strip (320 ms) — V4's entrances, which MS §3.2 retires («the console has no entrance and no stagger at load») | REVIEW m2; A11Y observation 2 |
| **W2-D** | The home hero's `route-current` loops (28 s `infinite`, `v4/hero.css`; under no-preference only): «nothing loops» | A11Y observation 3; `final/smoke/smoke.json` |
| **W2-A** | The account menu's logout (`button.account-menu__link`) is not a `.btn`: it declares no state when submitted. If the item should show a wait, make it a button of the system | A11Y 6 |
| **W1-P** | The preview's index should name the release's seat beside «L'ingresso, dopo «Entrer»» — proposed sentence: «sulla prima pagina della console si accende la porta del marchio — nel marchio della rail, in alto nella colonna di sinistra; sotto i 1024 px in quello della barra superiore — una volta per sessione. È un dettaglio minuto (24 px): guardare lì nel primo secondo e mezzo.» (`templates/dev/designpreview/index.html`, one `<p class="dp-states__how">`) | REVIEW m1 |
| **W2-B** (the login) | (a) The engage's wiring is W2-B's, as before: with a host that offers «Réessayer» the CTA stays waiting past 10 s until the person retries — by design, measured (B8). (b) *Seen in the smoke, not from the reports:* on the Arabic login at 390 px the password field's placeholder runs under the show / hide control (`final/smoke/zoom_login_ar_390_password.png`); already so in the «before» set (`zoom_before_v4_login_ar_390.png`) | this pass |
| **W3-F2 · W3-E** | Templates of theirs that the loader now reads: `templates/accounts/profile.html` — the export form's `data-loader="none"` must survive any rewrite (`test_loader_rules` fails without it); `templates/portal/messages.html` «Marquer comme lue» and `templates/documents/index.html` «Supprimer» are link-styled submits: they wait without a key | — |
| **The steward** | The manifest (below); DL54's numbering (26, 27); the Wave-1 CSS allowance after W2-C1 and W1-D together (`main.css` 43 840 B gz); **six failures that are on design-v5 already** (`a906d6d`, before this branch): `test_state_chips_carry_a_register` on W1-P's preview templates — W1-P's chips or W1-C's lint to settle (Tests, below) | A11Y observation 4; this pass |

### Left as built

- **REVIEW m4** — under reduced motion the release shows the verbatim mark and leaves no trace: the plan's letter (§1.9:
  «the end state, without travel»). The lit still is the Creative Director's to take or leave; nothing was changed.
- **REVIEW m1, for the owner's report, in words:** at the served size the release is a whisper on a 1× desktop — a
  6 × 8 px change inside the rail's 24 px mark — and reads as designed at 3× and 4×; a person will not notice it unless
  told where to look. The signature becomes legible when W2-B wires the engage on the login's stage at 160 px.
- **The keyboard's submit plays the 320 ms turn** (A11Y observation 1): the senior reviewer agreed it is an activation.

### Ownership — for the merge step (`scripts/check_ownership.py w1-d design-v5`: 16 inside, 13 slice, 15 generated, 12 outside)

The ten extra paths of step 2 stand (`apps/accounts/apps.py`, `apps/accounts/templatetags/{__init__,entrance}.py`,
`static/css/dev/loader-board.css`, `static/css/main.css`, `static/css/v5/tokens.css`,
`static/js/src/{console,shell,situation}.js`, `tests/frontend/test_design_preview.py`). **Two more, to write into the
manifest, not to ignore:**

1. `templates/accounts/profile.html` (W3-F2's) — one attribute, `data-loader="none"` on the export form: the review's own
   fix for M1 («a justified extra path for the steward, like the others»).
2. `static/js/src/nav.js` (W2-C1's) — the motion gate only: one import, three reads of the setting, the layout's frame.
   Plan §1.5 gives every script sequence to the gate and names the architrave; W2-C1 shipped before the gate reached
   design-v5. Its own browser tests pass unchanged.

In the slices: `tests/frontend/test_v5_tokens.py` (the reduced-motion rule: the discrete companion), `static/js/main.js`
(the guard's comment), A11Y §7, DS 2026 (the loader's prose; §2 / §16 figures regenerated), DL54 (the family's entries).

### Tests

On the final tree: `test_loader_rules` (15), `test_loader_w1_d` (27: 5 with Django's client, 22 in Chromium),
`test_rm_flag_parity`, `test_script_motion_gate`, both bundle-currency tests, `test_design_docs`, `test_v5_tokens`,
`test_v4_tokens`, `test_design_preview`, `test_cms_nav`, `test_reduced_motion_w1_d`, `apps/portal/tests/test_browser.py`,
`apps/accounts` — **1057 passed** (`final/pytest-targeted-1.log`); and, because the merge and `nav.js` touch every public
page, the navbar's and the layout's browser sets — `test_browser_w2_c1`, `test_rtl_browser_nav`,
`test_header_fits_the_narrowest_viewport`, `test_browser`, `test_forced_colors_probe`, `test_layout`,
`test_console_shell_stylesheets`, `test_static_assets` — **108 passed** (`final/pytest-targeted-2.log`). 0 failed, 0
skipped; no browser run crashed. The full suite was not run (V5.5: the integration checkpoint runs it). `ruff check`
clean on the files touched. The tests of «no wait is for ever» wait for the state they assert, with a bound, and
hold the lease's lower bound (still waiting 7 s after the submit, at rest not before 9 s) — never a date on a quiet
machine: the loader's tests re-run on the final file, 42 passed, and the seven that depend on time twice more, 7 / 7.

As a net under the merge, the static half of `tests/` was run once (`pytest tests -m "not browser"`,
`final/pytest-tests-static.log`): **1684 passed, 7 failed, none of them this branch's** — six are
`test_state_chips_carry_a_register` on W1-P's preview templates (`templates/dev/designpreview/{_family,_row,_strip,index}.html`:
a `dp-state` chip without `data-register`), **the same six on design-v5 at `a906d6d`** (run there, 6 failed, 86 passed);
the seventh, `tests/i18n/test_documentation.py::test_cited_paths_exist`, wanted a screenshot the RTL browser suite
writes (`docs/qa/rtl/form-errors-ar-390.png`, untracked) and passes once `tests/i18n/test_rtl_browser.py` has run in the
worktree (23 passed here, then the documentation tests green).

### Method, and what the next pass should know

- **The real path.** A control is pressed with a real pointer, Enter after real Tabs, or a tap. What answers is the
  lane's own server: a scratch middleware outside every repository (`.work/w1-d/w1-d-fix/lane/lane_slow.py`, loaded by
  `lane_settings.py` = `config.settings.dev` with that middleware first) answers a POST that carries the cookie
  `lane_answer` before any view — 204, an attachment, a page after N seconds: nothing is written, no form is processed.
  The export uses the product's own view.
- **Chromium answers no Runtime or DOM call of a page whose navigation is pending** — held at the network or really
  slow: `page.evaluate` waits for the commit. While a navigation is pending, the state is read through the page's own
  console reports and CDP captures (`Page.captureScreenshot` at `clip.scale` 3 is pixel-identical to Playwright's
  capture: 0 of 18 720 px differ).
- **The contrast** is read on two captures at device scale 3 that differ by the key alone (an adopted sheet hides
  `::after`: CSSOM, the CSP untouched): the key's core is the pixels whose difference is at least 90 % of the largest.
- **The headless shell has no back/forward cache** (`BackForwardCacheDisabledForDelegate`): B6 ran on the full Chromium
  already installed beside it (build 1234, Chromium 151), headless, with Playwright's `--disable-back-forward-cache`
  left out; a page restored from the cache fires no `load` (wait for the commit).
- **With the preview on, the session cookie is `ile_v5_sessionid`** (the dev settings' preview block), and the preview
  answers only on `ILE_DESIGN_PREVIEW_PORT`.
- **«No event tells a script» was tried, the Navigation API included** (F/`navigation-api.json`, the login's real
  submit): on a 204 and on an attachment Chromium fires `navigate` and then nothing — no abort of the event's signal, no
  `navigateerror`, no `navigatesuccess`; only a stop (`window.stop()`) aborts the signal. So the declaration and the
  lease stand. Resting at once on a stop, where that API exists, is a possible refinement; it is not built.

### Honest limits

Chromium only. The lease, the 204 and the undeclared file were given by the lane's scratch middleware, not by a product
view (the product has one form whose answer is a file — the review and the scan of `test_loader_rules` agree — and it is
declared; the documents' downloads are links). The variants' own pairs (`own-pairs.json`) are computed from
computed colours, not read on pixels — no variant keeps its own surface while busy today. The L1 host of B8 was built in
the login page from `components/loader.html` rendered by Django, with placeholder words (the login's wiring and its
words are W2-B's). The real back/forward cache was exercised on one public page; the guarded forms are served
`no-store` and are not cached — their `pageshow` path is held by the dispatched event in `test_loader_w1_d`. The lit
face (`.is-lit`) has no product path yet. No person watched the motion at speed.

### What this pass wrote and removed

Evidence and scratch outside every repository. On `ile_v5_l7`: 14 sessions minted by `Client.force_login` (no password
used, typed or stored) — **all 14 revoked** and the cookie file removed; one unread communication created for
qa-doc-person and **deleted** (0 unread left); 12 data exports by qa-doc-person through the product's own view and the
audit rows of these actions remain in the lane's clone. Browser profiles under `.profiles/w1-d-fix/` removed; the lane's
server stopped; no browser left running.

---

## Merge step — the steward's note on numbering (9 October 2026; label w1-d-merge)

W1-B's entries reached design-v5 first as DL54-26 … DL54-36, so at the family's own merge W1-D's two entries became
**DL54-37** (the loader «Lume» as built, with its addenda) and **DL54-38** (every V5 duration at 0 ms under reduced
motion), content unchanged. Wherever this file says «DL54-26» or «DL54-27» (the «Review fixes» section) or, before
9 October, «DL54-20» or «DL54-21» — and wherever `REVIEW.md` and `A11Y_PERF.md` say «DL54-20» or «DL54-21» — read
DL54-37 and DL54-38. The one citation in code, an assertion message of `tests/frontend/test_loader_rules.py`,
follows the new number. What shipped, the tag and what is left: `SHIPPED.md`, beside this file.
