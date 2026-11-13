# REVISIONE INDIPENDENTE — person-dashboard

Round 1 · premium_lift **7/10** · conforme: **NO** · implementabile: **NO**

> Section 1 is the best audit in this council round — I re-ran every number and every one is true (docH 4296/4990/7994, case-header 117/257/417, `dataMode: null`, shadows 0, animations 0, `imgCount: 0`, 3 ground colours, `tabular: "normal"`, "Voir mes documents" at 138.45×18, `rgb(30,74,133)`, zero `sequence__crossing` in templates, `--pending-700` referenced nowhere outside its own declaration), and the plancia + RAIL 2.0 + frontier + owner textures + tick meter is a genuinely proprietary answer, not a template. Then the spec stops measuring exactly where it matters: it computes 14 contrast ratios and every one is correct to the second decimal, but it never computes the one set it actually depends on — the five `--owner-*` fills that carry state and responsibility on the midnight ground land at **1.89:1 to 3.33:1**, the default bar `--mid-3` on `--mid-2` at **1.15:1**, and the only edge of a `todo` bar at **2.19:1**, so the signature component fails WCAG 1.4.11 on its primary information channel. It also revives its own diagnosed defect — §1.3 condemns `#1E4A85` for "l'aspetto di un link: un secondo accento interattivo", then §4.3/§4.4 paint `.chip--current` and `.state--review` in `--accent` itself. The signature animation is dead on arrival: I confirmed in Chromium that `transform-origin: inline-start` (L190) is **dropped** — there is no logical keyword for that property — so `rail-trace` scales outward from the centre in both LTR and RTL. And the two things the owner actually named as weak come back generic: the badge is a shadcn Badge with ILE hex codes (pill, tinted fill, uppercase micro-label, 14px stroke icon) that discards the project's own archival `border-inline-start` filet, and the answer to "not enough elegant modern coherent images" is one generated texture at `opacity: .22`.

## Violazioni dei vincoli non negoziabili

1. **WCAG 2.2 AA (1.4.11 non-text contrast) — the rail's primary channel.** §4.6 L178 `[data-state="done"] .rail__bar{background-color:var(--seg)}` with L174-176 mapping `--seg` to the existing `--owner-*` tokens, on the `--mid-2` plancia: person #0f6a72 = **2.52:1**, project #34506a = **1.89:1**, training #1c5f7c = **2.25:1**, authority #8c6d4b = **3.33:1**, territory #2f6b5c = **2.56:1**. L177 default bar `background:var(--mid-3)` on `--mid-2` = **1.15:1**. L180 `[data-state="todo"]{background-color:transparent}` leaves only the L177 `1px solid var(--hairline-dark-strong)` edge, composited = #4a5961 = **2.19:1**. §4.3 L103 lists `--owner-*` under "Esistenti impiegati" and gives computed ratios for `--accent-dark`, `--on-dark`, `--on-dark-2`, `--on-dark-3` and `--terr-line` on `--mid-2` — and omits exactly the five that fail.

2. **DS §1.3.1 one interactive accent.** §4.4 L114 `.chip--current{--chip-fg:var(--accent);--chip-bg:var(--accent-100)}` plus L108 `border:1px solid currentColor` paints a NON-interactive badge in the colour reserved for links, primary CTA and focus, and §4.3 L103 sends `.state--review` (the "Nouveau" message marker) to `--accent` as well. DS §1.3.1: "Link, CTA primaria e anello di focus condividono --accent. Nessun titolo, icona o sfondo lo usa." This is the identical defect the spec itself indicts at §1.3 L19.

3. **`.on-dark` cascade silently destroys the error state.** §4.4 L119 `.on-dark .chip{--chip-fg:var(--on-dark-2);--chip-bg:transparent}` has specificity (0,2,0) and beats `.chip--overdue` (0,1,0) at L117. Inside the plancia every chip — done, todo, overdue, seal — renders identically in `--on-dark-2` with one hairline border, while §4.6 L199 specifies the blocked state as "chip `--overdue` + parola". On midnight the semantic foregrounds are unusable anyway (ok-800 2.44:1, err-700 2.43:1, pending-700 2.28:1, seal-700 2.11:1) and the spec neither says so nor defines dark-chapter variants.

4. **MOTION §1 "Nessun altro numero".** §5 L213 `rail-trace` at **720 ms**. The immersive trace is a single pinned token, `--motion-draw: 900ms` (static/css/v2/tokens.css). 720 ms is not a token and MOTION §1 states the compiled CSS is counted by test. Either declare a second trace token with its justification or use `--motion-draw`.

