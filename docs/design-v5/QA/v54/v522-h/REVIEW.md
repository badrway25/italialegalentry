# V5.22 · Lane H — Homepage Composition V2 · final review, round 2 (label `v522-h-final-qa2`)

5 November 2026, 16:15–17:40. Senior design-engineering reviewer. Resumed after the account limit interrupted the
3 November attempt (its one usable artefact is disclosed in §7).

**What was reviewed.**
- Branch `v522-h` (worktree `C:/tmp/ile_wt/v522-h`), head **`d5ba7c1987e830e68ca06aff6d167ae2fa530546`** (the improve
  round after the final review, label `v522-h-final-improve`). design-v5 `28fa9fa2` (`v522/s2`, DL54-184) **is an
  ancestor of the branch** (`git merge-base --is-ancestor 28fa9fa2 HEAD`: yes — merged at `0191e444`), so no scratch
  merge was needed: the branch is served as it stands, and its tree is what the steward merges.
- The lane's own commits since the last review (`4afed998..HEAD`, first parent): `0191e444` the merge of design-v5,
  `7a8eecd9` the rebuilt dist, `aa640b08` the catalogue entry, `d5ba7c19` the improve. Its own diff since the merge
  commit (`0191e444..HEAD`, 15 files): `pages.css` (51 lines), the two lane H test modules (+2 static guards, +8 browser
  cases), lane S's two guards (`test_chapter_marks.py`, `test_journey_w3_d.py`, under V5.20), `locale/**` (+1 −1 in
  it/en/ar/fr), the dist `pages.css`, NOTES §14.

**Judged against.** V5.22, V5.25 (targeted checks; «if all six dimensions are ≥ 4 and no blocker exists: MERGE»),
V5.26; SECTION_SYSTEM_V2 §3.1, §5.3, §9.7–§9.9, §10; the V5.12–V5.21 standing rules and V5.20's strict test rule;
`evidence/v522/finish/v522-h-final-qa1.md` (head `4afed99`, 2 major, 6 minor); the builder's
`docs/design-v5/QA/v522/h/NOTES.md` §14; **the Director's ruling on F-M2** (recorded in §7).

**Servers** (all outside every repository; stopped at the end; 8780 and 8782 untouched — 8782 was down and was not
started: the twins below stand in for it, built as it is built):

| Port | Tree | Use |
|---|---|---|
| 8785 | the lane worktree `v522-h` at `d5ba7c19` | lane server: `config.settings.dev`, database lane l5 (`ile_v5_l5`; `migrate --check` clean, `makemigrations --check` no change), `ILE_DESIGN_PREVIEW=1`, `ILE_REFERENCE_DATE=2026-10-03` (G3 open); restarted once with 2026-09-30 for the gate-closed runs (16:23–16:25), then restored. The configured WhatsApp number read in process from the preview's untracked `.env` (option B; never printed) |
| 8788 | the lane worktree (collectstatic into a private root) | compressed twin of the lane (DEBUG off, `CompressedManifestStaticFilesStorage`, hashed and gzip-served assets, `core.clock` on 2026-10-03, as `settings_8782.py`), l5 |
| 8789 | `git archive 28fa9fa` (the previous review's base tree, re-verified byte-identical to design-v5 on `pages.css`, `main.css`, `_pilot.html`, the source sheet) | compressed twin of the base, same database |

**Browser and locks.** Headed **chromium-1234** (Playwright) for every visual check and every measure; Playwright's
headless shell for the lane's browser tests, as they are designed. Lock sessions, label `v522-h-final-qa2/<name>`, each
released: pilot 16:21:31–16:22:32, closed 16:23:55–16:25:24, inp (one slot, the busy run) 16:29:13–16:38:38, sanity
16:38:49–16:43:59, pytest_browser 16:44:16–16:57:32, inp2 (one slot, 0 pytest) 17:14:26–17:24:16, inp3 (**both** slots,
0 pytest, CPU 12–24 % at rest) 17:25:35–17:33:24 — each under 25 minutes. Log: `.work/v522-h-final-qa2/logs/locks.log`.
Two irregularities, disclosed: (1) 16:26:33–16:29:13 a two-slot attempt held slot A while waiting for slot B, which lane
P2's review held (`v522-p2-final-qa2 browser-1`, since 16:21:43); I stopped the wait rather than block the other lane,
and the stop command also ended my own tool shell (no other lane's process was touched — P2's lock session and its three
pytest pairs were checked alive at 16:31); (2) the machine was busy throughout with lane P2's final round (three pytest
pairs 16:20–16:5x and two headed sessions), so the first INP run's absolutes are unreadable and only its pairing is used
(§7).

**Where things are.** This report; screenshots in `evidence/v522/finish/v522-h-final-qa2/` (key crops at its root as
`fqa2_*.png`; folders `pilot/`, `plates/`, `sweep_frar/`, `sweep_closed/`, `axe_open/`, `s4_rm/`, `s4_nojs/`,
`s4_keys/`); scripts, raw JSON and logs in `C:/tmp/ile_v5_council/.work/v522-h-final-qa2/` (`tools/`, `data/`, `logs/`,
`twin/`, `trees/lane` = the clean archive the build was checked on).

