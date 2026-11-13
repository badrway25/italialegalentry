# W3-C · Document workspace and status — senior review (one pass)

Reviewer label `w3-c-review` (built nothing). V5.5 delivery mode: one review, then fix, then ship. Branch `v54-w3-c` at
`b62c10b` (steps 1 and 2 and their notes). Looked at on the reviewer's own server from this worktree (127.0.0.1:8889,
`ile_v5_l9`, `ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`, `--noreload`, no preview flag), headless Chromium in
ephemeral contexts, one browser and one pytest at a time, sessions minted with `Client.force_login` (no password used,
typed or stored) and revoked at the end; one lane-only persona with an unusable password
(`w3c-review@example.test`: three pieces, one due «tomorrow») created for the live deposits and deleted with everything
it owned; the server stopped. No browser run ended on a crash. Evidence:
`C:/tmp/ile_v5_council/evidence/v54/w3-c/review/` — 218 captures in `main/`, `drawer/`, `close/`, `swapclose/`,
`fermer*/`, `drw1100/`, `pages/`, `depot/`, `misc/`, each with its `report.json`.

**Looked at:** «Mes pièces» (`/fr|ar/espace-reserve/mes-documents/`) and `/documents/` for `qa-person` (seven pieces in
seven states, the Conditions not accepted), `qa-doc-person` (a piece to replace, two filed), the implementer's
`w3c-depot` and the review persona (open pieces with acts), `seed-company` (no file); a piece in every state (to replace,
missing, refused and gated, valid, held by an authority); the loose upload page and the Conditions gate page; the
deadlines page — fr and ar, at 1440 × 900, 1366 × 657, 1280 × 800, 1100 × 800, 390 × 844 and 360 × 800 (full pages at
1440 and 390). Driven: the preview drawer (open, swap, Esc, «Fermer», Back, `?état=` kept, the phone sheet and its trap),
the filter sheet, the search, the keyboard walk, forced colours, reduced motion, and the Dépôt end to end — the three
client guards, a past validity date, the server's content refusal, a filing in the drawer and on the piece's page at 390
(fr, ar), a loose deposit. The presenter, view and service diffs read line by line.

## Verdict: **SHIP_AFTER_FIXES**

«Mes pièces» is at the bar. It reads as an institutional workspace with a product's finish, not a table of badges: one
raised strip — «il registro» — says whose move it is in three runs whose marks are the pieces themselves (the colour is
the group, the shape is the state), then the one next piece with its date and the page's one primary; the filter is also
the key to the marks, in the register's own order; the collection draws the same three groups, one row per piece, the
row itself the link, the state always a word with its mark, the date always with its glyph, the act only where the
reader acts. Everything else lies flat under hairlines. «Valide» is ink with no check anywhere; «En examen» is lapis; red
never means lateness (F13 holds on the deadlines page). Arabic is a true mirror with the French record titles isolated.
The phone composition works (the strip composed, one filter control and its sheet, the first piece in the first screen).
The Dépôt is the best part of the family: every answer — a format, an empty file, a size, the server's content check, a
past date, the filing — lands in place, on the file's row or under the piece's new state, and the drawer and the register
behind it read themselves again.

No P0: no broken page, no wrong direction, no data or permission problem; the Dépôt's JSON road changes the form of the
answer and nothing else. Three majors must be fixed before the merge — the drawer loses the person's place after a swap,
opening it re-lays out the register under the pointer with nothing marking the open row, and an open piece due tomorrow
reads «En retard» on the preview because two clocks decide one deadline. The rest is polish.

## The gate, checked on the real pages

