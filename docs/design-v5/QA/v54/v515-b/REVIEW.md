# V5.15 W3: Lane B (Premium Forms + Icon Visual System), finishing review F1 (label v515f-b-qa1)

29 Oct 2026, 10:57–11:45. Reviewer: senior design-engineering reviewer, lane B, finishing round F1.

## Setup

- **Branch.** `v515-b` @ `72aa93f`, with a clean working tree. It contains design-v5 `7f2a02d` (merge `0ba1210`).
- **design-v5 has moved again.** HEAD is now `79769f6`, which adds the lane A merge `5f56542` and the catalogue sync. The branch does not contain it yet; see m-1.
- **Lane server.** 127.0.0.1:8784, restarted fresh for this review from `.work/v515-b/srv.sh`: `ile_v5_l4`, dev settings, ILE_DESIGN_PREVIEW=1, ILE_REFERENCE_DATE=2026-10-03. A leftover runserver from 09:58 was holding 8784, so I stopped it first. My server was **stopped at the end** of the review.
- **Browser.** **Headed** Chromium 1234 (Playwright `headless=False`). The run used real clicks, typing, Tab, Shift+Tab, Space and hover, plus emulated reduced motion, forced colours and JS off. Personas came through the preview switch: qa-company and qa-fresh-person.
- **Lock.** I held `C:/tmp/ile_locks/CHROMIUM_LOCK` as `v515f-b-qa1` three times, only while a browser was open:
  - 11:25:16–11:26:41;
  - 11:26:51–11:34:34;
  - one short session for `/entreprises/`, released before 11:35:55.

  Before that I waited behind `v515f-c-qa1` and `v515f-d-qa1`. No lock was taken over.
- **Scripts and output.**
  - `fin1_review.py`: round 3's probe set plus F1's geometry, empty-state and password probes. Run per section; it writes `fin1_results_<section>.json` (11 files, about 470 probes).
  - Screenshots: `fin1_*.png` (285).
- **Targeted pytest** on l4, one at a time, against `test_ile_v5_l4`:
  - `test_forms_v515_b` (not browser): 27 passed.
  - `test_static_assets`, `test_icons`, `test_script_motion_gate` and `test_motion_rules_w4_b`: 72 passed.
  - `-k "motion_gate or budget or glyph or empty_state"`: 24 passed.

## Coverage

| Surface | Coverage |
|---|---|
| Public «Recueil des besoins», steps 1 and 2 | fr and ar at all 8 widths; it at 1280/768/390/360; en at 1440/1024/430/375. Every run also checked the night foot below 60rem and the hairline chain. |
| Full walks | fr 1440, ar 1440, it 1024, en 768, ar 390; fr 360 and fr 1280 with reduced motion. Each walk: empty «Continuer», fill, step 2, review, a 14-stop Tab walk, and the consent check (Tab past it untouched, then Space twice). |
| Sign-up | fr and ar at all 8 widths, it 768, en 360: card hover and the password checklist geometry. |
| Console need (qa-company) | Four steps and the review at fr ×8, ar ×5, it 1280, en 430. |
| Receipt | fr, ar, en, it; fr 360 with reduced motion. |
| Empty states (qa-fresh-person) | Mes demandes, Communications, Mes échéances and Mes documents at fr 1440/1280/768/375, ar 1440/390, it 1024, en 430, and fr 360 with reduced motion. |
| Public empty states using the same component | FAQ and glossary searches with no result, at fr 1440, ar 390, it 1024, en 375. |
| `/entreprises/` | fr 1440/1280/1024/768/390, ar 1440/1280/390, it 1440, en 1280, including a scroll check of the sticky side. |
| Other | Glyph tiles at 1× and 2×, at rest and on hover; forced colours; JS off. |

Across every probe: **no horizontal overflow, no duplicate ids, no page errors**. The only console errors are 404s on `/xx/forum-virtuel/` and `/calendrier/`. Those addresses do not exist; they were my probe's guess, not a product link.

## Verdict

