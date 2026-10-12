# DESIGN COUNCIL V2 — Mobile e tipografia (esperto responsive + direttore tipografico)

Data: 23 settembre 2026 · Metodo: Chromium headless di Playwright (browser proprio), 6 pagine × 5 viewport
(320×568, 390×844, 768×1024, 1024×768, 1440×900), attesa 3 s + scorrimento completo per far scattare i reveal,
poi screenshot intero e above-the-fold, stato sticky a 700 px, stili calcolati. Evidenze: `shots/mobile/*.png`
(`{a,b,c}_{home,dashboard}_{W}x{H}_{full,fold,scrolled}.png`) e `shots/mobile/metrics.json` (overflow, header,
lock-up, hero, porta, vie, processo, rail, target, inventario tipografico, righe, font caricati). Zero errori di
console in tutte le 30 combinazioni. Riferimenti: PRINCIPI § 6 e § 10, MOODBOARD § 1, BRAND_ASSETS § 1.

Nota di metodo: in A e C i contenuti con `data-reveal` restano a `opacity: 0` finché lo scroll non li raggiunge
(A: `.motion-ok [data-reveal]`, C: `html.js [data-reveal]`); senza il passaggio di scorrimento gli screenshot
interi mostravano vie e processo vuoti. Non è un difetto in uso reale, ma va tenuto presente per ogni verifica.

## 1. Misure a confronto (home salvo indicazione)

| Misura | Target | A Rete luminosa | B Profondità architettonica | C Diplomazia contemporanea |
|---|---|---|---|---|
| Scroll orizzontale | 0 | 0 su tutti i 10 casi | 0 su tutti i 10 casi | **1155 / 1024 a 1024×768** (nav collassa solo ≤ 900 px; 8 voci sforano) |
| Header a 390 | ≤ 56 px | **73** (+37 barra AGAMI = 110 di chrome) | **61** (+37 = 98) | **56** (+36 = 92) |
| Header a 768 | — | 73 | 69 | 64 |
| Sticky a 390 | compatto | 57 (marchio 32, wordmark 13, tagline 0) | 61, invariato; wordmark **cresce 15 → 17** (`.header[data-floating] .lockup__wm`) | 56, invariato, tagline 8.5 visibile |
| Gutter 390 / 320 | 16 | 16 / 16 | 16 / **14** | 16 / **14.3** |
| Hero a 390 (% viewport) | ≤ 110 | **171 %** (1445 px; H1 a y 628, sotto la piega) | **141 %** (1193 px; porta a y 838 su 844: **fuori dalla prima schermata**) | **134 %** (1129 px; porta, didascalia, eyebrow e inizio H1 nella piega) |
| Hero a 768 / 1024 | ≤ 110 | 135 % / 132 % | 114 % / **152 %** | 120 % / **152 %** |
| Hero a 1440 | — | 112 % | 92 % | 89 % |
| Porta a 390 | ricomposta | scena quadrata 358×358, rete `slice` ritagliata, 9 etichette nascoste (0 vs 9 a 1440), porta 222×296 (57 % larghezza), prima del titolo → **ricomposta** | sotto H1 e CTA, 260×381 (67 %), stesso oggetto scalato (rapporto .683 vs .709 desktop), nessun ritaglio → **desktop impilato** (ordine invertito per LCP, dichiarato) | prima del titolo, 220×293 (56 %), intera (arco, foto, chiave, gradini, didascalia FR), territorio `slice` come texture, stazioni nascoste, striscia coordinate a 2 colonne → **ricomposta** |
| Quattro vie a 390 / 768 | lista verticale con scala colore | 1 col, bus verticale (pannelli a x 44), 330×268–292, titolo sans 16 px 600 maiuscolo, CTA 280×**32** / 2 col | 1 col, l'intera soglia è il link 358×350, titolo serif 23 px 300, ordinale 64 px / 2 col | 1 col, 358×272–298, indice mono + glifo, titolo serif 24 px 400, link-arrow 13 px / 2 col |
| Processo a 390 / 768 / 1024 | verticale sul telefono | verticale / verticale / orizzontale | lista verticale + figura statica di 178 px (decorativa) / idem / idem | verticale con dorsale / griglia 3×2 / griglia |
| Rail 2.0 a 390 (dashboard) | verticale, mai solo colore | verticale, 7 segmenti 318×82–120, glifo + responsabile + «Vous êtes ici» | verticale, 7 righe 62–82 px, gruppi MA/IT, glifo + responsabile + parola di stato | verticale, 7 segmenti 308×93–118, barra + numero + «Responsable : …» |
| Rail 2.0 a 768 / 1024 | — | verticale / orizzontale, segmenti **88 px**, track che sfora | verticale (40 px) / orizzontale, 123 px, track che sfora | **orizzontale già a 768**, segmenti 91 px, track che sfora / idem |
| Nav piattaforma a 390 | raggiungibile | striscia scorrevole 53 px sotto la barra (≈ 2,5 voci su 10 visibili) | lista di chip che va a capo, tutte e 10 visibili, dopo targa e rail | striscia scorrevole 36 px **a y 629**, dopo la banda del fascicolo (terza schermata) |
| Target < 24 px a 390 (home / dashboard) | 0 | **6 / 4** (link legali del footer alti 15 px; breadcrumb «Accueil» 42×20) | **0 / 0** (tutti ≥ 28 px) | **10 / 5** («ع» 20×24, 9 link del footer alti 15 px; «Accueil» 42×20) |
| Tabelle a 390 | schede | checklist a schede `data-label` ✓; nomi file `overflow-wrap: anywhere` → «language_certifi / cate.pdf» spezzato a metà parola | schede ✓ | schede ✓ |

