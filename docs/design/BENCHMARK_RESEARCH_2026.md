# BENCHMARK RESEARCH 2026 — design istituzionale europeo

Ricerca del Design Council · 20 settembre 2026 · Tre indagini indipendenti

Scopo: **estrarre principi, non clonare**. Il sito deve avere la *qualità* di un portale
istituzionale senza impersonarne uno (direttiva §69). Ogni relazione dichiara che cosa è
trasferibile e, soprattutto, che cosa **non** va preso perché ci farebbe somigliare a un sito
governativo.

Le tre indagini:

1. **Designers Italia (.italia), Europa Component Library, AGID** — le linee guida ufficiali vigenti.
2. **Portali istituzionali e legal-tech europei 2024–2026** — che cosa funziona e perché.
3. **Interfacce professionali di gestione pratiche** — per la piattaforma autenticata.

---

# Benchmark research 2026 — Designers Italia (.italia), Europa Component Library, AGID

**Research key:** `benchmark-italia-eu` · **Compiled:** 20 September 2026 · **Method:** direct retrieval of the official documentation sites (designers.italia.it, docs.italia.it, ec.europa.eu/component-library, commission.europa.eu, agid.gov.it, accessible-eu-centre.ec.europa.eu) plus GitHub release metadata. Every figure below is quoted from the source; anything I could not confirm is marked **[UNVERIFIED]** in §7.

**Why these three sources and not a mood board.** The client's objection is not "make it prettier", it is "make it credible in front of a Region, a Chamber of Commerce, a university and a consulate". The institutions that judge us already have a house style, and both .italia and ECL are the written form of that style. Copying their *branding* would be impersonation and is forbidden (§6). Copying their *reasoning* — how they decide density, when a card is legitimate, how a notice is ranked, how much of a 1920 viewport an institutional page is allowed to occupy — is exactly what separates "world-class institutional" from "generic SaaS". This document extracts the reasoning.

---

## 1. Version state as of 20 September 2026

| Resource | Current version | Date | Note |
|---|---|---|---|
| Design system .italia — documentation | **1.13.0** | **15 July 2026** | Version register at `designers.italia.it/design-system/fondamenti/versionamento/` |
| UI Kit Italia (Figma/Sketch) | **3.8.0** | via GitHub releases | `italia/design-ui-kit` |
| Design Tokens Italia | **1.2.1** | via GitHub releases | `italia/design-tokens-italia`, CSS + SCSS output |
| Bootstrap Italia | **2.18.3** | via GitHub releases | Bootstrap 5 theme, BSD-3-Clause |
| Bootstrap Italia v3 | **3.0.0-beta** | in development | not stable — do not model on it |
| Dev Kit Italia (web components) | **1.0.0-beta.0** | in development | community call opened March 2025 |
| Europa Component Library (ECL) | **v5.3.0** | **15 September 2026** | `ec-europa/europa-component-library`; v5.0.0 shipped 17 June 2026, so the whole v5 line is four months old |
| Linee guida di design per i siti internet e i servizi digitali della PA (AGID) | adopted by determinazione **n. 224/2022**, page last updated **8 October 2025** | | binding under art. 53 c.1-ter CAD |
| Manuale operativo di design | **2025.1** | | adds a "Norme e riferimenti" section mapping each legal requirement to a tool |
| EN 301 549 | **v4.1.1** | **September 2026** | adopts **WCAG 2.2**; *not yet* the legal reference (see §5) |

The .italia system follows **semantic versioning** (MAJOR.MINOR.PATCH, with `-alpha`/`-beta` suffixes signalling "tutto può ancora cambiare"). ECL is on a roughly fortnightly minor cadence (5.0.0 → 5.3.0 between 17 June and 15 September 2026). **Practical consequence for us:** pin what we borrow to a dated reading. Do not write "follows the .italia design system" in any public copy — that is both untrue and, per §6, undesirable.

---

## 2. Designers Italia / design system .italia — what the system actually says

### 2.1 Foundations (18 published)

`principi-e-intenzioni`, `identita`, `accessibilita`, `design-tokens`, `contenuti`, `linguaggio`, `microtesti`, `tono-di-voce`, `versionamento`, `colori`, `tipografia`, `griglia`, `spaziature`, `ombre`, `bordi-e-raggi`, `dimensioni`, `proporzioni`, `icone`.

Note the ordering: **six of the first eight foundations are about language, content and tone, not pixels.** In a system built for institutional credibility, "Linguaggio", "Microtesti" and "Tono di voce" are peers of "Colori". That is itself the first transferable principle.

### 2.2 Grid

- **6 columns** below 576px; **12 columns** at 576px and above.
- **Margin** (outer edge of the grid container): **12px**, fixed.
- **Gutter (intercolonna)**: 12px up to 767px; **24px** from 768px upward. An "intercolonna variabile" option scales 12 → 12 → 20 → 20 → 24 → 28px across the six breakpoints.
- **Container max-widths:** <576 = 100%; S 576 = **540px**; M 768 = **720px**; L 992 = **960px**; XL 1200 = **1176px**; XXL 1400 = **1320px**.
- Rule: *"È buona prassi che sia il contenuto a determinare il numero di colonne"* — the content decides the column count, not a house template. Named layouts include the 2-column equal split, the **2/3 + 1/3** sidebar, and 3–4 column grids.

**The number that matters: 1320px at XXL.** A national-scale institutional system lets its container grow to 1320px, and it *changes* the container at each breakpoint rather than freezing one width.

### 2.3 Typography

Families and roles: **Titillium Web** (primary — titles, subtitles, interactive elements, paragraphs; "geometric character that guarantees flexibility"); **Lora** (serif, for *long* reading passages, "to facilitate the reading of texts on digital devices"); **Roboto Mono** (technical data, numbers, codes).

| Level | Size | Line-height | Weight |
|---|---|---|---|
| H1 | 40–48px | 48–56px | Bold |
| H2 | 32–40px | 40–48px | Bold |
| H3 | 28–32px | 32–40px | Bold |
| H4 | 24–32px | 32–40px | SemiBold |
| H5 | 20–24px | 24–32px | SemiBold |
| H6 | 16–18px | 24px | SemiBold |
| Lead | 20–24px | 32px | Regular |
| Body (sans) | 12–18px | 24px | Regular |
| Body (serif) | 16–18px | 24px | Regular |
| Caption | 14px | 16px | Regular |
| Label | 16–18px | 24px | SemiBold |

Rules: **max 75 characters per line**; **4px baseline** and all vertical values as multiples of it; **"do not exceed four heading levels (H1, H2, H3, H4) per page"**; letter-spacing −1 on headings.

Two things to take from this table. First, the **H2 top of range is 40px against a 16–18px body — a ratio above 2.2**. Second, the system uses a **serif specifically for long-form reading**, not for display. Our build has inverted that (serif for display, sans for body), which is a defensible editorial choice, but it means we forfeit the "serif = long reading" affordance and must earn hierarchy purely by size, and currently we do not (§7.1).

### 2.4 Colour

Four typologies: **Primary** — "Blu Italia" `#0066cc`, described as the national PA identity colour; **Accent** — teal `#089994`, for interactive elements on saturated backgrounds; **System** — success (emerald), warning (orange), error (red), e.g. `color-emerald-8`, `color-orange-6`, `color-red-6`; **Neutral** — grey and slate for type, backgrounds and borders.

Token scheme: each hue has **10 numbered variants** by lightness (`color-blue-1` … `color-blue-10`, higher = darker).

Contrast: text **≥ 4.5:1**; large text (>24px) **≥ 3:1**; graphical elements **≥ 3:1**; none required for disabled or purely decorative elements. Colour "must support hierarchy rather than serve as the sole distinguisher" (WCAG 1.4.1).

**The adaptation clause is the one that concerns us directly:** the official Blu Italia represents PA digital identity *at national scale*; if you are designing territorial or local services, *"choose a dedicated primary colour"*. In other words the system itself instructs non-national actors to differentiate. Our deep institutional blue `#0f2b52` (`tokens.css:12`) is correct by this logic and must stay well away from `#0066cc`.

### 2.5 Spacing, borders, shadows

**Spacing** — base unit **4px**. Global tokens: `spacing.xxs` 4, `xs` 8, `s` 16, `m` 24, `l` 32, `xl` 40, `xxl` 48. Semantic tokens split by axis: `stack` (vertical, 8–48), `inline` (horizontal, 4–32), `inset` (internal padding, 16–48). Rule: *"define a hierarchy to manage distances between elements logically, using wider spaces between page sections and tighter spaces within a section or component."*

**Borders** — `border.base` 1px, `border.double` 2px, `border.thick` 4px, `border.broad` 8px.

**Radii** — only three: `radius.smooth` **4px**, `radius.rounded` **40px**, `radius.circle` **80px**. And an explicit rule that answers the client's "huge border-radius everywhere" complaint from the opposite direction: *"Gli angoli squadrati si addicono maggiormente a elementi che richiedono una presentazione più formale e strutturata, come modali o riquadri informativi"* — **square corners suit elements requiring a more formal, structured presentation, such as modals and informational boxes.** Rounding is for "visual lightness". Institutional weight is square.

**Shadows** — three stated purposes (hierarchy, readability by separating an element from its ground, depth) and three rules: proportional to the element's size and importance; **one consistent direction across the whole interface**; applied *sparingly*, "to avoid visual clutter". The page gives no numeric elevation ladder — it defers to the Bootstrap Italia implementation. **[Partially unverified: no token values published at the foundation level.]**

### 2.6 Components — 69 published, and the ones that matter to us

Navigation (15): Back, Back to top, **Breadcrumbs**, Bottomnav, Forward, **Header**, Megamenu, **Navscroll**, **Sidebar**, **Skiplinks**, Tabs, Thumbnav, Toolbar, Pagination, Sticky.
Forms (12): Autocomplete, Checkbox, Datepicker, Dropdown, Input, Number input, Radio, Select, Timepicker, Toggles, Upload, Transfer.
Feedback (4): **Alert**, **Callout**, **Notifications**, Tooltip.
Content (14): Accordion, Avatar, Badge, **Card**, Carousel, Chips, Collapse, Hero, **List**, Popover, Progress indicators, Rating, **Sections**, **Timeline**.
Layout/utility: Affix, **Form**, Footer, **Steppers**, **Tables**, Video player.

**Card — the single most useful finding for this project.** Cards are *"contenitori flessibili e versatili per organizzare e presentare contenuti strutturati"*, and the system requires each card to be **actionable, linking to a detail page**, and to carry **unique content — no repetition between cards**. It then states explicitly what a card must not be:

> do **not** use cards purely for decoration or visual framing;
> do **not** use a card simply to put a border around any kind of content.

It publishes **typed** card variants rather than one generic box: *editorial* (standard, featured, inline, mini), *event* (with period and dates), *media*, *service* (service icon + description), *document* (file type and size), *person*, *place*, *related links*. Markup requirements: semantic `article`, `time`, `address`; correct heading hierarchy; multiple cards grouped as `<ul>`/`<li>`.

**List** — *"raggruppare in una lista verticale una serie di contenuti correlati"*, with variants for avatars/icons/images, arrows, multiple actions, metadata, menu states (active, disabled, nested expandable) and link lists. The boundary is stated: *"le tabelle sono utili a mostrare set di dati più complessi"* — tables for richer data, lists for related items. Guidance: limit item count; order logically (alphabetical, numeric, or by frequency).

**Callout** — "a box with distinctive visual style to highlight important textual content on long pages". Variants: text, success, warning ("Attenzione"), danger/error, **Importante**, **Nota**, highlighted versions of each, and **Approfondimento** (a distinct style with background colour, folded-corner effect and action buttons). Anatomy: border (full or left-side only), highlighted title, representative icon, message body which may run to several paragraphs and contain links. Placement rule: insert *"at a strategic point on the page, such as the beginning of a section"* and use them **sparingly**.

**Tables** — use for inventories/lists where each entry is detailed by specific columns; comparative data; statistics; reports. *"Usa sempre le intestazioni delle colonne."* Limit column count. Enable sorting **only when necessary**, alphabetic or numeric. Variants: striped (light/dark), bordered with colour variations, borderless, compact, hover rows, coloured rows or individual cells, nested content, dark header with footer and caption. Responsive in two modes: *"Responsive, sempre"* and *"Responsive, breakpoint specifici"*.

**Timeline** — *"graphic representation of a series of events in chronological order to describe the history of an institution or the progress of a project."* Anatomy: placeholder (may hold an icon), date, the vertical line itself, event title, description (may contain links, images, buttons). Keep descriptions brief; distinguish entries clearly.

**Steppers** — *"elementi di navigazione che mostrano l'avanzamento dell'utente all'interno di una procedura complessa"*. Variants: text-only with step numbers; text + icon; ordered headers; step-by-step navigation buttons; mobile adaptations using a progress bar or dot indicators; dark-background versions. **Explicit "do not use" list:** when conditional logic can change the number of steps, when progression is not linear, or when steps need not be completed in order. The Form component cross-references it: *"puoi inoltre dividere il form in più passi, utilizzando il componente Stepper."*

**Form** — a wrapper that "groups and paginates correlated input fields". Labels and placeholders *"devono essere chiari e concisi"*. Insert captions and instructions **between** fields where they guide completion. Error microcopy *"deve aiutare le persone a completare la compilazione e risolvere in autonomia eventuali errori"*. On submit with errors, the form returns **an overall alert message plus per-field visual and informational validity cues** — i.e. summary *and* inline, not one or the other.

**Sections** — *"utile per organizzare e suddividere contenuti particolarmente ampi e complessi"*, with variants: base, muted background, primary-colour background, neutral, with background image, with cards. Guidance: *"creare sezioni con una struttura simile e posizionate in sequenza una dopo l'altra"*, and verify contrast whenever a background colour is customised. Notably **the Sections component exists in Bootstrap Italia and React but is absent from UI Kit Italia at v1.13.0** — the system itself treats the full-width band as an implementation pattern rather than a design primitive.

**Header** — three stacked bands. (a) *Slim header / top bar*: link to the **parent entity** ("ente di appartenenza", typically an external site), **language selector** — *"modifica la lingua di tutti i contenuti del sito"* — and a **login/access** button where a personal area exists. (b) *Central header*: entity icon or logo, entity name as text, optional subtitle describing the nature of the entity, social channels, search link; described as "essenziale" because it carries *"il brand dell'ente e la sua descrizione"*. (c) *Header nav*: a primary first-level menu and a secondary cross-cutting menu (tags, topics). Mobile: navigation hidden behind a menu icon, opening left-to-right.

**Icons** — from the Bootstrap Italia / UI Kit libraries. Five legitimate uses only: symbolising an interaction function (save, delete, send); navigation; categorising content type (video, image, document); loading/success feedback; social interactions. Rule: *"Ti consigliamo di abbinare un'icona a un'etichetta di testo che ne chiarisce la funzione"* — pair an icon with a text label; an icon may stand alone only when *"il simbolo è chiaro e non ambiguo"*, and even then the text label **must** remain available to a screen reader. There is no category for "one decorative icon per card to fill the space", which is what a generic SaaS grid does.

### 2.7 Principles and models

The six stated principles: a **coherent citizen experience** across 22,000+ administrations so the State reads as one; **accessible language** replacing bureaucratic complexity; **efficient implementation** (claimed −30% design time, −45% development time); **accessibility as opportunity**, explicitly beyond legal compliance and framed around situational limits (poor light, fatigue, mobile use); **diffusion of design culture**; **open-source sustainability**.

Four institutional **models** (last updated 11 March 2025): **Comuni** (1 architecture document, 90 HTML templates, 2 CMS themes, 21 prototypes), **Scuole** (28 templates, 1 WordPress theme, 18 prototypes), **ASL/healthcare** (1 component library, 15 page layouts, 7 prototypes), **Musei Civici** (30 page layouts, 9 prototypes). Each model leads with an **information-architecture document** before any visual work. The transferable move is not the templates — it is that an institution's site is designed *as an architecture of content types* (service, event, document, person, place, news) and only then styled.

---

## 3. Europa Component Library (ECL) and the Europa Web Guide

### 3.1 Structure

ECL ships **two systems**: **EC** (European Commission, `ec.europa.eu`) and **EU** (European Union, `europa.eu`). *"The name Europa Family covers all digital content managed by the European Commission."* Documentation is organised as **Guidelines** (typography, colours, use of images, iconography, logos, spacing), **Components**, **Utilities** (including layout/grid and stacks), **Resources**.

### 3.2 Typography (EU system)

Family: **Arial, sans-serif**. *"Arial is the standard typeface for the websites under the Europa.eu domain."* — a deliberately unremarkable, universally available face; the credibility comes from structure, not from a bought typeface.

| Level | Mobile | Desktop |
|---|---|---|
| H1 | 36px / 44px | **42px / 52px** |
| H2 | 32px / 40px | **36px / 44px** |
| H3 | 28px / 32px | **32px / 40px** |
| H4 | 24px / 28px | 28px / 32px |
| H5 | 20px / 28px | 20px / 28px |
| H6 | 16px / 24px | 16px / 24px |
| Lead | 20px / 28px | |
| Body M | 16px / 24px | |
| Body S | 14px / 18px | |
| Body XS | 12px / 18px | |

All headings at **weight 400 Regular** — hierarchy is carried by *size*, not by bold. Base body **16px**. Body line-height ratio **1:1.5**; heading ratio **1:1.2**. All line-heights **divisible by 4**. Measure: **no more than 80 characters including spaces on desktop**, **40–60 on mobile**.

**Desktop H2 36px against 16px body = 2.25×, at weight 400.** This is the calmest possible way to get authority: big, light, wide-spaced headings over ordinary body text.

### 3.3 Grid and spacing

Grid: **12 columns**. Breakpoints: xs ≥ 0, **s ≥ 480**, **m ≥ 768**, **l ≥ 996**, **xl ≥ 1140**. Container is fluid (100%) up to Large and capped at **1368px** at Extra Large. Gutters expressed in rem; exact values not published on the usage page **[UNVERIFIED]**.

Spacing tokens (rem): `2xs` 0.25 (4px), `xs` 0.5 (8), `s` 0.75 (12), `m` 1 (16), `l` 1.5 (24), `xl` 2 (32), `2xl` 2.5 (40), `3xl` 3 (48), `4xl` 4 (64). Values are **fixed, not responsive**. Rules: apply spacing to create hierarchy and grouping; **do not stack spacing values**; **avoid custom spacing outside the scale**.

Again: **1368px**. Both benchmark systems let an institutional page breathe to ~1320–1370px at large viewports.

### 3.4 Colour

Primary `#0E47CB` (`--ecl-color-primary-100`) across an 11-step ramp (`primary-180` … `primary-5` = `#F3F6FC`). Secondary: a 9-step yellow/gold ramp (`secondary-80` `#FFD633`). Neutrals: `dark-100` `#262B38` through `dark-5` `#F4F5F5`. Semantic: info `#0E47CB` (bg `#F3F6FC`), **success `#00A174`** (bg `#F2FCF9`), **warning `#FF8133`** (bg `#FFF7F2`), **error `#D7003D`** (bg `#FEF2F5`).

