# Design Council V2 — Accessibilità e RTL/arabo

Ruolo: esperto accessibilità + specialista UI arabo/RTL. Data: 23 settembre 2026.
Metodo: **test, non lettura**. Chromium headless di Playwright (browser proprio, mai la porta 9222),
server statico `http://127.0.0.1:8790/docs/design-v2/directions/<dir>/{home,dashboard}.html`.
axe-core **non** è in `node_modules` (nessuna installazione): tutte le verifiche sono script propri
(`scratchpad/a11y_audit.py`, `a11y_probe2..4.py`; risultati grezzi in `scratchpad/a11y_results.json`).
Per pagina: ordine dei titoli, landmark, nomi di img/SVG/controlli, campi form, contrasto calcolato dagli
stili computati (stack di pittura via `elementsFromPoint`, alfa composto; per header sticky sopra il
contenuto campionamento dei pixel con testo reso trasparente), 40 stop di Tab con confronto stile
`:focus-visible` vs non focalizzato e intersezione con l'header sticky, target ≥ 24 px con eccezione
di spaziatura 2.5.8, skip link, `scroll-padding`; `prefers-reduced-motion: reduce` a 0,3 s (elementi a
opacità 0 / hidden / fuori schermo / tracciati non disegnati, conteggio testi visibili vs pagina normale);
`forced-colors: active` (fold + rail); RTL con `dir="rtl" lang="ar"` impostati da init-script **prima**
del caricamento e di nuovo dopo, a 1440 e 390. Evidenze: `docs/design-v2/council/shots/a11y/` (86 file:
`*_forced_*`, `*_reduced_*_300ms`, `*_rtl_{1440,390}_*`, `*_focus_stop*`).

Nota di misura: nessun testo poggia direttamente sulla fotografia in nessuna delle tre direzioni (la foto
vive dentro la porta); il caso «vetro» reale è l'header sticky con `backdrop-filter` sopra il contenuto,
misurato a scroll 300/1400/2600 px: A 5,43:1, B 6,13:1, C 5,35:1 nel caso peggiore (link di nav) — PASS.

## Tabella dei fatti (1440×900, pagina assestata; RTL anche a 390)

| Pagina | Contrasto peggiore (testo) | Fail testo | Controlli senza nome | Focus (40 stop) | Target < 24 px | Reduced motion 0,3 s | Forced colors | Prop. fisiche CSS (tot / non gestite) | Difetti di specchiatura |
|---|---|---|---|---|---|---|---|---|---|
| A home | 4,86 (`.btn--primary`, need 4,5) | 0 | 0/52 | 40 visibili, 0 oscurati, outline 2 px ≥ 3,29:1 | 5 (link legali footer 15 px, spaziatura OK) | PASS (0 nascosti; 123 = 123 testi; `.net__packet` decorativo spento) | PASS (36 el. con `forced-color-adjust:none`) | 24 / 9 | lock-up specchiato; «™» salta in testa; 2 etichette SVG tagliate; spina mobile a sinistra; overflow 16 px a 390 |
| A dashboard | **3,48** (`span.t-cap` «Contexte», rgb(95,107,124) su rgb(6,18,31)) | **1** | 0/31 | 40 visibili, 0 oscurati | 4 (breadcrumb 42×20, footer) | PASS (146 = 146) | PASS (chip con glifo ○, bordi) | idem | rail 2.0 avanza da destra ✓; «MA → IT» non invertito |
| B home | 4,79 (`p.t-folio` footer) | 0 | 0/57 | 40 visibili, 0 oscurati, outline ≥ 6,12:1 | 0 | PASS (139 = 139; 1 `circle.route__node` a opacità 0 per stato, non per moto) | PASS (nessun blocco CSS; stati = glifo + testo) | 6 / 0 | lock-up specchiato; «TM» salta prima di ENTRY; disegno in sezione non specchiato (dichiarato) |
| B dashboard | 5,24 | 0 | 0/31 | 40 visibili, 0 oscurati | 0 | PASS (160 = 160) | PASS (rail: bordo superiore + riquadro + glifi ✓, meter bordato) | idem | rail avanza da destra ✓, gruppo Maroc a destra ✓ |
| C home | 5,69 | 0 | 0/34 | 40 visibili, 0 oscurati, outline ≥ 3,44:1 | 10 («ع» 19×24; link footer/contatto 15 px, spaziatura OK) | PASS (119 vs 120: etichetta del toggle marea) | PASS parziale (isoipse in `CanvasText`) | 4 / 0 | nessuno: lock-up e titolo bloccato `dir="ltr"` ✓, territorio e rotta specchiati ✓ |
| C dashboard | **3,86** (`.state--pending` «Non analysé» ×3, rgb(140,109,75) su rgb(239,230,218)) | **3** | 0/24 | 40 visibili, 0 oscurati | 5 (breadcrumb, footer) | PASS (134 = 134) | **difetto**: le isoipse diventano linee nere che attraversano i testi della case band | idem | rail avanza da destra ✓ (marcatore su 02 a x=933) |

