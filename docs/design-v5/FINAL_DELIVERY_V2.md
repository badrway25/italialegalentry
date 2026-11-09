# FINAL DELIVERY V2 — the Director's lane plan (Creative / Product Director, label `v524-director`)

5 November 2026, 19:30. Binding above this file: V5.24 (the owner's final-delivery remediation: typography, backgrounds/material,
Arabic, Pexels credits, the professional pass), V5.25 (final delivery mode: known defects, targeted checks, one matrix, one gate,
no score loops, stop conditions), V5.26 (professional judgement per section: tool → decision → implementation; «would an expert
digital product team have chosen this exact composition for this exact information?»), V5.22 (the composition remediation and its
standing constraints), V5.20 (the strict test-update rule and the final gate), V5.12 … V5.23 (locked copy never reworded or
machine-translated; Q1/Q4/Q5/Q8/Q9; privacy; the WhatsApp number never in a tracked file), and `docs/design-v5/SECTION_SYSTEM_V2.md`
on `design-v5` (§5.3 motion budget, §6 depth/typography, §7 budgets, §9.7 ownership, §9.8 preserved families, §9.9 acceptance,
§10 targets). The four audits this plan turns into work, read in full and adopted as written unless a ruling below says otherwise:
`evidence/v524/TYPOGRAPHY_V2.md` (v524-typo), `BACKGROUND_MATERIAL_V2.md` (v524-material), `IMAGERY_ATTRIBUTION.md` (v524-pexels),
`ARABIC_AUDIT.md` + `arabic/01…06` (v524-arabic). Repository rules apply to this file: no secret, no personal datum, no phone number.

**State at writing.** `design-v5` HEAD `4bafcfa0` = tag `v522/p2` (lanes S, M, P1, S2, H, P2 merged; DL54-181 … DL54-186). Lanes
H and P2 are merged; their worktrees (`C:/tmp/ile_wt/v522-h`, `v522-p2`) are history. The preview `http://127.0.0.1:8780` serves
`4bafcfa0` through the acceptance launcher (`C:/tmp/ile_v5_council/servers/acceptance/README.md`). Both Chromium lock slots and the
merge lock were free at 19:27. Measured on HEAD's dist (gzip -9): `main.css` 32 716 B; the home's five sheets 61 440 / 61 440;
Parcours 55 493 / 56 320; the glossary, term and Vivre pages 54 272 / 54 272; `pathways/index.css` 10 117 / 10 240;
`ecosystem/pilot.css` 9 508 / 9 728; `forum/forum.css` 7 369 / 8 192; `interior.css` 8 827 / 11 264; `lettura.css` 6 512 / 9 216.
Fonts shipped 77 240 B in six files.

---

> **AMENDMENT A1 — 5 November 2026, 20:30 (orchestrator, on the owner's V5.27 «ARABIC OWNER DECISION — FINAL», 20:08;
> `C:/tmp/ile_v5_council/directives/V5_27_ARABIC_OWNER_DECISION_FINAL.md`). Read before §2 and §3.8.** The owner answered
> question 1 of §6 with a HYBRID policy that is neither A, B nor C: (i) every non-legal, compositional locked key is rendered in
> **provisional professional Arabic now** (internally flagged «PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW», publicly complete);
> (ii) legal / substantive locked keys get **no team legal translation**: the authoritative **Italian** text is shown and identified
> as such where it exists; where the only source is the prescribed French, the block is shown **explicitly identified as
> source-language material** with an Arabic context line, or **hidden until validated** where it need not be exposed; French is never
> a silent fallback; (iii) **visible unintentional French in /ar/ = 0** with a controlled allowlist (proper names, official titles,
> quotations / source material displayed as such, identified source content); (iv) the rendered Arabic is verified natively
> (hierarchy, weight, leading, size, mixed Arabic/Italian terms, numerals, phone numbers, e-mail addresses, abbreviations, direction,
> arrows/chevrons, tabs, routes, actor map, FAQ, glossary, forms, mobile navigation); (v) the Arabic product test stays, detecting
> unexpected French fallback (not every Latin character); (vi) tools: real provenance only (`evidence/v524/TOOLS_AVAILABILITY.md`);
> (vii) the running build is NOT interrupted — the decision lands in lane AR (§3.8 as amended) and, if anything is left, in the one
> fix round; (viii) the report carries three Arabic counts (§5 as amended). **R7 is superseded by R7′; §3.8, §4, §5, §6 and R10 are
> amended in place below.** Where this file or a lane prompt still says «class C option B», «the class-C allowlist only» or «the 131
> class-C keys», R7′ prevails.

## 0. The decision in one screen

1. **Nine lanes, one matrix, one gate, then STOP.** T (Typography V2) · PX (imagery attribution) · LIB (the material / transition /
   icon-face primitives in the library) · HOME · PUB1 · PUB2 · PLAT (the professional pass per page, on the audits' per-section
   decisions) · AR (Arabic completeness) · CLOSING (dead chapter CSS, ratchets, catalogue, handoff). Then the ONE matrix (V5.25 §3)
   and the ONE technical gate (V5.25 §7), the candidate tag, the preview restart, the report «FINAL V2 ACCEPTANCE READY», freeze.
2. **Nothing is reopened.** Every composition the reviews passed stays (V5.25 §5: approved pages are not re-scored). The audits'
   per-section tables are the work list: the sections they mark KEEP are kept; the changes are grounds, transitions, type roles,
   faces and verbs — no new section, no new family, no new string except AR's 42 catalogue entries and 50 data rows. Each page is
   scored ONCE at its lane's merge against §10 (≥ 4 on the six dimensions; the home 4.5 composition and coherence) and merged.
