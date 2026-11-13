# Lane T — Typography V2 · the reviewer's gate (label `v524-t-qa`)

5 November 2026, 21:30–22:00. Senior design-engineering review of branch `v524-t` (worktree `C:/tmp/ile_wt/v524-t`, head
`aeea4fe4e2633148046c67610c05704e5bedef73`, one commit over `design-v5` `4bafcfa0` = tag `v522/p2`), against
`FINAL_DELIVERY_V2.md` §3.1's gate (items 1–6, targeted per V5.25 §2), R1, R4, R7, R12, R14, V5.20's strict test rule,
SECTION_SYSTEM_V2 §9.7/§9.8, and the four audits. Builder's record: `docs/design-v5/QA/v524/t/NOTES.md` (on the branch).

**Verdict: PASS — 0 blockers, 8 minors (recorded below; none requires a change before the merge).** Every gate item holds on
measures the reviewer took independently (own probes, own headed session, own swap-CLS run on 8782); the builder's figures were
reproduced, not copied.

Machine discipline (R12): lane server 8785 on `ile_v5_l3` (migrations in step, `migrate --check` 0); pytest on
`test_ile_v524_t`, one at a time; headed Chromium under `CHROMIUM_LOCK_A` 21:44:29 → 21:51:15 (6 min 46 s); headless probes
without a slot; 8782 switched to this tree under `PERFORMANCE_BENCHMARK_LOCK` (collectstatic from `v524-t` into
`evidence/v54/static-8782`, the persona session minted under `settings_8782` and deleted after the run), used for the swap-CLS
cells alone, stopped again (it was down before); both lane servers stopped and both locks released at the end; the worktree
clean (`git status` empty, HEAD unchanged). Nothing pushed, tagged, merged or deployed. The configured channels were compared in
process and are not written here.

Reviewer's tools (all outside the repository): `.work/v524-t-qa/tools/qa_probe.py` (fonts · type · motion · hero · channels ·
axe), `qa_headed.py` (the eye, 44 frames + metrics), `qa_cls_swap_8782.py` (the W1-A method), `run.sh` (pytest on the lane
database); logs under `.work/v524-t-qa/logs/`; JSON and stills under `evidence/v524/t/qa/`.

---

## 1. Gate items (FINAL_DELIVERY_V2 §3.1)

### (1) Tests green; the burn-down table equals the measured counts — HOLDS

| Run (log) | Modules | Result |
|---|---|---|
| `static1.log` (non-browser, `test_ile_v524_t`, 8 min 49 s) | `test_v5_tokens.py` · `test_typography_v2.py` · `test_fonts_budget_v2.py` · `test_design_docs.py` · `tests/i18n/test_catalogues.py` · `tests/i18n/test_rtl_static.py` · `tests/frontend/test_layout.py` · `test_css_bundle_is_current.py` · `test_frontispiece_v515_c.py` · `tests/compliance/test_locked_content.py` · `tests/compliance/test_public_pages.py` · `tests/security/test_confidential_material.py` (with `ILE_CONFIDENTIAL_SENTINELS`, values never printed) | **1 098 passed, 0 failed, 0 skipped** (2 browser tests deselected) |
| `browser1.log` (headless Chromium through pytest, no slot) | `test_browser.py::test_fonts_are_self_hosted_and_loaded` · `test_rtl_browser.py::test_arabic_typefaces_are_applied_and_loaded` · `test_typography_v2.py -m browser` (1440, 390) | **4 passed** |

The burn-down table is an equality test over 45 listed sheets and every unlisted one (`test_the_burn_down_table_equals_the_measured_counts`,
parametrised over `static/css/v5/**` and `apps/*/static/**`): green means no sheet listed that is clean, none clean that is
listed. The counting logic was read: clamp/min/max font-sizes, literals outside the scale, `var(--f-mono)` outside the
reference classes, descendant-form `:lang(ar)` / `[dir="rtl"]` rules writing a type property, `text-transform: uppercase`
outside the label role and the locked-caps classes — sound; the allow-lists are narrow. Also: `ruff check .` 0, `manage.py check`
0 issues, `makemigrations --check` no changes.

### (2) Fonts — HOLDS

- Shipped set **61 140 B** in six files (≤ 62 000); Readex Pro 16 128 (≤ 18 000), Host Grotesk 19 208 (≤ 22 000), italic
  14 096 (≤ 15 000), mono 2 688 + 7 272 = 9 960 (≤ 10 000), wordmark 1 748 (≤ 2 000).
