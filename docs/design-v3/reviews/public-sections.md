# REVISIONE INDIPENDENTE — public-sections

Round 1 · premium_lift **4/10** · conforme: **NO** · implementabile: **NO**

> This is the best-engineered document in the batch and the one most likely to fail the brief it was given. The audit is real — I reproduced §1.2 (seven `.section__title` at 38px/36px, weight 400), §1.4 (`max-inline-size: 420.75px`), §1.6 (page 7921px), §1.7 (11 `[data-reveal]` total), §1.10 (`348.172px 248.688px 248.703px 298.422px`, 16 links, 629px) and every one of the ~25 contrast ratios in §4.1 to two decimals, and the two UI-UX-Pro-Max outputs I re-ran came back byte-identical including the absurd "location, alt, let, auto, twice" — nothing here is fabricated. But the organising idea is architecturally broken: the four numbered movements and the fused congedo are hard-mapped to `entrances / orientation+pathways / pilot / trust+antifraud+news+ecosystem / reserved`, and `pages.services.home_sections()` lets the back office reorder, gate and unpublish every one of them — in the Phase-3-closed configuration that is running right now on :8770, `CLOSED_ORDER` contains no `pilot`, no `antifraud`, no `news` and no `reserved`, so Movement III disappears, Movement IV loses its declared protagonist, the numbering reads I, II, IV, and the `soglia` with its arch, three steps and `soglia-steps` DELIZIA entry has no content at all; the `banner` section that `CLOSED_ORDER` does contain is not mentioned anywhere in the spec. The claim that `data-movement` can be "derived from the rank class already present" is false — `section--c` and `section--d` appear in both Movement II and Movement IV, so the grouping is by section key, which lives in the service layer the spec forbids itself to touch. And on the actual commission: the owner said the backgrounds are unmemorable and there are not enough elegant modern images, and this spec answers with a grey `repeating-linear-gradient` graph-paper grid, a `gap: 1px` hairline bento lifted from a 21st.dev bento component, `padding: var(--s-6)` on every cell, a `translateY(-2px)` + `shadow-2` card hover, a fade + `translateY(12px)` reveal, and §7's headline "Immagini: zero nuove" — which is "institutional = sober" wearing a better suit, and that excuse was explicitly forbidden.

## Violazioni dei vincoli non negoziabili

1. LEGAL/PRODUCT TRUTH + PUBLICATION GATES — §4 movement table (lines 69-75) and §4.8: the four movements and the congedo are hard-mapped to a fixed section list, but `apps/pages/services.py:646 home_sections()` iterates `section_rows()` with `section_gate_open()` and skips builders returning None. `apps/pages/tests/test_home.py:19` `CLOSED_ORDER = [hero, banner, entrances, orientation, pathways, trust, ecosystem]` — in Phase-3-closed (:8770, a live configuration) Movement III (`pilot`), the Movement IV protagonist (`antifraud`), `news` and the whole CONGEDO soglia (`reserved`) do not render. The spec never states what an empty movement does, and `banner` (`templates/pages/home/_banner.html`, `data-section="banner"`, prescribed p2.home.banner.* texts) is absent from the spec entirely — grep for 'banner' returns only query strings and a 21st.dev table cell.

2. LEGAL/PRODUCT TRUTH — §4.7 line 179 and line 198 ("Nessun link si perde: 16 prima, 16 dopo"). The live footer's 16 links are 5 legal + 9 navigation (`Accueil` + 8 CMS `footer_menu` rows) + email + antifraud. The proposed anatomy is "ÉCOSYSTÈME 5 voci, INFORMATIONS 5 voci legali" = 10 route links. Four navigation destinations are silently deleted and the arithmetic in line 198 does not reconcile with the structure in line 179. `footer_menu` is CMS-driven and variable-length; "5 voci" is a measurement of one seed, not a contract.

