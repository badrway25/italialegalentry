# V5.22 · Lane S follow-up (`v522-s2`) · senior design-engineering review (label `v522-s2-qa1`)

2 November 2026, 16:05–19:05. Senior design-engineering reviewer.

**What was reviewed.** Branch `v522-s2` (worktree `C:/tmp/ile_wt/v522-s2`), head
**`5ae404c0c9720b6f3ee82b174eb13aec6bfc8749`**: two commits on design-v5 `269cf39` (`2ddaaaa` the follow-up, `5ae404c` its
notes). Diff read in full (60 files: 7 library sheets, 1 rule of `motion.css`, 3 JS modules, 12 templates, P1's
producer and one P1 sheet, 9 test modules, the dist). The worktree was never written to (`git status` empty before and
after).

**Judged against.** V5.22 (`directives/V5_22_…`), V5.23, SECTION_SYSTEM_V2 §9.7 (ownership), §9.8 (preserved
families), §9.9 (acceptance), §10 (targets); V5.12–V5.21 standing rules; V5.20's strict test rule; DL54-182 item 8/10
and DL54-183 item 10 (the four red guards); P2's QA_ROUND3 (MC-1…MC-5); H's QA_ROUND3 and NOTES §12.5 (H's requests);
the builder's `docs/design-v5/QA/v522/s2/NOTES.md`.

**Servers** (all outside every repository; all stopped at the end; 8780 and 8782 untouched):

| Port | Tree | Use |
|---|---|---|
| 8783 | the worktree (`v522-s2`) | lane server: dev settings, database lane l3 (`ile_v5_l3`), reference date 2026-10-03 (G3 open), the configured WhatsApp number read in process from the preview's untracked `.env` (option B, never printed) |
| 8791 | `git archive 269cf39` | the base (= `v522/p1`, design-v5), same database: every comparison is base against branch on one database |
| 8792 | `git merge-tree v522-h v522-s2` (lane H's final head `4afed99` + this branch), built | H's home with this branch |
| 8796 | `git merge-tree v522-h 269cf39` (lane H alone), built | H's home without this branch |
| 8794 | `git merge-tree v522-s2 v522-p2` (P2's head `53c2996`) + P2's half (`p2_with_lane_s.patch`, normalised to LF, `--whitespace=error`) + `p2_data_registro.patch`, built | P2's pages with this branch: the merge conditions in situ |
| 8795 | `git archive 53c2996` (P2 alone) | P2's drawings before this branch |
| 8788 / 8789 / 8790 / 8793 | base / branch / H + branch / H alone | **compressed twins** for INP: DEBUG off, `CompressedManifestStaticFilesStorage`, private `STATIC_ROOT`, as 8782 is built |

All merges were clean (`git merge-tree` reported no conflict); every scratch tree was rebuilt with `npm run build`.

**Browser and locks.** Headed **chromium-1234** (Playwright) for every visual check and every measure; the test suites
headless as designed. 31 lock sessions (`CHROMIUM_LOCK_A`/`_B`, label `v522-s2-qa1/<session>`), each ≤ 16 min, each
released; the four INP sessions (17:57–18:26) ran with no other Chromium on the machine. Log:
`.work/v522-s2-qa1/logs/locks.log`.

**Where things are.** Report: this file. Screenshots: `evidence/v522/finish/v522-s2-qa1/` (prefixes below). Scripts,
raw JSON and logs: `C:/tmp/ile_v5_council/.work/v522-s2-qa1/` (`tools/`, `data/`, `logs/`, `trees/`, `twin/`).

---

## 0 · Verdict — PASSED (0 major, 6 minor, all routed outside this branch's own product)

Every item of the brief is met, measured independently, at the widths and in the languages asked:

| Item | Result | Measured |
|---|---|---|
| The four red guards green, strength unchanged | **PASS** | red on the base tree (4 failed), green on the branch (627 passed in the guard/reader set); (a) (b) (c) unchanged guards, fixed in the product; (d) updated under V5.20, stronger (§1) |
| MC-1 / MC-2 / MC-3 at 1440 / 768 / 390, fr / ar | **PASS** | on P2's pages with this branch (8794): FAQ arrival, same-document and keyboard hash at every width; glossary 8/8 letters at 5 widths; Forum sommaire 5/5; Réseau's chosen entry in view at 390/768, no jump at 1440 (§2) |
| Index glyphs ≥ 20 px | **PASS** | lane H's home with this branch: the 8 glyphs 20 × 20 px (their svg 20 px) at 1440, 1280 and 1024, fr and ar (§3.1) |
| «La protezione» French title box in Arabic | **PASS** | title and body start on one edge at every width on 5 page types (Parcours, Formation, Diplômes, a pathway sheet, H's home): 572/572 at 1440 … 40/40 at 360; the base: 1127 vs 572 (§3.2) |
| Credit colon only in French | **PASS** | `Photo\u00a0: …` (fr), `Foto: …`, `Photo: …`, `صورة: …`; the base wrote `␠:` in all four (§3.3) |
| First-Tab and first-pointer-after-keyboard INP within 20 ms of the base, desktop and phone, fr and ar | **PASS** | compressed twins, n = 12 a cell on the home: the branch alone −28 to −48 ms on the first Tab, H + branch −4 to +8 ms; every median and Hodges–Lehmann shift ≤ +12 ms; one p75 at +24 ms (§4) |
| No visible change to the preserved families | **PASS** | base vs branch pixel comparison of the navbar, mega menus, phone sheet, footer, forms, login, privacy, cookie, orientation and four persona spaces: identical, except the contact head's photo credit (the credit request itself); Lume, forms, nav, portal, contact-architecture files untouched; `motion.css` only its §5 rule (§5) |

The branch does what it says, and the claims in its notes that I could re-measure hold to the unit (the restyle counts
at the modality flip — home 853, H alone 1 138 → H + branch 525, Arabic 904 / 1 195 → 542, Parcours 774 → 379,
Institutions 462 → 170 — reproduce exactly; the branch alone takes the home to 278). The minors are merge-order
conditions for the steward, lanes H and P2, and S-close (§10).

---

## 1 · The four red guards

**Red on the base, green on the branch.** The four guard functions run on a `git archive` of `269cf39`: **4 failed**
(`_sec-tracciato.css: .tracciato__linea::after` has no RTL twin; `mappa.html` writes `data-seat`;
`approdo.html writes data-register by hand`; `assert (5 >= 9)`). On the branch, the guards, their readers and the
modules that touch them (`test_rtl_static`, `test_loader_rules`, `test_state_chips_carry_a_register`, `test_o14_lint`,
`test_interior_w3_f1`, `test_orientation_w3_f1`, `test_pages_v522_p1`, `test_sezioni_v522_s`, `…_s2`,
`test_motion_v512_a_w2`): **627 passed** (`logs/guards_branch.log`). On P2's tree with this branch and P2's two
patches: **468 passed** (`logs/guards_sp2.log`).

**Strength — read test by test (V5.20 strict rule).**

| Guard | Test changed? | Judgement |
|---|---|---|
| (a) `test_every_horizontal_shift_has_its_rtl_twin` | no | Fixed in `_sec-tracciato.css` (`[dir=rtl] … ::after { translate: 110% 0 }` + `sez-run-rtl`). Unchanged strength |
| (b) `test_l3_attaches_only_to_fragment_containers` | no | Fixed by the pattern's own `data-seggio` (template, sheet, P1's producer and P1's sheet). Unchanged strength |
| (c) `test_data_register_is_written_by_the_partial_and_by_two_legends_only` | no | Fixed by the library's own `data-registro` in 16 templates. Unchanged strength. The three readers that consumed the old marker now read both (`data-registr(?:o|er)`), with two planted HTML cases and one CSS case for the new marker in the O14 lint: **equal or stronger** |
| (d) `test_a_tag_is_a_term_and_carries_neither_a_register_nor_a_mark` | yes, cited | The floor `>= 9` became the **exact** set (`room 1, need_detail 2, helpdesk 2`: one tag more or less fails), and the terms, now native disclosures, are held to the same invariant in their new form (no `data-register`, no `data-registro`, the word without a mark, the chevron beside it). The cited decision exists: SECTION_SYSTEM_V2 §3.5 PS-4 («Each Italian term chip is a `<details name="termini">`…») and §3.10 D1. **Stronger** |

Two other cited updates, checked: `test_pages_v522_p1.py` (six phrases and six seats pair through `data-seggio`, and
now `not section.select("[data-seat]")` — stronger); `test_motion_v512_a_w2.py` (the static assertion follows the new
mechanism, no `[data-input]` rule may end on `::details-content`, and the behaviour is proved in the browser module —
equivalent, reason cited §5.3/§9.9 item 6).

**One side effect checked and cleared.** `tokens.css` re-points chip tokens under `[data-register]` in forced
colours; before the rename the library's lists matched it. Those rules set `--chip-*` only, and no library or page
sheet reads `--chip-*` (grep): the rename changes nothing in forced colours.

---

## 2 · P2's merge conditions on lane S's modules (on P2's pages, 8794)

The three patches are in the branch byte-for-byte as P2's reviewer wrote them (diff read; `spia.js` LF). Measured in
headed Chromium on P2's own pages with this branch (`data/probe2.json`, `probe2_h.json`; captures `H_*`, `I_*`, `J_*`):

**MC-1 — `indice.js` (FAQ explorer).**

| Width | Arrival from another page (`/attention-aux-fraudes/` → `/faq/#faq_diplomas`) | Same document (`location.hash = '#faq_visas'`) | Keyboard (Enter on an in-page link to `#faq_recruitment_agency`, placed by the probe) |
|---|---|---|---|
| 1440 fr / ar | tabs: `#faq_diplomas` selected, heading 72 px from the top, CLS 0.0001 | selection follows the address | selection follows, modality «key» |
| 768 fr / ar | disclosure: the named answer open alone (1 of 9), heading at 88 px, CLS 0.0001 | `#faq_visas` open alone, heading at 72 px (under the letterhead) | open alone, heading at 72 px |
| 390 fr / ar | open alone, heading at 88 px, CLS 0 | open alone, heading at 72 px | open alone, heading at 72 px |

**MC-2 — `spia.js`.** Glossary, fr and ar, at 1440, 1280, 1024, 768 and 390: each of the 8 letters followed from the
rail lights itself (**8/8 at every width**, the three-column, two-column and one-column registers alike); a wheel
read-through lights all 8. Forum sommaire at 1440: **5 of 5** sections lit by a read-through (this database's event is
after its date, so the sommaire holds 5 links).

**MC-3 — `mappa.js`.** Réseau, fr and ar, each of the 6 actors chosen in turn: at 390 and 768 the chosen entry comes
into view every time (the page scrolls to it: y 314/330 at 390, 25/13 at 768); at 1440 the entry stands beside the
ring and the page does not move (y stays 0).

**P2's own assertions** on that tree (`test_pages_browser_v522_p2.py` + `test_browser_w1_c.py`, test database lane
l3b): **56 passed, 2 failed** — both the Forum half of P2's new spy test (`assert len(seen) == 5`, fr and ar), where the
test database's sommaire holds 7 links (programme and registration present before the event) and **all 7 are lit**.
The product is right; P2's assertion counts a constant (m1). W1-C's restored same-document step passes.

---

## 3 · Lane H's requests

### 3.1 The index glyph (`.indice__glifo { flex: none }`)
Lane H's home with this branch (8792): **the 8 glyphs are 20 × 20 px (svg 20 px) at 1440, 1280 and 1024, fr and ar**,
wrapped titles included (H's reviewer measured 15.5–19.2 px at 1024 and 18.4 px at 1280 on H alone). Captures `G_hs2_{fr,ar}_{1024,1280}_index.png`
(the Arabic wrapped titles also hug their glyphs — lane H's own final fix). The ranks are filed under `.indice__riga`.

### 3.2 «La protezione»'s French title on an Arabic page
The h2 carries `lang="fr"` when the locked title falls back (fr pages: no attribute; it, en, ar: `lang="fr"`), its text
byte-for-byte the locked title, and the plate's in-flow parts share one 46 rem column.

| Page (ar) | 1440 | 1024 | 768 | 390 | Base at 1440 |
|---|---|---|---|---|---|
| Parcours, Formation, Diplômes (title x / body x) | **572 / 572** | **209 / 209** | **64 / 64** | **44 / 44** | 1127 / 572 |
| Pathway sheet (salaried work) | **244 / 244** | **64 / 64** | **64 / 64** | **44 / 44** | 799 / 244 |
| H's home (8 widths) | **572 / 572** | **217 / 217** | **56 / 56** | **40 / 40** (430–360) | — |

French, Italian and English pages: positions identical to the base (116/116 at 1440, 44/44 at 390). In Arabic the
plate is 1–2 px shorter (the title now set with Latin leading). Captures `C_{base,branch}_ar_*_protezione.png`,
`G_hs2_ar_*_protezione.png`. Observation (no finding): on wide Arabic plates the French title now starts ~560 px from
the seal at the reading edge; it reads as one French quotation framed by the seal and the Arabic button, as §1 rule 6
asks.

### 3.3 The photo credit
`.foto__credit` and `_ingresso.html` captions, 5 pages × 4 languages (`data/probe1.json` D): branch **fr `Photo\u00a0: …`**
(U+00A0), **it `Foto: …`, en `Photo: …`, ar `صورة: …`**; base `␠:` (U+0020) in all four. The French no-break space
renders at **0.151 em** (1.81 px at 12 px) because Host Grotesk kerns the pair NBSP + colon — exactly as every other
`typo`-spaced French colon of the site (3.01 px at 20 px on the home: 0.151 em). Consistent; no finding.

### 3.4 The first keyboard input (the library's `[data-input]` rules and `motion.css` §5)
Deterministic restyle counts at the modality flip (Chromium trace, largest `UpdateLayoutTree`, Tab / pointer;
`data/restyle_desk.json`):

| Page | Base `269cf39` | Branch | Lane H alone | H + branch |
|---|---|---|---|---|
| home fr | 853 / 853 | **278 / 276** | 1 138 / 1 138 | **525 / 522** |
| home ar | 904 / 904 | — | 1 195 / 1 195 | **542 / 539** |
| Parcours | 774 / 775 | **379 / 378** | | |
| Institutions | 462 / 464 | **170 / 170** | | |
| Projet pilote | 526 / 526 | **338 / 336** | | |
| FAQ (design-v5) | 369 / 369 | **138 / 136** | | |

The builder's figures reproduce exactly.

---

## 4 · INP on the compressed twins

Conditions as the Performance Lead's rig: network A (150 ms, 1.6 Mbit/s down, 750 kbit/s up), CPU × 4, PHONE
412 × 823 @1.75 (mobile, touch), DESK 1440 × 900, cold loads (fresh context, cache disabled), trees interleaved with
the order rotating each round; per load the first Tab (its interaction's longest Event Timing entry) and then the first
pointer input after the keyboard (click / tap on the h1). Every load answered 200 on the real path. In 239 of the 240
loads the modality read «key» after the Tab and «pointer» after the click; on the desktop the headed window sometimes
received an OS pointer event before the Tab (57 loads, every tree alike), so the first flip was «pointer» → «key» instead
of none → «key» — it invalidates the same selectors. One load of the reference tree (lane H alone, desk fr) caught a
stray OS pointer event during the interaction (Tab 416 ms, pointer 88 ms, no flip); it is left in and only touches the
reference column. Home: two interleaved series pooled, **n = 12 a cell**; Parcours n = 6.
`data/inp_home_pooled.json`, `inp_home_desk.json`, `inp_home_phone.json`, `inp_home_b.json`, `inp_parcours.json`.

**Home — first Tab** (ms, median · p75; Δ = median shift · p75 shift · Hodges–Lehmann shift against the base):

| Cell | Base | **Branch** | Δ branch | **H + branch** | Δ H + branch | H alone | Δ H alone |
|---|---|---|---|---|---|---|---|
| desk fr | 140 · 152 | 96 · 104 | −44 · −48 · −40 | 148 · 160 | **+8 · +8 · +8** | 188 · 200 | +48 · +48 · +48 |
| desk ar | 144 · 152 | 96 · 112 | −48 · −40 · −48 | 140 · 160 | **−4 · +8 · 0** | 192 · 208 | +48 · +56 · +48 |
| phone fr | 108 · 112 | 80 · 88 | −28 · −24 · −24 | 116 · 120 | **+8 · +8 · +8** | 136 · 144 | +28 · +32 · +32 |
| phone ar | 124 · 128 | 88 · 88 | −36 · −40 · −32 | 124 · 128 | **0 · 0 · 0** | 156 · 160 | +32 · +32 · +32 |

**Home — first pointer input after the keyboard:**

| Cell | Base | **Branch** | Δ branch | **H + branch** | Δ H + branch | H alone | Δ H alone |
|---|---|---|---|---|---|---|---|
| desk fr | 228 · 248 | 184 · 200 | −44 · −48 · −40 | 208 · 224 | **−20 · −24 · −24** | 284 · 328 | +56 · +80 · +48 |
| desk ar | 224 · 240 | 196 · 208 | −28 · −32 · −32 | 208 · 216 | **−16 · −24 · −20** | 272 · 288 | +48 · +48 · +48 |
| phone fr | 88 · 112 | 100 · 136 | +12 · **+24** · −16 | 76 · 88 | **−12 · −24 · −24** | 116 · 136 | +28 · +24 · +24 |
| phone ar | 108 · 120 | 72 · 128 | −36 · +8 · −32 | 88 · 96 | **−20 · −24 · −16** | 156 · 168 | +48 · +48 · +40 |

**Parcours** (n = 6, base → branch, median): first Tab desk −36 (fr) / −28 (ar), phone −16 / −20; pointer after the
keyboard desk −28 / −36, phone −16 / −28; every p75 lower.

**Reading.** Against «within 20 ms of the base»: every median and every Hodges–Lehmann shift is in, for the branch alone
and for lane H's home with it, desktop and phone, French and Arabic; lane H alone is +28 to +56 ms over, and this
branch brings it back (H's M2 closes with it). One p75 cell is over: the branch alone, phone fr, pointer after the
keyboard, **+24 ms** at p75 (median +12, HL −16) — the rig's noise (that page restyles 278 elements at the flip
against the base's 853); the same cell on H + branch is −24. LCP medians 1.39–1.75 s (home), 1.96–2.38 s (Parcours);
CLS ≤ 0.031 on the desktop for the base, the branch and H + branch (H alone 0.047), 0 on phones; Parcours ≤ 0.025.

---

## 5 · The preserved families — base against branch, one database, reduced motion

`tools/stills.py` (pixel difference > 24 per channel), `data/stills_families_diff.json`, `stills_personas.json`:

| Family | Shots | Result |
|---|---|---|
| Navbar (element) | fr/ar × 1440, 1024, 768, 390 | **8/8 identical** |
| Mega menus (each of the 5 doors opened) | fr/ar × 1440 | identical except one 110–130 × 10 px band: the contact head's photo credit, visible below the panel |
| Phone sheet (opened) | fr/ar × 768, 390 | **4/4 identical** |
| Footer (element) | fr/ar × 4 widths | 7/8 identical; ar 768 showed 5 px at the scrollbar edge once — **6/6 identical** on re-shoot (capture noise) |
| Forms and legal: recueil des besoins, collaboration institutions, collaboration universités, login, privacy, cookie, orientation | fr/ar × 1440, 390 (+ it/en spots) | **identical** |
| Contact page | fr/ar/it/en | identical except the head photo's credit (`P_*_page_contact_fr_1440_crop.png`); the channels, both numbers, their `bdi`, links and names unchanged |
| Persona spaces (qa-doc-person, qa-person, qa-fresh-person, qa-company) | fr/ar × 1440 | **8/8 identical** |

Files: no diff in the navbar/mega/sheet/footer partials, `chrome.css`, `_portico.css`, `nav.js`, `shell.js`, Lume
(`lume.css`, `loader.css`, `head.js`, `lume/*`, `components/loader.html`), the form components and sheets,
`fieldcheck/steps/combobox.js`, `tokens.css`, `base.html`, `templates/portal/**`, `apps/portal/**`, the contact
templates and `apps/core/contact.py`, `locale/**`. `motion.css`: only §5 (the disclosure's keyboard condition), as the
brief allows. The configured WhatsApp number is in no file of the diff, no tracked file and no text evidence of this
review (digit search; count 0).

**The `motion.css` rule, behaviour proved.** FAQ (design-v5's accordion), fr/ar 1440, base vs branch: pointer opens
70 → 155 → 188 → 193 px (base 70 → 155 → 185 → 192) and closes 164 → 21 → 1 (base 151 → 21 → 1); from the keyboard it
opens at once (193 px at 20 ms) and closes at once (1 px at 10 ms) in both trees. The keyboard close keeps the discrete
`content-visibility` flip's 120 ms, invisible (`overflow: clip` at block-size 0). The person dashboard's accordions use
the same rules; their spaces are pixel-identical.

**The library pages** (102 pairs, 17 pages, fr/ar × 1440/390, it/en × 1440): the only differences are the photo
credits, the Arabic «la protezione» title (and the plate's 1–2 px of leading in Arabic), and a navbar link-colour
flicker at y 27–37 that also appears between repeated captures of the **same** tree (capture artefact; the navbar
element shots are identical). Montages: `S_*_diffbands.png`.

---

## 6 · The library's equivalences (what must not have moved)

- **Keyboard tier 0.** Under `html[data-input=key]`, every element of `.sez-tile`, `.sez-disc`, `.sg-g--key`,
  `.mosaico` and their descendants (with `::before`/`::after`): **0 element moves with the branch that did not move
  before** — 9 design-v5 pages vs the base, 10 P2 pages (fr + ar contact) vs P2 alone, H's home fr/ar vs H alone
  (`data/probe1.json` F, `probe3.json` L). The narrowed selectors (`.mosaico *` → two classes; `--sez-t`) lose nothing.
- **Stroke verb without its tag branch.** P2's carriers, each shape's computed dash at 9 local times (timeline slowed,
  then sought): Forum ring mid-draw at 150–600 ms and the fraud shield at 900–1 200 ms — **identical** P2 alone vs P2 +
  branch (`data/probe3_k.json`, `K_*`). AGAMI's colonnade and the project's door: the verb is inert in **both** trees
  (no section state above them) — an observation for P2, not this branch.
- **The route board's light** (Parcours, fr/ar, 1440/390, base and branch): 0 px of light inside any rail at rest; the
  lit lane runs `sez-run` (−110 % → 360 %) in French and `sez-run-rtl` (110 % → −360 %, sampled translate falling) in
  Arabic — identical in both trees, because P1's page twin already did it on Parcours; the library is now right for any
  other consumer (`A_*`).
- **The hemicycle** (Institutions, fr/ar, 1440/390): base 12 `[data-seat]`, branch **0**; six seats and six phrases
  carry `data-seggio`; a phrase lights its seat and a seat its phrase in both trees (`B_*`).

---

## 7 · Sweep and modes (the branch, 8783)

| Check | Runs | Result |
|---|---|---|
| Crawl, 4 languages + `/__design-v5/` | 129 pages × 2 trees | **all 200, 0 traceback** |
| Sweep: home, Projet pilote, Parcours, a pathway sheet, Entreprises, Institutions, Universités, Formation, Diplômes, FAQ, Contact × fr/it/en/ar × 1440, 1280, 1024, 768, 430, 390, 375, 360 (read-through) | 352 | **0 overflow, 0 element wider than the screen, 0 console error, one h1, the anti-fraud notice visible wherever present** |
| axe-core 4.13 (WCAG 2.0–2.2 A/AA) after a read-through, violations filed under their section | 44 (11 pages × fr/ar × 1440/390) | **0 violations** |
| Reduced motion | 44 | 0 section state written, nothing running at rest, no text held below full ink |
| No-JS | 44 | content complete in reading order; on the 20 walks compared with the base (5 pages × fr/ar × 1440/390) the elements hidden by design at a width (the pathway sheet's rail, items of the home) are the same, and the text length differs only by the Arabic credits' removed spaces |
| Keyboard (45 Tabs) | 44 | identical to the base on the 20 walks compared (no stop off screen or covered) |

MC pages (P2 + branch) are in §2; H's home glyphs and plate in §3.

---

## 8 · Tests, build, budgets

- **Non-browser** (lane l3, one pytest at a time): the guard set **627 passed**; the confidential-material guard with
  the private table (read in process, never printed), the contact channels with the configured number in process, the
  `main.css` ceilings and page totals, `test_css_bundle_is_current`, `test_chapter_marks`, `test_check_ownership`,
  catalogues, locked content, loader rules: **410 passed**, 0 skipped.
- **Browser** (lock slot A): `test_sezioni_browser_v522_s2`, `…_s`, `test_reduced_motion_w1_d`, `tests/i18n/test_rtl_browser`,
  `test_pages_browser_v522_p1`, `test_motion_v512_a_w2` (browser half): **104 passed**.
- **P2's assertions on P2 + branch** (lane l3b): 56 passed, 2 failed (§2, m1).
- **Build:** `npm run build` on an archive of the head reproduces the committed dist (**72 files, identical hashes**).
  `ruff check .` clean; `manage.py check` clean; `makemigrations --check` no change.
- **Budgets (gzip -9):** `main.css` **32 716 B** (base 32 718: the ratchet holds, −2); `core/reveal.css` 3 526;
  `core/sezioni.css` 11 308; `pathways/index.css` 10 117 (ceiling 10 240); `ecosystem/institutions.css` 8 381; `rise.js`
  1 325 (1 536).

---

## 9 · Scores (§26; 1–5; 3 = clean but editorial or static)

Scored at 1440 and 390 in fr and ar, checked at the 8 widths. The branch changes no composition, so the question for
lane S is «no page lower on any dimension than before» — none is. «Δ» names the cells this branch moves.

| Page (tree) | Comp. | Motion | Imagery | Interaction | Institutional | Coherence | Δ vs base |
|---|---|---|---|---|---|---|---|
| Home — lane H + this branch, fr | 4.5 | 4.5 | 4 | 4.5 | 4.5 | 4.5 | interaction 4 → 4.5: the first key's cost back at the base (H's M2) |
| Home — lane H + this branch, ar | 4.5 | 4.5 | 4 | 4.5 | 4 | 4.5 | coherence: «la protezione» on one edge; glyphs 20 px |
| Projet pilote | 4 | 4 | 4 | 4 | 4.5 | 4.5 | = |
| Parcours | 4.5 | 4 | 4.5 | 4.5 | 4.5 | 4.5 | ar coherence held with the plate now on one edge |
| Pathway sheet | 4 | 4 | 4 | 4 | 4.5 | 4.5 | ar plate on one edge |
| Entreprises | 4 | 4 | 4.5 | 4 | 4.5 | 4.5 | = (credit typography) |
| Institutions | 4 | 4 | 4.5 | 4 | 4.5 | 4.5 | = (the hemicycle pairs as before, without Lume's attribute) |
| Universités et formation | 4 | 4 | 4 | 4 | 4.5 | 4 | = |
| Formation | 4 | 4 | 4.5 | 4 | 4.5 | 4.5 | ar plate on one edge |
| Diplômes et titres | 4.5 | 4 | 4 | 4 | 4.5 | 4.5 | ar plate on one edge |
| FAQ — P2 + this branch | 4 | 4 | 4 | 4.5 | 4.5 | 4.5 | interaction/coherence from P2's branch-alone 4/4 (MC-1) |
| Glossaire — P2 + this branch | 4 | 4 | 4 | 4 | 4 | 4 | interaction from P2's branch-alone 3.5 (MC-2) |
| Forum — P2 + this branch | 4 | 4 | 4 | 4 | 4.5 | 4 | interaction from 3.5 (MC-2) |
| Réseau — P2 + this branch | 4.5 | 4 | 4 | 4.5 | 4.5 | 4.5 | phones: the chosen actor in view (MC-3) |
| Preserved families | — | — | — | — | — | — | pixel-identical (§5) |

Calibration note: Institutions' composition is scored 4 here (P1's reviewer 4.5) — my reading of a short page, equal on
the base and the branch; it is not a change made by this branch. The home's cells are lane H's to confirm in its final
review.

---

## 10 · Findings

### Major
None.

### Minor (none in this branch's product; each routed)

- **m1 · P2's Forum spy assertion counts a constant** (P2 / steward). On P2 + this branch, P2's
  `test_the_spy_lights_each_letter_followed_and_each_section_read` fails twice (fr, ar) at `assert len(seen) == 5`: the
  test database's sommaire holds 7 links and all 7 are lit. Compare with the sommaire's own link count
  (`page.locator('.forum-localnav a').count()`) before P2 merges. (The builder's request 8.3, confirmed independently.)
- **m2 · P2 still writes the chip's attribute** (P2 / steward). P2's branch writes `data-register` by hand in three
  templates and reads it in three test lines; without `requests/p2_data_registro.patch` guard (c) turns red again at
  P2's merge. With the patch the four guards and the readers pass on P2 + branch (468 passed). A P2 merge condition.
- **m3 · Two S-family guards red on lane H's home with this branch** (S-close or the steward at H's merge). On
  H + branch: `test_chapter_marks.py::test_no_public_page_draws_the_stair_nor_a_glyph_above_a_title…`
  (`HOME_EXPECTED {'compass', 'signpost'} <= set()`) and `test_journey_w3_d.py::test_the_home_draws_the_orientations_neutral_steps_on_the_public_passage`
  (the old `stepper … across=True` include). They are H's declared merge conditions (H QA_ROUND3 m7, NOTES §12.5 item 6),
  outside this follow-up's stated brief, but the files are lane S's (§9.7): they need a cited V5.20 update (the V2 home
  of §3.1) before or with H's merge.
- **m4 · Ownership row** (steward). `scripts/check_ownership.py`'s `FAMILY_ID` does not admit `v522-s2`; the family
  and P1's carried slices (services.py, `_institutions.css`, eight templates, `test_pages_v522_p1.py`) need their rows at
  the merge, as the builder's notes say.
- **m5 · P1's page twin is now redundant** (P1 / S-close). `_index.css`'s `[dir=rtl] .percorsi-tracciato … ::after` and
  its `sez-run-rtl` duplicate the library's own; harmless, removable at S-close.
- **m6 · The modality's last broad subjects** (S-close / Director). Still filed under tags or `:is()`: `_photo.css` and
  `_sec-campata.css` `img`, `_sigillo.css`'s `:is(...)`, P1's `_pilot.css` li/span, P2's `_projet.css .projet-racconto *`,
  and the preserved `base.css a` / `main.css` field rules. INP is already within target; recorded by the builder (§8.5,
  §8.6), with the two orphan chunks.

### Observations (no action asked of this branch)
- The stroke verb never runs on AGAMI's colonnade and the project's door (no section state above them), on P2 alone and
  with this branch alike — for P2's final review.
- The French credit's no-break space renders at 0.151 em (the typeface's kerning), as all French colons of the site.
- In Arabic the plate's French title sits at the start of its LTR column, away from the seal on the reading edge — the
  intended §1 rule 6 reading.

---

## 11 · Evidence and housekeeping

- Screenshots `evidence/v522/finish/v522-s2-qa1/`: `A_*` route board (rest, run; base/branch; fr/ar; 1440/390), `B_*`
  hemicycle, `C_*` «la protezione», `D_credit_*` credits, `G_hs2_*` H's home index and plate, `H_sp2_*` MC-1, `I_sp2_*`
  MC-2, `J_sp2_*` MC-3, `K_*` stroke carriers, `P_*` preserved-family crops, `S_*` base/branch diff montages, `Y_*` full
  pages (H + branch home, P2 + branch FAQ, Glossaire, Réseau, Forum), `Z_*` contact sheets. Some captures show the site's
  footer as the site draws it; this report writes no contact number.
- Data: `data/probe1*.json`, `probe2*.json`, `probe3*.json`, `probe6_*.json`, `sweep_branch_*.json`,
  `stills_*.json`, `inp_*.json`, `restyle_desk.json`, `crawl.json`, `dist_*.sha`.
- Servers 8783, 8788–8796 stopped (8780 and 8782 untouched); no lock held; no repository written; nothing pushed,
  merged, tagged or deployed.
