# COLOUR V5 — «carta, notte, laguna, oro» and eight status tones

Council of the V5 escalation · role **Colour / Material Designer** · 26 September 2026 · status **PROPOSAL, not wired** (the repository was read only).

| What | Where |
|---|---|
| Tokens (primitive → semantic → component, CSS custom properties) | `C:/tmp/ile_v5_council/council/colour/tokens-v5-colour.css` (22.4 KB with its comments, ≈ 13 KB without) |
| Specimen that consumes the tokens exactly as a component would | `council/colour/specimen.html` + `specimen.css` |
| Captures of the specimen (1440 and 390, plus crops) | `captures/colour/specimen_1440.png`, `specimen_390.png`, `specimen_chips.png`, `specimen_shells.png` |
| Captures of the current V4 colour use (before) | `captures/colour/sc_colour.png`, `sc_states_chips.png`, `sc_console_strip_rows.png`, `sc_console_ctx.png`, `home_fr_*.png`, `showcase_full.png` |
| Colour maths (WCAG 2.x relative luminance, OKLab/OKLCH, Machado 2009 CVD) | `scratch/colour/colourlib.py` |
| Diagnosis of V4, with numbers | `scratch/colour/diagnose_v4.py` → `diagnose_v4.out.txt` |
| Solver that produced the eight tones from hue + chroma under contrast constraints | `scratch/colour/tones_v5.py`, `gen_primitives.py`, `explore_tones.py`, `refine_800.py` |
| **Proof**: every ratio recomputed from the CSS file itself (var() chains resolved) | `scratch/colour/verify_tokens.py` → `verify_out.md` — **363 pairs checked, 0 below their minimum** |
| UI-UX-Pro-Max searches (colour, style, ux domains) | `scratch/colour/uupm/*.txt` (18 files) |

Every ratio quoted below is WCAG 2.x, floored to two decimals (a printed figure never overstates), and comes from `verify_out.md` or `diagnose_v4.out.txt`.

---

## 0. In ten lines

1. The owner is right on every count, and the numbers say so (§1): two of the six V4 registers are the *same* colour (neutro = attesa, ΔE 0.000), VALIDÉ is plain ink, EN EXAMEN = DÉPOSÉ, BLOQUÉ = MANQUANT; the chip bodies are invisible tints (ΔE 0.03–0.05 from the sheet); the pending brown `#705434` is the «dirty» colour; `--err-700` is the «crude red» (the most saturated colour in the system, C 0.178); five generations of neutrals are still in the cascade; the legacy shim paints 42 «accent» sites in a *red*; the forum banner's primary button sits at 1.46:1 on paper.
2. V5 keeps what is measured and shipped — the mineral paper, the ink, the navy-midnight evolved from the brand navy, the one lagoon accent, the shadows and depths of V4 — and **renames nothing a component reads today**: the V4 names become aliases of primitives with the same hex.
3. It adds **one material per state**: eight tones solved in OKLCH under contrast constraints — registro (lapis), esame (wisteria), deposito (slate), ambra, cotto (terracotta), granata (garnet), grafite, cenere — each with eight steps (body, hover body, edge, mark, word; night body, night word, night mark).
4. **No colour ever means «approved»**: green is gone from the whole system (`--ok-*` retired); VALIDÉ takes the *institution's ink* (lapis, the colour of the record and of the info notice), not a verdict colour. This is a change of expression of CR-11, not of the rule, and it is an owner/legal decision (§14).
5. **Nothing relies on colour alone**: every state is word + glyph (one 16 px circle grammar: outline = open, filled = settled) + pattern (hatch, dots, cross-hatch on strips and legends) + edge style (solid, dashed, dotted); the marks form a luminance ladder (3.1 → 9.1 on paper) so a greyscale or colour-blind reader has a second channel before the glyph.
6. The **tricolour** stays where the brand puts it: the mark, the wordmark, and one 3-segment filet on the institutional notice. Gold is the key: ornament on paper (2.37:1, never a word), text-capable on night (`oro-300`, 9.94:1).
7. **One family, two shells**: the public site reads on warm stone (page carta-50, sheet carta-25); the console works on paper one step lighter (page carta-25, sheet white) with night chrome — same primitives, no new hex, every pair verified (§5).
8. **Icons** take one of six semantic colours (`--icon-*`) and never a brand colour; a status glyph is painted by its chip.
9. **One focus ring** (`laguna-550`, 2 px, offset 2 px, 30 % halo) on paper, its light on night, and a two-tone ring on photographs.
10. Everything here is **A — adapt to Django + CSS**: no JavaScript, no React, no runtime cost beyond ≈ 13 KB of custom properties before gzip; 21st.dev patterns were consulted by other members and contribute nothing chromatic that survives CR-11.

---

## 1. What the owner sees today — the diagnosis, measured

Source: `diagnose_v4.out.txt` (V4 tokens, `v3/chip.css`, `v4/workspace.css`, `tokens.css` §STATE, `_legacy-tokens.css`), captures `sc_states_chips.png` and `sc_colour.png`.

