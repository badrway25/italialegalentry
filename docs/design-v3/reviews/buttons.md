# REVISIONE INDIPENDENTE — buttons

Round 1 · premium_lift **4/10** · conforme: **NO** · implementabile: **NO**

> The diagnosis is excellent and two of its ideas are genuinely worth shipping — moving the primary off `--brand-navy` onto `--accent` (one line, 61 template occurrences, fixes a real §1.3 r.1/r.4 violation) and making `:focus-visible` produce the hover state — but §4 does not deliver the button §4.1 describes, and I proved it in the browser rather than on paper. I appended the spec's own §4.2/§4.4 CSS to the served `main.css` at its stated cascade position and removed `hero.css:189-213` exactly as §4.6 instructs: the hero primary comes out `#0f6a72` at **2.77:1** against `--mid-1` and the hero secondary comes out near-white `--min-2` at 16.78:1, because the one rule that makes midnight work — `.chapter--dark .btn--primary, .hero .btn--primary, .platform-bar .btn--primary { … }` — is literally an ellipsis (`cta_SPEC.png` vs `cta_CURRENT.png`: the redesign looks *worse* than today on the owner's flagship surface). The refined fill is arithmetically wrong: `rgba(255,255,255,.055)` over `--accent` computes to `#1C727A`, not the `#106C75` in the table, giving **ΔL\* = 5.03** against a claimed 2.33 — the spec fails its own §8 risk-1 guard test (fail if ΔL\* > 3.5) on the first commit, and 4.62 on midnight against a claimed 2.73. Because v3's `.btn` lands after `components.css` at equal specificity it silently overrides `min-block-size`, `padding`, `border`, `letter-spacing` and (via the `font` shorthand) `font-size` on every variant §4.6 swears it does not touch — measured: `.btn--large` goes 44→48px, not the 56px `--btn-h-lg` promises, and by the same mechanism 12 `.btn--sm` jump 36→48px and 3 `.btn--upper` lose their `.06em` tracking, reviving on a locked prescribed text the exact unspaced-uppercase defect §1.10 condemns. Seven of ten variants have no CSS at all, `.btn--ghost` and `.btn--link` (8 uses, including a GDPR consent-withdrawal submit and every allauth link button) are never mentioned once, and `::after` is asked to be the press layer, the mooring line and the enlarged hit target simultaneously on the same element.

## Violazioni dei vincoli non negoziabili

1. MOTION_SYSTEM §1 ("Nessun altro numero" — four durations plus `--motion-ambient` ≥20 000 ms) and §4 ("un solo oggetto vivo per pagina … ≥ 20 s, in pausa fuori dal viewport"): §5 `button/busy-meter` invents **1200 ms in ciclo** and a **400 ms** stagger, neither of which is a system token. The spec declares the §4 waiver ("Eccezione dichiarata", blocking question 2) but never declares the §1 duration-token breach, and "paused off screen" is definitionally impossible for a busy indicator.

2. DESIGN_SYSTEM_V2 §2 ("quattro ruoli, e nessun quinto"; level 2 = `--shadow-2` **solo in hover**): §4.1 adds `--shadow-contact` as a fifth role AND §4.2 applies it permanently at rest via `.btn { box-shadow: var(--btn-inner,none), var(--shadow-contact) }`. Risk 2 honestly flags the fifth-role half as blocking; the "only on hover" half is not mentioned anywhere. Measured consequence: `sh=yes` on a `background-color: rgba(0,0,0,0)` hero secondary — a drop shadow under a transparent button.

3. DESIGN_SYSTEM_V2 §10 ("loading con spinner a tratto + testo"): §4.5 replaces it outright — «Il segnale d'attesa **non è uno spinner**: è il **misuratore a tacche**» — with no amendment requested, while two *other* amendments are listed as blocking. Undeclared deviation from a binding document.

4. DESIGN_SYSTEM_V2 §10 ("PRIMARY `--accent` pieno, testo `--min-0`"): §4.2 ships `--btn-ink: var(--min-2)`. Undeclared, and it is why §4.1's label ratios are quoted against `--min-2` rather than the prescribed `--min-0`.

5. Performance non-negotiable "no box-shadow animation": §4.2 animates `opacity` on `.btn::before` / `.btn::after` whose *entire* visual payload is a `box-shadow` (`--btn-inner-hover`, `--btn-inner-press`). The letter is respected, the paint cost is not — §7 admits this is "il rischio reale" and offers a `linear-gradient` fallback, i.e. the spec knows its own premium effect may not survive the budget it was written against.

