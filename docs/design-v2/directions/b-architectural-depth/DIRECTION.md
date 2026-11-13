# DIREZIONE B — LEGAL TECHNOLOGY / PROFONDITÀ ARCHITETTONICA

*Design Council V2 · ITALY LEGAL ENTRY™ · 23 settembre 2026 · prototipo in questa cartella:
`home.html`, `dashboard.html`, `styles.css`, `main.js`, `head.js`, `shots/`.*

## 1. Concetto in dieci righe

1. La piattaforma è **una struttura di diritto costruita**: piani, soglie, camere. Non un ministero, non una startup: uno studio legale internazionale del 2026.
2. La tela è **avorio caldo** (`#F8F5EE`); l'inchiostro è **tinto di navy-petrolio** (`#14212B`), mai nero.
3. La profondità nasce da **piani sovrapposti, hairline, gradini tonali e luce** — sette livelli di superficie, ombre solo per ruolo (card, hover, popover, modale).
4. Il buio esiste solo come **camera**: l'interno della porta nell'hero, il capitolo del processo, la barra della piattaforma. Il resto è avorio.
5. Due accenti con due mestieri: **petrolio** (`#0F5C63`) per il territorio, le sezioni e gli stati — mai interattivo; **un solo blu luminoso** (`#1F45D6`) per link, CTA e focus.
6. Tipografia: **serif display sottile** (Newsreader 260–300, asse ottico) contro un **grotesk preciso** (Fira Sans 400/500) e un mono per riferimenti e date.
7. L'hero è la **porta ufficiale del committente** — arco, fotografia, chiave d'oro, tre gradini — evoluta come *soglia architettonica*: piani che entrano in registro, contorno tracciato, chiave che sale dai gradini.
8. Le quattro vie sono **quattro soglie** in una fila a gradoni; il processo è **un disegno in sezione** — sei livelli dal BESOIN all'INCLUSION — appuntato accanto ai capitoli che lo illuminano.
9. Il moto ha una grammatica sola: *mise en registre* (i piani scivolano al loro posto), *soglia che si apre*, *tracé* (una linea che si disegna). Tre curve, quattro durate, nessun overshoot, `prefers-reduced-motion` come stato di prima classe.
10. La piattaforma condivide tutto: il fascicolo si apre con la **targa del dossier** su due piani e il **rail di responsabilità 2.0** — chi risponde di cosa, Marocco e Italia, glifo di ruolo, attore attuale.

## 2. Palette come token CSS (rapporti di contrasto calcolati, formula WCAG 2.x)

Tutti i valori sono in `styles.css` (`:root`). Le misure sono state calcolate con uno script (luminanza relativa sRGB), non a occhio.

### Piani (chiaro)

| Token | Valore | Ruolo | Contrasto |
|---|---|---|---|
| `--plane-0` | `#F8F5EE` | canvas | — |
| `--plane-1` | `#EFEBE1` | area / piani retrostanti | gradino 1.09 (tonale) |
| `--plane-2` | `#FCFAF5` | pannelli, righe | — |
| `--plane-3` | `#FFFFFF` | elevato: menu, segmento attuale | — |
| `--hairline` | `#DDD6C8` | ritmo 1 px | 1.33 (decorativo) |
| `--rule` | `#8C8474` | confine strutturale 1 px, segmenti "a venire" | **3.40** su canvas · 3.11 su area (UI ≥ 3) |

### Camere (scuro, mai nero)

| Token | Valore | Contrasto sulla camera |
|---|---|---|
| `--chamber-0/1/2` | `#0F1E2B` · `#142636` · `#1B3040` | gradini 1.10 (tonali) |
| `--chamber-line` | `#2C4152` | 1.60 — solo hairline decorativa |
| `--chamber-line-ui` | `#607B8F` | **3.81** su chamber-0 · 3.48 su chamber-1 (contorni dei piani nel disegno) |
| `--on-chamber` | `#F3EFE6` | **14.75** |
| `--on-chamber-2` | `#B4BEC7` | **8.97** · 7.21 su chamber-2 |
| `--petrol-on-chamber` | `#7CC5C5` | **8.58** (tracé, eyebrow) |
| `--lumen-on-chamber` | `#A6BBFF` | **9.00** (link e focus nel buio) |

### Inchiostro e accenti (su canvas `#F8F5EE`)

| Token | Valore | Contrasto | Uso |
|---|---|---|---|
| `--ink` | `#14212B` | **15.04** | testo |
| `--ink-2` | `#3F4B56` | **8.20** | testo secondario |
| `--ink-3` | `#5C6873` | **5.24** · 4.79 su area | didascalie, folio, tagline del lock-up |
| `--petrol` | `#0F5C63` | **7.06** · 6.46 su area | eyebrow, stati "fatto", giurisdizione MA — non interattivo |
| `--petrol-ui` | `#2E7C82` | **4.46** | filetti, meter, bordi (UI ≥ 3) |
| `--lumen` | `#1F45D6` | **6.70** · bianco su lumen **7.29** | l'unico blu interattivo |
| `--lumen-hover` | `#1736B3` | **8.71** · bianco **9.48** | hover |
| `--bronze` | `#8A6A3D` | **4.58** · 4.78 su plane-2 | filetto dei documenti |

