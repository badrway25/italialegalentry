# V5.4 EXECUTION PLAN — Italy Legal Entry™ design V5

The council's plan · Executive Creative Director + Product Architect, one voice · 4 October 2026 · **final** (label
plan-final): both red teams applied, resolution in §8.
Binding: the owner's directive of 4 October 2026, 20:20, «EXECUTION MODE — BUILD, DECIDE, SELF-REVIEW»
(`C:/tmp/ile_v5_council/directives/V5_4_EXECUTION_MODE.md`, cited V54 l.N). Earlier directives V5.1–V5.3 stay as context
where V5.4 does not override them. This plan supersedes `IMPLEMENTATION_PLAN.md` §1 (owner signatures per phase) and its
gate protocol where they conflict; that file's F/S content remains the engineering reference.

**Inputs.** The five plan maps in `C:/tmp/ile_v5_council/.work/v54-plan/` (`foundation.md`, `product.md`, `decisions.md`,
`platform.md`, `surfaces.md`), the two red-team reports beside them (`RED_TEAM_DESIGN.md` = RTD, `RED_TEAM_ENGINEERING.md`
= RTE; findings cited RTD-B1, RTE-M4 …), and the sources they cite, re-read where a decision needed them.
**Abbreviations.** P/ = `C:/tmp/ile_v5_council/proof/` · R/ = `C:/tmp/ile_wt/design-research-v5/docs/design-v5/` ·
Q/ = `C:/tmp/ile_wt/qa-v5/docs/design-v5/QA/` · W/ = `C:/tmp/ile_wt/design-v5/` (the product branch) · E/ =
`C:/tmp/ile_v5_council/evidence/v54/` (heavy evidence, outside every repository). In R/: DL `DECISION_LOG`, RS
`RESEARCH_SYNTHESIS_V52`, TS `TASTE_SYSTEM`, TR `TYPOGRAPHY_REVIEW`, MS `MOTION_SYSTEM`, EM `EMIL_SKILL_INTEGRATION`, IC
`ICON_SEMANTIC_MAP`, IA `IMAGE_ART_DIRECTION`, AUM `ASSET_USAGE_MATRIX`, UPu / UPl `UIUX_PRO_MAX_AUDITS_public` /
`_platform`; in R/research/: LS `LOADER_SIGNATURE`, PC `PLATFORM_COLORS`, NV `NAVIGATION`, DW `DOCUMENT_WORKSPACE`, JS
`JOURNEY_SIGNATURE`, HE `HERO_HE`, HEB `HERO_HE_BRIEF`, HF `HERO_FINAL_BRIEF`, BX `BENCHMARKS_external`, RRT
`RESEARCH_RED_TEAM`; in Q/: Hd · Ht · Hm · Hp · Ha = `hero-council/he_design · he_taste · he_motion · he_performance ·
he_a11y-mobile-rtl`, PFR `PERF_FIRST_RENDER`. In W/: DS `docs/design-v5/DESIGN_SYSTEM_V5.md`, CDV
`docs/design-v5/CREATIVE_DIRECTION_V5.md` (the research cites it «CD §n»), DS 2026 `docs/design/DESIGN_SYSTEM_2026.md`,
A11Y `docs/ACCESSIBILITY.md`, BA `docs/design-v2/BRAND_ASSETS.md`, **DL54 `docs/design-v5/DECISION_LOG_V54.md`** — V5.4's
own decision log, created by W1-0 with the entries of §8.3; where DL54 and an R/ rule disagree, DL54 binds the reviewers.
«Dnn» = a row of `decisions.md`. «CD» alone is the Creative Director.

**How to read it.** §1 settles every delegated decision in the form «compared X / Y / Z internally; the council chose Y
because …; evidence: …». §2 is how V5 enters the product. §3 is what the orchestrator launches: per wave, a numbered list of
workflows with their families, owned files, pages, gates and councils. §4 is what the owner sees. §5 is how each family is
run, §6 how it is reported, §7 what can go wrong and what is left open, §8 how each red-team finding was resolved. Nothing
here asks the owner to choose a design. The owner items (classes A–E of V54 l.7) are listed once, in §1.19.

---

## 0. The plan in fifteen lines

1. V5 enters design-v5 **in place, alias-first, family by family** (the V4 precedent). The owner's preview 8780 serves a
   separate worktree pinned to the last green tag. main stays V4 — the control on 8770 / 8771 / 8772 — until an explicit
   integration milestone, which is the owner's call (class D).
