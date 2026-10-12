# GATE A — Homepage (hero) + Navbar · scorecard del 25 settembre 2026 — **quarto giro**

Compilata sul modello `docs/design-v4/GATE_SCORECARD_TEMPLATE.md` (§71–78 della direttiva). Regole
applicate: **nessuna media** (§74); **l'implementatore non vota** (§72); ogni punteggio cita ciò che il
revisore ha **osservato in Chrome visibile** (§70) — Google Chrome 153, CDP 9222, `scripts/cdp.py`, una sola
scheda, sonde sequenziali, `Network.enable` + `Network.setCacheDisabled` in testa a ogni sonda. Le misure sono
`getBoundingClientRect` / `getComputedStyle` / `elementFromPoint` / `getBBox` / `getPointAtLength` / attributi SVG /
`performance.getEntriesByType` / `PerformanceObserver` (LCP, layout-shift, longtask, event, installati con
`Page.addScriptToEvaluateOnNewDocument`) / campionamento a ogni `requestAnimationFrame` / `document.getAnimations()` /
albero di accessibilità (`Accessibility.getPartialAXTree`) / eventi reali (`Input.dispatchMouseEvent`,
`Input.dispatchKeyEvent` con `Emulation.setFocusEmulationEnabled`, `Emulation.setDeviceMetricsOverride` con
`mobile: true` e `screenOrientation` per le rotazioni, `Emulation.setTouchEmulationEnabled`, `Emulation.setEmulatedMedia`
per reduced-motion e colori forzati, `Network.emulateNetworkConditions` 150 ms / 1,6 Mbit/s / 750 kbit/s +
`Emulation.setCPUThrottlingRate` 4 per il 4G lento) e letture di pixel con Pillow sulle catture del revisore. Le
catture di questo giro stanno in `docs/qa/chrome/design-v4/after/review_a4/` (prefisso `a4_`, ignorate da git:
`.gitignore:30`); i percorsi sono relativi alla radice del repository. Ogni numero di questo documento è una misura
del revisore presa in questo giro; i numeri del README e dei giri precedenti sono citati solo per confronto.

Nota sulle misure: la scheda riportava `devicePixelRatio` **1** (finestra 1905 × 1012, interno 1889 × 917, 63 rAF in
500 ms, `visibilityState: visible`); tutte le emulazioni con `deviceScaleFactor: 1`.

Nota sulla scheda: fra le **21:09 e le 21:10** del 25/09 la scheda del progetto è **sparita** dal Chrome di QA
(l'elenco dei target di 9222 conteneva una sola pagina, `chrome://intro/`, senza finestra: `Browser.getWindowForTarget`
→ «Browser window not found»). Nessuno script del revisore chiude schede e nessuna sonda era in corso (l'ultima,
`r16_arabic.py`, è finita alle 21:08:58 con le emulazioni azzerate); il revisore non ha aperto schede. Il coordinatore
ha poi ricreato la scheda su 8771 e l'ha autenticata come `qa-person`. Alla ripresa l'elenco dei target mostrava **due**
pagine `127.0.0.1:8771` (`/fr/` e `/fr/espace-reserve/`): per non scegliere a caso fra due schede il revisore **non** ha
fatto altre sonde, e le due previste dopo le 21:10 (un INP-proxy deliberato, la geometria di `r17_risers.py` in pagina)
sono sostituite o dichiarate in §7.

Questo documento verifica, correzione per correzione, le correzioni del terzo giro (`gates/GATE_A_2026-09-25_round3.md`,
§6: 2–6 ancora aperte dal secondo giro, 7–10 nuove), ciascuna contro il **suo** criterio di chiusura; poi cerca i
difetti introdotti o lasciati scoperti dalle correzioni, ri-assegna le dieci dimensioni, i quattro test e le verifiche
binarie.

---

## 0. Identità del gate

| Campo | Valore |
|---|---|
| Gate | **A** |
| Superfici | Homepage pubblica `/fr/`: hero «il portico» (porta, quattro vie, legenda in vetro con didascalia, titolo, lead, CTA; uscite etichettate nella variante interim) + navbar (barra istituzionale con controllo lingua e accesso/menu account, testata, indicatore, mega-menu, cassetto con segmentato); `/ar/` (e `/it/`, `/en/` per le uscite) per RTL e lingue; la vetrina `/_design/` |
| URL / account | **8770** (`ile`, fase 3 chiusa → variante **interim**: eyebrow, titolo editoriale, tre uscite etichettate, quattro voci); **8771** (`ile_qa`, fase 3 aperta → variante `phase3`, sette voci; autenticata come **`qa-person`** con `scripts/qa_chrome_signin.py` alle ≈ 20:57 per le misure del menu account); **8772** (lo stesso codice di 8770 dietro WhiteNoise gzip) per ogni misura di prestazione. Verificato all'inizio: `v4/hero.css`, `v4/shell.css`, `v4/buttons.css`, `main.js` e `js/dist/home.js` serviti da 8770, 8771 e 8772 hanno lo stesso md5 dei file dell'albero; l'HTML servito porta i segni del commit (4 `aria-describedby="hero-gloss-…"`, 4 `<tspan>` nelle tre uscite di 8770, 0 `data-reveal` nell'hero di entrambe le varianti — gli 8 `data-reveal` di 8771 sono nella sezione V2 «voyage», fuori dal gate). |
| Commit sotto revisione | **156db5f** (albero pulito: `git status` vuoto all'inizio, alle 21:17 e alla ripresa). Sulle superfici del gate, da dd29168: `apps/pages/services.py` (uscite: salita lungo lo stipite `C543 … 555 … H624`; `hero_exits` a due righe), `static/js/src/home.js` (reveal del titolo tolto; stessa salita), `static/css/v4/hero.css` (maschera del titolo tolta, alone `paint-order` sotto le uscite, 40 px sopra la porta sotto 64rem, legenda 236 px fra 64 e 80rem, margine delle azioni al telefono, uscite in colori forzati), `static/css/v4/shell.css` (scrim da `--nav-drawer-top`; menu account del cassetto; regola unica dell'anello), `static/js/main.js` (`--nav-drawer-top` scritto sulla testata), `templates/pages/home/_hero.html` (`<tspan>`, `aria-describedby`, gloss `aria-hidden`, commento), `…/partials/_hero_title_lines.html` (commento), `docs/design/DESIGN_SYSTEM_2026.md` (pesi dei fogli). |
| Revisione | **quarto giro** (terzo: `gates/GATE_A_2026-09-25_round3.md`, su dd29168, BLOCK per la sola regola delle prestazioni; secondo: `…_round2.md`, su d99f2bb; primo: `GATE_A_2026-09-25.md`, su c6f3503) |
| Implementatore (non vota) | Claude (sessione principale) |
| Revisore indipendente | agente separato (sessione distinta; nessuna modifica a codice, template, fogli, script o test; nessun riavvio di server; nessun pacchetto installato; nessuna credenziale digitata; nessun modulo inviato; nessuna scheda aperta o chiusa) |
| Data e ora della revisione | 25 settembre 2026, ore 20:46–21:17 (misure in Chrome fino alle 21:09); scorecard scritta alla ripresa, 26 settembre |

## 0-bis. Le correzioni del terzo giro — verifica una per una, contro il loro criterio

