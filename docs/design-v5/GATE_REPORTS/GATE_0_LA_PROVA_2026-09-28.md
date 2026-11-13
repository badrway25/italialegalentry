# Gate 0 «La prova» — closure report (28 September 2026)

**Status: CLOSED FOR THE OWNER'S REVIEW — nothing is signed, nothing is in force.** The composed
screens, the reviews and the signing sheet live outside the repository in `C:/tmp/ile_v5_council/proof/`
(entry page `index.html`, sheet `SIGNING_SHEET.md`, reviews in `reviews/`). No tracked file of this
repository was changed by any gate-0 lane: every lane compared `git status --porcelain --ignored` before
and after (identical, 800 lines each time). This report records the outcome so that the repository carries
the checkpoint the owner asked for; the pictures themselves are the deliverable.

## 1. What was built

Three rounds (27–28 September), 45 agent runs in all, every one read-only on the repository:

| Round | Work | Outcome |
|---|---|---|
| 1 | Foundation (V5 fonts, tokens, components, 110-symbol icon sprite, CSP capture harness), photographs, six comps (home interim + phase 3 in fr/ar, login «Il varco», console shell + person dashboard, «Mes pièces» + chip board, journey + hero-lights prototype, interim phone hero measured on 8770), three independent reviews, an ECD closing pass | Design NOT READY (2 blocking), red team and accessibility PASS WITH CONDITIONS; the ECD's fixes unverified |
| 2 | New photographs (Persona 7128956, Impresa 5973984, Università 32254672 — hands only in the diptych, no photographer twice, no gridded window), hero options H-A «La porta, piena» and H-B «Il pilastro e la soglia», production-shaped build `_prod/`, 44 px touch targets, three fresh verifiers, two fix loops | R3: design NOT READY on a stale package, red team and accessibility READY WITH CONDITIONS |
| 3 | Fixes of every verified finding, full re-shoot with `tools/currency_check.py` (fails if any capture is older than its sources), fresh verifiers, a last loop, a text-only sheet update, then a closure step (quiet-machine INP, index regeneration, two independent text verifications of every rewritten sentence) | Below |

## 2. The verdicts, verbatim (latest independent verification, R3B, 28 September afternoon)

- **Design** (`reviews/DESIGN_VERIFY_R3B.md`): «READY WITH CONDITIONS. No blocking finding remains.» —
  «The hero: sign H-B «Il pilastro e la soglia»».
- **Red team** (`reviews/RED_TEAM_VERIFY_R3B.md`): «READY_FOR_OWNER. No blocking finding; no major open.» —
  «The package is current, and it is what the comps show.»
- **Accessibility · RTL · performance** (`reviews/A11Y_RTL_PERF_VERIFY_R3B.md`): «READY_WITH_CONDITIONS» ·
  «No blocking finding.» · «V2 stays partial (major).» · «M3 stays a build condition (S2)».
- **Text of the signing package** (`reviews/TEXT_VERIFY_CLOSURE.md`, `_2.md`, 28 September evening):
  READY_WITH_CONDITIONS twice — «Nothing in SIGNING_SHEET.md or index.html misleads the owner about what they
  sign»; 420 + 220 sentences checked against their sources; the five remaining items are stale wording on the
  safe side (a «da verificare» mark kept after verification, a one-edit lag in the appendix, two sentences of the
  index notice). A final wording pass was launched at closure; its result is appended to the sheet, not here.
- **Package currency**: `SUMMARY 2026-09-28 21:02:26: 134 linked captures — 104 current, 30 declared records,
  0 failing; 119 sheet inputs checked; 0 unresolved links; 0 missing index links -> PASS` (reproduced by both
  text verifiers).

Design scores, round 1 → R3B (1–5): premium 3.5 → 3.5 · coherence 3 → 4 · typography 4 → 4 · colour/material
4 → 4 · imagery 3 → 3 · iconography 3 → 4 · motion 3.5 → 3.5 · UX clarity 4 → 4 · mobile 4 → 4 · identity 3.5 → 4.
The design verifier's reading: the craft and the system hold; «premium» and «imagery» stay at 3–3.5 because the
first screen is still an owner decision (O67) and the photographs are provisional under O54/O55.

## 3. What remains open — stated precisely, not closed by courtesy

1. **The approved budget's clause «no avoidable long task > 50 ms» is met by no page** (A11Y V2, partial,
   major). Every comp has one first-render task; in the R3B lab it measured 540–890 ms at CPU ×4, against
   1 190–1 650 ms for today's live home on 8772 measured in the same lab (about 65 % style/layout). LCP, CLS and
   INP meet the budget in every verifier cell under profile A (slow 4G + CPU ×4). Whether the remainder counts
   as «avoidable» is the owner's reading; the V5.1 directive §61 orders the breakdown.
