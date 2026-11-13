# W4-C — Accessibility + performance check (w4-c-a11y-perf, 16 October 2026)

One pass, independent of the builder's harness (my own probes, `C:/tmp/ile_v5_council/.work/w4-c/w4-c-a11y-perf/`), on the
branch `v54-w4-c` at `5ea1ce2` (design-v5 `fad36e0` + F1 + P1 + the reports). Plan §3.6 item 3, §2.6, §1.6, §1.8 / SP-8;
WCAG 2.2 AA; V5.5, V5.9 §15 («accessibility critical checks», «performance sanity check»), V5.10. Lane 4: the dev server
8784 from this worktree on `ile_v5_l4` (`ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`, `--noreload`, no preview
flag); signed-in pages through two sessions minted with `Client.force_login` (qa-doc-person, qa-person) by a scratch
script outside every repository — no password used, typed or stored; revoked at the end (2 rows deleted, file removed).
One headless Chromium (headless shell 1243) at a time, profile under `.profiles/w4-c-a11y-perf/`; every browser series
after the lock gate; the perf windows held `PERFORMANCE_BENCHMARK_LOCK` themselves (13:40–13:46, 13:48–13:55,
13:55–13:58, 14:06–14:12). No run crashed. Evidence: `C:/tmp/ile_v5_council/evidence/v54/w4-c/a11y-perf/`.

## Verdict — SHIP_AFTER_FIXES

- **F1 and P1 do what they say, in fr and ar, at 1440 and 390, under forced colours.** No WCAG failure, no performance
  regression comes from either on the normal path, and P1 removes the upload page's layout shift with no LCP cost.
- **One regression introduced by the branch (major, small): P1's lost-module path.** It is the senior review's M2,
  found here independently. A remedy that needs no JS is measured below.
- **One pre-existing AA failure confirmed (major, small): «Ma situation» 1.3.5.** It is the review's M1; I confirmed it
  by reading the form, not with my probes (limits).
- Nothing blocks. No P0.

## Accessibility — what was checked, and what it read

My method differs from the sweep's on purpose. A focus indicator is read **on the pixels**: each Tab stop is captured
focused, then with the focus taken away and given back. «Visible» means the screen changed; its contrast is the
contrast of that change. 2.4.11 is read by hit-testing 15 points of the focused element against fixed and sticky
layers. Hit areas are measured outward from the element's centre. Walks run under reduced motion, so no motion
pollutes the diff.

| Check | Views | Result |
|---|---|---|
| Keyboard walk, real Tab presses, focus read on the pixels | 56 views. Touched: the resume form, the upload, a piece, «Mes pièces», the Conditions gate (403). Sample: home, login, a door page, an interior page, dashboard, case file, journey, «Ma situation», 404. Each × fr, ar × 1440, 390. | **1 624 stops.** None lacks a visible indicator. None is entirely under a fixed or sticky layer (2.4.11). The skip link is the first stop everywhere. 4 stops are partly covered: the login's password field by its own show-password toggle, drawn inside the field. The change contrast is ≥ 3.44 : 1 on every stop but one. The exception is the home's CTA (2.04, the plate's navy → laguna fill): its 2 px outline at a 6 px offset measures **5.7 : 1** against the paper (`cta/`). |
| axe-core 4.13.0 (from disk): WCAG 2.0–2.2 A/AA plus best practice | The 56 views, plus F1's error state (4 views) | **0 violation nodes** |
| Forced colours (emulated), the same walk | 28 views: the 4 touched pages, home, dashboard, case file | **768 stops**, every one indicated; the lowest change 11.31 : 1. The Dépôt's ring 21 : 1; F1's summary 15.13 : 1. States are legible on the stills. |
| Reduced motion is a real still | The 56 views | Frame-to-frame change **0 px**; 0 running animations. The Dépôt's states under reduced motion (file chosen, refusal) also run 0 animations. |
| At rest without reduced motion | 26 views (13 page types × fr, ar at 1440) | **0 running animations, 0 `will-change`** (§2.6 Motion) |
| 400 % (320 × 256) | 28 views (14 page types × fr, ar) | **0 px** horizontal overflow. The fixed layers take ≤ 66 px of 256: the console's bottom bar (66 px fr, 55 px ar), the case file's and the questionnaire's action bars (61 px), the sticky letterhead (57 px). |
| 1.4.12 (WCAG values in a constructed sheet) | 32 views at 1440 and 390 | No overflow. The only newly clipped text is the rail's account name, cut with an ellipsis by design; the name is shown whole beside it. |
| Text contrast on the pixels | The touched pages, fr + ar, 1440: 330 text boxes. 9 boxes were not painted and are left out: the closed language menu's items, and one box cut at the viewport's edge. | **None under 4.5 : 1.** The lowest are «Italy» in the lock-up (5.19, 20 px) and the primary buttons' labels (5.29, 15 px / 500). The lowest ratios of text under 16 px run from 5.29 to 6.87 : 1; no V5 rule demands 7 : 1 on these elements (DS tables: 4.5 for text). Arabic text is ≥ 14 px. |
| Targets (hit-testing) | Every view | 2.5.8 holds. At 1440 the breadcrumb links are 20–22 px tall but pass by the spacing exception (axe `target-size` 0). At 390 (coarse pointer) every hit area is ≥ 44 px (SP-8) wherever the viewport edge or the fixed bar does not cut it: re-measured in view, «Remplacer la pièce» is 322 × 44. The login's «Lire la Privacy Policy» carries a 48 px band under a finger (`entrance.css`); my probe saw it cut by the viewport's bottom edge. |
| Names, roles, live regions | Touched pages | axe 0. The Dépôt's input is labelled «Fichier *» / «الملف *», described by its formats, then by the refusal. Its two regions: `role="status"` says the chosen file («attestation-w4c.pdf — PDF · 1 ko»); `role="alert"` says the refusal verbatim. |

**F1 — the resume form's errors (fr, ar × 1440, 390, plus forced colours).**
- An empty answer submitted from the keyboard (Enter in the field) lands the focus on the summary: `role="alert"`,
  «Le formulaire contient des erreurs.» / «يحتوي النموذج على أخطاء.». Its ring is visible (3.7 : 1; 15.13 under forced
  colours) and nothing covers it.
- Tab reaches the summary's link «Code de reprise». Enter puts the focus on the field, ring visible; the field is
  `aria-invalid` and described by its help and its error.
- A malformed code («ABC») gives «Ce code n’est pas valide.» in the summary and under the field.
- axe reports 0 in the error state.
- Note: the endpoint's own throttle (10 posts per 10 min) answered my first Arabic run with its 429 page. That page is
  accessible too. The Arabic cells were re-run after the window (`pass-resume-ar.json` supersedes the Arabic half of
  `pass-resume.json`).

**P1 — the Dépôt (upload and piece pages, fr, ar × 1440, 390).**
- The zone is drawn at its final size from the first frame: 76 px, 96 px in Arabic at 390. The input lies transparent
  over the frame and the title shows.
- Tab reaches the input. The zone's ring is visible (3.94 : 1; 21 : 1 under forced colours), and nothing covers it.
- Enter opens the picker (a file-chooser event). The chosen file's row and its announcement follow.
- A `.txt` file is refused on its row; the input becomes `aria-invalid` and is described by the refusal; the refusal is
  announced.
- In Arabic the mark sits at the inline start, at both widths (checked on the geometry).
- On «Mes pièces», the piece drawer opened from the keyboard focuses its Dépôt's input with the ring (4.11 : 1). Esc
  gives the focus to the piece's row (W3-C's rule).

