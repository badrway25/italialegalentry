# GATE A — Homepage (hero) + Navbar · scorecard del 26 settembre 2026 — **quinto giro**

Compilata sul modello `docs/design-v4/GATE_SCORECARD_TEMPLATE.md` (§71–78 della direttiva). Regole
applicate: **nessuna media** (§74); **l'implementatore non vota** (§72); ogni punteggio cita ciò che il
revisore ha **osservato in Chrome visibile** (§70) — Google Chrome 153, CDP 9222, `scripts/cdp.py`, una sola
scheda, sonde sequenziali, `Network.enable` + `Network.setCacheDisabled` in testa a ogni sonda. Le misure sono
`getBoundingClientRect` / `getComputedStyle` / `elementFromPoint` / `getBBox` / `getPointAtLength` / `Range.getClientRects`
/ `performance.getEntriesByType` / `PerformanceObserver` (LCP, layout-shift, longtask, event, paint, installati con
`Page.addScriptToEvaluateOnNewDocument`) / campionamento a ogni `requestAnimationFrame` (storia per fotogramma di vie,
nodi, uscite, traccia, gradini, chiave, fotografia, titolo, legenda) / `document.getAnimations()` / eventi reali
(`Input.dispatchMouseEvent`, `Input.dispatchKeyEvent` con `Emulation.setFocusEmulationEnabled`,
`Emulation.setDeviceMetricsOverride` con `mobile: true` e `screenOrientation` per le rotazioni,
`Emulation.setTouchEmulationEnabled`, `Emulation.setEmulatedMedia` per reduced-motion e colori forzati,
`Emulation.setScriptExecutionDisabled` per lo stato senza JavaScript, `Network.emulateNetworkConditions` 150 ms /
1,6 Mbit/s / 750 kbit/s + `Emulation.setCPUThrottlingRate` 4 per il 4G lento) e letture di pixel con Pillow sulle
catture del revisore. Le catture di questo giro stanno in `docs/qa/chrome/design-v4/after/review_a5/` (prefisso `a5_`,
ignorate da git: `.gitignore:30`); i percorsi sono relativi alla radice del repository. Ogni numero di questo documento
è una misura del revisore presa in questo giro (26/09, 08:36–09:05); i numeri del README e dei giri precedenti sono
citati solo per confronto.

Nota sulle misure: la scheda riportava `devicePixelRatio` **1** (finestra 1905 × 1012, interno 1889 × 861, 62 rAF in
500 ms, `visibilityState: visible`); tutte le emulazioni con `deviceScaleFactor: 1`, azzerate a fine sonda.

Nota sulla scheda: all'inizio i target di 9222 contenevano **una** pagina, `http://127.0.0.1:8771/fr/espace-reserve/`,
autenticata come `qa-person`. Le sonde su 8770 e 8772 l'hanno disconnessa da 8771 (cookie per host); alle 08:58 il
revisore l'ha ri-autenticata con `scripts/qa_chrome_signin.py` (sessione lato server, nulla digitato: «signed in as
qa-person@example.test», atterraggio 200 su `/fr/espace-reserve/`), ha fatto su 8771 le sole sonde del menu account e
del cassetto, e l'ha lasciata su `/fr/espace-reserve/` con il riassunto «qa-person» visibile.

Questo documento verifica, correzione per correzione, le correzioni del quarto giro (`gates/GATE_A_2026-09-25_round4.md`,
§6: 3 e 6 ancora aperte, 11–15 nuove), ciascuna contro il **suo** criterio di chiusura; poi cerca i difetti introdotti o
lasciati scoperti dalle correzioni, ri-assegna le dieci dimensioni, i quattro test e le verifiche binarie.

---

## 0. Identità del gate

| Campo | Valore |
|---|---|
| Gate | **A** |
| Superfici | Homepage pubblica `/fr/`: hero «il portico» (porta, quattro vie, legenda in vetro con didascalia, titolo, lead, CTA; uscite etichettate nella variante interim) + navbar (barra istituzionale con controllo lingua e accesso/menu account, testata, indicatore, mega-menu, cassetto con segmentato); `/ar/` (e `/it/`, `/en/` per le uscite) per RTL e lingue; la pagina d'accesso `/fr/compte/login/` e `/ar/compte/login/` (per la coreografia tolta); la vetrina `/_design/` |
| URL / account | **8770** (`ile`, fase 3 chiusa → variante **interim**: eyebrow, titolo editoriale, tre uscite etichettate, quattro voci); **8771** (`ile_qa`, fase 3 aperta → variante `phase3`, sette voci; `qa-person` per menu account e cassetto); **8772** (lo stesso codice di 8770 dietro WhiteNoise gzip) per ogni misura di prestazione. Verificato all'inizio: `v4/hero.css`, `v4/shell.css`, `main.js`, `js/dist/home.js`, `js/src/motion.js` serviti da 8770, 8771 e 8772 hanno lo stesso md5 dei file dell'albero (8772 con `Content-Encoding: gzip`); `js/dist/entrance.js` risponde **404** su 8770 e 8772; l'HTML servito porta i segni del commit (4 `<tspan>` nelle uscite di 8770, 4 `aria-describedby="hero-gloss-…"`, `lang="fr"` sui quattro gloss di 8771 `/ar/`, 0 riferimenti a `entrance.js` nella pagina d'accesso). |
| Commit sotto revisione | **d475749** (albero pulito: `git status` vuoto all'inizio e alla fine). Sulle superfici del gate, da 156db5f: `apps/pages/services.py` (`_route_path`: treccia fino a x 496, salita `C508 … 508 … 520` dentro l'arco, poi `H624`; `label_lang` / `text_lang`), `static/js/src/home.js` (coreografia d'ingresso tolta; stessa salita; uscite disegnate solo da 80rem; deriva della fotografia `translateY(0 → −18)`; lingua della didascalia), `static/js/main.js` (frecce della barra su link **e** chevron; `navOpener`; `placeDrawer` su `resize` e `ResizeObserver`; tolto il gestore `click` su `document` che chiudeva i pannelli), `static/css/v4/hero.css` (tratto pieno solo da 80rem; `.doorway { direction: ltr }`), `static/css/v4/shell.css` (chevron `inline-size: var(--hit-min)` su barre di cinque sezioni o meno, via `:has`; nota corretta), `templates/pages/home/_hero.html` (`lang` di riga e di gloss; commento), `templates/components/doorway.html` e `templates/allauth/layouts/entrance.html` (commenti; tolto lo script d'ingresso), `static/js/src/entrance.js` e `static/js/dist/entrance.js` (cancellati), `docs/design/DESIGN_SYSTEM_2026.md` (pesi dei fogli). |
| Revisione | **quinto giro** (quarto: `gates/GATE_A_2026-09-25_round4.md`, su 156db5f, BLOCK per la sola regola delle prestazioni; terzo: `…_round3.md`, su dd29168; secondo: `…_round2.md`, su d99f2bb; primo: `GATE_A_2026-09-25.md`, su c6f3503) |
| Implementatore (non vota) | Claude (sessione principale) |
| Revisore indipendente | agente separato (nessuna modifica a codice, template, fogli, script o test; nessun riavvio di server; nessun pacchetto installato; nessuna credenziale digitata; nessun modulo inviato; nessuna scheda aperta o chiusa). Due sole manipolazioni del DOM nella scheda, dichiarate: `#site-header.hidden = true` in `r5d_nojs_stage.py` (per fotografare il palcoscenico senza JavaScript, pagina ricaricata subito dopo) e `data-open` messo e tolto su un `<li>` per leggere l'ordine visivo di un pannello (`r7_mega.py`). |
| Data e ora della revisione | 26 settembre 2026, ore 08:36–09:05 (misure in Chrome); scorecard scritta subito dopo |

