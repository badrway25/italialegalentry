# TRANSIZIONI E CAMBI DI STATO — «la soglia»

Revisione 2. Superficie: gli scambi dentro la pagina (passo del wizard, `<details>`, riga di
checklist, sezione sostituita) e le transizioni fra pagine **dello stesso compito** (paginazione,
ricerca, riga di registro → dettaglio, ritorno). Vincolanti: `DESIGN_SYSTEM_V2.md`,
`MOTION_SYSTEM.md`, CSP `script-src 'self'` / `style-src 'self'`.

**Come sono state prese le misure di questa revisione.** Chromium 153.0.8010.12 headless
(Playwright del `.venv`), viewport 1440×900 e 390×844, contro il server vivo `:8771`. Dove serviva
provare il CSS candidato, il foglio è stato servito su un URL della **stessa origine**
(`/__cand.css`, via intercettazione di rotta) e iniettato in una **copia** della risposta HTML:
nessun file del repository è stato toccato. Le tracce di layout/paint vengono da
`Tracing.start` CDP con la categoria `disabled-by-default-devtools.timeline`, con una traccia di
**riposo** come riferimento. Tutti i numeri qui sotto sono stati ricalcolati in questa tornata:
quelli della revisione 1 che non reggevano sono corretti e segnati **[RIMISURATO]**.

---

## 0. RICHIESTE DI EMENDAMENTO

Tre, numerate, con clausola, ragione e costo. Tutto il resto del documento sta dentro i documenti
vincolanti senza deroga.

**EMENDAMENTO 1 — MOTION_SYSTEM § 2, riga «`height` solo via misura + `transform`/`clip-path`».**
*Richiesta*: ammettere `block-size: 0 → auto` su `::details-content` quando `interpolate-size:
allow-keywords` è dichiarato **sull'elemento `<details>`**, mai su `:root`.
*Ragione*: l'alternativa conforme è misurare l'altezza in JavaScript e animarla con una molla. Su
`<details>` costa un modulo, un `ResizeObserver` e una riscrittura della gestione di `[open]`, per
ottenere lo stesso risultato che il motore calcola da solo su un sottoalbero contenuto; e il
pannello della FAQ contiene testo di lunghezza sconosciuta, quindi la misura andrebbe rifatta a
ogni cambio di larghezza e di lingua.
*Costo, misurato*: **14 eventi `Layout` in 240 ms, uno per fotogramma animato**, confinati al
sottoalbero di un `<details>` (traccia CDP sulla FAQ viva: Layout a 20,3 · 35,7 · 51,3 · 69,1 ·
85,2 · 100,9 · 118,8 · 135,6 · 151,3 · 168,9 · 184,3 · 203,4 · 220,2 · 234,6 ms dopo il primo
evento). È l'unica voce di questa superficie che paga layout per fotogramma; tutte le altre sono a
**0 Layout e 0 Paint oltre il primo fotogramma**, misurato (§ 7).
*Limite che accetto*: un solo `<details>` in transizione per volta; pannello ≤ 2 altezze di
viewport; la regola non si applica a nessun altro elemento del prodotto — `:root` resta
`interpolate-size: numeric-only`, **verificato sulla pagina viva**: `getComputedStyle(:root)
.interpolateSize === "numeric-only"` mentre `getComputedStyle('.faq-item').interpolateSize ===
"allow-keywords"`.

**EMENDAMENTO 2 — DESIGN_SYSTEM_V2 § 10, «Stati: … loading con spinner a tratto + testo» contro
MOTION_SYSTEM § 4, «STANDARD, DENSE e LEGAL: nessun oggetto vivo».**
*Richiesta*: sulle pagine STANDARD e DENSE il bottone in attesa **non** porta spinner. I due
documenti si contraddicono e uno spinner è per definizione un loop.
*Ragione*: la pagina della domanda è STANDARD. Un loop lì è vietato dal § 4, e un loop da 1 s è
anche la cosa meno onesta da mostrare per un'attesa che ho misurato in **20–59 ms in locale**
(tre POST consecutivi sul questionario vivo: 59, 20, 22 ms).
*Costo*: fra 0 e 400 ms l'utente non vede un indicatore di attività; vede che i due bottoni sono
disattivati e che la risposta scelta ha preso il **timbro di commit** (§ 4.4). Oltre 400 ms parla
la live region. Su rete lenta il segnale è dunque testuale e non grafico.
*Alternativa scartata*: uno spinner a tratto fermo sotto reduced-motion sarebbe uno spinner che
non gira, cioè un glifo senza significato.

**EMENDAMENTO 3 — MOTION_SYSTEM § 1, «Nessun altro numero».**
*Richiesta*: mettere a verbale che § 1 governa le **durate animate**, e che due soglie non animate
possono esistere: **400 ms** prima che la live region dica «Enregistrement…», e **10 s** di
validità della marca del TIMBRO.
*Ragione*: nessuna delle due muove un pixel. La prima è una soglia di parola, scelta perché
sopra la latenza locale misurata (59 ms al massimo) e sotto il secondo in cui una persona comincia
a dubitare di avere premuto; la seconda è una finestra di validità di un dato in `sessionStorage`.
*Costo*: due numeri in più nel documento, entrambi dichiarati qui e ripetuti nel catalogo § 5 con
la dicitura «soglia, non durata».

---

## 1. STATO ATTUALE — riverificato

I sette rilievi della revisione 1 sono stati rimisurati sul server vivo. Reggono tutti; due numeri
erano sbagliati e sono corretti.

**1.1 Il wizard è un ricaricamento, e gli attributi HTMX sono markup morto.** HTMX non è caricato
su nessuna pagina. Gli attributi `hx-*` su `templates/orientation/_step.html:13` sono
**quattro** — `hx-post`, `hx-target`, `hx-swap`, `hx-push-url` — non cinque. **[RIMISURATO]**: la
revisione 1 scriveva «cinque» e la revisione indipendente ha ripetuto il numero; l'elenco in
entrambi i documenti ne conteneva quattro. Misura: `[...form.attributes].map(a=>a.name).filter(n
=>n.startsWith('hx-'))` → `["hx-post","hx-target","hx-swap","hx-push-url"]`.

**1.2 Dopo l'invio il fuoco cade su `<body>`.** Rimisurato con un invio nativo sul questionario
vivo: `document.activeElement` = `BODY`, id vuoto.

**1.3 Zero live region sulla pagina del passo.** `document.querySelectorAll('[aria-live],
[role=status],[role=alert]').length` → **0**.

**1.4 La barra di progressione anima `inline-size` ed è dipinta col navy del marchio.** Computed
sul figlio di `[role=progressbar]`: `transition-property: inline-size`,
`background-color: rgb(15, 37, 71)` = `--brand-navy` `#0F2547`. Larghezza del riempimento alla
prima domanda: **0 px**. Le classi `.wizard__progress-fill--*` sono **21**, confermato.

**1.5 Il questionario attivo ha `max_steps = 3`, non 8.** **[RIMISURATO]**: `aria-valuetext` =
«Question 1 sur 3 au maximum». La revisione 1 citava come esempio «Question 3 sur 8 au maximum ·
35 %»: era inventato. Il rail è dimensionato qui sotto per 3 **e** per 8, perché il jeu de règles
cambia.

**1.6 L'accordion apre in un fotogramma.** Confermato, e ora misurato anche *con* il foglio
candidato: senza, due altezze distinte; con, **16 altezze distinte** fra 77 px e 205 px sulla
stessa `.faq-item` viva (37 campioni `requestAnimationFrame`).

**1.7 Tab, accordion e stepper sono codice morto.** `templates/components/tabs.html` e
`stepper.html` non sono inclusi da nessun template; `data-accordion="single"` non compare in
nessuna pagina. `initTabs` **47 righe / 1 786 B**, `initSteppers` **41 / 1 414 B**,
`initAccordions` **13 / 388 B** = **101 righe, 3 588 B** di sorgente che gira su zero elementi a
ogni caricamento. **[RIMISURATO]**: la revisione 1 diceva «≈ 110 righe, ≈ 1,1 KB gzip»; sono 101
righe e **802 B gzip** (main.js 5 259 → 4 457 B gzip).

**1.8 Zero View Transitions, e il prodotto non ha nemmeno un ordinamento.** `grep -rn "?sort="
templates/` → **0 risultati**. La § 4.7 della revisione 1 specificava un FLIP per il cambio di
`?sort=`: animava un'interazione che nel prodotto **non esiste**. Eliminata, e sostituita con la
sola cosa che esiste davvero: una riga di registro che apre un dettaglio (`cases/index.html:31`).

**1.9 Il fascicolo cambia stato con `<select>` nudo + ricaricamento**, e il server risponde con
`messages.success(request, _("La ligne a été mise à jour."))` + `redirect`
(`apps/cases/views.py:183-186`). **Esiste dunque già un annuncio all'arrivo**, dentro
`<div class="container messages" role="status" aria-live="polite">` di `base.html:59`. Quello che
non esiste è l'informazione su **quale** riga.

**1.10 L'anello di fuoco del prodotto è dipinto col navy del marchio.**
`--focus-ring-color: var(--navy)` (`_legacy-tokens.css:162`) → `--navy: var(--brand-navy)`
(`v2/bridge.css:31`) → `#0F2547`, **13,754:1** su `--min-0`. Passa il contrasto e viola
DESIGN_SYSTEM_V2 § 1.3 regole 1 e 4. Non è la mia superficie e non lo cambio qui; le tabelle di
stato di questo documento sono scritte su `--accent-ring` (**3,704:1**, ricalcolato) e valgono
quando quel token sarà ripuntato. Lo segnalo perché ogni stato di fuoco che specifico eredita
quella regola.

---

## 2. RISPOSTA ALLA REVISIONE

Nessun punto resta senza risposta. **FATTO** = il difetto non c'è più e si vede dove.
**CONTESTATO** = con il numero che ho misurato.

### 2.1 MUST-FIX

