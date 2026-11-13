# W3-B · Dashboard and cards — senior review (one pass)

Reviewer label `w3-b-review` (built nothing). V5.5 delivery mode: one review, then fix, then ship. Branch `v54-w3-b`
at `41a725a` (step 1 + step 2 and their notes). Looked at on the reviewer's own server from this worktree
(127.0.0.1:8886, `ile_v5_l6`, `ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`, `--noreload`, no preview flag),
headless Chromium with its own profile, one browser and one pytest at a time, sessions minted with
`Client.force_login` (no password used, typed or stored) and revoked at the end; the server stopped. No run ended on a
crash. Evidence: `C:/tmp/ile_v5_council/evidence/v54/w3-b/review/` (`main/` with its `report.json`, `takeover/`,
`takeover-list/`, `empty/`, the contact sheets and crops beside them).

**Looked at:** the person's dashboard for four accounts (`qa-person` — a file with pieces due; `qa-doc-person` — a
piece to replace; `seed-person` — an advanced file, nothing asked; `qa-fresh-person` — no file), the company's
dashboard (`qa-company` with its company; `seed-company` without one), the bridge (`seed-company` on «Espace réservé»,
`seed-actor`, and an institution and a university — two lane-only accounts with unusable passwords, created for the
review and deleted with everything they owned) × fr / ar × 1440 × 900, 1366 × 657, 390 × 844, 360 × 800 (80
captures, full pages at 1440 and 390). The NowPanel's takeover was drawn with a lane-only overdue date on `qa-person`
(fr / ar, 1440, 1366 × 657, 390), then deleted. The presenter diff read line by line;
`tests/frontend/test_dashboard_w3_b.py` + `tests/security` run once on `test_ile_v5_l6`: **171 passed**.

## Verdict: **SHIP_AFTER_FIXES**