3. **Rulings where the audits left the call to the Director** (R1–R14, §2 below): Typography V2 adopted whole (Host Grotesk kept,
   Readex Pro, twelve steps, weight map, mono one seat, loading plan, byte ceilings); the credits leave `photo.html` with no hidden
   attribute; Material V2.1 adopted whole with one rename (the seam-crossing primitive is «il raccordo», `.sez-raccordo`, because
   «il varco» is the entrance's: `static/css/v5/_varco.css`, the `--varco-*` tokens, `test_login_form_w2_b.py`); page-type totals
   are never raised; the eight P1 route sheets' ceilings are recorded at the family's §7.1 letter 11 264; the home finds its bytes
   inside its own sheets with a fixed fallback order; the term page's «pietra» is conditional on `_lettura.css` savings;
   F-M2's ruling stands and its residual is CLOSING's F2-m1; Arabic class C: the owner's V5.27 hybrid policy (R7′), applied by lane AR.
4. **Ownership is total and disjoint** (§3): every file one lane; shared files one owner; a lane that needs a change in another
   lane's file writes it in its notes and the owner applies it — except PX, first in the merge order, which takes the shared test
   modules and two two-line slices under §9.7's «first lane in the merge order» rule so that every merge leaves `design-v5` green.
5. **Merge order:** PX → T → LIB → {HOME, PUB1, PUB2, PLAT, AR, as each passes} → CLOSING → MATRIX → GATE → candidate. T, PX and LIB
   start on day 1 in parallel (disjoint files); HOME, PUB1, PUB2, PLAT and AR start on day 1 against the written contracts (the token
   names of TYPOGRAPHY_V2 §4.2, the attributes and class names of BACKGROUND_MATERIAL_V2 §3 as renamed here) and rebase at each
   merge. Critical path ≈ 7–8 working days.
6. **Owner questions: the one that needed an answer is answered** (the locked French blocks on Arabic pages,
   `arabic/06_owner_question.md` → V5.27 hybrid, R7′) and two owner-side records that do not block (the Arabic reader's review of Readex Pro — item B2 —, the door
   photograph's written rights record for go-live). Everything else is decided here.

---

## 1. What the owner will see (the product change, in one table)

| Family label (live_status / the report) | What changes on the product | Lane |
|---|---|---|
| **Typography V2** | Display and titles at 600 (the hero's statement and the pilot's title no longer the lightest text on the page); one scale of twelve steps on every page; the typewriter labels and step numbers become the sans at 600 (no «report index» look); one label role per head; the public phone step-up (nothing under 14 px); Arabic set in Readex Pro at the same size and colour as the French (no 15–20 % smaller Arabic, no clipped descenders, no French titles floating in Arabic leading); 16 KB fewer font bytes, half the Arabic file | T (+ every lane in its own sheets) |
| **Imagery V2 · credits** | The 104 «Photo : … / Pexels» lines and chips disappear from every photograph (the licence permits it; provenance stays internal); one production-facing test | PX |
| **Section Background / Material V2** | Four material recipes from the tokens (dressed stone «pietra», lit paper «carta viva», the mask continuation «velatura», the brand wash by position), four seam primitives («raccordo», «sfumatura», «incastro», the cut), 11 ground/order corrections at 0 B, the tile face as a niche, two verb corrections (no «small squares settle» three bands in a row) — 14 same-kind seams → 0, 5 continuations → 15 | LIB (primitives) · HOME · PUB1 · PUB2 (placement) |
| **Arabic Complete** | 0 team-written French on the Arabic product (84 texts, 748 occurrences today), professional renderings, a rendered-product test; the three RTL minors; **the locked blocks per V5.27 (R7′): compositional keys in provisional professional Arabic, substantive keys as identified Italian / identified source text / hidden until validated — 0 unintentional French** | AR (+ T for the three CSS rules) |
| **Page Composition V2 · professional pass** | Per page: which sections take which ground / transition / typographic composition / icon / motion decision, and which are KEPT (most) | HOME · PUB1 · PUB2 · PLAT |
| **Cleanup** | Dead chapter / editorial CSS removed where verified unused; every ceiling ratcheted to its measure; one catalogue pass; `HANDOFF_V2.md` | CLOSING |

---

## 2. Rulings (the Director's decisions on the audits' open points; each is final, none is a question)

- **R1 · Typography V2 is adopted as TYPOGRAPHY_V2 §3–§6 writes it.** Host Grotesk stays the one Latin family (variable 400–700,
  italic on use); **Readex Pro** (OFL, variable `wght` 400–700, HEXP 0, the product's Arabic subset ≈ 16 080 B) replaces Vazirmatn;
  ILE Wordmark and the lock-up untouched; ILE Mono confined to `code, kbd, pre, .t-ref, .ctx__ref, .doc-workspace__ref,
  .error-page__ref, .db-ref, .reg-ref`. The twelve steps (`--t-display … --t-field`, §4.2), the weight map (400 reads · 500 acts ·
  600 intitles · 700 emphasis only), `--w-display: 600`, `--track-display: -0.03em`, the phone step-up under `(max-width: 47.999rem),
  (pointer: coarse)`, the Arabic block (ratio 1.0, floor 14 px, `--ar-lh-plus: 0.1` for titles, every Arabic type rule in the
  subject form `.x:lang(ar)`), the loading plan (preloads unchanged in count, `font-display: swap`, the recomputed `ILE Arabic
  Fallback`), the byte ceilings (§4.7). The console's `--u-*` scale stays; density stays. SECTION_SYSTEM_V2 §6.2's «eight sizes, no
  ninth» and «Arabic follows the Vazirmatn rules» are superseded by erratum (CLOSING). `tokens.css` and `base.html:30-32` are §9.8
  files: the steward records this family's change as a §9.8 exception (typography), T applies it.
- **R2 · The credits leave.** IMAGERY_ATTRIBUTION D1–D8 adopted: `photo.html` loses its `<figcaption>`; `Picture.credit` goes; no
  `data-credit`/`data-author` (nothing reads it; a name belongs in one place, SECTION_SYSTEM_V2 §8); the 14 + 2 `.foto__credit` rules
  go (each by its file's owner); `MediaAsset.attribution_required` + the one-condition guard in the five curated caption templates;
  the production-facing test `tests/compliance/test_imagery_credits_v524.py` is the gate's «Pexels-visible-label check»; D8's rule
  for a future attribution-required asset is written into `IMAGE_LICENSES.md`. No asset is replaced (none requires attribution).
- **R3 · Material V2.1 is adopted as BACKGROUND_MATERIAL_V2 §3 writes it** — one new ground kind (`pietra`), three recipes (`pietra`,
  `carta viva` = `data-luce="origine"`, `velatura` = `data-sfuma`), four transitions, the 11 ground/order corrections of §3.3, the
  two verb corrections of §3.4 (E «il mosaico» and PA-2 drop `node`: rule draw + glyph ink + face light), the tile's niche face
  (§3.5), the refused list (no blurred image fields, no noise on paper, no glass, no light mesh, no arch seams). **One rename:** the
  crossing primitive is **«il raccordo»** — `.sez-raccordo`, `--sez-raccordo` (48 px; 32 on phones), `data-verb="draw-y"`,
  `aria-hidden="true"` — not «varco». The partial is `static/css/v5/_materia.css`, page-only like `_casa.css` and
  `_platform-grounds.css`, imported by the route sheets that use it, **never by `main.css`**. `stone` and `pietra` are one kind for
  the adjacency rule; `pietra` never touches `stone`.
- **R4 · Budgets.** (a) **The page-type totals of §7.1 are the letter and are not raised:** home ≤ 61 440, landings / interior /
  pathways ≤ 56 320, reading pages and the Forum ≤ 54 272 (`tests/frontend/test_frontispiece_v515_c.py`). (b) **The eight P1 route
  sheets' ceilings** (`tests/frontend/test_pages_v522_p1.py:53-62`, set by lane P1 on its own measures) **are recorded at the
  family's §7.1 letter 11 264** — a recording, cited to this file and V5.24 §7–§10 under V5.20, not a raise of any page total:
  Parcours 55 493 + ≈ 770 = 56 263 ≤ 56 320 holds by itself. (c) **`main.css`: ≤ 32 716 B** (the measure; the tests' 32 718 is
  ratcheted to the measure by CLOSING). No lane adds a rule to a sheet `main.css` imports without removing at least as many bytes
  from one. (d) **The home** stays ≤ 61 440: HOME pays the material's ≈ 410 B from `pages.css` / `hero.css` — first the T
  conversions (clamps → tokens, the mono label rules, `.testa__label`), then the `.foto__credit` rule, then dead rules by Chromium
  coverage; if short, HOME drops in this order: the S2 → S3 sfumatura (≈ 110 B; H0's fade is already the page's one fade), then the
  S7 sill light (≈ 80 B). The S3 → S4 raccordo and the S4 → S5 velatura are never dropped (they are the two seams the owner named).
  (e) **The reading pages** (54 272 / 54 272): attributes only, 0 B; **the term page's «pietra» band is conditional** — PUB2 first
  runs the coverage pass on `static/css/v5/_lettura.css` (the retired glossary rules; `lettura.css` bundles it); if it frees ≥ 770
  B, `lettura.css` imports `_materia.css` and the scheda band takes `pietra`; otherwise the band takes `stone` (the glossary's
  `.lessico` is stone; the term page is one page later, §1 rule 5 holds through the compact head's paper). (f) The library partials'
  ceilings (`test_sezioni_v522_s.py:38-50`) may be re-recorded by LIB at measure + the audited increment (`_sec-strato.css` + ≈ 160,
  `_sec-mosaico.css` + ≈ 120, `_sezioni.css` + ≈ 45), cited; JS ceilings unchanged (0 new JS in every lane). (g) Fonts: TYPOGRAPHY_V2
  §4.7 (set ≤ 62 000; Latin public ≤ 22 000; Latin console ≤ 24 000; Arabic public ≤ 38 000; Arabic console ≤ 40 000; swap CLS ≤ 0.01).
- **R5 · Two deviations accepted and recorded.** The pathway sheets and Projet pilote carry no `data-rhythm="moment"` tall enough to
  be one (content-bound; the sheets' filo and the pilot's route become `band`); Formation's order becomes traversata → la protezione
  (pietra) → the grid (carta viva) → la boussole (Diplômes' order).
- **R6 · F-M2 (the first keyboard input's INP) — the ruling stands as recorded** (DL54-185 item 3, DL54-186): the relative gate
  «within 20 ms of the base» is replaced by the absolute budget of SECTION_SYSTEM_V2 §5.3 — first-Tab and first-pointer-after-keyboard
  INP ≤ 200 ms at p75 on the compressed twin 8782, desktop and phone, fr and ar, paired against the base, n ≥ 5. The first Tab is
  within it (160 · 176 · 128 · 168 ms); the desktop pointer after the keyboard is over it on the lane and on the base (216 · 248
  against the base's 176 · 208). **The residual trim is CLOSING's F2-m1** (§3.9): the library's keyboard-tier guards
  (`:root:not([data-input="key"])`, the inherited `--sez-t`) and lane H's one modality rule are narrowed; the preserved `main.css`
  modality rules are not touched. Gate: ≤ 200 ms in all four cells; if the desktop cell stays over on the base and the tree alike
  after the trim, it is recorded as **P2 with the base's figure beside it** (a synthetic CPU × 4 measure; every INP figure carries the
  base's) — not a release blocker, not a P0/P1. Every lane's review records it in these words wherever F-M2 is cited.
- **R7 · Arabic — SUPERSEDED in its class-C part by R7′ (owner's V5.27, 5 Nov 20:08); W1–W5 and the test stand.** `02_class_b_wraps.md` W1–W3 applied with the fragments as given (the 42 catalogue entries in it/en/ar, the 50 rows
  of `data_translations.json`); the three KEEP_SOURCE strings reworded as W1 says (team text, not locked); the test
  `tests/i18n/test_arabic_completeness.py` + `arabic_allowlist.py` placed and green with `KNOWN_FRENCH = {}`; the RTL minors M1–M3
  (CSS by T, templates by their owners); the plural-of-courtesy remark adopted («أين تصادفونه»). **Class C (130 locked keys + the
  prescribed Forum title): option B applied now** — kept as source text, isolated `lang="fr"`, allowlisted by key, the allowlist
  computed from the registry; the C-1 heading rule written so a heading whose whole content is French takes the French paragraph's
  edge. The owner's answer (A / B / C) switches the renderings by key without code changes. The preview's persona
  `preferred_language` stays `fr` (an acceptance-environment matter, not the product's); R1–R4 of W4 are backlog, recorded.
- **R7′ · Arabic, the locked blocks (owner's V5.27 hybrid policy; replaces «class C option B»).** The AR lane classifies EVERY
  key of `arabic/03_locked_blocks_register.md` (130 keys + the prescribed Forum title) into one of four treatments and records it in
  `docs/design-v5/QA/v524/ar/LOCKED_BLOCKS_REGISTER.md` (columns: class, treatment, reason, source route):
  **(1) C-UI — compositional, non-legal → provisional professional Arabic now.** Hero title, subtitle and body; the four entrances
  (titles, texts, buttons); the pilot's sequence words and body; the persons' page title and «comment ça marche»; the eight pathway
  TITLES; section titles; buttons and calls (`*.button`, `button_secondary_pilot`); the companies' title, intro, quote and form FIELD
  labels; the institutions' intro, recipients and button; the universities / training / living / diplomas / antifraud TITLES; the
  living intro; the Forum page's institutional copy (what / why / objectives / who / audience / header meta / patronage / registration
  intro and title); FAQ QUESTIONS; «marque déposée». Rendered through the locked layer as the page's text (no `lang` attribute),
  flagged internally `PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW` (status visible on the dev board / back-office only; nothing
  on the public UI may look unfinished). Professional institutional register, native reader's second pass; the French source text,
  its key and its checksum untouched; no it/en rendering added (the decision is Arabic; it/en keep today's behaviour).
  **(2) C-SUBST-IT — substantive with an authoritative Italian text** (e.g. `legal.privacy.fr_courtesy.*` where the verified Italian
  notice exists): the Italian text shown, identified as the authoritative Italian text (an Arabic caption line), with the Arabic
  context «courtesy Arabic translation not yet validated» where needed; the French never shown as the legal source.
  **(3) C-SUBST-FR — substantive whose only source is the prescribed French** (FAQ ANSWERS, glossary DEFINITIONS, pathway
  DESCRIPTIONS, `p3.persons.intro`, `p3.antifraud.body`, `p3.diplomas.body`, `p1.companies.form.consent`, the privacy / consent
  wordings): on the block's OWN source page (the FAQ, the glossary and term pages, the pathway sheets, Attention aux fraudes,
  Diplômes, the companies' form) shown as **identified source material** — isolated `lang="fr"` and preceded by one Arabic caption
  line naming it the source text in French with the Arabic translation pending validation (one caption per block, in the label
  role, no new colour, no new icon; CSS only where no existing class serves and only with the bytes paid, R4 c); on every OTHER
  surface that quotes the block (the home's «lo strato» plates and «la protezione», the pathway index descriptions, AGAMI's and
  the Forum's quoted bodies, Entreprises' FAQ plate) the French body is **hidden until validated**: the plate keeps its Arabic
  question / keyword / title and one Arabic line pointing to the source page («النص المصدر على صفحة …»). The AR lane may move a key
  between (3)'s two forms with a one-line reason; it may not invent legal meaning, rewrite a rule or translate the block.
  **(4) C-OFFICIAL — official titles and proper names kept in the original**: `p1.trademark.mark`, `p2.home.banner.title`
  «FORUM VÉNÉTIE–MAROC», the prescribed «FORUM PERMANENT VÉNÉTIE–MAROC», «Italy Legal Entry™», AGAMI's name — unchanged,
  isolated, allowlisted by key. **When in doubt between (1) and (3), (3).** The `<title>` / `<meta name=description>` follow the
  treatment (Arabic for (1); for (3) the source text with the page's Arabic name first). ENGINEERING: one layer, no template of a
  page lane touched — the renderings and the policy live beside the registry (`apps/cms/locked_content.py` keeps the French and
  the checksums byte-identical; NEW `apps/cms/locked_renderings.py` holds the Arabic renderings with status and the per-key
  treatment; `locked_content.get(key, lang)` returns the rendering with `effective = lang` for (1), the Italian with
  `effective = "it"` for (2), the source with `effective = "fr"` for (3)/(4); the `{% locked %}` tag of
  `apps/core/templatetags/ile_core.py` renders the caption for (2)/(3) and the hidden form for (3) off its source route; the
  dev board lists every key with its treatment and status). The test `tests/i18n/test_arabic_completeness.py` is re-specified:
  every `lang="fr"` run on `/ar/` must be a (3)-on-its-source-page block WITH its caption or a (4) key; every (1) key renders
  Arabic with no French word; every (3) key renders no French off its source page; proper names / quotations by the existing
  allowlist; anything else = unintended French = FAIL; `KNOWN_FRENCH = {}` stays. COUNTS for the report (§5): «provisional
  non-legal Arabic» = the number of (1) keys; «untranslated authoritative legal blocks» = the number of (2)+(3) keys with the
  treatment split (identified Italian / identified source on its page / hidden elsewhere); «unintended French fallback» = 0.
  The HOME, PUB1 and PUB2 lanes change nothing for this; their Arabic pages are re-checked at AR's gate (3) and at the matrix.
- **R8 · The platform is a preserved family and stays one.** PLAT applies the typography contract only (TYPOGRAPHY_V2 F-8, F-4's
  eyebrow → label role, numerals 600, the Arabic console on Readex Pro through the same tokens) and AR's one-line call; material §6:
  **no change** to the dashboards, the case file, documents, forms, organisation spaces; the dashboards' `data-rise` stays (functional
  data does not move for style; recorded, as the gold items of §9.8 are). The §9.8 exception is recorded by the steward as
  «typography tokens on the platform».
- **R9 · The professional pass (V5.26 §1–§2, §9) is decided section by section in §3's lane tables, from the audits' per-section
  rows.** KEEP is the answer wherever the composition passed its review and the audit marks it at or above the bar; the changes are
  the audits' decisions and nothing else. The FAQ (V5.26 §1) already has the premium searchable explorer, category navigation (tabs
  from 64 rem, disclosures below), the active question, the T1 seal, a 320 ms glide, keyboard and RTL, permalinks, the reset link and
  the empty search state (`components/empty_state.html`, `faq/index.html:66`), the related routes («il rimando»): it takes the stone
  ground and nothing more; «popular topics» are not added (no real data, V5.26 §1). Réseau, Contact, Vivre, Institutions, Le projet's
  story, the Forum's head/ring/actions, AGAMI's targa and approdo: KEEP. No 21st.dev component enters: the two libraries are in place.
- **R10 · Tools (V5.26 §3–§4; V5.24 §1).** The named plugins «design-critique» and «design-handoff» exist in no official marketplace
  (orchestrator's note, V5.25): their functions are supplied by `impeccable`'s critique (the §24 questions, once per page at the lane's
  merge) and by CLOSING's `HANDOFF_V2.md`. Per lane the working tools are named in §3; a tool is used only to decide and implement
  (never «consulted»). No calibration round, no council, no second creative review after a page passes. **V5.27 §6 — real provenance only:** the actual inventory is `C:/tmp/ile_v5_council/evidence/v524/TOOLS_AVAILABILITY.md` (requested name → installed? → real skill / path used); every lane's NOTES and `HANDOFF_V2.md` name the REAL tool (skill path or MCP server) behind each decision; no lane claims «design-critique» or «design-handoff» (not installed, no configured marketplace carries them); the build is never blocked waiting for a plugin source.
- **R11 · Family ids.** `scripts/check_ownership.py` `FAMILY_ID` admits none of the nine: the steward extends it with one alternative
  `|v5(?:2[4-9]|[3-9][0-9])-(?:t|px|lib|home|pub[12]|plat|ar|closing)` (docstring: «from V5.24 on, the final-delivery lanes of this
  file»), `tests/test_check_ownership.py` extended under V5.20 citing this file; branches `v524-<lane>`, worktrees
  `C:/tmp/ile_wt/v524-<lane>`, merge tags `v524/<lane>`, each family in `OWNERSHIP_V54.json` with its `owns` globs and slices.
- **R12 · Machine discipline.** One pytest per database lane: `TEST_DATABASE_URL` → `test_ile_v524_<lane>`. Headed Chromium only
  under a lock slot (`C:/tmp/ile_locks/CHROMIUM_LOCK_A` / `_B`, bash `noclobber` create with label + time, ≤ 25 min, > 40 min stale);
  headless probes and the non-browser suites take no slot. Lane servers on 8785–8789 by lane (T 8785, LIB 8786, HOME 8787, PUB1 8788,
  PUB2 8789, PLAT 8790, AR 8791, PX none needed), stopped at the lane's end; 8782 (the compressed twin) only for CLS / INP / LCP
  measures, switched under the lock as SERVERS.md says. Repo files LF (Python `read_bytes` / `write_bytes`); `PYTHONIOENCODING=utf-8`;
  `npm run build` with the installed packages, two builds identical, dist committed when it differs.
- **R13 · Steward merges** follow the v522 model (DL54-181 … 186; scripts under `C:/tmp/ile_v5_council/.work/v522-*-merge/tools`):
  `DESIGN_V5_MERGE_LOCK` (noclobber), merge `design-v5` into the branch first, the family in the manifest + `check_ownership <family>
  <base> --head <lane head>` PASS and `--validate` coherent, `git merge --no-ff`, `npm run build` (reproducible), catalogue sync /
  compile for new strings (professional it/en/ar; Arabic reviewed; locked text never translated), `manage.py check`,
  `makemigrations --check`, `ruff check .` (0), `tests/security/test_confidential_material.py` in-process with
  `ILE_CONFIDENTIAL_SENTINELS=<the private sentinel table, outside the repository>` (never printing values), the lane's
  targeted tests green, the DL entry (DL54-187 …) + `live_status.json` + `CHANGELOG_V54.md` (Italian, owner-friendly), annotated local
  tag, lock released, the preview restarted with the acceptance launcher and verified (`/fr/ /it/ /en/ /ar/ /__design-v5/`, the
  changed pages in four languages, the contact page with both channels, the nine personas' homes → 200, 0 tracebacks). No push, no
  public tag, nothing on `main`, nothing deployed (V5.24 §32, V5.25 §9).
- **R14 · Scope guard (V5.25 §1, §8).** A lane that finds a defect outside its tables writes it in its notes as a candidate for after
  acceptance and does not fix it — unless it is a genuine regression of its own change or a P0/P1.

---

## 3. The lanes

Common to every lane: branch / worktree / tag per R11; notes at `docs/design-v5/QA/v524/<lane>/NOTES.md` (what changed, the
contract items applied for other lanes, the new msgids if any, the measures, the stills' paths under
`C:/tmp/ile_v5_council/evidence/v524/<lane>/`); tests change only under V5.20's rule citing V5.24 and this file, each the same
invariant or stronger, no skip, no timeout raised; the six-dimension check once at merge (R9); stills to evidence; the reviewer's gate
is TARGETED (V5.25 §2) — never the full matrix.

### 3.1 Lane T — Typography V2 (`v524-t`; ≈ 2 days; merge second)

**Scope.** TYPOGRAPHY_V2 §4–§6, the shared layer only: the fonts (Readex Pro built by `evidence/v54/w1-a/tools/build_v5_fonts.py`
from `google/fonts` `ofl/readexpro` v1.205 — `instancer` wght 400–700 + HEXP 0, `subset` on the product's recipe,
`recalcTimestamp=False`, name IDs 0–6, 13, 14, family name «Readex Pro», `OFL-ReadexPro.txt`; Vazirmatn and its licence removed), the
`@font-face` and the recomputed `ILE Arabic Fallback`, the preload href, the tokens (stacks, twelve steps, line-heights on the 4 px
line, the phone step-up, `--w-display: 600`, `--track-display`, `--t-label*`, `--t-numeral*`, the Arabic block, removal of the Arabic
trio), `base.css` (the label and numeral roles, `.lead` → `--t-lead`, the `:lang(ar)` rules in subject form, the mono one-seat list,
the mono re-pointing block trimmed) and `buttons.css` (`.btn--primary` 16/24 600; 17/24 phones); **AR's three CSS items in
`static/css/v5/base.css`** (M1 the brand `bdi` `white-space: nowrap`; M3 `[dir="rtl"] :is(a, button):is([lang="fr"], [lang="it"],
[lang="en"]) { unicode-bidi: isolate; }`; C-1 `[dir="rtl"] :is(h1, h2, h3, h4):has(> [lang="fr"]:only-child) { direction: ltr;
text-align: start; }`); the guard tests with a **burn-down allowlist** `TYPOGRAPHY_BURNDOWN = {sheet: count}` of the `clamp()`
font-sizes, `var(--f-mono)` seats and descendant-form `:lang(ar)` rules still present per sheet, which every other lane empties
for its own sheets and CLOSING asserts empty; the docs of the type system. **Does not touch** page sheets, the library partials
(LIB applies the contract there), `main.css`'s import list, any template but `base.html:30-32`.

**Files owned.** `static/css/v5/tokens.css` (§9.8 exception, recorded) · `static/css/v5/fonts.css` · `static/fonts/**` (+
`licenses/OFL-ReadexPro.txt`; − `v5-vazirmatn-*`, `OFL-Vazirmatn.txt`) · `static/css/v5/base.css` · `static/css/v5/buttons.css` ·
`templates/base.html` lines 30–32 only (slice; §9.8 exception) · `C:/tmp/ile_v5_council/evidence/v54/w1-a/tools/build_v5_fonts.py`,
`cls_swap.py` (outside the repository) · `docs/design-v5/FONTS_V5.md` · `docs/design-v5/DESIGN_SYSTEM_V5.md` §3.3, §5 ·
`docs/design/DESIGN_SYSTEM_2026.md` §6.1–§6.8 · tests: `tests/frontend/test_v5_tokens.py` (the named tests re-pointed under V5.20),
NEW `tests/frontend/test_typography_v2.py`, NEW `tests/frontend/test_fonts_budget_v2.py`, `tests/frontend/test_design_docs.py`
(font list), the two font-loading browser tests as slices (`tests/frontend/test_browser.py::test_fonts_are_self_hosted_and_loaded`,
`tests/i18n/test_rtl_browser.py::test_arabic_typefaces_are_applied_and_loaded`) · `docs/design-v5/QA/v524/t/NOTES.md`.

**Budgets.** R4(g); `main.css` ≤ 32 716 after the token block grows by the twelve steps and shrinks by the Arabic trio, the mono
re-pointing, the `base.css` clamps (measured at the build; if over, T removes dead `base.css` rules found by coverage before merging —
never raises). Swap CLS ≤ 0.01 on 8782 (home, login, dashboard, documents; fr, ar; 1440, 390). 0 JS, 0 strings, 0 images.

**Tools.** impeccable (`reference/typography.md`, `typeset.md`), taste-skill (Rule 1, §7), ui-ux-pro-max (`typography.csv`,
`google-fonts.csv`), fontTools 4.60.2. Decision → implementation, no catalogue of faces.

**Gate (reviewer, targeted).** (1) `test_v5_tokens.py`, `test_typography_v2.py`, `test_fonts_budget_v2.py`, `test_design_docs.py`,
`tests/i18n/test_catalogues.py`, `test_rtl_static.py` green; the burn-down table equals the measured counts (no sheet listed that is
clean, none clean that is listed). (2) Fonts: the set ≤ 62 000 B, per-file ceilings, FONTS_V5 §1 bytes + SHA-256 in step; Readex Pro
fetched on `/ar/`, never on `/fr/`; no Vazirmatn anywhere (`grep` over the tree: 0). (3) Headed Chromium under a slot, 1440 · 1024 ·
390 × fr · ar on: home, Parcours, FAQ, Le projet, AGAMI (the name device, the identification block's mixed runs), Contact, login, the
person dashboard, the case file: display weight and tracking; one label per head at 13/14 px in the sans; numerals in the sans;
Arabic parity beside the French plates (title, lead, body, UI); descenders in nav words, chips and buttons not clipped; the French
runs on `/ar/` at Latin leading; no text under 14 px on phones; the swap on 8782 with the fallback held 1.5 s (CLS). (4) **The hero's
first screen** (preserved): a pixel diff against the base at 1440 and 390, fr and ar — the only differences are the statement's weight
and tracking and the primary call's weight through the tokens; composition and positions unchanged (≤ 1 px). (5) The Arabic
reader's exhibit (`v524-typo/shots/compare_1600.png` + the Arabic home still) recorded for item B2. (6) `main.css` measured; the
ratchet holds.

### 3.2 Lane PX — imagery attribution (`v524-px`; ≈ 1 day; merge FIRST)

**Scope.** IMAGERY_ATTRIBUTION D1–D8 (R2). As the first lane in the merge order it owns the shared test modules it must update so the
tree stays green, and two two-line slices (`Photo.attribution_required` in `apps/pages/services.py:241, 259` and
`apps/ecosystem/services.py`'s equivalent) — HOME and PUB1 rebase on it. The `.foto__credit` rules in other lanes' sheets are deleted
by those lanes (dead selectors meanwhile): LIB (`_photo.css`, `_fronte.css`, `_sec-strato.css`, `_compose.css`, `_sec-mappa.css`),
PUB1 (`ecosystem/_institutions.css:47-56`), HOME (`pages.css` `.pilota__quadro .foto__credit`), PUB2 (`cms/_lessico-v2.css:376-383`).
The curated-caption guards in `templates/pathways/detail.html:66` (PUB1), `templates/forum/partials/hero.html:46` and
`permanent_sections.html:57` (PUB2) are applied by those lanes on PX's contract (`{% if asset.attribution_required %}`). The doc
errata outside PX's two documents (SECTION_SYSTEM_V2 §8 block; DESIGN_SYSTEM_2026 `:2953-2958`, `:4379-4384`; the H/P2 NOTES lines)
go to CLOSING's docs pass; H's `_trust.html:15` / `_ecosystem_frame.html:10` comments to HOME.

**Files owned.** `templates/components/photo.html` · `apps/pages/imagery.py` · `apps/cms/models.py` (`MediaAsset.attribution_required`
property; no migration) · `apps/forum/models.py` (the same property on `Media`) · `templates/pages/partials/_ingresso.html` (line 77
guard; the file whole) · `templates/news/detail.html` (line 61) · the two slices above · tests: `tests/compliance/test_imagery_v512.py`,
`tests/compliance/test_figure_caption.py`, NEW `tests/compliance/test_imagery_credits_v524.py` (`@pytest.mark.compliance`),
`tests/frontend/test_interior_w3_f1.py`, `apps/pages/tests/test_home.py` (lines 160–174, 635–637), `apps/pages/tests/test_home_v522_h.py`
(line 441), `apps/pages/tests/test_browser.py` (comment, lines 89–93), `apps/ecosystem/tests/test_browser.py` (lines 103–105),
`tests/frontend/test_sezioni_v522_s2.py` (lines 155–170), `tests/frontend/test_sezioni_browser_v522_s2.py` (lines 347–358, retargeted
to a CC-BY `MediaAsset` fixture) · docs: `docs/IMAGE_LICENSES.md` (§1.3, §3.1, §3.4, new §3.5 and §1.10), `docs/design-v5/ASSET_USAGE_MATRIX.md`
(§11 erratum) · `docs/design-v5/QA/v524/px/NOTES.md`.

**Budgets.** HTML −70 … −110 B per frame; CSS only shrinks (every page sheet that bundles a changed partial re-measured gzip -9 against
its ceiling); `main.css` untouched by construction (imports none of the partials) and measured anyway; 0 JS, 0 images, catalogue +0 −0
(`msgid "Photo"` stays for the curated captions and the Forum media).

**Tools.** The audit's crawler (`.work/v524-audit/v524-pexels/crawl.py` + `analyse.py`), headless Chromium for the stills (no slot).

**Gate (reviewer, targeted).** (1) `pytest tests/compliance/test_imagery_v512.py tests/compliance/test_imagery_credits_v524.py
tests/compliance/test_figure_caption.py tests/frontend/test_interior_w3_f1.py tests/frontend/test_sezioni_v522_s2.py
apps/pages/tests/test_home.py -m "not browser"` green; the three browser twins green under a slot. (2) The rendered crawl of the 184
public pages + the nine personas: «slot credits: 0», «text hits: 0» except the footer's «©» and the glossary's «Source» (F5).
(3) Source grep over `templates/**` (excluding `templates/dev/**`): no `foto__credit`, `Pexels`, `Unsplash`, `Photo by` outside
`{% comment %}`. (4) Every D6 row applied as written (invariants equal or stronger; the strict rule's four conditions cited).
(5) Stills of `/fr/entreprises/`, `/fr/institutions/`, `/ar/parcours/`, `/fr/le-projet/` at 1440 and 390: the frames unchanged, the
lines and chips gone, no empty caption box. (6) `is_publishable` unchanged; `test_every_slot_is_licensed_…_recorded` still reads
licence, author and page for the 26 slots. (7) `/__design-v5/specimens/imagery/` still draws the frames and its data sheets (internal).

### 3.3 Lane LIB — the library: material, transitions, faces, verbs, type roles (`v524-lib`; ≈ 2 days; merge third)

**Scope.** BACKGROUND_MATERIAL_V2 §3.1, §3.2 (with R3's rename), §3.4, §3.5, §4.1 rows 1–4; TYPOGRAPHY_V2 §6's items in the library
sheets (`.testa__label`, `.ingresso__label` → the label role; `.sez-numeral`, `.tracciato__num`, `.linea__*` numerals → sans 600
tabular; `.sez-keyword` 600; clamps → tokens in `_fronte.css`, `_sezioni.css`, `_servizio.css`, `_sec-tracciato.css`, `_linea-v2.css`;
`_sezioni.css:147` and `_fronte.css:194-198` and the other descendant-form `:lang(ar)` / `[dir="rtl"]` type rules in the subject form;
`.fronte__name` takes `--track-display` and nothing else); PX's `.foto__credit` deletions in its five partials. **New
`static/css/v5/_materia.css`**: `.sez[data-ground="pietra"]` (+ `::before` drafting grid, 1 px `color-mix(in srgb, var(--line-rhythm)
70%, transparent)` every 48 px, `mask-image: linear-gradient(to inline-start, black 0%, transparent 62%)`, the RTL twin),
`.sez[data-luce="origine"]` (+ RTL twin: `radial-gradient(60% 50% at 0 0 …)` / `at 100% 0`), `.sez[data-sfuma="stone|paper|brand|night"]::after`
(`block-size: 12rem` → 8 rem on phones; `--sez-next` per kind; `--accent-wash` as the wash's first light), `.sez-raccordo` (2 px
`--line-structure` on light / `--accent-night` entering night; `inset-block-end: calc(-1 * var(--sez-raccordo))`; the 6 px
`--accent-mark` node; `--sez-d: var(--motion-draw)` delay; `z-index: 1`; the `wait` / `in` rules on `[data-sec-state]`; RTL inset
twin), `.sez--porte[data-incastro]` (the overlap), forced-colours and print stills; tokens and `color-mix` of tokens only, logical
properties only, no literal colour, no new duration or easing. **`protezione.html`**: the `ile-scudo` partial as `.sez-fondale`
(aria-hidden, 12 rem, `opacity: .3`, `stroke: var(--line-structure)`) low on the far side and `.protezione__davanzale`
(`data-verb="draw"`); `_sec-strato.css`: the fondale layer generalised from `.approdo__fondale`, the sill line. **`_sezioni.css`**: the
T2 tile's niche face `background: linear-gradient(var(--line-rhythm), var(--surface-raised) 85%)` (night face unchanged).
**`mosaico.html` + `_sec-mosaico.css`**: the tile's foot rule draws 0 → 40 % (`sez-draw` on `.sez-tile::after`, `--sez-i` from
`.sez-seq`), the glyph inks, the face light steps once; no `node`. **Does not touch** `tokens.css`, `base.css`, `buttons.css` (T),
`main.css`, `motion.css`, the icons and sprites (no icon change is decided), `rise.js` and `sezioni/*.js` (owned, unchanged: the runtime
already writes `data-sec-state`; the raccordo is a child of its section).

**Files owned.** `static/css/v5/_materia.css` (new) · `_sezioni.css` · `_sigillo.css` · `_sec-boussole.css`, `_sec-campata.css`,
`_sec-emiciclo.css`, `_sec-filo.css`, `_sec-flusso.css`, `_sec-indice.css`, `_sec-mappa.css`, `_sec-mosaico.css`, `_sec-passaggio.css`,
`_sec-racconto.css`, `_sec-strato.css`, `_sec-tracciato.css` · `_reveal.css` · `_photo.css` · `_journey-passage.css` · `_linea-v2.css` ·
`_servizio.css` · `_fronte.css` · `_compose.css` · `_porta.css` · `templates/components/sezioni/**` · `templates/components/stepper.html`,
`components/photo.html` is PX's (not LIB's) · `templates/pages/partials/_linea.html`, `_chapter_head.html`, `_section_header.html`
(unchanged; CLOSING decides their fate) · `static/js/src/rise.js`, `static/js/src/sezioni/**` (unchanged) · tests:
`tests/frontend/test_sezioni_v522_s.py`, `test_sezioni_browser_v522_s.py`, `test_seal_heads_browser_v522_s.py`, `tests/i18n/test_rtl_static.py`,
`tests/frontend/test_rm_flag_parity.py` (owned, expected untouched), NEW `tests/frontend/test_materia_v524_lib.py` (+ browser twin) ·
`docs/design-v5/COMPONENT_PROVENANCE.md` (the primitives' rows) · `docs/design-v5/QA/v524/lib/NOTES.md`.

**Budgets.** `_materia.css` ≤ 800 B gzip -9 per importing sheet (≈ 770 estimated); `_sec-strato.css` + ≈ 160, `_sec-mosaico.css` + ≈ 120,
`_sezioni.css` + ≈ 45 (R4 f); every route sheet that bundles a changed partial re-measured; page-type totals untouched by LIB alone
(the imports are the page lanes'); `main.css` 0 B; 0 JS; 0 strings; the T2 niche face keeps the glyph ≥ 4.5:1 (`--text-1` on the
gradient's darkest stop `--line-rhythm`: 12.9:1).

**Tools.** impeccable (critique: the AI-slop tells, the bans — side stripes, gradient text, glass, identical card grids), taste-skill
(anti-card-overuse), the Figma motion skills (`figma-use-motion` / `figma-implement-motion`: the raccordo's timing on the existing
`draw-y` verb, `--ease-sine`, `--motion-draw`, delayed by the section's own draw; its reduced-motion still), find-animation-opportunities
(the four-question gate: only the raccordo and the tile's light pass; no parallax on the grid, no drift on the velatura, no hover motion
on index rows).

**Gate (reviewer, targeted).** (1) Static: the six ground kinds and three attributes read only by `_materia.css` and the shell;
`_materia.css` tokens / `color-mix` only, logical properties only, every verb rule under `prefers-reduced-motion: no-preference` and
`:root:not(.rm)` with a drawn still; `test_rm_flag_parity.py` unchanged and green; the RTL twins present (`test_rtl_static.py`).
(2) The specimen board (`/__design-v5/` sezioni specimens) shows each recipe and primitive at 1440 and 390, fr and ar, in headed
Chromium under a slot: the pietra grid on the far side fading toward the plate (mirrored in Arabic), the carta viva light at the origin
corner (mirrored), the velatura never animating, the raccordo drawing once after the section's line and leaving `getAnimations()`, its
node within 2 px of the next band's head line, the incastro overlap, the tile niche, the mosaico verb (rule draw + ink + light, no
settle); reduced motion: no `data-sec-state` written, lines drawn. (3) The protection band on one page (Parcours) with the fondale and
the sill: the shield bookend low on the far side at ≈ 30 % `--line-structure`, the sill to the container's edge, nothing over the plate.
(4) Typography roles in the library: `.testa__label` / `.ingresso__label` sans 13/16 600 +0.08 em (Arabic 14/20, no capitals, no
tracking); numerals sans 600 tabular at 28/32 or 36/40; `.sez-keyword` 600; no `var(--f-mono)` left in LIB's sheets outside the
reference classes; no descendant-form `:lang(ar)` type rule (T's burn-down table emptied for LIB's sheets). (5) Budgets measured and
recorded; no page total moves.

### 3.4 Lane HOME — the homepage's professional pass (`v524-home`; ≈ 1.5 days)

**Decisions per section (BACKGROUND_MATERIAL_V2 §5.1; TYPOGRAPHY_V2 F-1, F-3, F-4).**

| # | Section | Ground / transition / motion / icon / type | Decision |
|---|---|---|---|
| 0 | Hero (first screen) | preserved | KEEP (the display weight and the primary call's weight arrive through T's tokens only; HOME re-measures with T) |
| H0 | «la soglia» | paper → wash fade, draw-y | KEEP (the model of the sfumatura) |
| S2 | «la linea V2» | brand wash KEEP · **out: sfumatura 6 rem into S3** (`_casa.css`; droppable last-but-one per R4 d) · motion KEEP · T1/T2 KEEP | change ground seam |
| S3 | «l'indice» | **ground stone** (`services._grounds`) · **out: raccordo** — the pilot's gold seam begins 32 px above the night band (`_pilot.html`, `_casa.css`) · GLIDE KEEP · glyphs KEEP · the stage's T2 64 KEEP | change ground + seam |
| S4 | «il panorama» | night KEEP · **out: velatura** — the night veils the masonry's first 12 rem (`.home-trust .strato--foto::before` gains the night stop) · develop ×2 KEEP | change seam |
| S5 | «lo strato» | the best material band on the site | KEEP |
| S6 | «la protezione» | **pietra** through LIB's partial (automatic: `protezione.html` + `_sec-strato.css`) | verify only |
| S7 | «la campata» | **carta viva**: the radial light at the arch's sill (`--accent-mark` 10 %, 60 % × 50 % at the sill's centre) · MASK KEEP | change ground (droppable last per R4 d) |
| S8 | reserved row | night joined to the footer, the key turns | KEEP |
| S1 | «il passaggio» (phones) | stone band, night arch seats, snap | KEEP |
| type | `.he__promise`, `.pilota__titolo` → `--t-display` / the tokens (600); `.testa__label` 15 px mono → the label role; the clamps of `pages.css` / `hero.css` → tokens; `.sez-keyword` 600 (library) | apply T's contract; the first screen re-measured (gate 4) |

**Files owned.** `templates/pages/home.html`, `templates/pages/home/**` (`_hero.html`: the foot `he__body` only), `templates/components/entrances.html`,
`components/pathway_list.html` · `apps/pages/static/pages/css/pages.css`, `hero.css` · `static/css/v5/_casa.css` · `static/js/src/home.js`
(unchanged) · `apps/pages/services.py` (minus PX's slice, rebased), `apps/pages/content.py`, `apps/pages/seeds.py` · tests: `apps/pages/tests/test_home.py`,
`test_home_v522_h.py`, `test_home_browser_v522_h.py`, `test_services.py`, `test_templates_static.py`, `test_browser.py`, `test_review2.py`
(the shared modules, §9.7) · `docs/design-v5/QA/v524/home/NOTES.md` (+ the one line «credits removed by v524 (V5.24 §2)» in `QA/v522/h/NOTES.md`,
and the comments `_trust.html:15`, `_ecosystem_frame.html:10`).

**Budgets.** The home total **≤ 61 440** (R4 d, the fallback order fixed there); `pages.css` ≤ 12 288, `hero.css` ≤ 11 264; `_casa.css`
tokens only; `home.js` ≤ 8 192 unchanged; 0 strings; the adjacency rule (`test_home_v522_h.py` already has it) with S3 stone: S2 brand →
S3 stone → S4 night → S5 photo → S6 pietra → S7 paper → S8 night. CLS ≤ 0.05, LCP ≤ 2.5 s mobile, INP per R6 on 8782.

**Tools.** impeccable's critique once on the integrated home (the §24 questions) at merge; `figma-use-motion` for the raccordo's 32 px
rise timing against the pilot's seam draw; no 21st research (no new pattern).

**Gate (reviewer, targeted; V5.25 §2 «desktop composition → 1440 + 1024», «mobile → 390/375/360»).** (1) `apps/pages/tests` + `test_home_browser_v522_h.py`
green on the lane's database; the grounds sequence asserted. (2) Headed Chromium under a slot at 1440 and 1024 fr, 390 and 360 fr + ar: the
S2 → S3 fade over 6 rem (or recorded dropped), the stage sheet on stone, the pilot's seam starting 32 px above the night and ending on
the band's head line (± 2 px, fr and ar), the night veiling the masonry's first 12 rem (8 rem on phones) with no animation on the
gradient, the protection's grid and bookend on the far side with the sill to the edge, the light at the arch's sill; reduced motion: the
designed stills, no `data-sec-state`; keyboard: no animation; 0 console errors. (3) The hero's first screen pixel diff against the base
(with T merged): weight and tracking only. (4) The home total measured; the fallback order applied and recorded if used. (5) The six
dimensions once: composition ≥ 4.5, coherence ≥ 4.5, the rest ≥ 4, fr and ar at 1440 and 390 — then MERGE.

### 3.5 Lane PUB1 — journeys and spaces (`v524-pub1`; ≈ 2 days)

**Decisions per page (BACKGROUND_MATERIAL_V2 §3.3, §5.3; TYPOGRAPHY_V2 §6; V5.26 §2).**

| Page | Sections changed (ground · transition · motion · icon) | KEPT |
|---|---|---|
| Parcours | head → board: **raccordo** (the trunk rises 48 px into the head's foot; `pathways/_tracciato.html`, `_index.css`) · «Comment ça marche» plates: **rule draw + ink + light, no settle** (`index.html:69-75`, `_index.css` §PA-2) · E «Dans l'Espace Personnes»: **carta viva** + the mosaico verb · K «la protezione»: **pietra** (via LIB) · `_materia.css` import in `index.css` · tiles' niche face (library) | the board B «il tracciato» (an interactive journey — V5.26 §2's Parcours), the filter pills, the boussole |
| Pathway sheets ×8 | `#etapes` → `data-ground="stone" data-rhythm="band"` (R5) · filo line → **raccordo** into the night arc ending on the arc's first seat in `--accent-night` (`detail.html:103`, `_sheet.css`) · K → pietra · import in `sheet.css` · PX's guard at `detail.html:66` | the «Aperçu» strip, H «chi decide», L «Ressources», the boussole |
| Projet pilote | `#sequence` → `data-ground="brand"` + `rhythm="band"` (R5) · `#participer` → `paper` (the lunettes on paper, their sill; the paper lunette's face `--surface-raised` if transparent) · import in `pilot.css` | the head's diptych, the doors' LIGHT, «l'approdo» |
| Entreprises | `#demarche` → `stone` (`companies.html:49`) · import in `companies.css` · PX's `attribution_required` in `apps/ecosystem/services.py` (rebased from PX) | D «il panorama» (a window deserves its edges), the preserved form chapter (its head's legacy rise is CLOSING's), A «transparence», «l'approdo» |
| Institutions | emiciclo → **velatura** `data-sfuma="stone"` at its foot · import in `institutions.css` · delete `_institutions.css:47-56` (credit chip) | everything else (the best body band of the merged pages) |
| Universités | `#filiere` → `data-ground="brand"` with the **sfumatura** at its top (`universities.html:43`) · import in `universities.css` | the campus frame, the arrival's gold |
| Formation | **order** F1 traversata → K la protezione (pietra) → E grid (carta viva + the mosaico verb) → A boussole (`training.html:76-88`) · import in `training.css` | the traversata's two frames and crossing line |
| Diplômes | dossier line → **raccordo** into the pietra band (`diplomas.html:49`) · E grid carta viva + verb · import in `diplomas.css` | F «le dossier» + C aside, the stamp tile, the boussole |
| Recueil / Collaboration heads | — | KEEP (the forms preserved; the gold and `reveal-mark` recorded for after acceptance) |
| type (all) | `_index.css`, `_sheet.css`, `_diplomas.css`, `_training.css`, `_universities.css`, `_companies.css`, `_pilot.css`, `_institutions.css`: numerals → sans 600, kickers (`.traversata__kicker`, `.filiera__kicker`, `.scheda-rail__titolo`, `.tracciato__nome`) → the label role, clamps → tokens, `:lang(ar)` subject form; T's burn-down emptied for these sheets | — |

**Files owned.** `templates/ecosystem/**`, `apps/ecosystem/**` (incl. `static/ecosystem/*.css`, `services.py`, tests) ·
`templates/pathways/**`, `apps/pathways/**` (incl. `static/pathways/*.css`, `services.py`, tests) · the header blocks only of
`templates/enquiries/company_needs.html` and `collaboration_proposal.html` (unchanged) · `tests/frontend/test_pages_v522_p1.py`
(the ceilings re-recorded per R4 b, cited), `test_pages_browser_v522_p1.py`, NEW `test_pages_browser_v524_pub1.py` for the new
assertions · `docs/design-v5/QA/v524/pub1/NOTES.md`.

**Budgets.** The eight route sheets ≤ 11 264 each (R4 b); page totals ≤ 56 320 (Parcours 56 263 expected, 57 B left — recorded);
`ecosystem.css`, `pathways.css` ≤ 11 264; 0 JS (the raccordo is markup + CSS); 0 strings; the adjacency rule on every page type
(stone ≡ pietra; pietra never touching stone): Parcours paper → paper* → brand → paper(carta viva) → pietra; sheets paper → stone →
night → pietra → paper → brand; pilot night → brand → paper → stone; Entreprises paper → stone → paper → stone → paper → stone;
Institutions paper → photo → stone; Universités paper → brand; Formation paper → paper* → pietra → paper → brand; Diplômes paper →
paper* → pietra → paper → brand (`*` the head → body touch that the audit accepts on these moments' own frames; recorded).

**Tools.** impeccable's critique once per page at merge; `figma-use-motion` for the three raccordi's timing; the probe of
`.work/v524-audit/v524-material/probe.py` re-run on the lane server for grounds, seams and verbs.

**Gate (reviewer, targeted).** (1) `test_pages_v522_p1.py`, the two browser modules, `apps/ecosystem/tests`, `apps/pathways/tests`
green. (2) Headed under a slot, 1440 + 1024 fr and 390 + 360 fr + ar on Parcours, one sheet (`salaried_work`), Projet pilote,
Entreprises, Institutions, Universités, Formation, Diplômes: each raccordo plays once after its section's line and lands within 2 px
of the next band's head line (fr and ar); the velatura on Institutions never animates; the mosaico tiles draw their rule, ink and
light with no settle; the pilot's route on the wash with the status plate standing on it; the Formation order; reduced motion stills;
0 overflow; 0 console errors. (3) The probe: 0 same-kind seams on the eight page types; the verbs listed per section as decided.
(4) Budgets measured; the ceilings' recording cited. (5) Six dimensions once per page ≥ 4 (§10 targets) — MERGE.

### 3.6 Lane PUB2 — system, trust and reading (`v524-pub2`; ≈ 2 days)

**Decisions per page (BACKGROUND_MATERIAL_V2 §5.2; TYPOGRAPHY_V2 §6; V5.26 §1–§2; R9).**

| Page | Sections changed | KEPT |
|---|---|---|
| FAQ | explorer `.faq-esploratore` → `stone` (`faq/index.html:73`) · «il rimando» → `paper` (`:84`) · `.faq-esploratore__categoria` mono 13 → the label role · the «Privacy Policy» span (`faq/_item.html` links, AR's W5.3) | the searchable explorer, tabs/disclosures, the active question, permalinks, the empty state, the T1 seal, the 320 ms glide (V5.26 §1 fulfilled; «popular topics» not added: no real data) |
| Glossaire + term | `.lessico` → `stone` (`glossary/index.html:66`) · `.glossary__related` → `paper` (`:81`) · `.lessico__lettera` 64 px 500 → **600** (`_lettura-v2.css`) · the term page's `.scheda-band` → **pietra if `_lettura.css` frees ≥ 770 B, else stone** (R4 e; `term.html:33`), its chip rows paper · the glossary's related links `lang="it"` isolation comes from T's M3 | the letter rail, the term cards' in-place answer, «Où le rencontrer», the plate |
| Vivre en Italie | — | KEEP whole (the head absorbed by its panorama, one ground by decision, «Pour s'installer») |
| Le projet | panorama → «le porte»: **incastro** (`data-incastro` on `.projet-porte`, `project.html:39`) · `_projet.css`: the locked statement column at `max-inline-size: var(--measure-body)` (F-8) · `interior.css` imports `_materia.css` | the story C «il racconto», the panorama, the foot strip |
| Réseau | `.rete__etichetta` mono 13 → the label role (fixes the Arabic glyphs falling to a system face, F-3) | the map (the site's strongest icon composition), «l'approdo» |
| Contact | — (labels through the library) | KEEP whole (the channel board with both channels unchanged, the doors and their hub line) |
| Forum | `.forum-filo` (I «dal dialogo ai progetti») → `stone` + **raccordo** from the pair's foot (`presentation.html:42`) · `forum.css` imports `_materia.css` · `hero.html:17-19`: the eyebrow msgid «Dialogue institutionnel permanent» and the `lang="fr"` branch removed (AR's W1.2) · `hero.html:46` and `permanent_sections.html:57`: PX's guard | the head's drawing, the pair's type, the ring on the night, the action plates |
| AGAMI | `.agami-identita` → `stone` (`agami.html:38`), the colonnade plate's face `--surface-area` → `--surface-raised` (`_agami.css:26`) · `.agami-id__etichetta(-voce)` and `dt` mono → the label role (the Arabic registers no longer in a mono fallback) | the colonnade's signature, «la targa» (Q9: every field once, no other identifier), «l'approdo» |
| Fraudes | `.frodi` → `stone` (`antifraud.html:37`) | the split, the sill, the shield, the three routes, the report plate |
| living/topic.html | W1.3's reworded sentence (AR's contract; the themes answer 404 today — latent) | — |
| type (all) | `_agami.css`, `_rete.css`, `_frodi.css`, `_contatto.css`, `_canali.css`, `_projet.css`, `cms/_lettura-v2.css`, `_faq-v2.css`, `_lessico-v2.css`, `forum/_forum.css`: clamps → tokens, labels → the role, numerals → sans 600, `:lang(ar)` subject form; delete `_lessico-v2.css:376-383` (credit) | — |

**Files owned.** `templates/pages/{project,network,contact,agami,antifraud,institutional_base}.html`, `templates/pages/partials/_canali.html`,
`fronte/_rete.html`, `fronte/_contatto_azione.html`, `templates/pages/partials/agami/**`, `projet/**` · `apps/pages/views.py` ·
`apps/pages/static/pages/css/{interior.css,_institutional.css,_canali.css,_contatto.css,_projet.css,_rete.css,_agami.css,_frodi.css,rete.css,agami.css,frodi.css}` ·
`templates/faq/**`, `templates/glossary/**`, `templates/living/**`, `apps/faq/**`, `apps/glossary/**`, `apps/living/**` ·
`apps/cms/static/cms/{lettura.css,faq.css,lessico.css,_faq-v2.css,_lessico-v2.css,_lettura-v2.css}`, `static/css/v5/_lettura.css` ·
`templates/forum/**`, `apps/forum/static/**` · tests: `apps/pages/tests/test_interior_v522.py`, `test_institutional.py`,
`test_contact_channels_v519.py` (must not weaken), `tests/frontend/test_pages_browser_v522_p2.py`, NEW `test_pages_browser_v524_pub2.py` ·
`docs/design-v5/QA/v524/pub2/NOTES.md` (+ the one line in `QA/v522/p2/NOTES.md`, line 322 corrected).

**Budgets.** Reading pages and the Forum ≤ 54 272 (the glossary family at 54 272 today: attributes only = 0 B; the term page per
R4 e); interior pages ≤ 56 320; `interior.css` ≤ 11 264 (8 827 + ≈ 770 + 90), `forum.css` ≤ 8 192 (7 369 + ≈ 770 + 60 = 8 199 —
**13 B over**: PUB2 removes ≥ 20 B of dead rules from `_forum.css` by coverage first, recorded; the ceiling is not raised),
`lettura.css` ≤ 9 216, `agami.css` ≤ 2 048 (+ 30), `faq.css`, `lessico.css`, `rete.css`, `frodi.css` unchanged; 0 JS; the catalogue
+1 −1 (the Forum eyebrow, AR's rendering) and the topic sentence; both contact channels byte-identical; every locked text byte-identical
(188 checks).

**Tools.** impeccable's critique once per page at merge; `figma-use-motion` for the Forum raccordo; the FAQ judged against V5.26 §1's
list (R9) with a one-paragraph record in the notes.

**Gate (reviewer, targeted; V5.25 §2 «phone glossary → 390/375/360 + RTL»).** (1) The lane's modules + `apps/faq`, `apps/glossary`,
`apps/living`, `apps/forum` tests + `test_contact_channels_v519.py` + `tests/compliance/test_locked_content.py` green. (2) Headed under a
slot: FAQ, Glossaire, a term page, Le projet, Forum, AGAMI, Fraudes at 1440 + 1024 fr and 390/375/360 fr + ar: the stone grounds, the
doors' arched tops rising 64 px into the volumes, the Forum raccordo once after the pair's rule and landing on the filo's head line
(± 2 px), the term page's band, the FAQ permalinks still landing on the open answer alone at the first paint (30 of 30, CLS 0), the
glossary rail lit by the spy, the Arabic registers of AGAMI in Readex Pro / Host (no system fallback), reduced motion stills, 0
overflow, 0 console errors. (3) Both channels on `/xx/contact/` unchanged (the configured values compared in process, never printed).
(4) Budgets measured; the `_forum.css` savings recorded. (5) Six dimensions once per page ≥ 4 — MERGE.

### 3.7 Lane PLAT — the platform, typography only (`v524-plat`; ≈ 0.5–1 day)

**Scope (R8).** TYPOGRAPHY_V2 F-8 (`.ws-head__lead` `max-inline-size: var(--measure-small)`; the workspace title clamp → `--u-title-lg`),
F-4 (`--u-eyebrow` → the label role 12/16, 13/20 on phones, in `_shell.css`), F-3/§4.2 (`_dashboard.css`, `_registers.css` numerals
28/32 **600**; refs stay in the mono), the Arabic console on Readex Pro (every `:lang(ar)` type rule in `_platform.css`, `_shell.css`,
`_frame.css`, `_table.css` in the subject form; T's burn-down emptied for the portal sheets); AR's W3.2 one-line call in
`apps/portal/services.py:2389` (`documents.services.displayed_text`). **Material: no change** (BACKGROUND_MATERIAL_V2 §6: the atrium,
the NowPanel, the drawn route, the calm panel are right; the public bands now share their language). `data-rise` on the dashboards
stays (recorded). Density stays product density. **Does not touch** forms, Lume, the entrance, the organisation spaces' structure,
icons, colour.

**Files owned.** `templates/portal/**` (expected unchanged), `apps/portal/**` (incl. `static/portal/*.css`, `static/portal/v5/*.css`,
`services.py`, tests) · `apps/companies/static/companies/companies.css`, `templates/companies/**` (unchanged) ·
`apps/documents/static/documents/documents.css` · `apps/academy/static/academy/academy.css` · `apps/helpdesk/static/**`,
`apps/selection/static/**` · NEW `tests/frontend/test_platform_v524_plat.py` (+ browser twin) · `docs/design-v5/QA/v524/plat/NOTES.md`.

**Budgets.** `portal/console.css` 8 032, `platform.css` 5 014, `registers.css` 2 984, `journey.css` 2 728, `situation.css` 2 243,
`case.css` 955 and the rest: each ≤ its measure today + 0 (type conversions only shrink or hold; measured); console font bytes ≤ 24 000
Latin / ≤ 40 000 Arabic; 0 JS; 0 strings; INP / CLS unchanged on the dashboards (8782).

**Tools.** ui-ux-pro-max (a11y and touch first), the typography inventories of `v524-typo/inv/` for the ten platform surfaces.

**Gate (reviewer, targeted; V5.25 §4's platform list).** (1) `apps/portal/tests`, `apps/documents/tests`, `apps/cases/tests`, the new
module green. (2) Headed under a slot: the person dashboard (three states through the personas), the company dashboard and need form,
the institution and university spaces, documents, the case file at 1440, 1024 and 390, fr and ar: the eyebrow as the label role, the
lead ≤ 29 rem, numerals 600, Arabic parity on Readex Pro, nothing under 14 px on phones, density unchanged — a pixel diff of the
person dashboard against the base at 1440 fr shows type changes only. (3) 0 animations at rest; `data-rise` sections as before.
(4) Budgets measured. (5) Six dimensions: not re-scored (preserved family; no composition change) — MERGE on (1)–(4).

### 3.8 Lane AR — Arabic completeness (`v524-ar`; ≈ 1.5 days)

**Scope (R7).** W1.1 `apps/cms/templatetags/cms_nav.py:134` (the reworded msgid); W1.4 `scripts/i18n_audit.py` KEEP_SOURCE emptied,
`tests/i18n/test_catalogues.py:217-221` kept iterating an empty table; W2 a data seed — NEW `apps/cms/team_translations.py` (the 50 rows
of `fragments/data_translations.json` as data, field names the models') + NEW management command `seed_team_translations`
(idempotent, `get_or_create` per `(master, language)`, `status=PUBLISHED`, `source="team — v524 (Q3 provisional)"`), called by the
seeds the preview and the tests already run, so the rows exist on every environment; W3.1 `apps/companies/models.py:90 taxonomy_label`
(guarded `pgettext("companies taxonomy", …)`); W3.2 NEW `documents.services.displayed_text` (guarded `pgettext("document requirement",
…)`), used in `apps/cases/services.py:783, 798` and the three templates (`words.lang` = the reader's language when found); W3.3
`TrainingProvider.display_name` for `kind == PROJECT` (`gettext("Équipe du projet")` + the brand lock-up) in the four Academy
templates; the 42 catalogue entries (`fragments/ar.po`, `it.po`, `en.po`, `msgctxt` kept) added to `locale/{ar,it,en}/LC_MESSAGES/django.po`
with `scripts/i18n_audit.py --sync --compile`; the test `tests/i18n/test_arabic_completeness.py` (T1–T5) + `tests/i18n/arabic_allowlist.py`
(four tables with reasons; the class-C table computed from the locked registry); W5.2 the brand inside Arabic catalogue sentences
rendered through `brand_bdi` (`cms_nav.py:539`); W5.3 the «Privacy Policy» spans in the login's `varco__assurance-more` and the
`chapter__more` link texts (the FAQ's is PUB2's); `docs/I18N_RTL.md` §5 (terminology extensions), §9 (I18N-04 → fixed), the register
`03_locked_blocks_register.md` copied to `docs/design-v5/QA/v524/ar/LOCKED_BLOCKS_REGISTER.md` (keys and counts only — it holds no
personal datum). **Does not touch** any locked text, any CSS (T has M1/M3/C-1), templates owned by PUB2 (W1.2, W1.3, W5.3-FAQ listed
there), `apps/portal/services.py` (PLAT applies the call).

**Files owned.** `locale/**` · `apps/cms/templatetags/cms_nav.py` · `apps/cms/team_translations.py` (new),
`apps/cms/management/commands/seed_team_translations.py` (new), the seed hook in `apps/cms/seeds*.py` · `apps/companies/models.py` ·
`apps/documents/**` (services, templates), `templates/components/document_row.html`, `templates/documents/**`, `templates/cases/**`,
`apps/cases/services.py` (slice: lines 783, 798) · `apps/academy/**`, `templates/academy/**` · `templates/account/**` and
`templates/allauth/**` (the one span) · `scripts/i18n_audit.py` · tests: `tests/i18n/test_catalogues.py`, NEW
`tests/i18n/test_arabic_completeness.py`, NEW `tests/i18n/arabic_allowlist.py`, `apps/companies/tests`, `apps/documents/tests`,
`apps/academy/tests` · `docs/I18N_RTL.md` · `docs/design-v5/QA/v524/ar/NOTES.md` + `LOCKED_BLOCKS_REGISTER.md`.

**Budgets.** Catalogue +42 (+3 reworded) msgids in it/en/ar, 100 % in every language, no fuzzy; 50 data rows × 3 languages; 0 CSS,
0 JS; no migration (no model change); `KNOWN_FRENCH = {}`; the test under a minute, non-browser, one database.

**Tools.** The audit's detector and crawler (`.work/v524-audit/v524-arabic/`), the native-reader second pass on the 42 entries
(register, «، ؛ ؟», Western digits, LRM after Latin runs, the plural of courtesy), `scripts/i18n_audit.py`.

**Gate (reviewer, targeted; V5.25 §2 «Arabic → the affected AR surfaces + representative widths»).** (1) `scripts/i18n_audit.py` clean;
the four catalogues compile; `tests/i18n` green incl. `test_locked_derived_msgids_are_never_translated` (empty table) and
`test_no_unreviewed_locked_fragment_in_the_catalogue`; `test_arabic_completeness.py` T1–T5 green with `KNOWN_FRENCH = {}`; every
allowlist entry justified. (2) The rendered crawl of `/ar/` (public, questionnaire walk, the four audiences' reserved area) re-run: 0
team-written French runs; the only French left = the class-C keys (count = the register's 131). (3) Headed under a slot, 1440 and
390 ar: a pathway sheet (the five stage titles), the questionnaire step 1 and a result page, the enterprise space's needs list and form
(sectors, regions), the person's dashboard «now» card and case file (the requested documents), the FAQ heading, the Forum head, the
Academy catalogue (the provider's name) — Arabic text, right-to-left, Western digits, the brand run unbroken at 390 (M1), «Privacy
Policy» isolated (M2). (4) The it/en twins of the same surfaces show the same 84 texts in Italian / English. (5) Locked copy
byte-identical (`locked_content.sha256.json`); no msgid of a locked text in the catalogue. (6) The owner question delivered as
`06_owner_question.md` says (R7), the default B recorded in the notes and the DL entry.

**AMENDED SCOPE (V5.27, R7′) — in addition to W1–W5 above.** (a) The classification of every locked key into C-UI / C-SUBST-IT /
C-SUBST-FR / C-OFFICIAL with the treatment and the source route, written to `docs/design-v5/QA/v524/ar/LOCKED_BLOCKS_REGISTER.md`
(keys, classes, counts, reasons — no personal datum). (b) NEW `apps/cms/locked_renderings.py`: the provisional professional Arabic
renderings of every C-UI key (native reader's second pass; formal institutional register; «، ؛ ؟»; Western digits; LRM after Latin
runs; the brand through `brand_bdi`), each with `status = "PROVISIONAL — PENDING LANGUAGE/LEGAL REVIEW"` and the treatment table of
the other classes; `locked_content.get()` consults it (the French texts, `LOCKED_TEXTS`, `locked_content.sha256.json` and
`scripts/lock_content.py` untouched — `tests/compliance/test_locked_content.py`'s byte-identity stays green). (c) The `{% locked %}`
tag (`apps/core/templatetags/ile_core.py`, now AR's file): the caption for C-SUBST-IT / C-SUBST-FR on the source route, the hidden
form with the Arabic pointer line elsewhere; the page lanes' templates untouched. (d) The identification caption's Arabic text (one
msgid, catalogue it/en/fr too), the pointer line's msgid; both professional, Arabic reviewed. (e) CSS: none if an existing label-role
class serves the caption; otherwise ONE rule in a slice of `static/css/v5/base.css` (recorded; the bytes paid in the same sheet,
R4 c; T merged before AR starts). (f) The dev board (`/__design-v5/`) lists every locked key with class, treatment and status
(internal). (g) `tests/i18n/test_arabic_completeness.py` re-specified as R7′ says; `arabic_allowlist.py` holds the (4) keys and the
proper-name / quotation tables computed from the register, nothing typed. (h) The rendered Arabic verified natively (V5.27 §4) in
the lane's headed gate: hierarchy, weight, leading, size, mixed Arabic/Italian terms, numerals, phone numbers (the configured
channels compared in process, never printed), e-mail addresses, abbreviations, direction, arrows/chevrons, tabs, routes, actor map,
FAQ, glossary, forms, mobile navigation. (i) The three counts for §5 in the NOTES and the DL entry.

**Files owned — additions.** `apps/cms/locked_content.py` (the `get()` seam only; French and checksums byte-identical) ·
`apps/cms/locked_renderings.py` (new) · `apps/core/templatetags/ile_core.py` · `tests/compliance/test_locked_content.py` (slice:
new guards only, the byte-identity test unchanged) · NEW `tests/i18n/test_locked_renderings_v524.py` · `apps/design_preview/**`
or the dev board's template for the locked-keys listing (the board's owner lane is none in §3; AR takes the one listing partial) ·
`static/css/v5/base.css` (one-rule slice, only if (e) needs it) · `docs/design-v5/QA/v524/ar/LOCKED_BLOCKS_REGISTER.md`.

**Gate — amended items.** (1) adds `test_locked_renderings_v524.py` and the byte-identity of every French locked text. (2) the
rendered crawl of `/ar/`: 0 unintended French; every remaining `lang="fr"` run is a C-SUBST on its source page with its caption or a
C-OFFICIAL key; the count of (1), (2), (3) keys equals the register's. (3) headed, 1440 and 390 ar, adds: the home (hero, entrances,
pilot sequence in Arabic; the «lo strato» plates and «la protezione» with their Arabic question / keyword and pointer line, no French
body), a pathway sheet (Arabic title; the description as identified source with its caption), the FAQ (Arabic questions; answers as
identified source), the glossary (definitions identified), Attention aux fraudes, Entreprises and its form (Arabic labels, the consent
identified), the Forum page in Arabic, AGAMI (Italian authoritative identification where it applies), Diplômes — plus V5.27 §4's
list. (6) replaced: the three counts recorded in the NOTES and the DL entry; the owner question closed as answered (V5.27).

### 3.9 Lane CLOSING — cleanup, ratchets, catalogue, handoff (`v524-closing`; ≈ 1.5 days; after every merge)

**Scope (V5.24 §18, §26, §27; V5.25 §6; SECTION_SYSTEM_V2 §9.6).** (a) **Dead chapter / editorial CSS**, removed only when verified
unused by Chromium coverage (the V5.20 method) over EVERY route — the public routes with every gate open (`core.public_routes`,
`gated_routes()` included), the four error pages, the seven forms' error state, the nine personas' pages, the dev board — in fr and
ar at 1440 and 390: candidates `chapter__*`, `section__header`, `he__body`, `reveal-mark`, `.fronte__wide*`, the retired glossary rules
of `_lettura.css` (if PUB2 left them), the duplicate V1/V4/V5 editorial helpers in `_pagina.css`, `_compose.css`, `_interior.css`,
`_reveal.css`, `_spaces.css`, `_pathways.css`, `pages.css`, `static/css/{base,layout,components,register}.css`, `v2/*`, `v4/*`.
**Rules still used by a legacy template stay** (the questionnaire's `orientation/*`, `news/*`, `community/*`, `consents/*`,
`partners/index.html`, the forum's gated partials, the preserved forms' `.chapter--area`): no re-composition of those pages (out of
scope; V5.25 §1). `_chapter_head.html` / `_section_header.html` stay while a template includes them. (b) **The fade-up default**
(`rise.js` translateY + opacity) removed from the public pages where it is the only motion left (§5.1's «15 pages»: the legal pages,
the CMS reading templates, published news) and from the Entreprises `#formulaire` chapter HEAD (`companies.html:64`; the form body
preserved, V5.22 §24); the two form pages' `reveal-mark` and the portal's `data-rise` stay recorded (§9.8). (c) **Ratchets:** every
per-sheet and per-page ceiling to its measure (`test_frontispiece_v515_c.py`, `test_pages_v522_p1.py`, `test_home_v522_h.py`,
`test_sezioni_v522_s.py`, the fonts' `test_fonts_budget_v2.py`), `main.css` to its new measure (≤ 32 716); T's `TYPOGRAPHY_BURNDOWN`
asserted empty and the table deleted. (d) **F2-m1** (R6): the trim of the keyboard-tier guards in the library and lane H's one modality
rule; measured on 8782 paired against the base (`v522/p2`), n ≥ 5, desk + phone, fr + ar; the result recorded in the DL entry in R6's
words. (e) **The single catalogue pass:** `scripts/i18n_audit.py --sync --compile` over the merged tree (professional it/en/ar for any
string a lane added; Arabic reviewed; locked text never translated), 100 % in every language. (f) **Docs:** `SECTION_SYSTEM_V2.md`
errata blocks (§2.1 + §2 the material primitives and «il raccordo»; §6.2 the twelve steps replace «eight sizes, no ninth» and the
Vazirmatn rules; §8 the credits superseded by V5.24 §2 (lines 203, 316, 330, 793, 801, 875, 1774, 1892); §9.7 the v524 ownership
table; §9.8 the three recorded exceptions — tokens.css/base.html (typography), the platform's tokens (PLAT), the preserved first
screen's weight through the tokens); `DESIGN_SYSTEM_2026.md:2953-2958`, `:4379-4384` (PX's two blocks); the H/P2 NOTES lines; **NEW
`docs/design-v5/HANDOFF_V2.md`** (concise, V5.24 §26: a «Tools used — real provenance» table copied from
`evidence/v524/TOOLS_AVAILABILITY.md` with each lane's real skill / MCP names (V5.27 §6); the reusable primitives and their attributes, the grounds and transitions, the
motion tokens and verbs, the typography rules and the twelve steps, the icon tiers, the Arabic rules, the budgets and ratchets, «no
regression to chapter layouts»); `live_status.json` families «Typography V2», «Section Background/Material V2», «Imagery V2 ·
credits», «Arabic Complete», the four lanes' Page Composition V2 pass; `CHANGELOG_V54.md` (Italian). (g) `check_ownership`'s
FAMILY_ID extension if the steward has not already made it (R11).

**Files owned.** Everything (sequential; no concurrent lane) — in practice the sheets and tests named above, `static/js/src/rise.js`
and its callers, the docs, `scripts/check_ownership.py` + `tests/test_check_ownership.py`, `docs/design-v5/QA/v524/closing/NOTES.md`
(with the coverage report and the before/after measures of every sheet).

**Budgets.** Only down: every sheet ≤ its pre-CLOSING measure; `main.css` ≤ 32 716 and ratcheted to the result; JS ≤ today's
(`rise.js` 1 325 ≤ 1 536; a smaller `rise.js` re-recorded); page totals ≤ their letters and re-recorded at the measure; fonts unchanged.
INP per R6.

**Tools.** Chromium coverage (`Profiler`/`CSS.startRuleUsageTracking` through Playwright, the V5.20 scripts under `.work/v520-css/`),
improve-animations only for the F2-m1 trim (read-only survey → the narrowed selectors), `scripts/i18n_audit.py`.

**Gate (reviewer).** (1) Coverage report: every removed rule unused on every route in both languages and widths; a rule used anywhere
was kept (spot-check 20 removed rules against the report). (2) The lane's targeted modules + the guards around the removed rules
(`test_chapter_marks.py`, `test_journey_w3_d.py`, `test_frontispiece_v515_c.py`, `test_pages_v522_p1.py`, `test_home_v522_h.py`,
`test_sezioni_v522_s.py`, `test_typography_v2.py`, `test_rm_flag_parity.py`) green; the ceilings equal the measures. (3) The legacy
pages (questionnaire start / result, a news page, the legal pages, the forms) render as before but for the fade-up: headed at 1440
and 390 fr, one each. (4) F2-m1's figures with the base's beside them. (5) The catalogue 100 %, no fuzzy. (6) `HANDOFF_V2.md` read
once by the reviewer: every primitive it names exists in the tree with the attribute it names. (7) MERGE → then the matrix.

---

## 4. The ONE acceptance matrix (V5.25 §3; after CLOSING's merge; ≈ 0.5 day; label `v524-matrix`)

On the exact tree of CLOSING's merge, served by a fresh lane server (and 8782 for the performance cells).

**Automated (headless, no slot) — 1440, 1280, 1024, 768, 430, 390, 375, 360 × fr, it, en, ar, over every public route with the gates
open + the four error pages + the nine personas' pages:** overflow 0 and no unclipped element wider than the page; one `h1`; no chapter
head on a V2 page; the adjacency rule (stone ≡ pietra); every `data-ground` in the six kinds; fonts fetched within the per-page
ceilings, Readex Pro on `/ar/` only, no Vazirmatn; no Pexels / Unsplash / «Photo by» text, no `figcaption` in a `figure[data-slot]`;
the Arabic detector 0 unintended French (R7′: every `lang="fr"` run a C-SUBST block on its source page with its caption or a C-OFFICIAL key; the C-UI keys in Arabic; the proper-name / quotation allowlist only); no text under 14 px below 48 rem; every `lang="fr"` element
≥ 20 px on `/ar/` at Latin leading; after a play-through 0 animations at rest and only `finished` entries; under reduced motion no
`data-sec-state` and 0 animations; keyboard: one Tab sets `html[data-input="key"]`, no animation; 0 console errors; axe serious /
critical 0 on the representative pages (home, Parcours, a sheet, Entreprises, Institutions, FAQ, Glossaire, Contact, AGAMI, the person
and company dashboards, the case file, documents, login) in fr and ar; both contact channels present on `/xx/contact/` (compared in
process); locked copy byte-identical. Performance on 8782 (slow 4G, CPU × 4, n ≥ 9): LCP ≤ 2.5 s mobile per page type fr and ar; CLS
≤ 0.1 (≤ 0.05 home and landings); INP ≤ 200 ms per R6 (first Tab, first pointer after keyboard, tabs, map, explorer, disclosures,
doors). Script and JSON under `.work/v524-matrix/`, stills under `evidence/v524/matrix/`.

**Headed Chrome, manual, V5.25 §4's priority (two slots, sessions ≤ 25 min):** Home; Navbar / mega menus; Lume; Parcours; Entreprises;
Institutions; Universités; FAQ / Glossaire; AGAMI; the person dashboard; the company dashboard; the institution / university spaces;
Documents; Case file; Forms; the mobile menu; Arabic / RTL — at 1440 and 390 in fr and ar, 1024 and 360 where the page has a
breakpoint there; reduced motion once per page. «Do not spend the same manual effort on every static page.»

**The six dimensions, ONCE per major page** (§26 / §10; the home 4.5 composition and coherence): recorded in `evidence/v524/MATRIX.md`
with the stills. A page under 4 on a dimension → its lane fixes that defect once (targeted) → that page re-checked only. No
re-scoring of a page a shared change did not touch. ARABIC = PASS/FAIL (visible unintended French = FAIL, V5.27 §3; the Arabic pages judged as natively designed per V5.27 §4 — hierarchy, weight, leading, size, mixed Arabic/Italian terms, numerals, phone numbers, e-mail addresses, abbreviations, direction, arrows/chevrons, tabs, routes, actor map, FAQ, glossary, forms, mobile navigation).

## 5. The ONE technical gate (V5.24 §30, V5.25 §7, V5.20; ≈ 0.5 day; label `v524-gate`)

On the same tree: the full non-browser suite (one pytest, one database); the browser suite (under a slot); `ruff check .` 0;
`manage.py check`; `makemigrations --check`; `npm run build` twice, identical dist; `tests/security/**` incl.
`test_confidential_material.py` with `ILE_CONFIDENTIAL_SENTINELS` (in-process, values never printed); the i18n and RTL suites;
`tests/compliance/test_imagery_credits_v524.py`; `tests/i18n/test_arabic_completeness.py`; `tests/compliance/test_locked_content.py`;
`scripts/check_ownership.py --validate`. **FAILURES 0 · BLOCKING LINT 0 · UNEXPECTED SKIPS 0 (the one environment-bound skip named)
· P0/P1 0.** A test changes only under V5.20's four conditions, cited.

Then the steward: annotated local tag **`v524/gate`** on the exact SHA; the preview 8780 restarted on it through the acceptance launcher
and verified (R13's list); the report **«FINAL V2 ACCEPTANCE READY»** — Candidate `<exact SHA>`; Visible families: Homepage
Composition V2 · Page Composition V2 · Section Background/Material V2 · Typography V2 · Motion Density V2 · Imagery V2 (credits removed)
· Icon Treatment V2 · Arabic Complete (V5.27 hybrid: provisional professional Arabic on the compositional keys; the substantive blocks identified Italian / identified source / hidden until validated) · Premium Forms · Global Lume · Premium
Navbar; **Arabic:** unintended French fallback: 0 · provisional non-legal Arabic: `<count of C-UI keys>` · untranslated authoritative legal blocks: `<count of C-SUBST keys + treatment split: identified Italian / identified source on its page / hidden elsewhere>` (V5.27 §8); Tests `<results>`; Outstanding P0/P1: 0; Outstanding owner items: §6; Preview URL http://127.0.0.1:8780/__design-v5/. **Then freeze.** No `main`, no `v2.0.0`,
no GitHub release, no deploy (V5.24 §32).

## 6. Owner questions (only genuine legal / brand / policy items)

1. **ANSWERED 5 Nov 20:08 — V5.27 hybrid (R7′); kept for the record.** The locked French blocks on the Arabic pages (`evidence/v524/arabic/06_owner_question.md`, in Italian for the owner): 130
   prescribed keys + the Forum's prescribed title, 1 897 French words, 53 keys / 691 words on the home's first screen, shown in French
   with `lang="fr"` on the Arabic site. **A** team-written provisional Arabic renderings flagged as such pending the legal referent's
   version · **B** French kept as source text and allowlisted by key (the default, applied now) · **C** A for the ≈ 35 non-legal
   compositional keys, B for the legal content. The outcome explanations quote the pathway family accordingly. The product ships
   complete on team copy under any answer; only this decides whether the Arabic home's first screen reads Arabic in this candidate.
2. **The Arabic reader's review (owner item B2, still open for Vazirmatn) now covers Readex Pro** — a brand / Arabic-register item on
   the owner's side; the exhibit is `v524-typo/shots/compare_1600.png` + the Arabic home still. Not blocking; the face is a design-system
   decision inside V5.24 §11–§14's mandate.
3. **The door photograph's written rights record** (IMAGE_LICENSES §7.1; `static/brand/v5/PROVENANCE.json`, D22): an owner action for
   the go-live checklist, not for this candidate.

Nothing else is asked: no font, no background, no animation, no icon treatment, no component, no pattern (V5.24 §33, V5.26 §10).

---

*Evidence index:* the four audits under `C:/tmp/ile_v5_council/evidence/v524/`; the measurements of §0 taken on `4bafcfa0` on 5 Nov
2026 (gzip -9 over `static/css/dist/**`, `static/js/dist/**`, `static/fonts/`); the ownership checker and manifest
`scripts/check_ownership.py`, `docs/design-v5/OWNERSHIP_V54.json`; the steward model `.work/v522-h-merge/`, `.work/v522-p2-merge/`;
the F-M2 figures DL54-185 item 3. This plan changes nothing in any repository; it is the work order.
