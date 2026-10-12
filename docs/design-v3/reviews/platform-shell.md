# REVISIONE INDIPENDENTE — platform-shell

Round 1 · premium_lift **6/10** · conforme: **NO** · implementabile: **NO**

> The forensic half of this document is the best I have reviewed: I recomputed all 21 contrast ratios in §4.0 and every one is exact to two decimals, the 13-glyph rail map matches `services.navigation()` key for key with no new asset needed, `--state-info-br: #5f84b5` is really there in tokens.css driving `.next-action`, `data-mode` really is declared nowhere, the count really is sewn into the label string, and a forbidden.py scan of the file returns zero violations. Then §4 declares every portal template `data-mode="DENSE"` "come impone il § 7" and immediately hangs `--shadow-2` on the inspector and `--shadow-3` on the account panel — §7 of the same binding document bans shadows on DENSE in the same table it cites, so the spec's headline fix for "Profondità: zero" is illegal on the pages it is meant to fix, and the document never notices. It is worse than that: §4.2 rewrites `case_header.html` with a four-fact anatomy that has no slot for `case.suspension_reason`, `status_since`, `progress.overdue`, or a multi-actor `responsible` list with organisation names — four things the current band renders and one of which ("Dossier suspendu") is a legal state of the file, which collides head-on with "workflow meaning is untouchable". The band also swallows the breadcrumbs and the `<h1>`, but it is rendered `{% if case %}`, and `components/page_header.html` — which carries title, eyebrow, lead and `lang` on twenty-plus platform templates — is not in the touched-template list at all, so an engineer building this literally ships a platform where most pages lose their title. Premium-wise the bar and band are genuinely strong and the official lock-up is the single most product-unifying move in the set, but the workspace where the user actually lives gets a bare `--min-0` canvas and a self-imposed shadow ban, so the owner's "backgrounds too simple or unmemorable" is answered in the chrome and conceded in the room.

## Violazioni dei vincoli non negoziabili

1. DESIGN_SYSTEM_V2 §7 (table line 213) and PREMIUM_2026_PRINCIPLES §14 (line 109) both state DENSE forbids «ombre». Spec line 228 declares every portal template `data-mode="DENSE"` «come impone il § 7», and then line 204 gives the inspector `--shadow-2`, line 143 gives the account panel `--shadow-3`, line 199 gives the collapsed-rail tooltip «suggerimento di livello 3», and lines 146/234 transition `box-shadow: none → --shadow-2` on the bar. The document's entire answer to its own difetto 7 is forbidden on the pages it declares.

2. WCAG 2.2 AA (4.5:1 for normal text). Spec line 250 specifies the skip link as «`--min-3` su `--accent-ring`» = #ffffff on #1d8a93 = **4.11:1**, computed. It fails AA on the first focusable element of every authenticated page. `--accent-ring` is defined in tokens.css as «focus ring, UI strokes» — a 3:1 non-text token — so this also misuses the token's declared role. `--accent` would give 6.32:1.

3. «ONE interactive accent … shared by links, primary CTA and focus; nothing else may use it» (tokens.css header). Spec line 169 paints the five-notch progress meter — a non-interactive data display — «piene in `--accent`». The spec contradicts itself: its own guard at line 309 limits `--accent` to «link, CTA, focus e barra della voce corrente» and does not list the meter.

4. «Role permissions … untouchable». Spec line 142 gates the command palette and line 199 gates the collapsible rail on `{% if user.is_staff %}` while claiming «nessuna chiave di contesto nuova». The project has a real RBAC in apps/accounts/roles.py (`role:operator`, `role:professional`, `role:legal_editor`, `role:content_editor`, `role:administrator`) that is explicitly separate from Django's `is_staff` — the module docstring criticises the old platform precisely because «its staff accounts all carried full administration». DESIGN_SYSTEM_V2 §9.1 assigns the palette to «operatore / professionista / redattore / admin». `is_staff` both hides the palette from the operational roles it is for and shows it to Django admins who are not operators. There is no `has_role` filter or context key in the codebase (grep: none), so the gate as written cannot express the intended rule.