| # | Correzione (terzo giro) | Stato | Prova (misura o cattura) |
|---|---|---|---|
| 2 | Scrim del cassetto sopra la testata | **CHIUSA** sul criterio — con il difetto nuovo **12** (ridimensionamento/rotazione a cassetto aperto) | Clic reale sul bottone «Menu» (`Input.dispatchMouseEvent`), 8770 **e** 8771, `scrollY` 0 e 200. **1024** e **768** (`mobile: true`), y 0: barra 0–33, testata 33–**98**, scrim 98–fondo, cassetto 98–fondo; y 200: testata 0–**65**, scrim e cassetto da 65. **390** (`mobile: true`), y 0 e 200: testata 0–**57**, scrim e cassetto da 57. `elementFromPoint` al centro del lock-up, del bottone «Menu» e del primo link lingua della barra (dove visibile: 768/1024 a y 0) = **l'elemento stesso** in tutti i 12 casi. Differenza media di pixel chiuso → aperto sul riquadro del lock-up: **0,63** (768, 1024) e **0,89** (390) su 255, identica sui due server (criterio < 2); sulla banda intera della testata 1,40–5,10 (il bottone passa a «× Menu»: voluto). Scroll parziale prima dell'apertura (1024): y 10 → piede 88 = scrim 88; y 30 → piede 68 = scrim 68. Il bordo dello scrim coincide con il piede reale della testata (±0 px). Catture `a4_02_drawer_open_8770_{1024,768,390}_y{0,200}.png` e `a4_02_drawer_open_8771_…`. Osservazione: a 390, 768 e 1024 il cassetto è a schermo intero (dal piede al fondo), quindi lo scrim sfocato non si vede mai a riposo (solo nella transizione). **Ma** il bordo è misurato **solo all'apertura** (`main.js:155–163`): a cassetto aperto una rotazione o un ridimensionamento lo lasciano dov'era (difetto 12). |
| 3 | Prestazioni — verifica binaria 9 | **PARZIALE** (invariata) | 8772, 1440 × 900, cache spenta, 4G lento + CPU ×4, due passate: **LCP 3 040 / 3 124 ms** — `image.doorway__img` (`doorway-800.webp`, 133 126 px²; candidati precedenti `P.utility-bar__identity` 1 764 / 1 672 e una riga del titolo 1 872 / 1 792); FCP 1 764 / 1 672; DCL 3 362 / 3 027; load 3 735 / 3 473; CLS **0,0037 / 0,0032**; long task max **470** / 218 ms (11 / 8 task); 0 violazioni CSP. **Pesi** (identici nelle due): CSS **22 fogli, 99,0 KB gzip** (388,3 nudi); JS **8 file, 35,6 KB** (99,3); font **6 file, 356,1 KB** (Newsreader tondo 128,9 precaricato, Newsreader **corsivo 143,4** finito a 3 449 / 3 461 ms, Plex Sans 22,1 + 23,6 + 23,7, Plex Mono 14,4); nessun font arabo; immagini 5 file, 79,5 KB (foto 76,8, precaricata da 235 / 243 ms); HTML **43 783 byte non compresso** (`curl` con `Accept-Encoding: gzip, br`: nessun `Content-Encoding` sull'HTML, gzip sui fogli); **42 richieste**. Senza limiti: LCP 292 ms (la foto), CLS 0,0002. INP-proxy: solo eventi incidentali del puntatore sotto CPU ×4, durata massima **64 ms** (la sonda deliberata non è stata fatta: §7). Confronto col terzo giro: LCP 2 960 / 3 088 → 3 040 / 3 124 (stesso ordine; README 3 056), CSS 98,0 → **99,0 KB** (1 KB di margine sui 100 del budget proposto), font 356,1 = 356,1. Il budget resta «proposto al CD» (README riga 249), non scritto in §68/DS; nessuna decisione su lock-up, corsivo, concatenazione, HTML compresso. |
| 4 | Mobile — la deroga | **CHIUSA sulla misura** (accettata); la **firma** del CD resta (voce 6a) | Viewport mobile vero (`mobile: true`, tocco, nessuna barra di scorrimento): **390 × 844** interim (8770) hero **1 090,8 px = 129,2 %**, azioni 716,8–760,8 e 772,8–**816,8** → **27,2 px** di margine (≥ 16); `phase3` (8771) 1 047,3 = **124,1 %**, azioni finite a 661,3. **768 × 1024** interim: azioni in riga finite a **1 007,8** (16,2 px dentro la piega; 995,8 con barra di scorrimento), `phase3` 903,2. Lead → azioni **24 px** = titolo → lead 24 (margine delle azioni `8px 0 24px`); 40 px sopra la porta sotto 64rem (`.hero__inner` `padding-top: 40px`). `scrollWidth` = viewport ovunque. I numeri del README sono esatti. Il revisore **accetta** la deroga su questa misura, con un'avvertenza per chi la scrive: è tarata su 390 × 844 con 0,8 punti di margine sul 130 %; a **375 × 812** l'interim è **136,3 %** e la seconda azione finisce a 832,8 (**20,8 px sotto** la piega), a **360 × 800** 142,3 % (**32,8 px sotto**); `phase3` 129,0 % / 138,4 % con le azioni dentro. Catture `a4_04_home_8770_390_mobile.png`, `a4_04_home_8771_390_mobile.png`, `a4_04_home_8770_768_mobile.png`, `a4_04_home_8771_768_mobile.png`. |
| 5 | La legenda a 1024 | **CHIUSA** | `.doorway-legend` **236 px** fra 64 e 80rem, **264** da 80rem; righe **44 / 44 / 44 / 44** (parole alte 20: nessun a capo) a **1024, 1100, 1279, 1280 e 1440** su 8770 `fr`, 8771 `fr`, 8770 `ar`, 8771 `ar` e 8770 `it` (25 combinazioni). Sovrapposizione allo stipite: **38 px** a 1024 (legenda 529–765, porta 727–947; in RTL 40–276 contro 238–458: 38), 21 a 1100, 0 a 1279, **29** a 1280, nessuna a 1440 (−4); a 1024 la legenda si ferma **15 px** prima del navy (780). Giudizio sulla cattura (`a4_06_legend_8770_1024.png`, `a4_06_legend_8771_1024.png`): il vetro L3 davanti allo stipite è lo stesso rapporto di 1280, la porta resta leggibile e il navy libero: **accettabile**. (A 1024 le vie escono però verso uscite nascoste: difetto 13b.) |
| 6 | Documentazione e decisioni | **PARZIALE** | **Chiusi**: il nome dei link della legenda è la parola e il gloss è la **descrizione** — albero di accessibilità su 8770 `fr`: `link` «Personnes» con descrizione di 66 caratteri, «Entreprises» 70, «Institutions» 97, «Universités & Formation» 66; 8770 `ar`: nomi e descrizioni arabi (47–51); 8771 `fr`: descrizioni 68–126; il gloss non compare come testo a sé nel sottoalbero della legenda. Il commento di `_hero.html` è vero per il testo (titolo compreso: riga 7). **Aperti**: (a) le tre deviazioni sono scritte nel README (§4.8, «da firmare dal CD») e **non** in `CREATIVE_DIRECTION.md` (invariato dal commit 6718f1a), nessuna firmata: lead non corsivo, reveal del titolo tolto, deroga a 390 (CD §3.1 dice «≤ 110 % del viewport a 390»); (b) su 8771 `/ar/` i nomi arabi portano descrizioni **francesi** (101–126 caratteri) — la lingua della descrizione si perde nella stringa piatta: una voce in più nella decisione pendente sulle lingue dell'hero arabo, accanto a terza colonna del mega-menu, sette voci, carattere del lock-up; (c) il **residuo** del toggle: **24 × 44** a 1280, 1366 e 1439, 28 × 44 a 1440, su entrambe le varianti. L'argomento del README non regge sui numeri: su `phase3` i toggle sono **tre** (non cinque), la lista misura **761,7 px** (non ≈ 745) e l'aria fra lock-up e lista è **31,4 px** (non ≥ 100); sulla variante **in vigore** (interim, quattro voci) l'aria è **356,3 px** e tre toggle da 44 ci starebbero con ≈ 300 px d'avanzo. (d) Il commento di testa di `home.js` («Everything … complete on the first frame — door, key, steps, **routes** … What moves is drawn ON TOP of a complete composition») è falso per vie, nodi e uscite (difetto 11). |
| 7 | Il titolo si vede, sparisce e rientra | **CHIUSA** | Storia per fotogramma di ogni `.hero__title .line` e del suo `span` (trasformazione, opacità, visibilità, `clip-path`), dell'H1 e delle animazioni con bersaglio nel titolo: **0 fotogrammi nascosti** su 666 (8770) e 638 (8771) senza limiti e su 244 / 324 (8772, 4G lento + CPU ×4), e 0 su 876 / 901 nelle due passate delle prestazioni; bordo superiore del titolo fermo (297 / 290,2 px: nessuno spostamento); **0** animazioni sul titolo. Reduced-motion invariato (0 animazioni, righe `transform: none`). L'hero resta IMMERSIVE per CD §3.1 (ricetta navy + mesh + grana invariata) e il budget «≤ 2 elementi chiave animati per vista» è rispettato: dopo il primo paint si animano la coreografia della porta (arco, vie, nodi, uscite, gradini, chiave) e la corrente; fotografia e palcoscenico solo con lo scroll. La deviazione da CD §3.1 resta da firmare (voce 6a). |
| 8 | L'etichetta d'uscita barrata dalle vie | **CHIUSA** sul criterio — con i difetti nuovi **13** (disegno delle salite; vie senza uscita a 64–80rem) e **14** (etichette arabe fuori dal palcoscenico) | 800 campioni per via (`getPointAtLength`) contro `getBBox` di ogni `<tspan>` ±1 unità: **0 / 0 / 0 / 0** per ogni etichetta a **1440 e 1280** in `fr` («Orientation» 551,5–636 × 178,2–193,2; «Formation» 562,9–636; «Mobilité» 575,9–636 × 363,1–379,2; «régulière» 566,8–636 × 377,1–393,2) e in `ar`, e a 1440 in `it` («Orientamento» da 538,5) e `en` («Regular / mobility»). Alone: `stroke rgb(11,26,51)` 4 px, `paint-order: stroke`; in colori forzati `CanvasText` su alone `Canvas` (misurato). La treccia resta a y 372–390 nel navy. **Il disegno, giudicato sulla cattura** (`a4_05_exits_8770_fr_1440_zoom.png`): fuori dall'arco le vie diventano un gomito a squadra e una salita quasi verticale sullo stipite fotografico — la via «person» sale di 190 unità fra x 535 e 551; le salite di «person» (verso «Orientation») e «university» (verso «Formation») **si incrociano** a y ≈ 361, fuori dal navy, e restano a meno di 5 unità (la larghezza del casing) per y 318–368 (difetto 13a). In `ar` lo zero è banale: le etichette stanno **fuori** dal viewBox (difetto 14). |
| 9 | Menu account del cassetto lontano dal riassunto | **CHIUSA** | 8771, `qa-person`, clic reale su «Menu» e sul riassunto: scarto fra il bordo iniziale della lista e quello del riassunto **0 px** a 390, 768 e 1024 in `fr` (bordo sinistro 20 / 40 / 40) e **0 px** sul bordo finale in `ar` (370 / 728 / 984); il `<details>` largo quanto il riassunto (134,5 × 44); lista 240 × 171 dentro il viewport; Esc chiude **solo** il menu (cassetto ancora aperto) e restituisce il focus al riassunto. Catture `a4_09_drawer_account_{fr,ar}_{390,768,1024}.png`. |
| 10 | Un anello, due compagni; due colori sul navy | **CHIUSA** | Focus emulato, Tab reale, lettura dopo 400 ms. **Chiaro** `outline 2px #1d8a93` + compagno **`0 0 0 2px #f4f3f0`** su: link lingua della barra (corrente e no), riassunto del menu account e sue voci, lock-up, `.main-nav__link`, `.main-nav__toggle`, `.main-nav__sublink`, «Voir l'espace», `.nav-toggle`, e nel cassetto riassunto account, link lingua (corrente e no), voci e toggle (17 controlli). **Scuro** `outline 2px #7fd1d8` + **`0 0 0 2px #0b1a33`** su primario, secondario e righe della legenda (prima e quarta). Il sotto-link corrente tiene il filetto d'accento con l'anello (`inset 3px 0 0 #0f6a72, 0 0 0 2px #f4f3f0`; `a4_11_mega_current_sublink_zoom.png`). Nessun alone V2 da 5 px sulle superfici del gate. Stato perso: la pillola della lingua corrente perde la sua `--shadow-1` mentre ha il focus (il fondo `#fbfaf8` resta) — accettabile. Colori forzati: `outline 2px` di sistema, `box-shadow: none`. Catture `a4_10_ring_hero_primary_zoom.png`, `a4_10_ring_legend_1440.png`, `a4_10_ring_lang_zoom.png`, `a4_10_ring_drawer_1024.png`. La regola `:is(.utility-bar, .site-header, .hero) :focus-visible` tocca solo l'hero della home: `templates/components/hero.html` non è incluso da nessun template, l'hero del forum è `.forum-hero`. |

## 1. BEFORE / AFTER (§73)

| Vista | BEFORE | AFTER | Verdetto «materialmente superiore» (sì/no + una frase) |
|---|---|---|---|
| Desktop 1440 | `docs/qa/chrome/design-v4/before/01_home.png` (V2 interim); terzo giro `after/review_a3/a3_04_home_8770_1440.png` | `a4_05_exits_8770_fr_1440.png` (interim), `a4_10_ring_legend_1440.png` (fase 3) | **Sì.** La composizione del terzo giro con le uscite finalmente libere (0 campioni nelle etichette, «MOBILITÉ / RÉGULIÈRE» su due righe con alone) e il titolo fermo. Il prezzo: le vie escono dall'arco con gomiti a squadra e salite verticali che si incrociano sullo stipite (difetto 13a, `a4_05_exits_8770_fr_1440_zoom.png`). |
| Desktop 1280 · 1366 · 1439 | terzo giro `a3_08_header_8771_1280.png` | `a4_05_exits_8770_fr_1280.png`; testata misurata a 1280 / 1366 / 1439 | **Sì.** Sette voci con **31,4 px** d'aria fra lock-up e lista a 1280, 1366 e 1439 (lista 761,7; fine 1180,5 ≤ 1220,5 a 1280, 1260 ≤ 1300 a 1439); interim 356,3 px; legenda 264 con righe da 44. |
| Tablet 768 · 1024 | terzo giro `a3_06_home_8770_768.png` | `a4_04_home_8770_768_mobile.png`, `a4_06_legend_8770_1024.png` | **Sì.** A 768 le azioni dell'interim dentro la piega (1 007,8); a 1024 legenda 236 con quattro righe da 44. A 1024 tre vie escono a destra dell'arco e finiscono nel vuoto (difetto 13b). |
| Mobile 390 | terzo giro `a3_06_home_8770_390_mobile.png` | `a4_04_home_8770_390_mobile.png`, `a4_04_home_8771_390_mobile.png` | **Sì.** Porta → titolo → lead → azioni (24 px, lo stesso passo) → corpo; interim 129,2 % con la seconda azione a 816,8; `phase3` 124,1 %. |
| Stato interattivo (hover/focus/press/aperto) | terzo giro `a3_02_*`, `a3_08_*`, `a3_12_*` | cassetto `a4_02_drawer_open_*`; menu account `a4_09_*`; anello `a4_10_*`, `a4_11_*`; rotazione e ridimensionamento `a4_02b_rotate_phone.png`, `a4_02b_resize_600-1024.png`, `a4_02b_resize_1024-600.png` | **Sì.** Lock-up e «Menu» fuori dal velo, menu account sotto il suo riassunto, un anello solo. **Ma** a cassetto aperto una rotazione del telefono fa coprire lock-up e «Menu» dal cassetto (difetto 12). |
| RTL (ar) | terzo giro `a3_10_home_ar_*` | `a4_05_exits_8770_ar_1440.png`, `a4_05_exits_8770_ar_1280.png`, `a4_08_home_ar_8770_1440.png`, `a4_08_home_ar_8771_1440.png`, `a4_08_home_ar_8770_390.png`, `a4_08_home_ar_8771_390.png` | **Sì.** H1 a filo del bordo finale: inchiostro destro = bordo del blocco **1 332,5 / 1 180,5 / 969 / 370** a 1440 / 1280 / 1024 / 390 (Δ 0) su 8770 e 8771; legenda a quattro righe da 44; menu account del cassetto al bordo finale (0 px). Le uscite arabe stanno fuori dal palcoscenico, a 17,7 px dalla colonna del testo a 1440 (difetto 14). |
| Reduced-motion | terzo giro `a3_09_reduced_motion_*` | `a4_07_reduced_motion_8770_1440.png`, `…_8770_390.png`, `…_8771_1440.png`, `…_8771_390.png` | **Sì.** `document.getAnimations().length` **0** al caricamento e dopo 1,5 s (8770 e 8771, 1440 e 390); righe del titolo `none`; invisibili solo le quattro correnti (per direzione §4.4) e la didascalia chiusa; a 390 vie e uscite `display: none` (la legenda sostituisce il diagramma, §4.5); uscite a opacità 1 a 1440. |
| Forced-colors | terzo giro `a3_09_forced_colors_*` | `a4_07_forced_colors_8770_1440.png`, `a4_07_forced_colors_8770_exits_zoom.png`, `a4_07_forced_colors_8771_1440.png` | **Sì.** Uscite `CanvasText` su alone `Canvas` (nuovo, leggibili), vie `CanvasText`, legenda `Canvas` con bordo, parole `LinkText`, bottoni con bordo 1 px, lingua corrente `outline 2px`, `filter: none` su porta e arco interno, focus `outline 2px` di sistema. Osservato (non misurato): dentro l'arco interno, che resta navy, la treccia nera si legge appena. |

## 2. I ruoli (§71) — cinque firme, cinque punteggi indipendenti

Limite dichiarato: **un solo agente revisore** ha compilato le sei righe (la direttiva chiede cinque revisori
distinti); per ogni dimensione vale il punteggio più basso fra i ruoli che la giudicano.

| Ruolo | Cosa giudica in via primaria | Firma | Note |
|---|---|---|---|
| Creative Director | Premium Feel · Modernity · Originality · Visual Depth · coerenza con `CREATIVE_DIRECTION.md` | revisore indipendente, 25–26/09/2026, quarto giro | Chiusi lo scrim sopra la testata, l'etichetta barrata e il titolo che lampeggiava. Contro: il componente firma ha ora gomiti a squadra e salite verticali che si incrociano sullo stipite (13a); a 64–80rem vie verso uscite che non ci sono (13b); in arabo le uscite pendono fuori dal palcoscenico (14); il disegno della porta si vede completo, sparisce e si ridisegna (11). Deviazioni non firmate: lead non corsivo, titolo senza reveal, deroga a 390 (tutte da CD §3.1). |
| UX Lead | Clarity · Interaction Quality · Mobile · efficienza (§89) | revisore indipendente, 25–26/09/2026, quarto giro | Chiusi: menu account sotto il riassunto, «Menu» mai velato, deroga a 390 e piega a 768. Contro: rotazione o ridimensionamento a cassetto aperto (12); toggle 24 × 44 anche dove c'è aria per 44 (interim); nel mega-menu la freccia su finisce sul chevron, dove le frecce non fanno più nulla e ↓ scorre la pagina (15). |
| Motion Lead | Motion · budget (§67) · pattern (DS §7) · reduced-motion | revisore indipendente, 25–26/09/2026, quarto giro | Titolo fermo (0 fotogrammi nascosti). Contro: la coreografia del palcoscenico riparte da una composizione già dipinta — vie, nodi e le tre uscite spariscono per ≈ 1,5 s e si ridisegnano (11); la testata transisce ancora `min-block-size` 64 → 56. Reduced-motion completo. |
| Frontend Lead | token (DS): nessun valore arbitrario · CSP · nessun `style=""` · prestazioni (§68) | revisore indipendente, 25–26/09/2026, quarto giro | 0 `style=` e 0 script inline nell'HTML servito, 0 violazioni CSP, token rispettati (test verde). Contro: LCP 3,04–3,12 s su 4G lento, font 356 KB, 22 fogli (99,0 KB gzip, 1 KB sotto il budget proposto), HTML non compresso; budget non adottato. |
| Accessibility Reviewer | Accessibility · contrasto misurato · tastiera · screen reader · RTL · forced-colors | revisore indipendente, 25–26/09/2026, quarto giro | Chiusi: nomi della legenda = parola con descrizione, un anello solo con la coppia scura sul navy. Contro: descrizioni francesi sotto nomi arabi su 8771 `/ar/`; dopo una rotazione «Menu» coperto dal cassetto tranne 14 px; frecce del mega-menu (15); `test_rtl_browser` non eseguito. |
| Red Team indipendente (§75–78) | i quattro test | revisore indipendente, 25–26/09/2026, quarto giro | Vedi §4: NO · NO · SÌ · NO. |

## 3. Le dieci dimensioni (§74) — scala 1–5 con ancore

**Critiche** (una sola ≤ 2 → **BLOCK**): Premium Feel · Modernity · Clarity · Institutional Credibility ·
Accessibility · Mobile. **Di sostegno** (≤ 2 → al massimo CONDITIONALLY_READY): Visual Depth · Motion ·
Originality · Interaction Quality. Fra parentesi il punteggio del terzo giro.

| # | Dimensione | Punteggio | Osservazione (cosa, dove, in Chrome) |
|---|---|---|---|
| 1 | **Premium Feel** (critica) | **3** (3) | I quattro dettagli del terzo giro sono chiusi e misurati (scrim sotto la testata: lock-up 0,63–0,89 / 255; uscite libere: 0 campioni; menu account a 0 px; titolo: 0 fotogrammi nascosti). Ma le correzioni ne hanno prodotti o lasciati scoperti altri quattro, visibili nella variante in vigore: (a) le uscite disegnate come gomito + salita verticale sullo stipite, con due vie che si incrociano a y ≈ 361 sulla pietra e restano a < 5 unità per 50 unità (`a4_05_exits_8770_fr_1440_zoom.png`) — il componente firma legge come un cablaggio; (b) a 1024–1279 tre vie che escono dall'arco e finiscono nel vuoto 12 px oltre la porta (`a4_06_legend_8770_1024.png`); (c) in arabo le uscite fuori dal palcoscenico, a 17,7 px dal titolo (`a4_05_exits_8770_ar_1440.png`); (d) a ogni caricamento vie, nodi e uscite visibili, poi spariti ≈ 1,5 s e ridisegnati (difetto 11 — lo stesso difetto del titolo, corretto solo sul titolo). Il materiale resta quello del DS. È l'ancora 3: «superfici e controlli del sistema, ma dettagli non allineati». |
| 2 | **Modernity** (critica) | **4** (4) | Grammatica 2026 coerente: barra 32 + testata 64 → 57 in vetro, indicatore che trasla, mega-menu dal bordo, segmentato, Menu V4, cassetto a schermo intero dal piede misurato della testata, anello unico. Non 5: mega-menu ancora elenco a chevron su due colonne, nessuna transizione di pagina. |
| 3 | **Visual Depth** | **4** (4) | L'ordine dei livelli a menu aperto è ora giusto (testata sopra, scrim e cassetto dal suo piede). Legenda e didascalia L3 in vetro, Menu L3 a due strati, testata scrollata L3, hero IMMERSIVE. Non 5: la luce (mesh) sotto la soglia di percezione; dopo una rotazione il cassetto (L4) si dipinge sopra la testata (12). |
| 4 | **Motion** | **3** (3) | Chiuso il difetto 7 (titolo fermo, 0 fotogrammi nascosti su 666 / 638 / 244 / 324). Resta 3: (a) il palcoscenico ripete lo stesso schema — su 8770 senza limiti vie, nodi e uscite sono completi dal primo campione (131 ms), a **335 ms** passano a `stroke-dashoffset 1` e opacità **0** e restano nascosti per **165 fotogrammi** (fino a 1 793 ms); su 4G lento + CPU ×4 (8772) sono leggibili dal primo paint (1 537 ms) per 1,2 s, poi **nascosti da 2 759 a 4 346 ms** (100 fotogrammi) — il commento di `home.js` dice il contrario (difetto 11); (b) la testata transisce ancora `min-block-size` (proprietà di layout; l'ancora 4 chiede 0 layout). Budget per vista rispettato (coreografia della porta + corrente), reduced-motion completo (0 animazioni). |
| 5 | **Clarity** (critica) | **4** (4) | Un H1, lead Plex 20/28, corpo, una primaria + una secondaria, legenda con parola e gloss in didascalia; le tre uscite ora leggibili (0 vie nelle etichette, alone). Non 5: su 8771 `/ar/` titolo inglese, lead, corpo e ora anche le descrizioni della legenda in francese sotto nomi arabi (decisione pendente); a 1024–1279 le vie puntano a uscite che non ci sono. |
| 6 | **Institutional Credibility** (critica) | **4** (4) | A menu aperto il marchio e la riga del promotore non sono più velati a nessuna larghezza (0,63–0,89 / 255 sul lock-up). Lock-up intatto con 31,4 px d'aria a 1280–1439, H1 arabo a filo (Δ 0 a quattro larghezze), nessun dato finto, testi bloccati invariati (le uscite sono le stesse parole dell'eyebrow, spezzate in due `<tspan>`). Al limite: dopo una rotazione a menu aperto il cassetto taglia a metà il lock-up (`a4_02b_rotate_phone.png`). |
| 7 | **Originality** | **4** (4) | Senza logo si riconosce ILE: carta minerale e navy del marchio, Newsreader 300 + Plex, la porta con chiave e gradini, le quattro vie ancorate alla legenda e intrecciate alla soglia, il segmentato con «ع». Non 5: il componente firma perde la sua curva fuori dall'arco (gomiti a squadra, 13a) e il mega-menu non ha la sua firma (dischi, fotografia). |
| 8 | **Interaction Quality** | **3** (3) | Chiusi e misurati i punti del terzo giro: «Menu» fuori dal velo (`elementFromPoint` = sé stesso, 12 casi), menu account sotto il riassunto (0 px, LTR e RTL, Esc che chiude solo il menu), un anello solo (17 + 3 controlli). Frecce del mega-menu su 8771 come nel terzo giro («Personnes» ↓ «Votre parcours» ↓ «Diplômes et titres» ↑ → «Entreprises» ↓ «Besoins professionnels», Esc sul toggle). Resta 3 per tre stati non allineati (§93): (a) a cassetto aperto, rotazione 390 × 844 → 844 × 390 o ridimensionamento 600 → 1024: cassetto e scrim restano a 57 px con la testata che finisce a 98 — lock-up e «Menu» sotto il cassetto (`elementFromPoint` = `div.nav-drawer`); all'inverso una banda di 41 px di pagina né velata né coperta (difetto 12); (b) mega-menu su 8770: ↑ dal primo link del pannello porta al chevron, dove → non fa nulla e ↓ **scorre la pagina** a pannello aperto (difetto 15); (c) toggle del sotto-menu **24 × 44** a 1280–1439 anche sulla variante con 356 px d'aria. |
| 9 | **Mobile** (critica) | **3** (3) | La condizione posta dal terzo giro è soddisfatta: interim **129,2 %** a 390 × 844 con la seconda azione a 816,8 (27,2 px di margine), `phase3` 124,1 %, a 768 azioni dentro la piega (1 007,8), bersagli 44 al tocco (terzo giro, invariati), nessuno scroll orizzontale. Resta 3 per un fatto nuovo, proprio del telefono: **ruotato a cassetto aperto** (390 × 844 → 844 × 390) il cassetto copre la testata dal suo 57° px — di «Menu», l'unico comando di chiusura su un telefono (non c'è Esc), restano visibili i 14 px superiori, e il lock-up è tagliato (`a4_02b_rotate_phone.png`, difetto 12): «azioni difficili da raggiungere» in quello stato. In più la deroga è tarata su un solo apparecchio: a 375 × 812 l'interim è 136,3 % e la seconda azione finisce 20,8 px sotto la piega (360 × 800: 142,3 %, −32,8). Chiuso il 12 e scritta la deroga con la sua gamma di viewport, la dimensione vale 4. |
| 10 | **Accessibility** (critica) | **4** (4) | Nomi della legenda = parola (fr/ar), gloss come descrizione (47–126 caratteri); un anello, un compagno; la coppia scura `#7fd1d8` / `#0b1a33` su ogni controllo dell'hero; tastiera nel mega-menu, nel cassetto (Esc con ritorno del focus) e nel Menu; H1 arabo a filo; reduced-motion e colori forzati completi (uscite leggibili in colori forzati). Non 5: descrizioni francesi sotto nomi arabi su 8771 `/ar/`; dopo una rotazione il bottone «Menu», se a fuoco, è coperto tranne 14 px (2.4.11 soddisfatto al minimo, 2.4.12 no); il chevron del mega-menu come vicolo cieco delle frecce (15); contrasti sui pixel non ri-misurati (§7); `test_rtl_browser` non eseguito. |

