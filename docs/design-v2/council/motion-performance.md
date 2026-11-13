# DESIGN COUNCIL V2 — MOTION + PERFORMANCE · verdetto misurato

*Motion Design Director + Frontend Performance Expert · 23 settembre 2026 · Chromium 153 headless (Playwright, browser proprio), 1440×900, server statico `127.0.0.1:8790`. Evidenze: `council/shots/motion/*.png` (piega a 0,3 / 1 / 2 / 4 s in moto normale, piega a 0,3 s in moto ridotto, porta isolata a 0,3 e 4 s, piega dopo il toggle dal vivo) e `council/motion-metrics.json` (rAF 6 s a CPU 1× e 4×, traccia CDP con Layout/Paint per finestra, inventario `document.getAnimations()`, sonde porta, rete, listener). Regole di riferimento: `MOTION_SYSTEM.md`, `FRONTEND_DEPENDENCIES.md` § 3, `BRAND_ASSETS.md` § 2.*

## 0. Numeri condivisi (non pesano nel confronto)

| Voce | A | B | C | Nota |
|---|---:|---:|---:|---|
| JS trasferito, gzip calcolato (main + Motion 24,0 KB) | 26,9 KB | 27,7 KB | 27,2 KB | tutti entro i 45 KB di § 3 |
| CSS gzip (styles.css) | 13,0 KB | 12,4 KB | 11,5 KB | + fonts.css 14 KB raw |
| HTML home, raw → gzip | 33 → 7,2 KB | 24 → 5,8 KB | **91 → 33,0 KB** | C inlinea 155 path di isoipse |
| Font caricati (home) | 368 KB · 6 file | 343 KB · 5 file | 368 KB · 6 file | Newsreader variabile 132 KB + corsivo 147 KB per una riga corsiva: da subsettare (tutte e tre) |
| Fotografia della porta | 949 KB | 949 KB | 949 KB | originale del committente in tutte e tre: **voce condivisa, nota, da risolvere** con AVIF/WebP ≤ 120 KB per viewport; non penalizza nessuna direzione |
| Layout iniziale 0–0,5 s | 255 ms | 320 ms | 254 ms | dominato da font + decodifica JPEG; identico nell'ordine di grandezza |
| Scroll nativo | ✓ | ✓ | ✓ | nessuna libreria smooth-scroll, `scroll-behavior: auto`, nessun `wheel`/`preventDefault`; Motion registra un `touchstart` non passivo su `window` (libreria, da verificare in fase 7) |

Il server non comprime (`SimpleHTTP`): i byte gzip sopra sono calcolati sui file, i byte «trasferiti» nel JSON sono raw. Caveat: headless usa un rasterizzatore software, quindi i costi di paint sono relativi, non assoluti; i conteggi di Layout/Paint sul thread principale e i frame rAF sono invece reali.

## 1. Tabella comparativa misurata

