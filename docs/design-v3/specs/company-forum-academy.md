# DESIGN V3 — SPEC DI SUPERFICIE: `company-forum-academy`

Area `company-forum-academy` · **round 2**, 24 settembre 2026 · Vincolanti: `DESIGN_SYSTEM_V2.md`,
`MOTION_SYSTEM.md`, `BRAND_ASSETS.md` §1, `apps/cms/forbidden.py`.
Superfici: `/fr/espace-reserve/entreprise/…` (`templates/companies/*`) · `/fr/forum/` (`templates/forum/*`) ·
`/fr/espace-reserve/formation/…` (`templates/academy/*`).
Coordinata con le spec sorelle: la pastiglia è di `badges.md` (`v3/chip.css`), i bottoni di `buttons.md`
(`v3/buttons.css`), le cuciture e `.chapter--dark` di `scroll.md`, `data-mode` e `{% block page_mode %}` di
`backgrounds.md`, la fotografia e `{% plate %}` di `imagery.md`, la shell di `platform-shell.md`.
**Qui non si ridefinisce nulla di loro** — e questa volta è vero anche per il **focus**, che nel round 1
avevo ridefinito (§0, DEROGA 1).

**Riproduzione delle misure di questo round.** Nessun file del repository è stato toccato per scrivere questo
documento. Chromium headless di Playwright dal `.venv`, **browser proprio, mai la porta 9222**,
`device_scale_factor=1`, viewport 1440×900 · 390×844, `locale` `fr-FR` e `ar`. Sessioni create lato server
(nessuna password digitata) per `seed-company@example.test` e `seed-person@example.test`. Il foglio candidato è
stato servito come `<link>` **same-origin** intercettando `/static/css/__candidate_round2.css` con
`page.route()`: l'iniezione `<style>` è stata **rifiutata dalla CSP** — provato in pagina questo round
(`style-src 'self'`: un `<style>` iniettato non applica, il colore sonda resta quello ereditato).
**Le rotte autenticate rispondono solo su :8770**; il Forum pubblico risponde su entrambe **e non allo stesso
modo** (§1.9). Script: `…/scratchpad/{measure.py, measure2.py, measure3.py}`, dati
`…/scratchpad/{report_round2.json, report_round2b.json, report_round2c.json}`, fogli candidati
`…/scratchpad/v3/{meter,workbench,forum,academy}.css` — quelli che il §4 riporta per intero e il §7 pesa.
Dati: impresa «Cantiere Adriatico S.r.l.», 4 besoins, 7 cours, 0 iscrizioni.

---

## 0. RICHIESTE DI DEROGA (numerate, in testa, come prescritto)

**DEROGA 1 — `MOTION_SYSTEM.md` §2, famiglia FOCUS: «anello 2 px + alone 3 px al 30 %».**
Chiedo che quella riga sia corretta in **«alone 5 px al 30 %»**.
*Clausola in conflitto:* `DESIGN_SYSTEM_V2.md` §2, livello 4, dice testualmente «anello 2 px `--accent-ring`
+ **alone 5 px** al 30 %». I due documenti vincolanti si contraddicono, e il prodotto non può avere due firme
di focus. *Motivo:* il 5 px è già implementato da due spec sorelle approvate — `platform-shell.md` §9
(`box-shadow: 0 0 0 5px color-mix(in srgb, var(--accent-ring) 30%, transparent)`) e `buttons.md` §4
(`0 0 0 5px var(--btn-halo)`) — mentre il 3 px compare in `case-file.md` §9. Correggere il documento che ha
**una** occorrenza costa meno che correggere i due che hanno l'implementazione.
*Costo dichiarato:* una riga in `MOTION_SYSTEM.md` §2. *Se negata:* una riga in `platform-shell.md` e una in
`buttons.md`. **In entrambi i casi questa superficie non cambia di un pixel**: i miei quattro fogli
contengono **zero** dichiarazioni di focus (verificabile: `grep -c "focus-visible" v3/{meter,workbench,forum,academy}.css`
→ 0). Il round 1 scriveva «alone 5 px» come se fosse una scelta mia: non lo era e non lo è.

**DEROGA 2 — `docs/design-v3/specs/imagery.md` §4.3, tabella dei quattro slot.**
Chiedo **due voci nominate** in quella tabella: `.plate--chapter` ammessa su `academy/catalogue.html`
(una, in testa) e un quinto slot `.plate--course` (rapporto **4:5**, grado `-lume`) su
`academy/course_detail.html` (una).
*Motivo:* il committente ha respinto il lavoro per «non abbastanza immagini eleganti moderne coerenti», e
l'Academy è la superficie che oggi ne ha **zero** (misurato questo round: `main img` = **0** su catalogo e su
«Mes formations»). `DESIGN_SYSTEM_V2.md` §6 ammette già la fotografia su RICH e §7 classifica l'Academy RICH;
il regime per modo di `imagery.md` ammette **≤ 1 lastra** in `rich`, e **entrambe le pagine ne prendono una
sola**. Non chiedo quindi nulla al sistema vincolante: chiedo che la spec sorella **nomini** due rotte che il
suo stesso regime già consente.
*Costo dichiarato:* due righe nella tabella `imagery.md` §4.3, un valore in più per `variant`, e sette
fotografie curate che devono passare `docs/IMAGE_LICENSES.md` §1 (licenza, crop, strip dei metadati,
`forbidden_subject_check`) **prima** della pubblicazione.
*Se negata:* `course_detail` e `catalogue` restano senza fotografia, il frontespizio disegnato del §4.C.3
diventa lo stato definitivo invece del ripiego, e **questa superficie non risponde alla critica del
committente**. Lo dico qui perché sia una decisione sua e non un'omissione mia.

**DEROGA 3 — `DESIGN_SYSTEM_V2.md` §9.3: «Multi-attore: due trame affiancate».**
Chiedo che, **sul solo filo di rilegatura da 3 px del registro dei besoins e della griglia intervenienti**
(non sulla barra di lavorazione da 10 px, dove §9.3 resta intatto), un besoin con più intervenienti porti
**una sola trama** — quella dell'**acteur autorisé** se ne esiste uno, altrimenti la prima per ordine di
cascata — e che **tutti** gli intervenienti restino nominati in parole nella riga.
*Motivo, misurato:* due trame affiancate dentro 3 px danno 1,5 px per trama, cioè esattamente il tratto
minimo che il §8 rischio 7 impone; a passo 4 px una trama di 1,5 px dentro 1,5 px non ha nemmeno un periodo
completo e collassa in una tinta piatta. Inoltre il diritto lo impone: `REQUIRES_AUTHORISED_ACTOR`
(`apps/companies/models.py:376`) dice che `IN_PROGRESS` esiste **solo** con un acteur autorisé vivo — quando
c'è, è lui il responsabile, e il filo deve dirlo senza ambiguità.
*Costo dichiarato:* su un besoin a due intervenienti il filo nomina uno solo; la riga nomina entrambi, e il
glifo accanto al nome porta il colore del proprio ruolo (`--owner-ink` locale). *Se negata:* il filo passa a
6 px per ospitarne due da 3 px, il registro perde 3 px di colonna di lettura e il foglio comincia a leggere
come una scheda colorata — che è il difetto §1.2.

**Nessun'altra deroga è richiesta.** In particolare **non** chiedo più — e ho rimosso — tutto ciò che nel
round 1 avrebbe richiesto una deroga senza dichiararla: `--accent` in pieno su `--mid-2` (2,52:1),
`--hairline-dark-strong` come confine di controllo (2,19:1), `--ink-2` come tacca su `--mid-1` (2,44:1),
`--shadow-2` a riposo sulla riga di ripresa, `data-mode` su un partial, il tracciato da 600 ms senza token,
i 44 px di bersaglio contro i 48 del §10, `backdrop-filter` sulla navigazione locale.

### 0-bis. CAMBIAMENTI DI CODICE POSSEDUTI (non sono deroghe: sono lavoro dichiarato)

Il round 1 apriva con «**Nessuna vista Django, nessun servizio, nessun modello, nessun contratto dati
toccato**» e poi ne chiedeva uno. La frase è cancellata. Questo è l'elenco completo e onesto.

| # | Che cosa | Dove | Costo | Obbligatorio? |
|---|---|---|---|---|
| C1 | `{% block page_mode %}` su `<body>` | `templates/base.html` | **già di `backgrounds.md`** (§6.1 di quella spec, riga `base.html:45`). Qui dichiaro solo i **valori** dei miei dieci template (§4.A.0) | sì, ma non è mio |
| C2 | `pages.services.photo_for_domain(slug)` + `{% plate %}` che accetta `variant="course"` | `apps/pages/services.py`, `templatetags/plate_tags.py` | ~20 righe: una mappa fissa di sette `course_type` → sette `MediaAsset` curati. Nessun modello, nessuna migrazione, nessun campo nuovo su `Course` | sì, **se** la DEROGA 2 è accolta |
| C3 | `next_module` per riga su «Mes formations» | `apps/academy/views.py:mine` | una `services.next_module(row)` per iscrizione in corso. **Non lo chiedo**: il §4.C.1 è riscritto su ciò che il contesto ha davvero | **no — rinviato a fase 2** |
| C4 | `scripts/territory.py` emette due nuovi gruppi | `scripts/territory.py` | `cartouche` (280×160) e `relation` (1200×520). Il generatore esiste già e la sua convenzione è quella giusta (§4.D) | sì |

**Nient'altro.** Nessuna vista, nessun servizio, nessun modello, nessun contratto dati oltre a C2 e C4; e
C2 è opzionale per costruzione, perché il frontespizio disegnato è il ripiego funzionante.

---

## 0-ter. RISPOSTA PUNTO PER PUNTO ALLA REVISIONE

### I quindici MUST-FIX

| # | Esito | Dove |
|---|---|---|
| 1 · contraddizione `--at` / `data-at` | **FATTO — e l'oggetto è stato ripensato, non rattoppato.** Il misuratore ha ora **due modi dichiarati**: `data-meter="count"` (cumulativo, 1..8, scritti tutti) e `data-meter="record"` (**non** cumulativo, una regola per tappa su `[data-passed~="…"]`). Nessun `--at:` in nessun foglio. Provato in pagina: le cinque tacche computano `border-style` `solid/solid/solid/**dashed**/solid` e `content` `""/""/""/**none**/""` sul besoin chiuso senza prise en charge | §4.0, §4.A.3 |
| 2 · tre decisioni cromatiche sotto 3:1 | **FATTO, con i numeri ricalcolati** — e **una metà è contestata**. CTA primaria su `--mid-2`: `--accent-dark` **9,09:1** con etichetta `--mid-1` **10,01:1**. Tacca piena su mezzanotte: `--terr-line` **6,07:1** su `--mid-1`, **5,51:1** su `--mid-2`; tacca vuota `--on-dark-3` **6,44 / 5,85**. Secondari: **non** `--on-dark-3` e **non** un pieno `--mid-4` (vedi §0-quater, contestazione 1) | §4.B.4, §6 |
| 3 · la barra non deve affermare una pipeline che non esiste | **FATTO — è la correzione più importante di questo round.** La barra e il misuratore si riempiono **solo** dalle transizioni che `NeedEvent` ha davvero registrato, lette in CSS da `data-passed`. Un besoin `UNDER_REVIEW → CLOSED` mostra un **buco** su «Pris en charge». `on_hold` e `withdrawn` sono **condizioni**, non tappe, e tengono la posizione | §4.A.3, §4.A.4 |
| 4 · `data-mode` fuori dal partial | **FATTO.** `data-mode` non esiste più in nessun partial. Il capitolo mezzanotte non è più `company_header.html`: è un partial **nuovo e separato**, incluso **solo** dai due template che passano `as_heading=True`. `need_detail` è **RICH** come dice §7. I due form non ricevono nessuna banda scura | §4.A.0, §4.A.1 |
| 5 · §4.C.1 sul contesto che `mine` ha davvero | **FATTO — riscritto sulle annotazioni reali** `row.modules_total` / `row.modules_attended` (`apps/academy/services.py:126-127`). Nessun `progress.*`, nessun `next_module` nella riga di ripresa. Il prossimo modulo per nome resta dov'è il dato: `enrolment_detail` | §4.C.1, §4.C.2 |
| 6 · `mandated_plans` | **FATTO.** Cinque registri, non tre. Il quinto ha una regola dura scritta, un test, e la frase integrale | §4.C.1 |
| 7 · la trama del responsabile | **FATTO.** Cinque dichiarazioni `repeating-linear-gradient` / `radial-gradient` scritte, mappa `[data-owner~="…"]` completa sui **quattro** valori di `ActorRole` **più** il caso vuoto, contrasti calcolati (4,57 il peggiore) | §4.0 |
| 8 · `aria-hidden` e la parola | **FATTO.** `aria-hidden="true"` sta **solo** su `.meter__track`. La frase del §6 è riscritta. Il `label` non esiste più come parametro: la parola è prodotta dalla catena `{% if %}` del partial, ed è **una sola sorgente** | §4.0, §6 |
| 9 · ordine di caricamento e regole da cancellare | **FATTO, e la revisione aveva ragione al punto che l'ho misurato.** Con il foglio candidato caricato **dopo**, `.forum-cta .btn--secondary` computa **ancora** `border-color: rgb(183,195,196)`, perché `apps/forum/static/forum/forum.css:144` scrive la scorciatoia `border:` a specificità (0,2,0). Le custom property **non possono** batterla. Elenco nominale delle regole da cancellare, con i byte | §4.E |
| 10 · 48 px, `--motion-draw`, alone di focus | **FATTO** per i primi due (48 px su ogni controllo con cornice, 44 su `.btn--icon`, come `buttons.md`; il tracciato usa `--motion-draw` **900 ms**). **CONTESTATO** il terzo, con le citazioni (§0-quater, contestazione 2) e comunque **rimosso**: non dichiaro più nessun focus | §6(f), §5, §0 DEROGA 1 |
| 11 · l'immagine dell'Academy | **FATTO.** Il «frontespizio generato» **non è più il disegno**: è il ripiego. Direzione fotografica scritta per sette domini, con i soggetti vietati, il formato, il peso, l'`alt`, e il cancello di pubblicazione | §4.C.3, §0 DEROGA 2 |
| 12 · guardia CSP su `scripts/territory.py` | **FATTO.** Contratto d'uscita completo + la regola «solo attributi di presentazione e classi» + il test che la asserisce. Il generatore attuale la rispetta già: verificato, `style` non compare nel file | §4.D, §9 |
| 13 · le due didascalie giuridiche | **FATTO.** Entrambe integrali, verbatim, e con il posto dove stanno | §4.C.1 |
| 14 · l'avviso G5 | **FATTO**, con il percorso verificato: `apps/forum/services.py:91-98` `public_speakers()` applica `SpeakerRole.public_name(site_flag)` (`apps/forum/models.py:248-252`) | §4.B.4 |
| 15 · la retorica del §1.2 | **FATTO.** «Quattro etichette identiche» è cancellato: le parole differiscono e il §1.2 lo dice ora per primo. E dichiaro che la metà «pastiglia» non la ripara niente qui, perché `STATE_MODIFIERS` sta in `models.py` e la pastiglia è di `badges.md` | §1.2 |

### Le dieci violazioni

| # | Esito |
|---|---|
| 1 `--accent` su `--mid-2` = 2,52 | **RIMOSSA.** `--accent-dark`, 9,09:1 (ricalcolato) |
| 2 bordo secondario 2,20 | **RIMOSSA** — e la revisione ha ragione sul numero, torto sul rimedio: vedi contestazione 1 |
| 3 tacca `--ink-2` su `--mid-1` = 2,44 | **RIMOSSA.** Variante mezzanotte dichiarata e scritta in `meter.css`, con i suoi rapporti |
| 4 stato conosciuto solo dalla forma | **RIMOSSA.** `aria-hidden` solo sulla pista |
| 5 `next_module` non è in contesto | **RIMOSSA** ri-scrivendo la funzione; e ciò che resterebbe è dichiarato in §0-bis C3 come rinviato |
| 6 «600 ms» senza token | **RIMOSSA.** `--motion-draw` 900 ms, il token che esiste |
| 7 alone 5 px | **RIMOSSA** cancellando ogni dichiarazione di focus da questa spec; il conflitto fra i due documenti vincolanti è la DEROGA 1 |
| 8 `--shadow-2` a riposo | **RIMOSSA.** Misurato sul candidato: `box-shadow` distinti a riposo su registro e insegna = **[]** (nessuno) |
| 9 `data-mode` su un partial | **RIMOSSA.** Partial separato, incluso da due template, `data-mode` sul `<body>` |
| 10 bersagli a 44 px | **RIMOSSA.** 48 px, come §10 e `buttons.md` |

### Le quattordici lacune

| # | Chiusa dove | Come |
|---|---|---|
| 1 il blocco `--at`/`data-at` | §4.0 | forma ad attributo, due modi, CSS scritto per intero |
| 2 off-by-one | §4.0, §4.A.3 | in modo `record` non esiste un `at`: la parola dice «Étape N sur 5» con N prodotto dalla catena `{% if %}`; un besoin `closed` è «Étape 5 sur 5» |
| 3 sei, sette, otto moduli | §4.0 | `data-at` scritto da 1 a 8; oltre 8 la pista sparisce e resta la cifra. `positions` è consumato dal `{% for %}` del template, **mai** da un selettore — detto esplicitamente |
| 4 la trama non aveva CSS | §4.0 | cinque dichiarazioni, passo 4 px, tratto 1,5 px, misura, `forced-colors` |
| 5 la tassonomia non combaciava coi dati | §4.0 | quattro valori di `ActorRole` + il caso vuoto; `professional` ha la trama piena, «aucun intervenant désigné» **non ha filo affatto** |
| 6 `ON_HOLD` / `WITHDRAWN` | §4.A.3, §4.A.4 | condizioni, non tappe; la posizione resta registrata; `aria-current="step"` va sulla tappa **tenuta**, calcolata da `need.events.last.from_status` |
| 7 ordine di caricamento | §4.E | `@import` per il pezzo condiviso, `<link>` in `extra_head` **dopo** il foglio d'app per i tre di superficie, e l'elenco delle regole cancellate |
| 8 dove si caricano i bundle JS | §4.E | `{% block extra_scripts %}` (`templates/base.html:70`), un blocco per base d'app, nominati |
| 9 contratto di `territory.py` | §4.D | `viewBox`, nomi di file, classi, `stroke-width`, dove atterrano, come si committano, e la regola CSP |
| 10 `as_heading` | §4.A.1 | risolta per costruzione: l'insegna scura esiste **solo** dove `as_heading=True`, quindi porta sempre l'`<h1>`; gli altri cinque template tengono la banda chiara con il `<p>` |
| 11 il cruscotto senza impresa | §4.A.2 | ridisegnato, con il testo bloccato verbatim: è la prima schermata di ogni conto nuovo |
| 12 l'aggregazione fra besoins | §4.A.2 | **eliminata**: la nota a margine è **per besoin**, non aggregata. Nessun `min()`, nessuna deduplicazione, nessun `dictsort` |
| 13 `live_assignments` vs `responsible` | §4.A.4 | una riga dura: `live_assignments` serve **solo** a calcolare `data-owner`; il blocco «Responsable» non si tocca, e «Autorisation … valable jusqu'au …» resta dov'è |
| 14 i pesi erano stime | §7 | pesati davvero, `gzip -9`, byte per byte, e le cancellazioni contate per regola |

### Gli otto segnali di «cheap»