Altri fatti comuni: un solo `h1`, nessun salto di livello, `main/header/footer/nav` presenti e le `nav`
multiple tutte con `aria-label`; tutti gli SVG `aria-hidden` o con nome (A 55+1, B 22+1, C 31+0); skip link
primo elemento focalizzabile e diretto a `<main>` (C aggiunge `tabindex="-1"`); `scroll-padding-top`
88/84/80 px ≥ header 73/69/64 px (2.4.11 ✓); 0 tabindex positivi; 0 autoplay; 0 errori console (A: 2 font
falliti alla prima richiesta, 0 alla ricarica — transitorio del server, non del prototipo). Tabelle: A e B
con `caption` e `th[scope]` 9/9; C dashboard senza `caption` (`th[scope]` 4/4). Contrasto non testuale
(1.4.11): A `.juris__seg` 8,8–10,9:1, `.btn--primary` 3,44 ✓; B `.btn--secondary` bordo 3,11 ✓, meter 3,55 ✓;
C `.btn--secondary`/`.tide-toggle` bordo **2,2:1** sul hero scuro (il testo passa; il confine no), meter
2,2 ma `aria-hidden` con equivalente testuale «0 sur 5 éléments complétés» ✓. Indicatore di focus: outline
2 px `solid` ovunque, mai coperto dall'header (il caso «skip link sotto l'header» è un falso positivo:
`elementsFromPoint` restituisce lo skip link stesso, z-index 100/200). Il ciclo di Tab è partito dal footer
(punto di partenza della navigazione sequenziale dopo lo scroll), quindi i 40 stop coprono footer + header +
hero + sezioni.

## Direzione A — Rete luminosa

