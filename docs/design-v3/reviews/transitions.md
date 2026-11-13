# REVISIONE INDIPENDENTE — transitions

Round 1 · premium_lift **4/10** · conforme: **NO** · implementabile: **NO**

> This is the best-audited spec I have read on this council and the weakest answer to the brief. Section 1 is genuinely excellent forensics — htmx absent, focus on BODY, zero live regions, a progress bar animating inline-size in navy #0F2547, 21 dead .wizard__progress-fill--* classes, tabs/accordion/stepper as dead code — all four claims I spot-checked are true. But the owner did not say "our transitions are technically incorrect"; he said the result is not premium, not dynamic, not wow. What this spec proposes to build is a 2px teal underline that slides under tabs, a 12px fade-slide panel swap at 120/240ms, a height transition on details, and an 8px translateY page crossfade. That is the literal default of every shadcn/Framer tutorial on the internet, and §8.7 concedes the point by budgeting for three screen recordings to prove the owner can see a difference at all — a spec that has to be filmed to be noticed has already lost the argument. Worse, it is not buildable as written: §4.2 says initTabs() "resta l'unica fonte di verità" while §7 deletes it; §4.3 is titled "zero JavaScript" and then specifies a JS-timed 60ms open delay and a post-transition scrollIntoView; §4.4 deletes the role=progressbar element while citing its aria-valuetext as the guarantee that the rail does not lie; and the exit animation cannot run because the panel it animates has already been set hidden in the same frame by the rule §4.2 declares non-negotiable.

## Violazioni dei vincoli non negoziabili

1. CSP style-src 'self' / no style="" attributes — §4.7 line 181: «Ogni riga di una tabella ordinabile porta view-transition-name: ile-row-{{ item.pk }}». A per-row CSS property interpolated from a Django template has exactly one obvious implementation, style="view-transition-name: …", which the project's own test forbids (apps/orientation/tests/test_compliance.py:126 asserts 'style="' not in the fragment). The spec carefully justified CSSOM setProperty for --mark-x in §4.2 line 103 and then says nothing at all here. No attr()/match-element fallback is named.

2. WCAG 2.2 AA contrast + the brief's rule that new tokens carry computed ratios — §4.1 line 77: «--swap-veil: 0.62; /* velo del form in attesa: ink 17px su min-0 a .62 → 6,9:1, sopra AA */». The number is fabricated. --ink #15222A composited at 0.62 over --min-0 #F4F3F0 gives L=0.1625 → 4.45:1, which FAILS 4.5:1 for the 17px <legend> question text. The .wizard__label choices in --ink-2 #4A5A62 come out at 2.79:1. The veiled <fieldset> (templates/orientation/_step.html) contains the legal question text itself, not only inactive controls, so the WCAG 1.4.3 inactive-component exemption does not cover it.

3. WCAG 2.2 AA visible focus — §4.2 line 96 «.tabs__viewport { position: relative; contain: layout paint; }» and §4.3 line 127 «.accordion__item { contain: layout paint; }». The project focus ring is static/css/base.css:384-389: outline + outline-offset + box-shadow 0 0 0 <offset> halo. contain: paint clips both the outline offset and the halo at the container edge, so a focused tabpanel (tabs.html:13 carries tabindex="0") and a focused <summary> lose their visible indicator on the clipped edges. The spec asserts «Visible focus» in §6 without noticing it destroyed it in §4.

4. MOTION_SYSTEM §0, «Ogni animazione dichiara una funzione fra sette, e se non ne ha una non esiste» — §5 line 203: «| row.flip | layout | …». LAYOUT is one of the nine FAMILIES in §2, not one of the seven FUNCTIONS in §0 (orientamento, gerarchia, causalità, stato, feedback, profondità, delizia). One of eleven catalogue entries is invalid on the system's first rule.

5. MOTION_SYSTEM §1, «Curve — tre» — §5 line 203 gives row.flip the curve «limitata da --motion-slow», which is a duration, not a curve. §4.6 line 170 sets only ::view-transition-group(*) { animation-duration: … } and never animation-timing-function, so every named group (ile-chrome-header, ile-chrome-rail, ile-case-band, and 40 rows) animates on the UA default `ease`. A fourth curve enters the shipped result. It escapes the cubic-bezier count test because it is never written in CSS, which makes it worse, not better.

6. Declared scope vs implementation — line 3 and §4.6 title restrict this to «transizioni fra pagine dello STESSO COMPITO», but line 163 ships a global, unscopable `@view-transition { navigation: auto }`. It will fire on public→portal, on login and logout, and on the language switcher (templates/components/language_switcher.html:14 is a plain same-origin <a>), morphing ile-main across an FR→AR LTR/RTL direction flip. No pageswap/pagereveal + skipTransition() gate is specified anywhere.