The dashboards are at the bar in their composition. The person's page answers in the right order and reads as an
institutional workspace, not a dashboard kit: the header says who and which file (the reference in ILE Mono, the
state and since when), ONE raised NowPanel says the piece, its state, its date, who answers for it and the one act,
the journey says what comes next, and everything else lies flat under hairlines — «il registro» of the pieces by who
holds them, each piece once, the dates and the communications as lists, the secondary folded. The company's page is
the same grammar, not a second system, and the bridge is honest: no invented next action, what is due first, an
overdue date in terracotta, empty regions as one line. No stat card, no grid of equal cards, no board anywhere.
Arabic is a true mirror. The phone composition is good (the NowPanel's facts two by two, the primary across).

No P0: no broken page, no wrong direction, no data or permission problem — and one cross-person exposure of the V4
dashboard is gone (see «Security»). Three majors must be fixed before the merge — the main QA persona's one primary
is a dead end, French free text breaks in Arabic on the takeover and the lists, and the deletion of one legacy rule
centres the empty state of four other console pages. The rest is polish.

## The gate, checked on the real pages

| Gate item | Result |
|---|---|
| One primary in the first viewport, with its piece and its date | yes wherever the account has an act — `qa-person` (the piece, 05.11.2026), `qa-doc-person` (the piece; no date in the data), `qa-fresh-person` (the questionnaire), the company (the need), the takeover (the date) — fully inside the first viewport at 1440, 1366 × 657, 390 and 360, fr and ar; none on «rien à faire» and on the bridge, by decision (DL54-80). **But see M1:** `qa-person`'s primary leads nowhere |
| No requirement id drawn twice | 0 duplicate `data-piece` / `data-need` on 80 captures |
| DOM order h1 → NowPanel → journey | yes on every person capture; h1 → NowPanel on the company's |
| ≤ 1 raised panel, ≤ 2 shadow values | the person: 1 plane (the NowPanel), 2 values (its shadow and W3-D's journey-node halo); the company: 1 and 1; the bridge: 0 and 0 |
| No stat card | none (no numeral ≥ 24 px in the workspace; no counted box) |
| The four NowPanel variants | «à vous», «rien à faire», «pas encore de dossier» and the takeover seen on real pages; «en attente d'un tiers» composed in the tests only (no QA account holds it) |
| Corners | 4 · 8 · full on the page (the chip's 12 px is its pill, W1-C's); W3-A's account menu adds its 6 px on phones |
| Health | 0 horizontal overflow, 0 console errors, 0 responses ≥ 400, 0 CSP reports, 0 running animations at load, 0 targets under 24 px — 87 loads |
| §3.1 item 7 — identity carriers | «il lume» in the rail, «La soglia» (the journey), «I cerchi» (every state a chip with its mark), «il registro» (the ledger's 16 px marks coloured by the group), ILE Mono (the file reference, the immatriculation, the need references), the owner's door in the one empty state. The swap test passes: without the logo, the night rail with its lit disc, the ledger marks and the mono reference still say ILE |
| The value matrix (§1.15) | in NOTES.md, per persona; what replaced personalisation is said (system-ordered priority, native disclosures, URL filters, the kept preferences) |

**Where am I · the one thing to do · what comes next — the first viewport**
- *`qa-person`*: where — yes (Tableau de bord, E46E03B461, «Orientation terminée» since 21.09.2026); the one thing —
  the piece, «À remplacer», 05.11.2026, «La personne», **but the act is a dead end (M1)**; next — the journey at 1440;
  at 1366 × 657 only its heading and shore labels peek (the NowPanel ends at 552 px).
- *`qa-doc-person`*: yes, yes («Remplacer la pièce»), yes.
- *`seed-person`*: where — yes; the one thing — «Aucune action ne vous est demandée pour l'instant», honest; next —
  not said in the panel (m2), and the journey contradicts the file's state (W3-D's carry-over below).
- *`qa-fresh-person`*: yes — «Le questionnaire d'orientation» with the owner's door and «Commencer le questionnaire».
- *Company*: yes — the legal name, «Vérifiée», the need to transmit with its state, one act (m4 on its label).
- *Bridge*: where — «ESPACE RÉSERVÉ» (the prescribed, locked h1 — `test_compliance.py` pins it); the one thing — what
  is due first with its chip; next — nothing claimed (DL54-80); m10 for the accounts whose work lives elsewhere.

## Security of the presenter changes

No legal rule, permission or visibility changed; nothing of one person reaches another role.
- **T1** (`cases.services.next_action(case, *, reader=None)`): pieces are read through
  `DocumentRequirement.objects.readable_by(reader)` at query time; without a reader only the CASE access class. The two
  case views pass `reader=request.user`; an assignee therefore sees only pieces it may already open. The blocking
  outcome's new link (`cases:assessment`) is guarded by `_case_or_404` + `can(user, "view", assessment)`.
- **The person's pieces now come from the account's own file only** (`_dashboard_pieces(user, active_case(user))`,
  `person=user`). The V4 dashboard read `register_context(user)`'s first block — for an administrator (whose
  `readable_by` is everything) or an assigned professional typed «person», that was **somebody else's file**, its
  counts and its three most urgent rows on «Mes documents». W3-B removes that exposure: keep it.
- The company's composition only re-orders what `companies.services` already returned (the needs, the live parties'
  `display_name` — never an e-mail — as the V4 table did); the bridge's registers are `card_builders_for` unchanged,
  built for non-persons only (F9). The takeover's text is the deadline's `source_note`, «affichée à la personne».
- `tests/security` + the family's tests: 171 passed.

## Findings

### Major

