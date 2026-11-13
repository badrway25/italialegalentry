# W1-P · Preview as the live product — independent UX re-check (round 2)

Italy Legal Entry™ design V5 · V5.4 «EXECUTION MODE» · 5 October 2026 · independent reviewer, lens **UX (council lead
for W1-P)**, label `w1p-ux-r2`. I built nothing in this family.

- **Baseline:** my round-1 report, `docs/design-v5/QA/v54/w1-p/ux.md` (FAIL: 1 blocking, 6 major, 11 minor). **Fixes:**
  `IMPLEMENTATION_NOTES.md`, «Review fixes — round 1».
- **Reviewed:** branch `v54-w1-p` at `8f12192`, `v54/base..HEAD` (12 commits). The fix round is `0dedb7e..8f12192`
  (`23ca9b6`, `1ea7d06`, `f7555d1`, `2a05390`, `60196ec`, `8f12192`). I checked it against plan §4.1–4.6, §3.3 item 3,
  §2.2, §2.7, DL54-01, and DL54-17 / DL54-18 as proposed on the branch. Ownership: `scripts/check_ownership.py w1-p
  v54/base` → 30 inside, 3 slice → PASS.
- **Server:** my own, `127.0.0.1:8786`, from `C:/tmp/ile_wt/v54-w1-p` at `8f12192` (the strip reads «ramo v54-w1-p ·
  8f12192»). Database `ile_v5_l4`, read-only use. Environment: `ILE_DESIGN_PREVIEW=1`, `ILE_DESIGN_PREVIEW_PORT=8786`,
  `ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`, `PGAPPNAME=ile-lane-4-ux-r2`, `--noreload`.
  `ILE_DESIGN_PREVIEW_LIVE_STATUS` and `ILE_DESIGN_PREVIEW_CHANGELOG` pointed at scratch paths under
  `C:/tmp/ile_v5_council/.work/w1p-ux-r2/`. Those files were absent except during walk 4 and were removed afterwards.
  8780, 8770–8772, the engineer's 8784 and Chrome 9222/9223 were never touched.
- **Method:** headless Chromium (Playwright), with my own profiles under `C:/tmp/ile_v5_council/.profiles/w1p-ux-r2/`.
  Every series was lock-gated with `lock_gate.py`; it waited four times (20 s, 115 s, 125 s, 15 s). An init script
  collected `securitypolicyviolation` events in the landing and in every framed document.
- **Credentials and writes:** no password was used, typed or stored. Authenticated pages were reached only through the
  persona switch. The only writes I caused:
  - what a sign-in writes (15 persona sign-ins), and their sign-outs;
  - one empty sign-in POST (no address, no password), answered with its errors;
  - one read-only probe: `qa-person`'s «Ma situation» form, refused before any view.
- **Evidence:** `C:/tmp/ile_v5_council/evidence/v54/w1-p/ux-r2/`, one folder per walk, each with its `report.json`:
  - `w1/`: the landing at 9 widths, the menus, ar, the phone frame, the strip following a click in the frame, the
    index, the viewer and the archive;
  - `w2/`: frame flows while signed out;
  - `w3/`: the personas;
  - `w4/`: sign-out, the refusal, council-passed surfaces, the changelog, the families;
  - `w5/`: the way in through the product, the sign-in states as a persona, the strip's languages on a reserved page;
  - `w6/`: the HTTP status of every URL the index lists.

  The scripts are in `C:/tmp/ile_v5_council/.work/w1p-ux-r2/`.

## Verdict

**PASS WITH FIXES — 0 blocking, 0 major, 10 minor.**

- **Round 1 is fixed.** The blocking finding and the six majors hold in the browser. Ten of the eleven minors are fixed.
  The eleventh (m2) has its wording fixed but keeps its plain-text format (n6). Every UX-lead question below answers
  yes.