## 0-bis. Le correzioni del quarto giro — verifica una per una, contro il loro criterio

| # | Correzione (quarto giro) | Stato | Prova (misura o cattura) |
|---|---|---|---|
| 3 | Prestazioni — verifica binaria 9 | **PARZIALE** (invariata) | 8772, 1440 × 900, cache spenta, 4G lento + CPU ×4, due passate: **LCP 3 020 / 3 060 ms** — `image.doorway__img` (`doorway-800.webp`, 133 126 px²; candidato precedente uno `SPAN` del titolo a 1 920 / 1 708); FCP 1 920 / 1 708; DCL 3 199 / 2 925; load 3 758 / 3 439; CLS **0,0032 / 0,0032**; long task max **464** / 182 ms (9 / 8 task); 0 violazioni CSP. **Pesi** (identici nelle due): CSS **22 fogli, 99,4 KB gzip** (389,4 nudi); JS **8 file, 36,0 KB** (100,3); font **6 file, 356,1 KB** (Newsreader tondo 128,9 precaricato, Newsreader **corsivo 143,4**, Plex Sans 22,1 + 23,6 + 23,7, Plex Mono 14,4); immagini 5 file, 79,5 KB (foto 76,8, precaricata da 231 / 228 ms); HTML **43 783 byte non compresso**; **42 richieste**. Senza limiti: LCP 328 ms (la foto), CLS 0,0002. **INP-proxy deliberato** (seconda passata, CPU ×4: hover su una riga della legenda, clic sul chevron «Entreprises», Esc, hover sul secondario): evento più lungo **72 ms** (`pointerup` / `click` del chevron). I numeri del README (3 004 / 3 068, CSS 99,4, JS 36,0) sono ritrovati. Il budget resta «proposto al CD», non scritto in §68/DS; nessuna decisione su lock-up, corsivo, concatenazione, HTML compresso. CSS a **0,6 KB** dal tetto proposto. |
| 6 | Documentazione e decisioni | **PARZIALE** | **Chiusi**: (b) la lingua delle righe e dei gloss — HTML servito e pagina: su 8771 `/ar/` i quattro gloss portano `lang="fr"` (le righe nessun `lang`: la parola è nella lingua della pagina); all'hover di ciascuna riga la didascalia prende `lang="fr"` e calcola `direction: ltr`, righe di testo allineate a sinistra (x 111) nel pannello; su 8771 `/fr/` e 8770 `/ar/` nessun `lang` aggiunto, didascalia `ltr` / `rtl` come la pagina. (c) Il chevron: **44 × 44** su 8770 `fr` e `ar` a 1280, 1366, 1439, 1440 e 1600 (tre chevron), aria fra lock-up e lista **296,3 px** a 1280–1439 e **370** a 1440; su 8771 (`phase3`, sette sezioni) resta **24 × 44** a 1280–1439 e **28 × 44** a 1440–1600 con aria **31,4 / 31,7 px**; la nota di `v4/shell.css:336–339` porta ora i numeri misurati. **Aperti**: (a) le deviazioni da CD §3.1 / §4.4, ora **quattro** (lead non corsivo, titolo senza reveal, palcoscenico senza coreografia d'ingresso, deroga a 390 con la sua gamma di viewport) — scritte nel README (§4.8, «Quarto giro»), **non** in `CREATIVE_DIRECTION.md` (ultimo commit 6718f1a), nessuna firmata; (b) le traduzioni arabe dei testi prescritti su 8771 `/ar/` (lead, corpo, gloss francesi) restano una decisione del committente, con la terza colonna del mega-menu, le sette voci e il carattere del lock-up. |
| 11 | Il palcoscenico si vede completo, sparisce e si ridisegna | **CHIUSA** | Storia per fotogramma (a ogni rAF, dal primo) di `[data-doorway-exits]`, prima `.exit__label`, primo `[data-route-node]`, prima e ultima `[data-route-line]`, `[data-route-casing]`, `[data-doorway-trace]`, primo gradino, chiave, fotografia, titolo, legenda: **0** passaggi da visibile a nascosto e **0** cambi di trasformazione, su 8770 `/fr/` (418 fotogrammi), 8770 `/ar/` (422), 8771 `/fr/` (436), pagina d'accesso 8770 `fr` (227) e `ar` (226), 8771 `fr` (232), e su 8772 in 4G lento + CPU ×4 (929 e 1 010 fotogrammi nelle due passate: uscite, nodi e legenda compaiono a 1 799 ms dopo le vie a 1 665 per lo streaming dell'HTML, poi restano). Si muove solo la corrente (`stroke-dashoffset` 1 → 0,86 in 4 s, dal primo fotogramma). `document.getAnimations()` al caricamento: 4 `route-current` (CSS) + 3 animazioni legate allo scroll (fotografia, palcoscenico); sulla pagina d'accesso **0**. Nessun errore, nessuna risorsa mancante, 0 violazioni CSP (ascoltatori `error` in cattura, `unhandledrejection`, `console.error`, `securitypolicyviolation` installati prima del caricamento) su home e accesso in `fr` e `ar`; la pagina d'accesso servita non carica più alcuno script d'ingresso (tre `<script>`: `head.js`, `main.js`, `dist/shell.js`); `entrance.js` è citato solo in documenti storici (gate B, README). Commenti di `home.js`, `_hero.html`, `doorway.html`, `entrance.html` veri. Reduced-motion invariato (§1). Il prezzo — nessun disegno d'ingresso, contro CD §3.1 e §4.4.1 — è una deviazione da firmare (voce 6a) e pesa su Motion (§3). |
| 12 | Il cassetto non segue la testata dopo un ridimensionamento o una rotazione | **CHIUSA** | Clic reale su «Menu», poi `setDeviceMetricsOverride`, lettura dopo **1** e **2** rAF e a riposo, su 8770 **e** 8771: 390 × 844 → 844 × 390 (`mobile: true`, tocco, orientamento orizzontale): piede della testata **110**, cassetto 110, scrim 110 già al primo fotogramma; 844 × 390 → 390 × 844: 57 = 57 = 57; 600 → 1024: 98 = 98 = 98; 1024 → 600: 57 = 57 = 57; 768 × 1024 → 1024 × 768 (rotazione): 110 = 110 = 110. `elementFromPoint` al centro del lock-up e di «Menu» = **l'elemento stesso** in tutti i 20 casi (5 transizioni × 2 server × 2 elementi). Catture `a5_12_rotate_phone_8770.png`, `a5_12_resize_600-1024_8770.png`. (Con il tocco emulato la barra istituzionale è alta 45 px — bersagli da 44 con puntatore grossolano — e il piede della testata è a 110 invece che a 98: non è un effetto del commit.) |
| 13 | Il disegno delle uscite | **CHIUSA** sul criterio (con JavaScript) — lo stato senza JavaScript confluisce nel difetto nuovo **16** | (a) Tracciati vivi (`getAttribute('d')`), 2 000 campioni per via con `getPointAtLength`, a 1440 e 1280 in `fr`, `ar`, `it`, `en` (8770): `… C431 yIn, 431 yOut, 496 yOut C508 yOut, 508 exitY, 520 exitY H624`; fuori dal navy, dal lato delle uscite (4 000 campioni), due vie dirette a uscite diverse distano **≥ 98,6 unità** (criterio ≥ 6) e non si incrociano; **0 / 0 / 0 / 0** campioni nei riquadri `getBBox` ±1 dei `<tspan>` in tutte e otto le combinazioni. Le vie escono dall'arco a x 528,4 (y 200) e 531,2 (y 300); le due dirette a «Mobilité régulière» escono dal **piede** del navy (x 512–513, y 397) e corrono in piano a y 400. Dentro il navy le salite di «person» (→ Orientation) e «university» (→ Formation) si incrociano e restano a < 2,5 unità per y 338–370 (< 5 unità per y 315–375): è la treccia, dove CD §4.1 la vuole. Contrasto delle salite sul navy, sui pixel della cattura a 1440: **7,66–8,98 : 1** (7,66 dove l'alone della chiave schiarisce il fondo a y 268). Giudizio sulla cattura ingrandita (`a5_13_exits_8770_fr_1440_zoom.png`, `a5_13_risers_8770_fr_1440_zoom6.png`): le vie attraversano la soglia intrecciate, salgono a destra della chiave dentro l'arco e ne escono in piano verso tre nodi; niente più gomiti né incroci sulla pietra. Le due vie a y 400 corrono lungo il piede del navy (il casing lo tocca): si legge come la base della soglia, accettabile. (b) Con JavaScript, fra 64 e 80rem, le uscite non sono disegnate e le vie finiscono **a x 531** (bordo dell'arco) a 1024 e 1279, tratto a dissolvenza (`url(#route-fade-…)`) — `a5_13b_js_8770_1024_zoom.png`. **Senza** JavaScript (`setScriptExecutionDisabled`): il tracciato del server porta le vie a x 624; la dissolvenza nasconde il colore, ma i tre **casing** (navy a 0,75, 5 px) attraversano la pietra fino a 11 px oltre la porta, senza nodo (`a5_13b_nojs_8770_1024_stagezoom.png`) — il limite dichiarato dal builder, misurato; oggi è nascosto da un difetto più grave dello stesso stato (16). |
| 14 | Le uscite arabe fuori dal palcoscenico | **CHIUSA** | 8770 `/ar/`, `direction` calcolata `ltr` su `svg.doorway` e su `.exit__label`; `getBBox` dei `<tspan>`: x **599,9–636,4** a 1440 e 599,9–636,0 a 1280 (dentro i 640 del viewBox), sopra il nodo (y 178–195 per i nodi a 200/300/400) come in LTR; bordo destro delle etichette a **685,2** px contro la colonna del testo a **736,5** → **51,3 px** a 1440 (1280: 605,2 contro 656,5 → **51,3**); **0** campioni di via nei riquadri. Parole su una riga ciascuna, lette nell'ordine giusto («التنقل» sopra «النظامي»). `.doorway` è la sola classe dell'SVG dell'hero della home (grep dei template): la regola non tocca altro. Cattura `a5_13_exits_8770_ar_1440.png`, `…_ar_1440_zoom.png`. |
| 15 | Mega-menu: il chevron come vicolo cieco delle frecce | **CHIUSA** | Tasti reali, focus emulato, 1440. **8770 `fr`** (quattro sezioni, «Forum» senza pannello): da «Personnes» ↓ → «Voir l'espace», ↓ → «Votre parcours», ↓ → «Voir l'espace» (ciclo), ↑ → **«Personnes»** (la fermata che ha aperto); → × 4 = Entreprises, Forum, Projet, Personnes (giro completo, sezione senza pannello compresa), ← → Projet; ↑ e ↓ su una sezione senza pannello: nulla. Dal **chevron**: → → «Entreprises», ← → «Personnes»; ↓ → «Voir l'espace», ↓, ↑, ↑ → **chevron**; Esc → chevron, pannello chiuso. Nel pannello → / ← passano alla sezione vicina e chiudono. Esc sul link d'apertura a pannello aperto → chiude, focus resta. Tab fuori dal pannello → pannello chiuso. **8770 `ar`**: stesse sequenze speculari (← = sezione seguente, → = precedente, con giro). **8771 `fr`** (sette sezioni, quattro senza pannello): ↓ ↓ ↓ → «Voir l'espace», «Votre parcours», «Diplômes et titres»; ↑ ↑ ↑ → di nuovo «Personnes»; ↓ su «Universités & Formation» (senza pannello): nulla. **`scrollY` = 0 dopo ogni tasto** (in tutte le sequenze). **Mouse**: clic sul chevron «Entreprises» → pannello aperto, focus sul primo link; ↑ → chevron; → → «Forum»; secondo clic sul chevron → chiuso; clic sul titolo dell'hero (fuori) → chiuso. Ordine delle frecce = ordine di lettura: «Voir l'espace» è nella colonna di sinistra (x 93) e viene prima della colonna delle voci (x 533 → 945 per riga); in RTL la colonna di destra (x 966) prima. |