| # | Esito | Dove |
|---|---|---|
| 1 | **FATTO** — la contraddizione è risolta eliminando il widget: `initTabs`/`initSteppers`/`initAccordions` si cancellano, nessuna tab entra in servizio, e il contratto che varrebbe se mai una entrasse è scritto per esteso | § 3.1, § 6.4 |
| 2 | **FATTO** — l'animazione di uscita non esiste più su nessuna voce della superficie; la regola generale `[data-leaving]` è comunque scritta | § 3.1, § 6.4 |
| 3 | **FATTO** — il velo è eliminato, non ricalibrato; con i numeri che lo condannano e la clausola di DESIGN_SYSTEM_V2 che lo vietava già | § 2.3, § 4.4 |
| 4 | **FATTO** — i due bottoni si disattivano, il fuoco è parcheggiato **prima** che si disattivino | § 4.4, codice in § 4.9 |
| 5 | **FATTO e in parte CONTESTATO** — `attr(data-vt type(<custom-ident>), none)` in CSS puro, misurato; nessun `style=""`, nessun JS per il nome | § 2.2 punto 1, § 4.7 |
| 6 | **FATTO** — `transform-origin` non ha parole chiave logiche: le tre dichiarazioni sono cadute. Sostituite da `--sill-a`/`--sill-b` e, sull'asse di blocco, da `top`, che **è** block-start in scrittura orizzontale | § 2.2 punto 6, § 4.2 |
| 7 | **FATTO** — `role="progressbar"` e i cinque `aria-*` **sopravvivono, sull'`<ol>`**; l'asserzione su `hx-post` cambia, ed è elencata come modifica richiesta, non nascosta | § 4.3, § 8 |
| 8 | **FATTO** — `pageswap` con `skipTransition()` fuori dal compito e fuori dalla lingua; misurato che `event.activation.entry.url` è disponibile | § 4.7, § 4.9 |
| 9 | **FATTO** — `contain: paint` eliminato ovunque. Misurato: non «clippa i bordi», **cancella il 100 % dell'anello** | § 2.2 punto 3 |
| 10 | **FATTO, e allargato** — la funzione di `row.flip` era `layout`, che è una **famiglia**; e non bastava la curva sui `group`: anche `old`/`new` restavano a `ease` e a **250 ms** | § 2.2 punto 5, § 4.7 |

### 2.2 Violazioni

**1 — `view-transition-name` per riga senza `style=""`. FATTO; la premessa «ha esattamente una
implementazione ovvia» è CONTESTATA.** Misurato su Chromium 153:
`view-transition-name: attr(data-vt type(<custom-ident>), none)` calcola l'identificatore
dall'attributo, senza toccare `style`. Tre casi misurati: valore valido → `ile-case-ref-E46E03B461`;
valore non valido come identificatore (`"9 bad!ident"`) → `none`; attributo assente → `none`. Il
degrado è quindi **per costruzione**, e nei motori senza `attr()` tipizzato la dichiarazione è
invalida in fase di parsing e il nome resta `none`.
Misurato anche che il CSP del progetto **blocca davvero** l'attributo: su
`http://127.0.0.1:8771/fr/faq/`, un elemento con `style="view-transition-name: …; color: red"`
conserva l'attributo nel DOM ma calcola `view-transition-name: none` e il colore del corpo, con in
console «Applying inline style violates the following Content Security Policy directive
'style-src 'self''»; lo stesso valore scritto con `el.style.setProperty(…)` **si applica**
(`ile-row-8`, `rgb(0, 128, 0)`, nessuna violazione). Una precisazione: il test citato dalla
revisione (`apps/orientation/tests/test_compliance.py:126`) copre solo `#orientation-step`, non la
tabella del fascicolo — ma il CSP la copre, e la conclusione della revisione è giusta.

**2 — `--swap-veil`. FATTO per eliminazione.** Il numero era inventato e lo confermo io stesso
ricalcolandolo: `--ink` `#15222A` composto al **62 %** su `--min-0` `#F4F3F0` dà
**4,455:1** (la revisione dice 4,45), `--ink-2` `#4A5A62` dà **2,788:1** (la revisione dice 2,79).
Per far passare 4,5:1 servirebbe α ≥ **0,6233** per `--ink` ma α ≥ **0,8456** per `--ink-2` e
α ≥ **0,9045** per `--ink-3`: a quel punto il velo non si vede più ed è teatro.
Ma la ragione per cui sparisce non è aritmetica: **DESIGN_SYSTEM_V2 § 3.2 chiude con «Nessuna
opacità sul testo (colore, non alfa)»**, e il `<fieldset>` contiene la domanda di legge. Il velo
era vietato prima di essere sbagliato. Lo stato di attesa è portato altrove (§ 4.4) e non tocca
l'opacità di nessun testo in tutta la superficie.

**3 — `contain: paint` e l'anello di fuoco. FATTO, e il difetto era peggiore.** Misurato con lo
stesso anello del prodotto (`outline 2px` + `outline-offset 2px` + alone `box-shadow 0 0 0 2px`)
su tre contenitori identici, contando i pixel dell'anello in uno screenshot ritagliato:
`contain: layout paint` → **0 pixel di anello**; `contain: layout` → **1 412**; nessun
contenimento → **1 412**. Non «si perde sui bordi ritagliati»: **sparisce tutto**. `contain` non
compare più in questo documento, in nessuna forma: senza tab non c'è più un viewport da isolare, e
il `<details>` non ne ha bisogno.

**4 — `layout` non è una funzione. FATTO.** Le sette funzioni sono orientamento, gerarchia,
causalità, stato, feedback, profondità, delizia; `LAYOUT` è una delle nove **famiglie** di § 2, e
quella famiglia dichiara già la funzione giusta: **causalità**. Il catalogo di § 5 è riscritto
interamente e ogni voce porta una delle sette.

**5 — La quarta curva. FATTO, e più larga di così.** Misurato, con `getComputedStyle(root,
'::view-transition-group(ile-a)')` durante una transizione reale:
*senza* regola d'autore → `animation-timing-function: ease`, `animation-duration: 0.25s`, e i
keyframe UA riportano `easing: "ease"`. Quindi non entrava solo una quarta curva: entrava anche un
**quinto numero, 250 ms**, e non solo sui `group` ma su `::view-transition-old(root)` e
`::view-transition-new(root)`, che la revisione 1 non nominava affatto. La correzione è universale
e verificata: con le tre regole di § 4.7 tutti e sei gli pseudo-elementi misurati riportano
`cubic-bezier(0.25, 1, 0.5, 1) / 0.24s` (entrate e gruppi) e
`cubic-bezier(0.7, 0, 0.3, 1) / 0.12s` (uscite). Nessun valore UA sopravvive.

**6 — `@view-transition { navigation: auto }` globale. FATTO.** La sola dichiarazione CSS resta
`auto`, ma la navigazione è **filtrata in `pageswap`**: `skipTransition()` se cambia il primo
segmento dopo la lingua **o** se cambia la lingua. Misurato che l'informazione c'è:
`event.activation.navigationType` = `"push"` e `event.activation.entry.url` =
`http://127.0.0.1:8771/__detail` su una navigazione reale. Il passaggio sito ↔ portale è escluso
per costruzione (primo segmento diverso) e resta alla superficie «autenticazione», a cui
DESIGN_SYSTEM_V2 § 8.8 assegna già il suo crossfade di 320 ms con la barra che scende in scena:
non lo tocco.

**7 — Il `<select>` nudo e le tab sul fascicolo. FATTO, rinunciando a entrambi.** Non decoro più
il `<select>`: § 9.8 dice «form a pagina con conferma», e quel form è opera della specifica
*fascicolo*. Il TIMBRO di questo documento **non presuppone quale controllo ci sia**: si attacca
alla riga (`[data-row-key]`) e al form (`[data-stamp-form]`), e funziona identico il giorno in cui
il `<select>` diventa una pagina di conferma. Le tab desktop sulle cinque sezioni sono ritirate:
§ 9.8 prescrive uno spazio di lavoro con le sezioni **presenti**, e `<details>` **solo** sotto
1024.

**8 — «Se un nome manca nel documento d'arrivo la transizione si annulla». CONTESTATA la mia
stessa frase, e FATTA.** Misurato: con `ile-chrome-header`, `ile-chrome-rail` e `ile-main`
nominati nel documento di partenza e il solo `rail` assente all'arrivo, la transizione **non si
annulla**: `ready` si risolve, si creano 16 animazioni e fra queste
`::view-transition-old(ile-chrome-rail)` che gira `-ua-view-transition-fade-out` **da sola**. È
esattamente lo sfarfallio che la revisione 1 diceva di prevenire. Di più: i due selettori che
citavo, `.portal-rail` e `.case-band`, **non esistono in nessun template**; i nomi veri sono
`.portal-bar` (`partials/portal_chrome.html:16`), `.portal__aside` + `components/local_nav.html`
(`portal/base_portal.html:42`) e `.case-header`
(`portal/partials/case_header.html:13`). Nella revisione 2 nessun elemento di *chrome* è nominato:
si nomina `main`, che esiste su ogni pagina (`base.html:56`), e si nominano **solo** gli oggetti
che attraversano, armati per la singola navigazione (§ 4.7).

### 2.3 Lacune

**1 — «zero JavaScript» che chiedeva JavaScript. FATTA, rinunciando all'esclusività.** Il ritardo
di 60 ms e lo `scrollIntoView` spariscono. Misurato perché non si possono avere con il CSS: con
`<details name>` il browser chiude il fratello da solo e il documento **salta**; nel rig, il
contenuto sotto il gruppo si è spostato di **−73 px** in un fotogramma e lo scroll anchoring non
ha compensato (`window.scrollY` invariato, `overflow-anchor: auto`). Non c'è modo CSS di ritardare
l'apertura. Conclusione: `data-accordion="single"` e l'attributo `name` escono dal contratto del
componente — non sono usati da nessuna pagina (`grep` → solo la riga che li genera) e l'unico
consumatore reale, la FAQ, non ha ragione di essere esclusiva (la ricerca renderizza **tutti** i
pannelli aperti, `faq/index.html:32`). `initAccordions` si cancella con gli altri due.

**2 — `interpolate-size` su `:root`. FATTA.** Dichiarato sui tre selettori, non sulla radice.
Verificato sulla pagina viva col foglio candidato: `:root` resta `numeric-only`, `.faq-item`
è `allow-keywords`, e l'altezza interpola (16 altezze distinte).

**3 — Selettori inesistenti. FATTA**, vedi violazione 8. Nessun nome di chrome.