3. LEGAL/PRODUCT TRUTH — §4.7 line 179 drops `templates/partials/footer.html`'s fourth column entirely, including the `{% blocktranslate %}` sentence "{{ project }} est un écosystème d'information et d'orientation promu par {{ promoter }}." (visible in my `rev_foot.png`) and the `{% brand_words %}` / `site-footer__mark` line "Italy Legal Entry™ — marque déposée". Risk #8 (line 272) promises a word-for-word text diff as the guard, but the proposed anatomy guarantees that diff fails. It also moves the gate-conditional `{% if gates.phase3_public %}` antifraud link into the bottom bar without restating the gate, and demotes the one element the implementation document requires to be highly visible from a bordered CTA to an inline footnote.

4. LEGAL/PRODUCT TRUTH + DATA CONTRACT — §4.6 line 175: "per il partner autorizzato, una pillola di stato ... con la parola". `templates/pages/home/_ecosystem.html` exposes only `card.partner.name` and `card.partner.logo_public`; `partners.services.authorized_partners()` already returns only authorised partners (gate G6). There is no status field, no word, no translation key and no source given. The implementer must invent public wording about partner legal authorisation — on a page whose own template comment says "nothing suggests a public authority" — or change the view, which the spec forbids at line 202.

5. DESIGN_SYSTEM_V2 §1.3 rule 5 + §7 — §4 line 75 and §4.7 line 179 fuse `_reserved` (a `home_sections()` CONTENT section, currently inside `<main>`) onto `--mid-0`. §2 exempts the FOOTER (`--mid-0 utility e piè di pagina`), not a content section with an h2, a prescribed body and a primary CTA. HOME is IMMERSIVE and allows two midnight chapters; hero + pilot already spend both. The defence at line 179 ("Il piè di pagina è cromatura") covers the footer and not the soglia.

6. DESIGN_SYSTEM_V2 §10 + §1.3 rule 3 — §4.5 line 151: `.avviso__actions a { border-color: var(--seal-600); color: var(--accent); }` applied to `a.btn.btn--secondary.btn--seal`. §10 defines SECONDARY as `bordo --hairline-strong, testo --ink` and TERTIARY as `testo --accent`; this is neither. §1.3 rule 3 restricts bronze to seals — a control's border is chrome, not a seal. This is the one place the spec puts a second colour on an interactive element.

7. DESIGN_SYSTEM_V2 §1.3 rule 2 + §6 — §4.4(a) lines 130-132 draw the 160px graticule in `color-mix(... var(--mortar) ...)`, i.e. `#D3D2CC` grey. §6 defines the cartographic system as the territory's graphic and §1.3 rule 2 says `--terr-line` draws "isoipse, graticola, rotta, glifi". The one background device offered in answer to "backgrounds too simple or unmemorable" is therefore rendered as neutral grey graph paper, not as the system's own signature — which is exactly what makes the spec's own risk #2 real.

8. MOTION_SYSTEM §0 + ANTI_PATTERNS §1 — §5 `movement-head` (line 212): `opacity 0→1, translateY(12px)→0` on folio, title and apparatus, staggered 60ms. §0 lists the forbidden example for GERARCHIA as "tutto entra insieme con lo stesso fade" and states "`fade-in-up` generico su tutto ciò che entra in viewport è vietato: è la prima riga di ANTI_PATTERNS.md". Three nodes receiving the identical fade 60ms apart is that pattern at reduced scale. It also silently forks `static/js/src/shell.js`, which already implements `[data-reveal]` HIERARCHY at 320ms / 10px / 60ms — the spec indicts that system as unused at §1.7 and then writes a second one at 240ms / 12px / 60ms instead of applying it.

9. WCAG 2.2 AA 1.4.11 (internal contradiction) — §1.5 line 19 condemns the current panels because their boundary is `#D3D2CC` at 1.37:1, "sotto il 3:1 che la 1.4.11 chiede a un bordo che porta informazione". §4.2 line 94 rebuilds them as `gap: 1px; background: var(--mortar)` where `--mortar` is that same `#D3D2CC`, and cell fill `--min-2` against ground `--min-0` is 1.06:1, so the divider between two adjacent cells is again a 1.37:1 hairline and nothing else. §6(a) line 225 claims the fix by quoting only the outer frame's 3.59:1.