The structural lesson: **every semantic colour is a pair — a foreground and a 5% tinted background** — so a notice never needs a shadow or a heavy border to read as a notice. Our `tokens.css:47–68` already does exactly this (`--color-*-fg` / `-bg` / `-border`); the benchmark confirms the approach.

### 3.5 Component usage rules — the quotable ones

**Cards.** Use *"to help visitors scan content / browse for information (as opposed to searching)"* and *"to group heterogeneous types of content"*. Avoid *"on small screen display — using too many cards can force users to scroll down extensively"*. Do: *"display only the most relevant information on each card: card with a thumbnail, title, description"*; *"keep to a minimum the number of links on a card, they act as teasers so just one in direct relation to a page is most often expected"*; *"limit the amount of cards to small groups of items"*; **"limit to 3-4 cards within a row"**. Don't: **"don't overuse cards"**; *"don't display too many links on a card, the main and ideally only action on a card should remain to navigate to the content it represents."*

**Content item — the alternative to the card, and the component we are most obviously missing.** *"The Content item component provides a quick overview of the content, to help users evaluate linked pages before committing to navigation."* It composes labels, primary metadata, an optional thumbnail, a paragraph, secondary metadata with icons, and **description lists**. Use it *"when you need a teaser that links to a page of interest"* or *"as part of a list"*. Do **not** use it when *"navigation structure or hierarchy … is the primary need"* (use a Navigation list) or for *"a single, high-priority content item requiring emphasis"* (use Featured item or Banner). This is precisely the ECL answer to "a collection of cards": a dense, bordered-by-rule, metadata-bearing row in a list — not a box.

**Breadcrumb.** Use *"in a large, multi-level information architecture where users may enter deep pages through search or external links"*, *"on pages that are 2nd or lower in the site hierarchy"*. **Do not use** *"if there is no clearly defined site hierarchy (i.e. hub-and-spoke model)"* or *"if your website's navigational structure is less than 3 levels deep"*. **"Always present the current page, without a link, as the final item."** On mobile it collapses to *"indicates and offers navigation to the parent page"* only. Placement must be consistent; labels concise and matching page titles; *"avoid verbose labels that create visual clutter or wrap across multiple lines."*

**Notifications.** Four variants, each with a *trigger condition*, not a mood: **Information** — *"when something has changed in the system that the user needs to be aware of"*; **Success** — *"when a user-initiated action has completed successfully and confirmation helps user confidence"*; **Warning** — *"when a user is about to take an action with potentially significant consequences, such as overwriting or deleting data"*; **Error** — *"when an action has failed and the user needs to understand why and how to recover"*. Purpose: *"to help users understand what has happened, what might go wrong, or what they need to do next"*. Rules: keep messages brief and contextual; *"use notifications sparingly so that each one retains its signal value"*; do not use them for non-critical content that does not affect task completion. Page-level vs inline distinction, dismissibility and `aria-live` are not covered on the usage page **[UNVERIFIED]**.

**Tables.** Use *"when presenting structured, static data"* and *"when users need to compare values across multiple items or dimensions, such as statistics, specifications, or dates"*. Zebra variant *"when the table contains many rows and users are likely to scan horizontally"*. Multi-header *"when your data has a hierarchical structure that cannot be expressed with a single row of column headers"*. Sort variant *"when users need to reorder rows by a particular column"*. Content rules: *"always align content from left to right within cells, following reading direction conventions"* — note *reading direction*, which is the RTL-correct formulation; *"use numerals, not words in data cells as users can scan and compare more quickly"*; *"use a dash ("-") to represent null or missing data in cells, rather than leaving them empty"*; *"do not use colour as the sole means of conveying information; always provide a text-based equivalent."*

**Site header.** Contains EC identity (logo), site name, main menu, and optionally login, language switcher, search. For **standardised** sites, logo + site name + language switcher + search form are **mandatory**; for **harmonised** sites only logo + site name are mandatory, with language support *"if your website supports multilingual content"*. The language component sits **to the left of the search form**.

**Page header.** Sits *"always … just below the Site header"* and composes: optional **Expandable** ("container for important announcements"), **Breadcrumb** (*mandatory, except homepage*), **Page title** (*mandatory, except homepage*), optional thumbnail, optional **Introduction** (*"a description of the content that the page addresses"*), optional **Meta** (*"primary metadata related to the page's content"*). *"The Page header elements are optional — depending on the page, rather than the site/template type."* Positive and negative versions exist; standardised and harmonised sites **must use the positive version only**.

That last sentence is the institutional discipline in one line: the dark/inverted treatment exists, and the rule is that ordinary pages do not get to use it.

### 3.6 Europa Web Guide

The **official rulebook** for the Commission's web presence, covering *"editorial, legal, technical, visual and contractual aspects"*. Chapters: (1) Governance of the Europa domain — including the inter-institutional EU website and the Commission websites; (2) Planning your web presence — define and plan, user research, **architecture and navigation**; (3) Design, content and development — design, **accessibility**, content, **privacy, security and legal notices**, development platforms/tools/IT standards, optimise, maintain; (4) Test, monitor, measure and report; (5) Additional resources — including **European Commission visual identity**. Last-update date not stated on the landing page **[UNVERIFIED]**.

Branding rule: sites are **EU-branded or EC-branded depending on communication need and audience** — EC branding for Commission activities, EU branding for content beyond a single institution. Domain rule: *"host all Commission-owned websites in the europa.eu domain … The use of the Europa web domain helps users to understand that they are visiting an authentic EU website."*

**The domain is the authenticity signal.** Not the blue, not the emblem, not the type. A design that tries to borrow authenticity from visual cues while sitting on a non-institutional domain is doing the one thing these guides are structured to prevent.

---

## 4. AGID — Linee guida di design

Legal basis: **mandatory technical rules under art. 53, comma 1-ter of the CAD** (Codice dell'Amministrazione Digitale), adopted by **determinazione n. 224/2022**, applying to *"all deliveries of websites and digital services for Public Administration"*. Eight requirement areas: **4.1 Accessibilità · 4.2 Affidabilità, trasparenza e sicurezza · 4.3 Semplicità e user experience · 4.4 Monitoraggio dei servizi · 4.5 Interfaccia utente · 4.6 Integrazione piattaforme abilitanti · 4.7 Licenze · 4.8 Attuazione.**

The older "Linee guida di design" chapter 6 (User interface) on docs.italia.it carries a banner saying it is superseded; it describes the UI Kit as *"una libreria di elementi già pronti che possono essere assemblati per montare un'interfaccia utente adatta a servizi della PA"* and notes that because the approach is open source, *"le Pubbliche Amministrazioni, le agenzie e singoli cittadini possono contribuire alla discussione e alla modifica dello UI Kit stesso"*. I could **not** retrieve verbatim DEVE/DOVREBBE/PUÒ clauses on institutional identity, emblem, or the "sito ufficiale" marking from the current binding text **[UNVERIFIED — see §7]**.

What is clear and sufficient for our purposes: **4.6 Integrazione piattaforme abilitanti** (SPID/CIE/pagoPA/AppIO) and **4.2 Trasparenza** (Amministrazione trasparente) are obligations that attach to being a public administration. Any visual cue that implies we carry them is a misrepresentation.

**Licences** (relevant to what we may legally reuse): Bootstrap Italia is **BSD-3-Clause**; design tokens ship as CSS and SCSS from `italia/design-tokens-italia`; UI Kit Italia is distributed via the Figma community and GitHub. Titillium Web and Lora are open-licence faces. **Permissive licensing is not permission to look like a government.** The constraint here is trademark, identity and consumer-confusion law, not software licence.

---

## 5. Accessibility baseline — the 2026 position

This is where the research produced the most time-sensitive finding, and it changes what "compliant" means for this project.

**EN 301 549 v4.1.1 was published in September 2026.** It:
- adopts **WCAG 2.2** as the benchmark for websites, software and digital documents, replacing WCAG 2.1;
- adds **six new requirements** drawn from WCAG 2.2;
- **removes** the obsolete **4.1.1 Parsing** criterion;
- requires sites and documents to **better respect users' accessibility preferences**;
- is the **first version developed specifically with the European Accessibility Act in mind**, and adds **a new annex mapping its requirements directly onto the EAA**.

**But:** *"The new version is not yet the legal reference standard… Until the European Commission formally cites EN 301 549 v4.1.1 in the Official Journal of the European Union, the current reference remains EN 301 549 v3.2.1 (2021), which is based on WCAG 2.1 Level AA."*

**European Accessibility Act:** enforceable since **June 2025**, extending accessibility obligations from the public sector to private companies offering products and services to EU consumers. Microenterprise relief applies (fewer than 10 employees **and** turnover/balance sheet under €2m) — precise applicability to an APS promoting a non-commercial information service is a legal question, not a design one **[UNVERIFIED — flag to counsel]**.

**Italy:** **D.lgs. 82/2022** extended the **Legge Stanca** (2004) to require conformity with EN 301 549 for private businesses in which public entities hold a majority stake, private providers acting on behalf of a public body, and **companies with average annual revenue above €500 million**.

**Operative conclusion for Italy Legal Entry.** Build to **WCAG 2.2 AA / EN 301 549 v4.1.1** now. Legally the floor today is v3.2.1 / WCAG 2.1 AA, but v4.1.1 is published, its citation is a formality of timing, and a project whose whole claim is institutional seriousness should not be shipping to a superseded standard in front of ministries. The six added 2.2 criteria are exactly the ones a legal-tech form flow will trip over — **2.4.11 Focus Not Obscured**, **2.5.7 Dragging Movements**, **2.5.8 Target Size (Minimum) 24×24**, **3.2.6 Consistent Help**, **3.3.7 Redundant Entry**, **3.3.8 Accessible Authentication**. `--control-height: 2.75rem` at `tokens.css:205` already exceeds 2.5.8; **3.3.7 Redundant Entry** and **3.3.8 Accessible Authentication** are the ones the orientation questionnaire and signup flow need to be audited against, and **3.2.6 Consistent Help** argues for a persistent, identically-placed contact/help affordance across the whole site.

---

## 6. What we must NOT take — the impersonation exclusion list

AGAMI is an **APS** — a private association. Italy Legal Entry is an information and orientation ecosystem. It does not issue visas, permits or authorisations, and it says so on its own home page ("Ce qu'elle ne fait pas"). Every item below would contradict that statement visually.

**Hard exclusions — do not use under any circumstance.**

1. **The .italia header lockup.** The three-band slim/central/nav header with "ente di appartenenza" pointing at a parent public body, and the "Sito ufficiale" convention that goes with it. Our utility bar may carry AGAMI as *promoter*, which it does, but it must never be shaped like the PA "ente di appartenenza" pattern.
2. **Blu Italia `#0066cc`** and its ramp. The system itself says this colour *is* the PA identity at national scale. Keep `#0f2b52` and stay far from `#0066cc` in hue and saturation.
3. **Titillium Web.** In Italy this face reads as "government website" the way Transport reads as "British road sign". Our IBM Plex Serif/Sans pairing is the right instinct and should be protected.
4. **The emblem of the Italian Republic, the Republic's stemma, regional coats of arms**, and any Ministry, Region, Comune or Chamber of Commerce logo, until and unless each is covered by a signed written authorisation. The home page already states partners appear "uniquement avec leur accord écrit" — the design must make that impossible to violate by accident.
5. **ECL/EC branding**: the European Commission logo, the ECL site-header lockup, the `ecl-` class surface, ECL's `#0E47CB` primary and `#FFD633` secondary as a pair.
6. **The EU emblem.** Under the administrative agreement published in the OJEU on **8 September 2012 (2012/C 271/04)**, any natural or legal person may use it *subject to conditions*, and prior written permission is not required if those conditions are met. The two disqualifying conditions apply squarely to us: use must not create *"the incorrect impression or assumption that there is a connection between the user and any of the institutions, bodies, offices, agencies and organs of the European Union or the Council of Europe"*, nor *"lead the public to believe erroneously that the user benefits from the support, sponsorship, approval or consent"* of them. The user *"may do so on its own legal responsibility"* and is liable for abusive use. A bilateral Veneto–Morocco mobility project is precisely the context where a twelve-star circle would be read as EU endorsement. **Do not use the EU emblem.** If EU co-funding ever exists, the emblem then comes with a mandated, separate attribution formula.
7. **`.gov.it` / `europa.eu` visual cues** — the "authentic site" domain signal. We are not on those domains and must not simulate the chrome that implies them.
8. **SPID / CIE / pagoPA / AppIO buttons or lookalikes.** These are the *piattaforme abilitanti* of AGID requirement 4.6. Our login is an ordinary account login and must look like one.
9. **"Amministrazione trasparente" section furniture.** A transparency section styled like the statutory one implies a statutory obligation we do not carry.
10. **The word "ufficiale" / "officiel" / "رسمي" applied to the site itself**, anywhere in the chrome.

**Soft exclusions — legal but strategically wrong.**

11. **Bootstrap Italia as a stylesheet.** BSD-3 permits it; adopting it delivers a site that looks like a Comune. It also reintroduces exactly the Bootstrap look the client rejected. Take the *tokens' reasoning*, not the CSS.
12. **The .italia illustration style** (the Designers Italia / IT-app illustration family) — strongly associated with PA services.
13. **ECL's Arial.** Correct for Europa because Europa needs to be unremarkable and universally installed. We are trying to be distinctive; Arial gives us neither institution nor distinction.

**The line to hold, stated once:** we borrow **structure, density, taxonomy and restraint**. We borrow **nothing that identifies**.

---

## 7. What this benchmark says about the current build

Grounded in the before screenshots and the source, and limited to what the benchmark sources make judgeable.

**7.1 The type scale is compressed exactly where hierarchy is made.** From `tokens.css:110–116`, computed at a 1440px viewport: H2 = `1.3rem + 0.9vw` = **33.8px**; lead = capped at **21px**; H3 = capped at **24px**; body = 16px. That gives **H2 : lead = 1.61**, and **H3 : lead = 1.14**. Benchmark: .italia H2 tops out at **40px** over a 16–18px body (≥ 2.2×); ECL desktop H2 is **36px** over 16px (**2.25×**) at weight 400. Our H2 cap of 34px is below both, and it is not reached until a 1467px viewport — so at 1280 and 1440, the two most common desktop widths in the capture set, H2 renders at 32.3px and 33.8px against a 21px lead. In `home__1440x900__fr.png` the consequence is visible: the H2s of "Quatre accès à l'écosystème", "Comment fonctionne l'orientation", "Les parcours réguliers", "Ce que fait la plateforme, et ce qu'elle ne fait pas" and "Un écosystème institutionnel" all sit at the same weight and nearly the same optical size as the leads beneath them. Nothing dominates, so the page reads as five equal-rank blocks. The fix the benchmark suggests is not "bigger everything" — it is **widen the steps** (a real 2.2×+ H2:body ratio) and **drop the weight** (ECL runs every heading at 400 and gets authority from size and space alone).

**7.2 One container width, used 90 times.** `layout.css:6–23` defines four containers — `--container-max` 1200, `--container-wide` 1360, `--container-narrow` 736, `--container-prose` 832 (`tokens.css:198–201`). Across `templates/`, the base `.container` appears **90 times** (65 as `container ` + 25 as `"container"`), against **1** use of `container--wide`, **1** of `container--prose` and **0** of `container--narrow`. That is the client's "identical container width for every section", demonstrable in code. Benchmark: .italia changes container at every breakpoint and reaches **1320px** at XXL; ECL is fluid to Large then caps at **1368px**. In `institutions__1920x1080__fr.png` the entire page — utility bar, nav, breadcrumb, side nav, photograph, content, footer — renders inside a single ~1136px block (1200 minus 2×32px gutter), leaving ~390px of empty ground each side at 1920. A 1920 institutional page should not look like a 1280 page with margins. The `--container-wide` token already exists; nothing uses it.

**7.3 The dashboard is the banned "empty KPI widgets" pattern, five times over.** `portal-dashboard__1440x900__fr.png`: "Mon orientation", "Mes documents", "Mes échéances", "Communications" each render as an identically sized dashed-border box with a centred bronze icon, a centred title, a centred two-line sentence, and an arrow link below. "Mes demandes" is the only panel with content, and it is the only one that reads as an interface. Against the ECL card rules this fails on *"don't overuse cards"* and on the .italia rule that a card must carry **unique** content; against .italia's card rule it fails hardest on *"do not use a card simply to put a border around any kind of content"* — a dashed rectangle around a sentence is exactly that. The benchmark alternatives are named and published: an **ECL Content item** row inside a list, or a **.italia List** with metadata, or a **Callout/Nota** when the message is genuinely "nothing here yet, here is what will appear". Five empty states do not need five boxes; they need one list with five rows and a rule between them.

**7.4 The home "Quatre accès" block is the banned card grid, and the benchmark has a directly applicable rule.** `home__1440x900__fr.png`: four equal columns, each with `01`/`02`/`03`/`04`, a line-drawing icon, a title, two lines of description and a link. ECL's card rule allows *"3-4 cards within a row"*, so the count is fine — but its condition is that cards group *"heterogeneous types of content"* to help people **scan or browse**. These four are homogeneous by construction (they are the four audience spaces, i.e. the site's primary navigation), which is precisely the case where ECL says to use a **Navigation list** rather than a content component: *"avoid if navigation structure or hierarchy … is the primary need."* The four entrances are the information architecture; presenting them as four decorated boxes flattens the site's structure into a brochure row.

**7.5 The one place the build is already benchmark-correct, and should be extended rather than replaced.** `institutions__1920x1080__fr.png` shows a **2/3 + 1/3 layout with a left side navigation** ("Les espaces de l'écosystème" with Entreprises / Institutions / Destinataires / Proposer une collaboration / Universités et formation / Projet pilote, current item marked by a bronze rule), a real **breadcrumb** (`Accueil ›  Espace Institutions`) with the current page unlinked — matching ECL's *"always present the current page, without a link, as the final item"* — a **large photographic moment**, and a **two-column indexed list** of destinataires that uses hairline rules instead of boxes. That page is closer to the target than anything else in the set. The "Destinataires" list does repeat one identical `🏛` icon six times, which fails the .italia iconography rule (an icon must symbolise a function or categorise a content *type*; six identical icons categorise nothing). Remove the icon and that block is correct.

