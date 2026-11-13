# W4-A — Mobile + RTL sweep: senior review

16 October 2026 · w4-a-review (reviewer; built nothing) · branch `v54-w4-a` at `4b61dcc`, merge base design-v5
`b06ea1e` · plan §3.6 item 1, §1.4 SP-7 / SP-8, §1.12 (N13, N14, N19), §2.5 (RTL), §2.6 · V5.5 (one review, then fix,
then ship), V5.8 (shared CSS ratchets down).

**Verdict: SHIP_AFTER_FIXES.** Nothing blocks. The sweep is careful, and its fixes are right, small and placed in the
owning families' files. On a phone the product reads as one product, in French and in Arabic. The chrome stays at
114 px or less, nothing overflows from 320 to 932, every title sits in the first screen (landscape included), and the
mirrors are coherent. The shared payload goes down.

Two items are major:

- **M1:** on «Mes pièces», in Arabic, a Latin file name stands at the far edge of its card (390) and of its cell (1440).
  It is the same defect class this area fixed in D23. It was missed because the visual pass looked at first screens
  only.
- **M2:** the verification is unfinished. Ten browser test files for the modules this branch changed never ran, and
  neither did a live look at 1366. The shared database has been down since about 15:35.

There are three minor items. After the fixes, no re-review is needed; only a P0 would call for one.

## How it was checked — and what could not be

- **The live look did not happen, and the reason is the infrastructure, not the branch.** The plan was a lane server on
  127.0.0.1:8886 from this worktree, on `ile_v5_l6`. The shared PostgreSQL in Docker (127.0.0.1:5439) did not answer
  during the whole review. The connection timed out on every 45-second poll from 16:44 to the end of the review
  (`E/review/dbwait.log`). The Docker engine hangs (`docker ps` and `docker version` never return) and the WSL VM does
  not respond.
- **No Django page renders without that database,** so no page was loaded on 8886. Docker was not restarted from here:
  other lanes and the owner's preview depend on it. It is the orchestrator's call.
- **What the review rests on instead:**
  1. **The implementer's real-page captures.** They were taken on this lane, on this branch's final tree:
     `E/after/`, `E/after2/` and `E/after3/` under a finger, plus `E/fix1/smoke/` with each fix's component at 1440
     (mouse) and 390 (finger), fr and ar. 212 contact sheets were read, about 40 of them closely. Details were
     enlarged where an RTL order or alignment was in doubt, by cropping the halves of a line, never by reading a
     transcription.
  2. **An independent re-aggregation of the probe records** (`after/coarse/results.jsonl`, 1 908 loads):
     - the worst chrome is 114 px;
     - no load overflows;
     - no title falls outside the first screen;
     - 410 targets are under 44 px under a finger: 373 are the dev showcase's own, 36 are «Ma situation»'s Stepper at
       320 (40 px, its gutters spent), and 1 is a glossary term in landscape at one scroll position.
  3. **Every changed line of the diff was read** (40 paths) against the plan and the rules the families already set.
  4. **The static tests ran:** 98 passed. They cover the area's static tests, `test_css_bundle_is_current.py`,
     `tests/i18n/test_rtl_static.py` and `test_static_pipeline.py`.
  5. **The bundles were weighed again from git with gzip -9:**
     - `dist/main.css`: 31 799 → **31 716 B**;
     - `dist/portal/console.css`: 7 134 → 7 126 B, so the console page types fall by 91 B;
     - the page-only sheets grow by less than `main.css` loses, so every page type is lighter (NOTES §4 confirmed).
  6. **`scripts/check_ownership.py w4-a design-v5` ran:** 3 inside, 1 slice, 13 generated, 22 delegated, 1 outside
     (m3).
  7. **One suspicion was tested in headless Chromium and cleared** (Notes below). The test used a static file, so it
     needed no server.
- **Evidence and scripts:** evidence of this review is in `C:/tmp/ile_v5_council/evidence/v54/w4-a/review/`; the
  scripts are in `C:/tmp/ile_v5_council/.work/w4-a/w4-a-review/`.