## 4. I quattro test (§75–78) — Red Team indipendente

| Test | Domanda | Risposta richiesta | Risposta | Perché, esattamente (elemento, cattura) |
|---|---|---|---|---|
| Generic AI | «Potrebbe essere scambiato per un template generico Claude/AI?» | **NO** | **NO** | Carta minerale e navy del marchio, Newsreader 300 maiuscolo + IBM Plex, la porta con chiave e gradini attraversata da quattro vie ancorate a una legenda in vetro, il segmentato con «ع», il lock-up ufficiale (`a4_05_exits_8770_fr_1440.png`, `a4_10_ring_legend_1440.png`). Il punto fragile resta il pannello del mega-menu (bianco, due colonne a chevron). |
| Editorial | «Sembra ancora principalmente una pubblicazione editoriale/legale?» | **NO** | **NO** | Il serif è solo nell'H1; lead, corpo, legenda, didascalia, nav, Menu in Plex; CTA a gradiente; il titolo ora fermo pesa come un titolo di prodotto, non come un frontespizio. Avvertenza invariata: sotto l'hero riprende la pagina V2. |
| 2026 | «Nascosto il logo, competerebbe con prodotti digitali premium del 2026?» | **SÌ** | **SÌ** | Stati e profondità reggono (testata stabile, cassetto dal piede misurato, Menu V4, anello unico, legenda senza salti, reduced-motion completo). Ciò che un prodotto premium del 2026 **non** spedisce, ed è la lista di §6: il disegno che si vede e si ridisegna (11), il cassetto che dopo una rotazione copre marchio e «Menu» (12), le salite che si incrociano sullo stipite e le vie verso uscite nascoste (13), le uscite arabe fuori dal palcoscenico (14). |
| Too much | «Abbiamo aggiunto effetti inutili solo per sembrare moderni?» | **NO** (altrimenti: elenco di cosa togliere, nell'ordine di `CREATIVE_DIRECTION.md` §6.4) | **NO** | Questo giro ha **tolto** un effetto (il reveal del titolo) e non ne ha aggiunti; l'alone delle uscite è leggibilità, non effetto. La coreografia del palcoscenico è prescritta (CD §4.4): il difetto 11 è di esecuzione (parte da una composizione già dipinta), non un effetto da togliere per §6.4. |

## 5. Verifiche binarie (tutte devono essere «sì»)

| Verifica | Sì/No | Prova |
|---|---|---|
| Nessuna formulazione vietata (`apps/cms/forbidden.py`), nessun testo bloccato alterato | **Sì** | Diff dd29168 → 156db5f: `_hero.html` (le uscite come `<tspan>` delle stesse parole, `aria-describedby`, `aria-hidden` sul gloss, commento), `_hero_title_lines.html` (commento), `services.py` (percorso e righe delle uscite); nessun testo toccato. `tests/compliance/test_locked_content.py`, `test_public_pages.py`, `test_phase3_texts_not_leaked.py` verdi (nota A). |
| Nessun `style=""`, nessuno script inline, nessun hotlink (CSP) | **Sì** | HTML servito di `/fr/` (8770, 8771, 8772): **0** ` style=`, 6 `<script>` di cui **0** inline; CSP con `script-src 'self'`, `style-src 'self'`, `font-src 'self'`, `img-src 'self' data:`; listener `securitypolicyviolation` installato prima del caricamento su 8772 (due passate 4G): **0** violazioni. `--nav-drawer-top` è scritto via CSSOM (`style.setProperty`), che la CSP non blocca. |
| Nessun valore fuori dai token (colori, raggi, ombre, durate, curve) | **Sì** | `tests/frontend/test_v4_tokens.py` e `test_design_docs.py` verdi (nota A); i valori nuovi del giro sono token (`--mid-1` per l'alone, `--s-10`, `--s-2` / `--s-6`, `--focus-ring-*`, `--accent-dark`); i numeri nuovi sono geometria SVG (543, 555, 14 unità d'interlinea) e una larghezza di layout (236 px). |
| «Nessun colore significa mai approvato»: nessun chip `conforme` con croma, nessun verde di verdetto | **Sì** | Nessun chip nelle superfici del gate; l'unico verde è quello del marchio nel lock-up. |
| Nessun dato, contatore, avatar, grafico o KPI finto | **Sì** | Nessun numero nell'hero e nella testata; le vie sono le `entrances()` reali; le uscite le parole dell'eyebrow; il menu account mostra `qa-person`. |
| Coordinate, «svg», «Suspendre le mouvement», etichette di debug: assenti | **Sì** | HTML servito (8770, 8771): 0 «Suspendre», 0 «svg» nei nodi di testo, 0 coordinate, 0 id duplicati (33 / 39 id). |
| Reduced-motion: pagina completa, nulla a opacità 0 | **Sì** | §1, riga Reduced-motion: 0 animazioni, titolo `none`, uscite a opacità 1; invisibili solo le correnti (per direzione) e la didascalia chiusa. |
| Contrasto sul peggior fondo (incluso sotto il vetro) ≥ 4,5 testo / ≥ 3 UI | **Sì** | Superfici con testo invariate nei colori e nei fondi (misure sui pixel del secondo giro); nuovo: anello scuro `#7fd1d8` su `#0b1a33` (token, ≈ 9,9 : 1) su ogni controllo dell'hero; le uscite hanno ora un alone `--mid-1` sotto le lettere (non ri-misurate sui pixel: §7). |
| Prestazioni: JS/CSS ≤ budget, LCP < 2,5 s, CLS < 0,1, INP < 200 ms (4G simulato) | **No** | §0-bis riga 3: LCP **3 040 / 3 124 ms** (la fotografia della porta) > 2 500; CLS 0,0037 / 0,0032 ✓; INP-proxy 64 ms (incidentale) ✓; CSS 99,0 KB ✓ sul budget proposto (1 KB di margine), JS 35,6 ✓, font **356,1** ✗ (proposto 200); budget non scritto in §68/DS; HTML non compresso. |
| RTL (ar) a tre larghezze senza proprietà fisiche nel CSS nuovo | **Sì** | Le regole nuove usano proprietà logiche (`inset-inline: 0 auto`, `justify-self: start`, `padding-block-start`, `margin-block`) e la variante `[dir="rtl"]` del filetto del sotto-link; H1 a filo a 1440 / 1280 / 1024 / 390 (Δ 0); menu account del cassetto a 0 px dal bordo finale in RTL; `tests/i18n/test_rtl_static.py` verde (nota A); `tests/i18n/test_rtl_browser.py` **non eseguito**. (Le uscite arabe fuori dal palcoscenico sono un difetto di composizione, 14, non una proprietà fisica.) |
| Demo page dei componenti coerente (§94) | **Sì, parziale** | `/_design/` (8770, HTML servito): sezione «Navigation» con segmentato, pannello del mega-menu e Menu account; **0** id duplicati (94 id), 0 `style=`, 0 script inline; **assenti** legenda in vetro, didascalia e porta (come nei giri precedenti). `tests/frontend/test_design_showcase.py` verde (nota A). |

**Nota A — esito dei test** (database dedicato `ile_lane4`, mai in parallelo fra loro):
1. `tests/frontend/test_design_docs.py tests/frontend/test_v4_tokens.py tests/frontend/test_frontend_bundle_is_current.py apps/pages/tests -q`
   — **395 passed in 903,06 s**, exit 0 (uscita in `review_a4/pytest_a4_fast.txt`, fuori dal repository).
2. `tests/compliance/test_locked_content.py tests/compliance/test_public_pages.py tests/compliance/test_phase3_texts_not_leaked.py tests/i18n/test_rtl_static.py tests/frontend/test_design_showcase.py tests/frontend/test_header_fits_the_narrowest_viewport.py tests/frontend/test_svg_wellformed.py tests/frontend/test_template_comments_do_not_leak.py -q`
   — **88 passed in 124,39 s**, exit 0 (`review_a4/pytest_a4_compliance.txt`). `test_header_fits_the_narrowest_viewport.py`
   lancia un Chromium headless proprio con Playwright, non la scheda visibile (nessun test attacca 9222: `grep` su `tests/`).

Il «727 passed, 1 xfailed» del builder (frontend + pages + cataloghi) non è stato ri-eseguito per intero; la parte
richiesta sì.

## 6. Esito

| Esito | Condizione |
|---|---|
| **PASS** | tutte le critiche ≥ 4, tutte le dimensioni di sostegno ≥ 3, quattro test corretti, tutte le verifiche «sì», AFTER materialmente superiore su ogni vista |
| **CONDITIONALLY_READY** | tutte le critiche ≥ 3 e nessuna ≤ 2, al massimo due dimensioni di sostegno ≤ 2, quattro test corretti, verifiche «sì»; correzioni elencate con scadenza; **nessuna propagazione** finché non diventa PASS |
| **BLOCK** | una dimensione critica ≤ 2, **oppure** un test sbagliato, **oppure** una verifica «no», **oppure** AFTER non materialmente superiore |

Esito del gate: ☐ PASS ☐ CONDITIONALLY_READY ☒ **BLOCK**

Motivazione, nell'ordine delle regole: nessuna dimensione critica ≤ 2 (Premium Feel **3**, Modernity 4, Clarity 4,
Credibility 4, Mobile **3**, Accessibility 4), nessuna di sostegno ≤ 2 (Visual Depth 4, Motion 3, Originality 4,
Interaction Quality 3), i quattro test corretti, l'AFTER materialmente superiore su ogni vista. Sulle dimensioni e sui
test il gate sarebbe **CONDITIONALLY_READY** — non PASS: Premium Feel e Mobile sono a 3. Lo tiene a **BLOCK** **una sola**
verifica binaria, come nel secondo e nel terzo giro: le prestazioni (LCP 3,04–3,12 s su 4G lento contro 2,5; budget
non adottato; le leve — carattere del lock-up, corsivo della fascia forum, concatenazione dei fogli, HTML compresso —
restano del committente).

