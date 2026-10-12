# W1-C — core components · senior review (one pass, V5.5)

Italy Legal Entry™ · design V5 · V5.4 plan §1.2, §1.4, §1.6, §1.8, §1.15, §3.3 item 7 · V5.5 delivery mode · label
**w1-c-review** · 9 October 2026 · branch `v54-w1-c` at `04f43e9` (clean worktree), reviewed on its own server
**127.0.0.1:8888** (`ile_v5_l8`, `ILE_REFERENCE_DATE=2026-10-03`; the preview routes on only for the chip board). I built
nothing; one pass, design + UX + taste together, against the owner's bar («credible alongside excellent international
digital products») and the settled direction (plan §1, DL54-45 … 51).

## Verdict — SHIP_AFTER_FIXES

Buttons, fields, chips, cards, notices and the disclosure read as one ILE system on the real pages, in French and in
Arabic, from 1440 to 360: flat primaries, «la lastra» at 16 px on a hairline, eight registers said three times without
colour, cards by purpose. The chip «i cerchi» is the strongest piece — an authored family, not a badge kit. Four things
visible on real pages are below the bar; each is a few lines inside the family's own files, and each was tried in the page
before being asked for (§ «The fixes, tried»): the password rules of the sign-up are raw HTML and pull the field's focus
rule away from its field (M1); the show / hide control eats the password's plate on phones (M2); a public form's action is
shorter than its fields and never takes the column on a phone (M3); a chip is stretched into a bar on two phone lists
(M4). No P0: no broken page, no wrong direction, nothing unusable, no data or security problem.

## What I looked at

- **The seven pages of the brief** — login, sign-up, contact form, person dashboard, «Mes pièces», a case file, FAQ — fr
  and ar at 1440 / 1366 / 390 / 360: 56 full-page captures, each with a probe of every button, field, chip, card,
  notice and row (box, type, colours, contrast, radius, shadow, targets under the floor). **The phone widths again,
  viewport by viewport** (43 scans): a full-page capture re-emulates the device and loses `(pointer: coarse)`, so it
  draws the 44 px targets at 36 px — the probes were right, the pictures were not.
- **States, on those pages and on the showcase** (158 jobs): keyboard focus, pointer focus, hover, press, filled,
  checked, the empty submit's errors on the whole page (login, sign-up, contact, company needs), the busy face (every
  POST answered 204 at the network — W1-D's method; no view is reached), reduced motion, forced colours. No credential
  was typed anywhere: the password fields stayed empty.
- **120 more cells** on 39 page types that draw the family: «Formation», the doors' related lists, the pathway's and the
  diplomas' tags, «Demande transmise», the Forum's closed registration, the account pages, the upload and a requirement,
  the company's dashboard, needs and form, the helpdesk (person and professional), the academy, the bridges; the
  showcase `/_design/` in both directions at the four widths; the chip board `/__design-v5/specimens/chips/` (three
  grounds, night at 2×, 390, forced colours).
- **A bench of the states no page and no board draws** (soft and icon buttons, radio, switch, disabled / read-only /
  warning fields, multiple select), built in the page with the product's own classes.
- **The code**: the six sheets of `static/css/v5/`, `components/{form_field,chip,badge,card,notice,tabs}.html`, the
  `{% chip %}` tag (its escaping), `apps/core/chips.py`, `initTabs`, the submit hook; NOTES.md; DL54-45 … 51.