- FONTS_V5 §1 bytes and SHA-256 in step with the files (Readex Pro `9669ea48c988…ec0e`; the other five unchanged, hashes checked);
  the licence `OFL-ReadexPro.txt` LF, the Reserved Font Name declared and unused.
- Fetched on the lane (encoded bytes, `qa/fonts.json`): `/fr/` login · contact · Le projet 20 956 B; home · Parcours · FAQ · AGAMI
  30 916 / 23 644 / 23 644 / 30 916 (the mono labels of LIB / HOME / PUB rows); the person dashboard and the case file 23 644
  (the mono core for the reference seat `.ctx__ref`, ≤ 24 000); `/ar/` 37 084 B on login · contact · Le projet, 39 772 on
  dashboard · case file · AGAMI (≤ 40 000 console; AGAMI's 39 772 is the mono row of PUB2), 47 044 on the home (recorded in the
  browser slice as a never-up figure). **Readex Pro fetched on every `/ar/` page and never on a `/fr/` one; no Vazirmatn file,
  face, stack, preload or licence anywhere** (`grep -ril vazirmatn static/fonts static/css/v5/fonts.css static/css/v5/tokens.css
  templates` → 0; the word survives only in comments of three non-T sheets, the «retired» lists of tests and historical notes —
  CLOSING's item b).

### (3) The eye — HOLDS (headed `chromium-1234`, 1440 · 1024 · 390 × fr · ar, nine pages; stills `qa/shots/`, metrics `qa/headed_metrics.json`)

- **Display weight and tracking.** Every `h1` that reads the tokens is 600 at −0.028 em: FAQ `h1.page-header__title` and the
  `ingresso__title` of Le projet, AGAMI, Contact 56/60.48 at 1440, 34/36.72 at 390; the login's 36/44 600; the console's
  `ctx__title` 34.72 (`--u-title-lg`) 600. The hero's statement `.he__promise` is still **500 / −0.028 em** (hero.css's literal —
  HOME's «type» row, §3.4): at 1440 fr the first screen is pixel-identical to the base. The AGAMI name device keeps its own 700.
- **One label per head at 13 / 14 px in the sans.** The label role is live where its classes are read: `.atrium__eyebrow` Host
  Grotesk 12/16 600 +0.08 em (13/20 on phones), the V1 folios, the console eyebrows; in Arabic 14/20 Readex Pro, no capitals, no
  tracking. The library's heads still carry their own labels — `.testa__label` ILE Mono 13/16 400, `.ingresso__label` 12 px literal,
  the FAQ category «GÉNÉRAL» in the mono — the LIB / PUB rows of the burn-down, as §3.1 defines them.
- **Numerals in the sans.** The console's step chips («Étape 1 sur 7», «الخطوة 1 من 7») Host, tabular; the Parcours route's
  `.tracciato__num` still ILE Mono 20 px (PUB1 / LIB rows).
- **Arabic parity beside the French plates.** Readex Pro at the French's size and colour on every page: the nav 15/20, the CTA
  16/24 600, the entrances' titles against their French descriptions, the FAQ's Arabic lead with the brand isolate on one line
  (M1), the case file's «إجراؤكم التالي» head against «Diplôme ou titre de formation» in Host at 20/28; the Western digits sit
  on the Arabic line (`EE167596D4`, `21.09.2026`, `1 من 7`). Body 17/28 (`test_rtl_browser` asserts it).
- **Descenders.** 0 clipped Arabic text in overflow-hidden boxes on the nine pages at 1440 / 1024 / 390 (the probe's Range-vs-clipper
  test over every Arabic text node); the navbar words, the status chips («للاستبدال», «أنت هنا»), the primaries, the rail — clean.
- **French runs on `/ar/` at Latin leading.** The locked statement, the entrances' descriptions, the FAQ's questions, the case
  file's requirement titles — Host at 1.08–1.47. Remaining exceptions, all page-lane rows: `h2.racconto__titolo` 24/32 (Le projet),
  the `_fronte.css` / `_sezioni.css` descendant rules; and one caveat of the method itself (minor 3 below).
- **Nothing under 14 px on phones.** Over every visible text node of the seven public pages at 390 in fr and ar: the only
  element under 14 px is the lock-up's «™» glyph (`span.lock__tm`, 7.7 px — the brand drawing, not reading text); login labels
  14, help 16/24, footer headings 14, station labels 14, the primary 17/24 600. The console keeps 12–13 px (`console-bottom`,
  `atrium__eyebrow` 13) by F-13 as recorded.
- **The swap on 8782** (`qa/cls_swap.json`, the W1-A method, fonts held 1.5 s, 12 cells): worst matched **0.0015** (home 390),
  every cell 200, Readex Pro loaded on every Arabic cell; bare (overrides stripped) up to 0.0039 — the recomputed fallback is
  load-bearing. ≤ 0.01 holds.
- Also measured: **overflow 0** (`scrollWidth ≤ clientWidth`) and **0 console / page errors** on 54 loads (9 pages × 3 widths × 2
  languages); the navbar's mega menu identical on base and lane (panel 100,72 · 1240 × 346, six 77 px entries, fr and ar;
  Readex Pro 17/24 500 in Vazirmatn's place) and the phone sheet identical (390 × 844, 34 links, 36 px minimum target, no
  overflow) — the preserved family not regressed (`qa/navbar.json`, `qa/shots/mega_*`, `sheet_*`).