| Owner's word | What is on the screen | Measure |
|---|---|---|
| **states too similar** | `neutro` (DÉPOSÉ, EN EXAMEN…) and `attesa` (MANQUANT, À REMPLACER, BLOQUÉ) share the mark `--ink-2 #4a5a62`; only a dashed vs solid 3 px rule separates them | ΔE OKLab **0.000** (identical colour) |
| | `conforme` (VALIDÉ) is `--ink #15222a`: the same colour as the word beside it | ΔE to the word 0 |
| | The chip body is `color-mix(mark 8 %)`: on the sheet it is a tint the eye cannot name | ΔE body → sheet 0.028 – 0.052; chroma ≤ 0.013 |
| | Notices: `warning` and `pending` are two beiges | ΔE bodies **0.010**, texts 0.054 |
| | Four of nine document states differ **only by the word** (see `specimen_chips.png`, left panel) | — |
| **dirty colours** | `--pending-700 #705434` («en attente», EXPIRÉ, deadlines «soon») | OKLCH L 0.47 **C 0.060** h 69 — a desaturated brown: it reads as mud, not as amber |
| | `--seal-600 #8c6d4b` bronze | C 0.062 h 69: the same mud, lighter |
| **crude red** | `--err-700 #b3261e` | L 0.50 **C 0.178** h 29 — the most saturated colour in the system, orange-leaning; and the rubric `#a4231b` and the brand red `#c4142b` are two more reds 0.03 / 0.07 away |
| **random colours** | five generations of neutrals are reachable in the cascade: V1 `--paper #faf7f0`, `--paper-deep`, `--paper-edge`, `--rule-hair`, `--rule-ink`, V2 `--min-*`, `--hairline*` | V1 warm paper h 87 C 0.010–0.020 vs V2 stone h 91–98 C 0.003–0.007: two different papers on one site |
| | three navies: V1 `--navy #0e2a47`, brand `#0f2547`, V4 `--mid-1 #0b1a33` | ΔE 0.017 / 0.062 |
| | the legacy shim resolves `--color-accent-600/700` and `--border-accent` to **`--rubric` (a red)** | **42 uses** in `components.css`, `pages`, `ecosystem` |
| | `--ok-700 #1e7a4d` green exists as a token («never approved») and `state-done` is a fourth blue `#1e4a85` | — |
| **not premium** | the forum banner on the home puts the *dark* primary (`#7fd1d8`) on a *light* ground | **1.46:1** on `--min-1` (a white-on-white button) |
| | `chips.GLYPH` (clock / warning / check / close / minus) is defined in Python and **rendered nowhere** (UI_INVENTORY §7): the non-chromatic channel the spec promised is absent from the DOM | — |

What is **not** wrong and is kept: the paper (`--min-*`), the ink, the navy-midnight scale, the lagoon accent and its gradients, the six shadow roles, the glass composites, the deadline discipline «never all red» (owner directive §19). Every one of those values was measured in V4 gates A–C and re-verified here.

---

## 2. Research — what was taken and what was refused

**UI-UX-Pro-Max** (`search.py`, domains colour · style · ux; 18 result files in `scratch/colour/uupm/`):

| Query (domain) | What came back | Taken / refused |
|---|---|---|
| «institutional navy premium», «legal tech trustworthy», «consulting professional services», «editorial warm paper», «dark navy premium» (colour) | the same family every time: **authority navy + trust gold** — Legal Services `#1E3A8A` / `#B45309`, Research Lab `#1E3A5F` / `#A16207`, Banking `#0F172A` / `#A16207`, Academic Journal `#1E3A5F` / `#B45309`; backgrounds `#F8FAFC`; destructive always `#DC2626` | **Taken**: navy as the institution, gold as the *accent of identity*, not of action — exactly the brand's own split (navy door, gold key). **Refused**: the cold Tailwind slate background (`#F8FAFC`), the `#DC2626` red (C ≈ 0.20: the crude red), and gold as a CTA colour on paper (`#B45309` reaches 4.6:1 only because it is brown) |
| «government public service accessible», «status semantic states dashboard» (colour) | Government Portal «blue + service green», Status Page «operational green + incident red + maintenance amber», IoT/finance «dark + status green» | **Refused wholesale**: green = done contradicts CR-11 («no colour means approved»); the traffic light is the pattern the owner called crude. Kept only the *principle* that a status system needs a distinct material per state |
| «glassmorphism dark premium», «liquid glass» (style) | glass = navigation and controls only, `rgba(255,255,255,.1–.3)`, blur 10–20 px, 1 px border at 20 % | **Taken as already built**: V4 `--glass-light .85`, `--glass-dark .55`, `--blur-nav 12px` — glass on sticky bars, never on content (DS V4 §1.4). No change |
| «enterprise dashboard trust» (style) | Fluent 2 and Spectrum: «semantic tokens, component states, focus-visible, reduced motion»; Swiss minimal for consoles | **Taken**: the three-layer token architecture (§11) and the console shell one step lighter (§5) |
| «color contrast status badge color alone», «status badge semantic colors accessible», «focus» (ux) | «don't convey by colour alone — icons/text in addition»; «4.5:1 normal text»; «focus indicator ≥ 2 CSS px perimeter, 3:1»; «one atomic status message per region, not a live region per badge»; «a chip label stays whole on one line» | **Taken** (§6, §9): word + glyph + pattern; ring 2 px offset 2 px ≥ 3:1 on every ground; the chip specification of the primitives member already carries the one-`role=status`-per-region rule |
| «dark mode», «dark mode palette elevation», «night mode surfaces» (ux, colour) | **no database match** (ux); colour returned sleep/alarm apps on indigo | Stated honestly: no external guidance was found for the night scale. The night levels are V4's measured scale (`--mid-0…4`) kept as `notte-950…700`, and every night pair was computed here |