5. Legal/product truth untouchable + «does not lose a fact the current screens carry». Spec line 151 says «`case_header.html` riscritto» and lines 154-171 give the complete replacement anatomy. The current template renders four things that anatomy has no slot for: `case.suspension_reason` as a `notice--warn` «Dossier suspendu» block, «depuis le {date}» (`status_since`) beside État, `progress.overdue` as «{n} en retard», and `responsible` as a list of `assignment.get_role_display` + `assignment.organisation.name` with the fallback sentence «Vous — aucun intervenant n'est assigné à ce dossier». DESIGN_SYSTEM_V2 §9.3 additionally requires «Multi-attore: due trame affiancate».

6. DESIGN_SYSTEM_V2 §9.1 specifies the case band as «`--mid-2` con la banda territoriale» and «riferimento in `--accent-dark`». Spec line 154 sets `.pband { background: var(--min-1) }` and line 140 removes the reference from the band entirely. The change is defensible (two midnight chapters on one portal page would break «one elsewhere»), but the spec overrides a binding clause silently — it argues explicitly against the Council on the 36→44px strip at line 200 and does not extend the same courtesy here.

7. MOTION_SYSTEM: every animation declares a trigger that exists. Motion entry 7, `shell.plate.copy` (line 240), is triggered by «clic sulla targa di contesto» — but line 140 defines that plate as a `<button>` that opens the palette for staff and a non-focusable `<span>` for the person. Neither role can trigger a copy; for the person it would be a pointer-only affordance with no keyboard equivalent. The «Référence copiée» announcement and the `check` glyph swap describe a clipboard action no part of the anatomy provides.

8. MOTION_SYSTEM cross-reference is wrong: line 77 rejects parallax as «vietato dal § 2 di MOTION_SYSTEM». §2 is «Le nove famiglie» and does not mention parallax; the prohibition is in §0 (forbidden example under PROFONDITÀ). Line 91 also lists as *accepted* from 21st candidate 1 a «molla criticamente smorzata 380/35/0.75» — a third spring; MOTION_SYSTEM §1 admits exactly two (SPRING_SETTLE 260/30, SPRING_FOLLOW 400/40), which §5 then uses correctly. §3 and §5 disagree.

## Lacune (ciò che l'implementatore dovrebbe inventare)

1. What renders the band on non-case pages. §4.2 folds breadcrumbs + `<h1>` + actions into `case_header.html`, which base_portal.html includes `{% if case %}`. `components/page_header.html` — used by academy, accounts, cases, companies, community, portal (20+ templates) and carrying `eyebrow`, `lead`, `lang`, `meta`, `align` — is absent from the §4.5 touched list, and the band anatomy has no `lead`, `eyebrow` or `meta` slot. The implementer must invent the whole non-case case.

2. The §4.5 «Template toccati» list is incomplete. Missing: `components/page_header.html`, `components/account_menu.html` (redesigned at line 143, and it contains the logout POST form with `{% csrf_token %}` — restyling it as a link would break logout), `components/language_switcher.html` (redesigned at line 144), `portal/partials/next_action.html` (moved into the workspace column per line 310), and the `{% block site_footer %}` in base_portal.html (reduced at line 198).

3. `{{ site.contact_email }}` currently sits in the portal footer. Line 198 reduces that footer «ai soli link legali» and moves only identity + «la riga legale» to the rail foot. The contact address is dropped with no replacement named.

4. How `platform-shell.css` is loaded and where it sits in the cascade. base.html preloads six v2 files and links `css/main.css`; base_portal.html links `portal/portal.css` via `{% block extra_head %}`. The spec names no link order, no `@layer`, and no relationship to `register.css` / `bridge.css` / the legacy layers — in a project that already ships `test_v2_bridge_is_temporary.py` for exactly this problem.

5. `--shell-bar-h: 52px sotto 768` and `--shell-row-h: 44px su (pointer: coarse)` (lines 114-117) exist only as CSS comments. No media query, no `@media (pointer: coarse)` block. Same for the plate, pinned at «altezza 32» on line 140 with no coarse-pointer override, against the ≥44px rule the spec asserts at line 256.

6. `.pbar` is never given a `position`. Sticky is implied by the scroll state (line 146), by `scroll-padding-block-start` (line 252) and by the rail's `inset-block-start: var(--shell-bar-h)`, but never stated.

7. The rail's `block-size: calc(100dvh - var(--shell-bar-h))` (line 192) is a fixed height on a sticky element whose natural origin is ~168px below the bar; at scroll position 0 it overhangs the viewport by the band's height. Unaddressed.

