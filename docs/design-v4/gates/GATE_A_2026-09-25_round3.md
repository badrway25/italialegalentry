# GATE A — Homepage (hero) + Navbar · scorecard del 25 settembre 2026 — **terzo giro**

Compilata sul modello `docs/design-v4/GATE_SCORECARD_TEMPLATE.md` (§71–78 della direttiva). Regole
applicate: **nessuna media** (§74); **l'implementatore non vota** (§72); ogni punteggio cita ciò che il
revisore ha **osservato in Chrome visibile** (§70) — Google Chrome 153, CDP 9222, `scripts/cdp.py`, una sola
scheda, sonde sequenziali, `Network.enable` + `Network.setCacheDisabled` in testa a ogni sonda. Le misure sono
`getBoundingClientRect` / `getComputedStyle` / `elementFromPoint` / `getBBox` / `getPointAtLength` / attributi SVG /
`performance.getEntriesByType` / `PerformanceObserver` (LCP, layout-shift, longtask, event, installati con
`Page.addScriptToEvaluateOnNewDocument`) / campionamento a ogni `requestAnimationFrame` / eventi reali
(`Input.dispatchMouseEvent`, `Input.dispatchKeyEvent` con `Emulation.setFocusEmulationEnabled`,
`Emulation.setTouchEmulationEnabled` + `setDeviceMetricsOverride mobile: true` per il puntatore grossolano,
`Emulation.setEmulatedMedia` per reduced-motion e colori forzati, `Network.emulateNetworkConditions` 150 ms /
1,6 Mbit/s / 750 kbit/s + `Emulation.setCPUThrottlingRate` 4 per il 4G lento) e letture di pixel con Pillow sulle
catture del revisore. Le catture di questo giro stanno in `docs/qa/chrome/design-v4/after/review_a3/` (prefisso
`a3_`, ignorate da git: `.gitignore:30`); quelle del secondo giro in `…/after/review2/` (prefisso `r2_`). I percorsi
sono relativi alla radice del repository.

Nota sulle misure: la scheda del revisore riportava `devicePixelRatio` **1** (finestra 1905 × 1012) e tutte le
emulazioni sono state fatte con `deviceScaleFactor: 1`: `outline` e `border` si leggono in px CSS (2 px = 2 px).

Nota sulla ripresa: un primo tentativo di questo giro è stato interrotto da un riavvio della macchina; i suoi
script sono stati riletti e **ri-eseguiti** (adattati, prefisso `q`), e **nessuna** misura di questo documento
viene dalle sue uscite (non salvate). Le catture `a3_02_drawer_{390,768,1024}.png` (senza `open`) e i `_tmp_*` di
quel tentativo non sono citate; `a3_02_drawer_open_*` e `a3_04_home_*` sono state **sovrascritte** dalle sonde di
questo giro.

Questo documento verifica, correzione per correzione, le sei correzioni del secondo giro
(`gates/GATE_A_2026-09-25_round2.md`, esito BLOCK per la sola regola delle prestazioni), poi ri-assegna le dieci
dimensioni, i quattro test e le verifiche binarie. Ciò che i giri precedenti hanno misurato e non è cambiato non
viene ripetuto se non per riferimento.

---

## 0. Identità del gate

| Campo | Valore |
|---|---|
| Gate | **A** |
| Superfici | Homepage pubblica `/fr/`: hero «il portico» (porta, quattro vie, legenda in vetro con didascalia, titolo, lead, CTA; uscite etichettate nella variante interim) + navbar (barra istituzionale con controllo lingua e accesso/menu account, testata, indicatore, mega-menu, cassetto con segmentato); `/ar/` per RTL; la vetrina `/_design/` |
| URL / account | **8770** (`ile`, fase 3 chiusa → variante **interim**: eyebrow, titolo editoriale, tre uscite etichettate, quattro voci, «Espace réservé»); **8771** (`ile_qa`, fase 3 aperta → variante `phase3`, sette voci; scheda autenticata come **`qa-person`**: menu account sulla barra e nel cassetto); **8772** (lo stesso codice di 8770 dietro WhiteNoise gzip) per ogni misura di prestazione — verificato: `v4/hero.css`, `v4/shell.css`, `v4/buttons.css`, `main.css` e `pages/js/home.js` serviti da 8772 hanno lo stesso md5 dei file dell'albero. Il cookie di sessione è per host: ogni visita a 8770/8772 disconnette la scheda da 8771 (misurato due volte); la scheda è stata ri-autenticata con `scripts/qa_chrome_signin.py` e **lasciata autenticata come `qa-person` su 8771** alla fine. |
| Commit sotto revisione | **dd29168** (albero pulito dall'inizio alla fine: `git status` vuoto alle 19:12 e alle 19:55). Sulle superfici del gate, da d99f2bb (secondo giro): `apps/pages/services.py` (treccia a 372), `static/js/src/home.js` (`braidY: 372`), `static/css/v4/hero.css` (lead in Plex, legenda 264, regola `data-reveal` tolta, `filter: none` in colori forzati), `templates/pages/home/_hero.html` (`data-reveal` tolti, commento riscritto), `static/css/v4/shell.css` (`html { overflow-anchor: none }`, scrim, controlli lingua al tocco, voce araba sul carattere di sistema, anello della lingua corrente, Menu V4 dell'account), `static/css/v4/tokens.css`, `GATE_SCORECARD_TEMPLATE.md:83`. |
| Revisione | **terzo giro** (il secondo: `gates/GATE_A_2026-09-25_round2.md`, su d99f2bb, BLOCK per la sola verifica delle prestazioni, sei correzioni; il primo: `gates/GATE_A_2026-09-25.md`, su c6f3503) |
| Implementatore (non vota) | Claude (sessione principale) |
| Revisore indipendente | agente separato (sessione distinta; nessuna modifica a codice, template, fogli, script o test; nessun riavvio di server; nessun pacchetto installato; nessuna credenziale digitata; nessun modulo inviato) |
| Data e ora della revisione | 25 settembre 2026, ore 19:12–20:05 |

## 0-bis. Le sei correzioni del secondo giro — verifica una per una

