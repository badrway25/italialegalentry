# CREATIVE DIRECTION V5 — «La soglia»

**Italy Legal Entry™ · Executive Creative Director · 27 September 2026**
**Status: PROPOSED — revised after the red team (27 September 2026).** Nothing here is in force until the owner signs it and a gate measures it. The independent red team (`RED_TEAM.md`, same folder) found 4 blocking, 19 major and 18 minor issues; this revision resolves each one in the text or answers it in writing, and §26 «Revisione dopo red team» lists every issue with its resolution and where it was applied. The repository `C:/tmp/italylegalentry` was only read (HEAD `c9a58d8`); everything this role wrote is under `C:/tmp/ile_v5_council/final/`, `C:/tmp/ile_v5_council/scratch/ecd/` (the revision's measurements and searches: `scratch/ecd/revision/`), two OFL licence texts added to `council/typography/fonts/`, and three one-line errata at the head of council reports (§26, M18).

**Companion files (same folder).** `DESIGN_SYSTEM_V5.md` (tokens, scales, component specs and the registry of 122 component types) · `21ST_COMPONENT_MATRIX.md` and `21ST_SEARCH_LOG.md` (the five curations merged, final decisions, coverage counts) · `ASSET_USAGE_MATRIX.md` · `ICON_SEMANTIC_MAP.md` (final) · `IMPLEMENTATION_PLAN.md`.

**Inputs.** The fifteen council reports under `C:/tmp/ile_v5_council/council/` — `UI_INVENTORY`, `CAPTURES_AND_REFERENCES`, `21st_nav-shell`, `21st_hero-public`, `21st_primitives`, `21st_forms-docs`, `21st_platform-domains`, `TYPOGRAPHY`, `COLOUR`, `ICON_SEMANTIC_MAP`, `IMAGERY`, `MOTION`, `MOBILE_UX`, `UX_PUBLIC`, `UX_PLATFORM` — and their evidence: the type and colour specimens and token proposals (`council/typography/`, `council/colour/`), the icon specimen (`council/icons/`), the loader and journey prototypes (`scratch/loader/`, `scratch/journey/`), the two mobile prototypes (`council/mobile/`). The repository's own design documents were read where a decision needed the original wording: `docs/design-v4/CREATIVE_DIRECTION.md` §3.1, `docs/design-v4/README.md` (gate A rounds 3–4), `docs/design-v2/BRAND_ASSETS.md` §1–2, `scripts/fetch_images.py` (editorial rules), `static/css/v4/tokens.css`, `static/css/v4/hero.css`.

**How to read.** §0 is the answer. §1 is the concept. §2–§20 are the decisions, area by area, each with its reason and its council source. §21 lists what is rejected. §22 treats the four gate-A deviations. §23 records how council conflicts were arbitrated. §24 consolidates the owner's decisions, in the order the owner should sign them. §25 says what I could not do. §26 is the revision after the red team: every issue, its resolution, and what is still open.

---

## 0. The answer in twelve lines

**Revised after the red team.** The owner signs pictures before decisions: a **gate 0 of composed screens** (`IMPLEMENTATION_PLAN.md` phase 0) comes before any signature of §24, except the few rulings the pictures themselves need (§24, first group).

1. **V5 is V4 finished, then given one gesture.** The owner judged an unfinished V4: on the public home only the hero and the navigation were built in the V4 direction (`UI_INVENTORY` §10.2), and in the console 5 authenticated templates out of about 51 speak the V4 language (`UX_PLATFORM` §2 D1). Restyling the first screen again would fail for the same reason. V5 is a pass over **every** public template and **every** console family, in one language.
2. **The concept is «La soglia» — one door, two shores, one key, one light — and each brand act has a budget.** *The door* (the owner's photograph inside the arch) lives on the hero, the login and the error pages, and the arch shape appears nowhere else except the journey's arrival threshold. *The key* turns once, when the person enters (the login). *The light* (gold, the only colour that travels) lives in three contexts only: the arch once after LCP, the journey line, the entrance. *The threshold* is the journey line — level, with the same grammar on the public site and in the person's dossier.
3. **Type.** Source Serif 4 for public titles, the promise line and the lead; Host Grotesk for everything that works; IBM Plex Mono for references; Vazirmatn and Markazi Text for Arabic. **The trademark name has one drawing everywhere** — the Newsreader 600 «ILE Wordmark» subset (11 code points, 1.71 KB, rebuilt and measured in this revision) in the lock-up, the hero H1, the project page, the footer and the rail. Fonts on the home: 356 KB → ≈ 74 KB (`TYPOGRAPHY` §9.2, byte counts of production-shaped builds).
4. **Colour.** Five materials — *carta, inchiostro, notte, laguna, oro* — seven chromatic state tones and one ink register, solved under contrast constraints (363 pairs verified by the council, `COLOUR` §10; the pairs this revision changes are re-computed in §26). **`conforme` stays ink, without chroma, as the repository already enforces with a test**: no colour and no check mark ever means «approved». Green leaves the system. The console becomes one step lighter paper under the same night chrome.
5. **Icons.** One hand: the ILE sprite plus Lucide geometry under the ILE treatment (1.5 px effective stroke at every size, square caps, miter joins, a 12 % tone on concept glyphs); five identity glyphs drawn from the mark; one concept, one glyph. Statuses become one family of circle marks — **«i cerchi»**: outline = open, filled = settled; VALIDE is the plain filled ink disc, with no check.
6. **Imagery.** One photograph per context, self-hosted, graded as by one photographer; Italy and Morocco shown through what they share, never through travel, borders or postcards. **The arcade concept waits for the owner's ruling on the scope of F15 («porte/soglie»)**; until then the prudent reading applies and a non-architectural set is ready — **«Lo stesso gesto»**, the same gesture of a craftsman's hand on each shore. Nobody identifiable stands on the Persona door. No photograph on operational screens. The door stays the LCP element.
7. **Motion «la chiave che gira».** Nothing painted is taken back (the gate-A law, now with a test). **Nothing loops on the home**: after LCP the arch light and the four route lights play once, in ≈ 3.3 s, and rest. The mark's key turns once, on the login stage, when the person submits; the tricolour planes never move. Every other wait is carried by the key alone in the button (L2), a still skeleton crossed by one light (L3) and the 2 px navigation thread — never by a door, and never with the brand on a request whose answer is legal.
8. **Chrome.** The public letterhead opens into portico panels whose photograph is the panel's own field, not a featured card; the console gets a labelled rail, a context bar that finally holds «Aller à…», the bell and a real identity, and a workspace with an inspector — not a fourth column. On phones the Menu control never disappears.
9. **Signature components.** The journey «La soglia» (public and console), the Piece Ledger «Il registro», the upload «Dépôt», the anti-fraud step «Il gradino» — the last one **once per page**.
10. **Mobile.** Solution A «Una schermata». *Measured for phase 3 at the four nominal viewports:* hero bottom at 96.0–96.5 % from 360 to 412 px, door +81 % in area at 390 (`MOBILE_UX` §3.4). *Not yet true for the interim* (what visitors see while G3 is closed): with the V4 interim title the door shrinks below today's and the hero reaches 101–108 % on the estimated real-phone heights. V5 gives the interim title its own setting, sets the door's floor at today's size, and re-measures both phases in gate 0 (§19). The fourth gate-A deviation is corrected, not waived.
11. **No React.** 122 component types in the V5 registry: 68 adapted from 21st.dev patterns and rewritten in Django templates + CSS (+ small ES modules / Motion), 5 native patterns reviewed on 21st, 40 ILE originals, 9 kept as built. **0 React islands.** 18 patterns rejected.
12. **Performance by construction, proven by measurement.** Fonts −282 KB on the home. JS: the `motion/mini` swap and native scroll effects move into the foundation (F6): −16.6 KB gz on every page, measured on the council's probes. CSS: the console-only sheets leave the public bundle (−6.4 KB gz, measured on today's bundle in this revision), each replaced sheet leaves in the step that replaces it, and CI tests hold `dist/main.css` ≤ 45 KB gz and public JS ≤ 45 KB gz per page type. No new LCP candidate: the vault layer is dropped. What is measured and what is estimated is said each time.

---

## 1. The concept and the promise

### 1.1 «La soglia»

Italy Legal Entry is a threshold. The official mark already says it with four shapes — two planes, an arched door, a golden key, three steps — and V5 makes the whole product speak that sentence and nothing else:

- **the portico** (public site) explains the door and the four ways to it, and shows the two shores it joins;
- **the console** (platform) is the room behind the door, where the work of a regular path is done;
- **the key** turns once, when you enter — on the login stage, which is exactly what the brand rule already allows (`BRAND_ASSETS.md` §1: «se si muove, si muove una volta, all'ingresso»);
- **the light** shows the way — it runs the arch once when the home or the login has painted, it lays the journey line as you read, it runs the door frame once as you enter — and it never replaces a word;
- **the steps** are the path itself: the three steps of the mark become the seven stations of the journey and the anti-fraud promise that no step can be skipped.

The mark's English tagline and the caption under the door remain unreproduced, in any language (`BRAND_ASSETS.md` §1: prohibited wording F13/F14). The concept is carried by shapes and behaviour, not by that sentence.

Premium, in this concept, is **restraint plus craft plus one gesture repeated with discipline** — and «with discipline» means budgeted: the arch, the gold light and the anti-fraud step each have a written allow-list and a test (§1.3, §1.4 laws 1, 5 and 7; `RED_TEAM` M2, M3, M14). That is the principle both reference sites teach (one mark with three uses; one accent; a strict section grammar — `CAPTURES_AND_REFERENCES` §3.1–3.3, principles only, nothing copied).

### 1.2 The promise, made operational

| The owner's word | What the person sees in V5 | What guarantees it |
|---|---|---|
| **Premium** | five materials, two faces and one drawing of the name, one icon hand, photographs graded as by one photographer, generous rhythm, hairlines instead of boxes, flat primaries without glow | tokens with a single direction of reference; a test forbids `--f-serif` in console sheets; a test reads the computed face of every rendering of the name; a test forbids hex in the sprite; `verify_tokens.py` in pytest form |
| **Elegant** | serif titles only where the portico speaks; an italic lead; passe-partout frames; one accent | the serif scope rule (§2); the one-accent rule (§3) |
| **Institutional** | registers, verifiable counts («4 sur 11»), dates in `<time>`, locked copy verbatim, `conforme` in ink, patronage attached to the Forum, never to the platform | CR-11 (no colour and no check mark means approved: `test_chips_registry.py`, kept, and its V5 extension); the locked-copy tests; no invented numbers anywhere |
| **Modern 2026** | native platform features: cross-document View Transitions, scroll-driven animations, Popover API, `<dialog>`, CSS subgrid, `svh`, variable fonts, AVIF | progressive enhancement only; every page complete without them |
| **Dynamic** | the gold light in its three contexts, the portico panel opening, state changes that show their cause, the upload lifecycle, the navigation thread | the motion laws (§6): additive, composited, interruptible, and nothing looping on the home |
| **Memorable** | six signatures you can describe tomorrow (§1.3) | each is ILE's own; none comes from a catalogue |
| **Image-rich** | a photograph for each door wherever the door appears; the two-shore diptych (arcades if the F15 ruling allows them, otherwise «Lo stesso gesto»); the Forum band; at most three loops, never on the home | one image = one context (`IMAGERY` §2.2); the F15 ruling before any curation (O54) |
| **Excellent UX** | one next action with its button; one list of what is asked; a labelled rail; filters that never select nothing; grouping by who must act; «Aller à…»; notifications; a phone-first hero | the P0 truth fixes (`UX_PLATFORM` §6) precede any visual gate |
| **Refined motion and loading** | a branded wait — the key in the busy button, a skeleton that stays still for a second and is then crossed by one light, the thread; the mark's key turning once at the entrance — with thresholds (nothing before 400 ms, content never waits, ≥ 480 ms once shown, 10 s → a message) | `test_loader_rules` (thresholds, the L1 singleton, the outcome-bearing list), `test_keyframe_easings`, the block test |
| **Coherent site and platform** | the same line, light, station marks, glyphs and tokens on the home and in the dossier — and the same seven stations once D-U9 and G3 allow it | one registry of glyphs, one journey component in three densities |

### 1.3 The six signatures — ILE's own

| # | Signature | What it is | Where it lives | Source |
|---|---|---|---|---|
| 1 | **La porta** | the owner's door: arch, photograph, key, three steps | home hero, login, error pages (static) | `BRAND_ASSETS.md` §2 (brand-locked) |
| 2 | **La luce** | the gold light — the only colour that travels | **three contexts only**: the arch once after LCP (hero, login) · the journey line (public passage, console rail) · the door frame once at the entrance (login submit) — never on a CTA, the header mark, the rail tile or a panel head | `MOTION` §5.1, §6.4, §7; `RED_TEAM` M3 |
| 3 | **La chiave che gira** | the key half-turns twice with a detent while the light runs the door frame, **once**; the tricolour planes never move; rest = the verbatim mark | the login stage on submit (and the sign-up, reset and verification stages) — nowhere else; the key alone (L2) in busy buttons | `MOTION` §6; `BRAND_ASSETS.md` §1; `RED_TEAM` M10 |
| 4 | **La soglia** | the journey line — **level**, the two shores at the same height — with two thresholds, laid by one light | the home's orientation passage (four steps until D-U9 and G3, then seven stations), the dashboard rail, the case rail, the Espace Personnes | `UX_PUBLIC` §5, `MOTION` §7, `21st_platform-domains` §5; `RED_TEAM` M4, M16 |
| 5 | **Due rive** | the two-shore diptych: «Due portici» (an Italian and a Moroccan arcade) **if the owner rules arcades outside F15**; otherwise «Lo stesso gesto» — a craftsman's hand guiding a chisel through cedar (Morocco) and through marble (Italy) | the head of the passage; the regular-mobility page | `IMAGERY` §2, §3.13–3.14; this revision §5; `RED_TEAM` B2 |
| 6 | **Il gradino** | the mark's three steps as the anti-fraud component: nobody can sell you a skipped step | **one full instance per page** — the band on the home, the rail block on inner pages; elsewhere (portico panels, drawer, footer) a one-line link | `UX_PUBLIC` §4.3; `RED_TEAM` M14 |

Two system signatures complete them: **«I cerchi»** (the status marks, §12) and **«Il registro»** (the Piece Ledger, one mark per requested piece, §12).

### 1.4 The ten laws that make it one team

These hold for every component, whatever its source.

1. **One accent, one travelling colour.** Laguna means *interactive*. Gold means *identity* and is the only colour that moves, in three contexts (§1.3). State tones appear only where a state is stated. **The tricolour lives in the mark and nowhere else** (V4 DS §1.8, `BRAND_ASSETS.md` §1; the council's notice filet is not adopted — O57).
2. **One serif scope, one drawing of the name.** Source Serif 4 sets public titles, the promise line and the lead; it never appears in the console (a test greps the console sheets). The trademark name is drawn only in the «ILE Wordmark» face, wherever it appears, and nothing else uses that face (a test reads the computed font of every rendering, on public, console and `/ar/` pages).
3. **One icon hand.** 24 grid, 1.5 px effective stroke at every size, square caps, miter joins, a 12 % tone on concept glyphs only. A donor glyph never enters with its own look.
4. **One motion physics.** One duration ladder, six curves, three springs with CSS twins; no overshoot anywhere; nothing painted is taken back; **nothing on the home loops**; one live object per page; the chrome stays still on navigation.
5. **One image, one context.** People are never duotoned, and nobody identifiable stands where the placement would cast them as an applicant. No text on busy pixels. **The arch belongs to the door, and the door has an allow-list**: the lock-up and the favicon, the hero, the login, the error pages, and the journey's arrival threshold — nothing else (a test counts arch occurrences per template).
6. **One primary action per screen**, placed next to its reason.
7. **No colour and no check mark mean approved.** Every state is a word + a mark + a pattern + an edge style; `conforme` is ink; a check mark appears only on the person's own interface acts (a ticked box, a chosen option, a saved setting), never on a piece, a step, a case or an outcome.
8. **Locked copy is rendered verbatim.** Design may split a locked string on its own separators for layout; it never retypes it (a test asserts the equality).
9. **Self-hosted, CSP-clean, progressive.** No `style=""`, no inline script, no remote asset; complete without JavaScript; complete under reduced motion; RTL mirrors direction only — never the mark, the door, a photograph or the key.
10. **Measured, or not shipped.** Every change re-probes every page its sheet touches (project memory: two regressions reached a commit from un-measured one-line corrections).

### 1.5 How the 21st.dev catalogue became ILE

The catalogue was input; the ILE design system is the output. Of 544 distinct candidates the curators registered (600 register rows, 45 candidates seen by two or three families), about 163 served as the source of a mechanism. None is installed. Each selected pattern was reduced to its mechanism and re-expressed through six filters:

1. **Tokens**, never the author's colours, radii, shadows or springs (#27428's overshoot curve became `--ease-layout`; #26905's spring became the critically damped `SPRING_SHEET`).
2. **ILE glyphs**, never lucide/react-icons at runtime.
3. **CSP**: no injected `<style>` (the reason #10443's shader wrapper, #29952 and #16834 lost their code), no `style=""` (positions written through CSSOM from bundled modules).
4. **Native elements first**: `<dialog>` (#23558, #26905 behaviours), `<details name>` (#22313, #26656), the Popover API (#23548 only as the fallback), real `<table>` (#19793), links for filters and pagination (#23541's algorithm is Django's `get_elided_page_range`).
5. **The best accessibility model in the shortlist**, even when its look was rejected (#31509 keyboard model, #29334 focus model, #23570 roving tabindex and bold sizer).
6. **ILE doctrine**: no ranking of the four doors, no verdict colour, no persons in command surfaces, no drag of a governed state.

That is why V5 reads as one design team: the catalogue supplied mechanics; the look, the physics and the words are ILE's.

---

## 2. Typography — «Fournier e la console»

**Decision: pairing A** (`TYPOGRAPHY` §8, measured file by file, all SIL OFL 1.1, self-hosted).

| Role | V5 face | File(s) and weight | Replaces |
|---|---|---|---|
| Public display and titles | **Source Serif 4** 400 roman, static instance at `opsz` 48 | `v5-SourceSerif4-400-opsz48-nosc.woff2` 25.3 KB, preloaded on public pages | Newsreader 300 (the thin brand line) |
| Public lead, pull quote | **Source Serif 4** 400 italic, `opsz` 20 | 19.1 KB, loaded on use | Newsreader italic 143.4 KB (the file that pushed the lead to roman in gate A) |
| Interface, body, the whole console | **Host Grotesk** variable 400–700 (+ 400 italic) | 18.8 KB preloaded everywhere; italic 13.8 KB on use | IBM Plex Sans (the default «serious tech» pairing) |
| References, hashes, rule versions | **IBM Plex Mono** 400 (kept) | 8.8 KB on use | — |
| Arabic interface | **Vazirmatn** variable 400–700 | 31.5 KB, preloaded on `/ar/` | IBM Plex Sans Arabic (three static files) |
| Arabic display | **Markazi Text** 400 | 20.8 KB, `/ar/` public | Noto Naskh Arabic |
| **Wordmark** (brand asset) — **every rendering of the trademark name** | **Newsreader 600, untouched**, as the «ILE Wordmark» glyph subset (11 code points: the capitals of the name, the space and ™ — the council's «13» corrected by recount; `opsz` 20; `unicode-range` limited to those code points) | **1.71 KB** (rebuilt from the pinned master and measured in this revision; an `opsz` 36 display instance of the same subset measures 1.70 KB) | the 128.9 KB Newsreader file preloaded on every page |

**Why.** The owner's verdict on the fonts is right for measurable reasons (`TYPOGRAPHY` §1): the hero H1 is the brand name in capitals set in a *newspaper* text face at weight 300 on navy — a thin, editorial line where the brand needs a monumental one; IBM Plex Sans is what almost every tool proposes for «institutional» (UI-UX-Pro-Max returns it as «Financial Trust» for banks) and its pairing with that serif produced «an administrative portal with an elegant font»; 356 KB of fonts on the home, ≈ 509 KB on the Arabic entrance; two Arabic registers. Source Serif 4 at 400 gives the most monumental version of the locked line on the board, in a transitional book register (institution, not newspaper); Host Grotesk is a 2024 grotesque with tabular figures and the `case` feature, a product register (not IBM, not Inter). Both declare no Reserved Font Name.

**Usage map.**

| Surface | Serif (Source Serif 4) | Sans (Host Grotesk) | Mono | Arabic (`:lang(ar)`) |
|---|---|---|---|---|
| Portico | every public page H1 (the project page's H1 is the name, so it takes the wordmark face); section titles (`--t-band`); **the hero's promise line** (the locked subtitle, as display); the hero lead (italic); Forum and Academy **public** titles; the Forum pull quote — *only these* | eyebrows, navigation, mega-menu, body 17/28, door titles 22/28 600, cards, buttons, chips, notices, forms, footer | folio references, programme meta | Markazi for the serif roles ×1.15; Vazirmatn for the rest; no italic, no uppercase, no tracking |
| Entrance (login) | the one H1 | everything else | — | idem |
| Console | **never** (Academy included — it leaves the serif) | everything | references, hashes, counters | Vazirmatn only |

**Scale.** Portico: `--t-display` clamp(40 → 72 px)/1.0 serif 400 (the promise line) · `--t-engraved` 32 → 40 px, the name in the wordmark face (the hero H1) · `--t-interim` 28 → 32 px (the interim title on phones) · `--t-plate` 48/52 · `--t-title` 38/44 · `--t-band` 30/36 · `--t-entry` 22/28 sans 600 · `--t-lead` 20/28 serif italic · `--t-body` 17/28 (≤ 65 ch) · `--t-ui` 15/20 500 · `--t-small` 14/20 · `--t-caption` 12/16 500 · `--t-folio` 13/16 mono. Console: unchanged from DS V4 (28/36 · 20/28 · 17/24 · 15/24 · 14/20 · 13/20 · 12/16 · eyebrow 11/16 · numeral 28/32 · ref 13/20 mono). One lever is reserved if the 1× 1366 × 768 laptop test finds the 13 px meta weak: `--u-small: 13.5px` — not a face change. Arabic: display ×1.15, body line-height 1.75 (public) / 1.7 (console), Western digits everywhere.

**The name, one drawing** (`RED_TEAM` M1). Wherever the trademark name is rendered — the lock-up, the hero H1, the project page H1 (`{% brand %}`), the footer's legal line, the console rail — it is set in «ILE Wordmark», in capitals with the lock-up's tracking (CSS `text-transform`; the text content stays the locked string, so no lower-case glyphs are needed — a mixed-case subset would cost +1.03 KB, measured, and is not proposed).

**The hero H1.** `p3.hero.title` is locked as «ITALY LEGAL ENTRY™»; its typeface is design. The council set it in Source Serif 4, 40 px under the Newsreader lock-up: the same words in two serif drawings in one viewport — the most visible «two authors» signal on the most important screen. **D-U1 option a is therefore the recommendation, in the wordmark face**: the H1 keeps its element and its locked text and is set as an engraved line of 32–40 px in «ILE Wordmark» (600, tracking .08 em, paper on night); the locked subtitle becomes the display statement in Source Serif 4 400 (40 → 64 px), so the eye reads the promise, and the name reads as the lock-up made large rather than as a second typeface. If gate 0 shows the `opsz` 20 outlines coarse at 32–40 px, the `opsz` 36 instance ships (+1.70 KB). *Option b* — the name as the 72 px display line — stays the owner's choice, in the same face with its `opsz` 72 instance (1.71 KB, measured); the typography lane found 600 at display size heavy, which is why option a is recommended.

**The wordmark.** The owner has not authorised removing the wordmark font, and V5 does not. It changes only the *delivery*: the 1.71 KB «ILE Wordmark» subset is pixel-identical at 20 and 14 px (`TYPOGRAPHY` §7). The outlined-SVG route (A2) removes the font and is **not adopted**; it stays available if the owner ever asks for it. Every class that renders the name (`.lock__wm`, `.rail__wordmark`, the `{% brand %}` classes) reads `--f-wordmark`, never `--f-serif` — which `body.console` re-points to the sans, so today's rail would fall back to the wrong face (`RED_TEAM` m10). The lock-up text hides only below 21.5 rem (344 px) instead of 23 rem, so the brand name is visible on the common 360 px Android width (`MOBILE_UX` §6.1, measured: lock-up 20–247 px, Menu button 294–340 px, no horizontal scroll).

**Setting rules.** French spacing with U+00A0 before `: ; ! ?` and inside « » (Host Grotesk lacks U+202F) — a content rule with a test over templates, `locked_content.py` and the `.po` files (0 occurrences today). Tabular figures on every date, count, reference, amount. `font-synthesis: none`. `text-wrap: balance` on titles; line-height ≥ 1.1 on any line of accented capitals. Sentence case for every non-locked title; locked capitals stay capitals and read as engraving once the design stops adding uppercase elsewhere (`UX_PUBLIC` §2.5). Serif 400 only (300 retired); sans 400 body, 500 controls, 600 titles ≤ 28 px, 700 only for `<strong>` in public prose.

**Loading.** `font-display: swap` with metric-matched fallback faces (`size-adjust` / ascent / descent computed against Arial, Segoe UI, Georgia, Times New Roman, Tahoma — `TYPOGRAPHY` §9.4). Preload: Host variable everywhere; Source Serif 4 roman on public templates; Vazirmatn (+ Markazi) on `/ar/`; nothing else. Per page (production-shaped builds): home 73.7 KB (today 356.1), console 29.3 KB (≈ 214), Arabic home 81.6 KB (≈ 509).

**Risks the owner should know.** Two serif families still share the public pages — the name in Newsreader, titles in Source Serif 4 — but never the same words: the name is always the wordmark. Host Grotesk draws I and l alike: references and IDs stay in Plex Mono, and the gate looks for a real Italian case. The Apple and Android fallback metrics were not computed (no such fonts on this machine) and must be before the fallback faces ship. The Arabic pair needs one review by a Moroccan reader, **blocking** for `/ar/`: Vazirmatn's letterforms come from a family drawn for Persian, and Noto Sans Arabic is kept as the fallback candidate if the reader finds them foreign (`RED_TEAM` m17).

**Owner decisions:** T1 pairing A (recommended) or B (Newsreader re-set at 400 `opsz` 72 + Public Sans); T2 Vazirmatn + Markazi after the Arabic reader review (blocking); T3 the Forum quote in Source Serif 4 italic; D-U1 above — option a, in the wordmark face.

---

## 3. Colour and material — «carta, notte, laguna, oro»

**Decision: `COLOUR.md` is adopted as the colour system**, with the five rulings below. Its proof is computed from the CSS file itself (`scratch/colour/verify_tokens.py` → 363 pairs, 0 below their minimum). The pairs the red-team revision changed (`conforme` in ink, the flat and paper-plate primaries, the night plate) were computed separately (§26.6); F2 re-runs the full check on the amended file.

**The materials** (unchanged hex for everything V4 measured and shipped; V4 names become aliases):

| Material | Role | Key steps |
|---|---|---|
| **carta** — paper | pages, areas, sheets, disabled, rhythm lines | 0 `#ffffff` · 25 `#fbfaf8` · 50 `#f4f3f0` · 100 `#ecebe6` · 150 `#e3e2dd` · 200 `#d3d2cc` |
| **inchiostro** — ink | text 1/2/3, structural edge | 900 `#15222a` (14.62:1 on carta-50) · 600 `#4a5a62` (6.46) · 500 `#55646b` (5.48) · 400 `#7a868b` (3.37, an edge) |
| **notte** — night, from the brand navy | dark chapters, rail, footer, tooltips, hero | 950 `#071226` · 900 `#0b1a33` · 850 `#10233f` · 800 `#16304f` · 700 `#1d3b5e`; text 50 `#eef1f6` · 200 `#b9c5d6` · 400 `#8a9bb3` |
| **laguna** — the one interactive accent | links, primary, current location, focus, selection | 700 `#0f6a72` text · 800 `#0b555c` hover · 650 `#12777f` mark · 550 `#1d8a93` focus ring · 400 `#7fd1d8` on night · 50/100 washes |
| **oro** — the key | the seal glyph, identity on night, **the travelling light** | `--brand-gold #c39a2b` (5.80:1 on brand navy; 2.37:1 on paper = ornament only) · `oro-300 #dfc176` text on night (9.94:1) |

**Seven chromatic state tones and one ink register** (`COLOUR` §6.1, amended after the red team) — *conforme* in **ink** (inchiostro-900 mark and word on a carta-100 body: 13.59:1; OKLCH chroma 0.024, under the 0.03 ceiling the new test sets), *esame* wisteria (new: in someone else's hands), *deposito* slate (neutro), *ambra* (attesa, due not late), *cotto* terracotta (azione: you must act now), *granata* garnet (rifiuto), *grafite* (new: blocco, a dependency), *cenere* ash (nullo). The lapis *registro* tone stays in the system for one use — the **information notice** — and never paints a state. Each chromatic register has eight steps (body, hover body, edge, mark, word, night body, night word, night mark), frozen as hex (no runtime `color-mix()` for a state). The marks form a luminance ladder (3.13 → 9.08 on carta-100, and conforme's ink mark at the dark end), which is the second channel for a greyscale reader.

**ECD rulings.**

1. **Two shells of one family — adopted (owner D1).** Public: page carta-50, sheet carta-25. Console: page carta-25, sheet white, night chrome unchanged. Same primitives, no new hex; every pair re-checked on white. It is the cheapest premium move in the system: the console stops looking like a public page with a sidebar and reads as a working desk.
2. **VALIDE stays ink — the repository's rule is the default** (`RED_TEAM` B1; the council's lapis, owner D2, is withdrawn as a recommendation). The council proposed lapis with a filled disc and a check. The repository already states and tests the opposite: `tests/frontend/test_chips_registry.py` («`conforme` must take the chapter's ink — no chroma — because no colour on this platform ever means approved») and `test_v4_tokens.py::test_no_register_is_painted_with_the_verdict_green_or_the_accent`. A blue filled disc with a check is the universal «approved» sign whatever a footnote says, and presenting it as «adopted, legal to confirm» inverted the burden. So `conforme` keeps V4's ink, gains no check, and green still leaves the system (`--ok-*` deleted). The word stays the model's «Valide» (§12). If the owner and legal still want lapis, they sign it in writing **before F4** and `test_chips_registry.py` changes in the same commit, carrying the signed wording (O14).
3. **Two new registers, `esame` and `blocco` (owner D5, D8).** EN EXAMEN was invisible (same colour as DÉPOSÉ); BLOQUÉ shared a register with MANQUANT. The mapping is data in `apps/core/chips.py`; templates do not change.
4. **Retirements with a one-release shim:** the green `--ok-*`, the bronze seal, the pending brown `#705434` («mud»), the crude `--err-700 #b3261e`, the V1 papers and navies, and the shim that paints 42 «accent» sites in a red — each of those 42 sites is looked at, not re-pointed blindly.
5. **Audience accents live on night and on photographs only.** The four V4 route colours (`--route-1..4-dark`, measured on notte-900) become the audience accents (§10). They appear in the hero legend and in the audience micro-visual, which always sits on the audience's photograph. No paper version is introduced: a ninth to twelfth chroma on paper would compete with the state tones. Persona's route colour equals the interactive night accent (`#7fd1d8`), a V4 choice: Persona reads as «the default» audience and as a link. **Recommendation (O19): shift it** to a warm sand, `#e6cdb0` — 11.34:1 on notte-900, OKLab ΔE ≥ 6.5 from every night state word and 7.0 from `oro-300` (computed in this revision) — the person warm, the three organisations cool. It is judged in gate 0 beside the gold of the key; if the two compete, Persona keeps V4's colour. **On paper there is no audience colour at all**: the phone list «Quatre accès» draws its glyphs in ink, not in route colours (`RED_TEAM` m4).

**Depth, glass, scrims.** Five depths on paper and five on night (V4 levels, renamed by function). **Glass only on the sticky bars** (the letterhead and the console context bar) — never on content, never behind a sheet, never animated (`RED_TEAM` M3, m5). The hero legend, the login's night panel and the audience micro-visual become **solid night plates** (notte-900 at .72, no `backdrop-filter`; a notte-50 glyph on that plate measures 6.16:1 even over a white pixel). Scrims are opacity only, with no blur at any width (a full-screen blur is costly on low-end Android). The V4 mesh stays in the hero only; the other night chapters are flat notte with the 3 % grain. Text on a photograph needs `--scrim-photo-aa` (notte-900 at .64) or a solid night plate; V4's `--grad-photo-dark` (.45) fails AA on a white pixel and is retired as a text ground. Night is a set of contexts (hero, passage, rail, footer, tooltips, login panel), not a theme: V5 proposes no dark mode.

**Focus.** One ring: laguna-550, 2 px, offset 2 px, 30 % halo on paper (≥ 3:1 on every ground); laguna-400 on night; a two-tone white/notte ring on photographs.

**Icons take one of six semantic colours** and never a brand colour; a status glyph is painted by its chip, never by the template (`COLOUR` §8).

---

## 4. Iconography — one hand

**Decision (`ICON_SEMANTIC_MAP`, amended).** The ILE sprite stays the product; **Lucide (ISC)** is the single donor of geometry for the ≈ 60 glyphs the vocabulary lacks; Phosphor is used only as a thesaurus; two libraries never mix. Every glyph — ILE or donor — takes the ILE treatment from one CSS rule: 24 grid, **1.5 px effective stroke at every size** (stroke-width per size class: 14 → 2.57, 16 → 2.25, 20 → 1.8, 24 → 1.5, 32 → 1.25, 48 → 1.0 — today a 16 px icon renders a 1.0 px line), **square caps, miter joins**, and a **12 % `currentColor` tone** inside the main shape of *concept* glyphs only. Under that treatment the «shadcn/Linear» look disappears: that look *is* the 2 px round stroke.

**Three tiers.** *Identity* (drawn from the mark, never toned, never mirrored): `ile-arch`, `ile-key`, `ile-steps`, `ile-mark`. *Concept* (audiences, actors, domains, phases — may carry the tone; reach templates only through the registry `apps/core/icons.py`). *Utility* (actions, direction, feedback — monoline, never toned).

**One concept, one glyph** — today 19 of 32 live symbols carry two or more unrelated concepts (`briefcase` five, `shield` four, `menu` for both navigation and row actions, `home` for dashboard and housing, `lock` for reserved access). The final map (`ICON_SEMANTIC_MAP.md`) gives one glyph to each of ≈ 150 concepts and a test enforces the bijection.

**ECD amendments to the council map.**

1. **Statuses become «i cerchi».** The council's pictographic picks for the document states (`glasses`, `hourglass`, `ban`, `arrow-down-to-line`) are replaced by the colour lane's circle grammar, drawn as ILE glyphs: outline = open, filled = settled (MANQUANT dashed ring · DÉPOSÉ ring + centre dot · EN EXAMEN half-filled disc · VALIDE **filled ink disc, no glyph** — the entry closed in the register · NON VALIDE filled disc + × · EXPIRÉ filled disc + clock hands · À REMPLACER ring + two arrows · BLOQUÉ lock · nullo slashed dotted ring). The red team's alternative for VALIDE, a disc with a horizontal bar, is not used: it reads as «minus» or «no entry». Reason: one family legible at 14 px inside a 24 px pill in Arabic and in dense tables; open vs settled readable without colour; the same marks become the Piece Ledger's pips (§12). A status mark is always the *register's* mark; the word carries the precise meaning. **The check rule** (`RED_TEAM` B1): a check glyph (`check`, `circle-check`) appears only on the person's own interface acts — a ticked box, a chosen OptionCard, a filter chip, a field the server confirmed, an account confirmation — and never on a piece, a journey step, a case, an assessment or any state the platform produces; a test holds it.
2. **Every chip carries its mark**, neutro included — this overrides `badges.md` §4.3 (council Q2). A chip without a mark is the V4 illegibility the owner saw.
3. **`ile-crossing` is withdrawn.** The journey has two thresholds (§11): the jurisdiction threshold between steps 3 and 4 takes `stamp` («les autorités compétentes»), the arrival threshold before step 6 takes `ile-arch` — **the only arch in the journey**: step 6 takes `building-2` (its first formalities are with public services), step 2 takes `signpost` (the possible pathways) so no glyph repeats on adjacent stations, and step 5 takes `clipboard-list` (no check anywhere on the journey) (`RED_TEAM` M2, m2, B1). A «crossing» glyph at the first threshold would tell a person they have crossed when their visa procedure starts (`UX_PUBLIC` §2.3).
4. **Empty states:** a region's empty line has no icon; a whole-page empty state keeps one domain glyph in a 40 px disc (it says *which* space is empty).
5. **Guichet numérique = `concierge-bell`**, confirmed after a 20 px side-by-side with the notification `bell`; if the owner reads them as twins, `messages-square` replaces it.
6. **The arrow becomes a primary-CTA glyph** (80 calls → ≈ 30): secondary links are links.
7. **`ile-steps` is redrawn as a stair profile** — three treads and risers rising in one direction — so it can no longer be read as `menu` or `list-filter` at 14–16 px (`RED_TEAM` m1).

Sprite ≈ 109 symbols (31 ILE drawings kept, 4 identity glyphs, 8 status marks, `arrow-start`, ≈ 65 Lucide geometries), ≈ 9 KB gzip, one cached request, fixed boxes (no CLS). In the console the ≈ 12 rail and bar symbols are rendered server-side as an in-document `<symbol>` block so the rail paints with its glyphs (today it paints without them at fp + 250 ms — `UX_PLATFORM` D7); to be measured against a sprite preload.

---

## 5. Imagery and video — «due rive»

**Decision: `IMAGERY.md` is adopted as the image direction**, with the reconciliations below, revised after the red team. Architecture and craft carry identity; people carry credibility. Italy and Morocco meet through what they share. People work, listen, speak and learn — they never pose, never shake hands, never stand under flags, and are never duotoned. Stock never passes as documentary.

**Per section — one image, one context** (full matrix in `ASSET_USAGE_MATRIX.md`):

| Section | Image (slug · Pexels id · author) | Ratio(s) | Reuse · status after the red team |
|---|---|---|---|
| Home hero | **the owner's door** (unchanged, LCP) | stage | door: hero + login + error pages only. **The vault layer is dropped** (arches behind the door, a new LCP candidate, decoration — `RED_TEAM` M2, m15) |
| Persona | `personne-fenetre-dos` (7594198 · Mikhail Nilov) — the same shoot and window light as the council's pick 7594098, the man **seen from behind** at his desk: nobody identifiable is cast as an applicant (`RED_TEAM` M13) | 3:2 · 4:5 | door card, Persona panel, Persona landing |
| Impresa | `atelier-mesure-precision` (7180823 · Thirdman) | 3:2 · 4:5 | idem for Impresa; the craftsman's face is in frame — legal reading O55 |
| Istituzione | **replaced** — the Palazzo della Ragione loggia was an arcade and a named monument (`RED_TEAM` M2, M13). Recommended: `table-des-institutions` (6949366 · Werner Pfennig), an empty council table with microphones and blank name cards — **the Forum loop 6951299, from the same room, then leaves the Forum page**; alternative: `salle-deliberation` (32266781 · Héctor Berganza), an unnamed legislative chamber, after a full-resolution check for flags, insignia and identifiability (O60) | 3:2 · 4:5 | idem for Istituzione; the alt text names no building |
| Università – Formazione | `bibliotheque-salle-lecture` (9489906 · Yaroslav Shuraev) + `etudiants-echange-campus` on the landing body | 3:2 · 4:5 | idem |
| The passage (head) | **held for the F15 ruling (O54).** If arcades are ruled outside F15: `arcades-padoue-pluie` (38843185 · Konstantinos Kanavoura) with a Moroccan arcade to re-select — the Casablanca frame 34453419 is **rejected** (its shop shutters close shop entrances: an entrance, on a prudent reading). Otherwise, **the fallback «Lo stesso gesto»**, ready now: `main-cedre-ciseau` (30563520 · Moussa Idrissi — a hand guiding a chisel through a geometric cedar carving) \| `main-marbre-ciseau` (6713855 · Tima Miroshnichenko — a hand guiding a chisel on marble); alternates 30563521 (a zellige cutter's hands, cropped so the face leaves the frame) and 12148970 (a mosaicist in Soave, Veneto — a black-and-white original, so only as a monochrome pair) | 4:5 + 4:5 | only as a pair; passage + regular-mobility page; the Italian frame is not geolocated, so no caption names a place |
| Orientation | `carnet-page-blanche` (5357492 · Maria Mileta) | 21:9 · 3:2 · 4:5 | orientation pages + the console's «no case yet» empty state |
| Documentation (public guide) | `classeur-pieces-mains` (4792285 · Anete Lusina) | 3:2 · 21:9 | public guide only — never inside the console |
| Cooperation / network | `table-travail-institutions` (33543226 · Emre Gokceoglu) | 3:2 · 21:9 | cooperation + network (same message) + the home's ecosystem tile |
| Forum | `forum-prise-de-parole` (16856088 · Domingos Henriques) — Forum landing hero (the speaker's face: legal reading O55) · `marche-marbre-zellige` (35816354 · Hassan Bouamoud) — Forum band, Forum panel, home Forum teaser — **held under the same owner flag as the terrazzo steps** (steps are a threshold on a prudent reading, O54); fallback `table-mise-mains` (6787057 · Artem Podrez — hands around blank notebooks on a white table, from above: faceless, weaker) | 4:5 · 21:9 · 3:2 | Forum only; never captioned as the Rovigo event |
| Territory | `plaine-peupliers-brume` (10005316 · Serena Koi) | 21:9 | Forum lower band + «Le projet» |
| Professionnels | `relecture-document-professionnel` (9870135 · Ron Lach) | 3:2 · 4:5 | that page only |
| Formation / Academy (public) | `laboratoire-formation-technique` (9242821 · Mikhail Nilov) | 3:2 · 16:10 | Formation landing; default course cover until real covers exist |
| Vivre en Italie | `velo-facade-stuc` (8551130 · Aneta Zelenková) | 3:2 · 21:9 | that section only; the alt names no country |
| Login | the door alone; the terrazzo steps (17687058) are not proposed (O24) | 4:5 | login only |
| Mega-menu | each panel shows its own door's image (Forum: «la marche» or its fallback) as the panel's field (§7) | 3:2 @ 480 w | inside the context |
| Console | **no photograph** (dashboard, situation, dossier, documents, company, selection, guichet, back-office) — the exception is the «no case yet» empty state | — | — |

**Video — at most three narrative loops, none in a hero, none on the home.** `portique-lumiere-boucle` (video 36909064, an arcade, trimmed before the door that enters the last seconds) → the «Le projet» chapter band — **held with the arcades for O54**; `forum-table-panoramique` (6951299, full pan checked for flags) → the Forum page — **only if Istituzione does not take 6949366, from the same room** (O60); `atelier-plan-boucle` (7479048, wall lettering cropped) → the Formation / Academy landing. Contract (`IMAGERY` §4.4): `muted playsinline loop preload="none"`, poster = frame 0, played only at ≥ 64 rem, in view, without Save-Data or reduced motion, after idle; a visible 44 px Pause toggle (WCAG 2.2.2); no audio track; ≤ 0.9 MB each; no welding or grinding footage (flashes, WCAG 2.3.1).

**ECD reconciliations.**

1. **Home image budget: door + 8 below the fold** — the four doors, the diptych (2), the Forum teaser («la marche» or its fallback, 21:9), the ecosystem cooperation tile; news covers only when news exists. This is `UX_PUBLIC`'s count; `IMAGERY`'s «door + layer + 9» traded the diptych for a portico video poster and three news covers. The deviation from CD V4 §5.6 («porta + 5») is the owner's to sign.
2. **The vault layer is dropped** (`RED_TEAM` M2, m15; O21 withdrawn): it added arches behind the door, it would have become the LCP element (`IMAGERY` §7), and it was decoration.
3. **No video on the home.** The home already has its one live object (the hero's first breath, played once) and its scroll story (the passage). The portico loop moves to «Le projet», where nothing else moves — if O54 allows an arcade at all.
4. **No photographic fallback anywhere.** A news item without its own cover is a text row; `micro-conference` and the generic `hero` fallback of `apps/pages/services.py:371` are retired; the AGAMI page stops borrowing the Institutions image.
5. **Thirteen of the fifteen current Unsplash photographs leave V5 placements** — the twelve IMAGERY retires (authors unknown, four survive only through redaction, six say «people at a table with laptops», one is a high-five) plus `micro-conference` (ruling 4). They are retired, not rejected. `atelier-de-travail` stays for the pilot page only if its author can be recorded; `campus-universitaire` stays in reserve, unplaced.
6. **The door's photograph** is read by first-time visitors as the Trevi postcard (`UX_PUBLIC` §3.1). It is a locked asset: V5 changes its treatment, not the image — a navy vignette centred on the key (0 bytes), tested at 1440 and 390 (owner D-U2).
7. **The editorial rules hold, including their prudent reading — and the prudent reading applies until the owner rules** (`RED_TEAM` B2). `docs/IMAGE_LICENSES.md` lists «porte/soglie» and «griglie/cancelli» among the forbidden subjects, and its own precedents rejected a corridor because it «evokes grids/thresholds»; `IMAGERY` rejected a vanishing passage for the «soglia» reading and then selected two covered walkways, a flight of steps and a vault. The council's defence («arcades are not doors; shutters, not doors») is not a prudent reading. So: **no V5 photograph enters `CURATED` before the owner's written ruling on the scope of F15** — arcades, covered passages, steps, vaults (O54) — recorded in `IMAGE_LICENSES.md` §1; «la marche» takes the same owner flag as the terrazzo steps; the Casablanca frame is rejected; the fallback set in the table above is ready so the home never waits for the ruling. Fourteen full-resolution checks (text, logos, doors, flags) still precede any entry in `CURATED` (`IMAGERY` §5.8); the fallback candidates were seen in this revision only as ≈ 350 px Pexels previews (`scratch/ecd/revision/sheet_*.jpg`).
8. **People** (`RED_TEAM` M13). A person on an audience door is cast by the placement, whatever the caption, and the Pexels License carries no model release. The Persona door therefore shows nobody identifiable; Impresa and the Forum voice keep a face only after a legal reading, door by door (O55). The durable answer is **commissioned photography for the four doors**, as already foreseen for the Forum (O56): the stock set is an interim. No alt text names a real building or place the picture does not need.
9. **Studios.** Several picks come from the most-used Pexels studios (Mikhail Nilov ×3, cottonbro, Thirdman, Ron Lach). The one grade and the crops reduce the «stock» look; they do not remove it — another reason for O56. The Moroccan-reader review extends from type to imagery (zellige, lanterns and landmarks are mild cultural signifiers — `RED_TEAM` m12).

**Treatment.** One deterministic grade for every colour photograph (contrast +8 %, saturation −15 %, soft S-curve, blacks lifted toward notte-900, highlights +4 % warm); no teal veil over faces. Duotone (notte-950 → carta-50) only on two non-human layers: the night variant of the plain and, if the arcade loop survives O54, the portico poster on night. Four ratios (3:2, 4:5, 21:9, 16:10), each cut as its own derivative around a recorded focal point (`data-focus` → `.img--focus-*`, CSP-safe). AVIF q≈50 + WebP q≈72 at 480/800/1200/1600 (+1920 for 21:9), explicit dimensions, no LQIP, a paper or night placeholder class from the manifest's average colour. Cards: radius 14 + passe-partout hairline, text below the image, never on it. The arch shape masks only the door (hero, login, error pages); the council's arch-shaped reveal at the passage threshold (D-U7) is withdrawn (`RED_TEAM` M2).

**Micro-visual per audience** — the actor glyph in a 36 px solid night disc (notte-900 at .72, no blur) plus a 3 px rule in the audience accent, at the image's bottom-start corner (moves to the right in RTL). One signature, four places: the door card, the mega-menu panel, the landing hero, the hero legend.

---

## 6. Motion system and the branded loader — «la chiave che gira»

**Decision: `MOTION.md` is adopted as the motion system** (five laws, tokens, twelve patterns, the loader, the journey, the performance rules), with the rulings below.

**The five laws.** (1) Function first: every animation declares its function (orientation, hierarchy, causality, state, feedback, depth, delight) or does not exist. (2) **Nothing painted is taken back** — three legal entrance classes: *A additive* (light drawn over a complete composition), *B pre-state before first paint* (never on text, the LCP element, `<main>` or the first viewport — and armed only for a fresh navigation without hash, because a restored scroll kept the pilot steps hidden 1.0–1.3 s, `MOTION` §5.2), *C scroll-linked with identity at zero*. (3) Motion is material: gold light moves only where the brand moves, in three contexts; laguna moves for the interface; **the tricolour never moves**; the mark's key turns once, at the entrance; the wordmark never moves. (4) One speed ladder, asymmetric, interruptible; state is set before motion. (5) Reduced motion is a complete still state; RTL mirrors only direction.

**Tokens** (kept V4 values + four durations, three curves, three springs with CSS `linear()` twins): feedback 120 · state 200 · space 320 · story 480 · draw 900 · route light 1200 (+ 400 stagger) · stagger 60 · key 1200 · door 1600 · luce 2200 · wait threshold 400 — the 28 s ambient token is retired with the hero loop; `--ease-enter/exit/layout` + `--ease-turn-in/turn-out/sine` (loader and light only); SOFT 260/30, SNAPPY 400/40, SHEET 200/27 (ζ 0.93–1.0: no overshoot anywhere). Per-keyframe easings are written as literals (a `var()` inside `@keyframes` silently ran linear in Chrome 153) and a test enforces it.

**The loader — one sign, four levels, a strict scope** (revised after `RED_TEAM` M2, M3, M10, M19). **L1 «Porta»** — the mark (or its door at stage scale): the key makes two half-turns with a detent while the gold light runs the door frame, **once** (1600 ms), then rests on the verbatim mark; **the tricolour planes never move and no crack of light opens** — a door that unlocks while a legal answer is being computed would promise an outcome («Aucun résultat administratif n'est promis»). L1 lives in one place: **the entrance stage on submit** (login, sign-up, reset, verification). **L2 «Chiave»** — the key alone in `currentColor`, 1200 ms, in busy buttons and row statuses; it is the loader of every other wait, and the only one allowed on **outcome-bearing** requests («Enregistrer et recalculer», the pre-assessment, eligibility, scan verification), which `loader.js` lists and a test checks. **L3 «Luce»** — a static skeleton for its first second, then one light across the whole sheet, for regions awaiting a fragment (preview drawer, notifications, «Aller à…», search), with the L2 key and a word in the region head instead of the council's 24 px door. **S «Filo»** — the navigation thread (the council called it «Soglia»; renamed so «La soglia» names only the concept and the journey, `RED_TEAM` m13): a 2 px laguna thread on the header edge from 400 ms after a click; the header mark and the rail tile stay still. **Four timing rules:** nothing before 400 ms for a generic wait (150 ms for an in-page action; 0 ms for a submit); content never waits for a cycle; ≥ 480 ms once shown; at 10 s the key stops, the words change («C'est plus long que d'habitude.»), a «Réessayer» appears. **Never full-screen.** The gold sweep is the *composited* dash (three clipped, transformed pieces) because the SVG `stroke-dashoffset` version froze during a 300 ms main-thread block — and a loader is shown precisely when the main thread is busy (`MOTION` §6.14: 27 positions in 27 frames vs 2 in 13; ≈ 97 % fewer paints). **L1 is a singleton**: `loader.js` serves a second L1 request as L2/L3 (the stress pages produced 51–67 ms tasks with several L1 at once); a unit test and a gate trace with every async region open hold it.

**ECD rulings.**

1. **The home's first breath is the light, not the key.** After LCP the gold light runs the arch once (900 ms, class A, the composited dash on the arch's own geometry). The key does *not* turn on the home: in V5 the key turns once, at the entrance. This overrides `UX_PUBLIC` §3.1 H7 and keeps one gesture per page.
2. **The hero current becomes four lights that travel once** (`MOTION` D10, amended by `RED_TEAM` M5). After the arch light, four short lights — one per route, in its audience colour — leave their legend rows once, 400 ms apart, 1200 ms each: the first breath ends in ≈ 3.3 s, then the stage rests. Nothing loops, so WCAG 2.2.2 needs no pause control, and the painted dash that cost ≈ 30 % of the main thread under CPU ×4 is gone. The keyframes are generated **at runtime from the measured path** — `getTotalLength` / `getPointAtLength`, twelve samples per route, once per layout, in an idle callback after LCP — and played with WAAPI on `transform` / `opacity` (CSP-safe), because `home.js` re-measures and rewrites the four routes at every width, in RTL and on font or legend changes, so build-time keyframes would leave the drawn routes. If the hero is off-screen or the tab hidden, the sequence waits and plays once when visible. Prototyped and traced in phase 0 and built in F6, before S1; if the sampling ever shows as a long task, the route geometry is frozen instead.
3. **The mark's key turns once, at the entrance** (owner decision O1, reworded after `RED_TEAM` M10). `BRAND_ASSETS.md` §1: «Il marchio in V2 è fermo; se si muove, si muove una volta, all'ingresso, con transform/opacity». The login stage's one-shot is that sentence taken literally, so the brand rule needs no amendment; O1 asks the owner to confirm the reading. If the owner reads §1 as forbidding even this, L1 is withdrawn and the login keeps the arch light and the L2 key in its button. Any loop of the mark, or any other L1 context, would need §1 amended first, in writing, before F5.
4. **View Transitions on the public site only**, new root 120 ms + 8 px rise, **off by default** and enabled only if the 6 + 6 re-measure at 120 ms keeps the destination LCP within +100 ms (measured +90 ms at 180 ms; 120 ms not measured yet — `RED_TEAM` m14). The console keeps the thread alone — a person working a dossier wants the next page, not a transition.
5. **The journey runs on native scroll-driven CSS** (0 bytes of JS for the home route; measured 12 paints, 0 dropped frames over the whole range vs 55 paints / 24 dropped frames today) and, in the console, as one WAAPI animation per load.
6. **Busy buttons keep their label** (V4's transparent label is retired, `MOTION` D8); the 10-second copy enters the locked-text registry in four languages (D7); **the `motion/mini` swap and the move of the two scroll-linked effects (the door drift and the stage settle) to native CSS happen in F6**, before any flagship step (`RED_TEAM` M9): −16.6 KB gz on every page, measured on the probes; the rail indicator moves to a CSS `linear()` spring. Trade-off, stated: browsers without scroll-driven animations (Firefox release, per secondary sources) show those two effects in their still state.

**Performance rules.** Transform and opacity only (`stroke-dashoffset` and `offset-distance` are measured *not* composited in Chrome 153); `will-change` only while moving; no animated `filter`, `backdrop-filter`, `box-shadow`, `width/height`, `top/left`; infinite animations pause off-screen and on hidden tabs; one live object per page; the chrome never moves on navigation. Weight: public JS ≈ 36.0 KB gz today (measured) → ≈ 19.4 KB gz after the F6 swap (36.0 − 16.6, from the probes) → an estimated 25–28 KB gz on the home with V5's additions (the loader 2.5 KB measured; the hero lights, the journey, the toast, the drawer and the panel morph estimated; search and «Aller à…» load on first use); CSS: the motion layer ≈ 8 KB gz measured on the prototypes, less with the level route (§11). CI tests per page type fail above 45 KB gz of JS and above 45 KB gz of `dist/main.css` (`IMPLEMENTATION_PLAN.md` §3.1).

---

## 7. Public navigation — «Letterhead → lintel» and «Il portico si apre»

**One surface gesture for the whole public chrome:** the letterhead extends downward as a single paper surface — for the mega-menu, for search, for the language thumb — never as a popover floating under a trigger (`21st_nav-shell` §4.1). The catalogue supplied mechanics (#31723 bar-and-panel as one surface, #31509 hover-intent and viewport timings and the only complete keyboard model, #21349 direction-aware swap, #27428 scroll states); the look is ILE's.

**Information architecture (owner D-U3).** Top row: the four doors, equal — *Personnes · Entreprises · Institutions · Universités & Formation* — a hairline, then *Forum · Projet*. «Actualités» moves into the Projet panel and returns to the top row only when there is a publishing cadence. **Every door has a panel with the same anatomy, or none has one** (today two of the four doors have none). Six items plus the separator measure ≈ 780 px, so language and access stay in the utility bar.

**The letterhead.** Paper, full width, 64 px → 56 px glass on scroll (existing sentinel; never hides on scroll-down; never a floating capsule). The lock-up stays verbatim (it scales as one unit 38 → 32 px on scroll). One 2 px laguna indicator slides to the hovered/focused item and, on click, stays on the clicked item until `pagehide` — the bar goes where you go (`MOTION` §5.6). The end zone holds the search button and, at most, one secondary.

**The utility bar made useful** (32 px, night): promoter at the reading edge · while `forum_banner` is on, the next dated rendez-vous as a quiet link («Forum Vénétie–Maroc · Rovigo, 2 octobre 2026») · «Espace réservé» with the `ile-key` glyph (never `lock`, which means BLOQUÉ in V5) · the language codes with visually hidden autonyms; «ع» in the Arabic system face with its own baseline.

**The portico panel** (mega-menu), recomposed after the red team so it no longer reproduces the reference site's «featured image card beside a serif blurb» (`RED_TEAM` M12). Inset 16 px from the viewport edges, `--radius-xl` bottom corners, shadow L3, the header's bottom hairline continuing into its top edge. Grid 8 | 4:

- (a) **the head line**: the door's locked gloss in serif 22/28, rendered from the registry (never retyped), ending with the panel's only arrow link «Voir l'espace»; below it, up to six sub-links in two columns — glyph + title 15/24 500 + one-line description 13/20 text-2, 52 px rows (needs a `description` field on child `MenuItem`);
- (b) **the door's own photograph as the panel's field**: the full panel height at the inline end, bleeding to the panel's edge (radius only on the outer corners), no caption, no text, no card frame; it cross-fades to a sub-link's image on hover or focus only when that sub-link has one (needs `image` + `image_alt` on `MenuItem`);
- a foot line: the anti-fraud entry as **one line** — the `shield-alert` glyph and a link to the anti-fraud page. The full «il gradino» lives once per page, elsewhere (`RED_TEAM` M14).

A scrim of notte-950 at 32 % (opacity only, no blur) appears only when the panel is opened by a click, a tap or the keyboard — never on a mere hover (`RED_TEAM` m8).

**Behaviour.** Hover-intent opens after 120 ms and closes after a 250 ms grace, on `(hover: hover)` devices only; click, Enter or Space on the disclosure button, and tap on touch. The existing keyboard model is kept (arrows between sections, ↓ into the panel, Esc closes the innermost layer and returns focus). Switching sections never closes the panel: content cross-slides 16 px in the reading direction and the height morphs (Motion `animate`, `SPRING_SOFT`). Open 200 ms `--ease-enter` (opacity + 8 px + clip from the bar edge), items stagger 30–40 ms (≤ 6), close 120 ms; reduced motion: an 80 ms opacity. WCAG 1.4.13: hoverable, dismissible, persistent. Panel photographs are **prefetched at idle, after LCP, at low priority, from 80 rem only** (`requestIdleCallback` + `fetchpriority="low"`), and fade in on load if a panel opens before they arrive — no pop-in on slow 4G, 0 LCP cost (`RED_TEAM` m8).

**Search inside the portico** (`21st_nav-shell` #31184 gesture, #11338 ARIA, #29989 zero state). A search IconButton at the end of the header morphs into a 44 px field; results open in the same panel surface, grouped by door. Index: a static JSON per language built at deploy (title, section, audience, URL; FR/IT accent folding, Arabic normalisation), fetched on first focus. The zero-result state offers the four doors and the questionnaire. The «/» shortcut works only outside fields and can be turned off (2.1.4). *Needs a build step — owner/dev decision.*

**The mobile drawer** — a native `<dialog>` from the reading edge (320 ms, scrim opacity only), rebuilt in the order people use it (merging `MOBILE_UX` §6.3 and `UX_PUBLIC` M1): a compact language row → the four doors as 64 px rows (glyph disc + word + one-line description) → a separator → Forum (with its date) · Projet → a search field → the one primary action («Découvrir le questionnaire d'orientation») → the anti-fraud entry as one line → at the foot, «Espace réservé» as a sticky bottom button in the thumb zone, and the promoter line. Sub-levels are exclusive `<details name="nav">` whose opened summary stays pinned as a header (#22313's layout — its per-character label animation is rejected: it breaks Arabic letter joining). The button reads «Fermer» while the drawer is open (today «× Menu», D9). The drawer's navigation starts at y ≈ 73 instead of 278 and fits in 743 px at 360 × 800 without scrolling (`MOBILE_UX` §6.3).

**Principles, not elements, from the reference sites** (`RED_TEAM` M12). The red team found three V5 elements close to agamieuromed.org, the promoter's own site: the gold-hairline tracked eyebrow above a serif title, the panel's «featured card», and the drawer's anatomy. The first two are changed (the section grammar in §20, the panel above). The drawer's order is dictated by use — the language first for a multilingual public, the four doors, the primary, the reserved access — and stays, but every public chrome surface passes a **side-by-side differentiation review** against `captures/ref_agami_*`: at gate 0 on the comps, then at the S1 and S2 gates, signed by the design reviewer, on six criteria — the section-header device, the eyebrow's typography, the panel's anatomy, the drawer's anatomy, the band alternation, the colour pairing. Navy, paper and gold are the owner's brand (the navy door, the gold key), not a borrowing; the other five criteria must read as ILE.

**Long reads** get a 2 px progress hairline under the header (CSS `animation-timeline: scroll(root)`, no JavaScript) and a sticky «Sur cette page» index ≥ 64 rem with a real travelling marker (IntersectionObserver), a `<details>` on phones. The Forum's sticky sub-nav gets the mirrored `--mask-fade-end` instead of a cut label.

---

## 8. The app shell — rail, context bar, workspace, inspector

**The question the brief asks** — «global rail + context sidebar + top context bar + workspace, or better». **The V5 answer is «or better»: a labelled global rail + a context bar that carries identity, search and notifications + a workspace with an optional inspector that holds the context index.** There is no permanent second sidebar. At 1280 px a four-column chrome (rail, context sidebar, workspace, inspector) leaves the workspace too narrow for the subgrid document collection, and the only screens that need a context index (the case file, a course, a commission) already have an inspector column where it belongs. On phones: a top bar, a bottom bar and a `<dialog>` drawer.

**Global rail (night).** Open (248 px) from **80 rem**, not 90 rem; below 80 rem a **labelled compact rail** (80 px: glyph 20 + a short label 12/16 — 13/20 under `:lang(ar)`, where the council's 11/14 was illegible (`RED_TEAM` m3) — two lines at most, from a new `short_label` in `portal.services.navigation`), never icon-only by default — this is an occasional, multilingual, stressful product, not a daily power tool (`UX_PLATFORM` §3.1). The persisted choice still wins; the width transitions only after `is-ready` (a load-time transition produced CLS 0.19 in gate C). Groups with real semantics only: *Parcours · Dossier · Échanges* in sentence case 12/16 500; Academy becomes a plain entry after a separator. One travelling hover plate (#21517) and one **travelling indicator** that moves with `SPRING_SNAPPY` to the clicked item and stays until `pagehide`. Counters from real data only. **The identity moment:** the mark at rest on the rail tile, its gold key as drawn — and still: no light runs it during navigation (`RED_TEAM` M3; the thread says «loading»). That is enough identity — no arch in the workspace (V4 pillar 2 kept).

**Context bar (56 px, glass).** Breadcrumb (collapsing to «…» beyond three levels) · the page title and state chip condensing into the bar when the H1 scrolls away (CSS scroll-driven, IntersectionObserver fallback, #23562) · end zone: **«Aller à…»** (IconButton + Ctrl/⌘ K, the account's own permitted destinations; staff get dossiers by reference and queues — **never persons**, CR-03/CR-04) · **the bell** with a real count badge → notification panel (§16) · **the account menu with an identity header** (initials disc, full name, e-mail, account type and organisation, «Dernière connexion»; a «Changer d'espace» group when roles allow; the handle never shows) · the language control. `scrollbar-gutter: stable` removes today's ≈ 15 px jump of the bar's end items. The ≈ 12 shell glyphs are in the document so the rail paints complete.

**Workspace.** 12 columns, `--workspace-max` 1320 px, `--page-pad` 32 px; page structure ContextHeader → NowPanel → the page's collections; an inspector of 320 px at the inline end where the page has facts, a timeline and people (case file, company need, commission), with the **context index** in its sticky head (Maintenant · Pièces · Parcours · Intervenants · Suivi · Messages; `aria-current="location"`; a critically damped marker). Panels: only the NowPanel is raised (L2); lists are sheets (L1); feeds are flat on the canvas with a hairline spine — raising only what matters is how a quiet console reads as expensive.

**Phone (< 64 rem).** A 57 px bar (no duplicate ≡ — the bottom bar's «Menu» is in the thumb zone and the top-left tile returns to the dashboard) · a bottom bar of four destinations + Menu with one-line labels ≥ 12 px (short labels by copy review, e.g. «Accueil · Dossier · Pièces · Messages · Menu»), real-count badges · the page's action bar *replaces* the bottom bar when one exists **and carries the Menu control, 44 px, at its inline end — the same place as in the bottom bar** — while the primary action fills the rest; without it the case file and «Ma situation» had no way to the navigation (`RED_TEAM` M6; WCAG 3.2.3, 2.4.5); persistent chrome stays 57 + 61 = 118 px ≤ 120 at 360 × 800 (today 174 px on the case file) · the console drawer kept as built (the best mobile surface in the product). A test renders every console template at 360 × 800 and finds one control named «Menu» that opens the drawer.

**Continuity.** The navigation thread covers every wait; the chrome never moves; no page-enter animation (gate E: the console arrives complete).

---

## 9. The hero — «La porta»

The door is the one memorable object the site has; V5 makes the composition around it worthy of it and gives it one gesture.

- **The stage is unchanged**: the owner's arch, photograph, golden key and three steps on the night mesh with 3 % grain; the photograph gets a navy vignette centred on the key (owner D-U2) so the statuary reads as stone relief around a dark doorway rather than as a fountain postcard.
- **Composition.** Hero height `min(100svh − header, 820px)` on desktop; the copy block anchored to the lower third instead of floating in empty navy; the next chapter visibly peeks (≥ 64 px at 1440 × 900) — a fold hint made of content, never a pulsing arrow.
- **One selector.** The legend of the four audiences is *the* first-viewport choice, on a solid night plate (no glass): four 52 px rows (glyph disc + word), the gloss in the reserved caption slot on hover and focus; hovering or focusing a row brightens that route and dims the others to 40 %. The door does not change colour (the council's glow re-tint is dropped — `RED_TEAM` M3). The secondary CTA (a back-office field) stops ranking one audience: the Forum date until 2 October, then «Comment ça marche» (owner D-U11). The primary stays the locked «Découvrir le questionnaire d'orientation».
- **The routes become light, not wires.** The four hairlines stay drawn; the painted current that read as «network, fibre» becomes four short lights that travel once after the arch light and rest (§6 ruling 2). **Nothing loops.** The exits over the photograph are removed on every variant (they collide with the photograph and sit inside the arch in RTL).
- **The first breath.** After LCP, once, the gold light runs the arch (900 ms), then the four route lights travel (≈ 3.3 s in all, under the 5 s of WCAG 2.2.2). The key does not move. Nothing painted is ever hidden.
- **Type.** The locked H1 as an engraved line in the «ILE Wordmark» face; the locked subtitle as the display line in Source Serif 4 400 (D-U1 option a, §2); the lead back in serif italic (Source Serif 4 italic, 19.1 KB) — subject to the measurement in §22.1.
- **Interim and phase 3 share one composition**; only the locked words change — and the interim title gets its own setting (Source Serif 4 at 28–32 px, a one-line eyebrow), because its five lines are what pushes the interim hero past a phone screen (§19). No variant-only furniture.
- **Phone:** Solution A (§19). **Landscape phones:** the door beside the copy (`@media (orientation: landscape) and (max-height: 30rem)`).
- **Guard.** The door photograph stays the LCP element (preloaded, 42 KB); no other image enters the hero (the vault layer is dropped); CLS protected by the reserved `aspect-ratio` of the compact viewBox.
- **Rejected for the hero:** a video; the 21st «smooth scroll hero» exit in which the arch silhouette widens into a photograph (#2061 — the arch shape belongs to the door, and the page gets one gesture); WebGL and shader grounds; a liquid-metal button; any entrance that starts invisible; any infinite loop.

---

## 10. Audience identity — four doors, four signatures

Each audience has exactly one glyph, one image, one micro-visual and one accent, and they travel together wherever the audience appears: hero legend → mega-menu panel → door card on the home → landing hero → footer index (word only).

| | **Persona** | **Impresa** | **Istituzione** | **Università – Formazione** |
|---|---|---|---|---|
| Glyph (concept tier, toned) | `person` (head + shoulders; also the person actor and «vous») | `building` (also the company actor, «Mon entreprise») | `institution` (pediment + columns) | `university` (cap; also the training-body actor) |
| Image (one context) | `personne-fenetre-dos` — a man seen from behind at his desk by a window, deciding his own path (7594198, the same shoot as the council's 7594098; nobody identifiable — O23) | `atelier-mesure-precision` — a young craftsman measuring a part with a caliper (7180823) | `table-des-institutions` — an empty council table, microphones, blank name cards (6949366), or an unnamed chamber (32266781) — O60 | `bibliotheque-salle-lecture` — two students in a wood-panelled reading room (9489906) |
| What the image says | a person planning a regular path | the skill a company needs | institutions that deliberate — no named building, no arch | study, without the graduation-cap cliché |
| Micro-visual | glyph in a 36 px solid night disc (notte-900 .72) + 3 px rule, bottom-start corner of the image | idem | idem | idem |
| Accent (night / on photographs) | `--aud-persona` `#7fd1d8` (V4 route 1) today — **shift proposed to `#e6cdb0`** (O19) | `--aud-impresa` `#8fbfe8` (route 2) | `--aud-istituzione` `#aab7cc` (route 3) | `--aud-universita` `#a8cfc0` (route 4) |
| First two tasks on the door card (existing destinations only) | Commencer le questionnaire · Voir les huit parcours (`UX_PUBLIC` E2) | Signaler un besoin · Le projet pilote (`UX_PUBLIC` E2) | to be written by copy review: the space's first form + its landing | to be written by copy review: the space's first form + its landing |
| Landing hero | 4:5 image at the inline end, eyebrow with glyph disc, sentence-case serif title, lead ≤ 3 lines, primary within 560 px at 360 × 800 | idem | idem | idem |

Rules: the four doors are equal — no ordinals, no zig-zag ranking, no landform glyphs (retired: at 20 px on navy a contour is a smudge); the micro-visual never relies on colour (the glyph and the word carry the meaning); the accent never appears on paper (the phone's «Quatre accès» list draws its glyphs in ink); images are never shared between audiences. The exact wording of the tasks is a copy decision; the rule is that each points to a destination that exists (`safe_url`).

---

## 11. The Morocco → Italy journey — «La soglia», the signature component

**One component, three densities, one light.** The same seven locked steps (`portal.services.JOURNEY_STEPS`), the same glyphs and the same two thresholds on the public site and in the dossier, so that a person who reads the home and then signs in finds their dossier on the line they have already seen, their step lit and the light stopping at it. That is the strongest «coherent site and platform» move available, and it needs no new data (`UX_PUBLIC` §5.3) — but on the public side it needs D-U9 and G3, so until then the public line carries the four orientation steps in the same grammar (see «The state the public actually sees» below).

**The semantic fix: two thresholds, not one.** In `JOURNEY_STEPS` the side switches before «Procédures auprès des autorités compétentes» and «Préparation du départ», which physically happen *before* departure: «side» means jurisdiction, not place. So:

- **Threshold A — the competent authorities** (between steps 3 and 4): a vertical hairline with the `stamp` glyph and one short caption reused verbatim from the locked FAQ («Chaque décision appartient aux autorités»). The jurisdiction changes; the person has not moved.
- **Threshold B — the arrival** (before step 6 «Arrivée et premières démarches»): `ile-arch` at station scale — the only arch in the journey (step 6 takes `building-2`), and the only place outside the door's allow-list where the arch appears: where it means something. The council's arch-shaped photograph reveal at this threshold (D-U7) is withdrawn (`RED_TEAM` M2).

**The public passage** (a home chapter, DARK navy). The two-shore diptych opens it (§5). One **level** line runs beneath — the two shores at the same height, their names as words at the two ends («Maroc» at the reading start, «Italie» at the end), the two thresholds as vertical hairlines. The council's cosine route rose from Morocco, low, to Italy, high: a price chart, and an elevation between two partners who cooperate as equals — a reading a Moroccan visitor will make (`RED_TEAM` M4; `MOTION` §7.2 already forbade «a growth curve»). The line is **always drawn at low contrast** (today it is invisible until scrolled — D5); the gold light *lays* it as the reader scrolls (native scroll-driven CSS: a counter-translated window reveals the travelled line; on a level line the light needs only its x, so the bob box and most of the sampled keyframes go — the journey's 3.2 KB gz of CSS shrinks, to be measured); stations are 2 px rings that take a filled paper dot as the light passes and keep it — **no halo, no ring of light** (`RED_TEAM` M3). The locked line «Aucun résultat administratif n'est promis ni garanti» sits under the chapter title. Numerals appear only here. Below 64 rem it becomes a vertical spine with the light running down. It **mirrors in RTL** (it is a sequence, not a map — `UX_PUBLIC` §5.4 over `21st_hero-public` decision 6): step 1 at the right, Morocco's image at the right. LTR, RTL and reduced motion are re-frozen from the level geometry in gate 0.

**The state the public actually sees** (`RED_TEAM` M16). The seven-station passage needs the legal decision D-U9 **and** phase 3 — the V4 pilot section renders only while gate G3 is open (`build_pilot` returns `None` on 8770). So the **primary public design is the fallback**, designed, prototyped and gated as such, on the interim server: **the orientation passage**. Until D-U9 and G3, the passage and «S'orienter» are one chapter — the diptych, the level line, the light, and on the line **the four steps of the orientation**: on the interim, the four neutral steps of `content.ORIENTATION_STEPS` with the editorial note (as `pages/home/_orientation.html` renders them today); in phase 3 without D-U9, the locked `p3.persons.how_it_works` split verbatim on «→» (D-U4). No sides, no thresholds; the questionnaire's primary action under the line. The same line, light, station marks and type appear in the console rail, so the site-to-platform continuity holds in grammar before it can hold in content. The seven-station version is the **upgrade** after D-U9 and G3: the passage then becomes its own chapter again and «S'orienter» keeps its stepper. The S1 acceptance runs on 8770 first.

**The console rail.** Dashboard: horizontal; case file: vertical and descriptive (the date each step was reached, in mono); phone: a current-step card («Étape 1 sur 7 · Maroc · Votre situation et votre objectif · Vous êtes ici») with «Voir les 7 étapes» in a `<details>`. The travelled line is drawn once (class B, 900 ms, stagger 120); after LCP one light — a 26 × 10 px streak, laguna tail, gold head — runs from step 1 to the current node at 120 ms per segment, crossing threshold A on its way; on arrival the current node's 2 px laguna ring draws once (320 ms) — no widening halo (`RED_TEAM` M3). After an action advances the case, the next load runs the light over the new segment only: «you moved». Current node: laguna ring + a flat laguna-50 wash + «Vous êtes ici» in words; no pulse; **done nodes are filled ink dots with no glyph** — no check anywhere on the rail (`RED_TEAM` B1); a «Cette étape» disclosure shows the step's detail, the screen where its work happens, and what it waits on — real data only. In the console the thresholds are glyphs (16 px), not drawings (owner decision: a 16 px `ile-arch` at threshold B, which respects «no door in the dashboard»).

**Guardrails.** No ticks on stations and no «vous êtes arrivé» (no colour — and no shape — means approved). No aeroplane, ship, suitcase, dotted flight path, map, flag, percentage, pulse, growth curve: the line is level. The key never travels the route (the key is not a vehicle; the light is). Actors per step appear only when a signed mapping exists (`MOTION` D9): the mechanism is ready (the actor's glyph disc fades in as the light passes), the data is not. **Publishing the seven labels and their sides on the public home is a legal decision (D-U9)**; until it is signed — and until G3 opens — the home shows the orientation passage described above, which is the design the public sees first.

**Reduced motion:** the route fully lit, every station lit, the arrival dot lit, no light; the console rail with its current ring and wash from the first frame. **Forced colours:** strokes `CanvasText`, light and rings removed.

---

## 12. Document workspace and the status system — «I cerchi» and «Il registro»

The platform's central act — assembling one's pieces — is today its least designed screen (a bare file input on a V2 page), and its states do not read (grey pills differing by a 3–4 px gutter; a HealthStrip two-thirds full while its caption says «0 sur 3 validées»). V5 makes this the flagship of the console.

**Status «i cerchi» — the chip V5.** Pill `--radius-full`, 24 px (20 dense, 28 large); **1 px edge** in the tone's 200, drawn in the register's style (solid; dashed for *attesa*; dotted for *nullo*); body = the tone's 50; a **16 px circle mark** in the tone's 600; the word 13/20 500 in the tone's 800 (`conforme`: carta-100 body, ink mark and word — §3); after the word, for case states that carry a phase, a **3-notch micro-meter** (3 × 4 px dots, `aria-hidden`, the phase in a visually hidden span) — which retires the V3 external gutter and its tick that three of three observers filed as a bug (`UX_PLATFORM` §5.1). The register comes from Python (`data-register`), never from a template; a test fails any chip rendered without its mark.

| State (fr) | Register → tone | Mark | Pattern (strips, legends) | Why |
|---|---|---|---|---|
| MANQUANT | attesa → ambra | dashed ring | hatch | the shape of an absence, due but not late |
| À REMPLACER | attesa → ambra | ring + two arrows (kin of the *Remplacer* action's `refresh-cw`) | hatch | same register, its own mark |
| DÉPOSÉ | neutro → deposito | ring + centre dot | solid | a fact; the base line |
| EN EXAMEN | **esame** → wisteria | half-filled disc | solid | it moves, but not by you — finally distinct from DÉPOSÉ |
| VALIDE | conforme → **ink** (inchiostro-900 on carta-100, no chroma) | **filled disc, no glyph** | solid | the entry closed in the register; ink, as the repository's test requires (`RED_TEAM` B1) |
| EXPIRÉ | azione → cotto | filled disc + clock hands | solid | act now; a roof tile, not an alarm triangle |
| NON VALIDE | rifiuto → granata | filled disc + × | dots | the reason is printed on the row |
| BLOQUÉ (`ChecklistStatus.blocked`, `EvidenceStatus.blocked`) | **blocco** → grafite | lock | cross-hatch | a dependency, heavy and calm; the row says what unblocks it |
| retiré · sans objet · archivé | nullo → cenere | slashed dotted ring | outline | carries nothing |

The doc-row's Conditions gate (`action_blocked`) stays what V4 made it: a sentence and a link in the action column, not a chip. Every other producer in `chips.py` follows the same rule (every *in review / assigned / scan pending / in progress* → esame; every *blocked* → blocco). Status change: mark out 120 / in 200, word cross-fade, edge style snaps; one polite announcement per region; the row that changed gets the **cause bar** (2 px laguna at the inline start, in 200 ms, out over 2 s). **The seal** (navy disc, gold `badge-check`, 5.80:1) is reserved to acts of an authority — the project's own «Vérifiée» of a company loses it (owner decision).

**The word «Valide».** The owner's list says «VALIDÉ»; the model label is «Valide», and CR-11 explains why (the piece received is the piece asked; nothing is approved). V5 keeps «Valide», in ink. The council's colour specimens label the chip «Validé» and show other patterns V5 forbids: they are **non-normative** (§26, m6), and gate 0 produces the normative chip board.

**«Il registro» — the Piece Ledger** replaces the proportional HealthStrip where a dossier asks for ≤ 24 pieces, revised after the red team (`RED_TEAM` M11): one **16 px** status mark per requested piece (the chip's mark size — at 12 px the marks that separate rifiuto from blocco and attesa from azione were one or two device pixels at 1×), **grouped by who holds the piece** into three labelled runs with their counts — «À vous» (attesa, azione, rifiuto: the person must act), «En cours» (neutro, esame, blocco: someone else holds it), «Réglées» (conforme). **The colour of a mark is its group; its shape is its state**: «À vous» in cotto-600 (5.98:1 on white), «En cours» in ink-600 (7.17:1), «Réglées» in ink-900 (16.23:1) — three hues at most, so the row cannot read as a candy progress bar. (A MANQUANT chip is amber and its pip is terracotta, deliberately: the chip names the state, the ledger names who must act.) Withdrawn and not-applicable pieces (nullo) are not pips: they are counted in words. The caption stays the locked sentence («3 pièces demandées · 0 sur 3 validées · 1 en attente»), with the group labels derived from the same counts (copy review). Above 24 pieces the runs become counts only. `aria-hidden`: the words carry the meaning. Gate check: a colour-vision-deficiency simulation of the **rendered** ledger at 1× DPR, in gate 0 and at S7.

**The collection** (`portal/documents.html`, `documents/partials/register.html`). **Grouped by who must act**: «À vous de fournir» (open by default) · «Attendu d'un tiers» · «Déposées, en attente d'examen» · «Examinées»; each group header = glyph + title + tabular count; empty groups are not drawn. **CSS subgrid** so the columns align across rows (today the state column drifts from x ≈ 625 to 651 because each row computes its own tracks) with one `aria-hidden` header row (Pièce · État · Responsable · Échéance) and visually hidden prefixes per zone; «Sans échéance» in words instead of a floating «—». **The row is the target** of «Consulter» (a stretched title link that opens the preview); only the person's act (Déposer / Remplacer) is a button; the row menu (`ellipsis-vertical`, not the hamburger) keeps only what is not on the row (Télécharger, Historique des dépôts). **Filters show only states with a count > 0** («Tous» + non-zero states; the rest in «Autres états»), with a sliding thumb; on the phone they wrap and never scroll sideways with clipped labels.

**The preview drawer.** A native `<dialog>` at the inline end, 420 px (a full-height sheet ≤ 640 px): the piece page's `<article>` fetched as an HTML fragment from the same URL (`connect-src 'self'`, no new endpoint); while it loads, L3 in the body and the L2 key with a word in the head (no door: `RED_TEAM` M2); its footer holds the person's action, which opens the Dépôt inside the drawer; `history.pushState` to the piece URL so a reload lands on the full page; `popstate` (Back) closes the drawer and returns focus to the row's title (`RED_TEAM` m9). No inline PDF renderer (it would need CSP and security changes).

**«Dépôt» — the upload flagship**, built in layers so it never fails worse than today: (1) the native file input in a labelled field (no-JS baseline); (2) a dropzone that keeps the real input inside it; (3) client guards that mirror the server (PDF / JPEG / PNG, 10 Mo) — a refused file still gets a row with its reason; (4) a real `<progress>` from XHR upload events with bytes and a time left; (5) the row lifecycle in ILE words: «En file» · «Envoi — 1,4 Mo sur 3,2 Mo · ≈ 18 s» · «Vérification du fichier» · «Déposée — version n» (neutral chip) · «Refusée : raison» or «Envoi interrompu» + «Réessayer». **Filed ≠ examined:** the review verdict never appears here. Success: the filed state's own mark (ring + centre dot) draws itself in 240 ms — no check mark on a piece — a toast «Pièce déposée — version 2», the cause bar on the row. Engineering: the same CSRF and multipart endpoint plus a JSON branch; throttling surfaces as a sentence, not a 429 page.

---

## 13. Buttons — the signature CTA and the default system

**The default system** keeps the V4 matrix, cleaned and **flattened** (`RED_TEAM` M3): PRIMARY on paper is a **flat laguna fill** (laguna-650, white label 5.29:1) — no gradient, no inner light, **no glow**; hover and focus move the fill one step (laguna-700, 6.32:1), press one more (laguna-800, 8.51:1) and 1 px down — one per screen. **On night, the primary is a paper plate**: a carta-25 fill with an ink label (15.56:1; the plate against notte-900 16.64:1), hover carta-100 — the letterhead's paper laid on the night, instead of the light-cyan gradient that, with gold streaks and glass, read as a crypto wallet. `--shadow-glow` and `--shadow-glow-dark` are retired. SECONDARY, SOFT, GHOST, LINK, DESTRUCTIVE (garnet outline or soft; always opens a dialog that states the consequence), ICON (40 px visible, 44 px hit, a tooltip that repeats its accessible name). Sizes 36 · 44 · 52. Unused variants (`tertiary`, `quiet`, `inline`, the `large` alias) retire. What V5 adds is craft in the states: a **stacked-faces cell** (idle, busy, done and error share one grid cell, so the width never shifts — #23536), a **busy key** (L2) in the icon slot or end padding with the label kept and `aria-disabled` (never `disabled`: focus stays), a press that goes down 1 px at 0 ms and settles back with the `--spring-snappy` curve, and **one arrow per block** on the forward action only.

**The signature CTA — «Bordo d'oro» (the gilt edge).** Used only on night surfaces and at most once per viewport: the hero's primary and the «La porta riservata» band's primary. Anatomy: the paper plate, 52 px, with a **static** 1 px gilt hairline inset 3 px inside its edge (`--brand-gold`, an ornament: 2.52:1 on the plate) and a notte-950 outer hairline. **Nothing travels** (`RED_TEAM` M3): hover and focus darken the plate one step; the gilt edge stays still; reduced motion changes nothing because nothing moves. **Why not the liquid-metal button** the primitives curation evaluated seriously (`21st_primitives` §2A.1): its vanilla WebGL tier costs 8.3 KB gz plus a GL context on the page whose LCP is measured, it injects a `<style>` the CSP refuses, and — decisively — chrome metal is a 2025 catalogue signature. The council's own answer, a gold light sweeping a gilt rim on a glossy dark button, was the same signature in gold, and it is withdrawn with the glow. The CSS «chrome rim» tier is rejected for the same reason.

---

## 14. Cards

| Card | Anatomy | Hover / focus | Used for |
|---|---|---|---|
| **Navigation card — the four doors** | photograph + micro-visual, locked title / gloss / CTA, two task links above a stretched title link | image scale 1.02 (320 ms), the route rule draws once (480 ms), shadow L1 → L2, a 6 % pointer spotlight — **the only spotlight on the site** | the home doors only |
| **Navigation card — generic** (registry PX27, added after the red team) | hairline grid, glyph tile, title, one line, «link line» with an underline wipe | 2 px lift + shadow L1 → L2; never a scale | related spaces, services in the bento |
| **Feature card** | hairline grid, no link | none | explanatory content |
| **Media card** | image 3:2 on top with passe-partout, serif caption *under* the image, tabular date | image scale 1.02 | news (lead + rows), Forum recap |
| **Document card** | eyebrow «Pièce demandée» + chip → title → responsible glyph + due → one full-width action; menu in the footer | row press .99 | the collection below 48 rem |
| **Course card** | 16:10 cover *only* if a licensed cover exists (owner), otherwise a glyph tile; meter of notches; next-step row | lift | Academy |
| **Project card** | compact + milestone list (date · chip · title) | lift | Forum governance |
| **Actor card** | glyph disc (never a photo), role, one-line remit | none | tribune, contacts, «Qui intervient» |
| **Stat card** | eyebrow, numeral 28/32 tabular, one qualifier, link to the filtered list | none | company overview and staff only — never KPI tiles on a person's screen |

All cards: radius 14 (`--radius-lg`), hairline on paper (passe-partout for images), no border on night; the whole card is a target only when it has one destination; nested interactive elements sit above a stretched link and keep 44 px targets. **Rejected:** 3D tilt, cursor-following previews, the flex-grow door expansion (a hover-driven layout shift counts in CLS), a folder silhouette for the dossier card (the `folder` glyph already carries the case).

---

## 15. Tabs, modals, drawers, tooltips, popovers — one decision rule

| Need | Primitive | Trigger | Dismiss | Surface | ≤ 640 px |
|---|---|---|---|---|---|
| Name an icon | **Tooltip** (`role=tooltip`) | hover/focus, 400 ms delay | leave / blur / Esc | notte-800, radius 6, no arrow, logical sides | none (the label exists elsewhere) |
| Explain a term, a small interactive panel | **Popover** (Popover API; #23548 flip/clamp only where anchor positioning is missing) | click | light dismiss / Esc | paper L3, radius 14 | full-width |
| A list of actions | **Menu** in a popover: icon · label · shortcut, groups, destructive last after a rule, rows 36 px (44 px on coarse pointers) | click on an IconButton | light dismiss / Esc | L3 | bottom sheet |
| Confirm, consent, a short task | **Modal** `<dialog>`: pinned header and footer, one scrolling body, scale .96 → 1 + opacity 320 ms, exit 120 ms, a 1 px top-edge sheen | button | Esc / Cancel / close | L4, radius 20, scrim (opacity only, no blur) | bottom sheet with a grab handle |
| Side context (detail, filters, activity) | **Drawer** `<dialog>` 420 px at the inline end (320 ms, `SPRING_SHEET` for sheets) | button, row | Esc / close / drag on the grip (phones) | L4 | bottom sheet |
| True alternatives within a page | **Tabs** (#23570): measured indicator, invisible bold sizer (no width jump), ±12 px directional swap, roving tabindex | click / arrows | — | — | tabs wrap or become a `<select>` |
| Filters and views that are navigations | **Segmented control** of links with a sliding thumb | link | — | track carta-100, thumb white | wraps |

Always: focus moves in at t = 0 and returns to the opener; `inert` behind (native with `showModal()`); scroll lock with `scrollbar-gutter` compensation; no animated `backdrop-filter`; reduced motion = appear/disappear.

---

## 16. Notification centre and toasts

**Notification centre** — built on the existing `Notification` model (today absent from the UI). A bell in the context bar with a real count badge (18 px, tabular, width reserved in `ch`); a popover ≥ 640 px, a sheet below; tabs «Toutes · À traiter · Archivées»; **sentence-first rows** (the actor and the object emphasised, the verb quiet, a dim «date · contexte» line), the actor's glyph disc, unread shown by weight + dot (never colour alone); **actions resolve in place** (the row keeps «Vous avez répondu…»); repeats collapse with a count; «Tout est à jour» as the empty state. Preferences on `NotificationPreference` as switch rows with a visible state word. The Communications page becomes an inbox grouped by day with the same rows.

**Toasts** — rendered by the server from Django messages after POST-redirect-GET, so they work without JavaScript: bottom inline-end, 360 px, the front toast full and older ones peeking, expanding on hover/focus, 6 s with a pause on hover/focus, «Tout fermer». `role=status`; an error is never only a toast (the inline notice and the error summary remain). Success wording is neutral («Pièce déposée — version 2»), never «validé».

---

## 17. Empty states, skeletons and the loading contract

**Empty states — by scope** (reconciling the V4 dashboard doctrine «one hairline and one sentence» with DS V4 §8.30): an empty **region** yields its space to regions that have data and becomes one line in a quiet «Rien pour l'instant» strip — never a panel drawn at the size of a full one; a whole-**page** empty state is the EmptyState V5: the domain's glyph in a 40 px disc, a title, one sentence, **one action**. «No case yet» carries the orientation photograph (4:5, 240 px, lazy) and «Commencer», which stays in the console. Error variant: «Réessayer» + contact. A public section that would render empty (News in phase 3) is hidden (owner D-U13). The 21st «fanned ghost tiles» are rejected: they are a catalogue signature, not ILE's.

**Skeleton — L3 «Luce».** Shaped exactly like the content (final dimensions, CLS 0), visible only from 400 ms, **still for its first second**, then one light crosses the whole sheet (1400 ms, 800 ms dark) — never block by block, never a shimmer loop, never an opacity pulse; content cross-fades in (skeleton out 120 ms, content in 200 ms) the frame it arrives. `aria-busy` on the region, one status message at 1 s («Ouverture du document…»), one at arrival only if the wait was announced, one at 10 s.

**The loading contract (public and console).**

| Moment | V5 |
|---|---|
| First frame of the home | the navy chapter painted from the first frame (`body.page-home` hard-stop background for the first `100svh`), the mark inline in the lock-up (≈ 1 KB SVG), the wordmark from its 1.71 KB subset — no cream flash |
| Click → next page | the thread from 400 ms; the header mark and the rail tile stay still; public View Transitions only after their re-measure (off by default) |
| In-page action (filter, mark as read) | nothing below 150 ms; the busy key after 150 ms, ≥ 480 ms once shown |
| Form submit | the busy key at 0 ms in the button, the thread from 400 ms; every public form gets `data-single-submit` |
| Region fetch (preview, «Aller à…», notifications, search) | L3 + the L2 key + a word in the region head from 400 ms; no door; content never waits for a cycle |
| Outcome-bearing request («Enregistrer et recalculer», the pre-assessment, eligibility, scan verification) | L2 in the button and L3 in the result region — never L1, never a door (`loader.js` holds the list; a test checks it) |
| Login | the stage's key turns once on submit (§18) |
| 10 s | the key stops at rest, «C'est plus long que d'habitude.», «Réessayer» |
| Never | a full-screen loader or curtain; an entrance that hides painted content; a ticking countdown; a spinner beside the brand; the mark looping; a door that opens while a legal answer is computed |

---

## 18. Login — «Il varco»

**A focused threshold.** On entrance pages the header keeps the lock-up, the language control and «Retour au site» — no mega-menu, no link to the page you are on. The page is split: at the inline start the **owner's door stage** on night (240 × 320, the gold light runs the arch once after LCP); at the inline end the form set **directly on the mineral paper** — no floating SaaS card (#28369's structure) — under one serif H1. Form: e-mail → password with «Oublié ?» at the end of the password label row → the show/hide text button → «Rester connecté» → one PRIMARY. **On submit the stage's key turns once** (two half-turns and the frame light, 1600 ms, the planes still: the person is entering) and the button carries the busy key at 0 ms; if the answer takes longer, the button's key and the thread carry the wait — the mark does not loop; on error the error summary takes focus; on success the next page takes over. No crack of light (`RED_TEAM` M10). The night panel is a solid plate, not glass. One reassurance line under the button reuses verbatim the locked FAQ answer on data protection (owner D-U6); no invented badges; passkeys only when the backend offers them. Reset, verification and MFA sub-pages share the layout. **Phone:** the V4-specified 120 px night band with the arch-and-steps glyph above the form; the e-mail field inside the first viewport at 390 × 844. **The door is the login's only image by default**; the terrazzo-steps accent would become the LCP element and ships only if the owner asks for it (and then preloaded). *Needs the owner's confirmation that this one-shot is what `BRAND_ASSETS.md` §1 allows (O1).*

---

## 19. Mobile — Solution A «Una schermata» is adopted

**The home hero on a phone becomes exactly one small viewport minus a 32 px peek of the next chapter** (`MOBILE_UX` §3). The door takes whatever height the copy leaves, between a floor equal to today's door at that viewport (223 px at 390 × 844 — revised from the council's 136 px, see below) and 300 px, via one flex column (`flex: 1 1 0` with a floor and a ceiling — no per-locale constant, no JavaScript); the copy (eyebrow, locked title, lead, two actions) sits low, in the thumb zone; the hero body paragraph and the four-audience legend **move** into chapter 01, whose rows become the four doors with their gloss always visible (the CD V4 §4.5 promise, finally kept). «Move» is specified (`RED_TEAM` m11): the copy is rendered once in each place, a media query shows one and sets `display: none` on the other, no `id` is duplicated, and the locked-copy equality test counts the one visible instance. The V1 `.hero` padding that leaked 96 px of empty navy into the V4 hero is closed. `100svh` (never `dvh`, which would shift the layout as the browser bars move).

**Measured on the prototype** (CSS injected into the served pages, fr/it/en/ar, 8770 and 8771). **Phase 3:** hero **711 / 723 / 755 / 826 px** at 360 × 800 / 375 × 812 / 390 × 844 / 412 × 915, i.e. **88.9–90.3 % of the viewport, bottom edge at 96.0–96.5 %**; the door 242 × 300 (+81 % area at 390 against today's 180 × 223); the primary action fully visible in all 40 measured cases (5 variants × 4 nominal + 4 estimated small viewports), the secondary in 39. **Interim** (what the public sees while G3 is closed), with the V4 interim title: the door shrinks to 166 × 206 (fr) and 144 × 178 (it) at 360 × 800 — *smaller* than today's; at the estimated real-phone heights the hero reaches 101.4–108.3 % even with the 2 rem interim-title lever, and 119.5 % at 320 × 568 with the primary 31 px under the fold (`MOBILE_UX` §3.4). The council's «door +81 %» was true for phase 3 at the nominal viewports only (`RED_TEAM` M7).

**What V5 changes for the interim.** The interim title gets its own setting — Source Serif 4 at 28–32 px, not the phase-3 display size, with a one-line eyebrow — and the door gets a **floor equal to today's door at the same viewport** (223 px tall at 390 × 844; the other viewports measured on 8770 and 8771 before S1), instead of the council's 136 px. When a small screen cannot hold everything, the precedence is: (1) the primary action fully visible; (2) the door never smaller than today's; (3) the hero ends inside the viewport with its 32 px peek. The interim is re-prototyped and re-measured in gate 0.

**Solution B's composition** (the door beside the title) is used where A is the wrong tool: phone landscape (`orientation: landscape` and `max-height: 30rem`), the inner landing pages (first primary within 560 px at 360 × 800 — today `/fr/parcours/` shows it at 2 745 px), and the login band.

**The rest of the phone.** The home from 13.1 to ≈ 9.2 screens at 390 (the doors as four 96 px rows, pathways as 64 px rows with detail in `<details>`, the FAQ as `<details>`, news hidden when empty, footer groups as `<details>` — estimates, not prototypes). The wordmark visible down to 344 px. The console: persistent chrome ≤ 120 px at 360 × 800; bottom-bar labels on one line ≥ 12 px; the first input of «Ma situation» above the sticky foot (≤ 520 px at 360 × 800: the note into a `<details>`, the form margin 48 → 16, the progress rail as one line «Question 1 sur 8» + dots); the case file's seven-step rail as a current-step card; the dashboard's Dossier facts as a two-column grid; «Ouvrir le besoin» inside the card that explains it; the phone list «Quatre accès» with its glyphs in ink (no audience colour on paper).

**Acceptance tests** — the ten of `MOBILE_UX` §10, adopted and extended after the red team: every case runs in **both phases** (8770 interim, 8771 phase 3), in four languages, at the four nominal viewports **and** the four estimated small ones plus 320 × 568. Primary visible in every case; the door never smaller than today's at the same viewport; hero bottom ≤ 100 % at the nominal viewports in both phases, and at the small ones in phase 3 (interim: reported, target ≤ 100 % with the new setting); every landing's primary within 560 px at 360 × 800; landscape primary in the first screen; chrome ≤ 120 px with a «Menu» control present on every console template; home ≤ 9.5 screens; no horizontal scroll 320–430; CLS/LCP inside budget; the same under reduced motion, forced colours and without JavaScript. They must be confirmed on one real iPhone and one real Android phone: the small-viewport heights are estimates of browser chrome.

---

## 20. The other surfaces, briefly

- **Inner public pages.** The four door landings and the Forum get the landing hero (4:5, §10); every other public page keeps a type header with the section grammar — **a 14 px `ile-steps` micro-mark in ink + a sentence-case eyebrow 13/20 500 in text-2 + a serif title + a sans lead**; the council's gold hairline and tracked capitals are dropped (they were the reference site's device, `RED_TEAM` M12, and once design stops adding capitals, the locked capitals read as engraving — `UX_PUBLIC` §2.5) — a 21:9 band where IMAGERY assigns one, «Sur cette page» on long reads, and a rail of *table of contents · «il gradino» (the page's one full instance) · related doors* — never again a 150 px column holding a display-size title (defect D1, «ATTENTIO / N AUX FRAUDES»). «The text scrolls, the picture answers» (≤ 3 photographs) only on the long explanatory landings.
- **Home chapters, in order** (the back-office keeps control through `home_sections`): La porta (hero) → Quattro porte → Ce que nous ne faisons pas + «il gradino» (the page's one full instance) → **the orientation passage** (the passage and «S'orienter» as one chapter until D-U9 and G3, §11; after them, Il passaggio → S'orienter, the one BRAND chapter with the locked «Comment ça marche» rendered as a stepper split verbatim on «→», owner D-U4) → Les parcours → Forum Vénétie–Maroc → L'écosystème (bento) → Actualités (only with articles) → La porta riservata → footer. Materials alternate: navy · paper · stone · navy · paper · photograph · paper · navy · night (the brand band returns with the upgrade). Section numbers disappear; numerals remain only for real sequences.
- **Forum (public).** An event card (date block from `event.starts_at`, time, venue, the locked patronage line, register · `.ics` · «Itinéraire» as a link), a **state machine computed from dates** — announced («Dans 5 jours», static) → today → held (a recap slot for commissioned photographs) → permanent (owner D-U5) —, a timetable that shows a time column only when every row has a time, a tribune of role cards with glyphs, «la marche» as the identity band (subject to O54; fallback in §5), the plain of the territory above the programme, the «table est mise» loop below the fold (only if Istituzione does not take the same room, O60). No disabled buttons in public: a closed route shows one sentence of «when». *The Forum is on 2 October 2026, five days from today: the V5 states cannot ship before it inside a safe plan (§ IMPLEMENTATION_PLAN), so they are designed for the `held` and `permanent` states.*
- **Footer — the closing lintel.** Columns kept; a quiet notte-950 closing band with no arch watermark (`RED_TEAM` M2); the anti-fraud entry as a one-line link; «Contenus vérifiés le …» kept; the build label leaves the public footer; `lang="en"` on English legal titles (or translation — owner).
- **Company workspace.** A needs overview strip (four counts by state as filter links), the needs table as the product's reference table (caption, scope, sticky head, stretched-link rows, sortable headers as links, cards below 64 rem), the CTA naming its verb, the referent's name and company instead of the handle, the need detail migrated to the case-file composition.
- **Academy.** Leaves the serif and joins the console language (owner decision `UX_PLATFORM` 9); «Mon suivi» first when enrolled (enrolment rows with a notched module meter); lesson lists; covers only if the owner funds licensed ones.
- **Forum governance.** «Espace momentanément indisponible» renders inside the console, not the public shell (P0); when the gate opens: state lanes without drag, the engagement caveat as a persistent notice, milestones through the timeline component.
- **Guichet numérique.** Triage first (two choice questions route to existing written answers; «Toujours pas ?» opens the form carrying both answers), thread rows with role labels and absolute dates, requests grouped by date; the staff queue as the reference table with the filter bar. The 20 templates that override `extra_head` get one test so no module base drops the console sheets again (the helpdesk rendered unstyled; fixed in `c9a58d8`).
- **«Ma situation».** The good bones stay (one question at a time, the per-question «why», OptionCards, the sticky foot); the counter matches the stepper; a DateField of three labelled inputs replaces the browser-locale date; after «Enregistrer et recalculer», an **outcome diff** says what changed — the most consequential click in the product must not look like a save; the recalculation waits on the L2 key in the button and L3 in the result region, never on the door.
- **Error pages.** The door at rest with the key out of the lock, the message, three ways back.
- **The public orientation questionnaire** (registry FM12, `RED_TEAM` B4). The hero's locked primary leads to it, and today it is the least designed page on the site: V2 `orientation/wizard.css`, a full-page POST per step, a **percentage progress bar**, inert `hx-*` attributes, plain radio lists, no busy state (`UI_INVENTORY` P60, `UX_PUBLIC` §2.2). V5 gives it the «Ma situation» grammar: one question at a time; «Question n sur N» in words, never a percentage or a `<progress>`; OptionCards with the real radio inside the label; the L2 key at submit; focus on the arriving question's first control; the journey thread on each step; the result page on the V5 kit, with the outcome and sources block (SW21). Server-rendered and complete without JavaScript. It ships with the home as step S1b; an acceptance test asserts no `%` sign and no `<progress>` in the questionnaire's rendered pages.
- **Long-form prose** (PX24): news detail, legal documents, living sheets, pathway detail — measure 65 ch, serif H1, sans body 17/28, «Sur cette page» and the reading progress, the `lang` of every foreign part.
- **Glossary** (PX25): the A–Z index as a sticky letter bar of links (letters without terms are not links), term pages with the definition, its source and related terms; the term page's unstyled `.glossary-term` and `.meta-list` get their rules.
- **Vivre en Italie** (PX26): topic and sheet cards on the generic navigation card (PX27) with one concept glyph each — today they have no CSS at all.
- **Account pages** (SC11): profile, deletion and the allauth management pages move into the console shell (they are authenticated surfaces living in the public shell today) on one settings layout: a section list, one form per section, a destructive zone last.
- **The pre-assessment outcome and its sources** (SW21, legally sensitive): the outcome in words with its register mark (never a verdict colour), the rules version in mono, the sources as a list with their consultation dates, the locked caveat visible; used on the dashboard, the case, the assessment page and the public questionnaire's result.
- **Homes of institution, university and professional accounts** (SW22): the successor of the «portal cards bridge» V4 rejected — ContextHeader, NowPanel, «À faire», an activity feed, shortcuts: the person's dashboard grammar without the journey rail.
- **Virtual Forum community** (9 pages, gate G11): composed from existing types — thread rows (SW13) for rooms, the event card (PX14) for the calendar, state lanes (SW11) for initiatives and moderation — and moved into the console shell when its gate opens; no new type.
- **Retired:** the home's jurisdiction bar (P23) — a proportional bar that reads as shares, whose message («who answers for what») the trust chapter and threshold A now carry — and the pilot-flow illustration (P49): the ecosystem pilot page renders the pilot sequence on the passage's level line, without sides, so the site keeps one diagram language.
- **Back-office (Unfold)** (SC12): the `UNFOLD` settings re-pointed to V5 — the primary ladder mapped to laguna and notte, Host Grotesk self-hosted through Unfold's `STYLES`, radius 6, no serif, status labels following the registers (`conforme` in ink, no green) — and the favicon's `ile-arch` as the site icon.

---

## 21. Explicitly rejected — and why

| Rejected | Proposed by / seen in | Why |
|---|---|---|
| A new hero that replaces the door, or a video in the hero | 21st hero searches | the door is a brand-locked asset (`BRAND_ASSETS` §2) and the LCP element; a hero video adds bytes on the LCP path and a second moving picture |
| Entrances that start invisible (title line reveal, stage choreography, AOS-style fade-ups, «opacity 0 until JS») | CD V4 §3.1 (removed in gate A), studiobadrane.com, many 21st heroes | law 2.2 — nothing painted is taken back; the gates measured 1.6 s of hidden routes and a re-entering title |
| A full-screen loader or curtain | agamieuromed.org, 21st page-transition overlays | a ~1 s wait the LCP budget cannot afford; content never waits |
| Liquid-metal / WebGL / shader buttons and grounds | 21st #10443, #21563, #19153, shader heroes | 8.3–100 KB gz, a GL context, an injected `<style>` (CSP), a consumer-tech signature; the brand's metal is the key's gold |
| Chrome «metallic rim» on buttons | 21st #29293 tier 1 | same signature problem; replaced by «Bordo d'oro» |
| Arch-shaped image windows on cards; the arch as a generic reveal (`.portico-reveal` ×2 per page); the hero exit where the arch widens into a photograph | CAPTURES §3.3.1, 21st #10905/#2061 | spends the brand's strongest shape; the arch masks only the door |
| Photographs on operational screens, including a photo band behind the dashboard header | 21st #19068 «Console with a window» | the console's richness comes from the person's real objects, the journey, material and motion; a decorative band competes with the one thing the page must say; LCP risk on a 2.43 s dashboard |
| Arch drawing at the MA→IT frontier of the dashboard rail | 21st platform-domains «La soglia» | V4 pillar 2 (no door in the dashboard); a 16 px `ile-arch` glyph at threshold B instead |
| One «crossing» frontier between steps 3 and 4 | ICON `ile-crossing`, MOTION draft | the side switch is jurisdiction, not place; two thresholds (§11) |
| The golden key travelling the route; a vehicle; a dotted flight path; flags; maps | 21st #24556, travel metaphors | the key is not a vehicle; the forbidden image vocabulary |
| Ranked doors: zig-zag widths, ordinals 01–04, landform glyphs; mega-menu eyebrow numbers | V2 «quay», 21st #9952 | four equal doors |
| Hover expansion of the doors (flex-grow 1 → 1.4) | 21st #27010 | a hover-driven layout shift counts in CLS (hover is not an input that excuses shifts) |
| Cursor-following image previews in navigation | 21st #28258, #9871, #9536 | pointer-only: no touch, no keyboard parity |
| Status palettes with semantic green/red; traffic lights | UI-UX-Pro-Max, coss / HeroUI badges | CR-11: no colour means approved |
| Pictographic status icons (search, warning, glasses, hourglass, ban) | council ICON/PRIMITIVES | replaced by one family of circle marks legible at 14 px |
| Fanned ghost-tile empty-state media | 21st #19747 | a catalogue signature; ILE's empty states are a line (region) or a glyph + one action (page) |
| Shimmer loops, opacity pulses, spinners beside the brand | 21st skeletons, motion CSV | V4 §7.1 #13 forbidden list; `background-position` sweeps repaint the sheet; L3 moves one light on the compositor |
| Tricolour trailing strokes in the loader; any tricolour on a control or a state | 21st #16834 adaptation | the tricolour lives in the mark; it moves only as the door opening |
| Page transitions in the console | nav-shell curation | +90 ms LCP measured on the public route; a person working a dossier wants the next page |
| Staff command palette that searches persons | 21st #27378 «Personnes» filter | CR-03 / CR-04 |
| Drag-and-drop kanban for Forum proposals | 21st kanban family | a governed state is a motivated decision, not a drag |
| KPI tiles, charts, percentages, scores on a person's screens | 21st dashboards | legal: no percentage and no score; counts in words |
| Avatar photographs in the console; greyscale-to-colour speaker portraits | 21st account menus, #10098 | glyph discs only; people are never duotoned |
| Confetti or any celebratory success motion | 21st checklists | nothing is «approved» |
| AI chat assistant surfaces | 21st catalogue noise | no such function exists; inventing one is forbidden |
| Dark-mode toggle / full dark theme | 21st menus | night is a set of contexts; no research base; doubled QA |
| Infinite scroll, auto-rotating carousels, marquees, ticking countdowns | 21st, agamieuromed.org | finite registers; motion without purpose; live-region noise |
| Slider controls | 21st sliders | no range field exists |
| Floating CTAs, FABs, chat bubbles | studiobadrane.com, 21st | they cover content; the bottom bar and the action bar own the thumb zone |
| Inline PDF renderer in the preview | forms-docs C12 | CSP and security changes (`frame-ancestors`, `worker-src`/wasm) |
| Remote fonts, remote images, remote scripts at runtime | reference sites | CSP `'self'`; everything self-hosted |
| Outlined-SVG wordmark (removing the wordmark font) | TYPOGRAPHY A2 | the owner has not authorised removing the wordmark font |
| The mark's English tagline and the door caption, in any language | BRAND_ASSETS §1 | prohibited wording F13/F14 |
| *Rejected after the red team:* the duotone vault layer behind the hero | IMAGERY §3.1 | more arches behind the door, a new LCP candidate, decoration (M2, m15) |
| An arch-shaped photograph reveal at the arrival threshold (D-U7); the footer's arch-and-steps watermark | UX_PUBLIC §5.2, 21st footer | the arch belongs to the door (M2) |
| VALIDE in lapis with a check; checks on journey nodes; a tick on a filed piece | COLOUR D2, the DS/COLOUR node spec, forms-docs | the repository's enforced rule: `conforme` is ink; no colour and no check mean approved (B1) |
| Infinite hero lights; any loop on the home | MOTION D10 | WCAG 2.2.2 without a pause control; the first breath now ends in ≈ 3.3 s (M5) |
| Glow on hover; light-cyan gradient primaries on navy; a light sweeping the CTA's gilt rim; glass on content, on the hero legend, the login panel and the micro-visual; blurred scrims | V4, council primitives and colour | with gold streaks, the vocabulary of crypto wallets and trading dashboards (M3, m5) |
| A gold light on the header mark or the rail tile during navigation | MOTION §6.3 S, UX_PLATFORM move 8 | effect density; the thread already says «loading» (M3) |
| L1 in panel heads and on outcome-bearing waits; the tricolour planes parting; a crack of light at the jamb | MOTION §6.2, §6.4 | a door that unlocks during a legal computation promises an outcome; the mark moves once, at the entrance (M10) |
| A route rising from Morocco (low) to Italy (high) | MOTION §7.1 | a growth chart and a hierarchy between equal shores (M4) |
| The gold-hairline tracked eyebrow; a photograph as a featured card beside a serif blurb in the mega-menu | CAPTURES §3.3.3, nav-shell | the reference site's elements, not its principles (M12) |
| A tricolour filet on the institutional notice | COLOUR D7 | the tricolour lives in the mark (M17, O57) |
| A percentage progress bar in the public questionnaire | V2 orientation wizard | no percentage, no score (B4) |

---

## 22. The four gate-A deviations

The owner accepts the first three if premium quality holds and wants the fourth corrected. The first three are **accepted as V4 deviations and resolved in V5** — not by restoring what was removed, but by giving the hero back its voice and its gesture in a form that cannot hide painted content. The fourth is **corrected**.

### 22.1 The lead is not italic

| | |
|---|---|
| **ORIGINAL** | CD V4 §3.1 item 1: «lead corsivo bloccato» — the hero lead set in the serif italic (Newsreader italic, `--t-lead` 20/28): the one reading voice beside a monumental title. |
| **CURRENT** | `.hero__lead` in IBM Plex Sans 400, 20/28, `--on-dark`, max 36 ch (`static/css/v4/hero.css` l.127–137, with the comment «Plex, not the serif italic: that one paragraph pulled Newsreader's italic file (144 KB) on every home load»). Recorded as a deviation to be signed in gate A round 3, item 6. |
| **REASON** | Performance: the 143.4 KB Newsreader italic file was transferred in contention with the LCP on slow 4G + CPU ×4 when the home LCP stood at 3.0–3.6 s; on the phone the lead *is* the LCP element (a text node). |
| **VISUAL IMPACT** | The hero lost its only change of voice: title, lead, body and legend all read in one register; in Plex the lead reads as interface copy, not as a statement — one ingredient of «portale amministrativo con font elegante». |
| **PERFORMANCE / ACCESSIBILITY IMPACT** | Current: −143.4 KB on the home, no legibility cost (roman is at least as legible). Restoring the italic in V5 costs **19.1 KB** (Source Serif 4 italic `opsz` 20), not 143.4; the risk is a later paint of the mobile LCP text if the italic arrives late — mitigated by `font-display: swap` with a metric-matched fallback, and to be measured, not assumed. Arabic never takes an italic. |
| **RECOMMENDATION** | **Accept the deviation for V4; resolve it in V5 by restoring the italic in Source Serif 4, behind a measured gate** — on 8772 (gzip), slow 4G + CPU ×4, 1440 × 900 and 390 × 844, three runs each: home LCP ≤ 2.2 s (median) and a font-swap CLS contribution ≤ 0.01. If the gate fails, set the lead in **Source Serif 4 roman** (already preloaded on public pages, 0 extra bytes): still a serif voice distinct from the interface sans. Never back to the UI face. |

### 22.2 The title has no reveal

| | |
|---|---|
| **ORIGINAL** | CD V4 §3.1: the H1 in Newsreader 300 «che si rivela riga per riga (stagger 60 ms, 480 ms)». |
| **CURRENT** | The title is painted complete from the first frame. The mask reveal and its `.line { overflow: hidden }` were removed from `home.js` in gate A round 3 (item 7): 0 frames with a hidden line in 870 and 978 samples (slow 4G, two passes) and 359 unthrottled. |
| **REASON** | The reveal started from the deferred module *after* first paint: it hid a title the person had already read and made it re-enter. It also put the page's largest text behind a script on slow devices. |
| **VISUAL IMPACT** | With the stage choreography also removed (22.3), the first viewport lost its only moment of motion — part of «not dynamic». The title itself remained thin (Newsreader 300 capitals). |
| **PERFORMANCE / ACCESSIBILITY IMPACT** | Current is strictly better: no hidden text at load, no LCP delay, nothing for assistive technology to wait for, no motion discomfort. A text reveal in a first viewport is illegal under V5 law 2.2 (class B forbids text, the LCP element and the first viewport). |
| **RECOMMENDATION** | **Accept, permanently.** V5 animates no text in any first viewport. The title's quality comes from type (Source Serif 4 400 instead of Newsreader 300 — the monumental version on the board) and composition (D-U1 option a); the hero's motion comes back additively (22.3). |

### 22.3 The stage has no entrance

| | |
|---|---|
| **ORIGINAL** | CD V4 §3.1 and §4.4: the arch traced once (900 ms) → the four routes drawn (900 ms, stagger 120) → the legend (200 ms); steps and key settling; the same choreography on the login door. |
| **CURRENT** | Removed in gate A round 4 (defect 11), with `static/js/src/entrance.js` for the login: the stage is complete from the first frame; the 28 s route current (CSS from the first frame) and the scroll-linked photo drift and stage settle remain. Measured: 0 visible → hidden transitions and 0 transform changes at load across 261 / 364 / 210 / 690 frames. |
| **REASON** | On slow 4G the routes, nodes and exit words vanished for 1.6 s *after* being painted — the same failure as the title. |
| **VISUAL IMPACT** | The brand's one gesture (the door opens once) was lost; the stage reads as a picture; the only remaining motion, the current along the routes, reads as network fibre. |
| **PERFORMANCE / ACCESSIBILITY IMPACT** | Removal: better CLS/LCP and stability. What remains costs: the current's `stroke-dashoffset` loop takes ≈ 30 % of the main thread under CPU ×4 while the hero is visible (`MOTION` §5.11) — a V4 cost V5 removes. |
| **RECOMMENDATION** | **Accept the removal permanently; give the intent back additively.** After LCP, once, the gold light runs the arch (900 ms, class A, composited dash on the arch's own geometry); the four route currents become four lights that travel once after the arch light (≈ 3.3 s in all) and rest — no loop, so no pause control is needed (`RED_TEAM` M5). On the login the key turns once when the person submits (a gesture caused by the person). Gate: the gate-A frame method (0 visible → hidden, 0 transform changes on painted content at fp + 0/250/600/1200/2500 ms) plus a trace (0 long tasks attributable to motion, 0 `compositeFailed` for the light). Reduced motion: no light; the composition is complete without it. |

### 22.4 The mobile hero is taller than the screen — corrected

| | |
|---|---|
| **ORIGINAL** | CD V4 §3.1: hero ≤ 100 vh on desktop and **≤ 110 % of the viewport at 390**; §4.5: on the phone the door alone, then the title; the gloss always visible. |
| **CURRENT** | 124.1 % (8771, phase 3) and 129.3 % (8770, interim) at 390 × 844; 138.4 % / 142.4 % at 360 × 800; 114.4 % / 119.2 % at 412 × 915; on a real phone, with the browser bars, 157–176 % of what is visible. The door is 180 × 223 px at 390. A waiver («deroga a 390») was proposed in gate A round 4 and never signed; the owner refuses it. |
| **REASON** | Three measured causes (`MOBILE_UX` §0): a V1 rule (`components.css:1171`, `.hero { padding-block: clamp(48px, 8vw, 96px) }`) leaks 96 px of empty navy into the V4 hero; the phone hero carries six blocks — the 7-line body paragraph and the 2 × 2 legend alone are 30–34 % of it, and the legend repeats chapter 01; nothing is sized against the viewport height. |
| **VISUAL IMPACT** | Text-heavy first screen with a small image; the four audiences presented twice in the first three screens; «readable, not memorable». |
| **PERFORMANCE / ACCESSIBILITY IMPACT** | Today the primary action misses the first screen in 3 of 40 small-viewport cases. Solution A: primary visible in 40 / 40, secondary in 39 / 40; `svh` (not `dvh`) so no layout shift when the browser bars move; `min-block-size` (not `height`) so the hero grows at 200 % text size (1.4.4, 1.4.10); the door is drawn larger, so on a DPR 3 phone the 400 px arch file shows at 1.58× — if it looks soft, a 600 px AVIF strip (+25–45 KB, ≈ +0.15–0.25 s on slow 4G, still inside 2.5 s) — to be measured. |
| **RECOMMENDATION** | **Correct it with Solution A «Una schermata»** (§19): measured for phase 3 at the nominal viewports — hero bottom at 96.0–96.5 % of the viewport from 360 to 412 px, door +81 % in area; the V1 leak closed, the body paragraph and the legend moved into chapter 01. **For the interim** (what the public sees while G3 is closed) the correction is not yet measured: its title gets its own setting and the door a floor at today's size, re-measured in gate 0 (`RED_TEAM` M7). The CD signature needed: the legend leaves the phone hero. Gate: the extended acceptance tests of §19 (both phases, nominal and small viewports), then one real iPhone and one real Android phone. |

---

## 23. Council conflicts — how they were arbitrated

| # | Topic | Positions | ECD ruling | Reason |
|---|---|---|---|---|
| 1 | Status glyphs | circle grammar (COLOUR) · pictograms `glasses`/`hourglass`/`ban` (ICON) · sprite icons `clock`/`search`/`warning` (PRIMITIVES) · `upload`/`refresh-cw` (UX_PLATFORM) | **circle grammar, «i cerchi»** | one family, legible at 14 px, open/settled without colour; the same marks become the ledger's pips |
| 2 | Status colours | V4 ink/pending/err (UX_PLATFORM §5, PRIMITIVES §2A.2) · eight tones (COLOUR) | **COLOUR's tones, with `conforme` kept in V4's ink** (revised after the red team, B1) | measured separation, no mud, no crude red, no green; the repository's «no colour means approved» test |
| 3 | Neutro chips without a mark | `badges.md` §4.3, ICON Q2 · «no chip without its glyph» (COLOUR) | **every chip carries its mark** | the V4 illegibility came from marks missing |
| 4 | BLOQUÉ | «not a chip» (PRIMITIVES) · register `blocco` (COLOUR) | **by scope**: a chip for blocked checklist/evidence states; a sentence + link for the doc-row Conditions gate | both are right where they apply |
| 5 | Journey frontier | `ile-crossing` (ICON, MOTION) · two thresholds (UX_PUBLIC) · the arch drawn at the frontier (21st platform-domains) | **two thresholds: `stamp` (A), `ile-arch` (B)**; in the console as 16 px glyphs | jurisdiction ≠ place; no door drawing in the dashboard |
| 6 | Journey in RTL | unmirrored (21st hero-public dec. 6) · mirrored (UX_PUBLIC, MOTION) | **mirrored** | a sequence, not a map |
| 7 | Arch windows on cards | yes (CAPTURES §3.3.1) · no (IMAGERY, UX_PUBLIC) | **no** | the arch belongs to the door (the threshold reveal is withdrawn after the red team) |
| 8 | The hero's gesture | key turns once (UX_PUBLIC H7) · light only (MOTION §5.1) | **light only** | the key turns once, at the entrance (the login) |
| 9 | Home images | door + layer + 9, portico video (IMAGERY) · door + 8, diptych (UX_PUBLIC) | **door + 8; no layer; no video on the home** | meaning over mood; one live object per page |
| 10 | Dashboard photo band | yes (21st #19068) · no (IMAGERY, COLOUR, UX_PLATFORM) | **no** | operational screens carry real objects |
| 11 | View Transitions | everywhere (nav-shell) · public only (MOTION) | **public only, 120 ms, off until measured** | +90 ms LCP at 180 ms; 120 ms not yet measured |
| 12 | Staff palette | includes «Personnes» (21st #27378) · never (UX_PLATFORM) | **never persons** | CR-03 / CR-04 |
| 13 | Signature CTA | liquid-metal WebGL tier (PRIMITIVES, conditional) · — | **«Bordo d'oro»**, CSS: the paper plate with a static gilt edge (the hover light withdrawn after the red team) | brand fit, CSP, weight, register |
| 14 | Loader | #16834 trace + tricolour strokes (PRIMITIVES) · «La chiave che gira» (MOTION) | **MOTION's loader** | the mark doing its own act; composited; prototyped and traced |
| 15 | Skeleton / busy timing | 120 ms + ≥ 380 ms (#23557) · 400 / 150 / 0 ms + ≥ 480 ms (MOTION) | **MOTION's thresholds, one set** | one law for every wait |
| 16 | Empty states | fanned tiles (21st #19747) · no icon (ICON) · one sentence (dashboard) · dashed box + glyph 48 (DS V4 #30) | **by scope**: region line; page = glyph disc + one action | honest and composed |
| 17 | Door hover | flex-grow (21st #27010) | **no grow**; image scale + route rule + spotlight | CLS |
| 18 | Mega-menu ordinals | 01–04 (nav-shell) · no ordinals (UX_PUBLIC) | **no ordinals** | doors are not ranked |
| 19 | Login image | stock aside with arch outline (21st #9106) · the door alone (IMAGERY) | **the door alone**; accent optional | the door is the login's image; LCP |
| 20 | Mobile drawer order | languages at the foot (MOBILE_UX) · language row first (UX_PUBLIC) | **compact language row first; «Espace réservé» sticky at the foot** | language is often the first action of a multilingual public |
| 21 | Rail default | collapsed below 90 rem (V4) · open from 80 rem + labelled compact (UX_PLATFORM) | **UX_PLATFORM** | occasional, multilingual users |
| 22 | Context sidebar | tree rail as a second sidebar (nav-shell) · index in the inspector (UX_PLATFORM) | **index in the inspector** | no fourth column at 1280 px |
| 23 | Speaker portraits | greyscale → colour on hover (#10098) · never duotone people (IMAGERY) | **no greyscale**; portraits only if authorised | dignity; one grade |
| 24 | The hero lead | serif italic (TYPOGRAPHY) · Plex roman (gate A) | **Source Serif 4 italic behind a gate; serif roman as fallback** | §22.1 |
| 25 | News without cover | `micro-conference` fallback (IMAGERY) · never a stock placeholder (hero-public) | **text rows** | one image, one context |
| 26 | Diptych context | regular-mobility page (IMAGERY) · passage head (UX_PUBLIC) | **both — the same message** | IMAGERY to confirm |
| 27 | Guichet glyph | `concierge-bell` (ICON) vs the bell family twin (ICON Q3) | **keep, after a 20 px side-by-side**; fallback `messages-square` | pertinent and memorable |

---

## 24. Decisions for the owner — consolidated

Grouped by what they unblock. «ECD» is my recommendation; nothing is decided until the owner signs. The phase each one blocks refers to `IMPLEMENTATION_PLAN.md`.

**Order of signature, revised after the red team** (`RED_TEAM.md` §8). (1) **The rulings the pictures need**, first: O54 (the scope of F15), O55 (identifiable people), O14 (VALIDE — default ink), O57 (the tricolour filet). (2) **Gate 0** (O59): the owner reviews composed screens built with the amended specification — the home's first three screens, the login, a mid-case dashboard, «Mes pièces». (3) **Then the decisions below**, each before the phase it blocks. Rows marked *revised* changed after the red team; *withdrawn* rows are kept for traceability; O54–O66 are new.

| # | Decision | ECD recommendation | Blocks |
|---|---|---|---|
| **Rulings the pictures need (sign first)** ||||
| O54 | **The scope of F15** («porte/soglie», «griglie/cancelli»): are arcades, covered passages, steps and vaults inside it? Recorded in `IMAGE_LICENSES.md` §1 before any V5 photograph enters `CURATED` (`RED_TEAM` B2) *new* | the prudent reading: yes for covered passages, steps and vaults — use «Lo stesso gesto» and the Forum fallback; the owner may rule otherwise, in writing | Phase 0, S1 |
| O55 | A legal reading, door by door, on identifiable people in stock photographs (the Pexels License has no model release) (M13) *new* | yes, before curation; Persona shows nobody identifiable in any case | Phase 0 |
| O14 | VALIDE: **default = ink** (the repository's rule, `test_chips_registry.py`), no check; the word stays «Valide»; lapis only if the owner and legal sign it in writing before F4, with `test_chips_registry.py` amended in the same commit (B1) *revised* | **ink** | F4 |
| O57 | A tricolour filet on the institutional notice (COLOUR D7) (M17) *new* | **no** — the tricolour lives in the mark | F4 |
| O59 | **Gate 0**: the owner reviews composed screens before signing the other decisions (B3) *new* | yes | before F1 |
| **Brand and identity** ||||
| O1 | The mark's key turns **once**, at the entrance (the login stage on submit), with the frame light; the planes never move; no loop, no crack of light — the literal reading of `BRAND_ASSETS.md` §1 «si muove una volta, all'ingresso» (MOTION D1, D2; M10) *revised* | yes; if refused, L1 is withdrawn | F5, S4 |
| O2 | The rail tile shows the mark with its gold key, **still** — no light runs it (UX_PLATFORM 8; M3) *revised* | yes | S5 |
| O3 | A 16 px `ile-arch` glyph at the arrival threshold of the console rail (exception to «no door in the dashboard») | yes, glyph only | S6 |
| O4 | ~~One arch-shaped reveal at the passage's arrival threshold (D-U7)~~ *withdrawn* (M2) | — | — |
| O5 | «Il gradino»: the mark's three steps as the anti-fraud component, **one full instance per page**, a one-line link elsewhere (D-U8; M14) *revised* | yes | S1, S2 |
| O6 | Wordmark delivered as the 1.71 KB Newsreader subset (11 code points); no outlined SVG; **every rendering of the name in that face** (M1) *revised* | yes | F1 |
| O7 | Lock-up text visible down to 21.5 rem (344 px) | yes | F1 |
| O8 | A navy vignette centred on the key over the door photograph (D-U2) | yes, after a 1440 / 390 test | S1 |
| **Type** ||||
| O9 | Pairing A (Source Serif 4 + Host Grotesk) or B (Newsreader re-set + Public Sans) | **A** | F1 |
| O10 | Vazirmatn + Markazi Text for Arabic, after one review by a Moroccan reader — **blocking** for `/ar/`, Noto Sans Arabic as the fallback candidate (m17) *revised* | yes, after review | F1 (`/ar/`) |
| O11 | Hero H1: the name as an engraved line **in the wordmark face** + the locked promise as the display line in Source Serif 4 (option a), or the name as the display line in the wordmark face with its `opsz` 36/72 instance (option b) (D-U1; M1) *revised* | **a** | S1 |
| O12 | Academy leaves the serif and joins the console type | yes | S10 |
| **Colour and status** ||||
| O13 | The console one step lighter (page carta-25, sheet white) (COLOUR D1) | yes | F2 |
| O15 | Registers `esame` and `blocco` + the re-mappings of `VerificationStatus`, `ScanStatus`, `AssessmentOutcome` (COLOUR D5, D8): seven chromatic registers + the ink register | yes; domain owner confirms readings | F4 |
| O16 | Retire green, bronze, the pending brown and the red «accent» shim (COLOUR D4) | yes | F2 |
| O17 | Every chip carries its mark (overrides `badges.md` §4.3) | yes | F4 |
| O18 | The project's «Vérifiée» is not a seal (UX_PLATFORM 4) | yes | S9 |
| O19 | Persona's accent: keep V4's `#7fd1d8` (= the interactive night accent) or shift to the warm sand `#e6cdb0` (m4) *revised* | **shift**, judged at gate 0 | S1 |
| O61 | On night the primary becomes the paper plate; the glow is retired; «Bordo d'oro» is a static gilt edge (M3) *new* | yes | F4 |
| **Imagery** ||||
| O20 | Home image budget «door + 8» (deviation from CD V4 §5.6 «porta + 5») | yes | S1 |
| O21 | ~~The duotone vault layer, conditional~~ *withdrawn* (M2, m15) | — | — |
| O22 | Retire 13 of the 15 current Unsplash photographs from V5 placements (12 + the news fallback); `atelier-de-travail` only if its author can be recorded | yes | S1–S2 |
| O23 | Persona image: the man **seen from behind** (7594198, the same shoot as the council's 7594098); the front view and the woman (7584771) are identifiable (M13) *revised* | 7594198 | S1 |
| O24 | Login accent photograph (terrazzo steps) | no — the door alone | S4 |
| O25 | Commission Forum photography with releases for the `held` state | yes | S11 |
| O56 | Commission photography for the four doors, with releases; the stock set is the interim (M13) *new* | yes, budget now | S1 (interim), later swap |
| O60 | Istituzione image: 6949366 (the Forum loop 6951299, from the same room, then leaves the Forum page) or 32266781 (after its full-resolution check) (M2, M13) *new* | 6949366 | S1 |
| O26 | Academy course covers (licensed, per course) vs glyph tiles | glyph tiles until covers are funded | S10 |
| O27 | Remove the generic `hero` image fallback; AGAMI and network pages stop borrowing images | yes | P |
| **Motion** ||||
| O28 | The removed hero choreography is replaced by the one-shot arch light (MOTION D3) | yes | S1 |
| O29 | The hero current becomes four route lights that play **once** after the arch light (≈ 3.3 s), then rest; keyframes generated at runtime from the measured routes (MOTION D10; M5) *revised* | yes | F6, S1 |
| O30 | View Transitions on the public site only, **off by default** until the 6 + 6 re-measure at 120 ms (MOTION D4; m14) *revised* | yes | F6 |
| O31 | Busy buttons keep their label (MOTION D8) | yes | F4 |
| O32 | The 10-second copy enters the locked registry in fr / it / en / ar (MOTION D7) | yes | F5 |
| O33 | `motion-armed` set by `head.js` for fresh navigations only (MOTION D12) | yes | F6 |
| O34 | The `motion/mini` swap **and** the two scroll-linked effects to native CSS, **in F6** (MOTION D5; M9) *revised* | yes | F6 |
| **Information architecture and copy** ||||
| O35 | Six top items (four doors + Forum + Projet); «Actualités» inside Projet (D-U3) | yes | S2 |
| O36 | `description`, `image`, `image_alt` fields on `MenuItem` (CMS change) | yes | S2 |
| O37 | Public search with a per-language index built at deploy | yes, P2 | S2 (P2) |
| O38 | Locked strings split on their own separators («→», «;») for layout, with an equality test (D-U4) | yes | S1 |
| O39 | Hero secondary CTA: the Forum date until 2 October, then «Comment ça marche» (D-U11) | yes | S1 |
| O40 | Hide the News block when empty (D-U13) | yes | S1 |
| O41 | Latin digits on Arabic pages (D-U10) | yes | F1 |
| O42 | Forum states computed from dates (D-U5) | yes | S11 |
| O43 | Copy review: bottom-bar and rail short labels; «Intervenant»; «Mes pièces» vs «Mes documents»; sentence-case group titles; «À vous : n» and the ledger's group labels; question-8 counter; company CTA verbs; the door cards' two tasks | yes, one review | S5–S9 |
| O44 | One reassurance line on the login (the locked FAQ answer on data) (D-U6) | yes | S4 |
| O45 | Where the hero body paragraph goes on the phone; **the interim title's own setting** (Source Serif 4 28–32 px, one-line eyebrow) and **the door's floor at today's size** (M7) *revised* | chapter 01; yes | S1 |
| O58 | The public orientation questionnaire rebuilt on the «Ma situation» grammar (FM12), shipped with the home as step S1b (B4) *new* | yes | S1b |
| **Legal, product and engineering (P0 — before any platform gate)** ||||
| O46 | Publish the seven `JOURNEY_STEPS` and their sides on the public home (D-U9); **until then the orientation passage (four steps, no sides) is the public design, gated on 8770** (M16) *revised* | yes after legal review | S1 |
| O47 | A signed mapping of journey steps to responsible actors (MOTION D9) | when legal can sign; the motion waits for the data | S6 |
| O48 | One next action computed over all open obligations; one list of «ce qui est demandé» (UX_PLATFORM 5) | yes — P0 | T track |
| O49 | The orientation questionnaire inside the console for signed-in people; how it relates to «Ma situation» (UX_PLATFORM 6) | yes — P0 | T track |
| O50 | The NowPanel owns the primary action (UX_PLATFORM 1) | yes | S6 |
| O51 | Empty-state doctrine by scope (UX_PLATFORM 2) | yes | F4, S6 |
| O52 | Person-facing state transitions as intent buttons (and a permission check of today's `<select>`) | yes — P0 if the person sees the form | T track |
| O53 | Speculation Rules, after their own measurement | later | P |
| O62 | The Piece Ledger grouped by who holds the piece, 16 px marks, three hues (M11) *new* | yes | S7 |
| O63 | The phone action bar carries the Menu control at its inline end (M6) *new* | yes | S5 |
| O64 | Console-only CSS in a console bundle; replaced sheets leave in the step that replaces them; dead CSS deleted in F2; CI budgets for CSS and JS (M8, M9) *new* | yes | F2, F6 |
| O65 | New registry types and their owners — FM12, PX24–PX27, SW21, SW22, SC11, SC12; the community pages composed from existing types; the jurisdiction bar and the pilot-flow illustration retired (M15) *new* | yes | S1b, P1, P2 |
| O66 | Process: re-mint the QA sessions and delete (or keep, knowingly) the seven session rows the mobile lane added to `ile_qa`; browser tools write outside the repository; a before/after check per lane; the memory plugin's `.remember/` folder inside the repository (M18) *new* | yes | Phase 0 |

---

## 25. What I could not do, and why

- **No browser measurement by this role.** I made no browser run, no Lighthouse, no trace; every browser number in this document comes from a council report and says so (measured on a prototype, measured on the served pages, or estimated). One V5 choice ships only behind a measurement I could not run: the italic lead (§22.1). The revision pass added four offline measurements of its own, listed in §26.6 (wordmark subsets, the CSS bundle's composition, contrast and chroma of the changed colours, Pexels previews).
- **No 21st.dev call by this role, and Pexels only in the revision.** The first pass made no call to either; the red-team revision made 16 Pexels search calls and looked at 24 previews, with the key only in the request header (§26.6). The five curations made 169 lookups (159 `search` + 10 `get_inspiration`) and 93 `get_component` calls between them, and the motion and mobile lanes 6 searches and 4 retrievals — 175 lookups and 97 retrievals in all (`21ST_SEARCH_LOG.md`); `generate` and `iterate_generation` were never called by anyone. I merged their registers by script (600 register rows, 544 distinct candidates) — the parser reads the curators' tables, and a malformed row could be miscounted.
- **The classification of the 122 component types** (adapt / native / custom / unchanged) is my judgement; the rule is written at the head of the registry so another reviewer can re-run it.
- **Inherited limits, not closed here:** headless Chrome only (no real phone, no Safari, no Firefox — `animation-timeline` and cross-document View Transitions in Firefox were checked only through secondary sources); image judgements from ≈ 350 px previews (nothing may enter `CURATED` before the 14 full-resolution checks); no native Arabic reader; no colour-blind user test (Machado simulation only); fallback font metrics for Apple and Android not computed; Lucide glyph names not all verified against the live catalogue; the journey's actor data does not exist; the Forum `held` state needs photographs that do not exist yet.
- **Legal readings are not mine.** VALIDÉ's colour and word, the public use of `JOURNEY_STEPS`, the thresholds' captions, the steps → actors mapping and the release situation of identifiable people in stock photographs go to the owner and legal.
- **Process notes for the owner** (from the council, verified where I could; `RED_TEAM` M18): on 26 September a council agent's Playwright session created `.playwright-mcp/` inside the repository during the read-only phase (it is no longer present; it held an icon-specimen capture); the motion lane's 26 September captures drove the QA Chrome and deleted its local `sessionid` cookie (`MOTION` §13 item 13) — QA sessions need to be re-minted; the mobile lane added seven session rows to the local `ile_qa` database. **The read-only phase was therefore breached three times, and disclosed.** This revision also found, and discloses, a fourth writer: the memory plugin of the tooling writes into `.remember/` inside the repository (git-ignored; last written on 27 September). The repository's tracked files are clean at `c9a58d8`. The fixes are O66 and phase 0 of the plan; I did not delete the database rows or re-mint sessions (both change state the owner has not released).
- **The Forum date.** 2 October 2026 is five days away. No safe V5 plan ships the Forum's new states before it; they are designed for the `held` and `permanent` states.

---

## 26. Revisione dopo red team

**What happened.** An independent red team (`RED_TEAM.md`, same folder, 27 September 2026) reviewed this proposal and its six companion documents against the repository's own rules. Its verdict: *not ready for signature as written; the fixes are well defined and none needs a new direction.* It found **4 blocking, 19 major and 18 minor** issues, ten internal contradictions, and it named what must not be traded away: the CSP discipline, 0 React islands, law 2.2 and its frame test, the composited loader and its block test, the font diet, the contrast proof, the reduced-motion still states, every chip keeping its word, and a candid §25. This revision keeps all of those. It changed the seven final documents, added two OFL texts to `council/typography/fonts/` and three errata at the head of council reports, and wrote its own measurements and searches under `scratch/ecd/revision/` (the edit scripts in `scratch/ecd/revision/edits/`, the pre-revision copies in `scratch/ecd/revision/pre_redteam/`). The repository was only read.

**How to read the tables.** *Resolution* says what changed; *Applied in* names the sections (CD = this document, DS = `DESIGN_SYSTEM_V5.md`, PLAN = `IMPLEMENTATION_PLAN.md`, ICON = `ICON_SEMANTIC_MAP.md`, ASSET = `ASSET_USAGE_MATRIX.md`, MATRIX = `21ST_COMPONENT_MATRIX.md`, LOG = `21ST_SEARCH_LOG.md`); *Status* is one of **Resolved** (the specification now answers it), **Resolved — owner decides** (the default is the red team's side and the owner signs), **Resolved in process** (the gate or test exists; the work happens in that gate), **Partly resolved** (what is left is stated).

### 26.1 Blocking

| ID | Issue (red team) | Resolution | Applied in | Status |
|---|---|---|---|---|
| **B1** | VALIDE painted lapis with a filled disc and a check; done journey nodes with a check; «Validé» on the specimens — against the rule the repository enforces (`test_chips_registry.py`: `conforme` takes ink, no chroma, «no colour on this platform ever means approved») | The repository's rule is the default. `conforme` stays **ink**: inchiostro-900 mark and word on a carta-100 body (13.59:1; OKLCH chroma 0.024), inchiostro-400 edge; its mark is the **plain filled disc, no glyph** (the red team's «disc + bar» was not used: it reads as «minus» / «no entry»). Done nodes are filled ink dots with no glyph; step 5's glyph `clipboard-check` → `clipboard-list`; the Dépôt's success tick → the filed state's own mark. **The check rule**: a check marks only the person's own interface acts, never a piece, a step, a case or an outcome. Tests: `conforme` chroma ≤ 0.03, `STATUS["conforme"]` not a check, no check symbol in chips, journey nodes or the ledger; `test_chips_registry.py` unchanged. Lapis only if owner and legal sign it in writing before F4 and amend that test in the same commit (O14). The lapis tone stays for the information notice only. The specimens that say «Validé» are non-normative; gate 0 makes the normative chip board | CD §0, §1.4 law 7, §3 ruling 2, §4, §11, §12, §21, §24 O14 · DS §2, §3.2, §4, §4.1, §10.2, §10.4, §10.7, §11 (DS01, SW06, DS09), §12 test 8 · ICON §2, §3.3, §8 · MATRIX §2, §3.1 · PLAN F2, F4, phase 0 | **Resolved — owner decides** (O14; default ink) |
| **B2** | «Due portici» (two covered walkways, «la marche» steps, a vault, a loggia, a portico loop) sits on the forbidden-subject boundary: `IMAGE_LICENSES.md` forbids «porte/soglie» and «griglie/cancelli», and its precedents rejected a corridor for evoking thresholds | **No V5 photograph enters `CURATED` before the owner's written ruling on the scope of F15** (arcades, covered passages, steps, vaults — O54), recorded in `IMAGE_LICENSES.md` §1; until then the prudent reading applies. The Casablanca frame is **rejected** (its shutters close shop entrances); «la marche» takes the terrazzo steps' owner flag; the vault is dropped; the loggia is replaced; the portico loop is held. A **non-architectural fallback is ready**, found in this revision through 16 Pexels searches (previews only): the diptych **«Lo stesso gesto»** — a hand guiding a chisel through cedar (30563520, Moussa Idrissi) \| a hand guiding a chisel on marble (6713855, Tima Miroshnichenko), alternates 30563521 and 12148970; the Forum band fallback 6787057 (Artem Podrez); the Istituzione replacement 6949366 or 32266781; the Persona back view 7594198 | CD §0, §1.2, §1.3, §5, §10, §20, §21, §24 O54, O60 · ASSET binding rules, §2, §3, §6, §8 · DS PX11, PX20 · MATRIX PX11, PX20 · PLAN phase 0, S1, §8 | **Resolved — owner decides** (O54); S1 no longer waits for the ruling |
| **B3** | No composed picture of any V5 screen exists; the owner would sign 53 decisions on prose — the process that produced «not premium enough» | **Gate 0 «La prova»** before F1: static, CSP-clean, self-hosted comps built outside the repository (`C:/tmp/ile_v5_council/proof/`) with the V5 fonts and amended tokens — the home's first three screens at 1440 and 390 in fr and ar, interim and phase 3; the login; a mid-case dashboard; «Mes pièces»; the normative chip board and the ledger at 1× with a CVD simulation; the passage from the level geometry in LTR, RTL and reduced motion; the hero's first breath and the login's key frozen frame by frame; two or three photographs at full resolution after O54; the reference-site side-by-side. **The owner signs the pictures (O59), then the decisions** — §24 now opens with that order | CD §0 preface, §24 preface and O59 · PLAN §1, §1b phase 0, §9 | **Resolved in process** — the comps themselves are gate 0's work and were **not** built in this revision (their photographs depend on O54; ≈ 6–8 days) |
| **B4** | The hero's locked primary leads to the V2 public questionnaire — full-page POST, a **percentage bar**, inert `hx-*`, plain radios, no busy state — which the finals did not design | Registry type **FM12 «Public orientation questionnaire»** on the «Ma situation» grammar (one question at a time, «Question n sur N», OptionCards, the L2 key at submit, focus on the arriving question, the thread per step, the result on SW21, complete without JavaScript); plan step **S1b** (≈ 3–4 days) shipped with S1; the acceptance test `test_questionnaire_no_percentage.py` (no `%`, no `<progress>`) | CD §20, §21, §24 O58 · DS §11 FM12, §12 test 13e · MATRIX row 122 · PLAN §1, S1b, §9 | **Resolved** |

### 26.2 Major

| ID | Issue (red team) | Resolution | Applied in | Status |
|---|---|---|---|---|
| **M1** | The brand name in two serif drawings 40 px apart (the Newsreader lock-up, the Source Serif H1); the project page does the same | Every rendering of the trademark name uses **«ILE Wordmark»** — the lock-up, the hero H1, the project H1, the footer's legal line, the rail — in capitals by CSS (the locked text unchanged). D-U1 option a is recommended *in the wordmark face*: the name as an engraved 32–40 px line, the locked promise as the Source Serif display line. Measured in this revision from the pinned master: the subset is **11** code points (not 13) and 1,748 B; an `opsz` 36 display instance 1,740 B, `opsz` 72 1,756 B; a mixed-case subset would add 1,056 B and is not needed. Law 2 amended; `test_brand_face.py` reads the computed face on public, console and `/ar/` pages | CD §0, §1.4 law 2, §2, §9, §24 O6, O11 · DS §3.3, §5, §11 BI01, §12 test 3 · ASSET §1, §4 · MATRIX BI01 · PLAN F1 | **Resolved** |
| **M2** | The arch or door in ≈ 15 places, against the CD's own «the arch belongs to the door» | **An allow-list with a test** (`test_arch_budget.py`): the lock-up and favicon, the hero, the login (with its phone band), the error pages, the journey's threshold B. Removed: the vault layer (O21 withdrawn), the footer watermark, the threshold reveal D-U7 (O4 withdrawn), `ile-arch` at step 6 (→ `building-2`), the door crops in panel heads (→ the L2 key), the Istituzione loggia; the arcade diptych and the portico loop held for O54 | CD §0, §1.4 law 5, §4, §5, §6, §11, §17, §20, §21, §23 · DS §10.7, §11, §12 test 13a · ICON §1, §3.3 · ASSET §1, §2 · MATRIX §3.1 | **Resolved** — the count is checked again on the gate-0 pictures |
| **M3** | Gold light in ≈ 10 contexts, glow on every primary, light-cyan gradients on navy, glass on content over mesh and grain: a fintech / crypto vocabulary | Gold light in **three contexts only** (the arch once after LCP; the journey; the door frame once at the entrance) — removed from the CTA, the header mark, the rail tile and panel heads. `--shadow-glow(-dark)` retired; primaries **flat** (laguna-650, 5.29:1; hover one step); **on night the primary is a paper plate** (carta-25, ink 15.56:1) instead of the cyan gradient; «Bordo d'oro» a **static** gilt edge. Glass on the two sticky bars only; the legend, the login panel and the micro-visual on a solid night plate; scrims without blur; the mesh in the hero only; the door's glow re-tint dropped; station rings of light → 2 px strokes | CD §0, §1.3, §3, §6, §7, §8, §9, §11, §13, §17, §18, §21, §23, §24 O61 · DS §3.4, §4, §8, §9, §10.1, §10.6, §10.7, §11, §13 · MATRIX §3.1 | **Resolved** — gate 0 judges it on pictures; the paper plate has a stated fallback (PLAN §8) |
| **M4** | The passage route rises from Morocco (low) to Italy (high): a growth chart and a hierarchy between equal partners | A **level** line, the two shores at the same height, their names as words at the two ends, the thresholds as vertical hairlines, stations without halos; the light needs only x (lighter CSS). LTR, RTL and reduced motion re-frozen at gate 0 | CD §11, §21 · DS §4, §10.7, §11 PX07 · MATRIX PX07 · PLAN phase 0, F6, S1 | **Resolved** — frames to re-freeze at gate 0 |
| **M5** | The hero's four lights loop forever (no pause control, WCAG 2.2.2), were not prototyped, and build-time keyframes cannot follow routes `home.js` rewrites at every width | The lights play **once** after the arch light — ≈ 3.3 s in all (≤ 5 s), then rest: no loop remains on the home, and `--motion-ambient` is deleted. Keyframes are sampled **at runtime** from the live paths (`getPointAtLength`, 12 samples per route, once per layout, idle after LCP; WAAPI on transform/opacity). Prototyped and traced in phase 0 / F6 before S1; if the sampling ever shows as a long task, the geometry is frozen | CD §6 ruling 2, §9, §21, §22.3, §24 O29 · DS §1.2, §3.5, §9, §10.7, §11 FB07 · MATRIX PX01, FB07 · PLAN phase 0, F6, S1 | **Resolved** — the prototype is phase 0's |
| **M6** | On phones the action bar replaces the bottom bar and the top ≡ is gone: no Menu on the case file or «Ma situation» | The action bar carries **«Menu» (44 px) at its inline end** — the same place as in the bottom bar (chosen over the red team's «start» for WCAG 3.2.3 consistency); chrome 118 px ≤ 120; `test_phone_menu.py` on every console template | CD §8, §19, §24 O63 · DS §6, §11 SC04, §12 test 13f · MATRIX SC04 · PLAN S5 | **Resolved** |
| **M7** | «Mobile corrected, door +81 %» holds only for phase 3 at nominal viewports; the interim door shrinks below today's and the interim hero reaches 101–108 % (119.5 % at 320 × 568) | §0 and §22.4 restated for both phases; the interim title gets its own setting (Source Serif 4 28–32 px, one-line eyebrow); the door's floor = **today's door at the same viewport** (223 px at 390 × 844), not 136 px; a stated precedence (primary → door → peek); the acceptance tests run in both phases at the nominal and the small viewports plus 320 × 568 | CD §0, §9, §19, §22.4, §24 O45 · DS §3.3, §3.6 · PLAN phase 0, S1 | **Resolved in process** — the interim numbers are measured at gate 0 |
| **M8** | The CSS estimate (+8–11 KB gz) is not grounded; with old sheets kept until P4 the render-blocking bundle can pass 50 KB gz | **Measured in this revision** (read-only, the repository's esbuild in transform mode): `dist/main.css` 217,057 B, 36.0 KB gz; `v4/workspace.css` and `v4/wizard.css` weigh ≈ 6.4 KB gz of it (29.7 KB gz without them). Console-only components go to `dist/console.css`; each replaced sheet leaves in the step that replaces it; the dead CSS is deleted in F2; `test_css_budget.py` holds `main.css` ≤ 45 KB gz (red line 50) with per-family deltas at each gate. Re-grounded estimate after phase F: ≈ 38–44 KB gz — **an estimate**: the net of the new component sheets against the ones they replace is not measured | CD §0, §6 · DS §1.2, §12 test 13c · PLAN §3.1, F2, P4, §8 | **Resolved** (the estimate is labelled as one) |
| **M9** | JS headroom 4.5 KB against unbudgeted modules; the `motion/mini` saving deferred to phase P | The `motion/mini` swap and the two scroll-linked effects to native CSS move **into F6**, before any flagship: −16.6 KB gz per page (the council's probes) → ≈ 19.4 KB gz, ≈ 25–28 expected on the home with V5 (estimate); search and «Aller à…» load on first use; `test_js_budget.py` per page type ≤ 45 KB gz | CD §0, §6 ruling 6, §24 O34 · DS §12 test 13d · PLAN §1, §3.1, F6, P3 | **Resolved** |
| **M10** | The loader animates the locked mark (the key turns, the tricolour planes part, a crack of light) and «unlocks» during waits whose outcome is legal | **The planes never move; no crack of light.** L1 = the key's two half-turns and the frame light, **one cycle**, in one place: the entrance stage on submit. Outcome-bearing requests (situation recalculation, assessment, eligibility, scan verification) get L2/L3 only — listed in `loader.js`, tested. `BRAND_ASSETS.md` §1 already says «se si muove, si muove una volta, all'ingresso»: the one-shot is that sentence taken literally, so the brand rule needs no amendment; O1 asks the owner to confirm the reading (if refused, L1 is withdrawn); any loop or other context would need §1 amended in writing before F5 | CD §0, §1.1, §1.3, §6, §17, §18, §21, §24 O1 · DS §3.5, §4, §10.7, §11 FB01/FB02, §12 test 5 · ASSET §1 · MATRIX FB01 · PLAN F5, S3, S4 | **Resolved — owner decides** (O1) |
| **M11** | 12 px ledger pips separate registers by a one-pixel micro-glyph; eight-colour rows read as candy | Marks at **16 px**; the ledger **grouped by who holds the piece** — «À vous» · «En cours» · «Réglées» — with labels and counts; **colour = the group** (cotto-600 5.98:1, ink-600 7.17:1, ink-900 16.23:1), **shape = the state**; three hues at most; nullo not drawn; a CVD simulation of the rendered ledger at 1× in gate 0 and S7 | CD §12, §24 O62 · DS §4, §11 SW07 · MATRIX SW07 · PLAN phase 0, S7, §8 | **Resolved** |
| **M12** | The section grammar (gold hairline + tracked eyebrow + serif title), the portico panel's «featured card» and the drawer's anatomy match agamieuromed.org elements — principles only is the rule | The eyebrow device replaced (a 14 px `ile-steps` micro-mark in ink + a sentence-case eyebrow; no gold hairline, no tracked capitals); the panel recomposed (a serif head line over the sub-links; the photograph as the panel's full-height field, no caption, no card); the drawer kept — its order is dictated by use — and every public chrome surface passes a **signed side-by-side differentiation review** against `captures/ref_agami_*` at gate 0, S1 and S2, on six criteria | CD §7, §20, §21 · DS §11 PC03, PC07, PX04 · MATRIX §3.1 · PLAN phase 0, §3.3, S1, S2 | **Resolved** — the drawer is judged in the review rather than changed now |
| **M13** | An identifiable man chosen as «ambiguous» on the Persona door; ubiquitous Pexels studios; a named Padua monument standing for «Institutions» | Persona → the **same shoot seen from behind** (7594198); every other face after a **legal reading, door by door** (O55); **commissioned photography for the four doors** (O56), the stock set as an interim; Istituzione replaced (6949366 or 32266781, O60); no alt text names a real building; studio concentration acknowledged; the Moroccan-reader review extended to imagery | CD §5, §10, §24 O23, O55, O56, O60 · ASSET binding rule 5, §2, §6 · PLAN phase 0, §8 | **Resolved — owner decides** (O55, O56, O60) |
| **M14** | «Il gradino» on every surface — up to three or four times on one page | **One full instance per page** (the band on the home, the rail block on inner pages); a one-line link in portico panels, the drawer and the footer; `test_gradino_once.py` | CD §1.3, §7, §20, §24 O5 · DS §11 PX08, PC03, PC07, PC11, §12 test 13b · MATRIX §3.1 | **Resolved** |
| **M15** | Live surfaces with no V5 component: community, prose, glossary, living cards, account pages, the assessment outcome, non-person homes, the back-office; the jurisdiction bar and pilot-flow diagram undecided; the generic navigation card missing | **Nine registry types added** — FM12, PX24 prose, PX25 glossary, PX26 topic cards, PX27 generic navigation card, SC11 account settings, SC12 back-office (Unfold) mapping, SW21 outcome + sources, SW22 non-person homes (113 → 122); the community pages composed from SW13, PX14 and SW11; the jurisdiction bar and the pilot-flow illustration **retired**; scheduled in S1b, P1 and P2, each with an owner by role (PLAN §6; O65) | CD §0, §14, §20, §24 O65 · DS §11, §12 · MATRIX §1, rows 114–122 · PLAN §1, P1, P2, §9 | **Resolved** |
| **M16** | The public signature (seven stations) needs legal D-U9 and the closed gate G3: visitors may never see it | The **orientation passage** — the passage and «S'orienter» as one chapter, the four orientation steps on the level line (the neutral `ORIENTATION_STEPS` on the interim, the locked sentence split on «→» in phase 3), no sides — is the **primary public design**, prototyped and gated on 8770 first; the seven stations are the upgrade | CD §0, §1.3, §11, §20, §24 O46 · DS §11 PX07 · MATRIX PX07 · PLAN S1 | **Resolved** |
| **M17** | A tricolour filet on the institutional notice stated as law, absent from the owner's decisions, against V4 DS §1.8 and `BRAND_ASSETS` | Removed from law 1 and from the notice tokens; added to §24 as **O57**, recommended **no** | CD §1.4 law 1, §21, §24 O57 · DS §4, §10.8 · ASSET §1 | **Resolved — owner decides** (default: no filet) |
| **M18** | The read-only phase was breached (a `.playwright-mcp/` folder in the repository, a QA cookie deleted, 7 session rows added), while reports still open with «not modified» | Facts restated in §25, with one more writer found in this revision and disclosed: the memory plugin writes `.remember/` inside the repository (git-ignored; last written on 27 September). Process fixes in PLAN §0.5 (browser outputs outside the repository; a before/after `git status --porcelain --ignored` with `GIT_OPTIONAL_LOCKS=0` and a session count per lane) and phase 0 (O66: re-mint the QA sessions; delete or keep the seven rows; decide on `.remember/`). **Errata** added at the head of `council/MOTION.md`, `council/MOBILE_UX.md` and `council/ICON_SEMANTIC_MAP.md` | CD §25, §24 O66 · PLAN §0, §1b · the three council reports | **Partly resolved** — the database rows and the QA sessions change state the owner has not released, so I did not touch them |
| **M19** | «One L1 per view» is checked per template; at runtime several async regions can each start an L1 (51–67 ms tasks in the stress runs) | L1 is now confined to the entrance stage (one per page by construction) **and** a singleton in `loader.js` (a second request is served as L2/L3), with a unit test and a gate trace with every async region open | CD §6 · DS §10.7, §11 FB01, §12 test 5 · PLAN F5 | **Resolved** |

### 26.3 Minor

| ID | Issue | Resolution | Applied in |
|---|---|---|---|
| m1 | `ile-steps` (three stacked lines) is a near-twin of `menu` and `list-filter` at 14–16 px | Redrawn as a stair profile (three treads and risers) | ICON §1 · CD §4 |
| m2 | `ile-arch` at threshold B **and** step 6; `compass` at steps 1 **and** 2 | `ile-arch` at threshold B only; step 6 `building-2`, step 2 `signpost` (both SHARED with the concepts they are) | ICON §3.3, §6 · CD §4 |
| m3 | A 4 px rhythm with 15/22 and 11/14 line-heights (11 px Arabic); «44 px for every control» beside 36 px tracks and 24 px chips | 15/24; 12/16 (13/20 in Arabic); the target rule restated: 24 px floor, 44 px for primary and touch targets, coarse-pointer growth | DS §3.6, §5, §6, §10.5 · CD §7, §8, §15 |
| m4 | «Audience accents never on paper» vs route-colour nodes in the phone list; Persona's accent equals the interactive accent | Glyphs in ink on paper; Persona shift proposed to `#e6cdb0` (11.34:1; ΔE ≥ 6.5 from the night state words, 7.0 from `oro-300`), judged at gate 0 (O19) | CD §3, §10, §19 · DS §2, §3.1 |
| m5 | Glass discs on photographs; a costly full-screen scrim blur | A solid night disc (notte-900 .72; the glyph ≥ 6.16:1 over a white pixel); no scrim blur anywhere | CD §3, §5, §15 · DS §3.1, §3.4 |
| m6 | Council specimens show patterns V5 forbids («Validé», ordinals, «3/7 étapes», a MONTANT column…) | Declared **non-normative** (they stay in `council/` as history); gate 0 produces the normative boards | CD §12, §26 · PLAN phase 0 |
| m7 | «72 adapted from 21st» counts native select, checkbox, switch, breadcrumb and pagination | Relabelled «Native · reviewed on 21st» (5); Adapt 68 | DS §11 · MATRIX §1 · CD §0 |
| m8 | Panel photographs fetched on first hover (pop-in on slow 4G); a scrim on a mere hover | Idle, low-priority prefetch ≥ 80 rem after LCP, fade-in on load; the scrim only on click, tap or keyboard | CD §7 · DS §10.5, §10.6 · PLAN S2 |
| m9 | The preview drawer's `pushState`: Back and focus unspecified | `popstate` closes the drawer and returns focus to the row title | CD §12 · DS §10.6, DS08 |
| m10 | The wordmark subset falls back to Newsreader; `.rail__wordmark` reads `--f-serif`, which the console re-points | `unicode-range` on the subset; every name class reads `--f-wordmark`; the computed-face test | CD §2 · DS §3.3, BI01, test 3 |
| m11 | «Moved in the template» implies duplicated markup, unchecked against the locked-copy tests and duplicate ids | Specified: rendered once in each place, one shown by a media query, no duplicate `id`, the equality test counts the visible instance | CD §19 · PLAN S1 |
| m12 | Zellige, lanterns and a Padua landmark are mild cultural or tourist signifiers | The Moroccan-reader review extended from type to imagery; the landmark removed | CD §5 |
| m13 | «La soglia» names the concept, the journey and the navigation thread; many Italian code names | The thread renamed «il filo»; one glossary with neutral code names (§26.9) | CD §6, §26.9 · DS PC13, §10.7 · MATRIX PC13 |
| m14 | View Transitions measured only at 180 ms | Off by default until the 6 + 6 re-run at 120 ms | CD §6 ruling 4, §17, §24 O30 |
| m15 | The vault layer is decorative, adds arches and would become the LCP element | Dropped | CD §5, §9, §21 · ASSET §2, §8 |
| m16 | OFL texts for IBM Plex Mono and the Newsreader subset missing | **Added**: `council/typography/fonts/OFL-Newsreader.txt`, `OFL-IBMPlexMono.txt` (copied from the pinned masters' licence files) | ASSET §1 · PLAN F1 |
| m17 | Vazirmatn comes from a Persian-script family, for a Moroccan audience | The Moroccan-reader review is blocking for `/ar/`; Noto Sans Arabic kept as the fallback candidate | CD §2, §24 O10 |
| m18 | «`generate` never called» rests on each lane's statement | Recorded as a declaration, not a verification (`get_usage` reports entitlement, not calls) | LOG §4 · MATRIX §1 |

### 26.4 The ten contradictions (`RED_TEAM` §5), resolved

| # | Said | And also said | Now |
|---|---|---|---|
| 1 | No ticks on stations | Done node = a lapis fill with a check | Done = a filled ink dot, no glyph; no check anywhere on the journey |
| 2 | The word stays «Valide» | Chips labelled «Validé» on the specimens | «Valide», in ink; the specimens are non-normative |
| 3 | The arch belongs to the door | ≈ 15 arch occurrences | An allow-list of five contexts and a test |
| 4 | Glass never on content | Glass discs on photographs | Solid night plates; glass on the sticky bars only |
| 5 | Audience accents never on paper | Route-colour nodes on paper rows | Glyphs in ink on paper |
| 6 | 44 px minimum for every control | 36 px tracks and rows, 24 px chips | 24 px floor, 44 px for primary and touch targets |
| 7 | Every line-height a multiple of 4 px | 15/22, 11/14 | 15/24, 12/16 (13/20 in Arabic) |
| 8 | The tricolour lives in the mark | A tricolour filet on the notice | No filet (O57) |
| 9 | No growth curve | A rising route | A level route |
| 10 | Every loop can be paused or lasts ≤ 5 s | An infinite hero loop | The first breath ends in ≈ 3.3 s; no loop on the home |

### 26.5 Hard constraints — status after the revision

| Constraint | Status | Evidence / what is left |
|---|---|---|
| CSP `script-src 'self'`, `style-src 'self'`, no inline | **PASS (spec)** | runtime route-light keyframes go through WAAPI from a bundled module, like the CSSOM writes already specified; the gate-0 comps must be CSP-clean too |
| Everything self-hosted | **PASS (spec)** | unchanged; the Unfold mapping loads Host Grotesk from `static/` |
| No Next.js / React rewrite | **PASS** | route C = 0 |
| 21st: no `generate` / `iterate_generation` | **PASS (declared)** | no 21st call in this revision; recorded as a declaration (m18) |
| Wordmark font not removed | **PASS** | the font stays and now draws the name everywhere (M1) |
| Editorial image rules | **PASS by default, owner ruling pending** | the prudent reading applies until O54; the Casablanca frame rejected; nothing curated; the fallback set seen only as previews |
| Licence and author recorded | **PENDING** | authors listed for every candidate, including the fallback set; recorded at curation |
| LCP ≤ 2.5 s · CLS ≤ 0.10 · INP ≤ 200 ms | **PLAUSIBLE, UNPROVEN** | the vault removed (no new LCP candidate); budgets now held by CI tests; the gates measure |
| No avoidable long task > 50 ms | **SPECIFIED** | L1 singleton + all-regions trace (M19); runtime sampling in an idle callback, traced in phase 0 (M5) |
| WCAG 2.2 AA, keyboard, reduced motion | **SPECIFIED** | 2.2.2 (no loop), 3.2.3 (Menu kept), small-size legibility (16 px marks, 12/16 labels, the target rule) |
| RTL Arabic | **SPECIFIED** | the level route mirrors; 13/20 Arabic rail labels; the Moroccan-reader review blocking |
| Reference sites: principles only | **SPECIFIED** | two elements changed, one under a signed review (M12) |
| Repository read-only in this phase | **HELD in this revision; BREACHED earlier, disclosed** | this revision only read the repository (esbuild in transform mode, `git status` without locks); the earlier breaches and the `.remember/` writer are disclosed (M18) |

### 26.6 What this revision measured and searched (and how)

- **Wordmark subsets** — `scratch/ecd/revision/wordmark_build.py` (fontTools 4.60.2, the pinned `Newsreader[opsz,wght].ttf` master): the council's subset holds 11 code points; rebuilt at `opsz` 20: 1,748 B; `opsz` 36: 1,740 B; `opsz` 72: 1,756 B; mixed case at `opsz` 20: 2,804 B. (Font sizes in this document are KiB, as the typography lane's.)
- **The CSS bundle's composition** — `scratch/ecd/revision/css_measure.cjs`: each source sheet of `static/css/main.css` minified with the repository's own esbuild in *transform* mode (nothing written in the repository) and gzipped at level 9: `dist/main.css` 217,057 B → 36,014 B gz; the concatenated minified sheets 36,048 B gz; without `v4/workspace.css` 30,880 B; without it and `v4/wizard.css` 29,666 B. (CSS sizes are kB of 1,000 B; the council's «35.8 KB» for the same file came from another compressor.)
- **Colour** — `scratch/ecd/revision/colour_check.py`: WCAG contrast and OKLCH / OKLab values for `conforme` in ink, the flat and paper-plate primaries, the solid night disc, the Persona candidates and the ledger groups. The full `verify_tokens.py` was **not** re-run on the amended file (F2 does it).
- **Photographs** — 16 Pexels search calls (14 distinct queries, tags `rt_*`) through the council's `scratch/pexels_tool.py` (the key only in the request header, never printed) and 24 previews looked at on three contact sheets (`scratch/ecd/revision/sheet_*.jpg`); nothing downloaded at full resolution, nothing curated.
- **Repository checks** — reads of `tests/frontend/test_chips_registry.py`, `static/css/v3/chip.css`, `apps/core/chips.py`, `docs/design-v2/BRAND_ASSETS.md`, `docs/IMAGE_LICENSES.md`, `templates/pages/home/_orientation.html`, `apps/pages/services.py` (`build_orientation`), `apps/cms/templatetags/cms_nav.py` (`{% brand %}`), `config/settings/base.py` (`UNFOLD`), `scripts/build_css.mjs`; `git status --porcelain --ignored` with `GIT_OPTIONAL_LOCKS=0`.

### 26.7 What remains open, and why

1. **The composed screens (B3) do not exist yet.** They are gate 0's work (≈ 6–8 days) and need the owner's F15 ruling for their photographs; this pass revised the specification they will be built from.
2. **The F15 scope (O54), the legal reading on faces (O55), VALIDE (O14), the filet (O57), the loader reading (O1)** are the owner's and legal's. Every default in the text is the prudent one.
3. **The fallback photographs** were judged on ≈ 350 px previews only; their full-resolution checks are listed in `ASSET_USAGE_MATRIX.md` §6.
4. **Not prototyped here:** the level route and its frames (M4), the runtime-sampled route lights (M5), the interim phone hero with its own title setting and the door floor (M7). All three are phase-0 items.
5. **Estimates, labelled:** the public CSS after phase F (≈ 38–44 KB gz), the public JS on the home with V5 (≈ 25–28 KB gz), the dead CSS's weight. The CI budgets will measure them.
6. **The Persona accent** (`#e6cdb0`) is a computed candidate; whether it competes with the gold of the key is a visual question for gate 0.
7. **The process fixes that change state** — the seven `ile_qa` session rows, the QA Chrome's sessions, the `.remember/` folder — wait for the owner (O66).
8. **The council's specimens** were not regenerated; they are declared non-normative.

### 26.8 Conditions for signature — the red team's order, with their status

1. **B1** — the default reversed to ink, no checks, «Validé» purged from anything normative → **done in the text**; O14 signs it.
2. **B2** — the owner rules on F15; the shortlist re-run under the ruling; a fallback set exists → **the fallback set exists; the ruling is O54.**
3. **B4** — FM12 and S1b → **done.**
4. **M1, M2, M3, M4, M14** applied to the specification → **done.**
5. **B3** — the gate-0 comps built with the amended specification; the owner reviews the pictures → **specified; to build.**
6. **M5, M6, M7** amended, with the interim and small-viewport cases in the acceptance tests → **done in the text; M5 and M7 prototyped in phase 0.**
7. **M8, M9, M19** — CI budgets, the swap and the dead-CSS deletion pulled into phase F, the L1 singleton → **done in the text.**
8. **M10, M12, M13, M15, M16, M17, M18** — decisions in §24, registry types added, process fixes → **done in the text; O1, O55, O56, O57, O60, O66 await the owner.**

Only then do the §24 decisions go to the owner — in the order §24 now gives.

### 26.9 One glossary — names in the documents, neutral names in the code (m13)

| Name in the documents | What it is | Code name |
|---|---|---|
| «La soglia» | the V5 concept, and the journey component that makes it visible | `journey` (public: `journey--public`; console: `journey-rail`) |
| «La porta» | the owner's door stage | `doorway` (existing) |
| «La luce» | the gold travelling light | `light` |
| «La chiave che gira» | the branded wait: L1 (entrance), L2 (key), L3 (skeleton) | `loader--door`, `loader--key`, `skeleton` |
| «Il filo» (formerly «Soglia») | the 2 px navigation thread | `nav-thread` |
| «I cerchi» | the status marks | `status-mark` |
| «Il registro» | the Piece Ledger | `ledger` |
| «Dépôt» | the upload flagship | `upload` |
| «Il gradino» | the anti-fraud step | `antifraud-step` |
| «Bordo d'oro» | the signature CTA | `btn--signature` |
| «Il portico si apre» | the portico panel (mega-menu) | `nav-panel` |
| «Il varco» | the entrance layout (login and its sub-pages) | `entrance` |
| «Due rive» — «Due portici» / «Lo stesso gesto» | the two-shore diptych and its two variants | `diptych` |
| «Una schermata» | the phone hero, Solution A | `hero--phone` |
| «La prova» | gate 0: the composed screens | — (a phase, not code) |
