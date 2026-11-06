# V5.12 — Lane B, wave W2 (label v512-b-w2): icons, the form system, the account shell

28 Oct 2026. Branch `v512-b-w2`, from design-v5 `6251475` (v512 W1 merged). Scope: the W2 row of DECISIONS.md «Waves»
for B — the 12 new symbols and the sprite split; the field system (one partial, the states, fieldcheck, choice cards,
combobox, date, number); the account shell. Not merged into design-v5.

Owner answers Q1–Q8 (DECISIONS §12–13) do not touch lane B's W2 items. Q7 (organisation experience) is D's; B
supplies the glyphs and the components listed in §6 below.

## 1. What changed

### Icons (commit `269254d`) — DECISIONS §4

| Where | Change |
|---|---|
| `static/icons/src/` (12 new) | Lucide 1.48.0 (ISC; none Feather-derived): `presentation`, `list-checks`, `file-search`, `book-text`, `earth`, `user-cog`, `messages-square`, `message-square-text`, `files`, `shield-check`, `mic`, `mail-plus` (it exists in 1.48.0). The 12 % tone on the board, page, cover, bubbles, front sheet, shield, capsule. |
| `apps/core/icons.py` | Registered (tier, floor, meaning, group «Concetti V5.12»). **Sprite split**: `SPRITE_DOMAIN`, `SPRITES`, `DOMAIN_SYMBOLS`, `SPRITE_OF` (symbol → file), `CHROME_SPRITE_MAX_BYTES = 31 049` (ratchet). `CHECK_BEARING` += `list-checks`, `shield-check` (both draw a check; their only seats named). `TWINS` += {list-ordered, list-checks}, {messages-square, message-square-text}, {document, files, file-search}; `shield-check` joins the shield twins. Concepts: training body / training phase / training pathway / «Formation avant le départ» → `presentation` (`book-open` is the Academy's alone, `university` the university's alone); the operator's dispatch desk → `user-cog` (was the back office's `settings`). |
| `CHAPTER` / `CHAPTER_OF` | The W1 waiting list closed: «Étapes» (pathway sheet, diplomas) and a result's next steps → `list-checks`; «Ressources» and «Sources officielles» → `book-text`; the contact form → `message-square-text`; the newsletter → `mail-plus`; the Forum speakers → `mic`; the discussions → `messages-square`; «Documentation généralement requise» → `files`. |
| `scripts/build_icons.py` | Emits **two sprites** by `SPRITE_OF` (aliases live in their target's file); refuses a chrome sprite ≥ 31 049 B. |
| `apps/core/templatetags/ile_core.py` | `svg_icon` writes each `<use>` against its own sprite (`_sprite_url(icons.SPRITE_OF[symbol])`, content-hashed per file). |
| `docs/design-v5/ICON_LICENSES.md` | 12 donor rows, 76 donors, two sprites, §4 entry. |
| Consumers of the sprite file | Tests and `scripts/regen_design_inventory.py` read both files. |

### The form system (commit `751be04` + this commit) — DECISIONS §5

| Where | Change |
|---|---|
| `templates/components/form_field.html` | **The one field partial.** Label always visible + «facultatif» on optional fields (no asterisk anywhere; `required` kept on the controls), control plate with a **leading glyph** (e-mail `at-sign`, phone `phone`) and a **trailing status slot** (error `circle-alert`, read-only `lock`; from the inline check `warning` / `check`), help line, **textarea counter** (limit from `max_length`), **one message row** (`aria-live=polite`; the server's `_error` box keeps `role=alert` and the id Django's `aria-describedby` names). Dispatches radio/checkbox groups → `choice_cards.html`, dates → `date_field.html`, numbers → `number_field.html`; a select of > 15 options gets `data-combobox`. |
| new `_field_label.html`, `_field_msg.html`, `_optional.html` | The label and the message row, shared by every field component and the allauth adapter. |
| `enquiries/partials/form_field.html`, `allauth/elements/field.html` | Thin adapters of the same anatomy (the allauth one from `attrs`). `news/_newsletter.html`: the consent is the partial (its locked label keeps its `lang`). The «Les champs marqués d’un astérisque (*) sont obligatoires.» notes removed (enquiries shell, company forms). |
| new `apps/core/templatetags/ile_forms.py` | `{% field_ui %}` (kind, optional, glyph, read-only, count, combobox, **the server's own messages** as `data-msg-*`, the password pair), `{% form_assets %}` (the page-only sheet + module, **once per response**, only where a field renders), `choice_options`. |
| new `static/js/src/fieldcheck.js` | Inline check: on blur, then on input once touched; the server's words; never blocks typing or submit; a server error stands until the value changes. **Warning**: Caps Lock on a password; a textarea within 10 % of its limit. **Success** only for a confirmed value: the two passwords equal. Enhances dates (three segments, the native input kept as the hidden ISO value), numbers (− / + stepper, disabled at the limits), and lazy-loads the combobox. Delegated events; `htmx:load` aware; no innerHTML, no inline style. |
| new `static/js/src/combobox.js` | ARIA 1.2 combobox over the native select (which keeps the name and is submitted): type to filter (case- and diacritics-insensitive, «starts with» first), ArrowUp/Down, Enter, Escape restores, Alt+ArrowDown; leaving with an unknown text restores the choice; polite count. |
| new `static/css/v5/_form.css` → `apps/core/static/core/forms.css` (page-only) | Optional tag, slots, M10 (message row 0fr → 1fr in 160 ms, edge 120 ms; 0 ms from the keyboard and under reduced motion), warning / success / read-only states, counter, combobox list and chevron, date segments, number stepper, forced colours. |
| new `static/css/v5/_choice.css` + `components/choice_cards.html` | **Choice cards** (21st «Icon Card Radio Group» 28351, geometry only): native input over the whole card, optional glyph disc, title, description, the person's check scaling 0.8 → 1 with the edge and the tint in 120 ms (M14). Grid follows the form's measure (`auto-fill, minmax(min(100%, 10.5rem), 1fr)`). `option_cards.html` is now an alias; the questionnaire's step (`orientation/_step.html`) draws choice cards (`wizard.css` imports `_choice.css`; its old plate rules removed). |
| `apps/accounts/forms.py` | Sign-up «Vi registrate come» = **audience cards with glyphs** (person, building, institution, university, professional's briefcase — registry symbols). |
| new `apps/core/countries.py` + `LICENSE-CLDR.txt` | 250 countries, ISO alpha-2, CLDR 48.0 names in fr/it/en/ar (generated once from ICU 78.2 via Node `Intl.DisplayNames`; Unicode License v3 verbatim); `choices(lang)`, `name()`, `match()` (free text in any of the four languages → code). |
| `apps/accounts/profile_forms.py` | Nationality and countries of residence are `CountryField` (ISO codes — what `rules.engine` reads; earlier free text mapped back by `match`). |
| `apps/companies/forms.py` | The company's country is the CLDR select; autocomplete tokens (`tel`, `organization-title`, `address-line1`, `postal-code`, `address-level2`, `address-level1`). |
| `apps/accounts/static/accounts/entrance.css` | The asterisk-hiding rule removed; the label-row grid places the message row in row 3. |

### The account shell — DECISIONS «Lane B» scope, acceptance 6

| Where | Change |
|---|---|
| new `apps/accounts/shell.py` | `frame(request)`: the console for a signed-in account whose reserved area is open (or staff), the public frame otherwise (anonymous password reset, area switched off). `console_context`: the space's rail (person, or company for a company account) and the trail «<space> › Mon compte › <section>». |
| `allauth/layouts/manage.html` | `{% extends request|account_frame %}` (builtin filter in `ile_core.py`: `{% extends %}` must be first). |
| new `allauth/layouts/_console.html` | `portal/base_portal.html` + the account's own grammar (`conto`, sections list at the reading edge) inside the workspace. |
| `templates/accounts/profile.html` | «Sécurité du compte» overview: e-mail verified / à vérifier (chip), password, two-factor with **`shield-check` when on, `shield` when off** + chip. |

## 2. What the owner sees in the preview (once merged)

- **/fr/compte/signup/**: «Vous vous inscrivez en tant que» as five cards with their audience glyph (two columns,
  one on a phone; AR mirrored); leave the e-mail wrong → the edge, the mark and «Saisissez une adresse de courriel
  valide.» under it, as you leave; type the same password twice → «Les deux mots de passe correspondent.» (its words and
  a teal edge; no script draws a check, O14); no asterisk on any label.
- **Every form** (contact, company needs, collaboration, newsletter, profile, help desk, community, Forum
  registration, depot fields): «facultatif» on the optional fields only; the e-mail and phone glyphs; the error mark
  in the field's end; the message row opening smoothly; a message counter on long texts.
- **/fr/compte/profil/, /email/, /password/change/, /2fa/** (signed in): inside the console, with the rail and
  «Espace réservé › Mon compte › …»; the security section with the shield; «Pays de résidence» is a searchable list
  (type «mar» → Maroc first; Arabic «مغ» → المغرب).
- **Questionnaire** (/fr/orientation/…): the answers are the same cards as everywhere, with the check scaling in.
- **Icons**: pathway sheet «Étapes» checklist, «Ressources» legal book, «Documentation» stack of files, /contact/
  form bubble, newsletter mail-plus, Forum speakers mic / discussions bubbles; training glyph is a presentation
  board; the operator's dispatch row a person with a cog.

Evidence (lane server 8784, Chromium under the lock, reduced motion): `C:/tmp/ile_v5_council/evidence/v512/b-w2/`
(signup, signup-inline, cards, contact, profile, email, situation, combo — fr/ar × 1440/390; `measure.json`,
`measure2.json`). All 16 page×lang×width probes: no horizontal overflow, 0 asterisks, one h1, the console rail on
every account page, `core/forms.css` only where a field renders.

## 3. Budgets

| Asset | Before | After |
|---|---|---|
| `static/img/icons.svg` (chrome) raw | 30 878 B | **17 039 B** (< 31 049 ratchet) |
| `static/img/icons-domain.svg` raw | — | 18 991 B (< 32 768) |
| `main.css` gzip | 31 149 B | 31 149 B (unchanged; ceiling 31 414) |
| `core/forms.css` gzip (page-only) | — | 2 304 B (≤ 6 KB) |
| `orientation/wizard.css` gzip (page-only) | 4 175 B | 4 700 B (≤ 6 KB; imports `_choice.css`) |
| `accounts/entrance.css` gzip | 4 861 B | 4 851 B |
| form-page JS gzip (`fieldcheck.js` + `combobox.js`, form pages only; combobox only with a long select) | — | 2 975 + 1 486 = 4 461 B (≤ 6 KB) |

No npm dependency, no animation library. The JS/CSS dist was rebuilt with `npm run build` (node_modules is a
junction to the main checkout's, not committed). `static/js/dist/piece-drawer.js` changed in the rebuild only
(same size; a chunk reference) — the steward rebuilds from clean anyway.

## 4. Tests

New: `tests/frontend/test_form_system_v512_b.py` (12: no asterisk / optional minority; anatomy and ids; the server's
messages; choice cards + the questionnaire; sign-up audience cards; date/number/combobox hooks; assets once per
response; budgets; M10/M14 + reduced motion + logical properties; countries; ISO codes in the profile; form glyphs in
the chrome sprite); `tests/frontend/test_account_shell_v512_b.py` (7: the four account pages in the console, the
trail, the public frame for anonymous / closed area, the security shield). `test_icons.py` +1 (the split) and its
sprite tests on both files; `test_chapter_marks.py` (contact form, Étapes, Ressources, Documentation marks).

Updated (stale by the change, guards kept): `test_journey_w3_d.py` (training glyph), `test_orientation_w3_f1.py`
(the sheet's import list), `test_components_w1_c.py` / `test_design_docs.py` / `test_entrance_form_w2_b.py` (no
asterisk; the errors in the message row; the label-row grid), `apps/accounts/tests/test_profile.py` (country =
ISO code), sprite readers (`test_templates_static`, portal/ecosystem compliance, `test_design_docs`,
`test_static_assets`, `test_svg_wellformed`, `test_layout`). `DESIGN_SYSTEM_2026.md` §10: five component sections,
44 files.

Runs (TEST_DATABASE_URL `test_ile_v5_l4`, one pytest at a time):
- icons + sprite consumers: `test_icons.py test_chapter_marks.py test_journey_w3_d.py` 68 passed; templates_static,
  portal/ecosystem compliance, design_docs, static_assets, svg_wellformed, layout, regen_design_inventory —
  363 passed;
- forms: `test_form_system_v512_b.py test_orientation_w3_f1.py apps/orientation/tests/test_wizard.py` 61 passed;
  `test_design_docs.py apps/accounts/tests/test_login_form_w2_b.py apps/accounts/tests/test_profile.py
  apps/companies/tests/test_no_people.py apps/companies/tests/test_views.py test_entrance_form_w2_b.py
  test_components_w1_c.py test_form_system_v512_b.py test_account_shell_v512_b.py` — 192 passed, then the 3
  remaining fixed (incl. the browser test of the entrance's error placement, re-run under the Chromium lock);
- broad non-browser regression (`apps/community apps/helpdesk apps/documents apps/forum apps/orientation apps/portal
  apps/news apps/enquiries apps/accounts apps/companies` + static/bundle/O14/icons/page-integrity/console-shell
  tests): 1501 passed, 5 failed + 5 setup errors; the errors were `caplog` missing because that run disabled the
  logging plugin (re-run normally: pass); the 5 failures fixed — O14 allow-list (the choice cards, the
  questionnaire, the security overview's `shield-check`), no check drawn by a script (the confirmation is words
  + edge), a forbidden word in a comment, the situation test posting a free-text nationality (now an ISO code),
  the AR fallback of «facultatif» (now `lang="fr"` until D translates it, `components/_optional.html`);
  re-run of those files + accounts + design docs: 501 passed, then the last 2 fixed (30 passed);
- browser, under the lock: `test_orientation_browser_w3_f1.py` + `test_rtl_browser.py -k "wizard or orientation"`
  12 passed (after the questionnaire's label was given the card's target again); `test_entrance_form_w2_b.py -m
  browser` 34 passed.

## 5. New translatable strings (for lane D — no .po edited)

`facultatif` (shown with `lang="fr"` until translated) · `La touche Majuscules est activée.` · `Les deux mots de passe ne correspondent pas.` ·
`Les deux mots de passe correspondent.` · `Il reste %(n)s caractères.` (python-format, the script replaces `%(n)s`) ·
`Aucun résultat.` · `%(n)s résultats.` · `Jour` · `Mois` · `Année` · `Diminuer` · `Augmenter` ·
`vérifiée` · `à vérifier` (may exist) ·
`Sécurité du compte` (exists, the account menu) · `Adresses e-mail`, `Mot de passe`, `Authentification à deux
facteurs`, `Mon compte` (exist; now also in the console trail).
Dropped by this branch: `Les champs marqués d’un astérisque (*) sont obligatoires.` (no template uses it any more).
Request: the profile's phone help still says «Facultatif — utilisé uniquement pour le suivi de vos demandes.» (kept,
it is translated); once D adds `Utilisé uniquement pour le suivi de vos demandes.` in four languages, replace the
help_text in `apps/accounts/profile_forms.py` (the «facultatif» tag already says it). The country list's empty
choice is «—» (no new string).
Country names need no catalogue: they are CLDR's, in `apps/core/countries.py`.

## 6. Requests to other lanes

- **Lane A** (owner of `templates/documents/partials/depot.html`): its label still writes
  `<span class="form-field__required" aria-hidden="true">*</span>` — please drop it (DECISIONS §5.3); `v5/field.css`
  keeps the `.form-field__required` rule only for that one line. Also: `COMPONENT_PROVENANCE.md` rows from B —
  Floating Label 23566 (hint/counter row + 120 ms invalid transition only; the label stays above), Combobox 34726
  (behaviour, ARIA 1.2 pattern, over a native select), Calendar 34713 (look only: segmented d/m/y, no grid), Icon Card
  Radio Group 28351 (geometry: disc + title + description + check), Status Badge 521 and Empty Background 18266 (W3),
  File List Item 28496 and Table with Filters 22162 (W3).
- **Lane C**: `templates/forum/partials/registration_form.html` writes «* Champs obligatoires» with an asterisk —
  please drop the note (the fields say «facultatif» now). The chapter-mark retune of W1 (`.chapter__mark` 2-unit
  share) still applies.
- **Lane D**: (a) `templates/components/account_menu.html`: «Sécurité du compte» could point to
  `{% url 'accounts:profile' %}#securite` (the overview) rather than straight to the 2FA page; (b) the D-owned
  `portal/situation.html` renders its date and nationality outside the partial — routing them through
  `components/form_field.html` gives them the segmented date and the country combobox (the form fields are already
  `CountryField`, the values ISO codes); (c) Q7 organisation spaces: glyphs available — `institution`, `university`,
  `presentation` (training body), `files` (documentation), `book-text` (legal sources), `messages-square`
  (discussions), `file-search` (to verify), `user-cog` (operator); components — `choice_cards.html` (with
  `choice_glyphs`), the field partial, the account shell; when the organisation spaces get their own space key,
  `accounts/shell.py` `console_context` needs one line to pick that rail; (d) the msgids of §5;
  (e) `templates/dev/designpreview/specimens/icons.html` names `settings` for the dispatch — now `user-cog`.
- **Steward**: `scripts/check_ownership.py v512-b 6251475` lists the new and touched files (components, allauth
  layouts, enquiries partials, orientation step, tests) as outside the v512-b slice — as in W1, please record them
  in the manifest for v512-b; `static/js/dist/**` and `static/css/dist/**` are generated.

## 7. Not done (by scope or by choice)

- W3 items: multi-step forms (company need, public needs, sign-up steps), the live password checklist, document rows
  and filters, the upload drop zone as the default `FileField` rendering (§5.10), the two-column form layout with the
  sticky aside (§5.13), the «demande transmise» confirmation (§5.15).
- Forms rendered by hand in D's portal templates do not get the new anatomy until they include the partial.
- The `settings` symbol stays in the sprite (the dev specimen board names it) though no product page draws it now.

## Fixes after review (v512-b-fix-w2)

One finding, minor (`templates/components/_field_msg.html`; `apps/core/templatetags/ile_forms.py` `form_assets`):

1. **One announcement channel.** The field's message row is `aria-live="polite"` and it held the server's error
   with `role="alert"` — an alert inside a live region can be said twice. The row is now the field's only channel:
   the server's error is `<div class="form-field__errors" id="…_error">` without a role, in
   `components/_field_msg.html` and in allauth's `elements/field.html`. The summary at the form's head stays the
   alert and takes the focus; the field's error is read when the field is reached, through `aria-describedby`;
   `fieldcheck.js` writes its own messages into the same row and never sets an alert role. `fieldcheck.js` now
   recognises the server's errors by `:not([data-kind])` (the ones it did not write) instead of `[role=alert]`.
   `docs/ACCESSIBILITY.md` §5 (live regions) and §6 (the field contract: the sample markup, «Errore collegato»)
   say so. Out of the partial and not changed: D's `portal/situation.html` and `documents/partials/depot.html`
   render their own errors with `role="alert"` outside any live row — no double channel there.
2. **Fields inside a fragment fetched by script.** `{% form_assets %}` puts a module script where the first field
   is; a fragment parsed with DOMParser and inserted (the preview drawer takes the piece page's `<article>`, which
   holds the review form) carries that script inert. Documented in `ile_forms.py` and at the head of
   `fieldcheck.js`: such fields still submit and the server still judges; for the inline check the host module
   imports `fieldcheck.js` and dispatches `fields:load` on the inserted root — `fieldcheck.js` now listens for it
   as it does for `htmx:load`. htmx swaps (the orientation step) are unaffected: htmx runs the scripts it swaps.
   **Request to lane A** (owner of `piece-drawer.js`): after `body.replaceChildren(node)`, when the node holds
   `[data-field]`, `import("./fieldcheck.js")` and `node.dispatchEvent(new CustomEvent("fields:load", { bubbles: true }))`.

Tests: `test_form_system_v512_b.py::test_one_announcement_channel_no_alert_inside_the_live_row` (new); the field-error
assertions of `test_components_w1_c.py`, `test_design_docs.py` (incl. the ACCESSIBILITY.md fragments),
`test_form_system_v512_b.py`, `apps/accounts/tests/test_login_form_w2_b.py` now assert the error without a role.
`npm run build:js` — only `static/js/dist/fieldcheck.js` changed. Runs (TEST_DATABASE_URL `test_ile_v5_l4`, one
pytest at a time, `-m "not browser"`): form system, components W1-C, design docs, login form, profile, entrance,
account shell, O14, wizard, static assets — 205 then 101 passed after the fixes; `apps/community apps/helpdesk
apps/enquiries` + profile/entrance/shell/O14/wizard/static assets — 357 passed. No browser run (no visual change).