### (4) The hero's first screen against the base — HOLDS on its substance, with the letter amended (minor 1)

Reduced motion, fonts loaded, lane 8785 vs base 8780, 167 / 139 elements compared (`qa/hero.json`, `qa/hero_*.png`):

| Cell | Moved | Resized | Pixels | What |
|---|---|---|---|---|
| 1440 fr | **0** | 0 | **0.0 %** | identical (the name's `h1` computes −0.028 em instead of −0.024 through `--track-title`: 0 visible pixels) |
| 390 fr | 3 | 3 | 4.1 % | the secondary link's text 15 → 16 (its 44 px box unmoved, the arrow 9 px further), two station labels 13 → 14 px wider by 4–9 px without moving, the CTA 15 → 16 at 500 — the phone step-up through `--t-ui` / `--t-folio` (R1); no block anchor moved |
| 1440 ar | 25 | 0 | 1.2 % | text-sized boxes follow Readex Pro's advance widths: the CTA 218 → 235 px wide (its left edge 17 px), the secondary 30 px, «المغرب» 6 px, the origins' arrows 6–14 px; the statement, the door, the nodes, the panels unmoved |
| 390 ar | 17 | 0 | 2.3 % | the same, plus the origin words 4–9 px wider |

The composition and its anchors are unchanged; the deltas are the two token-level decisions R1 adopts (the face at ratio 1.0,
the phone step-up) reaching the text boxes the hero reads through the tokens. The item's «weight and tracking only» cannot be
met at 390 and in Arabic without contradicting item (3) «no text under 14 px on phones» and R1's face.

### (5) The Arabic reader's exhibit — RECORDED
`C:/tmp/ile_v5_council/.work/v524-audit/v524-typo/shots/compare_1600.png` (copied to `evidence/v524/t/compare_1600.png`:
Host Grotesk beside Vazirmatn, Readex Pro, Alexandria and IBM Plex Sans Arabic at one size, with the content-area / tooth /
alef figures) + the Arabic home stills `evidence/v524/t/qa/shots/home_ar_1440_0.png`, `home_ar_390_0.png` — owner item B2.

### (6) `main.css` — HOLDS
Two `npm run build` with the installed packages: identical, `git status` empty (the committed dist is the build); only
`static/css/dist/main.css` differs from `design-v5` in dist. **32 695 B gzip -9** (Python `gzip.compress(…, 9)`) against the
base's 32 716 — the ratchet holds with 21 B of air; no ceiling raised anywhere (`test_frontispiece_v515_c.py` green).

---

## 2. The other conditions of the lane's pass

- **Every tool use ended in a real coherent product change (V5.26 §4; R10).** NOTES §3's table was checked against the product:
  impeccable `typography.md` / `typeset.md` → the four fluid steps bounded 1.45 ×, eight fixed, display 600 (visible on every
  token-reading title), the recomputed fallback (visible in the bare-vs-matched CLS); taste-skill Rule 1 / §7 → title-1 capped at
  56, the label role as the structural device (`.t-label, .eyebrow` in base.css, live on the console eyebrows and V1 folios);
  ui-ux-pro-max `google-fonts.csv` → the build recipe's axes and subset (the shipped 16 128 B file, no digits, no Latin); fontTools →
  the reproducible file and the fallback metrics. No collage, tokens only (the diff is tokens, roles, four rules and one weight),
  no component. The real tools are named by path in NOTES §3 (R10, V5.27 §6).
- **Preserved families (§9.8).** `tokens.css` and `base.html:24–32` are the recorded typography exception (R1); the navbar, the
  mega menus and the phone sheet measured identical; the forms' typed text 16 px; Lume untouched; contact and privacy templates
  untouched. The diff touches no page sheet, no library partial, no `main.css` import, no JS, no string, no image, no migration.
- **Locked copy byte-identical.** `tests/compliance/test_locked_content.py` green (checksums); the diff carries no template text.
- **Both contact channels unchanged.** `/fr/contact/`, `/ar/contact/` and the home's footer: the `tel:` and `wa.me` hrefs on the
  lane equal the base's, both kinds present (compared in process, `qa/channels.json` holds booleans only).
- **No test loosened.** Each re-pointed expectation cites V5.20's four conditions (V5.24 §11–§14 / TYPOGRAPHY_V2 §4 / R1) and
  holds the same or a stronger invariant: the scale test now pins twelve values at two viewports; the floors test adds the label
  and the Arabic block's form; the console step-up test is stronger (eyebrow 13); the two browser slices add the bytes fetched,
  the face file and the body's size and leading; the per-page figures 30 916 / 47 044 are measured values to burn down, under the
  audit's previous figures, never ceilings raised. The V1 mono re-pointing block of base.css lost its `font-family` line: verified
  that no sheet seats the mono on those six classes (the only `--font-ref` consumer left is V1's `code, kbd, pre, .t-ref`), and
  the footer headings draw Host Grotesk on every page.
- **Reduced motion / keyboard / axe.** Reduced motion: 0 running animations, 0 `data-sec-state` on home, Parcours, login (fr, ar,
  1440, 390). One Tab sets `html[data-input="key"]` with the skip link focused; the animations in flight after the Tab are the
  section verbs started by the scroll-through and are identical on base and lane (39 → 4 at rest, both trees). axe-core 4.10.2
  (WCAG 2.0/2.1 A + AA) on home, login, the dashboard and the case file × fr/ar × 1440/390: **0 violations** in 16 runs.
- **Contract items for the other lanes written in NOTES §4** (the token names, the subject form, the burn-down rows per lane,
  the requests to HOME / LIB / PUB1 / PUB2 / PLAT / CLOSING / steward) — present; one caveat to add (minor 3).

---

## 3. Findings (all MINOR; none blocks the merge)

1. **Gate (4)'s letter vs. the measured hero (390 and Arabic).** Only text-sized boxes change, by the adopted step-up (fr 390:
   +4 … 9 px widths, the secondary's arrow 9 px) and by Readex Pro's advance widths (ar 1440: the CTA 17 px wider, the secondary
   30 px); block anchors unmoved; 1440 fr pixel-identical. *Fix:* the Director records the amendment for HOME's gate (3) — «block
   anchors ≤ 1 px; text boxes follow the adopted step-up and face» — rather than HOME restating the hero's own 15 / 13 px at 390
   (which would put 13 px text back in the phone hero against V5.24 §13). Not T's change to make.
2. **The hero's statement is still 500.** The owner's §1 promise «the hero's statement no longer the lightest text» does not arrive
   through T: `hero.css` sets `.he__promise` 500 / −0.028 em literally (HOME's «type» row and burn-down `hero.css` 3·3·0·0·4).
   *Fix:* HOME applies `--t-display` / `--w-display`; the steward's live_status wording for Typography V2 says «through the tokens
   where the sheets read them» until HOME merges.
3. **F-7's boundary is token-deep, not inheritance-deep.** The Latin boundary restores the Latin leading only on the element that
   carries the `line-height` declaration (or its descendants). Where a sheet declares the leading on an Arabic ancestor of a
   `lang="fr"` run (Le projet's statement: `_sec-racconto.css:81` `line-height: var(--t-lead-lh)` on the wrapper; the French
   `span.ls` and `p` inside compute 20/32 = 1.6 at 390, 22/32 = 1.455 at 1440), the French inherits the computed Arabic leading.
   *Fix:* one paragraph in NOTES §4's contract: «put the type declaration on the lang-bearing element, or write the subject form
   on it»; add the statement to `ARABIC_PAGES_BURNDOWN["/ar/le-projet/"]`'s reason (today it names `.racconto__titolo` only).
   The page is already a burn-down row (PUB2 / LIB).
4. **NOTES §5 and §7.1 overstate the console's font figure.** «The persona pages fetch no mono at all (20 956 / 37 084)» holds
   for the need form only; the dashboard, the case file and documents fetch the mono core for the reference seat: 23 644 /
   39 772 B — within the ceilings 24 000 / 40 000 (the builder's own `probe/fonts.json` says so). DESIGN_SYSTEM_2026 §6.3 repeats
   the 20 956 for the console. *Fix:* correct the two figures in NOTES and the §6.3 sentence (docs only; no ceiling moves).
5. **Ownership slices outside §3.1's list** — `tests/frontend/test_layout.py` (fonts slices), `tests/i18n/test_rtl_static.py` (one
   test), `templates/errors/standalone.html:26`, `templates/base.html:24–27` (comment), `DESIGN_SYSTEM_2026.md` §2 rows 11 / 14 and
   the §3 `--t-numeral-lh` cell — each recorded with its reason in NOTES §4 (a red `design-v5` at T's merge otherwise; the first-lane
   rule as PX's). *Fix:* the steward records them as slices of family `v524-t` in `OWNERSHIP_V54.json` (R11); nothing for T.
6. **A documentation path.** DESIGN_SYSTEM_2026 §6 cites `evidence/v524/.work/v524-typo/shots/compare_1600.png`; the exhibit is
   `C:/tmp/ile_v5_council/.work/v524-audit/v524-typo/shots/compare_1600.png` (copy: `evidence/v524/t/compare_1600.png`). *Fix:* one line.
7. **A cosmetic indent** in `tokens.css` (` --toast-timeout: 6s;` lost one space when `--toast-w` left). *Fix:* at CLOSING's token
   pass (a rebuild for one byte is not worth it now).
8. **The name's `h1` tracking** (`.he__title--name`) computes −0.028 em instead of −0.024 through `--track-title` (0 visible pixels;
   the lock-up draws the name). *Fix:* none needed; recorded so HOME's pixel diff does not flag it.

---

## 4. Post-acceptance candidates seen outside T's tables (R14 — recorded, not fixed; each belongs to a lane's own row)

- AGAMI `/ar/`: the identification block's Arabic registers («جهة الاتصال الرسمية», «المقر القانوني» …) in a monospaced system
  fallback — visibly wrong; PUB2's `_agami.css` mono row (F-3), already in PUB2's table.
- Home `/ar/` 390: `.he-origin__word` 16/19.2 on two lines (HOME); Parcours: `.tracciato__num` mono numerals (PUB1 / LIB);
  FAQ: the category label «GÉNÉRAL» in the mono (PUB2); the pathway heads' French `h1` 56/75.6 in Arabic leading (LIB `_fronte.css`).
- The FAQ's Arabic `h1` at 56/70 (1.25 through `_fronte.css`'s rule rather than title-1's 1.18): LIB's row.
- The Pexels credit lines still visible on Contact and Parcours (PX, first in the merge order).

---

## 5. Stills and data (all under `C:/tmp/ile_v5_council/evidence/v524/t/qa/`)

- `shots/{home,parcours,faq,projet,agami,contact,login}_{fr,ar}_{1440,1024,390}_{n}.png` (1024 for home, Parcours, FAQ, AGAMI),
  `shots/{dash,case}_{fr,ar}_{1440,390}_{n}.png` — 118 headed frames (44 page visits); `shots/mega_{base,lane}_{fr,ar}_1440.png`,
  `shots/sheet_{base,lane}_{fr,ar}_390.png` — the preserved navbar on both trees.
- `hero_{base,lane}_{fr,ar}_{1440,390}.png`, `hero_diff_{fr,ar}_{1440,390}.png`, `hero.json`.
- `fonts.json`, `type.json` (54 page loads: every text node's size, the label / numeral / primary / display metrics, the Arabic
  guards, overflow, errors), `motion.json`, `channels.json` (booleans), `axe.json`, `navbar.json`, `cls_swap.json`,
  `headed_metrics.json`.
- Logs: `C:/tmp/ile_v5_council/.work/v524-t-qa/logs/{static1,browser1,probe1,probe2,headed1,cls_swap1,build1,build2,srv8785,srv8782}.log`.

Stop: the lane server 8785 and the twin 8782 stopped; `CHROMIUM_LOCK_A` and `PERFORMANCE_BENCHMARK_LOCK` released; the minted
session deleted; nothing in any repository changed by the review.
