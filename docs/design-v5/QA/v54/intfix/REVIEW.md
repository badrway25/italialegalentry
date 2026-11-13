# Integration checkpoint 3 — the steward's integration fixes: review (one pass)

Reviewer `intfix-review`, 16 October 2026, lane 3. I built nothing on this branch; this file is the one thing I wrote
in the worktree.

**Reviewed:** `git diff design-v5...v54-intfix` — merge base `fec37d3` (design-v5's W3-D merge), HEAD `792dd9d`: eleven
commits of the steward and three merges of design-v5 (`e6ecbde`, `aff19e7`, `a059610`); 32 paths, +674 / −67, twenty
of them generated bundle paths. The three-dot diff is `fec37d3..HEAD` and holds only the steward's paths: the merges brought
nothing of their own. design-v5 has since moved to `f447c28` (sec-f5) — the merge step's, not this review's.

**Read in full:** V5.5 with its addenda, V5.8's definitive ruling, V5.9; `NOTES.md`; `static/js/src/overlay.js` (all
1 060 lines — every way into `settle()`), `overlay/extras.js`, `motion.js`, `shell.js`; `main.js`'s double-submit guard;
`loader.js`'s lease, `free()` and hooks; the overlay API's callers (`console.js`, `nav.js`, `piece-drawer.js`); the seven
test diffs and the tests around them; DL54-112, DL54-113, DL54-128, DL54-129.

## Verdict: SHIP

No P0, no major. Each fix sits at its root cause — the overlay scrim bug especially: the overlay system's one
asynchronous settle no longer takes a fresh opening apart, and no other way out passes through the lines that changed.
No test was weakened to pass: the loader tests and the drawer's teardown read today's markup and assert as much or
more, and two rules were brought back to their purpose with written reasons that follow a recorded decision
(DL54-128). Nothing changes a family's design: no stylesheet, no product template. Four minors and two nits below; none
holds the merge — and design-v5 carries four reds until this branch lands on it.

## What I ran

| | Result |
|---|---|
| The JS bundles rebuilt from `static/js/src` with `build_frontend.mjs`'s options into a scratch directory (`absWorkingDir` the worktree) | **19 of 19 files byte for byte the committed `static/js/dist`**, names included |
| The CSS entries rebuilt in memory with `build_css.mjs`'s collected-paths plugin (`write: false`) | **22 of 22 byte for byte the committed `static/css/dist`** |
| `pytest -m "not browser"`: `test_overlays`, `test_loader_rules`, `test_script_motion_gate`, `test_v5_tokens`, `apps/pages/tests/test_templates_static`, `test_chips_cards_w1_c`, `test_template_comments_do_not_leak`, both bundle-currency files, `test_static_pipeline`, `test_journey_w3_d`, the SO_LINGER test | **741 passed, 1 failed** — `test_css_bundle_is_current::test_no_source_is_newer_than_its_output`, on mtimes only (m1); the content is current (row above) |
| `pytest` in Chromium, once: `test_overlays_browser_w2_a`, `test_overlays_console_browser_w2_a`, `test_overlays_console_w2_a`, `tests/i18n/test_rtl_browser_overlays`, `test_console_shell_browser_w3_a`, `test_console_phone_browser_w3_a`, `test_loader_w1_d`, `test_drawer_browser_w3_c` | **162 passed** — 0 failed, 0 errors, 0 skipped (JUnit), 15 min 29 s; no «Target crashed» |
| The new overlay test with fix (c) reverted in flight: a scratch pytest plugin serves the overlay core chunk with one part or both undone — nothing on disk | part 1 undone: **fails** at «Esc then Space, attempt 1»; part 2 undone: **fails** at «another script's close», the lock left on the page; both undone: **fails** at attempt 1. As committed: passes (the row above) |
| Fix (b) on the dev specimen board (the lane server on 8783, `overlay.js` alone): an open alert resized 1280×800 → 320×256 → back, then a burst of two resizes within one frame — under normal and under reduced motion | the body becomes a stop (`tabindex="0"`) when it scrolls and stops being one when it no longer does; the burst lands; identical under both settings; no console error |
| `ruff check` on the seven Python files | clean. `ruff format --check` flags three of them exactly as on `fec37d3` (188 / 66 / 8 lines, before and after): no debt added; CI runs `ruff check` |
| Line endings and trailers | LF only (blobs, worktree, diff); the eleven commits end with the Co-Authored-By line |

