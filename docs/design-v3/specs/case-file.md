# CASE-FILE — il fascicolo digitale e il banco dei documenti (V3, round 2)

Superficie: `templates/cases/detail.html`, `templates/portal/documents.html`,
`templates/documents/partials/register.html`, `templates/documents/requirement_detail.html`.
**Modalità di pagina dichiarata: `data-mode="dense"`** (`DESIGN_SYSTEM_V2.md` § 7, riga «fascicolo,
liste, tabelle, back-office»). Il round 1 non aveva aperto il § 7 e ha proposto ombre, una
fotografia, reveal, un oggetto legato allo scroll e un loop: **le cinque cose che questa classe di
pagina vieta.** Sono state tolte tutte. Questo documento riprogetta *dentro* DENSE.

Prove raccolte da me, round 2, in headless (Chromium di Playwright via `.venv/Scripts/python.exe`,
browser mio, mai la porta 9222) contro `http://127.0.0.1:8771`. Gli script di misura e i loro
output sono in `…/claude/cf3/m1…m11.py`; ogni numero di questo documento è nel § 10, con il modo in
cui è stato ottenuto. Storico visivo: `docs/design-v3/audit/case_file_{1440,390}_full.png`,
`documents_{1440,390}_full.png`, `docs/design-v2/before/case_file_desktop.png`.

---

## AMENDMENT REQUESTS

Quattro, numerate, tutte strette. Nessun'altra deviazione è presente; il § 0-bis dice come leggo le
clausole che *non* richiedono un'eccezione, perché il silenzio non è un'opzione.

### AR-1 — `DESIGN_SYSTEM_V2.md` § 6 (sistema cartografico) contro § 9.1 (case band)

**Clausola.** § 6: «Sistema cartografico: graticola 160 px con tacche; isoipse … **mai** su
STANDARD/DENSE/LEGAL». § 9.1: «(2) **Case band** `--mid-2` **con la banda territoriale al margine
finale**».
**Che cosa chiedo.** Di tenere la banda territoriale prescritta dal § 9.1 su una pagina DENSE, nella
forma minima: **solo tacche**, nessuna isoipsa, nessuna graticola. Un `repeating-linear-gradient`
di tacche verticali da 1 px in `--terr-line` (**5,51 : 1** su `--mid-2`, misurato), largo 56 px, sul
margine finale della banda, `aria-hidden`, `forced-color-adjust: auto` (sparisce in forced-colors),
zero moto.
**Perché.** Senza di essa la banda è un rettangolo scuro e il § 9.1 non è onorato. È l'unico segno
grafico di territorio della pagina e non entra mai nella colonna di lettura.
**Costo.** Una dichiarazione `background-image` su uno pseudo-elemento, ≈ 140 byte di CSS. Se
respinta: si cancella la riga `.cf-band::after` e nient'altro cambia.

### AR-2 — `DESIGN_SYSTEM_V2.md` § 10 (stato «loading con spinner a tratto + testo»)

**Clausola.** § 10: «Stati: … **loading con spinner a tratto + testo**».
**Che cosa chiedo.** Di **non** disegnare lo spinner su questa superficie. Lo stato di attesa è:
`aria-busy="true"`, l'etichetta che diventa «Enregistrement…», il controllo disabilitato *a colore*
(mai a opacità) e lo skeleton di livello 1 del § 9.6.
**Perché.** Uno spinner è un loop. `MOTION_SYSTEM.md` § 4 concede **un** loop a pagina e **solo**
alle pagine IMMERSIVE: «STANDARD, DENSE e LEGAL nessuno». Il § 9.6 dice già «skeleton di livello 1
con `aria-busy`, **mai solo uno spinner**». Il round 1 aveva squalificato il candidato 1 per
`animate-spin` e poi ne aveva specificato uno: la contraddizione che il revisore ha segnalato si
risolve togliendo lo spinner, non giustificandolo.
**Costo.** Su una rete lenta l'attesa è dichiarata da parole e da blocchi fermi, non da un oggetto
che gira. Nessun CSS di rotazione, nessun `@keyframes` su questa superficie.

### AR-3 — `DESIGN_SYSTEM_V2.md` § 9.1 e § 9.7 (inspector come terza colonna appiccicosa)

**Clausola.** § 9.1: «Spazio di lavoro 224 / 1fr / 320 … **inspector** appiccicoso a destra». § 9.7:
«Livello 3, appiccicoso».
**Che cosa chiedo.** Su **queste due superfici** (`cases/detail.html`, `portal/documents.html`)
l'inspector **non è una terza colonna a nessuna larghezza**. Il suo contenuto (pré-évaluation con la
frase prescritta, jeu de règles col sigillo, scadenze, storico) resta **tutto**, nell'ordine di
lettura, come primo foglio dello spazio di lavoro; la sua *permanenza* è portata dalla striscia
appiccicosa da 56 px della banda (§ 4.B), che non lascia mai lo schermo.
**Perché — aritmetica misurata.** Il contenuto del contenitore è **1240 px a 1440** e **1360 px a
1600** (misurato sul sito vivo, § 10.2). Togliendo il rail di navigazione da 224, l'inspector da 320
e due gutter da 24 restano **648 px a 1440** e **768 px a 1600** per il registro. Le quattro colonne
fisse del registro misurano **516 px** (§ 10.4): la colonna «Élément» resterebbe a **132 px** a 1440.
Un titolo reale — «Identifier les interlocuteurs et les autorités compétentes» — chiede **157 px**
per non spezzarsi in una parola per riga (misurato). Senza l'inspector il registro ha **992 px a
1440** e «Élément» ne prende **724**.
**Costo.** Si perde la co-presenza inspector/registro sopra 1600. Non si perde nessun contenuto e
nessun ordine di lettura: un test confronta la sequenza del testo a 1600 e a 390 e la vuole
identica. L'inspector resta una colonna sul cruscotto e sulle altre superfici RICH per cui il § 9.1
è stato scritto.

### AR-4 — `DESIGN_SYSTEM_V2.md` § 9.1 («misuratore a **cinque** tacche»)

**Clausola.** § 9.1: «avancement come **misuratore a cinque tacche** = conteggio».
**Che cosa chiedo.** **Una tacca per pièce**, non cinque: N tacche in un campo fisso da 120 px, con
`flex: 1` e `min-inline-size: 6px`; da N = 11 il misuratore sparisce e resta la frase.
**Perché.** Il fascicolo di prova ha **sette** pièces. Cinque tacche per sette elementi significa
quantizzare: «2 su 7» diventerebbe 1,43 tacche, cioè una tacca che mente. Il § 1 di questo documento
e il commento in testa a `templates/cases/detail.html` dicono entrambi che questa pagina non mostra
mai una percentuale perché «4 su 11» è verificabile e una barra non lo è. Cinque tacche fisse sono
una barra travestita.
**Costo.** Il misuratore non ha più una larghezza di tacca costante fra fascicoli diversi. La frase
in chiaro accanto («2 sur 7 éléments complétés») resta la codifica primaria, quindi il conteggio è
leggibile anche quando la tacca è di 6 px.

---

## 0. RISPOSTA ALLA REVISIONE

Nessun punto resta senza risposta. **DONE** = fatto, con il § che lo contiene. **DISPUTATO** = credo
che il revisore sbagli, con il numero che l'ho misurato.

| # | MUST-FIX | Esito | Dove |
|---|---|---|---|
| 1 | Aprire § 7, ridisegnare dentro DENSE o argomentare RICH | **DONE — ridisegnato dentro DENSE.** Niente ombre (grep `box-shadow` su `case-file.css` → **0**), niente fotografia, niente reveal `inView`, niente banda legata allo scroll, niente loop. `data-mode="dense"` dichiarato su tutti e quattro i template. La banda si comprime per **sola aritmetica di `position: sticky`** | § 0-bis, § 4.A, § 4.B, § 9 |
| 2 | `transform-origin: inline-start` non è CSS valido | **DONE — confermato da me.** `CSS.supports('transform-origin','inline-start')` = **false**; il valore calcolato ripiega su **`712px 9px`** su un blocco a piena larghezza a 1440 px, cioè il centro. Sostituito con `transform-origin: left` + `[dir="rtl"] { transform-origin: right }`. La frase del § 6 che diceva «si risolve da sola» è cancellata | § 4.F, § 5 voce 4, § 6, § 10.1 |
| 3 | Specchiare lo scrim del § 4.B | **DONE per rimozione** — lo scrim non esiste più: la fotografia è uscita (AR nessuna: il § 6 la vieta fuori da IMMERSIVE/RICH). **Correzione al rimedio proposto:** `linear-gradient(to inline-end, …)` **non è supportato** — `CSS.supports('background-image','linear-gradient(to inline-end,#000,#fff)')` = **false** (§ 10.1). Se un gradiente direzionale servisse, l'unica forma corretta sono due gradienti sotto `[dir]` | § 4.B, § 10.1 |
| 4 | Non cancellare `.state` da `register.css` | **DONE.** `class="state` è in **28 template** (contati: § 10.6). `state.css` diventa un **layer globale** importato da `main.css` dopo `register.css`; definisce `.st` e **rimappa gli otto modificatori legacy** `.state--*` sulle stesse quattro famiglie, *solo il colore*, lasciando intatta la geometria di `.state`. `register.css` non perde una riga. **Il risparmio di byte del § 7 è ritirato** | § 4.T, § 7, § 9.4 |
| 5 | Tabella reale sopra 768 | **DONE.** `table-layout: fixed` + `<col>`, nessun `display: grid` su `<tr>`, nessun `role=` inventato. `<caption>`, `<th scope="col">`, `<th scope="row">`, `data-label` conservati. **Misurato: 0 celle in overflow a 688 / 944 / 1096 / 1240 px** di larghezza di tabella | § 4.E, § 9.5, § 10.4 |
| 6 | Restituire i fatti che la riga aveva perso | **DONE.** `Facultative`, `version N`, `state_reason`, `responsible_note`: ognuno ha uno slot nominato e una misura | § 4.E |
| 7 | Restituire la frase prescritta e l'apparato di margine | **DONE.** Nota numerata verbatim, riga dei conteggi, `register.empty_text`, `.scroll-x role="region" tabindex="0"`, «Registre complet», banner del consenso: tutti disegnati | § 4.J |
| 8 | Ripensare la regola «un solo controllo» contro il consenso | **DONE — la regola è stata riscritta.** «Un'azione, **più il link che sblocca** quando c'è un blocco.» `.cf-deny` senza `href` vale solo dove `not row.is_for_the_person`; dove `row.action_blocked` il link alle Conditions resta sulla riga, com'è scritto in `apps/documents/presenters.py` righe 112-113. Ritirata anche la frase del § 1.6 che lo chiamava «un consenso che non c'entra» | § 1.6, § 4.E |
| 9 | `cf-row-settle` dichiara «layout», che non è una delle sette | **DONE.** Funzione = **causalità** (§ 2 di MOTION, famiglia LAYOUT). Ogni voce del § 5 ora dichiara **famiglia § 2 + la funzione di quella famiglia**, così le due non possono più divergere | § 5 |
| 10 | Specificare la costruzione 176 → 56, o lasciarla cadere | **DONE, senza moto.** Due strati in una `grid-template-rows: minmax(0,1fr) 56px`; la banda è `position: sticky` con `inset-block-start: calc(var(--cf-top) + 56px - 176px)`. **Misurato a ogni posizione di scroll** (0/30/60/90/119/120/121/300/1200/2500): la striscia è sempre interamente visibile sotto la barra, il rail è a **gap 0** dalla banda a ogni y, e la parte alta cala da 120 a 0 px fra y = 0 e y = 120. Nessun `height` animato, nessun `scroll()`, nessuna proprietà personalizzata guidata dallo scroll, zero JS | § 4.A, § 4.B, § 10.3 |
| 11 | `contain-intrinsic-size`, `position: relative`, tipo di `.st` | **DONE.** `content-visibility: auto` ora esiste **solo** su `.cf-files` e `.cf-versions`, sempre con `contain-intrinsic-size: auto 480px`; `.st` ha `position: relative` (verificato: il `::after` a 44 × 44 si misura sul chip, § 10.5); `.st` ha famiglia, corpo, interlinea, peso, tracking e cassa | § 4.T, § 9.4, § 9.7 |
| 12 | Percorso senza JavaScript per il cambio di stato | **DONE — e il `<dialog>` è stato abbandonato.** Il cambio di stato è un **form a pagina con conferma** (§ 9.8) dentro un `<details>` nativo sulla riga: funziona senza una riga di JavaScript, non introduce nessuna vista, nessun campo POST nuovo e nessun overlay. La domanda «un dialog per riga o uno solo» decade | § 4.G |
| 13 | «Tous les fichiers de votre compte» | **DONE — ridisegnata**, con la *stessa* grammatica di tabella del registro a una densità più bassa, non una seconda grammatica | § 4.K |
| 14 | Riconciliare § 4.C con § 9.3 | **DONE.** Tre parole di stato, codifica di forma, segmenti focalizzabili con Enter, due trame affiancate, «à titre indicatif», legenda testuale **nell'anatomia**. E la causa dell'inversione è nominata: il § 9.1 e il § 9.3 parlano di **due rail diversi** | § 4.C |

### Violazioni del round 1 — dove sono finite

| # | Violazione | Esito |
|---|---|---|
| 1 | Ombre `--shadow-2/3` su fogli, inspector, action bar | **Rimossa.** Zero `box-shadow` su questa superficie. La tesi «premium = ombre multistrato» del § 2 riga 7 è **ritirata** e sostituita (§ 4.0) |
| 2 | Fotografia a 176 px su pagina DENSE | **Rimossa.** Nessun raster su questa superficie. La risposta al committente è in § 4.0 |
| 3 | Reveal + oggetto legato allo scroll + loop | **Rimossi tutti e tre.** `cf-rail-locate` cancellato, `cf-band-compact` sostituito da `position: sticky`, `cf-skeleton` non anima più |
| 4 | Durata 1200 ms in loop, curva eased su un loop | **Decaduta** con lo skeleton. Nessun numero fuori da {120, 180, 240, 320}; nessun `linear` fuori dai loop (e non ci sono loop) |
| 5 | Funzione «layout» | **Corretta** in causalità (MUST-FIX 9) |
| 6 | Filetto `--accent` sulla targa; `--cf-drag` inventato | **Rimossi entrambi.** La versione in vigore si distingue per **peso d'inchiostro e piega**, mai per accento; il fondo di trascinamento è `--accent-wash`, che era già in `v2/tokens.css` riga 44. L'unico `--accent` prescritto su questa pagina è quello del § 9.3 sul segmento corrente del rail, ed è il documento vincolante a chiederlo |