## 1. BEFORE / AFTER (§73)

| Vista | BEFORE | AFTER | Verdetto «materialmente superiore» (sì/no + una frase) |
|---|---|---|---|
| Desktop 1440 | `docs/qa/chrome/design-v4/before/01_home.png` (V2 interim); quarto giro `after/review_a4/a4_05_exits_8770_fr_1440.png` | `a5_13_exits_8770_fr_1440.png`, `a5_13_exits_8770_fr_1440_zoom.png` | **Sì.** La composizione del quarto giro senza i suoi due difetti di disegno: la treccia e le salite stanno nel navy, le vie escono dall'arco in piano verso tre nodi (≥ 98,6 unità fra uscite diverse), e il disegno non sparisce più al caricamento (0 fotogrammi nascosti). |
| Desktop 1280 · 1366 · 1439 | quarto giro `a4_05_exits_8770_fr_1280.png` | `a5_13_exits_8770_fr_1280.png`, `a5_6c_header_8770_1280_zoom.png` | **Sì.** Chevron 44 × 44 sull'interim con 296,3 px d'aria; sette voci su `phase3` con 31,4 px; indicatore allineato al link al decimo di px. Il ritmo della barra interim si è però fatto disuguale (54 px fra sezioni con chevron, 14 fra «Forum» e «Projet»: difetto 17). |
| Tablet 768 · 1024 | quarto giro `a4_06_legend_8770_1024.png` | `a5_13b_js_8770_1024.png`, `a5_14_home_8770_fr_768.png` | **Sì.** A 1024 le vie finiscono al bordo dell'arco, nessun tratto nel vuoto (con JavaScript); legenda 236 con righe da 44; a 768 azioni dentro la piega (1 007,8). |
| Mobile 390 | quarto giro `a4_04_home_8770_390_mobile.png` | `a5_14_home_8770_fr_390.png`, `a5_14_home_8771_fr_390.png` | **Sì** (invariato): interim 129,2 %, seconda azione a 816,8; `phase3` 124,1 %. |
| Stato interattivo (hover/focus/press/aperto) | quarto giro `a4_02b_*`, `a4_09_*`, `a4_10_*` | `a5_12_rotate_phone_8770.png`, `a5_12_resize_600-1024_8770.png`, `a5_09_drawer_account_fr_390.png`, `a5_10_ring_chevron_8770_1280_zoom.png`, `a5_6b_caption_8771_ar_1440.png` | **Sì.** Cassetto che segue la testata in ogni rotazione, frecce complete su link e chevron, chevron 44 con l'anello chiaro a due compagni. |
| RTL (ar) | quarto giro `a4_05_exits_8770_ar_1440.png` | `a5_13_exits_8770_ar_1440.png`, `…_zoom.png`, `a5_14_home_8770_ar_1440.png`, `a5_14_home_8771_ar_1440.png`, `a5_14_home_8770_ar_390.png` | **Sì.** Uscite arabe dentro il palcoscenico, sopra i nodi, a 51,3 px dal testo; H1 a filo (inchiostro = blocco a 390, 768, 1440, Δ 0) su entrambi i server; didascalia francese `ltr` su 8771. |
| Reduced-motion | quarto giro `a4_07_reduced_motion_*` | `a5_07_reduced_8770_1440.png`, `…_8770_390.png`, `…_8771_1440.png`, `…_8771_390.png` | **Sì.** `getAnimations()` **0** a 1440, 1024 e 390 su 8770 e 8771; righe del titolo `none`; uscite a opacità 1; invisibili solo le quattro correnti (per direzione) e la didascalia chiusa; fotografia ferma a `scale(1.06)`. |
| Forced-colors | quarto giro `a4_07_forced_colors_*` | `a5_07_forced_8770_1440.png`, `a5_07_forced_8770_exits_zoom.png`, `a5_07_forced_8771_1440.png` | **Sì**, con una riserva: vie e uscite `CanvasText` (uscite su alone `Canvas`), corrente non disegnata; ma le salite, ora dentro l'arco interno che resta navy, stanno a **1,38 : 1** (difetto 18). |

