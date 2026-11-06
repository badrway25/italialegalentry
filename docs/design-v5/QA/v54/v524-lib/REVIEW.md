# V5.24 lane LIB — the reviewer's targeted gate, ROUND 2 (label `v524-lib-qa`, 6 November 2026, 02:05–02:40)

Reviewed: branch `v524-lib`, worktree `C:/tmp/ile_wt/v524-lib`, **committed head `3e46c896`** on `design-v5` `554c82d2` (= `design-v5`
HEAD, the v524-t merge — the lane needs no rebase). Gate: `FINAL_DELIVERY_V2.md` §3.3 «Gate (reviewer, targeted)» items (1)–(5),
V5.25 §2 (targeted, never the matrix), V5.20 (no test loosened), R3/R4/R9/R10/R12/R14, and the six blockers of round 1 (this file's
previous version, 00:13–00:55, FAIL) re-verified one by one. Served on 8786 by the reviewer (database lane `ile_v5_l5`, pid 20952,
launcher 30232, `--noreload`, the committed tree); pytest on `test_ile_v524_lib` (one run at a time; the headless twins on
`test_ile_v524_libq`); headed Chromium (`chromium-1234`) under `CHROMIUM_LOCK_A`, label `v524-lib-qa2`, 02:11:03 → 02:21:23;
headless probes without a slot (R12). Nothing in any repository was changed by this review; the worktree's `git status` is empty
before and after (two `npm run build` runs rewrote the dist byte-identically).