5. **Perf rule "no box-shadow animation".** §5 L218 `checklist-row-hover` lists `background-color` + `--shadow-2` under "Proprietà" with 180 ms in / 120 ms out. The hedge in the Budget column — "nessuna ombra animata **in loop**" — narrows a rule that has no loop qualifier. MOTION §2 also restricts animatable properties to `transform`, `opacity` and SVG `stroke-dashoffset`/`pathLength`. State the shadow as an untransitioned discrete swap or drop it.

6. **DS §4 spacing rhythm.** §4.4 L108 `gap:6px` and `padding-inline:10px`; §4.5 L142 meter notch `12×4 px, gap 3`. The scale is declared invariant at `--s-1` 4 · `--s-2` 8 · `--s-3` 12 …; 3, 6 and 10 px are off-grid and written raw rather than as tokens, as are ~20 other literals (13px, 17px, 22px, 12px) that already exist as `--t-folio`, `--t-body`, `--t-entry`, `--t-caption`.

## Lacune (ciò che l'implementatore dovrebbe inventare)

1. **`--rail-progress` has no declared source.** §4.6 L191 `transform:scaleX(var(--rail-progress,0))`; §5 L213 says it is "applicato subito" with reduced motion. Nothing says who writes it. The obvious implementation is `style="--rail-progress:.43"`, which `style-src 'self'` drops silently — the exact failure mode `templates/components/jurisdiction.html` documents in its own comment ("a style attribute would be silently dropped in production"). The spec even praises that `data-share` technique in §3 candidate 2 and then fails to apply it. Must state: JS via `setProperty`, or a `data-progress="n"` attribute with N enumerated CSS rules.

2. **`transform-origin: inline-start` (L190) is invalid CSS.** Verified in the bundled Chromium: the declaration is rejected (`setProperty` leaves the property empty) and the origin falls back to `50% 50%`. There is no logical keyword for `transform-origin` — `start` is rejected too. The signature trace will grow outward from its middle in FR *and* AR. Requires `transform-origin:left` with a `[dir="rtl"]{transform-origin:right}` override, which in turn contradicts §6's "Solo proprietà logiche".

3. **The rail panel content is literally `…`** (§4.6 L162 `<div class="rail__panel" id="rail-p1" role="region" …>…</div>`). Every keyboard and `aria-expanded` claim in §6 hangs on a disclosure whose payload is undefined. The only plausible source, `step.detail`, is optional in the current template (`{% if step.detail %}`), so segments without it get a button that expands an empty region.

4. **The owner WORD has no source.** `data-owner` is honestly derived from `step.owner_key|default:"indicative"` (L166) with a stated fallback, but `.rail__owner` renders "La personne" in the example and nothing says where that string comes from. `step.actor` is optional in the existing contract, and `data-owner`/`step.actor` can disagree.

5. **"Étape 3 sur 7" (L148) has no derivation.** The journey contract exposes `is_current` per step, not an index. Computing the current ordinal inside the template is doable but unspecified, and it is the headline fix for §1.2.

6. **`<li class="rail__frontier">` (L158) is a non-step item inside the `<ol>` of steps.** A screen reader will announce 8 list items while the visible text says "3 sur 7". No `role="presentation"`/`role="separator"` guidance is given.

7. **The markup ships `aria-expanded="false"` hard-coded (L152, L160) while §6 L227 promises "Senza JavaScript tutti i pannelli sono aperti".** Without JS the page then lies to assistive technology. The template must render `true` and JS must flip it, or the disclosure must be a `<details>`.

8. **`min-block-size:96px` (L182) does not fit its own content.** At the lg container (1176) minus 6 `--s-2` gaps, a segment is ≈161px wide. It must hold bar 10 + num 16 + 20px glyph + a 17/24 serif label that wraps to 2–3 lines (48–72) + a 24px chip + a 16px owner line + 5 gaps ≈ **175–200px**. The grid will auto-grow, so nothing breaks — but §7's whole height budget ("1440 → ≈ 2 480 px") rests on the 96 figure, and unlike the checklist card (which gets `-webkit-line-clamp:3`) `rail__label` gets no truncation rule.

9. **§7's numbers are asserted, not measured.** Every figure in §1 is a real measurement; every figure in §7 ("≈ 2 480", "≈ 3 050", "≈ 4 100", "≈ 168", "≈ 136 px", "−57 %", "sposta ≈ 1 584 px") has no derivation. Given the rail-height error above, at least one is wrong by ~2×.

10. **`base_portal.html` is shared by every role, and the spec only designs the PERSONNE case.** §4.2 L91 adds `data-mode` and a `portal_inspector` block to `base_portal.html`, and the workspace grid is `224 / 1fr / 320`. Nothing says what company/institution/university/professional dashboards (the `cards and not is_person` bridge grid) or a signed-in user **with no case at all** get: today `case_header.html` is rendered only `{% if case %}`. Without a branch the plancia disappears and the 3-column grid has an empty third column.