**4 — `sessionStorage['ile:task']`. FATTA per eliminazione.** La chiave non esiste più. Il doppio
arrivo è risolto strutturalmente: l'unico segnale è `pagereveal`, che **il browser emette solo
quando la transizione avviene davvero**. Misurato, e con un'implicazione che decide dove va il
codice: su un caricamento a freddo della FAQ viva gli eventi cadono nell'ordine `head.js` 374,5 ms
→ **`pagereveal` 380,6 ms** (`viewTransition: false`) → `module` 583,2 ms → `DOMContentLoaded`
583,2 ms; su una navigazione dello stesso compito `head.js` 239,3 → **`pagereveal` 256,5**
(`viewTransition: true`) → `module` 321,1 → `DOMContentLoaded` 321,2. **`pagereveal` precede il
primo modulo di 202,6 ms a freddo e di 64,6 ms a caldo**: il listener che mette la bandiera
d'arrivo **deve** stare in `static/js/head.js`, sincrono nel `<head>`, o `shell.js` non la vedrà
mai.

**5 — `state` vecchio o nuovo. FATTA, senza ambiguità.** Si memorizza **il testo vecchio**, letto
dal DOM nel momento del `submit` (`row.querySelector('.state').textContent.trim()`), e all'arrivo
il timbro suona **solo se** il testo letto adesso è **diverso**. Un solo verso, scritto in § 4.9.

**6 — Cinque sezioni che a volte sono quattro. FATTA per eliminazione delle tab.** La quinta
sezione sta dentro `{% if transitions %}` (`cases/detail.html:189`) e resta una sezione del
documento, con i suoi `aria-labelledby` (`#journey-title`, `#checklist-title`,
`#assessment-title`, `#actors-title`, `#state-title`) intatti, raggiungibile da `Ctrl+F` e
stampabile. Nessun contratto di ancoraggio cambia.

**7 — `localStorage` che nasconde quattro sezioni su cinque. FATTA** con la stessa eliminazione.
`data-tabs-remember` non è usato da nessun template e il codice che lo leggeva sparisce.

**8 — TIMBRO × View Transition sullo stesso POST → redirect → GET. FATTA, con un ordine.** Il
POST del `<select>` è una navigazione e **attiva** la transizione. L'ordine è deterministico:
`pagereveal` → se c'è `event.viewTransition`, il timbro si attacca a
`event.viewTransition.finished.then(stamp)`; altrimenti parte subito. Il timbro non gira **mai**
durante la transizione. La riga marcata non può essere in un pannello nascosto: non ci sono più
pannelli.

**9 — Fatto e da fare distinti dal solo colore. FATTA, e il colore non è nemmeno il segnale
principale.** Il segmento fatto è **pieno** (`scaleX(1)`), quello da fare è **vuoto**
(`scaleX(0)`): la differenza è presenza/assenza di tratto, non tinta. In più: il segmento corrente
porta un disco pieno di **8 px** misurato, l'ultimo segmento è **tratteggiato** perché il percorso
è adattivo, e restano l'etichetta visibile «Question N · P %» e `aria-valuetext`. Quattro canali
ridondanti. Contrasti ricalcolati: riempimento `--terr-line-lt` `#0F6A72` contro canvas
`--min-0` = **5,692:1**; riempimento contro traccia vuota `--hairline` `#D3D2CC` = **4,169:1**
(≥ 3:1, WCAG 1.4.11); l'ultimo segmento tratteggiato usa `--hairline-strong` `#7A868B` =
**3,373:1** sul canvas, perché *quello* porta significato (il percorso può essere più lungo).

**10 — 400 ms e 10 s. FATTA:** EMENDAMENTO 3, e ripetuta nel catalogo come «soglia, non durata».

**11 — «il fuoco va sul `<legend>`». FATTA.** Misurato: `<legend>` non è focalizzabile. Il nodo è
`<span class="wizard__question" id="wizard-question" tabindex="-1">`
(`orientation/_step.html:17`), che è l'unico bersaglio nominato in tutto il documento, anche nel
ramo d'errore.

### 2.4 Segnali di «cheap»

**1 — «il kit di default del 2026». Accolto senza riserve, e rifatto da capo.** Non c'è più una
tablist con la sottolineatura che scorre; non c'è più il fade + 12 px orizzontale; non c'è più il
crossfade con `translateY(8px)`. Al loro posto c'è **una legge e cinque gesti** (§ 3), e lo
strumento è sempre lo stesso: la riga da 2 px del sistema cartografico, messa in moto.

**2 — «TIMBRO è un timbro solo di nome». Accolto.** Non è più una regola che cresce da zero —
quello è l'evidenziatore di riga di qualunque back-office. Adesso **atterra**: arriva già spessa
(`scaleX(2.4)` su un tratto di 2 px, cioè 4,8 px) e si **comprime** a 2 px in 120 ms `--ease-in`,
la carta **cede** di 1 px e si riassesta con `SPRING_SETTLE`, e la parola di stato **posa**
(`scale(1.06) → 1`). Tre note in 120 ms + molla. Sul bronzo la revisione ha ragione a metà: il
bronzo è dei sigilli d'autorità e un cambio di stato operativo non lo è, ma la ferita
autoinflitta era un'altra — il gesto era senza peso. Ora ha peso senza rubare un token. E la
regola non «sfuma verso il colore di stato»: quello era un'animazione di colore, vietata. **Resta**,
come traccia della cosa che hai fatto, finché non navighi.

**3 — «Le View Transitions spese per un crossfade». Accolto, ed è il cuore della revisione 2.**
Adesso la riga del registro che clicchi **diventa** la testata del fascicolo che apre: il
riferimento e la pillola di stato sono lo stesso oggetto nei due documenti e attraversano.
Misurato su una navigazione cross-document reale sulla stessa origine, con i fogli di stile veri:
si creano `::view-transition-group(ile-ref-E46E03B461)` e
`::view-transition-group(ile-state-E46E03B461)` oltre a `ile-main` e `root`, tutti a 240 ms, e il
riquadro del riferimento **cambia misura durante il tragitto** (119 × 28 px nella riga → 132 × 28
px nella testata): è un'interpolazione vera, non uno scambio.

**4 — «Tre nomi italiani appiccicati dopo». Accolto.** I nomi adesso vengono **dopo** il
meccanismo e lo descrivono: la SOGLIA è letteralmente una riga che passa su un bordo; il VARCO è
letteralmente un oggetto che passa da una pagina all'altra; il TIMBRO atterra e comprime. Se si
toglie il nome, il gesto resta riconoscibile — che è l'unico test che conta.

**5 — «`--swap-shift: 12px` usato per tre gesti diversi». Accolto.** Non c'è più nessun
`translateX` nella superficie, **tranne uno**: le 12 px della foglia di registro (§ 4.7), che è
l'unico posto dove qualcosa scorre lateralmente, e scorre perché la paginazione ha un verso. Tutto
il resto esprime la direzione **con il bordo da cui una riga cresce**, non con una traslazione: è
più economico da comporre, non ha un valore da tarare, e in RTL si inverte da solo.

**6 — «§ 8.7 è il tell: tre registrazioni per far vedere la differenza». Accolto e cancellato.** La
consegna non porta video. Porta i numeri di § 7 e le quattro prove di § 9 che una persona esegue in
un browser in dieci minuti.

**7 — «Tutto è filetti da 2 px su carta». Accolto in parte, e difeso.** Il filetto da 2 px non è
una scelta di prudenza: è **lo spessore del sistema cartografico** già in produzione
(`.state` porta `border-inline-start: 2px solid currentcolor`, `register.css:715`; le tacche e la
graticola sono la stessa misura). Il mio errore era far fare a un filetto **fermo** il lavoro
dell'animazione. Nella revisione 2 il filetto non è mai fermo: **passa** sul bordo di ciò che
arriva (SOGLIA), **atterra e si comprime** su una riga (TIMBRO), **si riempie** su un segmento
(CAMMINO). Il registro non è più severo: è la stessa materia, in moto.

---

## 3. LA PROPOSTA — una legge, cinque gesti

> **La legge: in questo prodotto niente si dissolve. Qualcosa passa, e ciò che sta sotto appare.**

Un crossfade è la confessione che non si sa che cosa stia succedendo: due immagini della stessa
regione si sovrappongono e per 240 ms non è vero né lo stato di prima né quello di dopo. Qui
l'unico strumento è **una riga da 2 px in `--terr-line-lt`** — la linea della graticola, la stessa
che disegna la rotta e le tacche — e quella riga fa sempre una delle tre cose che una riga sa
fare: **passare**, **riempire**, **atterrare**.

| Gesto | Che cosa dice | Dove | Meccanismo |
|---|---|---|---|
| **IL VARCO** | ciò che hai scelto è ciò che stai leggendo | riga di registro → fascicolo | il riferimento e la pillola di stato sono nominati nei due documenti e attraversano (View Transition cross-document) |
| **LA PAGINA** | il registro è rilegato e tu stai voltando | paginazione, ricerca | il solo blocco della lista esce di 12 px verso il bordo da cui vieni ed entra di 12 px dal bordo verso cui vai; la testata e la barra di paginazione non si muovono |
| **LA SOGLIA** | qui è stata posata una cosa nuova | domanda del wizard, qualunque regione sostituita in pagina | una riga da 2 px spazza il bordo block-start della regione: si traccia dal margine di lettura, arriva intera, sgombera verso l'altro margine. Una sola animazione, 320 ms |
| **IL TIMBRO** | **questa** riga è cambiata, per mano tua | riga di checklist, stato del fascicolo | il tratto atterra spesso e si comprime, la carta cede di 1 px, la parola posa |
| **IL RESPIRO** | c'è altro sotto, ed è tuo | `<details>` | altezza nativa, zero JavaScript |

Perché `--terr-line-lt` e non `--accent`, che ha lo stesso esadecimale: DESIGN_SYSTEM_V2 § 1.3
regola 1 riserva `--accent` a **link, CTA primaria e anello di fuoco**, e dice «Nessun titolo,
icona o sfondo lo usa»; la regola 2 assegna la tinta del territorio alla **grafica** — «mai testo,
mai interazione». Un filetto che segna un arrivo non è un controllo: nessuno lo preme, non ha nome
accessibile, è un `::before` decorativo. Il token esiste esattamente per questo caso, e usarlo
tiene i due conti separati: `grep --accent` continua a restituire solo link, CTA e fuoco.

### 3.1 Quello che questa revisione toglie

Una specifica che aggiunge soltanto è una specifica che non ha deciso.

