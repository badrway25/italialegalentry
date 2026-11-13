# ASSET UFFICIALI — logo e «porta» del sito attuale

Stato: **ORIGINALI RECUPERATI** · Fonte: legalitalentry.it, ispezionato in sola lettura il
23 settembre 2026 · Vincolo del committente: questi due elementi restano l'identità del progetto e
hanno priorità su qualunque componente 21st.dev, preset di UI-UX-Pro-Max o sfondo generico.

---

## 1. Il logo

### Dove stava

`legalitalentry.it/`, `nav.main > a.lock`: un `<svg class="mark" viewBox="0 0 200 200">`
**inline** nell'HTML della pagina (non un file: il tema WordPress `italy-template` lo scrive nel
markup), seguito dal wordmark in testo.

### Che cos'è

Un marchio vettoriale in quattro parti, tutte geometriche:

| Parte | Geometria | Colore |
|---|---|---|
| due piani laterali | `polygon 26,16 80,44 80,166 26,178` e speculare | verde `#157A3C` a sinistra, rosso `#C4142B` a destra |
| la porta ad arco | `path M76,156 L76,104 a24,24 0 0 1 48,0 L124,156 Z`, tratto bianco 5 | navy `#0F2547` |
| la chiave | anello r 8 con foro r 3.4, gambo 4.8 × 30, due denti 8 × 4 e 6 × 4 | oro `#C39A2B` (foro navy) |
| tre gradini | 56, 68, 80 × 5 a y 160/167/174 | navy `#0F2547` |

Lock-up sul sito attuale: marchio 38 × 38 px + wordmark «ITALY LEGAL ENTRY» nel serif display,
maiuscolo, tracking `.13em`, 20 px, con «Italy» verde, «Legal» navy, «Entry» rosso + una riga di
tagline in inglese, 8,5 px, tracking `.22em`, grigio. Nel piè di pagina il wordmark è bianco su navy.

### ⚠ La tagline NON viene riprodotta — conflitto fra due istruzioni del committente

Il **documento d'implementazione** del committente (p. 7 §3.1) ordina di eliminare quella riga
«ovunque, incluso alt/ARIA del logo» (registro: `docs/CONTENT_SOURCE_MAP.md` F14), ed è nella lista
delle formulazioni vietate di `apps/cms/forbidden.py`, verificata da
`apps/pages/tests/test_institutional.py` su ogni pagina pubblica in ogni lingua. La **direttiva di
rebase visivo** §2 dice, testualmente, che un ridisegno non autorizza modifiche alle «prohibited
wording». L'**addendum del 23 settembre 2026** ripristina il *marchio* e l'*immagine* della porta e
non dice nulla di quella riga di testo.

Risoluzione adottata, e la linea è fra **immagine** e **parole**:

| | Decisione | Perché |
|---|---|---|
| marchio (arco, chiave, gradini, piani tricolore) | **riprodotto verbatim** | l'addendum è posteriore e riguarda esattamente questo |
| fotografia dentro l'arco, arco, chiave, gradini | **riprodotti** | idem: è immagine, ed è del titolare |
| tagline inglese sotto il wordmark | **non riprodotta** | è *parola*, è vietata dal documento del committente stesso, e §2 me lo impedisce |
| didascalia «A doorway, not a shortcut» sotto la porta | **non riprodotta** | stessa ragione (F13). Tradurla in francese sarebbe aggirare il divieto, non rispettarlo |

Se il committente vuole indietro la tagline o la didascalia, il documento che deve cambiare per
primo è quello d'implementazione: allora si aggiornano `apps/cms/forbidden.py`,
`docs/CONTENT_SOURCE_MAP.md` e questo paragrafo, in quest'ordine. **Non è una dimenticanza: è una
decisione, ed è reversibile in un commit.**

Animazioni originali sul marchio: `logoKeyShimmer` (la chiave sale di 2 px e si illumina, 3,5 s in
loop) e `:hover` con `scale(1.08) rotate(-3deg)` su curva con overshoot `(.34,1.56,.64,1)`.
**Non riportate** in V2: il loop su `filter: drop-shadow` è costoso e l'overshoot è nella lista dei
segnali «premium a buon mercato» dei benchmark. Il marchio in V2 è fermo; se si muove, si muove
una volta, all'ingresso, con transform/opacity.

