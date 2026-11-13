# W2-C1 · «Il portico» — the senior review (design + UX + taste, one pass)

Reviewer label `w2-c1-review`, V5.5 delivery mode (implement → review once → fix → ship). Reviewed: branch `v54-w2-c1`
at `dc29569` (clean worktree), on the reviewer's own server `127.0.0.1:8889` run from `C:/tmp/ile_wt/v54-w2-c1` on
`ile_v5_l9` (`ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`, `--noreload`), headless Chromium with the profile
`C:/tmp/ile_v5_council/.profiles/w2-c1-review/`, a signed-in session minted with `Client.force_login` (no password).
Pages: `/fr/`, `/ar/`, `/fr/faq/`, `/ar/faq/` at 1920 · 1440 · 1366 · 1280 · 1279 · 1024 · 390 · 360, closed, every
door by hover, pinned, the keyboard model key by key, scrolled, the current door, the text-spacing override (WCAG 1.4.12),
reduced motion, forced colours, signed in. Nothing was built by this reviewer. Evidence (captures, `measures.json`,
`console.json`, the N18 sheets) under `C:/tmp/ile_v5_council/evidence/v54/w2-c1/review/` (E/ below); the scripts under
`C:/tmp/ile_v5_council/.work/w2-c1/w2-c1-review/`. The builder's notes read first: `NOTES.md` beside this file.

## Verdict — SHIP_AFTER_FIXES

No P0. The pages work, the direction is the owner's, nothing is unusable, no data or security problem. Four majors, all
cheap, must go before the merge: the French letterhead does not hold its column from 1280 to ~1510 px; the bar overflows
the page under text spacing; three of the four door panels are three-quarters empty and every panel splits its lede in
two; the brand name disappears at 360 px. Then four minors.

## The judgement against the bar

**It is the owner's direction.** Fase 3's anatomy and order are all there and nothing else was tried: the night
institutional bar with the four autonyms, the paper letterhead with four doors · hairline · Forum · Projet, the portico
panel on 8 | 4 with the gloss first, the entries on hairline rows, the photograph in the last four columns, the
anti-fraud foot, the scrim for click and keyboard only. N-A gave only its mechanics (intent timing, the keyboard model,
one indicator), exactly as plan §1.12 says.

**Richer than Fase 3 — yes, as a system; not yet in three of the four doors.** The N18 sheet (E/n18/n18-1440.png,
n18-1920.png; the table below) shows the comp beside the build with Personnes open. The build adds four opened doors
where the comp had one, a colour photograph per door in the one V5 grade (the four frames are good: specific, people
from behind, never the stock smile), the architrave, the audience disc on a night plate, second lines shown whole where
the comp clamped them to two lines with an ellipsis, the plate in the letterhead instead of a link that left at the
first scroll, a panel hung from the content column instead of the viewport, and a complete keyboard model. The Personnes
panel is more premium than the comp's: one column that breathes, the photograph bleeding to the panel's edge, no
glyph noise. But the comp's single panel was denser than three of the build's four: Entreprises, Institutions and
Universités open a 1240 × 570 sheet (1360 × 550 at 1920) with two rows in it, and in every panel the lede column puts
the gloss in the top corner and «Voir l'espace» in the bottom corner, 340–460 px apart — the comp kept them together.
That is the one place where the build reads below the comp, and it is a composition fix, not a content fix (major 3).