## 2. I ruoli (§71) — cinque firme, cinque punteggi indipendenti

Limite dichiarato: **un solo agente revisore** ha compilato le sei righe (la direttiva chiede cinque revisori
distinti); per ogni dimensione vale il punteggio più basso fra i ruoli che la giudicano.

| Ruolo | Cosa giudica in via primaria | Firma | Note |
|---|---|---|---|
| Creative Director | Premium Feel · Modernity · Originality · Visual Depth · coerenza con `CREATIVE_DIRECTION.md` | revisore indipendente, 26/09/2026, quinto giro | Chiusi i quattro dettagli che tenevano il Premium Feel a 3 (salite sulla pietra, vie nel vuoto a 1024, uscite arabe fuori, disegno che spariva). Contro: il ritmo della barra interim a 1280–1439 (17); le salite illeggibili in colori forzati (18). Deviazioni non firmate, ora quattro: lead non corsivo, titolo senza reveal, palcoscenico senza disegno d'ingresso, deroga a 390. |
| UX Lead | Clarity · Interaction Quality · Mobile · efficienza (§89) | revisore indipendente, 26/09/2026, quinto giro | Chiusi: cassetto in rotazione e ridimensionamento, frecce del mega-menu (LTR, RTL, mouse), chevron 44 dove c'è aria. Contro: senza JavaScript, sotto 80rem, la testata appiccicosa contiene il menu intero e copre la pagina a ogni scroll (16, preesistente); la deroga a 390 non è ancora scritta con la sua gamma di viewport. |
| Motion Lead | Motion · budget (§67) · pattern (DS §7) · reduced-motion | revisore indipendente, 26/09/2026, quinto giro | 0 fotogrammi ripresi (palcoscenico e accesso). Contro: il disegno d'ingresso prescritto da CD §3.1 / §4.4.1 non c'è più (al caricamento si muove solo la corrente, `stroke-dasharray .06 .94` a opacità .55); la testata transisce ancora `min-block-size` (`v4/shell.css:128`), proprietà di layout. Reduced-motion completo. |
| Frontend Lead | token (DS): nessun valore arbitrario · CSP · nessun `style=""` · prestazioni (§68) | revisore indipendente, 26/09/2026, quinto giro | 0 `style=`, 0 script inline eseguibili (solo JSON-LD), 0 violazioni CSP, token rispettati (test verdi). Contro: LCP 3,02–3,06 s su 4G lento, font 356 KB, 22 fogli (99,4 KB gzip, 0,6 KB sotto il tetto proposto), HTML non compresso; budget non adottato. |
| Accessibility Reviewer | Accessibility · contrasto misurato · tastiera · screen reader · RTL · forced-colors | revisore indipendente, 26/09/2026, quinto giro | Chiusi: lingua dei gloss e della didascalia, «Menu» mai coperto dopo una rotazione, frecce complete. Misurati: salite 7,66–8,98 : 1 sul navy, uscite 9,94 : 1 sull'alone (coppia di token). Contro: salite a 1,38 : 1 in colori forzati (18); senza JavaScript il contenuto irraggiungibile sotto 80rem (16); `test_rtl_browser` non eseguito. |
| Red Team indipendente (§75–78) | i quattro test | revisore indipendente, 26/09/2026, quinto giro | Vedi §4: NO · NO · SÌ · NO. |

## 3. Le dieci dimensioni (§74) — scala 1–5 con ancore

**Critiche** (una sola ≤ 2 → **BLOCK**): Premium Feel · Modernity · Clarity · Institutional Credibility ·
Accessibility · Mobile. **Di sostegno** (≤ 2 → al massimo CONDITIONALLY_READY): Visual Depth · Motion ·
Originality · Interaction Quality. Fra parentesi il punteggio del quarto giro.

