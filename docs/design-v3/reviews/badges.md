# REVISIONE INDIPENDENTE — badges

Round 1 · premium_lift **6/10** · conforme: **NO** · implementabile: **NO**

> The central idea — a "vidimazione" with body, guide, glyph, word and a bronze seal register, plus an indicative register carrying zero colour — is the only spec-level answer in this council that invents a proprietary object instead of restyling a pill, and its contrast table is real: I recomputed all 25 figures in oklab and every one lands within 0.2 of the claim, always on the safe side. But it is not buildable as written and it is not compliant. The core rule, the single most important line in the document, is literally `.chip, .state, .badge { … }` (line 121); the glyph system never renders in phase 1 because `content:""` sits only on `.chip::before` while the register selectors are `.state--*::before`, so all 46 `.state` usages and 5 badge includes re-create E4, the exact defect the spec condemns; the seal's `clip-path: polygon()` and the seal-reveal's `clip-path: inset()` are the same property on the same element and do not interpolate, so the reveal erases the cut corner; and the stylesheet would never load, because base.html line 38 is a `<link rel="preload">` and the only stylesheet is `main.css`, whose `@import` list is never touched. Worse, it silently overturns a written legal ruling: `static/css/tokens.css:58-61` states "No green means 'approved'... this platform approves nothing" and makes `--state-done-fg` and `--state-info-fg` the same blue *on purpose* — E3 attacks that identity as a defect without ever citing the comment, §4.3 assigns green to `conforme`, and the mapping then paints `closed` ("Percorso concluso") green with a conformity check and `expired` red with an annulment bar, where `state--expired` is in fact the overdue counter at `case_header.html:59`. And the two details that actually carry the premium — 1.5/1.6px rotated-border glyphs and a bronze hatch-and-clipped-corner stamp — are the cheapest things in it, justified by a false claim that `icons.svg` lacks the symbols when it ships `icon-check`, `icon-warning`, `icon-info` and `icon-minus` already wired through `svg_icon` with `<use href>`.

## Violazioni dei vincoli non negoziabili

1. LEGAL/PRODUCT TRUTH — §4.3 table line 159 assigns `--ok-700 #1e7a4d` (green) to the `conforme` register, and §1 E3 (lines 26-30) attacks `--state-done-fg` == `--state-info-fg` as a defect. Verified in `static/css/tokens.css:58-61`: those two tokens are deliberately the same blue, under the comment "No green means 'approved'. A finished step is TRANSMIS or CLOS: a fact about the file, never a verdict. Same reasoning as the absent `eligible` outcome in the domain — this platform approves nothing." The spec never cites this comment; R3 (line 334) argues the risk away instead of escalating it. Reversing it is an owner/legal decision, not a design one.

2. LEGAL TRUTH — §4.2 mapping line 135 puts `closed` in the **conforme** register (green + conformity checkmark). `apps/cases/models.py` CaseStatus.CLOSED = "Percorso concluso", a fact about the file that may conclude without success; the codebase's own doctrine (tokens.css:59) says CLOS is "never a verdict".

3. LEGAL TRUTH — §4.2 mapping line 136 puts `expired` and `blocked` in the **rifiuto** register (red + annulment-bar glyph, §4.4 line 182). `templates/portal/partials/case_header.html:59` uses `state--expired` for the OVERDUE counter ("{{ n }} en retard"): an overdue deadline would render as an annulled act. ChecklistStatus.BLOCKED = "Bloccato" is a dependency state, not a refusal.

4. CSP (`style-src 'self'`, no `style=""`) — §5 line 262 `chip.state-swap` specifies `view-transition-name: chip-<pk>`. A per-primary-key value can only reach the element through an inline style attribute (blocked) or generated per-PK CSS; no mechanism is given. Cross-document View Transitions also require `@view-transition { navigation: auto }`, which the spec never mentions.

5. CSP — §4.6 line 224 reserves the counter width with `min-inline-size: calc(var(--digits, 2) * 1ch)` fed by `data-digits`, claiming "la stessa tecnica CSP-safe già usata da `.jurisdiction__segment[data-share]` (register.css:386)". Verified at `static/css/register.css:386-395`: that technique is *enumerated attribute selectors* (`[data-share="1"] { flex-grow: 1 }`), not an attribute→custom-property bridge. As written, `--digits` is never set by anything, so either an inline style (CSP violation) or unwritten `[data-digits="N"]` rules are required. The attribute is `data-digits`, the variable is `--digits`: nothing connects them.

