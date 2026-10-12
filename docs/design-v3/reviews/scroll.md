# REVISIONE INDIPENDENTE — scroll

Round 1 · premium_lift **5/10** · conforme: **NO** · implementabile: **NO**

> The audit (§1) is the best part of this document and is verifiably true — I confirmed the 11 `[data-reveal]` (3 in `_hero.html:39,40,42`, 8 in `_pilot.html:42`), that `.home-reserved` carries no `.section` class, that `.voyage__svg{display:none}` below 63.999rem kills every mobile scroll graphic, and that the contrast figures match `static/css/v2/tokens.css` line for line. But the proposal breaks the one motion rule that governs this whole surface: `MOTION_SYSTEM.md` §4 and `DESIGN_SYSTEM_V2.md` §5 allow **one** scroll-indexed object per page, zero on STANDARD/DENSE/LEGAL, and §5 of this spec ships eight scroll-linked families on the home plus a `scroll(root block)` bar injected into the global `templates/partials/header.html`, i.e. onto the fascicolo, the lists and the legal notices. §7 dodges this by arguing the scroll animations "non sono loop" — true, and irrelevant, because the clause it needs to answer is the scroll clause, which it never quotes. It is also not implementable as written: the seam's signature element (the 62% datum line) has no selector, no keyframes and no free pseudo-element, `--at` is referenced in CSS and declared nowhere so `tests/frontend/test_css_tokens_exist.py` fails on the new file, the `.voyage__figure` wrapper silently destroys the `<64rem` grid areas that place the two shores around the step list, and `static/css/v3/scroll.css` is never registered in `static/css/main.css`, the single entry point. And on the owner's actual complaint, this answers with 1px lines, 1×16px ticks, a 2px bar and 42px of parallax across ten screens, while §7 presents "nessuna immagine aggiunta" as a virtue on the day the owner asked for more images — it is the rejected editorial-severe register with a better vocabulary.

## Violazioni dei vincoli non negoziabili

1. ONE scroll-indexed object per page (MOTION_SYSTEM.md §4: «Una pagina IMMERSIVE può avere un loop ambientale e **un oggetto indicizzato allo scroll**; STANDARD, DENSE e LEGAL nessuno») — broken by §5 MOTION, which declares eight scroll-linked families on the home at once: seam.rise, seam.datum, seam.ticks (×4 boundaries), voyage.route, readbar.fill, parallax.header-dark, on top of the existing hero photo ViewTimeline and the tide loop. §7 «Immagini, loop, altezza» answers only the loop half («le animazioni guidate dallo scroll non sono loop, non avendo durata propria») and never addresses the scroll clause of the rule it names as binding on line 4.

2. Scroll-linked motion is forbidden outside IMMERSIVE (DESIGN_SYSTEM_V2.md §7: STANDARD «reveal 240 ms», DENSE «transizioni di stato, molla di layout · vietato: reveal», LEGAL «nulla») — broken by §4.5, which puts `.readbar` with `animation-timeline: scroll(root block)` as the last child of `templates/partials/header.html`, i.e. on every public page and every platform screen. The gate described in §4.5 «Esistenza» (≥4 sections + ≥3 viewports) is a) satisfied by a long fascicolo or a privacy notice, and b) applied in the given markup to `<nav class="readbar__marks" hidden>` only — `.readbar__fill` is unconditioned and always animates.