Il revisore dice anche che questo giro è stato **eseguito bene sul suo criterio**: delle nove correzioni del terzo
giro sette sono chiuse sulla misura (2, 4, 5, 7, 8, 9, 10), due parziali (3, 6), nessuna regredita, e i numeri del
README (§4.8, «Terzo giro») sono stati ritrovati (con un'eccezione: l'argomento sul toggle, voce 6c). Non avvicina però
il PASS sulle dimensioni: le stesse correzioni hanno prodotto o lasciato scoperti cinque difetti (11–15) — due sono il
rovescio diretto di una correzione (13 dalle salite di 8, 12 dal bordo misurato solo all'apertura di 2), uno è lo
stesso difetto del titolo lasciato al palcoscenico (11).

Correzioni richieste (numerate: prima le correzioni ancora aperte del terzo giro con il loro numero, poi i difetti
nuovi da 11; ognuna con dimensione, elemento, cattura, criterio di chiusura):

3. **Prestazioni — verifica binaria 9.** Dimensione: Frontend Lead. Misura: §0-bis riga 3. Criterio (invariato): su 8772,
   4G lento + CPU ×4, due passate, **LCP < 2,5 s**, CLS < 0,1, INP-proxy < 200 ms; il budget **scritto** in §68/DS e
   rispettato o con deroga firmata; i font della home entro il budget o una decisione scritta su lock-up (128,9 KB) e
   corsivo (143,4 KB); la riduzione dei 22 fogli con una data (il CSS è a 1 KB dal tetto proposto: ogni riga in più di
   `v4/*.css` lo supera); HTML: compresso o decisione scritta (BREACH) registrata nel gate.
6. **Documentazione e decisioni** (nessun codice, o poco). (a) Firmare in `CREATIVE_DIRECTION.md` (o in una sua appendice
   di deviazioni) le tre deviazioni da §3.1: lead non corsivo, titolo senza reveal, deroga a 390 — quest'ultima con la
   gamma di viewport per cui vale (a 375 × 812 l'interim è 136,3 % e la seconda azione a −20,8 px; a 360 × 800 142,3 %,
   −32,8 px). (b) Le decisioni pendenti del committente/CD: lingue di lead, corpo **e descrizioni della legenda** su
   `/ar/` (8771: descrizioni francesi di 101–126 caratteri sotto nomi arabi), terza colonna del mega-menu, sette voci,
   carattere del lock-up. (c) Il residuo del toggle: portarlo a 44 dove c'è aria (interim: 356,3 px) o correggere
   l'argomento del README (tre toggle, lista 761,7, aria 31,4 su `phase3`). Criterio: le firme e le decisioni scritte;
   il toggle 44 × 44 a 1280–1439 sulla variante interim, o l'argomento con i numeri misurati.
11. **Il palcoscenico si vede completo, sparisce e si ridisegna.** Dimensioni: Motion, Premium Feel. Elementi:
    `static/js/src/home.js:120–140` (`withMotion` → `animate(trace, { strokeDashoffset: [1, 0] })`, `animate(lines,
    { strokeDashoffset: [1, 0] }, { delay: stagger(0.12, { startDelay: 0.6 }) })`, `animate(arriving /* nodi e uscite */,
    { opacity: [0, 1] }, { delay: 1.5 })`) eseguito dal modulo differito **dopo** il primo paint; commento di testa
    `home.js:7–8` («Everything … complete on the first frame — door, key, steps, routes … What moves is drawn ON TOP of a
    complete composition»). Misura (storia per fotogramma di `[data-doorway-exits]`, primo `[data-route-node]`, prima e
    ultima `[data-route-line]`, `[data-doorway-trace]`): 8770 senza limiti, tutto completo dal primo campione (131 ms),
    a **335 ms** uscite e nodi a opacità **0** e vie a `stroke-dashoffset 1`, nascosti per **165 fotogrammi** fino a
    1 793 ms; 8772 su 4G lento + CPU ×4, leggibili dal primo paint (1 537 ms) per 1,2 s, poi **nascosti da 2 759 a
    4 346 ms** (100 fotogrammi) — le tre parole delle uscite comprese. È lo stesso schema del difetto 7, corretto sul
    titolo e lasciato al palcoscenico. Cattura: nessuna (è una sequenza; misura in `review_a4/r3_stage_frames.py`).
    Criterio: **0 fotogrammi** in cui una via, un nodo o un'etichetta d'uscita passa da visibile a nascosta, senza
    limiti e su 4G lento; o la coreografia disegna **sopra** la composizione completa (come la traccia dell'arco), o lo
    stato iniziale è applicato prima del primo paint senza peggiorare l'LCP misurato su 8772; commento vero;
    reduced-motion invariato.
12. **Il cassetto non segue la testata dopo un ridimensionamento o una rotazione.** Dimensioni: Mobile, Interaction
    Quality, Institutional Credibility. Elementi: `static/js/main.js:155–163` (`--nav-drawer-top` misurato e scritto
    **solo all'apertura**; nessun ascolto di `resize` / orientamento; `DESKTOP` chiude il cassetto solo oltre 80rem),
    `static/css/v4/shell.css:497–498` (`.nav-overlay`), `static/css/components.css:826` (`.nav-drawer`). Misura (8770,
    clic reale su «Menu», poi `setDeviceMetricsOverride`): 390 × 844 → **844 × 390** (`mobile: true`, orientamento
    orizzontale): testata 33–**98**, cassetto e scrim ancora da **57** → `elementFromPoint` al centro del lock-up e di
    «Menu» = `div.nav-drawer`, di «Menu» restano visibili 14 px; 600 → 1024 (desktop): identico; all'inverso 844 × 390
    → 390 × 844 e 1024 → 600: testata finita a 57, cassetto e scrim da **98** → banda di **41 px** di hero né velata né
    coperta; 768 × 1024 → 1024 × 768: corretto (98 = 98); 1024 → 1300: il cassetto si chiude. Catture
    `a4_02b_rotate_phone.png`, `a4_02b_resize_600-1024.png`, `a4_02b_resize_1024-600.png`. Criterio: a cassetto aperto,
    dopo ciascuna delle quattro transizioni sopra, bordo del cassetto e dello scrim = piede della testata ±1 px entro
    un fotogramma, e `elementFromPoint` su lock-up e «Menu» = l'elemento stesso (per esempio misurando la testata con
    un `ResizeObserver`, o chiudendo il cassetto al cambio di orientamento).
13. **Il disegno delle uscite.** Dimensioni: Premium Feel, Originality. Elementi: `apps/pages/services.py:405` e
    `static/js/src/home.js:60–61` (`C543 yOut, 543 exitY, 555 exitY H624`); `static/css/v4/hero.css:387–389`
    (`.doorway__exits { display: none }` sotto 80rem) contro la classe `doorway--exits`, che decide il percorso a ogni
    larghezza. (a) Misura (i tracciati vivi letti da `getAttribute('d')` a 1440, ricampionati a 20 000 punti per curva):
    la via «person» sale di 190 unità (y 390 → 200) fra x 535 e 551, sullo stipite fotografico; le salite di «person» e
    «university» **si incrociano a y ≈ 361** (distanza minima 0,02 unità), fuori dal navy (che finisce a x 531), e
    restano a meno di 5 unità — la larghezza del casing — per y 318–368; le vie «company» e «institution» condividono il
    tratto 555–624 a y 400 (quattro vie, tre uscite: atteso). Cattura `a4_05_exits_8770_fr_1440_zoom.png`: gomiti a
    squadra e fili affiancati dove CD §4.1 vuole una treccia **nel** navy (contrasto ≥ 8,7 : 1). (b) Fra 64 e 80rem le
    uscite sono nascoste ma le vie salgono lo stesso alle loro quote e corrono in piano fino a x 624: a 1024 (palcoscenico
    misurato 529 + 441 px) i tre tratti finiscono a ≈ 959 px, 12 px oltre il bordo della porta (947), senza nodo né
    parola (`a4_06_legend_8770_1024.png`; CD §4.5: «tra 1024 e 1279 … senza le tre uscite»). Criterio: (a) fuori dal
    navy nessun incrocio e due vie dirette a uscite diverse sempre a ≥ 6 unità (il passo della treccia) fino al loro
    piano; 0 campioni nelle etichette a 1280 e 1440, LTR e RTL; (b) sotto 80rem le vie finiscono dove finisce il disegno
    (all'uscita dall'arco o sulla stessa soglia), 0 tratti che terminano senza nodo.
14. **Le uscite arabe fuori dal palcoscenico.** Dimensioni: Premium Feel, RTL (Accessibility Reviewer). Elemento:
    `.exit__label` con `text-anchor="end"` a x 636 (`templates/pages/home/_hero.html:71`): in `direction: rtl` la fine del
    testo è a sinistra, quindi l'etichetta va **a destra** del nodo. Misura (8770 `/ar/`, `getBBox` dei `<tspan>`):
    x **636–672,6** in un viewBox largo 640 — a 1440 l'etichetta sporge **30,3 px** oltre il riquadro dell'SVG (718,8
    contro 688,5) e si ferma a **17,7 px** dalla colonna del testo (736,5); a 1280, 26,3 px oltre e 21,7 px dalla
    colonna; corpo 12 unità = **9,8 px** a 1280. In `fr` / `it` / `en` le etichette stanno dentro (fino a 636) e sopra il
    nodo. Catture `a4_05_exits_8770_ar_1440.png`, `a4_05_exits_8770_ar_1280.png`. Criterio: in RTL le etichette dentro
    il viewBox (x ≤ 640) e nella stessa relazione con il nodo di LTR, a ≥ 24 px dalla colonna del testo a 1280 e 1440, e
    0 campioni di via nel loro riquadro.
15. **Mega-menu: il chevron come vicolo cieco delle frecce.** Dimensioni: Interaction Quality, Accessibility. Elemento:
    `static/js/main.js:74–92` e `:120–140` — l'↑ dal primo link del pannello mette il focus sul `[data-nav-panel-toggle]`
    (il chevron), che non è fra i `topLinks` né nel pannello: lì le frecce non sono gestite. Misura (8770, 1440, focus
    emulato): «Personnes» ↓ → «Votre parcours»; ↓ → «Voir l'espace» (primo nell'ordine del DOM, ma saltato all'apertura);
    ↑ → **chevron** a pannello aperto; → sul chevron: il focus non si muove; ↓ sul chevron: il focus non si muove e **la
    pagina scorre** (la testata passa da y 43 a 6); Esc chiude e resta sul chevron. Su 8771 lo stesso ciclo da
    «Votre parcours» ↑ porta a «Voir l'espace» e da lì al chevron. Criterio: da ogni fermata della barra (link e chevron)
    ↓ entra nel pannello e ← / → passano alla sezione vicina; ↑ dal primo link torna alla fermata che ha aperto il
    pannello; nessuna freccia scorre la pagina mentre il focus è nella barra; l'ordine delle frecce nel pannello è quello
    di lettura.

Note, non correzioni: in colori forzati l'arco interno resta navy e la treccia `CanvasText` vi si legge appena
(osservato su `a4_07_forced_colors_8770_exits_zoom.png`, non misurato; il diagramma è `aria-hidden` e la legenda porta
l'informazione); la pillola della lingua corrente perde la sua ombra di livello 1 mentre ha il focus (il fondo resta);
a 390, 768 e 1024 il cassetto è a schermo intero e lo scrim sfocato di CD §3.2 si vede solo nella transizione;
`is-related` invariata.

Firma del Creative Director (esito finale, §6 della direttiva): ______ · data/ora: ______

## 7. Ciò che non è stato possibile verificare, e perché (§95)

- **Lo stato finale della scheda**: la scheda del progetto è sparita dal Chrome di QA fra le 21:09 e le 21:10 del 25/09
  (nota in testa); il coordinatore l'ha ricreata su 8771 e autenticata come `qa-person`. Alla ripresa i target di 9222
  mostravano **due** pagine `127.0.0.1:8771` (`/fr/` e `/fr/espace-reserve/`); il revisore non le ha toccate né
  ri-autenticate, e non ha verificato quale delle due sia quella del progetto.
- **INP-proxy deliberato** (hover su una riga della legenda, clic sul chevron, Esc, hover sul secondario sotto CPU ×4):
  previsto dopo le 21:10, non fatto. C'è solo la durata massima degli eventi incidentali del puntatore nella seconda
  passata 4G (64 ms).
- **La geometria delle salite in pagina** (`r17_risers.py`, non eseguito per la scheda sparita): l'incrocio e le
  distanze del difetto 13a sono calcolati sui tracciati misurati in pagina (`d` letto a 1440 da `r4_exits.py`), non
  campionati con `getPointAtLength`; la fine dei tratti a 1024 (≈ 959 px) è calcolata dalla larghezza misurata del
  palcoscenico e osservata sulla cattura.
- **Contrasti sui pixel**: non ri-misurati; nuovo in questo giro l'alone `--mid-1` sotto le parole delle uscite (che
  toglie il contorno della porta dietro le lettere): leggibili sulla cattura, non misurati.
- **Lo scrim su `/fr/parcours/` e sulla pagina di accesso** (README: «stesso esito»): non ri-misurato dal revisore.
- **La leggibilità delle uscite arabe** a 9,8 px (1280): osservata sulla cattura, non valutata con un lettore arabo.
- **`test_rtl_browser`**: non eseguito (pilota un browser; fuori dall'insieme richiesto). Non ri-eseguita per intero la
  suite «727 passed» del builder (nota A).
- **Cinque revisori distinti** (§71): un solo agente ha compilato le sei righe.

## 8. Metodo e limiti

- Osservazione: Chrome visibile via `scripts/cdp.py` (`Page.attach(url_contains="127.0.0.1:")`), una sola scheda
  (`Page.bringToFront`, `visibilityState: visible`, 63 rAF in 500 ms all'inizio), sonde sequenziali; viewport emulati
  1440 × 900, 1439 / 1366 / 1280 / 1279 × 800, 1100 × 800, 1024 × 768, 768 × 1024, 600 × 768, 390 × 844, 375 × 812,
  360 × 800, 844 × 390 (con `mobile: true`, tocco e orientamento dove indicato); emulazioni azzerate a fine sonda
  (viewport, tocco, media, rete, CPU, focus, esecuzione degli script).
- Script del revisore: `C:\Users\<user>\AppData\Local\Temp\claude\C--tmp-italylegalentry\review_a4\` (`common.py`,
  `r0_window.py`, `r1_md5.py`, `r2_title.py`, `r3_stage_frames.py`, `r4_exits.py`, `r5_exit_shots.py`, `r6_legend.py`,
  `r7_scrim.py`, `r8_scrim_edge.py`, `r9_account.py`, `r10_ring.py`, `r11_mega.py`, `r11b_mega.py`, `r12_toggle_ax.py`,
  `r13_mobile.py`, `r14_perf.py`, `r15_media.py`, `r16_arabic.py`, `crop.py`; `r17_risers.py` scritto e non eseguito);
  HTML servito salvato in `home_8770.html`, `home_8771.html`, `home_8772.html`, `design_8770.html`; esiti dei test
  `pytest_a4_fast.txt`, `pytest_a4_compliance.txt`.
- Nessun file del repository modificato al di fuori di questa scorecard e delle catture in `review_a4/`.