- **Three minors are claims the index makes that the owner won't see:**
  - the 404 state is Django's debug page;
  - the loader and stage states are not built yet;
  - the two sign-in states do nothing while a persona is inside.
- **One minor is a natural path** that ends on a password form, with nothing pointing to «Personas».
- **The other six are polish.**

None of these blocks the merge. n1–n4 are cheap: fix them on the branch before the merge. The rest can ride as W1-P
follow-ups. I don't need to see this again: the CD can check n1–n4 by looking at the index.

---

## 1. The baseline, item by item

| Round 1 | Now | Evidence |
|---|---|---|
| **B1** — blank frame and policy violations on any redirect or form answer | **FIXED** — every case now renders (list below) | `w2/01`–`10`, `w3/03`, `w4/01`, `w4/02b` |
| **M1** — the index's pair was never visible as a pair | **FIXED** — side by side at 1440, 1280 and 1024 (sizes below) | `w1/10_viewer_pair_*`, `w1/11_*`; leftover: n7 |
| **M2** — the index exposed 47 of 79 page types | **FIXED** — every census type is listed (counts below) | `w1/report.json` (`index_1440`), `w6/report.json` |
| **M3** — two clicks only to a persona's first page; the persona links were a trap | **FIXED** — every listed page is two clicks away (walk-through below) | `w3/01_two_clicks_deadlines_ar.png`, `w3/03_switch_company_needs.png`, `w3/report.json` |
| **M4** — a fold that did not look openable hid the public pages | **FIXED** — open with a chevron while nothing has passed; collapsed once something has, passed rows above it | `w1/09_index_1440_top.png`, `w4/08_index_passed_1440_top.png` |
| **M5** — the quick links overflowed the strip | **FIXED** — 40 of 40 rows clean (below) | `w4/report.json` (`strip`), `w4/04_strip_*`, `w4/05_*`, `w4/06_*`; trade-off: n5 |
| **M6** — the archive still handed the owner decisions V5.4 closed | **FIXED** — the framing changed (below); the notes are kept as written, as §4.2 asks | `w1/12_archive_1440_top.png` |
| m1 — wording | **FIXED** — all 13 strings of the table, file paths moved to tooltips | §4 |
| m2 — the refusal: jargon, plain text | **Wording FIXED**, format left as plain text | `w4/02b_refusal_in_frame.png` → n6 |
| m3 — «Analyse territoriale» listed as an ordinary page | **FIXED** — «… 403 per questa impresa: la pagina d’errore» | `w3/05_company_analysis_403.png` |
| m4 — the frame named by a raw path | **FIXED** — after a click in the frame: frame «Imprese — V4 + fondation», window «Imprese · V5 dal vivo · Italy Legal Entry™» | `w1/04_followed_door_1440.png` |
| m5 — «V5 ● V4 + fondation» read as a contradiction | **FIXED** — a muted «pagina:» before the state from 48 rem; below, the mark alone and the state | `w1/01_landing_fr_*` |
| m6 — «Entrer» offered for the persona already inside | **FIXED** — «dentro» on its row; «Dentro come «…»» and «Sortir» on top | `w3/04_menu_personas_company.png` |
| m7 — «Entrer» did not say where it lands | **FIXED** — «apre il suo Tableau de bord» / «apre il suo Espace entreprise» | `w1/05_menu_personas_1440.png` |
| m8 — the languages hid in «Altro» from 64 to 80 rem | **FIXED** — at 1024: fr ar it en on the row; «Altro» holds the frame, «Novità» and the build | `w1/01_landing_fr_1024x768.png`, `w1/07_menu_altro_1024.png` |
| m9 — the strip went stale after the product's own sign-out | **FIXED** — the landing is served again and names nobody | `w4/01_after_inframe_signout.png` |
| m10 — the stage states invited a submit | **FIXED** — «(senza inviare)» | index, «Stati senza credenziali» |
| m11 — the index's «Entrer» always entered in French | **FIXED in substance** — every page has its own «fr» and «ar» button. The card's main «Entrer» still enters in French, which is acceptable. | `w3/report.json` (`cards_as_doc_person`) |

