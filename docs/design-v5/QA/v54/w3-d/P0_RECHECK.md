# W3-D · The journey «La soglia» — P0 re-check

Label `w3-d-p0-recheck`, 12 October 2026. This pass re-checks only the blocking items of the accessibility +
performance check (`A11Y_PERF.md`, SHIP_AFTER_FIXES). That check had **one** blocking item, finding 1. Its two minor
findings and the senior review's items are outside this pass. This pass checked branch `v54-w3-d` at `2f9a827`, after
the fix pass («Review fixes» in `NOTES.md`: `02a0774`, `c1c8f6b`, `c844c84`, `d95c4b0`, `2f9a827`). It compared the
branch with design-v5 at `1c03e3b`, whose CSS is identical to the merge base `d40f209`. This pass changed no code. The
only file it wrote in the worktree is this report.

## Verdict — SHIP

**Finding 1 is closed.** The console pages' shared payload (main + console + portal) is now **49 614 B gzip −9**, against
the hard ceiling of **50 927 B** (DL54-87, V5.8): **1 313 B under**. Before the fix it was 51 530 B, 603 B over. The
rail's drawing is now a page-only sheet, `css/dist/portal/journey.css`. That sheet loads on exactly the pages that draw a
journey, and on no other console page.

## Finding 1 — what was checked

**1 · The shared payload, before → after (V5.8).** Each committed bundle was compressed with gzip −9 (mtime 0, the
DL54-87 method; it gives back 41 880 / 7 072 / 1 975 B on the merge base):

| Bundle | design-v5 `1c03e3b` (= `d40f209`) | before the fix `be2fb31` | `HEAD` `2f9a827` |
|---|---|---|---|
| `dist/main.css` (every page) | 41 880 | 40 599 | 40 599 (byte-identical to before) |
| `dist/portal/console.css` | 7 072 | 8 956 | **7 040** |
| `dist/portal/portal.css` | 1 975 | 1 975 | 1 975 (byte-identical) |
| **console pages: main + console + portal** | **50 927** | **51 530 (+603 over)** | **49 614 (1 313 under)** |
| `dist/portal/journey.css` (page-only) | — | — | 2 688 (13 692 raw) |

**2 · The committed bundles match a clean build.** HEAD's CSS sources were exported to a scratch folder, its
`static/css/dist/` was deleted, and `node scripts/build_css.mjs` was run. The build produced the same 15 files as HEAD's
committed `static/css/dist/`, **byte for byte (0 differ)**. The weights above are therefore what a rebuild of HEAD's
tree gives. `journey.css` becomes an entry by the build's own rule, because it is an app sheet that is not a partial.
Nothing was added to the build.

**3 · What left the shared bundle, and where it went.** These are the selectors of the committed bundles, before the
fix and at HEAD:
- **`console.css`:** 467 → 337 selectors. It lost 130 and gained none. Every selector it lost belongs to the rail
  (`journey*`, `tl*` and `wstep*`). The few lost selectors that `journey.css` does not carry are rules the fix pass
  changed: m1 renamed `tl__row--last` to `--latest`, and m3 rewrote the step-7 rules.
- **`main.css` and `portal.css`:** byte-identical before and after the fix.
- **`journey.css`:** carries only the rail. It has no `@import` and no `url()`, and its one `transition` is
  `transition:none`.
- **Rail-looking selectors still in `main.css`:** both are older than the fix. The first is `static/css/v4/wizard.css`'s
  legacy Stepper (`.wstep*`), which leaves with the consolidation after W3-F1's merge (the review's M4). The second is
  one bidi rule in `static/css/v5/base.css` (`.journey__when, .tl__when`).

**4 · Where the sheet loads (lane 8786 on `ile_v5_l6`, headless Chromium, 26 loads, no crash).** Evidence:
`C:/tmp/ile_v5_council/evidence/v54/w3-d/p0-recheck/` (`probe.json`, `probe.log`, 16 crops, `weigh_refs.txt`,
`split_check.json`).
- **Which pages link it.** The four journey pages link `css/dist/portal/journey.css` in this order: main → portal →
  console → journey. They are the dashboard, «Mon parcours», the case file and «Ma situation», checked with
  `seed-person` (threshold A) in fr and ar at 1440 and 390, `qa-doc-person` (step 1) on the dashboard and the case file,
  and `qa-fresh-person` on «Ma situation».
- **Cascade order.** That link order puts the rail in the same cascade position it held as `console.css`'s last import.
  The CSS uses no `@layer`, so splitting the sheet changes no cascade result.
- **The sheet is served and applied.** Each load received journey.css with status 200, and the page parsed 119 rules,
  113 of them style rules; 22 to 83 of those match elements of the page. The page also computed values that only this
  sheet sets:
  - at 1440: the rail's container `journey / inline-size` and the level line as a 9-column grid (mirrored in ar);
  - at 390: the card and its closed disclosure, with the summary shown;
  - on the case file: the spine and the timeline;
  - on «Ma situation»: the Stepper's line;
  - on all four: `pointer-events: none` on every line, and «Mon parcours»'s 32 px `.journey-page`.

  The crops show the drawing whole.
- **Pages without a journey.** These pages do not load the sheet and carry no rail element: Communications, Mes
  documents, Mes échéances and Mes demandes (`seed-person`), the dashboard and «Mon parcours» of `qa-fresh-person`
  (no file), and `qa-company`'s dashboard. They load only the shared three sheets, plus `documents.css` or
  `companies.css` where those pages already loaded them.
- **Clean loads.** 0 CSP reports, 0 console errors, 0 responses ≥ 400, 0 horizontal overflow.

**5 · Targeted tests** (`test_ile_v5_l6`, one run, `-m "not browser"`): **15 passed**. They cover:
- five tests from `test_journey_w3_d.py`: the page-only sheet, a person without a file, «Mon parcours», the dashboard
  and the case file;
- `test_console_shell_stylesheets.py`;
- `test_css_bundle_is_current.py`;
- `test_static_pipeline.py`, including a real `collectstatic` under the production storage.

## For the merge step (not findings)

- **Weigh again at the merge.** Weigh main + console + portal on the bundles rebuilt from a clean dist at the merge.
  design-v5 can move before then: the steward's `DESIGN_V5_MERGE_LOCK` (w2-a-merge) has been held since 00:39. The
  figure above is good for design-v5 at `1c03e3b`.
- **The trade V5.8 prescribes.** A person with a file now gets their dashboard in four sheets. That is 52 302 B: +772 B
  and one more request than before the fix. Every console page without a journey carries 1 916 B less, and the four
  journey pages share the one cached sheet.

## The lane, cleaned

Four sessions were minted with `Client.force_login` on `ile_v5_l6`, with no password used, typed or stored. They are
revoked: 4 rows deleted, and the cookie file removed. The server on 8786 is stopped, and no browser of this role is
left running. The benchmark lock was absent at the build and at the browser series, and this pass never created it.
The export's `node_modules` junction was removed with `rmdir` before the export was deleted; design-v5's
`node_modules` is intact. Scratch files are in `C:/tmp/ile_v5_council/.work/w3-d/w3-d-p0-recheck/` and the browser
profile in `C:/tmp/ile_v5_council/.profiles/w3-d-p0-recheck/`.
