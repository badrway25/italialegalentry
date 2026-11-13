# HERO-DOORWAY V3 — «LA SOGLIA»

Round 2 · riscrittura integrale dopo la revisione indipendente (`docs/design-v3/reviews/hero-doorway.md`).

Superficie: `templates/pages/home/_hero.html` · `static/css/v2/hero.css` · `static/css/v3/hero-doorway.css` (nuovo) ·
`scripts/territory.py` · `static/js/src/home.js`. Vincolanti: `DESIGN_SYSTEM_V2.md` § 8.3 / § 8.4 / § 11 ·
`MOTION_SYSTEM.md` · `BRAND_ASSETS.md` § 1–2 · `apps/cms/forbidden.py`. Coordinamento con
`docs/design-v3/specs/imagery.md` § 4.2 (gradazione `-notte`) e § 4.6.

**Tutte le misure di questo documento sono state rifatte** in Chromium headless (Playwright del `.venv`,
browser proprio, **mai la porta 9222**) il 24 settembre 2026 su `http://127.0.0.1:8771/fr/`, a 1440×900,
1440×800, 1366×768, 1280×800, 1200×900, 1024×768, 768×1024, 430×932, 390×844. Metodo e file in § 12.
Nessun numero è riportato dal round 1 senza essere stato ricalcolato.

---

## 0. RICHIESTE DI EMENDAMENTO (numerate, vincolanti per l'approvazione)

Cinque. Nessun'altra deviazione dai documenti vincolanti esiste in questa specifica; se ne trovate una,
è un difetto, non una scelta.

### EMENDAMENTO 1 — `DESIGN_SYSTEM_V2.md` § 8.3: «i nodi degli attori … (persona · organismo di formazione · università · autorità competente · impresa · istituzione)» con «etichette mono»

**Che cosa chiedo.** Quattro toponimi visibili invece di sei nodi etichettati, in **serif 13 px** invece che
in mono; il sesto attore — l'**autorità competente** — non è un nodo del campo ma **la soglia stessa**, e il
suo nome vive solo nella `<figcaption>`; «organismo di formazione» e «università» restano **un solo nome**.

**Perché.** (a) I quattro nomi visibili sono, verbatim, i quattro msgid pubblici di `content.ENTRANCES`
(`Personnes` · `Entreprises` · `Institutions` · `Universités et organismes de formation`): il prodotto ha
**quattro** porte d'ingresso, non sei, e inventarne una quinta e una sesta nell'eroe contraddirebbe
`apps/pages/content.py`. (b) Disegnare l'«autorità competente» come un attore che **cammina verso la porta**
direbbe che l'autorità partecipa al percorso della piattaforma: è falso e contraddice
`content.TRUST_DOES_NOT` («ces décisions relèvent des autorités compétentes»). L'autorità **è** il passaggio,
non un viaggiatore: perciò è il filetto della soglia. (c) Le «etichette mono maiuscole» sono, alla lettera,
l'idioma che la revisione ha nominato come il più riprodotto del 2024-2026 (§ Segnali 1). Misura:
`UNIVERSITÉS ET ORGANISMES DE FORMATION` in `--f-mono` 13 px `.08em` maiuscolo = **335,9 px** su una sola
riga (misurato in Chromium, § 12.3) — non entra da nessuna parte nella composizione; in serif 13 px su due
righe è **140,0 px**. La regola tipografica che adotto è cartografica e difendibile davanti a un direttore
artistico: **le coordinate si compongono in mono** (la striscia di chiusura resta mono, invariata) **e i
toponimi in serif**. Sono due cose diverse, e la differenza tipografica lo dice.

**Che cosa costa.** L'eroe porta due registri di piccolo corpo invece di uno. Se il consiglio rifiuta,
i quattro nomi tornano in `--f-mono` 13 px maiuscolo: `Personnes` 79,6 px, `Entreprises` ~92 px,
`Institutions` ~93 px entrano; `Universités et organismes de formation` **non entra** e andrebbe spezzato in
tre righe da ~112 px — e allora chiedo invece di sostituirlo con il solo `Universités`, che è una deriva
editoriale e richiede un msgid nuovo. Il ripiego peggiore è il rifiuto di entrambi: in quel caso i quattro
nomi spariscono dal disegno e restano solo nella `<figcaption>`; la tesi regge, la lastra tace.

### EMENDAMENTO 2 — `DESIGN_SYSTEM_V2.md` § 8.4: «fotografia del titolare dentro l'arco (opacità .50, saturazione .8, vignetta `--mid-1` con velo teal in alto)» e «Scroll: la fotografia scorre di 18 px»

**Che cosa chiedo.** (a) `opacity: 1` e **nessun `filter` a runtime**: la gradazione è cotta nel derivato
(`imagery.md` § 4.1, regola 1), con la gradazione `-notte` di `imagery.md` § 4.2 (nero `#0b171e`, bianco
`#c8d4d6`, saturazione 0,66, −6 % di luminanza media). (b) Il **velo teal** in alto sparisce; la vignetta è
ritarata (§ 7.2). (c) Un **ritaglio duro 3:4** nel derivato, al posto di un master 3:2 dentro un riquadro 3:4.
(d) La **parallasse di 18 px sullo scroll è rimossa**.

**Perché.** Misurato sullo schermo di oggi (§ 1.2): la fotografia **non riempie l'arco**. Il suo riquadro di
layout è 378 × 252 px dentro un arco di 378 × 504,7 — **il 49,4 % della porta**; sotto `door-y ≈ 267` non c'è
nessuna fotografia, solo il gradiente. Campionamento dei pixel di `fr_1440.png`: le righe 0→265 hanno
struttura, le righe 275→500 sono uniformi a `rgb(14, 27, 35)` = `--mid-1`, luminanza relativa **0,0100** —
cioè il fondo nudo. Il titolare dice «non abbastanza immagini»; su questa superficie metà dell'unica immagine
non è mai stata disegnata. Con il ritaglio 3:4 e la gradazione cotta la luminanza media della parte
fotografica visibile passa da **0,0283** (metà superiore, oggi) a **0,0820** (simulazione sul master reale,
§ 12.4): ×2,9 sulla parte che si vede, ×8,2 sulla metà che oggi non esiste.
Sul punto (d): `MOTION_SYSTEM` § 4 concede **un** oggetto indicizzato allo scroll **per pagina**; la home ne
ha due dal giorno uno (`home.js:95` parallasse della fotografia e `home.js:118` la rotta di § 8.6). Tolgo il
primo. 18 px di deriva su una fotografia sono decorazione; la rotta del processo è orientamento.

**Che cosa costa.** Due derivati nuovi per misura (`doorway-notte-{480,800,1200}.{avif,webp}`), con il
ritaglio 3:4; i vecchi 3:2 restano per nessuno e si cancellano. La chiave **non** è toccata: siede sull'arco
interno `--brand-navy` **pieno**, quindi il suo rapporto resta **5,80:1**, ricalcolato (§ 12.2). L'eroe perde
il suo oggetto legato allo scroll: è la perdita che rende la pagina conforme, e non ne chiedo un altro.

### EMENDAMENTO 3 — `DESIGN_SYSTEM_V2.md` § 8.3: «Capitolo `--mid-1` … ≤ 110 % del viewport a 390»

**Che cosa chiedo.** La soglia diventa **≤ 125 % a 390 px**, con la condizione aggiuntiva e verificabile che
**la CTA primaria stia interamente sopra la piega**.

**Perché — la clausola attuale è aritmeticamente insoddisfacibile, e lo dimostro con i numeri.** A 390×844 il
budget è 928,4 px. L'altezza irriducibile dello stack, con i testi bloccati e la porta alla misura che § 8.3
prescrive (220 px), misurata elemento per elemento in Chromium (§ 12.5): porta 293,3 + titolo 100,5 + lead
57,2 + azioni 110,0 + corpo 196,0 + striscia coordinate 104,0 = **861,0 px di solo contenuto**, prima di un
solo pixel di margine. Con i margini minimi che la scala di spazio ammette (24 + 24 + 24 + 20 + 24 + 24 = 140)
si arriva a **1 001 px = 118,6 %**, senza alcun respiro. Il documento chiede 110 %: non è raggiungibile
senza tagliare un testo prescritto o rimpicciolire la porta sotto la misura che lo stesso § 8.3 impone.
**E oggi il sito è a 132,4 %**: misurato, `.hero` = **1 117,7 px** a 390×844, con **330,7 px sotto la piega**
(§ 1.1). La revisione afferma «Today `heroBelowFold = 0`»: **è falso, e lo contesto con la misura** (§ 2,
punto D). Questa specifica porta il valore a **1 036,4 px = 122,8 %** con la porta **alzata** da 180 a 220 px
— cioè 81,3 px in meno di oggi **mentre** rende conforme la misura della porta.

**Che cosa costa.** Il documento ammette per scritto che il primo schermo del telefono non contiene l'eroe
intero. Contropartita verificabile: la CTA primaria termina a **y 743,4** su 844 (misurato), cioè
interamente visibile con 100,6 px di margine, e la porta è finalmente della misura prescritta. Se il
consiglio rifiuta, l'unica leva restante è il corpo (196 px, 7 righe a 17/28): portandolo a `--t-small`
14/20 si recuperano ~76 px e si scende a **≈ 960 px = 113,7 %**, ancora sopra 110 %, con un corpo di testo
giuridico a 14 px su telefono. Lo sconsiglio e non lo scrivo nella specifica.

### EMENDAMENTO 4 — `DESIGN_SYSTEM_V2.md` § 11: «`[dir="rtl"]` specchia gli SVG decorativi (`scaleX(-1)`)»

**Che cosa chiedo.** Il territorio dell'eroe (isoipse, graticola, lastra) **non si specchia in nessuna
lingua**. La regola `[dir="rtl"] .hero__territory { transform: scaleX(-1) }` (`hero.css:567`) si cancella e
non viene sostituita.

**Perché.** Il territorio non è decorativo: porta una geografia **dichiarata e stampata in chiaro** nella
striscia di chiusura — `33.97° N · 6.85° W` a sinistra, `45.41° N · 11.88° E` a destra, nelle quattro lingue,
in numerali occidentali per § 3.1. Specchiarlo mette il Veneto a nord-**ovest** e rende **false** due cifre
scritte sulla stessa riga. Il § 1.8 del round 1 imputava questa contraddizione al codice; la revisione ha
giustamente osservato che specchiare solo i tracciati la riproduce un piano più sotto. La risposta corretta
non è specchiare di meno: è **non specchiare affatto**. Una carta non si specchia per l'arabo, e
`MOTION_SYSTEM` § 5 lo dice già («non si specchia ciò che non è direzionale»): la direzione di lettura non
è un punto cardinale.

**Che cosa costa.** In `/ar/` la persona entra dal lato sinistro dello schermo, cioè contro il senso di
lettura. È un costo reale e lo dichiaro; è minore di quello di stampare due coordinate sbagliate.
`tests/i18n/test_rtl_browser.py` va aggiornato e `scripts/territory.py` **non** produce più varianti `-rtl`.
Lo strato dei nomi porta `dir="ltr"` come contesto di **posizionamento** (§ 9.3), con `dir="auto"` su ogni
`<span>` perché il testo arabo resti arabo.

