# REVISIONE INDIPENDENTE — hero-doorway

Round 1 · premium_lift **5/10** · conforme: **NO** · implementabile: **NO**

> The §1 audit is the best thing in this document and I could not break it: I recomputed every contrast figure (12.19 / 7.65 / 6.07 / 7.72 / 3.13 / 1.76 / 6.86 / 4.63 / 3.05 / 1.44 / 1.19 / 1.81 / 4.25) and every one matches to the second decimal, the station bounding boxes match fr_1440.json exactly, and "no new chunk" is true (home.js:18 already imports animate, scroll, stagger, withMotion). Then §4 collapses: the field inherits the 5fr column (503px at 1440, proved by the audit's own title w=704.7 against a 7fr/5fr grid with --s-8 gap), so the doorway silently shrinks 380→341px and the four labels at max-inline-size:22ch (~170px) must fit into 81px margins — the exact §1.4 sin, re-committed; `.field__caption{inset:0;z-index:4}` has no pointer-events:none and kills §8.4's doorway hover; the draw-on is physically impossible on three of four paths because they carry decorative stroke-dasharray; the spine at z-index 3 paints a 2px cyan line straight across the owner's key; and the sill lands at 69.4% where the threshold is at 74.16%. It also quietly breaks the binding documents it invokes: it indicts the code for not executing §8.3's six actor nodes, then ships four and drops "autorità competente" without an amendment, imports a 90ms GSAP stagger over the motion system's 40–60ms band, and puts bronze on a trajectory. Worst of all for the brief that produced it: the owner said the hero is "not speaking enough" and there are "not enough elegant modern coherent images", and this spec answers with roman numerals, mono caps, CAD dash patterns and a chart legend — every new element is a ≤2px stroke — while leaving the one image in the hero, the owner's photograph at opacity .50 behind a vignette, explicitly "§ 8.4 invariato".

## Violazioni dei vincoli non negoziabili

1. ONE interactive accent (--accent #0F6A72 / --accent-dark #7FD1D8, 'nothing else may use it', v2/tokens.css) — §4.4 defines `--terr-persona: #9fe3e8`, the same cyan hue at HIGHER luminance than the accent (12.19:1 vs 10.01:1 on --mid-1), drawn 2px wide from the bottom of the hero to the top, immediately beside the CTA that renders in rgb(127,209,216). Functionally a second accent.

2. Bronze --seal-600 for seals only — §4.4 `--terr-istituzione: #c7a77e = --seal-300` used as the INSTITUTIONS trajectory stroke plus a bronze ring at J. §9.3 grants bronze to an authority glyph ring inside the process list, not to a hero trajectory. The spec registers this only as Risk 6 ('Da scrivere nel sistema'), not as a formal amendment — unlike the §8.4 amendment it does file in §5.

3. Motion system durations/staggers (MOTION_SYSTEM §1: a signature hero animation may chain durations 'con ritardi scaglionati di 40–60 ms per riga, ma non inventa una durata') — §5 `hero.field.approach` uses stagger 90 ms, `hero.field.nodes` a 0.72 s delay, `hero.threshold.crossing` a 600 ms delay. §2 row 2 knowingly accepts '80–90 ms' from a GSAP result ('ACCETTATI i valori') over the binding document, with no amendment declared.

4. DESIGN_SYSTEM_V2 §8.3, binding — prescribes 'i nodi degli attori … (persona · organismo di formazione · università · autorità competente · impresa · istituzione)' and 'la rotta a sei stazioni'. §4.1/§4.3 ship four trajectories, merge 'organismo di formazione' with 'università' and drop 'autorità competente' entirely, and delete the six stations. §1.1 indicts the code for not executing §8.3; §4 then does not execute it either, with no amendment filed.

5. DESIGN_SYSTEM_V2 §8.3, binding — 'Capitolo --mid-1 … ≤ 110 % del viewport a 390' and 'Mobile: porta prima, intera, 220 px … CTA in vista'. §4.7 puts a portrait field (aspect-ratio 420/620 → 528px tall at a ~358px content width) FIRST, above the copy, plus a legend grid, eyebrow, 52px two-line title, lead, body and two 44px CTAs: ≈1200px against a 928px budget. The audit's own `heroBelowFold = 0` becomes a regression, and §4.7's '180 px a 390' is arithmetically impossible (42.86% of 358 = 153px).

6. --motion-ambient is 28s in static/css/v2/tokens.css; §5 `hero.field.tide` specifies 24 s with no token change and no note. MOTION_SYSTEM §1: 'Nessun altro numero.'

## Lacune (ciò che l'implementatore dovrebbe inventare)

1. The `d` attribute of all four trajectories in both geometries: curve family, control points, tension, tangent continuity at the shared node Nf.

2. --lx / --ly for items II, III, IV in landscape, and all four in portrait; plus the mechanism by which territory.py writes CSS custom properties into a hand-authored stylesheet without clobbering it.

3. The exact split of geometry between field__paths and field__spine, and the handoff between hero.threshold.crossing and hero.spine.progress on the shared strokeDashoffset/stroke-dasharray.

4. Portrait geometry beyond the door box and four entry points: node positions, confluence path shape, label anchors, the 'stessa topologia, ventaglio piu stretto' is not a specification.

5. Where the five node captions («orientation», «formation», «préparation», «besoin», «coopération») live in the DOM — SVG <text> (inside aria-hidden) or HTML (no element given).

6. The rest-state stroke-dasharray/strokeDashoffset of .field__path in CSS, and what the page looks like between first paint and JS execution (no-JS and slow-JS settled state).

7. --dir is used by hero.field.labels but defined nowhere.

8. The reveal mechanism that lets a dashed path draw itself (clipPath? mask? lead path?) and its markup.

9. The mask or z-order that makes trajectory I actually pass behind the doorway.

10. The overscan width of the contour layers needed to survive +/-26px travel.

11. The four new `field__role` msgids and the long figcaption msgid x 4 languages — ~20 new catalogue entries, absent from §7's cost and from the §4.5 claim 'nessuna traduzione nuova'.

12. Whether the modified opacities (.terr__layer--1/2, .terr__grid, .doorway__steps span) are edited in v2/hero.css or overridden from v3/hero-doorway.css, and at what specificity.

13. The restated `sizes` attribute for the doorway photograph under the new percentage-based doorway.

14. How the page-level budget in MOTION_SYSTEM §4 ('un oggetto indicizzato allo scroll' per PAGE) is met, given that the home page also carries §8.6's scroll-linked process route — the proposed §8.4 amendment only swaps the hero's photo parallax and leaves the page at two.

15. Which token family the four actor colours belong to: --owner-* and --route-* already map these actors; the spec invents a third parallel family without reconciling them.

## Segnali di «cheap / generico / default»

1. Roman numerals I-IV + uppercase mono micro-labels + 1.25px teal hairlines on midnight is the single most reproduced 'premium institutional / AI-made' idiom of 2024-2026. It reads as a template even when the content is good.

2. Worse, it is a SECOND set of four roman-numbered items on the same page as §8.5 'Le quattro vie' (which already uses 'indice serif' and --route-n). The reader is invited to map hero I-IV onto the wrong four things.

3. The `<ol class="field__legend">` with swatch + name + role is a chart legend. Nothing looks less like a hero and more like a dashboard widget.

4. Differentiating four actors by stroke-dasharray (1.5 5 / 10 6 / 12 5 2 5) is CAD / engineering-drawing language. It is correct for accessibility and wrong for 'authoritative but spectacular with measure' — the spec conflates two different axes and lets the a11y answer decide the aesthetic one.

5. Ten-to-twelve small circles with rings converging on a hub IS the 'SaaS integrations diagram'. Risk 1's guard (no radial symmetry, no pulsing halo) does not change the read: asymmetry does not stop a node graph from looking like a node graph. The spec names the risk and then ships the thing.

6. A ghost path at 22% opacity under the real path is the default 'muted twin' trick lifted from precisely the two animated-beam components §3 rejected.

7. ZERO MATERIAL. Every new element is a 1.25-2px stroke, a 3.5-10px circle or a <=13px text run. No light, no depth, no surface, no texture, no photography, no scale contrast. Against the owner's 'NOT: simple, editorial, severe, flat', a thin-line schematic with mono captions is arguably MORE severe and MORE flat than the wallpaper it replaces.

8. The motion dies after ~3 seconds. approach (900ms x4, 90ms stagger) + nodes + labels + crossing all fire once at load; after that the hero is a static diagram plus a 1.08 px/s tide. Risk 8 admits this. 'Not dynamic enough' is not answered by a one-shot entrance.

9. The hero would carry no image gain at all while the sister spec imagery.md presumably carries the image work — so on the owner's own named surface ('the hero is not speaking enough'), the deliverable is more text and more lines.

## MUST-FIX

1. GEOMETRY DEAD ON ARRIVAL AT 1440. `.hero__field` replaces `.hero__side` and therefore inherits `grid-template-columns: minmax(0,7fr) minmax(0,5fr)` with `gap: var(--s-8)` (hero.css:98-99) = 503.3px at 1440 (confirmed by the audit's own title w=704.7). `.doorway { inline-size: 67.86% }` renders the brand's signature object at 341px, not the 380px §8.4 and fr_1440.json both record — an undeclared 10% shrink. Side margins are (503.3-341.5)/2 = 80.9px; `.field__item { max-inline-size: 22ch }` at 13px mono needs ~170px. The four labels cannot fit beside the door. Fix: give the field its own full-bleed layer (viewBox 1440x820, like the contour SVGs) instead of the 5fr column, or cut the labels to <=10ch and move the roles under the figure — and restate the doorway width so it stays 380px.

2. `.field__caption { position:absolute; inset:0; z-index:4 }` (§4.6) has no `pointer-events: none`. It covers `.doorway` (z-index 2) and kills `.doorway:hover { transform: translateY(-4px) }` (hero.css:231) and §8.4's mandated 'hover: l'insieme sale 4 px, il primo gradino diventa oro'. The spec sets pointer-events:none only on `.hero__field > svg`.

3. THE DRAW-ON IS IMPOSSIBLE ON THREE OF FOUR PATHS. §5 `hero.field.approach` animates `strokeDashoffset 1->0` with `pathLength="1"` on `.field__path`, but §4.6 gives `.field__path--ii/--iii/--iv` decorative `stroke-dasharray` (1.5 5 / 10 6 / 12 5 2 5). One path cannot use stroke-dasharray for a pattern and for a trace at the same time — animating the offset on a dashed line produces marching ants, not a reveal. Specify a compatible mechanism (animated clipPath/mask on transform, or a solid lead path that draws then hands over) with the markup.

4. THE SPINE PAINTS OVER THE KEY. `.field__spine { z-index: 3 }` sits above `.doorway { z-index: 2 }`, and trajectory I runs T(280,460) -> R(280,48), i.e. the full height of the doorway interior: over the navy inner arch, over the owner's key, over the photograph. This contradicts §4.3's own 'dietro la porta' and defaces §8.4/BRAND_ASSETS §2. Put the spine below the doorway and start the visible segment at the crown, or give the clip mask geometry.

5. `field__paths` vs `field__spine` is never defined — which segments live in which file? And `hero.threshold.crossing` and `hero.spine.progress` both drive `strokeDashoffset` on `.field__spine`, with `hero.spine.progress` additionally rewriting `stroke-dasharray` to `.06 .94`. The two will fight; the handoff, the rest-state dasharray and the order of ownership are all missing.

6. `.doorway__sill { inset-block-start: 69.4% }` does not land on the threshold. Doorway box y 84->591 (507 units), T = y 460 -> (460-84)/507 = 74.16%. 69.4% puts the sill at y 435.9, 24 units above the threshold, on no declared landmark. (`inset-inline: 24%` is correct: it gives 181.2...378.8 = the inner arch 181->379.)

7. PATH DATA DOES NOT EXIST. §4.3 gives node lists joined by arrows. There is no `d`, no curve type, no control points, no tangent rule — and 'P0 -> Np -> C' can be drawn a hundred ways. The entire premium/cheap difference lives in those curves and the spec hands the decision to the implementer. Give the `d` strings, or the exact generator rule (curve family, tension, tangent continuity at Nf where II and III meet).

8. LABEL ANCHORS MISSING AND THE ONE GIVEN IS WRONG. Only `.field__item--i { --lx: 2.1%; --ly: 96.2% }` is supplied; it maps to (11.8, 673.4), which is neither P0(0,690) nor Np(92,676). `--ii/--iii/--iv` are 'valori emessi da territory.py', but the spec never says how a generator writes into a hand-authored `static/css/v3/hero-doorway.css` — one file, two authors, no mechanism. Emit them into a separate generated file and give all four pairs for both geometries.

9. COUNTS CONTRADICT EACH OTHER. §4.4 declares 'nodo di relazione (4)' while §4.3 names five (Np, Nu, Nf, Ni, Ns). §5 `hero.field.nodes` says '10 nodi' while §4.4's vocabulary totals 12 marks. Risk 2 says 'otto etichette' while §4.5's markup contains four `<li>`. And the five node captions («orientation», «formation», «préparation», «besoin», «coopération») have NO element anywhere in §4.5 — if they are drawn as SVG `<text>` they land inside `aria-hidden="true"` SVGs, which is exactly the 1.1.1 failure §1.7 indicts.

10. MOBILE BLOWS §8.3 AND HIDES THE CTAs. Portrait field (420/620) at ~358px content width = 528px tall, placed first, plus legend grid, eyebrow, 52px two-line title, lead, body, two 44px CTAs ~= 1200px against §8.3's 110%-of-844 = 928px budget. Today `heroBelowFold = 0`. Either shorten the portrait viewBox drastically, or keep the copy first and let the field follow.

11. THE HOVER PAYOFF IS BELOW PERCEPTION — the spec's own §1.5 charge. Ghosts go from rgba(63,166,175,.22) = 1.44:1 to .30 = 1.68:1 (I verified both). A 0.24 delta on a 1.25px stroke is invisible, and there is no keyboard, focus or touch equivalent, so on `hover: none` it never fires. Either make the reveal worth having and give it a `:focus-within` / toggle equivalent, or delete it.

12. GZIP FIGURE WRONG BY ~50%. §7 assumes 'i dati di path comprimono ~4:1'. Measured on the real files: templates/pages/home/partials/territory_hero_*.svg = 31,289 B -> 11,965 B gzip = 2.61:1. 22.4 KB at the real ratio is ~8.6 KB gzip, not 5.6 KB. The saving is real (11.7 -> 8.6 KB); the number in §7 is not.

13. FORBIDDEN WORDING GUARDED IN FR ONLY. §6.1 checks the French caption against forbidden.py. The exposure is the EN/IT rendering: 'franchit seule le seuil ... continue vers le nord' translates straight into the neighbourhood of the banned 'Cross the doorway to Italy'. Name `tests/compliance/test_public_pages.py` (it already runs forbidden.scan over every public route in every language) as the gate, and put a translator note on the msgid.

14. RTL REPRODUCES §1.8's OWN CONTRADICTION. Mirroring only the trajectories while leaving the contours unmirrored means that in /ar/ the person enters from the right — the side where the unmirrored northern relief (Veneto) sits — and the spine exits top-left, away from it. That is the same geography/composition break the spec convicts hero.css:567 of, moved one layer down. Either mirror nothing and author a second RTL geometry, or accept mirroring the terrain and rewrite territory.py's docstring claim.

15. `.field__item` is never reset at mobile. §4.7 sets `.field__caption { position: static }` but the `<li>`s keep `position:absolute; inset-inline-start: var(--lx)` and will stack on the nearest positioned ancestor instead of flowing into the two-column grid.

16. TIDE WILL TEAR THE EDGE AND CONTRADICTS ITS TOKEN. `--motion-ambient` is 28s; §5 says 24s with no token change. And +/-26px / -/+20px on contour layers the audit measures at exactly 1440px wide (x = -1.2 and 0.7) drags a 26px empty strip in from the edge — today's 12px is already at the limit. Specify the overscan (layer width 1440 + 2x max travel) or cut the travel. Also: '1,92 px/s' is the RELATIVE speed of two independent layers; no single object moves faster than 26px/24s = 1.08 px/s, so the perceptual gain over today's 0.43 px/s is 2.5x, not 4.5x.

17. THE PHOTOGRAPH'S `sizes` BECOMES WRONG. `sizes="(max-width: 47.999rem) 220px, (max-width: 63.999rem) 300px, 380px"` in _hero.html is written against px doorway widths. Making the doorway a percentage of the field changes every one of those numbers (380 -> ~341 at 1440) and the browser fetches the wrong srcset candidate. Restate `sizes`.

18. THE 'DETERMINISTIC PROJECTION' TAKEN FROM CANDIDATE 1 IS NEVER USED. §3 promises territory.py will project 33.97N/6.85W -> 45.41N/11.88E into the viewBox 'con la stessa aritmetica'. §4.3's numbers are hand-picked viewBox coordinates with no projection anywhere — the exact 'percentuali cucite a mano' sin charged to candidate 3. Write the projection or drop the claim.

19. ANSWER THE OWNER'S ACTUAL CHARGE ON THIS SURFACE. He said 'not enough elegant modern coherent IMAGES' and 'the hero is better but not speaking enough'. The one image in the hero is the owner's photograph at opacity .50 behind a --mid-1 vignette and a teal veil — see fr_1440_hero.png, where the arch reads as a grey smudge. §4 leaves it '§ 8.4 invariato' and proposes nothing. A hero spec that adds four 1.25px lines and leaves the only photograph invisible has not answered the verdict that commissioned it.

20. FORCED-COLORS RULE IS SELF-CONTRADICTORY. §4.6 says nodes and sill get `CanvasText` *with* `forced-color-adjust: none`. Those are mutually exclusive: forced-color-adjust:none opts the element OUT of the forced palette, so it keeps author colours, not CanvasText. Pick one, and prefer system colours + shape/dash differentiation over opting out.

