# V5.12 W1: senior final review of the integrated lanes (label v512-review-w1)

## Scope and method

**Date:** 28 Oct 2026.

**Base and branches:**
- base: design-v5 `e047fae`;
- lane A: `102e2df`;
- lane B: `164c19f`;
- lane C: `e677099`;
- lane D: `984117c`.

**How the review was run:**
- A scratch merge, A→B→C→D, in `C:/tmp/ile_wt/v512-review`. The worktree was removed at the end.
- `npm run build` on the merge left the tree clean, so the dist files are coherent.
- A server on 8787, on database `ile_v5_l7`. The database was migrated, then `preview_data_clean --apply` was run on it.
- A targeted pytest run on `test_ile_v5_l7`.
- One headless Chromium, under the lock.
- Screenshots are in `C:/tmp/ile_v5_council/evidence/v512/w1/shots/`.

## Verdict: APPROVE_WITH_FIXES

The four branches merge with no textual conflict. Each lane delivers what its notes say. In the preview, the owner will see:
- the loader on real navigation;
- chapter marks that match their section's concept;
- the person's own words in the reserved area;
- no «work in progress» blocks.

Five integration defects must be fixed before the merge. They are listed as M1 to M5 below, and each one is a small change.

## What was measured on the merge

**The threshold.** Measured in Chromium with 2.5 s of network latency (DevTools emulation), in fr at 1440, ar at 390, and with reduced motion:
- the `is-departing` class arrived after 451–468 ms;
- «Chargement…» appeared after 1 057–1 063 ms;
- the arrival page carried `lume-arrive`;
- without throttling, nothing showed.

**Reduced motion.** The line appeared through an 80 ms fade, the logo's doorway showed lit, and nothing travelled.

**The console release.** The first page after entering as a persona carried 2 `data-lume=release` hosts (the rail and the top bar). A reload carried none.

**Budgets** (gzip unless stated):

| File | Base | Merge | Limit |
|---|---|---|---|
| `main.css` | 31 192 B | 31 177 B | 31 414 B |
| `shell.js` | 3 785 B | 4 368 B | 4 700 B |
| `console.css` | 7 116 B | 7 771 B | — |
| `pages.css` | 3 779 B | 3 795 B | 6 KB |
| `icons.svg` (raw) | 31 049 B | 30 878 B | under 31 049 B |
| `head.js` (render-blocking) | 919 B | 2 067 B | — |

**Hidden routes:**
- /actualites/, /partenaires/ and /vivre-en-italie/sante/ answer 404, and the sitemap is clean.
- I scanned `<main>` on 20 pages in fr, it, en and ar and found:
  - no WIP phrase;
  - no `icon-ile-steps`;
  - no link to a hidden route.

**Horizontal overflow:** none at 1440 (fr) or 390 (ar), on the home, a pathway sheet, living, forum, diplomas and FAQ.

**Terminology, as qa-doc-person:**
- the rail foot reads «Samira El Amrani / Espace Personnes»;
- the next action reads «Responsable : Vous»;
- the chip reads «Étape 1 sur 7 — Votre situation et votre objectif»;
- there is no scan word;
- the footer reads «Phase 3 / Fase 3 / Phase 3 / المرحلة 3».

**Tests:**
- 1 286 passed and 3 failed: `test_chapter_marks`, `test_interior_w3_f1` (the pathway index) and `test_icons` (the empty-state count).
- `test_design_preview` and the confidential-material test both passed.

## Major: fix before merge

### M1. Three tests fail after the merge

Two come from B×C semantic conflicts. The third fails on C's branch alone.

- **`tests/frontend/test_chapter_marks.py`**
  - B expects the «Documentation» mark (`document`) on `/fr/parcours/salaried_work/`.
  - C hides an empty Documentation chapter, so that page draws only the stamp and the compass.
  - So B's visible claim («a document for Documentation») is not visible either.
- **`tests/frontend/test_interior_w3_f1.py::test_the_pathway_sheet_has_its_index_in_the_entrance_and_no_sticky_bar`**: it expects `#apercu`, which C now omits when there is no eligibility text.
- **`tests/frontend/test_icons.py::test_the_empty_state_draws_its_space_or_the_neutral_mark_never_document_by_default`**: it asserts `callers >= 21` and gets 15. C removed six empty-state branches, and the test fails on C's branch even before the merge.

**Fix:**
- B makes the expected marks depend on which chapters are present, or seeds documents and an eligibility text in the fixture.
- B, which owns `test_icons.py`, sets the floor to the real count and cites C's removals.

### M2. «Chargement…» stays French on the it, en and ar pages

- `data-lume-word` reads «Chargement…» on /it/, /en/ and /ar/.
- In Arabic it renders as «…Chargement», reversed by the bidi algorithm.
- It is a `role="status"` line, so screen readers announce it.

**Fix (D):** add the msgid with «Caricamento… / Loading… / جارٍ التحميل…» (DECISIONS §1 T2) and compile the catalogues.

### M3. The profile still says «Type de compte : Personne»

- Seen at /fr/compte/profil/ as qa-doc-person.
- This is the role-word leak the owner named in V5.12 §11 (lane D acceptance item 1).
- D asked B for this change; it is not in B's branch.