| # | Esito |
|---|---|
| 1 nessuna immagine sull'Academy | **RIMOSSO.** Fotografia art-directed per sette domini; il glifo resta come ripiego e il cancello di pubblicazione lo verifica (§9) |
| 2 «batteria» a cinque rettangoli | **RIMOSSO.** L'oggetto non è più un binario segmentato: è una **riga graduata** — filetto, graduazioni, nodi quadri — disegnata nella grammatica cartografica del sistema (§1.1 «tacche», §9.1 «misuratore a cinque tacche»). E in modo `record` **non può** essere un avanzamento cumulativo: si è verificato in pagina che una tappa saltata resta vuota fra due piene |
| 3 hachures Excel-97 | **RIDOTTO A UN FILO.** La trama vive **solo** su 3 px di rilegatura e su 10 px di barra. Nessuna superficie più larga la porta. Il motivo per cui un direttore artistico lo accetta: è il **filo di rilegatura** di un registro, non un riempimento |
| 4 nav appiccicosa con `backdrop-filter` | **RIMOSSO.** `backdrop-filter` è vietato dal §2 livello 6 fuori dall'header scrollato. La nav è **opaca** `--min-1`. Misurato sul candidato: `backdrop-filter: none`, e a riposo nessun repaint per frame |
| 5 «bento» | **RIMOSSA LA PAROLA E LA COSA.** Non due colonne di schede: **un registro e un margine** — colonna di lettura 8/12 e margine 4/12 con un solo filetto, ordinali in mono nel margine, note marginali. È la grammatica editoriale del prodotto, non un cruscotto SaaS |
| 6 tre strisce da 96 px | **RIMOSSO.** Regola nuova: **una sola striscia vuota per pagina**; se due o più regioni sono vuote, collassano in un unico stato vuoto di pagina |
| 7 raggio 2 px + ombra + filetto = card shadcn | **RIMOSSO.** Raggio **0** (§2: «Raggi: 0 sui capitoli e sui fogli»), **nessuna ombra a riposo** (misurato: `[]`), `--shadow-2` solo in hover. Il foglio è definito da cambio di fondo + filetto + il filo di rilegatura |
| 8 striscia di loghi che di solito è vuota | **RIMOSSO.** La regione partner **non si disegna** quando `public_partners()` è vuota — stessa regola dura del §8 rischio 3. Mai un segnaposto, mai un carosello, mai la scala di grigi |

### 0-quater. CONTESTAZIONI (due, con la misura che le sostiene)

**CONTESTAZIONE 1 — il rimedio proposto per il confine dei bottoni secondari è sbagliato, e il difetto
misurato è diverso da quello descritto.**
La revisione scrive: «The secondary buttons need a boundary at ≥3:1 — `--on-dark-3` #8fa0a3 **or a solid
`--mid-4` fill**». Misurato questo round:

* `--mid-4` #223A46 **su** `--mid-2` #14242E = **1,33:1**. Un pieno `--mid-4` su quella fascia è
  *meno* visibile del bordo che sostituisce: sarebbe la stessa violazione di 1.4.11, peggiorata.
* E il difetto attribuito alla build non c'è più: la fascia CTA **oggi** non usa `--hairline-dark-strong`.
  Misurato in pagina su `:8771` e `:8770`, `.forum-cta .btn--secondary` computa
  `border-color: rgb(183,195,196)` = `--on-dark-2` = **8,79:1 su `--mid-2`**. Il 2,19:1 era **mio**, scritto
  nel round 1, e sarebbe stata una **regressione** rispetto a ciò che il prodotto già fa.

**Esito:** prendo `--on-dark-2` (**8,79:1**), non `--on-dark-3` (5,85) e non un pieno `--mid-4` (1,33). Il
bordo resta 1 px. Il numero che la revisione dà per `--hairline-dark-strong` è invece **esatto**: ricomposto
qui, `rgba(214,226,228,.28)` su `--mid-2` dà **#4A5961 = 2,19:1** (su `--mid-1` dà #465359 = **2,20:1** — è
il fondo che la revisione ha usato).

**CONTESTAZIONE 2 — l'alone di focus a 5 px non è «una ridefinizione silenziosa della firma del sistema»:
è la firma del sistema.**
`DESIGN_SYSTEM_V2.md` §2, riga «4 focus»: «anello 2 px `--accent-ring` + **alone 5 px** al 30 %».
`platform-shell.md` §9 e `buttons.md` §4 lo implementano a 5 px. `MOTION_SYSTEM.md` §2 dice 3 px ed è
l'unico. I due documenti vincolanti si contraddicono e nessuna spec di superficie può risolverlo da sola: è
la **DEROGA 1**. **La parte della revisione che è giusta l'ho comunque applicata**: una spec di superficie non
deve dichiarare il focus, e questa non lo dichiara più — `grep -c "focus-visible"` sui miei quattro fogli
restituisce **0**.

---

## 1. VERDETTO SULLO STATO ATTUALE (ri-misurato questo round)

Queste tre superfici non hanno ricevuto il design V2. Non «parzialmente»: **per niente**. I token V2 sono
caricati (via `@import` in `static/css/main.css`, righe 18-23) e non vengono consumati.