8. `content-visibility: auto` on inspector sections (line 298) with no `contain-intrinsic-size`, which produces scrollbar jump and breaks the sticky `max-block-size` arithmetic.

9. The context plate has no empty state. `portal_chrome.html`'s contract is `{% if portal_context %}`; the bar's new order puts `margin-inline-start: auto` after the plate, and the spec never says what the bar looks like on a page with no context (most non-case portal pages).

10. `<details>` dismissal. `language_switcher.html`'s own comment promises «JS closes it on Escape, outside click and focus loss», but `grep data-dropdown static/js/src/` returns nothing — that JS was lost in the V2 rewrite. The spec keeps `<details>` for account and language, upgrades them to 280px elevated panels, and does not list dismissal among `shell-portal.js`'s jobs (line 286). Two of the bar's three disclosures also get no MOTION §6 entry while the palette does.

11. The `<480` lock-up. Line 138 says «il solo tassello con `aria-label`», but `brand_lockup()` emits `<img alt="">` plus the wordmark in `.lock__text`; hiding the text with `display:none` destroys the accessible name, and an `aria-label` cannot be added without editing `apps/cms/templatetags/cms_nav.py`, which the spec does not declare. (Using `.vh` instead would solve it — the spec should say so.)

12. `rgb(29 138 147 / .30)` at line 215 is `--accent-ring` hardcoded as a literal instead of `color-mix(in srgb, var(--accent-ring) 30%, transparent)`.

13. `shell.strip.reveal-current` (line 239) is declared «legata alla posizione, non temporale» but its reduced state is `behavior: 'auto'`, implying the default is `'smooth'` — a UA-timed animation that is none of the four durations.

14. The `shell.rail.hover-follow` highlighter uses `scaleY()` (line 235) on rows that are all `--shell-row-h`; the spec does not say whether the highlighter has a border or radius, which `scaleY` would distort on any row that wraps (long AR labels, «Demandes qui me sont confiées»).

15. `--ok-800` and `--seal-700` are justified at line 123 against `--min-1`, but their stated uses sit on `--min-3` (pill, line 166) and as a non-text ring (line 168), where `--ok-700` measures 5.32:1 and `--seal-600` 3.99:1 — both already pass. Two new tokens added to a system that prides itself on «four shadow roles and no fifth».

## Segnali di «cheap / generico / default»

1. The skeleton is Linear: dark bar + `⌘K` + glyph rail + collapse toggle + palette with «Dossiers · Documents · Personnes · Actions» type filters. §8 names the risk and its four guards — the lock-up, mono plate, Newsreader 48/52, staff-only palette — are all labels applied to that same skeleton. Nothing in the workspace geometry itself is un-Linear.

2. The `<kbd>Ctrl K</kbd>` chip (line 142) is the single most-copied SaaS signifier of 2022-24. In 2026 it reads as dated shorthand for «we are a product», which is the opposite of the register the owner asked for.

3. The monogram avatar is used twice — 24px in the bar (line 143) and 28px in the rail foot (line 198). Initials-in-a-circle is the most default component in every starter kit, and the spec takes it from a 21st candidate without re-expressing it.

4. The territory graticule at 8 % opacity behind a mask that fades to transparent at 62 %, inside a 56px bar (line 146), is the answer to «backgrounds too simple or unmemorable» — and at that opacity on that surface it risks being literally below the threshold of perception. No minimum-perceptibility check is specified, so the most likely outcome is a memorable idea that nobody can see.

5. The workspace is where 90 % of the pixels and 100 % of the working time are, and it gets `--min-0` canvas with sheets on it and a self-imposed DENSE shadow ban. The chrome is enriched, the room is left empty. This is the owner's exact complaint, relocated rather than answered.

6. «ع» as the Arabic language label (line 144). Today `language_switcher.html` renders `{{ l.name }}` from `site.languages`. Replacing «العربية» with a single letter is a designer's shorthand, not a language name, and it hardcodes four languages over a data-driven list. It reads as a placeholder somebody forgot to finish.

7. The five-notch meter — «cinque `<span>` 16 × 4» (line 169) — is the default segmented-progress widget of every dashboard kit. Only the mandatory literal count beside it saves it, and the count is what already exists today.

