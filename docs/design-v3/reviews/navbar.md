# REVISIONE INDIPENDENTE — navbar

Round 1 · premium_lift **6/10** · conforme: **NO** · implementabile: **NO**

> This is the most numerically honest spec I have reviewed here — I recomputed all eight of its WCAG figures (6.87 / 5.88 / 6.05 / 5.24 / 5.69 / 3.94 / 15.56 / 6.07) and the 88%-vs-82% glass floor (#dfdfde 5.37:1, #d0d2d2 4.72:1 / 4.16:1) and every one is exact to two decimals; the seven photo filenames all exist and public-conference-480 really is 11 306 B and campus-universitaire-480 really is 26 476 B; the Motion chunk really is 26 143 B gzip; main.css and its preload chain are described correctly; the menu-in / menu-in-rtl / menu-in-end keyframes and .main-nav__item--end really do exist and killing them by making the panel full-bleed is a genuinely good structural idea. And yet it does not survive contact with the codebase. Its two load-bearing engineering sections contradict each other and reality: §4.4 puts `position: relative` on `.main-nav__list`, which silently steals the containing block from `.site-header` and demolishes §4.5's entire full-width-panel argument, while the trace itself is authored *outside* that ul and would render ~327 px left of the item it marks; and the width budget — the spec's proudest table — assumes inner boxes of 1200 px at 1280 and 1240 px at 1440 when tokens.css gives `--container: 1176px` with `--grid-margin: 40px`, i.e. a real inner box of 1096 px, so the header overflows by 78 px in FRENCH before the IT/EN labels it warns about. Worse for the council: §4.3 animates the official lock-up to `scale(.842)`, and DESIGN_SYSTEM_V2 §8.1/§8.2 say in as many words "Nessun effetto, nessuna animazione" on the mark and "il lock-up non cambia" when scrolled — the spec breaks the one element the brand documents lock hardest, and it never declares that it is doing so. On the owner's actual question — does this read premium — the answer is only half yes: it is more crafted, but its vocabulary (frosted sticky bar, travelling spring underline, mega-menu with a photo in the right rail, mono ordinals on menu rows, 40 px ghost icon button) is the default 2024 SaaS navbar, and the one idea in the document that could not have been written for any other website — §4.8, the territory line as the seam where the letterhead ends and the map begins — is one CSS rule buried in the last paragraph, on a `:has(main > .chapter--dark:first-child)` selector that base.html's breadcrumbs block and messages div will defeat.

## Violazioni dei vincoli non negoziabili

1. DESIGN_SYSTEM_V2.md §8.2 line 233 — «Scrollato: carta all'88 % + backdrop-filter, --shadow-2; **il lock-up non cambia**» — and §8.1 line ~227 «Nessun effetto, nessuna animazione (il marchio sale di 1 px in hover e basta)». Spec §4.3 signal (1): «lock-up `transform: scale(.842)`», and MOTION entry `nav/header-settle` animates «lock-up `scale(1→.842)`» over 320 ms. The spec animates the official brand mark, which the binding brand/design documents forbid, and never declares the departure.

2. Performance non-negotiable «transform/opacity only; … no box-shadow animation». Spec §5, `nav/header-settle`, Proprietà column: «lock-up `scale(1→.842)`, tacche `opacity .55→0`, fondo, **`box-shadow`**». A 320 ms box-shadow transition on a full-bleed sticky header is exactly the banned case; MOTION_SYSTEM §2 permits a role shadow only inside the HOVER family, and header-settle is not a hover.

3. Performance non-negotiable «images <= 120 KB per viewport». Spec §4.5 defines `.main-nav__panel-visual` with `image-set(... 480 1x, ... 960 2x)` and gives NO `@media (min-width: 80rem)` scope and no rule hiding the visual in the drawer. Below 80 rem the accordion panels are `display: block` when opened, so on a DPR-2 phone opening the three sections that actually have children loads entretien-accompagnement-960 (35 900 B) + equipe-entreprise-960 (44 062 B) + collaboration-bureau-960 (48 262 B) = 128 224 B = 125.2 KB, over the 120 KB budget. §7's «0 byte» / «11–27 KB» figures quote only the 1x branch the spec itself does not select on retina.

4. Progressive-enhancement non-negotiable («server-rendered templates + progressive enhancement»). Spec §4 deletes `components.css` §7 outright; that block contains `html.no-js .main-nav__item:hover > .main-nav__panel` and `html.no-js .main-nav__item:focus-within > .main-nav__panel` (components.css:708-709) plus `html.no-js .main-nav__panel` (:922). Nothing in §4.5, §5 or §6 re-specifies the no-JS open state for the new absolutely-positioned, `::before`-backed panel. Without JS the mega-menu becomes unreachable on desktop.

5. Public/private boundary + role permissions. Spec §4.2 gives the door's markup as `<a class="door" href="{{ login_url }}">…` and says only «il tag `{% flag %}` non rende l'elemento». The current chrome guards this link with THREE conditions, in both utility_bar.html:9-14 and header.html:26-30: `{% flag "reserved_area_public_link" %}` AND `site.settings.reserved_area_enabled` AND a non-empty `{% safe_url 'account_login' %}`. As written the markup shape drops two of the three, and an implementer following it exposes the reserved-area entry when the client has switched `reserved_area_enabled` off.

## Lacune (ciò che l'implementatore dovrebbe inventare)

1. Which element is the panel's containing block. §4.4 sets `.main-nav__list { position: relative }` (for the trace); §4.5 asserts the panel is «ancorato a `.site-header`». The panel is `ul > li > div`, so §4.4 wins and `inset-inline: 0` spans the 828 px nav list, not the header. `.container` (layout.css:14-19) declares no `position`, so WITHOUT §4.4 the anchoring would have worked — the spec breaks its own premise. Implementer must invent a third positioned wrapper.

2. Where the trace actually lives. §4.4 puts `<span class="main-nav__trace">` AFTER `</ul>` — a sibling — then makes the ul `position: relative` and has nav.js measure `offsetLeft` «rispetto alla lista». The trace's containing block is therefore not the ul it is measured against; at 1440 it renders ~327 px (lock-up 303 + gap 24) to the reading-start side of the item it marks.

3. The real container widths. §4.4's budget assumes 1200 px inner at 1280 and 1240 at 1440. tokens.css:237 gives `--container: 1176px` from 75 rem and `--grid-margin: 40px` from 48 rem (tokens.css:215) → real inner box 1096 px at 1280 (deficit 78 px on the spec's own 1174 px requirement) and 1240 px at 1440 (that one is correct).