11. **The no-case branch destroys a locked prescribed text.** Today, a user without a case gets `page_header` built from `{% locked "p3.reserved.title" %}` + `p3.reserved.body`. §4.1 L79 puts "H1 «Tableau de bord»" inside the plancia with no alternative branch. Locked prescribed texts are on the untouchable list.

12. **`--accent-100 #DCEAEB` (L99) is a redundant token.** The system already ships `--accent-wash: #d9eef0` (v2/tokens.css L47), 3/4/5 RGB units away, which gives `--accent` at **5.24:1** — better than the new token's 5.12. A new token that is a slightly worse copy of an existing one is exactly the drift the DS's "prove" column exists to stop.

13. **`main.css` @imports vs the preload list.** §4.2 L90 adds five files to `static/css/main.css`. `templates/base.html` L25-38 preloads every existing layer individually with the comment "preloading these removes the request chain (LCP render delay)". Five un-preloaded `@import`s re-create that chain. Unaddressed.

14. **`-webkit-line-clamp:3` (§4.7 L203) needs `display:-webkit-box; -webkit-box-orient:vertical; overflow:hidden`** (or the modern `line-clamp` + `display:-webkit-box`). Given alone it does nothing.

15. **`.plancia__plate` is specified both as a class carrying `position:absolute; object-fit:cover` (L135-136) and as `<picture>` with `sizes` (L140).** The wrapper, not the `<img>`, is the positioned box; which element takes the class is unstated.

16. **`static/img/v3/` does not exist and no build step is wired.** `scripts/territory.py` does exist, but nothing says how `territory-plate-{640,1280,1920}.{avif,webp}` gets generated, committed or regenerated.

17. **Cross-spec collision on the one living object.** §5 L219 claims `inspector-lift` is "l'unico oggetto indicizzato allo scroll della pagina", and §7 L243 reserves `backdrop-filter` for "l'header scrollato". The platform shell that also renders on this page has its own scrolled-header behaviour. MOTION §4 allows RICH exactly one. Unreconciled.

## Segnali di «cheap / generico / default»

1. **The chip is a shadcn Badge with ILE hex codes.** §4.4: `display:inline-flex; gap; border-radius:999px; border:1px solid currentColor; background: tinted; 13px uppercase .06em; 14px 1.5-stroke icon`. That is the default-library badge, feature for feature, and badges are one of the things the owner named as still weak. §3 candidate 8 (`coss-badge`) is rejected as "Base UI + CVA per una pillola CSS" — but the pillola drawn is the same object. The per-variant glyph is the only proprietary move, and on the plancia even that is all that survives (L119).

2. **It throws away the one distinctive device the product already has.** §1.3 correctly says `.state` is not a pill — but the `border-inline-start: 2px solid currentcolor` filet reads as a register/archive mark and is specific to this project. It is replaced by a generic pill with nothing of the folio, the mono reference, the seal or the hairline grammar in it.

3. **One decorative texture at `opacity:.22` is the answer to "not enough elegant modern coherent IMAGES".** §4.5 L136/L140: a single generated abstract plate, 22% opacity, behind the header, `alt=""`. Correct and safe — and it will not read as "more images" to the person who wrote that sentence. `imgCount` goes from 0 to 1, and the 1 is invisible.

4. **Hover craft is `rgba(214,226,228,.05)`.** §4.6 L199. A 5% white wash is the default-dashboard hover. Nothing in the rail's rest→hover→focus sequence carries the cartographic grammar the rest of the spec builds.

5. **"Sticky inspector + four-fact `<dl>` + segmented progress bar" is standard SaaS furniture.** The plancia and the RAIL 2.0 are the only genuinely proprietary inventions; the other ~60% of §4.7 is the layout any competent dashboard gets by default, and the spec spends more words defending it than distinguishing it.

6. **The graticola is two `repeating-linear-gradient`s at `.055` alpha** (L130-132). At 160px step and 5.5% alpha over `--mid-2`, this is a hairline grid that will read as "slightly noisy dark box", which is close to the owner's exact complaint that backgrounds are "too simple or unmemorable". §8.1's defence ("uno screenshot in scala di grigi deve restare leggibile") protects legibility, not memorability.

7. **§8 risk 1 contradicts §4.5.** It promises "l'unico colore saturo è --accent-dark su **un** elemento («Vous êtes ici»)" while L137 also paints `.plancia__ref` in `--accent-dark` at 22px and L188 the `.rail__here`. Three, not one — and the self-imposed discipline that was supposed to keep it off fintech territory is not actually enforced.

