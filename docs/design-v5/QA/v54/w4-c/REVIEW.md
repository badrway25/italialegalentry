# W4-C — Performance + accessibility consolidation: senior review

16 October 2026 · w4-c-review (reviewer; built nothing) · branch `v54-w4-c` at `5ea1ce2` (design-v5 `fad36e0` + this
area's F1, P1, reports and DL54-159) · plan §3.6 item 3, §2.6, §1.6, §2.5; WCAG 2.2 AA; V5.5 (one review, then fix,
then ship), V5.8 (no shared ceiling raised), V5.9 §15, V5.10.

**Verdict: SHIP_AFTER_FIXES.** Nothing blocks. The release candidate is accessible and fast on what I measured, in
French and in Arabic, at 1440, 1366, 390 and 360. My own pass found 0 axe violations and 0 overflow. Every keyboard stop
has a visible indicator, and no focused element is hidden under a bar. The overlays trap and return the focus. The
reduced-motion state is truly still. LCP stays at 1.6 s or less and CLS at 0.023 or less on the compressed build of
this branch, and the upload page's shift is gone (0.000).

Two things must be fixed before the merge. Both are small:
- **M1** — a WCAG 1.3.5 failure that the sweep missed on «Ma situation». So the report's line «no WCAG 2.2 AA failure
  on any page type» is not yet true.
- **M2** — P1, this branch's layout-shift fix, removed the Dépôt's fallback when its script module does not arrive.

The four minors are polish and paperwork. No re-review is needed after the fixes; only a P0 would call for one.

## How it was checked