### EMENDAMENTO 5 — `DESIGN_SYSTEM_V2.md` § 8.4: «gradini posati (stagger 100)»

**Che cosa chiedo.** Lo stagger dei tre gradini passa da **100 ms a 60 ms**.

**Perché.** `MOTION_SYSTEM` § 1 ammette «ritardi scaglionati di **40–60 ms** per riga» e nient'altro. I due
documenti vincolanti si contraddicono; il sistema di moto è dichiarato normativo da `DESIGN_SYSTEM_V2` § 5,
quindi vince. Nella stessa riga correggo due valori che **non** hanno documento dietro e sono quindi difetti,
non emendamenti: `home.js:39` stagger 0,08 (80 ms) sul titolo → 60 ms, e `home.js:91` `duration: 0.5`
(500 ms) sull'assestamento della chiave → `--motion-slow` (320 ms), perché 500 non è una delle quattro durate.

**Che cosa costa.** I gradini si posano 80 ms prima. Nessun'altra conseguenza.

---

## 1. LO STATO DI OGGI, RIMISURATO

Il § 1 del round 1 non è stato smontato dalla revisione e non lo riscrivo per intero; qui stanno **solo** i
punti che ho ricalcolato e i **tre fatti nuovi** che il round 1 non aveva visto e che cambiano la specifica.

**1.1 L'eroe non sta nella pagina, e non è mai stato a zero.** `getBoundingClientRect()` su `.hero`:

| viewport | `.hero` altezza | sotto la piega | % del viewport | budget § 8.3 |
|---|---:|---:|---:|---|
| 1440 × 900 | **900,0** | **+102,0** | 100,0 % | ≤ 100 vh — l'eroe parte a y 102 sotto la testata |
| 1280 × 800 | 889,2 | +191,2 | 111,2 % | — |
| 1024 × 768 | 883,3 | +217,3 | 115,0 % | — |
| 768 × 1024 | 1 206,6 | +284,6 | 117,8 % | — |
| **390 × 844** | **1 117,7** | **+330,7** | **132,4 %** | **≤ 110 % → sforato di 189,3 px** |

Causa misurata: `.hero` porta `padding-block: 96px` a desktop e `48px` sotto 48 rem, ereditato dal foglio di
base. A 1440×900: 96 + `.hero__inner` 642 + `.hero__coords` 65 + 96 = 899 px, di cui **192 px di padding che
il territorio riempie e nient'altro**. Sono 192 px di composizione regalati, ed è da lì che questa specifica
prende lo spazio per la lastra, **senza aggiungere un pixel all'altezza dell'eroe**.

**1.2 Metà della fotografia non è mai stata disegnata.** `.doorway__img` dichiara `inline-size: 100%` e
`block-size: 100%`, ma il genitore è un `<picture>` in `display: inline`: l'altezza percentuale si risolve in
`auto`, il riquadro di layout diventa **378 × 252 px** (il rapporto 3:2 del master 800 × 533), e
`object-fit: cover` non ha nulla da fare perché il riquadro **è già** il rapporto dell'immagine. Riquadro
misurato con `scale(1.06)`: **400,7 × 267,1** — ed è esattamente il numero che `imagery.md` § 1.2 riporta come
«la lastra della porta». Campionamento dei pixel (§ 12.4): struttura fino a `door-y 265`, poi
`rgb(14, 27, 35)` uniforme fino al fondo. **La fotografia copre il 49,4 % dell'arco.** Questo, e non
l'opacità .50, è la ragione per cui «l'arco legge come una macchia grigia».

**1.3 La rotta di oggi usa il colore sbagliato.** `hero.css:74` dà a `.terr__route` `stroke: var(--accent-dark)`.
`DESIGN_SYSTEM_V2` § 1.3 regola 2 assegna la rotta a `--terr-line`, e la regola 1 riserva l'accento a link,
CTA primaria e anello di focus. È una violazione già in produzione, sulla mia superficie: la correggo (§ 5.3).

**1.4 La gerarchia invertita, ricalcolata.** Isoipse 1 `#3fa6af` @ .62 → composito `#2c717a` = **3,13:1** su
`--mid-1`; isoipse 2 @ .38 → `#215058` = **1,96:1**; graticola `#eef2f1` @ .055 → **1,14:1**; tacche @ .18 →
**1,69:1**. Confermati al centesimo. Il terzo gradino `--accent-dark` @ .24 → `#29474e` = **1,76:1**, sotto il
3:1 di WCAG 1.4.11. Confermato.

**1.5 La marea, ricalcolata onestamente.** `tide-1`: 12 px in 28 s = **0,43 px/s**; `tide-2`: 9 px in 34 s =
**0,26 px/s**. Separazione relativa massima fra i due strati: **21 px**. Confermato. Nota che il round 1 aveva
sbagliato a chiamare «1,92 px/s» una velocità relativa: la correzione è in § 8.

---

## 2. COME QUESTO ROUND RISPONDE ALLA REVISIONE

Venti MUST-FIX. **Diciannove DONE, uno DISPUTATO con la misura.** Nessun terzo stato.

