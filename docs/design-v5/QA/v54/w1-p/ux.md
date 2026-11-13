# W1-P · Preview as the live product — independent UX review

Italy Legal Entry™ design V5 · V5.4 «EXECUTION MODE» · 5 October 2026 · independent reviewer, lens **UX (council lead
for W1-P)**, label `w1p-ux`. I built nothing in this family.

- **Reviewed:** branch `v54-w1-p`, `v54/base..b3e991c` (5 commits: `1338303`, `aab76d2`, `7bb39e5`, `bb1ba5b`,
  `b3e991c`), against plan §4 (4.1–4.6), §3.3 item 3, §2.2, §2.7 and DL54-01. Ownership:
  `scripts/check_ownership.py w1-p v54/base` → 24 inside, 2 slice → PASS.
- **Server:** my own, `127.0.0.1:8786`, from `C:/tmp/ile_wt/v54-w1-p`, `ile_v5_l4` (read-only use), `ILE_DESIGN_PREVIEW=1`,
  `ILE_DESIGN_PREVIEW_PORT=8786`, `ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`, `PGAPPNAME=ile-lane-4-ux`,
  `--noreload`. 8780, 8770–8772 and Chrome 9222/9223 were never touched.
- **Method:** headless Chromium (Playwright) with my own profiles under `C:/tmp/ile_v5_council/.profiles/w1p-ux/`, every
  series lock-gated (`lock_gate.py`; it waited twice for the benchmark lock). No password was used, typed or stored: the
  authenticated pages were reached only through the persona switch. The only write I caused is what a sign-in writes
  (6 persona sign-ins: session rows, `last_login`, the audit row) and one sign-out; the read-only probe was a POST to a
  path that does not exist (nothing to write even if it had passed).
- **Evidence:** `C:/tmp/ile_v5_council/evidence/v54/w1-p/ux/` — `w1/` (landing, strip, menus, index, viewer, archive;
  `report.json`), `w2/` (persona switch; `debug_blank.log`, `redirect_experiment.json`), `w3/` (in-frame sign-out),
  `w4/` (in-frame POST, the documents app), `w5/` (the strip with council-passed links).

## Verdict

**FAIL — one blocking finding, six major, eleven minor.** Every fix stays inside W1-P's slice. The shape is right:
`/__design-v5/` opens straight on the real home, under a 40 px strip and nothing else; fr/ar, the phone frame and the
persona switch work on their main paths; the archive has left the main path. What fails is the frame in natural flows.
Any redirect or form answer inside the frame leaves the owner looking at a **blank white frame**, which also breaks
§4.6's «0 CSP violations». Fix the blocking item and the majors, then ask for a re-review: the blocking fix needs a
browser test of its own (below).

---

## 1. The UX lead questions, one by one