**Premium, dynamic, sophisticated, coherent.** The bar at rest is credible beside the references: 15/20 500 in
text-2, ink when open, the plate flat with the gold key as ornament, the 2 px architrave in laguna on the seam. The
panel is a transition (200 ms in, 120 out, instant from the keyboard), the entries rise once per page, the photographs
cross-fade under `contain: paint`, the indicator travels on the snappy spring and never on first placement — the
motion grammar of §1.5 is respected (the reduced-motion state is right in `chrome.css` §9 and still flattened by
`components.css` §29, W1-D's deletion). The panel is the door card opened: same photographs, same disc, same gloss —
hero, cards and navigation are one system. Typography is Host throughout (the serif gloss of the comp is gone, as §1.1
decided). The Arabic page mirrors correctly: the architrave under the open door from the right, the entries at the
first door's inline start, the plain panel at the inline end, ← → following the eye. Taste: nothing template-like,
nothing «AI»; the only default-looking pieces are the faint door chevrons and the V4 drawer below 80rem, which W2-C2
replaces.

**UX.** Hover intent 120 / 80 / 250 ms, a click pins, the scrim only then and never over the institutional bar, the safe
triangle holds the panel along the travel to doors 2–4 (272 px fr, 206 px ar in my run), Esc closes and returns the
focus, focus leaving the navigation closes, Home / End move the open panel like the arrows, the current door and the
current entry are marked on an interior page, 2.4.11 is held by the scroll padding. The 1024–1279 band and the phone
drawer work. Ten of ten per-family browser tests passed on the lane (below).

## Findings

### Blocking — none

### Major — fix before the merge

**M1 · The French letterhead overflows its content column by 80–83 px from 1280 to ~1510 px.**
`site-header__inner` is a non-wrapping flex row; in French the lock-up (303.5) + gap (24) + the six items (829 at
≥ 90rem, 795 at 80–90rem) + gap (24) + the plate (139.8 labelled, 32 as the key) do not fit the column:
1320 > 1240 at 1440, 1178.5 > 1096 at 1366 and 1280. The row overflows at the inline end, so the plate — and the
last item — sit outside the grid every other element respects: at 1440 the plate's right edge is at 1420 while the
languages above and the hero below end at 1340 (E/home-fr-1440-closed.png — the plate sticks out past «العربية»); at
1366 the key sits 83 px beyond the column (E/home-fr-1366-closed.png); at 1280 it is 9 px from the viewport's edge
(E/home-fr-1280-closed.png). Signed in, the seat is 136–141 px wide, so Arabic at 1366 overflows too (seat at x 58 vs
the column at 135: E/home-ar-1366-signed.png). Numbers: E/measures.json `*-closed.inner / tops / targa`, the
`signed_fit.py` run (fr-1440 end 1281–1420 vs column 100–1340; fr-1366 1282–1314 vs 135–1231; fr-1280 1239–1271 vs
92–1188; ar fits everywhere signed out). The builder's checks measured document overflow only, which stays 0 because the
viewport still has room. At the most common laptop widths the letterhead does not hold the grid: below the bar.
*Fix (the builder chooses, DS 2026 §7.2 is theirs):* either (a) keep the six items from 80rem and make them fit —
the label of the plate only from the measured threshold (≈ 95rem: at 1440 the key alone gives 1212.5 ≤ 1240), and at
80–90rem the compact lock-up (32/17), item padding 8 px and `gap: var(--s-4)` (≈ −85 px → 1094 ≤ 1096, tight — measure
Italian and English too); or (b) move the six-item threshold to 90rem (the 64–90rem band = four doors + «Menu», which
already fits) and the label to 95rem. Acceptance: the end zone's inline-end edge equals the column's edge at 1280, 1366,
1440, 1512 and 1920, fr · ar · it · en, signed out and signed in; `test_header_fits_the_narrowest_viewport` or a
per-family test should assert `end.right ≤ inner.content.right` at those widths, not only `scrollWidth`.

**M2 · WCAG 1.4.12 text spacing: the page overflows horizontally and chrome leaves the viewport (French).**
Under the standard override (line-height 1.5, letter-spacing 0.12em, word-spacing 0.16em) `scrollWidth` is 1600 at
1440, 1426 at 1280 and 1089 at 1024: the plate starts at x 1436 and is not on the 1440 screen at all
(E/home-fr-1440-spacing.png), and at 1024 the «Menu» button is cut by the viewport (E/home-fr-1024-spacing-door1.png).
Arabic passes. Plan §1.12 item 9 is the family's own acceptance: «the bar wraps, or falls back to the 1024 layout; it
never clips». The entries and the gloss inside the panel are fine (nothing clipped, lines whole).
*Fix:* a wrap allowance for the bar under pressure (`flex-wrap` on `.site-header__inner` or `.main-nav__list`, the
header growing by one row only in that case), or the fall-back to the band layout; M1's fit removes most of the
pressure first. Acceptance: under the override at 1024 / 1280 / 1440 fr + ar, `scrollWidth == clientWidth`, the plate
and «Menu» inside the viewport.

**M3 · Three of the four door panels are three-quarters empty, and every panel splits its lede into two corners.**
The one height (570 px fr, 488 ar; LA-7 — a plan decision I do not contest) is the Personnes panel's. Entreprises
(two rows, no second line, 97 px of content), Institutions and Universités (two rows with lines, ~160 px) then show
~450 px of bare paper across eight columns at 1440 (E/home-fr-1440-door2/3/4-hover.png) and more at 1920
(E/home-fr-1920-door2.png). The photograph carries the right third; the sheet reads unfinished. In every panel the
lede column pins «Voir l'espace» to the bottom (`.portico__space { grid-row: 2; align-self: end }`) while the gloss
sits at the top: 340 px apart in Personnes, 460 in the sparse doors (E/home-fr-1440-door1-hover.png). The comp had
«Voir l'espace» at the end of the gloss sentence. Excellent products never show a 1240 × 570 overlay with 5 % content;
this is the first thing the owner sees after Personnes.
*Fix, inside the plan:* `.portico__space` directly under the gloss (`align-self: start; margin-block-start: var(--s-4)`;
the entries keep `grid-row: 1 / span 2`): the lede becomes one block — gloss, then the link — and the void below reads
as the grid's air, not as a missing column. Consider closing the entries list with a hairline under the last row in
the door panels, so a short list ends instead of trailing off. Re-check the Arabic panels (488 px) and the plain Projet
panel after the move. Content stays live-only; the B1 lines remain the owner's.

**M4 · At 360 px the brand name disappears from the header.**
`chrome.css` §1 hides `.lock__text` at ≤ 23rem (368 px), a V4 rule moved verbatim. At 360 — the most common Android
width, and one of the four widths of this review — the header is the mark and a hamburger (E/home-fr-360-closed.png,
E/home-ar-360-closed.png, measures `fr-360-closed.lockup` = 38 px wide); the builder's note says the name is kept at
320, but build3/home-fr-320-closed.png shows the mark alone there too. The arithmetic says the name fits: at 14 px the
lock-up is 227.5 px, the icon-only «Menu» 46 px, the margins 2 × 20 → 313.5 ≤ 320 even at 320 px, with the word «Menu»
staying hidden at ≤ 23rem as now.
*Fix:* hide the name only below 20rem (or not at all) and keep «Menu» icon-only at ≤ 23rem; verify 320 / 340 / 360 /
390 fr + ar, no overflow, lock-up intact. One line, but the brand on phones depends on it.

### Minor — polish

**m1 · Three live second lines the builder's own rule admits are missing in the Projet panel.** `_SECOND_LINES`
shows a line only where a live sentence ≤ 160 characters exists; the pages behind «Italy Legal Entry» (86 chars fr /
62 ar), «Réseau» (70 / 47) and «Contact» (64 / 43) each open with one, unused, while «Actualités» has its line. The
Entreprises door was checked too: its two pages' first sentences are longer than 160, so its empty rows are honest
(probe: `.work/w2-c1/w2-c1-review/probe_lines.py`). Add the three keys (`("", "pages:project")` etc.) with their
pages' sources.

**m2 · The prescribed French gloss on the Arabic page is set ragged-left.** The span carries `lang="fr" dir="ltr"`
inside an RTL paragraph, so the French runs right-aligned (E/home-ar-1440-door1-hover.png). Put the `dir` on the
paragraph when `gloss_lang` is set (or `text-align: start` following the span's direction) so the French block is
ragged-right in its column, until the Arabic copy is signed (B1).

**m3 · The signed-in seat colours the person glyph gold.** `.targa-seat .account-menu__summary .icon:first-child
{ color: var(--identity-key) }` paints the account icon in the key's gold (E/home-fr-1440-signed.png); gold is the
key's, not a person's. Keep the glyph in ink (W2-C2 replaces the popover, not the seat).

**m4 · DL54 has no entry from this family.** The three decisions met during the build (Home / End move the open
panel; the plain panel's gloss keeps its language; the one height is the content's honest height) are in `NOTES.md`
only. DL54 «How it is kept» and the ownership slice expect one dated, append-only entry each, before the merge.

Not findings, for the record: the reduced-motion state reads 0.01 ms until W1-D deletes `components.css` §29 (the
V5 rule is already in `chrome.css` §9); the eight scripts before `load` (the `nav.js` chunk split) are the build
script's, W4-B / the steward's, as the builder says; the two «pageerror» lines in the a11y-perf lane's results are its
own injected script (this review's 28 keyed page loads logged 99 console messages, all W1-A's Vazirmatn preload
warning, 0 errors); the drawer's
segmented «ع» track is V4's by design until W2-C2.

## N18 — «richer than Fase 3», the comp beside the build

Sheets: E/n18/n18-1440.png and E/n18/n18-1920.png (left the comp `proof/home/phase3-menu.html` served from the proof
folder, right the build, Personnes open in both); singles comp-*.png / build-*.png; numbers in E/n18/measures.json.

| | Fase 3 comp (gate 0) | Build `dc29569` |
|---|---|---|
| Panels | one (Personnes) | four door panels + the plain Projet panel |
| Panel box, 1440 | 1408 × 463 from x 16 (viewport-inset, NV-5), radius 20 | 1240 × 570 in the content column (N1), 12 px bottom corners (DL54-14) |
| Gloss | Source Serif 22 px, «Voir l'espace» inline at its end | Host 20/28, «Voir l'espace» at the column's foot (M3) |
| Entries | two columns, a glyph per entry, descriptions clamped to two lines (268- and 245-char leads cut with «…») | one column on hairline rows, 17/24 500, second lines whole (147 / 105 / 114 / 89 chars), none invented |
| Photograph | one, inset in the panel, 469 px wide | the door's own, in colour, V5 grade, bleeding to the panel's edge, 413 px, audience disc on a night plate, 3 px accent rule |
| Indicator | a line under the open door | «l'architrave», one travelling 2 px line on the seam, physical pixels, spring, no travel on first placement / keyboard / reduced motion |
| Reserved area | a link in the utility bar (leaves at the first scroll, NV-1) | «la targa» in the letterhead's end zone, both states, key alone below 90rem with a tooltip, the account menu in the same seat when signed in |
| Keyboard | none | the §4.8 model complete, fr + ar |
| Scrim | always | click, tap and keyboard only, never over the institutional bar |
| Also in the comp | a search button, «Fermer» | no search exists in the product; the door toggles itself |
| Removed | — | per-entry glyphs (DE-2), the serif gloss (§1.1), the truncated description |

Judgement: richer, more premium and more dynamic as a whole and on Personnes; the sparse doors fall below the comp's
density until M3 is done.

## What was checked, and how it stands

| Check | Result |
|---|---|
| Keyboard model, fr and ar (E/measures.json `*-kb-*`) | Tab reaches the first door (7 stops), ring 2 px inset; ↓ opens and enters (scrim on); ↓↓ walks; ↑↑↑ returns to the door with the panel open; → opens the next door (ar: the previous, the eye's direction); End / Home open Projet / Personnes; Esc closes, focus stays on the door, scrim off; Enter re-opens; Tab through the 8 links leaves to the next door (panel open until focus leaves the navigation, APG); Shift+Tab out of the navigation closes. Matches NAVIGATION §4.8 line by line. |
| Pointer | hover opens without a scrim; a click pins and the scrim starts at y 97 (never over the bar); re-click closes; entry hover tints the row and the title; the safe triangle held the panel over 272 px (fr) / 206 px (ar) of travel to door 3. |
| 1024–1279 | four doors, no chevrons, the panel without its photograph (944 / 1096 px wide), key alone, «Menu» opens the side drawer with the languages, Forum, Projet; Esc closes it and returns the focus to «Menu». |
| Whole texts | no second line clamped or clipped at any width, under text spacing included; glosses whole. |
| «La targa» | hairline plate, radius 6, gold key, label from 90rem, key alone with a tooltip below, tint on hover, flag-gated, the account menu in the seat when signed in, the 44 px plate in the drawer — §1.11, except that the label threshold was not measured (M1). |
| fr / ar | RTL correct: architrave from the right, entries at the first door's inline start, plain panel at the inline end, arrows follow the eye; Arabic lines where they exist, never a French line in an Arabic list; the French gloss drawn LTR (m2). |
| Phone drawer, 390 and 360, fr and ar | opens from the header's real foot (y 57), promoter, plate, languages, six rows, sections unfold with the anti-fraud link, Esc closes the section then the drawer, focus loop, no overflow. 360: the name missing (M4). |
| Scrolled | 56 px bar, lock-up 32/17, glass only with no panel open; the panel from y 57. |
| Interior page | `/fr/faq/`: Personnes current with the architrave at rest, «FAQ» marked in the panel; ar the same. |
| Forced colours / reduced motion | borders and Highlight indicator; reduced motion flattened by §29 (W1-D). |
| Console / CSP | 0 errors over the series' 28 keyed page loads (99 messages, all the Vazirmatn preload warning); no inline style or script; photographs 0 before `load`, the four at idle from 80rem. |
| Tests | `tests/frontend/test_browser_w2_c1.py` + `tests/i18n/test_rtl_browser_nav.py` on `test_ile_v5_l9`: **10 passed** in 125 s. The full suite not run (V5.5: integration checkpoints). |

## Lane state

The server on 8889 is left running from `C:/tmp/ile_wt/v54-w2-c1` for the fix step (stop: the process listening on
127.0.0.1:8889 only); the builder's 8789 is also up. Profiles under `.profiles/w2-c1-review/`; captures in E/ as
listed; the N18 sheets in E/n18/.
