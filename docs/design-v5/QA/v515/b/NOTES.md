# V5.15 — Lane B, wave W3 (label v515-b-build): Premium Forms + Icon Visual System

28 Oct 2026. Branch `v515-b`, from design-v5 `ece1eeb` (v512 W2 + v516-p2 merged). Scope: DECISIONS §15 «Lane B —
Premium Forms + Icon Visual System» (the V5.15 override), with the old W3 B items (multi-step need / public needs /
sign-up, password checklist, document rows and filters). Built on W2's field system (one partial, fieldcheck.js,
choice cards, combobox, date, number, the account shell) — nothing beside it. Not merged.

**Carry-over (DECISIONS §16):** no item names lane B. M-2 (legal links) is lane C's; the one lane-B template it names,
`enquiries/partials/form_shell.html`, links only the privacy notice (category A, public) — no `legal:terms`,
`legal:notices` or `legal:disclaimer` link in it after this change, so nothing is left for C there.

## 1. What the owner sees, where (preview, once merged)

| Where | What |
|---|---|
| **/fr/entreprises/recueil-des-besoins/** (and the same form inside /fr/entreprises/) | **The formwork.** The section opens on its concept tile (briefcase), the title and the prescribed quote; then a raised panel with the lagoon→gold light on its upper edge, and — from 60rem of its own width — a sticky side at the reading edge: the three steps as a rail (square tiles, the current one lit, connectors that fill lagoon→gold), «Après l’envoi» and «Vos données». **Three steps**: «L’entreprise et son référent» (6 fields, paired two by two), «Le besoin» (8), «Vérification et envoi» — **the review** of everything typed, step by step, each with «Modifier», then the locked consent in its own plate, the privacy link, and the locked button with «Retour» at its start. «Continuer» checks the step with the server’s own messages (empty required fields light up together, focus on the first). The step slides 22 px in the direction of travel. The address keeps the step (`?etape=besoin`): reload / back return to it. |
| **/fr/compte/signup/** | **Two steps** inside «Il varco»: «Qui êtes-vous ?» — the five audience cards, their glyphs now in tiles that turn solid lagoon when chosen — then «Identité et mot de passe» with the **live password checklist**: the four rules of AUTH_PASSWORD_VALIDATORS in their own words; «au moins 12 caractères» and «pas uniquement des chiffres» fill their disc as you type (a plain disc — never a tick, O14), the two the server alone judges keep a dashed ring; the count is said once, politely, when typing pauses. A head rail (tiles + filling bar) above the step. |
| **/fr/espace-reserve/entreprise/mes-besoins/nouveau/** (qa-company) | The company’s need in **four steps + review** (Poste et territoire · Compétences · Langue et sécurité · Formation et calendrier · Vérification), the vertical rail beside the panel in the console, every short field paired, the number stepper and the selects in the 6 px plate. |
| **/fr/demande-transmise/** | **The receipt**: one raised sheet, the depot’s «filed» mark (a ring traced in 700 ms, then the gold dot — filed, not examined), the title, the thank-you sentence, the «not a candidacy» caveat with its info mark, the way on. A still under reduced motion. |
| Every form page | Inside the formwork the plate has 6 px corners, a sheet face that turns raised under the pointer and the focus, the leading glyph takes the lagoon on focus; «facultatif» is a quiet capsule; the consent sits in its own plate. A `FileField` rendered by the partial is a **drop zone** (upload tile, «Choisir un fichier ou le déposer ici», the chosen file’s name). |
| Choice cards everywhere (sign-up, questionnaire, Ma situation once D routes it through the partial) | The glyph disc became the **glyph tile**; a chosen card lifts with a lagoon wash and its tile turns solid. |
| Empty states (console lists, FAQ search without a match, profile without an organisation) | A muted surface with 12 px corners and the domain glyph in a lagoon tile (instead of a hairline and a grey disc). Lane C’s `.lettura` / `.servizio` copies of the old rule still override it on their pages — request below. |
| «Mes pièces» rows | A filed piece says its version **and its size** («240,0 Kio»). The stored file name is never shown (the register is not a file browser — an existing guard), and «Télécharger» stays on the piece’s page and drawer: the row is the link, a quiet row offers no second control (W3-C’s W-3 and Conditions-gate guards — a download in the row would break all three). The state filter no longer lists a state with 0 pieces: it is folded into «Tous». |

Not visible yet: the contact and collaboration forms use the same formwork, but G2 keeps them closed on the preview
database (the unavailable notice shows under the new section head).

## 2. The Icon Visual System — `static/css/v5/_glyph.css`

The ILE treatment around Lucide/ILE symbols where a symbol names a CONCEPT: the **glyph tile** — optical sizing (sm
32→16, md 44→22, lg 56→26, xl 72→32: the glyph a smaller share of a larger tile), a paper face turning into the
lagoon wash, an accent hairline at 20 %, a top light, a short accent-tinted shadow, and the brand’s one ornament: a
**gold hairline on the tile’s upper edge** (the doorway’s light). Inside a link / button / card the tile rises 1 px and
its glyph scales to 1.06 in the soft spring; at once from the keyboard, still under reduced motion. Variants:
`--solid` (current / chosen), `--warm` (caution), `--neutral`, `--night` (and automatically inside `.chapter--dark`).
Used now: form section heads (lg), step legends (md), side notes (sm), choice cards (md), the empty state (drawn on
the svg in components.css). `_chapter_head.html` and `_section_header.html` take an opt-in `tile=True` that puts the
chapter mark in an lg tile (keeps `chapter__mark` on the svg: the registry tests still read it) — for lane C to switch
on page by page once its page sheet imports `_glyph.css` (request below). No custom ILE drawing was added in this
wave: the tile carries the identity; the registry’s concept glyphs are unchanged (no new symbol, sprite untouched).

## 3. 21st.dev — reviewed, selected, adapted (rows for COMPONENT_PROVENANCE.md, lane A’s file)

| Family | Reviewed (ids) | Selected | What ILE took / changed |
|---|---|---|---|
| Multi-step form | 28551 Configuration Stepper, **23576 Wizard Steps**, 1205, 28565, 28546, 29865, 29518, 29801, 29526, 28569 | **Wizard Steps 23576** (ddoemonn) | State model (current, furthest, direction), square 28–32 px tiles scaling 0.92→1, connectors that fill, the position said once (polite), panel ±22 px in the direction of travel (WAAPI, 280 ms, cubic-bezier(0.23,1,0.32,1)), focus to the step after a move, keyboard-safe. **Changed:** no React / motion — vanilla module `steps.js`; a done step keeps its NUMBER (no tick, O14); steps are the form’s fieldsets (no-JS = same form); server-word validation; `?etape=`; review step; vertical rail beside the panel. |
| Password | **23542 Password Strength**, 1883, 29799, 19004, 25113, 182, 1504, 6279 | 23542 (checklist only) | The live requirements list. **No strength meter / segmented bar** (DECISIONS §5.11); the rules are the validators’ own help texts; disc not tick. |
| Upload | **19201 File Dropzone**, 18847 UploadThing, 29988, 40107, 18108, 34883, 27137, 31348 | 19201 (geometry) | Zone + icon + call to action + chosen file; native input over the zone; solid hairline (dashed = «attesa» on V5); no preview, no client upload. |
| Inputs / validation | 29174 Group Tone Input, **23564 Inline Validation**, 8164, 25083, 3652, 27356, 25097, 16190 | 23564 + 27356 (focus lift) | Plate face turning raised on hover/focus, leading-glyph tint on focus; hint/error row stays W2’s (M10). |
| Icon containers | 23982, **28299 Icon Feature Grid**, 10754, 11356, 24509, 3556, 27366, 29986 | 28299 (icon card head) | The icon-in-a-container idea only; the tile’s material, sizes and the gold light are ILE’s. |
| Empty state | 18266 Empty Background (Director §3) | 18266 | Muted surface + semantic glyph + title + one action; no illustration. |
| Document rows / filters | 28496 File List Item, 22162 Table with Filters (Director §3) | both | Size in the meta (no name, no overflow menu: the row is the link; download on the piece’s page); zero-count filters folded into «Tous». |

## 4. Budgets (measured, gzip -9)

| Asset | Before (design-v5 ece1eeb) | After |
|---|---|---|
| `main.css` | 31 288 B | **31 317 B** (+29: the empty state’s surface and tile, components.css §23). ≤ 31 414 ceiling, but the ratchet says «no rise»: **recorded exception request for the Director** — the empty state is a shared component on 14 templates; the alternative (page-only) would duplicate it in 6 page sheets. |
| `core/forms.css` (page-only, form pages + receipt) | 2 304 B | 5 776 B (≤ 6 KB) — now holds _glyph, _formwork, _receipt |
| `orientation/wizard.css` (page-only) | 4 700 B | 5 354 B (≤ 6 KB; imports _choice → _glyph) |
| `fieldcheck.js` + `steps.js` (a steps form page) | 2 975 B | 3 471 + 2 571 = **6 042 B** (≤ 6 KB). `steps.js` is fetched only where a `form[data-steps]` is; `combobox.js` (1 486 B) only where a long select is — the company need page loads all three (7.5 KB): over the 6 KB line by the combobox, **recorded**. |
| Sprites | unchanged | unchanged |

No npm dependency, no animation library; `npm run build` with the installed packages.

## 5. Headed review (Chromium 1234, headed, under C:/tmp/ile_locks/CHROMIUM_LOCK; lane server 8784, db l4)

`C:/tmp/ile_v5_council/evidence/v515/b/` — `review.py` / `review.json`: fr + ar × 1440 + 390, and reduced motion at
1440: the needs form empty «Continuer» (5 errors, focus on the first field, URL `?etape=entreprise`), step 2, step 3
with the review (2 parts), the sign-up step 2 with the checklist («12345678» → 0/2; a long phrase → 2/2), the receipt;
**0 page errors, no horizontal overflow** in every run. Shots: `w-*.png`, `needs1`, `signup1`, `done1`, `need-fr-1440`
(console), `need-ar-390`, `eco-fr-1440` (the form inside /entreprises/, the formwork in a narrow column),
`signup-ar-390`, `needs-ar-390`. Self-score against «premium institutional legal-tech»: formwork + steps 4/5, receipt
4/5, sign-up steps 4/5, console need 4/5. Improved after the first look: the head rail repeated the legend’s words
(removed), the last step’s actions stacked on a phone (one line now, «Retour» icon-only under 30rem with its name kept),
the console side drew an empty notes rule (gone), the back arrow did not mirror in AR (fixed).

## 6. Tests

New `tests/frontend/test_forms_v515_b.py` — 16 + 2 browser: the three step specs (prescribed order kept, no field
lost, unnamed fields join the last step, error step marked), the needs page without script (all steps and fields in
the DOM, rail anchors, messages, the locked button after the steps), the sign-up page (two steps, account type first,
the four rules with the two live ones, no checklist on the confirmation), the validators’ own words, the module
fetched only for a steps form and drawing no tick, `?etape=`, Enter never sends early, budgets, logical properties /
tokens / forced colours / reduced motion of the new sheets, the file zone, the receipt (filed, never approved), the
document row (size, never the name, one link), the zero-count filter folded, the glyph tile, choice tile, the
empty-state surface; in Chromium: the needs form step by step and reviewed (fr 1440, ar 390), the password checklist.

Updated (stale by the change; no functional, a11y, security or legal guard weakened):
- `test_documents_w3_c.py`: «a state with no piece is a word, not a link» → «folded into all» (DECISIONS §3 says
  fold; still asserts 2 links and now 0 dead entries);
- `test_interior_w3_f1.py`: the six-icon cap of a public body leaves out the form’s glyph tiles, as it leaves out the
  chapter heads’ marks (presentation guard; the one-primary and no-stair asserts unchanged);
- `test_entrance_form_w2_b.py` (browser): the password-control test picks an audience and presses «Continuer» before
  reading the sign-up’s two passwords (they are step 2 now) — its spell/capitalise/correct asserts unchanged;
- `tests/i18n/test_rtl_browser.py` (browser): the Arabic empty-submit check opens the needs form on its last step
  (`?etape=envoi`), where the locked button is, then submits — the errors and the layout asserts unchanged;
- `test_service_pages_w3_f2.py::test_the_profile_s_personal_fields_say_what_they_are_for`: the country of residence
  is the CLDR select since W2 — `autocomplete="country"` on the `<select>` (WCAG 1.3.5 kept; the token for a code);
- `docs/design/DESIGN_SYSTEM_2026.md` §10: four component sections, 50 files.
Kept, honoured instead of changed: «the register is not a file browser» (no file name), W-3 and the Conditions gate
(no download in the row), «no literal colour leaves the token sheets» (shadows → `--shadow-*`, `color-mix` of tokens),
«nothing dragged» (the file field’s hook is `data-filezone`), «form__entrance.html = form.html + host» (form.html got
the same `data-steps`), the Arabic page integrity (new words carry `lang="fr"` until translated: `{% ui_lang %}` and
`step.lang`).

Runs (TEST_DATABASE_URL `test_ile_v5_l4`, one pytest at a time):
- broad non-browser (`test_form_system_v512_b test_o14_lint test_chapter_marks test_icons test_components_w1_c
  apps/enquiries apps/accounts apps/companies test_locked_content apps/documents test_account_shell_v512_b`) — 669
  passed; the 1 failure (file name) fixed; 4 `caplog` errors from that run’s disabled logging plugin (pass normally);
- frontend set (23 files: chips/cards, components, documents W3-C, entrance, icons, interior, service pages, state
  chips, static assets, tokens, page integrity, design docs, layout, orientation, overlays, reduced motion, showcase,
  chapter marks, O14, form system, account shell, the new file) — 1230 passed, 20 failed → 9 were this branch’s (all
  fixed, re-run: 837 passed + the new file 16 passed); **11 fail identically on design-v5 ece1eeb** (not this lane:
  `test_service_pages_w3_f2` — the account pages’ old public frame (stale since W2’s account shell; 6), the situation
  «what for» lines (D’s situation template; 2), the 400/500 titles (2); the profile one is fixed here); listed for the
  steward;
- browser (under the Chromium lock, headless shell for pytest): `test_entrance_form_w2_b` 34 passed;
  `test_forms_v515_b test_form_system_v512_b test_rtl_browser_entrance` 15 passed; `test_rtl_browser` 21 passed after
  the update above — its `test_every_arabic_public_page_fits_the_viewport` (×2: «54 routes served < 55») fails
  identically on design-v5 `ece1eeb` (lane C’s W1 hide gates; steward’s W2 carry-over list);
- after the last changes: `test_service_pages_w3_f2 test_forms_v515_b` — 55 passed, the 10 failures all pre-existing
  (below).

## 7. New msgids (for lane D’s catalogue pass — no .po edited)

`Poste et territoire` · `Compétences` · `Langue et sécurité` (exists as a legend) · `Formation et calendrier` (exists) ·
`Vérification` · `L’entreprise et son référent` · `Le besoin` · `Vérification et envoi` · `Qui êtes-vous ?` ·
`Identité et mot de passe` · `Étape %(n)s sur %(total)s` (blocktranslate `Étape {{ n }} sur {{ total }}`) ·
`Étape %(n)s sur %(total)s : %(label)s` (python-format, the script replaces) · `Étapes du formulaire` · `Continuer` ·
`Retour` · `Modifier` · `Non renseigné` · `Oui` · `Non` · `À savoir avant l’envoi` · `Après l’envoi` · `Vos données` · `respecté` · `pas encore respecté` ·
`%(n)s règles sur %(total)s respectées.` · `Choisir un fichier` · `ou le déposer ici`.
Reused (exist): the non-commitment sentence, «Lire la Privacy Policy», «Télécharger», the privacy-link sentence.

## 8. Requests to other lanes

- **Lane A:** `COMPONENT_PROVENANCE.md` rows of §3 (Wizard Steps 23576, Password Strength 23542, File Dropzone 19201,
  Inline Validation 23564 + Primitive Input 27356, Icon Feature Grid 28299, Empty Background 18266, File List Item 28496,
  Table with Filters 22162) and W2’s still-missing rows (Floating Label 23566, Combobox 34726, Calendar 34713, Icon Card
  Radio Group 28351). Lume/threshold: a step change is not a navigation — `steps.js` uses `history.replaceState`, no
  link, no submit, so the loader never fires on it; please keep `shell.js` keyed on real submits (it is, via
  `defaultPrevented`).
- **Lane C:** import `static/css/v5/_glyph.css` in the public page sheets (`_pagina.css` / `pages.css` / `lettura.css`)
  and pass `tile=True` to `_chapter_head.html` / `_section_header.html` where the art direction wants the tiled mark;
  drop the `.lettura .empty-state*` and `.servizio .empty-state*` copies so the shared empty state speaks there.
  The contact page’s header (`templates/enquiries/contact.html` is B’s file): the formwork section is in place; the
  page-header composition for «contact → human/institutional connection» is yours to specify — send the markup and
  B applies it, or take the slice.
- **Lane D:** route `portal/situation.html`’s fields through `components/form_field.html` (segmented date, country
  combobox, tiles); translate §7; `templates/components/account_menu.html` «Sécurité du compte» → profile `#securite`
  (W2 request, still open).
- **Director:** the two recorded budget notes in §4 (main.css +29 B; the company need page’s three form modules);
  and «download action» on document rows (§3 of DECISIONS) collides with W3-C’s «the row is the link» / W-3 /
  Conditions-gate guards — kept on the piece’s page; rule if the row must carry it.
- **Steward:** 11 failures pre-exist on design-v5 `ece1eeb` in `tests/frontend/test_service_pages_w3_f2.py` (account
  pages now in the console since W2; the situation’s «what for» lines; the 400/500 titles) — owners B (the account
  frame: the test must read the console frame and its «Espace réservé › Mon compte › …» trail — B takes it in the fix
  pass), D (situation: the country is a select now), A/C (error pages); and `test_rtl_browser.py::
  test_every_arabic_public_page_fits_the_viewport` (54 < 55 routes since the hide gates).

## 9. Not done (by scope or by choice)

- «The verified chip uses its own mark»: a check-bearing symbol in a chip is a status context the O14 lint forbids;
  the conforme disc stays. Needs a Director ruling (e.g. a dedicated non-tick «verified» mark).
- Custom ILE SVG drawings for key concepts: none added this wave (the tile is the identity layer); candidates if wanted
  later — the referent (person + building), the review (sheet + lens).
- The «demande transmise» reference number: the done view carries no reference (a GET with `?k=`); adding one needs a
  view/session change in apps/enquiries — not a template change; left for a later slice.
- Contact / collaboration forms not viewable on the preview database (G2 closed there).

## 10. Round 1 improvements (v515-b-improve1, after quality round 1)

Committed together with round 2 (the round-1 work had stayed in the working tree; QA round 2 flagged it).

- **Steps engine.** A deep link or a reload opens the first step whose required fields are still empty, never a later
  one (`api.validate(steps[at], true)`). An error focuses the first field in error. Enter on a step that is not the
  last moves on and never sends (`stopImmediatePropagation`). The side rail's unreached links leave the Tab order
  (`tabIndex = -1`, `aria-disabled`). The head rail is `aria-hidden`: the live line and the legend speak.
  **Decision: a reload does not keep the typed values.** No `sessionStorage` or `localStorage` holds a personal
  datum (tested); the browser's own form restore is all there is.
- **The review** reads as a document: one part per step, each with its «Modifier». A required answer left empty is an
  error with its own way back (`is-missing`). It is written with `textContent` and never shows a password. Its
  module, `steps-review.js`, is fetched only when the last step is reached.
- **The minority is marked per step** (`_required.html`): «Le besoin» shows «obligatoire» on its one required field and
  no «facultatif» on its seven optional ones.
- **Words.** The script's words come from the catalogue. A word still in its French source carries `lang="fr"`
  (`ui_lang`, `msg_lang`, `step.lang`). `untranslated()` compares `gettext(msgid)` with the msgid itself.
- **Sign-up.** The fifth audience card spans both columns. The checklist holds only the two rules the browser can
  check, plus one quiet note for the rules only the server judges.
- **Console need.** The last row reads Précédent · Annuler · Créer le besoin, mirrored in Arabic.
- **Receipt.** It is a document: the filed mark beside the title, the route Reçue → En cours de traitement →
  Traitée with the first stop in gold, the caveat, one action. It has its own page-only sheet,
  `core/receipt.css`.
- **Empty state.** It uses the real lg glyph tile on a muted surface. Its sheet is page-only, `core/glyph.css`
  through `{% glyph_assets %}`, and is never part of main.css.
- **Three ILE drawings:** `ile-referent`, `ile-need`, `ile-review`. Each heads its step.

## 11. Round 2 improvements (v515-b-improve2, after quality round 2)

### Majors

- **M-1 (French in the live region of it/en/ar).** Root cause: `{% translate %}` doubles every `%` before its
  lookup, so a msgid with a placeholder never matched the catalogue, while `gettext()` did match. The new tag
  `{% script_word attr msgid %}` (`apps/core/templatetags/ile_forms.py`) calls `gettext()` itself and returns the
  value and `attr-lang="fr"` together, so the two can never disagree. It is used for the step position, the
  password count (`data-msg` + `data-msg-lang`), the combobox count and the textarea's «Il reste» count. The
  scripts set the node's `lang` from those attributes (`fieldcheck.js`: the summary and `setState(…, lang)`;
  `combobox.js`: the status). Measured: on `/ar/entreprises/recueil-des-besoins/` the attribute is now
  `data-msg-position="الخطوة %(n)s من %(total)s"`. An Arabic render test was added.
- **M-2 (lang on a container of translated words).** The rail's `<nav>` and the side's `<aside>` no longer carry
  `lang`. Each is named through `aria-labelledby` by a `<span hidden>` that carries `lang="fr"` while untranslated.
  The step labels inside keep their own language.
- **M-3 (the sign-up's head strip had no padding).** The night strip, with its `--pad` margins and padding, is
  scoped to `.formwork .steps-head`. Outside a formwork (the sign-up, beside the doorway's night) the head rail
  stands on the sheet. It has no slab. The tiles are paper with gold connectors, and the current tile is gold. The
  rail's inks are now custom properties (`--r-*`): night by default, paper on the sign-up and on the console's side.
- **M-4 (an empty night band under the console form).** Below 60rem, a steps formwork's side that holds no notes is
  not drawn (`:not(:has(.formwork__notes))`), and the panel gets its bottom corners back. The notes' top hairline
  is drawn only beside the panel (≥ 60rem), so the public form's night foot no longer opens on an orphan rule.
- **M-5 (composition).**
  1. The panel's content sits at ONE reading measure, `--measure: 46rem`, at the reading edge. The step rule, the
     fields, the review and the action row all end there, so «Continuer» sits at the fields' end. The formwork is
     side + measure wide (`max-inline-size: 71rem`), so the paper is no longer half empty at 1440, 1280 or 1024.
  2. Short fields are paired by meaning (`steps_pairs`), and only where the prescribed order already sets them side by
     side: «Secteur + Siège» and «E-mail + Téléphone» on the public form, «Langue + Niveau» on the console. «Nombre
     + Calendrier» are not next to each other in the prescribed order. Pairing them would reorder the form, so they
     are not paired (recorded).
  3. «Le besoin» shows its one required field, then «Précisions facultatives» on a hairline (`steps_more`). Under it
     the seven optional fields run two by two from a 48rem formwork, in their own order, with the free notes across.
     Their textareas start at two rows. The tower of six textareas becomes three rows plus the notes.
  4. The console's side is PAPER: `surface-sheet`, a gold rail, sticky, at its content's height. Only the console's
     own rail stays night, so two night columns no longer stand side by side. The panel keeps all its corners.
  5. Every field takes the full measure except the true short fields (a number, a date: 20rem), so the edge is no
     longer ragged in either direction.
- **M-6 (Icon Visual System).** The tile is a **paper seal**: the raised sheet falls to the page's sheet, with a
  `--line-rhythm` edge in place of the hard `--line-structure` hairline, a 1 px highlight inside the top edge and a
  faint under-shade. **The light** is 2 px along the top edge, from the reading corner to 55 %, fading at its end
  (`scaleX(.55)`, mirrored in Arabic). It runs to 100 % in 320 ms when its owner is hovered or focused: a link, a
  button, a card, or the step being filled (`.form-step:focus-within`). It takes 0 ms from the keyboard and has no
  transition under reduced motion (`html.rm` added). This motion contract is recorded in DESIGN_SYSTEM_2026.md §10
  (empty_state.html, «La tessera del glifo»). `ile-referent` is redrawn as ONE figure, the person standing in the
  doorway. The doorway or lens fill is 18 % (it was 12 %).
  **Not followed: the «round caps» advice.** It rests on a wrong premise. Every glyph of the sprite, the Lucide ones
  included, is drawn with square caps and miter joins by the one `.icon` rule (components.css §2; guarded by
  `test_icons::test_no_sheet_draws_a_glyph_with_a_thinner_hand_than_the_icon_rule`). The ILE drawings therefore
  already match the glyphs beside them. Changing the convention is a system-wide Director decision, not a lane-B
  slice.
- **M-7 (process).** Rounds 1 and 2 are committed together. The 21st rows went to lane A (§12). The targeted tests
  ran on l4 (§13). The lane server runs with `--noreload` and was restarted after every template change before each
  look.

### Minors

- The last-step row under 30rem: the primary has its own full row (`flex: 1 0 100%`), «Précédent» (icon) and
  «Annuler» share the row above, and «Annuler» is `btn--lg` (the same height as the primary).
- `.pw-rules__note` is aligned with the rule texts (`padding-inline-start: .875rem + s-2`) and set in `--text-2`.
- Receipt: the sheet is now really at the reading edge (`margin-inline: 0 auto`). The route's list is named
  «État de la demande» (an existing translated msgid; it was «Étapes»). «Traitée» is kept: it is the request's real
  end state in the team's register, not a promise, and the caveat follows.
- Forced colours: an unreached rail link is `GrayText`.
- **Budget (unit: KiB, gzip -9, measured with Python).** The steps' rails, review, navigation and console side moved
  out of `core/forms.css` into their own page-only sheet, `core/steps.css` (`v5/_steps.css`). It is linked once per
  response by `components/form_steps.html` (`{% steps_assets %}`), so a form without steps never carries it.
  | Asset | Size |
  |---|---|
  | `core/forms.css` | 5 101 B (≤ 6 144) |
  | `core/steps.css` | 2 298 B (≤ 3 072) |
  | `core/glyph.css` | 1 255 B |
  | `main.css` | 31 345 B (= the base; no rise) |
  | `fieldcheck.js` + `steps.js` | ≤ 6 144 B (tested) |
  | `combobox.js` | on its own §5.7 budget (≤ 3 KiB), fetched only where a long select is |

  **For the Director's register:** the unit is the KiB. The combobox has its separate budget, so round 1's M-6 is
  not reopened.

### New msgids for lane D

`Précisions facultatives`. Still untranslated, and marked `lang="fr"` until lane D's catalogue pass:
«L’entreprise et son référent», «Le besoin», «Vérification et envoi», «Vérification», «Qui êtes-vous ?», «Identité et
mot de passe», «Après l’envoi», «Étapes du formulaire», «À savoir avant l’envoi», «%(n)s règles sur %(total)s
respectées.» (python-format), «obligatoire».

## 12. Request to lane A: COMPONENT_PROVENANCE.md rows (lane B, V5.15 W3, rounds 1–2)

| 21st id | Name | Family | Use |
|---|---|---|---|
| 23576 | Wizard Steps | multi-step | **taken**: ported to `static/js/src/steps.js` (square tiles, filling connectors, direction-aware slide), no tick on a done step |
| 28546 | Stepper with Square Badges | side rail | reviewed: the square badge confirms the tile; its checkmark is refused (O14) |
| 8864 | Registration Stepper | side rail | reviewed: the accordion layout is refused (all fields stay in the page) |
| 3735 | (stepper candidate) | side rail | reviewed, not taken |
| 28550 | Segmented Progress Pill Stepper | head rail | reviewed: the pill is refused; the segment idea backs the head rail's bars |
| 29801 | Progress Bar Stepper | head rail | reviewed: a thin bar under each step backs the head rail's connectors |
| 29865 | Content Stepper | multi-step | reviewed: checkmark and spinner states refused (O14, no fake wait) |
| 7974 | (stepper candidate) | side rail | reviewed, not taken |
| 8281 | Multi-Step Form | multi-step | reviewed: the framer-motion container is refused (no React island; WAAPI) |
| 8597 | Order Status Card | receipt route | **taken (structure)**: the vertical process timeline becomes the receipt's three stops |
| 37491 | Delivery progress | receipt route | **taken (structure)**: stage list, first stage lit; no delivery vocabulary |
| 7710 | Order History | receipt route | reviewed: the dated timeline is refused (the receipt carries no date) |
| 8205 | Order Status Tracker | receipt route | reviewed, not taken (item summary, tracking actions) |
| 641 | Order tracking | receipt route | reviewed, not taken |
| 26902, 28381, 28384 | (route candidates) | receipt route | reviewed, not taken |
| 23542 | Password Strength | password checklist | adapted: the rule list, no strength meter |
| 19201 | File Dropzone | upload | adapted: its geometry over the native input |
| 23564 + 27356 | Inline Validation + Primitive Input | field states | adapted: server words, the live row |
| 28299 | Icon Feature Grid | glyph tile | the icon-in-a-container idea only |
| 27366, 24509, 29986 | Primitive Badge, Icon Only Badge, Styled Badges | glyph tile (round 2) | reviewed for the seal material: the gradient-outline and highlight ideas back the paper seal; the glow and pulse are refused |
| 18266 | Empty Background | empty state | adapted: muted surface + lg tile + one action |
| 28496, 22162 | File List Item, Table with Filters | document rows | adapted (§3) |

W2's rows are still missing too: Floating Label 23566, Combobox 34726, Calendar 34713, Icon Card Radio Group 28351.

## 13. Finishing round F1 (v515f-b-improve1, after quality round 3)

design-v5 `7f2a02d` (lanes P2/P3: special-category guard, privacy states, ownership) merged first, clean. No
conflicts, so no compliance guard was touched.

### Round 3's findings

- **M-1 «Après l’envoi» hairline (fixed).** `.formwork .formwork__notes { margin: 0; border: 0; }` beats base.css's
  `ul[role="list"]` rule (0,1,1). The 60rem night rule (0,4,0) still draws the rule between the rail and the notes.
  Measured at 1024/768/390/360 (fr) and 768/390 (ar): `border-top: 0px`, `margin: 0`, notes 32px from the side's
  top (it was 64px of void). Lane B's other lists have no `role="list"` (steps rail, review, receipt route, pw-rules),
  so they do not inherit the rule.
- **M-2 Arabic French-fallback heads (fixed).** `[dir="rtl"] :is(.form-step__title, .formwork__note-title,
  .form-step__subhead, .form-review__title)[lang]:not([lang="ar"]) { text-align: end; }`. `direction: ltr` is kept,
  so punctuation does not move. Measured in ar at 390: title text 184–271 beside its tile at 287; «Précisions
  facultatives» 191–331 on the right edge; «Après l’envoi» 206–287 beside its tile at 299. At 768 and 1440 the same.
- **M-3 «Le besoin» composition (fixed by meaning, not by `:has`).** The form names the like pairs in `steps_pairs`:
  Qualifications+Expérience and Langues+Formation. These are the two pairs of text areas already adjacent in the
  prescribed order, so nothing is reordered (the test still reads back `DATA_FIELDS`). The details are one column of
  rows: Nombre alone at 20rem · Q+E · L+F · Calendrier alone at 20rem · Notes across. A single-line detail alone
  keeps `max-inline-size: 20rem`. Measured at 1440/1280/1024/768 (fr, it, en, ar): in each pair both fields and both
  text areas share top and bottom (1384/1486 · 1510/1612 at 1440). Below 36rem the pairs stack.
- **M-4 Empty state (redesigned as the page's opening statement).** It no longer has a surface. The xl tile (72px)
  stands in a doorway: a 1px `--line-rhythm` arch, 88×120px, behind it at the reading corner, fading into the page
  at its foot (the portico's figure). The title is at `--t-entry` and the sentence is in `--text-2` at the text
  measure. The view's own action stays a secondary. The tile's light runs from 55% to the far corner once on
  arrival (320ms) and stays there; it does not run under reduced motion or `html.rm`. In forced colours the arch is
  `CanvasText`. No new copy. Measured on Mes demandes and Communications for a fresh account: fr 1440/390, ar
  1440/390 (the arch and tile at the right edge), it 1024, fr 1440 reduced motion (`animation: none`); no overflow.
  `.portal__main .empty-state { max-inline-size: none }` (the console's rule) still applies.
- **m forced colours (fixed).** `.steps-rail__item .steps-rail__link[aria-disabled="true"] { color: GrayText; }`.
  Measured: «2 Le besoin» and «3 Vérification et envoi» are no longer LinkText (0,0,159).
- **m password note (fixed, cause found).** Round 2's fix was right but lost to the entrance's
  `.varco .form-field__help ul { padding-inline-start: 1.25em }` (0,2,1). That rule pushed the discs 20px in, so
  the note looked misaligned. Now `.form-field__help.pw-rules > .pw-rules__list { padding: 0 }`, and the note and
  rule share `--pw-disc` and `--pw-gap`. Measured at fr 1440: rule text 831, note 831. At ar 390: rule text right edge
  337, note right edge 337.
- **m consent painted on Tab (fixed; Director to ratify).** fieldcheck.js: an untouched checkbox or radio is not
  checked on blur. It is checked once changed, and at «Continuer» and at the submission. Measured: Tab past the
  untouched consent gives 0 errors; check then uncheck gives the error. **Request to the Director:** §5.5 says
  «on blur». This narrows it for a box or choice nobody touched, because a box has no half-typed value. Ratify it
  or revert the 3 lines.
- **m lane D msgids (handed over again).** «Précisions facultatives», «%(n)s règles sur %(total)s respectées.»,
  «Vérification», «L’entreprise et son référent», «Le besoin», «Vérification et envoi», «Après l’envoi», «Vos
  données», «Étapes du formulaire», «À savoir avant l’envoi», «Qui êtes-vous ?», «Identité et mot de passe»,
  «obligatoire». No new msgid this round.
- **m /entreprises/ (fixed).** Above 75rem, a chapter whose body holds a formwork puts its head above and the
  formwork across all 12 columns. The head stays non-sticky, at 60rem. Measured at fr 1440: formwork 92–1228, the
  night side sticky at 92–388. At ar 1440 the side is on the right. At 1280 the same. At 768 the night foot is
  clean.
- **m glyph light at 1x (fixed).** `.glyph-tile::after` has a faint underglow of the light's own colour (30%).

### Also fixed

- `steps.js` now asks the one motion gate (`reducedMotion()`, `play()` from motion.js) and still cuts motion from
  the keyboard. `test_script_motion_gate` had failed twice on this branch.
- `test_forms_v515_b.py` sets `DJANGO_ALLOW_ASYNC_UNSAFE` like the other browser modules. Run alone, its two
  Chromium tests failed in setup (SynchronousOnlyOperation).

### Headed check (Chromium 1234, headed, under the lock; lane server 8784, `ILE_DESIGN_PREVIEW_PORT=8784`)

`C:/tmp/ile_v5_council/evidence/v515/b/f1_review.py` → `f1_results*.json`, `f1_*.png`. Coverage:
- the public form at fr 1440/1280/1024/768/390/360, ar 1440/768/390, it 1024 and en 768: step 1, step 2 and the
  night foot;
- the walk at fr 1440 with and without reduced motion;
- the sign-up checklist at fr 1440 and ar 390;
- the empty states as listed above;
- /entreprises/ at fr 1440/1280/768 and ar 1440;
- forced colours, and the glyph at 1x.

No page errors, and no horizontal overflow anywhere. The 404s in the empty-state runs are the probe's wrong
`/documents/` address, not the product.

Self-scores against V5.15 §26:
| Family | Score |
|---|---|
| Formwork | 4 (Arabic heads on the reading edge, no void in the foot, the night side on /entreprises/) |
| «Le besoin» | 4 (like with like, rows aligned) |
| Empty state | 4 (an opening statement in the doorway, not a box) |
| Other families | unchanged |

### Tests (l4, one pytest at a time)

- Non-browser: 938 passed (forms_v515_b, form_system_v512_b, icons, o14, apps/enquiries, static_assets,
  dashboard_w3_b, design_showcase, the token and reduced-motion files) + motion gate, rules and v512 (all pass after
  the steps.js fix).
- Updated, with no guard weakened:
  - the «Le besoin» rows: the exact like-pairs, and 4 pairs on the page;
  - the empty state: xl tile, no surface, the arch, the light still under `html.rm`;
  - the steps' motion assert: the gate import instead of a private media query.
- Browser (headless shell, under the lock):
  - `test_forms_v515_b test_entrance_form_w2_b test_rtl_browser_entrance`: 47 passed. The 2 failures were the
    module's missing `DJANGO_ALLOW_ASYNC_UNSAFE` (fixed).
  - Then `test_forms_v515_b test_form_system_v512_b -m browser`: 3 passed.
  - `test_rtl_browser -k "french_fallback or arabic_form_is_right or reserved_area"`: 3 passed. The Arabic
    empty-submit check was stale since round 1, because the address no longer opens a step past the first incomplete
    one. It now posts the empty form as it is and asserts at least 5 errors. That makes it stricter.