**M1 — The main QA persona's one primary is a dead end.** On `qa-person` (whose account has not accepted the
Conditions) the NowPanel names «Acte d'état civil légalisé · À remplacer · 05.11.2026» and offers, as the screen's ONE
primary, «Accepter les Conditions →» — which opens the public `/fr/condizioni-di-utilizzo/`: «Page en cours de
préparation… Aucun texte provisoire n'est affiché», with nothing to accept (the acceptance flow waits on G1;
`documents/terms_required.html` says so). Nothing in the panel says why the act on a civil-status act is to accept
conditions, and the list rows under it say «Consulter» for the same block. This is the persona the owner opens on the
preview (`main/qa-person--portal--{fr,ar}--{1440x900,1366x657,390x844,360x800}.png`). *Fix* (`_now_acts`,
`apps/portal/services.py` ≈ l.1749): when the filing is blocked by the conditions, the primary is «Consulter» on the
piece's own page, and the panel's note carries the catalogue's «Acceptation des Conditions d'utilisation requise.»
(the register row's own words) — never a button that promises an act the target cannot do. Same words as the rows.

**M2 — In Arabic, French free text written by the team is not isolated on the takeover and in the lists.** The
takeover's title and text (a deadline's title, its source note), the person's dates and communications, the company's
communications and «Derniers dépôts» carry no `dir`, so neutral characters at their edges are reordered on an Arabic
page: «[w3b-review] Rendez-vous au consulat — confirmer la date» is drawn «Rendez-vous au consulat — confirmer la date
[w3b-review]», «Note de test (lane 6, revue).» becomes «.Note de test (lane 6, revue)», «[w3b-review] Entretien (consulat
de Rabat).» becomes «.Entretien (consulat de Rabat) [w3b-review]» (`crop-ar-takeover-and-list.png`,
`takeover/qa-person--portal--ar--390x844.png`). Real titles carry parentheses, dates and final points; Arabic readers
are the platform's first audience. The bridge's `card.html` already does it right (`dir="auto"`), and the NowPanel
does it for a piece (`_data_lang`). *Fix:* the takeover branch of `now_panel` gives its words `dir="auto"` and the
partial emits `dir` when the presenter sets one (`now_panel.html` l.21–22 only test `words.lang` today); `dir="auto"`
on `.db-list__title` for `deadline.title`, `message.subject` and `document.label` (`templates/portal/dashboard.html`
l.168, l.187, l.257; `templates/companies/dashboard.html` l.136), the row's reading edge kept as on the bridge.

**M3 — Four other console pages now centre their empty state in a 42 rem box.** The bridge clean-up deleted, with the
card grid, `.portal-card .empty-state, .portal__main .empty-state { max-inline-size: none; margin-inline: 0 }` from
`portal.css`. The second selector was not the bridge's: it held every `components/empty_state.html` inside the
console's `.portal__main` on the page's start edge. On this branch «Communications», «Mes échéances», «Mes demandes»
and «Mon parcours» draw their empty state 672 px wide, centred (x = 508 in a main column starting at 280), where
design-v5 draws it across the column (`empty/*.png`; the base bundle holds the rule, the branch's does not). A page of
another family made worse by this merge. *Fix:* restore `.portal__main .empty-state { max-inline-size: none;
margin-inline: 0; }` in `portal.css` (its last consumers, W3-C / W3-E, retire it with their redraw).

### Minor

**m1 — The takeover leaves «Mes échéances» as a heading with nothing under it.** When the only date is the one the
NowPanel took over, the section keeps its head, drops its empty line (correctly: it would be false) and its link
(`deadlines` is empty), and shows nothing (`takeover/qa-person--portal--fr--1440x900.png`). *Fix:* keep the head's
«Toutes mes échéances» link when `now.deadline_pk` is set, or do not draw the section.

**m2 — «Rien à faire» names nobody.** `seed-person`'s raised plane holds one sentence, while the strip beside it says
the file is in the hands of «Acteur autorisé — Agenzia Mediterranea per il Lavoro». *Fix:* give the variant the
«Responsable» fact from the file's live assignment (role — organisation; existing strings), so the panel says whose
move it is — the copy packet's sentence can replace it once B1 signs.

**m3 — A filed piece names «La personne» where the row says who holds it.** `qa-doc-person`: «Passeport en cours de
validité · Déposé · La personne» sits among the pieces «in somebody else's hands», quiet, without an act — and names
the person (`main/qa-doc-person--portal--fr--1440x900.png`). *Fix:* for a piece the person answers for that is filed
or in review, draw no party (the chip «Déposé» / «En examen» says it), or the reviewing party when the data has one.

**m4 — The company's act does not match its sentence.** «Transmettez le besoin « … » au projet» over the primary
«Ouvrir le besoin» (`main/qa-company--company--fr--1440x900.png`). Honest — the click opens the need, whose page leads
with «Transmettre au projet» — but the one thing to do reads in two verbs and two clicks. *Fix (team decision):* either
the NowPanel carries the need page's own act (the same POST form and words, «Transmettre au projet», with the need's
title and reference in view), or keep «Ouvrir le besoin» and accept the two steps; never relabel the link as the act.

