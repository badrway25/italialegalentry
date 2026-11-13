# W4-A — Mobile + RTL sweep — notes

Area W4-A of the V5.4 plan (`docs/design-v5/V5_4_EXECUTION_PLAN.md` §3.6 item 1; §1.4 SP-7 / SP-8, §1.12 N13 / N14 /
N19, §1.14, §2.5, §2.6), worked in the owner's delivery mode (V5.5: implement → review once → fix → ship) under the V5.8
CSS budget (the shared bundles never rise). Branch `v54-w4-a`, worktree `C:/tmp/ile_wt/v54-w4-a`, from design-v5 at
`a833403` (tag `v54/wave-4`), design-v5 merged in at `0a8351b` (the W4-B merge) before the fixes and again at
`b06ea1e` (the w4-d part 1 and sec-f8 merges) before the merge step. Implementer `w4-a-impl-1`, 16 October 2026.
Evidence outside every repository: `C:/tmp/ile_v5_council/evidence/v54/w4-a/` (E/ below); scratch scripts in
`C:/tmp/ile_v5_council/.work/w4-a/w4-a-impl-1/` (S/ below). Decision log: DL54-157 (first written as DL54-155, which the
w4-d merge took; renumbered after design-v5's DL54-156 at the pre-merge sync — the steward renumbers it again if
another entry lands first).

The area owns no files of its own (plan §3.6): every fix landed in the owning family's file; the paths are listed for
the merge step at the end.

## The lane

- Dev server 8786 from this worktree on `ile_v5_l6` (`ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`,
  `--noreload`, no preview flag); pytest on `test_ile_v5_l6`. One headless Chromium and one pytest of mine at a time,
  each browser on its own profile (`C:/tmp/ile_v5_council/.profiles/w4-a-impl-1-<mode>/`). The benchmark lock waited
  for before every browser series and every build — and, after W4-C took it back in the middle of the after-sweep, page
  by page (the sweep pauses while it is held). No browser run ended on a crash. Never 8780, 8782, Chrome 9222 / 9223.
