# UX PUBLIC — V5 council · Senior UX panel for the public surfaces

**Panel:** Institutional UX · Navigation / IA · Brand · Accessibility · RTL / Arabic (one reviewer holding five chairs, see §12) · **Date:** 27 September 2026 · **Repository:** `C:/tmp/italylegalentry`, `main` @ `c9a58d8`, `git status` clean at session start; read only, **nothing modified**. · **Written by this panel:** this file and two crops in `C:/tmp/ile_v5_council/scratch/ux_public/`. · **Status:** PROPOSAL. No rule here is in force until the CD and the owner sign it and a gate measures it.

**Inputs read.** Captures (the 15 PNGs + 2 crops listed in §11) · council files `CAPTURES_AND_REFERENCES.md`, `UI_INVENTORY.md`, `IMAGERY.md`, `MOTION.md`, `ICON_SEMANTIC_MAP.md`, `TYPOGRAPHY.md`, `COLOUR.md`, `21st_hero-public.md`, `21st_nav-shell.md` · templates `base.html`, `partials/{utility_bar,header,main_nav,footer}.html`, `pages/home.html` and all eleven `pages/home/_*.html`, `pages/home/partials/{_hero_title_lines,_route_glyph}.html`, `components/{doorway,entrances,pathway_list}.html`, `pages/partials/_section_header.html`, `forum/index.html` + `forum/partials/{hero,local_nav,presentation,programme,speakers,cta_row,home_banner}.html`, `allauth/layouts/entrance.html`, `pathways/_antifraud_callout.html`, `pathways/index.html` l.45–51 · CSS `v4/hero.css`, `v4/shell.css`, `v2/voyage.css`, `v2/routes.css`, `base.css`, `components.css` · code `apps/cms/templatetags/cms_nav.py` (fallback menus, lock-up), `apps/cms/locked_content.py` (hero, entrances, banner keys), `apps/pages/services.py` (hero CTAs, news builder), `apps/core/gates.py` (Forum gates), `apps/portal/services.py` (`JOURNEY_STEPS`) · docs `docs/design-v4/CREATIVE_DIRECTION.md` §1–3.3, `docs/design-v2/BRAND_ASSETS.md` §1–2, `docs/ACCESSIBILITY.md` (gap G-08).

---

## 0. Verdict

The owner is right. In order of severity:

1. **The owner judged an unfinished V4, not V4.** On the public home only the hero (1 of 11 sections) and the navigation were built in the V4 direction; the other ten sections are the V2 «register» under V4 tokens (`UI_INVENTORY.md` §10.2). V4's own plan for the page — four equal doors with glyph discs and a spotlight, a process route with the Morocco→Italy frontier, news cards with images, two photographs in the ecosystem chapter (`CREATIVE_DIRECTION.md` §3.1) — was never built. A V5 that redesigns the first screen and leaves the rest would fail for the same reason. **Recommendation zero: V5 public is a pass over every home section and every public template, not a new hero.**
2. **One photograph on the whole public site**: the door, which is the brand, reused on the login. A platform about Italy and Morocco shows neither country, no person, no place. Below the first viewport the home runs ≈ 6,900 px (1440) and ≈ 10,200 px (390) without a single photograph.
3. **Repetition without progression.** The four audience names appear four times on the home (nav, hero legend, doors, footer) and twice more in menus, always with the same words; the hero legend and the doors print the same glosses. Ordinals are everywhere (section folios 01–06 that skip two sections, doors 01–04, pathways 01–08, pilot 01–08, a Forum programme that reads «15h00, 02, 03 … 08»), so no number means anything.
4. **Nothing happens in time.** No loading state, no page change, no reveal. The first painted frame of the home is an empty cream sheet that then flips to navy. The one scroll-linked story (the pilot route) shows eight unconnected dots when not scrolled and puts «VÉNÉTIE» above step 05.
5. **The brand's gesture is never performed.** The door and the key are a picture. The one moment the brand stands for — passing a door, regularly — has no moment in the story, in the navigation, or at the login.
6. **The phases have no form.** Morocco-side and Italy-side phases are drawn four different ways (orientation list, pilot route, jurisdiction bar, pathway list); the crossing is a mislabelled dot. The site's own phases (interim → phase 3; Forum before → after 2 October) switch by flag, with no designed transition.
7. **The chrome is text only, and unequal.** Three of seven top-level items open a panel; two of the four audience doors have none. The panel is a flat link list with identical chevrons. The mobile drawer lists utilities before navigation and says «Menu» while open.
8. **Visible cracks** that a premium eye catches in seconds: «ATTENTIO / N AUX FRAUDES» broken mid-word in the Espace Personnes rail; «Comment ça marche» printed twice; pathway and FAQ titles set smaller than their descriptions; a French sentence inside the Arabic hero; a build label («v2.0.0 — Fase 1») in the public footer.

**What a world-class 2026 institutional legal-tech product does instead:** it tells one story — *two shores, one regular door* — on every surface; each recurrence of a concept adds a layer; every wait and every change of place gets a designed moment that is also the brand; every word stays verifiable. All of it can be built with Django templates, CSS and a few small ES modules. Nothing below needs React.

**Five signature moves — the V5 public in five lines**

| | Move | What it is |
|---|---|---|
| S1 | **«Una porta, due rive»** | The home as one passage: the door → the four doors → what we do not do → the passage (seven phases, two thresholds) → start → the routes → the Forum (a dated rendez-vous) → who is behind it → the reserved door (§3, §5). |
| S2 | **«Il portico si apre»** | One surface gesture for mega-menu, search and drawer (`21st_nav-shell.md` §4.1), a photograph per door, and the anti-fraud step at the foot of every panel (§3.2, §3.10). |
| S3 | **«La chiave che gira»** | The key of the mark turns in every wait (`MOTION.md` §6); the thread «la soglia» covers every navigation; View Transitions keep the chrome still (§6). |
| S4 | **«Due portici»** | The IMAGERY library, one context per image, one grade; the Padua · Casablanca diptych at the head of the passage, where the two shores are named (§4, §5). |
| S5 | **«Il gradino»** | The anti-fraud message becomes one calm architectural element — the step you cannot skip — instead of four treatments, one of which breaks (§4.3). |

S1 and S5 are this panel's names; S2–S4 reuse the council's.

---

## 1. Scorecard — the public surfaces today

Scale 1–5, one reviewer, from the captures and the templates. **Premium** = material, craft, restraint. **Dynamic** = designed behaviour in time. **Memorable** = could you describe it tomorrow. **Clarity** = where to go next. **A11y/RTL** = what the captures and the markup show; it is not an audit.

| Surface | Premium | Dynamic | Memorable | Clarity | A11y/RTL | Main evidence |
|---|---|---|---|---|---|---|
| Home — hero | 3 | 2 | 4 | 3 | 3 | `before_home-8771_1440.png`, `before_home-8770_1440.png`, `typography/before_ar_home_1440.png` |
| Home — below the hero | 1 | 1 | 1 | 3 | 3 | `before_home-8771_1440_full.png`, the two crops |
| Letterhead + mega-menu | 2 | 1 | 1 | 2 | 4 | `before_megamenu-8771_1440.png` |
| Mobile drawer | 2 | 1 | 1 | 3 | 3 | `before_drawer-8771_390.png` |
| Espace Personnes (inner page) | 1 | 1 | 1 | 3 | 3 | `before_parcours-8771_1440_full.png` |
| Forum | 2 | 1 | 1 | 3 | 3 | `before_forum-8771_1440_full.png` |
| Footer | 3 | 1 | 1 | 4 | 3 | full-page captures |
| Login | 3 | 1 | 3 | 4 | 4 | `before_login-8771_1440.png` |
| Loading / page change | 1 | 1 | 1 | — | — | `before_loading-home-8772gzip_1440_fp+0250ms.png` |

The hero is the only surface above 2 for «memorable», and it earns that through the owner's door. Everything after the first scroll scores 1.

---

## 2. Cross-cutting findings

### 2.1 Repetition audit — the same thing, with no new layer