**B1, the cases that now render.** No document in walks 1–5 recorded a `securitypolicyviolation`.
- **(a)** Signed out, `?page=/fr/espace-reserve/mes-documents/` → the sign-in renders in the frame
  (`/fr/compte/login/?next=…`), and the strip follows.
- **(b)** Another persona's page is now a POST that switches personas. The trap is gone.
- **(c)** The product's own «Se déconnecter» inside the frame → the home, and the strip names nobody.
- **(d)** An empty sign-in POST inside the frame → its answer renders.
- **Also:**
  - a trailing-slash 301 renders;
  - signed out, the documents app in ar → the ar sign-in;
  - the product's own language switch inside the frame is followed by the strip;
  - a link inside the frame to `/backoffice/`, or to the preview's own index, shows the stage's message, «Questa pagina
    non si apre nella cornice». Its «Apri la pagina da sola» opens the refused address; «Torna alla pagina di prima»
    works.

**M1, the measured pair.**

| Window | Desktop frame | Phone frame |
|---|---|---|
| 1440 × 900 | 991 × 620 at x 16–1007 (scale 0.687, laid out at 1440 × 900) | x 1031–1423 |
| 1280 × 800 | 831 × 520 (scale 0.576) | x 871–1263 |
| 1024 × 768 | 575 × 360 (scale 0.399) | x 615–1007 |

«1:1» draws the desktop frame at 1442 × 902. After «Chiudi» or Escape, 0 frames are left.

**M2, the counts.**
- **79 of 79** census page types are listed:
  - 41 public rows, 86 URLs;
  - 47 persona rows, 94 URLs;
  - the states;
  - the four role-only types, under «fuori dall’anteprima».
- **Every listed URL answers as its row says** (`w6`):
  - public: 84 × 200, plus the virtual forum's two announced 404s;
  - persona pages: 90 × 200, plus the four announced 403s.
- **The documents app** is framed and followed by the strip («Pièce demandée»). A reload frames it again at
  `?page=/documents/requirements/…&lang=fr` (`w3/07c`, `w3/07d`).

**M3, the clicks.**
- From the landing: «Indice» → «ar» of «Mes échéances» = **2 clicks**. `qa-doc-person` is then inside, on
  `/ar/espace-reserve/mes-echeances/` (rtl).
- As `qa-doc-person`, one click on `qa-company`'s «Mes besoins · fr» switches persona and opens that page.
- The persona inside gets links; the other personas get forms.

**M5, the rows.** Signed out and as `qa-person` (the longest name), with 0, 2, 6 and 12 council-passed surfaces, at 1440,
1366, 1280, 1024 and 390: 40 of 40 rows have a 40 px strip, no overflow, no overlap, nothing outside the window and the
state never truncated. «Superfici V5 · 15» is grouped (public pages, then each persona). One click on another persona's
passed page switches persona and opens it.

**M6, the framing.** The H1 is «Archivio della ricerca», the lead is archival, and a historical notice («Le note sono
quelle di allora …») heads the page. The «non approvato» tags are kept.

## 2. The UX lead questions, again