- Signed-in pages through sessions minted with `Client.force_login` against `ile_v5_l6` by S/`mint.py` (no password
  used, typed or stored): `qa-doc-person` (the person with the file EE167596D4), `qa-person` (a file, the Conditions
  not accepted), `qa-fresh-person` (no file), `qa-company` (the company's pages), the organisations' bridge with
  `seed-company` (a company), `seed-actor` (a professional actor) and two accounts this area created **on the lane clone
  only** — `w4a-institution@example.test` (account type institution, `role:institution`) and
  `w4a-university@example.test` (university, `role:university`), no password: the census found no institution or
  university account on the clones, so their bridge had never been drawn —, and the staff pages with the role accounts
  (`demo-professionnel`: the help desk's queue and the permanent Forum's 503; `demo-operateur`: the dispatch and the
  operator's dashboard; `demo-acteur-autorise`: the selection's workspace).
- `qa-company` on `ile_v5_l6` is typed `person` (the 11 October correction was made on `ile_v5` only, SERVERS.md): its
  «Espace réservé» is a person's page there, so the bridge was drawn with the organisation accounts above.
- With `--noreload` the cached template loader keeps the first template it read: the server was restarted after the
  template changes and before the after-sweep.

## 1 · The sweep (before) — `SWEEP.md`

`SWEEP.md` holds the method, what holds everywhere, the defect legend (D1 … D21; D22 and D23 in its after section) and
the table page × width × language.
In short: 106 page states × fr, ar × 360 / 375 / 390 / 412 / 430, 844 × 390, 932 × 430, 390 × 640 and 320, under a
finger; 390 under a mouse; the Arabic overflow probes at 360 / 390 / 412 — **1 818 probed loads, 212 contact sheets,
each looked at** (S/`visual_before.md`, one line per sheet). The probe (S/`probe.js`) measures the overflow (the page and
every box), the chrome that stays on screen (at rest and at four scroll depths), the first object against the band the
chrome leaves, every target by `elementFromPoint` through its middle (its own `::before` / `::after` area counts, a
neighbour's does not), and in Arabic the flip list, the identity marks, text arrows, isolates and alignment.

**What holds everywhere:** the phone chrome ≤ 120 px (114 at most: the console's 48 px top bar and the bottom bar's
two-line French labels at 360); no overflow on any product page from 320 to 932; the first object in the first screen
(the error pages on a phone on its side apart, D12); the overlay contract's edges (the console drawer from the inline
start, the public sheet full screen on a phone and from the inline end from 48rem, the bottom sheets, the account menu a
sheet on a phone and a popover at the inline end beyond); the closed flip list mirrored in Arabic and no other icon; the
lock-up, the console's and the rail's marks, the door stage, the steps glyph (Q8), references and dates never mirrored;
landscape and short heights usable (the console's top bar leaves with the page under 480 px of height; every sheet and
drawer taller than the screen scrolls; no action bar traps the page).

## 2 · The fixes — each in its owning family's file

| id | severity | fix | file (family) |
|---|---|---|---|
| D1 | minor | the colophon's links 44 px both ways under a finger, the list's gap folded into its rows | `static/css/v5/chrome.css` §8 (W2-C1) |
| D2 | minor | the «aiuto» help line's link: a 44 px area under a finger on every page that draws it (one drawing, out of the reading pages' list) | `static/css/v5/_pagina.css` (W3-F1), `static/css/v5/_lettura.css` (W3-F2) |
| D3 | minor | the pending legal notice's address: a 24 px box, 44 px under a finger | `static/css/v5/_lettura.css` (W3-F2) |
| D4 | minor | orientation's resume link: one box whatever lines it takes, 44 px under a finger | `apps/orientation/static/orientation/wizard.css` (W3-F1) |
| D5 | minor | the passage's forward links and a consent's privacy link: one box, 44 px under a finger (the privacy link drawn once with the help line, for the door pages' forms too) | `apps/pathways/static/pathways/_pathways.css` (W3-F1), `static/css/v5/_pagina.css` |
| D6 | minor | the closed registration's link: a 24 px box, 44 px under a finger | `apps/forum/static/forum/_forum.css` (W3-F1) |
| D7 | minor | the documents' foot links and «Télécharger»: 24 px boxes; two foot links that wrap stand 20 px apart under a finger, so that their bands never overlap | `apps/portal/static/portal/v5/_workspace.css`, `_depot.css` (W3-C) |
| D8 | **major** | the company's contact e-mail and phone, each a left-to-right isolate (the phone's digit groups ran right to left on the Arabic page) | `templates/companies/profile.html` (W3-E) |
| D9 | minor | «Ma situation»'s Stepper takes from the gutters what its columns lack: eight 44 px columns from 360 (through its rail: the base sheet's `ol[role="list"]` reset outranks the class) | `apps/portal/static/portal/v5/_journey-stepper.css` (W3-D) |
| D10 | minor | the dashboards' account links 44 px wide under a finger («Profil» was 32) | `apps/portal/static/portal/v5/_dashboard.css` (W3-B) |
| D11 | minor | a short arrow link widened about its middle under a finger | `static/css/v5/buttons.css` (W1-C) |
| D12 | minor | a phone on its side (from 48rem under 30rem of height) seats the error pages' door at the end: the title was half out at 844 × 390 | `apps/cms/static/cms/errori.css` (W3-F2); W3-F2's test of the seat retargeted, intent kept |
| D13 | dev | the design showcase fits a phone: its grids hold their column, a sample's table scrolls in its region | `static/css/dev/showcase.css` (no owner: the steward's slice) |
| D14 | record | the locked French copy breaks beside its «:» and «« »» on a phone | B1 item 8 — not changed |
| D15 | minor | the FAQ's hint, a team-authored string, through the `typo` filter | `templates/faq/index.html` (W3-F2) |
| D16 | minor | the phone bar's title takes its own direction (`unicode-bidi: plaintext`): a French title with no `lang` on an Arabic page is cut at its own end | `apps/portal/static/portal/v5/_shell.css` (W3-A) |
| D17 | — | withdrawn: «1 / 8» read right to left on the Arabic page is the Arabic order, as «الخطوة 1 من 7» beside it | — |
| D18 | minor | the heads' words may shrink below their longest word: a company's name with a word longer than the column no longer widens the dashboard | `apps/portal/static/portal/v5/_frame.css` (W3-B / W3-E) |
| D19 | minor | the Forum's video controls never mirror | `apps/forum/static/forum/_forum.css` (W3-F1) |
| D20 | minor | the lock-up's link 44 px wide where it is the mark alone (320) | `static/css/v5/chrome.css` §1 (W2-C1) |
| D21 | minor | the passage's station words at 17 px below 64rem (RE-4) — W3-D's own line restored | `static/css/v5/_journey-passage.css` (W3-D) |
| D22 | minor | a meta row's part in the other direction than its row — a reference or a date, left to right on an Arabic page, a name in its own script — lays its point and its pull on the row's side (`flex-direction: row-reverse`): a «·» closed the Arabic help desk's and «Mes demandes»' lines, two points met on the staff queue's. Found by the re-sweep's look (§5) | `apps/portal/static/portal/v5/_registers.css` (W3-E) |
| D23 | minor | a saved result's French title on «Mon parcours» ends on the Arabic page's reading edge, wrapped or not: W3-E's head rule (its review's minor 6) reads `:dir()`, and this title's `lang` turns it through main.css — one selector added to that rule. Found by the re-sweep's look (§5) | `apps/portal/static/portal/v5/_registers.css` (W3-E) |
| D24 | dev · record | the dev showcase on the Arabic page: its French copy carries no `lang`, so its stops stand at the left and a swatch's hex reads «ecebe6#». Found by the re-sweep's look | `templates/dev/showcase.html` (no owner) — not changed |
| O1 (W4-B) | minor | on a phone a stop that Tab brings in from below keeps its whole ring: the public pages' scroll padding keeps 8 px at the foot (the ring's 2 + 2 px were cut by the screen's edge). Paid by writing D11's inline inset as its block one (the same area) | `static/css/v5/chrome.css` §3 (W2-C1); `static/css/v5/buttons.css` (W1-C) |