10. WCAG 2.2 AA 2.5.8 / brief's "44px on touch where the design allows" — §4.7 lines 191 and 195: `min-block-size: 40px` with a mobile grid of `gap: 0 var(--s-4)`, i.e. zero row gap, so two adjacent footer links are 40px tall and touching. A footer link list is the clearest case of "where the design allows" 44px, and the spec settles at 40 while making the row-gap zero.

## Lacune (ciò che l'implementatore dovrebbe inventare)

1. §4.4(b) LA PIEGA has no class name, selector, CSS block, markup, template or file — only a height, a ground, tick colour/size/pitch and a label. It is the signature device of the whole proposal and the implementer invents it entirely.

2. §4.4(c) IL RAIL has no class names, markup, CSS, JS, rotation angle or sticky offset (it must clear `--chrome-height` = 100px desktop), and specifies "a sinistra" — a physical direction in a spec that declares logical-properties-only at line 227. §5's `movement-tick` references it as though it existed.

3. §4 line 67's `data-movement` derivation from the rank class cannot work: `section--c` and `section--d` occur in both Movement II and Movement IV. The grouping is by section key, and keys live in `services.py`, which line 202 forbids touching. No mechanism given.

4. §4.3 line 109 drops `_section_header.html`'s `{% else %}<h2 class="visually-hidden" id="{{ title_id }}">{{ fallback_title }}</h2>` branch — every section's `aria-labelledby` target when the back-office heading is blank (`test_blank_heading_keeps_an_accessible_section_title`).

5. §4.3 / §4.5 markup shapes omit every `{% if X.lang %} lang="{{ X.lang }}"{% endif %}` fallback marker — the WCAG 3.1.2 language-of-parts marking on prescribed texts with no official IT/EN/AR version.

6. §4.3 wraps the contract's `date` in `<time>`, but `_section_header.html` defines `date` as "a revision date OR a source". No `datetime` format specified; a non-date string in `<time>` is invalid.

7. §4.5 omits `{% if s.note %}<p class="home-section__note">` (live in the template between body and actions) and the `{% if d.url %}` guard on the action.

8. §4.6 specifies only the gate-G3-open promoter branch (`faq_who`); `_ecosystem.html`'s `{% else %}` connective sentence for gate-closed is unmentioned.

9. §4.6 redesigns `components/empty_state.html` with no scoping — it is included by 21 templates across portal, forum, community, glossary, news, partners, pathways, deadlines, messages and requests, and is governed by DESIGN_SYSTEM_V2 §9.6 and other specs in this council. Its `role="status"` and `action_label`/`action_url` branch are not mentioned.

10. `templates/components/section_header.html` — the second header component, used by four `ecosystem/*.html` pages — is untouched, leaving two header grammars and leaving indictment §1.4's 420.75px column alive on those pages.

11. The movement names and congedo row heads are new user-visible French strings with no translation key, no locked-registry entry and no stated behaviour on /it/, /en/, /ar/ — on a page whose own docstring says nothing prescribed is typed in templates.

12. §4.7's "FR IT EN ع" language row has no markup, no reference to the existing `components/language_switcher.html`, no `lang`/`hreflang`, and invents a single-glyph Arabic label with no accessible name.

13. §4.8 adds five `@import`s to `main.css` but does not add the matching `<link rel="preload" as="style">` entries that `base.html` maintains for every layer specifically to remove the LCP request chain. §7 never mentions the request chain.

14. §4.8 introduces `static/js/src/sections.js` (esbuild auto-globs, so bundling is fine) but specifies no `<script type="module">` tag and no host page.

15. The movement table makes the entrances panel Movement I's protagonist "da incorniciare" and §4.2 designs the panel family for the four routes, yet `_entrances.html` / `components/entrances.html`, `_orientation.html` and `_pilot.html` are absent from §4.8's file list, while `_trust.html` appears there with zero design treatment despite carrying two gate-dependent layouts (`data-trust="faq"` vs `"interim"`).

16. Risk #6's selector inventory misses everything the spec renames. Verified breakages in `apps/pages/tests/test_home.py`: `section__title` assertions at :247, :505, :507, :522; `antifraud-panel__body` at :60 and :66; `#icon-shield` in the antifraud block; `class="empty-state"` at :392.