| Question | Answer | Evidence |
|---|---|---|
| Does `/__design-v5/` open on the live V5 home with nothing between the owner and the product but a slim strip? | **Yes.** One frame holds the real `/fr/`, under a 40 px strip, at nine widths from 320 to 1920. No banner, no picker, no catalogue. FCP is 72–132 ms warm (648 ms on the server's first request), with 0 horizontal overflow. | `w1/01_*`, `w1/report.json` (`landing_*`) |
| Is the index one click away and complete? | **One click** from 48 rem up («Indice» stands on the row); below 48 rem it is in «Altro», which the notes state. **Complete:** 79 of 79 census page types, the four role-only types listed apart, the public fold open while nothing has passed. Every URL answers as its row says. | `w1/09_*`, `w6/report.json` |
| Is the archive clearly secondary? | **Yes.** It is not on the landing's strip. It is the index's last section and the right end of the index's strip. Its title, lead and notice say «archivio»; the «non approvato» tags stay. Old addresses are forwarded (`/hero/`, `/type/`, `/compare/`, `#g-he` → `research/…`). | `w1/12_*`, `w1/report.json` (`old …`) |
| Can the owner reach every authenticated surface in two clicks without credentials? | **Yes, for every listed page.** Either «Indice» → «fr»/«ar» of the page (one POST enters that persona and opens the page), or «Personas» → «Entrer» for a persona's first page. Another persona's page is one click from the index or from «Superfici V5». The four role-only types are outside the preview by design. The natural path through the product still ends on a password form (n2). | `w3/01`, `w3/03`, `w4/06` |
| fr / ar | **Yes.** The strip's switch keeps the page, on reserved pages too, and ar frames are rtl. The product's own switch is followed. Persona pages are entered in the language chosen. «Sortir» from an ar reserved page lands on `/ar/`. The documents app takes its language from `?lang=`. | `w1/02`, `w2/08`, `w2/10`, `w3/01`, `w3/09b`, `w5/03` |
| Desktop / phone frames | **Landing: yes.** The phone is 392 × 828, centred, switched without a reload, and kept through a persona entry. **Index pair: yes**, side by side from 1024 to 1440. The phone frame is not fitted to the window's height (n7). | `w1/03`, `w1/10_*`, `w3/10` |
| Wording in plain Italian | **Yes.** The thirteen strings of m1 are in, and the plan's proper names are kept verbatim. Two nits remain (n8). | §4 |
| Nothing ranks or recommends | **Yes, in the live product.** Families are grouped by state, in the steward's order, and the scores are the ones the plan asks for. The archive's old «decide il proprietario» and «raccomandata» notes stay as written, under the historical notice (§4.2: «as it is»). | `w1/12`, `w4/09_families_board.png` |

## 3. Plan §4.6 — the items in my lens

| §4.6 item | Result | Note |
|---|---|---|
| frames load real pages only under the narrow condition | **PASS** | Every natural flow renders: redirects, a form's answer, the product's own sign-out, the read-only refusal. An address the frame may not hold shows the stage's message, never a blank frame. |
| at most one frame pair at a time, enforced by the hub's script | **PASS** | The pair is visible as a pair; 0 frames after «Chiudi» or Escape. |
| the strip paints in ≤ 1 s; the landing loads exactly one frame | **PASS** | FCP 72–132 ms warm, 648 ms cold. One frame at every width and in every flow. |
| 0 CSP violations | **PASS** | No `securitypolicyviolation` in the landing or in any framed document in walks 1–5: signed out, four personas, the sign-in POST, the refusal, the sign-out, the documents app, ar. The console's «Framing … violates frame-ancestors 'none'» lines appear only for the two addresses I refused on purpose (`/backoffice/`, the preview's own index). They are the browser logging the refusal that the stage's message then explains. |
| the research archive keeps working at its new paths | **PASS** | |
| the read-only rule, as the owner meets it | **PASS** | The probe is refused before any view, nothing changes, and the words are plain. It is still a plain-text page (n6). |

## 4. Findings

### Blocking

None.

### Major

None.

### Minor

**n1 — The index's «La 404», and the virtual forum's row, open Django's debug page, not the product's 404.**
- *Failure scenario:* in «Stati senza credenziali», «La 404 … fr» frames `?page=/fr/page-inexistante/`. The frame shows
  Django's yellow technical page, «Page not found (404)», in English, listing the URL patterns, while the strip calls it
  «La pagina 404» (`w2/07_g_404.png`). «Il forum virtuale — 404 finché il forum virtuale è chiuso» does the same in both
  languages (`w6`).