**Smoke** on the lane, every changed component scrolled to the middle of the screen, fr and ar, 1440 under a mouse and
390 under a finger, each pair sheet looked at (E/`fix1/smoke/_*.png`): nothing moved at 1440 (the error page's door in
its end seat, the footer's columns, the documents' table, the Stepper's spine); at 390 the footer's rows are 44 px, the
links that were runs are boxes, the Stepper's eight nodes fill the row, the company's phone reads «+39 0000 000000» on the
Arabic page, the enrolment's French title starts with its first word in the Arabic phone bar (2× capture, S/`look/`), an
Arabic title stays right to left.

## 3 · The hand-offs to this area

- **W3-D — «the door pages' station text stays 15 px on phones (RE-4 would be one line in `_journey-passage.css`)».**
  Taken: the line is restored (D21), below 64rem, for every page that draws «la linea»'s station words — the companies'
  door page, orientation, diplomas, training. The persons' door page draws stations without words; the home draws none.
  On a desktop the words keep 15 px (test: `test_the_station_words_read_one_step_up_on_a_phone`).
- **The design showcase overflows by 78 px at 390** (`templates/dev/showcase.html`, `static/css/dev/showcase.css`). It
  had grown to 202 px at 390 (126–304 across the widths; in Arabic the page's start was cut): the two-column grids'
  `1fr` let a sample table and the company panel's facts stretch their column. Fixed as the steward's slice (D13), the
  template untouched; the merge step assigns the path (below).
- **W4-B's «Seen on the way» (`QA/v54/w4-b/A11Y_PERF.md`), O1 and O2, both addressed to this area** — missed by the
  first pass of the grep below, found when it was run again at the end:
  - **O1 — «the home at 390: a focused link at the screen's bottom edge loses the bottom of its ring».** Taken (row O1
    in §2): measured on every public page state of the sweep, fr and ar, at 390 and 360 with the keyboard (S/
    `focusring.py`, E/`o1-before/`, E/`o1-final/`): 86 rings cut by 1–4.5 px of 2 480 stops → 0, none under the
    letterhead; a test holds it (red on the previous sheet).
  - **O2 — SP-8's 44 px.** The public footer's links and the dashboards' «Profil» under a finger: taken (D1, D10). The
    rail's foot tools at 36 px under a mouse: not a phone item — under a finger they are 44 (W3-A's coarse block in
    `_shell.css`, «these are the controls of the rail that a fine pointer finds at 36»), and below 64rem the rail is the
    drawer, whose rows are 44 for every pointer; whether SP-8's «the rail» asks 44 under a mouse too is W3-A's reading
    to confirm with the plan's owner — handed back, unchanged.
- **«W4-A» and «Wave 4» in the families' notes and the decision log** (`grep -n` over `QA/v54/*/NOTES.md`, `SHIPPED.md`,
  `REVIEW.md`, `A11Y_PERF.md` and `DECISION_LOG_V54.md`): beside W3-D's two lines and W4-B's O1 / O2 (above), no other
  mobile or RTL item (W4-D's and sec-f8's notes, merged at `b06ea1e`, name W4-A only to say they touch none of its
  files; W4-D's F-4 — the sign-in's invitation to a closed sign-up — is W2-B's page, «after W4-A»: copy, not layout).
  The others are W4-C's by the plan's own words — W2-A's REVIEW m1 (the drawer's cold open on the INP edge, «Wave 4's
  measure on a quiet machine and a real mid-range Android») and m2 (O10, the WebKit and Firefox smoke), W3-C's drawer and
  sheet in WebKit and Firefox (O10), DL54-95 item 7: plan §3.6 item 3 gives W4-C the cross-engine pass and the
  performance consolidation. Not taken here, said so.

## 4 · The payload — bundles rebuilt from a clean dist

Every page type's CSS (gzip −9 per sheet, summed: the stewards' `C:/tmp/ile_v5_council/.work/w2-a/w2-a-merge/weigh_pages.py`,
extended to DL54-151's page types in S/`weigh_ext.py`), design-v5 `b06ea1e` (the same CSS as `0a8351b`) → this branch's
final tree (E/`weigh_final.txt`):

| page type | design-v5 | W4-A | change |
|---|---|---|---|
| every page, and an interior page with no sheet of its own (`main.css`) — **shared** | 31 799 | 31 716 | −83 |
| console page types (+ console + portal) — **shared** | 39 978 | 39 887 | −91 |
| the login (+ entrance) · the home (+ hero + pages) | 36 660 · 46 160 | 36 577 · 46 081 | −83 · −79 |
| the company dashboard (+ companies) | 40 167 | 40 076 | −91 |
| «Mes pièces» (+ documents) · the documents' registers (+ panels) | 45 475 · 47 535 | 45 399 · 47 459 | −76 · −76 |
| a register page (+ registers) | 42 853 | 42 833 | −20 |
| «Mon parcours» with a file · a need's page · the help desk · an open request with its closure | 45 274 · 43 042 · 43 115 · 45 175 | 45 254 · 43 022 · 43 095 · 45 155 | −20 each |
| the selection · the Academy · the case file · the case file with its dialogs | 43 316 · 43 045 · 46 229 · 48 289 | 43 296 · 43 025 · 46 209 · 48 269 | −20 each |
| a journey page · «Ma situation» · an error page | 42 399 · 42 184 · 35 428 | 42 308 · 42 130 · 35 363 | −91 · −54 · −65 |
| the persons' door · the doors and the pilot · the Forum · orientation | 35 384 · 35 226 · 34 820 · 35 913 | 35 381 · 35 187 · 34 817 · 35 894 | −3 · −39 · −3 · −19 |
| the project pages · a reading page · a service page | 34 065 · 35 900 · 34 225 | 34 017 · 35 850 · 34 142 | −48 · −50 · −83 |