| Misura | A home | A dash | B home | B dash | C home | C dash |
|---|---:|---:|---:|---:|---:|---:|
| `cubic-bezier` distinti nel CSS (max 3) | 3 ✓ | — | 3 ✓ | — | 3 ✓ | — |
| Loop infiniti dichiarati / **in esecuzione a 4 s** | 4 / **3** | 1 / **1** | 1 / **1** | 0 / 0 | 5 / **5** | 0 / 0 |
| Periodo dei loop | 24 s · 6 s · 4 s (+3,2 s morto) | 2,8 s | 24 s | — | 28/34/40 s · 6 s · 6 s | — |
| Loop in pausa fuori dal viewport | no (3 attivi in fondo pagina) | no | no | — | marea sì (IO) · chiave/alone **no** | — |
| Loop fermi dopo toggle «riduci movimento» a pagina aperta | ✓ | ✓ | ✓ | — | **no: marea, chiave, alone continuano** | — |
| Moto ridotto da caricamento: elementi nascosti nella piega a 0,3 s | 0 ✓ | 0 ✓ | 0 ✓ | 0 ✓ | 0 ✓ | 0 ✓ |
| Moto normale: elementi nascosti nella piega a 0,3 s | 7 (rete + **scheda Forum**) | 0 | **15 (tutta la copia hero + tutta la porta)** | 0 | 1 (stazioni) | 0 |
| Chiave della porta visibile al primo paint | ✓ (0,3 s, opacità 1) | — | **✗ (compare a 1,42 s + 320 ms)** | — | ✓ (0,3 s, opacità 1) | — |
| rAF 0–3 s a CPU 1× (coreografia): fps medi / frame persi | 45,5 / 43 | 52,3 / 23 | 49,9 / 30 | 54,5 / 16 | **30,8 / 87** | 53,5 / 20 |
| rAF 3–6 s a CPU 1× (riposo): fps / persi / p95 | 59,3 / 2 / 16,8 ms | 60 / 0 | 58,7 / 4 / 16,8 ms | 60 / 0 | **27,2 / 98 / 66,7 ms** | 60 / 0 |
| rAF 3–6 s a CPU 4× (riposo): fps | 25,2 | 51,4 | **36,4** (migliore) | 59,0 | **19,8** | 60,0 |
| Traccia CDP 3–6 s a riposo: Layout / Paint | **178 / 24** | 0 / **363** | **1 / 4** | 0 / 4 | **82 / 162** | 0 / 4 |
| Animazioni scroll-linked native (ScrollTimeline/ViewTimeline) | 3 ✓ | 0 | 0 (JS) | 0 | 0 (JS) | 0 |
| DOM · radici SVG · path | 572 · 56 · 37 | 511 · 52 · 30 | 424 · 23 · 14 | 435 · 30 · 10 | 548 · 31 · **155** | 476 · 42 · 87 |
| Elementi con reveal generico in viewport | 17 | 18 | 17 | 11 | 19 | 8 |

Tutte e tre chiamano `scroll()` di Motion, ma solo A ottiene timeline native (usa `transform: [...]`); B e C usano le scorciatoie `y`/`scale`, che Motion degrada al callback JavaScript su evento di scroll. Regola rispettata alla lettera («via scroll()»), non nello spirito (0 lavoro sul thread principale).

## 2. Direzione A — «Rete luminosa» · MOTION QUALITY **6/10** · performance **CONDITIONAL**

**Numeri**: home 59,3 fps a riposo ma **178 Layout in 3 s** (uno per frame: il pacchetto anima `offset-distance` su un `<circle>` SVG con `filter: drop-shadow`), 25 fps a CPU 4×; cruscotto 60 fps ma **363 Paint in 3 s** per il `box-shadow` pulsante del rail. Dopo una rotella di 600 px la pagina **continua a muoversi da 598 a 584 px per ~240 ms** (3 prove su 3): il header sticky anima `min-height` 73→57 px e lo scroll anchoring insegue la transizione; con le transizioni di layout disattivate il salto di 16 px resta ma è istantaneo.

