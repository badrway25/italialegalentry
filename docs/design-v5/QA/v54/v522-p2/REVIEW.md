# V5.22 · Lane P2 (system, trust and reading) · final senior design-engineering review, round 2 (label `v522-p2-final-qa2`)

5 November 2026, 16:15–17:30. Senior design-engineering reviewer of lane P2. (A first attempt at this round, 3 November
00:32–00:34, was cut by the account limit after an export of the tree and two builds; nothing of it was used but the folder.)

**What was reviewed.** Branch `v522-p2` (worktree `C:/tmp/ile_wt/v522-p2`), head
**`6118d5433f8e0a301b207fad1be97448cba8d1e0`**: the final improve round `6118d54` on its merge `b995367` of design-v5
**`28fa9fa2`** (tag `v522/s2`, DL54-184). `git merge-base --is-ancestor 28fa9fa2 HEAD` holds, so the branch *is* the
integrated tree: no scratch merge this time, the worktree itself was served and tested. `b995367` differs from the clean
merge-tree `53d5c2c` of the last review in exactly the four dist sheets that bundle lane S's partials (`cms/faq.css`,
`cms/lettura.css`, `forum/forum.css`, `pages/css/interior.css`), as the builder says. No repository was written: `git status`
of the P2 worktree empty before and after, design-v5 untouched; the build check ran on a `git archive` export outside every
repository (`.work/v522-p2-final-qa2/trees/h`).

**Judged against.** `V5_25_FINAL_DELIVERY_ACCELERATION_SHORT.md` (targeted checks of what changed, no new score loop, «≥ 4 on
the six dimensions and no blocker → merge»), `V5_26` (professional judgement), `V5_22_…REMEDIATION.md`, `V5_23`,
`SECTION_SYSTEM_V2.md` (§5.3, §9.7, §9.8, §9.9, §10), the V5.12–V5.21 standing rules and V5.20's strict test rule; the
previous round `finish/v522-p2-final-qa1.md` (M1, m1–m6) and the builder's account, NOTES «Final improve round» (FI.1–FI.10).

**Servers** (started and stopped by this review; 8780 untouched; lane H's final review ran beside this one all along):

| Port | Tree | Use |
|---|---|---|
| 8787 | the P2 worktree at `6118d54` | lane server: dev settings, database lane l7 (`ile_v5_l7`), `ILE_DESIGN_PREVIEW=1`, reference date 2026-10-03 (G3 open), the configured WhatsApp number read in process from the preview's untracked `.env` (option B; never printed) |
| 8797 | the same | **compressed twin**: DEBUG off, `CompressedManifestStaticFilesStorage`, private `STATIC_ROOT` (`twin/static-q`, 1 086 files collected, 2 284 post-processed), built as 8782 is |

**Browser and locks.** Headed **chromium-1234** (Playwright) for every visual check and measure; the suites headless as they
launch. Every Chromium run inside a lock slot (`CHROMIUM_LOCK_A`/`_B`, label `v522-p2-final-qa2 <session>`), five sessions,
the longest 19 min 17 s (`browser-1`), each released (`.work/v522-p2-final-qa2/logs/locks.log`); the other slot was lane H's
final review (`v522-h-final-qa2`) throughout, so every timing below carries that load. pytest one per test database:
`test_ile_v5_l7`, `…_l7f`, `…_l7g`, `…_l7h`.

**Where things are.** Report: this file. Screenshots beside it in `finish/v522-p2-final-qa2/` (prefixes in §9). Tools, raw
JSON and logs: `C:/tmp/ile_v5_council/.work/v522-p2-final-qa2/` (`tools/`, `data/`, `logs/`, `trees/h`, `twin/`). No text
evidence of this review carries the configured WhatsApp number (masked in process); the site's own footer and contact board
show it in captures, as the site draws it.

---

## 0 · Verdict — PASSED: 0 major, 3 minor (none of them lane P2's to fix before the merge)

**The branch passes §9.9 on the integrated tree and may be merged.** The one major of round 1 — the integration gate — is
fixed at the root: lane P2's three templates write the library's `data-registro`, guard (c) and the three icon-count cases
are green on the branch (374 passed, §6), MC-1's P2 half is on the branch (the phone's first paint shows the address's
answer, W1-C's same-document step restored, the permalink test tightened, the spy test counting the sommaire's own links),
and every browser module that visits the lane's pages is green (68 + §6). Round 1's four fixable minors are fixed and
measured here: AGAMI's identity band plays its signature in view at load in both languages, its portico drawn from the
reading edge on the Arabic page (m2); the rows of the two V2 disclosures never wait for the legacy rise (m3); a dictionary
card answers the hand in place, so a mouse reader's rail lights all eight letters at every width and pointer position (m1);
m4's residue is traced and inside the gate (§1). The targeted checks of V5.25 §2 hold (§4): 30 of 30 phone permalinks at
390/375/360 fr/ar land on their open answer alone with CLS 0, the Réseau entry comes into view 40 of 40 at 430/390/375/360,
the Vivre seam is 0 px on one ground, the Forum head's drawing hangs on the title's line with 0 px² over the index, the
sommaire lights 5 of 5, the glossary rail 8 of 8 in 24 read-throughs. Contact channels unchanged, locked copy byte-identical
(188 checks), budgets inside every ceiling (the glossary family exactly at its 54 272), `main.css` at its ratchet, nothing
loosened, no new string, the build reproducible and the committed dist current.