### Segnali «cheap» — che cosa ho fatto

1. **Foto dietro scrim.** Eliminata. Non era solo vietata: era la mossa più riprodotta degli ultimi
   cinque anni e pagava una schermata sola. Al suo posto § 4.0.
2. **`2px dashed` rettangolare.** Eliminato il **rettangolo**. Il § 9.5 prescrive il tratteggio
   («bordo tratteggiato `--hairline-strong` che diventa `--accent` al drag») e quello resta, ma come
   **filetto iniziale della riga**, non come scatola: si deposita **sulla pièce**, non in un pozzo
   generico. § 4.F.
3. **Il chip = `Badge` di shadcn.** Cambiato dove contava: **raggio 999** (§ 2 — «999 sulle pillole
   di stato»; il 2 px del round 1 era per giunta fuori contratto), **cassa normale** a 14/20 in Fira
   Sans 500 — il § 3.2 riserva il maiuscolo a folio, eyebrow, stazioni e testi già bloccati, e un
   chip di stato non è nessuno dei quattro — e glifo dal nostro set a 1,5 px. Il `::after` per il
   bersaglio grosso resta ed è attribuito.
4. **Due dei quattro colori «nuovi» erano già sullo schermo.** Ammesso e corretto alla radice:
   **il round 2 introduce due valori di colore in tutto**, `--ok-800` e `--pending-100`, e ciascuno
   esiste perché una misura lo ha imposto (§ 4.T). `--st-err-bg`, `--st-ok-bg`, `--cf-field-line`,
   `--cf-drag`, `--cf-track`, `--st-*-fg` e `--st-*-line` sono **cancellati**: al loro posto ci sono
   i token che avevano già spedito.
5. **Lo spinner contro il rifiuto del candidato 1.** Risolto togliendo lo spinner — **AR-2**.
6. **L'unica idea distintiva è sotto-specificata.** § 4.D scrive lo sprite: griglia, viewBox, spessori,
   geometria della piega, otto specie, otto glifi, il segno di frontiera, il glifo arco+gradini, il
   colore, il budget e il test.

---

## 0-bis. LETTURE DI CLAUSOLA (ciò che *non* è un emendamento)

Il § 7 dice «Vietato: **ombre, vetro, reveal**» e l'§ 7 finisce «Ogni template dichiara `data-mode`;
un test lo verifica». Ecco come leggo ogni termine, perché un implementatore non deve indovinarlo.

- **Ombre** = ogni `box-shadow`. Su questa superficie: **zero**, anche in hover, anche sugli overlay
  — perché **non ci sono overlay** (§ 4.G). `grep box-shadow static/css/v3/{case-file,state,upload}.css`
  deve restituire **0 righe**: è il test.
- **Vetro** = ogni `backdrop-filter` / `filter`. Zero. Il § 2 lo concede solo all'header scrollato.
- **Reveal** = la famiglia **ENTRATA** del § 2 di MOTION: `inView`, una volta, `opacity` + `translateY`.
  Zero. Non leggo «reveal» come «ogni transizione»: il § 7 stesso mette in **Ammesso** «transizioni
  di stato, **molla di layout**», e senza transizioni di stato la riga della checklist non potrebbe
  cambiare stato — che è l'esempio *ammesso* della funzione CAUSALITÀ nel § 0 di MOTION.
- **Hover, press e focus** non sono nominati né in Ammesso né in Vietato. Li tengo, come famiglie
  HOVER e FOCUS del § 2, perché il § 9.4 prescrive esplicitamente «riga in hover livello 2» per le
  tabelle — che sono la riga DENSE del § 7. «Livello 2» qui vale come **fondo + hairline**: il
  materiale del livello 2 include `--shadow-2` *in hover*, e quella parte non la prendo, perché il
  § 7 la vieta e la specificità di modalità di pagina batte quella di componente.
- **Capitolo mezzanotte.** Il § 1.3 regola 5 ne concede **uno** fuori da HOME/FORUM. La pagina ne ha
  **uno**: la case band su `--mid-2` (§ 9.1). La barra di piattaforma da 56 px in `--mid-1` è
  **chrome**, non un capitolo: il § 1.3 dice «Il confine è un confine di sezione con transizione di
  sfondo, **non un box**», e il § 9.1 prescrive barra *e* banda insieme. Test: esattamente un
  elemento con fondo `--mid-*` dentro `{% block portal_content %}`.
- **Raggi.** § 2: «0 sui capitoli e sui fogli, 2 px sui controlli, 6 px sul tassello del marchio,
  999 sulle pillole di stato. Nessun altro.» Quindi: fogli a **0** (il `--radius-tile` 6 px del
  round 1 era un errore), controlli a `--radius-control`, chip a **999**, e `--radius-tile` non
  compare su questa superficie.

---

## 1. VERDETTO SULLO STATO ATTUALE

*(Invariato dal round 1, che il revisore ha ri-derivato e trovato esatto, salvo il § 1.6, corretto.)*

**1.1 — La V2 non è mai arrivata qui.** `casefile_measure_desktop.json` → `css: ["css/main.css",
"portal/portal.css"]`: nessuno dei sei fogli `static/css/v2/*.css`; `scripts: [… "js/dist/shell.js"]`,
`motion.js` assente. E `document.getAnimations().length === 0` su **tutte e quattro** le misure.
L'impatto di Motion non è «poco visibile»: è **zero animazioni**.

**1.2 — Il riquadro navy «Faire évoluer l'état» è illeggibile e usa un colore del marchio.**
`verso.bg = rgb(15,37,71)` = `--brand-navy`, che il § 1.3 riserva al solo lock-up. Dentro: `<select>`
320 × 25 con `background #FFFFFF` e `color #EEF2F1` → **1,13 : 1**; `<input>` 201 × 34, identico — il
testo dei campi è **bianco su bianco**. La glossa «Seules les évolutions permises…» è `rgb(74,90,98)`
su navy → **2,13 : 1**. Il bottone primario ha `background` e `border` `#0F2547` sopra una sezione
`#0F2547`: un CTA senza contorno contro il proprio fondo.

**1.3 — Il `<select>` nudo in cella.** Tre occorrenze, `125 × 22 px`, `appearance: auto`, bordo di
sistema `1px solid #767676`: 22 px **fallisce WCAG 2.2 AA 2.5.8 (24 px)**. Accanto, «Mettre à jour»
misura 138 × 44 ma con `background-color` e `border-color` `transparent`: un bottone che si legge
come testo. Il cambio di stato di un fascicolo legale è un widget del sistema operativo.

**1.4 — Nessuna gerarchia di superficie, niente di stabile, e a 768 px niente fascicolo.** Su 7
sezioni misurate, **5 hanno `background-color: rgba(0,0,0,0)`**; colonna unica di `3229 px` su
desktop e **`5552 px` a 390 px** (6,6 schermate) senza un solo elemento appiccicoso **dentro il
contenuto** — `.portal-bar` è `position: sticky` (`portal.css:24`) ma è chrome, e «PROCHAINE ÉTAPE»
e l'avanzamento escono dal campo visivo dopo la prima schermata e non tornano. In
`casefile_tablet.png` i primi 1024 px sono briciole di pane, una banda vuota di ~55 px, il titolo, la
case-band, la prossima tappa e **undici chip di navigazione su tre righe**: zero esigenze, zero
documenti, zero azioni. Su `documents_tablet.png` la prima riga del registro compare a **y ≈ 724**.

**1.5 — Otto stati resi con due colori e nessuna forma.** `documents_measure_desktop.json`: tutti gli
11 `.state` hanno `background-color: rgba(0,0,0,0)`, `border-radius: 0`, **altezza 16 px**,
`font-size: 13px`; `missing`, `replace` e «Bloqué» condividono `rgb(94,75,20)`, `expired` e `invalid`
condividono `rgb(143,29,29)`. Un bordo iniziale di 2 px è tutta la forma: non è un oggetto, è testo
colorato.

**1.6 — Il banco dei documenti non ha un deposito, e la riga non ha gerarchia.** *(Corretto: il
round 1 diceva «la riga si contraddice» e liquidava il link delle Conditions come «un consenso che
non c'entra». Era sbagliato, e `apps/documents/presenters.py` righe 112-113 dice l'opposto per
iscritto: «the Conditions gate is shown ON THE ROW with the link that resolves it (art direction A
§13.3), never as a banner above an empty box». Il difetto non è che il link ci sia; è che i tre fatti
non hanno gerarchia.)* Su `/fr/espace-reserve/mes-documents/` l'inventario dei controlli dà **2
elementi in tutta la pagina** (`under44: 0 / 2`): nessuna dropzone, nessun `input[type=file]`, nessun
progresso, nessun bottone — gli stati NEEDED → UPLOADING → PROCESSING prescritti dal § 9.5 **non
esistono come interfaccia**. E in `documents_desktop.png` la prima riga dice ÉTAT = `EXPIRÉ` e ACTION
= `BLOQUÉ` + «Accepter les Conditions d'utilisation», a capo su tre righe in ~110 px: **tre fatti di
rango diverso disegnati allo stesso rango** — è scaduta (stato), va ridepositata (conseguenza), e
prima devi accettare le Conditions (il blocco, con il link che lo toglie). La cura è la gerarchia,
non la cancellazione.

**1.7 — 1440 px di tela, 976 px di tabella, e una sola intestazione.** `table.w = 975` su casefile e
`976` su documents: ~310 px a destra completamente vuoti su entrambi. E
`headings: ["H1 Mes pièces"]`: le due sezioni sono etichettate da `<p class="folio">` puntato da
`aria-labelledby`, dieci righe di dati legali sotto un solo livello.

---

## 2. UI-UX-PRO-MAX

| # | Query esatta (`--domain`) | Output (condensato) | Esito |
|---|---|---|---|
| 1 | `case file detail view with status timeline and document checklist` (ux) | Forms/Submit Feedback; Image Scaling; Gesture Conflicts | **PARZIALE.** Tengo «Submit Feedback» → § 4.G |
| 2 | `file upload drag and drop progress states error handling` (ux) | Progress Indicators; Table Handling; Error Messages (`role="alert"`, mai il solo bordo rosso) | **2 su 3.** `role="alert"` → § 6. **RIFIUTO** la barra generica: il progresso è in **byte reali** |
| 3 | `status badge chip semantic color accessible` (color) | Tre palette di prodotto con verde/ambra/rosso generici | **RIFIUTATO.** Risponde con palette intere e le triadi violano la regola dell'accento unico. Uso i token **già spediti** in `v2/tokens.css`, più **due** valori misurati (§ 4.T) |
| 4 | `government legal case management dashboard premium` (`--design-system`) | «Trust & Authority», navy + oro, EB Garamond/Lato **via Google Fonts**, `drivers: none` | **RIFIUTATO.** È il registro respinto dal committente; l'`@import` da un CDN di font remoto è vietato dalla CSP (`style-src 'self'`) **e** dal motivo «Google Fonts hotlink» di `apps/cms/forbidden.py`. Tengo: focus 3–4 px, target 44 px, reduced-motion |
| 5 | `scroll linked progress rail timeline stepper animation` (gsap) | Skeleton shimmer 1200–1600 ms; scroll reveal; pausa offscreen | **RIFIUTATO in blocco, round 2.** Il § 7 non dà a DENSE né reveal né oggetto legato allo scroll né loop. Il round 1 ne aveva presi tre su tre |
| 6 | `document management workspace inspector panel split view` (product) | «Document Pipeline Dashboard»; «trust navy + signature green + pending amber + neutral grey» | **STRUTTURA SÌ, COLORE NO.** Il modello «pipeline» è la risposta alla tabella piatta: il documento *attraversa* stati e la riga deve mostrarlo. La palette la riduco a quattro famiglie con una regola, perché `--accent` non può significare «in corso» |
| 7 | `authoritative premium institutional depth material not flat` (style) | `skeuomorphism` (gradienti 8–12 stop, ombre multistrato), `material-you`, `soft-ui-evolution` | **RIFIUTATO, e il prestito è ritirato.** Il round 1 aveva preso «ombre di ruolo multistrato e pressione tattile». Le ombre sono vietate qui dal § 7. Resta **solo** la pressione tattile: `active { translate: 0 1px }` a 120 ms, che è la famiglia HOVER/FEEDBACK e non un'ombra |

---

## 3. 21ST.DEV — candidati confrontati

| # | Componente · URL | Che cosa prendo | Che cosa rifiuto |
|---|---|---|---|
| 1 | **File Upload** (uvain) `21st.dev/@uvain/components/file-upload` — *codice letto* | Un file rifiutato **ottiene comunque una riga** con il motivo; una riga fallita **resta al suo posto**; il progresso dice «1,4 Mo sur 12 Mo · 18 s» invece di una percentuale; il drag è un **contatore di profondità**; la barra esiste solo finché significa qualcosa; gli object URL vengono revocati | React + framer-motion + Tailwind; tinte per estensione su sei colori; `animate-spin`; `backdrop-blur` (è un `filter`); import da URL remoto |
| 2 | **Badge** (coss.com) `…/@coss.com/components/coss-badge` — *codice letto* | Una sola idea: `pointer-coarse:after:min-h-11 min-w-11` porta il bersaglio a 44 px **senza cambiare la dimensione visiva**. Verificato che funziona solo con `position: relative` sul chip (§ 10.5) | Otto varianti generiche; `disabled:opacity-64`; e — round 2 — **anche il corpo del chip**: raggio 2, cassa alta e tinta per variante sono la forma di default. Il § 2 chiede 999 e il § 3.2 non autorizza il maiuscolo qui |
| 3 | **File Upload Progress List** (sean0205) `…/@sean0205/components/c-progress-5` | Densità della riga: targa · nome · barra sottile · tempo residuo | È una coda di file, non un registro di *esigenze* |
| 4 | **Status** (diceui) `…/@diceui/components/status` | La pillola con punto indicatore: la forma dice «questo è uno stato» | Il punto **pulsa** in permanenza: è l'«esempio vietato» della riga STATO di MOTION § 0 |
| 5 | **Incident Status Timeline** (cnippet) `…/@cnippet-dev/…` | Timeline **collassabile**: corrente aperto, storico chiuso. È la risposta ai 5552 px di mobile, e in `<details>` nativi costa 0 KB | Le voci sono messaggi liberi; le nostre sono tappe governate dal Rule Engine |
| 6 | **Milestone Timeline** (7ovr) `…/@7ovr/components/timeline-1` | La semantica giusta del rail: `<ol>` con data, badge, titolo, testo | Tre soli stati e nessuna nozione di *chi* è responsabile |
| 7 | **Drawer** (coss.com) `…/@coss.com/components/drawer` | **Niente, round 2.** Non c'è più nessun drawer da costruire: l'inspector scende nell'ordine di lettura (AR-3) e il rail mobile è un `<details>` | Swipe e drag-to-dismiss su un fascicolo legale |
| 8 | **PDF Viewer** (extend-hq) | Prova che l'anteprima in pagina è tecnicamente possibile | ~1 MB di WASM contro 45 KB; e un file non ancora analizzato non può essere reso a nessuno tranne il depositante. La miniatura resta una **targa disegnata** |
| 9 | **Upload Dropzone Empty State** (arihantcodes) | Lo stato vuoto **è** la dropzone | Lo stato vuoto animato è delizia gratuita su dati sensibili |
| 10 | **Status Bar** (openstatusHQ) | **Navigazione da tastiera reale** sui segmenti: è ciò che il § 9.3 chiede («segmenti focalizzabili, Enter apre il dettaglio») e che il round 1 non aveva scritto | Una barra per giorno serve l'uptime |