- *Cause:* the preview always runs with DEBUG on, and with DEBUG on Django answers an unmatched URL with its technical
  page: `handler404` (`core.views.error_404`) is used only when DEBUG is off. The census captured its example on 8782,
  where DEBUG is off.
- *Fix:*
  1. Add «404» to `views.STATES`. Render `core.views.error_404` under `translation.override(lang)` for `?lang=fr|ar`,
     as the 429 route is rendered.
  2. Point the index's «La 404» at `stati/404/?lang=fr` and `?lang=ar`, in a new tab like the 429.
  3. On the virtual forum's row, say «(in sviluppo: la pagina tecnica di Django)», or link it to the same state.

  Test: the index's 404 links answer 404 with `errors/404.html`, in fr and in ar.

**n2 — Signed out, the product's own way in ends on a password form, and nothing points to «Personas».**
- *Failure scenario:* on the landing, the product's «Espace réservé» (`/fr/compte/login/`), «Connexion» or any reserved
  link frames the real sign-in: «Courriel», «Mot de passe», «Connexion» (`w2/01_a_reserved_signed_out.png`). The strip
  says only «L’accesso «Il varco» · V4 + fondation». The one visible way in asks for a password, which the preview's
  rule forbids.
- *Second gap:* «Entrer» from there opens the persona's first page, not the page the owner was heading to. The sign-in's
  `next=` is dropped, because the forms in the persona list carry no `page` field.
- *Fix:*
  1. When the framed page is the sign-in and nobody is inside, show one muted line beside the state: «Per entrare senza
     password: «Personas»». Draw it in `live.strip()` for the served page, and in `follow()` when the frame arrives
     there.
  2. Give each «Entrer» form a hidden `page` field set to the sign-in's `next`, server side and from `follow()`.
     `_next` already honours a page only when it is that persona's own.

  Test: signed out, `?page=/fr/espace-reserve/mes-echeances/` shows the line, and «Entrer» as `qa-doc-person` lands on
  «Mes échéances».

**n3 — The index's two sign-in states show the dashboard while a persona is inside.**
- *Failure scenario:* as `qa-doc-person`, «Dopo l’invio, sull’accesso — Nella cornice» frames `/fr/compte/login/`.
  allauth sends a signed-in visitor on to `/fr/espace-reserve/`, so the owner sees the Tableau de bord, not the sign-in
  (`w5/02_login_state_as_persona.png`). «La scena dell’accesso» behaves the same.
- *Fix:* while a persona is inside, draw those two «Nella cornice» links as a small POST to `esci/` with
  `page=/fr/compte/login/`, labelled «Esci dalla persona e apri l’accesso». `_next` already frames a public page after
  «Sortir». Signed out, they stay links.

**n4 — Three of the «Stati senza credenziali» describe behaviour that is not built yet.**
- *Failure scenario:* the index says:
  - «Dopo l’invio … la chiave gira una volta e si ferma»;
  - «L’ingresso, dopo «Entrer» … accende la porta del marchio … una volta per sessione»;
  - «La scena dell’accesso … la scena risponde a ogni passo».

  None of it exists in this tree:
  - there is no loader: no `static/js/src/loader.js`, no `templates/components/loader.html`;
  - there is no release hook: `apps/accounts/signals.py` has no `user_logged_in` receiver;
  - the sign-in's stage has no script: «The door is complete and still from the first frame»
    (`templates/allauth/layouts/entrance.html`).

  The owner who follows the index sees none of it, and is told it happens. W1-D builds the loader and the release;
  W2-B wires the engage and the stage.
- *Fix:* name each item's family — «W1-D», «W1-D + W2-B», «W2-B» — and add «in arrivo» while that family is not «v5» in
  `live_status.json` (`status.families`). For example: «— in arrivo con W1-D (il caricatore «Lume»): oggi la pagina non
  lo mostra ancora.»

  Test: without the file, the three items say «in arrivo»; with the family at «v5», the note goes.