| §9.9 item | Result |
|---|---|
| 1 · Scores ≥ 4, every owned page, six dimensions | **PASS** (§3 — a sanity look at 1440 and 390 fr/ar; two dimensions a change affected rise by half a point, none falls) |
| 2 · Headed Chromium, widths × languages, reduced motion, keyboard, no-JS | **PASS** — targeted per V5.25 §2 on what changed (§4); round 1's 320-run sweep, keyboard walks and no-JS runs stand for what did not change (no preserved family, no template structure, no script in P2's round) |
| 3 · WCAG 2.2 AA, axe 0 serious/critical | **PASS** — 40 runs on the six pages the round touched, at rest and in their interactive states: 0 violations (m5 of round 1 was not reproduced in these runs; recorded as before) |
| 4 · Locked copy byte-identical, legal notices visible | **PASS** (188 checks fr/it/en/ar; the notices in every sanity still) |
| 5 · Word/PDF test fails for every V2 section | **PASS** (no section changed its nature this round) |
| 6 · Budgets; LCP/CLS on the twin | **PASS** (§5; the Forum's phone LCP medians inside 2.5 s, its head CLS ≤ 0.019 — with a note on today's shared machine, m2) |
| 7 · V5.20 final gate on the integrated tree | **PASS** — the four red tests green, 374 + 492 + 68 + the §6 browser batch, 0 failed, 0 skipped, check / migrations / ruff clean, the build reproducible |
| 8 · Preview label «Page Composition V2» | steward, at merge |

---

## 1 · Round 1's findings — verified (fixed / not fixed)

Measured on the branch served at 8787, headed chromium-1234, unless named.

