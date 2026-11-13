# MOTION SYSTEM V2 — il moto ha un autore

Stato: **FONDAMENTA FISSATE** (token, curve, funzioni, politiche) · le voci del catalogo per
componente si compilano con la direzione scelta (§ 6) · Libreria: Motion 13.4.1 per JavaScript,
importata solo da `static/js/src/motion.js` · Prove: `docs/design-v2/MOODBOARD.md` § 5 e
`PREMIUM_2026_PRINCIPLES.md` § 3, 4, 5, 12, 16.

---

## 0. La regola che governa tutte le altre

Ogni animazione dichiara **una** funzione fra sette, e se non ne ha una non esiste:

| Funzione | Che cosa fa capire | Esempio ammesso | Esempio vietato |
|---|---|---|---|
| ORIENTAMENTO | da dove vengo, dove sono | il pannello di navigazione entra dal lato di lettura | testo che entra da direzioni casuali |
| GERARCHIA | che cosa conta di più | il titolo si rivela riga per riga, poi il resto | tutto entra insieme con lo stesso fade |
| CAUSALITÀ | che cosa ha prodotto che cosa | la riga della checklist cambia stato dopo il salvataggio | uno stato che «lampeggia» senza azione |
| STATO | in che condizione è la cosa | il chip di stato transisce fra due parole | colore che pulsa in continuazione |
| FEEDBACK | il sistema ha ricevuto | il bottone si abbassa di 1 px alla pressione | bottone che «fluttua» a riposo |
| PROFONDITÀ | che cosa sta sopra | l'overlay si solleva con ombra 64 | parallasse costante su tutta la pagina |
| DELIZIA | un momento firmato | la chiave della porta si rivela una volta all'ingresso | la chiave che levita per sempre |

`fade-in-up` generico su tutto ciò che entra in viewport è **vietato**: è la prima riga di
ANTI_PATTERNS.md.

## 1. Token

Vivono in `static/css/tokens.css` e in `static/js/src/motion.js` come **un solo insieme**; un
valore che compare in uno e non nell'altro è un difetto.

### Durate — quattro, più i loop

| Token | ms | Uso |
|---|---:|---|
| `--motion-instant` | 120 | feedback (pressione, cambio di stato inline, hover in uscita) |
| `--motion-fast` | 180 | hover in entrata, tooltip, focus, chip |
| `--motion-base` | 240 | reveal editoriali, pannelli, tab, accordion |
| `--motion-slow` | 320 | overlay, drawer, palette comandi, transizioni di pagina |
| `--motion-ambient` | ≥ 20 000 | l'unico loop ammesso per pagina (§ 4), lineare |

Nessun altro numero. Un'animazione «di firma» (hero) può concatenare più durate con ritardi
scaglionati di 40–60 ms per riga, ma non inventa una durata.

### Curve — tre

| Token | Valore | Uso |
|---|---|---|
| `--ease-out` | `cubic-bezier(.25, 1, .5, 1)` | tutto ciò che **entra** (Stripe ×12) |
| `--ease-in` | `cubic-bezier(.7, 0, .3, 1)` | tutto ciò che **esce** (Harvey, Mercury) |
| `--ease-standard` | `cubic-bezier(.4, 0, .2, 1)` | cambi di stato bidirezionali (tab, toggle, colore) |

Vietate: ogni curva con overshoot (`(.34,1.56,.64,1)`, `(.52,1.64,.37,.66)`), `ease-in-out` sui
reveal, `linear` fuori dai loop. Il test in `tests/frontend/test_motion_system.py` conta i
`cubic-bezier` nel CSS compilato: al massimo tre.

### Molle — due, solo in JavaScript

Le molle non hanno durata fissa, quindi non stanno nel CSS; Motion le calcola.

| Nome | `spring()` | Uso |
|---|---|---|
| `SPRING_SETTLE` | `{ stiffness: 260, damping: 30 }` — nessun rimbalzo | layout che si riassesta (riga inserita/rimossa, altezza di un accordion) |
| `SPRING_FOLLOW` | `{ stiffness: 400, damping: 40 }` | elementi che seguono il puntatore (indicatore attivo del menu) |

Nessuna molla con `damping` sotto 25: rimbalza, e il rimbalzo è overshoot.

## 2. Le nove famiglie