## The brief's checks

| Check | Result |
|---|---|
| Phone chrome ≤ 120 px | **Holds.** 114 px at most: the console's 48 px top bar plus the bottom bar with two-line French labels at 360. The public letterhead is 57 px. In landscape the console's top bar leaves with the page; only the 56 px bottom bar stays. |
| First object in the first viewport | **Holds** at every width, on the short height and in landscape. Before D12, the error pages in landscape put the title half out; D12 fixed it. |
| Targets ≥ 44 px on coarse pointers | **Holds** on product pages. What is left is the showcase, the Stepper at 320 (40 px, which still passes WCAG 2.5.8) and the glossary term in landscape. SP-8 is read with WCAG 2.5.8's inline exception: a link inside a sentence is not widened over the lines around it. **Agreed.** |
| No overflow 320–430 (and landscape) | **Holds:** 0 in 1 908 loads. The Arabic stress probes widen 18 page states, and only through fixed interface strings that never hold a person's words. |
| Arabic mirrored where it must be | **Mostly holds.** Coherent across the home, login, the phone sheet, the console drawer, the dashboards, the case file, documents, «Ma situation», Academy, the help desk, «Mon parcours», the company pages and the error pages. **Except M1.** |
| Never mirrored (logo, targa, numbers, references) | **Holds:** the lock-up is `direction: ltr` with the mark first; the door stage and the key; the steps glyph; references and dates are isolates. D8 (a phone number laid out right to left) is fixed. |
| Landscape and short heights usable | **Holds.** Sheets and drawers that are taller than the screen scroll, and no action bar traps the page. |
| No shared ceiling raised; desktop unchanged | **Holds where it was captured.** `main.css` and the console bundle both fall. Each change is scoped to `(pointer: coarse)`, to below 64rem, to a landscape-height clause, or to selectors nothing draws. Where it is not scoped it is neutral at desktop: `inline-block` on a stand-alone link, 2 px of inline padding. The 1440 smoke pairs show nothing moved. **1366 was captured by no one (M2).** |

## Findings

### Major

**M1 — In Arabic, Latin file names stand at the far edge of «Mes pièces»' file list, at 390 and at 1440.**

- **Where:** «جميع ملفات حسابكم» («Tous les fichiers de votre compte»):
  - `templates/portal/documents.html:67`, `<span class="doc-files__name" dir="auto">`, which
    `apps/portal/static/portal/v5/_table.css:85` makes `display: block`;
  - the same class in `templates/documents/index.html:58` (loose files);
  - the depot's answer `.doc-filed__name` (`templates/documents/partials/depot.html:79`, `_depot.css:470`).
- **What happens:**
  - `dir="auto"` resolves «diploma.pdf» to left-to-right, and the block's `start` then means *left*.
  - On a phone, the card's first line is the file name, flush left. Its gloss («Diplome ou titre de formation») and
    its facts line («شهادة أو مؤهل · 292 بايت · 21.09.2026») end on the reading edge, on the right.
  - At 1440, the name sits at the left of the «الملف» cell while the column head and the gloss sit at its right.
  - Seen in the lane's own captures: `E/fix1/smoke/documents-aside__ar__390.png` and `__ar__1440.png`, cropped in
    `E/review/docs_ar_halves.png` (the name alone in the left half) and `E/review/docs_ar_1440_crop.png`.
  - Reproduced off the lane, in a static page that loads this branch's own `main.css`, `console.css` and
    `documents.css` with the table's markup (`E/review/m1_mock.py`, `m1_compare_358.png`):
    - at 358, a Latin name stands 248 px from the cell's right edge while its gloss touches it;
    - at 1000, the name is 320 px from the right edge and the gloss 16 px;
    - with the rule proposed below, both names sit 0 px and 16 px from the right edge;
    - an Arabic file name is unchanged.