**Fix (B, `templates/accounts/profile.html`):** replace the row with «Votre espace» → `{{ space_label }}`. The view already passes `space_label`.

### M4. The preview hub links to pages that now answer 404

- `apps/designpreview/live.py` still lists:
  - the living topic `/vivre-en-italie/logement/`;
  - news `/actualites/`;
  - partners `/partenaires/`.
- A crawl of the hub's 172 links finds all three answering 404 in fr and in ar.
- The owner uses the hub to accept the product.

**Fix (D):** drop the three entries, or annotate them «404 finché…» as the virtual Forum entry is. Then update `CENSUS_TYPES` in `tests/frontend/test_design_preview.py`.

### M5. The threshold fires where DECISIONS §1 forbids it

**After a download.** In `templates/community/discussion.html:57`, the attachment «Télécharger» link has no `data-loader="none"`. After the download, the gold line and «Chargement…» stay for the full 10 s lease.
- Fix: B adds the attribute.

**On OUTCOME_BEARING forms.** A grep finds no template carrying `data-loader-action`. So the threshold and the arrival light both play on the legal-answer forms, against DL54-09:
- the situation's recalculation (the wizard in `portal/situation.html`);
- the pre-assessment;
- an eligibility;
- a scan's verification.

Fix: D tags the portal forms, and the owners of the orientation and documents templates tag theirs, using the names in `static/js/src/loader.js`.

## Minor

### Lane A

**m1. The «Chargement…» label collides with the header controls.**
- The label sits on the header rule at the inline end.
- At 1440 it overlaps the current-door underline under «Projet».
- At 390 in Arabic it overlaps the bottom of the «القائمة» button.
- Offset it from the active indicator. See `threshold-*.png`.

**m2. The `<meta name="generator">` tag was not added** (D asked for it). Once D's change lands, the release number appears nowhere.

**m3. `static/js/head.js` is render-blocking and unminified.** It is 4.9 KB raw and 2.1 KB gzip. Consider building it through esbuild.

### Lanes B and C

**m4. `.chapter__mark` is still sized for the `ile-steps` drawing.**
- On the merge, the gap between mark and title measures 11 px, and the mark sits 3 px off the reading edge, in fr and in ar.
- B asked C to retune `_pagina.css` and `pages.css` for this.

### Lane C

**m5. `/forum/` can answer 404 while the navigation still links to it.**
- The page answers 404 when there is no live edition.
- The route has no gate, so `path_is_open` returns True and the link stays.
- Give it a gate, as news and partners now have.

**m6. `news_public()` returns True on the newsletter flag alone.** That would reopen a page with zero articles. Check that the page then shows no empty block.

### Lane D

**m7. One specimen draws nothing.** In `templates/dev/designpreview/specimens/icons.html:58`, `svg_icon "wrench"` draws nothing now that `wrench` has left the sprite (B's request). Use `briefcase-business`.

**m8. `preview_data_clean` counts differ between dry run and apply.** The dry run reported 69 changes and `--apply` made 80. The dry run does not count the sample files it restores. The orchestrator should expect this.

**m9. Account labels are uneven.**
- `AUDIENCE_SPACE_LABELS` mixes a space name («Espace Personnes») with identity words («Entreprise», «Institution»). So the profile row would read «Votre espace : Entreprise». Harmonise this in W2 together with Q7.
- The account button now uses `get_full_name`, which falls back to the e-mail address when no name is set.
- The `qa-*@example.test` address is still visible on the dashboard's account strip (already declared by D).

### Platform, already there before W1 (B/D)

**m10.** `discussion.html` still contains the WIP phrase «téléchargement bientôt disponible».

**m11.** As qa-company, `/fr/espace-reserve/` shows the generic «ESPACE RÉSERVÉ» lead. This is W2 work: the owner's Q7 answer rejected the minimal default and asks for a real organisation experience.

## Integration

**Shared-file ownership: respected.**
- A edited the header, `portal_chrome`, the tokens and `main.css`.
- C edited the gates and `cms_nav`.
- D edited the footer, the portal and the locale files.
- B and C both edited `faq/index.html`, `living/topic.html`, `partners/index.html` and `apps/pages/tests/test_home.py`, on different lines. The merge is clean.
- `DESIGN_SYSTEM_2026.md` was edited by A and B and also merges cleanly.

**Coherence: good, with two exceptions.** The gates, terminology, icons and loader do not contradict each other, except for:
- M1: B's tests assume chapters that C hides.
- M2, M3 and M5: cross-lane requests that no lane has picked up yet.

**Rules:**
- Locked copy, the hero and the legal pages are untouched.
- The default answers for C9, C10 and Q2 are honoured.
- Nothing presents ILE as an authority.
- No secret is committed.
- The preview names are fictional (Valfiorita and Collina Verde are invented places), and the confidential-material test passes.

**Merge order after the fixes: A → B → C → D.** Then the orchestrator:
1. runs `migrate` (core/0002 and academy/0002);
2. runs `preview_data_clean --apply` on ile_v5;
3. restarts 8780.