**ACCESSIBILITÀ 8/10.** Zero fail sul sito; un fail sul dashboard (`.t-cap` 3,48:1 nella barra applicativa).
Le firme hanno versione testuale (stazioni del processo con responsabile scritto, legenda del rail con
glifi + pattern). Con `forced-colors` sopravvive, ma perché **36 (home) / 122 (dashboard) elementi**
tengono i colori d'autore via `forced-color-adjust: none` (`.btn, .route, .card, .next`): in un tema Windows
ad alto contrasto scuro le card resterebbero bianche — regge, ma ignora la palette dell'utente. Link legali
del footer a 15 px di altezza (2.5.8 passa solo per l'eccezione di spaziatura).

**RTL 6/10.** Al desktop la composizione regge: porta non specchiata, rete e onda specchiate con etichette
contro-specchiate, rail 2.0 da destra, barra di progresso con origine a destra, frecce `.ic--flip` invertite.
Ma: **9 proprietà fisiche non gestite** su 24 (`styles.css:320` legenda `left:0`; `:394` `translateX(4px)`
sul CTA delle rotte senza variante RTL; `:403–408` hub/stelo/bus/tick delle rotte mobili in `left`;
`:463, :466` spina e pallini del processo mobile in `left`) → a 390 in RTL la spina e i tick stanno a
**sinistra** del testo allineato a destra e la pagina ha **16 px di overflow orizzontale**
(`shots/a11y/a-luminous-network_home_rtl_390_{routes,process}.png`). Lock-up specchiato (bandiera a
destra) e «™» che salta davanti a «ITALY LEGAL ENTRY» perché né `.lock` né il titolo bloccato hanno
`dir="ltr"`. Le 3 `text-anchor` inline della rete non vengono scambiate sotto `scaleX(-1)`: «Italie» e
«Maroc» risultano tagliati ai bordi. **17 etichette tracciate** (10 maiuscole) restano in AR, compreso il
tracking negativo del `h1` (−0,78 px) — il reset a `letter-spacing: 0` copre solo 6 classi ed è agganciato a
`[dir="rtl"]`, non a `:lang(ar)`. Divisore «MA → IT» non invertito.

## Direzione B — Profondità architettonica

**ACCESSIBILITÀ 9/10.** Zero fail di contrasto su entrambe le pagine, zero target sotto 24 px, outline
6,1–7:1. Stati del rail sempre glifo + testo («✓ Terminée», «◉ Étape actuelle», «○ À venir») e riquadro sul
segmento corrente: sopravvivono a `forced-colors` **senza** alcun blocco dedicato. Reduced motion: titolo e
portale completi al primo paint; l'unico elemento a opacità 0 (`circle.route__node`) è uno stato legato al
capitolo 6 tramite IntersectionObserver (`main.js:188–197`, fuori da `withMotion`), non un reveal: appare
istantaneamente quando il capitolo è attivo. Da valutare renderlo statico anche in `reduce` come già fatto
sotto 1024 px (`styles.css:513`).

**RTL 7,5/10.** **0 proprietà fisiche non gestite** (le 6 occorrenze sono centrature simmetriche o
`--flip`). Sottolineatura nav, marcatore del rail, frecce e barra di progresso usano `--origin-start`/`--flip`
correttamente; le quattro soglie a gradoni scendono da destra; il gruppo «Maroc · avant le départ» sta a
destra. Difetti: lock-up specchiato (bandiera a destra del wordmark: `a.lockup` ha `direction: rtl`) e
«TM» che salta davanti a «ENTRY» (titolo senza `dir="ltr"`); **5–6 etichette maiuscole tracciate** non
azzerate in AR (`.eyebrow` 1,44 px, `.portal__cap` 2,2 px, `#forum-title` 1,12 px, `.rail__juris`,
`.app-bar__ref`, `.case__ref`); il disegno in sezione non si specchia e le 12 `<text>` restano
`text-anchor: start` (dichiarato in DIRECTION.md §9 come «da fare»: in RTL le etichette stanno a destra dei
piani, leggibili ma non composte). Cassetto mobile a tutta larghezza (nessun lato da specchiare).

## Direzione C — Diplomazia contemporanea

**ACCESSIBILITÀ 8/10.** Struttura la più completa: skip link con `tabindex="-1"` sul target, `dir="ltr"`
sul titolo bloccato, rail codificato a **pattern** (pieno/tratteggio/punti/linee) con legenda scritta,
stati con glifo. Fail: chip `.state--pending` **3,86:1** (×3 nel dashboard), confine dei bottoni ghost e del
toggle marea **2,2:1** sul hero scuro, «ع» del cambio lingua largo 19 px, checklist senza `caption`. In
`forced-colors` i controlli reggono, ma `.terr__layer path { stroke: CanvasText }` (`styles.css:672`)
trasforma le isoipse decorative in linee nere piene che attraversano «Tableau de bord», dossier e stato
nella case band (`shots/a11y/c-contemporary-diplomacy_dashboard_forced_1440_fold.png`).

**RTL 9/10.** **0 proprietà fisiche non gestite** (ogni `translateX` ha la variante `[dir="rtl"]`), lock-up
`direction: ltr`, titolo `dir="ltr"`, `:lang(ar)` con famiglie arabe, `letter-spacing: 0` e
`text-transform: none` globali (restano solo `th` 0,96 px e uno `span` 0,78 px), `min-inline-size` sui
bottoni, opacità 1 sulle didascalie. Territorio, rotta del processo e isoipse dei pannelli specchiati; la
rotta si legge da destra («Pays d'origine · rive sud» a destra, «Italie · rive nord» a sinistra); rail 2.0
da destra a 1440 e verticale con barre sul lato di lettura a 390; frecce `icon--flip-rtl` invertite, globo,
pausa e chevron giù correttamente **non** invertiti; nessun overflow. Da verificare (non attribuibile al
solo RTL): a 390 il cassetto aperto copre gli ultimi ~8 px dell'header.

## Must-fix (con riferimenti)

A — `styles.css:403–408, 463, 466` → `inset-inline-start` (elimina overflow e mette spina/hub a destra);
`:320` legenda in logico; `:394` variante `[dir="rtl"]`; `:688–689` spostare su `:lang(ar)` ed estendere il
reset a `h1 span/em`, `.lock__*`, `.t-mono`, `.case__ref`; `home.html`/`dashboard.html`: `dir="ltr"` su
`.lock` e sul wordmark bloccato, scambio `text-anchor` start↔end sulle 3 etichette della rete sotto RTL;
`dashboard.html` `.t-cap` → ≥ 4,5:1 (es. rgb(143,160,181) = 7,06); `:695–696` limitare
`forced-color-adjust: none` ai soli segmenti a pattern; divisore «MA → IT» con glifo logico.
B — `direction: ltr` su `.lockup` e `dir="ltr"` sul titolo (TM); `:lang(ar)` `letter-spacing: 0` anche per
`.eyebrow`, `.portal__cap`, `.t-band`/`#forum-title`, `.rail__juris`, `.app-bar__ref`, `.case__ref`,
`.t-mono` (`styles.css:170, 204, 228, 470`); decidere specchiatura del disegno e `text-anchor` (§9);
opzionale `.route__node` statico sotto `reduce` (`:398–399` come `:513`).
C — `.state--pending` colore ≥ 4,5:1 (es. rgb(112,84,52)); `styles.css:672` isoipse → `GrayText` o
`display: none` in `forced-colors`; bordo `.btn--secondary`/`.tide-toggle` ≥ 3:1 sul hero; «ع» ≥ 24 px;
`<caption>` sulla checklist; `th` senza tracking in AR; verificare la sovrapposizione cassetto/header a 390.

## RANKING

Accessibilità: **1. B (9)** · 2. A (8) · 3. C (8) — A e C hanno entrambe un token di colore che fallisce;
C ha più istanze (3) e il difetto delle isoipse in forced-colors, A il rischio `forced-color-adjust: none`.
RTL: **1. C (9)** · 2. B (7,5) · 3. A (6).
Combinato: **1. C (17)** · 2. B (16,5) — distanza minima, i difetti di B sono tutti a basso costo · 3. A (14).

## HUMAN_QA_REQUIRED (onesto)

Tutto quanto sopra è misurato da script e da screenshot: **non** sostituisce (1) una sessione reale con
NVDA/JAWS su Windows e VoiceOver su iOS — ordine di lettura del rail e del processo, annuncio di
`aria-current="step"`, gestione del focus di mega-menu e cassetto, tabelle; (2) Windows High Contrast
reale nei temi nero e bianco (qui solo la media query emulata con palette chiara di default); (3) una
**revisione araba madrelingua**: i prototipi sono in francese, quindi la bidirezionalità di stringhe miste
FR/AR, i numerali (orientali vs occidentali), la resa di Noto Naskh/IBM Plex Arabic a 12–100 px con
interlinea 1,8 e diacritici, il senso delle icone specchiate e la traduzione di «A doorway, not a shortcut»
restano compiti umani; (4) dispositivi reali (Safari iOS in AR, Chrome Android) per il cassetto e il rail
verticale.
