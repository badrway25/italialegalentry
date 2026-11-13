# V5.22 lane P1 — Page Composition V2: journeys and spaces — QA round 3 (label `v522-p1-qa3`)

Reviewer: the senior design-engineering reviewer of lane P1. Branch `v522-p1`, worktree `C:/tmp/ile_wt/v522-p1`, head
`2793da9` (round 2 «improve2» on `09f7233`, both on design-v5 `22b0ddd`, which has not moved). Binding: `directives/V5_22_…REMEDIATION.md`,
`SECTION_SYSTEM_V2.md` (§0–§10; P1 = §3.3–§3.10, §9.4; acceptance §9.9; targets §10), V5.12–V5.21 standing rules, V5.20
strict test rule. Date: 2 November 2026, 06:50–08:15. Nothing in the worktree was changed by this review.

## Verdict

**Passed (round 3). 0 major, 9 minor.** Both round-2 majors are fixed and hold at every width, language and input
measured. Every owned page scores at least 4 on all six §26 dimensions.

- **Parcours (R2 M1).** A family chosen anywhere in the board brings its lane under the bar, and nothing leaves the
  layout. Measured on 116 choices: tap, click, arrows and no-JS; fr and ar; 360–1440 px; up to 2 200 px into the board.
- **Collaboration head (R2 M2).** It is now one quiet annotation: the hemicycle stands beside the recipients sentence.

The technical floor is clean:

- 576 runs at the eight widths × four languages with no overflow;
- axe at 0 serious in P1's sections;
- locked copy unchanged and its tests green;
- the preserved families untouched;
- budgets held (`main.css` byte-identical);
- no translateY + opacity in any P1 section;
- the lane's browser module 25/25.

The minors are polish and robustness. Fix m3 and m4 before merge: one rule each, in P1's own sheets. m6 is a G3-closed
overflow that already exists on design-v5; it belongs to S's head rule and is routed to S. m1 is a WebKit risk this
machine cannot measure. Check it on an iPhone before the owner's walk-through.

## Round 2 findings — verified