**m5 — French typesetting: a guillemet ends a line.** The company's NowPanel title breaks «Transmettez le besoin «» /
«Soudure d'assemblage sur…» at 390 and 360 (`main/qa-company--company--fr--{390x844,360x800}.png`): the catalogue
string has ordinary spaces inside « ». *Fix:* the French-typography filter W2-E introduced (narrow no-break spaces
inside guillemets) on the NowPanel's title.

**m6 — On touch, a linked row's date floats away from its subject.** The communications rows: the 44 px link box
(`pointer: coarse`) leaves ≈ 30 px between the subject and its date, against tight unlinked rows above
(`main/w3brev-institution--portal--fr--390x844.png`, `…--ar--360x800.png`; the same rule serves the person's and the
company's communications). *Fix:* centre the link's content in its 44 px box, or take the height as padding.

**m7 — At 360 the «Responsable» fact splits its glyph from its word.** «Votre entreprise» wraps under its disc
(`main/qa-company--company--fr--360x800.png`). *Fix:* keep the glyph and the label in one non-wrapping inline group.

**m8 — The takeover's line is the source note without its label.** The deadlines page says «Origine : …»; the
NowPanel prints the note bare, as if it described the date (`takeover/…fr--1440x900.png`). *Fix:* the catalogue's
«Origine :» before it.

**m9 — The company without a company leaves the right third empty at desktop.** One NowPanel on 8 of 12 columns and
nothing beside it (`main/seed-company--company--fr--1440x900.png`). *Fix:* let the NowPanel's column follow the content
when the side is empty, or place «Communications» beside it as the person's page does without a file.

**m10 — The bridge does not say where a company's or an actor's work lives.** `seed-company` on «Espace réservé» has
four empty lines and its organisation; its one act («Déclarer mon entreprise») is in «Espace entreprise», `seed-actor`'s
in «Processus assignés» — only the rail says so (`main/seed-company--portal--fr--1440x900.png`,
`main/seed-actor--portal--fr--1440x900.png`). *Fix:* one quiet link at the head of the main column with the rail's own
label for the account's space; no claim, no new copy.

**m11 — Arabic: the progress figure orphans its total.** «العناصر المكتملة: 0 من» / «5» in the file's strip at 1440
(`main/qa-person--portal--ar--1440x900.png`). *Fix:* keep «0 من 5» together (a no-wrap group on the figures).

### Carry-overs to other families (not W3-B's merge)

- **W3-D:** `seed-person`'s file is «Phase gérée par un acteur autorisé» while the journey says «Vous êtes ici · 1 ·
  Votre situation et votre objectif» — the `SELECTION` mapping the notes already hand over; and «VOUS ÊTES ICI» moves
  between the shore-label row and under the step depending on whether a shore label stands there.
- **W3-C:** the register row's «Accepter les Conditions» (`components/document_row.html`) leads to the same placeholder
  page as M1.

## Kept as it is (said, not findings)

- The bridge's h1 «ESPACE RÉSERVÉ» and its lead are the prescribed access-point wording (`p3.reserved.*`), pinned by
  `test_compliance.py`; the trail's «Tableau de bord» beside it is W3-A's rule.
- Arabic bidi in the company's NowPanel title («أرسلوا الاحتياج «…» إلى المشروع» with a Latin title): checked against
  an isolated rendering — identical; the browser's line breaking is the standard one.
- The CSS weight: the console page types 761 B over the DL54-73 ceiling, reported in DL54-81 with the rows that bring
  it under (W3-C, W3-E) — not a regression worth a fix under V5.5.
- Ownership: `scripts/check_ownership.py w3-b design-v5` → 6 inside, 7 slice, 3 generated, 9 outside, each justified
  in DL54-78 / DL54-81 for the merge step to write into the manifest.
