# ART DIRECTION C — Digital Public-Service / Mediterranean Cooperation

**Key:** `direction-c` · **Date:** 20 September 2026 · **Status:** proposal for decision
**Applies to:** the public site and the authenticated platform of Italy Legal Entry™ (AGAMI — Dialogo Giuridico Interculturale APS)
**Read with:** `docs/qa/visual/before/` (the rejected build), the Design Council critiques, `benchmark-italia-eu`, `benchmark-portals`

This document is written so that a designer can draw from it and a Django/CSS engineer can build from it without asking a question. Every number is a decision, not an illustration. Where a value must be verified at build time it says so.

---

## 0. What this direction refuses

Before the idea, the boundary. This direction is not a re-skin of the current build; it inverts four of its structural assumptions. If any of these four survive, the direction has not been implemented:

| The current build | Direction C |
|---|---|
| Serif for display, sans for text (19.2% of words in serif on the best page, 3.8% on the worst) | **Grotesque for display, structure and interface; serif for reading.** Target 60–75% of running words in the serif. |
| One container (1200px) for every band at every viewport (7 of 7 on home at 1440 *and* at 1920) | **Container is a function of viewport and of section rank.** At 1920 the page uses 1440, not 1200. |
| Gold/bronze accent doing eight unrelated jobs (38 declarations in `components.css`) | **No gold. No bronze. Anywhere.** The accent is a single sea-teal with one job: *position and interaction*. |
| A brochure whose first screen is a stock photograph and whose IA is 492px below the fold | **A service counter.** The four audiences, the four tasks, and the "what we do not do" statement are in the first screen, on the darkest surface, with no photograph. |

And the pattern-level refusals, stated once so they can be tested: radius > 0 on any rectangle; `box-shadow` on any page element; `backdrop-filter` anywhere; any gradient; any uppercase string typed into content; any decorative icon; any card whose siblings are homogeneous; any empty state drawn as a dashed box with a centred icon; any counter; any element that fades in on scroll.

---

## 1. The idea

**The service is the object, and the service is made of steps, actors and responsibilities. The site is not a publication about a service — it is the front counter of one.** Everything the visitor meets is either a *task they can do*, a *step in a procedure*, an *actor who is responsible for that step*, or an *honest statement of what this organisation cannot do for them*. The register is the best of contemporary digital public service — plain, task-first, legible to someone reading their third language, accessible by construction — but the material is Mediterranean rather than administrative: grounds of limestone and sand rather than grey, an ink that is blue-green-black like deep water rather than corporate navy, a sea-teal for everything interactive, an olive reserved strictly for the Italy–Morocco cooperation axis, and a clay-terracotta for warnings. The proprietary graphic language is not ornament: it is **a measured route rule** — a hairline with stations, a filled marker for where you are, and a visible break where responsibility crosses from one shore to the other. It appears at three scales, it is the site's signature, and it is drawn only where a real sequence exists. The authenticated platform is not a second design; it is the same counter seen from behind, where the route rule carries a real case.

**The sentence a stakeholder says:**
> « En trois secondes je sais ce que je peux faire ici, qui décide quoi, et ce que ce site ne fera jamais à ma place. »

**The sentence the client can repeat to a Prefect:**
> "It looks like a serious cross-border public service, built in the Mediterranean rather than in a Nordic government IT department — and it never once pretends to be the State."

---

## 2. Grid

### 2.1 Base

- **Base unit 4px.** Every vertical value, every line-height, every padding is a multiple of 4. Enforced by a stylelint rule on `padding-block`, `margin-block`, `line-height`, `gap`.
- **Columns:** 4 (xs) · 8 (sm, md) · 12 (lg, xl).
- Content decides the column count within the grid — this is the .italia rule (*"è buona prassi che sia il contenuto a determinare il numero di colonne"*) and it is the formal licence for the asymmetry required here.

### 2.2 Breakpoints

| Name | Min-width | Columns | Gutter | Page margin | Rationale |
|---|---|---|---|---|---|
| `xs` | 0 | 4 | 16px | 16px | 320–599. One composition, authored, not reflowed. |
| `sm` | 600px | 8 | 20px | 24px | **Split layouts activate here, not at 896px.** Fixes the 768–895 orphan band where the current hero is 1094px tall against a 1024px viewport. |
| `md` | 900px | 8 | 24px | 40px | Tablet landscape / small laptop. Rails appear. |
| `lg` | 1200px | 12 | 28px | 56px | Full 12-column composition. |
| `xl` | 1600px | 12 | 32px | centred | Container reaches its cap. |

Media queries are written `min-width` only, in `rem` (`37.5rem`, `56.25rem`, `75rem`, `100rem`), and there are exactly five of them in the system. A component may not invent a sixth.

### 2.3 Containers

```css
--w-page:   min(100% - (2 * var(--margin)), 90rem);   /* cap 1440 */
--w-read:   36rem;   /* 576px — ~68 characters of Source Serif 4 at 18px */
--w-lead:   30rem;   /* 480px — ~52 characters at 22px */
--w-note:   20rem;   /* 320px — marginalia, panel content */
--w-form:   34rem;   /* 544px — single-column forms */
```

Computed container width at each capture width:

| Viewport | Margin | Container | Column | Cols 1–8 (work) | Cols 10–12 (panel) |
|---|---|---|---|---|---|
| 390 | 16 | 358 | 77.5 (4col) | — | — |
| 768 | 24 | 720 | 72.5 (8col) | — | — |
| 1024 | 40 | 944 | 97 (8col) | — | — |
| 1280 | 56 | 1168 | 71.7 | 675 | 243 |
| 1440 | 56 | 1328 | 85.0 | 876 | 311 |
| 1600 | 56 | 1488 → **1440** | 92.7 | 954 | 334 |
| 1920 | auto | **1440** | 92.7 | 954 | 334 |

**The number that matters: 1440 at 1920, not 1200.** The benchmark systems reach 1320 (.italia XXL) and 1368 (ECL XL); a page that freezes at 1200 and converts 480px of a 1920 screen into margin is the defect the client named. Above 1600 the container stops growing and the *margins* grow — but they grow having already spent 1440.

### 2.4 The three named layouts

**L1 — SERVICE.** No rails. Full-bleed bands stacked, each band holding its content in `--w-page` or going edge to edge. Used for: home, audience hubs, the model page, the Forum, the pilot. This is the default and the most common.

**L2 — SPACE.** Local navigation cols 1–3 (sticky, `top: var(--chrome-h)`), content cols 4–12. Used for: pages inside a space (Personnes, Entreprises, Institutions, Universités) and the legal set. Below `md` the rail becomes a horizontal scrollable segmented rule above the content, 44px tall, never a cloud of pills.

**L3 — READING.** Content cols 1–8 capped at `--w-read`; **marginalia cols 10–12** capped at `--w-note`. Used for: articles, pathway sheets, glossary entries, legal notices, FAQ answers. The marginalia column carries the date, the source, the responsible authority, the "ce que la plateforme ne fait pas" note, and the related links — aligned to the first baseline of the block it annotates. **If a page has no marginalia, it does not get L3; it gets a centred `--w-read` column inside the container.** A 576px column at the left edge of a 1200px container with nothing to its right is the defect; this rule makes it structurally impossible.

**L4 — WORK.** The platform. Left rail 248px, work column fluid, right case panel 320px. Specified in §14.

### 2.5 When a section may break the grid

A section may leave `--w-page` only under one of these five conditions, and the template must declare which:

1. **Ground change.** The band carries a different ground (`--ground-institution`, `--ground-process`, `--ground-cooperation`) and therefore must run edge to edge, because a coloured band that stops at a container edge reads as a card.
2. **Photograph.** A photograph at 100vw (see §6).
3. **Route rule, scale L.** The full-bleed sequence band (§7.2).
4. **Data table wider than the container.** Inside `.scroll-x`, which always emits `role="region" tabindex="0" aria-label`.
5. **The masthead, the services panel and the footer**, which are chrome.

Ceilings: **at most two full-bleed bands per page, never adjacent.** A page with three is over-designed; a page with zero is a document, which is legitimate for the legal set.

Inversely, a section may go *narrower* than the container — `--w-read` centred — only for continuous legal or explanatory prose, and never more than twice per page.

---

## 3. Typography

### 3.1 Families

| Token | Family | Licence / source | Axes used | Role |
|---|---|---|---|---|
| `--font-ui` | **Archivo** (Omnibus-Type) | OFL, variable | `wght 400–700`, `wdth 87–100` | All headings, navigation, buttons, labels, table content, data, forms, the wordmark, reference codes |
| `--font-read` | **Source Serif 4** (Adobe) | OFL, variable | `wght 400–600`, `opsz 8–60` | Lead paragraphs, body prose, notices, definitions, FAQ answers, legal text, pull-quotes, captions in editorial contexts |
| `--font-ui-ar` | **Readex Pro** | OFL, variable | `wght 400–700`, `HEXP 0–35` | Arabic equivalent of `--font-ui` |
| `--font-read-ar` | **Noto Naskh Arabic** | OFL, variable | `wght 400–700` | Arabic equivalent of `--font-read` |

There is **no monospace family.** Reference codes, case numbers and rule identifiers are set in Archivo at `wdth 87` with `font-variant-numeric: tabular-nums lining-nums slashed-zero` and `+0.06em` tracking. This closes open gate G-15 (`--font-mono: "IBM Plex Mono"` declared with zero `@font-face` rules and zero files shipped, so the "technical reference" register is currently Consolas on Windows and Menlo on macOS) by deleting the need rather than shipping a fourth family, and it keeps references in the institutional voice instead of the terminal one.

All four are self-hosted as `woff2`, subset by `unicode-range` (`latin`, `latin-ext`, `arabic`), `font-display: swap`, no third-party request, licence recorded in `docs/FONT_LICENSES.md`. The variable files ship **once per family**, not once per weight — the current build ships `ibm-plex-sans-400/500/600-latin.woff2` as three byte-identical copies of one variable font, 153,352 bytes of duplicate payload.

### 3.2 Why these, and not the incumbents

**Against IBM Plex Serif/Sans (the incumbent).** ADR-008 justifies Plex as "istituzionale ed europea, distinta da gov.it" — the criterion is *avoiding Titillium*, not *achieving distinction*. Plex was commissioned by IBM as the corporate voice of a technology company and is the single most-deployed open "serious tech" superfamily of the decade; it is the first suggestion nearly every tool returns for "institutional open pairing", which is the literal mechanism behind the client's phrase "a standard AI-generated website". Beyond taste, it lacks three things this project needs and cannot fake: no true small caps in any Plex family (so the build substitutes `text-transform: uppercase` at 12px with 0.12em tracking in 22+ rules — the SaaS eyebrow the client banned), no oldstyle figures (so dates punch cap-height holes through lowercase prose), and no optical size axis (the same outlines run from 12px to 64px, a 5.3× range, which is why the 48px H1 reads soft and inflated).

**Against Titillium Web.** In Italy this face *is* the government website, the way Transport is the British road sign. Using it would be impersonation, and §6 of the benchmark research forbids it outright.