2. **Console drawer INP** (A11Y R3B-N3 → `perf/INP_QUIET.md`): no quiet machine existed (another project's
   test suites ran on the laptop throughout). On mains, CPU ×4, cold open median 200 ms (p90 264); in the quiet
   seconds 160 ms (p90 200); at CPU ×1 everything under 65 ms; today's live drawer on 8772: 64 ms. Cause:
   `dialog.showModal()` restyles the whole document (633–811 elements) on open and close. Inside the budget on a
   quiet machine, with no margin against a 1.5× slower device → build condition: open the drawer without
   restyling the document.
3. **Public mega-menu and drawer keyboard model** (A11Y M3): a build condition of S2 by the plan.
4. **The first screen is not corrected, it is chosen** (DR M1 → **O67**): H-0 (today's composition), H-A
   (the door full, 1.26× wider, the four photographs peeking) or H-B (the door as a full-height pillar, the four
   audiences as a band at the threshold). Both the hero designer and the design verifier recommend H-B with five
   S1 conditions. **Not approved**: the V5.1 directive (§6, §78, §79) requires a live visual review of H-0/H-A/H-B
   and allows an H-C before any choice.
5. **Arabic**: the faces (Vazirmatn, Markazi Text) await the Moroccan reader review (O10, blocking for /ar/); the
   phase-3 /ar/ comp carries locked copy that is untranslated on 8771 and is marked «NON TRADUITE — ne pas signer».
6. **Not tested anywhere in gate 0**: real devices, Safari, Firefox, a screen reader, a Moroccan reader.

## 4. The four provisional rulings the pictures were built on (to be confirmed or overturned)

O54 the scope of F15 read prudently (no arcades, passages, steps, vaults, doors, gridded windows as subjects) ·
O55 no identifiable person · O14 VALIDE in ink, no check mark on any status, station, actor, rail, ledger row or
chip · O57 no tricolour filet. The sheet states what changes under each opposite ruling.

## 5. Gate A (mobile) — how gate 0 answers it

The interim phone hero prototype (`proof/phone-hero/`, Solution A, measured on the running 8770 home with injected
CSS): at 360×800 / 375×812 / 390×844 / 412×915 the hero ends at 96.0–96.5 % of the viewport (today: 119–142 %),
the door is 242 × 300 (today 180 × 223 at every width), both actions sit in the first screen with ≥ 56 px under
the secondary, the interim title has its own setting (O45). The owner ruled (V5.1 §7): V4 stays the baseline and
control; the mobile correction is integrated in V5 rather than back-ported to V4; target mobile ≥ 4 before final
propagation. The gate-A mobile item therefore closes in V5 S1, not in V4.

## 6. Tools, reported honestly

- **Pexels**: round 1 downloaded the council's shortlist at full resolution; round 2 searched and downloaded three
  replacements (Persona, Impresa, Università) with provenance in `proof/assets/img/photos/PROVENANCE.json`. All
  images are provisional (O54/O55) and outside the repository.
- **21st.dev**: no new catalogue search was ordered by the gate-0 prompts; the comps drew on the council's
  `21ST_COMPONENT_MATRIX.md`. **UI-UX-Pro-Max**: not called by the gate-0 prompts. **Emil Kowalski design
  engineering skill**: not yet evaluated (V5.1 §8). **Motion**: prototyped in the comps with plain WAAPI/CSS, not the
  Motion library.
- **Browsers**: headless Chromium only, each lane in its own profile; the QA Chrome on 9222 was never used.

## 7. What the owner does next

1. Open `C:/tmp/ile_v5_council/proof/index.html` (or serve it with `tools/shoot.py --serve`) and read
   `SIGNING_SHEET.md` §0 first.
2. Sign or refuse the pictures (O59); confirm or overturn O54, O55, O14, O57; adopt or replace the three new
   photographs.
3. O67 is deferred to the V5.1 live preview (H-0/H-A/H-B side by side in a visible Chrome, H-C allowed).
4. Say whether the first-render task counts as an «avoidable» long task under the approved budget, or whether the
   budget clause is to be read as «no avoidable long task beyond first render».

## 8. Process notes

- The session died at about 02:00 on 28 September during round 3 (machine restart). The interrupted lanes' partial
  edits were reconciled against their before-copies by the rerun and are disclosed in `reviews/FIXES_R3_DESIGN.md`
  §0 and `FIXES_R3_A11Y_PERF.md`.
- Superseded derivatives and backup pages were moved (not deleted) to `C:/tmp/ile_v5_council/_attic/`.
- The stale-package defect (captures older than their sources) appeared in four design verifications out of five
  before `currency_check.py` made it mechanical; from R3 on, every package step and every verifier runs it.
