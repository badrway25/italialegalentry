# Captures and references — V5 council, Chrome Capture Specialist

Date: 26 September 2026. Browser: the visible QA Chrome, one project tab, driven through `scripts/cdp.py` (one websocket to one page target). Repository untouched (read-only phase). Every PNG lives under `C:/tmp/ile_v5_council/captures/`; every script and every machine-readable log under `C:/tmp/ile_v5_council/scratch/capture/`.

Sign-in state at hand-over: the tab is signed in as `qa-person@example.test` on `http://127.0.0.1:8771` and left on `http://127.0.0.1:8771/fr/espace-reserve/` (`Tableau de bord`). Sessions were minted server-side with `scripts/qa_chrome_signin.py` against `ile_qa`; nothing was typed into any form, no form was submitted, no password appeared anywhere.

## 1. Method

| Aspect | How it was done |
|---|---|
| Attach | `Page.attach(url_contains="127.0.0.1:")`, `Network.enable` first; every probe ends by clearing device metrics and navigating back to a `127.0.0.1` URL. |
| Desktop | `Emulation.setDeviceMetricsOverride` 1440x900, DPR 1. |
| Mobile | `Emulation.setDeviceMetricsOverride` 390x844, DPR 2, `mobile: true`; cleared after each pass. Mobile PNGs are 780x1688 device pixels. |
| First viewport | `Page.captureScreenshot` after `document.readyState == complete` plus a 1.5 s settle. |
| Full page | A warm scroll down the whole document (so lazy images and reveals fire), back to top, then a `captureBeyondViewport` clip at 1 CSS px per image px, cut at 14 000 px. |
| Loading filmstrips | `Page.startScreencast` while navigating; the frame saved for `fp+Xms` is the last compositor frame painted at or before first paint + X. `Page.captureScreenshot` blocks on a throttled renderer, so its timing lies; screencast frames carry the compositor's own timestamp. The ILE filmstrips ran under DevTools "Slow 4G" (562 ms RTT, 1.6 Mb/s) + CPU x4 with cache disabled; the reference-site filmstrips ran unthrottled (they observe the intro, they measure nothing). |
| Action frames | Screencast around a click / hover / wheel; frame saved at action + t. |
| Scroll stories | Real `Input.dispatchMouseEvent mouseWheel` steps of 800 px (desktop) / 700 px (mobile), 1.1 s between steps; on the first three steps an extra frame ~0.25 s after the wheel catches reveals in progress (`_mid`). |
| Consent | agamieuromed.org shows a cookie banner; «Refuse» (the most privacy-preserving option) was chosen at 1440 and the first viewport captured both before and after. studiobadrane.com showed no consent banner. |
| Search controls | Opened and captured, nothing typed, closed with Escape. Studiobadrane's «Play video» button was not pressed. |
| Motion audit | `MOTION_AUDIT` JS (in `cap.py`) counts transitions, animations, keyframes, `prefers-reduced-motion` blocks, dominant durations and easings; results in `scratch/capture/ref_*.json`. |

Scripts: `cap.py` (shared helpers), `p1_public.py`, `p2_loading.py`, `p3_platform.py`, `p4_platform_extra.py`, `p5_guichet_check.py`, `p6_guichet_probe.py`, `r0_recon.py`, `r1_ref.py`, `r2_ref_extra.py`. Logs: `log_*.json` (one entry per PNG: file, what it shows). Recon data: `recon_agami_*.json`, `recon_studiobadrane_*.json`. Motion/structure reports: `ref_agami_desktop.json`, `ref_agami_mobile.json`, `ref_agami_transition.json`, `ref_studiobadrane_desktop.json`, `ref_studiobadrane_mobile.json`, `ref_extra.json`.

## 2. What the BEFORE captures show (current V4 state, honest reading)

Public site (8770 interim / 8771 phase 3 open):