## Lacune (ciò che l'implementatore dovrebbe inventare)

1. **The midnight rule is an ellipsis.** §4.2 ends `.chapter--dark .btn--primary, .hero .btn--primary, .platform-bar .btn--primary { … }` while §4.6 deletes `v2/hero.css:189-213`, the only rules that currently make midnight work. Measured in Chromium with exactly that edit applied: hero primary = `rgb(15,106,114)` at **2.77:1** vs `--mid-1` (§4.1 promises `#86D4DA→#79CDD4` at 10.01:1); hero secondary = `rgb(251,250,248)` at 16.78:1 (§4.1 promises `--mid-3` + `--btn-edge-dark`). Evidence: `cta_SPEC.png`, `rev_home_hero_stripped.png`.

2. **§4.1's colours and §4.2's CSS are two different buttons.** `rgba(255,255,255,.055)` composited over `--accent` = **#1C727A** (table says #106C75); bottom = **#0F656D** (table says #0E666D); **ΔL\* = 5.03** vs the claimed 2.33, i.e. an instant failure of §8 risk 1's own `ΔL* > 3.5` test. Midnight: #86D4DA/**#79C7CE**, ΔL\* = **4.62** vs 2.73. Label on the lightest band = **5.39:1**, not 5.88. (Every *flat* figure in the spec — 4.73, 3.68, 2.20, 9.55, 7.53, 8.51, 6.27, 5.89, 12.29, 15.56, 5.10, 1.26, 1.17 — recomputes exactly, so the author can do this; the gradient hexes were picked by hand and never reconciled with the alphas.)

3. **Seven of ten variants have no CSS**, despite §4.0 promising "gli esatti selettori CSS e il file": `.btn--tertiary`, `.btn--quiet`, `.btn--inline`, `.btn--sm`, `.btn--lg`, `.btn--block` and the whole `:disabled` / `[aria-disabled]` rule exist only as the single prose line 160 and the §4.3 table. `--surface-disabled`, `--btn-edge-dark`, `--accent-press` and `--err-press` are defined with correct computed ratios and then referenced by **no written rule at all**.

4. **`::after` is triple-booked.** §4.2 reserves `.btn::after` as the press layer; §5 `button/mooring-line` animates `scaleX` on "`::after` di 1 px" of `.btn--tertiary`/`.btn--inline`; §6 uses `::after` again to enlarge their hit target. One element has one `::after`. Worse, the §6 target-enlarging `::after` inherits `pointer-events: none` and `z-index: -1` from the base rule, so as written it cannot enlarge a hit target at all.

5. **No `transition` is declared anywhere in §4.2**, yet §5 specifies asymmetric in/out timings (`hover-surface` 180 ms in / 120 ms out, `press` 120 down / 180 up). The implementer must invent every transition declaration *and* the `@media (prefers-reduced-motion: no-preference)` wrapper that MOTION_SYSTEM §3 makes mandatory for every transition and keyframe — the spec's CSS block has no such wrapper.

6. **Cascade regression on variants the spec promises are untouched** ("122 occorrenze non si toccano"). v3's `.btn` is later than `components.css` at equal specificity, so it wins `min-block-size`, `padding-inline`, `border`, `border-radius`, `letter-spacing` and `font-size` (the `font` shorthand). Measured on `/fr/orientation/`: `.btn--large` 44 → **48px**, not the 56px `--btn-h-lg` implies, because no `.btn--lg` rule is written. Same mechanism: 12 `.btn--sm` go 36 → 48px (`--control-height-sm: 36px`), and 3 `.btn--upper` lose `letter-spacing: .06em` and `font-size: var(--font-size-label)`.

7. **`.btn--ghost` (4 uses) and `.btn--link` (4 uses) are never named once** — grep of the spec returns only a 21st.dev candidate description. `--btn-fill` and `--btn-ink` have no `var()` fallback, so both become 48px transparent boxes carrying a contact shadow, with `color` falling back to the inherited parent value.

8. **Focus halo hardcodes the wrong ground.** §4.4 writes `box-shadow: …, 0 0 0 2px var(--min-0)` and overrides only `.chapter--dark`; §4.2's selector list has three contexts and §4.2's prose has four (`.chapter--dark`, `.hero`, `.site-footer`, `.platform-bar`) — three different lists in three places. Measured grounds under `.btn`: `--mid-1` (hero), `--min-1`, `--min-0`, `--brand-navy` (forum). A focused hero button therefore gets a **15.77:1 white rectangle**; forum navy, 13.75:1.

