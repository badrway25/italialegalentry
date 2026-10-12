# DESIGN V3 — SPEC DI SUPERFICIE: `person-dashboard`

Specialista Dashboard UX + Legal-Tech UX · 24 settembre 2026 · **ROUND 2 — RIPARAZIONE**
Superficie `/fr/espace-reserve/` (ruolo PERSONNE) · `templates/portal/dashboard.html` + `base_portal.html` + `base.html`
Vincolanti: `DESIGN_SYSTEM_V2.md`, `MOTION_SYSTEM.md`, `BRAND_ASSETS.md` §1, `apps/cms/forbidden.py`.

**Riproduzione delle misure di questo round.** Server `runserver 127.0.0.1:8770` (DB `ile`); sessione server-side
per `qa-person@example.test` (fascicolo `E12273C5DF`, 9 voci di checklist); Chromium 153.0.8010.12 di Playwright
dal `.venv`, **headless**, `device_scale_factor=1`, viewport 1440×900 · 1280×900 · 768×1024 · 390×844.
Il prototipo è servito **sulla stessa origine** del sito (rotte intercettate: `…/fr/__proto__/` e
`…/static/css/v3/proto.css`), quindi carica i font reali e vive sotto la CSP reale
(`style-src 'self'`; nessuno `<style>` in linea è stato usato). Script in
`…/scratchpad/pd/{contrast.py, before.py, page.py, proto.css, verify.py, territory_plate_base.svg}`;
immagini `before_*.png`, `page_*.png`, `fold_*.png`, `shot_plate.png`, `shot_bars.png`.
Nessun file del repository è stato modificato oltre questa spec.

---

## 0. RICHIESTE DI DEROGA (AMENDMENT REQUESTS)

Sei, numerate. Ognuna nomina la clausola, la ragione **misurata** e il costo. Tutto ciò che non è qui è
conforme senza deroga.

**A1 — Quattro token semantici per il capitolo mezzanotte.** *Clausola:* DS §1.1 (la tavolozza è quell'elenco).
*Richiesta:* aggiungere `--ok-dark #29A86A`, `--err-dark #E6706A`, `--pending-dark #B58D5F`, `--seal-dark #AF8E69`.
*Ragione (ricalcolata):* i semantici chiari su `--mid-2 #14242E` danno `--ok-700` **2,99** · `--err-700` **2,43** ·
`--pending-700` **2,28** · `--seal-600` **3,33** · `--ok-800` **2,44** · `--seal-700` **2,11** — tutti sotto 4,5:1,
cioè la parola di stato nella plancia sarebbe illeggibile. I quattro nuovi sono risolti per superare **4,55:1 sul
foglio scuro `--mid-3`**, il che dà 5,21–5,25 su `--mid-2` e 5,74–5,78 su `--mid-1`.
*Precedente nel sistema:* è lo stesso schema a due luminosità già scritto in DS §1.3.1 per `--accent` / `--accent-dark`.
*Costo:* 4 token, **+180 byte** in `v3/tokens-v3.css`, una riga di test per rapporto in
`tests/frontend/test_css_tokens_exist.py` (il commento di `v2/tokens.css` L11 rimanda a
`tests/frontend/test_v2_tokens.py`, che **non esiste**: il file reale è quello — segnalato, fuori da questa spec).
*Non chiedo* una rampa `--owner-*-dark`: vedi §4.4, il rail sta sulla carta e usa i cinque token esistenti.

**A2 — La marca di stato ha raggio 0, non 999.** *Clausola:* DS §2, «Raggi: … 999 sulle pillole di stato. Nessun altro.»
*Richiesta:* l'oggetto di stato di questa superficie non è una pillola: è un rettangolo a raggio **0** con filetto
`border-inline-start` 2 px. *Ragione:* il revisore ha ragione sul fatto che una pillola tinta con glifo a 14 px è
la Badge di una libreria con i nostri esadecimali dentro, e che il filetto 2 px `currentcolor` di `.state` è il solo
segno d'archivio che il prodotto possiede già (§1.3). Il raggio 0 è comunque **dentro** l'insieme enumerato dalla
clausola; cambia l'assegnazione, non l'insieme. *Costo:* le pillole di stato spariscono da questa superficie; le
altre 14 superfici che usano `.state` restano invariate finché `badges.md` non atterra, quindi per un periodo il
prodotto ha due oggetti di stato. È il costo, ed è dichiarato.

**A3 — Un segmento del rail è interattivo solo se porta un dettaglio.** *Clausola:* DS §9.3, «Tastiera: segmenti
focalizzabili, Enter apre il dettaglio.» *Ragione (misurata nel codice):* `portal/services.py` L1006 —
`journey_for()` restituisce `"detail": ""` per **tutti e sette** i passi; `"actor": ""` per tutti e sette; `owner_key`
non esiste nel contratto. Oggi non c'è nulla da aprire, e un comando che apre una regione vuota è esattamente il
difetto che la revisione ha nominato (Lacuna 3). *Richiesta:* il segmento è un `<li>` non interattivo quando
`step.detail` è vuoto e un `<details>` **nativo** quando non lo è; nessun `aria-expanded` scritto a mano, nessun JS.
*Compensazione:* il rail porta **un** bersaglio reale — un link a `portal:pathways` sotto la pista, non sette.
*Costo:* finché la vista non riempie `detail`, il rail è una lista leggibile e non focalizzabile.

**A4 — La checklist sceglie la forma sulla larghezza della COLONNA, non della finestra.** *Clausola:* DS §9.4,
«Tabella reale sopra 768 … pop-in sotto 768.» *Richiesta:* `@container centre (min-width: 40rem)`.
*Ragione (misurata):* a 1280 la colonna centrale dello spazio di lavoro 176/1fr/320 misura **552 px**; lì la tabella
a quattro colonne costa **1 554 px** per 9 voci contro **978 px** della forma a scheda. A 1440 la colonna è 672 px e
la tabella costa 1 202. A 768 (due colonne, inspector in coda) la colonna è 688 px e la tabella costa 1 174.
Punti di commutazione misurati: 1440 → tabella · 1280 → schede · 768 → tabella · 390 → schede.
*Costo:* fra 1200 e 1439 la checklist è a schede dove la clausola darebbe una tabella; una persona che ridimensiona
la finestra vede la forma cambiare due volte. `@container` è supportato (verificato: `CSS.supports('container-type','inline-size')` = `true`).

**A5 — `transform-origin: bottom` è un valore fisico.** *Clausola:* DS §11 / MOTION §5, «solo proprietà logiche».
*Ragione (verificata in Chromium 153):* `transform-origin` **non ha parole chiave logiche**. `setProperty` con
`inline-start`, `inline-end`, `start` o `block-start` lascia la proprietà vuota e il calcolato ricade su `50% 50%`
(`CSS.supports('transform-origin','inline-start')` = `false`). Il solo valore fisico che questa superficie usa è
`bottom` sulla tacca del misuratore — asse di blocco, identico in `fr`/`it`/`en`/`ar`, che sono tutte
`horizontal-tb`. *Costo:* una riga da rivedere il giorno in cui il prodotto avrà una lingua verticale.
*Nota:* il round 1 usava `transform-origin: inline-start` su una traccia `scaleX`. Quella traccia non esiste più
(§5); la deroga si riduce a questo unico valore.

**A6 — «Prochaine étape» è un foglio a tutta larghezza sopra il rail, non il primo foglio della colonna centrale.**
*Clausola:* DS §9.2. *Ragione (misurata):* a 390×844, con il rail sopra, il bottone primario cade a y ≈ 1 971 —
fuori dalla prima schermata. Con questo ordine il bottone **finisce a y = 839 su una piega a 844**. Il criterio
d'accettazione del committente («cosa devo fare») passa sul telefono solo così. *Nota:* `base_portal.html` L36-38
**rende già** `next_action.html` fuori da `.portal`, sopra lo spazio di lavoro: la spec allinea il documento al
codice, non il contrario. *Costo:* la colonna centrale comincia con la checklist.

---

## 1. RISPOSTA PUNTO PER PUNTO ALLA REVISIONE

### 1.1 Violazioni dei vincoli non negoziabili

| # | Verdetto | Che cosa è cambiato |
|---|---|---|
| 1 WCAG 1.4.11, la barra del rail | **FATTO** | Ho ricalcolato ogni numero del revisore e sono **tutti esatti**: `--owner-person` 2,52 · `project` **1,89** · `training` 2,25 · `authority` 3,33 · `territory` 2,56 su `--mid-2`; `--mid-3` su `--mid-2` **1,15**; `--hairline-dark-strong` composita in `#4A5961` = **2,19**. Il rail **si sposta sul capitolo carta** (la seconda opzione del MUST-FIX 1): sul terreno `--min-1` i cinque token **esistenti** danno 3,99–7,03 pieni e 3,15–5,29 *come disegnati* (pigmento + la propria trama). Nessuna rampa `--owner-*-dark`. Tabella completa in §4.4 |
| 2 DS §1.3.1, un solo accento | **FATTO** | `--accent` resta su tre soli oggetti della pagina: il link, il bottone primario, l'anello di focus. La marca «corrente» non è più tinta d'accento (è `--ink` su `--min-1`); `.state--review` non esiste più su questa superficie; il solo uso «di forma» è la **cornice 2 px sulla barra del segmento corrente**, che DS §9.3 prescrive alla lettera. **Contestato in parte:** il MUST-FIX 2 suggerisce «`--terr-line-lt`» come alternativa neutra — `--terr-line-lt` e `--accent` sono **lo stesso esadecimale, `#0F6A72`** (`v2/tokens.css` L47 e L42; rapporto fra i due = 1,00). Sostituire il nome del token non cambia un pixel e sarebbe il secondo accento con un altro nome |
| 3 La cascata `.on-dark .chip` distrugge l'errore | **FATTO** | Riscritto senza cascata: la **variante** dichiara due custom property, il **capitolo** le ripunta. Nessuna regola di capitolo tocca un selettore di variante, quindi nessuna specificità può vincere su un'altra. CSS completo in §4.3 |
| 4 MOTION §1, 720 ms | **FATTO** | 720 ms eliminato. L'unica traccia della pagina usa `var(--motion-draw)` = **900 ms**, il token già fissato in `v2/tokens.css` L118 |
| 5 Ombra animata | **FATTO** | `--shadow-2` è scritto **fuori** dalla `transition-property`, che nomina solo `background-color`. CSS letterale in §5. Il revisore ha ragione: la clausola non ha il qualificatore «in loop» e il round 1 lo aveva aggiunto |
| 6 DS §4, ritmo dello spazio | **FATTO** | Ogni valore di **spaziatura** è un token: `gap`, `padding` e `margin` in questa spec non contengono un solo numero. Il conteggio completo dei `px` letterali del CSS di questa spec, commenti esclusi, e il motivo di ciascuno: **1** (×30) e **2** (×8) e **3** (×1) = capelli, filetti e la cornice del segmento corrente — il ritmo della riga, non la scala; **5** (×4) e **7** (×4) = passo delle trame, con il minimo a 4 px che il rischio 3 impone; **10** (×8) = la barra, DS §9.3 alla lettera; **36** (×1) = la striscia di navigazione sotto 1024, DS §9.1 alla lettera; **48** (×2) = il bottone primario, DS §10, e la colonna della frontiera; **224** (×1, come solo ripiego di `--container-rail`) e **320** (×1) = lo spazio di lavoro, DS §9.1 alla lettera. Nessun altro numero. I letterali tipografici 13/17/22/12 del round 1 sono spariti in `--t-folio`/`--t-body`/`--t-entry`/`--t-caption`/`--t-ui`, e `gap:6px`/`padding-inline:10px`/`gap:3px` in `--s-1`/`--s-2` |

### 1.2 Lacune

| # | Verdetto | Dove è chiusa |
|---|---|---|
| 1 `--rail-progress` senza sorgente | **FATTO per soppressione** | La custom property non esiste più. Nessuna quota calcolata raggiunge il CSS: l'unico rapporto della pagina, il misuratore, porta `class="is-done"` dal ciclo del template. Ragione in §4.6 |
| 2 `transform-origin: inline-start` | **FATTO** | Verificato io stesso in Chromium 153: la dichiarazione è **respinta** e il calcolato ricade su `50% 50%` (632 px su una scatola di 1 264). La traccia `scaleX` non esiste più; il tracciato è `stroke-dashoffset` su `pathLength="1"`, che non ha origine. Il residuo fisico è dichiarato in **A5** |
| 3 Il pannello del rail è `…` | **FATTO** | `<details>` nativo, reso **solo** se `step.detail` è non vuoto; markup delle due diramazioni in §4.5. Deroga **A3** |
| 4 La PAROLA del responsabile senza sorgente | **FATTO** | `step.actor` è `""` per tutti e sette (misurato nel codice). Il template rende `step.actor` se c'è, altrimenti la dicitura indicativa; `data-owner` e la parola escono **dalla stessa espressione**, quindi non possono contraddirsi. §4.5 |
| 5 «Étape 3 sur 7» senza derivazione | **FATTO** | Derivata nel template, senza toccare vista né contratto: `forloop.counter` dentro `{% if step.is_current %}` e `journey|length`. Snippet in §4.5 |
| 6 `<li class="rail__frontier">` dentro l'`<ol>` | **FATTO e misurato** | `role="presentation"`. Verificato nell'albero di accessibilità: il DOM ha **8** `<li>`, l'albero espone **7 listitem** (FR e AR) |
| 7 `aria-expanded="false"` scritto a mano | **FATTO per soppressione** | Nessun `aria-expanded` nel markup. `<details>` lo gestisce da sé e funziona senza JS |
| 8 `min-block-size: 96px` non ci sta | **FATTO** | Il revisore aveva ragione e la sua stima era **bassa**. Misurato con i font reali: il segmento a 7 colonne è **201 px** a 1440 e **211 px** a 1280 (non 96, non 175–200). Ricostruito: etichetta a `--t-ui` 15/20, marca che va a capo, righe allineate con `grid-template-rows`. §4.5 e §7 |
| 9 I numeri del §7 sono asseriti | **FATTO** | §7 è riscritto come **derivazione**: ogni regione misurata prima e dopo, e la somma delle regioni ricade esattamente sull'altezza del documento a tutti e quattro i viewport |
| 10 `base_portal.html` è di tutti i ruoli | **FATTO** | Matrice delle diramazioni in §4.2 |
| 11 La diramazione «senza fascicolo» distrugge un testo bloccato | **FATTO** | `{% locked "p3.reserved.title" %}` + `p3.reserved.body` restano, e la spec dice esattamente dove. §4.2 |
| 12 `--accent-100` ridondante | **FATTO** | Cancellato. Ricalcolato: `--accent` su `#DCEAEB` = **5,12**, su `--accent-wash #D9EEF0` = **5,24** — il revisore ha ragione. E nemmeno `--accent-wash` serve più: nessuna marca è tinta d'accento (violazione 2) |
| 13 `@import` contro la lista di preload | **FATTO** | Tre file, non cinque, e tre righe di preload nominate con il numero di riga. §4.1 |
| 14 `-webkit-line-clamp` da solo | **FATTO e verificato** | Verificato in Chromium 153: `-webkit-line-clamp:3` da solo lascia il blocco a **168 px** (nessun effetto); con `display:-webkit-box; -webkit-box-orient:vertical; overflow:hidden` scende a **72 px**. `line-clamp` moderno **non** è supportato (`CSS.supports('line-clamp','3')` = `false`), quindi la tripletta `-webkit-` è obbligatoria. §4.7 |
| 15 `.plancia__plate` classe o `<img>` | **FATTO per soppressione** | Non c'è più né `<img>` né `<picture>`: la lastra è **SVG in linea**. §4.6 |
| 16 `static/img/v3/` non esiste | **FATTO per soppressione** | Nessuna directory nuova, nessun binario da committare. `scripts/territory.py` **già scrive** partial SVG Django; la lastra è una terza chiamata alla funzione che c'è. §4.6 |
| 17 Collisione sull'unico oggetto vivo | **FATTO** | Riconciliato leggendo la spec vicina: `platform-shell.md` §… usa una **sentinella `IntersectionObserver`** e un attributo `data-scrolled` — *«Nessun ascoltatore di scroll, nessuna lettura di layout»* — cioè un cambio di stato discreto, non un oggetto indicizzato allo scroll; e dichiara che `backdrop-filter` **non** è usato dalla barra («la barra scrollata cambia terreno, non sfoca»). Questa superficie spende **zero** della dotazione RICH: nessun loop ambientale, nessun oggetto legato allo scroll, nessun `backdrop-filter`. Il §7 del round 1 sbagliava a dire il contrario |

### 1.3 Segnali di «cheap / generico / default»

| # | Verdetto | Che cosa ho fatto |
|---|---|---|
| 1 La pillola è una Badge di libreria | **RIMOSSO** | L'oggetto si chiama **`.mark`** ed è un altro oggetto: raggio 0, filetto 2 px sul lato di lettura, un solo capello sotto, parola in **Fira Mono 13/16 `.08em` maiuscola** (la faccia dei riferimenti e del folio, non il sans dell'interfaccia), glifo **20 px tratto 1,5** come prescrive DS §6 — non i 14 px della libreria. Misurato: 29 px di altezza, raggio `0px`, filetto `2px`, glifo `20×20` tratto `1.5px`. Deroga **A2** |
| 2 Butta via l'unico segno proprio | **RIMOSSO** | Il filetto `border-inline-start` **è** il cuore della marca. Verificato in AR: passa a destra (`border-left 0` / `border-right 2px`) perché è una proprietà logica |
| 3 Una texture a `opacity .22` come risposta alle immagini | **RIMOSSO** | La risposta non è un'opacità: è una **lastra incorniciata e didascalata**, disegno vero al 100 % di presenza, in SVG generato. Vedi §4.6. Il revisore ha ragione che `imgCount 0 → 1` invisibile non è una risposta |
| 4 L'hover è `rgba(…,.05)` | **RIMOSSO** | Il rail **non ha hover**, perché non è interattivo (A3): un lavaggio al 5 % su un elemento che non fa nulla era ornamento. L'hover esiste dove c'è un bersaglio: riga della checklist (livello 2 + `--shadow-2` discreta) e bottoni |
| 5 «Inspector + `<dl>` + barra segmentata» è mobilio SaaS | **CONTESTATO in parte, e corretto** | Il `<dl>` a quattro fatti **non è una mia invenzione**: DS §9.1 (2) lo prescrive parola per parola come i quattro fatti della case band, ed è il criterio d'accettazione del committente reso visibile. Contesto quello. **Accetto il resto**: l'inspector prende una grammatica propria — spina a capello continua, **folio in mono numerato per blocco** (`01 · 02 · 03`), livello 3 con `--shadow-3`. E ho tagliato la prosa difensiva del §4.7 del round 1 |
| 6 La graticola è due gradienti al 5,5 % | **RIMOSSO** | Niente più graticola in CSS sul fondo. La graticola è **dentro la lastra**, generata, con le **tacche** che DS §6 prescrive («graticola 160 px con tacche») e che il round 1 aveva omesso, a peso pieno (`--on-dark` .14 sulle linee, `--terr-line` .85 sulle tacche) e con `vector-effect: non-scaling-stroke`. Il fondo della plancia è `--mid-2` più la sola vignetta |
| 7 Il §8 rischio 1 contradice il §4.5 | **FATTO, e allargato** | Il revisore ha trovato tre usi di `--accent-dark`; ce n'erano quattro (`.plancia__ref`, `.rail__here`, la tacca del misuratore, la traccia) e **tre erano violazioni del DS §1.3.1** che lui non aveva nominato. Ora: riferimento → `--on-dark` (**14,08**); «Vous êtes ici» → `--on-dark` + forma; tacche del misuratore → **`--terr-line`** (**5,51** su `--mid-2`), che è l'assegnazione letterale di DS §1.3.2 («isoipse, **tacche**, rotta»); la rotta della lastra → `--terr-line`. Sul capitolo mezzanotte `--accent-dark` non compare **mai**: zero occorrenze |

