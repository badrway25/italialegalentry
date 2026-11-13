# UI INVENTORY — Italy Legal Entry™ (public site + authenticated platform)

**Role:** UI Inventory Engineer, V5 council · **Date:** 26 Sept 2026 · **Repository:** `C:/tmp/italylegalentry`, branch `main` @ `df8dc42` **plus the uncommitted working tree** (36 modified files; `static/css/dist/`, `static/brand/v2/doorway-arch-400.webp`, `scripts/build_css.mjs` untracked). Read-only: no file of the repository was modified.

## 0. Method, scope and limits

| Item | What was done | What was NOT done (and why) |
|---|---|---|
| Templates | Read every file under `templates/` (218 `.html`): components, partials, pages + home sections, portal, cases, documents, companies, selection, helpdesk, academy, forum (public + governance), ecosystem, pathways, news, living, FAQ, glossary, enquiries, orientation, allauth, errors, legal, `dev/showcase.html`. `apps/*/templates` holds only one e-mail `.txt`. | No page was rendered, no browser driven, no server called: this role is a static inventory. Defects marked **to verify** are inferred from markup + CSS only. |
| CSS | 22 source sheets under `static/css/` (dist excluded) + 12 app sheets under `apps/*/static/`. Every class used in templates mapped by script to its BEM block → template files → defining sheets; CSS blocks with no markup listed. | Computed styles, contrast and layout were not measured. |
| JS | `static/js/main.js`, `head.js`, `rail-pref.js`, `static/js/src/{shell,home,console,situation,motion}.js`, `apps/pages/static/pages/js/home.js`, `apps/orientation/static/orientation/wizard.js`. Bundle sizes measured on `dist/`. | — |
| Icons / images / fonts | `static/img/icons.svg` (36 symbols) against every `{% svg_icon %}` call **and** every Python mapping that chooses an icon (portal nav, actor glyphs, pathways, living topics, pages content, company nav, chips); `static/img/photos/manifest.json` (15 photos) against every slot consumer; `static/brand/**`, `static/img/*`; `static/fonts` + `fonts.css` + font tokens + every `font-family` declaration. | DB-driven images (news, forum, partners, pathways, CMS logo, HomeHero) cannot be enumerated without the database: listed by model field, not by file. |
| Counts | "Where used" = number of **template files** that include/use the element (grep), not runtime instances. `≈` = approximate. `dev/showcase.html` is excluded from counts unless it is the only user. | — |

**Status vocabulary** used in every table: **V4** (built in the current direction) · **V2/V3** (older layer, still live, re-valued only through V4 tokens) · **V1** (first component library, `components.css`) · **PARTIAL** · **SHOWCASE-ONLY** (exists, used only by `/_design/`) · **DEAD** (exists, used nowhere) · **ABSENT**. **Flag** column: ★ = flagship (navbar, hero, loader, app shell, person dashboard, documents, case file, journey, login).

---

## 1. Architecture snapshot

### 1.1 Shells

| Shell | Template(s) | Pages (templates) | Chrome | Footer | CSS loaded | JS loaded |
|---|---|---|---|---|---|---|
| **Public «portico»** | `base.html` + `partials/{utility_bar,header,main_nav,footer,seo_head}.html` | 61: home, institutional (project, AGAMI, network, antifraud, contact), pathways ×5, ecosystem ×4, forum ×3, news ×2, living ×3, FAQ, glossary ×2, enquiries ×4, orientation ×5, legal, errors ×6, partners, community ×9, consents ×2, **account profile / delete / done**, plus `pages/institutional_base.html`, `dev/showcase.html`, `portal/unavailable.html`, `forum/governance/unavailable.html` | utility bar 32 px + header 64→56 px glass + mega-menu (≥ 80rem) / drawer (< 80rem) | 4-column navy footer | `css/dist/main.css` (+ page sheet: `pages.css`, `ecosystem.css`, `forum.css`, `orientation/wizard.css`) | `head.js`, `main.js`, `dist/shell.js` (+ page module) |
| **Entrance** (login, signup, reset, verification) | `allauth/layouts/entrance.html` + `allauth/elements/*` | allauth entrance pages | public chrome + split screen: dark stage with the door / focus sheet 480 px | public | + `accounts/entrance.css` | shell.js (password toggle, busy button) |
| **Account manage** (e-mail, password, MFA) | `allauth/layouts/manage.html` → `allauth/layouts/base.html` | allauth manage pages | public chrome + `layout-sidebar` + `local-nav` | public | main.css only | main.js, shell.js |
| **Console** (platform) | `portal/base_portal.html` + `partials/portal_chrome.html` + `portal/partials/rail_nav.html` | 51 (incl. 4 section bases): portal ×9, cases ×3, documents ×4, companies ×8, selection ×4, helpdesk ×6, academy ×6, forum governance ×11 | rail 64/248 px + context bar 56 px glass; < 64rem bottom bar + `<dialog>` drawer | 4-line portal footer | + `portal/portal.css` + `portal/console.css` (+ `documents.css`, `companies.css`, `selection.css`, `helpdesk.css`, `academy.css`) | `rail-pref.js` (blocking), main.js, shell.js, `dist/console.js` (+ `dist/situation.js`) |
| Errors | `errors/base_error.html` → base.html | 6 | public | public | main.css | main.js |
| Dev showcase | `dev/showcase.html` at `/_design/` (DEBUG only) | 1 | public | public | + `dev/showcase.css` | — |
| Admin (staff) | Django Unfold; `admin/index.html` (Tailwind utility classes), `admin/rules/legalrule/{diff,preview}.html` | 3 | Unfold | — | Unfold | — |

**Coherence note:** four authenticated surfaces live in the PUBLIC shell, not the console: `accounts/profile.html`, `accounts/delete_request.html`, the allauth manage pages, and the whole Virtual Forum `community/*` (9 pages). `admin/rules/legalrule/preview.html` carries an inline `style=""` attribute (staff only, but relevant to the CSP rule).

### 1.2 CSS — the cascade as shipped (one bundle, five generations stacked)

| # | Sheet | Lines | Generation | Holds |
|---|---|---|---|---|
| 1 | `fonts.css` | 267 | — | 26 `@font-face` (§8) |
| 2 | `tokens.css` | 308 | V1 «2026» | first tokens (still names Fira Sans / Fira Mono) |
| 3 | `_legacy-tokens.css` | 338 | V1 | demolition scaffold: `--font-size-*`, `.text-*` utilities |
| 4 | `base.css` | 597 | V1 | reset, `.t-*` type utilities, skip-link, visually-hidden |
| 5 | `layout.css` | 392 | V1 | container, grid-auto, stack, cluster, layout-sidebar, split; `.zones`, `col-*` (dead) |
| 6 | `components.css` | 3 099 | V1 | header / nav / mega-menu / drawer, `.lang-switcher` (dead), account-menu, generic `.hero`, page-header, card, cta-panel, notice, badge, forms, alert, dialog, tabs, accordion, stepper, timeline, pagination, breadcrumbs, az-index, search-form, section-nav, related-links, error-page, `.reveal` |
| 7 | `register.css` | 919 | V2 «graphic language» | folio, register/entry, sequence, jurisdiction bar, `.plate` (dead), note / gloss / sources / outcome, empty |
| 8–12 | `v2/{tokens,bridge,shell,routes,voyage}.css` | 1 208 | V2 | lock-up, utility bar, header, drawer, footer; entrances as routes; home pilot voyage |
| 13–14 | `v3/{buttons,chip}.css` | 974 | V3 | buttons (variants, sizes, icon), chip/state/badge by `data-register` |
| 15–20 | `v4/{tokens,buttons,shell,workspace,hero,wizard}.css` | 4 778 | **V4** | V4 values under V2 names; primary gradient + busy meter; header / nav / mega-menu / drawer / lang-seg / account menu; console workspace; home hero; «Ma situation» wizard |
| app | `pages.css` 811 · `portal.css` 831 · `console.css` 770 · `ecosystem.css` 453 · `selection.css` 345 · `documents.css` 339 · `entrance.css` 262 · `companies.css` 231 · `helpdesk.css` 229 · `forum.css` 200 · `academy.css` 143 · `orientation/wizard.css` 107 | 4 721 | console + entrance = V4; portal, helpdesk, selection, academy, companies, forum, ecosystem, pages, orientation = V2 register language | page-scoped |

Bundle `static/css/dist/main.css`: 217 KB raw / **36 KB gzip**. Stacking examples: `.btn` is styled in **11** sheets, `.site-header` in 6, `.hero` in 6, `.form-field` in 6, `.notice` in 3.

### 1.3 JavaScript

| Module | Loaded on | Size | Behaviours (data-hooks) | Dead / inert parts |
|---|---|---|---|---|
| `head.js` | every page, sync in `<head>` | 3 lines | `no-js` → `js` | — |
| `main.js` (ES module, not bundled) | every page | 551 lines | form-error summary focus; nav drawer + mega-menu full keyboard model (`data-nav-*`); `<details data-dropdown>` (Escape, outside click); accordion single (`data-accordion`); tabs (`data-tabs`); `.reveal` IntersectionObserver; `<dialog>` (`data-dialog-*`); `data-history-back`; `form[data-single-submit]` disable | `initSteppers` (`data-stepper`: no template), `initCounters` (`data-counter`: none), section-nav marker (`data-section-nav`: none); tabs / dialog / accordion-single hooks used only by the showcase |
| `dist/shell.js` (esbuild + Motion) | every page | 3.4 KB | header `is-scrolled` (24 px sentinel), `is-over-dark`, sliding nav indicator (`SPRING_SNAPPY`), password show/hide (`data-password-toggle`), busy button (`is-busy`), `[data-reveal]` Motion `inView` reveals | `[data-reveal]` used only by the home pilot stations |
| `dist/home.js` | home | 4.3 KB | route re-anchoring to legend rows (ResizeObserver), scroll-linked photo drift 18 px + stage scale .96 / opacity .6 (ScrollTimeline), pause the current off-screen / hidden tab, legend → route lighting + caption slot, voyage line drawn with scroll | — |
| `pages/js/home.js` | home | 41 lines | dismissible forum banner (`data-dismissible`, sessionStorage) | — |
| `rail-pref.js` | console, blocking at top of body | 17 lines | stored rail state applied before first paint (CLS guard) | — |
| `dist/console.js` | console | 4.3 KB | rail collapse + localStorage, collapsed-rail tooltip, rail ↑/↓/Home/End, document register search (`data-doc-search`, debounced live count), doc-row popover placement, sticky context bar (`data-ctx` / `data-ctx-bar`), console `<dialog>` drawer | — |
| `dist/situation.js` | «Ma situation» | 2.5 KB | one question at a time, Précédent / Continuer, stepper sync, hash deep-links, 120/200 ms swap | imports `animate` from `"motion"` directly, bypassing `motion.js` («the one place this project imports Motion from») and its `reducedMotion()` helper (it reads the media query itself) |
| `orientation/wizard.js` | public orientation wizard | 26 lines | print button reveal; focus after `htmx:afterSwap` | **htmx is not loaded anywhere**: the `hx-post` attributes in `orientation/_step.html` are inert; each step is a full-page POST |
| Motion chunk | shared | 70 KB raw / 26 KB gz | `motion.js` re-exports `animate, scroll, inView, stagger, spring, hover, press`; `SPRING_SOFT {260,30}`, `SPRING_SNAPPY {400,40}`, `withMotion`, `reducedMotion` | `hover`, `press`, `SPRING_SOFT` exported, used by no module |