| Finding | Status | Measured |
|---|---|---|
| **M1** the integration gate: three templates wrote the bare `data-register`; MC-1's P2 half not on the branch | **Fixed** | `/fr/forum/`, `/fr/le-projet/`, `/fr/reseau/` (and `/ar/`) carry `data-registro` (1, 2, 2 per page) and no bare `data-register` (0). Guard (c) `test_data_register_is_written_by_the_partial_and_by_two_legends_only` **green**; `test_interior_w3_f1.py::test_one_primary_action_and_at_most_six_icons_in_the_body` **green** for the three routes — 374 passed in the guards' run (§6). W1-C's same-document step is back in `test_browser_w1_c.py` with the floor 2 → 3, cited (V5.20); the P2 permalink test asserts «shown == [the named answer] and exactly one button expanded» below 64 rem (stronger than «no other shown»); the spy test compares with the sommaire's own links (≥ 5) — 68 passed in the browser batch, the two tests among them |
| **m1** glossary rail: a mouse reader's read-through skipped a row's first letters | **Fixed** (P2's part; the root stays lane S's) | `spyhover.py` (round 1's method): fr/ar × 1440/1280/1024/768 × pointer in the margin / on the register's end side / on its start side = **24 read-throughs, all eight letters lit in every one** (round 1: C, L, P, Q missing at 1440, L, P at 1024, P, R / L, P, R at 768 with the pointer on the register). The hovered card stays on its row (tops equal to 0.1 px; `translate: none`), its letter fills, its rule runs to 1 (`eye_q.json`); Vivre's cards, the same component, answer the same way. `data/spyhover_q.json`; `eye_q_glossaire_{fr,ar}_1440_card_hover.jpg`, `eye_q_vivre_*` |
| **m2** AGAMI's first band never played its signature | **Fixed** | sampled every ~70 ms from `commit` through 3 s (`data/targeted_q.json`): at 1440 and 390, fr and ar, the band has no section state (in view at load, also at 1024 and 768), and `sez-mask` runs on the plate, `sez-stroke` on the colonnade, `sez-draw` on the connector (1440); the animations end (`running` 0 at 3 s); under reduced motion 0 animation in the band; `.colonnato` `scale: -1 1` on the Arabic page, the plate opening from the right. Seen: `tg_q_agami_{fr,ar}_{1440,390}_load_{500,900,1400,2600}ms.jpg` — the plate a sliver at 0.5 s, half open with the lines drawing at 0.9 s, the portico drawn at 1.4 s, at rest at 2.6 s; `tg_q_agami_ar_1440_rest_rm.jpg` the mirrored portico at rest |
| **m3** text held by the legacy rise inside two V2 sections | **Fixed** | AGAMI's question row and the term page's three related rows: `data-rise=""` is still written by the runtime (at 390 every one; at 1440 the last term row), **opacity 1, translate none** in every sample from the first frame (the minimum over the band's 40 samples 1.0), at 1440 and 390 fr/ar. `tg_q_terme_{fr,ar}_390_rows_entering.jpg` |
| **m4** FAQ arrival at 768: a shift up to 0.055 | **Traced, not fixable in CSS** (recorded for the Director — FI.6) | the phone widths this round asked for are clean: 30 of 30 arrivals at 390/375/360 fr/ar **CLS 0** with the named answer shown alone at `DOMContentLoaded` (the `:not(:target)` first-paint rule); round 1 measured the 768 residue (fr «visas» 0.055, «pré-évaluation» 0.027) and the builder traced it to the frame Chromium paints before `:target` matches; inside the 0.1 gate |
| **m5** axe `target-size` in one interactive state (term page, 1024, it/en) | **Not reproduced** in this round's 40 runs (fr/ar × 1440/390; the state is width- and language-bound) | no action was asked of P2; stands as recorded |
| **m6** the register readers' regex `data-registr(?:o|er)` | **Open — lane S / S-close** | `test_interior_w3_f1.py:335`, `test_orientation_w3_f1.py:118` unchanged (lane S's modules; P2 may not edit them); harmless to P2 now that its templates write `data-registro` |
| S2 review **m1** (the Forum spy assertion counted a constant) | **Fixed** | the test compares with the sommaire's own links; on the lane database (the event past at 2026-10-03) the sommaire lists 5 and 5 light; on the test database 7 and 7 (the builder's run) |
| S2 review **m2** (the chip's attribute) | **Fixed** (= M1) | — |
| MC-4 / FI.1 the merge of `28fa9fa` and the dist | **Done** | `npm run build` twice on the export: **77 dist files, every hash equal to the committed dist and to each other** (`data/dist_{head,build1,build2}.sha`) |
| MC-5 ownership family `v522-p2` | **Open — steward, at merge** | `check_ownership.py v522-p2 28fa9fa --head HEAD` → «unknown family 'v522-p2'» (the id rule needs `v5<nn>-p2`); P2's diff over design-v5 is 85 files: its route sheets and partials, the catalogue (8 files, +160 lines: the lane's ten msgids, it/en/ar), the cited slices of S-family test modules, its NOTES; no preserved family (§7) |

---

## 2 · Findings

### Major — none.

### Minor

- **m1 · One of lane S's browser tests red once in batch 2, green alone — timing under load, not P2's** (lane S,
  for S-close). `tests/frontend/test_sezioni_browser_v522_s2.py::test_an_explorer_permalink_lands_on_its_open_answer_and_follows_the_address[fr]`
  failed its phone step «its heading in view» (the heading at y 968–1 024 on an 844 px screen, 700 ms after the
  same-document hash change); the `[ar]` case and the 70 other tests of the batch passed, and **the test re-run alone passed,
  fr and ar (2 passed, 10.8 s)**. It runs on lane S's own fixture page (`fx.page("explorer")`, which links `main.css`,
  `reveal.css`, `fronte.css` and `core/sezioni.css` — none of P2's sheets), and `sezioni/indice.js` brings the heading in
  with `scrollIntoView({behavior: "smooth"})`: on a loaded machine (both Chromium slots busy at that minute) the smooth
  scroll outlasts the test's fixed 700 ms. Suggested for lane S: wait for the heading's box instead of a fixed 700 ms
  (`wait_for_function` on `getBoundingClientRect().bottom <= innerHeight`). Not a P2 defect; nothing in P2's round touches the
  fixture, the module or the library.