---

## 0 · Verdict — PASSED (0 major, 6 minor, all carried or the steward's) — merge

**Every finding of the final review that lane H could close is closed, and measured so:**
- **F-M1 · the Arabic pilot statement on one alignment — fixed.** On `/ar/` the locked French title now follows its seam
  as the Arabic lead and the link do: from 64 rem every title line, lead line and the link stand **0.0 px** off the gold
  thread's axis (1440 / 1280 / 1024); below, their right edges spread **0.0 px** (768, 430, 390, 375, 360). fr, it and
  en unchanged (0.0–0.1 px, one left edge below). Headed, reduced motion, the catalogue's entry present in all four
  languages. `fqa2_ok_FM1_ar_1440_pilot_title_on_the_seam_axis.png`, `…_ar_1024_…`, `…_ar_390_pilot_one_reading_edge.png`.
- **F-m2 · the lead's last line — fixed** (`text-wrap: pretty`): at the 8 widths in ar, fr, it and en the last line holds
  2–7 words (ar 768: «ومشروع واحد.»). `fqa2_ok_Fm2_ar_768_lead_last_line_two_words.png`.
- **F-m1 · gate closed, the two interim plates — fixed**: each at its own height (fr 164 / 272 px at 1440 and 1280,
  192 / 356 at 1024, 144 / 288 at 390; ar 164 / 244, 192 / 272, 144 / 216), **0 px** of empty plate under any last
  statement. `fqa2_ok_Fm1_closed_fr_1440_plates_own_heights.png`, `…_ar_1024_…`.