9. **Internal contradiction on the case-file button.** §4.6 says `cases/detail.html:105` "non si tocca: `btn--quiet` ora esiste", but the same table and §4.5 list "cambio stato del fascicolo" among the five slow submits converted to `button_async.html`, which is `btn btn--primary` with face-swapping. The implementer cannot satisfy both, and §4.3 gives QUIET no loading and no error state.

10. **Evidence files do not exist and control counts are inflated.** `hero_actions.png`, `home390_full.png`, `reserved.png` are nowhere on disk (sibling specs put theirs in `docs/design-v3/audit/`). §7 claims "home 19, forum 9, orientamento 8"; measured `.btn` = **5 / 2 / 1**, all interactive controls = **10 / 6 / 5** — so the "38 riquadri" paint argument rests on numbers ~3× too high. Cited guard tests `tests/frontend/test_v2_tokens.py` and `test_motion_system.py` do not exist in the repo.

11. **`press` is not free.** Zero occurrences in `chunk-P4EHGXV4.js` — esbuild tree-shakes it today. An esbuild probe reproducing today's imports versus today's + `press` grows the shared chunk **23 133 → 23 861 B gzip (+728 B)**. §5's "costo marginale zero sulla libreria" is false; the real home total is ≈29.4 KB, not 28.6. The budget still holds (45 KB), so this is a wrong number, not a blown budget.

12. `.btn--icon { inline-size: 44px }` with `.btn { min-block-size: var(--btn-h) }` = 44×**48**, contradicting both §10 and the spec's own §6 ("44 su `.btn--icon`"). No `min-block-size` override is given.

13. `--btn-edge: color-mix(in oklab, var(--accent) 80%, black)` resolves to `oklab(0.383836 -0.056848 …)` — the spec never states its sRGB hex, so §4.1's "Riempimento/bordo vs fondo 5.53:1" is unverifiable and no `forced-colors`/fallback value is given for the one stroke that carries the "spessore della lastra".

14. `letter-spacing: .005em` computes to **0.075px** at 15px (measured). It cannot produce the claimed "aria fra le aste a peso 500".

## Segnali di «cheap / generico / default»

1. `inset 0 1px 0 rgba(255,255,255,.9)` on a near-white `--min-2` secondary plus a permanent `--shadow-contact` is the Bootstrap-3 / macOS-2009 bevel. Risk 3 admits it ("legge come un bottone macOS del 2009") and then ships it anyway with a hand-wave ("se in revisione legge «smusso» si scende a .6"). On a legal-institutional surface this is the single likeliest thing to read as cheap to the owner who rejected V2.

2. A contact shadow under **every** `.btn`, including transparent outline and ghost variants — measured `sh=yes` on a `rgba(0,0,0,0)` background. A drop shadow under nothing is the default-library tell, not a premium one.

3. The delivered hero CTA pair (`cta_SPEC.png`): a muddy dark-teal slab at 2.77:1 against the ground beside a stark white slab. Side by side with `cta_CURRENT.png` it is visibly *less* authoritative than the build the owner already rejected. Whatever else is argued, this is the image the owner will see first.

4. 48px flat height with a 2px radius on every variant because `.btn--sm`/`.btn--lg` were never written — one undifferentiated rectangle size across the whole product is precisely the "controllo di modulo di default" charge §1.4 levels at the current build.

5. The three-tick `btn__meter` is the one detail that could read as *this product* rather than a library — but its 1200 ms / 400 ms numbers are outside the motion system, and at three dots pulsing on `opacity` it is one CSS review away from being indistinguishable from the generic bouncing-dots spinner it was invented to avoid.

6. `color-mix(in oklab, …)` as the only edge colour, with no stated hex and no fallback, is a modern-CSS flourish that hides the actual value from review — and it is the value that carries the entire "lastra, non rettangolo" argument.

7. §4.6 assigning document deletion (`documents/index.html:54`, "Supprimer") to `.btn--tertiary` — the *lightest* variant, a coloured underlined text link — directly contradicts §4.2's own argument that a destructive action must not weigh less than an ordinary one, when `.btn--danger` exists and is the right answer.

## MUST-FIX

