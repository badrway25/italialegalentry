# REVISIONE INDIPENDENTE — backgrounds

Round 1 · premium_lift **6/10** · conforme: **NO** · implementabile: **NO**

> The central idea is genuinely good and genuinely not generic — a designed threshold instead of a hairline, the graticola masked at 2.8% so it reads as atmosphere rather than a table, and grain-as-alpha-mask doing double duty as the ramp's anti-banding dither. That earns real credit, and the refusals (WebGL, aurora, glassmorphism, animated grain) are argued, not cargo-culted. But the spec is written as though it were measured, and it was measured at 1440 only: I reproduced the live home at 1440/768/390 and five of the nine sections put content inside the ramp below 1200px, which breaks the spec's own §6 hard rule and fails the test it proposes in the same paragraph. Worse, it hard-codes neighbour relationships (`th--from-*`) as static classes into partials that Django emits from a DB-ordered, gate-filtered loop (`apps/pages/services.py:646-668`), and on the live page `_trust` — whose real predecessor is the midnight `_pilot` — is given `th--fold th--from-area`, so the one boundary that most needs an ascent gets a paper-to-paper fold while the spec simultaneously deletes the hairline that currently marks it: a raw 15.4:1 cliff, exactly the §1.3 defect this document exists to kill. Add the undeclared `--th-*-mid` tokens, a §4.7 state table with zero selectors behind it whose hover is a 1.03:1 change (the spec convicts 1.076:1 as invisible in §1.1), a 600ms duration with no token where `--motion-draw` is 900ms, and a §4.6 photographic ground with no markup and no CSP-safe path for the image URL — and this is a strong concept wrapped in a spec an engineer cannot build without inventing the load-bearing half.

## Violazioni dei vincoli non negoziabili

1. MOTION — one immersive trace: the brief allows four durations {120,180,240,320ms} plus ONE immersive trace, and `static/css/v2/tokens.css:111` implements it as `--motion-draw: 900ms`. §5 specifies `ground/soglia-marea` at **600 ms** with no token defined anywhere, and §8 risk 5 caps thresholds at 2 descent/ascent + 3 folds = up to **5 `.tide` elements per page**, each firing a 600ms trace. That is five immersive traces where the system allows one, at a duration that does not exist in the token set.