- **m2 · The Forum's phone LCP on the twin today: medians inside the gate, three cold loads of twenty over it**
  (`perf_twin_q.json`, `perf_twin_q2.json`; 2 × n = 5, network A 150 ms / 1.6 Mbit/s, CPU × 4, cache off, 412 × 823
  @1.75): fr **2 146 ms** median over ten loads (1 988–2 544), ar **2 360 ms** (2 120–2 524), CLS 0 on every load; the desk
  1 520–1 912 ms, CLS ≤ 0.0198 (the head, m6 of round 3, holds). Round 1 measured 1 780 / 1 952 ms (n = 3) on the same
  Forum sheets — `forum/forum.css` is byte-identical since (`36d694b9`), the Forum's templates changed one attribute token;
  the +350–400 ms is today's machine (lane H's final review ran beside this one; its desk numbers moved the same way). Not a
  finding against P2: §5.3 wants n ≥ 9 on 8782 at the one exhaustive gate (V5.25 §7); recorded so that gate's Arabic Forum
  measure is read with this in mind.
- **m3 · `ruff format --check` on `tests/frontend/test_browser_w1_c.py`** (W1-C's module): not format-clean, as before the
  round — two long asserts outside the restored lines; `ruff check .` is clean. Pre-existing on design-v5; the steward's
  merge gate is `ruff check`. Left as it was, recorded.

Carried from round 1 without change, not lane P2's: m4's 768 residue (Director), m5 (no action), m6 and m1's root (lane S,
S-close), S2's request 8.3 third bullet (`_projet.css` universal keyboard subject — closing), round 3's m3 (the route sheets'
extra request — Director).

---

## 3 · Scores (§26, 1–5; the bar ≥ 4; V5.25 §5: no re-scoring beyond a sanity look)

Sanity look on the branch at 1440 and 390 in fr and ar: the ten pages read through once each with their entrances played,
captured whole (`sane_q_<page>_<lang>_<w>.jpg`, 40 stills; `data/sanity_q.json`: **0 px horizontal overflow, one h1, 0
console error** in the 40 runs). Round 1's scores carried; the two dimensions a change of this round affected are re-read
and marked in bold; nothing falls.

| Page | Comp. | Motion | Imagery | Interaction | Institutional | Coherence | Note |
|---|---|---|---|---|---|---|---|
| Le projet | 4.5 | 4 | 4.5 | 4 | 4.5 | 4.5 | = ; the four arched doors whole in the viewport (`eye_q_projet_fr_1440_doors.jpg`; the full-page capture's slivers are the capture's), the panorama's credit whole inside its frame and the viewport (fr and ar, `eye_q.json`) |
| Réseau | 4.5 | 4 | 4 | 4.5 | 4.5 | 4.5 | = ; MC-3 at 430/390/375/360 |
| Contact | 4 | 4 | 4 | 4.5 | 4.5 | 4.5 | = ; the three doors whole in the viewport |
| FAQ | 4 | 4 | 4 | 4.5 | 4.5 | 4.5 | = ; a phone permalink lands on its open answer at the first paint |
| Glossaire | 4 | 4 | 4 | **4.5** | 4 | 4 | interaction 4 → 4.5: the rail now lights every letter under a resting pointer, the card answers in place (letter, rule, shadow) — the one thing that held it at 4 is gone; institutional and coherence stay half a point under their §10 target (recorded since round 3) |
| Glossaire, term page | 4 | 4 | 4 | 4 | 4.5 | 4.5 | = ; the related rows never wait |
| Vivre en Italie | 4 | 4 | 4.5 | 4 | 4.5 | 4.5 | = ; the seam 0 px at 1440/1024/768/390 fr/ar |
| Forum | 4 | 4 | 4 | 4 | 4.5 | 4 | = ; the drawing on the title's line, the sommaire 5 of 5 |
| AGAMI | 4 | **4.5** | 4 | 4 | 4.5 | 4.5 | motion 4 → 4.5: the identity band now plays AG-1's signature (mask, colonnade, connector) in view at load, its question row stands at rest; with the night plate's draw + node and the approdo's settle + light the page has four distinct signatures and nothing legacy inside a V2 section |
| Attention aux fraudes | 4 | 4 | 4 | 4 | 4.5 | 4 | = |

«Would a senior designer, without context, call it a premium institutional legal-tech platform rather than an online report
with cards?» — yes for the ten pages, as in round 1; nothing in the 40 stills reads as a regression.

---

## 4 · Targeted checks (V5.25 §2) — what changed since round 1