- **Le tab escono dal prodotto.** `initTabs` e `initSteppers` si cancellano da `main.js`; i due
  template restano su disco **fuori servizio** e nessuna pagina li include. Ragioni, in ordine di
  forza: § 9.8 prescrive lo spazio di lavoro con le **sezioni presenti** e `<details>` **solo** sotto
  1024 — una tablist desktop contraddice il documento vincolante; il `data-tabs-remember` farebbe
  atterrare chi torna su un fascicolo con quattro sezioni su cinque invisibili (lacuna 7 della
  revisione, giusta); e il prodotto non ha **una** tab (§ 1.7), quindi inventarne una per avere
  qualcosa da animare è precisamente il difetto che la revisione ha nominato.
- **L'animazione di uscita esce.** Non c'è un solo posto in questa superficie in cui un nodo venga
  animato mentre lo si toglie. Il frammento del wizard si sostituisce con `replaceWith`, atomico.
  Questo scioglie la contraddizione `hidden` × uscita alla radice: non c'è uscita da osservare.
  **Contratto permanente**, se un giorno servisse: lo stato semantico (`hidden`, `aria-selected`,
  `tabIndex`) si scrive **nel fotogramma dell'azione**; l'uscita si porta con una classe di
  attesa `[data-leaving]`; `hidden` si applica su `animationend` **oppure** subito, sul percorso
  di annullamento (Escape, riattivazione rapida, `event.repeat`), **il primo dei due che arriva**;
  e nessuna correttezza dipende da `transitionend`.
- **L'ordinamento FLIP esce**, perché `?sort=` non esiste (§ 1.8).
- **Il velo del form esce** (violazione 2), e con lui ogni opacità su testo.
- **HTMX non entra**: 14 KB gzip contro 1,49 KB misurati di `soglia.js`, per un comportamento solo.

---

## 4. IL CODICE

Un nuovo foglio, un nuovo modulo, tre righe in `head.js`, e un elenco chiuso di modifiche ai
template. Tutto ciò che segue è completo: non c'è una regola da inventare.

### 4.1 File e token

**Nuovo** `static/css/v3/transitions.css`, importato per ultimo in `static/css/main.css` (una
riga, dopo `v3/buttons.css`).
**Nuovo** `static/js/src/soglia.js` → `static/js/dist/soglia.js` (esbuild, come gli altri: stesso
`splitting`, stesso chunk Motion condiviso), aggiunto a `templates/base.html` accanto a
`dist/shell.js`.

```css
/* transitions.css § 1 — token derivati. Nessun colore nuovo, nessuna durata nuova. */
:root {
  --sill-a: left;       /* il bordo FISICO da cui una riga cresce */
  --sill-b: right;      /* il bordo verso cui sgombera */
  --sill-w: 2px;        /* lo spessore del sistema cartografico */
  --leaf-shift: 12px;   /* la foglia di registro; <= 16 px (MOTION_SYSTEM § 2) */
  --stamp-land: 2.4;    /* il timbro atterra a 4,8 px e si comprime a 2 */
  --leaf-out: calc(-1 * var(--leaf-shift));
  --leaf-in: var(--leaf-shift);
}
:root[dir="rtl"] {
  --sill-a: right; --sill-b: left;
  --leaf-out: var(--leaf-shift); --leaf-in: calc(-1 * var(--leaf-shift));
}
:root[data-soglia="back"] {
  --sill-a: right; --sill-b: left;
  --leaf-out: var(--leaf-shift); --leaf-in: calc(-1 * var(--leaf-shift));
}
:root[data-soglia="back"][dir="rtl"] {
  --sill-a: left; --sill-b: right;
  --leaf-out: calc(-1 * var(--leaf-shift)); --leaf-in: var(--leaf-shift);
}
```

Le quattro combinazioni sono state **lette a runtime** sulla pagina viva, non dedotte:
LTR avanti `--sill-a: left`, `--leaf-in: 12px` · LTR indietro `right`, `calc(-1 * 12px)` ·
RTL avanti `right`, `calc(-1 * 12px)` · RTL indietro `left`, `12px`. Il verso del moto è quindi la
composizione di due fatti (lingua, senso di marcia), non una variabile da ricordare.

### 4.2 LA SOGLIA — la riga che passa

Il bersaglio porta `data-sill`. La riga esiste **solo** quando la radice porta
`data-arrival="swap"`, cioè solo quando una regione è stata davvero sostituita.

```css
/* transitions.css § 2 */
[data-sill] { position: relative; }
[data-sill]::before { content: none; }

@media (prefers-reduced-motion: no-preference) {
  :root[data-arrival="swap"] [data-sill]::before {
    content: "";
    position: absolute;
    inset-block-start: 0;
    inset-inline: 0;
    block-size: var(--sill-w);
    background: var(--terr-line-lt);
    transform: scaleX(0);
    transform-origin: var(--sill-a);
    animation: ile-sill var(--motion-slow) both;
    pointer-events: none;
    z-index: 1;
  }
  @keyframes ile-sill {
    0%   { transform: scaleX(0); transform-origin: var(--sill-a); animation-timing-function: var(--ease-out); }
    55%  { transform: scaleX(1); transform-origin: var(--sill-a); animation-timing-function: var(--ease-in); }
    56%  { transform: scaleX(1); transform-origin: var(--sill-b); animation-timing-function: var(--ease-in); }
    100% { transform: scaleX(0); transform-origin: var(--sill-b); }
  }
}
@media (forced-colors: active) {
  :root[data-arrival="swap"] [data-sill]::before { background: Highlight; forced-color-adjust: none; }
}
```

**L'invariante da non rompere**: ai fotogrammi 55 % e 56 % `scaleX` vale **esattamente 1** in
entrambi. È l'unica ragione per cui il cambio di `transform-origin` non si vede — a scala 1 il
punto d'origine non sposta nulla. Chi tocca questi keyframe deve tenere quei due valori a 1.

Misurato sul foglio candidato servito alla FAQ viva, forzando `currentTime` e leggendo lo pseudo:
scaleX **0** all'inizio → **0,757** al 20 % → **0,981** al 40 % (origine `0px`, cioè il bordo di
lettura) → origine **`1240px`**, cioè il bordo opposto, dopo il ribaltamento → **0,152** al 75 % →
**0** al 99 %. Altezza costante **2 px**, colore `rgb(15, 106, 114)` = `#0F6A72`. Una sola
animazione, **una sola durata token** (`--motion-slow`, 320 ms), due delle tre curve, dichiarate
dentro i keyframe: `animation-timing-function: var(--ease-out|--ease-in)` risolve correttamente
attraverso `var()` (verificato).

Perché non un translate: una riga che **cresce e sgombera** non ha bisogno di sapere quanto è
larga la regione, non produce nessun pixel fuori dal bordo, e in RTL si inverte cambiando una
parola chiave. Perché non un crossfade: non c'è nessun fotogramma in cui due testi diversi siano
visibili insieme.

**Stato ridotto.** Sotto `prefers-reduced-motion: reduce` il blocco intero non si applica e
`[data-sill]::before` resta `content: none`: **la riga non esiste**, non «esiste ferma». È
legittimo perché non porta informazione persistente — l'informazione «una nuova domanda è
arrivata» è portata, nei due stati identicamente, dal **fuoco** che si sposta sulla domanda e
dalla **live region** che dice la posizione. Nessun elemento resta a `opacity: 0`, nessun
contenuto manca.

### 4.3 IL CAMMINO — il rail sostituisce la barra navy

`<ol class="wizard__rail">` con `max_steps` `<li>`. **`role="progressbar"` e i suoi cinque
`aria-*` si spostano sull'`<ol>` e sopravvivono**: `apps/orientation/tests/test_compliance.py:118-121`
continua a passare senza modifica. Un `<ol>` con `role="progressbar"` perde la semantica di lista
e i `<li>` diventano presentazionali — corretto, perché i segmenti sono grafica e il testo sta
nell'etichetta visibile e in `aria-valuetext`. L'etichetta «Question N · P %» resta dov'è, con
il suo `id="wizard-progress-label"` referenziato da `aria-labelledby`.

I segmenti si colorano **dal server**, quindi il rail è giusto anche senza JavaScript: `--done` per
`forloop.counter0 < step_number - 1`, `--current` per l'uguaglianza, `--open` sull'ultimo.

```css
/* transitions.css § 3 */
.wizard__rail { display: flex; gap: var(--s-2); list-style: none; margin: 0 0 var(--s-2); padding: 0; }
.wizard__seg  { flex: 1 1 0; block-size: var(--sill-w); position: relative; background: var(--hairline); }
.wizard__seg--open { background: none; border-block-start: var(--sill-w) dashed var(--hairline-strong); }
.wizard__seg::after {
  content: ""; position: absolute; inset: 0;
  background: var(--terr-line-lt); transform: scaleX(0); transform-origin: var(--sill-a);
}
.wizard__seg--done::after, .wizard__seg--current::after { transform: scaleX(1); }
.wizard__seg--current::before {
  content: ""; position: absolute; inset-block-start: -3px; inset-inline-end: -4px;
  inline-size: 8px; block-size: 8px; border-radius: 999px; background: var(--terr-line-lt);
}
@media (prefers-reduced-motion: no-preference) {
  :root[data-arrival="swap"] .wizard__seg--current::after {
    animation: ile-rail var(--motion-base) var(--ease-out) both;
  }
  @keyframes ile-rail { from { transform: scaleX(0); } to { transform: scaleX(1); } }
}
@media (forced-colors: active) {
  .wizard__seg { background: Canvas; border-block-start: var(--sill-w) solid GrayText; }
  .wizard__seg::after, .wizard__seg--current::before { background: Highlight; forced-color-adjust: none; }
}
```

**Geometria, misurata sul questionario vivo col foglio candidato.** Contenitore `.wizard` =
**768 px** a viewport 1440 (48 rem), rail **688 px**. A `max_steps = 3` (il jeu de règles attivo):
tre segmenti di **224 px** × 2 px. A `max_steps = 8` e viewport **390 px**: rail **350 px**, otto
segmenti di **36,75 px** × 2 px — leggibili, e comunque non sono un bersaglio (non sono
focalizzabili, non sono cliccabili: saltare avanti in un questionario adattivo è una bugia).
Disco del segmento corrente **8 × 8 px**, `rgb(15, 106, 114)`. Ultimo segmento: `border-block-start
… dashed` verificato come `dashed` nel computed.

**Stati del rail** (non è un controllo: non ha hover, non ha fuoco, non ha disabled):
*fatto* tratto pieno `--terr-line-lt` (5,692:1 sul canvas) · *corrente* tratto pieno + disco 8 px +
`aria-valuenow` · *da fare* traccia vuota `--hairline` (nessun tratto: assenza, non tinta) ·
*aperto* (ultimo) tratteggio `--hairline-strong` (3,373:1) · *forced-colors* `Highlight` su
`Canvas` con `GrayText` per la traccia.