### 1.4 I quindici MUST-FIX, uno per uno

Nessuno è lasciato aperto. Dodici **FATTI**, tre **FATTI CON UNA CONTESTAZIONE PARZIALE** che porta il numero
che la prova.

| MUST-FIX | Verdetto | Dove · con quale misura |
|---|---|---|
| 1 Contrasto della barra del rail | **FATTO** | §4.4. Ricalcolati e confermati tutti i numeri del revisore (1,89–3,33 · 1,15 · 2,19). Presa la **seconda** opzione che offriva: il rail passa sulla carta. Rapporti pubblicati in tabella, pieni **e** come disegnati |
| 2 Togliere `--accent` da ogni elemento non interattivo | **FATTO, con contestazione parziale** | §1.1 riga 2 e §4.4. `var(--accent)` compare **2 volte** in tutto il CSS, entrambe prescritte da DS §9.2/§9.3. **Contesto** l'alternativa suggerita: `--terr-line-lt` **è** `#0F6A72`, lo stesso esadecimale di `--accent` (rapporto fra i due = **1,00**), quindi non sarebbe un'alternativa ma lo stesso pixel con un altro nome |
| 3 Sostituire `transform-origin: inline-start` | **FATTO** | §1.2 riga 2 e deroga **A5**. Riverificato: la dichiarazione è respinta, il calcolato ricade su `50% 50%`. La traccia `scaleX` è sparita; l'unico valore fisico rimasto è `bottom` su una tacca, dichiarato |
| 4 Dichiarare come `--rail-progress` arriva all'elemento | **FATTO per soppressione** | §4.6. Nessun rapporto calcolato raggiunge più il CSS: la tacca porta `is-done` dal ciclo del template. Motivazione scritta, non sottintesa |
| 5 La cascata `.on-dark .chip` | **FATTO** | §4.3. Riscritta a custom property: la variante dichiara, il capitolo ripunta. `--overdue` e `--seal` sopravvivono sulla plancia con 5,21 e 5,22 |
| 6 La diramazione senza fascicolo e i ruoli non-PERSONNE | **FATTO** | §4.2, matrice a quattro casi, con il testo bloccato nominato e la terza colonna che non si disegna quando non c'è inspector |
| 7 Ogni fatto che gli schermi di oggi portano | **FATTO** | §4.2, tabella di sette righe: sospensione, ripiego «Vous — aucun intervenant…», `portal-notices`, `rationale`, `ruleset_version`, `assessed_at`, `missing_count`, link al dettaglio |
| 8 Non mettere le fonti giuridiche dietro una disclosure | **FATTO** | §4.7. Presa la **seconda** opzione: il blocco pré-évaluation esce dall'inspector e va nella colonna centrale, con **tutti** i fondamenti visibili e nessun `<details>` |
| 9 Le due frasi prescritte, verbatim | **FATTO** | §4.8, entrambe citate per intero, con la sorgente (`orientation/seeds.py` L224-229 per la prima, `dashboard.html` L185 per la seconda) e il selettore che le ospita |
| 10 Correggere «oggi non c'è alcun bottone» | **FATTO** | §4.7. `next_action.html` L36-40 rende già `btn--primary`; la correzione è scritta e con essa l'avvertimento sulla seconda CTA |
| 11 Le voci di moto | **FATTO** | §5. 720 ms eliminato per `var(--motion-draw)`; `--shadow-2` fuori dalla `transition-property`, verificato con `grep` |
| 12 Rimisurare il §7 dopo l'altezza del segmento | **FATTO** | §4.4 e §7. Il segmento misura **201/211 px**, non 96 e nemmeno i 175–200 stimati; §7 è ricostruito come derivazione che quadra su entrambe le colonne |
| 13 `--accent-100` e i letterali grezzi | **FATTO** | §1.1 riga 6 e §1.2 riga 12. `--accent-100` cancellato (5,12 contro 5,24: il revisore ha ragione); conteggio completo dei `px` rimasti con la clausola che giustifica ciascuno |
| 14 Preload e passo di build | **FATTO** | §4.1 (tre righe di preload dopo L39, tre file e non cinque) e §4.6 (la chiamata in `scripts/territory.py`, che **non** crea `static/img/v3/` perché il generatore scrive partial SVG) |
| 15 Dare al badge qualcosa che non sia una pillola shadcn | **FATTO** | §4.3. `.mark`: raggio 0, filetto d'archivio 2 px, parola in **mono** 13/16, glifo **20 px** come DS §6, capello sotto. Misurato: 29 px, `border-radius: 0px`, `border-inline-start-width: 2px`, glifo `20×20` tratto `1.5px`. Deroga **A2** |

---

## 2. VERDETTO SULLO STATO ATTUALE (rimisurato questo round)

Ogni cifra qui sotto è stata **rimisurata** sul server vivo con la sessione QA; sono le stesse del round 1,
e ora sono accompagnate dalla scomposizione per regione che il §7 richiedeva.

**2.1 — Cinque schermi, e una prima schermata senza nulla da fare.** `scrollHeight` **4 296** a 1440×900,
**4 462** a 1280, **4 990** a 768, **7 994** a 390×844 (9,47 viewport). A 390 la banda del fascicolo è alta
**417 px**, `.next-action` comincia a `y = 843` su una piega a **844**: del blocco che risponde a «cosa devo fare»
si vede **un pixel**. La prima `.portal-section` comincia a `y = 1 418`.

**2.2 — Il RAIL 2.0 non esiste.** `.sequence__step` × 7: `aria-current` = `null` su tutti e sette; altezza 61–63;
nessun discendente focalizzabile. `.sequence__crossing` è definita in `register.css` L305–324 e
**nessun template la rende**. `.jurisdiction` è resa **solo** da `pages/home/_trust.html`: la barra delle
responsabilità sta sulla home pubblica e manca dal fascicolo.