**7.6 The Arabic build has untranslated French text inside RTL pages — this is a credibility defect, not a nicety.** `home__1920x1080__ar.png`: the hero renders an Arabic H1 and Arabic subtitle, then an **LTR French paragraph** ("Orientation vers des parcours de formation et de mobilité régulière, construits avec les acteurs compétents") directly beneath it; the "ما تقوم به المنصة" column contains two **French** bullet items beside a fully Arabic "ما لا تقوم به" column; the forum band quote is French. Whatever the cause — the hero template at `templates/pages/home/_hero.html:20` marks `hero__body` as a Phase 1 prescribed `home-hero__fragment` with its own `lang` attribute, so this may be deliberate locked-registry behaviour — the rendered effect in front of a Moroccan institutional reader is a half-translated site. The benchmark position is unambiguous: the .italia language selector *"modifica la lingua di tutti i contenuti del sito"* — **all** of the site's content. If a prescribed fragment genuinely cannot be translated in Phase 1, it needs a visible editorial treatment (a marked quotation with a source, in the .italia *Nota* callout idiom) rather than appearing as body copy in the wrong language and direction.

**7.7 Radii and shadows are already right; do not let the redesign undo them.** `tokens.css:163–167` gives radii of 0 / 2 / 3 / 4px plus a pill, and `:169–173` gives four restrained cool shadows. Against .italia's *"gli angoli squadrati si addicono maggiormente a elementi che richiedono una presentazione più formale e strutturata"* and its "use shadows sparingly, one consistent direction", this is correct and is one of the few places where the current system is already more institutional than generic. The client's "huge border-radius everywhere" complaint does not apply to the tokens; it applies to the *quantity of bordered boxes*, which is a different problem with a different fix.

---

## 8. Transferable rules — what to actually adopt

Synthesised from §2–§5, in the categories briefed, with the source that justifies each.

**Grid and layout.** Adopt a **stepped container** rather than one width: fluid below ~768, then a ladder to **~1320–1360px** at ≥1600 (.italia XXL 1320; ECL XL 1368). Use the existing `--container-wide` for full-width editorial bands and `--container-prose` (832) for long-form legal and glossary text, where the .italia 75-character / ECL 80-character measure rules bite. Adopt **12 columns** with **24px gutters ≥768px** and the **2/3 + 1/3** layout as the default for any page that has a side navigation — the `institutions` page already proves it works here. Let content determine the column count (*"È buona prassi che sia il contenuto a determinare il numero di colonne"*), which is the formal licence for the asymmetric, non-uniform composition the client is asking for.

**Type scale and families.** Keep IBM Plex Serif / Sans / Sans Arabic — it is the single strongest non-imitative identity decision in the build. But **widen the ladder**: target H2 ≥ 2.2× body at desktop (38–40px against 16–17px), give H3 a real gap over lead (28px vs 21px, not 24 vs 21), and consider ECL's discipline of **regular weight for every heading**, letting size and space carry rank. Keep all line-heights on the **4px baseline** and all values divisible by 4. Enforce **max four heading levels per page** (.italia). Enforce measure: **68ch** is already set at `tokens.css:139` and is right; add it to lead and to table cell text.

**Colour semantics.** Keep the foreground/background/border triplet per semantic state — both benchmarks do this and it removes the need for shadows on notices. Adopt ECL's discipline of a **~5% tinted background** per state. Keep the bronze accent for rules, numbering and marks only, as `tokens.css:31` already documents. Never let a state be signalled by colour alone (.italia, WCAG 1.4.1; ECL tables: *"always provide a text-based equivalent"*).

**Utility bar and language selector.** Keep the three-part utility bar, but make its content read as *association*, not *administration*: promoter attribution, reserved-area access, language. Follow both systems in placing the language switcher **in the top utility band**, and .italia's requirement that it switch **all** site content (see §7.6). Follow ECL in keeping it adjacent to, and left of, search.

**Breadcrumb.** Keep it, apply ECL's conditions: present on every page **2nd level or lower**, absent on the home page, **current page unlinked and last**, consistent position, concise labels matching page titles, and collapsing to the parent link on mobile. Drop it anywhere the hierarchy is genuinely hub-and-spoke rather than faking depth.

**Service navigation.** Replace the home "Quatre accès" card row with a **navigation structure** — .italia's *List* with arrows and metadata, or an indexed typographic block — and let the side navigation (already correct on `institutions`) be the consistent mechanism for moving inside a space. Adopt the .italia models' lesson: define the **content types** first (service, procedure, document, notice, event, partner, glossary term, news item, person) and give each its own component, instead of rendering everything through one card.

**Form patterns.** Adopt .italia's error contract literally: on submission failure, show **an overall alert summary and per-field inline validity cues**, with error microcopy that lets people *"risolvere in autonomia"*. Put instructions **between fields**, not in placeholders. Use the **Stepper** for the orientation questionnaire — but check it against .italia's disqualifiers first: if question count varies with answers, or order is not fixed, a stepper is the wrong component and a progress indicator is the right one.

**Notice / alert taxonomy.** Adopt a **two-axis** taxonomy, which is what the two systems have between them. Axis 1, ECL's **trigger-based** states: info (system changed), success (user action completed), warning (consequential action ahead), error (action failed + recovery). Axis 2, .italia's **editorial** callouts: *Nota*, *Importante*, *Approfondimento* — these are for standing content on long pages, placed *"at a strategic point … such as the beginning of a section"*, and they are the correct home for the legal disclaimers this project is full of ("pré-évaluation à caractère informatif", "ne se substitue jamais aux autorités compétentes", the anti-fraud warning). Today those live as small grey lines and low-contrast footnotes; as *Importante* callouts with a left rule and a real title they become an institutional signature rather than small print. Both axes obey *"use sparingly so that each one retains its signal value."*

**Card usage rules — the operative test.** A card is legitimate only if **all** of: it links to a detail page; its content is unique relative to its siblings; it groups **heterogeneous** content types; there are no more than 3–4 in a row; it carries essentially one link. A card is illegitimate if it is decoration, if it is a border around a sentence, if the set is homogeneous, or if the real need is navigation. When the test fails, the benchmark names the replacement: **Content item in a list**, **List with metadata**, **Table**, **Timeline**, **Callout**, **Navigation list**, **Featured item / Banner** for a single high-priority item. Apply this test to every card in the build; on the evidence of `portal-dashboard__1440x900__fr.png` and `home__1440x900__fr.png`, most will fail it.