**Reference sites** (agamieuromed.org, studiobadrane.com — principles only, nothing copied): both keep chroma for *one* job each (a signature accent, the status colours) on a broad neutral field and let photography carry the warmth. V5 does the same: the accent is the lagoon and nothing else; the tones exist only where a state is stated.

**21st.dev**: the primitives member's shortlist (`21st_primitives.md` §2A.2) rated every status-badge candidate and found their palettes «semantic green/red (coss, Astryx, HeroUI)» — refused for the same CR-11 reason. Nothing chromatic is imported from React code; the anatomy they kept (glyph + word, 1 px edge, tinted body) is what the tones below paint. Classification of this whole document: **A**.

---

## 3. The materials — the primary palette and the neutrals

Five materials, all Italian words, none of them a UI colour name:

| Material | Role | Steps (primitive `--p-*`) | Provenance |
|---|---|---|---|
| **carta** — the paper | pages, areas, sheets, raised, disabled, rhythm lines | 0 `#ffffff` · 25 `#fbfaf8` · 50 `#f4f3f0` · 100 `#ecebe6` · 150 `#e3e2dd` · 200 `#d3d2cc` | V2 `--min-3/2/0/1`, V4 `--surface-disabled`, `--hairline` — **unchanged hex** |
| **inchiostro** — the ink | text 1/2/3, structural lines | 900 `#15222a` (14.62 on carta-50) · 600 `#4a5a62` (6.46) · 500 `#55646b` (5.48) · 400 `#7a868b` (3.37, a component edge) | V2 `--ink`, `--ink-2`, `--ink-3`, `--hairline-strong` — unchanged |
| **notte** — the night, evolved from `--brand-navy` | dark chapters, rail, footer, tooltips, hero | 950 `#071226` · 900 `#0b1a33` · 850 `#10233f` · 800 `#16304f` · 700 `#1d3b5e`; text on night 50 `#eef1f6` (15.33 on 900) · 200 `#b9c5d6` (9.94) · 400 `#8a9bb3` (6.13; text only on 900/850) | V4 `--mid-0…4`, `--on-dark*` — unchanged |
| **laguna** — the one interactive accent | links, primary action, current location, focus, selection wash | 700 `#0f6a72` text (5.69 carta-50) · 800 `#0b555c` hover (7.67) · 650 `#12777f` mark and gradient top (4.76) · 600 `#15808a` hover top · 550 `#1d8a93` ring (3.70) · 400 `#7fd1d8` on night (9.93) · 350/300 dark gradient · 100/50 washes | V4 `--accent*` family — unchanged |
| **oro** — the key | the seal's glyph on navy, identity text on night | `--brand-gold #c39a2b` (5.80 on brand navy, 6.59 on notte-900; **2.37 on paper: ornament only, never a word**) · `--p-oro-300 #dfc176` text on night (9.94 on notte-900, 7.66 on notte-800) | brand (locked, v2/tokens.css) + one new light step |

**The brand and the tricolour.** `--brand-green`, `--brand-navy`, `--brand-red`, `--brand-gold` stay declared once, in `v2/tokens.css` (the test forbids a second declaration; the V5 file only *references* them). Where the tricolour is allowed: the mark (verbatim), the wordmark (three coloured words — the owner has not authorised removing its font), and **one** 3-segment filet (green · paper · red, 12 × 2 px) beside the title of the *institutional* notice (see `specimen_1440.png` §5). Nowhere else: not on a control, not on a state, not as a section colour. «The Italian language of the logo as accents, not as UI noise» is that filet, the navy disc of the seal and the gold key on it.

**Status ≠ accent ≠ brand** (`verify_out.md`, ΔE OKLab): every tone mark is ≥ 0.066 from the accent (the nearest, deposito, is a grey), ≥ 0.104 from the brand navy, ≥ 0.083 from the brand red (cotto is the nearest and is visibly orange-brown), ≥ 0.137 from the brand green, ≥ 0.104 from the gold (ambra is the nearest; it is darker and less yellow). No state can be mistaken for a link, and no state wears the flag.

**What is retired** (§11 gives the aliases): `--ok-700/300/100` (green), `--err-700/300/100`, `--pending-700/300`, `--seal-600/300/100` (bronze), the V1 `--state-*` block, `--rubric` as an accent (the shim), and the V1 paper family.

---

## 4. Depth, surfaces, glass — and the night

Five depths on paper and five on night, the V4 levels kept, now named by what they are:

| Semantic | Paper | Night | Note |
|---|---|---|---|
| `--surface-page` | carta-50 | `--surface-night` notte-900 | canvas |
| `--surface-area` | carta-100 | `--surface-night-area` notte-850 | section grounds, table heads, control tracks, rail hover |
| `--surface-sheet` | carta-25 | `--surface-night-sheet` notte-800 | cards, panels, rows; active rail item, tooltip |
| `--surface-raised` | carta-0 | `--surface-night-raised` notte-700 | popover, menu (+ `--shadow-3`) |
| `--surface-hover` | `#f2f4f3` (4 % laguna in carta-25, frozen; ink 14.69) | — | row hover |
| `--surface-selected` | laguna-50 | — | selection, BRAND ground |
| `--surface-disabled` | carta-150 | — | ink-3 on it 4.73 |
| `--surface-night-deep` | — | notte-950 | utility bar, footer, scrim base |