17. §1.11's "link alti 13 px" is a measurement error: I measured `.pathway-list__item` at 141-169px with `.pathway-list__title a::after { position: absolute; inset: 0px }`, so the 2.5.8 target is the whole item. §6(b) claims credit for fixing it with `.reglist` at 56px — a smaller target — and `.reglist` duplicates the existing `.pathway-list` (`components.css:1995-2074`) almost line for line.

## Segnali di «cheap / generico / default»

1. §4.2 line 94 `.panelgrid { display: grid; gap: 1px; background: var(--mortar); }` — the hairline-mortar bento grid is the defining shadcn/Tailwind marketing-page cliché of 2024-26, and the spec sources it openly from a 21st.dev bento component (`hirael/feature-10`, §3 row 1). Re-expressing it in Django and renaming `bg-border` to `--mortar` does not stop it reading as a bento grid.

2. §4.2 line 99 `.panel:hover { box-shadow: var(--shadow-2); transform: translateY(-2px); }` — card lifts 2px and gains a soft shadow on hover is the literal default shadcn `Card` interaction, and `--shadow-2` is a `0 1px 2px / 0 4px 12px` pair indistinguishable from `shadow-sm`.

3. §4.2 line 95 `.panelgrid > * { padding: var(--s-6) }` — uniform 24px on every cell, i.e. `p-6`. ANTI_PATTERNS §1 lists "Spaziatura uniforme gap-4 / p-6 | nessuna gerarchia spaziale" as a generated-design signal, and §6.6's own bento rejection ("quattro tessere uguali") condemns the same thing.

4. §4.4(a) lines 130-132 — a grey `repeating-linear-gradient` graph-paper background at 160px is the single most common 'make it look technical' AI background of this period and will read as a Tailwind `bg-grid` utility, particularly drawn in `#D3D2CC` rather than the territory teal the system reserves for it. Risk #2 names this and the guard ("si abbassa l'alfa, non il passo") makes it fainter, not more authored.

5. §5 line 212 `movement-head` — fade + 12px rise, staggered, on everything that enters the viewport. ANTI_PATTERNS §1: "Stesso fade-in-up su ogni elemento, o nessun moto | reveal identici in cascata". This is the one entrance animation on the whole surface and it is the default one.

6. §4.6 line 172 — arrow translates 4px on hover. Already present verbatim in `components.css:2069`, and taken again from 21st.dev candidate 2. The spec's entire 'dynamism' vocabulary is: 12px fade, 2px lift, 4px arrow, a ring stroke-dashoffset and three bars scaling from .7 to 1. For an owner who said 'not dynamic enough', that is a smaller motion budget than he already rejected.

7. §4.4(c) — sticky left rail, mono ticks, rotated running heads, `IntersectionObserver` scrollspy. This is the standard docs-site table-of-contents, and the spec takes it from `ibelick/scroll-progress`. It will read as Nextra/Mintlify chrome, not as an institutional device.

8. §4.1 / §4.5 — `--seal-050 #E7DDCD`, a beige band with a bronze top rule and a stamp glyph. At page width with 48-64px vertical padding this is one bad render away from reading as a legacy govtech cookie banner or a Bootstrap `alert-warning` in a warmer hue — the exact thing §1.8 and §3 row 4 are written to escape.

9. §7 line 241 — "Immagini: zero nuove", one deferred decorative `<picture>` slot for the entire surface, marked BLOCKED_BY_MISSING_ASSET at §6 line 233. The owner's stated defect is "not enough elegant modern coherent IMAGES". Answering it with a design that is "completo senza" is the forbidden excuse restated as a virtue.

10. The whole proposal's visual vocabulary — hairlines, ordinals, mono uppercase eyebrows, running heads, folios, serif section titles, a register list, a grey grid — is a more rigorous version of the editorial register the owner rejected on 24 September. Nothing in §4 is spectacular; the word 'measure' is fully honoured and the word 'spectacular' is not attempted.

## MUST-FIX

1. Resolve the movement architecture against the CMS contract, or abandon it. State explicitly what each movement does when its sections are gated off or reordered, assign `banner` to a movement, define how a movement with zero visible sections collapses (including the roman numerals), and define the congedo when `reserved` is absent (Phase-3-closed, live on :8770). Give the actual mechanism for `data-movement` — an `{% if s.key in ... %}` chain in the partial, or an explicit council decision to add a `movement` field in `services.py`.