Le 21 classi `.wizard__progress-fill--*` e la transizione su `inline-size` si cancellano da
`apps/orientation/static/orientation/wizard.css`: **1 432 B di sorgente, −261 B gzip**
(1 659 → 1 398). **[RIMISURATO]**: la revisione 1 dichiarava «−0,9 KB», che era falso di un fattore
3,5. Il filtro `progress_class` (`apps/orientation/templatetags/orientation_tags.py:35`) resta
senza chiamanti e si cancella con loro.

### 4.4 Il wizard — l'attesa senza velo e senza spinner

Il server è già pronto: `apps/orientation/views.py` sceglie il frammento sull'intestazione
`HX-Request` e risponde con `HX-Push-Url`, oppure con `HX-Redirect` a fine questionario. **Il
contratto dati non cambia. Il contratto di test sì**, ed è elencato in § 8, non nascosto.

**Ordine non negoziabile**, scritto nel codice come sequenza e non come intenzione:
**a.** scambio del DOM → **b.** fuoco su `#wizard-question` → **c.** testo della live region →
**d.** moto. La semantica è già corretta mentre l'animazione comincia.

**Lo stato di attesa, senza toccare l'opacità di un solo testo** (violazione 2, EMENDAMENTO 2):

1. **I due bottoni si disattivano.** `templates/orientation/_step.html` chiude `</fieldset>`
   **prima** di `<div class="wizard__actions">` — verificato a runtime:
   `fieldset.contains(document.querySelector('.wizard__actions'))` → **`false`**. Quindi `inert`
   sul `<fieldset>` lascerebbe «Continuer» e «Précédent» premibili durante il fetch, cioè un
   secondo POST di risposta su un questionario d'orientamento. Si disattivano **entrambi** con
   `disabled` (non `aria-disabled`: deve essere impossibile, non solo annunciato).
2. **Il fuoco è parcheggiato prima**, non dopo: `#wizard-question.focus({preventScroll:true})`
   viene **prima** di `b.disabled = true`, perché un bottone che si disattiva mentre ha il fuoco
   lo consegna a `<body>` — che è il difetto § 1.2, reintrodotto dalla cura. Fra l'invio e
   l'arrivo il fuoco sta sulla domanda che hai appena risposto; all'arrivo sta sulla domanda
   nuova, stesso nodo, stesso id: **il fuoco non si muove mai visibilmente**.
3. **La risposta scelta prende il timbro di commit**: un filetto da 2 px `--terr-line-lt` lungo il
   bordo inline-start della `.wizard__choice` selezionata, `scaleY(0 → 1)` in 120 ms `--ease-out`,
   `transform-origin: top`. Questo è lo stato di attesa: non «il modulo è spento», ma «questa
   risposta è presa».
4. **Oltre 400 ms** (soglia, EMENDAMENTO 3) la live region dice il testo di
   `data-step-saving`. Sotto quella soglia non dice nulla, perché la risposta è già arrivata:
   **59, 20, 22 ms** misurati in locale.

```css
/* transitions.css § 4 */
.wizard__choice { position: relative; }
.wizard__choice::before {
  content: ""; position: absolute; inset-block: 0; inset-inline-start: 0;
  inline-size: var(--sill-w); background: var(--terr-line-lt);
  transform: scaleY(0); transform-origin: top;
}
.wizard__form[aria-busy="true"] .wizard__choice:has(.wizard__input:checked)::before { transform: scaleY(1); }
@media (prefers-reduced-motion: no-preference) {
  .wizard__choice::before { transition: transform var(--motion-instant) var(--ease-out); }
}
@media (forced-colors: active) { .wizard__choice::before { background: Highlight; forced-color-adjust: none; } }
```

`transform-origin: top` **non** è una svista: sull'asse di blocco di un documento
`writing-mode: horizontal-tb` — cioè tutte e quattro le lingue del prodotto, arabo compreso —
`top` **è** block-start, e una parola chiave logica per `transform-origin` non esiste (§ 2.2
punto 6). Il giorno in cui esistesse un modo verticale, questa riga andrebbe rivista; nessun'altra.

**Stati di «Continuer» e «Précédent»** — la tabella completa, nessuna variante senza CSS.
`.btn--primary` prende già `--btn-bg: var(--accent)` da `static/css/v3/buttons.css`; qui si
aggiunge **solo** ciò che manca.

```css
/* transitions.css § 4bis — gli stati che il bottone non ha ancora */
.wizard__actions .btn[disabled] { cursor: default; }
@media (prefers-reduced-motion: no-preference) {
  .wizard__actions .btn { transition: background-color var(--motion-fast) var(--ease-out),
                                      translate var(--motion-instant) var(--ease-standard); }
  .wizard__actions .btn:active:not([disabled]) { translate: 0 1px; }
}
```

| Stato | Resa | Numeri |
|---|---|---|
| *rest* | `--accent` pieno, testo `--min-0`, 48 px, raggio 2 | testo **5,692:1**; fondo sul canvas **5,692:1** (≥ 3:1 come componente) |
| *hover* (`hover: hover`) | `--accent-hover` `#0B555C`, 180 ms `--ease-out` | testo **7,668:1** |
| *focus-visible* | anello 2 px `--accent-ring` + alone 2 px, offset 2 — la regola di `base.css:384` | **3,704:1** |
| *active* | `translate: 0 1px`, 120 ms `--ease-standard` | nessun colore cambia |
| *disabled (busy)* | `disabled`, etichetta **invariata**, nessuna opacità sul testo, `cursor: default` | il colore non cambia: l'informazione è `aria-busy` sul form + il commit + la live region |
| *loading* | non esiste come stato separato: è *disabled (busy)* | EMENDAMENTO 2 |
| *error* | torna il frammento con `.wizard__error[role="alert"]`, i bottoni si riabilitano, il fuoco va su `#wizard-question`, **nessuna animazione sull'errore** | — |

### 4.5 IL RESPIRO — `<details>`, zero JavaScript, davvero

```css
/* transitions.css § 5 */
.accordion__item, .faq-item, .wizard__help { interpolate-size: allow-keywords; }
.accordion__item, .faq-item { scroll-margin-block-start: var(--s-16); }

@media (prefers-reduced-motion: no-preference) {
  .accordion__item::details-content,
  .faq-item::details-content,
  .wizard__help::details-content {
    block-size: 0; overflow: clip; opacity: 0;
    transition: block-size var(--motion-base) var(--ease-in),
                opacity var(--motion-instant) var(--ease-in),
                content-visibility var(--motion-base) allow-discrete;
  }
  .accordion__item[open]::details-content,
  .faq-item[open]::details-content,
  .wizard__help[open]::details-content {
    block-size: auto; opacity: 1;
    transition: block-size var(--motion-base) var(--ease-out),
                opacity var(--motion-base) var(--ease-out),
                content-visibility var(--motion-base) allow-discrete;
  }
  .accordion__summary .icon { transition: transform var(--motion-base) var(--ease-standard); }
}
.accordion__item[open] > .accordion__summary .icon { transform: rotate(45deg); }
```

I tre selettori sono chiusi di proposito: i `<details>` che sono **menu** (`account_menu.html`,
`language_switcher.html`, `[data-dropdown]`) non li toccano, perché un menu che respira è un menu
lento.

Misurato sulla `.faq-item` viva: **16 altezze distinte** su 37 campioni, da **77 px** a **205 px**,
penultima 204,98 px e ultima 205 px — nessuno scatto finale. `:root` resta `numeric-only`.

**Stati di `<summary>`** — quello che manca oggi, scritto:

```css
/* transitions.css § 5bis */
.accordion__summary { min-block-size: 44px; display: flex; align-items: center; gap: var(--s-3);
                      cursor: pointer; }
.accordion__summary::-webkit-details-marker { display: none; }
@media (hover: hover) {
  .accordion__summary:hover .icon { transform: scale(1.08); }
  .accordion__item[open] > .accordion__summary:hover .icon { transform: rotate(45deg) scale(1.08); }
}
```

*rest* `--ink` · *hover* (solo `hover: hover`) il glifo cresce dell'8 %, 240 ms `--ease-standard`,
nessun colore che si muove · *focus-visible* l'anello di sistema, **non ritagliato** perché non
c'è più `contain` · *open* glifo a 45° · *disabled* non esiste (un `<summary>` non si disattiva) ·
*loading*/*error* non esistono (il contenuto è già nel DOM). Bersaglio misurato oggi su 390 px:
**76 px** di altezza, sopra i 44 px richiesti — da non perdere.

### 4.6 IL TIMBRO — il gesto che atterra

Markup: `<tr data-row-key="{{ item.pk }}">` sulle righe della checklist e `data-stamp-form` sul
form inline. Nient'altro.

```css
/* transitions.css § 6 */
tr[data-stamped] > :first-child { position: relative; }
tr[data-stamped] > :first-child::before {
  content: ""; position: absolute; inset-block: 0;
  inset-inline-start: calc(-1 * var(--s-3));
  inline-size: var(--sill-w); background: var(--terr-line-lt);
}
@media (prefers-reduced-motion: no-preference) {
  tr[data-stamped] > :first-child::before { animation: ile-stamp var(--motion-instant) var(--ease-in) both; }
  @keyframes ile-stamp {
    from { transform: scaleX(var(--stamp-land)); opacity: 0; }
    to   { transform: scaleX(1); opacity: 1; }
  }
  tr[data-stamped] .state { animation: ile-stamp-word var(--motion-instant) var(--ease-in) both; }
  @keyframes ile-stamp-word {
    from { transform: scale(1.06); opacity: 0; }
    to   { transform: scale(1); opacity: 1; }
  }
}
@media (forced-colors: active) {
  tr[data-stamped] > :first-child::before { background: Highlight; forced-color-adjust: none; }
}
```

La terza nota — **la carta che cede** — è l'unica molla di questa superficie e sta in JavaScript,
come prescrive MOTION_SYSTEM § 1: `animate(row.querySelectorAll("th, td"), {translate: ["0 1px",
"0 0"]}, {type: spring, stiffness: 260, damping: 30, delay: 0.12})`. Misurato che si può fare:
`transform`/`translate` su `<tr>` (`display: table-row`) e su `<td>` (`display: table-cell`)
calcolano `matrix(1, 0, 0, 1, 0, 1)` in Chromium 153 — le celle sono trasformabili.

**Il colore non è mai solo, e non deve nemmeno provarci**: `.state` porta già
`border-inline-start: 2px solid currentcolor` e la **parola** (`register.css:702-715`). Il timbro
non codifica lo stato: dice *quale riga* e *che è successo adesso*. Per questo non sfuma verso il
colore di stato — quella era un'animazione di colore, vietata — e per questo **resta**: è la
traccia di ciò che hai fatto, e sparisce quando lasci la pagina.

Lo stesso meccanismo serve il form «Faire évoluer l'état du dossier»: `data-stamp-form` sul form e
`data-row-key="case"` sulla `.case-header__fact` dello stato, che porta già la sua `.state`.

**Annuncio.** Non si aggiunge una seconda live region. All'arrivo il server ha già messo «La ligne
a été mise à jour.» dentro il `role="status"` di `base.html:59` (§ 1.9); ciò che manca è *quale*
riga, e quello si risolve **spostando il fuoco** sulla cella di stato marcata
(`tabIndex = -1`, `focus()`), dove la tecnologia assistiva legge l'intestazione di riga e la
parola di stato nuova. Un annuncio generico che parla e un fuoco specifico che atterra, in
quest'ordine: nessuna live region concorrente, nessun doppio parlato inventato dal client.

### 4.7 FRA PAGINE — IL VARCO e LA PAGINA

```css
/* transitions.css § 7 */
main { view-transition-name: ile-main; }
.register { view-transition-name: attr(data-vt type(<custom-ident>), none); }
.entry .t-ref, .case-header__reference {
  view-transition-name: attr(data-vt type(<custom-ident>), none);
  display: inline-block;   /* un nome su un inline che va a capo snapshotta il riquadro unito */
}
.entry .state, .case-header__facts .state { view-transition-name: attr(data-vt type(<custom-ident>), none); }