- **Tests** — the family's six source modules (`test_components_w1_c`, `test_chips_cards_w1_c`, `test_chips_registry`,
  `test_state_chips_carry_a_register`, `test_o14_lint`, `test_css_bundle_is_current`): **252 passed in 1.7 s**, no
  database, no browser. `scripts/check_ownership.py w1-c design-v5`: 23 inside, 6 slice, 14 generated, **60 outside —
  exactly DL54-50's and DL54-57's**, for the merge step to record. Not run: the browser suites and the full suite (I
  changed nothing; the implementer's runs are in NOTES.md).
- Sessions minted with `Client.force_login` by a scratch script outside every repository (no password used, typed or
  stored), revoked at the end. One browser at a time; the benchmark lock was never present; no run ended on «Target
  crashed».

## What is at the bar (measured, not assumed)

- **Health.** 379 recorded captures: every expected status (377 × 200, the two 403 by design), 0 CSP violations, 0 console
  errors on a product page, 0 horizontal overflow on a product page. On the 56 cells of the brief no control of the
  family is under its target floor (24 px fine, 44 px coarse).
- **Buttons.** 278 boxed buttons on the product pages: 0 with a background image, 0 with a shadow, all at 4 px, at
  36 / 44 / 52 (50 where a label takes two lines on a phone). Hover one step darker, the press 1 px down, the one ring on
  every variant and on night, disabled by colour and cursor, borders carrying the hierarchy in forced colours. A waiting
  button keeps its own surface and holds the key (login, contact). Flat means flat.
- **Fields.** 372 text controls: typed text 16 / 24 everywhere, a 1 px hairline at ≥ 3.37 : 1, 4 px corners, no shadow;
  52 px on public pages, 44 px in the console; label 14 / 20 at 8 px. An error is a doubled edge, a drawn mark and the
  words, and the summary takes the focus. The rule draws in 200 ms for a pointer, at once from the keyboard, 0 s under
  reduced motion (read from the page).
- **Chips.** 272 product chips on 19 page types, seven registers on the lane's data and «blocco» on the board: every one
  with its register and its mark, 24 px on one line, words ≥ 5.38 : 1, marks ≥ 3.28 : 1; right on stone, sheet and night;
  mirrored correctly in Arabic (mark at the reading edge, gauge at the end); legible under forced colours. «Valide» is
  ink and a plain disc. This is original work and it is the product's own.
- **Cards.** The record card (sheet, hairline, 8 px, level 1) on «Formation» and the related lists: titles at 20 / 28
  where V4 had 13 px, second actions on one line, hover = a stronger hairline and an underline, nothing lifts. No stat
  card and no board class exists. The action card and the summary strip are right on the showcase and the board.
- **Notices.** Wash, rule, mark, title — solid, dashed, double — consistent across the six kinds and the session
  messages; the «done» notice is ink, never green.
- **Disclosure and tabs.** The FAQ's rows have a drawn chevron, 56 px, a ring on the row. Tabs (no product consumer yet)
  behave on the showcase: the indicator travels for a pointer's choice only, the arrows and Home / End move the
  selection and the focus together, the ring shows.
- **Three radii.** The family draws 4 · 8 · pill; the fourth value on a console screen (6) and on the entrance (12) is
  the rail's, the targa's and the entrance sheet's.

## Findings

### Major — fix before shipping

**M1 · The sign-up's password rules are raw HTML, and they break the field around them** (the sign-up, fr and ar, at
every width; «Modifier le mot de passe»). `form_field.html` wraps the help in `<p class="form-field__help">`; Django's
password help is a `<ul>`, a `<p>` cannot hold one, the parser closes it. So: (a) the list is set at body size, 17 / 28
with default bullets — the loudest text of the form, above 13 / 20 for every other help line; (b) the field is now a
column ordered by `order`, and the stray list (order 0) pushes the 2 px focus rule some 270 px under its control — on
focus a teal line appears across the form below the list (`states/signup-focuspw-fr-1440.png`); (c) the field's error
message lands under the list, away from its field; (d) `aria-describedby` names an empty paragraph: the rules are not
announced as the field's description. *Fix:* the wrapper is a `<div>` with the same class and id; `v5/field.css` gives a
help list no margin, a 1.25 em indent and 4 px between items.