- **F-M2 · the first keyboard input — judged under the Director's absolute budget (§7).**
- **F-m5 · the merge conditions lane H could carry — done**: the catalogue entry is on the branch (`aa640b08`;
  `i18n_audit.py` OK, 100 % in it/en/ar/fr; the merge's own pass is +0 −0 for lane H), lane S's two guards are updated
  under V5.20 and are stronger (§5). The OWNERSHIP rows, the seed on the shared databases and the preview label remain
  the steward's steps.
- **F-m3, F-m4, F-m6 — carried, not lane H's files** (lane S / S-close / the Director), unchanged.

**The technical floor holds on the branch as it stands:** the clean-archive build reproduces the committed dist byte for
byte (twice); the home's sheets total **61 440 / 61 440 B** gzip -9 (0 B headroom — recorded), `main.css` 32 716 B under
its ratchet; the diff since design-v5 names no preserved family and no locked registry; overflow 0, no wide element,
0 console errors, 0 hidden or ringless focus stop in 8 sweep runs (gate open and closed); axe 0 violations in 8 document
runs and in every composed section; reduced motion, no-JS and keyboard pass; ruff, `check`, `migrate --check`,
`makemigrations --check` clean; every changed text file LF; the configured contact number in 0 tracked files and 0
lines of the diff (counted in process).

**Under the Director's ruling on F-M2 (§7):** the first keyboard input is **within the 200 ms p75 budget in all four
cells on the measure of record** (lane 160 · 176 · 128 · 168 ms, night run, both slots, n = 12); the first pointer input
after the keyboard is within it on the phone and **over it on the desktop on both trees** (lane 216 · 248, the base
176 · 208) — the residual the ruling assigns to S-close, recorded with its attribution (lane H: 9 of ~520 restyled
elements). Nothing a further round of lane H could change.

**§9.9 (V5.25 §5):** composition and coherence 4.5, motion 4.5, imagery 4.0, interaction 4.0, institutional 4.5, at 1440
and 390 in fr and ar — **every dimension at or above its bar, no blocker lane H can remove: MERGE.** The steward's
steps are listed in §9 (F2-m5), with the ruling to carry into the DL entry.

Verdict on the owner question «would a senior designer call this a premium institutional legal-tech platform, not an
online report with cards?»: **yes, in all four languages at every width** — the Arabic page now included, its moment
on one axis.

---

## 1 · The branch, the build, the catalogue

| Check | Result |
|---|---|
| Ancestry | design-v5 `28fa9fa2` is an ancestor of `d5ba7c19` (merged at `0191e444`, no conflict: the lane's 28 files and design-v5's 122 have no file in common — re-read in the diff) |
| Build | `git archive HEAD` into `.work/v522-h-final-qa2/trees/lane`, `node_modules` junction to the installed packages, `npm run build`: **every dist file byte-identical to the committed dist** (`main.css`, `core/portico.css`, `core/reveal.css`, `pages/css/hero.css`, `pages/css/pages.css`, `home.js`, `rise.js`; `git diff --no-index` over `static/css/dist` and `static/js/dist`: empty); a second build is identical |
| Catalogue | `scripts/i18n_audit.py` on the branch: **OK** (exit 0; only the long-standing reviewed overlaps listed, none lane H's). The lead served in the page's language on 8785: fr «Le même geste, …», it «Lo stesso gesto, …», en «The same gesture, …», ar «الحركة نفسها، على خشب الأرز وعلى الرخام: حرفتان، وضفّتان، ومشروع واحد.» — the same four renderings the final review reviewed; the title keeps `lang="fr"` on it/en/ar, none on fr. The lane database l5 holds the new default (the builder's seed; the steward's `seed_all --only pages.home_sections` does the same on the shared databases) |
| Ownership | the family's rows are the steward's merge step (`FAMILY_ID` already admits `v5<nn>-h`); the builder's list (NOTES §14.7) names the five whole files and the slices, including lane S's two guards and `locale/**` |
| Preserved families in the diff (`28fa9fa2..HEAD`, 38 files) | **none**: no navbar, mega-menu, phone-sheet, footer, Lume, `motion.css`, `head.js`, form, contact, privacy, cookie, portal, `base.html`, `tokens.css`, `main.css`, library (`_sezioni`, `_sigillo`, `_sec-*`, `rise.js`, `sezioni/`) or locked-registry file. `_hero.html` and `hero.css`: the foot only («la soglia»), unchanged since `4afed99` |
| Contact, option B | the configured number (read in process from the preview's `.env`, never printed) is in **0** tracked files and **0** lines of the diff |
| Lint, checks, line endings | `ruff check .` all checks passed; `ruff format --check` on the four changed test modules: formatted; `manage.py check` 0 issues; `migrate --check` on l5 clean; `makemigrations --check --dry-run` no change; every changed text file LF |

**The diff since the last review, read** (`0191e444..HEAD`, `pages.css`):
- §7 the pilot: `[dir="rtl"] .page-home .pilota__titolo[lang] { text-align: end }` (0,4,0 over §1's French-run rule at
  0,3,1) and, inside the 64 rem block, the same selector `text-align: center`; `.pilota__lead { text-wrap: pretty }`.
- §8 the integrity band: `.strato__lastre--2 { align-items: start }` (on the home only the closed gate lays two plates;
  the sheet is page-only).
- §4 the modality: the two `html[data-input="key"]` rules folded into one with three class-led subjects (the doors'
  arrows and arches, the promoter's photograph), `transition-duration: 0s` — the home's sheets now name `data-input`
  once (guarded).
- Equivalent rewrites that paid the bytes (each read against the rule that makes it redundant: `base.css`'s heading
  weights and balance, `ol[role="list"]`, the library's `.panorama` / `.panorama__quadro` / `.strato__lastra`, the
  elements' own line heights, the row's own hover ink): `list-style`, four `font-weight`, three `text-wrap: balance`,
  `flex: none`, `display: grid`, `position: relative`, one `line-height`, the news hover folded into
  `text-decoration: underline 1px`, the plate's padding written as its one differing side. Seen on the page: the
  sections' heights at 1440 are the final review's to the pixel (fr 6 112, ar 6 103; hero 975, orientation 654 / 677,
  index 698 / 705, the moment 738, trust 902 / 871, anti-fraud 613 / 622, ecosystem 861 / 837, reserved 169 / 168), and
  the sweep, the stills and axe find nothing new (§4).

---

## 2 · The final review's findings — verified

| F | Status | Measured (headed, 8785, reduced motion for the stills) |
|---|---|---|
| **F-M1** the Arabic pilot title off the seam's axis / on the far edge | **Fixed** | `pilot/pilot.json`: ar 1440 axis 712.4 — title lines 509.5–915.3 and 472.6–952.2, lead 476.5–948.3 and 656.1–768.7, link 622.3–802.5: **max offset 0.0 px**; 1280 (axis 632.4) and 1024 (504.4): 0.0 px; ar 768 right edges all 712.8, 430 all 399.2, 390 all 359.2, 375 all 344.0, 360 all 328.8: **spread 0.0 px**. Computed: `lang="fr"`, `direction: ltr`, `text-align: center` from 64 rem, `end` below. fr / it / en: 0.0 px (it 1024: 0.1), left edges 40 (768) and 16 (phones). `fqa2_ok_FM1_*.png`, `pilot/*_statement.png` (32 crops) |
| **F-M2** the first keyboard input | **Ruled** — §7 | the Director's absolute budget (≤ 200 ms p75 on the compressed twins, paired, n ≥ 5) replaces «within 20 ms of the base» |
| **F-m1** gate closed, the plates stretched to one height | **Fixed** | `plates/plates.json` (8785 on 2026-09-30): fr 1440 164 / 272, 1280 164 / 272, 1024 192 / 356, 390 144 / 288; ar 164 / 244, 164 / 244, 192 / 272, 144 / 216; empty plate below the last statement **0 px** in every cell. `fqa2_ok_Fm1_*.png` |
| **F-m2** the lead's last line one word (ar 768) | **Fixed** | last-line word counts: ar 2 · 3 · 4 · 2 · 4 · 4 · 5 · 5 (1440 → 360); fr 6 · 7 · 4 · 5 · 2 · 3 · 4 · 5; it 5 · 6 · 2 · 4 · 2 · 2 · 2 · 3; en 4 · 5 · 2 · 3 · 2 · 2 · 2 · 2 — never one |
| **F-m3** «la protezione»'s guillemets on phones | **Carried** (lane S / S-close) | `components/sezioni/protezione.html` is not in the lane's diff; the request stands in NOTES §14.8 |
| **F-m4** rhythm: the moment after the integrity band | **Carried** (the Director) | still 738 px after 902 + 613 = 1 515 px at 1440 × 900 (fr) |
| **F-m5** merge conditions | **Lane H's part done** | the catalogue entry on the branch (§1); S's two guards updated under V5.20 (§5); OWNERSHIP rows, `seed_all --only pages.home_sections` on the shared databases, the label «Homepage Composition V2», DL / live_status / changelog / tag: the steward's |
| **F-m6** the orientation's caveat plate on the Arabic page | **Carried** (S-close / the Director) | `_linea-v2.css` is lane S's and not in the diff; the plate reads as the final review described it |

The builder's account (NOTES §14) is accurate on every claim re-measured here: the 0.0 px axis and edge figures, the
plate heights, the last-line counts, the byte figures (11 306 / 61 440), the build's reproducibility, the restyle counts
(§7), the test changes' direction (stronger, cited), LF.

---

## 3 · What the owner sees now

**French, Italian, English — unchanged since the final review**, which found them a premium institutional platform at
every width: the hero's line into the orientation's route; the seal, the four stations and the caveat; the index and its
stage; the diptych developing on the night with its gold seam and its lead in the page's language; the four «Non.»
plates on the dressed stone and «la protezione»; the photograph rising in its arch while the doorway draws as one
line; the key turning beside CONNEXION. `sweep_frar/fr_1440_full.png`, `fr_390_full.png`, `fqa2_ref_fr_1440_pilot_centred.png`.

**Arabic.** The one defect the final review found with the merge's catalogue entry is gone: in the pilot's seam the
French title, the Arabic lead and the link stand on one axis from 64 rem and on one reading edge below, at every width
— the page's moment says one thing on one alignment in Arabic as it does in the other three languages.
`fqa2_ok_FM1_ar_1440_pilot_title_on_the_seam_axis.png`, `fqa2_ok_FM1_ar_390_pilot_one_reading_edge.png`,
`sweep_frar/ar_1440_full.png`, `ar_390_full.png`.

**Gate G3 closed** (reference date 2026-09-30): banner, neutral route, static index, the two interim plates now at
their own heights, the ecosystem; overflow 0, 0 console errors, focus clean. `fqa2_sheet_closed_fr_1440.png`,
`sweep_closed/*_full.png`.

---

## 4 · Targeted sanity (V5.25 §2) — fr and ar at 1440 and 390, headed, after a play-through

| Check | Result | Evidence |
|---|---|---|
| Overflow, wide elements, console | **0 / none / 0** in 4 open-gate runs and 4 closed-gate runs | `sweep_frar/sweep.json`, `sweep_closed/sweep.json` |
| Focus walk | 35 (1440) / 49 (390) stops inside `<main>`, none hidden under the sticky header or off-screen, none without a ring (the trust plates carry theirs on the plate's field) | same |
| axe-core 4.13, WCAG 2.0–2.2 A + AA | **0 violations** in 8 document runs (fr/ar × 1440/390 × motion on/off) and **0** in each composed section run on its own (hero, doors at 390, orientation, pathways, pilot, trust, anti-fraud, ecosystem, reserved). Incompletes: colour contrast over photographs and gradients (35–60 nodes), `aria-valid-attr-value` once in the preserved header at 390 — both as in the final review | `axe_open/axe.json` |
| Reduced motion | no `data-sec-state` written on any of the 9 sections at load or after; only Lume's animations run; the hero rests in black and white, the pilot's photographs in colour, the lines drawn | `s4_rm/rm.json`, `s4_rm/*.png` |
| No-JS | 8 / 8 pathway panels visible, the four doors on phones, the four plates, no locked text hidden, headings in reading order | `s4_nojs/nojs.json`, `s4_nojs/*_full.png` |
| Keyboard | 31 (1440) / 34 (390) stops to the footer in reading order; the tablist's ArrowDown, ArrowDown, End, Home, ArrowUp (wraps) with the page fixed (y 1 433 fr / 1 456 ar); the skip link first | `s4_keys/keys.json`, `s4_keys/*.png` |
| Preserved families | not in the diff (§1); the header, footer and hero's first screen render as on the base in every capture | `sweep_frar/*_full.png` |

---

## 5 · Tests (one pytest at a time per database; the lane worktree; CI placeholders, the `.env` not read; the private
sentinel table and the configured number read in process, never printed)

| Suite | Result |
|---|---|
| **The home and lane H's own** (test DB `test_ile_v5_l5`) — `test_home_v522_h.py`, `test_home.py`, `test_templates_static.py`, `test_prescribed_fragments.py`, `tests/compliance/test_locked_content.py` (the locked checksums), `tests/frontend/test_french_typography_w2_d.py`, `test_services.py`, `test_review2.py`, `tests/frontend/test_frontispiece_v515_c.py` (the per-sheet and per-page ceilings), `test_design_docs.py`, `test_css_bundle_is_current.py`, `test_static_pipeline.py` | **512 passed** (19 min 55 s on the busy machine; the final review's 510 + the 2 new guards) |
| **The guards around the merge** (same DB, after the first) — `tests/frontend/test_chapter_marks.py`, `test_journey_w3_d.py`, `tests/i18n/test_catalogues.py`, `test_page_integrity.py`, `test_rtl_static.py`, `test_locked_texts.py`, `tests/frontend/test_loader_rules.py`, `test_state_chips_carry_a_register.py`, `test_o14_lint.py`, `test_sezioni_v522_s.py`, `test_sezioni_v522_s2.py`, `test_interior_w3_f1.py`, `test_orientation_w3_f1.py`, `tests/compliance/test_imagery_v512.py` | **738 passed** (12 min 03 s) — lane S's two guards green on the branch (red at the final review), the catalogue tests green without a simulated pass |
| **Security and contact** (`ILE_CONFIDENTIAL_SENTINELS` = the private table, read in process; `WITH_WA=1`: the configured number read in process; nothing printed) — `tests/security/test_confidential_material.py`, `tests/compliance/test_no_personal_data_in_repository.py`, `apps/pages/tests/test_contact_channels_v519.py`, `tests/compliance/test_phase3_texts_not_leaked.py` | **82 passed, 0 skipped** (3 min 16 s) |
| **Browser** (Playwright's headless shell as designed; test DB `test_ile_v5_l5b`, one pytest on it; lock slot A 16:44:16–16:57:32) — `test_home_browser_v522_h.py`, `apps/pages/tests/test_browser.py` | **69 passed** (13 min 12 s; the final review's 61 + the 8 new cells) |
| `manage.py check` · `migrate --check` (l5) · `makemigrations --check` · `ruff check .` · `ruff format --check` (the 4 changed test modules) | 0 issues · up to date · no change · all checks passed · formatted |

Logs: `.work/v522-h-final-qa2/logs/t_setA.log`, `t_setB.log`, `t_setC.log`, `t_browser.log` (with their `.time` files).

**Test changes under V5.20, read in the diff.** Lane S's two guards, both updated on this branch as the final review's
merge condition asked, each citing V5.22 / SECTION_SYSTEM_V2 §3.1 and §4:
- `tests/frontend/test_chapter_marks.py` — *before:* the home skipped the «no bare mark» rule and only had to draw
  V5.12's two chapter marks; *now:* the home is held to the rule every page holds (no stair, no bare mark, no glyph above
  a title, one concept once) **and** its seals must be exactly `ile-orienta`, `ile-scudo`, `ile-accesso`, in that order,
  each once, on `/fr/` and `/ar/`. Stronger; nothing loosened.
- `tests/frontend/test_journey_w3_d.py` — *before:* the pre-V2 include string; *now:* exactly one include of
  `components/stepper.html`, with every V2 parameter and `only`, and still no `sequence__` class. Stronger.
- New: two static guards in `test_home_v522_h.py` (the title's two rules in their blocks, the lead's `pretty`, the
  plates' `align-items`; the home's one `data-input` rule with its three class-led subjects, present on the page) and
  one browser test in `test_home_browser_v522_h.py` parametrised over the 8 widths × 4 languages (axis within 2 px from
  64 rem, one reading edge within 1 px below, the last line ≥ 2 words, the lead in the page's language). No timeout
  raised, no skip added.

---

## 6 · Measurements

**CSS / JS (gzip -9, the committed dist = the rebuilt dist):**

| Asset | Size | Ceiling |
|---|---|---|
| `main.css` | **32 716** | 32 718 (ratchet; untouched by the lane) |
| `core/portico.css` · `core/reveal.css` | 2 993 · 3 526 | — |
| `pages/css/hero.css` | 10 899 (untouched this round) | 11 264 |
| `pages/css/pages.css` | **11 306** (11 299 after the merge; +7 B net for the round) | 12 288 |
| **Home, every sheet linked** | **61 440** | **61 440 (0 B headroom — recorded for the steward: any later byte in `core/reveal.css` or `pages.css` counts here)** |
| `home.js` · `rise.js` | 7 357 · 1 325 | 8 192 · 1 536 |

**Restyle at the modality flip** (deterministic, Chromium trace, largest `UpdateLayoutTree`, 1440 × 900, the twins):

| | base `28fa9fa` (8789) | lane (8788) |
|---|---|---|
| elements | 1 178 (fr) / 1 175 (ar) | 1 394 / 1 391 |
| first Tab | **276 / 281** restyled | **523 / 539** |
| first pointer after the keys | 274 / 279 | 520 / 536 |

The counts agree with the final review's (523 / 539 against 276 / 316) and with the builder's flip lab (NOTES §14.3:
lane H's own rules account for none of the difference; ≈ 150 are the vocabulary's `:root:not([data-input="key"])`
guards and 39 the keyboard tier's inherited `--sez-t`, both lane S's; the rest is the Tab's own restyle on a longer
page and the preserved `main.css` modality rules on 12 more links and 11 more buttons).

---

## 7 · F-M2 — the first keyboard input, under the Director's ruling

**The ruling, recorded.** The relative gate of the final review («within 20 ms of the base», F-M2 / round 3 M2) is
replaced by the absolute budget of SECTION_SYSTEM_V2 §5.3: **the first Tab and the first pointer input after the
keyboard at ≤ 200 ms at p75 on the compressed twin, desktop and phone, fr and ar, measured paired against the base
with n ≥ 5**; the residual trim is lane S's follow-up (closing). The DL entry carries the same words.

**The rig** (`tools/inp.py`, the Performance Lead's conditions as every V5.22 review used them): network A (150 ms,
1.6 Mbit/s down, 750 kbit/s up), CPU × 4, PHONE 412 × 823 @ 1.75 touch, DESK 1440 × 900; a cold load each (fresh
context, cache disabled); the trees interleaved and the order turning each round; after a 2.5 s rest the first Tab
(`html[data-input]` absent → `key`; the longest Event Timing entry of its interaction), then the first pointer input
(a click on the desk, a tap on the phone, on the page's h1). Base = design-v5 `28fa9fa` on 8789; lane = `d5ba7c19` on
8788; both on `ile_v5_l5`, both serving the same seeded home.

**Four paired runs exist for these two trees; only one was made on an idle machine.** The absolute budget is a property
of the twin, and the twin's figure is only readable when the base twin's own figures sit where every earlier quiet
measure put them (first Tab ≈ 100 ms, desk pointer ≈ 170–210 ms, LCP 1.4–1.7 s). Today's machine never got there:
lane P2's final round ran beside this review (three pytest pairs until 17:10, headed sessions until 17:1x), and even at
17:25 with 0 pytest, both slots held and CPU at 12–24 % the base twin measured 1.5–1.9 × its night values. So the
measure of record is the night run of this same label, and today's runs are read for their pairing only.

| Run | When, conditions | Cell | First Tab · base (med · p75) | lane | Δ p75 · HL | Pointer after keys · base | lane | Δ p75 · HL |
|---|---|---|---|---|---|---|---|---|
| **A · measure of record** | 3 Nov 00:29–00:40, this label's interrupted attempt, **both slots, idle machine, n = 12** (`data/prev_3nov/inp_home.json`; its lane twin was built from the attempt's scratch worktree, found at `d5ba7c19` and clean, its base from the same `28fa9fa` archive as today's — the twin folders themselves were rebuilt today, so the trees are inferred from the attempt's artefacts, not re-read) | desk fr | 104 · 104 | 144 · **160** | +56 · +40 | 168 · 176 | 208 · **216** | +40 · +32 |
| | | desk ar | 96 · 96 | 160 · **176** | +80 · +64 | 192 · 208 | 220 · **248** | +40 · +24 |
| | | phone fr | 88 · 96 | 116 · **128** | +32 · +24 | 76 · 104 | 116 · **144** | +40 · +16 |
| | | phone ar | 88 · 96 | 132 · **168** | +72 · +40 | 88 · 96 | 104 · **112** | +16 · +16 |
| B | 5 Nov 16:29–16:38, one slot, P2's three pytest pairs running, n = 8 (`data/inp_home.json`) | desk fr / ar | 292 · 304 / 220 · 248 | 356 · 408 / 396 · 408 | +104 · +68 / +160 · +152 | 480 · 528 / 516 · 608 | 584 · 624 / 588 · 616 | +96 · +96 / +8 · +64 |
| | | phone fr / ar | 176 · 200 / 188 · 232 | 264 · 296 / 292 · 328 | +96 · +72 / +96 · +88 | 164 · 240 / 160 · 192 | 192 · 208 / 284 · 384 | −32 · +8 / +192 · +144 |
| C | 5 Nov 17:14–17:24, one slot, 0 pytest, P2's headed session on the other slot, n = 10 (`data/inp_home_quiet.json`) | desk fr / ar | 160 · 216 / 148 · 184 | 232 · 264 / 264 · 312 | +48 · +48 / +128 · +104 | 336 · 392 / 380 · 400 | 348 · 392 / 424 · 496 | 0 · 0 / +96 · +76 |
| | | phone fr / ar | 124 · 136 / 136 · 152 | 168 · 176 / 180 · 208 | +40 · +40 / +56 · +48 | 104 · 104 / 116 · 136 | 172 · 264 / 136 · 200 | +160 · +52 / +64 · +28 |
| D | 5 Nov 17:25–17:33, **both slots**, 0 pytest, CPU 12–24 % at rest, n = 8 (`data/inp_home_quiet2.json`) | desk fr / ar | 160 · 160 / 168 · 192 | 252 · 280 / 236 · 248 | +120 · +88 / +56 · +76 | 300 · 320 / 316 · 344 | 388 · 424 / 408 · 440 | +104 · +76 / +96 · +88 |
| | | phone fr / ar | 104 · 104 / 120 · 128 | 152 · 160 / 192 · 200 | +56 · +48 / +72 · +72 | 88 · 128 / 104 · 120 | 96 · 104 / 180 · 224 | −24 · +16 / +104 · +44 |

(HL = Hodges–Lehmann shift of the paired series. In runs B–D the desktop window read `pointer` before the Tab — an OS
pointer event in the headed window, both trees alike, as the final review and S2's review saw —, so its first Tab is a
pointer → key flip, the same restyle class. LCP medians: A 1.39–1.71 s; D 1.52–1.94 s; CLS ≤ 0.05 everywhere.)

**Reading under the ruling.**
- **The first Tab: within the budget in all four cells** on the measure of record — lane **160 · 176 · 128 · 168 ms at
  p75** (desk fr, desk ar, phone fr, phone ar), 24–72 ms under it. Today's runs cannot confirm the absolutes (the base
  itself reads 160–304 ms at p75 on the desk) but agree on the pairing: the composed home costs **+24 to +88 ms (HL)**
  at the first key over `28fa9fa`, as the final review (+32 to +84) and S2's quiet reference (+36 to +52) found.
- **The first pointer input after the keyboard: within the budget on the phone** (144 · 112 ms) **and over it on the
  desktop — on both trees.** Lane 216 (fr) · 248 (ar) ms at p75 against the base's own 176 · 208; the lane's share is
  +32 · +24 ms (HL; +16 · +40 at the median). The base at `28fa9fa` already misses this cell in Arabic and sits 24 ms
  under it in French; the budget was not met by the integrated tree before lane H.
- **Whose it is.** Deterministic (§6): the lane restyles 520 / 536 elements at the pointer flip against 274 / 279. Lane
  H's own rule names three class-led subjects — 4 arrows, 4 arches, 1 photograph: 9 elements. The rest is the preserved
  `main.css` modality rules (§9.8: `html[data-input="key"] a` on 115 links and `.btn` on 16 buttons — 12 links and 11
  buttons more than the base, every one a composed section's own call) and lane S's library (the vocabulary's
  `:root:not([data-input="key"])` guards ≈ 150, the keyboard tier's inherited `--sez-t` 39; NOTES §14.3's table, route
  (a)). Nothing in this round moved it: the fold restyles the same 9 elements as the two rules it replaced.
- **Decision.** Under the ruling the first-Tab gate — the gate F-M2 and round 3's M2 were raised on — is **met**; the
  desktop pointer-after-keyboard cell is **the residual the ruling itself assigns to lane S's follow-up (closing)**: it
  is over budget on the base as well, so holding lane H's merge would not bring it within budget, and lane H holds
  9 of the ~520 elements it touches. It is recorded as a minor finding carried to S-close with its numbers (§9, F2-m1),
  and §9.9 item 6 reads **PASS with that residual recorded**. The Director may read it otherwise; the figures above are
  what the ruling asks for (paired, n ≥ 5, desktop and phone, fr and ar), with the base's own figures beside them.
- **A note on method, for the steward's DL entry.** The twin's absolutes are a night measure. A daytime figure without
  the base twin's figure beside it says nothing; every INP figure recorded for V5.22 should carry the base's.

---

## 8 · Scores (§26; 3 = clean but editorial or static) and §9.9

| Page | Composition | Motion | Imagery | Interaction | Institutional | Coherence |
|---|---|---|---|---|---|---|
| /fr/ 1440 · 390 | 4.5 | 4.5 | 4.0 | 4.0 | 4.5 | 4.5 |
| /ar/ 1440 · 390 | 4.5 | 4.5 | 4.0 | 4.0 | 4.5 | **4.5** (was 4.0: F-M1) |
| /it/, /en/ (1440 · 390) | 4.5 | 4.5 | 4.0 | 4.0 | 4.5 | 4.5 |

Why: composition and motion as the final review found them (nothing in this round changes a composition or a verb;
held at 4.5 by F-m4's rhythm, the Director's call); imagery 4.0 (lane M's ecosystem frame, the stage without an image);
institutional 4.5 in all four languages with the lead in the page's language; coherence 4.5 in Arabic now that the
moment stands on one alignment. Interaction stays at 4.0 (the bar): the tabs, the phone disclosures, the plates' links,
the key's turn, the halves' veil and the stage's mask are as the final review measured them, and the first pointer
after the keyboard on the desktop still carries the residual of §7 — not lane H's to trim.

| # | §9.9 item | Result |
|---|---|---|
| 1 | ≥ 4.5 composition and coherence, ≥ 4 the rest, at 1440 and 390 in fr and ar | **PASS** (§8) |
| 2 | headed: overflow, RTL, reduced motion, keyboard, no-JS — targeted per V5.25 at 1440 and 390 fr/ar, plus the pilot at the 8 widths × 4 languages and the closed gate at 1440/1280/1024/390 fr/ar | **PASS** (§2, §4) |
| 3 | WCAG 2.2 AA: axe 0 serious/critical, rings, names and roles | **PASS** (§4) |
| 4 | locked copy byte-identical, notices visible, both G3 states | **PASS** (§5 tests; §3) |
| 5 | the Word/PDF test fails for every V2 section | **PASS** (unchanged since the final review's table) |
| 6 | budgets recorded; INP within §5.3 under the ruling | budgets **PASS**; INP: §7 |
| 7 | the V5.20 final gate on the integrated tree | not this review's; the targeted suites §5 |
| 8 | preview label «Homepage Composition V2» | the steward's, at the merge |

---

## 9 · Findings

### Major

None.

### Minor

- **F2-m1 · The first pointer input after the keyboard on the desktop twin is over the 200 ms p75 budget on both
  trees** (lane 216 fr · 248 ar; the base 176 · 208; the lane's share +32 · +24 ms HL on the night run; §7). **Carried
  to S-close by the Director's ruling** («the residual trim is lane S's follow-up»). Attribution for the trim: the
  preserved `main.css` modality rules (115 links, 16 buttons under `html[data-input="key"]`; §9.8 — a decision for
  after acceptance, or a class-led subject if the Director opens it), lane S's vocabulary guards (≈ 150 elements) and
  keyboard tier (39, NOTES §14.3 route (a)); lane H's one rule: 9 elements. Re-measure at night, both slots, n ≥ 9,
  the base's figures beside the lane's.
- **F2-m2 · (= F-m3, carried: lane S / S-close)** «la protezione»'s guillemets break from their word on phones
  («« vendre / » un visa» at 390) — still so (`sweep_frar/fr_390_antifraud.png`); `components/sezioni/protezione.html`,
  a no-wrap span through `locked_spans`, `textContent` byte-identical.
- **F2-m3 · (= F-m4, carried: the Director)** rhythm — the moment 738 px after the 1 515 px integrity band at
  1440 × 900 (§3.1 ≈ 82 vh; §1 rule 5 ≥ 1 viewport); unchanged, a composition call, not a defect of this round.
- **F2-m4 · (= F-m6, carried: S-close / the Director)** the orientation's caveat plate on the Arabic page
  (`.linea__terminale`, `_linea-v2.css`): its rule on the reading edge, its French line from the plate's far end; the
  ruling S2's reviewer gave «la protezione»'s wide plates, or that plate's treatment.
- **F2-m5 · The steward's merge steps (= F-m5's remainder).** OWNERSHIP family `v522-h` (whole files `static/css/v5/_casa.css`,
  `templates/pages/home/_ecosystem_frame.html`, `_ecosystem_colophon.html`, `apps/pages/tests/test_home_v522_h.py`,
  `test_home_browser_v522_h.py`; slices for the shared files the lane changed, including lane S's two guards and
  `locale/**`), `check_ownership` on the branch; the catalogue step is +0 −0 (already carried); `seed_all --only
  pages.home_sections` on each shared database (`ile_v5`, `ile_v5_perf`; the old lead moves to the new default, an
  editor's text is never touched — `SUPERSEDED_DEFAULTS`); the preview label «Homepage Composition V2»; the DL entry
  **recording the Director's ruling on F-M2 in its words** and the figures of §7 (the night run's four cells and the
  desktop residual); live_status, the Italian changelog, the annotated tag; the preview restarted with the acceptance
  launcher and verified.
- **F2-m6 · The home's CSS total sits exactly at its 61 440 B ceiling** (0 B headroom; `pages.css` 11 306 / 12 288 has
  room of its own, the page total has none). Recorded: any later byte in `core/reveal.css`, `core/portico.css`,
  `hero.css` or `pages.css` on the home needs an equivalent rewrite or a ceiling decision by the Director.

### Observations (no action)

- A French question in the trust plates breaks at its hyphen at 390 («délivre- / t-elle») — a legitimate French break
  opportunity, unchanged since round 3, not raised.
- The Lume pre-warm veil (preserved, recorded deliberate) and the footer's stitched-capture differences, as the final
  review noted.
- The interrupted 3 November attempt of this review left its artefacts under this label (`.work/v522-h-final-qa2/`): a
  detached scratch worktree of `C:/tmp/italylegalentry` at `d5ba7c19` (clean, with a `node_modules` junction), the night
  INP data (kept as `data/prev_3nov/inp_home.json` and used as the measure of record, §7), and an empty migrate log.
  Their tools folder was overwritten by this run's copies before it was noticed; nothing of the attempt reached any
  repository or the evidence folder.

---

## 10 · Housekeeping

- Servers 8785 (PID 11000), 8788 (27896) and 8789 (28044) stopped at 17:35; nothing listens on those ports; 8780
  (`/fr/` 200) and 8782 untouched. No lock slot held (A and B free; `C:/tmp/ile_locks/` holds no `CHROMIUM_LOCK_*`).
- The interrupted attempt's scratch worktree (`.work/v522-h-final-qa2/wt`, detached at `d5ba7c19`, clean): its
  `node_modules` junction removed first (the link only), then `git worktree remove` — no longer listed by
  `C:/tmp/italylegalentry`. The clean archive `trees/lane`'s junction removed the same way; the archive, the twins'
  static roots and the data stay in `.work/v522-h-final-qa2/` (outside every repository).
- No repository's working tree, branch or tag written: `v522-h` clean at `d5ba7c19`, `design-v5` clean at `28fa9fa2`,
  `main` clean. Nothing pushed, merged, tagged or deployed; the lane worktree's own `node_modules` junction untouched.
- One database write outside the repositories: pytest's own `test_ile_v5_l5` / `test_ile_v5_l5b` (created and reused by
  pytest-django); the lane database `ile_v5_l5` served, not changed by this review.
- This report writes no contact number; some captures show the site's footer as the site draws it.