7. DESIGN_SYSTEM_V2 §9.8 (binding) — §4.5 line 158 keeps the naked <select> at templates/cases/detail.html:97-107 and 196-210 and decorates it with a 2px stamp, while §9.8 states the case-file state change must be «form a pagina con conferma, non <select> nudo». The spec spends its best idea polishing a control the design system has already banned. Relatedly §4.2 line 86 puts «le cinque sezioni di cases/detail.html» behind desktop tabs, which §9.8 does not prescribe (it prescribes a workspace with the sections present, and <details> only on mobile).

8. Technical claim that is simply false, used as the safety guarantee — §4.6 line 176: «Se un nome manca nel documento d'arrivo, la transizione si annulla e resta la navigazione di oggi: non c'è modo di romperla». A view-transition-name present in the old document and absent in the new does NOT abort the transition; the element gets an old-only group and animates OUT. Only duplicate names in the same document skip the transition. Since .portal-rail and .case-band exist in ZERO templates today (grep across templates/ returns 0 for both), the stated anti-flicker guarantee rests on two selectors that do not exist and, when they do, will produce exactly the header/rail flicker §4.6 claims to prevent on any navigation that drops one.

## Lacune (ciò che l'implementatore dovrebbe inventare)

1. §4.3 is titled «zero JavaScript» and then requires JS: a 60ms delay between the closing and opening panel, and scrollIntoView({block:'nearest'}) after the transition. templates/components/accordion.html:8 already uses the native name="…" exclusive <details>, where the browser closes the sibling itself and gives no hook to delay the opener. And §7 deletes initAccordions(). The implementer is left to re-invent exclusivity in JS that the same document just removed.

2. interpolate-size: allow-keywords is set on :root (§4.3 line 117). It inherits to the entire document, so every height:auto / width:auto transition anywhere in the product changes behaviour, not just the three accordion selectors. No containment or audit of other height transitions is specified.

3. §4.6 names .portal-rail and .case-band, neither of which exists in any template today (0 matches across templates/). The spec does not say who builds them or what happens in the interim.

4. The sessionStorage['ile:task'] key in §4.8 is written only by swap.js «al clic». Form POSTs, the back button and typed URLs never write it, so a stale key will suppress [data-reveal] on a page where the reveals should play, or leave a double arrival where it should suppress. Specify a write on every navigation, or read the task from location on load instead.

5. §4.5's sessionStorage mark {key, state, at} never says whether `state` is the OLD state text or the newly chosen value. §8.4's guard («il testo di stato letto nel DOM è cambiato rispetto a quello memorizzato») implies the old one; the inline <select> hands you the new one. One-line ambiguity, two opposite implementations.