| R2 | Status | Measured (headed chromium-1234, lane server 8786) |
|---|---|---|
| **M1** Parcours: a deep choice folds the board out of view | **Fixed** | Method: wheel-scroll to 300 / 600 / 900 / 1 500 / 2 200 px into the board, then tap (phones, touch context) or click (≥ 768). **Phones** (360 / 375 / 390 / 430, fr and ar, motion allowed): 34 choices. Bar at 56–140; chosen lane top at 157 (156–158) px; board height unchanged (2 346–2 523 px); 8 stations drawn; count line in the bar; focus on the family's radio. At the first card's centre the hand hits the card: the radio takes no pointer. **Reduced motion:** 18 more choices, the same. **Desktop** (768 / 1024 / 1280 / 1440, fr and ar): 22 choices. Lane at 133–134 under a bar ending at 116 (157 under 140 at 768). **No-JS:** 12 choices, the same. **Keyboard:** 30 arrow presses at 390 / 768 / 1440, fr and ar. Each arrow brings its lane under the bar instantly. The 1.6 px ring shows on the chip and on the lane's name, and no section animation runs (`qa3_parcours_keyboard_arrows_autres_fr_390.jpg`). **With motion and raw input** (no test-driver pre-scroll): the page glides with no frame jump over 120 px. The lane's light runs once: `sez-run` in fr, `sez-run-rtl` in ar (the round-2 fix holds). The frame develops in 480 ms. Nothing is running 2.6 s later. Evidence: `qa3_parcours_phone_deep1500_before_fr_390.jpg` → `…_after_travail_fr_390.jpg`; `qa3_parcours_phone_deep900_before_ar_390.jpg` → `…_after_autres_ar_390.jpg`; `qa3_parcours_desktop_deep600_after_etudes_fr_1440.jpg`; `qa3_parcours_choice_motion_250ms_fr_1440.jpg` |
| **M2** institutions' collaboration head below the bar | **Fixed** | 8 widths × fr/it/en/ar. The drawing is 108 × 54 beside the sentence at every width: it never stacks above it. The sentence is 15/24 in the quiet ink; the lead is 22/34 (20/31 below 64 rem). Formwork top: 581 px of 900 at fr 1440 (548 in ar), 768 px of 844 at fr 390, 799 px of 800 at fr 360, so it starts in the first screen. In Arabic the drawing sits on the right reading edge, the two French boxes hang from the same right edge, and the lead's language is set (`lang="fr"`). On it/en the locked texts stay French (`qa3_collab_institutions_head_fr_1440.jpg`, `…_ar_1440.jpg`, `…_fr_390.jpg`, `…_ar_390.jpg`). One residue in Arabic: m5 |
| m1 Universités empty quadrant | Fixed | The frame top equals plate 2's top at every width ≥ 64 rem: 303 / 303 at fr 1440, 307 / 307 in ar, 325 at 1280, 326 at 1024. The last plate lies over the frame's edge by 24 px; §3.8 says 48. The empty paper is now the strip beside plate 1, about 600 × 190 at 1440 (`qa3_universites_filiera_fr_1440.jpg`, `…_ar_1440.jpg`) |
| m2 French runs in Arabic at the Arabic leading | **Partly fixed → m3** | Fixed: the Parcours cards (16 runs at 28 px), Formation's second-time body and the Diplômes definitions. Still at the Arabic leading: four places in P1's sections (m3) |
| m3 phone chips' scrollbar | Fixed | `scrollbar-width: none` and an edge fade in the ground's own token: on the left in fr, on the right in ar, at 390 / 360 (`qa3_parcours_phone_bar_ar_390.jpg`) |
| m4 doors' calls at 768 | Fixed | Call tops are equal: 453 / 453 (fr 768), 462 / 462 (ar 768), 500 / 500 (it 1024), 403 / 403 (en and fr 1280), 414 / 414 (fr 1440), 422 / 422 (ar 1440) (`qa3_pilot_doors_calls_fr_768.jpg`) |
| m5 double rule under the doors | Fixed | The help line has `border-top: none`. It stands 24 px under the 2 px sill |
| m6 test coverage of the deep case | Fixed | The phone test now chooses after a wheel scroll at 0 / 900 / 1 500 px, in fr and ar, with touch. It asserts the bar in view, the lane under it, the board's height and its eight stations. Green (below) |
| m7 catalogue / S's guards | Carried, not P1's | The same 9 declared reds (below) |
| m8 Diplômes on phones | Carried (Director) | One definition open at a time (deviation 3) |
| m9 target gaps | Partly met | Parcours composition and imagery now reach 4.5. Entreprises composition stays at 4 because of m4 (EN-1's hangers) |

## Scores (§26, 1–5; bar ≥ 4 on every dimension; 3 = clean but editorial or static)

Scored at 1440 and 390 in fr and ar, checked at the eight widths and in it/en. The test applied: «would a senior
designer, without context, call it a premium institutional legal-tech platform rather than an online report with cards?».

| Page | Comp. | Motion | Imagery | Interaction | Institutional | Coherence | Note |
|---|---|---|---|---|---|---|---|
| Projet pilote | 4 | 4 | 4 | 4 | 4.5 | 4.5 | m4/m5 fixed: the doors read as one sill |
| Parcours | **4.5** | 4 | **4.5** | **4.5** | 4.5 | 4.5 | the choice is now the page's best moment (R2 interaction 3.5). Score holds in Chromium: m1 is a WebKit risk; m2 count wording; m7 card bottoms |
| Pathway sheets (×8) | 4 | 4 | 4 | 4 | 4.5 | 4.5 | unchanged; PS-2 names m3 |
| Entreprises | 4 | 4 | 4.5 | 4 | 4.5 | 4.5 | EN-1's numerals and its caption beside the quote are good. Not 4.5 while EN-1's hangers end in mid-air (m4) |
| Recueil des besoins (head) | 4 | 4 | 4 | n/a (form) | 4.5 | 4.5 | unchanged |
| Collaboration — institutions (head) | **4** | 4 | 4 | n/a (form) | 4.5 | **4** | R2 3.5 / 3.5. Coherence 4: the Arabic 28 px start (m5); the head's seal against the preserved form's tile (§9.8) |
| Collaboration — universités (head) | 4 | 4 | 4 | n/a (form) | 4.5 | 4.5 | the lead's language now set |
| Institutions | 4.5 | 4 | 4.5 | 4 | 4.5 | 4.5 | unchanged; IN-1 phone leading m3 |
| Universités et formation | 4 | 4 | 4 | 4 | 4.5 | 4 | m1 fixed. Coherence 4 until the catalogue lands: the U1 kickers are French on it/en/ar |
| Formation | 4 | 4 | 4.5 | 4 | 4.5 | 4.5 | Arabic body at the Latin leading |
| Diplômes et titres | 4.5 | 4 | 4 | 4 | 4.5 | 4.5 | Arabic definitions at the Latin leading |
| Parcours interim (G3 closed) | 4 | n/a | 4 | n/a | 4.5 | 4 | m6 (pre-existing S head rule) |

No page is lower than in round 2 on any dimension. The two pages below the bar in round 2 (Parcours interaction 3.5;
collaboration head 3.5 / 3.5) now reach it.

## Major

None.

## Minor

- **m1 Parcours: the lane comes under the bar only where a tapped label focuses its radio (WebKit risk, not
  measurable here).** The mechanism is «no script, the browser's own focus». It works in Chromium (Android Chrome,
  desktop Chrome, Edge), as measured above.
  - The risk: MDN documents that Safari (macOS and iOS) and Firefox on macOS do not focus a checkbox, radio or button
    on click or tap. There, a deep choice will light its lane in place and update the count, but will not scroll.
  - Nothing folds any more, so a reader can never be stranded in any browser; this is round 2's desktop behaviour.
  - No WebKit build is installed on this machine, and downloading one is outside the standing rules.
  - Fix: try it on an iPhone before the owner's walk-through. Keep S's request 11 open for S-close as a progressive
    enhancement: `scrollIntoView` of the chosen lane on `change`, instant under reduced motion and from the keyboard
    (≤ 0.3 KB, a section module).