4. The 1536–1599 px window. §4.2 makes `.door__label` visible at ≥96 rem (+~125 px), but `--container` stays 1320 (inner 1240) until 100 rem. Required 1211 + 125 = 1336 vs 1240 available → ~96 px overflow. §4.4's mandated test at 1280/1440/1600 skips exactly this band.

5. Panel padding. §4.5 asserts «4 righe × 48 = 192 px ≤ 224 px utili» inside `--nav-panel-h: 288px`, which implies 32 px block padding, but no padding value is ever declared. Also «container 1320» inside the panel vs the header's own 1320 container: if the implementer builds a raw 1320 grid rather than reusing `.container`, the panel's lead column misses the lock-up's left edge by 40 px.

6. One element, two class names. §4.1 anatomy: `.nav-drawer__door 40×40`. §4.2 markup: `<a class="door">` with `.door__glyph` / `.door__label`. §4.7 ordering: `.door`. Pick one — and `.door` is a global, unscoped name one character from the hero's `.doorway` / `.doorway__key` family (v2/hero.css:223-386).

7. Photo-to-section mapping is keyed on the wrong field. §4.5 uses `data-nav-index="{{ forloop.counter0 }}"` over the GATE-FILTERED loop, while `NavItem.id` (cms_nav.py `_slug`, e.g. `nav-6` for Projet) is stable across gates. With Phase 3 closed (the :8770 configuration this project actually runs) Institutions/Universités/Actualités drop out and Projet's counter0 falls from 6 to 3, so «Projet» silently gets `campus-universitaire`. A CMS editor reordering MenuItem rows reshuffles all seven.