- **The register markers.** The three pages in fr and ar: `data-registro` present (Forum 1, Le projet 2, Réseau 2), the
  bare marker absent, a valued `data-register="…"` absent (HTML of 8787).
- **The FAQ's phone first paint and permalinks** (`targeted.py` part `faq`; `data/targeted_q.json`): fr/ar × 390/375/360 ×
  the five anchors (the four trust keys and the fraud question), each arrived at from the fraud page: at
  `DOMContentLoaded` — before the module — the named answer is shown and **no other** (30 of 30); settled: shown alone, in
  view, under the letterhead with its question 88 px from the top, exactly one button expanded, **CLS 0 in all 30**. A plain
  `/faq/` on the same phones: 0 answers shown, 0 expanded before the module (the first paint folded, as designed). Same
  document: `#faq_diplomas` then `#faq_visas` from the address bar, 12 of 12 followed (the answer open alone, its question 72
  px from the top). `tg_q_faq_{fr,ar}_{390,375,360}_permalink_diplomas.jpg`, `…_360_permalink_visas.jpg`,
  `…_390_samedoc_visas.jpg`.
- **The glossary rail and the Forum sommaire spy** (`spyhover.py`, `targeted.py` part `forum`): §1 m1 — 24 of 24
  read-throughs light all eight letters; the rows read as one stop (C·D, L·N, P·Q·R, V at 1440 and 1280; C, D, L·N, P·Q, R·V
  at 1024 and 768). Forum at 1440 fr/ar: every sommaire entry lit in a wheel read-through, 5 of 5 (`forumspy`).
- **Réseau phone entry** (part `map`): each of the 5 actors tapped in turn, fr/ar × 430/390/375/360 = **40 of 40 entries in
  view** (top 409–620 px, bottom 8 px above the screen's foot; the page scrolls to it). `tg_q_reseau_{fr,ar}_{430,360}_chosen_professionals.jpg`.
- **The Vivre seam** (part `vivre`): fr/ar × 1440/1024/768/390: gap **0 px**, seam 0 px, the moment's ground = the band's
  (`rgb(236 235 230)`) — 8 of 8. `tg_q_vivre_{fr,ar}_{1440,390}_seam.jpg`.
- **The Forum head** (part `forum`, reduced motion, 1440/1024 fr/ar): the drawing hangs **72 px** from the head's top — the
  title's line —, never cut, **0 px² over the index**; on the twin see §5. `tg_q_forum_{fr,ar}_{1440,1024}_head.jpg`.
- **AGAMI's band and the two disclosures** (part `agami`): §1 m2 and m3; at 1024 × 768 and 768 × 1024 the band is also in
  view at load (top 429–454 px) and plays the same sequence (`agami-scroll`); `tg_q_agami_{fr,ar}_768_scrolled.jpg`.
- **axe-core 4.13** (WCAG 2.0–2.2 A/AA; `axe_q_fr-ar_1440-390.json`): the six pages the round touched (AGAMI, Glossaire,
  the term page, FAQ, Forum, Réseau) × fr/ar × 1440/390, at rest after a read-through and in their interactive states (the
  FAQ's fourth answer, the map's institutions, AGAMI's and the term page's disclosures open): **40 runs, 0 violations**.
- **Contact channels (V5.19, option B)** (`contact_check.py`): fr/it/en/ar — one WhatsApp link whose digits end in the
  configured number (read in process), one `tel:800642015`, both numbers in `<bdi dir="ltr">`, each link named; the
  configured number in **no tracked file of HEAD** (`git grep`, 0) and in **no line of P2's diff** over design-v5 (both
  forms, 0). `test_contact_channels_v519` and its browser module green with the number set (§6).
- **Locked copy and Q9** (`lockcheck.py`): **188 checks byte-identical** in fr/it/en/ar — every `[data-locked]` element on
  the ten pages, the FAQ's nine questions and answers, the ten terms and definitions (Glossaire, Vivre), the term page's
  definition and related definitions, the fraud page's question and answer (once each), AGAMI's `faq_who`. No registry or
  checksum in P2's diff; `locale/` unchanged this round (+0 −0).