**2.3 — I badge non sono badge.** `.state` calcolato: `background-color: rgba(0,0,0,0)`, `border-radius: 0px`,
`border-width: 0px` (esiste solo `border-inline-start: 2px solid currentcolor`), nessun `<svg>`, `::before` assente.
`.state--done` / `.state--review` rendono `rgb(30,74,133)` = `#1E4A85`, **assente dalla tavolozza V2**, a 7,97:1 su
`--min-0`: ha l'aspetto di un link. `.state--pending` rende `#4A5A62` = `--ink-2`, lo stesso inchiostro del corpo;
`--pending-700` non è usato da nessuna parte.

**2.4 — Gerarchia invertita.** `.folio__ordinal` 44 px e `.outcome__kind` 52 px sono i due elementi più grandi
della pagina, contro `h1` 38 px con interlinea 36. `.portal__section-title`, `.sequence__title` e `.entry__title`
misurano tutti e tre 22 px: tre livelli disegnati identici. `--t-title` 48/52 e `--t-band` 32/36 non sono applicati.

**2.5 — Nessuna profondità, nessun moto, nessuna immagine.** Su tutto `<main>`: ombre distinte **0**; elementi
con `animation-name` ≠ `none` **0**; `<img>`/`<picture>` **0**; `[data-mode]` = **`null`** (l'attributo non esiste
in nessun template del progetto: `grep -r data-mode templates/ static/css/ apps/ tests/` = 0 risultati).

**2.6 — La checklist su telefono.** `.data-table` a 390: 9 righe alte **293–341 px**, totale **2 891 px**.
`font-variant-numeric` sulla tabella = **`normal`**.

**2.7 — Bersagli.** Elementi interattivi sotto 44 px in `<main>`: **5** a 1440, **15** a 768 e a 390. Il minimo è
l'azione dello stato vuoto «Voir mes documents», **138,45 × 18 px**.

**Nota RTL.** In `ar` la logica è corretta (filetto a destra, nessun overflow orizzontale). Un difetto: gli ordinali
dei passi ereditano `Noto Naskh Arabic`, contro DS §3.1. Difetto di contenuto fuori da questa spec: su `/it/` e
`/ar/` il corpo di «Prochaine étape» esce in francese.

---

## 3. STRUMENTI CONSULTATI

**UI-UX-PRO-MAX** (7 interrogazioni, round 1, invariato nella sostanza). Accettati: «Step n of M» come **testo
visibile**; densità delle righe; card layout sotto la soglia invece del pop-in a quattro `data-label`; nessuna
durata sotto 120 ms. Respinti: il colore da solo per lo stato attivo (sul rail lo stato passa per quattro canali);
il gradiente caldo-freddo (i segmenti codificano **responsabilità**, che non ha ordine); il registro «istituzionale
⇒ complessità bassa»; GSAP/ScrollTrigger (libreria = Motion 13.4.1, CSP `script-src 'self'`); la palette
«Navy + Gold»; Liquid Glass; Cormorant/Montserrat via Google Fonts (vietati da CSP e da `forbidden.py`).

**21ST.DEV** (9 candidati, 3 letti nel codice). Cosa resta preso, dopo la revisione:

| # | Componente | Cosa prendo · cosa ho **cambiato** dopo la revisione |
|---|---|---|
| 1 | `stepper-03` | L'anatomia del conteggio visibile «Étape n sur N» e `aria-current="step"`. **Non prendo più** `<button>` per segmento: non c'è nulla da aprire (A3). Respinti anello che pulsa, molle `damping` 18/22, morph con `rotate` |
| 2 | `partition-bar` | La grammatica del segmento etichettato (barra sopra, parola + responsabile sotto) e il rifiuto di `style={{}}` in linea sotto CSP |
| 3 | `status` | **Respinto integralmente dopo la revisione.** Il round 1 ne prendeva «l'anatomia della pillola» ed è esattamente da lì che è arrivata la Badge di libreria. La marca V3 non ha né raggio 999 né fondo tinto sul capitolo scuro |
| 4 | `stepper-04` | Nulla. La pillola che scivola racconta un movimento continuo; il parcours è discreto |
| 5 | `c-stepper-13` | Il ripiegamento verticale, con la riduzione che DS §9.3 prescrive («barra a lato, etichette a destra») |
| 6 | `timeline-3` | Il glifo di **ruolo** al posto dell'avatar: l'attore è un ruolo, mai un volto |
| 7 | `c-progress-7` | L'accoppiata misuratore + lista, con le **tacche** e non la percentuale (DS §9.1) |
| 8 | `coss-badge` | Il contratto `variant`, riespresso in due custom property per variante — **non** la pillola |
| 9 | `badges-styled` | Nulla. Gradient fill, glow, live pulse: tre effetti esclusi |

---

## 4. LA PROPOSTA — «la plancia, il foglio, il registro»

**In una frase.** La prima schermata diventa **la plancia del fascicolo** — l'unico capitolo mezzanotte, con il
riferimento, i quattro fatti, il misuratore a tacche e una **lastra territoriale incorniciata**; sotto, su carta, il
**foglio della prossima azione** con il suo bottone; sotto ancora, a tutta larghezza su `--min-1`, il **RAIL 2.0**
come banda di registro inciso con la frontiera MA → IT; poi lo spazio di lavoro a tre colonne.

### 4.1 Modo di pagina, file, cascata

`base.html` L56, una riga cambiata — è il solo modo di dare al progetto l'attributo che DS §7 rende obbligatorio e
che oggi non esiste da nessuna parte:

```django
<main id="main-content" tabindex="-1" data-mode="{% block page_mode %}standard{% endblock %}">
```

`base_portal.html` dichiara `{% block page_mode %}rich{% endblock %}`. RICH = **un solo** capitolo mezzanotte
(la plancia), reveal editoriali ammessi, **isoipse e marea vietate** — e infatti la lastra di questa pagina non
porta strati di isoipse (§4.6).

CSS nuovi, **tre** file (non cinque, per non allungare la catena di richieste):

| File | raw | gzip | Contenuto |
|---|---:|---:|---|
| `static/css/v3/tokens-v3.css` | 1 041 | 394 | i 4 token della deroga A1, i 4 token di carta, le 12 coppie di variante della marca |
| `static/css/v3/mark.css` | 1 083 | 450 | `.mark` e le sue sei varianti |
| `static/css/v3/dashboard.css` | 15 968 | 3 238 | plancia, lastra, misuratore, foglio d'azione, rail, spazio di lavoro, checklist, inspector |
| **totale** | **18 092** | **3 722** | misurato con `gzip -9` sul CSS candidato |