Lines: `--line-rhythm` carta-200 (decorative, 1 px), `--line-structure` inchiostro-400 (≥ 3.13 on every paper), `--line-night` rgba(214,226,228,.45) — a component edge on **every** night level, composited on its own ground: 3.62 / 3.52 / 3.27 / 3.02 on 900 / 850 / 800 / 700 (a stronger second line was tried and found unnecessary).

Glass, mesh, shadows: unchanged from V4 (`--glass-light .85` → ink 15.42 on the worst composite; `--glass-dark .55` → on-dark 13.92; `--mesh-dark` navy 22 % + teal 8 %; six shadow roles, alphas doubled on night). Photography: text over a photograph needs `--scrim-photo-aa` rgba(11,26,51,.64) where the words sit (on-dark 4.5:1 against a **white** pixel) or `--scrim-photo-aaa` .76 (7:1); V4's `--grad-photo-dark` at .45 does **not** reach AA on a white pixel (verify_out.md, «V4 --grad-photo-dark»), which is why the hero H1 must keep sitting on the mesh, not on the photograph.

**Dark surfaces are contexts, not a theme.** V5 does not propose `prefers-color-scheme: dark` for the whole product (no research base, no owner request, doubled QA). Night is where V4 already puts it — hero, process, forum, rail, footer, tooltips, the login's left panel — and every token has its night counterpart so those contexts are complete: text (3 steps), accent, focus, lines, the eight tones (night body 900, night word 300, night mark 400), icons, discs.

---

## 5. One family, two shells — public site and platform

The owner asked for «public vs platform variants of one family». The proposal (`tokens-v5-colour.css`, last block; `specimen_shells.png`):

| | Portico (public) | Console (platform) |
|---|---|---|
| page | carta-50 warm stone | **carta-25** |
| area | carta-100 | **carta-50** |
| sheet | carta-25 | **carta-0 white** |
| raised | carta-0 (+ shadow) | carta-0 (+ shadow-3: depth by shadow, not by colour) |
| actor disc | carta-100 | carta-100 (keeps one step of relief on white) |
| chrome | letterhead glass, night chapters, photographs | night rail, glass context bar, night footer — unchanged |
| chroma | the accent, the key, photography; tones only where a state is stated (badges «à venir») | the accent and the tones, in chips, strips, deadlines, nodes; no photograph on operational screens |

Why one step lighter: a data sheet becomes white paper on a pale desk — rows, chips and document previews sit on the brightest ground, the night chrome frames it, and the console stops looking like a public page with a sidebar. Same primitives, **no new hex**; the selector is `body.console` (already set by `base_portal.html` and `base_companies.html`) with `.shell-console` for showcases. Every tone word and mark was re-checked on the white sheet and its hover (verify_out.md «console shell»: words 6.13 → 14.12, marks 3.74 → 10.84; text-3 on carta-25 5.88; focus ring on white 4.11). This is an owner decision (§14 D1): V4 DS §1.4 froze `--min-0` as the operational canvas.

---

## 6. The status system — registers, tones, glyphs, patterns

### 6.1 Registers → tones

A **register** is what a chip asserts (Python, `apps/core/chips.py`, reaches the DOM as `data-register`); a **tone** is the material that paints it. V5 keeps the six registers and adds two — `esame` and `blocco` — because two states the owner listed were sharing a register with a different meaning:

| Register | Asserts | Tone | mark 600 (OKLCH) | body 50 | word 800 | edge style | pattern (strip, legend) |
|---|---|---|---|---|---|---|---|
| `conforme` | the piece received is the piece asked; a step is done — **a fact, never a verdict** | **registro** lapis | `#284b8f` L .42 C .120 h 262 | `#e6efff` | `#1d3f82` | solid | solid |
| `esame` **new** | in the hands of an intervener: it moves without you | **esame** wisteria | `#8b67bc` L .59 C .131 h 302 | `#f2eaff` | `#5e3d87` | solid | solid |
| `neutro` | a fact is recorded; nobody must act, nobody judges | **deposito** cool slate | `#586674` L .50 C .028 h 248 | `#eaeff4` | `#434f5c` | solid | solid |
| `attesa` | something is due, from someone, and is not late | **ambra** | `#aa7600` L .60 C .126 h 78 | `#ffeccf` | `#694700` | **dashed** | **hatch** |
| `azione` | the file does not advance until a named actor acts, now | **cotto** terracotta | `#aa4300` L .52 C .149 h 44 | `#ffe9e0` | `#873300` | solid | solid |
| `rifiuto` | an act was refused, or the piece is invalid | **granata** garnet | `#932039` L .44 C .150 h 14 | `#ffe8e9` | `#830a2c` | solid | **dots** |
| `blocco` **new** | a dependency: heavy, not alarming | **grafite** | `#353e49` L .36 C .023 h 254 | `#e2e7eb` | `#242c35` | solid | **cross-hatch** |
| `nullo` | withdrawn, not applicable, archived: it carries nothing | **cenere** ash | `#7a868b` L .61 C .016 h 225 | `#f1f0ec` | `#55646b` | **dotted** | outline only |

