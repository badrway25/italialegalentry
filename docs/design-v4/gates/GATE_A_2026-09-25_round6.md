# GATE A — Homepage (hero) + Navbar · scorecard del 26 settembre 2026 — **sesto giro**

Compilata sul modello `docs/design-v4/GATE_SCORECARD_TEMPLATE.md` (§71–78 della direttiva). Regole
applicate: **nessuna media** (§74); **l'implementatore non vota** (§72); ogni punteggio cita ciò che il
revisore ha **osservato in Chrome visibile** (§70) — Google Chrome 153, CDP 9222, `scripts/cdp.py`, una sola
scheda, sonde sequenziali, `Network.enable` + `Network.setCacheDisabled` in testa a ogni sonda. Le misure sono
`getBoundingClientRect` / `getComputedStyle` / `elementFromPoint` / `getScreenCTM` / `getPointAtLength` /
`Range.getClientRects` / `performance.getEntriesByType` / `PerformanceObserver` (LCP, layout-shift, longtask, event,
installati con `Page.addScriptToEvaluateOnNewDocument`) / campionamento a ogni `requestAnimationFrame` (storia per
fotogramma del palcoscenico) / `document.getAnimations()` / eventi reali (`Input.dispatchMouseEvent` — anche
`mouseWheel` per scorrere senza JavaScript —, `Input.dispatchKeyEvent` con `Emulation.setFocusEmulationEnabled`,
`Emulation.setDeviceMetricsOverride` con `mobile: true`, `Emulation.setTouchEmulationEnabled`,
`Emulation.setEmulatedMedia` per reduced-motion e per i colori forzati **nelle due tavolozze** — `forced-colors: active`
con `prefers-color-scheme: light` e `dark` —, `Emulation.setScriptExecutionDisabled` per lo stato senza JavaScript,
`Network.emulateNetworkConditions` 150 ms / 1,6 Mbit/s / 750 kbit/s + `Emulation.setCPUThrottlingRate` 4 per il 4G
lento) e letture di pixel con Pillow sulle catture del revisore. Le catture di questo giro stanno in
`docs/qa/chrome/design-v4/after/review_a6/` (prefisso `a6_`, ignorate da git: `git status` resta vuoto); i percorsi
sono relativi alla radice del repository. Ogni numero di questo documento è una misura del revisore presa in questo
giro (26/09, 10:36–11:05); i numeri del README e dei giri precedenti sono citati solo per confronto.

Nota sulle misure: la scheda riportava `devicePixelRatio` **1** (finestra 1905 × 1012, interno 1889 × 861, 61 rAF in
500 ms, `visibilityState: visible`); tutte le emulazioni con `deviceScaleFactor: 1`, azzerate a fine sonda (viewport,
tocco, media, rete, CPU, focus, esecuzione degli script).

Nota sulla scheda: all'inizio i target di 9222 contenevano **una** pagina di progetto,
`http://127.0.0.1:8771/fr/espace-reserve/`, autenticata come `qa-person`. Le sonde su 8770 e 8772 l'hanno disconnessa
da 8771 (il cookie di sessione è per host, non per porta). Il revisore l'ha ri-autenticata con
`scripts/qa_chrome_signin.py` (sessione lato server, nulla digitato) per le sole sonde del menu account, poi di nuovo a
fine giro: la scheda resta su `/fr/espace-reserve/` con il riassunto «qa-person».

Manipolazioni del DOM nella scheda, dichiarate (tutte annullate subito, nessun file toccato): `style.clipPath = 'none'`
e poi `''` su `.doorway__routes` per confrontare i pixel con e senza il ritaglio nuovo (`r2_nojs_clip.py`,
`r2b_noise.py`); `document.getAnimations().forEach(a => a.pause())` prima di alcune catture, per togliere il rumore
della corrente dal confronto dei pixel (pagina ricaricata dopo).

Questo documento verifica, correzione per correzione, le correzioni del quinto giro (`gates/GATE_A_2026-09-25_round5.md`,
§6: 3 e 6 ancora aperte, 16–18 nuove), ciascuna contro il **suo** criterio di chiusura; poi cerca i difetti introdotti
dalle correzioni (e quelli che esse hanno reso visibili), ri-assegna le dieci dimensioni, i quattro test e le verifiche
binarie.

---

## 0. Identità del gate

| Campo | Valore |
|---|---|
| Gate | **A** |
| Superfici | Homepage pubblica `/fr/`: hero «il portico» (porta, quattro vie, legenda in vetro con didascalia, titolo, lead, CTA; uscite etichettate nella variante interim) + navbar (barra istituzionale con controllo lingua e accesso/menu account, testata, indicatore, mega-menu, cassetto con segmentato); `/ar/` per RTL; `/fr/parcours/` come seconda pagina pubblica per la testata senza JavaScript; `/fr/entreprises/` per lo stato «pagina corrente» della barra; la vetrina `/_design/` |
| URL / account | **8770** (`ile`, fase 3 chiusa → variante **interim**: eyebrow, titolo editoriale, tre uscite etichettate, **quattro** voci: Personnes ⌄ · Entreprises ⌄ · Forum Vénétie–Maroc · Projet ⌄); **8771** (`ile_qa`, fase 3 aperta → variante `phase3`, **sette** voci; `qa-person` per menu account e cassetto); **8772** (lo stesso codice di 8770 dietro WhiteNoise gzip) per ogni misura di prestazione. Verificato all'inizio: `v4/hero.css` (md5 `04cefe03`), `v4/shell.css` (`1a1c9bc3`), `components.css` (`e5b5cb52`), `main.js` (`02e6d585`), `head.js` (`d1d44e39`) serviti da 8770, 8771 e 8772 identici ai file dell'albero (8772 con `Content-Encoding: gzip`, `v4/shell.css` 6 362 byte); l'HTML servito porta i segni del commit: `<clipPath id="doorway-routes-arch">` una volta su 8770 e 8771, `fr` e `ar`; `doorway--exits` solo su 8770; 34 id (8770) e 40 (8771), **0** duplicati. |
| Commit sotto revisione | **213e00f** (albero pulito: `git status` vuoto all'inizio; alla fine l'unico file nuovo è questa scorecard, non tracciata). Sulle superfici del gate, da d475749: `static/css/v4/hero.css` (+13: senza JavaScript sotto 80rem `clip-path: url("#doorway-routes-arch")` su `.doorway--exits .doorway__routes`; in colori forzati `.doorway__inner { fill: Canvas; stroke: CanvasText }`, `.route__casing { stroke: Canvas; stroke-opacity: 1 }`, `.exit__node { fill: CanvasText }`), `static/css/v4/shell.css` (+28: fra 80 e 90rem, sulle barre di cinque sezioni o meno, chevron `position: relative; z-index: 1; margin-inline: -7px` e anello interno `outline-offset: calc(-1 * (width + offset))` con compagno `inset`; sotto 80rem `html.no-js .site-header { position: relative }`), `templates/pages/home/_hero.html` (+3: il `<clipPath>` e un commento), `docs/design/DESIGN_SYSTEM_2026.md` (pesi dei fogli). Nessun testo toccato. |
| Revisione | **sesto giro** (quinto: `gates/GATE_A_2026-09-25_round5.md`, su d475749, BLOCK per la sola regola delle prestazioni; quarto: `…_round4.md`, su 156db5f; terzo: `…_round3.md`, su dd29168; secondo: `…_round2.md`, su d99f2bb; primo: `GATE_A_2026-09-25.md`, su c6f3503) |
| Implementatore (non vota) | Claude (sessione principale) |
| Revisore indipendente | agente separato (nessuna modifica a codice, template, fogli, script o test; nessun riavvio di server; nessun pacchetto installato; nessuna credenziale digitata; nessun modulo inviato; nessuna scheda aperta o chiusa) |
| Data e ora della revisione | 26 settembre 2026, ore 10:36–11:05 (misure in Chrome e test); scorecard scritta subito dopo |