### Scala delle vie (una tinta per soglia)

`--route-1` petrolio `#0F5C63` **7.06** · `--route-2` navy-inchiostro `#1F3A57` **10.71** · `--route-3` pietra `#6B5535` **6.48** · `--route-4` ardesia `#3E5462` **7.28**.

### Stati (fg su bg ≥ 4.5 · bordo su canvas ≥ 3)

| Stato | fg / bg / bordo | fg:bg | bordo:canvas |
|---|---|---|---|
| à faire | `#6B4A0C` / `#F5E9CF` / `#A88232` | **6.68** | 3.27 |
| terminé | `#0F5C63` / `#D9E8E6` / `#2E7C82` | **6.09** | 4.46 |
| info | `#2C4A6E` / `#E2E9F1` / `#5F84B5` | **7.42** | 3.54 |
| attention | `#7A3A0E` / `#F8E5D6` / `#B0703A` | **7.04** | 3.69 |
| erreur | `#8F2424` / `#F8E0DE` / `#C4635F` | **6.83** | 3.64 |
| non analysé | `#5E4B14` / `#F3ECD8` / `#A08A46` | **7.14** | 3.10 |

Il colore non è mai da solo: ogni chip porta testo + pallino, ogni segmento del rail porta glifo + parola ("Terminée / Étape actuelle / À venir").

### Marchio ufficiale (usato verbatim, vedi § 13)

`--brand-navy #0F2547` **14.02** · `--brand-green #157A3C` **4.97** (4.55 su plane-1) · `--brand-red #C4142B` **5.54** (5.07) · chiave `#C39A2B` su navy del marchio **5.80**. Il grigio della tagline originale `#6B7280` misura 4.44 su avorio: nel prototipo la tagline usa `--ink-3` (5.24) — stesso tono, un gradino più scuro.

## 3. Tipografia

| Voce | Famiglia (prototipo) | Pesi | Dove |
|---|---|---|---|
| Display | **Newsreader** (variabile, asse `opsz` 6–72) | 260 targa · 300 titoli e bande · 200 ordinali · 300 corsivo per il lead | H1 88/64/44 px, H2 56/44/34, bande 36/30/26, ordinali 64 |
| UI / prosa | **Fira Sans** | 400 · 500 (600 mai nei titoli) | corpo 17/28, UI 15/20, folio 12 tracciato .1em |
| Riferimenti | **Fira Mono** | 400, cifre tabellari | numeri di dossier, date, capitoli, "Étape 2 sur 7" |
| Arabo | **Noto Naskh Arabic** (display) · **IBM Plex Sans Arabic** (UI) | 400–700 · 400/500/600 | `:lang(ar)` cambia famiglie e azzera il tracking |

Regole: interlinee multiple di 4 px; misura ≤ 60 caratteri (`max-width: 58ch`); tracking negativo solo ≥ 44 px (−.012em) e 0 in arabo; maiuscole tracciate solo nel folio/eyebrow e nei testi prescritti che sono già maiuscoli (le quattro vie, il Forum).

**Proposta oltre il prototipo** (da valutare con licenza): come grotesk "precisa" al posto di Fira Sans, *Suisse Int'l* (con Suisse Int'l Arabic) o, in open, *Instrument Sans*; come serif display sottile, *Newsreader* regge bene l'asse ottico e non va sostituito. Il lock-up ufficiale chiede un serif per il wordmark: nel prototipo è Newsreader 500 (l'originale usa 600 in una famiglia non dichiarata).

## 4. Scala di profondità — sette livelli, un token ciascuno

| Livello | Nome | Chiaro | Camera | Ombra / materiale |
|---|---|---|---|---|
| 0 | canvas | `--plane-0` | `--chamber-0` | nessuna |
| 1 | area / piano retrostante | `--plane-1` + hairline | `--chamber-1` | nessuna: è il gradino tonale (le targhe del fascicolo, il piano dietro la porta) |
| 2 | interattivo | `--plane-2` + hairline | `--chamber-2` + `--chamber-line` | `--sh-card` a riposo, `--sh-hover` + `translateY(−4px)` in hover (le soglie) |
| 3 | elevato | `--plane-3` | `--chamber-2` | `--sh-popover` (menu lingua, menu account); vetro solo sulla barra sticky |
| 4 | focus | anello 2 px `--lumen` + alone 6 px al 30 % | `--lumen-on-chamber` | — |
| 5 | overlay | `--plane-3` + scrim | — | `--sh-modal` (non usato nel prototipo) |
| 6 | immersivo | la porta (fotografia + camera navy) | capitolo del processo | il solo `backdrop-filter` è sull'header sticky |