| Question | Answer | Evidence |
|---|---|---|
| Does `/__design-v5/` open on the live V5 home with nothing between the owner and the product but a slim strip? | **Yes.** One frame, the real `/fr/` (lang `fr`, `ltr`), filling the window under a strip of exactly 40 px (1440 × 860 at 1440 × 900), at 1440, 1280, 1024 and 390. No banner, no catalogue, no picker. FCP 36–60 ms, 0 horizontal overflow. | `w1/01_landing_fr_*.png`, `w1/report.json` |
| Is the index one click away and complete? | **One click: yes** from 48 rem up («Indice»); below 48 rem it takes two («Altro» → «Indice»). **Complete: no.** It exposes 47 of the 79 page types in W1-0's census. Of the 32 absent, 28 can be reached by one of the four personas or by a visitor (M2). The 33 public pages it does list sit behind a collapsed fold that does not look openable (M4). | `w1/08_index_1440_full.png`; census comparison in M2 |
| Is the archive clearly secondary? | **In placement: yes.** It is not in the landing's strip, it is the index's last section, and its masthead says «archivio della ricerca». **In copy: no.** Its H1 is still «Le superfici da guardare». It still says that decisions are the owner's, and that nothing is propagated without his approval (M6). | `w1/12_archive_1440_top.png` |
| Can the owner reach every authenticated surface in two clicks without credentials? | **Only each persona's first page** («Personas» → «Entrer»). Any other page takes 3–4 clicks. The index's persona links fail before «Entrer» (a blank frame today, the login form after the B1 fix), and they open the wrong view while another persona is in (M3). | `w2/` steps A–D |
| fr / ar | **Yes, on the main paths.** The strip's language links keep the page. The ar frame is `rtl`. «Entrer» from an ar page lands in the ar console (`/ar/espace-reserve/entreprise/`). «Sortir» from a reserved ar page lands on `/ar/`. The console's own language links work inside the frame. Two gaps: the index's «Entrer» always enters in fr (m11), and from 64 to 80 rem the language switch hides in «Altro» (m8). | `w1/02`, `w2/E`, `w2/F`, `w2/G`, `w2/H` |
| Desktop / phone frames | **The landing: yes.** The phone is 392 × 828, centred, and switches without a reload. **The index's pair: no.** At 1440 the phone frame sits at x = 1482, so none of it is visible (M1). | `w1/03`, `w1/11_viewer_pair_1440.png` |
| Wording in plain Italian | **Mostly.** The proper names the plan mandates are kept verbatim. The jargon and file paths in m1 are not plain Italian. | §4 below |
| Nothing ranks or recommends | **The live product: yes.** Nothing ranks or recommends. «la migliore di oggi» is the directive's own «current best V5». Families are grouped by state, not ordered by score. **The archive: no.** It still recommends a viewing order («nell'ordine in cui vanno guardati») and hands choices to the owner (M6). | — |

## 2. Plan §4.6 — the items in my lens

| §4.6 item | Result | Note |
|---|---|---|
| frames load real pages only under the narrow condition | **PASS for GET pages; FAIL for UX** | Under the narrow condition a real page renders. A redirect inside the frame is upgraded to https and refused by `frame-src 'self'`. A POST answer is refused by `frame-ancestors 'none'`. Either way the owner sees an empty frame (B1). |
| at most one frame pair at a time, enforced by the hub's script | PASS (the cap holds) | The pair is not visible as a pair at 1440 (M1). |
| the strip paints in ≤ 1 s; the landing loads exactly one frame | PASS | FCP 36–60 ms; 1 frame at every width. |
| 0 CSP violations | **FAIL** | 0 on the plain landing, the index and its viewer. **Violations of three directives in four measured flows** (B1): `frame-src 'self'` (https-upgraded redirect), `form-action 'self'` (in-frame sign-out), `frame-ancestors 'none'` (in-frame POST answer). |
| the research archive keeps working at its new paths | PASS | `/__design-v5/hero/` → `research/hero/`; `/__design-v5/#g-he` → `research/#g-he`. |
| refusals and guards: the read-only rule as the owner meets it | PASS (behaviour), minor wording | The refusal shows inside the frame and nothing is changed. The text is a plain-text dead end full of jargon (m2). |

## 3. Findings

### Blocking

**B1 — Any redirect or form answer inside the live frame leaves a blank white frame, with CSP violations. §4.6 «0 CSP
violations» fails.**

