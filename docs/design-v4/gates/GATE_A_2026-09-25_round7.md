# GATE A — Homepage (hero) + Navbar · scorecard del 26 settembre 2026 — **settimo giro**

Compilata sul modello `docs/design-v4/GATE_SCORECARD_TEMPLATE.md` (§71–78 della direttiva). Regole
applicate: **nessuna media** (§74); **l'implementatore non vota** (§72); ogni punteggio cita ciò che il
revisore ha **osservato in Chrome visibile** (§70) — Google Chrome 153, CDP 9222, `scripts/cdp.py`, una sola
scheda, sonde sequenziali, `Network.enable` + `Network.setCacheDisabled` in testa a ogni sonda. Le misure sono
`getBoundingClientRect` / `getComputedStyle` (anche dello pseudo-elemento `::before`) / `elementFromPoint` /
`getScreenCTM` / `getPointAtLength` / `Range.getClientRects` / `performance.getEntriesByType` / `PerformanceObserver`
(LCP, layout-shift, longtask, event, installati con `Page.addScriptToEvaluateOnNewDocument`) / campionamento a ogni
`requestAnimationFrame` / `document.getAnimations()` / eventi reali (`Input.dispatchMouseEvent` — anche `mouseWheel`
per scorrere senza JavaScript —, `Input.dispatchKeyEvent` con `Emulation.setFocusEmulationEnabled` e un Tab reale prima
del focus programmatico, **`Input.dispatchTouchEvent`** con `Emulation.setTouchEmulationEnabled` e
`setDeviceMetricsOverride` `mobile: true`, `Emulation.setEmulatedMedia` per reduced-motion e per i colori forzati
**nelle due tavolozze**, `Emulation.setScriptExecutionDisabled` per lo stato senza JavaScript,
`Network.emulateNetworkConditions` 150 ms / 1,6 Mbit/s / 750 kbit/s + `Emulation.setCPUThrottlingRate` 4 per il 4G
lento) e letture di pixel con Pillow sulle catture del revisore (differenza fra la cattura a riposo e quella nello
stato; colonne d'inchiostro con luminanza < 140). Le catture di questo giro stanno in
`docs/qa/chrome/design-v4/after/review_a7/` (prefisso `a7_`, ignorate da git); i percorsi sono relativi alla radice
del repository. Ogni numero di questo documento è una misura del revisore presa in questo giro (26/09, 11:58–12:41); i
numeri del README e dei giri precedenti sono citati solo per confronto.

Nota sulle misure: la scheda riportava `devicePixelRatio` **1** (finestra 1905 × 1012, interno 1889 × 861, 61 rAF in
500 ms, `visibilityState: visible`); tutte le emulazioni con `deviceScaleFactor: 1`, azzerate a fine sonda (viewport,
tocco, media, rete, CPU, focus, esecuzione degli script).

Nota sulla scheda: all'inizio i target di 9222 contenevano **una** pagina di progetto,
`http://127.0.0.1:8771/fr/espace-reserve/`, autenticata come `qa-person`. Le sonde su 8770 e 8772 l'hanno disconnessa
da 8771 (cookie per host). Il revisore l'ha ri-autenticata con `scripts/qa_chrome_signin.py` (sessione lato server,
nulla digitato) per le sonde del menu account, e di nuovo a fine giro.

Manipolazioni del DOM nella scheda, dichiarate (tutte annullate subito, nessun file toccato): un ascoltatore `click`
in cattura che registra il bersaglio e annulla la navigazione dei soli link (per scandire i tocchi senza lasciare la
pagina); per attribuire la causa del difetto 22, un foglio **costruito** (`new CSSStyleSheet()` +
`document.adoptedStyleSheets`, poi svuotato) con una regola per volta — `::before { display: none }`,
`::before { pointer-events: none }`, `position: static`, `padding-inline: 7px`, `inline-size: 24px`. (Un primo
tentativo con un elemento `<style>` è stato bloccato dalla CSP `style-src 'self'` e non ha avuto effetto: i suoi numeri
sono scartati.)

Questo documento verifica, correzione per correzione, le correzioni del sesto giro (`gates/GATE_A_2026-09-25_round6.md`,
§6: 3 e 6 ancora aperte, 19–21 nuove), ciascuna contro il **suo** criterio di chiusura; poi cerca i difetti introdotti
dalle correzioni (e quelli che esse hanno reso visibili), ri-assegna le dieci dimensioni, i quattro test e le verifiche
binarie.

---

## 0. Identità del gate

