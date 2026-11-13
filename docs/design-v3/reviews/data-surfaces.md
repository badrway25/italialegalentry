# REVISIONE INDIPENDENTE — data-surfaces

Round 1 · premium_lift **6/10** · conforme: **NO** · implementabile: **NO**

> The audit in §1 is the best-evidenced thing in this repo: I recomputed all twenty contrast ratios and nineteen are exact to two decimals, including the two failures (--ok-700 on --ok-100 = 4.44, --seal-600 on --seal-100 = 3.86) that justify the new tokens, so --ok-800/--pending-100/--seal-700 are necessary and not invented; every grep count verifies (form__group in CSS = 0, form__fieldset in templates = 0, data-table in 20 templates, class="empty" in 31, empty_state.html included by 21, sprite = exactly 36 symbols with icon-threshold genuinely absent); the nested :has() at portal.css:476 is real and the spec understates it, since the invalid selector sits in a comma list with .table-region:has(table:has(…)) on L475 so the whole rule dies for both; and re-running query #5 returned the "don't use back.out on dense data tables; the overshoot reads as sloppy on informational UI" line verbatim, so the tool work is real, not fabricated. Then it breaks its own case. It diagnoses #1E4A85 as an illegal second interactive accent because "DÉPOSÉ" reads as a link, and in §4.1 gives .pill--filed the text colour --accent #0F6A72 — the site's actual link colour — which is strictly worse than the defect it replaces; it puts --radius-tile 6px on .reg after calling .reg a "foglio", where DS §2 says sheets are radius 0 and 6px belongs to the brand tile alone; and it builds the facet bar out of 999px pill chips that DS §10 forbids outright ("niente pillole oltre le pillole di stato"). The fatal one is §4.1's sortable header: it asserts the GET-form sort "funziona senza JavaScript" and rejects TanStack because "il server [lo] fa già con un ?sort=" — no view or service in portal, documents, cases or companies reads request.GET["sort"] (only "page"), and apps/documents/requirements.py:35 states the register order is a fixed product rank, so sorting cannot be built without the Django work the spec's own preamble forbids. Against the owner's brief this is an excellent correctness-and-density document and a weak spectacle one: it proposes zero images by its own statement, zero midnight chapter, zero territory graphics and no signature moment in 213 lines, and where it does reach for expression it reaches for shadcn's faceted-filter bar, a 2021 sweeping-gradient shimmer and Linear's density-toggle masthead.

## Violazioni dei vincoli non negoziabili

1. ONE INTERACTIVE ACCENT (DS §1.3 rule 1: 'Link, CTA primaria e anello di focus condividono --accent. Nessun titolo, icona o sfondo lo usa'; rule 2: territory teal 'mai testo, mai interazione') — broken by §4.1 pill table, line 98: `.pill--filed | --accent-wash #D9EEF0 | --accent #0F6A72 | 5,24:1 | icon-document`. A non-interactive status pill is painted in the exact hex used by every link, primary CTA and focus ring on the page. The spec's own §1.3 (line 19) condemns precisely this — 'Il #1E4A85 è un blu a 7,97:1: nella colonna ÉTAT «DÉPOSÉ» ha l'aspetto di un link — un secondo colore interattivo, vietato dal DS §1.3' — and then reproduces it in the real accent, which is worse, not better.

2. DS §2 RADIUS RULE ('Raggi: 0 sui capitoli e sui fogli, 2 px sui controlli, 6 px sul tassello del marchio, 999 sulle pillole di stato. Nessun altro.') — broken by §4.1 'Foglio', line 83: `.reg { background: var(--min-2); border: 1px solid var(--hairline); border-radius: var(--radius-tile) }`. The spec labels .reg '(foglio, livello 2)' on line 81 and then gives it --radius-tile = 6px, the value DS reserves for the brand tile. Sheets must be 0.

3. DS §10 ('Niente pillole oltre le pillole di stato') — broken by §4.3, line 121: `.facet` … `border-radius: 999px`, and line 122 `.facets__clear` as a pill button. 999px is reserved for status pills; filter chips are not in the DS §10 control taxonomy (PRIMARY/SECONDARY/TERTIARY/QUIET/DANGER/ICON/INLINE ACTION) at all.