6. MOTION SYSTEM §1 — §5 line 258 gives `chip.seal-reveal` a duration of **600ms**. `docs/design-v2/MOTION_SYSTEM.md:32-43` lists exactly four durations (120/180/240/320) plus `--motion-draw: 900ms` and `--motion-ambient`, and states "Nessun altro numero... non inventa una durata". No 600ms token exists in `static/css/v2/tokens.css`.

7. MOTION SYSTEM §2 — §5 line 258 declares `chip.seal-reveal` as "DELIZIA + GERARCHIA": two functions on one animation, where the rule is one. `MOTION_SYSTEM.md:68` lists nine families whose functions are gerarchia, orientamento, causalità, stato, feedback and profondità — DELIZIA is not among them.

8. MOTION SYSTEM §3 ("ogni `@keyframes` e ogni `transition` sta dentro `@media (prefers-reduced-motion: no-preference)`") — none of the CSS in §4.4, §4.5 or §4.7 is wrapped in that query; §4.7 line 233 writes hover as "180ms `--ease-out`" bare. The §5 table names the settled states but the CSS that must carry them is never shown.

## Lacune (ciò che l'implementatore dovrebbe inventare)

1. THE CORE RULE IS AN ELLIPSIS. §4.2 line 121 writes `.chip, .state, .badge { … }`. Everything the anatomy promises has to be invented: display/gap/padding, the three heights (20/24/30px), the 3px guide and its `--chip-gutter`, the 1px contour at 40% ink, `border-radius: var(--radius-control)`, the font stack and 13/16·600·0.06em tracking, and the defaults for `--m`, `--i`, `--chip-tint`, `--chip-ground`, `--chip-edge`, `--gutter-style`, `--gutter-w`.

2. THE GLYPHS DO NOT RENDER IN PHASE 1. §4.4 line 178 puts `content:""`, `inline-size`, `block-size`, `border-style` and `border-color:var(--m)` on `.chip::before` only. The register rules are `.state--filed::before`, `.state--missing::before`, `.state--valid::before` and set only `border-width`/size. A `.state` element is not a `.chip`, so it gets no `content` and therefore no pseudo-element at all — 46 `.state` usages and 5 `components/badge.html` includes get zero glyph, which is E4 restored and breaks §6's "canali non cromatici, sempre tre". §4.4 is also internally inconsistent with §4.2: it supplies `.state--*` twins for neutro/attesa/conforme and none for rifiuto or nullo, and none at all for any `.badge--*`.

3. SEAL REVEAL IS SELF-CANCELLING. §4.5 line 200 sets `clip-path: polygon(0 0, calc(100% - 7px) 0, 100% 7px, 100% 100%, 0 100%)` on `.chip--seal`; §5 line 258 animates `clip-path: inset(0 100% 0 0) → inset(0)` "sul guilloche". The guilloche is a `background-image` on that same element, not a separate node; one element carries one `clip-path`, and `polygon()` does not interpolate with `inset()`. No wrapper element, no `::before` reassignment, nothing.

4. THE STYLESHEET NEVER LOADS. §4 line 98 says chip.css is "caricato in `templates/base.html` dopo `css/v2/voyage.css` (riga 38)". Line 38 is `<link rel="preload" ... as="style">`; the only `<link rel="stylesheet">` is line 39, `main.css`, which `@import`s every layer in cascade order. `@import url("v3/chip.css");` must be appended to `static/css/main.css` after `v2/voyage.css` — the spec never says so, and a preload alone applies no styles.

5. `u-visually-hidden` (§6 line 278) does not exist. The utilities are `.visually-hidden` and `.sr-only` at `static/css/base.css:421-422`. The seal's hidden string is also never written down, so it can neither be checked against `apps/cms/forbidden.py` nor added to the four .po catalogues — same for the new visible suffix "— indicatif" (§4.6), which has no translation plan for IT/EN/AR.