**1.1 — L'accento del sistema non esiste su queste pagine; al suo posto c'è il tricolore ufficiale.**
`grep var(--accent)` su `companies.css`, `academy.css`, `forum.css`, `portal.css` → **0 occorrenze**
(l'unica stringa `--accent` in `forum.css` è il nome di classe `.forum-section--accent`, riga 104). Al suo
posto **`rgb(15, 37, 71)` = `--brand-navy` #0F2547**, ri-misurato questo round sul fondo dell'hero del Forum
**e sul fondo della fascia CTA** (`.forum-cta` → `backgroundColor: rgb(15, 37, 71)`). Sorgente dichiarata:
`static/css/v2/bridge.css:31`, `--navy: var(--brand-navy)`. `DESIGN_SYSTEM_V2.md` §1.3 regola 4: «Il
tricolore vive solo nel marchio». Il ponte doveva essere provvisorio; qui è lo stato definitivo.

**1.2 — Quattro stati del besoin sono lo stesso pixel — ma non la stessa parola.**
`static/css/tokens.css:61` `--state-done-fg: #1e4a85` e `:64` `--state-info-fg: #1e4a85` — **lo stesso
esadecimale**; `STATE_MODIFIERS` (`apps/companies/models.py:394-402`) manda `SUBMITTED` e `IN_PROGRESS`
entrambi su `filed`. Misurato sul cruscotto: `Vérifiée`, `Transmis au projet`, `En cours d'examen`,
`Pris en charge` rendono **tutte e quattro `rgb(30, 74, 133)`**, `background-color: rgba(0,0,0,0)`,
`border-radius: 0px`, altezza **16 px**, unico segno `border-inline-start: 2px solid currentcolor`.
**Le parole, invece, differiscono**, e il round 1 scriveva «quattro etichette identiche», che è falso: sono
quattro parole diverse in un unico trattamento. Il difetto è che **nient'altro** le distingue — non il
colore, non la forma, non la posizione, non un glifo. Due precisazioni dovute:
(a) `#1E4A85` non appartiene alla tavolozza V2 ed è un blu che ha l'aspetto di un link, cioè un secondo
accento interattivo (§1.3.1); (b) **la metà «pastiglia» di questo difetto non la ripara niente di ciò che
segue**: `STATE_MODIFIERS` vive in `models.py`, che questa spec non tocca, e la pastiglia appartiene a
`badges.md`, che ha già deciso (§4.1) che l'identità cromatica è **deliberata e resta**, e che a distinguere
saranno glifo, corpo, filetto e registro. Qui aggiungo il **quinto** canale che manca al registro: la
posizione sulla riga graduata (§4.A.3).

**1.3 — Il cruscotto impresa È il cruscotto della persona con parole diverse.**
Ri-misurato: `scrollHeight` **1 895 px**, container **1 320 px**, righe di registro **976 × 90**, `section`
con un fondo distinto: **due** (`rgba(0,0,0,0)` e `rgb(236,235,230)`), `box-shadow` distinti sull'intero
documento: **zero**, `data-mode`: **`null`**. La struttura, i `folio`, gli ordinali serif, la `register`, il
rail locale sono **gli stessi oggetti** del cruscotto persona. Di ciò che la direttiva chiede — contesto
territoriale, competenze richieste, avanzamento, fabbisogni di formazione, attori, calendario — **niente
compare**, benché `need.territory`, `need.skills`, `need.training_needs`, `need.safety_training_required`,
`need.start_from`, `need.headcount`, `need.assignments`, `need.events` esistano già.

**1.4 — La banda impresa costa 348 px di telefono per quattro coppie etichetta/valore.**
Ri-misurato: `.company-header` = 1440×**160** a desktop e 390×**348** a 390×844, cioè il **41,2 %** del primo
viewport, prima di qualunque cosa da fare. `background: rgb(236,235,230)`, nessuna ombra, nessun filetto
colorato, nessun grafico.

**1.5 — Il Forum pubblico è un rettangolo blu, un elenco e un altro rettangolo blu.**
Ri-misurato su `:8771`: `scrollHeight` **4 364 px**; `.forum-hero` alto **388,16 px** su 900 (**43,1 %**),
fondo `rgb(15,37,71)` piatto, `h1` **52 px**, `<img>` in pagina = **2**, `box-shadow` distinti = **1**. Il
programma è un `<ol>` di **otto** voci in cui **sette non hanno orario** (`time_label` vuoto ⇒ resta
l'ordinale) — riverificato questo round, 8 righe / 7 senza orario. A 390 l'hero misura **429,66 px** =
**50,9 %** del viewport e l'`h1` scende a **30,4 px**, sotto `--t-band` (32), cioè fuori scala.
**Correzione a me stesso:** il round 1 scriveva 401,7 px = 47,6 %. Non è più vero: oggi sono **429,66 px =
50,9 %**. Non ripeto una cifra che non ho ri-eseguito.

**1.6 — Diciassette corpi tipografici sul Forum, contro gli undici che il sistema ammette.**
Ri-misurati in pagina, ordinati: 52 · **27,2** · 22 · **21,6** · 20 · **17,6** · 17 · 16 · **15,2** · 15 ·
14 · **13,5** · 13 · **12,8** · **12,48** · 12 · **11** px. Sono **diciassette**, non diciotto: il **14,4 px**
che il round 1 elencava non c'è più. Otto non esistono in `DESIGN_SYSTEM_V2.md` §3.2 e sono il risultato di
`em` che si compongono a cascata. Il titolo di sezione del Forum è **27,2 px**, un corpo che nessuno ha scelto.

**1.7 — L'Academy non è un prodotto di apprendimento: è tre paragrafi.**
Ri-misurato: «Mes formations» `scrollHeight` **1 483 px** per tre sezioni **tutte vuote** (tre `.empty`), con
paragrafi larghi **418,5 px** su un container di **1 240**. Fondi di sezione sull'intera Academy:
`['rgba(0, 0, 0, 0)']`, cioè **zero**. Il catalogo: `scrollHeight` **2 366 px**, **sette** righe alte
**161–162 px** di solo testo. **`main img` = 0** su entrambe: l'Academy **non ha nessuna immagine**. Sulla
scheda del cours i moduli sono `.sequence__step`, lo stesso oggetto che il fascicolo giuridico usa per le
tappe di una procedura.

**1.8 — Moto: nessuno.** Il censimento di `getComputedStyle` dà come sola transizione ricorrente
`color, text-decoration-color | 0,18 s | cubic-bezier(.4,0,.2,1)` — i link. Le uniche `animation-name` ≠
`none` sono `menu-in` / `menu-in-end` del drawer condiviso. Ri-verificato questo round:
`document.getAnimations().length` = **0** sul Forum, sia a moto normale sia con `prefers-reduced-motion:
reduce`. In più la curva usata in entrata è `--ease-standard` mentre `MOTION_SYSTEM.md` §1 prescrive
`--ease-out` per ciò che entra.

**1.9 — Tre altezze di bottone per lo stesso prodotto — e la stessa pagina ne dà due secondo il server.**
Questo è il difetto ri-misurato con più precisione di tutti. Sul **Forum**, `.forum-cta`:

| Porta | Bottoni resi | Altezze |
|---|---|---|
| `:8770` (fase 3 chiusa) | `btn btn--primary btn--lg` + due `btn btn--secondary` | **52 · 52 · 52** |
| `:8771` (fase 3 aperta) | **nessun primario** + due `btn btn--secondary` | **44 · 44** |

A 390 su `:8771` il primo secondario va a **54 px** (l'etichetta va a capo) e il secondo resta a 44: la pila
di CTA è dentellata. Altrove: **36 px** (`btn--sm` su `needs.html` e `need_detail.html`).
`DESIGN_SYSTEM_V2.md` §10 ne prescrive **una, 48**, e `buttons.md` la fissa in `--btn-h`.
**Correzione a me stesso:** il round 1 scriveva che i due secondari della fascia CTA sono «testo su fondo blu
senza fondo proprio». Hanno un bordo, ed è `--on-dark-2` a **8,79:1**. Il difetto è la gerarchia (due
secondari e nessun primario su `:8771`), non il contrasto.

**Nota RTL/contenuto (HUMAN_QA_REQUIRED).** Su `/ar/forum/` la pagina passa in `dir="rtl"`, le famiglie
compagne si attivano e non c'è scorrimento orizzontale (ri-verificato: `scrollWidth === clientWidth`); ma i
bottoni della fascia CTA restano **in francese**, perché sono testi bloccati d'evento non tradotti. È un
difetto di contenuto, non di CSS.

---

## 2. UI-UX-PRO-MAX

Sette interrogazioni. Lo strumento è tarato su «government = accessible & ethical, avoid motion effects» e su
palette Tailwind con font serviti da una CDN di caratteri: è insieme il registro che il committente ha
respinto e una violazione della nostra CSP — i due host di quella CDN sono anche nel registro delle stringhe
vietate di `apps/cms/forbidden.py`, quindi non li trascrivo qui. Dove sbaglia lo dico.

| # | Query (dominio) | Restituito (condensato) | Esito |
|---|---|---|---|
| 1 | `B2B company dashboard for skills demand and hiring needs pipeline` (product) | «B2B Service» → *Accessible & Ethical + Minimalism & Swiss*, secondari *Bento Box Grid, Micro-interactions*, cruscotto «Sales Intelligence», «Professional blue + neutral grey» | **RESPINTO il nucleo**: «Sales Intelligence» presuppone un imbuto di vendita e un conteggio di candidati; questo prodotto **non presenta alcuna persona a un'impresa**. «Professional blue + neutral grey» è il grigio-blu del §1.2. **RESPINTO anche *Bento Box Grid***, che nel round 1 avevo accettato e che ha prodotto due colonne 60/40: vedi §4.A.2. **ACCETTATE** le *Micro-interactions* come autorizzazione esplicita al moto in un contesto B2B |
| 2 | `e-learning course progress dashboard modules completion resume learning` (product) | «LMS» → *Flat + Accessible*, «Calm blue + course category colors + grade green + alert red»; «Online Course» → *Claymorphism + Vibrant* | **RESPINTO Claymorphism/Vibrant** (registro da gioco: qui l'attestato dichiara «non vale ni titre ni autorisation»). **RESPINTE le «course category colors»**: sette colori di dominio contro la regola dell'accento unico. **ACCETTATA** una sola idea: il cruscotto d'apprendimento è il **soggetto** della pagina, non un elenco di iscrizioni (§4.C.1) |
| 3 | `conference event landing page agenda speakers timeline` (ux) | Performance › Image Optimization: «srcset, WebP, mai un'immagine 4000 px per 400 px». Navigation › Active State: «evidenziare la voce corrente» | **ACCETTATI entrambi**, e sono i due difetti del Forum: 2 immagini in 4 364 px e una `.forum-localnav` che non marca mai la sezione corrente. Diventano §4.B.1 e §4.B.3 |
| 4 | `scroll linked timeline animation reveal agenda government institutional` (gsap) | *Subtle* `opacity 0, y 12, 350 ms, power1.out`; *Standard* `y 24, stagger .08`; *Complex* `scrub + pin`. Note: «non più di ~8 figli in stagger», «pin forza reflow» | **ACCETTATI i parametri** (`y:12` → `translateY 12→0`; ~350 ms → `--motion-base` 240 + stagger 40-60; il tetto di 8 figli diventa la regola del programma: oltre otto voci l'agenda rivela per **gruppi**). **RESPINTO l'attrezzo**: GSAP non entra, la libreria è Motion 13.4.1 e la CSP è `script-src 'self'`. **RESPINTO il pin** |
| 5 | `progress indicator without percentage attendance record learning` (ux) | Feedback › Progress Indicators: «step indicator», es. «Step 2 of 4». Interaction › Focus States, severità Alta | **ACCETTATO «Step 2 of 4»** con una distinzione che il round 1 non faceva: uno *step indicator* è vero per un **conteggio** e falso per una **macchina a stati non lineare**. Di qui i due modi del §4.0. **RESPINTA la barra continua** |
| 6 | `status badge colour differentiation semantic states table` (color) | Tre palette con `Accent #22C55E`, `#D97706`, bordi `#A7F3D0` | **RESPINTO in blocco**: palette Tailwind generiche; adottarle introdurrebbe da tre a cinque accenti. La differenziazione qui **non passa dal colore** ma dalla forma e dalla posizione, e la pastiglia è di `badges.md` |
| 7 | `government institutional platform dense data workspace` (`--design-system`) | «Enterprise Gateway» (path selection, *Client Logos*, *Contact Sales*), «Data-Dense Dashboard», `#1E40AF` + `#D97706`, Fira Code/Fira Sans **via Google Fonts CDN**, «hover tooltips, chart zoom, spinner» | **RESPINTO quasi per intero**: *Client Logos* è impossibile (gate G6); *Contact Sales* è una falsità giuridica su questo prodotto; la CDN di caratteri viola la CSP **ed è una stringa vietata**; `#1E40AF` reintrodurrebbe il blu abusivo del §1.2. **ACCETTATE due righe**: la densità (le righe del registro scendono da 90 a **74 px**, misurato) e «no spinner da solo» → skeleton di livello 1 con `aria-busy`. Che la famiglia raccomandata sia **Fira Sans**, già licenziata e self-hosted, è la sola conferma utile |

---

## 3. 21ST.DEV

Sette candidati, tre famiglie di problema. Due studiati nel codice con `get_component`; **nessuno
installato** — se ne estrae la struttura e la si riscrive in Django e nei nostri token. `generate` e
`iterate_generation` non chiamati.

| # | Componente · URL | Cosa è buono per noi | Cosa è sbagliato per noi | Esito |
|---|---|---|---|---|
| 1 | **Deployment Pipeline** (@rmahammad, 29359) — *codice letto* | Stato **sempre glifo + PAROLA**; `useVisibilityPause` (IntersectionObserver); riassunto in `<p role="status" aria-live="polite">`; **container query**; bersagli minimi dichiarati | Alone che pulsa `repeat: Infinity` e glifo che ruota (due loop vietati); `color-mix` per tingere i nodi; `rounded-2xl` + `shadow-md`; React + Tailwind + shadcn. **E soprattutto: il riempimento per segmento presuppone una pipeline lineare** — che il nostro dominio non ha | **ISPIRAZIONE, con un rifiuto nuovo.** Presi: stato = glifo+parola, pausa fuori schermo, `aria-live`, container query. **Rifiutato ora anche il riempimento per segmento cumulativo**: è la causa del difetto che la revisione ha trovato |
| 2 | **World Map** (@manuarora700, 999) — *codice letto* | Proiezione equirettangolare `x = (lng+180)·(W/360)`, `y = (90−lat)·(H/180)`; arco come Bézier quadratica; `pathLength 0→1` | `dotted-map` a runtime; `next/image` con una `data:` URI; `next-themes`; `<animate repeatCount="indefinite">` su ogni nodo; il mappamondo puntinato è il cliché «global connectivity», e su un progetto bilaterale è falso | **ISPIRAZIONE molto parziale.** Prese: proiezione e costruzione dell'arco, **calcolate a build time in `scripts/territory.py`**. Rifiutati: libreria, mappamondo, pulsazioni |
| 3 | **Timeline** (@slide-cn, 28298) | Doppio orientamento con marcatori personalizzabili | Impaginazione alternata sinistra/destra: in RTL va specchiata a mano; nessun concetto di «voce senza orario», che è **7 casi su 8** del nostro programma | **RIFIUTATO come componente, ACCETTATO il principio** del doppio orientamento con un solo markup |
| 4 | **Timeline Rail** (@nayan_radadiya6, 6528) | Binario continuo con tacche | Descrizione e API inesistenti: niente da verificare su accessibilità o reduced-motion | **RIFIUTATO** |
| 5 | **Process Pillars** (@ankitsharma2615, 3192) | Fasi come barre segmentate | Nessuna parola di stato, nessun responsabile, nessun bersaglio. Riempimento **frazionario** = misura non verificabile | **ISPIRAZIONE minima**: la segmentazione sì, il frazionario no |
| 6 | **Onboarding Workspace Setup** (@ephraimduncan, 29449) | **Un'azione per passo** e stato di completamento | Barra percentuale in testa; passi tutti azionabili insieme; card con ombra e raggio grande | **ISPIRAZIONE**: conferma «un controllo alla volta» di `enrolment_detail.html` |
| 7 | **Efferd Dashboard 2** (@efferd, 13985) | Griglia densa a pesi diversi | KPI inventati, grafici di ricavi, feed d'attività: ogni tassello presuppone un dato che qui **non esiste o non deve esistere** | **RIFIUTATO ora anche il ritmo**: nel round 1 ne avevo preso «i pesi», e ne è uscito un 60/40. Al suo posto il registro e il margine (§4.A.2) |

---

## 4. LA PROPOSTA

Quattro fogli. **Uno** è condiviso e va nel bundle principale; **tre** sono di superficie e si caricano nel
blocco d'app, **dopo** il foglio legacy che devono correggere (§4.E — la revisione aveva ragione, e l'ho
misurato).

> `static/css/v3/meter.css` (condiviso) · `static/css/v3/workbench.css` · `static/css/v3/forum.css` ·
> `static/css/v3/academy.css`
> JS: `static/js/src/workbench.js`, `forum.js`, `academy.js` — entry point automatici
> (`scripts/build_frontend.mjs` ha `splitting: true` e raccoglie ogni `.js` di primo livello), che
> condividono il chunk Motion già scaricato da `shell.js` (**70 441 B grezzi / 26 143 B gzip**, verificato).

### 4.0 Il pezzo condiviso — «la riga graduata» (`v3/meter.css`)

**Il round 1 ha sbagliato una cosa sola, e l'ha sbagliata due volte:** ha usato **un** oggetto per **due**
verità diverse, e poi l'ha pilotato con una custom property che non può pilotare un `:nth-child()`.

Le due verità sono:

* **un conteggio** — «3 modules sur 5 suivis», «4 besoins en cours», «2 voci d'agenda trascorse». Qui il
  riempimento **cumulativo dal lato di lettura è vero**.
* **un registro di tappe in una macchina a stati non lineare** — un besoin. Qui il riempimento cumulativo
  **è una falsità**, perché `ALLOWED_TRANSITIONS` (`apps/companies/models.py:359-371`) ammette
  `UNDER_REVIEW → CLOSED` senza passare da `IN_PROGRESS`, ammette `UNDER_REVIEW → SUBMITTED` all'indietro, e
  tiene `ON_HOLD` e `WITHDRAWN` fuori dalla linea.

Quindi: **un oggetto, due modi dichiarati**, entrambi ad attributo, entrambi scritti per intero.

#### Il disegno — perché non è più una batteria

La revisione ha ragione: cinque rettangoli 18×8 con un filetto grigio sono l'indicatore di segnale del 2013.
L'oggetto è ridisegnato nella grammatica che questo sistema possiede già: **la graticola**. `DESIGN_SYSTEM_V2`
§1.1 assegna a `--terr-line` «isoipse, **tacche**, rotta»; §9.1 chiama l'avanzamento del fascicolo
«**misuratore a cinque tacche**»; `scripts/territory.py` disegna le tacche della graticola come croci
(`M x-4 y h8 M x y-4 v8`). La riga graduata è quello:

* **un filetto di riferimento** (`border-block-end` di ogni slot), **solido** dove c'è registrazione,
  **tratteggiato** dove non ce n'è;
* **una graduazione** di 1×7 px al bordo d'inizio di ogni slot — sempre, registrata o no;
* **un nodo** quadro di 7×7 px che poggia sul filetto, **stampato solo dove la registrazione esiste**, e che
  porta la **trama del responsabile**;
* sul nodo corrente, un **anello** 1,5 px `outline-offset: 2px` — il «Vous êtes ici» del §9.3.

Misurato in pagina (candidato servito come `<link>` same-origin): **5 slot = 110 × 16 px** a ≥ 768,
**8 slot = 176 × 16**, e a 390 lo slot passa a 20 px → **100 × 16** e **160 × 16**.
**Il buco è il messaggio**: su un besoin `UNDER_REVIEW → CLOSED` le cinque tacche computano
`border-style` = `solid · solid · solid · **dashed** · solid` e `content` = `"" · "" · "" · **none** · ""`.
Un avanzamento cumulativo non può produrre quel disegno, ed è la prova che questo oggetto non è quello.

#### Il markup

```django
{# templates/components/meter.html
   Contratto — modalità «count»:  mode="count" · positions (int, 1..8) · at (int, 0..positions) · word
                modalità «record»: mode="record" · stages (lista di slug) · passed (stringa separata da
                                   spazi) · now (slug) · condition ("" | "on_hold" | "withdrawn") · word
   `owner` (stringa separata da spazi) in entrambe. `positions` è consumato QUI, dal {% for %},
   e da nessun selettore CSS: il CSS consuma solo `at`, `passed`, `now`, `condition`, `owner`.

   aria-hidden sta su .meter__track e SU NIENT'ALTRO. La parola è contenuto: è l'unica resa
   accessibile dello stato di questo oggetto e non è mai visually-hidden (§8 rischio 1). #}
{% load i18n %}
<span class="meter{% if inline %} meter--inline{% endif %}"
      data-meter="{{ mode }}"
      {% if mode == "count" %}data-at="{{ at }}"{% endif %}
      {% if mode == "record" %}data-passed="{{ passed }}" data-now="{{ now }}"{% endif %}
      {% if condition %}data-condition="{{ condition }}"{% endif %}
      data-owner="{{ owner|default:'' }}">
  {% if mode == "count" and positions > 8 %}{# una pista che sfonda mente: resta la cifra #}
  {% else %}
  <span class="meter__track" aria-hidden="true">
    {% if mode == "record" %}{% for stage in stages %}<span class="meter__tick" data-stage="{{ stage }}"></span>{% endfor %}
    {% else %}{% for _ in ""|ljust:positions %}<span class="meter__tick"></span>{% endfor %}{% endif %}
  </span>
  {% endif %}
  <span class="meter__word">{{ word }}</span>
</span>
```

`""|ljust:positions` produce `positions` spazi e il `{% for %}` li itera: è l'unico modo di contare in un
template Django senza una riga di Python, ed è la ragione per cui `positions` non compare in nessun selettore.

#### Il foglio, per intero

```css
/* static/css/v3/meter.css */
:root {
  --meter-slot: 22px;              /* passo di una graduazione */
  --meter-node: 7px;               /* il quadro che poggia sul filetto */
  --meter-grad: 7px;               /* la graduazione */
  --meter-rule: var(--hairline-strong);  /* 3,37:1 su --min-0 · 3,59:1 su --min-2 · 3,14:1 su --min-1 */
  --meter-ink: var(--ink-2);             /* 6,87:1 su --min-2 · 6,46:1 su --min-0 */
  --meter-now: var(--accent-ring);       /* 3,70:1 su --min-0 · 3,94:1 su --min-2 */
}
/* La variante mezzanotte — la lacuna 3 della revisione. --terr-line è l'uso che il token
   dichiara di sé («tacche»), è grafica e mai interazione, ed è 6,07:1 su --mid-1. */
.chapter--dark {
  --meter-rule: var(--on-dark-3); /* 6,44:1 su --mid-1 · 5,85:1 su --mid-2 */
  --meter-ink: var(--terr-line);  /* 6,07:1 su --mid-1 · 5,51:1 su --mid-2 */
  --meter-now: var(--accent-dark);/* 10,01:1 su --mid-1 · 9,09:1 su --mid-2 */
}

.meter { display: grid; gap: var(--s-1); justify-items: start;
         font-variant-numeric: tabular-nums; }
.meter--inline { grid-auto-flow: column; align-items: center; gap: var(--s-3); }

.meter__track { display: flex; align-items: flex-end; }
.meter__tick { position: relative; inline-size: var(--meter-slot); block-size: 16px;
               border-block-end: 1px dashed var(--meter-rule); }
.meter__tick::before { content: ""; position: absolute; inset-block-end: 0; inset-inline-start: 0;
                       inline-size: 1px; block-size: var(--meter-grad);
                       background: var(--meter-rule); }
.meter__tick::after { content: none; position: absolute; inset-block-end: 1px;
                      inset-inline-start: calc((var(--meter-slot) - var(--meter-node)) / 2);
                      inline-size: var(--meter-node); block-size: var(--meter-node);
                      background-color: var(--owner-ink, var(--meter-ink));
                      background-image: var(--owner-weave, none);
                      background-size: var(--owner-weave-size, auto); }
.meter__word { font-size: var(--t-caption); line-height: var(--t-caption-lh);
               color: var(--ink-3); max-inline-size: 100%; }
.chapter--dark .meter__word { color: var(--on-dark-2); }   /* 8,79:1 su --mid-2 */

/* ---- MODO «COUNT» — cumulativo, da 1 a 8 e non oltre --------------------- */
[data-meter="count"][data-at="1"] .meter__tick:nth-child(-n + 1),
[data-meter="count"][data-at="2"] .meter__tick:nth-child(-n + 2),
[data-meter="count"][data-at="3"] .meter__tick:nth-child(-n + 3),
[data-meter="count"][data-at="4"] .meter__tick:nth-child(-n + 4),
[data-meter="count"][data-at="5"] .meter__tick:nth-child(-n + 5),
[data-meter="count"][data-at="6"] .meter__tick:nth-child(-n + 6),
[data-meter="count"][data-at="7"] .meter__tick:nth-child(-n + 7),
[data-meter="count"][data-at="8"] .meter__tick { border-block-end-style: solid; }
[data-meter="count"][data-at="1"] .meter__tick:nth-child(-n + 1)::after,
[data-meter="count"][data-at="2"] .meter__tick:nth-child(-n + 2)::after,
[data-meter="count"][data-at="3"] .meter__tick:nth-child(-n + 3)::after,
[data-meter="count"][data-at="4"] .meter__tick:nth-child(-n + 4)::after,
[data-meter="count"][data-at="5"] .meter__tick:nth-child(-n + 5)::after,
[data-meter="count"][data-at="6"] .meter__tick:nth-child(-n + 6)::after,
[data-meter="count"][data-at="7"] .meter__tick:nth-child(-n + 7)::after,
[data-meter="count"][data-at="8"] .meter__tick::after { content: ""; }

/* ---- MODO «RECORD» — una regola per tappa, sulla parola che il DATABASE
   ha scritto. data-passed è l'elenco dei NeedEvent.to_status; [~=] ne prende
   una parola. Niente è calcolato in Python, niente è calcolato in JavaScript. */
[data-passed~="draft"] .meter__tick[data-stage="draft"],
[data-passed~="submitted"] .meter__tick[data-stage="submitted"],
[data-passed~="under_review"] .meter__tick[data-stage="under_review"],
[data-passed~="in_progress"] .meter__tick[data-stage="in_progress"],
[data-passed~="closed"] .meter__tick[data-stage="closed"],
[data-now="draft"] .meter__tick[data-stage="draft"],
[data-now="submitted"] .meter__tick[data-stage="submitted"],
[data-now="under_review"] .meter__tick[data-stage="under_review"],
[data-now="in_progress"] .meter__tick[data-stage="in_progress"],
[data-now="closed"] .meter__tick[data-stage="closed"] { border-block-end-style: solid; }
[data-passed~="draft"] .meter__tick[data-stage="draft"]::after,
[data-passed~="submitted"] .meter__tick[data-stage="submitted"]::after,
[data-passed~="under_review"] .meter__tick[data-stage="under_review"]::after,
[data-passed~="in_progress"] .meter__tick[data-stage="in_progress"]::after,
[data-passed~="closed"] .meter__tick[data-stage="closed"]::after,
[data-now="draft"] .meter__tick[data-stage="draft"]::after,
[data-now="submitted"] .meter__tick[data-stage="submitted"]::after,
[data-now="under_review"] .meter__tick[data-stage="under_review"]::after,
[data-now="in_progress"] .meter__tick[data-stage="in_progress"]::after,
[data-now="closed"] .meter__tick[data-stage="closed"]::after { content: ""; }

/* «Vous êtes ici» — un anello, mai un colore da solo: la parola accanto dice
   la stessa cosa e la pastiglia la dice una terza volta. */
[data-now="draft"] .meter__tick[data-stage="draft"]::after,
[data-now="submitted"] .meter__tick[data-stage="submitted"]::after,
[data-now="under_review"] .meter__tick[data-stage="under_review"]::after,
[data-now="in_progress"] .meter__tick[data-stage="in_progress"]::after,
[data-now="closed"] .meter__tick[data-stage="closed"]::after {
  outline: 1.5px solid var(--meter-now); outline-offset: 2px; }

/* ---- LE DUE CONDIZIONI FUORI DALLA LINEA --------------------------------
   ON_HOLD e WITHDRAWN non sono tappe: sono condizioni SUL registro. La
   posizione È TENUTA — tutto ciò che è registrato resta registrato, e solo
   il nodo CORRENTE diventa aperto. (Lacuna 6.) */
[data-condition="on_hold"][data-now="draft"] .meter__tick[data-stage="draft"]::after,
[data-condition="on_hold"][data-now="submitted"] .meter__tick[data-stage="submitted"]::after,
[data-condition="on_hold"][data-now="under_review"] .meter__tick[data-stage="under_review"]::after,
[data-condition="on_hold"][data-now="in_progress"] .meter__tick[data-stage="in_progress"]::after,
[data-condition="on_hold"][data-now="closed"] .meter__tick[data-stage="closed"]::after {
  background-image: none; background-color: transparent;
  border: 1.5px solid var(--meter-ink); box-sizing: border-box; }
[data-condition="withdrawn"] .meter__tick { border-block-end-style: dotted; }
[data-condition="withdrawn"] .meter__tick::after { background-image: none;
  background-color: transparent; border: 1px solid var(--ink-3);
  box-sizing: border-box; outline: 0; }
.chapter--dark [data-condition="withdrawn"] .meter__tick::after { border-color: var(--on-dark-3); }

/* ---- LA TRAMA DEL RESPONSABILE ------------------------------------------
   DESIGN_SYSTEM_V2 §9.3 portato sul B2B. QUATTRO valori di ActorRole
   (apps/companies/models.py:705-710) PIÙ il caso vuoto — l'intero dominio e
   nient'altro. Passo 4 px, tratto 1,5 px (§8 rischio 7). Contrasti calcolati
   su --min-2: 6,05 · 8,05 · 6,76 · 4,57 · 5,88.
   ORDINE DI SORGENTE DELIBERATO: authorised_actor è ULTIMO, quindi su un
   besoin a più intervenienti vince lui. È la DEROGA 3 e ha un motivo di
   diritto: REQUIRES_AUTHORISED_ACTOR (models.py:376). */
[data-owner~="professional"] {                      /* «Professionnel mandaté» = una persona fisica
                                                       → la trama PIENA del §9.3 («pieno = persona») */
  --owner-ink: var(--owner-person); --owner-weave: none; }
[data-owner~="project_team"] {                      /* §9.3: «hachures 45° = équipe» */
  --owner-ink: var(--owner-project);
  --owner-weave: repeating-linear-gradient(45deg, var(--owner-ink) 0 1.5px, transparent 1.5px 4px); }
[data-owner~="training_body"] {                     /* §9.3: «punti = formazione» */
  --owner-ink: var(--owner-training);
  --owner-weave: radial-gradient(circle at 1px 1px, var(--owner-ink) 0 .75px, transparent .9px);
  --owner-weave-size: 4px 4px; }
[data-owner~="authorised_actor"] {                  /* §9.3: «linee = autorità» */
  --owner-ink: var(--owner-authority);
  --owner-weave: repeating-linear-gradient(0deg, var(--owner-ink) 0 1.5px, transparent 1.5px 4px); }
/* «aucun intervenant désigné» — l'assenza si disegna come assenza: nessuna
   trama, nessun filo, un nodo aperto. Non è «tratteggio», che il §9.3
   riserva al territorio e che su questa superficie NON si usa, perché un
   besoin non porta mai un ruolo territoriale. */
[data-owner=""], [data-owner~="none"] { --owner-ink: var(--ink-3); --owner-weave: none; }
[data-owner=""] .meter__tick::after, [data-owner~="none"] .meter__tick::after {
  background-color: transparent; border: 1px solid var(--ink-3); box-sizing: border-box; }

/* ---- MOTO — una voce sola, dichiarata al §5 ------------------------------ */
@media (prefers-reduced-motion: no-preference) {
  .meter__tick::after { transform: scale(1); transform-origin: center;
    transition: transform var(--motion-base) var(--ease-out); }
  .meter[data-enter] .meter__tick::after { transform: scale(0); }
}
@media (forced-colors: active) {
  .meter__tick { border-block-end-color: CanvasText; }
  .meter__tick::before { background: CanvasText; }
  .meter__tick::after { forced-color-adjust: none; }
  [data-condition="on_hold"] .meter__tick::after,
  [data-owner=""] .meter__tick::after { forced-color-adjust: auto; border-color: CanvasText; }
}
@media (max-width: 47.9375rem) { :root { --meter-slot: 20px; } }
```

**La mappa dei ruoli, per esteso** (lacuna 5 — la tassonomia che non combaciava):

| `ActorRole` (`models.py:705`) | Etichetta | Trama | `--owner-ink` | Contrasto su `--min-2` |
|---|---|---|---|---|
| `authorised_actor` | Soggetto autorizzato / acteur autorisé | linee orizzontali 1,5/4 px | `--owner-authority` #8C6D4B | **4,57** |
| `training_body` | Organisme de formation | punti su griglia 4 px | `--owner-training` #1C5F7C | **6,76** |
| `professional` | **Professionnel mandaté** | **pieno** | `--owner-person` #0F6A72 | **6,05** |
| `project_team` | Équipe du projet | hachures 45° 1,5/4 px | `--owner-project` #34506A | **8,05** |
| *(nessuno)* | «aucun intervenant désigné» | **nessuna — e nessun filo** | `--ink-3` #55646B | **5,88** |
| *(non usato qui)* | territorio | tratteggio, riservato al §9.3 | `--owner-territory` | — |

Il colore non porta mai da solo: c'è la trama, il glifo accanto al nome, e il nome.

### 4.A IL CRUSCOTTO IMPRESA — «il banco di lavoro» (`v3/workbench.css`)

#### A.0 Le modalità di pagina, dichiarate una per template

`data-mode` **non sta su nessun partial**. Sta sul `<body>`, con il meccanismo che `backgrounds.md` §6.1 ha
già specificato (`<body class="…" data-mode="{% block page_mode %}standard{% endblock %}">`, `base.html:45`).
Qui dichiaro solo i valori, e li dichiaro contro la tabella §7 del sistema:

| Template | `page_mode` | Perché |
|---|---|---|
| `companies/dashboard.html` | `rich` | §7: «cruscotti» |
| `companies/needs.html` | `rich` | §7: «cruscotti» |
| `companies/need_detail.html` | **`rich`** | §7 elenca «**fabbisogno impresa**» sotto RICH. La revisione ha ragione: il round 1 diceva DENSE e contraddiceva il sistema. **La pagina resta densa nei fatti** — nessun capitolo mezzanotte, nessuna isoipsa, nessuna fotografia, nessun loop — ma dichiara il modo che il sistema le assegna, e non consuma il budget che quel modo le concede |
| `companies/need_form.html` | `dense` | un modulo è back-office di sé stesso; §7 «liste, tabelle, back-office» |
| `companies/profile.html` | `dense` | idem |
| `companies/profile_form.html` | `dense` | idem |
| `forum/index.html` | `immersive` | §7: «FORUM pubblico» |
| `forum/governance/*.html` | `dense` | tavolo di lavoro |
| `academy/catalogue.html`, `mine.html`, `course_detail.html`, `enrolment_detail.html` | `rich` | §7: «Academy» |
| `academy/plan_detail.html` | `dense` | è un elenco |

**Capitoli mezzanotte per pagina** (§1.3 regola 5, §8 rischio 4): cruscotto **1** (l'insegna) · besoins **1**
(l'insegna) · `need_detail`, i due form, `profile` **0** · Forum pubblico **2** (hero + relazione) ·
Academy **0** su tutte e cinque. Il test li conta (§9).

#### A.1 L'insegna d'impresa — un partial NUOVO, non `company_header.html`

La revisione ha ragione su tutta la linea: `company_header.html` è incluso da **sette** template
(`base_companies.html:24`, `dashboard:22`, `needs:6`, `need_detail:14`, `need_form:17`, `profile:6`,
`profile_form:7`), e metterci dentro un capitolo mezzanotte lo stampa anche sui due moduli.

**Soluzione:** l'insegna è un partial **suo**, `templates/companies/partials/company_standard.html`, e lo
includono **solo i due template che passano `as_heading=True`** — cioè `dashboard.html` e `needs.html`, gli
unici due il cui **soggetto** è l'impresa. Gli altri cinque tengono `company_header.html` esattamente com'è
oggi, sul fondo chiaro, con il `<p>`.

Questo chiude anche la lacuna 10 **per costruzione**: l'insegna scura esiste solo dove l'`<h1>` è il nome
dell'impresa, quindi porta **sempre** un `<h1>` e **mai** un secondo; il ramo `{% if as_heading %}` sparisce
dalla versione scura perché non ha più un altro caso.

```django
{# templates/companies/partials/company_standard.html — contratto: company · open_needs #}
{% load i18n %}
<section class="company-standard chapter--dark" aria-label="{% translate 'Votre entreprise' %}">
  <div class="container company-standard__inner">
    <div>
      <p class="company-standard__eyebrow">{% translate "Entreprise" %}</p>
      <h1 class="company-standard__name" dir="auto">{{ company.legal_name }}</h1>
      <p class="company-standard__ref">{{ company.registration_number }}</p>
      {% if company.is_verified %}
      <p class="company-standard__seal">{% svg_icon "seal" "icon" %}
        <span>{{ company.verification_label }}</span></p>
      {% else %}
      <p class="company-standard__seal company-standard__seal--none">
        <span>{% translate "La transmission d’un besoin est possible une fois la vérification prononcée." %}</span></p>
      {% endif %}
      <dl class="company-standard__facts">
        <div class="company-standard__fact"><dt>{% translate "Secteur" %}</dt>
          <dd>{% if company.sector %}{{ company.sector.label }}{% else %}—{% endif %}</dd></div>
        <div class="company-standard__fact"><dt>{% translate "Établissement" %}</dt>
          <dd>{% if company.city %}{{ company.city }}{% if company.country %}, {{ company.country }}{% endif %}{% else %}—{% endif %}</dd></div>
        <div class="company-standard__fact company-standard__fact--wide">
          <dt>{% translate "Besoins ouverts" %}</dt>
          <dd>{% blocktranslate count n=open_needs|length asvar besoins_word %}{{ n }} besoin en cours{% plural %}{{ n }} besoins en cours{% endblocktranslate %}
            {% include "components/meter.html" with mode="count" positions=5 at=open_needs|length word=besoins_word inline=True %}</dd></div>
      </dl>
    </div>
    <div class="company-standard__cartouche">{% include "companies/partials/territory_cartouche.svg" %}</div>
  </div>
</section>
```

**Misurato, candidato servito come `<link>` same-origin:** l'insegna è alta **229 px** a 1440×900 e
**241 px** a 390×844 (contro **160** e **348** di oggi). Cioè: **+69 px a desktop, −107 px a telefono** —
il 12,7 % del primo viewport restituito dove costava di più. Il round 1 prometteva «200/156» e «192 px di
telefono restituiti»: erano cifre non eseguite, e questi sono i numeri veri.
In arabo l'insegna misura **233 px** a 1440 e non produce scorrimento orizzontale.

Il **cartiglio territoriale** (280×160, nascosto sotto 1024) è un frammento di graticola generato a build
time (§4.D): **due** tacche — `company.city, company.country` e il territorio del besoin più avanzato — e le
loro etichette in mono. `aria-hidden="true"`: l'alternativa testuale è già la riga dei fatti sotto, per
esteso. **Non è una mappa con spilli**, non ha contorni nazionali, non ha bandiere.
La graticola è disegnata a `stroke-opacity: .22` e le tacche a `.5`: **è decorazione, non informazione**, e
1.4.11 non le si applica — lo dico esplicitamente perché il round 1 citava «`--terr-line` su `--mid-2` 5,51
(grafica, ≥ 3:1 ampiamente)» come se coprisse anche l'opacità. Non la copre: ricomposto,
`--terr-line` al 34 % su `--mid-1` dà **#1F4A53 = 1,80:1** e al 18 % dà **#17343C = 1,33:1**. Il 5,51 vale
per la tinta piena, che è quella che porta **informazione** (i nodi del misuratore), e quella sì è a norma.

#### A.2 Il ritmo della pagina — un registro e un margine (`dashboard.html`)

Il round 1 chiamava «bento» una griglia `minmax(0,7fr) minmax(0,5fr)`. La revisione ha ragione: è un 60/40,
cioè lo stesso cruscotto a due colonne che il committente ha già respinto, riproporzionato. **La parola e la
cosa sono cancellate.**

Al loro posto la grammatica che questo prodotto possiede davvero: **una colonna di lettura e un margine.**
Un registro contabile ha un corpo e un margine; il margine non porta schede, porta **note marginali** —
allineate a un unico filetto, con gli ordinali in mono nella gronda. È diverso dal cruscotto persona (che non
ha margine), è diverso da un cruscotto SaaS (che ha schede), ed è la cosa che il prodotto è.

```css
.workbench { display: grid; gap: var(--s-12); grid-template-columns: minmax(0, 1fr); }
@media (min-width: 75rem) {
  .workbench { grid-template-columns: minmax(0, 8fr) minmax(0, 4fr); align-items: start; }
  .workbench__ledger { grid-column: 1; }
  .workbench__margin { grid-column: 2; position: sticky;
    inset-block-start: calc(var(--chrome-height) + var(--s-6));
    display: grid; gap: var(--s-8); padding-inline-start: var(--s-6);
    border-inline-start: 1px solid var(--hairline); }
}
.workbench__note { display: grid; gap: var(--s-2); }
.workbench__note > h3 { margin: 0; font-family: var(--f-mono); font-size: var(--t-folio);
  line-height: var(--t-folio-lh); letter-spacing: .08em; text-transform: uppercase;
  color: var(--ink-3); }
.workbench__demand { margin: 0; padding: 0; list-style: none; display: grid; gap: var(--s-2); }
.workbench__demand li { display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: var(--s-3);
  padding-block: var(--s-2); border-block-end: 1px solid var(--hairline);
  font-size: var(--t-ui); line-height: var(--t-ui-lh); }
.workbench__demand .t-ref { font-family: var(--f-mono); font-size: var(--t-caption);
  color: var(--ink-3); font-variant-numeric: tabular-nums; }
/* l'unica regione vuota ammessa: una striscia, e UNA SOLA per pagina (§8 rischio 3) */
.strip { display: flex; align-items: center; gap: var(--s-4); min-block-size: 96px;
  padding-inline: var(--s-4); border-block: 1px solid var(--hairline);
  font-size: var(--t-ui); line-height: var(--t-ui-lh); color: var(--ink-3); }
.strip__glyph { inline-size: 28px; block-size: 28px; flex: 0 0 auto; color: var(--hairline-strong); }
```

**Il margine — «CE QUI EST DEMANDÉ» — è PER BESOIN, non aggregato** (lacuna 12). L'aggregazione fra besoins
richiedeva una deduplicazione, un ordinamento e un `min()` che il linguaggio dei template non esprime; il
round 1 la prescriveva lo stesso. **È eliminata.** La nota a margine elenca, per ciascuno dei **primi tre**
besoins aperti, le **prime quattro** competenze obbligatorie con il riferimento del besoin e la sua data:

```django
{% for need in open_needs|slice:":3" %}
<div class="workbench__note">
  <h3>{{ need.reference }}{% if need.start_from %} · <time datetime="{{ need.start_from|date:'Y-m-d' }}">{{ need.start_from|date:"d.m.Y" }}</time>{% endif %}</h3>
  {% with ms=need.mandatory_skills %}
  {% if ms %}
  <ul class="workbench__demand">
    {% for skill in ms|slice:":4" %}<li><span>{{ skill.label }}</span><span class="t-ref">{{ need.reference }}</span></li>{% endfor %}
  </ul>
  {% if ms|length > 4 %}<p class="t-caption">{% blocktranslate count n=ms|length|add:"-4" %}et {{ n }} autre compétence obligatoire{% plural %}et {{ n }} autres compétences obligatoires{% endblocktranslate %}</p>{% endif %}
  {% endif %}
  {% endwith %}
  {% if need.training_needs or need.safety_training_required %}
  <p class="t-caption">{% translate "Formation à prévoir" %}</p>
  {% endif %}
</div>
{% endfor %}
```

Nessun `dictsort`, nessun `min()`, nessuna deduplicazione, nessuna riga di Python.
**Regola dura: se `open_needs` è vuoto, il margine non si disegna.** Un tassello vuoto è peggio del vuoto.

**Il cruscotto senza impresa** (lacuna 11) — `dashboard.html:32-45`, il ramo `{% if not company %}`, che è
**la prima schermata di ogni conto nuovo** e che il round 1 lasciava al disegno vecchio. Riceve la stessa
insegna, in variante `--empty`: eyebrow `ESPACE ENTREPRISE`, `<h1>` «Espace entreprise», e **il testo
bloccato verbatim**, che non si tocca né si riassume:

> «Déclarez votre entreprise, puis exprimez vos besoins en compétences. Le projet recueille des besoins : il
> ne présente aucune personne et ne promet aucun résultat.»

Sotto, **una sola** `.strip` con la grammatica del §9.6 (un filetto, il glifo arco+gradini a tratto, la frase
che dice chi riempie e quando, l'azione inline) e il primario «Déclarer mon entreprise» a 48 px. La regione
`01 BESOINS`, `02`, `03`, `04` non si disegnano: non c'è nulla da disegnarle dentro.

#### A.3 Il registro dei besoins (`partials/need_register.html`)

Ogni voce passa da `<li>` nudo a **foglio di livello 2**: `background: var(--min-2)`, `border: 1px solid
var(--hairline)`, **raggio 0** (§2: «Raggi: 0 sui capitoli e sui fogli»), **nessuna ombra a riposo**,
`--shadow-2` **solo in hover**, e un **filo di rilegatura** di 3 px nella trama del responsabile.

**Misurato a 1440×900**: riga **1240 × 74 px** (contro **976 × 90** di oggi — 16 px di densità guadagnati,
che è la sola riga della query 7 che accetto), griglia computata
`40px · 767,16px · 86,84px · 216px · 24px`, pista del misuratore **110 px**, colonna del record **216 px**.
In arabo: **1240 × 77-78 px**, griglia `40px · 789,27px · 64,73px · 216px · 24px`, **nessuno** scorrimento
orizzontale. A 390: **350 × 152-180 px** secondo la lunghezza del titolo, nessuno scorrimento orizzontale.

```html
<li class="need" data-owner="…" data-passed="…" data-now="…" data-condition="…">
  <a class="need__link" href="…">
    <span class="need__ordinal">01</span>
    <span class="need__body">
      <span class="need__title" dir="auto">…</span>
      <span class="need__gloss"><span class="t-ref">BA2E6298AF</span> · Rovigo · Construction navale
        · 4 profils · <span class="need__owner">…glifo + nome…</span></span>
    </span>
    <span class="state state--…">Pris en charge</span>       <!-- di badges.md -->
    <span class="need__record">…components/meter.html, mode="record"…</span>
    <svg class="need__go icon icon--flip-rtl">…</svg>
  </a>
</li>
```

```css
.needs { margin: 0; padding: 0; list-style: none; display: grid; gap: 4px; }
.need { position: relative; background: var(--min-2);
  border: 1px solid var(--hairline); border-radius: 0; }
.need__link { display: grid; align-items: center; column-gap: var(--s-4);
  grid-template-columns: 40px minmax(0, 1fr); min-block-size: 72px;
  padding: var(--s-3) var(--s-4) var(--s-3) var(--s-6);
  color: inherit; text-decoration: none; }
@media (min-width: 48rem) {
  .need__link { grid-template-columns: 40px minmax(0, 1fr) auto var(--need-rec, 216px) 24px; }
}
/* IL FILO DI RILEGATURA — 3 px, ed è l'unico posto in cui una trama si
   disegna su questa superficie. Niente di più largo di 3 px la porta mai. */
.need::before { content: ""; position: absolute; inset-block: -1px; inset-inline-start: -1px;
  inline-size: 3px; background-color: var(--owner-ink, transparent);
  background-image: var(--owner-weave, none); background-size: var(--owner-weave-size, auto); }
.need[data-owner=""]::before, .need[data-owner~="none"]::before { background: none; }
.need__ordinal { font-family: var(--f-mono); font-size: var(--t-folio);
  line-height: var(--t-folio-lh); font-variant-numeric: tabular-nums; color: var(--ink-3);
  align-self: start; padding-block-start: 2px; }
.need__body { min-inline-size: 0; }
.need__title { margin: 0; font-size: var(--t-ui); line-height: var(--t-ui-lh);
  font-weight: 500; color: var(--ink); overflow-wrap: anywhere; }
.need__gloss { display: block; margin-block-start: 2px; font-size: var(--t-caption);
  line-height: var(--t-caption-lh); color: var(--ink-3); }
.need__gloss .t-ref { font-family: var(--f-mono); font-variant-numeric: tabular-nums; }
.need__owner { color: var(--ink-2); }
.need__owner .icon { inline-size: 14px; block-size: 14px; vertical-align: -2px;
  margin-inline-end: 4px; color: var(--owner-ink, var(--ink-3)); }
.need__record { display: grid; gap: var(--s-1); justify-items: start; }
.need__go { inline-size: 24px; block-size: 24px; color: var(--ink-3); justify-self: end; }
@media (max-width: 47.9375rem) {
  .need__link { grid-template-areas: "ord body" "ord rec"; row-gap: var(--s-2);
    align-items: start; padding-inline: var(--s-5) var(--s-3); min-block-size: 0; }
  .need__ordinal { grid-area: ord; } .need__body { grid-area: body; }
  .need__record { grid-area: rec; display: flex; flex-wrap: wrap; align-items: center;
    gap: var(--s-2) var(--s-3); }
  .need .chip, .need .state { order: -1; }
  .need__record .meter { grid-auto-flow: column; align-items: center; gap: var(--s-3); }
  .need__go { position: absolute; inset-block-start: var(--s-3); inset-inline-end: var(--s-3); }
}
@media (hover: hover) {
  .need:hover { background: var(--min-3); box-shadow: var(--shadow-2); }
  .need:hover .need__go { transform: translateX(2px); }
  [dir="rtl"] .need:hover .need__go { transform: translateX(-2px); }
}
.need:active { transform: translateY(1px); }
.need[aria-busy="true"] .need__title, .need[aria-busy="true"] .need__gloss,
.need[aria-busy="true"] .need__record { background: var(--min-1); color: transparent; }
@media (prefers-reduced-motion: no-preference) {
  .need { transition: background-color var(--motion-fast) var(--ease-out); }
  .need__go { transition: transform var(--motion-fast) var(--ease-out); }
  .need:active { transition-duration: var(--motion-instant); }
}
```

**Il focus non è dichiarato qui**: è quello della shell, verbatim (`buttons.md` §4, `platform-shell.md` §9).
`grep -c "focus-visible" v3/workbench.css` → 0.

##### Come il template produce `data-passed`, `data-now`, `data-condition`, `data-owner`

Questo è il cuore del **MUST-FIX 3**, ed è interamente template + CSS.

```django
{% for need in needs %}
<li class="need"
    data-owner="{% for a in need.live_assignments %}{{ a.role }} {% endfor %}"
    data-passed="{% for e in need.events.all %}{{ e.to_status }} {% endfor %}"
    data-now="{% if need.status == 'on_hold' or need.status == 'withdrawn' %}{{ need.events.last.from_status|default:'draft' }}{% else %}{{ need.status }}{% endif %}"
    {% if need.status == 'on_hold' %}data-condition="on_hold"{% endif %}
    {% if need.status == 'withdrawn' %}data-condition="withdrawn"{% endif %}>
```

Quattro cose da dire, tutte verificate:

1. **`data-passed` è la storia reale.** `NeedEvent.to_status` (`models.py:805`) e l'ordinamento
   `["created_at", "id"]` (`:812`). Un besoin che ha fatto `UNDER_REVIEW → CLOSED` non ha mai un evento
   `in_progress`, quindi «Pris en charge» **resta vuoto**. Un besoin tornato indietro (`UNDER_REVIEW →
   SUBMITTED`) mostra entrambe le tappe registrate, perché entrambe lo sono.
2. **`data-now` per `on_hold` e `withdrawn` è la tappa TENUTA**, non la condizione. `need.events.last`
   restituisce l'ultimo evento e il suo `from_status` è lo stato da cui si è usciti — cioè esattamente «dove
   il besoin sta fermo». `|default:'draft'` copre il besoin senza eventi.
3. **`data-owner` serve SOLO alla trama** (lacuna 13). Il blocco «Responsable» di `need_detail.html:37-58`
   **non si tocca**: `services.responsible_for` (`services.py:423`) è l'unica cosa che porta `authorisation`
   e `valid_until`, e la frase «Autorisation {ref} — valable jusqu'au {date}» resta dov'è, con le parole che
   ha. `need.live_assignments` (`models.py:659`) è letto **unicamente** per `role`.
4. **Costo, dichiarato:** `need.events.all` e `need.live_assignments` sono relazioni, quindi il registro fa
   **due query per riga**. Con i quattro besoins del seed sono otto query. Se il numero di besoins per
   impresa cresce, la correzione è `.prefetch_related("events", "assignments")` in `services.needs_of` — **una
   riga**, e la registro qui come debito noto anziché scoprirla in produzione. Non la chiedo ora.

##### La parola, che è l'unica resa accessibile

La catena `{% if %}` vive **nel partial** e non altrove (non c'è più nessun parametro `label`, e non c'è più
la doppia sorgente che la revisione ha trovato fra §4.0 e §6):

| `need.status` | La parola | Stato del misuratore |
|---|---|---|
| `draft` | «Étape 1 sur 5» | nodo su `draft`, anello |
| `submitted` | «Étape 2 sur 5» | nodi su ciò che è registrato |
| `under_review` | «Étape 3 sur 5» | idem |
| `in_progress` | «Étape 4 sur 5» | idem |
| `closed`, con tutte le tappe registrate | «Étape 5 sur 5» | cinque nodi |
| `closed`, con una tappa mai registrata | **«Étape 5 sur 5 — une étape non enregistrée»** | il buco è visibile e la parola lo nomina |
| `on_hold` | **«Position tenue à l'étape N sur 5»** | nodi registrati pieni, nodo corrente **aperto** |
| `withdrawn` | **«Retiré à l'étape N sur 5»** | filetto punteggiato, nodi aperti |

Non c'è nessun off-by-one da spiegare (lacuna 2) perché **in modo `record` non esiste un `at`**: la parola
conta le tappe, il CSS accende i nodi, e i due non si parlano attraverso un numero.
Larghezze misurate a 12 px Fira Sans: «Étape 2 sur 5» **64,06 px** · «Position tenue à l'étape 3 sur 5»
**146,61 px** · «Étape 5 sur 5 — une étape non enregistrée» **202,13 px** — tutte su **una riga** dentro i
216 px della colonna. Per questo la colonna è 216 e non i 140 che il round 1 scriveva senza misurarli.

#### A.4 La pagina del besoin (`need_detail.html`) — `data-mode="rich"`, e nessun capitolo scuro

Sopra il titolo entra **la barra di lavorazione**: un `<ol class="workflow">` a cinque segmenti
(Préparation · Transmis · En examen · Pris en charge · Clos) con **la stessa identica logica** del
misuratore — `data-passed`, `data-now`, `data-condition` sull'`<ol>`, `data-stage` su ogni `<li>`.

**`aria-current="step"`** va sul `<li>` la cui tappa è uguale a `data-now`, prodotto dalla stessa catena
`{% if %}`; per `on_hold` e `withdrawn` va **sulla tappa tenuta**, che è dove il besoin sta davvero, e la
condizione è detta da una `<p class="workflow-note">` **sopra** la barra, referenziata da
`aria-describedby` sull'`<ol>`:

> «En attente depuis le {{ need.status_since }}. {{ need.hold_reason }} — la position acquise est conservée.»
> «Retiré par l'entreprise le {{ need.status_since }}. Les étapes déjà enregistrées restent au dossier.»

E, quando la storia ha un buco, una seconda riga, che è la frase giuridicamente più importante di questa spec:

> «Ce besoin a été clos sans avoir été pris en charge : aucune étape « Pris en charge » n'a été enregistrée.»

```css
.workflow { margin: 0 0 var(--s-8); padding: 0; list-style: none;
  display: grid; grid-auto-flow: row; gap: var(--s-2); }
@media (min-width: 64rem) {
  .workflow { grid-auto-flow: column; grid-auto-columns: minmax(0, 1fr); gap: var(--s-4); }
}
.workflow__step { display: grid; grid-template-columns: 10px minmax(0, 1fr);
  column-gap: var(--s-3); align-items: center; min-block-size: 36px; }
@media (min-width: 64rem) {
  .workflow__step { grid-template-columns: minmax(0, 1fr); row-gap: var(--s-2);
    align-content: start; align-items: start; min-block-size: 0; }
}
.workflow__bar { inline-size: 10px; block-size: 100%; min-block-size: 28px;
  border: 1px dashed var(--hairline-strong); background-color: transparent; }
@media (min-width: 64rem) {
  .workflow__bar { inline-size: auto; block-size: 10px; min-block-size: 0; }
}
.workflow__word { font-size: var(--t-ui); line-height: var(--t-ui-lh); color: var(--ink-3);
  grid-column: 2; }
.workflow__who { font-size: var(--t-caption); line-height: var(--t-caption-lh);
  color: var(--ink-3); grid-column: 2; }
@media (min-width: 64rem) { .workflow__word, .workflow__who { grid-column: auto; } }
.workflow__who .icon { inline-size: 14px; block-size: 14px; vertical-align: -2px;
  margin-inline-end: 4px; color: var(--owner-ink, var(--ink-3)); }

/* un segmento è inchiostrato SE E SOLO SE il database ha registrato quella transizione */
[data-passed~="draft"] .workflow__step[data-stage="draft"] .workflow__bar,
[data-passed~="submitted"] .workflow__step[data-stage="submitted"] .workflow__bar,
[data-passed~="under_review"] .workflow__step[data-stage="under_review"] .workflow__bar,
[data-passed~="in_progress"] .workflow__step[data-stage="in_progress"] .workflow__bar,
[data-passed~="closed"] .workflow__step[data-stage="closed"] .workflow__bar,
[data-now="draft"] .workflow__step[data-stage="draft"] .workflow__bar,
[data-now="submitted"] .workflow__step[data-stage="submitted"] .workflow__bar,
[data-now="under_review"] .workflow__step[data-stage="under_review"] .workflow__bar,
[data-now="in_progress"] .workflow__step[data-stage="in_progress"] .workflow__bar,
[data-now="closed"] .workflow__step[data-stage="closed"] .workflow__bar {
  border-style: solid; border-color: var(--owner-ink, var(--ink-2));
  background-color: var(--owner-ink, var(--ink-2));
  background-image: var(--owner-weave, none); background-size: var(--owner-weave-size, auto); }
/* …e la parola del segmento registrato passa da --ink-3 a --ink: stessa regola, stessa lista */
[data-passed~="draft"] .workflow__step[data-stage="draft"] .workflow__word,
[data-passed~="submitted"] .workflow__step[data-stage="submitted"] .workflow__word,
[data-passed~="under_review"] .workflow__step[data-stage="under_review"] .workflow__word,
[data-passed~="in_progress"] .workflow__step[data-stage="in_progress"] .workflow__word,
[data-passed~="closed"] .workflow__step[data-stage="closed"] .workflow__word,
[data-now="draft"] .workflow__step[data-stage="draft"] .workflow__word,
[data-now="submitted"] .workflow__step[data-stage="submitted"] .workflow__word,
[data-now="under_review"] .workflow__step[data-stage="under_review"] .workflow__word,
[data-now="in_progress"] .workflow__step[data-stage="in_progress"] .workflow__word,
[data-now="closed"] .workflow__step[data-stage="closed"] .workflow__word { color: var(--ink); }

.workflow__step[aria-current="step"] .workflow__bar {
  outline: 1.5px solid var(--accent-ring); outline-offset: 2px; }
.workflow__step[aria-current="step"] .workflow__word { font-weight: 500; color: var(--ink); }
[data-condition="on_hold"] .workflow__step[aria-current="step"] .workflow__bar {
  background-image: none; background-color: transparent; }
[data-condition="withdrawn"][data-passed] .workflow__step[data-stage] .workflow__bar {
  border-style: dotted; background-image: none; background-color: transparent;
  border-color: var(--ink-3); }
.workflow-note { margin: 0 0 var(--s-6); font-size: var(--t-small); line-height: var(--t-small-lh);
  color: var(--ink-2); display: flex; align-items: center; gap: var(--s-2); }
@media (prefers-reduced-motion: no-preference) {
  .workflow__bar { transform: scaleX(1); transform-origin: inline-start center;
    transition: transform var(--motion-base) var(--ease-standard); }
  .workflow[data-enter] .workflow__step[aria-current="step"] .workflow__bar { transform: scaleX(0); }
}
@media (forced-colors: active) {
  .workflow__bar { forced-color-adjust: none; border-color: CanvasText; }
  .need::before { forced-color-adjust: none; }
}
```

**Misurato:** a 1440 la barra è alta **62 px** con cinque segmenti da **235,2 px**; a 390 diventa una spina
verticale (barra da 10 px a lato, parola e responsabile a fianco) alta **252 px** in tutto, contro i 358 px
che avrebbero occupato cinque blocchi impilati.

Le due tabelle «Ce que décrit le besoin» e «Compétences» **restano tabelle**: `font-variant-numeric:
tabular-nums`, righe 48 px, hover di riga a livello 2, `caption` **visibile** invece che `visually-hidden`.
Nessuna ombra, nessuna fotografia, nessun reveal, nessun loop: `need_detail` dichiara RICH perché il §7 glielo
assegna, e **non spende** il budget che RICH le concede.

### 4.B IL FORUM PUBBLICO — «due rive, un tavolo» (`v3/forum.css`)

Modalità **IMMERSIVE**: due capitoli mezzanotte (hero e relazione), isoipse ammesse, **un** oggetto vivo.

#### B.1 L'hero (`partials/hero.html`)

Da rettangolo piatto a capitolo costruito. **Misurato con il candidato:** `min-block-size: min(72vh, 680px)`
a desktop rende **648 px** su un viewport da 900 (contro **388,16**), e `56vh` a 390 rende **472,63 px**
(contro **429,66**) — ma con dentro qualcosa invece che niente. L'`h1` passa a `--t-plate` **64/64** a
desktop e `--t-band` **32/36** a 390, misurati entrambi: **mai più i 30,4 px fuori scala** del §1.5.

Strati, dal fondo: `--mid-1` · graticola 160 px `--terr-line` al 18 % · **due rilievi di isoipse** (nord in
alto a destra, sud in basso a sinistra, generati a build time, ≤ 43 KB inline, il tetto del §6 del sistema) ·
maschera ellittica sotto la colonna di testo · **l'arco**: quando `event.hero_image` esiste
(`apps/forum/models.py:91`), la fotografia **dentro l'arco** — `aspect-ratio: 3/4`, raggio 190/190/0/0,
opacità .50, `saturate(.8)`, vignetta `--mid-1`, `<picture>` AVIF/WebP 480/800/1200 con `sizes`,
`fetchpriority="high"`, **≤ 120 KB per viewport**, attraverso `{% plate %}` di `imagery.md`. Quando non
esiste, **l'arco resta, disegnato a filetto**: il prodotto è riconoscibile senza fotografia.

I loghi di patronato restano esattamente come il gate G6 li rende: `services.public_partners()`
(`apps/forum/services.py:101-106`, `authorized=True, logo__isnull=False, is_public`). Quando la lista è
vuota, **niente** — non un riquadro grigio, non un segnaposto.

La striscia di chiusura porta le coordinate delle due rive in mono e il controllo **«Suspendre le
mouvement»** (obbligatorio: la pagina ha un oggetto vivo).

```css
.forum-hero { position: relative; isolation: isolate; overflow: clip;
  min-block-size: 56vh; display: grid; align-items: center;
  padding-block: var(--s-16) var(--s-12); background: var(--mid-1); color: var(--on-dark); }
@media (min-width: 64rem) { .forum-hero { min-block-size: min(72vh, 680px); } }
.forum-hero__field { position: absolute; inset: 0; z-index: -1; pointer-events: none; }
.forum-hero__field svg { position: absolute; inset: 0; inline-size: 100%; block-size: 100%; }
.forum-hero .terr__grid line { stroke: var(--terr-line); stroke-opacity: .18; stroke-width: 1; }
.forum-hero .terr__ticks path { stroke: var(--terr-line); stroke-opacity: .34; stroke-width: 1; }
.forum-hero .terr__layer path { fill: none; stroke: var(--terr-line); }
.forum-hero .terr__layer--1 path { stroke-opacity: .62; stroke-width: 1.1; }
.forum-hero .terr__layer--2 path { stroke-opacity: .38; stroke-width: .9; }

.forum-hero__inner { display: grid; gap: var(--s-8); grid-template-columns: minmax(0, 1fr); }
@media (min-width: 64rem) {
  .forum-hero__inner { grid-template-columns: minmax(0, 7fr) minmax(0, 5fr);
    column-gap: var(--s-16); align-items: center; }
}
.forum-hero__eyebrow { margin: 0; font-family: var(--f-mono); font-size: var(--t-folio);
  line-height: var(--t-folio-lh); letter-spacing: .08em; text-transform: uppercase;
  color: var(--on-dark-3); }                                   /* 6,44:1 */
.forum-hero__title { margin: var(--s-3) 0 0; font-family: var(--f-serif); font-weight: 300;
  font-size: var(--t-band); line-height: var(--t-band-lh); color: var(--on-dark); }
@media (min-width: 64rem) {
  .forum-hero__title { font-size: var(--t-plate); line-height: var(--t-plate-lh);
    letter-spacing: -.015em; }                        /* tracking negativo solo >= 40 px */
}
.forum-hero__lead { margin: var(--s-4) 0 0; font-family: var(--f-serif); font-style: italic;
  font-size: var(--t-lead); line-height: var(--t-lead-lh); color: var(--on-dark-2);
  max-inline-size: 42ch; }
.forum-hero__meta { margin: var(--s-6) 0 0; display: flex; flex-wrap: wrap;
  gap: var(--s-2) var(--s-6); font-family: var(--f-mono); font-size: var(--t-folio);
  line-height: var(--t-folio-lh); font-variant-numeric: tabular-nums; color: var(--on-dark-2); }
.forum-hero__patronage { margin: var(--s-4) 0 0; font-size: var(--t-small);
  line-height: var(--t-small-lh); color: var(--on-dark-2); }
.forum-hero__actions { margin: var(--s-8) 0 0; display: flex; flex-wrap: wrap; gap: var(--s-3); }

/* l'arco: DESIGN_SYSTEM_V2 §8.4, portato qui senza la porta intera */
.forum-hero__arch { position: relative; inline-size: 100%; max-inline-size: 420px;
  aspect-ratio: 3 / 4; border-radius: 190px 190px 0 0; overflow: clip;
  border: 1px solid var(--terr-line); justify-self: center; }
.forum-hero__arch::after { content: ""; position: absolute; inset: 16px 16px 0;
  border-radius: 174px 174px 0 0; border: 1px solid var(--terr-line); opacity: .6; }
.forum-hero__arch img { inline-size: 100%; block-size: 100%; object-fit: cover;
  opacity: .5; filter: saturate(.8); }  /* STATICO, mai animato: nessun filter in loop */
.forum-hero__arch--empty { background: var(--mid-2); }
.forum-hero__close { margin-block-start: var(--s-8); display: flex; flex-wrap: wrap;
  align-items: center; justify-content: space-between; gap: var(--s-4);
  padding-block-start: var(--s-3); border-block-start: 1px solid var(--hairline-dark);
  font-family: var(--f-mono); font-size: var(--t-folio); line-height: var(--t-folio-lh);
  color: var(--on-dark-3); }
```

#### B.2 La relazione Italia-Marocco (nuovo `partials/relation.html`)

Il **secondo** capitolo mezzanotte, su `--mid-2`, fra «Qu'est-ce que le Forum» e «Objectifs». Un SVG
**statico, generato a build time** (§4.D): due rive stilizzate — **non contorni nazionali**, frammenti di
graticola — e fra esse **un arco** Bézier quadratica da 33.97 N 6.85 W a 45.41 N 11.88 E (le coordinate di
`DESIGN_SYSTEM_V2` §8.3), `--terr-line` 1,5 px, che si traccia in `stroke-dashoffset` legato allo scroll.
Sull'arco, **sei nodi di attori** con etichette mono (persona · organisme de formation · université ·
autorité compétente · entreprise · institution); il nodo «autorité» porta l'anello bronzo `--seal-300`
(**7,72:1** su `--mid-1`).

**Sotto, sempre, l'alternativa testuale**: un `<ol>` con le stesse sei voci, **visibile**, non
`visually-hidden` — è contenuto, non didascalia. Sotto 720 px l'SVG **si nasconde** (`display: none` in
`@media (max-width: 44.9375rem)`) e resta la sola lista: una relazione a sei nodi su 390 px non si legge.
Nessun nome, nessun logo, nessuna bandiera: solo ruoli.

```css
.relation { background: var(--mid-2); color: var(--on-dark); padding-block: var(--s-16); }
.relation__figure { margin: 0 0 var(--s-8); }
.relation__figure svg { inline-size: 100%; block-size: auto; display: block; }
.relation .terr__route { fill: none; stroke: var(--terr-line); stroke-width: 1.5;
  stroke-linecap: round; }
.relation .terr__node { fill: none; stroke: var(--terr-line); stroke-width: 1.5; }
.relation .terr__node--seal { stroke: var(--seal-300); }       /* 7,72:1 su --mid-1 */
.relation .terr__label { fill: var(--on-dark-2); font-family: var(--f-mono); font-size: 12px; }
@media (max-width: 44.9375rem) { .relation__figure { display: none; } }
.relation__list { margin: 0; padding: 0; list-style: none; display: grid; gap: var(--s-3); }
@media (min-width: 64rem) {
  .relation__list { grid-template-columns: repeat(3, minmax(0, 1fr)); gap: var(--s-6); }
}
.relation__item { display: grid; grid-template-columns: 28px minmax(0, 1fr); gap: var(--s-3);
  padding-block: var(--s-3); border-block-start: 1px solid var(--hairline-dark);
  font-size: var(--t-ui); line-height: var(--t-ui-lh); }
.relation__item .icon { inline-size: 20px; block-size: 20px; color: var(--terr-line); }
.relation__item[data-role="authority"] .icon { color: var(--seal-300); }
.relation__role { color: var(--on-dark); }
.relation__place { display: block; font-family: var(--f-mono); font-size: var(--t-caption);
  line-height: var(--t-caption-lh); color: var(--on-dark-3); }
```

#### B.3 L'agenda e la navigazione locale

Il programma diventa una **timeline a doppio orientamento con un solo markup** (principio di 21st #3):
`<ol class="agenda">` con, a ≥ 1024, una dorsale 1 px `--hairline-strong` e nodi da 12 px; sotto 1024 la
dorsale scompare e resta l'elenco. Ogni voce: `time_label` in mono tabellare **quando esiste** — e quando non
esiste (**7 casi su 8 oggi**, riverificato) **l'ordinale prende il suo posto nella stessa colonna, in mono**,
così la colonna non si svuota; titolo `--t-entry` 22/28; descrizione `--t-body`; nodo pieno per le voci con
orario, a filetto per le altre (`[data-timed]`). La dorsale **non è legata allo scroll**: è completa e ferma, perché il §4 del documento di moto ammette un
solo oggetto indicizzato per pagina e sul Forum quell'oggetto è la rotta della relazione (§5). Oltre otto voci
l'agenda rivela per **gruppi**, non per riga (tetto della query 4).

```css
.agenda { margin: 0; padding: 0; list-style: none; display: grid; gap: 0; position: relative; }
.agenda__item { display: grid; grid-template-columns: 72px minmax(0, 1fr);
  column-gap: var(--s-4); padding-block: var(--s-4);
  border-block-end: 1px solid var(--hairline); position: relative; }
@media (min-width: 64rem) {
  .agenda__item { grid-template-columns: 88px 24px minmax(0, 1fr); column-gap: var(--s-4); }
  .agenda__spine { position: absolute; inset-block: 0; inset-inline-start: 99px;
    inline-size: 1px; background: var(--hairline-strong); }   /* completa e ferma (§5) */
}
.agenda__when { font-family: var(--f-mono); font-size: var(--t-folio);
  line-height: var(--t-entry-lh); font-variant-numeric: tabular-nums;
  color: var(--ink-3); text-align: end; }
/* l'ordinale PRENDE il posto dell'orario quando l'orario non c'e - 7 voci su 8 oggi */
.agenda__node { display: none; }
@media (min-width: 64rem) {
  .agenda__node { display: block; inline-size: 12px; block-size: 12px; margin-block-start: 8px;
    justify-self: center; border: 1px solid var(--hairline-strong); background: var(--min-0); }
  .agenda__item[data-timed] .agenda__node { background: var(--ink-2); border-color: var(--ink-2); }
}
.agenda__title { margin: 0; font-family: var(--f-serif); font-weight: 400;
  font-size: var(--t-entry); line-height: var(--t-entry-lh); color: var(--ink); }
.agenda__text { margin: var(--s-2) 0 0; font-size: var(--t-body); line-height: var(--t-body-lh);
  color: var(--ink-2); max-inline-size: 65ch; }
```

**`.forum-localnav` — il segnale «cheap» n. 4 è rimosso.** `DESIGN_SYSTEM_V2` §2, livello 6:
«`backdrop-filter` **solo** sull'header scrollato». Quindi: appiccicosa sì, **vetro no**.

```css
.forum-localnav { position: sticky; inset-block-start: var(--chrome-height); z-index: 5;
  background: var(--min-1); border-block-end: 1px solid transparent; }
.forum-localnav[data-stuck] { border-block-end-color: var(--hairline); }
.forum-localnav__list { margin: 0; padding: 0; list-style: none; display: flex;
  gap: var(--s-2); overflow-x: auto; scroll-snap-type: inline proximity;
  scrollbar-width: thin; position: relative; }
.forum-localnav__list a { display: flex; align-items: center; min-block-size: 48px;
  padding-inline: var(--s-3); scroll-snap-align: start; white-space: nowrap;
  font-size: var(--t-ui); line-height: var(--t-ui-lh); color: var(--ink-2);
  text-decoration: none; }
.forum-localnav__list a[aria-current="true"] { color: var(--ink); }
.forum-localnav__mark { position: absolute; inset-block-end: 0; inset-inline-start: 0;
  block-size: 2px; inline-size: 1px; background: var(--accent);
  transform: translateX(var(--mark-x, 0)) scaleX(var(--mark-w, 0)); transform-origin: left center; }
[dir="rtl"] .forum-localnav__mark { transform-origin: right center; }
```

**Misurato con il candidato:** `position: sticky`, `background-color: rgb(236, 235, 230)` = `--min-1`,
**`backdrop-filter: none`**, altezza del bersaglio di ogni voce **50,19 px** (≥ 48). Il filetto attivo è
l'**unica** cosa che `--accent` fa su questa pagina, perché è navigazione — e si muove per `transform` su un
solo elemento, quindi l'asserzione «0 layout e 0 paint oltre il primo frame» del §7 è ora vera (con il
`backdrop-filter` non lo era, e la revisione aveva ragione).

#### B.4 Intervenienti, risultati, partner, fascia CTA

**`partials/speakers.html`** — da riquadri grigi a **griglia di ruoli**: `repeat(auto-fit, minmax(260px,
1fr))`, ogni voce un foglio `--min-2` con il filo di rilegatura da 3 px nella trama del ruolo, il **ruolo
istituzionale come titolo** (`--t-entry`), il nome **solo se** esiste, l'organizzazione in mono. Nessuna
fotografia di persona, mai.

> **AVVISO G5, che questa griglia non deve perdere** (MUST-FIX 14). Il template **deve continuare a iterare
> la variabile di contesto `speakers`**, che viene da `apps/forum/services.py:91-98`
> `public_speakers(event)` e che applica `SpeakerRole.public_name(site_flag)`
> (`apps/forum/models.py:248-252`: nome **vuoto** a meno che `names_authorized` **e** il flag di sito **e**
> un riferimento d'autorizzazione di almeno 10 caratteri). `{% if speaker.person_name %}` è sicuro **solo**
> per questo. **Iterare `event.speaker_roles.all` nella nuova griglia pubblicherebbe nomi non autorizzati.**
> Lo stesso vale per `permanent_sections`, che pre-applica `public_name` a `item.public_speaker_name`
> (`services.py:117-119`).

**`permanent_sections.html`** — `.forum-cards` passa a fogli di livello 2 con `--shadow-2` **solo in hover**.
**`.forum-partners` — segnale «cheap» n. 8 rimosso**: la regione **non si disegna** quando
`public_partners()` è vuota (stessa regola dura del §8 rischio 3), perché con G6 in vigore quello è il caso
normale e una riga che non rende niente è peggio del vuoto. Quando almeno un logo autorizzato esiste: altezza
ottica normalizzata (`block-size: 40px; object-fit: contain`) su `--min-2`, **mai in scala di grigi**, mai in
carosello, mai alterato (alterare un logo autorizzato è un rischio legale).

```css
.speakers { margin: 0; padding: 0; list-style: none; display: grid; gap: var(--s-4);
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); }
.speaker { position: relative; padding: var(--s-4) var(--s-4) var(--s-4) var(--s-6);
  background: var(--min-2); border: 1px solid var(--hairline); }
.speaker::before { content: ""; position: absolute; inset-block: -1px; inset-inline-start: -1px;
  inline-size: 3px; background-color: var(--owner-ink, var(--ink-3));
  background-image: var(--owner-weave, none); background-size: var(--owner-weave-size, auto); }
.speaker__role { margin: 0; font-family: var(--f-serif); font-weight: 400;
  font-size: var(--t-entry); line-height: var(--t-entry-lh); color: var(--ink); }
.speaker__name { display: block; margin-block-start: var(--s-2); font-size: var(--t-ui);
  line-height: var(--t-ui-lh); color: var(--ink-2); }
.speaker__org { display: block; font-family: var(--f-mono); font-size: var(--t-caption);
  line-height: var(--t-caption-lh); color: var(--ink-3); }

.forum-cards { display: grid; gap: var(--s-4);
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); }
.forum-cards > * { background: var(--min-2); border: 1px solid var(--hairline);
  padding: var(--s-6); }
@media (hover: hover) { .forum-cards > a:hover { box-shadow: var(--shadow-2); } }

/* la regione NON si disegna quando public_partners() e vuota: la regola e nel template */
.forum-partners__list { margin: 0; padding: 0; list-style: none; display: flex;
  flex-wrap: wrap; align-items: center; gap: var(--s-6); background: var(--min-2);
  padding: var(--s-6); border: 1px solid var(--hairline); }
.forum-partners__list img { block-size: 40px; inline-size: auto; object-fit: contain; }
```

**`cta_row.html` — la correzione cromatica del MUST-FIX 2.** La fascia smette di essere `--brand-navy` e
diventa `--mid-2` (misurato sul candidato: `rgb(20, 36, 46)`; oggi `rgb(15, 37, 71)`).

```css
.forum-cta { background: var(--mid-2); color: var(--on-dark); padding-block: var(--s-12); }
/* L'unico accento interattivo, nella sua luminosità scura.
   --accent #0F6A72 su --mid-2 = 2,52:1 — era un difetto e non c'è più.
   --accent-dark #7FD1D8 su --mid-2 = 9,09:1; etichetta --mid-1 sul pieno = 10,01:1. */
.forum-cta .btn--primary { --btn-bg: var(--accent-dark); --btn-border: var(--accent-dark);
  --btn-fg: var(--mid-1); --btn-bg-hover: var(--on-dark); --btn-border-hover: var(--on-dark);
  --btn-fg-hover: var(--mid-1); --btn-ring: var(--accent-dark); }
/* Il confine dei secondari: --on-dark-2, 8,79:1 — cioè ciò che la build già
   fa (misurato: rgb(183,195,196)), NON --hairline-dark-strong (2,19:1) che il
   round 1 prescriveva, e NON un pieno --mid-4 (1,33:1 su --mid-2). §0-quater. */
.forum-cta .btn--secondary { --btn-border: var(--on-dark-2); --btn-fg: var(--on-dark);
  --btn-border-hover: var(--on-dark); --btn-fg-hover: var(--on-dark);
  --btn-ring: var(--accent-dark); }
```

**E queste due regole non funzionano finché `apps/forum/static/forum/forum.css:144` non è cancellata** —
provato in pagina questo round: con il candidato caricato **dopo**, il bordo computa ancora
`rgb(183, 195, 196)`, perché quella riga scrive la scorciatoia `border:` a specificità (0,2,0) e nessuna
custom property può batterla. È esattamente la lacuna 7 della revisione, e il §4.E la chiude.

Le altezze: il primario è `btn--lg` e i due secondari sono `.btn` nudi, cioè **52 e 44** oggi (§1.9). Con
`buttons.md` in vigore diventano **48 su tutte e tre** e la pila smette di essere dentellata; qui non
ridefinisco nulla di loro.

#### B.5 Il Forum autenticato (`forum/governance/*`) — `data-mode="dense"`

Stessa famiglia, modalità DENSE: **nessun capitolo scuro, nessuna isoipsa, nessun reveal, nessun loop**.
`base_governance.html` riceve la **banda di commissione** su `--min-1` (livello 1, filetto, nessuna ombra):
commissione, mandato, prossima seduta, in mono tabellare. Proposte e progetti passano al foglio di livello 2
con il misuratore in modo **`record`** sullo stato; `participation.html` riceve il filo di rilegatura nella
trama del responsabile. Deve leggere come un tavolo di lavoro fra istituzioni, non come un blog.

```css
.commission-band { background: var(--min-1); border-block-end: 1px solid var(--hairline);
  padding-block: var(--s-5); }                       /* livello 1: filetto, nessuna ombra */
.commission-band__inner { display: flex; flex-wrap: wrap; gap: var(--s-3) var(--s-8);
  align-items: baseline; }
.commission-band__name { margin: 0; font-family: var(--f-serif); font-weight: 400;
  font-size: var(--t-entry); line-height: var(--t-entry-lh); color: var(--ink); }
.commission-band__fact { font-family: var(--f-mono); font-size: var(--t-folio);
  line-height: var(--t-folio-lh); font-variant-numeric: tabular-nums; color: var(--ink-3); }

/* ---- coda di forum.css: moto e forced-colors ----------------------------- */
@media (prefers-reduced-motion: no-preference) {
  /* NESSUNA transizione di box-shadow: l'ombra di ruolo 2 compare in hover
     senza animarsi (MOTION_SYSTEM §2 «mai box-shadow in loop», buttons.md §5). */
  .forum-localnav__mark { transition: transform var(--motion-fast) var(--ease-out); }
  .forum-cards > a { transition: background-color var(--motion-fast) var(--ease-out); }
}
@media (forced-colors: active) {
  .forum-hero .terr__layer path { stroke: GrayText; }
  .forum-hero .terr__grid line, .relation .terr__route { stroke: CanvasText; }
  .speaker::before { forced-color-adjust: none; }
  .forum-localnav__mark { background: Highlight; }
}
```

### 4.C L'ACADEMY — «un vero prodotto di formazione» (`v3/academy.css`)

Modalità **RICH**: **zero** capitoli mezzanotte (l'Academy non ne ha bisogno: ha la carta e una fotografia),
reveal editoriali, nessuna isoipsa, **una** lastra per pagina.

#### C.1 Il cruscotto d'apprendimento (`mine.html`) — riscritto sul contesto che esiste

**Verificato** (`apps/academy/views.py:169-183`): `mine` mette in contesto `ongoing`, `completed`,
`withdrawn`, `plans`, `mandated_plans`, `summary`, e le righe portano le annotazioni
`modules_total` / `modules_attended` (`apps/academy/services.py:126-127`). **Non** porta `progress.*`, che
esiste solo su `enrolment_detail`, e **non** porta `next_module`.

**La riga di ripresa**, di conseguenza, nomina il **corso** e non il prossimo modulo:

```django
{% if ongoing %}{% with row=ongoing.0 %}
<a class="resume" href="{% url 'academy:enrolment' row.uuid %}">
  <span>
    <span class="resume__eyebrow">{% translate "Reprendre" %}</span>
    <span class="resume__title">{{ row.course.title }}</span>
    <span class="resume__meter">{% blocktranslate count n=row.modules_attended asvar w with total=row.modules_total %}{{ n }} module sur {{ total }} suivi{% plural %}{{ n }} modules sur {{ total }} suivis{% endblocktranslate %}
      {% include "components/meter.html" with mode="count" positions=row.modules_total at=row.modules_attended word=w %}</span>
    <span class="resume__where">{% translate "Le prochain module est nommé sur la page de la formation." %}</span>
  </span>
  <span class="btn btn--primary">{% translate "Reprendre" %}</span>
</a>
{% endwith %}{% else %}…{% endif %}
```

Quando non c'è nulla da riprendere, la riga porta **il catalogue**, che è sempre aperto e non condiziona
nulla. Quando `row.modules_total > 8`, il partial stampa la sola cifra: la pista sparisce (§8 rischio 1).
`next_module` per riga resta **rinviato** (§0-bis C3) e lo dichiaro invece di prometterlo.

**Cinque registri, non tre** (MUST-FIX 6). `mine.html` ne ha cinque, e il quinto è deliberatamente separato:

| # | Registro | Contesto | Regola |
|---|---|---|---|
| 1 | Les formations que je suis | `ongoing` | riga di ripresa in testa |
| 2 | Les formations suivies jusqu'au terme | `completed` | **porta la didascalia integrale**, sotto |
| 3 | Les formations interrompues | `withdrawn` | resa solo se non vuota, come oggi |
| 4 | Mes plans de formation | `plans` | **porta la didascalia integrale** nello stato vuoto |
| 5 | **Plans que je consulte au titre d'un mandat** | `mandated_plans` | **REGOLA DURA: non si fonde mai con il 4** |

> **Il quinto registro non si fonde con il quarto, e non è una preferenza di layout.** Una pagina intitolata
> «Mes formations» che elencasse il percorso di un'altra persona fra i propri direbbe una cosa falsa su di
> chi è quel percorso. Ogni riga nomina il dossier su cui poggia il mandato e porta, verbatim:
> «Ce parcours n'est pas le vôtre : vous le consultez au titre de votre affectation sur ce dossier, tant
> qu'elle est en cours.» Il round 1 scriveva «la colonna dei plans passa a destra, 5/12», che invita a
> fonderli. **La frase è cancellata.** Nel margine 5/12 va il registro 4; il registro 5 sta nella colonna di
> lettura, sotto, con il proprio folio «Mandat». Un test lo asserisce (§9).

**Le due didascalie giuridiche restano integrali** (MUST-FIX 13). Non stanno in una striscia da 96 px: la
striscia è per lo **stato vuoto**, e queste due sono contenuto della pagina piena e della pagina vuota
rispettivamente.

```css
.resume { display: grid; gap: var(--s-4); align-items: center;
  grid-template-columns: minmax(0, 1fr);
  padding: var(--s-6); margin-block-end: var(--s-12);
  background: var(--min-2); border: 1px solid var(--hairline); }  /* raggio 0, NESSUNA ombra */
@media (min-width: 48rem) {
  .resume { grid-template-columns: minmax(0, 1fr) auto; column-gap: var(--s-8); }
}
.resume__eyebrow { margin: 0; font-family: var(--f-mono); font-size: var(--t-folio);
  line-height: var(--t-folio-lh); letter-spacing: .08em; text-transform: uppercase;
  color: var(--ink-3); }
.resume__title { margin: var(--s-2) 0 0; font-family: var(--f-serif); font-weight: 400;
  font-size: var(--t-entry); line-height: var(--t-entry-lh); color: var(--ink); }
.resume__meter { margin-block-start: var(--s-3); }
.resume__where { display: block; margin-block-start: var(--s-2); font-size: var(--t-caption);
  line-height: var(--t-caption-lh); color: var(--ink-3); }
@media (hover: hover) { .resume:hover { box-shadow: var(--shadow-2); } }  /* SOLO in hover */

.academy-cols { display: grid; gap: var(--s-12); grid-template-columns: minmax(0, 1fr); }
@media (min-width: 75rem) {
  .academy-cols { grid-template-columns: minmax(0, 7fr) minmax(0, 5fr); align-items: start; }
}
.enrolments { margin: 0; padding: 0; list-style: none; display: grid; gap: 4px; }
.enrolment { position: relative; background: var(--min-2); border: 1px solid var(--hairline); }
.enrolment__link { display: grid; align-items: center; column-gap: var(--s-4);
  grid-template-columns: 40px minmax(0, 1fr); min-block-size: 72px;
  padding: var(--s-3) var(--s-4); color: inherit; text-decoration: none; }
@media (min-width: 48rem) {
  .enrolment__link { grid-template-columns: 40px minmax(0, 1fr) auto 216px 24px; }
}
.enrolment__ordinal { font-family: var(--f-mono); font-size: var(--t-folio);
  line-height: var(--t-folio-lh); font-variant-numeric: tabular-nums; color: var(--ink-3); }
.enrolment__title { margin: 0; font-size: var(--t-ui); line-height: var(--t-ui-lh);
  font-weight: 500; color: var(--ink); }
.enrolment__gloss { display: block; margin-block-start: 2px; font-size: var(--t-caption);
  line-height: var(--t-caption-lh); color: var(--ink-3); }
.enrolment__glyph { inline-size: 20px; block-size: 20px; color: var(--ink-3);
  vertical-align: -4px; margin-inline-end: var(--s-2); }
@media (hover: hover) { .enrolment:hover { box-shadow: var(--shadow-2); } }

.register-note { margin: var(--s-3) 0 0; font-size: var(--t-small);
  line-height: var(--t-small-lh); color: var(--ink-2); max-inline-size: 65ch; }
.register-note--legal { border-inline-start: 2px solid var(--hairline);
  padding-inline-start: var(--s-3); }
```

> Registro 2, sotto l'elenco, in `.register-note--legal` (`--t-small`, `--ink-2`, misura ≤ 65ch):
> «Chaque formation suivie jusqu'au terme donne lieu à une attestation de participation. Elle décrit ce qui
> a été suivi ; elle ne vaut ni titre ni autorisation.»
>
> Registro 4, stato vuoto, in `.empty` **per esteso**:
> «Un plan de formation réunit les cours conseillés pour un objectif donné. Il peut venir de votre
> orientation, d'un professionnel ou d'un besoin de compétences recensé ; il ne conditionne jamais l'accès
> aux cours, qui restent ouverts à tous.»

**Il segnale «cheap» n. 6 — tre strisce identiche — è rimosso da una regola.** Su un conto nuovo tutte e
cinque le regioni sono vuote, e cinque barre grigie identiche sono peggio del vuoto attuale. Quindi:
**una pagina disegna al massimo UNA striscia vuota.** Se due o più registri sono vuoti, i registri vuoti non
si disegnano affatto e la pagina porta **un solo** stato vuoto, in testa, con la grammatica del §9.6 e
l'azione inline. È la stessa regola dura del §8 rischio 3, applicata all'Academy.

#### C.2 Il misuratore dei moduli — e perché qui il cumulativo è vero

`templates/academy/mine.html` vieta barre, anelli e percentuali perché «suggerirebbero une mesure que
personne n'a effectuée». **Il misuratore in modo `count` non è una misura: è il conteggio, disegnato.**
`modules_attended` e `modules_total` sono interi esatti contati dal database (`Count("attendances",
distinct=True)`); le tacche sono `total`, le piene sono `attended`, e la parola accanto resta «3 modules sur
5 suivis», identica a oggi. Oltre 8 posizioni la pista sparisce e resta la cifra. **Nessuna percentuale
compare mai, da nessuna parte**, e un test conta le lunghezze percentuali su `width`/`inline-size` in
`meter.css`: devono essere **0**. (L'unico `%` del foglio è `max-inline-size: 100%` sulla parola, che è una
misura di testo e non un riempimento; il test lo esclude per nome.)

Su `enrolment_detail.html` il contesto è più ricco (`rows` = `services.module_rows`, con la presenza per
modulo) e il misuratore passa a modo **`record`**: una tacca per modulo, `data-stage="{{ row.module.pk }}"`,
`data-passed` costruito dai moduli seguiti. Un modulo seguito fuori ordine si vede per quello che è.

#### C.3 La scheda del corso (`course_detail.html`) — e l'immagine che il committente ha chiesto

**Il round 1 rispondeva a «non abbastanza immagini» con nessuna immagine, e lo vendeva come un pregio
(«costa 0 KB d'immagine»). La revisione ha ragione: è un segnaposto, ripetuto sette volte. È cancellato.**

`course_hero.html` (nuovo): fascia `--min-1`, griglia 7/5. A sinistra: eyebrow «ACADEMY ·
{{ course.get_course_type_display }}», titolo `--t-title` 48/52 (32/36 sotto 1024), `summary` in corsivo
`--t-lead`, e una riga di **quattro fatti in mono** (organisme · durée `{{ course.duration_hours }} h` ·
modalité · langue) con i loro glifi. L'azione d'iscrizione resta un `<form method="post">` e sale nell'hero.

A destra, **il frontespizio**: una **fotografia art-directed dentro l'arco**, rapporto **4:5**, servita da
`{% plate %}` di `imagery.md` con `variant="course"` (DEROGA 2), AVIF/WebP 480/800/1200, `sizes` fornito dal
tag, **≤ 120 KB per viewport**, `alt=""` perché non porta informazione che il testo non porti già.

**Direzione artistica, per i sette domini** — e questa è la parte che rende l'immagine non-stock:

| `CourseType` | Soggetto | Mai |
|---|---|---|
| `italian_language` | una pagina annotata a mano, un dizionario aperto, la luce di una sala di lettura | un'aula con studenti inquadrati |
| `rights_and_duties` | un registro rilegato, un timbro, una scrivania d'ufficio pubblico | un martelletto da giudice, una bilancia |
| `civic_education` | una facciata civica in controluce, una sala consiliare vuota | una bandiera, un monumento turistico |
| `workplace_safety` | un giunto di ponteggio, un casco appeso, un quadro elettrico | una persona che cade, un cartello di pericolo |
| `work_culture` | un banco da lavoro all'inizio del turno, utensili in ordine | una stretta di mano, un «team» che sorride |
| `professional_training` | un tornio, un banco di saldatura, un piano di taglio | un diploma, un cappello di laurea |
| `pre_departure` | una mappa topografica piegata, un tavolo con documenti | **frontiere, valigie, file, passaporti, aeroporti, porte, cancelli** — l'elenco dei soggetti vietati di `IMAGE_LICENSES.md` |

Regole comuni, non negoziabili: **nessun volto riconoscibile, nessuna persona identificabile, nessuna aula di
studenti** — questo prodotto non presenta persone, e una fotografia di persone su una pagina di formazione lo
smentirebbe; una sola sorgente di luce; croma bassa; nessun logo, nessun testo di terzi, nessun prodotto
riconoscibile (`IMAGE_LICENSES.md` §1.5); metadati rimossi (§1.6); licenza verificata **prima** del download
(§1.2); riga nel registro delle licenze (§1) **prima** della pubblicazione.

**Il glifo disegnato resta — come ripiego, non come disegno.** `.frontispiece--drawn` (arco a filetto
`--terr-line-lt`, **6,05:1** su `--min-2`, con il glifo di dominio) è ciò che si vede quando il
`MediaAsset` del dominio non esiste ancora. **Un cours pubblicato con il ripiego è un difetto di
pubblicazione, non uno stato di design**, e il §9 ne fa un test.

Il **catalogue** riceve **una** lastra `.plate--chapter` 21:9 in testa (DEROGA 2) — un laboratorio di
formazione, art-directed con le stesse regole — e **nient'altro**: le sette righe restano un registro
(ordinale mono, titolo, organisme, durata, modalità, glifo di dominio 20 px del set proprio). Sette
fotografie su una pagina di elenco sarebbero il catalogo di un e-commerce, e il regime `rich` ne ammette una.

I moduli smettono di usare `.sequence__step` (che appartiene al fascicolo giuridico) e diventano
**`.syllabus`**: `<ol>` di fogli da 64 px con ordinale mono, titolo `--t-entry`, `kind` come glifo + parola,
durata in mono tabellare. Il modulo corrente porta il filetto `--accent` 3 px e **l'unico controllo**.

```css
.course-hero { background: var(--min-1); padding-block: var(--s-12);
  border-block-end: 1px solid var(--hairline); }
.course-hero__inner { display: grid; gap: var(--s-8); grid-template-columns: minmax(0, 1fr); }
@media (min-width: 64rem) {
  .course-hero__inner { grid-template-columns: minmax(0, 7fr) minmax(0, 5fr);
    column-gap: var(--s-12); align-items: center; }
}
.course-hero__eyebrow { margin: 0; font-family: var(--f-mono); font-size: var(--t-folio);
  line-height: var(--t-folio-lh); letter-spacing: .08em; text-transform: uppercase;
  color: var(--ink-3); }
.course-hero__title { margin: var(--s-3) 0 0; font-family: var(--f-serif); font-weight: 300;
  font-size: var(--t-band); line-height: var(--t-band-lh); color: var(--ink); }
@media (min-width: 64rem) {
  .course-hero__title { font-size: var(--t-title); line-height: var(--t-title-lh); }
}
.course-hero__lead { margin: var(--s-4) 0 0; font-family: var(--f-serif); font-style: italic;
  font-size: var(--t-lead); line-height: var(--t-lead-lh); color: var(--ink-2);
  max-inline-size: 60ch; }
.course-facts { margin: var(--s-6) 0 0; padding: 0; display: flex; flex-wrap: wrap;
  gap: var(--s-3) var(--s-8); list-style: none; }
.course-facts li { display: flex; align-items: center; gap: var(--s-2);
  font-family: var(--f-mono); font-size: var(--t-folio); line-height: var(--t-folio-lh);
  font-variant-numeric: tabular-nums; color: var(--ink-2); }
.course-facts .icon { inline-size: 20px; block-size: 20px; color: var(--ink-3); }
.course-hero__action { margin: var(--s-8) 0 0; }

/* il frontespizio: la FOTOGRAFIA dentro l'arco. --drawn e il RIPIEGO (§8 rischio 9). */
.frontispiece { position: relative; inline-size: 100%; max-inline-size: 380px;
  aspect-ratio: 4 / 5; border-radius: 170px 170px 0 0; overflow: clip;
  border: 1px solid var(--terr-line-lt); justify-self: center; }  /* 6,05:1 su --min-2 */
.frontispiece img { inline-size: 100%; block-size: 100%; object-fit: cover; display: block; }
.frontispiece--drawn { background: var(--min-2); display: grid; place-items: center; }
.frontispiece--drawn .icon { inline-size: 96px; block-size: 96px;
  color: var(--terr-line-lt); opacity: .5; }
.frontispiece__credit { margin: var(--s-2) 0 0; font-family: var(--f-mono);
  font-size: var(--t-caption); line-height: var(--t-caption-lh); color: var(--ink-3); }

.syllabus { margin: 0; padding: 0; list-style: none; display: grid; gap: 4px; }
.syllabus__item { position: relative; display: grid; align-items: center;
  grid-template-columns: 40px minmax(0, 1fr) auto; column-gap: var(--s-4);
  min-block-size: 64px; padding: var(--s-3) var(--s-4);
  background: var(--min-2); border: 1px solid var(--hairline); }
.syllabus__item[data-current] { border-inline-start: 3px solid var(--accent); }
.syllabus__ordinal { font-family: var(--f-mono); font-size: var(--t-folio);
  line-height: var(--t-folio-lh); font-variant-numeric: tabular-nums; color: var(--ink-3); }
.syllabus__title { margin: 0; font-family: var(--f-serif); font-weight: 400;
  font-size: var(--t-entry); line-height: var(--t-entry-lh); color: var(--ink); }
.syllabus__kind { display: flex; align-items: center; gap: var(--s-2);
  font-size: var(--t-caption); line-height: var(--t-caption-lh); color: var(--ink-3); }
.syllabus__kind .icon { inline-size: 16px; block-size: 16px; }
.syllabus__length { font-family: var(--f-mono); font-size: var(--t-folio);
  line-height: var(--t-folio-lh); font-variant-numeric: tabular-nums; color: var(--ink-3); }
```

#### C.4 Iscrizione, attestato, supporti (`enrolment_detail.html`)

La **guida di avanzamento** (`progress_rail.html`, nuovo) è appiccicosa a destra ≥ 1200 px: misuratore in
modo `record`, «prossimo modulo» **per nome** (qui `next_module` **è** in contesto, verificato a
`views.py:194`), i due controlli, e nient'altro.

L'`.attendance` **resta un documento e non diventa mai una pastiglia**: foglio `--min-3`, filetto doppio
`--seal-600` 1 px in alto e in basso (**4,57:1** su `--min-2` — è un filetto, cioè UI, e sta sopra i 3:1;
`--seal-600` su `--seal-100` è **3,86:1** e **non si usa mai per testo**), riferimento in mono tabellare,
**la clausola integrale sotto, non ridotta**, e **nessun verde**: il verde qui direbbe «approuvé», che è
precisamente ciò che il documento nega.

I `materials` passano da `<ol class="sources">` a righe con glifo di tipo, sorgente e riferimento in mono,
righe da 48 px e bersaglio 48 px.

```css
@media (min-width: 75rem) {
  .enrolment-cols { display: grid; grid-template-columns: minmax(0, 1fr) 320px;
    column-gap: var(--s-12); align-items: start; }
  .progress-rail { position: sticky;
    inset-block-start: calc(var(--chrome-height) + var(--s-6)); }
}
.progress-rail { display: grid; gap: var(--s-4); padding: var(--s-6);
  background: var(--min-2); border: 1px solid var(--hairline); }
.progress-rail__next { margin: 0; font-family: var(--f-serif); font-weight: 400;
  font-size: var(--t-entry); line-height: var(--t-entry-lh); color: var(--ink); }
.progress-rail__actions { display: flex; flex-wrap: wrap; gap: var(--s-3); }

/* L'ATTESTATO E UN DOCUMENTO. Nessun verde, nessuna pastiglia, clausola integrale. */
.attendance { background: var(--min-3); border: 1px solid var(--hairline);
  border-block: 1px solid var(--seal-600); padding: var(--s-8) var(--s-6); }  /* 4,57:1 */
.attendance__ref { font-family: var(--f-mono); font-size: var(--t-folio);
  line-height: var(--t-folio-lh); font-variant-numeric: tabular-nums; color: var(--ink-2); }
.attendance__clause { margin: var(--s-4) 0 0; font-size: var(--t-body);
  line-height: var(--t-body-lh); color: var(--ink); max-inline-size: 65ch; }

.materials { margin: 0; padding: 0; list-style: none; display: grid; gap: 0; }
.materials li { display: grid; grid-template-columns: 24px minmax(0, 1fr) auto;
  align-items: center; column-gap: var(--s-3); min-block-size: 48px;
  border-block-end: 1px solid var(--hairline); font-size: var(--t-ui);
  line-height: var(--t-ui-lh); }
.materials .icon { inline-size: 20px; block-size: 20px; color: var(--ink-3); }
.materials__ref { font-family: var(--f-mono); font-size: var(--t-caption);
  line-height: var(--t-caption-lh); font-variant-numeric: tabular-nums; color: var(--ink-3); }

@media (prefers-reduced-motion: no-preference) {
  /* NESSUNA transizione di box-shadow, come sopra. Si anima solo il fondo. */
  .resume, .enrolment { transition: background-color var(--motion-fast) var(--ease-out); }
  .syllabus__item { transition: border-inline-start-color var(--motion-base) var(--ease-standard); }
}
@media (forced-colors: active) {
  .frontispiece { border-color: CanvasText; }
  .syllabus__item[data-current] { border-inline-start-color: Highlight; }
}
```

### 4.D `scripts/territory.py` — il contratto d'uscita (lacuna 9, MUST-FIX 12)

Il generatore **esiste già** e la sua convenzione è già quella giusta: emette **markup interno** (senza
radice `<svg>`: il template fornisce `viewBox` e gli attributi d'accessibilità), con **classi** e **nessuno
stile** — verificato: la stringa `style` non compare nel file, e ogni tratto è deciso in CSS
(`static/css/v2/hero.css:39-75`). Aggiungo **due chiamate**, con lo stesso `build()` e lo stesso seme fisso:

| Chiamata | `viewBox` | File emessi | Dove atterrano | Tetto |
|---|---|---|---|---|
| cartiglio impresa | `0 0 280 160` | `territory_cartouche_base.svg` | `templates/companies/partials/` | **≤ 4 KB** |
| relazione Forum | `0 0 1200 520` | `territory_relation_base.svg`, `…_layer-1.svg` | `templates/forum/partials/` | **≤ 22 KB** in tutto |
| *(esistenti, invariati)* | `0 0 1440 820` / `0 0 1440 260` | `territory_hero_*`, `territory_band_*` | come oggi | ≤ 43 KB per pagina IMMERSIVE |

Classi emesse, e **solo** queste: `terr__grid` (`<line>`), `terr__ticks` (`<path>`), `terr__route`
(`<path pathLength="1">`), `terr__stations` / `terr__station` / `terr__halo` / `terr__dot`,
`terr__layer terr__layer--N`, più, per le due chiamate nuove, `terr__mark` (le due tacche del cartiglio),
`terr__node` / `terr__node--seal` (i sei nodi della relazione) e `terr__label` (`<text>`).
Nessun `stroke-width`, nessun `fill`, nessun `stroke` sono emessi dal generatore: **stanno tutti in
`v3/workbench.css` e `v3/forum.css`**, dove il §4.A.1 e il §4.B.2 li scrivono.

> **LA REGOLA CSP, che il §8 del round 1 non aveva** (MUST-FIX 12). `scripts/territory.py` **non deve mai**
> emettere un elemento `<style>` né un attributo `style=""`, e nemmeno un `<script>`: la CSP è
> `style-src 'self'` e `script-src 'self'`, e questi SVG sono **inline nel documento**, quindi un solo
> `style=""` rompe la pagina intera, non solo il disegno. Il test del §9 lo asserisce sui **cinque** file
> generati, non solo sui due nuovi. Che il vincolo sia in vigore è provato in pagina questo round: un
> `<style>` iniettato non applica.

Riproducibilità: seme fisso, mai `Math.random`, mai `random`. **Se il rieseguito non è identico byte per byte
al committato, non entra.** I file sono committati (sono include Django, non artefatti di build), e il test
li rigenera in una directory temporanea e confronta.

### 4.E DOVE SI CARICA TUTTO — e quali regole muoiono (MUST-FIX 9, lacune 7 e 8)

Il round 1 diceva «caricati in `templates/base.html` dopo `css/v2/voyage.css` (riga 38)». **La riga 38 di
`base.html` è un `<link rel="preload">`**, e la cascata è costruita dagli `@import` di
`static/css/main.css`. Peggio: i tre fogli d'app sono `<link>` in `{% block extra_head %}`, cioè **dopo**
`main.css`, quindi vincono a parità di specificità su qualunque cosa `main.css` faccia. **Provato in pagina
questo round** (§0-ter MUST-FIX 9).

**Il piano corretto**, in tre righe:

1. **Il pezzo condiviso va nel bundle**, in coda a `static/css/main.css`, **dopo** `v3/buttons.css` — che è
   esattamente il posto in cui `buttons.md` ha già messo il proprio file:
   ```css
   @import url("v3/buttons.css");
   @import url("v3/meter.css");     /* NUOVO — il solo pezzo condiviso dalle tre superfici */
   ```
   e il `<link rel="preload" href="{% static 'css/v3/meter.css' %}" as="style">` accanto agli altri in
   `base.html`.
2. **I tre fogli di superficie vanno nel blocco d'app, DOPO il foglio legacy che correggono**, perché è
   l'unico punto della cascata che li lascia vincere:
   | File | Dove | Riga |
   |---|---|---|
   | `v3/workbench.css` | `templates/companies/base_companies.html` `{% block extra_head %}` | dopo `companies/companies.css` (riga 20) |
   | `v3/forum.css` | `templates/forum/index.html` **e** `templates/forum/governance/base_governance.html` | dopo `forum/forum.css` (`index.html:6`) |
   | `v3/academy.css` | `templates/academy/base_academy.html` `{% block extra_head %}` | dopo `academy/academy.css` (riga 17) |
3. **I bundle JS** vanno in `{% block extra_scripts %}` (`templates/base.html:70`, dopo
   `js/dist/shell.js`), uno per base d'app:
   `base_companies.html` → `<script type="module" src="{% static 'js/dist/workbench.js' %}"></script>` ·
   `forum/index.html` → `forum.js` · `base_academy.html` → `academy.js`.

**E queste regole si cancellano** — nominate, non «si riducono» (lacuna 14):

| File | Regole da cancellare | Perché | Misura |
|---|---|---|---|
| `apps/companies/static/companies/companies.css` | `.company-header`, `.company-header__inner`, `__folio`, `__name`, `__facts`, `__fact dt`, `__fact dd`, `__note`, e le due `@media (min-width: 48rem)` che le accompagnano; `.entry__responsible` | sostituite da `.company-standard` e da `.need__owner` | **11 regole di primo livello su 30, ≈ 1 320 B di 6 065 (22 %)** |
| `apps/forum/static/forum/forum.css` | tutto `.forum-hero*`, `.forum-localnav*`, `.forum-programme*`, `.forum-speakers*`, `.forum-cta*` (**in particolare la riga 144**, `.forum-cta .btn--secondary`), `.forum-cards`/`.forum-card*`, `.forum-section__title`, e `.btn.is-disabled` (riga 145, che `buttons.md` §1.7 convince già di violare il §10) | sostituite dal §4.B | **49 regole su 88, ≈ 6 010 B di 11 712 (51 %)** |
| `apps/academy/static/academy/academy.css` | `.attendance`, `.attendance__head`, `__reference`, `__facts`, e `.entry__gloss .t-caption` | sostituite dal §4.C.4 | **6 regole su 16, ≈ 751 B di 4 718 (16 %)** |

Restano dove sono: `.academy-filters*` (il catalogo ha i suoi filtri e funzionano), `.module-form`,
`.academy-inline`, `.companies-inline-form*`, `.companies-withdraw*`, `.companies-form`, `.need-actors*`
(**il blocco Responsable non si tocca**, lacuna 13), `.forum-form*`, `.forum-gallery*`, `.forum-documents*`.

---

## 5. MOTION — voci per `MOTION_SYSTEM.md` §6

Nessuna nuova durata, nessuna nuova curva, nessun overshoot, nessuna molla con `damping` < 25.
**Un solo oggetto vivo per pagina**; sulle superfici DENSE e RICH **nessun loop e nessun oggetto legato allo
scroll** (§4 del documento di moto: «Le pagine RICH ne hanno al massimo uno dei due; STANDARD, DENSE e LEGAL
nessuno»). Ogni voce dichiara la sua funzione fra le sette e il suo gemello ridotto.

| Nome | Funzione | Innesco | Durata / curva | Proprietà | Stato ridotto | Budget |
|---|---|---|---|---|---|---|
| `meter-node-set` | STATO | `inView` una volta sul registro | `--motion-base` 240 ms, stagger **40 ms per nodo** | `transform: scale(0→1)` su `.meter__tick::after` | nodi già a `scale(1)`, nessuna transizione | solo `transform`; ≤ 8 elementi; 0 layout/paint |
| `need-row-mark` | FEEDBACK | hover/focus su `.need` (`hover: hover`) | `--motion-fast` in / `--motion-instant` out, `--ease-out` / `--ease-in` | `background-color` della riga, `translateX(2px)` sulla freccia | identico, istantaneo | nessuna ombra animata; `--shadow-2` appare senza transizione |
| `workflow-step` | CAUSALITÀ | `inView` al primo frame dopo il POST (la pagina si ricarica) | `--motion-base`, `--ease-standard` | `transform: scaleX(0→1)` sul **solo** segmento `aria-current` | segmento già pieno | 1 segmento |
| `workbench-enter` | GERARCHIA | `inView` una volta, **per regione** non per riga | `--motion-base`, stagger 60 ms, `--ease-out` | `opacity 0→1`, `translateY 12→0` | tutto al valore finale | ≤ 4 regioni (tetto della query 4) |
| `forum-arch-draw` | DELIZIA + ORIENTAMENTO | ingresso nella pagina, **una volta** | **`--motion-draw` 900 ms** (il token che esiste), `--ease-out` | `stroke-dashoffset` sull'arco dell'hero, poi i gradini a stagger 100 ms | arco e gradini completi e fermi dal primo frame | 1 path |
| `forum-relation-route` | ORIENTAMENTO | posizione di scroll (`animation-timeline: view()`, orchestrazione Motion) | legata, non temporale | `stroke-dashoffset` dell'arco; i sei nodi passano da filetto a pieno alla loro quota | rotta intera, nodi pieni, valore finale fisso | **l'unico oggetto legato allo scroll del sito, e sta sull'unica pagina IMMERSIVE** |
| `localnav-indicator` | ORIENTAMENTO | `IntersectionObserver` sulle sezioni | `SPRING_FOLLOW` (400/40, senza rimbalzo) | `translateX` + `scaleX` del filetto attivo | il filetto salta senza transizione | 1 elemento |
| `forum-tide` | DELIZIA | ingresso nel viewport dell'hero | `--motion-ambient` **28 s**, lineare, in pausa fuori schermo | `transform: translate3d()` su **due** strati di graticola, ampiezza ≤ 8 px | fermo | **l'unico loop del sito**; controllo «Suspendre le mouvement» obbligatorio |
| `academy-resume` | ORIENTAMENTO | `inView` una volta sulla riga di ripresa | `--motion-base`, `--ease-out` | `opacity` + `translateY 12→0` | già a posto | 1 elemento |
| `syllabus-advance` | CAUSALITÀ | ricarica dopo «J'ai suivi ce module» | `--motion-base`, `--ease-standard` + `SPRING_SETTLE` sull'altezza misurata | il nodo si stampa, il filetto `--accent` scende al modulo successivo (`transform`), l'altezza si riassesta | nodo pieno, filetto già spostato, salto d'altezza immediato | annuncio `aria-live="polite"`: «Module 3 sur 5 suivi» |

**Il tracciato da 600 ms del round 1 non esiste più** (violazione 6). L'unico tracciato immersivo è
`--motion-draw` **900 ms** (`static/css/v2/tokens.css:111`), e il glifo del frontespizio **non si traccia
affatto**: con la DEROGA 2 il frontespizio è una fotografia, e una fotografia non si disegna.

**Il conteggio degli oggetti vivi, per pagina** (§4 del documento di moto):
Forum pubblico (IMMERSIVE) → **1 loop** (`forum-tide`) **+ 1 solo oggetto legato allo scroll**. E qui c'è
l'unica cosa che ho dovuto tagliare rispetto al round 1, che ne prescriveva due: `forum-relation-route` **e**
`agenda-spine` sarebbero due oggetti indicizzati allo scroll sulla stessa pagina, e il §4 del documento di
moto ne ammette **uno**. Resta `forum-relation-route`, che è la firma della pagina; **`agenda-spine` è
cancellato** e la dorsale dell'agenda si disegna completa e ferma, ricevendo il nodo pieno/vuoto per voce con
orario che oggi non ha. Cruscotto, besoins, `need_detail`, Academy, governance → **0 loop, 0 oggetti legati
allo scroll**.
Ogni `transition` e ogni `@keyframes` dei quattro fogli sta dentro
`@media (prefers-reduced-motion: no-preference)`: verificabile con un `grep`, ed è il §9.

---

## 6. ACCESSIBILITÀ E RTL

**Cosa cambia.**

**(a)** `aria-hidden="true"` sta su **`.meter__track` e su nient'altro**. La frase del round 1 («Il
misuratore è `aria-hidden="true"`») era falsa e contraddiceva il markup del §4.0: è **cancellata**. La
`.meter__word` è **contenuto**, non è mai `visually-hidden`, ed è prodotta da **una sola** catena `{% if %}`,
dentro il partial (il parametro `label` non esiste più: era la seconda sorgente che la revisione ha trovato).

**(b)** La barra di lavorazione è un `<ol>` con `aria-current="step"` sul segmento corrente — e, per
`on_hold` e `withdrawn`, **sulla tappa tenuta**, mai su nessuna. L'`<ol>` porta `aria-describedby` verso la
`.workflow-note`, che dice la condizione in parole. Una legenda testuale delle cinque tappe è presente.
Oggi `.sequence__step` non porta `aria-current` da nessuna parte.

**(c)** Lo stato non è mai solo colore. Sul registro dei besoins i canali sono **cinque**: la parola della
pastiglia, la parola del misuratore, il glifo del responsabile, la trama del filo, e **la posizione del nodo
sulla riga graduata** — che è il canale nuovo, ed è quello che risponde al §1.2.

**(d)** La `.forum-localnav` riceve `aria-current="true"` sulla voce corrente, non solo un filetto.

**(e)** L'alternativa testuale della grafica relazionale è **contenuto visibile**, non testo nascosto, e
sotto 720 px è l'**unica** resa.

**(f) Bersagli: 48 px** su ogni controllo con cornice delle tre superfici, **44 px** su `.btn--icon` — cioè
`DESIGN_SYSTEM_V2` §10 e `buttons.md` §8, alla lettera. Il round 1 scriveva 44 dopo aver convinto la build di
ignorare i 48: era incoerente e la revisione ha ragione. L'intera riga del registro è il bersaglio (misurata:
**74 px** di altezza); le voci della navigazione locale misurano **50,19 px** (misurate).

**(g)** `aria-live="polite"` sul completamento di un modulo e sulla transizione di un besoin.

**(h)** Skeleton di livello 1 con `aria-busy`, mai uno spinner nudo (§9.6).

**Contrasti, tutti ricalcolati questo round** (luminanza relativa WCAG 2.x, composizione alfa eseguita, non
stimata). Le tre righe che la revisione ha convinto sono in alto, con il loro rimedio.

| Coppia | Su | Rapporto | Uso | Esito |
|---|---|---|---|---|
| ~~`--accent` #0F6A72~~ | `--mid-2` | **2,52** | pieno della CTA primaria | **RIMOSSO** |
| `--accent-dark` #7FD1D8 | `--mid-2` | **9,09** | pieno della CTA primaria | ✔ |
| `--mid-1` | `--accent-dark` | **10,01** | etichetta di quel pieno | ✔ |
| ~~`--hairline-dark-strong` .28~~ | `--mid-2` → #4A5961 | **2,19** | confine dei secondari | **RIMOSSO** (su `--mid-1` → #465359 = **2,20**) |
| `--on-dark-2` #B7C3C4 | `--mid-2` | **8,79** | confine dei secondari (ed è ciò che la build già rende) | ✔ |
| ~~`--mid-4` #223A46~~ | `--mid-2` | **1,33** | il pieno proposto in revisione | **RESPINTO** (§0-quater) |
| ~~`--ink-2` #4A5A62~~ | `--mid-1` | **2,44** | nodo del misuratore su mezzanotte | **RIMOSSO** |
| `--terr-line` #3FA6AF | `--mid-1` / `--mid-2` | **6,07 / 5,51** | nodo del misuratore su mezzanotte | ✔ |
| `--on-dark-3` #8FA0A3 | `--mid-1` / `--mid-2` | **6,44 / 5,85** | filetto e graduazione su mezzanotte | ✔ |
| `--ink-2` | `--min-2` / `--min-0` / `--min-1` | **6,87 / 6,46 / 6,00** | nodo del misuratore su carta | ✔ |
| `--hairline-strong` #7A868B | `--min-2` / `--min-0` / `--min-1` | **3,59 / 3,37 / 3,14** | filetto e graduazione su carta, bordo del foglio | ✔ (UI ≥ 3) |
| `--accent-ring` #1D8A93 | `--min-0` / `--min-2` | **3,70 / 3,94** | anello «vous êtes ici» | ✔ |
| `--owner-person` #0F6A72 | `--min-2` | **6,05** | trama «professionnel mandaté» | ✔ |
| `--owner-project` #34506A | `--min-2` | **8,05** | trama «équipe du projet» | ✔ |
| `--owner-training` #1C5F7C | `--min-2` | **6,76** | trama «organisme de formation» | ✔ |
| `--owner-authority` #8C6D4B | `--min-2` | **4,57** | trama «acteur autorisé» (la peggiore delle cinque) | ✔ |
| `--ink-3` #55646B | `--min-2` / `--min-0` | **5,88 / 5,53** | «aucun intervenant désigné», didascalie | ✔ |
| `--seal-300` #C7A77E | `--mid-1` | **7,72** | anello del sigillo di verifica | ✔ |
| `--seal-600` #8C6D4B | `--min-2` | **4,57** | filetto dell'attestato (UI) | ✔ |
| `--seal-600` | `--seal-100` | **3,86** | **mai per testo** — dichiarato | ⚠ |
| `--on-dark` #EEF2F1 | `--mid-2` / `--mid-1` | **14,08 / 15,51** | testo su scuro | ✔ |
| `--terr-line` **al 34 %** | `--mid-1` → #1F4A53 | **1,80** | graticola del cartiglio | **decorazione, `aria-hidden`, 1.4.11 non si applica** — dichiarato |
| `--terr-line` **al 18 %** | `--mid-1` → #17343C | **1,33** | graticola dell'hero | idem |

**Nessun colore nuovo viene introdotto su queste tre superfici.** La differenziazione passa da forma,
posizione, trama e parola.

**RTL.** Solo proprietà logiche. Si specchiano: la direzione della dorsale dell'agenda, il senso di
riempimento della riga graduata (che è automatico: `display: flex` in `dir="rtl"` inverte l'ordine visivo e
`:nth-child()` continua a contare in ordine di lettura), il filo di rilegatura (`inset-inline-start`), la
freccia del registro, l'arco della grafica relazionale (`scaleX(-1)` sul solo gruppo decorativo), l'origine
del filetto attivo della navigazione locale. **Non** si specchiano: le etichette mono dei nodi
(`text-anchor` scambiato, non specchiato), i numeri, i riferimenti di besoin e d'attestato, il lock-up, il
glifo del sigillo.
**Misurato in `ar` a 1440×900**: righe del registro **1240 × 77-78 px**, griglia
`40px · 789,27px · 64,73px · 216px · 24px`, insegna **233 px**, **`scrollWidth === clientWidth`** (nessuno
scorrimento orizzontale).
`:lang(ar)`: `letter-spacing: 0` su folio, eyebrow, parole di stato e ordinali; `text-transform: none`;
interlinea 1,8 nel corpo; `min-inline-size: 120px` sui bottoni.
`forced-colors: active`: le trame restano (`forced-color-adjust: none` **solo** sul filo di rilegatura, sulla
barra di lavorazione e sul nodo del misuratore), le isoipse passano a `GrayText`, il focus usa l'`outline` di
sistema, i filetti e le graduazioni passano a `CanvasText`, i nodi aperti (`on_hold`, «aucun intervenant»)
tornano a `forced-color-adjust: auto` perché **devono** distinguersi dai pieni.

**HUMAN_QA_REQUIRED.** (1) I testi bloccati d'evento del Forum non sono tradotti in IT/EN/AR: i bottoni della
fascia CTA restano in francese su `/ar/forum/` (misurato). Non è risolvibile in CSS. (2) Le **sette**
fotografie dell'Academy e la fotografia dell'hero del Forum vanno verificate per art direction contro la
tabella del §4.C.3 e contro `IMAGE_LICENSES.md` — **mai un'immagine di cronaca migratoria**, mai un volto
riconoscibile. (3) Ogni logo partner passa dal gate G6 e non va mai alterato. (4) Il testo alternativo del
cartiglio, della grafica relazionale e delle sette fotografie va riletto contro `apps/cms/forbidden.py`: la
formulazione vietata non deve comparire nemmeno in `alt`, `aria-label`, `title` o testo per lo screen reader.
(5) La parola di stato del misuratore in AR va riletta da un madrelingua: «Étape 3 sur 5» in arabo con
numerali occidentali è una scelta da confermare. (6) «Position tenue à l'étape N sur 5» e «Ce besoin a été
clos sans avoir été pris en charge» sono **affermazioni giuridiche su un dossier d'impresa**: vanno approvate
dal responsabile del prodotto prima di andare in pagina.

---

## 7. PRESTAZIONI — pesate, non stimate

Il round 1 scriveva «~2,4 KB», «~5,4 KB». La revisione ha ragione: erano stime travestite da misure. Questi
sono i **fogli del §4**, scritti per intero, pesati con `gzip -9`.

| Artefatto | Grezzo | Gzip | Dove si carica |
|---|---:|---:|---|
| `v3/meter.css` | **11 094 B** | **3 043 B** | `@import` in `main.css` (tutte le pagine) |
| `v3/workbench.css` | **15 687 B** | **3 488 B** | `base_companies.html`, dopo `companies.css` |
| `v3/forum.css` | **12 217 B** | **2 978 B** | `forum/index.html` e `base_governance.html`, dopo `forum.css` |
| `v3/academy.css` | **9 338 B** | **2 178 B** | `base_academy.html`, dopo `academy.css` |
| **totale** | **48 336 B** | **11 687 B** | — |
| `workbench.js`, `academy.js` | ~2 KB ciascuno | ~0,9 KB | **chunk Motion già scaricato** da `shell.js` |
| `forum.js` | ~3 KB | ~1,2 KB | rotta legata allo scroll + marea + spia di navigazione |
| chunk Motion condiviso | **70 441 B** | **26 143 B** | `js/dist/chunk-*.js`, servito una volta, in cache |
| SVG cartiglio impresa | ≤ 4 KB | inline | build time, seme fisso |
| SVG relazione Forum | ≤ 22 KB | inline | build time; le isoipse dell'hero restano sotto i 43 KB del §6 |
| fotografia hero Forum · frontespizio corso · lastra catalogo | — | — | AVIF/WebP, `srcset` 480/800/1200, **≤ 120 KB per viewport**, `fetchpriority="high"` sul poster |

**Bilancio CSS per pagina, al netto delle cancellazioni del §4.E:**

| Pagina | CSS aggiunto (gz) | CSS tolto (grezzo) |
|---|---:|---:|
| cruscotto impresa, besoins, besoin | 3 043 + 3 488 = **6 531 B** | −1 320 B da `companies.css` |
| Forum pubblico e governance | 3 043 + 2 978 = **6 021 B** | −6 010 B da `forum.css` |
| Academy (cinque pagine) | 3 043 + 2 178 = **5 221 B** | −751 B da `academy.css` |

Il JS resta **largamente** dentro i 45 KB gz per pagina: il chunk Motion (26 143 B) è già scaricato dalla
shell su ogni pagina del sito e non si moltiplica; ciascuna delle tre superfici aggiunge ≤ 1,2 KB gz.

**Costo in paint/layout.** Tutte le animazioni del §5 muovono `transform` e `opacity`, più
`stroke-dashoffset` sui tre SVG (composito, non layout). **Nessun `filter` in loop, nessuna `box-shadow`
animata, nessun `width`/`height`/`top`/`left`.** `grep "box-shadow"` sui quattro fogli, commenti esclusi:
**meter 0 · workbench 1 · forum 1 · academy 2**, quattro occorrenze in tutto, e sono **tutte**
`box-shadow: var(--shadow-2)` su `:hover` dentro `@media (hover: hover)` — il ruolo 2 nel solo stato che il
§2 gli concede. **Nessuna delle quattro è transitata**: `grep "transition: box-shadow"` → **0**. Il round 1
ne aveva due (`.resume`, `.forum-cards > a`) e sarebbero state un'animazione di `box-shadow`, cioè un
vincolo di prestazione violato; l'ombra ora **compare**, non si anima, e si anima solo il fondo.
`grep -c "cubic-bezier"`: **0 su tutti e quattro** (le curve sono i tre token). Misurato sul candidato:
`box-shadow` distinti **a riposo** su registro e insegna = **`[]`**, nessuno.

**Il `backdrop-filter` è sparito**, e con lui la contraddizione che la revisione ha trovato fra il segnale 4 e
questa sezione: un elemento appiccicoso **opaco** su un layer di compositore non ridipinge per frame.

**Collaudo d'accettazione**: pannello Performance di Chrome durante l'esecuzione, **0 layout e 0 paint oltre
il primo frame**, INP < 200 ms, CPU rallentata 4×, e
`document.getAnimations().filter(a => a.timeline instanceof ViewTimeline)` deve avere **lunghezza 1** sul
Forum (`forum-relation-route`) ed **essere vuoto** su cruscotto, besoins, `need_detail`, Academy e governance.

---

## 8. RISCHI

| # | Come questo diventa economico | La guardia |
|---|---|---|
| 1 | **Il misuratore diventa una barra di avanzamento.** Basta che qualcuno aggiunga «60 %» accanto, o renda il nodo riempibile a metà | Il nodo è stampato o non stampato, mai frazionario: nessuna `width`/`inline-size` percentuale in `meter.css` (un test le conta: **0**). Oltre 8 posizioni la pista sparisce e resta la cifra. La parola con il conteggio esatto è **obbligatoria** e non è mai `visually-hidden`. **E in modo `record` non può diventarlo per costruzione**: le regole sono per tappa, non `:nth-child(-n+N)` |
| 2 | **Il misuratore dice una cosa falsa su un dossier.** È il difetto che la revisione ha trovato, ed è il più grave dei due | Il riempimento viene **solo** da `NeedEvent`. Un test costruisce un besoin `DRAFT → SUBMITTED → UNDER_REVIEW → CLOSED` e asserisce che la tacca `in_progress` resta vuota e che la frase «clos sans avoir été pris en charge» è in pagina |
| 3 | **La grafica relazionale diventa un mappamondo puntinato** | Nessun contorno nazionale, nessuna bandiera, nessun pianeta: due frammenti di graticola e un arco. Nessun nodo pulsa. Seme fisso: se non è riproducibile byte per byte, non entra |
| 4 | **Il cruscotto si riempie di tasselli vuoti** | Regola dura: **una regione senza dato non si disegna**, e **una pagina disegna al massimo una striscia vuota**. Nessun KPI inventato, nessun conteggio di persone |
| 5 | **Il capitolo mezzanotte si moltiplica** | Uno per pagina fuori da HOME e FORUM, due sul Forum (hero + relazione), **zero** sull'Academy, e la fascia CTA passa a `--mid-2`: è un'area, non un capitolo. Un test conta i `.chapter--dark` per template |
| 6 | **Il sigillo bronzo diventa decorazione** | Bronzo **solo** su: verifica d'impresa, anello dell'attore autorizzato, filetto dell'attestato. Mai testo (3,86:1 sul proprio fondo chiaro), mai fondo, mai accento |
| 7 | **Il Forum diventa un sito d'evento** | Nessun countdown; nessun carosello di loghi; **nessuna riga di loghi quando la lista è vuota**; nessuna fotografia stock — la fotografia dell'hero passa dalla direzione artistica del §4.C.3 e da `IMAGE_LICENSES.md` |
| 8 | **La trama del responsabile diventa illeggibile** | Passo minimo **4 px**, tratto **1,5 px**, contrasto ≥ 3:1 sul proprio fondo (peggiore: 4,57), la trama **solo** su 3 px di filo e 10 px di barra e **mai** su una superficie più larga, `forced-color-adjust: none` solo lì, e **la parola del responsabile sempre accanto**: se la trama sparisce, l'informazione resta |
| 9 | **Il frontespizio disegnato torna a essere il disegno.** È esattamente ciò che è successo nel round 1 | `.frontispiece--drawn` è un **ripiego**. Un test elenca i `Course` con `status == PUBLISHED` il cui `course_type` non ha un `MediaAsset` curato e **fallisce**: un corso pubblicato senza fotografia è un difetto di pubblicazione |
| 10 | **L'Academy prende il disegno del fascicolo giuridico** | `.syllabus` è una classe distinta con un ritmo distinto. Un corso non è una procedura: la clausola dell'attestato resta integrale, e nessun verde compare su quella pagina |
| 11 | **Qualcuno fonde il quinto registro dell'Academy nel quarto** | Regola dura scritta al §4.C.1 e un test che asserisce due `<section>` distinte con due `aria-labelledby` distinti, e la frase del mandato presente su ogni riga |
| 12 | **Un `style=""` entra da `scripts/territory.py`** | Regola scritta al §4.D e un test che la asserisce sui cinque file generati. Con `style-src 'self'` un solo attributo rompe la pagina intera |

---

## 9. COLLAUDO — i test che questa spec chiede

| Test | Asserisce |
|---|---|
| `test_v3_modes.py` | ogni template delle tre superfici dichiara `data-mode`; i valori sono quelli della tabella §4.A.0; `.chapter--dark` per pagina ≤ 1 (cruscotto, besoins), = 2 (Forum), = 0 (`need_detail`, i due form, `profile`, l'Academy, la governance) |
| `test_v3_meter.py` | in `meter.css`: `%` su `width`/`inline-size` = **0**; `box-shadow` = **0**; `cubic-bezier` = **0**; ogni `transition` è dentro `@media (prefers-reduced-motion: no-preference)`; `aria-hidden` compare nel partial **una sola volta** e su `.meter__track` |
| `test_v3_shadows.py` | sui quattro fogli: ogni `box-shadow` è `var(--shadow-2)` e sta dentro `@media (hover: hover)` su uno stato `:hover`; `transition: box-shadow` = **0**; `cubic-bezier` = **0**; nessun `@keyframes` e nessuna `transition` fuori da `@media (prefers-reduced-motion: no-preference)` |
| `test_v3_need_record.py` | un besoin `DRAFT → SUBMITTED → UNDER_REVIEW → CLOSED` rende `data-passed="draft submitted under_review closed "`, `data-now="closed"`, e **nessun** nodo su `in_progress`; un besoin `ON_HOLD` rende `data-condition="on_hold"` e `data-now` = la tappa tenuta; `aria-current="step"` compare **una sola volta** per barra |
| `test_v3_owner_weave.py` | ogni valore di `ActorRole` ha una regola `[data-owner~="…"]` in `meter.css`; il caso vuoto ha la sua; nessun valore è senza trama **e senza parola** |
| `test_v3_cascade.py` | `v3/workbench.css`, `v3/forum.css`, `v3/academy.css` compaiono nel `extra_head` **dopo** il rispettivo foglio d'app; le regole elencate al §4.E **non** esistono più nei tre fogli legacy |
| `test_v3_focus.py` | `grep "focus-visible"` sui quattro fogli = **0** (il focus è della shell) |
| `test_territory_csp.py` | i cinque file generati da `scripts/territory.py` non contengono `<style`, `style=`, `<script`; rigenerati in `tmp_path` sono **byte-identici** ai committati |
| `test_v3_speaker_gate.py` | `partials/speakers.html` itera `speakers` e **non** `event.speaker_roles`; con il flag di sito spento nessun `person_name` è in pagina |
| `test_v3_academy_registers.py` | `mine.html` rende **cinque** `<section>` con cinque `aria-labelledby`; la frase del mandato è su ogni riga del quinto; le due didascalie giuridiche sono in pagina **verbatim** |
| `test_v3_course_image.py` | nessun `Course` con `status == PUBLISHED` rende `.frontispiece--drawn`; ogni `MediaAsset` di dominio ha una riga in `IMAGE_LICENSES.md` |
| `test_v3_targets.py` | ogni controllo con cornice delle tre superfici misura ≥ 48 px; `.btn--icon` ≥ 44; l'intera riga del registro è il bersaglio |
| `test_v3_forbidden.py` | `apps.cms.forbidden.scan()` su ogni rotta pubblica delle tre superfici, in `fr`/`it`/`en`/`ar`, **compresi** `alt`, `aria-label`, `title` e il testo per lo screen reader = **0 violazioni** |
| `tests/i18n/test_rtl_browser.py` (esteso) | in `ar` a 1440 e a 390: `scrollWidth === clientWidth`; il filo di rilegatura è a `inset-inline-start`; il nodo corrente della riga graduata è dal lato di lettura |