8. The spec is built for seven panels; there are three. `_FALLBACK_MAIN` gives children only to Personnes (7), Entreprises (2) and Projet (4); Institutions, Universités, Forum and Actualités have none, so `main_nav.html` renders no `.main-nav__panel` for them. «tutti e sette i pannelli hanno la stessa geometria» and four of the seven `background-image` rules are dead.

9. The panel-open animation has no clip. `nav/panel-open` scales a `::before` background `scaleY 0→1` over 240 ms while the content fades in over 180 ms, and §5 explicitly forbids `clip-path`. With no `overflow: hidden` stated on `.main-nav__panel`, link rows render over the page below the panel's own unfinished background for the first ~100 ms.

10. Focus-ring contrast in the state the spec adds. §6 lists `--accent-ring` at 3.94:1 on `--min-2` but gives no figure for the scrolled glass. I measure `--accent-ring` on the #dfdfde composite at 3.08:1 — 0.08 of headroom — and the blend model ignores `saturate(140%)`, which shifts the sampled backdrop. WCAG 2.2 1.4.11 / 2.4.13 in `is-scrolled` is unverified.

11. `.main-nav__label` (a section row with no URL — supported by `cms.MenuItem`) is styled at components.css:641 and :899. §4 deletes components.css §7 and §4.4 respecifies only `.main-nav__link`. That row would render unstyled.

12. `.nav-overlay { display: none !important }` at ≥80 rem lives in the deleted block; §4.7 respecifies only `inset-block-start`.

13. Undeclared deviations from DESIGN_SYSTEM_V2 §8.2: the institutional bar is `--min-1` there and `--min-0` in §4.1; the language segments are «FR · IT · EN · **ع**» there and `{{ l.code|upper }}` → «AR» in §4.6 (no glyph mapping given); drawer rows are 52 px there and 56 px in §4.7; and §8.2's prescribed «CTA «Orientation» come bottone secondario» in the header is silently dropped without retiring it (it would cost another ~140 px of the already-negative budget).

14. `language_switcher.html` is included in three places — utility_bar.html:15, header.html:32 and **portal_chrome.html:32** (the authenticated platform shell). §4.6 introduces a `variant` parameter and names only the bar and the drawer; §4's «Template toccati» omits portal_chrome.html. The default-variant behaviour is never stated.

15. §4.8's selector `body:has(main > .chapter--dark:first-child)` — base.html:55-61 puts `{% block breadcrumbs %}` and a `{% if messages %}` div inside `<main>` before the content block, so the rule breaks the moment any Django message renders on a dark-hero page. The stated guard («progressive enhancement») covers browser support, not this.

16. Whether «— promoteur du projet» survives. §4.1 compresses the institutional bar to «imprint mono (promotore)»; the current bar carries `<strong>{{ site.promoter }}</strong><span class="hide-mobile"> — promoteur du projet</span>`, an attribution sentence. The spec never confirms the qualifier is kept.

17. nav.js is estimated at 3.2 KB raw for trace measurement + spring + hover intent + panel switch orchestration + will-change lifecycle + stagger. Optimistic, though the page budget holds: today's total is 32.5 KB gzip (main 5.3 + head 0.2 + shell 0.6 + motion 0.2 + chunk 26.1) against 45 KB.

## Segnali di «cheap / generico / default»

1. The mega-menu with a photo in the right rail is the single most templated 'premium SaaS' navbar of the last four years. §8 Risk 1 names the danger and then guards it with an arch mask and a gradient veil — which is what every template does. An institutional legal-pathways menu with a stock campus photo behind it will read as a WordPress theme, and the spec's own fallback («si sostituisce con il glifo arco+gradini») is the better design, offered only as a retreat.

2. Reusing the hero doorway's arch (`border-start-start-radius: 120px`) as dropdown decoration converts the project's one signature form into a motif. §3 refuses Lucide icons because «il progetto ha un set proprio», then spends the signature shape on a hover state. That is a dilution, not a lift.