**Emendamento V5.4 (DL54-07, 4 ottobre 2026; costruito da W1-D l'8 ottobre):** una volta, all'ingresso, *attraverso il
caricamento della pagina* — all'invio del login la chiave gira una volta sul proprio gambo e tiene; sulla prima pagina
della console dopo un accesso riuscito la porta si illumina dall'occhio della chiave, una volta per sessione, e torna al
marchio verbatim. È l'unico altro contesto; piani, porta e gradini non si muovono mai e la chiave non è mai tenuta,
disegnata o servita specchiata (DL54-08). `docs/design-v5/DECISION_LOG_V54.md` DL54-07; il marchio a strati in
`templates/components/loader.html`.

### Dove sta ora

| Cosa | Percorso | Note |
|---|---|---|
| originale, verbatim | `static/brand/original/logo-mark.svg` | geometria e colori intoccati; aggiunti solo `<title>` e `role="img"` |
| lock-up originale (markup) | `docs/design-v2/brand-original/logo-lockup.html` | evidenza |
| screenshot originale | `docs/design-v2/brand-original/legacy_logo_lockup.png` | evidenza |
| versioni V2 (header, sticky, mobile, piè di pagina, auth, piattaforma, favicon) | *da produrre in fase 6/8* | proporzioni invariate; variante per fondo scuro solo se necessaria |

Il favicon attuale del nuovo progetto (`static/img/favicon.svg` + `.ico`) è stato disegnato prima di
recuperare il marchio e **va allineato a questo** in fase 6.

Nota di palette: il marchio porta verde e rosso — è il tricolore, ed è del committente. Vale per
il marchio, non per la palette del sito: la direttiva chiede di evitare il tricolore «ovunque», e
i benchmark confermano che rosso e verde decorativi leggono «bandiera». Il marchio resta l'unico
punto in cui i due colori convivono.

---

## 2. La «porta» (`arch-photo-bg`)

### Che cos'è davvero

Non è un file SVG. È una **composizione CSS** che il tema chiama «portal illustration», nell'hero
della home, colonna destra (`.hero-grid > .portal.rv > .arch`). Cinque strati, dal fondo:

| Strato | Markup / regola | Cosa fa |
|---|---|---|
| l'arco | `.portal .arch` — `border-radius: 190px 190px 0 0`, `aspect-ratio: 3/4`, max 380 px, gradiente sabbia → carta, filetto; `::before` disegna un secondo arco interno rientrato di 16 px | la cornice a tutto sesto |
| la fotografia | `.arch-photo-bg > img.arch-bg-img` — `object-fit: cover`, **opacità .28**, `saturate(1.2) contrast(1.1)`, `scale(1.04)`; `.arch-overlay` = vignetta radiale trasparente → navy .85 | la facciata di una fontana monumentale romana, sfumata dentro l'arco |
| la porta interna | `.inner` — arco navy al 52 % della larghezza, `aspect-ratio 1/1.55`, ombra 22/50 | il vano scuro |
| la chiave | `<svg viewBox="0 0 60 130">` dentro `.inner`, 34 % della larghezza, oro `#C39A2B` | **la stessa chiave del logo**, in scala |
| i gradini | `.steps > i × 3` — barre navy 66 / 80 / 94 %, opacità .30 / .22 / .14 | i tre gradini del logo, in scala |
| la didascalia | `.cap` — mono 10 px, tracking `.2em`, «A doorway, not a shortcut» | il concetto |

Dinamica originale: reveal all'ingresso (`.rv`: opacità 0 → 1 e `translateY(14px)` → 0 in 600 ms,
via `IntersectionObserver`, soglia .12, ritardo scaglionato di 70 ms; `prefers-reduced-motion`
rispettato); la chiave **levita** (`keyInfiniteLevitate`, 3,6 s) e **brilla** (`keyGlow`, 2,8 s,
`drop-shadow` animato); al passaggio del mouse l'arco sale di 4 px, la foto passa a .42 e
`scale(1.1)` in 1,2 s, la porta interna sale e si illumina d'oro, i gradini si accendono uno a uno.
Sotto 900 px l'arco passa a 250 px e sale **sopra** il testo (`order: -1`).

