# W3-F1 shipped — 12 October 2026

**The doors, the project pages and orientation — the public interior in V5.** Tag **`v54/w3-f1`** (design-v5
`744421b`, the status commit, as for the earlier families); merge commit `f371340`. The owner's preview on
http://127.0.0.1:8780 serves it: v5-live checked out at the tag, 8780 restarted at 07:19 and verified. Steward's
merge, label `w3-f1-merge`, under `DESIGN_V5_MERGE_LOCK` from 05:49 (after W2-C2's merge released it). Reviewed once
and fixed (V5.5): `REVIEW.md` and `A11Y_PERF.md` both SHIP_AFTER_FIXES with no P0; the fix pass (`NOTES.md` «Review
fixes», §20 – §25) closed the review's five majors and eight minors and the check's three findings; the first merge
attempt stopped at the shared-CSS gate (`NOTES.md` «Steward»), and the budget and consolidation pass (§26 – §35)
answered it under the owner's V5.8 and the orchestrator's definitive ruling. No reviewer has read the budget pass
again.

## What shipped

- **One grammar for the public interior**, the home's under the hero: the entrance «l'ingresso» at the reading edge
  (the space's name, the prescribed title and its text as written), chapters with the home's section device, registers
  on hairlines with the whole row the target, «la linea» for real sequences, the stone for the one action, «Besoin
  d'aide ?» with its address; no side column, no sticky section bar, no card grid; three corners a screen; ≤ 6 icons
  in an editorial body. The trail, the head, the chapters, the register and D26's shared slots are drawn **once**, in
  `static/css/v5/_pagina.css`, for these pages and W3-F2's content, legal and account pages (the owner's V5.8 rule 3);
  each surface keeps only what it draws in its own partial.
- **The four doors** — /parcours/ (Personnes), /entreprises/, /institutions/, /universites-et-formation/ — with «la
  porta» (the night plate, the brand's three steps lit in the door's tint, the audience's disc) carrying the door's way
  in: the questionnaire on Personnes, the prescribed button on Institutions and Universités, «Recueil des besoins» on
  Entreprises. The **pathway sheets**, «Diplômes et titres» and «Formation» (their moments on «la linea»), the
  anti-fraud callout as a warning notice.
- **The project pages** — the Forum and its registration (the programme numbered, the Forum's name saying its language
  on the Arabic page), «Le projet», the pilot (its eight stations on «la linea»; the growth-curve illustration
  retired), AGAMI, the network, the contact page, «Attention aux fraudes».
- **Orientation** — the questionnaire's first page («Commencer» in its entrance), a step (its place in words,
  «Question n sur N au maximum», never a percentage; «Pourquoi cette question ?» as a native disclosure; a refusal said
  in words, never colour alone), the pre-evaluation, resuming, «Enregistrement indisponible».
- **«Ma situation»** (console) loses `v4/wizard.css`: its guided form is the console partial `v5/_wizard.css` (4 · 8 ·
  full, one raised panel, the foot part of the page).
- **Arabic**: every page mirrors; French on an Arabic page says its language; fr and ar from 320 to 1440 px.

## The merge

- **The sync** (`47f7343`): design-v5 at `8e13cd2` — 42 commits since the budget pass's sync (W2-C2's phone sheet,
  account popover and panel on overlay.js, its steward's merge, status and shipped note, the confidential-material docs
  commit) — merged into the branch. Two text conflicts, both areas' work kept: DS 2026 §2's inventory rows (design-v5's,
  then regenerated: `v4/wizard.css`'s row out) and the decision log (design-v5's entries, then the family's);
  `components.css` and `main.css`'s import list merged clean, each exactly both diffs; the bundles rebuilt from a clean
  dist (the JS byte for byte design-v5's but for the shared chunks' names).
- **The numbering**: the family's entries are **DL54-103 … DL54-108** (written as DL54-78 … 82, then DL54-100 … 105;
  `NOTES.md`'s closing note gives the mappings); the steward's record of the merge is **DL54-109**.
- **The 31 paths outside the slice** are the area's in the manifest (`d4f4b40`): 21 whole files (the page partials
  `_interior.css`, `_pagina.css`, `_porta.css`, the page sheets and partials of the institutional pages, the doors, the
  Forum and the pathways, the console partial `_wizard.css`, the retired pilot illustration, ten test files) and 10
  slices (the pathways' and the Forum's services and views, `console.css`'s import line, W3-F2's `_lettura.css`,
  `lettura.css` and its test — the consolidation —, W1-C's chip test, W1-B's icon test); four slices named as written
  (`pages.css`, `register.css`, `layout.css`, DS 2026). The check after it: 75 inside, 27 slice, 24 generated, and
  the manifest itself (before: 31 outside).