8. The §4.4 state table applies one generic rest/hover/focus/active/current/disabled/loading/error grid uniformly to three components that do not share those states. «loading: scheletro livello 1 fermo» for a *rail row* is a cell filled in to complete a matrix, not a decision — it is the clearest AI-made tell in the document.

## MUST-FIX

1. Resolve the DENSE/shadow conflict in writing before any code. DESIGN_SYSTEM_V2 §7 bans shadows on DENSE; §2 gives level 3 (popover, menu, inspector) `--shadow-3`. The binding docs genuinely disagree, and a spec whose §1.7 headline is «Profondità: zero» and whose fix is shadows was obliged to say which clause wins. Either declare the workspace RICH with an argument, or carve an explicit §7 exception for chrome/level-3 surfaces, or find depth in ground, hairline and scale instead of shadow. Do not ship line 228 and line 204 in the same document.

2. Restore the four facts the rewritten band drops: `case.suspension_reason` («Dossier suspendu» + reason), `status_since` («depuis le {date}»), `progress.overdue` («{n} en retard»), and `responsible` as a multi-actor list with `organisation.name` and the fallback «Vous — aucun intervenant n'est assigné à ce dossier». DESIGN_SYSTEM_V2 §9.3 also requires two hatchings side by side for multi-actor. The suspension notice is a legal state of the file and is non-negotiable.

3. Specify what renders the band on non-case pages, and what happens to `components/page_header.html`. The band currently absorbs the breadcrumbs and the `<h1>` but is included `{% if case %}`; `page_header.html` is on 20+ platform templates and carries `eyebrow`, `lead`, `lang` and `meta` that the band has no slot for. As written, most of the platform loses its title, or keeps `.page-header__title` at 38/36 and difetto 10 is not fixed while two title systems coexist.

4. Replace `{% if user.is_staff %}` (lines 142, 199) with the real role predicate. `apps/accounts/roles.py` defines OPERATOR, PROFESSIONAL, LEGAL_EDITOR, CONTENT_EDITOR, ADMINISTRATOR as Django groups deliberately separate from `is_staff`. State the exact role set, and name the context key or template filter that exposes it — there is none today, so «nessuna chiave di contesto nuova» is not achievable and should be withdrawn.

5. Fix the skip link: `--min-3` on `--accent-ring` is 4.11:1, an AA failure on the first focusable element of every authenticated page. `--min-3` on `--accent` gives 6.32:1. Also stop using `--accent-ring`, a declared 3:1 non-text token, as a text ground.

6. Remove `--accent` from the five-notch meter (line 169) or amend the §8 guard (line 309) to admit it. As written the document forbids at line 309 what it prescribes at line 169.

7. Delete or re-anchor Motion entry 7 `shell.plate.copy`. Its trigger contradicts the plate's own definition at line 140 for both roles, and for the person it would be a pointer-only affordance with no keyboard path.

8. Complete the §4.5 touched-template list — `components/page_header.html`, `components/account_menu.html` (note the logout POST form and its CSRF token), `components/language_switcher.html`, `portal/partials/next_action.html`, the `{% block site_footer %}` — and say where `{{ site.contact_email }}` goes.

9. Assign `<details>` dismissal (Escape, outside click, focus loss) to `shell-portal.js` and give the account and language menus MOTION §6 entries. `language_switcher.html`'s comment promises behaviour that no longer exists in `static/js/src/`, and the spec upgrades those menus to 280px elevated panels without restoring it.

10. Give the workspace a material idea. The bar and the band are answered; `--min-0` plus sheets is not an answer to «backgrounds too simple or unmemorable» for the surface the user actually inhabits. Whatever it is — a paper grain, a ruled column measure, a ground change under the central sheet — it has to be specified with tokens and an opacity that is demonstrably visible, not 8 % behind a 62 % mask.

11. State the CSS load order and the cascade strategy for `static/css/v3/platform-shell.css` against `portal.css`, `register.css`, `bridge.css` and the legacy layers, and add the coarse-pointer and 768 media queries that currently exist only as comments on lines 114-117 and 140.

12. Fix the two citation errors: MOTION_SYSTEM's parallax ban is §0, not §2 (line 77), and the «380/35/0.75» spring accepted at line 91 is a third spring the system does not admit — §3 and §5 must agree.