- **m2 Parcours: the count line says «3 parcours affichés» while all eight stay displayed.** Since round 2 this holds
  at every width. The polite live region tells a screen-reader user that three pathways are displayed while eight
  remain in the reading order. The bar says the same to a sighted reader looking at eight cards. Fix: a team string
  that says what the choice does, for example «Travail : 3 parcours». New msgids, with professional it/en/ar in
  S-close's pass.
- **m3 French runs in Arabic still at the Arabic leading in four P1 places.** This is round 2's m2, partly fixed.
  Each is the Arabic page against the French page at the same width:

  | Place | Arabic | French | Note |
  |---|---|---|---|
  | PA-2 step fragments `.come__testo` | 20/32 | 20/28 | 2–3 lines, every width (`qa3_parcours_pa2_leading_ar_1440.jpg`) |
  | IN-1 recipients sentence `.emiciclo__frase`, at 390 | 20/32 | 20/28 | several lines |
  | EN-4's French title | 36/50.4 | 36/43.2 | |
  | PS-2 authority names `.decide__nome` | 20/32 | 20/28 | single line |

  Fix: the rule the cards use, in P1's sheets (`_index.css`, `_institutions.css`, `_companies.css`, `_sheet.css`), or
  S's request 14.
- **m4 Entreprises EN-1: the hangers of panels 01 and 03 end in mid-air.** The stems stop short of their panels at
  every width ≥ 48 rem (gap in px, panels 01 / 02 / 03; `qa3_entreprises_en1_hangers_fr_1024.jpg`):

  | Width | fr | ar |
  |---|---|---|
  | 1440 | 28 / 0 / 28 | 14 / 0 / 14 |
  | 1024 | 42 / 0 / 28 | 28 / 0 / 28 |
  | 768 | 42 / 0 / 56 | 28 / 0 / 14 |

  The cause: each station is a grid whose implicit rows stretch to the tallest station (`align-content: normal`), so
  the shorter panels are pushed down. The flaw already shows in round 2's captures; the numerals make it more visible.
  Fix: `.imprese-demarche .flusso__tappa { align-content: start; }` in `_companies.css`. Alternatively S fixes it in
  `_sec-flusso.css` for every user of «il flusso».
- **m5 Collaboration-institutions head, Arabic, ≥ 48 rem: the note's French lines start 28 px inside the lead's.** The
  lead starts at 724 and the note at 752 at 1440, and 105 against 133 at 768 (`qa3_collab_institutions_head_ar_1440.jpg`).
  The cause: the sentence keeps `.card__text`'s 464 px measure inside a 608 px row, and the slack falls on the LTR start.
  The form pages load no P1 sheet, so the fix is S's request 13 (an `.emiciclo-nota` rule in `_fronte.css`, with the
  sentence `flex: 1`). The coupling to three borrowed main.css classes is the builder's own request 13.
