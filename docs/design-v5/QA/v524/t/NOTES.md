# V5.24 lane T — Typography V2 (label v524-t-build)

Branch `v524-t` (worktree `C:/tmp/ile_wt/v524-t`), cut from `design-v5` at `4bafcfa0` (= tag `v522/p2`, lanes S, M, P1,
S2, H, P2 merged). Lane server 8785 on the lane database `ile_v5_l3` (dev settings, `ILE_DESIGN_PREVIEW=1`,
`ILE_REFERENCE_DATE=2026-10-03`; the clone is in step with `ile_v5`: 75 migrations, 19 users, no refresh needed); pytest on
`test_ile_v524_t`, one at a time; headed `chromium-1234` under a Chromium lock slot (label `v524-t-eye`, one session);
headless probes without a slot; the compressed twin 8782 started from this tree under `PERFORMANCE_BENCHMARK_LOCK` for the
swap-CLS measure alone and stopped again (it was down when the lane began). Binding: V5.24 §11–§14, V5.25, V5.26, V5.20 (the
strict test rule), V5.22 §9.8, `FINAL_DELIVERY_V2.md` §0–§2 (R1, R4, R7, R12, R14) and §3.1, `evidence/v524/TYPOGRAPHY_V2.md`
(adopted whole, R1), `ARABIC_AUDIT.md` + `arabic/05_rtl_checklist_v2.md` (M1, M3, C-1 — the three CSS items T holds for
AR). Evidence of this lane: `C:/tmp/ile_v5_council/evidence/v524/t/` (`probe/` the headless probes and their JSON, `shots/`
the headed stills, `cls-swap/` the twin's figures, `src/readexpro/` the font source as published, `compare_1600.png` the
Arabic reader's exhibit); the lane's tools and logs under `C:/tmp/ile_v5_council/.work/v524-t/`.

Scope held (§3.1): the shared layer only — the fonts, `fonts.css`, `tokens.css`, `base.css`, `buttons.css`, the preload
slice of `base.html`, the two new test modules and the named slices, the three documents. No page sheet, no library partial,
no `main.css` import, no template but the preload lines, **0 JS, 0 strings, 0 images, no migration**.

---

## 1. What the owner sees

| Change | Where it shows now (the shared layer) | Where it shows once the lanes apply the contract |
|---|---|---|
| **Readex Pro** replaces Vazirmatn for every Arabic role, at ratio 1.0 | every Arabic page: nav, buttons, chips, leads, bodies, the console — the Arabic sits at the French's size and colour, on the Latin leadings (body 17/28, no more 32 px Naskh lines), descenders no longer clipped in 20 px controls; 16 128 B in place of 32 228 | — |
| **The twelve steps** declared once (`--t-display` … `--t-field`), the display line and titles at **600**, `--track-display` −0.03 em | every sheet reading `--t-band` (24 → 28), `--t-display` (44 → 64, 600), `--t-lead` (22/32 from 64 rem) and the legacy aliases follows at once | the clamps, literals and mono seats of the page sheets (the burn-down table, §5) |
| **The label role** (`--t-label`: Host Grotesk 13/16 600 +0.08 em, 14/20 on phones and in Arabic) and **the numeral role** (sans 600 tabular) | `.t-label`, `.eyebrow`, V1's folio (`h4`–`h6`, `.t-folio`), `.t-numeral`; the console eyebrow's tracking | `.testa__label`, `.ingresso__label`, the kickers, `.sez-numeral`, `.tracciato__num` (LIB, HOME, PUB1, PUB2, PLAT) |
| **The public phone step-up** — ui 16/24, small 14/20, caption 14/20, label 14/20, the primary call 17/24 below 48 rem and under a coarse pointer | every public page on a phone and every touch desktop: nothing under 14 px | — |
| **The primary call at 16/24 600** (17 on phones) | every `.btn--primary` (the hero's keeps its own 500 and 15 px through hero.css's `.btn.cta-b` / `.he__primary`: HOME's) | — |
| **Arabic type rules in the subject form**, the Latin leading and tracking restored inside a `lang="fr"` run | base.css; the tokens | the 41 descendant-form rules of the page sheets (burn-down) |
| **AR's three RTL minors** — M1 the brand isolate never breaks, M3 inline Latin links isolated, C-1 a wholly-French heading on the French paragraph's edge | every Arabic page | — |

---

## 2. What changed in the code

- `static/fonts/` — **`v5-readex-pro-var-400-700-arabic.woff2`** (16 128 B, SHA-256 `9669ea48…`) built from `google/fonts`
  `ofl/readexpro` v1.205 (`ReadexPro[HEXP,wght].ttf`, 278 544 B, SHA-256 `268bba7e…`, kept with its `OFL.txt` and `METADATA.pb`
  at `evidence/v524/t/src/readexpro/`, outside the repository) by `evidence/v54/w1-a/tools/build_v5_fonts.py` extended
  (`--dst`, the READEX entry: `fontTools.subset` on the Arabic recipe with every layout feature, then
  `varLib.instancer` wght 400–700 and HEXP pinned 0, name IDs 0–6, 13, 14, `recalcTimestamp=False`; the REMOVED list;
  `--check` exits 0 on the tree — the five W1-A files byte-identical, Readex Pro built twice to the same hash). 222 glyphs:
  the Arabic blocks, the presentation forms, U+0020, U+00A0; never the digits or the Latin; 47 of the product's 48 Arabic
  code points (the 48th, U+200E, is a bidi control). `licenses/OFL-ReadexPro.txt` (LF; copyright 2018 The Readex Pro
  Project Authors, RFN «RevReading Lexend» — never used, the subset keeps «Readex Pro»). **Removed:**
  `v5-vazirmatn-var-400-700-arabic.woff2`, `licenses/OFL-Vazirmatn.txt`. The set: 77 240 → **61 140 B**.
- `static/css/v5/fonts.css` — the Readex Pro `@font-face` (variable 400–700, swap, Vazirmatn's `unicode-range`) in
  Vazirmatn's place; `ILE Arabic Fallback` (Segoe UI) recomputed on the lane's Arabic sample with the W1-A method:
  size-adjust **107.1 %**, ascent **93.3 %**, descent **23.3 %**, gap 0 (Vazirmatn's were 97.1 / 105.6 / 55.3); header and
  licence list.
- `static/css/v5/tokens.css` §3.3 — rewritten: the stacks (`--f-sans-ar` on Readex Pro; `--f-serif-ar` and `--numeric-ref`,
  both read nowhere, gone); tracking `--track-display -0.03em · --track-title -0.028em · --track-title-2 -0.02em · --track-band
  -0.016em · --track-entry -0.012em · --track-display-caps 0.02em · --track-label 0.08em` (`--track-eyebrow`, `--track-folio`
  aliases of the label's); **the twelve steps** `--t-display 44→64/1 · --t-title-1 34→56/1.08 · --t-title-2 28→36/1.15 ·
  --t-band 24→28/1.25 · --t-entry 20/28 · --t-lead 20/28 (22/32 from 64 rem) · --t-body 17/28 · --t-ui 15/20 · --t-small 13/20 ·
  --t-caption 12/16 · --t-label 13/16 · --t-numeral 28/32 (+ --t-numeral-lg 36/40) · --t-field 16`; the legacy names
  `--t-plate` (= display), `--t-title` 36/44 (title-2's desktop size, fixed as its consumers were set), `--t-folio` (= label)
  as aliases; the console scale unchanged but `--u-title-lg` (the workspace head's clamp promoted) and the eyebrow as the
  label role; the weights `--w-display: 600`, `--w-label: 600`; `--ar-lh-plus` (0 at `:root`, 0.1 under `:lang(ar)`);
  `--ar-title-lh: 1.25`, `--ar-body-lh: 1.65` kept as legacy aliases on the V2 values (two sheets still read them — §4);
  `--ar-console-lh` gone (read nowhere). **The step-up block** `@media (max-width: 47.999rem), (pointer: coarse)` now holds
  `:root` (the public roles) and the console's (the eyebrow to 13/20). **The Arabic block** `:root:lang(ar), :lang(ar)`
  (the `:root` form so that V1's `static/css/tokens.css` `:root:lang(ar)` Naskh leadings — `--t-prose-lh: 32px`,
  `--t-gloss-lh` — are closed at the same specificity): the stack, `--ar-lh-plus 0.1`, the title leadings 1.1 / 1.18 / 1.25
  / 1.35, entry and lead 2rem, `--t-prose-lh: var(--t-body-lh)`, the small roles at 14 px, every `--track-*` 0. **The Latin
  boundary** `:where(:root:lang(ar)) :where([lang="fr"], [lang="it"], [lang="en"])` restates the stacks, `--ar-lh-plus 0`,
  the Latin leadings and tracking (F-7). **The 64 rem block** gives `--t-lead` 22/32 to `:root` and to the Latin run on an
  Arabic page alike. Also: 25 never-read custom properties removed to pay for the block (§5).
- `static/css/v5/base.css` — the label role (`.t-label, .eyebrow`: sans, `--t-label`, `--t-label-lh`, `--w-label`,
  `--track-label`, uppercase, `"case"`); the numeral role (`.t-numeral`: sans, `--t-numeral`, `--w-title`, tabular); the
  legacy mono re-pointing block trimmed to its tabular figures (no sheet sets the mono on those six classes since V5.22 — the
  `font-family` line was a no-op) and the dead `.home-pilot .section__title` selector dropped (`_pilot.html` has no
  `section__title`); the italic rule narrowed to `.institutional-banner__quote` (the only one components.css still sets
  italic); the Arabic rules in the **subject form** — `:is(h1, h2, h3, h4, h5, h6, .t-band, .t-label, .t-folio,
  .eyebrow):lang(ar):not([translate="no"]) { letter-spacing: 0; text-transform: none; }`, `:is(em, i):lang(ar)`,
  `:is(code, kbd, samp, .t-ref):lang(ar)`; the entrance help-line rule removed (Readex Pro's 1.25 em content area at 14 px
  is 17.5 px, inside entrance.css's 20 px line — the Vazirmatn overlap it corrected cannot recur); **M1** `bdi[dir="ltr"]:not(.phone,
  .email) { white-space: nowrap; }`, **M3** `[dir="rtl"] :is(a, button):is([lang="fr"], [lang="it"], [lang="en"]) {
  unicode-bidi: isolate; }`, **C-1** `[dir="rtl"] :is(h1, h2, h3, h4):has(> [lang="fr"]:only-child) { direction: ltr;
  text-align: start; }`.
- `static/css/v5/buttons.css` — `.btn--primary` 16/24 600 (`font-size: 1rem; line-height: 1.5rem; font-weight:
  var(--w-title)`), 17/24 under the step-up media; `.btn--upper` on `--track-label`, its Arabic rule in the subject form.
- `templates/base.html` lines 24–32 — the Arabic preload href and the comment that names the face (the comment is three
  lines above the slice the plan named; left stale it would have contradicted the href — recorded as a slice extension,
  §4). `templates/errors/standalone.html:26` — the same href (the Arabic error page would otherwise 404 its preload: a
  regression of the file removal, fixed under R14).
- Tests — NEW `tests/frontend/test_typography_v2.py` (the twelve steps declared once; the weight map and tracking; the
  step-up; the Arabic block and the Latin boundary; the label and numeral roles; the subject form and M1/M3/C-1 in base.css;
  the primary call; **the burn-down table** `TYPOGRAPHY_BURNDOWN` over `static/css/v5/**` and `apps/*/static/**` — five
  counts per sheet, equality, never up; the browser guards on the Arabic product with `ARABIC_PAGES` and
  `ARABIC_PAGES_BURNDOWN`); NEW `tests/frontend/test_fonts_budget_v2.py` (the set ≤ 62 000 and the per-file ceilings; Readex
  Pro in Vazirmatn's place with its licence; the subset's contents; FONTS_V5 states the ceilings and the fallback);
  `tests/frontend/test_v5_tokens.py` (twelve tests re-pointed under V5.20, each citing V5.24 §11–§14 / TYPOGRAPHY_V2 §4 /
  FINAL_DELIVERY_V2 R1 in its docstring or comment: the faces and licences, the stacks, the name/mono seat, the scale →
  `test_the_public_scale_is_the_twelve_steps_and_v1_lands_on_them`, the 12/14 px floors, the console step-up — the
  eyebrow at 13 on phones, stronger —, the FONTS_V5 licence list); `tests/frontend/test_design_docs.py` (the §6 phrase
  list: Readex Pro); the two browser slices `tests/frontend/test_browser.py::test_fonts_are_self_hosted_and_loaded` (no
  Readex on `/fr/`; the fetched bytes within the recorded figure) and `tests/i18n/test_rtl_browser.py::test_arabic_typefaces_are_applied_and_loaded`
  (Readex Pro then Host; the body at 17/28; the bytes within the recorded figure); and two slices outside §3.1's list,
  recorded as deviations in §4: `tests/frontend/test_layout.py` (the fonts slices: the Arabic preload is Readex Pro's file;
  the family and licence lists) and `tests/i18n/test_rtl_static.py::test_arabic_has_its_own_display_and_interface_pair`
  (the stack and the face).
- Docs — `docs/design-v5/FONTS_V5.md` (rewritten: the six files with bytes and hashes, the Readex Pro source and build, the
  licences with the hash openings, the loading plan and the recomputed fallback, the swap-CLS record, the per-page bytes and
  the ceilings); `docs/design/DESIGN_SYSTEM_2026.md` §6.1–§6.8 (rewritten: the families, the css block = the cascade, the
  file table, the licence, the loading plan, the twelve steps, the measures and the Arabic leading, the capitals = the label
  role, the numeral role) plus three cells outside §6 that my own files moved (§4); `docs/design-v5/DESIGN_SYSTEM_V5.md` §3.3
  (the cascade block) and §5 (the usage table).
- Tools (outside the repository) — `evidence/v54/w1-a/tools/build_v5_fonts.py` extended; `.work/v524-t/tools/`: `run.sh`
  (the lane's pytest runner on `test_ile_v524_t`), `probe_type.py` (fonts fetched, the Arabic guards, overflow, the hero
  diff, the coarse pointer), `headed_shots.py` (the eye), `cls_swap_8782.py` + `mint_8782_sessions.py` (the twin).

---

## 3. Tools → decision → change (V5.26 §4: each used to decide and implement, none «consulted»)

| Tool (read from disk) | Decision it settled | Change |
|---|---|---|
| **impeccable** `reference/typography.md` («use fewer sizes with more contrast», «hierarchy through scale + weight contrast ≥ 1.25», the fallback metric block, «variable fonts for 3+ weights», «preload the critical weight only», «bound your clamp(): max ≤ 2.5 × min») and `typeset.md` («product: fixed rem scale, 1.125–1.2 between close steps; marketing headings fluid»; «weight contrasts strong enough: medium vs regular is barely visible») | The two registers of the audit confirmed as one system: fluid clamps for the four display/title steps only (the widest ratio, 44 → 64, is 1.45 ×, far under 2.5), fixed rem for everything that reads; the display line at **600** against the 400 body (medium against regular was the F-1 complaint); one variable file per script; the preload count unchanged; the Arabic fallback recomputed with size-adjust / ascent / descent. | `tokens.css` §3.3 (four clamps, eight fixed, `--w-display: 600`); `fonts.css` (the fallback); the preload slice. |
| **taste-skill** Rule 1 («hierarchy with weight and colour, not just massive scale»; serif banned on software UI) and §7 («no oversized H1s») | `--t-title-1` capped at 56 (the `_fronte` value promoted, not a new 64) and `--t-display` reserved to one line per page; the label role as the structural device (13 px, 600, tracked) rather than a size; the serif stays only the name. | The steps' ceilings; the label role in base.css; `--f-serif` = the sans unchanged. |
| **ui-ux-pro-max** `data/google-fonts.csv` (Readex Pro: `HEXP: 0..100 \| wght: 160..700`, subsets arabic/latin/latin-ext/vietnamese, designers incl. Nadine Chahine; Host Grotesk `wght 300..800`, latin only; Vazirmatn `wght 100..900`) and `data/typography.csv` (no Arabic companion pairing with a Latin grotesk; its Arabic row pairs two Notos) | The companion is built from the audit's measurements, not from a catalogue pairing: the axes read from the CSV fixed the build recipe (pin HEXP at 0, limit wght to the product's 400–700); the CSV's latin subset for Readex Pro is why the subset recipe excludes the Latin and the digits explicitly (the stack hands them to Host). | `build_v5_fonts.py` READEX (the instancer limits; the subset ranges; the guard that fails if a digit or a Latin letter slips in). |
| **fontTools 4.60.2** (`subset`, `varLib.instancer`, the name and metrics tables) | The build order (subset, then instance — instancing first raised a `gvar` KeyError on the subset glyph set with `optimize=True`), the reproducibility (`recalcTimestamp=False`, two builds one hash), the metrics for the fallback (typo 1.000 / 0.250, `USE_TYPO_METRICS` set), the coverage check (47 / 48). | The script; `fonts.css`; FONTS_V5 §2, §4. |
| The audit's own crawler and stills (`.work/v524-audit/v524-typo/`), re-aimed at 8785 by `probe_type.py` | Where the shared layer alone already changes the product (the fonts fetched, the Arabic floor, the overflow at 1440/390/360, the hero's geometry, the coarse pointer at 1440) and where only a page lane can (the mono labels, the descendant rules) — the `ARABIC_PAGES_BURNDOWN` list and the per-page font figures recorded in the two browser slices. | `test_typography_v2.py`, the browser slices, §7. |

Not used, and why: `figma-use-motion` / `figma-implement-motion`, `animate`, `find-animation-opportunities`,
`improve-animations`, `emil-design-eng` — nothing of the shared type layer moves; 21st.dev — no component enters (R9).

---

## 4. Contract items applied for other lanes · requests to other lanes · deviations recorded

**Applied here for AR (R7):** M1, M3, C-1 in `base.css` (§2). M2 («Privacy Policy» spans) and the brand `bdi` in the
Arabic catalogue sentences are AR's / PUB2's templates; the CSS waits for them (`bdi[dir="ltr"]` already matches the
`brand_bdi` output).

**The token contract the lanes apply in their own sheets** (TYPOGRAPHY_V2 §4.2, §6; the names as declared here):
`--t-display` / `--t-title-1` / `--t-title-2` / `--t-band` / `--t-entry` / `--t-lead` / `--t-body` / `--t-ui` / `--t-small` /
`--t-caption` / `--t-label` (+ `-lh`, `--track-label`, `--w-label`) / `--t-numeral`, `--t-numeral-lg` (+ `-lh`; weight
`--w-title`) / `--t-field`; `--track-display`, `--track-title`, `--track-title-2`, `--track-band`, `--track-entry`; `--ar-lh-plus`
for a literal title leading (`line-height: calc(1.15 + var(--ar-lh-plus))`); `--u-title-lg` for the workspace head (PLAT).
Every Arabic type rule in the subject form (`.x:lang(ar)`); no `var(--f-mono)` outside the reference classes; no `clamp()`
in a `font-size`; `text-transform: uppercase` only through the label role. **The burn-down table** (`TYPOGRAPHY_BURNDOWN`,
45 sheets, measured on this tree) is each lane's work list — equality, so a converted sheet lowers its row:

| Lane | Sheets (counts: clamp · literal · mono · ar-descendant · uppercase) |
|---|---|
| LIB | `_sezioni.css` 2·0·2·1·1 · `_fronte.css` 6·2·0·1·1 · `_sec-tracciato.css` mono 1 · `_linea-v2.css` mono 1 · `_servizio.css` mono 1 · `_glyph.css` ar 1 · `_steps.css` ar 1 · `_formwork.css` 0·1·0·4·1 · `_receipt.css` 0·1·0·1·0 · `_portico.css` ar 3, upper 2 · `field.css` ar 1 · `aliases.css` mono 2 (`--font-ref`, `--font-mono`: the legacy names — CLOSING's call, not a seat) |
| HOME | `pages.css` 2·0·1·0·1 · `hero.css` 3·3·0·0·4 |
| PUB1 | `_index.css` 0·0·1·1·1 · `_sheet.css` 0·0·1·1·1 · `_diplomas.css` 0·0·1·1·0 · `_training.css` 0·0·1·1·0 · `_persone-v2.css` ar 1, upper 1 · `_companies.css` 1·0·1·0·0 · `_universities.css` mono 1 · `_spazi-v2.css` ar 1 |
| PUB2 | `_agami.css` 2·0·2·1·2 · `_rete.css` 0·0·1·0·1 · `_canali.css` 1·0·0·1·1 · `_contatto.css` 1 · `_frodi.css` 2 · `_faq-v2.css` 0·0·1·0·1 · `_lessico-v2.css` 2·0·0·1·0 · `_forum.css` 1 |
| PLAT | `_platform.css` 1·2·5·0·3 · `_shell.css` 0·1·0·3·0 · `_dashboard.css` ar 1 · `_depot.css` ar 1 · `_frame.css` upper 1 · `_journey-rail.css` ar 1 · `_registers.css` 0·0·1·1·0 · `_table.css` ar 1 · `_workspace.css` 0·0·1·2·0 · `portal.css` literal 1 · `academy.css` mono 1 |
| preserved families (CLOSING decides: a §9.8 exception or a recorded residue) | `chrome.css` 0·6·0·5·3 · `lume.css` ar 1, upper 1 · `entrance.css` ar 2 (`--ar-title-lh`, `--ar-body-lh`) · `wizard.css` ar 1, upper 1 |

**Requests to other lanes (not fixed here, R14):**
- **HOME** — `hero.css`'s `.he-origin__call` is a 12 px literal: on the seeded Arabic home (the test database, gate G3's
  interim variant) the four origin calls «اكتشفوا الفضاء» … draw Arabic under the 14 px floor — the one `small` finding of
  the whole lane (the preview's home does not render them); the token (`--t-caption`, 14 in Arabic) is the fix. The hero's first screen at 390 takes the public step-up through the tokens it reads (`.he__lead` and
  `.he__primary` on `--t-ui`: 15 → 16 px; the station labels on `--t-folio` = the label: 13 → 14 px); the composition's
  anchors do not move (§7.5). If HOME wants the fr 390 first screen byte-identical, one restatement in `hero.css` (`.he {
  --t-ui: 0.9375rem; --t-ui-lh: 1.25rem; --t-folio: 0.8125rem; --t-folio-lh: 1rem; }`) does it; T did not write a page
  class into the shared tokens. Also: `.he-origin__word` 16/19.2 on two lines in Arabic at 390 (the Arabic guard's «tight»;
  `hero.css`) — give it `--t-ui-lh` or 1.3 em. The hero's CTA keeps 500 / 15 px through `.btn.cta-b` / `.he__primary`:
  the audit's 16/24 600 reaches it only if HOME lets it.
- **LIB** — `_fronte.css:194-198` and `_sezioni.css:147` are the two descendant rules still floating French titles in
  Arabic leading (`/ar/parcours/salaried_work/` h1 56/75.6, lead 22/34; `/ar/entreprises/` `.testa__title` 36/50.4); the
  `.testa__label` / `.ingresso__label` mono seats are why the home, Parcours, FAQ, AGAMI and Entreprises still fetch the
  mono files (30 916 B Latin, 47 044 B Arabic on the home). `test_rtl_static.py`'s Vazirmatn slice was re-pointed by T
  (LIB owns the module; T merges first).
- **PUB2** — `_agami.css`: `.agami-id__etichetta(-voce)` and `dt` draw Arabic in ILE Mono (7 elements, F-3);
  `.racconto__titolo` 24/32 on `/ar/le-projet/` (a French h2 on an Arabic leading — LIB's `_sec-racconto.css` or
  `_projet.css`).
- **PLAT** — `--u-title-lg` is declared; `_platform.css:153`'s clamp reads it; `--u-eyebrow` tracking now follows
  `--track-label` (+0.08 em) through `--track-eyebrow` — the console eyebrows gain 0.02 em; the Arabic console eyebrow
  13/20 on phones.
- **CLOSING** — (a) SECTION_SYSTEM_V2 §6.2 erratum («eight sizes, no ninth» and the Vazirmatn rules superseded — R1);
  (b) the comments still naming Vazirmatn: `static/css/v5/chrome.css:149, 540`, `_fronte.css:19`, `aliases.css:113`,
  `tests/i18n/test_rtl_browser_w2_c2.py:130`, the fixture text of `tests/frontend/test_design_preview.py:3655`, the
  historical QA notes and plans (`V5_4_EXECUTION_PLAN.md`, `CREATIVE_DIRECTION_V5.md`, `council/TYPOGRAPHY.md`,
  `IMPLEMENTATION_PLAN.md`, `RED_TEAM.md`, `ASSET_USAGE_MATRIX.md`, `CHANGELOG_V54.md`, `RELEASE_NOTES_v2.0.0.md`,
  `OWNERSHIP_V54.json`'s slice label): records, not product; (c) the legacy aliases to delete when the table is empty:
  `--t-title`, `--t-title-lh`, `--t-plate`, `--t-folio`, `--t-folio-lh`, `--track-eyebrow`, `--track-folio`,
  `--ar-title-lh`, `--ar-body-lh`; (d) `--t-numeral-lh` is a V1 name (DESIGN_SYSTEM_2026 §3 relabelled from «riserva»)
  that `aliases.css` re-declares as `var(--u-numeral-lh)` after tokens.css: when the V1 scale leaves, the V5 declaration
  stands alone; (e) the burn-down rows of the preserved families (above); (f) V1's dead `.t-plate` rule in
  `static/css/base.css` (no `.t-plate` in any template; its `--t-plate-lh` / `--track-plate` aliases were dropped here).
- **Steward** — the §9.8 exception «typography» for `tokens.css` and `base.html` (R1); `check_ownership`'s `FAMILY_ID`
  extension and the family `v524-t` in `OWNERSHIP_V54.json` (R11) with these `owns`: `static/css/v5/tokens.css`,
  `static/css/v5/fonts.css`, `static/css/v5/base.css`, `static/css/v5/buttons.css`, `static/fonts/**`,
  `templates/base.html` (slice 24–32), `templates/errors/standalone.html` (slice 26), `tests/frontend/test_typography_v2.py`,
  `tests/frontend/test_fonts_budget_v2.py`, `tests/frontend/test_v5_tokens.py`, `tests/frontend/test_design_docs.py`
  (slice), `tests/frontend/test_layout.py` (the fonts slices), `tests/frontend/test_browser.py` (slice),
  `tests/i18n/test_rtl_browser.py` (slice), `tests/i18n/test_rtl_static.py` (slice), `docs/design-v5/FONTS_V5.md`,
  `docs/design-v5/DESIGN_SYSTEM_V5.md` (§3.3, §5), `docs/design/DESIGN_SYSTEM_2026.md` (§6; §2 rows 11 and 14; §3 the
  `--t-numeral-lh` row), `docs/design-v5/QA/v524/t/**`, `static/css/dist/main.css`.

**Deviations from §3.1's letter, each with its reason:**
1. `templates/base.html` lines 24–27 (the preload comment) edited with the href at 30 — a stale comment naming the retired
   face above the line that loads the new one; the §9.8 exception's subject (typography) covers both.
2. `templates/errors/standalone.html:26` — the Arabic error page preloads the Arabic face by name; without the edit the
   removed file is a 404 on every Arabic error page (a regression of this lane's change: R14).
3. `tests/frontend/test_layout.py` (fonts slices) and `tests/i18n/test_rtl_static.py` (one test) — both pin the Arabic face
   by name and would turn `design-v5` red at T's merge; T merges before LIB (§9.7's first-lane rule, as PX's). Same
   invariants, on Readex Pro.
4. `docs/design/DESIGN_SYSTEM_2026.md` outside §6: §2 rows 11 (`v5/fonts.css` 6.1 → 7.0 KB, the face name) and 14
   (`v5/base.css` 7.5 → 9.4 KB) — `test_documented_file_weights_are_roughly_true` holds the weights of my own sheets within
   10 %; §3 the `--t-numeral-lh` row relabelled from «riserva» — `test_reserve_labels_match_the_design_system_stylesheets`
   flags a reserve that base.css now consumes (the numeral role reads the V1 name).
5. **The public caption on phones is 14/20, not the audit's 13/20** — the audit's §4.2 table says 13, its §6 test note and
   the gate (3) say «no text under 14 px on phones», V5.24 §13 asks for the dense small text gone: the stronger reading
   wins; the console keeps its 13 px caption and eyebrow on phones (product density, F-13).
6. **The Arabic ui keeps 15/20, not the audit's 15/24** — Readex Pro's 1.25 em content area (18.75 px at 15 px) fits the
   20 px line that clipped Vazirmatn (23.4 px); 15/24 would have moved every control of the preserved navbar in Arabic by
   4 px of line box. Entry and lead do take 20/32 as the audit says.
7. **The Vazirmatn trio is not deleted but aliased** (`--ar-title-lh: 1.25`, `--ar-body-lh: 1.65` on the V2 values;
   `--ar-console-lh`, read nowhere, deleted): `accounts/entrance.css:311, 316` and `static/css/v5/_portico.css:77` (both
   preserved families) read the two names — a hard removal would have set their Arabic leading to the inherited value in
   silence. They are two rows of the burn-down (`ar_descendant`); CLOSING deletes the names when the rows are gone.
8. **The legacy scale names stay as aliases** (`--t-title` 36/44 fixed, `--t-plate`, `--t-folio`): 29 sheets read them; the
   lanes move to the twelve. `--t-title` is kept at its fixed value rather than aliased to the fluid title-2, so that no
   preserved family (the entrance's title, the spaces) changes on phones before its lane decides.
9. `--w-numeral` and `.t-numeral--lg` were not created (the numeral's weight is the title weight; a station reads
   `--t-numeral-lg` in its own sheet) — bytes, §5.
10. **The narrow restatement of W1-A stays:** below 48 rem tokens.css still restates `--track-display: -0.02em` and `--u-title:
    1.5rem` in its layout block (`test_the_narrow_overrides_of_the_names_v5_declares_are_restated` pins it) — the display
    line at 44 px tracks −0.02 em on phones (tracking follows size), −0.03 em from 48 rem; Arabic stays 0 at (0,2,0); a
    French display run inside an Arabic phone page takes the boundary's −0.03 em.
11. **25 never-read custom properties removed from `tokens.css`** to pay for the block (R4 c), each proven unread by a scan
    of every source sheet, JS module, template, Python module, test module and the DESIGN_SYSTEM_2026 css blocks (dynamic
    names included after the first pass caught the contrast pairs' `--tone-*-bg-hover` and the shadow test's
    `--shadow-2-dark`, both restored): `--p-laguna-300`, `--p-laguna-350`, `--p-laguna-600`, `--p-ambra-200`, `--p-cenere-200`,
    `--p-route-1`, `--p-route-3`, `--focus-ring-image-inner`, `--focus-ring-image-outer`, `--scrim-photo-aaa`, `--icon-status`,
    `--pattern-dots`, `--pattern-cross`, `--glass-light-over-dark`, `--inspector-w`, `--chip-bg-hover` (×9), `--count-h`,
    `--popover-bg`, `--popover-shadow`, `--popover-radius`, `--dialog-shadow`, `--toast-w`, `--panel-inset`, `--rail-indicator`,
    `--loader-thread` (+ `-night`), `--loader-light` (+ `-night`), `--journey-light-head`, `--journey-light-tail`,
    `--journey-station-edge`; plus `--f-serif-ar`, `--numeric-ref`, `--ar-console-lh`, `--t-plate-lh`, `--track-plate`. Their
    mentions in `DESIGN_SYSTEM_V5.md` §3–§4 and in historical notes are documentation of a token that no longer exists:
    CLOSING's docs pass (the §3 table of DESIGN_SYSTEM_2026 lists V1's tokens, not these).

**New msgids:** none (0 strings). **JS:** 0. **Images:** 0. **Migrations:** 0.

---

## 5. Budgets (gzip -9 = Python `gzip.compress(…, 9)` on the built dist; two `npm run build` identical)

| Measure | Before (4bafcfa0) | After (this branch) | Ceiling | Note |
|---|---|---|---|---|
| `static/css/dist/main.css` | 32 716 B | **32 695 B** | ≤ 32 716 (the ratchet, never up) | the type block grew (the twelve steps, the step-up, the Arabic block and its Latin boundary, the label and numeral roles, M1/M3/C-1: +352 B at the first build) and was paid inside T's sheets: the dead tokens (§4 item 11), the plate aliases, the trio's console name, `--f-serif-ar`, `--numeric-ref`, the caps restatement, the no-op `font-family` of the legacy mono block, the dead `.home-pilot` selector, the entrance help-line rule; 21 B of air — CLOSING ratchets to the measure |
| the shipped font set | 77 240 B (6 files) | **61 140 B** (6 files) | ≤ 62 000 | Readex Pro 16 128 ≤ 18 000; sans 19 208 ≤ 22 000; italic 14 096 ≤ 15 000; mono 9 960 ≤ 10 000; wordmark 1 748 ≤ 2 000 |
| a Latin public page, fonts fetched | 20 956 – 30 916 B | 20 956 B (login, contact, Le projet, glossary, forum, institutions, fraudes); 23 644 – 30 916 B where a label still draws the mono (home, parcours, FAQ, AGAMI, entreprises) | ≤ 22 000 | the mono rows are LIB's / HOME's / PUB's burn-down; `test_browser.py` records the home at 30 916, never up |
| a Latin console page | 23 644 B | 20 956 B (dashboard, case file, documents, the company's space and need form) | ≤ 24 000 | |
| an Arabic public page | 53 184 – 63 144 B | 37 084 B; 39 772 – 47 044 B where a label still draws the mono | ≤ 38 000 | `test_rtl_browser.py` records the home at 47 044, never up |
| an Arabic console page | 55 872 B | 37 084 B | ≤ 40 000 | |
| swap CLS, matched fallbacks (8782, this tree) | 0.0000 – 0.0009 (W1-A) | **0.0015** worst matched cell (12 cells: home, Arabic home, login, Arabic login, dashboard, Arabic dashboard, documents, Arabic documents at 1440 and 390) | ≤ 0.01 | §7.6 |
| page sheets | — | unchanged (no page sheet touched; the dist of the other sheets byte-identical) | — | the glossary family stays 54 272 / 54 272 |

---

## 6. Tests run (one pytest at a time on `test_ile_v524_t`; `-p no:randomly -p no:cacheprovider`, CI placeholders, the `.env` not read)

| Run (log under `.work/v524-t/logs/`) | Modules | Result |
|---|---|---|
| `static2` (before the test re-pointing: what the change breaks, so that every re-pointed expectation is named) | `test_v5_tokens.py`, `test_layout.py`, `test_rtl_static.py`, `test_design_docs.py`, `test_css_bundle_is_current.py`, `test_frontispiece_v515_c.py`, `test_forms_v515_b.py` | 848 passed, 32 failed (the 29 typography expectations re-pointed in §2, the two docs tests the §2 / §3 cells answer, and 17 contrast / shadow pairs broken by the first dead-token pass — the `--tone-*-bg-hover` and `--shadow-2-dark` tokens restored, §4 item 11) |
| `static3` (the re-pointed tree) | the same + `test_typography_v2.py`, `test_fonts_budget_v2.py`, `tests/i18n/test_catalogues.py`, `test_chips_cards_w1_c.py`, `test_service_pages_w3_f2.py` | 1 146 passed, 2 failed (two of T's own new assertions: the Latin boundary's restated set, the alias comparison — corrected), 1 skipped (`fontTools` is not in the project venv: the subset test rewritten to read the WOFF2 directory as bytes, no skip) |
| `static4` | `test_typography_v2.py`, `test_fonts_budget_v2.py`, `test_v5_tokens.py::test_the_public_scale_is_the_twelve_steps_and_v1_lands_on_them` | **151 passed**, 0 skipped |
| `browser2` (headless Chromium through pytest, no slot) | `test_browser.py::test_fonts_are_self_hosted_and_loaded`, `test_rtl_browser.py::test_arabic_typefaces_are_applied_and_loaded`, `test_typography_v2.py -m browser` (1440, 390) | **4 passed** (`browser1` before it: the home's `.he-origin__call` at 12 px on the seeded Arabic home — HOME's literal, §4 — moved the home into `ARABIC_PAGES_BURNDOWN`, where only the face is asserted) |
| `static5` (the final tree, the gate's list) | `test_v5_tokens.py`, `test_typography_v2.py`, `test_fonts_budget_v2.py`, `test_design_docs.py`, `tests/i18n/test_catalogues.py`, `tests/i18n/test_rtl_static.py`, `test_layout.py`, `test_css_bundle_is_current.py`, `test_frontispiece_v515_c.py`, `test_forms_v515_b.py` | **1 083 passed, 0 failed, 0 skipped (5 browser tests deselected) in 6 min 47 s** |

Every test change is under V5.20's four conditions, cited in the test (V5.24 §11–§14, TYPOGRAPHY_V2 §4, FINAL_DELIVERY_V2
R1 / §3.1); none loosened: the faces and licences, the stacks, the scale, the floors and the console step-up are asserted
on the new values with the same or a stronger invariant; the two browser slices assert more than before (the bytes fetched,
the body's size and leading, no retired face); the per-page font figures recorded there (30 916 / 47 044) are measures
to burn down, never ceilings raised.

`ruff check` on every changed Python file: 0. `manage.py check`: 0 issues. `makemigrations --check`: no changes. `npm run
build` twice: identical (only `static/css/dist/main.css` changed in dist).

---

## 7. Probes (headless, no slot; `evidence/v524/t/probe/*.json`; lane 8785 against the base 8780 = `4bafcfa0`)

### 7.1 Fonts fetched per page (`fonts.json`, 1440, encoded bytes)
Readex Pro on every `/ar/` page and never on a `/fr/` one; no Vazirmatn anywhere; the figures of §5. The persona pages
(dashboard, case file, documents, the company's space and need form) fetch no mono at all (20 956 / 37 084).

### 7.2 The Arabic guards (`arabic.json`; 1440 and 390; 13 public pages + 5 persona pages)
- **Nothing under 14 px on any Arabic page of the preview database** (0 findings in 36 page loads); under pytest's seeded
  database the home's interim hero draws its four origin calls at a 12 px literal (`hero.css`, HOME — §4).
- **No Arabic letters in an element whose first family is ILE Mono** — except AGAMI's identification block (7 elements,
  PUB2's `_agami.css`, F-3).
- **Multi-line Arabic under 1.3 em** — only `.he-origin__word` 16/19.2 on the home at 390 (HOME's `hero.css`).
- **French blocks on an Arabic page at Arabic leading** (block-level elements of ≥ 20 px; titles ≥ 24 px over 1.3, the rest
  over 1.5): the pathway sheet's h1 and lead (`_fronte.css`, LIB), Entreprises' `.testa__title` (`_sezioni.css:147`, LIB) and
  a 24/44 statement (`_companies.css`, PUB1), Le projet's `.racconto__titolo` 24/32 — all descendant-form rules of the
  burn-down; with the shared layer alone the home, Parcours, FAQ, Glossaire, Contact, login, Forum, Fraudes and the five
  persona pages pass (the test's `ARABIC_PAGES`).

### 7.3 Overflow and console errors (`overflow.json`)
1440 / 390 / 360 × fr / ar × 13 pages = **78 loads: `scrollWidth ≤ clientWidth` on every one, 0 console errors, 0 page errors.**

### 7.4 The coarse pointer at 1440 (`coarse.json`, `coarse_{fr,ar}_1440.png`; touch emulated — CDP's media feature emulation
does not flip `pointer`, Playwright's `has_touch` does)
`(pointer: coarse)` true → `--t-ui` 1rem, the nav links 16 px, the primary 17 px: the single-row navbar holds **one row of six
links** in fr and ar, header 65 px, no overflow.

### 7.5 The hero's first screen, lane against base (`hero_geometry.json`, `hero_diff_*.png`; reduced motion, fonts loaded)
Every element under `.he` with a class, bounding boxes compared (117 at 1440, 97 at 390):
- **1440 fr: 0 elements moved or resized, 0 type changes** (the CTA keeps its own 500 / 15 px: `.btn.cta-b`, `.he__primary`).
- **390 fr:** no anchor moves — the statement, the door, the stations' nodes, the origins, the CTA box are where they were;
  four text boxes grew by their own type (the secondary link 15 → 16 px, two station labels 13 → 14 px: the step-up through
  `--t-ui` and `--t-folio`), five more changed type without moving (the CTA 15 → 16, three labels). Pixel diff 4.1 % of the
  viewport = the re-rasterised glyphs (`hero_diff_fr_390.png`).
- **1440 ar / 390 ar:** the text-sized boxes follow Readex Pro's metrics (the CTA 218 → 235 px wide; the Arabic origin words'
  line boxes 26 → 21 px, their arrows 2 px lower; «المغرب» 6 px wider) — the statement, the nodes, the door and the panels
  unchanged. Pixel diff 1.2 % / 2.3 %: every Arabic glyph is a different face.
The gate (4) asked for weight and tracking only; the step-up and the face change are the two token-level decisions the
audit adopted (F-5, §3); the composition did not move. HOME's option in §4 if the fr 390 screen must stay byte-identical.

### 7.6 Swap CLS on the compressed twin 8782 (`cls-swap/cls_swap.json`; the W1-A method: every woff2 held 1.5 s, the swap's shifts summed; matched = the cascade as written, bare = the override descriptors stripped in flight; Windows fallbacks)
| Page | Viewport | matched (the cascade) | bare (overrides stripped) | Faces loaded |
|---|---|---|---|---|
| home | 1440x900 | **0.0008** | 0.0004 | Host Grotesk, ILE Mono, ILE Wordmark |
| home | 390x844 | **0.0015** | 0.0000 | Host Grotesk, ILE Mono, ILE Wordmark |
| home-ar | 1440x900 | **0.0011** | 0.0039 | Host Grotesk, ILE Mono, ILE Wordmark, Readex Pro |
| home-ar | 390x844 | **0.0004** | 0.0005 | Host Grotesk, ILE Mono, ILE Wordmark, Readex Pro |
| login | 1440x900 | **0.0003** | 0.0007 | Host Grotesk, ILE Wordmark |
| login-ar | 390x844 | **0.0006** | 0.0006 | Host Grotesk, ILE Wordmark, Readex Pro |
| dashboard | 1440x900 | **0.0000** | 0.0002 | Host Grotesk, ILE Mono, ILE Wordmark |
| dashboard-ar | 1440x900 | **0.0001** | 0.0004 | Host Grotesk, ILE Mono, ILE Wordmark, Readex Pro |
| dashboard-ar | 390x844 | **0.0004** | 0.0011 | Host Grotesk, ILE Mono, Readex Pro |
| documents | 1440x900 | **0.0000** | 0.0003 | Host Grotesk, ILE Mono, ILE Wordmark |
| documents | 390x844 | **0.0000** | 0.0004 | Host Grotesk, ILE Mono |
| documents-ar | 390x844 | **0.0006** | 0.0019 | Host Grotesk, ILE Mono, Readex Pro |

Every cell 200 (the twin's `ile_v5_perf` was four migrations behind the tree — `core 0003_public_telephone_channels` among them — and answered 500 on the persona pages until `manage.py migrate` under `settings_8782` brought it to 75, recorded for the Performance Lead); **worst matched swap CLS 0.0015 ≤ 0.01** (W1-A measured 0.0000 – 0.0009 on Vazirmatn); the bare cells up to 0.0039: the recomputed Arabic fallback is load-bearing too. 8782 was started from this tree for this measure alone (collectstatic into `evidence/v54/static-8782`, hashed URLs, `Content-Length: 16128` for the Arabic face, gzip and `immutable` as SERVERS.md says) under `PERFORMANCE_BENCHMARK_LOCK` (label `v524-t cls-swap`), then stopped and the lock released; it was down when the lane began. The minted session file was deleted after the run.

---

## 8. The eye (gate 3): headed `chromium-1234` under slot `v524-t-eye`, lane 8785, stills under `evidence/v524/t/shots/`

Stills: `{page}_{lang}_{width}_{n}.png` — home (5 per cell), Parcours (3), FAQ (2), Le projet (3), AGAMI (3), Contact (2),
login (1) at 1440 / 1024 (home, Parcours, AGAMI) / 390 × fr · ar; the person dashboard and the case file at 1440 and 390 × fr ·
ar (`dash_*`, `case_*`; the lane server's preview switch answers on its own port once `ILE_DESIGN_PREVIEW_PORT=8785` is set —
the first start without it served the login page in the personas' place, re-shot). What the eye found, item by item of gate 3:

- **Display weight and tracking.** The hero's statement is HOME's own 500 / −0.028 em (`hero.css`, not through the tokens):
  unchanged at 1440 and 390, fr and ar. The pilot's title and the Glossaire letters read `--w-display` / `--t-display` and are
  600 now (`home_fr_1440_3`, `home_ar_1440_3`). The AGAMI name device unchanged (700, its own clamp — LIB's `_fronte.css`).
- **One label per head at 13 / 14 px in the sans.** The library heads still carry the mono folio (`.testa__label` «Comment ça
  marche :» 15 px mono at 390, `home_fr_390_1`; the FAQ category «GÉNÉRAL», the Parcours kicker) — the burn-down rows of LIB /
  PUB2 / PUB1; the V1 folios and the console eyebrows (dashboard: «فضاء الأفراد», «ESPACE PERSONNES») are the label role already.
- **Numerals in the sans.** The route's «01 · 02 · 06» on Parcours and «01–04» on the home are the mono numerals (`_index.css`,
  `_sezioni.css` — PUB1 / LIB rows); the console's step chips («الخطوة 1 من 7», «Étape 1 sur 7») are Host, tabular.
- **Arabic parity beside the French plates.** On the Arabic home, Parcours, FAQ, AGAMI, Contact, login, dashboard and case
  file Readex Pro sits at the French's size and colour: the nav words, the CTA «اكتشفوا استبيان التوجيه», the origins' titles
  («الأفراد», «الشركات» …) against their French descriptions, the FAQ lead against the locked French questions, the case file's
  «إجراؤكم التالي» head against «Diplôme ou titre de formation» (`dash_ar_1440_0`, `case_ar_1440_0`). The tall-digit effect is
  gone: «EE167596D4», «21.09.2026», «1 من 7» sit on the Arabic line.
- **Descenders in nav words, chips and buttons.** No clipping in the Arabic navbar (16 px / 20 px line at 1440, the 390 sheet's
  rows), the status chips («للاستبدال», «أنت هنا»), the primary buttons («استبدال المستند», «تسجيل الدخول») and the rail
  (`dash_ar_1440_0`, `home_ar_390_0`).
- **The French runs on `/ar/` at Latin leading.** The home's locked statement and the entrances' descriptions, the FAQ's locked
  questions, the case file's French requirement titles sit on 1.08–1.4 (`home_ar_1440_0`, `faq_ar_390_1`, `case_ar_1440_0`); the
  exceptions the probe named (the pathway sheet's h1 and lead, Entreprises' `.testa__title`) are LIB's descendant rules.
- **Nothing under 14 px on phones.** The login at 390 (`login_fr_390_0`): labels 14, help 16/24, the primary 17 px 600; the home's
  station labels 14; the FAQ's disclosure rows 20 px; the footer headings 14 (the caption floor). The Pexels credits still
  visible at 390 (Parcours, Contact) are PX's lane, 14 px.
- **The identification block on AGAMI** (`agami_ar_1440_1`): the Arabic registers («جهة الاتصال الرسمية», «المقر القانوني» …)
  draw in a monospaced system fallback — the mono seat of `_agami.css` (PUB2, F-3) that the gate names; the values («AGAMI —
  Dialogo Giuridico Interculturale APS», the address, the codes) are Host at Latin leading, LTR, as before.
- **The swap on 8782** with the fallback held 1.5 s: §7.6 — the Arabic fallback (Segoe UI at 107.1 %) holds the line count of
  the home's lead and the dashboard's rail; no cell over 0.0015.
- **Nothing broken by the shared layer:** no overflow at 1440 / 1024 / 390 in either language, no console error (§7.3), the
  single-row navbar, the mega menus and the phone sheet as before, the forms' fields at 16 px, the Lume key where it was.

---

## 9. Post-acceptance candidates seen outside this lane's tables (R14: recorded, not fixed)

- HOME · `hero.css`: the Arabic origin words `.he-origin__word` at 16/19.2 on two lines (under 1.3 em — the only `tight`
  finding of the public crawl); the hero's CTA at 500 / 15 px while every other primary is 600 / 16 (`.btn.cta-b`,
  `.he__primary`); the `.he__eyebrow` and `.he-station__label` literal tracking (0.04 em) beside the label role's 0.08 em.
- PLAT · `_dashboard.css`: the company dashboard's `h2.db-now__title` 20/25 on two lines in Arabic (the probe's one console
  `tight` finding; `arabic.json`); the console eyebrows' tracking now +0.08 em through `--track-eyebrow` — PLAT confirms or
  re-pins.
- PUB1 · `_companies.css`: a French statement at 24/44 (1.83) on `/ar/entreprises/` at 390 — a descendant rule or a literal
  leading; `_index.css`: the route's mono numerals beside the glyph tiles (F-3, the audit's «index of a report»).
- PUB2 · `_agami.css`: the Arabic registers in ILE Mono (7 elements); `_lessico-v2.css`: the letters at 64 px still 500
  (`.lessico__lettera`, F-1) — in PUB2's table already.
- LIB · `_fronte.css:194-198`, `_sezioni.css:147`: the two descendant rules; `.testa__label` / `.ingresso__label` in the mono
  (the six public pages' extra 2 688–9 960 B of fonts).
- PX · the visible «Photo : … / Pexels» lines at 390 on Parcours and Contact (`parcours_ar_1440_1`, `contact_ar_390_0`) — PX's
  D1–D8.
- CLOSING · the preserved chrome's rows in the burn-down (`chrome.css` 6 literals, 5 descendant rules, 3 uppercase;
  `_portico.css`, `lume.css`, `field.css`, `_formwork.css`, `_glyph.css`, `_steps.css`, `entrance.css`, `wizard.css`): a §9.8
  exception or a recorded residue — T did not touch them.
- The dev board (`static/css/dev/*.css`, `apps/core/dev.py:127` lists `--t-plate`): outside the disciplines on purpose; its
  specimens still name the eight-size scale.
- The twin 8782's database `ile_v5_perf` lagged the tree by four migrations (now applied); the lane clones `ile_v5_l3…l9`
  were in step — SERVERS.md's «refresh after every merge» note for the Performance Lead.

---

## 10. Register — where «Vazirmatn» still appears after this lane

The face, its file, its licence, its stack, its preload, its `@font-face`: **0** anywhere. The word itself, after this lane:
- `static/`, `templates/`, `apps/`, `scripts/` (dist and pycache excluded): 3 files, every one a comment outside
  T's files — `static/css/v5/_fronte.css`, `static/css/v5/aliases.css`, `static/css/v5/chrome.css` (CLOSING item b);
- `tests/`: 9 files — the «retired» lists that assert the name is gone (`test_v5_tokens.py`, `test_layout.py`,
  `test_rtl_static.py`, `test_rtl_browser.py`, `test_fonts_budget_v2.py`, `test_typography_v2.py`, `test_browser.py`),
  one comment (`test_rtl_browser_w2_c2.py:130`) and one fixture text (`test_design_preview.py:3655`).
`grep -ril vazirmatn static/fonts static/css/v5/fonts.css static/css/v5/tokens.css templates` → 0.