How the tones were made (`tones_v5.py`, `gen_primitives.py`): each is a hue and two chromas; the body is L 0.95, the hover body L 0.918 at 1.35 × chroma, the word is the *lightest* L that keeps ≥ 7:1 on the body, ≥ 6.3:1 on the hover body and ≥ 7:1 on carta-100 (the darkest paper), the mark the lightest L that reaches its rung of the **luminance ladder** (below), the edge 34 % of the mark into the body, and the three night steps are solved against notte-900/800. Then frozen as hex — no `color-mix()` at runtime for a state colour, so a chip is one paint. (`refine_800.py` then pushed the words of registro and granata one step darker than their marks, so that word and mark are never the same hex.)

The ladder — marks on carta-100, the worst paper — is the second channel for a greyscale reader: nullo 3.13 · attesa 3.31 · esame 3.69 · neutro 4.93 · azione 5.00 · rifiuto 7.01 · conforme 7.05 · blocco 9.08. Heavier = more settled or more serious; the two lightest are the two «open» states.

Hue logic, so that nothing is random: the cool half (lapis 262 · slate 248 · graphite 254) is *the institution and the record*; wisteria 302 sits between the record and the person («someone is reading it»); the warm half (amber 78 · terracotta 44 · garnet 14) is *time and refusal*, in order of gravity; ash has no hue. No green anywhere; no yellow (amber is L .60 C .126 — a clear amber, not a highlighter); red only as garnet, deeper and less orange than V4's (h 14 vs 29, C .150 vs .178).

### 6.2 The eight document states

`documents.RequirementState` (seven members) + the Conditions gate `row.action_blocked` / `ChecklistStatus.blocked` = the owner's eight. Glyphs are one 16 px circle grammar (drawn in `specimen.html`'s sprite; final drawing belongs to the icon member, whose folder is still empty): **outline = open, filled = settled**.

| State | value | V4 today | V5 register | tone | glyph | pattern | why this and not that |
|---|---|---|---|---|---|---|---|
| VALIDÉ | `valid` | conforme = ink | conforme | registro | filled disc + check | solid | the record's ink; a check that *closes*; never green |
| EN EXAMEN | `in_review` | neutro (= DÉPOSÉ) | **esame** | esame | half-filled disc | solid | it moves, but not by you; distinct from DÉPOSÉ at last |
| DÉPOSÉ | `filed` | neutro | neutro | deposito | ring + centre dot | solid | a fact; the base line |
| MANQUANT | `missing` | attesa (= ink-2 dashed) | attesa | ambra | **dashed ring** | hatch | the shape of an absence; not a clock (a clock says «time», not «nothing here») |
| À REMPLACER | `to_replace` | attesa | attesa | ambra | two arrows in a ring | hatch | same register, its own glyph (the two share a colour on purpose: both are «due, not late») |
| EXPIRÉ | `expired` | azione (brown) | azione | cotto | filled disc + clock | solid | act now; a Mediterranean roof, not an alarm triangle |
| NON VALIDE | `invalid` | rifiuto (crude red) | rifiuto | granata | filled disc + × | dots | garnet; the reason is printed on the row |
| BLOQUÉ | `action_blocked`, `blocked` | attesa (= MANQUANT) | **blocco** | grafite | lock | cross-hatch | a dependency, heavy and calm; the row says what unblocks it |
| (retiré · sans objet) | `not_applicable`, `withdrawn`, `archived` | nullo | nullo | cenere | slashed ring | outline | carries nothing |

Divergence to settle with the primitives member (§14 D6): `21st_primitives.md` §2A.2 keeps the sprite icons (clock for MANQUANT, search for EN EXAMEN, warning for EXPIRÉ). The circle grammar above was chosen because it stays legible at 14 px inside a 24 px pill in Arabic and in a dense table, because it makes *open vs settled* visible without colour, and because a warning triangle is the reflex the owner called crude.

### 6.3 Case and process states

Rule for every producer in `chips.py` (53 members): *every* `in_review`, `under_review`, `assigned`, scan `pending`, `in_progress` becomes **esame**; *every* `blocked` becomes **blocco**; the rest is unchanged. The enums the owner named, in full:

| `cases.CaseStatus` | V5 register | tone | glyph |
|---|---|---|---|
| draft | attesa | ambra | dashed ring |
| oriented · training · selection · admin_process · pre_departure · entered · post_entry | neutro (+ `data-stage` 1/2/3 unchanged) | deposito | ring + dot |
| review_required · suspended | azione | cotto | clock |
| closed | neutro («a file can close without success: never a verdict») | deposito | ring + dot |

| Producer | Members → V5 register |
|---|---|
| `cases.ChecklistStatus` | pending → attesa · in_progress → **esame** · done → conforme · not_applicable → nullo · blocked → **blocco** |
| `cases.AssessmentOutcome` | possible → neutro + `chip--indicative` (dotted, no body) · missing_requirement → attesa · warning → attesa · stop → **blocco** (an obstacle, not a refusal by the platform) · review_required → azione |
| `accounts.VerificationStatus` | approved → conforme + `chip--seal` (navy disc, gold shield) · pending → **esame** (a human is checking; today attesa) · rejected → rifiuto · not_required → **nullo** (today neutro) |
| `documents.ScanStatus` | pending → esame · clean → neutro · infected → rifiuto · error → azione · not_configured → **nullo** (today neutro) |

The three re-mappings marked «today …» are proposals for the domain owner (§14 D5).

### 6.4 The chip, the strip, the legend, the night

