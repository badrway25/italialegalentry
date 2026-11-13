# V5.29 «SMALL LAYOUT & BRAND REFINEMENT» — stream BRAND (label `v529-brand`, branch `v524-brand`)

Directive: V5_29_FINAL_PREMIUM_VISUAL_REMEDIATION.md, last section (owner, 6 Nov 2026 21:49). One implementation pass, one
targeted headed review, one fix round. Lane server 8794 (database lane l6), pytest on `test_ile_v529_brand`.

## What changed

1. **One horizontal system of three related widths** (`v5/tokens.css` §3.6): `--content-wide` is the content's column
   (the container, 1176 · 1320 · 1440 px, unchanged), `--site-shell-max` the letterhead's shell (the column + 10rem,
   capped by the viewport less the `--grid-margin` gutters: 40 px at 1440, never the edge), `--form-wide` the premium
   form's band, which stands on the shell. The letterhead's inner reads `--site-shell-max`; the scrolled letterhead is
   the same box, the same width; the mega panels hang from it.
2. **The formwork** and its band (`.formwork-section` / the chapter that holds it) are `--form-wide` (was 71rem inside the
   column): the side 26 % (15rem floor), beside the panel from 56rem of the formwork's width (was 60rem: 1024 now shows
   the two columns); the panel's measure 60rem; the fields on two equal columns from 36rem — a line field one cell, a
   pair, a text area and the details across; a form without steps pairs its line fields two by two. One column on a
   phone. No field, order, string or behaviour changed.
3. **The lock-up** from 80rem is 36/19 (the verbatim 38/20 ratio; it was 32/17), at rest and scrolled alike; 64–80rem and
   the phone unchanged. Header height unchanged.
4. **The key** (nav.js `initBrandKey`, WAAPI through `motion.js`'s `play()`): rest → a 16° counter-turn (14 %) → the turn
   about its shaft to 364° (`--ease-turn`) → the settle on 360° (`--ease-enter`), `--motion-key` (1 200 ms), at the
   brand's reveal and on its hover / focus; one turn at a time, no fill, no loop; the origin is loader.css's 50 % — the
   shaft, the key's own centre per DL54-08. The planes, the door, the steps and the wordmark never move; the host stays
   `direction: ltr`. Decided with figma-use-motion's method (one keyframe track, per-segment easing, motion-easing.md).

## The fix round

Round 1 widened the content's column itself (1176 · 1248 · 1400 · 1520). The targeted tests showed what it moves: every
composition and image `sizes` measured on the column (the home's door at 96–100rem, the route board's lane frames at
1600, …) — a re-composition of every page, which V5.29 does not ask. The fix: the column stays; the shell and the form
widen around it. Round-1 stills: evidence/v529/brand/round1-global-container/.

## Measures (1440 × 900, French, classic 15 px scrollbar)

| | before | after |
|---|---|---|
| letterhead shell (inner box / content) | 1 320 / 1 240 | 1 425 / 1 345 |
| brand's distance from the window's edge | 92 px | 40 px |
| formwork (side · panel) | 1 136 (296 · 840) | 1 345 (350 · 995) |
| header height rest / scrolled | 65 / 57 | 65 / 57 |
| lock-up | 259 × 44, mark 32 | 289 × 44, mark 36 |
| main.css gzip -9 | 32 714 | 32 712 (≤ 32 716) |

At 1280: shell content 1 096 → 1 185, formwork 1 096 → 1 185; at 1024: formwork 929, stacked → side 241 · panel 687.

## Budgets

- main.css paid by custom properties nothing reads: `--rail-w-compact`, `--table-row-h`, `--grid-columns`,
  `--track-normal` (and their DESIGN_SYSTEM_2026.md rows), the unused `--container-lg / -xl / -xxl`, and one lock-up rule
  for both states in place of the scrolled pair.
- core/forms.css 5 551 → 5 603 B (no ceiling bites).
- **Re-recorded under V5.20, citing V5.29 §3:** shell.js 4 694 → 4 866 B (ceiling 4 700 → 4 866,
  tests/frontend/test_motion_v512_a_w2.py) — the key's turn; no dead code in shell.js's sources to pay with.

## Tests changed (V5.20)

- test_forms_v515_b.py: `--measure: 46rem` → `60rem`, stronger: the formwork reads `--form-wide`, no 71rem, the two
  columns and the line field's one cell are asserted.
- test_motion_v512_a_w2.py: the shell.js ceiling above.
- New: tests/frontend/test_brand_shell_v529.py (the three related widths, the column unchanged, the letterhead and the
  form's band on the shell; the lock-up in both states; the key through the gate, never looping).

## The targeted review (headed Chromium, slot A; evidence/v529/brand/, review.json)

Navbar 1440 · 1280 · 1024 · 390 and forms 1440 · 1024 · 768 · 390 (Entreprises #formulaire, contact, institutions'
collaboration, the login, the company console's «Nouveau besoin»), fr + ar.

- scrollWidth = clientWidth everywhere; the letterhead one row at every width; scrolled keeps x and width;
- the mega panel spans the shell's content edges exactly (40–1385 at 1440, 40–1225 at 1280, 40–969 at 1024), fr + ar;
- the form's band starts and ends on the letterhead's edges (40–1385 at 1440);
- the key runs at load and on hover, completes after the pointer leaves, `getAnimations()` empty at rest; the keyboard
  reaches the brand on the 2nd Tab, ring 1.6 px solid, the turn plays, name and href unchanged; under reduced motion no
  animation is ever created and the key's transform is `none`;
- RTL: `.lock-sig` direction ltr, no transform on the host or the base — the artwork is not mirrored;
- axe: 0 serious / critical on `.site-header` and on every form, fr and ar, all widths.

Blockers: 0.