@media (prefers-reduced-motion: no-preference) {
  @view-transition { navigation: auto; }

  /* Nessun numero e nessuna curva del browser sopravvivono a queste tre righe. */
  ::view-transition-group(*) { animation-duration: var(--motion-base);    animation-timing-function: var(--ease-out); }
  ::view-transition-old(*)   { animation-duration: var(--motion-instant); animation-timing-function: var(--ease-in); }
  ::view-transition-new(*)   { animation-duration: var(--motion-base);    animation-timing-function: var(--ease-out); }

  ::view-transition-old(ile-register) { animation: ile-leaf-out var(--motion-instant) var(--ease-in) both; }
  ::view-transition-new(ile-register) { animation: ile-leaf-in  var(--motion-base)    var(--ease-out) both; }
  @keyframes ile-leaf-out { to   { opacity: 0; translate: var(--leaf-out) 0; } }
  @keyframes ile-leaf-in  { from { opacity: 0; translate: var(--leaf-in)  0; } }
}
```

Il nome **non è mai nel markup a riposo**: i template scrivono `data-vt-name="…"` e `soglia.js`
copia `data-vt-name` in `data-vt` **solo** in `pageswap` e in `pagereveal`, e **solo** per i nomi
che in quel documento sono unici. Fuori da una transizione l'attributo `data-vt` non esiste,
`attr()` cade sul fallback `none`, e nessun elemento ha un nome. Questo chiude tre problemi in una
riga: il gruppo orfano che si dissolve da solo (violazione 8), il nome duplicato che annulla la
transizione (due `.register` convivono in `cases/detail.html` — gli assessment e gli
intervenants), e la navigazione fuori compito.

**I nomi.** `ile-register` sul blocco della lista; `ile-ref-<REFERENCE>` sul `.t-ref` della riga e
sul `.case-header__reference` del fascicolo; `ile-state-<REFERENCE>` sulla `.state` della riga e su
quella della case header. I riferimenti del prodotto sono alfanumerici (`E46E03B461`); il prefisso
garantisce comunque un identificatore valido, e un valore non valido cade su `none` — misurato.

**Il filtro, in `pageswap`.** `skipTransition()` se il primo segmento dopo la lingua cambia, o se
la lingua cambia. Misurato che i dati ci sono: su una navigazione reale
`event.activation.navigationType` = `"push"`, `event.activation.entry.url` =
`http://127.0.0.1:8771/__detail`. Il verso: `"traverse"` (indietro/avanti del browser) oppure un
`a[rel="prev"]` attivo → `data-soglia="back"`, che inverte `--leaf-in`/`--leaf-out`.
`components/pagination.html` porta già `rel="prev"` e `rel="next"` (righe 6 e 8 del template): **non serve
markup nuovo per sapere da che parte si sta andando.**

**Prova che funziona davvero, non in teoria.** Due documenti serviti sulla stessa origine del
server vivo, con `main.css` e `portal.css` veri e il markup copiato da `cases/index.html` e da
`portal/partials/case_header.html`. Alla navigazione si creano
`::view-transition-group(ile-ref-E46E03B461)`, `::view-transition-group(ile-state-E46E03B461)`,
`::view-transition-group(ile-main)` e `::view-transition-group(root)`, **tutti a 240 ms**; il
riquadro del riferimento misura **119 × 28 px** nella riga e **132 × 28 px** nella testata, quindi
il motore interpola posizione **e** dimensione. Con `prefers-reduced-motion: reduce` emulato, i due
caricamenti riportano `pagereveal` con `viewTransition: false`: **`@view-transition` dentro
`@media (prefers-reduced-motion: no-preference)` è onorato**, non solo accettato dal parser.

**forced-colors.** Le View Transitions restano attive: gli pseudo-elementi sono istantanee del
rendering già mappato dal sistema, e l'unico moto è opacità e traslazione, che la mappatura non
altera. La revisione 1 le disattivava per prudenza; è una prudenza che toglie la continuità
proprio a chi ha più bisogno di capire dove è andata la pagina. Resta da verificare a mano (§ 9).

### 4.8 Doppio arrivo — risolto senza chiavi

`[data-reveal]` di `shell.js` è l'animazione di **prima visita**. Dopo una View Transition
l'arrivo è già animato. Regola, in due righe e zero `sessionStorage`:

```js
/* static/js/head.js — sincrono nel <head>. pagereveal precede il primo modulo di 202,6 ms
   a freddo e di 64,6 ms a caldo: registrato altrove, non lo vedremmo mai. */
document.documentElement.classList.replace("no-js", "js");
addEventListener("pagereveal", (event) => {
  if (event.viewTransition) document.documentElement.dataset.arrival = "page";
});
```

```js
/* static/js/src/shell.js — una riga sola cambia, dentro il callback di inView. */
const settleAll = () => reveals.forEach((el) => el.classList.add("is-in"));
// dentro inView(...):  if (document.documentElement.dataset.arrival) { settleAll(); return; }
```

La bandiera si legge **dentro** il callback di `inView`, non al modulo: `inView` è comunque
asincrono e a quel punto `pagereveal` è certamente passato. **Una sola animazione d'arrivo per
navigazione, mai due**, e nessuno stato da invalidare.

### 4.9 `static/js/src/soglia.js` — per intero

**1 526 B gzip** (3 354 B minificato, esbuild `--bundle --format=esm --target=es2022 --minify`,
con `./motion.js` esterno perché il chunk Motion da 26,2 KB gzip è già caricato da `shell.js` su
ogni pagina).

```js
/**
 * static/js/src/soglia.js — «la soglia».
 * CSP: nessuno script inline, nessun attributo style. Le proprietà personalizzate si scrivono
 * con la CSSOM (el.style.setProperty), che style-src non copre — misurato sull'origine viva:
 * un attributo style="" viene rifiutato, setProperty si applica.
 */
import { animate, spring, withMotion } from "./motion.js";

const root = document.documentElement;
const SETTLE = { stiffness: 260, damping: 30 };
const STAMP = "ile:stamp";
const STAMP_MAX_AGE = 10000;              /* soglia di validità, non durata (EMENDAMENTO 3) */

const parts = (u) => new URL(u, location.href).pathname.split("/").filter(Boolean);
const sameTask = (u) => {
  const a = parts(u), b = parts(location.href);
  return a[0] === b[0] && (a[1] || "") === (b[1] || "");   /* [0] = lingua, [1] = compito */
};

/* ---- 1. Armare i nomi condivisi, e solo quando sono unici --------------- */
function arm(on) {
  const els = [...document.querySelectorAll("[data-vt-name]")];
  if (!on) { els.forEach((el) => el.removeAttribute("data-vt")); return; }
  const count = new Map();
  els.forEach((el) => count.set(el.dataset.vtName, (count.get(el.dataset.vtName) || 0) + 1));
  els.forEach((el) => {
    if (count.get(el.dataset.vtName) === 1) el.setAttribute("data-vt", el.dataset.vtName);
  });
}

addEventListener("pageswap", (event) => {
  const vt = event.viewTransition;
  if (!vt) return;
  const to = event.activation && event.activation.entry && event.activation.entry.url;
  if (!to || !sameTask(to)) { vt.skipTransition(); return; }
  const back = event.activation.navigationType === "traverse"
    || !!(document.activeElement && document.activeElement.closest('a[rel="prev"]'));
  root.dataset.soglia = back ? "back" : "forward";
  arm(true);
  vt.finished.then(() => arm(false));
});

addEventListener("pagereveal", (event) => {
  arm(true);
  if (event.viewTransition) event.viewTransition.finished.then(stamp);
  else stamp();
});

/* ---- 2. IL TIMBRO ------------------------------------------------------- */
function mark(form) {
  const row = form.closest("[data-row-key]");
  if (!row) return;
  const state = row.querySelector(".state");
  try {
    sessionStorage.setItem(STAMP, JSON.stringify({
      key: row.dataset.rowKey,
      was: state ? state.textContent.trim() : "",   /* IL TESTO VECCHIO. Mai il nuovo. */
      at: Date.now(),
    }));
  } catch (_) { /* storage rifiutato: il timbro è un di più, il registro resta il registro */ }
}

function stamp() {
  let m = null;
  try { m = JSON.parse(sessionStorage.getItem(STAMP) || "null"); sessionStorage.removeItem(STAMP); }
  catch (_) { return; }
  if (!m || Date.now() - m.at > STAMP_MAX_AGE) return;
  const row = document.querySelector(`[data-row-key="${CSS.escape(m.key)}"]`);
  const now = row && row.querySelector(".state");
  if (!row || !now || now.textContent.trim() === m.was) return;   /* nulla è cambiato: niente timbro */
  row.dataset.stamped = "";
  const cell = now.closest("td, th, dd") || now;
  cell.tabIndex = -1;
  cell.focus({ preventScroll: false });
  withMotion(
    () => animate(row.querySelectorAll("th, td"),
      { translate: ["0 1px", "0 0"] }, { type: spring, ...SETTLE, delay: 0.12 }),
    () => {},                                    /* ridotto: il tratto c'è, fermo, completo */
  );
}

/* ---- 3. IL CAMMINO — il wizard, senza HTMX ----------------------------- */
function step(event, form) {
  if (form.dataset.busy) { event.preventDefault(); return; }
  const target = document.querySelector("#orientation-step");
  const status = document.querySelector("#wizard-status");
  if (!target || !window.fetch || !window.DOMParser) return;   /* nessun JS: POST nativo */
  event.preventDefault();

  const body = new FormData(form);
  if (event.submitter && event.submitter.name) body.append(event.submitter.name, event.submitter.value);
  form.dataset.busy = "1";
  form.setAttribute("aria-busy", "true");
  const question = document.querySelector("#wizard-question");
  if (question) question.focus({ preventScroll: true });       /* PRIMA di disabilitare */
  const buttons = [...form.querySelectorAll(".wizard__actions button")];
  buttons.forEach((b) => { b.disabled = true; });
  const slow = setTimeout(() => {
    if (status) status.textContent = form.dataset.stepSaving || "";
  }, 400);                                                     /* soglia di parola, non durata */

  const restore = () => {
    clearTimeout(slow);
    form.removeAttribute("aria-busy");
    delete form.dataset.busy;
    buttons.forEach((b) => { b.disabled = false; });
  };

  fetch(form.action, {
    method: "POST", body, headers: { "HX-Request": "true" }, credentials: "same-origin",
  })
    .then((r) => {
      const to = r.headers.get("HX-Redirect");
      if (to) { location.assign(to); return null; }
      if (!r.ok) throw new Error(String(r.status));
      return r.text().then((html) => ({ html, url: r.headers.get("HX-Push-Url") }));
    })
    .then((res) => {
      if (!res) return;
      clearTimeout(slow);
      const next = new DOMParser().parseFromString(res.html, "text/html").querySelector("#orientation-step");
      if (!next) throw new Error("fragment");
      target.replaceWith(next);                                        /* a. DOM     */
      if (res.url) history.pushState({ ile: 1 }, "", res.url);
      const q = document.querySelector("#wizard-question");
      if (q) q.focus({ preventScroll: true });                         /* b. fuoco   */
      if (status) status.textContent = next.dataset.stepStatus || "";  /* c. parola  */
      root.dataset.arrival = "swap";                                   /* d. moto    */
    })
    .catch(() => { restore(); form.submit(); });                       /* la pagina di oggi */
}

document.addEventListener("submit", (event) => {
  const form = event.target;
  if (form.matches("[data-stamp-form]")) mark(form);
  else if (form.matches("[data-step-form]")) step(event, form);
});

addEventListener("popstate", () => { location.reload(); });
```