Round 1 is kept for the record in `docs/design-v5/QA/v524/lib/NOTES.md` §10 (the builder's answer, finding by finding); its 189 frames
stay under `evidence/v524/lib/qa/`. This round's frames and measures: `evidence/v524/lib/qa2/` (`qa2_measures.json`, `qa2_console.json`).

## 0. Verdict

**PASS — 0 blockers, 9 minors recorded. The lane merges as it stands (`3e46c896`).** Every item of §3.3's gate holds on the committed
head, measured again by the reviewer rather than read from the NOTES: (1) the static letter — the six kinds and three attributes read
by the shell and `_materia.css` alone, tokens and mixes only, logical properties, the verb rules under `no-preference` and
`:root:not(.rm)`, `test_rm_flag_parity.py` untouched and green, the RTL twins, LF files, a reproducible dist equal to the committed one;
(2) the specimen board at 1440 · 1024 · 390 in fr and ar — the raccordo now **painted** across the seam (193 against 235) with its node
**0.0 px** off the entered band's head rule, drawing once 0.9 s after the band's own line and leaving `getAnimations()`, the incastro
lifting the first door **64 px** over the band above, the grid and the light mirrored, the velatura still, the niche face, the mosaico's
draw + ink + layer with no settle, `reduce` writing no state and showing drawn stills, the keyboard running nothing; (3) the protection
on Parcours, the eight sheets' sample, Formation, Diplômes and the home — the sill to the container's edge at every width, the shield
low on the far side at 30 % where the field allows it and **standing down at 1024 and on the sheets** (nothing over the plate anywhere,
fr and ar); (4) the type roles — every LIB role on the twelve steps, Arabic through the tokens, no mono, no descendant Arabic rule, the
home's hero-line junction at **0.0 px** again; (5) the budgets — `main.css` 32 695 ≤ 32 716, the home **61 415 ≤ 61 440**, every partial
and route sheet under its ceiling, the one re-recorded ceiling cited under R4 f. Locked copy byte-identical and rendered identically to
the preview; both channels identical (compared in process); no test loosened; no preserved family touched; every tool use ended in a
visible change; the contract items for the other lanes written. Tests: 1 603 + 124 passed; the six reds are the base's (m2), none LIB's.

The six blockers of round 1 are closed one by one (§8). Round 1's verdict stands as the record of why the improve round was needed; this
verdict replaces it.

## 1. Gate item (1) — static

| Check | Result |
|---|---|
| the six ground kinds and the three attributes read only by `_materia.css` and the shell | PASS — `grep -rl 'data-luce\|data-sfuma\|data-incastro'` over `static/css/v5` and `apps/*/static` (dist excluded) → `_materia.css` only; the kinds named in any sheet are exactly `paper · stone · pietra · brand · night · photo`; `test_the_six_ground_kinds_and_the_material_attributes_are_painted_by_the_shell_and_materia_only` green (§6) |
| `_materia.css` tokens / `color-mix` of tokens only, logical properties only, no literal colour, no duration or curve of its own | PASS — read line by line against BACKGROUND_MATERIAL_V2 §3.1–§3.2 and §3.4: the mask's opaque stop is `--p-notte-950` (alpha only — the audit wrote `black`, a literal the sheet may not carry), `--riga` a mix of `--line-rhythm`, the light a mix of `--accent-mark`, `--sez-next` four tokens, the node `--accent-mark`, the line `--line-structure` / `--accent-night`; no `animation` / `transition`, no `--motion-*` / `--ease-*` declared; every inset logical; `varco` 0 occurrences (R3); `test_materia_holds_tokens_and_colour_mixes_of_tokens_only_logical_properties_and_no_motion_of_its_own` green |
| every verb rule under `prefers-reduced-motion: no-preference` and `:root:not(.rm)` with a drawn still | PASS — the raccordo rides `_reveal.css`'s `draw-y` (`wait` `scale: 1 0`; `in` `sez-draw-y`, `--ease-sine`, `--motion-draw`, backwards) and has no rule of its own (deviation 1, recorded); the tile's light now lives in `_sec-mosaico.css:255-260` under `@media (prefers-reduced-motion: no-preference)` and `:root:not(.rm):not([data-input="key"])`, `backwards`; forced colours draw the line and node in `CanvasText`, print and forced colours hide the grid and the velatura (`_materia.css:212-220`) |
| `test_rm_flag_parity.py` unchanged and green | PASS — not in the diff (`git diff design-v5...HEAD -- tests/frontend/test_rm_flag_parity.py` empty); green in §6 |
| the RTL twins present (`test_rtl_static.py`) | PASS — the mask `to left` / `[dir="rtl"] … to right`, the light `at 0 0` / `at 100% 0` (`_materia.css:121-135`); the raccordo and the layers on logical insets (no `translate`); `tests/i18n/test_rtl_static.py` green in §6 |
| `_materia.css` never imported by `main.css`; imported after the shell | PASS — `main.css` untouched (32 695 B, R4 c); the one importer is `apps/core/static/core/sezioni.css` (the fixtures' bundle, one line after `_sezioni.css`; a recorded deviation — the page lanes import it into their route sheets) |
| the two edited test modules under V5.20 | PASS — `test_sezioni_v522_s.py`: one line, the `_sec-mosaico.css` ceiling 1 229 → **1 355 re-recorded at the measure under R4 f**, cited (the builder's deviation 4 — see m1 below: the audited «≈ 120» increment would have given ≈ 1 323; the reviewer measured every spelling 1 349–1 355 and none reaches it without dropping a declaration); `test_typography_v2.py` (lane T's module, a slice the gate itself demands): the burn-down rows of `_sezioni`, `_sec-tracciato`, `_linea-v2`, `_servizio` deleted (equality → 0 measured) and `_fronte.css` 6·2·1·1 → `{"clamp": 2, "uppercase": 1}` (a lower equality), `/ar/parcours/salaried_work/` moved from the burn-down into `ARABIC_PAGES` (a stronger guard; the two remaining rows reworded, none removed). No skip, no timeout raised (the twin's `wait_for_function` keeps Playwright's default) |
| files LF, the dist reproducible, the committed dist = the build | PASS — `git ls-files --eol` over every changed source: all `i/lf w/lf`; `npm run build` twice by the reviewer → 77 dist files, the two sha256 lists identical (`.work/v524-lib/logs/qa2_dist1.sha` = `qa2_dist2.sha`), `git status --porcelain` empty after each (the committed dist IS the build) |
| `ruff check` on the four touched test modules | PASS — «All checks passed!» |

## 2. Gate item (2) — the specimen board (headed, under the slot, 1440 · 1024 · 390 × fr · ar; then `reduce`; then the keyboard)

1440 · 1024 · 390 × fr · ar, `reduced-motion: no-preference`; then `reduce`; then the keyboard (Tab first). 200 frames in
`C:/tmp/ile_v5_council/evidence/v524/lib/qa2/` (`fx_<fixture>-<lang>_<width>[_rm|_key|_seam].png`), measures in `qa2/qa2_measures.json`,
console `qa2/qa2_console.json` (**0 errors in 200 frames**), axe (serious + critical, `main`) **0** on every fixture and page probed.

| Recipe / primitive | Measured (every cell unless a width is named) | Verdict |
|---|---|---|
| pietra | `::before` grid `48px 48px, 48px 48px`, mask `linear-gradient(to left, …)` in fr and `to right` in ar; the grid stands on the far side and fades toward the plate (`fx_pietra-fr_1440.png`, `fx_pietra-ar_1440.png`); on the plate nothing | PASS |
| carta viva | `radial-gradient(60% 50% at 0px 0px, …)` fr / `at 100% 0px` ar at 1440 · 1024 · 390 (`fx_luce-*.png`) | PASS |
| velatura | `::after` 192 px at 1440 / 1024, 128 px at 390; `linear-gradient(transparent → the next ground)`; 0 animations on `::after` after the trigger, in `reduce` the same layer (`fx_sfuma-*.png`) | PASS (a still ground) |
| **raccordo** | the span's parent IS the entered band (`[data-sec="strato"][data-ground="stone"][data-rhythm="strip"]`) in all six cells; before the trigger `scale: 1 0` (`wait`); on the band's trigger `sez-draw-y` runs beside the band's own `sez-draw`, `animationDelay 0.9s`; 3 s later `getAnimations()` empty and `scale: none`; rect 2 × **48 · 41 · 32** (1440 · 1024 · 390); the line's top − the band's top **0.0** px; **the line's bottom − the head rule's top 0.0 px** (letter: ≤ 2) in fr and ar at every width; **painted: the line's 4 px column reads 193.2–193.5 against the ground's 235.0 beside it** (Δ ≈ 42 on 0–255) in all six cells (`fx_raccordo-*_seam.png`: the line crossing the seam and ending on a gold node beside the head rule's start); `--raccordo-x` placed (23 px) | **PASS (B2 closed)** |
| **incastro** | the band 64 px up (`bandUp 64`), `padding-top 0px`, the ground `linear-gradient(transparent 64px, stone 0)`, **the first door's top 64 px above the band above's foot (`doorOverAbove 64`)** in all six cells (`fx_incastro-*.png`: the arched tops over the paper band) | **PASS (B4 closed)** |
| the tile's niche face | `.sez-tile` `linear-gradient(rgb(211,210,204) → raised 85%)` and `isolation: isolate` on every fixture tile and on the Parcours board, FAQ «il rimando», Formation, Diplômes; the glyph on `--text-1` over `--line-rhythm` 12.9:1 (`test_the_tile_s_face_is_a_niche…` green) | PASS |
| the mosaico verb | before the trigger the floor layer at `opacity 0`; on the trigger `sez-draw` (the card's rule), `sez-ink` (the glyph), `sez-layer` on `::before` (the floor) — **no `sez-node`**; empty after 3 s; the floor at 1 at rest (`fx_mosaico-*.png`, both languages, three widths); the light's rules read from `_sec-mosaico.css` (the shell carries none, B1) | PASS |
| reduced motion (`reduce`) | **0 `[data-sec-state]`, 0 running animations** on raccordo · pietra · mosaico · incastro · sfuma at every width in fr and ar; the raccordo `scale: none` (drawn) **and painted (193 vs 235)**; the floor at 1; the incastro's 64 px rise; the velatura 192/128 (`fx_*_rm.png`) | PASS |
| keyboard (Tab, then the scroll) | `html[data-input="key"]`, **0 running animations**, the raccordo `scale: none`, the floor lit (`fx_*_key.png`) | PASS |
| overflow · console · axe | `scrollWidth − clientWidth` 0 on every fixture and page at every width; 0 console errors; axe serious/critical 0 on pietra, mosaico, raccordo, incastro (`main`) in fr and ar at three widths | PASS |

The reviewer looked at the stills, not only the numbers: `fx_raccordo-fr_1440_seam.png` / `fx_raccordo-ar_1440_seam.png` / `fx_raccordo-fr_390_seam.png`
show the 2 px line leaving the seam and the gold node on the entered strip's head line (mirrored in Arabic); `fx_raccordo-fr_1440_rm.png` the
same line standing drawn under `reduce`; `fx_incastro-fr_1440.png` / `-ar_1440.png` the four arched tops the whole 64 px over the paper
band; `fx_pietra-fr_1440.png` / `-ar_1440.png` the drafting grid on the far side fading toward the plate, the shield low at 30 %, the
sill from the plate's far edge to the container's; `fx_mosaico-fr_1440.png` the niche faces with their 40 % rules and lit floors;
`fx_luce-fr_1440.png` / `-ar_1440.png` the light at the origin corner, mirrored; `fx_sfuma-fr_1440.png` the night dissolving over 12 rem.

## 3. Gate item (3) — «la protezione» on Parcours (and the sheet, Formation, Diplômes, the home's S6)

The product's protection bands stand on `stone` until the page lanes import `_materia.css` (`pietra` is HOME's / PUB1's attribute); the
sill and the bookend draw on either — measured on 8786 (`qa2/qa2_measures.json`, the stills `<page>_<lang>_<width>_body.png` and
`home_*_protezione.png`):

| Page · width | Plate | Field | Sill (plate's far edge → container) | Shield (12 rem, opacity 0.3, far side, low) | Verdict |
|---|---|---|---|---|---|
| Parcours 1440 fr / ar | 92–988 / 436–1332 (896) | 92–1332 (1240) | 988–1332 / 92–436, **344 px**, on the plate's top rule | **1140–1332 / 92–284**, below the plate's middle, `overlap False` (`parcours_fr_1440_body.png`, `parcours_ar_1440_body.png`) | PASS |
| Parcours 1024 fr / ar | 40–936 / 73–969 | 40–969 (929) | 33 px | **`display: none`** — the field's free span (33 px) is under the shield's 12 rem; the sill alone runs on (`parcours_fr_1024_body.png`, `parcours_ar_1024_body.png`) | **PASS (B3 closed)** |
| Parcours 390 fr / ar | the whole field (335) | 335 | 0 px (nothing drawn) | `display: none` | PASS |
| the sheet `salaried_work` 1440 fr / ar | 420–1316 / 108–1004 in a 912 px column | 912 | **16 px** to the column's edge | **`display: none`** (round 1: 176 px behind the plate) (`sheet_fr_1440_body.png`, `sheet_ar_1440_body.png`) | **PASS (B3 closed)** |
| the sheet 1024 · 390 | the whole 679 / 335 px column | — | 0 | `display: none` | PASS |
| Formation · Diplômes 1440 fr / ar | 92–988 / 436–1332 | 1240 | 344 px | 1140–1332 / 92–284, `overlap False` | PASS |
| Formation · Diplômes 1024 · 390 | 896 / the field | 929 / the field | 33 / 0 | `display: none` | PASS |
| the home S6 1440 fr / ar | 92–988 / 436–1332 | 1240 | 344 px | 1140–1332 / 92–284 | PASS |
| the home S6 1024 fr / ar | 32–928 / 81–977 | 32–977 (945: the home's wider container) | **49 px** | `display: none` (49 < 192) | PASS |
| the home S6 390 | the whole field (343) | 343 | 0 | `display: none` | PASS |

The field is a size container (`container-type: inline-size` computed on `.protezione__campo` in every cell); the shield at 30 %
(`opacity 0.3`), 192 px, `stroke: var(--line-structure)`, `fill: none`; the sill 1 px of `--line-structure` from the plate's top rule
(Δ ≤ 1 px); its draw is the `draw` verb after the soglia (`--sez-d: var(--motion-draw)` in the sheet — asserted by
`test_the_protection_stands_on_a_drawing_table…`; round 1 measured the delay on the running animation, this round's fixture band was in
view at load, so its entrance had played before the probe read it — the geometry is what changed and it is right). The locked text of
the plate is byte-identical (§5). The pietra ground proper (the drafting grid) was proven on the fixture board (§2) and reaches the
product with the page lanes' attribute.

## 4. Gate item (4) — the type roles in the library (computed styles on the lane server, `qa2/qa2_measures.json`)

| Role | 1440 fr | 390 fr | 1440 ar | Verdict |
|---|---|---|---|---|
| `.ingresso__label` (folio) | Host Grotesk 13/16 600 +1.04 px (0.08 em) uppercase | 14/20 600 +1.12 px | Readex Pro 14/20 600, no tracking, no capitals | PASS |
| `.testa__label.t-label` (panel head) | 13/16 600 +1.04 px uppercase (Entreprises) | 14/20 600 +1.12 px | Readex Pro 14/20 600, no capitals | PASS (LIB's); the first `.testa__label` on Parcours and the home is PUB1's board label / HOME's colophon without `t-label` → the net's 13/16 600 +0.08 em but no capitals (their request in NOTES §4) |
| `.testa__title` statement / process | 36/41.4 600 −0.72 px · 28/35 600 −0.448 px | 28/32.2 · 24/30 | Readex Pro 36/45 (1.25 = 1.15 + `--ar-lh-plus`) · 28/37.8 | PASS — the descendant `:lang(ar)` rule gone, the tokens carry Arabic |
| h1 on `--t-title-1` | 56/60.48 600 −1.568 px (sheet, Le projet, FAQ, AGAMI, Formation, Contact) | 34/36.72 | Arabic h1 56/66.08 (1.18); the French h1 on `/ar/parcours/salaried_work/` 56/60.48 (1.08, F-7 closed) | PASS |
| caps h1 on `--t-title-2` + 0.02 em | 36/41.4 +0.72 px (Parcours, Entreprises, Diplômes) | 28/32.2 +0.56 px | 36/41.4 (a Latin run on the Arabic page) | PASS (the Forum's caps title reads 36/44 with the same +0.72 px: its leading comes from `forum/_forum.css`, PUB2's row) |
| numerals (`.tracciato__num`, `.filo__num`, `.sez-numeral`, the linea's) | board 28/32 600 Host Grotesk; filo 36/40 600; the home's orientation across numeral 36/36 600 (the solo numeral's row, B6) | 28/32 | 28/32 · 36/40 Readex Pro | PASS — no mono |
| `.strato__corpo--parola .ls-1` («Non.») | 600 | 600 | 600 | PASS |
| Contact address link | 28/35 600 −0.448 px (`--t-band`) | 24/30 | 28/37.8 Readex Pro | PASS |
| `.fronte__name` | letter-spacing −3.024 px = −0.03 em of its 100.8 px (`--track-display`) | −1.04 px (52 px) | −3.024 px | PASS |
| the account / error titles | `.conto .account-page__title` on `--t-title-2` (static, `test_the_numerals_are_the_sans…`); the login's `.entrance__title` 36/44 is the entrance's own rule (lane S's §9.8 exception 1, not LIB's) | | | PASS |
| `var(--f-mono)` in LIB's sheets | none (`grep` over the 23 sheets of §3.3 → 0) | | | PASS |
| mono still rendered on the pages (other lanes' rows, unchanged from round 1's m7) | `p.scheda-rail__titolo` (PUB1 `_sheet.css`), `p.traversata__kicker` (PUB1 `_training.css`), `span.dossier__num` (PUB1 `_diplomas.css`), `p.orienta__didascalia` (HOME `pages.css`), AGAMI's `dt` (PUB2 `_agami.css`); the Forum's eyebrow 13/20 500 (PUB2 `hero.html:17-19`, to go with AR's W1.2) | | | not LIB's — T's burn-down rows of those lanes |
| descendant-form `:lang(ar)` / `[dir="rtl"]` type rules in LIB's sheets | none (`grep` → 0; `_sezioni.css:147` and `_fronte.css:194-198` gone) | | | PASS |
| T's burn-down for LIB's sheets | rows `_sezioni` / `_sec-tracciato` / `_linea-v2` / `_servizio` deleted, `_fronte.css` → `{"clamp": 2, "uppercase": 1}` (the name device's two clamps by the letter; the folio label's uppercase until `_ingresso.html` — PX's file — carries `t-label`); `test_typography_v2.py` green (§6) | | | PASS (a lower equality, V5.20) |
| nothing under 14 px on phones among LIB's roles | labels 14/20, titles ≥ 24, numerals 28, the address 24 | | | PASS — the sub-14 texts the crawl lists at 390 are the lock-up's «™» (T's recorded exception), the portico's overlay caption (a preserved family) and Entreprises' form step tiles (`_steps.css`, the preserved forms) — none LIB's |
| Readex Pro fetched on `/ar/` only | every `/ar/` page fetches `v5-readex-pro-var-400-700-arabic.woff2`, no `/fr/` page does | | | PASS (T's guard, re-seen) |

## 5. Preserved families, locked copy, channels, strings, ownership, tools

- `git diff design-v5...HEAD --stat` over every §9.8 file and family — `partials/header.html`, `main_nav.html`, the portico, `chrome.css`,
  `_portico.css`, `lume.css`, `motion.css`, the forms (`_form*.css`, `_formwork.css`, `_glyph.css`, `_choice.css`, `_steps.css`),
  `templates/portal/**`, `apps/portal/**`, `templates/base.html`, `tokens.css`, `main.css`, `base.css`, `buttons.css`, `apps/cms`, `locale`,
  `apps/pages`, `templates/pages`, `templates/pathways`, `templates/ecosystem`, `templates/faq`, `templates/glossary`, `templates/forum`,
  `config`, `static/js` — **empty**. The navbar, mega menus, Lume, forms, privacy, terminology, the platform, the hero's first screen and
  the contact architecture are untouched by construction. The one §9.8-named file LIB touches, `_fronte.css` (the folio seals), is a
  named exception (§9.8 item 5) and in LIB's owned list (§3.3).
- **Locked copy:** `tests/compliance/test_locked_content.py` green (§6: the registry's French texts and checksums byte-identical); the
  RENDERED locked texts (`[data-locked]` elements' text) on ten pages — `/fr/`, `/fr/parcours/`, `/fr/parcours/salaried_work/`,
  `/fr/entreprises/`, `/fr/faq/`, `/fr/attention-aux-fraudes/`, `/fr/diplomes-et-titres/`, `/fr/formation/`, `/ar/`, `/ar/parcours/` —
  compared in process between 8786 (the lane) and 8780 (the preview): the same keys, identical digests on every page. The five
  template diffs add structure (`protezione__campo`, `protezione__davanzale`, `sez-fondale`), a class (`t-label`, `t-numeral`) and a
  verb switch — no string.
- **Both contact channels** on `/fr/contact/`: compared in process between 8786 and 8780 — 1 `tel:` href and 1 `wa.me` href on each,
  identical (digest `9eee7fa9bacb6e29` on both, the same as round 1's); never printed. `ILE_WHATSAPP_NUMBER` unset throughout.
- 0 new msgids, 0 JS, 0 images, 0 migrations (the diff holds no `.po`, no `static/js/src`, no model, no migration).
- Routes: the 57 `PublicRoute`s × fr / it / en / ar on 8786 → 228 requests, 216 × 200; the 12 non-200 are the three gated routes
  (`forum-virtuel`, `actualites`, `partenaires`, `requires_gate`) in four languages, 404 on the preview 8780 as well — not the lane's.
- Files outside §3.3's letter, both recorded in NOTES §4 / deviations 11–12: `apps/core/static/core/sezioni.css` (the fixtures' bundle,
  one `@import`) and `tests/frontend/test_typography_v2.py` (lane T's module: the rows the gate asks LIB to empty, and the Arabic page
  rows — a lower equality and a stronger guard; the steward records the slice). `components/photo.html` (PX's) untouched.
- **The tools, verified against the diff (V5.26 §4 — a tool use ends in a product change; R10 real names):** `impeccable` → the niche
  face on every T2 tile, the masked drafting grid (no side stripe, no frame), no glass / gradient text / blurred field → `_sezioni.css`
  §3, `_materia.css`, `_sec-strato.css` ✓; `taste-skill` Rule 4 → one raised plate, the band structured by the sill and the bookend,
  no second box → `protezione.html`, `_sec-strato.css` ✓; `figma:figma-use-motion` / `figma-implement-motion` → the raccordo's phases on
  the existing `draw-y` (`--sez-d: var(--motion-draw)`, the node the line's tip), the light one step after the rule
  (`--motion-slow` + the stagger), `--raccordo-x` the one parameter — and, this round, «validate one animation end to end» taken as the
  pixel proof: the span inside the band it enters, the twin reading the paint → `_materia.css`, `_sec-mosaico.css`,
  `test_materia_browser_v524_lib.py` ✓ (the product change is now VISIBLE — §2); `find-animation-opportunities` four-question gate →
  nothing animates in `_materia.css` of its own, the velatura still ✓; `ui-ux-pro-max` → the bookend stands down by the FIELD's free span
  (a container query, the system's own device in `_formwork.css`), not the viewport → `_sec-strato.css` ✓ (§3). No 21st component (R9);
  no «design-critique» / «design-handoff» named (R10). V5.26 §8 (the abstraction rule) respected this round: the light moved from the
  shell (bundled by every page sheet) to the pattern that has the behaviour (`_sec-mosaico.css`).
- **Contract items for the other lanes** — present in NOTES §4: (a) T's contract applied, (b) PX's credit rules deleted (13 rules, five
  partials), (c) the material contract HOME / PUB1 / PUB2 build against — the attributes, the class with its two modifiers, the
  **first-child-of-the-entered-band placement**, `--raccordo-x`, `--sez-raccordo` for a panel-head landing, the node's colour note (m4 of
  round 1), the import order; the requests to PUB1 (`t-label` / `t-numeral` on the board, the «Comment ça marche» plates' `ink` + the
  three light rules in `_index.css`), HOME (the colophon's `t-label`, the S6 import), PUB2 (`_projet.css:172`), CLOSING (five items),
  the steward (the family's `owns`). Complete for the merge.

## 6. Tests run on the committed head (database `test_ile_v524_lib`, one pytest at a time; the headless twins on `test_ile_v524_libq`; logs under `C:/tmp/ile_v5_council/.work/v524-lib/logs/qa2_*.log`)

| Run | Modules | Result |
|---|---|---|
| `qa2_static.log` (02:07:22 → 02:27:03, `-m "not browser"`, 1 610 collected) | `test_materia_v524_lib.py` (the lane's static module, 15), `test_sezioni_v522_s.py` (lane S's library module with the re-recorded mosaico ceiling), `test_rm_flag_parity.py` (untouched), `tests/i18n/test_rtl_static.py`, `test_frontispiece_v515_c.py` (every page type under its §7.1 total — **the home 61 415 ≤ 61 440**), `test_pages_v522_p1.py` (the route sheets' ceilings), `test_typography_v2.py` (T's burn-down with LIB's rows emptied, the Arabic page rows), `test_v5_tokens.py`, `test_fonts_budget_v2.py`, `test_design_docs.py`, `test_static_pipeline.py` (**`collectstatic` under the production storage exits 0** — the builder's 0xC0000142 was the harness's interruption, not the product), `test_css_bundle_is_current.py` (the committed dist = the build), `tests/compliance/test_locked_content.py` (76: the French texts and checksums byte-identical), `test_imagery_credits_v524.py`, the neighbours `test_sezioni_v522_s2.py`, `apps/pages/tests/test_interior_v522.py`, `test_chapter_marks.py`, `test_layout.py`, `test_motion_v512_a_w2.py`, `apps/pages/tests/test_home_v522_h.py`, `test_home.py`, `apps/pathways/tests`, `tests/test_check_ownership.py` (**the four subprocess cases green** — the builder's errors were the same interruption) | **1 failed / 1 603 passed / 6 deselected** — the one: `test_home_v522_h.py::test_final_round_the_arabic_titles_stand_against_their_glyphs_and_the_connector_on_its_rule` (`re.search('--t-folio-lh: 1rem;', tokens.css)` → None: T's alias) — **red on `design-v5` `554c82d2` already** (round 1's control run `qa_base_control.log`; m2), lane H's module, not LIB's |
| `qa2_browser.log` (headless, no slot, `test_ile_v524_libq`, 02:21:31 → 02:37:15, after the headed session) | `test_materia_browser_v524_lib.py` (the lane's twin, 14: the raccordo at 1440 and 390 fr/ar incl. the paint, the bookend at 1440 / 1024, the incastro, the mosaico verb, `reduce` and the keyboard), `test_sezioni_browser_v522_s.py` and `test_seal_heads_browser_v522_s.py` (lane S's library contracts, LIB-owned, unchanged), `test_sezioni_browser_v522_s2.py` (the 16 cases the builder's run lost to «Connection closed while reading from the driver»), `test_pages_browser_v522_p1.py` (incl. the four cases that `Target crashed` under the builder: the pilot doors' calls, the campus frame fr/ar, the companies' three moments), `apps/pages/tests/test_home_browser_v522_h.py` (incl. **`test_the_hero_line_runs_down_into_the_orientation_seal_sill[fr/ar]` — B6**) | **5 failed / 124 passed** — the five are round 1's m2, red on the base already and unchanged: `test_the_institutions_head_…[fr/ar]` (`16 ≤ 15.5` at 390, T's phone step-up of the ui role) and `test_final_the_arabic_index_s_titles_…[1440/1280/1024]` (the connector `centre −2` in Arabic, T's 14/20 Arabic label). Lane P1's and H's modules, for the steward / CLOSING under V5.20. **Every LIB-relevant case green**, the hero-line junction among them |
| `ruff check` on the four touched test modules, then `ruff check .` over the whole tree | | 0 · «All checks passed!» |
| the steward's merge checks run ahead (R13): `manage.py check` · `makemigrations --check --dry-run` · `tests/security/test_confidential_material.py` in-process with `ILE_CONFIDENTIAL_SENTINELS` | | 0 issues · «No changes detected» · 17 passed (no value printed) |
| the headless sill probe (`scratchpad/sill_probe.py`, the pietra fixture with a spacer, fr and ar) | | the sill `scale 0 1` in `wait`; on the trigger `sez-draw` with `animationDelay 0.9s` (the soglia's 0 s) → after the soglia; after 3 s nothing running, `scale: none` |

The builder's in-flight sets (`imp_static_set.log` 2 failed / 1 444 passed / 4 errors; `imp_browser_set.log` 9 failed / 90 passed / 16 errors) are
explained by this round: the static reds beyond m2 were `0xC0000142` subprocess launches and the browser reds beyond m2 were
`Target crashed` / `Connection closed while reading from the driver` (three Chromium loads at once under the harness's close) —
every one of those cases is green here on the committed head, run one Chromium at a time.

## 7. Budgets (gzip -9; the partials minified alone with the repository's esbuild; the dist as committed = as built; before = `554c82d2`)

| Sheet | Before | After (reviewer's measure) | Ceiling | Verdict |
|---|---|---|---|---|
| `_materia.css` (new) | — | **788** | ≤ 800 (§3.3) | PASS |
| `_sezioni.css` (the shell) | 2 444 | **2 382** | 2 382 (recorded at the measure, `test_materia_v524_lib.py`; the audited 2 444 + 45 never reached) | PASS (− 62: the light out of the shell — B1 closed) |
| `_sec-strato.css` | 1 423 | **1 557** | 1 638 (unchanged) | PASS (+ 134 ≤ the audited ≈ 160) |
| `_sec-mosaico.css` | 1 203 | **1 355** | **1 355** (1 229 re-recorded at the measure, R4 f, cited in `test_sezioni_v522_s.py` and `test_materia_v524_lib.py`) | PASS at its new letter — m1: + 152 against the audited «≈ 120» (≈ 1 323); every spelling the reviewer tried measures 1 349–1 355 (the state rules unscoped 1 353; without `border-radius: inherit` 1 349, a corner change) — the audited figure was an estimate, nothing removable without a design change; no route sheet and no page total moves past its ceiling |
| `_sec-tracciato.css` · `_sec-filo.css` | 1 418 · 999 | 1 420 · 1 012 | 1 434 · 1 024 | PASS |
| `_linea-v2.css` | 1 618 | 1 622 | the passage increment ≤ 1 229 | PASS |
| `_fronte.css` · `_servizio.css` | 5 637 · 2 426 | 5 507 · 2 388 | — | − 130 · − 38 |
| `_photo.css` · `_compose.css` · `_sec-mappa.css` | 1 174 · 1 212 · 1 320 | 1 071 · 1 199 · 1 307 | the panorama increment ≤ 716 | PASS (the credit rules) |
| **`main.css` (dist)** | 32 695 | **32 695** | ≤ 32 716 (R4 c) | PASS — untouched by construction (imports none of the partials) |
| `pages/css/pages.css` · `hero.css` · `core/reveal.css` · `core/portico.css` | 11 306 · 10 899 · 3 526 · 2 993 | **11 302** · 10 899 · 3 526 · 2 993 | 12 288 · 11 264 | **the home 32 695 + 11 302 + 10 899 + 3 526 + 2 993 = 61 415 ≤ 61 440** (the base 61 419; round 1's 61 470 was B1 — closed) |
| `pathways/index.css` · `sheet.css` · `training.css` · `diplomas.css` | 10 117 · 9 701 · 8 788 · 8 895 | 10 188 · 9 695 · 8 843 · 8 950 | 10 240 · 10 240 · 9 728 · 9 728 (P1's, R4 b) | PASS |
| `ecosystem/pilot.css` · `companies.css` · `institutions.css` · `universities.css` | 9 508 · 8 701 · 8 381 · 7 630 | 9 477 · 8 708 · 8 368 · 7 504 | 9 728 · 9 216 · P1's · 8 448 | PASS |
| `pathways/pathways.css` · `ecosystem/ecosystem.css` | 4 716 · 4 977 | 4 621 · 4 886 | 11 264 | PASS |
| `pages/css/fronte.css` · `interior.css` | 6 141 · 8 827 | 6 009 · 8 873 | — · 11 264 | PASS |
| `cms/lettura.css` · `servizio.css` · `errori.css` · `forum/forum.css` | 6 512 · 2 879 · 3 647 · 7 369 | 6 546 · 2 838 · 3 609 · 7 303 | 9 216 · — · — · 8 192 | PASS |
| `core/sezioni.css` (the fixtures' bundle) | 11 308 | 11 759 | none (by design, m8 of round 1) | — |

Every figure above equals the builder's NOTES §6 to the byte (the stale figures of round 1's m3 are gone). The page-type totals are
asserted by `test_frontispiece_v515_c.py` (§6): no total moves past its §7.1 letter; the home at 61 415.

## 8. Round 1's six blockers, re-verified

| # | Round 1 | The builder's answer (NOTES §10) | Re-verified this round | Status |
|---|---|---|---|---|
| B1 | the home 61 470 > 61 440 (the light in the shell) | the three light rules → `_sec-mosaico.css` scoped `.mosaico .sez-tile::before`; `isolation` folded into `.sez-tile`; `font-feature-settings` out of the label net | the shell 2 382 (− 62 against the base), `pages.css` 11 302, **the home 61 415 ≤ 61 440** by the reviewer's own gzip; `test_frontispiece_v515_c.py` green (§6); the light plays from the mosaico sheet (§2) | **CLOSED** |
| B2 | the raccordo never painted (`.sez` isolates; the protrusion under the next ground) | fix B: the span the FIRST CHILD of the band it enters, `inset-block-start: 0`; the fixture, the twin (reads the paint), COMPONENT_PROVENANCE, NOTES §4 (c) updated | the line's column 193 against 235 in six cells and under `reduce`; the node on the head rule at 0.0 px; the stills show the line (§2) | **CLOSED** |
| B3 | the shield behind the plate at 1024 and on the sheets | `container-type: inline-size` on the field + `@container (max-width: 67.999rem) { .sez-fondale { display: none } }`; the 63.999 rem media gone | 1024: `display: none` on Parcours, Formation, Diplômes, the home (field 929 / 945 px); the sheets: `none` at 1440 and 1024; 1440 on the wide pages: the shield beside the plate, `overlap False` in fr and ar (§3) | **CLOSED** |
| B4 | the incastro inert (the band's padding sank the first door 32 px under the seam) | `.sez[data-incastro] { padding-block-start: 0 }`; the twin asserts ≥ 63 px | `doorOverAbove 64` in six cells; the stills (§2) | **CLOSED** |
| B5 | the two new modules red (the `_rule` reader, the clamp count, the band selector, the 390 trigger, the rm loop) and ruff F841 | `_rule` reads outside at-rule blocks, `font-size: clamp(` counted, the entered band by its attributes, `wait_for_function` (no timeout raised), the rm loop ends on the raccordo page, a pixel assertion added, a 1024 case added | both modules green on the committed head (§6); `ruff check` clean; the pixel assertion would now catch B2 (it reads the paint) | **CLOSED** |
| B6 | the home's hero line 4 px off the orientation seal's sill (the numeral role's 40 px leading grew the linea's first row) | the across numeral `font-size: var(--t-numeral-lg); line-height: 1` (36 in a 36 px row) and both `calc()`s on `--t-numeral-lg` | `lineBottom − sealBottom` **0.0** at 1440 and 1024, fr and ar (`home_*_orientation.png`); lane H's `test_the_hero_line_runs_down_into_the_orientation_seal_sill[fr/ar]` green (§6); the across numeral 36/36 600 | **CLOSED** |

Round 1's minors: m1 moot (the light left the shell); m2 the base's reds (re-seen in §6, unchanged, not LIB's); m3 the NOTES refreshed (§6–§8, §10 filled,
the figures equal the measures); m4 recorded as a placement note in NOTES §4 (c); m5 taken; m6, m7 carried (below); m8, m9 by design.

## 9. Discipline record

- `CHROMIUM_LOCK_A` free at 02:05 (slot B free; the merge lock `DESIGN_V5_MERGE_LOCK` from the T merge not mine, left as found); taken
  under `v524-lib-qa2` at 02:11:03 (noclobber, label + time) and released at 02:21:23 (10 min 20 s ≤ 25 min; 200 frames). The headless twins ran after the
  headed session, never beside it (the builder's browser set had lost 16 + 4 cases to a Chromium crash when three Chromium loads ran at
  once — §6).
- Lane server 8786 started by the reviewer at 02:06 on `ile_v5_l5` from the committed head and **stopped at 02:28** once the headed
  session, the route sweep, the channel / locked-copy comparison and the sill probe were done (pid 20952 and its launcher 30232;
  8786 free, the preview 8780 untouched — pid 8004). The headless twins run on pytest's own live server and needed it no more.
- `PYTHONIOENCODING=utf-8`, `ILE_READ_ENV_FILE=0`, `ILE_WHATSAPP_NUMBER` unset, `ILE_CONFIDENTIAL_SENTINELS` read in-process by the guard
  only; no private value printed; the contact digests only.
- Scratch (nothing in a repository): `~/AppData/Local/Temp/claude/C--tmp-italylegalentry/0557441a-c48d-44fe-a67b-6577308c9f96/scratchpad/lib_qa2_headed.py`;
  the logs `.work/v524-lib/logs/qa2_*`.

## 10. Findings

**Blockers:** none. The six of round 1 are closed by measure (§8); every gate item of §3.3 holds (§1–§5, §7); no test was loosened
(§1); every budget holds with `main.css` at 32 695 ≤ 32 716 and the home at 61 415 ≤ 61 440 (§7); no preserved family moved (§5);
every tool use ended in a visible product change (§5); the contract items for HOME / PUB1 / PUB2 / CLOSING / the steward stand in
NOTES §4.

**Minors (recorded, not blocking):**
- m1 `_sec-mosaico.css` is re-recorded at **1 355**, + 152 B against the audited «≈ 120» (≈ 1 323): R4 f allows the re-recording «at
  measure + the audited increment, cited» and the builder cites it (deviation 4) with the reason — the audited figure was an estimate
  made against the shell's neighbours; the reviewer measured every spelling (1 349–1 355) and found no declaration to drop without a
  design change (the layer's corner). Within R4 f's letter as a recorded deviation; the steward records it in the DL entry; CLOSING's
  ratchet pass re-records it at the measure again if PUB1's `_index.css` copy changes nothing here.
- m2 Red on `design-v5` HEAD already, before this lane (lane T's merge): `apps/pages/tests/test_home_v522_h.py::test_final_round…`
  (the `--t-folio-lh: 1rem` literal, now T's alias), `test_home_browser_v522_h.py::test_final_the_arabic_index_s_titles_…` × 3 (the S3
  connector 2 px under the Arabic label's 20 px line) and `test_pages_browser_v522_p1.py::test_the_institutions_head_…` × 2 (16 px on a
  phone where the test caps at 15.5 — the public step-up). Lane H's and P1's modules; the steward / CLOSING re-point them under V5.20
  (the same invariants on the new tokens). Not LIB's — verified by round 1's control run on the base and unchanged here.
- m3 (round 1's m6) `fronte-halo` runs at rest on the frontispieces (Parcours at 1024, Formation and the FAQ at 390, AGAMI, Entreprises
  at 1440; `restAnimations` in `qa2_measures.json`): the head motif's own light, pre-existing on the base, in `_fronte.css` (a §9.8
  named exception, lane S's V5.22 composition). Outside LIB's tables (R14): recorded for the matrix's «0 animations at rest» item and
  CLOSING — a post-acceptance candidate, not fixed here.
- m4 (round 1's m7) The mono still rendered by other lanes' seats — `p.scheda-rail__titolo` (PUB1 `_sheet.css`), `p.traversata__kicker`
  (PUB1 `_training.css`), `span.dossier__num` (PUB1 `_diplomas.css`), `p.orienta__didascalia` (HOME `pages.css`), AGAMI's `dt` (PUB2
  `_agami.css`), the Forum's eyebrow at 500 (PUB2) — and the Forum's caps h1 at 36/44 (`forum/_forum.css`, PUB2) are those lanes' rows
  of T's burn-down; LIB's sheets hold none.
- m5 Under 14 px on the public pages, none LIB's: the lock-up's «™» (T's recorded exception), the portico's eyebrow / kicker at 12 px
  and its overlay caption at 13 px on phones (the navbar, a preserved family — T's `_portico.css` / `chrome.css` rows), Entreprises'
  form step tiles at 12 px on phones (`_steps.css`, the preserved forms), the hero's station labels at 12 px on the Arabic home at
  1024 (HOME's `hero.css` row of T's burn-down). Recorded for those lanes / the matrix.
- m6 The incastro's contract lifts the band's FIRST content 64 px: on Le projet the first child of `.projet-porte` must be the doors
  themselves (no head between the raised edge and the arches) or PUB2 places the head inside the band after the doors — a placement
  note for PUB2, written in NOTES §4 (c)'s spirit; the primitive is right by the audit's letter («the doors' arched tops rise»).
- m7 The pietra fixture band (`fx_pietra-*`) is in view at load, so the headed pass read its entrance at rest; the sill's draw after
  the soglia was proven by the headless probe with a spacer (§6). A fixture with a spacer would let the twin assert the delay too —
  a test-strengthening candidate for CLOSING, not a defect.
- m8 `apps/core/static/core/sezioni.css` (the fixtures' bundle, 11 308 → 11 759 B) has no ceiling — by design (round 1's m8).
- m9 Two files outside §3.3's letter (the fixtures' bundle, T's test module slice) — recorded by the builder (deviations 11–12); the
  steward records the slice in the family's manifest entry.

## 11. Scores (the gate's measured surfaces; 4 where a dimension is not applicable, said so — no composition change in this lane, R9 / V5.25 §5)

| Surface | Composition | Motion | Imagery | Interaction | Institutional | Coherence | Note |
|---|---|---|---|---|---|---|---|
| the specimen board (pietra, carta viva, velatura, raccordo, incastro, mosaico, the niche) | 4 | 4 | 4 (n/a: no photograph; the grid's lead) | 4 (n/a) | 4 | 4 | every recipe and primitive as the audit decided, mirrored in Arabic, still under `reduce` and from the keyboard; the raccordo now reaches the eye (painted, on the head rule) and the incastro overlaps — round 1's two under-4 dimensions are at the bar; a library board is no page composition (R9) |
| «la protezione» on Parcours, the sheet, Formation, Diplômes, the home | 4 | 4 | 4 (n/a) | 4 (n/a) | 4 | 4 | the drawing table reads at 1440 in fr and ar (sill, bookend at 30 %, nothing over the plate); at 1024 and on the sheets the bookend stands down and the sill alone runs on; the plate's locked text byte-identical |
| the type roles in the library (heads, frontispieces, numerals, keyword, address, name device, account / error titles) | 4 | 4 (n/a) | 4 (n/a) | 4 (n/a) | 4 | 4 | every measured role on the twelve steps, Arabic through the tokens, no mono, no clamp outside the letter's two, nothing under 14 px on phones among LIB's roles; the home's hero-line junction restored (0.0 px) |

No composition changed in this lane (R9 / V5.25 §5): the pages' merge scores stand; the lane passes on its gate items.