`static/css/main.css`: tre `@import` dopo `v3/buttons.css`.
`templates/base.html`: **tre righe di preload dopo L39** (l'ultima oggi è `css/v3/buttons.css`), nello stesso stile
delle quattordici che ci sono — il commento a L25 dice perché, e cinque `@import` non preloadati avrebbero
ricreato la catena che quel commento ha rimosso.

Template toccati: `base.html` (una riga), `base_portal.html` (blocco `page_mode`, blocco `portal_inspector`,
diramazione senza fascicolo), `dashboard.html`, `partials/case_header.html` → plancia, e **nuovi**
`partials/{rail.html, rail_segment.html, mark.html, task_row.html, task_card.html, inspector.html}`.
**Nessuna vista, nessun contratto dati, nessuna migrazione.**
Glifi: **non** un nuovo sprite. `static/img/icons.svg` esiste già con 36 simboli `#icon-*` e
`{% svg_icon %}` (`apps/core/templatetags/ile_core.py` L65) li rende. Ne servono **sette nuovi**:
`icon-owner-person`, `-owner-project`, `-owner-training`, `-owner-authority`, `-owner-territory`,
`icon-frontier`, `icon-seal`; e due di stato, `icon-wedge` e `icon-ring-alert`. `icon-check`, `icon-clock`,
`icon-warning`, `icon-person`, `icon-institution`, `icon-university` ci sono già.

### 4.2 Le diramazioni: chi vede che cosa

`base_portal.html` è la shell di **ogni** ruolo. La matrice, esplicita:

| Caso | Plancia | Foglio d'azione | Banda del rail | Spazio di lavoro |
|---|---|---|---|---|
| **PERSONNE con fascicolo** (`case`) | sì, completa | se `next_action` | sì, se `journey` | 3 colonne: nav · centro · inspector |
| **PERSONNE senza fascicolo** (`not case`) | **variante «soglia»**: stesso terreno mezzanotte, stessa lastra, ma al posto dei quattro fatti il **testo bloccato** — `{% locked "p3.reserved.title" %}` come `<h1>` e `p3.reserved.body` come lead, resi da `components/page_header.html` **dentro** la plancia con `class="plancia__threshold"`; nessun riferimento, nessun misuratore | no | no | **2 colonne**: nav · centro (le sezioni vuote con la loro grammatica). La terza colonna **non si disegna**: `.work` passa a `grid-template-columns: var(--container-rail) minmax(0,1fr)` via `:has()` → vedi sotto |
| **impresa / istituzione / università / professionista** (`cards and not is_person`) | no — la plancia è la banda **di un fascicolo**, e questi ruoli non ne hanno uno (P1 in `REQUIREMENT_MATRIX_V2.md`). Ricevono `components/page_header.html` come oggi | se `next_action` | no | 2 colonne, e la griglia di card **invariata**: è il ponte, ed è marcato come tale in `dashboard.html` |

```css
/* La terza colonna esiste solo se c'è un inspector da metterci. Niente colonna vuota. */
.work { display: grid; grid-template-columns: var(--container-rail, 224px) minmax(0, 1fr);
        gap: var(--s-6); padding-block: var(--s-12); align-items: start; }
@media (min-width: 75rem) {
  .work:has(> .work__inspector) { grid-template-columns: var(--container-rail) minmax(0,1fr) 320px; }
}
```

`var(--container-rail)` è il token del sistema, non un 224 magico: `tokens.css` lo definisce **176** a `lg`,
**200** a `xl`, **220** a `xxl`; 224 resta solo come ripiego. Misurato: colonna centrale **672 px** a 1440,
**552** a 1280, **688** a 768. `:has()` è supportato (verificato: `CSS.supports('selector(:has(> div))')` =
`true`); dove non lo fosse, la regola non si applica e lo spazio di lavoro resta a due colonne con l'inspector
in coda — cioè la forma che serve proprio nel caso «nessun inspector». Il degrado non produce mai la colonna vuota
che la Lacuna 10 denunciava.

**I fatti che la pagina di oggi porta e che il round 1 aveva perso.** Ognuno ha un posto nominato:

| Fatto | Sorgente | Dove va |
|---|---|---|
| `case.suspension_reason` + «Dossier suspendu» | `case_header.html` L70-75 | `.plancia__suspension`, ultima riga della plancia, a tutta larghezza, filetto 2 px `--err-dark`, fondo `--mid-1`, parola + frase. Mai un colore da solo |
| «Vous — aucun intervenant n'est assigné à ce dossier» | `case_header.html` L56 | il `<dd>` del fatto **Responsable**, verbatim, quando `responsible` è vuoto |
| `portal-notices` «Avis de l'équipe» | `dashboard.html` L48-54 | **subito sotto il foglio d'azione**, a tutta larghezza, `aria-label` invariato: è un avviso dell'équipe, non un contenuto di colonna |
| `assessment.rationale` | `dashboard.html` L156 | `.assess__why`, colonna **centrale**, mai troncato (contiene la frase bloccata, §4.8) |
| `assessment.ruleset_version` + `assessed_at` | L159-163 | `.assess__note`: marca `--seal` «Jeu de règles v{n}» + data in mono |
| `assessment.missing_count` | L188-190 | `.assess__gloss`, sotto i fondamenti |
| «Voir le détail de la pré-évaluation» | L191 | `.assess__more`, link con freccia, invariato |

### 4.3 `mark.css` — la marca di stato

Quattro canali: **parola** + **glifo proprio per variante** + **forma** (filetto 2 px, raggio 0) + colore.
La variante dichiara due custom property; il capitolo le ripunta. Nessuna regola di capitolo tocca un selettore
di variante, quindi la cascata non può più cancellare uno stato (violazione 3).

```css
:root{
  --m-done-fg:var(--ok-800);      --m-done-bg:var(--ok-100);
  --m-current-fg:var(--ink);      --m-current-bg:var(--min-1);
  --m-todo-fg:var(--pending-700); --m-todo-bg:var(--pending-100);
  --m-wait-fg:var(--ink-3);       --m-wait-bg:var(--neutral-100);
  --m-overdue-fg:var(--err-700);  --m-overdue-bg:var(--err-100);
  --m-seal-fg:var(--seal-700);    --m-seal-bg:var(--seal-100);
  --m-hair:var(--hairline);
}
.on-dark{
  --m-done-fg:var(--ok-dark);      --m-done-bg:transparent;
  --m-current-fg:var(--on-dark);   --m-current-bg:transparent;
  --m-todo-fg:var(--pending-dark); --m-todo-bg:transparent;
  --m-wait-fg:var(--on-dark-3);    --m-wait-bg:transparent;
  --m-overdue-fg:var(--err-dark);  --m-overdue-bg:transparent;
  --m-seal-fg:var(--seal-dark);    --m-seal-bg:transparent;
  --m-hair:var(--hairline-dark);
}
.mark{display:inline-flex;align-items:center;gap:var(--s-2);
  min-block-size:calc(var(--s-5) + var(--s-2));          /* 28px: glifo 20 + 2×--s-1 */
  padding-inline:var(--s-2);padding-block:var(--s-1);
  border-radius:0;                                        /* deroga A2 */
  border-inline-start:2px solid var(--mark-fg);           /* il filetto d'archivio */
  border-block-end:1px solid var(--m-hair);
  background:var(--mark-bg);color:var(--mark-fg);
  font-family:var(--f-mono);font-size:var(--t-folio);line-height:var(--t-folio-lh);
  letter-spacing:var(--track-folio);text-transform:uppercase;
  font-variant-numeric:tabular-nums lining-nums}
.mark__glyph{inline-size:var(--s-5);block-size:var(--s-5);flex:none;
  fill:none;stroke:currentColor;stroke-width:1.5}          /* DS §6: 20px, tratto 1.5 */
.mark--done   {--mark-fg:var(--m-done-fg);   --mark-bg:var(--m-done-bg)}    /* glifo check      */
.mark--current{--mark-fg:var(--m-current-fg);--mark-bg:var(--m-current-bg)} /* glifo cuneo      */
.mark--todo   {--mark-fg:var(--m-todo-fg);   --mark-bg:var(--m-todo-bg)}    /* glifo clock      */
.mark--wait   {--mark-fg:var(--m-wait-fg);   --mark-bg:var(--m-wait-bg)}    /* glifo cerchio    */
.mark--overdue{--mark-fg:var(--m-overdue-fg);--mark-bg:var(--m-overdue-bg)} /* glifo anello !   */
.mark--seal   {--mark-fg:var(--m-seal-fg);   --mark-bg:var(--m-seal-bg)}    /* glifo sigillo    */
:lang(ar) .mark{text-transform:none;letter-spacing:0}
@media (forced-colors:active){
  .mark{background:Canvas;color:CanvasText;border-color:CanvasText;forced-color-adjust:none}
  .mark__glyph{stroke:CanvasText}
}
```

**Rapporti calcolati** (relative luminance WCAG 2.x, ricalcolati questo round):

| Variante | Carta: parola su fondo | Mezzanotte: parola su `--mid-2` |
|---|---|---|
| `--done` | `--ok-800 #186B43` su `--ok-100` **5,43** (su `--min-2` 6,25) | `--ok-dark #29A86A` **5,22** |
| `--current` | `--ink` su `--min-1` **13,59** | `--on-dark` **14,08** |
| `--todo` | `--pending-700` su `--pending-100 #F0E9DE` **5,79** | `--pending-dark #B58D5F` **5,25** |
| `--wait` | `--ink-3` su `--neutral-100 #E8E9E7` **5,04** | `--on-dark-3` **5,85** |
| `--overdue` | `--err-700` su `--err-100` **5,10** | `--err-dark #E6706A` **5,21** |
| `--seal` | `--seal-700 #6B4F2E` su `--seal-100` **6,11** (su `--min-0` 6,80) | `--seal-dark #AF8E69` **5,22** |

Il filetto è `currentColor`, quindi porta lo stesso rapporto della parola: ≥ 5,04 ovunque, molto sopra il 3:1
di 1.4.11. Nessuna variante è tinta d'accento.

**Portata.** `.mark` sostituisce `.state` **solo** nei template di questa superficie. `register.css` non si tocca:
`.state--*` è usata da 15 altre superfici e la sua correzione appartiene a `badges.md`. Effetto su questa pagina:
`#1E4A85` non viene più reso (§2.3).

**Mappa degli stati**, perché l'implementatore non debba inventarla:

| Sorgente | Valore | Variante |
|---|---|---|
| `ChecklistStatus` | `done` | `--done` |
| | `in_progress` | `--current` |
| | `pending` | `--todo` |
| | `not_applicable` | `--wait` |
| | `blocked` | `--overdue` |
| `item.is_overdue` (proprietà) | vero | `--overdue`, **vince** su `status` |
| `DOCUMENT_STATES` (`portal/services.py` L1028) | `valid` | `--done` |
| | `review` | `--wait` |
| | `invalid` | `--overdue` |
| responsabile = `authority` / jeu de règles | — | `--seal` |

### 4.4 `rail.css` — il RAIL 2.0, sul capitolo carta

**Perché sulla carta.** Il MUST-FIX 1 dà due strade. Ho misurato la prima e l'ho respinta: per portare i cinque
`--owner-*` sul terreno `--mid-2` servivano cinque token nuovi, e calibrati perché ogni barra *come disegnata*
(pigmento + la propria densità di trama) cadesse su 3,05–3,07:1, il pigmento pieno doveva salire fino a 4,39:1 —
cioè un bronzo molto chiaro accanto al sigillo, contro DS rischio 7. Sulla carta i **cinque token esistenti**
passano senza toccare nulla:

| Responsabile | Token (esistente) | Trama | Pieno su `--min-1` | **Come disegnata** |
|---|---|---|---|---|
| persona | `--owner-person #0F6A72` | pieno, nessuna trama | **5,29** | **5,29** |
| équipe del progetto | `--owner-project #34506A` | hachures 45°, 1 px / 5 px (20 % terreno) | 7,03 | **4,37** |
| organismo di formazione | `--owner-training #1C5F7C` | punti, `background-size:5px 5px` (15,2 %) | 5,91 | **4,32** |
| autorità competente | `--owner-authority #8C6D4B` | linee 90°, 1 px / **7 px** (14,3 %) | 3,99 | **3,15** |
| territorio | `--owner-territory #2F6B5C` | tratteggio 2 px / 10 px (20 %) | 5,21 | **3,51** |
| indicativo (nessun dato) | `--ink-3 #55646B` | hachures 135°, 1 px / 7 px | 5,14 | **3,86** |

«Come disegnata» = colore medio pesato sull'area della barra, composito del terreno sopra il pigmento, contro
`--min-1`. Il passo dell'autorità è 7 px e non 4 perché a 4 px la media cadeva a **2,68** — sotto 1.4.11. Ogni
barra porta inoltre `border: 1px solid var(--seg)`, un bordo **pieno** che dà al bordo della forma il rapporto
pieno della colonna «Pieno» (≥ 3,99) indipendentemente dalla trama.

**Lo stato è forma, non solo colore** — e la trama sopravvive in tutti e tre gli stati, perché si **inverte**:

```css
/* Ogni responsabile dichiara due trame: NEGATIVA (linee di terreno sul pigmento, barra "inchiostrata")
   e POSITIVA (linee di pigmento sul terreno, barra "incisa"). Il round 1 disegnava la trama di terreno
   anche sulla barra trasparente: le linee erano del colore del fondo, cioè invisibili. */
[data-owner="person"]{--seg:var(--owner-person);--hatch-neg:none;--hatch-pos:none;--hatch-size:auto}
[data-owner="project"]{--seg:var(--owner-project);
  --hatch-neg:repeating-linear-gradient(45deg,var(--min-1) 0 1px,transparent 1px 5px);
  --hatch-pos:repeating-linear-gradient(45deg,var(--seg)   0 1px,transparent 1px 5px);--hatch-size:auto}
[data-owner="training"]{--seg:var(--owner-training);
  --hatch-neg:radial-gradient(var(--min-1) 1.1px,transparent 1.2px);
  --hatch-pos:radial-gradient(var(--seg)   1.1px,transparent 1.2px);--hatch-size:5px 5px}
[data-owner="authority"]{--seg:var(--owner-authority);
  --hatch-neg:repeating-linear-gradient(90deg,var(--min-1) 0 1px,transparent 1px 7px);
  --hatch-pos:repeating-linear-gradient(90deg,var(--seg)   0 1px,transparent 1px 7px);--hatch-size:auto}
[data-owner="territory"]{--seg:var(--owner-territory);
  --hatch-neg:repeating-linear-gradient(to right,var(--min-1) 0 2px,transparent 2px 10px);
  --hatch-pos:repeating-linear-gradient(to right,var(--seg)   0 2px,transparent 2px 10px);--hatch-size:auto}
[data-owner="indicative"]{--seg:var(--ink-3);
  --hatch-neg:repeating-linear-gradient(135deg,var(--min-1) 0 1px,transparent 1px 7px);
  --hatch-pos:repeating-linear-gradient(135deg,var(--seg)   0 1px,transparent 1px 7px);--hatch-size:auto}

.rail__bar{display:block;block-size:10px;                       /* DS §9.3: barra 10 px */
  border:1px solid var(--seg);
  background-color:var(--seg);background-image:var(--hatch-neg);background-size:var(--hatch-size)}
[data-state="done"]    .rail__bar{background-color:var(--seg);background-image:var(--hatch-neg)}
[data-state="todo"]    .rail__bar{background-color:transparent;background-image:var(--hatch-pos)}
[data-state="current"] .rail__bar{background-color:var(--min-2);background-image:none;
                                  border:2px solid var(--accent)}   /* DS §9.3, l'accento come FORMA */
[data-state="blocked"] .rail__bar{background-color:transparent;background-image:var(--hatch-pos);
                                  border:2px solid var(--err-700)}
```

Verificato nel calcolato: `person/done` → `background-color: rgb(15,106,114)`, `background-image: none`;
`training/todo` → `background-color: rgba(0,0,0,0)`, `background-image: radial-gradient(rgb(28,95,124) 1.1px, …)`;
`training/current` → `rgb(251,250,248)` con bordo `rgb(15,106,114)` a `2px`.

**La pista.**

```css
.rail-band{background:var(--min-1);border-block:1px solid var(--hairline);padding-block:var(--s-8)}
.rail__h{font-family:var(--f-mono);font-size:var(--t-folio);line-height:var(--t-folio-lh);
  letter-spacing:var(--track-folio);text-transform:uppercase;color:var(--ink-3);margin:0 0 var(--s-1)}
.rail__count{font-family:var(--f-sans);font-size:var(--t-ui);line-height:var(--t-ui-lh);
  color:var(--ink-2);margin:0 0 var(--s-4)}
.rail__track{display:grid;grid-auto-flow:column;grid-auto-columns:minmax(0,1fr);
  gap:var(--s-1);list-style:none;margin:0;padding:0}
.rail__seg{display:grid}
.rail__cell{display:grid;grid-template-rows:auto minmax(0,1fr);gap:var(--s-2);
  inline-size:100%;padding-block:0 var(--s-3)}
.rail__body{display:grid;grid-template-rows:auto minmax(0,1fr) auto auto;gap:var(--s-2);align-content:start}
.rail__head{display:flex;align-items:center;gap:var(--s-2)}
.rail__num{font-family:var(--f-mono);font-size:var(--t-folio);line-height:var(--t-folio-lh);
  letter-spacing:var(--track-folio);font-variant-numeric:tabular-nums lining-nums;
  direction:ltr;unicode-bidi:isolate;color:var(--ink-3)}
.rail__glyph{inline-size:var(--s-5);block-size:var(--s-5);flex:none;fill:none;stroke:var(--seg);stroke-width:1.5}
.rail__label{font-family:var(--f-sans);font-size:var(--t-ui);line-height:var(--t-ui-lh);color:var(--ink);margin:0}
.rail__state{margin:0}
.rail__owner{font-family:var(--f-mono);font-size:var(--t-caption);line-height:var(--t-caption-lh);
  letter-spacing:var(--track-folio);color:var(--ink-2);margin:0}
.rail__here{font-family:var(--f-mono);font-size:var(--t-caption);line-height:var(--t-caption-lh);
  letter-spacing:var(--track-folio);text-transform:uppercase;color:var(--ink);margin:0}
.rail__frontier{display:grid;grid-template-rows:auto minmax(0,1fr);gap:var(--s-2);inline-size:48px;
  border-inline:1px dashed var(--hairline-strong)}          /* il canale, 3,14:1 su --min-1 */
.rail__frontier svg{inline-size:var(--s-6);block-size:var(--s-6);justify-self:center;
  fill:none;stroke:var(--ink-2);stroke-width:1.5}           /* inchiostro, non teal: vedi la nota sotto */
.rail__frontier span{font-family:var(--f-mono);font-size:var(--t-caption);line-height:var(--t-caption-lh);
  letter-spacing:var(--track-folio);color:var(--ink-2);writing-mode:vertical-rl;justify-self:center}
.rail__legend{display:flex;flex-wrap:wrap;gap:var(--s-2) var(--s-6);list-style:none;margin:var(--s-4) 0 0;padding:0}
.rail__key{display:inline-flex;align-items:center;gap:var(--s-2);font-family:var(--f-mono);
  font-size:var(--t-caption);line-height:var(--t-caption-lh);letter-spacing:var(--track-folio);color:var(--ink-2)}
.rail__swatch{inline-size:var(--s-6);block-size:10px;border:1px solid var(--seg);
  background-color:var(--seg);background-image:var(--hatch-neg);background-size:var(--hatch-size)}
.rail__caption{font-family:var(--f-sans);font-size:var(--t-caption);line-height:var(--t-caption-lh);
  color:var(--ink-3);margin:var(--s-2) 0 0}
.rail__more{margin:var(--s-4) 0 0}

/* 768–1199: due colonne, la frontiera attraversa la pista intera */
@media (min-width:48rem) and (max-width:74.999rem){
  .rail__track{grid-auto-flow:row;grid-template-columns:repeat(2,minmax(0,1fr));gap:var(--s-3) var(--s-6)}
  .rail__frontier{grid-column:1/-1}
}
/* sotto 1200: barra a lato, etichette a destra (DS §9.3) */
@media (max-width:74.999rem){
  .rail__track{grid-auto-flow:row;gap:var(--s-3)}
  .rail__cell{grid-template-columns:10px minmax(0,1fr);gap:0 var(--s-4);padding-block:0}
  .rail__bar{block-size:auto;inline-size:10px;align-self:stretch}
  .rail__body{gap:var(--s-1)}
  .rail__frontier{inline-size:auto;grid-template-columns:10px minmax(0,1fr);grid-template-rows:none;
    gap:0 var(--s-4);align-items:center;
    border-inline:0;border-block:1px dashed var(--hairline-strong);padding-block:var(--s-2)}
  .rail__frontier svg{inline-size:10px}
  .rail__frontier span{writing-mode:horizontal-tb;justify-self:start}
}
@media (forced-colors:active){
  .rail__bar{forced-color-adjust:none}          /* DS §11: le trame restano */
  .rail__frontier svg{stroke:CanvasText}
}
```

**Perché la frontiera è disegnata a inchiostro e non in teal.** Sul capitolo carta `--terr-line-lt` e `--accent`
sono **lo stesso esadecimale, `#0F6A72`**: un glifo «di territorio» accanto alla cornice d'accento del segmento
corrente sarebbe, a occhio, un terzo oggetto interattivo. Su questa superficie la disciplina è più stretta di
quanto DS §1.3.2 richieda: sulla **carta** il colore `#0F6A72` compare **solo** dove DS §1.3.1 lo permette —
`grep -c 'var(--accent)'` sul CSS di questa spec dà **2** (il filetto 3 px del foglio d'azione, DS §9.2; la
cornice 2 px del segmento corrente, DS §9.3) — e la grammatica cartografica sulla carta è portata dal **canale
tratteggiato** e dalla trama, non da un teal. Il teal del territorio vive dove non può essere confuso con un
comando: dentro la lastra, sul capitolo mezzanotte, come `--terr-line` (`grep` = 7 occorrenze, tutte grafiche).

**Misure reali** (font veri, testi francesi veri, headless, DSF 1):

| viewport | contenitore | colonna del segmento | altezza del segmento | righe dell'etichetta |
|---|---:|---:|---:|---|
| 1440 (xl) | 1320 (contenuto 1240) | **151,5** | **201** | 1–3 |
| 1280 (lg) | 1176 (contenuto 1096) | **133,5** | **211** | 1–4 |
| 768 (md, 2 colonne) | 768 (contenuto 688) | **332** | 103–123 | 1 |
| 390 (sm) | 390 (contenuto 350) | **350** | 103–123 | 1 |

Nessun `min-block-size` sulla cella: l'altezza **è** il contenuto, e le righe si allineano fra i segmenti grazie a
`grid-template-rows` (marca e responsabile finiscono alla stessa quota in tutti e sette). **Nessun `line-clamp`
sull'etichetta di un passo del parcours**: troncare il nome di una tappa amministrativa è una perdita di significato,
e la griglia cresce senza rompere nulla. Verificato: `scrollWidth > clientWidth` su ogni discendente della cella = **0**;
`document.documentElement.scrollWidth > clientWidth` = `false` a tutti e quattro i viewport, in `fr` e in `ar`.

### 4.5 Il markup del rail

**Due filtri, e nient'altro.** Il linguaggio dei template Django non sa trasportare un valore da un'iterazione
alla successiva, quindi «l'ordinale del passo corrente» non è derivabile con i soli tag nativi. Due filtri in
`apps/core/templatetags/ile_core.py` — accanto a `svg_icon` e `active`, che vivono già lì. **Leggono il contratto,
non lo cambiano**; nessuna vista, nessun modello, nessuna migrazione:

```python
@register.filter
def current_index(journey) -> int:
    """1-based ordinal of the step marked `is_current`, or 0. The journey contract exposes
    `is_current` per step and no index; this reads it, it does not add to it."""
    for i, step in enumerate(journey or (), start=1):
        if step.get("is_current"):
            return i
    return 0


#: owner key -> glyph in static/img/icons.svg. `indicative` (no data yet) falls back to the compass.
_OWNER_GLYPHS = {"person": "owner-person", "project": "owner-project", "training": "owner-training",
                 "authority": "owner-authority", "territory": "owner-territory"}


@register.filter
def owner_glyph(key: str) -> str:
    return _OWNER_GLYPHS.get(key or "", "compass")
```

```django
{# partials/rail.html — contratto: `journey` (lista di dict da portal.services.journey_for), `pathways_url` #}
{% load i18n ile_core %}
{% with total=journey|length current=journey|current_index %}
<section class="rail-band" aria-labelledby="rail-h">
  <div class="container">
    <nav class="rail" aria-labelledby="rail-h">
      <p class="rail__h" id="rail-h">{% translate "Mon parcours" %}</p>
      {% if current %}<p class="rail__count">{% blocktranslate with n=current %}Étape {{ n }} sur {{ total }}{% endblocktranslate %}</p>{% endif %}

      <ol class="rail__track">
        {% for step in journey %}
          {% if forloop.counter == 4 %}
          {# La frontiera MA → IT. JOURNEY_STEPS (portal/services.py L975-983) è una tupla FISSA: i
             primi tre passi hanno side="morocco", gli ultimi quattro side="italy". La riva cambia
             fra il terzo e il quarto, sempre. role="presentation" perché non è un passo: verificato,
             l'albero di accessibilità espone 7 listitem su 8 <li>. #}
          <li class="rail__frontier" role="presentation">
            {% svg_icon "frontier" "rail__frontier-glyph" %}
            <span>{% translate "MA → IT" %}</span>
          </li>
          {% endif %}
          {% include "portal/partials/rail_segment.html" with step=step index=forloop.counter current=current %}
        {% endfor %}
      </ol>

      <ul class="rail__legend">
        {% for key, word in owner_legend %}
        <li class="rail__key" data-owner="{{ key }}">
          <span class="rail__swatch" aria-hidden="true"></span><span>{{ word }}</span>
        </li>
        {% endfor %}
      </ul>
      <p class="rail__caption">{% translate "Les segments marquent des étapes, non des durées." %}</p>
      {% if pathways_url %}<p class="rail__more">
        <a class="link-arrow" href="{{ pathways_url }}">{% translate "Voir mon parcours en détail" %}
        {% svg_icon "arrow" "icon icon--flip-rtl" %}</a></p>{% endif %}
    </nav>
  </div>
</section>
{% endwith %}
```

```django
{# partials/rail_segment.html — contratto: `step`, `index` (1-based), `current` (1-based, 0 se nessuno) #}
{% load i18n ile_core %}
<li class="rail__seg"
    data-state="{% if index == current %}current{% elif current and index < current %}done{% else %}todo{% endif %}"
    data-owner="{{ step.owner_key|default:'indicative' }}"
    {% if index == current %}aria-current="step"{% endif %}>

  {% if step.detail %}
  <details class="rail__cell rail__cell--more"><summary class="rail__summary">
  {% else %}
  <div class="rail__cell">
  {% endif %}

    <span class="rail__bar" aria-hidden="true"></span>
    <div class="rail__body">
      <span class="rail__head">
        <span class="rail__num">{{ index|stringformat:"02d" }}</span>
        {% svg_icon step.owner_key|owner_glyph "rail__glyph" %}
      </span>
      <p class="rail__label">{{ step.label }}</p>
      <p class="rail__state">
        {% if index == current %}{% translate "Étape actuelle" as w %}{% include "portal/partials/mark.html" with kind="current" label=w %}
        {% elif current and index < current %}{% translate "Terminée" as w %}{% include "portal/partials/mark.html" with kind="done" label=w %}
        {% else %}{% translate "À venir" as w %}{% include "portal/partials/mark.html" with kind="wait" label=w %}{% endif %}
      </p>
      <p class="rail__owner">{% if step.actor %}{{ step.actor }}
        {% else %}{% translate "Responsable à préciser — à titre indicatif" %}{% endif %}</p>
      {% if index == current %}<p class="rail__here">{% translate "Vous êtes ici" %}</p>{% endif %}
    </div>

  {% if step.detail %}
  </summary><div class="rail__detail">{{ step.detail }}</div></details>
  {% else %}
  </div>
  {% endif %}
</li>
```

Le tre parole di stato sono quelle di DS §9.3 alla lettera: **Terminée · Étape actuelle · À venir**.
La variante della marca per «À venir» è `--wait` (neutra) e non `--todo` (in attesa d'azione): un passo non ancora
raggiunto non è un compito in ritardo di nessuno.

Tre cose che questo markup **non** fa, e perché:
1. **Nessun `aria-expanded`.** `<details>` lo espone da sé, correttamente, e senza JavaScript. La Lacuna 7 —
   «il template dichiara `false` mentre senza JS tutto è aperto» — non può più verificarsi.
2. **Nessun pannello vuoto.** Il `<details>` esiste solo se `step.detail` esiste. Oggi (`journey_for()` L1006:
   `"detail": ""`) **zero** segmenti su sette rendono un `<details>`: il rail è una lista leggibile, e lo dice
   la deroga A3.
3. **La parola del responsabile e `data-owner` vengono dallo stesso dato.** Se un giorno la vista riempirà
   `owner_key`, riempirà anche `actor`; finché non lo fa, la trama è `indicative` **e** la dicitura è visibile.
   La dicitura non è rimovibile via CSS: è testo nel flusso.

`owner_legend` è costruito nel template dalle chiavi effettivamente presenti fra i passi (o, quando non ce n'è
nessuna, dalla sola voce `indicative`): la legenda elenca ciò che è disegnato, mai cinque trame quando se ne
disegna una.

### 4.6 `plancia.css` — il capitolo mezzanotte e la lastra

**La lastra non è un'immagine nuova: è un disegno che il progetto genera già e che nessun template rende.**
`scripts/territory.py` scrive partial SVG Django (non raster) e produce **già**
`templates/portal/partials/territory_band_{base,layer-1}.svg` per «PLATFORM BAND 1440 × 260» (L181-185) — reso da
nessuna parte (`grep -r territory_band templates/` = 0 risultati). Lo stesso difetto di `.sequence__crossing`.

La chiamata che serve è una terza riga in `main()`, e **nessun strato di isoipse**, perché DS §7 le vieta su RICH:

```python
# PLATE 1200 × 480 — la lastra del fascicolo: graticola con tacche, una meridiana di frontiera,
# la rotta in due tratti che la attraversa, sei stazioni. Nessuna isoipsa: la pagina è RICH.
w, h = 1200, 480
fx = 660                                     # la meridiana
sta_ma = [(108, 318), (282, 246), (468, 300)]
sta_it = [(852, 222), (1014, 300), (1128, 198)]
write(build_plate(w, h, fx, sta_ma, sta_it, graticule=120), BAND_DIR, "territory_plate")
```

`build_plate()` è `build()` con `layers=0` più due gruppi: `terr__frontier` (una meridiana piena e due bordi di
canale tratteggiati a ±16 px) e la rotta spezzata in `terr__route--ma` / `terr__route--it`, ciascuna con
`pathLength="1"`. **Misurato generando il file davvero** (importando `scripts/territory.py` in uno scratch, senza
scrivere nel repository): **2 961 byte raw, 709 byte gzip**, in linea nell'HTML — **zero richieste HTTP**, nessun
AVIF, nessuna directory nuova, nessun binario, perfetta a DPR 1/1,5/2/3 senza moiré perché ogni tratto è
`vector-effect: non-scaling-stroke`.

Il round 1 proponeva «una lastra AVIF ≤ 44 KB a 1280 con `<picture>` e `sizes`, a `opacity .22`». Era, come dice
il revisore, invisibile *e* costosa: **62 volte** i byte di questa, con una catena di richieste in più e una
directory da creare. Qui la lastra è **al 100 % di presenza**, incorniciata, con la sua didascalia.

```django
<figure class="plate">
  <svg class="plate__frame" viewBox="0 0 1200 480" preserveAspectRatio="xMidYMid slice"
       aria-hidden="true" focusable="false">{% include "portal/partials/territory_plate_base.svg" %}</svg>
  <figcaption>33.97° N · 6.85° W → 45.41° N · 11.88° E</figcaption>
</figure>
```

La didascalia sono **le coordinate verbatim di DS §8.3**: zero prosa nuova, zero affermazione su un confine.
`aria-hidden` sul disegno (decorativo), la didascalia nel flusso (fattuale). La lastra **non si specchia** in
`ar`: un territorio non ha direzione di lettura (DS §11 elenca ciò che non si specchia — numeri, titolo bloccato,
fotografia; una carta appartiene a quella lista, non a quella delle frecce). `HUMAN_QA_REQUIRED`.

```css
.plancia{position:relative;isolation:isolate;overflow:clip;
  background:var(--mid-2);color:var(--on-dark);
  border-block-end:1px solid var(--hairline-dark-strong);padding-block:var(--s-6)}
.plancia::after{content:"";position:absolute;inset:0;z-index:-1;   /* la sola vignetta: niente graticola CSS */
  background:radial-gradient(120% 82% at 16% 0%,transparent 0,var(--mid-1) 84%)}
.plancia__inner{display:grid;grid-template-columns:minmax(0,7fr) minmax(0,5fr);
  gap:var(--s-6) var(--s-8);align-items:start}
.plancia__identity{grid-column:1;grid-row:1}
.plancia__facts{grid-column:1;grid-row:2;align-self:end;display:grid;
  grid-template-columns:repeat(2,minmax(0,1fr));gap:var(--s-4) var(--s-6);margin:0}
.plate{grid-column:2;grid-row:1/3;align-self:start;margin:0;display:grid;gap:var(--s-2)}
.plancia__suspension{grid-column:1/-1;grid-row:3;margin:0;display:grid;gap:var(--s-1);
  padding:var(--s-3) var(--s-4);border-inline-start:2px solid var(--err-dark);background:var(--mid-1)}
.plancia__crumbs{font-family:var(--f-mono);font-size:var(--t-caption);line-height:var(--t-caption-lh);
  letter-spacing:var(--track-folio);text-transform:uppercase;color:var(--on-dark-3);margin:0 0 var(--s-3)}
.plancia__title{font-family:var(--f-serif);font-size:var(--t-title);line-height:var(--t-title-lh);
  font-weight:300;color:var(--on-dark);margin:0 0 var(--s-2)}   /* color ESPLICITO: h1 eredita --ink da base.css */
.plancia__ref{font-family:var(--f-mono);font-size:var(--t-entry);line-height:var(--t-entry-lh);
  letter-spacing:var(--track-folio);color:var(--on-dark);
  font-variant-numeric:tabular-nums lining-nums;direction:ltr;unicode-bidi:isolate;margin:0}
.plancia__fact dt{font-family:var(--f-mono);font-size:var(--t-caption);line-height:var(--t-caption-lh);
  letter-spacing:var(--track-folio);text-transform:uppercase;color:var(--on-dark-3);margin:0 0 var(--s-1)}
.plancia__fact dd{margin:0;font-family:var(--f-sans);font-size:var(--t-ui);line-height:var(--t-ui-lh);
  color:var(--on-dark)}
.plancia__since{color:var(--on-dark-2)}
.plate__frame{display:block;inline-size:100%;block-size:auto;aspect-ratio:5/2;
  border:1px solid var(--hairline-dark-strong);background:var(--mid-1)}
.plate figcaption{font-family:var(--f-mono);font-size:var(--t-caption);line-height:var(--t-caption-lh);
  letter-spacing:var(--track-folio);color:var(--on-dark-3);direction:ltr;unicode-bidi:isolate}
.plate .terr__grid line{stroke:var(--on-dark);stroke-opacity:.14;stroke-width:1;vector-effect:non-scaling-stroke}
.plate .terr__ticks path{stroke:var(--terr-line);stroke-opacity:.85;stroke-width:1;fill:none;
  vector-effect:non-scaling-stroke}
.plate .terr__frontier line{stroke:var(--terr-line);stroke-width:1;vector-effect:non-scaling-stroke}
.plate .terr__frontier-axis{stroke-opacity:.95}
.plate .terr__frontier-edge{stroke-opacity:.45;stroke-dasharray:3 5}
.plate .terr__route{fill:none;stroke:var(--terr-line);stroke-width:1.5;vector-effect:non-scaling-stroke}
.plate .terr__halo{fill:var(--terr-line);fill-opacity:.14}
.plate .terr__dot{fill:var(--terr-line)}
@media (max-width:74.999rem){
  .plancia__inner{grid-template-columns:minmax(0,1fr)}
  .plancia__identity{grid-row:2} .plancia__facts{grid-row:3} .plancia__suspension{grid-row:4}
  .plate{grid-column:1;grid-row:1} .plate__frame{aspect-ratio:32/9}
}
@media (forced-colors:active){ .plate{display:none} }   /* una carta in due colori di sistema non dice nulla */
```

**Il misuratore, e una ridondanza tolta.** Il round 1 metteva il misuratore nell'identità **e** ripeteva
«0 sur 9 éléments complétés» nel fatto *Avancement*: lo stesso dato due volte a 40 px di distanza. Ora il
misuratore **è** il fatto:

```django
<div class="plancia__fact"><dt>{% translate "Avancement" %}</dt><dd>
  <span class="meter" data-done="{{ progress.done }}" role="img"
        aria-label="{% blocktranslate with done=progress.done total=progress.total %}{{ done }} sur {{ total }} éléments complétés{% endblocktranslate %}">
    <span class="meter__ticks" aria-hidden="true">
      {% for i in progress.range %}<span class="meter__notch{% if i <= progress.done %} is-done{% endif %}"></span>{% endfor %}
    </span>
    <span>{% blocktranslate with done=progress.done total=progress.total %}{{ done }} sur {{ total }} éléments complétés{% endblocktranslate %}</span>
  </span>
  {% if progress.overdue %}{% include "portal/partials/mark.html" with kind="overdue" label=overdue_label %}{% endif %}
</dd></div>
```

Il rapporto **non passa da una custom property**: la tacca porta `is-done` dal ciclo. È la risposta alla
Lacuna 1 — non «ecco come `--rail-progress` arriva al CSS», ma «nessun rapporto calcolato arriva al CSS».
`progress.range` è `range(1, total+1)`; se la vista non lo espone, `{% for i in ""|ljust:progress.total %}` con
`forloop.counter` fa lo stesso senza toccare la vista.

```css
.meter{display:flex;align-items:center;flex-wrap:wrap;gap:var(--s-2);margin:0;
  font-family:var(--f-mono);font-size:var(--t-folio);line-height:var(--t-folio-lh);
  letter-spacing:var(--track-folio);color:var(--on-dark-2)}
.meter__ticks{display:flex;gap:var(--s-1)}
.meter__notch{inline-size:var(--s-3);block-size:var(--s-1);background:transparent;
  border:1px solid var(--terr-line);                       /* 5,51:1 su --mid-2 */
  transform-origin:bottom}                                 /* deroga A5: la tacca si riempie dal basso */
.meter__notch.is-done{background:var(--terr-line)}
```

`--terr-line` e non `--accent-dark`: DS §1.3.2 assegna al teal del territorio «isoipse, **tacche**, rotta»,
e DS §1.3.1 riserva l'accento a link, CTA e focus. Il round 1 aveva sbagliato qui e il revisore non l'aveva visto.

### 4.7 Le altre regioni

**Prochaine étape** — foglio `--min-2` dentro il contenitore, `border-inline-start: 3px solid var(--accent)`
(DS §9.2), titolo `--t-entry` serif, marca del responsabile (`--seal` se autorità), la frase
« Cette étape ne dépend pas de vous. » quando `action.is_for_someone_else`, e il bottone primario a **48 px**.
**Correzione del round 1:** `templates/portal/partials/next_action.html` L36-40 **rende già**
`<a class="btn btn--primary btn--arrow">` quando `action.url` è valorizzato. Dire «oggi non c'è alcun bottone» era
vero del solo fascicolo del seed, e un implementatore che lo leggesse alla lettera aggiungerebbe una **seconda**
CTA. Il compito qui è la **forma** del foglio e i 48 px, non l'esistenza del bottone.

```css
.act{background:var(--min-0);padding-block:var(--s-6)}
.act__inner{background:var(--min-2);border:1px solid var(--hairline);
  border-inline-start:3px solid var(--accent);padding:var(--s-6);display:grid;gap:var(--s-3)}
.act__label{font-family:var(--f-mono);font-size:var(--t-folio);line-height:var(--t-folio-lh);
  letter-spacing:var(--track-folio);text-transform:uppercase;color:var(--ink-3);margin:0}
.act__text{font-family:var(--f-serif);font-size:var(--t-entry);line-height:var(--t-entry-lh);
  color:var(--ink);margin:0;max-inline-size:60ch}
.act__actor{display:flex;flex-wrap:wrap;align-items:center;gap:var(--s-2) var(--s-4);margin:0}
.act__gloss{font-family:var(--f-sans);font-size:var(--t-small);line-height:var(--t-small-lh);color:var(--ink-2)}
.act__cta .btn{min-block-size:48px;display:inline-flex;align-items:center;padding-inline:var(--s-6)}
```
Misurato: il bottone rende **117,1 × 48**.

**Checklist** — forma tabella o forma scheda secondo la larghezza della colonna (deroga A4).

```css
.work__main{display:grid;gap:var(--s-12);min-inline-size:0;
  container-type:inline-size;container-name:centre}
.tabwrap{display:none}
.tasks{display:block}
@container centre (min-width:40rem){ .tabwrap{display:block} .tasks{display:none} }

.tab{inline-size:100%;border-collapse:collapse;font-family:var(--f-sans);table-layout:fixed;
  font-variant-numeric:tabular-nums lining-nums}          /* oggi è `normal` (§2.6) */
.tab caption{position:absolute;inline-size:1px;block-size:1px;overflow:hidden;clip-path:inset(50%)}
.tab th,.tab td{text-align:start;vertical-align:top;padding:var(--s-3) var(--s-4) var(--s-3) 0;
  border-block-end:1px solid var(--hairline);font-weight:400}
.tab thead th{font-family:var(--f-mono);font-size:var(--t-folio);line-height:var(--t-folio-lh);
  letter-spacing:var(--track-folio);text-transform:uppercase;color:var(--ink-3);
  padding-block:0 var(--s-2);border-block-end:1px solid var(--hairline-strong)}
.tab tbody th{font-family:var(--f-serif);font-size:var(--t-body);line-height:var(--t-body-lh);color:var(--ink)}
.tab td{font-size:var(--t-small);line-height:var(--t-small-lh);color:var(--ink-2)}
.tab .c-state{inline-size:23%} .tab .c-owner{inline-size:27%}
.tab .c-due{inline-size:16%;font-family:var(--f-mono);font-size:var(--t-folio);
  letter-spacing:var(--track-folio);font-variant-numeric:tabular-nums lining-nums}

.task{display:grid;gap:var(--s-2);padding-block:var(--s-3);border-block-end:1px solid var(--hairline)}
.task__req{font-family:var(--f-serif);font-size:var(--t-body);line-height:var(--t-body-lh);color:var(--ink);
  margin:0;display:-webkit-box;-webkit-box-orient:vertical;-webkit-line-clamp:3;overflow:hidden}
.task__meta{display:flex;flex-wrap:wrap;align-items:center;gap:var(--s-2) var(--s-4);margin:0}
.task__owner{display:inline-flex;align-items:center;gap:var(--s-2);font-family:var(--f-sans);
  font-size:var(--t-small);line-height:var(--t-small-lh);color:var(--ink-2)}
.task__due{font-family:var(--f-mono);font-size:var(--t-folio);line-height:var(--t-folio-lh);
  letter-spacing:var(--track-folio);color:var(--ink-2);font-variant-numeric:tabular-nums lining-nums}
.task__duelabel{color:var(--ink-3)}
```

La tripletta `-webkit-` è obbligatoria e verificata (Lacuna 14). Il prefisso `data-label` sopravvive **solo**
su ÉCHÉANCE, come `.task__duelabel`: la marca dice la propria parola, il responsabile è una frase, l'elemento è
l'intestazione di riga. Per `—` si aggiunge `<span class="visually-hidden">{% translate "Aucune échéance" %}</span>`.
Misurato a 390: scheda **118–170 px** contro le **293–341** di oggi; la regione passa da **2 891** a **1 290 px**
(**−55,4 %**). Nessun filtro client-side: il round 1 ne proponeva uno «progressivo»; è stato tolto perché era
l'unico pezzo di JavaScript della pagina e il suo solo scopo era nascondere righe che hanno conseguenze legali.

**Documenti** — nome in mono, tipo, marca dello stato scanner, azione. Stato vuoto secondo DS §9.6: una hairline,
il glifo arco+gradini a tratto 24 px, la frase che dice chi riempie e quando, e l'azione come **bottone terziario
a 44 px** al posto del link 138,45 × 18.

**Pré-évaluation — nella colonna CENTRALE, non nell'inspector.** Il MUST-FIX 8 ha ragione e il rimedio giusto è
il secondo che propone: i fondamenti sono la base giuridica di una pre-valutazione e non stanno dietro una
disclosure né dentro una colonna di 320 px. Il blocco intero (esito, motivazione, jeu de règles, data, **tutti** i
fondamenti, conteggio dei mancanti, link al dettaglio) vive nella colonna centrale, misurato **770 px** a 1440.
`.outcome__kind` scende da 52 px a `--t-entry` 22/28. Nessun `<details>`.

**Inspector** (`<aside class="portal__inspector">`, 320 px, `position: sticky`) — messaggi, scadenze, conto.
La grammatica propria che la revisione chiedeva: **spina a capello** continua sul lato di lettura, e un folio in
mono numerato per blocco (`01 · Communications`, `02 · Échéances`, `03 · Compte`), cioè il registro applicato in
verticale. Livello 3 del DS §2 → `--shadow-3`, statica.

```css
.work__inspector{display:grid;gap:var(--s-6);position:sticky;inset-block-start:var(--s-16);
  border-inline-start:1px solid var(--hairline);padding-inline-start:var(--s-6)}
.ibox{background:var(--min-3);box-shadow:var(--shadow-3);padding:var(--s-4)}
.block__folio{font-family:var(--f-mono);font-size:var(--t-folio);line-height:var(--t-folio-lh);
  letter-spacing:var(--track-folio);text-transform:uppercase;color:var(--ink-3);
  margin:0 0 var(--s-2);padding-block-end:var(--s-2);border-block-end:1px solid var(--hairline)}
@media (max-width:74.999rem){
  .work__inspector{grid-column:1/-1;position:static;border-inline-start:0;padding-inline-start:0;
    border-block-start:1px solid var(--hairline);padding-block-start:var(--s-6);
    grid-template-columns:repeat(2,minmax(0,1fr))}
}
@media (max-width:63.999rem){
  .work{grid-template-columns:minmax(0,1fr)}
  .work__nav ul{display:flex;overflow-x:auto;gap:var(--s-4)}     /* DS §9.1: striscia 36 px */
  .work__nav a{white-space:nowrap;min-block-size:36px}
  .work__inspector{grid-template-columns:minmax(0,1fr)}
}
```

`grep box-shadow` sul CSS candidato dà **due** occorrenze, entrambe di ruolo: `--shadow-3` sull'inspector
(livello 3) e `--shadow-2` sull'hover di riga (livello 2, solo in hover). Nessun quinto ruolo, nessuna ombra
animata.

### 4.8 Le due frasi prescritte, verbatim e localizzate

Il MUST-FIX 9 ha ragione: ce ne sono **due distinte**, e il round 1 non nominava né l'una né l'altra.

**(A) La frase di DS §9.7** non è una stringa di template: arriva **dentro `assessment.rationale`**, perché è
parte del testo d'esito seminato in `apps/orientation/seeds.py` (L224-229 per `individual_analysis`, e l'omologa
per ogni altro esito):

> «Cette pré-évaluation a un caractère purement informatif : toute décision relève exclusivement des autorités
> compétentes. Prochaines étapes à caractère informatif : … »

*Dove va:* dentro `.assess__why`, nella colonna centrale, come testo pieno. **Mai** troncata, **mai** con
`line-clamp`, **mai** dentro una disclosure. `.assess__why` non ha regola di troncamento — è l'unico blocco di
prosa della pagina che ne è esplicitamente privo.

**(B) La frase di `dashboard.html` L185**, resa nel ramo `{% else %}` di `assessment.sources`:

> «Cette pré-évaluation ne s'appuie sur aucune règle actuellement en vigueur dans la plateforme : aucune source
> ne lui est donc rattachée. Elle reste une orientation, jamais une décision.»

*Dove va:* `.assess__lock`, subito sotto `.assess__note`, con filetto `border-inline-start: 2px solid
var(--hairline-strong)` — il filetto della citazione, non quello di uno stato. Resta nel ramo `{% else %}`:
quando i fondamenti esistono si mostrano i fondamenti, quando non esistono si dice perché.

Nessuna delle due è riscritta, riformattata o abbreviata. `.assess__lock` e `.assess__why` sono le uniche due
regole della spec con `max-inline-size: 65ch` e nessun `overflow` dichiarato.

---

## 5. MOTO — voci per `MOTION_SYSTEM.md` §6

**Questa pagina non introduce JavaScript.** Zero byte. Nessun ascoltatore di scroll, nessun
`IntersectionObserver`, nessun bundle nuovo. Tutto il moto è CSS dentro
`@media (prefers-reduced-motion: no-preference)`; fuori da quel blocco il valore a riposo **è** lo stato finale.
Ciò è possibile perché la lastra è nella prima schermata a **tutti e quattro** i viewport misurati (bordo
superiore a `y = 80`, piega ≥ 844): il tracciato non può eseguirsi fuori dal viewport, che è la condizione di
MOTION §7.

| Nome | Funzione | Innesco | Durata | Curva | Proprietà | Stato ridotto | Budget |
|---|---|---|---|---|---|---|---|
| `plate-route-draw` | ORIENTAMENTO | caricamento, **una volta** | `var(--motion-draw)` = **900 ms**; il tratto italiano con `animation-delay: 60ms` | `--ease-out` | `stroke-dashoffset` 1 → 0 su due `<path pathLength="1">` | `stroke-dashoffset: 0` a riposo: la rotta è **intera e ferma** | 2 path; ridipintura del solo tratto in una scatola 503×203; da provare nel pannello Performance a CPU 4× |
| `meter-notch-fill` | STATO | caricamento, una volta | `var(--motion-fast)` 180 ms per tacca, `animation-delay` scaglionato **40 ms** via `:nth-child` | `--ease-out` | `transform: scaleY(0→1)`, `transform-origin: bottom` (deroga **A5**) | tacche già piene | ≤ 9 elementi compositi, 0 layout; **non si esegue** se `done == 0` |
| `mark-state-change` | STATO | ritorno del server dopo un'azione (la parola cambia) | `var(--motion-base)` 240 ms | `--ease-standard` | `color`, `background-color`, `border-color` | parola aggiornata senza transizione | mai in loop, nessuna scala, nessun rimbalzo |
| `row-hover` | FEEDBACK | puntatore, solo `@media (hover:hover)` | `var(--motion-fast)` in / `var(--motion-instant)` out | `--ease-out` / `--ease-in` | **solo** `background-color` in transizione; `--shadow-2` è uno **scambio discreto** | identico (l'hover non è moto essenziale) | 1 paint su 1 riga |
| *(focus)* | ORIENTAMENTO | tastiera | istantaneo | — | `outline` di sistema | identico | — |

```css
/* Il tracciato. Fuori dal blocco: rotta intera, ferma. */
.plate .terr__route{stroke-dasharray:1;stroke-dashoffset:0}
@media (prefers-reduced-motion:no-preference){
  .plate .terr__route{animation:plate-route-draw var(--motion-draw) var(--ease-out) both}
  .plate .terr__route--it{animation-delay:60ms}
  @keyframes plate-route-draw{from{stroke-dashoffset:1}to{stroke-dashoffset:0}}
}

/* Il misuratore. */
.meter__notch{transform:scaleY(1)}
@media (prefers-reduced-motion:no-preference){
  .meter[data-done]:not([data-done="0"]) .meter__notch.is-done{
    animation:meter-notch-fill var(--motion-fast) var(--ease-out) both}
  .meter__notch:nth-child(2){animation-delay:40ms}   /* … fino a :nth-child(9){320ms} */
  @keyframes meter-notch-fill{from{transform:scaleY(0)}to{transform:scaleY(1)}}
}

/* L'hover di riga. --shadow-2 NON è in transition-property: è uno scambio discreto. */
.tab tbody tr,.task{background-color:transparent}
@media (hover:hover) and (prefers-reduced-motion:no-preference){
  .tab tbody tr,.task{transition:background-color var(--motion-instant) var(--ease-in)}
  .tab tbody tr:hover,.task:hover{transition-duration:var(--motion-fast);transition-timing-function:var(--ease-out)}
}
@media (hover:hover){
  .tab tbody tr:hover,.task:hover{background-color:var(--min-2);box-shadow:var(--shadow-2)}
}

/* Il cambio di stato della marca. */
@media (prefers-reduced-motion:no-preference){
  .mark{transition:color var(--motion-base) var(--ease-standard),
                   background-color var(--motion-base) var(--ease-standard),
                   border-color var(--motion-base) var(--ease-standard)}
}
```

Numeri usati: **120 · 180 · 240 · 900** — i quattro token e la traccia, e **nessun altro**.
Scaglionamenti: **40 ms** e **60 ms**, dentro la banda 40–60 che MOTION §1 ammette esplicitamente.
Curve: `--ease-out`, `--ease-in`, `--ease-standard` — tre, e `grep -c cubic-bezier` sul CSS candidato dà **0**,
perché sono tutte lette dai token.
Molle: **nessuna** (l'accordion a molla del round 1 è sparito insieme al pannello JavaScript).
Dotazione RICH: **loop ambientali 0 · oggetti indicizzati allo scroll 0 · `backdrop-filter` 0**. Riconciliato con
`platform-shell.md`, che usa una sentinella `IntersectionObserver` e un cambio di terreno discreto, non un
oggetto legato allo scroll, e che esclude `backdrop-filter` dalla barra.

---

## 6. ACCESSIBILITÀ E RTL

**Cosa cambia, e cosa è stato verificato in browser.**

- «Étape n sur N» è **testo visibile** (oggi non esiste); `aria-current="step"` sul segmento corrente (oggi `null`
  su tutti e sette); «Vous êtes ici» è testo, non un pittogramma.
- La frontiera è `<li role="presentation">`. **Verificato**: 8 `<li>` nel DOM, **7 `listitem` nell'albero di
  accessibilità**, identico in `fr` e in `ar`. La frase «MA → IT» resta leggibile dallo screen reader come testo
  fra gli elementi, che è ciò che è.
- Mai il solo colore: parola + glifo + forma del riempimento + trama, quattro canali su ogni stato.
- Bersagli (WCAG 2.2 AA, 2.5.8 ≥ 24×24): voci del rail di navigazione **44 px** (misurato), bottone primario
  **48 px** (misurato 117,1×48), azione dello stato vuoto 44 px, marche non interattive 28 px (non sono bersagli).
  Il minimo di oggi, 138,45 × 18, sparisce.
- Focus: `outline: 2px solid var(--accent-ring)` + `outline-offset: 2px` su carta (`--accent-ring` **3,44** su
  `--min-1`, **3,70** su `--min-0`); `--accent-dark` (**9,09** su `--mid-2`) sul capitolo scuro; più
  `:root{ scroll-padding-block-start: calc(var(--chrome-masthead) + var(--s-2)) }` perché un ancoraggio a fuoco
  non finisca sotto la barra appiccicosa.
- `forced-colors: active`: `forced-color-adjust: none` **solo** su `.rail__bar` (DS §11, le trame restano);
  la marca torna `Canvas`/`CanvasText` con bordo 1 px e glifo `CanvasText`; la lastra si nasconde.
- `prefers-reduced-motion`: ogni `@keyframes` e ogni `transition` è dentro
  `@media (prefers-reduced-motion: no-preference)`; il valore a riposo è lo stato finale. Misura da preservare:
  elementi a `opacity: 0` con moto ridotto = **0**. La rotta è intera; le tacche sono piene; le marche hanno il
  loro colore; nessun contenuto è nascosto o diverso.

**RTL — verificato a 1440 in `dir="rtl"`.** Solo proprietà logiche. Il rail avanza da destra: il segmento 01 è a
`x = 1 189`, il 07 a `x = 100`. Il filetto della marca passa al lato destro
(`border-left-width: 0px`, `border-right-width: 2px`). `scrollWidth > clientWidth` = `false`.
Correzione del difetto misurato in §2: `.rail__num` e `.plancia__ref` forzano `font-family: var(--f-mono)`,
`font-variant-numeric: tabular-nums lining-nums`, `direction: ltr`, `unicode-bidi: isolate` — **verificato**:
in `ar` entrambi rendono `"Fira Mono"` e non più `Noto Naskh Arabic`.
`:lang(ar)` su `.mark`, `.rail__owner`, `.rail__h`, `.plancia__crumbs`: `text-transform: none`, `letter-spacing: 0`.
Si specchia **solo** il glifo di frontiera (`[dir="rtl"] .rail__frontier svg{transform:scaleX(-1)}`); **non** si
specchiano numeri, riferimento, misuratore e **lastra** (§4.6).

**Passaggio su `forbidden.py`, eseguito.** Ho fatto girare `apps.cms.forbidden.scan()` su **tutte e 25** le
stringhe nuove o riposizionate di questa spec — incluse le etichette invisibili, le `aria-label` e le didascalie:
«Étape n sur N», «Vous êtes ici», «Terminée», «Étape actuelle», «À venir», «Frontière MA → IT», «MA → IT»,
«Les segments marquent des étapes, non des durées.», «Responsable à préciser — à titre indicatif»,
«33.97° N · 6.85° W → 45.41° N · 11.88° E», «Voir mon parcours en détail», «Aucune échéance», «Jeu de règles»,
«Fondements», «Tableau de bord», … → **zero violazioni**. Il claim inglese e lo slogan della porta non compaiono:
`BRAND_ASSETS.md` §1 resta rispettato — l'immagine resta, le parole no.

**HUMAN_QA_REQUIRED.**
(a) Lettura NVDA e VoiceOver dell'ordine del rail in FR e AR, con e senza JS.
(b) Le due frasi bloccate del §4.8 a 320 px e a 200 % di zoom: nessun troncamento, nessuna disclosure.
(c) Approvazione delle **due** frasi nuove: « Les segments marquent des étapes, non des durées. » e
« Voir mon parcours en détail ». Nessun'altra prosa nuova è introdotta.
(d) `territory_plate`: conferma che non costituisca un'affermazione su un confine (§8.8) e che la scelta di **non**
specchiarla in `ar` sia quella voluta.
(e) Difetto di contenuto già misurato, fuori da questa spec: su `/it/` e `/ar/` il corpo di «Prochaine étape» e i
requisiti della checklist escono in francese.
(f) Trame al 200 % di zoom, a DPR 1 / 1,5 / 2 / 3, e in scala di grigi.

---

## 7. PRESTAZIONI — derivate, non asserite

**Byte.** CSS: 18 092 raw / **3 722 gzip** su tre file (tabella in §4.1), misurato con `gzip -9`. Lastra SVG in
linea: 2 961 raw / **709 gzip**, dentro l'HTML, **zero richieste**. Sprite dei glifi: già servito
(`static/img/icons.svg`), **+9 simboli**. **JavaScript nuovo: 0 byte** — il totale della pagina resta il chunk
condiviso di Motion (26 KB) che `shell.js` carica già, ben sotto i 45 KB. Immagini raster: **nessuna**, quindi
0 KB per viewport contro un budget di 120.
`register.css` non si cancella in questa fase (regola del ponte): netto **+3,7 KB gzip**.

**Paint e layout.** Nessun `filter`, nessuna ombra animata, nessun `backdrop-filter`, nessuna animazione di
`width`/`height`/`top`/`left`/`background-position`. `grep box-shadow` = 2 occorrenze, entrambe di ruolo.
L'unico costo di ridipintura è il tratto della rotta durante i 900 ms del tracciato: due path in una scatola di
503×203, da verificare nel pannello Performance a CPU 4× e a viewport 390 — la stessa prova che l'arco dell'hero
già supera.

**Altezze.** Il confronto onesto è sul **contenuto fra la barra e il piè di pagina**, cioè su `<main>`, perché la
barra e il piè di pagina non appartengono a questa superficie: la barra è di `platform-shell.md`, il piè di pagina
di `base_portal.html`, e questa spec non li tocca. Tutte le cifre «prima» sono misurate sul server vivo (sessione
QA, fascicolo `E12273C5DF`, 9 voci); tutte le cifre «dopo» sul prototipo con i font reali sulla stessa origine.

| Regione di `<main>` | 1440 prima → dopo | 1280 prima → dopo | 768 prima → dopo | 390 prima → dopo |
|---|---|---|---|---|
| briciole (riga propria) | 60 → *dentro la plancia* | 60 → — | 60 → — | 60 → — |
| intestazione di pagina | 133 → *dentro la plancia* | 133 → — | 133 → — | 133 → — |
| banda del fascicolo | 117 → — | 189 → — | 257 → — | 417 → — |
| **plancia** (briciole + H1 + riferimento + 4 fatti + lastra) | 48+60+133+117 → **325** | 48+60+133+189 → **325** | 48+60+133+257 → **568,5** | 48+60+133+417 → **493,4** |
| prossima azione (+ stacco) | 24+173 → **283** | 24+173 → **283** | 24+173 → **283** | 24+233 → **339** |
| banda del rail | *non esiste* → **355** | *non esiste* → **365** | *non esiste* → **710** | *non esiste* → **1 083** |
| spazio di lavoro | 3 602 → **2 334** | 3 696 → **2 380** | 4 156 → **2 809** | 6 801 → **3 571** |
| **`<main>`** | **4 157 → 3 297** (**−20,7 %**) | **4 323 → 3 353** (**−22,4 %**) | **4 851 → 4 370,5** (**−9,9 %**) | **7 716 → 5 486,4** (**−28,9 %**) |

Le due colonne quadrano. **Prima**, la somma delle regioni misurate ricade esattamente sul documento: a 1440,
62 (barra) + 60 + 133 + 48 + 117 + 24 + 173 + 3 602 + 77 (piè di pagina) = **4 296**; a 390, 161 + 60 + 133 + 48 +
417 + 24 + 233 + 6 801 + 117 = **7 994**. **Dopo**, 325 + 283 + 355 + 2 334 = **3 297** = l'altezza di `<main>`
misurata nel prototipo; 493,4 + 339 + 1 083 + 3 571 = **5 486,4**.

**Documento intero, proiettato** con la barra che `platform-shell.md` fissa (`--shell-bar-h: 56px`, **52 px** sotto
768, L309/L321) e il piè di pagina di oggi misurato (77 px ≥ 768, 117 px a 390):

| viewport | oggi | V3 (proiettato) | Δ |
|---|---:|---:|---|
| 1440×900 | 4 296 | 56 + 3 297 + 77 = **3 430** | **−20,2 %** |
| 1280×900 | 4 462 | 56 + 3 353 + 77 = **3 486** | **−21,9 %** |
| 768×1024 | 4 990 | 56 + 4 370,5 + 77 = **4 503,5** | **−9,7 %** |
| 390×844 | 7 994 | 52 + 5 486,4 + 117 = **5 655,4** | **−29,3 %** |

Il caso 768 va detto per intero: **−9,7 %** soltanto, perché la pagina guadagna una banda di rail di **710 px**
che oggi non esiste affatto, più una lastra di 219,5. Il contenuto preesistente si è contratto di circa 1 410 px e
la struttura nuova ne ha aggiunti circa 930. Il round 1 prometteva −42 % e −49 %: erano cifre non calcolate, e il
revisore ha ragione a dire che almeno una sbagliava di circa il doppio.

**La regione che il committente ha nominato.** Checklist a 390: **2 891 → 1 290 px**, cioè **−55,4 %**;
riga per riga da **293–341 px** a **118–170 px**.

**La prima schermata — il numero che conta davvero.** Posizione in pagina del bordo inferiore del bottone primario.
Le cifre «misurato» vengono dal prototipo, che usa una barra da 56 px; la colonna «con la barra V3» le riporta
sulla barra che `platform-shell.md` fissa (56 ≥ 768, 52 < 768).

| viewport | piega | misurato (barra 56) | con la barra V3 | in schermata? | oggi |
|---|---:|---:|---:|---|---|
| 1440×900 | 900 | 615 | **615** | sì, con 285 px di margine | `.next-action` a y 444; nel seed non c'è CTA |
| 1280×900 | 900 | 615 | **615** | sì, con 285 px | y 516 |
| 768×1024 | 1 024 | 859 | **859** | sì, con 165 px | y 584 |
| 390×844 | 844 | 839 | **835** | **sì, con 9 px** | `.next-action` comincia a **843**: se ne vede **un pixel** |

A 390 la prima schermata porta ora: lastra, briciole, H1, riferimento, i quattro fatti con il misuratore a tacche,
il testo della prossima azione, il responsabile e il bottone da 48 px. Oggi porta **zero** elementi azionabili.

**Dipendenza dichiarata, e misurata.** Quei 9 px a 390 dipendono da `platform-shell.md`. La barra **di oggi** è
alta **161 px** a 390 (si dispone su tre righe: misurato su `body > .portal-bar`) contro i 62 px di 1440. Se la
spec della shell non atterra prima di questa, la CTA a 390 cade a y ≈ **944**, cioè **100 px sotto la piega**, e
il criterio d'accettazione sul telefono torna a fallire. È una dipendenza d'ordine, non un rischio di disegno, ed
è nel §8.

---

## 8. RISCHI

1. **La plancia legge come un header fintech.** Difesa: nessun gradiente sul testo, nessun bagliore, raggio 0 sui
   capitoli; sul capitolo mezzanotte `--accent-dark` **non compare affatto** (zero occorrenze: il riferimento è
   `--on-dark`, le tacche sono `--terr-line`, la rotta è `--terr-line`); la lastra è una graticola con una rotta,
   mai una fotografia di persone. Prova: uno screenshot in scala di grigi deve restare completamente leggibile.
   Il round 1 affermava «l'unico colore saturo è `--accent-dark` su **un** elemento» mentre ne aveva quattro; ora
   l'affermazione è zero, ed è verificabile con un `grep`.
2. **La lastra legge come un grafico di crescita.** Il rischio si è **avverato** nella prima resa di questo round:
   una curva monotona ascendente su una griglia regolare è un grafico. Rimediato: la rotta ondula (sale, scende,
   risale), attraversa una **meridiana di frontiera** con il suo canale tratteggiato, e le tacche della graticola
   più le coordinate in didascalia la collocano su una carta. Stessa difesa per il rail: segmenti di larghezza
   **uguale** (`1fr`), mai dimensionati sulla durata, mai in salita, con la didascalia esplicita.
3. **Moiré delle trame** a 200 % di zoom o a DPR 1,5. Difesa: passo ≥ 4 px (il più fitto è 4 px; l'autorità è a 7),
   tratto 1 px, `background-size` in px e mai in percentuale, `vector-effect: non-scaling-stroke` sulla lastra.
   QA a 100/150/200/300 % e a DPR 1/1,5/2/3.
4. **Arcobaleno di marche.** Difesa: al massimo **tre** varianti nello stesso blocco; la checklist ne usa due
   (`--todo`, `--overdue`); `--seal` solo accanto a un'autorità o al jeu de règles.
5. **Il bronzo diventa un motivo decorativo** (`--owner-authority` accanto a `--seal`), vietato da DS §1.3.3.
   Difesa: il bronzo compare al massimo **due volte** per schermata — il segmento dell'autorità e il sigillo del
   jeu de règles — e mai come fondo pieno.
6. **`data-owner` resta `indicative` per sempre** perché la vista non fornisce mai `owner_key`, e il rail mostra
   sette trame identiche. Difesa: la dicitura «à titre indicatif» è **testo nel flusso**, non rimovibile via CSS;
   un test conta le trame distinte e segnala quando sono una sola. È il rischio più concreto della spec ed è
   dichiarato come tale, non risolto.
7. **La lastra letta come un'affermazione su un confine.** Difesa: nessuna costa nominata, nessun riempimento di
   stato, nessuna bandiera; graticola, una meridiana e due tratti astratti; approvazione umana obbligatoria.
8. **Due oggetti di stato nel prodotto** finché `badges.md` non atterra: `.mark` qui, `.state` sulle altre 15
   superfici. È il costo dichiarato della deroga A2; la spec non tocca `register.css`.
9. **Fascicolo a zero avanzamento** (`0 sur 9`): misuratore vuoto e rail senza segmenti completati possono
   leggersi come «rotto». Difesa: `meter-notch-fill` non si esegue quando `done == 0` (non c'è nulla da
   raccontare), e la frase in parole accompagna sempre le tacche — testo da far approvare, mai inventato nel CSS.
10. **`@container` e i browser senza supporto.** Difesa: la regola di partenza è la forma a **scheda**, che
    funziona a ogni larghezza; un browser senza supporto per le container query ottiene sempre le schede, mai una
    tabella schiacciata. Il degrado è verso la forma più robusta, non verso quella più fragile.
11. **Dipendenza d'ordine da `platform-shell.md`.** Il guadagno sulla prima schermata a 390 è di **9 px**, e
    poggia sulla barra da 52 px che quella spec fissa (L321). La barra di oggi a 390 è alta **161 px** (misurata):
    con quella, la CTA cade **100 px sotto la piega** e §7 non regge. Difesa: nessuna, se non l'ordine di
    atterraggio — questa superficie va implementata **dopo** la shell, e il test di piega a 390 va scritto come
    asserzione (`bottom della CTA ≤ innerHeight`) perché la regressione sia rumorosa e non silenziosa.
12. **I due filtri di template.** `current_index` e `owner_glyph` sono l'unico codice Python che questa spec
    aggiunge. Difesa: leggono il contratto e non lo estendono, vivono accanto a `svg_icon` in
    `apps/core/templatetags/ile_core.py`, e `current_index` restituisce **0** quando nessun passo è corrente —
    caso in cui il rail rende sette segmenti `todo`, la riga «Étape n sur N» non si stampa e nulla si rompe.
