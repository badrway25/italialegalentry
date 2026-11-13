# W4-C shipped — 27 October 2026

**Performance + accessibility consolidation — every page type measured on the compressed twin 8782, the accessibility
critical checks in fr and ar, real defects fixed.** Tag **`v54/w4-c`** (design-v5 `35b51c3`, the status
commit, as for the earlier families); merge commit `3ca6579`. The owner's preview on http://127.0.0.1:8780
serves it: v5-live checked out at the tag, 8780 restarted at 20:25 on 27 October and verified by request
(`verify_8780.log`: every request as expected, 0 failures; no traceback in the server log). Steward's merge, label `w4-c-merge`, under
`DESIGN_V5_MERGE_LOCK`, attempt 3: the first (16 October, 16:00–16:50) stopped at the tests because the shared
database was down; the second (17 October, from 01:29) was cut by the machine's reboot during the browser tests while
holding the lock; this one took that lock over at 19:38 on 27 October, design-v5 clean and unchanged at `96b6e96`, on
the Docker database again (`evidence/v54/SERVERS.md`, «27 Oct 2026»). Reviewed once and fixed
(V5.5): `REVIEW.md` and `A11Y_PERF.md` were both SHIP_AFTER_FIXES with no P0 (both majors and the cheap minors fixed in
the one fix pass, the rest handed on by name — `NOTES.md` «Review fixes»). The record: DL54-159 (the family's
decisions) and DL54-160 (the merge).

## What shipped

W4-C composes no page: it ran the release gates' two checks on the candidate — every page type measured, every page
read for accessibility in French and in Arabic — and fixed the real defects it found in the files of the families that
draw them.

- **The release gates' two checks, run on the candidate.** *Accessibility* (`A11Y_SWEEP.md`): 101 pages — every
  surface of the preview, the four organisation bridges, the staff's pages, the error pages, the open menu, a
  questionnaire step — × fr, ar × 1440, 390: the accessibility tree and axe-core 4.13.0, the keyboard walk at every stop,
  contrast on the pixels and non-text contrast, forced colours, 400 %, text spacing (1.4.12), every overlay opener, the
  tooltips, the forms' errors, Arabic's language of parts. **0 axe violations on 404 page views; 11 444 Tab stops, each
  with a visible indicator, none hidden under a fixed bar; the lowest ring 3.44 : 1, the lowest text 5.19 : 1; no
  overflow at 400 %; no WCAG 2.2 AA failure left after the fixes below.** *Performance* (`PERF.md`): the twin 8782
  serving the branch, compressed and production-like, 78 page types × fr, ar × 1440, 390, slow 4G + CPU × 4, five cold
  loads a cell (1 560 loads): **LCP — slowest median 1 508 ms (budget 2 500); INP — every overlay's cold open ≤ 120 ms
  at p90; CLS within budget everywhere** once the upload page was fixed; HTTP/2 measured.
- **F1 — the questionnaire's resume form says its errors as every other form does**: the shared summary
  (`role="alert"`, a link to the field) and the focus on it after the round trip, in place of a bare line that left the
  focus on `<body>` (`templates/orientation/resume.html`).
- **P1 — the Dépôt is drawn at its final size from the first frame**: the upload page no longer shifts when its module
  arrives (CLS 0.042–0.071 on every load → **0.000**), a piece's page likewise.
- **M2 — the Dépôt is never silent**: until `depot.js` has arrived (late, or lost on the way), a chosen file shows the
  browser's own control in the frame with the file's name; a file chosen while the module travels is taken up when it
  arrives; a new choice or a send empties both live regions first.
- **M1 — «Ma situation» declares its two personal fields' purpose** (WCAG 1.3.5): the date of birth `bday`, the country
  of residence `country-name` (`SituationForm`).
- **m2 — «Privacy Policy» and «Cookie Policy» are read in English** where they stand alone (`lang="en"`): the public and
  console footers, the virtual Forum's join form, the Forum's privacy note; inside a translated sentence the name is the
  document's proper name (docs/ACCESSIBILITY.md, 3.1.2, G-08).