2. **Wave 1** brings the foundation into the real product (tokens, type, colour, corners, icons, core components, motion
   and the loader), scored on specimen boards, and turns 8780 into the live V5 product. **Wave 2** builds the flagships
   (overlay system, login, navbar, the hero's port, the home under the hero). **Wave 3** the platform and the public
   interior. **Wave 4** mobile, RTL, motion, performance and integration readiness.
3. **Type «Una voce»:** Host Grotesk for everything; the wordmark is the only serif; ILE Mono for references; Vazirmatn
   for Arabic. It is the build default under test: A-bis is ranked against it, blind, on the composed home (W2-E).
4. **Colour:** «En examen» in lapis (no violet left); broken edges and hatch at 3 : 1; glass 0.94; night marks re-solved;
   VALIDE in ink with no check; no tricolour filet.
5. **Corners «Lo spigolo»:** 2 · 4 · 6 · 8 · 12 · full, one scale for both worlds, **at most three values on any screen**;
   the arch is the only large curve.
6. **Loader «Lume»:** one gesture across the sign-in — on submit the key turns once and holds, with no light; the lit
   doorway plays on the arriving console page, once per session and only after a successful sign-in. L2: one key turn,
   then hold. L3: «Mandata»'s quiet seat, on asynchronous fragments only. Nothing loops.
7. **Signature CTA: CTA-B «Soglia»,** on the hero's primary only, once per page. Every other primary is flat.
8. **Reserved area: «la targa»,** in the letterhead's end zone in both states, flat.
9. **Navbar «Il portico»:** the owner's Fase 3 anatomy, **8 | 4 with the photograph at the end**, refined — content-width
   panel, one panel per door, whole texts, one travelling indicator, a full keyboard model, the phone sheet on the overlay
   system, and a «richer than Fase 3» check.
10. **Login «Le vie convergono al varco»:** route lights converging into the door, and a stage that **answers the person**
    (focus, a valid address, the password, the key); «la lastra» fields; a flat CTA that holds the key.
11. **Overlays:** one native system — tooltip, popover, modal, drawer, sheet — built on `overlay.js` + `overlays.css`; the
    portico panel uses its primitives.
12. **Cards:** no card board. The system orders priority, disclosures fold secondary content, filters live in the URL; the
    report shows the value matrix.
13. **Hero:** built by the hero-final workflow in `P/research/hero/he/`. It enters the product through a port family in
    Wave 2, with a parity check on re-held frames. Its door rests ajar after the opening: taken under V54 l.9, said in
    words in the report.
14. **Every family runs one loop:** implement → scorecard → fix → council → fix → CD decision → checkpoint → propagate →
    merge → report. The gate: on each of six scales **the lowest chair's score ≥ 4** on written anchors, taste at 0 F and
    ≤ 1 P\*, accessibility PASS, performance PASS with evidence — by a council first calibrated on three surfaces the owner
    has already judged.
15. **Owner items:** one copy-and-legal packet (B1), the Moroccan reader (B2), the main merge at the milestone (D1, later),
    an optional commissioned shoot (D2). No design choice is asked.

---

## 1. DECISIONS

Every row below was open in the research and is now closed. The council (design, taste, UX, motion, accessibility,
performance, with the Creative Director's final word) decided on the measured evidence. Where a decision carries a
reservation, the reservation is written next to it, with its pre-registered trigger. **Every trigger is mechanical:** a
measured condition, verified by a chair who built none of the surface and wrote none of the decision; or **the owner's
verdict on a shown result** — if he dislikes it, it is corrected or reverted (V54 l.30; §2.2). The CD executes the
remedy and records the firing in DL54; the CD never adjudicates a trigger on its own decision.

### 1.1 The type system — the Typography Director's call, ratified by the council

**Compared:**
- A «Fournier e la console»: Source Serif 4 + Host Grotesk.
- A-bis: Newsreader Display + Host Grotesk.
- **B «Una voce»: Host Grotesk only.**
- C «Vignelli»: Bodoni Moda + Hanken Grotesk.
- D «La firma»: Newsreader Display + Public Sans.

All five ran against the V4 control on the gate-0 comps (TR: 79 loads, 0 CSP). A and B were then judged again on the built
H-E by the 4 October chairs.

**Chose B «Una voce» as the build default.** It is «A minus the serif», two tokens from A (TR §7 item 3), and the test that
could overturn it is scheduled, not conditional (below).

**Because:**
1. **The two chairs that judged type on the V5.3 direction agree — on the hero's promise.**
   - Design: «the serif tips the page toward the editorial register the owner refused» (Hd §10 item 1).
   - Taste: «TYPE A reads editorial at once — the grotesque default is the right reading of the order» (Ht §0 item 6).
   - V5.3 §2 asks for a premium *digital* institution and refuses «serif-heavy editorial composition» — not a serif as
     such; V5.1 §69 still asks «Does the typography have character?».
2. **One voice.** With a grotesque promise, a serif on interior titles is a second voice that has to earn its place.
   Whether it does is the question TS §24 row 3 defers to «the first full page built on the light wall, not before». That
   page is the composed home of W2-E, and the test runs there.
3. **Digital and international are B's best scores** (5 and 4.5); its Arabic is one family, the most coherent of the four
   (TR §3.B, §6). Bytes are **not** a reason: V5.1 §83, «Do not sacrifice typography prematurely»; B and A-bis sit within
   the same font budget.
4. **The platform loses nothing.** It is pixel-identical in A and B (TR §3.B, verified on dashboard, documents and case
   file).

**What TR measured against B, in full.** Premium 3 and institutional 3.5 on the gate-0 comps, which predate V5.3. The
generic-AI row passes «with a warning: a medium grotesque, tight, on a dark hero is the typographic half of "AI SaaS
landing page"» (TR §6). At 64 px «Host Grotesk is a text face with no display cut — its spacing has to be forced» (TR §3.B).
TR §7 item 1 recommended A's architecture. B is therefore a default under test:
- **How premium is held meanwhile:** the composition, the door stage, the light and the craft; weight 500 for the one
  display line, tracking by size, and the forced spacing at 64 px checked on stills.
- **The A-bis test — unconditional, at W2-E** (RTD-M2). On the composed home, the Typography Director builds A-bis in the
  lane: the wordmark's Newsreader in its display cut (21.6 KB) on the promise and the chapter titles, nothing else changed.
  Design and taste rank B and A-bis **blind** at 1440 and 390, fr and ar, and score premium on each. **A-bis becomes the
  system** (two tokens; W3-F inherits it) when both chairs rank it first, or when B scores below 4 on premium and A-bis
  does not. Otherwise B stays. The result is reported either way.
- **Triggers after W2-E** — each re-runs the blind test on the page concerned, under the same rule: any premium score
  below 4 on the home or a door page, whatever its attribution; the owner's verdict on a shown page (V54 l.30).
- **Rules retired while B is the system:** TY-2 (the serif's scope), TY-3 (the display as a serif sentence), CDV law 2's
  serif clause and HET §0 item 9 («one serif line (the promise)») are marked «retired under B» in DL54, so that no reviewer
  applies a rule the system contradicts. They return, with A-bis's scope, if the test switches.

**The system** (wired by W1-A):

*Faces*
- **Host Grotesk** variable 400–700, roman, preloaded.
- **Host Grotesk italic** 400, loaded on use, for titles of acts cited in sources only; never on the portico.
- **«ILE Wordmark»**: Newsreader 600, 11 code points, 1.7 KB. Every rendering of the name. Not reopened.
- **«ILE Mono»**: the IBM Plex Mono 400 subset, renamed because «Plex» is a Reserved Font Name (TR §6 licence note). For
  references, hashes and rule versions.
- **Vazirmatn** variable 400–700, for every Arabic role.
- Markazi Text and Source Serif 4 are not carried.

*Public scale* (TR §3.B, C6)
- **Eight sizes:** 64 · 36 · 28 · 20 · 17 · 15 · 13 · 12.
- Display: `clamp` 40 → 64, weight 500, tracking −0.026 em at 64.
- Titles: weight 600, with tracking that stops at 20 px. Reading text: 400.
- Line-heights on the 4 px rhythm (RH-1).

*Console scale*
- The foundation's `--u-*` roles; the eyebrow and the count rise from 11 to 12 px (C5).
- **One step up below 48 rem or under a coarse pointer:** body 16, label 15, meta 14, caption 13, eyebrow 12. This is TR
  F2's «A+»: text under 14 px falls from 63–67 % to 29–33 %, with no overflow.

*Rules*
- Weight 500 for what acts (controls, links, tabs, labels of values); 400 for values and running text; 600 for titles
  (C4).
- Measures in rem: 36 rem at 17 px, 29 rem at 15 px (C1 — a `ch` measure gave 80 characters a line).
- Typed text in every field is 16 px, at every width (LG-1, TY-14, RS S26).
- Never under 12 px in Latin, never under 14 px in Arabic (DL A7, A25).
- Arabic in Vazirmatn: titles 600 with no ×1.15 (it «sits full on the em»), line-height 1.35–1.4; body 1.75; console
  1.7.

*Loading*
- **Preloads:**
  - Latin pages: Host roman + the wordmark.
  - Arabic pages: Vazirmatn + Host (for Latin runs) + the wordmark.
  - Evidence: preloading the first screen's faces cut the French home's first-render task from 350 to 221 ms (PFR §0).
- **Fallbacks:**
  - Metric-matched for Windows (exists) and Android (TR C2's computed values).
  - Apple's are computed before the integration milestone (§7).
  - Swap CLS ≤ 0.01 with matched fallbacks.

*French spacing — never inside locked copy* (RTE-M10)
- Host has no U+202F, so French uses U+00A0.
- The French-typography treatment is an **opt-in filter on team-authored strings only**. Locked strings — `{% locked %}`
  output and every `data-locked` element — never pass through it: a no-break space changes the characters of a prescribed
  text, and `test_locked_texts.py:30–37` matches them exactly.
- Drawing locked French with no-break spaces is B1 item 8 (owner and counsel). Only after it is signed do the tests and
  `scripts/verify_locked_against_source.py` learn to normalise U+00A0.

**Owner?** No. V54 l.7 «which font among candidates»; l.16. The Moroccan reader's review of Vazirmatn is owner item B2,
and the build does not wait for it.

### 1.2 Colour amendments and the status register (incl. «En examen»)

**Compared** three answers for «En examen» (PC §0, §7.1; DL A13):
- the gate-0 wisteria (h 302);
- the register's lapis (h 262), with the information notice moved to slate;
- a muted wisteria.

**Chose the lapis**, with C2–C5, C7 and C9 applied, C6 kept as a rule, and C8 adopted.
- C8 means «argento» `#d9dee6` for `--aud-istituzione`.
- If the hero-final council records a different audience set measured in context, the hero's set becomes the token set.
- **C8's caveat, checked** (RTD-m4): PC C8 warns that «argento» «is a neutral, not a hue … reads as plain light text»,
  0.047 from the BLOQUÉ night mark. W1-A's colour board sets the four audience accents side by side on night; design and
  taste must read Istituzione as a hue there, or W1-A takes the nearest hue that passes both that reading and the
  separation check. The hero's set still wins.

**Because:**
- The wisteria body `#f2eaff` is ΔE 0.005 from Tailwind `purple-100`. That is V5.1 §48's «generic AI purple». It is also
  the one taste reservation (CL-2) that reaches every console page (TS §24 row 9).
- The lapis mark separates better: closest pair 0.087 against 0.054.
- The palette loses a hue family (7 → 6) and seven primitives (102 → 95), with no byte, request or script added (PC §8).
- C8 widens the closest audience pair, Impresa / Istituzione, from 0.047 to 0.131 (PC §8 C8).

**The eight registers:**

| Register | Material | Edge and mark |
|---|---|---|
| conforme | ink | plain filled disc, no glyph |
| esame | lapis | `--p-registro-500` `#5278c1` |
| neutro | slate | — |
| attesa | amber | dashed edge at step 600, 3.13–3.96 : 1 |
| azione | terracotta | — |
| rifiuto | garnet | struck |
| blocco | graphite | `lock` |
| nullo | ash | dotted edge at step 600 |

**The other colour amendments:**
- The hatch at α 0.78 (3.04 : 1).
- Night marks re-solved by C5: 8 of 28 weak pairs → 0.
- The pinned bars' glass 0.85 → 0.94 by C7: «Italy» over the night hero rises from 3.79 to 4.61 : 1.
- The information notice on the slate wash (C2).
- Literal colours become named tokens (C9).

**Deadlines:**
- «Soon» = attesa (amber); «overdue» = azione (terracotta). Red never means lateness (PC §3.5).
- This fixes the off-by-one register on `/portal/deadlines/`, where «En retard» is styled as a refusal today (platform
  map F13).
- A deadline is never drawn without its glyph (PC D-doc-3).

**Standing rulings, applied:**
- **O14:** VALIDE in ink; no check mark anywhere, the chosen filter chip included (IC §10 row 6). The lint is completed so
  it also catches JavaScript cases (today 0 of 2, DL A5).
- **O57:** no tricolour filet; red and green appear in the mark only.
- **O19:** Persona on sand, confirmed (PC-5).
- **Brand colours:** declared once, in `v2/tokens.css`. The proof's «PROOF ADDITION 0» is not carried, because
  `test_v4_tokens.py:265` forbids it.

**Owner?** No.
- PC §7.1 suggested that the author of «no colour ever means approved» confirm that a blue «En examen» cannot read as
  favourable.
- The council judges that it cannot. Blue is the conventional in-progress register, and approval has no colour at all:
  VALIDE is ink.
- The change is one reversible token. It is shown in the first platform report, not asked.

### 1.3 The corner scale

**Compared:**
- the adopted six: 4 · 6 · 10 · 14 · 20 · full;
- **«Lo spigolo»: 2 · 4 · 6 · 8 · 12 · full;**
- square corners, refused as «the State's clothes» — «Le DSFR est réservé aux services de l'État» (BX §0.7).

**Chose «Lo spigolo»**, one scale for public pages and the console, **with at most three values on any screen.**

**Because:**
- Institutional, public-service and luxury references sit between 0 and 6 px, with one or two values. The sites with
  several values above 10 px are the ones that read as templates (BX §4.2, P2).
- H-E was built at 4 / 10, and its taste brief allows nothing above 10 px but the arch.
- Taste rules «the sharper scale … never two scales» (TS §24 row 1, RA-4).

**The check the wisteria got, run on the corners** (RTD-M8, m12). «Lo spigolo»'s values coincide with Tailwind's default
radius ladder (sm · base · md · lg · xl · full), the substrate of shadcn. A series on a 2 px step has no other natural
values, so the identity cannot live in the values: it lives in how few appear and in what carries the screen.
- **At most three distinct radii on any screen at rest** — `full` included; the arch and the 0 px photographic bands
  excluded; an open overlay may add its own one. The references use «one or two values» (BX §4.2): «two corners, two
  durations, one curve» (BX §3.4). Counted by script on every capture.
- **The silhouette check:** TS §19.2 symptom 10 («1 px muted border + `rounded-md` + grey-500 caption») is judged by eye on
  stills of every console screen type, with the swap test (§3.1).

**Roles** (the token names stay, the values change):

| Token | Value | Role |
|---|---|---|
| `--radius-xs` | 2 | inner corners, nested insets |
| `--radius-sm` | 4 | buttons, fields, tooltip, skeleton, checkbox, the hero's plates |
| `--radius-md` | 6 | the targa, menu rows, the segmented track |
| `--radius-lg` | 8 | cards, panels, photographs on paper, popovers |
| `--radius-xl` | 12 | dialogs, drawers, sheets |
| `--radius-full` | 999 | chips, counts, indicators — never a button or a card |

**Rules:**
- Nested corners are concentric (RA-3): the segmented thumb is 4 inside a 6 track, with 2 px between them.
- Photographic bands at 21 : 9 have no radius.
- The arch is the only large curve. Every focus ring follows its element's radius.
- Where a screen would show a fourth value, the family folds the nearest role into one already on the screen, inside its
  own files (usually 6 → 4), and its scorecard records the count.

**Acceptance.** The W1-A council captures TS's three screens — a first screen, «Mes pièces» and the login — in both scales,
counts the radii on each, and records the comparison. It is an internal check, not an option shown to the owner.

**Owner?** No. V54 l.7 «radius».

### 1.4 Spacing and shadow rules

**Chose:** TS §5, §6 and §11 become binding rules (they were proposals). They are the measured rules the taste lane wrote
from the references and the probes (0 glow found on 62 loads). They are also exactly what holds the platform at 3 / 5:
look-alike panels, and six shadow values on one screen (platform map F5, F11).

**Spacing:**
- **SP-1 One scale.** Every gap between neighbours is a step of the 4 px scale. The console is at 77–83 % today at 1440;
  the target is ≥ 98 %, after the listed optical exceptions.
- **SP-2 Near things are near.** The gap between two groups is at least 2.5 × the gap inside a group. H-E measured 1.2.
- **SP-3 A label belongs to its control.** Label above at 14 / 20 weight 500, 8 px from the control; 20–24 px between two
  fields.
- **SP-4 One padding per component:**
  - panel 24 (16 when dense);
  - button 16 / 20 / 24 inline, for heights 36 / 44 / 52;
  - register row ≥ 64; table row 48.
- **SP-5 Sections.** Public chapters 96 / 64 / 48 (desktop / tablet / phone). Console page padding 32 / 16; panel gap 24.
- **SP-6 No remainder.** No unplanned interval above 64 px inside a composed screen.
- **SP-7 A phone is recomposed, not shrunk.** Chapters 48, cards 16 apart, padding 16; reading sizes go up one step.
- **SP-8 Targets.** 24 px is the floor of every target. 44 px for primary actions, form controls, the rail, the bars,
  drawer rows and every target under a coarse pointer.

**Rhythm (RH-1 … RH-8):**
- Line-heights on the 4 px line.
- One section device, at the reading edge.
- A picture or a drawn figure at least every second screen of the home and the door pages.
- A short home: 3–8 screens at 1440.
- One thing once. The page as a chain of questions. Dense, then quiet.

**Shadows:**
- **SH-1 Five levels, each with a meaning:** 0 canvas · 1 sheet · 2 raised · 3 popover / menu / panel · 4 modal / drawer
  with a scrim.
- **SH-2 Hairlines before boxes.** A row never carries a shadow; navigation never carries one either.
- **SH-3 The night's own colour.** Shadows are `rgba(7, 18, 38, α)`: never black, never coloured, never luminous. The glow
  is retired.
- **SH-4 A shadow never animates.** A hover's change of plane is a pre-painted layer whose opacity changes.
- **SH-5 Glass has one seat.** Only the two sticky bars, once scrolled: blur 12 px, static, α 0.94.
- **SH-8 A shadow budget:**
  - a hero: at most four distinct shadow values;
  - a viewport at rest: at most one shadow of level 3 or more;
  - a console screen: one raised panel (the NowPanel) and at most two shadow values. The dashboard and the case file
    carry six today.
- **SH-9 Primaries are flat:** no inner light, no glow, no arris on a primary — the login's included (§1.13). The one
  material signature is §1.10.
- **The lit arris has one seat: night plates** (the hero's plates, the targa on night, the login stage's plate), where
  the light has a cause. Paper surfaces — fields, overlays, panels, cards — carry a hairline only; TS §19.2 symptom 4
  lists «a lit edge» among the glow look-fors (RTD-M8).

**Owner?** No.

### 1.5 Motion tokens and grammar

**Compared:**
- the eleven open motion rulings MS-O1 … O8, R4, R7 and R10, and K17 (DL A18; MS §19);
- the three exit curves, measured (MS §5.3);
- the five tiers (MS §2).

**Chose the motion lane's ruling set, whole, with the reasons written in MS** — and one named exception, the entrance
release (§1.9). Every interaction measured below 105 ms at CPU ×4 under the CSP (DL A18).

**Tokens:**
- No duration added or changed (MS §4.2): fast 120 · standard 200 · emphasized 320 · slow 480 (public lines only) ·
  draw 900 · route-light 1200 · route-stagger 400 · stagger 60 · key 1200 · door 1600 · luce 2200 · wait 400 (a threshold,
  not a duration).
- Springs `--spring-snappy`, `--spring-soft` and `--spring-sheet` as `linear()` twins (470 / 430 / 550 ms).
- **Added:**
  - `--motion-reduced: 80ms` (MS-O4);
  - `--ease-turn` = `cubic-bezier(0.77, 0, 0.175, 1)`, the one key-turn curve of the loader, the login and the hero. It
    replaces `--ease-turn-in` / `--ease-turn-out`. LS §9 named it `--sig-turn`; it takes the `--ease-*` name the
    hero-final build already uses (HF §9.1) — DL54.

**Curves:**
- **Enter:** `--ease-enter` (0.25, 1, 0.5, 1), for every arrival and for the way *into* a hover (MS-O1, finding MS1).
- **Exit (MS-O2):**
  - a small surface leaves on `--ease-enter` at 120 ms;
  - a long travel leaves on `--ease-layout` at 200 ms;
  - `--ease-exit` keeps one role only: an object that crosses the view.
- **Move:** `--ease-layout`, or a spring twin when the distance varies.
- **Light:** `--ease-sine`.
- No overshoot anywhere.

**Tiers:**

| Tier | What | Clock |
|---|---|---|
| 0 | static: every keyboard-initiated change (T-7, R-07) | 0 ms |
| 1 | micro feedback; the press goes down at 0 ms and is released on `--spring-snappy` | ≤ 120 ms |
| 2 | state transition | ≤ 320 in, ≤ 200 out, a sequence ≤ 600 |
| 3 | signature: L1, the filed mark, the journey light | L1 once per sign-in; the mark 240 ms; the light 120 ms a segment |
| 4 | one immersive public moment per page | ≤ 5 s (WCAG 2.2.2) |

Density at any moment (T-3): one control's feedback + one tier-2 surface + one tier-3 *or* tier-4 sequence.

**Rulings:**
- **MS-O3:** nothing travels across a page load. Inside a page there is one indicator: `--ease-layout` in the console,
  `--spring-snappy` on public pages.
- **MS-O4:** under reduced motion, overlays use one 80 ms opacity and nothing else.
- **MS-O5:** tooltips share one 400 ms wait; neighbours then show at once; the group cools after 400 ms.
- **MS-O6:** anchored surfaces drop 4 px. Only a modal scales, and only from 0.96.
- **MS-O7:** a hover that moves anything sits behind `(hover: hover) and (pointer: fine)`.
- **MS-O8:** the busy key turns once, then holds.
- **R4:** the door cards' pointer light is removed. It drew 0 px of difference for 0.53 s of style work.
- **R7:** the phone action bar does not travel.
- **R10:** the rail collapse ships instant, unless `contain: layout` brings it to 60 fps at CPU ×4.
- **K17:** text never waits for a reveal.

**Laws:**
- **Nothing loops** (CDV §17).
- **Properties:**
  - only `transform` and `opacity` animate;
  - `clip-path` is allowed for a one-shot;
  - `stroke-dashoffset` only for the 240 ms filed mark.
- **Never animated:** `filter`, `backdrop-filter`, `box-shadow` (MO-14, SH-4).
- **`will-change`** is set for the run only and removed on `animationend`.
- **Phase-aligned keyframes** for every multi-beat sequence. They cut the loader from 120–200 ms to 54–62 ms of main thread
  (LS §5.2).
- **Every tier has its still,** designed first. The still is also the reduced-motion state and the no-JS state (T-6).
- **The console has no entrance and no stagger at load** (MS §3.2) — with one named exception, the entrance release: once
  per sign-in, on the first console page, on the rail's mark, never over painted content (§1.9). L3's seat applies to
  asynchronously fetched fragments only, never to a server-rendered region (RTD-m2).

**Reduced motion, built as a state** (RTE-M2):
- V1 `components.css:3071–3091`'s universal `0.01ms !important` block is deleted in W1-D. The V5 rule replaces it: the
  duration tokens are zeroed in the `prefers-reduced-motion` block, and `--motion-reduced` applies to `opacity` only
  (MS-O4, RM-1). `test_design_docs.py:815–845` (its motion half), A11Y §7 and `test_v4_tokens.py:231` are retargeted in
  the same merge.
- **One gate for script motion:** `motion.js`'s `reducedMotion()` reads the media query and the preview's `html.rm` flag;
  every WAAPI and `requestAnimationFrame` sequence (the loader, the route lights, the hero clock, the architrave, the
  journey light) runs through it. A static test refuses `.animate(` and `requestAnimationFrame` in `static/js/src/`
  outside it.
- **No hang at 0 ms:** state is set at t = 0, and no script waits on `transitionend` / `animationend` without a timeout
  (a 0 s transition never fires its event).
- **The preview flag is not the state** (MS7): `html.rm` is generated from the media block's token list,
  `test_rm_flag_parity.py` ships with W1-D, and council evidence for reduced motion uses Playwright
  `emulateMedia({reducedMotion: "reduce"})`, never the flag alone.

**Engine:**
- CSS transitions + `@starting-style`, and WAAPI for measured sequences.
- No new use of the `motion` library. Its existing uses go family by family, and the dependency leaves in W4-B.

**Owner?** No. V54 l.7: easing, hover, micro-interaction. **The feel is judged on evidence an agent can read** (RTD-M10):
the motion chair works from filmstrips (frames every 16.7 ms, at 1× and with the animation clock at 0.25×) and from
frame-difference series — an agent samples frames; it does not watch at speed (Hd §10 item 2). Each flagship report
carries local 1× and 0.25× recordings, so the owner judges the feel on the result; «no person watched the motion at speed»
stays in the honest limits (§6) until he has.

### 1.6 Focus

**Compared:**
- a ring and a halo everywhere: soft, and it reads «SaaS» on links and chrome;
- a ring only (the foundation's comment);
- **a ring everywhere, plus the halo on text fields only.**

**Chose the third — one focus system:**
- `:focus-visible` only.
- **The ring:** a 2 px `--focus-ring` (laguna-550) outline at a 2 px offset, following the element's radius.
  - On night: `--focus-ring-night` (laguna-400).
  - On photographs: the two-tone ring (carta-0 inside, notte-900 outside).
- **On text fields:**
  - the 5 px `--focus-halo` (α 0.3) is added;
  - on a pointer focus, a 2 px laguna rule draws from the reading edge in 200 ms;
  - from the keyboard and under reduced motion, the rule is there at once.
- **Forced colours:** `Highlight`.
- **Never animated:** tier 0.
- **Never hidden under a sticky bar** (WCAG 2.4.11): the existing `scroll-padding-block-start` (V1 `base.css`, pinned
  by `test_design_docs.py:827`) is kept and measured under the V5 bars by W2-C1. `focus-clear.js` is written only if
  that measurement fails, and W2-C1 then owns it (RTE-m4).
- **Contrast:** the ring holds ≥ 3 : 1 against both neighbouring colours on every ground. C1 checks it on the lapis body:
  3.55 and 3.23 : 1.

**Because:** the halo marks the active field exactly where the ring sits on the field's edge; anywhere else it adds
softness and no information.

**Tests:** the focus half of `test_design_docs.py:815–845` (a navy `box-shadow` ring) is retargeted to this system by
W1-A.

**Owner?** No.

### 1.7 The icon system and icon sizing

**Compared:**
- the product's 36-symbol sprite and its multi-meaning glyphs;
- the gate-0 sprite (113 symbols);
- the icon review's amendments (IC §10).

**Chose the ICON_SEMANTIC_MAP system,** built by W1-B.

*One concept, one glyph*
- One concept → one glyph, and one glyph → one concept.
- Enforced through `apps/core/icons.py`, which holds the registry, `MIN_SIZE` and `TWINS`.
- Today 19 of 32 live symbols carry two or more concepts, and `arrow` is 80 of 163 calls (IC §0).

*Three tiers*
- **Identity:** `ile-arch` (floor 16), `ile-key`, `ile-steps`, `ile-mark` (floor 20). Never toned, never mirrored.
- **Concept:** carries the 12 % tone; reaches templates only through the registry.
- **Utility:** monoline, never toned.

*Status — «i cerchi»*
- Outline = open; filled = settled. The chip mark is 16 px.
- `check` / `circle-check` only for the person's own act. Never in a chip, a node, a station or the ledger.

*Sizes and stroke*

| Size | xs | sm | md | lg | xl | hero |
|---|---|---|---|---|---|---|
| px | 14 | 16 | 20 | 24 | 32 | 48 |
| stroke-width (24-unit grid) | 2.57 | 2.25 | 1.8 | 1.5 | 1.25 | 1 |
| effective stroke | 1.5 | 1.5 | 1.5 | 1.5 | 1.67 | 2 |

Square caps, miter joins, `currentColor` only.

*Audiences*
- Persona `person` ≠ Impresa `building` ≠ Istituzione `institution` ≠ Università `university`.
- Never below 20 px. The closest pair, `building` / `institution`, is 0.61 alike at 16 px (IC §3.1). In chrome discs the
  glyph is drawn at 24 px, because `building`'s floor is 24.

*Rules*
- The six-icon ceiling applies to the editorial body of public pages; the chrome is exempt.
- A glyph column is all or nothing (DE-7).
- A row carries a glyph only when it says something.

*Settled questions*

| # | Decision | Reason |
|---|---|---|
| Q7 | threshold B keeps the gate-0 nested arch, floor 16 | the review's recommendation |
| Q8 | `ile-steps` does **not** mirror in Arabic | it is an identity glyph drawn from the mark, and it must climb the same way as the stage's steps beside it, which never mirror (HE §0 item 10); the Moroccan reader may still comment (B2) |
| Q9 | share `university`; no `backpack` | `backpack` sits next to the forbidden luggage vocabulary |
| Q10 | `shield`; no `fingerprint` | no biometric sign |
| Q11 | one live area: re-proportion the 22 pictorial V4 drawings; redraw `building`, `document`, `info`, `warning` | — |
| Q12 | `award` for «Diplômes et titres» | — |
| Q13 | the status candidates as drawn, judged on the chip board at 1× and 2× | — |
| Q5 | Lucide ISC / MIT donor geometry, with the notice in `ICON_LICENSES.md` | 65 original drawings are not needed |
| Q3 | `concierge-bell` for the Guichet | 0.34 alike from `bell`; floor 20 |

*Amendments*
- `badge-dot` enters; `rotate-ccw` and `network` leave (IC §10).
- Result: 111 symbols, ≈ 6 KB gzip.

*RTL*
- The closed flip list: arrow, arrow-start, chevron-end, logout, send, signpost, milestone, panel-left-close.
  `test_page_integrity.py:59` (`_FORWARD_ICONS`) is retargeted to it.

*One ILE hand, shown before the merge* (RTD-M8)
- The donor geometry is Lucide's (Q5), the shadcn icon set. Before W1-B merges, a sheet sets the ILE sprite beside the
  raw Lucide originals at 1× and 2×; design and taste must read one ILE hand there (square caps, miter joins, the stroke
  table, the re-proportioned pictorial set). A glyph that still reads as Lucide is redrawn.

**Owner?** No. V54 l.24.

### 1.8 Control heights

**Chose:**

| Control | Height |
|---|---|
| `--control-sm` | 36 — fine pointer only: dense console toolbars, the segmented track |
| `--control-md` | 44 — the default; every control under a coarse pointer |
| `--control-lg` | 52 — public primaries, public form fields, the hero's CTA, the login's CTA and fields |
| `--control-icon` | 40 on a fine pointer, 44 on a coarse one |
| hit area | floor 24 on a fine pointer; 44 under a coarse pointer and for every primary |
| chips | 20 / 24 / 28; a 44 px hit area under a coarse pointer, made by padding |
| rail rows | 44; 40 under 760 px of height on a fine pointer (UPl S-1) |
| rows | register row ≥ 64 · table row 48 · drawer and sheet rows 64 |

**Compared:** a 56 px login CTA (`surfaces.md` §2.3) against the 52 px step of the scale.

**Chose 52.**
- The hero's signature CTA is 343 × 52 (Hd §6.6). The two entrances to the reserved area then share one height.
- 56 would be a ninth control value for a single button.
- The login's CTA gets its strength from the key, the full width and the weight — kept flat (SH-9) — not from 4 px.

**Owner?** No.

### 1.9 The loader — «Lume», one state machine for three tiers

**Compared** three candidates on one state machine (LS §0, §3, §8), with the gate-0 cycle as the control:
- A «Mandata»: the door answers.
- **B «Lume»: the light answers.**
- C «Passo»: the path answers.

**Chose a fusion, named «Lume»:**

| Tier | What | Where |
|---|---|---|
| L1 | **one gesture across the sign-in.** *Engage*, on the login's submit: the stage's key turns once (0 → 360°) and holds — no light. *Release*, on the first console page after a successful sign-in: «Lume»'s doorway fills with light from the key's eye, on the rail's mark, and the key reads in ink | the sign-in only; the release once per session |
| L2 | the 18 px key turns once in 260 ms on `--ease-turn`, then holds; it goes from dim to lit at the answer | every busy control |
| L3 | «Mandata»'s seat: rows rise 4 px in 200 ms, 40 ms apart, with no light | asynchronously fetched fragments only — the preview drawer, notifications, search, «Aller à…»; never a server-rendered region; a refresh swaps in place |

**Because:**
1. **The owner's invariant names an opening and a light.** V54 l.19: «door + key + rotation/opening + light». Only «Lume»
   shows both so they read. «Mandata»'s frame light barely reads at 2× at 900 ms; «Passo» shows a passage, not an
   opening (`surfaces.md` §3.1).
2. **The light says «it is open» only when it is** (RTD-M6). LS §8 item 4: «a room that fills with light says "it is
   open": the right picture at sign-in, the wrong one anywhere near a legal answer». So the lit doorway plays only after a
   successful sign-in, on the page the person has entered. A refused sign-in loads the error page at rest; the login itself
   shows only the key's turn — the neutral gesture CDV §18 allowed «not gated». Nothing of L1 plays on the
   `OUTCOME_BEARING` list (recalculate-situation, pre-assessment, eligibility, scan-verification), which keeps L2 + L3.
3. **The mark moves once, at the entrance — across the page load.** BA §1: the mark «se si muove, si muove una volta,
   all'ingresso»; CDV M10 / O1 require §1 amended in writing for any other context. Engage and release are one movement,
   split by the navigation and played once per sign-in. The amendment — «once, at the entrance, across the page load» —
   is recorded in DL54, citing V54 l.19, and W1-D adds a one-line pointer to it in BA §1. It is the only other context.
4. **M10's reasons hold absolutely.** The tricolour planes, the door and the steps never move; nothing cracks open. The
   mark is `direction: ltr`; the key turns 0 → 360° about its shaft and holds on the verbatim mark. Between 90° and 270°
   the bit shows on the other side: that is the turning the owner asked for (V54 l.9, l.19), and «the tricolour mark never
   mirrors» is read as «never held, drawn or served mirrored» — recorded in DL54 and said in the loader and hero reports
   (RTD-m7). Only M10's *letter* («frame light only») yields, to the owner's later invariant.
5. **The quietest grammar wins at the frequent tiers.** LS §6, verdict 2: «Mandata»'s L3 is «the right default».
6. **The three cost the same:** 54–62 ms of main thread per L1 run, 10–11 frames, no long task, compositor only.

**Build rules:**
- One state machine: rest → engaged → open → rest. **Nothing loops.** A long wait is a still picture, with words at 1 s
  and at 10 s (the 10 s state offers «Réessayer»). `MIN_SHOWN` 480 ms; the loader is a singleton.
- **The engage on the login:** on submit, the stage's key turns once in 480 ms and holds while the CTA's L2 key turns.
  Never gated on the answer; never delaying the navigation.
- **The release:** a `user_logged_in` receiver in `apps/accounts/signals.py` sets a session flag (allauth's sign-in and
  the preview's persona switch both send the signal). The first console page consumes it and plays the release on the
  rail's mark (below 64 rem, the top bar's mark), once, never over painted content. Under reduced motion the mark shows
  the release's end state, without travel.
- **The release's seat was never shot below 120 px** (LS §8: L1 was drawn at 160 px). W1-D measures it at the rail mark's
  served size; the fallback below decides.
- **Before any measurement:** the muddy grey-beige at +40–80 ms is fixed (a warmer first stop, or a 120 ms opacity
  ramp); `will-change` is dropped on `animationend`.
- **Generated light sheet:** `scripts/gen_loader_light.py` writes `static/css/v5/_loader-light.css`, imported by the
  console entry only (§2.3); the output is committed with a currency test.
- **One shared key-turn primitive** (the `.sig__l` layers, `--ease-turn`, rotateY about the shaft): the loader, the login
  and the hero's rotating key.
- **Tests** (`test_loader_rules.py`): nothing `infinite`; a phase's animations share one duration; L1 markup appears only
  in its allow-listed templates and never on an `OUTCOME_BEARING` form (RTE-m6); L3 attaches only to fragment containers,
  never to a server-rendered region (RTD-m2).

**Acceptance:**
- The ten re-measurements of `surfaces.md` §3.3, run on the product's sources under the lock (every earlier capture
  predates the final `sig.js`, RRT M1). Item 8 becomes: on the login, submit → the engage → the next page's first paint
  against the reduced-motion baseline (±1 frame); on the console, the release on the rail mark.
- The three measured conditions below, on filmstrips at 1× and 0.25×.

**Fallback — on measured conditions, not on «feel»** (RTD-M10). «Mandata»'s release (a frame light) replaces «Lume»'s at
the rail seat if any of these holds, read by the motion chair and verified by a fresh chair:
1. **Visibility:** at the seat's served size, less than half of the doorway's area changes by ΔE00 > 6, or the change
   holds for less than 600 ms, at 1×.
2. **The muddy tone:** between +40 and +120 ms the doorway's mean chroma dips more than 5 C\* units below the lower of its
   two end colours (LS §5's grey-beige, row B).
3. **The glow watch-point:** any pixel outside the doorway's shape changes by ΔE00 > 2 during the release, or the release
   plays more than once (LS §6: the light «must stay inside the door and play once»).

If «Mandata»'s frame light also fails condition 1 at that seat, the arriving page carries no release, L1 is the engage
alone, and the report says so in words. The owner's verdict on the shown loader is a trigger too (V54 l.30).

**Owner?** No. V54 l.19 is explicit.

### 1.10 The signature CTA

**Compared:**
- T0 «Bordo d'oro»: a static gilt hairline.
- T2: a first-party WebGL ring.
- H-C's conic rim.
- CTA-A «Intarsio d'oro»: Liquid-Metal class, a still gilt inlay, CSS.
- **CTA-B «Soglia»:** the door's line; a laguna leaf that opens toward the door; CSS.

**Chose CTA-B «Soglia»,** on the hero's primary only, once per page. Nothing else on the site carries a material
treatment.

**Because:**
- **It meets all six conditions of V5.3 §7:** institutional; not crypto or gaming; does not steal from the door; contrast
  intact (label 7.52 : 1); works on phones; light (715 B gzip, 0 B of script). Sources: HS §15, HE §2.9.
- **Both chairs chose it as the default:** design (Hd §6.6) and taste (Ht §0 item 9, §14). Motion scored B 4 and A 2,
  before M-3 was fixed.
- **CTA-A** puts gold three times at rest in the first screen and is the first gold a phone shows; «by eye [it] steals from
  the door there» (Hd §6.6). It is also the catalogue's liquid-metal recipe, adapted (taste reservation P* 9).
- **T2** costs 3.4 KB of script, for desktops only. **T0** breaks onto two lines at 360 px.

**Refinement:**
- The inset hairline becomes the night plate's own stone hairline instead of cyan. Taste called the cyan line «the one
  object on the wall that smells of a console» (Ht §14).
- The leaf opens under a fine pointer only. On touch, the pressed state (one step darker, 1 px down) is the whole answer.
- The hero-final council's decision binds for the hero's execution details. Where it differs from this paragraph, the CD
  reconciles the two in DECISION_LOG before the port.

**Where it never appears:**
- the header, and the targa;
- the login submit, a flat PR01 primary that holds the key (§1.13);
- cancel, delete, pagination and table rows.

**Owner?** No. V54 l.7 «which 21st component»; l.13.

### 1.11 The reserved-area entrance — «la targa»

**Compared:**
- (a) the letterhead's end zone, in both states;
- (b) the compact state only, with the seat reserved from the first paint;
- (c) the utility bar (today, and in the Fase 3 comp).

**Chose (a).**

**Because:**
- The utility bar is not sticky, so today the entrance leaves at the first scroll (NV-1).
- 19 of 22 captured homes keep their primary action in the compact bar, and both owner references do (DL A11; TS LA-5).

**The component:**
- **Plate:** an ink hairline, radius 6, the gold `ile-key` as an ornament, the words in ink. On night: a `--line-night`
  hairline, the words in paper.
- **Hover** tints the plate (fine pointer only). The key does not move (O1).
- **Label:** shown wherever the four languages fit. Below the measured threshold, the key alone, with a name tooltip.
- **Signed in:** the same seat opens the account popover, built on the overlay system; it replaces the `<details>`.
  It is wired by W2-C2, after W2-A has merged (§3.4).
- **Flags:** rendered only behind the existing `reserved_area_public_link` + `reserved_area_enabled`. When they are off,
  no hole is left.
- **Material:** never gilt, never metal.
- **Phone:** the sheet's pinned foot carries the night version at 44 px.

**The language control** stays in the utility bar, as one component:
- `nav[aria-label]`, with autonyms («Italiano · Français · English · العربية» — never «ع», DL A25);
- 24 px targets on a fine pointer, 44 px on a coarse one;
- first in the phone sheet.

**Owner?** No. V54 l.17.

### 1.12 The navbar — «Il portico», Fase 3 developed

**Compared** internally only — no option is shown:
- the owner's Fase 3 comp as it is (`P/home/phase3-menu.html`: the portico panel on a grid 8 | 4 — the gloss and the
  entries first, the photograph at the end, l.44–48 and the notes at l.231);
- N-A «Il sommario» (photograph · index · reading pane) — the anatomy the owner did **not** choose when NV §11 N1 put the
  two to him;
- P-A's chrome conventions;
- against the measured defects NV-1 … NV-7, LA-7, m6, R3A-2 and M3.

**Chose:** keep Fase 3's anatomy **and its order**, fix what the evidence fails, and take N-A's proven *mechanics* only
(intent timing, the keyboard model, the indicator) — never its layout (RTD-M4).
- **The anatomy kept:**
  - the night utility bar;
  - the letterhead with six items: four doors as buttons, a hairline, Forum, Projet;
  - the portico panel on 8 | 4: the door's gloss line, entries on hairline rows, the photograph field at the inline end,
    the anti-fraud foot;
  - the scrim.

**The changes:**
1. **Geometry — NV-5's 440 px fixed without flipping the panel.**
   - The panel hangs from the content width (`.letterhead__inner`), not from the viewport (N1).
   - Inside the 8 columns, the gloss line takes the lock-up's span and the entries column starts at the first door's inline
     start; the photograph keeps the last 4 columns.
   - One panel height for the four doors (± 24 px), with shared column origins (N3, LA-7).
   - **Pointer distance** (RTD-m3): the first door's first entry within 48 px of the door (N2, applied to the first door).
     Doors 2–4 meet a pointer-path budget instead: the open panel holds along the straight path from the door to its
     first entry (a safe triangle — no panel switch while the pointer moves toward the open panel), proved per door by a
     browser test, the travel reported in px.
2. **A panel for every door, from live content only.**
   - Content: the locked gloss; then the CMS children, or the door card's two live task links (Institutions,
     Universités); then «Voir l'espace».
   - «Projet» is a plain panel, without a photograph.
   - No schema change: `MenuItem` has `description_<lang>` and no image field.
3. **Entries.**
   - Titles at 17 / 24, weight 500, on hairline rows.
   - **A second line under an entry wherever a short live sentence exists** — `MenuItem.description_<lang>` when filled,
     otherwise the destination's own live sentence, as the comp already reused live labels (E2) — shown whole, never
     clamped, never written by us. The panel descriptions are **item 1** of the B1 packet; an entry without a live
     sentence shows its title until that item is signed.
   - Per-entry glyphs are not kept: an open panel adds at most two glyphs (DE-2, N14). The door's audience glyph is drawn
     once — at ≥ 20 px on a 36 px night disc, at the photograph's bottom-start corner. The panel reads as the door card,
     opened.
4. **Imagery.**
   - The door's own audience photograph, **in colour, in the V5 grade** (§1.16).
   - A frame never shown elsewhere on the same page (AUM rule 1; V54 l.23).
   - Loading: 4 : 5 srcset 640 / 960, lazy, `fetchpriority=low`; an idle prefetch after `load`, from 80 rem only; never
     on phones, never with Save-Data.
   - The graded average colour holds the field while the photograph arrives.
   - When the door changes, the photographs cross-fade by opacity in 200 ms. The field is isolated with
     `contain: paint`.
5. **Motion.**
   - One indicator, «l'architrave», on the seam between bar and panel: `translateX()` + `scaleX()` on `--spring-snappy`.
     It does not travel on its first placement, from the keyboard, or under reduced motion.
   - The panel is a transition. In: opacity + 8 px from the bar, 200 ms `--ease-enter`. Out: 120 ms. It is instant on a
     keyboard open and on a door change.
   - Content swaps in 120 ms of opacity.
   - On the first pointer open per page only, the entries rise 4 px, 30 ms apart (≤ 150 ms added).
   - Glass only when scrolled, on a fine pointer, with no panel open.
   - No smooth scroll on Tab.
6. **Behaviour.**
   - Hover intent: open after 120 ms, switch after 80 ms, close after a 250 ms grace.
   - A click pins a panel that hover opened.
   - The scrim only for a click, a tap or the keyboard, and never over the utility bar.
   - Keys: ← → ↓ ↑ Home End Esc. Focus leaving the navigation closes the panel.
   - A CSS fallback without JS. Evidence: NV §4.2–§4.10, 56 / 56 behaviour checks.
   - **On the overlay system's primitives** (RTD-m8): the panel's scrim, light dismissal, Esc, focus return and motion
     tokens come from `overlay.js`; it stays a disclosure navigation (`button[aria-expanded]` + region), not a dialog.
     W2-C1 codes against the primitive contract W2-A publishes at its start, behind a local adapter; W2-C2 switches to
     `overlay.js` once W2-A has merged.
7. **1024–1279 px.** The four doors in the bar; the panel opens without its photograph; «Menu» carries Forum · Projet ·
   languages · search.
8. **The phone and tablet sheet,** on the overlay system (§1.14), landed by W2-C2 after W2-A merges.
   - A native `<dialog>` that owns its header line: the lock-up + «Fermer», which takes the first focus.
   - The Fase 3 order. The doors are 64 px rows that unfold in place (an exclusive `<details name>`).
   - The targa and the promoter sit in the pinned foot.
   - Motion: «Quiet» (opacity + 12 px, 320 / 200 ms) at full width on phones; from 48 to 80 rem the side sheet slides in
     from the inline end.
   - The cold open's INP p90 ≤ 200 ms.
9. **Text spacing (WCAG 1.4.12).** The bar wraps, or falls back to the 1024 layout. It never clips (m6).

**What changes from what the owner saw — said, not hidden.**
- **Added:** four panels instead of one; each door's opened photograph; the architrave; the audience disc; the keyboard
  model; whole second lines; the targa in the letterhead.
- **Removed or changed:** the per-entry glyphs (DE-2); the serif gloss, now in Host (§1.1 — it returns if A-bis wins); the
  truncated description.
- **Kept in place:** 8 | 4, the photograph at the end, the gloss first, the anti-fraud foot.
- **«Richer than Fase 3» (N18):** a before / after sheet at 1440 and 1920 — the comp beside the build, the same door open —
  lists every addition and removal above; design and taste must each judge the build richer, more premium, more dynamic
  and more sophisticated (V54 l.17).

**Because:**
- V54 l.17 binds the direction and asks it to be «richer, more premium, more dynamic, more sophisticated».
- The changes answer the comp's measured defects: a truncated disclaimer, the pointer distance, a viewport-inset panel,
  one panel out of four, no keyboard model, an off-screen focus ring.
- «The panel is the door card, opened» makes the hero, the cards and the navigation one system.

**Acceptance:** N1–N17 of `surfaces.md` §1.4, amended — N2 as change 1 above; N10's LCP tolerance in ms (§2.6) and CLS
≤ 0.05; N17 on the six scales of §3.1 — plus **N18** the «richer than Fase 3» sheet and **N19** in Arabic, the architrave
under the active door and menus aligned on the inline end, in `test_rtl_browser` (RTE-m5). Files: W2-C1 and W2-C2 (§3.4).

**Owner?** No. The description lines are copy (B1, item 1).

### 1.13 The login — «Il varco»: «Le vie convergono al varco»

**Compared:**
- the gate-0 comp — the owner's verdict: concept good, left side too static, form too simple (V54 l.18);
- four left-side treatments, internally:
  - a looping ambient field — refused, because nothing loops;
  - a parallax depth stack — refused: motion for show, with a text-raster risk (B4);
  - one longer arrival sentence, then rest — refused: a person spends 10–40 s on the form, and for all of it the stage
    would be as still as the comp the owner judged (RTD-M5; V5.3 §4.E «non voglio animazioni talmente sottili da
    risultare virtualmente assenti», §14; V5.1 §22);
  - **drawn convergence that answers the person — chosen.**

**Chose — the left side** (night stage, 5 / 12):
- **Kept:** the owner's door stage (arch photograph, gold key, three steps), the solid night plate, the 3 % grain, the help
  line, the promoter.
- **Depth, drawn.** Four route hairlines in the audience accents rise from the plate's lower edge and converge into the
  threshold — the door is the vanishing point — with a low warm pool on the steps (≤ 12 %). This is also the no-JS state.
- **The stage answers the person** — tier 1–2, event-driven, compositor-only (the opacity and transform of pre-painted
  light layers), 0 ms when the input comes from the keyboard, nothing looping:
  1. focus on «Courriel»: the four routes light into the threshold (one pass, 600 ms);
  2. a valid address (the field's own validity, on input or blur): the routes hold lit;
  3. focus on the password: the light runs up the door's frame and holds (one pass, 600 ms — a tier-2 sequence, not the
     900 ms arch draw);
  4. submit: the stage's key turns once and holds (L1's engage, §1.9) while the CTA's L2 key turns.
  Clearing the address or leaving the form returns the matching state in 200 ms, without travel. The light layers are
  isolated with `contain: paint`; no text sits on a moving layer (B4).
- **On arrival:** if no field has focus after LCP, one arrival sentence runs once — the home's four route lights travel
  into the threshold (1200 ms each, 400 ms apart) and rest. Any focus or input cuts it to its still and hands over to the
  person's states.
- **Reduced motion:** every state appears at its end, without travel. **Forced colours:** the hairlines in `CanvasText`, no
  light layers.
- **Below 48 rem:** the 120 px band keeps the arch only; focus on either field lights the arch's frame; submit turns the
  key.
- **The error page loads at rest:** no arrival sentence and no travel at load; the stage shows the still that matches the
  kept address (the routes held lit, at 0 ms); later inputs drive the states as usual.
- **Shared primitives:** one route-light primitive with the home; one key-turn primitive with the loader and the hero.

**Chose — the form** (paper, 7 / 12), inside allauth's real templates:
- **Templates.**
  - A project `account/login.html`: the same view, fields, CSRF, redirect, passkey and code blocks.
  - The contract classes are kept (`test_layout.py:179–191`).
- **Hierarchy:**
  - eyebrow: `ile-steps` 14 px + «Espace réservé», 13 / 20, weight 500;
  - H1 «Connexion»: 36 / 44 on desktop, 28 / 36 on phones, Host 600 (the type system);
  - invitation: 17 / 28;
  - the fields, then the CTA;
  - the reassurance at 15 / 24, with its question as a label;
  - the help link, with a 44 px target.
- **Fields — «la lastra»:**
  - 52 px tall; typed text 16 px; the label above at 14 / 20 weight 500, 8 px away; 24 px between fields;
  - a hairline edge, radius 4 — no lit arris on paper (§1.4);
  - hover: the edge changes in 120 ms (fine pointer only);
  - focus as in §1.6;
  - autofill restyled to the field's own surface;
  - the e-mail field `dir="ltr"`, `autocapitalize=none`, `spellcheck=false`.
- **Placeholders** removed, through a `LoginForm` subclass set in `ACCOUNT_FORMS['login']`.
- **The reset link** sits at the end of the label row: a `password_reset_help_text.html` override plus a `form_field.html`
  slot.
- **Micro-interactions:**
  - show / hide: one channel (`aria-pressed` + the existing live label string); the glyph swaps at once; the caret is
    kept;
  - the press goes down in 0 ms and releases on `--spring-snappy`;
  - the busy face rides on a transform, so the label never moves; the L2 key turns once and holds;
  - on an error: the summary takes the focus; both fields point to it with `aria-describedby`; no red edge; the e-mail is
    kept and the password cleared.
- **The CTA:**
  - full width, 52 px, label 16 / 24 weight 500;
  - the L2 key glyph at the inline end — «the button holds the key»: the same key turns when the button is busy;
  - **flat** (SH-9; RTD-m1): the primary's fill, no arris, no inner light, no glow; hover darkens one step, on a fine
    pointer only;
  - not a signature material: the page's one signature belongs to the hero.
- **States:**
  - four unhappy states, composed from live strings only:
    - too many attempts;
    - too many requests — a project `templates/429.html` including `errors/429.html` fixes allauth's English fallback;
    - e-mail not verified;
    - link expired;
  - the Caps Lock hint and a session-ended line wait for copy (B1).
- **Removed:** «Se souvenir de moi». It is not live (`ACCOUNT_SESSION_REMEMBER = False`), and adding it would be product
  policy. Not pursued.
- **Order:**
  - the skip link targets the form's heading (m9);
  - `lang` on the Latin runs of the Arabic page (R3A-3);
  - the way back near the top on phones (LG-6);
  - below 44 rem of height, a 72 px band, so the submit stays in the first viewport at 360 × 640 (LG-5).

**Because:**
- V54 l.18 asks exactly this: on the left «route lights, doorway, richer motion, depth»; on the right custom fields, focus
  states, micro-interactions, hierarchy, refined surfaces and a stronger CTA.
- The motion answers the person instead of performing at them: rich where the person acts, silent where nobody does.
  WCAG 2.2.2 holds without a pause control — nothing unbidden lasts more than 5 s, and nothing loops.
- Every element answers a measured defect (LG-1 … LG-6) or the owner's own words.
- The CTA gets its strength from meaning (the key), the width and the weight, not from material (DL A10: metal is the
  hero's).

**Acceptance:** L1–L13 of `surfaces.md` §2.4, amended:
- **L7** → the arrival sentence starts after the LCP entry, lasts ≤ 3.4 s and is cut by any focus. With a scripted person
  (focus on «Courriel» at 2 s, a valid address by 5 s, focus on the password at 7 s), **at t = 10 s three person-driven
  stage states are visible** in captures; `getAnimations()` is empty 1 s after the last input; nothing under forced
  colours; under reduced motion the end states appear at 0 ms.
- **L8** → on submit, the engage plays and the next page is not delayed against the reduced-motion baseline (±1 frame).
- **L13** → the six scales of §3.1.
- **L14** (new) → the CTA computes flat: no `box-shadow`, no inset, no gradient.

**Propagation:** every entrance page — login, the signup's gated message, reset, verification, MFA — through
`allauth/layouts/entrance.html`; the person-driven states run wherever an entrance page has an e-mail or password field.

**Owner?** No. Microcopy without a live string is B1.

### 1.14 The overlay system — modal, drawer, popover, tooltip

**Compared:**
- the product's three unrelated mechanisms: a dialog with a `:target` fallback, a row `popover`, a `<details>` account
  menu;
- gate 0's keyframe-only overlays: no exit, the scrim at once;
- the native specification: DS §10.6; DL R-02, R-07, R-09, R-21; MS §6–§12; EM §8 «Slide»;
- the 21st sources searched and shortlisted in GROUP_4 (§2–§5, §13).

**Chose one ILE system on native elements**, opened by one shared module (`static/js/src/overlay.js`), with one sheet
(`static/css/v5/overlays.css`). The desktop portico panel uses the same primitives (§1.12).

**Shared anatomy:**
- **Surface:** a paper sheet (`--surface-raised`) with a 1 px `--line-rhythm` edge — no lit arris on paper (§1.4).
- **Shadow:** popover `--shadow-3`; modal and drawer `--shadow-4`.
- **Scrim:** `--scrim-modal`, opacity only, never a blur.
- **Radii:** tooltip 4 · popover 8 · dialog, drawer and sheet 12 (top corners only for a sheet, inline-start corners only
  for a drawer).
- **Head:** start-aligned; a sans title at `--u-section`; a 40 px glyph disc for a consequence; «Fermer», 44 px, at the
  inline end — **always present**: a grip or a scrim is never the only way out (WCAG 2.5.7), and a test proves it.
- **Body:** scrolls with `overscroll-behavior: contain`.
- **Foot:** pinned; the primary at the inline end; a destructive action last, as the garnet outline.

**Families:**

| Family | Element | Dismissal | Motion in → out | ≤ 640 px |
|---|---|---|---|---|
| Tooltip | the control's own `::after` with `attr(aria-label)`; inside a clipping ancestor (the rail's `.rail__scroll`, scrolling tables, drawer bodies) the top-layer variant: one shared `popover="manual"` element placed by anchor positioning or by script | leave, blur, Esc (script), press: 0 ms; a hover bridge between the control and the tip (WCAG 1.4.13) | 400 ms wait, then 120 ms opacity; a warm group; instant from the keyboard | none |
| Popover / menu | `popover` + `popovertarget`; anchor positioning with a flip / clamp fallback | light dismiss, Esc, focus leaving (S-7) | a 4 px drop + opacity, 200 ms → 120 ms | bottom sheet |
| Modal / alertdialog | `<dialog>`, `showModal(opener)` | Esc; the scrim only when pointerdown *and* click land on it; an alertdialog never closes on its scrim, and its Esc is the safe answer | scrim 200 ms; 0.96 → 1 + opacity, 320 ms → 120 ms; closes on the server's result | bottom sheet |
| Navigation drawer | modal `<dialog>` | Esc, the scrim, a link | «Slide»: ±100 %, `--ease-enter` 320 ms → `--ease-layout` 200 ms; the scrim moves with the panel | full width («Quiet» on the public phone) |
| Preview drawer | a non-modal panel beside the list on desktop | Esc, Back, «Fermer» | «Slide» from the inline end; content swaps never replay the slide | modal sheet |
| Bottom sheet | `<dialog>` from the bottom | Esc; the scrim (not with unsaved input); the grip; «Fermer» | `--spring-sheet` 550 ms → 200 ms; a 48 px bleed; safe areas | — |

**Mechanics:**
- The state is set at t = 0.
- Transitions run both ways, with `@starting-style` and `allow-discrete` on `display` and `overlay`.
- Nothing that shapes a panel sits under `[open]` (B1). A leaving panel is `inert` (B2).
- `::backdrop` reads custom properties from its dialog (B3).
- 0 ms from the keyboard; the `--motion-reduced` opacity under reduced motion.
- RTL through one `translate: calc(100% * var(--dir)) 0`, covered in `test_rtl_browser` because the static guard cannot see
  it (§2.5).
- **History:** the preview drawer's Back keeps `?état=`, and content swaps use `replaceState`.

**Support and fallbacks** (RTE-M7). Every overlay opens, closes, contains focus and dismisses correctly on the current and
previous major versions of Chrome, Edge, Firefox and Safari; the rest is enhancement:

| Feature | Floor | Without it |
|---|---|---|
| Popover API | Firefox 125 | `overlay.js` toggles `hidden`, with the same light dismissal and Esc |
| `@starting-style`; the `overlay` property | Firefox 129, Safari 17.5; `overlay` is Chromium-only | the surface appears and leaves at once |
| anchor positioning | Chrome 125, Safari 26, Firefox later | `overlay.js` places by `getBoundingClientRect`, with the same flip / clamp |
| `::backdrop` reading custom properties | Chrome 122, Firefox 120, Safari 17.4 | the scrim's fallback colour |

Playwright WebKit and Firefox run in W2-A's own gate (open, close, Esc, focus return, the trap), not only in Wave 4.

**The INP rule:**
1. Each dialog is laid out in advance, at idle, and opened with `showModal(opener)`.
2. The cold open is measured on the heaviest pages: «Mes pièces» in Arabic, and the phase-3 home at 390 (n ≥ 9, CPU ×4).
3. If p90 stays > 200 ms, the dialog opens with `show()` + the shared scrim + a script focus trap (Tab wraps inside) +
   `aria-modal="true"` + Esc + focus return, proved by keyboard browser tests. Never `inert` on `main` alone: the header,
   rail and footer would stay tabbable, `aria-modal` would be false, and INP_QUIET §0 measures little gain.
4. Never `content-visibility` on page chapters (R3A-1).

**21st sources** — the mechanism only, route A, adapted to ILE under the CSP:

| Family | Adopted | Declined |
|---|---|---|
| Modal | #26905, #22490, #23539, #26651 (#24871 as the list of defects to avoid) | #23539's 12 px rise; every hold-to-confirm (#28348, #29383) |
| Drawer / sheet | #23558, #11443 (+ #24837), #25376, #16095, #17826, #31360, #29334 | #11443's `backdrop-blur` |
| Tooltip | #23572, #34684, #22232, #29880 | #23572's glide and blur |
| Popover | #34684, #23548, #11561, #23696 | — |

**Not built in V5.4:** the «Définition» legal-term popover. It would show a locked definition away from its page, which
needs a legal reading. Parked (§7).

**Because:**
- V54 l.22 asks for one premium system.
- Native elements give the accessibility behaviour for free.
- The specification and its measurements already exist: «Slide» matches gate 0 to 0.1 px and adds the exit, the scrim and
  the retarget; every tap ≤ 200 ms at CPU ×4 (EM §8.5–§8.7).

**Acceptance:** O1–O9 of `surfaces.md` §4.4, plus **O10** the WebKit and Firefox smoke, and **O11** a tooltip on an
icon-only control in the collapsed rail shown whole, hoverable and dismissed by Esc.

**Owner?** No.

### 1.15 Card personalisation — the Product Architect's decision

**Compared** each gesture, audience by audience (`platform.md` §4.2): drag to reorder, reorder with buttons, resize, hide
and show, stored preferences, pinning.

**Chose no card board.** Instead, in order of value:
1. **The system orders priority.**
   - Four NowPanel variants: «à vous» · «en attente d'un tiers» · «rien à faire» · «pas encore de dossier».
   - An overdue deadline takes over the NowPanel.
   - A region the account cannot use is not rendered. An empty region is one line.
2. **Native `<details>` disclosures, for secondary content only.**
   - Academy, the pre-assessment sources, «Derniers dépôts», closed deadlines.
   - The server picks the default from the data. The choice is not remembered.
   - Never on a binding region.
3. **Filters and sorts live in the URL** (`?état=`): shareable, nothing stored.
4. **The existing per-account preferences stay:** language, e-mail notifications, the rail collapse (applied before the
   first paint).
5. **Later, outside V5.4:** an «Épingler» toggle for organisation and staff lists, stored on the account. It needs the
   privacy text checked first (B).

**Because:**
- A person's priorities follow legal obligations, and the system knows them better than the person does.
- Drag needs WCAG 2.5.7 and 2.1.1 alternatives, plural strings in four languages and tests for every role — a high cost
  for low value here.
- V3 removed remembered tabs and a stored density switch, for good reasons (`platform.md` §4.1 P2).
- Letting a user hide a binding region would be product policy (C). Refused.

**Reported, not silent** (RTD-m11). V54 l.20 lists personalisation among the targets, so W3-B's report shows the value
matrix (`platform.md` §4.2) and what replaced personalisation: system-ordered priority, disclosures, URL filters and the
kept preferences.

**Owner?** No. V54 l.21: «the Product Architect decides».

### 1.16 Imagery — the rules applied, and who decides what

**Who decides:**
- The **Image Art Director** decides every frame, crop, grade and slot budget, inside the rules below.
- The **Creative Director** holds the veto on register: cliché, stock feeling, editorial drift.
- The **owner** is asked only to widen O54 / O55, or to fund a commission (§1.19, D2).

**The rules:**
- **One significant image, one primary context** (the audience). It is reused only inside that context (AUM rule 1).
  Within a context, the same frame never appears twice on one page: the panel, the hero entrance and a card each show a
  different frame.
- **O54, read prudently.** No arcade, covered passage, step, vault, door or gridded window as a photo subject; S1 and S3 are
  held.
- **O55: no identifiable person.**
  - People are seen from behind.
  - The three partial profiles are held.
  - The mega-menu figure with a three-quarter face is retired.
- **A place is what the record says** (AUM rule 7). **One room, one category; one shoot, one context** (rule 8).
- **Records:** self-hosted files; licence and author in `docs/IMAGE_LICENSES.md` + `PROVENANCE.json`.
- **The grade:** the one V5 grade (PN §2). No veil, no duotone, no mirroring, no EXIF / XMP / ICC in derivatives.
- **Delivery:** AVIF + WebP srcset within each slot's budget; lazy, except the LCP image.
- **The door photograph** stays exactly as served: its look is the approved one, and colour-managing it would change it
  (that would be brand, A).

**Black-and-white → colour — in the home hero only** (V54 l.9 asks it there; RTD-M3):
- In the hero, the four audience photographs rest in black-and-white at full tonal range and take colour under the hand
  and once in the first movement — «colour follows light» (HF §6). Built as a static greyscale twin of the same file
  under the colour image, cross-faded by opacity: the `filter` is set once and never animated (MO-14); the image is
  downloaded once; the layer is isolated with `contain: paint` (B4).
- **Everywhere else, an audience photograph rests in colour, in the V5 grade** — the navbar panel's included. Off the hero
  there is no light for the colour to follow, and greyscale at rest becomes the catalogue hover the 21st curation graded
  «D for the treatment» (GROUP_4 #20029). On a phone, with no hover and a tap that navigates, the photographs would stay
  grey; IA rejects black-and-white frames as «another language».
- A wider use needs its own taste test on that page at ≤ 1 P\*, with #20029 named as the catalogue comparison.
- The hero's one chair conflict (HE §8.4 item 1, dimming at rest) is settled by the hero-final brief: no dimming,
  black-and-white at full range (HF §12.1). The door — the only colour photograph of the first screen at rest — leads
  (TS §24 row 4: «the door does not yield»).

**Film:**
- Zero stock loops, and no film in the hero.
- DL A21: «not one of the 15 says something its own still does not».

**The Università frame** (AUM `cours-tableau-dos` against H-E `paillasse-deux-etudiantes`):
- The hero-final build settles it for the hero entrance.
- The AUM registry is then updated, so that no frame serves two contexts.

**Owner?** No. V54 l.23. Only D2, the optional commission.

### 1.17 The hero — how the separately built result enters the product

**The brief is final** (V54 l.9):
- desktop = E2's narrative flow; mobile = E3's composition; E2's motion carried onto E3 on mobile;
- photographs black-and-white → colour; the Morocco → Italy path;
- fewer lines and dashes; the steps in more evident colour;
- a rotating key / opening; meaningful luminous motion; four entrances legible.

**Who builds it:** the hero-final workflow, wf_4f8e9849-d48.
- Steps: a CD brief (HF) → the build in `P/research/hero/he/` → a six-lens council loop until every lens is ≥ 4 → the CD's
  decision.
- Outputs: `R/research/HERO_FINAL_BRIEF.md`, `HERO_FINAL.md`, and `Q/hero-final/`.
- It builds on the gate-0 foundation's token names. W1-A re-values some of them in the product (radii 4 · 6 · 10 · 14 · 20
  → 2 · 4 · 6 · 8 · 12; no `--f-serif`), so the port re-holds the prototype on the product's tokens before any comparison
  (RTE-M6).

**What the port holds — the invariants as they really are** (RTD-M7):
- **The door stage:** arch, photograph, key and steps present, in place and in drawing; never replaced; never mirrored;
  changed only as V54 l.9 asks. The hero-final changes three things, each under l.9: the steps take more evident colour
  (HF §8); the key turns once (HF §9.1); the door opens — a warm band ≤ 14 % of the leaf at its opening edge, with a spill
  on the steps — and **stays ajar** once the first movement has played (HF §9.2). The first paint and the no-JS page show
  the stage as the owner drew it, closed; under reduced motion the ajar still shows from the first paint.
- **The ajar rest is taken under V54 l.9 and said in words.** An opening that closes again «reads as a refusal» (HF
  §9.2); the aperture is light from inside, not a passage, and it promises nothing. The hero report states it in one
  sentence, with its revert: the band's and the spill's rest opacity (0.8) set to 0 gives the closed rest (a forward
  correction, §2.2), and the tag `v54/w2-d` reverts the port whole. The CD records the choice in DL54 before W2-D starts.
- **The key passes its mirror image mid-turn and ends on the verbatim key** (HF §9.1: 0 px difference): «never mirrors»
  read as «never held mirrored», in DL54 and in the report (§1.9 item 4).
- **The type system** (§1.1) — a grotesque promise, or A-bis if W2-E's test switches it.
- **The corners** (§1.3) — plates 4, cards 8, the arch the only large curve; ≤ 3 radii in the hero box.
- **The CTA** (§1.10), and black-and-white → colour, here only (§1.16).
- **One tier-4 sequence ≤ 5 s** (HF: 3.45 s at 1440, cap 4.0 s); nothing loops; the settled state equals the
  reduced-motion still.
- **One brand expression:** the name drawn once; the locked H1 keeps it semantically. Live copy only; Arabic layout only.
- **One curve, one place per file, one CLS** (reconciled in DL54, RTD-m9): `--ease-turn` (§1.5); the stylesheet at
  `apps/pages/static/pages/css/hero.css`, a page entry (HF §14's `static/css/v5/hero.css` would have to enter `main.css`,
  §2.3); the module at `static/js/src/hero.js`, imported by the home entry; hero CLS ≤ 0.05 (HF §0 item 11, §2.6).

**Entry path: W2-D «Hero port».**
- **Start condition:** the hero-final CD decision is PASSES or PASSES_WITH_CONDITIONS. Its conditions become the port's
  acceptance items.
- **Step 0 — the constraint check, before any port code.** The invariants above are checked against the hero-final build
  (`HERO_FINAL.md`, its council files and the build itself). Any constraint the build does not already meet is resolved
  by the CD in DL54 before the port starts — never discovered by the parity check.
- **Step 1 — the re-hold.** A scratch copy of the prototype (in E/w2-d/; the proof stays untouched) is loaded on the
  product's W1-A token sheet, and its held frames are captured again: they are the parity reference.
- **What the port writes** (its owned files, §3.4):
  - `templates/pages/home/_hero.html` (HF §14's markup; the `d.*` contract kept);
  - `templates/pages/home.html` (the LCP preload re-pointed, the page sheets, the one home script);
  - `apps/pages/static/pages/css/hero.css`, importing `static/css/v5/_door.css`. The prototype's 300+ literal colours and
    67 gradients become named tokens in a hero block of `static/css/v5/tokens.css` (C9), so the app-sheet rule of
    `test_design_docs.py:937` stays whole — a budgeted step, with its own parity re-check. `v4/hero.css` leaves
    `main.css` through the steward;
  - `static/js/src/home.js` — the home's one entry: it imports `hero.js` (the hero module: sampling at idle, every guard
    of the fix pass) and the dismissible notice moved verbatim from `apps/pages/static/pages/js/home.js`, which is
    deleted (one request fewer);
  - the door-master derivatives (AVIF + WebP, 400–2383 px) in `static/brand/v5/`; the four photographs in
    `static/img/photos/`, with their provenance;
  - the retargeted tests: `apps/pages/tests/test_home.py` (51 tests) and the doorway markup tests.
- **The parity check** (it replaces a second full council on the composition):
  - **Pixels:** the hero box only, the chrome masked, at 1440 × 900, 1366 × 768, 390 × 844 and 360 × 800, fr and ar, at
    rest and at three beats, within 1 % of the re-held frames;
  - **The clock** (`data-he-clock`) identical within one frame;
  - **Performance,** on 8782 in one lock window, n ≥ 9 interleaved cold loads per cell. LCP and the first-render task are
    compared with (a) the product's W1-0 «before» set and (b) the re-held prototype plus the expected delta of the
    product's larger CSS, stated before measuring (`main.css` at its ceiling + `hero.css`; about 5 ms per KB gzip of
    render-blocking CSS on slow 4G, RTE-M6). «No worse» means a median difference within PFR §1's resolution: ≤ +30 ms
    for the first-render task, ≤ +50 ms for LCP, reported with both medians and the spread;
  - 4 / 4 entrances in the first viewport at the 18 sizes; 0 CSP violations; 0 console errors.
- **Council:** the hero council's design, accessibility and performance chairs re-read the product page; **taste sits as a
  full chair**, because the context changes — the real chrome, the real fonts, the chapters below (RTD-m13); motion reads
  the filmstrips; the CD signs the port.
- **If the decision is REDO:** the home keeps the V4 hero re-valued by the V5 tokens. The hub labels it «V4 + fondation»,
  it stays off the hub's default path, and no report shows it until the hero passes.

**Owner?** No. V54 l.9: «do not ask E2 vs E3 again». The ajar rest is reported in words, not asked.

### 1.18 The other delegated decisions — one row each

| Row | Decision | Source |
|---|---|---|
| D04 · the targa's seat | §1.11 | DL A11 |
| D05 · the public panel and bar | §1.12 | DL A14 |
| D06 · console navigation | P-A «Tre livelli». The rail is global navigation; the band shows the current object; actions sit at the band's end or in the phone action bar. The current entry is «il lume», after a taste check of its kinship with a well-known active indicator (fallback: the edge bar). One rail per account type (`shell_navigation(user, space)`), with «Changer d'espace» for multi-role accounts. «Site public» at the rail's foot. The ten destinations are kept. «Aller à…» is staff only. The bottom bar holds ≤ 4 entries + «Menu». A pinned rail foot and one density step on fine pointers (S-1); a second skip link to «Menu» (S-2); phone chrome ≤ 120 px (S-3). The rail's destinations, URLs and permissions are unchanged, so no policy question arises. | DL A15; NV §11; UPl §8 |
| D15 · «Mes pièces» | Three groups, by who acts. No row menu: the whole row is the target. The count at 20 px. The strip and the beads are drawn side by side, then the council keeps one. Search hidden for ≤ 12 pieces; variant B not now. The register by its own width: 6 columns from 66 rem, 5 from 52 rem, cards below. Media queries for the page; container queries only inside narrow columns. The Dépôt draws all 11 of the server's answers. The preview drawer is non-modal on desktop. The group words stay as existing catalogue strings until B1 signs «À vous · En cours · Réglées». «Bloqué» is not added as a piece state (policy, C); V4's «Bloqué» on the Conditions gate stays. | DL A16; DW §17 |
| D16 · the journey «La soglia» | OJ1 A′: no relay brackets until the actors' mapping is signed. OJ2: a dossier in `SELECTION` sits on threshold A. OJ3: the council chooses between the beads and «il registro» on the drawn pair. OJ4: the light should play only when the position has changed, which needs a stored last-seen position (policy, C — not pursued); in V5.4 the rail is drawn still at load, with no relay. OJ7: `ile-steps` beside the title. One marker per column: the numeral on the public passage, the glyph on the console's «Mon parcours», the holder on its own row (TS §24 row 8). The OJ5 / OJ6 words wait for B1. | DL A19; JS §10 |
| D17 · platform words and events | One counter per event in the presentation: one live region, a dot on the rail. A deadline's distance in words, within 14 days and when late. The urgency ladder stops once a piece is filed (F8). The Dépôt on a phone: one sentence, one button. The timeline titled by what changed. The wordings are B1. «Since your last visit» and one-event notification semantics are policy (C) — not pursued. | DL A30; UPl §8 |
| D19 · the photographs | §1.16 | DL A20 |
| D20 · film | Zero loops; no film in the hero. The Forum recording appears only if the owner publishes it — not pursued now. | DL A21 |
| D21 · Arabic | Vazirmatn (§1.1). Fallback per component, never per string. Nothing under 14 px. Overflow probes at 360 / 390 / 412. Languages by their own names. The review of the faces and translations is B2. | DL A7, A25 |
| D22 · the door photograph | Kept as served. Its rights record is an owner action before anything goes remote (§7). | DL A22 |
| D24 · the home under the hero | The audiences offered twice at most above 1.5 screens (RH-5). «Il gradino» on its own plate. Chapter 01 shows no second set of the four photographs (four bays only if the hero has no lintels). The diptych «Lo stesso gesto» as a pair. The description paragraph moves out of the hero but stays on the desktop page (K16). The French-typography filter, on team-authored strings only — never on locked copy (§1.1; B1 item 8). The promoter sentence and the recast of «ÊTES-VOUS…» wait for B1. | DL A24; UPu §10 |
| D26 · the grammar of a legal page | Adopted as layout **slots**: one inset, one action, an authority link's host made visible, a caption and credit under every photograph, and a «who can help me» slot filled with live text only. Headings stay verbatim: headings as the reader's questions, and the «who can help me» wording, are copy and arrive through B1 item 7 (RTD-m5). The «verified on» line appears only where a date and a verifier already exist — no new commitment. The review calendar is C — not pursued now. | DL A31 |
| D27 · the first-render clause | Read as «no long task beyond the first render». The first-render task is budgeted per page (§2.6). `content-visibility` stays off (R3A-1). Font preloads are part of base.html's contract. | DL A27 |
| D28 · H-E's motion | Superseded by the hero-final score; its council binds, inside §1.17's invariants. | DL A29 |
| D29 · signing the pictures | Settled by V54: an internal family gate, propagation without per-family approval. | DL A1 |
| D30 · process | The flagged skills are not invoked; the reviewers apply their written rules (MS, EM). The 21st and Pexels keys: the owner rotates them before anything goes remote. | DL A28 |
| D31 · register entries | O13 lighter console, kept · O19 sand, confirmed · O29 route lights once · O30 public View Transitions off · O34 the tab indicator in CSS · O36 handled without a schema change (§1.12) · O61 «Bordo d'oro» retired as the default (CTA-B) · O62 the register strip · O63 «Menu» in the phone bar + a second skip link · O65 six registry types. O42, O43, O46 and O47 are owner items (B / C), parked or in B1. | DL C |
| Track T · truth defects (`IMPLEMENTATION_PLAN.md` §2) | T1–T3 by unifying presenters on the **existing** precedence: one `next_action` feeds the dashboard, the case and the documents; the case lists its checklist and its requirements; orientation stays inside the console when signed in. No rule changes. T4–T9 as written, each re-measured. Changing the precedence itself would be B / C — not pursued. | IP §2 |

### 1.19 The owner's items (classes A–E of V54 l.7) — the complete list

| Class | Item | Blocking? |
|---|---|---|
| **A** brand | **None asked.** The mark, the wordmark and the tricolour are untouched, and the door photograph keeps its look. Three changes made under the owner's own directives are **said in words in their reports**, each with its revert: the hero's door rests ajar after the opening, and the steps carry more colour (V54 l.9; §1.17); the key passes its mirror image mid-turn and ends on the verbatim key (V54 l.9, l.19; §1.9); the mark moves once per sign-in, across the page load — BA §1 amended in DL54 (V54 l.19; §1.9). | — |
| **B1** content / legal | **One copy-and-legal packet.** The team drafts the French; the owner and counsel approve; the owner's translators translate (we never translate Arabic). Items, in order: **1** the panel descriptions (≤ 90 characters, four languages) · **2** login microcopy without a live string (Caps Lock hint, session-ended line, unhappy-state sentences) · **3** «Mes pièces» group words and glosses, the caption's third clause, «La personne» / «Vous», two durations on a row · **4** deadline-distance words, the timeline title, the Dépôt's phone wording, the throttle sentence · **5** OJ5 / OJ6 and D-U9 / D9 · **6** the recast of «ÊTES-VOUS…» and the promoter line (with counsel) · **7** legal pages' headings as the reader's questions, and the «who can help me» wording (D26) · **8** the French typography of locked copy — U+00A0 inside prescribed texts (with counsel; §1.1). | No — until each item is signed, the build uses live strings only, and locked copy stays byte-identical |
| **B2** content / legal | **The Moroccan reader and the Arabic edition:** O10 (now for Vazirmatn alone), the Allegato 1 translation, IC Q8 (`ile-steps` mirroring — decided «no mirror», open to comment), IA Q9, «المسؤول». | Only for signing `/ar/` and the main merge; the build proceeds with Arabic layout and French locked copy, as today |
| **C** product policy | **None asked.** Every change that would alter the business workflow is left out of V5.4. The list is in §7. | — |
| **D1** irreversible | **Later, not now:** at the integration milestone, merging design-v5 into main ends the V4 control; main is tagged `v4-control-final` first. | Asked only when Wave 4 has passed |
| **D2** high cost | **Optional:** a commissioned shoot (O56) for what stock cannot give — a Persona with a Moroccan sign, institutions cooperating, an Italian workplace in Italy, Rovigo, a Forum hall (IA §7). Default: reviewed stock, under the prudent readings. | No |
| **E** true creative tie | **None.** The one chair conflict (the hero's rest exposure) is resolved by HF §12.1 (§1.16). | — |

---

## 2. INTEGRATION ARCHITECTURE

### 2.1 The shape — architecture A: in place, alias-first, family by family

**Compared** three architectures (`product.md` §10):
- A — in place, alias-first;
- B — a switch (`data-design="v5"`) with a second bundle;
- C — a parallel `templates_v5/` tree.

**Chose A.**

**Because:**
- **The precedent worked.** V4 entered the same way: `2adfd1f`, 18 commits.
- **V5 was drawn for aliasing.** It shares 78 custom-property names and 110 class names with the product by design. Aliasing
  is its natural mechanism; scoping fights it (every rule gains a class, and the comps' measured cascade no longer
  transfers).
- **One tested path at all times.** No CSP change, no build-system change beyond one rule, no infrastructure change.
- **B** would bring the A/B catalogue back to the owner. **C** defers all the integration risk to one flip commit.

**Rules:**
- **Honest states** (RTD-M9). Between W1-A and its own family, a page is «V4 + fondation»: V4's composition on V5's
  tokens. That is a hybrid, and it is labelled as one — the hub shows it as «V4 + fondation», never as V5, and no report
  presents it. A page is «V5» only once its family has passed its council.
- **No page worse than before.** W1-A's tokens re-value every page at once. The before / after set (W1-0) is judged pair by
  pair, and a page judged worse blocks the merge (§3.1 item 6).
- **Delete what you supersede** (RTE-B1). Each family deletes, in its own merge, every legacy rule its components replace —
  V1 as well as V2–V4 — section by section, by the deletion map of §2.3. A shared legacy sheet goes section by section, and
  its last named consumer deletes the file.

### 2.2 Branches, worktrees, the live preview, reversibility

**Branches and worktrees:**
- **design-v5** (worktree `C:/tmp/ile_wt/design-v5`) is the integration branch: the steward merges, builds and tests there.
  **8780 does not serve it.**
- **v5-live** (worktree `C:/tmp/ile_wt/v5-live`, a detached HEAD) is what 8780 serves: always the last green tag. After a
  merge passes, the steward runs `git -C C:/tmp/ile_wt/v5-live checkout --detach v54/<family>`, and the orchestrator
  restarts 8780. Rolling the preview back is checking out the previous tag — instant, no revert. The owner never sees a
  merge in progress, conflict markers, or new static files on stale templates (RTE-B2).
- **main** stays V4 (8770 / 8771 / 8772) until the integration milestone (D1). It is **never merged** into design-v5: at
  each wave start the steward cherry-picks main's code commits (non-design fixes) and lists them in the changelog;
  documentation-only commits on main are never brought over (RTE-m3). W1-0 cherry-picks `31048b6` (dev
  `DB_CONN_MAX_AGE` 0 + its test) and tags `v54/base`.
- **One branch per family:** `v54/<family>`, in its own worktree `C:/tmp/ile_wt/v54-<family>`, with `.env` copied and a
  `node_modules` junction **to design-v5's own `node_modules`** — never to main's (RTE-M1). It is branched from design-v5
  at the wave's tag and commits in small steps.

**Node.** W1-0 replaces design-v5's `node_modules` junction — today it points into `C:/tmp/italylegalentry/node_modules`,
the V4 control — with its own `npm ci` from design-v5's lock file. Only the steward runs `npm ci`, `install` or
`uninstall`; `package.json` and `package-lock.json` are serialized files.

**Generated files.** `.gitattributes` gains `static/css/dist/** -diff merge=binary` and `static/js/dist/** -diff
merge=binary`, so a conflict never writes markers into a bundle. The steward deletes `static/js/dist/` before `build:js`
(esbuild does not clean its `outdir`, and stale hashed chunks would pile up) and rebuilds every bundle after each merge.

**The merge** — the steward, one family at a time:
1. Check the family's diff (`git diff --name-only <wave-tag>...HEAD`) against its slice of the ownership manifest with
   `scripts/check_ownership.py`; a path outside the slice stops the merge.
2. Merge with `--no-ff`: one merge commit per family.
3. Rebuild `dist/` from clean. Regenerate the inventory tables (DS 2026 §2 weights, §6.2, §10 count, §12, §16, §19; the
   A11Y counts) with `scripts/regen_design_inventory.py`, and `docs/qa/design/capture-report.json` with `capture.py`
   whenever pages, icons or the chrome changed. Families never edit these by hand.
4. Run the suites of §2.7: the full set, browser tests at 0 skips.
5. Tag `v54/<family>`; update `live_status.json` and the changelog; check the tag out in v5-live; the orchestrator
   restarts 8780.
- **Before any propagation step inside a family:** a checkpoint commit + tag `v54/<family>/pre-propagation`.

**Reversibility — the policy as it really is** (RTE-M8):
- **Only the most recent family merge is reverted** (`git revert -m 1 <merge>`, then the dist and the inventories
  regenerated and the tag moved). An older family is **corrected forward**: later families build on it (W1-C's buttons
  and fields sit under every W2 family) and share the inventories, the tests and the dist.
- **Re-landing a reverted family** is a revert of the revert on top of design-v5, then its fixes, then the normal merge
  gate.
- **The preview** rolls back by tag checkout in v5-live, at once, whatever is happening in design-v5.
- **main** is tagged `v4-control-final` before the D1 merge.
- V54 l.30's «propagate without per-family approval» rests on this policy; each report states the family's tag.

**The ownership manifest** (RTE-M4): `docs/design-v5/OWNERSHIP_V54.json`, written by W1-0 from §3's lists — per family,
path globs, plus function- or section-level slices for shared files. `scripts/check_ownership.py` reads it before every
merge. A file not in the manifest has no writer until the steward assigns it.

**Serialized shared files** — one writer at a time, merged only by the steward:

| File | Rule |
|---|---|
| `package.json`, `package-lock.json` | the steward only |
| `static/css/main.css` (the import list) | W1-A in Wave 1; afterwards each family's own deletions, through the steward |
| `static/css/v5/tokens.css` | W1-A; later families append one named block through the steward (W2-B the door stage's, W2-D the hero's) |
| `templates/base.html` | W1-A (head, preloads); W2-C1 (the `chrome` block). Nobody else: the loader and the navigation load through `shell.js` (§2.3) |
| `static/js/main.js` | by function: `initTabs`, `initAccordions` W1-C · `initMisc`'s submit guard → L2 W1-D · `initDialogs`, `initDropdowns` W2-A · `initNavigation` (moved into `nav.js`) W2-C1 · `initReveal` W4-B — each with its DS 2026 §16 row; merged in completion order, the steward resolving the `init*` call list |
| `templates/partials/portal_chrome.html` | W1-D (the rail mark's release hook) → W2-A (the drawer element) → W3-A |
| `apps/portal/static/portal/console.css` (the import list) | W1-D (the `_loader-light.css` import) → W3-A → each Wave-3 family adds its own partial's import, through the steward |
| `templates/components/form_field.html` | W1-C → W2-B (the reset slot) |
| `tests/frontend/test_layout.py`, `tests/i18n/test_rtl_browser.py` | existing functions by slice (fonts W1-A; mirrors W1-B; account menu W2-A; entrance W2-B; header W2-C1); **new tests go in new per-family files** (`test_layout_<family>.py`, `test_rtl_browser_<family>.py`) |
| `docs/design/DESIGN_SYSTEM_2026.md`, A11Y, `tests/frontend/test_design_docs.py` | families edit their own prose sections and test functions; the inventory tables are the steward's, regenerated |
| `docs/qa/design/capture-report.json` | the steward only, by `capture.py` |
| `apps/portal/services.py` | Wave 3 order: W3-A → W3-B → W3-C → W3-E |
| `apps/cases/services.py` | W3-B (T1) → W3-D (`journey_for`) |
| `apps/core/chips.py` · `apps/core/icons.py` | W1-C · W1-B |
| `apps/designpreview/**`, `config/settings/dev.py` | W1-0 (the specimen route) → W1-P; `live_status.json` the steward only |
| `config/settings/base.py` | W2-B only (one setting: `ACCOUNT_FORMS`) |

### 2.3 Directories, loading order and the deletion map

**Fonts**
- `static/fonts/v5-*.woff2`: Host roman variable, Host italic, ILE Wordmark, ILE Mono, Vazirmatn variable.
- **Licences** (RTE-m2): the SIL OFL 1.1 text for each family in `static/fonts/licenses/` — Host Grotesk; Newsreader (the
  wordmark subset); IBM Plex Mono, whose «ILE Mono» rename keeps IBM's copyright notice («Plex» is a Reserved Font Name);
  Vazirmatn — referenced from the header of `v5/fonts.css`. The repository holds none today.
- `docs/design-v5/FONTS_V5.md` records the sources, versions, subsetting and renaming commands, and the hashes.
- The V4 faces and `static/css/fonts.css` leave design-v5 in the W1-A merge. main keeps them.
- The ILE Mono rename (and the check of Host's «Light» name-table entries) uses the fontTools the proof's tools already use:
  a dev-time step outside the product's requirements; no runtime dependency.

**What every page loads — `main.css`.** `static/css/v5/`, imported after `v4/*` in this order: `fonts.css`, `tokens.css`,
`aliases.css` (DS §13: V1 / V2 / V4 names → V5 values), `base.css` (type roles, focus, night, RTL), `buttons.css`,
`field.css`, `chip.css`, `card.css`, `notice.css`, `tabs.css`, `overlays.css`, `loader.css` (L2 and L3 only), `chrome.css`
(the public chrome).

**Page-only CSS — never in `main.css`** (RTE-B1 item 3): `_`-prefixed partials in `static/css/v5/`, each imported by the
entries that draw it.
- `_door.css` (the door stage, as drawn) → the home's `hero.css`, the entrance's `entrance.css`, and the console entry for
  the one empty state that shows the door.
- `_loader-light.css` (generated; the L1 release) → the console entry.
- `_journey-passage.css` (the public passage) → the page sheets of the pages that draw it.
- Their gradients and literal colours are tokens in `v5/tokens.css` (C9).

**Console-only CSS — out of `main.css`** (≈ −6.4 KB gzip on public pages, IP §4): `_`-prefixed partials in
`apps/portal/static/portal/v5/`, imported by the existing entry `apps/portal/static/portal/console.css`, which
`base_portal.html` loads and every console template keeps through `{{ block.super }}`.

**The one build change.** `scripts/build_css.mjs` skips `_`-prefixed files as entries wherever they are (their importers
bundle them); `test_css_bundle_is_current` learns the same rule. `test_design_docs.py:612` becomes «every non-partial
`static/css` sheet is imported by `main.css`; every partial by at least one entry», and `:500–512` and `:1050` read the
console entry and the page sheets as well as the `main.css` cascade.

**Page sheets** stay app entries, loaded in `extra_head`: the home (`apps/pages/static/pages/css/pages.css`, `hero.css`), the
entrance (`apps/accounts/static/accounts/entrance.css`), documents, companies, and so on. App sheets keep
`test_design_docs.py:937`'s rule — no gradient, no `rgba(`, no hex; tokens only.

**The deletion map** — who deletes which legacy CSS, in their own merge (RTE-B1 item 2); the section count checked by
`test_design_docs.py:658` is updated in the same merge:

| Legacy | Deleted by |
|---|---|
| `fonts.css`; the declarations of V1 `tokens.css`, `v2/tokens.css` (except the brand colours, `test_v4_tokens.py:265`) and `v4/tokens.css` that `v5/aliases.css` re-declares; the adopted names in `_legacy-tokens.css` (§2.7); V1 `base.css`'s type roles, links, digits and focus | W1-A |
| `components.css` §2 icons | W1-B |
| `components.css` §1 buttons, §3 badges, §4 notices, §13 cards, §14 tabs, §15 accordion, §20's field rules; `v3/buttons.css`, `v3/chip.css`, `v4/buttons.css`; `register.css`'s status pastille | W1-C |
| `components.css`'s universal reduced-motion block (`:3071–3091`) | W1-D |
| `components.css` §8 account menu, §21 dialog; `v4/workspace.css`'s row popover | W2-A |
| `components.css` §27's entrance rules | W2-B |
| `components.css` §5 utility bar, §6 language switcher, §7 header and drawer, §25 footer; `v2/shell.css`; `v4/shell.css` | W2-C1 (W2-C2 for the drawer's last rules) |
| `v4/hero.css` | W2-D |
| `components.css` §11 banner, §12 four entrances; `v2/routes.css`; the home's old rules in `pages.css` | W2-E |
| `v4/workspace.css`: Panel, HealthStrip, facts, ContextHeader | W3-B |
| `v4/workspace.css`: DocumentCollection / Row / Card, SegmentedControl, search; `register.css`'s register and entry | W3-C |
| `components.css` §16 stepper, §17 timeline; `v2/voyage.css`; `v4/workspace.css`'s JourneyRail; `register.css`'s sequence | W3-D |
| `components.css` §23 empty state; the rest of `v4/workspace.css` (date and message lists, EmptyState, the case header) — **the file** | W3-E |
| `components.css` §9 breadcrumbs, §10 page header, §18 pathway list, §19 CTA panel, §20's FAQ and glossary blocks, §22 pagination, §24 local navigation, §26 errors, §27's manage pages, §28 legal page; `v4/wizard.css`; `register.css`'s folio, marginal note, sources, jurisdiction bar, slab and outcome; V1 `layout.css`'s editorial parts | W3-F1 / W3-F2, by page |
| `components.css` §29 reveal | W4-B |
| what remains of V1 `base.css`, `layout.css`, `components.css`, `register.css`, with `v2/bridge.css` (which leaves with `register.css`) and `_legacy-tokens.css` | W4-D |

**JavaScript**
- **One public entry** (RTE-m1): `static/js/src/shell.js`, already loaded on every page, imports `nav.js` (the public
  navigation) and `overlay.js`; `loader.js` is imported dynamically on the first submit; `focus-clear.js` exists only if
  W2-C1's measurement requires it (§1.6). The console keeps `console.js`. The home keeps one entry, `home.js`, which imports
  `hero.js`. `journey-rail.js` is imported by the pages that draw the rail.
- `build:js` bundles each entry automatically (target es2022).
- `motion.js` gains the V5 utilities and the one reduced-motion gate (§1.5). It keeps the Motion-library wrappers that
  `shell.js` and `home.js` still import until their families remove them; the dependency leaves in W4-B.
- `static/js/main.js` (loaded as a module) shrinks as families take its functions (§2.2's slices).
- `static/js/head.js` gains the input-modality flag (`data-input`, R-07) — W1-D.
- `static/js/rail-pref.js` stays: it runs before the first paint.

**Icons**
- `static/icons/src/*.svg` → `scripts/build_icons.py` → `static/img/icons.svg`.
- Same `icon-` ids, with aliases for the V4-only ids (`user`, `shield`, `globe`, `key`, `home`, `list`) until they are swept.
- Plus `apps/core/icons.py`.

**Templates** are edited in place. `templates/components/` stays flat, because the §10 check is non-recursive. The
foundation families' specimen boards live in `templates/dev/designpreview/specimens/<board>.html`, rendered by the
dev-only specimen route.

**Images**
- `static/brand/v5/`: the door-master derivatives.
- `static/img/photos/` + `PROVENANCE.json`.

### 2.4 Build

- `npm run build:css` and `npm run build:js` stay as they are, except for the `_` partial rule. The dist stays versioned,
  because production runs `collectstatic`, not Node; it is `merge=binary` and rebuilt from clean by the steward.
- Generated sources are committed, each with a currency test or a steward regeneration:
  - `scripts/gen_loader_light.py` → `static/css/v5/_loader-light.css`;
  - `scripts/build_icons.py` → `static/img/icons.svg`;
  - `scripts/regen_design_inventory.py` → the DS 2026 and A11Y inventory tables;
  - `docs/qa/design/capture.py` → `docs/qa/design/capture-report.json`.
- No new runtime package. No React: IP §7's criteria give route C = 0. No remote script. No font or image hotlinked.

### 2.5 CSP, i18n and RTL

**CSP: unchanged.**
- `'self'` everywhere; `img-src 'self' data:`.
- No inline style or script (JSON-LD excepted).
- The preview's framing exception is a dev-only middleware added in the preview settings (§4.4), not a per-view widening;
  `test_design_preview.py:2670` is updated to say so.

**RTL**
- Logical properties only; one `--dir` variable for translations; an RTL twin for every horizontal shift.
- The closed icon flip list.
- **Never mirrored:** the mark (`direction: ltr`), the door stage, the key, the steps, `ile-steps`, the tricolour.
- Arabic fallback per component, never per string.

**The logical-property guard becomes recursive**
- Over `static/css/**` (excluding `dist/` and `dev/`) and the portal partials.
- With an explicit allow-list for LTR stage geometry: the door stage and the loader light (in the proof:
  `components.css:938,960,1055`, `loader-light.css:16–35`).
- Today it is non-recursive (`test_rtl_static.py:20–25`), so `static/css/v5/` would escape it.
- **What the static guard cannot see** (RTE-m5): translations written as `calc(100% * var(--dir))`, and indicators placed by
  script (the architrave, anchored menus). `test_rtl_browser` covers them: in Arabic, the indicator sits under the active
  item and menus align on the inline end.

**Languages**
- fr (the source), it, en, ar; `prefix_default_language`.
- Locked copy verbatim — the French-typography filter never touches it (§1.1). Arabic: layout only, never translated by
  us.
- The preview process uses its own language cookie, as it uses its own session and CSRF cookies (§4.4).

### 2.6 Performance budgets

**Where and how** (RTE-M9): on the compressed twin 8782 — `CompressedManifestStaticFilesStorage` with `DEBUG=False` (so the
hashed URLs are emitted, and the preload / `url()` hash match behind PFR fix 1 is observed), its own `STATIC_ROOT` with
`collectstatic` after each build, `WHITENOISE_USE_FINDERS=False`, the database `ile_v5_perf` (a clone of `ile_v5` made in
W1-0), `ILE_REFERENCE_DATE=2026-10-03`, `CONN_MAX_AGE` 0 — on slow 4G + CPU ×4, under the lock. **The V4 reference** for
every «≤ V4» budget is the W1-0 «before» set measured on 8782 itself at `v54/base`: the same data, storage and date, not
8772. HTTP/1.1, as the dev server serves; one HTTP/2 measurement behind a local TLS reverse proxy runs before the milestone,
or the milestone report states that it could not.

**Statistics:** n ≥ 9 interleaved cold loads per cell. A comparison is «no worse» when the median difference is within
PFR §1's resolution — ≤ +30 ms for the first-render task, ≤ +50 ms for LCP — reported with both medians and the spread.
Every report states the protocol: n, pooling, tolerance.

| Budget | Value | Source |
|---|---|---|
| LCP | ≤ 2.5 s, every page type, fr + ar, 1440 + 390 | owner, 26 Sep |
| CLS | ≤ 0.10 on every page; **≤ 0.05 on flagship pages** (HF §0 item 11, extended to every flagship); font swap ≤ 0.01 with matched fallbacks; 0.01 elsewhere is a target, not a gate | owner; HF; TR |
| INP | ≤ 200 ms; an overlay's cold open p90 ≤ 200 ms on the heaviest page | owner; `surfaces.md` §4.4 |
| Long tasks | none beyond the first render (D27); the first-render task no worse than the «before» set on the same page; the home also no worse than the re-held prototype plus the stated CSS delta (§1.17) | DL A27; PFR |
| CSS | the ratchet below | RTE-B1 |
| Requests | per page type, CSS + JS requests before `load` ≤ the «before» set's count (the home today: 2 sheets, 5 scripts); font preloads ≤ 2 on Latin pages, ≤ 3 on Arabic ones | PFR §8.3; RTE-m1 |
| Fonts | Latin public ≤ 25 KB · console ≤ 32 KB · Arabic ≤ 56 KB (B measured 20.5 / 29.3 / 51.9) | TR §6 |
| Sprite | ≤ 32 KB raw (≈ 28.6 KB; 6.4 KB gzip) | DS §12 #7 |
| JS | per module: overlay ≤ 4 KB gzip, loader ≤ 4, nav ≤ 4, tooltip helpers ≤ 1; a public page ≤ 45 KB gzip in all | IP §7; `surfaces.md` |
| Images | per slot (AUM §8): the door row ≤ 110 kB on desktop, ≤ 40 kB with the 320 px srcset; nothing above the fold lazy, nothing below it eager | IA §0 |
| Motion | 0 animations and 0 `will-change` at rest; 0 `compositeFailed`; 0 animations at load on console pages, **except the entrance release** (once per sign-in, on the rail's mark, §1.9) | MS; HE §8.5 |

**The CSS budget — measured, then ratcheted:**
1. **Baseline.** W1-0 records, per page type (the home, a door page, an interior page, the login, the dashboard, «Mes
   pièces», the case file): `main.css` gzip, the page's own sheets gzip, their total, and the fonts.
2. **Wave 1 — the transitional allowance:** each page type's total CSS ≤ its baseline + 8 KB gzip, and `dist/main.css`
   ≤ 45 KB gzip at every merge (DS §12 13c).
3. **From the first Wave-2 merge the ceiling never rises:** each page type's ceiling is its measured total at the end of
   Wave 1; every later merge fits under it; the steward lowers a ceiling whenever a merge lands more than 1 KB below it.
4. **At the milestone:** `dist/main.css` ≤ 36 KB gzip — V4's weight today (35.8 KB) — with the console and page-only
   partials out of it and the deletion map complete (W4-D).
5. **A family over its ceiling does not merge.** It first deletes the legacy rules its components supersede (§2.3), then
   moves page-specific rules into page partials. If it is still over, the Performance Lead measures LCP and the
   first-render task with the fonts on 8782 (n ≥ 9); only if both pass may the CD raise that page type's ceiling once, by
   ≤ 2 KB, in DL54. Never above 45 KB for `main.css`.
6. **Re-measured with the fonts after every bundle change** (PFR §6 fix 3: a smaller sheet alone once *added*
   151–248 ms).

**Evidence for every PASS:** traces, run files and captures in E/<family>/, with the numbers and the protocol in the
family's scorecard.

### 2.7 Tests — the V4 pins, their owners, and the suites each wave runs

**The pins and their V5 replacements** (the owning family in brackets; RTE-M3):

| Test today (pins V1 or V4) | Under V5 |
|---|---|
| `test_v4_tokens.py:108` — v4/* closes the cascade [W1-A] | → `test_v5_tokens.py`: v5/* closes it, and the console partials close `console.css` |
| `test_v4_tokens.py:121, 196` — the DS V4 blocks; `--f-sans` is Plex; the Plex preload [W1-A] | the DS 2026 blocks equal the V5 values; `--f-sans` is Host; the preload policy per script (§1.1) |
| `test_v4_tokens.py:231` — reduced motion zeroes every duration [W1-D] | retired into `test_v5_tokens`: tokens zeroed, `--motion-reduced` on opacity only |
| `test_v4_tokens.py:252` — six shadow roles [W1-A] | five levels (SH-1) |
| `test_v4_tokens.py:265, 275, 291, 302` — brand colours only in v2; no literal colour in v4 / entrance / console; registers never green or accent; the z-order [W1-A] | kept, and extended to v5/*, the page partials and the portal partials (the generated loader light allow-listed) |
| `test_static_assets.py:133–171` — token completeness, 4 px line-heights, prose, **every contrast pair**, read from V1 `tokens.css` only [W1-A] | retargeted to the effective cascade (`_effective()`, as `test_v4_tokens` does) or retired into `test_v5_tokens` — never left green on values no page renders |
| `test_legacy_token_shim.py:30–32` — 1,626 of 1,636 used [W1-A] | the names V5 adopts (`--radius-xs/sm/md`, `--control-height`, `--focus-ring-*`, `--z-modal`) leave the shim; `MAX_SHIM_TOKENS` and `MAX_LEGACY_USAGES` lowered; DS 2026 §17 records them |
| `test_design_showcase.py:175–198` — a swatch per palette token [W1-A] | the V5 palette |
| `test_browser.py:211–220`, `test_rtl_browser.py:205–217` — Plex and Naskh in a browser [W1-A] | Host and Vazirmatn |
| `test_design_docs.py:558–595` — `fonts.css`, Plex, Naskh in DS 2026 §6 [W1-A] | `v5/fonts.css`, Host, Vazirmatn |
| `test_design_docs.py:612–659` — every sheet in `main.css`; fonts and tokens first; the section count [W1-A; each deleting family for `:658`] | §2.3's retarget |
| `test_design_docs.py:500–512`, `:1050` — components in the `main.css` cascade [W1-A] | read the console entry and the page sheets too |
| `test_design_docs.py:937` — no gradient, `rgba(` or hex in app sheets | kept; the hero's and the door's colours become tokens |
| `test_design_docs.py:815–845` — V1's reduced-motion block and the navy `box-shadow` focus [W1-D the motion half; W1-A the focus half] | the V5 rule (§1.5) and the focus system (§1.6) |
| `test_design_docs.py:796, 996, 1190–1226` — the keyboard list, G-02, `main.js`'s 80 rem `DESKTOP`, `.nav-toggle` / `.nav-drawer` [W2-C1] | the 1024 px door layout, with DS 2026 §7.2 / §11 and A11Y §3 rewritten in W2-C1's slice (RTE-m8) |
| `test_design_docs.py:1098–1170` — the figures of `capture-report.json` [the steward] | regenerated by `capture.py` after every merge that changes pages, icons or the chrome |
| `test_design_docs.py:1228–1247` — sheet weights within ± 10 % [the steward] | regenerated by `regen_design_inventory.py` |
| `test_design_docs.py:597` — `main.js`'s `init*` list [each slice owner] | updated with the slice |
| `test_page_integrity.py:59` — `_FORWARD_ICONS` [W1-B] | the closed flip list |
| `test_chips_registry.py`, `test_state_chips_carry_a_register.py` — «one of six» [W1-C] | eight registers |
| `test_layout.py:41, 55, 179, 231, 256` [W1-A, W2-A, W2-B, W2-C1 by slice] | the intent kept; `v5/fonts.css`'s families; the entrance contract kept |
| `test_static_assets.py:177, 199, 240, 277` [W1-B] | kept; the sprite swap keeps the ids, or aliases them |
| `test_css_bundle_is_current.py`, `test_css_tokens_exist.py` [W1-A] | kept, plus the `_` partial rule |
| `test_frontend_bundle_is_current.py:45` — Motion's exports [W4-B] | rewritten in the merge that removes the dependency |
| `test_console_shell_stylesheets.py` [W3-A], `test_header_fits_the_narrowest_viewport.py`, `test_browser.py` [W2-C1] | the intent kept; the selectors retargeted |
| `tests/i18n/test_rtl_static.py:20–25`, `:154` [W1-A] | a recursive glob with the allow-list; Arabic = Vazirmatn (main keeps V4's until the milestone) |
| `test_rtl_browser.py` (23 tests) | kept; overlays, sheets, the architrave and anchored menus added in per-family files |
| `test_locked_texts.py:30–37` | unchanged: the filter never touches locked copy (§1.1) |
| `tests/security/test_log_privacy.py:57` [W1-P] | the persona switch logs a persona key, never an e-mail |
| `test_design_preview.py` [W1-P] | rewritten (§4), with the dev middleware chain installed |
| app tests: hero / doorway (5 files, incl. `test_home.py`, 51 tests) [W2-D], header classes (8) [W2-C1], `css/dist/` paths (9) [each owner] | retargeted, family by family |
| forced colours, template comments, `tests/security/*`, `tests/compliance/*` | unchanged |

**New tests:** `test_v5_tokens.py` (with PC D-doc-6's checks — night separation; edges and patterns ≥ 3 : 1; glass over
night — and the reduced-motion rule) · `test_icons.py` · `test_loader_rules.py` (nothing `infinite`; one duration per
phase; the L1 allow-list; L3 on fragments only) · `test_rm_flag_parity.py` · `test_script_motion_gate.py` (no `.animate(`
or `requestAnimationFrame` outside `reducedMotion()`) · `test_overlays.py` (the markup contract; «Fermer» always present) ·
`test_css_budget.py` (the §2.6 ceilings) · `test_image_contexts.py` (no frame in two contexts) · the per-family RTL and
layout files · the rewrite of `test_design_preview.py` (§4).

**The suites** — every lane on its own `TEST_DATABASE_URL` (concurrent runs on `test_ile` deadlock), always on top of
`pytest -m "not browser"` in full, compliance and security included:

| When | Must also run |
|---|---|
| W1-A | all seven browser files (the font swap reflows every page: the 320 px header test, `test_rtl_browser`, pages, portal); `test_design_showcase`; `test_legacy_token_shim` |
| W1-B | `test_static_assets`, `test_svg_wellformed`, `test_page_integrity`, `test_rtl_browser` (mirrors) |
| W1-C | `test_chips_registry`, `test_state_chips_carry_a_register`, `test_layout` (the form contract), the accounts tests, `test_rtl_browser` (forms) |
| W1-D | `test_loader_rules`, `test_rm_flag_parity`, `test_script_motion_gate`, `test_frontend_bundle_is_current`, the portal browser tests (no-JS submit) |
| W1-P | `test_design_preview` (with the dev middleware chain), `tests/security` |
| W2-A | `test_overlays`, the portal browser tests, `test_rtl_browser` (drawers, sheets), keyboard walks; the WebKit + Firefox smoke |
| W2-B | the accounts / allauth flows, the 429 test, `tests/security`, `test_layout` (entrance), `test_rtl_browser` (form) |
| W2-C1 / W2-C2 | `test_browser`, `test_cms_nav`, the 320 px header test, `test_rtl_browser` (nav), `tests/compliance` (the anti-fraud foot, the gates) |
| W2-D / W2-E | `apps/pages` (51 + browser), `test_image_contexts`, `tests/i18n` (locked texts, integrity), the phase-3 leak tests |
| W3-A … W3-E | `apps/portal`, `apps/documents`, `apps/cases`, `apps/companies` (presenters change: T1, F8, F9, F13, `journey_for`), `test_phase_console`, the object-permission and authorisation audits, the portal browser tests |
| W3-F1 / W3-F2 | all of `tests/i18n` and `tests/compliance`, `apps/orientation` compliance, the `apps/ecosystem` browser tests |
| The steward, every merge | everything, with `-m browser` at **0 skips** (`-rs`, failing on any skip); `npm run build` from a clean `dist/`; the currency tests; `capture.py` when pages, icons or the chrome changed |

### 2.8 Servers and measurement

| Port | What | Rule |
|---|---|---|
| 8780 | the owner's live V5: the **v5-live** worktree at the last green tag, `ile_v5`, `ILE_DESIGN_PREVIEW=1`, `ILE_REFERENCE_DATE=2026-10-03`, `--noreload`, `DB_CONN_MAX_AGE=0` | restarted only by the orchestrator, after the steward has checked a new tag out; no lane, chair or agent loads it |
| 8782 | the compressed twin: the worktree under measurement (a family lane before its merge, design-v5 after it), `CompressedManifestStaticFilesStorage`, `DEBUG=False`, its own `STATIC_ROOT`, `WHITENOISE_USE_FINDERS=False`, `ile_v5_perf`, `ILE_REFERENCE_DATE=2026-10-03`, `CONN_MAX_AGE` 0, the preview flag unset; its settings file lives outside the repository, like 8772's | the only place where performance PASS is measured; switched only by the Performance Lead, under the lock |
| 8783–8789 | the family lanes' dev servers, one per worktree, each on its own database clone (`ile_v5_l3` … `ile_v5_l9`) and its own test database | each lane runs its own headless browser — never Chrome 9222 / 9223 |
| 8770 / 8771 / 8772 | main = the V4 control | untouched |

- **Database clones** are made by W1-0 (`CREATE DATABASE … TEMPLATE ile_v5` needs zero connections to the source, so it
  runs before 8780 starts, or by `pg_dump` / `pg_restore`). Lanes never write `ile_v5`.
- **Authenticated captures in lanes** use a session minted with Django's `Client.force_login` against the lane's own clone,
  by a scratch script outside the repository: no password is used, typed or stored. 8780's persona switch is for the
  owner.
- **The lock.** Every benchmark run waits while `C:/tmp/ile_locks/PERFORMANCE_BENCHMARK_LOCK` exists, and holds the lock
  while it runs.
- **Cross-engine.** Playwright WebKit and Firefox run in W2-A's gate and in W4-C, if the binaries are present. There is no
  Safari and no real device locally; every report says so.

### 2.9 The integration milestone (main)

**Entry conditions:**
- Wave 4 has passed.
- The whole-product council scores ≥ 4 on every scale, by §3.1's rule (the lowest chair).
- `dist/main.css` ≤ 36 KB gzip; the deletion map is complete.
- B2 is done, or explicitly accepted as pending for `/ar/`.
- The Apple fallback metrics are computed.
- The HTTP/2 measurement is done, or its absence is stated.
- The interim-phase variant is built, if the go-live phase needs it.
- The owner has seen the result on 8780.

**Then:** main is tagged `v4-control-final`, and the owner takes the D1 decision. Nothing deploys, either way: production
stays untouched.

---

## 3. FAMILY ORDER AND WAVES — what the orchestrator launches

Each wave below is a numbered list of workflows. A workflow runs one family (two for W2-C, split in time) through the loop
of §5.1 in its own worktree and lane; «Owns» is its slice of the ownership manifest (§2.2); «Gate» adds the family's own
items to the universal gate of §3.1; «Council» lists the chairs, the lead first; «Suites» points to §2.7's row. A
workflow ends when the steward has merged it and tagged `v54/<family>`, or when the CD has decided REDO.

### 3.1 The gate every family passes (V54 l.10, l.28)

A family is shown, merged or propagated only when all of this holds (RTD-B1, M1, M8, M9, M10). W1-0, W1-K and W1-P are
tooling and carry no design scores; their gates are their own.

**1. The scale** (Hd §8.3): 1 fails · 2 weak · 3 competent, below the bar · **4 at the owner's bar** — «credible alongside
excellent international digital products» (V5.1 §96) · 5 above it.

**2. One instrument per scale,** answered on named stills, with the files attached:

| Scale | Instrument | Scored by (two chairs at least) |
|---|---|---|
| Visual | TS §21.2 Q3 (is the spacing intentional?) and Q4 (does the composition create hierarchy?), on the standard capture set | design, taste |
| Premium | TS §21.1 Q1–Q8, with no «No» | design, taste, the family's director |
| Originality | TS §21.1 Q2 and the swap test (TS §2.3, §19.3 B) on every still, naming the signature that carries it | taste, design |
| UX | the family's acceptance list; on console pages LA-9's five answers in the first viewport at 1440, 1366 × 768 and 390; on public pages RH-6's chain of questions | UX, design |
| Mobile | the phone set (360 × 800, 375 × 667, 390 × 844, 412 × 915, 844 × 390) — emulated, and said so | UX, accessibility |
| Coherence | TS §21.1 Q3, measured: off-token radii 0; ≤ 3 distinct radii per screen (§1.3); gaps on the scale ≥ 95 % public and ≥ 90 % console; ≤ 4 shadow values a viewport and SH-8's caps; one sprite | design, the family's director |

«The family's director» is the Typography, Iconography, Image Art or Motion Director, or the Product Architect, where
the family's council lists one; where it lists none, the two other chairs suffice.

**3. The pass rule.** On every scale, the **lowest** score among the chairs who score it is ≥ 4 — never a mean. The CD may
refuse a pass and never grants one over a score below 4. A disputed score is re-measured by a fresh chair (one re-score per
scale per round), whose score replaces it. «PASSES WITH CONDITIONS» only when every scale is ≥ 4 and every condition is a
minor finding. At most three council rounds; a fourth means the CD changes the direction internally.

**4. Taste** (TS §19, §21.2, §21.3 item 4), by a chair who built none of it:
- 0 F on the **eighteen** symptoms of TS §19.2, and portrait A answered «no»;
- ≤ 1 P\* — a failed portrait B (swap) or C (brochure) counts as a P\* (TS §19.1 items 3–4);
- the swap test passing on every still, with its carrying signature named;
- the brochure test at ≤ 2 of 11 (TS §21.1 Q5);
- the taste review (TS §21.2) with no «No» on Q1, Q4, Q9 and Q10, and at most two «Partly»;
- **for flagships** — W1-D, W2-A, W2-B, W2-C1 + W2-C2, W2-D + W2-E, W3-A, W3-B, W3-C, W3-D — a **blind ranking** by three
  reviewers who built none of it: the V5 surface, V4 on the same URL (from the W1-0 «before» set) and two of the family's
  named references, at 1440 and 390. It passes when all three rank V5 above V4, and at least two rank it above at least
  one reference, at both sizes (HEB §7, T1).

**5. References.** Each family names three real products in its brief and shows side-by-side captures at 1440 and 390 —
from `P/research/benchmarks/` where they exist, otherwise captured headless by the family (public pages only, never signed
in, nothing typed). A family may add a reference, not replace one:

| Family | References |
|---|---|
| W1-A type · colour · corners | GOV.UK · Collège de France · Mercury |
| W1-B icons | IBM · GOV.UK · Linear |
| W1-C components | GOV.UK (the task list) · IBM · Linear |
| W1-D motion and loader | Linear · Vercel · Stripe |
| W2-A overlays | Linear · Vercel · IBM |
| W2-B login | e-Residency · Mercury · Wise |
| W2-C navbar | agamieuromed.org (the owner's reference) · European Commission · Rijksmuseum |
| W2-D / W2-E home | Collège de France · e-Residency · Rijksmuseum |
| W3-A … W3-E platform | GOV.UK (task list, step by step) · Mercury · Linear |
| W3-F public interior | service-public.fr (fiche F2728) · GOV.UK (the visa guide) · OECD |

**6. Foundation families** (W1-A, W1-B, W1-C, W1-D) are scored on their **specimen boards** — the type specimen, the colour
register board, the corner and shadow board, the icon sheet, the chip board, the button and field set, the loader
filmstrips — rendered by the dev-only specimen route. Because their propagation is global by construction, they also pass
**«no page worse than before»** (blocking): every page type of the W1-0 set, fr and ar, at 1440 and 390, before and after.
Automated: overflow, clipped text, contrast failures, CLS, overlapping targets and missing focus rings must not increase.
By eye: the design chair marks each pair better / same / worse; one «worse» blocks the merge until it is fixed, in the
aliases.

**7. Platform families** (W3-A … W3-E). Each brief names, screen by screen, the identity carriers that make the screen ILE's
at rest — «La soglia» (the rails), «I cerchi · Il registro» (states), the L2 key in waits, the door in its one empty state,
«il lume» in the rail, the ledger references in ILE Mono. On every console screen type the gate runs the swap test, the
symptom-10 silhouette check by eye on stills, and TS §21.1 Q1 «Does this feel expensive?». A screen type with no named
carrier, or one that fails the swap test, does not pass.

**8. Accessibility PASS:** a keyboard walk in fr and ar; axe clean; contrast; forced colours; reduced motion through
`emulateMedia` (§1.5); 400 % reflow; 1.4.12 text spacing; targets (SP-8); focus never obscured.

**9. Performance PASS,** with the §2.6 budgets measured on 8782 and the protocol stated.

**10. Motion evidence:** filmstrips at 1× and 0.25× and frame-difference series for every motion the family adds; for
flagships, local 1× and 0.25× recordings for the report (§6).

**11. Health:** 0 CSP violations, 0 console errors; 0 horizontal overflow from 320 to 1920 px.

**12. Tests and ownership:** the family's row of §2.7 green, browser tests at 0 skips; its DS 2026 prose sections updated;
its diff inside its slice of the manifest.

**The standard capture set:** 1920 × 1080, 1440 × 900, 1366 × 768, 1280 × 800, 1024 × 768, 412 × 915, 390 × 844,
360 × 800; 375 × 667 and 844 × 390 for the flagships; fr and ar, with it / en spot checks on the home and the login;
reduced motion and forced colours on each flagship screen.

### 3.2 The dependency graph

```
W1-0 infra ──► every measurement, every lane, the manifest, v5-live
W1-0 ──► W1-K calibration ──► the first family gate (W1-A's)
W1-0 ──► W1-P preview ──► the owner's live view
W1-0 ──► W1-A tokens · type · colour · corners · fonts ──┬──► W1-B icons ──┐
                                                          └──► W1-D motion + loader
                                         W1-A + W1-B ──► W1-C core components
W1-C + W1-D ──► W2-A overlays ──► W2-C2 (sheet, targa popover, panel on overlay.js) · W3-A · W3-C (preview drawer)
W1-C + W1-D ──► W2-B login (creates _door.css)
W1-C ──► W2-C1 navbar (bar and panels)
hero-final decision + W1-C + W1-D + W2-B merged ──► W2-D hero port ──► W2-E home chapters + the A-bis test
W2-C2 ──► W3-F2 content · W2-C2 + W2-E ──► W3-F1 doors
W2-A ──► W3-A shell ──► W3-B dashboard ──┬──► W3-C documents ──┐
                                         └──► W3-D journey ─────┴──► W3-E case file + secondary
W3-F1 merged ──► W3-D's merge (the passage's imports in their page sheets)
Wave 3 ──► W4-A ──► W4-B ──► W4-C ──► W4-D (which also waits for W2-D + W2-E) ──► the D1 question
```

**Order inside the waves:**
- **Wave 1:** W1-0 → (W1-K ∥ W1-P ∥ W1-A) → (W1-B ∥ W1-D) → W1-C. No family gate before W1-K has passed.
- **Wave 2:** W2-A ∥ W2-B ∥ W2-C1 ∥ W2-D (when the hero passes; it merges after W2-B) → W2-C2 after W2-A and W2-C1 merge
  → W2-E after W2-D.
- **Wave 3:** W3-F2 and W3-A at once, W3-F1 once W2-E has merged; W3-A → W3-B → (W3-C ∥ W3-D) → W3-E; W3-D merges
  after W3-F1.
- **Wave 4:** sequential.

### 3.3 Wave 1 — the foundation, and the preview as the live product

**Launch:** this plan. **Reports to the owner in Wave 1: none.** The first report is the first flagship that passes on a V5
page (§6), and it carries Wave 1 in one line.

**1. `v54-w1-0` — W1-0 · Infra, baseline, live preview** (the orchestrator and the steward; first; S)
- **Does:**
  1. design-v5: replaces the `node_modules` junction with its own `npm ci`; adds the two `merge=binary` lines to
     `.gitattributes`; cherry-picks `31048b6`; moves the QA password literal of `scripts/qa_prepare_env.py` to an
     environment variable (the hygiene task); creates DL54 with the entries of §8.3; tags `v54/base`.
  2. v5-live: `git worktree add --detach C:/tmp/ile_wt/v5-live v54/base`, `.env` copied; the orchestrator restarts 8780
     from it.
  3. Databases, while the orchestrator has 8780 stopped for its move to v5-live (a template clone needs zero connections
     to `ile_v5`): `ile_v5_perf`, the lane clones `ile_v5_l3` … `ile_v5_l9`, and one test database per lane; the four
     QA personas counted on `ile_v5` (no credential involved).
  4. 8782: its settings file outside the repository (§2.8).
  5. Lanes: ports, worktrees (with the junction to design-v5's `node_modules`), test databases.
  6. `docs/design-v5/OWNERSHIP_V54.json` from §3's «Owns» lists; `scripts/check_ownership.py`;
     `scripts/regen_design_inventory.py`.
  7. The specimen route `/__design-v5/specimens/<board>/` in `apps/designpreview` (it renders
     `templates/dev/designpreview/specimens/<board>.html`; 404 when absent).
  8. **The «before» set** on 8782 at `v54/base`: every page type captured (the standard set, fr and ar) and traced (LCP,
     CLS, INP, the first-render task; n ≥ 9); CSS bytes and requests counted per page type. Authenticated pages with
     minted sessions on `ile_v5_perf`. It is the baseline of §2.6 and of «no page worse than before».
- **Owns:** `.gitattributes`; `scripts/qa_prepare_env.py` (the literal only); `docs/design-v5/DECISION_LOG_V54.md`;
  `docs/design-v5/OWNERSHIP_V54.json`; `scripts/{check_ownership,regen_design_inventory}.py`;
  `apps/designpreview/{urls,views}.py` (the specimen route only); the `templates/dev/designpreview/specimens/` folder.
- **Gate:** verified by the steward — the suite green at `v54/base`; 8780 serving v5-live; the before-set complete; the
  manifest parses and covers every file §3 assigns. No council: there is no design in it.

**2. `v54-w1-k` — W1-K · Council calibration** (after W1-0; parallel with W1-P and W1-A; read-only; S)
- **Does:** the chairs of §3.1's table score, blind, three surfaces the owner has already judged — the V4 person dashboard
  (design-v5 at `v54/base` on a lane server, with a minted session; the owner: ≈ 3 / 5, V54 l.20), the gate-0 login comp
  (`P/login/`; the owner: «concept good, left side too static, form too simple», V54 l.18), and H-E as built
  (`P/research/hero/he-archive-v53/`; the 4 October chairs: 3.5–3.75).
- **Gate:** every chair lands each of the three below 4 on visual, premium and originality. A chair that does not writes
  what it missed against the anchors and re-scores; a chair off twice is replaced by a fresh chair, calibrated the same way.
  Only calibrated chairs score a gate.
- **Outputs:** `W/docs/design-v5/QA/v54/w1-k/` (scores, the chairs' notes); stills in E/w1-k/.

**3. `v54-w1-p` — W1-P · Preview as the live product** (after W1-0; M)
- **Owns:** `apps/designpreview/**` (the landing and strip, the index, the archive move, the persona switch, the preview
  middleware), `templates/dev/designpreview/**` except `specimens/`, `static/css/dev/designpreview.css`,
  `static/js/dev/designpreview.js`, the preview block of `config/settings/dev.py`, `tests/frontend/test_design_preview.py`,
  the persona line of `tests/security/test_log_privacy.py`.
- **Pages:** `/__design-v5/` (the live home under the strip), `/__design-v5/index/`, `/__design-v5/research/…`, the persona
  endpoints.
- **Gate:** §4.6.
- **Council:** UX (lead), a security reviewer (the persona switch and the frames), accessibility, performance (the database
  ceiling, the frame cap), CD.
- **Suites:** W1-P. **Propagation:** none.

**4. `v54-w1-a` — W1-A · Foundation: tokens, type, colour, corners, spacing and shadow rules** (after W1-0; L)
- **Owns:** `static/css/main.css`; `static/css/v5/{fonts,tokens,aliases,base}.css`; `static/fonts/v5-*` and
  `static/fonts/licenses/**`; the removal of `static/css/fonts.css` and the V4 woff2; W1-A's rows of the deletion map;
  `templates/base.html` (head and preloads); `scripts/build_css.mjs` (the `_` rule);
  `templates/dev/designpreview/specimens/{type,colour,corners}.html`; tests — `test_v5_tokens.py` (new),
  `test_v4_tokens.py` (retargeted or retired), `test_static_assets.py:133–171`, `test_legacy_token_shim.py`,
  `test_design_showcase.py`, `test_css_tokens_exist.py`, `test_css_bundle_is_current.py`, `test_rtl_static.py`,
  `test_browser.py:211–220`, the fonts slices of `test_layout.py` and `test_rtl_browser.py`, the fonts, cascade and focus
  functions of `test_design_docs.py`; DS 2026 §2 (prose), §5–§8, §12, §17; `docs/design-v5/FONTS_V5.md`.
- **Pages:** all of them, re-valued at once.
- **Gate:** scored on the type specimen, the colour register board and the corner and shadow board; no page worse than
  before; contrast verified on ≥ 400 pairs, 0 below their minimum, C3 / C4 / C5 / C7 included, and C8's check (Istituzione
  reads as a hue on night beside the other three); swap CLS ≤ 0.01; the font budgets; the Wave-1 CSS allowance (§2.6); the
  three-screen corner comparison with its radii count.
- **Council:** the Typography Director (lead), design, taste, accessibility, performance, CD.
- **Suites:** W1-A. **Propagation:** global, by construction.

**5. `v54-w1-b` — W1-B · Icon system** (after W1-A; parallel with W1-D; M)
- **Owns:** `static/icons/src/**`, `scripts/build_icons.py`, `static/img/icons.svg`, `apps/core/icons.py`, the `svg_icon`
  tag, `docs/design-v5/ICON_LICENSES.md`, `components.css` §2, `templates/dev/designpreview/specimens/icons.html`; the
  `svg_icon` call sites in templates, for the re-mapping only (not `portal_chrome.html`: the rail is W3-A's); tests —
  `test_icons.py` (new), `test_static_assets.py:177–277`, `test_svg_wellformed.py`, `test_page_integrity.py:59`, the mirrors
  slice of `test_rtl_browser.py`.
- **Pages:** every page with a glyph.
- **Gate:** 111 symbols; the sprite ≤ 32 KB raw; every `svg_icon` call resolves; `MIN_SIZE` and `TWINS` enforced; the
  semantic sheet at 1× and 2×, fr and ar; the flip list verified in RTL; **the ILE sprite beside raw Lucide at 1× and 2×
  reads as one ILE hand** (before the merge); no page worse than before.
- **Council:** the Iconography Director (lead), design, taste, accessibility, CD.
- **Suites:** W1-B. **Propagation:** every glyph site; the rail's re-mapping is W3-A's.

**6. `v54-w1-d` — W1-D · Motion and the loader «Lume»** (after W1-A; parallel with W1-B; M; flagship)
- **Owns:** `static/js/src/{motion,loader}.js`; `static/js/head.js` (the input-modality flag); `static/css/v5/loader.css`,
  `static/css/v5/_loader-light.css`, `scripts/gen_loader_light.py`; `templates/components/{loader,busy_key}.html`;
  `apps/accounts/signals.py` (the release flag); the release hook in `templates/partials/portal_chrome.html` and the
  `_loader-light.css` import line in `apps/portal/static/portal/console.css` (Wave 1 only);
  `initMisc`'s submit guard in `static/js/main.js`; `components.css`'s universal reduced-motion block; A11Y §7; the one-line
  pointer in BA §1; `templates/dev/designpreview/specimens/loader.html`; tests — `test_loader_rules.py`,
  `test_rm_flag_parity.py`, `test_script_motion_gate.py`, `test_v4_tokens.py:231` (retired), the reduced-motion function of
  `test_design_docs.py`.
- **Pages:** the first console page after sign-in (the release); every form submit (L2); the existing fragment containers
  (L3). The login's engage is wired by W2-B on W1-D's primitive.
- **Gate:** §1.9's acceptance and its three measured conditions; the reduced-motion still; forced colours; 390 px; 200 %
  zoom; the blind ranking (flagship).
- **Council:** the Motion Director (lead), design, taste, accessibility, performance, CD.
- **Suites:** W1-D. **Propagation:** L2 to every busy button; the release to its one seat; L3 to the fragment containers
  (later families attach it to theirs).

**7. `v54-w1-c` — W1-C · Core components** (after W1-A and W1-B; L)
- **Owns:** `static/css/v5/{buttons,field,chip,card,notice,tabs}.css`; the component templates — `form_field` (Wave 1), the
  chip partial, `badge`, `notice`, `tabs`, the buttons; `apps/core/chips.py` (eight registers; `badge` kinds → registers);
  the O14 lint (CSS, HTML, JS); `initTabs` and `initAccordions` in `static/js/main.js`; W1-C's rows of the deletion map;
  `templates/dev/designpreview/specimens/{chips,buttons,fields}.html`; tests — `test_chips_registry.py`,
  `test_state_chips_carry_a_register.py`, the lint test, the form slice of `test_layout.py`.
- **Pages:** every page that uses these components.
- **Gate:** the chip board (8 registers + nullo, on paper / white / night, fr / ar, at 20 / 24 / 28 px); the button set
  (every state, the press, the busy face; primaries flat); fields at 16 px with a hairline only; cards by purpose — no
  stat-card on person or company screens; focus on every ground; all 65 chip sites re-probed; no page worse than before.
- **Council:** design (lead), taste, UX, motion, accessibility, performance, CD.
- **Suites:** W1-C. **Propagation:** every template that uses them.

### 3.4 Wave 2 — the flagships

**Launch:** Wave 1 merged; the steward cherry-picks main's code commits and tags `v54/wave-2`.

**1. `v54-w2-a` — W2-A · The overlay system** (M; flagship)
- **Owns:** `static/js/src/overlay.js`, `static/css/v5/overlays.css`;
  `templates/components/{dialog,drawer,popover,tooltip,sheet}.html`;
  `templates/components/account_menu.html` → the account popover; for this wave only, the drawer element in
  `templates/partials/portal_chrome.html`, the row menu in `templates/components/document_row.html` and the drawer code in
  `static/js/src/console.js`; `initDialogs` and `initDropdowns` in `static/js/main.js`; W2-A's rows of the deletion map;
  tests — `test_overlays.py`, the account-menu slice of `test_layout.py`, `test_rtl_browser_overlays.py`, browser tests for
  Esc, Back, focus return and the trap.
- **Publishes first:** the primitive contract (scrim, dismissal, focus, motion tokens), one page in its QA folder, which
  W2-C1 reads.
- **Pages:** the console drawer, the account menu and the row menu on every console page (`console.js` imports
  `overlay.js`). The public account popover is wired by W2-C2, which adds `overlay.js` to `shell.js`.
- **Gate:** O1–O11 (§1.14); the INP rule; the WebKit + Firefox smoke; the blind ranking.
- **Council:** accessibility (lead), motion, UX, performance (INP), design, taste, the 21st curator, CD.
- **Suites:** W2-A. **Propagation** (§1.14): the console drawer → popovers and menus → modal and alertdialog → the tooltip
  group. The preview drawer and the filter sheet are wired by W3-C; the phone sheet and the targa popover by W2-C2.

**2. `v54-w2-b` — W2-B · The login «Il varco» and the entrance pages** (M; flagship)
- **Owns:** `templates/allauth/layouts/entrance.html`; `templates/account/login.html` (new),
  `templates/account/password_reset_help_text.html` (new), `templates/429.html` (new); the reset slot in
  `templates/components/form_field.html`; the `LoginForm` subclass in `apps/accounts/forms.py` + `ACCOUNT_FORMS` in
  `config/settings/base.py`; `apps/accounts/static/accounts/entrance.css`; `static/css/v5/_door.css` (created here: the door
  stage as drawn, tokenised) and its token block in `v5/tokens.css`; `static/js/src/entrance.js` (the stage's states, the
  arrival sentence, the engage); `components.css` §27's entrance rules; tests — the entrance slice of `test_layout.py`, a
  new 429 test, the allauth flows, `test_rtl_browser_entrance.py`.
- **Pages:** `/{fr,ar,it,en}/compte/login/`, signup, password reset, verification, MFA.
- **Gate:** L1–L14 as amended (§1.13); the blind ranking.
- **Council:** design (lead), taste, UX, motion, accessibility, performance, a security reviewer, CD.
- **Suites:** W2-B. **Propagation:** every page on `entrance.html`.

**3. `v54-w2-c1` — W2-C1 · The navbar «Il portico»: the bar and the panels** (L; flagship with W2-C2)
- **Owns:** `templates/partials/{utility_bar,header,main_nav,footer}.html`, `templates/components/language_segmented.html`;
  `apps/cms/templatetags/cms_nav.py` (the door cards' task links as fallback children; the D-U3 IA);
  `static/css/v5/chrome.css`; `static/js/src/nav.js`, `static/js/src/shell.js`; `initNavigation` in `static/js/main.js`
  (moved into `nav.js`); the `chrome` block of `templates/base.html`; `static/js/src/focus-clear.js` only if §1.6's
  measurement fails; W2-C's rows of the deletion map; DS 2026 §7.2 / §11 and A11Y §3; `docs/qa/design/capture.py` (the
  drawer selectors and figures); tests — `test_browser.py`, `test_cms_nav.py`, `test_header_fits_the_narrowest_viewport.py`,
  the header slice of `test_layout.py`, `test_rtl_browser_nav.py`, `test_design_docs.py:796, 996, 1190–1226`; the 56
  behaviour checks of NV §9.3 (22 on the keyboard) ported.
- **Pages:** every public page, allauth's public pages included.
- **Gate:** N1–N19 as amended (§1.12), less N8 / N9's sheet and N13's signed-in popover (W2-C2); the `ile_v5` `MenuItem`
  «main» rows checked (data, not a migration); 2.4.11 measured with the CSS-native scroll padding.
- **Council:** design (lead), taste, UX, motion, accessibility, performance, the Image Art Director, CD.
- **Suites:** W2-C1. **Propagation:** every public page at once (the chrome is one partial).

**4. `v54-w2-d` — W2-D · The hero's port** (on the hero-final decision; merges after W2-B; M; flagship with W2-E)
- **Owns:** `templates/pages/home/_hero.html`, `templates/pages/home.html`, `apps/pages/static/pages/css/hero.css` (new),
  `static/js/src/home.js`, `static/js/src/hero.js` (new), `apps/pages/static/pages/js/home.js` (moved, then deleted), the
  hero's token block in `v5/tokens.css`, `static/brand/v5/**`, the hero's four images in `static/img/photos/` and their
  provenance, the deletion of `v4/hero.css`, `apps/pages/tests/test_home.py` and the doorway tests.
- **Pages:** `/fr/`, `/ar/`, `/it/`, `/en/`.
- **Gate:** §1.17's step 0, the re-hold and the parity check; hero CLS ≤ 0.05; the universal gate.
- **Council:** the hero council's design, accessibility and performance chairs; **taste as a full chair**; motion; CD.
- **Suites:** W2-D / W2-E. **Propagation:** the home only.

**5. `v54-w2-c2` — W2-C2 · The navbar: the phone sheet, the targa popover, the panel on `overlay.js`** (after W2-A and
W2-C1 have merged; M)
- **Owns:** the sheet in `templates/partials/main_nav.html` and its parts of `chrome.css` and `nav.js`; the signed-in
  targa's account popover in `templates/partials/header.html`; the `overlay.js` import in `static/js/src/shell.js`; the
  panel's switch from the local adapter to `overlay.js`; the drawer's last legacy rules.
- **Pages:** every public page below 80 rem; the signed-in header.
- **Gate:** N8 / N9 (the sheet's cold-open INP p90 ≤ 200 ms on the phase-3 home, fr + ar), N13, N14; O2–O8 for the sheet;
  the panel's dismissal and focus through `overlay.js`; the blind ranking for the navbar as a whole (W2-C1 + W2-C2).
- **Council:** accessibility (lead), design, taste, UX, motion, performance, CD.
- **Suites:** W2-C1 / W2-C2. **Propagation:** every public page.

**6. `v54-w2-e` — W2-E · The home chapters under the hero, and the A-bis test** (after W2-D; M; flagship with W2-D)
- **Owns:** every `templates/pages/home/_*.html` partial except `_hero.html`, and `templates/pages/home/partials/**`;
  the home's part of `apps/pages/static/pages/css/pages.css`; the order in
  `pages.services.home_sections()` (no copy change); the French-typography filter (team-authored strings only); W2-E's rows
  of the deletion map; the A-bis lane state (two tokens and the display cut, merged only if A-bis wins).
- **Pages:** the home, in four languages.
- **Gate:** RH-4: 3–8 screens at 1440, ≤ 9.5 at 390; RH-5's «once» count = 0 · 0; RH-6's chain of questions; D24's items;
  the image-contexts test; **the A-bis blind test** (§1.1), its result recorded in DL54; the blind ranking for the home as
  a whole (W2-D + W2-E).
- **Council:** design (lead), taste, UX, the Image Art Director, motion, accessibility, performance, the Typography Director
  (the test), CD.
- **Suites:** W2-D / W2-E. **Propagation:** the home.

**Reports to the owner** (§6): W2-B with W1-D (the login shows the loader whole); W2-C1 + W2-C2 with W2-A (the sheet and the
account popover on V5 pages); W2-D + W2-E together. The first of these carries Wave 1 in one line.

### 3.5 Wave 3 — the platform families and the public interior

**Launch:** W2-A, W2-B, W2-C1 and W2-C2 merged — Wave 3 does not wait for the hero: W2-D and W2-E may still be in their
loop; cherry-picks; tag `v54/wave-3`. W3-F2 and W3-A start at once; W3-F1 starts when W2-E has merged.

**1. `v54-w3-f1` — W3-F1 · The doors, the project pages and orientation** (after W2-E; L)
- **Owns:** `templates/pages/**` except `home.html` and `home/**`; `templates/ecosystem/**`, `templates/orientation/**`,
  `templates/pathways/**`; `templates/forum/{index,register,register_done}.html` and the `forum/partials/**` they use; the
  interior part of `apps/pages/static/pages/css/pages.css`; `apps/ecosystem/static/ecosystem/ecosystem.css`; the public part
  of `apps/forum/static/forum/forum.css`; `apps/orientation/static/orientation/{wizard.css,wizard.js}` (retiring
  `v4/wizard.css`); W3-F1's rows of the deletion map.
- **Pages:** the doors `/fr/parcours/`, `/fr/entreprises/`, `/fr/institutions/`, `/fr/universites-et-formation/`,
  `/fr/forum/`, `/fr/le-projet/`, `/fr/projet-pilote/`; `/fr/orientation/`, `/fr/diplomes-et-titres/`, `/fr/formation/`,
  `/fr/attention-aux-fraudes/` — each with its ar twin.
- **Gate:** D26's layout slots with verbatim headings (§1.18); RH-1 … RH-8, RH-3 (a picture every second screen) on the
  door pages; forms at 16 px; the type system as W2-E's test left it.
- **Council:** design (lead), taste, UX, the Image Art Director, accessibility, performance, CD.
- **Suites:** W3-F1 / W3-F2. **Propagation:** every page it owns.

**2. `v54-w3-f2` — W3-F2 · Content, legal, error and account pages** (parallel from the start; L)
- **Owns:** `templates/{faq,glossary,partners,news,living,community,enquiries,legal,errors,consents,accounts}/**`;
  `templates/allauth/layouts/{base,manage}.html` and the elements of the manage pages; W3-F2's rows of the deletion map.
- **Pages:** `/fr/faq/`, `/fr/glossaire/`, `/fr/partenaires/`, `/fr/actualites/`, `/fr/vivre-en-italie/`,
  `/fr/forum-virtuel/`, `/fr/contact/`, `/fr/privacy-policy/`, the 400 / 403 / 404 / 410 / 429 / 500 errors, the profile and
  account-management pages, the newsletter consent pages — each with its ar twin.
- **Gate:** D26's slots; RH-1 … RH-8; forms at 16 px; the errors in four languages, 429 included.
- **Council:** design (lead), taste, UX, accessibility, performance, CD.
- **Suites:** W3-F1 / W3-F2. **Propagation:** every page it owns.

**3. `v54-w3-a` — W3-A · Console shell and navigation** (first of the console chain; L; flagship)
- **Owns:** `templates/partials/portal_chrome.html`, `templates/portal/base_portal.html`; in `apps/portal/services.py`
  `shell_navigation`, `NAV_GLYPHS` → the registry, the `NAV_BOTTOM` cap; `apps/portal/static/portal/console.css` (which
  imports `_loader-light.css` and the console partials), `v5/_shell.css`, `v5/_notifications.css`;
  `static/js/src/console.js`, `static/js/rail-pref.js`; the console's use of the account popover; the rail's icon
  re-mapping; the T5 test;
  `test_console_shell_stylesheets.py`.
- **Pages:** the 51 console templates (the shell), and the staff pages' chrome.
- **Gate:** ≤ 4 bottom entries for every QA role; the same rail keys on every URL of a space; the rail's foot visible at
  1366 × 657; three keys to reach «Menu»; phone chrome ≤ 120 px; 0 animations at load except the entrance release; the
  notification centre as a popover (a sheet on phones), its content an asynchronous fragment with L3; §3.1 item 7; the
  blind ranking.
- **Council:** the Product Architect (lead), UX, design, taste, motion, accessibility, performance, CD.
- **Suites:** W3-A … W3-E. **Propagation:** every console page.

**4. `v54-w3-b` — W3-B · Dashboard and cards** (after W3-A; M; flagship)
- **Owns:** `templates/portal/dashboard.html`, `templates/companies/dashboard.html`; the dashboard presenters in
  `apps/portal/services.py`, F9 included (stop building the hidden grid for persons); T1, the unified `next_action`, in
  `apps/cases/services.py` (a presenter change only); `apps/portal/static/portal/v5/_dashboard.css`; the bridge part of
  `portal.css`; the dashboard part of `companies.css`; W3-B's rows of the deletion map.
- **Pages:** the person dashboard (three personas), the company dashboard, the institution / university bridge.
- **Gate:** one primary in the first viewport, with its piece and its date; no requirement id drawn twice; DOM order h1 →
  NowPanel → journey; ≤ 1 raised panel and ≤ 2 shadow values per screen; no stat-card on person or company screens; the
  four NowPanel variants composed; §3.1 item 7; the blind ranking; the value matrix for the report (§1.15).
- **Council:** the Product Architect (lead), UX, design, taste, accessibility, performance, CD.
- **Suites:** W3-A … W3-E. **Propagation:** every dashboard.

**5. `v54-w3-c` — W3-C · Document workspace and status** (after W3-B; parallel with W3-D; L; flagship)
- **Owns:** `templates/documents/{index,upload,requirement_detail,terms_required}.html`,
  `templates/documents/partials/register.html`, `templates/portal/documents.html`, `templates/components/document_row.html`;
  `apps/documents/presenters.py` (F8); the Dépôt's JSON answers in `apps/documents/views.py` if needed (IP S7);
  `apps/documents/static/documents/*.css`; the deadline kinds in `apps/portal/services.py` (F13);
  `apps/portal/static/portal/v5/{_workspace,_depot,_table}.css`; the preview drawer and the filter sheet on `overlay.js`;
  W3-C's rows of the deletion map.
- **Pages:** `/documents/`, `/fr/espace-reserve/mes-documents/`, upload, requirement detail, `terms_required`, the deadline
  registers.
- **Gate:** the first card's title at ≤ 700 px at 390 × 844; the first object in the first viewport at 390 and 360; ledger
  counts = group counts (a test); entries follow `STATE_ORDER`; a filed piece due tomorrow reads calm (a test); no
  `badge--*` left on console pages; edges and hatch ≥ 3 : 1; a colour-vision check; the whole row as the target (0 dead probe
  points); the Dépôt's 11 answers composed; the register at 6 / 5 columns, then cards, by its own width; the preview
  drawer's history (`?état=` kept, `replaceState` on swaps); L3 on the drawer's fragment; §3.1 item 7; the blind
  ranking.
- **Council:** the Product Architect (lead), UX, design, taste, motion, accessibility, performance, CD.
- **Suites:** W3-A … W3-E. **Propagation:** every document surface, and every status chip site.

**6. `v54-w3-d` — W3-D · The journey «La soglia»** (after W3-B; parallel with W3-C; merges after W3-F1; M; flagship)
- **Owns:** `templates/components/{journey_rail,case_timeline,stepper,wizard_stepper}.html`;
  `static/css/v5/_journey-passage.css` and its import lines in the page sheets of the pages that draw the passage (after
  W3-F1's merge); `apps/portal/static/portal/v5/_journey-rail.css`; `static/js/src/journey-rail.js`; the `SELECTION`
  mapping in `journey_for` (`apps/cases/services.py`); W3-D's rows of the deletion map.
- **Pages:** the dashboard's rail, «Ma situation», «Mon parcours», the case file's rails, and the public passage (the home
  and the door pages, wherever it stays).
- **Gate:** one passage and one rail drawing, never a third; the phone journey as a card + a disclosure; still at load; the
  numeral / glyph / holder rule; `SELECTION` on threshold A; no task above 12 ms; §3.1 item 7; the blind ranking.
- **Council:** design (lead), motion, UX, taste, accessibility, performance, CD.
- **Suites:** W3-A … W3-E. **Propagation:** every journey site.

**7. `v54-w3-e` — W3-E · The case file and the secondary pages** (after W3-C and W3-D; L)
- **Owns:** `templates/cases/**`;
  `templates/portal/{situation,deadlines,messages,message_detail,requests,request_detail,pathways,unavailable}.html`;
  `templates/components/page_header.html`; `templates/components/badge.html` (retired on console pages);
  `templates/companies/**` except the dashboard; `templates/{selection,academy,helpdesk}/**`;
  `templates/forum/governance/**`;
  `templates/notifications/email/**` (no visual change in V5.4: checked for removed class names only); the portal list
  partials; `apps/{academy,helpdesk,selection}/static/**/*.css`; `companies.css` except the dashboard part; the governance
  part of `forum.css`; W3-E's rows of the deletion map, including the last of `v4/workspace.css`.
- **Pages:** the authenticated list of `product.md` §12 — the case `EE167596D4`, requests, messages, deadlines, the
  guichet, formation, the company pages; the staff pages' chrome only.
- **Gate:** `platform.md` §3's items; the C-3 checklist as register rows; staff consequence dialogs on the modal; the
  identity carriers of the screens with neither rail nor register (messages, the guichet, help pages) named and
  swap-tested (§3.1 item 7).
- **Council:** the Product Architect (lead), UX, design, taste, accessibility, performance, CD.
- **Suites:** W3-A … W3-E. **Propagation:** every secondary console page. Deep staff and back-office work is recorded as
  design debt.

**Reports to the owner:** one per passed flagship (W3-A, W3-B, W3-C, W3-D); one at the end of the wave for W3-E, W3-F1 and
W3-F2.

### 3.6 Wave 4 — cross-cutting work and integration readiness

**Launch:** Wave 3 merged; tag `v54/wave-4`. The four workflows run in sequence. They own no files of their own: each fix
lands in the owning family's files (the manifest names them), through the steward. The home joins the sweeps when W2-D +
W2-E have merged; W4-D does not close without them.

**1. `v54-w4-a` — W4-A · Mobile + RTL sweep**
- **Covers:** every page at 360 / 375 / 390 / 412 / 430 px, landscape and short heights, in fr and ar.
- **Checks:** phone chrome ≤ 120 px; the first object in the first viewport; targets (SP-8); the Arabic overflow probes;
  the mirrors, and the things that never mirror.
- **Council:** a mobile lead, an RTL lead, accessibility, CD.

**2. `v54-w4-b` — W4-B · Motion audit**
- **Method:** the improve-animations audit, run read-only over the whole product first, then its fixes.
- **Checks:** tier ceilings; one indicator per page; nothing at load in the console but the entrance release; a
  reduced-motion still everywhere; `[data-reveal]` reveals that hide text removed (K17) with `components.css` §29 and
  `initReveal`; the `motion` dependency removed by the steward once unused, with `test_frontend_bundle_is_current.py:45`
  rewritten in the same merge.
- **Council:** the Motion Director, performance, accessibility, CD.

**3. `v54-w4-c` — W4-C · Performance + accessibility consolidation, on 8782**
- **Checks:** every page type traced (LCP, CLS, INP, the first-render task) against §2.6 with its protocol; the HTTP/2
  measurement; axe and keyboard walks in fr and ar; forced colours; 400 % reflow; 1.4.12; Playwright WebKit and Firefox on
  every page type, where available.
- **Council:** the Performance Lead, the Accessibility Lead, CD.

**4. `v54-w4-d` — W4-D · Integration readiness**
- The interim-phase variant of the chrome and the hero, if the go-live phase needs it (the Product Architect checks the
  phase flags).
- The deletion map's last row: the remaining legacy layers removed → `dist/main.css` ≤ 36 KB gzip; dead code removed;
  DS 2026 final.
- The whole-product council (every lens, §3.1's rule) ≥ 4.
- The release notes for the owner; then the D1 question.

### 3.7 Summary

| # | Workflow | Family | Depends on | Size | Lead | Flagship |
|---|---|---|---|---|---|---|
| 1.1 | `v54-w1-0` | Infra, baseline, v5-live, 8782, manifest, DL54 | — | S | steward | — |
| 1.2 | `v54-w1-k` | Council calibration | W1-0 | S | CD | — |
| 1.3 | `v54-w1-p` | Preview as the live product | W1-0 | M | UX + security | — |
| 1.4 | `v54-w1-a` | Tokens · type · colour · corners · fonts | W1-0 (its gate after W1-K) | L | Typography Director | — |
| 1.5 | `v54-w1-b` | Icon system | W1-A | M | Iconography Director | — |
| 1.6 | `v54-w1-d` | Motion + the loader «Lume» | W1-A | M | Motion Director | yes |
| 1.7 | `v54-w1-c` | Core components | W1-A, W1-B | L | design | — |
| 2.1 | `v54-w2-a` | Overlay system | W1-C, W1-D | M | accessibility | yes |
| 2.2 | `v54-w2-b` | Login «Il varco» + entrance pages | W1-C, W1-D | M | design | yes |
| 2.3 | `v54-w2-c1` | Navbar: bar and panels | W1-C | L | design | yes (with 2.5) |
| 2.4 | `v54-w2-d` | Hero port | the hero-final decision; W1-C, W1-D; merges after W2-B | M | the hero council's chairs | yes (with 2.6) |
| 2.5 | `v54-w2-c2` | Navbar: sheet, targa popover, panel on `overlay.js` | W2-A, W2-C1 | M | accessibility | yes (with 2.3) |
| 2.6 | `v54-w2-e` | Home chapters + the A-bis test | W2-D | M | design | yes (with 2.4) |
| 3.1 | `v54-w3-f1` | Doors, project pages, orientation | W2-C2, W2-E | L | design | — |
| 3.2 | `v54-w3-f2` | Content, legal, errors, accounts | W2-C2 | L | design | — |
| 3.3 | `v54-w3-a` | Console shell + navigation | W2-A | L | Product Architect | yes |
| 3.4 | `v54-w3-b` | Dashboard + cards | W3-A | M | Product Architect | yes |
| 3.5 | `v54-w3-c` | Document workspace + status | W3-B | L | Product Architect | yes |
| 3.6 | `v54-w3-d` | Journey «La soglia» | W3-B; merges after W3-F1 | M | design + motion | yes |
| 3.7 | `v54-w3-e` | Case file + secondary pages | W3-C, W3-D | L | Product Architect | — |
| 4.1–4.4 | `v54-w4-a` … `d` | Mobile + RTL · motion · performance + a11y · readiness | Wave 3 (W4-D also W2-D, W2-E) | M each | the lane's lead + CD | — |

---

## 4. PREVIEW AS LIVE PRODUCT

### 4.1 What `/__design-v5/` opens — the current best V5

`/__design-v5/` lands on **the live V5 home** — the real `/fr/` page served by 8780, full window, in one same-origin frame —
under a slim dev-only strip (≤ 40 px) that sits outside the page (RTD-m10, M9). Built by W1-P.

- **The strip:** «Italy Legal Entry™ — V5, current best» · the v5-live tag, its commit and date · «Changed since the last
  report» (three lines from the steward's changelog, opened on demand) · «Personas» (Entrer / Sortir, §4.4) · the status
  of the page in the frame — «V5 — council-passed» or «V4 + fondation» · «Index» · «Open the page alone».
- **The default path** — the strip's quick links — holds council-passed surfaces only. Until the home passes (W2-D +
  W2-E), the frame's label reads «V4 + fondation».
- **`/__design-v5/index/`, one click away:**
  - **Public pages,** one row per page: the real URLs in fr and ar (it and en for the home and the login), each with
    «Desktop 1440» and «Phone 390» frames opened on demand. The hub's script holds **at most one frame pair at a time**,
    unloading the previous pair before it loads the next — enforced in code and tested, because 8780's database ceiling
    is 8 slots (RTE-m9).
  - **Authenticated pages** — four persona cards: «Personne avec dossier» (`qa-doc-person`, case `EE167596D4`), «Personne,
    conditions non acceptées» (`qa-person`), «Personne sans dossier» (`qa-fresh-person`), «Entreprise — Cantiere
    Adriatico» (`qa-company`). Each card has «Entrer» (a POST) and the list of its pages, in fr and ar. A staff persona is
    never offered.
  - **The family status board,** from `live_status.json` (written by the steward only): per family its state (V5
    council-passed / V4 + fondation), its scores, a link to the CD decision, its tag, its date. «V4 + fondation» pages are
    grouped apart, collapsed.
  - **The specimen boards** of the foundation families, under «Fondation».
  - **Compare with V4:** the same URLs on 8771 (main, phase 3) — never on 8780.
  - A link to the research archive.

### 4.2 `/__design-v5/research/` — the archive

- Today's hub moves here as it is. It holds the catalogue:
  - H-0 … H-E and E1–E3;
  - the hero and type pickers; compare;
  - the proof comps; the loader candidates;
  - navigation N-A / P-A; the colour and icon boards; the gate-0 package.
- Its «prototipo di ricerca — non approvato» labels are kept.
- The old URLs (`/__design-v5/hero/`, `/type/`, `/compare/`, `/proof/…`) redirect (302) to their `/research/` equivalents.
- The proof stays served from `C:/tmp/ile_v5_council/proof/`, outside the repository, as today.

### 4.3 What leaves the main path

- the option pickers, and every A/B/C page;
- the «non approvato» banners;
- the proof iframes;
- the «Baseline V4 (controllo)» group that points at the same server (`services.py:1709–1724`) — false the moment V5
  enters the templates;
- the index of frames as a landing page: it is one click away (§4.1).

### 4.4 How the authenticated pages are reached safely

Built by W1-P; passed by the council's security reviewer before it ships (RTE-M5).

**The persona switch:** `POST /__design-v5/accedi/<persona>/` and `POST /__design-v5/esci/`, inside `apps/designpreview`
(so it stays in the app's removal footprint).
- **Allowed only when all hold:**
  - DEBUG and `ILE_DESIGN_PREVIEW=1`;
  - a loopback `REMOTE_ADDR` **and no proxy header** — a request carrying `X-Forwarded-For`, `Forwarded`, `X-Real-IP`,
    `X-Forwarded-Host` or `CF-Connecting-IP` is refused, because a local tunnel or port-forward connects from loopback;
  - `Host` equal to `127.0.0.1:<port>` or `localhost:<port>`, for the process's own configured port
    (`ILE_DESIGN_PREVIEW_PORT`: 8780, or the lane's);
  - POST with CSRF, enforced by its own POST-only decorator (405 on GET; the existing `_preview_only` forces GET / HEAD,
    `views.py:70–83`).
- **Personas:** an allow-list of the four QA accounts, by e-mail, in the preview settings.
- **Refused:**
  - `is_staff` or `is_superuser` accounts;
  - unknown accounts;
  - any database not named in `ILE_DESIGN_PREVIEW_ALLOWED_DATABASES` — `ile_v5` and the named lane clones only; **never
    `ile_qa`**, the V4 control's database on 8771.
- **Sign-in:** `auth.login(request, user, backend="django.contrib.auth.backends.ModelBackend")`. It sends
  `user_logged_in`, so the entrance release plays as after a real sign-in (§1.9). One log line, carrying the persona key —
  never the e-mail (`test_log_privacy.py:57`).
- **Read-only personas:** a session opened by the switch carries a flag; while it is set, unsafe methods (POST, PUT,
  PATCH, DELETE) outside `/__design-v5/` get 403, except a named allow-list (signing out, the language switch). The
  personas never drift — accepting the terms as `qa-person` would destroy that persona. Flows that write (the Dépôt,
  uploads) are shown by the lanes on their clones, and through the states (`?état=`).
- **Absent** under the test and production settings.

**Distinct cookies for the preview process.** In `dev.py`'s preview block:
- `SESSION_COOKIE_NAME="ile_v5_sessionid"`;
- `CSRF_COOKIE_NAME="ile_v5_csrftoken"`;
- `LANGUAGE_COOKIE_NAME="ile_v5_language"`.
- Cookies are per host, not per port. With distinct names, a V5 session or language never clobbers V4's on 8770–8772;
  messages are session-stored, so they follow.

**No credential is typed anywhere.**
- The QA password literal in `scripts/qa_prepare_env.py` moves to an environment variable in design-v5 (W1-0's hygiene
  task).
- The literal stays in main and in git history (RTE-m7): the orchestrator confirms, from the repository and the deployment
  notes, that those accounts never existed on a remote host. If they did, rotating the password is an owner action before
  anything goes remote (§7.2).

**Frames** — the codebase's own pattern (`core.middleware.BackofficeCSPMiddleware`, `apps/core/middleware.py:49–61`):
- Real pages send `X-Frame-Options: DENY` and `frame-ancestors 'none'` (`base.py:335, 356`).
- A preview-only middleware, added in the preview block of `dev.py` and listed **after** `CSPMiddleware` and
  `XFrameOptionsMiddleware` (so its response hook runs first), sets `response._csp_replace` with `frame-ancestors 'self'`
  and `X-Frame-Options: SAMEORIGIN` (which `XFrameOptionsMiddleware` then keeps), and adds
  `Vary: Sec-Fetch-Dest, Sec-Fetch-Site`.
- **It applies only when all hold:** DEBUG + the flag; loopback with no proxy header; GET or HEAD; `Sec-Fetch-Dest:
  iframe`; `Sec-Fetch-Site: same-origin`.
- A top-level navigation keeps the normal policy.
- **Tests that prove it** run with `override_settings(MIDDLEWARE=<the dev chain>)`: relaxed only when every condition
  holds, strict otherwise; the database guard read from its setting, so the happy path is testable; 405 on GET; the
  read-only rule; the frame-pair cap.

### 4.5 The loader and the states, without credentials

- **The engage on the login:** submit any address with a wrong password — the key turns once and holds; the error page
  then loads at rest, with no light.
- **The release:** «Entrer» as a persona — the first console page plays the lit doorway on the rail's mark, once per
  session.
- **The stage's states:** focus on «Courriel», type an address, focus on the password — the stage answers at each step.
- **The 429 page:** through its DEBUG error route.

### 4.6 W1-P's acceptance

**Refusals and guards:**
- absent without the flag (404); 404 off loopback, with a proxy header, or with a foreign `Host`;
- 405 on GET for `accedi` / `esci`;
- staff accounts, unknown accounts and a database outside the allow-list refused — `ile_qa` included;
- distinct session, CSRF and language cookie names;
- persona sessions read-only: 403 on unsafe methods outside the preview, the allow-list excepted;
- the log line carries no e-mail.

**Frames and speed:**
- frames load real pages only under the narrow condition;
- at most one frame pair at a time, enforced by the hub's script;
- the strip paints in ≤ 1 s, and the landing loads exactly one frame;
- 0 CSP violations.

**Continuity:**
- the research archive's tests keep passing at their new paths;
- v5-live is checked out at the tag, and the orchestrator restarts 8780 after the merge.

---

## 5. PROCESS

### 5.1 The family loop — each step and what it produces

1. **Brief** (CD; ≤ 1 page).
   - The decided direction (§1), the family's slice of the manifest, the pages, the acceptance targets, the council, the
     **three named references** (§3.1 item 5) and, for platform families, the **identity carriers screen by screen**
     (§3.1 item 7).
   - Reports live in `W/docs/design-v5/QA/v54/<family>/` (brief, scorecard, the chairs' files, the CD decision, the
     report); heavy evidence — captures, traces, filmstrips, recordings — in E/<family>/, outside the repository.
2. **Audit and curation** (≤ 20 % of the family's effort).
   - **UI-UX-Pro-Max:** audit the *current* product pages of the family, rank the weaknesses, choose the strongest fix,
     re-audit after it. The calls are logged.
   - **21st.dev** (§5.4).
   - **The Emil principles,** as the review checklist: hierarchy, spacing, typography, timing, origin, interruption,
     press, the tooltip group, reduced motion.
   - No new research document; no option page.
3. **Implement** (the family's frontend engineer, in the family worktree).
   - LF bytes; real Django templates; real data; live copy only; only inside the slice.
4. **Self-review scorecard** (the implementer).
   - The six scales on §3.1's anchors and instruments, each with one evidence line; the taste row; the accessibility
     checklist; the performance numbers and their protocol; the radii count.
   - The standard capture set (§3.1). LOOK at every capture.
5. **Fix** until every self-score is ≥ 4. A surface at 3 / 5 never goes to the council.
6. **Independent council** — calibrated chairs (W1-K) that did not implement, in parallel, each on its own rig,
   re-measuring.
   - The order of reading: design → taste → UX → motion → accessibility → performance, plus the family's director.
   - Each scores the scales §3.1 assigns it, gives a verdict, and lists findings (blocking / major / minor), each with its
     concrete fix.
   - Taste runs TS §19 (the **eighteen** symptoms and the three portraits) and TS §21.2, and organises the flagship blind
     ranking. Motion judges filmstrips and frame-difference series.
7. **Fix** every blocking and major finding. The CD triages the minors.
8. **The Creative Director's decision:** PASSES, PASSES WITH CONDITIONS, or REDO, under §3.1's pass rule — the lowest
   chair's score ≥ 4 on every scale; the CD may refuse a pass, never grant one over a score below 4; a disputed score goes
   to a fresh chair; conditions are minor findings only.
   - The CD writes the reason in its own words («too editorial», «too SaaS», «incoherent», «premium», «passes», «redo»).
   - At most three council rounds. A fourth means the CD changes the direction internally.
9. **Checkpoint, then propagate.**
   - A checkpoint commit + the tag `v54/<family>/pre-propagation`.
   - Propagate to the family's scope.
   - Re-measure every page the change touches: two regressions once reached a commit from un-measured one-line
     corrections.
10. **Merge** (the steward): §2.2's five steps — the ownership check, `--no-ff`, the regenerated dist and inventories, the
    suites at 0 browser skips, the tag and the v5-live checkout. The report goes out as §3 schedules it (§6).

**The scorecard** — one table per family, in its QA folder:

| Scale | Lowest chair | Each chair | Evidence (one line, with a file) |
|---|---|---|---|
| Visual quality | n / 5 | … | TS §21.2 Q3–Q4 on the capture set |
| Premium feel | n / 5 | … | TS §21.1 Q1–Q8, no «No» |
| Originality | n / 5 | … | TS §21.1 Q2 + the swap test; the signature named |
| UX | n / 5 | … | the acceptance list; LA-9 / RH-6 |
| Mobile | n / 5 | … | the phone set, emulated |
| Coherence | n / 5 | … | TS §21.1 Q3 measured; radii per screen |
| Taste | 0 F / n P\* | … | portraits A–C · brochure n / 11 · §21.2 · blind ranking (flagships) |
| Accessibility | PASS / FAIL | … | keyboard fr / ar · axe · contrast · forced colours · reduced motion (`emulateMedia`) · reflow · 1.4.12 · targets |
| Performance | PASS / ACCEPTABLE / FAIL | … | LCP · CLS · INP · first-render task · bytes · requests · traces · protocol (n, pooling, tolerance) |
| Motion | — | … | filmstrips 1× / 0.25× · frame differences · recordings (flagships) |

### 5.2 The 20 / 80 rule in practice

- **A family's research is bounded:** the audit, the 21st shortlist, and the sources of this plan. Nothing else.
- **A question met during the build** is decided by the CD inside the family, written in DECISION_LOG as one line with its
  reason and its evidence, and built.
- **A prototype outside the product** is made only when a mechanism must be proven first. It is then archived under
  `research/`.

### 5.3 Roles

| Role | Authority |
|---|---|
| Executive Creative Director | the final word on design, inside §3.1's pass rule: it may refuse a pass, never grant one over a score below 4 |
| Product Architect | integration, data, the policy boundary, card personalisation, the shared files, the ownership manifest |
| Typography / Iconography / Image Art / Motion Directors | their systems; each scores premium and coherence on its families |
| Taste Director | blocks the generic-AI look before review; runs TS §19 and the blind rankings |
| UX lead | the user's questions answered, in order |
| Accessibility Lead | WCAG 2.2 AA, including 2.2.2 and reduced motion |
| Performance Lead | owns the lock and 8782 |
| Integration steward | merges, the dist, the inventories and the capture report, the tags, v5-live, npm, the status file, DL54's transcription |
| Frontend engineers | one per family lane |
| Chairs | only calibrated chairs (W1-K) score a gate; no chair scores a surface it built |

### 5.4 How 21st.dev, UI-UX-Pro-Max and the Emil principles are used inside a family

- **21st.dev — the sequence:** search many → shortlist ≤ 3 internally → choose one per mechanism → record its id →
  adapt the mechanism.
  - «Adapt» means route A: ILE CSS + vanilla JS under the CSP. No React, no copied styles, no imported icons.
  - 21st's AI generation is never used (the owner's credits). No page of alternatives is shown.
- **UI-UX-Pro-Max:** run on the family's current implementation, at the start and again after the fixes — never on
  abstract alternatives.
- **Emil Kowalski's principles:** the motion and design reviewers' criteria — timing, curve, origin, interruption, press,
  the tooltip group, the stills. The three flagged skills are not invoked; their written rules in MS and EM apply.

### 5.5 Discipline

- **Messages:** the orchestrator never messages a running workflow agent; that spawns a twin under the same id. Course
  corrections go into a notice file in the family's QA folder, read at the agent's next step.
- **Writes:**
  - LF bytes (Python `read_bytes` / `write_bytes`);
  - one writer per file, inside the slice of `OWNERSHIP_V54.json` — the steward refuses a merge otherwise;
  - git writes only on the family branch, and the steward's merges, tags and v5-live checkouts.
- **Production:** untouched. No deploy, no DNS, no remote infrastructure, no real e-mail, no external form.
- **Before «fixing» something that looks like a visual mistake,** check the token comments and the two design documents: it
  may be deliberate.

---

## 6. REPORTING

**When:** one report per passed flagship, and one per wave end. **Wave 1 has no report of its own:** the first report is
the first flagship that passes on a V5 page, and it carries Wave 1 in one line (RTD-M9). A flagship whose only seats are
«V4 + fondation» pages is reported with the first flagship that shows it on a V5 page: W1-D with W2-B (the login shows
the loader whole), W2-A with W2-C2 (the phone sheet and the account popover).

**Where:** the owner's channel. The same text sits in the hub's changelog.

**The format:**

1. **Title:** what is live now. For example: «Wave 2 — the login and the loader are live in V5».
2. **One paragraph per family,** always in this shape:
   «We compared X / Y / Z internally. The council chose Y because …. We implemented it on ‹pages›. Measures: LCP … ·
   CLS … · INP … · first-render task … · bytes … (protocol: n, pooling, tolerance). Scores (the lowest chair): visual … ·
   premium … · originality … · UX … · mobile … · coherence …; taste 0 F, n P\*; accessibility PASS; performance PASS. Open
   it: ‹8780 URL›. Reversible at tag `v54/<family>`.»
3. **What changed from what you approved — said in words.** For example: the hero's door rests ajar after it opens, and its
   revert; the key passes its reverse side mid-turn and ends on your mark; the navbar's per-entry glyphs removed and its
   gloss now in Host; the A-bis test's result.
4. **What we watched for, and fixed** — at most three lines.
5. **Recordings** (flagships): local 1× and 0.25× recordings of every motion, with their paths — judge the feel on them.
6. **What comes next** — the next families.
7. **Owner items** — A–E only, at most the current packet, each with its default if unanswered.
8. **Honest limits** — Chromium on Windows (with Playwright WebKit and Firefox where they ran); no real phone; no screen
   reader; HTTP/1.1 measurements until the milestone; no Moroccan reader until B2; **no person watched the motion at
   speed** until you have; the scores are the council's claim, the result is yours to judge.

**W3-B's report** also shows the personalisation value matrix and what replaced personalisation (§1.15).

**Never** «choose A / B / C / D». Never a picture to sign. Never a micro-choice.

**A worked example** (the numbers are placeholders until measured on the product):

> We compared three loaders internally: «Mandata» (the door answers), «Lume» (the light answers) and «Passo» (the path
> answers). The council chose «Lume», as one gesture across your sign-in: when you press the sign-in button the key turns
> once and holds; when your space opens, its doorway fills with light — once, and only if the sign-in succeeded. A refused
> sign-in shows no light. The planes, the door and the steps never move; the key passes its reverse side mid-turn and ends
> on your mark. We implemented it on the login and the reserved area. Measures: ‹n› ms of main thread per run, no long
> task, CLS 0, nothing loops (n = 9, interleaved, CPU ×4). Scores (the lowest chair): ‹…›; taste 0 F, ‹n› P\*. Recordings at
> 1× and 0.25×: ‹paths›. Open http://127.0.0.1:8780/__design-v5/, then «Personas» → «Entrer» as «Personne avec dossier».
> Reversible at tag `v54/w2-b`.

---

## 7. RISKS AND WHAT IS NOT DECIDED (honest)

### 7.1 Risks

| # | Risk | Where | Mitigation |
|---|---|---|---|
| 1 | The serif-less public face scores below 4 on premium | W2-E, W3-F | The A-bis test runs blind at W2-E whatever the scores, and again on any premium < 4 or the owner's verdict (§1.1). B is two tokens from A. |
| 2 | Transitional CSS weight while the legacy and V5 layers coexist | every merge | A measured baseline + 8 KB in Wave 1, then a ceiling that never rises; the deletion map, V1 included; page-only partials out of `main.css`; the bust rule (§2.6). |
| 3 | Shared names (78 tokens, 110 classes) make W1-A regress pages that are not yet refined | W1-A | «No page worse than before», blocking (§3.1 item 6). Fixes go into the aliases, not the templates. |
| 4 | The hero-final workflow needs more rounds | W2-D | The home stays «V4 + fondation», off the hub's default path. Wave 3 does not wait for it; only W2-E and W3-F1 do. |
| 5 | «Lume» departs from the research's recommendation and from M10's letter; its release seat was never shot below 120 px | W1-D | The release only after a successful sign-in; three measured fallback conditions, then «Mandata», then the engage alone; BA §1's amendment in DL54. |
| 6 | Measurement covers Chromium on Windows only: no Safari, no real phone, no screen reader | all | WebKit and Firefox in W2-A's gate and W4-C; every report states the limit. |
| 7 | Apple fallback metrics are missing (a bare swap measured 0.33 on the documents page) | W1-A → milestone | First-screen faces are preloaded. The metrics are computed before the milestone. |
| 8 | The Arabic pages carry French copy under Arabic layout, and the faces are unreviewed | all | B2; `/ar/` is not signed until then. Layout rules are enforced (§1.18 D21). |
| 9 | The copy packet is slow, so some UX gains wait | W2–W3 | Live second lines where they exist; live strings everywhere else. |
| 10 | Test-suite cost: 2,444 tests, retargets and the DS doc tax slow every family | all | One database per lane; the per-wave suite matrix; retargets in the same merge; inventories regenerated by the steward. |
| 11 | The persona switch is a password-less login | W1-P | DEBUG + flag + loopback + no proxy header + its own `Host` + POST / CSRF + allow-list + a database allow-list without `ile_qa` + no staff + read-only sessions; tests on the dev middleware chain; the security review; absent outside dev. |
| 12 | Drawer INP: `showModal()` restyles 633–811 elements | W2-A | Pre-layout at idle; above 200 ms p90, `show()` + scrim + a focus trap — never `inert` on `main` alone. |
| 13 | First-render long tasks exist on every page | all | Budgeted per page against the before-set (§2.6), not eliminated. |
| 14 | Parallel family branches conflict | Waves 2–3 | The ownership manifest and its check; serialized files; per-family test files; the dist `merge=binary` and rebuilt from clean. |
| 15 | The owner dislikes a propagated family | any | The latest family reverted, older ones corrected forward; the preview rolled back at once by tag checkout (§2.2). |
| 16 | Two «Mes pièces» routes | W3-C | Both render the same V5 workspace. Merging the URLs is policy — not pursued. |
| 17 | Staff and back-office surfaces have no audit | W3-E | Out of V5.4, recorded as design debt. The unfold back-office keeps its theme (colours mapped only). |
| 18 | The interim phase is not designed in V5 | W4-D | Built only if the go-live phase needs it. The Forum date has passed, so the interim's Forum CTA is stale (O39). |
| 19 | The QA personas on `ile_v5` are unverified | W1-0 | Counted before W1-P ships; read-only on 8780. |
| 20 | `ile_v5`'s `MenuItem` «main» rows may override the fallback IA | W2-C1 | Checked as data; no migration. |
| 21 | The owner's preview shows a merge in progress | every merge | 8780 serves v5-live at the last green tag (§2.2). |
| 22 | An npm write lands in main's `node_modules` | any | design-v5's own `npm ci`; lanes junction to it; npm is the steward's alone. |
| 23 | The council scores its own team generously | every gate | W1-K's calibration; the lowest chair per scale; fresh-chair re-scores; blind rankings for flagships; the owner's verdict as a trigger. |
| 24 | The platform lift reads as subtraction — «too simple, too shadcn» | W3 | Identity carriers per screen; the swap and symptom-10 checks; ≤ 3 radii; the lit arris on night only; the Lucide sheet (§3.1 item 7). |

### 7.2 Not decided, and why

**Product-policy changes, left out of V5.4.** Each would need the owner (class C). None is asked now; each is parked:
- «Se souvenir de moi» (`ACCOUNT_SESSION_REMEMBER` is `False`);
- a session-end warning, or a way to extend the session;
- storing «since your last visit» — so in V5.4 the journey has no relay and there is no «Nouveau depuis»;
- one-event notification semantics (reading a message also clears its notification);
- «Bloqué» as a state of a piece (`RequirementState` has none);
- fewer rail destinations, or merged routes (URL and permission consequences);
- the Forum's pre-opening state model;
- a server-side store for UI preferences (it also needs the privacy text checked, B);
- letting users hide binding regions — refused, not parked;
- the review calendar behind a «verified on» line;
- any change to the precedence behind `next_action`;
- the «Définition» legal-term popovers (they need a legal reading).

**Owner actions before anything goes remote** (not design questions):
- the door photograph's rights record (DL A22);
- the rotation of the 21st and Pexels keys;
- the rotation of the QA password, only if the orchestrator finds those accounts were ever used on a remote host (§4.4);
- the three flagged Emil skills — a process permission; they are not invoked.

**Questions the plan cannot settle alone:**
- **Where the hero-final CD's decision differs** from §1.10, §1.16 or §1.17: it binds for the hero, and the CD reconciles
  the two in DL54 at W2-D's step 0, before any port code.
- **Whether the owner finds the result premium at his bar.** The council's scores are our claim, calibrated on his own
  past verdicts; the owner judges the working result. That is the directive's own order (V54 l.7, l.33).

---

## 8. RED-TEAM RESOLUTION

Both red teams returned SOUND WITH FIXES. Every finding below is **accepted**; none is rejected. Where a fix offered two
ways, the row says which one this plan takes and why.

### 8.1 Design red team (RTD)

| # | Severity | Finding | Resolution |
|---|---|---|---|
| B1 | blocking | The ≥ 4 / 5 gate had no anchors, no aggregation and no originality instrument; a CD override could pass a 3; no calibration; no named references | **Accepted.** §3.1 rewritten: Hd §8.3's anchors with V5.1 §96 as the bar; one instrument per scale (premium TS §21.1 with no «No»; originality §21.1 Q2 + the swap test naming the signature; coherence §21.1 Q3 measured; visual §21.2 Q3–Q4; UX the acceptance list + LA-9; mobile emulated, said so); the minimum over the chairs; the CD may refuse, never grant over a sub-4; a disputed score re-measured by a fresh chair; «with conditions» only at ≥ 4 everywhere with minor conditions; W1-K calibrates the chairs on the V4 dashboard, the gate-0 login and H-E as built before any gate; three named references per family with side-by-side captures (§3.1 items 1–5, §3.3, §5.1). |
| M1 | major | The taste gate dropped TS §19.1 items 3–4 and HEB §7's blind ranking; «17 symptoms» | **Accepted.** 0 F and ≤ 1 P\*, a failed portrait B or C counted as a P\*; the swap test passing with its signature named; the brochure test ≤ 2 of 11; TS §21.2's pass rule; for flagships, a blind ranking by three non-builders against V4 and two named references. Eighteen symptoms, everywhere (§3.1 item 4, §5.1, DL54). |
| M2 | major | Type B rests on less evidence than claimed | **Accepted.** B stays the default (two tokens); bytes dropped as a reason; TR's measurements against B stated in full; the A-bis test unconditional at W2-E, the first full page on the light wall, ranked blind by taste and design; the trigger fires on any premium < 4 on the home or a door page, whatever the attribution, and on the owner's verdict; TY-2, TY-3, CDV law 2's serif clause and HET §0 item 9 retired under B in DL54 (§1.1, §3.4). |
| M3 | major | Black-and-white → colour made sitewide | **Accepted.** Confined to the home hero; the navbar panel and every other audience photograph rest in colour, in the V5 grade; a wider use needs its own taste test at ≤ 1 P\* with #20029 named (§1.16, §1.12). |
| M4 | major | The navbar flip re-opened the anatomy the owner closed | **Accepted.** 8 \| 4 kept, the photograph at the end; NV-5 fixed by the content-width panel and the entries column starting at the first door, with the gloss on the lock-up's span — no flip; a short live second line per entry where one exists, never clamped; the panel descriptions are B1 item 1; the false «every element kept» replaced by an honest list of additions and removals; N18 «richer than Fase 3» judged by design and taste at 1440 and 1920 (§1.12). |
| M5 | major | The login's answer to «too static» was a one-shot, then rest | **Accepted.** Nothing loops, and the stage answers the person — focus on «Courriel» lights the routes, a valid address holds them, the password carries the light to the frame, submit turns the key — tier 1–2, compositor-only, 0 ms from the keyboard; three person-driven states visible at t = 10 s (L7); the end states without travel under reduced motion (§1.13). |
| M6 | major | «Lume» said «open» on a refused sign-in; the mark played twice; the brand rule | **Accepted.** One gesture across the page load: on submit the key turns and holds, with no light; the release only on the arriving console page after a successful sign-in, once per session, never over painted content; the error page at rest; BA §1's amendment recorded in DL54 citing V54 l.19, with a pointer in BA §1; the one named exception written into the console rule (MS §3.2), §2.6 and W3-A's gate; §4.5's demo rewritten (§1.5, §1.9, §2.6, §3.5, §4.5). |
| M7 | major | The ported hero rests ajar while the plan said «untouched» | **Accepted — option (b), decided now.** The ajar rest is taken under V54 l.9 and said in words in the hero report, with its revert (the rest opacity 0.8 → 0; the tag `v54/w2-d`); recorded in DL54 before W2-D. Option (a) is not taken: a door that opens and shuts again reads as a refusal (HF §9.2). §1.17's invariant rewritten to what holds; §1.19 A lists the change (§1.17, §1.19). |
| M8 | major | The platform lift is subtraction; the corners are Tailwind's; a lit edge; Lucide geometry; screens with no carrier | **Accepted.** Identity carriers named screen by screen in every platform brief; the swap test, the symptom-10 check and TS §21.1 Q1 on every console screen type; the lit arris only on night plates; ≤ 3 distinct radii per screen; the ILE sprite beside raw Lucide at 1× and 2× before W1-B merges (§1.3, §1.4, §1.7, §1.13, §1.14, §3.1 item 7, §3.3). |
| M9 | major | The owner's first view was V4 re-valued; the foundation had no ≥ 4 | **Accepted.** Foundation families scored on specimen boards, plus a blocking «no page worse than before»; the first owner report is the first flagship passed on a V5 page, with Wave 1 in one line; the hub's default path shows council-passed surfaces only and labels the rest «V4 + fondation»; the hero's REDO fallback kept off that path (§2.1, §3.1 item 6, §3.3, §4.1, §6, §1.17). |
| M10 | major | Motion «feel» certified by agents that cannot watch at speed | **Accepted.** The motion chair judges filmstrips and frame-difference series; flagship reports carry local 1× and 0.25× recordings; «no person watched the motion at speed» joins the honest limits; the «Mandata» fallback fires on three measured conditions — the doorway's light share by ΔE00 over 600 ms, the muddy-tone chroma dip, the glow watch-point (§1.5, §1.9, §6). |
| m1 | minor | The login CTA broke SH-9 | **Accepted — the flat way:** strength from the key, the full width and the weight; no arris, no shadow; L14 tests it. No entrance exception is added to SH-9 (§1.4, §1.8, §1.13). |
| m2 | minor | L3's scope was ambiguous | **Accepted.** L3 on asynchronous fragments only (the preview drawer, notifications, search, «Aller à…»), never on server-rendered regions; `test_loader_rules` checks it (§1.5, §1.9). |
| m3 | minor | N2 and N3 could not both hold | **Accepted — N2 on the first door,** a pointer-path budget for doors 2–4 (a safe triangle, a browser test per door, the travel reported); N3's shared origins kept (§1.12). |
| m4 | minor | C8's «argento» caveat was dropped | **Accepted.** W1-A's colour board checks that Istituzione reads as a hue on night beside the other three; the hero's set still wins (§1.2, §3.3). |
| m5 | minor | D26 mixed layout and wording | **Accepted.** W3-F builds the slots with verbatim headings; question headings and the «who can help me» wording are B1 item 7 (§1.18, §1.19, §3.5). |
| m6 | minor | «The owner is never that trigger»; the CD judged reversals of its own decisions | **Accepted.** Every trigger includes the owner's verdict on the shown result; triggers are mechanical — a measured condition, then an independent chair; the CD never adjudicates a trigger on its own decision (§1 head, §1.1, §1.9). |
| m7 | minor | The key's turn passes through its mirror image | **Accepted.** The reading «never held, drawn or served mirrored» recorded in DL54 and stated in the loader and hero reports (§1.9, §1.17, §1.19). |
| m8 | minor | The portico panel sat outside the overlay system | **Accepted.** The panel uses `overlay.js`'s scrim, dismissal and focus primitives and the overlay motion tokens, and stays a disclosure navigation; the switch lands in W2-C2, after W2-A (§1.12, §1.14, §3.4). |
| m9 | minor | Values disagreed; the parity check failed by construction | **Accepted.** Reconciled in DL54 (§8.3): eighteen symptoms; six scales (N17, L13); CLS ≤ 0.05 on flagships with 0.01 a target; `--ease-turn`; the hero's files. §1.17's constraints are checked against the hero-final build at W2-D's step 0, before any port code (§1.17, §2.6). |
| m10 | minor | The hub could read as a catalogue | **Accepted.** `/__design-v5/` lands on the live V5 home under a slim strip (commit, changes since the last report, personas, status); the index is one click away (§4.1). |
| m11 | minor | Personalisation left silent | **Accepted.** W3-B's report shows the value matrix and what replaced personalisation (§1.15, §6). |
| m12 | minor | The corner evidence was over-read | **Accepted** — folded into the cap of three radii per screen (§1.3). |
| m13 | minor | The hero port had only a taste spot check | **Accepted — a full taste chair at W2-D,** rather than deferring the verdict to W2-E (§1.17, §3.4). |

### 8.2 Engineering red team (RTE)

| # | Severity | Finding | Resolution |
|---|---|---|---|
| B1 | blocking | The CSS budgets were infeasible under the plan's own sequence | **Accepted.** W1-0 records each page type's CSS bytes; the cap is the baseline + 8 KB gzip in Wave 1, then a ceiling that never rises from the first Wave-2 merge; the 36 KB `main.css` target moves to the milestone (W4-D), justified as V4's weight; every family deletes each legacy rule it supersedes, V1 included, by the deletion map (shared sheets by section, the last named consumer deletes the file); the door stage, the loader light and the public passage become page partials outside `main.css`, with tokenised gradients and `test_design_docs.py:612` retargeted; a family over its ceiling does not merge (the bust rule); every bundle change re-measured with the fonts (§2.1, §2.3, §2.6). |
| B2 | blocking | 8780 served the integration worktree | **Accepted.** 8780 serves `C:/tmp/ile_wt/v5-live`, a detached HEAD at the last green tag; the steward merges, builds, tests and tags in design-v5, then checks the tag out in v5-live, and the orchestrator restarts 8780; rollback is a checkout of the previous tag; `.gitattributes` marks both dist trees `merge=binary`; `static/js/dist/` is deleted before `build:js` (§2.2, §2.8, §3.3). |
| M1 | major | `node_modules` was a junction into main's | **Accepted.** design-v5 gets its own `npm ci` in W1-0; lanes junction to design-v5's `node_modules`; only the steward runs npm; both package files serialized; `test_frontend_bundle_is_current.py:45` rewritten in W4-B's merge (§2.2, §2.7, §3.6). |
| M2 | major | Reduced motion could not be the designed state | **Accepted.** The universal block deleted in W1-D and replaced by the V5 rule; `test_design_docs.py:815`, A11Y §7 and `test_v4_tokens.py:231` retargeted; one `reducedMotion()` gate (media query + preview flag) for every WAAPI / rAF sequence, with a static test; no wait on transition events without a timeout; `test_rm_flag_parity` ships with W1-D; council evidence through `emulateMedia` (§1.5, §2.7, §3.3). |
| M3 | major | The test map was incomplete and partly contradicted the layout | **Accepted.** Every pin listed has an owner in §2.7; the `main.css`-only checks read the console entry and the page sheets; gradients tokenised; the steward regenerates `capture-report.json` and the weight tables; W1-A removes the adopted names from the shim and lowers its ceilings; the V1 token and contrast tests retargeted to the effective cascade or retired into `test_v5_tokens`; the merge gate runs `-m browser` at 0 skips; the per-wave suite matrix adopted (§2.2, §2.7). |
| M4 | major | «One writer per file» was not guaranteed | **Accepted.** `OWNERSHIP_V54.json` (globs + function and section slices), checked before each merge by `check_ownership.py`; inventories and the capture report regenerated by the steward; `main.js` sliced by function; new tests in per-family files; every unowned file assigned — `home.html` and `pages/js/home.js` to W2-D, `focus-clear.js` to W2-C1 if built, `head.js`, the release flag (`signals.py`) and the Wave-1 rail hook to W1-D, the content templates to W3-F2 and the console ones to W3-E; the targa popover sequenced after W2-A, in W2-C2 (§2.2, §3). |
| M5 | major | The persona switch had gaps | **Accepted.** Proxy headers refused and `Host` pinned to the process's own port; `ile_qa` dropped — `ile_v5` and named lane clones only, from a setting; persona sessions read-only (403 on unsafe methods outside the preview, with an allow-list) — chosen over resets, so the personas never drift; lane clones made before 8780 starts; the frame exception in the codebase's `_csp_replace` pattern, after `CSPMiddleware` and `XFrameOptionsMiddleware`, with `Vary`, GET / HEAD only; tests on the dev middleware chain, a settings-driven database guard and a POST-only decorator; a persona key in the log; the preview's own language cookie (§2.5, §2.8, §4.4, §4.6). |
| M6 | major | The hero parity check could not pass | **Accepted.** The prototype re-held on the W1-A token sheet; the hero box compared with the chrome masked; performance at n ≥ 9 interleaved cold loads per cell in one lock window, with PFR's tolerances in ms, against the product's before-set and the re-held prototype; the expected CSS delta stated before measuring — «delete the legacy layers first» is not available, because W2-D runs beside W2-A and W2-C1; W2-D owns `home.html`, and `pages/js/home.js` is folded into the home entry and deleted; the tokenisation of the prototype's colours and gradients budgeted, with its own re-check (§1.17, §3.4). |
| M7 | major | The overlay system had three gaps | **Accepted.** `showModal()` with pre-layout at idle; above 200 ms p90, `show()` + scrim + a script focus trap + `aria-modal` + Esc + focus return, proved by keyboard tests — never `inert` on `main` alone; a top-layer tooltip variant for clipping containers, with a hover bridge and Esc; feature floors and fallbacks per engine; WebKit and Firefox in W2-A's gate; the preview drawer keeps `?état=` with `replaceState`; «Fermer» always present, tested (§1.14, §2.7, §3.4). |
| M8 | major | Reversibility was narrower than claimed | **Accepted.** The policy is written: revert only the latest family and correct older ones forward; the revert-of-revert procedure; the preview rolls back by tag checkout; main tagged `v4-control-final` before D1 (§2.2, §2.9, §1.19). |
| M9 | major | 8782 did not measure what ships | **Accepted, with one mechanism changed.** 8782 runs `CompressedManifestStaticFilesStorage` with `DEBUG=False` and `CONN_MAX_AGE` 0; «the same data for both twins» is obtained by measuring the V4 reference on 8782 itself at `v54/base` — the same database clone, storage and `ILE_REFERENCE_DATE` — instead of on 8772, which stays untouched; the protocol (n, pooling, tolerance) in every report; one HTTP/2 run before the milestone, or its absence stated (§2.6, §2.8, §2.9). |
| M10 | major | The French-typography filter touched locked copy | **Accepted — both halves:** locked output (`{% locked %}`, `data-locked`) is excluded from the filter now, and the no-break-space rendering of locked strings is B1 item 8; only once it is signed do the tests and `verify_locked_against_source.py` normalise U+00A0 (§1.1, §1.18, §1.19). |
| m1 | minor | Five new ESM entries per public page; no request budget | **Accepted.** One public entry (`shell.js` imports `nav` and `overlay`; `loader` imported on the first submit; `focus-clear` only if built); the home's two scripts become one; a request budget per page type (§2.3, §2.6). |
| m2 | minor | The OFL texts did not exist | **Accepted.** The OFL text for each family in `static/fonts/licenses/`, IBM's notice kept for «ILE Mono» (§2.3, §3.3). |
| m3 | minor | Cherry-picking and merging main both planned | **Accepted — cherry-pick:** main is never merged into design-v5; its code commits are cherry-picked at each wave start and listed in the changelog, so main's orchestration documents and personal drafts stay out (§2.2). |
| m4 | minor | `focus-clear.js` duplicated the scroll padding | **Accepted.** The CSS-native `scroll-padding-block-start` is kept and measured by W2-C1; the module is written only on a measured failure, and W2-C1 owns it (§1.6, §2.3). |
| m5 | minor | `var(--dir)` translations and script-placed indicators escaped the RTL guard | **Accepted.** `test_rtl_browser` covers the architrave under the active item and menus on the inline end, in Arabic (N19, §1.14, §2.5). |
| m6 | minor | The L1 allow-list had no test | **Accepted.** `test_loader_rules` asserts L1 markup only on its allow-listed templates and never on an `OUTCOME_BEARING` form (§1.9). |
| m7 | minor | The QA password literal stays in main and in history | **Accepted.** W1-0 moves it to an environment variable in design-v5; the orchestrator confirms the accounts never existed on a remote host; if they did, rotation is an owner action before anything goes remote (§4.4, §7.2). |
| m8 | minor | W2-C's door layout moves pinned figures | **Accepted.** DS 2026 §7.2 / §11, A11Y §3 and `capture.py` are inside W2-C1's slice (§2.7, §3.4). |
| m9 | minor | The frame-pair limit was enforced only by layout | **Accepted.** The hub's script holds at most one frame pair at a time, tested; the landing loads one frame (§4.1, §4.6). |

### 8.3 What DL54 receives from W1-0, before W1-A

1. The generic-AI test has **eighteen** symptoms (TS §19.2).
2. **Six** scales everywhere — visual, premium, originality, UX, mobile, coherence — N17 and L13 included.
3. CLS: ≤ 0.10 on every page, ≤ 0.05 on flagship pages, font swap ≤ 0.01; 0.01 elsewhere is a target.
4. `--ease-turn` = `cubic-bezier(0.77, 0, 0.175, 1)`, replacing LS's `--sig-turn` and gate-0's `--ease-turn-in` / `-out`.
5. The hero's files: `templates/pages/home/_hero.html`, `apps/pages/static/pages/css/hero.css`, `static/js/src/hero.js`.
6. BA §1 amended: the mark moves «once, at the entrance, across the page load» (V54 l.19).
7. «The tricolour mark never mirrors» means never held, drawn or served mirrored; the turn passes its mirror image (V54
   l.9, l.19).
8. M10's letter («frame light only») yields to V54 l.19; its reasons hold.
9. TY-2, TY-3, CDV law 2's serif clause and HET §0 item 9 are retired under type B, and return with A-bis's scope if W2-E
   switches.
10. The hero's door rests ajar after the opening, under V54 l.9, with its revert.
11. Black-and-white → colour is confined to the home hero.
12. The lit arris has one seat, night plates; every primary but the hero's CTA-B is flat.
13. At most three distinct radii on a screen.
14. The `_`-partial rule; the app-sheet token rule; the CSS ratchet and its bust rule.
15. The gate of §3.1, the calibration (W1-K) and the reference list.

*End of the plan. One writer: the council (plan-final). Next step: the orchestrator launches W1-0, then W1-K, W1-P and W1-A
(§3.3).*