- **m6 Interim Parcours (G3 closed): 10 px horizontal overflow in Arabic at 768–769 px, already on design-v5.**
  - Measured on a temporary server (8796, reference date 25 Sept): 128 runs, of which only ar 768–769 overflow
    (`qa3_interim_head_overflow_ar_768.jpg`).
  - The cause: the head's route node `.ingresso__lead::before` (`inset-inline-start: -50px`) follows the French lead's
    own LTR direction. The lead's box starts at 40 px, so the node hangs 10 px left of the viewport.
  - At other widths the node floats on the lead's left, away from the head's right-hand spine: x ≈ 680 against the
    spine's 1311 at 1440 (`qa3_interim_head_node_ar_1440.jpg`).
  - The same 10 / 11 px appears on design-v5 `22b0ddd` served the same way (8797), and P1 did not touch the interim's
    head call. It is S's head rule on P1's page.
  - Fix: S places the lead's node by the page's direction (`:root[dir="rtl"]`), or P1 adds a page-only override in
    `pathways/index.css`. Add ar 768 to the interim checks; round 2 never measured it.
- **m7 Parcours cards in one row have ragged bottoms (≥ 48 rem).** Card heights per row at 1440: Travail 202 / 258 /
  258 px, Études 286 / 202 / 202. At 1024: 258 / 342 / 286. The cards are `align-items: start`; a stretched row would
  read as one register. Polish.
- **m8 Phone keyboard: the checked chip can stay scrolled out of the chip row.** After the arrows reach «Autres voies»
  at 390, the ring shows on the lane's name and the count reads «1 parcours affiché». The chip itself sits beyond the
  row's fade (`qa3_parcours_keyboard_arrows_autres_fr_390.jpg`). A tap always hits a visible chip, so this is a
  keyboard-only nit.
- **m9 Carried, not P1's, unchanged:**
  - The steward carries `p1/catalogue/*.po` at merge. Until then «Voir dans le glossaire», «Destinataires» and the
    three U1 kickers render French on it/en/ar.
  - S's three reds, and S's update of the tag guard (request 2).
  - Diplômes on phones keeps one definition open at a time (deviation 3, Director).

## What passes (§9.9)

- **Composition and the Word/PDF test.** Every V2 section still carries at least two of drawing/image, signature
  motion, state, depth and spatial structure. Parcours' board now has all five. EN-1 reads statement → process.
- **No overflow (G3 open):** 18 URLs × fr/it/en/ar × 1440/1280/1024/768/430/390/375/360 = 576 runs under reduced
  motion. 0 px overflow, 0 script errors, 0 hidden legal notices. The only text outside the viewport is the preserved
  forms' honeypot labels (deliberate).
- **G3 closed:** Parcours interim, both collaboration heads and Recueil × 4 languages × 8 widths = 128 runs. Content
  complete, notices visible; only m6.
- **Reduced motion:** 28 full-page stills (7 changed pages × fr/ar × 1440/390). No `data-sec-state` written, nothing
  running. Routes are drawn, frames in colour, the arrival lit. The only animation is the preserved Lume veil on a
  context's first load (§9.8).
- **Motion vocabulary:** 28 full-page runs with a slow real scroll, every running animation sampled. No translateY +
  opacity and no text held from opacity 0 in any P1 section. Both survive only in the approved heads' `rise-in`
  (S / V5.15) and the preserved form's light. A choice on Parcours runs LIGHT (the lane's dash, 1.2 s) and DEVELOP
  (480 ms), then holds nothing.
- **Keyboard:** 16 Tab walks (8 pages fr 1440, 8 pages ar 390). No stop is obscured: the letterhead and the sticky
  family bar are counted (the page's `scroll-padding` holds). None is off-screen. Stretched tiles and PA-2's stations
  draw their 1.6 px ring on their plate. While the keyboard is the input, only the letterhead's transition and the
  Parcours head's halo run (S).
- **No-JS:** 40 runs (10 pages × fr/ar × 1440/390) with complete reading order and no overflow. The family choice works
  (12 choices above). The heads' «Nature» rows are at opacity 0 at the instant of load and at 1 by 1.6 s (the head's own
  CSS entrance, S / V5.15, as in round 2).