- **My lane:** 127.0.0.1:8884, served from this worktree on `ile_v5_l4` (the lane's own clone) with
  `ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`, `--noreload` and no preview flag. The server ran in two modes:
  - first as the dev server, for the accessibility pass;
  - then as a **compressed instance of this branch**, for the performance spot check. It used the twin's own settings
    module (`settings_8782`: DEBUG off, WhiteNoise's `CompressedManifestStaticFilesStorage`, finders off, the
    2026-10-03 clock), with only two changes: its own `STATIC_ROOT` and `ile_v5_l4`. `collectstatic` reported
    617 files copied and 1 455 post-processed, the twin's own figures; `main.css` was 31 865 B gzip, `immutable`.
  - The twin 8782 itself was never touched.
- **Browsers:** one headless Chromium (Playwright 1.63, headless shell 1243) at a time, with its own profile. Every
  series waited for `PERFORMANCE_BENCHMARK_LOCK`, and the performance runs held it. No run crashed.
- **Sessions:** minted with `Client.force_login` for 9 personas (no password used, typed or stored). All 9 were revoked
  at the end, and the secrets file was removed.
- **Evidence:** `C:/tmp/ile_v5_council/evidence/v54/w4-c/review/` — `probe/`, `walk/`, `depot/`, `resume/`, `motion/`,
  `forced/`, `reflow/`, `spacing/`, `stills/`, `overlays/`, `perf/`.
- **Scripts:** `C:/tmp/ile_v5_council/.work/w4-c/w4-c-review/`.

| Pass | What | Result |
|---|---|---|
| Probe at the two widths the sweep did not measure | 99 page types (the census, less the two lane-only bridges W4-C deleted), fr and ar, at 1366 × 768 and 360 × 780 (touch): 396 views. Checks: axe-core 4.13.0 (WCAG 2.0–2.2 A/AA plus best practice), plus the experimental rules the sweep did not run (`label-content-name-mismatch`, `p-as-heading`, …); overflow; CSP; the input purposes. | **0 violations**, 0 px overflow, 0 CSP reports. The experimental flags are patterns, not failures: the rail's brand name differs only by its dash, the hero's origin links are named by their title word, and the empty-state and register titles are not headings. **The input-purpose read found M1.** |
| Keyboard walk | Real Tab presses: 36 walks at 1366 × 768 (18 page types) and 26 at 360 × 780 (13), fr and ar, 1 966 stops in all. | **0 stops without an indicator**; **0 hidden under a fixed or sticky layer** (2.4.11). One stop is partly under the phone bar: the 218 px textarea of a new help-desk request (fr), which AA allows. |
| Overlays from the keyboard | The phone sheet and the console drawer at 360, the case file's state dialog at 1366, the portico door at 1366 and 1440; fr and ar. | The modals move the focus in (the dialog to «Annuler»), keep it there over 25 Tabs, close on Esc and return the focus to the opener, visibly. The door (a disclosure) leads the next Tab into its panel; Esc closes it and sets `aria-expanded="false"` on the door. |
| P1, the Dépôt | The upload and requirement pages, fr and ar, at 1440, 1366, 390 and 360. | Drawn at its final size from the first frame. The keyboard ring is visible (a solid laguna border plus the 2 px ring), and the chosen file's row appears. Without script, it is the browser's own control. **With script but the module blocked: M2.** |
| F1, the resume form | Submitted empty, fr and ar, at 1366 and 360. | The focus lands on the summary (`role="alert"`, 2 px ring), which links to `#id_token`. The field is `aria-invalid` and described by its help and its error. RTL is correct. |
| Reduced motion | Home fr and ar, login, dashboard, journey ar, a door page; at 1366 and 360; sampled at 0.3 / 1.2 / 2.5 / 4.5 s. | **0 animations** at every sample under the setting. Without it, the hero's discovery (35 / 29 animations) and «Il varco» (16) finish before 4.5 s; nothing is running and 0 `will-change` is left at rest. |
| Forced colours · 400 % · 1.4.12 | 8 page types, fr and ar: forced colours at 1366 and 360; 400 % at 320 × 256; text spacing at 360. | Every state and indicator is drawn; 0 px overflow on all 16 reflow views; no text lost under the spacing. |
| Performance spot check | On the compressed instance, the §2.6 profile: profile A plus CPU × 4, cold, a fresh context per load, interleaved. 24 cells, n = 5 (training ar 1440: n = 9), 124 loads under the lock. INP: 3 overlays × 5 cold opens. | Table below. LCP medians 1 068–1 604 ms. CLS medians ≤ 0.020; the upload and requirement pages 0.000 on every load. INP ≤ 152 ms. |
| Static | `check_ownership.py w4-c design-v5`; the CSS weights at gzip -9; line endings. | PASS (3 inside, 1 slice, 1 generated, 3 delegated). `main.css` 31 799 B and the console page type 39 978 B, both unchanged. `documents.css` 5 497 → 5 494 B. All eight changed files are LF. |
| Tests | Non-browser targeted tests: `test_depot_w3_c`, `test_orientation_w3_f1`, `test_css_bundle_is_current`, `test_documents_w3_c`, `apps/orientation/tests`. Browser targeted tests: `test_depot_browser_w3_c`, `test_orientation_browser_w3_f1`. Run on `test_ile_v5_l4`. | **219 passed** (non-browser). **21 passed**, 0 skipped (browser). |

**The performance spot check** (the compressed instance of `5ea1ce2`; medians, with min–max in brackets):

| Cell | n | LCP ms | CLS median / max | CSS + JS before `load` | JS gzip B | Fonts B |
|---|---|---|---|---|---|---|
| home fr 1440 · ar 1440 | 5 · 5 | 1 580 (1 304–1 616) · 1 604 (1 508–1 744) | 0.020 / 0.023 · 0.018 / 0.018 | 3 + 7 | 24 138 | 20 956 · 53 184 |
| home fr 390 · ar 390 | 5 · 5 | 1 268 · 1 532 (1 340–2 264) | 0.000 · 0.000 | 3 + 7 | 24 138 | 20 956 · 53 184 |
| login fr 1440 · ar 390 | 5 · 5 | 1 324 · 1 472 | 0.016 / 0.023 · 0.000 | 2 + 7 | 18 462 | — |
| door (pathways) fr 1440 · ar 390 | 5 · 5 | 1 156 · 1 312 | 0.015 / 0.023 · 0.000 | 2 + 6 | 16 781 | — |
| training ar 1440 · fr 1440 | 9 · 5 | 1 328 · 1 128 | 0.013 / 0.018 · 0.010 / 0.023 | 2 + 6 | 16 781 | — |
| FAQ ar 390 | 5 | 1 296 | 0.000 | 2 + 6 | 16 781 | — |
| dashboard fr 1440 · ar 390 | 5 · 5 | 1 436 · 1 328 | 0.000 / 0.001 · 0.000 | 4 + 8 | 19 168 | 23 644 · 55 872 |
| «Mes pièces» ar 390 · fr 1440 | 5 · 5 | 1 472 · 1 216 | 0.000 · 0.000 / 0.003 | 5 + 9 | 27 510 | — |
| upload fr 1440 · ar 1440 · ar 390 · fr 390 | 5 each | 1 068 · 1 276 · 1 224 · 1 076 | **0.000 / 0.000** on all four | 4 + 9 | 24 491 | — |
| requirement ar 1440 · fr 390 | 5 · 5 | 1 432 · 1 176 | 0.000 · 0.000 | 4 + 9 | 24 491 | 63 144 · 30 916 |
| case file fr 1440 · ar 390 | 5 · 5 | 1 304 · 1 344 | 0.000 / 0.001 · 0.000 | 7 + 8 | 20 765 | — |
| journey ar 1440 | 5 | 1 272 | 0.000 | 5 + 8 | 19 168 | — |

INP, cold opens at CPU × 4 (n = 5 each, all opened and closed):

| Overlay | Open | Close |
|---|---|---|
| Console drawer (ar 390) | 88–104 ms | 32 ms |
| Public sheet (ar 390) | 104–152 ms | 48–56 ms |
| Piece drawer (fr 1440) | 72–112 ms | 48–64 ms |

The tasks of 50 ms or more after FCP reach 267 ms at CPU × 4 (case file ar 390). They are the same first-layout tasks
PERF.md traces.

These figures agree with PERF.md within the noise of a shared machine. My protocol is the sanity rule W4-C used
(n = 5), not §2.6's n ≥ 9 «no worse» proof: no cell came near a budget.

## The brief's checks

| Gate | Result |
|---|---|
| No WCAG 2.2 AA failure on any page type, fr and ar (names, keyboard, focus visible and not obscured, contrast, forced colours, 400 %, 1.4.12, target size) | **Not yet: M1** (1.3.5 on «Ma situation»). Everything else in the list holds, both in W4-C's sweep (1440 and 390) and in this review (1366 and 360, plus the walks and stills above). |
| Every page type within §2.6's budgets on the compressed twin, with the protocol stated | **Holds where a budget is a gate:** LCP, CLS, INP and JS ≤ 45 KB on public pages (the largest public page, the home, loads 24 138 B). PERF.md states its protocol (n = 5, interleaved, profile A plus CPU × 4, the lock, the windows) and measures HTTP/2. **Four letter-of-the-budget exceptions** are recorded as PASS or «recorded» without an acceptance: m4. |
| Fixes in the owning families' files; no shared ceiling raised; no visual regression | Both fixes land in their owners' files: F1 in `templates/orientation/resume.html` (W3-F1) and P1 in `_depot.css` (W3-C), with the generated sheet and W3-C's test. Shared bundles are unchanged. There is no visual change on the normal path. **P1 regresses the no-module path: M2.** |
| Limits stated, not hidden | Yes, in NOTES.md, A11Y_SWEEP.md and PERF.md: no WebKit or Firefox binary, no real phone, and no screen reader run by a person. |

## Findings

### Major

**M1 — «Ma situation» does not declare its input purposes (WCAG 1.3.5, AA).**
- **What happens:** the situation form asks for two facts about the person whose purposes are in WCAG's list, and
  declares neither:
  - `date_of_birth` → `bday`;
  - `country_of_residence` → `country-name`.
- **Where:** `apps/accounts/profile_forms.py`, `SituationForm`, l. 148–153 and l. 160–165.
- **Scope:** every «Ma situation» page (`qa-doc-person`, `qa-person`, `qa-fresh-person`), fr and ar, at every width.
  The read: `review/probe/*situation*-1366.json`, `fields[].ac` = `null`.
- **Why it was missed:** axe does not flag a missing `autocomplete`.
- **Precedent:** the same class was fixed on the profile form in the same file (W3-F2's A2, DL54-98: `name`, `tel`,
  `country-name`). The situation form two classes below was left out.
- **Fix:** `widget=forms.DateInput(attrs={"type": "date", "autocomplete": "bday"})` and
  `widget=forms.TextInput(attrs={"autocomplete": "country-name"})`. This is a delegated path through the steward
  (the file's existing slice is the profile form's).
- **Test:** the two attributes asserted beside W3-F2's profile test.
- **Then:** amend A11Y_SWEEP.md's verdict and DL54-159 to name the fix.

**M2 — P1 removed the Dépôt's no-module fallback.**
- **What P1 did:** it keys the enhanced drawing on `html.js`, which `head.js` sets in `<head>`. That drawing makes the
  input `opacity: 0` over the frame, shows the frame's own words, and reads the keyboard ring from `:focus-within`
  (`_depot.css` l. 196–228). Before P1, the drawing waited for depot.js's own `[data-enhanced]`.
- **The gap:** `html.js` only says that a script ran; it does not say that `depot.js` arrived.
  `static/js/src/console.js` l. 187–191 imports the module with no failure path. Its own contract reads: «without it
  the Dépôt is the browser's own form».
- **Measured:** I aborted `static/js/dist/depot*.js` at 1366 and 360, in fr and ar
  (`review/depot/upload-*-blocked-chosen.png`, `depot.json`). A chosen file then shows **nothing**: no row, no name,
  and the native control is invisible. Before P1, the browser's own control stayed visible and named the file (as the
  no-script capture `upload-*-nojs-chosen.png` shows).