3. The mono ordinals `01 ─ Votre parcours ›` are decorative numerology: the children are an unordered list (FAQ, Glossaire, Attention aux fraudes) with no sequence, and the project already owns a real ordinal language — the four routes and the six stations of the hero route. Numbering an alphabetical menu is the default 21st.dev/Aceternity garnish and spends a meaningful token on nothing.

4. A 40×40 icon-only key with a 1 px ring and a transparent ground is the shadcn ghost icon-button default — and at 1440, the exact viewport of every `docs/design-v2/before/*_desktop.png` the owner reviews, the label is hidden (it only appears at ≥96 rem). §1.3 condemns the current door for being «testo grigio da 12 px» and replaces it with no text at all above the fold. The owner's complaint was that the site is 'not speaking'; this makes the platform entrance mute until the user scrolls.

5. `blur(14px) saturate(140%)` frosted sticky bar is the most exhausted premium signifier available, and §4.3 keeps it verbatim as signal (3) of four while §1.1 condemns the current scrolled state as non-existent.

6. A travelling underline on a spring is the Motion/Framer landing-page demo. §8 Risk 7 anticipates the charge and answers it with damping numbers, which is an engineering answer to an aesthetic objection.

7. Signal (2) of the four scroll signals is imperceptible: `--hairline` ticks at 55% over `--min-2` composite to #e5e4e0, 1.22:1. So of §4.3's four 'segni' one is invisible, one is the effect §1.1 just condemned, one violates the brand lock, and only the door arming actually lands — the remedy is thinner than the diagnosis.

8. The evidence is missing. The header promises `nav_{desktop,tablet,mobile}_{top,scrolled,drawer}.png`, `nav_desktop_panel.png`, `nav_desktop_panel_end.png`, `nav_rtl_top.png` and `measure.json`, and §1 cites them by name six times. None of those files exists anywhere in the repository (`docs/design-v3/audit/` holds a different, unrelated set). Several §1 claims check out against the CSS (the 13.5 px at shell.css:203, `--min-3` + 1 px `--hairline` + `--shadow-3` at :239-243, `box-shadow: none` on the drawer at :335), but no reviewer can verify a single optical claim against the image it names.

## MUST-FIX

1. Resolve the containing-block contradiction. Do not put `position: relative` on `.main-nav__list` (§4.4) if the panel is to anchor to `.site-header` (§4.5) — the panel is a descendant of that ul. Give the trace its own positioned wrapper inside the ul (or make the trace a child of the ul and measure in that same space), and state explicitly that `.site-header` is the only positioned ancestor of `.main-nav__panel`. As written the trace lands ~327 px off target at 1440 and the panel is nav-width, not header-width.

2. Rebuild the §4.4 width budget on the real tokens: `--container` is 1176 px at 1280 (tokens.css:237) and `--grid-margin` is 40 px (tokens.css:215), so the inner box is 1096 px, not 1200 — the header overflows by 78 px in FR. Add the 1536–1599 px row, where the ≥96 rem door label adds ~125 px against a still-1240 px box (~96 px overflow), and extend the mandated Playwright test to 1536.

3. Drop `transform: scale(.842)` on the lock-up, or take the exemption to the council in writing. DESIGN_SYSTEM_V2 §8.2 line 233 says «il lock-up non cambia» when scrolled and §8.1 says «Nessun effetto, nessuna animazione» on the mark. Remove `lock-up scale(1→.842)` from the `nav/header-settle` MOTION entry or replace the compaction with something that is not the official brand mark.

4. Remove `box-shadow` from the `nav/header-settle` animated-properties list. If the elevation must appear, put `--shadow-2` on a pseudo-element and transition its `opacity`.

5. Scope `.main-nav__panel-visual` to `@media (min-width: 80rem)` and set `background-image: none` below it. Otherwise a DPR-2 phone opening the three real accordions pulls 128 224 B (125.2 KB) of 960-wide WebP, over the 120 KB/viewport budget, and §7's «0 byte» figure is wrong for every retina device.