**M2 · The show / hide control takes the plate** (login, sign-up, password change, delete account). The control is the
sentence «Afficher le mot de passe» inside the field (162–170 px in French, 110 px in Arabic) and the plate reserves
160–176 px for it. Left for the password: **204 px at 1440, 130 px at 390, 100 px at 360** — and a password here has at
least 12 characters: in the field's own type a 12-character sample measures 113 px and a 14-character one 132 px, so on
a phone the password a person asked to see is cut. At rest the placeholder runs into the control: «Mot de passeAfficher
le mot de passe» on the login at 360; «Mot de passe (coAfficher le mot de passe» on the sign-up at 390 and 360; clipped
at 1440 too («(confirmation» without its bracket); in Arabic at 360 the placeholder loses its first word. Three such
sentences stand in a column on the password change page. *Fix:* the control is a glyph in a 44 px seat (`eye` /
`eye-off` are in the sprite; plan §1.13 already says «the glyph swaps at once»), the live string its accessible name,
`aria-pressed` the one channel; the plate's end padding becomes `--field-h` (with its RTL twin). `shell.js` §3 then
swaps the glyph and no longer writes `textContent` — one justified path. Minimum, if the script cannot be touched in
this pass: below 48 rem the control leaves the plate and sits under it at the inline end (CSS only).

**M3 · A public form's action is shorter than its fields, and on a phone it does not take the column** (contact, company
needs, collaboration, profile, e-mail, password change — everything but the entrance sheet and the FAQ's search). Plan
§1.8 gives 52 px to «public primaries, public form fields»; the family re-pointed the field (`body:not(.console) {
--field-h }`) and not the button: «Envoyer le message» is 179 × 44 under 672 × 52 fields, and the same 179 px at 390
where the login's action is a 52 px block. *Fix:* in `v5/buttons.css`, the actions of a public form take `--control-lg`
and `--btn-pad-lg`, and below 48 rem the primary is block; in the same commit either every public primary takes §1.8's
52 px or DL54 records why not. (The profile form's submit is not inside `.form__actions`: the selector must reach it.)

**M4 · A chip is stretched into a bar on two phone lists** — «Derniers dépôts» on the dashboards (person, terms pending,
the professional's bridge) and «Mes formations», fr and ar: «non analysé» is 296 px wide at 390 (266 at 360) where it is
108 px at 1440; «Suivi en cours» 253 px. The lists are grids and stretch their items; V4 did the same, but a V5 pill
296 px long reads as an empty field, three times, on the first console screen. *Fix:* `.chip { inline-size: fit-content; }`
in `v5/chip.css` — a chip is as wide as its word whatever lays it out.

### Minor — polish, in this pass where it is one line

- **m1 · The person's own mark is drawn in ink, not in white.** `:where(…) { color: var(--text-on-accent) }` loses to V1
  `base.css:68` (`input { color: inherit }`): the tick, the radio's dot and the switch's thumb are `#15222a` on the teal
  fill, 3.07 : 1 where the sheet means 5.29. One rule with real specificity:
  `input:is([type="checkbox"], [type="radio"]):checked { color: var(--text-on-accent); }`.
- **m2 · A chip on two lines is a lozenge** (helpdesk at 390; three lines on the board). Take
  `border-radius: calc(var(--chip-box, var(--chip-h)) / 2)`: the same pill on one line, a 12 px plate on two.
- **m3 · Two buttons 5 px apart** on «Supprimer mon compte», «Demande transmise» and the upload (the white space between
  two inline boxes): the system's pair is 12 px. Three templates of the page families.
- **m4 · The placeholder's ink is a token only inside `.form-field`**: the documents' search shows the browser's
  `#757575`. Put it in the zero-specificity base of `v5/field.css`.
- **m5 · A notice has no measure**: on «Demande transmise» at 1440 the lines run 130–150 characters in a 1240 px box.
  Cap the text (the box may stay wide).
- **m6 · Edges.** The disclosure's row starts 4 px inside its section (the question at x = 104 under «Général» at 100);
  the first tab's label 12 px inside its panel's text; a focused tab's ring is the only square one — give the tab the
  2 px corner.
- **m7 · One disclosure, two sizes.** The component's row is 17 / 24; the FAQ's question (its `h3`) is 20 / 28 — nine
  headlines in a column, two or three lines each at 390, broken inside «délivre-t-elle». Let the heading take the
  row's type (its role is kept).
- **m8 · `.meta-row` on a phone** (carried over value for value): «Nature» and its « : » on two lines beside a
  two-line value. Keep the colon with its label; stack label over value below 48 rem.
- **m9 · The focus of a public text field** (the implementer's open point): the ring sits between two bands of its own
  halo at 2.6–2.8 : 1; against the ground it is 3.7–3.9, and the edge and the foot rule are 4.11 on the plate. My
  reading: not a failure — the state is carried by parts at ≥ 3 : 1 — but the ring loses its edge. Laguna-600 for the
  field's ring (3.33 on the halo) would close it; the accessibility check rules, after shipping.
- **m10 · States with no page and no board.** Soft and icon buttons, radio, switch, disabled / read-only / warning
  fields, the multiple select: all correct on my bench but for m1. Add one row of them to the showcase's form board
  (the buttons' and fields' boards of plan §3.3 were not built; under V5.5 the showcase is enough).
- **m11 · The gauge of a case status** — three 6 px circles beside a circle mark and a dashed edge («◌ Brouillon ●○○»)
  — is the busiest chip of the system. Notches that are not circles (2 × 6 px bars) would leave the circle to the mark.
  Taste; optional.

### The implementer's other open points

Agreed as they stand: the console keeps its own ring without a halo until m9 is settled; the icon-only button's busy
face waits for its first consumer; `warning` → attesa and `pending` → esame; the dashboard header's date under its
reference at 390; `badge` as a hook; the seal, the filter chip and the count not drawn.

## The fixes, tried

Nothing was written to the repository. The rules were added as an adopted style sheet and the two markup changes made in
the DOM by the harness; before and after are side by side in `…/review/fixsim/pair-*.png`.

- M1: the list at 13 / 20 under its field, the rule on the control's foot, the sign-up's form 142 px shorter at 390
  and 154 px at 1440.
- M2: the password's room 100 → 208 px at 360 and 204 → 328 px at 1440; no collision at any width, fr and ar.
- M3: 52 px at 1440; a 350 × 52 block at 390, fr and ar.
- M4 and m2: 296 → 108 px; the two-line chip a plate; **no chip box moves** at 1440 on the dashboard, «Mes pièces» and the
  company's table (17 chips compared, to the pixel).

## Seen on the way — not this family's

- **W2-A / W3-F2 — first:** on «Supprimer mon compte» at 1440 the account's links box covers the end of the warning
  notice's first line (what is deleted). Older than this family, but it hides text on a destructive page.
- **W3-B:** the dashboards are still V4's grid of equal sheets — on the organisation's bridge, five panels of one
  sentence each under the action. «Cards by purpose» is true of the sheet and not yet of these pages: the action card
  and the summary strip have no consumer.
- **W3-C:** `SCAN_BADGES` beside the registry — a failed scan now reads amber «attesa» on the bridges' lists (DL54-52),
  and a clean one reads conforme where the registry says neutro («an antivirus issues no conformity»): hand the member
  to the tag in its first step. «En retard» is still drawn as a refusal. «Mes pièces»: the third row's chip stands 27 px
  off its column. A missing date is a lone «—».
- **W3-E:** on «Mes formations» a plan's state is bare capitals («EN COURS») beside entries that carry chips; hand-written
  console labels at 13 / 20 (the case's state form).
- **W3-F1:** the anti-fraud callout in the side column is 272 × 822 px of four-word lines at 1440; «Pour aller plus
  loin» sits 6 px under the FAQ's last row; «Termes utiles»; the Privacy Policy link at 17 / 28 under a 15 / 24 consent;
  a telephone number in a 672 px field.
- **W2-B:** the placeholders repeat their labels on sign-up and password change (plan §1.13 removes the login's).

## Evidence

`C:/tmp/ile_v5_council/evidence/v54/w1-c/review/` — `base/` (the 56 cells, probes), `phone/` (43 viewport scans),
`states/`, `states2/` (states, the showcase's crops, forced colours, reduced motion), `pages/` (the 120 cells), `board/`
(the chip board), `bench/` (the states no page draws), `fixsim/` (the fixes, before and after), `compare/` (crops of
W1-0's before-set). Tools: `C:/tmp/ile_v5_council/.work/w1-c/w1-c-review/tools/`.
