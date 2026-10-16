# W3-E · The case file and the secondary console pages — accessibility + performance check (one pass)

Label `w3-e-a11y-perf`, 16 October 2026 — the family's one accessibility/performance check (V5.5: implement → review
once → fix → ship). Built nothing, changed nothing in the family's code. Checked branch `v54-w3-e` at `dd0eba7` (steps
1–3 and their notes) against its merge base with design-v5, `fec37d3` (W3-D's shipped note). design-v5 has moved since
(`abed4c5`: the sec-f5, intfix and sec-f7 merges): no stylesheet changed there and no template of the area — the
dashboard's one condition (sec-f7) and, in JS, `overlay.js`, `overlay/extras.js` and `shell.js` (the overlay's late
settle, which the case file's dialogs inherit at the merge). The senior review was committed (`6699bc7`) while this
check ran; it adds only its report.

**Lane.** Lane 5, port 8785. Accessibility on the dev server from `C:/tmp/ile_wt/v54-w3-e` (`ile_v5_l5`,
`ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`, `--noreload`, no preview flag). Performance on the same port as a
**compressed twin** of the merge base (an export of `fec37d3` in this role's scratch folder) and of the head, served in
turn — the plan's 8782 shape: DEBUG off, `CompressedManifestStaticFilesStorage`, hashed URLs, gzip on the wire,
`collectstatic` into a scratch root per tree (W3-C's check's settings file, re-pointed at lane 5). Signed-in pages through
sessions minted with `Client.force_login` on `ile_v5_l5` (no password used, typed or stored), revoked at the end.
Headless Playwright Chromium (the venv's), its own profile under `C:/tmp/ile_v5_council/.profiles/w3-e-a11y-perf/`; one
browser and no pytest at a time; every series waited on `PERFORMANCE_BENCHMARK_LOCK` (never present; never created).
**No run crashed.** Never 8780, 8782, 9222 or 9223. **Nothing was submitted**: every dialog was left by Esc, «Annuler»
or «Fermer»; the only writes on the clone are the ten minted sessions (deleted at the end), the accounts' `last_login`
and one `auth.login` audit event each.

**Data.** The clone's own personas and step 1's «[w3e]» dates and communications for `qa-person` (left by the
implementer on purpose). The senior reviewer, on the same clone from 8885, seeded five lines of its own on
`EE167596D4` while this check ran: the professional's case file (C2) and `qa-doc-person`'s (C1) were measured with
them — five row menus and a line linked to a piece, which is how finding 2 surfaced.

Evidence: `C:/tmp/ile_v5_council/evidence/v54/w3-e/a11y-perf/` — `desk/`, `phone/` (keyboard walk with the ring read on
pixels, pixel contrast, hit areas, the accessibility tree, axe — one JSON + PNG per page), `reflow/`, `spacing/`,
`reduce/`, `forced/`, `interact/` (the row menu, the alert dialogs, the no-script path, the filters), `extra/` (the need's
head at six widths, the rings re-measured, the forced-colours ring crops, the trigger's box, the dialogs' contrast),
`rest.json`, `twin/` (the BASE / HEAD runs and traces, `summary_*.json`). Probes:
`C:/tmp/ile_v5_council/.work/w3-e/w3-e-a11y-perf/` (W3-D's and W3-C's probes adapted; W1-0's `trace.py`, `analyse.py`,
`health.js` byte-identical; axe-core 4.13.0, W1-0's copy).

## Verdict — SHIP_AFTER_FIXES

**0 blocking · 1 major · 5 minor** in W3-E's files, and no performance regression. The major is a WCAG 2.2 AA failure
on one page in one state: **a draft need's head scrolls sideways at 320, 360 and 375 px in French** (finding 1 — one
declaration in the family's page-only sheet, checked in the browser: the page then fits at every width). The one axe
violation is the row menu's «⋮», drawn 22 px wide (finding 2 — also one declaration, also checked). Otherwise **no WCAG
2.2 AA failure** on the area's 39 page states, fr and ar (1440, 390 touch, 320; reduced motion, forced colours, text
spacing): 3 528 keyboard stops named and `:focus-visible`, none hidden by a fixed layer; 6 622 text runs at AA or more
against the worst pixel, the state words at 7 : 1 or more (nullo's 5.38 by design); **the state changes on the overlay
system keep their contract** — the focus on «Annuler», the trap, Esc and the scrim, the focus back on «⋮», the
consequence and the rule tied to their controls, the no-script path. **Performance:** the shared CSS falls by 4 056 B on
every console page (main.css −3 577 B on every page); every page type of the area is lighter but the case file (+1 422 B
through three page-only sheets, allowed by V5.8 with the twin check) and the closed module's 503 (+52 B); on the
compressed twin (W1-0's protocol, n = 9, interleaved) LCP stays within −68 … +28 ms of the merge base, the first-render
task is lower or equal in every n = 9 cell, CLS ≤ 0.0005 (one load of 0.029 at n = 5), the row menu and the line's
dialog open cold in p90 96 and 152 ms on the heaviest page, nothing loops at rest; «Mon parcours» is 244–372 ms earlier
than V4. The minors: under forced colours a row link's ring loses its bottom edge; two landmarks share a name on the
Academy plan; one link is 22 px tall on a phone; the case file links seven stylesheets.

## What was measured

39 page states × fr / ar — every page type the family redrew, with the clone's own data:

| Keys | Account | Pages |
|---|---|---|
| P1–P8 | `qa-person`, `qa-fresh-person` | «Mes échéances» (six dates: late, near, far, done, cancelled), «Communications» (five, two unread), «la lettera» (an unread one: a GET reads only), «Mes demandes», a request, «Mon parcours» (results + W3-D's journey), «Ma situation» (the phone's action bar, the one total), the empty state |
| H1–H6 | `qa-person`, `demo-professionnel`, `demo-operateur` | the guichet, a request and its exchange, opening a request, the professional's queue, the professional's request (the internal note), the dispatch desk (staff chrome) |
| A1–A5 | `qa-person` | the catalogue (the domains as the filter), a course, «Mes formations», a follow-up, the plan |
| K1–K7 | `qa-company`, `seed-company`, `qa-admin` | «Mes besoins» (the filter, E-3), a need taken in charge, the need form, «Mon entreprise», the declaration, the territorial analysis (staff chrome), a draft need (the pending notice, the two head acts) |
| L1–L4 | `seed-actor`, `seed-person` | the selection workspace, the process (the actor's acts), the person's panel, the identity communicated |
| G0 | `qa-person` | the Forum permanent shut (G11): the module's 503 in the error pages' grammar |
| C1–C8 | `qa-doc-person`, `demo-professionnel`, `qa-person`, `seed-person`, `qa-fresh-person` | the case file `EE167596D4` (the person; the assigned professional — the file's state dialog and, with the reviewer's lines, five row menus), `E46E03B461` (five lines, three row menus and their alert dialogs, six pieces), `0FEEBAE3A9` (SELECTION), «Mes dossiers» (the person's, entrusted, empty), the pre-assessment |

Passes: 1440 × 900 (fine pointer) and 390 × 844 (phone emulation, touch) — keyboard walk with the ring read on pixels,
pixel contrast, hit areas, Chromium's accessibility tree, axe on `wcag2a/2aa/21a/21aa/22aa` and `best-practice`, W1-0's
`health.js` (78 + 78 loads); 320 × 640 (400 % reflow, 78); WCAG 1.4.12 text spacing at 1440 and 390 (15 states, 60);
reduced motion (`emulateMedia`) and forced colours (Chromium's emulation) at 1440 and 390 (8 states each, 32 + 32); the
state changes from the keyboard and the pointer — the row menu, the line's and the file's alert dialogs, the trap, Esc,
the scrim, the focus back, the no-script path — at 1440 and 390, fr and ar, normal, forced colours and reduced motion
(14 runs, 7 of them run again after a probe fix); the two filters; the open overlays' contrast (5); a 5-second window at
rest on 11 pages at 1440 and 390, with a dialog open and after it closed (22); the re-measures and the fixes tried
through the CSSOM (`extra/`, 32). **About 440 recorded loads: 0 CSP reports, 0 console errors** — the 503 page's own
status line apart, as W1-0 counts the 410 page's.

How the probes read pixels (W3-B's, unchanged; W3-D's and W3-C's checks): the keyboard walk clips every stop focused,
then the same clip at the same scroll with nothing focused — the indicator is the pixels that changed (ring fill =
changed pixels in a 6 px band round the box ÷ a 2 px perimeter; change contrast = the median ratio between each changed
pixel's two colours). Contrast: every text run of `<main>` fully in view and under no fixed layer, its computed colour
with its opacity chain against the pixels under it, the page re-drawn with every glyph transparent: the dominant pixel,
and the worst pixel covering ≥ 5 % of the run. Hit areas: `elementFromPoint` probed outward from each target's centre (a
stretched link's `::after` and a button's `::before` count — they take the press).

## Accessibility

| Check | Result |
|---|---|
| axe 2.0–2.2 A/AA | **0 violations at 1440** on the 78 loads. **At 390, `target-size` on one control**: the row menu «⋮» of a line that is also the way to its piece (C2, `#line-17-actions`, fr and ar — finding 2). best-practice: `landmark-unique` on the Academy plan (A5, fr and ar — finding 4). «Incomplete» in the area's markup: only `aria-controls` from the file's «Nouvel état» to its closed dialog (as the shell's «Menu» to its closed drawer) and contrast cases axe cannot resolve, read on pixels below |
| Keyboard, fr and ar | **2 200 stops at 1440 and 1 328 at 390, every one named and `:focus-visible`.** The case file's order is its five questions (journey · next action · what is asked, each line's «⋮» after its words · pieces · who · the file's state · what changed). The probe's 22 «nameless» stops are textareas named by their `<label>` (its name lookup stopped at `input`): Chromium's tree has 0 nameless controls on every page |
| The state changes (C-5, C-6) | The «⋮» is reached by Tab (24 presses at 1440, 7 at 390), named «Actions» and described by its line. Enter opens W2-A's menu with the focus on «Nouvel état de cette ligne»; Enter opens the line's **alert dialog** — `role=alertdialog`, `aria-modal=true`, named by its title, described by the line, its chip and the consequence — with the focus on **«Annuler»**. Tab and Shift+Tab stay inside (Annuler → Mettre à jour → Fermer → the radio group, one stop; the arrows choose). **Esc closes it and the focus is back on the row's «⋮»**, its ring visible; a press on the scrim leaves it open; «Annuler» closes it with the same return. The file's dialog: «Nouvel état» reached by Tab, the same grammar, the closure's consequence tied to its radio («Un dossier clôturé ne se rouvre pas : on en ouvre un nouveau.»), «Motif» described by its rule («La suspension exige une motivation.»), Esc back on «Nouvel état». Without script the menu still opens (the native popover) and its item shows the dialog in place (`:target`); «Fermer» leads back to the row. Fr and ar, 1440 and 390, normal, forced colours and reduced motion: 0 console errors, 0 duplicate ids |
| Focus visible | The area's controls carry the laguna-550 ring at **3.94 : 1 change contrast** (filter links, row links, buttons; the dialog's «Annuler» 4.11, its radios 3.19); never under 3.70 on any page (the 503 page's links and its act, on the error pages' ground); 15.13 under forced colours. Five weak readings at 1440 and eight at 390 were stops cut by the viewport's edge (a row link and a button at its bottom, tall scroll regions): measured again at the viewport's centre, fill 1.01–1.07. Under forced colours a stretched row link keeps its ring on three sides only (finding 3) |
| Focus not obscured (2.4.11) | 0 stops hidden by a sticky or fixed layer at 1440 or 390; one partly covered (a tall textarea of the need form, 7 of 21 points under the phone's bottom bar) — allowed at AA |
| Names, roles, structure | One h1 on every page. The case file: h1, an h2 per question, h3 for «Exigences» and «Pièces du dossier», a region per section and `complementary «Suivi du dossier»`. The filters are `navigation «Filtrer par état»` / «Filtrer par domaine», `aria-current` on the chosen group (moved there after Enter; an empty group is a word, not a link). «Communications»' count is the page's one `role=status`. The menu is a `group` named by its line. Data carry their own language where it is known (`lang` on a line's and a course's words); free text is `dir="auto"` |
| Contrast on pixels | **3 370 text runs at 1440 and 3 252 at 390, 0 below AA against the dominant pixel and 0 against the worst pixel.** **State words: 222, all ≥ 7 : 1** (COLOUR §10's AAA rule) but nullo's ten («Annulée», «Non applicable»: 5.38 : 1, its own definition — W1-C). The clause (`.reg-note`, text-2, 13–14 px) 6.87; text under 16 px between 4.5 and 7 : 1 is W1-A's tokens as designed (text-2 6.87, text-3 5.88, laguna-700 links 5.93–6.05) — none is a state word or a notice title. The open overlays: 47 text runs in the open menu, the line's dialog (fr 1440, ar 390) and the file's (fr 1440, ar 390): 0 below AA; the chips at 7 : 1 or more but nullo's 5.38; the primaries' white label 5.29 (W1-A's token, 15 px) |
| Targets (2.5.8; 44 on touch) | At 1440, 0 targets under 24 px without the spacing exception (209 with it: the shell's 20 px breadcrumb links, the «⋮», one facts link). At 390 the area's controls are 44 px — the filter links, «Marquer comme lue», the acts, the phone's action bars (310 × 44) — and a row link takes its whole row (358 × 84–103). Two exceptions: **the «⋮» is 22 px wide at both sizes** (its `::before` takes the press over 44–46 px; finding 2) and «Voir le programme complet» (a follow-up's facts) is 22 px tall on a phone (finding 5) |
| Arabic | The rows, the filters, the dialogs and the bottom sheet mirrored; references, dates and figures not mirrored; French data stay left-to-right inside Arabic rows; **no Arabic text under 14 px** |
| Reduced motion — a real still | 0 animations at load, at + 1 s and at the end, on every page (32 loads). The overlays under `reduce`: **opacity only, 80 ms** (W2-A's `--motion-reduced`), `transform`, `translate` and `scale` none at + 400 ms — the menu, the dialog, the scrim. With motion allowed nothing moves at load either (0 running animations at + 0.7 s on 22 pages): the HealthStrip's `strip-fill` that W3-D caught on the case file left with it |
| Forced colours | System colours only: the chips keep their edge (dashed attesa, solid otherwise) and their marks, the filter's indicator is Highlight, the hairlines stay, the dialog has its edge, its double focus ring and its scrim. Usable at 1440 and 390 (`forced/`, `interact/line-fr-1440-forced-dialog.png`). The current rail / bar entry shows no focus change: W3-A's (W3-D's O2, still open — «Seen on the way») |
| 400 % reflow (320 × 640) | **0 horizontal overflow on 77 of 78 loads; the draft need in French overflows by 61 px — at 360 and 375 too** (finding 1). No clipped text but the shell's console-bar title ellipsis. The probe's 118 «overlaps» are the line boxes of French data inside Arabic rows (bidi): looked at on two pages, no glyph touches another |
| Text spacing (1.4.12) | 60 loads: no text clipped; no overflow but the draft need at 390 in French (its head acts again, and the company's five-entry bottom bar — W3-A's) |

## Performance

**CSS and JS — the committed bundles**, gzip −9 / mtime 0 (the stewards' way), the merge base against the branch:

| Bundle | `fec37d3` | `v54-w3-e` | Δ |
|---|---:|---:|---:|
| `dist/main.css` (every page) | 35 483 | **31 906** | **−3 577** |
| `dist/portal/console.css` | 6 778 | 7 189 | +411 (`v5/_frame.css`, out of main.css) |
| `dist/portal/portal.css` | 1 935 | 1 045 | −890 |
| **SHARED — main + console + portal (every console page)** | **44 196** | **40 140** | **−4 056** |
| `portal/registers.css` (new page-only sheet: the registers' grammar, ≈ 40 page types) | — | 2 593 | +2 593 |
| `portal/case.css` (new page-only sheet: the case file) | — | 814 | +814 |
| module sheets: `helpdesk` · `academy` · `selection` · `companies` | 875 · 618 · 1 085 · 873 | 262 · 192 · 463 · 189 | −2 345 |
| `portal/situation.css` | 2 202 | 2 206 | +4 |
| JS | — | — | `console.js` +41 B raw (−7 B gzip: §2f in, §2c out); every chunk renamed, raw sizes identical |

design-v5's shared ceilings (its head `abed4c5` adds no stylesheet): main.css 35 483, the console page types 44 196 —
**both fall**.

**Each page type with the sheets it links** (read from the served HTML of each tree on the twin, gzip −9):

| Page type | `fec37d3` | `v54-w3-e` | Δ | CSS requests |
|---|---:|---:|---:|---|
| the person's registers, «Mes dossiers», the pre-assessment, the empty states (P1–P5, P8, C5–C8) | 44 196 | 42 733 | −1 463 | 3 → 4 |
| «Mon parcours» (P6) | 46 617 | 45 154 | −1 463 | 4 → 5 |
| «Ma situation» (P7) | 46 398 | 42 346 | −4 052 | 4 → 4 |
| the help desk (H1–H6) | 45 071 | 42 995 | −2 076 | 4 → 5 |
| the Academy (A1–A5) | 44 814 | 42 925 | −1 889 | 4 → 5 |
| the company's pages (K1, K3–K6) · a need (K2, K7) | 45 069 | 42 733 · 42 922 | −2 336 · −2 147 | 4 → 4 · 4 → 5 |
| the selection (L1–L4) | 45 281 | 43 196 | −2 085 | 4 → 5 |
| the Forum permanent shut (G0: the error pages' sheet) | 35 483 | 35 535 | +52 | 1 → 2 |
| **the case file (C1–C4)** — with its dialogs, as drawn for every reader measured | 46 617 | **48 039** | **+1 422** | **4 → 7** |

Every page type of the area is lighter but two: the 503 page (+52 B: it now links the error pages' own sheet, shared by
every error page) and **the case file, +1 422 B through three page-only sheets** (registers 2 593, case 814 and W2-A's
panels 2 071 — CONTRACT §1 wherever a dialog is drawn, which is for every reader who may move a line or the file). V5.8
allows that growth through page-only sheets after deletion, with a twin check: below. JS is unchanged (45 972 B gzip on
every console page, nine requests).

**Requests before `load`** (Resource Timing on the twin): the registers' pages 3 + 9 → 4 + 9, the modules 4 + 9 → 5 + 9,
«Mon parcours» 4 + 9 → 5 + 9 (and one more font file: ILE Mono for the records' references, 2.7 KB), **the case file
4 + 9 → 7 + 9**. W1-0's before set counted 3 + 8 on the console page types and the case file, 4 + 8 on the modules: the
ninth script is earlier families'; W3-E's own share is one stylesheet on the redrawn pages and three on the case file
(finding 6).

**Cold loads before / after** — W1-0's `trace.py` protocol on the compressed twin: profile A (150 ms RTT, 1.6 / 0.75
Mbps), CPU × 4, cache disabled, a fresh profile per load, interleaved blocks BASE 5 · HEAD 5 · HEAD 4 · BASE 4 (n = 9 a
cell and tree; one discarded warm-up per cell after every server start), medians; «blocks» = HEAD − BASE inside each
block. Tolerance (§2.6): ≤ +50 ms LCP, ≤ +30 ms first-render task.

| Cell (n = 9 / 9) | LCP ms (blocks) | FCP | first-render task | longest load task | CLS max | LCP element | elements |
|---|---|---|---|---|---|---|---|
| the case file, five lines (`E46E03B461`) — fr 1440 | 1 312 → 1 340 (+4, +122) | 944 → 1 028 | 47 → 34 | 130 → 107 | 0.0005 → 0 | `p.panel__text` → `p.db-assessment__text` | 760 → 1 199 |
| the same — ar 1440 | 1 616 → 1 580 (+36, −192) | 1 184 → 1 172 | 48 → 38 | 187 → 151 | 0 → 0 | `p.panel__text` → `p.db-assessment__text` | 759 → 1 198 |
| the same — fr 412 | 1 212 → 1 204 (−24, +60) | 1 008 → 1 012 | 30 → 29 | 160 → 132 | 0 → 0 | `span` → `p.db-now__text` | 760 → 1 199 |
| the same — ar 412 | 1 468 → 1 400 (−16, −88) | 1 172 → 1 160 | 38 → 37 | 217 → 170 | 0 → 0 | `h1.ctx__title` → `p.db-now__text` | 759 → 1 198 |
| «Mon parcours» (W1-0's flagship «journey-results») — fr 1440 | 1 180 → 1 164 (−36, −12) | 972 → 1 008 | 44 → 38 | 79 → 91 | 0 → 0.0005 | `p` both | 565 both |
| the same — ar 1440 | 1 400 → 1 428 (−28, +70) | 1 148 → 1 188 | 51 → 41 | 122 → 131 | 0.001 → 0 | `p` both | 565 both |
| the same — fr 412 | 1 148 → 1 156 (−4, +22) | 988 → 1 000 | 30 → 29 | 80 → 106 | 0 → 0 | `p` both | 565 both |
| the same — ar 412 | 1 384 → 1 412 (+20, +124) | 1 172 → 1 156 | 38 → 38 | 119 → 136 | 0 → 0 | `p` both | 565 both |

Read as the plan asks (medians, n = 9, the tolerance): **no LCP regression** — −68 … +28 ms, every cell inside +50,
block signs mixed in four of eight; **the first-render task lower or equal everywhere** (0 … −13 ms); CLS ≤ 0.0005;
the requests and bytes as above. The case file's DOM grows by 58 % (the rows' menus and the dialogs laid out in
advance: W2-A's INP rule) and its longest load task still falls (layout 90 → 66 ms at fr 1440, 157 → 87 at ar 412).
The LCP element moves from V4's panel text to the outcome's text in the side column (1440) and the NowPanel's text
(412) — no later. «Mon parcours» keeps its DOM and its LCP element; its longest load task grows by 9–26 ms at × 4 (≈ 2–6
ms at × 1: the records' layout, and a late re-layout when the ILE Mono face of the references arrives) — an observation,
not a regression to fix. Against W1-0's before set (V4 on 8782, the same protocol): «Mon parcours» LCP 1 508 · 1 688 ·
1 528 · 1 656 → 1 164 · 1 428 · 1 156 · 1 412 ms (244–372 ms earlier), W1-0's first-render task 327–436 → 29–41 ms.

The other page types the family redrew, n = 5 / 5 (blocks BASE 3 · HEAD 3 · HEAD 2 · BASE 2), and the four cells whose
LCP median moved past +50 ms there measured again at n = 9:

| Cell | LCP ms (blocks) | FCP | first-render task | longest load task | CLS max | requests (CSS + JS) |
|---|---|---|---|---|---|---|
| the case file `EE167596D4` (no line by then) — fr 1440 | 1 220 → 1 272 (+152, 0) | 964 → 1 028 | 47 → 34 | 105 → 137 | 0 → 0 | 4 + 9 → 7 + 9 |
| the same — ar 412 | 1 448 → 1 452 (+40, −62) | 1 180 → 1 188 | 35 → 28 | 184 → 205 | 0 → 0.0287 ¹ | 4 + 9 → 7 + 9 |
| «Mes échéances» — fr 1440 | 1 072 → 1 064 (−8, +2) | 932 → 968 | 51 → 44 | 54 → 90 | 0 → 0 | 3 + 9 → 4 + 9 |
| the same — fr 412 | 1 096 → 1 152 (+56, +84) | 992 → 976 | 32 → 31 | 73 → 105 | 0 → 0 | 3 + 9 → 4 + 9 |
| a guichet request — fr 1440 | 1 144 → 1 236 (+92, +16) | 976 → 1 032 | 37 → 35 | 128 → 123 | 0 → 0 | 4 + 9 → 5 + 9 |
| the same — ar 412 | 1 360 → 1 440 (+100, −70) | 1 172 → 1 212 | 36 → 36 | 176 → 176 | 0 → 0 | 4 + 9 → 5 + 9 |
| the Academy catalogue — fr 1440 | 1 168 → 1 236 (+108, +40) | 948 → 1 052 | 41 → 35 | 90 → 108 | 0 → 0 | 4 + 9 → 5 + 9 |
| the same — ar 412 | 1 464 → 1 392 (−56, −166) | 1 176 → 1 216 | 36 → 38 | 228 → 144 | 0 → 0 | 4 + 9 → 5 + 9 |
| «Mes besoins» — fr 1440 | 1 168 → 1 120 (+32, −108) | 944 → 996 | 41 → 36 | 118 → 118 | 0 → 0.0001 | 4 + 9 → 4 + 9 |
| the same — ar 412 | 1 324 → 1 356 (+144, −82) | 1 156 → 1 156 | 34 → 39 | 156 → 192 | 0 → 0 | 4 + 9 → 4 + 9 |
| a selection process — fr 1440 | 1 312 → 1 356 (+324, −64) | 1 032 → 1 020 | 38 → 34 | 148 → 193 | 0.0005 → 0 | 4 + 9 → 5 + 9 |
| a guichet request — fr 1440, **again at n = 9** | 1 164 → 1 152 (+36, +2) | 948 → 952 | 48 → 45 | 97 → 102 | 0.0005 → 0 | 4 + 9 → 5 + 9 |
| the Academy catalogue — fr 1440, **again at n = 9** | 1 152 → 1 116 (−60, −44) | 944 → 956 | 45 → 44 | 84 → 66 | 0 → 0 | 4 + 9 → 5 + 9 |
| «Mes échéances» — fr 412, **again at n = 9** | 1 068 → 1 088 (+8, +28) | 980 → 980 | 29 → 27 | 62 → 66 | 0 → 0 | 3 + 9 → 4 + 9 |
| the case file `EE167596D4` — fr 1440, **again at n = 9** | 1 220 → 1 196 (−12, −22) | 964 → 988 | 43 → 30 | 93 → 110 | 0 → 0 | 4 + 9 → 7 + 9 |

¹ One load of five (a slow one, LCP 1 624 ms); 0 in the four others — under the 0.05 of a flagship.

At n = 5 four cells crossed +50 ms with block signs that disagree or a machine that moved (other lanes share it: the
selection's blocks are +324 and −64); measured again at n = 9 the same four sit at −36 … +20 ms. No meaningful LCP or
first-render regression on any redrawn page type; the first-render task is lower in 12 of the 15 rows, equal in one,
+2 and +5 ms in two (inside its 30 ms). FCP at 1440 in French lands 4–84 ms later in the five n = 9 cells (median +24:
one stylesheet more on HTTP/1.1 — in the traces read, the extra sheet arrives before main.css, so the cost is the
shared 1.6 Mbps pipe, not a queue) — inside the LCP tolerance, and smaller under HTTP/2.

**The state changes, cold** (HEAD, the same protocol, n = 9, the heaviest page of the area — the case file with five
lines, 1 199 elements; the row menu pressed after it is scrolled into view, then its item): **the row menu opens in
56–112 ms (median 96 fr 1440 · 72 ar 412; p90 96 · 80) and the line's alert dialog in 72–160 ms (median 104 · 88; p90
152 · 112)** — under §1.14's 200 ms for an overlay's cold open; the interactions' longest tasks 56–81 ms at × 4.

**At rest — nothing loops.** 5 s windows on 11 pages at 1440 and 390 (22), and with a line's dialog open and after Esc
on the case file: 0 style recalculations, 0 layouts, 0 `requestAnimationFrame` or timer calls, 0 running animations;
task time ≤ 17 ms in 5 s (`rest.json`).

## Findings

1. **Major — the draft need's head scrolls sideways on a phone: WCAG 1.4.10 at 320 px, and at 360 and 375.** On
   «Soudure d'assemblage sur charpente métallique» (`qa-company`, `BD1F1C30DB`, a draft: «Modifier le besoin» and
   «Transmettre au projet»), French, the document is 381 px wide at 320, 360 and 375 (`extra/extra.json` → `head_widths`;
   `reflow/K7-fr-320.png`, `extra/K7-head-fr-320.png`): the acts' group `div.ws-head__action.reg-acts` keeps its
   max-content width, 365 px — the two buttons side by side — because `.ws-head__action { flex: none }`
   (`v5/_frame.css`, moved with its values from V4's sheet) holds it in the head's wrapping row while its children take
   100 % each below 48rem (`v5/_registers.css` §8: `.reg-acts > * { flex: 1 1 100%; inline-size: 100% }`). Arabic fits
   (304 px); at 390 and up French fits by 9 px. The plan's phone set (360 × 800, 375 × 667) is where it shows. The
   template is this family's (`companies/need_detail.html`, the head of step 2); the merge base had no such head. *Fix*
   (the registers' page-only sheet, no shared byte): in `_registers.css` §8, `.reg-head .ws-head__action { flex: 1 1
   100%; min-inline-size: 0; }` — the group takes the head's line and its buttons stack in it. Adopted through the CSSOM
   on the lane, it holds: the document is 320 · 360 · 375 · 390 px wide at those widths, fr and ar, each button the
   line's width (`extra/fix_check.json`, `extra/fix1-K7-fr-320.png`). Re-measure with text spacing after the commit.
2. **Minor (it is the one axe violation) — the row menu's «⋮» is 22 px wide.** `v5/_case.css` sets `.db-task__end
   .file-row__menu { inline-size: auto }` to keep the phone's row act from stretching it; `auto` collapses `.btn--icon`'s
   box to its glyph: 22 × 40 at 1440, 22 × 44 at 390, where the system's icon control is 40 × 40 / 44 × 44
   (`extra/extra.json` → `trigger`). Its `::before` still takes the press over 44–46 px, so WCAG 2.5.8 holds on pixels,
   but axe's `target-size` reads the 22 px box and fires where the row is also the way to its piece (a stretched link
   round it: C2, `#line-17-actions`, fr and ar at 390), and the visible control is a thin bracket against the words
   (`interact/line-fr-1440-forced-dialog.png`, `forced/C3-ar-390.png`). *Fix:* `inline-size: var(--btn-h-icon)` in place
   of `auto` — the same escape from the phone's 100 %, at the system's size. Adopted through the CSSOM it gives 40 × 40
   at 1440 and 44 × 44 at 390, at the row's inline end, no overflow (`extra/fix2-trigger-390.png`); it also answers the
   review's minor 2 (the trigger floating with the words) if the row's last column is sized to it.
3. **Minor — under forced colours a stretched row link's ring loses its bottom edge.** The next line of the row (its
   meta: the reference, the territory…) is painted over the outline's bottom edge at its 3 px offset — Chromium draws a
   Canvas backplate behind text in forced colours: 59 % of the ring's perimeter drawn on the needs register, 72–95 % on
   «Communications», 103 % with colours (`extra/K1-forced-compare.png`, `extra/forced_offset.json`). Three sides stay at
   15.13 : 1, so 2.4.7 holds. *Fix:* a gap under a row's title, in forced colours only — `@media (forced-colors:
   active) { .reg-row .db-task__title { margin-block-end: 6px } }` in `_registers.css`. Measured through the CSSOM
   (`extra/forced_offset.json`): with the meta line 6 px lower the whole ring returns (fill 1.03); `outline-offset: 1px`
   alone does not (0.58).
4. **Minor (best-practice; carried from the merge base) — two region landmarks with one name on the Academy plan.** The
   gap table's section and its scroll region are both labelled by the same `h2` (`plan-gap-title`): axe
   `landmark-unique`, A5 fr and ar at both sizes. *Fix:* label the scroll region by the table's caption, as the area's
   other scroll regions do (`aria-labelledby="t-…"`).
5. **Minor — «Voir le programme complet» is 22 px tall on a phone** (a follow-up's facts, `academy/enrolment_detail.html`):
   under the plan's 44 px for a finger (WCAG holds by spacing). *Fix:* the console link's block size on a coarse pointer
   (`min-block-size: var(--hit-primary)`), or the `db-link` the page's other links use.
6. **Minor (budget, not a measured regression) — the case file links seven stylesheets.** Main, portal, console, W2-A's
   panels, the registers, the case's and the journey's: 7 + 9 requests before `load` against 4 + 9 at the merge base and
   W1-0's 3 + 8 for the case-file page type (§2.6: «≤ the before set's count»); W3-E's share is three. The twin shows no
   LCP and no first-render regression (above), so V5.8's sanity check passes and the bytes are allowed. *Fix:* none
   needed to ship; record the count in DL54 with the page type's first own sheets, or let the case file link one sheet
   that imports the registers' and the case's partials (one request less, 2.6 KB not reused from the cache).

The senior review (`REVIEW.md`, committed as `6699bc7` while this check ran) was read after the measures. Its four
majors are design and UX (the case file's first screen, the next line drawn twice, the history's «Vous», the three
closures without the alert dialog); none is an accessibility failure on the checks above, and this check repeats none
of them. Its minor 2 (the phone's «⋮» floats with the words) and finding 2 here are the same control: both are fixed
by giving it the system's width in a column of its own. Finding 1 is not in the review (its 0-overflow sweep did not
draw a draft need at 320–375).

## Seen on the way — outside this area (for the orchestrator; not counted in the verdict)

- **O1 · W3-A's shell — under forced colours the current page's entry still shows no focus** (W3-D's O2, open): 22 of
  the 32 forced-colours walks, the current rail entry at 1440 and the current bar entry at 390, fr and ar — its
  forced-colours outline is the focus outline.
- **O2 · W3-A's bottom bar for a company account overflows under text spacing**: «Tableau de bord · Mes besoins · Mon
  entreprise · Communications · Menu» runs 69 px past 390 with WCAG 1.4.12's spacing (the person's four entries fit).
- **O3 · the public footer on the 503 page** (W3-F2's error grammar): its links are 24–25 px tall on a phone, under
  the plan's 44 px for a finger (WCAG holds by spacing).
- **O4 · two QA lanes on one clone.** The senior review seeded and later removed five lines of its own on `EE167596D4`
  while this check measured it: the desk and phone passes drew C1 and C2 with them (which is how finding 2 surfaced),
  the performance series without them (`EE167596D4` had no line by then; the core series uses `E46E03B461`, untouched
  by either role). A shared lane clone wants one writer at a time.

## Not checked

WebKit and Firefox; a screen reader (the tree read is Chromium's); a real phone; the HTTP/2 shape of production (the
twin is HTTP/1.1, where the case file's extra stylesheets cost the most). **Nothing was submitted**: the POST round trip
(the return to `#line-<pk>`, the status region's sentence, a refused move) is the review's (`p/`) and the
implementer's, not re-run here. The Forum permanent's open pages (G11 keeps the module shut; its 503 was checked) and
the bridge's institution and university accounts: both need lane-only seeds, not written on a clone the reviewer was
using. The reserved area's own 503 (it needs the clone's flag switched off). it / en.

## The lane, cleaned

The ten minted sessions revoked on `ile_v5_l5` (`sessions.py revoke`: 10 rows deleted, the cookie file removed); the
server on 8785 stopped; no browser of this role left running, its profiles deleted; the twin's two static roots and the
merge base's export deleted from the scratch folder; the benchmark lock never created; nothing else written on the clone
(no line, state, message or date). Scratch and evidence outside every repository; this report is the only file this
role wrote in the worktree.
