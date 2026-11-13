# TYPOGRAPHY — V5 type system for Italy Legal Entry™

**Role:** Typography Specialist, V5 council · **Date:** 26 September 2026 · **Repository read:** `C:/tmp/italylegalentry`, branch `main` @ `df8dc42` plus the uncommitted working tree — **nothing in the repository was modified**. Everything produced by this lane lives under `C:/tmp/ile_v5_council/` (this file, `council/typography/`, `scratch/fonts/`, `scratch/typography/`).

**Read this first.** The recommendation is a two-family Latin system with a matching Arabic pair, all SIL OFL 1.1, self-hosted, measured file by file:

| Role | Recommended (pairing A, «Fournier e la console») | Alternative (pairing B, «Newsreader evoluto») |
|---|---|---|
| Display serif (public only) | **Source Serif 4** — 400 roman at `opsz` 48 + 400 italic | **Newsreader** kept, re-set (400 at `opsz` 72, never 300) |
| Interface / body / console | **Host Grotesk** variable 400–700 + 400 italic | **Public Sans** variable 400–700 + 400 italic |
| Data references, hashes | **IBM Plex Mono** 400 (kept) | same |
| Arabic interface | **Vazirmatn** variable 400–700 (replaces IBM Plex Sans Arabic) | same |
| Arabic display | **Markazi Text** 400 (replaces Noto Naskh Arabic) | Noto Naskh Arabic 400 kept |
| Wordmark (brand asset) | **Newsreader 600, untouched** — served as a 1.7 KB glyph subset or as outlined SVG | same |
| Latin home page font payload | **73.7 KB** (today 356.1 KB) | 92.1 KB |
| Console page | **29.3 KB** (today ≈ 214 KB) | 32.9 KB |
| Arabic home page | **81.6 KB** (today ≈ 509 KB) | 110.5 KB |

The owner's font judgement is right for a precise reason: the current system pairs the most-suggested "serious tech" superfamily (IBM Plex) with a newspaper text serif set at weight 300 for a brand line in capitals, ships 272 KB of Newsreader for a 20-glyph wordmark and one italic quote, and mixes two Arabic registers. Pairing A fixes the register (institution, not newspaper; product, not IBM), the payload (−79 % on the home, −84 % on the Arabic entrance) and the loading behaviour (metric-matched fallbacks, so the swap no longer moves the page). Pairing B is the conservative route if the owner refuses a second serif next to the Newsreader lock-up.

---

## 0. Method, and what was not done

| Done | How | Evidence |
|---|---|---|
| Read the type system as shipped | `static/css/fonts.css` (26 `@font-face`), `static/fonts/` (26 woff2, 965 KB), `static/css/v4/tokens.css` §TYPE, `tokens.css` (V1), `base.css`, `v2/shell.css` (`.lock__wm`), `apps/portal/static/portal/console.css` (`.rail__wordmark`), `templates/base.html` (preloads), `scripts/fetch_fonts.py`, `docs/design-v4/DESIGN_SYSTEM_V4.md` §4, `CREATIVE_DIRECTION.md` §2, `OWNER_DIRECTIVE_2026-09-24.md` §87–88, `docs/design/ART_DIRECTION_A.md` §3.2, `DESIGN_SYSTEM_2026.md` §6, `docs/design-v4/README.md` (measured LCP and font bytes), `apps/cms/locked_content.py` (the locked hero title) | this file §1 |
| UI-UX-Pro-Max, for real | 17 queries over `--domain typography` and `--domain google-fonts`, plus the `--design-system` run for «Italy Legal Entry» (variance 6, motion 7, density 6) | §3, raw logs `scratch/typography/upm_typography.txt`, `upm_gfonts.txt` |
| Candidate acquisition for measurement only | 59 families from `@fontsource` / `@fontsource-variable` 5.3.0 via jsDelivr and 46 master files (35 families, plus Host Grotesk and Vazirmatn) with their OFL texts from `google/fonts` (`ofl/*`) → `scratch/fonts/` | `scratch/typography/tools/download.py`, `masters.py`, `pkg_availability.txt` |
| Measurement | fontTools 4.60.2 + brotli: axes, instances, OpenType features, French/Italian coverage (34 accented letters + 27 punctuation/space/symbol code points incl. U+202F narrow no-break space, U+2116, arrows, ≤ ≥ ‰ ᵉ), figure widths (tabular by default?), x-height / cap-height / average width, vertical metrics; then production-shaped builds (variable slices and static instances, one fr/it/en charset, hinting stripped, OFL name IDs kept) with real woff2 sizes | `analysis.json`, `masters.json/.txt`, `subsets.json/.txt`, `tools/subset_measure.py`, `tools/measure_v5.py`, `scratch/fonts/_subsets/*.woff2` |
| Looking, not guessing | Specimen boards rendered in headless Chrome at 1:1 and at device scale 2 with the real locked copy («ITALY LEGAL ENTRY™», the French lead, console strings), cut into per-candidate tiles | `scratch/typography/specimens/*.html`, `*.png`, `tiles/`, `zoom.png` |
| Fallback metrics | `size-adjust` / `ascent-override` / `descent-override` computed from the font files against the Windows fallbacks (Arial, Segoe UI, Georgia, Times New Roman, Tahoma) on a French/Italian sample string | §9.4, `council/typography/tokens-v5-type.css` |
| Deliverables | this report; `council/typography/tokens-v5-type.css` (proposal, not wired); `council/typography/specimen.html` + `specimen.css` + `fonts/` (the measured files, 274 KB for both pairings) | §11 |

**Not done, and why.** (1) No LCP/CLS re-measurement with the new fonts in the real pages: the repository is read-only in this phase and the fonts are not wired; the numbers in §9 are byte counts and a decomposition of the measured baseline, labelled as estimates where they are estimates. (2) Fallback metrics for Android (Roboto, Noto Serif/Noto Naskh) and Apple (Helvetica, Times, Geeza Pro) were not computed: those fonts are not on this machine; the values must be added from a Mac and an Android device before the fallback faces ship. (3) No native Arabic reader reviewed the Arabic boards; the Arabic recommendation is typographic (register, weight parity, coverage, cost) and needs one review by a Moroccan reader before the gate. (4) 21st.dev was not used: it holds React components, not type systems; no `generate`/`iterate_generation` call was made. (5) The wordmark was not redrawn or converted: the SVG option in §7 is a proposal for the owner, and the 1.7 KB subset was measured but not installed.

---

## 1. Diagnosis — what the current system actually does