3. «durata ≥ 600 ms fuori dai capitoli immersivi» is question 6 of the sixty-second test (ANTI_PATTERNS.md §5) — broken by §4.3 table row `figure` (600 ms) and §5 entry `reveal.figure`, whose scope is «SVG, diagrammi, **rail di giurisdizione**». The jurisdiction rail is a RICH/STANDARD pathway component, not an immersive chapter. The same line adds `--motion-trace: 600ms`, a fifth duration token, against MOTION_SYSTEM.md §1 «Nessun altro numero» (defensible only if read against DESIGN_SYSTEM_V2.md §5's «600–900 ms» range, and only inside immersive chapters).

4. «Il teal del territorio è grafica; mai testo, mai interazione» (DESIGN_SYSTEM_V2.md §1.3 rule 2) — broken by §4.4: «superata, filetto `--terr-line` (6,07:1)». `--terr-line` is used there as the state mark of a step in an interactive, keyboard-reachable list, beside `--accent-dark` for the current step. That is a second teal doing interaction work.

5. «colour never alone» / §6's own claim «Colore mai solo» — false for the pair that matters. §4.4 separates *current* from *passed* by hue only: `--accent-dark` filetto vs `--terr-line` filetto, two teals at 10,01:1 and 6,07:1 on `--mid-1`. The filled-vs-empty dot separates *reached* from *not reached*, and `aria-current="step"` serves AT only; a sighted user distinguishing current from already-passed gets colour and nothing else.

6. «transform/opacity only» (performance constraint) — §5 entry `voyage.station` animates `fill` and «colore del filetto» over 180 ms. MOTION_SYSTEM.md §2 does sanction colour for the STATO family, so this is arguable, but the spec never declares the exception and the brief's rule is literal.

7. «Vietate: … `linear` fuori dai loop» (MOTION_SYSTEM.md §1) — six §5 entries declare curve «lineare». This is the right choice for a scrub and MOTION_SYSTEM §2 gives the SCROLL family curve «—», but the spec must say so explicitly or it reads as a fourth curve introduced without argument.

## Lacune (ciò che l'implementatore dovrebbe inventare)

1. The seam's signature graphic has no implementation. §4.2 says «Alla quota 62 % corre la linea di livello: 1 px `--terr-line`, `scaleX(0→1)`, `view()`, `animation-range: entry 0% entry 85%`» — but the code block already spends `.chapter--dark::before` on the gradient and `.chapter--dark::after` on the exit gradient. No element, no class, no `@keyframes`, no `view-timeline-name` on the chapter. Same for `seam.rise` itself: the §5 table names `translateY(-14px → 0)` on `::before` and the §4.2 block writes only the rest state `transform: translateY(0)`.

2. `--at` (§4.5, `inset-inline-start: calc(var(--at) * 100%)`) is referenced in CSS and declared in no stylesheet. `tests/frontend/test_css_tokens_exist.py` fails the new file unless `--at` is added to `RUNTIME_PROPERTIES` (today `{"--nav-drawer-top", "--reveal-index"}`). The spec also never says how it is set — and the project's own comment in `static/css/v2/voyage.css` lines 108-112 tells the implementer that style attributes are CSP-blocked, while `static/js/main.js:347` shows the sanctioned CSSOM route (`style.setProperty("--reveal-index", …)`). The implementer will have to work this out, and may well invent the class-ladder workaround used by `apps/orientation/engine.py:387`.

3. The `.voyage__figure` wrapper (§4.1, «+1 `<div class="voyage__figure">` intorno ai tre elementi della colonna figura») silently breaks the mobile layout. `static/css/v2/voyage.css` lines 168-176 lay `.voyage` out as areas "south" / "steps" / "north"; once the two `.voyage__shore` paragraphs and the SVG are nested in a div, their `grid-area: south|north|line` is inert and the northern shore stops closing the list. No `<64rem` rule is given, and no internal layout for `.voyage__figure` at any width.

4. The mobile drawing (§4.4, «la spina resta e riceve il disegno che oggi non ha, `scaleY()` sul suo `::before` legato a `--voyage`») is not implementable. `.voyage__step::before` is already the 7px station dot (voyage.css 200-211) and the spine is `border-inline-start: 1px solid var(--hairline-dark)` on `.voyage__step`, which cannot be scaled. A new element is needed, plus a per-step timeline — with a single `--voyage` timeline every step would draw simultaneously.

5. The synchronisation claim of §4.4 («la linea raggiunge la stazione n esattamente quando si legge la tappa n») does not follow from the code given: `view-timeline-name: --voyage` is declared on `.home-pilot`, which contains `.section__header` (eyebrow + title + lead), the note and the «Découvrir le projet pilote» link. `animation-range: contain 0% contain 100%` therefore spans several hundred pixels in which no step is being read. The timeline belongs on `.voyage__stations`.

6. `static/css/v3/scroll.css` is never registered. `templates/base.html:39` loads exactly one stylesheet, `css/main.css`, whose `@import` list ends at `v2/voyage.css`. §4.1 says «dopo `v2/voyage.css`» but names neither `main.css` nor the preload block (base.html 26-38). As written the file does not load.

7. Readbar geometry is undefined. `--rail-h: 2px` is added to `scroll-padding-block-start` (§6) but nothing says whether the bar lives inside the 64px `--header-height`, adds 2px to it, or replaces `.site-header`'s existing `border-block-end: 1px solid var(--hairline)` (shell.css:92). §3 asserts «la nostra barra È il bordo inferiore dell'header» and no rule implements that.

8. Readbar existence is contradictory: §4.5 «Esistenza» describes the whole bar disappearing, the markup puts `hidden` on `<nav class="readbar__marks">` only. What JS toggles, and what the always-present fill does on a login screen, is undecided.

9. Reduced-motion readbar has no mechanism: §5 `readbar.fill` reduced state is «scatto discreto al confine della sezione corrente (stessa IO)». Once the CSS scroll animation is gated out by `@media (prefers-reduced-motion: no-preference)`, some per-section `scaleX` value has to be written from JS — again through an undeclared custom property.

10. Touch behaviour of the marks is unspecified and probably hostile: §4.5 asks for 44×44 contact areas on `pointer: coarse`, hanging from a 2px bar across a 390px viewport with 8+ sections (≈48px apart). They overlap, they are invisible, and 44px of them sits over the top of the page. No `pointer-events` rule, no minimum spacing, no decision to drop the marks on coarse pointers.

11. The rest appearance of `.readbar__mark` is never given — only «opacità 0,55→1» in §5 and `--rail-track: color-mix(in srgb, var(--ink) 16%, transparent)` for the track. A focusable `<a>` whose only visible indicator is ~9% ink fails 1.4.11 (3:1 for UI components).

12. New UI string «Sections de la page» (§4.5) has no translation plan. With `{% translate %}` and no .po entries the AR document announces a French `aria-label` with no `lang`, on a surface the brief scopes to FR/IT/EN/AR.

13. Tokens declared and never used: `--seam-lift`, `--reveal-lift`, `--reveal-lift-fine` (§4.2). Every value is then hardcoded (14px, 10px, 6px) in the CSS and the tables.

14. The legacy reveal system is ignored. `static/js/main.js:339-347` drives `.reveal` / `.reveal--stagger` / `--reveal-index` and `static/css/components.css:3085` transitions on it. §4.3 generalises `html.js [data-reveal]:not(.is-in){opacity:0}` site-wide without saying what happens on pages that already carry `.reveal`, or on `templates/orientation/result.html:81` (`data-reveal-once`).

15. Scope is claimed but not delivered: the header says «superficie: tutto il pubblico e la piattaforma», and §4 specifies the home and the header. Nothing addresses the platform screens in `docs/design-v2/before/*.png` (person_dashboard, case_file, forum) beyond hiding the bar on short pages.

16. Internal contradiction on direction: §1.3 condemns the current reveal because «parte da −10 px, cioè scende mentre lo scroll sale»; §4.2 then specifies the seam as `translateY(-14px → 0)` — the same downward travel — while the prose says «il capitolo scuro non compare: **sale**». An implementer cannot tell which way the seam moves.

17. §4.4 hardcodes the arithmetic on 8 steps («24vh × 8», «≈ 2 090 px»), but the template renders `d.steps|length` from the CMS. The CSS survives a different count; the height claim, the pin budget and the HUMAN_QA note do not.

## Segnali di «cheap / generico / default»

1. A thin accent progress bar welded under a sticky header is the most generic scroll ornament of the last decade. §3 identifies this precisely (risk 2, and it rejects ibelick/motion-primitives «Scroll Progress» for exactly this reason) and then ships that component's mechanic verbatim — `scaleX` with a logical `transform-origin`. Dots with `aria-current` do not change what it reads as in the first two seconds, which is the test the owner applies.

2. Sticky media column on the left, steps scrolling on the right (§4.4) is the Aceternity / Apple product-page scrollytelling layout — the same shape the spec rejects in «Scroll Reveal Content A» and «Scroll 01». Naming the risk (§8.1) is not a guard, and the stated escape («se la sincronia si perde in collaudo si elimina il pin») means the one genuinely ambitious move in the document is pre-authorised to be deleted.

3. Gradient fades between sections (§4.2, 128px + 96px) is what a generated page does first. Restricting it to two ground stops with no hue shift is the right discipline, but the artefact on screen is still «a gradient between two sections».

4. The total visual amplitude of the proposal is 1px datum lines, two 1×16px corner ticks, a 2px bar, 6-14px lifts and 42px of parallax across 10.3 screens. §4.6 states the intent as «si legge come spessore, non come movimento» — that is the severe, flat, editorial register the owner rejected on 23 September, restated with better vocabulary. Nothing here is «spettacolare con misura».

5. The 1×16px `--hairline-strong` corner ticks are claimed in §4.2 as «la nostra firma … non somiglia a niente del catalogo». At 1440px they are two hairline dashes in the container margin. A signature has to be perceptible to function as one, and this claim is unfalsifiable as stated.

6. Zero answer to «not enough elegant modern coherent IMAGES» — §7 presents «Nessuna immagine aggiunta» as a virtue. On the surface the owner named as weak, the scroll spec is where new imagery would earn its keep (the pinned figure column is literally an empty 26rem slot holding a 140px SVG).

7. `--rail-track: color-mix(in srgb, var(--ink) 16%, transparent)` on a 2px bar renders as a barely-there grey line. Combined with marks at opacity 0.55 of an unspecified colour, the readbar's rest state will read as unfinished rather than restrained.

8. `--seam-out: var(--min-0)` plus `:has(+ .section--process)` producing an exit gradient back to ground is a fade-to-and-fade-from device; on the home it applies once. Fine here, but the rule as written («ogni cucitura») invites a page that dissolves at every boundary, which is the Tailwind-landing look.

## MUST-FIX

1. Resolve the scroll-object budget head-on. MOTION_SYSTEM.md §4 says one scroll-indexed object per page; §5 of this spec lists eight on the home. Either amend MOTION_SYSTEM.md in the same change with a written argument (scroll-driven CSS on the compositor is not the same 'living object' the rule was written against, and the rule's cost model was per-frame JS), or cut to one scroll-indexed *system* per page and say which. Not addressing it is not an option: the spec names that document as binding on line 4.

2. Take the readbar off DENSE and LEGAL pages structurally, not by heuristic. `animation-timeline: scroll(root block)` in `templates/partials/header.html` means every fascicolo, list and privacy page gets a scroll-linked animation that DESIGN_SYSTEM_V2.md §7 forbids. Gate the whole `.readbar` on the template's existing `data-mode` (IMMERSIVE/RICH only) and put the `hidden` on `.readbar`, not on `.readbar__marks`.

3. Specify the datum line: element or pseudo-element (both of `.chapter--dark`'s are taken), class name, the `view-timeline-name` declaration on the chapter, the `@keyframes`, and the `@supports` + `prefers-reduced-motion` wrapper. As written the single graphic that carries the seam's meaning does not exist.

4. Declare `--at`: name it something that cannot collide (`--readbar-at`), state that `shell.js` writes it with `element.style.setProperty()` (CSSOM, not a style attribute — cite `static/js/main.js:347` as precedent), and add it to `RUNTIME_PROPERTIES` in `tests/frontend/test_css_tokens_exist.py`. Otherwise the new stylesheet fails an existing test on day one.

5. Give the `<64rem` layout for `.voyage__figure`. The wrapper as proposed orphans `grid-area: south|north|line` and moves the northern shore off the end of the step list — losing the 'route between two shores' framing that `_pilot.html`'s own comment says the drawing exists to carry.

6. Move `view-timeline-name: --voyage` from `.home-pilot` to `.voyage__stations`, or the 'line reaches station n when step n is read' claim is false by the height of the section header plus the note and the link.

7. Separate current from passed by form, not by two teals. Keep `--accent-dark` for the current step and mark 'passed' with the same accent at reduced weight plus a filled/hollow or rule-thickness difference; `--terr-line` must not carry state (DESIGN_SYSTEM_V2.md §1.3 rule 2).

8. Reconsider `aria-current="step"` on `.voyage__step`. The pilot sequence is prescribed legal content and `_pilot.html`'s comment states the pilot is never presented as an authorised channel. `aria-current="step"` plus a class literally named for a step being 'reached/superata' announces reading position as process position, which is a meaning the content does not assert. Use `aria-current="true"` on the readbar mark only, and drive the station fill as decoration (`aria-hidden` SVG), or justify the semantic explicitly.

9. Scope the 600 ms `figure` trace to immersive chapters only (ANTI_PATTERNS.md §5 q.6), and restrict `--motion-trace` to that scope in MOTION_SYSTEM.md §1 when adding it.

10. Register the file: add `@import url("v3/scroll.css")` to `static/css/main.css` after `v2/voyage.css` and the matching preload in `templates/base.html`.

11. Settle the readbar's 2px: does it sit inside `--header-height`, extend it, or replace `.site-header { border-block-end }` (shell.css:92)? Give the rule, and give the mark's rest colour with a computed ratio (≥3:1, WCAG 1.4.11) — or drop the marks on `pointer: coarse` rather than hanging 44px invisible targets across the top of a 390px page.

12. Fix the direction contradiction in §4.2 (`translateY(-14px → 0)` described as 'sale') and, whichever way it travels, state the `::before` geometry that guarantees no hard midnight edge appears above the gradient during the travel.

13. Raise the amplitude or admit the answer is incomplete. A 2px bar, 1px lines and 42px of parallax will not read as 'authoritative but spectacular with measure'. The pinned figure column is the one place in the document with room for something memorable — give it the art-directed image and the drawn territory the owner asked for, inside the 120 KB per-viewport budget, or say in §8 that imagery is delegated to `imagery.md` and that this spec deliberately answers only the structural half.