`root.dataset.arrival = "swap"` **non si toglie**: il gate serve solo alle animazioni d'arrivo, che
hanno `animation-fill-mode: both` e girano una volta per elemento; e a ogni scambio il frammento è
un nodo nuovo, quindi l'animazione riparte da sola. Toglierlo dopo due fotogrammi ucciderebbe
l'animazione a metà.

---

## 5. MOTION — voci per `MOTION_SYSTEM.md` § 6

Undici voci, undici funzioni prese **dalle sette** di § 0. Nessuna cella contiene una famiglia al
posto di una funzione, nessuna cella contiene una durata al posto di una curva.

| Nome | Funzione | Innesco | Durata | Curva / molla | Proprietà | Stato ridotto | Budget misurato |
|---|---|---|---|---|---|---|---|
| `soglia.sill` | orientamento | una regione è stata sostituita (`[data-arrival="swap"]`) | 320 | `--ease-out` poi `--ease-in`, nei keyframe | `transform: scaleX` + `transform-origin` | la riga non è resa; l'arrivo lo dicono fuoco e live region | **0 Layout, 0 Paint** fra 65 e 566 ms |
| `soglia.rail` | stato | cambio di passo | 240 | `--ease-out` | `transform: scaleX` del segmento corrente | segmento già pieno | 0 layout: `::after` in posizione assoluta |
| `wizard.commit` | feedback | `submit` in corso | 120 | `--ease-out` | `transform: scaleY` del filetto della scelta | filetto presente, pieno | 1 pseudo-elemento |
| `respiro.details` | gerarchia | `toggle` di `<details>` | 240 | `--ease-out` apre / `--ease-in` chiude | `block-size`, `opacity`, `content-visibility` (`allow-discrete`) | pannello completo, nessuna transizione | **14 Layout, uno per fotogramma** — EMENDAMENTO 1 |
| `respiro.icon` | stato | `toggle` | 240 | `--ease-standard` | `transform: rotate(45deg)` | icona già ruotata | esistente, solo ritemporizzata |
| `respiro.hover` | feedback | puntatore su `<summary>` (`hover: hover`) | 240 | `--ease-standard` | `transform: scale(1.08)` del glifo | identico | 0 layout |
| `timbro.rule` | causalità | arrivo con marca valida < 10 s **e** stato cambiato | 120 | `--ease-in` | `transform: scaleX 2.4 → 1`, `opacity` | tratto presente, fermo | **0 Layout, 0 Paint** fra 90 e 521 ms |
| `timbro.paper` | feedback | contatto (ritardo 120 ms) | molla | `SPRING_SETTLE` 260/30 | `translate: 0 1px → 0 0` su `th, td` | nessun cedimento | `transform` su `table-cell` verificato |
| `timbro.word` | stato | contatto | 120 | `--ease-in` | `transform: scale(1.06 → 1)`, `opacity` | parola presente | 1 elemento |
| `varco.cross` | causalità | riga di registro → fascicolo (e ritorno) | 240 | `--ease-out` | gruppo di transizione: posizione **e** dimensione | `@view-transition` non si attiva | 4 gruppi, sulla GPU |
| `pagina.leaf` | orientamento | paginazione, ricerca, `traverse` | 120 fuori / 240 dentro | `--ease-in` / `--ease-out` | `opacity`, `translate` ≤ 12 px sul solo blocco della lista | `@view-transition` non si attiva | 1 gruppo nominato |

**Soglie, non durate** (EMENDAMENTO 3): 400 ms prima dell'annuncio di attesa; 10 000 ms di
validità della marca. Nessuna delle due muove un pixel.

**Vietato su questa superficie**: qualunque `fade-in-up` generico, overshoot, `filter`, animazione
di `box-shadow`, animazione di colore, loop, qualunque animazione su ciò che si ripete dalla
tastiera, e qualunque opacità su testo.

---

## 6. ACCESSIBILITÀ, RTL, FORCED-COLORS

**6.1 Che cosa cambia.** (a) una live region `role="status" aria-live="polite" aria-atomic="true"`
per il wizard, **fuori** dal frammento sostituito (una live region sostituita non annuncia mai
nulla); (b) il fuoco va su `#wizard-question` — mai sul `<legend>`, che non è focalizzabile —
`preventScroll: true`, **prima** che i bottoni si disattivino e **prima** dell'animazione;
(c) il fuoco va sulla cella di stato timbrata all'arrivo sul fascicolo; (d) `role="progressbar"` e
i suoi cinque `aria-*` passano dall'ex `<div>` all'`<ol class="wizard__rail">`, invariati;
(e) nessuna seconda live region per il TIMBRO: l'annuncio generico esiste già lato server.

**6.2 Regola dura.** Nulla che si ripete dalla tastiera si anima. Non ci sono più frecce di
tablist da ripetere; resta il caso `event.repeat === true` su `Enter`/`Space` di un `<summary>`,
dove il browser non emette `toggle` ripetuti. Il commit del wizard è protetto da `form.dataset.busy`,
che è la stessa guardia del doppio POST.

**6.3 Reduced motion è uno stato completo.** `@view-transition` è dentro
`@media (prefers-reduced-motion: no-preference)` — **misurato onorato**: con la preferenza emulata,
due caricamenti consecutivi riportano `pagereveal` con `viewTransition: false`. Ogni `@keyframes` e
ogni `transition` di questo foglio sta dentro lo stesso blocco. `withMotion()` ha il suo `settle`
su ogni chiamata. Nessun elemento resta a `opacity: 0`: i pseudo-elementi che non si animano non
sono resi affatto, e nessun contenuto reale dipende da loro. La preferenza si legge dal vivo.

**6.4 Il contratto che vale se una tab tornasse.** Stato semantico nel fotogramma dell'azione;
`[data-leaving]` per l'uscita; `hidden` su `animationend` **o** subito sul percorso di
annullamento, il primo dei due; nessuna correttezza appesa a `transitionend`. Scritto qui perché
la revisione ha ragione a pretenderlo, anche se oggi non c'è nulla che lo usi.

**6.5 RTL.** Non c'è **nessun** `translateX` in questa superficie tranne la foglia di registro; la
direzione è espressa dal bordo da cui una riga cresce (`--sill-a`/`--sill-b`). Le quattro
combinazioni lingua × verso sono state lette a runtime (§ 4.1). Non si specchia ciò che non è
direzionale: la rotazione del glifo `+`, l'opacità, lo `scaleX` del timbro (che comprime, non
scorre), il cedimento di 1 px sull'asse di blocco. Copertura da aggiungere a
`tests/i18n/test_rtl_browser.py`.

**6.6 forced-colors.** Sill, rail, commit e timbro passano a `Highlight` con
`forced-color-adjust: none`; la traccia vuota del rail passa a `GrayText` su `Canvas`. Le View
Transitions **restano attive** (§ 4.7). Il fuoco usa l'outline di sistema.

**6.7 Contrasti di questa superficie, tutti ricalcolati in questa tornata.**

| Coppia | Rapporto | Uso |
|---|---:|---|
| `--terr-line-lt` `#0F6A72` / `--min-0` | **5,692** | sill, rail pieno, commit, timbro |
| `--terr-line-lt` / `--hairline` `#D3D2CC` | **4,169** | segmento fatto contro segmento da fare (WCAG 1.4.11 ≥ 3) |
| `--hairline-strong` `#7A868B` / `--min-0` | **3,373** | ultimo segmento tratteggiato |
| `--min-0` su `--accent` | **5,692** | etichetta del bottone primario |
| `--accent-hover` `#0B555C` / `--min-0` | **7,668** | hover |
| `--accent-ring` `#1D8A93` / `--min-0` | **3,704** | anello di fuoco (quando il token sarà ripuntato, § 1.10) |
| `--ink` / `--min-0` | **14,624** | corpo, invariato |