**n5 — At the owner's 1440 the strip no longer shows the build or the claim.**
- *Failure scenario:* round 1 showed «Italy Legal Entry™ — V5, la migliore di oggi» and «ramo … · commit» from 90 rem.
  To fit the worst case (the longest persona name, «V5 — council-passed», «Superfici V5»), the claim now needs 120 rem
  and the build 100 rem. Yet at 1440, signed out with nothing passed, 404 px of the row stay empty: the state ends at
  x 381 and the languages start at x 785 (`w1/report.json`, `landing_1440`).
- *Measured free space at 1440:*

  | State of the row | Free px |
  |---|---|
  | signed out, nothing passed | 404 |
  | a persona inside | 257 |
  | council-passed surfaces, signed out | 233 |
  | all three at once | 79 |

  The build needs about 187 px and the claim about 108 px. Plan §4.1 puts the tag, its commit and its date on the
  strip; at 1440 they are one click away, in «Novità».
- *Fix:* tier by what the row holds, not by the worst case.
  1. `live.strip()` adds the modifiers `dp-strip--persona`, `dp-strip--quick` and `dp-strip--v5`; `follow()` toggles
     `--v5` with the state.
  2. The build keeps round 1's 90 rem tier unless a persona is inside together with surfaces or a «V5» state.
  3. The claim keeps it only when no modifier applies.
  4. Extend `test_the_strip_never_outgrows_its_row_with_council_passed_surfaces` to assert that the build is visible at
     1440, signed out with nothing passed.

**n6 — The read-only refusal is still a plain-text page inside the product.**
- *Failure scenario:* as `qa-person`, «Ma situation» submitted inside the frame shows three sentences in the browser's
  default monospace face on white, under the strip (`w4/02b_refusal_in_frame.png`). The words are right now (m2), but
  the page is a dead end; its only way back is the browser's «Indietro».
- *Fix (the response stays `text/plain`, as the security review accepted):*
  1. In `framed()`, when the framed document's `contentType` is `text/plain` and its text starts with «Anteprima V5 —
     sola lettura», hide the frame.
  2. Show those sentences in the stage's message box (the one refused frames use), with «Torna alla pagina di prima» →
     the page before the refused submit.
  3. Detect the refusal before `follow()`, so that `lastPage` is not overwritten.

  Browser test: the refusal shows in the box, and «Torna alla pagina di prima» brings back the form's page.

**n7 — The viewer's phone frame is not fitted to the window's height.**
- *Failure scenario:* the desktop frame is scaled to fit; the phone frame is always 392 × 846. The part below the window
  (`w1/report.json`, `pair_*`):

  | Window | Phone frame below the window |
  |---|---|
  | 1440 × 900 | 10 px |
  | 1280 × 800 | 110 px (736 of 846 visible) |
  | 1024 × 768 | 142 px |

  A phone page's bottom edge — a cookie notice, a sticky action — shows only after scrolling the viewer.
- *Fix:* in `fit()`, scale the phone too when the height is short: `min(1, available height / 846)`, with the same
  wrapper technique, its page still laid out at 390 px. Compute the desktop's width budget from the phone's scaled width.
  Extend `test_the_viewer_shows_both_frames_of_the_pair_at_the_owner_s_widths` to assert that both frames' bottoms are
  inside the window at 1280 × 800.

**n8 — Wording: the singular and the dates.**
- *Failure scenario:* the fold reads «V4 + fondation 1 famiglie» (`w4/09_families_board.png`); with one page left it
  would read «1 pagine pubbliche». The plain-Italian sentences carry ISO dates: «Aggiornato il 2026-10-05», «… ·
  8f12192 · 2026-10-05».
- *Fix:* use `famigli{{ n|pluralize:"a,e" }}` and `pagin{{ n|pluralize:"a,e" }} pubblic{{ n|pluralize:"a,he" }}`. Parse
  the dates in `live.py` and print them with `|date:"j F Y"` under the Italian override («5 ottobre 2026»), keeping the
  ISO value in the `datetime` attribute.