| # | Dimensione | Punteggio | Osservazione (cosa, dove, in Chrome) |
|---|---|---|---|
| 1 | **Premium Feel** (critica) | **4** (3) | I quattro dettagli che nel quarto giro fissavano l'ancora 3 sono chiusi e misurati: (a) le salite stanno nel navy, fuori dal navy ≥ 98,6 unità fra vie dirette a uscite diverse e nessun incrocio sulla pietra (`a5_13_exits_8770_fr_1440_zoom.png`); (b) a 1024–1279 le vie finiscono al bordo dell'arco (x 531); (c) le uscite arabe stanno nel palcoscenico, a 51,3 px dal testo; (d) al caricamento nulla di dipinto sparisce (0 fotogrammi su 418–1 010). La composizione a 1440 si legge come una soglia attraversata: treccia sotto la chiave, tre uscite in piano con alone. Restano «1–2 dettagli da rifinire», ancora 4: il ritmo della barra interim a 1280–1439 (54 px fra sezioni con chevron contro 14 fra «Forum Vénétie–Maroc» e «Projet», difetto 17) e le salite in colori forzati (18, modo non predefinito). Non 5: il pannello del mega-menu resta un elenco bianco a due colonne, e il componente firma ha perso il suo momento d'ingresso. |
| 2 | **Modernity** (critica) | **4** (4) | Grammatica 2026 coerente: barra 32 + testata 64 → 56 in vetro, indicatore che trasla (allineato al link a 0,1 px a 1280–1600), mega-menu dal bordo, segmentato, Menu V4, cassetto dal piede misurato della testata anche dopo una rotazione, anello unico. Non 5: nessuna transizione di pagina; il disegno d'ingresso della porta è tolto. |
| 3 | **Visual Depth** | **4** (4) | Ordine dei livelli giusto in ogni stato misurato (testata sopra, scrim e cassetto dal suo piede in 20 casi su 20). Legenda e didascalia L3 in vetro, Menu L3 a due strati, testata scrollata L3, hero IMMERSIVE (ricetta navy + mesh + grana non toccata dal commit). Non 5: la luce (mesh) resta sotto la soglia di percezione. |
| 4 | **Motion** | **3** (3) | Chiuso il difetto 11: nessun fotogramma ripreso, su nessuno dei tre server né sulla pagina d'accesso. Ma la dimensione non sale, per due ragioni misurate: (a) **il disegno d'ingresso prescritto** (CD §3.1: «arco tracciato una volta 900 ms → quattro vie disegnate 900 ms con stagger 120 → legenda 200»; §4.4.1) **non c'è più**: al caricamento l'hero è fermo salvo la corrente (quattro `route-current` CSS, tratto 6 % a opacità .55, 28 s: `stroke-dashoffset` 1 → 0,86 nei primi 4 s) — la ricetta IMMERSIVE regge, l'intensità «alta» del moto dell'hero no; è una deviazione da firmare, e la via che il criterio del quarto giro lasciava aperta (stato iniziale dal primo paint, per esempio un'animazione CSS che parte col documento invece che da un modulo differito) non è stata provata; (b) la testata transisce ancora `min-block-size` (`static/css/v4/shell.css:128`), proprietà di layout — l'ancora 4 chiede 0 layout. Budget per vista rispettato (corrente + coppia legata allo scroll); la deriva della fotografia 0 → −18 unità non scopre mai il piede dell'arco mentre è visibile (lo scarto si apre dopo che il piede è passato sotto la testata: 0,2 px a y 720 con il piede a 37 px, testata a 57). Reduced-motion completo (0 animazioni). Il Motion non è più debole del quarto giro — un difetto (la ripresa) è tolto — ma ha perso il momento che l'ancora 5 chiede («porta»). |
| 5 | **Clarity** (critica) | **4** (4) | Un H1, lead Plex, corpo, una primaria + una secondaria, legenda con parola e gloss in didascalia; tre uscite leggibili (0 campioni di via, 9,94 : 1 sull'alone); a 1024–1279 nessuna via verso uscite invisibili. Non 5: su 8771 `/ar/` titolo inglese, lead, corpo e gloss francesi sotto parole arabe (ora etichettati `lang="fr"`, decisione pendente); ritmo della barra interim a 1280 (17). |
| 6 | **Institutional Credibility** (critica) | **4** (4) | Lock-up e «Menu» mai coperti dal cassetto (20 / 20 casi, anche dopo una rotazione); lock-up intatto con 296,3 px d'aria (interim) e 31,4 (`phase3`) a 1280–1439; H1 arabo a filo; nessun dato finto; testi bloccati invariati (le uscite sono le parole dell'eyebrow). Non 5: senza JavaScript, sotto 80rem, il sito pubblico si riduce al menu (16). |
| 7 | **Originality** | **4** (4) | Senza logo si riconosce ILE: carta minerale e navy del marchio, Newsreader 300 + Plex, la porta con chiave e gradini, quattro vie ancorate alla legenda e intrecciate nella soglia, tre uscite, il segmentato con «ع». Non 5: il mega-menu non ha la sua firma (dischi, fotografia) e la porta non si disegna più. |
| 8 | **Interaction Quality** | **4** (3) | I tre stati non allineati del quarto giro sono chiusi e misurati: (a) cassetto e scrim al piede della testata al primo fotogramma dopo cinque rotazioni/ridimensionamenti, su due server; (b) frecce su link **e** chevron, LTR e RTL, sezioni senza pannello comprese, ↑ che torna alla fermata d'apertura, Esc che torna lì, `scrollY` sempre 0, anche partendo da un clic del mouse; (c) chevron 44 × 44 dove c'è aria. Menu account sotto il riassunto (0 px in `fr` e `ar`), Esc a due livelli, un anello solo (chevron 44: `outline 2px #1d8a93` + `0 0 0 2px #f4f3f0`). Tolto il gestore `click` che chiudeva i pannelli: nessun effetto misurabile, il `focusout` chiude lo stesso (clic sul titolo → pannello chiuso, con e senza focus emulato). Non 5: un clic sull'area vuota del pannello lo chiude (focus sul `body`; comportamento del `focusout`, invariato da 156db5f); all'apertura del cassetto il focus resta su «Menu» (il `first.focus()` di `setDrawer` cade mentre il cassetto è ancora `visibility: hidden`; il Tab seguente entra nel cassetto). |
| 9 | **Mobile** (critica) | **3** (3) | Il fatto che teneva il 3 (cassetto ruotato sopra «Menu») è chiuso. La condizione posta dal quarto giro per il 4 però era doppia: «chiuso il 12 **e** scritta la deroga con la sua gamma di viewport» — la deroga non è scritta (README: «la gamma di viewport va scritta con la firma»), e le misure non cambiano: interim **129,2 %** a 390 × 844 (seconda azione a 816,8), **136,3 %** a 375 × 812 (seconda azione a 832,8, 20,8 px sotto la piega), **142,3 %** a 360 × 800; `phase3` 124,1 / 129,0 / 138,4 %. In più un fatto nuovo, preesistente, proprio del telefono: **senza JavaScript** a 390 × 844 la testata appiccicosa è alta **1 014 px** e resta sullo schermo a ogni scroll — il contenuto non si raggiunge (`a5_nojs_8770_390_scrolled.png`, difetto 16). Con JavaScript: bersagli 44, nessuno scroll orizzontale (`scrollWidth` = viewport a 360–768), porta → titolo → lead → azioni a passo 24. |
| 10 | **Accessibility** (critica) | **4** (4) | Nomi della legenda = parola, gloss come descrizione, ora con la sua lingua (`lang="fr"` su 8771 `/ar/`, didascalia `ltr`); un anello, un compagno, la coppia scura sul navy; tastiera completa nel mega-menu (LTR/RTL), nel cassetto (Esc a due livelli, focus restituito) e nel Menu account; «Menu» mai coperto (2.4.11); reduced-motion completo; contrasti misurati sui pixel: salite 7,66–8,98 : 1, uscite 9,94 : 1 (token). Non 5: in colori forzati le salite dentro l'arco interno a **1,38 : 1** (18; il diagramma è `aria-hidden` e la legenda porta l'informazione); senza JavaScript sotto 80rem il contenuto irraggiungibile (16; WCAG non esige il funzionamento senza script, ma il contratto del progetto — `static/js/main.js:4`, «Every behaviour here enhances markup that already works without JavaScript» — sì); `test_rtl_browser` non eseguito. |

## 4. I quattro test (§75–78) — Red Team indipendente