- Home hero (`before_home-8771_1440.png`): navy field, uppercase serif display «UN ÉCOSYSTÈME POUR LES PARCOURS RÉGULIERS VERS L'ITALIE», the doorway/arch with the golden key and a cyan wire-frame overlay, an audience list card (Personnes / Entreprises / Institutions / Universités & Formation) and two CTAs. It is the only surface with an image. On 8770 (interim, `before_home-8770_1440.png`) the hero is text only with the wordmark as title, no arch, and the nav has no chevrons.
- Mega-menu (`before_megamenu-8771_1440.png`): a plain white panel with a title, one line of description, «Voir l'espace →» and a single link («Votre parcours»). No imagery, no hierarchy, ~150 px tall on a 1440 canvas. Hover does not open it (`before_navhover-*`: panel open on hover = False); it opens on the chevron click, in ~120 ms with no visible motion between the two frames.
- Inner pages are text: `/fr/parcours/` (`before_parcours-8771_1440.png`) is a serif column with a right rail of links; the Forum page (`before_forum-8771_1440.png`) is a navy band with serif titles and a sticky sub-nav — competent, institutional, but image-less. 8770's `/fr/parcours/` is shorter (2861 px vs 4556 px full-page).
- Login (`before_login-8771_1440.png`): split layout, arch on navy at left, white card at right; the mobile login stacks the arch above the card. Reads clean but generic.
- Mobile drawer (`before_drawer-8771_390.png`): a flat list of labels with chevrons, promoter line, «Espace réservé» pill, language segmented control. No icons, no descriptions.
- Loading under slow 4G + CPU x4 (`before_loading-home-8771_1440_fp+*`): first paint 4.0 s after navigation start on 8770/8771 (uncompressed dev serving) and 2.33 s on 8772 (gzip). At fp+0.25 s only the header bar with a single nav label «Personnes» is laid out on a cream page; at fp+0.6 s the navy hero and copy are there but the arch image is missing; the arch arrives around fp+1.2 s. Nav labels pop in later (a layout-shift candidate). There is no skeleton, no progress cue, no branded loading state. (These are screencast first-paint readings, not Lighthouse LCP; the memory's 1.4–1.8 s LCP figure was measured differently.)

Platform (8771, console shell):

- Dashboard, documents, dossier, «Ma situation», entreprise (`before_dashboard_1440.png`, `before_documents_1440.png`, `before_case_1440.png`, `before_situation_1440.png`, `before_entreprise_1440.png`): navy rail with icon labels, cream canvas, white cards with hairline borders, teal primary button, IBM-Plex-style sans for UI, serif only for the Academy page. Information design is good (stepper, timeline, status chips, filters); visual identity is thin — nothing ties the console to the doorway/key identity except the small logo tile. Console loading (`before_loading-dashboard_1440_fp+0250ms.png`): the rail renders without its icons and the main column is empty until content pops in; no skeleton.
- Account menu, collapsed rail, phone drawer (`before_dashboard-accountmenu_1440.png`, `before_dashboard-railcollapsed_1440.png`, `before_console-drawer_390.png`): all work; the phone drawer is the best-looking mobile surface in the product (icon rows, sections, language control, «Site public»).
- Academy (`before_formation_1440.png`): serif catalogue with numbered rows — the one console page with typographic character.
- Forum permanent (`before_forum-permanent_1440.png`): renders in the public layout, not the console shell, with a single «Espace momentanément indisponible» notice. Placeholder state.
- Guichet numérique (`before_guichet_1440.png`, re-checked in `before_guichet_1440_recheck.png` and after a hard reload in `before_guichet_1440_reload.png`): renders UNSTYLED — rail links stacked as plain text at the top, then the bar, then the content. Diagnosis from the DOM only (`p6_guichet_probe.py`): body is `page-portal console is-ready`, `main.css` (1379 rules) and `portal/portal.css` (106) and `helpdesk/helpdesk.css` (26) are loaded, but `portal/console.css` (61 rules, the console shell's own sheet) is NOT: `templates/helpdesk/base_helpdesk.html` overrides `extra_head` and re-adds only `portal.css` + `helpdesk.css`, while `templates/portal/base_portal.html` now loads `portal.css` + `console.css`. Both templates are modified in the working tree. Not fixed here (read-only phase); reported for the council. Any other module base that overrides `extra_head` the same way (the grep lists 20 templates with `block extra_head`) deserves the same check.

Mobile public (`before_home-8771_390.png`): the arch sits above the display title; the hero is 1.8 screens tall before the first CTA; readable, not memorable.

## 3. Reference study — principles only, never copying

### 3.1 agamieuromed.org (institutional reference, the project promoter's own site)

Stack observed: custom CSS, no Bootstrap; self-written keyframes; `scroll-behavior: smooth`; `data-parallax`, `data-marquee`. Fonts: a Cormorant-class serif for display, an Inter-class sans for UI. Motion audit: 290 transitions on the home, dominant durations 0.14 s (micro), 0.24 s, 0.48–0.56 s (reveals), 1.1 s (hero plate); easings `cubic-bezier(0.2,0.7,0.2,1)` and `cubic-bezier(0.16,1,0.3,1)` (expo-out); 17 `prefers-reduced-motion` blocks; keyframes `heroPlateIn`, `navItemIn`, `numLand`, `skeleton-shimmer`, `loader-spin`, `marquee-scroll(-rtl)`, `dept-marquee(-rtl)`, `dialog-in`, `backdrop-in`, `toast-in`, `preview-pan/progress/shine`.

What gives it prestige, dynamism and premium feel (captures in brackets):

1. A branded threshold. Load and every page change pass through a navy radial curtain with the seal centred (`ref_agami_1440_load_fp+0500ms.png`, `ref_agami_1440_pagetransition_a+0700ms.png`); the page fades in under it (~1 s). A 2 px gold progress line runs along the top of the viewport and grows with scroll (visible in every `scroll*` frame). The seal reappears as a hero watermark, a floating badge and the loader — one mark, three uses.
2. Image in navigation. Each of the five hover mega-menus is a three-column link panel plus a featured image card with an italic serif description and an «Overview →» link (`ref_agami_1440_nav01…nav05`). The panel opens in ~150 ms with a subtle stagger of items (`navopen-anim_a+0080/0160`). The search icon swaps the nav for an inline search field inside the header (`ref_agami_1440_search_a+0300ms.png`).
3. A strict section grammar. Every section starts «— EYEBROW» in gold tracked capitals, then a serif title, then sans copy. Bands alternate navy / cream / white; cards use hairline borders and gold top rules rather than shadows; numerals are gold serif (`ref_agami_1440_scroll09.png`).
4. Real institutional photography, treated consistently: a full-width group photo framed by a thin gold border under the hero (`ref_agami_1440_02_first-viewport-clean.png`); a founder portrait with a sourced claim; governance and member cards shot in the same office (`scroll05`, `scroll06`); results cards in navy duotone with a year eyebrow (`scroll07`); a forum banner with a darkened Moroccan-architecture photo and centred serif (`scroll03`). People and places, no cliché objects.
5. Rhythm devices: a marquee ribbon of themes with a pause button (`scroll01_mid`), a four-pillar icon strip, a «Where would you like to start?» two-column path list with arrows (`scroll09`), a cream CTA band with a freephone chip, a newsletter band, a deep footer with a quotation (`scroll11`).
6. Mobile: a right-side drawer with a search field, icon rows (title + one-line subtitle + chevron), a gold «Join», a language grid and a contact chip (`ref_agami_390_menu-open.png`, `menu-anim_a+0100ms`); the marquee becomes a bottom ribbon with its pause control (`ref_agami_390_ar_first-viewport.png`).
7. RTL: a true mirror with Noto Naskh Arabic for display (`ref_agami_1440_ar_first-viewport.png`); the ribbon runs the other way (dedicated `-rtl` keyframes); floating controls move to the left; Latin acronyms stay upright inside Arabic lines (`ref_agami_1440_ar_scroll01.png`).

What not to take from it: the ~1 s loader is a wait the owner's LCP budget cannot afford; the hero at 1440 is text-only with the photo below the fold and the cookie banner covering the corner; two heading systems compete at the top (association name block then display title); the floating badge and back-to-top crowd the bottom-right; marquees are decoration.

### 3.2 studiobadrane.com (premium professional-services reference)

Stack observed: Bootstrap 5 + AOS (`fade-up/left/right`, 700 ms, `ease-out-cubic`, staggered delays 10–300 ms), Google Fonts Cormorant Garamond 400–700 + Inter 300–700, bootstrap-icons; `badrane-v2.css`. Motion audit: 259 transitions at 0.25 s / 0.2 s ease and 0.7 s AOS reveals, `cubic-bezier(0.22,0.6,0.36,1)` for cards; 35 reduced-motion blocks (Bootstrap's plus its own); keyframes `dropdownFadeIn`, `dropdown-open-anim`, `scrollPulse`, `t-marquee`, `urgency-pulse`. First paint 0.94 s unthrottled (0.79 s on mobile), no loader.

What gives it prestige, dynamism and premium feel:

1. Full-bleed photography under a navy gradient overlay, on every hero: open book and statue of justice on the home (`ref_studiobadrane_1440_01_first-viewport.png`), the office on «About» (`ref_studiobadrane_1440_inner_first-viewport.png`); a thin vertical gold line at the bottom centre of the hero pulses as a scroll cue.
2. Typographic pairing with a single accent: Cormorant for titles and italic taglines («Legal protection beyond borders» in gold italic), Inter for everything else in tracked uppercase for nav and eyebrows; one gold word italicised inside a white headline («An *international* legal practice»); old-style gold numerals in the stats strip with hairline separators (`stickyheader_a+0500ms`).
3. A header that earns its space: a utility row (toll-free pill, phones, email, «Calculate your compensation», IT|FR|EN|AR) over a main row with a four-language logo lock-up; after 300 px of scroll the two rows collapse into one sticky white bar with the BOOK button turning navy, within ~250 ms (`stickyheader_a+0100ms` → `a+0500ms`). Dropdowns are white panels with a gold top edge, icon-in-tinted-circle rows, the first item highlighted, group dividers (`nav01_practice-areas_click.png`); the top-level hover state is gold text plus underline (`navhover_a+0400ms`).
4. Search as a command palette: a centred dialog over a blurred page with «Esc to close / Enter to open» hints (`ref_studiobadrane_1440_search_a+0800ms.png`).
5. Cards and bands: white cards with 1 px borders that lift ~4 px with a soft shadow and darker border on hover (`cardhover_a+0400ms`); navy «Why choose» glass cards; a world-map section with gold pins and country chips over a blurred Moroccan photo (`scroll07`); the Morocco & Arab World Desk with a riad courtyard image in a rounded frame (`scroll09`); a dark «Talk to the Firm» contact card with icon rows (`scroll13`); values cards with a gold top rule and tiny «01–04» numerals (`inner_scroll02`).
6. Dynamism at low cost: AOS staggered fade-ups on every section (`scroll01_mid` vs `scroll01`), 0.2–0.25 s hover transitions everywhere, a pulsing scroll cue, an urgency pulse on the toll-free chip.
7. Mobile: a full-screen navy menu with tracked uppercase items, a gold underline under the active one, sub-menus as white panels with a gold top edge (`ref_studiobadrane_390_menu-open.png`, `menu-sub.png`); the hero keeps its photo (`ref_studiobadrane_390_01_first-viewport.png`).
8. RTL: nav, utility bar and cards mirror correctly; Noto Sans Arabic for headings (`ref_studiobadrane_1440_ar_first-viewport.png`, `ar_scroll01.png`).

What not to take from it: hero text depends on JS to appear (opacity 0 until AOS runs — `load_fp+0000ms` shows the faded headline), which is the opposite of what a strict LCP budget and a `script-src 'self'` CSP want; Google Fonts loaded remotely (ILE must self-host); a permanent «Book a Consultation» pill plus a WhatsApp FAB overlap content on every mobile frame (`ref_studiobadrane_390_scroll03.png`); the Arabic italic tagline is a synthesised oblique — Arabic should never be italicised (`ref_studiobadrane_1440_ar_first-viewport.png`); the book-and-statue photograph is the legal cliché ILE's editorial rules forbid in spirit; the two-row header is heavy on first view.

### 3.3 Principles to ADAPT for Italy Legal Entry (no layout or element copied)

1. Image as structure, through ILE's own device. Both references get their premium feel from full-bleed, consistently treated photography under a navy gradient. ILE already owns a stronger mask than either: the doorway arch. Arch-shaped image windows (CSS `clip-path`/mask, no JS) for audience cards, section openers and the login split — filled with editorially compliant Pexels imagery (people, places, workshops, campuses, civic architecture; never borders, luggage, passports, airports, tourist clichés, logos or readable third-party text), self-hosted with licence and author recorded — would give an identity neither reference has.
2. Mega-menu with a featured image and descriptions per audience (Personnes / Entreprises / Institutions / Universités & Formation), three columns of real links, opening within ~150 ms with a CSS-only stagger; hover-open on pointer devices with a click fallback and full keyboard support. Today's panel is empty.
3. A section grammar kept everywhere: gold hairline + tracked eyebrow + serif title (ILE's Newsreader) + sans body; alternating navy / cream / white bands; numbered sections (ILE already numbers 01–06 on the home — keep the numbers, add the imagery).
4. Header compaction on scroll (a scroll-driven `animation-timeline: scroll()` with an `IntersectionObserver` fallback), gold/teal underline on the active item, and the same compaction on the console bar.
5. No full-screen loader. Instead: a 2 px accent progress line at the top during navigation and scroll, cross-document View Transitions (`@view-transition { navigation: auto }`, CSS only, progressive enhancement) for a 200 ms cross-fade between pages instead of agami's 1 s curtain, and skeleton shimmer for console lists while data streams. Content must be visible without JS: reveals via `animation-timeline: view()` inside `@supports`, with `prefers-reduced-motion` turning every reveal off, never AOS-style opacity-0-until-JS.
6. Motion vocabulary from the audits: 140–240 ms for hover/focus/menus, 480–560 ms for reveals, expo-out easing (`cubic-bezier(0.16,1,0.3,1)`), gold serif numerals that «land» once on the stats strip; Motion 13 (already a dependency) only for the few sequenced moments (mega-menu stagger, stepper progress), everything else CSS.
7. Cards: hairline borders, icon in a tinted circle, hover lift ≤ 4 px with a soft shadow, gold top rule for featured cards; status chips stay as they are (they are already good).
8. Console search / command palette with keyboard hints, in the console bar (Ctrl/Cmd+K), and a «Trouver mon parcours» quick-finder on the public site.
9. Mobile drawer with icon rows (title + one-line subtitle), a language grid and a contact chip — the console drawer already has the right bones; bring the public drawer to the same level. Keep the console's bottom bar; never add a floating CTA that covers content.
10. Trust cues: patronage line, dated events with place and time, sourced claims, partner names — ILE's Forum page already carries them; make them a visible pattern (event card with a gold top rule, date/place/time icon row).
11. RTL: pick a proper Arabic display face to pair with Newsreader (Noto Naskh Arabic for display, Noto Sans Arabic for UI — self-hosted), never italicise Arabic, mirror floating controls and any ribbon direction, and re-measure every page in `ar`.
12. Loading truthfulness: on slow 4G + CPU x4 the current home paints the hero text 0.6 s after first paint and the arch 1.2 s after; the V5 hero image must be the LCP element with explicit dimensions, `fetchpriority="high"`, AVIF/WebP, and a navy placeholder of the same aspect so nothing shifts.

## 4. Capture inventory

Every file in `C:/tmp/ile_v5_council/captures/` (317 PNGs at hand-over) with what it shows, taken from the capture logs. `fp+Xms` = first paint + X (screencast frame); `a+Xms` = action + X; `_mid` = ~0.25 s after a wheel step; `_full` = full page at 1 CSS px per image px.


### Public site, 8770 (phase 3 closed, interim) — 22 files

| File | What it shows |
|---|---|
| `before_drawer-8770_390.png` | mobile navigation drawer open on http://127.0.0.1:8770/fr/ |
| `before_drawer-8770_390_t120ms.png` | mobile drawer ~120 ms after tapping Menu on http://127.0.0.1:8770/fr/ |
| `before_drawer-sub-8770_390.png` | mobile drawer with the first section's sub-menu expanded on http://127.0.0.1:8770/fr/ |
| `before_forum-8770_1440.png` | http://127.0.0.1:8770/fr/forum/ first viewport at 1440px, signed out, phase 3 closed (interim) |
| `before_forum-8770_1440_full.png` | http://127.0.0.1:8770/fr/forum/ at 1440px, signed out, phase 3 closed (interim) (full page, 1425x4748 css px) |
| `before_forum-8770_390.png` | http://127.0.0.1:8770/fr/forum/ first viewport at 390px, signed out, phase 3 closed (interim) |
| `before_forum-8770_390_full.png` | http://127.0.0.1:8770/fr/forum/ at 390px, signed out, phase 3 closed (interim) (full page, 390x6231 css px) |
| `before_home-8770_1440.png` | http://127.0.0.1:8770/fr/ first viewport at 1440px, signed out, phase 3 closed (interim) |
| `before_home-8770_1440_full.png` | http://127.0.0.1:8770/fr/ at 1440px, signed out, phase 3 closed (interim) (full page, 1425x5751 css px) |
| `before_home-8770_390.png` | http://127.0.0.1:8770/fr/ first viewport at 390px, signed out, phase 3 closed (interim) |
| `before_home-8770_390_full.png` | http://127.0.0.1:8770/fr/ at 390px, signed out, phase 3 closed (interim) (full page, 390x7728 css px) |
| `before_login-8770_1440.png` | http://127.0.0.1:8770/fr/compte/login/ first viewport at 1440px, signed out, phase 3 closed (interim) |
| `before_login-8770_1440_full.png` | http://127.0.0.1:8770/fr/compte/login/ at 1440px, signed out, phase 3 closed (interim) (full page, 1425x1530 css px) |
| `before_login-8770_390.png` | http://127.0.0.1:8770/fr/compte/login/ first viewport at 390px, signed out, phase 3 closed (interim) |
| `before_login-8770_390_full.png` | http://127.0.0.1:8770/fr/compte/login/ at 390px, signed out, phase 3 closed (interim) (full page, 390x1904 css px) |
| `before_megamenu-8770_1440.png` | mega-menu of the first section open (chevron clicked) on http://127.0.0.1:8770/fr/ |
| `before_megamenu-8770_1440_t120ms.png` | mega-menu of the first section ~120 ms after clicking its chevron (http://127.0.0.1:8770/fr/) |
| `before_navhover-8770_1440.png` | pointer hovering the first section link on http://127.0.0.1:8770/fr/ (panel open on hover: False) |
| `before_parcours-8770_1440.png` | http://127.0.0.1:8770/fr/parcours/ first viewport at 1440px, signed out, phase 3 closed (interim) |
| `before_parcours-8770_1440_full.png` | http://127.0.0.1:8770/fr/parcours/ at 1440px, signed out, phase 3 closed (interim) (full page, 1425x2853 css px) |
| `before_parcours-8770_390.png` | http://127.0.0.1:8770/fr/parcours/ first viewport at 390px, signed out, phase 3 closed (interim) |
| `before_parcours-8770_390_full.png` | http://127.0.0.1:8770/fr/parcours/ at 390px, signed out, phase 3 closed (interim) (full page, 390x2838 css px) |

### Public site, 8771 (phase 3 open) — 22 files

| File | What it shows |
|---|---|
| `before_drawer-8771_390.png` | mobile navigation drawer open on http://127.0.0.1:8771/fr/ |
| `before_drawer-8771_390_t120ms.png` | mobile drawer ~120 ms after tapping Menu on http://127.0.0.1:8771/fr/ |
| `before_drawer-sub-8771_390.png` | mobile drawer with the first section's sub-menu expanded on http://127.0.0.1:8771/fr/ |
| `before_forum-8771_1440.png` | http://127.0.0.1:8771/fr/forum/ first viewport at 1440px, signed out, phase 3 open |
| `before_forum-8771_1440_full.png` | http://127.0.0.1:8771/fr/forum/ at 1440px, signed out, phase 3 open (full page, 1425x4360 css px) |
| `before_forum-8771_390.png` | http://127.0.0.1:8771/fr/forum/ first viewport at 390px, signed out, phase 3 open |
| `before_forum-8771_390_full.png` | http://127.0.0.1:8771/fr/forum/ at 390px, signed out, phase 3 open (full page, 390x5768 css px) |
| `before_home-8771_1440.png` | http://127.0.0.1:8771/fr/ first viewport at 1440px, signed out, phase 3 open |
| `before_home-8771_1440_full.png` | http://127.0.0.1:8771/fr/ at 1440px, signed out, phase 3 open (full page, 1425x7813 css px) |
| `before_home-8771_390.png` | http://127.0.0.1:8771/fr/ first viewport at 390px, signed out, phase 3 open |
| `before_home-8771_390_full.png` | http://127.0.0.1:8771/fr/ at 390px, signed out, phase 3 open (full page, 390x11080 css px) |
| `before_login-8771_1440.png` | http://127.0.0.1:8771/fr/compte/login/ first viewport at 1440px, signed out, phase 3 open |
| `before_login-8771_1440_full.png` | http://127.0.0.1:8771/fr/compte/login/ at 1440px, signed out, phase 3 open (full page, 1425x1627 css px) |
| `before_login-8771_390.png` | http://127.0.0.1:8771/fr/compte/login/ first viewport at 390px, signed out, phase 3 open |
| `before_login-8771_390_full.png` | http://127.0.0.1:8771/fr/compte/login/ at 390px, signed out, phase 3 open (full page, 390x2054 css px) |
| `before_megamenu-8771_1440.png` | mega-menu of the first section open (chevron clicked) on http://127.0.0.1:8771/fr/ |
| `before_megamenu-8771_1440_t120ms.png` | mega-menu of the first section ~120 ms after clicking its chevron (http://127.0.0.1:8771/fr/) |
| `before_navhover-8771_1440.png` | pointer hovering the first section link on http://127.0.0.1:8771/fr/ (panel open on hover: False) |
| `before_parcours-8771_1440.png` | http://127.0.0.1:8771/fr/parcours/ first viewport at 1440px, signed out, phase 3 open |
| `before_parcours-8771_1440_full.png` | http://127.0.0.1:8771/fr/parcours/ at 1440px, signed out, phase 3 open (full page, 1425x3579 css px) |
| `before_parcours-8771_390.png` | http://127.0.0.1:8771/fr/parcours/ first viewport at 390px, signed out, phase 3 open |
| `before_parcours-8771_390_full.png` | http://127.0.0.1:8771/fr/parcours/ at 390px, signed out, phase 3 open (full page, 390x5782 css px) |

### Loading filmstrips, public home (slow 4G + CPU x4, cache disabled) — 30 files

| File | What it shows |
|---|---|
| `before_loading-home-8770_1440_fp+0000ms.png` | http://127.0.0.1:8770/fr/ loading under slow 4G + CPU x4, cache disabled, at 1440px — first paint + 0.0s (first paint 4.00s after navigation start; frame stamped 4.00s) |
| `before_loading-home-8770_1440_fp+0250ms.png` | http://127.0.0.1:8770/fr/ loading under slow 4G + CPU x4, cache disabled, at 1440px — first paint + 0.2s (first paint 4.00s after navigation start; frame stamped 4.14s) |
| `before_loading-home-8770_1440_fp+0600ms.png` | http://127.0.0.1:8770/fr/ loading under slow 4G + CPU x4, cache disabled, at 1440px — first paint + 0.6s (first paint 4.00s after navigation start; frame stamped 4.35s) |
| `before_loading-home-8770_1440_fp+1200ms.png` | http://127.0.0.1:8770/fr/ loading under slow 4G + CPU x4, cache disabled, at 1440px — first paint + 1.2s (first paint 4.00s after navigation start; frame stamped 5.18s) |
| `before_loading-home-8770_1440_fp+2500ms.png` | http://127.0.0.1:8770/fr/ loading under slow 4G + CPU x4, cache disabled, at 1440px — first paint + 2.5s (first paint 4.00s after navigation start; frame stamped 6.47s) |
| `before_loading-home-8770_390_fp+0000ms.png` | http://127.0.0.1:8770/fr/ loading under slow 4G + CPU x4, cache disabled, at 390px — first paint + 0.0s (first paint 4.16s after navigation start; frame stamped 4.16s) |
| `before_loading-home-8770_390_fp+0250ms.png` | http://127.0.0.1:8770/fr/ loading under slow 4G + CPU x4, cache disabled, at 390px — first paint + 0.2s (first paint 4.16s after navigation start; frame stamped 4.16s) |
| `before_loading-home-8770_390_fp+0600ms.png` | http://127.0.0.1:8770/fr/ loading under slow 4G + CPU x4, cache disabled, at 390px — first paint + 0.6s (first paint 4.16s after navigation start; frame stamped 4.75s) |
| `before_loading-home-8770_390_fp+1200ms.png` | http://127.0.0.1:8770/fr/ loading under slow 4G + CPU x4, cache disabled, at 390px — first paint + 1.2s (first paint 4.16s after navigation start; frame stamped 5.21s) |
| `before_loading-home-8770_390_fp+2500ms.png` | http://127.0.0.1:8770/fr/ loading under slow 4G + CPU x4, cache disabled, at 390px — first paint + 2.5s (first paint 4.16s after navigation start; frame stamped 6.50s) |
| `before_loading-home-8771_1440_fp+0000ms.png` | http://127.0.0.1:8771/fr/ loading under slow 4G + CPU x4, cache disabled, at 1440px — first paint + 0.0s (first paint 4.02s after navigation start; frame stamped 4.02s) |
| `before_loading-home-8771_1440_fp+0250ms.png` | http://127.0.0.1:8771/fr/ loading under slow 4G + CPU x4, cache disabled, at 1440px — first paint + 0.2s (first paint 4.02s after navigation start; frame stamped 4.21s) |
| `before_loading-home-8771_1440_fp+0600ms.png` | http://127.0.0.1:8771/fr/ loading under slow 4G + CPU x4, cache disabled, at 1440px — first paint + 0.6s (first paint 4.02s after navigation start; frame stamped 4.46s) |
| `before_loading-home-8771_1440_fp+1200ms.png` | http://127.0.0.1:8771/fr/ loading under slow 4G + CPU x4, cache disabled, at 1440px — first paint + 1.2s (first paint 4.02s after navigation start; frame stamped 4.96s) |
| `before_loading-home-8771_1440_fp+2500ms.png` | http://127.0.0.1:8771/fr/ loading under slow 4G + CPU x4, cache disabled, at 1440px — first paint + 2.5s (first paint 4.02s after navigation start; frame stamped 6.51s) |
| `before_loading-home-8771_390_fp+0000ms.png` | http://127.0.0.1:8771/fr/ loading under slow 4G + CPU x4, cache disabled, at 390px — first paint + 0.0s (first paint 4.04s after navigation start; frame stamped 4.04s) |
| `before_loading-home-8771_390_fp+0250ms.png` | http://127.0.0.1:8771/fr/ loading under slow 4G + CPU x4, cache disabled, at 390px — first paint + 0.2s (first paint 4.04s after navigation start; frame stamped 4.19s) |
| `before_loading-home-8771_390_fp+0600ms.png` | http://127.0.0.1:8771/fr/ loading under slow 4G + CPU x4, cache disabled, at 390px — first paint + 0.6s (first paint 4.04s after navigation start; frame stamped 4.64s) |
| `before_loading-home-8771_390_fp+1200ms.png` | http://127.0.0.1:8771/fr/ loading under slow 4G + CPU x4, cache disabled, at 390px — first paint + 1.2s (first paint 4.04s after navigation start; frame stamped 5.14s) |
| `before_loading-home-8771_390_fp+2500ms.png` | http://127.0.0.1:8771/fr/ loading under slow 4G + CPU x4, cache disabled, at 390px — first paint + 2.5s (first paint 4.04s after navigation start; frame stamped 6.37s) |
| `before_loading-home-8772gzip_1440_fp+0000ms.png` | http://127.0.0.1:8772/fr/ loading under slow 4G + CPU x4, cache disabled, at 1440px — first paint + 0.0s (first paint 2.33s after navigation start; frame stamped 2.33s) |
| `before_loading-home-8772gzip_1440_fp+0250ms.png` | http://127.0.0.1:8772/fr/ loading under slow 4G + CPU x4, cache disabled, at 1440px — first paint + 0.2s (first paint 2.33s after navigation start; frame stamped 2.52s) |
| `before_loading-home-8772gzip_1440_fp+0600ms.png` | http://127.0.0.1:8772/fr/ loading under slow 4G + CPU x4, cache disabled, at 1440px — first paint + 0.6s (first paint 2.33s after navigation start; frame stamped 2.74s) |
| `before_loading-home-8772gzip_1440_fp+1200ms.png` | http://127.0.0.1:8772/fr/ loading under slow 4G + CPU x4, cache disabled, at 1440px — first paint + 1.2s (first paint 2.33s after navigation start; frame stamped 3.38s) |
| `before_loading-home-8772gzip_1440_fp+2500ms.png` | http://127.0.0.1:8772/fr/ loading under slow 4G + CPU x4, cache disabled, at 1440px — first paint + 2.5s (first paint 2.33s after navigation start; frame stamped 4.79s) |
| `before_loading-home-8772gzip_390_fp+0000ms.png` | http://127.0.0.1:8772/fr/ loading under slow 4G + CPU x4, cache disabled, at 390px — first paint + 0.0s (first paint 2.51s after navigation start; frame stamped 2.51s) |
| `before_loading-home-8772gzip_390_fp+0250ms.png` | http://127.0.0.1:8772/fr/ loading under slow 4G + CPU x4, cache disabled, at 390px — first paint + 0.2s (first paint 2.51s after navigation start; frame stamped 2.70s) |
| `before_loading-home-8772gzip_390_fp+0600ms.png` | http://127.0.0.1:8772/fr/ loading under slow 4G + CPU x4, cache disabled, at 390px — first paint + 0.6s (first paint 2.51s after navigation start; frame stamped 3.11s) |
| `before_loading-home-8772gzip_390_fp+1200ms.png` | http://127.0.0.1:8772/fr/ loading under slow 4G + CPU x4, cache disabled, at 390px — first paint + 1.2s (first paint 2.51s after navigation start; frame stamped 3.69s) |
| `before_loading-home-8772gzip_390_fp+2500ms.png` | http://127.0.0.1:8772/fr/ loading under slow 4G + CPU x4, cache disabled, at 390px — first paint + 2.5s (first paint 2.51s after navigation start; frame stamped 4.94s) |

### Loading filmstrip, console dashboard (slow 4G + CPU x4, cache disabled) — 10 files

| File | What it shows |
|---|---|
| `before_loading-dashboard_1440_fp+0000ms.png` | http://127.0.0.1:8771/fr/espace-reserve/ (signed in) loading under slow 4G + CPU x4, cache disabled, at 1440px — first paint + 0.0s (first paint 3.86s after navigation start; frame stamped 3.86s) |
| `before_loading-dashboard_1440_fp+0250ms.png` | http://127.0.0.1:8771/fr/espace-reserve/ (signed in) loading under slow 4G + CPU x4, cache disabled, at 1440px — first paint + 0.2s (first paint 3.86s after navigation start; frame stamped 3.91s) |
| `before_loading-dashboard_1440_fp+0600ms.png` | http://127.0.0.1:8771/fr/espace-reserve/ (signed in) loading under slow 4G + CPU x4, cache disabled, at 1440px — first paint + 0.6s (first paint 3.86s after navigation start; frame stamped 4.45s) |
| `before_loading-dashboard_1440_fp+1200ms.png` | http://127.0.0.1:8771/fr/espace-reserve/ (signed in) loading under slow 4G + CPU x4, cache disabled, at 1440px — first paint + 1.2s (first paint 3.86s after navigation start; frame stamped 5.05s) |
| `before_loading-dashboard_1440_fp+2500ms.png` | http://127.0.0.1:8771/fr/espace-reserve/ (signed in) loading under slow 4G + CPU x4, cache disabled, at 1440px — first paint + 2.5s (first paint 3.86s after navigation start; frame stamped 6.00s) |
| `before_loading-dashboard_390_fp+0000ms.png` | http://127.0.0.1:8771/fr/espace-reserve/ (signed in) loading under slow 4G + CPU x4, cache disabled, at 390px — first paint + 0.0s (first paint 3.79s after navigation start; frame stamped 3.79s) |
| `before_loading-dashboard_390_fp+0250ms.png` | http://127.0.0.1:8771/fr/espace-reserve/ (signed in) loading under slow 4G + CPU x4, cache disabled, at 390px — first paint + 0.2s (first paint 3.79s after navigation start; frame stamped 3.95s) |
| `before_loading-dashboard_390_fp+0600ms.png` | http://127.0.0.1:8771/fr/espace-reserve/ (signed in) loading under slow 4G + CPU x4, cache disabled, at 390px — first paint + 0.6s (first paint 3.79s after navigation start; frame stamped 4.39s) |
| `before_loading-dashboard_390_fp+1200ms.png` | http://127.0.0.1:8771/fr/espace-reserve/ (signed in) loading under slow 4G + CPU x4, cache disabled, at 390px — first paint + 1.2s (first paint 3.79s after navigation start; frame stamped 4.99s) |
| `before_loading-dashboard_390_fp+2500ms.png` | http://127.0.0.1:8771/fr/espace-reserve/ (signed in) loading under slow 4G + CPU x4, cache disabled, at 390px — first paint + 2.5s (first paint 3.79s after navigation start; frame stamped 5.81s) |

### Platform, signed in as qa-doc-person on 8771 — 30 files

| File | What it shows |
|---|---|
| `before_case_1440.png` | http://127.0.0.1:8771/fr/espace-reserve/dossiers/EE167596D4/ first viewport at 1440px, signed in as qa-doc-person@example.test (h1: Dossier EE167596D4; landed /fr/espace-reserve/dossiers/EE167596D4/) |
| `before_case_1440_full.png` | http://127.0.0.1:8771/fr/espace-reserve/dossiers/EE167596D4/ at 1440px, signed in as qa-doc-person@example.test (full page, 1425x1775 css px) |
| `before_case_390.png` | http://127.0.0.1:8771/fr/espace-reserve/dossiers/EE167596D4/ first viewport at 390px, signed in as qa-doc-person@example.test (h1: Dossier EE167596D4; landed /fr/espace-reserve/dossiers/EE167596D4/) |
| `before_case_390_full.png` | http://127.0.0.1:8771/fr/espace-reserve/dossiers/EE167596D4/ at 390px, signed in as qa-doc-person@example.test (full page, 390x2834 css px) |
| `before_dashboard_1440.png` | http://127.0.0.1:8771/fr/espace-reserve/ first viewport at 1440px, signed in as qa-doc-person@example.test (h1: Tableau de bord; landed /fr/espace-reserve/) |
| `before_dashboard_1440_full.png` | http://127.0.0.1:8771/fr/espace-reserve/ at 1440px, signed in as qa-doc-person@example.test (full page, 1425x1867 css px) |
| `before_dashboard_390.png` | http://127.0.0.1:8771/fr/espace-reserve/ first viewport at 390px, signed in as qa-doc-person@example.test (h1: Tableau de bord; landed /fr/espace-reserve/) |
| `before_dashboard_390_full.png` | http://127.0.0.1:8771/fr/espace-reserve/ at 390px, signed in as qa-doc-person@example.test (full page, 390x3007 css px) |
| `before_documents_1440.png` | http://127.0.0.1:8771/fr/espace-reserve/mes-documents/ first viewport at 1440px, signed in as qa-doc-person@example.test (h1: Mes pièces; landed /fr/espace-reserve/mes-documents/) |
| `before_documents_1440_full.png` | http://127.0.0.1:8771/fr/espace-reserve/mes-documents/ at 1440px, signed in as qa-doc-person@example.test (full page, 1425x1458 css px) |
| `before_documents_390.png` | http://127.0.0.1:8771/fr/espace-reserve/mes-documents/ first viewport at 390px, signed in as qa-doc-person@example.test (h1: Mes pièces; landed /fr/espace-reserve/mes-documents/) |
| `before_documents_390_full.png` | http://127.0.0.1:8771/fr/espace-reserve/mes-documents/ at 390px, signed in as qa-doc-person@example.test (full page, 390x2559 css px) |
| `before_formation_1440.png` | http://127.0.0.1:8771/fr/espace-reserve/formation/ first viewport at 1440px, signed in as qa-doc-person@example.test (h1: Academy; landed /fr/espace-reserve/formation/) |
| `before_formation_1440_full.png` | http://127.0.0.1:8771/fr/espace-reserve/formation/ at 1440px, signed in as qa-doc-person@example.test (full page, 1425x2277 css px) |
| `before_formation_390.png` | http://127.0.0.1:8771/fr/espace-reserve/formation/ first viewport at 390px, signed in as qa-doc-person@example.test (h1: Academy; landed /fr/espace-reserve/formation/) |
| `before_formation_390_full.png` | http://127.0.0.1:8771/fr/espace-reserve/formation/ at 390px, signed in as qa-doc-person@example.test (full page, 390x2971 css px) |
| `before_forum-permanent_1440.png` | http://127.0.0.1:8771/fr/espace-reserve/forum-permanent/ first viewport at 1440px, signed in as qa-doc-person@example.test (h1: Forum permanent; landed /fr/espace-reserve/forum-permanent/) |
| `before_forum-permanent_1440_full.png` | http://127.0.0.1:8771/fr/espace-reserve/forum-permanent/ at 1440px, signed in as qa-doc-person@example.test (full page, 1425x1322 css px) |
| `before_forum-permanent_390.png` | http://127.0.0.1:8771/fr/espace-reserve/forum-permanent/ first viewport at 390px, signed in as qa-doc-person@example.test (h1: Forum permanent; landed /fr/espace-reserve/forum-permanent/) |
| `before_forum-permanent_390_full.png` | http://127.0.0.1:8771/fr/espace-reserve/forum-permanent/ at 390px, signed in as qa-doc-person@example.test (full page, 390x2030 css px) |
| `before_guichet_1440.png` | http://127.0.0.1:8771/fr/espace-reserve/guichet/ first viewport at 1440px, signed in as qa-doc-person@example.test (h1: Guichet numérique; landed /fr/espace-reserve/guichet/) |
| `before_guichet_1440_full.png` | http://127.0.0.1:8771/fr/espace-reserve/guichet/ at 1440px, signed in as qa-doc-person@example.test (full page, 1425x2315 css px) |
| `before_guichet_1440_recheck.png` | http://127.0.0.1:8771/fr/espace-reserve/guichet/ re-captured at 1440px after a 2 s settle, signed in as qa-doc-person@example.test: confirms whether the unstyled rendering is a capture race or the page state |
| `before_guichet_1440_reload.png` | http://127.0.0.1:8771/fr/espace-reserve/guichet/ at 1440px after a hard reload (ignoreCache), signed in as qa-doc-person@example.test |
| `before_guichet_390.png` | http://127.0.0.1:8771/fr/espace-reserve/guichet/ first viewport at 390px, signed in as qa-doc-person@example.test (h1: Guichet numérique; landed /fr/espace-reserve/guichet/) |
| `before_guichet_390_full.png` | http://127.0.0.1:8771/fr/espace-reserve/guichet/ at 390px, signed in as qa-doc-person@example.test (full page, 390x2243 css px) |
| `before_situation_1440.png` | http://127.0.0.1:8771/fr/espace-reserve/ma-situation/ first viewport at 1440px, signed in as qa-doc-person@example.test (h1: Ma situation; landed /fr/espace-reserve/ma-situation/) |
| `before_situation_1440_full.png` | http://127.0.0.1:8771/fr/espace-reserve/ma-situation/ at 1440px, signed in as qa-doc-person@example.test (full page, 1425x1366 css px) |
| `before_situation_390.png` | http://127.0.0.1:8771/fr/espace-reserve/ma-situation/ first viewport at 390px, signed in as qa-doc-person@example.test (h1: Ma situation; landed /fr/espace-reserve/ma-situation/) |
| `before_situation_390_full.png` | http://127.0.0.1:8771/fr/espace-reserve/ma-situation/ at 390px, signed in as qa-doc-person@example.test (full page, 390x1514 css px) |

### Platform, console shell states (qa-doc-person) — 4 files

| File | What it shows |
|---|---|
| `before_console-drawer_390.png` | console drawer (whole rail) open on the phone |
| `before_console-drawer_390_t150ms.png` | console drawer on the phone ~150 ms after tapping Menu in the bottom bar |
| `before_dashboard-accountmenu_1440.png` | console dashboard at 1440px with the account menu (Personne) open |
| `before_dashboard-railcollapsed_1440.png` | console dashboard at 1440px with the rail collapsed («Réduire la navigation») |

### Platform, signed in as qa-company on 8771 — 4 files

| File | What it shows |
|---|---|
| `before_entreprise_1440.png` | http://127.0.0.1:8771/fr/espace-reserve/entreprise/ first viewport at 1440px, signed in as qa-company@example.test (h1: Cantiere Adriatico S.r.l.; landed /fr/espace-reserve/entreprise/) |
| `before_entreprise_1440_full.png` | http://127.0.0.1:8771/fr/espace-reserve/entreprise/ at 1440px, signed in as qa-company@example.test (full page, 1425x1440 css px) |
| `before_entreprise_390.png` | http://127.0.0.1:8771/fr/espace-reserve/entreprise/ first viewport at 390px, signed in as qa-company@example.test (h1: Cantiere Adriatico S.r.l.; landed /fr/espace-reserve/entreprise/) |
| `before_entreprise_390_full.png` | http://127.0.0.1:8771/fr/espace-reserve/entreprise/ at 390px, signed in as qa-company@example.test (full page, 390x2749 css px) |

### Reference: agamieuromed.org at 1440 — 50 files

| File | What it shows |
|---|---|
| `ref_agami_1440_01_first-viewport.png` | https://agamieuromed.org/en/ first viewport at 1440px as a new visitor (any consent banner left as shown) |
| `ref_agami_1440_02_first-viewport-clean.png` | https://agamieuromed.org/en/ first viewport at 1440px after choosing «Refuse» on the cookie banner (most privacy-preserving option) |
| `ref_agami_1440_ar_first-viewport.png` | https://agamieuromed.org/ar/ first viewport at 1440px (dir=rtl, RTL reference) |
| `ref_agami_1440_ar_scroll01.png` | https://agamieuromed.org/ar/ at 1440px after one wheel step (RTL marquee, ribbon and section header) |
| `ref_agami_1440_inner_first-viewport.png` | inner page https://agamieuromed.org/en/dipartimenti/ first viewport at 1440px |
| `ref_agami_1440_inner_scroll01.png` | inner page https://agamieuromed.org/en/dipartimenti/ at 1440px after one wheel step |
| `ref_agami_1440_load_fp+0000ms.png` | https://agamieuromed.org loading at 1440px (no throttling) — first paint + 0.0s (first paint 1.93s after navigation start; frame stamped 1.93s) |
| `ref_agami_1440_load_fp+0200ms.png` | https://agamieuromed.org loading at 1440px (no throttling) — first paint + 0.2s (first paint 1.93s after navigation start; frame stamped 2.13s) |
| `ref_agami_1440_load_fp+0500ms.png` | https://agamieuromed.org loading at 1440px (no throttling) — first paint + 0.5s (first paint 1.93s after navigation start; frame stamped 2.40s) |
| `ref_agami_1440_load_fp+0900ms.png` | https://agamieuromed.org loading at 1440px (no throttling) — first paint + 0.9s (first paint 1.93s after navigation start; frame stamped 2.81s) |
| `ref_agami_1440_load_fp+1500ms.png` | https://agamieuromed.org loading at 1440px (no throttling) — first paint + 1.5s (first paint 1.93s after navigation start; frame stamped 2.96s) |
| `ref_agami_1440_load_fp+2500ms.png` | https://agamieuromed.org loading at 1440px (no throttling) — first paint + 2.5s (first paint 1.93s after navigation start; frame stamped 2.96s) |
| `ref_agami_1440_load_fp+4000ms.png` | https://agamieuromed.org loading at 1440px (no throttling) — first paint + 4.0s (first paint 1.93s after navigation start; frame stamped 2.96s) |
| `ref_agami_1440_nav01_agamiidentity-history-an_hover.png` | https://agamieuromed.org/en/ at 1440px, pointer hovering the top-level item «AGAMIIdentity, history and organisation» (13 extra visible links: dropdown open) |
| `ref_agami_1440_nav02_international-cooperatio_hover.png` | https://agamieuromed.org/en/ at 1440px, pointer hovering the top-level item «International cooperationItaly, Morocco, Europe and the Mediterranean» (12 extra visible links: dropdown open) |
| `ref_agami_1440_nav03_research-and-trainingres_hover.png` | https://agamieuromed.org/en/ at 1440px, pointer hovering the top-level item «Research and trainingResearch Center, Journal and library» (10 extra visible links: dropdown open) |
| `ref_agami_1440_nav04_projectsprogrammes-netwo_hover.png` | https://agamieuromed.org/en/ at 1440px, pointer hovering the top-level item «ProjectsProgrammes, networks and opportunities» (10 extra visible links: dropdown open) |
| `ref_agami_1440_nav05_eventsevents-news-and-pr_hover.png` | https://agamieuromed.org/en/ at 1440px, pointer hovering the top-level item «EventsEvents, news and press area» (5 extra visible links: dropdown open) |
| `ref_agami_1440_navopen-anim_a+0000ms.png` | https://agamieuromed.org/en/ at 1440px, dropdown «AGAMIIdentity, history and organisation» opening on hover — action + 0.00s (frame stamped -1.04s) |
| `ref_agami_1440_navopen-anim_a+0080ms.png` | https://agamieuromed.org/en/ at 1440px, dropdown «AGAMIIdentity, history and organisation» opening on hover — action + 0.08s (frame stamped +0.05s) |
| `ref_agami_1440_navopen-anim_a+0160ms.png` | https://agamieuromed.org/en/ at 1440px, dropdown «AGAMIIdentity, history and organisation» opening on hover — action + 0.16s (frame stamped +0.15s) |
| `ref_agami_1440_navopen-anim_a+0300ms.png` | https://agamieuromed.org/en/ at 1440px, dropdown «AGAMIIdentity, history and organisation» opening on hover — action + 0.30s (frame stamped +0.27s) |
| `ref_agami_1440_navopen-anim_a+0600ms.png` | https://agamieuromed.org/en/ at 1440px, dropdown «AGAMIIdentity, history and organisation» opening on hover — action + 0.60s (frame stamped +0.42s) |
| `ref_agami_1440_pagetransition_a+0000ms.png` | click on «Discover the Departments» → https://agamieuromed.org/en/dipartimenti/ at 1440px: what the visitor sees between pages — action + 0.00s (frame stamped -1.06s) |
| `ref_agami_1440_pagetransition_a+0150ms.png` | click on «Discover the Departments» → https://agamieuromed.org/en/dipartimenti/ at 1440px: what the visitor sees between pages — action + 0.15s (frame stamped +0.04s) |
| `ref_agami_1440_pagetransition_a+0350ms.png` | click on «Discover the Departments» → https://agamieuromed.org/en/dipartimenti/ at 1440px: what the visitor sees between pages — action + 0.35s (frame stamped +0.34s) |
| `ref_agami_1440_pagetransition_a+0700ms.png` | click on «Discover the Departments» → https://agamieuromed.org/en/dipartimenti/ at 1440px: what the visitor sees between pages — action + 0.70s (frame stamped +0.68s) |
| `ref_agami_1440_pagetransition_a+1200ms.png` | click on «Discover the Departments» → https://agamieuromed.org/en/dipartimenti/ at 1440px: what the visitor sees between pages — action + 1.20s (frame stamped +1.19s) |
| `ref_agami_1440_pagetransition_a+2000ms.png` | click on «Discover the Departments» → https://agamieuromed.org/en/dipartimenti/ at 1440px: what the visitor sees between pages — action + 2.00s (frame stamped +1.99s) |
| `ref_agami_1440_pagetransition_a+3500ms.png` | click on «Discover the Departments» → https://agamieuromed.org/en/dipartimenti/ at 1440px: what the visitor sees between pages — action + 3.50s (frame stamped +3.49s) |
| `ref_agami_1440_scroll01.png` | https://agamieuromed.org at 1440px after wheel step 1 (mouseWheel, scrollY=784) |
| `ref_agami_1440_scroll01_mid.png` | https://agamieuromed.org at 1440px ~0.25 s after wheel step 1 (reveal/transition in progress) |
| `ref_agami_1440_scroll02.png` | https://agamieuromed.org at 1440px after wheel step 2 (mouseWheel, scrollY=1584) |
| `ref_agami_1440_scroll02_mid.png` | https://agamieuromed.org at 1440px ~0.25 s after wheel step 2 (reveal/transition in progress) |
| `ref_agami_1440_scroll03.png` | https://agamieuromed.org at 1440px after wheel step 3 (mouseWheel, scrollY=2384) |
| `ref_agami_1440_scroll03_mid.png` | https://agamieuromed.org at 1440px ~0.25 s after wheel step 3 (reveal/transition in progress) |
| `ref_agami_1440_scroll04.png` | https://agamieuromed.org at 1440px after wheel step 4 (mouseWheel, scrollY=3184) |
| `ref_agami_1440_scroll05.png` | https://agamieuromed.org at 1440px after wheel step 5 (mouseWheel, scrollY=3984) |
| `ref_agami_1440_scroll06.png` | https://agamieuromed.org at 1440px after wheel step 6 (mouseWheel, scrollY=4784) |
| `ref_agami_1440_scroll07.png` | https://agamieuromed.org at 1440px after wheel step 7 (mouseWheel, scrollY=5584) |
| `ref_agami_1440_scroll08.png` | https://agamieuromed.org at 1440px after wheel step 8 (mouseWheel, scrollY=6384) |
| `ref_agami_1440_scroll09.png` | https://agamieuromed.org at 1440px after wheel step 9 (mouseWheel, scrollY=7184) |
| `ref_agami_1440_scroll10.png` | https://agamieuromed.org at 1440px after wheel step 10 (mouseWheel, scrollY=7984) |
| `ref_agami_1440_scroll11.png` | https://agamieuromed.org at 1440px after wheel step 11 (mouseWheel, scrollY=8784) |
| `ref_agami_1440_scroll12.png` | https://agamieuromed.org at 1440px after wheel step 12 (mouseWheel, scrollY=8982) |
| `ref_agami_1440_scroll13.png` | https://agamieuromed.org at 1440px after wheel step 13 (mouseWheel, scrollY=8982) |
| `ref_agami_1440_search_a+0000ms.png` | https://agamieuromed.org/en/ at 1440px, search overlay opening (nothing typed, nothing submitted) — action + 0.00s (frame stamped -1.04s) |
| `ref_agami_1440_search_a+0120ms.png` | https://agamieuromed.org/en/ at 1440px, search overlay opening (nothing typed, nothing submitted) — action + 0.12s (frame stamped +0.10s) |
| `ref_agami_1440_search_a+0300ms.png` | https://agamieuromed.org/en/ at 1440px, search overlay opening (nothing typed, nothing submitted) — action + 0.30s (frame stamped +0.26s) |
| `ref_agami_1440_search_a+0800ms.png` | https://agamieuromed.org/en/ at 1440px, search overlay opening (nothing typed, nothing submitted) — action + 0.80s (frame stamped +0.58s) |

### Reference: agamieuromed.org at 390 — 40 files

| File | What it shows |
|---|---|
| `ref_agami_390_01_first-viewport.png` | https://agamieuromed.org/en/ first viewport at 390px as a new visitor (any consent banner left as shown) |
| `ref_agami_390_ar_first-viewport.png` | https://agamieuromed.org/ar/ first viewport at 390px (RTL reference) |
| `ref_agami_390_load_fp+0000ms.png` | https://agamieuromed.org loading at 390px (no throttling) — first paint + 0.0s (first paint 0.82s after navigation start; frame stamped 0.82s) |
| `ref_agami_390_load_fp+0200ms.png` | https://agamieuromed.org loading at 390px (no throttling) — first paint + 0.2s (first paint 0.82s after navigation start; frame stamped 1.01s) |
| `ref_agami_390_load_fp+0500ms.png` | https://agamieuromed.org loading at 390px (no throttling) — first paint + 0.5s (first paint 0.82s after navigation start; frame stamped 1.32s) |
| `ref_agami_390_load_fp+0900ms.png` | https://agamieuromed.org loading at 390px (no throttling) — first paint + 0.9s (first paint 0.82s after navigation start; frame stamped 1.71s) |
| `ref_agami_390_load_fp+1500ms.png` | https://agamieuromed.org loading at 390px (no throttling) — first paint + 1.5s (first paint 0.82s after navigation start; frame stamped 1.85s) |
| `ref_agami_390_load_fp+2500ms.png` | https://agamieuromed.org loading at 390px (no throttling) — first paint + 2.5s (first paint 0.82s after navigation start; frame stamped 1.85s) |
| `ref_agami_390_load_fp+4000ms.png` | https://agamieuromed.org loading at 390px (no throttling) — first paint + 4.0s (first paint 0.82s after navigation start; frame stamped 1.85s) |
| `ref_agami_390_menu-anim_a+0000ms.png` | https://agamieuromed.org/en/ at 390px, mobile menu opening after tapping the menu button — action + 0.00s (frame stamped -1.01s) |
| `ref_agami_390_menu-anim_a+0100ms.png` | https://agamieuromed.org/en/ at 390px, mobile menu opening after tapping the menu button — action + 0.10s (frame stamped +0.09s) |
| `ref_agami_390_menu-anim_a+0200ms.png` | https://agamieuromed.org/en/ at 390px, mobile menu opening after tapping the menu button — action + 0.20s (frame stamped +0.20s) |
| `ref_agami_390_menu-anim_a+0350ms.png` | https://agamieuromed.org/en/ at 390px, mobile menu opening after tapping the menu button — action + 0.35s (frame stamped +0.35s) |
| `ref_agami_390_menu-anim_a+0700ms.png` | https://agamieuromed.org/en/ at 390px, mobile menu opening after tapping the menu button — action + 0.70s (frame stamped +0.70s) |
| `ref_agami_390_menu-anim_a+1200ms.png` | https://agamieuromed.org/en/ at 390px, mobile menu opening after tapping the menu button — action + 1.20s (frame stamped +0.79s) |
| `ref_agami_390_menu-open.png` | https://agamieuromed.org/en/ at 390px, mobile menu open |
| `ref_agami_390_menu-sub.png` | https://agamieuromed.org/en/ at 390px, mobile menu with the first sub-level «» expanded |
| `ref_agami_390_scroll01.png` | https://agamieuromed.org at 390px after wheel step 1 (mouseWheel, scrollY=700) |
| `ref_agami_390_scroll01_mid.png` | https://agamieuromed.org at 390px ~0.25 s after wheel step 1 (reveal/transition in progress) |
| `ref_agami_390_scroll02.png` | https://agamieuromed.org at 390px after wheel step 2 (mouseWheel, scrollY=1400) |
| `ref_agami_390_scroll02_mid.png` | https://agamieuromed.org at 390px ~0.25 s after wheel step 2 (reveal/transition in progress) |
| `ref_agami_390_scroll03.png` | https://agamieuromed.org at 390px after wheel step 3 (mouseWheel, scrollY=2100) |
| `ref_agami_390_scroll03_mid.png` | https://agamieuromed.org at 390px ~0.25 s after wheel step 3 (reveal/transition in progress) |
| `ref_agami_390_scroll04.png` | https://agamieuromed.org at 390px after wheel step 4 (mouseWheel, scrollY=2800) |
| `ref_agami_390_scroll05.png` | https://agamieuromed.org at 390px after wheel step 5 (mouseWheel, scrollY=3500) |
| `ref_agami_390_scroll06.png` | https://agamieuromed.org at 390px after wheel step 6 (mouseWheel, scrollY=4200) |
| `ref_agami_390_scroll07.png` | https://agamieuromed.org at 390px after wheel step 7 (mouseWheel, scrollY=4900) |
| `ref_agami_390_scroll08.png` | https://agamieuromed.org at 390px after wheel step 8 (mouseWheel, scrollY=5600) |
| `ref_agami_390_scroll09.png` | https://agamieuromed.org at 390px after wheel step 9 (mouseWheel, scrollY=6300) |
| `ref_agami_390_scroll10.png` | https://agamieuromed.org at 390px after wheel step 10 (mouseWheel, scrollY=7000) |
| `ref_agami_390_scroll11.png` | https://agamieuromed.org at 390px after wheel step 11 (mouseWheel, scrollY=7700) |
| `ref_agami_390_scroll12.png` | https://agamieuromed.org at 390px after wheel step 12 (mouseWheel, scrollY=8400) |
| `ref_agami_390_scroll13.png` | https://agamieuromed.org at 390px after wheel step 13 (mouseWheel, scrollY=9100) |
| `ref_agami_390_scroll14.png` | https://agamieuromed.org at 390px after wheel step 14 (mouseWheel, scrollY=9800) |
| `ref_agami_390_scroll15.png` | https://agamieuromed.org at 390px after wheel step 15 (mouseWheel, scrollY=10500) |
| `ref_agami_390_scroll16.png` | https://agamieuromed.org at 390px after wheel step 16 (mouseWheel, scrollY=11200) |
| `ref_agami_390_scroll17.png` | https://agamieuromed.org at 390px after wheel step 17 (mouseWheel, scrollY=11900) |
| `ref_agami_390_scroll18.png` | https://agamieuromed.org at 390px after wheel step 18 (mouseWheel, scrollY=12600) |
| `ref_agami_390_scroll19.png` | https://agamieuromed.org at 390px after wheel step 19 (mouseWheel, scrollY=12784) |
| `ref_agami_390_scroll20.png` | https://agamieuromed.org at 390px after wheel step 20 (mouseWheel, scrollY=12784) |

### Reference: studiobadrane.com at 1440 — 56 files

| File | What it shows |
|---|---|
| `ref_studiobadrane_1440_01_first-viewport.png` | https://www.studiobadrane.com/en/ first viewport at 1440px as a new visitor (any consent banner left as shown) |
| `ref_studiobadrane_1440_ar_first-viewport.png` | https://www.studiobadrane.com/ar/ first viewport at 1440px (dir=rtl, RTL reference) |
| `ref_studiobadrane_1440_ar_scroll01.png` | https://www.studiobadrane.com/ar/ at 1440px after one wheel step (RTL cards and sticky header) |
| `ref_studiobadrane_1440_cardhover_a+0000ms.png` | https://www.studiobadrane.com/en/ at 1440px, pointer arriving on the «Damage compensation» area card (hover state) — action + 0.00s (frame stamped -1.02s) |
| `ref_studiobadrane_1440_cardhover_a+0150ms.png` | https://www.studiobadrane.com/en/ at 1440px, pointer arriving on the «Damage compensation» area card (hover state) — action + 0.15s (frame stamped +0.15s) |
| `ref_studiobadrane_1440_cardhover_a+0400ms.png` | https://www.studiobadrane.com/en/ at 1440px, pointer arriving on the «Damage compensation» area card (hover state) — action + 0.40s (frame stamped +0.38s) |
| `ref_studiobadrane_1440_cardhover_a+0800ms.png` | https://www.studiobadrane.com/en/ at 1440px, pointer arriving on the «Damage compensation» area card (hover state) — action + 0.80s (frame stamped +0.75s) |
| `ref_studiobadrane_1440_inner_first-viewport.png` | inner page https://www.studiobadrane.com/en/chi-siamo/ first viewport at 1440px |
| `ref_studiobadrane_1440_inner_scroll01.png` | inner page https://www.studiobadrane.com/en/chi-siamo/ at 1440px after one wheel step |
| `ref_studiobadrane_1440_inner_scroll02.png` | inner page https://www.studiobadrane.com/en/chi-siamo/ at 1440px after two wheel steps |
| `ref_studiobadrane_1440_load_fp+0000ms.png` | https://www.studiobadrane.com loading at 1440px (no throttling) — first paint + 0.0s (first paint 0.94s after navigation start; frame stamped 0.94s) |
| `ref_studiobadrane_1440_load_fp+0200ms.png` | https://www.studiobadrane.com loading at 1440px (no throttling) — first paint + 0.2s (first paint 0.94s after navigation start; frame stamped 1.07s) |
| `ref_studiobadrane_1440_load_fp+0500ms.png` | https://www.studiobadrane.com loading at 1440px (no throttling) — first paint + 0.5s (first paint 0.94s after navigation start; frame stamped 1.36s) |
| `ref_studiobadrane_1440_load_fp+0900ms.png` | https://www.studiobadrane.com loading at 1440px (no throttling) — first paint + 0.9s (first paint 0.94s after navigation start; frame stamped 1.78s) |
| `ref_studiobadrane_1440_load_fp+1500ms.png` | https://www.studiobadrane.com loading at 1440px (no throttling) — first paint + 1.5s (first paint 0.94s after navigation start; frame stamped 2.39s) |
| `ref_studiobadrane_1440_load_fp+2500ms.png` | https://www.studiobadrane.com loading at 1440px (no throttling) — first paint + 2.5s (first paint 0.94s after navigation start; frame stamped 3.41s) |
| `ref_studiobadrane_1440_load_fp+4000ms.png` | https://www.studiobadrane.com loading at 1440px (no throttling) — first paint + 4.0s (first paint 0.94s after navigation start; frame stamped 4.92s) |
| `ref_studiobadrane_1440_nav01_practice-areas_click.png` | https://www.studiobadrane.com/en/ at 1440px, dropdown «Practice Areas» opened by click |
| `ref_studiobadrane_1440_nav02_compensation_click.png` | https://www.studiobadrane.com/en/ at 1440px, dropdown «Compensation» opened by click |
| `ref_studiobadrane_1440_navhover_a+0000ms.png` | https://www.studiobadrane.com/en/ at 1440px, pointer arriving on the top-level item «About Us» (hover state) — action + 0.00s (frame stamped -0.02s) |
| `ref_studiobadrane_1440_navhover_a+0150ms.png` | https://www.studiobadrane.com/en/ at 1440px, pointer arriving on the top-level item «About Us» (hover state) — action + 0.15s (frame stamped +0.11s) |
| `ref_studiobadrane_1440_navhover_a+0400ms.png` | https://www.studiobadrane.com/en/ at 1440px, pointer arriving on the top-level item «About Us» (hover state) — action + 0.40s (frame stamped +0.39s) |
| `ref_studiobadrane_1440_pagetransition_a+0000ms.png` | click on «Discover the Firm» -> https://www.studiobadrane.com/en/chi-siamo/ at 1440px: what the visitor sees between pages — action + 0.00s (frame stamped -0.02s) |
| `ref_studiobadrane_1440_pagetransition_a+0150ms.png` | click on «Discover the Firm» -> https://www.studiobadrane.com/en/chi-siamo/ at 1440px: what the visitor sees between pages — action + 0.15s (frame stamped +0.13s) |
| `ref_studiobadrane_1440_pagetransition_a+0350ms.png` | click on «Discover the Firm» -> https://www.studiobadrane.com/en/chi-siamo/ at 1440px: what the visitor sees between pages — action + 0.35s (frame stamped +0.13s) |
| `ref_studiobadrane_1440_pagetransition_a+0700ms.png` | click on «Discover the Firm» -> https://www.studiobadrane.com/en/chi-siamo/ at 1440px: what the visitor sees between pages — action + 0.70s (frame stamped +0.68s) |
| `ref_studiobadrane_1440_pagetransition_a+1200ms.png` | click on «Discover the Firm» -> https://www.studiobadrane.com/en/chi-siamo/ at 1440px: what the visitor sees between pages — action + 1.20s (frame stamped +1.19s) |
| `ref_studiobadrane_1440_pagetransition_a+2000ms.png` | click on «Discover the Firm» -> https://www.studiobadrane.com/en/chi-siamo/ at 1440px: what the visitor sees between pages — action + 2.00s (frame stamped +1.61s) |
| `ref_studiobadrane_1440_pagetransition_a+3500ms.png` | click on «Discover the Firm» -> https://www.studiobadrane.com/en/chi-siamo/ at 1440px: what the visitor sees between pages — action + 3.50s (frame stamped +1.61s) |
| `ref_studiobadrane_1440_scroll01.png` | https://www.studiobadrane.com at 1440px after wheel step 1 (mouseWheel, scrollY=800) |
| `ref_studiobadrane_1440_scroll01_mid.png` | https://www.studiobadrane.com at 1440px ~0.25 s after wheel step 1 (reveal/transition in progress) |
| `ref_studiobadrane_1440_scroll02.png` | https://www.studiobadrane.com at 1440px after wheel step 2 (mouseWheel, scrollY=1600) |
| `ref_studiobadrane_1440_scroll02_mid.png` | https://www.studiobadrane.com at 1440px ~0.25 s after wheel step 2 (reveal/transition in progress) |
| `ref_studiobadrane_1440_scroll03.png` | https://www.studiobadrane.com at 1440px after wheel step 3 (mouseWheel, scrollY=2400) |
| `ref_studiobadrane_1440_scroll03_mid.png` | https://www.studiobadrane.com at 1440px ~0.25 s after wheel step 3 (reveal/transition in progress) |
| `ref_studiobadrane_1440_scroll04.png` | https://www.studiobadrane.com at 1440px after wheel step 4 (mouseWheel, scrollY=3200) |
| `ref_studiobadrane_1440_scroll05.png` | https://www.studiobadrane.com at 1440px after wheel step 5 (mouseWheel, scrollY=4000) |
| `ref_studiobadrane_1440_scroll06.png` | https://www.studiobadrane.com at 1440px after wheel step 6 (mouseWheel, scrollY=4800) |
| `ref_studiobadrane_1440_scroll07.png` | https://www.studiobadrane.com at 1440px after wheel step 7 (mouseWheel, scrollY=5600) |
| `ref_studiobadrane_1440_scroll08.png` | https://www.studiobadrane.com at 1440px after wheel step 8 (mouseWheel, scrollY=6400) |
| `ref_studiobadrane_1440_scroll09.png` | https://www.studiobadrane.com at 1440px after wheel step 9 (mouseWheel, scrollY=7200) |
| `ref_studiobadrane_1440_scroll10.png` | https://www.studiobadrane.com at 1440px after wheel step 10 (mouseWheel, scrollY=8000) |
| `ref_studiobadrane_1440_scroll11.png` | https://www.studiobadrane.com at 1440px after wheel step 11 (mouseWheel, scrollY=8800) |
| `ref_studiobadrane_1440_scroll12.png` | https://www.studiobadrane.com at 1440px after wheel step 12 (mouseWheel, scrollY=9600) |
| `ref_studiobadrane_1440_scroll13.png` | https://www.studiobadrane.com at 1440px after wheel step 13 (mouseWheel, scrollY=10400) |
| `ref_studiobadrane_1440_scroll14.png` | https://www.studiobadrane.com at 1440px after wheel step 14 (mouseWheel, scrollY=11134) |
| `ref_studiobadrane_1440_scroll15.png` | https://www.studiobadrane.com at 1440px after wheel step 15 (mouseWheel, scrollY=11134) |
| `ref_studiobadrane_1440_search_a+0000ms.png` | https://www.studiobadrane.com/en/ at 1440px, search control activated (nothing typed, nothing submitted) — action + 0.00s (frame stamped -0.05s) |
| `ref_studiobadrane_1440_search_a+0120ms.png` | https://www.studiobadrane.com/en/ at 1440px, search control activated (nothing typed, nothing submitted) — action + 0.12s (frame stamped +0.07s) |
| `ref_studiobadrane_1440_search_a+0300ms.png` | https://www.studiobadrane.com/en/ at 1440px, search control activated (nothing typed, nothing submitted) — action + 0.30s (frame stamped +0.28s) |
| `ref_studiobadrane_1440_search_a+0800ms.png` | https://www.studiobadrane.com/en/ at 1440px, search control activated (nothing typed, nothing submitted) — action + 0.80s (frame stamped +0.79s) |
| `ref_studiobadrane_1440_stickyheader_a+0000ms.png` | https://www.studiobadrane.com/en/ at 1440px, one 300px wheel from the top: how the two-row header collapses into the sticky white bar — action + 0.00s (frame stamped -0.02s) |
| `ref_studiobadrane_1440_stickyheader_a+0100ms.png` | https://www.studiobadrane.com/en/ at 1440px, one 300px wheel from the top: how the two-row header collapses into the sticky white bar — action + 0.10s (frame stamped +0.08s) |
| `ref_studiobadrane_1440_stickyheader_a+0250ms.png` | https://www.studiobadrane.com/en/ at 1440px, one 300px wheel from the top: how the two-row header collapses into the sticky white bar — action + 0.25s (frame stamped +0.24s) |
| `ref_studiobadrane_1440_stickyheader_a+0500ms.png` | https://www.studiobadrane.com/en/ at 1440px, one 300px wheel from the top: how the two-row header collapses into the sticky white bar — action + 0.50s (frame stamped +0.46s) |
| `ref_studiobadrane_1440_stickyheader_a+1000ms.png` | https://www.studiobadrane.com/en/ at 1440px, one 300px wheel from the top: how the two-row header collapses into the sticky white bar — action + 1.00s (frame stamped +0.99s) |

### Reference: studiobadrane.com at 390 — 49 files

| File | What it shows |
|---|---|
| `ref_studiobadrane_390_01_first-viewport.png` | https://www.studiobadrane.com/en/ first viewport at 390px as a new visitor (any consent banner left as shown) |
| `ref_studiobadrane_390_ar_first-viewport.png` | https://www.studiobadrane.com/ar/ first viewport at 390px (RTL reference) |
| `ref_studiobadrane_390_inner_first-viewport.png` | inner page https://www.studiobadrane.com/en/chi-siamo/ first viewport at 390px |
| `ref_studiobadrane_390_load_fp+0000ms.png` | https://www.studiobadrane.com loading at 390px (no throttling) — first paint + 0.0s (first paint 0.79s after navigation start; frame stamped 0.79s) |
| `ref_studiobadrane_390_load_fp+0200ms.png` | https://www.studiobadrane.com loading at 390px (no throttling) — first paint + 0.2s (first paint 0.79s after navigation start; frame stamped 0.98s) |
| `ref_studiobadrane_390_load_fp+0500ms.png` | https://www.studiobadrane.com loading at 390px (no throttling) — first paint + 0.5s (first paint 0.79s after navigation start; frame stamped 1.28s) |
| `ref_studiobadrane_390_load_fp+0900ms.png` | https://www.studiobadrane.com loading at 390px (no throttling) — first paint + 0.9s (first paint 0.79s after navigation start; frame stamped 1.68s) |
| `ref_studiobadrane_390_load_fp+1500ms.png` | https://www.studiobadrane.com loading at 390px (no throttling) — first paint + 1.5s (first paint 0.79s after navigation start; frame stamped 2.27s) |
| `ref_studiobadrane_390_load_fp+2500ms.png` | https://www.studiobadrane.com loading at 390px (no throttling) — first paint + 2.5s (first paint 0.79s after navigation start; frame stamped 3.28s) |
| `ref_studiobadrane_390_load_fp+4000ms.png` | https://www.studiobadrane.com loading at 390px (no throttling) — first paint + 4.0s (first paint 0.79s after navigation start; frame stamped 4.78s) |
| `ref_studiobadrane_390_menu-anim_a+0000ms.png` | https://www.studiobadrane.com/en/ at 390px, mobile menu opening after tapping the menu button — action + 0.00s (frame stamped -0.00s) |
| `ref_studiobadrane_390_menu-anim_a+0100ms.png` | https://www.studiobadrane.com/en/ at 390px, mobile menu opening after tapping the menu button — action + 0.10s (frame stamped +0.09s) |
| `ref_studiobadrane_390_menu-anim_a+0200ms.png` | https://www.studiobadrane.com/en/ at 390px, mobile menu opening after tapping the menu button — action + 0.20s (frame stamped +0.19s) |
| `ref_studiobadrane_390_menu-anim_a+0350ms.png` | https://www.studiobadrane.com/en/ at 390px, mobile menu opening after tapping the menu button — action + 0.35s (frame stamped +0.34s) |
| `ref_studiobadrane_390_menu-anim_a+0700ms.png` | https://www.studiobadrane.com/en/ at 390px, mobile menu opening after tapping the menu button — action + 0.70s (frame stamped +0.38s) |
| `ref_studiobadrane_390_menu-anim_a+1200ms.png` | https://www.studiobadrane.com/en/ at 390px, mobile menu opening after tapping the menu button — action + 1.20s (frame stamped +0.38s) |
| `ref_studiobadrane_390_menu-open.png` | https://www.studiobadrane.com/en/ at 390px, mobile menu open |
| `ref_studiobadrane_390_menu-sub.png` | https://www.studiobadrane.com/en/ at 390px, mobile menu with the first sub-level «Practice Areas» expanded |
| `ref_studiobadrane_390_pagetransition_a+0000ms.png` | tap on «Discover the Firm» -> https://www.studiobadrane.com/en/chi-siamo/ at 390px: what the visitor sees between pages — action + 0.00s (frame stamped -0.01s) |
| `ref_studiobadrane_390_pagetransition_a+0150ms.png` | tap on «Discover the Firm» -> https://www.studiobadrane.com/en/chi-siamo/ at 390px: what the visitor sees between pages — action + 0.15s (frame stamped +0.15s) |
| `ref_studiobadrane_390_pagetransition_a+0350ms.png` | tap on «Discover the Firm» -> https://www.studiobadrane.com/en/chi-siamo/ at 390px: what the visitor sees between pages — action + 0.35s (frame stamped +0.17s) |
| `ref_studiobadrane_390_pagetransition_a+0700ms.png` | tap on «Discover the Firm» -> https://www.studiobadrane.com/en/chi-siamo/ at 390px: what the visitor sees between pages — action + 0.70s (frame stamped +0.68s) |
| `ref_studiobadrane_390_pagetransition_a+1200ms.png` | tap on «Discover the Firm» -> https://www.studiobadrane.com/en/chi-siamo/ at 390px: what the visitor sees between pages — action + 1.20s (frame stamped +1.20s) |
| `ref_studiobadrane_390_pagetransition_a+2000ms.png` | tap on «Discover the Firm» -> https://www.studiobadrane.com/en/chi-siamo/ at 390px: what the visitor sees between pages — action + 2.00s (frame stamped +1.30s) |
| `ref_studiobadrane_390_scroll01.png` | https://www.studiobadrane.com at 390px after wheel step 1 (mouseWheel, scrollY=700) |
| `ref_studiobadrane_390_scroll01_mid.png` | https://www.studiobadrane.com at 390px ~0.25 s after wheel step 1 (reveal/transition in progress) |
| `ref_studiobadrane_390_scroll02.png` | https://www.studiobadrane.com at 390px after wheel step 2 (mouseWheel, scrollY=1400) |
| `ref_studiobadrane_390_scroll02_mid.png` | https://www.studiobadrane.com at 390px ~0.25 s after wheel step 2 (reveal/transition in progress) |
| `ref_studiobadrane_390_scroll03.png` | https://www.studiobadrane.com at 390px after wheel step 3 (mouseWheel, scrollY=2100) |
| `ref_studiobadrane_390_scroll03_mid.png` | https://www.studiobadrane.com at 390px ~0.25 s after wheel step 3 (reveal/transition in progress) |
| `ref_studiobadrane_390_scroll04.png` | https://www.studiobadrane.com at 390px after wheel step 4 (mouseWheel, scrollY=2800) |
| `ref_studiobadrane_390_scroll05.png` | https://www.studiobadrane.com at 390px after wheel step 5 (mouseWheel, scrollY=3500) |
| `ref_studiobadrane_390_scroll06.png` | https://www.studiobadrane.com at 390px after wheel step 6 (mouseWheel, scrollY=4200) |
| `ref_studiobadrane_390_scroll07.png` | https://www.studiobadrane.com at 390px after wheel step 7 (mouseWheel, scrollY=4900) |
| `ref_studiobadrane_390_scroll08.png` | https://www.studiobadrane.com at 390px after wheel step 8 (mouseWheel, scrollY=5600) |
| `ref_studiobadrane_390_scroll09.png` | https://www.studiobadrane.com at 390px after wheel step 9 (mouseWheel, scrollY=6300) |
| `ref_studiobadrane_390_scroll10.png` | https://www.studiobadrane.com at 390px after wheel step 10 (mouseWheel, scrollY=7000) |
| `ref_studiobadrane_390_scroll11.png` | https://www.studiobadrane.com at 390px after wheel step 11 (mouseWheel, scrollY=7700) |
| `ref_studiobadrane_390_scroll12.png` | https://www.studiobadrane.com at 390px after wheel step 12 (mouseWheel, scrollY=8400) |
| `ref_studiobadrane_390_scroll13.png` | https://www.studiobadrane.com at 390px after wheel step 13 (mouseWheel, scrollY=9100) |
| `ref_studiobadrane_390_scroll14.png` | https://www.studiobadrane.com at 390px after wheel step 14 (mouseWheel, scrollY=9800) |
| `ref_studiobadrane_390_scroll15.png` | https://www.studiobadrane.com at 390px after wheel step 15 (mouseWheel, scrollY=10500) |
| `ref_studiobadrane_390_scroll16.png` | https://www.studiobadrane.com at 390px after wheel step 16 (mouseWheel, scrollY=11200) |
| `ref_studiobadrane_390_scroll17.png` | https://www.studiobadrane.com at 390px after wheel step 17 (mouseWheel, scrollY=11900) |
| `ref_studiobadrane_390_scroll18.png` | https://www.studiobadrane.com at 390px after wheel step 18 (mouseWheel, scrollY=12600) |
| `ref_studiobadrane_390_scroll19.png` | https://www.studiobadrane.com at 390px after wheel step 19 (mouseWheel, scrollY=13300) |
| `ref_studiobadrane_390_scroll20.png` | https://www.studiobadrane.com at 390px after wheel step 20 (mouseWheel, scrollY=14000) |
| `ref_studiobadrane_390_scroll21.png` | https://www.studiobadrane.com at 390px after wheel step 21 (mouseWheel, scrollY=14700) |
| `ref_studiobadrane_390_scroll22.png` | https://www.studiobadrane.com at 390px after wheel step 22 (mouseWheel, scrollY=14970) |

Sub-folders under `captures/` that belong to other council agents and were not produced by this role: `21st_nav/` (21 files), `21st_primitives/` (19), `colour/` (15), `typography/` (2: `before_ar_home_1440.png`, `before_it_home_1440.png`).

## 5. What could not be done, and why

- agamieuromed.org at 390: the script found no «Refuse» button (`refused_cookies: false`), so the mobile first viewport was taken as shown; the desktop refusal earlier in the same profile most likely persisted, and no banner is visible in the mobile frames.
- studiobadrane.com dropdowns do not open on hover (Bootstrap, click-to-open); they were opened by click, the URL was verified unchanged, and closed with Escape. Its hero video was not played.
- agami page transition: the desktop pass found no «Discover the Departments» link in the header/nav scope (`transition_link: null`); a dedicated transition pass (`r1_ref.py agami transition`) captured it from the home page instead.
- Reference sites were observed, not measured: no Lighthouse, no INP, no throttled runs on them (out of scope, and not needed for a principles study).
- ILE loading filmstrips are CDP-emulated (Slow 4G + CPU x4, cache disabled), screencast-timed. They are not Lighthouse LCP numbers and should not be compared with the 1.4–1.8 s figure in the project memory.
- The Guichet numérique defect (missing `portal/console.css`) was diagnosed from the DOM and the two templates only; nothing was changed (read-only phase).
- The forum-permanent console page is a placeholder in the current build; there was nothing more to capture there.
- No 21st.dev calls were made by this role (other agents cover it); no Pexels calls were made; no production access.
- Repository integrity at hand-over: `git status` in `C:/tmp/italylegalentry` shows the same 37 modified and 5 untracked entries as at the start of this session plus one new untracked directory, `.playwright-mcp/` (created 16:24–16:25 on 26 Sept, containing `ile-v5-icon-specimen.png`, two console logs and two page snapshots). This role used only `scripts/cdp.py` on the QA Chrome and never Playwright; the folder was written by another council agent's Playwright MCP session, inside the repository, during the read-only phase. Flagged for the orchestrator: it is not tracked, but it should be removed by whoever created it, and that agent used a browser this phase reserved to the capture role.
