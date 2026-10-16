# Integration checkpoint 3 — the steward's integration fixes, step 1 (intfix-1)

Branch `v54-intfix`, cut from `design-v5` at `8e13cd2` (W2-C2's shipped note), 12 October 2026, lane 3
(tests on `test_ile_v5_l3`, Chromium through Playwright, sessions minted with `Client.force_login`). Four known
failures, each read to its root cause; one commit each, and these notes. Nothing deployed, no production touched.

| | failure | verdict | fix |
|---|---|---|---|
| (a) | `test_design_preview.py::test_a_client_that_resets_after_its_page_costs_the_server_no_slot`, `OSError [Errno 22]` on GitHub's Linux runner | the test packed the Windows `struct linger` | the platform's layout |
| (b) | `test_script_motion_gate.py::test_no_animate_or_frame_loop_outside_the_gate` | W2-A's `overlay/extras.js` asked for a frame itself | the frame comes from motion.js's gate, handed over in the core |
| (c) | the console drawer reopened from the keyboard often ignored a press on the scrim (W3-A's «Menu» test, 2 runs in 3 on design-v5) | **a real bug of the overlay system**: a dialog's late `close` event settled a drawer already open again | the late event settles only a closed dialog; an opening settles a close it has not heard |
| (d) | three tests of `test_loader_w1_d.py` | one product gap (a guarded form refused for ever without the state machine), two stale tests (markup W3-F2 and W2-C2 changed legitimately) | `shell.js` lifts the guard with the face; the two tests read today's markup, nothing they protect dropped |

## (a) SO_LINGER in the platform's layout — `31e3084`

**Root cause.** The test resets three sockets (SO_LINGER on, timeout 0: `close()` sends a RST) and packed the option
as `struct.pack("hh", 1, 0)`: four bytes, Windows' `struct linger` (winsock2.h: two `u_short`). Linux's is two `int`
(sys/socket.h, eight bytes), and its kernel refuses a shorter option with `EINVAL` — errno 22, what GitHub's runner
reported. **Measured:** in a local `python:3.13-slim` container `"hh"` and `"HH"` raise errno 22 and `"ii"` is
accepted (read back as `(1, 0)`); on this Windows machine all three are accepted. **Fix:** `"HH"` on `win32`, `"ii"`
elsewhere (Linux, macOS). What the test proves is unchanged: the clients still reset.

## (b) The overlay's resize throttle through the motion gate — `822b3ae`

**Root cause.** W1-D's rule (V5.4 plan §1.5; `test_script_motion_gate.py`): no module calls `requestAnimationFrame`
or `.animate(` outside `motion.js`, whose helpers ask `reducedMotion()` first. W2-A's `overlay/extras.js` throttled
its resize (a zoom may make a dialog's body scroll, or stop: its focus stop follows) with
`window.requestAnimationFrame`. **Fix.** `extras.js` imports nothing by design (`test_overlays.py`, A11Y_PERF M4), and
`overlay.js` may make no other dynamic import, so `overlay.js` imports `nextFrame` from `motion.js` statically and
hands it over in the core it installs; the throttle waits on `core.nextFrame()` behind a boolean latch. Behaviour kept:
one re-read per frame of resizes; under reduced motion the gate answers at once, and a resize is already dispatched
once a frame.

**Weight.** The overlay core chunk now imports the motion chunk (`chunk-IHMJKVKL`, Motion + `motion.js`), which every
product page already loads — `shell.js` (base.html) and `console.js` import it — so no product page fetches anything
new. The one page that does is the dev specimen `templates/dev/designpreview/specimens/overlays.html`, which loads
`overlay.js` alone. Sizes below.

## (c) A dialog's late `close` event took the trap from a drawer opened again — `96b389d`

**The symptom.** On a console page at phone width: «Menu» opens the drawer, Esc closes it, Space opens it again — and
a press on the dimmed page does not close it (W3-A's `test_menu_is_reached_in_three_keys…` failed 2 runs in 3 on
design-v5; W2-A's own run saw «a click on the scrim right after a quick close and reopen did not close the drawer»).

**Reproduced first.** A probe (12 iterations: Esc and Space pressed back to back, then a press at 370, 400) broke 9
times in 12, and its event log showed the mechanism every time:

```
51 overlay:close:esc  open=false      ← the module's close(): settle() at once
53 keydown Space
56 overlay:open:api   open=true       ← the drawer opens again
64 overlay:close:close open=true      ← the platform's `close` event of the Esc, one frame late: settle() again
66 toggle:open        open=true       ← the dialog's toggle event re-adopts it as a non-modal panel
```

After that: the `<dialog>` still `[open]` and drawn, but `aria-modal` gone, the scrim closed (`pointer-events: none`;
`elementFromPoint(370, 400)` is the page's empty state, not the scrim), the scroll lock gone, the panel `inert` (its
timer re-checks `isOpen()`, which is true, so it stays inert), the focus sent back to «Menu». The three iterations
that passed had a frame between the two keys.

**Root cause.** `overlay.js` settled a dialog on its native `close` event: `panel.addEventListener("close", () =>
settle(panel))`. That event comes late — Chromium dispatches it with the next frame's events (the specification queues
it as a task: late either way). The module's own `close()` settles at once, so the late event is normally a no-op
(`record.open` is already false) — unless the dialog was opened again in between: then `record.open` is true again and
`settle()` takes the NEW opening apart. Esc then Space within one frame (Playwright's keys are 2–3 ms apart; a
person's, on a busy page whose next frame is late), or a close and an opening in one task (the public API), are
enough. W2-C2's «held scrim» (`data-held`) is not
involved: the press never reached the scrim, which had already been closed.

**Fix (two parts, both needed).**
1. The `close` listener settles only a dialog that is closed (`if (!panel.open) settle(panel)`): a dialog closed and
   opened again in between hears its old close while open, and that close was settled already.
2. `open()` settles a close it has not heard yet before opening — closed, but still open in the books (`record.open`):
   a form `method="dialog"` or another script closed it, and its `close` event has not arrived. Without part 2, part 1
   alone left the page locked after such a sequence (measured: another script's `d.close()` then the system's
   `open()`, a press on the scrim, `html[data-overlay-lock]` still set).

Not covered, and said: a dialog closed AND opened again by other scripts within one frame keeps the books of its first
opening (open, its first modality) — no product script does that; the module's own openings are covered.

**Proved.** `test_overlays_console_browser_w2_a.py::test_a_drawer_closed_and_opened_again_within_a_frame_keeps_its_trap_and_a_press_on_the_scrim_closes_it`:
Esc then Space lined up behind one frame (`requestAnimationFrame`, then the two keys), twelve times over, each time
the whole trap checked after the next frames (open, `aria-modal`, not inert, the scrim open and under the press, the
lock, the focus inside, `aria-expanded`) and a press on the scrim closing it with the focus back on «Menu»; then the
same close and opening in ONE task through the module's API; then another script's `close()` before the system's
`open()`, the page given back after the press. **Before the fix: 4 runs of 4 failed at the first attempt**
(`inert: True, behind: False, focus: False`); the API and script cases failed too (probe). **After: 10 runs of 10.**
W3-A's «Menu» test 5 of 5 alone — a weak witness here: on this machine it also passed, before the fix, the 4 runs of 5
that reached the drawer (the fifth drew live-server port 4045, which Chromium refuses as unsafe) — the race needs the
keys inside one frame, and the new test lines them up. The overlay suites: 90 passed (below).

## (d) The loader's three failures — `37dd8ad`

1. **`test_without_the_state_machine_nothing_waits` — the PRODUCT.** W3-F2's account pages (`b5e9c21`) guard the
   profile form with `data-single-submit`, like every allauth form of their frame — legitimate, and the creative
   direction's rule («every public form gets `data-single-submit`»). With `loader.js` lost (the test aborts it),
   `shell.js` took back its face (`is-busy`, `aria-busy`) but main.js's guard stayed: `data-submitted` and
   `aria-disabled="true"` for ever — a refusal nothing ends, which W1-D's own review counts as a defect (A11Y_PERF:
   WCAG 4.1.3, a state announced that never ends). The gap was latent on every guarded form (allauth's included); the
   test met it on the first guarded form it read. **Fix:** `shell.js`'s catch lifts the guard (the mark, the
   `aria-disabled` main.js put on the form's submit buttons) with the face, as `loader.js`'s lease would have; every
   guarded form submits through a `.btn` (checked), so the catch is the one path. The test now runs on the account's
   guarded form and on the help desk's unguarded request, reads the guard in the submit's own task (a guard never set
   cannot pass for one lifted), and **fails without the fix** (measured: `aria-disabled: "true"`, `submitted: True`).
   `test_loader_rules.py` pins the release in the catch.
2. **`test_a_wait_that_no_page_ends_is_a_lease` — the TEST was stale.** Its «unguarded form announces no refusal» read
   the profile form, guarded since W3-F2. The unguarded case is now the help desk's request
   (`/fr/espace-reserve/guichet/nouvelle-demande/`: one `.btn--primary`, no guard, no opt-out), checked to be unguarded
   before it is used; the guarded login, the refused second submit, the lease, the rest and the next submit are as they
   were.
3. **`test_a_submit_control_that_is_not_a_button_of_the_system_declares_no_state` — the TEST was stale.** It looked for
   `form button.account-menu__link`, the account menu's design-V4 face, which W2-C2 (`8dbe427`) retired for the overlay
   system's popover: it found no control and asserted that. The sign-out controls are now found by what they do — the
   forms that post to `account_logout` —: the popover's `.overlay__item` and the rail's `.rail__tool` (the drawer's
   copy with it), each checked to be no `.btn` (the premise), none given a class or `aria-busy`.

## Weight (V5.8)

CSS: no source touched; every `css/dist` bundle rebuilt from a clean dist is byte for byte design-v5's — the shared
payload (main.css; main + console + portal) is unchanged. JS, design-v5 → v54-intfix:

| bundle | min | gzip −9 |
|---|---|---|
| overlay core chunk (`YVIIZEE7` → `W3HGCHWG`) | 19 456 → 19 546 | 6 476 → 6 521 |
| `overlay/extras.js` chunk (`OJU3JFTX` → `MMO4GKTU`) | 3 742 → 3 737 | 1 600 → 1 597 |
| `overlay.js` entry | 163 → 198 | 143 → 154 |
| `shell.js` entry | 2 356 → 2 523 | 1 163 → 1 214 |

Chunk names follow this worktree's `node_modules` path (a junction to design-v5's; the steward's `35acc4c` note):
`54U76P5C` → `7CFJBW7C`, `MFQVK52T` → `IHMJKVKL`, `OAT2KRBG` → `3N2TNL6A`. Compared with the base, modulo the names
and the order of the chunk imports: only the four bundles above differ (the overlay core chunk, the extras chunk, the
`overlay.js` and `shell.js` entries); every other chunk and entry is the same. The steward's clean rebuild after the
merge renames them back.

## Paths touched (for the merge's ownership check)

`tests/frontend/test_design_preview.py`; `static/js/src/overlay.js`, `static/js/src/overlay/extras.js` (W2-A's);
`static/js/src/shell.js` (the hook, W1-D's); `static/js/dist/**` (generated);
`tests/frontend/test_overlays_console_browser_w2_a.py` (W2-A's: one test added); `tests/frontend/test_loader_w1_d.py`,
`tests/frontend/test_loader_rules.py` (W1-D's); this file.

## Tests (lane 3, `TEST_DATABASE_URL=…/test_ile_v5_l3`; one pytest and one browser at a time)

Run on `37dd8ad` (the four fixes); the one commit after it changes a comment of `shell.js` and these notes — every
bundle rebuilt from a clean dist is byte for byte the same (hash compared), and the static checks ran again on it.

- the new overlay test alone: **before the fix 4 runs of 4 failed** at the first attempt; **after it, 10 runs of 10**;
- W3-A's «Menu» test alone: 5 of 5;
- `test_script_motion_gate`, `test_frontend_bundle_is_current`, `test_css_bundle_is_current`, `test_static_pipeline`,
  `test_overlays`, `test_loader_rules`, `test_design_preview`: **384 passed**;
- the browser suites — `test_overlays_browser_w2_a`, `test_overlays_console_browser_w2_a`, `test_overlays_console_w2_a`,
  `tests/i18n/test_rtl_browser_overlays`, `test_console_shell_browser_w3_a`, `test_console_phone_browser_w3_a`,
  `test_loader_w1_d`: **144 passed** (15 min);
- after the comment change: the two bundle-currency tests, `test_loader_rules`, `test_script_motion_gate`,
  `test_static_pipeline`, `test_overlays`: 70 passed;
- every non-browser test of `tests/frontend` (the design preview apart, above): 1 509 passed, 2 xfailed, **1 failed
  — not this step's**: `test_chips_cards_w1_c.py::test_the_chip_is_drawn_by_one_sheet` (W3-F2's `_lettura.css` draws
  `.registro__row > .chip` outside the chip test's placements). It reads only sources this branch does not touch — no
  CSS and no chip test changed since `8e13cd2` —, so it fails on the base as it does here; on design-v5's tip (after
  the W3-F1 merge, `f371340`) the rule lives in `static/css/v5/_pagina.css`, which the chip test lists.

**Against design-v5's tip.** design-v5 moved after the cut (the W3-F1 merge `f371340`, the steward's rebuild
`a2644b0`); none of its new commits touches a path of this branch, and a trial merge (`git merge-tree`) is clean.

**Not run:** the full regression (the integration checkpoint's own run); GitHub's runner itself (the SO_LINGER layout
is proved on Linux in a container, not on the runner).

# Checkpoint 3 — the full suite on the merged branch (intfix-2)

Lane 3, 15 October 2026 (`test_test_ile_v5_l3`, one pytest and one Chromium at a time, sessions minted with
`Client.force_login`). Nothing deployed, nothing pushed, no production touched, 8780 not touched; the lane server on 8783
was not needed (no page had to be seen outside the tests).

## The merges awaited, and the merge (steps 1–2)

- **Landed, none awaited:** when this step resumed, the three queued merges were on design-v5 — `v54/w3-f1` (`744421b`;
  the merge `f371340`), `v54/w3-c` (`e39bc32`; the merge `92cdddb`) and the DevOps readiness merge `1a61a7c`, recorded in
  DL54-121 (`3d5351b`, then design-v5's tip).
- **The merge** was made by this step's first run on 12 October: `e6ecbde` (a first sync at `a2644b0`, W3-F1) and
  `aff19e7` (design-v5 at `3d5351b`). Every source merged without a conflict; design-v5's decision-log numbering kept, no
  entry added; the generated bundles conflicted on the chunk names a worktree's path gives and were rebuilt from a clean
  dist (`npm run build`). That run's full suite stopped at 11 % when its session ended
  (`evidence/v54/intfix/cp_nonbrowser.log`); the runs below are the checkpoint's. **Re-verified today:** a rebuild from a
  clean dist is byte for byte the committed tree; against design-v5 the merged tree differs only by step 1's four fixes
  (each source's delta identical before and after the merges), their bundles and these notes.

## (e) The chip drawn by one sheet — nothing to change

`test_chips_cards_w1_c.py::test_the_chip_is_drawn_by_one_sheet` passes on the merged tree (the file: 17 passed). The rule
`.registro__row > .chip { justify-self: start; margin-block-start: var(--s-2); }` **places** the chip — where it sits in
the register row's grid and the space above it — and paints nothing. W3-F1 (`3df3639`, `_interior.css`) and W3-F2
(`2c98ca2`, `_lettura.css`) had each drawn it; W3-F1's budget pass, merging second, consolidated them (V5.8 rule 3): one
rule in the shared partial `static/css/v5/_pagina.css` (`7cdaba8`, removed from both sheets), registered in the test's
`placed` map as its docstring prescribes (`3ff62c9`). `_lettura.css` and `_interior.css` name the chip only in comments.

## The full suite (step 4)

| run | tree | result | time |
|---|---|---|---|
| `pytest -m "not browser" -q -p no:randomly --create-db` | `aff19e7`, a fresh test database | **5 058 passed, 0 failed**, 3 skipped, 2 xfailed (507 deselected) | 1 h 03 min 45 s |
| `pytest -m browser -q -p no:randomly`, run 1 | `aff19e7` | **507 passed, 0 failed, 1 error** — a teardown, below | 55 min 11 s |
| the failing file after the fix | `d8fdc42` | `test_drawer_browser_w3_c.py`: 18 passed | 57 s |
| `pytest -m browser -q -p no:randomly`, run 2 (with the teardown survey below) | `d8fdc42` | **507 passed, 0 failed, 0 errors** | 49 min 38 s |

- Skipped: the three cases of `apps/cases/tests/test_intake.py` that need a legal rule in force — none is (as at every
  checkpoint). Xfailed: the two declared debts (`test_design_showcase.py`'s captions, `test_legacy_token_shim.py`).
- No browser run crashed (no «Target crashed», no «Connection closed while reading from the driver»). Chromium only:
  Firefox and WebKit are not installed, so W2-A's other-engine smoke was not collected.
- The `--durations` tables show ~1.79e9 s for the tests that freeze time in their setup (freezegun and pytest's timer,
  DL54-77 item 8): a figure, not a failure.
- The machine was shared (another project's test suite, two other lanes' suites, a lane server on 8785): the durations
  are indicative. The JUnit files agree with the summaries (non-browser: 5 063 cases, 0 failures, 0 errors).

## The failure — a new tab left loading, and the flush deadlocked (`d8fdc42`)

**Symptom.** Browser run 1: `tests/frontend/test_drawer_browser_w3_c.py::test_a_modified_press_keeps_the_links_own_way`
passed, then errored at teardown: pytest-django's transactional flush (one `TRUNCATE` of every table) raised
`psycopg.errors.DeadlockDetected` — «Process 50169 waits for AccessExclusiveLock on relation …; blocked by process 50173.
Process 50173 waits for AccessShareLock on relation …; blocked by process 50169».

**Root cause — the test.** The other process is the live server's request thread. The test Ctrl+clicks a row's link —
the browser's own way: a new tab on the piece's page, `/documents/requirements/<id>/` — and closed that tab at once,
still on `about:blank`. Closing a tab does not stop the server: it went on rendering the piece page in its request's
transaction (`ATOMIC_REQUESTS`) after the test had returned. The `TRUNCATE` takes its tables one by one; the request,
holding the tables it had read, asked for one the `TRUNCATE` already held, and Postgres aborted the flush. Usually the
flush simply waits a few milliseconds for the request; the deadlock needs the two lock orders to cross. **Measured**
(temporary probes on lane 3, never committed: the test's steps, then `pg_stat_activity` on the test database, the test's
own connection excluded): a request of the live server was still running when the test returned in **24 runs of 24**,
and in 12 of 12 with `wait_for_load_state("load")` added (it returns on `about:blank`, before the navigation) — busy for
35–55 ms more (once 0.6 s, once 1.4 s), reading `documents_documentversion`, `cases_caseassignment`, `auth_group`…
No product code is involved: only a test harness flushes a database under a live request. W3-C's runs passed this test;
the checkpoint met the crossing once, in its first browser run.

**Fix.** The test lets the new tab reach the link's own URL and load it (`wait_for_url(<the link's path>,
wait_until="load")`) before closing it. Once the document has loaded, its request's transaction has committed, and the
piece page asks nothing more of the database on its own: its scripts fetch on an action only (`depot.js` after a filing,
the drawer when it opens); its icons, fonts and chunks are static. What the test proves is kept — the modified press
opens a new tab, the drawer stays closed, no console error, no CSP report — and the new tab must now arrive where the
link points. **After the fix**, the real test, its browser context's requests logged: **no request in flight at its
return in 58 runs of 58**; the only requests still open then were static chunks (`depot.js`'s dynamic import); within
the next second a database backend showed twice — once an autovacuum worker (its query recorded), once unrecorded (the
first probe logged no query).

**The survey — no other test leaves a request behind.** Browser run 2 carried a pytest plugin (scratch only, kept as
`evidence/v54/intfix/cp3_survey_plugin.py`) that, at the teardown of every test using the live server — before the
flush —, recorded any client backend still active or in a transaction on the test database. **Run 2: none, in 507
tests.** Positive control: the test as it was before `d8fdc42`, under the same plugin, recorded 5 times of 5.

**Intermittent tests.** One, fixed: this teardown — 1 error in the first full browser run (its precondition present in
every run of the old test; the crossing itself rare); none in the second run nor in the drawer file's runs since. Nothing
else failed in either browser run (1 014 test runs). No test was marked skip or xfail.

## Static checks and the weight

- `manage.py check`: no issues; `makemigrations --check --dry-run`: no changes; `ruff check .` (CI's lint step, ruff
  0.16.8): all checks passed — on `aff19e7`; after `d8fdc42` (one test file), `ruff check` and `ruff format --check` on it.
- **The shared CSS** (`weigh_pages.py`, `gzip.compress(data, 9)`): every CSS bundle of the merged tree is byte for byte
  design-v5's — this branch changes no stylesheet. The branch's cut `8e13cd2` → design-v5 `3d5351b` → the merged tree:

| page type | `8e13cd2` | `3d5351b` | merged |
|---|---|---|---|
| interior page (`main.css` only) — every page's shared payload | 41 029 | 37 324 | 37 324 |
| the login (+ `entrance.css`) | 45 890 | 42 185 | 42 185 |
| the home (+ `hero.css`, `pages.css`) | 55 680 | 51 262 | 51 262 |
| console page types (`main` + `console` + `portal`) | 49 770 | 47 200 | 47 200 |
| the company's dashboard (+ `companies.css`) | 50 643 | 48 073 | 48 073 |
| «Mes pièces» (+ `documents.css`) | 50 942 | 52 697 | 52 697 |

The fall from the cut is the families' (W3-F1's and W3-C's merges); the rise of «Mes pièces» is W3-C's own page sheet
(DL54-120 item 6). Every page type DL54-120 records — fifteen, the page-only sheets included — stands exactly at its
ceiling on the merged tree (`evidence/v54/intfix/cp3_weigh.log`).

## What is left

- **design-v5 moved during the checkpoint**, to `fec37d3`: W3-D's merge (`e35714c`, the journey «La soglia»), DL54-129,
  the tag `v54/w3-d` — 33 commits, not among the merges this step awaited. A trial merge conflicts only on the generated
  `static/js/dist/situation.js`; none of the 33 commits touches a path of this branch. W3-D left its full suite to the
  integration checkpoint and handed it the motion gate's red (fixed here, `822b3ae`): the pass that follows merges it
  and runs the suite again.
- The merge of `v54-intfix` into design-v5 (the steward's: the ownership check with the paths below, a clean rebuild).
- Not run here: GitHub's runner on this tree; Firefox and WebKit (not installed).
- The `--durations` figure for frozen-time setups (DL54-77 item 8), untouched.

## Paths touched by this step (for the merge's ownership check)

`tests/frontend/test_drawer_browser_w3_c.py` (W3-C's: the one test, a wait before its new tab is closed); this file.

## Evidence

`C:/tmp/ile_v5_council/evidence/v54/intfix/cp3_*`: the suites' logs and JUnit files (`cp3_nonbrowser`, `cp3_browser_1`,
`cp3_browser_2`), the probes' logs (`cp3_probe1` … `cp3_probe5`, `cp3_drawer1`), the survey's plugin and its control, the
weigh.

# Checkpoint 3, second pass — design-v5 at `fec37d3` (W3-D's merge)

Lane 3, 15–16 October 2026, the same conditions. design-v5 moved during the first pass (W3-D's merge); W3-D had left
its full suite to the integration checkpoint and handed it the motion gate's red. This pass merges it and runs
everything again.

## The merge — `a059610`

- design-v5 at `fec37d3`: W3-D's merge `e35714c` (the journey «La soglia»), its steward's record DL54-129, the tag
  `v54/w3-d`, the shipped note — 33 commits. Every source merged without a conflict (none of the 33 touches a path of
  this branch); design-v5's decision-log numbering kept, no entry added. The one conflict was a generated bundle
  (`static/js/dist/situation.js`, the chunk names): both dist trees rebuilt from clean. `css/dist` is byte for byte
  design-v5's; `js/dist`, the chunk names read as one, differs only by step 1's four bundles (checked file by file: 19
  files, 4 differ — the overlay core chunk, the extras chunk, `overlay.js`, `shell.js`). W3-D brings no migration.
- `manage.py check`, `makemigrations --check --dry-run`, `ruff check .`: clean, on the merge and on the last fix
  `34c5471`.

## The full suite

| run | tree | result | time |
|---|---|---|---|
| `pytest -m "not browser" -q -p no:randomly --create-db` | `a059610`, a fresh test database | 5 108 passed, **3 failed**, 3 skipped, 2 xfailed (519 deselected) | 1 h 01 min 40 s |
| the three failing files and their neighbours (`apps/pages/tests`; the journey's, the showcase's, the design docs', the comments', the CSS bundle's and the motion gate's tests) | `34c5471` | **954 passed, 0 failed**, 1 xfailed | 10 min 33 s |
| `pytest -m browser -q -p no:randomly`, with the teardown survey | `34c5471` | **519 passed, 0 failed, 0 errors**; the survey: no test leaves a request of the live server running | 52 min 23 s |

Skips and xfails as in the first pass. No browser run crashed. JUnit (non-browser): 5 116 cases, 3 failures, 0 errors.

## The three failures — design-v5's own since W3-D's merge

Each reads a file W3-D's merge changed and no file of this branch. **Proved on a pristine tree of `fec37d3`** (a
temporary detached worktree, removed after): the same three fail there, with the motion gate step 1 fixed (`822b3ae`)
— 4 failed, 615 passed on the four files. None of the three files was among W3-D's targeted runs (its notes list them).

1. **`test_template_comments_do_not_leak.py::test_no_short_comment_spans_more_than_one_line` — the product
   (`f2f1e67`).** W3-D's `002fd24` wrote a four-line `{# … #}` in `templates/dev/showcase.html`'s `extra_head`.
   Django's `{# #}` is single-line: the four lines rendered as text into the page (measured with the template engine:
   the block rendered its prose; now nothing). Fixed: the same words in `{% comment %}`. Development only (the showcase
   is served under DEBUG).
2. **`test_v5_tokens.py::test_the_console_partials_close_the_console_entry` — a stale test, corrected (`71a3675`).**
   W3-D moved «Ma situation»'s form (`v5/_wizard.css`) out of the console entry and split the rail into a vocabulary
   and two components (DL54-128 item 4): `portal/journey.css` = nodes + rail, `portal/situation.css` = form + nodes +
   Stepper — page sheets of the portal itself, importing `v5/_x.css`, the vocabulary `v5/_journey-nodes.css` written
   once and composed into both. The guard knew only another app's page sheet (`../portal/v5/_x.css`, W3-C) and gave
   each partial ONE importer (DL54-112) — a simplification of what it protects: that no page loads a partial twice. One
   importer would force the vocabulary to be drawn twice, or into the shared console bundle (V5.8's ceilings), so the
   test is wrong, not the product; W3-D's own tests pin that «Ma situation» alone links `situation.css` and carries no
   `journey.css`. **The reason for the correction:** the guard now resolves an import where the collected tree puts it,
   and checks what «one importer» meant — never both the entry and a page sheet; every partial imported; the entry's
   partials last and no rule of its own (unchanged); and no product template, through its chain of `{% extends %}`,
   links two sheets that import one partial. Mutations caught: «Ma situation» linking `journey.css` too
   («portal/situation.html loads v5/_journey-nodes.css twice»), the entry importing the vocabulary, the rail's partial
   imported by nobody.
3. **`apps/pages/tests/test_templates_static.py::test_stylesheet_uses_tokens_and_logical_properties_only` — a stale
   ban, corrected (`34c5471`).** W3-D's merge imports the passage into the home's sheet
   (`@import url("../../css/v5/_journey-passage.css");`), a line W3-D's test requires; this compliance test banned any
   `@import`, since `3093261`, when the sheet was served as written. Today the sheet is an entry of
   `scripts/build_css.mjs`, the home links its bundle, and the bundle inlines the partials (no `@import` in
   `dist/pages/css/pages.css`), as for the eleven other page sheets that import partials. **The reason:** the ban's
   purpose — the home's stylesheet loads nothing more — is checked on the bundle; the source may import local partials
   only; and the tokens, logical-properties, no-URL, no-`!important` and forbidden-wording checks now also run on the
   partials it imports (the passage, which the home newly serves, passes them) — wider than before, not narrower.
   Mutations caught: an external import, a non-partial import, an `@import` in the bundle, a physical property in the
   passage.

## The weight (V5.8)

Every CSS bundle of the merged tree is byte for byte design-v5's at `fec37d3`. DL54-129's twenty page types all stand
exactly at their ceilings. The shared payload, `3d5351b` → `fec37d3`: `main.css` 37 324 → 35 483 B on every page, the
console page types 47 200 → 44 196 B (W3-D's merge). The six page types of `weigh_pages.py`:

| page type | `3d5351b` | `fec37d3` | merged |
|---|---|---|---|
| interior page (`main.css` only) — every page's shared payload | 37 324 | 35 483 | 35 483 |
| the login (+ `entrance.css`) | 42 185 | 40 344 | 40 344 |
| the home (+ `hero.css`, `pages.css`) | 51 262 | 49 844 | 49 844 |
| console page types (`main` + `console` + `portal`) | 47 200 | 44 196 | 44 196 |
| the company's dashboard (+ `companies.css`) | 48 073 | 45 069 | 45 069 |
| «Mes pièces» (+ `documents.css`) | 52 697 | 49 693 | 49 693 |

## What is left

- **design-v5 moved again during this pass**, to `f447c28`: the sec-f5 merge (`e0d816b`, F-5 — the back office's own
  sign-in form signs no one in) and DL54-130 — 18 commits in `apps/accounts`, the settings and the documents. Not
  merged here: this checkpoint covers design-v5 at `fec37d3`. A trial merge is clean; of this branch's paths it
  touches `tests/frontend/test_design_preview.py`, in another test (the frame's refused page), not step 1's SO_LINGER
  line.
- **design-v5 carries four reds until this branch lands on it**: the motion gate (step 1, `822b3ae`) and the three
  above.
- `ruff format --check` flags lines that are design-v5's own (`test_v5_tokens.py` 507 and 513; W3-D's notes name two
  of `test_design_docs.py`): CI lints with `ruff check`, which is clean.
- The merge of `v54-intfix` into design-v5 (the steward's): the ownership check with the paths below, a clean rebuild.
- Not run here: GitHub's runner on this tree; Firefox and WebKit (not installed).

## Paths touched by this pass (for the merge's ownership check)

`templates/dev/showcase.html` (slices of W1-C, W2-A, W2-C2 and W3-C in OWNERSHIP_V54.json; the comment is W3-D's);
`tests/frontend/test_v5_tokens.py` (W1-A's, with slices); `apps/pages/tests/test_templates_static.py` (W1-B's); this
file. With the first pass's `tests/frontend/test_drawer_browser_w3_c.py` (W3-C's).

## Evidence

`C:/tmp/ile_v5_council/evidence/v54/intfix/cp3_w3d_*`: the non-browser log and JUnit file, the fixed files' run, the
mutations, the browser log and JUnit file, the weigh.

# At the merge (the steward, label intfix-merge)

Lane 3, 16 October 2026, under `C:/tmp/ile_locks/DESIGN_V5_MERGE_LOCK` (taken at 01:28:48, «holder: intfix-merge»).
The same conditions as the two passes: `TEST_DATABASE_URL=…/test_ile_v5_l3`, one pytest and one Chromium at a time,
sessions minted with `Client.force_login`, `-p no:randomly`. Nothing deployed, nothing pushed, no production touched.

## The sync — `23600fc`

design-v5 had moved from `fec37d3` to `f447c28` during the second pass: the sec-f5 merge (`e0d816b`, F-5 — the back
office's own sign-in signs no one in; a second factor an account holds is presented in every session) and its steward's
record DL54-130 — 18 commits in `apps/accounts`, the settings, the documents and their tests. `git merge --no-ff
design-v5`: no conflict. The one path the two sides share, `tests/frontend/test_design_preview.py`, auto-merged: sec-f5
changed another test in it (the frame's refused page), not step 1's SO_LINGER line. No stylesheet, template or script
came in and no migration; both dist trees deleted and rebuilt from clean (`npm run build`): byte for byte the committed
tree (`git status` clean) — and their mtimes now follow their sources, which closes the review's m1 in this worktree.

## The family in the manifest — `473aa20`, `1f4d63f`

`check_ownership.py intfix design-v5` first answered «unknown family 'intfix'» (exit 2). The steward:

- `scripts/check_ownership.py` accepts the id `intfix` — the steward's integration fixes at an integration
  checkpoint, a family outside plan §3's waves, as `devops` and `sec-f<n>` are; the id rule's test holds three new
  cases (`intfix` valid; `intfix-2`, `intfix3` not) (`473aa20`);
- `docs/design-v5/OWNERSHIP_V54.json` registers the family «intfix» (`1f4d63f`): wave 0, `steward` false (its fixes
  are held to slices like any family's), `delegated` false, DL54-01's branch and worktree, no merge tag (the
  checkpoint's annotated tag `v54/checkpoint-3` marks design-v5, not a family); the test's `OUTSIDE_THE_WAVES` names
  it. Twelve entries, each with its reason — one whole (`docs/design-v5/QA/v54/intfix/**`: these notes and the review)
  and eleven slices, each file staying its owner's: the late settle and the frame wait in W2-A's `overlay.js`; the
  resize throttle in W2-A's `overlay/extras.js`; the catch in W1-D's section of `shell.js`; the comment block in
  `templates/dev/showcase.html` (W3-D's words); the SO_LINGER layout in W1-P's `test_design_preview.py`; the new tab's
  wait in W3-C's `test_drawer_browser_w3_c.py`; the catch's assertion in W1-D's `test_loader_rules.py`; the three tests
  in W1-D's `test_loader_w1_d.py`; the new test in W2-A's `test_overlays_console_browser_w2_a.py`; the console
  partials' guard in W1-A's `test_v5_tokens.py` (beside W3-C's slice); the home sheet's import rule in
  `apps/pages/tests/test_templates_static.py` (beside W1-B's and W2-D's slices).

`check_ownership.py intfix design-v5`, before the steward's two commits: **37 paths — 2 inside, 11 slice, 24 generated
→ PASS**; each slice was read in the diff (`git diff design-v5...v54-intfix`) and stays inside it. After them the
steward's three paths join the list — the manifest (steward-only), the checker and its test (the steward family's whole
files) — as at the sec-f5 merge. `--validate`: coherent, **28 families, 684 entries**.

## The tests on the merged branch

On `1f4d63f` (the sync and the manifest; the tree as merged), `TEST_DATABASE_URL=…/test_ile_v5_l3`:

| run | result | time |
|---|---|---|
| `pytest -m "not browser" -p no:randomly`: the test files the branch changed (`test_check_ownership`, `apps/pages/tests/test_templates_static`, `test_design_preview`, `test_loader_rules`, `test_loader_w1_d`, `test_v5_tokens`, `test_drawer_browser_w3_c`, `test_overlays_console_browser_w2_a`); those that cover its sources — `overlay.js` and `overlay/extras.js` (`test_overlays`, `test_overlays_browser_w2_a`, `test_overlays_console_w2_a`, `test_browser_w2_c2`, `test_nav_sheet_w2_c2`, `test_console_shell_w3_a`, `test_documents_w3_c`, `test_static_assets`, `tests/i18n/test_rtl_browser_overlays`, `test_script_motion_gate`), `shell.js` (`test_components_w1_c`, `test_entrance_w2_b`, `test_entrance_form_w2_b`), the showcase (`test_design_showcase`, `test_template_comments_do_not_leak`, `test_journey_w3_d`, `test_chips_cards_w1_c`, `test_browser_chips_w1_c`, `test_browser_w1_c`, `test_icons`, `test_o14_lint`, `test_state_chips_carry_a_register`); `test_design_docs`, `test_static_pipeline`, both bundle-currency tests, `tests/security`; and sec-f5's two test modules (`test_backoffice_second_factor`, `test_mfa_middleware`: the sync's newest code, run beside this branch for the first time) | **1 824 passed, 0 failed**, 1 xfailed (the showcase's declared debt), 206 deselected — JUnit: 1 825 cases, 0 failures, 0 errors | 10 min 19 s |
| `pytest -m browser -p no:randomly`, Chromium: the overlay and console browser tests (`test_overlays_browser_w2_a`, `test_overlays_console_browser_w2_a` — the late settle's test among them —, `test_overlays_console_w2_a`, `tests/i18n/test_rtl_browser_overlays`, `test_console_shell_browser_w3_a`, `test_console_phone_browser_w3_a` — W3-A's «Menu» test among them —, `apps/portal/tests/test_browser.py`, W2-C2's `test_browser_w2_c2`), `test_loader_w1_d`, and the browser tests of the files the branch changed (`test_drawer_browser_w3_c`, `test_design_preview` — sec-f5's framing test among them) | **200 passed, 0 failed, 0 errors, 0 skipped**; no «Target crashed», no «Connection closed while reading from the driver» | 22 min 05 s |
| `manage.py check`; `makemigrations --check --dry-run`; `ruff check .` (ruff 0.16.8); `ruff format --check` on the steward's two Python files | no issue; no changes; all checks passed; already formatted | |
| `regen_design_inventory.py` (check mode) | the inventory tables and the counts are current | |

The machine was shared (sec-f7's and another lane's suites ran meanwhile, on their own databases; 1.5–2.3 GB free):
the durations are indicative. Logs and JUnit files: `evidence/v54/intfix/cp3_merge_nonbrowser.*`,
`cp3_merge_browser.*`, `cp3_merge_static_checks.log`.

## Left, and handed on

- The review's findings, none holding the merge, handed to their owners: **m2** (W1-D: shell.js's catch is the one
  release only while every guarded form submits through a `.btn` — a static test of that premise, or the release on
  the early return too); **m3** (W1-D: `initMisc`'s comment in `main.js` still names loader.js as the guard's only
  lifter — one line); **m4** (W2-A: fix (b)'s path has no behavioural test — a resize step in the 400 % test); **n1**
  (the steward, at the next pass over `test_v5_tokens.py`: cite DL54-128 item 4 for the third way not taken, and say
  that the chain check follows `{% extends %}` only). **n2** is recorded in DL54-131 (the two rules superseded).
- The review's «seen on the way», not this branch's: a year of cache on the three fixed-name scripts imported from
  inside the bundles (`loader.js`, `depot.js`, `piece-drawer.js`; `WHITENOISE_MAX_AGE`) → the DevOps owners and W1-D;
  a live server that draws a port Chromium refuses → the test infrastructure.
- Not run: GitHub's runner on this tree; Firefox and WebKit (not installed). main (the V4 line) is untouched.
