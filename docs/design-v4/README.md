# DESIGN V4 — freeze, checkpoint, ordine

Stato: **DESIGN FREEZE in vigore dal 24 settembre 2026, ore 20:27** · Checkpoint: `d657264`
Direttiva: «DIRETTIVA PRIORITARIA DEL PRODUCT OWNER» (100 sezioni), che supera le precedenti
istruzioni visive dove sono in conflitto.

---

## 1. Che cosa è fermo, e che cosa no

Il design visuale attuale (V2 + V3) **non è approvato** e **non viene più esteso** ad altre pagine.
La pagina che il committente ha indicato come esempio di design non accettato è
`/fr/espace-reserve/mes-documents/`; la sua cattura è il BEFORE di controllo (§85 della direttiva).

Chiuso prima del freeze, come richiesto («termina l'operazione atomica corrente»): la fase 1b
delle pastiglie di stato — 63 siti + 12 badge, registro derivato dall'enum, test alla sorgente —
commit `d657264`. È l'ultimo commit del linguaggio V3.

**Esito della suite larga al checkpoint** (nove app + frontend + i18n + compliance, 37 minuti):
1 612 passati, 3 saltati, 1 xfail atteso, **7 falliti — nessuno dovuto alle pastiglie o ai bottoni**.
I sette vengono dalla home e dal lock-up V2 di stamattina (commit `0545b49`/`09aa4e9`): nove stringhe
dell'hero e della rotta («Maroc», «Vénétie»…) assenti dai cataloghi it/en/ar (`i18n_audit --sync`);
il wordmark latino senza `lang` nella cromatura araba (corretto: `lang="en"` sul lock-up); i link del
menu lingua nella pagina araba. L'hero V2 è congelato e viene **ricostruito** nel passo 8: i suoi
msgid si scrivono allora, una volta, nella forma definitiva. Registrato qui perché nessuno legga
«suite verde» dove non lo è.

Resta valido e **non** si tocca: architettura Django, modello di dominio, IAM, Rule Engine, audit,
gate legali, formulazioni vietate (`apps/cms/forbidden.py`), il marchio e la porta ad arco come
fondamento (§80), «nessun colore significa mai approvato» (`static/css/tokens.css` §STATE).

## 2. Strumenti — stato verificato il 24 settembre 2026, ore 20:30 (§95)

| Strumento | Installato | Autenticato | Disponibile | Limiti | Crediti | Piano |
|---|---|---|---|---|---|---|
| **21st.dev MCP** | sì (MCP `mcp__21st__*`) | sì, con la chiave fornita | `get_usage` → `tier: paid`, `aiGenerationEnabled: true`, ricerche e recuperi **illimitati** | nessuno sulla ricerca/recupero | la generazione AI consuma crediti del committente: **non usata**, si usa `search` + `get_component` e si adatta | a pagamento, già attivo |
| **UI-UX-Pro-Max** | sì, plugin `ui-ux-pro-max-skill` **2.13.0** a livello utente | n/a (ricerca locale, nessuna rete) | `scripts/search.py` eseguito con `--design-system` e `--domain` | dati locali: 119 linee guida UX, 79 stili, 192 palette, 74 abbinamenti tipografici, 105 icone, 17 preset GSAP | nessuno | gratuito (MIT) |
| **Motion** | sì, `motion` 13.4.1 vendorizzato, bundle esbuild | n/a | sì | CSP `script-src 'self'`: nessuno script inline | nessuno | MIT |
| **Pexels API** | chiave fornita | sì | pipeline `scripts/fetch_images.py` (sorgente `pexels`) | 200 richieste/ora (limite Pexels) | gratuito | gratuito con attribuzione registrata |
| **Google Chrome Stable 153, visibile, CDP 9222** | sì | n/a | sì — via `scripts/cdp.py` (l'attach di Playwright si blocca sulle schede dell'utente) | — | — | — |

**Come si legge UI-UX-Pro-Max (chiarimento del committente, 20:58).** È una fonte di competenza,
non un design system da accettare o respingere in blocco. La sua proposta per «legal tech
institutional» — navy + EB Garamond/Lato + Google Fonts — si analizza **elemento per elemento**:
il navy è mantenibile o evolvibile se serve al sistema premium; Garamond non è adatto come font UI
dominante (accentua proprio l'estetica editoriale rifiutata), al più un uso display limitato a
giudizio del Creative Director; le Google Fonts non si collegano in rete, ma un font open-source
valido si **self-hosta**. Percorso richiesto: SKILL RECOMMENDATION → EXPERT ANALYSIS → PROJECT
ADAPTATION → LIVE PROTOTYPE → CHROME REVIEW. Le analisi si chiedono con **problem statement specifici
per superficie**, non «generate design system for institutional website».

**Aggiunto il 25/09**: un terzo server locale, `127.0.0.1:8772`, serve lo stesso codice dietro lo storage
compresso di WhiteNoise (`CompressedStaticFilesStorage`, gzip; brotli non installato) da un `STATIC_ROOT` nello
scratchpad della sessione (`measure_settings.py`, fuori dal repository): è l'unico modo onesto di misurare le
prestazioni che la produzione avrà per CSS e JS. I font non si comprimono, l'HTML non è compresso (nessun
`GZipMiddleware`, come in produzione dietro il reverse proxy). Solo pagine pubbliche: il cookie di sessione è per
host, non per porta.

## 3. Le otto pagine campione (§1) e i cinque gate (§71)

| # | Pagina | URL (server) | Gate |
|---|---|---|---|
| 1 | Homepage pubblica | `/fr/` (8770) | A |
| 2 | Navbar / mega-navigation | `/fr/` con menu aperto (8770) | A |
| 3 | Login | `/compte/login/` (8770) | B |
| 4 | Dashboard Persona | `/fr/espace-reserve/` (8771, `qa-person`) | C |
| 5 | Mes Documents — **pagina pilota e di controllo** | `/fr/espace-reserve/mes-documents/` (8771) | C |
| 6 | Fascicolo digitale | `/fr/espace-reserve/dossiers/<id>/` (8771) | D |
| 7 | Orientation wizard | «Ma situation» (8771) | D |
| 8 | Company dashboard | `/fr/espace-reserve/entreprise/` (8771, `qa-company`) | E |

I BEFORE stanno in `docs/qa/chrome/design-v4/before/`. Ogni gate: BEFORE/AFTER, scorecard a dieci
dimensioni senza media (§74), i quattro test — «AI generico?», «ancora editoriale?», «2026?»,
«troppo?» — e revisione indipendente (§72). Nessun implementatore approva il proprio lavoro.

## 4. Ordine di lavoro (§97) — dove siamo

1. checkpoint — **fatto** (`d657264`)
2. stop alla propagazione — **in vigore**
3. audit della pagina indicata — BEFORE catturati, audit in `MES_DOCUMENTS_AUDIT.md`
4. analisi UI-UX-Pro-Max — `UI_UX_PRO_MAX_AUDIT.md`
5. ricerca 21st — `21ST_RESEARCH.md`
6. sintesi del Creative Director — `CREATIVE_DIRECTION.md` (+ `GATE_SCORECARD_TEMPLATE.md`)
7. Design System V4 — `DESIGN_SYSTEM_V4.md`; **fondazione costruita e verificata in Chrome**:
   `static/css/v4/tokens.css` (ultimo layer: nomi V2 con valori V4, override sotto `md` e moto ridotto
   ripetuti, linee `--line-*`), IBM Plex Sans/Mono vendorizzati da `@fontsource` 5.3.0 con
   `scripts/fetch_fonts.py --from-fontsource` (Fira ritirato: −310 KB, +184 KB), `SPRING_SOFT` /
   `SPRING_SNAPPY` in `motion.js`, `tests/frontend/test_v4_tokens.py` (il contratto letto dai blocchi
   css del DS, contrasti ricalcolati, i due fatti di cascata), sei documenti aggiornati. Misurato su
   `/fr/` e `/ar/`: Plex sui controlli, token in cascata, nessun font mancante. I fogli dei componenti
   V4 arrivano con le pagine che li usano (8–11), non prima
8. Homepage/nav V4 — **hero e navbar costruiti e misurati in Chrome** (`static/css/v4/{shell,hero}.css`,
   `templates/pages/home/_hero.html`, `partials/{header,utility_bar}.html`, `components/language_segmented.html`,
   `static/js/src/{home,shell}.js`): un solo palcoscenico SVG 640×520 con la porta del committente, le quattro
   vie che si dissolvono nell'arco interno (uscite etichettate solo se l'eyebrow ha tre parole) e la legenda in
   vetro ancorata alle vie da `home.js`; striscia delle coordinate, marea e territorio rimossi; testata 64→56 in
   vetro, indicatore che trasla, mega-menu a tutta larghezza, cassetto dal lato del menu. **Deviazione
   misurata**: lingua e accesso restano sulla barra istituzionale (le sette voci del menu CMS + lock-up non
   lasciano posto: 905 + 303 px su 1240) finché il committente non decide le quattro voci proposte dal CD.
   **Revisione indipendente del 25/09 (`gates/GATE_A_2026-09-25.md`, commit `c6f3503`): BLOCK** — nessuna
   critica ≤ 2 e i quattro test corretti, ma due verifiche binarie «no» (letterali fuori dai token;
   prestazioni non dimostrate), la testata che a 1280–1439 sovrastampava il marchio, la variante interim
   non osservabile (8770 su codice vecchio). Correzioni applicate nello stesso giorno: 1 testata (13,5 px/8 px
   sotto 90rem, 10 px di padding sopra), 2 legenda (didascalia fissa in testa al pannello, nessun salto,
   nodi fermi), 3 letterali → token (`--drop-door`, `--grad-primary-*`, `color-mix`; test
   `test_the_v4_component_sheets_carry_no_literal_colour`), 4 vie con casing scuro e treccia nella navata,
   5 toggle 44, bersagli touch, righe 44, porta mobile 180, 7 segmentato nel cassetto e frecce in tutto il
   mega-menu, 9 entrambi i server riavviati, 10 hover del palcoscenico rimosso, 11 soglia 24 px. Restano
   al committente: la deroga sull'altezza dell'hero a 390, le lingue dell'hero arabo, la terza colonna del
   mega-menu (fotografie), il glifo «ع» (45 KB di font arabo sulle pagine latine).
   **Prestazioni misurate** (Chrome, CDP, server di sviluppo **senza compressione**, cache disattivata; profilo
   Lighthouse «slow 4G»: 150 ms RTT, 1,6 Mb/s, CPU ×4): home LCP **520 ms** senza limiti / **4,2 s** su 4G, CLS 0 / 0,025,
   5 long task; console LCP 552 ms / 3,3 s, CLS 0 / 0,057. Trasferito per pagina: home CSS 318 KB, JS 101 KB, font
   487 KB (Newsreader tondo + corsivo 272, Plex Sans latin 69, Plex Sans Arabic per il glifo «ع» 45), immagini 86,
   40 richieste; console CSS 336, JS 97, font 259. Il tetto «LCP < 2,5 s su 4G» **non è dimostrato**: senza
   compressione il CSS (318 KB, render-blocking) costa da solo 1,6 s; con brotli in produzione CSS e JS scendono a
   ≈ 90 KB, i font no. Riduzioni possibili e non decise qui: il glifo «ع» in latino (−45 KB), il corsivo di
   Newsreader (−143 KB, ma è il lead della direzione), i fogli V2/V3 co-caricati (finiscono con la propagazione).
   Catture: `docs/qa/chrome/design-v4/after/01_home_*.png`, `02_header_*.png`. Le altre sezioni della home
   (vie, processo, orientation, ecosistema, news, piè di pagina) sono ancora V2 sotto i token V4.
   **Secondo giro di revisione indipendente (`gates/GATE_A_2026-09-25_round2.md`, su `d99f2bb`): BLOCK per la
   sola regola delle prestazioni** — punteggi 4/4/4/3/4/4/4/3/3/4, i quattro test corretti, correzioni 1, 2, 3,
   7, 9, 10 chiuse, 5 e 6 chiuse con riserva, 4 parziale, 8 non dimostrabile sul server senza compressione.
   Tre difetti nuovi trovati dal revisore e corretti lo stesso giorno: la testata che oscillava a scrollY 25–32
   (13 commutazioni in 3 s → `html { overflow-anchor: none }`, misurato 0 commutazioni a 25/28/30/32/40); lo
   scrim del cassetto fissato a `--header-height` che copriva 34 px della testata a 768–1279 (ora dall'alto,
   `z-index` sotto la testata: misurato top 0 / 19 < 20 a 768 e 1024 — **sbagliato**, vedi il terzo giro); il commento dell'hero «completo al primo
   frame» falso (lead, corpo e azioni partivano a opacità 0 per ≈ 1 s: `data-reveal` tolto, regola morta
   rimossa, misurato opacità 1 a 150 ms). Inoltre: treccia delle vie alla soglia della navata (y 372–390, non a
   metà parete), pannello della legenda 264 px (quattro righe da 44, nessuna parola a capo), controlli lingua e
   accesso a 44 px al tocco (misurato con emulazione touch: barra 44, lucchetto 44, lista 44, link 44 tramite
   area di tocco), riga 83 del template di scorecard corretta (`test_motion_system.py` non esiste).
   **Deroga proposta al committente per l'hero a 390** (suggerita dal revisore): altezza ≤ 130 % del viewport e
   le due azioni dentro gli 844 px — misurato 129 %, azioni a 757 e 813 px (**sbagliato**: viewport desktop con barra di scorrimento; vedi il terzo giro). **Prestazioni con compressione**
   (server 8772, gzip, slow 4G, CPU ×4, due passate): home LCP **3,4–3,5 s** (contro 4,6–5,8 s senza
   compressione), CSS 349 → 94 KB, JS 101 → 37 KB; ingresso LCP **2,9 s** (contro 4,4 s). L'elemento LCP è la
   fotografia della porta (`doorway-800.webp`, 77 KB, scoperta dopo il CSS). Il tetto di 2,5 s **resta non
   raggiunto**: i font pesano 402 KB sulla home (Newsreader tondo 129 KB per il lock-up del marchio, presente su
   ogni pagina; corsivo 144 KB per la citazione della fascia forum, sezione V2; Plex 85 KB). Fatto: il lead
   dell'hero in Plex (era il corsivo serif), la voce araba del segmentato disegnata dal carattere di sistema
   sulle pagine non arabe (−44,5 KB), preload di Plex prima di Newsreader. **Da decidere dal committente**: il
   carattere del lock-up (Newsreader 600 per venti caratteri costa 129 KB: subset con fonttools — non
   installato —, oppure Plex, oppure il wordmark come SVG), il corsivo della fascia forum (cade con la
   propagazione V4 della home).
   **Terzo giro di revisione indipendente (`gates/GATE_A_2026-09-25_round3.md`, su `dd29168`): BLOCK per la
   sola regola delle prestazioni** — punteggi 3/4/4/3/4/4/4/3/3/4 (Premium Feel da 4 a 3: due correzioni del
   secondo giro avevano prodotto difetti visibili), i quattro test corretti; chiusi l'oscillazione della
   testata, il testo dell'hero al primo frame, la treccia, i bersagli 44 al tocco; **aperto e regredito** lo
   scrim; parziali prestazioni, deroga, legenda a 1024 e documentazione; quattro difetti nuovi (7–10).
   Correzioni applicate lo stesso giorno e misurate in Chrome visibile (catture in
   `docs/qa/chrome/design-v4/after/review_a3fix/`):
   - **2, scrim.** Lo scrim è figlio della testata sticky, che con il suo `z-index` 20 forma un contesto di
     impilamento: il 19 lo metteva **sopra** il lock-up e il bottone «Menu», non sotto la testata. Il «19 < 20»
     del secondo giro confrontava numeri di livelli diversi. Ora lo scrim parte dal piede misurato della testata:
     `main.js` scrive `--nav-drawer-top` sulla testata, e cassetto e scrim lo ereditano. Misurato a 390, 768 e
     1024 con `scrollY` 0 e 200: bordo dello scrim = piede della testata (98, 65, 57 px); `elementFromPoint`
     su lock-up, «Menu» e link lingua = l'elemento stesso; differenza di pixel chiuso → aperto sul lock-up
     0,63–0,89 su 255. Stesso esito su `/fr/parcours/` e sulla pagina di accesso.
   - **4, deroga.** Misurata con un viewport mobile vero (390 CSS px, nessuna barra): interim **1 090,8 px =
     129,2 %** (era 132,1), azioni finite a 760,8 e **816,8** (27 px dentro lo schermo); `phase3` 124,1 %, azioni
     a 661,3. A 768 × 1024: interim 124,2 %, azioni finite a **1 007,8**, dentro la piega. Due cause: il margine
     V1 delle azioni (`components.css`, 32 px) non collassava nella colonna flex del telefono (48 px fra lead e
     azioni, ora 24 come i due gradini sopra), e sotto 64rem 7vh sopra la porta (72 px su un tablet verticale,
     ora 40). La deroga resta **da firmare dal CD**.
   - **5, legenda.** 236 px fra 64 e 80rem, non 200: «Universités & Formation» misura 144 px a 13 px. Quattro
     righe da 44 a 1024, 1280 e 1440, su 8770, 8771 e `/ar/`; a 1024 il pannello copre 38 px dello stipite (29 a
     1280) e si ferma 15 px prima del navy. **Resta**: sul telefono (legenda 2 × 2) la quarta cella va su due
     righe (56 px), perché una cella ha 87 px per la parola.
   - **6, documentazione.** Il nome dei link della legenda è ora la parola; il gloss è la loro **descrizione**
     (`aria-describedby` su un elemento nascosto), letta dall'albero di accessibilità in `fr` e `ar`. Il
     commento di `_hero.html` è ora vero anche per il titolo (vedi 7). **Deviazioni da firmare dal CD**: il lead
     dell'hero non più corsivo (CD §3.1); il risparmio di 143,4 KB sulla home arriva solo quando la fascia forum
     V2 smette di scaricare il corsivo, ancora misurato il 25/09. **Residuo**: il toggle del sotto-menu resta
     24 × 44 fra 80 e 90rem (28 × 44 da 90rem). Con le sette voci di `phase3` la lista misura ≈ 745 px e lascia
     ≥ 100 px d'aria, che cinque toggle da 44 consumerebbero; da 90rem l'aria è 32 px. Dipende dalla decisione
     del committente sulle quattro voci; il minimo di 2.5.8 (24 px) è rispettato.
   - **7, titolo.** Il reveal a maschera del titolo (CD §3.1) partiva dal modulo differito **dopo** il primo
     paint: nascondeva un titolo già letto e lo faceva rientrare. È **rimosso** da `home.js`, con la maschera
     `.line { overflow: hidden }` che serviva solo a lui: **0** fotogrammi con una riga nascosta su 870 e 978
     campioni (4G lento, due passate) e su 359 senza limiti. Deviazione da CD §3.1 **da firmare dal CD**.
   - **8, uscite.** Fuori dall'arco ogni via sale o scende all'altezza della sua uscita entro 24 unità, lungo lo
     stipite (x 531–555), poi corre in piano fino al nodo (`home.js` e `services._route_path`, stessa formula).
     Un'etichetta di più parole va a capo prima dell'ultima: su una riga «MOBILITÉ RÉGULIÈRE» arrivava a x 503,
     dentro il navy della treccia. Un alone `--mid-1` sotto le lettere (`paint-order`) interrompe il contorno
     della porta (x 592 e 608), che attraversava ogni parola: il revisore non lo contava, la cattura lo mostrava.
     Misurato su 800 campioni per via: **0** dentro ogni etichetta a 1440 e 1280 in `fr`, e a 1440 in `it`, `en`
     e `ar`. La treccia resta a y 372–390, sopra il piede del navy (397). In colori forzati l'etichetta è
     `CanvasText` su un alone `Canvas`.
   - **9, menu account del cassetto.** Il `<details>` prende la larghezza del suo riassunto e la lista parte dal
     suo bordo iniziale: scarto **0 px** a 390, 768 e 1024, in LTR e in RTL, dentro il viewport.
   - **10, anello.** Una sola regola in `v4/shell.css` per barra, testata (mega-menu e cassetto compresi) e hero:
     l'anello della cascata, 2 px, con il suo compagno di 2 px. Nell'hero navy si usa la coppia scura
     (`--accent-dark` + `--mid-1`), la stessa della rail della console. Misurato dopo la transizione su quindici
     controlli: chiaro `#1d8a93` + carta su barra, testata, mega-menu e cassetto; scuro `#7fd1d8` + `#0b1a33` su
     primario, secondario e righe della legenda. I corpi delle pagine pubbliche V2 tengono l'alone V2 fino alla
     propagazione.
   **Prestazioni** (8772, gzip, 4G lento, CPU ×4, 1440 × 900): LCP **3 656 ms** a freddo (TTFB 756) e **3 056 ms**
   alla seconda passata. L'elemento è la fotografia della porta, precaricata. CLS 0,012 / 0,009; senza limiti LCP
   348 ms. Trasferito: CSS 99,1 KB gzip in 22 fogli, JS 35,7, font 356,1 (Newsreader tondo 128,9 precaricato per
   titolo e lock-up, corsivo 143,4 per la fascia forum V2, Plex 83,8), immagini 79,5, 42 richieste; nessun font
   arabo. Il tetto di 2,5 s **resta non raggiunto**. Le leve restano del committente: il carattere del lock-up,
   il corsivo della fascia forum e la concatenazione dei fogli.
   **Quarto giro di revisione indipendente (`gates/GATE_A_2026-09-25_round4.md`, su `156db5f`): BLOCK per la
   sola regola delle prestazioni** — punteggi invariati 3/4/4/3/4/4/4/3/3/4, i quattro test corretti; delle
   correzioni del terzo giro sette chiuse sulla misura (2, 4, 5, 7, 8, 9, 10), due parziali (3 prestazioni, 6
   documentazione), nessuna regredita; cinque difetti nuovi (11–15), due dei quali rovesci diretti delle
   correzioni del terzo giro. Correzioni applicate e misurate in Chrome visibile il 26/09 (catture in
   `docs/qa/chrome/design-v4/after/review_a3fix/`, prefisso `fix_1…`):
   - **11, il palcoscenico.** La coreografia d'ingresso partiva dal modulo differito **dopo** il primo paint:
     traccia dell'arco e vie a `stroke-dashoffset 1`, nodi e uscite a opacità 0, gradini a `scaleX(.7)`, chiave
     8 px più in basso, corrente riportata a 0. Toglieva ciò che la persona aveva già visto, come il titolo del
     terzo giro. È **rimossa** da `home.js`, e con lei la stessa coreografia della porta sulla pagina di accesso
     (`static/js/src/entrance.js` e il suo bundle, cancellati: il file faceva solo quello). La deriva della
     fotografia allo scroll ora parte dallo stato dipinto (`scale(1.06)`, prima 6 px più in basso). Misurato per
     fotogramma su vie, nodi, uscite, traccia, gradini, chiave e fotografia: **0** passaggi da visibile a
     nascosto e **0** cambi di trasformazione al caricamento, su 8770 (261 fotogrammi), 8771 (364), la pagina di
     accesso (210) e 8772 su 4G lento + CPU ×4 (690). Restano la corrente (CSS, dal primo fotogramma) e la coppia
     legata allo scroll. **Deviazione da CD §3.1 e §4 da firmare dal CD**, con quella del titolo.
   - **12, il cassetto al ridimensionamento.** `main.js` misura di nuovo il piede della testata a ogni `resize`
     e a ogni cambio di dimensione della testata (`ResizeObserver`) mentre il cassetto è aperto. Misurato dopo
     due fotogrammi e a riposo, per 390 × 844 ↔ 844 × 390 (rotazione, `mobile: true`), 600 ↔ 1024 e 768 × 1024 →
     1024 × 768: bordo del cassetto e dello scrim = piede della testata (57 o 98 px), lock-up e «Menu» colpiscono
     sé stessi, in tutti e cinque i casi.
   - **13, il disegno delle uscite.** (a) Ogni incrocio resta nel navy: la treccia termina a x 496, ogni via sale
     o scende alla quota della sua uscita fra x 496 e 520 (dentro l'arco, a destra della chiave) ed esce
     dall'arco in piano fino al nodo; stessa formula in `home.js` e in `services._route_path`. Misurato su 2 000
     campioni per via a 1440 e 1280, in `fr` e in `ar`: fuori dal navy due vie dirette a uscite diverse distano
     **≥ 98,6** unità (criterio ≥ 6) e non si incrociano; **0** campioni nelle etichette in `fr`, `ar`, `it`, `en`.
     (b) Le uscite si disegnano da 80rem, dove sono visibili. Sotto, `home.js` traccia la via senza uscite e il
     tratto torna alla dissolvenza: a 1024 le quattro vie finiscono a x 531, al bordo dell'arco. Senza JS fra 64
     e 80rem il tracciato del server porta ancora alle uscite; la dissolvenza ne nasconde il tratto, ma il
     casing (navy a 0,75) resta visibile sulla pietra. È un limite dichiarato del disegno senza script.
   - **14, le uscite arabe.** Il palcoscenico non è specchiato, e ora non lo è nemmeno il suo testo
     (`.doorway { direction: ltr }`): in RTL `text-anchor: end` metteva le parole a destra del nodo, fuori dai 640
     del viewBox. Misurato su `/ar/` a 1440 e 1280: etichette a x 599,9–636,4, sopra il nodo come in LTR, **51 px**
     dalla colonna del testo, 0 campioni di via.
   - **15, le frecce del mega-menu.** Link e chevron di ogni sezione sono fermate con le frecce: ←/→ passano alla
     sezione vicina, sezioni senza pannello comprese; ↓ apre il pannello ed entra; ↑ dal primo link torna alla
     fermata che l'ha aperto; Esc torna lì. Nessuna freccia scorre la pagina. La causa del salto di «Voir
     l'espace» era un doppio trattamento: il ↓ della barra, dopo aver messo il focus nel pannello, risaliva
     all'`li` e veniva trattato di nuovo. Misurato con tasti reali su 8770 e 8771 `fr` e 8770 `ar`: ↓ → «Voir
     l'espace» → «Votre parcours», ↑ → «Voir l'espace», ↑ → la fermata d'origine; `scrollY` invariato; in RTL ←/→
     speculari.
   - **6.** (b) Nella legenda la riga porta la lingua della sua parola e il gloss la propria (`label_lang`,
     `text_lang`); la didascalia prende la lingua del gloss. Su 8771 `/ar/` le quattro righe sono nella lingua
     della pagina, i gloss francesi portano `lang="fr"` e la didascalia è `fr`, LTR. Le **traduzioni arabe** dei
     testi prescritti restano una decisione del committente. (c) Lo chevron è **44 × 44** dove c'è aria, cioè
     su una barra di cinque sezioni o meno: interim, quattro sezioni, 296 px d'aria a 1280–1439 e 370 a 1440.
     Resta 24 × 44 / 28 × 44 sulle sette sezioni di `phase3`, dove l'aria misurata è **31–32 px** con tre
     chevron. Il numero «≥ 100 px» della nota di `v4/shell.css` era sbagliato e ora è corretto. (a) Le
     deviazioni da firmare dal CD sono ora quattro: lead non corsivo, titolo senza reveal, palcoscenico senza
     coreografia d'ingresso, deroga a 390. Per la deroga il revisore ha misurato 136,3 % a 375 × 812 e 142,3 % a
     360 × 800, quindi la gamma di viewport va scritta con la firma. Nessuna è scritta in `CREATIVE_DIRECTION.md`,
     che è il documento del CD.
   **Prestazioni** (8772, gzip, 4G lento, CPU ×4): LCP **3 004 / 3 068 ms**, fotografia della porta; CLS
   0,003 / 0,034; senza limiti 388 ms. CSS **99,4 KB** gzip in 22 fogli (a 0,6 KB dal tetto proposto di 100), JS
   36,0, font 356,1, 42 richieste; HTML 43,8 KB non compresso. Invariate le leve del committente.
   **Quinto giro di revisione indipendente (`gates/GATE_A_2026-09-25_round5.md`, su `d475749`), eseguito come
   workflow: un revisore, poi uno scettico per ogni difetto nuovo che lo ri-misura e prova a confutarlo.
   BLOCK per la sola regola delle prestazioni.** Punteggi 4/4/4/3/4/4/4/4/3/4: Premium Feel e Interaction
   Quality salgono a 4. Motion resta a 3 per la coreografia tolta senza firma e per la transizione di
   `min-block-size` della testata. Mobile resta a 3 per la deroga a 390 non scritta e per il difetto 16. Le
   correzioni 11–15 sono chiuse; 3 e 6 restano parziali. Tre difetti nuovi, **tutti confermati** dagli
   scettici, nessuno confutato. Durante la verifica il container del database si è fermato a un riavvio di
   Docker (09:12), e gli scettici hanno misurato l'HTML servito da `d475749`, salvato prima. Correzioni del
   26/09, misurate a database ripristinato:
   - **16, senza JavaScript sotto 80rem** (difetto anteriore, dal 17/09). Il menu completo sta nella testata,
     e la testata sticky copriva la pagina a ogni scroll: 1 014 px a 390. Senza script la testata ora
     scorre con la pagina (`html.no-js .site-header { position: relative }` sotto 80rem). Misurato con la
     rotella a 390, 768, 1024 e 1279: dopo 1 500 px la testata è fuori dal viewport (0 px visibili) e il
     centro del titolo dell'hero colpisce il titolo; a 1440 la testata sticky da 65 px è invariata. Il
     residuo del 13b senza script è chiuso: fra 64 e 80rem le vie sono ritagliate al bordo dell'arco
     (`clipPath` `doorway-routes-arch`, x ≤ 531). A 1024 e 1279 i pixel dentro l'arco sono identici, e sulla
     pietra non resta nulla.
   - **17, il ritmo della barra interim a 1280–1439.** Lo chevron da 44 px metteva 21 px d'aria per lato
     contro 14 fra due sezioni senza chevron, e «Forum Vénétie–Maroc Projet» si leggeva come una voce sola.
     Il riquadro da 44 ora si sovrappone ai 7 px di padding dei vicini e sta sopra di essi. L'anello è
     disegnato dentro (`outline-offset` −4 px, compagno `inset`) e non tocca le parole vicine. Misurato con
     `Range.getClientRects`: ogni distanza d'inchiostro è **14 px**, scarto 0, a 1280, 1366 e 1439 in `fr` e in
     `ar`. I tre chevron rispondono al tocco su tutto il riquadro 44 × 44, ai quattro bordi. A 1440 le
     distanze sono 24/28, scarto 4. `phase3` ha scarto 3 a 1280.
   - **18, colori forzati.** L'arco interno prende `Canvas` con un contorno `CanvasText`, e i casing delle vie
     `Canvas`. Misurato sui pixel a 1440 in `fr` e `ar`: salite 21:1, treccia 7,0 e 9,7:1. Anche i nodi
     d'uscita passano a `CanvasText`.
   **Prestazioni** (8772, 4G lento, CPU ×4, due passate ripetute due volte): LCP 3 336 / 3 392 e poi 3 140 /
   3 056 ms, sempre la fotografia della porta; la varianza fra le passate è di ≈ 300 ms. CLS ≤ 0,034. Il CSS è
   ora **100,0 KB gzip**: tocca il tetto proposto. **Leva misurata per il committente**: senza commenti, i 21
   fogli di `main.css` pesano **47,8 KB** gzip invece di 95,3. Basterebbe un passo di minificazione a
   `collectstatic`, senza pacchetti nuovi (un'espressione regolare nello storage). È una decisione di build del
   committente, come la concatenazione dei fogli.
   **Sesto giro di revisione indipendente (`gates/GATE_A_2026-09-25_round6.md`, su `213e00f`; stesso workflow):
   BLOCK per la sola regola delle prestazioni.** Punteggi 4/4/4/3/4/4/4/3/3/4. Le correzioni 16, 17 e 18 sono
   chiuse sul loro criterio; 3 e 6 restano parziali. Interaction Quality torna a 3 per il difetto 19, un
   rovescio della correzione 17. Tre difetti nuovi, **tutti confermati** dagli scettici, nessuno confutato.
   Correzioni del 26/09, misurate in Chrome visibile:
   - **19, gli stati dello chevron sulla barra interim.** La sovrapposizione del terzo giro portava la
     tinta di hover a 1–3 px dalle parole vicine, la fondeva con la pillola della sezione corrente e dava allo
     chevron i clic sul bordo di «Forum». Ora il riquadro da 44 è solo l'area di tocco: tinta e anello sono una
     forma di 28 px al suo centro (`::before`, anello `outline-offset` −6 px). Il ritmo sotto 90rem lo tiene
     un padding di 14 px attorno a ogni parola, senza sovrapposizioni. Misurato a 1280, 1366 e 1439, in `fr` e
     in `ar`: ogni distanza d'inchiostro è **28 px** (scarto 0); tinta a 24–37 px dalle parole, anello a 20–24;
     8 px fra la tinta e la pillola corrente su `/fr/entreprises/`; i bordi di ogni link colpiscono il link;
     un clic reale 3 px dentro «Forum Vénétie–Maroc» porta a `/fr/forum/`; chevron 44 × 44; aria dal lock-up
     240 px in `fr` e 304 in `ar`. A 1440 lo scarto resta 4.
   - **20, la chiave in colori forzati.** L'arco interno riprende il suo navy, il fondo della chiave; le vie
     restano leggibili grazie al loro casing `Canvas`. Palette chiara e scura, `fr` e `ar`: chiave **5,3:1**
     sul navy, foro dell'anello 1,08–1,10:1 sul fondo, salite 15,3:1 sul casing.
   - **21, glifi e gradini in colori forzati** (difetto anteriore). I glifi della legenda passano a `CanvasText`:
     20:1 in entrambe le palette. I gradini sono a piena opacità, con un bordo `Canvas` di 2 px sotto il
     riempimento. Misurati contro i pixel appena fuori dal bordo: mediane 4,9–19,6:1 nella palette chiara e
     14,2–20,0:1 nella scura; il minimo di 2,8 è sui pixel di bordo fra due gradini.
   **Il CSS era salito a 100,5 KB gzip.** I miei commenti dei giri 3–6 in `v4/shell.css` e `v4/hero.css` ora
   sono di una o due righe, con il riferimento al giro; le misure stanno qui. Il confronto senza commenti con
   `213e00f` mostra che sono cambiate solo le regole di 19–21. Ora il CSS pesa **99,0 KB** gzip. **Prestazioni**
   (8772, 4G lento, CPU ×4): LCP 3 364 / 3 416 ms, sempre la fotografia; CLS ≤ 0,034. La varianza fra le
   passate di questi giri va da 3,0 a 3,7 s.
   **Settimo giro di revisione indipendente (`gates/GATE_A_2026-09-25_round7.md`, su `265577c`; stesso workflow):
   BLOCK per la sola regola delle prestazioni.** Punteggi 4/4/4/3/4/4/4/4/3/4: Interaction Quality torna a 4.
   Le correzioni 19, 20 e 21 sono chiuse sul loro criterio; 3 e 6 restano parziali. Il confronto senza
   commenti fra `213e00f` e `265577c` cambia solo le regole di 19–21. C'è un difetto nuovo, **22**,
   confermato e giudicato minore: la forma di 28 px dello chevron, un `::before` che riceveva i puntatori,
   faceva stimare al ritocco del tocco di Chrome un bersaglio di 36–38 px, e i 4 px esterni del riquadro da
   44 andavano ai link vicini. **Corretto** il 26/09 con `pointer-events: none` sulla forma. Misurato con il
   banco dello scettico del settimo giro, un tocco per pixel sull'intero riquadro, a 1280, 1366, 1439 e 1440,
   in `fr` e in `ar`: con raggio di tocco 1, 6 e 12 sul primo chevron e 6 sugli altri, **43 o 44 pixel su 44**
   aprono il pannello (prima 36–38). Il pixel residuo è sempre l'ultimo mezzo pixel del bordo verso il link
   successivo nell'ordine di lettura: dove due bersagli si toccano, vince il successivo. Lo stesso effetto c'è
   sulla barra `phase3`, che non è cambiata (22 su 24). Invariati gli stati di 19: tinta a 24–37 px dalle
   parole, anello a 20–24, 8 px dalla pillola corrente, clic sui bordi dei link, distanze d'inchiostro 28 px.
   **Verifica indipendente** (`442cda6`, round-7 §9): correzione 22 **chiusa**, nessuna regressione. 3 432 tocchi
   su 78 scansioni: 3 405 aprono il pannello dello chevron; gli altri 27 cadono a 0,5 px dal bordo condiviso
   con il link successivo, un pareggio di bordo più largo sulla barra `phase3` invariata. 252 clic del mouse
   sui bordi su 252 raggiungono il loro bersaglio.
   **Prestazioni** misurate dal revisore sul settimo giro: LCP 3 032 / 2 940 ms, sempre la fotografia; CSS
   99,0 KiB gzip; font 356,1 KB, sopra anche il tetto di 320 KB già scritto nel DS 2026 §6.2; HTML non
   compresso. Restano le decisioni del committente e del CD elencate sopra.
   **Prestazioni, decisioni del committente del 26/09 (budget approvato: LCP ≤ 2,5 s, CLS ≤ 0,10, INP
   ≤ 200 ms, nel profilo concordato).** L'LCP è stato prima **scomposto**, sul server 8772 con 4G lento e
   CPU ×4, a 1440 × 900. TTFB 88–90 ms. La fotografia viene scoperta dal preload a +139–148 ms, ma la
   richiesta parte solo a +1 208–1 521 ms: priorità Low, in coda dietro 21 fogli VeryHigh sulle sei
   connessioni HTTP/1.1. Poi 1,24–1,66 s di trasferimento conteso (corsivo di Newsreader, 144 KB, a metà
   download) e 39–166 ms di render. LCP 2 992 / 3 012 ms. Il carattere del marchio **non** era la causa;
   il committente non ne autorizza la modifica, e non è stato toccato. Interventi, nell'ordine:
   - **build CSS** (`scripts/build_css.mjs`, `npm run build:css`, esbuild già presente): i 21 fogli
     diventano `css/dist/main.css`, **35,6 KB gzip invece di circa 95**, e ogni foglio d'app è minificato
     in `css/dist/…`. Nessun commento, nessun abbassamento di sintassi, `url()` riancorati nello spazio
     statico. **Equivalenza provata**: circa 7 milioni di valori calcolati, confrontati bundle contro
     sorgenti su 30 combinazioni pagina × larghezza (sito pubblico, console, fascicolo, impresa,
     selezione, sportello, formazione, orientamento), **0 differenze**. Test
     `tests/frontend/test_css_bundle_is_current.py`; DS 2026 §2 riscritto;
   - **compressione HTML** nello stack applicativo (`core.middleware.TextGZipMiddleware`, sotto
     WhiteNoise: nessun proxy nel repository; solo tipi testuali; padding BREACH di Django):
     **43,9 → 7,9 KB**, `Vary: Accept-Encoding`. Test `tests/security/test_html_compression.py`;
   - **fotografia**: ritagliata alla striscia che l'arco mostra davvero (il 50 % centrale) e ridotta a
     400 × 533, la stessa densità visibile di prima. Scarto dall'ideale 3,30 contro il 3,69 di oggi:
     più fedele, e **41,9 KB invece di 77** (`brand/v2/doorway-arch-400.webp`). Il preload porta ora
     `fetchpriority="high"`;
   - **CLS mobile**: sotto 64rem il riquadro SVG ha le proporzioni dell'arco dal primo fotogramma
     (`aspect-ratio: 368 / 456`). `home.js` restringeva il viewBox dopo il paint e la copia scendeva di
     77 px: 0,054 → 0,0043.
   **Dopo**, stesso profilo, tre passate: desktop LCP **1 440–1 672 ms** (la fotografia; ritardo di
   richiesta 131–141 ms), CLS 0,0032; mobile (412 × 823, DPR 1,75) LCP **1 424–1 820 ms** (il lead),
   CLS 0,0043. **Prestazioni: dentro il budget.** Il corsivo di Newsreader parte ora a circa 1,3 s, dopo
   la fotografia, e non pesa più sull'LCP. La tipografia sarà comunque riesaminata nella direttiva V5.
   **Suite completa** sull'albero con questi interventi: 3 221 superati, 12 falliti. Quattro erano test che
   citavano i vecchi percorsi dei fogli (aggiornati a `css/dist/…`). Otto fallivano già su `df8dc42`, cioè
   prima di oggi, e sono stati corretti nello stesso commit: il test dei partner leggeva l'`<img>` del
   lock-up nel piè di pagina come un logo (ora limitato a `<main>`); i sei test browser del portale
   cercavano la navigazione locale V2 (`nav.local-nav`) che la console V4 ha sostituito con la rail
   (ora `.rail__item[aria-current]`), e una parola di 101 caratteri senza spazi in un titolo di scadenza e
   in un oggetto di messaggio allargava le righe della dashboard a 1 105 px (ora `.dates__what` e
   `.threads__subject` possono restringersi e spezzare la parola); `docs/I18N_RTL.md` citava
   `language_switcher.html`, rinominato il 25/09 in `language_segmented.html`.
9. Login/app shell V4 — **costruiti** (`templates/allauth/layouts/entrance.html` + `apps/accounts/static/accounts/entrance.css`
   + `static/js/src/entrance.js`, rimosso il 26/09 con la coreografia della porta, vedi il quarto giro del gate A; `templates/partials/portal_chrome.html`, `templates/portal/base_portal.html`,
   `templates/portal/partials/rail_nav.html`, `apps/portal/static/portal/console.css`, `static/js/src/console.js`;
   la porta come componente `templates/components/doorway.html`; il campo password con il controllo
   mostra/nascondi etichettato in `components/form_field.html`; il bottone occupato con il misuratore): da
   misurare in Chrome e da sottoporre al revisore (gate B). Non costruiti, e detto: la ricerca della console e il
   CommandMenu (nessun motore di ricerca esiste: sarebbe una funzione inventata), il campanello delle notifiche
   (il conteggio dei messaggi non letti è già nella voce «Communications»), lo stato «successo» del bottone
   prima del redirect (l'accesso è un POST intero, non una richiesta in pagina).
   **Misurato in Chrome il 25/09** (`docs/qa/chrome/design-v4/after/04_login_*.png`, `05_console_*.png`): ingresso
   5/7 con la porta a 320 px e la striscia in vetro, foglio 480 raggio 20, titolo Plex 28/600, campi 44/10, toggle
   password funzionante, primario 52; a 768 fascia 141 px con l'arco, a 390 il foglio a tutta larghezza. Console:
   rail 248 aperta da 90rem / 64 chiusa (persistita), tooltip L3 a rail chiusa, barra 56 in vetro appiccicosa con
   breadcrumb, «Site public», account e lingua segmentata; sotto 64rem barra superiore, barra inferiore (cinque voci,
   etichette sillabate) e cassetto `<dialog>` da 300 px con la rail intera; RTL specchiato; 0 `style=""`. Il
   contenuto del workspace (titoli serif, fasce, elenchi) è ancora V2: è il gate C.
   **Revisione indipendente del 25/09 (`gates/GATE_B_2026-09-25.md`, su `4185bae`): BLOCK** — punteggi
   3/4/4/3/4/4/3/3/3/3, i quattro test corretti, AFTER superiore su ogni vista; sulle sole dimensioni sarebbe
   CONDITIONALLY_READY; il BLOCK viene dalla verifica 9 (prestazioni: ingresso LCP 2,94–2,97 s con gzip) e
   dalla 11 (vetrina non verificata). Tredici correzioni; applicate e misurate lo stesso giorno: (1) il
   controllo mostra/nascondi della password non aveva alcuna regola CSS — ora un controllo GHOST di 36 px
   dentro il bordo finale del campo, Plex 13/20 500, hover, premuto = wash dell'accento, area di tocco 44,
   bordo `CanvasText` a colori forzati (misurato 168 × 36 a 1440, 160 × 36 a 390, dentro il campo, `type`
   e etichetta che cambiano, `aria-pressed`); (2) il tooltip della rail in RTL era ancorato al bordo
   sinistro del viewport (`inset-inline-end` scritto per LTR) — ora lati fisici: bordo destro del tooltip =
   bordo sinistro della voce − 12 px, centro verticale coincidente (misurato 1362 / 1374, gap 12, Δ 0), col
   ritardo di 400 ms sul puntatore e nessuno sul focus; (3) i link lingua del cassetto della console
   avevano altezza 0 sotto 768 px (`--utility-h` = 0) — misurati 40 × 32 con puntatore fine, 44 × 44 al
   tocco; (4) bottone del menu 40 con area 44 via `::after`, riassunto account 44 al tocco; (5) il menu
   account è il Menu V4 (`--min-3`, hairline, `--shadow-3`, raggio `lg`, voci 36 Plex 13, separatore prima
   di «Se déconnecter»; misurato); (6) la fotografia della porta è precaricata (`<link rel="preload"
   as="image">`) sull'ingresso e sulla home, la voce araba del segmentato — nome nascosto compreso — usa il
   carattere di sistema sulle pagine non arabe (−44,5 KB: misurato, nessun font arabo caricato
   sull'ingresso francese); (7) la fascia dell'ingresso sotto 768 px tiene la porta a 64 px accanto
   all'aiuto (raggio `lg`); (8) colori forzati: bordo `CanvasText` su tooltip, cassetto e toggle,
   `filter: none` sulla porta; (9) ritardo del tooltip, ingresso del workspace (`ws-in`, 200 ms), anello di
   focus della rail con `--accent-dark`; (10) landmark distinti («Navigation de l'espace réservé» ·
   «Navigation rapide» · «Menu»), `lang="en"` sul wordmark, frecce ↑↓/Home/End anche nel cassetto
   (misurato); (11) il test dei letterali copre `entrance.css` e `console.css`. **Prestazioni dopo le
   correzioni** (8772, gzip, slow 4G, CPU ×4, due passate): ingresso LCP **2,7–3,0 s** (font 259 → 214 KB),
   home **3,1 s** (font 402 → 358 KB). Il tetto di 2,5 s **resta non raggiunto**, e la causa misurata non è
   più il peso ma le richieste: 21 fogli CSS e 38 richieste su un server HTTP/1.1 a 150 ms di RTT (sei
   connessioni: quattro giri di rete prima del primo rendering); precaricare la fotografia non sposta
   l'LCP perché il rendering stesso aspetta i fogli. Due leve, nessuna decisa qui: (a) un passo di build
   che concateni la cascata in un solo foglio per la produzione (stima: −600 ms e più su 4G lento; il
   contratto «ogni foglio importato da main.css» resta vero alla sorgente); (b) il carattere del lock-up
   (129 KB). **Budget numerico proposto al CD** (nessuno esisteva, verifica 9): per pagina, con gzip, CSS
   ≤ 100 KB, JS ≤ 45 KB, font ≤ 200 KB, LCP < 2,5 s e CLS < 0,1 su slow 4G. **Non chiuse, e dette**: (12)
   «Communica-tions» sillabato nella barra inferiore a 390 — decisione di copy del CD (etichetta breve
   diversa dalla voce della rail?); (13) la vetrina `/_design/` — vedi sotto. **Deviazioni registrate**: la
   testata pubblica resta sopra l'ingresso (CD §3.3 voleva il lock-up scuro sul palcoscenico); la cartella
   delle catture `docs/qa/chrome/design-v4/after/` non è ignorata da git (le catture restano non tracciate).
   **Secondo giro (`gates/GATE_B_2026-09-25_round2.md`, su `79cf0fd`): BLOCK per la sola verifica delle
   prestazioni** — punteggi 4/4/4/3/4/4/3/4/4/4 (da 3/4/4/3/4/4/3/3/3/3), i quattro test corretti; chiuse
   1, 2, 3, 4, 5, 8, 10, 11; parziali 6 (ingresso LCP 2,71–2,84 s con gzip; console 1,8–2,1 s; CSS 103–106 KB),
   7 (porta intera, non il glifo: decisione del CD), 9 (accettata la rimozione del «page enter»), 13; aperta
   12 (copy). Sette difetti nuovi (14–20), sei corretti lo stesso giorno: (14) il testo digitato passava
   sotto il controllo della password — la regola dell'ingresso batteva quella della cascata a pari
   specificità: `padding-inline-end` ridetto in `entrance.css` a specificità maggiore; (15) `padding` della
   lista del menu account 8/8/8/0 per `ul[role="list"]` di `base.css`: selettore più specifico; (16) vetrina:
   `id="wrap_"` vuoto due volte (`id_for_label` di un RadioSelect è vuoto → `auto_id`), barra compatta e piede
   campione nel flusso (`--sample`), test `test_no_element_id_appears_twice` verde; (17) barra inferiore a
   esattamente `--bottom-bar-h` (era 58,8 px con etichette su due righe): piede del wizard e barra
   dell'azione ora la toccano senza sormontarla; (18) **un solo anello con un solo compagno**: l'alone di 5 px
   dei bottoni V3 e il compagno `--min-2` ceduti al compagno globale; sulla rail e nel cassetto l'accento
   scuro con la terra della rail; (19) striscia d'aiuto a raggio `lg` quando va a capo (< 80rem). **Al
   committente**: (19) il glifo arco+gradini al posto della porta intera sotto 1024 (CD §3.3); (20) i font
   dell'ingresso arabo ≈ 509 KB (Noto Naskh + Plex Arabic in tre pesi + Newsreader) contro i 200 KB proposti —
   la pila tipografica araba è una decisione; (6) l'HTML non compresso (nessun `GZipMiddleware`: BREACH) e la
   concatenazione dei fogli restano le leve per i 2,5 s dell'ingresso.
10. Mes Documents V4 · 11. Dashboard Persona V4 — **costruiti** (`documents/partials/register.html` come
   DocumentCollection con HealthStrip, segmentato in `?état=`, ricerca in pagina e DocumentRow a sette zone;
   `portal/documents.html` con la testata di workspace e l'azione primaria di deposito; `portal/dashboard.html`
   a pannelli — ContextHeader, «Prochaine étape» L2 con bordo a gradiente e ResponsibilityBar, «Dossier» con
   il misuratore a tacche, JourneyRail, «Mes documents» con HealthStrip e le tre pièce più urgenti, scadenze
   con urgenza, comunicazioni, Academy; quattro componenti nuovi: `glyph`, `document_row`, `health_strip`,
   `journey_rail`; `static/css/v4/workspace.css`; lato Python: conteggi per stato, urgenza, salute, glifo
   dell'attore, azione primaria, filtro nell'URL, tacche reali). Da misurare in Chrome e da sottoporre al
   revisore (gate C). Mappatura dei registri dei chip: resta quella di `apps/core/chips.py` (V3, motivata),
   non quella proposta in `CREATIVE_DIRECTION.md` §3.5.4 — differenza da decidere dal Creative Director.
   Non costruito, e detto: il caricamento flagship (sta sulla pagina della pièce, gate D), il riordino FLIP
   delle righe al filtro (il filtro è una navigazione), il popover con la cronologia inline (il menu porta
   alla pagina della pièce).
   **Misurato in Chrome il 25/09** (`docs/qa/chrome/design-v4/after/08_dashboard_*.png`, `09_documents_*.png`, tre
   account reali di `ile_qa`: `qa-person` con fascicolo e CGU non accettate, `qa-doc-person` con fascicolo e CGU
   accettate, `qa-fresh-person` **creato il 25/09 senza fascicolo** perché nessun account di prova ne era privo).
   Sette difetti trovati misurando e corretti: (1) il cruscotto **saltava l'intero workspace** per una persona
   senza fascicolo — quattro test del portale lo dicevano (`test_dashboard_for_a_fresh_account_shows_empty_states_not_numbers`
   e tre altri): ora il pannello «Votre prochaine action» sta da solo con la frase e «Commencer le questionnaire»,
   le regioni vuote sono una frase con l'azione in linea; (2) il pannello «Mon compte» (identità, ultimo accesso,
   Profil, Sécurité, Back-office per lo staff) era stato perso: ripristinato come quinta riga; (3) la riga
   compatta del cruscotto era la riga intera schiacciata in 360 px: ora identità · stato · scadenza; (4) il
   menu della riga (`popover` nativo con `margin: 0`) si apriva in alto a sinistra del viewport: ora posizionato
   accanto al bottone da `console.js` (misurato: bordo destro = bordo destro del bottone a 1440, specchiato in
   RTL, dentro il viewport); (5) due regioni vuote usavano l'EmptyState tratteggiato che la regola del 21/09
   vieta: ora frase + link; (6) la legenda della HealthStrip e il controllo segmentato dicevano le stesse sette
   cose due volte a una riga di distanza: il controllo porta il punto di registro, la striscia tiene barra e
   parole; a 390 il controllo scorre in una riga; (7) il misuratore stampava «0 sur 0» per un fascicolo senza
   elementi: non stampato. La testata prescritta dell'accesso (persona senza fascicolo) usa la testata di
   workspace, non il `page_header` serif. I file depositati tornano sul cruscotto come «Derniers dépôts» sotto
   le pièce (una pièce non è un file). Quattro msgid recuperati dallo storico (`Back-office`, `Dernière connexion :`,
   la frase della checklist, `Commencer le questionnaire`) e uno nuovo (`Derniers dépôts`), tradotti in it/en/ar.
   Test: 346 del portale e dei documenti verdi sulla corsia 4; 320 veloci verdi. Pronto per il revisore (gate C).
   **Revisione indipendente del 25/09 (`gates/GATE_C_2026-09-25.md`, su `d324235`): BLOCK** — punteggi
   3/3/4/3/3/3/4/3/3/3, i quattro test corretti, AFTER superiore sul cruscotto ovunque e su Mes pièces a
   1440/1280/390 (non a 1024); due verifiche binarie «no»: il **verde di verdetto** nella HealthStrip e nei
   punti del segmentato (`conforme` in `--ok-700`, `azione` nell'accento) e le prestazioni. Dieci correzioni;
   applicate e misurate lo stesso giorno: (1) i sei registri della striscia e dei punti con **le marche dei
   chip** (conforme = inchiostro, neutro/attesa = inchiostro 2, azione = pending, rifiuto = err, nullo =
   hairline-strong) e un canale **non cromatico** — tratteggio a 45° per «attesa», punti per «rifiuto»
   (token `--texture-hatch` / `--texture-dots`), bordo tratteggiato/doppio/punteggiato sui punti del
   controllo; test `test_no_register_is_painted_with_the_verdict_green_or_the_accent`; (2) la griglia della
   riga decisa dalla **larghezza del foglio** (container query): sette zone da 1100 px di foglio (misurate
   intere a 1128 con la rail aperta a 1440), cinque zone con l'azione sulla propria riga sotto, scheda sotto
   700; chip su una riga; l'etichetta della porta delle CGU abbreviata in «Accepter les Conditions» con
   l'`aria-label` intero; (3) la preferenza della rail applicata **prima del primo frame** da uno script
   classico esterno (`static/js/rail-pref.js`, in testa al `<body>` della console): CLS con `ile.rail = open`
   misurato 0 a 1024 e 1280 su cruscotto e Mes pièces (prima 0,19–1,47); (4) la metà inferiore della pagina
   pilota come Table V4 in Plex, nomi dei file come link senza sottolineatura, «Registre complet» e «Déposer
   un fichier hors exigence» come bottoni LINK, il componente `notice` in Plex (correzione di sistema:
   0 serif e 0 sottolineature misurati sotto il registro); (5) al tocco `.btn--sm`, `.btn--link`, `.seg__link`
   a 44, area 44 sul bottone del menu di riga (`elementFromPoint` verificato), link dei file a 44;
   (6) colori forzati: linea del rail `CanvasText`, bordo sul segmentato, `Highlight` sulla voce corrente,
   punti bordati, trame sui segmenti (misurato); (7a) un solo PRIMARY per schermo — quello della testata
   (cruscotto, fascicolo, impresa); sul fascicolo sotto 64rem la barra appiccicosa porta l'azione e la
   testata la nasconde; (7b) «Bloqué» non sulle righe compatte; (7c) il lato del percorso come parola
   («Maroc» sulla prima tappa, «Italie» alla frontiera); (7d) linea del rail `--hairline-strong`; (7e)
   `align-items: start` sulla griglia: un pannello vuoto non si stira sul vicino; (7f) ricerca a fine riga
   sulla stessa riga del controllo da 64rem; (7g) a 390 il controllo scorre con la barra sottile visibile;
   (8) la ricerca annuncia «Pièces affichées : n / total» in una regione `role="status"` a digitazione
   ferma (misurato: «1 / 7» per «casier»). **Prestazioni, finalmente con sessione e compressione**
   (8772 su `ile`, sessione coniata su quel database, slow 4G, CPU ×4): cruscotto LCP **2,43 s**, Mes pièces
   **2,0–2,1 s**, CLS 0, CSS 108–110 KB gzip, JS 38 KB, font 199–214 KB — sotto i 2,5 s; il CSS supera di poco
   il budget proposto (100 KB): la concatenazione della cascata e i fogli `hero`/`wizard` fuori dalla
   console restano la leva, decisione del CD. **Da decidere, registrato**: (10a) la mappatura dei registri —
   parere del revisore: tenere `chips.py` ed emendare CD §3.5.4; (10b) il segmentato come `nav` di link senza
   cursore a molla (una pagina per filtro: deviazione da DS §8.14, scritta qui); (10c) la testata prescritta
   «ESPACE RÉSERVÉ» in francese su `/ar/` per chi non ha fascicolo (stessa decisione del gate A); (10d) la
   vetrina `/_design/` completata con controllo segmentato, testata di contesto col misuratore, barra di
   responsabilità, testata di workspace, regione vuota; (9) il carattere del lock-up. **Non chiuso**: il
   responsabile per tappa del JourneyRail (nessun dato lo porta: `JOURNEY_STEPS` non ha un attore).
   **Gate D — fascicolo e «Ma situation», costruiti il 25/09** mentre il gate B era in revisione (una sola
   scheda Chrome: la misura segue). Fascicolo (`templates/cases/detail.html`, `apps/cases/presenters.py`,
   `components/case_timeline.html`, `journey_rail.html` con la variante `descriptive`, `health_strip.html`
   con `bare`, stili in `v4/workspace.css`, barra di contesto in `console.js`): ContextHeader con eyebrow,
   riferimento mono, riga meta (objectif · chip · responsabile con glifo · misuratore a tacche) e UNA azione;
   allo scroll una barra compatta in vetro sotto la barra della console; colonna 8 con le quattro domande di
   §48 nell'ordine — JourneyRail verticale con la **data reale** in cui ogni tappa è stata raggiunta (dal
   registro di audit: apertura e transizioni; nessuna data per le tappe non raggiunte), «Prochaine étape» L2,
   la checklist come Table semantica con la barra di salute e il cambio di stato via modulo di pagina come
   prima, gli intervenants con glifo, autorizzazione e validità; inspector 4 appiccicoso con la **Timeline
   letta dal registro di audit** (aperture, transizioni, pre-valutazioni, incarichi, righe — l'attore come
   tipo, mai un nome), la pre-valutazione con regole, data e fondamenti, comunicazioni e scadenze; per lo staff
   il modulo di transizione in coda; sul telefono una barra appiccicosa con l'azione primaria sopra la
   navigazione inferiore. «Ma situation» (`templates/portal/situation.html`, `components/option_cards.html`,
   `components/wizard_stepper.html`, `static/css/v4/wizard.css`, `static/js/src/situation.js`):
   lo stesso modulo in un solo POST (§89), tre domande chiuse passate da `<select>` a radio (stessi nomi,
   stessi valori), Stepper verticale coi nodi pieni secondo `PersonProfile.answered()`, una domanda per volta
   su pannello L2 con la luce FOCUS dietro, OptionCard su input nativi, piede appiccicoso in vetro con
   «Précédent» · «Continuer» e il submit sempre presente; senza script le otto domande si susseguono.
   **Non costruito, e detto**: le sezioni `<details>` del telefono (un comportamento in più da imparare su una
   sola larghezza), il `view-transition-name` condiviso fra testata e barra (due elementi con lo stesso nome
   nello stesso istante: vietato dalla specifica), i glifi delle OptionCard (nessuna opzione ha un glifo
   onesto), il wizard pubblico `orientation/_step.html` e la pagina risultato (§3.7, secondo tempo). **Da
   decidere**: la frase «n question(s) renseignée(s) sur 7» conta i sette campi letti dalle regole mentre il
   modulo pone otto domande (la riconoscibilità del titolo non è letta da nessuna regola: `PROFILE_FIELDS`)
   — lo Stepper mostra le otto, il conteggio resta quello del profilo.
   **Misurato in Chrome il 25/09** (`docs/qa/chrome/design-v4/after/10_file_*.png`, `11_situation_*.png`;
   `qa-person` con fascicolo E46E03B461, `qa-doc-person` con un'azione successiva collegata): fascicolo a
   1440/1280 griglia 8/4 con inspector appiccicoso a 128 px, testata con eyebrow, riferimento, chip,
   responsabile, misuratore a 5 tacche; barra di contesto in vetro a 56 px che compare a 600 px di scroll e
   sparisce al ritorno; JourneyRail verticale con **due date reali** (apertura e stato corrente, dal
   registro di audit) e la tappa raggiunta piena; Timeline di tre eventi reali (apertura, pre-valutazione,
   nuovo stato) con l'ultimo nodo acceso; Table 5 × 5 con tre moduli di riga (le sole righe che la persona
   può cambiare); a 768/390 una colonna, la tabella come schede etichettate, la barra dell'azione primaria a
   56 px sopra la navigazione inferiore (misurata con `qa-doc-person`: «Continuer» in testata, nel
   pannello, nella barra compatta e nella barra del telefono). «Ma situation»: 8 domande, una visibile con
   lo script, tutte senza; Stepper 8 nodi, 0 pieni (profilo vuoto: le tre scelte «je ne sais pas encore»
   / «non précisé» sono selezionate nel registro neutro, non come risposte); piede appiccicoso 64 px
   (a 390 sopra la barra inferiore); «Continuer» → domanda 2 con focus, 8/8 → solo «Précédent» e il submit;
   OptionCard selezionata = bordo accento; senza script 8 domande visibili e il solo submit. Tre difetti
   trovati misurando e corretti: il pannello «Prochaine étape» conservava lo span a 8 colonne del cruscotto
   (1 356 px di pagina a 1280 → `grid-column: auto` nel fascicolo); la luce FOCUS sbordava del 6 % a 390
   (→ `inset-inline: 0`); l'esito della pre-valutazione era nel display serif V2 (→ Plex 20/28 600 nei
   pannelli, anche sul cruscotto); in più la fascia V2 del fascicolo non compare su «Ma situation».
   Pronto per il revisore (gate D).
   **Revisione indipendente del 25/09 (`gates/GATE_D_2026-09-25.md`, su `edd2ae7`): BLOCK** — punteggi
   2/3/4/3/2/3/4/3/2/3, test «2026» NO; due delle tre cause bloccanti erano **regressioni dell'ultimo commit**,
   entrate dopo le misure del costruttore: (1) le etichette del JourneyRail col nome del lato finivano nella
   colonna del nodo (28 px, nove righe) — mancava `grid-column` (gate C 7c); (2) la barra dell'azione del
   telefono fuori schermo (y 2 848 su 844) perché il `translate` dell'ingresso `ws-in` rendeva il workspace
   contenitore del `position: fixed`. Dodici correzioni; applicate e misurate lo stesso giorno: (1)
   `grid-column: 2` sull'etichetta; sul binario orizzontale il nome del lato su una riga propria sopra i nodi
   (righe 16/28/auto/auto: i sette nodi restano allineati); (2) `ws-in` in sola opacità — il viaggio di 8 px
   del pattern 1 è una deviazione, scritta qui; (3) l'inspector con `max-block-size` sul viewport e scorrimento
   interno; (4) un solo PRIMARY: nel modulo guidato il submit è SECONDARY finché «Continuer» è visibile e
   PRIMARY sull'ultima domanda; sul fascicolo «Enregistrer l'état» SECONDARY e il `<select>` senza stato
   preselezionato (voce vuota «Nouvel état», `required`); (5) il default neutro («Je ne sais pas encore»,
   «Non précisé») senza spunta; (6) lo scambio del wizard senza i due pannelli insieme (l'arrivante è
   invisibile finché il partente non è uscito), il «draw» verticale con `rail-draw-y` (`scaleY`) e il
   verticale anche sotto 64rem; (7) contatore su una riga, piede 4 px sopra la barra inferiore reale,
   `select` 44 al tocco, Stepper come riga di nodi sul telefono (la domanda comincia in vista); (8) la
   regione della tabella senza `overflow` (la testata si attacca), le colonne «Fondement» / «Échéance»
   omesse quando nessuna riga le riempie, nessuna fermata `tabindex` inutile; (9) colori forzati sulla
   Timeline (nodo e spina) e **un solo anello di focus**: i nomi V2 dell'anello ripuntati al token V4
   `--accent-ring` in `v4/tokens.css`; (10) `case_timeline.html` accettato dalla guardia dei registri, il
   modulo di stato con gli Input V4, il riferimento in mono dentro l'h1 (la pretesa del README è ora vera),
   «n sur m éléments complétés» una sola volta (nella testata), eyebrow 11/16; (11) le domande non correnti
   nascoste **prima** dello script (`html.js .wiz:not(.wiz--guided)`), il resto come per A–C; `hashchange`
   gestito. **Da decidere, registrato**: (12a) il modulo di stato del fascicolo lo vede anche il
   proprietario (la policy lo permette; la documentazione lo dice dello staff) — chi lo vede e con quale copy;
   (12b) CD §3.6.3 «chip--seal e frase informativa bloccata» sulla pré-évaluation: non costruiti (nessuna
   autorità la emette: nessun sigillo; la frase è nella rationale come dato) — deviazione scritta; (12c) i
   nodi raggiunti pieni dell'accento = posizione, non verdetto (DS §10); (12d) vetrina completata; (12e)
   l'ambiente 8772 ricostruito con `collectstatic --clear`. Ancora aperto: «sur 7» sotto otto domande.
   **Secondo giro (`gates/GATE_D_2026-09-25_round2.md`, su `89d0428`): BLOCK per la sola verifica delle
   prestazioni** — punteggi 3/4/4/4/4/4/4/3/4/4 (da 2/3/4/3/2/3/4/3/2/3), test «2026» ora SÌ; con sessione e gzip
   fascicolo LCP 2,0–2,1 s e «Ma situation» 1,8–2,0 s, CLS ≤ 0,001; chiuse 1–7 e 10; parziali 8, 9, 11, 12.
   Quattro difetti nuovi (13–16), corretti e misurati lo stesso giorno: (13) **regressione della correzione 6 del
   gate E**: la soglia delle schede a 880 px di regione valeva per ogni tabella e la checklist del fascicolo
   (regione 690–774 px nella colonna 8) non era mai una tabella — ora le schede scattano sotto 640 px per ogni
   tabella e sotto 880 per la sola Table dei bisogni (cinque colonne larghe); (14) il binario orizzontale del
   cruscotto aveva perso lo scaglione (la regola a specificità maggiore azzerava i ritardi): ritardi ridetti alla
   stessa specificità; (15) `#case-reason` portava ancora l'anello V2 di `components.css`: l'anello della cascata
   alla specificità di quella regola; (16) l'URL segue lo Stepper (`history.replaceState`) e gli stili in linea che
   Motion lascia dopo lo scambio sono rimossi a fine transizione; a colori forzati anche la linea delle tappe
   raggiunte è `CanvasText`. **Aperti, e detti**: (10f) l'aiuto a 13/20 (il CD dice 14/20: nella scala della
   console non esiste 14); (9) la voce «sur 7» sotto otto domande; (12c) la nota sui nodi raggiunti sta nel DS
   2026 §10 (`journey_rail.html`), non in un «DS §10» generico come scritto sopra.
   **Gate E — cruscotto impresa, costruito il 25/09** (`templates/companies/dashboard.html`,
   `companies/partials/need_table.html`, `apps/companies/services.py` — voci della rail con glifo e gruppo
   «Espace entreprise» —, stili in `v4/workspace.css`), mentre il gate C era in revisione; misura in Chrome a
   seguire con `qa-company` (Cantiere Adriatico S.r.l., verificata, quattro bisogni in quattro stati).
   ContextHeader con eyebrow «Entreprise», ragione sociale come h1, riga meta (la verifica come parola col suo
   registro — `chip--seal` solo quando è pronunciata —, settore, stabilimento, «n besoins en cours» in cifre
   tabellari) e UNA azione (quella del passo successivo: «Ouvrir le besoin», «Compléter le besoin», «Créer un
   besoin»); riga 1 8/4 con «Votre prochaine action» L2 (ResponsibilityBar con glifo tratteggiato quando
   nessun intervenant è designato, `building` quando tocca all'impresa) e «Mon entreprise» L1 (fatti su due
   colonne, glifo `building` in disco 40, la nota sulla verifica, il link all'identità); riga 2 la Table
   semantica dei bisogni — Besoin (titolo · riferimento mono · territorio · settore · n profils) · État ·
   Responsable (nome reale o «aucun intervenant désigné» col disco tratteggiato) · Mis à jour le · «Ouvrir le
   besoin» —, testata appiccicosa, schede sotto 64rem; riga 3 Communications a tutta larghezza. Senza impresa:
   testata di workspace col testo esistente e il passo «Déclarer mon entreprise». Nessuna estetica da
   marketplace: nessuna persona, nessun conteggio di talenti, nessuna fotografia. **Non costruito, e detto**: il
   pannello «Formation liée» (§3.8.4): nessun dato lega una formazione a un'impresa in questa applicazione;
   la pagina «Mes besoins» e le altre del workspace impresa restano V2 (propagazione). Test: 97 dell'app
   `companies` verdi, 250 veloci verdi. **Misurato in Chrome il 25/09** (`docs/qa/chrome/design-v4/after/13_company_*.png`,
   `qa-company`): un difetto trovato misurando e corretto — il workspace impresa non portava la classe
   `console` del corpo (`base_companies.html`): rail sovrapposta, griglia collassata a 168 px; dopo la
   correzione, a 1440 «Votre prochaine action» 744 px, «Mon entreprise» 360, la Table dei bisogni 1128 con 5
   colonne e 4 righe (Brouillon/attesa, Transmis/neutro, En cours d'examen/neutro, Pris en charge/neutro),
   tre «aucun intervenant désigné» col disco tratteggiato e un intervenant reale; sigillo `chip--seal` sulla
   verifica pronunciata; a 768 e 390 una colonna e le righe come schede; rail con glifi e gruppo «Espace
   entreprise». Pronto per il revisore (gate E).
   **Revisione indipendente del 25/09 (`gates/GATE_E_2026-09-25.md`, su `747bcc2`): BLOCK per meccanica del
   modello** — punteggi 3/4/4/4/3/4/4/3/3/3 (sui soli punteggi sarebbe CONDITIONALLY_READY), i quattro test
   corretti; una verifica binaria «no»: l'indicatore di focus sulla barra in vetro (1,03 : 1, l'outline V2 su
   navy ereditato dalla classe `portal-bar`), e l'AFTER non superiore a 1024 con la rail aperta. Dieci
   correzioni; applicate e misurate lo stesso giorno: (1) la barra inferiore del telefono con le quattro voci
   del workspace impresa + «Menu» (`navigation()` segna `bottom`); (2) l'anello di focus della cascata sulla
   barra di contesto e sulla lingua corrente (correzione di guscio, vale per tutta la console); (3) glifi per
   `authorised_actor` (`handshake`) e `project_team` (`institution`): l'intervenant designato non porta più il
   disco di «nessuno»; (4) la testata appiccicosa della tabella sotto la barra della console (`--ctx-h`) e
   sotto la barra compatta del fascicolo quando è accesa (`has-ctx-bar`); (5) i fatti su due colonne solo
   quando il pannello le contiene (container query da 480 px), `overflow-wrap` sui valori, la verifica detta
   due volte (chip della testata + nota) e non tre; (6) le schede della tabella decise dalla larghezza della
   **regione** (container query a 880 px), non del viewport; (7) le schede disegnate da un solo foglio: le
   regole V2 di `portal.css` (etichetta «BESOIN», 48 px per cella) sovrascritte a specificità maggiore;
   (8a) testata su una riga (`white-space: nowrap`), (8c) stato hover del bottone LINK, (8d) titolo del bisogno
   15/24, (8f) `.empty` nel pannello nella faccia della console; (9) **il pattern «page enter» rimosso**: la sua
   opacità 0 → 1 faceva cadere l'LCP sullo skip-link (misurato dal revisore) — la console arriva completa,
   deviazione da DS §7 pattern 1 scritta qui e in DS §12. **Non chiusi, e detti**: (8b) l'ombra di hover sulle
   righe di una tabella `border-collapse` non si disegna — deviazione da DS §8.23; (8e) «Rovigo, IT»: il paese è
   un codice ISO nel modello, un nome per lingua è una decisione di dati; (10b) le tassonomie `Sector` /
   `Territory` hanno etichette fr/it soltanto: sulle pagine en/ar restano in francese — decisione di dati;
   (10a) la deviazione «Formation liée» va riportata in CD §3.8 dal Creative Director; (10c) vetrina completata
   con i fatti dell'impresa e la Table dei bisogni (quattro righe, un intervenant designato).
   **Secondo giro (`gates/GATE_E_2026-09-25_round2.md`, su `baaf148`): BLOCK per la sola verifica delle
   prestazioni** — punteggi 3/4/4/4/4/4/4/3/4/4 (da 3/4/4/4/3/4/4/3/3/3), i quattro test corretti, l'AFTER
   superiore anche a 1024 con la rail aperta; il «no» sul contrasto del focus è diventato «sì» (anello 3,91 : 1
   sul vetro); resta il «no» sul CSS (107,5 KB gzip contro i 100 proposti) mentre LCP 1,8 s e CLS 0,001.
   Chiuse 1, 2, 3, 4, 8; parziali 5 (referente su tre righe a 1024: dato), 6, 7, 9, 10. Due difetti nuovi
   (11–12) e due parziali, corretti e misurati lo stesso giorno: (11) «Nouveau besoin» su una riga a 390
   (`nowrap` sui bottoni della testata di pannello); (12) i link del piè di pagina della console con l'anello
   della cascata e il suo compagno (l'alone V2 di `v2/shell.css` era il quarto stile di anello della pagina);
   (6) il titolo del bisogno prende due quinti della riga da tabella (misurato 40 % a 1440 e 1280 aperta,
   righe 68 a rail chiusa) e la larghezza intera da scheda; (7) le schede con interlinea di cella ridotta (misurate 262–286 px a 390 contro i ≤ 260 chiesti: cinque celle etichettate, altezza data dai dati).
   **Registrato**: (3) i glifi degli attori — `handshake` e `institution` compresi — sono elencati nel DS 2026
   §10 (`glyph.html`); (9) la nota sul «page enter» rimosso sta in DESIGN_SYSTEM_2026 **§12 Motion** (non nel
   DS V4); (10) CD §3.8.4 dice già «se dati»: nessuna deviazione da scrivere per «Formation liée»; (8e) e le
   etichette delle tassonomie restano decisioni di dati.
   **Gate C, secondo giro (`gates/GATE_C_2026-09-25_round2.md`, su `79cf0fd`): BLOCK per la sola verifica delle
   prestazioni** — punteggi 4/4/4/3/4/4/4/4/4/4 (da 3/3/4/3/3/3/4/3/3/3), i quattro test corretti, l'AFTER
   superiore a ogni larghezza; chiuse 1, 2, 3, 4, 6, 7a–f, 8; parziali 5, 9 (con sessione e gzip: LCP
   1,78–1,86 s, CLS ≈ 0, JS 36 KB, ma CSS 106–108 KB e font 218 KB), 10; aperta 7g. Sei difetti nuovi (11–16),
   tutti corretti e misurati lo stesso giorno: (11) a colori forzati ogni registro della striscia è `Highlight`
   e le due trame restano distinte (tratteggio per «attesa», punti per «rifiuto»); (12) la riga del
   segmentato che scorre **sfuma alla fine** (token `--mask-fade-end` / `-rtl`) ovunque la regione dei
   controlli sia più stretta delle otto voci; (13) il link del file sopra la glossa (`z-index`) con 44 px al
   tocco; (14) **un solo compagno dell'anello** su ogni controllo del workspace (l'alone di 5 px dei fogli V2/V3
   ceduto al compagno di 2 px) e l'anello anche sulla voce corrente del segmentato; (15) le azioni di riga
   SECONDARY — il PRIMARY di Mes pièces è quello della testata («Remplacer/Déposer la pièce» e la porta delle
   CGU in riga sono secondarie); (16) il controllo non va mai a capo dentro il proprio binario: la ricerca
   resta a fine riga finché le otto voci ci stanno accanto (1440) e va sotto quando non ci stanno (1280 con
   la rail aperta: il controllo prende la riga intera, nessuno scorrimento) — deviazione da 7f «a fine riga»
   limitata al caso in cui non c'è posto. I quindici ritardi di scaglione sono multipli del token
   `--motion-stagger` (10e). **Al CD**: CD §3.5.4 e DS V4 §8.14 prescrivono ancora la mappatura dei registri
   e il cursore a molla che il codice non segue — le deviazioni sono scritte qui e vanno recepite o respinte
   dal Creative Director.
12. revisione in Chrome · 13. revisione indipendente · 14. correzioni · 15. **solo dopo il PASS**,
propagazione: 16. Fascicolo · 17. Wizard · 18. Company · 19. Academy · 20. Forum · 21. resto ·
22. mobile · 23. RTL · 24. accessibilità · 25. prestazioni · 26. red team · 27. QA finale

## 5. Regole nuove che valgono da subito

- **Il freeze non è una fase conservatrice** (chiarimento delle 20:58). Le scelte visive precedenti
  — art direction editoriale, serif dominante, folio/register, palette, bottoni V3, sidebar, navbar,
  sistema di superfici, livello di moto, il rifiuto di vetro/gradienti/arrotondamenti, l'impostazione
  minimalista — **non vincolano più** e possono essere sostituite per intero. Restano assoluti solo:
  testi legali, formulazioni vietate, responsabilità degli attori, workflow, IAM, privacy, sicurezza,
  accessibilità, prestazioni, Django come core, asset di marca ufficiali, nessuna falsa identità
  ministeriale, nessuna funzione inventata.
- **Autorizzati espressamente, se usati professionalmente:** gradienti sofisticati, sfondi a strati,
  luce mesh/radiale, blur, vetro controllato, superfici arrotondate moderne, ombre più ricche, hover
  premium, Motion avanzato, SVG animato, effetti legati allo scroll, immagini moderne, pannelli
  premium, bottoni sofisticati, chip moderni, cassetti, overlay, command/search UI, app shell
  moderna, più profondità. Priorità estetica: **credibilità istituzionale + prodotto digitale
  premium 2026 + impatto visivo + moto + usabilità.**

- **NO USER VALUE = REMOVE** (§5): coordinate geografiche, «svg», «Suspendre le mouvement» e ogni
  etichetta pseudo-tecnica spariscono dalla home nel passo 8, salvo funzione reale e comprensibile.
- **Istituzionale ≠ editoriale** (§4): il serif e il registro tipografico restano per le pagine
  lunghe di contenuto; cruscotti, workspace documenti, wizard, fascicolo, B2B, autenticazione e
  strumenti operativi usano una tipografia UI digitale (§87–88).
- Nessuna feature finta per fare effetto (§90): niente grafici, KPI, mappe, coordinate o dati
  animati che non siano dati reali del prodotto.
- Il lavoro si guarda presto e in Chrome visibile (§70, §84): prima HOME, LOGIN, DASHBOARD
  PERSONA, MES DOCUMENTS; poi il resto.