**Both shared bundles fall** (`main.css` 31 799 → 31 716 B, ceiling 31 906; the console page types 39 978 → 39 887,
ceiling 40 140) and **every page type is lighter than design-v5's**, so under every ceiling DL54-154 lowered to the
merged weights. The page-only sheets carry their families' fixes (the owner's V5.8 rule 2): the registers' sheet D22 /
D23 (2 875 → 2 946 B), `pathways.css` the passage's forward links (D5), `forum.css` the closed registration's link and
the video's direction (D6, D19) — each page type paid by `main.css` and the console bundle.

What paid (deleted, each proved unused by grep on design-v5 and on the in-flight branches W4-C, W4-D and sec-f8 —
templates, views, scripts; no stored text on the clones carries a class): `.form-row`, `.form-row--2` and `.is-warning`
(`v5/field.css`); `.t-title`, `.t-plate`, `.t-lead`, `.t-entry`, `.voyage__shore` and `.voyage__num` cut from
`v5/base.css`'s lists (the `--t-*` tokens of those names stay: the showcase reads them); the documents' old title classes
and the V4 grid's rule in the console's shell (`_shell.css`).

## 5 · The re-sweep (after) and the tests

**The same sweep on the fixed tree** (E/`after/`; S/`visual_after.md`, one line per sheet; `SWEEP.md` «After the
fixes»): 1 818 probed loads under a finger and the 74 overlay states, 202 under a mouse, 303 overflow probes in Arabic,
the lane restarted after the template changes and the profiles' caches emptied; every one of the 212 sheets looked at.
Against the before sweep:

- targets under 44 × 44 under a finger 16 464 → 410 — what is left is the dev showcase's own samples, «Ma situation»'s
  Stepper at 320 (40 px: the gutters are spent; 44 from 360) and one glossary term in landscape at one scroll position
  (its area under the sticky A–Z index); under a mouse 44 → 14, every one the showcase's;
- the first object out of the first screen 9 → 0 (D12); no overflow on any page at any width, the showcase included
  (126–304 px before); a phone number outside an isolate 1 → 0 (D8); the chrome 114 px at most, unchanged;
- the Arabic overflow probes widen 18 page states instead of 45, each through a fixed interface string only (a label, a
  button, a heading no person writes).