**Violazioni di MOTION_SYSTEM.md**
- `styles.css:668` `keyfloat 6s ease-in-out infinite` — **la chiave che levita per sempre** (§ 0 DELIZIA, esempio vietato; § 4; BRAND_ASSETS § 2 «in V2 la chiave si rivela una volta»); < 20 s; `ease-in-out`.
- `styles.css:669` `keyglow 4s ease-in-out infinite` — secondo loop, < 20 s.
- `styles.css:673,676,294` `packet 24s` su SVG con `drop-shadow`: terzo loop; SVG non compositato → layout+style a ogni frame; mai in pausa fuori dal viewport (misurato attivo in fondo pagina).
- `styles.css:674,677` `hubpulse 3.2s` anima `r`: regola morta (`.net__hub .ring` non esiste in `home.html`) ma dichiarata con periodo vietato.
- `styles.css:675,678` `herepulse 2.8s` su **`box-shadow` in loop** nel cruscotto (§ 2 «mai box-shadow in loop»; § 4: pagina DENSE, nessun loop); § 0 STATO «colore che pulsa in continuazione».
- `styles.css:185,193,195` transizioni su `min-height`, `width/height`, `font-size` del header (§ 2 «mai width, height»); causa il creep di scroll misurato.
- `main.js:82` titolo 280 ms; `main.js:110,111,113,115` 900 / 600 / 1200 / 600 ms; stagger 150 e 35 ms (`:110`, `:115`) — durate inventate e stagger fuori 40–60 (§ 1).
- `main.js:76-79` reveal generico opacity + translateY(14) su 17 elementi, 320 ms invece di 240 — ANTI_PATTERNS riga 1.
- `home.html:164` `aside.focus` (data reale del Forum) sta nella piega a 1440×900 ma resta a **opacità 0 a 0,3 s e ancora a 4 s** (inView con margine −8 % non scatta senza scroll); in moto ridotto è visibile. Contenuto nascosto dal moto.
- `styles.css:378` `.route:hover translateY(-4px)` — HOVER ≤ 2 px; `styles.css:284,417` `drop-shadow` statico su tracciati che si disegnano (rasterizzazione a ogni frame del tracé).
- `main.js:17` preferenza letta una volta (classe `motion-ok`); il blocco `@media reduce` (`:681`) rimedia per i loop CSS (verificato: tutto fermo dopo il toggle dal vivo).

**Funzione vs decorazione**. Servono: titolo a maschera (gerarchia); contorno che si traccia (struttura); **percorso → archi → nodi → etichette** (causalità: il momento più leggibile dei tre prototipi, screenshot t2000→t4000); processo legato allo scroll con stazioni che si accendono (orientamento); parallasse a tre velocità solo ≥ 1024 px su ViewTimeline nativa (profondità, costo zero); header compatto + barra di lettura (orientamento); stelo delle rotte in hover/focus-within (feedback); rail 2.0 (stato, purché l'anello sia statico). Decorazione: chiave che levita, alone che respira, pacchetto (dichiarato «l'unico oggetto vivo», è il terzo), pulsazione del rail.

**Porta (BRAND_ASSETS § 2)**: riconoscibile ✓ (arco 3/4, foto al 50 %, arco interno navy, chiave oro 64×138 px, tre gradini, didascalia); chiave al primo paint ✓; nessun `filter` in loop ✓ (alone pre-renderizzato in opacità); nessun overshoot ✓; moto ridotto completo e fermo ✓ (0 nascosti). **Ma la chiave levita per sempre ✗** — l'unico vincolo di § 2 sulla dinamica che A viola, ed è quello che il MOTION_SYSTEM chiama per nome.

**Must-fix**: (1) rimuovere `keyfloat`, `keyglow`, `herepulse`; tenere al massimo il pacchetto, spostato su un wrapper HTML con `offset-path` compositato o su `transform` lungo punti campionati, in pausa via IntersectionObserver; (2) header a altezza costante: compattare il lock-up con `transform: scale`, mai `min-height/width/height/font-size`; (3) scheda Forum: nessun reveal per ciò che è già nella piega (o `inView` con `amount: 0`); (4) durate 280/600/900/1200 → 320 concatenate con ritardi; (5) togliere `drop-shadow` da `net__route`/`proc__path`/`net__packet`; (6) `.route:hover` a −2 px; (7) sostituire `[data-reveal]` generico con reveal solo sui titoli di sezione.

## 3. Direzione B — «Profondità architettonica» · MOTION QUALITY **8/10** · performance **PASS**

**Numeri**: home 58,7 fps a riposo con **1 Layout e 4 Paint in 3 s** (il migliore), 36,4 fps a CPU 4× (il migliore fra le home); cruscotto 60 fps, 0 Layout, 4 Paint, **0 animazioni infinite**; rotella nativa 600/600; JS 27,7 KB gzip; DOM più leggero (424 nodi, 14 path). Un solo loop (`glowBreath` 24 s, lineare, opacità): conforme a § 4, costo misurato ≈ 0; si ferma con il toggle dal vivo.