- *Failure scenarios (measured):*
  - **(a)** Signed out, the index's «Mes pièces · fr» of `qa-doc-person`. The frame asks for
    `/fr/espace-reserve/mes-documents/`, gets a 302 to the login, and that hop is upgraded to `https://127.0.0.1:8786/`.
    Console: «Framing 'https://127.0.0.1:8786/' violates … "frame-src 'self'"». `ERR_BLOCKED_BY_CSP`, white frame
    (`w2/A_signed_out_card_link.png`, `w2/debug_blank.log`).
  - **(b)** As `qa-doc-person`, `qa-company`'s «Mes besoins · fr» (a redirect): white frame (`w2/D_other_persona_link.png`).
  - **(c)** The product's own sign-out inside the frame (`/fr/compte/logout/`, then its button). Console: «Sending form
    data … violates "form-action 'self'"» and the `frame-src` line again. White frame. The server has already signed
    out, yet the strip still says «Personas • Personne avec dossier» (`w3/03_after_in_frame_signout.png`,
    `w3/report.json`).
  - **(d)** Any in-frame POST answered 200: the login form submitted empty, by script (no address, no password).
    `ERR_BLOCKED_BY_RESPONSE`, «… violates "frame-ancestors 'none'"», white frame (`w4/02_after_in_frame_post.png`).
  - *Predicted from the same mechanism, not exercised (each would write to the clone):* «Commencer» of the
    orientation questionnaire (a POST, behind the hero's primary CTA); every public form (contact, the three enquiry
    forms, forum registration, newsletter); sign-up; password reset; any link that answers a redirect (trailing slash,
    `/`, an expired session).
- *Cause:* the global CSP carries `upgrade-insecure-requests` (`config/settings/base.py:360`). On this plain-http
  server Chromium upgrades the redirect hops of the frame's navigations to https, and `'self'` then refuses them. And by
  plan §4.4 a POST answer is never relaxed, so it can never be framed. The engineer's browser tests never framed a
  redirect or an ordinary POST answer: only GET pages answering 200, and the preview's own relaxed refusal.
- *Experiment (nothing changed on disk):* with `upgrade-insecure-requests` removed from the **landing's** CSP alone (the
  header rewritten in the browser), case (a) lands correctly on the login inside the frame, with no violation
  (`w2/redirect_experiment.json`, «strip-landing»).
- *Fix (inside W1-P's slice):*
  1. Drop the directive wherever the preview frames. On `views.landing` and `views.index`, add
     `@csp_replace({"upgrade-insecure-requests": None})`: django-csp 4.0 omits a directive whose replacement is `None`
     (`csp/utils.py: build_policy`). In `frames.relax()`, add `replace["upgrade-insecure-requests"] = None`: a redirect
     that the framed document starts itself (case c) is upgraded by that document's own policy. Production is untouched,
     because the frame exception exists only under DEBUG and the flag. **Verify the second half with a browser test**
     (my header-rewrite experiment cannot keep the `Sec-Fetch-*` headers the exception needs). The test: signed out,
     `?page=/fr/espace-reserve/` ends on the login rendered in the frame; the in-product sign-out ends on the home
     rendered in the frame; 0 `securitypolicyviolation`.
  2. Never leave a blank frame. On the frame's `load`, when `frame.contentWindow.location` cannot be read (the
     `catch` branch, which today returns silently) or the frame is `about:blank`, show a message held in the stage of
     `landing.html`. Proposed text: «Questa pagina non si apre nella cornice: è la risposta a un invio, oppure un
     indirizzo che la cornice non tiene.», with «Apri la pagina da sola» (pointing at the last page followed) and «Torna
     alla pagina di prima». Cover it with a browser test (an empty login POST inside the frame shows the message, never
     a white frame). That covers the POST answers the plan keeps unframeable. The security reviewer may instead accept
     relaxing a POST answer under the same narrow condition (`Sec-Fetch-Site: same-origin`, loopback, own Host), which
     would make the product's forms usable in the frame.
  3. The strip goes stale after an in-product sign-out (case c): see m9.

### Major

**M1 — The index's «pair» never shows as a pair at the owner's width.**
- *Failure scenario:* at 1440 × 900, «Desktop 1440» then «Telefono 390» on «La home · fr». The desktop frame is
  1442 × 902 (cut at the right and at the bottom). The phone frame lands at x = 1482, so none of it is visible. Both
  buttons read as pressed; pressing «Telefono 390» changes nothing on screen (`w1/11_viewer_pair_1440.png`,
  `viewer_pair_1440` in `w1/report.json`). The pair only fits in a window about 1890 px wide.