- **The shared CSS (the owner's V5.8)**, gzip -9 of bundles rebuilt from a clean dist: **`dist/main.css` 41 029 →
  38 683 B (−2 346 B on every page)**; the console page types 49 770 → 48 556 B (−1 214 B; `console.css` +1 132 B
  carries «Ma situation»'s guided form out of `main.css`); the login, the home, the content, account and error pages,
  «Mes pièces» and the company's dashboard all lighter; every ceiling lowered to its merged weight. The area's own CSS
  is in its page-only sheets: the persons pages 42 177 B (their first page sheet, `pathways.css`, +1 148 B on their
  own pages), orientation 42 722 B (+361 B through its own sheet), the ecosystem doors 42 018 B, the Forum 42 177 B,
  the institutional pages 41 480 B — recorded as measured (DL54-109 items 4 – 6); the performance sanity check is the
  family's (NOTES §31: FCP equal or earlier, LCP within the spread).
- **The capture report and the inventory**: `capture.py` on lane 7, 43 captures, every one as expected and the report
  unchanged (nothing to commit); the inventory current after the sync's regeneration.
- **The tests** (`TEST_DATABASE_URL=…/test_ile_v5_l7`, one pytest at a time, every browser run behind the benchmark
  lock): on the branch, **2 065 passed** without the browser (tests/i18n, tests/compliance, tests/security, the
  orientation, ecosystem, pages and pathways apps, the Forum's public tests, «Ma situation»'s view tests, the
  family's and W3-F2's unit files, test_layout, test_design_docs, the two bundle-current tests, the static pipeline
  with a real collectstatic, O14, the chips' register, the icons, and what the merge touched besides) with 2
  failures — the merge's one semantic conflict: W2-C2's phone sheet draws a primary of its own earlier in the
  document, and two gated-door tests took it for the page's prescribed button; they read the page's content now
  (`78cb0de`; the file then 63 passed) — and 1 skip (the confidential-material check: the branch worktree's `.env`
  predates the private sentinel table); **159 passed** in the browser (the family's two files, the doors' and the
  home's, tests/i18n's RTL files with W2-C2's, W3-F2's two files and W3-A's questionnaire foot, W2-C2's browser
  file; no skip, no crash); on design-v5 after the merge, **826 passed** (the bundles, the design docs, the static
  pipeline, the ownership and inventory scripts, tests/security — the confidential-material check with its
  sentinel table, passed —, the preview, the family's, W3-F2's and W2-C2's unit files, the gated doors), and the
  preview's tests again on the status change, **297 passed**. `ruff check` and `ruff format --check` clean on the
  touched test.

## On http://127.0.0.1:8780 (checked after the restart, by request only — no browser on the owner's server)

- http://127.0.0.1:8780/fr/ · http://127.0.0.1:8780/ar/ · http://127.0.0.1:8780/__design-v5/ — the strip names
  `v54/w3-f1`; the index lists the family as passed, with its review
  (http://127.0.0.1:8780/__design-v5/decisioni/w3-f1/REVIEW.md); its 18 surfaces are v5 in `live_status.json`, and
  the index's 17 page rows of them read «V5 · council-passed» (the questionnaire's step is a state, reached by driving
  the questionnaire).
- **The doors** (fr; the same paths under `/ar/`): http://127.0.0.1:8780/fr/parcours/ ·
  http://127.0.0.1:8780/fr/entreprises/ · http://127.0.0.1:8780/fr/institutions/ ·
  http://127.0.0.1:8780/fr/universites-et-formation/
- **The pathways**: http://127.0.0.1:8780/fr/parcours/salaried_work/ · http://127.0.0.1:8780/fr/diplomes-et-titres/ ·
  http://127.0.0.1:8780/fr/formation/
- **The project pages**: http://127.0.0.1:8780/fr/forum/ · http://127.0.0.1:8780/fr/forum/inscription/ ·
  http://127.0.0.1:8780/fr/le-projet/ · http://127.0.0.1:8780/fr/projet-pilote/ · http://127.0.0.1:8780/fr/agami/ ·
  http://127.0.0.1:8780/fr/reseau/ · http://127.0.0.1:8780/fr/contact/ ·
  http://127.0.0.1:8780/fr/attention-aux-fraudes/
- **Orientation**: http://127.0.0.1:8780/fr/orientation/ · http://127.0.0.1:8780/fr/orientation/reprendre/
- «Ma situation» (console) through the preview's persona switch: http://127.0.0.1:8780/fr/espace-reserve/ma-situation/

## Not done

- **No reviewer read the budget and consolidation pass again** (V5.5: one review, then fix); its proofs — a
  148-capture comparison of every pixel and computed style, the deletions' class-by-class search, the performance
  sanity check — are the family's own (`NOTES.md` §26 – §35).
- **The full suite was not run** — the integration checkpoint's (V5.5). The targeted set ran on the branch and the
  post-merge checks on design-v5.
- **Frames for the doors** (the Image Art Director): RH-3 on /entreprises/ and /forum/ (and /le-projet/ on a phone)
  waits for curated, captioned frames; until then the entrance's end seat holds «la porta» or the page's own photograph.
- **Copy decisions (the owner's packet, B1)**: the door's primary within 560 px at 360 × 800 is not reached on
  /parcours/, /universites-et-formation/ in French and /entreprises/ (the locked leads run ten to twelve lines on a
  phone); /orientation/'s «Commencer» follows the prescribed lead and inset on a phone; the question headings of B1
  item 7 are proposed in `NOTES.md` §5 and §18, not written.
- **Handed to other families**: the chrome's current-door marking on /forum/ and /formation/ (review m8 → W2-C1 /
  W2-C2); the home's French lead on the Arabic page (m7's other half → W2-D's `pages.css`, through the steward); «la
  linea» to `_journey-passage.css`, the timeline (`components.css` §17, `components/timeline.html`) and «Ma
  situation»'s Stepper (still in `v5/_wizard.css`) → W3-D; «Ma situation»'s act as the phone's action bar → W3-E;
  `--hit-min`'s V4 44 px in `v5/aliases.css`, the orphan component templates (`hero.html`, `local_nav.html`,
  `timeline.html`, `cta_panel.html`) and `ecosystem.services.local_nav` → W4-D; the service pages' own trail and
  help line (W3-F2's `_servizio.css`, review m11's remainder) → W3-F2 / the steward, if a third surface draws the trail
  alone.
- **The design showcase** (`/_design/`, dev only) loads `main.css` alone, so its samples of the trail and the page
  header lose the legacy box and type `components.css` §9 and §10 gave them; the product's pages draw both through
  their sheets.