**Violazioni di MOTION_SYSTEM.md**
- `styles.css:85` `--d-trace: 960ms` (unica durata inventata) e `:728` `transition: stroke-dashoffset var(--d-trace) linear` — `linear` fuori dai loop (§ 1).
- `styles.css:458` `.seuil__door::before { transition: inset }` e `:459` `.seuil__lintel { transition: … inset }` — `inset` = top/left, layout (§ 2).
- `styles.css:215,217` `.lockup__mark { transition: width, height }`, `.lockup__wm { transition: font-size }` — layout in transizione al distacco del header (il header però non cambia altezza: nessun creep misurato).
- `styles.css:373` loop dell'alone non in pausa fuori dal viewport (misurato attivo in fondo pagina) né sospendibile (§ 4).
- `styles.css:341` `will-change: transform` permanente sull'`<img>` 2400×1600 → layer GPU da ~15 MB decompressi finché non esistono i derivati.
- `styles.css:460,462,366` hover a −4 px su soglie e chiave — HOVER ≤ 2 px.
- `main.js:120,174` stagger 70 ms (> 60); `main.js:173` reveal delle soglie y 24 → 0 (ENTRATA: mai più di 16); `main.js:158` reveal generico su 17 elementi in 4 gruppi — ANTI_PATTERNS riga 1, anche se qui i gruppi sono testate di sezione e CTA, non «tutto».
- `main.js:124-131` sequenza della porta a `setTimeout` (120 → 1560 ms): funziona ed è coperta dal timer di sicurezza a 4 s (`:264`), ma non è annullabile né legata a `animate().finished`.
- Parallasse (`main.js:144-145`) e barra di lettura (`:46`) via `scroll()` con callback JS: nessuna ScrollTimeline nativa misurata (usa `y`, non `transform`).

**Funzione vs decorazione**. Servono: titolo a maschera 320 ms stagger 70 (gerarchia); *mise en registre* del piano retrostante e delle targhe (profondità, 320/240 ms); tracé dell'arco (orientamento/struttura); **arco interno che sale 28 px → chiave che sale 26 px dai gradini → gradini che si costruiscono dal centro** (causalità: percorso → avanzamento, leggibile nei frame t1000→t2000→t4000); capitolo che illumina il piano n via IntersectionObserver (stato, misurato); tracé del processo legato allo scroll; header che si stacca (orientamento); soglia che si apre in hover/focus-visible (feedback); marcatore del rail che si disegna una volta (stato). Decorazione: solo il respiro dell'alone a 24 s, ammesso. È la sola direzione in cui il catalogo di § 6 si compila senza eccezioni.

**Porta (BRAND_ASSETS § 2)**: riconoscibile ✓ ed è la più fedele (gradini navy 34/24/16 %, foto .34, vignetta navy .82, ombra dell'arco interno originale); nessun `filter` in loop ✓; nessun overshoot ✓; moto ridotto completo e fermo dal primo paint ✓ (0 nascosti, alone fisso .8); **la chiave si rivela una volta ✓** (unica direzione conforme). **Chiave al primo paint ✗**: a 0,3 s la porta è un rettangolo avorio con due linee, a 1,0 s ancora vuota (`b_home_normal_t1000.png`), la chiave entra a 1,42 s e si assesta a ~1,75 s; con essa restano a opacità 0 eyebrow, lead, corpo, CTA e nota (15 elementi nella piega a 0,3 s). Non viola la lettera di § 2 (che vieta l'invisibilità solo in moto ridotto), ma per 1,4 s l'utente non vede né l'asset del committente né un bottone.

