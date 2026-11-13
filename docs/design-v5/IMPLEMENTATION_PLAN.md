# IMPLEMENTATION PLAN — V5 «La soglia»

**Italy Legal Entry™ · Executive Creative Director · 27 September 2026 · status PROPOSED — revised after the red team** (`RED_TEAM.md`; every change is traced in `CREATIVE_DIRECTION_V5.md` §26). Ordered, safe, measurable. **It starts with phase 0** — the rulings the pictures need, then composed screens the owner reviews (gate 0) — and the build phases start only when the owner has signed `CREATIVE_DIRECTION_V5.md` (the decisions of its §24 that block each phase are listed in §1 below). Until then the repository stays read-only.

**Order, as the owner asked:** foundation first (fonts, tokens, icons, buttons/badges, loader, motion), then the flagship surfaces in the owner's order — homepage, navbar/mega-menu, loader, login, app shell/sidebar, person dashboard, documents, case file, company area, academy, forum — then propagation. A parallel **truth track** fixes what no design can fix (contradictory next actions, a case page that says nothing is asked while three pieces are, a primary CTA that leaves the console) because the platform gates cannot be judged on screens that tell the person two different things.

---

## 0. Principles

1. **One phase, one branch; one component family per commit; one measurement per commit.** Branches `v5/f1-fonts`, `v5/f2-tokens`, … merged only after their gate PASS. Nothing in this plan deploys to production.
2. **Re-measure after every change** — every page a shared sheet touches, not only the page being worked on (project memory: two regressions reached a commit from un-measured one-line corrections). Chips appear on 65 sites in 33 templates; `buttons.css` on 76 templates; the tokens on everything.
3. **Visual defects are often deliberate** — before «fixing» a visual oddity, read the comments in `static/css/v4/tokens.css` and the design documents (project memory: three of three obvious repairs were wrong). The council marked the deliberate ones (`UX_PUBLIC` §2.4: D7, D8, D12).
4. **Tests run in isolated lanes** — concurrent pytest runs deadlock on `test_ile`; set `TEST_DATABASE_URL` per lane (project memory).
5. **Servers and browsers.** Performance on **8772** (gzip); phase-3-only surfaces (the pilot, the passage) on **8771** (`ile_qa`); interim checks on **8770**. The QA Chrome (9222) belongs to the capture role; every probe runs in its own headless profile (the motion lane's 26 September captures drove the QA tab and deleted its session cookie — not to be repeated). Sessions are minted server-side (`scripts/qa_chrome_signin.py` method); no password is ever typed, no form submitted by a probe. **After the council's breaches** (`RED_TEAM` M18): every browser tool writes its output outside the repository (Playwright's output directory included); every lane runs a before/after check — `GIT_OPTIONAL_LOCKS=0 git status --porcelain --ignored` on the repository and a count of the session table in `ile_qa` — and reports both numbers.
6. **Nothing is removed before its replacement passes — and nothing replaced lingers.** V4 names stay as aliases for one release; a V3/V4 component sheet leaves the bundle as soon as the step that replaces it passes its gate; the dead CSS (no markup uses it) goes in F2; V1/V2 sheets are deleted in phase P, file by file, after a grep proves no markup uses them (revised after `RED_TEAM` M8).
7. **Every gate has four independent reviews** — design, UX, motion, performance — plus an accessibility/RTL pass, by reviewers who did not implement the step, each new defect re-measured by a sceptic before it counts (the gate-A round-5 method). Scores on the existing `docs/design-v4/GATE_SCORECARD_TEMPLATE.md`; **PASS** requires no BLOCK finding and ≥ 4/5 on Premium feel, Coherence, Motion, UX, Mobile, Accessibility and Performance.

---

## 1. Phase −1 — the owner's signatures that unblock each phase

| Phase | Blocking decisions (`CREATIVE_DIRECTION_V5.md` §24) |
|---|---|
| **0 «La prova»** | **O54** the scope of F15 · **O55** identifiable people · **O14** VALIDE (default ink) · **O57** the tricolour filet · **O66** the process fixes — then **O59**, the owner's review of the composed screens, which comes before every row below |
| F1 fonts | O9 pairing A/B · O10 Arabic faces (after one Moroccan reader review of `council/typography/specimen.html`, blocking) · O6 wordmark delivery, every rendering of the name · O7 wordmark breakpoint · O41 Latin digits in Arabic |
| F2 tokens | O13 lighter console · O16 retirements · O64 the console bundle and the dead-CSS deletion |
| F3 icons | Q5 of the icon map (ISC donor geometry) · Q3 Guichet glyph |
| F4 primitives | O14 VALIDE in ink (already signed in phase 0) · O15 registers + re-mappings (domain owner) · O17 every chip has its mark · O31 busy label kept · O51 empty-state doctrine · O57 no filet · O61 the paper-plate primary, no glow |
| F5 loader | **O1** the mark's key turns once, at the entrance · O32 the 10-second copy in four languages |
| F6 motion | O28 arch light · O29 route lights once · O30 public View Transitions (off by default) · O33 `motion-armed` · **O34** the `motion/mini` swap and native scroll effects · O64 the CI budgets |
| S1 home | O5, O8, O11, O19, O20, O22, O23, O38, O39, O40, O45, O46 (legal: public use of `JOURNEY_STEPS`), O54 (already signed), O56, O60 — O4 and O21 are withdrawn |
| S1b public questionnaire | O58 |
| S2 nav | O35 IA · O36 CMS fields · O37 search build step |
| S4 login | O1 · O24 accent photo · O44 reassurance line |
| S5 shell | O2 rail tile (still) · O43 short labels · O63 Menu in the action bar |
| S6–S9 platform | O3, O18, O47, **O48–O52** (product/engineering: unified next action, one list, orientation in the console, NowPanel primary, intent transitions), O62 the ledger |
| S10–S11 | O12, O25, O26, O42 |
| P1–P2 | O65 the new registry types and their owners |

---

## 1b. Phase 0 — «La prova»: the rulings, the composed screens, the process fixes (≈ 6–8 days + the owner's review)

The red team's third blocking finding (`RED_TEAM` B3): the owner judged V4 on screens and was asked to sign V5 on ≈ 400 KB of prose. Phase 0 makes the owner sign pictures, then decisions.

1. **The rulings the pictures need** — O54 (the scope of F15, written into `docs/IMAGE_LICENSES.md` §1 by whoever holds the repository after the signature), O55 (a legal reading on identifiable people), O14 (VALIDE in ink), O57 (no filet).
2. **The photographs** — the shortlist re-run under the O54 ruling; the full-resolution checks of `ASSET_USAGE_MATRIX.md` §6 for the two or three photographs the comps use (the door, a door image, the diptych or «Lo stesso gesto»).
3. **The comps** — static, CSP-clean HTML (no inline style or script; everything self-hosted), built **outside the repository** in `C:/tmp/ile_v5_council/proof/`, with the V5 fonts (`council/typography/fonts/`) and the amended tokens (`DESIGN_SYSTEM_V5.md` §2–§4): the home's first three screens at 1440 × 900 and 390 × 844, in fr and ar, interim **and** phase 3 (the orientation passage is the interim's); the login; a mid-case dashboard; «Mes pièces» with the ledger. Also the normative chip board (eight registers, `conforme` in ink) and the ledger at 1× DPR with a colour-vision-deficiency simulation; the passage frozen from the **level** geometry in LTR, RTL and reduced motion; the hero's first breath and the login's key frozen frame by frame (0 / 300 / 900 / 1500 / 2400 / 3300 ms). The council's specimens stay in `council/` as non-normative history.
4. **Two prototypes** the red team asked for before S1: the hero's route lights with keyframes sampled at runtime from the live paths (one trace under CPU ×4: the sampling must not appear as a long task), and the interim phone hero with its own title setting and the door floor at today's size (the extended acceptance tests of CD §19, measured on 8770 with CSS injected, as `MOBILE_UX` did).
5. **The reviews on the pictures** — the design reviewer's side-by-side against `captures/ref_agami_*` (six criteria, CD §7); a check of the red team's risks that only pictures reveal (M1 the name, M2 the arch count, M3 the effects, M4 the route, M14 the anti-fraud step); the owner signs the pictures (O59), then §24.
6. **The process fixes** (O66) — the QA sessions re-minted server-side; the seven session rows the mobile lane added to `ile_qa` deleted or kept knowingly; the memory plugin's `.remember/` folder inside the repository accepted or moved; the before/after check of §0.5 in every lane from now on.

**Gate 0 passes** when the owner has signed the pictures. Nothing in phase F starts before.

---

## 2. Track T — truth and visible defects (parallel to F; no visual change; blocks S5–S9 gates)

| # | Fix | Where | Acceptance |
|---|---|---|---|
| T1 | **One next action** computed over all open obligations (blocking outcome → overdue item, checklist *or* requirement → due item → open item the person must act on → orientation not done → state fallback), one presenter feeding the dashboard, the case and the documents primary | `apps/cases/services.py next_action`, `apps/portal/services.py` | on `EE167596D4` the three screens name the same action; unit tests per precedence rung |
| T2 | **One «ce qui est demandé»**: the case lists checklist items *and* requirements (or links «3 pièces demandées pour ce dossier → Voir les pièces»); minimum: never «Aucune pièce n'est encore demandée» when requirements exist | `cases/detail.html`, presenter | the contradiction test on the QA fixtures |
| T3 | **Orientation inside the console** for signed-in people (the orientation templates choose `portal/base_portal.html` when authenticated); each questionnaire names the other in one sentence | `orientation/*.html`, views | the dashboard's primary never leaves the console shell |
| T4 | Forum governance «unavailable» rendered inside the console when the portal is on | `forum/governance/unavailable.html` | captured in the console shell |
| T5 | Test that every console base overriding `extra_head` keeps the console sheets (the Guichet regression fixed in `c9a58d8`) | 20 templates | `test_extra_head_bases.py` green |
| T6 | Permission check of the person-facing «Faire évoluer l'état du dossier» `<select>`: a bug (remove) or a feature (intent buttons in S8) | `cases/views.py`, `transitions_available()` | decision recorded |
| T7 | Public defects read in code, to confirm in a browser before fixing: D1 «ATTENTIO / N AUX FRAUDES» (size from a container query), D2 doubled «Comment ça marche» (visually hidden heading), D3 titles smaller than their descriptions, D4 «VÉNÉTIE» over station 05 (`justify-self: end` at every width), D9 «Fermer» while the drawer is open, D10 `lang="en"` on English legal titles and the console footer's «Privacy Policy», D11 two panel entries to one URL, D6 `lang="fr" dir="ltr"` on the French fragment in the Arabic hero | the templates and sheets named in `UX_PUBLIC` §2.4 | each re-captured at 1440 / 390 in fr and ar; no CLS change |
| T8 | Markup defects from the inventory: `.notice--warn` has no CSS (the defined modifier is `--warning`); the allauth alert always shows `info`; forum gallery `<img>` without dimensions; forum `<video>` without captions; the admin legal-rule preview's inline `style` (CSP) | `UI_INVENTORY` §10.6 | each verified in a browser first |
| T9 | «Ma situation»: the counter matches the stepper («sur 7» / «1 / 8» — owner copy) | `portal/situation.html` | captured |

T-fixes follow the same «re-measure every page the change touches» rule. The deliberate items (D7 the lower-case interim fragment, D8 the exits, D12 the zig-zag) are **not** fixed in T: V5 changes them by design in S1.

---

## 3. The gate protocol — applied to every step below

### 3.1 Measurements (performance reviewer; scripts extend `scratch/capture/p2_loading.py`, `scratch/probe2/*`, `scratch/mobile/*`)

| Measure | How | Budget / pass |
|---|---|---|
| LCP | 8772, slow 4G (562.5 ms RTT, 1.6 Mb/s down) + CPU ×4, cache cleared, **3 runs, median**, 1440 × 900 and 390 × 844 | **≤ 2.5 s** (owner) — V5 target **≤ 2.2 s** to keep margin (today 1.44–1.82 s) |
| CLS | same runs + a scroll pass | **≤ 0.10** — V5 target ≤ 0.05; font swap ≈ 0 with metric-matched fallbacks |
| INP | busy primary, rail toggle, drawer open, mega-menu open, filter, upload start — CPU ×4 | **≤ 200 ms** |
| Long tasks | trace during load, each loader state, a View Transition navigation, the hero light, the journey scroll | **0 tasks > 50 ms attributable to V5 code**; 0 long animation frames |
| Compositing | trace category `blink.animations` | **0 `compositeFailed`** for anything infinite, scroll-linked or loading; the 300 ms **block test**: a loader keeps moving during a busy main thread |
| Law 2.2 (nothing painted is taken back) | frame capture at fp + 0 / 250 / 600 / 1200 / 2500 ms, per element | **0** visible → hidden transitions, **0** transform changes on painted content |
| Restored scroll | reload at a mid-page scroll, back/forward, hash arrival | **0** in-viewport element at opacity 0 after first paint |
| Weight | built `dist/` — **held by CI tests** (`test_css_budget.py`, `test_js_budget.py`), with the per-family delta reported at every gate | public JS **≤ 45 KB gz per page type** (≈ 36.0 today, measured; ≈ 19.4 after the F6 swap, from the probes; ≈ 25–28 expected on the home with V5, estimated) · fonts per page **≤ 100 KB** (A: 29–82) · **`dist/main.css` ≤ 45 KB gz**, red line 50 (36.0 today, measured; 29.7 without the console-only sheets, measured in this revision; ≈ 38–44 expected after phase F — an estimate: the net of the new component sheets against the ones they replace is not measured) · console-only CSS in `dist/console.css` · images per `ASSET_USAGE_MATRIX` §8 · sprite ≤ its measured ceiling |
| Screenshots | after `document.fonts.ready` (a capture before the fonts arrive shows invisible text in the block period) | — |
| Sampling | per-frame states read after every rAF callback (a `ResizeObserver` tick) or from screencast pixels — never a rAF-first sampler (it reports frames that were never painted) | — |

### 3.2 Chrome review checks (design and UX reviewers; the visible QA Chrome or a headed run)

Every page the step touches, at **1440 × 900, 1280 × 800, 1366 × 768 at 1× (the owner's laptop class), 768 × 1024, 390 × 844, 360 × 800**, in **fr and ar** (it and en on the home and the login): full-page capture; first viewport; the states the step adds (hover, focus, pressed, disabled, busy, error, empty, loading at 400 ms / 1 s / 10 s); **reduced motion** (`Emulation.setEmulatedMedia`); **forced colours**; **no JavaScript**; **200 % zoom** and the WCAG 1.4.12 text-spacing override; a **keyboard-only walk** (focus order, focus visible and never obscured under sticky bars — 2.4.11); an **axe** run; the **RTL** pass (direction mirrors, the mark/door/photographs/key never do).

### 3.3 The four independent reviews (+ accessibility / RTL)

| Review | Asks | Evidence required |
|---|---|---|
| **Design** | does it look like one team? tokens only (no raw hex, no author look), the serif scope and the one drawing of the name, the icon hand, one image one context, the signatures used where they belong and nowhere else (the arch allow-list, the three gold contexts, one «gradino» per page); **for public chrome, the differentiation review against the reference site** | before/after captures; token grep; a side-by-side with the gate-0 comps and with `captures/ref_agami_*` |
| **UX** | the task works; one primary per screen next to its reason; copy in words; the locked copy verbatim; IA; mobile targets (`MOBILE_UX` §10) | task walk-throughs in fr and ar; copy diff; the mobile acceptance tests |
| **Motion** | the five laws; the function comment on every animation; reduced-motion still state; RTL direction; one live object | frame tests, traces, RM and RTL captures |
| **Performance** | the budgets of §3.1 | the three-run medians and traces, attached to the gate file |
| **Accessibility / RTL** | WCAG 2.2 AA: contrast (tokens verified + the rendered page), focus, targets (24 px floor, 44 px for primary and touch targets), 1.4.13, 2.2.2 (nothing auto-moving beyond 5 s without a pause control), 3.2.3 (the Menu control present on every phone screen), 3.1.2 (language of parts), forced colours, Arabic typography, a CVD simulation of rendered status marks at 1× | axe, keyboard walk, forced-colours and `/ar/` captures |

Gate files go under `docs/design-v5/gates/` like V4's; **propagation (phase P) of a family starts only after its flagship gate PASS**.

---

## 4. Phase F — foundation

Each step: scope → files → tests → Chrome review checks → performance checks → reviews. Rough effort is an ECD estimate for one developer, not a measurement.

### F1 — Fonts and type tokens (≈ 2–3 days)

- **Scope.** Build the eight woff2 files (pinned `google/fonts` commits; fontTools `instancer` + `subset`, hinting dropped, OFL name IDs kept) with `scripts/fetch_fonts.py --build`; `static/css/v5/fonts.css` with the metric-matched fallback faces (Windows values computed; **Mac and Android values computed before merge**); `--f-*` / `--t-*` / `--u-*` tokens (`DESIGN_SYSTEM_V5.md` §3.3) with the V4 aliases re-pointed; preloads in `base.html` (Host everywhere; Source Serif 4 roman on public; Vazirmatn + Markazi on `/ar/`); the «ILE Wordmark» face (11 code points, `unicode-range`) on **every rendering of the name** — `.lock__wm`, `.rail__wordmark`, the `{% brand %}` classes (hero H1 as the engraved line, project H1, footer legal line), never through `--f-serif` — and the `opsz` 36 instance only if gate 0 asked for it; the OFL texts shipped with the files (Newsreader and IBM Plex Mono added to `council/typography/fonts/` in the revision); the lock-up breakpoint 23 → 21.5 rem; `font-synthesis: none`; the Fira strings deleted from `tokens.css`; the French-spacing content rule.
- **Tests.** `test_fonts_build.py` (the wordmark file holds exactly its 11 code points), `test_serif_scope.py`, `test_brand_face.py` (the computed face of every rendering of the name, public / console / `/ar/`), `test_french_spacing.py`; `test_v4_tokens.py` / `test_design_docs.py` family strings updated.
- **Chrome checks.** Every public template and every console template re-captured (fonts touch everything); the hero H1 in the wordmark face at 32–40 px (and option b if the owner chose it); the 13 px console meta on the 1× 1366 × 768 laptop (lever `--u-small: 13.5px`); Arabic pages with the Moroccan reviewer's notes applied; the wordmark pixel-identical at 20 / 14 px; 360 px header with the wordmark visible and no horizontal scroll.
- **Performance.** Font bytes per page (home ≤ 74 KB, console ≤ 30, `/ar/` ≤ 82); LCP mobile (the lead is a text node) and desktop; CLS contribution of the swap ≈ 0.
- **Reviews.** Design (type fidelity, the two-serif page), accessibility (1.4.12, Arabic), performance.

### F2 — Colour and material tokens (≈ 2 days + the 42-site review)

- **Scope.** `static/css/v5/tokens.css` (primitives, semantic, component — `DESIGN_SYSTEM_V5.md` §2–§4) and `v5/aliases.css`; the V4 names aliased to identical hex; the console shell one step lighter (`body.console`); retirements shimmed (`--err-*`, `--pending-*`, `--seal-*`, `--state-*`), `--ok-*` deleted; **each of the 42 sites of the red «accent» shim reviewed** (a link → `--accent-text`; an order rule → `--line-structure`); the `--grad-photo-dark` text use replaced by `--scrim-photo-aa` or a plate; **`conforme` re-pointed to ink** (carta-100 body, inchiostro-400 edge, inchiostro-900 mark and word); **the console-only sheets moved out of `main.css`** into `dist/console.css` (workspace, wizard; later the Dépôt, the table, the notification panel, the console journey rail); **the dead CSS deleted** — `.plate`, `.home-hero`, `.lang-switcher`, `.language-switcher`, `.zones`, `.entrances`, `.portal-columns`, `.portal-table`, `col-*`, `.text-*`, the dead `.t-*` — each after a grep proves no markup uses it (moved here from P4: `RED_TEAM` M8).
- **Tests.** `test_v5_tokens.py` (the pairs of `verify_tokens.py` in pytest form, **re-run on the amended file** — the `conforme` row changed after the red team — and recomputed from the built CSS); `test_v5_layers.py`; `test_css_budget.py`; the existing «no register painted with the verdict green or the accent» test and `test_chips_registry.py` kept unchanged.
- **Chrome checks.** Public pages unchanged except the retired colours (before/after diff: the aliases must produce identical pixels where V4 measured); the console on the lighter shell (dashboard, documents, case, company, situation) — rows, chips and previews on white, night chrome unchanged; forced colours.
- **Performance.** `dist/main.css` before and after (≈ −6.4 KB gz for the console-only sheets, measured on today's bundle; the dead CSS's weight measured when deleted; tokens +≈ 2.7 KB gz); no runtime `color-mix()` for states.
- **Reviews.** Design, accessibility (contrast on the rendered pages, not only the tokens).

### F3 — Icons (≈ 3–4 days + ½ day design review — the icon lane's estimate)

- **Scope.** `apps/core/icons.py` registry; `static/icons/src/*.svg` (31 ILE kept, 4 identity, 8 status marks, `arrow-start`, ≈ 65 Lucide geometries without their root attributes, tone paths on the concept tier); `scripts/build_icons.py`; the CSS treatment (stroke per size, square caps, miter); `docs/design-v5/ICON_LICENSES.md`; the site migration **public first** (nav, footer, contact, anti-fraud entries, ecosystem bullets removed, pagination), **then console** (rail, rows, menus, account); `link-arrow` glyphs removed from secondary links; the favicon on `ile-arch`; the ≈ 12 console shell symbols rendered in the document.
- **Tests.** `test_icons.py` (10 assertions, `ICON_SEMANTIC_MAP.md` §8 — two added after the red team: no check glyph on a state, the arch only in its allow-list).
- **Chrome checks.** A specimen page at 14 / 16 / 20 / 24 / 48 px on paper and night (square caps must not spike on `handshake`, `phone`, `quote`); 0 empty `<use>` (the `getBBox` gate of `docs/qa/design/capture.py`); the `concierge-bell` / `bell` side-by-side (Q3); the rail painting with its glyphs at fp + 250 ms; RTL flip list.
- **Performance.** Sprite size (set the test ceiling from the build); the console first paint with and without the inlined shell symbols vs a sprite preload.
- **Reviews.** Design (one hand), accessibility (names of icon-only controls), UX (the rail readable).

### F4 — Buttons, chips, counts, notices, fields (≈ 4–5 days)

- **Scope.** `v5/buttons.css` (the V4 matrix cleaned and **flattened** — flat fills, no gradient, no inner light, `--shadow-glow` retired; **the paper plate** as the primary on night; stacked-faces cell, press/release spring, unused variants retired, the **signature «Bordo d'oro»** with its **static** gilt edge — nothing travels); `v5/chip.css` + `apps/core/chips.py` (registers `esame`, `blocco`, the re-mappings, `STATE_GLYPHS`, marks rendered in `.chip__g`, the 3-notch micro-meter replacing the V3 gutter and gauge); `.count`; the seal restricted to authority acts; deadline ladder; notices V5 (5 kinds, the institutional one without a tricolour filet); **`conforme` in ink with the plain filled disc, and no check on any state (the check rule)**; fields (state model, add-ons, textarea counter, **DateField**), checkbox/radio/switch rows, OptionCard, error summary; EmptyLine / EmptyState V5.
- **Tests.** `test_chips.py` (with the red team's extension: `conforme` chroma ≤ 0.03, `STATUS["conforme"]` not a check, no check symbol in chips, journey nodes or the ledger); `test_chips_registry.py` unchanged; button-state and chip snapshot tests in `/_design/`.
- **Chrome checks.** A chip board: eight registers × paper / white console sheet / night / forced colours / greyscale (the ladder); the **65 chip sites in 33 templates** re-probed; every button variant × state (D/H/F/P/X/L) on paper and night; the signature CTA at rest, hovered and focused (nothing travels); fields in fr and ar with errors.
- **Performance.** INP on a busy primary.
- **Reviews.** Design, UX (words of the chips, «Valide»), accessibility (one announcement per region; never colour alone), motion (state change).

### F5 — The loader and the loading states (≈ 4 days — the prototype exists)

- **Scope** (reduced after `RED_TEAM` M2, M3, M10, M19). `v5/loader.css` from `scratch/loader/loader.css` (literal keyframe easings) + the composited sweep generated for **one** geometry — the entrance stage's door frame — by a script in `scripts/` run by `build:css`; **L1 plays one cycle and rests, the tricolour planes never move, no crack of light**; `static/js/src/loader.js` (no Motion: classes + one WAAPI trickle; exports `startTurning`, `stopTurning`, `busy`, `waitRegion`, `filo`), with **L1 as a singleton** (a second request is served as L2/L3) and an **`OUTCOME_BEARING` list** (situation recalculation, assessment, eligibility, scan verification) that only ever gets L2/L3; `components/loader.html`, `components/busy_key.html`; **no overlay on the header mark** (the council's lock sweep is withdrawn); hooks: `form[data-single-submit]` on every public form, same-origin link clicks → the thread, `pageshow` persisted → reset, the preview drawer → `waitRegion` (L3 + the L2 key in the head); `btn-busy` retired; the 10-second copy in four languages.
- **Tests.** `test_loader_rules.py` (constants, the singleton, the entrance-only L1, the outcome-bearing list), `test_keyframe_easings.py`, `test_design_docs.py` (the new keyframe names in DS 2026 §12), bundle currency.
- **Chrome checks.** States A (navigation), B (content), C (inline action), D (sign-in) frozen at 0 / 400 / 1000 / 1600 / 10 000 ms; the 240 px stage against the verbatim SVG at rest (pixel-identical) and after its one cycle; reduced motion; RTL (thread from the right, mark unmirrored); forced colours.
- **Performance.** Traces on 8772 during A + B + C: 0 long tasks; the **block test**; a trace **with every async region open at once** (preview, notifications, «Aller à…», search) — no task > 50 ms (`RED_TEAM` M19); CSS ≈ +2 KB gz, JS ≈ +2.5 KB gz.
- **Reviews.** Motion (lead), design (the mark at rest), performance, accessibility (announcements at 1 s, arrival, 10 s — never per cycle).

### F6 — Motion infrastructure (≈ 3 days)

- **Scope.** Motion tokens (+4 durations, +3 curves, CSS spring twins, `SPRING_SHEET` in `motion.js`); `head.js` sets `motion-armed` only for a fresh navigation without hash; the reveal contract (`html.js.motion-armed [data-reveal]:not(.is-in)`, the reveal pass first in `shell.js`, the same-row stagger fix); the **arch light** component (composited dash on the arch geometry, once after LCP through `withMotion`); the **route lights, once** — keyframes sampled **at runtime** from the live paths (`getPointAtLength`, twelve samples per route, once per layout, in an idle callback after LCP; WAAPI on `transform` / `opacity`), because `home.js` rewrites the routes at every width (prototyped in phase 0); the **journey** CSS generator for a **level** line (window, light on x only, station class table per count); the public **View Transitions** sheet (new root 120 ms), **off by default** until measured; the video module (`video.js`, ≈ 1 KB). **Moved here from P3** (`RED_TEAM` M9): the **`motion/mini` swap** and the move of the two scroll-linked effects (the door drift, the stage settle) to native `animation-timeline` CSS — nothing imports `scroll` any more — and the rail indicator as a CSS `linear()` spring.
- **Tests.** `test_data_reveal_placement.py`, `test_keyframe_easings.py`, `test_v5_tokens.py` (motion block), `test_js_budget.py` (≤ 45 KB gz per page type), `test_frontend_bundle_is_current` (it asserts the shared module's export list).
- **Chrome checks.** The law-2.2 frame test on home, login, dashboard, case file at 1440 / 390; the restored-scroll test on the home (reload inside the passage, back/forward, hash).
- **Performance.** **View Transitions: destination LCP with and without, 6 + 6 alternating runs** (measured + 90 ms at 180 ms; enable only if ≤ + 100 ms at 120 ms); the route lights vs today's current (main-thread share while the hero is visible: ≈ 0 after the ≈ 3.3 s first breath; the runtime sampling never a long task); the shared Motion chunk before and after the swap (target −16.6 KB gz, from the probes).
- **Reviews.** Motion, performance.

### Gate F — the foundation gate

On `/_design/` (the showcase, updated to V5: type, colour, icons, buttons, chips, fields, notices, loader, motion patterns) **and** on three real pages re-captured with the foundation only (home, dashboard, documents): the four reviews + accessibility. **Nothing in phase S starts before Gate F PASS**, because every flagship reads these tokens.

---

## 5. Phase S — the flagship surfaces, in the owner's order

Every S step ends with its own gate (§3). A flagship gate PASS is what allows its family to propagate in phase P.

### S1 — Homepage (≈ 8–10 days, images curated in parallel after O54)

- **Scope.** *Hero «La porta»* (`CREATIVE_DIRECTION_V5.md` §9): desktop composition (`min(100svh − header, 820px)`, copy low, the next chapter peeking ≥ 64 px), the V1 `.hero` padding leak closed (re-measured at desktop, where it is part of the approved composition), **Solution A** on phones (`council/mobile/solution_a_una_schermata.css` as the starting point; the body paragraph and the legend rendered once in each place and switched by a media query, with no duplicate `id`), **the interim title's own setting and the door's floor at today's size** (O45), landscape rule, the legend as the one selector on a solid night plate (no stage re-tint), the exits removed, **the arch light then the route lights, once (≈ 3.3 s), nothing looping**, the key-centred vignette, the H1 as the name in the wordmark face per O11, the lead per the §22.1 gate, the secondary CTA per O39. *Chapters* in the order of CD §20: the four doors (photographs per O23 / O60, micro-visual on a solid disc, spotlight, two task links; landform glyphs and ordinals retired), «Ce que nous ne faisons pas» + **the page's one «il gradino»**, **the orientation passage** — the primary public state (the diptych or «Lo stesso gesto» per O54, the **level** line, the light, the four orientation steps — `content.ORIENTATION_STEPS` on the interim, the locked sentence split on «→» in phase 3 — no sides, the questionnaire's primary; the seven-station passage and a separate BRAND band only after O46 and G3), pathways register rows, the Forum teaser («la marche» or its fallback), the ecosystem bento, News hidden when empty, «La porta riservata» with the signature CTA (the paper plate, static gilt edge), the footer's closing lintel without an arch. *First-frame contract*: `body.page-home` navy for the first `100svh`, the mark inline in the lock-up. *Images*: the door + 8 curated (after O54 and the full-resolution checks); no vault layer.
- **Depends on.** Gate 0; Gate F; T7; the curated images (`ASSET_USAGE_MATRIX.md` §6).
- **Chrome review checks.** Home at the six widths in fr / it / en / ar, **8770 (interim) first** — the orientation passage is what the public sees — then 8771 (phase 3); the **extended mobile acceptance tests** of CD §19 (both phases; four languages; the four nominal viewports **and** the four estimated small ones + 320 × 568; primary visible in every case; the door never smaller than today's at the same viewport; hero bottom ≤ 100 % at the nominal viewports in both phases and at the small ones in phase 3; home ≤ 9.5 screens at 390; landscape 667 × 375 and 844 × 390 with the primary in the first screen); the arch allow-list, the three gold contexts and one «gradino» per page checked on the captures; the differentiation review against the reference site; the hero states (legend hover / focus per audience; the first breath frozen at 0 / 300 / 900 / 1500 / 2400 / 3300 ms, then still); the passage frozen at scroll positions from the level geometry (LTR, RTL, reduced motion, phone spine — the gate-0 frames as reference); every door card hover / focus; the reserved band's signature CTA; no horizontal scroll 320–430 px; DPR 3 sharpness of the door (then decide on the 600 px strip).
- **Performance checks.** Home LCP ≤ 2.2 s (desktop: the door; mobile: the lead — test italic vs roman); CLS ≤ 0.05; below-the-fold images ≈ 375 KB desktop / ≈ 250 KB mobile, all lazy; the route lights (once) and the passage at ≈ 0 paints per scroll frame, and nothing moving after ≈ 3.3 s at the top of the home; 0 long tasks from motion; the first frame navy at fp + 0.
- **Reviews.** Design (lead), UX (the home as one passage; copy; the four doors equal), motion (laws, frames), performance, accessibility / RTL (the passage mirrors; the mark, door, photographs never).

### S1b — The public orientation questionnaire (≈ 3–4 days, ships with S1)

- **Scope** (`RED_TEAM` B4; registry FM12; O58). The hero's locked primary leads here, so it ships with the home. The V2 public wizard (full-page POST per step, a percentage bar, inert `hx-*`, plain radio lists, no busy state) takes the «Ma situation» grammar: one question at a time; «Question n sur N» in words; OptionCards with the real radio inside the label; the L2 key at submit (0 ms); focus on the arriving question's first control; the navigation thread on each step; the result page on the V5 kit with the outcome + sources block (SW21); the `hx-*` attributes removed; server-rendered, complete without JavaScript; the page sheet `v5/console/wizard.css` loaded as a page sheet, not in `main.css`. Signed-in people are routed into the console by T3.
- **Depends on.** Gate F; T3.
- **Tests.** `test_questionnaire_no_percentage.py` (no `%` sign and no `<progress>` in any rendered step or result; «Question n sur N» present); the locked-copy tests on the questionnaire's prescribed strings.
- **Chrome review checks.** Every step and the result at 1440 / 390 in fr and ar, interim and phase 3; keyboard only; no JavaScript; reduced motion; 200 % zoom.
- **Performance checks.** Each step's LCP and INP on submit; 0 long tasks.
- **Reviews.** UX (lead), design, accessibility (focus on arrival, the error summary), legal wording of the result (SW21).

### S2 — Navbar and mega-menu (≈ 5–6 days; search ≈ 3 more, may slip to P)

- **Scope.** The IA of O35 (six top items); the letterhead (scroll states, indicator persistence); the **portico panels** recomposed (grid 8 | 4: the serif head line and two columns of sub-links; the door's photograph as the panel's full-height field, no card, no caption) with the CMS fields (`MenuItem.description`, `image`, `image_alt`), the door photographs at 3:2 @ 480 w **prefetched at idle after LCP, ≥ 80 rem, low priority**, the anti-fraud entry as a one-line foot link, hover-intent 120 / 250 ms, section cross-slide + height morph (`SPRING_SOFT`), the scrim only on click / tap / keyboard open; the utility bar (Forum date, `ile-key`, language); the **mobile drawer** on native `<dialog>` in the new order (the anti-fraud entry as one line), pinned `<details>` sub-levels, «Fermer»; language thumb; reading progress + «Sur cette page» on long reads; the Forum local nav fade; **public search** (index build step) if O37 is signed for this phase.
- **Depends on.** Gate F; S1 (the door images).
- **Chrome review checks.** Every panel open at 1280 / 1440 in fr and ar (the photograph moves to the left in RTL); the keyboard model (←/→ between sections, ↓ into the panel, ↑ back, Esc to the origin, no page scroll) re-run with real keys as in gate A round 4; hover-intent vs a diagonal pointer path (no accidental switch); touch; 1.4.13 (hoverable, dismissible, persistent); the drawer at 360 × 800 (fits without scrolling; navigation starts near y 73); the header at 360 with the wordmark; reduced motion (80 ms opacity).
- **Chrome review checks (added).** The differentiation review against `captures/ref_agami_*` on the panel and the drawer, signed by the design reviewer.
- **Performance checks.** 0 panel image bytes before LCP (the idle prefetch comes after it); INP on opening a panel and switching sections ≤ 200 ms at CPU ×4; CLS 0 from the header; the search index ≤ 30 KB gz per language, fetched on first focus.
- **Reviews.** Design, UX (IA, labels, the four doors equal in the chrome), motion, performance, accessibility.

### S3 — The loader in context (≈ 3 days)

- **Scope.** Wire F5 everywhere: the thread on every same-origin navigation (public and console; the header mark and the rail tile stay still), `data-single-submit` + busy keys on **every** public form (enquiries, Forum registration, questionnaire), region loaders (L3 + the L2 key) on the few async regions (preview, «Aller à…», notifications, search), L2/L3 only on the outcome-bearing requests, the 10-second path; switch on the public View Transitions if F6 measured them inside the gate.
- **Chrome review checks.** Slow 4G navigations filmed (screencast) between the home, a landing, the Forum, the login and the console: the thread appears at 400 ms, never earlier; the old page never goes blank; bfcache return resets; reduced motion (static thread); RTL.
- **Performance checks.** Traces of a navigation with the thread; the block test on a real page; the all-regions-open trace; LCP of the destination with View Transitions on (≤ + 100 ms).
- **Reviews.** Motion (lead), performance, UX (the 10-second copy), accessibility (announcements).

### S4 — Login «Il varco» (≈ 3 days)

- **Scope.** The focus letterhead; the split (the door stage on night + the arch light after LCP; the form on the mineral paper, serif H1); the key turning **once** on submit (L1 at stage scale — two half-turns and the frame light, the planes still, no crack of light; owner O1), the wait then carried by the button's L2 key and the thread, the error summary focused on error; the night panel a solid plate; «Oublié ?» in the label row; the reassurance line (O44); the reset / verify / MFA sub-pages; the phone band (120 px night + arch-and-steps glyph), the e-mail field in the first viewport at 390 × 844.
- **Chrome review checks.** Login, signup, reset, verify, TOTP at the six widths in fr and ar; a **submit filmed on slow 4G** (the key turns at 0 ms, once, and rests; nothing waits); a failed login (sessions minted server-side; no password typed by the probe — the failing case produced with a server-side fixture); password managers' autofill (`autocomplete` values); reduced motion.
- **Performance checks.** Login LCP (the door) ≤ 2.2 s; INP on submit; 0 long tasks while the key turns.
- **Reviews.** Design, UX (the focused threshold), motion, accessibility (error summary, focus), performance.

### S5 — App shell (≈ 6–7 days)

- **Scope.** The labelled rail (open from 80 rem, compact 80 px labelled below with 12/16 labels, 13/20 in Arabic; `short_label` in `portal.services.navigation`), the travelling indicator, group titles; the context bar (collapsing breadcrumb, condensing title, «Aller à…» with a same-origin JSON of permitted destinations — staff variant without persons, the bell + count badge + notification panel on the `Notification` model, the account menu V5 with identity and space switcher, language); `scrollbar-gutter: stable`; the shell symbols in the document; the bottom bar (short labels, one line ≥ 12 px, the page action bar replacing it **and carrying «Menu» at its inline end** — O63; no duplicate ≡); the rail tile with the mark, still (O2); **toasts** from Django messages; the context index pattern in the inspector head.
- **Depends on.** Gate F; T1–T5 (so the shell's pages tell one story).
- **Chrome review checks.** Dashboard, documents, case, company, situation, Guichet, Academy at 1440 (rail open) / 1280 (open from 80 rem) / 1100 (compact labelled) / 390 (bottom bar); rail collapse persisted and restored without a load-time transition; `test_phone_menu.py` at 360 × 800 on every console template; keyboard ↑/↓/Home/End in the rail; ⌘/Ctrl K and Esc; the bell panel (empty «Tout est à jour», unread, to-act); the account menu for a person, a company referent, staff and a multi-role account; RTL; reduced motion.
- **Performance checks.** Console first paint with glyphs at fp + 250 ms; CLS from the scrollbar ≈ 0 (today ≈ 15 px jump); INP of the rail toggle (with `contain: layout`), the palette, the bell ≤ 200 ms; «Aller à…» module ≤ 4 KB, loaded on first use.
- **Reviews.** Design, UX (lead: labelled rail, identity, short labels), motion (indicator, drawer), performance, accessibility (the palette's combobox, the bell's live count).

### S6 — Person dashboard (≈ 4–5 days)

- **Scope.** ContextHeader (identity only) → **NowPanel** with its primary (O50) → «À faire» (merged pieces + deadlines) → **JourneyRail «la soglia»** (the travelled line, done nodes as filled ink dots without a glyph, the light to the current node after LCP and the 2 px ring drawn once on arrival, threshold A `stamp`, threshold B `ile-arch` 16 px per O3, «Cette étape» disclosure, causality on the next load) → «Activité» (the case timeline by day) → «Raccourcis»; empty regions collapsed; the «no case yet» EmptyState with the orientation image; «Mon compte» moved to the account menu; the Dossier facts as a two-column grid on phones.
- **Depends on.** S5; **T1–T3**.
- **Chrome review checks.** A new person, a person mid-case (`EE167596D4`), a person with an overdue piece, a person without a case, a company referent with the person role; phone (current-step card, «Mon parcours» above the bottom bar at 390 × 844); the rail light frozen at 0 / 120 / 240 / 360 ms in LTR and RTL; reduced motion.
- **Performance checks.** Dashboard LCP (last measured 2.43 s on the uncompressed server; target ≤ 2.2 s on 8772); 0 long tasks from the rail light; CLS 0.
- **Reviews.** UX (lead: now / where / what happened), design, motion, performance, accessibility.

### S7 — Documents (≈ 7–9 days; the Dépôt needs a JSON branch in the upload views)

- **Scope.** The collection (subgrid, header row, groups by who must act, empty groups not drawn, «Sans échéance»), DocumentRow V5 (stretched title → preview, only the person's act as a button, the `ellipsis-vertical` menu trimmed), non-zero filters with the sliding thumb, the **Piece Ledger** replacing the HealthStrip (≤ 24 pieces; 16 px marks in three labelled runs — «À vous» · «En cours» · «Réglées» — colour = the group, shape = the state, O62), the **preview drawer** (fragment fetch, L3 + the L2 key in the head, `pushState`, `popstate` closing it and returning focus to the row title), the **Dépôt** (the five layers; client guards mirroring the server; XHR progress; the row lifecycle; the same CSRF endpoint + a JSON branch; throttling as a sentence), the piece detail page migrated from V2 to the V5 kit, toasts and the cause bar, the title coherence «Mes pièces» (O43).
- **Depends on.** S5; T1–T2.
- **Chrome review checks.** A register of 3, 12 and 30 pieces (ledger vs counts-only fallback), every state present once; the ledger at 1× DPR through a colour-vision-deficiency simulation (protanopia, deuteranopia, tritanopia, greyscale); the columns aligned across rows (measure the state column's x on every row); keyboard: title → act → menu per row; the preview open / close / reload on the pushed URL; an upload filmed on slow 4G (queued → sending with bytes → verifying → filed, the filed mark drawing itself — no check; a refused format; an interrupted transfer with Retry) — with test files, never real documents; phone (cards, filters wrapping); ar.
- **Performance checks.** INP on filter change and preview open; the upload's progress updates without long tasks; the drawer's fragment fetch shows nothing below 400 ms.
- **Reviews.** UX (lead: the flagship interaction), design, motion (row FLIP ≤ 40 rows, the filed mark, cause bar), performance, accessibility (the dropzone keeps the real input; announcements at start and end only).

### S8 — Case file / fascicolo (≈ 5–6 days)

- **Scope.** The order Maintenant → Ce qui est demandé (one list, grouped, with the ledger) → Parcours (the vertical rail, current step expanded) → Qui intervient; the inspector «Suivi» (timeline by day, the last node lit once) with the **context index**; «Intervenant» (O43); state transitions as **intent buttons** with a consequence dialog (O52 / T6); the sticky compact bar with the micro-ledger and the one primary; the assessment page migrated.
- **Depends on.** S6, S7; T1, T2, T6.
- **Chrome review checks.** Person and staff views of the same case; a suspended case; a closed case (neutral, never a verdict); the index marker following the scroll; the phone composition (current-step card, sticky action bar replacing the bottom bar: chrome ≤ 120 px at 360 × 800).
- **Performance checks.** LCP ≤ 2.2 s; INP on intent buttons and the dialog; the compact bar's condensing without CLS.
- **Reviews.** UX (lead), design, motion, performance, accessibility.

### S9 — Company area (≈ 4 days)

- **Scope.** The needs overview strip (counts as filter links), the needs table as the reference Table V5 (stretched rows, sortable headers as links, cards below 64 rem), the CTA naming its verb, «Vérifiée» without the seal (O18), the referent's name + company in the account summary, the need detail migrated to the case-file composition, the company profile and analysis pages on the kit.
- **Chrome review checks.** qa-company at the six widths; every need state; sorting by keyboard; ar.
- **Performance / reviews.** As S8.

### S10 — Academy (≈ 4 days; public Formation landing ≈ 2 more)

- **Scope.** Academy leaves the serif (O12) and joins the console language; «Mon suivi» first when enrolled (enrolment rows + notched module meter); the catalogue as a register with non-zero filters; lesson lists; covers only per O26; the Academy caveat as a V5 notice; «Mes formations» as a real entry. Public: the Formation / Academy landing with `laboratoire-formation-technique` and the «atelier» loop (V3).
- **Chrome / performance / reviews.** As S8; the video contract checked (plays only ≥ 64 rem, in view, no Save-Data / reduced motion; the Pause toggle; the poster alone on phones).

### S11 — Forum (public ≈ 5 days; governance when its gate opens)

- **Scope.** Public: the event card and the **date-computed state machine** (announced → today → held → permanent) for the page, the home teaser and the utility-bar link; the timetable rule; the tribune of role cards; «la marche» band (or its fallback, per O54), the plain band, the «table est mise» loop (only if O60 keeps it); the gallery filmstrip for the `held` state with **commissioned photographs with releases** (O25); no disabled buttons (a sentence of «when»); the landing hero (`forum-prise-de-parole`, never captioned as documentary). Governance (when the gate opens): state lanes without drag, the engagement caveat as a persistent notice, milestones through the timeline component.
- **Timing, honestly.** The Forum is on **2 October 2026**, five days after this plan. No step of this plan can ship before it safely (Gate F alone takes longer); S11 is therefore designed for the `held` and `permanent` states. If the owner wants something visible before the event, only T-track fixes on the Forum page are candidates, and each still needs its measurement.
- **Chrome / performance / reviews.** As S1 for the public page; the state machine tested with a fixture date for each state.

---

## 6. Phase P — propagation (after each family's flagship gate)

| Wave | Templates | Kit |
|---|---|---|
| P1 public | the other ≈ 50 public templates: inner pages (the revised section grammar, landing heroes for the four doors), pathways detail and index, living (index, topic, sheet — **PX26 on PX27**), news (index, detail — **PX24 prose**), FAQ, glossary (**PX25**), ecosystem (four; the pilot page on the passage's level line, the pilot-flow illustration retired), partners, the **9 unstyled community pages** (composed from SW13, PX14, SW11), enquiries, errors; the home's jurisdiction bar retired | CD §20 |
| P2 console | the account pages moved into the console on **SC11**; the pre-assessment outcome on **SW21**; the homes of institution, university and professional accounts on **SW22**; the back-office mapping **SC12**; then the ≈ 32 V2 register templates and 5 V2/V3 lists, **by family, not by page**: DocumentRow / Collection · Table · Timeline · Register-row V5 · Panel / Facts — piece detail and assessment first (in S7 / S8), then need detail, requests / messages / deadlines / pathways (→ inbox and lists), helpdesk staff (queue, dispatch) with the filter bar, selection, forum governance when its gate opens | UX_PLATFORM §4 |
| P3 depth | public search (if not in S2); staff «Aller à…» variant; the shortcuts dialog; notification preferences (switch rows); Speculation Rules (measured, with the exclusions of UX_PLATFORM §3.12) — the `motion/mini` swap moved to F6 | MOTION §8.3 |
| P4 clean-up | (the dead CSS already left in F2; each replaced V3/V4 component sheet left in the step that replaced it) the V1/V2 sheets once no markup uses them, the V4 aliases after one release, the showcase-only components not adopted, `hx-*` attributes without htmx; one final full-site re-probe | UI_INVENTORY §10.5 |

Each wave: the §3 protocol on every touched page, reviews by family, no page left half-migrated (a page is V5 or V4, never both).

**Owners of the nine types added after the red team** (roles, not people — O65): FM12, the UX lead, with legal on the result wording (S1b); PX24–PX27, the design lead (P1); SC11 and SW22, the UX-platform lead (P2); SW21, the UX-platform lead with legal on the outcome wording (P2); SC12, the developer who holds the `UNFOLD` settings (P2); the community pages, the product owner, when gate G11 opens.

---

## 7. The React-island decision

**Criteria** (all must hold): the interaction cannot be built with server-rendered HTML + CSS + ≤ ~4 KB of vanilla JS or Motion; its state is genuinely client-side and complex; it fits the ≤ 45 KB gz public JS budget with no long task > 50 ms at CPU ×4; it works under `script-src 'self'` / `style-src 'self'` without injected styles; the page is complete without it; it is at least as accessible as the native alternative.

**Evaluated** (`21ST_COMPONENT_MATRIX.md` §5): the liquid-metal button, the command palette, the upload, the mega-menu morph, the notification centre, the toast manager, the data table, a kanban, a PDF viewer, the journey animation, charts. **None meets the criteria. Route C = 0.** React is not added. If a future need appears (for example a genuinely client-side document annotation tool), the same six criteria decide, and the island would ship as a separately bundled, dynamically imported module on the one page that needs it, with its own gate.

---

## 8. Risks and rollback

| Risk | Where | Mitigation · rollback |
|---|---|---|
| Fonts shift metrics or legibility (Host 13 px, I/l) | F1 | metric-matched fallbacks; the `--u-small` lever; pairing B ready in `tokens-v5-type.css`; one revert commit restores V4 fonts |
| The lighter console reads washed out | F2 | one selector (`body.console`); revert = remove the block |
| Square caps spike on some glyphs | F3 | the specimen check before the site migration; per-glyph fix in `src/` |
| 65 chip sites regress | F4 | the chip board + re-probe of every site; aliases keep V4 values until the gate |
| The key's one-shot at the entrance reads as a gimmick | F5, S4 | judged frame by frame at gate 0; O1 lets the owner withdraw L1 (the login keeps the arch light and the L2 key) |
| The L2 key looks busy or cheap at 14–24 px | F5 | judged on real pages at 1× and 2×; the thread alone as the fallback in rows |
| View Transitions cost LCP | F6 / S3 | measured gate; off by default; the thread alone |
| The italic lead costs LCP | S1 | measured gate; the serif roman fallback (the vault layer is dropped) |
| Solution A on real phones differs from the estimate | S1 | one iPhone + one Android before sign-off; the interim title's own setting; the landscape rule |
| Truth-track changes alter legal meaning | T1–T3 | product / legal review of the precedence; unit tests per rung |
| Stock photographs raise release questions | S1, S2, S10, S11 | never documentary; full-resolution checks; replace with commissioned photographs when available |
| Scope creep from the catalogue | all | the registry is closed: a new component type needs an ECD entry with its route and class before code |
| The F15 ruling takes time | phase 0, S1 | «Lo stesso gesto» and the Forum fallback are ready; S1 never waits for arcades |
| The interim hero cannot meet the door floor and the peek on small phones | phase 0, S1 | the stated precedence (primary, door, peek); the interim title's own setting; measured on 8770 before S1 |
| The paper-plate primary reads weak or odd on night | phase 0 | judged on the gate-0 comps; fallback: a flat laguna-400 plate without gradient or glow |
| The runtime sampling of the route lights shows as a long task | phase 0, F6 | idle callback after LCP, twelve samples per route; if it still shows, freeze the route geometry |
| The grouped ledger confuses («why is MANQUANT amber in the chip and terracotta in the ledger?») | S7 | the group labels carry the words; the copy review (O43); fallback: ink-only marks |
| Stock faces raise legal questions | S1, S2 | O55 before curation; Persona shows nobody identifiable; commissioned photography (O56) |

Rollback unit = one commit per family; the V4 aliases make every F step reversible without touching templates.

---

## 9. Rough effort (ECD estimates, one developer, excluding review time)

| Phase | Estimate |
|---|---|
| Phase 0 «La prova» | ≈ 6–8 days (comps, two prototypes, the photograph checks) + the owner's review |
| T track | 5–8 days (engineering + product decisions) |
| F1–F6 + Gate F | ≈ 18–22 days |
| S1–S11 (+ S1b) | ≈ 58–69 days |
| P1–P4 (+ the nine new registry types) | ≈ 31–44 days |

Reviews add about a quarter on top. These are orders of magnitude for planning, not commitments; the council measured nothing about implementation speed.

---

## 10. What this plan does not do

- It does not start before the owner's signatures (§1), and it does not ship to production.
- It does not re-open the brand: the mark, the wordmark font, the door photograph and the prohibited wording stay as the owner set them.
- It does not add a framework, a remote asset or a second animation library.
- It does not invent data: actors per journey step, a document kind, course covers and Forum photographs arrive when the owner provides them; until then the interface shows what exists.
- It does not curate a photograph before the owner's F15 ruling (O54) is written into `docs/IMAGE_LICENSES.md` §1, and it does not ask the owner to sign decisions before the pictures of gate 0.