- **Why it matters:** the submit still posts, but a silent picker on the core upload task invites repeat picks and
  abandonment. The failure (a dynamic import lost on a poor mobile connection) is uncommon but real. This is the
  branch's one regression.
- **Fix** (keeps P1's 0.000):
  - in `console.js`, `.catch(() => document.documentElement.classList.add("depot-off"))` on the import;
  - in `_depot.css`, one block that gives the input its place back under `.depot-off`: `position: static`,
    `opacity: 1`, sizes auto; the zone wraps; the title is hidden;
  - the JS dist rebuilt (the steward rebuilds it from clean at the merge anyway);
  - a browser test in W3-C's `test_depot_browser_w3_c.py` that aborts the module's route and asserts the chosen
    file's name is visible;
  - correct the two comments: `_depot.css` §2 bis («With script…») and console.js 2d.

### Minor

**m1 — The letterhead still shifts on desktop public loads, and the hand-off names a closed family.**
- **What happens:** `nav.main-nav` moves on 24 of my 34 desktop public loads (0.009–0.023 each). PERF.md counts 11 of
  860 public loads above 0.03, one of them at 0.109 (training, ar 1440).
- **Why it is minor:** under every gate at the median, but above §2.6's 0.01 target, and visible.
- **Fix:** plan §3.6 says Wave 4's fixes land in the owning family's files through the steward, as F1 and P1 did.
  Either reserve the menu row's block size here (fallback metrics or a fixed `block-size` on the letterhead's row,
  W2-C1's `chrome.css`), or hand it to W4-D by name with that rule. «For W2-C1» has no one to do it.

**m2 — «Privacy Policy» and «Cookie Policy» carry no `lang="en"` on the Arabic (and French) pages.**
- **Where:** the letterhead footer and the console footer on every page, the login's «قراءة Privacy Policy», and the
  contact page's link (3.1.2).
- **Why it is minor:** defensible as the documents' proper names.
- **Fix:** W3-F2's A4 hand-off is answered in NOTES.md §4 as «already fixed», but only the error pages and the legal
  page's h1 are marked. Either mark the standalone labels, or write the proper-name reading in A11Y.md and correct the
  answer.

**m3 — The meta row's label colon is French typography in every language.**
- **What happens:** `static/css/v5/card.css` l. 233 draws `content: "\00a0:"`, so Arabic reads «الطبيعة :»,
  «آخر تحقق :» on the interior pages' facts row (English and Italian get the space too).
- **Fix:** scope the space to `:lang(fr)` and give the others a bare colon. This is W1-C's sheet, not this branch's;
  seen here because the review looked at Arabic at 360.

**m4 — Four budget letters are recorded as PASS without an acceptance.**
- **The four:**
  - the overlay core is 6 523 B against §2.6's 4 KB per module (DL54-95: «not met»);
  - Arabic console pages that load ILE Mono load 63 144 B of fonts against the 56 KB Arabic budget (55 872 B
    without it);
  - the entrance pages load one script request over W1-0's count (the 394 B helpers chunk);
  - the tasks after FCP are read as «the rest of the first render».
- **Why it is minor:** none has a measured cost (re-measured above: LCP ≤ 1.6 s, INP ≤ 152 ms), so V5.5 says ship.
- **Fix:** write them as accepted exceptions — one line in DL54-159 and the release notes' known limits — rather than
  as PASS.

## What holds, and is good work

- **The sweep:** 404 views per pass, six passes, the probes' by-design patterns read on stills and named. Of the
  claims I re-measured, the AA verdict is the one that did not hold (M1).
- **The fixes:** P1 is the right fix for the shift: the shift is gone at n = 9 and here at n = 5 on all eight cells.
  F1 makes the last odd form answer like the others.
- **The hand-offs:** every Wave 4 hand-off is answered with a measure: the drawer's INP edge, the seven sheets of the
  case file, O1–O3, the helpers chunk.
- **The lane:** left clean. The lane-only accounts are deleted (0 left), the sessions revoked, and the twin returned to
  design-v5's tree.

## Limits (said)

- **Chromium only:** no WebKit or Firefox binary, no Safari, no real phone, no screen reader run by a person. Names,
  roles and live regions were read from the DOM and the accessibility tree.
- **Where the spot check ran:** on a compressed instance of this branch with the twin's settings, not on 8782 itself.
  It used a lane database clone, on a shared machine (≈ 4.6 GB free), at n = 5.
- **What this review did not repeat:** the 1440 / 390 sweep. It re-read the claims at 1366 / 360 and by targeted
  checks.

## For the fix step

1. **M1:** `apps/accounts/profile_forms.py` (two widgets) plus a test, as a delegated path.
2. **M2:** `static/js/src/console.js` (the `.catch`), `apps/portal/static/portal/v5/_depot.css` (the `.depot-off`
   block and the comment), and `tests/frontend/test_depot_browser_w3_c.py` (the blocked-module test). Then
   `npm run build`; the JS dist and `documents.css` are generated. Re-measure the upload page's CLS on the compressed
   build (it must stay 0.000) and re-run the two Dépôt test files.
3. **m1–m4:** fix m1 here or name W4-D in the hand-off, and correct the three report lines (A11Y_SWEEP verdict, NOTES
   §4 A4, PERF m4 exceptions). m3 goes to W1-C's sheet if the steward wants it in this merge.