2. Rebuild §4.7 on the real footer. Enumerate all 16 links (5 legal + 9 CMS `footer_menu` + email + antifraud), define the layout for a variable-length `footer_menu`, keep the `{% blocktranslate %}` promoter/ecosystem sentence and decide the `site-footer__mark` line explicitly, restate `{% if gates.phase3_public %}` on the antifraud link, and say whether the two `<nav aria-label>` landmarks and three `<h2>` survive. Re-derive the "16 → 16" claim so it is arithmetically true.

3. Resolve the `<main>` boundary. `_reserved` is a `home_sections()` section inside `<main id="main-content">`; `partials/footer.html` is a sibling of `</main>`. One `.congedo` element cannot wrap both. Moving the footer into `<main>` destroys the `contentinfo` landmark; moving `reserved` out of the loop removes it from CMS ordering and gating. Specify which, and what it costs.

4. Restore every dropped template branch in the markup shapes: the `visually-hidden` fallback `<h2>`, every `{% if X.lang %} lang="{{ X.lang }}"{% endif %}`, `{% if s.note %}`, `{% if d.url %}`, and the `_ecosystem` gate-closed `{% else %}`. Then add to risk #8 a concrete list of the attributes — not only the words — that the before/after diff must preserve.

5. Rewrite risk #6 with the real inventory: `section__title` (test_home.py :247, :505, :507, :522), `antifraud-panel__body` (:60, :66), `#icon-shield`, `class="empty-state"` (:392). Either keep the old class alongside the new one on the same element, or state that these six assertions are updated and by whom.

6. Specify the piega and the rail as real components — class names, CSS blocks, markup, template file, sticky offset against `--chrome-height`, logical inline-start rather than "a sinistra", and the source and translation key of every label — or cut them. As written they are the two devices carrying the answer to "not dynamic enough" and neither can be built.

7. Fix the 1.4.11 contradiction the spec creates for itself: either raise the interior `--mortar` to a 3:1 value, or give the cells a fill that separates them from the ground by more than 1.06:1, or withdraw the argument used against the current build in §1.5.

8. Drop the bronze border from `.btn--seal` (§4.5 line 151). Use SECONDARY (`--hairline-strong` + `--ink`) or TERTIARY (`--accent`) as DESIGN_SYSTEM_V2 §10 defines them, and keep `--seal-600` on the glyph and the sheet's rules only.

9. Scope the `empty_state.html` redesign. Either add a variant flag used only by `_news.html`, or hand the component to whichever spec owns DESIGN_SYSTEM_V2 §9.6 and cite that decision here.

10. Delete `.reglist` and upgrade `.pathway-list` in place, or state in writing why the surface needs a second identical list grammar. Same for `movement-head`: apply `shell.js`'s existing `[data-reveal]` (320ms / 10px / 60ms) rather than shipping a second reveal that differs by 80ms and 2px — and then justify, against MOTION_SYSTEM §0 and ANTI_PATTERNS §1, why a staggered fade-up is the right GERARCHIA entrance at all.

11. Give the rail's active tick a second, non-colour channel (weight, length, or a filled ordinal) and correct §1.11 / §6(b): `.pathway-list__title a::after { inset: 0 }` already gives a 141px pointer target, so the 2.5.8 indictment is false and the proposed 56px row is a regression. Raise the congedo links to 44px and give the mobile two-column grid a non-zero row gap.

12. Answer the actual commission. The owner rejected editorial, severe and flat, asked for images, and forbade the sobriety excuse — and this spec's whole answer is a grey graph-paper grid, a 1px bento, a beige band and a 12px fade, with "zero new images" stated as a performance win. Either commission the Movement II photograph as a real deliverable with a brief rather than BLOCKED_BY_MISSING_ASSET, draw the graticule in the territory's own `--terr-line` as §6 prescribes, and name one authored moment on this surface that a visitor would remember — or say plainly to the council that this surface cannot deliver 'spettacolare con misura' without an asset budget, so the decision is made by the owner and not absorbed silently into the design.