## MUST-FIX

1. Compute and fix the rail bar contrast. `--owner-*` on `--mid-2` measures 1.89–3.33:1 and `--mid-3` on `--mid-2` measures 1.15:1 — below WCAG 1.4.11. Either define a dark-chapter owner ramp (`--owner-*-dark`) with published ratios ≥ 3:1 against `--mid-2`, or move the rail to the paper chapter. Publish the ratios in the §4.3 table like every other token.

2. Remove `--accent` from every non-interactive element. `.chip--current` (L114) and `.state--review` (L103) must not use the one interactive accent. Give the current state the accent as a *form* only (the 2px `--accent-dark` frame on the bar, which DS §9.3 already prescribes) and give the chip a neutral or `--terr-line-lt` treatment plus its glyph.

3. Replace `transform-origin: inline-start` (L190) — verified dropped by Chromium, origin falls back to centre. Use `transform-origin: left` with an explicit `[dir="rtl"] .rail__trace{transform-origin:right}` and say in §6 that this is the one permitted physical-property exception, since no logical keyword exists.

4. Declare how `--rail-progress` reaches the element, CSP-safely. Follow the documented `data-share` pattern in `templates/components/jurisdiction.html`, or state that `dashboard.js` sets it via `setProperty` and that without JS the trace stays at 0 (which is acceptable but must be written).

5. Fix the `.on-dark .chip` cascade (L119) so that `--overdue` and `--seal` survive on the plancia, or state plainly that inside the midnight chapter state is carried by glyph + word only, and update §4.6 L199 accordingly. As written, §4.4 and §4.6 contradict each other on the blocked state.

6. Write the branch for a dashboard **without a case** and for the non-PERSONNE roles that share `base_portal.html`. Name where `{% locked "p3.reserved.title" %}` / `p3.reserved.body` go, and what the 224/1fr/320 grid does when there is no inspector content.

7. Account for every fact the current screens carry, explicitly. `case.suspension_reason` + the "Dossier suspendu" notice; the `Responsable` fallback sentence "Vous — aucun intervenant n'est assigné à ce dossier" (it is in the measured band text); the `portal-notices` "Avis de l'équipe" region; `assessment.rationale`, `ruleset_version`, `assessed_at`, `missing_count` and the "Voir le détail de la pré-évaluation" link. None of these appear anywhere in §4.

8. Do not put legal sources behind a disclosure. §4.7 L205 reduces FONDEMENTS to 3 with "Voir les 6 fondements" in a `<details>`. The Fondements are the legal basis of a pre-assessment; §8 risk 6 protects the disclaimer sentence and leaves the sources unprotected. Either keep all sources visible or move the pré-évaluation block out of the 320px inspector.

9. Quote the two prescribed sentences verbatim and say which goes where. §4.7 says "la frase di disclaimer sempre presente" without naming it; there are two distinct locked strings in play (DS §9.7's "Prochaines étapes à caractère informatif…" and the template's "Cette pré-évaluation ne s'appuie sur aucune règle actuellement en vigueur… Elle reste une orientation, jamais une décision.").

10. Correct §4.7 L202: `templates/portal/partials/next_action.html` **does** render `<a class="btn btn--primary btn--arrow">` when `action.url` is set. "oggi non c'è alcun bottone" is true of the seeded case only. An implementer reading it literally will add a second CTA.

11. Fix the motion entries: `rail-trace` to `--motion-draw` (900 ms) or declare a second trace token with justification, and restate `checklist-row-hover` so `--shadow-2` is a discrete swap, not an animated property.

12. Re-measure §7 after fixing the rail segment height. 96px cannot hold bar + number + glyph + a wrapping 17/24 serif label + chip + owner line at a ~161px column; give `rail__label` a clamp rule and rebuild the height table from the corrected figure.

13. Delete `--accent-100` and use the existing `--accent-wash #d9eef0` (5.24:1 with `--accent`, better than the proposed 5.12). Put the raw literals (`gap:6px`, `padding-inline:10px`, `gap:3px`, 13/17/22/12px) onto the existing space and type tokens.

14. Add the five `v3/` files to the preload list in `templates/base.html` (L25-38) or say why the request chain is acceptable, and specify the build step that produces `static/img/v3/territory-plate-*` from `scripts/territory.py`.

15. Give the badge something that is not a shadcn pill. The owner named badges as weak; a tinted rounded-full chip with a stroke icon is the default answer. Carry the register grammar into it — the mono reference face, the hairline rule, the seal for authority — so it reads as this product and not as a component library.