## 0-bis. Le correzioni del quinto giro — verifica una per una, contro il loro criterio

| # | Correzione (quinto giro) | Stato | Prova (misura o cattura) |
|---|---|---|---|
| 3 | Prestazioni — verifica binaria 9 | **PARZIALE** (invariata; il CSS ora **oltre** il tetto proposto) | 8772, 1440 × 900, cache spenta, 4G lento + CPU ×4, due passate, a suite di test finite: **LCP 3 284 / 3 084 ms** — `image.doorway__img` (`doorway-800.webp`, 133 126 px²); FCP 2 440 / 1 760; DCL 3 134 / 3 412; load 3 971 / 3 900; CLS **0,0032 / 0,0351** (la voce maggiore 0,0304 a 1 924 ms nella seconda); long task max **919** / 364 ms (13 / 13 task); 0 violazioni CSP, 0 errori. **Pesi** (identici nelle due): CSS **22 fogli, 102 441 byte gzip = 100,04 KiB** (391,5 KiB nudi) — **41 byte sopra** il tetto proposto di 100 KiB (102 400 byte); JS **8 file, 36,0 KB**; font **6 file, 356,1 KB** (Newsreader tondo 128,9 precaricato, Newsreader **corsivo 143,4**, Plex Sans 22,1 + 23,6 + 23,7, Plex Mono 14,4); immagini 5 file, 79,5 KB (foto 76,8, precaricata, richiesta a 271 / 324 ms, finita a 3 069 / 2 921); HTML **43 926 byte non compresso**; **42 richieste**. Senza limiti: LCP 456 ms (la foto), CLS 0,0002. **INP-proxy deliberato** (seconda passata, CPU ×4: hover su una riga della legenda, clic sul chevron «Entreprises», Esc, hover sul secondario): evento più lungo **96 ms** (`pointerdown` / `mousedown` del chevron), gli altri ≤ 48. I numeri del README (3 336 / 3 392 / 3 140 / 3 056 ms, CSS «100,0 KB») sono ritrovati entro la varianza (≈ 300 ms). La leva misurata dal builder (fogli senza commenti a `collectstatic`: 95,3 → 47,8 KB) è scritta come decisione del committente, non presa; il budget resta «proposto al CD», non scritto in §68/DS. |
| 6 | Documentazione e decisioni | **PARZIALE** (invariata) | `docs/design-v4/CREATIVE_DIRECTION.md`: ultimo commit **6718f1a** (24/09); le **quattro** deviazioni da §3.1 / §4.4 (lead non corsivo, titolo senza reveal, palcoscenico senza disegno d'ingresso, deroga a 390 con la sua gamma di viewport) restano scritte solo nel README, nessuna firmata; la gamma della deroga non è scritta. Pendenti anche: traduzioni arabe di lead, corpo e gloss su 8771 `/ar/`, terza colonna del mega-menu, sette voci, carattere del lock-up, e ora la minificazione dei fogli. |
| 16 | Senza JavaScript, sotto 80rem, la testata appiccicosa copre la pagina | **CHIUSA** | **(a) Testata.** `Emulation.setScriptExecutionDisabled`, `html.no-js`, scroll con `mouseWheel` reale di 1 500 px. **8770 `/fr/`**: a **390 × 844** (`mobile: true`) la testata è `position: relative`, 0–1 014 px a y 0; dopo lo scroll `scrollY` 1 500, testata −1 500…−486, **0 px visibili**; portato il titolo nel viewport, `elementFromPoint` al suo centro = uno `<span>` **dentro l'H1** (non nella testata). A **768 × 1024**, **1024 × 768** e **1279 × 800**: 33–979 → −1 467…−521, **0 px visibili**, centro del titolo = titolo. A **1440**: `position: sticky`, 65 px a ogni scroll (invariata). **8770 `/fr/parcours/`**: stessi numeri a 390 / 768 / 1024 / 1279 (0 px visibili dopo 1 500), centro di `H1.page-header__title` = l'H1; a 1440 sticky da 65. **8771** (`phase3`, sette sezioni): a 1024 la testata senza script è 33–1 474 e dopo 1 500 px ne restano 0; a 390 0–1 509 e ne restano **9 px** (≤ 110). **Con JavaScript nulla è cambiato** (`r3_js_header_drawer.py`, 8770 `/fr/` e `/fr/parcours/`): `position: sticky` a 390, 768, 1024, 1279 e 1440; dopo lo scroll testata 0–57 (390) e 0–65 (768–1279); clic reale su «Menu» → cassetto e scrim a **57 / 57** e **65 / 65** (piede della testata), `visibility: visible`, scrim opacità 1; lock-up e «Menu» colpiti da `elementFromPoint` al loro centro in tutti i 16 casi. **(b) Il ritaglio delle vie.** `clip-path` calcolato `url("#doorway-routes-arch")` **solo** senza JavaScript a 390, 768, 1024 e 1279; `none` a 1440 e **con** JavaScript a ogni larghezza. Con le animazioni ferme, togliere e rimettere il ritaglio cambia i pixel **solo a x ≥ 530 unità**: 1024 → 977 px cambiati, **0** a sinistra di x 530; 1279 → 1 130 / **0**; 768 → 465 / **0**; 390 → 373, di cui 15 sulla colonna x 530 (il pixel a cavallo del bordo, scala 0,28). Nessun altro disegno perso: nodi e anelli d'origine (x 34, y 348–486) dentro il rettangolo 0–531 × 0–520; porta, fotografia, chiave e gradini fuori dal gruppo ritagliato. Senza ritaglio (misura del confronto) il casing arrivava a x 618. Cattura `a6_16b_nojs_stage_1024_zoom.png`: sulla pietra dopo l'arco non resta nulla. (Senza script, sotto 80rem, dentro il navy si vedono le due salite del tracciato con uscite fino a y 200 e 300 — tratto sfumato più casing —, mentre con JavaScript le vie finiscono in piano a x 531: un disegno diverso fra i due stati, dentro l'arco; non è nel criterio e non lo conto come difetto.) |
| 17 | Il ritmo della barra interim a 1280–1439 | **CHIUSA** sul criterio — gli stati del chevron confluiscono nel difetto nuovo **19** | 8770, `Range.getClientRects` sul testo e riquadro dell'`svg` del glifo, in ordine visivo: a **1280, 1366 e 1439**, in `fr` **e** in `ar`, le sei distanze d'inchiostro della barra (parola → glifo → parola … «Forum» → «Projet» …) sono **14,0 px tutte**, scarto **0** (criterio ±4). I tre chevron sono **44 × 44**, `position: relative`, `z-index: 1`, `margin-inline-start: -7px`; `elementFromPoint` ai quattro bordi (1 px dentro) e al centro di ciascuno = il chevron. A **1440**: 24 / 28 / 24 (scarto 4), chevron statici. Aria fra lock-up e lista: **338,3 px** (`fr`) e **402,4** (`ar`) a 1280–1439 (la lista si è accorciata di 42 px), 370 / 441,2 a 1440. Indicatore che trasla: all'hover di ciascuno dei quattro link, bordo sinistro e destro dell'indicatore = bordi del link a **0,0–0,1 px**, in `fr` e `ar`, a 1280 e 1439. Pannello aperto dal chevron: `top` 97 contro il piede della testata a 98, larghezza 0–1 265 (1280) e 0–1 424 (1439), come prima. Frecce del menubar a 1280 `fr` / `ar` e 1439 `fr`: le stesse sequenze del quinto giro (↓ ↓ ↓, ↑ × 4, → × 4 con giro, dal chevron → ← ↓ ↑ Esc, dal pannello → ← con chiusura), `scrollY` 0 dopo ogni tasto. **Ma** il riquadro da 44 che ora copre il padding dei vicini porta con sé gli stati visibili del chevron — pillola di hover e di pressione, anello — fin contro le parole vicine, e 7 px di ciascun link vicino passano al chevron: difetto **19**. |
| 18 | Colori forzati: le salite dentro l'arco interno a 1,38 : 1 | **CHIUSA** sul criterio — la chiave confluisce nel difetto nuovo **20** | 8770 `/fr/` e `/ar/`, 1440, `forced-colors: active` in tavolozza **chiara** e **scura**: `.doorway__inner` `fill` rgb(255, 255, 255) / rgb(0, 0, 0) (Canvas), `stroke` CanvasText; `.route__casing` Canvas, `stroke-opacity` 1; `.route__line` CanvasText; `.exit__node` CanvasText. Contrasto per punto (800 punti per via con `getPointAtLength`, pixel della via contro il pixel del casing a 2–3 px in perpendicolare): **salite** mediana **21,0 : 1** (decimo percentile 13,8–15,9) nelle due tavolozze e nelle due lingue; **treccia dentro l'arco** mediana 10,96–21 (decimo percentile 3,46–6,4); **sulla fotografia** mediana 5,64–21 (decimo percentile 3,95–13,1); i minimi (1,0–2,8) sono punti di antialias o di sovrapposizione di due vie nella treccia. Su 8771 (`phase3`) arco interno Canvas e vie CanvasText allo stesso modo. Catture `a6_18_forced_light_8770_fr_stage.png`, `a6_18_forced_dark_8770_fr_stage.png`, `…_lower.png`: salite, treccia e uscite si leggono. Il prezzo: in tavolozza chiara la chiave d'oro, che stava sul navy, sta ora sul bianco (difetto **20**). |

## 1. BEFORE / AFTER (§73)

| Vista | BEFORE | AFTER | Verdetto «materialmente superiore» (sì/no + una frase) |
|---|---|---|---|
| Desktop 1440 | `docs/qa/chrome/design-v4/before/01_home.png` (V2 interim); quinto giro `after/review_a5/a5_13_exits_8770_fr_1440.png` | `a6_03_perf_8772_1440.png`, `a6_14_home_8770_ar_1440.png`, `a6_14_home_8771_ar_1440.png` | **Sì.** A 1440 il commit non tocca nulla di visibile con JavaScript (chevron statici, ritmo 24 / 28, nessun ritaglio): la composizione del quinto giro, invariata. |
| Desktop 1280 · 1366 · 1439 | quinto giro `a5_6c_header_8770_1280_zoom.png` (54 px fra sezioni con chevron, 14 senza) | `a6_17_states_sheet.png`, `a6_17_focus_sheet.png`, `a6_19_fused_sheet.png` | **Sì, con riserva.** A riposo la barra ha ora un ritmo uniforme (14 px ovunque, «Forum Vénétie–Maroc» e «Projet» non si leggono più come una voce sola). In hover, pressione e focus il chevron disegna però la sua pillola e il suo anello fin contro le parole vicine, e accanto alla pillola di un link corrente o aperto si fonde con essa (difetto 19). |
| Tablet 768 · 1024 | quinto giro `a5_13b_js_8770_1024.png`, `a5_13b_nojs_8770_1024_stagezoom.png` | `a6_14_home_8770_fr_768.png`, `a6_16c_js_drawer_1024.png`, `a6_16b_nojs_stage_1024_zoom.png`, `a6_16_nojs_8770_1024_scrolled.png` | **Sì.** Con JavaScript invariata; senza JavaScript la pagina si raggiunge (testata che scorre via) e sulla pietra oltre l'arco non resta più alcun casing. |
| Mobile 390 | quinto giro `a5_14_home_8770_fr_390.png`, `a5_nojs_8770_390_scrolled.png` (testata da 1 014 px sempre sullo schermo) | `a6_14_home_8770_fr_390.png`, `a6_16c_js_drawer_390.png`, `a6_16_nojs_8770_390_scrolled.png` | **Sì.** Con JavaScript invariata (interim 129,2 %, seconda azione a 816,8); senza JavaScript il contenuto si raggiunge dopo il menu. |
| Stato interattivo (hover/focus/press/aperto) | quinto giro `a5_10_ring_chevron_8770_1280_zoom.png`, `a5_09_drawer_account_fr_390.png` | `a6_17_fr_1280_hover_chev1.png`, `a6_17_fr_1280_pressed_chev1.png`, `a6_17_fr_1280_focus_chev1.png`, `a6_17_ar_1280_focus_chev1.png`, `a6_19_fr_1280_current_entreprises_hover_chev0.png`, `a6_09_drawer_account_fr_390.png` | **Sì, con riserva** (contro il BEFORE V2, che questi stati non li aveva): cassetto, scrim, menu account, frecce, indicatore invariati e misurati. Ma **contro il quinto giro** gli stati del chevron fra 80 e 90rem sono peggiorati (difetto 19): pillola di hover e di pressione a 1–2 px dalle parole vicine (prima 7), anello a 2–3 px, pillola fusa con quella del link corrente o aperto. |
| RTL (ar) | quinto giro `a5_13_exits_8770_ar_1440.png`, `a5_14_home_8770_ar_390.png` | `a6_14_home_8770_ar_1440.png`, `a6_14_home_8770_ar_390.png`, `a6_14_home_8771_ar_1440.png`, `a6_17_ar_1280_hover_chev1.png` | **Sì.** H1 a filo (inchiostro = blocco, Δ 0) a 390 / 768 / 1440 su 8770 e 8771; barra araba a 14 px uniformi (con la stessa riserva del chevron: la pillola tocca «منتدى» e «الشركات»). |
| Reduced-motion | quinto giro `a5_07_reduced_*` | `a6_07_reduced_8770_1440.png`, `a6_07_reduced_8770_390.png` | **Sì.** `getAnimations()` **0** a 1440, 1280, 1024 e 390 su 8770 e 8771; titolo `none`; uscite a opacità 1; invisibili solo le quattro correnti e la didascalia chiusa; fotografia ferma a `scale(1.06)`; `transition-duration` della testata 1e-05 s. |
| Forced-colors | quinto giro `a5_07_forced_8770_exits_zoom.png` (salite 1,38 : 1) | `a6_18_forced_light_8770_fr_stage.png`, `a6_18_forced_dark_8770_fr_stage.png`, `a6_18_forced_light_8770_fr_lower.png`, `a6_18_forced_dark_8770_fr_lower.png`, `a6_17_fc_light_1280_focus_chev1_zoom.png` | **Sì, con due riserve.** Le vie si leggono in ogni tratto nelle due tavolozze; in tavolozza **chiara** la chiave d'oro sta sul bianco a 2,63 : 1 con il foro dell'anello diventato un punto navy (20, effetto della correzione 18), e glifi della legenda e gradini restano sotto 1,8 : 1 (21, preesistente). |

## 2. I ruoli (§71) — cinque firme, cinque punteggi indipendenti

Limite dichiarato: **un solo agente revisore** ha compilato le sei righe (la direttiva chiede cinque revisori
distinti); per ogni dimensione vale il punteggio più basso fra i ruoli che la giudicano.

| Ruolo | Cosa giudica in via primaria | Firma | Note |
|---|---|---|---|
| Creative Director | Premium Feel · Modernity · Originality · Visual Depth · coerenza con `CREATIVE_DIRECTION.md` | revisore indipendente, 26/09/2026, sesto giro | Chiuso il ritmo disuguale della barra (17) e il casing sulla pietra senza script (16b). Contro: gli stati del chevron fra 80 e 90rem non sono stati ridisegnati per la nuova geometria (19); in colori forzati chiari la chiave del marchio perde il suo fondo (20). Deviazioni non firmate, ancora quattro. |
| UX Lead | Clarity · Interaction Quality · Mobile · efficienza (§89) | revisore indipendente, 26/09/2026, sesto giro | Chiuso il sito irraggiungibile senza script (16: 0 px di testata dopo lo scroll su due pagine pubbliche a quattro larghezze). Contro: fra 80 e 90rem i primi e gli ultimi 7 px dei link vicini a un chevron aprono il pannello della sezione accanto (un clic 3 px dentro «Forum Vénétie–Maroc» apre quello di «Entreprises»), la pillola del chevron si fonde con quella del link corrente (19); la deroga a 390 non è scritta. |
| Motion Lead | Motion · budget (§67) · pattern (DS §7) · reduced-motion | revisore indipendente, 26/09/2026, sesto giro | Nessun effetto del commit sul moto; 0 fotogrammi ripresi nelle due passate in 4G lento (430 e 632 fotogrammi). Contro, invariati: il disegno d'ingresso prescritto da CD §3.1 / §4.4.1 non c'è; la testata transisce ancora `min-block-size` (`static/css/v4/shell.css:128`). Reduced-motion completo. |
| Frontend Lead | token (DS): nessun valore arbitrario · CSP · nessun `style=""` · prestazioni (§68) | revisore indipendente, 26/09/2026, sesto giro | 0 `style=`, 0 script inline eseguibili, 0 violazioni CSP, 0 id duplicati, test verdi. Contro: LCP 3,08–3,28 s su 4G lento; CSS **100,04 KiB**, 41 byte sopra il tetto proposto; font 356 KB; HTML non compresso; budget non adottato. Il valore `-7px` della correzione 17 ripete a mano il padding dei link a 80–90rem (`padding-inline: 7px`, stesso foglio): un letterale accoppiato, non un token. |
| Accessibility Reviewer | Accessibility · contrasto misurato · tastiera · screen reader · RTL · forced-colors | revisore indipendente, 26/09/2026, sesto giro | Chiusi: contenuto raggiungibile senza script (16), salite leggibili in colori forzati (18, 21 : 1). Misurati: anello del chevron visibile anche in colori forzati (Highlight di sistema, disegnato dentro). Contro, minori: chiave 2,63 : 1 in colori forzati chiari (20), glifi della legenda 1,73 : 1 e gradini 1,2–1,45 : 1 nella stessa tavolozza (21, preesistenti); anello del chevron a 2–3 px dalle parole vicine (19, non una violazione WCAG). `test_rtl_browser` non eseguito. |
| Red Team indipendente (§75–78) | i quattro test | revisore indipendente, 26/09/2026, sesto giro | Vedi §4: NO · NO · SÌ · NO. |

## 3. Le dieci dimensioni (§74) — scala 1–5 con ancore

**Critiche** (una sola ≤ 2 → **BLOCK**): Premium Feel · Modernity · Clarity · Institutional Credibility ·
Accessibility · Mobile. **Di sostegno** (≤ 2 → al massimo CONDITIONALLY_READY): Visual Depth · Motion ·
Originality · Interaction Quality. Fra parentesi il punteggio del quinto giro.

| # | Dimensione | Punteggio | Osservazione (cosa, dove, in Chrome) |
|---|---|---|---|
| 1 | **Premium Feel** (critica) | **4** (4) | Chiusi i due dettagli che il quinto giro citava: il ritmo della barra interim (14 px uniformi a 1280–1439, `fr` e `ar`) e le salite in colori forzati. A 1440 la composizione è quella del quinto giro (treccia sotto la chiave, tre uscite in piano con alone, nulla di dipinto che sparisce: 0 fotogrammi nascosti in 430 e 632 fotogrammi sotto 4G lento). Restano «1–2 dettagli da rifinire», ancora 4: fra 80 e 90rem la pillola di hover del chevron tocca le parole vicine (1–2 px contro i 12–17 misurati a 1440) e si fonde con la pillola del link corrente (`a6_19_fused_sheet.png`: «⌄ Entreprises» come un'unica forma sulla pagina `/fr/entreprises/`, difetto 19); in colori forzati chiari la chiave sta sul bianco (20, modo non predefinito). Non 5: il pannello del mega-menu resta un elenco bianco a due colonne e il componente firma non ha più il suo momento d'ingresso. |
| 2 | **Modernity** (critica) | **4** (4) | Grammatica 2026 coerente e invariata: barra 32 + testata 64 → 56 in vetro, indicatore che trasla (allineato al link a 0,0–0,1 px), mega-menu dal bordo, segmentato, Menu V4, cassetto dal piede misurato della testata. Non 5: nessuna transizione di pagina; il disegno d'ingresso della porta è tolto. |
| 3 | **Visual Depth** | **4** (4) | Ordine dei livelli giusto in ogni stato misurato (testata sopra; cassetto e scrim dal suo piede in 16 casi su 16; pannello dal piede della barra). Il `z-index: 1` del chevron resta dentro il contesto della testata (`position: sticky; z-index: 20`): non può salire sopra il menu account della barra istituzionale. Non 5: la luce (mesh) resta sotto la soglia di percezione. |
| 4 | **Motion** | **3** (3) | Il commit non tocca il moto: 0 fotogrammi ripresi, corrente dal primo fotogramma, reduced-motion completo (0 animazioni su due server a quattro larghezze). La dimensione resta a 3 per le due ragioni misurate nel quinto giro, invariate: (a) il disegno d'ingresso prescritto (CD §3.1: arco 900 ms → quattro vie 900 ms con stagger 120 → legenda 200; §4.4.1) non c'è, deviazione non firmata; (b) la testata transisce `min-block-size` (`static/css/v4/shell.css:128`), proprietà di layout — l'ancora 4 chiede 0 layout. |
| 5 | **Clarity** (critica) | **4** (4) | Un H1, lead Plex, corpo, una primaria + una secondaria, legenda con parola e gloss; tre uscite leggibili; la barra interim si legge ora come quattro voci distinte a riposo. Non 5: su 8771 `/ar/` titolo inglese, lead, corpo e gloss francesi sotto parole arabe (decisione pendente); fra 80 e 90rem, in hover, la pillola del chevron di una sezione si fonde con la voce seguente (19). |
| 6 | **Institutional Credibility** (critica) | **4** (4) | Senza JavaScript il sito pubblico non si riduce più al menu: la testata scorre via e il contenuto si raggiunge su `/fr/` e `/fr/parcours/` (16). Lock-up e «Menu» mai coperti (16 / 16 casi); lock-up con 338,3 px d'aria (interim) e 31,4 (`phase3`) a 1280–1439; nessun dato finto; testi bloccati invariati. Non 5: le decisioni sui testi arabi e le deviazioni del CD non sono firmate. |
| 7 | **Originality** | **4** (4) | Senza logo si riconosce ILE: carta minerale e navy del marchio, Newsreader 300 + Plex, la porta con chiave e gradini, quattro vie intrecciate nella soglia, tre uscite, il segmentato con «ع». Non 5: il mega-menu non ha la sua firma e la porta non si disegna. |
| 8 | **Interaction Quality** | **3** (4) | L'ancora 4 chiede «tutti gli stati del DS §6, allineamento a 1 px»; fra 80 e 90rem, sulla barra interim, **gli stati del chevron non sono allineati** con ciò che hanno accanto dopo la correzione 17 (difetto 19, misurato sui pixel a 1280, 1366, 1439, `fr` e `ar`): la pillola di hover e di pressione (`--min-1`, 44 × 44, raggio 6) arriva a **1–2 px** dall'ultimo pixel scuro della parola precedente e dal primo della seguente (a 1440: 12–17 px); l'anello, disegnato dentro, a **2–3 px**; sulla pagina in cui «Entreprises» è corrente, o col suo pannello aperto, l'hover sul chevron di «Personnes» fonde le due pillole in una sola forma che comincia prima del chevron e finisce dopo «Entreprises»; i 7 px di bordo dei link accanto a un chevron appartengono al chevron (un clic reale 3 px dentro il riquadro di «Forum Vénétie–Maroc» apre il pannello di «Entreprises» e lascia l'URL su `/fr/`; stesso esito in `ar`). È l'ancora 3: «ogni elemento interattivo ha hover/focus/press, alcuni non allineati (§93)». Il resto è al livello 4 e misurato: frecce del menubar invariate a 1280 e 1439 in LTR e RTL, indicatore allineato a 0,1 px, cassetto e scrim, Menu account sotto il riassunto (1440; 390 `fr` e `ar`; 1024) con Esc a due livelli e focus restituito. Torna a 4 con la chiusura del 19. |
| 9 | **Mobile** (critica) | **3** (3) | Il difetto 16 (senza JavaScript la testata copriva il telefono) è chiuso: a 390 × 844 senza script 0 px di testata dopo 1 500 px di scroll, il titolo si raggiunge. Resta la condizione posta dal quarto giro per il 4 — la deroga scritta con la sua gamma di viewport —, non soddisfatta; le misure sono le stesse: interim **129,2 %** a 390 × 844 (seconda azione a 816,8), **136,3 %** a 375 × 812 (seconda azione a 832,8, 20,8 px sotto la piega), **142,3 %** a 360 × 800; `phase3` 124,1 / 129,0 / 138,4 %. Con JavaScript: bersagli 44, nessuno scroll orizzontale (`scrollWidth` = viewport a 360–768), porta → titolo → lead → azioni a passo 24, H1 arabo a filo. |
| 10 | **Accessibility** (critica) | **4** (4) | Due miglioramenti misurati: contenuto raggiungibile senza script (16) — il contratto di `static/js/main.js:4` è rispettato sotto 80rem —; vie ≥ 3 : 1 in colori forzati nelle due tavolozze (salite mediana 21 : 1). Tastiera completa invariata (menubar LTR/RTL, cassetto, Menu account), «Menu» mai coperto, reduced-motion completo, anello del chevron visibile anche in colori forzati (colore di sistema, `outline-offset: -4px`). Non 5, minori: in colori forzati chiari la chiave a 2,63 : 1 sul Canvas (20) e glifi della legenda a 1,73 : 1, gradini a 1,2–1,45 : 1 (21, preesistenti; il diagramma è `aria-hidden` e ogni glifo è accanto alla sua parola, per questo non fanno cadere la dimensione); `test_rtl_browser` non eseguito. |

## 4. I quattro test (§75–78) — Red Team indipendente

| Test | Domanda | Risposta richiesta | Risposta | Perché, esattamente (elemento, cattura) |
|---|---|---|---|---|
| Generic AI | «Potrebbe essere scambiato per un template generico Claude/AI?» | **NO** | **NO** | Carta minerale e navy del marchio, Newsreader 300 maiuscolo + IBM Plex, la porta con chiave e gradini attraversata da quattro vie intrecciate nella soglia e ancorate a una legenda in vetro, tre uscite con le parole dell'eyebrow, il segmentato con «ع», il lock-up ufficiale (`a6_03_perf_8772_1440.png`, `a6_14_home_8770_ar_1440.png`). Il punto fragile resta il pannello del mega-menu. |
| Editorial | «Sembra ancora principalmente una pubblicazione editoriale/legale?» | **NO** | **NO** | Serif solo nell'H1; lead, corpo, legenda, nav, Menu in Plex; CTA a gradiente; il palcoscenico è un diagramma di prodotto. Avvertenza invariata: sotto l'hero riprende la pagina V2 (`a6_16_nojs_8770_1024_scrolled.png`: «01 L'ÉCOSYSTÈME», serif). |
| 2026 | «Nascosto il logo, competerebbe con prodotti digitali premium del 2026?» | **SÌ** | **SÌ** | Stati e profondità reggono sulle superfici principali; la barra interim ha ora un ritmo da prodotto. Ciò che un prodotto premium non spedisce è la lista di §6: la pillola del chevron che tocca le parole e si fonde con la voce accanto (19), la chiave sul bianco in colori forzati (20), e l'LCP di 3 s. |
| Too much | «Abbiamo aggiunto effetti inutili solo per sembrare moderni?» | **NO** (altrimenti: elenco di cosa togliere, nell'ordine di `CREATIVE_DIRECTION.md` §6.4) | **NO** | Il commit non aggiunge effetti: un ritaglio senza script, una regola di posizione, tre regole in colori forzati, una geometria del chevron. |

## 5. Verifiche binarie (tutte devono essere «sì»)

| Verifica | Sì/No | Prova |
|---|---|---|
| Nessuna formulazione vietata (`apps/cms/forbidden.py`), nessun testo bloccato alterato | **Sì** | Diff d475749 → 213e00f su `templates/`: solo `_hero.html`, un commento Django e un `<clipPath>`; nessun testo. `tests/compliance/test_locked_content.py`, `test_public_pages.py`, `test_phase3_texts_not_leaked.py` verdi (nota A). |
| Nessun `style=""`, nessuno script inline, nessun hotlink (CSP) | **Sì** | HTML servito di `/fr/` e `/ar/` (8770, 8771): **0** ` style=`, 6 `<script>`, 0 inline eseguibili (solo JSON-LD); `/_design/`: 0 `style=`, 0 inline. CSP servita: `script-src 'self'`, `style-src 'self'`, `font-src 'self'`, `img-src 'self' data:`, `object-src 'none'`. Ascoltatore `securitypolicyviolation` installato prima del caricamento: **0** violazioni su 8772 (due passate 4G). Il `clip-path: url("#doorway-routes-arch")` punta a un frammento dello stesso documento. |
| Nessun valore fuori dai token (colori, raggi, ombre, durate, curve) | **Sì** | `tests/frontend/test_v4_tokens.py` e `test_design_docs.py` verdi (nota A); i valori nuovi sono geometria (rettangolo SVG 0–531 × 0–520 in unità del palcoscenico, `margin-inline: -7px` che ripete il `padding-inline: 7px` letterale dello stesso intervallo — accoppiati a mano, vedi Frontend Lead) e colori di sistema (`Canvas`, `CanvasText`). |
| «Nessun colore significa mai approvato»: nessun chip `conforme` con croma, nessun verde di verdetto | **Sì** | Nessun chip nelle superfici del gate; l'unico verde è quello del marchio nel lock-up. |
| Nessun dato, contatore, avatar, grafico o KPI finto | **Sì** | Nessun numero nell'hero e nella testata; le vie sono le `entrances()` reali; le uscite le parole dell'eyebrow; il menu account mostra `qa-person`. |
| Coordinate, «svg», «Suspendre le mouvement», etichette di debug: assenti | **Sì** | HTML servito (8770, 8771, `fr` e `ar`): 0 «Suspendre», 0 «svg» nei nodi di testo, 0 coordinate visibili, 0 commenti di template trapelati, 0 id duplicati (34 / 40 id; il `clipPath` nuovo è unico). |
| Reduced-motion: pagina completa, nulla a opacità 0 | **Sì** | §1, riga Reduced-motion: 0 animazioni su due server a quattro larghezze; invisibili solo le correnti e la didascalia chiusa. |
| Contrasto sul peggior fondo (incluso sotto il vetro) ≥ 4,5 testo / ≥ 3 UI | **Sì** | Colori e fondi del testo e dei controlli invariati dal secondo giro; la pillola del chevron è lo stesso `--min-1` di prima (l'hover non porta informazione di contrasto); l'anello del chevron resta `2px #1d8a93` + compagno `#f4f3f0`, e in colori forzati è il colore di sistema. In colori forzati le vie sono ≥ 3 : 1 (mediana 21). La chiave (2,63 : 1, 20), i glifi della legenda (1,73 : 1) e i gradini (1,2–1,45 : 1, 21) in colori forzati chiari sono grafica `aria-hidden` o affiancata alla sua parola: non fanno cadere la verifica, ma vanno corretti. |
| Prestazioni: JS/CSS ≤ budget, LCP < 2,5 s, CLS < 0,1, INP < 200 ms (4G simulato) | **No** | §0-bis riga 3: LCP **3 284 / 3 084 ms** (la fotografia della porta) > 2 500; CLS 0,0032 / 0,0351 ✓; INP-proxy 96 ms ✓; CSS **100,04 KiB ✗** sul budget proposto (41 byte sopra), JS 36,0 ✓, font **356,1** ✗ (proposto 200); budget non scritto in §68/DS; HTML non compresso. |
| RTL (ar) a tre larghezze senza proprietà fisiche nel CSS nuovo | **Sì** | Le regole nuove sono `margin-inline` (logica), `position` / `z-index`, `outline-offset` e `box-shadow: inset` (simmetrici), e un rettangolo in unità dell'SVG non specchiato (`.doorway { direction: ltr }`, CD §4.1). Misurato in `ar`: distanze d'inchiostro 14,0 a 1280 / 1366 / 1439, anello dentro il riquadro, frecce speculari, H1 a filo a 390 / 768 / 1440 (Δ 0) su 8770 e 8771, menu account del cassetto sotto il riassunto; `tests/i18n/test_rtl_static.py` verde (nota A); `tests/i18n/test_rtl_browser.py` **non eseguito**. |
| Demo page dei componenti coerente (§94) | **Sì, parziale** | `/_design/` (8770, HTML servito, 200): **0** id duplicati (94 id), 0 `style=`, 0 script inline; **assenti**, come nei giri precedenti, legenda in vetro, didascalia e porta, e ora anche la variante del chevron da 44 a 80–90rem con i suoi stati. `tests/frontend/test_design_showcase.py` verde (nota A). |

**Nota A — esito dei test** (database dedicato `ile_lane4`, mai in parallelo fra loro, mai con `-p no:logging`; il
container `italylegalentry-db-1` è rimasto «Up (healthy)» per tutto il giro):
1. `tests/frontend/test_design_docs.py tests/frontend/test_v4_tokens.py tests/frontend/test_frontend_bundle_is_current.py apps/pages/tests -q`
   — **395 passed in 768,48 s**, exit 0 (uscita in `review_a6/pytest_a6_fast.txt`, fuori dal repository).
2. `tests/compliance/test_locked_content.py tests/compliance/test_public_pages.py tests/compliance/test_phase3_texts_not_leaked.py tests/i18n/test_rtl_static.py tests/frontend/test_design_showcase.py tests/frontend/test_header_fits_the_narrowest_viewport.py tests/frontend/test_svg_wellformed.py tests/frontend/test_template_comments_do_not_leak.py -q`
   — **88 passed in 167,77 s**, exit 0 (`review_a6/pytest_a6_compliance.txt`). `test_header_fits_the_narrowest_viewport.py`
   lancia un Chromium headless proprio, non la scheda visibile.

Le due suite hanno girato in parallelo alle sole sonde funzionali (database diversi: `ile_lane4` contro `ile` /
`ile_qa`), mai alle misure di tempo, prese a suite finite. Il «808 passed, 1 xfailed» del builder (frontend + pages +
accounts + cataloghi) non è stato ri-eseguito per intero; la parte richiesta sì.

## 6. Esito

| Esito | Condizione |
|---|---|
| **PASS** | tutte le critiche ≥ 4, tutte le dimensioni di sostegno ≥ 3, quattro test corretti, tutte le verifiche «sì», AFTER materialmente superiore su ogni vista |
| **CONDITIONALLY_READY** | tutte le critiche ≥ 3 e nessuna ≤ 2, al massimo due dimensioni di sostegno ≤ 2, quattro test corretti, verifiche «sì»; correzioni elencate con scadenza; **nessuna propagazione** finché non diventa PASS |
| **BLOCK** | una dimensione critica ≤ 2, **oppure** un test sbagliato, **oppure** una verifica «no», **oppure** AFTER non materialmente superiore |

Esito del gate: ☐ PASS ☐ CONDITIONALLY_READY ☒ **BLOCK**

Motivazione, nell'ordine delle regole: nessuna dimensione critica ≤ 2 (Premium Feel 4, Modernity 4, Clarity 4,
Credibility 4, Mobile **3**, Accessibility 4), nessuna di sostegno ≤ 2 (Visual Depth 4, Motion **3**, Originality 4,
Interaction Quality **3**), i quattro test corretti, l'AFTER materialmente superiore al BEFORE su ogni vista. Sulle
dimensioni e sui test il gate sarebbe **CONDITIONALLY_READY** — non PASS: Mobile, critica, è a 3. Lo tiene a **BLOCK**
**una sola** verifica binaria, come nei quattro giri precedenti: le prestazioni (LCP 3,08–3,28 s su 4G lento contro 2,5;
font 356 KB contro i 200 proposti; CSS ora 41 byte **sopra** il tetto proposto di 100 KiB; budget non adottato; le leve —
carattere del lock-up, corsivo della fascia forum, minificazione o concatenazione dei fogli, HTML compresso — restano del
committente).

Giudizio sul giro: delle cinque correzioni del quinto giro **tre sono chiuse sul loro criterio** (16, 17, 18) e i
numeri del README (§4.8, «Quinto giro») sono stati ritrovati uno per uno (0 px di testata dopo 1 500 px senza script,
14 px d'inchiostro con scarto 0, chevron 44 × 44 ai quattro bordi, salite 21 : 1, LCP ≈ 3,1–3,3 s, CSS «100,0 KB»); due
restano parziali (3 prestazioni, 6 documentazione). Nessuna correzione è regredita sul suo criterio. Ma due correzioni
hanno spostato il problema invece di toglierlo: la 17 ha reso uniforme il ritmo **a riposo** lasciando gli stati del
chevron disegnati sul riquadro da 44 che ora invade i vicini (19: è questo che fa scendere Interaction Quality da 4 a 3);
la 18 ha dato all'arco interno il Canvas e con esso ha tolto alla chiave del marchio il suo fondo navy nella tavolozza
chiara (20, minore). Il 21 è preesistente, reso visibile dalla verifica delle due tavolozze che questo giro ha aggiunto.

Correzioni richieste (numerate: prima le correzioni ancora aperte del quinto giro con il loro numero, poi i difetti
nuovi da 19; ognuna con dimensione, elemento, cattura, criterio di chiusura):

3. **Prestazioni — verifica binaria 9.** Dimensione: Frontend Lead. Misura: §0-bis riga 3 (LCP 3 284 / 3 084 ms, la
   fotografia della porta; font 356,1 KB; CSS 102 441 byte gzip in 22 fogli = 100,04 KiB; HTML 43 926 byte non
   compresso). Criterio (invariato): su 8772, 4G lento + CPU ×4, due passate, **LCP < 2,5 s**, CLS < 0,1, INP-proxy
   < 200 ms; il budget **scritto** in §68/DS e rispettato o con deroga firmata (oggi il CSS lo supera di 41 byte); i
   font della home entro il budget o una decisione scritta su lock-up (128,9 KB) e corsivo (143,4 KB); la riduzione dei
   22 fogli (minificazione misurata dal builder: 95,3 → 47,8 KB; o concatenazione) con una data; HTML compresso o
   decisione scritta (BREACH) registrata nel gate.
6. **Documentazione e decisioni** (nessun codice). Invariato dal quinto giro: (a) firmare in `CREATIVE_DIRECTION.md` (o
   in una sua appendice di deviazioni) le **quattro** deviazioni da §3.1 / §4.4 — lead non corsivo, titolo senza reveal,
   palcoscenico senza disegno d'ingresso, deroga a 390 con la sua gamma di viewport (interim 129,2 % a 390 × 844,
   136,3 % a 375 × 812 con la seconda azione 20,8 px sotto la piega, 142,3 % a 360 × 800); (b) le decisioni del
   committente/CD: traduzioni arabe di lead, corpo e gloss su `/ar/`, terza colonna del mega-menu, sette voci,
   carattere del lock-up, minificazione dei fogli. Criterio: le firme e le decisioni scritte nel documento del CD.
19. **Barra interim fra 80 e 90rem: gli stati del chevron invadono i vicini.** Dimensioni: Interaction Quality
    (principale), Premium Feel, Clarity (minore). Elementi: `static/css/v4/shell.css:381–392` (correzione 17:
    `.main-nav__list:not(:has(> .main-nav__item:nth-child(6))) .main-nav__toggle { position: relative; z-index: 1;
    margin-inline: -7px }` e l'anello interno) insieme a `static/css/v4/shell.css:226–229` (`.main-nav__toggle:hover {
    background: var(--min-1) }`, radius `--radius-sm`) e `:188–192` (pillola `--min-1` del link corrente, aperto, in
    hover). Misure (8770, sui pixel delle catture a 1×, colonna della pillola a 3 px dal bordo superiore del riquadro,
    ultimo/primo pixel con luminanza < 140 nelle righe del testo): a **1280, 1366 e 1439**, `fr` e `ar`, pillola di hover
    del chevron a **1–2 px** dall'ultima lettera della parola che precede e **2–3 px** dalla prima della parola che segue
    (a 1440, dove la regola non vale: 12 / 16–17 px; prima della correzione 17, dedotto dalla geometria del quinto giro,
    7 px); pressione: stesso sfondo, stessa distanza (`a6_17_states_sheet.png`); anello (`outline 2px rgb(29,138,147)`,
    `outline-offset: -4px`, compagno `inset 2px #f4f3f0`) a **2–3 px** dalle lettere vicine (`a6_17_focus_sheet.png`;
    a 1440 6–17 px). Con una pillola accanto: sulla pagina `/fr/entreprises/` (link «Entreprises» `aria-current`) o col
    pannello di «Entreprises» aperto, l'hover sul chevron di «Personnes» fonde le due pillole in una sola forma che copre
    «⌄ Entreprises» (`a6_19_fused_sheet.png`; la pillola del chevron si sovrappone per 7 px a quella del link). Bersagli:
    `elementFromPoint` 3 px dentro il bordo di ogni link accanto a un chevron restituisce il chevron (`fr`: fine di
    «Personnes» e di «Entreprises», inizio di «Entreprises» e di «Forum Vénétie–Maroc»; lo stesso in `ar`); un clic reale
    3 px dentro il riquadro di «Forum Vénétie–Maroc» apre `nav-1-panel` («Entreprises») e l'URL resta `/fr/` (1280 e 1439,
    `fr` e `ar`). La parte cliccabile del link arabo «الأفراد» scende da 44,6 a 37,6 px (≥ 24: nessuna violazione
    2.5.8). Criterio: a 1280, 1366 e 1439, in `fr` e in `ar`, sulla barra interim: (a) la forma di hover e di pressione del
    chevron a **≥ 6 px** dall'inchiostro delle parole vicine e il suo anello a **≥ 4 px**, misurati sui pixel; (b) fra la
    forma del chevron in hover e la pillola di un link adiacente corrente o aperto uno stacco visibile **≥ 2 px** (nessuna
    fusione), misurato su `/fr/entreprises/` e col pannello aperto; (c) invariati: distanze d'inchiostro uniformi ±4 px
    (17), riquadro di tocco 44 × 44, frecce del menubar; (d) o i 7 px di bordo tornano al proprio link, o la condivisione
    è scritta come scelta nel commento della regola. Una via possibile: lasciare il riquadro da 44 trasparente come sola
    area di tocco e disegnare hover, pressione e anello su una forma interna centrata di 28–32 px.
20. **Colori forzati, tavolozza chiara: la chiave del marchio perde il suo fondo.** Dimensioni: Accessibility (colori
    forzati), Premium Feel in quel modo; minore. Elementi: `static/css/v4/hero.css:736` (correzione 18: `.doorway__inner {
    fill: Canvas; … forced-color-adjust: none }`) sotto `static/brand/original/key.svg` (immagine, `fill="#C39A2B"` con il
    disco del foro `#0F2547`, colori non adattabili dal CSS) e il bagliore `.doorway__glow` (oro, invisibile sul bianco:
    1,01 : 1). Misura (8770 `/fr/` e `/ar/`, 1440, `forced-colors: active` + `prefers-color-scheme: light`, pixel della
    cattura): oro della chiave rgb(195, 154, 43) su Canvas rgb(255, 255, 255) = **2,63 : 1**; il disco del foro rgb(15, 37,
    71) diventa un **punto navy** a 15,26 : 1 dentro l'anello d'oro (`a6_18_forced_light_8770_fr_stage.png`); in tavolozza
    scura la chiave è a 7,98 : 1 e il foro si legge come foro (1,38 : 1 sul nero); prima della correzione 18 l'arco
    interno restava navy e la chiave stava sul suo fondo d'origine (5,80 : 1 per il commento di `hero.css:208–209`; non
    ri-misurato: i server servono solo 213e00f). Criterio: in colori forzati, tavolozza chiara **e** scura, a 1440 in `fr`
    e in `ar`, la chiave ≥ 3 : 1 contro ciò che ha direttamente dietro **e** il foro del suo anello dello stesso colore di
    quel fondo (≤ 1,1 : 1), con le vie ancora ≥ 3 : 1 (18) — per esempio un fondo `CanvasText`/navy solo sotto la chiave,
    o la chiave resa come sagoma `CanvasText` sotto `forced-colors` —, oppure il limite scritto e firmato dal CD come
    limite del modo a colori forzati.
21. **Colori forzati, tavolozza chiara: glifi della legenda e gradini sotto 3 : 1** (preesistente, mai misurato nelle due
    tavolozze). Dimensione: Accessibility (colori forzati); minore. Elementi: `static/css/v4/hero.css:462–467`
    (`.doorway-legend__glyph { color: var(--on-dark-2) }`: il colore dichiarato sull'`svg` sopravvive, calcolato
    `forced-color-adjust: preserve-parent-color`, perché non è ereditato) contro `.doorway-legend { background: Canvas }`
    (`hero.css:740`); `.doorway__steps rect { fill: CanvasText }` (`hero.css:739`) con le opacità 0,55 / 0,38 / 0,24
    (`hero.css:236–238`) sopra la fotografia. Misura (8770 `/fr/`, 1440): glifo rgb(185, 197, 214) su Canvas bianco =
    **1,73 : 1** in tavolozza chiara (11,43 : 1 in scura; 3,23 : 1 fuori dai colori forzati sul vetro della legenda);
    gradini contro la fotografia fra un gradino e l'altro **1,20–1,45 : 1** in chiara (i tre gradini quasi spariscono,
    `a6_18_forced_light_8770_fr_lower.png`), 2,05–3,21 : 1 in scura. Il diagramma è `aria-hidden` e ogni glifo sta accanto
    alla sua parola (CanvasText): per questo è minore. Criterio: in colori forzati, nelle due tavolozze, a 1440, glifi
    della legenda ≥ 3 : 1 sul fondo della legenda (per esempio `color: CanvasText` sotto `forced-colors`) e ciascun
    gradino ≥ 3 : 1 contro i pixel della fotografia accanto (per esempio opacità 1 sotto `forced-colors`), misurati sui
    pixel.

Note, non correzioni: senza JavaScript, fra 64 e 80rem, dentro l'arco si vedono le due salite del tracciato con uscite
(fino a y 200 e 300, tratto sfumato più casing) mentre con JavaScript le vie finiscono in piano a x 531 — due disegni
diversi dello stesso stato, entrambi dentro l'arco (`a6_16b_nojs_stage_1024_zoom.png`); senza JavaScript, fra 80 e
90rem, il pannello che si apre in hover su un bordo di 7 px di un link è quello della sezione accanto (stessa causa del
19); la barra `phase3` (sette sezioni, fuori dalla correzione 17) ha a 1440 un ritmo 16 / 20 / 24 px (scarto 8; a
1280–1439 11 / 14, scarto 3); a 1280 il pannello del mega-menu comincia a y 97, 1 px sopra il piede della testata (98),
come nei giri precedenti; con `.main-nav__toggle` in `position: relative` il chevron resta dentro il contesto di
sovrapposizione della testata (`z-index: 20`).

Firma del Creative Director (esito finale, §6 della direttiva): ______ · data/ora: ______

## 7. Ciò che non è stato possibile verificare, e perché (§95)

- **`test_rtl_browser`**: non eseguito (pilota un browser; fuori dall'insieme richiesto). Non ri-eseguita per intero la
  suite «808 passed, 1 xfailed» del builder (nota A).
- **Cinque revisori distinti** (§71): un solo agente ha compilato le sei righe.
- **La barra interim con il menu account aperto**: la combinazione (fase 3 chiusa, utente autenticato) esiste solo su
  8770 / `ile`, dove il revisore non ha una sessione e non ne ha creata una (sarebbe una scrittura in quel database).
  Che il `z-index: 1` del chevron non possa passare sopra il menu account è dedotto dal contesto di sovrapposizione
  misurato (`#site-header` `position: sticky; z-index: 20`; barra istituzionale `static`), non osservato.
- **Il tocco sul chevron fra 80 e 90rem**: l'area 44 × 44 è misurata con `elementFromPoint` e con clic del mouse ai
  quattro bordi; nessun tocco emulato su quella barra.
- **Lo stato prima della correzione 17 e della 18**: i server servono solo 213e00f; i «7 px» fra pillola e parole e la
  chiave a 5,80 : 1 sul navy sono dedotti dalla geometria misurata nel quinto giro e dal commento del foglio, non
  ri-misurati.
- **La tavolozza scura dei colori forzati** è l'emulazione di Chrome (`forced-colors: active` + `prefers-color-scheme:
  dark`), non un tema a contrasto elevato reale di Windows; i minimi per punto delle vie nella treccia (1,0–2,8) sono
  punti di antialias o di due vie sovrapposte, e per questo il documento riporta mediane e decimi percentili.
- **Uno screen reader reale** e **dispositivi reali**: nulla ascoltato; rotazioni e tocco non ri-misurati in questo giro
  (il commit non tocca il cassetto; i bordi del cassetto e dello scrim sono stati ri-misurati con clic reali a 390, 768,
  1024 e 1279 su due pagine).
- **Lo stato senza JavaScript** su pagine diverse da `/fr/` e `/fr/parcours/`: dedotto dal CSS condiviso, non misurato
  pagina per pagina.
- **La leggibilità delle uscite arabe** a 12 unità: osservata sulla cattura, non valutata con un lettore arabo.
- **I contrasti delle superfici con testo sotto il vetro**: non ri-misurati sui pixel (colori e fondi invariati dal
  secondo giro).

## 8. Metodo e limiti

- Osservazione: Chrome visibile via `scripts/cdp.py` (`Page.attach(url_contains="127.0.0.1:")`, poi `"127.0.0.1:8771"`
  per le sonde con l'account), una sola scheda (`Page.bringToFront`, `visibilityState: visible`, 61 rAF in 500 ms
  all'inizio), sonde sequenziali; viewport emulati 1440 × 900, 1439 / 1366 / 1280 × 900, 1279 / 1280 × 800, 1024 × 768,
  768 × 1024, 390 × 844, 375 × 812, 360 × 800 (con `mobile: true` e tocco dove indicato); emulazioni azzerate a fine sonda.
- Script del revisore: `C:\Users\<user>\AppData\Local\Temp\claude\C--tmp-italylegalentry\review_a6\` (`common.py`,
  `sampler.js`, `r0_window.py`, `r1_nojs_header.py`, `r2_nojs_clip.py`, `r2b_noise.py`, `r3_js_header_drawer.py`,
  `r4_bar.py`, `r5_bar_states.py`, `r5b_ar1439.py`, `r6_ring.py`, `r7_pill.py`, `r8_forced.py`, `r8b_glyph.py`,
  `r9_perf.py` (derivato da `review_a5/r10_perf.py`), `r9b_css.py`, `r10_mega.py` (derivato da `review_a5/r7_mega.py`),
  `r11_mobile.py`, `r12_reduced.py`, `r13_8771_bar.py`, `r14_account.py`, `r15_fc_bar.py`, `r16_fc_routes.py`); uscita
  delle prestazioni `r9_out.txt`; HTML servito salvato in `home_8770_fr.html`, `home_8770_ar.html`, `home_8771_fr.html`,
  `home_8771_ar.html`, `home_8772_fr.html`, `parcours_8770.html`; esiti dei test `pytest_a6_fast.txt`,
  `pytest_a6_compliance.txt`.
- Una sonda (`r5_bar_states.py`, `ar` 1439) ha letto due hover senza effetto subito dopo un Esc e una navigazione; ripetuta
  due volte da sola (`r5b_ar1439.py`), hover e indicatore sono corretti su tutti e quattro i link: non è un difetto.
- Le prestazioni sono state misurate a suite di test finite (le suite hanno girato in parallelo alle sole sonde
  funzionali, su un database diverso).
- Nessun file del repository modificato al di fuori di questa scorecard e delle catture in `review_a6/`.