| Test | Domanda | Risposta richiesta | Risposta | Perché, esattamente (elemento, cattura) |
|---|---|---|---|---|
| Generic AI | «Potrebbe essere scambiato per un template generico Claude/AI?» | **NO** | **NO** | Carta minerale e navy del marchio, Newsreader 300 maiuscolo + IBM Plex, la porta con chiave e gradini attraversata da quattro vie intrecciate nella soglia e ancorate a una legenda in vetro, tre uscite con le parole dell'eyebrow, il segmentato con «ع», il lock-up ufficiale (`a5_13_exits_8770_fr_1440.png`, `a5_13_exits_8770_ar_1440.png`). Il punto fragile resta il pannello del mega-menu (bianco, colonne a chevron). |
| Editorial | «Sembra ancora principalmente una pubblicazione editoriale/legale?» | **NO** | **NO** | Serif solo nell'H1; lead, corpo, legenda, didascalia, nav, Menu in Plex; CTA a gradiente; il palcoscenico è un diagramma di prodotto (vie, nodi, uscite), non un'illustrazione. Avvertenza invariata: sotto l'hero riprende la pagina V2. |
| 2026 | «Nascosto il logo, competerebbe con prodotti digitali premium del 2026?» | **SÌ** | **SÌ** | Stati e profondità reggono: nulla di dipinto sparisce, cassetto che segue la testata in ogni rotazione, menubar completo da tastiera, chevron 44, anello unico, legenda senza salti, reduced-motion completo. Ciò che un prodotto premium non spedisce è la lista di §6: la barra interim dal ritmo disuguale (17), le salite perse in colori forzati (18), il sito che senza script si riduce al menu (16), e l'LCP di 3 s. |
| Too much | «Abbiamo aggiunto effetti inutili solo per sembrare moderni?» | **NO** (altrimenti: elenco di cosa togliere, nell'ordine di `CREATIVE_DIRECTION.md` §6.4) | **NO** | Questo giro ha **tolto** un effetto (il disegno d'ingresso del palcoscenico e della porta d'accesso) e non ne ha aggiunti. Semmai il rischio si è rovesciato: l'hero IMMERSIVE ha ora meno moto di quanto la sua direzione prescriva (§3, Motion). |

## 5. Verifiche binarie (tutte devono essere «sì»)

| Verifica | Sì/No | Prova |
|---|---|---|
| Nessuna formulazione vietata (`apps/cms/forbidden.py`), nessun testo bloccato alterato | **Sì** | Diff 156db5f → d475749: `_hero.html` (attributi `lang` e commento), `doorway.html` e `entrance.html` (commenti; tolto un `<script>`), `services.py` (percorso delle vie; `label_lang`, `text_lang`); nessun testo toccato. `tests/compliance/test_locked_content.py`, `test_public_pages.py`, `test_phase3_texts_not_leaked.py` verdi (nota A). |
| Nessun `style=""`, nessuno script inline, nessun hotlink (CSP) | **Sì** | HTML servito di `/fr/` e `/ar/` (8770, 8771): **0** ` style=`, 6 `<script>`, di cui 5 con `src` e 1 `application/ld+json` (dati, non eseguibile); pagina d'accesso: 3 `<script>` con `src`. CSP servita: `script-src 'self'`, `style-src 'self'`, `font-src 'self'`, `img-src 'self' data:`. Ascoltatore `securitypolicyviolation` installato prima del caricamento: **0** violazioni su 8770, 8771, pagina d'accesso e 8772 (due passate 4G). |
| Nessun valore fuori dai token (colori, raggi, ombre, durate, curve) | **Sì** | `tests/frontend/test_v4_tokens.py` e `test_design_docs.py` verdi (nota A); i valori nuovi sono geometria SVG (431, 496, 508, 520 unità) e il token `--hit-min` per il chevron. |
| «Nessun colore significa mai approvato»: nessun chip `conforme` con croma, nessun verde di verdetto | **Sì** | Nessun chip nelle superfici del gate; l'unico verde è quello del marchio nel lock-up. |
| Nessun dato, contatore, avatar, grafico o KPI finto | **Sì** | Nessun numero nell'hero e nella testata; le vie sono le `entrances()` reali; le uscite le parole dell'eyebrow; il menu account mostra `qa-person`. |
| Coordinate, «svg», «Suspendre le mouvement», etichette di debug: assenti | **Sì** | HTML servito (8770, 8771, `fr` e `ar`): 0 «Suspendre», 0 «svg» nei nodi di testo, 0 coordinate, 0 id duplicati (33 / 39 id). |
| Reduced-motion: pagina completa, nulla a opacità 0 | **Sì** | §1, riga Reduced-motion: 0 animazioni su due server a tre larghezze, titolo `none`, uscite a opacità 1; invisibili solo le correnti (per direzione) e la didascalia chiusa. |
| Contrasto sul peggior fondo (incluso sotto il vetro) ≥ 4,5 testo / ≥ 3 UI | **Sì** | Superfici con testo invariate nei colori e nei fondi (misure sui pixel del secondo giro); nuove misure di questo giro sui pixel: salite 7,66–8,98 : 1 sul navy (anche sotto l'alone della chiave); parole delle uscite `#b9c5d6` su alone `#0b1a33` = 9,94 : 1 (coppia di token, alone di 4 px sotto le lettere). La grafica è `aria-hidden`: le salite a 1,38 : 1 in colori forzati (18) non fanno cadere la verifica, ma vanno corrette. |
| Prestazioni: JS/CSS ≤ budget, LCP < 2,5 s, CLS < 0,1, INP < 200 ms (4G simulato) | **No** | §0-bis riga 3: LCP **3 020 / 3 060 ms** (la fotografia della porta) > 2 500; CLS 0,0032 ✓; INP-proxy deliberato 72 ms ✓; CSS 99,4 KB ✓ sul budget proposto (0,6 KB di margine), JS 36,0 ✓, font **356,1** ✗ (proposto 200); budget non scritto in §68/DS; HTML non compresso. |
| RTL (ar) a tre larghezze senza proprietà fisiche nel CSS nuovo | **Sì** | Le regole nuove sono `inline-size: var(--hit-min)` (logica) e `direction: ltr` sull'SVG del palcoscenico (non specchiato per disegno, CD §4.1); H1 a filo a 390 / 768 / 1440 (Δ 0) su 8770 e 8771; frecce del menubar speculari; menu account del cassetto a 0 px dal bordo finale; uscite arabe dentro il palcoscenico; `tests/i18n/test_rtl_static.py` verde (nota A); `tests/i18n/test_rtl_browser.py` **non eseguito**. |
| Demo page dei componenti coerente (§94) | **Sì, parziale** | `/_design/` (8770, HTML servito, 200): sezione «Navigation» con segmentato, pannello del mega-menu e Menu account; **0** id duplicati (94 id), 0 `style=`, 0 script inline; «svg» compare solo come nome del file dello sprite nella documentazione delle icone; **assenti** legenda in vetro, didascalia e porta (come nei giri precedenti). `tests/frontend/test_design_showcase.py` verde (nota A). |

**Nota A — esito dei test** (database dedicato `ile_lane4`, mai in parallelo fra loro, mai con `-p no:logging`):
1. `tests/frontend/test_design_docs.py tests/frontend/test_v4_tokens.py tests/frontend/test_frontend_bundle_is_current.py apps/pages/tests -q`
   — **395 passed in 934,75 s**, exit 0 (uscita in `review_a5/pytest_a5_fast.txt`, fuori dal repository). Eseguito
   prima delle misure di prestazione, che sono state prese a suite finita.
2. `tests/compliance/test_locked_content.py tests/compliance/test_public_pages.py tests/compliance/test_phase3_texts_not_leaked.py tests/i18n/test_rtl_static.py tests/frontend/test_design_showcase.py tests/frontend/test_header_fits_the_narrowest_viewport.py tests/frontend/test_svg_wellformed.py tests/frontend/test_template_comments_do_not_leak.py -q`
   — **88 passed in 118,54 s**, exit 0 (`review_a5/pytest_a5_compliance.txt`). `test_header_fits_the_narrowest_viewport.py`
   lancia un Chromium headless proprio con Playwright, non la scheda visibile.

Il «808 passed, 1 xfailed» del builder (frontend + pages + accounts + cataloghi) non è stato ri-eseguito per intero; la
parte richiesta sì.

## 6. Esito

| Esito | Condizione |
|---|---|
| **PASS** | tutte le critiche ≥ 4, tutte le dimensioni di sostegno ≥ 3, quattro test corretti, tutte le verifiche «sì», AFTER materialmente superiore su ogni vista |
| **CONDITIONALLY_READY** | tutte le critiche ≥ 3 e nessuna ≤ 2, al massimo due dimensioni di sostegno ≤ 2, quattro test corretti, verifiche «sì»; correzioni elencate con scadenza; **nessuna propagazione** finché non diventa PASS |
| **BLOCK** | una dimensione critica ≤ 2, **oppure** un test sbagliato, **oppure** una verifica «no», **oppure** AFTER non materialmente superiore |

Esito del gate: ☐ PASS ☐ CONDITIONALLY_READY ☒ **BLOCK**

Motivazione, nell'ordine delle regole: nessuna dimensione critica ≤ 2 (Premium Feel **4**, Modernity 4, Clarity 4,
Credibility 4, Mobile **3**, Accessibility 4), nessuna di sostegno ≤ 2 (Visual Depth 4, Motion **3**, Originality 4,
Interaction Quality 4), i quattro test corretti, l'AFTER materialmente superiore su ogni vista. Sulle dimensioni e sui
test il gate sarebbe **CONDITIONALLY_READY** — non PASS: Mobile, critica, è a 3. Lo tiene a **BLOCK** **una sola**
verifica binaria, come nei tre giri precedenti: le prestazioni (LCP 3,02–3,06 s su 4G lento contro 2,5; font 356 KB
contro i 200 proposti; budget non adottato; le leve — carattere del lock-up, corsivo della fascia forum, concatenazione
dei fogli, HTML compresso — restano del committente).

Il revisore dice anche che questo giro è stato **eseguito bene sul suo criterio**: delle sette correzioni del quarto
giro cinque sono chiuse sulla misura (11, 12, 13, 14, 15), due parziali (3 prestazioni, 6 documentazione), nessuna
regredita, e i numeri del README (§4.8, «Quarto giro») sono stati ritrovati uno per uno (fotogrammi, bordi del cassetto,
≥ 98,6 unità, 51 px, frecce, 296 / 370 px d'aria, LCP 3,0 s, CSS 99,4 KB). Due dimensioni salgono (Premium Feel e
Interaction Quality, da 3 a 4). Per la prima volta nessun difetto nuovo è un rovescio grave di una correzione: dei tre
difetti nuovi, uno è **preesistente** e mai misurato prima (16, lo stato senza JavaScript), due sono effetti **minori**
delle correzioni 6c e 13 (17, 18). Resta da decidere, oltre alle prestazioni, il moto dell'hero: senza il disegno
d'ingresso il Motion non può superare 3, e questa è una scelta del CD, non del builder.

Correzioni richieste (numerate: prima le correzioni ancora aperte del quarto giro con il loro numero, poi i difetti
nuovi da 16; ognuna con dimensione, elemento, cattura, criterio di chiusura):

3. **Prestazioni — verifica binaria 9.** Dimensione: Frontend Lead. Misura: §0-bis riga 3 (LCP 3 020 / 3 060 ms, la
   fotografia della porta; font 356,1 KB; CSS 99,4 KB in 22 fogli; HTML 43 783 byte non compresso). Criterio
   (invariato): su 8772, 4G lento + CPU ×4, due passate, **LCP < 2,5 s**, CLS < 0,1, INP-proxy < 200 ms; il budget
   **scritto** in §68/DS e rispettato o con deroga firmata; i font della home entro il budget o una decisione scritta
   su lock-up (128,9 KB) e corsivo (143,4 KB); la riduzione dei 22 fogli con una data (il CSS è a 0,6 KB dal tetto
   proposto); HTML compresso o decisione scritta (BREACH) registrata nel gate.
6. **Documentazione e decisioni** (nessun codice). (a) Firmare in `CREATIVE_DIRECTION.md` (o in una sua appendice di
   deviazioni) le **quattro** deviazioni da §3.1 / §4.4: lead non corsivo, titolo senza reveal, **palcoscenico senza
   disegno d'ingresso** (nuova: arco, vie, nodi, uscite, gradini e chiave non si disegnano più; la stessa cosa sulla
   pagina d'accesso, che è del gate B), deroga a 390 con la gamma di viewport per cui vale (interim 129,2 % a 390 × 844,
   136,3 % a 375 × 812 con la seconda azione 20,8 px sotto la piega, 142,3 % a 360 × 800). Se il CD non firma la terza,
   la via è un disegno d'ingresso che parta dallo stato iniziale **prima del primo paint** (CSS dal documento, non da un
   modulo differito), misurato con 0 fotogrammi ripresi e senza peggiorare l'LCP. (b) Le decisioni pendenti del
   committente/CD: traduzioni arabe di lead, corpo e gloss su `/ar/` (oggi francesi, ora etichettati `lang="fr"`),
   terza colonna del mega-menu, sette voci, carattere del lock-up. Criterio: le firme e le decisioni scritte nel
   documento del CD, con la gamma di viewport della deroga.