2. ONE interactive accent: §4.3 `.ground--midnight{ --lume:rgba(127,209,216,.08) }` and §8 risk 2 ('il lume usa solo bianco (carta) o `--accent-dark` (mezzanotte)') spend `--accent-dark` (#7fd1d8) as ambient decoration. `v2/tokens.css:6-9` states the accent is interactive-only: 'ONE colour is interactive: links, the primary action and the focus ring share it, and **nothing else may use it**.' The spec does not amend §1.3 and does not argue the exception.

3. At most two midnight chapters on HOME: §4.5 assigns `_hero.html` → `ground--midnight` (--mid-1), `_pilot.html` → `ground--midnight` (--mid-1) and `templates/partials/footer.html` → `ground--utility` (--mid-0). That is three dark grounds — counted by the spec's own method, since §1.6 convicts the forum precisely by counting '`navy` + piè di pagina `--mid-0` + area `--min-1`' as three. The spec never states whether the utility footer is exempt, so by its own accounting it breaks the cap it enforces on others.

4. CSP `style-src 'self'` — §4.6 'La superficie fotografica': a photograph 'diventa **fondo di capitolo**' with 'AVIF+WebP 480/800/1200' and srcset, receiving the `doorway__overlay` vignette plus grain. No markup shape, no element, and above all **no mechanism for getting a per-section image URL into CSS**. Any CMS-driven background image requires either `style="--photo:url(...)"` (banned) or a generated stylesheet (unspecified). As written §4.6 cannot be implemented under `style-src 'self'`.

5. Colour never alone / state feedback below the spec's own discrimination floor: §4.7 hover on `.ground--sheet` goes `--min-2` #fbfaf8 → `--min-3` #ffffff = **1.03:1**; active goes to `--min-1` #ecebe6 = **~1.06:1**. §1.1 declares 1.076:1 and 1.064:1 to be 'sotto la soglia differenziale … sparisce del tutto in luce ambiente forte'. The spec therefore ships, as its only hover and active affordance, a colour-only change it has itself certified as imperceptible — and specifies no non-colour companion and no `:focus-within` equivalent.

6. Tricolour only in the official mark: §1.6 correctly convicts `.forum-cta { background: var(--forum-navy) }` (`apps/forum/static/forum/forum.css:141`), but §4.5 does not touch `templates/forum/partials/cta_row.html` or `apps/forum/static/forum/forum.css`, while §8 risk 6 promises 'Un test fallisce su qualunque `background-color` di sezione che non sia uno dei cinque token'. The spec ships a test that fails on code it declines to fix.

## Lacune (ciò che l'implementatore dovrebbe inventare)

1. §4.3 uses `var(--th-descent-mid)`, `var(--th-ascent-mid)` and `var(--th-fold-mid)` in `.th--descent/.th--ascent/.th--fold`, but **none of the three is declared in the `:root` block**. They exist only as prose rows in the §4.2 table, and the `@supports` sRGB fallback promised there ('→ letterale `#5c6769`') appears nowhere in the CSS. As pasted, all three thresholds resolve to `transparent` at the mid stop.

2. The `--ground-prev` contract is baked into each partial as a static class, but `apps/pages/services.py:634-668` builds the home from `HomeSection.objects.visible()` filtered by `section_gate_open()` and `PHASE3_ONLY_SECTIONS = {PILOT, ANTIFRAUD, RESERVED}` (`apps/pages/content.py:103`). Section presence and order are DB- and phase-controlled — the live order I measured (hero, entrances, orientation, pathways, pilot, trust, antifraud, news, ecosystem, reserved) already differs from `SECTION_DEFAULTS`. The spec never says how the ramp survives reordering; the obvious CSS-only fix it does not propose is sibling selectors (`.ground--midnight + .ground{ --ground-prev:var(--mid-1) }`), which the DOM supports because the loop emits siblings.

3. Threshold heights are calibrated to 1440 only. Measured `padding-block-start` on the live home: `home-entrances` (`section--b`, `th--ascent`, `--th:96px`) = 96 / **64** / **48**px at 1440/768/390 → overruns by 32px and, with the `--th:56px` mobile override, by 8px. `home-orientation`, `home-pathways`, `home-news`, `home-ecosystem` (`section--c`, `th--fold`, `--th:48px`) = 48 / **32** / **32**px → overrun by 16px at both smaller widths, because `@media (max-width:47.999rem)` lowers `--th` only for `.th--descent,.th--ascent`, explicitly not for `.th--fold`. §4.2's 'zero px di altezza aggiunta' and §6's test `test_v3_threshold_is_clear.py` both fail as specified. No rank→threshold mapping table is given.

4. §4.7 defines seven states and §4.3 contains **not one selector for any of them** — no `:hover`, no `:focus-within`, no `[aria-disabled]`, no loading or error hook. '`.ground--sheet` interattivo' is never defined: the implementer must invent which element that is (`a.ground--sheet`? `.ground--sheet:has(a)`? a `<button>` wrapper?) and write every state rule from scratch.

5. `templates/portal/partials/portal_chrome.html` **does not exist**. The directory contains access_point.html, card.html, case_header.html, deadline_item.html, next_action.html. The row that carries the entire platform application of the system ('barra di contesto `ground ground--midnight`, rail `ground ground--area`') points at a non-existent file and names no selector, so the platform half of §4.5 is unbuildable as written.

6. `_banner.html` (SectionKey.BANNER, order 20, gate `forum_banner`, sits between hero and entrances) is absent from §4.5's table. It is gated shut on :8771 today, so `_entrances th--from-midnight` is correct at this moment, but the gate is time- and editor-controlled; when it opens, entrances ramps up from a midnight that is no longer its predecessor.

7. Deleting `apps/pages/static/pages/css/pages.css:47-49` removes the hairline everywhere, but §4.5 gives `_antifraud.html` and `_reserved.html` no threshold ('sono code di capitolo'). Measured today, both carry `border-block-start: 1px rgb(211,210,204)`. After the change, ecosystem→antifraud→reserved and trust→antifraud are consecutive paper grounds with neither ramp nor rule — the §1.1 defect, reintroduced. `home-reserved` additionally has `padding-block-start: 0px` and no `.section` class, and its content sits inside an opaque `#f4f3f0` `home-reserved__panel`, so `.ground--paper` on it paints grain and graticola under an opaque box: no effect at all.

8. `_hero.html` and `_pilot.html` already carry `chapter--dark`, and `layout.css` also ships `.section--verso` and `.section--inverse`. `.ground--midnight` re-declares `color: var(--on-dark)`. The spec never says whether `chapter--dark` is kept, removed, or how the three dark mechanisms compose.

9. §5 `ground/graticola-deriva` is to be paused by 'il comando «Suspendre le mouvement» già esistente'. That control is hero-scoped: `static/js/src/home.js:63` does `hero.querySelector("[data-tide-toggle]")` and the pause classes `.is-offscreen`/`.is-paused` are read only by `.hero__territory--layer-*` in `v2/hero.css:81-86`, and home.js runs only on the home. Putting the loop on 'le quattro landing di via' and the forum needs a new per-page observer, a new visible labelled control (a **new UI string**, which must clear `forbidden.py` and contradicts §4.5's 'non cambia una sola parola'), and a JS entry point on pages that load none. Budgeted at '< 700 B'.

10. The §4 ambient-quota claim ('si attiva sulle quattro landing di via e sul FORUM') is asserted, never verified. `v2/tokens.css:112` documents `--motion-ambient: 28s` as 'the one living object per page: the tide'; the spec does not show those pages have their quota free.

11. `prefers-contrast: more` does not do what §6 claims. §4.3 sets the kill-switch on `:root`, but `.ground--midnight` and `.ground--utility` re-declare `--grat-ink`, `--grain-ink`, `--grain-amount` and `--lume` **on the element itself**, and an element-level declaration always beats an inherited one. High contrast therefore flattens the paper chapters and leaves the midnight chapters fully textured. (The `[data-mode="dense"] .ground` rule works, because it targets the same element at higher specificity — which shows the author knew the mechanism and then used the wrong one three lines later.)

12. §4.3 writes `mask-mode: alpha;` **before** the `mask:` shorthand. The shorthand resets `mask-mode` to `match-source`, so the declaration is dead — and §4.4's verification ('Verificato in Chromium 153: `CSS.supports('mask-mode','alpha') === true`') and HUMAN_QA item §6-2 both rest on a property the stylesheet discards.

13. `.ground::before` is inset by `var(--th)`, so on every threshold section the graticola begins abruptly at y=96px (or 48px) at full mask opacity — a new horizontal seam where the grid starts, on the very boundary the spec was written to smooth. Not mentioned, not guarded.

14. `.th--from-paper` is used on `templates/partials/footer.html` in §4.5 but is never defined in §4.3 (only `--area`, `--sheet`, `--midnight` exist). It happens to work because `--ground-prev` defaults to `--min-0`, but it ships as a dead class in markup.

15. §7's 'Due pseudo-elementi per capitolo, **nessuno promosso** (nessun `will-change`, nessun `transform` a riposo)' contradicts §5, which runs `translate3d` for ≥28s on `.ground::before` — a full-section, mask-carrying, three-gradient layer that compositing will promote and must rasterise. The CDP figures (0 layout, 0 recalc, 6.5ms) were taken on the static prototype `bg/proto3.html` and do not cover the one animation the spec actually adds.

16. Arithmetic slip in the one number I recomputed independently: `--tide` rgba(63,166,175,.45) over `--mid-1` #0e1b23 composites to **#245a62 at 2.26:1**, not '#22535b, **2,05:1**' (§4.2, §6). `--min-edge`/`--accent` at 4.87:1 checks out exactly, so the model is sound — but a document whose authority is 'misurati, non stimati' should not have a wrong composite in its accessibility section.

17. §4.2 justifies `--contact` as 'variante di ruolo 2 … per non rompere il test `grep box-shadow`'. `v2/tokens.css:75` says 'SHADOWS — four roles, and no fifth', and the only box-shadow assertion I can find in `tests/frontend/test_design_docs.py:794` is about the focus ring, not a shadow-role census. The named guard does not exist, so 'si registra come variante' is an assertion with nothing enforcing it.

18. §4.6 introduces images without an alt-text policy, on the one surface where the forbidden-wording rule bites ('including alt / ARIA / title'). §4.5's 'Nel corpo dei template non cambia **una sola parola**' is contradicted by §4.6 and by §5's required pause control.

## Segnali di «cheap / generico / default»

1. The stack the spec actually ships — flat ground + noise + orthogonal grid + one corner radial glow — **is** the jatin-yadav05/meghtrix recipe it studied at §3 rows 3-4, and it is the most-copied dark-background formula of 2024-25. §3 row 7 mocks Aceternity for being copied ('memorabile è ciò che non si trova su 21st.dev') and then assembles the same four layers. The only claimed differentiator is that the module is 160px to match `scripts/territory.py` — a correspondence nobody can perceive at 2.8% opacity under a radial mask. This is the document's biggest unguarded risk and it names every other risk but this one.

2. The hover at 1.03:1 and active at 1.06:1 (§4.7). Nothing reads cheaper than an interactive surface that does not respond; and it is the exact failure the spec opens by condemning.

3. `--contact: 0 1px 0 rgba(255,255,255,.7) inset, …` (§4.2). A 70%-white inset top highlight on a sheet is the 2010 bevel. On #fbfaf8 it is nearly invisible; where it is visible it will read as Bootstrap-era chrome, not as 2026 material.

4. The 1px `.tide` line. The spec's whole §1.3 argument is that a 1px line 'non separa, graffia' — and its replacement for the boundary event is a 1px line in a different colour, at 2.26:1, animated by a scaleX wipe. A teal hairline that draws itself is a very common 2021-2023 section-divider tic; at 5 per page (§8 risk 5) it becomes exactly the 'decorazione, non composizione' the spec warns against, and §8 risk 5 guards the count but not the tic.

5. The abrupt grid-start seam at y=--th on every threshold section (see gaps): a second, unintended hairline, produced by the fix for the first one.

6. `graticola-deriva` drifts the `::before`, which carries the lume in the same background stack — so the 'light source' slides with the grid. A light that moves with the surface it lights is the classic tell of a generated background. The spec does not say whether this is intended.

7. §4.6 is the section that answers the owner's loudest complaint ('non abbastanza immagini eleganti moderne coerenti') and it is one paragraph long with no markup, no selector, no example and no mechanism. A duotone-everything pipeline is also the fastest route to imagery that reads as a filter applied to stock — the spec offers no art direction, no crop rules, no subject guidance beyond 'mai cronaca migratoria'.

8. Nothing in the proposal is **dynamic**, which was an explicit item on the owner's rejection list. §5 delivers one 1px wipe, one rail indicator and one 28s drift that is switched off on the home. The spec argues statelessness as a virtue (§2, §7) — that argument is sound on performance and is precisely the 'institutional = sober' register the owner forbade as an excuse.

## MUST-FIX

1. Fix the `_pilot` → `_trust` boundary. On the live page the midnight `_pilot` is followed by `_trust`, which §4.5 gives `th--fold th--from-area` (a 48px ramp starting at #ecebe6). Combined with deleting `pages.css:47-49`, the only true light→dark→light passage on the home loses both its ramp and its hairline and becomes a raw #0e1b23 → #ecebe6 cliff. `_trust` must carry `th--ascent th--from-midnight`.

2. Replace the static `th--from-*` classes with sibling-derived grounds. Section presence and order come from `HomeSection.objects.visible()` + `section_gate_open()` + `PHASE3_ONLY_SECTIONS` (`apps/pages/services.py:634-668`, `apps/pages/content.py:103`); the rendered order already differs from `SECTION_DEFAULTS`, and PILOT/ANTIFRAUD/RESERVED vanish entirely on the Phase-3-closed build at :8770. The sections are DOM siblings, so express the ramp with `.ground--midnight + .ground{ --ground-prev:var(--mid-1); --th:96px; --th-mid:var(--th-ascent-mid); --th-end:var(--min-edge) }` and equivalents, so the threshold is derived from the actual neighbour and survives reordering and gating.

3. Recalibrate `--th` against measured rank padding at every breakpoint, not just 1440. Measured: `section--b` = 96/64/48px and `section--c` = 48/32/32px at 1440/768/390. Either bind `--th` to the rank token (`--th: min(96px, var(--rank-b-block))`) or publish a rank→threshold table; and extend the mobile override to `.th--fold`, which today keeps 48px against 32px of padding. As written the spec's own `test_v3_threshold_is_clear.py` fails on five of nine home sections.

4. Declare `--th-descent-mid`, `--th-ascent-mid` and `--th-fold-mid` in `:root` in §4.3, with the `@supports` non-oklab literal fallbacks promised in §4.2. As pasted, all three threshold ramps collapse to `transparent` at the mid stop.

5. Move the `prefers-contrast: more` kill-switch off `:root` and onto the ground elements (`@media (prefers-contrast:more){ .ground{ --grat-ink:transparent; --grain-amount:0; --lume:transparent } }`), because `.ground--midnight`/`.ground--utility` re-declare those properties on the element and an element-level declaration beats an inherited one. Today the guard silently does nothing on the dark chapters.

6. Write §4.7 as CSS. Name the interactive-sheet selector, and give hover/active a change that clears the spec's own §1.1 discrimination floor plus a non-colour companion (border, the `--contact` relief, or a 1px `--accent-ring` inline edge) — 1.03:1 and 1.06:1 are not states. Add the `:focus-within` equivalent for the sheet, not only the ring on the inner control.

7. Resolve the motion-system breaches in writing: define the duration `soglia-marea` uses (either reuse `--motion-draw: 900ms` or add a token and amend §MOTION), and cap the immersive trace at one per page rather than the five §8 risk 5 permits. Also verify, rather than assert, that the four landing pages and the forum have their single ambient loop free before allocating `graticola-deriva` to them.

8. Either specify `--lume` on midnight as a neutral cool white at low alpha, or obtain an explicit amendment to DESIGN_SYSTEM_V2 §1.3 for spending `--accent-dark` as ambient light. As it stands the spec dilutes the one signal that means 'interactive'.

9. Rewrite §4.6 with markup or delete it. It is the section that answers the owner's imagery complaint and it currently has no element, no selector, and no CSP-legal path for a per-section image URL under `style-src 'self'`. Specify `<picture>`/`<img class="ground__plate" alt="">` inside `.ground` with `object-fit: cover`, the vignette and grain as the existing pseudo-elements above it, the srcset breakpoints, and the alt/ARIA policy against `apps/cms/forbidden.py`.

10. Correct `templates/portal/partials/portal_chrome.html` — it does not exist (the directory holds access_point.html, card.html, case_header.html, deadline_item.html, next_action.html) — and name the real selectors for the context bar, rail, canvas and sheets. The platform application of the whole system currently rests on one row pointing at a missing file.

11. Keep a separator where the spec removes the hairline and supplies no threshold: `_antifraud` and `_reserved` (and any paper→paper tail). Today they carry a real 1px #d3d2cc rule; after the change they have nothing. Also drop `.ground--paper` from `_reserved`, whose `padding-block-start` is 0 and whose content sits inside an opaque `#f4f3f0` panel, so the material never shows.

12. Either fix `.forum-cta { background: var(--forum-navy) }` (`apps/forum/static/forum/forum.css:141`, `templates/forum/partials/cta_row.html:8`) in §4.5, or drop the §8 risk 6 test — as written the spec diagnoses the violation in §1.6, proposes a test that fails on it, and never repairs it.

13. Reconcile the midnight-chapter count: hero + pilot + the `--mid-0` footer is three dark grounds by the exact method §1.6 uses to convict the forum. State in writing whether the utility footer counts, and make the proposed test agree.

14. Remove the dead `mask-mode: alpha` (the `mask:` shorthand resets it) and put the mode after the shorthand, so §4.4's verification and the HUMAN_QA fallback actually describe the shipped behaviour.

15. Reconcile §7 with §5: either `graticola-deriva` is dropped, or §7 stops claiming 'nessuno promosso' and re-measures with the loop running on a real landing page, including the raster cost of a full-section masked layer. And budget the JS honestly — the pause mechanism is hero-scoped in `home.js:56-72`, so the four landing pages need a new observer, a new entry point and a new labelled control, not '< 700 B'.

