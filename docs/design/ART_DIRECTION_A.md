# ART DIRECTION A — European Institutional Editorial

**Direction key:** `A` · **Codename:** *Le Registre* · **Date:** 20 September 2026 · **Status:** proposed art direction, complete and buildable · **Scope:** public site + authenticated platform, fr / it / en / ar

This document is the brief. A designer and a Django/CSS engineer should be able to build from it without asking a question. Where a value is given, it is the value. Where a value must be verified in the browser before it is frozen, the verification is specified.

---

## 1. The idea

**Italy Legal Entry is a register.** Not a brochure, not a service, not a dashboard: a numbered, dated, sourced record of what the regular routes to Italy are, who is responsible at each step, and what this organisation does and does not do. Everything on the site therefore has three properties, and the design makes all three visible at once: a **position** (an ordinal — §01, step 04, entry 07), an **authority** (a named responsible actor — *entreprise*, *institution*, *autorité consulaire*, *Équipe AGAMI*), and a **date or source** (a revision date, a ruleset version, a legal reference). The graphic consequence is an editorial page with a real apparatus: a left **folio rail** carrying the ordinal and the running head, a measured reading column, and a right **margin** carrying the note, the date, the caveat and the source. The page is dense because a register is dense; it is calm because a register does not argue, it records. Photography is rare and large and captioned like an archive plate; the rest of the time the page is carried entirely by type and by a four-weight rule system. Red — **rubric** — marks order and nothing else, which is what red has meant in legal and administrative registers since before print. The authenticated platform is the same register in working form: the case file is literally a dated, numbered, attributed record, so the platform needs no new visual language at all, only a different tuning of this one.

**The sentence a stakeholder says:** *"It looks like something an institution publishes — at a glance I can see what is numbered, who is responsible, and where it comes from."*