- **Nothing loosened** (V5.20 strict rule, the round's diff read line by line): `test_browser_w1_c.py` restores W1-C's step
  and raises the floor 2 → 3 (cited); `test_pages_browser_v522_p2.py` tightens the permalink assertion and replaces a constant
  by the sommaire's own count with a floor of five, and adds three tests that fail on the round's starting sheets (the
  builder's swap-in run, FI.9); `test_interior_v522.py` and `test_forum_v522.py` read the renamed marker, the same invariant.
  No other test module changed.
- **The CSS of the round, read.** `_faq-v2.css`: below 64 rem `.indice__pannello:not(:target) .indice__corpo` hidden under
  `.js` only — a no-JS reader still sees every answer; `_lessico-v2.css`: the two rules share one declaration block (the
  glossary family had no byte to spare), the seal's draw moved into the same `prefers-reduced-motion: no-preference` block
  as the panorama's scale (verified: the enclosing block at line 424 is that media query, not a width query), `1360ms` =
  `calc(160ms + 1200ms)`; `_agami.css`: the load sequence keyed `:root.js:not(.rm):not([data-input="key"]) .agami-identita:not([data-sec-state])`
  — a band below the fold gets `data-sec-state="wait"` from `rise.js` at load, so the selector releases it and the runtime
  plays the signature on its trigger (the runtime's contract, `rise.js` line 24); `[dir="rtl"] .colonnato { scale: -1 1 }`
  on a drawing symmetric about its middle; `v5/_lettura.css`: the removed `.page-header__recipients` rule is written by no
  template, Python or script on HEAD (`git grep`: only the NOTES mention it).

---

## 5 · Budgets and performance

**CSS, gzip -9, the tests' method** (`budgets_q.json`; fr = it = en = ar):

| Sheet | Branch | Round 1 | Ceiling |
|---|---|---|---|
| `main.css` | **32 716** | 32 716 | 32 718 (the ratchet; untouched) |
| `pages/css/interior.css` | 8 827 | 8 827 | 11 264 |
| `cms/lettura.css` | 6 512 | 6 529 | 9 216 |
| `cms/faq.css` | 1 935 | 1 929 (T2 1 935) | 2 048 |
| `cms/lessico.css` | 2 384 | 2 356 | 2 560 |
| `pages/css/agami.css` | 1 760 | 1 667 | 2 048 |
| `pages/css/rete.css` · `frodi.css` · `forum/forum.css` | 1 817 · 1 200 · 7 369 | = | 2 048 · 1 536 · 8 192 |

| Page total | Branch | Ceiling |
|---|---|---|
| Le projet, Contact | 54 203 | 56 320 |
| Réseau | 56 020 | 56 320 |
| AGAMI | 55 963 | 56 320 |
| Fraudes | 55 403 | 56 320 |
| FAQ | 53 823 | 54 272 |
| Glossaire, term page, Vivre | **54 272** | 54 272 (0 B left) |
| Forum | 46 604 | 54 272 |

The glossary family stands exactly at its ceiling (the builder's FI.8: the next rule there needs a saving first — S-close's
ratchet or a Vivre-only sheet). `test_frontispiece_v515_c` (ceilings and totals) and `test_css_bundle_is_current` green (§6).
No JS source of P2's.

**Performance — the compressed twin 8797** (the Forum, the one page whose head CLS was a finding; n = 5 phone, 4 desk;
network A, CPU × 4, cold; both Chromium slots busy, see m2):

| View · page | fr: LCP median (min–max) ms · CLS max | ar: LCP median (min–max) ms · CLS max |
|---|---|---|
| phone · Forum, series 1 (lane H's browser suite in the other slot) | 2 144 (1 988–2 544) · 0.0 | 2 308 (2 120–2 524) · 0.0 |
| phone · Forum, series 2 (both slots free) | 2 148 (2 084–2 492) · 0.0 | 2 404 (2 296–2 468) · 0.0 |
| desk · Forum, series 1 / 2 | 1 520 / 1 574 · 0.0126 / 0.0122 | 1 672 / 1 912 · 0.0191 / 0.0198 |

Over the ten phone loads per language: fr median 2 146 ms, ar 2 360 ms, **CLS 0 on all 20**; three loads of twenty above
2.5 s, all in series 1 and none in series 2 (`perf_twin_q.json`, `perf_twin_q2.json`). Three blocking sheets of four on the
phone (the Forum has no route sheet), 103 / 135 kB transferred; the phone's LCP element is the head's title. The head's CLS
is the m6 (round 3) measure: ≤ 0.020 (round 1: 0.0095 / 0.0186). INP not re-measured:
lane P2 ships no script and changed none; `v522/s2`'s first-input measures on the compressed twins stand. The Director's
ruling of this round on lane H's F-M2 (the absolute §5.3 budget — first-Tab and first-pointer-after-keyboard INP ≤ 200 ms at
p75 on the compressed twin, paired with the base, n ≥ 5 — replacing the relative «within 20 ms») concerns lane H's review and
its DL entry; it is recorded here because lane S's `motion.css` INP rule and the class-led modality rules reached this branch
with `28fa9fa`, and nothing of P2's touches them.

---

## 6 · Tests (one pytest per test database; the browser suites headless as they launch, each inside a lock slot)

| Run | Test DB | Result |
|---|---|---|
| The four guards and their readers + the lane's static modules: `test_state_chips_carry_a_register`, `test_interior_w3_f1`, `test_orientation_w3_f1`, `test_o14_lint`, `apps/pages/tests/test_interior_v522`, `apps/forum/tests/test_forum_v522` | l7 | **374 passed** (12 min 33 s) — guard (c) and the three icon-count cases green (round 1: 1 + 3 red) |
| Targeted non-browser with the configured number and the private sentinel table (read in process): `apps/pages/tests/test_contact_channels_v519`, `test_frontispiece_v515_c`, `test_css_bundle_is_current`, `test_sezioni_v522_s`, `test_sezioni_v522_s2`, `test_content_pages_w3_f2`, `tests/security/test_confidential_material`, `tests/i18n/test_rtl_static`, `tests/i18n/test_ui_translations` | l7f | **492 passed, 0 skipped** (15 min 38 s) |
| Browser batch 1: `test_pages_browser_v522_p2` (54 — the new spy, card, band and rows tests among them), `test_browser_w1_c` (the restored step), `test_browser_contact_channels_v519` (the configured number) | l7g | **68 passed** (19 min 13 s) |
| Browser batch 2 — lane S's checks on the merged pages: `test_sezioni_browser_v522_s2` (16), `test_motion_v512_a_w2` (20), `tests/i18n/test_rtl_browser` (23), `test_content_pages_browser_w3_f2` (13) | l7h | **71 passed, 1 failed** (9 min 33 s) — the one failure is m1 (lane S's fixture test, a 700 ms wait on a smooth scroll under load); **re-run alone: 2 passed** (fr, ar; `rerun_s2_q.log`) |

**Checks on the worktree:** `ruff check .` clean; `manage.py check` no issue; `makemigrations --check` no change;
`git diff --check` clean; every file of the round LF in the index (`git ls-files --eol`: `i/lf` for all 16); `npm run build`
twice on the export of HEAD — 77 dist files, every hash equal to the committed dist (the build is reproducible and the
dist current); `ruff format --check` on the round's four Python files: three formatted, `test_browser_w1_c.py` not (m3).

---

## 7 · Preserved families, ownership, compliance

- **Preserved families (§9.8).** P2's 85-file diff over design-v5 touches no navbar, mega menu, phone sheet, footer, Lume
  (`lume.css`, `loader.css`, `motion.css`, `head.js`), form component or sheet, `base.html`, `tokens.css`, `main.css`,
  portal, privacy or cookie file, `apps/core/contact.py`, locked registry or checksum (path search). `institutional_base.html`
  gains only the `{% block route_sheet %}` hook between `interior.css` and `fronte.css` (round 3's recorded deviation).
- **Ownership (§9.7).** This round's 16 files: the lane's two route partials and sheet (`_faq-v2.css`, `_lessico-v2.css`,
  `_agami.css`), the shared reading partial `v5/_lettura.css` (one dead rule removed — a saving the glossary family needed;
  the rule was the lane's own since P1's collaboration head, written by nothing), its three templates, its four dist sheets,
  its two static test modules, its browser module, `test_browser_w1_c.py` (the cited slice MC-1 asked of this lane), its
  NOTES. No file of lane S's.
- **Q4 / Q5 / Q8.** Unchanged since round 1: the Forum's imagery drawn, AGAMI without a photograph, Vivre without a theme
  card or «coming soon», the fraud page adding no authority or portal link, nothing presenting ILE as an authority.
- **Images.** No new image or slot; the panorama's credit on Le projet whole in both languages (§3).
- **Privacy.** No personal datum in the round; the configured number in no tracked file (§4).

---

## 8 · Observations for lane S, the Director and the steward (not lane P2's findings)

- **Steward, at P2's merge:** MC-5 — the family `v522-p2` (the id rule needs `v5<nn>-p2`, `v516-p2` being taken), its route
  sheets, partials and templates, the catalogue (8 files), the cited slices of S-family test modules including
  `test_browser_w1_c.py`'s restored step; the catalogue pass for the lane's ten msgids and the five it no longer uses (FI.7);
  the preview label «Page Composition V2»; `forum/forum.css` and `pages/css/interior.css` carry no change of this round
  (their dist hashes equal `b995367`'s). The merge itself is a fast-forward of design-v5 to `6118d54` or a `--no-ff` merge of
  it; the build on the merged tree will be identical (verified here on HEAD).
- **Lane S / S-close:** m1's root (`spia.js` to group a row by layout position — then the lexicon's cards may take the
  library's lift back), m6 (the readers' regex), S2's request 8.3 third bullet.
- **Director:** FI.6 (m4's 768 residue, the frame before `:target`); round 3's m3 (the route sheets' extra request); the
  half-point gaps of §3 (Glossaire institutional and coherence, Forum coherence, Fraudes coherence — all at 4, targets 4.5);
  the twin's shared-machine note (m2) for the one exhaustive gate.
- **Lane H's review:** the Director's ruling on F-M2 as recorded in §5.

---

## 9 · Evidence (`C:/tmp/ile_v5_council/evidence/v522/finish/v522-p2-final-qa2/`)

- `tg_q_*` — the targeted checks: the FAQ permalinks at 390/375/360 (fr/ar), the same-document step at 390, the Réseau
  entry at 430 and 360, the Vivre seam at 1440 and 390, AGAMI's band at 500 / 900 / 1 400 / 2 600 ms after commit (fr/ar ×
  1440/390), its rest under reduced motion (the Arabic portico mirrored), the band at 768 after a scroll, the term page's rows
  entering at 390, the Forum head at 1440 and 1024.
- `sane_q_<page>_<lang>_<w>.jpg` — the 40 full pages of the sanity look (10 pages × fr/ar × 1440/390).
- `eye_q_*` — the viewport checks: Le projet's and Contact's doors, the panorama's credit, a card under the hand on the
  glossary and on Vivre (fr/ar, 1440).
- Data (`.work/v522-p2-final-qa2/data/`): `targeted_q.json`, `spyhover_q.json`, `sanity_q.json`, `eye_q.json`,
  `axe_q_fr-ar_1440-390.json`, `perf_twin_q.json`, `budgets_q.json`, `dist_{head,build1,build2}.sha`, `p2_files.txt`.
- Tools (`.work/v522-p2-final-qa2/tools/`): `c.py` (shared, re-pointed), `targeted.py`, `spyhover.py`, `sanity.py`, `eye.py`,
  `axe.py` (page filter), `perf_twin.py` (page filter), `budgets.py`, `lockcheck.py`, `contact_check.py`, `run.sh`,
  `run_dev.ps1`, `with_lock.sh`; `twin/` the twin's settings, launcher and `static-q`.
- Logs (`.work/v522-p2-final-qa2/logs/`): `guards_q.log`, `targeted_q.log`, `browser1_q.log`, `browser2_q.log`,
  `targeted_headed.log`, `spyhover.log`, `sanity.log`, `axe.log`, `perf_twin.log`, `eye.log`, `build{1,2}.log`,
  `srv8787.log`, `twin8797.log`, `locks.log`.
- Locks (`logs/locks.log`): five sessions — `browser-1` B 16:21:43–16:41:00 (19 min 17 s), `headed-1` B 16:41:19–16:51:31,
  `headed-2` B 16:51:53–16:59:33, `headed-3` A 17:00:11–17:10:24 (rc 1 = batch 2's one failure, m1), `headed-4` A
  17:11:14–17:12:58 — each released, none over 25 min, no slot taken over as stale; the other slot was lane H's final review
  (`v522-h-final-qa2`: pilot, inp-a, sanity, pytest_browser) through most of the hour.
- Housekeeping: servers 8787 and 8797 stopped (their PIDs killed, the ports free); 8780, lane H's 8785, 8788 and 8789
  untouched (8780 answers 200); no lock held at the end; the P2 worktree and design-v5 untouched (`git status --porcelain`
  empty on both, heads `6118d54` / `28fa9fa2`); the export `trees/h` (its `node_modules` junction removed) and the twin's
  `static-q` stay under `.work/v522-p2-final-qa2/` (outside every repository); the test databases `test_ile_v5_l7`, `…_l7f`,
  `…_l7g`, `…_l7h` remain on the local server (`--reuse-db`). No text file of this review carries the configured WhatsApp
  number (digit-run search over the report, the data and the logs, both forms: 0). Nothing pushed, merged, tagged or deployed.