6. §4.2 hard-codes «le cinque sezioni di cases/detail.html», but the fifth section (templates/cases/detail.html:190, «Faire évoluer l'état du dossier») sits inside an {% if %} and is absent for roles without the transition permission. A tablist that is sometimes four tabs is unspecified. Nothing is said about what happens below 80rem, about the deep-link/anchor contract (#journey-title, #checklist-title, #assessment-title, #actors-title, #state-title are live aria-labelledby ids), about Ctrl+F across hidden panels, or about print.

7. localStorage persistence of the selected case-file tab (§4.2 rule 1, via data-tabs-remember, main.js:264) means a returning user can land on a legal case file with four of five sections hidden and no indication that «Qui intervient sur ce dossier» exists. Not addressed.

8. How §4.5's TIMBRO and §4.6's cross-document View Transition interact on the same POST→redirect→GET is never stated. The stamp fires «dopo il ricaricamento» while a view transition may still be running, and the marked <tr> may be inside a tab panel that is hidden on arrival.

9. The rail's done (--accent) vs to-do (--hairline-strong) distinction in §4.4 line 152 is carried by colour plus a filled 8px disc on the current step only. Done and to-do differ by hue alone. The live region text covers it for AT, but not for a low-vision sighted user. No glyph or fill-pattern is specified.

10. 400ms before the «Enregistrement…» announcement (§4.4) and the 10s mark expiry (§4.5) are numbers outside the four-duration token set. Defensible as thresholds rather than durations, but the spec never says so.

11. §4.4 says the error state puts «il fuoco … sul <legend>». <legend> is not focusable; the focusable node is the <span id="wizard-question" tabindex="-1"> inside it. Small, but it is the kind of line an implementer will transcribe literally and ship broken.

## Segnali di «cheap / generico / default»

1. The whole visual proposal is the 2026 default kit: an animated 2px underline that slides under a tablist, a fade + 12px horizontal slide panel swap, an accordion height transition, and an 8px translateY page crossfade. Strip the Italian and the token names and this is the shadcn tabs demo plus the first page of the Motion docs. Five of the eight 21st.dev candidates studied are literally tab/stepper components, and what was extracted from them is the indicator and the fade-slide — the two most copied gestures on that site. There is no signature gesture anywhere in this document.

2. TIMBRO is a stamp in name only. The metaphor — a seal pressed onto a legal record, the single most ownable motion idea available to this product — is rendered as a 2px rule doing scaleY(0→1) along a row's inline-start border, i.e. the generic "row highlight" from every admin table, relabelled. The premium version of this gesture is a press: weight, a brief settle, ink meeting paper. The spec even forbids itself the bronze --seal-600 that would have made it read as a seal («un cambio di stato non è un sigillo»), which is a defensible token rule and a self-inflicted wound on the one memorable moment in the surface.

3. Cross-document View Transitions are the single most spectacular capability in this spec and they are spent on a crossfade. §4.6 nominates .site-header, .portal-rail, .case-band and main, then animates main with opacity + 8px translateY. The obvious premium move — a case-file row morphing into the detail page's case band, a route card morphing into the page it opens, a shared element that makes the navigation feel like one continuous document — is never proposed. §4.7 gets closest with per-row FLIP and then caps it at a re-sort.

4. SOGLIA / RESPIRO / TIMBRO reads as three Italian nouns applied after the fact to fade-slide, height-transition and border-highlight. The naming does the work the design was supposed to do. An owner who rejected "editorial" will recognise the move.

5. --swap-shift: 12px with 120ms out / 240ms in, quoted three times as if it were a finding, is the exact default pairing of the Framer Motion getting-started example. Using one shift value for tabs, the wizard and pagination flattens three different gestures into one.

6. §8.7 is the tell: «Il committente non vede la differenza … Guardia: consegnare la revisione con tre registrazioni a 60 fps». The mitigation for "the owner will not notice" is a video. On a surface the owner explicitly named as weak, that is an admission that the proposal does not meet the brief, dressed as a delivery plan.

7. The rail replacing the progress bar is described as «una regola di 2 px», «l'ultimo tratteggiato», «disco pieno 8 px con anello 2 px». Everything in this spec is 2px hairlines on paper. That is precisely the flat, severe register in the owner's rejected list, and "institutional restraint" is being used here as the unstated justification the brief forbids.

## MUST-FIX

1. Resolve the initTabs() contradiction: §4.2 line 105 «initTabs() di main.js resta l'unica fonte di verità per tabindex e aria-selected» vs §7 line 227 «Si eliminano da main.js initTabs/initSteppers/initAccordions nella forma attuale (≈110 righe)». Pick one and write the resulting activate() in full.

2. Resolve hidden-vs-exit-animation. main.js:255 activate() sets panels[i].hidden = !selected for every panel in the action frame, and §4.2 rule (1) makes that non-negotiable. An element with hidden is display:none, so the 120ms opacity/translateX exit in §4.2 rule (3) and the tab.panel entry in §5 can never be observed. Specify the [data-leaving] holding class, when hidden is finally applied, and how the abort path (Escape, rapid re-activation, §6 line 213) forces it immediately.

3. Fix or delete the --swap-veil contrast claim. Recompute against --ink #15222A / --ink-2 #4A5A62 over --min-0 #F4F3F0 and pick an alpha that clears 4.5:1 for the <legend>, or stop dimming the fieldset and carry the busy state on the actions row only.

4. Guard the double submit. §4.4 puts opacity + inert on the <fieldset>, but templates/orientation/_step.html closes </fieldset> BEFORE <div class="wizard__actions">: «Continuer» and «Précédent» stay at full opacity and fully clickable during the fetch. On a legal orientation questionnaire that is a duplicate answer POST. Specify disabled/aria-disabled on both buttons and where focus parks.

5. Say how per-row view-transition-name is emitted without a style attribute (§4.7). Either swap.js writes it with setProperty before navigating, or drop §4.7 entirely. As written it is a CSP violation waiting to be committed.

6. Replace transform-origin: inline-start (§4.2 line 93, §4.4 line 152) and transform-origin: block-start (§4.5 line 158). transform-origin has no logical keywords; the syntax is [left|center|right|top|bottom|<length-percentage>]. These three declarations are invalid and will be dropped by the parser, which silently breaks the tab mark, the rail fill and the TIMBRO in both LTR and RTL. Define a --swap-origin custom property flipped under :dir(rtl), or use left/right with an RTL override.

7. Reconcile §4.4 with apps/orientation/tests/test_compliance.py. Line 124 asserts form["hx-post"] == url — removing the five hx-* attributes breaks it. Lines 118-121 assert a role="progressbar" element carrying aria-valuenow, aria-valuemin, aria-valuemax, aria-valuetext and a resolvable aria-labelledby — replacing it with <ol class="rail"> breaks it, and §4.4 line 152 cites that same aria-valuetext as the guarantee that the rail is honest. Specify whether role=progressbar and the visible «Question N · P %» label survive on the <ol>, and note that the spec's «Nessuna modifica di vista né del contratto dati» claim is untrue at the test layer.

8. Scope @view-transition. Global navigation: auto is not «pagine dello stesso compito». Specify the pageswap/pagereveal listener that calls skipTransition() when the first path segment after the language code changes, and unconditionally on a language switch.

9. Remove contain: paint from .tabs__viewport and .accordion__item, or prove the focus ring survives. contain: layout alone gives most of the isolation without clipping.

10. Fix the §5 catalogue: row.flip declares «layout», which is not one of the seven functions, and its curve cell holds a duration. Add animation-timing-function to ::view-transition-group(*) so the UA `ease` does not become a fourth curve.