- **axe 4.13 (WCAG 2.0–2.2 A/AA):** 72 runs (18 pages × fr/ar × 1440/390), 0 violations. The one exception is
  `target-size` on Recueil fr 1440: the preserved form's step-rail link under the sticky letterhead at the probe's
  scrolled position, as in round 2. The radio group's name, role and value are clean: fieldset, legend, five radios,
  each named by its chip.
- **RTL:** the board, bar, fade, light (`sez-run-rtl`), cards, filiera, flusso, doors and heads all mirror. French
  locked runs keep their own direction. Residues: m3, m5, m6.
- **Legal notices (§1.7):** all visible in every run, including the pilot status plate, the how-it-works caveat,
  «Qui décide ?», the Formation notice, the «Nature» rows, «la protezione», the orientation caution and the forms'
  privacy links.
- **Locked copy:** `test_locked_content`, `test_locked_texts`, `test_prescribed_fragments` and `test_locked_split`
  pass. No registry, hash or catalogue file is in the lane's diff. The recipients note renders
  `p3.institutions.recipients` through `{% locked %}`, unchanged.
- **Preserved families:** no file of the navbar, Lume, forms, channels, privacy, portal, `base.html`, `tokens.css` or
  `main.css` is in `22b0ddd..2793da9`. The two form templates changed in their header block and `extra_head` only.
- **Ownership (§9.7):** this round's diff is P1's: `apps/pathways`, `apps/ecosystem`, `templates/pathways`,
  `templates/ecosystem`, the collaboration header block, and the two P1 test modules.