**n9 — Inside the «V4 + fondation» fold, every row repeats the fold's chip.**
- *Failure scenario:* 41 identical «● V4 + fondation» chips sit under a summary that already says «V4 + fondation · 41
  pagine pubbliche» (`w1/09_index_1440_top.png`). While nothing has passed they carry no information, and they push the
  titles out of line (some wrap onto a second line).
- *Fix:* in `_row.html`, print the chip only when `row.state == "v5"`, as the persona cards already do.

**n10 — «V5 dal vivo» on the index forgets the page the owner left.**
- *Failure scenario:* on the landing at «Mes échéances», «Indice» then «V5 dal vivo» lands on the home. The page left is
  two «Indietro» away (`w5/report.json`, steps 4 and 4b).
- *Fix:* the strip's «Indice» link carries the current page and frame (`?da=…`), kept current by `follow()` as it keeps
  «Apri a parte». The index's «V5 dal vivo» returns to `landing_url(page_param(da))`.

## 5. Clicks from the landing, measured

| Target | Round 1 | Now |
|---|---|---|
| a public page, through the index | 3 | **2** («Indice», the language link) |
| a persona's first page | 2 | 2 («Personas», «Entrer») |
| any other listed page of a persona | 3–4 | **2** («Indice», «fr» / «ar») |
| another persona's page while one is inside | a blank frame, or the wrong view | **2** from the landing, 1 from the index |
| a council-passed surface, once there are some | — (the row overflowed) | **2** («Superfici V5», the page) |
| the documents app, the Academy, the Guichet, detail pages, account pages | 3–4, not listed | **2** (listed now) |
| the fr ↔ ar switch | 1, but 2 from 64 to 80 rem | 1 down to 64 rem; 2 below |

## 6. What works, and stays

- **The landing is the product.** One frame, the full window, a 40 px strip outside the page, and nothing in between.
  The strip holds one row of 40 px at every width I measured and in every state of the row.
- **The frame never goes blank in a natural flow:**
  - redirects render;
  - a form's answer renders;
  - the product's own sign-out renders and resets the strip;
  - the read-only refusal shows where it happened;
  - an address the frame may not hold is explained, with the way out and the way back.
- **The persona switch is two clicks from anywhere,** in either language, without a password. It never drifts the
  personas, and the strip always says who is inside.
- **The index is a complete, truthful map of the census,** apart from n1 and n4. Every listed address answers what its
  row says.
- **The archive** says what it is, keeps its notes as they were written, and keeps its old addresses working.

## 7. Honest limits

- **Browser coverage:** Chromium headless on Windows only. No WebKit, no Firefox, no real phone, no screen reader.
  Accessibility and security belong to their own reviewers; I touched them only where the owner meets them.
- **Suites:** I did not re-run the W1-P suites. The reviewers' test database (`test_ile_v5_l9`) is shared by the
  re-checking reviewers, and concurrent runs deadlock. The engineer's run 2 log
  (`E/w1-p/fix-1/s2_w1p_suites_r2.log`) shows 480 passed. The eleven tests the notes name for the UX fixes exist in
  `tests/frontend/test_design_preview.py`.
- **The «V5 — council-passed» states** were seen only through a scratch `live_status.json` that my own server read
  (walk 4), removed afterwards. The steward's file does not exist yet.
- **Public forms were not submitted** (contact, the enquiry forms, the forum registration, «Commencer» of the
  questionnaire): each would write to the clone. The mechanism they rely on — a form's answer shown in the frame — is
  verified by the empty sign-in POST and by the refusal.
- **Scope of the walks:** I measured the flows the owner meets. I did not re-measure the a11y fixes (focus, forced
  colours, text spacing), beyond seeing that the strip keeps its row.