## Performance — on the lane, against W1-0

The lane is a DEBUG dev server with uncompressed static files. Its absolute timings are not the twin's; an A/B on the
same lane is comparable. Protocol:
- Cold loads, a fresh context each, cache disabled.
- Profile A (150 ms RTT, 1.6 / 0.75 Mbps) and CPU × 4.
- Observers registered at document start: LCP and its element, FCP, CLS (the largest session window, input excluded,
  with its sources), long tasks after FCP, Resource Timing.
- n = 5 interleaved per cell, then the Arabic cells at n = 9 with the two arms strictly alternated.
- P1's A/B: the same page and data, with `documents.css` and with the sheet before P1 (`3ca0b0c^`). **Both arms are
  served through the same request interception.** My first run intercepted only the «before» arm. An intercepted
  response skips the network throttle, and that gave a spurious +100–240 ms; the second run corrects it (both runs are
  in `perf/`).

| P1's A/B (`perf/runs-depot2.jsonl`, `runs-ar-ab.jsonl`) | After P1 | Before P1 |
|---|---|---|
| CLS — the upload page, fr 1440 / fr 390 / ar 1440 / ar 390 | **0.000** (max 0.0005) | 0.059 / 0.042 / 0.067 / 0.071 (on every load; the builder's twin figures to the third decimal) |
| CLS — a piece's page, same cells | **0.000** | 0.030 / 0.023 / 0.035 / 0.034 |
| LCP, paired difference (after − before) | Arabic, n = 9 alternated: medians **+32 / −4 / +16 / −16 ms**. French, n = 5: −20 / −44 / −32 / +44 ms. All within §2.6's +50 ms. | — |
| LCP element | Unchanged: `p.ws-head__lead`, `p.doc-piece__rule`, the Arabic heading's `span` at 1440 | the same |
| Long tasks after FCP | Same pattern in both arms (≤ 236 ms at CPU × 4 on both); none after load + 1 s. **None introduced.** | — |

- **Bytes.** `documents.css`: 5 497 → 5 494 B (gzip −9, mtime 0). `main.css` 31 799, console 7 134, portal 1 045,
  `wizard.css` 4 114 B: unchanged. The JS dist is untouched. Nothing is beyond §2.6: the area lowers one page sheet.
- **Requests.** No new request comes from this area:
  - upload and piece: 4 CSS + 9 JS (W1-0: 4 + 8);
  - «Mes pièces»: 5 + 9 (W1-0: 4 + 8);
  - resume: 2 + 6 (= W1-0).
  The ↑ predate W4-C and are recorded in PERF.md: V5.8's page sheets and the helpers chunk, W4-B's O3.
- **LCP element against W1-0.**
  - «Mes pièces»: V5's lead paragraph (`p.ws-head__lead`; W1-0's `p.doc-page__lead`) at 1440, the register's title at
    390 fr. It is not worse: on the twin these pages' LCP medians are 1 096–1 304 ms, against W1-0's 1 552–1 692 ms.
  - The resume page: `p.ingresso__lead`.