| # | Finding | Evidence | Why it reads «not premium» |
|---|---|---|---|
| 1 | **The hero H1 is the brand name in capitals**, set in Newsreader **300** at 44→76 px on navy. | `apps/cms/locked_content.py:212` `p3.hero.title = "ITALY LEGAL ENTRY™"` (locked); `v4/tokens.css` `--t-display` 300; `CREATIVE_DIRECTION.md` §3.1 | Newsreader is a newspaper text face (Production Type, drawn for news reading). Its light weight in caps on a dark ground gives a thin, editorial line where the brand needs a monumental one. The display board (§4) shows it next to the alternatives at the same size. |
| 2 | **IBM Plex Sans is the interface and body face.** | `v4/tokens.css` `--f-sans`; DS V4 §4.1 | AD-A §3.2 already recorded it: Plex is «the default suggestion of almost every tool asked for an institutional open pairing», has no optical axis, no small caps, and only tabular figures. UI-UX-Pro-Max returns it as «Financial Trust» for banks (§3). The owner's phrase for the result — «portale amministrativo con font elegante» — is the signature of a default pairing. |
| 3 | **Fonts cost 356 KB on the home, ≈ 214 KB on the console, ≈ 509 KB on the Arabic entrance**, against the 200 KB per-page budget proposed in verification 9. | `docs/design-v4/README.md` (rounds 7–9: «font 356,1 KB», «i font dell'ingresso arabo ≈ 509 KB contro i 200 KB proposti») | Newsreader roman 128.9 KB is preloaded on **every** page because the lock-up uses it; the italic (143.4 KB) loads for one forum quote (`forum.css:180`) and was measured «a metà download» in the LCP decomposition. |
| 4 | **Two serif drawings for one wordmark**: the lock-up (`.lock__wm`, 20 px, 600, tracking .13em) and the console rail (`.rail__wordmark`, 12.5 px) draw from a 200–800 variable file of 564 code points to set 13 distinct glyphs. | `v2/shell.css:140`, `console.css:85`; measured: the same glyphs at 600/`opsz` 20 subset to **1.7 KB** (`_subsets/v5-wordmark-Newsreader-600-opsz20.woff2`) | The font choice is the owner's; the delivery is not. |
| 5 | **Arabic mixes registers and weights**: Noto Naskh Arabic (variable, 94 KB) for display and IBM Plex Sans Arabic in three static files (43–46 KB each) for the interface; the interface face's Kufi construction sits against a Latin serif display. | `fonts.css`; AD-A §3.2 «register mismatch» | The Arabic edition reads as two products. |
| 6 | **No metric-compatible fallbacks**: every face is `font-display: swap` with a bare system stack; Newsreader's ascent is 0.735 em against Georgia's 0.917, so the swap shifts every title. | `fonts.css`; measured vertical metrics (§9.4) | Part of the measured CLS 0.003–0.057 is font swap; on slow 4G the H1 visibly jumps. |
| 7 | **Stale names**: `tokens.css` (V1) still declares `--font-ui: "Fira Sans"`, `--font-ref: "Fira Mono"` and `--font-ui-ar` with a Fira fallback; V2 console pages still set titles in the serif. | `tokens.css:81-85`, `UI_INVENTORY.md` §9 | Coherence debt for whoever builds V5. |
| 8 | **Latin coverage is fine, French punctuation is not policed.** No template or locked string uses U+00A0 or U+202F before `:` `;` `!` `?` or inside « » (0 occurrences). | grep over `templates/`, `apps/cms/locked_content.py`, `locale/*/django.po` | French typographic spacing is a premium signal that costs nothing; it must become a content rule with a test, whatever the face. |
| 9 | **Italics are needed and available.** The hero lead is italic (serif), forum quote/note are italic; legal prose needs italics for titles of acts (*Testo Unico sull'immigrazione*). | `pages.css:183`, `forum.css:123,180` | Excludes upright-only UI candidates (Onest, Special Gothic). |

---

## 2. Brief → checks

| Owner's criterion | How this lane tested it |
|---|---|
| institution, modernity, quality, elegance, technology, international credibility | Boards with the real copy on navy and on paper; each face judged on register (newspaper / book / fashion / tech product / government / institution) and craft (spacing, italics, figures) |
| a very selective display face | The serif appears only where DS V4 §4.2 allows it (public H1, section titles, hero lead, forum/Academy public titles, wordmark) — and nowhere on the console |
| an excellent UI face for platform/dashboards/operational text | 13/14/15 px tiles at 2×; tabular figures; I/l/1 and 0/O tests; weights 400/500/600 on paper and on navy |
| optional reading face only if useful | Not added: the body copy stays in the UI sans (DS V4 §4.2 decision), the serif italic is the only «reading» voice, for the lead |
| no cheap fonts, no banal pairs, no editorial serif dominating operational screens | Controls rendered on purpose: EB Garamond + Lato (the tool's pairing), Inter, Figtree, Playfair; the serif is banned from the console by token |
| self-hosted, OFL/Apache, good Latin + fr/it diacritics | Every candidate's licence and Reserved Font Names read from the OFL texts; coverage measured (§4–§6) |
| Arabic needs its own paired face | Ten Arabic families measured and rendered (§6) |
| performance budget (LCP ≤ 2.5 s, CLS ≤ 0.10, INP ≤ 200 ms on slow 4G × CPU 4) | Byte counts per page from production-shaped builds; preload plan; fallback metrics; §9 |
| WCAG 2.2 AA, keyboard, reduced motion, RTL | §10 |

---

## 3. UI-UX-Pro-Max — what it returned, and what was kept

`python …/ui-ux-pro-max/scripts/search.py "<query>" --domain typography|google-fonts`, plus `"legal tech institutional platform government services" --design-system --variance 6 --motion 7 --density 6 -p "Italy Legal Entry"`.

| Query (domain) | Top returns | Verdict |
|---|---|---|
| institutional premium legal tech (typography) | Legal Professional = **EB Garamond / Lato**; Premium Sans = DM Sans; Tech Startup = Space Grotesk / DM Sans; Tech/HUD Mono; Luxury Minimalist; Crypto/Web3 | EB Garamond/Lato rendered as a control (§4, §5): Garamond as display accentuates the editorial-administrative reading the owner rejected (directive §87, README §«come si legge UI-UX-Pro-Max»); Lato is a 2010 humanist with no variable axis. DM Sans / Space Grotesk / Plus Jakarta are the banal pairs of the last five years. |
| government modern elegant (typography) | Noto Serif JP / Noto Sans JP; Enterprise SaaS Mobile = Plus Jakarta Sans; Corporate Trust = Lexend / Source Sans 3; Classic Elegant = Playfair Display / Inter; Accessibility First | Source Sans 3 measured and rendered (§5): its x-height (0.478) is too low for 13–15 px operational text. Lexend is a reading-aid face, wide and soft. Playfair/Inter is the cliché control. |
| dashboard ui sans variable (typography) | Dashboard Data; Flat/Neumorphism mobile; Premium Sans; **Financial Trust = IBM Plex Sans** («excellent for data») | Confirms Plex's reputation — and why it reads «bank/tool». |
| luxury editorial display serif modern; fintech trustworthy precise; editorial serif display institutional luxury; swiss grotesk neutral corporate; finance banking trust; variable font modern sans ui; elegant serif heading sans body (typography) | Playfair (×4), Source Serif 4 (in «Minimalist Monochrome Editorial»), Inter (×3), IBM Plex (×2), Lexend, Poppins/Open Sans, Outfit/Work Sans, Varela Round | Source Serif 4 taken to the board and kept (§4). Everything else is either the template signal (Inter, Poppins, Open Sans) or fashion (Playfair). |
| arabic multilingual (typography) | Arabic Elegant = Noto Naskh Arabic / Noto Sans Arabic | Both measured; Naskh kept only in pairing B; Noto Sans Arabic loses to Vazirmatn on weight parity and bytes (§6). |
| government modern elegant; institutional premium legal tech (google-fonts) | Adamina, Amethysta, Artifika, Belgrano, Brawler, Lustria, Vidaloka, Copse, Gupter, Marko One; Share Tech Mono | Single-weight display serifs from 2011–2013 with no italics or axes: not production-grade for a four-language system. |
| dashboard ui sans variable; grotesk neo-grotesque swiss (google-fonts) | **Instrument Sans**, Pontano Sans, Asta Sans, **Special Gothic**, Spline Sans, **Zalando Sans**, AR One Sans, Inclusive Sans; Familjen Grotesk, Space Grotesk, **Host Grotesk** | The useful part of the tool: it surfaced the 2024–2025 grotesques. Instrument Sans, Special Gothic, Zalando Sans, Familjen and Host Grotesk were downloaded, measured and rendered (§5). Host Grotesk became the recommendation. |
| serif display variable optical size; sans variable tabular numbers; serif display high contrast elegant; humanist sans latin-ext; monospace tabular data (google-fonts) | Kalnia Glaze, Funnel Display, Tourney, Pixelify Sans; Siyaq number fonts; TikTok Sans, Gilda Display, Libre Caslon Display; Average/Duru/Quattrocento Sans; Share Tech Mono, Monofett, Lekton | Keyword noise: the CSV matches words, not qualities. Funnel Sans was still taken to the board (§5). |
| arabic; arabic sans; arabic naskh (google-fonts) | Qahiri, Noto Naskh, Amiri Quran, Alkalami, Mirza, Ruwudu, Vibes, Scheherazade New, IBM Plex Sans Arabic, Noto Kufi, Almarai | Amiri (106 KB per weight), Almarai (no 500/600), Kufi (signage register) measured and set aside; §6. |
| `--design-system` run | Pattern «Enterprise Gateway», style «Accessible & Ethical», colours blue/green (#1E40AF / #16A34A), type **EB Garamond / Lato**, motion «stagger, back.out(1.4)» | Read element by element as the owner's clarification requires: the accessibility checklist (contrast 4.5, focus rings, reduced motion, 44 px targets) is already the project's; the type pairing is rejected above; the overshoot easing is banned by the project (`BRAND_ASSETS.md`, CD §2 pillar 5); the palette is the colour lane's business. |

---

## 4. Display candidates (Latin) — 14 measured, 12 rendered

Coverage was measured on the google/fonts masters where one exists (the fontsource «latin» files strip arrows and U+202F, so they under-report). «Instance KB» is the measured woff2 of one static instance at the display optical size, fr/it/en charset, hinting stripped, OFL notice kept (`scratch/fonts/_subsets/`).

| Face | Foundry / designer · licence · RFN | Axes / styles | fr/it coverage · figures | Personality on the board | Risks | Instance KB | Verdict |
|---|---|---|---|---|---|---|---|
| **Newsreader** (current) | Production Type, Hugues Gentile · OFL · no RFN | `opsz` 6–72, `wght` 200–800, true italic | complete; **no U+202F**; `tnum` default, `pnum`, `case`, `sups`; no small caps | Newspaper text serif; at 60 px caps it is honest but light; the italic is the best thing about it | Register «editorial» is precisely what §87 asks to demote; the current 300 weight is the worst instance of it | 21.6 (400/opsz 72) · italic 23.8 (static) | **Pairing B** (kept, re-set at 400) |
| **Source Serif 4** | Adobe, Frank Grießhammer · OFL · **no RFN in the google/fonts copy** (Adobe's own release names «Source» as RFN — use the google/fonts source, or rename the build) | `opsz` 8–60, `wght` 200–900, true italic | **complete, incl. U+202F, №, → ≤ ≥ ‰, minus**; `tnum` default + `pnum`, `lnum/onum`, `smcp/c2sc`, `case`, `zero`, `frac` | Transitional after Fournier: wide, stately capitals (the strongest «ITALY LEGAL ENTRY™» on the board), quiet lowercase, a superb italic at 22 px. Reads institution and publishing, not newspaper, not fashion | Association with Adobe products for designers; «quiet» rather than «memorable» — the memorability belongs to the door and the colour, not to the serif | **25.3** (400/opsz 48, no small caps) · 31.9 with small caps · **19.1 italic** (static, opsz 20) · 23.9 (400/opsz 60) | **Pairing A — recommended** |
| Literata | TypeTogether · OFL · no RFN | `opsz` 7–72, `wght` 200–900, italic | complete (no U+202F); `tnum/pnum`, `smcp` | Sturdy, large x-height, e-book warmth; the semi-upright italic is a signature but a distracting one on a lead | «Google Play Books» register; heavier colour on navy | 19.3 | considered, no |
| Spectral | Production Type · OFL · no RFN | static 200–800 + italics, no axes | complete (no U+202F); `smcp` | Sharper, more luxurious than its sibling Newsreader; caps slightly spiky | No optical axis; 7 static files for a full family; reads «premium magazine» | 21.2 (400, fontsource latin) | runner-up for pairing B if Newsreader is refused outright |
| Castoro | Tiro Typeworks · OFL · no RFN | static 400 + italic | complete (fontsource latin) | Venetian old-style; warm, scholarly, a gorgeous italic; the Venice link is real (Jenson, 1470) | One weight, no axes; reads «university press»; the reference is invisible to users | 26.5 | considered, no |
| Bodoni Moda | indestructible type, Owen Earl · OFL · no RFN | `opsz` 6–96, `wght` 400–900, italic | complete (no U+202F); `smcp`, `onum` | The Italian typographic monument (Parma). At 60 px caps on navy, dramatic and beautiful; at 44 px the hairlines dissolve, at 32 px they break | Fashion register (Vogue), hairlines on screen, unusable below ≈ 48 px; the board also showed a missing en/em dash in the instance — a build-verification item | 13.3 (400/opsz 96) | rejected for the system; a single hero moment at ≥ 56 px would be the only defensible use, and the owner did not ask for a fashion voice |
| Noto Serif Display | Monotype for Google · OFL · no RFN | `wdth` 62.5–100, `wght` 100–900, italic | complete (no minus) | Didone-ish, competent, anonymous | «Noto» = default | 12.4 | no |
| Fraunces | Undercase Type · OFL · no RFN | `opsz` 9–144, `wght` 100–900, `SOFT`, `WONK`, italic | complete (no U+202F) | Warm, characterful, DTC-brand voice even at WONK 0 | Trend of 2020–2023; not institutional | 16.4 | no |
| Instrument Serif | Instrument, Rodrigo Fuenzalida · OFL · no RFN | static 400 + italic | missing №, ≤ ≥ | Condensed contemporary display; the AI-startup landing page face of 2024–2025 | Cliché; one weight | 13.8 | no |
| DM Serif Display | Colophon · OFL · no RFN | static 400 + italic | complete (fontsource latin) | Heavy high-contrast display; agency/branding voice | Too loud for an institution; one weight | 24.2 | no |
| Gloock | Duarte Pinto · OFL · no RFN | static 400 | complete (no U+202F) | Blocky Didone display | Loud; one weight | 15.7 | no |
| Playfair Display | Claus Eggers Sørensen · OFL · **RFN «Playfair Display»** | `wght` 400–900, italic | complete (no U+202F) | The luxury cliché | Cliché; RFN forces renaming | 19.7 | control only |
| EB Garamond | Georg Duffner / Octavio Pardo · OFL · no RFN | `wght` 400–800, italic | complete (no U+202F) | Beautiful caps, small x-height; reads law firm, tradition, paper | Exactly the equivalence «institutional = editorial + serif» the directive calls wrong | 23.3 (400, fontsource latin) | control only (UI-UX-Pro-Max's pairing) |
| Mona Sans `wdth` 125 | GitHub, Deni Anggara · OFL · **RFN «Mona»** | `wdth` 75–125, `wght` 200–900, italic | complete (no U+202F) | Extended grotesque as a display voice: tech product, not institution | GitHub identity; RFN | 20.0 | no (as display) |

**Why Source Serif 4 over Newsreader.** Same class (transitional), same completeness of styles, but: capitals with Roman proportions instead of newspaper economy; a real `opsz` range that lets one static instance at 48 serve 30–76 px; the complete French repertoire including the narrow no-break space; small caps available if the public eyebrows ever want them; a lineage (Fournier → Bodoni) that connects France and Italy without a fashion face. It is also less visible on the web than Newsreader has become since 2023.

---

## 5. Interface candidates (Latin) — 22 measured, 18 rendered, 6 zoomed at 2×

«Var KB» is the measured woff2 of a variable slice `wght` 400–700 (or 400–600 where stated), fr/it/en charset; «italic» a static 400 italic subset.

| Face | Foundry · licence · RFN | Axes | x-height · avg width | Figures · features | fr coverage | Board at 13–15 px (2×) | Risks | Var KB · italic | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| **IBM Plex Sans** (current) | IBM, Abbink / Bold Monday · OFL · **RFN «Plex»** | `wght` 100–700, `wdth` 75–100, italic | 0.516 · 0.592 | tabular only; `lnum/onum`, `zero`, `case`, `salt`, ss01–06 | complete incl. U+202F | Legible, serifed I distinguishes I/l/1 (best of the set), squared terminals read «tool/IBM» | The default institutional open pairing; RFN means self-built subsets must be renamed | 29.1 (400–600) · 23.8 | control; retire (mono stays) |
| **Host Grotesk** | Element Type, Doğukan Karapınar (2024, v1.003) · OFL · no RFN | `wght` 300–800, true italic | 0.496 · 0.558 | tabular by default (no `pnum`); `case`, `calt`, `frac`, `sups`, `ordn`, `locl` (Turkish i), ss02 single-storey a, ss03 alt 3 6 9 | complete but **U+202F, №** | Warm neo-grotesque, open apertures, even colour at 13 px, excellent 500 on navy, true italic; I and l are identical strokes | Young family (2024): fewer features (no small caps, no proportional figures), no serifed I; must be watched for updates | **18.8** (400–700) · **13.8** | **Pairing A — recommended** |
| Public Sans | USWDS, Dan Williams (Libre Franklin lineage) · OFL · no RFN | `wght` 100–900, italic | 0.517 · 0.544 | `tnum/pnum`, `lnum/onum`, `calt`, `salt`, ss01 | no U+202F | Robust, the most «public service» colour at 15 px; wide tabular dates | Reads US government; plain rather than elegant | 22.4 · 13.8 | **Pairing B** |
| Mona Sans | GitHub, Deni Anggara · OFL · **RFN «Mona»** | `wdth` 75–125, `wght` 200–900, italic | 0.525 · 0.553 | `tnum` (slashed tabular zero), `pnum`, `case`, ss01–08 | no U+202F | Highest craft of the set; width axis gives condensed table heads and an extended display voice; slashed zero in data | GitHub identity for a developer audience; RFN → rename the build; heavier | 35.9 (400–600) · 21.5 | runner-up to Host |
| Hanken Grotesk | Alfredo Marco Pradil · OFL · no RFN | `wght` 100–900, italic | 0.493 · 0.545 | tabular default; `case`, ss01–03 | no U+202F, ↗ | Swiss, quiet; lighter and smaller at 13–15 px than Host; I/l identical | Helvetica-adjacent anonymity; needs +1 px at small sizes | 21.1 · 11.8 | considered |
| Instrument Sans | Instrument, Rodrigo Fuenzalida · OFL · no RFN | `wdth` 75–100, `wght` 400–700, italic | 0.510 · 0.569 | `tnum/pnum`, `case`, ss01–12 | no U+202F, №, ≤ ≥ | Narrow, modern, product-like; fine in tables | 2024–2025 trend (with Instrument Serif); no 300 | 29.6 · 17.3 | considered |
| Onest | Simpals, Voloshin / Kudryavtsev · OFL · no RFN | `wght` 100–900, **no italic** | 0.527 · 0.592 | `tnum/pnum`, `calt`, `case`, `salt`, ss01–02 | complete incl. U+202F | Crisp, the best 15 px colour of the set — but the italic on the board is a faux slant | No italic: excluded by §1 (9) | 21.4 · — | excluded |
| Source Sans 3 | Adobe, Paul D. Hunt · OFL · no RFN | `wght` 200–900, italic | 0.478 · 0.493 | `pnum` + tabular default, `smcp`, cv01–19 | complete incl. U+202F | Reads small at 15 px, «documentation» | Too small an x-height for console text | 27.1 · 16.5 | no |
| Geist | Vercel · OFL · no RFN | `wght` 100–900, italic | 0.530 · 0.581 | `tnum/pnum`, `case`, ss01–11 | no U+202F | Clean; the face of AI/startup 2024 | Cliché by association | 18.7 (400–600) · 13.1 | no |
| Inter 4 | Rasmus Andersson · OFL · no RFN | `opsz` 14–32, `wght` 100–900, italic | 0.546 · 0.640 | everything (`tnum`, `case`, cv01–14, ss01–08) | complete | Technically the best UI face available; and the definition of «template» | CD §1: «Newsreader + IBM Plex, non Inter» — the identity cost stands | 51.0 (400–600) · 25.0 | control |
| Schibsted Grotesk | Bakken & Bæck · OFL · no RFN | `wght` 400–900, italic | 0.527 · 0.582 | `tnum/pnum`, `zero`, `case` | no U+202F | Media grotesque; heavy files | 43.3 KB for one slice | 43.3 · 24.9 | no |
| Atkinson Hyperlegible Next | Braille Institute · OFL · no RFN | `wght` 200–800, italic | 0.496 · 0.533 | `tnum/pnum`, `case` | no U+202F, № | Distinctive disambiguated forms; reads «accessibility font» | Not a premium voice | 18.4 · 13.8 | no |
| Familjen Grotesk | Familjen STHLM · OFL · no RFN | `wght` 400–700, italic | 0.500 · 0.539 | `tnum/pnum`, `calt` | no U+202F | Narrow Scandinavian media grotesque | No 300/800; media register | 18.5 (fontsource var) · 12.2 | no |
| Albert Sans | Andreas Rasmussen · OFL · no RFN | `wght` 100–900, italic | 0.500 · 0.556 | `liga`, `frac` only | no U+202F | Geometric-humanist, soft; I/l identical | Too soft for legal | 31.3 · 10.3 | no |
| Special Gothic | Alistair McCready (2025) · OFL · no RFN | `wght` 400–700, **no italic** | 0.504 · 0.491 | `tnum/pnum` | no U+202F | Trade Gothic voice; faux italic | No italic | 31.7 · — | excluded |
| Zalando Sans | Zalando (2025) · OFL · no RFN | `wght` 200–900, italic | 0.514 · 0.543 | `tnum/pnum`, `calt` | no U+202F | Its tabular figures render with very wide advances on the board («0 sur 3» gaps) | Corporate identity; rendering anomaly to investigate | 37.3 · 16.4 | no |
| Radio Canada | CBC/Radio-Canada · OFL · no RFN | `wght` 300–700, italic | 0.515 · 0.554 | `tnum/pnum`, `calt` | no U+202F | Clean humanist, plain | Broadcaster identity | 24.7 · 11.6 | no |
| Funnel Sans | Dicotype (2024) · OFL · no RFN | `wght` 300–800, italic | 0.500 · 0.542 | `tnum/pnum` | no U+202F | Tech product | Trend | 17.0 · 11.2 | no |
| Hubot Sans, Wix Madefor Text, Figtree, Lato | GitHub (RFN «Hubot»), Wix/Dalton Maag, Erik Kennedy, Łukasz Dziedzic | — | — | — | — | Measured; Figtree and Lato rendered as controls | Identity (Hubot, Wix), cliché (Figtree), 2010 (Lato) | — | no |

**Why Host Grotesk.** On the 2× tiles it is the face that keeps an even, warm colour from 12 px eyebrows to the 28 px console title, sets 500 on navy without clogging, has a true italic, and does not carry an identity (IBM, GitHub, Vercel, US government, Adobe) or a trend (Instrument, Geist, Inter). It is small (18.8 KB for 400–700) because it is a disciplined family, not because it lacks glyphs (404 code points). Its two real limits are known and mitigated: I/l are identical strokes (references, hashes and IDs are always in Plex Mono, whose I is serifed and whose zero is slashed; Italian «Il …» at sentence start is disambiguated by the word) and figures are tabular-only (correct for the console; in public prose the slight gap around «1» is acceptable and is the same limit the current Plex has). It has no U+202F: the content rule in §8.3 uses U+00A0, which every face has.

**Why not Mona Sans, the closest rival.** Better features (slashed tabular zero, width axis, small-size stylistic sets), but 36 KB against 19, a Reserved Font Name that forces renaming every build, and an identity that half the ecosystem's technical partners will recognise as GitHub's. If the owner wants the width axis for dense tables, Mona is the upgrade path and its licence handling is documented in §8.5.

---

## 6. Mono and Arabic

### 6.1 Mono (references `E46E03B461`, hashes, rule versions, folio ordinals)

| Face | Licence · RFN | Default figures · `zero` | Subset KB (400) | Verdict |
|---|---|---|---|---|
| **IBM Plex Mono** (current) | OFL · **RFN «Plex»** | tabular · slashed zero via `zero` · serifed I | **8.8** (own subset) / 14.4 (fontsource file, no renaming needed) | **kept** in both pairings: nothing better for 13 px references; already vendored and documented |
| JetBrains Mono | OFL · no RFN | tabular · `zero` | 8.7 | IDE voice; no |
| Geist Mono | OFL · no RFN | tabular · ss01–11 | 8.2 | Vercel; no |
| Fragment Mono | OFL · no RFN | tabular · `zero`, `smcp` | 13.9 | Helvetica-mono, the most «quiet» match for a grotesque; optional upgrade, +5 KB, no functional gain |

RFN note: a self-built subset of Plex Mono is a Modified Version and must not carry the name «Plex» internally; either keep using the fontsource file (as today) or rename the build's name IDs (`ILE Mono`). The CSS `font-family` string is free in both cases.

### 6.2 Arabic — 12 measured, 10 rendered

Arabic-range builds (Google's «arabic» ranges without the mathematical alphanumerics), `rlig/init/medi/fina/calt/kern/mark/mkmk` kept.

| Face | Designer · licence | Axes | Register on the board (48 px display / 15 px body) | Pairs with | Build KB | Verdict |
|---|---|---|---|---|---|---|
| **IBM Plex Sans Arabic** (current UI) | Abbink, Morcos, Apelian · OFL · RFN «Plex» | static 100–700 | Modern Kufi-influenced sans; compact body; strong | Plex Sans (superfamily) — the argument dies with Plex Sans | 28.9 + 31.3 + 31.1 (400/500/600) = **91.3** | replaced |
| **Vazirmatn** | Saber Rastikerdar · OFL · no RFN | `wght` 100–900 | Contemporary, neutral, the best small-size legibility of the set; loops open at 13–15 px; tabular figures; `locl` ARA forms; both Arabic-Indic and Persian digit sets | a neo-grotesque (Host, Public Sans): weight and width parity with Segoe UI Arabic 97 % (§9.4) | **31.5** (400–700 variable) · 19.0 (400 static) | **Arabic UI, both pairings** |
| Noto Sans Arabic | Monotype / Chahine, Qandah · OFL | `wdth`, `wght` | Neutral modern; heavier files | any sans | 42.2 (400 static) · 90.2 (400–700 slice) | no (bytes) |
| Noto Kufi Arabic | Monotype · OFL | `wght` | Wide geometric Kufi; signage | — | 43–46 per weight | no (register) |
| Readex Pro | Jockin, Shaver-Troup · OFL | `wght`, `HEXP` | Lexend-derived, wide and rounded; tiny files | Lexend | 15.4 (400–700) | no (reading-aid register) |
| Alexandria | Mohamed Gaber · OFL | `wght` | Bold geometric; loud | — | 30.6 (fontsource var) | no |
| Beiruti | Arlette Boutros · OFL | `wght` | Elegant, condensed, Naskh-derived sans; distinctive at 48 px, small at 15 px (low loop height) | a display role only | 37.0 (400–700) | considered for Arabic display; loses to Markazi on text sizes |
| **Markazi Text** | Borna Izadpanah, Fiona Ross · OFL · no RFN | `wght` 400–700 | Naskh-flavoured text face with modern proportions; refined at 48 px on navy, readable at 15 px; the correct cross-script partner of a Latin transitional serif | Source Serif 4 (pairing A) | **20.8** (400) · 36.8 (400–600) | **Arabic display, pairing A** |
| Noto Naskh Arabic (current display) | Monotype · OFL | `wght` 400–700 | Traditional administrative Naskh; correct, dense, small on the em | Newsreader (pairing B) | 46.1 (400) · 82.6 (400–600) | **pairing B** |
| Almarai | Boutros · OFL | static 300/400/700/800 | Competent Kufi sans; no 500/600 | — | 29–32 per weight | no |
| Amiri | Khaled Hosny · OFL | static | Classical Naskh, Quranic register | — | 106 per weight | no (bytes, register) |
| Tajawal | Boutros · OFL | static | Geometric Kufi, light files, small repertoire | — | 8–9 per weight | no (register) |

**Size parity.** Markazi and Noto Naskh sit low on the em (size-adjust against Segoe UI 76.8 % and comparable): under `:lang(ar)` the display roles are set at **1.15×** the Latin size and the body line-height at 1.75. Vazirmatn needs no correction (97 %). These factors are written into `tokens-v5-type.css`.

---

## 7. The wordmark — untouched font, new delivery

The lock-up stays Newsreader 600, uppercase, tracking .13 em, 20 px (14 px below 48 rem), with the console rail variant at 12.5 px. The owner has not authorised a font change and none is proposed. What changes is how those 13 glyphs reach the browser:

| Option | What ships | Bytes on every page | Fidelity | Notes |
|---|---|---|---|---|
| Today | `newsreader-200-800-normal-latin.woff2`, preloaded | 128.9 KB | — | also feeds the public titles; in pairing A it feeds nothing else |
| **A1 — glyph subset (measured)** | `ILE Wordmark` = Newsreader instanced at 600 / `opsz` 20, subset to the text «ITALY LEGAL ENTRY™» with `kern` + `case`, `unicode-range` limited to those code points | **1.7 KB** (`council/typography/fonts/v5-wordmark-Newsreader-600-opsz20.woff2`) | pixel-identical at 20 px and 14 px; at 12.5 px the `opsz` 20 outlines are marginally heavier than the auto-`opsz` today — invisible on the navy rail | zero risk, one `@font-face`, keeps the text selectable and translatable (it is not translated: `dir="ltr"`) |
| A2 — outlined SVG | `static/brand/v2/wordmark.svg` with the three fills and a `currentColor` variant for dark | 0 KB of font; ≈ 3 KB SVG, inlined or sprited | exact at any size; immune to font loading, FOUT and fallback | needs the owner's nod («technique, not font»); `<title>` and `aria-label`; the H1 cannot use it (text) |

Recommendation: A1 now (it is measured and reversible), A2 as the end state once the owner confirms.

**The hero H1.** `p3.hero.title` is locked as «ITALY LEGAL ENTRY™»; its typeface is design. Rule: the H1 is a title, not a logo — it is set in the display serif (Source Serif 4, 400, `--t-display`, tracking +0.02 em, `font-feature-settings: "case"`) and the lock-up 40 px above it stays the logo. The board shows Source Serif 4 producing the most monumental version of that line. If the owner wants strict sameness between logo and H1, the fallback is to set the H1 in `ILE Wordmark` (same 1.7 KB file); it is not recommended: 600/`opsz` 20 outlines at 72 px look heavy and newspaper-like.

---

## 8. The system

### 8.1 Families and tokens (pairing A; pairing B in `tokens-v5-type.css` behind a comment)

```css
--f-serif:   "Source Serif 4", "ILE Serif Fallback", "Iowan Old Style", Georgia, "Times New Roman", serif;
--f-sans:    "Host Grotesk", "ILE Sans Fallback", "Segoe UI", Roboto, "Helvetica Neue", Arial, system-ui, sans-serif;
--f-mono:    "IBM Plex Mono", ui-monospace, "Cascadia Mono", Consolas, monospace;
--f-wordmark:"ILE Wordmark", "Newsreader", "Iowan Old Style", Georgia, serif;   /* .lock__wm, .rail__wordmark only */
--f-serif-ar:"Markazi Text", "ILE Arabic Display Fallback", "Segoe UI", "Geeza Pro", "Noto Naskh Arabic", serif;
--f-sans-ar: "Vazirmatn", "ILE Arabic Fallback", "Segoe UI", "Geeza Pro", "Noto Sans Arabic", sans-serif;
--f-arabic-sys: "Segoe UI", "Noto Sans Arabic", "Geeza Pro", system-ui, sans-serif; /* the «ع» control on Latin pages: kept, measured saving 44.5 KB */
```

The V2/V4 aliases (`--font-ui`, `--font-ref`, `--font-mono`, `--font-ui-ar`, `--font-display`, `--font-display-ar`) are re-pointed in the proposal so that every layer of the cascade changes face at once, as V4 did. `tokens.css` (V1) drops its Fira strings.

### 8.2 Usage map

| Surface | Display serif | Sans | Mono | Arabic |
|---|---|---|---|---|
| **Portico (public)** | H1 of every public page; hero H1; section titles (`--t-band`); hero lead in italic; forum and Academy public titles; the pull quote of the forum band (italic) — *only these* | eyebrows, navigation, mega-menu, body copy 17/28, entrance titles 22/28 600, cards, CTAs, chips, notices, footer, forms | folio references, dates in the voyage, programme meta | `:lang(ar)`: Markazi for the serif roles at 1.15×, Vazirmatn for everything else, Western digits everywhere (DS V4 rule kept) |
| **Entrance (login, signup)** | the door panel's one title | everything else | — | idem |
| **Console** | **never** (wordmark excepted) | all text: ContextHeader 28/36 600, sections 20/28 600, cards 17/24 600, body 15/24, controls 14/20 500, meta 13/20, captions 12/16 500, eyebrows 11/16 600 .06em, numerals 28/32 500 `tnum` | references 13/20, hashes, rule versions, chip counters | Vazirmatn only |
| **Back-office (Unfold)** | never | Host Grotesk if Unfold's font setting is overridden; otherwise Unfold's Inter stays (staff only) | idem | idem |
| **E-mail, PDF** | out of scope; system fonts | | | |

Rule of the serif, unchanged from DS V4 §4.2 and now enforceable by token: `--f-serif` is read only by `.t-display`, `.t-plate`, `.t-title`, `.t-band`, `.t-lead`, `.page-header__title`, forum/academy public title classes and `.lock__wm`; a test greps the console sheets for `--f-serif` and fails on any hit.

### 8.3 Setting rules

- **Figures.** `font-variant-numeric: tabular-nums` on every date, count, reference, amount and numeric column (V4 rule kept; Host is tabular by default so the rule is belt-and-braces); `slashed-zero` in mono. Dates `12.10.2026`, amounts `1 250,00 €` with U+00A0 as thousands separator and before `€`.
- **French spacing.** U+00A0 (no-break space) before `:` `;` `!` `?` and inside « »; **not** U+202F, which Host Grotesk lacks (Source Serif 4 has it). One content rule, one test over `templates/`, `locked_content.py` and the `.po` files; today there are zero occurrences of either, so the rule starts clean.
- **Capitals.** Eyebrows stay sans, 600, `.06em`, uppercase, with `font-feature-settings: "case"` (Host has `case`); the display serif never goes uppercase below `--t-title`, and the brand H1 gets `+0.02em`. Arabic: `text-transform: none`, `letter-spacing: 0` (joining script), as `base.css:211` already does.
- **Italic.** Serif italic for the lead and the forum quote only; sans italic for `<em>` in prose and legal titles; no synthetic italics anywhere (`font-synthesis: none`); Arabic has no italic — `em` under `:lang(ar)` becomes weight 500.
- **Optical sizes.** Shipped as static instances (`opsz` 48 roman, `opsz` 20 italic), not as an `opsz` axis: the measured variable slice `opsz` 20–60 / `wght` 400–600 is 88.7 KB against 25.3 + 19.1 KB, and the visual difference between `opsz` 48 and 60 at 72 px is below what the gate reviewers measured as a defect.
- **Weights.** Sans 400 body, 500 controls and rail, 600 titles ≤ 28 px, 700 only for `<strong>` in public prose; serif 400 only (300 retired: it was the thin hero); mono 400.
- **Line length and leading.** Public body 17/28 at ≤ 65 ch; lead 20/28 at ≤ 60 ch; console body 15/24; every line-height a multiple of 4 px (existing test).

### 8.4 Scale — portico (public)

| Token | V4 | **V5 proposal** | Family · weight · tracking | Why |
|---|---|---|---|---|
| `--t-display` | clamp(44 → 76) / 0.96 · serif 300 | **clamp(2.5rem, 1.4rem + 3.4vw, 4.5rem) = 40 → 72 / 1.0** · serif **400** · +0.02em when uppercase, −0.015em otherwise | Source Serif 4's capitals are wider than Newsreader's; 72 px fills the same measure as 76 did; weight 400 is the fix for the thin brand line |
| `--t-plate` | 52/56 | **48/52** | serif 400 · −0.015em | landing titles |
| `--t-title` | 40/44 | **38/44** | serif 400 · −0.01em | page H1 |
| `--t-band` | 32/36 | **30/36** | serif 400 · −0.005em | section titles |
| `--t-entry` | 22/28 · sans 600 | 22/28 · sans 600 | — | unchanged |
| `--t-lead` | 20/28 · serif italic | 20/28 · serif italic 400 (`opsz` 20 instance) | — | unchanged; the italic file is loaded only where a lead exists |
| `--t-body` | 17/28 · sans 400 | 17/28 · sans 400 | — | Host at 17 px measured comfortable |
| `--t-ui` | 15/20 · 500 | 15/20 · 500 | — | |
| `--t-small` | 14/20 | 14/20 | — | |
| `--t-caption` | 12/16 · 500 | 12/16 · 500 | — | |
| `--t-folio` | 13/16 · mono · .06em | 13/16 · mono · .06em | — | |

### 8.5 Scale — console

Numbers unchanged from DS V4 §4.3 (28/36 · 20/28 · 17/24 · 15/24 · 14/20 · 13/20 · 12/16 · 11/16 · numeral 28/32 · ref 13/20 mono): the scale was designed for a 0.516 x-height and Host is 0.496 (−4 %). On the 2× tiles the 13 px meta stayed legible; the gate must confirm it on a 1× 1366 × 768 laptop (the owner's device class), and the one lever if it fails is `--u-small: 13.5px`, not a face change.

### 8.6 Arabic under `:lang(ar)`

`--f-serif → --f-serif-ar`, `--f-sans → --f-sans-ar`; display roles × 1.15 (`--t-display` 46 → 83, `--t-title` 44, `--t-band` 34); body line-height 1.75 public / 1.7 console; `letter-spacing: 0`; `text-transform: none`; `min-inline-size: 120px` on buttons (V4 rule); Western digits; `em` → weight 500; references stay LTR in mono (`dir="ltr"`, `unicode-bidi: isolate`).

---

## 9. Loading, payload, performance

### 9.1 Files (pairing A) — measured, `council/typography/fonts/`

| File | Face · style | Range | KB | Loaded when |
|---|---|---|---|---|
| `v5-HostGrotesk-var-400-700.woff2` | Host Grotesk, variable `wght` 400–700 | latin (fr/it/en charset in one file) | **18.8** | every page — **preloaded** |
| `v5-HostGrotesk-400-italic.woff2` | 400 italic | latin | 13.8 | when an `<em>` exists (browser loads on use) |
| `v5-SourceSerif4-400-opsz48-nosc.woff2` | Source Serif 4, 400 roman, `opsz` 48 | latin | **25.3** | public pages — **preloaded** on public templates only |
| `v5-SourceSerif4-400-italic-static.woff2` | 400 italic, `opsz` 20 | latin | 19.1 | home hero lead, forum quote |
| `v5-IBMPlexMono-400.woff2` | Plex Mono 400 (or the 14.4 KB fontsource file to avoid renaming) | latin | 8.8 | pages with references |
| `v5-wordmark-Newsreader-600-opsz20.woff2` | `ILE Wordmark` | 13 code points | 1.7 | every page (or 0 with SVG) |
| `v5-Vazirmatn-var-400-700-arabic.woff2` | Vazirmatn variable | arabic | 31.5 | `/ar/` — preloaded |
| `v5-MarkaziText-400-arabic.woff2` | Markazi Text 400 | arabic | 20.8 | `/ar/` public |
| **Total on disk** | 8 files | | **139.8** | today 26 files, 965 KB |

No `latin-ext` split: the four languages are fr/it/en/ar and one Latin file with Œ œ Ÿ ẞ … covers them; `unicode-range` is still declared so that Arabic files never load on Latin pages and vice-versa (the «ع» control keeps `--f-arabic-sys`).

### 9.2 Per page

| Page | Today (README, gzip runs) | Pairing A | Pairing B | Preloaded bytes today (Newsreader 128.9 + Plex 400 22.1; `/ar/`: Noto Naskh 94.0 + Plex Arabic 400 42.8) → A |
|---|---|---|---|---|
| Home, Latin | 356.1 KB (Newsreader 128.9 preloaded + italic 143.4 + Plex 83.8) | **73.7** (18.8 + 25.3 + 19.1 + 8.8 + 1.7) | 92.1 (Newsreader 21.6 + italic 23.8 + Public Sans 22.4 + italic 13.8 + mono 8.8 + wordmark 1.7) | 151.0 → **44.1** |
| Public page without lead | ≈ 300 | 54.6 | 54.5 | 151.0 → 44.1 |
| Entrance (login) | 214 (after the «ع» fix) | 54.6 (serif title, no italic) | 54.5 | 151.0 → 44.1 |
| Console dashboard | ≈ 214 | **29.3** (18.8 + 8.8 + 1.7) | 32.9 | 151.0 → 18.8 |
| Arabic home | ≈ 509 | **81.6** (31.5 + 20.8 + 18.8 + 8.8 + 1.7) | 110.5 (Noto Naskh 46.1 + Vazirmatn 31.5 + Public Sans 22.4 + mono 8.8 + wordmark 1.7) | 136.8 → 52.3 |

Budget proposed in verification 9: fonts ≤ 200 KB per page. Both pairings sit under half of it on every page; A is under 100 KB everywhere.

### 9.3 Effect on the budget (LCP ≤ 2.5 s, CLS ≤ 0.10, INP ≤ 200 ms; slow 4G, CPU × 4)

- **LCP.** After the compression and preload work of 26 September the home LCP is 1.44–1.67 s on desktop (the door photo) and 1.42–1.82 s on mobile, where the element is **the lead — a text node, therefore font-dependent**. The README's decomposition attributed 1.24–1.66 s of the earlier 3.0 s to transfer contention with Newsreader italic (144 KB) mid-download. Pairing A removes that file from the home entirely (the lead's italic is 19.1 KB), cuts the preloaded font bytes from 151.0 KB to 44.1 KB and the page's total font bytes from 356.1 KB to 73.7 KB: on the profile's 1.6 Mb/s that is ≈ 0.5 s less on the critical path and ≈ 1.4 s less of contended transfer overall. Observed while building the specimen: a headless screenshot taken before the fonts arrived showed invisible text for every face still inside the default `font-display: auto` block period — the reason `swap` plus preload plus metric-matched fallbacks is the rule, and why the gate must screenshot after `document.fonts.ready`. **Estimate, to be measured in the gate:** mobile LCP −0.3 to −0.6 s; desktop unchanged (the photo). The budget is met today and stays met.
- **CLS.** Font swap is a shift source today (no overrides; Newsreader's ascent 0.735 vs Georgia 0.917). The fallback faces in §9.4 are metric-matched, so the swap moves nothing measurable; expected CLS contribution of fonts ≈ 0. `font-display: swap` stays (not `optional`: on a first visit over slow 4G, `optional` would show Georgia for the brand line and never swap).
- **INP / long tasks.** Fonts add no script; woff2 decoding is off the main thread. No change.
- **Requests.** Latin page: 3–5 font requests instead of 3–7; all `crossorigin`, same origin, `Cache-Control: immutable` with hashed names (ManifestStaticFilesStorage already does this).

### 9.4 Metric-matched fallbacks (computed from the files, Windows fallbacks)

| Web face | Local fallback | `size-adjust` | `ascent-override` | `descent-override` | `line-gap-override` |
|---|---|---|---|---|---|
| Host Grotesk 400 | Arial | 104.7 % | 96.9 % | 30.1 % | 0 % |
| Host Grotesk 400 | Segoe UI | 105.5 % | 96.2 % | 29.8 % | 0 % |
| Source Serif 4 400 `opsz` 48 | Georgia | 94.5 % | 109.7 % | 35.5 % | 0 % |
| Source Serif 4 400 `opsz` 48 | Times New Roman | 103.4 % | 100.2 % | 32.4 % | 0 % |
| Vazirmatn 400 | Segoe UI | 97.1 % | 105.6 % | 55.3 % | 0 % |
| Vazirmatn 400 | Tahoma | 98.2 % | 104.4 % | 54.7 % | 0 % |
| Markazi Text 400 | Segoe UI | 76.8 % | 109.2 % | 47.0 % | 0 % |
| Public Sans 400 (B) | Arial | 105.3 % | 90.2 % | 21.4 % | 0 % |
| Newsreader 400 `opsz` 72 (B) | Georgia | 101.3 % | 72.6 % | 26.2 % | 0 % |

Method: advance width of a 260-character French/Italian sample in each face over the same sample in the fallback (`size-adjust` = web ÷ fallback); ascent and descent from the file's typo or hhea metrics (whichever the `USE_TYPO_METRICS` bit selects) divided by `size-adjust`, as fontaine/capsize do. Missing and required before shipping: Roboto / Noto Sans Arabic / Noto Serif (Android), Helvetica / Times / Geeza Pro (Apple). They are written as `@font-face` rules with `src: local()` in `tokens-v5-type.css`.

### 9.5 Preload and order

Public Latin: `<link rel="preload">` for Host var, then Source Serif 4 roman (in that order: the sans paints the navigation first). Console: Host var only. `/ar/`: Vazirmatn, then Markazi on public pages. Nothing else is preloaded; italics and mono load on use. `fonts.css` keeps `font-display: swap`, adds `font-synthesis: none` at `:root`.

---

## 10. Accessibility and RTL

- **Contrast** is unaffected by faces; the lighter colour of Host at 400 is compensated by the existing ink tokens (14.62:1 on paper); the gate re-measures the 13 px meta at `--ink-3` (5.48:1).
- **WCAG 1.4.12 text spacing** (line-height 1.5, paragraph 2×, letter-spacing .12 em, word-spacing .16 em): Host and Source Serif 4 have no ligature-dependent shapes that break under letter-spacing; Arabic is exempt from letter-spacing by rule (`:lang(ar)` sets 0 and the test overrides must not apply it to joining scripts — note for the a11y lane).
- **200 % zoom / reflow**: the scale is rem-based except the console layout constants; unchanged.
- **Minimum sizes**: 12 px captions with weight 500 (V4) stay the floor; nothing below.
- **RTL**: mirrored logical properties are the shell's job; type-wise the rules of §8.6 apply, and the console references stay LTR isolated. Vazirmatn's `locl` Arabic forms are selected by `<html lang="ar">`, which Django sets.
- **Reduced motion, forced colours**: no type dependency. Font loading is not animated; no FOUT masking with opacity (a banned pattern: it hides the text behind a JS timer).
- **Cognitive**: one sans for every instruction, one serif for titles; no small caps in operational text; tabular figures on every number.

---

## 11. Subsetting and build plan

1. **Sources, pinned.** Variable masters from `google/fonts` (`ofl/hostgrotesk`, `ofl/sourceserif4`, `ofl/vazirmatn`, `ofl/markazitext`, `ofl/newsreader`) at a recorded commit; IBM Plex Mono from `@fontsource/ibm-plex-mono` 5.3.0 as today. `scripts/fetch_fonts.py` gains a `--build` step (fontTools `instancer` + `subset`, `fonttools[woff]` + `brotli` in the dev requirements; both are already importable in this environment, versions 4.60.2 / 1.1); the runtime never contacts a font host (CSP unchanged).
2. **Instances.** Host `wght` 400–700 slice (keeps the axis for 500/600/700), italic static 400; Source Serif 4 static 400 at `opsz` 48, italic static 400 at `opsz` 20; Vazirmatn `wght` 400–700 slice; Markazi static 400; Newsreader static 600 at `opsz` 20 for the wordmark; Plex Mono static 400.
3. **Charset.** Latin: U+0020–007E, U+00A0–00FF, U+0131, U+0152–0153, U+0178, U+02C6, U+02DC, dashes, quotes, bullets, ellipsis, ‰, ‹ ›, U+2009, U+202F, ⁄, €, №, ™, arrows, −, ∕, ≤ ≥ (the set measured here). Arabic: Google's «arabic» ranges without U+1EE00–1EEFF. Features kept: `kern liga calt ccmp locl mark mkmk tnum pnum lnum case zero frac sups ordn` (Latin), plus `rlig init medi fina isol curs dlig` (Arabic). Hinting dropped (as Google serves variable fonts). Name IDs 0, 1–6, 13, 14 kept: the OFL notice travels with every file.
4. **Reserved Font Names.** None of the four new families declares one (OFL texts read: Source Serif 4 google/fonts copy, Host Grotesk, Vazirmatn, Markazi Text, Newsreader, Public Sans, Noto). IBM Plex declares «Plex»: a self-built Plex Mono subset must be renamed internally (`ILE Mono`) or the fontsource file kept as is.
5. **Registration.** `docs/IMAGE_LICENSES.md` §6 and `docs/design-v2/FRONTEND_DEPENDENCIES.md` list the five families, authors, OFL, source commit, build date; `static/fonts/` holds the OFL texts.
6. **Verification in the build.** A test opens every shipped woff2 with fontTools and asserts: the fr/it charset is present (the Bodoni dash gap on the board is the kind of defect this catches), `tnum` figures are equal-width, the wordmark file contains exactly its 13 code points, no file exceeds its budget (roman ≤ 30 KB, var sans ≤ 22 KB, Arabic ≤ 35 KB), and no `@font-face` names a missing file. `tests/frontend/test_v4_tokens.py` and `test_design_docs.py` update their family strings; `test_css_bundle_is_current.py` is unaffected.
7. **Rollout order** (after owner decisions, inside the V5 gates): tokens + fonts.css + preloads (one commit, measured) → public templates (display roles) → console (no visual change but the face) → Arabic → wordmark A2 if approved. Re-measure LCP/CLS after every step (memory rule: re-probe every page a shared sheet touches).

---

## 12. Risks and owner decisions

| Risk | Severity | Mitigation |
|---|---|---|
| Two serif families on the same page (Newsreader lock-up, Source Serif 4 H1) | design | Lock-up is the logo (SVG or 1.7 KB face), the H1 is typography; both transitional, same axis of contrast; the board shows them together. If refused → pairing B. |
| Host Grotesk is a 2024 family (v1.003): future updates may change metrics | medium | Pin the source commit; the build test guards metrics; the fallback overrides are recomputed by the build script, not by hand. |
| I/l identical in Host (Italian «Il», names) | low | References/IDs always in Plex Mono; `Il` disambiguated by words; if the gate finds a real case, Mona Sans (serif-less too) does not help — Plex Sans or Atkinson would, at an identity cost. |
| No proportional figures in Host (public prose) | low | Same limit as today's Plex; acceptable; Source Serif 4 has `pnum` for the lead. |
| Arabic faces unreviewed by a native reader | medium | One review of `specimen.html` (Arabic section) before the gate; fallback is Noto Naskh + Vazirmatn (pairing B's Arabic). |
| Fallback metrics for Android/Apple not computed | medium | Compute on a Mac and an Android before shipping the fallback faces; until then the overrides only help Windows. |
| Markazi's small size on the em | low | 1.15× display factor in the tokens; verify at 390 px. |
| Plex RFN if subsetting Plex Mono locally | low | Rename or keep the fontsource file. |

**Owner decisions needed** (nothing here is decided by this lane):
1. Pairing A (Source Serif 4 + Host Grotesk) or B (Newsreader re-set + Public Sans).
2. Wordmark delivery: A1 subset now, A2 SVG later — or keep the full Newsreader file (costs 127 KB per page for nothing).
3. Replace IBM Plex Sans Arabic with Vazirmatn (both pairings) — subject to the Arabic reader review.
4. The forum quote: Source Serif 4 italic (A) instead of Newsreader italic; or drop the italic there.
5. Optional: Mona Sans instead of Host if a width axis is wanted for dense staff tables (accepting RFN renaming and the GitHub association).

---

## 13. Evidence index

| What | Where |
|---|---|
| This report | `C:/tmp/ile_v5_council/council/TYPOGRAPHY.md` |
| Token and `@font-face` proposal (not wired) | `C:/tmp/ile_v5_council/council/typography/tokens-v5-type.css` |
| Owner specimen (both pairings, public + console + Arabic) | `C:/tmp/ile_v5_council/council/typography/specimen.html`, `specimen.css`, `fonts/` (8 + 5 measured files, 4 OFL texts), `specimen.png` |
| Boards and tiles (all candidates, 1:1 and 2×) | `C:/tmp/ile_v5_council/scratch/typography/specimens/` (`display2.png`, `ui2.png`, `arabic.png`, `zoom.png`, `tiles/`) |
| Measurements | `scratch/typography/{analysis.json,masters.json,masters.txt,subsets.json,subsets.txt,summary.txt}`; production builds `scratch/fonts/_subsets/v5-*.woff2` |
| Tools (all read-only towards the repository) | `scratch/typography/tools/{download.py,masters.py,analyse.py,masters_analyse.py,summarise.py,subset_measure.py,measure_v5.py,specimens.py,specimens2.py,zoom.py,tiles.py}` |
| UI-UX-Pro-Max raw output | `scratch/typography/upm_typography.txt`, `upm_gfonts.txt` (+ the session's additional queries quoted in §3) |
| Candidate font files (measurement only, never into the repository) | `scratch/fonts/<family>/` (fontsource), `scratch/fonts/_masters/` (google/fonts masters + OFL), `scratch/fonts/_extra/` |