**Must-fix**: (1) porta visibile dal primo frame: piano, foto, arco interno e chiave a opacità 1 subito; coreografare *solo* tracé, salita di 8–12 px di chiave e arco interno, gradini `scaleX` — la causalità resta, l'attesa sparisce; (2) copia hero: CTA e corpo senza opacità 0 (o ritardo ≤ 160 ms totale), il reveal resta al solo titolo; (3) `inset` → `transform: scale`/`translate` su `seuil__door::before` e `seuil__lintel`; (4) 960 ms → 320 + 320 + 320 concatenati con `--e-in`; (5) alone: `animation-play-state: paused` fuori viewport via IO; (6) hover a −2 px; (7) `will-change` solo sul derivato ≤ 1000 px; (8) parallasse con `transform: [...]` per ottenere ScrollTimeline nativa; stagger 60.

## 4. Direzione C — «Diplomazia contemporanea» · MOTION QUALITY **5/10** · performance **FAIL (home) · PASS (cruscotto)**

**Numeri**: home **27,2 fps a riposo a CPU 1×** (98 frame persi in 3 s, p95 66,7 ms), **82 Layout + 162 Paint in 3 s**, 19,8 fps a CPU 4×, 30,8 fps durante la coreografia; 155 path inline, HTML 91 KB. Causa: i tre strati della marea sono `<g>` SVG animati in JavaScript da Motion (`x`/`y` su elementi SVG → attributo `transform`, mai compositato) → ripittura dell'intero territorio a ogni frame. Cruscotto: 60 fps, 0 Layout, 4 Paint, 0 loop — pulito. Rotella nativa 600/600; header via sentinella IntersectionObserver (nessun listener di scroll proprio: la soluzione più elegante).

**Violazioni di MOTION_SYSTEM.md**
- `main.js:102` **tre** loop «marea» 28/34/40 s `repeat: Infinity` su `<g>` SVG — tre oggetti vivi (§ 4: uno), su elementi non compositabili (§ 2, § 7: 0 paint oltre il primo frame).
- `main.js:139` chiave `y 0→−6` **6 s `easeInOut` `repeat: Infinity`** — la chiave che levita per sempre (§ 0, § 4, BRAND_ASSETS § 2); < 20 s; `ease-in-out`; **mai in pausa**: misurata in movimento in fondo pagina e dopo «Suspendre le mouvement» (il bottone ferma solo la marea).
- `main.js:142` alone 6 s `easeInOut` `repeat: Infinity` opacity + scale — quinto oggetto vivo, idem mai in pausa.
- § 3 «la preferenza si legge dal vivo»: dopo il toggle a pagina aperta **marea, chiave e alone continuano** (misurato); da caricamento in moto ridotto è invece corretto (0 nascosti, 0 animazioni a 1,5 s, bottone nascosto perché senza lavoro).
- `main.js:77` titolo **600 ms** stagger 80; `:98` 900 ms; `:99` stagger 120 + ritardo 500; `:135` stagger 100; `:138` 500 ms — durate inventate, stagger fuori 40–60 (§ 1).
- `styles.css:281` `transition: opacity 0.4s` (400 ms inventata); `:275-277` `0.32s` scritto a mano invece del token.
- `styles.css:276,299` hover porta −4 / −3 px — HOVER ≤ 2 px.
- `main.js:59,65` reveal generico su 19 elementi con **`scale` 1.012** (testo rasterizzato) — ANTI_PATTERNS riga 1; l'entrata «dall'alto» non lo redime.
- `styles.css:548` `animation-duration: 0.01ms` universale non copre le animazioni WAAPI/Motion (di qui il fallimento del toggle dal vivo).
- Processo e foto via `scroll()` ma JS-driven (nessuna ScrollTimeline nativa misurata).

**Funzione vs decorazione**. Servono: rotta del territorio che si traccia con stazioni (orientamento: le due rive e la porta come passaggio, chiaro a t1000); arco tracciato + gradini posati dal più largo (causalità); titolo a maschera (gerarchia, ma 600 ms è lento); rotta del processo legata allo scroll (causalità); linea d'ormeggio in hover/focus-within (feedback); marcatore «étape actuelle» che si assesta una volta (stato); header via sentinella (orientamento); **il bottone «Suspendre le mouvement»** (unica direzione con controllo utente, WCAG 2.2.2). Decorazione: marea a tre strati (dichiarata «profondità», è la «parallasse costante» dell'esempio vietato in § 0), chiave che respira, alone che respira, `scale` nei reveal.