`grep box-shadow styles.css` restituisce i quattro ruoli, il tracé della porta e l'ombra dell'arco interno originale (mantenuta dal committente).

## 5. Vocabolario di moto

**Curve (tre)**: `--e-in cubic-bezier(.25,1,.5,1)` entrata · `--e-out cubic-bezier(.7,0,.3,1)` uscita · `--e-std cubic-bezier(.4,0,.2,1)` bidirezionale. Nessun overshoot: la curva `(.34,1.56,.64,1)` del sito attuale è stata eliminata.
**Durate (quattro + una)**: 120 ms micro-stato · 180 ms hover/entrata · 240 ms reveal · 320 ms piani in registro · **960 ms** solo per il *tracé* nel capitolo immersivo (hero) · loop ambientale unico: il respiro dell'alone della chiave, 24 s, lineare, solo opacità.

| Nome | Funzione | Innesco | Cosa si muove | Durata / curva | Ridotto |
|---|---|---|---|---|---|
| Titolo a maschera | gerarchia | load | ogni riga dell'H1 `translateY(105%→0)` in un contenitore `overflow:hidden` | 320 ms · e-in · stagger 70 | testo già in posizione |
| Mise en registre | profondità | load / inView | piani avorio retrostanti (`translate(−24,−16)→0`), targhe della piattaforma (`y 8→0`), le quattro soglie (`y 24→0`) | 320 / 240 ms · e-in · stagger 40–70 | stato finale |
| Tracé | orientamento | load (hero) · scroll (processo) | `stroke-dashoffset 1→0` su `pathLength="1"`: contorno dell'arco, poi il percorso nel disegno in sezione | 960 ms lineare (hero) · scroll-linked via `scroll()`/ScrollTimeline (processo) | linea completa |
| Soglia che si apre | feedback | hover / focus | la cornice interna della card passa da `inset:12px` a `8px`, l'architrave sale 4 px, la card si alza 4 px | 180 ms · e-in | senza transizione |
| Porta che si costruisce | causalità | load | piano → contorno → luce (fotografia) → arco interno sale 28 px → chiave sale 26 px sotto l'alone → tre gradini `scaleX 0→1` → didascalia | 320 ms per passo · e-in · scaletta 120→1560 ms | porta completa e ferma |
| Capitolo che illumina | stato | inView (amount .4, finestra 12–62 % del viewport) | riempimento e etichetta del livello n, filetto petrolio del capitolo `scaleY` | 240 ms · e-std | istantaneo |
| Parallasse controllata | profondità | scroll (solo ≥ 1025 px) | fotografia `y 0→26px`, chiave `y 0→−14px` mentre l'hero esce dal viewport | lineare, ScrollTimeline | nessuna |
| Header che si stacca | orientamento | scroll > 8 px | sfondo → vetro, hairline, lock-up compatto (38→32 px) | 180 ms · e-std | idem (non è moto) |
| Cassetto mobile | causalità | tocco | `opacity 0→1, y −8→0`; Escape chiude e riporta il focus | 240 / 180 ms | `hidden` toggle |