6. Key the panel photo on `item.id`, not `forloop.counter0`. `NavItem.id` is stable (`nav-0`…`nav-6` from the source tuple index in cms_nav.py `_fallback_main`) while the template loop is over the gate-filtered list: with Phase 3 closed — a configuration this project actually runs on :8770 — «Projet» drops from index 6 to 3 and silently inherits `campus-universitaire`. Also state what happens for a CMS section with no mapping.

7. Restore the full reserved-area guard in §4.2's markup shape: `{% flag "reserved_area_public_link" %}` AND `site.settings.reserved_area_enabled` AND a non-empty `{% safe_url 'account_login' %}`, exactly as utility_bar.html:9-14 and header.html:26-30 carry them today. As written the spec drops two of the three.

8. Fix the 768–1279 regression the move of the door creates. `.utility-bar` renders from 48 rem up (v2/shell.css:79-83) and `.drawer-utility` is `display: none` above 48 rem (:279-284), so moving «Espace réservé» into `.nav-drawer` hides the platform entrance behind the hamburger for the entire tablet/small-laptop band, where it is permanently visible today. Either keep a copy in the bar at 48–80 rem or hoist the door out of `.nav-drawer` at that breakpoint.

9. Re-specify the no-JS path. `components.css` §7 — which §4 deletes — is the only place `html.no-js .main-nav__item:hover/:focus-within > .main-nav__panel` exists (:708-709, :922). State the no-JS open rule for the new absolutely-positioned, `::before`-backed panel, or progressive enhancement is broken.

10. Publish the evidence. Either commit the nine named PNGs and `measure.json` under `docs/design-v3/`, or delete the filenames from the header and from the six places §1 cites them. A verdict section whose every claim points at a non-existent file cannot be reviewed.

11. Give `--accent-ring` a measured contrast on the scrolled glass. I make it 3.08:1 on the #dfdfde composite, before `saturate(140%)` shifts the sampled backdrop — 0.08 of headroom on a WCAG 2.2 AA focus indicator, in the state the spec is adding. Either publish the figure with the saturate accounted for, or define a darker ring token under `.is-scrolled`.

12. Specify the panel's block padding (the «224 px utili» arithmetic implies 32 px but never says so), and say whether the inner grid reuses `.container` — «container 1320» read literally misaligns the panel's lead column from the lock-up by 40 px.

13. Pick one class name for the door. §4.1 says `.nav-drawer__door`, §4.2 and §4.7 say `.door`. Scope it (`.nav-door`) so it cannot be confused with v2/hero.css's `.doorway` family.

14. Add `overflow: hidden` to `.main-nav__panel` (or delay the content until the background reaches scaleY(1)). With `clip-path` forbidden and the background scaling over 240 ms while rows fade in over 180 ms, the link rows render outside their own background for the first frames.

15. Fix or replace §4.8's selector. `body:has(main > .chapter--dark:first-child)` fails whenever base.html's `{% block breadcrumbs %}` or the `{% if messages %}` div (base.html:55-61) renders — use `:first-of-type`, or set a server-side class on `<main>`. This is the only genuinely original idea in the document and it should not be left on a selector that a flash message defeats.

16. Carry over the rules the deletion takes with it: `.main-nav__label` (components.css:641, :899, for a CMS section row with no URL) and `.nav-overlay { display: none }` at ≥80 rem.

17. Declare every departure from DESIGN_SYSTEM_V2 §8.2 explicitly rather than silently: institutional bar `--min-0` vs the prescribed `--min-1`; «AR» vs the prescribed «ع» (and give the glyph mapping, since `{{ l.code|upper }}` cannot produce it); 56 px drawer rows vs 52 px; and the prescribed secondary «Orientation» CTA in the header, which this spec neither places nor retires.

18. Make the door speak at 1440. Lower the labelled threshold from 96 rem to 90 rem, or give the resting door a filled/washed ground — the current proposal shows the owner an unlabelled 40 px key at exactly the viewport he reviews, which is a weaker affordance than the 113×36 text link §1.3 condemns.

19. Promote §4.8 from footnote to spine, and cut or re-motivate the mono ordinals on the panel rows. The territory line at the paper/midnight seam is the one element here that could not have been written for any other site; the `01 ─` numbering on an unordered list is the element most likely to read as generated.