16. **Senza JavaScript, sotto 80rem, la testata appiccicosa contiene tutto il menu e copre la pagina.** Dimensioni:
    Mobile, Accessibility (robustezza), Interaction Quality, Institutional Credibility. Elementi:
    `static/css/components.css:849–864` (`html.no-js .nav-drawer { position: static; … }`, `flex-basis: 100%`: il menu
    intero diventa un blocco **dentro** `.site-header`) e `static/css/components.css:469–470` (`.site-header { position:
    sticky }`). Preesistente: la regola `no-js` viene da 1e176b3 (17/09) e d475749 non la tocca; nessun giro precedente
    l'ha misurata. Misura (8770 `/fr/`, `Emulation.setScriptExecutionDisabled`, `html.no-js`): a **1024 × 768** e **1279
    × 800** la testata va da 33 a **979** px a y 0 e da 0 a **946** px dopo `scrollTo(0, 1500)`, `position: sticky`,
    `elementFromPoint` a metà larghezza e al 75 % dell'altezza = `main-nav__link` / `main-nav__panel`; a **390 × 844**
    (`mobile: true`) la testata è 0–**1 014** px a ogni scroll e il contenuto non compare mai (`a5_nojs_8770_390_scrolled.png`,
    `a5_13b_nojs_8770_1024_scrolled.png`); a 1440 la testata è 65 px (corretta). Dietro la testata (nascosta nel DOM solo
    per la cattura) lo stesso stato mostra il limite dichiarato della correzione 13b: a 1024 e 1279 i tre **casing** delle
    vie (navy a 0,75, 5 px) attraversano la pietra fino a x 624, **11 px oltre la porta** (608), senza nodo
    (`a5_13b_nojs_8770_1024_stagezoom.png`). Criterio: senza JavaScript a 390, 768, 1024 e 1279, dopo `scrollTo(0, 1500)`
    la testata non supera l'altezza che ha con JavaScript (≤ 110 px) — o il menu senza script sta fuori dall'elemento
    appiccicoso —, e `elementFromPoint` al centro del titolo dell'hero, portato nel viewport, restituisce il titolo; e fra
    64 e 80rem senza JavaScript nessun tratto di via o di casing oltre il bordo dell'arco (x 531 unità), o questo limite
    scritto e firmato come limite del modo senza script.
17. **Il ritmo della barra interim a 1280–1439.** Dimensioni: Premium Feel, Clarity (minore). Elemento:
    `static/css/v4/shell.css:370–374` (`.main-nav__list:not(:has(> .main-nav__item:nth-child(6))) .main-nav__toggle {
    inline-size: var(--hit-min) }`, correzione 6c) con i 7 px di padding dei link sotto 90rem. Misura (8770, 1280,
    inchiostro del testo con `Range.getClientRects` e del glifo del chevron con il suo `svg`): parola → proprio glifo
    **21,0 px**, glifo → parola seguente **21,0 px** (il chevron sta a metà strada fra la sua sezione e la seguente), fra
    «Forum Vénétie–Maroc» e «Projet» **14,0 px**: **54 px** fra due sezioni separate da un chevron contro **14** fra le due
    senza, in `fr` e in `ar`; a 1440 24 / 28 / 24 (uniforme); prima della correzione (chevron da 24, come oggi su `phase3`)
    11 / 11 / 14. Cattura `a5_6c_header_8770_1280_zoom.png`: «Forum Vénétie–Maroc Projet» si legge come una voce sola.
    Criterio: a 1280, 1366 e 1439 sulla barra interim la distanza d'inchiostro fra sezioni adiacenti uniforme entro ±4 px,
    che fra loro ci sia un chevron o no (per esempio l'area di tocco da 44 che si sovrappone al padding invece di
    aggiungere spazio visibile, o un margine sulle sezioni senza pannello), con il chevron ancora ≥ 44 × 44.