| Famiglia | Funzione | Innesco | Durata | Curva | Che cosa muove | Stato ridotto |
|---|---|---|---|---|---|---|
| ENTRATA | gerarchia | `inView` (una volta) | base, scaglionata 40–60 ms | out | `opacity 0→1`, `translateY 12→0 px` (mai più di 16) | tutto già al valore finale |
| USCITA | orientamento | azione | instant/fast | in | `opacity 1→0`, `translateY 0→-8` | rimozione immediata |
| LAYOUT | causalità | cambio dei dati | SPRING_SETTLE | — | `height` via `animate` su valore misurato, `transform` sui fratelli | salto immediato |
| SCROLL | orientamento | posizione di scroll | legata, non temporale | — | `scroll()` → `strokeDashoffset`, `opacity`, `translate` | valore finale fisso |
| HOVER | feedback | puntatore (solo `hover: hover`) | fast in, instant out | out / in | `transform` ≤ 2 px, colore, ombra **di ruolo** | identico (l'hover non è moto essenziale) |
| FOCUS | orientamento | tastiera | fast | out | anello 2 px + alone 3 px al 30 % | identico, istantaneo |
| DATI | stato | cambio del valore | base | standard | numero che scorre solo se il dato è reale e calcolato; chip che cambia parola | testo aggiornato senza transizione |
| OVERLAY | profondità | apertura | slow | out / in | scrim `opacity`, pannello `translateY 8→0` + `opacity`; drawer `translateX` dal lato di lettura | apertura immediata, scrim fermo |
| PAGINA | orientamento | navigazione | slow | out / in | crossfade del `<main>` con testata condivisa (View Transitions dove supportate) | nessuna |

Proprietà animabili: `transform`, `opacity`, e per gli SVG `stroke-dashoffset` / `pathLength`.
`height` solo via misura + `transform`/`clip-path`. **Mai** `filter`, `box-shadow` in loop, `width`,
`top/left`, `background-position` su aree grandi.

## 3. Reduced motion è uno stato completo, non un'assenza

`withMotion(fn, settle)` in `static/js/src/motion.js` è l'unico punto d'ingresso: la seconda
funzione **deve** portare l'elemento allo stato finale. In CSS, ogni `@keyframes` e ogni
`transition` sta dentro `@media (prefers-reduced-motion: no-preference)`; fuori da quel blocco il
valore è quello finale. Con «riduci movimento» attivo la pagina è identica nei contenuti, i reveal
sono istantanei, i loop fermi, la porta dell'hero è completa e ferma, nulla resta a opacità 0.

La preferenza si legge **dal vivo** (`matchMedia` a ogni chiamata), non una volta: chi la cambia
a pagina aperta non deve ricaricare.

## 4. Un solo oggetto vivo per pagina

Una pagina IMMERSIVE può avere **un** loop ambientale (≥ 20 s, lineare, `transform`/`opacity`,
in pausa fuori dal viewport via `IntersectionObserver`, fermo con reduced-motion) e **un** oggetto
indicizzato allo scroll. Le pagine RICH ne hanno al massimo uno dei due; STANDARD, DENSE e LEGAL
nessuno. La chiave che «levita per sempre» del sito attuale è esattamente ciò che questa regola
esclude: in V2 la chiave si rivela una volta.

## 5. Direzione e arabo

Il moto che ha una direzione di lettura la segue: in `dir="rtl"` i pannelli entrano da destra, il
rail di processo avanza da destra a sinistra, `translateX` cambia segno (proprietà logiche o
`--dir: -1` moltiplicato in JS). Non si specchia ciò che non è direzionale: rotazioni, scale,
opacità, controlli media, numeri. `tests/i18n/test_rtl_browser.py` copre le firme visive in AR.

## 6. Catalogo per componente — da compilare con la direzione scelta

Ogni voce: nome · funzione · innesco · durata · curva · proprietà · stato ridotto · budget (0
layout/paint in DevTools durante l'animazione).

| Componente | Funzione | Stato |
|---|---|---|
| Hero: titolo a reveal riga per riga | gerarchia | *da compilare* |
| Hero: la porta (`enhanced-v2`) — arco e gradini che si disegnano, chiave che si rivela | delizia + orientamento | *da compilare* |
| Quattro vie di accesso | orientamento | *da compilare* |
| Processo NEED → INCLUSION (scroll-linked) | orientamento | *da compilare* |
| Rail giurisdizione / responsabilità 2.0 | stato | *da compilare* |
| Navigazione: header che si trasforma allo scroll, mega-menu | orientamento + profondità | *da compilare* |
| Piattaforma: cambio di stato del fascicolo | causalità | *da compilare* |
| Piattaforma: caricamento documento → stato | causalità + feedback | *da compilare* |
| Tabelle: inserimento/rimozione riga, apertura dettaglio | layout | *da compilare* |
| Overlay: dialog, drawer, palette comandi | profondità | *da compilare* |
| Transizione sito → portale dopo l'accesso | orientamento | *da compilare* |
| Stati vuoti e di caricamento (skeleton) | stato | *da compilare* |

## 7. Budget e prova

Prima di accettare un'animazione: pannello Performance di Chrome durante l'esecuzione, 0 layout e
0 paint oltre il primo frame; INP < 200 ms sulle interazioni che la innescano; nessuna animazione
fuori dal viewport; bundle entro `FRONTEND_DEPENDENCIES.md` § 3. Test su moto normale, ridotto,
CPU rallentata 4×, viewport mobile.