- *Fix:* keep the desktop frame's own viewport at 1440 CSS px, but draw it scaled to fit beside the phone. Put a wrapper
  of the scaled size around it and give the frame `transform: scale(var(--dp-scale)); transform-origin: 0 0`, with
  `--dp-scale = min(1, (innerWidth − 392 − 3 × gap) / 1442, (innerHeight − bar − 2 × gap) / 902)`, set by the viewer's
  script on open and on `resize`. Add a «1:1» toggle for true size. Media queries inside the frame are unaffected
  (the frame still lays out at 1440). Test: both frames' visible width > 0 at 1280 and 1440.

**M2 — The index is not complete.**
- *Failure scenario:* compared with W1-0's census (`C:/tmp/ile_v5_council/evidence/v54/w1-0/before/PAGE_TYPES.json`,
  79 page types), the index exposes 47. Of the 32 absent, 28 can be reached by a persona or a visitor; the other 4 need
  role accounts the preview does not offer. The 28:
  - **console:** the whole **Guichet numérique** (list, detail, new request); the whole **Academy** (catalogue,
    course, «Mes formations», enrolment); the whole **documents app** (`/documents/`, upload, upload refused by the
    terms, requirement detail); the request detail; «Mes dossiers»; the company's new-need form. The organisation
    bridge (`qa-company` at `/fr/espace-reserve/`) is listed only as the persons' dashboard, not on `qa-company`'s card;
  - **account:** e-mail addresses, password change, 2FA, delete request, logout confirmation;
  - **public and states:** pathway sheet, living topic, glossary term, «demande transmise», forum registration,
    orientation «reprendre», password-reset done, verification sent, 410.

  The documents app cannot even be framed by address. `?page=/documents/` answers 400 with «La pagina chiesta non è
  una pagina di questo sito», which is false. Reached through the console, the frame shows the requirement page but the
  strip does not follow: the state and «Apri da sola» stay on «Mes documents», and a reload goes back there
  (`w4/report.json`). These pages also have no surface key, so the steward can never mark them «V5 — council-passed».
  When W3's families pass, the strip would keep saying «V4 + fondation».