4. MOTION: ONE AMBIENT LOOP PER PAGE, >= 20s / four durations only (MOTION_SYSTEM §1 'Nessun altro numero'; §4 'STANDARD, DENSE e LEGAL nessuno') — broken twice in §5: entry 7 `skel/shimmer` = '1 600 ms lineari, in ciclo' (a duration present in neither static/css/v2/tokens.css nor static/js/src/motion.js) and entry 9 `f/submit-progress` = '900 ms lineari in ciclo'. Both are loops well under 20s on data/form pages, which are DENSE by DS §7 and get zero living objects. Entry 7 grants itself the exemption in its own performance note ('non consuma il budget «un oggetto vivo per pagina» (§4)') without declaring an amendment to the binding document.

5. NO DJANGO VIEW / DATA-CONTRACT CHANGES (mandate, and the spec's own §4 preamble line 77: 'Nessuna vista Django, nessun contratto dati toccato: tutto passa da classi, data-* e parametri GET già disponibili') — broken by §4.1 'Ordinamento', line 86: `<button class="reg__sort" name="sort" value="due">` inside `<form method="get">`, 'funziona senza JavaScript', and by §3 candidate 9's rejection reason 'un ordinamento che il server fa già con un ?sort='. Verified false: grep over apps/portal/views.py, apps/documents/views.py, apps/companies/views.py shows request.GET read only for 'page' (portal/views.py lines 86, 104, 111, 123); no 'sort' key anywhere in apps/portal, apps/documents or apps/cases; apps/documents/requirements.py:35 documents the register order as a fixed rank ('Rank used to sort a register. Missing and expiring first'). §4.3's 'facet, ordinamento e pagina sono già parametri GET' is one-third true.

6. LEGAL/PRODUCT TRUTH IS UNTOUCHABLE — broken by §4.2, lines 109-113, which caps `.reg__record` at four lines and 128–152px (pill+échéance / titre / responsable / action). templates/documents/partials/register.html carries five further facts per row with no slot in that card: `Facultative` (mandatory flag), `row.state_reason` (the rule behind the state, class doc-register__reason), `version {{ n }}`, `row.responsible_note`, and the `row.action_blocked` branch's link to accept the Conditions d'utilisation (`{% safe_url 'legal:terms' %}` with the locked fallback 'Acceptation des Conditions d'utilisation requise.'). templates/portal/dashboard.html adds `item.source_title` — the FONDEMENT that DS §9.8 names explicitly ('checklist con FONDEMENT') — and `item.responsible_note`. The spec promises verbatim retention for empty-state sentences (§4.4) and says nothing about the row's legal payload.

## Lacune (ciò che l'implementatore dovrebbe inventare)

1. SPRING_SETTLE and SPRING_FOLLOW do not exist in static/js/src/motion.js (grep: 'NOT DEFINED ANYWHERE'); motion.js exports only animate, scroll, inView, stagger, spring, hover, press, withMotion, reducedMotion. §5 entries 1, 2 and 5 reference SPRING_SETTLE as if it were available, while MOTION_SYSTEM §1 says a value present in one place and not the other 'è un difetto'. Numbers (260/30) are given, so cheap to fix, but the spec must say it is creating them.

2. `--dir` is used in §6 ('il chevron di espansione (rotazione moltiplicata per --dir)') and is defined in no stylesheet in static/css/. MOTION_SYSTEM §5 prescribes it; nobody has implemented it.

3. What element is `.reg__record`? §4.2 keeps the `<thead>` in the DOM and gives `<td>` a `data-role`, implying the card IS the `<tr>` restyled; §4.1 line 104 lists `.reg__record` as an independent root selector. Worse, §7 puts `content-visibility: auto` + `contain-intrinsic-size: 0 148px` on it — applying size containment to a table row is untested and can collapse table layout. No markup shape is given for either reading.

4. Where the sorting `<form method="get">` opens and closes is never stated. Inside `<thead>`/`<tr>` is invalid HTML; wrapping the whole `.reg` collides with `.finder`'s own form in the same masthead. No `form="id"` association is offered.

5. `.reg__head::after` (the pin strip, §4.1 line 85 and §5 entry 6) is specified on the `<thead>` while `position: sticky` is on the `<th>`. Generated content on a table-header-group box is unreliable; the implementer must relocate it to per-`th` `::after` or a sentinel element, and must invent which.

6. `scroll-padding-block-start` conflict: §6 proposes `calc(var(--chrome-height) + 48px)` on the document, but static/css/v2/shell.css:490 already sets it from `--header-height` and static/css/base.css:17 from `--chrome-block-size`. Three declarations, three different tokens, and the cascade order of data-surfaces.css against shell.css is unspecified.

7. The sticky offset `inset-block-start: var(--chrome-height)` (100px) is asserted from the token file, not measured inside the reserved area where the institutional bar may be absent. If it is, every sticky thead floats 36px low.

8. `templates/components/data_table.html` is said to take `rows`, `columns`, `sortable`, `region_label`, but `columns` is in no view context and not one `{% include %}` call site is shown. Every caller must hardcode the column list; one worked example is needed.

9. `<caption>` is absent from the `.reg` anatomy (§4.1 line 81). Both current tables carry one, and on templates/portal/dashboard.html:94 it doubles as the region's accessible name via `aria-labelledby="t-dashboard-1"`. DS §9.4 requires `caption`. Following the anatomy literally deletes it and strips the region's name.

10. §4.6(b) removes `role="alert"` from `.f__error` — correct — but never states that `.f__error`'s id must be appended to the control's `aria-describedby`. It is only implied by 21st.dev candidate 3's 'describedby composto [descId, msgId]'. DS §10 requires `aria-describedby`.

11. `.reg[data-density]` persists in localStorage with no key name, no statement of per-table versus global scope, and no account of what a shared `.facets__permalink` URL does with a density the recipient did not choose.

12. `.reg__foot` appears in the anatomy (§4.1 line 81) and is defined nowhere else. Pagination markup is never specified at all — even though `?page=` is the one GET parameter that genuinely works (services.paginate, templates/components/pagination.html, used by 7 templates), which also makes §1's 'paginazione 0' true only of rendered chrome.

13. The mobile record card has no radius, no border, no inter-card spacing, and no behaviour specified for the 768–1024 band between the card layout and the desktop table.

## Segnali di «cheap / generico / default»

1. §4.3 `.facet` — 999px pill chips with a 12px check glyph, an active wash, a live count and a 'Tout effacer (3)' clear-all. This is the shadcn/Tailwind faceted-filter bar verbatim and is the most recognisable default-library tell in the whole document. It is also the DS §10 violation. An institutional register should be filtering on a rule, not on Notion tags.

2. §4.5 `skel/shimmer` — a 40%-wide gradient band sweeping across every loading region on a 1600ms loop. The sweeping shimmer is the 2020–2022 default-library loading look; in 2026 it reads as a component someone installed. The spec's own instinct elsewhere (one shimmer per region, 200ms delay, 400ms floor) is good craft applied to a tired form.

3. §4.1 'Masthead' — region name + live count + search + density toggle + permalink. This is Linear/Notion table chrome on a legal register. The spec names the risk itself in §8 ('Cromatura da console BI') and guards it at >8 rows, which is honest, but a localStorage density switcher is still a SaaS tic, not an institutional signature.

4. §4.3 `<p class="reg__count">7 lignes · 3 en attente</p>` — 'lignes' is spreadsheet vocabulary replacing a domain noun. The existing templates/documents/partials/register.html already says '3 pièces demandées · 1 sur 3 validées · 2 en attente', and its own comment insists 'Counts, never a percentage meter: "3 sur 7" is verifiable'. The proposal downgrades verified domain grammar to generic UI copy.

5. Six pill tints on one surface. The spec names this risk ('Confetteria di pillole') and caps visible states at four, which is the right guard — but the six-colour status palette with a glyph each is still the stock dashboard look, and .pill--filed in link-teal makes it read as a chip library rather than a legal register.

6. §7, line 191: 'Immagini: zero.' The owner's verdict named 'not enough elegant modern coherent IMAGES' and 'backgrounds too simple or unmemorable'. This surface proposes no image, no midnight chapter, no --terr-line graphic, no seal treatment and no typographic event. The one candidate for memorability is a 32px hairline arch-and-steps glyph in the empty state. Every premium move in the document is subtractive (remove the navy filet, remove the pop-in, remove the asterisk, remove transition:all). Subtraction is very likely correct for a DENSE surface under DS §7 — but the spec never argues that, and the silence is exactly what the owner will read as the same answer again.

## MUST-FIX

1. Recolour `.pill--filed` (§4.1 line 98). Remove --accent as pill text. A status is not interactive; use an ink-neutral ground (--min-1 + --ink + icon-document, as .pill--blocked already does) or a new non-accent semantic pair with computed ratios. Otherwise 'DÉPOSÉ' is chromatically identical to every link on the page — the exact defect §1.3 was written to kill.

2. Change `.reg` border-radius from var(--radius-tile) to 0 (§4.1 line 83), and state the radius for `.reg__record`. DS §2: sheets are 0; 6px belongs to the brand tile alone.

3. Redesign `.facet` and `.facets__clear` without 999px pills (§4.3 lines 121-122). Express the active facet with the DS §10 vocabulary already available — a QUIET/SECONDARY control with 2px radius, a rule on the reading edge, aria-current and the check glyph. Keep the count-in-a-span accessible-name fix, which is genuinely good.

4. Resolve the two sub-20s loops (§5 entries 7 and 9) against MOTION_SYSTEM §1 and §4. Either obtain and write an explicit derogation for request-bounded loaders into MOTION_SYSTEM (DENSE pages, loop stops on response, degrades to static if an ambient loop exists) and register 1600ms as a token, or re-spec both as non-looping: a stepped/determinate indicator for f/submit-progress and a static level-1 skeleton for skel/shimmer.

5. Cut column sorting from V1, or stop claiming it is free. No view or service reads ?sort= (request.GET is read only for 'page'), and apps/documents/requirements.py:35 fixes the register's rank as product truth. Either delete §4.1 'Ordinamento', the aria-sort markup, §5 entry 4 and candidate 9's rejection reason, or write the view/service work explicitly as out-of-scope-for-this-spec and route it through the product owner as a scoped change — not as the a11y footnote it currently is in §6(f).

6. Give the mobile record card a home for every fact it currently drops (§4.2). Name the slot for row.state_reason, Facultative, version {{ n }}, responsible_note, item.source_title (the FONDEMENT), and the action_blocked branch's Conditions d'utilisation link with its locked fallback sentence — and state, as §4.4 does for empty states, that these strings stay verbatim. A four-line 128–152px card cannot carry them; either add a fifth line, fold them into the `.reg__expand` detail row, or raise the height budget and re-derive the 2891→1332px figure.

7. Keep `<caption>` in the `.reg` anatomy and preserve the aria-labelledby link. templates/portal/dashboard.html:94 names its region through the caption; the proposed anatomy has no caption and would silently strip the region's accessible name. DS §9.4 requires it.

8. Correct the two factual errors in §1.5 and §6. The dashboard scroll region is NOT unnamed: templates/portal/dashboard.html:92 carries aria-labelledby="t-dashboard-1" resolving to a visually-hidden caption ('Éléments du dossier, leur état, le responsable et l'échéance'). Drop 'nessun aria-label' and 'senza nome'; the real defects — the invalid nested :has() and a focusable region that does not scroll — stand on their own and are in fact stronger than stated, because the invalid selector is comma-joined with .table-region:has(table:has(…)) at portal.css:475, so the whole rule is discarded for both. Also correct --hairline-strong on --min-3 from 3,59:1 to 3,74:1 (recomputed).

9. Specify the form boundary for any GET control inside `.reg`, and specify where the sticky pin strip lives (per-th ::after or sentinel), since ::after on a table-header-group is not dependable.

10. State what element `.reg__record` is, and justify or drop content-visibility: auto on it — size containment on a table row can collapse the table. Separate the height saving (which comes from the card redesign) from the paint saving (which comes from content-visibility); §7 currently conflates them.

11. Resolve the scroll-padding-block-start conflict with shell.css:490 (--header-height) and base.css:17 (--chrome-block-size), declare the load order of data-surfaces.css relative to shell.css, and measure the real sticky offset inside the reserved area instead of assuming --chrome-height = 100px.

12. Add a one-paragraph answer to the owner's actual brief. Either argue explicitly that DS §7 DENSE mode is why this surface carries no image, no midnight chapter and no living object — and name where the premium lives instead (materia, tabular numerals, the 56px row, the arch-and-steps glyph) — or find the one signature moment this surface can afford. As written, a document that says 'Immagini: zero' will read to the owner as the same refusal he rejected on 24 September.

13. Note, do not fix silently: the whole-row `.reg__link::after { inset: 0 }` overlay (§4.1 line 89) makes the état, échéance and reference cells unselectable — a user cannot copy a case reference such as 103C80FBC6. The spec cares enough about references to wrap them in <span dir="ltr"> in §6. Either exempt the reference cell with position/z-index as done for `.reg__cell--action`, or drop the stretched overlay and make the 56px target from the link's own padding.