**Two fixes made during the after-sweep** (in §2's rows): the showcase's table region (`e4f54f3`, D13: an absolute
visually hidden label in the needs table still widened the page by 162 px at 390) and the 500's sentence through the
typo filter (`2a5592f`, D15).

**Two defects the after look found, present before** (D22, D23 — §2; `2b23963`): both in W3-E's `v5/_registers.css`.
Measured on the lane with S/`d22.py` (E/`d22-before/`, E/`d22-after/`: eight register pages, fr and ar, 390 and 1440):
24 rows with a part's point on the wrong side → 0; the saved result's French title, 184 and 124 px short of the Arabic
reading edge → 0 and 0; the French pages unchanged. The 25 page states that link the registers' sheet were then swept
again on the whole matrix (E/`after2/`: 450 + 50 + 75 loads, no crash) and their 50 sheets looked at
(S/`visual_after2.md`): nothing worse anywhere — the Arabic rows' first point is now clipped at the row's start as the
French one is (5 and 5 on the help desk, at every width). D24, the dev showcase's copy with no `lang` on the Arabic page,
is recorded and not changed.

**W4-B's O1** (§3; `a0f733b`): measured and fixed after that — 86 focus rings of 2 480 stops cut by the screen's bottom
edge → 0 (S/`focusring.py`). The shared sheet having changed again (the scroll padding's foot; D11's inline inset
written as its block one, the same area), the fourteen page states that draw an arrow link were probed again on the
whole matrix (E/`after3/`: 252 + 28 loads): identical to the after sweep on every measure.

**The pre-merge sync.** design-v5 merged in at `b06ea1e` (`71a96f9`: the w4-d part 1 and sec-f8 merges — no template,
stylesheet, script or bundle among them, so the dist stayed current); one conflict, the decision log's tail: design-v5's
DL54-155 and DL54-156 kept, this area's entry renumbered DL54-157. The ownership check: below.

**The tests** — one pytest at a time on `test_ile_v5_l6`, every file under the benchmark lock (the runner waits while it
is held), the targeted set and not the full suite, on the final tree (S/`run_tests.sh`, S/`tests_final.log`, each file's
output in S/`test_out/`); a first run, on the tree before O1, was stopped after eleven green files to take O1
(S/`tests_interrupted.log`; the twelfth, cut by the stop itself, passed in the run below), then everything ran again:

| file | result |
|---|---|
| `tests/frontend/test_mobile_rtl_w4_a.py` (the area's: the sheets' rules; in Chromium every short link, the lock-up at 320, the company's phone, a foreign title in the phone bar, the Stepper from 360, the error page on its side, the station words, a reference's point and a result's title on the Arabic page, the home's focus rings at 390) | 26 passed |
| `test_css_bundle_is_current.py` · `test_frontend_bundle_is_current.py` · `test_static_pipeline.py` | 5 · 5 · 3 passed |
| `test_design_docs.py` · `test_o14_lint.py` · `test_components_w1_c.py` | 40 · 53 · 30 passed |
| `test_case_file_w3_e.py` (the registers' sheet) · `test_service_pages_w3_f2.py` (with its retargeted assertion) · `test_layout.py` · `tests/i18n/test_rtl_static.py` | 22 · 47 · 29 · 81 passed |
| browser: `tests/i18n/test_rtl_browser.py` · `test_rtl_browser_overlays.py` · `test_header_fits_the_narrowest_viewport.py` | 23 · 5 · 5 passed |
| browser: `test_console_phone_browser_w3_a.py` · `test_console_shell_browser_w3_a.py` | 29 · 35 passed |
| browser: `test_nav_sheet_w2_c2.py` · `test_browser_w2_c1.py` · `test_browser_w2_c2.py` · `test_browser_w3_f1.py` | 11 · 12 · 25 · 12 passed |

**498 passed in 20 files, none failed, none skipped.** The ten browser files left in the list did not run: from about
15:35 the shared PostgreSQL in Docker stopped answering (connections time out after 60 s, the Docker engine answers 500,
`wsl.exe` hangs; free memory 4.6 GB of 32, the commit charge near its limit) — `test_orientation_browser_w3_f1.py` hung
after ten passing tests and was stopped with its browser, not counted. Not run, for the merge step to run once the
database answers: `test_orientation_browser_w3_f1.py`, `test_journey_browser_w3_d.py`, `test_dashboard_browser_w3_b.py`,
`test_documents_browser_w3_c.py`, `test_depot_browser_w3_c.py`, `test_drawer_browser_w3_c.py`,
`test_content_pages_browser_w3_f2.py`, `test_service_pages_browser_w3_f2.py`, `apps/portal/tests/test_browser.py`,
`apps/pages/tests/test_browser.py`. The shared engine was not restarted from this lane: other lanes (W4-C's merge holds
the merge lock) and the owner's preview depend on it.

`manage.py check` clean; ruff clean on the area's test file.

**What is left** — by design, recorded, or not this area's:

- D14 (record): the locked French copy's breaks beside «:» and inside «« »» — B1 item 8, the owner's and counsel's;
- the 429's «;», the same words as the 500's: never reached on the lane, and W2-B's test holds its exact sentence — left
  as written;
- «Ma situation»'s Stepper at 320 (40 px a column); the glossary's terms in landscape at one scroll position;
- the dev showcase's own samples under 44 px, and D24 (its copy has no `lang`) — a dev page, not a product surface;
- W4-B's O2 rail tools at 36 px under a mouse — W3-A's reading of SP-8, handed back (§3);
- WebKit, Firefox and real devices: W4-C's cross-engine pass (O10) — everything here is Chromium, emulated;
- the two accounts this area created on the lane clone `ile_v5_l6` only (`w4a-institution@example.test`,
  `w4a-university@example.test`, no password): left there for the merge step's and W4-C's looks at the organisations'
  bridge; they exist on no other database;
- the lane server 8786 is stopped; no Chromium of this lane is left running.

## Paths outside the slice — for the merge step

`scripts/check_ownership.py w4-a design-v5` on the final branch (merge base `b06ea1e`, 40 paths): **3 inside** (this
file's folder — `NOTES.md`, `SWEEP.md` — and `tests/frontend/test_mobile_rtl_w4_a.py`), **1 slice** (the decision log:
the area's append-only entry DL54-157 and its index row), **13 generated** (the CSS dist, rebuilt from clean), **22
delegated** (the owning families' files, each listed in §2 with its family — W1-A's `base.css`, W1-C's `buttons.css` and
`field.css`, W2-C1's `chrome.css`, W2-A / W3-A's `_shell.css`, W3-B's `_dashboard.css`, W3-C's `_workspace.css` and
`_depot.css`, W3-D's `_journey-stepper.css` and `_journey-passage.css`, W3-E's `_frame.css`, `_registers.css` and
`companies/profile.html`, W3-F1's `_pagina.css`, `wizard.css`, `_pathways.css` and `_forum.css`, W3-F2's `_lettura.css`,
`errori.css`, `faq/index.html`, `errors/500.html` and its test `test_service_pages_w3_f2.py`, one assertion retargeted
for D12 with its intent kept), and **one outside: `static/css/dev/showcase.css`** → FAIL until the manifest names it.
The file is in no family's slice (the showcase test's xfail says it has no owner; W3-D handed its overflow to «the
steward / the showcase's owner»): the merge step writes it into `OWNERSHIP_V54.json` as W4-A's justified slice («the
two-column grids' column and the sample table's scroll region, D13»), or as the steward's.

## Review fixes (w4-a-fix, 16 October 2026)

The one fix pass of `REVIEW.md` (M1, M2, m1 – m3, the nit) and of `A11Y_PERF.md` (its major and its four minors) — V5.5's
«fix». Evidence: `C:/tmp/ile_v5_council/evidence/v54/w4-a/fix2/` (F/ below); scripts:
`C:/tmp/ile_v5_council/.work/w4-a/w4-a-fix/` (W/ below). Six commits, one an item, each with its tests and the CSS dist
rebuilt from clean for its own state (`15bd79b` … `b2c761f`): each commit's static tests pass on its own tree, every
browser file on the last one.

**The lane, the shared database still down.** 127.0.0.1:5439 refused connections at 19:55 and again at 21:14 (Docker
Desktop's engine pipe gone); nothing was restarted from this lane. As the accessibility check did, the pass ran on a
scratch PostgreSQL 17.2 cluster of the machine's own binaries (W/`pg/`, 127.0.0.1:5479, trust on loopback only): the
lane's database by `migrate` + `seed_all` (the go-live state: G2 closed), and the records the survey needs built through
the domain's own services on the seed's synthetic accounts (W/`scenario.py`: pieces filed as «diploma.pdf», as
«شهادة الميلاد.pdf» and under a long Latin name, two loose files, the file's parties — an organisation named in Latin, one
in Arabic —, a contact request, a help-desk request, an Academy enrolment, the company's profile and a need with its
answerable party; no password set, typed or stored); signed-in pages through `Client.force_login` (W/`mint.py`, the
sessions revoked at the end); the tests on the same cluster (`TEST_DATABASE_URL=…:5479/test_ile_w4a_fix`: pytest builds
its own database from the migrations, so the shared server's data plays no part in a test). What still waits for
`ile_v5_l6` is said under M2.

| item | fix | where (family) | commit |
|---|---|---|---|
| M1 | a name in the other direction than the page ends on the page's reading edge — the registers' head rule, `:dir(rtl) X:dir(ltr), :dir(ltr) X:dir(rtl) { text-align: end }`, in the owning sheets | `.doc-files__name` in W3-C's `_table.css`, `.doc-filed__name` in W3-C's `_depot.css`; `.reg-party__name`, `.reg-step__text`, `.db-task__who` and `.data-table [dir]` joined W3-E's head rule (`_registers.css`); a record's reference packs to its summary cell's reading edge (`_registers.css`) | `15bd79b` |
| M1, the survey | the company's own name an isolate in the page's own h1 (W3-B's box rule `.db-head .ctx__title[dir]` deleted), its identity values the same, as the template's referent row already wrote them; the selection's team-written sentences isolates | W3-B's `companies/dashboard.html`, `_dashboard.css` and its test of the h1 (retargeted, intent kept); W3-E's `companies/profile.html`, `selection/partials/responsible.html`, `selection/process.html` | `15bd79b` |
| m1 | D10's `justify-content: center` deleted: the box grows at its end | W3-B's `_dashboard.css` | `c265620` |
| finding 1 | a notice's address alone in its paragraph (`.notice__body .email`): its line and 2 px, a 44 px band under a finger — the go-live notice on every public form; D3 is that rule now (out of `_lettura.css`); D6 stays the Forum's, its link a page's | W1-C's `v5/notice.css`, W3-F2's `_lettura.css` | `cb992c8` |
| finding 2 | the phone bar's account button draws its ring inside its 44 px, as the bottom bar's entries do | W3-A's `_shell.css` | `4727f8d` |
| found on the way | a loose file's act («حذف», 31 px in Arabic) 44 px wide about its middle under a finger — the icon buttons' own band | W3-C's `_table.css` | `a161806` |
| m2 | the strings the review named through W2-D's `typo` | W2-C2's `partials/main_nav.html` and its test of the sheet (retargeted); W3-F1's `pathways/_antifraud_callout.html`, `pathways/training.html`, `orientation/result.html` | `b2c761f` |
| the nit | the 500 test's no-break space written as an escape | this area's test | `15bd79b` |

**M1 — what was measured.**

1. The reviewer's sites, re-probed: «Mes pièces» on both routes, the loose upload's answer and the file's parties, fr and
   ar, at 390 and 1440 — and held in Chromium by the tests below.
2. The grep made a probe, so that the 137 `dir="auto"` sites are read where they render, not only where the data shows
   them: W/`survey.js` on 25 console pages × fr, ar × 390 under a finger and 1440 under a mouse — every block whose
   direction is not its container's, each of its lines' gap to the container's reading edge, once with the pages' own
   words and once with each `dir="auto"` text swapped into the other script, the names a person may type
   (F/`survey_compare.txt`). Before (the branch's head), the class stood on seven components beyond the reviewer's
   three; after, on none: «Mes pièces» 248 px short of the reading edge at 390 and 591 at 1440 (the loose files 198 /
   186), the French page's Arabic names 236 / 533 → 0; the file's parties 174 / 428 in Arabic and 107 / 475 in French → 0;
   a need's party 60 / 830 → 0; the need's skills 246 / 377 → 0; its history's note 271 / 494 → 0; the process's «who»
   281 → 0; a request's reference 57 / 260 → 0; the company's head 117 → 0. What the probe still flags is by design: a
   person's or the team's prose — a help-desk turn, a letter, a lead, an Academy row's summary, a wrapped fact value —
   keeps its own start (W3-F1's review m7; W3-E's facts rule), and a meta row's part keeps its 20 px pull (D22).
3. The whole pages at 390 in Arabic, looked at (F/`after/sheets/`: documents, the file, the requests, the help desk,
   Academy, the company's dashboard, profile and need, the selection). The look found one more defect of the family on
   the selection's pages: French sentences an actor or the team wrote — an authorisation's scope, a piece of evidence
   and its detail, a step's note in the journal — laid out right to left, their period at the far end
   («.Documents déposés…»); isolates now (W/`punct.js`: 12 → 7 on the 25 pages, the 7 left false positives — an Arabic
   sentence that opens with «PDF», paired brackets the bidi algorithm resolves, checked on pixels).

**M2 — the verification.**

- **The ten browser files**, one pytest at a time under the benchmark lock, on the final tree — all green: orientation
  11, the journey 12, the dashboard 27, the documents 27, the Dépôt 10, the drawer 18, the content pages 11, the service
  pages 5, `apps/portal` 8, `apps/pages` 28 (W/`tests_browser.log`, each file's output in W/`test_out/`). With them, again,
  the browser files the first run had covered: the area's own 48 (static and Chromium), `test_rtl_browser` 23,
  `test_rtl_browser_overlays` 5, `test_console_phone_browser_w3_a` 29, `test_console_shell_browser_w3_a` 35,
  `test_header_fits_the_narrowest_viewport` 5, `test_nav_sheet_w2_c2` 11, `test_browser_w2_c1` 12, `test_browser_w2_c2` 25,
  `test_browser_w3_f1` 12. No run crashed. The files m2's templates reach ran again after it (W/`tests_after_m2.log`).
- **The look** (W/`smoke.py`, F/`look/smoke/_*.png`): the implementer's smoke list on this base and the pass's own
  components — 24 × fr, ar × 1440 and 1366 under a mouse, 390 and 360 under a finger, every pair sheet looked at. At 1440
  and 1366 nothing moved but the names, now on their reading edge, and the notices' address box (+4 px); at 390 and 360
  the files' names, the parties, the skills, the «who» lines, the references and the company's head stand on the Arabic
  reading edge and an Arabic name on the French one, «Profil» on its edge, the ring inside the bar. (The 404 on a DEBUG
  lane is Django's debug page: not looked at, nothing of it changed here.)
- **The accessibility check's own runner** (copied with its probe and axe-core 4.13.0, on this pass's own profile —
  W/`run_a11y.py`, W/`pages_a11y.json`) on the 13 page states this pass touched × fr, ar, under a finger (390 full, 360 and
  320, 844 × 390) and under a mouse (1440 full, the 320 reflow): axe 0 violations, no overflow, no stop without a ring
  or invisible; under a finger every target 44 × 44 once `a161806` landed — the run's one finding, the loose files'
  «حذف» —, and one rounding: the dashboard's communication rows at 320 in Arabic are 44 px boxes at a fractional offset,
  43 by integer points; under a mouse every target under 24 px is the console bar's trail, spacing-excepted (W4-C's); a
  ring cut only at the console's desktop foot (W4-C's) and around a focusable scroll region taller than the screen
  (F/`a11y/`, F/`a11y-recheck/`).
- **Red on the previous sheet:** the pass's 26 new or changed tests run against an export of the branch's head
  (`694290a`): 26 failed, each for its measured reason (W/`red_on_head.txt`); all green on the final tree.
- **What still waits for `ile_v5_l6`** — the merge step's, once the database answers (restarting Docker is the
  orchestrator's): the accessibility check's scripts on the QA data (`mint.py`, `run_a11y.py coarse|fine` with
  `pages_check.json`, `run_perf.py w4a-lane` against `base-lane` with the branch point served from `base_b06ea1e/`) and a
  look at D7, D8, D16, D18, D22 and D23 on the QA records. On this base, D8, D16, D22 and D23 are held in Chromium by the
  area's tests and D7 and D18 were measured above (the documents pages' targets; the company's long name wraps in its
  head, no overflow). No script changed in this pass, and both shared bundles are lighter.

**m1, m2, m3.** m1 as the review asks (`c265620`): «Profil» 6 → 0 px from the line above at 390 and 360, fr and ar, 44 ×
44. m2 (`b2c761f`): the strings it names; the NowPanel's label of `companies/services.py` already passes `typo` where it
is drawn (`portal/partials/now_panel.html`, `now.title|typo`) — nothing to change there. **The other team-authored
`{% translate %}` lines beside « » : ; ? ! — 149 outside `templates/dev/` by
`grep -rn 'translate "[^"]*\( [:;!?»]\|« \)' templates --include=*.html | grep -v templates/dev/` — are recorded for
W4-D beside D14**: each passes through `{% translate "…" as x %}{{ x|typo }}` (the filter returns a prescribed string
untouched), family by family, measured at 360 and 375; the locked copy stays B1's. m3 is the merge step's (below).

**A11Y_PERF.md.** Finding 1 (`cb992c8`), 48 measures — the address on the contact page and its form, «Recueil des
besoins», the companies' door, the pending legal page and the Forum's registration × fr, ar × 320, 360 and 390 under a
finger and 1440 under a mouse: every one 28 px tall, 48 under a finger, no overflow (20 px in French and 23 in Arabic with
no band before; F/`spot-before/`, F/`spot-after/`). Finding 2 (`4727f8d`): Tab to the account button at 390 and 360, fr
and ar, in the person's and the company's spaces — its ring from −2 to 0 px → from 2 to 4 px, its foot 50 → 44 px in the
48 px bar. Finding 3, the Academy's filter row: there is no registers script to add a focus handler to — a script on a
page that draws none is W4-C's keyboard pass or W3-E's: handed on, unchanged. The two desktop items (the console's foot
scroll padding above phone widths, the trail links' 24 px under a mouse) are W4-C's, as the check says (W4-C is at its
merge step): not taken here.

**The payload** — rebuilt from a clean dist, gzip −9 per sheet, summed per page type (the implementer's
S/`weigh_ext.py`; F/`weigh_fix.txt`):

| page type | design-v5 (ceiling) | the branch's head | after the fixes |
|---|---|---|---|
| every page (`main.css`) — **shared** | 31 799 | 31 716 | **31 637** |
| console page types (+ console + portal) — **shared** | 39 978 | 39 887 | **39 798** |
| the company dashboard | 40 167 | 40 076 | 39 987 |
| «Mes pièces» · the documents' registers | 45 475 · 47 535 | 45 399 · 47 459 | 45 364 · 47 424 |
| a register page · «Mon parcours» with a file | 42 853 · 45 274 | 42 833 · 45 254 | 42 782 · 45 203 |
| a need's page · the help desk · the selection · the Academy | 43 042 · 43 115 · 43 316 · 43 045 | 43 022 · 43 095 · 43 296 · 43 025 | 42 971 · 43 044 · 43 245 · 42 974 |
| the case file · with its dialogs | 46 229 · 48 289 | 46 209 · 48 269 | 46 158 · 48 218 |
| the login · the home · an error page | 36 660 · 46 160 · 35 428 | 36 577 · 46 081 · 35 363 | 36 498 · 46 002 · 35 284 |
| the persons' door · the doors · the Forum · orientation | 35 384 · 35 226 · 34 820 · 35 913 | 35 381 · 35 187 · 34 817 · 35 894 | 35 302 · 35 108 · 34 738 · 35 815 |
| the project pages · a reading page · a service page | 34 065 · 35 900 · 34 225 | 34 017 · 35 850 · 34 142 | 33 938 · 35 750 · 34 063 |

Every page type is lighter than design-v5's ceiling and than the branch's head. The page-only sheets carry their
surfaces' rules (`documents.css` 5 512 → 5 566 B: the names' rule and the act's band; `registers.css` 2 946 → 2 984: the
head rule's names and the reference's cell); the shared bundles pay for the notices' rule and fall: `main.css` −79 B
(the dead legacy type classes `.text-h4` … `.text-secondary`, the note's marker `.note__marker` and `.icon--accent`
deleted — no template, view, script or module of design-v5, W4-C or W4-D names them, by grep), `console.css` −10 B
(the company head's box rule).

**The tests.** Static, one pytest at a time (W/`tests_static.log`): the two bundle-currency files 5 · 5,
`test_static_pipeline` 3, `test_dashboard_w3_b` 60, `test_depot_w3_c` 28, `test_documents_w3_c` 41, `test_case_file_w3_e`
22, `test_chips_cards_w1_c` 17, `test_components_w1_c` 30, `test_journey_w3_d` 41, `test_legacy_token_shim` 6 (and its
standing xfail), `test_icons` 20, `test_o14_lint` 53, `test_service_pages_w3_f2` 47, `test_layout` 29,
`tests/i18n/test_rtl_static` 81, `apps/selection/tests` 86, `apps/companies/tests` 99, `test_french_typography_w2_d` 13,
`test_design_docs` 40 (with the notes and the decision log as committed);
the browser files above. `manage.py check` clean; ruff clean on the test files touched.

**Left, by design or handed on.**

- `ile_v5_l6`'s items above (the merge step's); m2's remainder (W4-D, beside D14); m3 (the merge step); finding 3
  (W3-E / W4-C) and the two desktop items (W4-C).
- By design, recorded: a wrapped fact value keeps its own start (W3-E's facts rule — `dd[dir]` hugs its words on the
  reading edge; a long one, a person's message or a mandate's scope, reads from its own start as a person's prose
  does); a focusable scroll region taller than the screen cannot show its whole ring.
- W4-D holds `_legacy-tokens.css`, `components.css` and `register.css` whole (its deletion map): this pass deleted five
  dead type classes, the note's marker and `.icon--accent` there, to pay for finding 1 — should W4-D's part 2 delete
  the same rules or the sheets, its version stands.
- The scratch cluster (W/`pg/`), its databases and the minted sessions are this pass's alone: the sessions revoked, the
  cluster stopped. The lane server 8786 is stopped; no Chromium of this pass is left running.

**Paths for the merge step.** `check_ownership.py w4-a design-v5` on the final branch: 5 inside, 1 slice, 13 generated,
**37 delegated** — the implementer's 22 and this pass's 15: W3-C's `_table.css`; W1-C's `v5/notice.css`; W4-D's
`_legacy-tokens.css`, `components.css` and `register.css`; W3-B's `companies/dashboard.html` and its test
`test_dashboard_w3_b.py`; W3-E's `selection/partials/responsible.html` and `selection/process.html`; W2-C2's
`partials/main_nav.html` and its test `test_nav_sheet_w2_c2.py`; W3-F1's `pathways/_antifraud_callout.html`,
`pathways/training.html` and `orientation/result.html`; the steward's `docs/design/DESIGN_SYSTEM_2026.md` (§2's weight
of `v5/notice.css`, 4.2 → 4.9 KB, which `test_design_docs` holds to 10 %; the steward's
`scripts/regen_design_inventory.py` rewrites it at the merge) —, and **1 outside, `static/css/dev/showcase.css`** → FAIL until
the manifest names it (the review's m3): W4-A's justified slice («the two-column grids' column and the sample table's
scroll region, D13»), or the steward's.
