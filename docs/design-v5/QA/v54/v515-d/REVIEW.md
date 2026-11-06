# Lane D: finishing review F1 (`v515f-d-qa1`)

- **Branch:** `v515-d` (worktree `C:/tmp/ile_wt/v515-d`).
- **Head:** `7f1afc9`, which contains the design-v5 merge at `9e65841`. `git merge-base --is-ancestor` confirms design-v5's HEAD is already in the branch.
- **Lane server:** 8786 (database lane l6, dev settings, `ILE_DESIGN_PREVIEW=1`, `ILE_REFERENCE_DATE=2026-10-03`).
- **Browser:** headed Chromium 1234 (Playwright `headless=False`).
- **Lock:** `C:/tmp/ile_locks/CHROMIUM_LOCK` was taken with noclobber in four sessions (15:03–15:13 probes, 15:13–15:21 and 15:21–15:27 pytest browser runs, then the person probe). None exceeded 25 minutes, and the lock was released after each.
- **Probe and raw results:** `C:/tmp/ile_v5_council/.work/v515f-d-qa1/fin1/` (`probe.py`, `rmprobe.py`, `res_*.json`, `pytest_browser.txt`).
- **Screenshots:** `qafin1-*.png` in this folder.

## Verdict

**The previous review's major (M-1) is fixed and verified.** The atrium rises from 3.5 to 4. Every family is now at ≥ 4 and there is no major, so lane D is ready to show the owner. The minors still open belong to the Director or the steward (locked copy, the gradients rule). None of them is lane D's to fix.

## What was inspected

- **Organisation dashboards:** university, institution and company, through the persona switch.
  - All four languages (fr, it, en, ar) at 1440, 1280, 1024, 768, 430, 390, 375 and 360, with motion: 96 loads.
  - Reduced motion: fr and ar at 1440, 768 and 390.
  - A frame-by-frame trace of the seal glyph during the load envelope (about 750 frames per run, 3.2 s), at 1024 in fr and ar, for each of the three.
- **Person dashboards:** person, fresh person and documents person, in all four languages at all eight widths: 96 loads.
- **Keyboard:** 22 Tab presses each on the university (ar 1440), company (fr 1024), institution (en 1280) and company (ar 390). Hover on the lattice cell and identity sheet.
- **Rail pages:** every page linked from the rail for each organisation persona at 1440 and 390, 37 page loads in all:
  - Mon organisation;
  - Mes demandes;
  - Communications, the register and one message;
  - the company's Espace entreprise;
  - Mes documents;
  - Mes échéances;
  - Guichet;
  - the language switch.
- **Results across all of these:**
  - HTTP 200 everywhere.
  - **0 px horizontal scroll** on every load.
  - **0 console errors and 0 page errors.**
  - **0 running animations** 2.8 s after load, on all 192 dashboard loads.

## The previous findings (latest review: finishing round F2, `d_state.json`)

| # | Finding | Status | Evidence |
|---|---|---|---|
| **M-1 (major)** | **The RTL counter-flip threw the seal's audience glyph about 150 units out of its seal.** This left an empty seal on the university and institution dashboards, and a stray gold mark in the company's head in Arabic at every width ≥ 768. | **FIXED** | `atrium_glyph` now wraps the `<use>` in `<g class="atrium__glyph-flip" transform="matrix(-1 0 0 1 2x+size 0)">`. The math checks out: x ↦ 2x+size−x maps [x, x+size] onto itself, reversed, so the glyph mirrors about its own centre. The CSS rule is gone.<br><br>**Measured on all 12 Arabic loads at 768–1440** (3 organisations × 1440/1280/1024/768): the glyph's centre is **0.0 px horizontally and 0.0–0.5 px vertically** from the centre of the `M160 62` ring, and the screen transform `a` is > 0, so the glyph is not mirrored. fr, it and en are identical (no wrapper, centred).<br><br>**Frame trace during the envelope** (ar and fr, 3 organisations): the maximum drift is **0.0 / 0.4 / 0.2 px**. The glyph fades in place (opacity 0 → 1) and never jumps.<br><br>Reduced motion gives the same positions. At ≤ 430 the phone band is drawn and, by design, there is no glyph; there is still exactly one wrapper in ar.<br><br>**Screenshots:** `qafin1-university-ar-1440.png`, `qafin1-company-ar-1024.png`, `qafin1-institution-ar-768.png`, `qafin1-company-fr-1440.png`, `qafin1-rm-*-ar-1440.png`.<br><br>**The new guard** `test_the_seals_glyph_stands_in_its_seal_in_every_direction` (1440/1024/768) passes. |
| m-5 (minor, Director §9) | **Locked French h1 and lead on the company dashboard in it, en and ar.** The company shows its locked h1 «ESPACE RÉSERVÉ» and the person-facing lead in French. | **NOT FIXED: locked copy, not lane D's** | Still shows in it, en and ar (`qafin1-company-ar-1024.png`).<br><br>**Wider than recorded:** the **fresh person** (no file yet) shows the same locked pair in all four languages, including ar (`qafin1-fresh-person-ar-390.png`). design-v5 has the same branch (`templates/portal/dashboard.html` l.61–64), so this predates lane D. Add the fresh person's page to the Director's §9 decision. |
| m-6 (minor, steward/Director) | **The gradients rule fails on `_platform.css`.** `test_conforming_app_stylesheets_use_only_design_tokens` finds 11 gradients in `apps/portal/static/portal/v5/_platform.css`. | **NOT FIXED: decision pending** | Still red: 1 failed, 132 passed in `test_platform_v515_d.py` + `test_design_docs.py` on lane l6. Required before the W3 merge: either move the gradients to tokens (lane A) or add the file to `KNOWN_NON_CONFORMING_APP_STYLESHEETS`. |