6. `--chip-ground` IS ONLY DEFINED FOR MIDNIGHT. §4.3 line 167 redeclares it on `.section--verso`, `.plate--verso`, `[data-chapter="midnight"]`, but nothing ever switches it to `--min-1`, even though the contrast table has a dedicated "su `min-1`" column. `--min-0` (#f4f3f0, the page canvas per `v2/tokens.css:17`) is absent from the table entirely. Chips on a section ground or on the canvas will paint an 8% tint keyed to `--min-2` (#fbfaf8) and read as a mis-matched rectangle.

7. THE SEAL'S TOUCH TARGET EXPANDS NOTHING. §4.8 line 245 routes the 44px `::after` for an interactive seal onto "il `<span>` esterno del partial" — an outer `<span>` is not the `<a>`/`<button>`, so the enlarged area is not the target. No alternative (e.g. moving the seal edge to a third pseudo-element or a nested `<i>`) is given.

8. `chip.seal-reveal` HAS NO HOOK. The page rule (§5 line 264) "su una pagina che ha già il suo oggetto vivo i sigilli non si rivelano" is declared "CSS puro, 0 JS", but `templates/base.html:44` offers only `{% block body_class %}` — there is no `data-mode`/page-mode attribute to select on, and no selector is proposed.

9. PHASE 2's `register` ARGUMENT HAS NO SOURCE. The partial contract (§4.2 line 142) is `label · register · count · seal · indicative · size`, but nothing says how a template derives `register` from `{{ item.status }}` while keeping the promised "zero Python": no template filter, no model property, no mapping dict, no file. Likewise `data-digits` has no computation rule.

10. R6's GUARD DOES NOT DO WHAT IT SAYS. `scripts/css_class_audit.py` (read: its docstring) reports *template classes that no stylesheet defines* and fails above a ceiling; it cannot "fallire se `.badge--` ricompare". R7's test ("ogni valore di ogni `TextChoices` deve trovare un selettore in chip.css") is named but given no path, no module and no mechanism for reading CSS selectors from Python.

11. FACTUAL PREMISE OF §4.4 IS FALSE. Line 172 claims "`static/img/icons.svg` non contiene i simboli che servono". The sprite ships `icon-check`, `icon-warning`, `icon-info`, `icon-clock`, `icon-minus`, `icon-close`, `icon-shield`, `icon-lock`, and `apps/core/templatetags/ile_core.py:65-73` already injects them as `<svg><use href="…icons.svg#icon-X"></use></svg>` with `aria-hidden="true"` and `currentColor` — which is exactly what `.badge` does today. The `mask-image` argument is a strawman against a mechanism nobody proposed.

12. The deliverable is 339 lines; the brief caps the spec at 320.

## Segnali di «cheap / generico / default»

1. The five hand-drawn CSS glyphs at non-integer border widths (1.5px and 1.6px, §4.4). A rotated 1.6px right/bottom border is how a CSS tutorial draws a checkmark; at 1x DPR and at the 125%/150%/200% zooms the spec's own R4 demands, it anti-aliases into a grey smear with uneven arms. R4 worries about moiré in the guilloche and says nothing about the glyphs, which are the far more likely visible defect.

2. A SECOND ICON FAMILY on the same row as the first. The spec's own accepted guidance (§2 #7) is "una sola famiglia visiva per superficie", and then §4.4 invents a geometric border family that will sit in the same table cell as the sprite's stroked icons, with different weights and terminals. Two icon languages per row is the most reliable way to look unfinished.

3. The bronze + 58° diagonal hatch + clipped corner "sigillo" (§4.5) is the single most AI-generated "premium institutional" trope in circulation. `docs/design-v2/ANTI_PATTERNS.md:64` already bans "oro/giallo saturo, gradienti metallici... lusso di plastica", and R2 guards only the *quantity* of seals, never the trope itself. One bronze stamp with a hatch on a Django table reads as a stock certificate mockup, not as authority.

4. The indicative chip: dashed contour + dotted guide + synthetic-risk italic + a visible "— indicatif" suffix (§4.6). Four decorations stacked to rescue one meaning. R8 identifies the failure ("si legge come campo vuoto o segnaposto") and answers it by adding more decoration rather than by finding one strong non-colour signature.

5. `--m` and `--i` as custom property names (§4.2). Two-letter unnamespaced globals in a codebase with six stylesheet layers and a `_legacy-tokens.css` bridge; the first collision will be silent and undebuggable.

6. The register system is LESS differentiated than the spec's own indictment implies. Five registers for sixteen values means seven of eleven CaseStatus values (oriented, review_required, training, selection, admin_process, pre_departure, post_entry) collapse into one identical `neutro` pixel. E3's charge — "VALIDO e IN ESAME sono la stessa cosa" — is only half answered: EN EXAMEN and TRANSMIS remain byte-identical. Nothing in the proposal expresses progression through the eleven states, which is what a case-file dashboard is for.

7. `review_required` ("Verifica professionale necessaria") mapped to the passive **neutro** register, when it is one of the five CR-11 outcomes recorded in `docs/security/AUDIT_MODEL.md:418` and means action is required. `suspended` (which `Case.clean()` forces to carry a written `suspension_reason`) flattened into the same `attesa` register as `draft`.

8. §7's headline claim "**0 layout, 0 paint** in DevTools durante il movimento" is false as written: `chip.hover` transitions `background-color` (legitimate under the HOVER family, but it repaints), `chip.focus` transitions `outline-offset` (repaint), and `chip.count` rewrites a text node every frame. An owner who checks will find the one hard number in the performance section is wrong.

## MUST-FIX

1. Escalate the green question instead of deciding it. Quote `static/css/tokens.css:58-61` verbatim in §1, state that `conforme` in green reverses a written ruling, and either (a) keep the register's mark blue-neutral and carry conformity on glyph + guide style alone, or (b) obtain an explicit owner/legal sign-off recorded in the spec. Do not leave it as risk row R3.

2. Re-derive the mapping table from `apps/cases/models.py` meanings, not from string similarity. Minimum: `closed` out of `conforme`; `expired` and `blocked` out of `rifiuto`; `review_required` and `suspended` out of the passive registers. State the intended sense of every one of the 16 enum values next to its register, and add a sixth register for "action required" if the mapping needs it.

3. Write the `.chip, .state, .badge { … }` rule in full — every declaration, every default custom property — and write the phase-1 fallbacks so the pseudo-element actually exists on `.state` and `.badge`: put `content:""` and the shared geometry on `.chip::before, [class*="state--"]::before, [class*="badge--"]::before`, then enumerate `::before` register rules for ALL five registers across ALL three vocabularies, including `.badge--*`. Say explicitly what happens to the `{% svg_icon %}` already rendered inside `.badge`.

4. Replace the hand-drawn glyphs with the existing sprite (`icon-check`, `icon-warning`, `icon-info`, `icon-minus`, `icon-close`) via `{% svg_icon %}`/`<use href>` with `currentColor`, which is already CSP-clean, already `aria-hidden`, already one family, and survives forced-colors — or justify the geometric family against the sprite that actually exists, not against a mask-image strawman. If geometry is kept, move every border width to whole pixels and show the 125%/150%/200% rendering.

5. Fix the seal reveal: give the guilloche its own element (or move the polygon to a wrapper and the inset to the inner node), and replace the invented 600ms with `--motion-draw` or a new token defined in `v2/tokens.css` with a stated reason; declare exactly one MOTION_SYSTEM §2 family for it.

6. Delete `view-transition-name: chip-<pk>` or replace it with a CSP-legal mechanism (`view-transition-name: match-element`, or a bounded enumerated set), and add the `@view-transition { navigation: auto }` opt-in the cross-document transition needs.

7. Write the real `data-digits` bridge: enumerated `[data-digits="1"] { --digits: 1 }` … `[data-digits="4"]`, exactly as `register.css:386` does for `data-share`, and name what computes the attribute in the template.

8. Add `@import url("v3/chip.css");` to `static/css/main.css` after `v2/voyage.css` (and optionally the matching preload in base.html), and correct the false line-38 instruction.

9. Define `--chip-ground` for every ground the chip can land on — `--min-0`, `--min-1`, `--min-2`, `--min-3` and midnight — with the selectors that set it, and extend the contrast table to `--min-0`.

10. Write the seal's visually-hidden string, in FR/IT/EN/AR, with the correct class (`.visually-hidden`), plus the translation plan for "— indicatif"; confirm each against `apps/cms/forbidden.py`.

11. Give the seal's interactive variant a working 44px target (a third pseudo-element or a nested element), and state that `chip--s` at 20px is forbidden on any `a`/`button` chip so 2.5.8 holds on fine pointers.

12. Name the phase-2 `register` derivation concretely (template filter, model property or dict) and reconcile it with the "zero Python" claim; specify the page-mode hook `chip.seal-reveal` selects on, since `base.html:44` provides none.

13. Replace R6's and R7's guards with tests that can exist: name the file, the assertion, and how CSS selectors are read from Python. And cut the document to 320 lines.