---

## 4. LA PROPOSTA

### 4.0 La tesi premium, riscritta per DENSE

Il round 1 aveva scritto: «premium si ottiene con ombre di ruolo multistrato». Su questa pagina è
falso *per regola*, e sarebbe stato debole comunque. La tesi del round 2:

> **Su una pagina densa il premium è il registro, non la profondità.**

Tre cose lo portano, e nessuna delle tre viene da una libreria.

1. **La targa.** Ogni esigenza ha un oggetto disegnato: un foglio 36 × 46 con l'angolo piegato e il
   segno della specie, in otto specie, più otto glifi di stato e un segno di frontiera MA → IT. Sette
   targhe disegnate su una pagina sono **più immagine** di una fotografia di stock, e sono nostre. È
   la risposta al committente che dice «non ci sono abbastanza immagini»: non gli manca una foto, gli
   manca che i suoi oggetti abbiano una faccia. § 4.D.
2. **Il filetto come sistema.** Le superfici si separano per **fondo + hairline + ritmo di 4 px**, mai
   per ombra. Quattro ruoli di filetto e nessun quinto: hairline informativo (`--hairline`, 1 px),
   confine di componente (`--hairline-strong`, 1 px, **3,59 : 1** su `--min-2`), apertura di banda
   (2 px `--ink`), riga in ritardo (3 px `--err-700`, **6,27 : 1**). Un foglio che si stacca per un
   bordo e un tono è più difficile da disegnare di uno che si stacca per un'ombra: è il mestiere che
   questa pagina chiede.
3. **La banda che non se ne va.** 176 px di mezzanotte che diventano una striscia di 56 px per **sola
   aritmetica di `position: sticky`**, misurata a ogni y (§ 10.3). Il riferimento, lo stato e la
   prossima azione sono sullo schermo a ogni posizione di scroll, e non è costato un'animazione, un
   listener o un byte di JavaScript. La quiete a quel prezzo è un lusso.

### 4.A Anatomia

```
                 ┌ barra di piattaforma (chrome, sticky, --cf-top = 56)
≥1280  .cf-band  │ 176 → 56, sticky, --mid-2, l'unico capitolo mezzanotte
       .cf-rail  │ rail 2.0 (§ 9.3): <ol> a TUTTA LARGHEZZA sopra le colonne, sticky sotto la banda
       .portal   │ [ nav 224 ][ workspace 1fr ]          gutter 24        (AR-3: niente terza colonna)
1024–1279        │ identico; workspace 848
 768–1023        │ nav → striscia orizzontale 36 px (§ 9.1); workspace a tutta larghezza 688
                 │ rail 2.0 → verticale (§ 9.3: «Verticale sotto 1024»)
  <768           │ workspace in <details>; rail 2.0 → <details> con pastiglia «Étape 2 sur 7»
                 │ .cf-actionbar sticky in basso, 64 px, una sola azione + il conteggio
```

**I due rail non sono lo stesso oggetto** — è la causa dell'inversione del round 1. Il § 9.1 (3)
descrive il **rail di navigazione** (`.portal__aside`, `components/local_nav.html`, 224 px, che sotto
1024 diventa una striscia orizzontale da 36 px). Il § 9.3 descrive il **rail di giurisdizione /
responsabilità 2.0**, che è «`<ol>` di N segmenti a tutta larghezza **sopra** le colonne» e
«**Verticale sotto 1024**». Il round 1 li aveva fusi in una colonna da 264 px e aveva quindi invertito
entrambi. Round 2: si seguono le due clausole alla lettera. Larghezze del § 9.1 adottate senza
modifiche: **224 / 1fr**, e 36 px per la striscia sotto 1024.

Il contenitore misurato sul sito vivo (§ 10.2): **688 px a 768 · 944 a 1024 · 1096 a 1280 · 1240 a
1440 · 1360 da 1600**. Larghezza del workspace = contenitore − 224 − 24 sopra 1024, contenitore
sotto. Il registro ci sta senza overflow a tutte e cinque (§ 10.4).

Tutte le sporgenze appiccicose passano da **un solo token**:

```css
:root { --cf-top: 56px; }            /* l'altezza della barra di piattaforma del § 9.1 */
.cf-band { inset-block-start: calc(var(--cf-top) + var(--cf-band-strip) - var(--cf-band-h)); }
.cf-rail { inset-block-start: calc(var(--cf-top) + var(--cf-band-strip)); }
.portal__aside { inset-block-start: calc(var(--cf-top) + var(--cf-band-strip) + var(--cf-rail-h) + var(--s-4)); }
```

Il giorno in cui la barra cambia altezza, si cambia `--cf-top` e la pagina intera segue. È anche la
risposta allo «stato transitorio» che il round 1 aveva lasciato indefinito: **non c'è uno stato
transitorio**, perché niente si anima; la geometria è esatta a ogni y (§ 10.3).

### 4.B `.cf-band` — la banda di contesto, senza fotografia e senza moto

Fondo `--mid-2` (§ 9.1: «Case band `--mid-2`»). **Nessuna fotografia**: il § 6 riserva «altre
fotografie» a IMMERSIVE e RICH, e questa pagina è DENSE. **Nessuno scrim**, quindi nessuna
asimmetria RTL da riparare. Due strati in una griglia, e la compressione è la sticky:

```css
.cf-band {
  position: sticky;
  inset-block-start: calc(var(--cf-top) + var(--cf-band-strip) - var(--cf-band-h)); /* = -64px */
  z-index: 3;
  display: grid;
  grid-template-rows: minmax(0, 1fr) var(--cf-band-strip);   /* 120 + 56 = 176 */
  block-size: var(--cf-band-h);
  background: var(--mid-2);
  color: var(--on-dark);
  border-radius: 0;                                          /* § 2: 0 sui capitoli */
}
```

Scorrendo, la parte alta esce dallo schermo sotto la barra di piattaforma e la striscia da 56 px si
incolla. Misurato (§ 10.3): a y = 0 la parte alta è 120 px; a y = 60 è 60; a y = 120 è 0 e resta 0
fino in fondo; la striscia è **sempre** interamente visibile e il rail le è **sempre** attaccato a
gap 0. Nessuna `@keyframes`, nessun `transition`, nessun listener, nessun `scroll()`.

**Parte alta (120 px)** — breadcrumb (dal guscio), `<h1>` «Dossier» in `--t-entry` serif, obiettivo in
`--on-dark-2` (**8,79 : 1** su `--mid-2`), responsabile con glifo di ruolo, e il **misuratore**
(§ 4.B1).
**Striscia (56 px)** — riferimento in mono `--accent-dark` (**9,09 : 1**), pillola di stato in
variante scura, e la prossima azione come INLINE ACTION. Tre fatti, una riga, sempre visibili.
Separate da `border-block-start: 1px solid var(--hairline-dark-strong)` — composita a **rgb(74, 89,
97)**, **2,19 : 1** sul fondo: è un filetto di ritmo, non un'informazione, e non deve raggiungere 3:1.

Rapporti calcolati **contro `--mid-2`**, che il documento vincolante non tabula (§ 1.2 dà i rapporti
su `--mid-1` e `--mid-3`): `--on-dark` **14,08** · `--on-dark-2` **8,79** · `--on-dark-3` **5,85** ·
`--accent-dark` **9,09** · `--terr-line` **5,51** · `--seal-300` **7,00**.

**AR-1 — banda territoriale** al margine finale, se l'emendamento passa:

```css
.cf-band::after {
  content: ""; position: absolute; inset-block: 0; inset-inline-end: 0;
  inline-size: 56px; pointer-events: none;
  background-image: repeating-linear-gradient(90deg,
    var(--terr-line) 0 1px, transparent 1px 14px);
  opacity: .55;                  /* statico, mai animato */
}
[dir="rtl"] .cf-band::after { transform: scaleX(-1); }
@media (forced-colors: active) { .cf-band::after { display: none } }
```

### 4.B1 Il misuratore (AR-4)

```html
<p class="cf-meter">
  <span class="cf-meter__ticks" aria-hidden="true">
    <span class="is-on"></span><span class="is-on"></span><span></span><span></span>
    <span></span><span></span><span></span>
  </span>
  <span class="cf-meter__count">{% blocktranslate %}{{ done }} sur {{ total }} éléments complétés{% endblocktranslate %}</span>
</p>
```
```css
.cf-meter { display: flex; align-items: center; gap: var(--s-3); margin: 0; }
.cf-meter__ticks { display: flex; gap: 4px; inline-size: 120px; flex: none; }
.cf-meter__ticks > span {
  flex: 1; min-inline-size: 6px; block-size: 8px; border-radius: 0;
  border: 1px solid var(--on-dark-3);         /* 5,85 : 1 su --mid-2 — tacca vuota */
  background: transparent;
}
.cf-meter__ticks > .is-on {
  background: var(--accent-dark);             /* 9,09 : 1 — tacca piena */
  border-color: var(--accent-dark);
}
.cf-meter__count { font-size: var(--t-small); color: var(--on-dark-2); font-variant-numeric: tabular-nums; }
```
Onestà sulla misura: **piena contro vuota vale 1,56 : 1** — la distinzione **non** è di luminanza, è
di **forma** (pieno contro contorno), che è esattamente il vocabolario del § 9.3 («pieno / bordo /
attenuato»), e il conteggio è comunque in parole. Entrambe le forme superano 3 : 1 **contro il
fondo**, che è ciò che 1.4.11 chiede (5,85 e 9,09). Da N = 11 il blocco `.cf-meter__ticks` non viene
reso e resta la sola frase.

### 4.C `.cf-rail` — responsabilità 2.0, riconciliato con il § 9.3

`<ol>` di N segmenti **a tutta larghezza sopra le colonne**, sticky sotto la striscia della banda.
Ogni `<li>`:

```html
<li class="cf-rail__step is-current" aria-current="step">
  <a class="cf-rail__hit" href="{{ step.url }}">
    <span class="cf-rail__bar cf-rail__bar--authority" aria-hidden="true"></span>
    <span class="cf-rail__n t-ref">4</span>
    <span class="cf-rail__label">Parcours régulier</span>
    <span class="cf-rail__owner"><svg class="cf-glyph" width="20" height="20" aria-hidden="true"
      focusable="false"><use href="{% static 'img/v3/case-glyphs.svg' %}#owner-authority"></use></svg>
      L’autorité compétente</span>
    <span class="cf-rail__state">{% translate "Étape actuelle" %}</span>
    <span class="visually-hidden">{% blocktranslate %}Étape {{ n }} sur {{ total }} — Vous êtes ici{% endblocktranslate %}</span>
  </a>
  <span class="cf-rail__frontier" aria-hidden="true"><svg width="20" height="20"><use href="…#frontier-ma-it"></use></svg></span>
  <span class="cf-rail__indicative">{% translate "à titre indicatif" %}</span>
</li>
```

Quello che il § 9.3 chiede e il round 1 non aveva scritto, adesso c'è tutto:

- **Le tre parole di stato**, in chiaro e non solo per lo screen reader: `Terminée` · `Étape
  actuelle` · `À venir`, in `.cf-rail__state`, `--t-caption`, `--ink-3` (5,88 : 1 su `--min-2`).
- **La codifica di forma**: `is-done` → barra **piena**; `is-current` → `border: 2px solid
  var(--accent)` sul segmento + un marcatore triangolare da 8 px sotto la barra; `is-todo` → barra
  con **solo contorno** `--hairline-strong`. L'`--accent` sul segmento corrente **è prescritto dal
  § 9.3** («bordo `--accent` 2 px + marcatore»): non è un'invenzione di questa specifica, ed è l'unico
  `--accent` non-interattivo della pagina.
- **Segmenti focalizzabili, Enter apre il dettaglio**: `.cf-rail__hit` è un `<a>` vero, target
  `min-block-size: 44px`, anello di focus come tutti gli altri.
- **Due trame affiancate** per le tappe multi-attore.
- **«à titre indicatif»** in chiaro dove `cases.services` / Rule Engine non ha dato.
- **Legenda testuale**, nell'anatomia e non solo nei rischi: `<p class="cf-rail__legend">` sotto
  l'`<ol>`, che nomina le cinque trame a parole — «plein : la personne · hachures : l'équipe ·
  points : l'organisme de formation · lignes : l'autorité compétente · tirets : le territoire».
- **Frontiera MA → IT** fra le tappe che cambiano riva, specchiata in RTL.
- **Verticale sotto 1024** (§ 9.3), `<details>` sotto 768.

Trame, con i rapporti misurati su `--min-1`:

```css
.cf-rail__bar { block-size: 10px; border-radius: 0; }
.cf-rail__bar--person    { background: var(--owner-person); }                        /* 5,29 : 1 */
.cf-rail__bar--project   { background: repeating-linear-gradient(45deg,
                             var(--owner-project) 0 2px, transparent 2px 5px); }     /* 7,03 : 1 */
.cf-rail__bar--training  { background: radial-gradient(circle at 2px 2px,
                             var(--owner-training) 1.25px, transparent 1.25px) 0 0 / 5px 5px; } /* 5,91 */
.cf-rail__bar--authority { background: repeating-linear-gradient(0deg,
                             var(--owner-authority) 0 1.5px, transparent 1.5px 4px); }          /* 3,99 */
.cf-rail__bar--territory { background: repeating-linear-gradient(90deg,
                             var(--owner-territory) 0 6px, transparent 6px 10px); }             /* 5,21 */
/* multi-attore: due trame adiacenti, non sovrapposte */
.cf-rail__bar--dual { background-size: 100% 50%, 100% 50%;
                      background-position: top, bottom; background-repeat: no-repeat; }
@media (forced-colors: active) {
  .cf-rail__bar { forced-color-adjust: none; background: Canvas; border: 2px solid CanvasText; }
  .cf-rail__bar--project   { border-style: dashed; }
  .cf-rail__bar--training  { border-style: dotted; }
  .cf-rail__bar--authority { border-style: double; }
  .cf-rail__bar--territory { border-style: groove; }
}
```
`forced-color-adjust: none` **solo** su `.cf-rail__bar`, come prescrive il § 11.

### 4.D Lo sprite — `static/img/v3/case-glyphs.svg`

Il revisore ha ragione: è l'unica idea qui che una libreria non poteva dare, e il round 1 le aveva
dedicato una frase. Ecco le regole di disegno, complete abbastanza per essere incise.

**Contratto generale** (§ 6: set proprio, tratto 1,5 px, 20 px, `currentColor`).
Un solo file, `<symbol>` con `id`, servito da `static/`, un solo request, riusato con `<use>`.
`fill: none`, `stroke: currentColor`, `stroke-width: 1.5`, `stroke-linecap: butt`,
`stroke-linejoin: miter`, `vector-effect: non-scaling-stroke`.

**Le targhe** — `viewBox="0 0 36 46"`, rese a 36 × 46 px CSS.

*Sagoma.* Un foglio con l'angolo iniziale-alto **piegato**, piega da 10:

```
outline : M 2.75 2.75 H 23 L 33.25 13 V 43.25 H 2.75 Z
piega   : M 23 2.75 V 13 H 33.25            (la piega "aperta": due cateti)
sigillo : M 23 2.75 L 33.25 13              (la piega "chiusa": la sola ipotenusa)
```
`#plate-fold-sealed` è un `<symbol>` a sé, sovrapposto con un secondo `<use>` **solo quando la
versione è quella in vigore** (`row.current.is_current`). Una versione superata mostra la piega
aperta. **È l'unica codifica di «en vigueur» sulla targa: nessun colore, nessun accento.** La parola
«En vigueur» resta nel markup, come oggi (`requirement_detail.html:95`).

*Campo della specie.* Un quadrato 20 × 20 centrato in (18, 29) — il terzo basso del foglio. Nessun
tratto entra a meno di 3 dal contorno. Al massimo quattro tratti per specie.

| `id` | specie | disegno (coordinate nel viewBox 36 × 46) |
|---|---|---|
| `plate-passport` | passeport | due linee x 8→28 a y 33 e y 37 (la banda a lettura ottica) + un chevron largo 6 con vertice a (18, 25) |
| `plate-diploma` | diplôme | cerchio r 4 in (18, 27) + due nastri: (16,31)→(15,37) e (20,31)→(21,37) |
| `plate-contract` | contrat | linea x 9→27 a y 35 + una firma: `M 11 32 Q 15 26 18 32 T 25 31` |
| `plate-civil` | état civil | verticale x 12, y 22→38 + tre tacche x 12→26 a y 25, 30, 35 |
| `plate-criminal` | casier | corpo 12 × 9 in (12, 29) + arco della staffa r 3 centrato in (18, 29) |
| `plate-nullaosta` | nulla osta | il segno di frontiera ridotto a 16 di larghezza, centrato in (18, 30) |
| `plate-attestation` | attestation | poligono a 9 lati r 5 in (18, 28), nessun riempimento |
| `plate-other` | autre | una sola linea x 13→23 a y 30 — l'assenza di segno, dichiarata |

*Inchiostro.* `color: var(--ink-3)` a riposo (**5,88 : 1** su `--min-2`); `color: var(--ink)`
(**15,56 : 1**) sulla riga che chiede un'azione a questa persona. Mai `--accent`, mai `--seal-*`
(il bronzo è dei sigilli), mai un colore di famiglia di stato: la targa dice **che cosa è**, il chip
dice **come sta**.

**Gli otto glifi di stato** — `viewBox="0 0 20 20"`, resi a 16 × 16 nel chip e a 20 × 20 altrove.

| `id` | stato (§ 9.5) | disegno |
|---|---|---|
| `g-needed` | NEEDED / `missing` | quadrato vuoto 12 × 12 in (4, 4) |
| `g-uploading` | UPLOADING (transiente) | asta x 10 da y 15 a y 5 + punta (6,9)→(10,5)→(14,9) |
| `g-processing` | PROCESSING / `filed` | vassoio: linea x 4→16 a y 13 + due ritorni verticali di 4 |
| `g-review` | UNDER REVIEW / `in_review` | lente: cerchio r 5 in (8,8) + manico (12,12)→(16,16) |
| `g-valid` | VALID / `valid` | spunta (4,10)→(8,14)→(16,5) |
| `g-rejected` | REJECTED / `invalid` | croce (5,5)→(15,15) e (15,5)→(5,15) |
| `g-expiring` | EXPIRING / `to_replace` | clessidra: due triangoli che si toccano in (10,10), campo 10 × 14 |
| `g-expired` | EXPIRED / `expired` | calendario 12 × 11 in (4,5) + due montanti di 3 + diagonale (4,16)→(16,5) |

**`#frontier-ma-it`** — due segmenti di riva (x 1→6 e x 14→19 a y 10) con una tacca verticale a x 10,
y 5→15. Specchiato in RTL con `transform: scaleX(-1)` sullo `<use>` (§ 11).
**`#door-arch-steps`** — il glifo arco + gradini del § 6, reso a 48 px negli stati vuoti: arco r 12 su
una base x 4→28 + tre gradini da 4 di altezza, larghi 20, 16, 12. **Mai la porta intera fuori
dall'hero** (§ 6).
**`#owner-person` · `#owner-project` · `#owner-training` · `#owner-authority` · `#owner-territory`** —
i cinque glifi di ruolo del § 6, 20 × 20, l'autorità con anello a sigillo.

**Budget e prova.** 8 targhe + 1 piega + 8 glifi di stato + 1 frontiera + 1 arco-gradini + 5 ruoli =
**24 `<symbol>`**. Tetto: **≤ 4 096 byte grezzi, ≤ 1 600 byte gzip**, fallito da
`tests/frontend/test_v3_assets.py` se superato. Nessun `<image>`, nessun `<filter>`, nessun
`<style>` dentro l'SVG (CSP), nessun `fill` letterale: tutto `currentColor`.

### 4.E `.cf-req` — la riga di esigenza

**Una tabella vera a ogni larghezza sopra 768**, `table-layout: fixed` con `<col>`, `<caption>`,
`scope`, cifre tabellari, `data-label` su ogni cella. Nessun `display: grid` su `<tr>`, nessun `role`
ARIA a rimpiazzare ciò che il markup dà già (§ 9.4 e il contratto scritto in
`apps/portal/static/portal/portal.css:379: «Above 768 the table is a real table and the header is
read normally»`).

Cinque colonne, come oggi. **La targa non ha una colonna propria**: vive dentro il `<th scope="row">`,
il che elimina anche il `<td aria-hidden="true">` decorativo che il round 1 aveva inventato.

| colonna | token | px | che cosa porta |
|---|---|---|---|
| Élément | — | `1fr` | targa 36 × 46 · titolo (link) · `source_ref` in mono · **`Facultative`** · **`version N`** · **`state_reason`** |
| État | `--cf-col-state` | **148** | il chip `.st` (il più largo in FR misura **122,02 px**) |
| Responsable | `--cf-col-owner` | **148** | `row.responsible` · **`responsible_note`** su riga propria |
| Échéance | `--cf-col-due` | **84** | `<time>` in mono a cifre tabellari |
| Action | `--cf-col-act` | **136** | **una** azione INLINE (§ 10 «mono 13 px con freccia») + il link che sblocca, quando c'è |

Misurato (§ 10.4): **0 celle in overflow** con larghezze di tabella 688 · 944 · 1096 · 1240, in FR e
in AR, con i titoli e le etichette reali — compreso «Le professionnel mandaté» e «Identifier les
interlocuteurs et les autorités compétentes». Sotto 1024 il `padding-inline-end` delle celle passa da
16 a 12 px: sono i 16 px che fanno stare la riga a 688.

**I fatti restituiti** (MUST-FIX 6), con il posto e il motivo:

- `{% if not row.mandatory %}Facultative{% endif %}` → `.cf-req__tag`, `--t-caption`, `--ink-3`, sulla
  riga dei tag sotto il titolo. È una qualità della *pièce*, sta con la pièce.
- `version {{ row.version_count }}` → stesso posto, in mono `--t-folio`, separato da un `·`.
- `row.state_reason` → `.cf-req__reason`, `--t-caption`, `--ink-3`, **sotto il titolo** e non sotto il
  chip: è una frase, e la colonna État ha 136 px utili mentre Élément ne ha 724 a 1440. Solo le righe
  che hanno un motivo pagano l'altezza.
- `row.responsible_note` → `.cf-req__note`, `display: block`, `--t-caption`, nella cella Responsable.
  Misurato: «Sportello Unico di Milano» e «mandat du 04.03.2026» stanno in 136 px su due righe, 0
  overflow.
- `row.state_rule` → **non** ripetuto su ogni riga. Va nella **legenda del registro**: un `<dl>` sotto
  la tabella che elenca *solo gli stati presenti in questa pagina*, ciascuno con il suo chip e la sua
  regola da `documents.requirements.STATE_RULES`. Ogni parola porta la sua regola, una volta, dove si
  può leggere per intero invece che in 136 px.

**L'azione** — la regola riscritta (MUST-FIX 8):

> **Un'azione, mai due. Più il link che toglie il blocco, quando c'è un blocco.**

```django
<td data-label="{% translate 'Action' %}">
  {% if row.may_file %}
    <a class="cf-act" href="{{ row.detail_url }}">{% if row.current %}{% translate "Remplacer la pièce" %}{% else %}{% translate "Déposer la pièce" %}{% endif %}<span class="cf-act__arrow" aria-hidden="true">→</span></a>
  {% elif row.action_blocked %}
    <span class="st st--pending"><svg class="st__glyph" aria-hidden="true" focusable="false"><use href="{% static 'img/v3/case-glyphs.svg' %}#g-needed"></use></svg>{% translate "Bloqué" %}</span>
    <span class="cf-req__unblock">{% safe_url 'legal:terms' as terms_url %}{% if terms_url %}<a href="{{ terms_url }}">{% translate "Accepter les Conditions d’utilisation" %}</a>{% else %}{% translate "Acceptation des Conditions d’utilisation requise." %}{% endif %}</span>
  {% elif not row.is_for_the_person %}
    <p class="cf-deny"><svg class="cf-glyph" aria-hidden="true" focusable="false"><use href="…#owner-authority"></use></svg>{% blocktranslate with who=row.responsible %}Attendu de : {{ who }}{% endblocktranslate %}</p>
  {% else %}
    <a class="cf-act" href="{{ row.detail_url }}">{% translate "Consulter" %}<span class="cf-act__arrow" aria-hidden="true">→</span></a>
  {% endif %}
</td>
```

`.cf-deny` (nessun `href`) vale **solo** nel ramo `not row.is_for_the_person`. Non tocca mai un
`action_blocked`, dove togliere il link significherebbe togliere l'unica via d'uscita. Il presenter
resta esattamente com'è.

**Il link che risponderebbe 403 non viene mai disegnato**: `{% if v.download_url %}…{% elif
v.delivery_block %}<p class="cf-deny">{{ v.delivery_rule }}</p>{% endif %}` — che è ciò che
`documents.presenters.present_version` (righe 69-76) già calcola.

`row.is_overdue`: `border-inline-start: 3px solid var(--err-700)` (**6,27 : 1** su `--min-2`) **e** la
parola «En retard» in `.cf-req__tag`, mai il solo filetto.

**Hover della riga**: fondo `--min-1`, transizione `--motion-fast` `--ease-out`, dentro
`@media (prefers-reduced-motion: no-preference)` e dentro `@media (hover: hover)`. Nessuna ombra:
«livello 2 in hover» del § 9.4 qui vale come fondo + hairline (§ 0-bis).

### 4.E1 La fiche — il pop-in del § 9.4 sotto 768

Il pop-in è il costrutto prescritto e resta. Quello che cambia è la **geometria**: cinque coppie
impilate producono una riga di **292 px** a 390 (misurato). Le stesse cinque coppie in due colonne per
le celle corte producono **183–205 px** (misurato). Nessuna etichetta sparisce: `data-label` resta su
ogni cella e ogni `::before` viene scritto.

```css
@media (max-width: 47.99rem) {
  .cf-register tr {
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
    grid-template-areas: "elem elem" "state due" "owner act";
    column-gap: var(--s-4); row-gap: 10px;
    padding-block: 14px; border-block-end: 1px solid var(--hairline);
  }
  .cf-register th { grid-area: elem; padding: 0; border: 0; }
  .cf-register td { padding: 0; border: 0; min-block-size: 44px; }
  .cf-register td:nth-of-type(1) { grid-area: state }
  .cf-register td:nth-of-type(2) { grid-area: owner }
  .cf-register td:nth-of-type(3) { grid-area: due }
  .cf-register td:nth-of-type(4) { grid-area: act }
  .cf-register td::before {
    content: attr(data-label); display: block;
    font-family: var(--f-mono); font-size: var(--t-caption); line-height: var(--t-caption-lh);
    letter-spacing: var(--track-folio); text-transform: uppercase; color: var(--ink-3);
    margin-block-end: 2px;
  }
}
```
La tabella conserva `display: block` su `tbody`/`tr`/`th`/`td` e `<thead>` nascosto visivamente, come
in `portal.css`; la fiche aggiunge solo la griglia. Il selettore è `.cf-register`, non
`table:has(tbody [data-label])`: la regola globale di `portal.css` continua a servire ogni altra
tabella del prodotto, invariata.

### 4.F `.cf-drop` — deposito, senza rettangolo tratteggiato