- **Why it is major:**
  - «Arabic mirrored where it must be» is this area's core check, and «Mes pièces» is a flagship page.
  - The project already has a rule for exactly this case. W3-E applies it as `.file-history .tl__detail:dir(ltr)
    { text-align: end }`, as `.reg-page .portal-facts dd[dir] { justify-self: start }`, and as the head rule that D23
    extended. W3-F1's m7 states it: «a HEAD ends on the reading edge».
  - An Arabic reader sees each card's link hanging on the wrong side.
  - It escaped the sweep for two reasons. The visual pass covered first screens only (212 sheets × 8 first
    viewports), and this list lies below the fold. The probe's alignment check accepts an element whose own direction
    is left-to-right.
- **Same pattern elsewhere, not drawn by the lane's data:**
  - `.reg-party__name dir="auto"`: an organisation's name in the case file's parties, a need's actors, and the
    selection's responsible actor (`templates/cases/detail.html:182`, `templates/companies/need_detail.html:70`,
    `templates/selection/partials/responsible.html:24`);
  - it is grid-stretched inside `.reg-party__words` (`_registers.css:789`), so a Latin name would stand at the left
    while its label stands at the right;
  - the same static page with `registers.css` confirms it (`E/review/party_mock.py`, `party_compare.png`): at 358,
    «Agenzia Formazione Veneto S.r.l.» stands 60 px short of its label's reading edge, and on the edge with the rule.
- **Fix, in the owning sheets** (W3-C's `_table.css` and `_depot.css`; W3-E's `_registers.css`):
  1. Apply the established rule, for example
     `:dir(rtl) :is(.doc-files__name, .doc-filed__name, .reg-party__name):dir(ltr) { text-align: end; }` and its
     mirror for an Arabic name on a French page. Alternatively, keep the block in the page's direction and put the
     name in an inline `<bdi>`.
  2. Re-probe «Mes pièces» (both routes), the loose upload and the case file, in fr and ar, at 390 and 1440.
  3. Grep the other block-level `dir="auto"` sites (137 in `templates/`) for the same case.
  4. Look at the full page at 390 in Arabic, not only its first screen, on the pages that print people's data:
     documents, the case file, requests, the help desk, Academy and company needs.

**M2 — The verification is not complete.**

- **The ten browser test files did not run.** NOTES §5 names them for this branch's changed modules:
  - `test_orientation_browser_w3_f1.py` (`wizard.css`);
  - `test_journey_browser_w3_d.py` (`_journey-stepper.css`, `_journey-passage.css`);
  - `test_dashboard_browser_w3_b.py` (`_dashboard.css`);
  - `test_documents_browser_w3_c.py`, `test_depot_browser_w3_c.py` and `test_drawer_browser_w3_c.py`
    (`_workspace.css`, `_depot.css`, the console shell);
  - `test_content_pages_browser_w3_f2.py` and `test_service_pages_browser_w3_f2.py` (`_lettura.css`, `errori.css`,
    `500.html`, `faq/index.html`);
  - `apps/portal/tests/test_browser.py` and `apps/pages/tests/test_browser.py`.
- **Why:** the shared PostgreSQL stopped answering at about 15:35 and was still down for this whole review.
- **The live look did not happen either.** This review's pass on 8886 (fr and ar at 1440, 1366, 390 and 360) did not
  start. Nobody has looked at 1366 with the changes; the smoke covers 1440 and 390.
- **Fix:**
  1. Once the database answers, run the ten files green: one pytest at a time, under the benchmark lock.
  2. Look at the smoke list of components (`E/fix1/smoke/`) at 1440 and 1366 under a mouse, and at 390 and 360 under
     a finger, in fr and ar. Add M1's pages.
  3. Never merge on the unrun set.

### Minor

**m1 — D10 centres «Profil» and moves it 6 px off the account block's start edge on a phone.**

- `apps/portal/static/portal/v5/_dashboard.css:856` sets `justify-content: center` on `.db-account__links a`.
- In French at 390, «Profil» starts at 22 px while «Mon compte» and the line above it start at 16 px
  (`E/review/acct_fr.png`).