## New in this round

**Nothing at major level.**

Observations:

1. **Reduced motion: lane A's mark fades for 80 ms once, which is correct.** Under `prefers-reduced-motion: reduce`, the company's first load showed 3 `running` animations at 0.6 s. These are lane A's `lume-still` on the rail's brand tile and Lume mark: 80 ms, 1 iteration, `finished` at 5.6 s (`rmprobe.py`). This is the Lume's reduced-motion still, a crossfade far under a second. It is not lane D's and not a defect.
2. **Faint shell watermark behind the main column.** A very low-contrast brand mark (the open book with the keyhole door) sits behind the main column under the calm panel, on the company and institution dashboards (enhanced crop: `.work/v515f-d-qa1/fin1/zoom_company_ar_1024.png`). It is not in `_platform.css`. Treat it as the shell's deliberate ground unless lane A says otherwise ("visual defects are often deliberate"). It does not affect the ink or contrast of any text. No action for lane D.
3. **The merge resolution in `tests/frontend/test_dashboard_browser_w3_b.py` (w3-b's file).** For `.reg-calm` only, the new branch swaps the reading-measure and no-surface checks for a span check, and keeps lane B's rules for `.empty-state`. This is a documented exception and the open question is raised as a request to the Director and lane B. The steward must confirm it at the W3 merge (ownership §10.0). I accept it as is.
4. **Browser suites on lane l6:** `test_platform_browser_v515_d.py` + `test_dashboard_browser_w3_b.py` gave **31 passed, 22 failed**. Every lane D guard passes.
   - **The 22 failures are the pre-existing design-v5 set** recorded in `2811165` / DL54-173:
     - 18 × `c-rise` in the «nothing animates at load» gate. This is lane A's rise at load, in the one-primary and company first-viewport tests.
     - 4 × the bridge's register order. An institution now has its own dashboard.
   - The DRAFT-chip corner failure listed in earlier notes no longer appears.
   - None of the 22 is lane D's. They should go on the W3 merge plan, not on this lane.

## Scores (V5.15 §26)

| Family | Score | Why |
|---|---|---|
| Platform design energy: atrium | **4** (was 3.5) | **The seal stands complete in every language and width.** The audience glyph sits in the ring of the central arch, read the right way round in Arabic (0.0–0.5 px, `a` > 0). The company's stray gold mark is gone. Motion and reduced motion give the same still. The phone motif and the gold «here» station hold. |
| Platform design energy: dashboards and lattice | **4** | **The compositions are clean and there is no overflow anywhere:** the person's dashboard, the lattice, the identity sheet's facts lattice, the calm panel and the company composition, across 192 loads. The locked generic head on the company and fresh-person dashboards (m-5, Director) holds it at 4. |
| Platform motion | **4** | **Finite envelope, then still.** Nothing runs 2.8 s after load. The glyph fades in place with no jump. Under reduced motion only lane A's 80 ms Lume still runs. |
| Institution/University experience (Q7) | **4** | Both organisation heads are complete in Arabic again. The seal, the name, the folded «Présentation» at 1024 (head 205 / 218 px) and the CTA in the sheet's foot all hold. Keyboard order is logical in RTL, with visible rings (solid 1.6 px; cells take the ring). |
| Platform coverage | **4** | Every rail page answers 200 with no scroll or errors at 1440 and 390. The account and 2FA heads (lane B's files) are still waiting for the Director. |
| Terminology | **4** | The eyebrows are correct in four languages («Espace Entreprises» / فضاء الشركات, etc.). m-5 (locked French head, now also seen on the fresh person) and the rail label equal to its item stay with the Director. |

**Minimum: 4. Majors: 0.**

## Requests carried to others (not lane D)

- **Director §9:** the company's and the fresh person's locked h1 and lead in it, en and ar (m-5, widened).
- **Steward/Director:** the gradients rule for `_platform.css` (m-6), needed before the full ring is green at merge.
- **Director and lane B:** decide whether the empty state on platform registers is lane D's calm panel or lane B's statement with no surface (the test keeps both).
- **Steward at the W3 merge:**
  - confirm the edit to w3-b's `test_dashboard_browser_w3_b.py`;
  - plan the 18 `c-rise` and 4 bridge-order failures that design-v5 already carries.
- **Carried from earlier rounds:**
  - the Mon compte / 2FA atrium heads (lane B);
  - the it/en rail label equal to its item (Director);
  - the Circular Progress provenance row (lane A).