| Gate item (plan §3.5 item 5, the brief) | Result |
|---|---|
| The first card's title ≤ 700 px at 390 × 844 | 693 px fr / 661 ar (`qa-person`, whose strip carries the gate's line), 625 / 629 (`qa-doc-person`), 653 / 661 (`w3c-depot`) |
| The first object in the first viewport at 390 and 360 | yes — the strip and its primary (437 px at 390, fr) and the first piece's title above the bottom bar, every persona, fr and ar; at 360 × 800 `qa-person`'s two-line title ends 1 px under the bar (693 + 42 vs 734) |
| The row as the link, with its piece, its state and its date | yes — hover lights the whole row, a press anywhere opens the piece (the actor's column included), one Tab stop per row, a 2 px ring |
| Eight registers, never colour alone; «valide» without a check | seen: azione (Expiré), rifiuto (Non valide), attesa (Manquant, À remplacer, dashed), esame (En examen, lapis), neutro (Déposé), conforme (Valide, the plain ink disc), blocco (the gate's lock); each a word and its mark; no check in the chip, the run, the filter or the sheet; forced colours draw every edge and mark (`misc/fc-*`) |
| Ledger counts = group counts | 3 · 3 · 1 = 3 · 3 · 1 (`qa-person`), 1 · 2 · 0 (`qa-doc-person`), and live through three filings on the review persona: 3 · 0 · 0 → 2 · 1 · 0 → 0 · 3 · 0 — but see m1 for the caption's own count |
| Entries in `STATE_ORDER` | Expiré, Non valide, Manquant, À remplacer, En examen, Déposé, Valide — filter, sheet and rows |
| A filed piece due tomorrow reads calm | yes — the review persona's piece due 04.10.2026, filed live: the calendar, no word, in the row and the drawer (before the filing it read «En retard»: M3) |
| The register strip's one primary | one `btn--primary` per page, in the strip, described by its piece: «Consulter» on `qa-person` with «Acceptation des Conditions d’utilisation requise.» (honest while G1 holds), «Remplacer la pièce», «Déposer la pièce»; none when nothing is asked (the sentence) |
| 6 / 5 columns, then cards, by the register's own width | 1440 six; 1366, 1280, 1100 five (the actor under the title); 390, 360 cards; cards beside an open drawer (M2) |
| Preview drawer — non-blocking on desktop | yes — no scrim, no `aria-modal`, the list usable beside it, another row swaps it without replaying the slide; on the left in Arabic |
| Preview drawer — history, Esc, focus | the opening pushes the piece's URL, a swap replaces it, Esc / «Fermer» / Back bring the register back with its `?état=` (`?état=invalid` kept); the focus on the title, back on the row's title — **except after a swap (M1)** |
| Phone sheet | modal (`aria-modal`, three Tabs stay inside), Esc closes it, the focus back on the row — fr and ar, 390 and 360 |
| Filter sheet | the system's bottom sheet, grip and «Fermer»; the focus on the current entry, back on the control after Esc; a choice reloads on `?état=`; the empty filter says so with «Voir toutes les pièces» |
| Reduced motion · RTL | the drawer: `translate: none`, opacity only; Arabic mirrored throughout, French titles and reasons isolated, Latin digits |
| The Dépôt's answers composed; validation, limits, permissions unchanged | composed in place (see «Security» for the server side): «Format non accepté…», «Le fichier est vide.», «Le fichier dépasse la taille maximale de 10 Mo.» on the file's row, nothing sent; «Le contenu du fichier ne correspond pas à son extension.» from the server, on the same row; «Cette date est déjà passée…» under its field; «Pièce déposée (version 1). Elle sera examinée par un intervenant du dossier.» under the new state with the filed mark, the register behind updated; «Document téléversé.» on the loose road; Arabic the same |
| F13 on the deadline registers | «En retard» azione (terracotta, the clock-hands disc, the alarm-clock glyph), «Bientôt» attesa (amber dashed ring, the clock), the calendar otherwise — fr and ar (`pages/deadlines-depot-*`) |
| Health | 0 console errors, 0 CSP reports, 0 horizontal overflow, 0 responses ≥ 400 except the gate page's 403 (the road without script, unchanged); nothing moves at load except the entrance release (W1-D) on a session's first page |

## Security and the server's rules

No legal rule, permission, limit or visibility changed. The Dépôt's JSON road (`apps/documents/views.py`) is read only
after `_get_requirement` and `require(user, "file", requirement)` have run; the Conditions gate, the throttle, the form's
validation chain (size, allow-list, content, image, active PDF), the antivirus and the storage run the same lines on both
roads; the answer carries the form's and the service's own sentences, is never cached (`no-store`) and is posted with the
form's CSRF token. The client guards are a courtesy only — the server refused a PNG named `.pdf` on its own. `next_piece`
reads `cases.services.next_action(case, reader=user)` over rows that `readable_by` already narrowed. Targeted run on
`test_ile_v5_l9`: `tests/frontend/test_documents_w3_c.py`, `test_depot_w3_c.py`, `apps/documents`, `tests/security`
(non-browser) — **342 passed, 1 skipped** (the confidential sentinels' table is not configured on the lane), 0 failed.

## Findings

### Major

**M1 — After a swap, closing the drawer throws the person back to the top and the focus to the wrong row.** Desktop,
fr or ar, `qa-person`: open «Extrait de casier judiciaire» from its row, scroll, press «Proposition de contrat de
travail» (the content swaps — correct), then close. With «Fermer» (mouse or keyboard) or Esc from inside the drawer, the
page glides from scrollY 1 028 to 0 and the focus lands on «Extrait…», the first row opened, not the piece that was shown;
with Esc while the focus is on the list, the page goes to the top and the focus stays on «Proposition…», 1 060 px below
the fold (`swapclose/`, `fermer/`, `fermer3/`; the focus trace in `fermer2/`). Swapping is what a non-modal preview is
for, so every browsing session ends lost. Two causes: the native `<dialog>`, shown once, restores the focus to the
element focused at that `show()` when `panel.close()` runs — `overlay.js`'s `settle()` then finds the focus outside the
panel and does not move it to `record.opener`, which the swap did update; and the close's `history.back()` lets the
browser restore the register entry's scroll position saved at the first opening (`scrollRestoration: auto`). *Fix*
(`static/js/src/piece-drawer.js`, on `overlay:close`): when the reason returns the focus, focus `detail.opener` (the
current row's title) and bring it into view (`block: "nearest"`) after the history's restoration — or hold
`history.scrollRestoration = "manual"` while the drawer owns its entry; a browser test: swap → «Fermer» / Esc → the focus
on the shown piece's row, inside the viewport. The system's half goes to W2-A (carry-over).

**M2 — Opening the drawer re-lays out the register under the pointer, and nothing marks the open row.** At 1440, 1366,
1280 and 1100 (fr and ar) the workspace makes room, so the register switches from its table to the phone's cards and its
filter track to the phone's one control (the documented decision, DL54-102 — kept). But the row that was pressed moves,
and the card that slides under the pointer takes the hover — underlined title, tinted surface — so it reads as the piece
in the drawer while the drawer shows another (`drawer/drw-qa-person-fr-1440--1-open.png`, `…-fr-1366--1-open.png`,
`…-ar-1440--1-open.png`, `drw1100/drw1100-fr--open.png`). After a swap or two nothing on the page says which piece is
open. *Fix:* mark the open row — `aria-current="true"` on its title link and a quiet selected state (the hover surface
and a 2 px inline-start rule, held while open, moved on a swap, cleared on close) — and keep the pressed row where the
pointer left it when the register re-lays out (measure its top before the `data-drawer-beside` toggle, restore it after,
in `beside()`; the same on closing).

**M3 — Two clocks decide one deadline: an open piece due tomorrow reads «En retard».** On the reviewer's server
(reference date 03.10.2026, real date 12.10), the review persona's piece due 04.10.2026 is drawn «En retard» in
terracotta with the alarm-clock in the strip, the row and the drawer (`depot/dep-guards-fr-1440--1-drawer.png`) — it is
«Bientôt» (attesa, the clock). `present_requirement` passes `overdue=requirement.is_overdue`, and
`DocumentRequirement.is_overdue` (`apps/documents/models.py` l.334) compares with `timezone.localdate()`, the real clock,
while `due_urgency` and the deadlines page read `core.clock`; `cases.ChecklistItem.is_overdue` (`apps/cases/models.py`
l.305) and T1 (`cases/services.py` l.590, l.605, «overdue first») do the same. Production has one clock (the override is
DEBUG-only), so this lives on the lanes and the owner's preview — exactly where the deadline registers are judged — and
it grows daily: on the preview `qa-person`'s piece due 05.11.2026 turns «En retard» on 6 November, and T1 then ranks it
as overdue. *Fix:* `clock.today()` in both `is_overdue` properties (two lines; a justified path outside the slice, the
clock rule of the 5 October fix), with a test under a reference date; at the least, drop `overdue=` in the presenter
(`due_urgency` already returns «overdue» from the project's clock) — but then the NowPanel and the register disagree.

### Minor

**m1 — The caption counts a set no run shows.** `qa-person`'s strip says «À faire 3 · En cours 3 · Valide 1», then «7
pièces demandées · 1 sur 7 validées · 4 en attente» — four open pieces across two runs, a fourth way to count the same
seven. The gate's equality holds for the runs; the strip's own sentence breaks it. *Fix:* end the caption at «1 sur 7
validées» (a clause dropped, no new word) — the copy packet's item 6 proposes it; the team can take it now.

**m2 — Two primaries in one view when the drawer shows the strip's piece.** At 1280 on `qa-doc-person` the strip's
«Remplacer la pièce →» and the drawer's «Déposer» stand side by side, both teal, for the same act
(`drw1100/drw1280-doc-fr--open.png`). *Fix:* while the drawer shows the strip's piece, the strip's act takes the open
row's selected state (M2) and steps down to secondary.

**m3 — The files tables stack into label blocks on a phone.** «Tous les fichiers de votre compte» on `qa-person` is six
blocks of four uppercase labels (FICHIER, TYPE, TAILLE, DÉPOSÉ LE) split by 2 px navy rules — ≈ 1 300 px at 390, where
the register's finish stops (`main/reg-qa-person-fr-390x844--full.png`, `misc/emptyfilter-fr-390.png`,
`depot/dep-index-fr-390.png`). *Fix:* under 40rem one list item per file — the name (the link) on its line, «type · taille
· date» on one muted line, «Supprimer» at the inline end — the register's hairline, no uppercase labels.

**m4 — «Supprimer» deletes a loose file at once.** `/documents/`, «Autres fichiers déposés»: no confirmation, no undo.
V4 did the same, but the overlay system now has the alertdialog and W3-F2 put the account's deletion behind one. *Fix:*
the system's alertdialog — the file's name in the question, «Annuler» the safe answer, «Supprimer» the garnet outline —
the form unchanged without script.

**m5 — The loose deposit's answer empties the page.** After «Document téléversé.» the form is gone; the page names no
file and offers no next deposit (`depot/dep-loose-fr-1440--2-filed.png`). *Fix:* the answer carries the file's name
before the server's sentence, and the zone comes back for another file (existing words only).

**m6 — The chosen file's size contradicts its refusal.** An empty file reads «PDF · 1 ko» beside «Le fichier est vide.»;
a file just over the limit reads «PDF · 10 Mo» beside «…la taille maximale de 10 Mo.» (`sizeOf` rounds 0 B up to 1 ko and
10.0001 Mo down to 10). *Fix:* 0 B as «0 ko» (or no size), one decimal near the limit.

**m7 — «Il registro» drawn twice.** The strip's marks (`_workspace.css` `.reg-run__marks`: size and three group colours)
repeat the dashboard's rules (`.db-ledger__marks` in `_dashboard.css`, already on every console page through
`console.css`). V5.8 rule 3: the family that merges second consolidates. *Fix:* draw the strip's marks with the shared
ledger rules (or one ledger-marks primitive both use) and delete the copies from the page sheet.

### Carry-overs to other families (not W3-C's merge)

- **W2-A (overlay system):** `settle()` decides «was the focus inside the panel» after `panel.close()`, when the native
  dialog has already restored the focus to the element focused at its `show()`; a panel whose content swaps (the preview
  drawer) keeps a stale restore target. Read the focus before closing (M1's system half).
- **W3-B / W3-E:** T1 (`cases/services.py` l.590, l.605) and the case file's checklist (`cases.ChecklistItem.is_overdue`)
  share M3's clock; fixed with it if the model lines change. The implementer's own W3-B list stands (`_deadlines_card`'s
  no-op mapping, the bridge's `SCAN_BADGES`).
- **Copy review (O43, the owner's):** one page under three names — «Mes pièces» (h1), «Mes documents» (rail, bottom
  bar, the register's trail), «Registre complet» for `/documents/`, whose trail stops at «Espace réservé» — and the
  loose page's trail «Téléverser» under the h1 «Déposer un fichier».

## Kept as it is (said, not findings)

- The register re-laying out to cards beside the drawer is DL54-102's decision; M2 fixes what it costs, not the decision.
- «Consulter» as `qa-person`'s one primary, with the gate's sentence under the date: the honest act while the
  acceptance flow waits on G1 (the answer W3-B's review M1 asked for on the dashboard).
- «Pièce acceptée» (a version's decision label), «1 sur 7 validées» and its Arabic «مقبولة» are domain and catalogue
  words older than V5 — the copy review's, not this family's.
- A deposit dated «12.10.2026» on a lane whose reference date is 03.10 is the real time of the act, a fact.
- The «En vigueur» tag on the current version uses the neutro register's mark, as the registry defines it.

## For the merge step

- **Shared payload (gzip −9, `gzip.compress(…, 9)`):** design-v5 at the start of this review (`abbabda`) 42 152 + 6 809 +
  1 932 = **50 893** B on the console page types; design-v5 now (`3780a7c`, W3-F2 merged during the review) 41 464 +
  6 809 + 1 932 = **50 205**; this branch's tree 40 876 + 6 809 + 1 935 = **49 620**. The two families deleted different
  legacy rules: rebuild the merged tree from a clean dist and weigh it — it must come out ≤ 50 205.
- **Page-only:** `dist/documents/documents.css` 1 172 → 5 418 B; W2-A's `dist/core/overlay-panels.css` (2 071 B) now
  linked by the two register pages. «Mes pièces» in all: 52 065 → 57 109 B on the branch's base (51 377 on design-v5
  now). Record it under V5.8 rule 2 and DL54-87 item 3, after m7's consolidation.
- **Decision log:** W3-C's entries are written DL54-96 … DL54-104; design-v5 now holds DL54-96 … DL54-99 (W3-F2's three
  and the steward's merge entry) — renumber from DL54-100.
- **Ownership:** `scripts/check_ownership.py w3-c design-v5` → 18 inside, 7 slice, 21 generated, 15 outside, each
  justified in the notes (DL54-99, -101, -104 as written) for the manifest; M3's model lines add two justified paths.