- **m4 — four budget letters written as accepted exceptions**, none with a measured cost (the overlay core 6.5 KB
  against 4 KB per module; Arabic console pages with the monospaced face 63 KB of fonts against 56 KB; the entrance
  pages' one script request over V4's count, a 394 B helpers chunk; the work after the first paint as the rest of the
  first render) — also in the release notes' known limits, which now carry W4-C's figures.
- **Shared CSS (V5.8)**: on the merged tree, `main.css` 31 637 → **31 637 B** gzip on every page, the console page types
  39 798 → **39 798 B** — unchanged; `documents.css` (page-only) 5 566 → **5 564 B**.

## The merge

- design-v5 `96b6e96` → merge `3ca6579` (`--no-ff`, no conflict: the branch was synced at `96b6e96`, W4-C's entry
  renumbered DL54-159), `d1d036b` (DL54-160, the merge's record), `35b51c3` (the status and the changelog; tag
  `v54/w4-c`), then this note. The inventory was current (no commit).
- Ownership (`check_ownership.py w4-c 96b6e96`): 5 inside, 2 slice (the decision log, append-only; `SituationForm`'s
  two widgets, assigned to W4-C in the manifest with its reason), 5 generated, 13 delegated, and the manifest itself
  (the steward's own write); 0 outside. `--validate`: 30 families, 785 entries.
- Bundles rebuilt from a clean dist: byte for byte. Shared CSS gate: `main.css` 31 637 → 31 637 B, the console page
  types 39 798 → 39 798 B, `documents.css` 5 566 → 5 564 B (gzip 9).
- Targeted tests on the merged branch, lane 4, one pytest and one Chromium at a time: **941 passed** (non-browser) and
  **311 passed** (browser, Chromium); no failure, no skip, no crash. The full suite is left to the next integration
  checkpoint.
- Evidence: `C:/tmp/ile_v5_council/evidence/v54/w4-c/merge/attempt3/`.

## On http://127.0.0.1:8780

- http://127.0.0.1:8780/__design-v5/ — the strip names `v54/w4-c`; the index carries the family row w4-c and
  http://127.0.0.1:8780/__design-v5/decisioni/w4-c/REVIEW.md
- http://127.0.0.1:8780/fr/ and http://127.0.0.1:8780/ar/ — the footer's «Privacy Policy» / «Cookie Policy» in
  `lang="en"`; http://127.0.0.1:8780/fr/forum/ likewise
- http://127.0.0.1:8780/fr/orientation/reprendre/ and http://127.0.0.1:8780/ar/orientation/reprendre/ — the resume
  form's errors through the shared summary (F1)
- Through the preview's persona switch (`qa-doc-person`): http://127.0.0.1:8780/fr/espace-reserve/ma-situation/ and
  http://127.0.0.1:8780/ar/espace-reserve/ma-situation/ (`bday`, `country-name`, M1);
  http://127.0.0.1:8780/fr/espace-reserve/mes-documents/; http://127.0.0.1:8780/documents/upload/ (the Dépôt at
  its final size from the first frame, P1; the browser's own control until `depot.js` arrives, M2)

## Not done

- **To W4-D**: the letterhead's intermittent shift on public pages (medians ≤ 0.02, within budget); `card.css`'s
  French colon in every language (G-14); the focus ring cut at the viewport's bottom edge; the overlay core's wiring
  at load (a lead, not a defect).
- **To the steward**: esbuild's 394 B helpers chunk, one script request over W1-0's count on the entrance pages. It is
  an accepted exception with no measured cost, so it was not taken at this merge.
- **To W3-C / W3-E**: `lang="fr"` on records whose language is known, once the content plumbing carries one.
  **To W2-C1 / the steward**: «Formation» marks two doors `aria-current`.
- **What DL54-158 item 10 handed to W4-C after its fix pass** (the Academy's filter row's focus, the console's foot
  scroll padding above phone widths and the trail's 24 px under a mouse, the console drawer's brand ring 4 px over the
  screen's top): open, for the next pass the orchestrator sends.
- **Not run**: Playwright WebKit and Firefox (no binary on this machine), a real phone, a screen reader used by a
  person; the full test suite (the next integration checkpoint's).