- **Budgets (gzip -9, the guard's call):**
  - `main.css` 32 718, byte-identical to `22b0ddd`.
  - Page sheets, each under its ceiling:

    | Sheet | Size | Ceiling | Note |
    |---|---|---|---|
    | `pathways/index.css` | 10 099 | 10 240 | 141 B headroom |
    | `ecosystem/pilot.css` | 9 487 | 9 728 | |
    | `ecosystem/companies.css` | 8 682 | 9 216 | |
    | `ecosystem/institutions.css` | 8 365 | 9 216 | |
    | `ecosystem/universities.css` | 7 614 | 8 448 | |
    | `pathways/sheet.css` | 9 676 | 10 240 | |
    | `pathways/training.css` | 8 759 | 9 728 | |
    | `pathways/diplomas.css` | 8 866 | 9 728 | |
    | the family sheets | 4 977 / 4 716 | 11 264 | |

  - Page totals, form sheets excepted (≤ 56 320):

    | Page | Total |
    |---|---|
    | Parcours | 55 500 (820 B headroom) |
    | sheet | 55 077 |
    | pilot | 54 888 |
    | Diplômes | 54 267 |
    | Formation | 54 160 |
    | Entreprises | 54 083 |
    | Institutions | 53 766 |
    | Universités | 53 015 |
    | form pages | 49 511 |

  - No new JS, image or request.
- **Performance (indicative, lane server, not the 8782 throttled gate):** LCP 0.78–1.20 s; CLS ≤ 0.0001 through load
  and scroll; a family choice causes 0 layout shift, and its events take 16–48 ms. One long task on the Parcours load.

## Strict-rule review of the round's test changes

All acceptable. Each cites QA_ROUND2 or SECTION_SYSTEM_V2 §0.1 / §2 B («nothing leaves the layout»), and each keeps or
strengthens its invariant:
- `test_on_a_phone_the_family_choice_is_one_bar_and_brings_its_lane_under_it`. Round 1's fold assertion («only the
  chosen family's stations») was the behaviour that stranded the reader; it is replaced by «8 stations, board height
  unchanged». The test adds five wheel-and-tap choices at 0 / 900 / 1 500 px in fr and ar, asserting the bar in view,
  the lane within 40 px under it and the count in the bar. Stronger, and it covers R2 m6.
- `test_choosing_a_family_keeps_every_station_and_lights_its_lane`: the selector follows the markup, and the board
  height, the lane under the bar and the far end are added. Stronger.
- `test_the_route_board_holds_the_eight_pathways_on_their_family_lanes`: radio placement and order, chip labels, and
  per-lane `sizes` (the fork). Same or stronger.
- `test_the_form_pages_open_on_their_space_s_compact_band_and_keep_their_form`: one annotation, and `lang="fr"` on both
  boxes in Arabic. Stronger.
- Four new browser tests: the annotation, the doors, the campus frame and the numerals. The added waits are new
  60–150 ms pacing steps, not raised timeouts. No skip and no loosened assertion.
- Gap: no test asserts the panel hangers (m4) or the Arabic leading of PA-2 / IN-1 (m3).

## Tests run by this review (lane DB `test_ile_v5_l6`, one pytest at a time)

- **Non-browser, targeted** (locked copy ×4, `test_pages_v522_p1`, `apps/ecosystem`, `apps/pathways` and
  `apps/enquiries` tests, `interior_w3_f1`, chapter marks, icons, sezioni, frontispiece, state chips, loader rules,
  bundles, o14, design docs, imagery, motion rules, `rtl_static`, catalogues, page integrity): **1 239 passed,
  9 failed** in 28 min. The nine are the declared nine, none naming a rule of this round:
  - the five catalogue / integrity cases for round 1's five msgids (plus two stale msgids), until the steward carries
    `p1/catalogue/*.po`;
  - S's `test_data_register…` (`sezioni/approdo.html`), `test_l3…` (`sezioni/mappa.html`) and
    `test_every_horizontal_shift…` (`_sec-tracciato.css`);
  - the tag guard (request 2).
- **Browser:** `tests/frontend/test_pages_browser_v522_p1.py`, **25 passed** (172 s, slot B 07:49–07:52).

## Observations for S, the Director and the steward (not P1 findings)

- The builder's notes say the family group answers «Arrows/Home/End as any radio group». Chrome's native radios take
  the arrows only. Home scrolls the document to its top, leaving the focused radio off-screen. The native pattern
  needs no Home/End: correct the notes; nothing to build.
- The recipients note borrows `.ingresso__lead`, so it enters with the head's approved `rise-in`. That is consistent
  with the head (S / V5.15), but it is text held at opacity 0 during the head's entrance. Request 13 would give it its
  own rule.
- `html:has(.percorsi-tracciato)` extends html's `scroll-padding` on /parcours/ only, from P1's page sheet. `chrome.css`
  is untouched, and the builder flagged it to the steward.
- The Lume pre-warm ghost and the Lume veil on a first load are the preserved family (§9.8), as in round 2.

## Evidence (`C:/tmp/ile_v5_council/evidence/v522/p1/`)

- Cited stills: `qa3_*.jpg` (27) in this folder.
- Full sets in `qa3/`:
  - `deep/`: the 116 choices (JSON per mode, before/after captures, keyboard captures).
  - `collab/`: both heads, 8 widths × 4 languages, with motion and settled.
  - `minors/`: filiera, leading, doors, bar, EN-1, board.
  - `sweep/` (576 runs), `shots/` (motion sampling), `rmshots/`, `nojs/`, `axe/`, `keys/`, `keys390/`, `sec/`
    (per-section viewports).
  - `motion/`, `spot/`: leading fr vs ar, card rows, inks, raw-input glide, keyboard animations, no-JS «Nature».
  - `interim/` (G3 closed); `diag/`: overflow bisect, design-v5 comparison, hangers.
  - `perf/`, `overview/`: downscaled full pages.
- Tools: `C:/tmp/ile_v5_council/.work/v522-p1-qa3/tools/`. They include `deep3.py`, `collab3.py`, `minors3.py`,
  `qa.py`, whose keyboard walk counts the sticky family bar as an obscuring layer, `spot3.py`, `motion3.py`,
  `diag_overflow.py`, `bisect*.py`, `hangers.py`, `perf3.py`, `cmp_dv5.py`, `chain1.sh`, `chain2.sh` and `with_lock.sh`.
  Logs are in `…/logs/`.
- Headed chromium-1234. Lock sessions, each ≤ 7 min and released, no takeover:
  - B 06:54–06:56, 06:56–06:58, 06:59–07:01, 07:01–07:04, 07:23–07:24, 07:24–07:28, 07:28–07:32, 07:32–07:36,
    07:36–07:42, 07:42–07:42, 07:42–07:44, 07:44–07:48, 07:48–07:49, 07:49–07:49, 07:49–07:52 (browser tests),
    07:52–07:52, 07:52–07:52, 07:58–07:58;
  - A 08:04–08:05, 08:06–08:07.
- Servers, all started for this review:
  - lane 8786 (DB l6, reference date 3 Oct);
  - temporary 8796 (the lane's tree, 25 Sept: G3 closed);
  - temporary 8797 (design-v5 `22b0ddd`, 25 Sept, for m6's comparison).

  8796 and 8797 were stopped after their checks, and 8786 at the end.