- The 44 × 44 px comes from the box's `min-inline-size`, not from the centring. Drop the line: the box grows at its
  end and the target is unchanged.

**m2 — French spacing is still missing beyond the two strings D15 fixed.**

- About 140 `{% translate %}` lines in `templates/` (138 outside `templates/dev/`) still have an ordinary space beside
  « » : ; ? !.
- So does the company NowPanel's label, built in `apps/companies/services.py:507`: «Transmettez le besoin « %(title)s »
  au projet».
- Examples:
  - «Lire la page « Attention aux fraudes »» in the phone sheet's foot (`templates/partials/main_nav.html:73,96`) and
    in the anti-fraud callout;
  - «Voir le parcours « Formation dans le pays d’origine »» and «Découvrir « Vivre en Italie »»
    (`templates/pathways/training.html:41,50`), the very links D5 widened.
- A phone can still start a line with «»» or «:», or end one on «««.
- **Fix:** pass the remaining team-authored strings through `typo` (W2-D's filter), family by family or once where
  those components render, and measure at 360 and 375. Otherwise record it for W4-D beside D14. The locked copy stays
  B1's.

**m3 — The ownership check fails until the merge step writes one path.**

- `check_ownership.py w4-a design-v5`: 1 path outside, `static/css/dev/showcase.css` (D13), so the check reports FAIL.
- NOTES already hands it to the merge step, which writes it into `OWNERSHIP_V54.json` as W4-A's slice or the
  steward's. It is listed here so the merge does not skip it.

## Notes — checked, no change asked

- **W4-B's O2 (rail tools at 36 px under a mouse).** The plan's own D06 row (§1.18) gives the rail «a pinned rail foot
  and one density step on fine pointers (S-1)». W3-A's 36 px under a mouse is that step, and under a finger the tools
  are 44 px. The hand-back can be closed as conforming.
- **French heads and leads on Arabic pages.** On the door pages, Academy's course and enrolment, and the forms'
  consent, a French head ends on the Arabic reading edge while its lead keeps its own start. This is the deliberate
  rule of W3-F1's review m7 (`static/css/v5/_interior.css` §7), not a defect.
- **The company NowPanel's French need title inside Arabic guillemets.** It wraps as «Soudure» … «métallique» at the
  line ends. This was checked in Chromium against controls: one word, `<bdi>`, and a pure Arabic quote
  (`E/review/bidi.png`, `glyphs.png`, `prod_glyphs.png`). The guillemets are mirrored correctly for an RTL reading.
- **D17 withdrawn — agreed.** In a right-to-left paragraph «1 / 8» reads from the right, like «الخطوة 1 من 7» beside it.
- **Accepted residue:**
  - D14 (B1);
  - the 429's «;»;
  - the Stepper at 320 (40 px);
  - the glossary term in landscape;
  - D24 (a dev page).
- **The tests.** The area's static tests are regex reads of the sheets, in the project's style; its Chromium tests hold
  the behaviour. Nit: `test_the_500_keeps_its_semicolon_with_its_words` asserts a literal U+00A0. Write it `\u00a0`,
  as the FAQ test does and as `pages_typo.py` asks.

## For the fix pass and the merge step

1. **M1:** the rule in W3-C's and W3-E's sheets; re-probe «Mes pièces», the loose upload and the case file in fr and
   ar at 390 and 1440; grep the `dir="auto"` blocks; look at full pages at 390 in Arabic for the pages that print
   people's data.
2. **m1:** one line deleted. **m2:** the `typo` pass, or a W4-D record.
3. Rebuild `static/css/dist` from clean and re-weigh: `main.css` must stay ≤ 31 799 B and the console page types
   ≤ 39 978 B.
4. **When the database answers:** the ten browser files (M2), the 1366 and 1440 look at the smoke components, and the
   area's own `test_mobile_rtl_w4_a.py` browser half again after the fixes.
5. **m3:** the manifest entry for `static/css/dev/showcase.css`.