| Campo | Valore |
|---|---|
| Gate | **A** |
| Superfici | Homepage pubblica `/fr/`: hero «il portico» (porta, quattro vie, legenda in vetro con didascalia, titolo, lead, CTA; uscite etichettate nella variante interim) + navbar (barra istituzionale con controllo lingua e accesso/menu account, testata, indicatore, mega-menu, cassetto con segmentato); `/ar/` per RTL, `/it/` e `/en/` per la lunghezza delle voci; `/fr/parcours/` per la testata senza JavaScript; `/fr/entreprises/` e `/fr/le-projet/` per lo stato «pagina corrente» della barra; la vetrina `/_design/` |
| URL / account | **8770** (`ile`, fase 3 chiusa → variante **interim**, **quattro** voci: Personnes ⌄ · Entreprises ⌄ · Forum Vénétie–Maroc · Projet ⌄); **8771** (`ile_qa`, fase 3 aperta → variante `phase3`, **sette** voci; `qa-person` per menu account e cassetto); **8772** (lo stesso codice di 8770 dietro WhiteNoise gzip) per le prestazioni. Verificato all'inizio: `v4/hero.css` (md5 `9318cf91`), `v4/shell.css` (`f3f8facb`), `components.css` (`e5b5cb52`), `main.js` (`02e6d585`), `head.js` (`d1d44e39`) serviti da 8770, 8771 e 8772 **identici ai file dell'albero** (8772 con `Content-Encoding: gzip`: `v4/shell.css` 5 725 byte, `v4/hero.css` 6 993). HTML servito: `<clipPath id="doorway-routes-arch">` una volta su 8770 e 8771, `fr` e `ar`; `doorway--exits` solo su 8770; 34 id (8770) e 40 (8771), **0** duplicati. |
| Commit sotto revisione | **265577c** (albero pulito: `git status` vuoto all'inizio; alla fine l'unico file nuovo è questa scorecard, non tracciata). Sulle superfici del gate, da 213e00f: `static/css/v4/shell.css` (correzione 19: da 80rem, sulle barre di cinque sezioni o meno, lo chevron da 44 è `position: relative; isolation: isolate`, la tinta di hover è un `::before` `inset: 8px` — 28 × 28, raggio `--radius-sm`, `z-index: -1` —, l'anello `outline-offset: -6px` senza compagno, `box-shadow: none`; sotto 90rem `padding-inline: 14px` su link ed etichette al posto del margine negativo del quinto giro; più i commenti condensati), `static/css/v4/hero.css` (correzioni 20–21, solo sotto `forced-colors`: `.doorway__inner` perde `fill: Canvas`, `.doorway-legend__glyph { color: CanvasText }`, `.doorway__steps rect:nth-child(n) { opacity: 1; stroke: Canvas; stroke-width: 2px; paint-order: stroke; vector-effect: non-scaling-stroke }`; più i commenti condensati), `docs/design/DESIGN_SYSTEM_2026.md` (pesi: shell 22,5 → 21,4 KB, hero 24,0 → 23,0 KB — ritrovati: 21 865 e 23 587 byte). Nessun template, nessun testo, nessun JavaScript toccato. |
| Revisione | **settimo giro** (sesto: `gates/GATE_A_2026-09-25_round6.md`, su 213e00f, BLOCK per la sola regola delle prestazioni; quinto: `…_round5.md`, su d475749; quarto: `…_round4.md`, su 156db5f; terzo: `…_round3.md`, su dd29168; secondo: `…_round2.md`, su d99f2bb; primo: `GATE_A_2026-09-25.md`, su c6f3503) |
| Implementatore (non vota) | Claude (sessione principale) |
| Revisore indipendente | agente separato (nessuna modifica a codice, template, fogli, script o test; nessun riavvio di server; nessun pacchetto installato; nessuna credenziale digitata; nessun modulo inviato; nessuna scheda aperta o chiusa) |
| Data e ora della revisione | 26 settembre 2026, ore 11:58–12:41 (misure in Chrome e test); scorecard scritta subito dopo |

**I commenti condensati non hanno cambiato regole.** Tolti i commenti (`/* … */`) e normalizzati gli spazi,
`static/css/v4/shell.css` e `static/css/v4/hero.css` di 213e00f e di 265577c differiscono **solo** nelle regole di 19–21:
in `shell.css` +20 righe (le cinque regole dello chevron da 44 da 80rem) e −8 (il blocco 80–90rem del quinto giro:
`position: relative; z-index: 1; margin-inline: -7px` e l'anello con compagno `inset`) sostituite dal solo
`padding-inline: 14px`; in `hero.css` una riga cambiata (`.doorway__inner { fill: Canvas; stroke: CanvasText;
forced-color-adjust: none }` → `{ stroke: CanvasText }`) e due aggiunte (glifi, gradini). Nessun'altra riga di regola
differisce (script `review_a7/css_nocomment.py`).

## 0-bis. Le correzioni del sesto giro — verifica una per una, contro il loro criterio

| # | Correzione (sesto giro) | Stato | Prova (misura o cattura) |
|---|---|---|---|
| 3 | Prestazioni — verifica binaria 9 | **PARZIALE** (il CSS torna **sotto** il tetto proposto; LCP e font no) | 8772, 1440 × 900, cache spenta, 4G lento + CPU ×4, due passate, **a suite di test finite**: **LCP 3 032 / 2 940 ms** — `image.doorway__img` (`doorway-800.webp`, 133 126 px²); FCP 1 688 / 1 740; DCL 3 673 / 3 249; load 3 897 / 3 700; CLS **0,0038 / 0,0121**; long task max **414** / 272 ms (12 / 12 task); 0 violazioni CSP, 0 errori; palcoscenico: 557 / 657 fotogrammi campionati, **0** ripresi dopo il primo visibile. **Pesi** (identici nelle due): CSS **22 fogli, 101 382 byte gzip = 99,0 KiB** (389,4 KiB nudi) — **1 018 byte sotto** il tetto proposto di 100 KiB (al sesto giro 41 byte sopra: −1 059 byte, tutti dai commenti); JS **8 file, 36 892 byte**; font **6 file, 356,1 KB** (Newsreader tondo 128,9 precaricato, Newsreader **corsivo 143,4**, Plex Sans 22,1 + 23,6 + 23,7, Plex Mono 14,4) — sopra i 200 proposti **e sopra il tetto scritto di 320 KB del percorso latino** (`docs/design/DESIGN_SYSTEM_2026.md` §6.2, che cita AD-A §3.7.6: è il corsivo del serif a portarlo fuori); immagini 5 file, 79,5 KB (foto 76,8, precaricata, richiesta a 241 / 274 ms, finita a 2 850 / 2 869); HTML **43 926 byte non compresso**; **42 richieste**. Senza limiti: LCP 404 ms (la foto), CLS 0,0002. **INP-proxy deliberato** (seconda passata, CPU ×4: hover su una riga della legenda, clic sul chevron «Entreprises», Esc, hover sul secondario): evento più lungo **120 ms** (`pointerdown` / `mousedown` del chevron), gli altri ≤ 96. Numeri del README («Sesto giro»: LCP 3 364 / 3 416 ms, CSS «99,0 KB»): il CSS ritrovato al byte; l'LCP di questo giro è più basso di 330–480 ms, dentro la varianza 3,0–3,7 s che il README stesso dichiara. Il budget resta «proposto al CD», non scritto in §68/DS; la leva della minificazione (95,3 → 47,8 KB, misurata dal builder) resta decisione del committente. |
| 6 | Documentazione e decisioni | **PARZIALE** (invariata) | `docs/design-v4/CREATIVE_DIRECTION.md`: ultimo commit **6718f1a** (24/09); 265577c tocca solo README, scorecard del sesto giro e pesi del DS. Le **quattro** deviazioni da §3.1 / §4.4 (lead non corsivo, titolo senza reveal, palcoscenico senza disegno d'ingresso, deroga a 390 con la sua gamma di viewport) restano scritte solo nel README, nessuna firmata. Pendenti anche: traduzioni arabe di lead, corpo e gloss su 8771 `/ar/`, terza colonna del mega-menu, sette voci, carattere del lock-up, minificazione dei fogli. |
| 19 | Barra interim fra 80 e 90rem: gli stati del chevron invadono i vicini | **CHIUSA** sul criterio (a, b, d; c con mouse e tastiera) — il **tocco** confluisce nel difetto nuovo **22** | 8770, pixel delle catture a 1× (colonne cambiate fra riposo e stato, sulla riga a 10 px dal bordo superiore del riquadro; inchiostro dei vicini con luminanza < 140). **(a)** A **1280, 1366 e 1439**, `fr` e `ar`, sui tre chevron: tinta di hover = `::before` 28 × 28, `rgb(236, 235, 230)` (`--min-1`), raggio 6, riquadro trasparente (`background: rgba(0, 0, 0, 0)`); a **23–25 px** dall'ultima lettera della parola che precede e dalla prima di quella che segue (criterio ≥ 6). **Pressione** (`mousePressed` tenuto): stessa forma, stessi 23–25 px (nessuna regola `:active`: la pressione è l'hover). **Anello** (Tab reale + focus, letto dopo 400 ms): `outline 2px solid rgb(29, 138, 147)`, `outline-offset: -6px`, `box-shadow: none`, `:focus-visible` vero; 36 px di lato, a **18–20 px** dall'inchiostro vicino (criterio ≥ 4); contro la testata `rgb(245, 244, 240)` **3,73 : 1**, anche con la testata scorsa sopra l'hero scuro (`is-over-dark`, vetro 92 %: stesso pixel composto). A 1440 (fuori criterio; la forma da 28 vale da 80rem) tinta a 19–25 px, anello a 14–20. Catture `a7_02_states_sheet.png`, `a7_03_fr_1280_focus_hover_chev1.png`. **(b)** Su `/fr/entreprises/` e `/ar/entreprises/` («Entreprises» `aria-current`), col pannello di «Entreprises» aperto (`data-open="true"`) e su `/le-projet/`: fra la tinta dello chevron in hover e la pillola adiacente **9 px** sulla riga di misura (8 px geometrici: il `::before` comincia 8 px dentro il riquadro, la pillola finisce sul suo bordo), a 1280, 1366 e 1439, `fr` e `ar`, sui due lati — nessuna fusione (`a7_04_pills_sheet.png`). **(c)** Distanze d'inchiostro (`Range.getClientRects` del testo, riquadro dell'`svg`, in ordine visivo): **28,0 px tutte**, scarto **0**, a 1280, 1366, 1439 in `fr` e `ar`, e in `it` e `en` a 1280 e 1439; chevron **44 × 44** a ogni larghezza; frecce del menubar (↓ ↓ ↓ ↑ × 4; → × 4 con giro, ← ↑ ↓; dallo chevron → ← e ↓ ↓ ↑ ↑ ↓ Esc; dal pannello ↓ → ↓ ← ←) con gli stessi esiti del sesto giro a 1280 e 1439, `fr` e `ar`, `scrollY` 0 dopo ogni tasto. **(d)** I bordi tornano ai link: `elementFromPoint` 1 e 3 px dentro i bordi di ogni link → il link, 1 px dentro i quattro bordi di ogni chevron → lo chevron (le sole eccezioni, a «bordo − 1» su bordi frazionari condivisi, spariscono in una scansione a passi di 0,5 px: il cambio di bersaglio cade entro 0,5 px dal bordo di layout); **clic reali del mouse** 3 px dentro la fine di «Personnes», l'inizio e la fine di «Entreprises», l'inizio di «Forum Vénétie–Maroc», la fine di «Projet» → `/fr/parcours/`, `/fr/entreprises/`, `/fr/forum/`, `/fr/le-projet/` (e gli omologhi `ar`) a 1280 e 1439; clic 1 px dentro i bordi sinistro e destro di ogni chevron → il suo pannello, URL invariato. Senza JavaScript, a 1280 e 1439, l'hover 3 px dentro ciascun bordo di link apre il pannello **della propria** voce (nessuno per «Forum»): la nota del sesto giro è risolta. **Con il tocco no**: la scansione a passi di 1 px con `Input.dispatchTouchEvent` dà allo chevron solo 36 dei suoi 44 px (difetto 22). |
| 20 | Colori forzati, tavolozza chiara: la chiave perde il suo fondo | **CHIUSA** | 8770 `/fr/` e `/ar/`, 1440, `forced-colors: active` con `prefers-color-scheme` **chiaro e scuro**: `.doorway__inner` `fill` `rgb(15, 37, 71)` (navy, `forced-color-adjust: preserve-parent-color`), `stroke` CanvasText. Oro della chiave `rgb(195, 154, 43)` sul navy = **5,80 : 1** nelle due tavolozze e nelle due lingue; il foro dell'anello (scansione verticale a x 448, 12–13 righe dentro l'anello d'oro) = `rgb(15, 37, 71)`, **1,00 : 1** col fondo (criterio ≤ 1,1). Vie (centro della linea contro il casing a 1,6 / 2,0 px in perpendicolare, 600 punti per via, esclusi i punti sotto la legenda): mediana **21,0 : 1** in ogni tratto — pietra, fotografia, arco interno, salite, uscite — nelle due tavolozze e lingue; decimo percentile 5,5–21 (i più bassi nella treccia, dove due vie si sovrappongono). Su 8771 (`phase3`): chiave 5,80, foro 1,00, vie mediane 12,7–15,6 (decimo percentile 4,0–8,8). Catture `a7_07_forced_key_steps_sheet.png`, `a7_07_forced_light_fr_1440.png`, `a7_07d_8771_sheet.png`. Il bagliore d'oro dietro la chiave resta un alone tenue sul navy (decorazione, non UI). |
| 21 | Colori forzati, tavolozza chiara: glifi della legenda e gradini sotto 3 : 1 | **CHIUSA** | Stesse sonde. **Glifi**: `color` `rgb(0, 0, 0)` in chiara, `rgb(255, 255, 255)` in scura; pixel più contrastato di ogni glifo contro il fondo della legenda (`Canvas`) **16,9–20,3 : 1** in chiara, **16,2–19,9 : 1** in scura (8770 `fr` e `ar`, 8771 `fr`; il glifo è un tratto sottile antialiasato, da qui lo scarto dal 21). **Gradini**: `opacity` 1, `fill` CanvasText, `stroke` Canvas 2 px con `paint-order: stroke` e `vector-effect: non-scaling-stroke` — metà del tratto sta sotto il riempimento, il filetto **visibile è 1 px** (a 1× antialiasato in `rgb(213–214, 215–216, 218)` in chiara). Riempimento contro il pixel 1 px oltre il bordo superiore, mediane per gradino **14,56 / 7,01 / 19,60 : 1** in chiara, **19,46 / 5,41 / 20,03 : 1** in scura; il filetto contro la pietra della fotografia 6,54 : 1 (chiara). Contro la fotografia **3 px** oltre il bordo, senza il filetto in mezzo, il gradino alto in chiara resta a 2,10 : 1 (nero su pietra scura): il contrasto di confine lo porta il filetto Canvas, ed è così che 1.4.11 lo misura (colori adiacenti). Cattura `a7_07_forced_key_steps_sheet.png`: tre barre nere filettate di bianco in chiara, tre barre bianche filettate di nero in scura. Anche le uscite si leggono nelle due tavolozze (testo CanvasText con alone Canvas, nodi 19,95–21 : 1; `a7_07_forced_exits_sheet.png`). |

## 1. BEFORE / AFTER (§73)

| Vista | BEFORE | AFTER | Verdetto «materialmente superiore» (sì/no + una frase) |
|---|---|---|---|
| Desktop 1440 | `docs/qa/chrome/design-v4/before/01_home.png` (V2 interim); sesto giro `after/review_a6/a6_03_perf_8772_1440.png` | `a7_03_perf_8772_1440.png`, `a7_14_home_8770_ar_1440.png`, `a7_14_home_8771_ar_1440.png` | **Sì.** A 1440 la composizione è quella del sesto giro; cambiano solo la forma di hover e l'anello degli chevron (la forma interna da 28, che vale da 80rem), ora a 14–25 px dalle parole. |
| Desktop 1280 · 1366 · 1439 | sesto giro `a6_17_states_sheet.png`, `a6_19_fused_sheet.png` (pillola del chevron a 1–2 px dalle parole, fusa con la pillola corrente) | `a7_01_bar_8770_fr_1280_zoom.png`, `a7_02_states_sheet.png`, `a7_04_pills_sheet.png` | **Sì.** Ritmo uniforme (28 px d'inchiostro ovunque), tinta e anello dello chevron staccati dalle parole (23–25 / 18–20 px) e dalle pillole (9 px); i bordi dei link tornano ai link. |
| Tablet 768 · 1024 | sesto giro `a6_14_home_8770_fr_768.png`, `a6_16c_js_drawer_1024.png` | `a7_14_home_8770_fr_768.png`, `a7_16c_js_drawer_1024.png`, `a7_16_nojs_8770_1024_scrolled.png` | **Sì.** Invariata (il commit non tocca nulla sotto 80rem): cassetto e scrim dal piede della testata, testata senza script che scorre via. |
| Mobile 390 | sesto giro `a6_14_home_8770_fr_390.png` | `a7_14_home_8770_fr_390.png`, `a7_16c_js_drawer_390.png`, `a7_16_nojs_8770_390_scrolled.png` | **Sì.** Invariata: interim 129,2 % a 390 × 844 (seconda azione a 816,8), H1 a filo, testata senza script che scorre via. |
| Stato interattivo (hover/focus/press/aperto) | sesto giro `a6_17_fr_1280_hover_chev1.png`, `a6_19_fr_1280_current_entreprises_hover_chev0.png` | `a7_02_fr_1280_hover_chev1.png`, `a7_02_fr_1280_pressed_chev1.png`, `a7_03_fr_1280_focus_chev1.png`, `a7_03_fr_1280_focus_hover_chev1.png`, `a7_04_fr_1280_open_hover_chev1.png`, `a7_05_fr_1280_indicator_projet.png`, `a7_09_drawer_account_fr_390.png` | **Sì, con riserva.** Con mouse e tastiera ogni stato del chevron è staccato e allineato; cassetto, scrim, menu account, frecce, indicatore invariati e misurati. La riserva è il tocco: i 4 px di bordo di ogni chevron vanno al link accanto (difetto 22, introdotto dal `::before`). |
| RTL (ar) | sesto giro `a6_14_home_8770_ar_1440.png`, `a6_17_ar_1280_hover_chev1.png` | `a7_14_ar_sheet.png`, `a7_01_bar_8770_ar_1280_zoom.png`, `a7_02_ar_1280_hover_chev1.png`, `a7_04_ar_1280_open_hover_chev1.png` | **Sì.** Barra araba a 28 px uniformi, tinta a 23–25 px dalle parole e a 9 px dalle pillole, anello a 18–19; H1 a filo (inchiostro = blocco, Δ 0) a 390 / 768 / 1440 su 8770 e 8771. |
| Reduced-motion | sesto giro `a6_07_reduced_*` | `a7_07_reduced_8770_1440.png`, `a7_07_reduced_8770_390.png` | **Sì.** `getAnimations()` **0** a 1440, 1280, 1024 e 390 su 8770 e 8771; titolo `none`; uscite a opacità 1; invisibili solo le quattro correnti e la didascalia chiusa; foto ferma a `scale(1.06)`; transizione del `::before` e dei link 1e-05 s. |
| Forced-colors | sesto giro `a6_18_forced_light_8770_fr_stage.png` (chiave sul bianco a 2,63 : 1, glifi 1,73 : 1, gradini 1,2–1,45 : 1) | `a7_07_forced_light_fr_1440.png`, `a7_07_forced_dark_fr_1440.png`, `a7_07_forced_key_steps_sheet.png`, `a7_07_forced_exits_sheet.png`, `a7_08_fc_light_fr_1280_focus_chev1.png` | **Sì.** Chiave sul suo navy (5,80 : 1, foro 1,00), vie a mediana 21 : 1 sul casing, glifi 16–20 : 1, gradini filettati; anello dello chevron nel colore di sistema (15,13 : 1 in chiara, 14,37 in scura). |

## 2. I ruoli (§71) — cinque firme, cinque punteggi indipendenti

Limite dichiarato: **un solo agente revisore** ha compilato le sei righe (la direttiva chiede cinque revisori
distinti); per ogni dimensione vale il punteggio più basso fra i ruoli che la giudicano.

| Ruolo | Cosa giudica in via primaria | Firma | Note |
|---|---|---|---|
| Creative Director | Premium Feel · Modernity · Originality · Visual Depth · coerenza con `CREATIVE_DIRECTION.md` | revisore indipendente, 26/09/2026, settimo giro | Chiusi gli stati del chevron che toccavano le parole (19) e la chiave sul bianco (20). Note, non difetti: l'anello dello chevron ha angoli quasi vivi (raggio 6 − 6 = 0 all'interno) attorno a una forma raggiata 6, quindi non «abbraccia» la forma in modo concentrico (2 px sui lati, ≈ 5 in diagonale); con 28 px da entrambe le parti lo chevron sta esattamente a metà fra la sua parola e la seguente — l'uniformità chiesta dal quinto giro toglie la vicinanza che lo lega alla sua voce (a 1440 resta 24 / 28). Deviazioni non firmate, ancora quattro. |
| UX Lead | Clarity · Interaction Quality · Mobile · efficienza (§89) | revisore indipendente, 26/09/2026, settimo giro | Chiusi i bersagli presi dai vicini con il mouse (un clic 3 px dentro «Forum» porta a `/fr/forum/`). Contro, nuovo: con il **tocco** (Chrome, `Input.dispatchTouchEvent`, raggio 1, 6 e 12) i primi e gli ultimi 4 px di ogni chevron da 44 aprono la pagina del link accanto invece del pannello (22): su un tablet in orizzontale o un portatile touch fra 1280 e 1600 un tocco sul bordo dello chevron porta via dalla pagina. La deroga a 390 non è scritta. |
| Motion Lead | Motion · budget (§67) · pattern (DS §7) · reduced-motion | revisore indipendente, 26/09/2026, settimo giro | Nessun effetto del commit sul moto oltre la transizione di 120 ms del `::before` (`--motion-fast`, `--ease-exit`, azzerata sotto reduced-motion); 0 fotogrammi ripresi nelle due passate in 4G lento. Contro, invariati: il disegno d'ingresso prescritto da CD §3.1 / §4.4.1 non c'è; la testata transisce ancora `min-block-size` (`static/css/v4/shell.css:128`). |
| Frontend Lead | token (DS): nessun valore arbitrario · CSP · nessun `style=""` · prestazioni (§68) | revisore indipendente, 26/09/2026, settimo giro | 0 `style=`, 0 script inline eseguibili, 0 violazioni CSP, 0 id duplicati, test verdi; commenti condensati senza regole cambiate; CSS 99,0 KiB (sotto il tetto proposto). Contro: LCP 2,94–3,03 s su 4G lento; font 356 KB (sopra anche il tetto scritto di 320 KB); HTML non compresso; budget non adottato. Tre letterali di geometria accoppiati a mano (`inset: 8px`, `outline-offset: -6px` = −(8 − 2), `padding-inline: 14px`): non token, e il −6 dipende da `--focus-ring-width` senza esprimerlo. |
| Accessibility Reviewer | Accessibility · contrasto misurato · tastiera · screen reader · RTL · forced-colors | revisore indipendente, 26/09/2026, settimo giro | Chiusi 20 e 21: in colori forzati, nelle due tavolozze, chiave 5,80 : 1 col foro nel colore del fondo, glifi 16–20 : 1, gradini filettati, vie 21 : 1 di mediana. Anello dello chevron visibile (3,73 : 1 sulla testata; colore di sistema in colori forzati). Contro: area di tocco effettiva dello chevron **36 px su 44** (22; resta ≥ 24, nessuna violazione 2.5.8, ma non i 44 del principio 7 del DS); `test_rtl_browser` non eseguito. |
| Red Team indipendente (§75–78) | i quattro test | revisore indipendente, 26/09/2026, settimo giro | Vedi §4: NO · NO · SÌ · NO. |

## 3. Le dieci dimensioni (§74) — scala 1–5 con ancore

**Critiche** (una sola ≤ 2 → **BLOCK**): Premium Feel · Modernity · Clarity · Institutional Credibility ·
Accessibility · Mobile. **Di sostegno** (≤ 2 → al massimo CONDITIONALLY_READY): Visual Depth · Motion ·
Originality · Interaction Quality. Fra parentesi il punteggio del sesto giro.

| # | Dimensione | Punteggio | Osservazione (cosa, dove, in Chrome) |
|---|---|---|---|
| 1 | **Premium Feel** (critica) | **4** (4) | Chiusi i due dettagli che il sesto giro citava: la pillola del chevron che toccava le parole e si fondeva con la pillola corrente (ora una forma da 28 px a 23–25 px dalle parole e a 9 px dalle pillole, `a7_02_states_sheet.png`, `a7_04_pills_sheet.png`), e la chiave del marchio sul bianco in colori forzati (ora sul suo navy). A 1440 la composizione è quella del sesto giro (0 fotogrammi ripresi in 557 e 657 fotogrammi sotto 4G lento). Restano «1–2 dettagli da rifinire», ancora 4: l'anello dello chevron è un quadrato quasi vivo attorno a una forma raggiata (non concentrico: 2 px sui lati, ≈ 5 in diagonale, `a7_03_fr_1280_focus_hover_chev1.png`), accanto agli anelli raggiati dei link; lo chevron equidistante (28 / 28) dalla sua parola e dalla seguente. Non 5: il pannello del mega-menu resta un elenco bianco a due colonne e il componente firma non ha il suo momento d'ingresso. |
| 2 | **Modernity** (critica) | **4** (4) | Grammatica 2026 coerente e invariata: barra 32 + testata 64 → 56 in vetro, indicatore che trasla (uguale al riquadro del link a 0,0 px su ogni voce, `fr` e `ar`, 1280–1440), mega-menu dal bordo, segmentato, Menu V4, cassetto dal piede misurato della testata; la forma interna dello chevron separata dall'area di tocco è un pattern corrente. Non 5: nessuna transizione di pagina; il disegno d'ingresso della porta è tolto. |
| 3 | **Visual Depth** | **4** (4) | Ordine dei livelli giusto in ogni stato misurato: testata sopra; cassetto e scrim dal suo piede (57 / 65 px) in 8 casi su 8 con lock-up e «Menu» colpiti al centro; pannello dal piede della barra (97 contro 98, come nei giri precedenti), lock-up visibile col pannello aperto a cinque larghezze. Il `::before` a `z-index: -1` resta dentro il contesto dello chevron (`isolation: isolate`): nessuno strato nuovo sulla testata. Non 5: la luce (mesh) resta sotto la soglia di percezione. |
| 4 | **Motion** | **3** (3) | Il commit aggiunge solo la transizione di colore del `::before` (120 ms, `--ease-exit`, 1e-05 s sotto reduced-motion). Invariate le due ragioni del 3: (a) il disegno d'ingresso prescritto (CD §3.1: arco 900 ms → quattro vie 900 ms con stagger 120 → legenda 200; §4.4.1) non c'è, deviazione non firmata; (b) la testata transisce `min-block-size` (`static/css/v4/shell.css:128`), proprietà di layout — l'ancora 4 chiede 0 layout. Reduced-motion completo (0 animazioni su due server a quattro larghezze). |
| 5 | **Clarity** (critica) | **4** (4) | Un H1, lead Plex, corpo, una primaria + una secondaria, legenda con parola e gloss; tre uscite leggibili; la barra interim si legge come quattro voci distinte a riposo e negli stati (la tinta dello chevron non si fonde più con la voce accanto). Non 5: su 8771 `/ar/` lead, corpo e gloss francesi sotto parole arabe (decisione pendente); lo chevron a metà strada fra due parole lega poco la freccia alla sua voce (nota del CD, non difetto: è l'uniformità chiesta dal criterio 17). |
| 6 | **Institutional Credibility** (critica) | **4** (4) | Nessun testo toccato; lock-up con 240,3 px d'aria (`fr`), 304,3 (`ar`), 257,5 (`it`), 229,1 (`en`) a 1280–1439 e 370 / 441,2 a 1440 — mai coperto (8 / 8 casi col cassetto; 30 / 30 col pannello aperto: cinque larghezze × tre pannelli × due lingue); nessun dato finto; il sito resta raggiungibile senza script (0 px di testata dopo 1 500 px a 390, 768, 1024, 1279 su due pagine). Non 5: le decisioni sui testi arabi e le deviazioni del CD non sono firmate. |
| 7 | **Originality** | **4** (4) | Senza logo si riconosce ILE: carta minerale e navy del marchio, Newsreader 300 + Plex, la porta con chiave e gradini — ora anche in colori forzati, con la chiave d'oro sul suo navy —, quattro vie intrecciate nella soglia, tre uscite, il segmentato con «ع». Non 5: il mega-menu non ha la sua firma e la porta non si disegna. |
| 8 | **Interaction Quality** | **4** (3) | Torna a 4, come il sesto giro aveva scritto, con la chiusura del 19: l'ancora 4 chiede «tutti gli stati del DS §6, allineamento a 1 px» e con mouse e tastiera è misurato a 1280, 1366, 1439 in `fr` e `ar` — hover e pressione a 23–25 px dalle parole, anello a 18–20, 9 px dalle pillole corrente e aperta, bordi di ogni link al proprio link (clic reali), chevron 44 ai quattro bordi, indicatore allineato a 0,0 px, frecce del menubar invariate, cassetto e scrim, menu account (1440; 390 `fr` e `ar`; 1024) con Esc a due livelli e focus restituito. Non 5, e da correggere prima di un PASS: con il **tocco** i 4 px di bordo di ogni chevron da 44 vanno al link accanto (36 px effettivi su 44; un tocco 2 px dentro il bordo sinistro dello chevron di «Personnes» porta a `/fr/parcours/`, dentro quello destro a `/fr/entreprises/`), difetto 22, introdotto dal `::before` del 19. |
| 9 | **Mobile** (critica) | **3** (3) | Invariata la condizione posta dal quarto giro per il 4 — la deroga scritta con la sua gamma di viewport —, non soddisfatta; misure identiche al sesto giro: interim **129,2 %** a 390 × 844 (seconda azione a 816,8), **136,3 %** a 375 × 812 (seconda azione a 832,8, 20,8 px sotto la piega), **142,3 %** a 360 × 800; `phase3` 124,1 / 129,0 / 138,4 %. Con JavaScript: bersagli 44, nessuno scroll orizzontale (`scrollWidth` = viewport a 360–768), porta → titolo → lead → azioni a passo 24, H1 arabo a filo. (Il difetto 22 tocca i tablet in orizzontale e i portatili touch, da 80rem: non il telefono.) |
| 10 | **Accessibility** (critica) | **4** (4) | Due chiusure misurate nelle due tavolozze dei colori forzati: chiave 5,80 : 1 col foro nel colore del fondo (20), glifi 16,2–20,3 : 1 e gradini filettati (21); vie a mediana 21 : 1; anello dello chevron nel colore di sistema (15,13 / 14,37 : 1) e a 3,73 : 1 sulla testata fuori dai colori forzati; tastiera completa (menubar LTR/RTL, cassetto, Menu account), reduced-motion completo. Non 5: area di tocco effettiva degli chevron 36 px su 44 (22: ≥ 24, nessuna violazione 2.5.8, ma sotto i 44 del principio 7 del DS); `test_rtl_browser` non eseguito; testi francesi su `/ar/` di 8771. |

## 4. I quattro test (§75–78) — Red Team indipendente

| Test | Domanda | Risposta richiesta | Risposta | Perché, esattamente (elemento, cattura) |
|---|---|---|---|---|
| Generic AI | «Potrebbe essere scambiato per un template generico Claude/AI?» | **NO** | **NO** | Carta minerale e navy del marchio, Newsreader 300 maiuscolo + IBM Plex, la porta con chiave e gradini attraversata da quattro vie intrecciate nella soglia e ancorate a una legenda in vetro, tre uscite con le parole dell'eyebrow, il segmentato con «ع», il lock-up ufficiale (`a7_03_perf_8772_1440.png`, `a7_14_ar_sheet.png`). Il punto fragile resta il pannello del mega-menu. |
| Editorial | «Sembra ancora principalmente una pubblicazione editoriale/legale?» | **NO** | **NO** | Serif solo nell'H1; lead, corpo, legenda, nav, Menu in Plex; CTA a gradiente; il palcoscenico è un diagramma di prodotto. Avvertenza invariata: sotto l'hero riprende la pagina V2 («01 L'ÉCOSYSTÈME», serif; `a7_16_nojs_8770_1024_scrolled.png`). |
| 2026 | «Nascosto il logo, competerebbe con prodotti digitali premium del 2026?» | **SÌ** | **SÌ** | Stati e profondità reggono sulle superfici principali; la barra interim ha ora stati da prodotto (forma interna staccata dalle parole e dalle pillole). Ciò che un prodotto premium non spedisce è la lista di §6: lo chevron che al tocco cede i suoi bordi ai link accanto (22) e l'LCP di 3 s. |
| Too much | «Abbiamo aggiunto effetti inutili solo per sembrare moderni?» | **NO** (altrimenti: elenco di cosa togliere, nell'ordine di `CREATIVE_DIRECTION.md` §6.4) | **NO** | Il commit non aggiunge effetti: una forma di hover più piccola, un padding, tre regole in colori forzati, commenti più corti. |

## 5. Verifiche binarie (tutte devono essere «sì»)

| Verifica | Sì/No | Prova |
|---|---|---|
| Nessuna formulazione vietata (`apps/cms/forbidden.py`), nessun testo bloccato alterato | **Sì** | Diff 213e00f → 265577c: nessun file in `templates/`; `tests/compliance/test_locked_content.py`, `test_public_pages.py`, `test_phase3_texts_not_leaked.py` verdi (nota A). |
| Nessun `style=""`, nessuno script inline, nessun hotlink (CSP) | **Sì** | HTML servito di `/fr/` e `/ar/` (8770, 8771) e `/fr/` (8772): **0** ` style=`, 6 `<script>`, 0 inline eseguibili (solo JSON-LD); `/_design/`: 0 `style=`, 0 inline. CSP servita: `script-src 'self'`, `style-src 'self'`, `font-src 'self'`, `img-src 'self' data:`, `object-src 'none'`, `frame-ancestors 'none'`. Ascoltatore `securitypolicyviolation` installato prima del caricamento: **0** violazioni su 8772 (due passate 4G). La CSP ha bloccato anche il `<style>` di prova del revisore: è attiva. |
| Nessun valore fuori dai token (colori, raggi, ombre, durate, curve) | **Sì** | `tests/frontend/test_v4_tokens.py` e `test_design_docs.py` verdi (nota A); le regole nuove usano `var(--hit-min)`, `var(--radius-sm)`, `var(--min-1)`, `var(--motion-fast)`, `var(--ease-exit)` e colori di sistema (`Canvas`, `CanvasText`); i letterali nuovi sono geometria (`inset: 8px`, `outline-offset: -6px`, `padding-inline: 14px`, `stroke-width: 2px`) — accoppiati a mano, vedi Frontend Lead. |
| «Nessun colore significa mai approvato»: nessun chip `conforme` con croma, nessun verde di verdetto | **Sì** | Nessun chip nelle superfici del gate; l'unico verde è quello del marchio nel lock-up. |
| Nessun dato, contatore, avatar, grafico o KPI finto | **Sì** | Nessun numero nell'hero e nella testata; le vie sono le `entrances()` reali; le uscite le parole dell'eyebrow; il menu account mostra `qa-person`. |
| Coordinate, «svg», «Suspendre le mouvement», etichette di debug: assenti | **Sì** | HTML servito (8770, 8771, `fr` e `ar`; 8772 `fr`): 0 «Suspendre», 0 «svg» nei nodi di testo, 0 `{#`, 0 id duplicati (34 / 40). (Sulla vetrina `/_design/`, pagina di sviluppo, il testo «static/img/icons.svg» documenta lo sprite: non è una superficie del gate.) |
| Reduced-motion: pagina completa, nulla a opacità 0 | **Sì** | §1, riga Reduced-motion: 0 animazioni su due server a quattro larghezze; invisibili solo le correnti e la didascalia chiusa; transizioni a 1e-05 s. |
| Contrasto sul peggior fondo (incluso sotto il vetro) ≥ 4,5 testo / ≥ 3 UI | **Sì** | Colori e fondi del testo invariati dal secondo giro; anello dello chevron 3,73 : 1 sulla testata (e sulla testata sopra l'hero scuro, stesso pixel composto), 15,13 / 14,37 : 1 in colori forzati; la tinta di hover (`--min-1`, 1,08 : 1) non porta informazione. In colori forzati, nelle due tavolozze: chiave 5,80 : 1, glifi 16,2–20,3, gradini ≥ 5,41 contro il pixel oltre il bordo (filetto Canvas), vie mediana 21, uscite e nodi 19,95–21. |
| Prestazioni: JS/CSS ≤ budget, LCP < 2,5 s, CLS < 0,1, INP < 200 ms (4G simulato) | **No** | §0-bis riga 3: LCP **3 032 / 2 940 ms** (la fotografia della porta) > 2 500; CLS 0,0038 / 0,0121 ✓; INP-proxy 120 ms ✓; CSS 99,0 KiB ✓ sul tetto proposto (ma non adottato); JS 36,0 ✓; font **356,1 KB ✗** (proposto 200; scritto 320 per il percorso latino); budget non scritto in §68/DS; HTML non compresso. |
| RTL (ar) a tre larghezze senza proprietà fisiche nel CSS nuovo | **Sì** | Le regole nuove sono `padding-inline` (logica), `inset` (simmetrico, 8 px sui quattro lati), `outline-offset` e `isolation` (simmetrici); in `hero.css` solo colori e tratti sotto `forced-colors`, dentro l'SVG non specchiato (`.doorway { direction: ltr }`). Misurato in `ar`: 28 px d'inchiostro a 1280 / 1366 / 1439, tinta e anello simmetrici (23–25 / 18–19 px), frecce speculari, clic sui bordi, H1 a filo a 390 / 768 / 1440 su 8770 e 8771, menu account del cassetto sotto il riassunto; `tests/i18n/test_rtl_static.py` verde (nota A); `tests/i18n/test_rtl_browser.py` **non eseguito**. |
| Demo page dei componenti coerente (§94) | **Sì, parziale** | `/_design/` (8770, HTML servito, 200): **0** id duplicati (94 id), 0 `style=`, 0 script inline; la testata della vetrina porta la barra interim con i tre chevron da 44 (quindi forma e anello nuovi da 80rem), ma **assenti**, come nei giri precedenti, legenda in vetro, didascalia e porta, e una tavola degli stati dello chevron. `tests/frontend/test_design_showcase.py` verde (nota A). |

**Nota A — esito dei test** (database dedicato `ile_lane4`, mai in parallelo fra loro, mai con `-p no:logging`; il
container `italylegalentry-db-1` è rimasto «Up (healthy)» per tutto il giro):
1. `tests/frontend/test_design_docs.py tests/frontend/test_v4_tokens.py tests/frontend/test_frontend_bundle_is_current.py apps/pages/tests -q`
   — **395 passed in 1 150,61 s**, exit 0 (uscita in `review_a7/pytest_a7_fast.txt`, fuori dal repository).
2. `tests/compliance/test_locked_content.py tests/compliance/test_public_pages.py tests/compliance/test_phase3_texts_not_leaked.py tests/i18n/test_rtl_static.py tests/frontend/test_design_showcase.py tests/frontend/test_svg_wellformed.py tests/frontend/test_template_comments_do_not_leak.py -q`
   — **85 passed in 113,50 s**, exit 0 (`review_a7/pytest_a7_compliance.txt`; rispetto al sesto giro manca
   `test_header_fits_the_narrowest_viewport.py`, che lancia un Chromium proprio).

Le due suite hanno girato una dopo l'altra, in parallelo alle sole sonde funzionali (database diversi: `ile_lane4`
contro `ile` / `ile_qa`), mai alle misure di tempo, prese a suite finite (12:21–12:23). Il «808 passed, 1 xfailed» del
builder (frontend + pages + accounts + cataloghi) non è stato ri-eseguito per intero; la parte richiesta sì.

## 6. Esito

| Esito | Condizione |
|---|---|
| **PASS** | tutte le critiche ≥ 4, tutte le dimensioni di sostegno ≥ 3, quattro test corretti, tutte le verifiche «sì», AFTER materialmente superiore su ogni vista |
| **CONDITIONALLY_READY** | tutte le critiche ≥ 3 e nessuna ≤ 2, al massimo due dimensioni di sostegno ≤ 2, quattro test corretti, verifiche «sì»; correzioni elencate con scadenza; **nessuna propagazione** finché non diventa PASS |
| **BLOCK** | una dimensione critica ≤ 2, **oppure** un test sbagliato, **oppure** una verifica «no», **oppure** AFTER non materialmente superiore |

Esito del gate: ☐ PASS ☐ CONDITIONALLY_READY ☒ **BLOCK**

Motivazione, nell'ordine delle regole: nessuna dimensione critica ≤ 2 (Premium Feel 4, Modernity 4, Clarity 4,
Credibility 4, Mobile **3**, Accessibility 4), nessuna di sostegno ≤ 2 (Visual Depth 4, Motion **3**, Originality 4,
Interaction Quality 4), i quattro test corretti, l'AFTER materialmente superiore al BEFORE su ogni vista. Sulle
dimensioni e sui test il gate sarebbe **CONDITIONALLY_READY** — non PASS: Mobile, critica, è a 3. Lo tiene a **BLOCK**
**una sola** verifica binaria, come nei cinque giri precedenti: le prestazioni (LCP 2,94–3,03 s su 4G lento contro 2,5;
font 356 KB contro i 200 proposti e oltre i 320 scritti per il percorso latino; budget non adottato; HTML non compresso).
Il CSS, da solo, è rientrato: 99,0 KiB, 1 018 byte sotto il tetto proposto.

Giudizio sul giro: delle cinque correzioni del sesto giro **tre sono chiuse sul loro criterio** (19, 20, 21) e i numeri
del README (§4.8, «Sesto giro») sono stati ritrovati — 28 px d'inchiostro con scarto 0, 8 px geometrici fra tinta e
pillola, clic reale su «Forum» che porta a `/fr/forum/`, chevron 44 × 44, aria 240 / 304 px, chiave sul navy, glifi e
gradini in colori forzati, CSS 99,0 KB —; alcune misure del README differiscono per metodo (chiave 5,3 : 1 contro i
5,80 misurati qui, anello «a 20–24 px» contro 18–20 dal bordo esterno dell'anello), nessuna in peggio. Due restano
parziali (3 prestazioni, 6 documentazione). I commenti condensati non hanno cambiato alcuna regola. Nessuna correzione
è regredita sul suo criterio con mouse e tastiera, e le cose vicine che il commit poteva toccare — barra `phase3` a sette
voci (identica: chevron 24 / 28 statici, 11–14 / 16–24 px, aria 31,4 a 1280), pannello, indicatore, cassetto e scrim,
testata senza script, frecce, menu account, reduced-motion, home araba a 1440 e 390 — sono invariate e misurate. Ma la
correzione 19 ha introdotto, con il suo `::before`, una perdita che nessun giro aveva misurato perché nessuno aveva
provato il tocco su questa barra: il **22**.

Correzioni richieste (numerate: prima le correzioni ancora aperte del sesto giro con il loro numero, poi i difetti
nuovi da 22; ognuna con dimensione, elemento, cattura, criterio di chiusura):

3. **Prestazioni — verifica binaria 9.** Dimensione: Frontend Lead. Misura: §0-bis riga 3 (LCP 3 032 / 2 940 ms, la
   fotografia della porta; font 356,1 KB; CSS 101 382 byte gzip in 22 fogli = 99,0 KiB; HTML 43 926 byte non
   compresso). Criterio (invariato, precisato): su 8772, 4G lento + CPU ×4, due passate, **LCP < 2,5 s**, CLS < 0,1,
   INP-proxy < 200 ms; il budget **scritto** in §68/DS e rispettato o con deroga firmata; i font della home entro il
   budget — oggi anche oltre il tetto **già scritto** di 320 KB del percorso latino (DS 2026 §6.2) — o una decisione
   scritta su lock-up (128,9 KB) e corsivo (143,4 KB); la riduzione dei 22 fogli (minificazione misurata dal builder:
   95,3 → 47,8 KB; o concatenazione) con una data; HTML compresso o decisione scritta (BREACH) registrata nel gate.
6. **Documentazione e decisioni** (nessun codice). Invariato: (a) firmare in `CREATIVE_DIRECTION.md` (o in una sua
   appendice di deviazioni) le **quattro** deviazioni da §3.1 / §4.4 — lead non corsivo, titolo senza reveal,
   palcoscenico senza disegno d'ingresso, deroga a 390 con la sua gamma di viewport (interim 129,2 % a 390 × 844,
   136,3 % a 375 × 812 con la seconda azione 20,8 px sotto la piega, 142,3 % a 360 × 800); (b) le decisioni del
   committente/CD: traduzioni arabe di lead, corpo e gloss su `/ar/`, terza colonna del mega-menu, sette voci, carattere
   del lock-up, minificazione dei fogli. Criterio: le firme e le decisioni scritte nel documento del CD.
22. **Al tocco, lo chevron da 44 della barra cede i suoi bordi ai link accanto** (regressione della correzione 19).
    Dimensioni: Interaction Quality (principale), Accessibility (dimensione del bersaglio), Mobile per i tablet in
    orizzontale (minore). Elemento: `static/css/v4/shell.css:373–380`,
    `.main-nav__list:not(:has(> .main-nav__item:nth-child(6))) .main-nav__toggle::before { content: ""; position:
    absolute; inset: 8px; z-index: -1; … }` (con `:367–371`, lo chevron `inline-size: var(--hit-min); position:
    relative; isolation: isolate`), da 80rem, su 8770 (barra interim, quattro voci). Misura (Chrome 153,
    `Emulation.setDeviceMetricsOverride` `mobile: true` + `Emulation.setTouchEmulationEnabled`, un
    `Input.dispatchTouchEvent` `touchStart` / `touchEnd` per ogni pixel del riquadro, alla sua mezza altezza, con un
    ascoltatore `click` in cattura che registra il bersaglio e annulla la navigazione dei link): dei **44 px** di ogni
    chevron solo **36** (`fr` 1366, chevron 0 e 1) o 37 (`ar` 1280 e 1366) aprono il pannello; i **primi 4 e gli ultimi
    4 px** fanno cliccare il **link accanto** — 2 px dentro il bordo sinistro dello chevron di «Personnes» → `A
    /fr/parcours/`, 2 px dentro il destro → `A /fr/entreprises/`; per lo chevron di «Entreprises» → `/fr/entreprises/` e
    `/fr/forum/`; in `ar` gli omologhi —, con raggio del tocco 1, 6 e 12 px identici; a 1440 (`mobile: false`, tocco
    attivo) 38 px su 44. Il mouse non è toccato (clic reali 1 px dentro ogni bordo → lo chevron). **Causa attribuita**
    (foglio costruito, una regola per volta, `fr` 1366): `::before { display: none }` → **43 px su 44**;
    `::before { pointer-events: none }` → **43 su 44**; `padding-inline: 7px` sui link → 36 (il padding non c'entra);
    chevron `position: static` → 42. Sulla barra `phase3` di 8771 (chevron 24 statico, nessun `::before`) 23 px su 24. È il
    riquadro generato dentro il bottone che la regolazione del tocco di Chrome prende come bersaglio del bottone, al
    posto dei suoi 44 px. Effetto: su un tablet in orizzontale o un portatile touch fra 1280 e 1600 px un tocco sul bordo
    di uno chevron lascia la pagina invece di aprire il pannello; il bersaglio effettivo scende a 36 px (≥ 24, nessuna
    violazione 2.5.8; sotto i 44 del principio 7 del DS e del criterio (c) del 19, che chiedeva il riquadro di tocco
    44 × 44 invariato). Riproduzione: `review_a7/r11c_touchscan.py` (scansione), `r11g_radius.py` (raggi 6 e 12, con e
    senza `::before`), `r11h_pe.py` (`pointer-events: none`). Criterio: a **1280, 1366, 1439 e 1440**, `fr` e `ar`, con
    il tocco emulato (raggio 1, 6 e 12), **≥ 43 dei 44 px** di ogni chevron aprono il suo pannello e nessun tocco dentro
    il riquadro dello chevron attiva il link accanto; invariati, misurati sui pixel, gli stati del 19 (tinta ≥ 6 px dalle
    parole, anello ≥ 4, stacco ≥ 2 dalle pillole), i clic del mouse sui bordi e la barra `phase3`. Una via misurata qui:
    `pointer-events: none` sul `::before` (43 / 44 senza toccare la geometria).

Note, non correzioni: l'anello dello chevron (`outline-offset: -6px` su `--radius-sm` 6) ha angoli interni a raggio 0
attorno a una forma raggiata 6 — non concentrico, e diverso dagli anelli raggiati dei link accanto; a 28 / 28 px lo
chevron sta a metà fra la sua parola e la seguente (l'uniformità chiesta dal criterio 17 annulla la vicinanza che lega
la freccia alla sua voce; a 1440 resta 24 / 28): decisione di disegno per il CD; lo chevron non ha uno stato di
pressione distinto dall'hover e, sotto il tocco, la tinta resta dopo il tocco (DS V4 §6: «Touch: nessun hover; lo stato
alternativo è il press»; «hover … solo con `(hover: hover)`») — vale per tutta la barra dal primo giro, non per questo
commit; l'indicatore sotto 90rem è largo quanto la pillola, 14 px oltre l'inchiostro per lato (10 da 90rem): coerente
con la pillola; a 1280–1600 il pannello del mega-menu comincia a y 97, 1 px sopra il piede della testata (98), come nei
giri precedenti; i tre letterali di geometria del 19 (8, −6, 14 px) sono accoppiati a mano fra loro e a
`--focus-ring-width`.

Firma del Creative Director (esito finale, §6 della direttiva): ______ · data/ora: ______

## 7. Ciò che non è stato possibile verificare, e perché (§95)

- **`test_rtl_browser`** e **`test_header_fits_the_narrowest_viewport`**: non eseguiti (pilotano un browser proprio;
  fuori dall'insieme richiesto). Non ri-eseguita per intero la suite «808 passed, 1 xfailed» del builder (nota A).
- **Cinque revisori distinti** (§71): un solo agente ha compilato le sei righe.
- **Il tocco su un dispositivo reale**: il difetto 22 è misurato con il tocco emulato di Chrome
  (`Input.dispatchTouchEvent`, che passa per il riconoscimento dei gesti e la regolazione del tocco del browser); non
  su un tablet reale, e non in Safari/WebKit (iPad), la cui regolazione del tocco è diversa: lì l'effetto può essere
  diverso o assente. Lo stato **prima** della correzione 19 al tocco non è misurabile (i server servono solo 265577c):
  la regressione è dedotta dal foglio costruito che toglie o rende trasparente il solo `::before` (43 / 44).
- **La barra interim con il menu account aperto**: la combinazione (fase 3 chiusa, utente autenticato) esiste solo su
  8770 / `ile`, dove il revisore non ha una sessione e non ne ha creata una (sarebbe una scrittura in quel database).
- **La tavolozza scura dei colori forzati** è l'emulazione di Chrome (`forced-colors: active` + `prefers-color-scheme:
  dark`), non un tema a contrasto elevato reale di Windows: che il `fill` navy dell'arco interno sopravviva anche lì
  (oggi `forced-color-adjust: preserve-parent-color`, non forzato) non è verificato; i minimi per punto delle vie nella
  treccia sono punti di antialias o di due vie sovrapposte, per questo il documento riporta mediane e decimi percentili.
- **Uno screen reader reale** e **dispositivi reali**: nulla ascoltato; rotazioni non misurate (il commit non tocca
  nulla sotto 80rem; cassetto e scrim ri-misurati con clic reali a 390, 768, 1024 e 1279 su due pagine).
- **Lo stato senza JavaScript** su pagine diverse da `/fr/` e `/fr/parcours/`: dedotto dal CSS condiviso.
- **La leggibilità delle uscite arabe** a 12 unità, anche in colori forzati: osservata sulla cattura, non valutata con
  un lettore arabo.
- **I contrasti delle superfici con testo sotto il vetro**: non ri-misurati sui pixel (colori e fondi invariati dal
  secondo giro).

## 8. Metodo e limiti

- Osservazione: Chrome visibile via `scripts/cdp.py` (`Page.attach(url_contains="127.0.0.1:")`, poi `"127.0.0.1:8771"`
  per le sonde con l'account), una sola scheda (`Page.bringToFront`, `visibilityState: visible`, 61 rAF in 500 ms
  all'inizio), sonde sequenziali; viewport emulati 1600 / 1440 / 1439 / 1366 / 1280 × 900, 1366 / 1280 × 1024 con
  `mobile: true` e tocco, 1279 × 800, 1024 × 768, 768 × 1024, 390 × 844, 375 × 812, 360 × 800; emulazioni azzerate a fine
  sonda.
- Script del revisore: `C:\Users\<user>\AppData\Local\Temp\claude\C--tmp-italylegalentry\review_a7\` (`common.py`,
  `sampler.js`, `css_nocomment.py`, `r0_window.py`, `r1_geom.py`, `r1b_geom_it_en.py`, `r2_states.py`,
  `r3_focus_fuse.py`, `r4_fuse.py`, `r5_ind_clicks.py`, `r5b_scan.py`, `r6_8771.py`, `r7_forced.py` (il suo campione
  delle vie a 2,6 px cadeva fuori dal casing ed è sostituito da `r7b_forced.py`), `r7c_exits.py`, `r7d_forced_8771.py`,
  `r8_fc_bar.py`, `r9_mega.py` (da `review_a6/r10_mega.py`), `r9_perf.py` (da `review_a6/r9_perf.py`),
  `r10_panel_nojs.py`, `r11_touch.py` (prima scansione, senza ricaricare fra un tocco e l'altro: scartata),
  `r11b_touch.py`, `r11c_touchscan.py`, `r11d_touchcause.py` / `r11e_touchcause.py` (con `<style>`, bloccati dalla CSP:
  scartati), `r11f_touchcause.py`, `r11g_radius.py`, `r11h_pe.py`, `r12b_reduced_before.py`, `r13_overdark.py`, e
  `p_r1_nojs_header.py`, `p_r3_js_header_drawer.py`, `p_r11_mobile.py`, `p_r12_reduced.py`, `p_r14_account.py` derivati
  da `review_a6`); uscita delle prestazioni `r9_out.txt`; HTML servito in `page_*.html`, `home_8770_*.html`; esiti dei
  test `pytest_a7_fast.txt`, `pytest_a7_compliance.txt`.
- `r13_overdark.py` non ha trovato l'anello con la differenza di pixel (la colonna cambiata era un'altra); la cattura
  `a7_13_overdark_fr_1280_focus_hover_chev1.png` mostra l'anello, e il pixel della testata sopra l'hero scuro è
  `rgb(245, 244, 240)`, lo stesso su cui l'anello è stato misurato a 3,73 : 1.
- Le prestazioni sono state misurate a suite di test finite (le suite hanno girato in parallelo alle sole sonde
  funzionali, su un database diverso).
- Nessun file del repository modificato al di fuori di questa scorecard e delle catture in `review_a7/`. A fine giro la
  scheda è di nuovo su `http://127.0.0.1:8771/fr/espace-reserve/`, autenticata come `qa-person`.

## 9. Verifica indipendente della correzione 22 (commit 442cda6)

Verificatore indipendente (non ha scritto la correzione), 26/09/2026, dopo il commit `442cda6` (albero pulito). Chrome
visibile via `scripts/cdp.py`, una sola scheda, sonde sequenziali, `Network.enable` + `Network.setCacheDisabled` in
testa a ogni sonda, emulazioni azzerate a fine sonda (scheda riportata su `http://127.0.0.1:8770/fr/forum/`). Ogni
numero è una misura del verificatore presa ora. Script e risultati:
`C:\Users\<user>\AppData\Local\Temp\claude\C--tmp-italylegalentry\review_a7\verify_22_fix\` (`w.py`, `s1_matrix.py`,
`s1b_host.py`, `s2_boundary.py`, `s3_states.py`, `s4_mouse.py`, `p1_efp_offset.py`; `s1_results.jsonl`, `s2_*.json`);
catture `docs/qa/chrome/design-v4/after/review_a7/verify_22_fix/` (prefisso `v22_`). Metodo del tocco come al §6,
punto 22: `setDeviceMetricsOverride` (`mobile: true`; a 1440 `mobile: false` come nel settimo giro, più `mobile: true`
a raggio 6) + `setTouchEmulationEnabled`, un `touchStart` / `touchEnd` per pixel del riquadro a mezza altezza, ascoltatore
`click` in cattura; un tocco conta per lo chevron solo se il clic va al suo bottone **e** `aria-expanded` diventa `true`.

| Punto | Esito | Misura |
|---|---|---|
| Regola servita e diff | **sì** | `shell.css` servito da 8770 e da 8771 identico al byte (22 081) al file di `442cda6`; `pointer-events: none` alla riga 380, nella regola `…:not(:has(> .main-nav__item:nth-child(6))) .main-nav__toggle::before`; in pagina il `::before` ha `pointer-events: none`, `inset: 8px`, raggio 6 px. `git diff 265577c 442cda6 -- static/css/v4/shell.css`: **+3 righe** (due di commento e la dichiarazione), nessuna rimossa, nessun'altra proprietà o regola toccata; il resto del commit è documentazione (README, questa scorecard, DS: peso 21,4 → 21,6 KB). |
| Tocco sulla barra interim (8770), per pixel | **≥ 43 / 44 ovunque** (prima 36–38) | 78 scansioni, **3 432 tocchi**: 1280, 1366, 1439, 1440, `fr` e `ar`, raggi 1, 6 e 12, **tutti e tre** gli chevron (1440 `mobile: true` solo a raggio 6). **3 405** aprono il pannello del proprio chevron; **27** cliccano un link, sempre e solo il campione a 0,5 px dal bordo condiviso con il link **seguente** nell'ordine di lettura; nessun altro bersaglio, nessun tocco a vuoto; raggi 1, 6 e 12 identici campione per campione. `fr` 1280 / 1366 / 1439: chevron di «Personnes» 43 / 44 (ultimo campione → `A /fr/entreprises/`), di «Entreprises» 43 / 44 (→ `A /fr/forum/`), di «Projet» 44 / 44 (nessun vicino dopo). `ar` 1280 e 1366: «Personnes» 43 / 44 (primo campione → `A /ar/entreprises/`), «Entreprises» e «Projet» 44 / 44; `ar` 1439: «Entreprises» 43 / 44 (→ `A /ar/forum/`), gli altri 44 / 44. 1440, `fr` e `ar`, `mobile: false` e `true`: **44 / 44** sui tre (da 90rem ci sono 4 px d'aria fra chevron e link seguente). |
| Il pixel residuo è un pareggio di bordo? | **sì** | Scansione fine a passi di 1/8 px da −1,25 a +1,25 px attorno a ogni bordo condiviso, 1280, raggi 1 / 6 / 12 identici. `fr`: la zona di tocco dello chevron di «Personnes» è [727,5; 771,5) sul riquadro [728,125; 772,125) — cede 0,625 px a «Entreprises» e ne prende altrettanti a «Personnes» —; quello di «Entreprises» [870,5; 914,5) ± 0,125 su [871,06; 915,06); «Projet» comincia esattamente a 1144. `ar`: «Personnes» ≈ [479,0; 523,0) su [478,17; 522,17) (cede 0,75–0,875 px, ne prende altrettanti), «Entreprises» ≈ [365,0; 409,0) su [364,84; 408,84). Ogni chevron ha dunque una zona di **44 px ± 0,125**, solo traslata di ≤ 0,875 px verso la griglia dei pixel: non è superficie persa. Controlli dove la correzione non c'entra: sulla stessa barra il bordo link|link «Forum»|«Projet» (1078,97) dà «Projet» già 1,25 px dentro «Forum»; mouse ed `elementFromPoint` (con `mobile: true`) passano al bersaglio seguente 0,875 px prima di ogni bordo, link|link compresi. Sulla barra `phase3` di 8771 (regola invariata, chevron 24 statico, nessun `::before`): **22 / 24** `fr` 1280 (primo campione → il proprio link, ultimo → il seguente), **23 / 24** `ar` 1280, **27 / 28** `fr` 1440, raggi 1 / 6 / 12; in scansione fine la zona del primo chevron `fr` 1280 è ≈ [506,0; 528,5) sul riquadro [505,25; 529,25): la barra invariata perde più di quella corretta. Il «mezzo pixel» del README è esatto in `fr`; in `ar` il residuo arriva a 0,875 px. |
| Stati del 19, sui pixel (mouse e tastiera, senza tocco) | **invariati** | 1280 (e 1439), `fr` e `ar`, tre chevron: tinta di hover `rgb(236, 235, 230)` sul `::before`, riquadro trasparente, a **23–25 px** dall'inchiostro vicino (criterio ≥ 6); pressione identica; anello `2px solid rgb(29, 138, 147)`, `outline-offset: -6px`, `box-shadow: none`, `:focus-visible` vero, 36 px, a **18–20 px** dall'inchiostro (≥ 4); su `/fr/entreprises/` e `/ar/entreprises/` («Entreprises» `aria-current`, pillola `rgb(236, 235, 230)`) **9 px** fra la tinta e la pillola, sui due lati (≥ 2). Gli stessi numeri del §0-bis (19). Il README dice «24–37 / 20–24 / 8»: altro metodo, tutti sopra i criteri. Catture `v22_fr_1280_hover_chev1.png`, `v22_fr_1280_pressed_chev1.png`, `v22_fr_1280_focus_chev1.png`, `v22_fr_1280_current_hover_chev0.png` e le omologhe `ar`. |
| Clic del mouse sui bordi | **invariati** | **252 clic** reali (1 e 3 px dentro i bordi sinistro e destro, 1 px dentro alto e basso, di ogni link e di ogni chevron; 1280, 1366, 1439; `fr` e `ar`): 252 sul proprio bersaglio, ogni clic sullo chevron apre il proprio pannello. Clic che navigano, 1280, 3 px dentro i bordi dei link accanto agli chevron: `/fr/parcours/`, `/fr/entreprises/` (×2), `/fr/forum/`, `/fr/le-projet/` e gli omologhi `/ar/`. |
| Barra `phase3` (8771) | **invariata** | Chevron 24 × 44 statici a 1280, 28 a 1440; la regola della barra interim non vi si applica (`::before` con `pointer-events: auto`, regola esclusa dalle liste di sette voci); tocco come sopra. |

Esito della correzione 22: **CHIUSA**. Il criterio «≥ 43 dei 44 px a 1280, 1366, 1439 e 1440, `fr` e `ar`, raggi 1, 6
e 12» è soddisfatto in ogni caso (43 o 44). La clausola «nessun tocco dentro il riquadro attiva il link accanto» vale
fuori dalla striscia di ≤ 0,875 px sul bordo condiviso: è la tolleranza di un pixel che il criterio stesso concede, lo
chevron la riprende sul bordo opposto (zona di 44 px ± 0,125), e lo stesso pareggio, più largo, c'è sulla barra
`phase3` invariata e sui bordi link|link: un pareggio di bordo di Chrome, non un bersaglio che la forma sottrae.
Regressioni: **nessuna**. L'esito del gate (BLOCK per le sole prestazioni, §6) non cambia. Limiti: solo il tocco
emulato di Chrome (nessun dispositivo reale, nessun WebKit); scansione fine solo a 1280; stati del 19 a 1280 e 1439,
non a 1366; 1440 con `mobile: true` solo a raggio 6.