## The brief's questions

### 1. Is each fix at its root cause?

**(c) The overlay scrim bug — yes, and no other way out is touched.** The bug was the module's one asynchronous settle:
a dialog's native `close` event, which Chromium dispatches with the next frame's events (the specification queues it
as a task: late everywhere). Every other way into `settle()` runs in the task of the act:

- `close()` settles at once — and `close()` is what Esc (the document's capture `keydown` for a dialog that is not
  `:modal`; the `cancel` listener for one that is), the scrim, «Fermer» (`data-overlay-close`), a link in a drawer, the
  grip, Back (extras' `popstate` → `core.close`), a native modal's backdrop, `nav.js` putting the sheet away past the
  desktop width and `console.js` closing the phone-only panels all call;
- a popover settles on `beforetoggle`, in the task (light dismiss, Esc, a choice, the focus leaving, `hidePopover()`).

So for every close the module makes, the late event was a no-op before the fix and is a no-op after it. Part 1
(`if (!panel.open) settle(panel)`) still settles every native close the module did not make — a dialog that is closed
when its event arrives — and no longer one that has been opened again, which is exactly the run that took the trap
away. Part 2 (`if (record.open) settle(panel)` in `open()`) runs only when the books say open and the element is
closed: a close the module has not heard. No product path makes one today (no `method="dialog"` and no `closedby` in a
template; every close is the module's, the `cancel` listener included), so it is defensive — and the new test's third
case (another script's `close()`, then the system's `open()`) shows it is needed when it happens. The gap the two parts
leave (a dialog closed AND reopened by other scripts within one frame keeps its first opening's books) is stated in
NOTES.

| Way out | Its path | Touched by the fix? | Seen passing in my run |
|---|---|---|---|
| Esc, every modal kind (an alert answers safe) | capture `keydown` (not `:modal`) or `cancel` (`:modal`) → `escapePanel` → `close()` or the safe answer | no | board: Esc closes every modal kind and the focus goes back to its opener; console: «Menu», the drawer |
| Back | extras' `popstate` → `close(reason: back)` | no | board: Back closes the drawer beside the list and keeps the address; the piece drawer: Esc, «Fermer» and Back |
| A press outside | the scrim's `click` → `close()`; a menu's light dismiss → `beforetoggle` | no | board: the scrim closes a dialog, never an alert nor unsaved input; console: a menu sheet takes the whole press; the new test |
| The focus return | `settle()`'s, unchanged | its second, late run is gone | the new test: the focus back on «Menu» after each of its 14 presses |
| The trap | `record.modal`, `aria-modal`, the scrim, the lock, `aria-hidden` | kept by the fix | the new test: the whole trap after every reopening; the drawer's trap and its tree |
| The account popover | popover: `beforetoggle` | no | it hangs from its trigger (fr, ar); on a phone it is a sheet that stays a menu |
| Menus | popover | no | board: a menu opens on its trigger's inline end and every way out works; RTL: a menu aligns on its trigger's inline end. (The register's row menu left the product with W3-C — DOCUMENT_WORKSPACE D2: a row opens its piece in the drawer, which the console tests check) |
| The phone sheets | a menu as a sheet over the scrim; a drawer as a modal sheet | no | board: on a phone the dialog and the menu are sheets; the piece drawer on a phone; the new test itself runs at 390 × 844 with touch |

**The new test catches the bug.** Served the overlay core with part 1 undone, it fails at its first attempt with the
trap gone (`aria-modal` removed, the panel `inert`, the scrim no longer under the press, the focus out of the drawer);
with part 2 undone it fails on «another script's close», the lock left on the page; with both undone — the code before
the fix — at the first attempt, as NOTES records (4 runs of 4). Each part is needed, and the test sees each.

**(b) The motion gate — yes.** The red was real: `overlay/extras.js` asked for a frame itself, which W1-D's rule forbids
outside `motion.js`. The frame now comes from the gate, handed over in the core (`extras.js` still imports nothing —
`test_overlays` pins it); the boolean latch keeps one re-read per frame; under reduced motion `nextFrame()` resolves at
once, and a browser dispatches `resize` at most once a frame anyway. The new static import adds no fetch to a product
page: `motion.js` is already in the graph of every page that loads the overlay system (`shell.js` from `base.html`,
`console.js`, `piece-drawer.js` import the same chunks); only the dev specimen board, which loads `overlay.js` alone,
now fetches the Motion chunk (`chunk-IHMJKVKL`, 26 532 B gzip, and its 412 B helper chunk) — as NOTES says, and
development only. No test exercises this path (m4); my probe above shows it working both ways under both motion
settings.

**(a) SO_LINGER — yes.** `struct linger` is two `int` on Linux and macOS, two `u_short` on Windows; the resets and what
the test asserts are unchanged.

**(d) The loader — yes, for the product gap.** main.js's guard on a `data-single-submit` form had one lifter, loader.js;
without it, `data-submitted` and `aria-disabled` stayed for ever. The catch lifts them with the face, at once — coherent
with W1-D's state model (`aria-disabled` is part of the wait, and without the state machine nothing waits) — and lifts
exactly what main.js set (the form's own submit buttons). The trade is no double-submit refusal when loader.js cannot
be loaded: in production a failed fetch (the manifest storage keeps the unhashed `loader.js` that shell.js's dynamic
import names, and `collectstatic` never runs with `--clear`), and the server meets a double post from a page without
script anyway. The precondition the fix rests on is unpinned (m2).

**The teardown deadlock (`d8fdc42`) — yes.** The cause is the test: a request left running in the live server across the
transactional flush, measured in flight 24 times of 24. The test now waits for the new tab's load — and so also asserts
that the tab lands on the link's own path — and the steward's survey plugin found no other test leaving a request (0
of 507, then 0 of 519; positive control 5 of 5).

**W3-D's three reds — yes.** The four-line `{# #}` rendered into the dev showcase: now `{% comment %}` (development
only). The other two are test corrections, read under question 2.

### 2. Was any test weakened?

No.

- `test_design_preview.py`: the option's byte layout only.
- `test_overlays_console_browser_w2_a.py`: one test added, nothing removed.
- `test_drawer_browser_w3_c.py`: one wait added, which asserts more (the new tab's path).
- `test_loader_rules.py`: one assertion added (the release in the catch).
- `test_loader_w1_d.py`: (i) the lease test keeps its guarded 204 (the login) and an unguarded «file» answer; the
  unguarded form is now the help desk's request, asserted unique and unguarded before it is used, because W3-F2 guarded
  the profile form (the next test's guarded case) — the timings, the refused second submit, the rest and the next
  submit are as they were. (ii) «Without the state machine» runs on a guarded and an unguarded form, reads the guard in
  the submit's own task — a guard never set cannot pass for one lifted — and fails without the fix (the steward
  measured it). (iii) «Not a button of the system» looked for `button.account-menu__link`, retired by W2-C2, found
  nothing and failed; it now finds every sign-out control by its form's action, requires both the popover's row and
  the rail's tool, and checks its premise (no `.btn`) on each.
- `test_v5_tokens.py`, `apps/pages/tests/test_templates_static.py`: two rules brought back to their purpose, each with a
  written reason, both following a recorded decision — corrections, not weakenings:
  - the console partials: DL54-112's «ONE importer» becomes: never both the entry and a page sheet; the entry imports a
    partial once; every partial is imported; the entry's partials last; and, new, no product template links — through
    its chain of `{% extends %}` — two sheets that import one partial. The departure is W3-D's (DL54-128 item 4: the
    nodes vocabulary composed into `portal/journey.css` and `portal/situation.css`, one request fewer on «Ma
    situation»), merged under DL54-129 (W3-D had left its full suite to this checkpoint). Mutations caught (NOTES).
    Two precision points: n1.
  - the home's sheet: «no `@import`» guarded a sheet served as written; the home now links the bundle
    (`css/dist/pages/css/pages.css`, in `templates/pages/home.html`; no `@import` in it). The check is now: local `_`
    partials only, found by the static finders, every `@import` of that form, no `@import` in the bundle — and the
    tokens, logical properties, no URL, no `!important` and the forbidden wording run on each imported partial too:
    wider than before. Partials are followed one level; the passage imports nothing, and the bundle check catches any
    import left.

### 3. Do the loader changes keep what the loader's tests protect?

Yes. Every behaviour the three browser tests protected is still asserted — the 10 s lease, the refused second submit of
a guarded form, the rest and the next submit; nothing waits without the state machine; no state on a control that is
not a `.btn` — on today's markup, and `test_loader_rules` pins the release in the catch. All of `test_loader_w1_d.py`
passed in my run, the lease included.

### 4. Is the chip decision right?

Yes. `test_the_chip_is_drawn_by_one_sheet` failed on step 1's base `8e13cd2` and passes on the merged tree with nothing
changed here: W3-F1's budget pass (`7cdaba8`, `3ff62c9`, on design-v5 since its merge) consolidated W3-F1's and W3-F2's
two drawings into one rule of the shared partial `static/css/v5/_pagina.css` and registered it in the test's `placed`
map. The rule (`justify-self: start; margin-block-start: var(--s-2)`) places the chip and paints nothing — what the
test's docstring allows outside `v5/chip.css` —, and `_lettura.css` and `_interior.css` name the chip only in comments.
The file passed in my run.

### 5. Does anything change a family's design?

No. No stylesheet changed: the 22 CSS bundles are design-v5's, so the shared payload and every page type stand where
DL54-129 put them. The one template is the dev showcase's comment. The JS restores W2-A's designed trap, keeps the
resize re-read's behaviour, and touches the loader only where loader.js is missing.

## Findings — none holds the merge

**m1 · The worktree as left fails `test_css_bundle_is_current.py::test_no_source_is_newer_than_its_output`.** Five
sources — `apps/portal/static/portal/console.css`, `journey.css`, `templates/portal/situation.html`,
`apps/pages/static/pages/css/pages.css`, `static/css/v5/_journey-passage.css` — were rewritten between 23:53:12 and
23:53:37 on 15 October (the two corrections' mutation probes, restored: git is clean), after the bundles of 22:31. The
content is current: the 22 CSS entries rebuilt in memory are byte for byte the committed ones; the commits are right
and a fresh clone passes. *Fix:* the merge's clean rebuild, already planned (or a rebuild in this worktree before a
suite runs here). Nothing to commit.

**m2 · The catch is the one release only while every guarded form submits through a `.btn`.** A guarded form sent by
another control returns early in shell.js (`if (!control && !form.dataset.loaderHost) return;`): loader.js is never
imported, and main.js's guard is never lifted — loader.js present or not. True today (the profile, the deletion
request, every allauth form through its `button` element), pinned by no test. *Fix:* a static test — every
`data-single-submit` form's submit buttons are `.btn` — or lift the guard on that early return too.

**m3 · main.js's guard comment (`initMisc`) still names loader.js as the guard's only lifter.** shell.js's catch is now
the other. *Fix:* one line.

**m4 · Fix (b)'s path has no behavioural test.** No overlay test resizes an open dialog: the 400 % test reads the stop at
the opening. *Fix:* a resize step there — open at a large size, resize, the stop follows; resize back, it goes.

**n1 · The guard correction's wording and reach.** The written reason says one importer «would force the vocabulary to be
drawn twice, or into the shared console bundle»; a third way existed — the vocabulary as its own page-only entry,
linked by both page types — and DL54-128 item 4 records why W3-D did not take it (one request fewer). *Fix:* cite it.
The chain check follows `{% extends %}` only: sound today (every journey and documents sheet is linked in a page's
`extra_head` with `{{ block.super }}`; the one variable `{% extends %}` is `templates/429.html`), but a sheet linked from
an included partial would escape it — say so in the comment.

**n2 · For the merge's decision-log entry.** This branch supersedes two recorded rules: DL54-112's «ONE importer» (now:
never the entry and a page sheet; a page loads a partial once) and `3093261`'s `@import` ban on the home's sheet (now
on the bundle the home links).

**Info, no action.** Part 2 settles inside `open()`, so `overlay:close` fires before `overlay:open` from within one call;
a listener that keeps state set just before `open()` would lose it on that path — `piece-drawer.js` sets `registerUrl`,
opens, and its `overlay:close` clears it. Unreachable today (every product close is the module's); worth remembering
if a template ever gains a `method="dialog"`.

## Seen on the way — outside this branch (not counted)

- **A year of cache on three fixed-name scripts.** `config/settings/base.py` sets `WHITENOISE_MAX_AGE = 31536000` (set
  at the bootstrap, 17 September). WhiteNoise gives every non-versioned file `max-age=31536000,
  public` (`add_cache_headers`; hashed names stay `immutable`), and three entries are imported by a fixed name from
  inside the bundles (four import sites), where the manifest storage rewrites nothing: `loader.js` (from `shell.js` and `piece-drawer.js`),
  `depot.js` and `piece-drawer.js` (from `console.js`). After a release that changes one of them, a returning browser
  can run its cached old copy against the new pages for up to a year (the old chunks it imports are still served:
  `collectstatic` never runs with `--clear`). The DevOps owners' and W1-D's to weigh: a short `WHITENOISE_MAX_AGE`
  (the hashed files keep their immutable header whatever it says), or content-hashed names for the entries imported
  dynamically.
- **The live server can draw a port Chromium refuses.** This machine's dynamic TCP range starts at 1024 (`netsh int
  ipv4 show dynamicport tcp`: 1024 + 64 511), so a session's live server can land on one of the ~19 ports Chromium
  refuses in that range — the steward's W3-A run drew 4045. Rare, but a browser-suite flake with no cause in the code;
  a conftest that hands `--liveserver` a free port above 10080, or Windows' default range, removes it.

## Not checked

- GitHub's Linux runner (the SO_LINGER layout was proved in a container by the steward, not by me); Firefox and WebKit
  (not installed).
- The full suite — the steward's second pass: 5 108 passed and 3 failed on `a059610`, the three fixed on `34c5471`
  (954 passed around them), 519 browser tests passed on `34c5471`. I ran the targeted static tests and the overlay,
  console, loader and piece-drawer browser suites.
- design-v5's newer tip `f447c28` (sec-f5): the merge step's.

## The lane, cleaned

Lane 3 only: the test database `test_test_ile_v5_l3`; the dev server on 8783 for the probe, stopped (port free); 8780
never touched. One pytest and one browser at a time; no crash. Nothing written in the worktree but this file: the
bundle rebuilds ran in my scratch directory or in memory, the probe and the mutation plugin live in my scratch
directory and are not committed, and `git status` stayed clean through the review. Another session's non-browser
pytest ran meanwhile on lane 5's database; it did not touch lane 3's.