**Tables and data.** Use tables wherever the portal currently uses boxes for comparable records (demandes, documents, échéances all qualify under ECL's *"compare values across multiple items or dimensions"*). Always column headers (.italia). Limit columns. Zebra only for long scanning tables. Sorting only where needed. **Dash for null, never an empty cell.** Align by **reading direction**, which resolves correctly under RTL. Use `--font-mono` for reference numbers and dates — .italia reserves Roboto Mono for exactly this, and it is a cheap, strong institutional signal.

**Accessibility baseline.** Target **WCAG 2.2 AA / EN 301 549 v4.1.1** (§5), with the six new 2.2 criteria treated as design requirements, not a test-phase checklist — in particular **3.2.6 Consistent Help** (one identically-placed help/contact affordance sitewide), **3.3.7 Redundant Entry** (the orientation questionnaire must not re-ask what it already knows) and **3.3.8 Accessible Authentication**. Contrast floors: 4.5:1 text, 3:1 large text and graphical elements. Icons always paired with a text label, or with the label available to assistive technology.

**Density and content width.** Both systems converge on a 16px base, a 4px baseline, 24px gutters, a measure around 75–80 characters, and a large-viewport container around 1320–1368px. Sections are separated by **wider** vertical space than the space **inside** them (.italia's explicit stack/inline/inset distinction). The way out of "section after section of the same thing" is not more decoration — it is varying **container width, column split, background band and component type** section by section, which both systems permit and our `--container-wide` / `--container-narrow` / `--container-prose` tokens already support and nothing uses.

---

## 9. What I could not verify

1. **ECL gutter values in rem** — the grid usage page states gutters are "expressed in rems" without publishing the numbers. Would need the SCSS source in `ec-europa/europa-component-library`.
2. **ECL outer margins per breakpoint** — not published on the grid usage page.
3. **.italia shadow token values** — the `ombre` foundation gives principles only and defers to the Bootstrap Italia implementation; no numeric elevation ladder at foundation level.
4. **.italia component-to-radius mapping** — the `bordi-e-raggi` page publishes three radius tokens but states no per-component mapping.
5. **AGID verbatim DEVE/DOVREBBE/PUÒ clauses on institutional identity**, the emblem, and any "sito ufficiale" marking — the current binding text on docs.italia.it did not yield these through the chapter index or the superseded §6.2 page; the older UI chapter carries a "these guidelines are outdated" notice. Would need the PDF at `agid.gov.it/sites/agid/files/2024-07/Linee_Guida_design_per_siti_internet_e_servizi_digitali_della_PA.pdf`.
6. **A formal statement on whether non-PA entities may adopt the .italia design system.** Neither `fondamenti/identita/` nor `come-iniziare/per-designer/` addresses private bodies, associations or suppliers. The system is consistently framed as "per la Pubblica Amministrazione". **Absence of a prohibition is not permission**, and §6 does not depend on one: the argument against adoption is impersonation risk, not licence.
7. **ECL notification page-level vs inline distinction, dismissibility, and `aria-live` requirements** — not on the usage page; would need the component's Accessibility tab.
8. **ECL logo usage restrictions** — the `guidelines/logo/` page serves assets (muted, standard positive/negative, condensed positive/negative, in 35 languages) but publishes no clear-space, minimum-size or third-party-use rules. The EU emblem rules in §6.6 come from the 2012 administrative agreement (OJEU 2012/C 271/04) and the Commission's "Use of the EU emblem in the context of EU programmes 2021-2027", not from ECL.
9. **Europa Web Guide last-update date** — not stated on the landing page.
10. **EAA applicability to AGAMI** — whether an APS promoting a free information and orientation service falls inside the EAA's scope, and whether the microenterprise exemption applies, is a legal determination. Design to WCAG 2.2 AA regardless; do not let the design brief be the place this question is answered.

---

**Sources**

- [Designers Italia — Versionamento](https://designers.italia.it/design-system/fondamenti/versionamento/)
- [Designers Italia — Fondamenti](https://designers.italia.it/design-system/fondamenti/) · [Griglia](https://designers.italia.it/design-system/fondamenti/griglia/) · [Tipografia](https://designers.italia.it/design-system/fondamenti/tipografia/) · [Colori](https://designers.italia.it/design-system/fondamenti/colori/) · [Spaziature](https://designers.italia.it/design-system/fondamenti/spaziature/) · [Bordi e raggi](https://designers.italia.it/design-system/fondamenti/bordi-e-raggi/) · [Ombre](https://designers.italia.it/design-system/fondamenti/ombre/) · [Icone](https://designers.italia.it/design-system/fondamenti/icone/) · [Identità](https://designers.italia.it/design-system/fondamenti/identita/) · [Princìpi e intenzioni](https://designers.italia.it/design-system/fondamenti/principi-e-intenzioni/)
- [Designers Italia — Componenti](https://designers.italia.it/design-system/componenti/) · [Card](https://designers.italia.it/design-system/componenti/card/) · [List](https://designers.italia.it/design-system/componenti/list/) · [Callout](https://designers.italia.it/design-system/componenti/callout/) · [Tables](https://designers.italia.it/design-system/componenti/tables/) · [Timeline](https://designers.italia.it/design-system/componenti/timeline/) · [Steppers](https://designers.italia.it/design-system/componenti/steppers/) · [Form](https://designers.italia.it/design-system/componenti/form/) · [Sections](https://designers.italia.it/design-system/componenti/sections/) · [Header](https://designers.italia.it/design-system/componenti/header/)
- [Designers Italia — Modelli](https://designers.italia.it/modelli/) · [Per designer](https://designers.italia.it/design-system/come-iniziare/per-designer/) · [Linee guida di design (normativa)](https://designers.italia.it/normativa/linee-guida-di-design/)
- [AGID — Linee guida di design per i servizi digitali della PA](https://www.agid.gov.it/it/design-servizi/linee-guida-design-servizi-digitali-pa) · [PDF (2024-07)](https://www.agid.gov.it/sites/agid/files/2024-07/Linee_Guida_design_per_siti_internet_e_servizi_digitali_della_PA.pdf) · [Manuale operativo di design §6.2](https://docs.italia.it/italia/designers-italia/design-linee-guida-docs/it/stabile/doc/user-interface/il-disegno-di-un-interfaccia-e-lo-ui-kit.html)
- [italia/bootstrap-italia (BSD-3-Clause)](https://github.com/italia/bootstrap-italia) · [italia/design-ui-kit](https://github.com/italia/design-ui-kit)
- [Europa Component Library](https://ec.europa.eu/component-library/) · [EU system](https://ec.europa.eu/component-library/eu/) · [Typography](https://ec.europa.eu/component-library/eu/guidelines/typography/) · [Colours](https://ec.europa.eu/component-library/eu/guidelines/colours/) · [Spacing](https://ec.europa.eu/component-library/eu/guidelines/spacing/) · [Grid](https://ec.europa.eu/component-library/eu/utilities/layout/grid/usage/) · [Card](https://ec.europa.eu/component-library/eu/components/card/usage/) · [Content item](https://ec.europa.eu/component-library/eu/components/content-item/usage/) · [Breadcrumb](https://ec.europa.eu/component-library/eu/components/navigation/breadcrumb/usage/) · [Notification](https://ec.europa.eu/component-library/eu/components/notification/usage/) · [Table](https://ec.europa.eu/component-library/eu/components/table/usage/) · [Site header](https://ec.europa.eu/component-library/eu/components/site-wide/site-header/usage/) · [Page header](https://ec.europa.eu/component-library/eu/components/site-wide/page-header/usage/) · [Releases](https://github.com/ec-europa/europa-component-library/releases)
- [Europa Web Guide](https://commission.europa.eu/resources-partners/europa-web-guide_en)
- [AccessibleEU — EN 301 549 v4.1.1 update, September 2026](https://accessible-eu-centre.ec.europa.eu/content-corner/news/european-accessibility-standard-en-301-549-has-been-updated-2026-09-07_en)
- [EU emblem — administrative agreement, OJEU 2012/C 271/04](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:42012Y0908(01)) · [Use of the EU emblem in EU programmes 2021-2027](https://commission.europa.eu/document/download/3192a0ef-6bda-4e1a-81ca-65ade2ffad73_en?filename=eu_emblem_rules.pdf)

---

# Benchmark research — European institutional & legal-tech digital products, 2024–2026

**Author:** council member `benchmark-portals`
**Date of capture:** 20 September 2026
**Scope:** external reference research only. No repository file was modified. Live measurement of our own build was read-only against `http://127.0.0.1:8770`.

---

## 0. Method, and what this report is worth

I did not write this from memory. I captured 35 public sites and 18 interior pages with headless Chromium at 1440×1000 (viewport shots at scroll 0 / 1250 / 2600), read the PNGs, and then ran a DOM measurement pass on seven of them to extract real computed values: font families, sizes, line-heights, weights, letter-spacing, border-radius, box-shadow, and the actual pixel widths and x-offsets of content columns. Everything numeric below is measured, not estimated.

Artefacts (all in my scratchpad, not the repo):

- `C:\Users\<user>\AppData\Local\Temp\claude\C--tmp-italylegalentry\2835bd7f-e7c1-4c7b-a100-aef407711009\scratchpad\council\benchmark-portals\shots\` — 35 homepages × 3 scroll positions
- `...\scratchpad\council\benchmark-portals\shots2\` — 18 interior pages × 2 scroll positions
- `...\scratchpad\council\benchmark-portals\measure_ext.py` — external measurement script
- `...\scratchpad\council\benchmark-portals\measure.py` — measurement of our own home page at 390 / 1440 / 1920

**Known limits.** Cookie walls obscured part of ECB, Freshfields, Ca' Foscari and Sciences Po. Three targets blocked automated access entirely (Lexology, Legifrance, the IOM Migration Data Portal); ICMPD served only a consent interstitial; Jus Mundi rendered blank without JS hydration. I have not reported anything I could not see. I did not fetch `legalitalentry.it`.

**Our own baseline, measured, so the comparisons below are anchored.** Home page at `/fr/`, three viewports:

| Property | 390 px | 1440 px | 1920 px |
|---|---|---|---|
| `.container` width | 390 (full bleed) | **1200** (x=120) | **1200** (x=360) |
| `h1.hero__title` | 32 / 36.8, w400, IBM Plex Serif | 48 / 55.2, w400 | 48 / 55.2, w400 |
| `h2.section__title` | 24.31 / 27.96, w500 | 33.76 / 38.82, w500 | **34 / 39.1, w500** |
| `h3` | 20 / 26, w500 | 24 / 31.2, w500 | 24 / 31.2, w500 |
| body | 16 px IBM Plex Sans | 16 px | 16 px |
| `.eyebrow` | 12 / 19.2, w600, ls 1.44 px, `#7A6124` | identical | identical |
| section padding-block | 48 px ×6 sections | 72 px ×6 sections | 80 px ×6 sections |
| measured H2 line width | 358 | 576 | **576** |
| sections with a background | 1 of 6 (`#F4F1EA`) | 1 of 6 | 1 of 6 |

Two facts fall straight out of that table and they frame everything in this report.

1. **The page stops responding to the viewport at 1200 px.** From 1440 to 1920 the viewport gains 480 px and the design spends 100 % of it on empty margin. The H2 measure is 576 px at both widths. Compare: OECD's home grid is 1248 px at 1440 and contains sub-columns of 608 / 821 / 928; Freshfields runs a 1392 px container at 1440 (96.7 % of viewport); IUAV runs 1300 (90 %). Nobody in the reference set freezes one width for the whole page.
2. **Six sections, six identical openings.** Six `.eyebrow` elements at exactly 12 px / w600 / 1.44 px tracking in the same gold, six `h2.section__title` at exactly 34 px / w500, six identical `padding-block`. The client's phrase "repetitive eyebrow + H2 + paragraph + 3 cards" is not an impression; it is a literal description of the computed styles. See `docs\qa\visual\before\home__1440x900__fr.png`.

---

## PART A — The reference set

### A1. National and regional public-service portals with an editorial voice

---

#### Rijksoverheid (Netherlands) — `https://www.rijksoverheid.nl/`

*Shots: `rijksoverheid__top.png`, `rijksoverheid__mid.png`. Measured.*

**What it does well.** It is the most disciplined institutional homepage in the set, and it contains almost no cards. It is dense, it is calm, and its authority is manufactured entirely by a single structural device plus a rigid link grammar.

**Mechanisms.**

- **The *Rijkslint* (state ribbon).** A narrow vertical navy bar carrying the state arms, hung from the top edge, centred, on a white field above the navy band. It is the only ornament on the page and it is the whole brand. It costs one `<div>`. It reads as constitutional because it is a *shape* the state owns, not a logo pasted into a header row.
- **Page title as a coloured band, not a hero.** Below the ribbon: a navy band, `h1` "Home" at **40 / 45, w600, white**, left at x=136, with the site search right-aligned in the same band. No image, no lead, no CTA pair. The band *is* the header.
- **The four-column topic index.** Eight entries laid out 4×2 at 222 px each. Each entry is: a chevron glyph, an `h3` at **24 / 31, weight 400, in link-blue `rgb(1,104,155)`**, and beneath it a single comma-separated run of child topics truncated with an ellipsis ("AOW, Bijstand, WW-uitkering, WOZ-waarde, Inkomstenbelasting, WIA…"). No card. No border. No icon. No shadow. The heading is set at *regular* weight because it is a link, and its colour carries its affordance.
- **Solid colour blocks where a card would be lazy.** "Actueel / Ministeries / Regering" are three flat navy rectangles, square corners, containing only a white title, one sentence, and "Lees verder ›". They are colour, not chrome.
- **Photo credit as a first-class element.** "Beeld: © ANP", "Beeld: © Ministerie van Algemene Zaken" printed under each image. Institutional honesty rendered as typography.

**Measured.** RijksSans throughout. Body 17.27 / 27.27 (ratio 1.58). Container 1168 at 1440. H2 32 / 37 w600–700 in `rgb(21,66,115)`. Radius 0 everywhere I sampled; `box-shadow: none`.

**Transferable to us: very high.** Our `Quatre accès à l'écosystème` (`home__1440x900__fr.png`, second section) is four bordered boxes each with a decorative line-icon, a number `01–04`, an `h3`, a sentence, and a caps CTA. The Rijksoverheid version of the same content is four links with a teaser string, no box, no icon, and it reads as *more* institutional, not less. Our `entrance__title` is already 24 px — the same size as Rijksoverheid's — so this is a subtraction, not a redesign.

---

#### service-public.fr / the DSFR (France) — `https://www.service-public.fr/`

*Shots: `service-public-fr__top.png`, `__mid.png`, `sp-fiche__mid.png`. Measured. DSFR tokens read from `https://raw.githubusercontent.com/betagouv/dsfr-design-md/main/DESIGN.md`.*

**What it does well.** It proves that a legally-consequential information service can be visually plain, typographically restrained, and still unmistakably itself. And it is the only reference in the set whose *content type* — official guidance on rights and procedures — matches ours exactly.

**Mechanisms.**

- **Corners are square by law.** The DSFR ships exactly three radius values: `none` (0 px, the default for every component), `sm` (4 px, used only on the top corners of the search input), and `pill` (9999 px, only tags/badges/toggles). There is no fundamentals-level radius scale at all. One documented shadow exists in the entire system (`fr-card--shadow`). No gradient tokens.
- **The callout with a keyline.** "Allô Service Public 3939" sits on a pale rose field with a **4 px solid red bar on the left edge only**. That bar is the whole component. It is how the French state says *this is important* without a badge, an icon, or a shadow.
- **Type before title, everywhere.** Every tile in "Fiches pratiques par thème" opens with a small grey category line ("Passeport", "Simulateur", "Démarche en ligne", "Vivre à l'étranger") above a bold Bleu France title. The taxonomy is visible on every item, so a wall of 12 tiles is scannable.
- **Sub-headings at body size.** Measured on the visa fiche: `h1` 40 / 48 w700; **`h2` 16 / 24 w700** — the same size as body text. Hierarchy below the page title is carried by weight and vertical space alone. This is a deliberate, confident refusal to inflate.
- **The sources block is structural.** Every fiche ends with three collapsed panels: *Textes de loi et références*, *Services en ligne et formulaires*, *Voir aussi*. The legal basis is not an afterthought link; it is a permanent, named region of the page.
- **Reading column is narrow by choice.** Content column measured at **800 px on a 1440 viewport (55 %)**, dominant repeated inner width 776.

**Measured.** Marianne. DSFR scale: h1 40/48, h2 32/40, h3 28/36, h4 24/32, h5 22/28, h6 20/28 desktop; body-md 16/24, body-lg 18/28, body-xl 20/32. Spacing unit `1v = 4px`. Button heights 32 / 40 / 48. Input height 40. Card padding 24 / 32 / 40. Bleu France `#000091`. Explicit prohibition: *"Never colour a title in Bleu France except via `text-title-blue-france`, reserved for explicit identity expressions."* And: *"The DSFR explicitly recommends not using Spectral as the primary face. It's an accent."*

**Transferable to us: very high, with one warning.** Two things to take: the left-keyline callout (it replaces our boxed notices), and the mandatory sources panel (it replaces the fact that our `Avertissement` currently lives only as a footer link). The warning: the DSFR's serif-as-accent rule is the *inverse* of our stack — we set every heading in IBM Plex Serif. That is a legitimate divergence, but it means we cannot borrow DSFR typography wholesale; we can only borrow its discipline.

---

#### GOV.UK — `https://www.gov.uk/`

*Shots: `govuk__top.png`, `govuk-guidance__mid.png`, `govuk-stepbystep__mid.png`. Measured. Pattern docs fetched.*

**What it does well.** The most extreme demonstration in existence that hierarchy is a *ratio*, not a decoration.

**Mechanisms.**

- **Type does the hero.** `h1` at **48 / 50, w700, white on `#1D70B8`**, left-aligned in a 630 px column with the entire right half of a 1440 viewport left empty. No image. No eyebrow. No secondary CTA. Below it a labelled search field. That is the whole hero.
- **A reading measure of 630 px on a 1440 viewport (44 %).** Body 19 / 25. Heading-to-body ratio **48 / 19 = 2.53**. Ours is 48 / 16 = 3.0 for H1 but **34 / 16 = 2.13** for H2 — and because our H2 is frozen at 34 px from 1400 px upward, our section headings get relatively *weaker* the wider the screen.
- **Step by step navigation.** Numbered circles on a vertical hairline; each step is a bold title with a `Show` disclosure that opens to real links; the step you are on takes a grey fill. GDS ran *"8 rounds of research with users, including those with disabilities and people with low digital literacy"* plus a Digital Accessibility Centre review, and publishes the known failures: users rarely engage with the pattern header, and moving between two step-by-steps frustrates them.
- **Inset text.** A 5 px grey left bar and nothing else marks a caution inside prose ("You must have a confirmed job offer before you apply for your visa").
- **Every page ends by asking.** "Is this page useful? / Yes / No / Report a problem with this page" in a bordered strip above a 10 px blue rule and the footer.
- **Line-heights are all multiples of 5 px** to hold a vertical rhythm.

**Transferable to us: high for process, medium for aesthetics.** Our `Comment fonctionne l'orientation` (`home__1440x900__fr.png`, third section) is a horizontal rail of four small numbered circles with four short labels — decoration that describes a process rather than being one. The GOV.UK pattern is vertical, expandable, and each step contains the actual links. That is the single highest-value structural swap available on the home page. What we should *not* take is GOV.UK's visual language wholesale: it is a state service and we must not read as one.

---

#### admin.ch — The Federal Council (Switzerland) — `https://www.admin.ch/gov/en/start.html`

*Shot: `admin-ch__top.png`.*

**What it does well.** Calm to the point of austerity, and it solves multilingualism with a sentence.

**Mechanisms.**

- **Four-language wordmark lock-up.** "Schweizerische Eidgenossenschaft / Confédération suisse / Confederazione Svizzera / Confederaziun svizra" stacked at ~8 px beside the shield, then a vertical rule, then the service name. The plurality of languages *is* the identity mark.
- **Three-tier header at decreasing darkness**: a dark slate utility strip ("Swiss federal authorities ⌄", "Subscribe to news", "EN ⌄"), a white brand row, a white section row. No sticky, no shadow, no mega-menu.
- **Asymmetric hero without a card.** Text left at 46 %, press photograph right at 45 %, a 9 % gutter, `h1` ~34 px, photo credited "© FCh" in 12 px grey beneath. The image is a real working photograph of the institution, not stock.
- **Language handled in prose:** *"On our English website, you will find a selection of information… For more details, please choose the German, French or Italian site."* Three inline links. It is honest about asymmetric coverage instead of pretending every language has every page.

**Transferable to us: high, and it is a direct indictment.** Our hero (`home__1440x900__fr.png`) has the same skeleton — text left, image right — but the image is a generic stock photograph of anonymous hands over a document, mounted in a decorative offset double-border frame with a drop shadow. The frame is what makes it read as a template. admin.ch proves the layout is fine; the picture and its frame are the problem. And the Swiss language sentence is exactly the pattern we need given that Allegato 1 IT is missing.

---

### A2. International organisations

---

#### OECD — `https://www.oecd.org/en.html`

*Shots: `oecd__top.png`, `__mid.png`, `oecd-pubs__mid.png`. Measured. Open-access relaunch confirmed July 2024.*

**What it does well.** It is the best answer in the set to "how do you open a homepage without a generic hero".

**Mechanisms.**

- **The butted two-tone hero.** A deep navy text panel (≈28 % of the viewport) is butted **flush** against a photograph (≈28 %) — one rectangle, no gutter, no radius, no shadow. Inside the navy: a small all-caps eyebrow ("EDUCATION: PISA 2025 RESULTS"), a white `h1`, a five-line standfirst, a link, and a footer line "Report • 8 September 2026". To its right, a third column, "Top stories", is a **list**: 80×62 thumbnail, "Press release" label, bold multi-line title, hairline separator. Three items. The hierarchy is hero-panel > list, not three equal cards.
- **Asymmetric section openings.** "About the OECD": heading at x=96 in a 395 px column, body text starting at x=520 in a separate column. The heading and its prose do not share a measure. This single move destroys the "eyebrow + H2 + paragraph, all left-aligned at the same x" rhythm that the client named.
- **Multiple container widths on one page.** Measured common widths at 1440: **1248** (48 occurrences), **608**, **821**, **928**, 763, 811. The page has a grid, not a container.
- **Data is the illustration.** A stacked horizontal bar chart of PISA results at 821 px beside a 395 px commentary column, with a source line, a caveat footnote and a definition footnote set at 12 px beneath it.
- **Publications as a horizontal rail of colour-coded tiles** — pale blue, apricot, white — each with a "Report" chip top-left and `date • pages` bottom-left. They overflow the viewport rather than being padded out to a 3-up grid.
- **Per-page language availability.** On the publications page: `Available in: [English] français` as a small inline control at the top of the page — not a global switcher in the header. It states which languages *this page* exists in.

**Measured.** Noto Sans / Noto Sans Display VF. `h1` 60 / 64.2 **w900**, ls −1.2 px. `h2` 28 / 36.12 **w800**, ls −0.84 px. Body 16 / 24 in `rgb(88,97,121)` — a blue-grey, never pure black. Radius 0 on sampled headings.

**Transferable to us: very high.** Three specific takes: (1) the butted colour-panel/photo hero; (2) the heading column offset from the body column; (3) the per-page language-availability line, which is the correct answer to our four-language reality and our missing Italian annex.

---

#### ILO — `https://www.ilo.org/`

*Shots: `ilo__top.png`, `ilo__low.png`.*

**What it does well.** Colour discipline at band scale. The page is a sequence of full-width fields, and the field colour tells you what kind of content you are in.

**Mechanisms.**

- **Alternating full-bleed bands.** ILO blue header → deep aubergine nav → photographic hero → white → pale blue (publications) → deep aubergine (priority programmes). Six bands, four colours, zero ambiguity about where a section starts.
- **Zero-radius tiles with a brand hairline.** Publication tiles are square-cornered aubergine blocks with a **3 px red rule along the bottom edge**. The red is used nowhere else on the block. One hairline carries the whole brand.
- **The artefact is the image.** Publications are shown as photographed report covers at an angle — not an icon, not a stock photo, the actual object.
- **Two-tier header** with the mission line ("Advancing social justice, promoting decent work") and the affiliation line ("ILO is a specialized agency of the United Nations") right-aligned in the top band, small, permanent.

**Transferable to us: high for banding, medium otherwise.** Our home page has **one** tinted band in six sections. ILO shows what controlled full-width bands actually buy you: a reader can tell at a glance how many kinds of thing are on the page. The affiliation line is also directly relevant — our header already carries "AGAMI — Dialogo Giuridico Interculturale APS — promoteur du projet", which is the right instinct, executed at too low a contrast to read (see `home__1440x900__fr.png`, top strip).

**What not to take:** the hero, which layers a diagonal white display type from an unrelated poster over a full-bleed astronaut photograph. It is noise.

---

#### ECB — `https://www.ecb.europa.eu/`

*Shots: `ecb__top.png`, `__mid.png`. Partly obscured by consent banner.*

**Mechanisms worth stealing.**

- **The yellow keyline.** Content panels carry a **4 px yellow bar on the left edge**. On a navy-and-white site, that one stripe is instantly recognisable as ECB. It is the cheapest identity device in the entire reference set.
- **The split panel.** A translucent white panel overlaid on a full-bleed photographic band, divided by a thin blue vertical rule into `eyebrow + headline` | `body paragraph`. Two columns inside one panel, separated by a hairline rather than by whitespace.
- **All-caps letterspaced institutional wordmark**: `EUROPEAN CENTRAL BANK | EUROSYSTEM`, with the pipe carrying the sub-brand.
- **Three-column text with one column tinted** to mark it as a different kind of item (a call for expression of interest, not an interview).

**Honest verdict: partial.** The ECB's identity system is excellent and its execution is dated — soft radial gradients behind the header, blurred photography, a hero that is 60 % out-of-focus banknotes. Take the keyline, the split panel and the hairline column rule. Take nothing else.

---

#### BIS — `https://www.bis.org/`

*Shots: `bis__top.png`, `__mid.png`. The site self-identifies as new ("Welcome to the new BIS website. Please share your feedback").*

**This is the most instructive entry in the report, because it is half of what we want and half of what the client rejected.**

**What is wrong with it** — and note these are, item for item, on the client's banned list: the hero is a **crimson-to-purple gradient band** carrying a **centred giant generic title** ("Welcome to the BIS") over a **generic subtitle** ("Promoting global monetary and financial stability through international cooperation"), followed immediately by **three identical cards**. A serious central-banking institution shipped this in 2026. It is proof that institutional seniority does not protect you from the generic.

**What is right with it** — the research index below the fold is excellent:

- Asymmetric **2 : 1** split (research feed 800 px, speeches rail 440 px).
- Every item opens with typed chips: `BIS Working Paper` + `No 1378`, with the date **right-aligned on the same baseline**.
- Author bylines are individually linked and underlined.
- Topic tags appear only where they exist — no empty slots.
- The speeches rail attaches a portrait, a name and a *role* ("Chair, Financial Stability Institute") to each item. Attribution is the design.

**Transferable to us: the index, yes; the homepage, as a cautionary tale.** Our `news-index__1280x800__fr.png` currently renders its category filter as an **unstyled `<ul>` with browser default bullets and blue underlined links**, above a dashed-border empty state with a centred icon. The BIS index is what that page should look like once there is content: typed chip, title, standfirst, byline, date, tags, hairline.

---

#### Council of Europe — `https://www.coe.int/`

*Shots: `coe__top.png`, `__mid.png`.*

Included for honesty, not admiration. The Council of Europe — the most obviously analogous body to our subject matter — runs a dated portal: default-blue underlined link titles, `FOCUS` badges floating above bordered image cards, a strip of six institutional logos at 40 px with 9 px all-caps captions, and a social share bar rendered as eight coloured brand squares at the top of the page. **Its only genuinely good feature is the orange progress hairline under the sticky header.**

**Value to us:** it defines the floor. If our site merely looks "institutional", we land here. The client is right that this is not good enough.

---

### A3. Universities and research institutions

---

#### Università Iuav di Venezia — `https://www.iuav.it/`

*Shots: `iuav__mid.png`, `iuav-interior__top.png`. Measured.*

**The single most valuable reference in this report.** It is in the Veneto, it is an institution, it is contemporary, it is distinctive, and it contains not one card, not one icon, not one shadow, and not one rounded corner.

**Mechanisms.**

- **The wordmark is a typographic construction.** `I / U / A / V` set vertically in a monospaced face with dashes between the letters, forming a small square block; beside it "Università Iuav di Venezia" in three lines; beside that, separated by a vertical rule, `I00` and `1926–2026` in a monospaced display face. Identity from type and rule, nothing drawn.
- **Asymmetric hero with a collage, not a photo.** Left third: a five-line paragraph and one square black button. Right two-thirds: overlapping duotone image blocks — mint, periwinkle, orange — with small white label chips ("Calendario del Centenario", "Mostre del Centenario", "Conferenze del Centenario") pinned on the seams where blocks overlap. The overlap *is* the composition.
- **A full-bleed black band for "In evidenza"** containing a three-part editorial split: image (50 %) | small label + large title (25 %) | body text (25 %), with a 1 px white rule across the top of the two text columns.
- **The interior index page is a masterclass.** Measured on `/ateneo`: `h1` **30 / 40 weight 400** and `h2` **30 / 40 weight 400** — *identical*. There is no size contrast and no weight contrast between the page title and the section titles. Hierarchy comes from (a) full-width 1 px hairlines between sections, (b) position, and (c) a right-aligned **grey ghost link** at the same 30 px size ("Leggi tutte le informazioni") sitting opposite each section heading across the full 1300 px measure. Sub-links are a hairline-separated list of `→ label` rows in a 650 px left column.
- **Container 1300 px on a 1440 viewport (90 %).** Body 16 / 25.

**Transferable to us: very high, and it should be the primary aesthetic reference for the public site.** Specifically: our `Les espaces de l'écosystème` on the project page (`project__1280x800__fr.png`) is currently four rows of `[gold icon] [blue link] [arrow]` — which is a generic list with decoration. IUAV's version of that same component is a heading, a paragraph, a hairline, and two arrow rows, with a ghost "read everything" link thrown to the opposite margin. It is more confident and it uses fewer elements.

**Caveat:** IUAV's palette (orange / mint / periwinkle on black and white) belongs to an architecture and design school. We take the *structure* — hairlines, right-thrown ghost links, one type size for all headings, overlapping image blocks — not the colours.

---

#### European University Institute — `https://www.eui.eu/`

*Shots: `eui__top.png`, `eui-law__mid.png`.*

**Mechanisms.**

- **The angled panel joint.** A full-bleed photograph of the Badia's cloister, with a content bar overlapping its lower edge; the bar is split into a **white half and a navy half joined by a diagonal cut**. White half: institution name + one-line mission + "About us →". Navy half: a search field prompted "Example: PhD in Economics" + "Explore our programmes". One shape carries both *who we are* and *what do you want*.
- **Two-tier nav with rule separators.** Row 1: brand + broad sections. Row 2: `Apply | Events | News | People | Research |🔍` as boxed cells divided by 1 px rules — a cell grid, not a row of links.
- **The footer disclaimer.** In small red text: *"The European Commission supports the EUI through the European Union budget. This website reflects the views only of the author(s), and the Commission cannot be held responsible for any use which may be made of the information contained therein."* Followed by the full legal address.

**Transferable to us: the disclaimer pattern is critical.** Our whole legal posture is "we inform and orient, we are not an authority, we grant nothing". The EUI shows the register: small, red, permanent, in the footer, phrased as a limitation of responsibility. Our equivalent currently hides behind a footer link labelled `Avertissement` and a "Lire l'avertissement →" link at the bottom of one home section. It should be *printed*, not linked.

---

#### Max Planck Society — `https://www.mpg.de/en`

*Shot: `mpg__top.png`.*

**One mechanism, and it is a good one: identity-derived geometry.** The MPG logo is a pennant — a rectangle with one corner cut. Their hero content panel repeats that shape: a translucent white panel over a satellite image, with the **bottom-right corner bevelled off**. A serif headline in Max Planck green sits inside it. The notch is not decoration; it is the logo's grammar applied at page scale.

Secondary: they use `› more` links rather than buttons for almost everything, which keeps the page quiet.

**Transferable to us: medium-high, conditionally.** If Italy Legal Entry has any geometric signature in its mark, repeating it as a panel shape is the cheapest route to "distinctive" that does not involve gradients, blobs or animation. If it does not, invent one deliberately (a single cut corner, a consistent 4 px keyline colour, a hairline rule weight) and then apply it *everywhere*.

---

#### Sciences Po, Ca' Foscari, Bocconi, Padova — brief verdicts

- **Sciences Po** (`sciencespo__top.png`): a fully committed red. All-caps red nav band, red bar-shaped CTAs, red brand. Distinctive purely by chromatic conviction. But the hero is a looping video with two centred red bars floating over it — the client would reject it.
- **Ca' Foscari Venezia** (`unive__mid.png`): a strong maroon (`≈#5F1330`) and — notably — a **light/dark theme toggle in the primary header**. Content is ordinary bordered cards with multi-line underlined links.
- **Università di Padova** (`unipd__mid.png`): a paginated grey carousel with prev/next pills and six dots. Ordinary.
- **Bocconi**: captured, unremarkable for our purposes.

---

### A4. Serious legal-tech and professional services

---

#### Freshfields — `https://www.freshfields.com/`

*Shots: `freshfields__top.png`, `__mid.png`. Measured. 2024 rebrand confirmed (name shortened, new wordmark, rollout from October 2024).*

**The best-designed law-sector site in the set, and the closest to what the client means by "authoritative, elegant, distinctive, contemporary, European".**

**Mechanisms.**

- **Two typefaces doing opposite jobs.** The wordmark is a heavy geometric grotesque, all-caps, black: `FRESHFIELDS`. Everything editorial is set in a custom transitional serif, `FreshfieldsHeadline`, at **weight 400** and enormous sizes: `h1` **80 / 88**, `h2` **64 / 64**, `h3` **40 / 40**. Body is `FreshfieldsText` at 17 px. Heading-to-body ratio **4.7 : 1**. The serif is never bolded; scale alone carries it.
- **A cream ground, not white.** The page sits on a warm off-white. It immediately stops reading as a default Tailwind page.
- **Commissioned illustration instead of stock photography.** Flat, saturated, hand-drawn scenes (a woman on a subway; a figure under an orange overpass) with a limited palette. This is the single most effective anti-generic move available and it requires no code at all — only an art budget and a decision.
- **Colour-field sections.** "At the forefront of law" set in the black serif on a full **periwinkle** field occupying two-thirds of the width, with an illustration occupying the remaining third.
- **Near-full-bleed container: 1392 px at 1440 (96.7 %).** The opposite of our 1200 px cap.

**Transferable to us: very high.** We already have a serif (IBM Plex Serif) and a warm tint (`#F4F1EA`, currently used on exactly one section). Freshfields shows what happens when you commit: serif at weight 400 at genuinely large sizes, warm ground on *most* of the page rather than one band, commissioned imagery. Our H1 is 48 px at weight 400 — the right idea at roughly 60 % of the conviction.

**What not to take:** the giant rounded container frame around the hero block.

---

#### Doctrine — `https://www.doctrine.fr/`

*Shot: `doctrine__top.png`.*

A French legal-research product, and the only legal-tech company in the set that does not look like a SaaS landing page.

**Mechanisms.**

- **A mixed-face headline in one block.** Line 1 in a bold sans: *"Tous vos besoins. Une IA juridique."* Lines 2–3 in a large serif at the same leading: *"Doctrine réconcilie la donnée juridique publique avec vos documents dans un espace de travail sécurisé."* Two voices — assertion, then explanation — inside one typographic object.
- **No hero image.** The headline sits on white, left-aligned, with the right 45 % empty. The first image on the page is a screenshot of the actual product, below the fold, showing a real three-pane workspace.
- **Honest microcopy under the CTA:** "7 jours d'essai gratuit · Sans carte bancaire · Sans engagement" at 13 px grey.

**Transferable to us: high, and cheap.** Mixing two faces in a single headline block is a real compositional device we can implement with our existing Plex Serif + Plex Sans pairing, and it would immediately differentiate our hero from a generic one.

---

#### Clifford Chance — `https://www.cliffordchance.com/`

*Shot: `cliffordchance__top.png`.* Included as a control. Full-bleed photographic carousel, white text overlay, violet pill button, five dots. It is the default. It is what the client means by "conventional".

---

### A5. Chambers of commerce, economic and bilateral cooperation bodies

---

#### GIZ — `https://www.giz.de/`

*Shots: `giz__top.png`, `thamm__top.png`.*

**Mechanisms.**

- **A monospaced/technical display face for headlines** ("International cooperation with impact", "Where we work") — set large over a full-bleed photograph. Unusual, immediately recognisable, and it does the entire job of making the brand distinctive.
- **A 24 px lead paragraph as the first element after the hero**, in a narrow measure, treated as a design element rather than filler.
- **Numbers with provenance.** On "Where we work": a white panel carrying `1,437 running projects` and `22B Total Volume in Euro` in a large light weight — immediately followed by *"Current data version as of December 31, 2025"*. This is how you show figures without producing a "startup counter": name the number, name its date, name its source.
- **A full-width dark band as a filter bar.** Region tabs (`All / Supraregional / Africa ⌄ / Asia ⌄ / Europe ⌄ / Latin America and the Caribbean ⌄`) rendered as a navigation band across the entire viewport, with the active item underlined in the accent colour.

**Transferable to us: the dated figure and the full-width filter band, definitely.** The full-bleed headline over a landscape photo is on the client's banned list and only survives here because the typeface is so unusual; do not reproduce it with a normal face.

---

#### Union for the Mediterranean — `https://ufmsecretariat.org/`

*Shot: `ufm__top.png`.*

**Two mechanisms.**

- **Trilingual header strip:** `English | Français | العربية` as three plain text links, top-left, with a rule between them. No flag icons, no dropdown, no `🌐`. This is the correct pattern for us.
- **The logo lock-up carries all three scripts** — the organisation's name set in Latin, French and Arabic in three stacked lines beside the mark.
- **Partner lock-up bar.** A white horizontal strip floated over the hero image carrying four institutional emblems: the EU flag, the UfM mark, the Hashemite arms, and the Italian MAECI mark with the tricolore. This is how a cooperation body shows who stands behind an event without claiming to *be* them.

**Transferable to us: high.** We are a bilateral Italy(Veneto)–Morocco initiative in fr/it/en/ar. The three-script wordmark and the plain-text language strip are both directly applicable. The partner bar is the correct pattern for the "Partenaires" content we currently reduce to a link.

---

#### Regione del Veneto — `https://www.regione.veneto.it/`

*Shot: `regione-veneto__top.png`.* Our territorial authority. A red band, a Bootstrap-style utility row of seven all-caps red links, and a 3-column news grid whose images are a mix of photography and JPEG event posters. **Relevance: it defines the reference frame of the officials who will judge us.** We must look demonstrably more considered than this, while being visibly *not* it — we are not a public authority and must not be mistaken for one.

*(Camera di Commercio Venezia Rovigo could not be captured: `ERR_CERT_COMMON_NAME_INVALID` on `www.dl.camcom.gov.it`.)*

---

### A6. Long-form legal reading and indexed reference content

---

#### EUR-Lex — `https://eur-lex.europa.eu/`

*Shot: `eurlex-doc__mid.png` (Regulation (EU) 2024/1348).*

**This is the aesthetic of legal credibility, and it is worth studying precisely because it is not "designed".**

**Mechanisms.**

- **A document-services rail, not a nav.** A 300 px left column: tabs `Text / Document information / Procedure / Document summary`; then a list of document actions each with its own small icon — *Up-to-date link, Permanent link, Download notice, Save to My items, Create an email alert, Create an RSS alert*; then two solid blue section bars, `Table of contents` and `Hide consolidated versions`.
- **A version timeline.** Under "consolidated versions": `27/02/2026` (blue link), `22/05/2024` (plain), and `Legal act` on a grey field with a **blue bar on its left edge marking the version currently displayed**. Three lines of type answer "which text am I reading, and is it current?"
- **The act itself is set as an official journal facsimile.** Centred masthead (`Official Journal of the European Union`, `EN`, `L series`), the act number left and the date right on one line, a centred three-deck title block, then justified body with numbered recitals `(1) (2) (3)` in hanging indent and superscript footnote references. Serif. Dense. Authoritative.

**Transferable to us: high, and underexploited.** We publish legal-adjacent reference content (glossary, textes de référence, avertissement, phase-dependent information). The version timeline answers a real problem we have — our footer says `v2.0.0 — Fase 1` and our whole product has a Phase 1 / Phase 3 split. That belongs in the content, dated, not in a footer version string.

---

#### Bruegel — `https://www.bruegel.org/`

*Shots: `bruegel__top.png`, `__mid.png`, `bruegel-index__mid.png`. Measured.*

**The best editorial index in the set, and the closest model for our news / forum / glossary pages.**

**Mechanisms.**

- **There is no card.** Measured: `border-radius: 0px`, `box-shadow: none` on every item sampled. An index entry is a vertical stack: image → **content-type label in dark red** (`Analysis`, `Policy Brief`, `Event`, `Newsletter`, `First Glance`, `Book`) → title → standfirst → authors → date → tags. That is all. No container, no border, no padding box.
- **Tags are square 1 px outlined rectangles**, small, with a literal `…` chip when there are more. Not pills.
- **A genuinely asymmetric grid.** Measured on `/publications` at 1440: the lead item is **552 px wide at x=152**; the three secondary items are **260 px at x=736 / x=1028**. One grid, two item widths, deliberately unequal. Content area 1136 px inside a 1200 container.
- **Body copy is a serif; UI is a grotesque.** Measured: standfirsts in `Officina Serif ITC` at **18 / 27**; headings in `Conduit ITC` at 22.68 / 29.26 w500; navigation in `aktiv-grotesk`. Three faces, three jobs, no ambiguity.
- **A black sticky bar** carrying the wordmark and the tagline "Improving economic policy". The tagline lives in the chrome, permanently.
- **Photographic band + floated white panel** for the flagship item, panel internally split title-column / body-column.

**Transferable to us: very high.** Every element of the Bruegel index item is content we already have or will have: type, title, standfirst, author, date, tags. Our `news-index` page currently has a bulleted `<ul>` and a dashed empty box. This is the target.

---

#### Aksel (NAV, Norway) — `https://aksel.nav.no/`

*Shot: `aksel-komponenter__top.png`. Typography spec fetched.*

**Mechanisms.** A persistent left rail with a search field at its head and grouped sections (`Grunnleggende / Byggeklosser / Mønster og Maler / Støtte`), disclosure chevrons, and a light/dark toggle in the header. A status pill (`Komponent` + "DataGrid er ute i preview! →") announces change inline.

**Measured spec.** Source Sans 3. Eight sizes only: 14, 16, 18, 20, 24, 28, 32, 40. **Base body size for digital products is 18 px.** Headings: XLarge 40/52 (ls −1 %), Large 32/40 (−0.8 %), Medium 24/32, Small 20/28, XSmall 18/24. Stated principle: *"optimal bredde på brødtekst … er mellom 50 og 75 tegn per linje"* — 50–75 characters per line, noted as particularly benefiting users with reading or concentration difficulties.

**Transferable to us: the left rail, directly, for the authenticated portal.** Our `portal-dashboard__1440x900__fr.png` already has a left rail, and it is the one genuinely good thing on that page. The Aksel version adds search-in-rail and grouped headings, which is what our rail needs as the portal grows past six items.

**Also relevant:** Designers Italia's PA design system, which we should know because our audience is Italian, mandates **max 75 characters per line**, a **4 px vertical rhythm baseline**, and **no more than four heading levels per page**; its scale is h1 40–48/48–56, h2 32–40/40–48, h3 28–32, h4 24–32, h5 20–24, h6 16–18, body 12–18/24, in Titillium Web with **Lora recommended for longer reading passages**.

---

## PART B — What NOT to do, and why

### B1. EURES, the EU's own labour-mobility portal — `https://eures.europa.eu/`

*Shot: `eures__top.png`.*

**This is our closest functional peer in Europe and it is a catalogue of the client's banned list.** In one viewport: a **blue-to-violet gradient band**; **gradient blobs** (a large lilac ellipse bleeding off the left edge); a **floating collage** of two photographs at an angle with a tilted purple frame; a **wavy white organic shape** cutting across the bottom right; a yellow pill CTA; **carousel pagination** (1 2 3 4) plus a pause button; and immediately below, **four identical outline-icon cards**. The typography is Arial-grade.

**Why it matters.** It is the strongest possible argument to our client that "EU institutional" is not automatically "credible-looking", and the strongest possible argument to our team that being functionally adjacent to EURES is not an excuse to look like it. If a visitor lands on Italy Legal Entry after EURES, the contrast is our entire opportunity.

### B2. Migration Partnership Facility (ICMPD / EU) — `https://www.migrationpartnershipfacility.eu/`

*Shot: `mpf__top.png`.*

Our nearest institutional twin: an EU-funded facility for migration and mobility partnerships between member states and third countries. It is **technically correct and aesthetically ordinary** — the exact phrase our client used about us. A grey band with a watermark world map; a **centred** two-line blue headline; a **centred** grey sub-paragraph; a Bootstrap nav with `⌄` carets; news items with 11 px calendar-icon dates; a yellow `Learn more...` button with a trailing ellipsis.

**The lesson:** nothing here is *wrong*. That is precisely the failure mode we are in. Correctness is the floor, not the goal.

### B3. Enabel (Belgian development agency) — `https://www.enabel.be/`

*Shot: `enabel__top.png`.*

A **centred giant serif mission statement** over a full-bleed aerial photograph of a container ship, with a circled `Scroll ↓` button in the bottom-right. A bilateral cooperation agency executing the single most banned pattern on the list. Note that it is a *good* photograph and an *elegant* typeface, and the result is still generic — because the composition is the cliché, not the assets.

### B4. Clio (legal-tech SaaS) — `https://www.clio.com/`

*Shot: `x-clio__mid.png`.*

Dark navy full-bleed band, huge light-weight sans display type, **fully rounded pill buttons**, a geolocation interstitial ("Hey there! It looks like you're in Belgium."), eyebrow-in-caps-over-headline, and a cookie bar. This is the register our client means by "generic SaaS website". Its presence in a legal category is exactly why our client is nervous: legal-tech has converged on this look, and converging with it would cost us credibility with ministries.

### B5. BIS's own 2026 homepage — see A4 above

Re-stated here because it is the most uncomfortable data point: a central-bank institution, relaunching in 2026, shipped a centred generic hero on a purple gradient followed by three identical cards. Institutional weight is not a defence. Only design decisions are.

---

## PART C — Six things every good example does, that we do not

1. **They vary the container.** OECD: 1248 / 928 / 821 / 608 on one page. GOV.UK: 960 page, 630 reading. service-public: 800 reading. Bruegel: 1136 with 552 and 260 items inside it. IUAV: 1300. Freshfields: 1392. **We use 1200 for all six home sections at every width ≥ 1200.**

2. **They vary the section.** Colour field, band, rule, offset, or full bleed — something changes between one section and the next. ILO alternates four band colours. IUAV drops to a full-black band. OECD offsets the heading column from the body column. **We have one tinted band in six sections and identical `padding-block` on all of them.**

3. **They make the taxonomy visible.** Bruegel's dark-red content-type label, service-public's grey category line, BIS's `BIS Working Paper / No 1378` chips, OECD's `Report` chip. The reader always knows what *kind* of object they are looking at before reading its title. **We have no content-type vocabulary anywhere in the public site.**

4. **They refuse the card by default.** Rijksoverheid's topic index, Bruegel's publication items, IUAV's section index, GOV.UK's "Popular on GOV.UK", MPG's `› more` links — all are link-lists with typographic structure and hairline separators. Cards appear only where an object genuinely has a boundary (a publication with a cover, a dated event). **We use a bordered-box card for four navigational links, two policy columns, five dashboard empty states, and one newsletter form.**

5. **They date and source everything.** GIZ prints "Current data version as of December 31, 2025" under its figures. EUR-Lex shows a version timeline. OECD prints `Report • 8 September 2026` inside the hero panel and `date • pages` on every publication tile. Rijksoverheid credits every photograph. service-public ends every page with its legal sources. **Our dates appear only as `20.09.2026` in the portal and `2 octobre 2026` in the forum banner; we have no source-of-record block on any public page.**

6. **They tell the truth about language coverage.** admin.ch names the other language sites in a sentence. OECD prints `Available in: English | français` per page. UfM runs a plain three-script strip. **Our Arabic home page at 1920 (`home__1920x1080__ar.png`) shows the hero standfirst and two bullets of the "ما تقوم به المنصة" list still in French — untranslated French leaking into an RTL page is a credibility failure that no amount of visual polish will cover.**

---

## PART D — Transferable mechanisms, ranked by impact for Italy Legal Entry

Ranked by *how much of the client's rejection each one answers*, with the evidence and the thing it replaces.

**1. Break the single container. Give each section a role-appropriate width.**
Evidence: OECD (1248 / 928 / 821 / 608), GOV.UK (960 / 630), service-public (800), Bruegel (1136 / 552 / 260), IUAV (1300), Freshfields (1392).
Replaces: one `--container-max: 75rem` applied to every section at every width above 1200 px.
Effort: low (CSS only). Impact: highest single item in this list — it is the mechanical cause of "identical container width for every section" and of the dead 480 px at 1920.

**2. Kill the navigational card. Replace with a typographic index.**
Evidence: Rijksoverheid topic grid (chevron + 24 px link-blue heading at weight 400 + truncated child-topic string); IUAV `/ateneo` (hairline + heading + paragraph + `→` rows + right-thrown ghost link); GOV.UK "Popular on GOV.UK".
Replaces: `Quatre accès à l'écosystème` (4 bordered icon cards), `Les espaces de l'écosystème` (4 icon rows), and the portal's five dashed empty-state boxes.
Effort: low–medium. Impact: removes "a collection of cards", "every card with an icon", "cards for content that does not need a card" in one pass.

**3. Introduce a visible content-type vocabulary.**
Evidence: Bruegel (`Analysis` / `Policy Brief` / `Event` / `Book` in dark red, above every title); service-public (grey category above every tile title); BIS (`BIS Working Paper` + `No 1378` chips with right-aligned date); OECD (`Report` chip + `date • pages`).
Replaces: our untyped news index, glossary and forum listings.
Effort: medium (needs a taxonomy decision, then a single component). Impact: high — it is what makes dense pages scannable instead of tiring, and it is the difference between "a list" and "an index".

**4. Commit to a serif editorial voice at real scale, on a warm ground.**
Evidence: Freshfields (`h1` 80/88, `h2` 64/64, `h3` 40/40, all weight 400, cream ground, body 17); Bruegel (serif standfirsts at 18/27); Doctrine (mixed bold-sans + large-serif inside one headline block); MPG (green serif headline).
Replaces: H1 48/55.2 and H2 34/39.1 frozen above 1400 px, on a ground that is white for five of six sections.
Effort: low (we already load IBM Plex Serif and already have `#F4F1EA`). Impact: high — it is the cheapest route to "elegant, European, distinctive" and it uses assets we have already paid for.

**5. Use controlled full-width bands, alternating, with a purpose per band.**
Evidence: ILO (six bands, four colours: brand blue → aubergine nav → photo → white → pale blue → aubergine); IUAV (full-black "In evidenza" band); GIZ (dark full-width filter band); Designers Italia (alternating text-left / bleed-right image bands).
Replaces: one `.section--muted` in six sections.
Effort: low. Impact: high — it is the direct answer to "controlled full-width bands" on the client's wanted list and to the flat, undifferentiated vertical rhythm we currently ship.

**6. Adopt a single institutional keyline as brand signature, and use it everywhere.**
Evidence: ECB (4 px yellow left bar on panels); service-public/DSFR (4 px red left bar on the callout, 4 px blue bottom bar under tiles); ILO (3 px red bottom rule on tiles); Council of Europe (orange progress hairline).
Replaces: drop shadows, decorative offset frames (the hero photo frame), and the gold icon set.
Effort: very low. Impact: high — one 4 px rule is worth more identity than twelve line-icons.

**7. Rebuild the orientation process as a vertical step-by-step, not a decorative rail.**
Evidence: GOV.UK step-by-step (numbered circles on a vertical hairline; each step a bold title with a `Show` disclosure containing the real links; current step grey-filled; 8 rounds of user research behind it); EUR-Lex left services rail.
Replaces: the four small circles and four short labels in `Comment fonctionne l'orientation`.
Effort: medium. Impact: high — it converts our single most important conversion path from an illustration of a process into the process.

**8. Print the sources, the dates and the disclaimer; do not link them.**
Evidence: service-public (`Textes de loi et références` / `Services en ligne et formulaires` / `Voir aussi` as permanent end-of-page panels); EUR-Lex (version timeline with the current version bar-marked); GIZ ("Current data version as of December 31, 2025"); EUI (red Commission disclaimer in the footer, with the full legal address); Rijksoverheid (per-image credit lines).
Replaces: `Avertissement` as a footer link and a "Lire l'avertissement →" at the end of one home section; the `v2.0.0 — Fase 1` string in the footer.
Effort: low–medium. Impact: high — this is the precise register that makes a non-authority credible in front of authorities, and it is the thing that most distinguishes A-grade institutional sites from B-grade ones.

**9. Offset the heading column from the body column.**
Evidence: OECD ("About the OECD" heading at x=96 in a 395 px column, prose starting at x=520); IUAV (heading left, ghost link right across a 1300 px measure); ECB (panel split by a hairline into eyebrow+headline | body); Bruegel (title column | body column inside the floated white panel).
Replaces: six sections where eyebrow, H2 and lead all start at the identical x and share a 576 px measure.
Effort: low. Impact: medium-high — this alone breaks the "eyebrow + H2 + paragraph" monotony that the client named verbatim.

**10. Replace stock photography with commissioned imagery, real institutional photography, or structured image blocks.**
Evidence: Freshfields (commissioned flat illustration); admin.ch (a real press photograph of the Federal Council, credited "© FCh"); IUAV (duotone overlapping image blocks with label chips on the seams); ILO (photographed publication covers); Rijksoverheid (credited ANP photojournalism).
Replaces: the framed stock photograph of anonymous hands over a document in the home hero and the "post-it workshop" stock image on the project page (`project__1280x800__fr.png`).
Effort: high (budget, not code). Impact: high but slow — flag it early; it is the one item on this list that cannot be shipped by the front-end.

**11. Handle four languages the way institutions do.**
Evidence: UfM (`English | Français | العربية` as plain text links, and a three-script wordmark); admin.ch (four-language lock-up + inline sentence naming the other language sites); OECD (`Available in: English | français` per page).
Replaces: a `Français ⌄` dropdown in the utility strip, and untranslated French leaking into the Arabic pages.
Effort: low for the control, high for the content discipline. Impact: high for credibility with our specific audience, and it is the only item here that also fixes a correctness defect.

**12. Give the portal a proper side navigation with search and grouping.**
Evidence: Aksel (grouped rail with search at its head, disclosure chevrons, inline status pill); EUR-Lex (document-services rail).
Replaces: the flat six-item rail in `portal-dashboard`.
Effort: low. Impact: medium now, high as the portal grows.

**13. Show numbers only with a date and a source; never as a counter.**
Evidence: GIZ (`1,437 running projects` / `22B Total Volume in Euro` + "Current data version as of December 31, 2025"); OECD (chart with source line + sampling caveat + abbreviation footnote).
Replaces: the empty KPI-style widgets in `portal-dashboard` (`2 demandes transmises` is fine; the four dashed boxes with centred icons are not).
Effort: low. Impact: medium — and it pre-empts the "startup counters" and "empty KPI widgets" bans before anyone is tempted.

---

## Appendix — measured comparison table

All values computed at a 1440 px viewport via `getComputedStyle`, 20 September 2026.

| Site | Display face | H1 | H2 | Body | Reading measure | Container @1440 | Radius | Shadow |
|---|---|---|---|---|---|---|---|---|
| **Italy Legal Entry (ours)** | IBM Plex Serif | 48 / 55.2 w400 | **34 / 39.1 w500** | 16 (Plex Sans) | 576 | **1200 (83 %)** | 4 px | present |
| Freshfields | FreshfieldsHeadline | **80 / 88 w400** | 64 / 64 w400 | 17 | ~916 | 1392 (97 %) | 0 | none |
| OECD | Noto Sans Display VF | 60 / 64.2 **w900** | 28 / 36.12 w800 | 16 / 24 | 608–928 | 1248 (87 %) | 0 | none |
| GOV.UK | GDS Transport | 48 / 50 w700 | 24 / 30 w700 | **19 / 25** | **630 (44 %)** | 960 | 0 | none |
| Rijksoverheid | RijksSans | 40 / 45 w600 | 32 / 37 w600 | 17.3 / 27.3 | 324 (3-col) | 1168 | 0 | none |
| service-public.fr | Marianne | 40 / 48 w700 | **16 / 24 w700** | 16 / 24 | **800 (55 %)** | 776 dominant | 0 | none |
| Bruegel | Conduit ITC | 45.36 / 54.4 w500 | — | **18 / 27 (Officina Serif)** | 552 / 260 | 1136 | **0** | **none** |
| IUAV | Standard | **30 / 40 w400** | **30 / 40 w400** | 16 / 25 | 650 | 1300 (90 %) | 0 | none |
| DSFR (spec) | Marianne | 40 / 48 | 32 / 40 | 16 / 24 | — | — | **0 (three stops only)** | one, documented |
| Designers Italia (spec) | Titillium Web | 40–48 / 48–56 | 32–40 / 40–48 | 12–18 / 24 | **max 75 chars** | — | — | — |
| Aksel (spec) | Source Sans 3 | 40 / 52 | 32 / 40 | **18** base | **50–75 chars** | — | — | — |

Two numbers to keep in front of the team: **our H2 is 34 px at 1440 and 34 px at 1920**, and **our container is 1200 px at 1440 and 1200 px at 1920**. No site in this table does that. Fixing those two lines of CSS is the cheapest step from "conventional Django/Tailwind landing page" toward "world-class institutional ecosystem" — and it is a precondition for every other mechanism above.

---

## Sources

[OECD](https://www.oecd.org/en.html) · [OECD open-access announcement, July 2024](https://www.oecd.org/en/about/news/press-releases/2024/07/oecd-data-publications-and-analysis-become-freely-accessible.html) · [ILO](https://www.ilo.org/) · [Council of Europe](https://www.coe.int/en/web/portal) · [ECB](https://www.ecb.europa.eu/home/html/index.en.html) · [BIS](https://www.bis.org/) · [European University Institute](https://www.eui.eu/en/home) · [Università Iuav di Venezia](https://www.iuav.it/) · [Ca' Foscari Venezia](https://www.unive.it/) · [Università di Padova](https://www.unipd.it/) · [Max Planck Society](https://www.mpg.de/en) · [Rijksoverheid](https://www.rijksoverheid.nl/) · [service-public.fr](https://www.service-public.fr/) · [Système de Design de l'État (DSFR)](https://www.systeme-de-design.gouv.fr/) · [DSFR design tokens as DESIGN.md](https://github.com/betagouv/dsfr-design-md) · [GOV.UK](https://www.gov.uk/) · [GOV.UK Design System — type scale](https://design-system.service.gov.uk/styles/type-scale/) · [GOV.UK Design System — step by step navigation](https://design-system.service.gov.uk/patterns/step-by-step-navigation/) · [admin.ch](https://www.admin.ch/gov/en/start.html) · [Designers Italia — tipografia](https://designers.italia.it/design-system/fondamenti/tipografia/) · [Aksel (NAV) — typografi](https://aksel.nav.no/grunnleggende/styling/typografi) · [Bruegel](https://www.bruegel.org/) · [Doctrine](https://www.doctrine.fr/) · [Freshfields](https://www.freshfields.com/) · [Freshfields 2024 brand refresh](https://www.freshfields.com/en/our-thinking/news/news-search/2024/09/freshfields-reveals-refreshed-brand) · [Clifford Chance](https://www.cliffordchance.com/home.html) · [GIZ](https://www.giz.de/en/html/index.html) · [Enabel](https://www.enabel.be/) · [Union for the Mediterranean](https://ufmsecretariat.org/) · [EURES](https://eures.europa.eu/index_en) · [Migration Partnership Facility](https://www.migrationpartnershipfacility.eu/) · [Regione del Veneto](https://www.regione.veneto.it/) · [EUR-Lex, Regulation (EU) 2024/1348](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32024R1348) · [Sciences Po](https://www.sciencespo.fr/en/) · [Clio](https://www.clio.com/)

---

# Benchmark — Professional case-management and service-workflow interfaces, 2024–2026

*Research brief: `benchmark-platform`. Scope: the authenticated platform, not the public site. Sources are public design systems, published design histories and product documentation from public administration, health, legal, financial-crime compliance and education administration. Consumer SaaS was deliberately excluded except where named as an anti-reference.*

---

## 0. The finding that frames the rest of this section

Before any benchmark is useful, one fact has to be stated plainly: **Italy Legal Entry does not currently have a platform. It has the public website with a login in front of it.** Every recommendation below is therefore a build instruction, not a refinement.

The evidence is not interpretive:

- `portal-dashboard__1440x900__fr.png` (qa-person) and `portal-company__1280x800__fr.png` (qa-company) are **the same page**. Same H1 ("ESPACE RÉSERVÉ"), same standfirst ("Accédez à votre espace personnel pour suivre vos demandes, vos parcours et vos communications"), same six-section grid, same left rail (*Tableau de bord · Mes demandes · Mon parcours · Mes documents · Mes échéances · Communications*). The company account differs by exactly one extra card, "Mon organisation" — and its account block reads `qa-company@example.test · **Personne**`. A company is being told it is a person. `PLATFORM_REQUIREMENTS_V2.md` §3 requires that navigation adapt to permissions and that the public shell not be reused after login; §8 requires that the company workspace revolve around *fabbisogni*. Neither holds.
- The public mega-menu (*Personnes / Entreprises / Institutions / Universités & Formation / Forum Vénétie–Maroc / Actualités / Projet*) and the full public footer with eleven navigation links are rendered **on every authenticated page** (`portal-documents__1280x800__fr.png`, `portal-pathways__1280x800__fr.png`). The signed-in user is being marketed to.
- `portal-pathways__1280x800__fr.png` — "Mon parcours" — contains no parcours. A disclaimer banner, then a centred dashed box. The eleven case-file states of §6 (`DRAFT → ORIENTED → REVIEW_REQUIRED → TRAINING → SELECTION → ADMIN_PROCESS → PRE_DEPARTURE → ENTERED → POST_ENTRY → CLOSED / SUSPENDED`) have **no visual representation anywhere in the product**.
- `portal-documents__1280x800__fr.png` — "Mes documents" is a *file manager* ("Vous n'avez encore téléversé aucun document"), not a *register of obligations*. §7 defines seven user-visible document states (MANCANTE · CARICATO · IN REVISIONE · VALIDO · NON VALIDO · SCADUTO · DA SOSTITUIRE). None is expressible: `static/css/components.css:220-245` provides only `.badge--info/success/warning/error/pending`.
- The component catalogue is a brochure catalogue. Across 29 numbered sections and 74 KB (`static/css/components.css`) there is: §10 *Page header, hero variants*, §12 *Four entrances*, §13 *Cards*, §19 *CTA panel*, §29 *Motion — reveal on scroll*. There is **no data table** — the only table rule in the whole system is `.account-table` at `components.css:2943-2960`, fourteen lines inside "Account pages". There is no case header, no filter, no work queue, no assignment control, no document register, no activity feed, no diff view, no detail pane.
- There is one type scale, and it is an editorial scale. At 1280 px, `--font-size-h1` (`tokens.css:111`) resolves to its 48 px cap and `--font-size-lead` (`:115`) to ~20.6 px; `--section-gap` (`:158`) is 64–96 px. Those are magazine values. A work surface needs a second, denser scale (14/15 px UI body, 20–24 px control heights, 36–44 px table rows) and it does not exist.
- `components.css:2542-2574` — §23 *Empty state* — is a single rule: `text-align: center`, `border: dashed`, `max-inline-size: var(--container-narrow)`, `margin-inline: auto`, plus a 2.5 rem accent-coloured icon. That one rule is doing the work of every empty region in the platform, which is why five of them stack vertically down `portal-dashboard__1440x900__fr.png` and produce exactly the "collection of cards" the client rejected.

So the question is not "how do we make the portal prettier". It is "what are the eight or ten primitives that serious case-handling software has and this product lacks". That is what follows.

---

## 1. The case header that survives navigation

**The reference.** Two independent traditions converged on the same answer.

The UK **Ministry of Justice Design System** — the design system built specifically for caseworkers, probation officers and court staff — calls it the **identity bar**: *"Use the identity bar component to give users context of where they are within a service such as viewing a case."* Its markup is deliberately thin:

```html
<div class="moj-identity-bar">
  <div class="moj-identity-bar__container">
    <div class="moj-identity-bar__details">
      <span class="moj-identity-bar__title"><b>Jane Wolensky</b> and <b>Simon Wolensky</b></span>
    </div>
    <div class="moj-identity-bar__actions"> … </div>
  </div>
</div>
```

The title carries inline emphasis because a case is often *about* more than one named party. The actions slot holds a small number of primary/secondary buttons, or the MoJ **button menu** when there are more. MoJ's own guidance is that it earns its place only when the entity has **subsections you navigate between** — it is not a decorative page title.

**Epic's Storyboard** (health, deployed in most large US and many EU hospitals) reached the same conclusion from the other direction: a vertical column pinned to the left of the chart that *stays put regardless of which activity tab the clinician is in*. Its stated content model is the one to steal, because it is a *question model*, not a field list: **who they are · why they are here · recent events · key information · actions to take**. The documented benefits are unglamorous and exactly right — fewer clicks, less scrolling, better use of widescreen, and the patient's story told the same way every time.

**How to build it.** One Django inclusion tag, `{% case_header case %}`, rendered by the *platform* base template (not the public one) immediately under the platform shell, on every case-scoped URL. Contents, in this order:

1. **Identity line** — the person's or company's name, at `--font-size-h3` (20–24 px), not H1. The case is the page; the page title is a subsection name.
2. **Reference** — `ILE-2026-000148`, in tabular figures (`base.css:233` already sets `lining-nums tabular-nums`), selectable, with a copy control. Institutions quote references on the telephone.
3. **State chip** — one of the eleven §6 states, with a *domain* colour, not a generic semantic one (see §10).
4. **Three to five key/value pairs**, as a `<dl>` laid out with `display: grid; grid-template-columns: max-content 1fr` — pathway, opened date, responsible actor, next deadline. Labels at 13 px uppercase-tracked, values at 15 px.
5. **Actions slot**, right-aligned in LTR and start-aligned in RTL via `margin-inline-start: auto`.

Then a **contextual sub-navigation** immediately below it — MoJ ships both a *sub navigation* (horizontal) and a *side navigation* (vertical) component for precisely this second level. Horizontal for ≤6 sections; vertical rail on ≥1024 px when the case has many.

Make it `position: sticky; top: 0` with a collapsed variant: on scroll past ~120 px, the header reduces to identity + reference + state chip on a single 48 px row. Do this with `IntersectionObserver` on a sentinel element and a class toggle; no JS, no collapse — the full header just scrolls away, which is acceptable.

**Why it reads institutional.** Because it is a *record header*, not a profile card. It asserts that this thing has an identity independent of the screen you are looking at, that it can be cited, and that someone is responsible for it. Commercial dashboards open on aggregate metrics; institutions open on a named file. The header is also the single most effective cure for the "generic SaaS" charge, because no SaaS marketing template contains one.

**Today.** `portal-dashboard__1440x900__fr.png` has `ESPACE RÉSERVÉ` in display serif at roughly 48 px — a *page* title where a *case* title belongs — and it is identical for every user and every role. There is no reference number, no state, no responsible actor, nothing to cite.

---

## 2. The journey, visualised honestly

**The reference.** The MoJ **progress tracker** exists because a task list is the wrong shape for a regulated process. Its guidance is the most important sentence in this entire benchmark:

> *"When a user is subject to steps in a process outside of their responsibility or control, a progress tracker supports or replaces a task list by giving a different overview on progress and outcomes."*

And its two hard boundaries:

> *"This differs from a timeline in that it does not log events and grow."*
> Do not misrepresent the likelihood of progress — the tracker shows *predetermined, finite* steps, not promised outcomes.

That is a direct fit for `PLATFORM_REQUIREMENTS_V2.md` §11 ("Nulla deve far apparire Italy Legal Entry come l'autorità che decide") and for the Rule Engine's five permitted outcomes. The component is a vertical `<ol>`, one icon per step, a connecting rule drawn with a `::before` pseudo-element and a 6 px left border, two states only: complete and not complete.

Two supporting references:

- **DfE "Apply for teacher training"** publishes its whole state machine in the open: thirteen candidate-facing application states (*Awaiting references → Waiting to be sent → Pending decision from provider → Offer made → Pending conditions → Conditions met (recruited) → Enrolled*, plus the rejection, withdrawal and decline branches). Every dashboard variant is designed per state. This is the closest public analogue to §6's eleven states, and the lesson is that **you design the dashboard once per state, not once**.
- **Bootstrap Italia / Designers Italia** ships `.steppers` for linear procedures (header `<ul>` of `<li>` steps, a `.confirmed` class on completed steps, and a `.steppers-progress` bar sitting between the Back and Forward buttons) and a separate `timeline` component for chronological events. Italy's own public-administration system keeps the two concepts apart too.

**How to build it.** Two distinct components, never merged:

- `.ile-lifecycle` — the honest journey. A vertical `<ol>` of the §6 states *that apply to this person's pathway* (§6: "Non tutti percorrono tutti gli stati"). Three visual states: **done** (filled mark, full-opacity label), **current** (ring mark, label at `--weight-medium`, plus a one-line "what this means" and "who is responsible"), **not yet reached** (hollow mark, label at `--text-secondary`). Steps that lie with an external authority carry a discreet actor label ("Questura di Treviso", "Consolato") and an explicit *"Ce délai ne dépend pas d'Italy Legal Entry"*. **Never a percentage.** A percentage is a promise.
- `.ile-timeline` — see §6 below.

At ≥1024 px, put the lifecycle in a narrow left column (240–280 px) beside the case body, not stacked above it. This is the disciplined asymmetry the client asked for and it removes one full-width stacked band.

**Why it reads institutional.** Because it refuses to flatter. A commercial product shows 68 % complete; an institution shows *"Étape 4 sur 9 — Examen par l'autorité compétente — en attente depuis le 12 mai"*. The honesty is the aesthetic.

**Today.** `components.css:1696` §16 "Stepper & progress" and `:1826` §17 "Timeline (pilot sequence)" both exist — but §17 is explicitly labelled *pilot sequence*, i.e. a marketing device for the public project page. Neither is bound to the case-file state machine. `portal-pathways__1280x800__fr.png` shows the consequence: the page named "Mon parcours" renders no parcours at all.

---

## 3. "Next action" prominence

**The reference.** GOV.UK **One Login**'s design recommendations make a small but decisive point: if a service homepage lists what a user has submitted, label it *"Your applications"* — service-specific — because research showed generic menu labels made users think the link led somewhere else entirely. Generic labels cost comprehension.

The DfE dashboard states work carries the structural lesson: the dashboard is not a container of widgets, it is **a sentence about what happens next**, re-written per state.

**How to build it.** A single `.ile-next-action` band, full-bleed within the content column, directly under the case header, above everything else. It contains:

- an eyebrow: `PROCHAINE ACTION` (12 px, `--tracking-eyebrow`);
- one imperative sentence at `--font-size-h3`: *"Téléversez votre certificat de langue italienne (niveau A2)"*;
- one line of consequence and deadline: *"Requis avant le 30 octobre 2026 · sans ce document, l'étape « Procédure administrative » ne peut pas s'ouvrir"*;
- **one** primary button;
- one `<a>` for "pourquoi cette demande" pointing at the rule and its source.

Exactly one. §4 of the requirements says "prossima azione (una sola priorità)". When the responsible party is *not* the user — and for a mobility pathway it usually is not — the band changes voice entirely: `EN ATTENTE` / *"Aucune action de votre part n'est requise. Le dossier est en cours d'examen par [actor] depuis le [date]."* That second variant is what makes the first one credible.

Visually: no card. Give it a 3 px `border-inline-start` in the accent, a `--surface-2` ground, generous internal padding, and let it sit flush in the column. A bordered rounded card here would immediately read as a SaaS "upsell tile".

**Why it reads institutional.** Because it takes a position. Five cards of equal weight (the current dashboard) tell the user that the system has no opinion about what matters. One statement, with a deadline and a named responsible party, is how a registry, a court office or a chamber of commerce communicates.

**Today.** `portal-dashboard__1440x900__fr.png` has no primary action anywhere. It has five empty dashed boxes, four "Toutes mes …→" links of identical weight, and a large numeral `2` above "demandes transmises" — a startup counter, explicitly on the banned list (RB §11).

---

## 4. Checklists that name a responsible party

**The reference.** The GOV.UK **task list** was rebuilt after two years of cross-government work, and every change it made is instructive:

- statuses moved to **sentence case** ("Completed", "Incomplete") because uppercase is harder to scan;
- **the whole row is the link**, because users were clicking the status as if it were a button;
- statuses are mixed: a finished task is **plain black text**, an unfinished one is a **blue tag** (`govuk-tag--blue`). Not every status gets a coloured chip — colour is reserved for what needs attention;
- optional hint text is *"a single short sentence, without any full stops"*, with no links inside it;
- it is explicitly **not** for showing a user's answers (use a summary list) and **not** for a fixed-order process.

The missing half, for this project, comes from the requirements themselves: §11 mandates *"passo · stato · attore responsabile · documenti richiesti · scadenza se nota · fonte · azione dell'utente · note"*. No public design system ships that, because no public design system has to coordinate a person, a company, an authorised actor and a training body on the same list.

**How to build it.** `<ul class="ile-checklist">`, one `<li>` per obligation, laid out as a three-column grid at ≥768 px and stacked below:

```
[ task name + hint ]  [ responsible party ]  [ status ]
```

- **Responsible party** is a first-class column, not metadata: `Vous` · `AGAMI` · `Entreprise X` · `Autorité compétente` · `Organisme de formation`. Render `Vous` at `--weight-medium` in the text colour and every other actor at `--text-secondary`, so the user's own obligations are visually extractable at a glance from a list of twenty.
- **Status** uses the domain vocabulary, plain text when settled, tagged when action is needed.
- The row links only when the user can act; otherwise it is inert text with a date. Do not make a row clickable that leads nowhere — that is the single most common way these lists lose trust.
- Add an optional `[ échéance ]` column with MoJ's **contextual date** idea — a date that carries its own urgency wording in a table ("dans 6 jours", "en retard de 3 jours") rather than relying on colour alone.

Group with `<h2>` per phase; do not use summary cards (one card per obligation would be forty cards).

**Why it reads institutional.** The responsible-party column is the whole argument. It converts a to-do list into a **division of responsibilities**, which is what a legal-tech ecosystem between two states actually is. It also silently satisfies the mandate in §3 of the rebase directive: "chi è responsabile".

---

## 5. Document requirements as a register of obligations

**The reference.** Every serious document surface in regulated work is built the same way, and it is the opposite of an uploader.

- **IRCC (Canada, immigration)** issues a *personal document checklist* — the list exists **before** any file exists, generated from the application type. The portal's Details column carries states such as *"Uploaded – not submitted to IRCC"*: the state distinguishes "in my hands" from "in theirs". That distinction is exactly §7's `CARICATO` vs `IN REVISIONE`.
- The **MoJ "Upload files" pattern** is precise about the list: filename, file size, a download link, a delete action, presented in a **summary list**, with a success message at the top of the page after a deletion. It also recommends sequential upload (one file, then "add another") as the default, with batch multi-upload only where research proves sequential creates friction — because sequential is far kinder to users with low digital confidence, which describes a significant share of this platform's population. Notably, MoJ's pattern says **nothing about virus scanning**; §7 of the requirements does, which means that state (`IN SCANSIONE`) has to be designed here rather than borrowed.
- **Hummingbird** (financial-crime compliance) shows what the reviewing side needs: resizable side-by-side panes so an analyst can keep the request-for-information pinned on the left while working the file on the right.

**How to build it.** A **requirements register**, not a gallery. A `<table class="ile-doc-register">` — a real table, with a real `<caption>`, `<th scope="col">`, `scope="row"` on the document name:

| Document required | State | Version | Valid until | Linked requirement | Action |
|---|---|---|---|---|---|

- **Rows exist when the requirement exists**, with state `MANQUANT`. An empty register is a populated table of things you still owe — which means "Mes documents" is *never* empty for a person with an active pathway, and the dashed centred void in `portal-documents__1280x800__fr.png` disappears by construction.
- **Colour discipline**: `VALIDE` plain text with a small rule mark; `EN EXAMEN` neutral chip; `MANQUANT` / `NON VALIDE` / `EXPIRÉ` accented chip. Never five different colours in one column.
- **Version** matters legally. §7 requires version and upload history: expose `v2` as a link to the upload history rather than silently replacing a file. Superseded versions stay visible and struck-through-by-state (`REMPLACÉ`), not deleted.
- **Linked requirement** links back to the rule and its source. This is the single feature that makes the register feel like a legal instrument rather than Dropbox.
- Wrap in the existing scroll container (`layout.css:244`) for narrow viewports; below 768 px, transform each row into a definition block with the document name as heading. Do not horizontally scroll a six-column table on a 320 px phone.
- Sensitive-download requirements from §7 (authorisation on *every* download, signed temporary URLs, no `/media/` exposure) mean the Action cell must be a `POST` form or an authorised view, never a naked `<a href>` to a file path.

**Why it reads institutional.** A register with states and versions is the visual grammar of a records office. A grid of file thumbnails is the grammar of a consumer cloud drive.

---

## 6. Timeline and activity feed as the legal record

**The reference.** The **MoJ timeline** is the most transferable component in this whole benchmark because it was designed to show *"the history of a case or application"* and it has a byline slot that accepts a **system** as the author:

```
.moj-timeline
└ .moj-timeline__item
  ├ .moj-timeline__header
  │ ├ .moj-timeline__title    ("Risk assessment completed")
  │ └ .moj-timeline__byline   ("by Joe Bloggs"  |  "by NDelius")
  ├ .moj-timeline__date       (<time> — "4 June 2026 at 9:32am")
  └ .moj-timeline__description
```

`by NDelius` — attributing an event to a named system — is precisely what §16's audit trail needs when the Rule Engine, not a human, produced an outcome. MoJ's exclusions are as valuable as its inclusions: do not use the timeline as a task list, a progress indicator, navigation, or to display large amounts of information.

**How to build it.** `.ile-activity`, reverse-chronological, one `<li>` per `AuditEvent` the viewer is permitted to see:

- **Title** = the event in the past tense, in domain language: *"Règle ILE-RULE-0142 v3 appliquée"*, *"Document « Passeport » marqué VALIDE"*, *"Dossier assigné à [soggetto autorizzato]"*.
- **Byline** = actor. Person, organisation, or `Moteur de règles` / `Système`. Never anonymous.
- **`<time datetime="…">`** with tabular figures and the locale's own date form (Arabic must get Arabic-Indic or Western digits per project decision — decide once, in `tokens.css`, and never mix within a page).
- **Description** optional, one or two sentences.
- Left rule at 1 px `--border-subtle` with an 8 px dot per entry, drawn with `::before` and `inset-inline-start` so it mirrors correctly in Arabic. This is the single most common RTL failure in timeline components.
- Paginate or "show earlier activity" after ~15 entries. Do not lazy-load infinitely: an audit record that cannot be reached by a stable URL is not an audit record.

**Why it reads institutional.** It is a ledger. Ledgers are append-only, attributed, dated and boring — and boring, in this domain, is the luxury signal. This component alone does more for the "credible in front of a ministry" test than any amount of photography.

---

## 7. Queues, assignment and ownership

**The reference.** The best public evidence here is DfE's **TRS console** design history, which published its task-visibility research verbatim. The findings are unusually blunt and map directly onto §9's authorised-actor workspace:

- A **"Completed tasks" tab is essential**: *"One that really annoys me is currently once a task is completed, that's it, (it's) gone."*
- Users expect **search to apply to the task list itself**, not to the underlying records.
- Filters by **owner** and **task type** were requested repeatedly and are not optional.
- Ownership prevents duplicated work: *"It can cause duplication if someone has had to contact somebody and you can't leave a note or say 'I'm working on this'…"*
- **Status wording matters more than status colour**: users preferred **"On hold"** to **"Blocked"**, because "Blocked" implied a technical fault outside their control.
- Managers and agents disagreed about who may assign — so **assignment must be a permission, configurable per role**, which is exactly the deny-by-default, object-level model in §2.

HMCTS's Work Allocation service is the large-scale implementation of the same idea: tasks are generated from configurable business rules, assigned by role-assignment rules, and surfaced as *my tasks* by default, with *available tasks* as a second view.

The **MoJ filter** component is the standard furniture: a `moj-filter` panel beside the list, with a *Selected filters* area at the top rendering each active filter as a removable tag (`moj-filter__tag`, each with visually-hidden *"Remove this filter"*) plus a *Clear filters* link. Filters live in a sidebar; the selected set lives above the results.

**How to build it.** `/platform/queue/` for the authorised actor, the operator and the moderator:

- Tabs or sub-nav: **Mes tâches** (default) · **Disponibles** · **Terminées**. Default to *mine*.
- A filter rail (`moj-filter` shape) at ≥1024 px; below that, a `<details>` disclosure above the table so it costs no JS.
- Selected-filter tags immediately above the table, each a `POST`/`GET` link that removes one facet.
- The table: reference · subject · phase · responsible · waiting since · next deadline. **"Waiting since" as elapsed days, right-aligned, tabular** — the column an operator actually scans.
- Claim/assign as an explicit `POST` with a confirmation (MoJ's "confirm an action" pattern), producing an `AuditEvent` per §16 and §9's mandatory chain `CompanyNeed → AuthorizedActor → SelectionProcess → CaseFile/Person → AuditEvent`.
- Status vocabulary in the users' own words, decided with the AGAMI operators, not translated from English engineering terms. "En attente de pièce", "En attente de l'autorité", "Suspendu", not "Blocked".

**Why it reads institutional.** Because it makes responsibility visible and transferable, with a record of every transfer. And because "Terminées" persists — institutions do not delete their finished work.

---

## 8. Versioned rules with diff and four-eyes approval

This is the module where the product can genuinely be distinctive, because almost nobody builds it well, and it is the one §5 describes in most detail.

**The references.**

- **OECD / Observatory of Public Sector Innovation, *Cracking the Code* (Rules as Code)** gives the framing and, usefully, the vocabulary to put on screen: a machine-consumable version of a rule exists **alongside** its natural-language counterpart — never instead of it. Every rule screen must therefore be **two-column by design**: the legal text and its source on one side, the executable condition on the other, with the assertion that they correspond being a human, signed, dated act.
- **legislation.gov.uk** solves the hardest UI problem in the domain — *time*. Legislation is shown consolidated by default; "Show Timeline of Changes" reveals point-in-time versions, so you can read the law **as it stood on a given date**. §5 requires exactly this (`valid_from`, `valid_to`, "data della valutazione", reproducible snapshot). The interaction to copy: a date control in the rule browser reading *"Règles applicables au [date]"*, defaulting to today, which re-renders the whole ruleset at that instant.
- **Wagtail** — Django-native, so this is a build reference, not just an inspiration. Wagtail ships a configurable multi-task moderation workflow (replacing single-step "submit for moderation") where each task is assigned to a group; revision comparison is reachable **both from the revision listing and from inside the moderation review**, so an approver sees the diff in the act of approving rather than having to go and find it; and a log viewer records the object's history. That is the shape of §5's `DRAFT → LEGAL_REVIEW → APPROVED → ACTIVE → RETIRED`.
- **Flowable's DMN decision editor** shows the metadata bar that a rule screen needs: name, description, **version, creator, modification date**, plus a History control that loads any earlier version. **Camunda/DMN decision tables** are the honest visual form for conditions — a grid of inputs, outputs and a declared hit policy that a lawyer can read without learning JSON.

**How to build it.**

1. **Rule index** — a dense table: `rule_id` · juridiction · parcours · effet (`POSSIBLE` / `MISSING_REQUIREMENT` / `WARNING` / `STOP` / `REVIEW_REQUIRED`) · version · statut · valide du–au. Filter by the four-eyes lifecycle state. Sort by validity.
2. **Rule detail — two columns.** Left: the condition rendered as a **read-only decision table** (never raw JSON as the primary view; offer "voir la source" as a disclosure). Right: `source_title`, `source_url`, the quoted passage, and the NHS-style **"Review date"** primitive — a small, explicit statement of when the rule was last checked against its source and when it is next due. That one line, published, is worth more institutional credibility than any visual flourish.
3. **Diff.** Two-column, per-field, at the level of the *rule fields*, not of a text blob: condition changed, effect changed, validity window changed, message key changed, source changed. Use `--color-success-bg` / `--color-error-bg` as row washes at low opacity with a leading `+` / `−` glyph, and never colour alone — the marker plus a screen-reader label carry the meaning. Show the two version numbers, both authors and both timestamps in the diff header.
4. **Approval.** A dedicated review screen. The approver sees the diff, the source, and a form with an explicit statement — *"J'ai vérifié la règle contre sa source"* — plus an optional comment. The approve button is **disabled and explained when the approver is the author** (§5: "L'autore non approva la propria regola"), not merely rejected after the fact. Every transition writes an `AuditEvent`.
5. **Evaluation snapshot.** On every outcome page: ruleset version, evaluation date, and an expandable list of *every rule applied, with its version*. This is §20's acceptance criterion 2 made visible, and it is the feature that lets a university or a ministry audit the system instead of trusting it.

**Why it reads institutional.** Because it publishes its own fallibility — dated, versioned, sourced, reviewable, and attributable to two named people. Nothing in commercial software looks like this, which is the point.

---

## 9. Permission-scoped navigation and the two-band shell

**The reference.** **GOV.UK One Login** separates two things the current build conflates. Its service header has **two bands**: a top black band belonging to the *account* (navigate to your One Login, sign out of both), and below it a grey band belonging to the *service* (service name and the service's own navigation). The recommendation is explicit: replace generic menu labels with service-specific ones, because research showed users otherwise believed the links left the service.

**HMRC** goes further for internal tools with a distinct **internal header** — HMRC logo, a vertical teal bar on the left, a green bar — introduced because *"the internal header helped users recognise they were using an internal service"*, and accompanied by a flat prohibition: *"Do not use the internal header for services used by the general public."* HMRC also ships a **caseworker guidance banner** reserved for genuinely critical internal guidance and *"strictly for internal use… never displayed on public-facing pages."*

GOV.UK's **service navigation** component (`govuk-service-navigation`, with `__service-name`, `__list`, `__item--active` and a mobile `__toggle`) is the mechanical model.

**How to build it.**

- A **separate `platform_base.html`**, not `base.html` with an `{% if user.is_authenticated %}`. Different shell, same identity.
- **Band 1 (identity, 40 px)**: promoter line, the person's name and organisation, role indicator, language, sign out. Dark, quiet, persistent.
- **Band 2 (workspace)**: "Italy Legal Entry — Espace de travail" plus **only the modules this role has permission to use**. §3: "un modulo non disponibile **non si mostra** solo perché esiste nel codice". Build this from a permission-filtered registry in Python and iterate it in the template; never hard-code `<a>` lists in HTML.
- **Kill the public mega-menu and the public footer after login.** The platform footer is three links — mentions légales, confidentialité, version/build — on one line. The eleven-link marketing footer visible in `portal-documents__1280x800__fr.png` is actively harmful: it is an escape hatch out of the work surface.
- Adopt MoJ's **organisation switcher** shape for users attached to more than one entity (a professional with several mandates, a training body with several cohorts).
- Labels must be workspace labels. "Tableau de bord" is the generic label One Login's research warns about; "Mon dossier", "Mes obligations", "Pièces demandées", "Décisions et avis" are service-specific and tell the user where they are going.

**Why it reads institutional.** Crossing a threshold is a legal act, and the interface should acknowledge it. When the shell changes at login, the user understands that the rules changed too. When it doesn't — the current state — the authenticated area reads as a subpage of a brochure.

---

## 10. Dense but readable tables

**The reference.** MoJ ships the whole kit because caseworkers live in it: **sortable table** (ascending/descending column sort), **pagination**, **multi select** ("let users select all the items in a table"), **numeric data** ("make numbers more prominent"), **contextual date** ("highlights important information about a date in a table"), and **scrollable pane** for tables that unavoidably overflow. The existence of a dedicated *numeric data* and *contextual date* component is the signal: in case work, the numbers and the dates are the content.

DSFR — mandatory for French State services since circular n° 6411-SG of 7 July 2023 — likewise treats the `tableau` as a first-class component rather than a utility.

**How to build it.** A real `.ile-table` component in `components.css`, which does not currently exist:

- Row height 44 px at desktop (comfortable) with a `--density-compact` modifier at 36 px for queues. Add `--row-height-comfortable` / `--row-height-compact` tokens; the current spacing scale (`tokens.css:144-156`) has no such value.
- **UI type scale**: 15 px body / 13 px caption for tables, not the 16 px editorial body. Add `--font-size-ui` and `--font-size-ui-sm`.
- Horizontal rules only (1 px `--border-subtle`), no vertical rules, no zebra striping. Zebra striping is a crutch for rows that are too tall.
- `th` at 13 px, uppercase, `--tracking-eyebrow`, `--text-secondary`, with a sticky header (`position: sticky; inset-block-start: 0`) inside the scroll container.
- **Numeric and date columns right-aligned in LTR, and `text-align: end` so they mirror in Arabic**; `font-variant-numeric: tabular-nums` (already available at `base.css:233`).
- Sort as a `<button>` inside the `<th>` with `aria-sort` on the `th`; a server-rendered `?sort=field&dir=asc` round trip is entirely acceptable and keeps the platform JS-light.
- Below 768 px, transform rows into stacked definition blocks with the identifying cell promoted to a heading — not a horizontally scrolling six-column grid.
- Empty table: **keep the column headers** and put one full-width row explaining the absence. Carbon raised this exact issue; stripping the headers destroys the user's model of what the table is for.

**Why it reads institutional.** Density with air. A table that shows twenty rows without scrolling, in a typeface with real tabular figures, is the visual argument that this system holds actual records. Three cards showing "0" is the visual argument that it does not.

**Today.** There is no table component. `.account-table` (`components.css:2943-2960`) is fourteen lines and belongs to a settings page.

---

## 11. Inspector and detail panes

**The reference.** **Hummingbird**'s side-by-side investigation views with resizable panels are the clearest public statement of the need: *"Some people pin RFI details to the left panel while completing an AML workflow on the right, while others view case-level investigation details while writing a detailed narrative."* The requirement is not "a modal"; it is **two contexts held simultaneously** — the evidence and the act of recording a judgement about it.

Epic's Storyboard is the same principle applied to a persistent rail rather than a transient pane.

**How to build it — and where not to.** Be disciplined, because this is where products start to look like admin tools:

- **Do** use a two-pane layout for the document review surface (document preview / metadata + decision form) and for the rule editor (source text / condition). `display: grid; grid-template-columns: minmax(0,1fr) minmax(320px, 420px)` above 1280 px, stacking below. A `<details>`-driven disclosure is a perfectly good no-JS fallback.
- **Do** make the right pane's content addressable by URL (`?panel=document-12`), so a reviewer can send a colleague a link to exactly what they were looking at. Panes that only exist in client state cannot be cited, and in this domain everything must be citable.
- **Don't** build a global resizable-splitter framework. Resizing is a power-user affordance for people who use the tool eight hours a day; AGAMI's authorised actors will not, at first.
- **Don't** use modals for anything a user must compare against something else. MoJ's modal dialog is scoped to interruptions the user *must* interact with, and its **interruption card** to pausing a journey with important information — both are for decisions, not for reading.

**Why it reads institutional.** Because it respects that judgement requires evidence in view. A modal that hides the evidence while asking for the decision is a compliance failure dressed as a UI convention.

---

## 12. Guided wizards and progressive disclosure

**The reference.** GOV.UK's **form structure** guidance ("one thing per page") is the canonical statement, and its six claimed benefits are all directly relevant to a Moroccan applicant on a 360 px phone in a second or third language: users understand what is being asked, focus on one question, navigate an unfamiliar process, do better on mobile, **recover easily from errors**, and the service gains automatic save, per-question analytics and branching.

But note the exception, which matters for the operator side: pages may be merged after research, and the example given is *"internal service for government users who need to repeat and switch between tasks quickly"*. **One thing per page for the person; grouped forms for the operator.** Two different densities, deliberately.

The **Bootstrap Italia stepper** is the Italian public-administration implementation: `.steppers` with a `<ul>` header of `<li>` steps, `.confirmed` on completed steps, and `.steppers-progress` sitting between the Back and Forward controls — i.e. the progress indicator lives *with* the navigation, not floating above the page.

**How to build it.**

- One question per screen for orientation, with back, and with **save-and-resume**. The current start page already advertises "une question par écran… vous pouvez revenir en arrière" and offers "Vous avez un code de reprise ?" (`orientation-start__1280x800__fr.png`) — the mechanism exists, but the questionnaire itself has no visible step indicator.
- A compact step indicator, at the top of the form column: `Étape 3 sur 8`, with a thin rule showing proportion. Do not use a twelve-dot indicator on a phone.
- **Explanations beside the question, not in a tooltip** (§4: "spiegazioni accanto alle domande"). Use GOV.UK hint text for short cases and a `<details>` "Pourquoi cette question ?" for long ones.
- **A check-answers screen before submission** using a `govuk-summary-list` with per-row *Change* links, each returning to its question and coming back. §4 requires "revisione prima dell'invio finale"; the summary-list-with-actions is the proven form, and DfE's **summary card** variant is the right escalation when the same structure repeats (several company needs, several family members).
- Error handling: an error summary at the top of the page linking to each field, plus inline messages. This is not decoration — it is the difference between a person completing the form and abandoning it.

**Why it reads institutional.** One question, one explanation, one source, one way back. A multi-step form with a progress bar and three columns of inputs reads as data collection; a sequence of plainly-asked questions reads as an interview conducted by someone competent.

---

## 13. Empty states that teach

**The reference.** Nielsen Norman Group's three guidelines for empty states in complex applications:

1. **Communicate system status** — say what happened. *"There are no records to display for the selected date range"* resolves the ambiguity between "nothing here", "still loading" and "broken".
2. **Provide learning cues** — the empty state is often the only place a feature can be explained at the moment it is relevant ("pull revelations"). The canonical example: Datadog's *"Star your favorites to list them here."*
3. **Provide a direct pathway** — a button, a link, or an explicit instruction. Never a dead end.

**Carbon** adds the sizing rule that the current build gets wrong: **an educational empty state is for a page's primary resource; a secondary resource gets a plain one-liner.** A page with five equally-weighted illustrated empty states has told the user that nothing on it matters.

**How to build it.** Replace the single `.empty-state` rule (`components.css:2542-2574`) with three:

- `.ile-empty--primary` — used **once per page, maximum**, for the page's subject. Left-aligned, no dashed border, no decorative icon. A heading, two sentences that explain the mechanism (*"Les documents apparaissent ici lorsqu'une étape de votre parcours en requiert un. Aucune étape active ne demande de pièce pour le moment."*), and one action.
- `.ile-empty--inline` — one line of `--text-secondary` text inside a section, no box, no icon. This is what the four secondary regions on the dashboard should be.
- `.ile-empty--table` — a single full-width `<td>` row **under retained column headers**.

Three rules follow from the domain:

- **Distinguish "nothing yet" from "nothing you may see."** A permission-filtered list must not imply absence. §15 forbids a user discovering the existence of an unauthorised object — which means the empty state says *"Aucun élément à afficher"* and never *"3 éléments masqués"*.
- **Prefer to make emptiness impossible.** The document register (§5 above) is pre-populated with `MANQUANT` rows. The checklist is pre-populated from the pathway. Most of the current dashed voids are a data-modelling decision, not a design problem.
- **Never centre an empty state in a wide column.** Centring plus a dashed border plus a gold icon is the exact "generic SaaS" signature the client named, and it is currently applied five times on one page.

---

## 14. What actually separates institutional from commercial

Collating the references above, the difference is not decoration. It is six structural commitments:

1. **The record outranks the screen.** A case header with a citable reference, a state, and a responsible party, present on every view (MoJ identity bar, Epic Storyboard). Commercial products open on aggregates; institutions open on a named file.
2. **Nothing is claimed that is not true.** MoJ's progress tracker explicitly forbids implying progress the service does not control. Percentages, counters and "3 étapes restantes !" are the tells. §5's five permitted outcomes and the ban on "idoneo/ammissibile" are the same discipline in language.
3. **Every statement carries its provenance.** Source, version, validity window, review date, ruleset snapshot. Rules as Code, legislation.gov.uk point-in-time, NHS review date. This is the single cheapest and most powerful credibility device available and it is currently used nowhere in the platform.
4. **Attribution is universal.** Every event has an actor, including when the actor is a machine (MoJ's `by NDelius`). Anonymous state changes are how software loses standing in front of a regulator.
5. **Density is a courtesy, not a compromise.** Real tables, real registers, real queues, tabular figures, 36–44 px rows. The refusal to use a table is what produces "a collection of cards".
6. **Colour and ornament are rationed.** GOV.UK's task list gives a coloured tag only to what is incomplete. Nord's healthcare system is explicit: soft neutrals, roomy type, *nothing that would alarm someone sitting beside a patient*. Ornament spent on decoration is ornament unavailable for meaning.

And the negative test, stated as design rules rather than as the client's adjectives: **no card without a boundary it must express** (a card says "this is a separable object of the same kind as its siblings" — a document register row is not that); **no icon without a distinct referent** (five sections with five different gold icons is five decorations); **no equal-weight grid of five things** (it says the system has no priorities); **no centred column of text on a 1440 px work surface** (centring is for reading, asymmetry is for working).

---

## 15. Build list — the primitives that do not exist yet

Ordered by how much of the rejected result each one removes. All are absent from the 29 sections of `static/css/components.css`.

| # | Component | Replaces / removes | Requirement |
|---|---|---|---|
| 1 | `platform_base.html` + two-band platform shell | public mega-menu and 11-link footer on every authenticated page | §3 |
| 2 | `.ile-case-header` (+ contextual sub-nav) | the `ESPACE RÉSERVÉ` hero repeated per role | §6 |
| 3 | `.ile-next-action` band | the five equal-weight dashboard cards | §4 |
| 4 | `.ile-table` (sortable, sticky head, compact density) | absence — `.account-table` is 14 lines | §7, §8, §9 |
| 5 | `.ile-doc-register` with the 7 document states | "Aucun document" void; file-manager mental model | §7 |
| 6 | `.ile-checklist` with responsible-party column | absence | §11 |
| 7 | `.ile-lifecycle` bound to the 11 case states | §17 "Timeline (pilot sequence)", a marketing device | §6 |
| 8 | `.ile-activity` (attributed, dated audit feed) | absence | §16 |
| 9 | `.ile-queue` + filter rail + selected-filter tags | absence | §9 |
| 10 | `.ile-rule-diff` + approval screen with self-approval lock | absence | §5 |
| 11 | `.ile-empty--primary / --inline / --table` | the single centred dashed `.empty-state`, used 5× per page | — |
| 12 | Domain status vocabulary (state chips mapped to §6/§7 states) | generic `.badge--info/success/warning/error/pending` | §6, §7 |
| 13 | UI type + density tokens (`--font-size-ui`, row heights) | the editorial-only scale at `tokens.css:110-122` | — |
| 14 | `.ile-source-ref` + review-date line | absence | §5 |

Two cross-cutting constraints, since they will be discovered painfully otherwise:

- **RTL is structural, not a stylesheet.** Every one of these components has an inline axis that carries meaning: the timeline rule, the case-header actions, the checklist's responsible-party column, the diff's left/right, the table's numeric alignment. Use `inset-inline-start`, `margin-inline-start`, `border-inline-start`, `text-align: end` throughout, and test the two-pane inspector in Arabic before it is considered done. Neither DSFR nor Bootstrap Italia will help here — neither ships RTL — so this is original work.
- **These components must survive without JavaScript.** Sorting via query string, filters as a `<form>`, the inspector pane as `<details>` at narrow widths, the sticky case header degrading to a normal one. A platform used on poor connections, in four languages, by people whose administrative status depends on it, cannot make server-rendered correctness optional.

---

## Sources

Public administration — design systems and patterns
- [MOJ Design System — Components (full catalogue)](https://design-patterns.service.justice.gov.uk/components/)
- [MOJ Design System — Identity bar](https://design-patterns.service.justice.gov.uk/components/identity-bar/)
- [MOJ Design System — Timeline](https://design-patterns.service.justice.gov.uk/components/timeline/)
- [MOJ Design System — Progress tracker](https://design-patterns.service.justice.gov.uk/components/progress-tracker/)
- [MOJ Design System — Filter](https://design-patterns.service.justice.gov.uk/components/filter/)
- [MOJ Design System — Side navigation](https://design-patterns.service.justice.gov.uk/components/side-navigation/)
- [MOJ Design System — Sortable table](https://design-patterns.service.justice.gov.uk/components/sortable-table/)
- [MOJ Design System — Patterns index](https://design-patterns.service.justice.gov.uk/patterns/)
- [MOJ Design System — Upload files pattern](https://design-patterns.service.justice.gov.uk/patterns/upload-files/)
- [GOV.UK Design System — Task list](https://design-system.service.gov.uk/components/task-list/)
- [GOV.UK Design System — Summary list and summary card](https://design-system.service.gov.uk/components/summary-list/)
- [GOV.UK Design System — Service navigation](https://design-system.service.gov.uk/components/service-navigation/)
- [GOV.UK Design System — Check answers pattern](https://design-system.service.gov.uk/patterns/check-answers/)
- [GOV.UK Service Manual — Form structure ("one thing per page")](https://www.gov.uk/service-manual/design/form-structure)
- [GDS design notes — Iterating the task list pattern as a community](https://designnotes.blog.gov.uk/2023/12/15/working-as-a-community-to-iterate-the-task-list-pattern/)
- [HMRC Design Resources — Internal header](https://design.tax.service.gov.uk/hmrc-design-patterns/internal-header/)
- [HMRC Design Resources — Caseworker guidance banner](https://design.tax.service.gov.uk/hmrc-design-patterns/caseworker-guidance-banner/)
- [GOV.UK One Login — Let users navigate to their One Login and sign out easily](https://www.sign-in.service.gov.uk/documentation/design-recommendations/let-users-navigate-sign-out)
- [Designers Italia — Design system .italia](https://designers.italia.it/argomenti/design-system/)
- [Designers Italia — Steppers](https://designers.italia.it/design-system/componenti/steppers/)
- [Designers Italia — Timeline](https://designers.italia.it/design-system/componenti/timeline/)
- [Bootstrap Italia — Steppers](https://italia.github.io/bootstrap-italia/docs/componenti/steppers/)
- [Système de Design de l'État (DSFR) — Fil d'Ariane](https://www.systeme-de-design.gouv.fr/version-courante/fr/composants/fil-d-ariane)
- [Système de Design de l'État (DSFR) — présentation](https://www.info.gouv.fr/organisation/service-d-information-du-gouvernement-sig/systeme-de-design)

Education administration — published design histories
- [DfE — Apply for teacher training: application dashboard states](https://becoming-a-teacher.design-history.education.gov.uk/apply-for-teacher-training/application-dashboard-states/)
- [DfE — Manage teacher training applications](https://becoming-a-teacher.design-history.education.gov.uk/manage-teacher-training-applications/)
- [DfE — TRS console: task visibility user research findings](https://design-histories.education.gov.uk/trs-console/task-visibility-user-research-findings)
- [GDS blog — Why and how we create design histories](https://dfedigital.blog.gov.uk/2020/09/01/design-history/)

Health
- [NHS digital service manual — Components](https://service-manual.nhs.uk/design-system/components)
- [Nord Design System (Nordhealth) — About](https://nordhealth.design/about/)
- [Epic Storyboard — Connect Care glossary](https://ehealth.connect-care.ca/epic-systems/epic-modules/storyboard)
- [University of Iowa Health Care — Epic Storyboard](https://epicsupport.sites.uiowa.edu/epic-resources/storyboard)

Immigration and legal records
- [IRCC — What is a personal document checklist?](https://ircc.canada.ca/english/helpcentre/answer.asp?qnum=829&top=23)
- [IRCC — Uploading documents after submission](https://ircc.canada.ca/english/helpcentre/answer.asp?qnum=1624&top=38)
- [legislation.gov.uk — Changes to Legislation](https://www.legislation.gov.uk/changes)
- [legislation.gov.uk — Help (point-in-time versions, timeline of changes)](https://www.legislation.gov.uk/help)

Rules, versioning and approval workflow
- [OECD OPSI — *Cracking the Code: Rulemaking for humans and machines*](https://oecd-opsi.org/publications/cracking-the-code/)
- [OECD Working Paper No. 42 — Rules as Code (PDF)](https://oecd-opsi.org/wp-content/uploads/2022/03/rac-wp.pdf)
- [Wagtail — Managing workflows (moderation)](https://docs.wagtail.org/en/v4.0.4/editor_manual/administrator_tasks/managing_workflows.html)
- [Wagtail — Comparing revisions (PR #3170)](https://github.com/wagtail/wagtail/pull/3170)
- [Flowable — Decision editor (version, history)](https://documentation.flowable.com/latest/user/design/dmn-editor)
- [Camunda — DMN in Modeler](https://docs.camunda.io/docs/components/modeler/dmn/)

Banking / financial-crime compliance
- [Hummingbird — Side-by-side investigation views](https://www.hummingbird.co/resources/see-exactly-what-you-need-with-side-by-side-investigation-views)
- [HMCTS — Work Allocation task management API](https://github.com/uk-gov-mirror/hmcts.wa-task-management-api)
- [HMCTS — CCD caseworker UI](https://github.com/hmcts/ccd-case-management-web)

Empty states and enterprise interaction
- [Nielsen Norman Group — Designing empty states in complex applications: 3 guidelines](https://www.nngroup.com/articles/empty-state-interface-design/)
- [Carbon Design System — Empty states pattern](https://carbondesignsystem.com/patterns/empty-states-pattern/)