1. Write the midnight rule. Replace `.chapter--dark .btn--primary, .hero .btn--primary, .platform-bar .btn--primary { … }` with real declarations delivering §4.1's row (`--btn-fill: var(--accent-dark)`, `--btn-ink: var(--mid-1)`, `--btn-fill: var(--mid-3)` + `--btn-edge: var(--btn-edge-dark)` for the secondary), and reconcile the three divergent context lists in §4.2 selector, §4.2 prose and §4.4 into one. Without this, §4.6's deletion of `hero.css:189-213` ships a 2.77:1 primary and a white-slab secondary in the hero.

2. Reconcile §4.1's hexes with §4.2's alphas. Either publish the alphas that actually produce #106C75/#0E666D and #86D4DA/#79CDD4, or restate the table from `rgba(255,255,255,.055)`/`rgba(10,21,28,.055)` — currently ΔL* is 5.03 light / 4.62 midnight against claimed 2.33 / 2.73, so the §8 risk-1 test fails on commit one. Note the asymmetry: a white overlay moves a dark teal far more than an equal-alpha dark overlay does, so the two stops cannot share an alpha.

3. Add a `.btn` reset/guard for the variants the v3 base silently captures: write `.btn--sm { min-block-size: var(--btn-h-sm) }`, `.btn--lg { min-block-size: var(--btn-h-lg) }`, restore `.btn--upper`'s `letter-spacing` and `font-size` (otherwise §1.10's unspaced-uppercase defect returns on `access_point.html:23`, which carries a **locked prescribed text** `{% locked "p3.reserved.button" %}`), and give `--btn-fill`/`--btn-ink` `var()` fallbacks.

4. Define or explicitly retire `.btn--ghost` and `.btn--link` — 8 uses the spec never names, including `selection/disclosures.html:101` "Retirer cette autorisation" (GDPR consent withdrawal), `selection/process.html:225`, `portal/messages.html:31` (with its `aria-label`), and `templates/allauth/elements/button.html`, which maps the `link` tag for every allauth flow.

5. Resolve the `::after` triple booking on `.btn--tertiary`/`.btn--inline` (press layer vs mooring line vs hit target), and fix the §6 hit-target pseudo, which cannot work while it inherits `pointer-events: none` and `z-index: -1` from the base rule. Give the enlarged target its own element or move the press layer to `::before`-only for the frameless variants.

6. Write the `transition` declarations and wrap every transition and `@keyframes` in `@media (prefers-reduced-motion: no-preference)` as MOTION_SYSTEM §3 requires. As written the CSS has no transitions at all and no reduced-motion block, so §5's timings are unreachable and reduced motion is unimplemented.

7. Bring `button/busy-meter` onto system tokens or declare the §1 duration breach alongside the §4 one: 1200 ms and the 400 ms stagger are invented numbers, and MOTION_SYSTEM §1 says "Nessun altro numero". Also state what happens to "paused off screen", which a busy indicator cannot honour.

8. Declare the two undeclared DESIGN_SYSTEM_V2 §10 deviations (spinner → tick meter; PRIMARY ink `--min-0` → `--min-2`) in the same blocking-questions list that already carries the shadow-role and motion-loop amendments, and add the second half of the §2 breach: level 2 allows `--shadow-2` **only in hover**, while §4.2 puts a contact shadow at rest on every button including transparent ones.

9. Fix the focus halo: `0 0 0 2px var(--min-0)` is hardcoded but buttons sit on `--mid-1`, `--min-1`, `--min-0` and `--brand-navy` (measured). On the hero that is a 15.77:1 white rectangle around every focused control. Derive the halo from a `--btn-halo` set per context, or drop the halo and rely on `outline-offset` alone.

10. Resolve the `cases/detail.html:105` contradiction (`btn--quiet` untouched vs one of the five `button_async.html` submits) and re-assign document deletion from `.btn--tertiary` to `.btn--danger`, which the spec's own hierarchy argument demands.

11. Correct §7: `press` costs **+728 B gzip** on the shared chunk (measured by esbuild probe; zero occurrences in the current chunk), not zero; and the control counts are 5/2/1 `.btn` (10/6/5 controls) on home/forum/orientation, not 19/9/8. Produce and commit the three cited screenshots into `docs/design-v3/audit/`, and point risk 2/risk 6 at tests that exist — `tests/frontend/test_v2_tokens.py` and `test_motion_system.py` are not in the repo.