Un `<form enctype="multipart/form-data">` che **funziona senza JavaScript**, sullo stesso endpoint
(`row.upload_url` = `documents:requirement_file`) e con lo stesso CSRF. Con JS,
`XMLHttpRequest.upload.onprogress` per i byte reali. **Nessuna vista nuova, nessun contratto dati
nuovo.**

Il § 9.5 prescrive «bordo tratteggiato `--hairline-strong` che diventa `--accent` al drag». Lo tengo
— ma come **filetto**, non come scatola, perché la scatola tratteggiata è il gesto di default:

```css
.cf-drop {
  border-inline-start: 2px dashed var(--hairline-strong);   /* 3,59 : 1 su --min-2 */
  padding-inline-start: var(--s-6);
  background: var(--min-2);
  position: relative;
}
.cf-drop.is-armed { border-inline-start: 2px solid var(--accent); }   /* 6,05 : 1 */
.cf-drop::before {                        /* lo strato di trascinamento, già composto */
  content: ""; position: absolute; inset: 0; background: var(--accent-wash);
  opacity: 0; pointer-events: none;
}
.cf-drop.is-armed::before { opacity: 1; }
.cf-drop[aria-disabled="true"] { background: var(--min-1); border-inline-start-style: solid; }
```
`--accent-wash` è il token già spedito (`v2/tokens.css:44`): `--accent` ci sta sopra a **5,24 : 1**,
`--ink` a **13,48 : 1**. Il `--cf-drag: #E3F1F2` del round 1 è cancellato.

**La zona di rilascio è la riga dell'esigenza**, non un pozzo separato: si deposita *sulla pièce*.
`dragenter`/`dragleave` con un **contatore di profondità**, così il fondo non sfarfalla sui figli.

Stato disabilitato: fondo `--min-1`, testo `--ink-3` (**5,14 : 1** su `--min-1`), **e la frase che
risolve il blocco, con il link** — mai una sola opacità.

**La coda** — `<ul>`, una riga per file: targa · nome in mono `--t-folio` · **una riga di byte reali e
tempo residuo** («1,4 Mo sur 12 Mo · 18 s») · barra:

```css
.cf-drop__bar { block-size: 4px; background: var(--hairline); overflow: hidden; }
.cf-drop__fill {
  block-size: 100%; background: var(--accent);
  transform: scaleX(0); transform-origin: left;     /* MAI width */
}
[dir="rtl"] .cf-drop__fill { transform-origin: right; }
@media (prefers-reduced-motion: no-preference) {
  .cf-drop__fill { transition: transform var(--motion-base) var(--ease-standard); }
}
```
`transform-origin: inline-start` **non esiste** — `CSS.supports` restituisce `false` e il valore
calcolato ripiega sul centro (§ 10.1). La traccia `--hairline` sta a **1,45 : 1** sul foglio: è
deliberato e ammesso, perché l'informazione è **nei byte scritti accanto**, non nella barra, e 1.4.11
non chiede contrasto a una parte la cui resa visiva non è necessaria per capire lo stato. Riempimento
`--accent` contro traccia: **4,17 : 1**.

La barra **esiste solo mentre trasferisce**: a fine corsa sparisce e lascia la parola. Un file
rifiutato **ottiene la sua riga** in famiglia rossa col motivo («Trop volumineux — 14 Mo sur 10 Mo
autorisés», `role="alert"`); un trasferimento fallito **resta al suo posto** e fa crescere
«Réessayer», offerto solo quando il fallimento è ritentabile.

### 4.G `.cf-transition` — il cambio di stato, form a pagina, zero JavaScript, zero overlay

Il round 1 proponeva un `<dialog>`: senza JS non si apre, e il § 9.8 prescrive «cambio di stato come
**form a pagina** con conferma». Il `<dialog>` è **abbandonato**. Con lui se ne va l'ultimo overlay
della pagina — e quindi l'ultima ragione per cui questa specifica avrebbe dovuto chiedere un'ombra.

`section--verso` (il box navy del § 1.2) sparisce. Al suo posto, **su carta**:

```django
<details class="cf-transition" id="tr-{{ item.pk }}">
  <summary class="cf-transition__open">{% translate "Faire évoluer cette ligne" %}</summary>
  <form method="post" action="{% url 'cases:set_item_status' case.reference item.pk %}" class="cf-form">
    {% csrf_token %}
    <p class="cf-form__now">{% blocktranslate with s=item.get_status_display %}État actuel : {{ s }}{% endblocktranslate %}</p>
    <p class="cf-form__field">
      <label for="status-{{ item.pk }}">{% translate "Nouvel état de cette ligne" %}</label>
      <select id="status-{{ item.pk }}" name="status" aria-describedby="help-{{ item.pk }}">
        {% for value, label in statuses %}<option value="{{ value }}"{% if value == item.status %} selected{% endif %}>{{ label }}</option>{% endfor %}
      </select>
      <span class="cf-form__help" id="help-{{ item.pk }}">{% translate "Seules les évolutions permises par l’état actuel sont proposées. Chaque changement est enregistré." %}</span>
    </p>
    <p class="cf-form__actions"><button type="submit" class="btn btn--primary">{% translate "Enregistrer ce changement" %}</button></p>
  </form>
</details>
```

- **Conferma** (§ 9.8): la conferma è la struttura in due tempi — aprire il pannello, leggere la frase
  che nomina lo stato attuale, premere un bottone che dice che cosa fa. **Nessun campo POST nuovo**:
  la vista `cases.views.set_item_status` legge `request.POST["status"]` e nient'altro, oggi come
  domani.
- **Senza JavaScript funziona**: `<details>` è nativo, il `<form>` è un form.
- **2.5.8**: `<select>` e `<input>` a **48 px** (§ 10), `background: var(--min-3)`, `color: var(--ink)`
  (**15,56 : 1**), `border: 1px solid var(--ink-3)` (**5,88 : 1** — il `--cf-field-line: #55646B` del
  round 1 *era* `--ink-3`, byte per byte: cancellato e sostituito dal token vero), etichetta visibile
  sopra, aiuto sotto via `aria-describedby`. Il `<select>` nudo da 125 × 22 in cella sparisce.
- Il `<summary>` è un bersaglio da 44 px con `list-style: none` e un marcatore disegnato (`::before`
  con un glifo, non un triangolo di sistema).
- La stessa forma, una sola volta e non per riga, per il cambio di stato **del fascicolo**
  (`cases:transition`), come ultimo foglio dello spazio di lavoro.

### 4.H L'inspector, nell'ordine di lettura (AR-3)

Tutto il contenuto del § 9.7 resta, e resta nell'ordine: **primo foglio** dello spazio di lavoro,
`.cf-sheet--quiet`, dopo il rail e prima del registro.

- pré-évaluation: «Parcours pertinent», jeu de règles col **sigillo `--seal-600`** (**4,57 : 1** su
  `--min-2` — il bronzo è dei sigilli, § 1.3 regola 3), e **la frase prescritta sempre presente**;
- storico delle versioni (`.cf-versions`), scadenze, messaggi;
- mai una decisione, mai un numero non calcolato.

La **permanenza** che il § 9.7 cercava è portata dalla striscia della banda, che non lascia mai lo
schermo. Un test confronta la sequenza del testo a 1600 e a 390: identica.

### 4.I I tre livelli di foglio, senza una sola ombra

```css
.cf-sheet          { background: var(--min-2); border: 1px solid var(--hairline);
                     border-radius: 0; padding: var(--s-6) var(--s-8); }         /* livello 2 */
.cf-sheet--acting  { border-inline-start: 3px solid var(--accent);               /* § 9.2 */
                     background: var(--min-3); }                                 /* livello 3 par le ton */
.cf-sheet--quiet   { background: var(--min-1); border: 0;
                     border-block-start: 1px solid var(--hairline-strong); }      /* livello 1 */
```
Tre livelli e nessun quarto. Si separano per **fondo** (`--min-1` 1,14 : 1 · `--min-2` · `--min-3`
contro `--min-2` 1,03 : 1) e per **peso di filetto** (`--hairline` 1,45 : 1, `--hairline-strong`
3,59 : 1). Il salto di tono è piccolo: è il filetto a fare il lavoro, ed è per questo che il suo peso
è un sistema di quattro ruoli e non una scelta caso per caso. `grep box-shadow` su questo foglio:
**zero righe**.

### 4.J L'apparato di margine del registro (MUST-FIX 7)

Tutto quello che `templates/documents/partials/register.html` porta oggi resta, e ha un posto
disegnato.

1. **La nota prescritta**, verbatim, `<p class="note doc-register__note"><span class="note__marker">1</span>`
   + «L'état d'une pièce dit ce que le dossier a reçu, et rien de plus. **Aucune ligne de ce registre
   ne vaut acceptation.**» — testo bloccato: **nessun moto, nessun reveal, mai in un `<details>`, mai
   troncato**. Sopra 1280 vive in una **colonna di margine** vera da `--cf-margin-w: 264px` alla fine
   della sezione (`grid-template-columns: minmax(0,1fr) var(--cf-margin-w)`), il che usa i ~310 px a
   destra che il § 1.7 aveva trovato vuoti; sotto 1280 scende sotto la tabella, col suo marcatore.
2. **La riga dei conteggi** (`.doc-register__counts`): «7 pièces demandées · 1 sur 7 validées» in
   `--t-small`, e il conteggio aperto come chip `.st st--pending` con il glifo `#g-needed`. Mai una
   percentuale.
3. **`register.empty_text`** — lo stato vuoto del § 9.6: una hairline, il glifo `#door-arch-steps` a
   48 px in `--ink-3`, la frase di `EMPTY_REGISTER` (che nomina già chi riempie la regione e quando),
   e l'azione inline. Nessun rettangolo tratteggiato decorativo.
4. **`.scroll-x` `role="region" tabindex="0"`** — **conservato su entrambe le tabelle**, con
   `aria-label` e un anello di focus visibile sulla regione. Misurato: in FR non scorre mai da 688 px
   in su (§ 10.4); resta perché a zoom 400 % o con un'etichetta araba lunga deve poter scorrere, e
   togliere una regione raggiungibile da tastiera sarebbe una regressione.
5. **«Registre complet»** e «Déposer un fichier hors exigence» (`.doc-page__aside`): una striscia
   `.cf-sheet--quiet` a fine pagina, due INLINE ACTION.
6. **Il banner del consenso** in fondo (`components/notice.html`, `kind="pending"`): resta. È detto
   una volta in fondo **e** su ogni riga che blocca, perché così lo ha deciso il presenter.

### 4.K «Tous les fichiers de votre compte» (MUST-FIX 13)

Le due sezioni `.doc-loose` — i file del conto e i documenti dell'organizzazione — **non restano con
la grammatica legacy**, e **non prendono una grammatica nuova**. Prendono **la stessa** grammatica di
tabella del registro, a una densità più bassa. Una grammatica sostituita, non aggiunta.

```
.cf-files   ←  stessa base .cf-register: table-layout: fixed, <col>, <caption>, scope,
               data-label, la fiche sotto 768, la .scroll-x
```
Differenze, e solo queste:

| | registro (`.cf-register`) | file (`.cf-files`) |
|---|---|---|
| superficie | `--min-2` (foglio, livello 2) | `--min-0` (tela, livello 0) — **è la retrocessione** |
| colonne | Élément 1fr / État 148 / Responsable 148 / Échéance 84 / Action 136 | Fichier 1fr / Type 148 / Taille 96 / Déposé le 120 |
| targa | sì (una pièce è un'esigenza) | **no** — un file non è un'esigenza |
| chip | sì | **no** — un file non ha uno stato di esigenza. Dove `antivirus` ha qualcosa da dire, la dice come **parola** con la sua regola, mai come chip di famiglia |
| nome | titolo in `--t-body` | nome in mono `--t-folio`, estensione in `--t-caption` |
| `content-visibility` | **no** | `auto` + `contain-intrinsic-size: auto 480px` |

`{% include "components/pagination.html" %}` resta dov'è. La sezione conserva il suo `<h2>` reale
(§ 6 (d)) al posto del `<p class="folio">` puntato da `aria-labelledby`.

### 4.L Mobile

Sotto 768: le cinque sezioni sono `<details>`, **aperte** solo quelle che chiedono un'azione, con lo
stato in `sessionStorage`; il rail 2.0 è un `<details>` la cui `<summary>` è la pastiglia «Étape 2 sur
7 — Compétences»; in basso `.cf-actionbar` (`position: sticky; inset-block-end: 0`, 64 px, `--min-3`,
`border-block-start: 1px solid var(--hairline-strong)`, **nessuna ombra**) porta **una sola** azione —
la stessa di «Prochaine étape» — e il conteggio.

**Misurato a 390 px** (§ 10.7), fascicolo con 7 pièces: banda 176 + pastiglia 44 + quattro `<details>`
chiusi a 57 + `<summary>` aperto 57 + registro in fiche 1 418 + action bar 64 = **1 930 px**, nessuno
scorrimento orizzontale, primo chip di stato a **y = 136**. Oggi: **5 552 px**, primo controllo utile
a y ≈ 724 su tablet. Obiettivo del round 1 (≤ 2 400) superato con 470 px di margine.

### 4.T I token — due valori nuovi, e nessun altro

Quattro famiglie. Il **colore** dice se una cosa è in corso, ti manca, è risolta o è rotta; **parola**
e **glifo** dicono dove sei nella pipeline. `--accent` non entra in tabella: è di link, CTA e focus
(l'unica eccezione è il segmento corrente del rail, che il § 9.3 prescrive).

Il round 1 aveva inventato dodici token, di cui due byte-identici a `--ok-100`/`--err-100`, uno
byte-identico a `--ink-3`, e due uguali ai colori che il § 1.5 criticava. Round 2: **si usano i token
che avevano già spedito**, e si introducono **due valori**, ciascuno perché una misura lo ha imposto.

```css
/* I DUE VALORI NUOVI */
--ok-800:      #1a6b44;  /* perché --ok-700 su --ok-100 misura 4,44 : 1 e non arriva a 4,5.
                            #1a6b44 = --ok-700 scurito sulla propria tinta: 5,42 : 1 su --ok-100,
                            6,23 : 1 su --min-2, 5,86 : 1 su --min-0, 5,45 : 1 su --min-1. */
--pending-100: #f2ead9;  /* perché la famiglia ocra non ha un fondo e --seal-100 è dei sigilli
                            (§ 1.3 regola 3). 1,15 : 1 contro --min-2 — esattamente la stessa
                            separazione che ha --ok-100 (1,15) e vicina a --err-100 (1,23).
                            --pending-700 ci sta sopra a 5,84 : 1. */
```

| Famiglia | Stati (§ 9.5 ↔ `RequirementState`) | fondo | testo | filetto 1 px | glifo |
|---|---|---|---|---|---|
| **NEUTRE «en cours»** | UPLOADING (transiente) · PROCESSING (`filed`) · UNDER REVIEW (`in_review`) | `--min-1` | `--ink` → **13,59 : 1** | `--hairline-strong` → **3,14** sul chip / **3,59** sul foglio | `#g-uploading` · `#g-processing` · `#g-review` |
| **OCRE «il vous manque»** | NEEDED (`missing`) · EXPIRING (`to_replace`) | `--pending-100` | `--pending-700` → **5,84 : 1** | `--pending-700` → **5,84** / **6,70** | `#g-needed` · `#g-expiring` |
| **VERT «résolu»** | VALID (`valid`) | `--ok-100` | `--ok-800` → **5,42 : 1** | `--ok-700` → **4,44** / **5,10** | `#g-valid` |
| **ROUGE «rompu»** | REJECTED (`invalid`) · EXPIRED (`expired`) | `--err-100` | `--err-700` → **5,10 : 1** | `--err-700` → **5,10** / **6,27** | `#g-rejected` · `#g-expired` |

**Otto parole del § 9.5, sette stati del dominio.** Il round 1 diceva «otto stati» e ne elencava due
che non esistono nel modello. La riconciliazione, per iscritto: `documents.models.RequirementState`
ha **sette** membri (`missing`, `filed`, `in_review`, `valid`, `invalid`, `expired`, `to_replace`);
UPLOADING è uno **stato transiente di client**, che vive solo finché un `XMLHttpRequest` è in volo e
non è mai persistito. La tabella qui sopra è la mappa completa.

**Geometria** — nessun colore:
```css
--cf-top: 56px; --cf-band-h: 176px; --cf-band-strip: 56px; --cf-rail-h: 64px;
--cf-margin-w: 264px;
--cf-col-state: 148px; --cf-col-owner: 148px; --cf-col-due: 84px; --cf-col-act: 136px;
--cf-cell-gap: 16px;   /* 12px sotto 1024 */
--cf-plate-w: 36px; --cf-plate-h: 46px;
```
Cancellati dal round 1: `--st-neutral-{bg,fg,line}`, `--st-pending-{bg,fg,line}`, `--st-ok-{bg,fg,line}`,
`--st-err-{bg,fg,line}`, `--cf-panel`, `--cf-track`, `--cf-drag`, `--cf-field-line`, `--cf-rail-w`,
`--cf-inspector-w`.

Tutti i rapporti sono ricalcolati in questo round con la luminanza relativa WCAG 2.x su un Chromium
mio (§ 10.8) e vanno fissati in `tests/frontend/test_v3_tokens.py`.

### 4.S Stati dei controlli

| Controllo | rest | hover | focus | active | disabled | loading | error |
|---|---|---|---|---|---|---|---|
| `.btn--primary` | `--accent`, testo `--min-0` (**5,69**), 48 px, r 2 | `--accent-hover` (**7,67**), 180 ms | anello 2 px `--accent-ring` (**3,70** su `--min-0`, **3,94** su `--min-2`, **3,44** su `--min-1`) + alone 3 px al 30 %, offset 2 px | `translate: 0 1px`, 120 ms | fondo `--min-1`, testo `--ink-3` (**5,14**) + la parola «indisponible» — **mai opacità sul testo** | `aria-busy="true"` + «Enregistrement…» + skeleton livello 1. **Nessuno spinner** (AR-2) | — |
| `.btn--secondary` | bordo `--hairline-strong`, testo `--ink` | fondo `--min-1` | idem | idem | idem | idem | — |
| `.cf-act` (INLINE ACTION) | mono 13 px `--accent` (**6,05** su `--min-2`, **5,29** su `--min-1`) + freccia | sottolineatura che si traccia | anello sull'`<a>`, ≥ 24 px | — | non esiste: l'azione indisponibile non è un link | — | — |
| `.cf-drop` | tratteggio iniziale `--hairline-strong` (**3,59**) | bordo `--ink-3` | anello sull'intera zona | — | `--min-1` + la frase che sblocca, **con il link** | — | famiglia rossa + `role="alert"` |
| `.cf-req` (riga) | hairline | fondo `--min-1`, 180 ms, solo `hover: hover` | anello sulla cella | — | — | skeleton livello 1, fermo | filetto iniziale 3 px `--err-700` (**6,27**) + la parola |
| campo | `--min-3`, bordo `--ink-3` (**5,88**), 48 px | bordo `--ink` | anello + bordo `--accent` | — | fondo `--min-1` | — | bordo `--err-700` + messaggio in `aria-describedby` |

### 4.F1 File e template

**Nuovi CSS** (`style-src 'self'`, nessun `<style>`, nessun `style=""`, nessun CDN):

- `static/css/v3/case-file.css` — banda, rail 2.0, fogli, registro, fiche, dropzone, action bar.
  Caricato **solo** su queste rotte via `{% block extra_head %}`.
- `static/css/v3/state.css` — `.st`, le quattro famiglie, **e la rimappatura legacy**. **Globale**,
  `@import` in `main.css` **dopo** `register.css` (MUST-FIX 4).
- `static/css/v3/upload.css` — coda, barra, verdetti. Solo su queste rotte.

**Sprite**: `static/img/v3/case-glyphs.svg` (§ 4.D).
**Entry point**: `static/js/src/case-file.js` (`scripts/build_frontend.mjs` prende già `src/*`).

**Template toccati** — solo markup e classi, **nessuna vista, nessun contratto dati, nessun campo POST
nuovo**: `cases/detail.html`, `portal/documents.html`, `documents/partials/register.html`,
`documents/requirement_detail.html`, `portal/partials/case_header.html`. Tutti dichiarano
`data-mode="dense"`.
**Nuove partial**: `cases/partials/{rail,transition_panel}.html`,
`documents/partials/{dropzone,state_chip,register_legend}.html`.

```django
{# documents/partials/state_chip.html — una sola forma, usata da tutte e quattro le superfici #}
<span class="st st--{{ state }}">
  <svg class="st__glyph" width="16" height="16" aria-hidden="true" focusable="false"><use href="{% static 'img/v3/case-glyphs.svg' %}#g-{{ glyph }}"></use></svg>{{ label }}</span>
```
```django
{# la riga du registre #}
<tr class="cf-req{% if row.is_overdue %} cf-req--overdue{% endif %}">
  <th scope="row" data-label="{% translate 'Élément' %}">
    <span class="cf-req__head">
      <svg class="cf-plate" width="36" height="46" aria-hidden="true" focusable="false">
        <use href="{% static 'img/v3/case-glyphs.svg' %}#plate-{{ row.code|default:'other' }}"></use>
        {% if row.current.is_current %}<use href="{% static 'img/v3/case-glyphs.svg' %}#plate-fold-sealed"></use>{% endif %}
      </svg>
      <span class="cf-req__body">
        <a class="cf-req__title" href="{{ row.detail_url }}">{{ row.title }}</a>
        {% if row.source_ref %}<span class="cf-req__source t-ref">{{ row.source_ref }}</span>{% endif %}
        <span class="cf-req__tags">
          {% if not row.mandatory %}<span class="cf-req__tag">{% translate "Facultative" %}</span>{% endif %}
          {% if row.is_overdue %}<span class="cf-req__tag cf-req__tag--late">{% translate "En retard" %}</span>{% endif %}
          {% if row.current %}<span class="cf-req__tag t-ref">{% blocktranslate with n=row.version_count %}version {{ n }}{% endblocktranslate %}</span>{% endif %}
        </span>
        {% if row.state_reason %}<span class="cf-req__reason">{{ row.state_reason }}</span>{% endif %}
      </span>
    </span>
  </th>
  <td data-label="{% translate 'État' %}">{% include "documents/partials/state_chip.html" with state=row.state_css glyph=row.state_css label=row.state_label %}</td>
  <td data-label="{% translate 'Responsable' %}">{{ row.responsible }}{% if row.responsible_note %}<span class="cf-req__note">{{ row.responsible_note }}</span>{% endif %}</td>
  <td data-label="{% translate 'Échéance' %}">{% if row.due_date %}<time datetime="{{ row.due_date|date:'c' }}">{{ row.due_date|date:"d.m.Y" }}</time>{% else %}—{% endif %}</td>
  <td data-label="{% translate 'Action' %}">{# § 4.E #}</td>
</tr>
```

---

## 5. MOTION — voci per `MOTION_SYSTEM.md` § 6

Tutte in Motion 13.4.1 via `static/js/src/motion.js`, dentro `withMotion(fn, settle)`. Proprietà
ammesse: `transform`, `opacity`, e `background-color` **solo** in hover, che il § 2 riga HOVER
autorizza per nome («`transform` ≤ 2 px, **colore**, ombra di ruolo» — la terza non la prendo).
Ogni voce dichiara **la famiglia del § 2** e **la funzione di quella famiglia**, così le due non
possono divergere: era il difetto di `cf-row-settle`.

**Su DENSE non esiste**: nessun reveal `inView` (§ 7), nessun oggetto indicizzato allo scroll (§ 4),
nessun loop ambientale (§ 4), nessuno spinner (AR-2). La banda non è in questa tabella perché **non
anima**: è `position: sticky`.

| Nome | Famiglia § 2 | Funzione | Innesco | Durata | Curva | Proprietà | Stato ridotto | Budget |
|---|---|---|---|---|---|---|---|---|
| `cf-state-commit` | DATI | **stato** | al ricaricamento dopo la POST: `case-file.js` ha messo l'id della riga in `sessionStorage` al submit, lo legge, anima **quella** riga una volta e lo cancella | `--motion-base` 240 | `--ease-standard` | il vecchio chip `opacity 1→0` + `translateY 0→-6`, il nuovo `opacity 0→1` + `translateY 6→0`; i due condividono **una** `grid-area` | testo già al valore finale; `aria-live="polite"` annuncia comunque | 0 layout: una sola `grid-area`, nessun reflow di cella |
| `cf-row-settle` | LAYOUT | **causalità** | inserimento / rimozione di una riga | `SPRING_SETTLE` (260/30) | — | `height` misurata via `animate`, poi `transform` sui fratelli | salto immediato | mai su liste > 25 righe |
| `cf-details-open` | LAYOUT | **causalità** | `toggle` di un `<details>` | `SPRING_SETTLE` | — | altezza misurata → `scaleY` del contenitore + `opacity` del contenuto | apertura istantanea | una sola sezione per volta |
| `cf-upload-progress` | DATI | **stato** | `XMLHttpRequest.upload.onprogress` | `--motion-base` 240 | `--ease-standard` | `transform: scaleX(0→n)`, `transform-origin: left` (`right` in RTL) | barra assente; la riga aggiorna «1,4 Mo sur 12 Mo» in testo | **mai `width`**; un elemento per riga; rimossa a fine corsa |
| `cf-upload-verdict` | USCITA | **orientamento** | fine della richiesta | `--motion-fast` 180 | `--ease-in` | barra `opacity 1→0` + `scaleY 1→0`; il chip finale passa da `visibility: hidden` a visibile | barra rimossa, chip già presente | il chip finale è nel DOM da subito |
| `cf-drop-arm` | HOVER | **feedback** | `dragenter`/`dragleave` con **contatore di profondità** | in `--motion-fast` / out `--motion-instant` | out / in | `opacity` dello strato `--accent-wash` (pseudo-elemento già composto) | il fondo cambia senza transizione | 0 layout |
| `cf-press` | HOVER | **feedback** | pressione su `.btn` / `.cf-act` / `<summary>` | `--motion-instant` 120 | `--ease-in` | `translate: 0 1px` | identico (§ 2: l'hover non è moto essenziale) | 0 layout |
| `cf-row-hover` | HOVER | **feedback** | puntatore su una riga, solo `hover: hover` | `--motion-fast` 180 | `--ease-out` | `background-color` → `--min-1` | identico | **una** repaint, confinata al rettangolo della riga. È l'unica paint ammessa dopo il primo frame, ed è quella che il § 9.4 chiede |
| `cf-skeleton` | — | **nessuna: non anima** | attesa > 300 ms | — | — | nessuna. Blocchi fermi di livello 1 (`--min-1`), `aria-busy="true"` sul contenitore, annuncio `aria-live="polite"` a fine caricamento (§ 9.6) | identico | è in tabella perché il catalogo deve dire anche ciò che **non** si muove |

**`SPRING_SETTLE` non esiste ancora** (MUST-FIX/Lacuna 9): `static/js/src/motion.js` ri-esporta
`spring` ma non definisce le due molle del § 1. Da aggiungere lì, non in `case-file.js`, perché il
§ 1 dice che i token vivono in `tokens.css` **e** in `motion.js` «come un solo insieme»:

```js
// static/js/src/motion.js
export const SPRING_SETTLE = { stiffness: 260, damping: 30 };  // MOTION_SYSTEM § 1
export const SPRING_FOLLOW = { stiffness: 400, damping: 40 };
```

**Ogni `transition` e ogni `@keyframes` sta dentro `@media (prefers-reduced-motion: no-preference)`**
(§ 3). Fuori da quel blocco il valore è quello finale. In `case-file.css` c'è **un solo** blocco
`no-preference`, alla fine del file, e `grep -c "@keyframes" static/css/v3/*.css` deve dare **0**:
su questa superficie non c'è nessuna animazione CSS, solo transizioni.

**Ciò che non si anima, per regola**: nessun conteggio che «scorre» (i numeri qui sono verificabili,
non decorativi); nessun reveal sul testo prescritto della pré-évaluation né sulla nota del registro
né su un motivo di rifiuto; nessuna pulsazione su un chip; nessun moto su una riga che il lettore non
ha toccato; nessun moto sulla banda.

---

## 6. ACCESSIBILITÀ E RTL

**Risolto qui** — (a) i due campi a 1,13 : 1 spariscono col box navy; (b) il `<select>` 125 × 22
diventa un form a pagina con controlli a 48 px dentro un `<summary>` da 44 px: **2.5.8 passa senza
JavaScript**; (c) i chip passano da 16 px a **26 px misurati** (2 px di padding + 20 px di interlinea
+ 2 × 1 px di filetto), sopra i 24 px di 2.5.8, e a **44 × 44** su `pointer: coarse` via `::after` —
verificato in un contesto touch che il pseudo-elemento si posiziona sul chip perché `.st` porta
`position: relative` (§ 10.5); (d) `documents.html` acquisisce `<h2>` reali al posto dei
`<p class="folio">` puntati da `aria-labelledby`; (e) ogni stato è **fondo + filetto + glifo +
parola**: quattro codifiche, il colore non è mai solo.

**Da rispettare** — `role="alert"` (non `status`) sul rifiuto di un deposito; `aria-live="polite"` +
`aria-busy` sulla coda; `aria-current="step"` sulla tappa corrente; segmenti del rail focalizzabili
con Enter (§ 9.3); `.scroll-x` con `role="region"`, `tabindex="0"`, `aria-label` e anello di focus
visibile; `scroll-padding-block-start: calc(var(--cf-top) + var(--cf-band-strip) + var(--cf-rail-h))`
sul `:root`, perché con tre elementi appiccicosi in testa un ancoraggio da tastiera finirebbe sotto
di loro (§ 2, livello 4).

**`prefers-reduced-motion` è uno stato completo**: la banda è già compatta o estesa esattamente come
nell'altro stato (non anima mai), le barre di progresso saltano al valore col testo dei byte al loro
posto, i `<details>` aprono d'un colpo, i chip si sostituiscono senza transizione, **nulla resta a
`opacity: 0`**, nessun contenuto manca. La preferenza si legge dal vivo (`matchMedia` a ogni
chiamata, § 3).

**`forced-colors: active`** — misurato su un contesto `forced_colors="active"` (§ 10.5): il chip
diventa `Canvas` / `CanvasText` / bordo `CanvasText`, cioè **le quattro famiglie diventano
indistinguibili per colore**. È il caso previsto: restano il **glifo** e la **parola**, che sono la
prima e la seconda codifica. In più: filetti a `CanvasText`, `forced-color-adjust: none` **solo** sui
segmenti del rail (con quattro `border-style` diversi per i cinque attori, § 4.C), banda territoriale
nascosta, targhe conservate perché disegnate in `currentColor`.

**RTL** — solo proprietà logiche. **Si specchiano**: il verso del rail, il glifo di frontiera, la
freccia dell'INLINE ACTION, la banda territoriale, la piega della targa (è un angolo *iniziale*, e
`transform: scaleX(-1)` sullo `<use>` la porta dall'altra parte). **Non si specchiano**: numeri,
misuratore, date, riferimenti di pratica, il lock-up. **La barra di progresso non si risolve da
sola**: `transform-origin: left` + `[dir="rtl"] .cf-drop__fill { transform-origin: right }` — la
frase del round 1 che diceva il contrario è cancellata. `:lang(ar)` — famiglie compagne,
`letter-spacing: 0` su ogni etichetta, interlinea 1,8 nel corpo; **nessun `text-transform: none` sul
chip**, perché il chip non è più maiuscolo in nessuna lingua. Misurato in AR a 1440 e a 390: **0
celle in overflow, nessuno scorrimento orizzontale** (§ 10.4).

**HUMAN_QA_REQUIRED** — (1) NVDA e VoiceOver sulla sequenza «riga → chip → legenda → azione», FR e AR;
(2) un deposito reale con rete strozzata, per verificare che i byte annunciati siano quelli e che
«Réessayer» compaia; (3) la striscia appiccicosa su iOS Safari con la barra degli indirizzi che si
ritrae — `position: sticky` sotto una barra anch'essa sticky è l'unico punto dove il calcolo di
`--cf-top` può scostarsi; (4) zoom 400 % a 320 px, dove la `.scroll-x` entra davvero in funzione;
(5) con un account terzo, che nessun link di download compaia dove `delivery_block` non è vuoto;
(6) Windows alto contrasto sul rail a cinque trame.

---

## 7. PRESTAZIONI

**CSS** — tetti, non stime, da far fallire in `tests/frontend/test_v3_assets.py`: `case-file.css`
**≤ 9 KB gzip**, `upload.css` **≤ 2 KB gzip**, entrambi caricati **solo** su queste rotte;
`state.css` **≤ 2 KB gzip**, **globale**. L'unico risparmio rivendicato è reale e verificabile:
`apps/documents/static/documents/documents.css` righe **91-160** duplicano il pop-in che
`apps/portal/static/portal/portal.css` righe **379-420** fornisce già a ogni tabella con `data-label`;
quelle righe si tolgono. **Il risparmio su `register.css` è ritirato** (MUST-FIX 4): non si tocca.

**JS — la somma del round 1 era sbagliata, il revisore ha ragione, ecco i miei numeri.** Misurati con
`gzip -9` sui file di `static/js/` il 24 settembre 2026 (§ 10.9):

| file | gzip | perché è sulla pagina |
|---|---:|---|
| `js/head.js` | 206 B | `base.html` |
| `js/main.js` | 5 293 B | `base.html` |
| `js/dist/shell.js` | 613 B | guscio della piattaforma |
| `js/dist/chunks/chunk-P4EHGXV4.js` | 26 120 B | **importato staticamente** dalla prima istruzione di `shell.js` — è Motion, ed è già pagato |
| **oggi, sulla pagina** | **32 232 B** | = 31,48 KB |
| `js/dist/case-file.js` (tetto) | **≤ 4 600 B** | XHR del deposito, molla dei `<details>`, scambio del chip, contatore di profondità del drag, memoria dei `<details>` in `sessionStorage` |
| **totale** | **≤ 36 832 B** | **35,97 KB su 45** — margine **9 248 B ≈ 9,03 KB** |

Il round 1 diceva «≈ 31 KB su 45» e ometteva `head.js` e `main.js`. Il margine reale non è 14 KB: è
**9,03 KB**, ed è contro quello che va giudicata ogni aggiunta futura. Il tetto di `case-file.js` è
sceso da 5,2 a 4,6 KB perché il round 2 elimina il codice di `scroll()`, di `inView`, dello skeleton
animato, del drawer e del `<dialog>`.

**Niente React**: il pannello è un `<details>`, il collasso è un `<details>`, il progresso è
`XMLHttpRequest`, la compressione della banda è `position: sticky`. Nessuna isola React è
giustificata qui, e lo metto per iscritto.

**Immagini** — **nessun raster su questa superficie**: 0 KB sui 120 ammessi per viewport. Un solo
`case-glyphs.svg` ≤ 4 096 byte grezzi / ≤ 1 600 gzip, un request, riusato con `<use>`.

**Paint e layout** — si animano solo `transform` e `opacity`, più `background-color` sull'hover di
una riga (§ 5). La barra usa `scaleX`, mai `width`: un deposito da 12 MB produce **0 layout**.
Nessun elemento è promosso: **non c'è `will-change` su questa pagina**, perché non c'è niente da
promuovere — la banda non si muove, scorre la pagina sotto di essa. `content-visibility: auto`
**solo** su `.cf-files` e `.cf-versions`, sempre con `contain-intrinsic-size: auto 480px`; **non** sul
registro, perché nascondere al layout la cosa per cui il lettore è venuto per risparmiare paint è un
cattivo affare e farebbe sobbalzare la barra di scorrimento sotto tre elementi appiccicosi. Nessun
`filter`, nessuna ombra, nessuna ombra animata, nessun loop.

**Obiettivi misurabili** (§ 10): altezza a 390 px **da 5 552 a 1 930 px** (misurato); primo chip di
stato a 390 px a **y = 136**; primo controllo utile a 768 px **da y ≈ 724 a y ≤ 420**; 0 celle in
overflow a 688/944/1096/1240 in FR e AR; INP < 200 ms su `toggle` del pannello di transizione e su
`dragenter`.

---

## 8. RISCHI

1. **La striscia appiccicosa mangia il viewport su un telefono corto.** Barra 56 + striscia 56 =
   112 px fissi su 844 di altezza a 390 — il 13 %. Guardia: sotto 768 la banda **non** è appiccicosa
   (solo la `.cf-actionbar` lo è, 64 px), e la pastiglia del rail sta nel flusso. Il costo fisso a
   390 è quindi 64 px, non 112. Da verificare a mano su iOS Safari (HUMAN_QA 3).
2. **Quattro famiglie lette come quattro semafori.** Guardia: la parola è la prima codifica, il glifo
   la seconda, il filetto la terza; il test rifiuta qualunque `.st` senza testo; nessuno stato dice
   «approuvé», e la legenda del registro porta la regola di ogni parola presente in pagina.
3. **Il progresso che mente.** Una barra al 100 % ferma mentre l'antivirus lavora è la bugia classica.
   Guardia: UPLOADING finisce a byte completati e **cede il posto** a PROCESSING, indeterminato per
   costruzione e dichiarato a parole; nessuna interpolazione inventata fra i due.
4. **Il registro senza inspector legge come una lista lunga (AR-3).** Guardia: il contenuto del § 9.7
   è il **primo** foglio, non l'ultimo; la striscia porta lo stato e la prossima azione a ogni scroll;
   un test confronta la sequenza del testo a 1600 e a 390 e la vuole identica.
5. **Il link che risponde 403.** Già impossibile lato presenter e impossibile lato markup, perché
   nessun ramo disegna un `<a>` senza `download_url`. Il test di consegna deve fallire se un `<a>`
   punta a `documents:signed_download` con `delivery_block` non vuoto.
6. **Il rail a cinque trame illeggibile in stampa o in forced-colors.** Guardia: la trama è la terza
   codifica dopo parola e numero, `forced-color-adjust: none` **solo** sui segmenti, quattro
   `border-style` distinti in forced-colors, legenda testuale obbligatoria nell'anatomia.
7. **`state.css` globale cambia colore a 28 template.** È il prezzo di MUST-FIX 4 ed è voluto: la
   rimappatura tocca **solo** la proprietà `color` degli otto modificatori `.state--*`, mai la
   geometria, così Academy, Forum, Helpdesk, Companies, Selection e il cruscotto cambiano tinta e non
   forma. Guardia: un test di regressione visiva sui sei template rappresentativi elencati nella
   revisione.
8. **Il `<details>` come unico contenitore del cambio di stato è saltabile da tastiera in fretta.**
   Guardia: `<summary>` a 44 px con anello di focus, `aria-expanded` gestito nativamente, e la frase
   «État actuel : …» dentro il pannello, così chi lo apre legge sempre da dove parte.

---

## 9. IL CSS, PER ESTESO

Quanto basta perché nessuno debba chiedermi niente. Ogni valore qui è nel § 10.

### 9.1 Token (in testa a `case-file.css`)

```css
:root {
  --ok-800: #1a6b44;
  --pending-100: #f2ead9;
  --cf-top: 56px;
  --cf-band-h: 176px;
  --cf-band-strip: 56px;
  --cf-rail-h: 64px;
  --cf-margin-w: 264px;
  --cf-col-state: 148px;
  --cf-col-owner: 148px;
  --cf-col-due: 84px;
  --cf-col-act: 136px;
  --cf-cell-gap: var(--s-4);
  --cf-plate-w: 36px;
  --cf-plate-h: 46px;
  scroll-padding-block-start: calc(var(--cf-top) + var(--cf-band-strip) + var(--cf-rail-h));
}
@media (max-width: 63.99rem) { :root { --cf-cell-gap: var(--s-3); } }
```

### 9.2 Banda, rail, spazio di lavoro

```css
.cf-band {
  position: sticky;
  inset-block-start: calc(var(--cf-top) + var(--cf-band-strip) - var(--cf-band-h));
  z-index: 3;
  display: grid;
  grid-template-rows: minmax(0, 1fr) var(--cf-band-strip);
  block-size: var(--cf-band-h);
  background: var(--mid-2);
  color: var(--on-dark);
  border-radius: 0;
}
.cf-band__tall  { padding: var(--s-5) var(--grid-margin) 0; min-block-size: 0; overflow: hidden; }
.cf-band__strip {
  display: flex; align-items: center; gap: var(--s-6);
  padding-inline: var(--grid-margin);
  border-block-start: 1px solid var(--hairline-dark-strong);
}
.cf-band__ref { font-family: var(--f-mono); font-size: var(--t-folio); letter-spacing: var(--track-folio);
                color: var(--accent-dark); font-variant-numeric: tabular-nums; }

.cf-rail {
  position: sticky;
  inset-block-start: calc(var(--cf-top) + var(--cf-band-strip));
  z-index: 2;
  min-block-size: var(--cf-rail-h);
  background: var(--min-1);
  border-block-end: 1px solid var(--hairline);
}
.cf-rail__list { display: grid; grid-auto-flow: column; grid-auto-columns: 1fr;
                 gap: var(--s-2); margin: 0; padding: 0; list-style: none; }
.cf-rail__hit  { display: grid; gap: 2px; min-block-size: 44px; padding: var(--s-2);
                 color: var(--ink); text-decoration: none; }
.cf-rail__step.is-current .cf-rail__hit { border: 2px solid var(--accent); }   /* § 9.3, prescritto */
.cf-rail__state { font-size: var(--t-caption); color: var(--ink-3); }
.cf-rail__legend { font-size: var(--t-caption); color: var(--ink-3); padding: var(--s-2) var(--grid-margin); margin: 0; }

@media (max-width: 63.99rem) {                     /* § 9.3 : verticale sotto 1024 */
  .cf-rail { position: static; }
  .cf-rail__list { grid-auto-flow: row; grid-auto-columns: auto; }
}
@media (min-width: 64rem) {
  .portal { grid-template-columns: 224px minmax(0, 1fr); }        /* § 9.1, invariato */
  .portal__aside { position: sticky;
    inset-block-start: calc(var(--cf-top) + var(--cf-band-strip) + var(--cf-rail-h) + var(--s-4)); }
}
@media (max-width: 47.99rem) {
  .cf-band { position: static; }                   /* rischio 1 */
  .cf-actionbar { position: sticky; inset-block-end: 0; block-size: 64px;
    background: var(--min-3); border-block-start: 1px solid var(--hairline-strong);
    display: flex; align-items: center; gap: var(--s-3); padding-inline: var(--grid-margin); }
}
```

### 9.3 Il registro

```css
.cf-register { inline-size: 100%; border-collapse: collapse; table-layout: fixed; }
.cf-register caption { position: absolute; inline-size: 1px; block-size: 1px;
                       overflow: hidden; clip-path: inset(50%); }
.cf-register th, .cf-register td {
  text-align: start; vertical-align: top;
  padding-block: 14px; padding-inline: 0 var(--cf-cell-gap);
  border-block-end: 1px solid var(--hairline);
}
.cf-register thead th {
  font-family: var(--f-mono); font-size: var(--t-folio); line-height: var(--t-folio-lh);
  letter-spacing: var(--track-folio); text-transform: uppercase; color: var(--ink-3);
  padding-block: var(--s-2); border-block-end: 1px solid var(--hairline-strong);
}
.cf-register td, .cf-register time { font-variant-numeric: tabular-nums; }
.cf-req__head  { display: grid; grid-template-columns: var(--cf-plate-w) minmax(0, 1fr); gap: var(--s-3); }
.cf-plate      { inline-size: var(--cf-plate-w); block-size: var(--cf-plate-h); color: var(--ink-3); }
.cf-req--acting .cf-plate { color: var(--ink); }
.cf-req__title { font-size: var(--t-body); line-height: 1.5rem; font-weight: 500; color: var(--ink); }
.cf-req__source, .cf-req__tag { font-size: var(--t-caption); line-height: var(--t-caption-lh); color: var(--ink-3); }
.cf-req__tag--late { color: var(--err-700); }
.cf-req__reason, .cf-req__note { display: block; font-size: var(--t-caption);
                                 line-height: var(--t-caption-lh); color: var(--ink-3); }
.cf-req--overdue { border-inline-start: 3px solid var(--err-700); }
.cf-act { font-family: var(--f-mono); font-size: var(--t-folio); line-height: 1.25rem;
          letter-spacing: var(--track-folio); color: var(--accent);
          display: inline-block; min-block-size: 24px; }
.cf-deny { display: flex; gap: var(--s-2); font-size: var(--t-caption); color: var(--ink-3); margin: 0; }
.scroll-x:focus-visible { outline: 2px solid var(--accent-ring); outline-offset: 2px; }

.cf-files { /* stesse regole, superficie e colonne del § 4.K */
  background: var(--min-0);
  content-visibility: auto;
  contain-intrinsic-size: auto 480px;
}
```

### 9.4 `state.css` — globale

```css
/* ---- il chip nuovo -------------------------------------------------------- */
.st {
  display: inline-flex; align-items: center; gap: 6px;
  min-block-size: 24px; padding-block: 2px; padding-inline: 10px 12px;
  border: 1px solid; border-radius: 999px;                 /* § 2 : 999 sulle pillole di stato */
  font-family: var(--f-sans);
  font-size: var(--t-small); line-height: var(--t-small-lh);   /* 14 / 20 */
  font-weight: 500; letter-spacing: 0; text-transform: none;   /* § 3.2 : niente maiuscolo qui */
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
  position: relative;                                      /* il ::after qui sotto ne ha bisogno */
}
.st__glyph { inline-size: 16px; block-size: 16px; flex: none; }

:is(.st--filed, .st--review, .st--uploading) {
  background: var(--min-1);       color: var(--ink);         border-color: var(--hairline-strong); }
:is(.st--missing, .st--replace) {
  background: var(--pending-100); color: var(--pending-700); border-color: var(--pending-700); }
.st--valid {
  background: var(--ok-100);      color: var(--ok-800);      border-color: var(--ok-700); }
:is(.st--invalid, .st--expired) {
  background: var(--err-100);     color: var(--err-700);     border-color: var(--err-700); }

@media (pointer: coarse) {
  .st--action::after {
    content: ""; position: absolute;
    inset-block-start: 50%; inset-inline-start: 50%; translate: -50% -50%;
    min-inline-size: 44px; min-block-size: 44px;
  }
}

/* ---- la rimappatura legacy : COLORE soltanto (MUST-FIX 4) ------------------
   `.state` resta in register.css con la sua geometria (13 px, 600, maiuscolo,
   filetto iniziale 2 px). Qui cambia solo la tinta, così i 28 template che la
   usano parlano il vocabolario nuovo senza cambiare forma.
   Rapporti su --min-0 : pending 6,29 · ink-2 6,46 · ok-800 5,86 · err-700 5,89. */
:is(.state--missing, .state--replace) { color: var(--pending-700); }
:is(.state--filed, .state--review)    { color: var(--ink-2); }
:is(.state--valid, .state--done)      { color: var(--ok-800); }
:is(.state--invalid, .state--expired) { color: var(--err-700); }
```

### 9.5 Il blocco del moto — uno solo, a fine file

```css
@media (prefers-reduced-motion: no-preference) {
  .cf-drop__fill      { transition: transform var(--motion-base) var(--ease-standard); }
  .cf-drop::before    { transition: opacity var(--motion-fast) var(--ease-out); }
  .cf-drop:not(.is-armed)::before { transition-duration: var(--motion-instant);
                                    transition-timing-function: var(--ease-in); }
  .btn:active, .cf-act:active, summary:active { transition: translate var(--motion-instant) var(--ease-in); }
  @media (hover: hover) {
    .cf-req:hover { transition: background-color var(--motion-fast) var(--ease-out); }
  }
}
.btn:active, .cf-act:active, summary:active { translate: 0 1px; }
@media (hover: hover) { .cf-req:hover { background: var(--min-1); } }
```
`grep -c "@keyframes" static/css/v3/case-file.css` → **0**.
`grep -c "box-shadow" static/css/v3/*.css` → **0**.
`grep -c "cubic-bezier" static/css/v3/*.css` → **0** (le tre curve sono token di `v2/tokens.css`).

---

## 10. REGISTRO DELLE MISURE

Tutto misurato da me in questo round, su un Chromium di Playwright headless lanciato da
`.venv/Scripts/python.exe`, contro `http://127.0.0.1:8771`, con `static/css/v2/tokens.css` e
`static/css/fonts.css` serviti dallo stesso origin (così i font sono quelli veri). Script:
`…/claude/cf3/m1.py … m11.py`.

**10.1 Supporto CSS** (`m1.py`).
`CSS.supports('transform-origin','inline-start')` → **false**; `transformOrigin` calcolato su un
blocco a piena larghezza a viewport 1440 → **`712px 9px`**, cioè il centro. `'left'` → **true**,
calcolato `0px 9px`.
`CSS.supports('background-image','linear-gradient(to inline-end, #000, #fff)')` → **false** — il
rimedio a una riga proposto dalla revisione non è disponibile.
`content-visibility: auto` **true** · `contain-intrinsic-size: auto 400px` **true** ·
`position: sticky` **true** · `animation-timeline: scroll()` **true** (non usato) · `color-mix` **true**.

**10.2 Contenitore del sito vivo** (`m2.py`, su `/fr/`, larghezza **interna**, margini esclusi):
390 → n/d · **768 → 688** · **1024 → 944** · **1280 → 1096** · **1440 → 1240** · **1600 e 1920 → 1360**.
`--grid-gutter` 24 (12 sotto 430), `--grid-margin` 40 (20 sotto 430), `--chrome-masthead` 72.

**10.3 Geometria della banda appiccicosa** (`m10.py`, viewport 1440, `--cf-top: 56`):

| scrollY | alto della banda | basso della banda | striscia | rail | gap banda↔rail | parte alta visibile |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 56 | 232 | 176 → 232 | 232 | **0** | 120 |
| 30 | 26 | 202 | 146 → 202 | 202 | **0** | 90 |
| 60 | −4 | 172 | 116 → 172 | 172 | **0** | 60 |
| 90 | −34 | 142 | 86 → 142 | 142 | **0** | 30 |
| 119 | −63 | 113 | 57 → 113 | 113 | **0** | 1 |
| 120 … 2500 | −64 | 112 | **56 → 112** | 112 | **0** | **0** |

La striscia è interamente visibile sotto la barra a ogni y. Nessuna animazione, nessun listener.

**10.4 Tenuta delle colonne** (`m3/m5/m6/m7.py`). Piano adottato:
`Élément 1fr / État 148 / Responsable 148 / Échéance 84 / Action 136`, `padding-inline-end` 16 px
(12 px sotto 1024), `table-layout: fixed`, contenuti reali (FR: «Identifier les interlocuteurs et les
autorités compétentes», «Le professionnel mandaté», «Sportello Unico di Milano» ; AR: «تحديد الجهات
والسلطات المختصة في الملف», «المهني المكلَّف»).

| larghezza tabella | Élément | celle in overflow | scroll orizzontale |
|---:|---:|---:|---|
| 688 (viewport 768) | 172 | **0** | no |
| 944 (viewport 1024) | 428 | **0** | no |
| 1096 (viewport 1280) | 580 | **0** | no |
| 1240 (viewport 1440) | 724 | **0** | no |
| 1240, `dir="rtl"`, AR | 644 | **0** | no |

Piani scartati, con la ragione: `1fr/176/184/104/168` → colonna Élément a 16 px a 648 e 5 celle in
overflow a 688 ; `1fr/160/160/92/152` → 5 celle in overflow fino a 720. Il costo dell'inspector:
**a 648 px di workspace la colonna Élément scende a 16-112 px**, contro i **157 px** che il titolo più
lungo richiede — è la misura che sostiene AR-3.

**10.5 Il chip** (`m5/m6.py`, Fira Sans 500 a 14/20, glifo 16, padding 2/10/2/12, filetto 1 px).
Altezza **26,00 px** (≥ 24 di 2.5.8). Larghezze FR: «Valide» 85,00 · «Manquant» 110,22 · «Non valide»
113,67 · «En examen» 114,61 · **«À remplacer» 122,02** (la più larga; la colonna ne offre 136).
AR: «ناقص» 78,25 · «صالحة» 82,28 · «قيد الفحص» 109,34.
Contesto touch (`has_touch`, `is_mobile`): `matchMedia('(pointer: coarse)')` **true**,
`.st--action` calcolato `position: relative`, `::after` `content: ""` con `min-inline-size` e
`min-block-size` **44px** — il bersaglio si misura **sul chip**.
`forced_colors="active"`: chip `background rgb(255,255,255)`, `color rgb(0,0,0)`, bordo `rgb(0,0,0)`.

**10.6 `.state` nei template.** `grep -rln 'class="state' templates/ apps/*/templates/` →
**28 file** (academy 3, cases 2, companies 4, documents 2, forum/governance 7, helpdesk 3, portal 2,
selection 4, + `portal/partials/case_header.html` compreso nei 2 di portal). `static/css/main.css`
importa `register.css` globalmente: un foglio caricato per rotta non può sostituirlo. MUST-FIX 4
confermato e accettato.

**10.7 Altezza mobile** (`m7/m9.py`, viewport 390 × 844, 7 pièces).
Pop-in generico (cinque coppie impilate): riga **292–314 px**, registro **2 110 px**, pagina intera
**2 679 px** → **manca il bersaglio**.
Fiche a due colonne (§ 4.E1): riga **183–205 px**, registro **1 418 px**, pagina intera **1 930 px**,
banda 176, pastiglia 44, `<details>` chiusi 57 ciascuno, action bar 64, **nessuno scorrimento
orizzontale**, primo chip a **y = 136**.

**10.8 Rapporti di contrasto** (`m1/m4/m11.py`, luminanza relativa WCAG 2.x, ogni valore letto da
`getComputedStyle` su `v2/tokens.css`, non trascritto a mano).

| coppia | rapporto |
|---|---:|
| `--on-dark` / `--mid-2` | **14,08** |
| `--on-dark-2` / `--mid-2` | **8,79** |
| `--on-dark-3` / `--mid-2` | **5,85** |
| `--accent-dark` / `--mid-2` | **9,09** |
| `--terr-line` / `--mid-2` | **5,51** |
| `--seal-300` / `--mid-2` | **7,00** |
| `--hairline-dark-strong` compositato su `--mid-2` | **rgb(74, 89, 97)** → **2,19** |
| `--accent-dark` / `--on-dark-3` (piena vs vuota) | **1,56** |
| `--ink` / `--min-2` · `--min-1` | **15,56** · **13,59** |
| `--ink-3` / `--min-2` · `--min-1` | **5,88** · **5,14** |
| `--accent` / `--min-2` · `--min-1` · `--min-0` | **6,05** · **5,29** · **5,69** |
| `--min-0` / `--accent` · `--accent-hover` | **5,69** · **7,67** |
| `--accent-ring` / `--min-0` · `--min-1` · `--min-2` | **3,70** · **3,44** · **3,94** |
| `--hairline-strong` / `--min-1` · `--min-2` | **3,14** · **3,59** |
| `--hairline` / `--min-2` | **1,45** |
| `--accent-wash` / `--min-2` ; `--accent` / `--accent-wash` ; `--ink` / `--accent-wash` | **1,15** ; **5,24** ; **13,48** |
| `--accent` / `--hairline` (riempimento vs traccia) | **4,17** |
| `--ok-700` / `--ok-100` | **4,44** ← *sotto 4,5 : è la misura che impone `--ok-800`* |
| `--ok-800` / `--ok-100` · `--min-2` · `--min-1` · `--min-0` | **5,42** · **6,23** · **5,45** · **5,86** |
| `--err-700` / `--err-100` · `--min-2` · `--min-0` | **5,10** · **6,27** · **5,89** |
| `--pending-700` / `--pending-100` · `--min-2` · `--min-0` | **5,84** · **6,70** · **6,29** |
| `--pending-100` / `--min-2` ; `--ok-100` / `--min-2` ; `--err-100` / `--min-2` ; `--min-1` / `--min-2` | **1,15** ; **1,15** ; **1,23** ; **1,14** |
| `--seal-600` / `--min-2` | **4,57** |
| `--ink-2` / `--min-0` | **6,46** |
| `--owner-*` / `--min-1` (person · project · training · authority · territory) | **5,29** · **7,03** · **5,91** · **3,99** · **5,21** |

**10.9 Peso del JavaScript** (`gzip -9`, 24 settembre 2026, `wc -c`).
`static/js/head.js` 233 → **206** · `static/js/main.js` 19 944 → **5 293** ·
`static/js/dist/shell.js` 1 136 → **613** · `static/js/dist/chunks/chunk-P4EHGXV4.js` 70 441 →
**26 120** · `static/js/dist/motion.js` 242 → **189**.
La prima istruzione di `dist/shell.js` è `import{…}from"./chunks/chunk-P4EHGXV4.js"`: il chunk di
Motion è sulla pagina perché il guscio lo importa staticamente. Totale odierno **32 232 B**. La
revisione dava `main.js` a 5 309 B; io misuro **5 293 B** con `gzip -9` — 16 byte di differenza, che
è il livello di compressione, non una discordanza di sostanza.