18. **Colori forzati: le salite dentro l'arco interno a 1,38 : 1.** Dimensioni: Accessibility (colori forzati), minore.
    Elementi: `static/css/v4/hero.css:723–731` (in colori forzati le vie passano a `CanvasText` ma `.doorway__inner`
    tiene il suo riempimento navy: solo `filter: none`) insieme alla correzione 13 (`apps/pages/services.py`
    `_route_path` e `static/js/src/home.js` `routePath`: salite a x 496–520, dentro l'arco). Misura (8770 `/fr/`, 1440,
    `forced-colors: active`, schema chiaro, pixel della cattura): la salita di «person» a y 300 / 250 / 220 unità è
    `(0, 0, 0)` su navy `(15, 37, 71)` = **1,38 : 1**, a y 340 1,22 : 1; nel quarto giro le salite correvano sulla pietra
    (leggibili) e l'avvertenza riguardava solo la treccia. Cattura `a5_07_forced_8770_exits_zoom.png`: le tre uscite
    sembrano partire dal bordo del navy senza una via che le raggiunga. Il diagramma è `aria-hidden` e la legenda porta
    l'informazione: per questo è minore. Criterio: in colori forzati ogni tratto di via ≥ 3 : 1 contro ciò che ha dietro
    (per esempio `.doorway__inner { fill: Canvas }` sotto `forced-colors`, o un casing `Canvas` dentro l'arco), misurato
    sui pixel a 1440 in `fr` e in `ar`.

Note, non correzioni: un clic sull'area vuota di un pannello del mega-menu lo chiude (il `focusout` porta il focus al
`body`; invariato da 156db5f; il gestore `click` tolto in questo commit non cambia nulla di misurabile); all'apertura
del cassetto il focus resta su «Menu» (il `first.focus()` di `setDrawer` agisce mentre il cassetto è ancora `visibility:
hidden`; il Tab seguente entra nel cassetto, quindi la tastiera funziona); con il tocco emulato la barra istituzionale è
alta 45 px e il piede della testata a 110; le due vie verso «Mobilité régulière» escono dal piede del navy e corrono a
y 400 con il casing che lo tocca — letto come la base della soglia, accettabile; dentro il navy le salite verso
«Orientation» e «Formation» si incrociano e restano a < 2,5 unità per 32 unità d'altezza — è la treccia, al suo posto.

Firma del Creative Director (esito finale, §6 della direttiva): ______ · data/ora: ______

## 7. Ciò che non è stato possibile verificare, e perché (§95)

- **`test_rtl_browser`**: non eseguito (pilota un browser; fuori dall'insieme richiesto). Non ri-eseguita per intero la
  suite «808 passed, 1 xfailed» del builder (nota A).
- **Cinque revisori distinti** (§71): un solo agente ha compilato le sei righe.
- **Uno screen reader reale**: che i gloss francesi con `lang="fr"` vengano letti con la voce francese come descrizione
  di un link arabo è dedotto dall'HTML e dall'albero delle proprietà, non ascoltato.
- **La leggibilità delle uscite arabe** a 12 unità (≈ 11,2 px a 1440, 9,8 px a 1280): osservata sulla cattura, non
  valutata con un lettore arabo.
- **Dispositivi reali**: rotazioni e tocco sono emulati (`setDeviceMetricsOverride` con `screenOrientation`,
  `setTouchEmulationEnabled`); nessun telefono o tablet fisico.
- **Lo stato senza JavaScript a 768** e sulle pagine diverse dalla home (difetto 16): misurato a 390, 1024, 1279 e 1440
  sulla home; che la regola valga per ogni pagina pubblica è dedotto dal CSS condiviso, non misurato pagina per pagina.
  Che il difetto esistesse nei giri precedenti è dedotto dalla storia di git (regola del 17/09), non misurato sui commit
  vecchi (i server servono solo d475749).
- **Lo scrim su `/fr/parcours/`** (README: «stesso esito»): non ri-misurato; il cassetto e lo scrim sono misurati sulla
  home di 8770 e 8771.
- **Il menu account del cassetto a 768 e 1024**: questo giro lo ha misurato a 390 (`fr` e `ar`) e nella barra a 1440;
  il codice del menu account non è toccato dal commit.
- **Il Motion della pagina d'accesso** (senza coreografia della porta): verificato solo per errori e riferimenti rotti
  (nessuno); il giudizio sul suo moto è del gate B.
- **I contrasti delle superfici con testo sotto il vetro**: non ri-misurati sui pixel (colori e fondi invariati dal
  secondo giro); misurati in questo giro solo salite, uscite e salite in colori forzati.

## 8. Metodo e limiti

- Osservazione: Chrome visibile via `scripts/cdp.py` (`Page.attach(url_contains="127.0.0.1:")`, poi `"127.0.0.1:8771"`
  per le sonde con l'account), una sola scheda (`Page.bringToFront`, `visibilityState: visible`, 62 rAF in 500 ms
  all'inizio), sonde sequenziali; viewport emulati 1600 / 1440 × 900, 1439 / 1366 / 1280 × 900, 1279 / 1280 × 800,
  1100 × 800, 1024 × 768, 768 × 1024, 600 × 768, 390 × 844, 375 × 812, 360 × 800, 844 × 390 (con `mobile: true`, tocco
  e orientamento dove indicato); emulazioni azzerate a fine sonda (viewport, tocco, media, rete, CPU, focus, esecuzione
  degli script).
- Script del revisore: `C:\Users\<user>\AppData\Local\Temp\claude\C--tmp-italylegalentry\review_a5\` (`common.py`,
  `sampler.js`, `r0_window.py`, `r1_stage_frames.py`, `r2_exits.py`, `r3_exitside.py`, `r4_exit_shots.py`, `r5_mid.py`,
  `r5b_nojs.py`, `r5c_nojs_header.py`, `r5d_nojs_stage.py`, `r6_drawer.py`, `r7_mega.py`, `r8_mouse.py`, `r9_header.py`,
  `r9b_rhythm.py`, `r10_perf.py` (derivato da `review_a4/r14_perf.py`), `r11_photo.py`, `r12_legend_lang.py`,
  `r13_media.py`, `r13b_fc_crop.py`, `r14_mobile.py`, `r15_ring.py`, `r16_misc.py`, `r17_account.py`,
  `r18_drawer_focus.py`); uscite `r2_out.txt`, `r10_out.txt`; HTML servito salvato in `home_8770.html`,
  `home_8771.html`, `home_ar_8770.html`, `home_ar_8771.html`, `design_8770.html`; esiti dei test `pytest_a5_fast.txt`,
  `pytest_a5_compliance.txt`.
- Le prestazioni sono state misurate a suite di test finita (la prima suite ha girato in parallelo alle sonde
  funzionali, mai alle misure di tempo).
- Nessun file del repository modificato al di fuori di questa scorecard e delle catture in `review_a5/`.