**Porta (BRAND_ASSETS § 2)**: riconoscibile ✓ (arco `190px`, foto .5 desaturata, arco interno navy con filetto teal, chiave 67×145 px, gradini teal, didascalia tradotta come testo reale); chiave al primo paint ✓ (0,3 s, opacità 1: la sonda la conferma in tutti gli stati); nessun `filter` in loop ✓; nessun overshoot ✓; moto ridotto completo e fermo ✓ (alone .7). **Chiave che levita per sempre ✗** (il rischio n. 7 della DIRECTION lo ammette: non è una mitigazione).

**Must-fix**: (1) marea: un solo strato, su un wrapper HTML con `transform` compositato (o `animation` CSS `translate` con `animation-play-state` via IO), ≥ 20 s lineare; oppure marea statica e la rotta come unico oggetto vivo; (2) rimuovere i loop di chiave e alone (la chiave si assesta una volta: `main.js:138` basta); (3) ascoltare `matchMedia(...).addEventListener("change")` e fermare tutti i controlli Motion; il bottone deve governare *tutto* ciò che si muove; (4) titolo 320 ms stagger 60; 900/500/400 → durate del set concatenate; (5) reveal senza `scale`, e solo sui titoli; (6) hover porta −2 px; (7) isoipse: ridurre i 155 path (semplificazione a build time) o servirle come `<img>` SVG esterno cacheabile per togliere 26 KB gzip dall'HTML; (8) parallasse con `transform: [...]`.

## 5. Ranking moto + prestazioni

1. **B — Profondità architettonica** · MOTION 8/10 · **PASS**. Tre curve, un loop conforme, 1 Layout + 4 Paint a riposo, cruscotto senza moto superfluo, chiave che si rivela una volta. Da correggere: porta e CTA invisibili per 1,4 s, `inset` in transizione, 960 ms.
2. **A — Rete luminosa** · MOTION 6/10 · **CONDITIONAL**. La coreografia della rete è la più forte e la porta è completa dal primo frame, ma tre loop nell'hero, il `box-shadow` pulsante nel cruscotto, il header che anima il layout e sposta lo scroll, la scheda Forum bloccata a opacità 0.
3. **C — Diplomazia contemporanea** · MOTION 5/10 · **FAIL** (home). Intenzione territoriale e controllo utente esemplari, cruscotto pulito, ma 27 fps a riposo, cinque oggetti vivi di cui due mai in pausa, toggle dal vivo ignorato. Con la marea su un solo layer compositato e i loop della chiave rimossi passerebbe davanti ad A.

**Le tre frasi che contano**
1. Solo B rispetta la regola che decide tutto — la chiave si rivela una volta — mentre A e C la fanno levitare per sempre (6 s), riproducendo l'esatto difetto del sito attuale che MOTION_SYSTEM § 4 e BRAND_ASSETS § 2 escludono per nome.
2. A riposo l'hero di C ripittura 162 volte in 3 s e scende a 27 fps a CPU 1× perché la marea anima `<g>` SVG in JavaScript; l'hero di B nello stesso intervallo fa 1 layout e 4 paint.
3. Il cruscotto di A pulsa un `box-shadow` all'infinito (363 paint in 3 s) e il suo header anima l'altezza spostando lo scroll di 16 px per 240 ms dopo la rotella: sono difetti di sistema, non di gusto, e vanno corretti prima di qualunque adozione.

*Non misurato qui: viewport mobile e RTL (fuori mandato), INP su interazioni reali, Chrome con GPU hardware; la fotografia da 949 KB rende l'LCP di tutte e tre fuori budget finché non esistono i derivati.*