| # | Correzione (secondo giro) | Stato | Prova (misura o cattura) |
|---|---|---|---|
| 1 | Testata che oscillava fra 25 e 32 px di scroll | **CHIUSA** | `getComputedStyle(html).overflowAnchor = none` (`v4/shell.css:90`). A 1440 su **8770 e 8771**, `scrollTo(y)` da pagina ferma e poi 3 s di osservazione (`MutationObserver` sulla classe + campioni a 100 ms): y **20** e **24** → 0 commutazioni, non scrollata, interno 64 / testata 65; y **25** → **una** commutazione (l'ingresso, a 3 ms / 9 ms) e poi ferma, interno 60,3 → **56**, `scrollY` sempre 25; y **28 / 30 / 32 / 40 / 60** → **0 commutazioni**, `scrollY` invariato, interno 56 / testata 57. Trascinamento lento 0 → 100 px a passi di 2 px ogni 30 ms: **una** commutazione reale (la sonda ne registra due: la prima è il ritorno a 0 dallo stato precedente); 100 → 0: una. Criterio del secondo giro («stabile entro 300 ms, 0 commutazioni nei 3 s, `scrollY` fermo, a ogni y fra 0 e 100») soddisfatto. Cattura `a3_01_header_scrolled_400_1440.png` (scrollata, 57 px). |
| 2 | Scrim del cassetto sopra la testata (768–1279) | **APERTA — REGREDITA** | Il README (§4.8) dice «ora dall'alto, `z-index` sotto la testata: misurato top 0 / 19 < 20». Misurato: lo scrim parte **da 0** e copre **tutta** la testata e la barra istituzionale, a **ogni** larghezza. `.nav-overlay` è **figlio** di `header.site-header` (genitore misurato: `HEADER.site-header`, fratello di `.site-header__inner`); la testata è `position: sticky; z-index: 20` e quindi un contesto di impilamento: dentro di esso lo scrim posizionato a `z-index: 19` si dipinge **sopra** il contenuto non posizionato della testata (lock-up, voci, bottone «Menu»). Il confronto «19 < 20» mette a confronto due numeri di livelli diversi. **1024**, y 0: scrim 0–768 (`rgba(7,18,38,.5)`, blur 6), barra 0–33, testata 33–98, cassetto 98–768 (z 40); `elementFromPoint` al centro del **wordmark**, del **bottone «Menu»** e del primo **link lingua** = `div.nav-overlay`; differenza media di pixel chiuso → aperto (0–255): barra **104,0**, testata **113,9**, riquadro del wordmark **108,7**. y 200: testata 0–65, cassetto 65, scrim da 0, wordmark e «Menu» sotto lo scrim. **768**: identico (barra 104,1, testata 113,4, wordmark 108,7). **390**, y 0 e 200: testata 0–57, cassetto 57, scrim da 0; wordmark, «Menu» → `nav-overlay`; testata 112,1, wordmark 108,6. Secondo giro: 34 px della testata a 768–1279, **1 px** a 390; ora il 100 % della testata e della barra a 390, 768 e 1024, in cima e scrollato. Catture `a3_02_drawer_open_1024.png`, `a3_02_drawer_open_768.png`, `a3_02_drawer_open_390.png`, `a3_08_drawer_account_menu_1024.png` (wordmark e «Menu» sfocati sotto il velo). Criterio del secondo giro non soddisfatto in nessuna delle sue parti. |
| 3 | Prestazioni — verifica binaria 9 (con: «completo al primo frame» e l'elemento LCP) | **PARZIALE** | **Fatto e misurato**: server compresso (8772, gzip); misura prima/dopo nel README; **nessun font arabo** su `/fr/` (la voce «ع» e il suo nome nascosto sul carattere di sistema, `--f-arabic-sys`); **lead in Plex** (`IBM Plex Sans` normale); fotografia **precaricata** (`initiatorType: link`, parte a 367 / 242 ms); l'elemento LCP è ora **la fotografia della porta** (`image.doorway__img`, `doorway-800.webp`), come scrive il README — la riserva (a) del secondo giro è sciolta; lead, corpo e azioni a opacità 1 dal primo campione (sotto). **Non fatto**: LCP su 4G lento **2 960 / 3 088 ms** (> 2,5 s); il budget è ancora «proposto al CD» (README §4.9), non scritto in §68/DS; font **356,1 KB** contro i 200 del budget proposto (Newsreader tondo 128,9 per il lock-up, **Newsreader corsivo 143,4** ancora scaricato dalla home per la fascia forum V2 — il lead ha lasciato il corsivo, il file no); **22 fogli** co-caricati (V2 `shell/routes/voyage`, V3 `buttons/chip`, V4) senza data di riduzione; HTML 43,3 KB non compresso. Dettaglio in §5, riga 9. **Commento dell'hero**: vero per lead/corpo/azioni, **falso per il titolo** (difetto nuovo 7). |
| 3a | …di cui: «il testo dell'hero completo al primo frame» (criterio: nessun `data-reveal` nell'hero, lead/corpo/azioni a opacità 1 a ≈ 150 ms) | **CHIUSA sul criterio** — con il difetto nuovo 7 sul titolo | HTML servito: **0** `data-reveal` nella sezione hero (8770 e 8771; il secondo giro: 8 su 8771). Primo campione con il DOM pronto (8770: 348 ms, `readyState: interactive`; 8771: 396 ms): lead **1**, corpo **1**, azioni **1**, eyebrow 1, titolo 1 (`visibility: visible`); +150 ms (452 / 499 ms): idem; nessuna regola dei fogli caricati mette a opacità 0 una parte del testo dell'hero (scansione di `document.styleSheets`: 0). **Ma** il titolo, dipinto a riposo, viene poi nascosto dallo script e ri-rivelato: difetto 7. |
| 4 | Mobile — deroga e due bersagli | **PARZIALE** (bersagli **chiusi**; deroga **accettabile per `phase3`, non per l'interim**, e non scritta) | **Bersagli** (tocco emulato, `pointer: coarse` vero): barra istituzionale a **1024** e **768**: barra **44**, «Espace réservé» **128,4 × 44**, lista lingue **184 × 44**, quattro link **44 × 40** con `::before inset -2px` → `elementFromPoint` a 0 / ±21 / −22 px in verticale e ±21 in orizzontale dal centro = il link (a +22 si è sul bordo inferiore della barra) → area **44 × 44**; cassetto a **390**: «Espace réservé» 166,3 × 44, lista **350 × 44**, link 85,5 × 40 + area 44; a **1024** lista 944 × 44, link 234 × 40 + area 44. Con puntatore fine la barra resta 32 e i link 36 × 28 (ammesso nel secondo giro). Catture `a3_05_utility_touch_1024.png`, `a3_05_utility_touch_768.png`, `a3_05_drawer_touch_390.png`, `a3_05_drawer_touch_1024.png`. **Deroga** («≤ 130 % di 844 e le due azioni entro 844») misurata con un viewport mobile vero (390 CSS px, nessuna barra di scorrimento): **8771 `phase3`** hero **1 071,3 px = 126,9 %**, azioni 585,3–629,3 e 641,3–685,3 → **soddisfatta**; **8770 interim** hero **1 114,8 px = 132,1 %** (> 130 %), azioni 740,8–784,8 e **796,8–840,8** → la seconda azione sta nel primo schermo per **3,2 px**. Il README scrive «misurato 129 %, azioni a 757 e 813 px»: 757 / 813 sono i **bordi superiori** delle azioni misurati con 375 px di contenuto (viewport desktop con barra di scorrimento: lì l'hero misura 1 130,8 = **134,0 %**); il 129 % non corrisponde a nessuna delle due misure. Il secondo giro misurava l'interim a **128,8 %**: la crescita di ≈ 28 px è una riga di lead in più — causa probabile il lead passato dal corsivo serif a Plex, più largo (non isolata con una misura prima/dopo). La deroga non è scritta dal CD. Catture `a3_06_home_8770_390_mobile.png`, `a3_06_home_8771_390_mobile.png`. |
| 5 | Le vie alla soglia; la quarta riga della legenda | **Treccia CHIUSA** (con il difetto nuovo 8 sulle uscite); **legenda CHIUSA da 1280, PARZIALE a 1024** | **Treccia**: a 1440, 1280 e 1024 su 8770 e 8771 (`getPointAtLength`, 600 campioni per via): le vie entrano nel navy a x 365 a **y 372 / 378 / 384 / 390**, si incrociano a x 448 a **y 381**, escono a x 531 a y 390 / 384 / 378 / 372 (corsia i → 3 − i); arco interno navy `getBBox` x 365–531, **y 139–397**; chiave y 207–329. La treccia sta nella fascia 372–390, fra 7 e 25 unità sopra il piede del navy (397): la soglia, non più metà parete (secondo giro: 350–368). Il tracciato del server (`services._route_path`, 372) e quello di `home.js` (`braidY: 372`) coincidono (ricostruiti con la stessa formula: identici al `d` vivo). Il criterio («y ≈ 380–395 di scena, sopra i gradini») è soddisfatto. **Legenda**: **264 px** a 1440 e 1280 su entrambi i server e su `/ar/` a 1440; **quattro righe da 44**, ogni parola su una riga (altezza 20); a **1024** il pannello è **200 px** (regola di media) e la quarta riga è **56** («Universités & Formation» alta 40 = due righe) su 8770 e 8771 — il criterio del secondo giro citava 1440/1280/**1024**; su `/ar/` a 1024 quattro righe da 44 (parole più corte). A 390 (legenda 2 × 2) 44 / 44 / 44 / 56. Catture `a3_04_home_8770_1440.png`, `a3_04_home_8771_1440.png`, `a3_04_home_8770_1280.png`, `a3_04_home_8771_1280.png`. |
| 6 | Documentazione e decisioni | **PARZIALE** | **Chiusi**: `GATE_SCORECARD_TEMPLATE.md:83` cita ora `test_v4_tokens.py` e `test_design_docs.py` (entrambi esistono); la nota sull'elemento LCP (la fotografia) nel README è vera. **Non vero**: il commento di `_hero.html:22` («eyebrow, **title**, lead, body and actions carry no reveal and never start hidden») — il titolo è nascosto dallo script dopo il primo paint (difetto 7). **Aperti**: il nome dei link della legenda include ancora l'intero gloss (albero di accessibilità: «Personnes S'orienter vers une voie régulière et se préparer avant le départ.», **76 caratteri**, nessuna `description`: `aria-describedby` non adottato); le decisioni del committente/CD sulle lingue di lead e corpo su `/ar/` (8771: lead e corpo francesi con `lang="fr"`), sulla terza colonna del mega-menu (ancora due colonne 400/800, 0 immagini, 0 dischi), sulle sette voci, sulla deroga a 390, sul carattere del lock-up; e — nuova — la deviazione da CD §3.1 («lead corsivo bloccato») introdotta per risparmiare il corsivo di Newsreader, registrata nel README come «fatto», non firmata dal CD, e che sulla home **non risparmia nulla finché la fascia forum V2 scarica lo stesso file** (143,4 KB, misurato). `is-related` (nota 12 del primo giro): invariata. |

## 1. BEFORE / AFTER (§73)

| Vista | BEFORE | AFTER | Verdetto «materialmente superiore» (sì/no + una frase) |
|---|---|---|---|
| Desktop 1440 | `docs/qa/chrome/design-v4/before/01_home.png` (V2 interim); secondo giro `after/review2/r2_00_home_1440_rest.png` | `a3_04_home_8771_1440.png` (fase 3), `a3_04_home_8770_1440.png` (interim), `a3_12_focus_secondary_hero_1440.png` | **Sì.** La composizione del secondo giro (navy-mezzanotte con mesh, porta intera, legenda in vetro ancorata, titolo Newsreader 300, primario a gradiente) con la treccia ora alla soglia del navy, la legenda a 264 px con quattro righe da 44, il lead in Plex 20/28. Nella variante interim le tre vie che escono a destra **attraversano l'etichetta «MOBILITÉ RÉGULIÈRE»** (difetto 8, `a3_11_exits_8770_1440_zoom.png`). |
| Desktop 1280 · 1366 · 1439 | secondo giro `r2_01_header_1280.png` | `a3_08_header_8771_1280.png`, `a3_08_header_8771_1439.png`, `a3_04_home_8771_1280.png`, `a3_04_home_8770_1280.png` | **Sì.** Sette voci a 13,5 px e lock-up con **31,4 px** d'aria a 1280, 1366 e 1439 (nessuna sovrapposizione, ultima voce dentro il contenitore: 1156,5 ≤ 1220,5 a 1280; 1236 ≤ 1300 a 1439; `.nav-drawer` a 24 px dal lock-up, `overflow: visible`, 769/769); interim 356,3 px. Legenda 264 × 208 con righe da 44. |
| Tablet 768 | secondo giro `r2_05_home_768.png` | `a3_06_home_8771_768.png`, `a3_06_home_8770_768.png`, `a3_05_utility_touch_768.png` | **Sì.** Porta 220 px in testa, legenda a righe piene da 52, azioni in riga (8771: 878,8–922,8; 8770: 983,5–1 027,5 — sotto la piega di 1 024 di 3,5 px nella variante interim; misura con barra di scorrimento, 753 px di contenuto); con il tocco barra 44 e link lingua con area 44. |
| Mobile 390 | secondo giro `r2_05_home_390.png` | `a3_06_home_8771_390_mobile.png`, `a3_06_home_8770_390_mobile.png`, `a3_09_reduced_motion_390.png` | **Sì**, con la deroga da decidere: porta 180 → titolo → lead → **azioni** → corpo → legenda; toggle 92 × 44; `scrollWidth` 390. Hero 126,9 % (`phase3`) / **132,1 %** (interim). Sulla cattura a 375 px di contenuto (`a3_09_reduced_motion_390.png`) l'etichetta del primario va su **due righe** dentro il bottone da 44 (osservato, non misurato). |
| Stato interattivo (hover/focus/press/aperto) | secondo giro `r2_03_*`, `r2_07_*` | mega-menu `a3_08_megamenu_1440.png`, `a3_08_megamenu_click_1440.png`; menu account pubblico `a3_08_account_menu_public_1440.png`, `a3_08_account_menu_public_hover_1440.png`; focus `a3_08_focus_lang_1440.png`, `a3_08_drawer_focus_1024.png`, `a3_12_focus_secondary_hero_1440.png`; cassetto `a3_02_drawer_open_1024.png`, `a3_02_drawer_open_768.png`, `a3_02_drawer_open_390.png`, `a3_08_drawer_1024_8771.png`, `a3_08_drawer_account_menu_1024.png`, `a3_08_drawer_account_menu_390.png`; testata scrollata `a3_01_header_scrolled_400_1440.png` | **Sì** rispetto al BEFORE (V2: nessun cassetto V4, nessun Menu V4, nessun segmentato). Rispetto al secondo giro: la testata non oscilla più e il menu account è il Menu V4 anche sulla barra pubblica; **ma** a menu aperto lo scrim vela ora **l'intera** testata e la barra a ogni larghezza (correzione 2 regredita), e nel cassetto la lista del menu account si apre a **569 px** dal suo riassunto a 1024 (difetto 9). |
| RTL (ar) | secondo giro `r2_06_home_ar_1440.png`, `r2_06_home_ar_1024.png`, `r2_06_home_ar_390.png` | `a3_10_home_ar_8771_1440.png`, `a3_10_home_ar_8771_1024.png`, `a3_10_home_ar_8771_390.png`, `a3_10_home_ar_8770_1440.png`, `a3_10_home_ar_8770_390.png` | **Sì.** H1 a filo del bordo finale del blocco: inchiostro destro = bordo del blocco **1 332,5 = 1 332,5** (1440), **969 = 969** (1024), **355 = 355** (390), Δ 0, su 8771 (titolo latino `dir="ltr"`) e 8770 (titolo arabo); legenda 264 al bordo esterno del palcoscenico con quattro righe da 44 a 1440 (200 px e 44 × 4 a 1024); uscite in arabo su 8770. Lead e corpo francesi su 8771 (`lang="fr"`), corpo-frammento francese su 8770 allineato all'inizio (decisione del committente, come nel secondo giro). |
| Reduced-motion | secondo giro `r2_08_reduced_motion_*` | `a3_09_reduced_motion_1440.png`, `a3_09_reduced_motion_390.png` | **Sì.** `document.getAnimations().length` = **0** al caricamento e dopo 1,5 s (1440 e 390); righe del titolo `transform: none` (il difetto 7 non si presenta); nell'hero invisibili solo le quattro correnti (opacità 0, `animation: none`: ferme e nascoste per direzione §4.4) e la didascalia chiusa; a 390 anche il gruppo delle vie (`display: none`: la legenda sostituisce il diagramma, §4.5); `--motion-fast` 0 ms. |
| Forced-colors | secondo giro `r2_08_forced_colors_*` | `a3_09_forced_colors_1440.png`, `a3_09_forced_colors_legend_hover_1440.png` | **Sì.** Vie `CanvasText`, correnti `display: none`, legenda `Canvas` con bordo `CanvasText` e parole `LinkText`, bottoni con bordo 1 px, lingua corrente `outline 2px Highlight`, `filter: none` su porta e arco interno (nuovo, voluto), testata con bordo; didascalia in hover a opacità 1 con bordo e testo `CanvasText`. |

## 2. I ruoli (§71) — cinque firme, cinque punteggi indipendenti

Limite dichiarato: **un solo agente revisore** ha compilato le sei righe (la direttiva chiede cinque revisori
distinti); per ogni dimensione vale il punteggio più basso fra i ruoli che la giudicano.

| Ruolo | Cosa giudica in via primaria | Firma | Note |
|---|---|---|---|
| Creative Director | Premium Feel · Modernity · Originality · Visual Depth · coerenza con `CREATIVE_DIRECTION.md` | revisore indipendente, 25/09/2026, terzo giro | Treccia alla soglia e legenda a 264 come chiesto. Due correzioni hanno prodotto difetti visibili: la treccia abbassata fa passare tre vie **dentro** l'etichetta «MOBILITÉ RÉGULIÈRE» (componente firma, variante oggi in vigore); lo scrim «sotto la testata» la vela invece per intero. Deviazioni ancora aperte: lead non più corsivo (CD §3.1) senza firma del CD e senza il risparmio che la motivava; mega-menu a due colonne senza dischi né fotografia; lingua e accesso sulla barra istituzionale; sette voci CMS. |
| UX Lead | Clarity · Interaction Quality · Mobile · efficienza (§89) | revisore indipendente, 25/09/2026, terzo giro | Chiusi: oscillazione della testata, bersagli 44 al tocco su barra e cassetto, Menu V4 sulla barra pubblica. Contro: il bottone «Menu» (unico chiudi visibile) sotto il velo sfocato a menu aperto; il menu account del cassetto che si apre lontano dal suo riassunto; il toggle del sotto-menu ancora 24 px a 1280; l'interim a 390 oltre la deroga proposta. |
| Motion Lead | Motion · budget (§67) · pattern (DS §7) · reduced-motion | revisore indipendente, 25/09/2026, terzo giro | Il ciclo di layout della testata è sparito (0 commutazioni). Contro: il titolo si vede, **sparisce** sotto la maschera e rientra (difetto 7) — su 4G lento dopo 1,3–1,5 s di lettura; la testata transisce ancora `min-block-size` 64 → 56 (una proprietà di layout, ora senza ciclo). Reduced-motion completo; corrente in pausa fuori viewport (misurato). |
| Frontend Lead | token (DS): nessun valore arbitrario · CSP · nessun `style=""` · prestazioni (§68) | revisore indipendente, 25/09/2026, terzo giro | 0 letterali nei fogli V4 (test verde), CSP pulita, 0 `style=`, 0 script inline, nessun font arabo sulle pagine latine, fotografia precaricata, CSS 98,0 KB gzip. Contro: LCP 2,96–3,09 s su 4G lento; font 356 KB (lock-up 129 + corsivo della fascia V2 143); 22 fogli; budget non adottato; HTML non compresso. |
| Accessibility Reviewer | Accessibility · contrasto misurato · tastiera · screen reader · RTL · forced-colors | revisore indipendente, 25/09/2026, terzo giro | Bersagli 44 al tocco (2.5.8 e oltre); frecce ed Esc nel mega-menu; Esc nel cassetto con ritorno del focus; Menu V4 con Esc e ritorno del focus; H1 arabo a filo a tre larghezze. Contro: nome dei link della legenda con l'intero gloss (76 caratteri); due compagni dell'anello e, sul navy dell'hero, due colori d'anello (difetto 10); lead/corpo francesi su `/ar/`; `test_rtl_browser` non eseguito. |
| Red Team indipendente (§75–78) | i quattro test | revisore indipendente, 25/09/2026, terzo giro | Vedi §4: NO · NO · SÌ · NO. |

## 3. Le dieci dimensioni (§74) — scala 1–5 con ancore

**Critiche** (una sola ≤ 2 → **BLOCK**): Premium Feel · Modernity · Clarity · Institutional Credibility ·
Accessibility · Mobile. **Di sostegno** (≤ 2 → al massimo CONDITIONALLY_READY): Visual Depth · Motion ·
Originality · Interaction Quality. Fra parentesi il punteggio del secondo giro.

| # | Dimensione | Punteggio | Osservazione (cosa, dove, in Chrome) |
|---|---|---|---|
| 1 | **Premium Feel** (critica) | **3** (4) | Il secondo giro dava 4 con «1–2 dettagli da rifinire» (quarta riga della legenda a 56, scrim su 34 px della testata a 768–1279). La quarta riga è a 44 da 1280 e la testata non pompa più; ma i dettagli non allineati (§93) sono ora **quattro**, e due sono stati prodotti dalle correzioni: (a) a menu aperto lo scrim vela **l'intera** testata e la barra istituzionale a 390, 768 e 1024 — wordmark e bottone «Menu» sfocati e scuriti (differenza media 108,7 / 255 sul riquadro del wordmark; `a3_02_drawer_open_390.png`, `…_1024.png`); (b) nella variante interim tre vie attraversano l'etichetta «MOBILITÉ RÉGULIÈRE» (59 / 112 / 121 campioni dentro il suo riquadro; `a3_11_exits_8770_1440_zoom.png`); (c) nel cassetto il menu account si apre all'altro capo della riga (lista 744–984 con il riassunto a 40–175, `a3_08_drawer_account_menu_1024.png`); (d) il titolo che si vede, sparisce e rientra (difetto 7). Il materiale resta quello del DS (primario a gradiente, vetro L3, Menu V4 misurato: 240 × 171, `--min-3`, raggio 14, `--shadow-3`, padding 8 su quattro lati). È l'ancora 3: «superfici e controlli del sistema, ma dettagli non allineati». |
| 2 | **Modernity** (critica) | **4** (4) | Grammatica 2026 coerente, e ora anche lo stato della barra fra 25 e 32 px lo è (0 commutazioni): barra 32 + testata 64 → 57 in vetro, indicatore che trasla, mega-menu a tutta larghezza dal bordo della barra (0–1425, y 97, raggio `0 0 20 20`, `--shadow-3`), segmentato in barra e cassetto, Menu V4 dell'account sulla barra pubblica e nel cassetto, cassetto con scrim + blur 6. Non 5: mega-menu ancora elenco a chevron su due colonne (400/800), nessuna transizione di pagina. |
| 3 | **Visual Depth** | **4** (4) | Ogni superficie al suo livello a riposo e in hover: legenda e didascalia L3 in vetro, mega-menu e Menu L3 con `--shadow-3` a due strati, testata scrollata L3, hero IMMERSIVE con mesh e grana, `--drop-door` sulla porta. Al limite del 4: a menu aperto l'ordine dei livelli è sbagliato — lo scrim (L4) si dipinge **sopra** la testata che dovrebbe restargli sopra. Non 5: la luce (mesh) resta sotto la soglia di percezione. |
| 4 | **Motion** | **3** (3) | Chiuso il ciclo di layout della testata (0 commutazioni a 25–60 px, `overflow-anchor: none`). Tiene il 3: (a) **il titolo lampeggia** — dipinto a riposo, poi `home.js:66–71` lo porta a `translateY(110%)` sotto la maschera e lo rianima: misurato a ogni frame, 8770 a riposo per 5 frame da 204 ms, a **308 ms** traslato di 118,25 px (invisibile), ≥ 40 px sotto la maschera per 17 frame (308–478 ms), assestato ≈ 0,8 s; 8771 a riposo da 218 ms, 80,1 px a 337 ms, 15 frame nascosto; su **4G lento + CPU ×4** (8772) il titolo è **leggibile dal FCP (1 760 / 1 672 ms) per 44 / 39 frame**, poi **scompare** a 3 271 / 3 054 ms e rientra (ultimo frame nascosto 3 432 / 3 183 ms). È il contrario del pattern HIERARCHY di CD §3.1 («si rivela riga per riga») e del commento dell'hero. (b) La testata transisce ancora `min-block-size` (layout, ora senza ciclo): l'ancora 4 chiede 0 layout. Reduced-motion completo (0 animazioni); corrente 28 s a opacità .55, **in pausa** fuori viewport (`animationPlayState` `running` a y 0, `paused` a y 1 800, di nuovo `running` a y 0). |
| 5 | **Clarity** (critica) | **4** (4) | Un H1, lead Plex 20/28, corpo 17/28, **una** primaria + una secondaria, la legenda con glifo, disco, parola e gloss in didascalia, ogni riga un link alla landing; a 390 le azioni prima del corpo. Non 5: l'etichetta «MOBILITÉ RÉGULIÈRE» barrata dalle vie si legge male (grafica `aria-hidden`, ma è l'etichetta visiva della terza uscita); su `/ar/` (8771) il lettore arabo vede titolo inglese, lead e corpo francesi (decisione pendente). |
| 6 | **Institutional Credibility** (critica) | **4** (4) | Lock-up intatto a riposo a ogni larghezza da 1280 (31,4 px d'aria), barra del promotore, porta del committente, nessun dato finto, testi bloccati invariati (diff dei template: solo `data-reveal` tolti e un commento), H1 arabo a filo. Al limite del 4: a menu aperto il marchio **e** la riga del promotore sono sotto un velo sfocato su telefono e tablet — non è ciò che un'istituzione mostra del proprio marchio (il secondo giro lo scriveva per 34 px a 768–1279; ora vale per il 100 % a ogni larghezza). |
| 7 | **Originality** | **4** (4) | Senza logo si riconosce ILE: carta minerale + navy del marchio, Newsreader 300 + Plex, la porta con chiave e gradini, le quattro vie ancorate alla legenda che ora si intrecciano alla soglia del navy, il segmentato con «ع». Non 5: il componente firma è eseguito con un difetto proprio (uscita 3 barrata) e il mega-menu non ha la sua firma (dischi, fotografia). |
| 8 | **Interaction Quality** | **3** (3) | Chiusi e misurati: testata stabile; mega-menu con **ArrowDown** sulla voce che apre e mette a fuoco il primo link («Votre parcours»), **ArrowDown/ArrowUp** nel pannello (→ Diplômes et titres → Formation → Vivre en Italie → Attention aux fraudes; ↑ Vivre en Italie), **ArrowRight** che chiude e passa a «Entreprises», **ArrowDown** che apre il suo pannello («Besoins professionnels»), **Esc** che chiude e restituisce il focus al toggle; click sul chevron apre e chiude; Menu V4 pubblico con hover (`--surface-hover`, voce a 9 px dal bordo della lista), Esc e ritorno del focus al riassunto; cassetto con Esc e ritorno del focus a `.nav-toggle`; bersagli 44 al tocco. **Non allineati (§93)**, e per questo 3: (a) a menu aperto il bottone «Menu» — l'unico chiudi visibile — è sotto lo scrim (`elementFromPoint` = `nav-overlay`: il clic chiude perché colpisce lo scrim, ma hover/press/focus del bottone non si vedono che attraverso il velo); (b) nel cassetto la lista del menu account si apre a 569 px dal suo riassunto a 1024 e sovrapposta al riassunto a 390 (difetto 9); (c) il toggle del sotto-menu è ancora **24 × 44** a 1280 (28 × 44 a 1440; il secondo giro lo segnalava fra 80 e 90 rem); (d) compagni dell'anello diversi fra controlli vicini (difetto 10). |
| 9 | **Mobile** (critica) | **3** (3) | Il secondo giro diceva: «con la deroga e i due bersagli a 44 la dimensione vale 4». I bersagli sono a 44 (misurati al tocco, sopra). La deroga **non è scritta** dal CD e, misurata, **tiene per `phase3`** (126,9 %, azioni finite a 685) ma **non per l'interim** — la variante in vigore finché la fase 3 è chiusa: **132,1 %**, seconda azione finita a 840,8 su 844 (3,2 px di margine), e l'interim è cresciuto dal 128,8 % del secondo giro (una riga di lead in più). A 768 la riga delle azioni dell'interim finisce a 1 027,5, sotto la piega di 1 024 (viewport con barra di scorrimento, 753 px di contenuto). Tutto il resto dell'ancora 4 è raggiunto: composizione propria, bottoni 44 a tutta larghezza, toggle 92 × 44, righe della legenda ≥ 44, nessuno scroll orizzontale (390 = 390). Resta 3 finché la deroga non è scritta con una soglia che l'interim rispetta (o l'interim non torna sotto il 130 %). |
| 10 | **Accessibility** (critica) | **4** (4) | Bersagli 44 al tocco sulla barra e nel cassetto (2.5.8 con margine); tastiera completa nel mega-menu, nel Menu e nel cassetto (sopra); `scroll-padding` e contrasti del secondo giro invariati sulle superfici non cambiate (parola della legenda ≥ 6,18 sul pixel più chiaro del vetro; didascalia ≥ 7,06; nav 6,46; segmentato 6,00); lead `#eef1f6` Plex 20 su `#0b1a33` **15,3 : 1** (token); anello sui bottoni dell'hero `#1d8a93` su `#0b1a33` **4,22 : 1** (token, ≥ 3) con la banda carta da 2 px; H1 arabo a filo a tre larghezze; colori forzati e reduced-motion completi. Non 5: il nome di ogni link della legenda include il gloss (76 caratteri su «Personnes», nessun `aria-describedby`); due compagni e due colori d'anello (difetto 10); lead/corpo francesi su `/ar/` (con `lang`); la tastiera con il cassetto aperto sul bottone velato non misurata (§7); `test_rtl_browser` non eseguito. |

## 4. I quattro test (§75–78) — Red Team indipendente

| Test | Domanda | Risposta richiesta | Risposta | Perché, esattamente (elemento, cattura) |
|---|---|---|---|---|
| Generic AI | «Potrebbe essere scambiato per un template generico Claude/AI?» | **NO** | **NO** | Nessuna tessera-con-icona, nessun Inter/zinc/viola: carta minerale e navy del marchio, Newsreader 300 maiuscolo + IBM Plex, la porta con chiave e gradini attraversata da quattro vie ancorate a una legenda in vetro, il segmentato con «ع», il lock-up ufficiale (`a3_04_home_8771_1440.png`, `a3_04_home_8770_1440.png`). Il punto fragile resta il pannello del mega-menu (`a3_08_megamenu_1440.png`: bianco, due colonne a chevron), che dentro la testata con lock-up e segmentato non basta a farlo generico. |
| Editorial | «Sembra ancora principalmente una pubblicazione editoriale/legale?» | **NO** | **NO** | Sulla superficie del gate il serif è solo nell'H1 (e ora **non** più nel lead, Plex 20/28); corpo, legenda, didascalia, nav, Menu in Plex; CTA a gradiente. Avvertenza dei giri precedenti ancora valida: sotto l'hero riprende la pagina V2 (e la fascia forum V2 scarica il corsivo di Newsreader). Nella variante interim il titolo editoriale a cinque righe pesa, ma su un fondo IMMERSIVE con CTA e porta. |
| 2026 | «Nascosto il logo, competerebbe con prodotti digitali premium del 2026?» | **SÌ** | **SÌ** | L'esecuzione degli stati e della profondità regge (CD §6.3): testata in vetro stabile, indicatore a molla, mega-menu con frecce complete, Menu V4 con ombra a due strati, legenda con didascalia senza salti, reduced-motion completo, corrente in pausa fuori viewport. Ciò che un prodotto premium del 2026 **non** spedisce, ed è la lista di §6: il velo del cassetto sopra la testata a ogni larghezza (2), il titolo che si vede e sparisce (7), l'etichetta d'uscita barrata dalle vie (8), il menu account del cassetto che si apre lontano dal riassunto (9). |
| Too much | «Abbiamo aggiunto effetti inutili solo per sembrare moderni?» | **NO** (altrimenti: elenco di cosa togliere, nell'ordine di `CREATIVE_DIRECTION.md` §6.4) | **NO** | Nessun effetto nuovo; il terzo giro ha **tolto** il reveal di lead/corpo/azioni. La corrente resta sottile (.55, 28 s, in pausa fuori viewport, assente con reduced-motion). La rivelazione del titolo ha una funzione per direzione (HIERARCHY), ma nella forma misurata (dopo il primo paint) è un difetto di esecuzione (7), non un effetto da togliere per §6.4. |

## 5. Verifiche binarie (tutte devono essere «sì»)

| Verifica | Sì/No | Prova |
|---|---|---|
| Nessuna formulazione vietata (`apps/cms/forbidden.py`), nessun testo bloccato alterato | **Sì** | Diff d99f2bb → dd29168 su `templates/pages/home/_hero.html`: tolti tre `data-reveal` e riscritto il commento; `apps/pages/services.py`: la sola quota della treccia; nessun testo toccato. Test di compliance e della home eseguiti nella corsia del revisore (nota A). |
| Nessun `style=""`, nessuno script inline, nessun hotlink (CSP) | **Sì** | HTML servito di `/fr/` (8770 e 8771): **0** attributi ` style=`, **6** `<script>` di cui **0** inline (tutti con `src` o `application/ld+json`); intestazione `Content-Security-Policy` con `script-src 'self'`, `style-src 'self'`, `font-src 'self'`, `img-src 'self' data:` su entrambi; listener `securitypolicyviolation` installato prima del caricamento su 8772 (due passate 4G): **0** violazioni. |
| Nessun valore fuori dai token (colori, raggi, ombre, durate, curve) | **Sì** | `test_the_v4_component_sheets_carry_no_literal_colour` verde (nota A); la sola occorrenza di un letterale nei tre fogli V4 del gate è `#e8e8e7` **dentro un commento** (`v4/shell.css:132`). Token nuovi del giro (`--f-arabic-sys`, `--hit-min` già presente, `--scrim`, `--blur-scrim`) in `v4/tokens.css`. |
| «Nessun colore significa mai approvato»: nessun chip `conforme` con croma, nessun verde di verdetto | **Sì** | Nessun chip nelle superfici del gate; l'unico verde è quello del marchio nel lock-up. |
| Nessun dato, contatore, avatar, grafico o KPI finto | **Sì** | Nessun numero nell'hero e nella testata; le vie sono le `entrances()` reali (link alle landing); le uscite sono le tre parole dell'eyebrow bloccata; il menu account mostra `qa-person` (utente reale del database di QA). |
| Coordinate, «svg», «Suspendre le mouvement», etichette di debug: assenti | **Sì** | HTML servito (8770 e 8771): **0** «Suspendre», **0** «svg» in nodi di testo, **0** coordinate; su 8770 i soli `<text>` dell'SVG sono le tre etichette d'uscita (`aria-hidden` con l'intero SVG). |
| Reduced-motion: pagina completa, nulla a opacità 0 | **Sì** | §1, riga Reduced-motion: 0 animazioni, righe del titolo `none`, invisibili solo le correnti (per direzione) e la didascalia chiusa. |
| Contrasto sul peggior fondo (incluso sotto il vetro) ≥ 4,5 testo / ≥ 3 UI | **Sì** | Superfici non cambiate: le misure sui pixel del secondo giro (minimo testo 6,18 sulla parola della legenda sotto il vetro; didascalia ≥ 7,06; nav 6,46; segmentato 6,00; primario 9,94). Cambiate: lead 15,3 : 1 (token, stesso colore, altra famiglia); pannello della legenda più largo, stesso vetro; anello dei bottoni dell'hero 4,22 : 1 sul navy (UI ≥ 3). Le vie sulla pietra non ri-misurate dopo lo spostamento della treccia (§7). |
| Prestazioni: JS/CSS ≤ budget, LCP < 2,5 s, CLS < 0,1, INP < 200 ms (4G simulato) | **No** | **8772** (gzip), 1440 × 900, cache spenta, 4G lento + CPU ×4, due passate. **Passata 1**: LCP **2 960 ms** — `image.doorway__img` (`doorway-800.webp`, 133 126 px²; candidati precedenti: `P.utility-bar__identity` 1 760, la riga del titolo 1 904); FCP 1 760; DCL 3 194; load 3 669; CLS **0,0037** (0,0005 a 1 873, 0,003 a 2 080, 0,0002 a 2 537); 11 long task (max 186 ms); fotografia `link` da 367 a 2 910 ms. **Passata 2**: LCP **3 088 ms** (stesso elemento); FCP 1 672; DCL 3 000; load 3 500; CLS **0,0224** (0,0193 a 1 812); 10 long task (max 199); fotografia 242 → 3 058. **Pesi** (identici nelle due): CSS **22 fogli, 98,0 KB gzip** (385,2 KB nudi); JS **8 file, 35,6 KB** gzip (99,4); font **6 file, 356,1 KB** (Plex Sans 400/500/600 22,1 + 23,6 + 23,7; Newsreader tondo **128,9**; Newsreader **corsivo 143,4**, finito a 3 430 / 3 479 ms; Plex Mono 14,4); **nessun font arabo**; immagini 5 file 79,5 KB (foto 76,8); HTML **43,3 KB non compresso**; **42 richieste**. Senza limiti: LCP 364 ms (la foto), CLS 0,0002. **INP-proxy** (CPU ×4, 8772: hover su una riga della legenda, click sul chevron, Esc, hover sul secondario): durata massima di evento **72 ms**. Confronto: secondo giro (server senza compressione) LCP 3 776 ms su `.antifraud-panel__body`, CSS 318 KB nudi / 20 fogli, font 487 KB / 8 (Plex Arabic 45), CLS 0,0057, INP-proxy 120 ms; README (§4.9) «home 3,1 s, font 358 KB» — coerente con questa misura. **Contro il budget proposto nel README** (per pagina con gzip): CSS ≤ 100 ✓ (98,0: 2 KB di margine), JS ≤ 45 ✓ (35,6), font ≤ 200 **✗** (356,1), LCP < 2,5 s **✗** (2,96–3,09), CLS < 0,1 ✓. Il budget non è scritto in §68/DS. |
| RTL (ar) a tre larghezze senza proprietà fisiche nel CSS nuovo | **Sì** | `grep` di `left/right/margin-left/…/text-align: left|right/float` su `static/css/v4/*.css`: nessuna; H1 a filo a 1440 / 1024 / 390 (Δ 0), legenda specchiata, uscite in arabo (8770); `tests/i18n/test_rtl_static.py` verde (nota A); `tests/i18n/test_rtl_browser.py` **non eseguito** (pilota Chrome). |
| Demo page dei componenti coerente (§94) | **Sì, parziale** | `/_design/` (8770, `a3_13_showcase_navigation_1440.png`): sezione «Navigation» con il segmentato, il pannello del mega-menu, l'indicatore e il Menu account; **0** id duplicati; **assenti** la legenda in vetro, la didascalia e la porta (come nel secondo giro). `tests/frontend/test_design_showcase.py` verde (nota A). |

**Nota A — esito dei test**, database dedicato `ile_lane4`:
1. `tests/frontend apps/pages/tests/test_templates_static.py tests/i18n/test_catalogues.py -q -x` — **496 passed, 1 xfailed
   in 339,81 s**, exit 0 (l'xfail è `tests/frontend/test_legacy_token_shim.py::test_the_shim_is_gone`, un test di debito
   dichiarato: passa solo a migrazione finita). Comprende `test_v4_tokens.py` (letterali), `test_design_docs.py`,
   `test_design_showcase.py`, `test_frontend_bundle_is_current.py`.
2. `tests/compliance/test_locked_content.py tests/compliance/test_public_pages.py tests/compliance/test_phase3_texts_not_leaked.py
   apps/pages/tests/test_home.py tests/i18n/test_rtl_static.py -q` — **120 passed in 345,47 s**, exit 0.
3. Il tentativo interrotto ha lasciato `review_a3/pytest_a3.txt` (fuori dal repository): **416 passed in 453,22 s, exit 0**
   sullo stesso albero; il file non registra il comando, quindi è citato come riferimento e non come prova.
Il run 1 comprende i test marcati `browser` di `tests/frontend` (`test_browser.py`, `test_header_fits_the_narrowest_viewport.py`:
12 test raccolti, verdi): lanciano un Chromium **headless proprio** con Playwright, non la scheda visibile. Non eseguito, e
detto: `tests/i18n/test_rtl_browser.py` (fuori dall'insieme richiesto).

## 6. Esito

| Esito | Condizione |
|---|---|
| **PASS** | tutte le critiche ≥ 4, tutte le dimensioni di sostegno ≥ 3, quattro test corretti, tutte le verifiche «sì», AFTER materialmente superiore su ogni vista |
| **CONDITIONALLY_READY** | tutte le critiche ≥ 3 e nessuna ≤ 2, al massimo due dimensioni di sostegno ≤ 2, quattro test corretti, verifiche «sì»; correzioni elencate con scadenza; **nessuna propagazione** finché non diventa PASS |
| **BLOCK** | una dimensione critica ≤ 2, **oppure** un test sbagliato, **oppure** una verifica «no», **oppure** AFTER non materialmente superiore |

Esito del gate: ☐ PASS ☐ CONDITIONALLY_READY ☒ **BLOCK**

Motivazione, nell'ordine delle regole: nessuna dimensione critica ≤ 2 (Premium Feel **3**, Modernity 4, Clarity 4,
Credibility 4, Mobile 3, Accessibility 4), nessuna di sostegno ≤ 2 (Visual Depth 4, Motion 3, Originality 4, Interaction
Quality 3), i quattro test corretti, l'AFTER materialmente superiore al BEFORE su ogni vista. Sulle dimensioni e sui
test il gate sarebbe **CONDITIONALLY_READY** — non PASS: Premium Feel e Mobile sono a 3. Lo tiene a **BLOCK** **una sola**
verifica binaria, come nel secondo giro: le prestazioni (§5, riga 9) — ora misurate onestamente sul server compresso,
con l'elemento LCP giusto, e **sopra** il tetto (2,96–3,09 s) con un budget che resta una proposta.

Il revisore dice anche, con la stessa chiarezza, che questo giro **non** avvicina il gate al PASS sulle dimensioni:
Premium Feel scende da 4 a 3 perché due correzioni del secondo giro hanno prodotto difetti visibili (lo scrim che
doveva stare sotto la testata la vela per intero, ora anche a 390; la treccia abbassata che barra l'etichetta della
terza uscita), e il commento «completo al primo frame» è diventato più falso per il titolo di quanto fosse prima.
Delle sei correzioni del secondo giro: **chiusa** 1; **chiusa sul criterio** 3a (con il difetto nuovo 7); **treccia
chiusa** e **legenda chiusa da 1280** in 5 (parziale a 1024; difetto nuovo 8); **parziali** 3 (prestazioni), 4 (bersagli
chiusi, deroga no), 6 (documentazione); **aperta e regredita** 2.

Correzioni richieste (numerate: prima le correzioni ancora aperte del secondo giro con il loro numero, poi i difetti
nuovi da 7; ognuna con dimensione, elemento, cattura, criterio di chiusura):

2. **Scrim del cassetto sopra la testata — ora a ogni larghezza.** Dimensioni: Premium Feel (critica), Interaction Quality,
   Institutional Credibility, Visual Depth. Elemento: `static/css/v4/shell.css:495–503` (`.nav-overlay { inset-block-start: 0;
   z-index: calc(var(--z-header) - 1) }`) con `.nav-overlay` **figlio** di `header.site-header` (`position: sticky; z-index: 20`
   → contesto di impilamento: il 19 si confronta con il contenuto della testata, non con la testata). Misura: §0-bis riga 2
   (scrim da 0 a 390/768/1024, y 0 e 200; `elementFromPoint` su wordmark, «Menu» e link lingua = `nav-overlay`; wordmark
   108,7 / 255 di differenza media). Catture `a3_02_drawer_open_390.png`, `a3_02_drawer_open_768.png`, `a3_02_drawer_open_1024.png`.
   Criterio: a 390, 768 e 1024, con `scrollY` 0 e 200, a menu aperto `elementFromPoint` al centro del wordmark, del bottone
   «Menu» e (dove visibile) del primo link lingua restituisce l'elemento stesso; differenza media di pixel chiuso → aperto sul
   riquadro del wordmark < 2; il bordo superiore dello scrim coincide con il piede reale della testata (±1 px) **oppure** lo
   scrim sta sotto la testata nell'ordine di pittura (scrim fuori dalla testata, fratello nel `body`, con `z-index` minore;
   o contenuto della testata posizionato sopra di esso). Misurare pixel e punto, non i numeri di `z-index`.
3. **Prestazioni — verifica binaria 9.** Dimensione: Frontend Lead. Misura: §5 riga 9. Criterio: su 8772, 4G lento + CPU ×4,
   due passate, **LCP < 2,5 s** (la fotografia della porta), CLS < 0,1, INP-proxy < 200 ms; il budget **scritto** in §68/DS
   (non «proposto») e rispettato o con deroga firmata; i font della home entro il budget o una decisione scritta su lock-up
   (Newsreader tondo 128,9 KB) e corsivo (143,4 KB, scaricato dalla fascia forum V2); la riduzione dei 22 fogli (o la
   concatenazione per la produzione) con una data; HTML: decisione scritta (BREACH) registrata nel gate.
4. **Mobile — la deroga.** Dimensione: Mobile (critica). Elemento: `.hero` a 390 nella variante interim (8770): **1 114,8 px =
   132,1 %**, seconda azione finita a 840,8 (3,2 px di margine), era 128,8 %; `phase3` 126,9 % con azioni a 685. Catture
   `a3_06_home_8770_390_mobile.png`, `a3_06_home_8771_390_mobile.png`. Criterio: deroga **scritta dal CD** con una soglia che
   entrambe le varianti rispettano, misurata con un viewport mobile vero (390 CSS px, nessuna barra di scorrimento), e le due
   azioni entro 844 con almeno 16 px di margine; oppure l'interim ≤ 130 % (il lead in Plex ha aggiunto una riga: verificare).
   A 768 la riga delle azioni dell'interim (983,5–1 027,5) entro la piega di 1 024.
5. **La legenda a 1024.** Dimensioni: Premium Feel, Mobile. Elemento: `.doorway-legend` a 64–80 rem (**200 px**): quarta riga
   **56** («Universités & Formation» su due righe) su 8770 e 8771 (e 56 a 390). Criterio: quattro righe da 44 a 1024 (il
   criterio del secondo giro elencava 1024), o una decisione scritta che la regola delle righe da 44 vale da 1280 e che sotto
   la quarta riga va a capo.
6. **Documentazione e decisioni** (nessun codice, o poco): il commento di `_hero.html:22` vero per il titolo (vedi 7); il nome
   dei link della legenda (76 caratteri con il gloss: `aria-describedby` sul gloss e nome = parola); la deviazione «lead non più
   corsivo» (CD §3.1) firmata dal CD, con la nota che il risparmio sulla home si realizza solo quando la fascia forum V2 smette
   di scaricare il corsivo; le decisioni pendenti del committente/CD (lingue di lead e corpo su `/ar/`, terza colonna del
   mega-menu, sette voci, deroga a 390, carattere del lock-up). Residuo del secondo giro: il toggle del sotto-menu **24 × 44** a
   1280 (28 × 44 a 1440).
7. **Il titolo si vede, sparisce e rientra.** Dimensioni: Motion, Premium Feel. Elementi: `static/js/src/home.js:66–71`
   (`animate(lines, { transform: ["translateY(110%)", "translateY(0)"] }, { delay: stagger(0.06, { startDelay: 0.1 }) })`
   applicato **dopo** il primo paint alle `.hero__title .line > span`, dentro `.line { overflow: hidden }`); commento di
   `templates/pages/home/_hero.html:22` («…title… never start hidden»). Misura: a ogni frame — 8770 a riposo 5 frame da 204 ms,
   traslato di 118,25 px (invisibile) a 308 ms, ≥ 40 px sotto la maschera per 17 frame; 8771 a riposo da 218 ms, 80,1 px a
   337 ms; su 4G lento leggibile dal FCP (1 760 / 1 672 ms) per 44 / 39 frame e **nascosto** da 3 271 / 3 054 a 3 432 / 3 183 ms.
   Criterio: **0 frame** in cui una riga del titolo passa da visibile (`transform: none`) a nascosta; o il titolo resta fermo
   (reveal tolto, deviazione da CD §3.1 scritta), o lo stato iniziale della rivelazione è applicato **prima** del primo paint
   (senza peggiorare l'LCP misurato su 8772); commento vero; reduced-motion invariato.
8. **L'etichetta «MOBILITÉ RÉGULIÈRE» barrata dalle vie.** Dimensioni: Originality, Premium Feel, Clarity. Elementi:
   `static/js/src/home.js:34` (`braidY: 372`) e `apps/pages/services.py` (`_route_path`, 372) contro `.exit__label` della terza
   uscita (`getBBox` x 503,4–636, y 377,1–393,2, ancorata a `end`). Misura (1440 e 1280, 800 campioni per via): dentro il
   riquadro dell'etichetta cadono **59 / 112 / 121** campioni delle vie person / company / institution (1280: 58 / 115 / 124);
   con la treccia del secondo giro (350), ricalcolata a runtime con la stessa formula, **0 / 42 / 38** — la correzione 5 ha
   triplicato l'incrocio. «FORMATION» è attraversata dalla via person (19–20 campioni, invariato). Catture
   `a3_11_exits_8770_1440_zoom.png`, `a3_11_exits_8770_1280_zoom.png`. Criterio: **0** campioni di via dentro il riquadro di
   ogni etichetta d'uscita (±1 unità) a 1280 e 1440, in LTR e in RTL (`/ar/` su 8770: «التنقل النظامي» accanto alle vie, non
   misurata), senza riportare la treccia a metà parete (etichette sopra il nodo, o un alone scuro dietro il testo, o le vie
   che salgono prima di x 503).
9. **Il menu account del cassetto si apre lontano dal suo riassunto.** Dimensioni: Interaction Quality, Premium Feel.
   Elemento: `.drawer-utility .account-menu` (un `<details>` largo quanto la riga del cassetto: **944 px** a 1024, 350 a 390)
   con la lista allineata al bordo finale. Misura (8771, `qa-person`): 1024 → riassunto 135 × 44 a x 40–175, lista 240 × 171 a
   **x 744–984** (569 px più in là, sopra la «ع» del segmentato e le prime voci); 390 → lista a x 130–370, sovrapposta alla fine
   del riassunto (20–155). Catture `a3_08_drawer_account_menu_1024.png`, `a3_08_drawer_account_menu_390.png`. Criterio: la
   lista allineata al bordo iniziale del riassunto (±1 px) nel cassetto a 390, 768 e 1024, e al bordo finale in RTL; il
   `<details>` largo quanto il suo riassunto.
10. **Un anello, due compagni — e sul navy dell'hero due colori d'anello.** Dimensioni: Accessibility, Interaction Quality.
    Misura (focus emulato, `:focus-visible` vero): `.utility-bar__link`, `.main-nav__link`, `.brand--lockup`, `.main-nav__toggle`,
    `.main-nav__sublink`, il riassunto del Menu, le voci del cassetto → `outline 2px #1d8a93` + **`0 0 0 5px rgba(29,138,147,.3)`**
    (`static/css/v2/shell.css:480–483`, `:focus-visible` globale V2, e `:74–77`); i link lingua (barra e cassetto, correnti e
    no) e i bottoni → `outline 2px #1d8a93` + **`0 0 0 2px #f4f3f0`** (`base.css:384`, `v4/shell.css:424`, `v4/buttons.css:169`);
    nell'hero `.doorway-legend__row` → `outline 2px #7fd1d8` + `0 0 0 5px rgba(127,209,216,.3)` (`v2/shell.css:485`) mentre
    primario e secondario sullo stesso navy prendono l'anello chiaro `#1d8a93` (4,22 : 1) con la banda carta
    (`a3_12_focus_secondary_hero_1440.png`). Il README (gate B, 18; gate D, 9) dichiara «un solo anello con un solo compagno».
    Criterio: su testata, barra, cassetto e hero un solo compagno (misurato sugli elementi elencati), e su ogni superficie scura
    l'anello scuro per ogni controllo (bottoni compresi).

Note, non correzioni: la barra scrollata (57 px) e lo `scroll-padding` del secondo giro invariati; «Voir l'espace» (colonna
sinistra del pannello) non è nel giro delle frecce, che parte da «Votre parcours» — raggiungibile con Tab, non misurato;
`is-related` invariata; la scheda è stata lasciata autenticata come `qa-person` su 8771.

Firma del Creative Director (esito finale, §6 della direttiva): ______ · data/ora: ______

## 7. Ciò che non è stato possibile verificare, e perché (§95)

- **Contrasti sui pixel**: non ri-misurati; le superfici con testo non hanno cambiato colore né fondo (lead: stessa tinta,
  altra famiglia; legenda: stesso vetro, più larga). I valori nuovi sono calcolati sui token.
- **Le vie sulla pietra dopo lo spostamento della treccia**: l'avvicinamento (x 300–365) scende di 22 unità rispetto al
  secondo giro e passa su un'altra parte della fotografia; il contrasto contro il casing non è stato ri-campionato.
- **Il bottone «Menu» velato con il cassetto aperto, da tastiera** (2.4.11): non misurato; misurato solo che il punto del
  bottone restituisce lo scrim e che Esc chiude e restituisce il focus.
- **L'etichetta araba della terza uscita** (`/ar/` su 8770) vicina alle vie: visibile in `a3_10_home_ar_8770_1440.png`, non
  campionata.
- **INP reale**: misurato un proxy (durata massima degli eventi sotto CPU ×4, 72 ms), non un'interazione di campo.
- **La causa della crescita dell'interim a 390** (128,8 → 132,1 %): attribuita al lead in Plex per l'altezza (≈ 28 px = una
  riga del lead), non isolata con una misura prima/dopo sullo stesso albero.
- **`test_rtl_browser`**: non eseguito (fuori dall'insieme; pilota un browser). `test_browser` e `test_header_fits_the_narrowest_viewport` sono verdi nel run 1 (Chromium headless proprio).
- **Il comando del run da 416 test** del tentativo interrotto: non registrato nel file.
- **Cinque revisori distinti** (§71): un solo agente ha compilato le sei righe.

## 8. Metodo e limiti

- Osservazione: Chrome visibile via `scripts/cdp.py` (`Page.attach(url_contains="127.0.0.1:")`), una sola scheda
  (`Page.bringToFront`, `visibilityState: visible`, 63 rAF in 500 ms verificati all'inizio), sonde sequenziali; viewport
  emulati 1440 × 900, 1439 / 1366 / 1280 × 800, 1024 × 768, 768 × 1024, 390 × 844 (anche con `mobile: true` e tocco);
  emulazioni sempre azzerate a fine sonda (viewport, tocco, media, rete, CPU, focus).
- Misure: vedi la testata del documento; in più la storia per frame del titolo (`requestAnimationFrame`, installata prima del
  caricamento), la geometria delle vie per campionamento (`getPointAtLength`) contro `getBBox` delle etichette, la stessa
  formula della treccia ricalcolata a runtime in un SVG temporaneo (rimosso) per il confronto 350 / 372, le differenze di
  pixel chiuso → aperto per lo scrim, l'albero di accessibilità (`Accessibility.getPartialAXTree`) per il nome dei link della
  legenda, `md5` dei fogli serviti da 8772 contro quelli dell'albero.
- Script del revisore: `C:\Users\<user>\AppData\Local\Temp\claude\C--tmp-italylegalentry\review_a3\` (`q0_window.py`,
  `q1_oscillation.py`, `q2_scrim.py`, `q2c_stacking.py`, `q3_first_frame.py`, `q3b_frames.py`, `q4_braid_legend.py`,
  `q5_touch_lang.py`, `q6_mobile.py`, `q6b_mobile_true.py`, `q7_perf.py`, `q8_header_menu.py`, `q8b_mega.py`, `q9_media.py`,
  `q10_arabic.py`, `q11_session.py`, `q12_account.py`, `q13_inp.py`, `q14_misc.py`, `q15_drawer_braid.py`,
  `q15b_drawer_account.py`, `q16_showcase.py`, `q17_final.py`); esiti dei test `pytest_a3_fast.txt`, `pytest_a3_compliance.txt`.
- Sessioni: la scheda è stata trovata autenticata su 8771; ogni visita a 8770 / 8772 la disconnette (cookie per host); è
  stata ri-autenticata tre volte con `scripts/qa_chrome_signin.py qa-person@example.test /fr/espace-reserve/` (sessione
  coniata lato server, nessuna credenziale digitata) e lasciata autenticata.
- Nessun file del repository modificato al di fuori di questa scorecard e delle catture in `review_a3/`.
