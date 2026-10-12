# RED TEAM — V5 «La soglia»

**Italy Legal Entry™ · Independent Red Team (visual QA · accessibility · performance · institutional credibility) · 27 September 2026**
**Object:** the proposal in `C:/tmp/ile_v5_council/final/` (CREATIVE_DIRECTION_V5, DESIGN_SYSTEM_V5, 21ST_COMPONENT_MATRIX, 21ST_SEARCH_LOG, ASSET_USAGE_MATRIX, ICON_SEMANTIC_MAP, IMPLEMENTATION_PLAN) and the fifteen council reports in `council/`. Nothing is built; this reviews a specification.
**Rules I kept:** the repository `C:/tmp/italylegalentry` was only read (HEAD `c9a58d8`, `git status` clean before and after); this file is the only thing I wrote. No browser was driven, no form submitted, no password typed, no secret printed, no 21st.dev or Pexels call made.

**Method.** I read all seven final documents in full. I read the council reports where a final decision rests on them (UI_INVENTORY §1–§6 and §10, MOTION §0–§14, CAPTURES_AND_REFERENCES §2–§3, UX_PUBLIC §0–§2, UX_PLATFORM §0 and §3.13–§5, MOBILE_UX §0–§3, IMAGERY, COLOUR §14, TYPOGRAPHY, and the 21st curations' compliance lines). I checked the claims that touch hard constraints against the repository itself: `config/settings/base.py` (CSP), `scripts/fetch_images.py` (editorial rules and `FORBIDDEN_SUBJECT_KEYWORDS`), `docs/IMAGE_LICENSES.md`, `docs/design-v2/BRAND_ASSETS.md`, `docs/design-v4/DESIGN_SYSTEM_V4.md` §1.8, `tests/frontend/test_chips_registry.py`, `tests/frontend/test_v4_tokens.py`, `tests/frontend/test_static_assets.py`, `static/js/src/home.js`, `apps/cms/templatetags/cms_nav.py` and the templates that render the brand name. I looked at seven visual artefacts: the colour specimen and chip board (`captures/colour/specimen_1440.png`, `specimen_chips.png`), the type specimen (`council/typography/specimen.png`), the icon specimen (`council/icons/specimen-render.png`), the loader stage frames (`scratch/loader/sheet_stage_v2.png`) and the journey frames (`scratch/journey/frames/home_ltr.png`). I recounted the component registry by script: 113 types · 72 Adapt · 32 Custom · 9 Unchanged · 84 reviewed on 21st. The finals' counts are correct.

**Severity.**
- **BLOCKING:** must be resolved before the owner signs, or before the named phase starts. It breaks a hard constraint or a legal rule already enforced in the repository, or it would have the owner sign on a false premise.
- **MAJOR:** must be fixed before the gate of the phase it touches.
- **MINOR:** fix inside the step, at low cost.

---

## 0. Verdict

**Not ready for signature as written. The fixes are well defined and none of them needs a new direction.** The review found **4 blocking, 19 major and 18 minor** issues.

**What holds up, and should not be traded away.**
- The CSP discipline, 0 React islands, no WebGL and no shaders.
- Law 2.2 («nothing painted is taken back») with a frame test.
- The composited loader, measured under CPU ×4 with a block test.
- The font diet, measured file by file: 356 KB → 74 KB on the home.
- Contrast proven by a script: 363 pairs.
- A reduced-motion still state for every pattern.
- Every chip keeps its word.
- A candid §25 in the Creative Direction.

**The four risks that decide whether V5 reads as premium or as one more over-designed portal:**

1. **Legal semantics.** VALIDE turns chromatic (lapis blue) and gets a filled disc with a check, and done journey nodes also carry a check. Both contradict the rule the repository already enforces: `conforme` takes the ink, with no chroma, because «no colour ever means approved».
2. **The photographic concept «Due portici» sits on the forbidden-subject boundary.** It is built on arcades, a vault, steps and a passage. The project's own register forbids «porte/soglie» and «griglie/cancelli», and it has already rejected a corridor because it «evokes grids/thresholds».
3. **Nothing has been composed.** No page of V5 exists as a picture. The owner is asked to sign 53 decisions on ≈ 400 KB of prose, which is the process that produced «not premium enough» the first time.
4. **Saturation.**
   - The arch and door motif appears in about 15 places.
   - The gold light appears in about 10 contexts.
   - Glow, glass, mesh and grain sit together on navy with cyan buttons.
   - The passage draws a cyan line that rises from Morocco to Italy, with glowing points.

   Together these push the result toward a fintech/crypto landing page, the opposite of «institutional but modern». The finals also contradict themselves in ten places (§5), which is the first symptom of «many authors pasted together».

---

## 1. Summary

| ID | Sev. | Area | Issue |
|---|---|---|---|
| B1 | BLOCKING | legal · colour · icons | VALIDE is chromatic with a check; done journey nodes carry a check. This breaks the enforced «conforme = ink, no chroma» rule. |
| B2 | BLOCKING | imagery · hard constraint | «Due portici» (arcades, passage, steps, vault) is at odds with F15 «porte/soglie, griglie/cancelli» and its precedents. |
| B3 | BLOCKING | process · premium | No composed visual of any flagship screen exists; the owner would sign on text. |
| B4 | BLOCKING | missing component | The public orientation questionnaire (the hero's locked primary CTA) is absent from the registry and the plan, and it still shows a percentage bar. |
| M1 | MAJOR | coherence · type | The brand name is set in two serif faces in one viewport (lock-up Newsreader vs hero H1 Source Serif). |
| M2 | MAJOR | identity · repetition | The arch/door motif appears in ≈ 15 places, against the CD's own «the arch belongs to the door». |
| M3 | MAJOR | aesthetic · effects | The density of gold light, glow and glass reads as fintech/crypto. |
| M4 | MAJOR | credibility · journey | The passage route rises from Morocco (low) to Italy (high): it reads as a growth chart and as a hierarchy. |
| M5 | MAJOR | a11y · performance · feasibility | The hero's infinite travelling lights have no pause control (WCAG 2.2.2), are not prototyped, and cannot follow routes that `home.js` re-measures at runtime. |
| M6 | MAJOR | UX · a11y | On phones the action bar replaces the bottom bar and the top ≡ is removed, so no Menu remains on the case file or the wizard. |
| M7 | MAJOR | grounding · mobile | «Mobile corrected, door +81 %» is true only for phase 3 at nominal viewports; in the interim phase the door shrinks and the hero exceeds 100 %. |
| M8 | MAJOR | performance | The CSS estimate (+8–11 KB gz) is not grounded; with old sheets kept until P4, the render-blocking bundle can pass the plan's own 50 KB ceiling. |
| M9 | MAJOR | performance | JS headroom is 4.5 KB against unbudgeted modules; the `motion/mini` saving is deferred to phase P. |
| M10 | MAJOR | brand · semantics | The loader animates the locked mark (key, tricolour planes) and «unlocks the door» during waits whose outcome is legal. |
| M11 | MAJOR | a11y · status | 12 px ledger pips separate three registers only by a knocked-out micro-glyph; eight-colour pip rows risk reading as candy. |
| M12 | MAJOR | constraint · references | The section grammar, the portico panel and the mobile drawer closely match agamieuromed.org elements (principles only is the rule). |
| M13 | MAJOR | credibility · licensing | Identifiable stock people sit on the «Persona» door in an immigration context; the imagery relies on ubiquitous Pexels studios; a named real civic building stands for «Institutions». |
| M14 | MAJOR | repetition | The anti-fraud «il gradino» can appear 3–4 times on one page. |
| M15 | MAJOR | missing components | Community, prose/legal pages, glossary, living cards, account pages, assessment outcome, non-person homes and the back-office have no V5 component. |
| M16 | MAJOR | grounding · coherence | The public «La soglia» signature depends on legal D-U9 and the closed gate G3, so visitors may never see it. |
| M17 | MAJOR | brand · decisions | The tricolour filet outside the mark is stated as law, but it is missing from the owner decisions and contradicts V4 DS §1.8 and BRAND_ASSETS. |
| M18 | MAJOR | process · read-only | The read-only phase was breached during the council (`.playwright-mcp/` in the repo, a QA cookie deleted, 7 DB session rows). |
| M19 | MAJOR | performance | «One L1 per view» is enforced only per template; runtime composition can exceed it (measured 51–67 ms tasks). |
| m1–m18 | MINOR | various | §4 |

---

## 2. Blocking

### B1 — VALIDE becomes a verdict colour and the check becomes a verdict mark

- **What.**
  - VALIDE (`conforme`) gets lapis (`--p-registro-600 #284b8f`, body `#e6efff`) and the mark «filled disc + check»: CD §3 ruling 2, §12 table, DS §3.2.
  - Done journey nodes get `--node-done-fill: registro-600` with a white glyph (DS §4). The colour specimen draws that glyph as a **check** (`captures/colour/specimen_1440.png`, «4. Parcours — fait»).
  - The chip specimen labels the chip **«Validé»** (a past participle, «validated»), while CD §12 says the word stays «Valide» (`specimen_chips.png`, `specimen_1440.png` §1).
- **Why it blocks.**
  - The repository states the legal rule and tests it. `tests/frontend/test_chips_registry.py` l.10–13: «`conforme` must take the chapter's ink — **no chroma** — because no colour on this platform ever means approved».
  - `test_v4_tokens.py::test_no_register_is_painted_with_the_verdict_green_or_the_accent` guards the same line, and UX_PLATFORM §5 repeats it («`conforme` is ink without chroma»).
  - Blue plus a check in a filled disc is the universal «approved/OK» sign, whatever a legal footnote says.
  - CD §11 itself forbids «ticks on stations», and the DS/COLOUR node spec reintroduces them.
  - Presenting this as «adopted, legal to confirm» (O14) inverts the burden: the existing law is the default.
- **Fix.**
  - Keep `conforme` achromatic: an inchiostro-900 mark on the carta body, as V4.
  - Replace the check with a non-verdict mark, for example a filled disc with a horizontal «recorded» bar.
  - Remove every check from journey nodes (done = filled ink dot, no glyph).
  - Purge «Validé» from the specimens.
  - Extend the tests: the `conforme` mark and body have chroma ≤ a small threshold, `STATUS["conforme"] != "check"`, and no `check` glyph in `.journey__node`.
  - If the owner and legal still want lapis, the decision is signed in writing **before F4**, and `test_chips_registry.py` is amended in the same commit with the signed wording.

### B2 — The photographic concept collides with the project's forbidden-subject rule (F15)

- **What.** «Due portici» selects:
  - two covered walkways: a Padua street under arcades (38843185) and a Casablanca covered walkway «with shop shutters» (34453419);
  - «la marche» (35816354), marble steps with a zellige riser, used for the Forum band, the Forum panel and the **home Forum teaser**;
  - the hero vault layer (17857002);
  - the Palazzo della Ragione loggia (39768540);
  - a portico video trimmed before a door enters (36909064).
- **Why it blocks.** Following the editorial rules is a hard constraint.
  - `docs/IMAGE_LICENSES.md` l.14 lists as forbidden subjects **«porte/soglie»** and **«griglie/cancelli»**; `scripts/fetch_images.py` docstring: «never … doorways, grids».
  - The project's own precedents reject, on a prudent reading, «lungo corridoio di vetrate a griglia: evoca griglie/soglie» (IMAGE_LICENSES §4) and a door seen in the background.
  - IMAGERY itself rejected 15138264 because «a long vanishing passage invites the “soglia” reading (F15, prudential)» (IMAGERY l.74). It then selected two passages.
  - Roller shutters on shops close shop entrances («shutters, not doors» is not a prudent reading).
  - The terrazzo steps got an F15 owner flag (IMAGERY l.213); «la marche», the same subject class, got none (l.160) and is placed on the home.
- **Fix.**
  - Get a written owner ruling on F15's scope (arcades, covered passages, steps, vaults), recorded in `IMAGE_LICENSES.md` §1 before **any** V5 photograph enters `CURATED`.
  - Apply the terrazzo standard to «la marche».
  - Re-crop or reject the Casablanca frame (shutters = entrances).
  - Prepare a non-architectural fallback for the diptych and the Forum band (craft, hands, working tables of each shore), so S1 does not wait for the ruling.

### B3 — No composed visual exists; «premium» cannot be judged from a text

- **What.** The only V5 visuals are specimens (type, colour, icons), two motion prototypes (loader, journey) and CSS injected into the V4 mobile hero (`scratch/`, `council/*/`). No V5 home, login, dashboard or documents page exists as a picture. The owner is asked for 53 signatures (CD §24).
- **Why it blocks.** The owner's complaint is visual («not premium enough»). V4 was also signed as a document and judged on screens. Several risks below (M1, M2, M3, M4, M14) are exactly what a composition would reveal in minutes, and a text cannot.
- **Fix: add a gate 0, «visual proof», before F1.**
  - Build static, CSP-clean HTML comps, self-hosted, built outside the repository (for example `ile_v5_council/proof/`), with the real V5 fonts and tokens.
  - Cover the home's first three screens (1440 and 390, fr and ar), the login, the dashboard (mid-case) and «Mes pièces».
  - Use two or three candidate photographs at full resolution after the B2 ruling.
  - Include one motion reel (arch light, journey, loader) frozen frame by frame.
  - The owner signs the pictures, then the decisions that implement them.

### B4 — The hero's primary CTA leads into a flow V5 does not design

- **What.**
  - The locked primary on the home is «Découvrir le questionnaire d'orientation».
  - That public wizard is V2: `orientation/wizard.css`, full-page POST per step, a **percentage progress bar**, inert `hx-*` attributes, plain radio lists, no busy state (UI_INVENTORY P60, UX_PUBLIC §2.2).
  - UX_PUBLIC §3.4 P3 says it «must receive the “Ma situation” grammar».
  - The finals dropped it: no registry type (FM09 is «Ma situation» only), no S-step. T3 only re-routes signed-in people, and S3 only adds a busy key.
- **Why it blocks.**
  - V5 would polish the door and then hand every visitor to the least designed page on the site.
  - A percentage bar contradicts the legal «no percentage, no score» rule cited throughout the finals.
- **Fix.**
  - Add registry type **FM12 «Questionnaire public»**: the FM09 grammar (one question at a time, «Question n sur N», no percentage), OptionCards, a busy key at submit, focus on the arriving question, the thread on each step, and the result page on the V5 kit.
  - Add plan step **S1b** (≈ 3–4 days) that ships with S1, and an acceptance test that asserts no `%` and no `<progress>` in the questionnaire.

---

## 3. Major

### M1 — The brand name in two serif drawings, 40 px apart

- **What.** On the phase-3 home, the lock-up draws «ITALY LEGAL ENTRY™» in Newsreader 600 (the wordmark), and the H1 directly below draws the same words in Source Serif 4 400 capitals at 40–72 px. The type specimen shows it (`council/typography/specimen.png`, first panel). The project page's H1 does the same (`templates/pages/project.html` l.14 via `{% brand %}`, set in `--f-serif`). CD §2 accepts it («the lock-up is a logo»).
- **Why major.** The eye compares the two drawings immediately. It is the most visible «two authors» signal on the most important screen.
- **Fix.**
  - Set **every** rendering of the trademark name in the «ILE Wordmark» face. The hero H1 and the project H1 are exactly the wordmark's glyphs, so this costs 0 bytes; add a ≈ 2 KB display instance if `opsz` 20 looks coarse at 72 px.
  - Adopt D-U1 option a: Source Serif carries the promise line.
  - Amend law 2 accordingly.
  - Add a test: the computed `font-family` of every `{% brand %}` and `.lock__wm` output is «ILE Wordmark» on public, console and `/ar/` pages (see also m10).

### M2 — Arch and door saturation

- **What.** The arch or door appears in:
  - the lock-up and its lock sweep;
  - the hero door, plus the arch light;
  - the vault layer behind the hero (arches);
  - the login door, plus the key turning and the crack of light;
  - error pages;
  - L1 24 px door crops in panel heads (preview, «Aller à…», notifications, search);
  - the rail tile and its sweep;
  - the favicon;
  - `ile-arch` at **both** journey step 6 and threshold B (adjacent);
  - the footer's closing arch-and-steps band;
  - the D-U7 arch-shaped reveal in the passage;
  - the diptych (two arcades);
  - the Istituzione image (a loggia of arches);
  - the portico video;
  - the phone login band.
- **Why major.** CD §1.4 law 5 and §21 say «the arch shape belongs to the door» and reject arch windows because they «spend the brand's strongest shape». The proposal spends it everywhere. Repeated, the door stops being an event and becomes a theme-park motif.
- **Fix.**
  - Keep the door where it is the brand: hero, login, error pages, lock-up, favicon.
  - Drop the vault layer (O21), the footer arch watermark and the D-U7 reveal.
  - Keep `ile-arch` only at threshold B (step 6 takes another glyph).
  - Use L2/L3 instead of L1 door crops in panel heads.
  - Keep at most **one** arcade context (the diptych) and give Istituzione a non-arched subject.
  - Add a test that counts arch occurrences per template.

### M3 — Effect density drifts to fintech/crypto

- **What.**
  - The gold light appears in: the arch light (hero, login), four route lights (loop), the passage light and its «ring of light» per station, the header-mark sweep, the rail-tile sweep, the JourneyRail head and its arrival ring, the «Bordo d'oro» rim sweep (twice on the home), and the L1 sweep and crack.
  - Every primary glows on hover (`--shadow-glow`).
  - Dark primaries are light-cyan gradients on navy.
  - Glass sits on the header, context bar, hero legend, login panel and micro-visual discs, on top of a mesh with 3 % grain.
  - The CD rejects liquid metal because «chrome metal is a 2025 catalogue signature». A gilt rim with a light sweep on a glossy dark button is the same signature in gold.
- **Why major.** Navy, cyan glow, gold streaks and glass is the visual vocabulary of crypto wallets and trading dashboards: the wrong register for a legal-institutional platform («institutional but modern»).
- **Fix.**
  - The gold light lives in **three** contexts only: the arch once after LCP (hero, login), the journey (public and console), and L1 during waits. Remove it from the CTA, the header mark and the rail tile.
  - «Bordo d'oro» becomes a static gilt hairline; hover darkens the fill and nothing travels.
  - Retire `--shadow-glow` and `--shadow-glow-dark`: hover darkens the fill by one step.
  - Glass only on sticky bars.
  - Station «rings of light» become solid 2 px strokes.

### M4 — The passage reads as a rising chart and as a hierarchy

- **What.** The route is «a cosine route from the south shore (Maroc) to the north (Vénétie)» (MOTION §7.1). In the frames (`scratch/journey/frames/home_ltr.png`) it is a cyan line climbing from bottom-left to top-right on navy, with glowing points as the light advances.
- **Why major.**
  - MOTION §7.2 forbids «a growth curve». This is one, and it looks like a price chart.
  - Placing Morocco low and Italy high draws an elevation between the two shores on a platform about cooperation between equals: a credibility and cultural-sensitivity risk that a Moroccan reader will notice.
- **Fix.**
  - Draw the route level, or as a symmetric arc with both shores at the same height.
  - Carry geography with the words (Maroc · Italie) and the two thresholds as vertical hairlines.
  - Station marks without halos.
  - Re-freeze LTR, RTL and reduced motion.

### M5 — The hero's travelling lights: WCAG 2.2.2, not prototyped, and not placeable

- **What.**
  - The four lights loop forever (28 s cycle, 7 s apart; CD §6 ruling 2, §9).
  - The video gets a 44 px pause toggle for WCAG 2.2.2; the hero loop gets none. Pausing off-screen is not a user mechanism.
  - UX_PUBLIC §7 required «every loop (hero light, videos) can be paused or lasts ≤ 5 s».
  - MOTION §13 item 9 says the hero lights are «specified and costed, not prototyped».
  - They are to be generated at build time as track × bob keyframes «sampled on each route». But `static/js/src/home.js` (header, l.21–23) re-measures and **rewrites** the four route paths at every width («this file replaces it with one measured at every width»), and again in RTL and on font or legend changes. Build-time keyframes will leave the drawn routes.
- **Fix.**
  - Play each light **once** after LCP, the whole sequence ≤ 5 s, then rest. This satisfies 2.2.2 and removes the only infinite loop on the home. If a loop is kept, add a visible pause control.
  - Generate the light's keyframes at runtime from the measured path (`getPointAtLength`, once per layout, after LCP), animated by WAAPI on `transform`/`opacity` (CSP-safe), or freeze the route geometry.
  - Prototype and trace before S1.

### M6 — Phones lose the menu on the case file and the wizard

- **What.** CD §8 (phone) removes the top-bar ≡ («no duplicate ≡») and lets the page action bar **replace** the bottom bar (MOBILE_UX §9.1). On the case file and «Ma situation», no control opens the navigation; only the top-left tile, which goes to the dashboard.
- **Why major.** It is a navigation dead-end on the two most task-critical screens, it breaks the consistent navigation of WCAG 3.2.3, and it weakens 2.4.5.
- **Fix.** When the action bar replaces the bottom bar, restore the top ≡ (57 + 61 = 118 px still fits the 120 px budget), or put a 44 px «Menu» at the action bar's start.

### M7 — «Mobile corrected» is true for phase 3 at nominal viewports only

- **What.**
  - CD §0.10 and §22.4: «hero ends at 96.0–96.5 %… door +81 % in area».
  - In the **interim** phase (what the public sees while G3 is closed), MOBILE_UX measured the door at **144 × 178** at 360 × 800 in Italian, smaller than today's 180 × 223 (l.193).
  - The interim hero reaches **101.4–108.3 %** at the estimated real-phone heights even with the 2 rem lever (l.206), and **119.5 %** at 320 × 568 with the primary 31 px under the fold (l.211).
  - The acceptance floor «door never below 136 px» allows a door smaller than today's.
- **Fix.**
  - Restate §0 and §22.4 with both phases.
  - Add the interim variants and the four estimated small viewports to the acceptance tests.
  - Give the interim title its own setting (Source Serif 4 at 28–32 px, one-line eyebrow).
  - Set the door floor at today's height (223 px at 390).

### M8 — The CSS budget is not grounded

- **What.**
  - CD §0.12 and the plan (§3.1) estimate CSS «+8–11 KB gz» with a ceiling of 50 KB gz.
  - MOTION §8.3 alone measured ≈ 8 KB gz for the loader, the sweep and the journey.
  - About 15 new component sheets still have to come (buttons, chip, field, card, overlays, chrome, workspace, identity, transitions, hero, the passage, the portico panel, notifications, the table, the Dépôt…).
  - The plan keeps V1–V4 sheets until **P4**. `components.css` alone is 3 099 lines and UI_INVENTORY §10.5 lists dead blocks.
  - The bundle is render-blocking on the LCP path (≈ +55 ms per 10 KB gz at 1.44 Mb/s).
- **Fix.**
  - Add a CI budget test per step on `dist/main.css` (gz), and report per-family deltas at each gate.
  - Move the dead-CSS deletion (`.plate`, `.home-hero`, `.lang-switcher`, `.zones`, `col-*`, `.text-*`…) into **F2**.
  - Keep console-only components (workspace, Dépôt, table, notification panel) out of `main.css`, in the console sheet.

### M9 — JS headroom is thin and the saving is deferred

- **What.** Public JS ≈ 40.5 / 45 KB gz (MOTION §8.3), with «≈ 4.5 KB of headroom for the rest of V5». That rest includes the public search combobox and its normalisation, the toast stack, `video.js`, the drawer rebuild, the portico panel's height morph and tabs. The `motion/mini` swap (−11.3 KB, −16.6 KB once `scroll()` leaves) is O34, phase P2/P3.
- **Fix.**
  - Do the `motion/mini` swap and move the two scroll-linked effects to native CSS **in F6**, before any S step.
  - Add a CI test that fails above 45 KB gz per page type.

### M10 — The loader moves the locked mark, and «unlocks» during legal waits

- **What.**
  - L1 turns the key, parts the two tricolour planes by 6 % and opens a crack of light (MOTION §6.2, §6.4).
  - The login stage performs the full unlock on submit.
  - BRAND_ASSETS §1: «Il marchio in V2 è fermo; se si muove, si muove una volta, all'ingresso».
  - DS V4 §1.8 and BRAND_ASSETS keep the tricolour to the mark and warn that it reads as «flag». Animating the planes draws the eye to exactly that.
  - Semantically, a door that unlocks while «Enregistrer et recalculer» recomputes a legal orientation, or while an assessment loads, suggests a favourable outcome («Aucun résultat administratif n'est promis»).
- **Fix.**
  - Planes never move.
  - L1 = the key's half-turns and the frame light only.
  - L1 never on outcome-bearing requests (situation recalculation, assessment, eligibility, scan verification): use L2/L3 there, listed in `loader.js` and tested.
  - O1 signed **and** BRAND_ASSETS §1 amended before F5.

### M11 — Status marks at 12 px

- **What.** The Piece Ledger draws one 12 px mark per piece (CD §12). Three registers are «filled disc + knocked-out micro-glyph»: conforme ✓, azione clock, rifiuto ×. COLOUR §10 states that rifiuto/blocco (protanopia, ΔE 0.030) and attesa/azione (deuteranopia, ΔE 0.015) are separated only by shape, pattern and edge. At 12 px on a 1× laptop those shapes are one or two device pixels. A row of up to 24 pips in eight hues also risks reading as a candy progress bar.
- **Fix.**
  - Pips ≥ 16 px, or a ledger grouped by register (mark + count).
  - Cap the hues in the ledger to three groups: to act / waiting / settled.
  - Run a CVD simulation on the rendered ledger at 1× DPR as a gate check.

### M12 — Derivation from the reference sites

- **What.** CAPTURES §3.1 documents agamieuromed.org, the promoter's own site:
  - «Every section starts “— EYEBROW” in gold tracked capitals, then a serif title, then sans copy. Bands alternate navy / cream / white»;
  - mega-menus of «link columns plus a featured image card with an italic serif description and an “Overview →” link»;
  - a mobile drawer with «a search field, icon rows (title + one-line subtitle), … a language grid».

  V5 adopts:
  - PX04 «gold hairline 24 × 1 + tracked eyebrow + serif title + sans lead», with alternating materials;
  - the portico panel «(a) sub-links with one-line descriptions · (b) a serif statement + the only arrow “Voir l'espace” · (c) the photograph»;
  - a drawer of «language row → 64 px rows (glyph + word + one-line description) → search field → primary».
- **Why major.** The hard constraint is «principles only — never copy layouts or elements». These are elements and a layout, and the source is recognisable to the same institutional audience.
- **Fix.**
  - Hold a side-by-side differentiation review at S1 and S2 (the V5 comps against `captures/ref_agami_*`), signed by the design reviewer.
  - Replace the gold-hairline eyebrow with an ILE device (a laguna 2 px tick or a three-step micro-mark, not gold).
  - Recompose the panel so the photograph is not a «featured card» beside a serif blurb (for example, the image as the panel's full-height inline-end field, with no text on it).

### M13 — Stock people, studio ubiquity, a named institution

- **What.**
  - The Persona door uses an identifiable man chosen because «his origin is ambiguous and international» (IMAGERY l.82) on the door that asks «Êtes-vous une personne ?» of prospective migrants. The placement casts him as an applicant whatever the caption, and the Pexels License gives no model release (IMAGERY §9.5).
  - Several picks come from the most-used Pexels studios (Mikhail Nilov ×3, cottonbro, Thirdman, Ron Lach), a recognisable «stock» look.
  - «Institutions» is a named, recognisable Padua monument («Palazzo della Ragione, à Padoue» in the alt), which a visitor can read as a partnership with that city.
- **Fix.**
  - Get a legal reading on identifiable people per door before curation.
  - Prefer non-identifiable framing for Persona (hands, back, at a distance).
  - Budget commissioned photography for the four doors, as already foreseen for the Forum.
  - Name no real building in alt text, or pick an unidentifiable civic interior.

### M14 — «Il gradino» on every surface

- **What.** It is the foot row of **every** portico panel, a home band, the drawer, the rails and the footer (CD §1.3 #6, §7, §20). On the home a visitor can meet it in the open panel, the band and the footer.
- **Why major.** UX_PUBLIC §2.1's own rule is «each recurrence adds a layer». Repeating a safety message three times turns it into noise and makes an institution sound alarmed.
- **Fix.** One full instance per page (the band on the home, the rail on inner pages); a one-line link in panels and the drawer; the footer entry stays.

### M15 — Inventory items with no V5 component

- **What.** UI_INVENTORY lists these live surfaces; the registry has no type and the plan only says «propagate»:
  - the Virtual Forum `community/*` (9 unstyled pages: rooms, calendar, initiatives, moderation);
  - long-form **prose** (news detail, legal documents, living sheets, pathway detail);
  - the **glossary** A–Z and term pages;
  - **living** topic and sheet cards (unstyled);
  - **account** profile, delete and the allauth manage pages (public shell);
  - the **outcome + sources** block of the pre-assessment (C28, legally sensitive);
  - the homes of **institution, university and professional** accounts (the «portal cards bridge» V4 rejected, C31, with no successor);
  - the jurisdiction bar (P23) and the pilot-flow diagram (P49): keep or retire?
  - the **back-office** (Unfold) theme, listed by the owner as a platform surface;
  - the «generic navigation card» of CD §14, which is not in the 113.
- **Fix.** Add registry types, or explicit «retire / keep as is» decisions:
  - PX24 Prose;
  - PX25 Glossary;
  - PX26 Topic card;
  - SW21 Outcome + sources;
  - SW22 Non-person home;
  - SC11 Account settings layout;
  - FM12 (B4);
  - an Unfold colour and font mapping.

  Schedule them in P1 and P2 with owners.

### M16 — The public signature may never be public

- **What.**
  - The home passage is the V5 coherence argument: the same seven stations in the portico and in the dossier (CD §11).
  - Publishing the seven labels needs legal D-U9.
  - The pilot section is **phase 3 only** today (`build_pilot` returns `None` while G3 is closed; MOTION §7.1).
  - Until both are resolved the public sees the fallback: the locked four-step sequence without thresholds.
- **Fix.** Design, prototype and gate the fallback as the **primary** public state on 8770. Make the S1 acceptance run on the interim server, and treat the seven-station version as the upgrade.

### M17 — A brand rule changed without a signature

- **What.** CD §1.4 law 1 and DS §4 add a tricolour filet (12 × 2 px) beside the institutional notice's title (COLOUR D7). DS V4 §1.8 says «Il tricolore non esiste altrove», and BRAND_ASSETS says the mark is the one place green and red coexist. COLOUR listed it as a decision (D7); CD §24 does not.
- **Fix.** Add it to §24 as an owner decision (recommendation: drop it; the navy glyph and the gold rule already say «institutional»).

### M18 — The read-only phase was breached (disclosed)

- **What.** CD §25 and MOTION §13.13 record three things:
  - a Playwright session created `.playwright-mcp/` inside the repository (now gone);
  - the 26 September captures drove the QA Chrome and deleted its `sessionid` cookie;
  - the mobile lane added 7 session rows to the local `ile_qa` database.

  Several reports still open with «the repository was read and not modified».
- **Fix.**
  - Re-mint the QA sessions and delete (or confirm) the 7 rows.
  - Set every browser tool's output directory outside the repository.
  - For every lane, add a before/after check (`git status --ignored` on the repo, plus a session-table count) to the protocol.
  - Correct the opening lines of the affected reports.

### M19 — «One L1 per view» is not enforceable per template

- **What.** The stress runs measured 51–67 ms tasks with several L1 at once (MOTION §6.14). DS test #5 checks «one L1 per template render». At runtime, several surfaces can be open at once, each with its own L1: the preview drawer, the notification panel, «Aller à…» and the search results.
- **Fix.** Make L1 a singleton in `loader.js`: a second L1 request while one runs is served as L2/L3. Add a unit test and a gate trace with all async regions open.

---

## 4. Minor

| ID | Issue | Fix |
|---|---|---|
| m1 | `ile-steps` («Mon parcours»: lines of 6/11/16) is a near-twin of `menu` (≡) and of Lucide `list-filter`; they are hard to tell apart at 14–16 px in `council/icons/specimen-render.png` | Draw it as a stair profile (risers and treads), or keep it off the rail |
| m2 | Adjacent repetition on the journey: `ile-arch` at threshold B **and** step 6; `compass` for steps 1 **and** 2 | Threshold B = hairline only; a distinct glyph for step 2 |
| m3 | The DS cites a 4 px rhythm, yet specifies 15/22 (portico links) and 11/14 (compact rail labels; 11 px Arabic is illegible). It says «44 px minimum for every control» next to 36 px segmented tracks and menu rows and 24 px filter chips | 15/24; 12/16 (13/20 under `:lang(ar)`); state the real target rule (WCAG 24 px, 44 px for primary targets) |
| m4 | «Audience accents never on paper» (CD §10) vs route-colour nodes in the paper «Quatre accès» phone list (MOBILE_UX §3.3); Persona's accent equals the interactive accent | Glyph in ink on paper; shift Persona off `#7fd1d8` (O19) |
| m5 | «Glass never on content» (CD §3) vs glass-dark micro-visual discs on photographs (door cards, panels, landings); a full-screen static 6 px blur behind sheets is costly on low-end Android | Solid notte-900 disc at .72, no `backdrop-filter`; no scrim blur ≤ 40rem |
| m6 | Council specimens show patterns V5 forbids: legend ordinals 01–04, «3/7 étapes», «14 j restants», a MONTANT column, «Validé», named patronage with an invented venue | Stamp specimens «non-normative» or purge them before they become references |
| m7 | «72 adapted from 21st.dev» counts native select, checkbox rows, switch, breadcrumb and pagination (the Django algorithm) as 21st-sourced | Relabel: «reviewed on 21st · native pattern» |
| m8 | Portico-panel photographs are fetched on first hover, a visible pop-in on slow 4G; a 32 % page scrim appears on a mere hover | Idle, low-priority prefetch ≥ 80rem after LCP, fade-in on load; scrim only on click/keyboard open |
| m9 | The preview drawer's `pushState`: Back behaviour and focus return are unspecified | `popstate` closes the drawer and returns focus to the row title |
| m10 | The wordmark subset's fallback is «Newsreader», which V5 retires; `.rail__wordmark` reads `--f-serif`, which `body.console` re-points to the sans | Declare `unicode-range`; point both selectors at `--f-wordmark` in F1; add the computed-font test of M1 |
| m11 | «Moved in the template» (hero body and legend on phones only) implies breakpoint-duplicated markup; not specified against the locked-copy equality tests and duplicate ids | Specify: render twice with media-query `display: none`, no duplicate ids, the equality test counts one instance |
| m12 | Zellige, hanging lanterns and a Padua landmark are mild cultural or tourist signifiers | Extend the planned Moroccan-reader review from type to imagery |
| m13 | «La soglia» names the concept, the journey and the navigation thread («S Soglia»); 15+ Italian code names | One glossary; neutral code names (`journey`, `nav-thread`) |
| m14 | View Transitions measured only at 180 ms (+90 ms, 10 ms margin); 120 ms not measured | Already gated; keep it off by default until the 6 + 6 re-run |
| m15 | The vault layer is decorative, adds arches (M2) and would become the LCP element | Drop it instead of making it conditional |
| m16 | OFL texts for IBM Plex Mono and the Newsreader wordmark subset are missing from `council/typography/fonts/` | Add them before F1 (licence record) |
| m17 | Vazirmatn's letterforms come from a Persian-script family, for a Moroccan audience | Keep the Moroccan-reader review blocking for `/ar/`; keep Noto Sans Arabic as the fallback candidate |
| m18 | «`generate` never called» rests on each lane's statement; `get_usage` reports entitlement, not usage | Record it as a declaration, not a verification (21ST_SEARCH_LOG §4 already hedges) |

---

## 5. Internal contradictions in the finals (the «many authors» symptom)

| # | Says | And also says |
|---|---|---|
| 1 | No ticks on stations (CD §11) | Done node = lapis fill + white glyph, drawn as a check (DS §4, COLOUR specimen) |
| 2 | The word stays «Valide» (CD §12) | Chips labelled «Validé» (colour specimens) |
| 3 | The arch belongs to the door (CD §1.4 law 5, §21) | ≈ 15 arch occurrences (M2) |
| 4 | Glass never on content (CD §3) | Glass discs on photographs (DS §3.4, CD §10) |
| 5 | Audience accents never on paper (CD §10) | Route-colour nodes on paper rows (MOBILE_UX §3.3, adopted by CD §19) |
| 6 | 44 px minimum for every control (DS §6) | 36 px segmented tracks and menu rows, 24 px filter chips (DS §3.6, §10.2) |
| 7 | Every line-height is a multiple of 4 px (DS §5) | 15/22, 11/14 (CD §7, §8; DS §10.5) |
| 8 | The tricolour lives in the mark (V4 DS §1.8, BRAND_ASSETS) | A tricolour filet on the notice (CD §1.4, DS §4), missing from §24 |
| 9 | No growth curve (MOTION §7.2) | A rising route (MOTION §7.1, frames) |
| 10 | Every loop can be paused or lasts ≤ 5 s (UX_PUBLIC §7) | An infinite hero loop with no control (CD §6, §9) |

---

## 6. Hard constraints — status

| Constraint | Status | Evidence / residual risk |
|---|---|---|
| CSP `script-src 'self'`, `style-src 'self'`, no inline | **PASS (spec)** | `config/settings/base.py` l.348–361; no `style=""`, CSSOM writes and WAAPI only, keyframes generated at build; council specimens use inline styles but are not product |
| Everything self-hosted at runtime | **PASS (spec)** | Fonts and images downloaded; 21st previews never shipped; `media-src` falls back to `default-src 'self'` |
| No Next.js/React rewrite; React only if justified | **PASS** | Route C = 0 on six stated criteria (21ST_COMPONENT_MATRIX §5) |
| 21st: no `generate` / `iterate_generation` | **PASS (declared)** | 0 in every lane's report; not independently verifiable (m18) |
| Wordmark font not removed | **PASS in intent** | Subset delivery (O6 to sign); outlined SVG rejected; M1 and m10 must be fixed so the name renders in it everywhere |
| Editorial image rules (fetch_images, IMAGE_LICENSES) | **AT RISK — B2** | F15 «porte/soglie, griglie/cancelli» vs the arcade/step/vault concept; 14 full-resolution checks still pending |
| Licence and author recorded | **PENDING** | Authors listed for all 17 + 3; nothing curated yet |
| LCP ≤ 2.5 s · CLS ≤ 0.10 · INP ≤ 200 ms (slow 4G + CPU ×4) | **PLAUSIBLE, UNPROVEN** | Baseline 1.44–1.82 s (`ac92427`); risks M5, M8, M9, M19; hero lights not prototyped |
| No avoidable long task > 50 ms | **AT RISK** | Multi-L1 stress 51–67 ms (M19); runtime light generation must stay off the critical path (M5) |
| WCAG 2.2 AA, keyboard, reduced motion | **AT RISK** | 2.2.2 (M5), 3.2.3 (M6), small-size legibility (M11, m3); reduced-motion states are complete |
| RTL Arabic | **MOSTLY SPECIFIED** | Gaps: hero light direction on re-anchored routes (M5), 11 px Arabic rail labels (m3), Arabic reader review pending |
| Reference sites: principles only | **AT RISK — M12** | Section grammar, panel and drawer anatomy |
| Repository read-only in this phase | **BREACHED, disclosed** | M18; repo clean at `c9a58d8` now |

---

## 7. What holds up — keep it

- **Law 2.2 and its frame test.** It is what stopped V4's regressions; V5 extends it (restored-scroll test, `motion-armed` on fresh navigations only).
- **The composited sweep** measured against a 300 ms main-thread block (27/27 positions against 2/13), and the literal-easing trap found and tested.
- **The type diet:** 356 → 74 KB on the home, ≈ 509 → 82 KB in Arabic, with production-shaped files on disk.
- **Colour proven by script** (363 pairs), green retired, and state carried by word + mark + pattern + edge. Only the conforme hue must change (B1).
- **The truth track (T1–T9)** before any platform gate. That is the right order.
- **Honest limitations** in every report and in CD §25, including the process breaches.

---

## 8. Conditions for signature (in order)

1. **B1:** reverse the default to achromatic conforme and no checks; purge «Validé»; legal signs in writing if lapis is still wanted.
2. **B2:** the owner rules on F15's scope; the image shortlist is re-run under the ruling; a fallback set exists.
3. **B4:** add FM12 and step S1b.
4. **M1, M2, M3, M4, M14:** apply the fixes above to the specification (motif and effect budget, one typeface for the name, a level route).
5. **B3:** build the visual-proof comps with the amended specification; the owner reviews the pictures.
6. **M5, M6, M7:** amend the hero-light, phone-navigation and mobile-claim sections; add the interim and small-viewport cases to the acceptance tests.
7. **M8, M9, M19:** add CI budget tests (CSS gz, JS gz per page type, L1 singleton); pull the `motion/mini` swap and the dead-CSS deletion into phase F.
8. **M10, M12, M13, M15, M16, M17, M18:** decisions recorded in CD §24; missing registry types added; process fixes applied.

Only then do O1–O53 go to the owner.

---

## 9. What this review did not do, and why

- **No browser run, no trace, no Lighthouse.** Every performance judgement here reads the council's measurements or the code. The claims I call unproven (hero lights, CSS growth, runtime L1 count) need the gate's measurements.
- **Photographs:** I looked at no Pexels image. The B2 and M13 judgements rest on IMAGERY's own descriptions and on the project's written rules and precedents.
- **Visuals examined:** seven council images only (listed in the method). The four-language captures and the 21st previews were not re-viewed.
- **Not re-run:** `verify_tokens.py` (contrast), the font builds, the Lucide name check. I recounted the registry only.
- **No 21st.dev call.** The claim that `generate` was never called is recorded as declared by each lane.
- **Legal readings are not mine.** B1, B2 (scope of F15), M13 (releases, implied endorsement) and M16 (D-U9) go to the owner and legal. I state the rule that exists in the repository and where the proposal departs from it.