---

## 2. Flagship components — verdicts at a glance

| ★ Flagship | Status | Where | Main quality notes (static reading) |
|---|---|---|---|
| **Navbar** (utility bar + header + mega-menu + drawer + language + access) | V4 | every public page (61 + entrance + manage) | Solid engineering: full keyboard model incl. RTL arrows, focus trap, drawer placed under the real header edge, 44 px targets, glass on scroll, spring indicator. Visually **text-only**: mega-menu panels = title + description + link list, no image, no featured item (CD V4 §5.6 planned 1 photo per panel — "third column" still an owner decision). Language + access forced onto the 32 px institutional bar (7 CMS sections + 303 px lock-up fill the 1240 px row — documented deviation). |
| **Hero** (home) | V4 | `pages/home/_hero.html`, home only | Strongest identity object: navy mesh + 3 % grain, the owner's door (arch, photo, golden key, three steps) with 4 audience routes braided through the inner arch, glass legend of 4 links, ambient 28 s current, scroll-linked drift. Entrance choreography removed (gate A r4, defect 11) → static on load. The only hero of the site: every other public page opens on a plain `page-header` (no image, no stage). |
| **Loader** | **ABSENT** | — | No page loader, no skeleton, no top progress bar, no View Transitions. Only loading state: 3-notch **busy meter** on submit buttons of `form[data-single-submit]` (only allauth forms carry the attribute). `.is-pending` chip state defined in `v3/chip.css`, unused. |
| **App shell** (rail + context bar + bottom bar + drawer) | V4 | all 51 console templates | Navy rail, grouped (Parcours / Dossier / Échanges / Academy / Mon rôle), collapsible + persisted + tooltip when collapsed; glass context bar with breadcrumb + «Site public» + account + language; mobile bottom bar (4 + Menu) and `<dialog>` drawer. Page-enter motion built then removed. Shell is V4 but **≈ 40 of the 51 pages inside it are still V2 register pages** (§4). |
| **Person dashboard** | V4 | `portal/dashboard.html` | ContextHeader (name, title, ref, chip, since, one primary) + 8/4 «Prochaine étape» (L2 panel, gradient edge, ResponsibilityBar) / «Dossier» facts + 5-notch meter; JourneyRail; documents (HealthStrip + 3 compact rows + latest deposits); dates; threads; Academy; account. No KPI tiles (policy). Non-person accounts fall back to the V1/V2 `portal-card` grid ("bridge"). |
| **Documents** | V4 register + V2 detail/upload | `portal/documents.html`, `documents/index.html` (shared `documents/partials/register.html`); `documents/requirement_detail.html`, `upload.html`, `terms_required.html` | Register = HealthStrip + SegmentedControl (filter in URL) + live search + DocumentRow (7 zones, stacks as card < 48rem) + popover row menu + V4 files table. Upload = plain `<input type=file>` in a V1 form field: **no dropzone, no progress, no preview** (DS V4 #26 «Upload flagship» not built). |
| **Case file** | V4 detail + V2 index/assessment | `cases/detail.html` | 8/4 workspace: descriptive JourneyRail, next step, checklist table + HealthStrip, actors, staff transition form; inspector: case timeline (last node lights once), assessment, threads, dates; sticky compact glass ctx-bar; mobile sticky action bar. `cases/index.html` (register rows) and `cases/assessment.html` remain V2. |
| **Journey** | PARTIAL | JourneyRail (dashboard, case); `wstep` stepper («Ma situation»); public orientation wizard; home 4-step `sequence` | Four unrelated renderings of «where am I»: V4 JourneyRail (7 locked steps, MA→IT frontier, draws once); V4 `wstep`; the public orientation wizard (`orientation/wizard.css`) with a **percentage progress bar** and inert htmx; `components/stepper.html` (native `<progress>`) SHOWCASE-ONLY. |
| **Login** | V4 | `allauth/layouts/entrance.html` | Split stage: the door (cropped viewBox) on navy + help line; focus sheet 480 px; password show/hide; busy button. Public letterhead kept above. Door static. allauth `alert` element always shows the `info` icon whatever its level. |

---

## 3. PUBLIC SITE — components and patterns

| # | Component / pattern | Status | Template(s) | CSS selectors · sheet(s) | JS | Where used (≈) | Role | Quality notes | Flag |
|---|---|---|---|---|---|---|---|---|---|
| P1 | Institutional utility bar | V4 | `partials/utility_bar.html` | `.utility-bar__*` · base, components, v2/shell, **v4/shell** | — | every public page | promoter identity + account/login + language | 32 px, hidden < md (content moves into the drawer). Text-only; carries language + access by deviation. | ★ |
| P2 | Header / letterhead + brand lock-up | V4 | `partials/header.html`; lock-up drawn by `{% brand_lockup %}` (cms_nav.py) | `.site-header`, `.brand`, `.lock`, `.lock__mark/__wm/__w1–3/__tm` · components, v2/shell, **v4/shell** | shell.js: `is-scrolled`, `is-over-dark` | every public page | brand + navigation container | 64 → 56 px glass after 24 px; lock-up = logo-mark.svg + wordmark text in Newsreader 600 (green/navy/red words); tagline deliberately not rendered (forbidden phrase). CMS logo image can replace the lock-up. | ★ |
| P3 | Main navigation + mega-menu | V4 | `partials/main_nav.html` (CMS `MenuItem` or fallback: 7 sections — Personnes, Entreprises, Institutions, Universités & Formation, Forum, Actualités, Projet) | `.main-nav__list/__item/__link/__toggle/__panel/__panel-lead/__sublist/__sublink` · base, components, v2/shell, **v4/shell** (`@keyframes mega-in`) | main.js (open/close, ←/→ between sections, ↓ into panel, Escape innermost); shell.js indicator | every public page | discovery | Full-width panel from the bar edge; 2-column sublist > 4 items; no image, no description per link, no "featured" slot, no search. Chevron = separate 44 px toggle beside the link. | ★ |
| P4 | Mobile drawer + scrim | V4 | inside `partials/header.html` (`.nav-drawer`, `.drawer-utility`, `.nav-overlay`) | components, v2/shell, **v4/shell** | main.js (`data-nav-toggle`, focus loop, `--nav-drawer-top`) | every public page < 80rem | mobile nav | Slides from the menu's side over blurred scrim; account/login + language at top. `menu`/`close` icon swap. | ★ |
| P5 | Sliding nav indicator | V4 | created by shell.js (`.main-nav__indicator`) | v4/shell | shell.js (Motion spring) | desktop header | active/hover marker | Jumps under reduced motion; re-measured on resize/fonts. | ★ |
| P6 | Language selector (segmented FR · IT · EN · ع) | V4 | `components/language_segmented.html` | `.lang-seg__*` · v4/shell, console.css | none (plain links) | utility bar, drawer, console bar, console drawer (4 includes) | language switch | `ع` drawn with system Arabic font on Latin pages to save 45 KB. Stale comment references a non-existent `components/language_switcher.html`; `.lang-switcher` (25 rules) and `.language-switcher` CSS are dead. | ★ |
| P7 | Account menu (dropdown) | V4 | `components/account_menu.html` (`<details data-dropdown>`) | `.account-menu__*` · components, **v4/shell**, console.css, portal.css | main.js dropdowns | utility bar, drawer, console bar (signed-in) | account links + logout | Menu per DS #17; icons user/home/key/logout. **Class collision:** `accounts/partials/account_menu.html` (a side nav on profile/delete pages) reuses `.account-menu` / `.account-menu__list`, which components.css positions `absolute` as a dropdown — **to verify** on `/compte/profil/`. | |
| P8 | Skip link | V1 | `base.html` | `.skip-link` · base | — | all pages | a11y | OK. | |
| P9 | Home hero — doorway stage, 4 routes, glass legend | V4 | `pages/home/_hero.html` + `partials/_hero_title_lines.html` + `components/doorway.html` | `.hero`, `.hero__copy/__title/__lead/__actions/__stage`, `.doorway*`, `.route__casing/__line/__current/__ring/__node`, `.exit*`, `.doorway-legend__*`, `.line`, `.tm` · **v4/hero** (+ generic `.hero` rules in components, v3/v4 buttons, v4/shell, pages) | home.js | home (1) | identity + 4 audience entries | Only immersive object of the site. Copy complete on first frame; entrance animation removed; routes current 28 s CSS (`@keyframes route-current`), paused off-screen; compact viewBox < 64rem. H1 Newsreader 300, clamp 44–76 px. `d.photo` (hero slot photo) computed server-side but **not rendered**. | ★ |
| P10 | Doorway (brand door SVG) | V4 | `components/doorway.html` (included inside an `<svg>`) | `.doorway__body/__img/__veil/__arch-inset/__inner/__glow/__key/__steps/__arch` · v4/hero, entrance.css | home.js (photo drift only) | home hero + login stage (2) | brand identity | Proportions locked (BRAND_ASSETS §2). Photo `doorway-arch-400.webp` preloaded as LCP on both pages. | ★ |
| P11 | Generic hero component | **DEAD** | `components/hero.html` | `.hero--editorial/--inverse/--muted/--compact` · components | `.reveal` | 0 includes | — | Retired; its CSS still in components.css. | |
| P12 | Forum hero | V2 | `forum/partials/hero.html` | `.forum-hero__*` · forum.css, v3/v4 buttons | — | forum index, register, register_done (3) | event header | Eyebrow, title, subtitle, date meta, patron logos, optional DB hero image, registration CTA. Not aligned with the V4 hero language. | |
| P13 | Page header (public) | V1 (+ V2 register) | `components/page_header.html` | `.page-header__eyebrow/__title/__lead/__meta` · components, register, ecosystem, portal | — | **55 includes** (public + many console pages) + 19 hand-written `.page-header` (pathways ×5, orientation ×3, living ×2, enquiries ×3, community ×2, news, glossary term, project, antifraud) | page H1 + lead | The de-facto opening of every non-home page: type only, no image, no background variation. Also used inside the console (V2 pages), where V4 uses `ws-head`/`ctx`. | |
| P14 | Section header — home folio / component | V2 | `pages/partials/_section_header.html` (folio: ordinal · running head · date); `components/section_header.html` (eyebrow) | `.section__header/__title/__lead`, `.folio__ordinal/__head/__date`, `.eyebrow` · layout, register, pages, voyage | — | home ×6 sections; ecosystem ×4 | section heading | Two parallel section-header patterns (folio vs eyebrow). | |
| P15 | Audience entrances (the 4 doors) | V2 | `components/entrances.html` + `pages/home/partials/_route_glyph.html` | `.register--entrances`, `.register__item`, `.entry__ordinal/__title/__gloss/__cta/__arrow`, `.route__glyph` · register, v2/routes, pages | home.js (`is-related` lit from hero legend) | home entrances section (1) | 4 audience doors | Deliberately a numbered register, not cards (no image, no card). Contour landform glyph per actor (DS V4 §9 says it should become actor glyphs — not done). | |
| P16 | Pathway list (numbered editorial list) | V1 | `components/pathway_list.html`; `pathways/index.html` variant with icon | `.pathway-list__*` · components, pages | — | home pathways, pathways index (2) | the 8 regular routes | Stretched link, CSS counter numerals. Text-only. | |
| P17 | Pathway families (interim register) | V2 | inline in `pages/home/_pathways.html` | `.register.home-families` · register, pages | — | home (gate closed) | neutral family labels | Register with no destination (intentional). | |
| P18 | Card | V1 | `components/card.html` | `.card`, `.card--link/--flat`, `.card__eyebrow/__title/__text/__meta` · components | — | home news; ecosystem ×4 "related" (5) | teaser | No media slot at all; stretched link. | |
| P19 | News card | **unstyled** | `news/_card.html` | `.news-card__media/__body/__meta/__category/__title/__summary` · **no CSS rule anywhere** | — | news index, news detail related (2) | article teaser | Second card component for the same content type; hero image rendered at intrinsic size with no styling. | |
| P20 | Image / feature section — institutional pages | V2 | `pages/partials/_picture.html` inside `.page-figure` | `.page-figure` · pages.css | — | project, AGAMI, network (3) | editorial photo | `<picture>` WebP srcset + JPG fallback, lazy. One photo per page. | |
| P21 | Image / feature section — ecosystem landings | V2 | `ecosystem/partials/photo.html` | `.ecosystem-photo__img` · ecosystem.css | — | companies, institutions, universities, pilot (4) | landing photo | Same pattern, second implementation (`Photo` from `ecosystem.services`, not `pages.services`). | |
| P22 | Home orientation (4-step sequence) | V2 | `pages/home/_orientation.html` | `.sequence`, `.sequence__step/__marker/__title/__body`, `.home-orientation__*` · register, pages | — | home | how orientation works | Vertical list with ticks; one primary CTA. | |
| P23 | Home trust «does / does not» + jurisdiction bar | V2 | `pages/home/_trust.html` + `components/jurisdiction.html` | `.home-trust__*`, `.jurisdiction__bar/__segment--{morocco,italy,platform,authority}/__legend/__swatch` · pages, register | — | home (1) | transparency + who answers for what | Jurisdiction bar = the "recognisable device" (textures + legend, data-share not inline style). | |
| P24 | Home anti-fraud panel | V2 | `pages/home/_antifraud.html` | `.antifraud-panel__*` · pages | — | home, antifraud page (2) | fraud warning | Shield icon panel, secondary CTA. | |
| P25 | Home ecosystem (promoter + partners) | V2 | `pages/home/_ecosystem.html` | `.home-ecosystem__*` · pages | — | home, network page (2) | promoter + authorised partners | Partner logos only if `logo_public`; text fallback. | |
| P26 | Home reserved-area panel / access point | V2 | `pages/home/_reserved.html`; `portal/partials/access_point.html` (cta-panel variant) | `.home-reserved__*`; `.cta-panel` · pages, components | — | home (1); access_point: tests only (0 templates) | entry to the platform | access_point partial is not included by any template (only a test). | |
| P27 | Home pilot «route between two shores» | V2 | `pages/home/_pilot.html` (`{% voyage_route %}`) | `.voyage__shore/__dot/__svg/__line/__station/__stations/__step/__num/__label` · v2/voyage, pages | home.js (scroll draw), shell.js (`[data-reveal]`) | home (phase 3 only) | process visualisation | Scroll-drawn SVG line; vertical list < 64rem. | |
| P28 | Forum section on home (banner) | V2 | `pages/home/_banner.html` → `forum/partials/home_banner.html` | `.home-banner`, `.forum-banner__*` · pages, forum, register | pages/js/home.js (dismiss) | home (1) | Forum Vénétie–Maroc notice | Quote in Newsreader italic (the only reason the italic font loads on home). | |
| P29 | Forum page sections | V2 | `forum/index.html` + partials: `hero`, `local_nav`, `presentation`, `programme`, `speakers`, `registration_section`/`registration_form`/`privacy_note`, `permanent_sections`, `virtual_forum_teaser`, `cta_row` | `.forum-section`, `.forum-localnav`, `.forum-programme`, `.forum-speakers`, `.forum-cards`/`.forum-card`, `.forum-gallery`, `.forum-documents`, `.forum-partners`, `.forum-form`, `.forum-cta` · forum.css | — | forum index / register / done (3) | event + permanent space | Text-heavy; programme and speakers are plain lists; disabled CTAs rendered as `span.is-disabled`. | |
| P30 | Institutional banner component | **DEAD** | `components/institutional_banner.html` | `.institutional-banner__*` · components | — | 0 | — | Superseded by `forum/partials/home_banner.html`. | |
| P31 | News index (filter bar, list, newsletter) | **unstyled** | `news/index.html`, `news/_newsletter.html`, `news/detail.html` | `.news-index`, `.filter-bar__*`, `.news-list`, `.newsletter`, `.article`, `.related-articles` · **no CSS** | — | 2 pages | news | Only global styles apply (container, page-header, prose, form-field, btn). | |
| P32 | FAQ / accordion | V1 | `faq/_item.html` (reuses accordion classes) ; `components/accordion.html` | `.accordion__item/__summary/__panel`, `.faq-item__*`, `.search-form__*`, `.related-links__*` · components | main.js accordion (single mode unused) | FAQ (1); component SHOWCASE-ONLY | Q&A | Native `<details>`; FAQ uses `accordion__panel` where the component uses `accordion__body` (two markups). No expand icon in FAQ summary. | |
| P33 | Tabs | **SHOWCASE-ONLY** | `components/tabs.html` | `.tabs__list/__tab/__panel` · components | main.js roving tabindex | 0 product pages | — | Never used in product. | |
| P34 | Footer | V2 (+V4 tokens) | `partials/footer.html` | `.site-footer__*`, `.lock--dark` · base, components, v2/shell, v3/chip | — | every public page | legal + navigation + project | Navy, 4 columns: lock-up (dark), promoter, e-mail, trademark words / legal links / nav / project + anti-fraud link. No newsletter, no social, no imagery. | |
| P35 | CTA bands | V1 | `components/cta_panel.html` (incl. `--inverse`); `pathways/_orientation_cta.html`; `ecosystem-cta` wrapper; `forum/partials/cta_row.html` | `.cta-panel__*`, `.ecosystem-cta`, `.forum-cta__*` · components, ecosystem, forum | — | ecosystem ×3, pathways ×5, forum ×1 | conversion band | Four implementations; flat paper/navy band, no image. | |
| P36 | Modal | **SHOWCASE-ONLY** | `components/dialog.html` (native `<dialog>`, `:target` fallback) | `.dialog__*` · components (`@keyframes dialog-in`) | main.js | 0 product pages | — | Never used in product. | |
| P37 | Drawers (public) | V4 | = P4 | — | — | — | — | Only the nav drawer. | |
| P38 | Search (public) | PARTIAL | FAQ `search-form`, glossary `search-form` (server GET) | `.search-form__*` · components | — | FAQ, glossary (2) | in-section search | **Global site search ABSENT**; no search in header or mega-menu. | |
| P39 | Language selector | V4 | = P6 | | | | | | ★ |
| P40 | Loader | **ABSENT** | — | — | — | — | — | See §2. | ★ |
| P41 | Page transition | **ABSENT** | — | — | — | — | — | No View Transitions; public "page enter" (DS V4 pattern 1b) not built. | |
| P42 | Scroll indicator / reading progress / back-to-top | **ABSENT** | — | — | — | — | — | — | |
| P43 | Tooltips (public) | **ABSENT** | — | — | — | — | — | Only native `title` attributes. | |
| P44 | Badges (public) | V3 | `components/badge.html`, `.badge` in pathways | `.badge` · v3/chip | — | pathways ×4 | "à venir" / state markers | Badge = chip with register; no numeric badge. | |
| P45 | Stats / counters | **ABSENT** (by policy) | — | — | main.js `initCounters` dead | — | — | Owner rule: no invented KPI. | |
| P46 | Gallery | V2 | `forum/partials/permanent_sections.html` | `.forum-gallery__*` · forum | — | forum permanent (1) | photos/videos | `<img>` without width/height (CLS risk); no lightbox. | |
| P47 | Media / video | V2 | same | `.forum-gallery__video` | — | forum (1) | video | `<video controls>` with no `<track>` captions. | |
| P48 | Timeline (public) | V1 | `components/timeline.html`; `.timeline` hand-written in pathways | `.timeline__item/__marker/__label/__text` · components, ecosystem, pages | main.js `.reveal` stagger | ecosystem companies, pilot flow; pathways detail / diplomas / index_interim (5) | steps | Horizontal ≥ 48rem, vertical below. | |
| P49 | Process visualisation | V2 | voyage (P27), jurisdiction (P23), `ecosystem/partials/pilot_flow.html` + `img/illustrations/pilot-flow.svg`, home `sequence` | `.pilot-diagram*` · ecosystem | `.reveal` | home, ecosystem pilot | process | Three different diagram languages. | |
| P50 | Local / side navigation | V1 | `components/local_nav.html`; `pathways/_side_links.html`; allauth manage | `.local-nav__*`, `.layout-sidebar__aside` · base, components | — | ecosystem layout, institutional base, pathways ×4, manage (≈ 8) | section nav | Sticky column desktop / pill list mobile. | |
| P51 | Section "sommaire" nav | V1 | `pathways/detail.html` | `.section-nav__*` · components | main.js marker never wired (no `data-section-nav`) | 1 | in-page TOC | Current-section highlight does not run. | |
| P52 | Breadcrumbs | V1 | `components/breadcrumbs.html` | `.breadcrumbs__*` · base, components, wizard, console, portal | — | **39 templates** + console bar | wayfinding | CSS chevrons mirrored in RTL. | |
| P53 | Notices (public) | V1 (+V4 font) | `components/notice.html`, `form_unavailable.html`, `pathways/_preview_notice.html`, `_antifraud_callout.html`, `ecosystem/partials/preview_notice.html` | `.notice--{info,success,warning,error,pending,institutional}` · components, v4/shell | — | **24 includes** + 21 hand-written | status/legal messages | `role=alert` only for errors. | |
| P54 | Institutional quote | V1 | `components/blockquote.html` | `.blockquote-institutional` · components | — | ecosystem companies (1) | quotation | — | |
| P55 | Metadata row | V1 | `components/metadata_row.html`; `pathways/_metadata_row.html`; inline `.meta-row` | `.meta-row__item` · components | — | component SHOWCASE-ONLY; pathways ×3, portal ×2 inline | date/place/state | Icon + dt/dd. | |
| P56 | Glossary A–Z + entries | V1 | `glossary/index.html`, `glossary/term.html` | `.az-index__*`, `.glossary-entry` (styled); `.glossary-term`, `.meta-list` (**no CSS**) | — | 2 | Italian legal terms | Term page partly unstyled. | |
| P57 | Living in Italy — topic / sheet cards | **unstyled** | `living/index.html`, `topic.html`, `sheet.html` | `.living-topics`, `.topic-grid`, `.topic-card__icon`, `.sheet-list`, `.sheet-card` · **no CSS** | — | 3 | practical topics | Icon per topic (globe, home, plus…) but grid/card have no rules. | |
| P58 | Partners list | **unstyled** | `partners/index.html` | `.partners__logo` · **no CSS** | — | 1 | authorised partners | Logos at intrinsic size. | |
| P59 | Enquiry forms (contact, company needs, collaboration) | V1 | `enquiries/*`, `partials/form_shell.html`, `partials/form_field.html` | `.enquiry-page/-form/-done` **no CSS**; `.form`, `.form-field`, `.hp-field` · components | main.js error focus | 4 | lead capture | Honeypot, error summary; page wrappers unstyled; gated by `form_unavailable`. | |
| P60 | Orientation wizard (public) | V2 | `orientation/{start,step,_step,result,resume,save_unavailable}.html` | `.wizard__*`, `.wizard-intro/-result/-resume/-disclaimer` · orientation/wizard.css | orientation/wizard.js (print; htmx hooks inert) | 5 | pre-assessment questionnaire | Percentage progress bar (`progress_class`); plain radio/checkbox list (not the V4 OptionCard); `<details>` "Pourquoi cette question ?". Different system from «Ma situation». | ★ (journey) |
| P61 | Error pages | V1 | `errors/*` | `.error-page`, `.js-only` · components | main.js history back | 6 | 4xx/5xx | Text + e-mail + back. | |
| P62 | Legal document page | V1 | `legal/document.html` | `.legal-page`, `.prose` · components, base | — | 1 | legal texts | — | |
| P63 | Community (Virtual Forum) | **unstyled** | `community/*` (9) | `.community-*` (13 blocks) · **no CSS** | — | 9 | discussion rooms, calendar, initiatives, moderation | Behind gate G11; public shell for an authenticated feature. | |
| P64 | Institutional page links / actor list | V2 | `pages/project.html`, `antifraud.html`, `contact.html`, `network.html` | `.page-links__*`, `.actor-list__*`, `.contact-address` · pages | — | 4 | related links / actors | Icon + label rows. | |
| P65 | Newsletter form | V1 | `news/_newsletter.html` | `.newsletter` (**no CSS**) + form-field | — | news index | subscription | Gated. | |
| P66 | Dismissible banner | V2 | `pages/home/_banner.html` | `.home-banner__dismiss` · pages | pages/js/home.js | home | hide notice for the tab | Button hidden without JS. | |

---

## 4. AUTHENTICATED PLATFORM — components and patterns

| # | Component / pattern | Status | Template(s) | CSS selectors · sheet(s) | JS | Where used (≈) | Role | Quality notes | Flag |
|---|---|---|---|---|---|---|---|---|---|
| C1 | Navigation rail | V4 | `partials/portal_chrome.html` + `portal/partials/rail_nav.html` | `.rail`, `.rail__brand/__tile/__wordmark/__scroll/__group/__group-title/__list/__item/__glyph/__label/__collapse`, `.rail--drawer`, `.rail__tip` · console.css | console.js, rail-pref.js | 51 console templates | platform navigation | 10 base entries + role entries; glyph + word; collapsed tooltip; ↑/↓/Home/End. Company workspace swaps in its own 5 entries. Icons reused across concepts (§7). | ★ |
| C2 | Context bar (top bar) | V4 | `partials/portal_chrome.html` (`.portal-bar.console-bar`) | `.console-bar__menu/__tile/__crumbs/__title/__actions/__link/__lang` · console.css, portal.css | console.js | 51 | where am I + account + language | 56 px glass sticky; breadcrumb from ≥ 64rem, page title below. | ★ |
| C3 | Bottom bar (mobile) | V4 | same | `.console-bottom__item/__label` · console.css | console.js | 51 (< 64rem) | thumb navigation | 4 entries flagged `bottom` + Menu. | ★ |
| C4 | Console drawer | V4 | same (`<dialog class="console-drawer">`) | `.console-drawer__head/__foot/__close` · console.css (`@keyframes console-drawer-in[-rtl]`) | console.js (`showModal`, backdrop close, focus return) | 51 (< 64rem) | full rail on mobile | Native dialog. | ★ |
| C5 | Console footer | V4 | `portal/base_portal.html` | `.portal-footer`, `.console__footer` · console, portal | — | 51 | legal links | 4 lines. | |
| C6 | Workspace grids | V4 | dashboard, case, company | `.ws-grid`, `.file-grid__main/__inspector`, `.ws-wide` · v4/workspace | — | 3 | layout 8/4, 7/5, 6/6, 12 | 12-col grid, three panel measures. | ★ |
| C7 | ContextHeader + compact ctx-bar | V4 | dashboard, `cases/detail.html`, `companies/dashboard.html`, `companies/partials/need_table.html` | `.ctx__words/__greeting/__eyebrow/__title/__meta/__ref/__since/__resp/__progress/__action`, `.ctx-bar__*` (`has-ctx-bar`) · v4/workspace | console.js (ctx-bar) | 4 | page title + file state + one primary | Mono reference, chip, meter; compact bar is `aria-hidden` duplicate. No `view-transition-name` (spec conflict, documented). | ★ |
| C8 | Workspace head | V4 | documents, situation, dashboard (no case), company | `.ws-head__words/__title/__lead/__action/__action-note` · v4/workspace | — | 5 | page title + primary | Third header pattern in the console (with `page_header` and `ctx`). | |
| C9 | Legacy case header band | V2 | `portal/partials/case_header.html` | `.case-header__*` · portal.css | — | pages inside a case that do not empty the block | 4 facts band | Uses `.notice--warn` (**no CSS**; defined modifier is `--warning`) — **to verify**. | |
| C10 | Legacy next-action band | V2 | `portal/partials/next_action.html` | `.next-action--{urgency}__*` · portal.css | — | same | "your next action" | Superseded by `ws-next` panel on V4 pages; still drawn elsewhere. | |
| C11 | Panel (L1 / L2 / edge) | V4 | inline | `.panel--l1/--l2/--edge`, `.panel__head/__eyebrow/__title/__section/__text/__actions/__meta/__more` · v4/workspace | — | 7 | container | Only 5 product pages use it. | ★ |
| C12 | Next-step panel + ResponsibilityBar | V4 | dashboard, case detail, company dashboard | `.ws-next--{urgency}`, `.resp__label/__actor/__note` · v4/workspace | — | 3 | the one priority + who acts | Answers "who is responsible" with glyph. | ★ |
| C13 | Facts list + five-notch meter | V4 | dashboard, case ctx, company | `.facts__row`, `.meter__notch--on`, `.meter__words` · v4/workspace (`@keyframes notch-fill`) | CSS | 3 | file facts + progress count | Count, never a percentage. | ★ |
| C14 | Glyph / avatar | V4 | `components/glyph.html` | `.glyph--{sm,md,lg,dark,none}` · v4/workspace | — | 5 | actor type disc | Never a photo of a person; dashed disc when no glyph. | |
| C15 | JourneyRail | V4 | `components/journey_rail.html` | `.journey`, `.journey--descriptive`, `.journey__step--{current,done,italy,frontier}`, `__node/__side/__label/__here/__when/__actor` · v4/workspace (`rail-draw`, `rail-draw-y`) | CSS | dashboard, case detail (2) | where am I in 7 steps | Horizontal ≥ 64rem, vertical below / descriptive. | ★ |
| C16 | HealthStrip | V4 | `components/health_strip.html` | `.health`, `.health--compact`, `.health__strip/__segment/__counts/__n/__open` · v4/workspace (`strip-fill`) | — | dashboard, register, case (3) | pieces by state | Bar aria-hidden, words carry the counts; segment `title` = only tooltip. | ★ |
| C17 | SegmentedControl (state filter) | V4 | `documents/partials/register.html` | `.seg__list/__item/__link/__link--empty/__dot/__count` · v4/workspace | — (links) | register (1) | filter by state | Filter in URL; fade mask when scrolling; DS asked for a sliding spring thumb — not built (documented deviation). | ★ |
| C18 | Document search | V4 | register | `.doc-search__icon/__input` · v4/workspace | console.js | 1 | filter rows by title | Client-side, accent-folding, live count announced. | ★ |
| C19 | DocumentCollection / DocumentRow (+ card < 48rem) | V4 | `components/document_row.html` in `documents/partials/register.html`, dashboard (compact) | `.doc-collection`, `.doc-row`, `.doc-row--{overdue,compact}`, `__identity/__words/__title/__meta/__reason/__state/__blocked/__responsible/__actor/__due--{urgency}/__health/__action/__menu/__more` · v4/workspace | — | 2 | one required piece | 7 zones; state = word + register; one row template for phone and desktop. DocumentCard (DS #25) = the same row stacked. | ★ |
| C20 | Row menu popover | V4 | inside document_row | `.doc-menu`, `.doc-menu__item` (`[popover]`) · v4/workspace | console.js (placement) | 1 | consult / download / versions | Uses the `menu` (hamburger) icon for a row-actions menu (§7). | ★ |
| C21 | Latest deposits list | V4 | dashboard | `.deposits__row/__name/__kind` · v4/workspace | — | 1 | files scanned | — | |
| C22 | Table (V4) + table-as-cards | V4 | `cases/detail.html`, `portal/documents.html`, `companies/partials/need_table.html` | `.table-region`, `.table`, `.table__primary/__gloss/__link/__actor/__none/__overdue/__select/__form`, `.table__row--overdue` · v4/workspace | — | 3 | checklist, files, needs | Semantic caption/scope; cards below region width; sticky head under ctx-bar. | ★ |
| C23 | Data table (V2) | V2 | 16 templates (academy, companies analysis/profile/need, documents index, forum governance ×5, helpdesk dispatch, selection ×3, accounts profile) | `.scroll-x`, `.data-table` · portal, documents, selection | — | 16 | lists of records | Second table system. | |
| C24 | Account table (V1) | V1 | `allauth/elements/table.html`, `portal/requests.html` | `.account-table` · components | — | 2 | e-mail list, requests | Third table system. | |
| C25 | Case timeline | V4 | `components/case_timeline.html` | `.tl`, `.tl__row--last`, `__node/__when/__what/__title/__detail/__actor` · v4/workspace (`tl-light`) | CSS | case detail (1) | audit trail | Append-only; last node lights once. | ★ |
| C26 | Dates and threads mini-lists | V4 | dashboard, case detail, company | `.dates__row--{urgency}/__when/__what`, `.threads__row--unread/__link/__subject/__meta` · v4/workspace | — | 3 | deadlines, messages | Icons calendar / clock / warning by urgency. | ★ |
| C27 | Actors list | V4 | case detail | `.actors__row/__words/__who/__mandate` · v4/workspace | — | 1 | who intervenes | Glyph + role + mandate. | ★ |
| C28 | Outcome + sources (assessment) | V2 → V4 panel | dashboard, case detail, `cases/assessment.html`, `documents/requirement_detail.html`, forum governance | `.outcome--{kind}__kind`, `.sources__item/__consulted`, `.note`, `.gloss` · register, v4/workspace, documents | — | ≈ 6 | pre-assessment result | Word + rule, sources listed. | |
| C29 | Staff state-transition form | V4 inputs | case detail | `.file-state__form`, `.form-field` · v4/workspace | — | 1 | change case status | Bare `<select>` styled as V4 input. | |
| C30 | File action bar (mobile) | V4 | case detail | `.file-action-bar` · v4/workspace | — | 1 | sticky primary on phone | — | ★ |
| C31 | Portal cards grid (non-person accounts) | V1/V2 | `portal/partials/card.html` | `.portal-cards`, `.portal-card__header/__title/__figure/__count/__footer`, `.portal-list__*` · portal | — | dashboard (bridge) | company/institution/university/pro home | Explicitly a "bridge"; icon-card grid the V4 direction rejects. | ★ |
| C32 | Portal list (messages, deadlines, card items) | V2 | `portal/messages.html`, `deadlines.html`, `partials/deadline_item.html`, card | `.portal-list__item/__title/__meta/__aside` · portal | — | 4 | lists | Badge aside; pagination. | |
| C33 | Message detail | V2 | `portal/message_detail.html` | `.meta-row`, `.portal-message` · portal | — | 1 | read one message | "Marquer comme lue" primary with check icon. | |
| C34 | Requests list / detail («Mes demandes») | V1/V2 | `portal/requests.html`, `request_detail.html` | `.account-table`, `.portal-facts` · components, portal | — | 2 | requests the person sent from their account | Table from the V1 account layer inside the V4 shell. | |
| C35 | «Mon parcours» (orientation results) | V2 | `portal/pathways.html` | `.portal-result`, `.meta-row` · portal | — | 1 | past pre-assessments | Icon-meta rows (calendar / document / info / key). | |
| C36 | «Ma situation» guided form | V4 | `portal/situation.html` | `.wiz__rail/__count/__stage/__q/__ordinal/__field/__question/__help/__foot/__foot-count/__note/__notask/__list`, `.wiz--guided` · v4/wizard | situation.js | 1 | profile facts, one question at a time | Sticky glass foot; one primary per step; works without JS. | ★ |
| C37 | Wizard stepper | V4 | `components/wizard_stepper.html` | `.wstep__item--{done,current}/__link/__node/__label` · v4/wizard | situation.js | 1 | question map | Anchor links work without JS. | ★ |
| C38 | OptionCard | V4 | `components/option_cards.html` | `.opts__legend/__help/__hint/__grid`, `.opt__mark/__title`, `.opts--error` · v4/wizard | — (native inputs) | 1 | radio/checkbox choices as cards | Check draws itself; ≥ 48 px. Not used by the public orientation wizard. | ★ |
| C39 | Document detail / versions / upload | V2 | `documents/requirement_detail.html`, `upload.html`, `terms_required.html`, `index.html` (loose files) | `.doc-page`, `.doc-piece`, `.doc-versions`, `.doc-version`, `.doc-form`, `.doc-loose`, `.doc-inline-form`, `.doc-register` · documents.css | — | 4 | one requirement, its versions, deposit | V2 register look inside the V4 shell. | ★ |
| C40 | File upload | **PARTIAL** | form_field with `<input type=file>` | `.form-field input[type=file]` · components | — | upload, requirement detail (2) | deposit a file | No dropzone / drag state / real progress / success tick (DS #26, pattern 12). | ★ |
| C41 | Document preview | **ABSENT** | — | — | — | — | — | Download link only; no drawer preview (DS #19 Drawer "for document preview" not built). | ★ |
| C42 | Company workspace | V4 (dashboard) + V2 (needs, need detail/form, profile/form, analysis) | `companies/*`, `partials/company_header.html`, `need_register.html`, `need_table.html` | `.company-id`, `.ws-company`, `.ws-needs`; V2: `.company-header`, `.need-head/-actors/-missing`, `.companies-*` · v4/workspace, companies.css | — | 7 | B2B needs | Split across two generations. | |
| C43 | Selection («Processus assignés») | V2 | `selection/*` + `partials/responsible.html` | `.selection-*`, `.responsible` · selection.css | — | 4 | authorised-actor process | Dense V2 register; bare `<select>`/checkbox forms. | |
| C44 | Helpdesk «Guichet numérique» | V2 | `helpdesk/{requests,open_request,detail,queue,dispatch}.html` | `.desk-state--{tone}`, `.desk-mandate`, `.exchange__head/__role`, `.desk-form`, `.desk-dispatch`, `.desk-scroll` + `.sequence` · helpdesk.css | — | 5 | request/answer exchange | Stylesheet header forbids radius > 2 px, shadows, cards — directly contrary to V4. Exchange drawn as a `sequence` (no chat bubbles). | |
| C45 | Academy (catalogue, course, enrolment, plan, mine) | V2 | `academy/*` + `partials/enrolment_entry.html` | `.academy-filters__*`, `.attendance__*`, `.module-form`, `.academy-inline` + register/sequence/portal-facts · academy.css | — | 6 | training | Register rows, no cover images (CD §5.6 planned 1 cover per course). | |
| C46 | Academy cards | **ABSENT** | — | — | — | — | — | Courses are register entries. | |
| C47 | Course progress | PARTIAL | enrolment detail | `.sequence__step--current`, facts "n modules sur N" | — | 1 | progress | Count + current module; no progress bar (by policy). | |
| C48 | Forum governance workspace | V2 | `forum/governance/*` (11) | register/entry, portal-section, portal-facts, data-table, state | — | 11 | commissions, proposals, projects, tables, annual report | Entirely V2. | |
| C49 | Register / entry (V2 list primitive) | V2 | inline | `.register`, `.register__item`, `.entry__ordinal/__title/__gloss/__actor/__cta` · register, v2/routes, academy, companies, documents, selection | — | **22 templates** | list of records | The dominant list pattern of the platform. | |
| C50 | Portal section + folio | V2 | inline | `.portal-section`, `.folio`, `.portal__section-title` · portal, register | — | **28 / 30 templates** | section heading in console | Serif titles on operational screens (V4 says Plex only). | |
| C51 | Portal facts | V2 | inline | `.portal-facts__row` · portal, companies | — | 13 | dl facts | Parallel to V4 `.facts`. | |
| C52 | Chips / status | V3 + V4 pill | inline; `components/badge.html` | `.chip.state` (V4 pill) · v4/workspace; `.state`, `.badge`, `[data-register=neutro/attesa/azione/conforme/rifiuto/nullo]`, `data-stage`, `.is-pending` · v3/chip | — | `.state` 35 · `.chip` 6 · badge 5 | state as word + register | Six registers from Python (`core/chips.py`); never "approved". V4 pill only on V4 pages; V3 stamp elsewhere. `chips.GLYPH` (clock / warning / check / close / minus per register) defined but **not rendered anywhere**. | ★ |
| C53 | Notices in platform | V1 + V4 font | notice component, `.portal-notices` | `.notice--*` | — | ≈ 12 | institutional/team notices, unavailable | See C9 for `--warn`. | |
| C54 | Empty states | V4 sentence + V1 component | `.empty` paragraph; `components/empty_state.html` | `.empty` · register, v4/workspace; `.empty-state__icon/__title/__text` · components, v4/workspace, portal | — | `.empty` 32 · component 21 | nothing here yet | Two patterns: one-sentence hairline (V4 rule) vs icon + title component still used on 21 pages. DS #30 six named variants not built. | |
| C55 | Pagination | V1 | `components/pagination.html` | `.pagination__*` · base, components | — | 6 | prev / page n of N / next | No page numbers; not restyled V4 (DS #22). | |
| C56 | Breadcrumb in console | V1 in V4 bar | breadcrumbs component inside context bar | + console, portal | — | 51 | wayfinding | — | ★ |
| C57 | Filters | mixed | seg (V4), `.academy-filters` (V2), news `.filter-bar` (unstyled) | — | — | 3 | filter lists | Three filter patterns. | |
| C58 | Inputs / select / textarea / checkbox / radio | V1 + V4 overrides | `components/form_field.html`, `allauth/elements/{field,fields}.html`, `enquiries/partials/form_field.html` | `.form-field__label/__control/__help/__errors/__check/__required`, `.form-field--{error,required,consent}` · components; V4 overrides in v4/buttons, v4/workspace (`.console__workspace .form-field`), entrance.css | main.js error focus | **21 includes** + 2 variants | forms | Three scopes of input styling (public V1, console V4, entrance V4). DS V4 checkbox/radio styling only on OptionCard. | |
| C59 | Password show/hide | V4 | form_field (password branch) | `.form-field__control--password`, `.form-field__toggle` · v4/buttons, entrance | shell.js | login, signup, password pages | reveal password | Labelled, `aria-pressed`. | ★ |
| C60 | Busy button | V4 | any `form[data-single-submit]` | `.btn.is-busy` (`@keyframes btn-busy`) · v4/buttons | shell.js | allauth forms only | loading feedback | Not applied to console forms (upload, situation, helpdesk…). | ★ |
| C61 | Form error summary | V1 | `components/form_errors.html` | `.form-errors__list` + notice · components | main.js focus | 13 | WCAG 3.3.1 | — | |
| C62 | Switch | **ABSENT** | — | — | — | — | — | DS #12 not built. | |
| C63 | Command palette | **ABSENT** | — | — | — | — | — | DS #35 not built. | |
| C64 | Notification centre | **ABSENT** | — | — | — | — | — | Closest: «Communications» list; unread count only inside the rail label text; no bell, no panel. | |
| C65 | Toast | **ABSENT** | — | `.messages`, `.alert--*` · components | — | base.html | — | Django messages render as an inline alert block at the top of `<main>` (DS #20 not built). | |
| C66 | Popover | V4 (one) | doc-row menu | `[popover]` | console.js | 1 | row actions | Only instance. | |
| C67 | Tooltip | V4 (one) | collapsed rail | `.rail__tip` · console.css | console.js | rail | label of a glyph | Only instance (DS #15 generic tooltip not built). | |
| C68 | Skeleton | **ABSENT** | — | token only | — | — | — | DS #31 not built. | |
| C69 | Loaders | **ABSENT** (busy meter only) | — | — | — | — | — | See C60. | ★ |
| C70 | Error states | V1/V2 | form errors, notice error, `form_unavailable`, `portal/unavailable.html`, card "unavailable" notice, error pages | — | — | ≈ 15 | failure | No network-error state (no async requests exist). | |
| C71 | Collapsible sections (console) | **ABSENT** | — | — | — | — | — | Case detail explicitly refuses `<details>` sections; only `helpdesk/dispatch.html` uses `<details>`. | |
| C72 | Quick actions | **ABSENT** as a component | `ctx__action` (one primary), dashboard account buttons | — | — | — | — | By design: one primary per screen. | |
| C73 | Dashboard KPI / stats | **ABSENT** (policy) | — | — | — | — | — | — | |
| C74 | Account pages (profile, delete) | **unstyled wrappers** | `accounts/profile.html`, `delete_request.html`, `delete_done.html`, `partials/account_menu.html` | `.account-layout`, `.account-section`, `.account-facts`, `.account-form`, `.account-links`, `.form-actions`, `.table-wrap`, `.form-inline` · **no CSS**; `.account-page`, `.account-panel` · components, entrance | — | 3 | profile, data export, deletion | Public shell; see P7 class collision. | |
| C75 | Data rows (summary) | mixed | register entry (V2), doc-row (V4), dates/threads/deposits/actors (V4), portal-list (V2), table rows (V4/V2/V1) | — | — | — | — | Seven row patterns across the platform. | |

---

## 5. Shared primitives (both sides)

| Primitive | Variants present (CSS) | Variants used in templates (template files) | Sheets | Notes |
|---|---|---|---|---|
| Button `.btn` | primary, secondary, soft, ghost, link, text, tertiary, quiet, inline, danger, inverse, icon, arrow, upper, block, sm, lg, large; states `is-busy`, `is-disabled` | primary 86 · secondary 76 · sm 29 · arrow 24 · link 12 · inverse 10 · lg 6 · danger 5 · ghost 4 · upper 1 · text 1 · large 1 (in 76 templates) | base, components, layout, register, v3/buttons, **v4/buttons**, v4/hero, v4/workspace, academy, entrance, forum | V4: primary gradient + inner light + shadow + glow, soft new; `soft`, `tertiary`, `quiet`, `inline`, `icon` never used. Two sizes names (`lg` / `large`). IconButton (DS #2) not used. |
| Link with arrow `.link-arrow` | one | 20 templates | components, v2/voyage | Secondary navigation everywhere. |
| Layout primitives | `container`, `stack`, `cluster`, `grid-auto`, `layout-sidebar`, `split`, `scroll-x`, `list-reset`, `hide-mobile` | container 87 · scroll-x 19 · stack 8 · layout-sidebar 7 · cluster 6 · grid-auto 6 | layout | `.zones`, `.grid`, `col-*`, `.measure`, `.center`, `mt-/mb-` utilities largely dead. |
| Typography utilities | `.t-folio`, `.t-ref`, `.t-caption`, `.t-gloss`, `.t-prose`, `.prose`, `.eyebrow` (+ dead `.t-band`, `.t-entry`, `.t-lead`, `.t-plate`, `.t-title`, `.t-ui`, `.t-numeral`, `.text-*`) | t-caption 16 · t-folio 12 · t-ref 11 · prose 7 · t-prose 5 · t-gloss 4 · eyebrow 4 | base, layout, register, _legacy-tokens | Two utility families (`.t-*`, `.text-*`). |
| Focus ring | one ring + 2 px companion (unified in gate reviews) | — | v4/shell, v4/buttons, v4/workspace, console | Several "ONE ring" override blocks exist because earlier halos (V2 5 px) kept resurfacing. |
| Reveal on scroll | `.reveal` (main.js + components.css) and `[data-reveal]` (shell.js + Motion) | `.reveal` 2 · `[data-reveal]` 1 | components, ecosystem, pages, v2/voyage | Two systems for the same effect; `data-reveal-once` hook (orientation result) read by nothing. |

---

## 6. ABSENT — consolidated list (requested patterns with no implementation)

| Pattern | Public | Platform | Closest existing thing | DS V4 status |
|---|---|---|---|---|
| Loader / page loader | ABSENT | ABSENT | busy meter on allauth submit buttons | pattern 13 (static skeleton + busy) partly |
| Page transition | ABSENT | ABSENT (removed) | — | pattern 1/1b specified, 1 built then removed |
| Scroll indicator / reading progress | ABSENT | — | header state change on scroll | not specified |
| Tooltip (generic) | ABSENT | rail only | `.rail__tip`, native `title` | DS #15 |
| Stats / counters / KPI | ABSENT (policy) | ABSENT (policy) | counts in words (HealthStrip, meter) | refused |
| Global search | ABSENT | ABSENT | FAQ / glossary GET search; document register filter | DS #34 |
| Command palette | — | ABSENT | — | DS #35 (staff) |
| Notification centre | — | ABSENT | «Communications» list, unread count in rail label | — |
| Toast | ABSENT | ABSENT | inline Django `.alert` block | DS #20 |
| Skeleton | ABSENT | ABSENT | — | DS #31 |
| Switch | ABSENT | ABSENT | — | DS #12 |
| Modal in product | SHOWCASE-ONLY | only as console drawer | `components/dialog.html` | DS #18 |
| Tabs in product | SHOWCASE-ONLY | ABSENT | `components/tabs.html` | DS #13 |
| Drawer (content: preview, filters, activity) | nav only | nav only | console drawer | DS #19 |
| Document preview | — | ABSENT | download link | DS #19 |
| Upload dropzone / progress | — | ABSENT | plain file input | DS #26 |
| Academy course cards / covers | — | ABSENT | register entries | CD §5.6 |
| Collapsible sections (console) | FAQ only | ABSENT (refused on case file) | `<details>` in helpdesk dispatch | CD §3.6.4 not built |
| Image in mega-menu | ABSENT | — | — | CD §5.6 (owner decision pending) |
| Hero on non-home public pages | ABSENT | — | page-header, one photo on 7 pages | CD §5.6 "hero 4:5" per landing |
| Gallery / media outside forum | ABSENT | — | forum gallery | — |
| Numeric badge (counter) | ABSENT | ABSENT | — | DS #4 |

---

## 7. ICON SPRITE — `static/img/icons.svg` (36 symbols, 6.3 KB, `{% svg_icon %}` → `<svg><use href="…icons.svg#icon-ID">`)

Sources scanned: every `svg_icon "…"` in templates; `icon=` / `glyph=` include params; Python maps `portal.services.NAV_GLYPHS` (rail), `companies.services` company nav, `documents.requirements.ACTOR_GLYPHS`, `pathways.services.DEFAULT_ICONS`, `living.catalogue.INITIAL_TOPICS`, `pages.content.ENTRANCES` / `NETWORK_ACTORS`, `portal.services` card icons, `core.chips.GLYPH` (unused). Showcase occurrences omitted.

| # | Symbol id | Concepts it stands for → where (template:line or Python map) | Sites (≈) | ⚠ Same icon, different concepts? |
|---|---|---|---|---|
| 1 | `person` | Person actor glyph (ACTOR_GLYPHS person → case responsible, next-action resp); «Personnes» audience (hero legend, network actors); pathway `family_reunification`; case ctx «Vous» fallback (`cases/detail.html:47`) | 5 | **yes** — the Persons audience, "you", and family reunification |
| 2 | `user` | Account menu summary + «Profil» (`components/account_menu.html:7,15`); message sender «L’équipe du projet» (`portal/message_detail.html:15`) | 3 | **yes** — own account vs the project team; also duplicates `person` for "a human" |
| 3 | `building` | Companies audience (hero legend, network); company actor glyph; rail «Mon entreprise» + company nav «Mon entreprise»; company dashboard glyph (`companies/dashboard.html:86`); company portal card; pathway `self_employment_entrepreneurship`; living «Services publics» | 8 | **yes** — companies vs public services vs self-employment |
| 4 | `institution` | Institutions audience (hero legend, network); actor `project_team` (ACTOR_GLYPHS); ecosystem institutions enumeration bullet (`ecosystem/institutions.html:24`); living «Service sanitaire national (SSN)» | 5 | **yes** — institutions vs the project team vs national health service |
| 5 | `university` | Universities audience (hero legend, network); actor `training_body`; rail «Academy»; ecosystem universities enumeration bullet; pathway `study_and_training_in_italy`; living «École» | 6 | **yes** — universities vs the platform's own Academy vs school |
| 6 | `briefcase` | Actor `professional`; network «Professionnels»; rail «Mes dossiers» (cases); company nav «Mes besoins»; pathway `salaried_work`; living «Fiscalité de base» | 6 | **yes** — case files vs professionals vs company needs vs salaried work vs taxation |
| 7 | `arrow` | Forward CTA / link arrow (btn--arrow, link-arrow, entry arrow, pathway-list arrow, pagination prev/next, mega-menu «Voir l’espace») | 80 calls in 45 templates | no (flips in RTL) |
| 8 | `arrow-up-right` | External authority link (`pathways/detail.html:102`) | 1 | no |
| 9 | `check` | OptionCard selected mark; notice success; message «État: lue» + «Marquer comme lue» button; rail «Processus assignés» (selection); ecosystem universities «Domaines» bullets | 6 | **yes** — success/selected vs a navigation entry vs a list bullet |
| 10 | `warning` | Notice error/warning default; form error summary; overdue due date (doc-row, dashboard & case dates); pathways warnings | 7 | minor — error vs overdue |
| 11 | `shield` | Anti-fraud (home panel, antifraud page, footer link, pathways callout); actor `authority`; ecosystem companies «guarantee» notice (`ecosystem/companies.html:39`); living «Sécurité au travail» | 7 | **yes** — anti-fraud vs public authority vs a guarantee vs work safety |
| 12 | `calendar` | Deadlines (rail «Mes échéances», deadline item, portal card); upcoming due date (doc-row, dashboard/case dates); message received date; pathways/portal date meta | 10 | no (dates) |
| 13 | `clock` | Pending notice; form unavailable; due soon (doc-row, dates) | 5 | no (waiting / soon) |
| 14 | `document` | Rail «Mes documents»; doc-row glyph + «Consulter»; portal documents card; news empty state; pathways document list bullets; «Version des règles» meta (`portal/pathways.html:37`); living «Droits et devoirs» | 8 | **yes** — documents vs rules version vs rights & duties vs news |
| 15 | `globe` | Pathway `skilled_work_eu_blue_card`; living «Langue italienne» | 2 | **yes** — EU Blue Card vs Italian language (and not used for the language selector) |
| 16 | `menu` | Hamburger: public header toggle, console bar, bottom bar «Menu»; **and** DocumentRow «more» row-actions button (`components/document_row.html:57`) | 4 | **yes** — open navigation vs row actions (a "more/kebab" glyph is missing) |
| 17 | `close` | Dialog close; banner dismiss; header toggle (open state); console drawer close; (chips.GLYPH rifiuto, unused) | 4 | no |
| 18 | `chevron` | Account menu disclosure; mega-menu panel toggle | 2 | no |
| 19 | `chevron-end` | Mega-menu sub-link bullet; rail collapse button; rail fallback glyph | 3 | minor — bullet vs collapse control |
| 20 | `plus` | Accordion expand (component); living «Santé» | 2 | **yes** — expand vs health |
| 21 | `minus` | Only `core.chips.GLYPH["nullo"]` (map never rendered) + showcase | 0 live | unused |
| 22 | `search` | Document register search field; pathway `scientific_research` | 2 | **yes** — search control vs research pathway |
| 23 | `mail` | Footer e-mail; contact/AGAMI/error/pathways interim/ecosystem e-mail links; rail «Communications»; company nav «Communications»; messages empty state; messages card | 9 | minor — e-mail address vs internal message centre |
| 24 | `phone` | — | 0 | unused |
| 25 | `lock` | Reserved-area access (utility bar, drawer, home reserved panel, access point) | 4 | no |
| 26 | `key` | Account menu «Sécurité du compte»; «Référence» meta in `portal/pathways.html:39` | 2 | **yes** — security vs a reference number; also competes with the brand's golden key (separate asset `key.svg`) |
| 27 | `info` | Notice info default; allauth alert (all levels); home orientation note; pathways info notes; «État» meta (`portal/pathways.html:38`); antifraud page FAQ link | 10 | minor — info vs status vs FAQ |
| 28 | `map-pin` | Rail «Mon parcours»; pathway `other_regular_routes`; pathway detail eyebrow default; company nav «Analyse territoriale» | 4 | **yes** — my journey vs other routes vs territorial analysis |
| 29 | `download` | Doc-row menu «Télécharger» | 1 | no |
| 30 | `home` | Account menu «Espace réservé»; rail «Tableau de bord»; company nav «Tableau de bord»; access point «Tableau de bord»; living «Logement» | 5 | **yes** — dashboard vs housing |
| 31 | `logout` | Account menu «Se déconnecter» | 1 | no |
| 32 | `settings` | — | 0 | unused |
| 33 | `quote` | — | 0 | unused |
| 34 | `list` | Rail «Mes demandes»; rail «Demandes qui me sont confiées» (helpdesk queue); requests card; doc-row menu «n dépôts» (versions); antifraud page glossary link; pathways index notice | 6 | **yes** — requests vs assigned queue vs versions vs glossary |
| 35 | `handshake` | Rail «Guichet numérique» (helpdesk); actor `authorised_actor`; pathway `training_in_origin_country` | 3 | **yes** — helpdesk vs authorised actor vs training |
| 36 | `compass` | Rail «Ma situation»; orientation CTA (`pathways/_orientation_cta.html`); portal pathways empty/restart; antifraud page «Espace Personnes» link; living «Éducation civique» | 5 | **yes** — my situation vs orientation vs civic education |

**Summary:** 32 of 36 symbols are live; **4 unused** (`phone`, `settings`, `quote`, `minus`). **19 of the 32 live symbols carry two or more unrelated concepts** (person, user, building, institution, university, briefcase, check, shield, document, globe, menu, plus, search, key, map-pin, home, list, handshake, compass — the strongest collisions: `briefcase` ×5 concepts, `building` ×3, `university` ×3, `shield` ×4, `document` ×4, `list` ×4, `menu` nav vs row actions, `home` dashboard vs housing, `plus` expand vs health). Root cause: icons are chosen in four independent Python maps (rail, actors, pathways, living topics) from one small sprite with no semantic registry. Missing glyphs implied by the UI: more/kebab, upload, external-link variant for internal, eye (password), filter, bell, sort, chat/message thread, academy/course.

---

## 8. IMAGES

### 8.1 Photo library — `static/img/photos/manifest.json` (generated by `scripts/fetch_images.py`)

All 15 photos: source **Unsplash**, licence Unsplash License, downloaded 17 Sept 2026, **author = «Unsplash contributor (author lookup unavailable offline)» for all 15** (attribution incomplete — docs/IMAGE_LICENSES.md says to complete it). Files per photo: WebP 480 / 960 / 1440 / 1920 + JPG 1440 (no 1920 for `espace-de-travail` and `salle-de-formation`: sources too narrow). No AVIF, no grading pass, no focal-point classes (all three required by CD V4 §5.2–5.3; not implemented).

| Slug | Usage slot | Subject | Consumer (code) | Rendered where | Status |
|---|---|---|---|---|---|
| `atelier-de-travail` | workshop | workshop, sticky notes on a wall | `pages.services.project_context` (`photo_for_slot("workshop")`); `ecosystem.services` SPACES pilot → `EcosystemSpace.hero_image` | «Le projet» page **and** ecosystem «Projet pilote» landing (+ og:image of project page) | ⚠ **same image, two contexts** |
| `dialogue-institutionnel` | entrance_institution | participant speaking in a meeting | `pages.services.agami_context`; ecosystem SPACES institutions | «AGAMI» promoter page **and** ecosystem «Institutions» landing | ⚠ **same image, two different concepts** (the promoter association vs the Institutions audience) |
| `equipe-entreprise` | entrance_company | three colleagues at a work table | ecosystem SPACES companies | ecosystem «Entreprises» landing | single use |
| `etudiants-bibliotheque` | entrance_university | students working in a library | ecosystem SPACES universities | ecosystem «Universités» landing | single use |
| `public-conference` | forum_event | audience in a conference room | `pages.services.network_context` | «Réseau» (network) page — **not** the forum page | slot/usage mismatch |
| `reunion-cooperation` | hero | work meeting, note-taking | `pages.seeds` → `HomeHero.image`; `build_hero` → `d.photo` | **not rendered**: the V4 hero template never reads `d.photo` (home social card stays og-default.png) | computed, unused |
| `bibliotheque-savoir` | academic | circular library (portrait) | none | — | unused |
| `campus-universitaire` | university | university façade and lawn | none | — | unused |
| `collaboration-bureau` | cooperation | two colleagues congratulate each other | none | — | unused |
| `demarches-ecriture` | living | person filling documents by hand | none (living pages have no images) | — | unused |
| `entretien-accompagnement` | entrance_person | advisory interview, laptops and notebook | none (no Persons landing photo) | — | unused |
| `espace-de-travail` | reserved_area | shared workspace seen from above (cropped to remove brands) | none (platform uses no photos by design) | — | unused |
| `micro-conference` | news_default | microphone before a conference room | none (news cards have no default image) | — | unused |
| `orientation-ecran` | orientation | hand pointing at a screen | none | — | unused |
| `salle-de-formation` | training_classroom | trainer in front of participants | none | — | unused |

**Result:** 5 of 15 photos are visible anywhere (2 of them twice); 10 are shipped but never shown. The home page shows **no photograph** besides the door; the mega-menu none; pathways/news/living/FAQ/forum (without DB image) none; the platform none (by design).

### 8.2 Brand assets and other static images

| Asset | Size | Used where | Notes |
|---|---|---|---|
| `static/brand/original/logo-mark.svg` | 1.0 KB | lock-up in public header (every public page), footer (dark variant), console rail tile, console bar tile, console drawer head (5 placements) | same asset, same concept (brand) — fine. Official brand asset (BRAND_ASSETS.md). |
| `static/brand/original/key.svg` | 0.5 KB | inside `components/doorway.html` → home hero + login stage | the golden key; never animated now. |
| `static/brand/v2/doorway-arch-400.webp` | 42 KB, 400×533 (untracked) | door photograph in home hero (preloaded LCP) **and** login/entrance stage (preloaded) | ⚠ same image in two contexts — intentional brand identity (owner's Roman fountain façade inside the arch). |
| `static/brand/v2/doorway-{480,800,1200}.{webp,avif}` | 6 files, ≈ 474 KB | **none** | orphaned after the switch to `doorway-arch-400.webp`. |
| Wordmark | text | lock-up (`{% brand_lockup %}`), `{% brand %}` spans (rail, footer inline mark, home visually-hidden H1) | text in Newsreader 600, three coloured words; not an image. |
| `static/img/grain.svg` | 0.4 KB | `.hero::before` texture 3 % multiply (home hero) | — |
| `static/img/og-default.png` | 30 KB, 1200×630 | `og:image` of every page without its own photo (incl. home) | — |
| `static/img/favicon.svg` / `favicon.ico` | — | every page | — |
| `static/img/illustrations/entrance-{person,company,institution,university}.svg` | 4 files | referenced only in `pages/content.py` (`EntranceDefault.illustration`) and passed as data; **no template renders them** | dead (retired illustrations). |
| `static/img/illustrations/orientation.svg` | 1 file | passed by `build_orientation`; not rendered | dead. |
| `static/img/illustrations/pilot-flow.svg` | 1 file | `ecosystem/pilot.html` pilot diagram | single use. |

### 8.3 Database-driven images (not enumerable offline)

| Model field | Rendered in | Notes |
|---|---|---|
| `news.Article.hero_image` | `news/_card.html` (unstyled), `news/detail.html` | no default image; card img unstyled. |
| `forum` event `hero_image`, patron partner logos, media gallery (image/video), partner logos | `forum/partials/hero.html`, `permanent_sections.html` | gallery `<img>` without width/height; video without captions. |
| `pathways` `hero_image` | `pathways/detail.html` (`.hero__figure`) | decorative flag respected. |
| `partners.Partner.logo` | `partners/index.html` (unstyled), home ecosystem (if `logo_public`) | gate G6. |
| `ecosystem.EcosystemSpace.hero_image` | ecosystem landings | seeded from slots (§8.1). |
| `pages.HomeHero.image` | computed, not rendered | see `reunion-cooperation`. |
| `SiteSettings.logo` (+ `use_logo_image`) | header, replaces the lock-up | client switch. |

### 8.4 Same image in different contexts — flags

| Image | Context A | Context B | Judgement |
|---|---|---|---|
| `dialogue-institutionnel` | AGAMI (the promoter, a private association) | Institutions audience landing | **conflicting** — the same face stands for two different actors; risks implying the promoter is an institution. |
| `atelier-de-travail` | «Le projet» (the project) | «Projet pilote» landing | overlapping — acceptable but repetitive (both reachable within two clicks). |
| `doorway-arch-400.webp` | home hero | login stage | intentional (brand door). |
| `logo-mark.svg` | public header/footer | console rail / bar / drawer | intentional (brand). |

---

## 9. FONTS — `static/css/fonts.css` (26 self-hosted woff2, `font-display` as declared, unicode-range subsets)

| Family | Files (subset × style/weight) | Tokens | Where used | Notes |
|---|---|---|---|---|
| **Newsreader** (variable 200–800, roman + italic) | 4: normal latin / latin-ext, italic latin / latin-ext | `--f-serif`, `--font-display`, `--font-heading` | **wordmark** of the lock-up (`.lock__wm`, 600, every public header + footer, console rail wordmark via `console.css`); home hero H1 (300, clamp 44→76 px); public page titles (`.page-header__title`), section titles, CTA panel titles, home section titles (components.css: 20 declarations, pages.css 9, register.css 7, base.css 7); forum titles; V2 console pages still set in serif (portal.css 4, helpdesk 2, documents 2, companies 1, selection 1). **Italic**: home forum-banner quote, forum programme note, dead institutional banner | Preloaded (normal latin) on Latin pages. Needed on **every** page because the wordmark uses it — owner has NOT authorised removing the wordmark font. Italic file loads only for the forum quote. |
| **IBM Plex Sans** 400 / 500 / 600 + 400 italic | 8: 4 styles × latin / latin-ext | `--f-sans`, `--font-ui`, `--font-body` | all interface: navigation, buttons, forms, chips, console (workspace 42 declarations, shell 12, wizard 9, hero 6, entrance 6, console 8), hero lead, body text | Preloaded 400 latin. The V4 "superfamily" choice. |
| **IBM Plex Sans Arabic** 400 / 500 / 600 | 9: 3 weights × arabic / latin / latin-ext | `--font-ui-ar`; second in `--f-sans` | Arabic UI and body on `/ar/` | Preloaded on RTL. |
| **Noto Naskh Arabic** (variable 400–700) | 3: arabic / latin / latin-ext | second in `--f-serif`; `--font-display-ar` | Arabic display/headings (hero H1, titles) on `/ar/` | Preloaded on RTL. |
| **IBM Plex Mono** 400 | 2: latin / latin-ext | `--f-mono`, `--font-ref`, `--font-mono` | folio ordinals, references (`.t-ref`, `.ctx__ref`, doc-workspace ref), counts, rule versions, voyage numerals, chip counters (workspace 6, v2/shell 2, voyage 2, chip 2, wizard 1, academy 2) | Tabular figures. |
| System Arabic stack | — | `--f-arabic-sys` | the «ع» code of the language control on non-Arabic pages | Saves the 45 KB Plex Sans Arabic on Latin pages. |
| Fira Sans / Fira Mono | **no files** | still named in `tokens.css` (`--font-ui`, `--font-ref`, `--font-ui-ar` fallback) and `v2/tokens.css` (`--f-sans`, `--f-mono`) | overridden by `v4/tokens.css` | stale references to retired fonts. |

Total self-hosted font payload in `static/fonts`: 26 files. README §4 (25/09) recorded ≈ 402 KB of fonts on the home before later reductions; this role did not re-measure.

---

## 10. Cross-cutting findings for the V5 council

| # | Finding | Evidence | Impact on "premium / coherent" |
|---|---|---|---|
| 1 | **Two design generations inside the console.** V4 is built on 5 pages (dashboard, documents register, case detail, «Ma situation», company dashboard); ≈ 40 console templates (academy, helpdesk, selection, forum governance, companies needs/profile/analysis, cases index/assessment, portal deadlines/messages/requests/pathways/message/request detail, documents requirement/upload) still use the V2 register language (portal-section + folio + register/entry + portal-facts + data-table + serif titles + V3 stamp chips). | §4 C23, C42–C51; README §4 step 15 "propagation only after PASS" | The app shell promises a 2026 product; one click away the page reverts to an editorial register. |
| 2 | **Home: only hero + navbar are V4.** Entrances, orientation, pathways, pilot, trust, antifraud, ecosystem, news, reserved, footer are V2 under V4 tokens (README §4 item 8 says so). | §3 P14–P28 | The first screen is immersive, the rest of the scroll is type-only. |
| 3 | **Unstyled surfaces** (classes with zero CSS rules): news (index, card, detail, newsletter), living (index, topic, sheet), community (9 pages), enquiry page wrappers, account profile/delete wrappers, partners index, glossary term, pathways doc/authority lists, training phases. | block→CSS map | Visibly generic pages on public paths. |
| 4 | **Parallel systems for the same job:** 3 table systems (`.table` V4 / `.data-table` V2 / `.account-table` V1); 2 wizard systems (public orientation vs «Ma situation»); 2 reveal systems; 2 news cards; 2 empty-state patterns; 3 console page-header patterns + 2 legacy bands; 2 section-header patterns; 4 CTA-band implementations; 3 filter patterns; 7 row patterns; 2 photo partials; 2 accordion markups. | §3, §4, §5 | Inconsistent rhythm, spacing and states between pages. |
| 5 | **Dead / showcase-only code:** `components/hero.html`, `institutional_banner.html` (0 includes); `tabs`, `dialog`, `stepper`, `metadata_row`, `accordion` components (showcase only); main.js steppers / counters / section-nav; `data-reveal-once`; `hx-*` without htmx; 5 retired illustrations; 6 orphaned doorway files; 10 unshown photos; 4 unused icons; CSS blocks with no markup (`.plate` 27 rules, `.home-hero` 10, `.lang-switcher` 25, `.language-switcher`, `.zones`, `.entrances`, `.portal-columns`, `.portal-table`, `col-*`, `.text-*`, several `.t-*`); `chips.GLYPH` never rendered; Motion `hover`/`press`/`SPRING_SOFT` unused. | §1.3, §3, §7, §8 | Weight and confusion for whoever builds V5; safe deletion candidates after verification. |
| 6 | **Markup defects to verify in a browser:** `.notice--warn` has no CSS (case header + dashboard suspension notices; defined modifier is `--warning`); `accounts/partials/account_menu.html` reuses `.account-menu__list`, which is `position:absolute` as a dropdown; forum gallery `<img>` without dimensions (CLS); forum `<video>` without captions; allauth alert always `info` icon; admin legalrule preview inline `style` (CSP). | §3 P7, §4 C9, P46–47 | Small but visible quality cracks. |
| 7 | **Motion inventory is thin and mostly removed:** live = header glass/height, nav spring indicator, mega-menu in, drawer slide, hero current 28 s, scroll-linked door photo + stage, voyage line, reveal (2 systems), JourneyRail draw, timeline last-node light, notch fill, strip fill, OptionCard check, wizard swap, busy meter. Removed = hero choreography, title mask reveal, console page-enter. Absent = page transitions, loaders, skeletons, toasts, list insert/remove FLIP, status-change crossfade, upload feedback, image reveals/hover. | §1.3, §2 | "Refined motion and loading states" (owner brief) has almost no footprint yet. |
| 8 | **Imagery is the largest gap versus "image-rich":** 5 photos visible site-wide, none on home besides the door, none in navigation, pathways, news defaults, living, Academy; licence authors missing for all 15; no AVIF/grading/focal system; one photo re-used for two different actors. | §8 | Direct conflict with the V5 brief; licensing debt must be cleared before any reuse. |
| 9 | **Icon semantics:** 19 of 32 live icons stand for unrelated concepts; `menu` used for both navigation and row actions; `home` for dashboard and housing; `briefcase` for five things. | §7 | Undermines "excellent UX" in the rail and the living/pathway pages. |
| 10 | **Typography is coherent in intent** (Newsreader public / Plex UI / Plex Mono refs / Arabic companions), but serif still sets V2 console titles, Fira names linger in tokens, and Newsreader must ship on every page for the wordmark. | §9 | Owner decision on the wordmark font conditions any font-budget saving. |

---

*Files used for this inventory are all under `C:/tmp/italylegalentry` (read-only). Working scripts and raw maps: `C:/tmp/ile_v5_council/scratch/{blocks.py,blocks.txt,css_only_blocks.txt,icons.py,icons.txt}`.*
