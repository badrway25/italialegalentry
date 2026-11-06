# V5.22 lane S — QA round 2 (label `v522-s-qa2`)

Senior design-engineering review of lane S's round 1 (label `v522-s-improve1`): Section System V2 foundation, Icon
Treatment V2, Motion Density V2. 1 November 2026, 16:45–18:30.

- **Under review:** branch `v522-s` at `d9551f4` (worktree `C:/tmp/ile_wt/v522-s`). That is the round-1 work
  (`8be8d22` + `82f9028`) on the merge `d4c9d8a` (lane M), plus the merge of design-v5 `d8552b9`, which brings four
  steward documents only.
- **Baseline:** 8780 serves design-v5 `d8552b9` from `C:/tmp/ile_wt/v5-live` (restarted 16:08:46 today). Between
  `fdd6e34` and `d8552b9`, templates, CSS and JS differ only by the imagery tag and the dev specimens. The one visible
  change is the campus frame on /xx/universites-et-formation/. Every «before» below is therefore `fdd6e34`'s look on
  the surfaces lane S touches. I checked it against the `fdd6e34` audit captures and against my round-1 «before» captures.
- **Lane server:** 8783 from the worktree (dev settings, `ile_v5_l3`, `ILE_DESIGN_PREVIEW=1`,
  `ILE_REFERENCE_DATE=2026-10-03`, `--noreload`). The WhatsApp number comes from the worktree's own git-ignored `.env`.
  I compared its line with `v5-live`'s by hash only, and it was never printed. The server is stopped at the end.
- **Browser:** headed Chromium (chromium-1234, Playwright), lock slot A only. Sessions: 16:52–17:09, 17:11–17:17,
  17:18–17:29, 17:36–17:49, 17:53–17:59, 18:01–18:03, 18:11–18:17 (the lane's browser tests, headless by their own
  design), 18:17–18:21 (§7.3) and 18:23–18:24 (hover). Each was 25 minutes or less and released. Slot B was never
  touched.
- **Tests:** targeted pytest on `test_ile_v5_l3`, one run at a time (§7).
- **Read in full first:** the V5.22 directive, SECTION_SYSTEM_V2 §0–§12 (incl. §11.1), my round-1 report, the
  builder's NOTES §1–§10, and the diff `d4c9d8a..82f9028` (47 files) plus the merge.
- **Scripts and raw data:** `C:/tmp/ile_v5_council/.work/v522-s-qa2/`, with the data copied to `qa2_data/` here. Every
  capture in this folder that starts with `qa2_` belongs to this review.

---

## 0. Verdict

**PASS (round 2). 0 major, 6 minor, 3 nits.** Lane S can merge first, as §9.7's order wants.

Tests: 716 targeted and browser tests passed, 0 failed, 0 skipped (§7).

**The three majors of round 1 are fixed.** I re-measured each one with my own probes, not the builder's tests:

- **M1, axe.** 0 violations of any impact in 276 runs:
  - 192 fixture runs (24 fixtures × fr/ar × 1440/1024/768/390);
  - 24 runs after interaction (a tab or node chosen, a disclosure opened, resized 1440 → 390 → 1440);
  - 60 real-page runs.

  While a list is a tablist it owns `tab`s only, through `li[role=none]`. It becomes a list of `li` again on a phone.
- **M2, «la linea V2».** Every connector stands drawn at rest, in view at load and from the keyboard: 48 probes at the
  8 widths, fr/ar, with scale 1, no clip, no animation and no scroll-linked timeline.
  - At 48–80 rem the rows of four are joined by a real carriage return.
  - The origin seal stands on the marks' row, and its sill is the route's first stretch.
  - Below the fold the route draws once, then stands whole at 1440/1024/768/390, with nothing held.
- **M3, the head's call.** Measured at 13 sizes × 11 heads × fr/ar (plus it/en at four sizes), the call never leaves the
  first screen:
  - Entreprises 1280 × 720: 695 → 699 / 720;
  - Parcours 1024 × 768: 744 → 748 / 768.

  From 48 rem the title moves +2 to +4 px. On a phone's door head it moves +12 px, with the call still 34 px or more
  inside the first screen (a recorded deviation, which I accept). Short phones keep a typographic folio, and their
  title does not move.
  - The seat is at least 8 px below the band's top and the sill at least 12 px above the title, in all 224 seal renders.
  - Forced colours draw the sill and the arch.
  - Parcours' seal, line, rings and arrival share one axis in 4 languages at 1440/1280/1024/768.