## 2. Lock-up ufficiale (marchio / wordmark / tagline, px misurati)

Regola: marchio 38, wordmark serif 20 `.13em`, tagline 8.5 `.22em`, proporzioni intoccate. Rapporto ufficiale
marchio : wordmark = 1,9.

| Contesto | A | B | C |
|---|---|---|---|
| Header 1440 | 38 / 20 Newsreader **600** / 8.5 ✓ | 38 / 20 Newsreader **500** / 8.5 | 38 / 20 Newsreader **600** / 8.5 ✓ |
| Header 1024 · 768 | 38/20/8.5 · 38/20/8.5 (header 73) | 32/15/**—** · 32/15/**—** (tagline solo ≥ 1360) | 38/20/8.5 · 38/20/8.5 |
| Header 390 · 320 | 32/13/— · 38/—/— (solo marchio) | 32/15/— · 32/13/— | 38/14/**8.5** · 38/—/— (solo marchio) |
| Sticky 1440 · 390 | 30/16/— (fade) · 32/13/— | 32/17/— · 32/**17**/— | 38/20/8.5 · 38/14/8.5 |
| Footer 1440 · 390 | 38/20/8.5 · 32/13/**—** (la DIRECTION promette «completo») | 48/22/8.5 · 40/17/8.5 ✓ | 46 su tessera/20/8.5 · 46/20/8.5 ✓ (variante scura) |
| Barra piattaforma | 30 nudo su inchiostro (navy del marchio 1,24:1) / 15 avorio, nascosto < 768 | 38 su targhetta avorio / 13–16 avorio | 40 su tessera / 15 avorio, nascosto ≤ 720 |
| Rapporto a 390 | 2,46 | 2,13 (sticky 1,88 ✓) | 2,71 |

La tagline non scende mai sotto 8.5 px in nessuna direzione (quando è mostrata). Nessuna direzione scala il
lock-up come unità: A e B riducono il marchio, C riduce solo il wordmark. Il vincolo «tagline ≥ 8.5» rende
impossibile una riduzione proporzionale con tagline (38→32 darebbe 7,2 px): la scelta corretta è tenere 38/20/8.5
finché entra, poi passare al solo marchio; C è la più vicina, A la più lontana (solo marchio già a 320).

## 3. Sistema tipografico (stili calcolati a 1440, home + dashboard)

| Prova § 6 | A | B | C |
|---|---|---|---|
| Tre voci | Fira Sans / Newsreader / Fira Mono ✓ | idem ✓ | idem ✓ |
| Compagni arabi | `[dir=rtl]` scambia i token (non `:lang(ar)`) | `:lang(ar)` scambia famiglie, tracking 0, `min-width` bottoni ✓ | `:lang(ar)` famiglie, tracking 0, interlinea 1.8/1.35/1.2, peso 400 sul display, niente maiuscole, opacità 1 ✓✓ |
| Pesi in uso | Sans 400/500/600/**700**, serif 300/400/500/600/**700**, mono 400/500 (11 combinazioni) | Sans 400/500, serif 200/260/300/500 (`opsz` 72/48), mono 400 (7) — **nessun 600/700** | Sans 400/500/600, serif 300/400/600/**700**, mono 400/500 (9) |
| 700 nei titoli | **6 H3 `.proc__title` + 2 `small`** (nessun peso dichiarato → bold dello UA) | 0 ✓ | **2 H3** `.focus-card__title`, `.pilot-card__title` (stesso errore per omissione) |
| Dimensioni distinte (home / dashboard) | **18** / 12, con **8 px** (×2), 8.5, 10, 11 | 17 / 13 (token 88/56/36/26 + 40/28/23/22/19/14/11 nei componenti) | 16 / **9**; scala token a 10 gradini ma 13.5 (×8), 10, 30, 40 fuori scala |
| Interlinee | unitless 1.04/1.08 → 67.6, 51.84 px (fuori griglia) | in px, quasi tutte multiple di 4 (88/60/44/40/36/32/28/24/20/16) ✓ | unitless 0.98–1.5 → 51.84, 35.84, 26.4, 20.15 (fuori griglia) |
| Tracking negativo | display −.012em ≥ 36 px ✓ | −.012em solo ≥ 44 px (−1.056 px a 88) ✓ | −.015em ≥ 40 px (−1.5 px a 100) ✓ |
| Etichette maiuscole | **16** combinazioni tracking@size (.04–.22em) | 11 | 12; ma Fira Mono è il **41 %** degli elementi di testo (53/129; 36 % nel cruscotto: anche gli eyebrow H2) |
| Righe (cpl a 1440) | mediana 56, max 68 ✓ | mediana 56, max 68; **rail caption 93** nel cruscotto | mediana 43, max 68 ✓ |
| Cifre tabellari | `tnum` globale: 10/10 ✓ | solo `.t-mono`: **16/17 home, 25/25 cruscotto** senza tabular (date in `time`, ordinali 01–04) | `tnum` globale: 15/15 ✓ |
| H1 | titolo bloccato in Fira Sans 600 20→32 px `.14em` (più piccolo del display serif 65 px) | titolo bloccato in Newsreader 260 `opsz` 72, 88 px (44 a 390, 35 a 320) | titolo bloccato in Newsreader 300, 100 px (52 a 390), ™ a 0.4em |
| Wordmark | Newsreader 600 ✓ fedele | Newsreader 500 (più leggero dell'originale) | Newsreader 600 ✓ fedele |

Font caricati ovunque: Fira Sans 400/500(/600), Fira Mono 400, Newsreader variabile 200–800 (+ corsivo). Nessuna
pagina carica le famiglie arabe (corretto: sono dichiarate in `fonts.css` e attivate solo da `dir`/`lang`).

## 4. Giudizio per direzione

### A — Rete luminosa · MOBILE 6/10 · TIPOGRAFIA 5/10
Composizione mobile intenzionale: la scena diventa quadrata, la rete è ritagliata con `slice` e perde le nove
etichette, la porta fa da copertina, il bus delle vie diventa verticale, il processo ha la spina, il rail 2.0 è
verticale con «Vous êtes ici», la nav della piattaforma sta subito sotto la barra. Ma la prima schermata a 390 è
110 px di chrome + porta: eyebrow e titolo cominciano a y 628 e l'hero vale 1,7 schermate; il CTA delle vie è alto
32 px; sei link del footer sono alti 15 px; i nomi dei documenti si spezzano a metà parola; a 1024 il rail 2.0
comprime i segmenti a 88 px. Tipografia: tre voci vere e cifre tabellari globali, ma il sistema non ha autorità:
11 combinazioni di peso, sei titoli di stazione in Newsreader 700 per omissione, testo a 8 px, 18 corpi, 16
tracking diversi per le etichette. È il prototipo con più idee mobili e con meno disciplina.

### B — Profondità architettonica · MOBILE 5/10 · TIPOGRAFIA 8/10
Ingegneria impeccabile: zero overflow, zero target sotto 24 px (tutti ≥ 28), chip di navigazione che vanno a capo
senza scorrere, tabelle a schede, gutter 16, interlinee su griglia. Ma sul telefono è desktop impilato: la porta
ufficiale — l'asset che il committente vuole al centro — è scalata a 260 px e inizia a y 838 su 844, cioè non
esiste nella prima schermata; le quattro soglie sono quattro card da 350 px in fila (1,4 k px); la figura in
sezione del processo a 178 px è decorativa; a 1024×768 l'hero vale 152 % perché il breakpoint impila troppo presto;
l'header non si compatta e la regola sticky ingrandisce il wordmark da 15 a 17 px proprio sul telefono. Tipografia:
è l'unica direzione che supera il test § 6 sui pesi (niente 600/700, 260/300 con asse ottico) e sulla scala delle
interlinee; `:lang(ar)` c'è. Mancano le cifre tabellari fuori da `.t-mono` (25/25 numeri del cruscotto), la
tagline sparisce dall'header sotto 1360 px, una didascalia arriva a 93 caratteri, e il wordmark a 500 è più
leggero dell'originale.

### C — Diplomazia contemporanea · MOBILE 7/10 · TIPOGRAFIA 7/10
La composizione mobile è la più convincente: header 56 px con lock-up 38 + tagline 8.5 conservata, porta intera
come copertina con didascalia in francese, titolo a 52 px in due righe, striscia coordinate ricomposta a due
colonne, stazioni verticali con dorsale, rail 2.0 verticale con «Responsable : …», footer con lock-up completo su
tessera. Difetti: **overflow orizzontale a 1024×768** (nav collassa solo ≤ 900 px), la nav della piattaforma è
relegata a y 629 dopo la banda del fascicolo, il rail 2.0 diventa orizzontale già a 768 con segmenti di 91 px e
track che sfora, dieci target sotto 24 px (la «ع» è larga 20 px), l'hero a 1024 vale 152 %. Tipografia: il set
arabo più completo, cifre tabellari globali, cruscotto disciplinato (9 corpi), display a 100 px con tracking
corretto; ma due H3 scivolano a 700 per omissione, il mono occupa il 41 % del testo (anche gli eyebrow dei titoli),
quattro corpi sono fuori dalla scala dichiarata e le interlinee unitless escono dalla griglia.

## 5. Must-fix con evidenza

**A**
1. Chrome a 390: header 73 + barra 37 = 110 px → header ≤ 56, barra AGAMI nel cassetto (`a_home_390x844_fold.png`).
2. Hero 171 % con H1 a y 628 → scena ≤ 260 px o titolo nella piega (`metrics.json` a_home_390 `hero.pctOfViewport`).
3. `.proc__title` senza peso → Newsreader 700 su 6 stazioni: dichiarare 400 (`type.weightsGe700InHeadings`).
4. Testo a 8 px (2 elementi) e 10–11 px diffusi → niente sotto 11; 16 tracking di etichetta → 3.
5. Sei link del footer alti 15 px, «Accueil» 42×20, CTA delle vie 280×32 → `min-height` 28/44 (`targets.worst`).
6. `.doc__name { overflow-wrap: anywhere }` spezza «language_certifi/cate.pdf» → rottura su `_` e `.` o ellissi.
7. Striscia della nav piattaforma: 2,5 voci su 10 senza affordance di scorrimento → gradiente di taglio o chip a capo.
8. Rail 2.0 a 1024: segmenti 88 px e track che sfora → verticale fino a 1023 (`rail2.trackScrollX`).
9. Footer a 390 perde tagline e riduce il marchio (32/13/—) contro la DIRECTION § 2.1.

**B**
1. Porta sotto la piega a 390 (y 838/844) → porta come copertina prima dell'H1 o hero ≤ 930 px (`b_home_390x844_fold.png`).
2. Header 61 → 56; `.header[data-floating] .lockup__wm { 17px }` scavalca il 15 px mobile → limitare ≥ 1101 px.
3. Tagline nascosta nell'header da 1359 px in giù → mostrarla almeno fino a 768 (`locks[0].tag.vis`).
4. Numeri non tabellari: `time`, `seuil__ordinal`, `seg__num` → `font-variant-numeric: tabular-nums` globale.
5. `p.rail__caption` a 93 caratteri per riga a 1440 → `max-inline-size: 60ch` (`lines.top`).
6. Hero 152 % a 1024×768: tenere due colonne fino a 1024 incluso.
7. Gutter 14 px a 320 → 16. 8. Rail 2.0 a 1024: 123 px e track che sfora. 9. Figura del processo a 178 px sul telefono: nasconderla o ridisegnarla verticale.

**C**
1. **Bloccante**: `scrollWidth` 1155 a 1024×768 → collasso della nav a ≤ 1100 px (`c_home_1024x768_fold.png`, «Pr» tagliato).
2. `.focus-card__title`, `.pilot-card__title` senza peso → 700: dichiarare 400.
3. Dieci target < 24 px a 390: «ع» 20×24 e nove link del footer alti 15 px → 28 px minimi.
4. Nav della piattaforma a y 629, dopo la banda: portarla sotto la barra (come A) o rendere la banda comprimibile.
5. Rail 2.0 orizzontale già a 768 con segmenti di 91 px → verticale fino a 1023; a 1440 i segmenti sono 86 px in una colonna da 650: valutare due righe.
6. Hero 152 % a 1024: il breakpoint impila troppo presto (a 1024 la piega mostra solo la porta).
7. Corpi 13.5 / 10 / 30 / 40 fuori dalla scala dichiarata; interlinee unitless → griglia 4 px.
8. Fira Mono al 41 % del testo (eyebrow H2 compresi) → mono solo per riferimenti, date, coordinate, codici.
9. Gutter 14.3 a 320 → 16.

## 6. Classifiche

**MOBILE**: 1. C (7) — 2. A (6) — 3. B (5).
C è l'unica con header a 56 px, lock-up con tagline sul telefono e porta-copertina intera; deve però risolvere
l'overflow a 1024 e la posizione della nav. A ricompone davvero (rete ritagliata, bus verticale) ma paga 110 px di
chrome, 171 % di hero, target piccoli e testo a 8 px. B è la più solida tecnicamente ma sul telefono è desktop
impilato con la porta fuori dalla prima schermata: non «wow», e non è quello che la brief chiede.

**TIPOGRAFIA**: 1. B (8) — 2. C (7) — 3. A (5).
B ha l'unico sistema che passa il test § 6 sui pesi e sulle interlinee (260/300 con `opsz`, mai 600/700, griglia
4 px, `:lang(ar)`); le cifre tabellari e la tagline nell'header sono correzioni di un'ora. C ha il set arabo più
completo e il cruscotto più disciplinato ma lascia entrare il 700 per omissione e fa del mono una seconda voce
principale. A ha tre voci e `tnum` globale ma nessuna scala: 18 corpi, 11 combinazioni di peso, 700 su sei
titoli, 8 px.

**Raccomandazione di sintesi**: la composizione mobile di C con il sistema tipografico di B (pesi 260/300/400/500,
interlinee in px multiple di 4, `tabular-nums` globale, `:lang(ar)` di C), il lock-up tenuto a 38/20/8.5 finché entra
e poi solo marchio, header ≤ 56 con barra istituzionale nel cassetto, rail 2.0 verticale fino a 1023 in tutte e tre.