The chip (`specimen.css` `.chip`, the reference for the V5 rewrite of `v3/chip.css`): pill `--radius-full`, 24 px (20 dense, 28 large), **1 px edge in the tone's 200**, body 50, glyph 16 px in the mark, word 13/20 500 in the tone's 800, `--chip-edge-style` per register. Modifiers: `chip--seal` (20 px navy disc, gold glyph 5.80:1), `chip--indicative` (transparent body, dotted edge — «à titre indicatif», public site), a `button.chip` for filters (hover body 100).

Strips and legends (HealthStrip, `seg__dot`) paint the **mark** and the **pattern** (`--pattern-hatch`, `--pattern-dots`, `--pattern-cross`, white over the mark) — the same textures V4 already draws for the jurisdiction bar, extended to eight.

Night contexts (`.on-inverse`, `.rail`, `.tooltip`, `.site-footer`, all existing classes): the same registers flip to the night steps — body 900, edge = mark 400, word 300 (≥ 7.01 on the night body, ≥ 5.50 mark on notte-900, ≥ 4.24 on notte-800).

Forced colours: tones yield to `Canvas`/`CanvasText`, `nullo` to `GrayText`; glyph, edge style, pattern and word remain — the state is still readable.

---

## 7. Deadlines, journey nodes, notices, the seal