Il concetto è esatto: **una porta, non una scorciatoia** — l'arco è l'ingresso regolare, la chiave
è ciò che lo apre, i gradini sono il percorso. Ed è la stessa grammatica del marchio: arco +
chiave + gradini. È per questo che vale come firma visiva, e non solo come decorazione.

### La fotografia

Autore: **il titolare del progetto** (dichiarato in sessione il 23 settembre 2026). Nel sito
attuale è servita dal CDN di Unsplash (`photo-1525874684015-58379d421a52`, 800 × 533); qui è stata
scaricata a 2400 px (`docs/design-v2/brand-original/arch-photo-original-2400.jpg`, 949 KB) e
**non verrà mai più richiesta al CDN** né al sito legacy a runtime. Per la versione servita si
chiede al titolare il file master, da cui produrre AVIF/WebP responsive sotto i 120 KB per viewport.
Registrata in `docs/IMAGE_LICENSES.md`.

### Dove sta ora

| Cosa | Percorso |
|---|---|
| markup originale | `docs/design-v2/brand-original/portal.html` |
| CSS originale (41 regole e keyframe, verbatim) | `docs/design-v2/brand-original/portal.css` |
| JS del reveal originale | `docs/design-v2/brand-original/reveal.js` |
| la chiave, verbatim | `static/brand/original/key.svg` |
| screenshot originali (arco desktop/mobile, hero desktop/mobile) | `docs/design-v2/brand-original/legacy_*.png` |
| **`enhanced-v2`** | *in costruzione nei prototipi di direzione (`docs/design-v2/directions/*/`), poi in `static/brand/v2/`* |

### Che cosa può cambiare in V2, e che cosa no

Può: profondità, path che si disegnano (`pathLength` su arco e gradini), rivelazione della chiave,
progressione legata allo scroll, luce e gradienti, parallasse minima, bagliore elegante, prospettiva,
micro-movimento, composizione mobile propria (ritaglio, viewBox, quantità di elementi).
Non può: perdere l'arco, la chiave, i gradini o la fotografia dentro l'arco; diventare una PNG;
usare loop su `filter`; usare curve con overshoot; restare invisibile con «riduci movimento».

Prestazioni: l'originale anima `filter: drop-shadow` in loop su due elementi e `transform` sulla
foto in hover con `transition 1.2s`. In V2 il bagliore è uno strato pre-disegnato animato in
opacità; nulla anima fuori dal viewport; con `prefers-reduced-motion` la composizione è completa e
ferma.

Accessibilità: decorativa, `aria-hidden="true"` (come nell'originale); la didascalia, se
mantenuta, è testo reale e leggibile, non `aria-hidden`.

---

## 3. Evidenze richieste nel rapporto finale (§ 11 dell'addendum)

| Voce | Dove |
|---|---|
| percorso originale del logo | inline in `legalitalentry.it/` (`nav.main > a.lock > svg.mark`) |
| percorso locale nuovo | `static/brand/original/logo-mark.svg` → `static/brand/v2/…` |
| origine di `arch-photo-bg` | hero della home, colonna destra; tema `italy-template` `style.css` v1.0.0 §«HERO ARCHWAY PHOTO INTEGRATION» |
| tecnologia | CSS (arco, vignetta, gradini) + `<img>` + SVG inline (chiave) + JS (`IntersectionObserver`) |
| screenshot originale | `docs/design-v2/brand-original/legacy_arch_desktop.png`, `legacy_arch_mobile.png` |
| screenshot V2 | *dopo la scelta della direzione* |
| modifiche apportate | *sezione «Asset ufficiali» di `directions/<scelta>/DIRECTION.md`, poi qui* |
| comportamento mobile / reduced-motion / prestazioni | *verificati in Chrome visibile prima di dichiarare l'hero completo* |