Nota di margine, poiché ho ricalcolato tutto: `v2/tokens.css:54` commenta `--pending-700` come
«6.7:1 on --min-0»; il valore calcolato è **6,294:1**. Passa comunque; il commento va corretto da
chi possiede quel file.

---

## 7. PRESTAZIONI — misurate, non stimate

**Byte, gzip, tutti rimisurati.**

| Voce | gzip | Nota |
|---|---:|---|
| `static/css/v3/transitions.css` | **+2 098 B** | come scritto, 8 436 B sorgente (i nove blocchi di § 4 concatenati); 1 610 B se minificato |
| `static/js/dist/soglia.js` | **+1 526 B** | 3 354 B minificato, Motion esterno |
| `static/js/head.js` | **+70 B** | 198 → 268 |
| `apps/orientation/static/orientation/wizard.css` | **−261 B** | 21 classi + le regole della barra |
| `static/js/main.js` | **−802 B** | `initTabs` + `initSteppers` + `initAccordions`, 101 righe |
| `orientation/wizard.js` non più caricato su `step.html` | **−493 B** e una richiesta | resta su `result.html` per `.js-print` |
| **Bilancio netto per pagina** | **+2 631 B** | ≈ 2,6 KB |

JavaScript totale su una pagina STANDARD dopo la modifica: `main.js` 4 457 + `shell.js` 604 +
`soglia.js` 1 526 + chunk Motion 26 201 + `head.js` 268 = **33 056 B gzip ≈ 32,3 KB**, contro un
tetto di 45 KB. HTMX (14 KB) è **evitato**, non rimandato.

**Layout e paint, dalla traccia CDP con riferimento a riposo.** Traccia di riposo su 560 ms:
**zero** eventi `Layout` e `Paint`.

| Animazione | Layout | Paint | Quando |
|---|---:|---:|---|
| `soglia.sill` (320 ms) | 3 | 7 | a 0,4 / 64,3 / 566,3 ms e 1,2 / 1,6 / 64,7 / 64,9 / 566,7 / 567,0 ms — cioè **creazione della scatola e smontaggio**; fra 65 e 566 ms, per tutta l'animazione, **nulla** |
| `timbro` (120 ms + molla) | 4 | 10 | a 0,6 / 26,7 / **88,5** / 521,1 ms — l'88,5 è il fotogramma in cui nasce il `::before`, il 521 è la rimozione della tabella di prova; fra 91 e 521 ms **nulla** |
| `respiro.details` (240 ms) | **16** | 28 | 2 al montaggio (0,5 · 2,2 ms) e **14 durante l'animazione**, uno per fotogramma, da 20,3 a 234,6 ms: **l'eccezione dichiarata** (EMENDAMENTO 1) |

**Verifica finale del foglio, assemblato dai nove blocchi di § 4 e servito alla FAQ viva.**
39 regole di primo livello, 6 `@keyframes` — tutti dentro
`@media (prefers-reduced-motion: no-preference)` — e:

- **zero blocchi di dichiarazione vuoti**, percorrendo ricorsivamente `sheet.cssRules`. È la prova
  diretta che nessuna dichiarazione cade in fase di parsing: era esattamente il sintomo delle tre
  `transform-origin: inline-start|block-start` della revisione 1, che producevano `#sel { }`;
- **zero `cubic-bezier(` letterali**: ogni curva arriva da un token, quindi il conteggio di
  `tests/frontend/test_motion_system.py` sul CSS compilato non è toccato da questo foglio;
- `main` nominato `ile-main`, `:root` a `interpolate-size: numeric-only`, `.faq-item` a
  `allow-keywords`, `--sill-a: left`;
- `<summary>` alto **76 px** a 1440 **e** a 390 (≥ 44 px);
- **nessun errore né avviso in console**, CSP compreso.

**Guadagno netto.** Il wizard passa da una navigazione completa per domanda a una richiesta e uno
scambio di sottoalbero; la barra che animava `inline-size` (proprietà di layout, vietata da
MOTION_SYSTEM § 2) sparisce insieme alle sue 21 classi.

**Prova richiesta prima dell'accettazione**: pannello Performance durante ogni voce di § 5 — 0
layout/paint oltre il primo fotogramma salvo `respiro.details`; INP < 200 ms su `toggle` di
`<details>` e invio della risposta; CPU rallentata 4×; 390 px; `prefers-reduced-motion: reduce`;
`forced-colors: active`; `dir="rtl"`.

---

## 8. MODIFICHE RICHIESTE FUORI DAL MIO FOGLIO

Elenco chiuso. Una specifica che dice «nessuna modifica al contratto» e poi ne richiede sei è la
cosa che la revisione ha giustamente chiamato falsa.

| File | Modifica |
|---|---|
| `static/css/main.css` | una riga: `@import url("v3/transitions.css");` in coda |
| `templates/base.html` | `<script type="module" src="{% static 'js/dist/soglia.js' %}">` accanto a `dist/shell.js` |
| `static/js/head.js` | il listener `pagereveal` di § 4.8 (+70 B gzip) |
| `static/js/src/shell.js` | una riga dentro il callback di `inView`: `if (document.documentElement.dataset.arrival) { settleAll(); return; }` |
| `static/js/main.js` | cancellare `initTabs`, `initSteppers`, `initAccordions` e le loro tre chiamate |
| `templates/orientation/_step.html` | la barra diventa `<ol class="wizard__rail" role="progressbar" …>` con i cinque `aria-*` **invariati**; `id="orientation-step"` prende `data-sill`, `data-step-status="{{ … }}"`; il form perde i **quattro** `hx-*` e prende `data-step-form data-step-saving="{% translate 'Enregistrement…' %}"` |
| `templates/orientation/step.html` | `<p class="visually-hidden" id="wizard-status" role="status" aria-live="polite" aria-atomic="true"></p>` **fuori** da `#orientation-step`; il blocco `extra_scripts` sparisce |
| `apps/orientation/static/orientation/wizard.js` | i due listener `htmx:*` si cancellano (non possono scattare); resta `.js-print` per `result.html` |
| `apps/orientation/static/orientation/wizard.css` | le 21 classi `--*`, `.wizard__progress-bar`, `.wizard__progress-fill` e la sua transizione |
| `apps/orientation/templatetags/orientation_tags.py` | il filtro `progress_class` resta senza chiamanti: si cancella |
| **`apps/orientation/tests/test_compliance.py:124`** | `assert form["method"] == "post" and form["hx-post"] == url` → `assert form["method"] == "post" and form["action"] == url and form.has_attr("data-step-form")`. **Le righe 118-121 non cambiano**: `role="progressbar"` e i cinque `aria-*` sopravvivono sull'`<ol>` |
| `templates/cases/detail.html` | `<tr data-row-key="{{ item.pk }}">`; `data-stamp-form` sui due form di stato; `data-row-key="case"` sulla `.case-header__fact` dello stato |
| `templates/cases/index.html` | `data-vt-name="ile-register"` sull'`<ol class="register">`, `data-vt-name="ile-ref-{{ row.case.reference }}"` sul `.t-ref`, `data-vt-name="ile-state-{{ row.case.reference }}"` sulla `.state` |
| `templates/portal/partials/case_header.html` | gli stessi due `data-vt-name` sul `.case-header__reference` e sulla `.state` |
| `templates/components/tabs.html`, `stepper.html` | restano su disco **fuori servizio**; il modello tastiera del documento di accessibilità (e la lista di controlli di `tests/frontend/test_design_docs.py:794-809`, che cita `templates/components/tabs.html`) va annotato di conseguenza da chi possiede quel documento |
| `templates/components/accordion.html` | `single` e l'attributo `name` escono dal contratto (lacuna 1) |
| `MOTION_SYSTEM.md` § 6 | le undici voci di § 5 |

---

## 9. RISCHI E PROVE ANCORA DA FARE

1. **Sembrare una SPA scadente.** *Guardia*: nessuna uscita animata, uscite a 120 ms fisse,
   nessuna voce oltre 320 ms, stato semantico sempre scritto nel fotogramma dell'azione.
2. **Il nome duplicato che annulla la transizione.** Due `.register` convivono in
   `cases/detail.html`. *Guardia*: `arm()` conta i nomi e arma solo gli unici (§ 4.9); e il
   fallimento degrada alla navigazione di oggi.
3. **Il timbro su un cambio non avvenuto.** *Guardia*: scadenza 10 s, consumo immediato, e timbro
   **solo** se il testo di stato letto adesso è diverso da quello memorizzato al `submit`.
4. **Il rail che mente** su un questionario adattivo. *Guardia*: ultimo segmento tratteggiato,
   «au maximum» in `aria-valuetext`, mai una percentuale presentata come certezza.
5. **`attr()` tipizzato non è ovunque.** Dove non c'è, la dichiarazione è invalida e il nome resta
   `none`: nessun VARCO, nessuna regressione. Misurato il fallback su valore non valido.
6. **L'anello di fuoco è ancora navy** (§ 1.10). Non è mio, ma ogni stato di fuoco che ho scritto
   lo eredita.

**HUMAN_QA_REQUIRED** — quattro prove che una macchina headless non può chiudere:
1. NVDA + Firefox e VoiceOver + Safari sul wizard: posizione e domanda non devono sovrapporsi nel
   parlato; e sul fascicolo, il `role="status"` del server seguito dal fuoco sulla cella timbrata
   non deve produrre doppio parlato.
2. Il VARCO **sul portale autenticato**: le geometrie di § 4.7 vengono da un rig fedele ai due
   markup ma servito fuori dall'area riservata, che questa sessione non poteva raggiungere. Vanno
   rimisurate sulla pagina vera, a 1440 e a 390.
3. `::details-content` + `interpolate-size` su Safari ≥ 18.4 e Firefox; e `attr()` tipizzato sugli
   stessi.
4. `forced-colors: active` **con** le View Transitions attive, su Windows High Contrast reale: se
   l'istantanea non rispetta la mappatura, si aggiunge
   `@media (forced-colors: active) { @view-transition { navigation: none } }` — una riga, già
   scritta qui, non ancora inserita perché disattivarle senza prova toglie continuità proprio a chi
   ne ha più bisogno.