**Stato ridotto**: ogni animazione passa da `withMotion(fn, settle)` (`static/js/src/motion.js`); gli stati iniziali nascosti esistono in CSS solo sotto `.js` **e** `prefers-reduced-motion: no-preference`; con "riduci movimento" la pagina è completa al primo paint, il tracé è disegnato, la porta è costruita, la barra di lettura è nascosta. Senza JavaScript (`.no-js`) nulla è mai nascosto. Un timer a 4 s (`motion-done`) forza lo stato finale in ogni caso.
**Budget**: solo `transform`, `opacity` e `stroke-dashoffset`; nessun `filter` animato (il `drop-shadow` in loop dell'originale è sostituito da un alone pre-renderizzato in `radial-gradient`); nessun `will-change` permanente tranne sull'immagine parallasse.

## 6. I quattro componenti firma

### a) Hero — la struttura avorio con la porta come camera
Griglia a 12 colonne con linee di piano hairline (subgrid) visibili al di sotto del testo; a sinistra eyebrow, **ITALY LEGAL ENTRY™** (titolo prescritto, verbatim, a maschera riga per riga), lead corsivo, corpo prescritto, due CTA (una sola porta il blu luminoso), avvertenza. A destra la **porta ufficiale evoluta** (§ 13): un piano avorio-profondo fuori registro, l'arco 3:4 con contorno tracciato, la fotografia del committente nella soglia, la camera navy con la chiave che sale dai tre gradini, la didascalia mono *A doorway, not a shortcut* come testo reale. Il solo scuro dell'hero è l'interno della porta.

### b) Le quattro vie — quattro soglie in una fila a gradoni
`<ol class="seuils">`: quattro pannelli-porta, ciascuno con la propria tinta (`--route-n`), ordinale Newsreader 200 a 64 px, glifo proprietario a 1,5 px, titolo e bottone prescritti (verbatim, maiuscoli), cornice interna ad arco ribassato e **architrave** colorata. Sul desktop i pannelli salgono a gradoni (0/32/64/96 px): una scala, non quattro card. In hover/focus la soglia *si apre* (cornice che si allarga, architrave che sale, pannello che si solleva di 4 px con `--sh-hover`); il link ha equivalente tastiera. Entrano in registro con `inView` (stagger 70 ms).

### c) Processo — il disegno in sezione
Capitolo scuro unico della pagina. A sinistra, **appuntato** (`position: sticky`, nessun pinning JS), un SVG in sezione: sei piani prospettici — BESOIN · COMPÉTENCES · FORMATION · PARCOURS RÉGULIER · ENTRÉE · INCLUSION — ognuno con la propria porta, un percorso che li attraversa e un nodo finale. A destra sei capitoli con copia prescritta (p3.*), etichetta della sequenza pilota e **responsabile** con glifo di ruolo. `inView` sul capitolo imposta `data-active` sulla sezione: i livelli fino a n si illuminano (riempimento petrolio al 16 %, etichetta avorio); `scroll()` lega il tracé alla lettura. Sotto 1024 px la figura è statica, tutta illuminata, e i capitoli seguono in lista (fallback come in *Scroll 01*). Alternativa testuale: `<title>` + `<desc>` e i capitoli stessi. Didascalia: «Les proportions indiquent les étapes du modèle, non une durée.»

### d) Rail di giurisdizione / responsabilità 2.0
Nel fascicolo: **due gruppi** — *Maroc · avant le départ* (petrolio) e *Italie · procédures et inclusion* (navy-inchiostro) — sette segmenti con numero mono, etichetta del passo (JOURNEY_STEPS reali), **glifo di ruolo + attore**, stato in parole con glifo (Terminée / Étape actuelle / À venir), contatore "Étape 2 sur 7". Il segmento attuale è elevato (`--plane-3`, ombra card) e porta l'unico marcatore blu luminoso, che si disegna (`scaleX`) all'apertura. Sotto 900 px il rail diventa verticale con il marcatore laterale. Nota onesta: gli attori per segmento sono **indicativi** nel prototipo e devono arrivare da `cases.services` / Rule Engine, mai scritti a mano; la didascalia lo dichiara.

## 7. Shell della piattaforma

Non sidebar + topbar generiche ma **camera · targa · rail · piano di lavoro**:
- **Barra-camera** (56 px, `--chamber-0`): lock-up ufficiale (marchio intatto su una targhetta avorio, wordmark monocromo avorio), contesto «Contexte E46E03B461» in mono, «Site public», menu account e lingua su `<details>`.
- **Targa del dossier** su due piani (`.case__back` fuori registro): riferimento mono 30 px, Objectif, État (chip + «depuis le»), Responsable, Avancement come **conteggio + meter a cinque segmenti** (mai una percentuale non verificabile).
- **Rail 2.0** (§ 6d).
- **Piano di lavoro a tre colonne**: *indice* (216 px, sticky, voci numerate, corrente con filetto blu) · *main* (Prochaine étape come targa di prima classe con filetto petrolio; checklist élément · état · RESPONSABLE · échéance in `<table>` con caption; documenti come registro; pré-évaluation con esito, jeu de règles e nota) · *inspector* (Messages, Dates à retenir, Mon compte). Gli stati vuoti sono una hairline, il glifo dei tre gradini e una frase che dice chi li riempirà.
- Font, accento, raggi (2/4 px), ombre e curve sono gli stessi del sito pubblico (parità di piattaforma).

## 8. Composizione mobile (320 / 390 / 768)

- Header ≤ 60 px: lock-up compatto (marchio 32 px, wordmark 15→13 px, tagline nascosta), bottone **Menu** (44 px) che apre un **cassetto-soglia** a tutta altezza: navigazione in serif, **le quattro vie in lista verticale con la loro tinta**, Connexion, lock-up in coda.
- Hero: copia a una colonna, poi la porta centrata (300 → 260 px) sul suo piano retrostante; linee di piano nascoste; la parallasse è disattivata sotto 1025 px.
- Soglie: due colonne a 768, una colonna sotto; i gradoni scompaiono, l'architrave resta.
- Processo: figura statica illuminata, capitoli in lista.
- Fascicolo: targa a una colonna; rail verticale; indice come lista di chip che va a capo (tutte e dieci le destinazioni restano visibili, niente scorrimento laterale); tabella in schede (`data-label`); inspector in coda.
- Gutter 16 px, target ≥ 24 px (tutti i controlli ≥ 28 px, i bottoni 36–48 px), nessuno scroll orizzontale (verificato a 320 e 390, § 14).

## 9. Note RTL

- Solo proprietà logiche (`inset-inline`, `margin-inline-start`, `padding-inline-end`, `text-align: start`); `--origin-start` e `--flip` cambiano con `[dir="rtl"]`: la sottolineatura della nav, il marcatore del rail e le frecce si specchiano; il lock-up e il marchio no.
- `:lang(ar)` cambia le famiglie (Noto Naskh Arabic / IBM Plex Sans Arabic), azzera ogni `letter-spacing`, dà `min-width` ai bottoni.
- Da fare oltre il prototipo: le etichette SVG del disegno in sezione vanno ancorate a `text-anchor: end` e spostate a sinistra dei piani in RTL; il cassetto entra dal lato di lettura; numerali coerenti (o arabi orientali o occidentali) nel rail e nelle tabelle.

## 10. Rischi

1. **Fotografia pesante**: l'originale del committente è 2400×1600, 948 KB; il budget dice ≤ 120 KB per viewport. Servono derivati AVIF/WebP a 720/1000 px (`<picture>`), con `fetchpriority="high"` sul solo derivato dell'hero.
2. **Attori del rail e del processo**: nel prototipo sono indicativi; se il Rule Engine non li fornisce, vanno omessi, non inventati.
3. **Lock-up tricolore vs regola "niente tricolore"**: è il marchio ufficiale, quindi si usa; ma resta il solo punto in cui verde e rosso compaiono — nessun altro elemento li riprende, per non far scivolare l'identità nella bandiera.
4. **Subgrid e `color-mix`**: richiesti dal CSS delle linee di piano e delle soglie; supportati da Chromium ≥ 117 / Safari 16 / Firefox 71+; in caso di assenza il degrado è solo estetico.
5. **Capitolo appuntato**: 6 capitoli × 54 vh di scroll; su schermi bassi (768×1024 in landscape) la figura sticky può coprire i capitoli: sotto 1024 px la sezione è già statica, ma tra 1024 e 1180 px va provato con Chrome visibile.
6. **Newsreader 260** su Windows senza antialias sub-pixel può risultare sottile: da verificare su ClearType prima dell'adozione (fallback: 300).

## 11. Candidati 21st.dev esaminati (solo `search`; `get_component` per tre, a scopo di studio strutturale; nessuna generazione)

### Hero (≥ 5)
| Nome | URL | Cosa ho preso / rifiutato |
|---|---|---|
| Hero Minimalism (@lyanchouss) | https://21st.dev/@lyanchouss/components/hero-minimalism | preso: una promessa sola, zero decorazione · rifiutato: simmetria centrata |
| Minimal Centered Hero, hero-24 (@ln-dev7) | https://21st.dev/@ln-dev7/components/hero-24 | preso: gerarchia eyebrow → titolo stretto → subline · rifiutato: CTA a pillola, centratura |
| HeroGridSection (@hurerag24) | https://21st.dev/@hurerag24/components/hero-grid-section | preso: la griglia di fondo, ma **allineata alla griglia vera** (12 linee di piano in subgrid, non una texture) · rifiutato: avatar impilati (social proof finta) |
| Financial Hero (@lavikatiyar) | https://21st.dev/@lavikatiyar/components/hero-section | preso: le card sovrapposte a destra come *piani* → il piano avorio fuori registro dietro la porta · rifiutato: texture a griglia, copy SaaS |
| Hero Geometric (@componentry) | https://21st.dev/@componentry/components/hero-geometric | preso: conferma del serif + sans nel titolo · rifiutato: shader WebGL (anti-pattern § 17) |
| Hero Shutter Text (@daiwiikharihar) | https://21st.dev/@daiwiikharihar/components/hero-shutter-text | preso: l'idea della maschera di riga (una sola, 320 ms) · rifiutato: l'effetto "otturatore" |
| Hero Section Dark (@kinfe123) | https://21st.dev/@kinfe123/components/hero-section-dark | preso: il buio come capitolo · rifiutato: hero interamente scuro |
| Dotted Modern (@satoriui) · Experience Hero (@hardikkashiyani…) · Shader Hero (@beratberkayg) | catalogo | rifiutati in blocco: titolo a gradiente, griglia di punti, GSAP/WebGL "Awwwards" |

### Navigazione (≥ 5)
| Nome | URL | Cosa ho preso / rifiutato |
|---|---|---|
| **Morphing Scroll Navbar** (@laziekiki) — *studiato con get_component* | https://21st.dev/@laziekiki/components/morphing-scroll-navbar | preso: stato `atTop/direction/progress` con `requestAnimationFrame`, `aria-current="location"`, barra di avanzamento della lettura → il mio `data-floating` oltre 8 px e la hairline `--p` · rifiutato: la capsula che si restringe scendendo, le curve con overshoot `(.34,1.32,.5,1)`, lo `<style>` inline (CSP) |
| Scroll Navigation Menu (@spaceboydavey) | https://21st.dev/@spaceboydavey/components/scroll-navigation-menu | rifiutato: l'header che diventa hamburger su desktop |
| Navbar Section 2 (@solaceui) | https://21st.dev/@solaceui/components/navbar-section-2 | preso: un solo mega-pannello per le vie → il cassetto elenca le quattro soglie con la loro tinta · rifiutato: barra scura su hero chiaro |
| Motion Navigation Menu (@unlumen) | https://21st.dev/@unlumen/components/motion-navigation-menu | preso: un contenitore che si trasforma invece di N dropdown (per il futuro mega-menu) · rifiutato: molle |
| Header 1 (@efferd) | https://21st.dev/@efferd/components/header-1 | preso: blur **solo** sulla barra sticky, menu mobile animato |
| Navbar Menu (@manuarora700) · Liquid Morph Floating Menu (@aayush-duhan) | catalogo | rifiutati: "bignav" a hover, pillola organica con letter-roll |
| **Animated Sidebar** (@starc007) — *studiato con get_component* | https://21st.dev/@starc007/components/animated-sidebar | preso: il contratto di focus del pannello mobile (focus al primo link, Escape, ritorno del focus al bottone), `data-state`, l'idea dell'indice che si riduce a rail · rifiutato: molle, `filter: blur` sulle sotto-voci, icone lucide, portal |

### Processo e rail
| Nome | URL | Cosa ho preso / rifiutato |
|---|---|---|
| **Scroll 01** (@felipemenezes098) — *studiato con get_component* | https://21st.dev/@felipemenezes098/components/scroll-01 | preso: media sticky + finestra "attivo" al centro (qui `inView` con margine 12–62 %), **fallback mobile impilato** · rifiutato: dissolvenze di opacità sul testo (contrasto) |
| Features With Panel (@scrollxui) · Sticky Content Wrapper (@hyperiux) | https://21st.dev/@scrollxui/components/features-with-panel · https://21st.dev/@hyperiux/components/sticky-content-wrapper | preso: il pannello che cambia con il capitolo · rifiutato: immagini che scalano, snap |
| Vertical Descriptive Stepper (@sean0205) · Process Timeline (@shadcnui-blocks) | https://21st.dev/@sean0205/components/c-stepper-13 · https://21st.dev/@shadcnui-blocks/components/timeline-05 | preso: titolo + descrizione per passo · rifiutato: cerchi numerati a spunta (stepper orizzontale vietato dal brief) |
| Animated Progress Stepper (@shadcnspace) | https://21st.dev/@shadcnspace/components/stepper-03 | rifiutato: badge pulsante, punto viaggiante |
| Multi-Step Progress (@sean0205) · Progress Bar segmentata (@jatin-yadav05) · HeroUI Progress Bar (@hero_ui) | https://21st.dev/@sean0205/components/c-progress-7 · https://21st.dev/@jatin-yadav05/components/progress-bar · https://21st.dev/@hero_ui/components/heroui-progress-bar | preso: "n di m" accanto alla barra, segmenti discreti (il meter a 5), etichetta accessibile + output formattato → il conteggio come testo · rifiutato: colori di stato senza parola |

## 12. UI-UX-Pro-Max (v2.13.0) — cosa ho consultato

| Query (dominio) | Risposta | Decisione |
|---|---|---|
| "warm ivory canvas tinted ink teal petroleum luminous blue legal institutional" (color) | tre palette: canvas viola/teal su scuro, "warm ink + amber on cream", "diary" ambra/indaco | **rifiutate**: viola e ambra sono fuori territorio; presa solo la conferma "crema + inchiostro caldo" come base |
| "thin light serif display with precise grotesk legal institutional premium" (typography) | Legal Professional (EB Garamond + Lato), Classic Elegant (Playfair + Inter), Kinetic Brutalism (Space Grotesk) | **rifiutate** tutte e tre (studio legale 1998, template, brutalismo); presa la regola "serif per l'autorità, sans per il corpo" con serif **sottile** e asse ottico |
| "case file dashboard progress rail responsibility deadline checklist" (ux) | "Progress indicators: Step 2 of 4" | **accettata**: il rail dichiara "Étape 2 sur 7" in testo |
| "pinned scroll-driven diagram chapters reveal planes slide reduced motion" (gsap) | reveal 300–600 ms power2.out y 24 stagger .08; pin+scrub | **accettato** come tetto (io: 240–320 ms, y 12–24, stagger ≤ 70 ms); **rifiutato** `pin: true` → `position: sticky` + ScrollTimeline; "non pinnare più di 1–2 sezioni" → una sola |
| "architectural layered planes depth hairlines institutional legal premium" (style) | skeuomorphism, glassmorphism, parallax storytelling | skeuomorfismo **rifiutato**; vetro **solo** sulla barra sticky; parallax **accettata** in forma controllata (un capitolo appuntato, 26 px di deriva, niente scroll-jacking) |

## 13. Asset ufficiali — come li ho integrati

### Il marchio (`/static/brand/original/logo-mark.svg`)
Usato **verbatim come `<img>`** (una sola sorgente, mai ridisegnato, mai inline duplicato, proporzioni intatte, niente shimmer né rotazione in hover: le keyframes `logoKeyShimmer` e la scala `1.08 rotate(−3deg)` dell'originale non esistono più). Lock-up: marchio 38 px + wordmark Newsreader 500, maiuscolo, `.13em`, *Italy* verde `#157A3C` · *Legal* navy `#0F2547` · *Entry* rosso `#C4142B` + tagline *Digital Pathways to Italy* 8,5 px `.22em` (colore `--ink-3` per il contrasto, vedi § 2). Gap 12 px, altezza del link 44 px, `aria-label` sul link e testo nascosto alle AT (una sola voce).

| Contesto | Marchio | Wordmark / tagline | Nota |
|---|---|---|---|
| Header pubblico a riposo (≥ 1360 px) | 38 px | 20 px + tagline | allineato alla baseline della nav, 24 px di aria, «Connexion» a destra |
| Header sticky (scroll > 8 px) | 32 px | 17 px, tagline nascosta | transizione 180 ms su dimensione, non su forma |
| 1101–1359 px | 32 px | 15 px, tagline nascosta | le sette voci a 13 px; «Connexion» resta nella barra istituzionale («Espace réservé») |
| ≤ 1100 px | 32–38 px | 15 px | la navigazione passa al cassetto (bottone **Menu**, 44 px) |
| Mobile ≤ 480 / ≤ 359 px | 32 px | 15 → 13 px, tracking .10em | il bottone Menu perde la parola sotto 360 px |
| Cassetto mobile | 38 px | 20 px + tagline | in coda, sopra una hairline: firma il pannello |
| Footer | 48 px (40 px ≤ 480) | 22 px + tagline (17 → 14 px sotto 480/360) | su `--plane-1`; verde 4.55, rosso 5.07 |
| Barra della piattaforma (scura) | 32 px **su una targhetta avorio** (`--plane-0`, 3 px di bordo, raggio 2) | wordmark monocromo avorio, tagline nascosta | la sola "variante scura": il marchio non cambia, cambia il piano che lo porta |

Il titolo prescritto **ITALY LEGAL ENTRY™** resta l'H1 dell'hero, separato dal lock-up.

### La porta (`docs/design-v2/brand-original/portal.html`, `portal.css`, `reveal.js`)
Conservato: l'arco 3:4 con la semicirconferenza in cima (`border-radius: 50% 50% 0 0 / 37.5%`, cioè 190 px su 380), il gradiente sabbia → carta, la cornice interna a 16 px (ora un secondo tracciato SVG), **la fotografia del committente** (`arch-photo-original-2400.jpg`, mai l'URL Unsplash) a opacità .34 (originale .28) con la vignetta radiale navy `rgba(15,37,71,.82)`, **l'arco interno navy `#0F2547` al 52 %** con rapporto 1:1.55 e la sua ombra, **la chiave d'oro** (`key.svg`, 34 % dell'arco), **i tre gradini** 66/80/94 % navy a opacità decrescente, **la didascalia mono** *A doorway, not a shortcut* — ora testo reale, fuori dall'`aria-hidden`, letto dalle AT.

Evoluto, nel linguaggio della soglia architettonica:
1. **Piani**: un piano avorio-profondo fuori registro dietro l'arco, e l'arco stesso posato sulle linee di piano della griglia a 12 colonne.
2. **Tracé**: il contorno dell'arco e la cornice interna sono due `path` con `pathLength="1"` che si disegnano in 960 ms (l'unica durata immersiva), dal piede sinistro, sopra la volta, al piede destro: *un percorso che attraversa una soglia*.
3. **Luce**: la fotografia appare dopo il tracé (320 ms); alla base dell'arco una luce avorio (`.arch__light`) e nell'arco interno un **alone pre-renderizzato** in `radial-gradient` dietro la chiave — al posto dei `filter: drop-shadow` in loop (`keyGlow`, `keyInfiniteLevitate`, `portalInnerFloat`), che costavano GPU su tutta l'area.
4. **Avanzamento**: l'arco interno *sale* di 28 px nella sua sede, la chiave *sale* di 26 px dai gradini, i gradini si *costruiscono* dal centro (`scaleX`, stagger 80 ms) — pathway → connection → advancement, non decorazione.
5. **Scroll**: parallasse controllata (fotografia +26 px, chiave −14 px) solo ≥ 1025 px, via ScrollTimeline; nessun autoplay pesante.
6. **Hover** (solo `hover: hover`): fotografia a .44, chiave −4 px, primo gradino oro — come l'originale, senza `scale(1.14) rotate(4deg)`.
7. **Curve**: l'overshoot `(.34,1.56,.64,1)` è sostituito da `--e-in (.25,1,.5,1)`.
8. **Ridotto**: con `prefers-reduced-motion` la porta è completa e ferma dal primo paint, alone fisso a .8; nessun loop.
9. **Mobile**: l'arco scende sotto la copia a 300 → 260 px, centrato sul suo piano (l'originale lo metteva **prima** del titolo con `order: −1`: qui l'H1 viene prima per gerarchia e LCP).
10. **Accessibilità**: `.arch` è `aria-hidden`; `alt=""` sulle immagini; la didascalia è testo.

Cambiato rispetto all'originale, in sintesi: eliminati i tre loop infiniti e i filtri animati, l'overshoot, il fetch remoto, l'ordine mobile; aggiunti il piano retrostante, il doppio tracé, la luce di base, l'alone statico, la sequenza di costruzione, la parallasse leggera, la didascalia accessibile. Geometria, colori del marchio, fotografia, chiave e gradini sono quelli del committente.

### Nel fascicolo
Nessuna porta. Solo la grammatica: il lock-up sulla targhetta avorio nella barra-camera; i **tre gradini** come glifo (`#i-steps`, tre barre 8/12/16) davanti agli stati vuoti di Messages e Dates à retenir.

## 14. Verifica (auto-controllo, Chromium headless di Playwright)

Script: `scratchpad/b/check.py` (browser proprio, mai la porta 9222). Per ogni pagina × 1440×900 / 768×1024 / 390×844 / 320×640, con e senza `prefers-reduced-motion`: errori di console e richieste fallite, `scrollWidth ≤ clientWidth` e nessun elemento oltre il bordo, un solo `h1`, SVG `role="img"` etichettati, nessun salto di titolo, target ≥ 24 px, stato dei reveal; in più lo scroll fino al capitolo 4 (il livello 4 deve accendersi e il tracé avanzare) e l'apertura/chiusura del cassetto mobile con Escape.

Risultati dell'ultima esecuzione (Chromium headless di Playwright, `check.py`):

| Pagina × viewport | Errori console | Richieste fallite | scrollWidth / clientWidth | Elementi oltre il bordo | Probe a11y | Reveal non risolti |
|---|---|---|---|---|---|---|
| home 1440×900 | 0 | 0 | 1440 / 1440 | 0 | 0 | 0 |
| home 768×1024 | 0 | 0 | 768 / 768 | 0 | 0 | 0 |
| home 390×844 | 0 | 0 | 390 / 390 | 0 | 0 | 0 — cassetto: `aria-expanded` true all'apertura, false dopo Escape |
| home 320×640 | 0 | 0 | 320 / 320 | 0 | 0 | 0 |
| dashboard 1440×900 | 0 | 0 | 1440 / 1440 | 0 | 0 | 0 |
| dashboard 768×1024 | 0 | 0 | 768 / 768 | 0 | 0 | 0 |
| dashboard 390×844 | 0 | 0 | 390 / 390 | 0 | 0 | 0 |
| dashboard 320×640 | 0 | 0 | 320 / 320 | 0 | 0 | 0 |
| le stesse otto con `prefers-reduced-motion: reduce` | 0 | 0 | idem | 0 | 0 | 0 — righe del titolo `transform: none` al primo paint |

Altre misure: il capitolo 4 portato al centro del viewport imposta `data-active="4"` e il tracé è al 60 % (`stroke-dashoffset` 0.40); a 1,2 s dal caricamento la porta è a `is-planed is-traced is-lit is-open is-keyed` (arco 437×583 px a x=963); testo dell'hero e lock-up dell'header allineati a x=40; header senza overflow a 1101, 1120, 1200, 1280, 1360 e 1440 px; CTA nella camera in inchiostro (`rgb(20,33,43)`). `styles.css`: tre `cubic-bezier`, un solo `backdrop-filter`, nessun `style=` né `<style>`/`<script>` inline. Pesi: `styles.css` 60 KB e `main.js` 10 KB non minificati; Motion 24 KB gzip dal bundle condiviso.

Screenshot in `shots/`: `home_desktop.png` (pagina intera), `home_desktop_fold.png`, `home_desktop_hero_building_520ms.png` / `_1200ms.png` (la porta a metà costruzione), `home_desktop_routes.png` / `_hover.png`, `home_desktop_process.png` (capitolo 4 acceso) / `_cta.png`, `home_1280_fold.png`, `home_768_fold.png`, `home_mobile.png` (390, intera), `home_mobile_menu.png`, `home_320_fold.png`, `dashboard_desktop.png`, `dashboard_desktop_fold.png`, `dashboard_mobile.png`, `dashboard_320_fold.png`.

Non verificato in questa sessione: Chrome visibile a 360/768/1440 in AR (RTL) e la misura INP/LCP su 4G simulato; il file del committente da 948 KB rende l'LCP di questo prototipo superiore al budget finché non esistono i derivati (§ 10.1).
