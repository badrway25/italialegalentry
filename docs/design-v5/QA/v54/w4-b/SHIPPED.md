# W4-B shipped — 16 October 2026

**Motion audit — the Motion library leaves; every animation through motion.js's gate; a reduced-motion still
everywhere; nothing at load in the console but the entrance release.** Tag **`v54/w4-b`** (design-v5 `96bcbbd`, the
status commit, as for the earlier families); merge commit `844e11f`. The owner's preview on http://127.0.0.1:8780
serves it: v5-live checked out at the tag, 8780 restarted at 08:39 and verified by request (`verify_8780.log`:
33 requests, every one as expected, at 08:39; no traceback in the server log). Steward's merge, label `w4-b-merge`,
under `DESIGN_V5_MERGE_LOCK` from 07:32:08. Reviewed once and fixed (V5.5): `REVIEW.md` and `A11Y_PERF.md` were both SHIP_AFTER_FIXES with no P0 (the check's one major and every minor
of both fixed in the one fix pass, `NOTES.md` «Review fixes»); the steward's targeted run and the requests on 8780
checked it on the merged tree (`NOTES.md` «At the merge (the steward)»). The record: DL54-153 (the family's decisions)
and DL54-154 (the merge).

## What shipped

- **The Motion library is gone** — from every source, both package files (`motion` and with it `framer-motion`,
  `motion-dom`, `motion-utils`, `tslib`) and every bundle. Its last two callers moved to the platform: «Ma situation»'s
  question change runs on the Web Animations API through `motion.js`'s gate (`play()`: the same clocks, the token's
  curve, the arriving question's one-frame flash gone), and shell.js's `[data-reveal]` reveal — which no page used and
  which hid text until a script showed it — is deleted. **The home's script 51 249 → 24 138 B gzip** (9 → 7 script
  requests); every page type about 26.9 KB lighter with one request fewer (a module one entry alone imports is now
  inlined: `nav.js` into `shell.js`, `hero.js` into `home.js`). Plan §2.6's 45 KB holds on every page type again.
- **Text never waits for a reveal (K17)**: `components.css` §29 (`.reveal`, its stagger, its permanent `will-change`)
  and `main.js`'s `initReveal` and `initCounters` (a count-up outside the gate) deleted.
- **The console's rail folds at once (R10)**: its 200 ms transition of the rail's width and the page's padding re-laid
  the workspace on every frame and never reached 60 fps at CPU × 4; only transform and opacity animate.
- **The keyboard never animates (tier 0)**: the portico (Esc after a pointer's opening, the chevron, the architrave),
  the skip link's slide, the links' colour fade (the console bar's trail), and «Ma situation»'s question change — from
  the keyboard the new question is there in the key's own task with its focus ring. An interrupted question change (a
  return within the 120 ms fade, a Stepper jump back) no longer leaves the page with no question and the focus on
  `body`.
- **The curves back to their roles**: ten declarations on the superseded exit curve move to `--ease-enter` (the
  portico's pointer exit no longer holds near-full opacity for its first ~40 ms).
- **Forced colours**: the current page of the rail and of the phone bar wears its lit disc (and in the rail its word
  underlined), no longer the focus ring's outline at rest — so focusing it shows a ring (WCAG 2.4.7).
- **Held as before** (measured by the review): the hero, «Il varco», «Lume» and the overlays — the same animations, 0 px
  on every settled frame; under reduced motion every page a still; nothing at load in the console but the entrance
  release; 0 animations and 0 `will-change` at rest.
- **Shared CSS (V5.8)**: `main.css` 31 906 → **31 799 B** gzip on every page (−107), the console page types
  40 140 → **39 978 B** (−162); no page type grows.

## The merge

- **The order and the sync**: the orchestrator launched W4-B ahead of W4-A (the plan's §3.6 sequence put W4-A
  first) and asked for its merge first; W4-A, in flight with no commit yet, syncs with this one. design-v5 had moved
  from the branch's merge base `8ab5b89` to `5bf2f90` (the sec-f7 merge, W3-E and its merge, the private-root probe's
  test, the devops-2 merge: 91 commits); the steward's sync (`d707d32`) resolved the decision log — the family's entry
  is **DL54-153** on design-v5 (DL54-132 on the branch; its mentions in `NOTES.md` and `A11Y_PERF.md` follow,
  `7e20cbf`) —, DS 2026 §2's generated table (`regen_design_inventory.py --write`) and the dist trees (rebuilt from
  clean). No merged source imports the library or an export `motion.js` lost; no template, W3-E's included, draws a
  reveal.
- **Ownership** (`bac3e12`, `b113836`, on the branch): the two no-owner paths are W4-B's slices in the manifest
  (`scripts/build_frontend.mjs`'s `INLINED` list, `docs/design-v2/FRONTEND_DEPENDENCIES.md`'s `motion` row); the
  dependency's removal in `package.json` and `package-lock.json` — the plan's own step for the steward in this merge
  (§3.6 item 2) — is adopted as the steward's write, the files staying the steward's whole (the lock read: nothing
  else required the five packages). After it: 7 inside, 8 slice, 23 generated, 16 delegated and the three steward-only
  paths the steward writes itself (the manifest, the two package files), 0 outside; `--validate`: coherent,
  29 families, 738 entries.