- **Deadline ladder** (owner directive §19, «never all red»): normal → text-2 / mark text-3; upcoming → text-1 (500) / text-2; soon → ambra word + mark; overdue → cotto word + mark (600). Four steps, two hues, no red: the garnet is for refusal, not for lateness.
- **Journey nodes**: done = registro-600 disc with white check (8.42:1 glyph); current = laguna-700 ring 2 px + laguna-50 halo 5 px («vous êtes ici»); next = inchiostro-400 outline (3.37) + text-3 numeral; blocked = grafite-600 disc with cross-hatch and lock. The past is the record's ink, the present is the accent, the future is paper.
- **Notices** (five kinds, five materials): a *sheet* with a quiet wash at step **25** (not 50: a large candy panel is what made V1 read as a template — `sc_states_chips.png`), a 3 px rule and a 20 px glyph in the mark, a title in the tone's word, **body text in ink**. info = registro (a fact), pending = esame (an intervener), warning = ambra (due), error = granata (refused / form error), institutional = carta-100 wash, navy glyph, **gold 3 px rule** (`--notice-institutional-rule`: identity ornament, 2.20 on carta-100; the boundary is the hairline and the wash), tricolour filet beside the title. Ratios: titles 7.68 – 13.59 (AAA on every body), rules/glyphs 3.63 – 12.78. `info` and `success` remain one material by design (a finished step is a fact).
- **The seal** (an authority's stamp): `--seal-disc` brand navy, `--seal-glyph` brand gold (5.80). Bronze is retired: the seal was the only bronze.

---

## 8. Icon colour rules

An icon is a glyph in `currentColor` (`base.css`: `fill: none; stroke: currentcolor`, the sprite hard-codes nothing). It takes **one** of these and never a brand colour — the tricolour lives in the mark, the gold in the key:

| Token | Value | Where | Worst paper / night |
|---|---|---|---|
| `--icon-default` | text-2 `#4a5a62` | beside a label, in a control, in a row, the rail on paper | 5.52 (carta-150) — AA as text, AAA-graphic |
| `--icon-muted` | text-3 `#55646b` | meta, secondary rows, folio | 4.73 |
| `--icon-strong` | text-1 | a title's glyph, the selected item | 12.50 (carta-150) |
| `--icon-interactive` | laguna-650 `#12777f` | a link's or an action's glyph; the ghost button | 4.07 (carta-150) · 4.43 (carta-100) |
| `--icon-status` | `currentColor` | a status glyph: painted by its chip (`--chip-mark`), notice, deadline, node | by the tone (≥ 3.02, and ≥ 4.62 in hover except attesa 3.10 / esame 3.42) |
| `--icon-disc-bg` / `-fg` | carta-100 / text-2 | the 24 / 32 / 40 px disc behind an actor glyph (person, authority, company…) | 6.00 |
| `--icon-on-night` / `-strong` / `-muted` | notte-200 / notte-50 / notte-400 | rail, footer, tooltips, hero | 6.53 (notte-700) / 10.08 / 5.56 (muted: notte-900/850 only) |
| `--icon-disc-night-bg` / `-fg` | notte-800 / notte-200 | the disc on night | 7.65 |

Rules: (1) an icon never carries a meaning its label does not carry; (2) the accent on an icon means *interactive*, so a decorative icon is never laguna; (3) a status glyph is never coloured by the template — the chip's register does it; (4) the four route colours (`--route-*`) stay V4 and are never alone (index + glyph + word); (5) in a night context, an icon takes the night token, never a lightened paper token; (6) `forced-colors`: nothing to do, `currentColor` follows.

---

## 9. Focus ring

One ring, three contexts, every ground verified:

- **Paper**: `--focus-ring` laguna-550 `#1d8a93`, 2 px, offset 2 px, halo 5 px at 30 % (`--focus-halo`); 3.70 on carta-50, 3.94 on carta-25, 4.11 on white, 3.44 on carta-100, 3.41 on laguna-50, 3.07 on laguna-100 (the SOFT hover) — ≥ 3:1 everywhere (WCAG 2.2 2.4.11/2.4.13: 2 px perimeter, 3:1 state contrast).
- **Night**: `--focus-ring-night` laguna-400 `#7fd1d8`, 6.53 – 9.93.
- **Photograph**: a two-tone ring, inner white / outer notte-900 (`--focus-ring-image-*`, 15.33 between them): whatever the pixel under it, one of the two is ≥ 4.16 against it.
- The V4 names `--focus-ring-color/-width/-offset` keep pointing at the same values, so every `:focus-visible` in the cascade already draws this ring (gate D correction 9).

---

## 10. The contrast proof — key tables, and the honest weak points

`verify_out.md` (generated by `verify_tokens.py` from the CSS file, not from a spreadsheet) holds **363 pairs, 0 below minimum**: every text/ground and glyph/ground of every tone on the five papers (carta-0/25/50/100 and the hover), on the three nights (900/850/800) and on its own bodies; the neutrals, accent, lines, focus; identity, seal, scrims; notices, deadlines, nodes; icons; the console shell. The eight tones, floored:

| register | word / body | word / hover | word / carta-100 | mark / body | mark / hover | mark / carta-100 | night word / night body | night mark / notte-900 | night mark / notte-800 |
|---|---|---|---|---|---|---|---|---|---|
| conforme | 8.70 | 7.91 | 8.43 | 7.28 | 6.62 | 7.05 | 7.05 | 5.53 | 4.26 |
| esame | 7.21 | 6.54 | 7.05 | 3.77 | 3.42 | 3.69 | 7.01 | 5.54 | 4.27 |
| neutro | 7.22 | 6.57 | 7.00 | 5.08 | 4.62 | 4.93 | 7.02 | 5.51 | 4.24 |
| attesa | 7.25 | 6.57 | 7.03 | 3.42 | 3.10 | 3.31 | 7.03 | 5.51 | 4.25 |
| azione | 7.18 | 6.49 | 7.02 | 5.12 | 4.62 | 5.00 | 7.02 | 5.51 | 4.24 |
| rifiuto | 8.78 | 7.92 | 8.60 | 7.17 | 6.46 | 7.01 | 7.06 | 5.52 | 4.26 |
| blocco | 11.34 | 10.33 | 11.83 | 8.70 | 7.93 | 9.08 | 7.80 | 6.01 | 4.63 |
| nullo | 5.38 | 4.95 | 5.14 | 3.28 | 3.02 | 3.13 | 7.06 | 5.50 | 4.24 |

Words are AAA (≥ 7:1) everywhere except `nullo` (AA by design: it carries nothing and must read as lighter); marks are ≥ 3:1 (graphic) everywhere, ≥ 4.5 for the five «settled» tones.

**Separation** (ΔE OKLab after Machado 2009 simulation at severity 1.0, `verify_out.md` §Separation):
- marks: worst pair rifiuto / blocco under protanopia 0.030 — separated by pattern (dots vs cross-hatch), glyph (× vs lock); the greyscale ladder is close there too (ΔY 0.028), so **the glyph and the pattern are load-bearing for that pair**; every other pair ≥ 0.054 in every simulation;
- words: attesa / azione under deuteranopia **0.015** (`#694700` vs `#873300` become near-identical browns) — the two words differ, the marks (3.31 vs 5.00 on paper), the glyphs (dashed ring vs filled clock) and the patterns (hatch vs solid) separate them; this is the price of keeping both in the warm half, accepted knowingly;
- bodies: conforme / esame 0.001 under deuteranopia — two washes; the body is never the channel.

**Other honest limits of the numbers**: `attesa` mark on its hover body 3.10 and `esame` 3.42 are graphic-minimum figures (glyph and edge, never text); `--icon-interactive` on the disabled surface is 4.07 (a disabled control shows no interactive icon anyway); gold on paper is 2.37 and is therefore ornament only; the V4 `--grad-photo-dark` fails AA on a white pixel (4.5 needs α .64) — a V4 defect to carry to the hero and performance members.

---

## 11. The tokens — architecture, wiring, tests

**Three layers, one direction of reference** (`tokens-v5-colour.css`):

1. **Primitives** `--p-<material>-<step>` — raw hex, never read by a component (carta, inchiostro, notte, laguna, oro, registro, esame, deposito, ambra, cotto, granata, grafite, cenere).
2. **Semantic** `--surface-*`, `--text-*`, `--line-*`, `--accent-*`, `--focus-*`, `--icon-*`, `--identity-*`, `--scrim-*`, `--tone-<register>-{bg, bg-hover, edge, mark, text, night-bg, night-text, night-mark}`, `--pattern-*`.
3. **Component** `--chip-*` (re-pointed by `[data-register]` and by the night contexts), `--deadline-*`, `--node-*`, `--seal-*`, `--notice-*`; plus the two-shell block and the forced-colours block.

**Wiring plan** (for whoever implements; nothing was touched):

1. Add the file as `static/css/v5/tokens.css`, loaded **after** `v4/tokens.css`; add it to `scripts/build_css.mjs`'s entry (bundled into `dist/main.css`).
2. In the same commit turn the V4 names into aliases with the same hex: `--min-0: var(--p-carta-50)` … `--ink: var(--p-inchiostro-900)` … `--mid-1: var(--p-notte-900)` … `--accent: var(--p-laguna-700)` … `--accent-ring: var(--p-laguna-550)` … `--edge-dark: var(--line-night)`. No component changes value; `test_v4_tokens.py`'s ratio table still passes because the hex is identical.
3. Retire with a one-release shim: `--err-700: var(--tone-rifiuto-mark)`, `--err-300: var(--tone-rifiuto-night-text)`, `--pending-700: var(--tone-attesa-mark)`, `--pending-300: var(--tone-attesa-night-text)`, `--seal-600: var(--seal-disc)`, `--state-info-*/done-*` → `--notice-info-*`, `--state-warn-*` → `--notice-warning-*`, `--state-error-*` → `--notice-error-*`, `--state-pending-*` → `--notice-pending-*`; **delete** `--ok-*`; re-point the legacy `--color-accent-600/700` and `--border-accent` from `--rubric` to `--accent-text` (42 sites, each to be looked at: an «accent» that was red is either a link or an order rule).
4. `apps/core/chips.py`: `REGISTERS += ("esame", "blocco")`; the mapping diff of §6.3; `GLYPH` re-keyed to the eight glyph names and **rendered** (today it is not) — the template writes `data-register` and the glyph, never a colour.
5. `v3/chip.css` → V5 chip (the specimen's `.chip` block); `v4/workspace.css` HealthStrip, `seg__dot`, deadlines, journey → the tone / deadline / node tokens; `components.css` notices → the notice tokens.
6. Tests: keep `test_no_register_is_painted_with_the_verdict_green_or_the_accent` (still true: tones are neither `--ok-*` nor `var(--accent)`); keep «brand declared once» (V5 references, never declares); add `tests/frontend/test_v5_tokens.py` = `verify_tokens.py` in pytest form (363 assertions); add a test that no `[data-register]` chip is rendered without its glyph.
7. Re-measure every page a shared sheet touches before committing (project memory: two regressions came from un-measured one-liners) — chips appear on 65 sites / 33 templates.

Cost: ≈ 13 KB of custom properties once comments are stripped (2.7 KB gzip, measured), zero JavaScript, no runtime `color-mix()` for states, no extra request. Performance budget untouched.

---

## 12. Classification

Everything in this document is **A — adapt to Django + CSS**. No pattern needs Motion (**B**) — a state *change* choreography is the primitives member's (crossfade, glyph draw) and uses these tokens unchanged; nothing needs a React island (**C**); the traffic-light palettes, the `#DC2626` reds and the semantic-green badge libraries are **D — rejected** under CR-11.

---

## 13. What I could not do, and why

- **No wiring, no live measurement on the application**: the repository is read-only in this phase; the tokens were verified by computation and on a specimen page (Chromium via Playwright, 1440 and 390), not inside the console. The first wired page must be re-probed.
- **No user testing with colour-blind readers**: separation is Machado-simulated (deutan, protan, tritan, severity 1.0) and greyscale-checked, not observed.
- **No dark theme**: night is a set of contexts (§4); a full `prefers-color-scheme: dark` is out of scope and UI-UX-Pro-Max returned no guidance for it («no database match» for «dark mode», stated explicitly).
- **Glyphs are drafts**: the eight-state circle grammar is drawn in the specimen's inline sprite (16 px); the icon member owns the final drawing and the sprite (`static/img/icons.svg`), and their folder is empty at the time of writing.
- **The deuteranope word pair** attesa / azione (ΔE 0.015) could only be widened by moving one of the two out of the warm half; I chose to keep the «time» family coherent and to lean on glyph and pattern. The owner may prefer the other trade.
- **The gold** cannot be made a text colour on paper (2.37 – 2.63) without ceasing to be the brand's gold; `oro-300` exists only for night.
- **Arabic**: colour is direction-agnostic; the chip's glyph sits at inline-start and patterns are symmetric — checked by reasoning, not by an RTL capture of the specimen.
- The forum banner defect (1.46:1) and the photo scrim (α .45 < AA) are V4 defects **reported**, not corrected (read-only).

---

## 14. Decisions for the owner

| # | Decision | My recommendation |
|---|---|---|
| D1 | Console one step lighter (page carta-25, sheet white) vs V4's `--min-0` canvas | lighter (§5); it is the cheapest «premium» move in the system |
| D2 | VALIDÉ in the institution's lapis (chromatic, never green) vs V4 «ink without chroma» | lapis; CR-11 is kept (no verdict colour, no green anywhere), the state becomes visible; legal to confirm the wording «la couleur du registre, pas d'une décision» |
| D3 | EN EXAMEN in wisteria — the one hue that is neither the record nor the warm half | yes; it is the state users wait on most and it was invisible |
| D4 | Retire `--ok-*` green, bronze seals, the pending brown and the rubric-as-accent shim | yes, with the one-release aliases of §11 |
| D5 | Re-map `VerificationStatus.pending` → esame, `not_required` → nullo, `ScanStatus.not_configured` → nullo, `AssessmentOutcome.stop` → blocco | yes; domain owner to confirm the readings |
| D6 | Glyphs: circle grammar (this document) vs sprite icons (primitives member) | circle grammar for the eight states; sprite icons for everything else |
| D7 | The tricolour filet on the institutional notice (the only tricolour outside the brand lock-up) | keep it, and nowhere else |
| D8 | Two new registers in Python (`esame`, `blocco`) — a `chips.py` change and 65 template sites to re-check | yes; the mapping is data, the templates do not change |