**Of the 13 minors, 11 are fixed.** m10 (EN-3's mark) is the Director's. m13's 8782 measurement is the Performance
Lead's. My proxy in §7.3 shows no LCP or CLS regression from lane S's deltas.

**What else holds:**
- The 24 fixtures render cleanly in 768 renders (8 widths × fr/it/en/ar): 0 overflow, 0 text cut, 0 text collisions,
  0 console errors.
- Reduced motion (96 stills) and no-JS (96) are complete.
- The home is pixel-identical (fr/ar × 1440/390).
- CLS is 0 on the seven seal heads.
- `main.css` is byte-identical, at 32 718 B.
- Every §7 budget holds, and the build reproduces byte for byte from `HEAD`.
- No preserved family, locked string or legal notice is touched.

**What is still below a premium bar, all minor:**
- **n1.** On Arabic pages, French runs are end-aligned in B cards, F panels, E tiles and French titles. That contradicts
  §1 rule 6 and §2 B's RTL line.
- **n2.** On phones «il mosaico» is a stack of tall white cards.
- **n3.** The T1 seat's face departs from §4.3 and reads heavy.
- **n4.** «la linea V2» hyphenates a locked capital word at 1440.
- **n5.** F's CSS exceeds its §2 contract.
- **n6.** The 8782 measurement is still owed, and `fronte.css` has 3 B of headroom.

n1 and n2 should be settled before P1 and P2 compose those patterns: the partials and sheets are S's (§9.7), so the
composing lanes cannot fix them.

---

## 1. What was checked

| Area | What | Count |
|---|---|---|
| Fixtures, layout | 24 fixtures × 8 widths (1440/1280/1024/768/430/390/375/360) × fr, ar, it, en. Probes: document overflow; text outside the viewport unless in its own scroller; text-range collisions between unrelated elements; targets under 24 px; console errors. Section captures at 1440/768/390/360 in fr and ar | 768 renders, 192 shots |
| Fixtures, reduced motion | `reduced_motion=reduce`, the section a screen below the fold, scrolled in. Probes: state written, animations running, strokes held, scales, grey images | 96 |
| Fixtures, no-JS | `java_script_enabled=False`. Every heading, paragraph, item, link and summary is visible and in reading order | 96 |
| Fixtures, keyboard | A 16-press Tab trail in fr/ar at 1440/390. Plus the passage's plates, what runs on focus, and the focus ring of the stretched-link plates | 92 trails + 34 |
| Fixtures, motion | Below the fold, by `scrollIntoView` and by real wheel scrolling: `wait` → `in` → nothing held 2.6 s later; no text masked. «La linea» entrance frames at 4 widths | 23 + 12 + 2 |
| Fixtures, axe | axe-core (`.work/w1-0-before/axe`), CSP bypassed in the check only, scoped to the section | 192 + 24 after interaction |
| «La linea V2» | Every connector: computed scale, clip and driving animations, box and borders; at rest, from the keyboard, after the entrance; carriage return pixel-checked | 48 + 12 |
| Real heads | 7 seal heads + 4 typographic. Before/after at 8 widths in fr/ar, after in it/en; geometry, overlaps, the call at 13 sizes; Parcours' axis; forced colours; the draw at load; CLS | 528 + 748 + 32 + 16 + 3 + 56 loads |
| Hover, real mouse | 9 fixtures × fr/ar at 1440: the responses that run | 18 + M21 |
| Real pages, other | M22 band (4 widths), M21 under the mouse, login eyebrow, home full-page stills pixel-diffed, axe, keyboard trail, short phones | — |
| Code | The 47-file diff of round 1 and the merge. The updated and new tests against the V5.20 strict rule. Preserved families, §9.7 ownership, LF, build reproducibility | — |
| Tests | 17 targeted non-browser modules + the lane's two browser modules (§7) | see §7 |

---

## 2. The round-1 findings, one by one

| Round 1 | Status | What I verified |
|---|---|---|
| **M1** tablist owns `li` (axe critical/serious) | **Fixed** | 192 fixture axe runs at 4 widths in fr/ar: 0 violations (`qa2_data/fx_axe.json`). After interaction (Arrow keys on tabs and nodes, a disclosure opened) and after resizing 1440 → 390 → 1440: 0 (`qa2_data/states.json`). Ownership after each step: tablist → children `role=none`, 8/5/6 `[role=tab]`, 0 `.indice__apri`; list → `LI`, 8/5 buttons with `aria-expanded`. The map keeps its tablist after a resize, by design, and stays at axe 0. Code: `indice.js` `wrap()` moves the heading's words into the button only in disclosure mode; `mappa.js` sets `role=none` on the items |
| **M2a** connectors scroll-linked at rest | **Fixed** | 48 probes (8 widths × linea/linea-how × fr/ar, plus keyboard at 4 widths): every connector has `scale` 1, `clip-path: none`, 0 animations and 0 scroll timelines (`qa2_data/linea_rest.json`). M5 is qualified `:not(.linea--large)`. Shots: `qa2_linea_rest_*` |
| **M2b** origin seal misaligned | **Fixed** | «01» stands over the seat. The seat's foot sits on the marks' row, and its sill is drawn in the route's ink and weight and runs into segment 1 (`qa2_zoom_linea_origin_fr_1440.png`, `_ar_1440.png`). Below 48 rem the route leaves the sill (`qa2_linea_rest_linea-fr_390.png`) |
| **M2c** no carriage return | **Fixed** | At 768, 1024 and 1280 (cols 4), the route turns down at row 1's end, runs back in the rows' gap and drops at the reading edge into station 5. It mirrors in Arabic (`qa2_linea_rest_linea-fr_1024.png`, `qa2_linea_rest_linea-ar_768.png`). At pixel level it is joined at both corners (`qa2_zoom_linea_return_*`). It ends 4 px before the mark, as every segment does. Two nits: n7, n8 |
| **M3** call below the first screen | **Fixed** | 374 rows × before/after (`qa2_data/cta.json`): 0 «leaves the first screen», 0 «below before and after». Smallest margins: 375 × 667 Parcours 5 px (unchanged, typographic folio); 1024 × 768 Parcours 20 px; 1280 × 720 Entreprises 21 px. Title shift: +2/+4 from 48 rem, +12 on the phones' door heads (+4 on the other heads), 0 on short phones; −8 to −20 on the typographic folios. Seal geometry over 224 renders: band top → seat ≥ 8 px, sill → title ≥ 12 px. Forced colours: arch border and sill in CanvasText (`qa2_sheet_forced_1440.png`). Parcours axis: seal = line = rings = arrival to 0.1 px in fr/ar/it/en at 4 widths, and the line starts exactly at the sill (`qa2_data/axis.json`) |
| m1 keyboard animates | **Fixed** | No time-based animation runs on keyboard focus in 92 fixture trails, except the global link `color` transition (120 ms, `main.css`, preserved; not motion). The seal's draw, the linea and flow lights, the needle, the tile threshold and the `select` frames are all gated `:not([data-input="key"])` or `transition: none` |
| m2 J and flow without fixtures | **Fixed** | `passaggio` and `flusso` are fixtures. The passage's arch strokes draw on first entry at 390 (`sez-stroke`, done by 600 ms). The flow draws one curve through the nodes, right to left in Arabic (`qa2_fx_flusso-*`) |
| m3 Arabic fixtures without `lang` | **Fixed** | French samples carry `lang="fr"`, and final punctuation stays at the run's end (`qa2_zoom_tracciato_ar_390_cards.png`) |
| m4 folio seal faint | **Fixed, with a new deviation** | The edge is a 62 % border, readable at 1×, and forced colours keep the arch and sill. The face is now a grey vault, not §4.3's face: n3 |
| m5 RTL labels of «la linea» | **Recorded, then extended**: n1 | — |
| m6 explorer draws one concept twice | **Fixed** | The answer plate draws its `ile-domande` seal only (`qa2_sheet_fx_explorer_racconto_1440.png`) |
| m7 frameless mosaico and tracciato | **Fixed on desktop**; phones: n2 | Framed bento: the photo is the lead's ground, its words on a plate. The wide tile for frameless leads. The tracciato's rails and family frames (`select`, black and white at rest). All three frames load when scrolled to (`qa2_data/lazy.json`); the blank third frame in the long phone shots is the shot's lazy-load timing, not a defect |
| m8 K light sweep untriggered | **Fixed** | `strato` and `approdo` run `sez-sweep` once as they enter and leave nothing (`qa2_data/fx_motion.json`) |
| m9 `test_chapter_marks` | **Fixed** | `HOME_EXPECTED = {"/fr/": {"compass", "signpost"}}` restored and asserted, which is stronger |
| m10 EN-3 briefcase | **Director's** | Recorded in NOTES §10.6 |
| m11 panorama strip on phones | **Fixed** | The plate stands under the strip (`qa2_fx_panorama-band-fr_390.png`) |
| m12 racconto stroke scales | **Fixed** | Non-scaling hairline (`qa2_sheet_fx_explorer_racconto_1440.png`) |
| m13 LCP/CLS/INP on 8782; `fronte.css` headroom | **Carried**: n6 | Proxy in §7.3 |

---

## 3. §9.9 acceptance, item by item

| # | Item | Result | Evidence |
|---|---|---|---|
| 1 | No page lower on any §26 dimension than at `fdd6e34` | **PASS.** Lane S recomposes no body. The heads are refined: the seal, the route's one axis, the typographic folios. The home is pixel-identical. See §5 | §5, `qa2_home_*` |
| 2a | 8 widths, fr/it/en/ar: rhythm, crops, no overflow, density, icons, RTL | **PASS, with minors.** 768 fixture renders and 528 head renders are clean. RTL mirrors everywhere. The French-run alignment deviates (n1). The mosaico is long on phones (n2) | `qa2_data/fx_measure_*.json`, `heads.json` |
| 2b | Reduced motion = the designed still | **PASS** (96/96; the real seals stand drawn) | `qa2_data/fx_rm.json` |
| 2c | Keyboard: reachable, visible, not obscured, no animation | **PASS.** Tabs and map run on Arrows/Home/End/Escape (the builder's browser test, re-run in §7). The plates show the 1.6 px ring by `:focus-within`. Nothing time-based runs on focus | `qa2_data/fx_keys.json`, `qa2_sheet_focus.png` |
| 2d | No-JS complete, in reading order | **PASS** (96/96) | `qa2_data/fx_nojs.json` |
| 3 | WCAG 2.2 AA, axe 0 serious/critical | **PASS.** 0 violations of any impact in 276 runs | `fx_axe.json`, `states.json`, `axe_pages.json` |
| 4 | Locked copy byte-identical; notices visible; both G3 states | **PASS.** `test_prescribed_fragments`, `test_locked_split` and the protection's `textContent` test are green (§7). Lane S prints no new string | §7 |
| 5 | The Word/PDF test fails for every V2 section | **PASS for the library.** Each pattern carries at least two of: drawing, signature motion, state, depth, spatial structure. The weakest is the phone mosaico (n2) | §4 |
| 6 | §7 budgets; LCP/CLS/INP on 8782 | **§7 PASS** (§6). **8782 not measured**: it is the Performance Lead's (n6). Proxy 8780 vs 8783: see §7.3 | §6, §7.3 |
| 7 | V5.20 gate | **Targeted PASS** (§7). The full suite is the integrated tree's gate | §7 |
| 8 | Preview label | After the merge (the steward's) | — |
| — | Hover, with a real mouse (`qa2_data/hover.json`, `qa2_hover_*`) | **PASS.** Each response is the spec's:<br>• mosaico: pre-painted layer, 2 px lift, glyph 2 px, threshold 40 → 100 %;<br>• doors: `flex-grow` 1 → 1.25;<br>• linea: one `sez-flash` along the route plus the seal's light;<br>• flow: one `sez-luce` along the curve;<br>• map: preview, panel cross, spoke draw, the highlight's glide;<br>• route board: the card's frame goes to colour and its lane rule lights;<br>• boussole: the needle turns.<br>No shadow animates except the T2a ring (noted in §7.4). M21 on Le projet's link rows: oro at 16 % → the teal accent at 10 % | — |
| — | T1 folio seals, motion vocabulary, M22 live on real pages | **PASS.** The seven heads show their seal in 4 languages at 8 widths. Probed on Parcours, Entreprises and Fraudes, the seal draws at load (`sez-stroke` then `sez-tone`, finished by 2.1 s, `qa2_draw_*`). It stands drawn under reduced motion, and the keyboard snaps it to its end state (the draw is gated `:not([data-input="key"])`). M22: the Entreprises band runs `drift` (−3 % → +3 %) at 1440/1024/768 instead of `fdd6e34`'s `reveal-mask` + `reveal-zoom`, which it keeps at 390 | `qa2_data/draw.json`, `m22.json` |

---

## 4. New findings (round 2)

### Major

None.

### Minor

**n1 · RTL: French runs end-aligned in B cards, F panels, E tiles and French section titles, against §1 rule 6 and
§2 B.**

- **Where:** `static/css/v5/_sezioni.css`:
  ```css
  [dir="rtl"] .sez :is(.tracciato__carta, .flusso__lastra, .mosaico__tessera) [lang="fr"]:not(html),
  [dir="rtl"] .sez .testa__title[lang="fr"] {
    text-align: end;
  }
  ```
  The static test `test_a_french_run_beside_a_marker_hangs_from_its_edge_on_an_arabic_page` asserts this rule.
- **What:**
  - Round 1's m5 concerned «la linea»'s two-word station labels (W3-F1's precedent), and I accepted recording it there.
  - The builder extended it to whole paragraphs. A French description in an Arabic card now reads ragged-left, every
    line starting at a different x (`qa2_zoom_tracciato_ar_390_cards.png`).
  - §2 B's RTL line says «a French card is its own LTR box at its own start». §1 rule 6 says «aligned to its own start
    … a deliberate quotation plate, never a misaligned paragraph».
  - One Arabic page would also carry two alignments for French runs:
    - start, in K plates (`qa2_fx_strato-ar_1440.png`), the terminal plates, the passage and free paragraphs;
    - end, in B, F, E and titles.
  - Within one route-board lane at 390 Arabic, the lane's name «FAMILLE» stands at the far left, at its own start, while
    the card under it hangs its French from the right (`qa2_lazy_tracciato_tracciato-ar_390.png`).
  - The test's docstring cites §1 rule 6 for the opposite of what it says.
- **Fix:**
  - Either keep `text-align: end` only for one-line labels beside a marker (station labels, card titles that fit one
    line) and give multi-line runs (`.tracciato__riga`, `.flusso__testo`, `.mosaico__riga`) their own start, in their
    own LTR box hanging from the reading edge;
  - or obtain the Director's explicit amendment of §1.6 and §2 B before H, P1 and P2 compose B, F and E in Arabic.
  - Correct the test's citation either way.

**n2 · «Il mosaico» below 48 rem is a stack of tall white cards.**

- **Where:** `static/css/v5/_sec-mosaico.css`.
- **What:**
  - At 390 the grid fixture is 1 396 px (1.65 screens), against 698 at 1440. Each compact tile is about 175 px: a 48 px
    glyph tile, then the title, the line and the threshold rule (`qa2_fx_mosaico-fr_390.png`). The frameless
    `mosaico-ampio` is 1 180 px.
  - On a phone this is the «online report with cards» image the V5.22 rejection names. §2 E's «< 48 rem: one column,
    tiles ≥ 64 px tall» asks for compact tiles.
  - P1 (PA-3, F2, D3) and P2 (G2) compose it and cannot edit the sheet (§9.7).
- **Fix:** below 48 rem, set the compact tiles as rows: glyph tile at the inline start, title and line beside it, about
  72–88 px each. Keep the lead large, with its frame or the wide tile. Expect about 650–750 px.
- **Related, for P1, not S:** the route board at 390 is 2 880 px (3.4 screens) for eight stations. The register it
  replaces is 2.0 screens at 390 (AUDIT_pages1 PA-1). The sticky chip bar is in place, as §2 B asks.

**n3 · The T1 seat's face departs from §4.3 and reads heavy.**

- **Where:** `static/css/v5/_sigillo.css`:
  ```css
  --sg-face: linear-gradient(var(--line-rhythm), var(--surface-raised) 85%);
  ```
  §4.3 prescribes `linear-gradient(180deg, var(--surface-raised), var(--surface-sheet))`.
- **What:**
  - With the mark standing on the sill (32 in 68), the upper half of every seat is now a grey dome.
  - At 1× on the heads, and in rows (`qa2_fx_sigillo-fr_1440.png`, `qa2_zoom_seals_1440.png`, the 390 heads in
    `qa2_sheet_heads_390_fr.png`), the seat weighs more than its mark. It edges towards the «headstone» the sill was
    meant to prevent (§4.3).
  - Round 1's faintness is cured by the 62 % border alone.
- **Fix:** return to §4.3's face and keep the border. Or record the deviation with the Director, with captures of both.

**n4 · «La linea V2» hyphenates locked capitals at ≥ 80 rem.**

- **Where:** `static/css/v5/_linea-v2.css`, `.linea__label--caps { hyphens: auto }`.
- **What:**
  - With eight stations across, a column is 129–134 px at 1280–1440. The pilot sequence's «ACCOMPAGNEMENT» needs about
    155 px at 15 px / 0.05 em, so it renders «ACCOMPAGNE-» / «MENT» (`qa2_linea_rest_linea-fr_1440.png`). The same
    happens at 768 in Arabic (`qa2_linea_rest_linea-ar_768.png`).
  - `textContent` is unchanged, but on PP-1, the owner's first width, a locked word is visibly broken.
- **Fix:** `hyphens: manual` on caps labels, and at ≥ 80 rem let a caps label use its column gap (24 px), or tighten
  the tracking to 0.02 em there. Check «ACCOMPAGNEMENT» and «PROCÉDURES RÉGULIÈRES» at 1280 afterwards.

**n5 · F's CSS exceeds its §2 contract.**

- **What:**
  - §2 F gives the pattern `_journey-passage.css (+ ≤ 1.2 KB gzip)`.
  - The build has `_linea-v2.css` at +1 226 B (ceiling 1 229) and the new `_sec-flusso.css` at 868 B (a self-set ceiling
    of 922 B). That is 2 094 B for F.
  - The family sheets and page totals hold (§7.1), so nothing ships over a §7 ceiling.
  - The 922 B ceiling, though, was set by the lane alone.
- **Fix:** record the measured variant's ceiling with the Director (ratify 922 B), or fold.

**n6 · Carried m13.**

- **What:**
  - LCP, CLS and INP of S's real-page deltas on 8782 are not measured. Switching 8782 belongs to the Performance Lead
    under the lock (SERVERS.md); the request is in NOTES §10.6.
  - The deltas are: `fronte.css` +633 B, `reveal.css` +1 170 B, `rise.js` +454 B.
  - My proxy (§7.3) shows no LCP regression beyond noise and CLS at 0.
  - `fronte.css` is at 6 141 / 6 144 B. The next seal-head fix will need room, so S-close should ratchet it or find
    bytes first.
- **Fix:** the Performance Lead measures on 8782 before the integrated V5.20 gate.

### Nits

- **n7 · The carriage return's choreography.**
  - Mid-entrance (about 450 ms at 768/1024), the return's run under row 1 appears before the route reaches the turn.
    The `--capo` box opens with one mask, so its top and bottom borders reveal together (`qa2_sheet_linea_enter_768.png`).
  - At rest it is perfect.
  - Fix: delay the box's bottom edge by one segment, or draw it as a separate pseudo-element.
- **n8 · A 1 px seam in the return's drop.** Where `.linea__num::after` meets `.linea__segno::after` (1024, fr) there is
  a 1 px gap (`qa2_zoom_linea_return_corner_fr_1024.png`). It is invisible at 1×.
- **n9 · `ruff format --check`** would reformat `sezioni_fixtures.py`, `test_sezioni_v522_s.py`,
  `test_sezioni_browser_v522_s.py` and the new `test_seal_heads_browser_v522_s.py`. CI lints with `ruff check` only, and
  that is clean. Other lanes format their changed files (DECISION_LOG_V54), so this lane should too.

### Accepted, recorded deviations

- The phones' door heads: the title is +12 px, and the call stays 34 px or more inside the first screen.
- Short phones (≤ 760 px tall): a typographic folio, the title unchanged. At 375 × 667 the head loses its disc and
  shows no seal; that is coherent with the four typographic heads.
- The flow's ResizeObserver stays connected until `pagehide`. Re-measuring on resize is its job.

---

## 5. Scores (§26; 1–5, 3 = clean but editorial or static)

**Pages lane S visibly changes, at 1440 and 390, in fr and ar.** The bodies are unchanged, so the audits' numbers stand.
I checked the heads, M22, M21, the login key and the home pixel diff. **No dimension drops.**

| Page | Comp. | Motion | Imagery | Interaction | Institutional | Coherence | Note |
|---|---|---|---|---|---|---|---|
| Parcours | 3 | 2.5 | 2.5 | 3 | 3.5 | 3.5 | One axis for seal, line and rings; the seal on phones; short phones typographic |
| Pathway sheet | 2 | 2 | 1.5 | 2 | 3.5 | 3.5 | Seal folio; body unchanged |
| Entreprises | 3.5 | 3 | 3.5 | 3.5 | 4 | 3.5 | M22 drift; the call at 699/720 (1280 × 720) |
| Institutions | 3 | 3 | 3.5 | 2.5 | 3.5 | 3.5 | Seal folio |
| Universités et formation | 2.5 | 2.5 | 3.5 | 2 | 3.5 | 4 | `ile-sapere` |
| Formation | 3 | 3 | 3.5 | 2 | 3.5 | 4 | Seal folio |
| Attention aux fraudes | 3 | 2.5 | 2 | 2 | 4 | 4 | `ile-scudo` |
| Diplômes et titres | 2 | 2.5 | 3 | 2 | 3.5 | 4 | Typographic folio |
| Contact | 2.5 | 2.5 | 3 | 3 | 3.5 | 4 | Typographic folio; channels unchanged |
| Réseau | 2.5 | 2 | 2.5 | 2 | 3.5 | 3 | Typographic folio |
| AGAMI | 2 | 2 | 2 | 1.5 | 3 | 3 | Typographic folio |
| FAQ | 3 | 3 | 2 | 3.5 | 3.5 | 4 | — |
| Le projet | 2.5 | 2 | 2.5 | 2 | 3.5 | 3.5 | M21 accent |
| Home | 2.5 | 2.5 | 2.5 | 2 | 3.5 | 3 (ar 2.5) | Pixel-identical (H's) |

**The composition library on its 24 fixtures** (what H, P1 and P2 will compose; the builder self-scored 4 across):

| | Comp. | Motion | Imagery | Interaction | Institutional | Coherence |
|---|---|---|---|---|---|---|
| ≥ 48 rem | 4 | 4 | 3.5 | 4 | 4 | 3.5 |
| < 48 rem | 3.5 | 4 | 3.5 | 4 | 4 | 3.5 |

- **Composition, 4 / 3.5.**
  - The framed bento: the photograph as the lead's ground.
  - «Il flusso»'s panels hung on one measured curve.
  - The route board's rails with their family frames.
  - «La linea V2» with its seal origin and carriage return.
  - These read as an institutional product, not a report, at ≥ 48 rem.
  - On phones the mosaico and the doors stack as tall cards (n2).
- **Motion, 4.** One timing language with distinct verbs per pattern: line draw, mask, stroke, sweep, node settle,
  glide, widening and drift. Nothing is held, and the stills are designed.
- **Imagery, 3.5.** Frames are now in E, B, D and A. The T1 marks are small and their seat heavy (n3).
- **Interaction, 4.** Tabs, map, explorer and disclosure run at axe 0 with the full key set. The route board has native
  lane selection. Doors and flow light on hover or focus, and the passage snaps with Tab.
- **Coherence, 3.5.** Two alignments for French runs on Arabic pages (n1); the seat's face off-spec (n3).

---

## 6. Budgets (gzip -9 on the branch's dist; `fdd6e34` and round 1's `4c738be` in brackets)

| File | Measured | Ceiling | |
|---|---|---|---|
| `main.css` | 32 718 (32 718 · 32 718), byte-identical | 32 718 | PASS |
| `core/reveal.css` | 3 549 (2 379 · 3 532) | 6 144 | PASS |
| `pages/css/fronte.css` | 6 141 (5 508 · 6 138) | 6 144 | PASS, 3 B left (n6) |
| `pages.css` · `interior.css` · `ecosystem.css` · `pathways.css` | 4 732 · 4 148 · 5 421 · 5 577 | 12 288 · 11 264 · 11 264 · 11 264 | PASS |
| `hero.css` · `lettura.css` · `forum.css` · `glyph.css` · `portico.css` | unchanged | — | — |
| `accounts/entrance.css` | 4 845 (4 838) | existing guards | PASS |
| `rise.js` | 1 327 (873 · 1 326) | 1 536 | PASS |
| Chunks: indice · mappa · flow · spia · racconto | 1 088 · 901 · 605 · 577 · 408 | 1 536 · 1 536 · 1 331 · 1 024 · 922 | PASS |
| `img/icons-marks.svg` | 8 439 raw | 16 384 raw | PASS |
| Pattern partials (lane's own ceilings, `test_sezioni_v522_s`) | in the test (§7) | `_sec-flusso.css` 922: n5 | PASS |

**The build reproduces byte for byte.** I used `git archive HEAD` into a scratch folder, with `npm run build` on the
installed esbuild 0.28.2. `static/css/dist` and `static/js/dist` came out identical to the committed files.

---

## 7. Tests, code and performance

### 7.1 Targeted tests (`test_ile_v5_l3`, one run at a time)

**676 passed** (7 browser cases deselected) in 15 min 58 s, 17:52–18:09 (`qa2_data/pytest_targeted.log`). The 17
modules:

- `test_sezioni_v522_s`, `test_locked_split`, `test_icons`, `test_chapter_marks`, `test_motion_v512_a_w2`;
- `test_interior_w3_f1`, `test_frontispiece_v515_c` (per-sheet and per-page ceilings), `test_css_tokens_exist`;
- `test_design_docs`, `test_journey_w3_d`, `test_css_bundle_is_current`, `apps/pages/tests/test_home`;
- `test_prescribed_fragments`, `test_static_pipeline`, `apps/ecosystem/tests/test_compliance`;
- `test_rm_flag_parity` (untouched, as §2.0 requires), `test_forms_v515_b` (the questionnaire's sheet that imports the
  passage).

The 7 deselected browser cases of the same modules ran under the lock afterwards: **7 passed** (motion and forms,
18:16–18:17).

### 7.2 The lane's browser modules

`test_sezioni_browser_v522_s.py` and `test_seal_heads_browser_v522_s.py`, under lock slot A (18:11–18:16): **33 passed**
in 5 min 04 s (`qa2_data/pytest_browser.log`).

Their claims match my independent probes: the ARIA ownership, «la linea» at rest, the flow's curve, the passage's Tab,
the band's light, the heads' call and axis.

**In all: 716 passed, 0 failed, 0 skipped, no assertion loosened.**

**Lint and line endings on the diff:**
- `ruff check` on the five changed Python files: all checks passed. CI's lint step is `ruff check .`
  (`.github/workflows`).
- The 35 changed non-dist files are LF, with 0 CR bytes.
- `ruff format --check` would reformat the lane's four own test modules (n9). Three of them were already unformatted
  at round 0. `test_chapter_marks.py` stays formatted.

### 7.3 Performance proxy (m13 / n6)

8782 is switched only by the Performance Lead. I therefore compared the two dev servers that differ by lane S's changes
alone:

- 8780: design-v5 `d8552b9`;
- 8783: `v522-s` `d9551f4`.

Both are Django `runserver`, uncompressed, cache disabled. Conditions: slow 4G (150 ms RTT, 1.6 Mbit/s down, 750 kbit/s
up), CPU × 4, 390 × 844 at DPR 2, headed, A/B interleaved, n = 5 per page and side (`qa2_data/perf_proxy.json`).

| Page | LCP median before → after | Δ | Sample spread | CLS max before → after |
|---|---|---|---|---|
| fr/entreprises/ | 3 216 → 3 304 ms | +88 | 640 / 212 | 0 → 0 |
| fr/parcours/ | 2 992 → 3 048 ms | +56 | 96 / 144 | 0 → 0 |
| ar/formation/ | 3 300 → 3 456 ms | +156 | 180 / 304 | 0 → 0 |
| fr/attention-aux-fraudes/ | 2 928 → 2 992 ms | +64 | 200 / 116 | 0 → 0 |

**Reading:**
- The absolute values are the uncompressed dev server's and are not comparable with §5.3. The «before» is above 2.5 s
  too.
- The delta is consistently small and positive. It matches the extra render-blocking bytes, which uncompressed are
  about 13 KB: `reveal.css` +7 444 B raw, `fronte.css` +2 495, the family sheet +1 995 (`_photo.css`'s panorama and
  `select` rules, unused until a page composes D), `rise.js` +1 372. That is about 65 ms at 1.6 Mbit/s.
- On the compressed twin the same additions are about 3.3 KB gzip, or 15–20 ms.
- CLS stays 0, and the seven seal heads also measure CLS 0 at load at 1440 and 390 in fr and ar
  (`qa2_data/cls.json`).
- **So lane S's real-page deltas add only byte cost and no layout cost.** The 8782 measurement (n6) has to confirm that
  pages close to 2.5 s keep their margin.

### 7.4 Code

- **Round 1's diff (47 files).** Every source file is lane S's under §9.7. The six family dists change only because
  their entries import S's partials.
- **Preserved families are untouched:** header, menus, Lume, forms, `base.html`, `tokens.css`, `main.css`,
  `_portico.css`, `nav.js`, `shell.js`. No new npm package, no `!important`, no literal colour.
- **Motion.** The new keyframes animate compositor properties only: `stroke-dashoffset`, `clip-path`, `scale`,
  `opacity`. The flow's light and the linea's light are the accent's (§4.5: no gold added by hover). A paint-only
  `box-shadow` transition on the T2a disc's ring (200 ms) predates round 1, and §2 E's door `flex-grow` is the
  Director's.
- **Tests under the V5.20 strict rule.**
  - `test_chapter_marks.py` is stronger (the home's expectation restored).
  - `test_sezioni_v522_s.py` gains a flow-wrapper check, the RTL rule check (whose citation is wrong: n1) and a
    `_sec-flusso.css` ceiling.
  - `test_seal_heads_browser_v522_s.py` and 10 browser tests are new.
  - No assertion was loosened, no skip added, no timeout raised.
- `indice.js`, `mappa.js` and `flow.js` are clean: no scroll listener, one media listener, ResizeObserver until
  `pagehide`.

---

## 8. Evidence index (this folder)

- **«La linea V2»:**
  - `qa2_linea_rest_<fixture>-<lang>_<w>.png`;
  - `qa2_zoom_linea_origin_{fr,ar}_1440.png`;
  - `qa2_zoom_linea_return_{left,right}_fr_1024.png`, `qa2_zoom_linea_return_corner_fr_1024.png`;
  - `qa2_linea_enter_*` and `qa2_sheet_linea_enter_768.png`.
- **Heads:**
  - `qa2_head_<page>_<lang>_<w>_{before,after}.png` (fr/ar at 1440/768/390/360; it/en at 1024);
  - `qa2_pair_head_{entreprises,parcours}_fr_1440.png`, `qa2_zoom_seals_1440.png`;
  - `qa2_sheet_heads_390_{fr,ar}.png`, `qa2_sheet_heads_it_en_1024.png`, `qa2_sheet_typo_folios.png`;
  - `qa2_short_*` and `qa2_sheet_short_phones.png`;
  - `qa2_parcours_axis_*`;
  - `qa2_forced_*` and `qa2_sheet_forced_1440.png`;
  - `qa2_draw_*`.
- **Fixtures:**
  - `qa2_fx_<name>-<lang>_<w>.png` (fr/ar at 1440/768/390/360);
  - `qa2_fxrm_*` (reduced motion), `qa2_fxnojs_*` (no script), `qa2_fxmo_*` (entrance frames);
  - `qa2_focus_*` and `qa2_sheet_focus.png`;
  - `qa2_lazy_tracciato_*`, `qa2_enter_*`;
  - sheets: `qa2_sheet_fx_390_a.png`, `qa2_sheet_fx_768_flusso_mosaico.png`, `qa2_sheet_fx_k_1440.png`,
    `qa2_sheet_fx_explorer_racconto_1440.png`;
  - `qa2_zoom_tracciato_{ar_390_cards,fr_390_top}.png`.
- **Hover:** `qa2_hover_<fixture>-fr_1440.png`; M21 is in `qa2_data/hover.json`.
- **Home and login:** `qa2_home_{fr,ar}_{1440,390}_{before,after}.png` (0 differing pixels), `qa2_login_eyebrow_*`.
- **Data** (`qa2_data/`): `fx_measure_fr_ar`, `fx_measure_it_en`, `fx_rm`, `fx_nojs`, `fx_keys`, `fx_axe`,
  `fx_motion`, `states`, `focusshots`, `passkeys`, `lazy`, `gutter`, `hover`, `linea_rest`, `linea_enter`, `heads`,
  `cta`, `axis`, `draw`, `cls`, `m22`, `login`, `axe_pages`, `keys_pages`, `budgets`, `perf_proxy` (`.json`), plus
  `pytest_targeted.log` and `pytest_browser.log`.

Lane server 8783 stopped at the end of the review. No Chromium slot is held.