- **The shared CSS gate (V5.8) passed**: `main.css` 31 906 → 31 799 B on every page, the console page types
  40 140 → 39 978 B, every page type lower; every ceiling lowered to the merged weight. **The script budget (§2.6)**:
  the home 51 249 → 24 138 B gzip, a public page 43 674 → 16 781, an entrance page 45 351 → 18 462, a console page
  46 060 → 19 168, «Ma situation» 47 282 → 20 537. The record: **DL54-154** (`dd61b21`), with the table of every page
  type before → after; DL54-152's missing index row added there.
- **Bundles** rebuilt from a clean dist in the branch (every bundle neither side conflicted on byte for byte the
  merge's) and in design-v5 after the merge (byte for byte the merged ones: no build commit).
  `scripts/regen_design_inventory.py`: current on both. The capture report is unchanged (W4-B changed motion only).
  `ruff check .` clean; `manage.py check`: no issue; `makemigrations --check`: no changes.
- **Tests** (lane `test_ile_v5_l8`, one pytest and one browser of the steward's at a time, no run crashed; V5.5:
  targeted, not the full suite; `C:/tmp/ile_v5_council/evidence/v54/w4-b/merge/tests_*.log`): non-browser — the merge
  brief's list with the family's static files, devops-2's static-caching test (the import graph W4-B's build writes)
  and the checker's and the inventory's tests — **846 passed**, 0 skipped, **1 failed**: the checker's pin on
  `package.json`'s ownership, broken by the steward's own first manifest entries and fixed (`b113836`; the file
  **57 passed**); browser (headless Chromium) — the family's motion file, the loader, the entrance, the overlays and
  their RTL files, the phone sheet, the journey, the console's shell and phone bar, `tests/i18n/test_rtl_browser.py` and
  the hero — **310 passed**, 0 skipped, 0 failed; on design-v5 after the merge **124 passed**; the preview's own tests
  and the checker's with the new status files **354 passed**.
- `live_status.json`: the family row w4-b — state v5, its review as the decision, the tag. No surface key changes: W4-B
  composes no page, and every surface it moved was already V5 at the tag of the family that composed it.
  `CHANGELOG_V54.md`: the entry first.

## On http://127.0.0.1:8780

All checked by request after the restart (`verify_8780.log`): 200, one h1 on every page, the removed stubs 404, no
Motion code in any bundle, no traceback.

- http://127.0.0.1:8780/__design-v5/ — the strip names `v54/w4-b`; the index http://127.0.0.1:8780/__design-v5/index/
  lists the family with its review (http://127.0.0.1:8780/__design-v5/decisioni/w4-b/REVIEW.md).
- The public pages — the home's lighter script, the portico still from the keyboard (Esc after a pointer's opening, the
  arrows), the skip link without its slide, the links without their fade from Tab: http://127.0.0.1:8780/fr/ and
  http://127.0.0.1:8780/ar/ (the hero's motion unchanged), a door http://127.0.0.1:8780/fr/entreprises/, the FAQ
  http://127.0.0.1:8780/fr/faq/, the login «Il varco» http://127.0.0.1:8780/fr/compte/login/ (its motion unchanged), the
  sign-up http://127.0.0.1:8780/fr/compte/signup/.
- Through the preview's persona switch («Personas» → «Entrer», no password) as «Personne avec dossier»
  (qa-doc-person): the dashboard http://127.0.0.1:8780/fr/espace-reserve/ (nothing at load but the entrance release;
  the rail folds at once; the trail's links from Tab without a fade) and «Ma situation»
  http://127.0.0.1:8780/fr/espace-reserve/ma-situation/ («Continuer» with the pointer: the 120 ms fade, then the
  200 ms arrival from 16 px; with Enter from the keyboard: the next question at once with its focus ring; «Continuer»
  then «Précédent» at once: one question, never none); the mirror under http://127.0.0.1:8780/ar/espace-reserve/ and
  http://127.0.0.1:8780/ar/espace-reserve/ma-situation/ (the arrival from the left).
- Reduced motion and forced colours: the system's settings (under reduced motion every page is a still; under forced
  colours the rail's current entry wears its lit disc and its word underlined, and the focus adds its ring).

## Not done

- **`node_modules`**: design-v5's still holds `motion`, `framer-motion`, `motion-dom`, `motion-utils` and `tslib` (no
  build imports them); this programme's standing rule allows no `npm ci` or `install`, so they leave at the next
  `npm ci`.
- **Measures not made at the merge**: no browser on 8780 (by rule); the steward measured no motion by hand — the
  family's review and its accessibility + performance check stand (`REVIEW.md`, `A11Y_PERF.md`, the fix pass in
  `NOTES.md`); nobody has watched the motion at speed; Firefox, WebKit, a real phone and a screen reader were never run
  (W4-C's).
- **Handed on** (DL54-154 item 9; none of it holds the merge): **W4-D** — the legacy sweep (`components/hero.html`, the
  `.entrance` rules of `components.css`, the `--duration-reveal` / `--reveal-distance` / `--reveal-index` tokens of
  `_legacy-tokens.css`, `cms_nav.py`'s `hero_lines`, `data-reveal-once` on `orientation/result.html`, the dead guard
  `html.js .page-home .reveal` of `pages.css`); **W1-A** — `v5/tokens.css` l. 468 still calls the springs «CSS twins
  of motion.js»; **W3-A** — `console.js`'s `is-ready` hook and its header line on the rail's width; **W4-A** (in flight)
  — syncs with this merge; **W4-C** — the motion seen at speed, Firefox and WebKit.
- **The full suite** was not run (V5.5: the integration checkpoint runs it). Nothing was pushed to GitHub; nothing was
  deployed.