**What this direction is not.** It is not a magazine and not a newspaper. There is no masthead flourish, no drop cap, no multi-column newspaper text, no pull-quote as decoration, no editorial "personality". The apparatus — folio, rule, margin, plate, source list — is borrowed from institutional publishing (a research institute's report, a code of practice, a bilateral agreement, an annual register), not from the press. An institution that publishes, not a publisher.

---

## 2. Grid

### 2.1 Breakpoints

Six named tiers. Breakpoints are content decisions, not device names. Each tier is **authored**, not derived by reflow.

| Tier | Range | Columns | Gutter | Outer margin | Container | Rail |
|---|---|---|---|---|---|---|
| `xs` | 320–429 | 4 | 12px | 20px | fluid | folio line (horizontal) |
| `sm` | 430–767 | 6 | 16px | 24px | fluid | folio line |
| `md` | 768–1199 | 12 | 24px | 40px | fluid | folio line |
| `lg` | 1200–1439 | 12 | 24px | — | **1176** | vertical rail, 2 cols |
| `xl` | 1440–1599 | 12 | 24px | — | **1320** | vertical rail, 2 cols |
| `xxl` | ≥1600 | 12 | 24px | — | **1440** | vertical rail, 2 cols |

Column widths are derived, not declared: `col = (container − 11 × gutter) / 12`. At `lg` = 76px, at `xl` = 88px, at `xxl` = 98px.

Three deliberate consequences:

1. **The container changes at every tier above 1200.** The current build freezes at 1200px and converts every pixel above 1440 into margin (measured: 1200@x=360 at 1920, 37.5% dead gutter — `home__1920x1080__fr.png` is `home__1440x900__fr.png` with wider white edges). Here, 1920 renders a 1440 container and the rail widens to 220px. Both benchmark systems do this: .italia reaches 1320 at XXL, ECL 1368 at XL.
2. **The rail changes state at 1200**, not the content. Below `lg` the rail's 176px is too narrow to set a 44px numeral, so the folio becomes a horizontal line above the block. The device survives at every width; only its axis changes.
3. **No `clamp()` on display type or containers.** Fluid interpolation is what flattened the current hierarchy (H2:lead falls from 1.62 at 1920 to 1.35 at 390). Sizes step at breakpoints so the ratio is designed at each width.

### 2.2 The three zones

At `lg`+ every band is composed from three zones on the 12-column grid:

```
│ RAIL          │ CONTENT                       │ MARGIN   │
│ cols 1–2      │ cols 3–9                      │ cols 11–12
│ 200px @ xl    │ 760px @ xl                    │ 200px @ xl
│ ordinal       │ title, prose, register,       │ note,
│ running head  │ table, sequence               │ date,
│ local index   │                               │ source,
│ breadcrumb    │                               │ caveat
```

Column 10 is a **fixed empty channel** (88px at `xl`). It is not wasted; it is what makes the margin read as a margin rather than as a second content column.

### 2.3 Content widths

| Token | Value | Grid slot | Use |
|---|---|---|---|
| `--width-prose` | **576px** hard cap | cols 3–8 at `lg`, cols 3–7 at `xl`/`xxl` | running text, the measured reading column |
| `--width-register` | grid-derived, cols 3–9 | 760px at `xl` | entry lists, tables, sequences, checklists |
| `--width-spread` | cols 1–12 | 1320px at `xl` | a register that runs the full container (rail empty, ordinals become the list's first column) |
| `--width-plate` | 100vw, no max | — | the one full-bleed band per page |
| `--width-form` | **528px** | cols 3–8, centred at `md`− | forms, account, login |
| `--width-margin` | cols 11–12 | 200px at `xl` | marginal notes at caption size |

The measure was never the problem — the emptiness beside it was. The current build sets every heading and lead at exactly 576px at x=152 inside a 1200px container, with nothing in the remaining 624px, for 1100px of scroll. Here the same 576px column is flanked by an ordinal, a running head and a margin apparatus. The column is identical; the page is not.

**Verification gate.** `--width-prose` is a pixel value targeting **62–68 characters of French at prose size**. Before freezing, measure the average lowercase advance of the shipped serif at 17px in Chromium and adjust the pixel value. Do not express it in `ch` — the current `68ch` token renders 81 characters, a 19% miscalibration.

### 2.4 When a section may break the grid

Four permitted breaks, and no others. A page may contain **at most two**.

1. **PLATE** — a band goes full bleed (100vw, no container). Permitted **once per page**, on the page's Rank A section only. It must carry a folio in the rail or folio line, and if it is photographic it must carry a caption.
2. **SPREAD** — a register (entry list) runs cols 1–12 instead of 3–9. Permitted only when the rail is empty for that band, because the list's own ordinals take over the rail's job.
3. **INSET** — a notice or a legal statement indents to cols 4–9 (at `xl`: starts at x=+112 relative to content, 584px wide). Used to make a caveat read as an interruption inside the argument.
4. **MARGIN PROMOTION** — a marginal note with no host block occupies cols 10–12 as a standing note beside a plate. Used for the anti-fraud statement in the home hero, and essentially nowhere else.

A section that does none of these is a **standard band**: folio in rail, content in cols 3–9, margin in 11–12. Most sections are standard bands. The breaks are events.

---

## 3. Typography

### 3.1 Families

| Role | Family | Licence | Files shipped |
|---|---|---|---|
| Display + prose (Latin) | **Newsreader** — Production Type, Paris | OFL | variable roman (`wght` 200–800, `opsz` 16–72) + variable italic — 2 woff2 |
| Interface (Latin) | **Fira Sans** — Erik Spiekermann / Carrois Apostrophe | OFL | 400, 500, 600 + 400 italic — 4 woff2 |
| Display + prose (Arabic) | **Noto Naskh Arabic** | OFL | variable (`wght` 400–700) — 1 woff2 |
| Interface (Arabic) | **IBM Plex Sans Arabic** | OFL | **one** variable woff2, `font-weight: 100 700` |
| Reference codes, case numbers | **Fira Mono** | OFL | 400 — 1 woff2 |

All self-hosted, subset by `unicode-range` per script, `font-display: swap`, no third-party request. `font-synthesis: none` globally — no faux bold, no faux italic, in any script.

### 3.2 Why these and not the incumbents

**Against IBM Plex.** ADR-008 justifies Plex as "an institutional European voice, distinct from gov.it (Titillium)" — the stated criterion is avoiding gov.it, not achieving distinction. IBM Plex was commissioned by IBM as the corporate voice of a technology company and is the most-deployed open "serious tech" superfamily of the last decade; it is the default suggestion of almost every tool asked for an institutional open pairing, which is the mechanism behind the client's phrase *"a standard AI-generated website"*. Beyond taste, three concrete deficits: (a) **no optical size axis** — the same outlines run from 12px to 64px, a 5.3× range, which is why the 48px H1 reads soft and inflated; (b) **no true small caps** in any Plex family, so the system substitutes `text-transform: uppercase` at 12px with 0.12em tracking in 22+ rules — the SaaS eyebrow the client banned; (c) **lining figures only**, so dates punch holes in lowercase prose. Separately, `--font-mono: "IBM Plex Mono"` is declared and no Plex Mono file exists, so the technical register is currently Consolas on Windows and Menlo on macOS — three textures for one role.

**For Newsreader.** It carries a real `opsz` axis from 16 to 72 in one file: the 88px plate and the 17px prose are *different drawings*, which is exactly the deficit above. It was drawn for on-screen reading with a large x-height, which is what allows this direction's central move — setting the running text in the serif rather than the sans. It has true italics (not obliques) and a full Latin-Extended coverage for French and Italian diacritics. It is not in the default institutional-open-source suggestion set, which is the point.
*Fallbacks if Newsreader fails the legibility QA in §3.7:* **Spectral** (same foundry, OFL, 7 weights + italics, true small caps, no variable axis) or **Literata** (TypeTogether, OFL, variable `wght` + `opsz` 7–72).

**For Fira Sans.** Humanist skeleton, drawn by Spiekermann/Carrois for a UI at small sizes; it does not read as a Silicon Valley grotesque. Full Latin-Extended. Avoid Inter, Source Sans, Public Sans, Work Sans, Roboto — all as unmarked as Plex; avoid Titillium Web outright (§5.6, impersonation).

**For Noto Naskh Arabic.** A true Naskh is the correct cross-script counterpart to a Latin serif and is the register Moroccan administrative documents use. IBM Plex Sans Arabic's Kufi-influenced construction is a register mismatch against a serif — and today it is doing *all six* Arabic levels, so the Arabic edition has no display/text contrast at all (`document.fonts.check('400 16px "IBM Plex Serif"')` returns **false** on every `/ar/` page). Plex Sans Arabic stays as the Arabic interface face: it is already subset, already weight-matched to Plex Sans within 3%, and its job here is labels, buttons, tables and forms, where a Kufi construction is correct.

### 3.3 The Latin scale

Ten roles. Four display, four text, two interface. Every line-height is a multiple of 4px. **Prose size never changes across breakpoints** — only the display sizes and the measure change.

| Token | Role | xs 320–429 | sm 430–767 | md 768–1199 | lg 1200–1439 | xl/xxl ≥1440 | Family / weight |
|---|---|---|---|---|---|---|---|
| `--t-plate` | the one display line on a page | 40/44 | 46/52 | 60/64 | 76/80 | **88/92** (104/108 ≥1600) | Newsreader 400, `opsz` 72, `-0.02em` |
| `--t-title` | page H1 | 32/40 | 34/40 | 42/48 | 48/52 | **52/56** | Newsreader 400, `opsz` 48, `-0.015em` |
| `--t-band` | section H2 | 28/36 | 28/36 | 32/40 | 36/44 | **38/44** | Newsreader 400, `opsz` 36, `-0.01em` |
| `--t-entry` | H3 / an entry's title | 20/28 | 20/28 | 21/28 | 22/28 | **22/28** | Newsreader 500, `opsz` 24, 0 |
| `--t-lead` | standfirst | 19/28 | 20/28 | 21/32 | 22/32 | **22/32** | Newsreader 400 italic optional |
| `--t-prose` | running body — **the serif** | 17/28 | 17/28 | 17/28 | 17/28 | **17/28** | Newsreader 400, `opsz` 18 |
| `--t-gloss` | secondary text inside an entry | 15/24 | 15/24 | 15/24 | 15/24 | **15/24** | Fira Sans 400 |
| `--t-caption` | marginalia, captions, credits | 13/20 | 13/20 | 13/20 | 13/20 | **13/20** | Fira Sans 400 |
| `--t-ui` | buttons, nav, labels, table cells | 15/20 | 15/20 | 15/20 | 15/20 | **15/20** | Fira Sans 500 |
| `--t-folio` | running head, small caps labels | 13/16 | 13/16 | 13/16 | 13/16 | **13/16** | Fira Sans 600, `+0.08em`, caps |
| `--t-numeral` | the rail ordinal | 22/24 | 24/24 | 28/32 | 40/40 | **44/44** | Newsreader 400, `tnum` |

**Ratios this produces.** At 1440: plate:band = 2.32, band:prose = **2.24**, band:gloss = 2.53, entry:prose = 1.29. At 390: band:prose = **1.65**. The current build measures band:prose = 2.11 at 1440 only because its "prose" is 16px sans; against its own 21px lead it is 1.61, and at 390 it collapses to 1.35. Benchmark floors: .italia H2 tops at 40px over a 16–18px body (≥2.2×); ECL desktop H2 36px over 16px = 2.25× at weight 400.

**Deleted tokens.** `--font-size-h4`, `--font-size-label`, `--font-size-button`, `--font-size-legal`, `--font-size-small`, `--font-size-eyebrow`. Four of these carry duplicate values today (14/14, 15/15) and `--font-size-h4` (18px fixed) is *smaller than the lead* at 1440 and 768 — a fourth heading level below a paragraph. Their jobs are absorbed by `--t-ui`, `--t-caption` and `--t-folio`.

**Four heading levels maximum per page** (.italia rule, adopted literally): `plate` or `title` (h1) → `band` (h2) → `entry` (h3) → and one optional `--t-folio` label acting as h4. A page that needs a fifth level has an IA problem, not a typography problem.

### 3.4 Measure and leading

Leading is bound to **measure**, not to a style name. The current system does the opposite: the 21px lead at 45–57 characters gets 1.7, while a 16px definition at **147 characters** gets 1.6 and 14px legal text gets a hard-coded 1.55.

| Measure | Size | Line-height |
|---|---|---|
| ≤ 45 characters (lead, standfirst) | 22px | 32px (1.45) |
| 62–68 characters (prose) | 17px | 28px (1.65) |
| ≤ 50 characters (gloss inside an entry) | 15px | 24px (1.60) |
| ≤ 34 characters (margin note) | 13px | 20px (1.54) |
| table cell | 15px | 24px |

**Hard cap: 68 characters everywhere, no exception.** Blocks that currently have no cap and must get one: `.glossary-entry__definition` (measured 147 characters), `.forum-programme__note` (101), `.home-reserved__body` (94), `.antifraud-panel__body` (80), `.page-section__text` (87), `.faq` answer panel (151, measured at `max-width: none`).

### 3.5 Case

**Capitalisation is a CSS decision, never a content decision.** Today 22 headings are typed in caps in the `.po` catalogue with computed `text-transform: none`, tracked at −0.48px, −0.34px, +0.65px, +1.04px or +1.63px depending on which file styled them — the same string, *"POURQUOI ITALY LEGAL ENTRY"*, is set at 33.76px/−0.34px on one page and 27.2px/+1.63px on another. Every uppercase string moves back to sentence case in the catalogues, and the design gets exactly **two** capital registers:

- `--t-folio` — 13px Fira Sans 600, `+0.08em`, uppercase, `font-feature-settings: 'case' 1`. The running head, the state chip, the table header, the actor label. This is the only tracked-caps object in the system.
- `.display--caps` — a display line set in caps, `+0.03em`, permitted **once per page at most**, and only on a plate.

Tracking tokens: `--track-plate: -0.02em`, `--track-title: -0.015em`, `--track-band: -0.01em`, `--track-normal: 0`, `--track-folio: +0.08em`, `--track-caps-display: +0.03em`. The single `--tracking-tight: -0.01em` applied across a 12–64px range and both cases is deleted.

### 3.6 Figures

`font-variant-numeric: tabular-nums lining-nums` as **one rule in base.css** keyed on `td, th, time[datetime], .folio__ordinal, .register__ordinal, .case-ref, .deadline, .amount` — not seven scattered component rules and zero in the three app stylesheets that render actual data. Oldstyle figures (`onum`) in running prose where the shipped face provides them; lining + tabular in every table and every ordinal. Slashed zero on reference codes. Western digits in Arabic (correct for Morocco), LTR-isolated with `<bdi>`.

### 3.7 Font QA gates (block release)

1. **Optical size** — render `--t-plate` and `--t-prose` from the same variable file and confirm the `opsz` axis is applied (stem contrast measurably different). If the browser ignores `opsz`, ship Spectral instead.
2. **Small caps** — `font-variant-caps: small-caps` must produce *true* small caps in the shipped Fira Sans build. If it synthesises, the `--t-folio` register stays tracked uppercase and no small-caps class is defined. Verify; do not assume.
3. **Oldstyle figures** — `font-variant-numeric: oldstyle-nums` must change the glyphs. If absent, prose uses lining and the token is deleted rather than left as a no-op.
4. **Ink parity Latin/Arabic** — measure rendered ink at 100px for 400/500/600 in both scripts; require agreement within **5%**. The current Plex/Plex-Arabic pair achieves 3%; a swap must not regress it.
5. **Legibility at 1× DPR** — read `--t-prose` on a 1× Windows display at 100% zoom and on a mid-range Android. A 17px serif is the single highest-risk decision in this direction; if it fails, raise to 18/30 and re-measure the column, do not fall back to sans.
6. **Payload** — total Latin-path woff2 ≤ **320 KB**. Today 153 KB of the font payload is duplicate: `ibm-plex-sans-400/500/600-normal-latin.woff2` are byte-identical copies of the same variable file (45,712 bytes each, md5 `b2c9031d…`).

---

## 4. Navigation

### 4.1 Utility bar — 36px, navy, not sticky

Three contents, in this order, and nothing else:

- **Promoter**, full, never truncated: `AGAMI — Dialogo Giuridico Interculturale APS · promoteur du projet` at `--t-caption` in `--paper-muted`. At `xs`/`sm` it **wraps to two lines**; `text-overflow: ellipsis` is forbidden on identity, legal and navigational text. (Today it is clipped to 38–44% of its length, and in Arabic the ellipsis falls at the *start*, so the word AGAMI is the part that disappears.)
- **Languages, inline, no dropdown**: `FR · العربية · IT · EN` at `--t-ui` 15px. Four options do not need disclosure. Arabic is second by decision: it is the script of the primary audience. Each carries `lang`, `hreflang` and `dir` on the label span only, so the row's grid does not break. Current language marked by a 2px rubric rule under the label, plus weight 600 — never colour alone.
- **Reserved area**: labelled link `Espace réservé`, with the lock glyph *and* the word at every width.

### 4.2 Masthead — 72px, paper, one 1px `--rule-ink` below

Opaque. **No `backdrop-filter`, no blur, no shadow, no scroll-shrink, no hide-on-scroll.** The current `.site-header::before` applies `backdrop-filter: saturate(140%) blur(8px)` behind a 94%-opaque veil at every viewport from 320 to 2560 — glassmorphism, banned by name, paid for in compositing, blurring nothing.

Contents: the **lockup** (§7.1) at the inline start; a **search field** at the inline end, present on every page in the same position (WCAG 2.2 §3.2.6 *Consistent Help*, and the site currently has zero site-wide search).

### 4.3 Primary navigation — 44px row under the masthead, two tiers

```
Personnes    Entreprises    Institutions    Universités et formation
                      Le modèle · Forum · Ressources · Le projet
```

**Line 1 is the four audiences and it is permanent in every gate state and every language.** Today Institutions and Universités disappear from the header *and* the footer while Phase 3 is closed, on a home page whose own section is headed "Quatre accès à l'écosystème — chaque acteur dispose de son espace". The gate must attach to the **destination**, not to the row: a `fallback_url_name` so Institutions resolves to the hub when open and to an honest interim page when closed. A compliance test asserts exactly four audience rows in header and footer, in both gate states, in four languages.

Line 2 is the institution's own voice: the method, the convening, the reference shelf, the project.

Current item: weight 500 → 600 **and** a 2px rubric rule below, **and** `aria-current`. Three signals, one of which survives greyscale and forced colours. Today it is colour + an animated bar, and the hover state and the current state are pixel-identical.

**Mega-menu:** a panel renders only when the item has **≥3 distinct destinations**; otherwise the top-level item is a plain link. It is anchored to its trigger. Today the "Personnes" panel is 576×211px containing two links that both point at the page you already clicked, mis-anchored 224px to the left of its trigger.

### 4.4 The running head — the sticky element

The masthead and nav row scroll away. After **400px** of scroll a single **48px running head** appears, sticky, paper ground, 1px `--rule-ink` below:

```
▤   Espace Personnes                    §03 LES PARCOURS RÉGULIERS      ⌕
```

Mark (24px) · page title (`--t-ui`) · **the current section's folio ordinal and running head** (`--t-folio`, updated by an IntersectionObserver over the section list) · search. This is the editorial running head applied to navigation, it is the direction's signature chrome, and it means the reader always knows their position inside the register.

**Sticky is bound to one measured token.** `--chrome-block-size` is computed in CSS from the real stack and consumed by the drawer, the overlay, `scroll-padding-block-start`, `scroll-margin` and every sticky sub-nav. No JavaScript writes geometry onto one element that its siblings also need. And: `@media (max-width: 79.999rem) { html.no-js .site-header { position: static } }` — today, without JavaScript, the header is **781px tall and sticky** at 390 and at 1024, so at 1024×768 the content is never visible at all.

### 4.5 Mobile — a drawer that is an index

`<dialog>` + `showModal()`: focus trap, Esc, `inert` background for free. Docked at the stuck chrome height. Enters `translateY(-100%) → 0` at 200ms `--ease-out`, exits 140ms `--ease-in`. Scroll lock uses `position: fixed; top: calc(var(--scroll-y) * -1)` with restore on close, not `body { overflow: hidden }` alone.

Contents — three register blocks, not an accordion:

```
01  Personnes                     →
02  Entreprises                   →
03  Institutions                  →
04  Universités et formation      →
────────────────────────────────────
    Le modèle · Forum · Ressources · Le projet
────────────────────────────────────
    Rechercher [                 ⌕]
    Contact · FAQ · Glossaire · Espace réservé
    FR · العربية · IT · EN
```

Today the drawer is 72% empty (208px of content in a 731px panel), offers four destinations, and two of the four audiences the home page names are absent from it entirely.

### 4.6 Breadcrumb

Derived from **the same menu tree as the navigation**, not per-view. Present only at depth ≥2. Current page last and unlinked (ECL). Set at `--t-folio` in the rail at `lg`+, above the title below `lg`. Collapses on `xs`/`sm` to the parent link only. Omitted entirely where the hierarchy is genuinely hub-and-spoke — a one-level `Accueil > Contact` stub is worse than nothing, and today *every* page renders exactly that while the header underlines a different parent.

### 4.7 Side navigation = the rail's local index

At `lg`+ the rail carries the section index for the current page:

```
01  Les parcours réguliers
02  Formation avant le départ
▌03 Diplômes et titres          ← current: 2px rubric rule + weight 600
04  Vivre en Italie
05  Questions fréquentes
```

Below `lg` it becomes a **44px horizontally-scrollable segmented rule** — not a cloud of 999px pills. (The portal's `.local-nav__link` is currently 34px on phone and tablet and 40px at 1280: the navigation gets *smaller* when you switch from a mouse to a finger.)

### 4.8 The platform shell — same family, different tuning

`templates/shell_platform.html`. Does **not** extend `base.html`. Today `base_portal.html` extends the public base, so a signed-in user's screen carries a 24-link public mega-menu and a 484px public footer beneath a 276px content box — the marketing furniture is 1.8× taller than the work.

| | Public | Platform |
|---|---|---|
| Top bar | utility 36 navy + masthead 72 paper + nav 44 | **one 44px navy bar**: mark · project · case reference · language · account · help · `← Site public` |
| Rail | local index, `lg`+ only | **permanent at every width ≥1024**, carries case navigation with counts and state chips; icon rail 768–1023; bottom bar of four below 768 |
| Page header | title block | **none** — replaced by the case header (§14.2) |
| Footer | full | **one line**: legal · support · ruleset version |
| Container | 1176/1320/1440 | same ladder, but the work column does not inherit `--width-prose` |
| Type, colour, rules, motion | identical tokens | identical tokens |

Same grid, same type scale, same four rules, same rubric. A user moving between the two never leaves the family; they can see immediately which side they are on.

---

## 5. Colour

### 5.1 Philosophy

Five structural jobs. A colour that cannot be assigned one of these five is not in the system.

| Job | Colour | Meaning | Where it may appear |
|---|---|---|---|
| **INK** | `#10161D` | text | all running text, all headings on paper |
| **GROUND** | paper family | the page | three warm surfaces, nothing else |
| **STRUCTURE** | navy `#0E2A47` | the institution speaking | masthead rule, the **one** verso band per page, the footer, the 2px band rule, the platform top bar |
| **ORDER** | rubric `#A4231B` | position in a sequence | ordinals, the current item's rule, the head rule of a register, the source-list markers, the superior margin markers |
| **AXIS** | cooperation green `#1B6B4A` | the Morocco side | the Moroccan half of a bilateral diagram, the Forum, the pilot, partner marks — **and nothing else**, so that navy-Italy against green-Morocco becomes a readable signal |

Plus four **state triplets** (fg / bg / border), used only where a state exists.

The test: *if you cannot say which of the five jobs a coloured mark is doing, remove it.* Applied to the current build, this removes 38 of the 38 bronze declarations in `components.css`, where bronze is simultaneously eyebrow text, the active nav marker, the default icon colour, the blockquote rule, the notice rule, a decorative dot in the language switcher, the nav underline, a panel top rule, the breadcrumb corner and the footer heading colour.

### 5.2 Tokens

```css
:root {
  /* GROUND — three warm surfaces, and no fourth */
  --paper:        #FAF7F0;  /* page ground */
  --paper-deep:   #F0EBE0;  /* process band: forms, steps, procedures */
  --paper-edge:   #E4DED0;  /* table zebra, rule fill */
  --surface-input:#FFFFFF;  /* form controls only */

  /* INK */
  --ink:          #10161D;  /* 16.99:1 on --paper */
  --ink-secondary:#3A362E;  /* 11.23:1 */
  --ink-muted:    #5F584C;  /*  6.57:1 — marginalia, captions, credits */

  /* STRUCTURE */
  --navy:         #0E2A47;  /* 13.96:1 on paper; white on it 14.58:1 */
  --navy-deep:    #08182F;  /* the platform top bar only */
  --paper-on-navy:#FAF7F0;  /* 13.62:1 */
  --paper-muted-on-navy:#C3CBD6; /* 8.91:1 */

  /* ORDER */
  --rubric:       #A4231B;  /*  6.92:1 on paper — text-safe at any size */
  --rubric-rule-on-navy:#D9705C; /* 4.46:1 on navy — RULE ONLY, never text */

  /* AXIS */
  --cooperation:  #1B6B4A;  /*  6.04:1 on paper */

  /* RULES — four weights, four meanings */
  --rule-hair:  #D8D1C4;    /* 1px — rhythm between rows, non-semantic */
  --rule-ink:   #8C8374;    /* 1px — structural boundary, 3.49:1 */
  --rule-band:  var(--navy);     /* 2px — opens a band, closes a plate */
  --rule-order: var(--rubric);   /* 2px — the current item, the head of a register */

  /* STATE — fg on bg ≥4.5:1, border on paper ≥3:1 (re-verify at build) */
  --state-ok-fg:#1B6B4A;      --state-ok-bg:#E6EFE8;      --state-ok-br:#4F9070;
  --state-info-fg:#1E4A85;    --state-info-bg:#E8EDF4;    --state-info-br:#5F84B5;
  --state-warn-fg:#7A4E00;    --state-warn-bg:#FAF0DF;    --state-warn-br:#B08A3C;
  --state-error-fg:#8F1D1D;   --state-error-bg:#F8E7E5;   --state-error-br:#C4635F;
  --state-pending-fg:#5E4B14; --state-pending-bg:#F4EEDC; --state-pending-br:#A08A46;
}
```

Every contrast figure above is computed against the ground named. State triplets are inherited from the current system, which documents them as meeting their floors; **re-verify all fifteen against `--paper` #FAF7F0** before freezing, since the ground has moved.

Twelve currently-unused tokens (`accent-100/400`, `neutral-100/400/800`, `primary-500/600`, `secondary-50/100/300/700/900`) are **deleted**, not kept as "riserva". A reserve nobody spends is dead weight that invites arbitrary use later.

### 5.3 Ground changes are the composition

**Rule: no page ships with a single ground.** Three grounds, each with a meaning:

- `--paper` — the site explains.
- `--paper-deep` — the process: steps, forms, procedures, the orientation flow, the platform's case header.
- `--navy` — **the institution speaks**: the home plate, the promoter statement, the disclaimer, the Forum band, "ce que la plateforme ne fait pas". **Exactly one navy band per page, never two.**

Today `.section--inverse` is defined at `layout.css:47`, documented at `DESIGN_SYSTEM.md §6.4`, and used **zero times across 169 templates**, so the only dark surface on any page is the footer — which therefore becomes the heaviest visual event on the site by accident.

Pair every ground change with a **measure change**: a navy band carries a 44-character statement, not a 68-character paragraph.

### 5.4 Contrast behaviour

- Text ≥ **4.5:1**; text above 24px ≥ 3:1 but the system does not use the relaxation — every text token here clears 4.5:1 on its ground.
- Rules, borders, state markers, focus rings: ≥ **3:1** against the surface **they are drawn on**, not against the element they surround. (The skip link's ring is currently 1.38:1 against the page, because `base.css:311` strips the halo that does the job everywhere else.)
- **Never colour alone.** Every state carries a word, and where space permits a rule weight or a glyph. ECL: *"always provide a text-based equivalent."*
- Every token is defined for **both** grounds. A component on navy uses `--paper-on-navy` / `--rubric-rule-on-navy`; there is no "inverse variant" improvised per component.
- **Three chromatic events maximum per viewport.** Count, at any scroll position, the marks that are not ink / paper / rule. Four means one is decoration.

### 5.5 Dark mode

**None.** Reason: this direction has exactly one ground change with a meaning (paper → navy), and a user-inverted palette destroys it — the verso band stops being a counter-ground and becomes ordinary. Ship `color-scheme: light` explicitly and do not define a `prefers-color-scheme: dark` palette.

Instead, ship what is actually missing: a **`@media (forced-colors: active)`** layer. `grep -n "forced-colors" static/css/*.css` returns nothing today, and the design's entire structural vocabulary is background-painted pseudo-elements — the `aria-current` bar, the error dot, the accent hairlines — all of which are repainted Canvas and vanish under Windows High Contrast. Rule for the new system: **structure is drawn with `border`, `outline` or text, never with `background` on a pseudo-element**, and the forced-colors layer restores every rule and state with `CanvasText` / `LinkText` / `Highlight`. One forced-colours capture joins the standard screenshot matrix.

### 5.6 Forbidden

No gradient of any kind. No `backdrop-filter`. No glassmorphism, no blobs, no floating decorative objects. No second blue — links are `--ink` with an underline (`text-underline-offset: 0.18em`, `text-decoration-color` at 45% mix), never a distinct link blue; today `#1e4a85` is simultaneously the link colour, a status badge colour and, within a hair, the structural navy. No colour-only state. No tint outside the five state triplets. No rubric as text on navy. No `--radius-pill`. **Blu Italia `#0066cc`** and its ramp, **ECL `#0E47CB` + `#FFD633`**, and **Titillium Web** are excluded by identity, not by licence: the .italia system states that its blue *is* the PA identity at national scale and instructs non-national actors to choose a dedicated primary. **No EU emblem** (OJEU 2012/C 271/04: use must not create the impression of a connection with, or endorsement by, EU institutions — a bilateral Veneto–Morocco mobility project is precisely that context). No Republic emblem, no regional or comunal stemma, no Ministry or Chamber of Commerce mark without a signed written authorisation. No SPID / CIE / pagoPA / AppIO button or lookalike. No "Amministrazione trasparente" section furniture. The word *ufficiale / officiel / رسمي* never applied to the site itself.

---

## 6. Imagery

### 6.1 The rule

**An image appears only where it documents something specific.** Not "the companies page needs a picture" — *"this is the Sala della Gran Guardia, Rovigo, 2 October 2026"*.

**Maximum one photograph per page.** It is always a **PLATE**: full bleed, no radius, no shadow, no frame, no offset outline, no border. It is the page's Rank A section or it does not exist.

### 6.2 The caption contract

No image renders without a caption. Four mandatory fields, template-enforced:

```
place — date — one factual sentence — credit
Rovigo, Sala della Gran Guardia — 2 octobre 2026 — Ouverture du
Forum permanent Vénétie–Maroc. — © Nom Prénom / AGAMI
```

Set at `--t-caption` in the rail at `lg`+, directly beneath at `md`−. A `<figure>` without a `<figcaption>` is a **build failure**. Today there are six `<figure>` elements on the public site and **zero** `<figcaption>` elements, while `.prose figcaption` is fully styled at `base.css:410` and used nowhere. This single rule kills the stock library by itself, because there is nothing truthful to write under a photograph of strangers around a table in an unnamed city.

### 6.3 Crop discipline

**Two ratios. No others.**

- `2 / 1` — the **band plate**: territory, venue, architecture, a convening. Full bleed.
- `3 / 2` — the **document plate**: the source library's native ratio, so no crop occurs at all. Used inside the content column at `--width-register`.

Today one 3:2 library is forced into `4/3`, `16/7`, `16/9`, `21/9` and unconstrained, every one with `object-position: 50% 50%` — five ratios, no art direction, only geometry; the 21:9 banner discards 36% of the frame height blind. Under this direction, `object-position` is **stored per asset in the manifest** beside the existing `crop` field, so the subject is held under crop, and a container ratio never decides what a photograph shows.

### 6.4 Subjects

Two categories, and a third that is forbidden.

- **TERRITORY** — Rovigo, the Polesine, the Veneto industrial fabric; Moroccan ports, training institutes, civic architecture.
- **DOCUMENT** — registers, stamped paper, archive shelving, forms, signatures, seals.
- **Never**: people at laptops, meetings around reclaimed wood, post-it walls, students laughing, "collaboration", "teamwork", "espace de travail". The current hero is `reunion-cooperation` at 484×363 — the most-published category on Unsplash — and the pilot page carries a brainstorming wall of pink and yellow post-its, which is startup iconography, not institutional cooperation between the Veneto and Morocco.

Keep `docs/IMAGE_LICENSES.md` exactly as it is. Its forbidden-subject list (no borders, suitcases, queues, passports, airports, doors, thresholds, gates; no stereotyped migration iconography; no tourist clichés) and its §4 log of thirteen rejected candidates *with the reason for each* are the strongest artefact in this area and survive the redesign untouched.

### 6.5 When there are none

**The site ships with zero photographs** until the Forum reportage of 2 October 2026 exists. A site with no pictures reads as sober; a site with six interchangeable stock pictures reads as a template, which is the verdict already delivered.

This is possible because the page is carried by the graphic language of §7, not by imagery. Concretely: the home's Rank A section is a **typographic plate** — navy, full bleed, 88px display — not a photographic one. The plate slot exists either way; only its fill changes.

**Delete** the nine photographs that never render on any of the 52 public pages (4.83 MB of 6.99 MB shipped and never displayed, plus a duplicate 1.52 MB copy in `media/library/photos`). Commission the Forum reportage as a separate line item; after it, the site's image count is roughly a dozen, each with a caption that is true.

---

## 7. Iconography and the proprietary graphic language

The site must be recognisable with no photographs at all. Six devices do that work. They are the identity.

### 7.1 The mark and the lockup

**The mark** is the folio device at 24px: a square containing three horizontal rules of unequal length — long, short, long — stacked on a 4px rhythm, the second rule in rubric, the others in ink. It reads as entries in a register, and at favicon size as a stable institutional block. It is not a temple, not a flag, not a threshold, not a passport. It is literally the page's own structure, which is the definition of an identity rather than a logo.

Retire the current favicon (three vertical bars over a bronze base on navy — a public-building abstraction) and the `entrance-institution.svg` pediment, which today appears in the home entrances, in the footer, and **six times identically** in one six-item list on the Institutions page.

**Lockups:**

| | Contents | Used at |
|---|---|---|
| A | mark + wordmark + descriptor | ≥1280 masthead, footer |
| B | mark + wordmark | 768–1279, platform top bar |
| C | mark alone | ≤767, favicon, avatar, running head |

Wordmark: Newsreader 500 at 22px, `-0.01em`. **Clear space ≥ 1× cap height (≈24px at 1440)** on all sides — today the wordmark's right edge is at x=338 and the first nav item starts at x=343: five pixels. Descriptor: `Écosystème d'information et d'orientation — AGAMI APS`, `--t-folio`, hidden below 1280 in favour of lockup B (never hidden leaving a bare string). The ™ stays `dir="ltr" translate="no"`, superior, ~55% of cap height, tracked away from the "y". In Arabic the descriptor is Arabic and sits on the mirrored side; the wordmark itself stays Latin and LTR-isolated.

### 7.2 The folio

The single strongest mark on the site. At `lg`+, in the rail; below `lg`, a horizontal line.

```
lg+, in the rail:                below lg, horizontal:

  03                             ─────────────────────────────────
  ─────                          03 — LES PARCOURS RÉGULIERS — 20.09.2026
  LES PARCOURS
  RÉGULIERS
  ─────
  Révisé le
  20.09.2026
```

Ordinal at `--t-numeral` (44px at `xl`) in **rubric**, tabular. A 24px rubric rule beneath it. The running head at `--t-folio`. A date or source at `--t-caption` in `--ink-muted`. The ordinal is generated by a CSS counter and is **presentational** — the anchor is always a slug (`#parcours-reguliers`), so renumbering never breaks a link.

This device replaces the eyebrow entirely. The eyebrow is abolished: today six eyebrows on one home page, all at 12px / weight 600 / `letter-spacing: 1.44px` / `rgb(122,97,36)` / x=152 / width 576, defined once in `base.css:218` and duplicated verbatim in three other files.

### 7.3 The register rule set

Four weights, four meanings, no fifth. A line on this site always means something.

| Rule | Weight/colour | Meaning |
|---|---|---|
| hair | 1px `--rule-hair` | rhythm between rows of the same kind |
| ink | 1px `--rule-ink` | a structural boundary (end of a zone, under the masthead) |
| band | 2px `--navy` | opens a band; closes a plate |
| order | 2px `--rubric` | the current item; the head of a register |

Today the border census on one page returns navy 1px on 32 elements, `#c4cad1` 1px on 29, `#dde1e5` 1px on 17 and bronze 2px on 5 — four values for "a line", none of which means anything.

### 7.4 The entry

The atomic content object. **It replaces the card everywhere.** A card exists in this system only if it passes the benchmark test in full (links to a detail page; unique content relative to siblings; groups *heterogeneous* content types; ≤4 in a row; one link) — which, applied to the current build, essentially nothing does.

```
──────────────────────────────────────────────────────────────  1px hair
 01   Travail salarié                            ENTREPRISE   →
      entrées pour travail dans le cadre des quotas annuels
──────────────────────────────────────────────────────────────
 02   Travail qualifié — Carte bleue européenne  ENTREPRISE   →
      pour les profils hautement qualifiés, sur la base d'un titre
──────────────────────────────────────────────────────────────
```

Anatomy: rubric ordinal (tabular, 22px) · title `--t-entry` serif · gloss `--t-gloss` sans, one line · **responsible actor** `--t-folio` at the inline end · arrow. The whole row is one target (≥64px at `lg`+, ≥104px at `xs`). Rows may be unequal in height; they align on their top rule, never on a forced baseline grid.

The 01–08 `Les parcours réguliers` list already in the build (`persons__1440x900__fr.png`, y≈880–1900) is the closest existing object and the proof this works. It becomes the site's core pattern rather than one section inside one page — including in the platform, where a document requirement, a deadline and a message are all entries.

### 7.5 The margin note

The device nobody else does on the web, and the one that reads as *published* rather than *assembled*.

A marginal note sits in cols 11–12, at `--t-caption` in `--ink-muted`, **aligned to the first baseline of the block it annotates**, tied to a point in the text by a superior rubric marker (`¹ ² ³`). It carries: the source, the date, the legal caveat, the "ce que la plateforme ne fait pas" clause, the ruleset version, the responsible authority.

Where a block has no margin note, the block widens from cols 3–9 to cols 3–10 and the margin closes. The column is never left as a void. Below `lg` the note moves beneath its block, indented by the ordinal column, marker preserved.

This is where the legal apparatus lives. Today those clauses are small grey lines and low-contrast footnotes; as a margin apparatus with markers and sources they become the institution's signature.

### 7.6 The plate and the verso band

**Plate** — full bleed, once per page: either a photograph at 2:1 with an archive caption, or a **verso band** (navy, typographic). Closed at the bottom by a 2px `--rubric-rule-on-navy` rule. Opened at the top by a 2px navy rule where it meets paper.

The Forum hero already in the build is the only controlled full-width band anywhere on the site and the only moment with presence. It proves the team can do it; this direction does it on every page, exactly once.

### 7.7 Icons

One drawing system. 1.5px stroke, **square caps** (round caps read consumer), all strokes `currentColor`, no literal hex anywhere in `static/img/` (today `entrance-person.svg` bakes `#0f2b52`, `#9a7b2f`, `#fbfaf7`, and `orientation.svg` adds `#1f6b48`). Add a test that fails on any literal hex inside an SVG.

Five legitimate uses (.italia): symbolising an interaction function; navigation; categorising a **content type** (document, event, person, place); loading/success feedback; social. Always paired with a text label, or the label available to assistive technology. **Maximum six icons per page.** Never one icon per row. Never one icon per card — there are no cards.

**Retire the four entrance illustrations** (176×132, a stick figure with a dotted rising path, three buildings) and `pilot-flow.svg` (a rising growth curve with the final node filled gold — a growth chart drawn for an institutional sequence, implying an outcome the platform does not promise). Retire the pilot page's floating decorative squiggle outright.

---

## 8. Spacing and vertical rhythm

**Base unit 4px. Every line-height is a multiple of 4. Every block space comes from one list.**

```css
--s-1:  4px;   --s-2:  8px;   --s-3: 12px;  --s-4: 16px;
--s-6: 24px;   --s-8: 32px;   --s-12:48px;  --s-16:64px;
--s-24:96px;   --s-32:128px;
```

No value outside this list. No stacked spacing (`margin` + `padding` doing the same job on adjacent elements) — ECL's rule, adopted.

**Space between sections is always greater than space inside them.** Section rank sets the outer space:

| Rank | Section type | padding-block `lg`+ | `md` | `xs`/`sm` |
|---|---|---|---|---|
| **A** | plate | 0 (band height) + 96 after | 0 + 64 | 0 + 48 |
| **B** | spread (title + prose + margin) | **96 / 96** | 64 / 64 | 48 / 48 |
| **C** | register, table, sequence | **56 / 56** | 40 / 40 | 32 / 32 |
| **D** | notice, marginal band, legal | **32 / 32** | 24 / 24 | 24 / 24 |

Today the section padding is `72/72` on **every** section at 1440 and `80/80` on every section at 1920, so the scroll has no accents: six beats of identical duration.

**Baseline discipline.** The first baseline of a section's title, the first baseline of its folio ordinal, and the first baseline of its first margin note **align**. This is one `margin-block-start` per zone, computed from the difference of the three line-heights, and it is checkable in a browser test. It is the single craft detail that most signals "typeset" rather than "laid out".

---

## 9. Surfaces, borders, elevation

**Elevation: none.** Zero `box-shadow` on content. The only permitted shadow in the entire system is on the two surfaces that genuinely float — the mobile drawer and the dialog — at one value:

```css
--shadow-surface: 0 8px 32px rgb(14 42 71 / 0.18);
```

Everything else separates by **rule** and by **ground change**. A test asserts `box-shadow` appears on no selector other than `.nav-drawer` and `dialog`.

**Radius: 0.** Two exceptions, both functional: **2px** on form controls and buttons, so a control reads as a control; **50%** on a step marker circle. `--radius-pill` is deleted. .italia states the principle from the opposite direction: *"gli angoli squadrati si addicono maggiormente a elementi che richiedono una presentazione più formale e strutturata"* — square corners suit elements requiring a formal, structured presentation. A radius census of the current home page at 1440 returns 2px ×12, 3px ×7, 50% ×5 and 999px ×5: four radii on one page.

**Boxed surfaces: two in the whole system.**

1. **NOTICE** — a 4px inline-start rule in the state colour, a 5%-tinted ground from the state triplet, a title at `--t-folio`, body at `--t-prose`, no icon chip, no shadow, no radius. Four trigger-based variants (ECL): *information* (something changed), *success* (an action completed), *warning* (a consequential action ahead), *error* (an action failed + recovery). Plus three editorial variants (.italia): **Note**, **Important**, **Approfondissement** — these are for standing content on long pages and they are where the legal disclaimers live ("pré-évaluation à caractère informatif", "ne se substitue jamais aux autorités compétentes", the anti-fraud statement). Placed at the beginning of a section, used sparingly, *"so that each one retains its signal value"*.
2. **FORM PANEL** — `--surface-input` white, 1px `--rule-ink`, 2px radius, no shadow.

**Nothing else is boxed.** No dashed box with a centred icon. An empty region is **one hairline plus one left-aligned sentence** naming who fills it and when, with the resolving action inline as a text link. The portal currently renders six of these dashed boxes on one dashboard — five of them identical, each with the same icon twice (once in the header, once centred in the box).

**Buttons: three ranks, no more.**

| Rank | Treatment | Rule |
|---|---|---|
| PRIMARY | filled navy, paper text, 44px, 2px radius | exactly one per view |
| SECONDARY | 1px navy outline, navy text, 44px | zero or more |
| TEXT | ink, underlined, arrow optional | anywhere |

Delete `.btn--ghost`, `.btn--upper` (used once, to look different), and the bronze uppercase entrance link. Write the rule down: **the primary action of a flow keeps the same rank on every surface it appears on.** Today "start the orientation questionnaire" is a filled navy button on the home page and an outline button in the portal.

---

## 10. Information hierarchy

### 10.1 How a page announces its importance

Three page openings. The archetype chooses one; the author does not.

- **Opening A — plate.** A full-bleed band, typographic or photographic, `--t-plate`. For: home, Le modèle, Forum, Attention aux fraudes, Le projet, AGAMI. The page is a statement.
- **Opening B — title block.** Paper, no band. Rail: breadcrumb + folio. Cols 3–8: `--t-title` + one standfirst at `--t-lead`. Cols 11–12: the page's standing margin apparatus (revision date, ruleset version, the informative-nature caveat). Closed by a 2px navy rule. For: the four hubs, references, the platform's public-facing pages.
- **Opening C — folio line only.** A horizontal folio line, then the title at `--t-title` on the reading column. No standfirst. For: articles, pathway sheets, glossary entries, news items, legal pages.

**Never two leads.** The home hero currently sets two consecutive paragraphs saying the same thing in two typefaces at two sizes — the second one a CMS fragment beginning lowercase and ending without a full stop, rendered in French on `/it/` and `/ar/`.

### 10.2 The anatomy of a section

Four slots. Slot 3 is the variable.

| Slot | Contents | Zone |
|---|---|---|
| 1 FOLIO | ordinal · running head · date/source | rail (`lg`+) or folio line |
| 2 HEAD | band title `--t-band`; optional standfirst `--t-lead` at ≤45 characters | cols 3–8 |
| 3 BODY | **exactly one of six types** | cols 3–9, or a permitted break |
| 4 MARGIN | 0–3 notes with superior markers | cols 11–12 |

**The six body types:** `PROSE` · `REGISTER` (entry list) · `TABLE` · `SEQUENCE` (timeline) · `PLATE` · `NOTICE`.

### 10.3 How every section stops looking identical

Three enforced rules. Each is a test, not an aspiration.

1. **No body type may appear twice consecutively on a page.**
2. **No section rank may appear twice consecutively.** A page has exactly one Rank A, at most three Rank B, and the rest C/D.
3. **A page must use at least four of the six body types**, and at least two ground values.

A home page therefore reads `A-C-B-C-D-B-C` rather than `B-B-B-B-B-B`. Today five content sections on the home page render — measured — eyebrow at 12px / 1.44px / `rgb(122,97,36)`, then H2 at 33.76px / line-height 38.82 / weight 500 / x=152 / width 576, then a lead at 21px / width 576. Not similar: **identical to two decimal places**, five times.

The head treatment and the container are what flatten the page — the section *content* is already varied. Fix the heads and the containers and the complaint dissolves.

---

## 11. Motion

**Nothing moves on scroll.** Delete `.reveal` and all three of its template usages, delete the IntersectionObserver stagger, the `will-change` that keeps a compositor layer alive for the life of the page, and the 2.5s safety timeout. Delete `initCounters()` and `.counter` — zero usages, and "startup counters" is on the banned list. Content visibility must never depend on a script having succeeded; today any throw in one of the six initialisers that run before `initReveal()` leaves every `.reveal` block permanently at `opacity: 0`.

Never moving: page content on scroll, photographs, headings, the wordmark, numbers, section bands, table and list rows, the header (no shrink, no hide-on-scroll). Institutional calm is content that is simply *there*.

Four tiers. Anything outside them is deleted.

| Tier | What | Duration | Easing | Travel |
|---|---|---|---|---|
| **1 STATE** | disclosure chevron, `aria-current` rule, checkbox/radio, `:active` press | 120ms | `cubic-bezier(0.2, 0, 0, 1)` | ≤4px |
| **2 SURFACE** | drawer, mega-menu panel, dialog, dropdown | enter 200ms / exit 140ms | `cubic-bezier(0.16,1,0.3,1)` / `cubic-bezier(0.7,0,0.84,0)` | its own dimension — a drawer travels `translateY(-100%)`, not 8px |
| **3 MARK** | **the signature** — a 2px rubric rule draws from the inline start under the destination when the system moves the reader against their will: form-error summary focus, wizard step change, a newly arrived message | 240ms, one shot | `--ease-standard` | the rule's own width |
| **4 PROGRESS** | upload, wizard progress | real elapsed work | linear | — |

Ceilings: nothing exceeds 240ms except Tier 4; nothing travels more than 12px except a Tier 2 surface. Banned outright: parallax, scroll-linked animation, decorative loops, moving gradients, autoplay carousels, and hover as the *sole* feedback for anything — every hover affordance has an `:active` and `:focus-visible` equivalent, because four of the current build's motion events are hover-only and therefore do not exist on a phone.

**Reduced motion is the default posture.** Everything new is wrapped in `@media (prefers-reduced-motion: no-preference)`; Tier 3 degrades to an instantly-drawn static rule (the mark still appears, it simply does not draw). Keep the existing `prefers-reduced-motion: reduce` block exactly as written — it is implemented properly and completely, and it is better than most commercial products.

---

## 12. Hero approach

### 12.1 Home — Rank A verso band, typographic, full bleed

100vw, block-size `62vh` at `lg`+, clamped `min 520px / max 720px`. Navy. Inside, the 12-column container.

- **Rail (cols 1–2):** folio `00` in `--rubric-rule-on-navy`, a 24px rule, running head `ÉDITION 2026`, then `Vénétie — Maroc` and `Révisé le 20.09.2026` at `--t-caption` in `--paper-muted-on-navy`.
- **Content (cols 3–9):** the title at `--t-plate` 88/92, **sentence case**, three lines maximum, `--paper-on-navy`. Below at cols 3–7: one standfirst at `--t-lead` 22/32 — **one**, not two. Then a 1px rule and, beneath it, the two actions on one line: PRIMARY `Commencer l'orientation`, TEXT `Voir les parcours réguliers →`.
- **Margin (cols 11–12):** **the anti-fraud statement**, promoted (grid break 4). Three lines with rubric superior markers: `¹ Personne ne peut vous vendre un visa.` / `² Nous ne demandons jamais d'argent.` / `³ Aucune « voie rapide » n'existe.` Then a text link `Attention aux fraudes →`.

That last decision is not decoration. On today's public site `grep -ic "fraude"` on the home page returns **0** and `/fr/attention-aux-fraudes/` returns 404, because the page is gated behind Phase 3; in Phase 3 the warning sits at y=7333 on a phone — **8.7 swipes down**. Putting it in the hero margin makes the site's most important safety message the second thing a reader's eye lands on, at no cost to the composition.

**No photograph in the home hero.** The current one is a 484×363 thumbnail (11% of a 1440 viewport, 4% of its area) of four people in hoodies around a reclaimed-wood table, behind an offset bronze outline that overshoots the image by 22px on two sides and reads as a printing misregistration. Either an image is a full-bleed moment of a real place with a caption, or the page opens on type. There is no defensible middle at 484px.

### 12.2 Interior page — Opening B, no band

Paper. Rail: breadcrumb at `--t-folio`, then the page folio. Cols 3–8: title at `--t-title` 52/56, sentence case, then one standfirst at `--t-lead`. Cols 11–12: the standing margin apparatus. Closed by a 2px navy rule. The first body block begins 56px below it.

No eyebrow. No lead repetition. No hero photograph. The H1 is set in **sentence case by CSS**, and an editor cannot change the identity by typing caps into the CMS — today `/fr/entreprises/` renders `<h1>DE QUELS PROFILS PROFESSIONNELS VOTRE ENTREPRISE A-T-ELLE BESOIN ?` with computed `text-transform: none`, four ragged lines of tightly-tracked all-caps serif, and Google shows a shouting result.

---

## 13. Data and process visualisation

### 13.1 A pathway — the register entry, expanded

Body type `REGISTER`, cols 3–9 (or a SPREAD to 1–12 when it is the page's main object). 2px navy rule above the first row, 1px hair between rows, 2px navy rule below the last.

```
═══════════════════════════════════════════════════════════════  2px navy
 01   Travail salarié                                ENTREPRISE   →
      entrées pour travail dans le cadre des quotas annuels
───────────────────────────────────────────────────────────────  1px hair
 02   Travail qualifié — Carte bleue européenne      ENTREPRISE   →
      pour les profils hautement qualifiés, sur la base d'un titre
───────────────────────────────────────────────────────────────
 03   Formation dans le pays d'origine    INSTITUTION · UNIVERSITÉ →
      parcours de formation professionnelle et civico-linguistique
═══════════════════════════════════════════════════════════════
```

Hover/focus: ordinal turns from `--ink-muted` to `--rubric`, a 2px rubric rule appears on the inline-start edge of the row (Tier 1, 120ms). No background change, no shadow, no lift.

This replaces: the four "Quatre accès" entrance columns, the five 999px pills on "Les parcours réguliers", the three-up on the Companies page, the six-item Destinataires list with its six identical temple icons, and the news index cards.

### 13.2 A timeline — the SEQUENCE

**Vertical, always.** Never a row of circles joined by lines. The current 4+4 pilot diagram runs its connector after step 4 to the container edge and stops, requiring the reader to jump down and back to the left for step 5; the connector after step 8 also runs to nowhere; and step 3's two-line label drops its baseline out of alignment with steps 1, 2 and 4. At 390 it has no meaning at all.

```
 cols 1–2        cols 3–9
 ┌ date/phase ┐  ┌────────────────────────────────────────────┐
 │            │▌ │ 01  Besoin exprimé par l'entreprise        │
 │  Phase 1   ││ │     L'entreprise décrit les profils…       │
 │            ││ │                              ENTREPRISE    │
 │            ││ ├────────────────────────────────────────────┤
 │  Phase 2   │▌ │ 02  Profils et compétences                 │
 │            ││ │                    INSTITUTION · UNIVERSITÉ│
 │            ││ ├────────────────────────────────────────────┤
 │ ═══════════╪╪═╡ ⟨ MAROC → ITALIE ⟩  responsabilité transférée
 │            ││ ├────────────────────────────────────────────┤
 │  Phase 5   │▌ │ 05  Procédures régulières                  │
 │            ││ │                        AUTORITÉS COMPÉTENTES│
 └────────────┘  └────────────────────────────────────────────┘
```

A **1px continuous rule** runs the full height in the gutter between rail and content. Each step puts a **2px rubric tick** on it. The rule is `--cooperation` green above the crossing and `--navy` below it, and the crossing itself is a labelled hairline running the full width. This is the direction's signature diagram: it distinguishes phase from step, actor from action, and Morocco from Italy — none of which the current diagrams do — and it works at 320px unchanged, because it is a list.

### 13.3 A checklist — a real table

Columns, always headed: `Élément | État | Responsable | Échéance | Action`. Missing and expiring rows first. Tabular figures. **Dash (`—`) for null, never an empty cell** (ECL). Aligned by *reading direction*, so RTL resolves correctly.

Seven visible states, each carried by a **word** at `--t-folio` plus a 2px rule in the state colour on the inline-start of the cell — never colour alone:

`MANQUANT · DÉPOSÉ · EN EXAMEN · VALIDE · NON VALIDE · EXPIRÉ · À REMPLACER`

Uploaded files are **versions inside a row**, not top-level objects. Consent, where it blocks upload, is a **row-level blocked state with an inline link that resolves it**, not a banner above an empty box.

### 13.4 A rule outcome — the marginal apparatus applied to law

The most important screen in the product, and today it renders outside the platform, in the public shell, as `<ul><li>{{ item.text }}</li></ul>`.

```
 RAIL                CONTENT (cols 3–9)                 MARGIN (11–12)

 ÉVALUATION          ▌ Parcours possible                 Jeu de règles
 04.10.2026            (--t-title 52px, the WORD          v2.3.1
 ─────                 carries it; the 4px inline-        Évaluée le
 Réf.                  start rule is the state)          04.10.2026
 A7C3-0091                                                ¹ Cette pré-
                     ─────────────────── 2px navy ──       évaluation est
                     MOTIVATION                            informative.
                      01  Règle R-114 — titre reconnu      Les décisions
                          appliquée · satisfaite           relèvent des
                      02  Règle R-207 — durée de séjour    autorités
                          appliquée · à vérifier ¹         compétentes.
                     ─────────────────────────────
                     CE QUI MANQUE  (checklist rows,
                      with responsible actor + link)
                     ─────────────────────────────
                     SOURCES
                      01  D.lgs. 286/1998, art. 27
                          — consulté le 04.10.2026 →
                      02  Decreto flussi 2026, art. 4 →
                     ─────────────────────────────
                     [ Demander une revue professionnelle ]
```

Five outcome kinds — `POSSIBLE · ÉLÉMENT MANQUANT · AVERTISSEMENT · ARRÊT · REVUE REQUISE` — each a word at `--t-title` with a 4px state rule, not a coloured box. The numbered **source list** (rubric ordinals, title, reference, consultation date, link) is the single element that most converts "a questionnaire result" into "an institutional finding", and it is the one element the current result page has none of.

---

## 14. Platform interpretation

The platform is this direction's **working edition**. A case file is a register: numbered, dated, attributed. No new visual language.

### 14.1 App shell

`shell_platform.html`, not extending `base.html`.

- **Top bar 44px, `--navy-deep`:** lockup B · project name · the current case reference (`--font-mono`, LTR-isolated) · language · account menu · one help entry · one low-contrast `← Site public`. No mega-menu. No public footer — one legal strip with the ruleset version.
- **Rail 240px, sticky, full height ≥1024:** the same rail device, now grouped `MON DOSSIER` / `MON COMPTE`, each row carrying a count or a state chip. **Rows a role cannot use are absent, not greyed.** `navigation()` takes the account's role and returns *different structures*, not a filtered list — today it returns a hardcoded six-row list identical for every account, so `qa-company` is offered "Mon parcours" and "Commencer l'orientation" (the individual mobility questionnaire) and is labelled *"Personne"*.
- 768–1023: icon rail. Below 768: a four-item bottom bar (Dossier · Checklist · Pièces · Échanges) plus a sheet.

### 14.2 The case header — 96px, sticky under the top bar

Ground `--paper-deep`, closed with a 2px navy rule. Present on **every** authenticated screen.

```
DOSSIER ILE-2026-0043 · Amina B. · Travail salarié — famille de parcours
───────────────────────────────────────────────────────────────────────
ÉTAT  ORIENTÉ    ·    PHASE 2/7    ·    RESPONSABLE  Équipe AGAMI — orientation
```

Line 1: reference in `--font-mono`, LTR-isolated in Arabic. Line 2: `--t-folio` labels with values at `--t-ui`.

Where no `CaseFile` model exists yet, **derive both lines from what is already in the database** — consents, orientation sessions, submitted requests, memberships — and label the state honestly: `ÉTAT COMPTE CRÉÉ — ORIENTATION NON FAITE`. The system already knows, for the QA person account: two requests submitted and still "Nouvelle"; no orientation session; upload blocked pending consent; no organisation linked. Four known facts, four inferrable next actions, none of them currently surfaced.

**Delete the `page_header` from every portal screen.** Today it re-serves the public home page's marketing teaser — the same two locked strings — as a 48px H1 to people who have already logged in, and `ESPACE RÉSERVÉ` appears twice within 190px.

### 14.3 Next action band

Directly beneath the case header. **One** sentence at `--t-entry` 22px serif. One named responsible party. One date where known. One PRIMARY button. One `Pourquoi ?` disclosure linking the rule and its source. **Never two actions.**

### 14.4 Dashboard

One prioritised column. No tiles.

1. Next action band
2. Horizontal **phase rail** — 7 steps, the SEQUENCE component in its only horizontal form, current phase marked by a 2px rubric rule
3. **The checklist table** (§13.3)
4. Dated lists: échéances, communications — as entry rows
5. Append-only activity log

Empty regions: one hairline plus one left-aligned sentence naming who fills the region and when, with the resolving action inline. Never a dashed box, never a centred icon, never a standalone numeral at 34px above the words "demandes transmises".

### 14.5 List

A real `<table>` above 768 with `<caption>`, `scope="col"`, `scope="row"`, inside a labelled `role="region" tabindex="0"` scroll container — the pattern `templates/portal/requests.html` already proves. Below 768, a **defined pop-in**: each row becomes a labelled stack of `label / value` pairs at 48px minimum, hairline separated. Never a horizontal scroll for a four-column table.

### 14.6 Detail

Four regions, in this order:

1. Case header strip — real reference, state
2. **Où en est votre demande** — an ordered, append-only step list with state, responsible actor and date per step
3. **Ce qui vous est demandé** — checklist rows with inline actions
4. **Ce que vous avez transmis** — the definition list, demoted to the bottom, collapsed by default

### 14.7 Wizard

One question per screen. Folio in the rail: `QUESTION 03 / 07` with the progress rule beneath it. Question at `--t-band` 38px. Options as **56px rows** with the control pinned to the reading edge and the label immediately beside it, `input` ≥24px (today: 20×20px radios, and in Arabic the radio sits at x=334 while its label sits at x=33 — 280px apart with nothing between them).

Mandatory contract for every multi-step pattern in the system:

- Stored answers re-checked in the template (`{% if c.key in answers %} checked{% endif %}`) — today "Précédent" returns every radio unchecked.
- After every swap, focus moves to the question `<legend>` (`tabindex="-1"`) — today it lands on `<body>`.
- A **persistent polite live region outside the swapped node** announces "Question n sur m" — today the step page has zero live regions.
- `novalidate` on the form; errors go through the design system's summary + inline contract, never the browser's native bubble.
- Save and resume (WCAG 2.2 §3.3.7 Redundant Entry).

---

## 15. Mobile

Authored, not derived. Three budgets, enforced by test:

- **Home ≤ 5 viewport heights at 390.** Today 8.65; at 320, 9.90.
- **All four audience routes visible within 1.5 screens.** Today they begin at 1.82 / 2.29 / 2.76 / 3.23 screens and the block is 1907px tall.
- **Zero elements below 44px** in the interactive tree below 1024. Today the home at 390 has 25 sub-44px interactive elements and every portal page has 31–40, including the `.entrance__cta` — the primary call to action of each audience — at **22px**.

**Concrete decisions:**

| | Decision |
|---|---|
| Hero | full-bleed navy plate, 72vh; title `--t-plate` 40/44 over three lines; one standfirst; one PRIMARY button; the second action a text link; the three fraud lines beneath a 1px rule |
| Folio | horizontal line above every band: `03 — LES PARCOURS RÉGULIERS — 20.09.2026`, 13px caps on a 1px rule |
| Audience routes | a 4-row register at **104px per row**: ordinal 20px rubric tabular · title 20px serif · one-line gloss 15px · chevron. Whole row is the target. Section drops from ~1900px to ~460px |
| Margin notes | move beneath their block, indented by the ordinal column, superior marker preserved |
| Section padding | Rank B 48, Rank C 32, Rank D 24 — halved from desktop (today `--section-gap` clamps to 64px on a phone) |
| Measure | `--t-prose` stays 17/28; the column is the viewport minus 2×20px |
| Tables | pop-in (§14.5) |
| Footer | three `<details>` groups, closed by default. Today 18 links at 19px each in an adjacent stack, 967px — 1.15 screens |
| 768–1199 | authored as its own tier, **not** "wide phone". Two-column entrances, a real vertical side navigation, a prose cap so 768 does not exceed 1280's line length. Today the home hero at 768 is **1094px — 107% of the viewport** — because `.split` does not become two columns until 896px, orphaning the 768–895 band |

---

## 16. RTL and Arabic

The RTL *engineering* in the current build is genuinely excellent — zero horizontal overflow across 50 measurements on 19 public Arabic routes and 6 portal pages, logical properties throughout, mirrored progress bars, mirrored tables, mirrored disclosure markers. That engineering is kept in full. The Arabic *product* is rebuilt.

### 16.1 Type

```css
:lang(ar) {
  --font-display: "Noto Naskh Arabic", "IBM Plex Sans Arabic", serif;
  --font-body:    "Noto Naskh Arabic", "IBM Plex Sans Arabic", serif;
  --font-ui:      "IBM Plex Sans Arabic", system-ui, sans-serif;

  /* Arabic needs ~1.47× the vertical space of accented Latin */
  --lead-plate: 1.35;  --lead-title: 1.40;  --lead-band: 1.45;
  --lead-prose: 1.85;  --lead-ui: 1.55;

  /* ALL tracking zeroed, not an enumerated subset */
  --track-plate: 0; --track-title: 0; --track-band: 0;
  --track-normal: 0; --track-folio: 0; --track-caps-display: 0;
}
```

**Sizes ×1.10 on text roles, ×1.05 on display**, with a hard floor of **14px**. Measured justification: the ink height of `س` at 16px is 5px against a Latin x-height of 7px, so Arabic at 16px reads like Latin at ~11.5px; the current 12px eyebrow is an effective 8.6px.

**Leading justification, measured:** at the site's real H2 setting (33.76px / line-height 38.82px), two consecutive lines of vocalised Arabic produce glyph rects that **overlap by 12.2px** — line 1's ink ends at 44 while line 2's ink begins at 31.8, with 51px of ink inside a 38.8px line box. At 16px body, Arabic gets **1.6px of total leading** against Latin's 8px.

**Tracking justification:** `base.css:118` applies `letter-spacing: -0.01em` to `h1–h6` unconditionally, and the `:lang(ar)` block resets only `--tracking-eyebrow` and `--tracking-button`. So every Arabic heading carries negative tracking — measured −0.48px on H1, −0.34px on H2 — the exact rule `docs/I18N_RTL.md §7.5` states breaks Arabic ligatures. The fix is a token-level reset plus a **static test asserting no non-zero `letter-spacing` is reachable under `:lang(ar)`**, which is a tighter guarantee than the current hand-maintained blocklist of eight component rules (all of which contain only deletions, and none of which covers `forum.css`, where `.forum-hero__eyebrow` computes +1.79px).

**Ban `font-weight: 700` in Arabic** where only 400/500/600 are subset; `font-synthesis: none` makes the failure visible rather than smeared.

### 16.2 Mirroring under this direction

- The **rail mirrors to the inline end** (right → left becomes right in Arabic); the **margin** mirrors to the inline start. The empty channel (col 10) mirrors with them. Everything is `inline-start` / `inline-end`; no `left`/`right` anywhere.
- **Folio ordinals stay Western digits** (correct for Morocco) and are wrapped in `<bdi>`.
- The **running head** in Arabic is not uppercase — Arabic has no case. Its register is carried instead by a 2px rubric inline-start rule plus weight 600 at 15px. This is an *addition* for Arabic, not a deletion: the current Arabic design system consists of one font swap and eight rules that only remove things.
- Arrows are CSS/SVG only and flip with `icon--flip-rtl`. **No `→` inside a translatable string** — today French prescribed sentences keep right-pointing arrows on a page where every Arabic arrow points left.

### 16.3 Prescribed French — a designed object, not a leak

100 prescribed texts exist in French only (`apps/cms/locked_content.py:861`, with `# "ar": {...}` still a comment). They are the H1s, the leads, the pathway definitions, the timeline steps, the fraud warning. The result is that a typical Arabic page is **44% Arabic**, `/ar/forum/` is **1.1%** Arabic, and opening Phase 3 drops the Arabic home page from **73.5% to 17.9%**.

A new first-class component, `.prescribed`, is the **only** way locked French is ever rendered:

```
┌─ نص رسمي بالفرنسية — النسخة العربية قيد الإعداد ─────────────  caption 15px
▌
▌  [Arabic summary — خلاصة — 2–3 lines written by AGAMI's editors,
▌   explicitly NOT a translation of the locked text, so the content
▌   lock test still passes]
▌
▌  ┌─ LTR island, Latin faces restored, its own left axis ──────┐
▌  │ De quels profils professionnels votre entreprise           │
▌  │ a-t-elle besoin ?                                          │
▌  └────────────────────────────────────────────────────────────┘
└─────────────────────────────────────────────────────────────────
```

4px rubric inline-start rule · `--paper-deep` ground · full-width band so it never shares a row, a grid cell or a two-column comparison with Arabic text · Latin faces restored inside (`[lang="fr"] { --font-display: Newsreader; --font-body: Newsreader; }`) so prescribed French looks like the French design instead of a stranger · bidi isolation on an inner `<bdi>`, not on the block, so the block keeps the page axis and only the Latin run flips.

That last point fixes the worst visible defect in the Arabic build: because `base.css:426` sets `direction: ltr` on the *block*, `text-align: start` resolves to **left**, and every fallback block lands on the opposite margin. Measured: a Forum hero whose two lines begin **1136px apart** on opposite edges; pathway rows with **~760px of empty space between the ordinal and the title**, eight times; one entrance card where the title is flush left and its own CTA — also French — is flush right.

### 16.4 Gates

- **Arabic-script coverage of `<main>` is a release gate**, per route, with a published budget. Below budget, the page is not served at `/ar/` as if it were translated: it carries an honest Arabic notice and a one-paragraph Arabic summary.
- Work ordered by risk, not by sitemap: **anti-fraud → FAQ → orientation questionnaire → parcours → forum**.
- A test asserts every Arabic element's computed line-height ≥ its font's `fontBoundingBoxAscent + fontBoundingBoxDescent`.
- A test walks **text nodes** (not elements) and asserts every Latin run on an Arabic page is inside a `<bdi lang="…">`. The current test checks elements that already carry `lang`, which is why the nav string, the wizard legend, the Forum banner children and the utility bar all slip through.
- The glossary is the cheapest large win: its definitions are CMS content, not locked text. Rebuild it as a two-column index — Italian term as the headword (correctly: it is the word the user meets on a form), Arabic gloss beneath it in the Naskh, French definition in `.prescribed` until the Arabic exists — with an **Arabic-native index** (by theme: الإقامة / العمل / الدراسة / الوثائق) rather than a Latin A–Z bar laid out right-to-left so the eye reads it backwards.

---

## 17. Wireframes

### 17.1 Home, above the fold, 1440 × 900

Container 1320, margins 60, 12 cols × 88, gutters 24.

```
 col │  1    2  │  3    4    5    6    7  │  8    9  │ 10 │ 11   12
     ┌──────────────────────────────────────────────────────────────────────┐
  0  │▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ UTILITY 36px · --navy ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓│
     │ AGAMI — Dialogo Giuridico Interculturale APS · promoteur du projet   │
     │                        FR · العربية · IT · EN      🔒 Espace réservé  │
 36  ├──────────────────────────────────────────────────────────────────────┤
     │  MASTHEAD 72px · --paper                                             │
     │  ▤▤  Italy Legal Entry™                    ┌──────────────────────┐  │
     │      Écosystème d'information et            │ Rechercher        ⌕ │  │
     │      d'orientation — AGAMI APS              └──────────────────────┘ │
108  ├────────────────────────────────────────────────── 1px --rule-ink ────┤
     │  NAV 44px · --paper                                                  │
     │  Personnes    Entreprises    Institutions    Universités et formation│
     │  ▔▔▔▔▔▔▔▔▔                Le modèle · Forum · Ressources · Le projet │
152  ╞══════════════════════════════════════════════════ 2px --navy ════════╡
     │████████████████ PLATE · verso band · 100vw · --navy ████████████████ │
     │                                                                      │
     │  00        │ Un ordre de passage                │  ¹ Personne ne     │
     │  ▬▬▬       │ pour la mobilité régulière         │    peut vous       │
     │            │ vers l'Italie                      │    vendre un visa. │
     │  ÉDITION   │                                    │                    │
     │  2026      │  --t-plate 88/92 · Newsreader 400  │  ² Nous ne         │
     │            │  sentence case · 3 lines max       │    demandons       │
     │  Vénétie   │                                    │    jamais d'argent.│
     │  — Maroc   │ Orientation, formation avant le    │                    │
     │            │ départ et accompagnement, avec     │  ³ Aucune « voie   │
     │  Révisé le │ les acteurs compétents.            │    rapide »        │
     │  20.09.2026│  --t-lead 22/32 · cols 3–7 · ≤45ch │    n'existe.       │
     │            │                                    │                    │
     │            │ ──────────────────────── 1px ──────│  ▌ Attention aux   │
     │            │ ┌──────────────────────┐           │    fraudes →       │
     │            │ │ Commencer            │  Voir les │                    │
     │            │ │ l'orientation        │  parcours │  (grid break 4:    │
     │            │ └──────────────────────┘  →       │   margin promoted) │
     │            │                                    │                    │
 710 │▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ 2px --rubric-rule-on-navy ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬│
     ├──────────────────────────────────────────────────────────────────────┤
     │  01        │  Quatre accès à l'écosystème                            │
     │  ▬▬▬       │   --t-band 38/44                                        │
 766 │  QUATRE    │ ════════════════════════════════════ 2px --navy ════════│
     │  ACCÈS     │  01  Personnes                      PARTICULIERS     →  │
     │            │      s'orienter vers une voie régulière et se préparer  │
     │  Rank C    │ ───────────────────────────────────────── 1px hair ─────│
 900 └────────────┴──────────────── fold ─────────────────────────────────┘
```

### 17.2 Home, above the fold, 390 × 844

4 cols, 12px gutters, 20px margins.

```
     ┌────────────────────────────────────────┐
  0  │▓▓▓ UTILITY · --navy · 2 lines, no ▓▓▓▓▓│
     │ AGAMI — Dialogo Giuridico              │
     │ Interculturale APS · promoteur         │
     │ FR · العربية · IT · EN    🔒 Espace     │
  76 ├────────────────────────────────────────┤
     │ MASTHEAD 64px · --paper                │
     │ ▤▤ Italy Legal Entry™            [☰]   │
 140 ╞═══════════════════════ 2px --navy ═════╡
     │███████ PLATE · 72vh · --navy ██████████│
     │                                        │
     │ 00 ▬▬ ÉDITION 2026                     │
     │                                        │
     │ Un ordre                               │
     │ de passage                             │
     │ pour la mobilité                       │
     │ régulière vers                         │
     │ l'Italie                               │
     │   --t-plate 40/44                      │
     │                                        │
     │ Orientation, formation avant le        │
     │ départ et accompagnement, avec les     │
     │ acteurs compétents.   --t-lead 19/28   │
     │                                        │
     │ ┌────────────────────────────────────┐ │
     │ │ Commencer l'orientation            │ │ 48px
     │ └────────────────────────────────────┘ │
     │ Voir les parcours réguliers →          │ 44px
     │ ──────────────────────────── 1px ──────│
     │ ¹ Personne ne peut vous vendre un visa.│
     │ ² Nous ne demandons jamais d'argent.   │
     │ ³ Aucune « voie rapide » n'existe.     │
     │ ▌ Attention aux fraudes →              │
 748 │▬▬▬▬▬▬▬ 2px --rubric-rule-on-navy ▬▬▬▬▬▬│
     ├────────────────────────────────────────┤
     │ ───────────────────────────────── 1px  │
     │ 01 — QUATRE ACCÈS — 20.09.2026         │  ← folio line
 796 │ Quatre accès à l'écosystème            │
     │   --t-band 28/36                       │
     │ ═══════════════════════════ 2px navy ══│
 844 └───────────── fold ─────────────────────┘
        ↓ next screen: four 104px register rows
        ┌────────────────────────────────────┐
        │ 01  Personnes                    → │ 104px
        │     s'orienter vers une voie…      │
        ├────────────────────────────────────┤
        │ 02  Entreprises                  → │ 104px
        │     exprimer les besoins en…       │
        ├────────────────────────────────────┤
        │ 03  Institutions                 → │ 104px
        ├────────────────────────────────────┤
        │ 04  Universités et formation     → │ 104px
        └────────────────────────────────────┘
        Section total ≈ 460px (was 1907px).
        All four routes complete by 1.45 screens.
```

### 17.3 Person dashboard, 1440 × 900 (platform)

```
     ┌──────────────────────────────────────────────────────────────────────┐
  0  │▓ TOP BAR 44px · --navy-deep                                          │
     │ ▤ Italy Legal Entry™ · Espace réservé   ILE-2026-0043   FR  ⌄Amina B.│
     │                                          Aide   ← Site public        │
 44  ├──────────────┬───────────────────────────────────────────────────────┤
     │ RAIL 240px   │ CASE HEADER 96px · --paper-deep · sticky              │
     │ sticky       │ DOSSIER ILE-2026-0043 · Amina B. · Travail salarié    │
     │              │ ──────────────────────────────────────────────────────│
     │ MON DOSSIER  │ ÉTAT ORIENTÉ · PHASE 2/7 · RESPONSABLE Équipe AGAMI   │
     │ ▌01 Vue      │ ══════════════════════════════════ 2px --navy ════════│
     │   d'ensemble │ PROCHAINE ACTION                                      │
     │  02 Mon      │                                                       │
     │     parcours │ Déposez votre attestation de diplôme.                 │
     │  03 Pièces ③ │   --t-entry 22/28 · serif                             │
     │  04 Checklist│ Responsable : vous · Attendue avant le 14.10.2026     │
     │       ②      │                                                       │
     │  05 Échéances│ ┌───────────────────────┐   Pourquoi cette pièce ? ⌄  │
     │  06 Échanges │ │ Déposer la pièce      │                             │
     │       ①      │ └───────────────────────┘                             │
     │  07 Histori- │ ────────────────────────────────────── 1px --rule-ink │
     │     que      │ PHASE  01 ──▌02── 03 ── 04 ── 05 ── 06 ── 07          │
     │              │        compte  orienté  dossier  instruction …        │
     │ MON COMPTE   │ ──────────────────────────────────────────────────────│
     │  Identité    │ CE QUI VOUS EST DEMANDÉ                               │
     │  Consente-   │ ══════════════════════════════════════════ 2px navy ══│
     │   ments      │ Élément          État        Responsable    Échéance  │
     │  Sécurité    │ ───────────────────────────────────────── 1px hair ───│
     │              │ Attestation de ▌MANQUANT     vous          14.10.2026 │
     │ ──────────   │ diplôme                                    [Déposer]  │
     │ Aide et      │ ───────────────────────────────────────────────────── │
     │ guichet →    │ Pièce d'identité ▌VALIDE     vous          —          │
     │              │ ───────────────────────────────────────────────────── │
     │              │ Traduction      ▌EN EXAMEN   Équipe AGAMI  —          │
     │              │ assermentée                                           │
     │              │ ══════════════════════════════════════════════════════│
     │              │ ÉCHÉANCES                                             │
     │              │ 14.10.2026  Dépôt de l'attestation          vous    → │
     │              │ ───────────────────────────────────────────────────── │
     │              │ ÉCHANGES                                              │
     │              │ 18.09.2026  Accusé de réception — Équipe AGAMI      → │
     │              │ ───────────────────────────────────────────────────── │
     │              │ HISTORIQUE                                            │
     │              │ Aucun événement depuis le 18.09.2026. Les étapes      │
     │              │ enregistrées par l'équipe apparaissent ici.           │
 900 └──────────────┴───────────────────────────────────────────────────────┘
```

No tiles. No dashed boxes. No standalone counter. The fold budget: 44 top bar + 96 case header + 140 next action + ~340 checklist = 620px, leaving 280px of air — against today's 421px of chrome before the first portal content appears (47% of the fold) and 637px on a phone (75%).

---

## 18. Risk and cost

### 18.1 What could go wrong

| Risk | Severity | Mitigation |
|---|---|---|
| **Density reads as austere or unwelcoming** to the primary audience — a 24-year-old in Casablanca on a mid-range Android. This is the direction's central bet and the one most likely to fail. | High | The phone composition is authored separately (§15), the reading size never shrinks, register rows are 104px targets, and the first screen carries one action and three plain safety sentences. Validate with five real users in Morocco before committing the home page. |
| **17px serif body fails at 1× DPR** on Windows and older Android — the single highest-risk typographic decision. | High | Font QA gate §3.7.5 is a release blocker. If it fails: raise to 18/30 and re-measure the column. Do **not** fall back to sans — that would make it a colour variant of the current build. |
| **Rubric red reads as "error"** or as alarm, especially beside a form. | Medium | Error state is a darker `#8F1D1D` used only with a word and a 4px rule; rubric never appears on a tinted ground; rubric never appears on more than two marks per viewport. Test in greyscale and forced colours. |
| **The margin column starves.** Every block needs an editor to write a note, or the column empties and the page looks broken. | Medium | The margin is optional per block; when empty the content widens to cols 3–10 and the channel closes. Write the first twenty margin notes as part of the design work, not as a content backlog. |
| **A half-built version looks worse than today.** The current site's safety is its uniformity; a page where three sections use the new apparatus and four do not will read as broken rather than as transitional. | **Critical** | Sequence by *system*, never by page: tokens → grid → type → the six devices → archetypes → then pages, all at once per archetype. No page ships half-converted. Keep the current build serving until the archetype layer is complete. |
| **Folio numbering breaks anchors** when content is reordered. | Low | Ordinals are CSS counters; anchors are slugs. |
| **The 14 archetypes are never written** and every new page converges on cards again — which is what happened the first time, with 51 of 74 templates extending `base.html` directly. | High | A test fails when a view renders a template that declares no archetype. This is the P0 that unblocks everything else (`REQUIREMENT_MATRIX_V2.md:220`, REQ-DES-04, still TODO). |
| **The Arabic edition stays a French site with an Arabic shell.** The typography here is correct and will make the untranslated French *more* visible, not less. | High | `.prescribed` (§16.3) plus the per-route Arabic-share CI gate. The design is the forcing function; treat "this page is 18% Arabic" as a defect with the status of a contrast failure. |
| **Photography never arrives**, and the site ships permanently with none. | Low | That is the designed state, not a degradation. The graphic language is specified to carry the site alone. |

### 18.2 What it costs

Person-days, one senior designer and one Django/CSS engineer working in parallel. Excludes content authoring, translation and photography.

| Workstream | Days |
|---|---|
| Fonts (licence, subset, self-host, QA gates), tokens, base, grid, breakpoints | 5 |
| The six devices as tested components (folio, rules, entry, margin, plate, verso) | 8 |
| Navigation: masthead, two-tier nav, running head, drawer as `<dialog>`, rail, breadcrumb, search | 7 |
| The 14 page archetypes as base templates + the archetype assertion test | 10 |
| Home + four hubs + Forum recomposition | 9 |
| Reference / article / legal / glossary / FAQ / news recomposition | 6 |
| Platform: shell, case header, next action, dashboard, list, detail, wizard, role-resolved navigation | 18 |
| Arabic type system, `.prescribed`, bidi isolation rework, CI gates | 6 |
| Accessibility: the four critical and seven high findings, forced-colors layer, focus-ring contract | 6 |
| Visual QA matrix (10 widths × 4 languages × 2 gate states + forced colours), design-system chapter, ADR updates | 6 |
| **Total** | **≈ 81 person-days** |

≈ 16 calendar weeks with one designer and one engineer; ≈ 9 weeks with two engineers. The platform workstream (18 d) is the largest single item and is also the one with the most product risk, because it depends on a `CaseFile` model that does not exist; it can begin against derived state (§14.2) without waiting for it.

**Separate line:** documentary reportage of the Forum, Rovigo, 2 October 2026 — one photographer, one day, ~12 usable frames with place, date and credit. Until it exists the site ships with zero photographs, which is the designed state.

### 18.3 Acceptance gates — how you know the direction shipped

Automated, in CI, each one a direct answer to a critique finding:

1. No page renders two consecutive sections of the same **rank** or the same **body type**; every page uses ≥4 of the 6 body types and ≥2 grounds.
2. Every route declares exactly one **archetype**.
3. At 1920, the widest band on every page uses **≥1440px**; at least two bands per page differ in container width.
4. `--t-band : --t-prose` ≥ **2.2** at ≥1200 and ≥ **1.6** at 390.
5. Home at 390 ≤ **5 viewport heights**; all four audience routes complete within **1.5**.
6. Zero `border-radius` > 2px outside `.step-marker`; zero `box-shadow` outside `.nav-drawer` and `dialog`; zero `backdrop-filter`; zero gradient.
7. `<figure>` without `<figcaption>` = build failure. Every `<figcaption>` contains place, date and credit.
8. Every text block has a `max-inline-size`; no rendered line exceeds **68 characters**.
9. Zero uppercase strings in the `.po` catalogues for title fields; zero `text-transform: uppercase` outside `.folio` and `.display--caps`.
10. No non-zero `letter-spacing` reachable under `:lang(ar)`; every Arabic line-height ≥ its font's bounding box; per-route Arabic share meets its budget.
11. Every `input[type=radio|checkbox]` ≥ 24px; every interactive row ≥ 44px below 1024; the first 20 tab stops on each archetype have a focus ring ≥3:1 **against the surface it is drawn on**.
12. With `java_script_enabled=False`, the header occupies <25% of the viewport at 320, 390, 768 and 1024, and no `.reveal`-style rule hides content.
13. The four audience rows are present in header **and** footer, in both gate states, in four languages.
14. One forced-colours capture per archetype in the screenshot matrix.

---

*End of ART DIRECTION A — European Institutional Editorial.*