- **Nothing loops.** After load there are only one-time fetches:
  - L2's loader module and its chunk, which the Dépôt asks for once it is wired;
  - the portico's four door photographs, at 1440, on the public page.
  0 animations are running at the end, and no long task falls after load + 1 s.
- **The resume page:** 1 of its 12 lane loads shifted 0.066 at fr 1440: `nav.main-nav`, then the chapter body. This is
  the letterhead's intermittent shift (W3-F2 O1), which the builder handed to W2-C1. F1 is not the cause: a GET renders
  nothing new. Median 0.000, against a 0.10 budget on this non-flagship page.

## Findings

### Major

**A1 — P1 removed the Dépôt's fallback when its module does not arrive** (= REVIEW M2, measured independently).
- **What P1 did:** `html.js` (set by `head.js`) now draws the zone: the input is `opacity: 0` over the frame. But
  `html.js` does not mean that `depot.js` arrived. `console.js` imports it with no failure path.
- **Measured:** with `static/js/dist/depot.js` aborted, a chosen file shows **nothing** (`depot/depot-upload-fr-1440-nomodule-chosen.png`).
  Before P1, the browser's own control stayed visible and named the file (`…-nomodule-preP1-chosen.png`).
- **Why it matters:** the submit still posts, but the picker on the core upload task is silent. This is the branch's
  one regression.
- **Fix:** take the review's M2 fix, or the CSS-only one measured here. The CSS-only fix is two rules in `_depot.css`
  (page-only sheet; the input is `required`):

```css
.js [data-depot]:not([data-enhanced]) .doc-depot__zone > input[type="file"]:valid { opacity: 1; }
.js [data-depot]:not([data-enhanced]) .doc-depot__zone > input[type="file"]:valid ~ * { visibility: hidden; }
```

  - **Measured in the page through a constructed sheet:** with the module blocked, the chosen file's native control
    shows in the frame, and the zone stays 76 → 76 px (no shift). On the normal path the rule never matches.
    Evidence: `depot/fallback2-*.png`.
  - My first variant (`position: static`) overflowed at 390 (`fallback-blocked-390.png`), so it is not the one to take.
  - **The CSS-only fix also covers** a lost `console.js` and browsers without modules. The review's `.catch` does not
    cover those, and it needs a JS rebuild.
  - **Either fix satisfies this check** if a browser test aborts the module and asserts the chosen name is visible.

**A2 — «Ma situation» declares no input purpose for the date of birth and the country of residence** (WCAG 1.3.5;
= REVIEW M1, confirmed).
- `apps/accounts/profile_forms.py`, `SituationForm`: `date_of_birth` is `DateInput(type=date)` with no
  `autocomplete="bday"`, and `country_of_residence` has no `autocomplete="country-name"`. The profile form's own
  `country_of_residence` already carries it.
- Fix: the two widget attributes, plus the test the review names. `nationality` has no HTML purpose token; leave it.
- Not caught by my probes (axe does not test 1.3.5).

### Minor

**a1 — the Dépôt's polite region keeps the previous file's sentence after a refusal** (W3-C, pre-existing).
- After the client guard refuses a second file, `role="status"` still reads «attestation-w4c.pdf — PDF · 1 ko», while
  `role="alert"` says the refusal.
- Nothing is announced twice. A virtual-cursor reader can still meet the stale line.
- Fix: in `depot.js`'s refusal path, `say(live, "")` on the polite region, or empty it in `clear()`. No merge action
  needed.

**a2 — the letterhead's intermittent shift, seen on the lane too.** One load at 0.066 on the resume page; its median is
0.000. It stays the builder's hand-off to W2-C1 (W3-F2 O1). It is not this branch's regression.

## Tests and limits

- **Targeted tests, run once each:**
  - 219 non-browser passed: `test_depot_w3_c`, `test_css_bundle_is_current`, `test_orientation_w3_f1`,
    `test_documents_w3_c`, `apps/orientation/tests`;
  - 21 browser passed: `test_depot_browser_w3_c`, `test_orientation_browser_w3_f1`;
  - database `test_ile_v5_l4`, one pytest at a time.
- **Chromium only.** No WebKit or Firefox binary is on this machine, and none was downloaded. No real device; no screen
  reader run by a person: names and announcements are read from the DOM and the accessibility tree.
- **My sample is not the census.** It is the touched pages plus 9 page types. The sweep's 101-page matrix and the
  review's 396 views at 1366 and 360 cover the rest.
- **1.3.5 and the language of parts** were not probed here.
- **The lane is not the twin.** P1's A/B is lane-relative; the absolute figures belong to PERF.md and the review.