**Against Inter, Public Sans, Source Sans, Work Sans.** Unmarked. Public Sans is the US federal system's face. These solve nothing.

**Against Arial (ECL's choice).** Correct for Europa, which needs to be unremarkable and universally installed. We need to be distinctive; Arial delivers neither institution nor distinction.

**For Archivo.** A grotesque drawn by Omnibus-Type for highlights and headlines with a **real width axis (62–125)**, which is the deciding factor: one family covers the display register (`wdth 100`), the interface register (`wdth 100`), the dense-data register (`wdth 92`) and the reference register (`wdth 87`) without a second family and without condensing by transform. It carries tabular and lining figures, a slashed zero, complete Latin-Ext for French and Italian diacritics, and nine weights. Its squared terminals and open apertures read as *civic signage and timetables* — a public-transport, station-board register — which is exactly the service idea. It is not a SaaS default.

**For Source Serif 4.** A transitional serif with a genuine **optical size axis (opsz 8–60)**: the 18px body and the 40px pull-quote are drawn from the same file with different contrast and spacing, which is the precise thing Plex cannot do. Warm, designed for extended screen reading, true italics, oldstyle and lining figure sets. It is placed where .italia places Lora — *for long reading*, not for display — which is the structural inversion that carries this direction.

**For Readex Pro.** One design covering Arabic with vertical metrics matched to Latin grotesques, plus an `HEXP` (horizontal expansion) axis that lets us widen Arabic interface text to compensate for its smaller apparent size **without faking weight**. It is drawn for high legibility for readers with limited literacy in the language, which is precisely the primary audience of this project. Used in humanitarian and multilateral contexts, not in SaaS.

**For Noto Naskh Arabic.** A true naskh is the correct cross-script counterpart to a reading serif, and naskh is the register of Moroccan administrative documents. IBM Plex Sans Arabic's kufi-influenced construction is a register mismatch against any serif, and today it does *all six levels* on `/ar/` because `tokens.css:215` remaps both `--font-display` and `--font-body` to it.

**Acceptance test before any of this is signed off:** render Archivo 400/500/600 and Readex Pro 400/500/600 at 100px, measure total ink, and require agreement within **5%**. The current Plex pair achieves 3%; a swap that regresses that is rejected. Then repeat for Source Serif 4 against Noto Naskh Arabic.

### 3.3 The scale

Eight roles. Four display ranks (per .italia: "non superare quattro livelli di titolo per pagina"), four text ranks. Sizes are stepped at breakpoints, **not** fluid-clamped — a clamp is why the current hierarchy flattens exactly where the screen is smallest (H1:H2 falls from 1.42 at 1440 to 1.32 at 390).

| Role | Family / instance | Weight | 390 | 600 | 900 | 1200 | 1600 | Tracking |
|---|---|---|---|---|---|---|---|---|
| `t-statement` | Archivo `wdth 100` | 600 | **40 / 44** | 52 / 56 | 64 / 68 | 76 / 80 | **88 / 92** | −0.02em |
| `t-title` | Archivo `wdth 100` | 600 | 30 / 36 | 34 / 40 | 38 / 44 | 42 / 48 | 44 / 52 | −0.015em |
| `t-section` | Archivo `wdth 100` | 600 | 24 / 32 | 26 / 32 | 28 / 36 | 30 / 36 | 32 / 40 | −0.01em |
| `t-sub` | Archivo `wdth 100` | 600 | 19 / 28 | 20 / 28 | 20 / 28 | 21 / 28 | 22 / 32 | 0 |
| `t-lead` | Source Serif `opsz 26` | 400 | 19 / 28 | 20 / 32 | 21 / 32 | 22 / 32 | 23 / 36 | 0 |
| `t-body` | Source Serif `opsz 18` | 400 | 17 / 28 | 17 / 28 | 18 / 28 | 18 / 28 | 18 / 32 | 0 |
| `t-ui` | Archivo `wdth 100` | 500 | 16 / 24 | 16 / 24 | 16 / 24 | 16 / 24 | 16 / 24 | 0 |
| `t-micro` | Archivo `wdth 100` | 400 | 13 / 20 | 13 / 20 | 13 / 20 | 13 / 20 | 13 / 20 | +0.005em |

Two further instances, not ranks:

- `t-label` — Archivo `wdth 88`, weight 650, **13 / 16**, `+0.08em`, `text-transform: uppercase` **applied in CSS, never typed in content**. This is the *only* uppercase register in the system. Permitted on: table column headers, state chips, the responsible-actor mark, rail group titles, photograph credits' prefix, the route rule's shore markers. Forbidden everywhere else, and forbidden on any heading.
- `t-ref` — Archivo `wdth 87`, weight 600, **15 / 20**, `+0.06em`, uppercase, `font-variant-numeric: tabular-nums lining-nums slashed-zero`. Case references, ruleset versions, ordinals in indexed lists, dates in a date gutter.

**Ratios at 1440** (compare the current build: display:h2 = 1.90, h1:h2 = 1.42, h2:body = 2.11, and eight tokens crushed into a 9px band below 24px):

- `t-statement` : `t-body` = 88 : 18 = **4.89**
- `t-statement` : `t-section` = 88 : 32 = **2.75**
- `t-title` : `t-section` = 44 : 32 = 1.38
- `t-section` : `t-body` = 32 : 18 = **1.78** — deliberately below the ECL 2.25, because the family change (grotesque → serif) does part of the work that pure size does in a single-family system. A heading in Archivo 600 over a paragraph in Source Serif 400 is unmistakable at 1.78; the same 1.78 inside one family would not be.
- `t-body` : `t-micro` = 18 : 13 = 1.38 — a real step, not the 1.067 that separates `--font-size-small` from `--font-size-body` today.

**Deleted tokens:** `--font-size-h4` (18px, smaller than the lead at every width above 390), `--font-size-label`, `--font-size-button`, `--font-size-legal`, `--font-size-caption`, `--font-size-eyebrow`. Eleven size tokens become eight roles plus two instances, and **no two of them carry the same value**.

### 3.4 Measure, figures, features

- Prose: `max-inline-size: var(--w-read)` — 576px, ≈68 characters of Source Serif 4 at 18px. Applied to `.prose`, `.notice__body`, `.glossary__definition`, `.faq__answer`, `.section__text`, `.forum__body` — every one of which today ships with `max-inline-size: none` (the FAQ answer measures 1136px ≈ 151 characters at 1280; the glossary definition 147 characters at 1440).
- Lead: `var(--w-lead)` — 480px, ≈52 characters at 22px.
- Marginalia / panel: `var(--w-note)` — 320px, ≈46 characters at 15px.
- `ch` is **not** used as a measure unit. Measured average lowercase advance for Archivo at 16px is ~7.9px against a digit advance of 9.6px — a 1.21 ratio — so a `ch` cap of 68 renders ~81 characters. All measures are `rem`, calibrated against real strings and re-verified when a family changes.
- **Figures:** `font-variant-numeric: oldstyle-nums proportional-nums` on `t-body` and `t-lead` in running prose (Source Serif has a real oldstyle set); `lining-nums tabular-nums slashed-zero` on every `td`, `th`, `time[datetime]`, `.deadline`, `.ref`, `.route__tick`, and every portal metric — declared as **one rule in `base.css` keyed on those selectors**, not as seven scattered component rules.
- `font-feature-settings: "kern" 1, "liga" 1, "calt" 1` globally; `"case" 1` on `t-label` and `t-ref` so accented capitals and punctuation sit correctly.
- Leading is bound to measure, not to a style name: ≤52 characters → 1.3–1.45; 52–68 characters → 1.55–1.6; anything at 13–15px → 1.55 minimum. The current system does the inverse (1.7 on a 45-character lead, 1.5 on 147-character definitions).

### 3.5 Arabic metrics

The `:lang(ar)` block sets **twelve tokens, not four**, and every one of them adds rather than deletes:

```css
:lang(ar) {
  --font-ui:   var(--font-ui-ar);
  --font-read: var(--font-read-ar);

  /* Arabic ink height at 16px measures ~5px against a Latin x-height of ~7px:
     Arabic at 16px reads like Latin at ~11.5px. Compensate on text ranks only. */
  --scale-text: 1.08;          /* t-body, t-ui, t-label, t-micro, t-ref */
  --scale-display: 1.00;       /* t-statement, t-title — the alef is already tall */

  --lh-statement: 1.30;
  --lh-title:     1.32;
  --lh-section:   1.40;
  --lh-sub:       1.50;
  --lh-lead:      1.70;
  --lh-body:      1.85;
  --lh-ui:        1.75;

  --tracking-display: 0;
  --tracking-title:   0;
  --tracking-section: 0;
  --tracking-label:   0;
  --tracking-ref:     0;
  --case-label: none;          /* consumed as text-transform: var(--case-label) */
}
```

The evidence these replace: at the current Arabic H2 setting (33.76px / line-height 1.15 = 38.82px), two consecutive lines of vocalised Arabic **overlap by 12.2px** — line 1's ink ends at y=44 while line 2's ink begins at y=31.8 — because Plex Sans Arabic's font box at 48px is 52+20 = 72px forced into a 55.2px line box, and `--leading-*` is never adjusted for Arabic. Separately `--tracking-tight: -0.01em` is applied to `h1–h6` unconditionally in `base.css:118` and never reset in the `:lang(ar)` block, so every Arabic heading in the shipped build carries negative tracking against the team's own documented rule.

**The mechanism matters as much as the values.** Every locale-sensitive decision lives in a token; **no component may ship a `:lang(ar)` twin.** The current system has nine `:lang(ar)` rules, all of which only delete (`text-transform: none`, `letter-spacing: 0`), and the hand-maintained list already has holes — `components.css` carries 15 `letter-spacing` declarations against 7 resets, and the entire Forum component is uncovered (`.forum-hero__eyebrow` computes +1.792px). A static test fails the build when any rule sets a non-zero `letter-spacing` reachable under `:lang(ar)`.

**Hard floors:** nothing in Arabic below **15px** (this retires the 12px eyebrow by construction). `font-weight` above 700 is banned in Arabic — only 400/500/600/700 are subset, and the browser's synthetic bold smears the joins.

---

## 4. Navigation

### 4.1 Chrome height — one token, computed in CSS

```css
:root { --chrome-h: calc(var(--utility-h) + var(--masthead-h)); }
/* xs: 0 + 56 = 56 ; sm+: 36 + 68 = 104 */
```

`--chrome-h` is consumed by: the mobile sheet's `inset-block-start`, the sheet's scrim, `html { scroll-padding-block-start }`, every sticky sub-navigation, every `scroll-margin`, and the platform's case header. **No JavaScript writes geometry.** The current build writes `--nav-drawer-top` from `getBoundingClientRect()` onto the drawer only, so its sibling overlay is painted 41px too high and covers 59% of the close button, dropping its label contrast from 13.52:1 to 3.92:1.

Below `lg`, `html.no-js .site-header { position: static }`. Without this the header is **781px tall** on a phone without JavaScript and the page is unreachable at 1024×768.

### 4.2 Utility bar — 36px, `--ground-institution`

Left (inline-start): `AGAMI — Dialogo Giuridico Interculturale APS · promoteur`, wrapped in `<bdi lang="it">`, `t-micro`. **It may wrap to two lines on narrow viewports; it may never be truncated.** Today it is clipped to 146 of 263px at 320, and because the Latin run is not isolated, in Arabic the ellipsis falls on the *beginning* — the visible string becomes "… — Dialogo Giuridico Interculturale APS" with the promoter's own name cut off.

Right (inline-end), in this order: **language as four inline items** (`العربية · Français · Italiano · English` — current language first, then by audience; not a dropdown, four options do not need disclosure), then `Aide` (the WCAG 3.2.6 *Consistent Help* affordance, identically placed on every page of both the public site and the platform), then `Mon espace`. Each is 36px tall with a 44px touch target achieved by padding.

Below `sm` the utility bar does not render; its contents move into the sheet, and `Aide` gains a persistent position as the last row of the sheet **and** the last row of the footer, so it is always reachable in two gestures.

### 4.3 Masthead — 68px, `--ground-page`, 1px `--rule-strong` below

Inline-start: the **lockup** (§7.4) with `min-inline-size` reserving 1× cap height (≈22px at 1440) of clear space — today the wordmark's right edge is at x=338 and the first nav item begins at x=343, five pixels away.

Centre: **the search field, always visible at `md` and above.** 44px tall, 280px wide, `--ground-raise`, 1px `--rule-strong`, no radius, placeholder "Rechercher une démarche, une fiche, un terme". A service without search is a brochure; today `type="search"` appears **zero times** on the home page, and the only two search boxes in the build sit inside the FAQ and the glossary, both of which 404 on the live public site.

Inline-end: four audience items — **Personnes · Entreprises · Institutions · Universités et formation** — then `Démarches`, then a `t-label` `Forum` and `Projet`.

**The four audiences are permanent in the header and in the footer, in every gate state, in every language.** What the gate changes is the *destination*, not the row: `MenuItem` gains a `fallback_url_name`, so Institutions resolves to the space when G3 is open and to an honest interim page when it is closed. Today `cms_nav.py:109–110` and `:130–131` delete the rows entirely while the home page's own body still announces "chaque acteur dispose de son espace" and links to forms — the chrome contradicts the content on the same page, and `/fr/institutions/` returns 404. A compliance test asserts exactly four audience rows in the header and in the footer, in both gate states, in all four languages.

Current item: **three co-signals**, never colour alone — weight 500→650, a 2px `--rule-sea` under the item, and `aria-current="page"`. The hover state uses the rule at 50% inline-size so hover and current are never pixel-identical (today they are).

### 4.4 The Services panel — one panel, not seven

`Démarches` opens **a single full-bleed panel** under the masthead: `--ground-process`, max-block-size 60vh, non-modal (no overlay, no scroll lock, no `inert` needed), Esc closes, focus returns to the trigger, the trigger *is* the disclosure (not an adjacent 32×44px chevron).

Contents: the whole service index as task rows in three columns — `Je veux travailler en Italie`, `Je veux me former avant de partir`, `Mon entreprise cherche des profils`, `Nous voulons proposer une coopération`, `Je veux comprendre les parcours réguliers`, `Je veux vérifier une offre suspecte`, `Je cherche un terme`, … Each row: `t-ui` task + `t-micro` gloss + `→`, full-row target, 1px hairline between, 48px tall.

This deletes the per-item mega-menu, whose "Personnes" panel today is a 576×211px box containing the word "Personnes", a description, and **two links that both point at the page you already clicked** — because six of seven children are gated — and which is mis-anchored 224px to the left of its own trigger.

### 4.5 Mobile — a sheet, not a 72%-empty drawer

Trigger: 44×44 `Menu` button in a 56px bar, inline-start; lockup C centred; search glyph inline-end.

The sheet is `position: fixed; inset: 0; padding-block-start: env(safe-area-inset-top)`, `role="dialog" aria-modal="true"`, `inert` on `<main>` and `<footer>`, scroll locked with the `position: fixed; top: calc(var(--scroll-y) * -1)` pattern (restoring `scrollTo` on close — `body { overflow: hidden }` alone does not hold on iOS and loses scroll position). Enter `translateY(-100%) → 0` over 200ms; exit 140ms.

Order inside the sheet — and this is the *phone information architecture*, which today does not match the desktop one at all:

1. Search field (56px)
2. Rule
3. **Four audience rows**, 56px each, each with the XS route rule showing how many steps that audience's path has
4. Rule, `t-label` "Démarches"
5. The service index, 48px rows
6. Rule, `t-label` "Le projet"
7. Forum · Projet · Actualités · Partenaires
8. Rule
9. FAQ · Glossaire · Contact · **Attention aux fraudes**
10. Language, four inline items, 44px
11. `Mon espace`

Today the drawer contains four top-level rows in a 731px panel — 523px, 72%, blank — and Institutions and Universités, which the home page calls "les quatre accès", are not in it.

### 4.6 Breadcrumb

Derived from the same menu tree as the navigation, never per-view. Present only at depth ≥ 2 (ECL: *"do not use if your website's navigational structure is less than 3 levels deep"*). Current page last and **unlinked**. Labels match page titles exactly. Below `sm`, collapses to `↑ Espace Personnes` — the parent only. Today every breadcrumb is `Accueil > current page` while the header underlines "Personnes" as the current section and the side rail says "Le projet" — three hierarchies, three answers.

### 4.7 Side navigation (L2)

`t-label` group title, then 44px rows with 1px hairlines. Current: 2px `--rule-sea` on the inline-start edge + weight 650 + `aria-current`. Sticky at `top: var(--chrome-h)`. At `md` and below it becomes a horizontally scrollable segmented rule, 44px tall, inside `.scroll-x` — never the 999px-radius pill cloud that currently makes the portal's own navigation **34px on a phone and 40px on a desktop**.

### 4.8 How the platform shell differs while staying in the family

Same type, same colours, same rules, same route device, same focus ring. Six deliberate differences:

| | Public | Platform |
|---|---|---|
| Masthead ground | `--ground-page` (light) | `--ground-institution` (dark), 48px |
| Primary navigation | Four audiences + Démarches + search | **None.** The rail is the navigation. |
| Footer | Full site map, three `<details>` on phone | **A 48px legal strip**: legal links · support · ruleset version |
| Rails | L2 left rail only on space pages | Left rail 248px always + right case panel 320px |
| Vertical rhythm | Rank A/B/C: 96/64/40 at `lg` | Uniform 32px — density is the point |
| Container | `--w-page`, capped 1440 | Full width minus rails, **no cap** |

The platform extends `templates/shell_platform.html`, which does **not** extend `base.html`. Today `base_portal.html:1` does, so a signed-in person's dashboard carries 24 marketing links above it and a 484px public footer below it — on the deadlines page, marketing furniture 1.8× taller than the work.

---

## 5. Colour philosophy

### 5.1 The principle

**Every colour has exactly one structural job. If you cannot say what a mark's colour *means*, the mark is wrong.** Five colours, four grounds, four rules. Nothing else exists.

And one rule that is an argument, not a preference:

> **No colour on this site ever means "approved".** We approve nothing; we issue nothing; we authorise nothing. There is no green success state anywhere in the public site or the platform. A step that is finished is *TRANSMIS* or *CLOS* — a fact about the file, not a verdict. Green is reserved entirely for the Italy–Morocco cooperation axis, where it means *bilateral*, not *yes*.

This single decision does more institutional work than any layout change: it makes the interface structurally incapable of implying an authority we do not hold, which is the exact line PRODUCT §2 and the home page's own "Ce qu'elle ne fait pas" section are trying to hold in prose.

### 5.2 Light tokens (default)

```css
:root {
  /* GROUNDS — the page changes ground to change register */
  --ground-page:        #FBF8F2;  /* limestone — the site explains */
  --ground-raise:       #FFFFFF;  /* inputs, table zebra, sheet */
  --ground-process:     #F2EDE2;  /* sand — procedures, steps, forms, results */
  --ground-inset:       #E9E2D3;  /* a recess inside a process band */
  --ground-institution: #0E2027;  /* deep ink-teal — the institution speaks */
  --ground-cooperation: #23382E;  /* deep olive — Italy–Morocco axis only */

  /* INK */
  --ink:          #101C22;  /* 15.98:1 on --ground-page */
  --ink-2:        #38484F;  /*  8.97:1 */
  --ink-3:        #5E6E74;  /*  5.00:1 — muted, the floor for text */
  --ink-on-dark:  #F4F0E8;  /* 14.74:1 on --ground-institution */
  --ink-on-dark-2:#B9C6C9;  /*  9.55:1 */

  /* SEA — interaction and position. The only interactive colour. */
  --sea:          #0A5C68;  /*  7.22:1 — link text, active state */
  --sea-strong:   #073F48;  /* 11.3:1 white-on — filled control ground, current marker */
  --sea-rule:     #0E7C8B;  /*  4.63:1 — 2px rules, focus ring, route current segment */
  --sea-tint:     #E4EFF0;  /* ground of an information notice */
  --sea-on-dark:  #7FD0DC;  /*  9.53:1 on --ground-institution */

  /* OLIVE — the cooperation axis. Never a state. */
  --olive:        #3F5D3C;  /*  6.97:1 */
  --olive-tint:   #EBF0E4;
  --olive-on-dark:#A9C79A;  /*  9.02:1 */

  /* CLAY — attention, caution, deadline, fraud warning */
  --clay:         #8C3517;  /*  7.51:1 */
  --clay-rule:    #B8542E;
  --clay-tint:    #FAEDE6;
  --clay-on-dark: #F0A68A;  /*  8.39:1 */

  /* REFUSAL — an error, a refused submission, a STOP outcome */
  --refusal:      #8E1F2B;  /*  8.32:1 */
  --refusal-tint: #F9E9EA;

  /* RULES — four values, four jobs, no fifth */
  --rule-hair:   #D8D0C0;  /* 1.45:1 — separation only; never the sole boundary of a control */
  --rule-strong: #8E8676;  /* 3.42:1 — input borders, table structure (WCAG 1.4.11) */
  --rule-ink:    #101C22;  /* 2px — opens a band or a table. Once per band. */
  --rule-sea:    #0E7C8B;  /* 2px — current position, and nothing else */

  /* FOCUS — an inseparable pair. --focus-halo is redeclared per surface. */
  --focus-ring:  var(--sea-rule);
  --focus-halo:  var(--ground-page);
}
.on-dark { --focus-ring: var(--sea-on-dark); --focus-halo: var(--ground-institution); }
```

All contrast figures above are computed against `--ground-page #FBF8F2` (or against `--ground-institution` where stated) and are reproduced here to be re-verified in CI, not trusted.

### 5.3 Structural assignments

| Colour | Job | Where it may appear | Where it may never appear |
|---|---|---|---|
| `--ground-institution` | The institution speaks | The home service band; one interior band per long page; the platform top bar; the footer | Twice on one page; as a card; as a button fill |
| `--ground-process` | A procedure is described | Step bands, forms, wizard, rule-outcome band, verdict panels | As alternating stripes to "break up" a page |
| `--sea` family | Interaction and position | Links, buttons, the focus ring, the route's current marker, `aria-current` rules, info notices | As a decorative rule, as a heading colour, as a background wash |
| `--olive` family | The Italy–Morocco axis | The Forum band, the pilot, the partner/network page, the southern shore in the two-shores contour, the "Maroc" side of any responsibility diagram | As a success state, as a checkmark, as a generic accent |
| `--clay` family | Something requires care | Fraud warnings, deadlines, consequential actions, "form closed" notices | As a brand accent |
| `--refusal` | Something failed or is refused | Form errors, a STOP rule outcome, a rejected document | On a required-field marker (use the word « obligatoire ») |

**Notices** are a two-axis taxonomy, following the benchmark: the *trigger* axis (info / caution / error, from ECL) and the *editorial* axis (Note / Important / Approfondissement, from .italia). Anatomy, one component: 4px inline-start rule in the family colour, a 5% tint ground, a `t-label` title, body in `t-body` serif capped at `--w-read`, an optional 24px icon. No shadow — the tint is the separation. The legal disclaimers this project is full of ("pré-évaluation à caractère informatif", "ne se substitue jamais aux autorités compétentes") become *Important* notices with a real title, not grey footnotes.

### 5.4 Dark mode

**Shipped, not deferred.** A service consulted on a phone at night by someone comparing an offer against our fraud warning gets a dark interface if their system asks for one. `prefers-color-scheme` plus an explicit three-state toggle (`système / clair / sombre`) in the utility bar, stamped as `data-theme` on `<html>`.

The elegant part: **the institutional band is always the opposite of the page ground.** In dark mode `--ground-institution` becomes `#F4F0E8` and its text becomes `--ink` — the inversion device survives by flipping, so there is no second design to draw and no band that disappears.

```css
:root[data-theme="dark"], :root:not([data-theme="light"]) { @media (prefers-color-scheme: dark) {
  --ground-page:#0D1418; --ground-raise:#131C21; --ground-process:#151F24; --ground-inset:#1C272C;
  --ground-institution:#F4F0E8; --ground-cooperation:#DDE6D6;
  --ink:#E9E4DA; --ink-2:#B3BEC1; --ink-3:#8B989C;      /* 6.24:1 on --ground-page */
  --ink-on-dark:#101C22; --ink-on-dark-2:#38484F;       /* i.e. ink on the inverted band */
  --sea:#6FC6D4; --sea-strong:#A8DDE6; --sea-rule:#3E9AA8; --sea-tint:#14272B;
  --olive:#A9C79A; --clay:#F0A68A; --refusal:#F2A3A8;
  --rule-hair:#2A343A; --rule-strong:#59666B; --rule-ink:#E9E4DA;
  --focus-halo:var(--ground-page);
}}
```

Every colour is defined on bare `:root` first; the dark block redefines only tokens. `body` always carries an explicit background.

### 5.5 Forbidden

Gold and bronze in any value. `#0066CC` and the Blu Italia ramp. `#0E47CB` / `#FFD633`. `#089994`. Any gradient, including "subtle" ones. `backdrop-filter` anywhere (the current `.site-header::before` blurs a 94%-opaque veil that by the team's own documentation is there to show nothing through — it is glassmorphism, on the banned list, active at all ten capture widths). Colour as the sole carrier of any state. Green as approval. More than one dark band per page. Tinted or coloured shadows. Any blue link that is not `--sea`. Hard-coded hex anywhere outside `tokens.css` — including inside SVG files, where `entrance-person.svg` currently bakes `#0f2b52`, `#9a7b2f`, `#fbfaf7` and `orientation.svg` adds `#1f6b48`.

---

## 6. Imagery

### 6.1 The rule that makes stock impossible

**No photograph renders without a caption, and the caption is `Lieu · Date · Crédit`.** This is enforced in the `{% photo %}` template tag, which raises on a missing field rather than rendering. Nothing else is needed to delete the current library, because there is nothing truthful to write under a frame of four strangers in hoodies around a reclaimed-wood table. Today the site renders six `<figure>` elements and **zero** `<figcaption>`, while `.prose figcaption` sits fully styled in `base.css:410`, unused.

### 6.2 Budget

- **At most one photograph per page.** At most **six** in the entire public site at launch. A page with none is the normal case — 44 of 52 public pages already have none, and that is correct; the error is the eight that have one for no reason.
- Nine of the fifteen licensed photographs never render anywhere: 4.83 MB of 6.99 MB shipped and unused. They are deleted from the repository. `docs/IMAGE_LICENSES.md` — the strongest artefact in this area, with its thirteen logged rejections and its forbidden-subject list — survives untouched as the gate for what replaces them.

### 6.3 Size, ratio, treatment

- **A photograph occupies either the full bleed (100vw) or columns 1–8. A photograph narrower than eight columns is forbidden.** This deletes the 484×363 hero thumbnail (11% of a 1440 viewport, 4% of its area) structurally rather than by taste.
- **Exactly two ratios: 3:2** (the library's native ratio, no crop — a document plate) and **2:1** (the full-bleed band). The build currently forces one 3:2 library into 4:3, 16:7, 16:9, 21:9 and no-ratio-at-all, every one of them with `object-position: 50% 50%`, so 2.286 and 2.333 coexist and no two images on any two pages align.
- `object-position` is stored **per asset in the manifest**, beside the existing `crop` field. It is never allowed to default.
- **Treatment: no radius, no shadow, no frame, no overlay gradient, no offset outline.** A 2px `--rule-ink` sits on the photograph's top edge; the caption sits below its bottom edge in `t-micro`, `--ink-3`, with the credit prefix in `t-label`. Delete `.home-hero__figure::before` (the offset gold rectangle that mis-registers below and right of the image, and in Arabic mirrors into a bare line running to the lower-left of nothing), delete `border-radius` and `box-shadow` from `.ecosystem-photo__img` and `.forum-hero`.
- **Grade, applied at ingest, one recipe:** shadows lifted so no pixel falls below 12% luminance, highlights held under 96%, white balance warm. This is what makes the set read as Mediterranean light rather than as a filter. It is a Lightroom preset and a documented ImageMagick pipeline, not a CSS effect.

### 6.4 Subjects

Two categories only.

**Territory** — the Polesine, the Rovigo skyline, the Adriatic edge, the Veneto industrial fabric, a provincial road; Moroccan ports, training institutes, civic architecture, a coastline.
**Document and room** — a register, stamped paper, an archive shelf, a counter, an empty assembly hall, a signed act, a queue-less desk.

**Banned, absolutely:** people at laptops; meeting tables; post-it walls (the pilot page currently carries a brainstorming wall of pink and yellow notes — startup iconography, not institutional cooperation); handshakes; airports; doors; thresholds; suitcases; queues; passports; the Colosseum, the Ponte Vecchio, gondolas.

### 6.5 When there are none

The page is carried by **ground changes** and by the **two-shores contour** (§7.3). A full-bleed `--ground-institution` band with a Statement replaces a hero image and is stronger than one. Until real reportage exists — the Forum of 2 October 2026 at the Sala della Gran Guardia is the obvious first commission — **the site ships with zero photographs.** A site with no pictures reads as sober; a site with six interchangeable stock pictures reads as a template, which is the verdict already delivered.

---

## 7. Iconography and the proprietary graphic language

### 7.1 Icons

One drawing system, defined once: **24×24 box, 1.75px stroke, butt caps, miter joins, `currentColor` only, no fill, no colour inside the file, 20 icons maximum.** A test fails the build on any literal hex inside `static/img/`.

Five permitted uses, from .italia, and no sixth: (1) an interaction function (send, upload, delete), (2) navigation (back, forward, external), (3) a content type (document, event, table), (4) a status that is *also* carried by a word, (5) nothing else.

**Always paired with a text label.** No icon in a heading. No icon inside a card header. No icon repeated to fill space — today `institutions__1280x800__fr.png` prints the identical classical-temple glyph on all six rows of one list, which conveys exactly zero bits. No emoji. The four entrance illustrations, the pilot growth-curve squiggle and the pediment glyph are deleted, not restyled; they are the weakest assets in the system.

### 7.2 « Le tracé » — the route rule

**This is the site's signature and the thing you would recognise printed in black on white.**

Anatomy:
- A **2px horizontal rule** in `--rule-ink` — the baseline of the procedure.
- **Station ticks:** 1px vertical strokes, 10px tall, descending *below* the line.
- **Station spacing** is proportional to real duration or real position where that is known; equal where it is not. It is never spaced for looks.
- **The current station** is an 8×8 filled square in `--sea-strong` sitting *on* the line, plus a 2px `--rule-sea` segment drawn from the origin to that square.
- **A shore change** — responsibility crossing from Morocco to Italy, or from the platform to an authority — is a **6px gap** in the rule with a `t-label` marker beneath it (`MAROC` / `ITALIE`, or `AGAMI` / `AUTORITÉ COMPÉTENTE`).
- Labels hang below the ticks in `t-micro`, `--ink-2`, left-aligned to their tick, never rotated, never truncated.

Three scales:

| Scale | Size | Where |
|---|---|---|
| **XS** | 64×12px, 3–8 ticks, no labels | Inside a list row, a nav row, a table cell: "step 3 of 7" |
| **M** | Full column width, labelled | Under a section title on a process page; in the platform case header |
| **L** | Full-bleed band, 96px tall, `--ground-process` | Once per page maximum — the model, the pilot sequence, the Forum cycle |

**Vertical variant** for timelines and the case file: the same rule rotated, ticks pointing into the date gutter, the current station square at the open phase.

**The lint rule that keeps it honest:** `.route` renders only from a data structure with ≥3 real steps, each carrying a label and a responsible actor. A route rule with fabricated or decorative stations fails the template test. This replaces the current 4+4 grid of 40px circles whose connector after step 4 runs to the container edge and stops, forcing the reader to jump down and back to the left for step 5 — a diagram that lies about its own reading order.

### 7.3 « Les deux rives » — the two-shores contour

A **single vector**: two open curves, 1.5px, facing each other across a measured gap. The northern curve (Veneto / Adriatic) sits on the top edge of a band; the southern curve (Moroccan coast) on the bottom edge. **It is not a map**: no borders, no country outlines, no flags, no dots for cities.

Used in exactly three places site-wide: the top edge of the footer, the Forum band, and the system/404 pages. **Once per page maximum.** `currentColor` at 8% opacity on light grounds, 14% on dark. In `--ground-cooperation` bands the southern curve takes `--olive-on-dark` and the northern `--ink-on-dark-2` — the only place in the system where the two shores are distinguished by colour.

This is the entire illustration vocabulary. There is nothing else.

### 7.4 The mark and the lockup

**The mark is the route rule compressed into a glyph:** a 2px horizontal bar in a 24×24 box, with three ticks and one filled square — the three initials I · L · E read as three stations, the square as "you are here". It works at 16px (favicon), in one colour, in forced-colours mode, and embroidered on a badge.

**Wordmark:** Archivo `wdth 92`, weight 600, tracking −0.005em, sentence case `Italy Legal Entry`. The ™ at 52% cap height, superior, tracked away from the "y", wrapped `dir="ltr" translate="no"` (the current implementation of this is correct — keep it exactly).

**Descriptor:** `t-label`, `Mobilité régulière Vénétie–Maroc` / `التنقل النظامي بين فينيتو والمغرب`. **Present in every language including Arabic**, which is the bilingual signal a Veneto–Morocco project currently lacks entirely.

**Three lockups:** A = mark + wordmark + descriptor (`lg` and above); B = mark + wordmark (`sm`–`md`); C = mark alone (`xs`, favicon, avatar). **Clear space: 1× cap height (≈22px at 1440) on all sides, reserved with `min-inline-size`, not hoped for.**

---

## 8. Spacing and vertical rhythm

Base 4px. Scale, named by value so nobody has to remember a t-shirt size:

```
--s-4 --s-8 --s-12 --s-16 --s-24 --s-32 --s-40 --s-48 --s-64 --s-80 --s-96 --s-128
```

Semantic tokens split by axis, following .italia's `stack` / `inline` / `inset` distinction:

```css
--stack-tight: 8px;   --stack: 16px;   --stack-loose: 32px;
--inline-tight: 8px;  --inline: 16px;  --inline-loose: 24px;
--inset: 16px;        --inset-loose: 24px;
```

### 8.1 Section padding is a function of rank, not a single token

| Rank | xs | sm | md | lg | xl |
|---|---|---|---|---|---|
| **A** (full-bleed, ground change) | 64 | 80 | 96 | 128 | 160 |
| **B** (major section) | 40 | 48 | 64 | 80 | 96 |
| **C** (minor section) | 24 | 32 | 40 | 48 | 56 |

**The constraint that destroys the flat page mechanically:** *two adjacent sections may never share a rank.* It is a template-level assertion, testable, and it alone converts today's `B-B-B-B-B-B` home page — six bands with byte-identical 72px/72px padding at 1440 and 80px/80px at 1920 — into a scroll with long and short breaths.

### 8.2 Inside a section

```
opening → content        32
title → lead             12
lead → content           32
row → row                 0  (1px --rule-hair, 16px inset each side)
content → closure        24
marginalia first baseline aligns to the first baseline of the block it annotates
```

Vertical space between sections is always greater than vertical space inside them. Never stack two spacing tokens to reach a value; add the value to the scale or use the next one.

---

## 9. Surfaces, borders, elevation

**Radius: 0.** Every rectangular surface — buttons, inputs, notices, tables, photographs, panels, the sheet, dialogs, chips. One exception in the entire system: the account avatar at `50%`. `--radius-sm`, `--radius-md`, `--radius-pill` are deleted from the tokens. This follows .italia verbatim — *"gli angoli squadrati si addicono maggiormente a elementi che richiedono una presentazione più formale e strutturata"* — and it removes at a stroke the five 999px pills that currently carry the site's most important taxonomy (the five regular pathway families) and the six rounded pills that are the portal's phone navigation.

**Elevation: none.** There are exactly **two** shadowed objects in the system, both of them things that genuinely float above the page: the mobile sheet and the modal dialog. Both use the same scrim — `0 0 0 100vmax rgb(13 20 24 / 0.55)` — plus a single 1px `--rule-ink` edge. **Nothing else in the product has a shadow.** Depth is carried by ground changes and rules. This is the cheapest and most decisive anti-SaaS move available, and it is unforgiving: without shadows, every misalignment is visible, which is the point.

**Borders — four uses, no fifth:**

| Token | Weight | Job |
|---|---|---|
| `--rule-hair` | 1px | Separation between rows, between list items. Never the sole boundary of a control (1.45:1). |
| `--rule-strong` | 1px | Input borders, table cell structure, panel edges (3.42:1, satisfies WCAG 1.4.11). |
| `--rule-ink` | 2px | Opens a band or a table. **Once per band.** |
| `--rule-sea` | 2px | Current position only — `aria-current`, the route's drawn segment, the open accordion. |
| *(notice)* | 4px inline-start | The notice component's family rule. |

**Focus — one inseparable pair, inherited by everything, neutralised by nothing:**

```css
:where(a, button, input, select, textarea, summary, [tabindex]):focus-visible {
  outline: 3px solid var(--focus-ring);
  outline-offset: 2px;
  box-shadow: 0 0 0 5px var(--focus-halo);
}
```

A component may change `--focus-halo` to match the ground it sits on. **No component may set `box-shadow: none` on focus.** Today `.skip-link:focus` does exactly that, and because its ring is `--color-accent-200 #e3d6b4` drawn on `#fbfaf7` with a 2px offset, the first tab stop of every page in every language has a **1.38:1** focus indicator. The test that catches this measures ring-versus-the-surface-it-is-drawn-on, not ring-versus-element, across the first 20 tab stops of each archetype.

**Forced colours:** a `@media (forced-colors: active)` layer restores every rule, marker and state with `CanvasText` / `LinkText` / `Highlight`. **Structure is drawn with `border`, `outline` or text — never with `background` on a pseudo-element**, because those repaint to Canvas and vanish. One forced-colours capture joins the standard screenshot matrix. Today `grep -n "forced-colors" static/css/*.css` returns nothing, and the `aria-current` bar, the form-error dot and every accent hairline disappear.

---

## 10. Information hierarchy

### 10.1 The page's rank contract

- **Exactly one Rank A per page.** Never zero, never two.
- **Two or three Rank B.**
- Everything else is Rank C.
- **No two adjacent sections may share a rank, a ground, an opening register, or a container width.**

Home reads `A · C · B · C · B · C · A?` — no: one A. Home reads **`A · B · C · B · C · C`**. An interior page reads `header · C · B · C · A · C`, with its single A placed where the page's argument peaks — usually "who is responsible" or "what we do not do", not at the top.

### 10.2 The four section-opening registers

**The eyebrow — a 12px tracked-caps line above a heading — is deleted from the system.** Today it appears seven times on one page at exactly 12px / weight 600 / 1.44px tracking / `rgb(122,97,36)` / x=152 / width=576, followed each time by a 33.76px H2 at x=152 and a 21px lead at width 576. Not similar — identical, to two decimal places, five times.

Its replacement is four registers. **A page may use each at most twice.**

**R1 — Numbered opening.** `t-ref` ordinal (`02`) in the margin or inline-start, a 1px hairline running from it to the container edge, the title hanging on the rule. Carries the route ordinal where the section is a step.

**R2 — Rule opening.** A 2px `--rule-ink` across the full container, the title hanging beneath its inline-start end, no label, no lead. The loudest opening after Rank A.

**R3 — Bare statement.** The title alone. Nothing above it, nothing below it but the content. Used once per page for the thing that matters.

**R4 — Panelled opening.** Title and lead in cols 1–4; the first content row begins at col 5 and runs to 12. The asymmetry is the opening.

### 10.3 The anatomy of a section

Five slots. Slots 2 and 4 are optional; a section that fills all five is rare and is probably Rank A.

```
1  RANK MARK      the ordinal, or the rule, or nothing        (register R1–R4)
2  OPENING        title (t-section) + optional lead (t-lead, --w-lead)
3  CONTENT        one of: indexed list · table · route rule · prose (--w-read)
                  · notice · timeline · service rows · photograph
4  MARGINALIA     cols 10–12: source, date, responsible actor, caveat, related
5  CLOSURE        a single 1px hairline, or a single onward link. Never both.
```

**Content type is the variable that must change**, not the decoration. Six consecutive sections of indexed lists would be as flat as six eyebrows. The rotation on the home page is: service rows (A) → route rule L (B) → indexed list (C) → two-column opposition (B) → table (C) → facts (C).

### 10.4 How a page announces its importance

By **ground**, by **container**, by **rank padding**, by **one Statement**. Not by heading size alone, and never by more chrome. The Statement is the single element on the page set at `t-statement`; if a page has no Statement it has no Rank A band and is, by design, a document.

---

## 11. Motion

Four tiers. Everything outside them is deleted.

**What never moves:** page content on scroll (the entire `.reveal` apparatus is deleted — it serves three of 169 templates and hides content behind `opacity: 0` awaiting an unguarded ten-call JavaScript chain, so one throw in `initNavigation` leaves the four entrances, the eight pathways and the timeline permanently invisible); photographs; headings; the wordmark; numbers (`initCounters()` and `.counter` are deleted — zero usages, and "startup counters" is on the banned list); section bands; table and list rows; the masthead (no shrink, no hide-on-scroll).

| Tier | Duration | Easing | Travel | What |
|---|---|---|---|---|
| **1 — STATE** | 120ms | `cubic-bezier(.2,0,0,1)` | ≤4px | Disclosure chevron, `aria-current` rule, checkbox/radio, `:active` press, masthead rule on scroll |
| **2 — SURFACE** | in 200 / out 140 | in `cubic-bezier(.16,1,.3,1)` / out `cubic-bezier(.7,0,.84,0)` | its own dimension | Sheet (`translateY(-100%)→0`), services panel, dialog, dropdown |
| **3 — ORIENTATION** | 240ms, one shot | `cubic-bezier(.2,0,0,1)` | — | **The route rule draws to the current station**, once, and only when the position changed since the last render (server-set `data-route-advanced`). Also: the 2px rule under a form-error summary on focus, and under a newly arrived message. Draws, stops, never loops, never repeats on re-render. |
| **4 — PROGRESS** | real elapsed work | linear | — | Upload progress, wizard step position. Never a fabricated duration. |

**Ceilings:** nothing exceeds 240ms except Tier 4; nothing travels more than 12px except a Tier 2 surface.

**Banned:** parallax, scroll-linked animation, decorative loops, moving gradients, autoplay carousels, and hover as the sole feedback for anything — every hover affordance carries `:active` and `:focus-visible` equivalents, because today four of the site's motion behaviours are hover-only and a phone gets nothing.

**Reduced motion:** the existing `prefers-reduced-motion` block is kept exactly as it is — it is the best-implemented part of the current build (tokens zeroed, keyframes cancelled, a global `transition-duration: 0.01ms !important` guard, and a runtime re-check). Tier 3's draw becomes an instant end state. All *new* motion is wrapped in `@media (prefers-reduced-motion: no-preference)` so stillness is the default rather than the exception.

---

## 12. Hero approach

### 12.1 Home — the Service Band (Rank A)

**Full-bleed. `--ground-institution`. No photograph. `min-block-size: 420px`, `max-block-size: 62vh` at `md` and above.**

Content, in `--w-page`:

- **Cols 1–8:** `t-statement` (88px at 1600, 76 at 1200, 40 at 390), **three lines maximum**. If the copy needs four, the copy is wrong. Below it one `t-lead` line in `--ink-on-dark-2`, capped at `--w-lead`. Below that, a 2px `--rule-inverse`, then **four task rows**:

  | | |
  |---|---|
  | `t-ref` `01` | `t-sub` **Je veux travailler ou me former en Italie** · `t-micro` gloss · `→` |
  | `t-ref` `02` | `t-sub` **Mon entreprise cherche des profils** |
  | `t-ref` `03` | `t-sub` **Nous sommes une institution** |
  | `t-ref` `04` | `t-sub` **Nous sommes une université ou un organisme de formation** |

  Each row 72px at `lg`, the whole row a target, 1px `--rule-inverse` between, no box, no illustration, no icon. **This is the information architecture, so it is presented as navigation, not as content** — which is exactly ECL's condition for using a navigation list rather than cards when the set is homogeneous.

- **Cols 10–12:** the **authority statement**, in `t-body` serif on a 4px `--clay-rule` inline-start:

  > **Personne ne peut vous vendre un visa.**
  > **Nous ne demandons jamais d'argent.**
  > **Aucune « voie rapide » n'existe.**
  >
  > Italy Legal Entry ne délivre ni visa, ni permis, ni autorisation. → *Attention aux fraudes*

This puts the four audiences, the primary tasks, the fraud warning and the non-authority statement **all in the first screen**. Today the "Quatre accès" heading is 68px below the fold at 1440, the entrance titles 492px below it, the fraud warning is 8.7 phone-screens down in Phase 3 and **entirely absent** from the public site today (`grep -ic "fraude"` on the live home returns 0; `/fr/attention-aux-fraudes/` returns 404, gated behind Phase 3 for no reason).

Directly beneath the band: the **route rule at scale L** on `--ground-process` — the model, `besoin → compétences → formation → parcours légal → entrée → inclusion`, with the responsible actor under each station and the shore change drawn between `formation` and `parcours légal`. This sequence currently exists once, as a diagram in section 6 of 11 of the Phase-3 home, owned by the pilot project, with no URL.

### 12.2 Interior page

**No band. No hero. No photograph.**

```
breadcrumb (t-micro)
t-title, cols 1–8                       ← the page title is the user's task, in sentence case
t-lead, --w-lead                        ← one lead, never two
2px --rule-ink across the full container  ← closes the header
content
```

The page's single Rank A band is placed *inside* the page, where the argument peaks. On `/fr/entreprises/` that is "Ce que nous attendons d'une entreprise et ce que nous ne ferons pas"; on a pathway sheet it is the route rule at scale L; on `/fr/agami/` it is the promoter statement.

All page titles are **sentence case, enforced in CSS and validated in the CMS**. Today 22 headings are shouted in caps typed into the translation catalogue, with computed `text-transform: none` and tracking that is −0.48px in one file and +1.632px in another for the *same words* — and `<title>` reads `ATTENTION AUX FRAUDES · Italy Legal Entry™`, so search results shout too.

---

## 13. Data and process visualisation

### 13.1 A pathway (indexed list)

```
══════════════════════════════════════════════════════════════════════  2px --rule-ink
01   Travail salarié                                    SALARIÉ    ▪▪▪▫▫▫▫    →
     Décret flux, nulla osta, visa, permis de séjour.
──────────────────────────────────────────────────────────────────────  1px --rule-hair
02   Travail hautement qualifié — Carte bleue UE      QUALIFIÉ    ▪▪▫▫▫▫     →
     …
```

Columns at `lg`: `t-ref` ordinal (col 1) · `t-sub` title + `t-body` one-line gloss (cols 2–7) · `t-label` family (col 8) · XS route rule (cols 9–10) · `→` (col 12). Row height ≥ 72px, the whole row a target. No icon, no card, no pill. Below `sm`, the row becomes ordinal + title + XS route + chevron at 72px, gloss hidden.

This is the one genuinely editorial object in the current build (the 01–08 `Les parcours réguliers` block), promoted from a section inside one page to the site's core reference pattern.

### 13.2 A timeline

Two columns, vertical route rule between them.

```
        │
2026    │▪  Phase 2 — Orientation enregistrée              ÉQUIPE AGAMI
09.20   │   Votre pré-évaluation a été enregistrée…
        │   → 2 éléments vous sont demandés
        │
        ┆   ── MAROC ▸ ITALIE ──                            (shore change: 6px gap)
        │
2026    │○  Phase 3 — Dossier transmis                     AUTORITÉ COMPÉTENTE
——      │   Aucune date communiquée.
```

Date gutter cols 1–2 in `t-ref`. Rule in col 3. Content cols 4–9. **Responsible actor cols 10–12 in `t-label`** — the client's acceptance question "qui è responsabile" answered on every row. Completed phases collapse to a single 44px line; the current phase is open and contains its checklist rows, documents and sources.

### 13.3 A checklist

A real `<table>`, never boxes:

| Élément | État | Responsable | Échéance | Action |
|---|---|---|---|---|
| Pièce d'identité en cours de validité | **TRANSMIS** | Vous | — | Remplacer |
| Attestation de formation linguistique | **À FAIRE** | Vous | 14.10.2026 | Téléverser |
| Nulla osta | **EN EXAMEN** | Autorité compétente | — | — |

Four states, `t-label` chips: **À FAIRE · TRANSMIS · EN EXAMEN · CLOS.** Each is a 2px inline-start rule plus a word — never colour alone, and **never a green "validated"**. Missing and expiring rows sort first. Null cells contain `—`, never empty (ECL's rule). Column heads `t-label`, `scope="col"`, a visually-hidden `<caption>`, tabular figures, `.scroll-x` where needed. Below `sm`, rows pop in: label above value, 1px rule, 12px inset, 48px minimum.

### 13.4 A rule outcome

```
═════════════════════════════════════════════════  2px --rule-ink
  ⚑  ÉLÉMENT MANQUANT                              t-label, --clay
  Votre situation correspond à un parcours régulier,
  mais deux éléments manquent avant toute démarche.  t-title
─────────────────────────────────────────────────
  POURQUOI                    ← per applied rule, one line each, with its rule id
  CE QUI MANQUE               ← checklist rows (13.3), with responsible actor
  SOURCES                     ← numbered <ol>: title · reference · date · link
  Jeu de règles RS-2026.3 · évalué le 20.09.2026     t-ref
  [ Demander une revue professionnelle ]             one primary action
```

On `--ground-process`. **Five kinds — POSSIBLE · ÉLÉMENT MANQUANT · AVERTISSEMENT · ARRÊT · REVUE REQUISE** — each with a distinct 24px mark and a distinct rule weight; **colour is the third signal, never the first**. Today the engine hardcodes one kind (`KIND = "INFORMATIVE_PREASSESSMENT"`), the template hardcodes `data-result-kind="informational"`, the result page renders `<ul><li>{{ item.text }}</li></ul>`, shows no sources at all, and lives outside the platform because `templates/orientation/result.html:1` extends `base.html`.

---

## 14. Platform interpretation

### 14.1 App shell

```
┌────────────────────────────────────────────────────────────────────────┐
│ ◧ Italy Legal Entry  Espace de travail        FR ▾   Aide   Amina B. ▾ │  48px, --ground-institution
├──────────────┬─────────────────────────────────────────┬───────────────┤
│ MON DOSSIER  │  case header  (88px, sticky)            │  CASE PANEL   │
│  Vue         │  next action band                       │   320px       │
│  Parcours    │  work column                            │               │
│  Pièces   2  │                                         │               │
│  Échéances 1 │                                         │               │
│  Échanges  3 │                                         │               │
│              │                                         │               │
│ MON COMPTE   │                                         │               │
│  Profil      │                                         │               │
│  Sécurité    │                                         │               │
│  Consents    │                                         │               │
│  ─────────── │                                         │               │
│  ← Site      │                                         │               │
└──────────────┴─────────────────────────────────────────┴───────────────┘
│ Mentions · Confidentialité · Support · RS-2026.3                        │  48px legal strip
```

Left rail 248px, sticky, full height, grouped with `t-label` titles, each row carrying a count or a state chip. **Rows the role cannot use are absent, not greyed.** At `md` (900–1199) the rail becomes a 64px icon rail with labels in tooltips *and* in the accessible name. Below `md`, a bottom bar of four (Dossier · Checklist · Pièces · Échanges) plus a sheet for the rest.

Exactly one labelled `← Site public` link, at the foot of the rail, in `--ink-on-dark-2`.

### 14.2 Case header (88px, sticky under the top bar)

```
DOSSIER ILE-2026-0043 · Amina B. · Travail salarié — famille de parcours     t-ref + t-ui
─────────────────────────────────────────────────────────────────────────
ÉTAT COMPTE CRÉÉ — ORIENTATION NON FAITE · RESPONSABLE Équipe AGAMI      ▪▪▫▫▫▫▫  2/7
```

`t-label` for the field names, `t-ui` for values, the **M-scale route rule** at the inline-end showing phase n/7. The reference stays LTR-isolated in Arabic. 2px `--rule-ink` closes the header.

This replaces the current dashboard headline, which is the *public home page's marketing teaser* re-served to people who already logged in: `p3.reserved.title` / `p3.reserved.body` drive both surfaces, so the string "ESPACE RÉSERVÉ" appears twice within 190px, at 48px and again as the rail title, and on `/ar/` both are in French.

**Where no `CaseFile` exists yet, the state is derived from what the database already knows** — consents given, orientation sessions, submitted requests, organisation memberships — and labelled honestly (`ÉTAT: COMPTE CRÉÉ — ORIENTATION NON FAITE`). Four known facts about the QA person account today produce four inferable next actions and the interface surfaces none of them.

### 14.3 Next-action band

Directly beneath the case header, `--ground-process`, 140px:

> **Prochaine action** `t-label`
> **Commencez l'orientation pour obtenir votre famille de parcours.** `t-title`
> Responsable : **vous** · Aucune échéance communiquée `t-ui`
> `[ Commencer l'orientation ]`   `pourquoi ? ▸`

**One sentence, one responsible party, one date when known, one primary button, one "pourquoi" disclosure linking the rule and its source. Never two.**

### 14.4 Dashboard

No tiles. One prioritised column:

1. Case header
2. Next action band
3. Horizontal route rule — the seven phases, current marked
4. **The checklist table** (§13.3)
5. Échéances — a dated list
6. Échanges — a dated list with unread marked by weight + rule, not colour
7. Historique — an append-only activity log, `t-micro`, date gutter

**Empty regions are one left-aligned serif sentence under a hairline, naming who fills the region and when, with the resolving action inline.** Never a dashed box, never a centred icon, never a standalone numeral at 34px above the word "demandes transmises". Today the dashboard is a 2×3 grid of 400px tiles, four of them exactly 276px tall, each carrying an icon in its header and repeating the same icon a second time inside a centred dashed box — six of the client's banned patterns in one screen, five of them saying nothing is there.

### 14.5 Role branching

`navigation()` and the dashboard regions **take the account's role, deny by default, and return different structures** — not a filtered list. Today `services.py:627–640` returns a hardcoded six-entry list for every account, so `qa-company@example.test` is served the Person dashboard, labelled « Personne », and offered the individual mobility questionnaire.

Company rail: `TABLEAU DE L'ENTREPRISE` (Vue · **Besoins (3)** · Projets · Échanges) then `ORGANISATION` (Identité et vérification · Membres · Pièces · Consentements). Company case header: `ENTREPRISE — Raison sociale · P.IVA · VÉRIFICATION EN COURS · TERRITOIRE Veneto — Treviso · RESPONSABLE DU COMPTE`. `Mon parcours` and `Mon orientation` are **absent**, not empty.

A *besoin* becomes a first-class object with its own register — `Réf | Profil | Postes | Territoire | Calendrier | État | Responsable | MAJ` — and a five-station route rule (Exprimé → Qualifié → Acteur autorisé assigné → Sélection en cours → Clôturé) that names the authorised actor and shows **counts only, never a person list**.

### 14.6 List, detail, wizard

**List:** table, `t-label` heads, zebra only above 20 rows, sticky header, `—` for null, `.scroll-x` as a component that refuses to render without a label.

**Detail:** object header → *Où en est votre demande* (ordered step list with state, responsible actor and date per step, append-only) → *Ce qui vous est demandé* (checklist rows with inline actions) → *Ce que vous avez transmis* (the current definition list, demoted to the bottom, collapsed by default). The reference is a human case number, not `{{ item.kind }}-{{ item.pk }}`.

**Wizard:** one question per screen on `--ground-process`; the route rule at scale M as the progress indicator (Tier 4); **answers re-checked from the session** (`{% if c.key in answers %} checked{% endif %}` — today "Précédent" returns to a question with every radio unchecked, because the template never emits `checked`); after every swap, focus moves to the `<legend>` (`tabindex="-1"`) and a persistent polite live region **outside the swapped node** announces "Question n sur m"; controls come from the shared `form_field.html` primitive (≥24px radios, `aria-invalid` on the widget not the fieldset, `novalidate`, summary + inline errors per .italia's error contract).

---

## 15. Mobile

Not a reflow. An authored composition at `xs`.

**Budget, enforced in CI:** the home page is **≤ 4.5 viewport heights at 390** (today 8.65; 9.90 at 320). The Phase-3 home is ≤ 6 (today 13.2). Every portal page ≤ 3 (today 4.52).

**Chrome:** 56px, one bar. No utility bar. `--chrome-h: 56px`.

**Home at 390, section by section:**

| Section | Height | How |
|---|---|---|
| Service band | 640 | Statement 40/44 (3 lines) · lead 2 lines · four task rows at 88px |
| Authority statement | 220 | Moves below the task rows, 4px clay rule, serif |
| Route rule (model) | 280 | **Vertical** variant — the horizontal 4+4 circle grid has no meaning at 390 |
| Pathway index | 620 | 8 rows × 72px + opening |
| What we do / do not do | 380 | Two stacked groups, each with its own ground: `--ground-page` and `--ground-inset` |
| Ecosystem facts | 200 | Definition rows |
| Footer | 300 | Three `<details>`, closed |

≈ 2,640px ≈ **3.1 viewport heights.**

**Specific phone decisions:**
- The four entrances become **four rows of 88px**, not four 397–423px illustrated blocks. That section falls from 1,907px to 352px.
- **No photograph unless full-bleed** at 100vw × 3:2.
- `--section-gap` by rank on phone: A 64 · B 40 · C 24 (the current `clamp(4rem, 6vw, 6rem)` gives a phone 64px between every pair of sections).
- **Every interactive element ≥ 44px block-size**, achieved with padding so visual weight is unchanged. Today the home at 390 has 25 sub-44px targets — `.entrance__cta` is 22px, `.link-arrow` 26px, eighteen footer links 19px each in an adjacent stack — and every portal page has 31–40.
- The footer becomes three `<details>` groups, closed (today 967px of stacked links, 1.15 screens).
- Tables pop in below `sm`.
- The hero H1 floor is 40px against a 19px lead — ratio 2.1, matching desktop, instead of the current 1.78 falling to 1.32 for H2.
- `--margin: 16px` at 320–359 with the Statement floor at 36px so the headline holds three lines, not four.

---

## 16. RTL and Arabic

### 16.1 Mechanics (keep — this is already the best-engineered part of the build)

Logical properties throughout, enforced by `tests/i18n/test_rtl_static.py`. Zero horizontal overflow at 320–1920 on every Arabic route. Mirrored rails, mirrored arrows, mirrored progress, mirrored tables. The route rule's origin is `inline-start`, so in Arabic it draws **right to left** — which is the correct semantics for progress and requires no special case.

### 16.2 Type

Per §3.5: Readex Pro for interface and display, Noto Naskh Arabic for reading, `--scale-text: 1.08`, Arabic-specific leading tokens, all tracking zeroed at token level, a 15px floor, weights capped at 700 with synthetic bold banned. The Arabic brand carries its own descriptor in the lockup at every breakpoint.

### 16.3 Prescribed French — a designed object, not a leak

There are 100 prescribed texts and all 100 exist only in French (`apps/cms/locked_content.py:861` — `LOCKED_TEXTS = {"fr": {…}}` with `# "ar": {…}` still a comment). They are the H1s, the leads, the pathway definitions, the timeline steps, the fraud warning and the trust statements. A typical Arabic page is **44% Arabic**; `/ar/forum/` is **1.1%** — 36 Arabic characters against 3,182 Latin. Opening Phase 3 drops the Arabic home from 73.5% to 17.9%.

**The `.prescribed` component** is the only way locked French is ever rendered on an Arabic page:

- Its **own full-width band** on `--ground-process`. It never shares a row, a grid cell or a two-column comparison with Arabic text.
- A 4px `--clay-rule` on the inline-start edge.
- An Arabic caption above it in `t-label`: **«نص رسمي بالفرنسية — الترجمة العربية قيد الإعداد»**.
- A mandatory Arabic **`خلاصة`** slot: 2–3 lines written by AGAMI's editors that are explicitly *not* a translation of the locked text (so `test_no_catalogue_translates_a_locked_text` still passes) and that carry the block's meaning.
- Latin faces restored **inside** it: `--font-ui: Archivo; --font-read: "Source Serif 4"`. Today, because `:lang(ar)` sets the families on the root, every French fallback block renders in the Arabic sans — "DE QUELS PROFILS PROFESSIONNELS…" is 12.3% wider in that face than in the serif it wears on the French page, which is why that H1 wraps to 221px.
- Its own LTR island: the Latin run is wrapped in `<bdi lang="fr" dir="ltr">` **inline**, while the block keeps `direction: rtl; text-align: start`. This replaces the current `[dir=rtl] :is(p,h1…)[lang]` block-level rule, under which every fallback flips to the opposite margin — on `/ar/parcours/` a row's number sits at x=1288 and its title at x=492, roughly **760px of void between them**, eight times.
- Emitted by a **single template tag** that always produces `<bdi lang dir>` or nothing. The element allow-list in CSS is deleted; the test walks **text nodes**, not elements, which is why the nav string, the wizard legend, the Forum banner children and the utility bar currently slip through a test that reports "corretto".

### 16.4 Arabic-share budget, enforced

Per-route minimum Arabic share of visible characters in `<main>`, failing CI below it:

| Route class | Floor |
|---|---|
| Service pages (home, audiences, orientation, fraud, FAQ) | **90%** |
| Reference (pathways, glossary, Vivre en Italie) | 80% |
| Institutional (project, AGAMI, Forum, legal) | 60% |

Below the floor, the page is **not served at `/ar/` as if it were translated**: it serves an Arabic notice plus the `خلاصة` and the contact address. Work order by risk, not by sitemap: anti-fraud → FAQ → orientation → parcours → forum.

### 16.5 Details

- `™`, `©`, `AGAMI`, dates and references always `<bdi>`. The footer currently renders "AGAMI — Dialogo Giuridico Interculturale APS 2026 ©" with the Latin sentence's full stop stranded at the left edge.
- **Identity is never truncated.** `text-overflow: ellipsis` is permitted only on user-generated strings that have a full copy elsewhere on the page.
- Arrows inside isolated Latin runs are replaced in the source strings with `·`; direction is never left loose in two senses on one page.
- The glossary gets an **Arabic-native index** (by theme: الإقامة / العمل / الدراسة / الوثائق) with the Latin A–Z demoted to a secondary filter, and each term becomes a bilingual object: Italian headword (the term the user will meet on a form), Arabic gloss, then the French definition inside `.prescribed` until the Arabic exists.
- Western digits throughout (correct for Morocco). Arabic comma `،` and question mark `؟`; no Latin `?` inside Arabic strings; no space before a colon (`{% translate "Référence de la session :" %}`, with the colon inside the string).
- URL segments localised with `gettext_lazy` inside `path()`, with 301s. Today one Arabic URL bar carries French, Italian and English segments and not one Arabic one, and pathway slugs are raw English database keys.

---

## 17. Wireframes

### 17.1 Home above the fold — 1440 × 900

```
┌──────────────────────────────────────────────────────────────────────────────────────┐
│ AGAMI — Dialogo Giuridico Interculturale APS · promoteur   العربية Français Italiano │ 36  --ground-institution
│                                                            English   Aide  Mon espace│
├──────────────────────────────────────────────────────────────────────────────────────┤
│ ▬▪▬  Italy Legal Entry™          ┌────────────────────┐   Personnes  Entreprises     │ 68  --ground-page
│      Mobilité régulière          │ 🔍 Rechercher une  │   Institutions  Universités  │     1px --rule-strong below
│      Vénétie–Maroc               │    démarche…       │   Démarches ▾   Forum  Projet│
├══════════════════════════════════════════════════════════════════════════════════════┤
│                                                                                      │
│  ╔═ cols 1–8 ═══════════════════════════════════╗   ╔═ cols 10–12 ═══════════════╗   │
│  ║                                               ║   ║                            ║   │
│  ║  Une voie régulière                           ║   ║ ┃ Personne ne peut vous    ║   │  --ground-institution
│  ║  vers l'Italie,                               ║   ║ ┃ vendre un visa.          ║   │  Rank A, full bleed
│  ║  construite avec                              ║   ║ ┃                          ║   │  t-statement 76/80
│  ║  les acteurs compétents.                      ║   ║ ┃ Nous ne demandons        ║   │  3 lines max
│  ║                                               ║   ║ ┃ jamais d'argent.         ║   │
│  ║  Orientation, formation avant le départ       ║   ║ ┃                          ║   │  4px --clay-rule
│  ║  et accompagnement.                           ║   ║ ┃ Aucune « voie rapide »   ║   │  t-body serif
│  ║  ═════════════════════════════════════════    ║   ║ ┃ n'existe.                ║   │
│  ║  01  Je veux travailler ou me former       →  ║   ║ ┃                          ║   │  72px rows
│  ║      en Italie                                ║   ║ ┃ Italy Legal Entry ne     ║   │  no box, no icon
│  ║  ─────────────────────────────────────────    ║   ║ ┃ délivre ni visa, ni      ║   │
│  ║  02  Mon entreprise cherche des profils    →  ║   ║ ┃ permis, ni autorisation. ║   │
│  ║  ─────────────────────────────────────────    ║   ║ ┃                          ║   │
│  ║  03  Nous sommes une institution           →  ║   ║ ┃ Attention aux fraudes →  ║   │
│  ║  ─────────────────────────────────────────    ║   ║ ┗                          ║   │
│  ║  04  Nous sommes une université ou un      →  ║   ╚════════════════════════════╝   │
│  ║      organisme de formation                   ║                                    │
│  ╚═══════════════════════════════════════════════╝                                    │
│                                                                                      │
├──────────────────────────────────────────────────────────────────────────────────────┤ ← fold ≈ 900
│  LE MODÈLE                                                                           │  --ground-process
│  ▬▬▬▬▬▪▬▬▬▬▬▬▬▬▬▬▬┆  ┆▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬            │  route rule, scale L
│  │      │      │      │       │        │          │                                  │
│  Besoin Compé- Forma- ┆MAROC▸ Parcours Entrée en  Inclusion                           │
│         tences tion   ┆ITALIE légal    Italie                                        │
└──────────────────────────────────────────────────────────────────────────────────────┘
```

Note what is absent: no photograph, no eyebrow, no card, no illustration, no gold, no rounded corner, no shadow.

### 17.2 Home above the fold — 390 × 844

```
┌────────────────────────────────────┐
│ ☰   ▬▪▬ Italy Legal Entry™     🔍  │  56  --ground-page
├════════════════════════════════════┤
│                                    │
│  Une voie régulière                │  --ground-institution
│  vers l'Italie,                    │  t-statement 40/44
│  avec les acteurs                  │  3 lines
│  compétents.                       │
│                                    │
│  Orientation, formation avant       │  t-lead 19/28
│  le départ, accompagnement.        │
│  ════════════════════════════      │  2px --rule-inverse
│  01  Je veux travailler ou      →  │  88px
│      me former en Italie           │
│  ────────────────────────────      │
│  02  Mon entreprise cherche     →  │  88px
│      des profils                   │
│  ────────────────────────────      │
│  03  Nous sommes une            →  │  88px
│      institution                   │
│  ────────────────────────────      │
│  04  Nous sommes une            →  │  88px
│      université ou un              │
│      organisme de formation        │
│                                    │
├────────────────────────────────────┤  ← fold ≈ 844
│ ┃ Personne ne peut vous vendre     │  4px --clay-rule
│ ┃ un visa.                         │  t-body serif
│ ┃ Nous ne demandons jamais         │
│ ┃ d'argent.                        │
│ ┃ Aucune « voie rapide » n'existe. │
│ ┃ Attention aux fraudes →          │
└────────────────────────────────────┘
```

All four audiences are on screen one. Today the fourth is at y=2724 — 3.2 screens down — and two of them are not in the navigation at all.

### 17.3 Person dashboard — 1440 × 900

```
┌──────────────────────────────────────────────────────────────────────────────────────┐
│ ▬▪▬ Italy Legal Entry  Espace de travail          FR ▾    Aide    Amina B. ▾         │ 48 --ground-institution
├───────────────┬──────────────────────────────────────────────────┬───────────────────┤
│ MON DOSSIER   │ DOSSIER ILE-2026-0043 · Amina B.                 │ QUI FAIT QUOI     │
│ ▌Vue          │ Travail salarié — famille de parcours            │ ───────────────── │ 88 sticky
│  Parcours     │ ──────────────────────────────────────────────── │ Orientation       │ 2px --rule-ink
│  Pièces    2  │ ÉTAT ORIENTATION NON FAITE                       │ Équipe AGAMI      │
│  Échéances 1  │ RESPONSABLE Vous      ▬▪▬▬▬▬▬▬▬▬▬▬▬  PHASE 1/7   │                   │
│  Échanges  3  ├──────────────────────────────────────────────────┤ Décision finale   │
│  Historique   │ PROCHAINE ACTION                                 │ Autorité          │
│               │ Commencez l'orientation pour obtenir             │ compétente        │
│ MON COMPTE    │ votre famille de parcours.                       │ italienne         │
│  Profil       │ Responsable : vous · aucune échéance             │                   │
│  Sécurité     │ [ Commencer l'orientation ]      pourquoi ? ▸    │ ───────────────── │
│  Consentements├──────────────────────────────────────────────────┤ CE QUE LA         │
│  ───────────  │ VOTRE PARCOURS                                   │ PLATEFORME NE     │
│  ← Site public│ ▬▪┆▬▬┆▬▬┆▬▬┆▬▬┆▬▬┆▬▬                             │ FAIT PAS          │
│               │  1  2  3  4  5  6  7                             │ Elle ne délivre   │
│               │  Compte créé · Orientation · Dossier · …         │ ni visa, ni       │
│               ├──────────────────────────────────────────────────┤ permis, ni        │
│               │ CE QUI VOUS EST DEMANDÉ                          │ autorisation.     │
│               │ ════════════════════════════════════════════     │                   │
│               │ ÉLÉMENT          ÉTAT      RESPONSABLE  ÉCHÉANCE │ ───────────────── │
│               │ ────────────────────────────────────────────     │ BESOIN D'AIDE     │
│               │ Orientation      À FAIRE   Vous         —        │ Guichet numérique │
│               │ Pièce d'identité À FAIRE   Vous         —        │ Ouvrir une        │
│               │ Consentements    TRANSMIS  Vous         —        │ demande →         │
│               ├──────────────────────────────────────────────────┤                   │
│               │ ÉCHÉANCES                                        │                   │
│               │ ───────────────────────────────────────────────  │                   │
│               │ Aucune date ne vous a encore été communiquée.    │                   │
│               │ L'équipe AGAMI les inscrira ici. Voir le guichet →│                   │
│               ├──────────────────────────────────────────────────┤                   │
│               │ ÉCHANGES  3 non lus                              │                   │
│               │ 20.09.2026  Accusé de réception — demande 0043   │                   │
│               │ ...                                              │                   │
├───────────────┴──────────────────────────────────────────────────┴───────────────────┤
│ Mentions légales · Confidentialité · Support · Jeu de règles RS-2026.3               │ 48
└──────────────────────────────────────────────────────────────────────────────────────┘
```

Fold budget at 1440×900: 48 top bar + 88 case header + 140 next action + 120 route + 360 checklist = **756px**, leaving 144px of air — against today's 421px consumed before any information appears (47% of the fold), 637px on a phone (75%).

---

## 18. Risk and cost

### 18.1 What could go wrong

**1. This is a content project wearing a design brief.** The service band needs four task sentences in four languages, the checklist needs a responsible actor per element, the route needs a real model with real actors, and every photograph needs a place, a date and a credit. If that content does not arrive, the direction degrades into empty structure — which is worse than the current build, because empty structure is conspicuous where empty cards are merely dull. **Mitigation:** a content contract signed before the first template is written, and a `pending` state for every slot that renders an honest institutional line rather than a placeholder.

**2. It could read as .gov.** A limestone-and-ink public-service look sits close to an administration's. **Mitigations, all already in this document:** no emblem, no coat of arms, no "sito ufficiale" convention, no three-band PA header lockup, no Blu Italia, no Titillium, no SPID/CIE/pagoPA affordances, no "Amministrazione trasparente" furniture; the promoter line is always *promoteur*, never *ente di appartenenza*; the serif reading voice and the olive cooperation axis are not administrative devices; and the "no colour means approved" rule makes the interface structurally incapable of implying authority. **Review gate:** before launch, show three screens to a lawyer with the single question *"could a reasonable reader think this is a public body?"*

**3. The route rule could become wallpaper.** The moment it is drawn where there is no real sequence it stops being a signature and becomes a squiggle. **Mitigation:** the template-level lint (≥3 real steps, each with a label and an actor) and a hard budget of one L-scale route per page.

**4. Zero radius and zero shadow are unforgiving.** Every 1px misalignment, every ragged column bottom, every inconsistent inset becomes visible. This is a feature and a cost: it buys craft and it demands craft.

**5. Archivo's width axis invites misuse.** Four named instances only (`wdth 100` display/UI, `92` wordmark, `88` label, `87` reference), locked as CSS custom properties; any other value fails review.

**6. The right-hand marginalia column can be empty.** L3 requires real marginalia. **Mitigation:** the layout rule in §2.4 — no marginalia, no L3.

**7. Dark mode doubles the visual QA matrix.** 273 captures become 546. **Mitigation:** capture dark only at 390 and 1440, in fr and ar, on the 12 archetype representatives — 48 additional shots, not 273.

**8. Two new Latin families and two new Arabic families mean the entire type QA is re-run.** Ink parity, Arabic line-box overflow, diacritic clipping, `latin-ext` coverage for Italian and French, subsetting, and the 100px measurements all have to be redone from zero.

**9. Search needs an index.** Promising search in the masthead and not shipping it is worse than not promising it.

### 18.2 What it costs

Engineering, assuming one competent Django/CSS engineer and one designer, and assuming the archetype layer (REQ-DES-04, still TODO) is written first:

| Work | Estimate |
|---|---|
| `tokens.css` rewritten as roles; `base.css`, `layout.css`, grid, focus, forced-colours layer | **3 days** |
| Fonts: acquire, subset, `@font-face`, ink-parity and line-box tests, licence file | **2 days** |
| Component catalogue rebuilt (notice, route rule ×3 scales, indexed list, table, timeline, checklist, verdict band, service rows, form primitives, sheet, services panel) | **8 days** |
| The 12–14 archetype templates + assigning all 169 existing templates to one, with the test that fails on an undeclared archetype | **10 days** |
| Platform shell, case header, next-action band, dashboard, list/detail/wizard, role branching | **12 days** |
| RTL: Arabic type system, `.prescribed` component, bidi tag, share-budget CI gate | **5 days** |
| Accessibility: focus-pair audit, forced colours, no-JS header, wizard state restoration, target-size sweep, WCAG 2.2 / EN 301 549 v4.1.1 pass | **5 days** |
| Visual QA matrix rebuild incl. dark and forced-colours | **3 days** |
| **Engineering total** | **≈ 48 working days** |

Design: **12 days** (mark and lockup, route-rule specification at three scales, the two-shores vector, the archetype compositions, the phone compositions, the dark palette).

Content (not design, and the critical path): the four task sentences, the model's actors per station, the Arabic editorial `خلاصة` for every prescribed block, the checklist responsibilities, the Forum programme with real times, and the six photographs with captions. **20+ days, and it cannot be compressed by adding engineers.**

**What this direction does not cost:** a redesign of the accessibility engineering, the RTL mechanics, the gate machinery, the `public_routes` registry, the object-level permission model in `apps/portal/services.py`, or `docs/IMAGE_LICENSES.md`. Those are the good parts, and this direction is built on top of them rather than over them.