| # | MUST-FIX | Esito | Dove · con quale numero |
|---|---|---|---|
| 1 | Geometria morta a 1440: il campo eredita la colonna 5fr (503,3 px) e la porta si stringe a 341 px | **DONE** | Confermo la colonna: `grid-template-columns` calcolato = `704.656px 503.328px`, `gap: 32px`. La lastra **non** è più nella colonna: `.hero__field` è largo **esattamente quanto la porta** e la lastra è disegnata nell'`overflow` visibile dell'SVG della porta, in coordinate della porta (§ 4.1). Porta misurata dopo la modifica: **380,0 × 506,7 px a 1440, 1280 e 1024** — invariata. |
| 2 | `.field__caption{inset:0;z-index:4}` senza `pointer-events:none` uccide l'hover della porta | **DONE** | Lo strato dei nomi e **tutti e tre** gli SVG portano `pointer-events: none` (§ 6); l'hover di § 8.4 si sposta da `.doorway` a `.doorway__arch, .doorway__cross`, così la lastra non sale con la porta. |
| 3 | Il draw-on è impossibile su tre tracciati su quattro (dasharray decorativo) | **DONE** | **Non esiste più un solo `stroke-dasharray` decorativo.** Un solo inchiostro (`--terr-line`) in quattro valori e quattro spessori; gli attori si distinguono per posizione, spessore, geometria e nome. `strokeDashoffset 1→0` con `pathLength="1"` funziona su ogni tracciato. |
| 4 | La dorsale dipinge sopra la chiave | **DONE per geometria, senza maschera.** | L'ascesa è `M190 548 V374.8`: **finisce sul filetto della soglia** e non entra mai nel riquadro dell'arco navy (`x 91,7…288,3 · y 70,2…374,8`). La riemersione comincia a `y −3`, cioè **sopra la volta**. Fra 374,8 e 0 non c'è nessun tracciato: è la sparizione, ed è anche il tempo morto dell'animazione (§ 8). |
| 5 | `field__paths` vs `field__spine`: handoff e dasharray condivisi mai definiti | **DONE** | I due nomi sono spariti. Tre `<svg>` dentro la porta, a ruoli disgiunti (§ 5.2): `doorway__field` (dietro), `doorway__trace` (l'arco, § 8.4, invariato), `doorway__cross` (davanti); due animazioni indipendenti, ciascuna su **un** tracciato, ciascuna con il proprio `pathLength="1"`; nessun `stroke-dasharray` riscritto da JS; nessuno stato condiviso (§ 8). |
| 6 | `.doorway__sill` a 69,4 % non cade sulla soglia | **DONE** | Il filetto non è più un `div` con una percentuale: è una `<line>` nello **stesso viewBox della porta**, a `y = 374,8`. Derivazione: piede dell'arco navy = `1,5 + 13,7 % × 503,67 + 52 % × 377 × 1,55 = 374,4`; misurato sul DOM = `668,1 − 293,3 = ` **374,8**. In percentuale dell'altezza della porta: **73,97 %** (la revisione calcolava 74,16 % dal viewBox del round 1; la differenza è il bordo da 1,5 px dell'arco). Uso 374,8 in unità, non una percentuale, così la questione non si ripresenta. |
| 7 | I dati di path non esistono | **DONE** | § 4.3: tabella dei nodi **e** le stringhe `d` complete, generate con la funzione `to_path()` già in `scripts/territory.py` (Catmull-Rom → Bézier cubiche, tensione 1/6). Continuità tangenziale a `Nf(−20, 557)`, che è insieme il quinto nodo di I e l'ultimo di II: tangente di I `(186, −10)` = **−3,08°**, tangente d'arrivo di II `(98, 9)` = **+5,25°**, **angolo di giunzione 8,32°**. Non è zero **di proposito**: due linee che si toccano con tangente identica leggono come **una** linea piegata; un affluente entra con un angolo, e 8° è l'angolo più piccolo che si legge ancora come giunzione a 1,5 px di tratto. |
| 8 | Ancoraggi delle etichette assenti, e l'unico dato è sbagliato | **DONE** | Tutti e quattro, per tutte le larghezze, in § 6: `--lx` è una percentuale della **larghezza** della porta, `--ly` dell'**altezza** della porta, e il riquadro contenitore coincide con la porta per costruzione. **Nessuno script scrive nel CSS**: i valori sono costanti scritte a mano in `hero-doorway.css`, e `tests/frontend/test_field_anchors.py` verifica che coincidano con quelle emesse da `territory.py` (§ 11). Riquadri misurati dopo l'impianto in § 12.5. |
| 9 | I conteggi si contraddicono | **DONE** | Un solo inventario, § 4.2: **4 canali · 6 stazioni · 1 confluenza (2 archi) · 1 soglia · 4 nomi**. La `<figcaption>` nomina le stesse cose e nient'altro. Le cinque didascalie di nodo del round 1 sono state **cancellate**: non esistono più né in HTML né in SVG. |
| 10 | Il telefono sfonda § 8.3 e nasconde le CTA | **DONE (+ EMENDAMENTO 3)** | La lastra **non esiste** sotto 48 rem: costa **0 px** di altezza. Misurato dopo l'impianto: `.hero` = **1 036,4 px a 390×844 (122,8 %)** contro **1 117,7 px (132,4 %)** oggi, **con la porta alzata da 180 a 220 px** come § 8.3 prescrive. CTA primaria: fondo a **y 743,4** su 844. La clausola «110 %» è insoddisfacibile: dimostrazione aritmetica nell'Emendamento 3. |
| 11 | Il guadagno dell'hover è sotto la percezione | **DONE per cancellazione** | I tracciati «fantasma» a `.22 → .30` (**1,43:1 → 1,68:1**, ricalcolati) sono **spariti**. Non c'è nessun hover sulla lastra. L'unico hover resta quello di § 8.4 sulla porta, che è decorativo, su un blocco `aria-hidden`, e non ha né deve avere un equivalente da tastiera. |
| 12 | La cifra gzip è sbagliata del ~50 % | **DONE — la revisione ha ragione, con il suo numero** | Ricompresso io: i tre partial reali, 31 289 B → **11 965 B** con `gzip -9`, rapporto **2,62:1**, identico alla revisione. (Comprimendo i tre file **separatamente** si ottiene 12 373 B / 2,53:1: la differenza è il dizionario condiviso; la cifra che conta è quella del flusso unico, 2,62:1.) Il «≈ 4:1» del round 1 è cancellato. Bilancio reale in § 10. |
| 13 | La formulazione vietata è sorvegliata solo in FR | **DONE** | `tests/compliance/test_public_pages.py::test_no_forbidden_formulations_on_public_pages` esegue già `cms.forbidden.scan()` su **ogni rotta pubblica in ogni lingua**: è il cancello, e lo nomino. Nota per il traduttore sul msgid in § 9.1. |
| 14 | L'RTL riproduce la contraddizione del § 1.8 | **DONE (+ EMENDAMENTO 4)** | Non si specchia **niente**: né terreno, né lastra, né tracciati. Cade `hero.css:567`. Lo strato dei nomi usa proprietà logiche dentro un contesto di posizionamento `dir="ltr"` con `dir="auto"` su ogni `<span>` (§ 9.3). |
| 15 | `.field__item` non è mai azzerato sul telefono | **DONE** | Non c'è più nessun `<li>` assoluto da azzerare: i nomi sono quattro `<span>` dentro uno strato che è `display: none` sotto 48 rem e che, fra 48 e 64 rem, vive **dentro la prima riga della griglia** insieme alla porta (§ 6). |
| 16 | La marea strappa il bordo e contraddice il suo token | **DONE** | **28 s** (`--motion-ambient`), un solo periodo per entrambi gli strati — spariscono i 24 s del round 1 **e** i 34 s di `calc(var(--motion-ambient) + 6s)` che sono in produzione. Overscan dichiarato: i tre `<svg>` del territorio passano da `inset: 0` a `inset: -24px -32px`; corsa massima 26 px orizzontale (< 32) e 20 px verticale (< 24), quindi **nessuna striscia vuota può entrare**. Velocità ricalcolate: 26/28 = **0,93 px/s** per lo strato più veloce (oggi 0,43), separazione relativa 46 px contro 21 px = **×2,2**. Il «1,92 px/s» del round 1 confondeva una velocità relativa con una velocità: cancellato. |
| 17 | Il `sizes` della fotografia diventa sbagliato | **DONE** | La porta resta a 380 / 300 / 220 px **esatti** (misurati: 380,0 a 1440-1024; 300,0 a 768; 220,0 a 390). `sizes` riscritto in § 7.3, coerente con `imagery.md` § 4.6. |
| 18 | La «proiezione deterministica» non viene mai usata | **DONE per ritiro** | La pretesa è cancellata dalla specifica. La lastra è un **disegno autorato**, non una proiezione, e lo dico. Le sole coordinate reali della pagina restano le due della striscia di chiusura, già stampate verbatim — ed è anche la ragione dell'Emendamento 4. |
| 19 | Rispondere alla vera accusa del titolare su questa superficie | **DONE, ed è il cuore del round 2** | § 1.2 e § 7: la fotografia passa dal **49,4 %** della porta al **100 %**, con un ritaglio duro 3:4, la gradazione `-notte` cotta nel derivato, nessun `filter` a runtime, vignetta ritarata; luminanza media della parte fotografica visibile da **0,0283** a **0,0820** (misura + simulazione sul master reale, § 12.4). In più: una **luce d'apertura** dietro l'arco (§ 4.4) e una banda di terreno sotto la porta. Provino a confronto: `…/scratchpad/hero3/arch_compare.png`. |
| 20 | La regola `forced-colors` si contraddice | **DONE per cancellazione** | `forced-color-adjust: none` **non compare da nessuna parte** in questa specifica. Colori di sistema e differenziazione per spessore e geometria (§ 9.4). |

**Punto contestato.** Uno solo, ed è nel MUST-FIX 10:

> **D. «Today `heroBelowFold = 0`» è falso.** Misurato con il mio browser, senza toccare il repository:
> a 1440×900 `.hero` è alto **900,0 px** e il suo bordo inferiore cade a **y 1 002**, cioè **102,0 px sotto la
> piega**; a 390×844 è alto **1 117,7 px** e cade a **y 1 174,7**, cioè **330,7 px sotto la piega**, pari al
> **132,4 %** del viewport contro il 110 % che § 8.3 impone. Metodo: `.hero.getBoundingClientRect().bottom −
> window.innerHeight`, senza scroll, su `http://127.0.0.1:8771/fr/`, Chromium headless, `deviceScaleFactor: 1`
> (§ 12.1). La conseguenza per la revisione è che «heroBelowFold = 0 diventa una regressione» non regge:
> non c'è nessuno zero da difendere, c'è un 330,7 da ridurre. **Lo riduco a 249,4 px** e l'altezza a
> 1 036,4 px, alzando nel frattempo la porta alla misura prescritta.

**Le sei violazioni.** 1 (secondo accento `--terr-persona`) e 2 (bronzo su una traiettoria): **rimosse** —
i token `--terr-persona / --terr-impresa / --terr-formazione / --terr-istituzione / --terr-ghost` non
esistono più, la lastra ha **un solo inchiostro**, `--terr-line`, e non introduce **nessun token nuovo**.
3 (durate e stagger): **rimossa** — tutti gli stagger sono 60 ms, tutte le durate vengono dai token, più
l'unico tracciato immersivo (§ 8). 4 (§ 8.3, sei attori): **EMENDAMENTO 1**. 5 (§ 8.3, budget a 390):
**EMENDAMENTO 3**. 6 (24 s contro 28 s): **rimossa**.

**I nove segnali «a buon mercato».** 1 numeri romani + mono maiuscolo: **cancellati**, non esistono più.
2 il secondo gruppo di quattro numerati: **cancellato** con i numeri. 3 la legenda a campioni:
**cancellata**; restano quattro toponimi nel margine basso della lastra, senza campione, senza indice, senza
griglia. 4 i pattern CAD: **cancellati**; nessun `stroke-dasharray` in tutta la specifica. 5 il grafo a nodi:
**cancellato**; niente cerchi con alone — sei **tacche di rilevamento** (barre da 9 unità perpendicolari al
tracciato) su **un solo** percorso, che è una carta, non un hub. 6 il gemello fantasma: **cancellato**.
7 «zero materiale»: § 4.4 e § 7 — fotografia a tutto arco, luce d'apertura, gradazione cotta, banda di
terreno, labbro della soglia, contrasto di scala fra un display da 100 px e toponimi da 13. 8 «il moto muore
dopo 3 s»: risposta onesta in § 8 — il sistema concede **un** loop per pagina e io non ne chiedo un secondo;
rendo percepibile quello che c'è (×2,2) e tolgo il secondo oggetto legato allo scroll che era già in
produzione. 9 «nessun guadagno d'immagine»: è esattamente ciò che questo round consegna (§ 7).

---

## 3. LA TESI

**La porta è il soggetto; tutto il resto è il terreno che le arriva addosso.**

Sotto il piede della porta, in una banda di 128 unità, quattro canali arrivano a un punto: l'impresa dice di
che cosa ha bisogno, l'università e gli organismi di formazione lo trasformano in preparazione, le due
correnti confluiscono, e **una sola linea sale**. Attraversa il filetto dell'istituzione — che passa sotto la
porta e non entra mai — sale i tre gradini, tocca la soglia e **sparisce**. Riappare sopra la volta e lascia
il foglio verso nord.

Tre cose la distinguono dal disegno che la revisione ha demolito. **È locale**: non attraversa il viewport,
occupa la vicinanza della porta, come il dettaglio di un estuario invece della carta del mondo. **È di un
solo inchiostro**: nessuna serie categoriale, nessuna tinta nuova, nessun pattern; quattro valori dello
stesso teal e quattro spessori. **È materiale**: la fotografia riempie l'arco per la prima volta, una luce
sta dietro la volta, il terreno ha un tono, la soglia ha un labbro e un'ombra.

Il tracciato dell'impresa corre **contro** il senso del viaggio: è il modo più economico di dire «questa è la
causa, non il percorso», e cancella la lettura «grafico di crescita» che § 8.6 vieta per nome.

---

## 4. GEOMETRIA

### 4.1 Il sistema di coordinate — una sola origine, nessuna deriva possibile

Tutto il disegno vive in **un solo spazio**: il riquadro della porta, `viewBox="0 0 380 506.67"`
(506,67 = 380 × 4/3, cioè l'`aspect-ratio: 3 / 4` che § 8.4 prescrive). Gli SVG usano
`preserveAspectRatio="xMidYMid meet"` dentro un riquadro che **ha già** quel rapporto: la mappa è dunque
esatta, 1 unità = `larghezza-porta / 380` px, a ogni larghezza. Ciò che sta fuori dalla porta si disegna in
coordinate negative o maggiori di 380/506,67 e appare grazie a `overflow: visible` sull'`<svg>`.

Conseguenze, e sono la risposta al MUST-FIX 1 e al MUST-FIX 8:

* la lastra **non dipende dalla colonna 5fr**, né dal contenitore, né dall'altezza del viewport;
* le etichette HTML si ancorano con percentuali della **stessa** porta, quindi geometria ed etichette non
  possono divergere — non per disciplina, per costruzione;
* la porta resta `380 / 300 / 220 px` esatti, e il `sizes` della fotografia resta vero.

Estensione della lastra, in unità della porta: `x` da **−516** a **+480**, `y` da **−76** a **+634,67**.
La banda del terreno è `y 506,67 → 634,67` (**128 unità**). Il bordo inferiore della lastra **coincide con il
filetto della striscia delle coordinate**: misurato a 1440×900, fondo della porta `y 716`, fondo di
`.hero__field` `y 844`, inizio di `.hero__coords` `y 844`. Non è un caso: è `.hero__field`
`min-block-size = larghezza-porta × 1,87018` con `.hero__inner { padding-block-end: 0 }` (§ 6.1).

### 4.2 L'inventario — uno solo, e i conteggi tornano

| oggetto | quantità | forma | inchiostro |
|---|---:|---|---|
| canali | **4** | curve Catmull-Rom, mai tratteggiate | `--terr-line` a 1,00 / .72 / .72 / .62 |
| stazioni | **6** | tacca di rilevamento, barra 9 unità ⊥ al tracciato | `--terr-line` 1,00 |
| confluenza | **1** (2 archi aperti) | archi concentrici r 24 e r 40, aperti in basso | `--terr-line` .72 |
| soglia | **1** (+ 1 labbro d'ombra) | linea sul piede dell'arco navy + ombra 3 px sotto | `--terr-line` 1,00 · `--mid-0` .55 |
| nomi | **4** | serif 13/18 | `--on-dark-3` |
| terreno della banda | 1 velo + 3 linee | gradiente verticale + tre isoipse lunghe | `--terr-line` .085 → 0 · .10 |
| luce d'apertura | 1 | ellisse a gradiente radiale, dietro la porta | `--mid-3` .46 → 0 |

Le sei stazioni di § 8.3 stanno **tutte sul percorso della persona**, in ordine: `S1` approdo · `S2`
confluenza con la formazione · `S3` bacino, dove arriva l'impresa · `S4` attraversamento del filetto
istituzionale · `S5` **la soglia** · `S6` capolinea oltre la volta.

### 4.3 I nodi e le stringhe `d`

Regola del generatore, identica a quella già in casa: **Catmull-Rom attraverso i nodi, emessa in Bézier
cubiche con tensione 1/6**, funzione `to_path()` di `scripts/territory.py` (righe 66-77), `r1()` per
l'arrotondamento a un decimale. Seme fisso, nessun `Math.random`, output byte-identico su ogni macchina.
`territory.py` guadagna una funzione `field()` che emette i due file sotto e stampa gli ancoraggi (§ 11).

| # | canale | nodi (unità della porta) |
|---|---|---|
| **I** | **PERSONNES** | `(−516, 578) · (−372, 575) · (−236, 570) · (−112, 563) · Nf(−20, 557) · (74, 553) · B(190, 548)` |
| **II** | **UNIVERSITÉS ET ORGANISMES DE FORMATION** | `(−516, 521) · (−378, 528) · (−240, 538) · (−118, 548) · Nf(−20, 557)` |
| **III** | **ENTREPRISES** (contro-corrente) | `(480, 584) · (392, 577) · (300, 566) · (238, 557) · B(190, 548)` |
| **IV** | **INSTITUTIONS** (il filetto che inquadra) | `(390, 528) · (300, 516) · (190, 512) · (60, 515) · (−56, 524)` |

```
.field__path--i
  d="M-516 578C-492 577.5 -418.7 576.3 -372 575C-325.3 573.7 -279.3 572 -236 570C-192.7 568 -148 565.2 -112 563C-76 560.8 -51 558.7 -20 557C11 555.3 39 554.5 74 553C109 551.5 170.7 548.8 190 548"

.field__path--ii
  d="M-516 521C-493 522.2 -424 525.2 -378 528C-332 530.8 -283.3 534.7 -240 538C-196.7 541.3 -154.7 544.8 -118 548C-81.3 551.2 -36.3 555.5 -20 557"

.field__path--iii
  d="M480 584C465.3 582.8 422 580 392 577C362 574 325.7 569.3 300 566C274.3 562.7 256.3 560 238 557C219.7 554 198 549.5 190 548"

.field__path--iv
  d="M390 528C375 526 333.3 518.7 300 516C266.7 513.3 230 512.2 190 512C150 511.8 101 513 60 515C19 517 -36.7 522.5 -56 524"

.cross__ascent   d="M190 548 V374.8"
.cross__sill     d="M91.7 374.8 H288.3"
.cross__lip      d="M78 377.4 H302"
.cross__out      d="M190 -3C190 -7.5 188.7 -21.8 190 -30C191.3 -38.2 193.7 -46.3 198 -52C202.3 -57.7 209 -60.7 216 -64C223 -67.3 236 -70.7 240 -72"

.field__basin    d="M167.4 539.8A24 24 0 0 1 212.6 539.8"   /* r 24 */
                 d="M154 530.5A40 40 0 0 1 226 530.5"       /* r 40 */

.field__station  S1 d="M-288.1 567.4L-287.9 576.4"
                 S2 d="M-20.2 552.5L-19.8 561.5"
                 S3 d="M189.8 543.5L190.2 552.5"
                 S4 d="M185.5 512L194.5 512"
                 S5 d="M185.5 374.8h9"
                 S6 d="M220.4 -70.2L223.6 -61.8"
```

Le tre isoipse lunghe della banda (decorative, 1,16:1) sono emesse da `territory.py` con
`y = base + 3,4·sin(0,0062·x + 1,7k) + 1,5·sin(0,0143·x + 0,9k)`, `base ∈ {566, 596, 622}`, campionate ogni
169 unità da `x = −520` a `x = 486` e passate a `to_path()`. Tre linee, 7 punti ciascuna: **il costo in byte
è dichiarato in § 10 e non è una stima.**

Verifiche geometriche, fatte e non asserite:

* **La persona non entra mai nell'arco navy.** L'ascesa è verticale a `x = 190`; l'arco navy occupa
  `x 91,7…288,3`, `y 70,2…374,8`. L'ascesa si ferma a `y 374,8`, cioè **sul** bordo inferiore, non dentro.
* **La persona attraversa il filetto istituzionale.** IV passa per `(190, 512)`; l'ascesa passa per `x = 190`
  fra `y 548` e `y 374,8`: si incontrano in `(190, 512)` = stazione **S4**.
* **La riemersione non tocca la porta.** Comincia a `y = −3`, sopra la sommità dell'arco (`y = 0`).
* **Nessun canale entra nella colonna del testo.** Misurato dopo l'impianto: il riquadro dipinto dei quattro
  canali è `y 716 → 844` a 1440×900, e il fondo di `.hero__copy` è **y 656**. Margine: **60 px**. A 1024×768:
  canali `y 708,7 → 836,7`, fondo della copia **y 678**. Margine: **30,7 px**. A nessuna larghezza un
  tracciato passa sopra un carattere.

### 4.4 La materia

**La luce d'apertura.** `<ellipse cx="190" cy="120" rx="430" ry="340">` con un gradiente radiale
`--mid-3 #1b2f3a` da `.46` a `0`, disegnata **dietro** la porta (`.doorway__field`, z 0). Non è un alone: è
il cielo dietro una volta, e la sua funzione è dare **profondità** al soggetto invece che attorno ad esso.
Composito al centro: `#1b2f3a` @ .46 su `--mid-1` = `rgb(20, 36, 46)`, luminanza relativa **0,0161**; il
toponimo `--on-dark-3` posato su quella zona resterebbe a **5,85:1** (§ 12.2), cioè sopra il 4,5:1 del corpo
piccolo — e i quattro toponimi stanno comunque più in basso, dove la luce è già a zero e il rapporto è 6,44:1. Nessuna animazione, nessun `filter`, un solo elemento, zero paint dopo il primo frame.

**Il velo del terreno.** `<rect x="-516" y="506.67" width="996" height="128">` con un gradiente lineare
verticale `--terr-line` da `.085` (**1,13:1**) a `0`: la banda ha un tono, non è il vuoto sotto un disegno.

**Il labbro della soglia.** Due linee, non una: `.cross__sill` a `y 374,8`, 2 px, `--terr-line` pieno, larga
esattamente quanto il piede dell'arco navy (`x 91,7…288,3`) — quindi **su fondo `--brand-navy`**, dove il
rapporto è **5,29:1** (ricalcolato); e `.cross__lip` a `y 377,4`, 3 px, `--mid-0` @ .55, larga 224 unità.
Una linea chiara con la sua ombra è un bordo fisico; una linea sola è un capello. L'ombra è **dichiarata
decorativa** e non porta informazione: la soglia è detta dalla linea chiara e dalla stazione S5.

**La fotografia.** § 7. È il pezzo di materia più grande della pagina e finora ne mancava metà.

---

## 5. I FILE, E CHE COSA CAMBIA IN CIASCUNO

### 5.1 Markup — `templates/pages/home/_hero.html`

Nessuna chiave nuova in `build_hero()`, nessuna vista toccata, nessun contratto dati modificato.
`.hero__side` diventa `.hero__field`, che è una `<figure>` e ha finalmente la sua `<figcaption>` — il che
soddisfa anche la regola strutturale di `tests/compliance/test_figure_caption.py`.

```django
<figure class="hero__field" data-field>
  <div class="doorway" data-doorway aria-hidden="true">
    {# dietro la porta: luce d'apertura, terreno, quattro canali, confluenza, quattro stazioni #}
    <svg class="doorway__field" viewBox="0 0 380 506.67" preserveAspectRatio="xMidYMid meet"
         aria-hidden="true" focusable="false">{% include "pages/home/partials/field_approach.svg" %}</svg>

    <div class="doorway__arch">{# § 8.4, invariato salvo la fotografia (§ 7) #}
      <div class="doorway__photo">
        <picture>
          <source type="image/avif" srcset="… doorway-notte-{480,800,1200}.avif …" sizes="{{ DOOR_SIZES }}">
          <source type="image/webp" srcset="… doorway-notte-{480,800,1200}.webp …" sizes="{{ DOOR_SIZES }}">
          <img class="doorway__img" src="…doorway-notte-800.webp" alt="" width="1200" height="1600"
               decoding="async" fetchpriority="high" data-doorway-photo>
        </picture>
        <div class="doorway__overlay"></div>
      </div>
      <div class="doorway__inner"><span class="doorway__glow"></span>
        <span class="doorway__keywrap" data-doorway-key>…key.svg…</span></div>
      <div class="doorway__steps"><span></span><span></span><span></span></div>
    </div>

    <svg class="doorway__trace" viewBox="0 0 380 506.67" preserveAspectRatio="xMidYMid meet"
         aria-hidden="true" focusable="false"><path pathLength="1" d="M0.75 506.67 V190 A189.25 189.25 0 0 1 379.25 190 V506.67"/></svg>

    {# davanti alla porta: ascesa, soglia, labbro, S5, riemersione, S6 #}
    <svg class="doorway__cross" viewBox="0 0 380 506.67" preserveAspectRatio="xMidYMid meet"
         aria-hidden="true" focusable="false">{% include "pages/home/partials/field_cross.svg" %}</svg>
  </div>

  <p class="field__names" dir="ltr" aria-hidden="true">
    <span class="field__name field__name--i"   dir="auto">{% translate "Personnes" %}</span>
    <span class="field__name field__name--ii"  dir="auto">{% translate "Universités et organismes de formation" %}</span>
    <span class="field__name field__name--iii" dir="auto">{% translate "Entreprises" %}</span>
    <span class="field__name field__name--iv"  dir="auto">{% translate "Institutions" %}</span>
  </p>

  <figcaption class="field__caption visually-hidden">{% translate "…§ 9.1…" %}</figcaption>
</figure>
```

I quattro `{% translate %}` riusano **gli stessi msgid** di `content.ENTRANCES` (`apps/pages/content.py:151`):
nessuna traduzione nuova. La `<figcaption>` è **un** msgid nuovo × 4 lingue = **4 voci di catalogo**, ed è
l'unico costo di traduzione di questa specifica (§ 10). I nomi visibili portano `aria-hidden="true"` perché
compaiono verbatim nella `<figcaption>`, che è la fonte di verità: nulla si perde, niente si legge due volte.

Il `<div class="doorway">` resta `aria-hidden="true"`, come § 8.4 impone. I nomi e la didascalia stanno
**fuori** da esso: era un difetto latente del round 1, che li metteva dentro.

### 5.2 SVG generati — `scripts/territory.py`

Due file nuovi, **non sei**, e nessuna variante `-rtl` (Emendamento 4):

| file | contiene | ruolo |
|---|---|---|
| `partials/field_approach.svg` | `<defs>` (luce, due maschere di dissolvenza, velo del terreno) · velo · 3 isoipse · IV · III · II · I · confluenza · S1–S4 | dietro la porta |
| `partials/field_cross.svg` | `<defs>` (dissolvenza della riemersione) · ascesa · labbro · soglia · S5 · riemersione · S6 | davanti alla porta |

I due file **non condividono nessun elemento animabile**: l'ascesa e la riemersione sono due `<path>` distinti,
ciascuno con il proprio `pathLength="1"`, ciascuno guidato da una sola animazione. È la risposta al MUST-FIX 5.

Il territorio di fondo resta a tre file ma **più magro**: `count=11`, `step=64`, graticola a 240 con 15 crocette
invece di 40, **niente rotta e niente stazioni** (spariscono `.terr__route` e `.terr__stations`, che sono la
diagonale-grafico di § 1.2 e il colore sbagliato di § 1.3). Byte misurati in § 10.

### 5.3 Fogli di stile

`static/css/v2/hero.css` — **si modifica**, non si sovrascrive, perché le regole in questione sono difetti
della superficie e non varianti: `padding-block` (§ 1.1), `.terr__route` in `--accent-dark` (§ 1.3), le
opacità di § 1.4, l'overscan della marea, `[dir="rtl"] .hero__territory` (Emendamento 4), `.hero__side` →
`.hero__field`. `static/css/v3/hero-doorway.css` — **nuovo**, caricato dopo, contiene la lastra: tutto ciò
che è in § 6.2 e § 6.3. Nessun `style=""`, nessun `<style>`, nessun font remoto, nessun CDN: **conforme a
`style-src 'self'`** — e lo so per prova, perché il tentativo di iniettare un foglio inline nella pagina
viva è stato **respinto dalla CSP** durante questa misurazione (§ 12.1).

---

## 6. CSS — completo

### 6.1 Impaginazione (in `v2/hero.css`)

```css
/* § 1.1: i 192 px di padding morto diventano la composizione, a parità di altezza totale. */
.hero { padding-block: 0; }
.hero__inner { padding-block: var(--s-6) 0; }

/* La colonna resta 7fr/5fr; il campo è largo ESATTAMENTE quanto la porta e si centra nella colonna. */
.hero__field {
  --door-w: 380px;
  position: relative;
  inline-size: var(--door-w);
  margin-inline: auto;
  margin-block: 0;
  align-self: end;
  display: grid;
  align-content: start;
  /* (76 spazio sopra la volta + 506,67 porta + 128 banda) / 380 */
  min-block-size: calc(var(--door-w) * 1.87018);
  padding-block-start: calc(var(--door-w) * 0.2);   /* 76 unità */
}
.doorway { position: relative; z-index: 1; inline-size: 100%; margin: 0; }
```

Perché funziona, con i numeri misurati: a 1440×900 `min-block-size` = 710,7 px, `.hero__field` occupa
`y 133,3 → 844`, la porta `y 209,3 → 716`, la banda `y 716 → 844`, `.hero__coords` comincia a `y 844`.
`.hero` = **800,0 px**, **+2,0 px** sotto la piega (oggi: 900,0 e +102,0). A 1280×800 e 1024×768 l'altezza è
**792,7 px** in entrambi i casi — la composizione è la **stessa** a ogni larghezza desktop, perché l'altezza
della riga non è più decisa dalla colonna di testo. A 1440×1080 la riga si allunga, la porta resta incollata
al fondo, lo spazio cresce fra il titolo e la porta: è il comportamento voluto.

### 6.2 La lastra (in `v3/hero-doorway.css`)

```css
.doorway__field,
.doorway__cross,
.doorway__trace {
  position: absolute; inset: 0; inline-size: 100%; block-size: 100%;
  overflow: visible;            /* la lastra vive fuori dal riquadro della porta */
  pointer-events: none;         /* MUST-FIX 2 */
}
.doorway__field { z-index: 0; }
.doorway__arch  { position: relative; z-index: 1; }
.doorway__trace { z-index: 2; }
.doorway__cross { z-index: 3; }

.field__path {
  fill: none; stroke: var(--terr-line);
  stroke-linecap: round; stroke-linejoin: round;
  vector-effect: non-scaling-stroke;
}
.field__path--i   { stroke-width: 2;   stroke-opacity: 1;   }  /* 6,07:1 */
.field__path--ii  { stroke-width: 1.5; stroke-opacity: .72; }  /* 3,77:1 */
.field__path--iii { stroke-width: 1.5; stroke-opacity: .72; }  /* 3,77:1 */
.field__path--iv  { stroke-width: 1;   stroke-opacity: .62; }  /* 3,13:1 */

.field__basin path   { fill: none; stroke: var(--terr-line); stroke-opacity: .72; stroke-width: 1;
                       vector-effect: non-scaling-stroke; }
.field__station path { fill: none; stroke: var(--terr-line); stroke-opacity: 1; stroke-width: 1.5;
                       stroke-linecap: butt; vector-effect: non-scaling-stroke; }
.field__texture path { fill: none; stroke: var(--terr-line); stroke-opacity: .10; stroke-width: 1;
                       vector-effect: non-scaling-stroke; }   /* 1,16:1 — decorativo, dichiarato */

.cross__ascent,
.cross__out  { fill: none; stroke: var(--terr-line); stroke-width: 2; stroke-linecap: round;
               vector-effect: non-scaling-stroke; }
.cross__sill { fill: none; stroke: var(--terr-line); stroke-width: 2; stroke-linecap: butt;
               vector-effect: non-scaling-stroke; }           /* 5,29:1 su --brand-navy */
.cross__lip  { fill: none; stroke: var(--mid-0); stroke-opacity: .55; stroke-width: 3;
               stroke-linecap: butt; vector-effect: non-scaling-stroke; }  /* decorativo */

/* La dissolvenza del bordo del foglio: due finestre, una per registro di larghezza. Nessuna maschera
   sopra la colonna del testo è necessaria — i canali stanno tutti SOTTO il piede della porta (§ 4.3). */
.field__approach { mask: url(#field-fade-wide); }
@media (max-width: 89.999rem) { .field__approach { mask: url(#field-fade-narrow); } }
```

I due gradienti di dissolvenza, in `userSpaceOnUse` su `x` (unità della porta):

| maschera | 0 % | 100 % | 100 % | 0 % | finestra visibile a … |
|---|---:|---:|---:|---:|---|
| `field-fade-wide` (≥ 90 rem) | −516 | −400 | +400 | +480 | 1440: schermo 498,3 → 1 298,3, cioè dissolto 141,7 px prima del bordo |
| `field-fade-narrow` (< 90 rem) | −300 | −196 | +341 | +410 | 1024: schermo 304 → 1 014, cioè dissolto 10 px prima del bordo |

### 6.3 I nomi

```css
.field__names {
  position: absolute; inset-inline: 0;
  inset-block-start: calc(var(--door-w) * 0.2);       /* il riquadro coincide con la porta */
  block-size: calc(var(--door-w) * 4 / 3);
  margin: 0; z-index: 4; pointer-events: none;
}
.field__name {
  position: absolute;
  inset-inline-start: var(--lx);
  inset-block-start: var(--ly);
  max-inline-size: var(--lw);
  font-family: var(--f-serif); font-weight: 400;
  font-size: var(--t-folio);                 /* 13 px — la scala a undici corpi, § 3.2 */
  line-height: 18px;                          /* multiplo di 2 px, dentro il ritmo di 4 sulle due righe */
  letter-spacing: .02em;
  color: var(--on-dark-3);                    /* 6,44:1 su --mid-1 */
  text-wrap: balance;
}
.field__name--i   { --lx: -75.789%; --ly: 117.632%; --lw: calc(100% * 150 / 380); }
.field__name--ii  { --lx: -31.579%; --ly: 114.079%; --lw: calc(100% * 150 / 380); }
.field__name--iii { --lx:  51.579%; --ly: 117.632%; --lw: calc(100% * 150 / 380); }
.field__name--iv  { --lx:  86.842%; --ly: 117.632%; --lw: calc(100% * 150 / 380); }
:lang(ar) .field__name { letter-spacing: 0; }   /* § 3.2 */
```

`--lx` è una percentuale della **larghezza** della porta, `--ly` dell'**altezza**: i valori corrispondono,
rispettivamente, a `x = −288 / −120 / 196 / 330` e `y = 596 / 578 / 596 / 596` in unità della porta.
`--lw = 150 unità` (39,47 % della larghezza) obbliga ogni lingua a **andare a capo invece di traboccare**:
è la garanzia che serve per l'arabo, dove non posso misurare la larghezza da qui.

Riquadri **misurati** dopo l'impianto (§ 12.5), a 1440×900, in coordinate del viewport:

| nome | x | larghezza | y | fondo | libero fino a `.hero__coords` (y 844) |
|---|---:|---:|---:|---:|---:|
| Personnes | 610,3 | 55,6 | 805,3 | 823,3 | 20,7 |
| Universités et organismes de formation (2 righe) | 778,3 | 140,0 | 787,3 | 823,3 | 20,7 |
| Entreprises | 1 094,3 | 62,9 | 805,3 | 823,3 | 20,7 |
| Institutions | 1 228,3 | 63,4 | 805,3 | 823,3 | 20,7 |

Nessuna sovrapposizione fra i quattro (666 < 778,3; 918,3 < 1 094,3; 1 157,2 < 1 228,3) e nessuno esce dal
viewport (1 291,7 < 1 440). A 1024×768: `316 → 371,7`, `484 → 624`, `800 → 862,9`, `934 → 997,4` — l'ultimo
termina **26,6 px** prima del bordo. A 768×1024: `6,6 → 62,3` … `494,5 → 558`, tutti dentro. Il fondo della
colonna di testo è `y 656` (1440), `y 678` (1024), `y 1 166,9` (768, dove i nomi stanno a 640,5-662,3,
**sopra** la copia): **nessuna collisione a nessuna larghezza.**

### 6.4 Il registro stretto e il telefono

```css
@media (max-width: 63.999rem) {            /* 768 → 1023 : una colonna, la porta in testa */
  .hero__field { --door-w: 300px; align-self: start; order: -1; }
  .hero__inner { padding-block: var(--s-2) var(--s-6); gap: var(--s-3); }
}
@media (max-width: 47.999rem) {            /* < 768 : la lastra non esiste */
  .hero__field { --door-w: 220px;                     /* § 8.3, alzata da 180 */
                 min-block-size: calc(var(--door-w) * 1.4667);
                 padding-block-start: calc(var(--door-w) * 0.1333); }
  .doorway__field, .field__names { display: none; }
  .hero__coords { gap: var(--s-2); }
}
```

Sotto 48 rem restano **la soglia, il labbro, l'ascesa e la riemersione**, perché vivono dentro la porta e
scalano con lei: la tesi sopravvive al telefono al costo di **zero pixel di altezza**. La riemersione viene
tagliata dal bordo superiore dell'eroe a `door-y −64,4`, dove la sua maschera di dissolvenza la tiene già al
**20 %** di opacità: il taglio non si vede (§ 12.5).

### 6.5 Il terreno di fondo (in `v2/hero.css`)

```css
/* § 1.4: le isoipse scendono sotto il livello delle linee informative. */
.terr__layer--1 path { stroke-opacity: .30; stroke-width: 1;  }   /* 3,13 → 1,68:1 */
.terr__layer--2 path { stroke-opacity: .18; stroke-width: .9; }   /* 1,96 → 1,33:1 */
.terr__grid line     { stroke-opacity: .07; }                     /* 1,14 → 1,19:1, passo 240 */
.terr__ticks path    { stroke-opacity: .14; }                     /* 1,69 → 1,48:1 */

/* MUST-FIX 16 : overscan. Corsa max 26 px in x (< 32) e 20 px in y (< 24): nessun bordo può entrare. */
.hero__territory { inset: -24px -32px; inline-size: auto; block-size: auto; }
```

Tutti e tre gli `<svg>` prendono lo stesso riquadro sovradimensionato, quindi restano **in registro fra
loro**; la lastra è ancorata alla porta e non dipende da loro.

### 6.6 Stati

| stato | che cosa fa |
|---|---|
| **riposo / senza JS / moto ridotto** | tutto disegnato: nessun `stroke-dasharray` nel CSS, nessuna opacità 0, nessuna trasformazione. La lastra è completa dal primo frame. |
| **hover sulla porta** (`hover: hover`) | § 8.4: `.doorway__arch` **e** `.doorway__cross` salgono di 4 px insieme (così la soglia non si scolla dal piede dell'arco), il primo gradino diventa `--brand-gold`. La lastra e i nomi **non** si muovono. 180 ms `--ease-out`. |
| **focus** | l'unico elemento focalizzabile della figura è `.tide-toggle`: anello 2 px `--accent-dark`, alone 3 px al 30 %, `outline-offset: 2px`. |
| **active** | `.tide-toggle`: 1 px verso il basso, 120 ms. |
| **disabled · loading** | non pertinenti: nessun controllo disabilitabile, SVG in linea, nessuna richiesta, nessuno skeleton. |
| **errore** (la fotografia non carica) | restano arco, arco navy, chiave, gradini, soglia, labbro, lastra: la composizione è completa senza di essa, e il fondo dell'arco resta il suo gradiente. |
| **`forced-colors`** | § 9.4. |

---

## 7. LA FOTOGRAFIA (EMENDAMENTO 2)

### 7.1 Il difetto, e la sua correzione in tre righe

```css
.doorway__photo picture { display: block; block-size: 100%; }
.doorway__img { inline-size: 100%; block-size: 100%; object-fit: cover; object-position: 50% 42%;
                opacity: 1; filter: none; transform: none; }
```

Il `transform: scale(1.06)` sparisce: serviva a nascondere i bordi di un'immagine che non riempiva il
riquadro. `filter: saturate(.8) contrast(1.05)` sparisce: la gradazione è **cotta nel derivato**
(`imagery.md` § 4.1). Con esso sparisce l'unico `filter` a runtime di questa superficie.

### 7.2 La gradazione e la vignetta

Derivati nuovi, dalla pipeline di `imagery.md`, gradazione **`-notte`**: nero `#0b171e`, bianco `#c8d4d6`,
saturazione **0,66**, −6 % di luminanza media, **ritaglio duro 3:4** (mai `cover` su un master 3:2 dentro un
3:4), AVIF q52 + WebP q72 a 480 / 800 / 1200 px di larghezza.

```css
.doorway__overlay { background:
  radial-gradient(ellipse 58% 52% at 50% 36%,
                  rgba(14,27,35,0) 42%, rgba(14,27,35,.20) 76%, rgba(14,27,35,.66) 100%),
  linear-gradient(180deg, rgba(14,27,35,.24) 0%, rgba(14,27,35,0) 22%,
                  rgba(14,27,35,0) 62%, rgba(14,27,35,.46) 90%, rgba(14,27,35,.62) 100%); }
```

Il velo teal è tolto: era lui a ingrigire. Il secondo gradiente **scurisce il piede** della porta, e non è
un gusto: è la condizione perché i tre gradini conservino il loro contrasto sulla fotografia (sotto).

Misure, fatte simulando la gradazione **sul master reale** `static/brand/v2/doorway-800.webp` e compositando
la vignetta pixel per pixel (§ 12.4):

| grandezza | oggi | V3 |
|---|---:|---:|
| area dell'arco coperta dalla fotografia | **49,4 %** | **100 %** |
| luminanza media della parte fotografica visibile | 0,0283 (solo metà superiore) | **0,0820** |
| luminanza del fondo sotto `door-y 267` | 0,0100 (= `--mid-1` nudo) | 0,0820 |
| luminanza al piede (door-y 470…500, dove stanno i gradini) | — | 0,0241 |

### 7.3 Contrasti ricalcolati sulla nuova base

| elemento | fondo | rapporto | soglia |
|---|---|---:|---|
| chiave `--brand-gold` | `--brand-navy` **pieno** | **5,80:1** | invariata — la chiave non sta sulla fotografia |
| soglia `--terr-line` 2 px | `--brand-navy` | **5,29:1** | ≥ 3:1 (1.4.11) ✔ |
| ascesa `--terr-line` 2 px | piede graduato, L 0,0241 | **4,91:1** | ✔ |
| riemersione `--terr-line` 2 px | `--mid-1` (fuori dalla porta) | **6,07:1** | ✔ |
| gradino 1 `--accent-dark` @ **.80** | piede graduato, L 0,0241 | **5,75:1** | ✔ |
| gradino 2 @ **.62** | piede graduato | **4,10:1** | ✔ |
| gradino 3 @ **.50** | piede graduato | **3,18:1** | ✔ (oggi @ .24 su `--mid-1` = **1,76:1**, fallisce) |

`sizes`, riscritto (MUST-FIX 17), coerente con le larghezze **misurate** della porta (380,0 / 300,0 / 220,0):

```
sizes="(min-width: 64rem) 380px, (min-width: 48rem) 300px, 220px"
```

A DPR 1 il browser sceglie 480 (telefono) e 480/800 (desktop); a DPR 2, 480 × 2 = 440 → 480 sul telefono e
760 → 800 sul desktop; a DPR 3 su 390 px, 660 → 800. Il candidato da 1200 serve i DPR 3 desktop e le finestre
molto alte. `imagery.md` § 4.6 chiede «380 → 400»: quella misura veniva dal riquadro dell'`<img>` **scalato
di 1,06** (400,7 px); tolto lo `scale`, il riquadro vero è **380,0 px**, e i due documenti si riallineano su
questo numero.

**I byte, misurati** (gradazione `-notte` applicata al master `doorway-1200.webp` e ricodificata con Pillow,
AVIF q52 / WebP q72; § 12.4). Il ritaglio 3:4 ha **il doppio dei pixel** del 3:2 a parità di larghezza, e
nonostante questo i derivati **pesano meno**, perché una gradazione desaturata a 0,66 con gli estremi
rimappati comprime meglio dell'originale:

| candidato | oggi (3:2) | V3 `-notte` (3:4) | delta |
|---|---:|---:|---:|
| 480 AVIF | 24 914 B | 480 × 640 = **25 379 B** | +1,9 % |
| 800 AVIF | 60 721 B | 800 × 1 067 = **55 839 B** | **−8,0 %** |
| 1200 AVIF | 123 932 B | 1 200 × 1 600 = **89 853 B** | **−27,5 %** |
| 800 WebP | 78 618 B | **67 458 B** | −14,2 % |

Il candidato servito al primo viewport è **800 AVIF = 54,5 KB** (desktop a DPR 2: 380 × 2 = 760 → 800;
telefono a DPR 3: 220 × 3 = 660 → 800). Tetto da asserire a build time: **≤ 60 KB AVIF a 800 px, ≤ 95 KB a
1200 px**. Primo viewport della home: **54,5 KB**, contro i 120 KB del budget. *Avvertenza onesta:* la misura
parte da un master già compresso; la pipeline vera, che parte dall'originale, darà numeri dello stesso ordine
ma non identici, e il tetto va verificato a build time, non qui.

---

## 8. MOTION — voci per `MOTION_SYSTEM.md` § 6

Tutto in `static/js/src/home.js` con `withMotion()`; `animate`, `scroll`, `stagger` sono **già** importati
(`home.js:18`): nessun import nuovo, nessun chunk nuovo.

| nome | funzione | innesco | durata · curva · stagger | proprietà | stato ridotto | budget |
|---|---|---|---|---|---|---|
| `hero.field.approach` | **causalità** | carico, una volta | 900 ms (`--motion-draw`) ciascuna · `--ease-out` · **stagger 60 ms** · ordine **IV → III → II → I** | `strokeDashoffset 1→0` su `.field__path` (`pathLength="1"`) | `strokeDashoffset: 0` | 4 figli (≤ 8), un solo `<svg>`, nessun repaint fuori da esso |
| `hero.field.stations` | **gerarchia** | fine del proprio tracciato + `--motion-base` | 240 ms · `--ease-out` · stagger 60 ms | `opacity 0→1`, `scale(.6)→scale(1)`, `transform-box: fill-box` | opacità 1, scala 1 | 4 tacche, solo `transform` + `opacity` |
| `hero.cross.ascent` | **causalità** | `1 320 ms` (fine di `approach` + `--motion-base`) | **600 ms** · `--ease-out` | `strokeDashoffset 1→0` su `.cross__ascent` | disegnata | un `<path>`, riquadro proprio |
| `hero.cross.emergence` | **delizia** | fine di `ascent` + `--motion-base` (**la pausa È la porta**) | **600 ms** · `--ease-out` | `strokeDashoffset 1→0` su `.cross__out` | disegnata | un `<path>` |
| `hero.door.trace` · `steps` · `key` | **delizia** (§ 8.4) | carico | 900 ms · gradini **stagger 60 ms** (Em. 5) · chiave **320 ms** (`--motion-slow`) | invariate | invariate | invariato |
| `hero.tide` | **profondità** | continuo; in pausa fuori dal viewport, a scheda nascosta e su richiesta | **28 s** (`--motion-ambient`), lineare, `alternate`, **un solo periodo** | `translate3d` ±26 px strato 1, ∓20 px strato 2 | assente | 2 elementi compositati, 0 paint |

**Perché 600 ms.** `MOTION_SYSTEM` § 1 ammette «un tracciato immersivo **600–900 ms**»; 600 è l'estremo basso
della banda ed è il valore che `home.js:37` usa già per le righe del titolo. Non introduco nessun numero:
le durate usate in tutta la specifica sono `{120, 180, 240, 320}` + `{600, 900}` + `28 s`.

**La pausa dietro la porta.** Fra `ascent` e `emergence` passano 240 ms (`--motion-base`) in cui **non
succede niente di visibile**: è il tempo in cui la persona è dietro la volta. Non è un ritardo tecnico, è
l'affermazione — ed è anche la ragione per cui l'ascesa e la riemersione sono due tracciati e non uno.

Sequenza completa al carico: 0 → 1 080 (quattro canali) → 1 320 → 1 920 (ascesa) → 2 160 → 2 760
(riemersione). **2,76 s**, in parallelo alla coreografia della porta di § 8.4.

**Oggetti vivi sulla pagina, dopo questa specifica.** Un loop ambientale (la marea) e **un** oggetto
indicizzato allo scroll (la rotta di § 8.6). Oggi ce ne sono **due**, perché `home.js:95` lega alla
`ScrollTimeline` anche la fotografia della porta: l'Emendamento 2 lo toglie. **Questa specifica riduce il
numero di oggetti animati della pagina e non ne chiede nessuno in più.**

**Risposta onesta al segnale 8 («il moto muore dopo 3 secondi»).** Sì. Il sistema concede un loop per pagina
e io non ne chiedo un secondo; chiedere un secondo loop sarebbe il modo più rapido per far sembrare
«a buon mercato» la pagina. Quello che faccio è renderlo visibile: strato più veloce **0,93 px/s** contro
0,43 (×2,2), separazione relativa **46 px** contro 21 (×2,2), con l'overscan che la rende possibile senza
strappare il bordo. Se sia **percepibile** non lo deduco da un numero: è la voce 5 di § 9.5.

Collaudo, prima di accettare: pannello Performance di Chrome durante la sequenza — **0 layout e 0 paint
oltre il primo frame**; INP < 200 ms; CPU rallentata 4×; moto normale / ridotto / cambiato a pagina aperta.

---

## 9. ACCESSIBILITÀ, LINGUE, MODALITÀ FORZATE

### 9.1 L'alternativa testuale

I tre `<svg>` della porta restano `aria-hidden="true"`; la `<figure>` porta una `<figcaption>`
`visually-hidden` che è **la fonte di verità** e nomina, nell'ordine, esattamente gli oggetti di § 4.2.
Testo (FR; poi tradotto):

> « Schéma. Sous le seuil, quatre voies se rejoignent : l'entreprise fait connaître ses besoins
> professionnels ; l'université et les organismes de formation les transforment en préparation ; les deux
> courants se rejoignent devant la porte. La personne est la seule à monter les marches et à atteindre le
> seuil ; sa ligne disparaît derrière la voûte et reparaît au-dessus d'elle. La ligne des institutions passe
> sous la porte sans y entrer. Le passage lui-même relève des autorités compétentes. »

Verificato contro `apps/cms/forbidden.py`: nessuna delle 16 `FORBIDDEN_PHRASES`, nessuno dei 10
`FORBIDDEN_PATTERNS` (in particolare `\bmatching\b`), nessun carattere di `FORBIDDEN_CHARACTERS` (`®`).
**Il cancello è `tests/compliance/test_public_pages.py::test_no_forbidden_formulations_on_public_pages`**, che
esegue `cms.forbidden.scan()` sull'HTML reso di **ogni rotta pubblica in ogni lingua** — quindi anche
sull'EN e sull'IT di questa didascalia, che è l'esposizione che la revisione ha giustamente indicato.

**Nota per il traduttore, da scrivere nel `.po` sopra il msgid:**
> *Ne traduisez pas « franchit le seuil » par une formule qui s'approche de « Cross the doorway to Italy » ou
> de « A doorway, not a shortcut » (`apps/cms/forbidden.py`). En anglais, préférez « reaches the threshold » ;
> en italien, « raggiunge la soglia ». Ne jamais employer « matching ».*

### 9.2 Il resto della conformità

Le etichette **non sono interattive**: nessun bersaglio nuovo, nessuna tabulazione prima dell'H1. L'unico
controllo della figura è `.tide-toggle`, oggi **234,8 × 32 px** (misurato): **da portare a 44 px** di altezza
su `pointer: coarse` (WCAG 2.2 · 2.5.8) — resta un difetto aperto di questa superficie e lo scrivo qui perché
non sparisca. Il colore non è mai solo: i quattro canali hanno lo **stesso** colore e si distinguono per
spessore (2 / 1,5 / 1,5 / 1), posizione, forma e nome — il criterio 1.4.1 è soddisfatto per costruzione,
perché il colore non distingue nulla. `prefers-reduced-motion` è uno stato completo: nessun
`stroke-dasharray` e nessuna opacità 0 nel CSS, quindi il disegno è **identico** in contenuto, semplicemente
fermo; `.tide-toggle` non è disegnata perché non c'è nulla da sospendere.

### 9.3 Arabo e RTL (EMENDAMENTO 4)

Non si specchia niente. `hero.css:567` si cancella; `territory.py` non emette varianti `-rtl`; la lastra ha
una sola geometria in tutte le lingue. Lo strato `.field__names` porta `dir="ltr"` come **contesto di
posizionamento**, così `inset-inline-start: var(--lx)` significa «da sinistra» in tutte le lingue e resta una
proprietà logica; ogni `<span>` porta `dir="auto"`, così il testo arabo è composto in arabo. `:lang(ar)`
azzera la spaziatura (§ 3.2) e `--lw` forza l'andata a capo invece del trabocco. `tests/i18n/test_rtl_browser.py`
va aggiornato: sparisce l'asserzione sullo specchio, entra l'asserzione che a `/ar/` i quattro nomi sono
tradotti e dentro il viewport.

### 9.4 `forced-colors` (MUST-FIX 20)

```css
@media (forced-colors: active) {
  .field__path--i, .cross__ascent, .cross__sill, .cross__out,
  .field__station path, .doorway__trace path { stroke: CanvasText; }
  .field__path--ii, .field__path--iii, .field__path--iv, .field__basin path { stroke: CanvasText; }
  .field__texture path, .terr__layer path { stroke: GrayText; }
  .cross__lip, .field__bank, .field__aperture { display: none; }
  .field__approach { mask: none; }          /* la dissolvenza non deve nascondere un'informazione */
  .doorway__steps span { background: CanvasText; }
}
```

Nessun `forced-color-adjust: none`, da nessuna parte. Gli spessori restano (`vector-effect: non-scaling-stroke`
non è toccato dalla tavolozza forzata) e con essi la sola differenziazione che avevo già scelto.

### 9.5 `HUMAN_QA_REQUIRED`

1. NVDA + Firefox e VoiceOver + Safari sulla `<figcaption>` in FR / IT / EN / AR: la frase si capisce senza
   il disegno?
2. Giudizio umano, non sostituibile: la banda con i quattro toponimi legge come **il margine di una lastra
   incisa** o come una legenda di grafico? È la domanda su cui la revisione ha affondato il round 1.
3. `/ar/` con un lettore reale: una carta non specchiata in una pagina RTL disorienta o si legge come una
   carta?
4. La fotografia gradata `-notte` a tutto arco su schermo OLED reale e su un pannello economico: l'arco legge
   come un'apertura o come una cartolina?
5. La marea a 0,93 px/s: si percepisce? Se no, il tetto è ≤ 2 px/s di separazione relativa e si può salire una
   volta sola; se comincia a sembrare uno screensaver, si scende.
6. Verifica editoriale che «l'entreprise fait connaître ses besoins / la personne atteint le seuil / les
   institutions n'y entrent pas / le passage relève des autorités compétentes» non collida con la verità
   giuridica del documento d'implementazione.
7. `coord` e `tide-toggle` restano in francese su `/ar/` (§ 1.8 del round 1): da colmare nel catalogo, fuori
   da questa specifica ma sulla stessa superficie.

---

## 10. PRESTAZIONI — cifre misurate, non stimate

**Byte in linea nell'eroe** (`gzip -9` su un flusso unico, come lo serve il server):

| | oggi | V3 |
|---|---:|---:|
| graticola + tacche + rotta + stazioni | 3 170 | **899** (passo 240, 15 crocette, niente rotta né stazioni) |
| isoipse, due strati | 28 119 | **19 185** (`count=11`, `step=64`) |
| `field_approach.svg` | — | **3 043** |
| `field_cross.svg` | — | **977** |
| seconda maschera di dissolvenza | — | **505** |
| **totale non compresso** | **31 289** | **24 609** (**−21,3 %**) |
| **totale gzip** | **11 965** (2,62:1) | **8 680** (2,84:1) — **−27,5 %** |

La cifra del round 1 («≈ 5,6 KB gzip, i dati di path comprimono ≈ 4:1») è cancellata: il rapporto reale
misurato è **2,62:1** oggi e **2,84:1** in V3, e il risparmio vero è **3,3 KB gzip**, non 6,1.

**JavaScript.** Sei voci di moto, `animate` / `scroll` / `stagger` già importati: sorgente aggiunta ≈ 1,5 KB,
**≈ 0,7 KB gzip**; e ne esce una (la parallasse della fotografia, Emendamento 2). Il budget di pagina
(≤ 45 KB gzip, di cui 26 il chunk condiviso di Motion) non si muove.

**Immagini.** Nessuna immagine nuova per numero; i tre derivati della porta cambiano ritaglio e gradazione,
e **pesano meno di oggi** nonostante il doppio dei pixel (§ 7.3): 800 AVIF **55 839 B** contro 60 721.
Primo viewport della home: **54,5 KB**, sotto i 120 KB.

**Catalogo.** **Quattro** voci nuove (un msgid × 4 lingue): la `<figcaption>`. I quattro nomi riusano i msgid
di `content.ENTRANCES`. Il round 1 dichiarava «nessuna traduzione nuova» e ne nascondeva ~20: questa è la
cifra vera.

**Paint e layout.** `doorway__field` non si muove mai dopo il carico; `doorway__cross` anima due
`strokeDashoffset` una volta ciascuno; i due strati di isoipse si muovono come elementi interi (`transform`
compositato, 0 paint); i nomi sono HTML su uno strato proprio, e **non sono animati affatto**. Nessun
`filter` (ne sparisce uno), nessun `box-shadow` animato, nessuna animazione di `width` / `top` / `left`,
nessuna animazione legata allo scroll nell'eroe. **Budget dichiarato: 0 layout e 0 paint oltre il primo frame
dopo la sequenza di carico.**

---

## 11. CHE COSA DEVE ESSERE SCRITTO, FILE PER FILE

| file | modifica |
|---|---|
| `templates/pages/home/_hero.html` | `.hero__side` → `<figure class="hero__field">`; tre `<svg>` dentro `.doorway`; `.field__names`; `.figcaption`; `sizes` e `srcset` della fotografia; `width`/`height` 1200 × 1600. |
| `templates/pages/home/partials/field_approach.svg`, `field_cross.svg` | **nuovi**, generati. |
| `templates/pages/home/partials/territory_hero_{base,layer-1,layer-2}.svg` | rigenerati: `count=11`, `step=64`, graticola 240, senza rotta né stazioni. |
| `scripts/territory.py` | `main()` con i nuovi parametri; funzione `field()` che emette i due file e **stampa** su stdout il blocco CSS dei quattro ancoraggi; niente varianti `-rtl`. |
| `static/css/v2/hero.css` | § 6.1 (padding), § 6.5 (opacità e overscan), hover spostato su `.doorway__arch, .doorway__cross`, `.doorway__photo picture` e `.doorway__img` (§ 7.1), `.doorway__overlay` (§ 7.2), opacità dei gradini, rimozione di `[dir="rtl"] .hero__territory`, `.terr__route` rimosso. |
| `static/css/v3/hero-doorway.css` | **nuovo**: § 6.2, § 6.3, § 6.4, § 9.4. |
| `static/js/src/home.js` | quattro voci nuove (§ 8); stagger 0,08 → 0,06; gradini 0,1 → 0,06; chiave 0,5 → 0,32; **rimozione** del blocco `scroll(...)` sulla fotografia. |
| `tests/frontend/test_field_anchors.py` | **nuovo**: importa `territory.field()`, confronta i quattro `--lx`/`--ly` con quelli presenti in `v3/hero-doorway.css`; fallisce se divergono. |
| `tests/frontend/test_motion_system.py` | invariato nel codice; deve continuare a contare **tre** `cubic-bezier`. |
| `tests/i18n/test_rtl_browser.py` | l'asserzione sullo specchio del territorio si rimuove (Em. 4); entra quella sui quattro nomi in AR. |
| `locale/*/LC_MESSAGES/django.po` | un msgid nuovo × 4 lingue, con la nota per il traduttore di § 9.1. |

---

## 12. APPENDICE DI MISURA

### 12.1 Metodo

Chromium headless di Playwright, lanciato dal `.venv` del progetto
(`C:\tmp\italylegalentry\.venv\Scripts\python.exe`), **browser proprio, mai la porta 9222**,
`deviceScaleFactor: 1`, `wait_until="networkidle"` + 400 ms, `http://127.0.0.1:8771/fr/`.
Tutte le geometrie con `Element.getBoundingClientRect()` senza scroll; le estensioni del testo con
`Range.selectNodeContents()`, che dà l'inchiostro e non il blocco.
Il candidato è stato **servito come foglio di stile** intercettando la risposta di
`/static/pages/css/pages.css` e accodandovi il CSS, perché il primo tentativo con un `<style>` in linea è
stato **respinto dalla CSP** (`Applying inline style violates the following Content Security Policy directive
'style-src 'self'`): è la prova, non chiesta ma utile, che la superficie è davvero sotto `style-src 'self'`.
Il markup della lastra è stato costruito via `page.evaluate` **sulla sola istanza di browser**; nessun file
del repository è stato modificato per queste misure. Script e uscite:
`…\scratchpad\hero3\{measure,probe2,calc,pix,grade3,paths,proto}.py`, `…\{measure,probe2,proto}.json`,
`…\{proto_1440x900,proto_1024x768,proto_768x1024,proto_390x844,arch_compare}.png`.

### 12.2 Contrasti (luminanza relativa WCAG 2.x, calcolata, non stimata)

| coppia | rapporto |
|---|---:|
| `--terr-line #3fa6af` su `--mid-1 #0e1b23` | **6,07:1** |
| `--terr-line` @ .72 → `#317f88` su `--mid-1` | **3,77:1** |
| `--terr-line` @ .62 → `#2c717a` su `--mid-1` | **3,13:1** |
| `--terr-line` @ .30 → `#1d454d` su `--mid-1` | **1,68:1** |
| `--terr-line` @ .18 → `#18373f`… su `--mid-1` | **1,33:1** |
| `--terr-line` @ .10 → `#132931` su `--mid-1` | **1,16:1** |
| `--terr-line` su `--brand-navy #0f2547` | **5,29:1** |
| `--on-dark-3 #8fa0a3` su `--mid-1` | **6,44:1** |
| `--on-dark-3` su `--mid-1` + luce d'apertura al centro (`rgb(20,36,46)`) | **5,85:1** |
| `--brand-gold #c39a2b` su `--brand-navy` | **5,80:1** |
| `--accent-dark` @ .80 / .62 / .50 sul piede graduato (L 0,0241) | **5,75 / 4,10 / 3,18:1** |
| *(controllo)* `--accent-dark` @ .55 / .38 / .24 su `--mid-1` — i gradini di oggi | 3,91 / 2,54 / **1,76:1** |
| *(controllo)* `rgba(63,166,175,.22)` e `.30` su `--mid-1` — i «fantasmi» del round 1 | **1,43:1** e **1,68:1** |
| *(controllo)* `#9fe3e8` su `--mid-1` — il secondo accento del round 1 | 12,19:1 (> `--accent-dark` 10,01:1) |

### 12.3 Larghezze di testo (Chromium, font del sito, 1440×900)

| stringa | famiglia · corpo | larghezza |
|---|---|---:|
| `UNIVERSITÉS ET ORGANISMES DE FORMATION` | `--f-mono` 13 px, `.08em`, maiuscolo | **335,92 px** |
| `PERSONNES` | idem | 79,56 px |
| `Universités et organismes de formation` | `--f-serif` 14 px, `.02em` | 230,92 px |
| `Universités et organismes` / `de formation` | idem, su due righe | **150,72 / 76,81 px** |
| `Personnes` / `Entreprises` / `Institutions` | idem | 59,91 / 67,77 / 68,33 px |
| gli stessi a 13 px, misurati sull'impianto | `--f-serif` 13 px | **55,6 / 62,9 / 63,4** e **140,0** (2 righe) |

### 12.4 La fotografia

Campionamento di `full_1440.png` sul riquadro della porta (x 899…1278, y 294…800), media di riga ogni
25 px: struttura (varianza cromatica) fino a `door-y 265`; da `door-y 275` in poi
`rgb(17,32,41) → rgb(14,27,35)`, luminanza **0,0100**, cioè `--mid-1` nudo. Riquadro di layout dell'`<img>`:
**400,7 × 267,1** con `scale(1.06)`, cioè **378 × 252** senza → 49,4 % dell'arco `378 × 504,7`.
La gradazione `-notte` è stata **applicata in Python al master reale** `doorway-800.webp` (desaturazione
verso la luma a 0,66, rimappatura degli estremi su `#0b171e`/`#c8d4d6`, −6 % di luminanza), il ritaglio duro
3:4 preso al centro, la vignetta di § 7.2 compositata pixel per pixel: luminanza media della parte
fotografica visibile (esclusa l'area coperta dall'arco navy) **0,0820**; piede **0,0241**. Immagine di
confronto: `…\scratchpad\hero3\arch_compare.png` (sinistra: lo schermo di oggi; destra: il candidato).
I byte di § 7.3 vengono dalla stessa gradazione applicata al master `doorway-1200.webp` e ricodificata con
Pillow 12.3 (AVIF q52, WebP q72, `method=6`), confrontata con `os.path.getsize()` sui derivati in produzione.

### 12.5 Impianto del candidato — geometrie misurate

| viewport | `.hero` | sotto la piega | % del viewport | porta | `.hero__field` | banda dipinta | fondo CTA |
|---|---:|---:|---:|---|---|---|---:|
| 1440 × 900 | **800,0** | **+2,0** | 88,9 % | `x 898,3 · y 209,3 · 380,0 × 506,7` | `y 133,3 → 844` | `y 716 → 844`, `x 378,3 → 1 378,3` | 656,0 |
| 1280 × 800 | **792,7** | +94,7 | 99,1 % | `x 776,3 · y 202,0 · 380,0 × 506,7` | `y 126 → 836,7` | `y 708,7 → 836,7` | 653,2 |
| 1024 × 768 | **792,7** | +126,7 | 103,2 % | `x 604,0 · y 202,0 · 380,0 × 506,7` | `y 126 → 836,7` | `y 708,7 → 836,7` | 678,0 |
| 768 × 1024 | **1 126,9** | +204,9 | **110,0 %** | `x 234 · y 170 · 300,0 × 400,0` | `y 110 → 671` | `y 570 → 671,1` | 1 146,9 |
| 390 × 844 | **1 036,4** | +249,4 | **122,8 %** | `x 85 · y 94,3 · 220,0 × 293,3` | `y 65 → 387,7` | — (lastra assente) | **743,4** |

Confronto con oggi, stessa procedura: 900,0 / +102,0 · 889,2 / +191,2 · 883,3 / +217,3 · 1 206,6 / +284,6 ·
**1 117,7 / +330,7**. La riemersione: riquadro dipinto `y 137,3 → 206,3` a 1440 (sommità dell'eroe: 102),
`y 113,2 → 167,6` a 768 (sommità: 102), `y 52,6 → 92,6` a 390 (sommità: 57) — a 390 i primi 4,4 px sono
tagliati dal bordo dell'eroe, dove la maschera di dissolvenza tiene il tracciato al **20 %**.

---

### 12.6 Geometria della lastra

Le stringhe `d` di § 4.3 sono state prodotte dalla funzione `to_path()` di `scripts/territory.py`, importata
senza modifiche (`importlib`), sulle tabelle di nodi pubblicate: chiunque le rigeneri ottiene gli stessi
byte. Angolo di giunzione a `Nf` calcolato dalle tangenti Catmull-Rom nei due nodi: **8,32°**. I byte degli
SVG di § 10 sono `len(markup.encode())` sul markup emesso e `gzip.compress(flusso, 9)` sul flusso
concatenato, confrontati con i tre partial reali letti dal disco.

---

## 13. RISCHI

| # | rischio | perché sembrerebbe «a buon mercato» | guardia |
|---|---|---|---|
| 1 | **La banda dei quattro nomi ridiventa una legenda.** | Quattro parole allineate sono a un passo da una legenda di grafico. | Nessun campione, nessun indice, nessuna griglia, nessun riquadro; serif e non mono; ciascun nome sotto la portata del proprio canale; interlinea e colore di **margine di foglio**, non di interfaccia. Verifica umana obbligatoria (§ 9.5.2). Se fallisce, i nomi escono dal disegno e restano nella didascalia. |
| 2 | **La luce d'apertura legge come un alone da prodotto SaaS.** | Un alone dietro un oggetto è il cliché più veloce del 2024. | È un'**ellisse asimmetrica** centrata sulla volta, non un cerchio dietro l'oggetto; non pulsa, non si anima, non usa `filter`; il suo massimo è `.46` di `--mid-3`, cioè un fondo, non una sorgente. Se in revisione legge come alone: scende a `.30` prima di toccare la geometria. |
| 3 | **La fotografia a tutto arco diventa una cartolina.** | Una fotografia di monumento grande e nitida è il rischio opposto a quello di oggi. | La gradazione `-notte` è la stessa di tutte le altre lastre del sito (`imagery.md` § 4.2): quattordici fotografie devono leggere come **una sola commissione**. Il piede è scurito, la vignetta tiene i bordi, la saturazione è 0,66. Verifica umana (§ 9.5.4). |
| 4 | **Deriva verso l'infografica.** | «Autorevole» si perde al primo numero non calcolato. | Il disegno non porta **nessuna cifra**. Le uniche dell'eroe restano le due coordinate reali della striscia di chiusura, che esistono già — ed è anche la ragione dell'Emendamento 4. |
| 5 | **Il telefono resta fuori budget.** | Un eroe che occupa un quarto di schermo in più di quanto il sistema ammette. | Emendamento 3, con la dimostrazione aritmetica. Misura dopo l'impianto: 1 036,4 px contro 1 117,7, **con la porta alzata alla misura prescritta**, e la CTA primaria a 100,6 px dalla piega. |
| 6 | **Gli emendamenti 1 e 3 vengono respinti insieme.** | Si tornerebbe a sei nodi mono su un telefono che non li contiene. | Ripieghi già scritti, dentro ciascun emendamento. Nessuna parte della geometria di § 4.3 dipende da quelle due decisioni: si tolgono i nomi e si riduce la porta, il resto della specifica non cambia. |
| 7 | **L'arabo senza specchio disorienta.** | Nessun numero può decidere questa. | § 9.5.3, con un lettore reale. Se disorienta, l'alternativa **non** è specchiare: è comporre una seconda geometria in cui la persona entra da destra e i rilievi vengono ridisegnati coerentemente da `territory.py` — un lavoro reale, da chiedere come round a sé. |
| 8 | **Il registro 1024–1280 perde il bordo destro della banda.** | Una linea tagliata dal bordo dello schermo sembra un errore. | La maschera `field-fade-narrow` porta a zero i canali prima del bordo del foglio a **ogni** larghezza sotto 90 rem; misurato a 1024, l'ultimo nome termina 26,6 px prima del bordo e i canali sono già dissolti. |