**READY TO SHOW. Minimum family score: 4. No major findings.** All four of round 3's majors are fixed, and the fixes hold in the headed run at every width and in every language. Round 3's six minors are fixed or handed over. Two new minors remain; neither blocks showing the lane to the owner.

## Previous findings (round 3), verified

| # | Finding | Status | Evidence |
|---|---|---|---|
| M-1 | «Après l’envoi» hairline and 64px void below 60rem | **Fixed** | See [M-1](#m-1). |
| M-2 | Arabic French-fallback heads on the wrong edge | **Fixed** | See [M-2](#m-2). |
| M-3 | «Le besoin» ragged 2-up rows | **Fixed** | See [M-3](#m-3). |
| M-4 | Empty state a plain muted box (3.5) | **Fixed** | See [M-4](#m-4). |
| m | Forced colours: unreached rail link painted LinkText | **Fixed** | «3 Vérification et envoi» (`aria-disabled=true`) computes rgb(96,0,0), not LinkText rgb(0,0,159). Reachable links stay LinkText. |
| m | Password note 16px off the rule texts | **Fixed** | Note text and rule text start at the same x: fr 1440 at 831 and 831; fr 768 at 198 and 198; fr 390 at 38 and 38. In ar the right edges match: 594/594 at 1440, 337/337 at 390, 307/307 at 360. See `fin1_signup-fr-1440-pw.png`. |
| m | Consent painted on Tab | **Fixed** | In all 7 walks, Tab past the untouched box gives 0 errors. Space, Space, Tab gives 1 error. The narrowing of §5.5 is recorded in NOTES §13 for the Director to ratify. |
| m | Lane D msgids | **Handed over** | NOTES §13 lists the full set, including «Précisions facultatives». They are still French with `lang=fr` on it/en/ar, which is correct until lane D translates them. |
| m | `/entreprises/` night side never showed at desktop | **Fixed, with a residue** | The night side shows and is sticky at 1440/1280 in fr/it/en and on the right in ar. The residue is new minor m-2. |
| m | Glyph light reads as a gold tab at 1× | **Fixed** | `::after` has a 30% underglow. At rest it holds `scaleX(0.55)`; in RTL the gradient is 270deg with origin 100%. |

### M-1

- At 1024/768/430/390/375/360, in fr/ar/it/en, the notes have `border-top: 0px` and `margin: 0`, and sit 32px from the side's top (round 3: 64px).
- At ≥ 60rem the intended night rule remains: 0.8px `rgba(214,226,228,.14)`, 24px padding.
- `/entreprises/` below 75rem shows the same clean foot.
- Screenshots: `fin1_needs-fr-768-foot.png`, `fin1_needs-ar-390-s2.png`.

### M-2

`text-align: end` in RTL. Every head now ends beside its tile, at all 8 widths:

| Width | Step title | Sub-head | Note title |
|---|---|---|---|
| ar 1440 | ends at 928, tile 944–988 | ends at 988 = the fields' edge | ends at 1256, tile 1268 |
| ar 390 | ends at 271, tile 287 | — | ends at 287, tile 299 |

Screenshots: `fin1_needs-ar-1440-s2.png`, `fin1_needs-ar-390-s2.png`.

### M-3

- The order is unchanged: Nombre alone at 20rem, Q+E, L+F, Calendrier alone at 20rem, Notes across.
- In both pairs the fields share top and bottom: 1384/1486 and 1510/1612 at fr 1440. The same holds at 1280/1024/768 in fr/it/en/ar.
- In ar, a single field sits at the reading edge (668–988).
- Below 36rem the pairs stack cleanly.
- Screenshots: `fin1_needs-fr-1440-s2.png`, `fin1_needs-ar-1440-s2.png`.

### M-4

The empty state has no surface:

- an 88×120 rhythm arch with the xl 72px tile on its threshold;
- the title at 20px `--t-entry`, and the sentence in `--text-2`;
- the light animates once (`empty-light`) and rests at `scaleX(1)`; under reduced motion `animation: none`.

| Context | Measurement |
|---|---|
| Console fr 1440 | Arch and tile aligned to the page title's edge (280/288) |
| ar 1440 | Tile at 1088–1160, the reading corner |
| ar 390 | Stacked, tile at the right |
| Public FAQ and glossary (no result) | Same object, no overflow, at all four checked widths |

Mes documents shows no empty state for a fresh person, so it has nothing to judge there. The result reads as the page's opening statement, not a box.

Screenshots: `fin1_empty-fr-1440-mes-demandes-view.png`, `fin1_empty-ar-390-communications-view.png`, `fin1_pubempty-*`.

## New findings

**None major.**

- **m-1. The branch is behind design-v5 (minor, for the merge, not the design).**
  - Where: branch `v515-b`.
  - Detail: design-v5 is now `79769f6`, which adds the lane A merge `5f56542` (navbar, mega menu, Lume loader, motion language; it touches shared sheets) and the catalogue sync. `v515-b` has `7f2a02d` only.
  - Fix: merge `79769f6` into `v515-b` before the steward's merge. Then re-probe two things: the formwork under lane A's sticky letterhead (`fin1_entreprises-fr-1440-scrolled.png` shows the side under the header band), and the public pages that use the empty state now that `rise.js` moves sections in.
- **m-2. The formwork on `/entreprises/` stops short of the container's end edge at ≥ 75rem (minor).**
  - Where: `static/css/v5/_formwork.css`, the F1 chapter rule.
  - Detail: at fr 1440 the formwork runs 92–1228 (1136px, `71rem`). The letterhead and the next chapter's content run to 1340, so there is a 112px gutter on the end side only. In ar it mirrors (196–1332 against the logo at 1340). F1 said the formwork «spans the full container»; that holds for the grid columns, but the formwork's own max-inline-size caps it.
  - Fix: on that chapter, let the formwork take the container's full measure (`max-inline-size: none`). Or centre it, or keep it at the reading edge with the end gutter matching the start. Re-probe at 1440/1280 in fr and ar.

### Observations (not findings)

- **Tab order on desktop.** On the public form at ≥ 60rem, the rail links come after «Manifestez votre intérêt», although the night side is drawn first. The DOM puts the panel before the side, and the rail is a secondary navigation that repeats the step heads. This is acceptable under 2.4.3 and unchanged since round 1.
- **Arabic field labels.** On the Arabic public form the field labels are still French. That copy belongs to the catalogue (lane D), not to lane B. Re-check it after merging `79769f6`.
- **Phone-width «Précédent».** At 390/360 it is a 44px arrow and keeps its accessible name («Précédent» in the Tab walk). This is unchanged and correct.

## Scores (V5.15 §26)

| Family | Score | Why |
|---|---|---|
| Formwork, public «Recueil des besoins» | 4 | One 46rem measure, Continuer at the fields' end. The night side reads as one institutional object. Arabic heads are on the reading edge. The foot is clean below 60rem. The night side now shows on `/entreprises/` at desktop (end gutter m-2). |
| Multi-step engine and review | 4 | Errors focus the first field (5 on empty «Continuer»), the live line is localised, the review is a document, and Tab past the untouched consent says nothing. |
| Sign-up two steps + password checklist | 4 | The note sits on the rule texts' edge in fr and ar at every width. The head rail and card hover are as in round 3. |
| Console need (4 steps + review) | 4 | Clean at every width; the review is a calm document with the actions grouped at the end. |
| «Le besoin» composition | 4 | Like with like, rows aligned, singles at a short measure, Notes across. |
| Receipt | 4 | Route labelled in four languages, at the reading edge, calm under reduced motion. |
| Icon Visual System | 4 | Paper seal and reading-corner light with the 1× underglow. RTL mirrored, still under reduced motion. |
| Empty state | 4 | An opening statement in the doorway, not a box. Consistent on console and public pages, RTL correct, no motion under reduced motion. |
| 21st adaptation | 4 | Adapted, not pasted; provenance rows in NOTES §12 for lane A. |

**Minimum: 4. No major. The lane meets the bar of 4/5 per family with no major.** It can be shown to the owner once m-1's merge is done.