- *Fix:* derive `PUBLIC_PAGES` / `PERSONA_PAGES` from the census, or mirror it with one row per page type, including
  the census's example URLs for detail pages (pathway `salaried_work`, glossary `permesso_di_soggiorno`, living
  `logement`, requirement `70d79bd5…`, course `italien-a1`, and the rest). Accept the documents app's non-prefixed
  paths: `page_param` should allow `^/documents/`, and the script's `prefix` test should follow any same-origin path
  outside `/__design-v5/`, `/backoffice/`, `/static/`, `/media/`, `/api/`. List the role-account pages (helpdesk queue,
  dispatch, selection, Forum permanent's 503) under one line: «fuori dall'anteprima: nessuna persona per questi ruoli».
  Add a test that the index's URLs cover the census.

**M3 — Authenticated pages are two clicks away only on the first page, and the index's persona links are a trap.**
- *Failure scenarios:*
  - **(a)** Signed out, any page link of a persona card: a blank frame (B1). After B1's fix it becomes the real login
    form, asking for an address and a password, against the rule that no credential is ever typed.
  - **(b)** As persona A, a page of persona B: a blank frame, or A's view of B's address.
  - **(c)** «Entrer» always lands on the persona's home (`views._next` ignores the page asked for). Reaching «Mes
    échéances» from the index therefore takes «Entrer» → (landing) → «Indice» → the link: 3 clicks after the index,
    4 from the landing. From the landing the rail makes it 3.
  - **(d)** The index's «Entrer» always posts `lang=fr`.
- *Fix:* while a persona is not the one inside, render each of its page links as a small POST form to
  `accedi/<persona>/`, carrying `page` (one per language: «fr», «ar»). `_next` honours `page` only if it equals one of
  that persona's own `PERSONA_PAGES` URLs, in any language; otherwise it uses the home, as today. One click then enters
  the persona and opens that page in that language. Every listed authenticated page becomes «Indice» → page = **two
  clicks** from the landing. The active persona's links stay plain links. Test: as nobody, one POST from a card ends on
  `?page=<that page>` with the persona inside; a foreign `page` falls back to the home.

**M4 — The index's public pages are hidden behind a fold that does not look openable.**
- *Failure scenario:* the index's first section reads «Nessuna pagina pubblica ha ancora passato il consiglio.» Below
  it is a box, «● V4 + fondation 33 pagine pubbliche». The `<summary>` is `display: flex`, which removes the
  disclosure triangle, and `.dp-index__summary` adds no chevron, so nothing says it opens. The same goes for «Le chiavi
  delle superfici, per lo steward» (`w1/08_index_1440_top.png`). Until a public page passes (Wave 2), every public page
  is one hidden click deeper than the plan's «one click away».
- *Fix:* give `.dp-index__summary` the strip's chevron (`::after`, rotating on `[open]`). Open the public fold by
  default while nothing has passed: `<details class="dp-index__fold"{% if not passed %} open{% endif %}>`. That keeps
  the plan's «grouped apart, collapsed» for the steady state.

**M5 — The strip's council-passed quick links overflow the row as soon as surfaces pass.**
- *Failure scenario:* the server's own landing, with the quick-link markup of `_strip.html` injected for N passed
  surfaces (nothing written to `live_status.json`; `w5/report.json`):
  - N = 2 (the Wave-2 flagships, «La home» and «L'accesso «Il varco»»): the row overflows by **48 px at 1440**.
    «Apri da sola» is cut off and the page gets a horizontal scroll (`w5/strip_quick2_1440.png`).
  - N = 4: +53 px at 1366, +274 px at 1440.
  - N = 6: up to +449 px. «Personas», «Novità» and «Indice» are pushed off-screen (`w5/strip_quick4_1440.png`).

  The persona's name (up to 11 rem) and «V5 — council-passed» (longer than «V4 + fondation») make it worse. Persona
  pages count too: `strip()` takes every passed URL in the current language, so by Wave 3 the list is long. The engineer
  measured the strip only with zero quick links.
- *Fix:* never inline. Make one `<details class="dp-strip__menu">` labelled «Superfici V5 (n)», drawn only when n > 0,
  listing the passed surfaces in the current language, grouped public / persona. Add a test for the row width with 2,
  6 and 12 passed surfaces at 1280 and 1440, signed out and with the longest persona name.

**M6 — The archive still hands decisions to the owner that V5.4 closed, and still reads as the place to look.**
- *Failure scenario:*
  - The top notice says «O59 (le immagini) e O67 (il primo schermo) sono decisioni aperte del proprietario, e nessuna
    famiglia V5 viene propagata prima della sua approvazione». That is false under V54 l.30 (propagation without
    per-family approval) and V54 l.9 (the hero: «do not ask E2 vs E3 again»).
  - Eight catalogue notes say «decide il proprietario» or «la scelta è del proprietario» (`services.py:874`, `997`,
    `1104`, `1171`, `1370`, `1392`, `1502`, `1665`: type systems, the hero, the loader, navigation).
  - The page's H1 is «Le superfici da guardare», and its lead promises «l'ordine in cui vanno guardati».

  V54's «never "choose A/B/C/D"» therefore still reaches the owner, one click from the index.
- *Fix:* plan §4.2 says «as it is», so keep every note as written, and change only the framing:
  - H1: «Archivio della ricerca».
  - Lead: «I prototipi e le maquette da cui la V5 è stata decisa, conservati come erano, per tracciabilità.»
  - Replace the warning with one historical line: «Le note sono quelle di allora (fino al 4 ottobre 2026): dove dicono
    «decide il proprietario», con la V5.4 decide il consiglio, e una famiglia approvata si propaga senza attendere. Il
    prodotto V5 di oggi è nella pagina principale.»
  - Keep the «prototipo di ricerca — non approvato» tags.

### Minor

**m1 — Wording that is not plain Italian.** Each item: the string → a plainer one. The plan's proper names (V5 —
council-passed, V4 + fondation, Personas, Entrer, Sortir, the persona names) stay verbatim.

| Where | Now | Proposed |
|---|---|---|
| strip, «Novità» and «Altro» panels | «Servito» | «Versione in uso» |
| `_personas.html` | «Le pagine che scrivono rispondono 403.» | «Ogni invio che cambierebbe dei dati viene fermato.» |
| `_personas.html` (warn) | «… (soltanto ile_v5 e le copie dei cantieri)» | «… (soltanto il database dell'anteprima e le sue copie)» |
| `_changelog.html` | «Lo steward non ha ancora scritto il suo registro (docs/design-v5/CHANGELOG_V54.md).» | «Ancora nessuna novità registrata.» (the path in a `title`) |
| index, head note | «Il registro dello stato (C:/tmp/…/live_status.json) non c'è ancora: ogni superficie è «V4 + fondation».» | «Nessuna superficie ha ancora passato il consiglio: per ora ogni pagina è «V4 + fondation».» (the path in the steward's fold) |
| index, lead | «… soltanto quando lo dice il registro dello steward» | «… soltanto quando il consiglio l'ha approvata» |
| index, personas | «… ogni invio che scriverebbe risponde 403 …» | «… ogni invio che cambierebbe dei dati viene fermato …» |
| index, states | «L'ingaggio, all'accesso» · «Il rilascio» · «Gli stati del palco» · «accende la porta sul marchio della colonna» · «il palco risponde» | «Dopo l'invio, sull'accesso» · «L'ingresso, dopo «Entrer»» · «La scena dell'accesso, mentre si compila» · «accende la porta del marchio, nella colonna di sinistra» · «la scena risponde» |
| index, V4 | «(main, fase 3)» · «Le due sessioni non si toccano: questo server ha cookie con nomi propri.» | «(il sito di oggi)» · «Entrare qui non vi fa uscire di là, e viceversa.» |
| persona notes | «le pagine mostrano la porta delle condizioni» · «ogni regione vuota dice che cosa fare» | «le pagine chiedono di accettare le condizioni» · «ogni riquadro vuoto dice che cosa fare» |
| strip | «Apri da sola» | «Apri a parte» (the tooltip keeps the full sentence) |
| 400 of `?page=` | «… la cornice tiene soltanto un indirizzo che comincia con /fr/, /ar/, /it/ o /en/» | after M2's fix, also /documents/: «… un indirizzo di questo sito (le pagine in /fr/, /ar/, /it/, /en/ e /documents/)» |

**m2 — The read-only refusal is a plain-text dead end with jargon.** As `qa-company`, a POST shows, in a monospace
default face, «non scrive: POST /fr/espace-reserve/… non è stato eseguito», «copie dei cantieri», «?état=»
(`w2/J_refusal_in_frame.png`). *Fix:* wording — «Anteprima V5 — sola lettura. Questa azione non è stata eseguita e
nulla è cambiato: le persone di prova restano uguali per chi guarda dopo. Per tornare indietro usate «Indietro» del
browser; per uscire dalla persona, «Sortir» nella barra in alto.» If the security reviewer agrees, serve it as minimal
HTML with a «Torna alla pagina» link, built from a same-origin `Referer` path.

**m3 — «Analyse territoriale» is listed as an ordinary page of `qa-company`, but that persona gets a 403** («Accès non
autorisé», `w2/I_company_analysis.png`; W1-0's census uses it as its 403 sample). *Fix:* label the entry «Analyse
territoriale — 403 per questa impresa (la pagina d'errore)», or move it to «Stati senza credenziali».

**m4 — The frame's accessible name becomes a raw path.** After the first load, `follow()` sets `frame.title = page + …`
(«/fr/ — V4 + fondation»), and the tab is always «V5 dal vivo · Italy Legal Entry™». *Fix:* in `follow()`, use the
framed document's title (`frame.contentDocument.title`) for the frame's `title`, and set `document.title` to «<that> ·
V5 dal vivo».

**m5 — «V5 ● V4 + fondation» side by side reads as a contradiction** (390 and the narrow strip). *Fix:* a small muted
prefix inside the chip, «pagina: V4 + fondation», which keeps the label verbatim.

**m6 — The persona menu offers «Entrer» for the persona already inside** (`w2/G_personas_menu_signed_in.png`). *Fix:*
show «dentro» in place of the button on the current row (the index cards already do).

**m7 — «Entrer» does not say where it lands.** *Fix:* a muted line under each persona: «apre il suo Tableau de bord»
or «apre l'Espace entreprise».

**m8 — From 64 to 80 rem the languages and the frame switch both go into «Altro», so the fr/ar switch, the review's
main task, takes two clicks.** Measured at 1024: about 470 px of the row are free. *Fix:* keep the language links
visible down to 64 rem and move only the frame switch, «Novità» and «Apri da sola» into «Altro». Below 48 rem
«Indice» needs two clicks; that is acceptable on a loopback-only desktop tool, but say so in the notes.

**m9 — After an in-product sign-out the strip keeps the persona's dot and name until a reload** (case B1-c; it stays
true once the frame renders). *Fix:* in `follow()`, when the framed page carries no account menu (or reaches the home
after a POST to `…/compte/logout/`), reload the landing at `landingUrl(page)`, so the strip is rendered again with the
session as it is.

**m10 — «Gli stati del palco … Nella cornice» invites typing into the login inside the frame, and Enter blanks it**
(B1-d). *Fix:* add «(senza inviare)» to the item. B1's fallback message covers the rest.

**m11 — The index's «Entrer» always enters in French** (`<input name="lang" value="fr">`). *Fix:* solved by M3's
per-language buttons. Otherwise, carry the language of the last page framed.

## 4. Clicks from the landing, signed out (measured)

| Target | Today | After M3 / M4 |
|---|---|---|
| a public page, through the index | 3 («Indice», open the fold, the link) | 2 |
| a public page, through the product's own navigation in the frame | 1–2 | 1–2 |
| a persona's first page | **2** («Personas», «Entrer») | 2 |
| any other listed page of a persona | 3 (… + the rail) or 4 (… «Indice», the link) | **2** («Indice», «fr»/«ar» of that page) |
| a page the index does not list (Guichet, Academy, documents app, details, account) | 3–4, through the product only | 2, once M2 lists it |

## 5. What works, and stays

- The landing is the product. The real home sits in one frame, full window, under a strip of exactly 40 px that is
  outside the page. There is no interstitial. The strip paints at 36–60 ms.
- The strip's layout holds from 1920 down to 390 with zero quick links. Its menus are `<details>`, close on Escape or
  a click elsewhere, and only one is open at a time.
- Languages: the strip keeps the page; ar is RTL; the persona switch keeps the language; «Sortir» lands on the right
  public page.
- The persona switch: two clicks, no password, the persona's name and dot in the strip, and a refusal that changes
  nothing.
- The archive's old addresses and the hub's old anchors are forwarded.
- Wording elsewhere is clean Italian. Nothing in the live product ranks or recommends.

## 6. Honest limits

- Chromium headless on Windows only. No WebKit or Firefox, no real phone, no screen reader. Accessibility and security
  are for their own reviewers; I touched them only where the owner meets them.
- Case B1-d's form-flow consequences (questionnaire, enquiry forms, sign-up) are predicted from the measured mechanism.
  I did not exercise them, because each would write to the clone.
- B1's fix is verified for the landing half only (header rewrite in the browser). The framed-document half needs the
  browser test described in B1.
- The «V5 — council-passed» state was not seen live: `live_status.json` is the steward's and is absent. M5 was measured
  by injecting the template's own quick-link markup into the server's response.
- I did not re-run the W1-P suites: the reviewers' test database `test_ile_v5_l9` is shared, and concurrent runs
  deadlock. The engineer's logs show 395 passed, 0 skipped, and none of the scenarios in B1 is among them.