| What repeats | Where | Why it hurts | V5 rule |
|---|---|---|---|
| The four audience names | nav, hero legend (same glosses as the doors: `_hero.html` comment, «the same texts the entrances section renders»), doors section, footer, drawer, mega-menu | Six appearances, one layer. The legend and the doors are the same object twice, 700 px apart. | **Each recurrence adds a layer.** Nav = the word. Hero legend = the word + its route (a choice). Doors = image + promise + the first two tasks. Mega-menu = the door's full map + its photograph. Footer = the plain index. A recurrence that adds nothing is removed. |
| The brand name | header lock-up, then the hero H1 (`p3.hero.title` = «ITALY LEGAL ENTRY™»), 250 px apart | The largest type on the site restates the logo; the promise («Le parcours régulier vers l'Italie, de l'orientation à l'intégration.») comes second. | §3.1 move H2. |
| Ordinals | folios 01–06 (the pilot and anti-fraud sections are unnumbered), doors 01–04 inside folio 01, pathways 01–08, pilot 01–08, Forum programme «15h00, 02…08» | Numbers stop meaning order. | Numerals **only** for real sequences a person follows: the seven phases, a programme's times. Section eyebrows are words. The doors are not ranked. (V4 CD §1 had already retired «01/02»; they survived in the V2 sections.) |
| The arrow glyph | 80 of 163 icon calls (`ICON_SEMANTIC_MAP.md` §0) | Every link looks like every CTA. | One arrow per block, on the forward action only. |
| Audience glyphs reused for pathways | `person` = Personnes **and** «Regroupement familial»; `building` = Entreprises **and** «Travail indépendant» (parcours capture; ICON map §2) | On the Espace Personnes page the Persona glyph labels one of eight pathways. | ICON map §5.1 and §7. |
| `lock` for «Espace réservé» | utility bar, drawer, home reserved panel | «Locked» reads «not for you»; in V5 `lock` means BLOQUÉ. | `ile-key`: the reserved door is opened by the key (ICON map). |
| The door photograph | home hero, login | Intentional (brand): keep. But it is also the **only** image of Italy the visitor sees. | Add the IMAGERY library; never a third use of the door. |
| «People at a table with laptops» | 6 of the 15 current library photos; one of them stands for two different actors (AGAMI and the Institutions audience) | The actors cannot be told apart. | `IMAGERY.md` §1, §3. |
| Anti-fraud, four treatments | home panel (large shield + uppercase serif), pathways rail callout (broken, D1), footer outline pill, one link among seven in the Personnes panel | The most important safety message has no identity, and one version breaks. | «Il gradino», §4.3. |
| Uppercase serif | door titles, page titles, Forum titles, anti-fraud, pilot | One voice for everything, so nothing stands out. | §2.5. |

### 2.2 Loaders, states and waits — what the visitor actually sees

- **First frame** (`before_loading-home-8772gzip_1440_fp+0250ms.png`, gzip server, slow 4G + CPU ×4): a cream sheet, the wordmark in its fallback serif, no mark, one nav label («Personnes»). The navy hero arrives later. The first thing the audience sees is an empty page that flips to navy, a luminance flash on the one page that must feel composed. The home HTML is 7,953 B gzipped on 8772 (measured with one GET), so this is most likely parse and paint order under CPU ×4, not transfer — to confirm in a trace.
- **Nav labels pop in one by one** (`CAPTURES_AND_REFERENCES.md` §2): the header steps during the first second.
- **No navigation feedback.** On slow 4G, 2–4 s pass between a click and the next paint, with the old page frozen.
- **Forms.** The busy meter exists only on allauth forms (`form[data-single-submit]`). The enquiry forms, the Forum registration and the public orientation questionnaire have none. The questionnaire is a full-page POST per step with a percentage bar and inert `hx-*` attributes (`UI_INVENTORY.md` P60): the home's primary CTA leads into the least designed flow on the site.
- **Empty states on the public home.** «Aucune actualité publiée pour le moment» (section 05) and «Les partenaires sont présentés au fur et à mesure…» (section 06). The first is deliberate: in phase 3 `build_news` returns the block even when empty (`apps/pages/services.py` l.622–626). An empty state in an institutional showcase is an owner decision, not a bug (§3.8 T5).
- **Disabled CTAs on the Forum** (`span.is-disabled`, `cta_row.html`): dead ends with no «when».

### 2.3 Phase transitions — Morocco, the crossing, Italy; and the site's own phases

(The brief's «weak phase transitions». §5 gives the design.)

- The same subject — what happens before, at and after the crossing — is drawn four ways: the orientation sequence (four ticks), the pilot «route between two shores» (eight stations, `_pilot.html`), the jurisdiction bar (four textured segments, `_trust.html`) and the pathway list (eight rows, one of them «Formation dans le pays d'origine»). None shows where Morocco ends and Italy begins. None uses the brand's door at the crossing.
- **The pilot route is the only one that tries, and it fails twice in the capture** (`crop_home_pilot_trust_1440.png`). Unscrolled, the line is not drawn: eight floating circles. And the «VÉNÉTIE» label sits above station 05 instead of the far end. Cause, read in `v2/voyage.css` l.40–51: `grid-template-columns: auto auto` with `justify-content: space-between`, while the SVG and the station list span both columns, so the two auto tracks absorb the full width and the second column starts at the middle. `justify-self: end` for the north shore exists only in the < 64rem block (l.188). The result is exactly the editorial claim the template says it refuses to make («which shore each step belongs to»): it visually puts the Veneto shore at «Procédures régulières». **P0 defect (D4).**
- **The code already knows the phases.** `apps/portal/services.py` `JOURNEY_STEPS` holds seven steps with a side (`morocco` ×3, `italy` ×4), and the console's JourneyRail draws the frontier between them. The public site never shows the visitor the sequence they will later find in their own dossier. That is a lost bridge between portico and console.
- **A semantic trap to resolve before anything is drawn.** In `JOURNEY_STEPS` the side switches before «Procédures auprès des autorités compétentes» and «Préparation du départ», which physically happen *before* departure. So «side» means *jurisdiction* (whose authorities act), not *place*. One frontier drawn as «the crossing» would tell a person they have crossed when their visa procedure starts. `ICON_SEMANTIC_MAP.md` §5.3 puts `ile-crossing` («two shores + one arc») at that frontier and inherits the same ambiguity. §5.2 proposes two thresholds.
- **Site phases.** Interim (8770) and phase 3 (8771) show two different heroes: a five-line uppercase title with three exit labels, and the trademark as H1 with none. The site changes identity by gate. The Forum switches from event to «Forum permanent» by flag (`gates.forum_banner_visible`, `gates.forum_permanent_mode`), with no day-of state and no recap state. The event is on **2 October 2026, five days from today**. The QA Forum page renders the permanent mode, with no registration and the date on one small line.

### 2.4 Hierarchy inversions and cracks

| # | Defect | Evidence | Cause (read in code, to confirm in a browser) | Fix |
|---|---|---|---|---|
| D1 | «ATTENTIO / N AUX / FRAUDES» broken mid-word in the Espace Personnes rail | `before_parcours-8771_1440_full.png`, right rail | `pathways/_antifraud_callout.html` renders `h2.notice__title`; `components.css` l.261 and `v4/shell.css` l.751 set weight and family but no size, so the global h2 size lands in a ≈ 150 px column; `base.css` l.43 `overflow-wrap: break-word` breaks the word | Size from a container query (`@container (inline-size < 20rem)`), never larger than the column's longest word; `hyphens: manual`; the callout is redrawn as «il gradino» (§4.3) |
| D2 | «Comment ça marche» printed twice (a heading, then the first words of the locked text) | parcours capture, bottom | `pathways/index.html` l.49 adds a visible heading; the locked `p3.persons.how_it_works` starts with the same words | Visually hidden heading (kept for the outline) |
| D3 | Pathway titles smaller than their descriptions; FAQ questions smaller than their answers | parcours capture; `crop_home_entrances_pilot_1440.png` (pathways); `crop_home_pilot_trust_1440.png` (trust) | Title ≈ 13 px bold serif vs body ≈ 15 px | Title ≥ body + 2 steps (TYPOGRAPHY scale): question/title 17/24 600, answer 15/24 |
| D4 | «VÉNÉTIE» above station 05 | pilot crop | §2.3 | `justify-self: end` on `.voyage__shore--north` at every width; re-capture |
| D5 | Pilot line invisible when not scrolled | pilot crop | The scroll-drawn line starts at 0 % | `MOTION.md` §7 «lit window»: the whole line is always drawn at low contrast; the light adds and never withholds (`MOTION.md` §2.2) |
| D6 | A French sentence inside the Arabic hero | `typography/before_ar_home_1440.png` | The interim locked body fragment has no Arabic and falls back to FR | Content first (translation or hide in `ar`); if kept: `lang="fr" dir="ltr"`, isolated, set in the Latin face at the Arabic size |
| D7 | Hero body starts lower-case («orientation vers des parcours…») on 8770 | `before_home-8770_1440.png` | **Deliberate**: `body_is_fragment` renders a locked fragment | Owner/content decision; as shipped it reads as a typo |
| D8 | Exit labels over the door's photograph | 8770 hero; Arabic hero (inside the arch) | **Deliberate** V4 exits at x 624–636 of the stage | V5 removes the exits (§3.1 H4) |
| D9 | «× Menu» while the drawer is open | `before_drawer-8771_390.png` | Static `<span>Menu</span>` in `partials/header.html` | «Fermer» while open; the button's name follows |
| D10 | «Privacy Policy», «Cookie Policy» in English without `lang="en"`; build label «v2.0.0 — Fase 1» in the public footer | full-page captures; `docs/ACCESSIBILITY.md` G-08 | Known residual gap; `SiteSettings.version_label` default | `lang="en"` (or translate: owner); keep «contenus vérifiés le …» (a real trust cue); move the build label out of the public footer |
| D11 | Two panel entries to one URL: «Voir l'espace» and «Votre parcours» (both `pathways:index`); Projet → «Italy Legal Entry» (= `pages:project`) | `cms_nav.py` `_FALLBACK_MAIN` | Fallback data | One destination per panel entry (§3.2) |
| D12 | The doors' zig-zag 7/5 · 5/7 ranks four equal doors (the long one reads «first») | entrances crop | **Deliberate** V2 «quay of four piers» (`v2/routes.css` l.1–35); V4 CD §3.1.2 asked for an equal 2×2, not built | Four equal doors (§3.3) |

D7, D8 and D12 are deliberate choices in the code (project memory: *visual defects are often deliberate*); they are listed as design or owner questions, not as bugs. D1, D3, D4, D5 and D9 read as defects. Each one needs a browser measurement before a fix is committed, and every page the touched sheet reaches must be re-captured (project memory: *re-measure after every change*).

### 2.5 The typographic voice (UX view; the system itself is `TYPOGRAPHY.md`)

- **Uppercase is partly content.** The locked door titles («ÊTES-VOUS UNE PERSONNE ?»), the door buttons and the banner button («DÉCOUVREZ LE FORUM») are uppercase in `locked_content.py`. The design must leave them as they are, and must stop *adding* uppercase everywhere else (page titles, Forum titles, anti-fraud, pilot, CTA labels in CSS). Then the locked capitals read as engraving, not as shouting.
- **Light serif capitals collide.** Uppercase Newsreader 300 at display size with tight leading makes accented capitals touch the line above («VÉNÉTIE», «RÉGULIER»: parcours and pilot captures). TYPOGRAPHY pairing A (Source Serif 4, 400) or B (Newsreader ≥ 400, `opsz` 72) fixes the weight. This panel adds: sentence case for every non-locked title; `line-height` ≥ 1.1 on any line of accented capitals; `text-wrap: balance` on titles.
- **Three heading voices on one inner page**: serif titles, blue bold sans notice titles, bold serif list titles. V5: one display voice (serif, public only), one UI voice (sans); notices in the UI voice at UI sizes.
- **Arabic**: no uppercase, no tracking, no italics; small text one step larger than Latin. The Arabic eyebrow in the hero is ≈ 11 px and illegible (`TYPOGRAPHY.md` §8.6).

---

## 3. Surface by surface — critique, the world-class bar, concrete moves

Each move gives **what**, **how**, the **route** (A = Django + CSS + small JS; B = Motion 13 JS; C = React island; D = rejected) and its **guard** (budget, accessibility). Council cross-references are in brackets.

### 3.0 The home as one passage (S1) — chapter order and rhythm

Today: hero (navy) → 01 doors → 02 orientation → 03 pathways → pilot (navy) → 04 transparency → anti-fraud → 05 news (empty) → 06 promoter/partners → reserved → footer. Two dark bands in 7,800 px, one image, eight numbered folios.

Proposed order (the back-office keeps control of order and publication through `home_sections`; this is a recommendation to the editor, not code):

| # | Chapter | Recipe (`DESIGN_SYSTEM_V4.md` §1.4, as named in CD §3) | Images | Why here |
|---|---|---|---|---|
| 1 | **La porta** — hero (§3.1) | IMMERSIVE navy | the door (LCP, unchanged) | the promise, the four choices |
| 2 | **Quattro porte** — the four doors (§3.3) | SOFT paper | 4 (one per door) | «who are you» |
| 3 | **Ce que nous ne faisons pas** — trust + «il gradino» (§3.8) | NEUTRAL + stone band | — | for an anxious, immigration-adjacent audience, «is this serious, is this a scam» is the second question, not the ninth |
| 4 | **Il passaggio** — the seven phases (§5) | DARK navy, the light | the diptych (2) | how it works, where Morocco ends and Italy begins |
| 5 | **S'orienter** — the orientation band (§3.4) | BRAND gradient | — | the primary action, after the explanation |
| 6 | **Les parcours** — the eight regular routes (§3.4) | NEUTRAL | — | the catalogue |
| 7 | **Forum Vénétie–Maroc** — the dated rendez-vous + the pilot sequence (§3.6) | IMMERSIVE photo band | 1 | the living proof, dated |
| 8 | **L'écosystème** — promoter, partners, services (§3.8) | NEUTRAL bento | 1 | who is behind it |
| 9 | **Actualités** — only when there are articles (§3.8) | NEUTRAL | ≤ 3 covers | freshness |
| 10 | **La porta riservata** — reserved access (§3.8) | BRAND-dark | — | the last door, anticipates the console |
| 11 | Footer — the closing lintel (§3.9) | night | — | closure |

Rhythm: navy · paper · stone · navy · brand · paper · photograph · paper · (paper) · navy · night — the chapters alternate materials instead of repeating paper. Images: **door + 8** (4 doors, 2 diptych, 1 Forum, 1 ecosystem), plus news covers only when news exists. `IMAGERY.md` §7 budgets «door + layer + 9» with a different mix (4 cards, Forum teaser, portico poster, 3 news); this panel trades the V1 «portico» video poster for the diptych (meaning over mood) and adds one ecosystem tile. Reconciliation for the CD (decision D-U12).

### 3.1 Home hero — «La porta»

**Critique.**
- The door is the one memorable object on the site. The composition around it is not premium. At 1440 × 900 there is ≈ 180 px of empty navy above the title and ≈ 150 px below; nothing hints at what follows, so the fold is a wall. The four routes are thin cyan hairlines converging on the key: they read «network, fibre», a tech cliché, more than «four regular ways through one door».
- The H1 is the trademark (phase 3 lock) directly under the lock-up: the name twice, the promise second.
- The secondary CTA «Espace entreprises» (back-office `HomeHero.secondary_cta_*`, not locked) singles out one audience of four in the first viewport, while the legend beside it offers all four. Two competing selectors.
- 8770 interim: a five-line uppercase title plus three exit labels that overlap the photograph. It is a different hero from phase 3: the site changes identity by gate.
- The door's photograph (the owner's Roman fountain façade, opacity .5 on navy — deliberate, `v4/hero.css` l.190: «on navy the original .28 disappears») is read by a first-time visitor as the Trevi fountain, the most famous tourist image of Rome, inside a platform whose editorial rules forbid tourist clichés. It is a locked brand asset (`BRAND_ASSETS.md` §2), so the question is its treatment, not its replacement.
- Mobile (`before_home-8771_390.png`): the door, the name, the promise and two CTAs fill the first viewport; the four-door legend falls below the body text. The reorder «actions before body» is deliberate (`v4/hero.css` l.650–668) and harmless (no focusable content is reordered).
- Static. The entrance choreography was rightly removed (gate A, round 4: it hid painted content); nothing replaced it. The one loop, the 28 s route «current», costs ≈ 30 % of the main thread while the hero is on screen (`MOTION.md` §0.9).

**World-class 2026.** A first screen that states the promise in one line, shows the brand doing something once, makes the four choices its primary interaction, and visibly continues into the next chapter. Composed, not centred in emptiness.

**Moves.**
- **H1 — Composition.** Hero height `min(100svh − header, 820px)`; the copy block anchored to the lower third, not vertically centred; the next chapter peeks ≥ 64 px at 1440 × 900 and ≥ 48 px at 390 × 844 — a fold hint made of content, never a pulsing arrow. Route A.
- **H2 — Name vs promise** (owner decision D-U1). The H1 text and element stay as locked. *Option a (recommended):* the H1 is set as an engraved line (display serif 400, ≈ 32–40 px, tracking +.02 em) and the locked subtitle becomes the display statement (clamp 40 → 64 px; it is already sentence case). The h1 stays first in the outline; the eye goes to the promise. *Option b:* keep as is. (Fading or trimming the header lock-up while the hero is in view is rejected: the lock-up is the logo, `BRAND_ASSETS.md` §1.) Route A.
- **H3 — Routes as light, not wires.** Replace the four hairlines with `MOTION.md` §5.11's composited travelling light: one short glint per route, once every ≈ 8 s, paused off-screen, gone under reduced motion. Each route carries its audience colour only as it leaves its legend row; the key still receives the four routes. Hover or focus on a legend row: that route brightens, the others dim to 40 %, the door's glow re-tints to the route (`21st_hero-public.md`, «Portico V5» (3)). Route A; the existing `home.js` re-anchoring is kept.
- **H4 — Remove the exits** on every variant: they collide with the photograph and, in RTL, sit inside the arch (D8). The eyebrow already carries the three words.
- **H5 — One selector.** The legend becomes *the* first-viewport choice: four 52 px rows, glyph disc + word, the gloss shown in the existing reserved caption slot on hover/focus. The secondary CTA (a back-office field, no lock) no longer ranks audiences: «Forum Vénétie–Maroc · 2 octobre 2026» until the event, then «Comment ça marche» (anchor to the passage) — decision D-U11. The primary stays «Découvrir le questionnaire d'orientation».
- **H6 — Mobile.** Keep the door (compact viewBox) at 180 px wide; below 64rem let `.hero__copy` become `display: contents` (the stage already is) so a single order can read door → title → promise → actions → **legend** → body. The phone's first scroll reaches the four doors. Tab order (actions, then legend links) already matches that visual order. Route A.
- **H7 — The key turns once** on first load, *after* LCP and only if the stage is in view: `MOTION.md` L1 «Porta» at stage scale (1,600 ms, transform and opacity only, rest = the verbatim mark). It is additive: nothing painted is taken back (`MOTION.md` §2.2). Reduced motion: no turn. Route A (WAAPI driven by classes; `MOTION.md` §0.9 says the loader needs no Motion).
- **H8 — Photograph treatment** (owner decision D-U2). Keep opacity .5 (needed on navy) and add a radial navy vignette centred on the key (veil 0 at 30 % radius → .65 at the arch edge), so the statuary reads as stone relief around a dark doorway rather than as the fountain postcard. Zero bytes. Test at 1440 and 390 before any commit. Route A.
- **H9 — Material.** `--mesh-dark` + 3 % grain (exist). IMAGERY's duotone «vault» layer (≤ 24 KB, below the copy's contrast floor, measured) only if the owner signs the home image budget (`IMAGERY.md` §7).
- **Guard.** LCP stays the door photograph (preloaded, 42 KB); nothing in H1–H9 delays it. CLS: the compact viewBox is already reserved (`aspect-ratio`, `v4/hero.css` l.544). Every hover effect has a `:focus-visible` twin.

### 3.2 Letterhead, mega-menu, search — «Il portico si apre» (S2)

**Critique.**
- **IA.** Seven peers — four audiences, Forum, Actualités, Projet — with no grouping. Only Personnes, Entreprises and Projet open a panel; Institutions and Universités & Formation, two of the four doors, are bare links. The doors are unequal in the chrome.
- **Panel** (`before_megamenu-8771_1440.png`). A white sheet the full width of the viewport, square top, rounded bottom, no scrim: the hero stays at full contrast behind it and competes. A title, one line of description, a link; seven sub-links behind identical chevrons. «Attention aux fraudes», a warning, sits between «Formation» and «Glossaire» at the same weight. «Voir l'espace» and «Votre parcours» are the same URL (D11).
- **Behaviour.** It opens on the 44 px chevron button only; hover does nothing (`before_navhover-*`: open on hover = False). Link + separate disclosure button is correct for accessibility, but the pointer user's only way in is a small chevron beside the label.
- **Utilities.** Language and access live in a 32 px institutional bar because seven items fill the header (documented deviation, `utility_bar.html` comment). The «ع» sits below the Latin baseline of «IT FR EN».
- **No search anywhere** (`UI_INVENTORY.md` P38).

**World-class 2026.** The navigation *explains* each door before the click: grouped links with one-line descriptions, one photograph that is the door's own image (the same one the door carries on the home and on its landing), the warning where it belongs, search in the same surface, hover-intent with full keyboard and touch parity, and a page that dims behind the panel.

**Moves.**
- **N1 — IA** (owner decision D-U3; N2 depends on it). Top row = the four doors, equal: `Personnes · Entreprises · Institutions · Universités & Formation`, a hairline separator, then `Forum · Projet`. «Actualités» moves into the Projet panel, and returns to the top row only when there is a publishing cadence. Every door has a panel **with the same anatomy**, or none has one. Minimum per door: «Comprendre» (the landing), «Agir» (the first form: questionnaire / besoins / proposition / collaboration), and «Se préparer» or «Documents» where it exists. Six items plus a separator measure ≈ 780 px (scaled from the 905 px measured for seven in `utility_bar.html`), which still leaves no room for language + access beside a 303 px lock-up in 1,240 px: the utility bar stays, and becomes useful (N6).
- **N2 — Panel anatomy** (V4 CD §3.2 and `21st_nav-shell.md` «Portico panel», built this time). 12 columns, `4 | 5 | 3`:
  - (a) sub-links: glyph (ICON map) + title 15/22 500 + one-line description 13/20 `--ink-2`, 52 px rows, at most six. Needs a `description` field on child `MenuItem` (CMS change).
  - (b) the door's statement: display serif title 22/28, the door's locked gloss (`p3.entrances.*.text`, rendered from the registry, not retyped), and one primary link «Voir l'espace» — the only arrow in the panel.
  - (c) one photograph 3:2 (`IMAGERY.md` §3.18: the door's own image, reused only inside its context). It cross-fades to a sub-link's image on hover/focus only when that sub-link has one.
  - Foot row, full width: **«il gradino»** compact (§4.3) — the anti-fraud step, the same on every panel.
- **N3 — Behaviour.** Hover-intent open after 120 ms, close grace 250 ms, on `(hover: hover)` devices only; click / Enter / Space on the disclosure button and tap on touch. Arrow keys between sections (exists), ↓ into the panel (exists), Esc closes the innermost layer and returns focus (exists). Switching sections never closes the panel: content cross-slides 16 px in the reading direction and the height morphs (`21st_nav-shell.md` #21349 / #31509 mechanics). WCAG 1.4.13: the panel is hoverable, dismissible (Esc) and persistent. Route A + B (Motion `animate` for the height morph, `SPRING_SOFT`).
- **N4 — Surface.** Inset 16 px from the viewport edges, `--radius-xl` on the corners below the bar, L3 shadow; a scrim `--mid-0` at 32 % over the page, animated in opacity only (no animated blur, `MOTION.md` §5.7). The header's bottom hairline continues into the panel top: one surface. Open 200 ms `--ease-enter` (opacity + 8 px + clip from the bar edge), items stagger 30–40 ms (≤ 6), close 120 ms. Reduced motion: 80 ms opacity.
- **N5 — Search inside the portico.** A search button at the end of the header row morphs into a field inside the same panel surface. Index: static JSON per language, built at deploy (title, section, audience, URL; FR/IT accent folding, Arabic normalisation), fetched on first focus. Results grouped by door; the zero-result state offers the four doors and the questionnaire. Route A; needs a build step (dev/owner decision).
- **N6 — The utility bar, made useful.** Promoter (reading edge) · while `forum_banner` is on, the next dated rendez-vous as a quiet link («Forum Vénétie–Maroc · Rovigo, 2 octobre 2026») · «Espace réservé» with `ile-key` · the language control. The bar still collapses on scroll (exists). Language codes stay in the bar, with visually hidden autonyms; «ع» in the Arabic UI face with its own baseline correction (`TYPOGRAPHY.md`).
- **N7 — Active state.** The sliding indicator follows the clicked item and stays there until `pagehide` (`MOTION.md` §5.6): the bar goes where you go.
- **Guard.** Panel photographs are requested on the first hover-intent or focus of the bar, never at load (0 LCP impact), ≤ 30 KB each, AVIF/WebP, `decoding="async"`. `scroll-padding-top` = header height so a focused target is never hidden (2.4.11). Targets ≥ 44 px (WCAG 2.5.8 asks 24 px; ILE's own rule is stricter).

### 3.3 The four doors — audience entrances

**Critique** (`crop_home_entrances_pilot_1440.png`). Folio «01 L'ÉCOSYSTÈME» above four boxes numbered 01–04. Uneven widths (7/5 · 5/7: the deliberate V2 «quay», but it ranks equal doors, D12). Uppercase light-serif locked questions. Faint contour «landform» glyphs no one can decode (a single summit for a person?). The locked CTA words (uppercase, teal) sit apart from their arrow, which floats in the far corner. No image. The template calls these «the most important object on the site» (`components/entrances.html`); they look like a form.

**World-class.** Four equal doors that the eye reads as four *places*, each with its own photograph, glyph and colour, one clear target, and a hover that previews what is behind.

**Moves.**
- **E1 — Four equal panels.** ≥ 1024: one row of four with a 4:5 photograph, or 2 × 2 with 3:2 (the CD chooses); 720–1023: 2 × 2; < 720: a list with 96 px thumbnails. One photograph per door (`IMAGERY.md` §3.2–3.5), never shared. Glyph disc 40 px (ICON map §5.1). The route colour as a 3 px rule on the reading edge (`IMAGERY.md` §5.6 micro-visual; light-surface route tokens are needed, `21st_hero-public.md` decision 4). Locked title, gloss and button verbatim; the button text and its arrow grouped as one.
- **E2 — Progression, not repetition** (§2.1). Under the locked gloss, the door's first two tasks as plain text links (for example Persona: «Commencer le questionnaire», «Voir les huit parcours»; Impresa: «Signaler un besoin», «Le projet pilote»), only to destinations that exist (`safe_url`). Pattern: the title link is the primary target (stretched over the panel); the two task links sit above the stretched layer, each ≥ 44 px; keyboard order title → task 1 → task 2. This replaces the current «the whole panel is one link» rule, deliberately.
- **E3 — Hover and focus.** Photograph scale 1.02 (320 ms), the route rule draws once (480 ms), shadow L1 → L2, a pointer spotlight at 6 % of the accent (V4 CD: the one spotlight of the site). Hero-legend focus ↔ door `is-related` (exists). Reduced motion: none of it.
- **E4 — Retire** the landform glyphs and the ordinals here.
- Route A. Budget: four lazy images with exact `sizes`, ≤ 45 KB each at 960 w.

### 3.4 Pathways and the orientation band

**Critique.** Home pathways: a two-column list of eight, titles smaller than descriptions (D3), descriptions that start lower-case (they are data), arrows pinned to the far end, no glyphs. Orientation: a paragraph with a left rule holding the locked «Comment ça marche : … → … → … → …» — a four-step process typed as arrows inside running text — and a primary button. The home's primary action is explained by a sentence with arrows.

**World-class.** The pathway index is a scannable register with one glyph per pathway (not per audience), a clear title > description hierarchy, and nothing decorative. The orientation is shown as a short, honest sequence beside its button, with its promise limits in plain sight.

**Moves.**
- **P1 — Pathway rows.** Glyph from the ICON map pathway set (`factory` salaried work, `id-card` EU Blue Card, `book-open` training in the country of origin, `backpack` study, `users` family reunification, `store` self-employment, `flask-conical` research, `route` other routes); title 17/24 600; description 15/24 `--ink-2`; the arrow appears on hover/focus only (4 px nudge). No numerals (§2.1). Route A.
- **P2 — «Comment ça marche» as a stepper rendered from the locked string** (decision D-U4). A template filter splits the locked text on «→» into `<li>` items, the way `hero_lines` already splits the H1 without changing a character. The literal «→» stays in the text content (visually hidden span) and a drawn separator replaces it on screen, so the text content remains the locked string character for character; nothing is typed in the template, so `test_templates_static.py` stays green; a new test asserts the equality. Glyphs from ICON map §5.3: `compass` (steps 1–2, one phase), `book-open`, `scroll-text`. Route A.
- **P3 — The orientation band** is the page's one BRAND chapter (V4 CD §3.1.4): `--grad-brand`, the stepper, the primary CTA, the disclaimer line visible. The questionnaire it leads to must receive the «Ma situation» grammar (one question at a time, a stepper, no percentage, focus on the question). Until then the band promises more than the flow delivers.

### 3.5 The passage — the phases

It replaces the pilot band as the home's process chapter. The pilot's locked title and eight steps move to the Forum chapter and the ecosystem pilot landing, rendered verbatim and without sides. Full design in §5.

### 3.6 Forum Vénétie–Maroc — the dated rendez-vous

**Critique** (`before_forum-8771_1440_full.png`). A navy band with an uppercase serif title, one small line of date/place/time and a patronage line; then six text sections with identical left-bar titles. «Objectifs» and «À qui s'adresse-t-il» are enumerations written as one paragraph with semicolons. The programme mixes a time («15h00») with ordinals (02–08). Four grey role cards («Sénateur de la République»…). A navy CTA band with two outline buttons (disabled `span`s when the routes are closed). No image of Rovigo, of the Veneto, of Morocco, of a room or of a table. Nothing tells the visitor the event is in five days. The page title in permanent mode («Forum Permanent Vénétie–Maroc») differs from the nav label («Forum Vénétie–Maroc»). The home banner is gated (`forum_banner`, off on the QA server), and after 2 October a flag flips the whole page to «permanent», with no day-of state and no recap.

**World-class.** An institutional event page: a dated card you can act on (add to calendar, find the place, register or read why not), a programme you scan by time, a tribune of roles that looks like a tribune, one strong photograph of place and one of people at work, and a designed life-cycle: announced → today → held → permanent.

**Moves.**
- **F1 — Event card.** A date block from the model (`event.starts_at`): the day numeral in the display serif, month and year in small capitals, the weekday; the time range; the venue («Sala della Gran Guardia, Rovigo»); the patronage line (locked, verbatim); actions: register (when open) · `.ics` download (generated server-side, same origin) · «Itinéraire» as a plain link to an address page (no embedded map: no remote scripts or frames). The locked meta line stays rendered verbatim; the date block *is* the `<time datetime>` element, so nothing is read twice. Route A.
- **F2 — A state machine, not a flag** (decision D-U5). The page, the home banner and the utility-bar link compute one state server-side from `starts_at` and the gates: `announced` («Dans 5 jours», static text computed at render — never a ticking countdown, which is live-region noise), `today` («Aujourd'hui · 15h00–18h00», venue first), `held` («S'est tenu le 2 octobre 2026», a recap slot for commissioned photographs, outcomes and documents), `permanent` (the existing mode). The transition between states is a date, not a manual flip.
- **F3 — Patronage stays attached to the event.** The Region and the Commune patronise the Forum, not the platform. The patronage line never moves next to the platform's name (home hero, trust chapter): that would read as an endorsement of ILE.
- **F4 — Photography.** `IMAGERY.md` §3.10 (the voice) and §3.11 («la marche», two crafts, one step) for the hero; §3.15 (the plain, 21:9) above the programme; the V2 video «la table est mise» below the fold, desktop, poster-first, with a pause control (`IMAGERY.md` §4.2). Stock is never captioned as the real event (`IMAGERY.md` §2.6).
- **F5 — Programme as a timetable.** A time column only when every row has a time, otherwise ordinals only; never both. No hover (it is a document).
- **F6 — Lists from locked enumerations**, only where the locked text carries a separator that can be split verbatim (the P2 filter on «;»); otherwise the paragraph stays (the lock wins).
- **F7 — Tribune.** Role cards with the actor glyph (`stamp` for authorities, `institution`, `building`) and the role in the serif; names only when authorised (existing rule).
- **F8 — Local navigation.** Sticky under the header, with a travelling marker (IntersectionObserver scroll-spy) and a 2 px reading-progress hairline (`21st_nav-shell.md` «Scroll / reading indicator»). Route A.
- **F9 — No disabled buttons in public.** A closed route shows one sentence of «when», or is absent.

### 3.7 Inner pages — Espace Personnes as the model

**Critique** (`before_parcours-8771_1440_full.png`). A plain page header (uppercase serif H1 whose accented lines touch), a seven-line lead, a rail of text links, the broken anti-fraud box (D1), the list with its inverted hierarchy (D3), a duplicated «Comment ça marche» (D2). Fifty-five public templates open on the same type-only `page_header` (`UI_INVENTORY.md` P13).

**Moves.**
- **I1 — Landing hero** for the four door landings and the Forum: a 4:5 photograph at the inline end (the door's own image, one context), an eyebrow with the door's name and glyph disc, a sentence-case title, a lead of three lines at most, the door's primary action. Other inner pages keep a type header but gain the section grammar (gold hairline + tracked eyebrow + serif title + sans lead) and a 21:9 band where IMAGERY assigns one.
- **I2 — «Sur cette page».** A sticky table of contents ≥ 64rem with a travelling marker, a `<details>` on mobile; a reading-progress hairline on long reads (guides, legal texts, the Forum). Route A.
- **I3 — The rail** becomes: table of contents · «il gradino» compact · related doors. Never again a ≈ 150 px column holding a display-size title.
- **I4 — «The text scrolls, the picture answers»** (`21st_hero-public.md` feature pattern) for the long explanatory landings only (ecosystem companies / institutions / universities, the pilot): at most three photographs, the text never hidden.

### 3.8 Trust, anti-fraud, ecosystem, reserved access, news

- **T1 — Trust.** The «what the platform does / does not do» pair stays: it is the product's honesty, and it moves up to chapter 3 (§3.0). Two columns with a hairline between them; the FAQ quotes as a real Q&A (question 17/24 600 above a 15/24 answer, D3). The jurisdiction bar is redrawn in the phase language of §5: same four segments and textures (its «recognisable device»), the two thresholds marked.
- **T2 — Anti-fraud** becomes «il gradino» at chapter scale (§4.3): a full-width stone band 96–120 px, the three steps of the mark as a quiet line drawing at the reading edge, the locked title and body verbatim, one link. It replaces the large shield panel.
- **T3 — Ecosystem** as a bento (`21st_hero-public.md` «Bento ecosystem»): one photograph tile (cooperation), a promoter tile (name + the locked FAQ answer), three service tiles (Guichet numérique, Academy, company and university spaces), a partners tile that shows names once authorised and, until then, one honest sentence rather than an empty-state illustration.
- **T4 — Reserved access** as a BRAND-dark band that anticipates the console: navy, `ile-key`, the key turning once on hover/focus (`MOTION.md` L2 at 24 px), one secondary button «Connexion». The last door of the page.
- **T5 — News** (owner decision D-U13). Today phase 3 ships the block even when empty (deliberate, `build_news`). This panel recommends hiding it when there is nothing to show; when there are articles, one lead with its cover + two rows (`21st_hero-public.md` «News»).

### 3.9 Footer — the closing lintel

**Critique.** A competent navy four-column footer with no closure, English legal titles without `lang`, a build label (D10), and the anti-fraud as an outline pill — its third treatment.

**Moves.** The columns stay. A closing band with the arch-and-steps outline at 6–8 % on `--mid-0` (`21st_hero-public.md` decision 3; the wordmark at display size only with the owner's sign-off). «Il gradino» compact as the anti-fraud entry. «Contenus vérifiés le …» kept. The build label leaves the public footer. The language control repeated at the foot, where people look for it. Route A, ≈ 1 KB inline sprite.

### 3.10 Mobile drawer

**Critique** (`before_drawer-8771_390.png`). The promoter sentence, the access button and the language control come first and push the navigation to mid-screen. Seven flat rows (three with chevrons), no glyphs, no descriptions. The lower 40 % of the screen is empty. «Menu» sits next to a ×.

**Moves.**
- **M1 — Order.** A compact language row (segmented, autonyms visually hidden) → the four doors (glyph disc + word + one-line description, 64 px rows) → a separator → Forum (with its date) · Projet → a search field → at the foot: «Espace réservé» as a sticky bottom button in the thumb zone, the promoter line, the contact address. (`ref_agami_390_menu-open.png` shows the principle of navigation before utilities, with full autonyms; nothing of its layout is copied.)
- **M2 — Sub-levels** as exclusive `<details name="nav">` whose opened summary stays pinned (`21st_nav-shell.md` drawer); «il gradino» compact inside Personnes.
- **M3 — Native `<dialog>`**, like the console drawer: inert background, focus return; 320 ms from the reading edge; scrim in opacity only.
- **M4 — Label** «Fermer» while open (D9).
- Route A.

### 3.11 Login — the door that opens

**Critique** (`before_login-8771_1440.png`). Clean and generic: the door, static, on the left; a SaaS card on the right. The full public mega-navigation sits above a task page, including an «Espace réservé» link to the page you are already on. «Mot de passe oublié ?» sits 4 px under the field. Nothing says what is inside or how data is protected. On mobile the full door stacks above the form (`CAPTURES_AND_REFERENCES.md` §2); V4 CD §3.3 specified a 120 px navy band with the arch-and-steps glyph below 1024 px, which was not built. (This panel did not re-open the mobile capture; see §12.)

**World-class.** A focused threshold: minimal chrome; the brand's gesture tied to the action (the key turns while you are being let in); crisp busy, error and success states; one sentence of reassurance; «no account yet» and «I need help» paths that do not compete with the primary action.

**Moves.**
- **L1 — Focus letterhead.** On entrance pages the header keeps the lock-up, the language control and «Retour au site»; no mega-menu, no self-link. Route A (a block override in `allauth/layouts/entrance.html`).
- **L2 — The key turns on submit.** The existing `form[data-single-submit]` busy state drives the stage: `MOTION.md` L1 «Porta» at stage scale while the request is in flight (§6.7 D). On error the key returns to rest and the error summary takes focus (exists). On success, 320 ms: the crack of light at the jamb (`MOTION.md` §6.2), then the navigation, which the console's transition takes over. Reduced motion: the busy meter alone (exists). Route A.
- **L3 — Form detail.** «Oublié ?» moves to the end of the password label row; 16 px between each field and its help; the show/hide control stays a labelled text button (exists); `autocomplete` values verified. Passkeys only when the backend offers them (not today, no promise).
- **L4 — Reassurance** (decision D-U6): one line under the button, reusing verbatim the locked FAQ answer on data protection (`faq_data_protection`). No invented badges.
- **L5 — Mobile:** the V4 CD §3.3 band (120 px navy + mesh + arch-and-steps glyph); the e-mail field inside the first viewport at 390 × 844.

---

## 4. Brand, imagery and the arch — this panel's positions

- **4.1 The arch mask.** This panel agrees with `IMAGERY.md` §0.6: the arch shape stays exclusive to the door and the login; no arch windows on cards (it would spend the brand's strongest asset), which also rejects the suggestion in `CAPTURES_AND_REFERENCES.md` §3.3.1. **One exception is proposed** (decision D-U7): the arch as a *motion*, once per page, at a threshold — either the hero exit («the portico opens», `21st_hero-public.md`) or the passage's arrival threshold (§5.2), never both on one page. The panel prefers the arrival threshold, because there the shape means what it says (passing the door) instead of decorating a scroll.
- **4.2 One image, one context** (`IMAGERY.md` §2.2) is also a UX rule. Persona's image is the same on the home door, in the Persona mega-panel and on the Persona landing: recognition by repetition *inside* a context. No image crosses two contexts.
- **4.3 «Il gradino» — the anti-fraud step** (decision D-U8). The mark's three steps say «the path has steps; none can be skipped». The anti-fraud message says «nobody can sell you a shortcut». It is the same idea, so it gets the same drawing. One component, three sizes: a chapter band on the home, the foot row of every mega-panel, a compact block in rails and in the drawer. Always: the steps as a line drawing taken from the mark's own geometry (not a new icon, never the full door), the locked `p3.antifraud.title` (and body where there is room), one link. It replaces the four current treatments (home panel, pathways callout, footer pill, panel link) and closes D1.
- **4.4 The key** is the brand's action. It turns in waits (`MOTION.md` §6), it opens the reserved area (`ile-key`), it is never a decorative sparkle, never a loop on `filter`, never an overshoot (`BRAND_ASSETS.md` §2).
- **4.5 The tricolour** stays in the mark only (`BRAND_ASSETS.md` §1; `COLOUR.md` §0.6). Italy and Morocco are told through photographs of what they share (`IMAGERY.md` «due portici»), never through flags, green-white-red rules or a red star.
- **4.6 The door's photograph** — a treatment question (§3.1 H8, D-U2), not a replacement.

---

## 5. Phase transitions — «Una porta, due rive»

### 5.1 One sequence, four renderings → one grammar

Every public picture of «before / at / after the crossing» uses one grammar:
- **Two shores as places, not flags.** The diptych opens the chapter — Casablanca's arcade at the reading start, Padua's at the reading end, shown together, same ratio and grade, never split (`IMAGERY.md` §3.13–3.14 «only paired»; this moves or extends the diptych's context from the regular-mobility pathway page to the passage — the same message; IMAGERY to confirm). The line runs beneath the pair from one photograph to the other.
- **One line, one light.** `MOTION.md` §7's light lays the line as the reader scrolls; the whole line is always visible at low contrast (the light adds, never withholds — D5).
- **Seven stations with phase glyphs** (ICON map §5.3): `compass` (steps 1–2), `book-open`, `scroll-text`, `clipboard-check`, `ile-arch`, `sprout`.
- **Numbers only here** (§2.1): 1–7.

### 5.2 Two thresholds, not one — the semantic fix

- **Threshold A — «Les autorités compétentes».** Between step 3 («Préparation et formation avant le départ») and step 4 («Procédures auprès des autorités compétentes»), where `JOURNEY_STEPS` switches side: a vertical hairline with the `stamp` glyph and a short caption («Chaque décision appartient aux autorités.», reusable verbatim from the locked FAQ `faq_preassessment_guarantee`). The jurisdiction changes; the person has not moved. Recommendation to the ICON lane: `ile-crossing` should not mark this point (it says «you crossed»); use `stamp`, and keep `ile-crossing` for threshold B or retire it in favour of `ile-arch`.
- **Threshold B — «L'arrivée».** Before step 6 («Arrivée et premières démarches»): the brand's door, as the `ile-arch` glyph at station scale; and, if D-U7 is signed, the page's one arch-shaped motion: the Padua photograph, already visible inside an arch-shaped window, opens to its full frame as the light reaches the threshold (additive: the image is visible from the first frame). This is the only place in the story where the door appears outside the hero, and it appears where it means something.
- **Guardrails.** The passage never implies an outcome: no check marks on stations (`COLOUR.md` §0.4: no colour means approved), no «vous êtes arrivé», and the locked line «Aucun résultat administratif n'est promis ni garanti» (end of `p3.persons.how_it_works`) visible under the chapter title.
- **Legal decision D-U9.** Publishing the seven `JOURNEY_STEPS` labels and their sides on the public home. They are `gettext` labels, not locked registry text, but their public use is an editorial claim about the regular pathway and must be signed. Until it is, the chapter renders the locked four-step orientation sequence (P2) without sides and without thresholds — still one line, one light, the diptych.

### 5.3 Portico ↔ console continuity

The home's passage and the console's JourneyRail are the same seven stations, glyphs and thresholds. A person who reads the home and then signs in finds their dossier on the line they have already seen: their step lit, the light stopping at it (`MOTION.md` §7, console rail). This is the strongest «coherent public site and platform» move available, and it needs no new data.

### 5.4 RTL

The passage is a sequence, not a map (the council refused maps), so it mirrors: step 1 at the reading edge (the right in `ar`), the light running right → left, Morocco's arcade at the right. `MOTION.md` §7's prototype already does this. This panel therefore disagrees with `21st_hero-public.md` decision 6 («keep the path unmirrored so the Morocco→Italy geography stays true»): without a map there is no geography to keep true, and reading order is what the reader needs. The mark, the door and the photographs never mirror.

### 5.5 The site's own phases, as designed transitions

- **Interim ↔ phase 3.** One hero composition for both; only the locked words change (interim title and fragment vs trademark and promise). No variant-only furniture (the exits go, H4).
- **Forum.** `announced → today → held → permanent`, computed from dates (§3.6 F2); the home banner and the utility-bar link follow the same states.
- **Gate-closed destinations.** When a door's destination is not public yet, the door stays, with its sentence of «when» (`components/entrances.html`: «the destination changes, not the presence»); never a disabled button.

---

## 6. Loading, waits and page change — the public contract

(Mechanics and numbers belong to `MOTION.md`; this is what the visitor must experience.)

| Moment | Today | V5 |
|---|---|---|
| First frame, home | cream sheet, fallback wordmark, no mark, one nav label | the navy chapter painted from the first frame: `body.page-home` (a server class) carries a background of `--mid-1` for the first `100svh` and paper after it (a hard-stop gradient; verify that no section relies on a transparent background over the body); the mark inline in the lock-up (≈ 1 KB SVG, as on the legacy site, `BRAND_ASSETS.md` §1) so it paints with the HTML; the wordmark from the 1.7 KB subset (`TYPOGRAPHY.md` §7 A1) |
| Nav labels | pop in one by one | the list painted in one piece; reserved inline sizes if a trace shows the stepping persists; CLS verified on 8772 |
| Door photograph | arrives ≈ 1.2 s after first paint (8771) | preloaded (exists); the arch body gradient of the same geometry already painted (exists) — keep |
| Click → next page | the old page frozen for 2–4 s | the thread «la soglia» from 400 ms (`MOTION.md` §6.3 S) + public-only View Transitions of 120–180 ms (`MOTION.md` §5.5: +90 ms on the destination's LCP, passes the 100 ms gate by 10 ms — re-measure after shortening) |
| Mega-panel photograph | — | fetched on first hover-intent; the panel never waits for it (fixed slot, paper ground) |
| Any public form | busy state only on allauth forms | `data-single-submit` on every public form; L2 «Chiave» in the button (`MOTION.md` §6.3); focus on the error summary (exists) |
| Questionnaire step | full reload + percentage bar | the «Ma situation» grammar; a View Transition between steps where supported (to verify for POST → redirect → GET); focus on the question |
| Search results | — | a reserved-height region; the L3 «Luce» skeleton after 120 ms for at least 380 ms (`21st_nav-shell.md` #23557 rules) |
| Empty sections | «Aucune actualité…», «Les partenaires…» | hidden (news, D-U13) or written as honest content (partners) |
| Error pages | text, e-mail, back | the door at rest with the key out of the lock (static), the message, three ways back (home, the four doors, contact) |

Never: a full-screen loader or curtain, an entrance that hides painted content, a ticking countdown.

---

## 7. Accessibility and RTL — requirements for every move above

- **Keyboard and focus.** Every hover effect has a `:focus-visible` twin. The mega-panel keeps the disclosure model (buttons with `aria-expanded` / `aria-controls`, never `role="menu"`). Drawer and search in native `<dialog>`. `scroll-padding-top` = the sticky header's height (2.4.11). One focus ring (`COLOUR.md` §9), two-tone on photographs.
- **Targets** ≥ 44 px, including the task links inside the door panels (E2).
- **1.4.13.** Hover panels are dismissible (Esc), hoverable and persistent. No information only on hover: the doors always show their gloss; the hero caption slot duplicates, never replaces.
- **2.2.2.** Every loop (hero light, videos) can be paused or lasts ≤ 5 s; videos carry a visible pause control and `<track>` captions, and show their poster under reduced motion and Save-Data (`IMAGERY.md` §4.4).
- **Reduced motion.** A complete still state for every move (`MOTION.md` §2.5): the passage fully drawn, the key at rest, no View Transition.
- **Language of parts (3.1.2).** `lang` on every fallback string (the French fragment in the Arabic hero, D6), on «Privacy Policy» / «Cookie Policy» (D10), and on Latin place names inside Arabic labels. The trademark keeps `lang="en" dir="ltr" translate="no"` (exists).
- **Arabic (`/ar/`).** Arabic display and UI faces per `TYPOGRAPHY.md` §6.2 / §8.6; no uppercase, tracking or italic (the Forum quote's italic becomes roman in `ar`); small text one step larger; only directional icons flip (`icon--flip-rtl`), never the mark or the door; mega-panel columns mirror (the photograph moves to the left), the cross-slide flips, the drawer comes from the right, the thread starts at the right, the passage mirrors (§5.4). Digits: Latin digits for dates and times, consistently, unless the owner chooses otherwise (D-U10).
- **Translation debt visible in `ar`.** The nav label «منتدى Vénétie–Maroc» keeps French place names inside an Arabic label; the interim hero fragment is French (D6). This is content work that must come before visual work. The V5 gate includes an `ar` pass on every public template.
- **Text on photographs.** Never on busy pixels (`IMAGERY.md` §5.4); captions beneath; glass plates measured at the worst composite.

---

## 8. Classification of every pattern proposed here

| Pattern | Route | Mechanics from | Notes |
|---|---|---|---|
| Hero composition, engraved H1, legend as the selector, vignette, exits removed | A | — | CSS + template |
| Hero travelling light; the key turns once | A | `MOTION.md` §5.11, §6 | WAAPI driven by classes, no Motion |
| Mega-panel open / close, stagger, scrim | A | `21st_nav-shell.md` #31723 surface, #31509 timings | CSS |
| Mega-panel section switch (cross-slide + height morph) | B | #21349 direction-aware swap | Motion `animate`, `SPRING_SOFT` |
| Public search inside the panel | A | #31184 gesture, #11338 ARIA, #29989 zero state | static JSON per language |
| Four doors: photograph, spotlight, route rule, task links | A | #27010 (softened), #26797 spotlight | ≈ 10 lines of vanilla `pointermove` |
| Pathway rows; stepper from a locked string | A | — | template filter + equality test |
| The passage: line, light, stations, two thresholds | A | `MOTION.md` §7 (native scroll-driven CSS) | Motion `scroll()` only where `animation-timeline` is unsupported (B) |
| Arch-shaped opening at the arrival threshold | A | `21st_hero-public.md` #10905 «portico-reveal» | D-U7 |
| Forum event card, state machine, `.ics` | A | #25369 grammar | state computed server-side |
| Forum programme, tribune, gallery | A | #10098 magazine list, #27093 filmstrip mechanics | native `<dialog>` lightbox |
| Table of contents + reading progress | A | #18113, scroll-driven CSS | |
| Drawer on `<dialog>` with pinned `<details>` | A | #29334 focus model, #22313 layout only | |
| Login focus letterhead; the key turns on submit | A | `MOTION.md` §6.7 D | |
| View Transitions (public) + the thread | A | `MOTION.md` §5.5 | behind the measured gate |
| Footer closing band | A | #29773 | |
| React islands | **C — none** | — | nothing here justifies one |
| Rejected | **D** | — | full-screen loader or curtain (agamieuromed.org's ~1 s threshold), opacity-0-until-JS entrances (studiobadrane.com's AOS), WebGL/shader heroes, carousels or video in the hero, cursor-following image previews, floating CTAs and chat bubbles, marquees, ticking countdowns, invented statistics strips, logo walls, arch windows on cards, hover-only content, flags / maps / planes / luggage imagery |

This panel made **no 21st.dev call**; the component ids are those already retrieved and read by the curation lanes (`21st_hero-public.md`, `21st_nav-shell.md`). `generate` and `iterate_generation` were not called.

---

## 9. Priorities and acceptance

- **P0 — before any V5 styling (defects and honesty).** D1, D2, D3, D4, D5, D9, D10 (`lang`), D11; `lang` on the Arabic fragment (D6). Acceptance: each page re-captured at 1440 and 390 in `fr` and `ar`, axe clean, no CLS change.
- **P1 — the V5 public spine.** S1 home chapters (§3.0–3.4 and §5, behind D-U9 or with the locked fallback), S2 mega-menu and drawer (behind D-U3 and the CMS `description` / `image` fields), S3 first-frame contract + thread + public View Transitions, S5 «il gradino», the Forum states (§3.6). **The Forum states only help the event if they ship before 2 October**; otherwise build them for the `held` state.
- **P2 — depth.** Landing heroes (§3.7), search (N5), footer closure, the login key, videos, error pages.

**Gates for every item** (budget approved by the owner): LCP ≤ 2.5 s, CLS ≤ 0.10, INP ≤ 200 ms on 8772 under slow 4G + CPU ×4; no added long task > 50 ms; the reduced-motion still state captured; an `ar` pass; a keyboard walk-through; a full-page re-probe of every page a shared sheet touches.

---

## 10. Decisions for the owner

| # | Decision | Panel recommendation |
|---|---|---|
| D-U1 | Hero: which reads first, the trademark H1 or the promise | Option a: engraved H1, the promise as the display line; lock untouched |
| D-U2 | Treatment of the door's photograph (read as the Trevi postcard) | Keep the photograph; add the key-centred vignette; test |
| D-U3 | IA: six top items (four doors + Forum + Projet), equal panels for the four doors, Actualités inside Projet | Yes |
| D-U4 | Render locked «→» and «;» sequences as lists by splitting the locked string verbatim | Yes, with a test that the text content equals the locked string |
| D-U5 | Forum states announced / today / held / permanent, from dates | Yes; the `held` state needs commissioned photographs |
| D-U6 | One reassurance line on the login (the locked FAQ answer on data) | Yes |
| D-U7 | An arch-shaped motion outside hero and login, once per page, at a threshold | Only at the passage's arrival threshold |
| D-U8 | «Il gradino»: the mark's steps as the anti-fraud component | Yes |
| D-U9 | Publish the seven `JOURNEY_STEPS` and their sides on the home (legal) | Yes after legal review; the locked four-step fallback until then |
| D-U10 | Digits on Arabic pages | Latin digits, consistently |
| D-U11 | Hero secondary CTA (back-office): replace «Espace entreprises» | The Forum date until 2 October, then «Comment ça marche» |
| D-U12 | Home image budget: door + 8 (this panel) vs door + layer + 9 (IMAGERY) | Door + 8, all lazy below the fold; measure |
| D-U13 | Ship an empty News block in phase 3, or hide it | Hide it until there are articles |

---

## 11. Captures and references read by this panel

Read one at a time: **15 capture PNGs + 2 crops cut from one of them** (`before_home-8771_1440_full.png`) = 17 image reads. **That is one over the cap of 16** if the crops count as reads (they are derived from an already-read capture; reported rather than hidden). Every capture is listed and described in `CAPTURES_AND_REFERENCES.md` §4; the crops are new.

| # | File (under `C:/tmp/ile_v5_council/`) | Used for |
|---|---|---|
| 1 | `captures/before_home-8771_1440.png` | hero, phase 3 |
| 2 | `captures/before_home-8771_1440_full.png` | home rhythm and sections |
| 3 | `captures/before_megamenu-8771_1440.png` | the panel |
| 4 | `captures/before_home-8771_390.png` | mobile hero |
| 5 | `captures/before_drawer-8771_390.png` | drawer |
| 6 | `captures/before_parcours-8771_1440_full.png` | inner page, D1–D3 |
| 7 | `captures/before_forum-8771_1440_full.png` | Forum |
| 8 | `captures/before_login-8771_1440.png` | login |
| 9 | `captures/before_home-8770_1440.png` | interim hero |
| 10 | `captures/before_loading-home-8772gzip_1440_fp+0250ms.png` | first frame |
| 11 | `captures/typography/before_ar_home_1440.png` | RTL (interim) |
| 12 | `captures/ref_agami_1440_nav02_international-cooperatio_hover.png` | mega-menu principles |
| 13 | `captures/ref_studiobadrane_1440_01_first-viewport.png` | hero principles |
| 14 | `captures/ref_agami_390_menu-open.png` | drawer principles |
| 15 | `captures/before_home-8771_390_full.png` | mobile length |
| 16 | `scratch/ux_public/crop_home_entrances_pilot_1440.png` (y 780–1850 + 2630–3020 of #2) | doors, pathways |
| 17 | `scratch/ux_public/crop_home_pilot_trust_1440.png` (y 3400–4190 + 4200–4700 of #2) | pilot band, trust |

**Correction to `CAPTURES_AND_REFERENCES.md` §2.** It describes `before_home-8771_1440.png` as showing the long title «UN ÉCOSYSTÈME POUR LES PARCOURS RÉGULIERS VERS L'ITALIE» and says the 8770 interim hero is «text only with the wordmark as title, no arch». The captures show the reverse: 8771 (phase 3) has the trademark H1 «ITALY LEGAL ENTRY™» with the door and the legend; 8770 (interim) has the long uppercase title, the door, the legend and three exit labels. Both have the door. Also, the 8771 mega-menu shows seven sub-links, not «a single link».

**Reference principles used** (never a layout or an element). agamieuromed.org: a grouped mega-panel with a featured image over a dimmed page; a drawer that puts navigation before utilities and names languages by their autonyms. studiobadrane.com: a photographic hero; the next band peeking into the first viewport. Refused from both: the full-screen loader, opacity-0-until-JS text, floating CTAs, remote fonts, legal clichés, readable third-party text in photographs.

---

## 12. What this panel did not do, and why

- **One reviewer, five chairs.** Institutional UX, IA, brand, accessibility and RTL were held by one agent: no second reader, no user test, no native Arabic reader. The scores in §1 are one judgement.
- **No live browser pass.** Findings come from the 26 September captures and from the templates and CSS read at `c9a58d8`. The causes given for D1, D3, D4 and D5 are read, not measured. The only live requests were GETs of `/fr/` on the three local QA servers (size only). No form was touched, no password typed, no sign-in made, nothing in production.
- **Not re-viewed as images** (the cap): the mobile login, the Forum at 390, the drawer's sub-level, the other loading frames, the orientation questionnaire, the ecosystem landings, and the news, living, FAQ and glossary pages. They are cited from `CAPTURES_AND_REFERENCES.md` and `UI_INVENTORY.md`.
- **Arabic judged on one interim capture** (`typography/before_ar_home_1440.png`); no phase-3 `ar` capture was read.
- **No 21st.dev and no Pexels calls** by this panel; the curation and imagery lanes made them. `generate` / `iterate_generation` were never called.
- **No accessibility tooling** (axe, a screen reader) was run; the accessibility items are design requirements plus defects visible in the markup or the captures.
- **Legal and editorial proposals** (D-U4, D-U9, the threshold captions) are proposals only; the lock owner and the legal reviewer decide.
- **The image cap was exceeded by one read** if the crops count (§11).
