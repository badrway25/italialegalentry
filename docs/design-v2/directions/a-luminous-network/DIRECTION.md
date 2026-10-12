# DIREZIONE A — «Rete luminosa» · Istituzione digitale come rete di percorsi

Prototipi: `home.html`, `dashboard.html`, `styles.css`, `main.js` (serviti su
`http://127.0.0.1:8790/docs/design-v2/directions/a-luminous-network/`). Screenshot in `shots/`.
Nessuno stile o script inline; font da `/static/css/fonts.css`; Motion da `/static/js/dist/motion.js`.

## 1. Concetto in dieci righe

1. La piattaforma è una **rete istituzionale viva**: i nodi sono gli attori (persona, organismo di formazione, università, impresa, istituzione, autorità competente), le linee sono i **percorsi regolari** tra le due sponde del Mediterraneo.
2. Al centro della rete non c'è un logo ma **la porta ufficiale del committente**: l'arco con la fotografia, l'arco interno navy, la chiave d'oro e i tre gradini. Tutte le linee convergono lì: *la voie régulière est une porte, pas un raccourci*.
3. Un solo capitolo inchiostro per pagina (hero, processo) su una base avorio calda: il buio è un capitolo, non una modalità.
4. **Un solo blu interattivo** (`--lum`), condiviso da link, CTA, focus e dalle linee luminose; l'oro esiste solo nella chiave ufficiale; verde e rosso solo nel marchio.
5. Tipografia a tre voci: grotesk istituzionale per l'interfaccia (Fira Sans), serif display leggero per i momenti firma (Newsreader 300), mono per riferimenti e numeri (Fira Mono), con i compagni arabi dichiarati.
6. Profondità per scala di superfici e hairline; le ombre solo per tre ruoli; vetro solo su elementi fluttuanti (header scrollato, scheda Forum).
7. Il moto dichiara la sua funzione: *disegno del percorso* (connessione), *pulsazione dell'attore corrente* (stato), *progressione legata allo scroll* (avanzamento). Una curva d'ingresso, una d'uscita, una standard; quattro durate.
8. I quattro componenti firma esistono come oggetti riconoscibili: hero-porta, quattro vie come diramazioni di un unico bus, processo NEED→INCLUSION come linea disegnata dallo scroll con responsabile per tappa, rail giurisdizione/responsabilità 2.0.
9. La piattaforma condivide font, accento, raggi, curve con il sito: la stessa rete, letta come fascicolo.
10. Personalità: autorità + sofisticazione tecnica. Non fintech-neon (niente gradienti viola, particelle, shader), non ministero (niente tricolore come identità, niente insegne; la serif è leggera, non solenne).

## 2. Asset ufficiali (addendum del committente)

### 2.1 Il logo — `/static/brand/original/logo-mark.svg`

Usato **verbatim come `<img>`**: nessuna geometria toccata, nessun effetto (il legacy aveva shimmer della chiave con `filter: drop-shadow` in loop e hover `scale(1.08) rotate(-3deg)` con curva overshoot: entrambi eliminati).

| Contesto | Marchio | Wordmark | Tagline | Note |
|---|---|---|---|---|
| Header pubblico (carta `#faf9f5`) | 38 px | Newsreader 600, 20 px, `.13em`, maiuscolo: ITALY `#157A3C` (5.14:1), LEGAL `#0F2547` (14.49:1), ENTRY `#C4142B` (5.72:1) | 8.5 px, `.22em`, `#5f6b7c` (5.14:1) | L'header pubblico è diventato **carta** proprio per ospitare il lock-up sul fondo per cui è stato disegnato. Gap 12 px, allineamento verticale al centro, come nel sito attuale. |
| Header scrollato (vetro avorio 86 % + blur) | 30 px | 16 px | scompare (opacità 0, altezza 0) | Barra da 72 → 56 px; il lock-up si compatta con la stessa curva standard, 240 ms. |
| Mobile 480–767 px | 32 px | 15 px | 8.5 px | |
| Mobile < 480 px | 32 px | 13 px | nascosta | |
| Mobile < 360 px | 38 px | nascosto | nascosta | Lo spazio non consente il wordmark accanto al bottone Menu senza deformarlo. |
| Barra della piattaforma (inchiostro) | 30 px | 15 px, **monocromo avorio** | nascosta (mobile) / non mostrata | **Unica variante per fondo scuro**: il marchio resta identico (i piani verde/rosso e il tratto bianco dell'arco lo tengono leggibile), il wordmark tricolore non passerebbe il contrasto sul buio, quindi diventa avorio. |
| Piè di pagina (carta) | 38 px | 20 px | 8.5 px | Lock-up completo. |
| Hub delle quattro vie (pillola inchiostro) | 22 px | «Italy Legal Entry™» sans | — | Il marchio come nodo centrale del bus. |

Il titolo bloccato dell'hero «ITALY LEGAL ENTRY™» resta, verbatim, come `<h1>` (grotesk 600, `.14em`).

### 2.2 La porta — «arch-photo-bg», evoluta

Fedele all'originale: arco 3/4 con sommità semicircolare (`border-radius: 50% 50% 0 0 / 37.5% 37.5% 0 0`, equivalente responsive di `190px 190px 0 0`), **fotografia del committente** (`docs/design-v2/brand-original/arch-photo-original-2400.jpg`, mai Unsplash) con vignetta radiale navy, arco interno navy `#0F2547` al 52 % di larghezza (`aspect-ratio 1/1.55`, top 13 %), **chiave** `/static/brand/original/key.svg` al 34 % dell'arco interno, tre gradini 66/80/94 %, didascalia mono «A doorway, not a shortcut» (resa come testo reale sotto la porta; la porta stessa è `aria-hidden`).

Che cosa è cambiato, e perché:

| Originale | Evoluzione | Motivo |
|---|---|---|
| Fondo sabbia→carta dentro l'arco, foto al 28 % | Fondo `#1a2f4d → ink-1`, foto al 50 % con vignetta più profonda | Sul capitolo inchiostro la foto deve portare più luce; la vignetta la fonde con la rete. |
| Bordo 1.5 px `--rule` + arco interno `::before` a 16 px | Le stesse due linee, ma come **path SVG che si disegnano** (esterno avorio 55 %, interno blu luminoso 45 %) | Il tracciato è il linguaggio del territorio: l'arco è la cornice legale che viene «tracciata». |
| Gradini navy al 30/22/14 % | Gradini **blu luminoso** al 90/55/30 %, il primo con alone | Su fondo navy i gradini navy sparirebbero; il blu li lega alle linee della rete. |
| `portalInnerFloat` 6 s, `keyInfiniteLevitate` 3.6 s con rotazione e scala, `keyGlow` con `filter: drop-shadow` in loop, hover `scale(1.14) rotate(4deg)` | Chiave: sola traslazione ±5 px in 6 s; alone: **layer pre-renderizzato** (gradiente radiale oro) che respira in opacità .7↔1 in 4 s; nessun hover, nessuna rotazione | Costo: solo `transform`/`opacity`; niente filtri in loop su aree grandi; niente overshoot. |
| `.rv` reveal 600 ms `ease` | Sequenza Motion: contorno 900 ms → foto 600 ms → arco interno 320 ms → chiave e alone 320 ms → gradini dal basso 240 ms ×3 → percorso principale 1200 ms → rete | La sequenza racconta *percorso → connessione → avanzamento*: prima la cornice, poi la procedura (chiave), poi i gradini, infine i percorsi che vi convergono. |
| Statica rispetto allo scroll | Parallasse a tre velocità: testo 1×, scena −40 px, foto −22 px dentro l'arco (solo ≥ 1024 px, `scroll()`/ScrollTimeline) | Profondità controllata; mai sul testo. |
| Mobile: arco 250 px, `order: -1` | Mobile: scena quadrata, porta al 62 % (≈ 220 px), rete ritagliata (`preserveAspectRatio slice`) senza etichette, `order: -1` | La porta è la copertina; le etichette a 4 px sarebbero rumore, i nodi ingranditi portano la lettura. |
| Ridotto: reveal disattivato | Ridotto: tutto completo e fermo (contorni, foto, chiave, gradini, rete); niente loop | Stato di prima classe: `withMotion(fn, settle)` per ogni animazione. |

Nel fascicolo la porta **non** è copiata: la sua grammatica (arco, chiave, gradini) vive solo come glifo di linea `g-doorway` negli stati vuoti (messaggi, scadenze) e nel marchio ufficiale della barra.

## 3. Palette — token CSS e rapporti misurati

Rapporti calcolati con la formula WCAG (script `contrast.py`), non a occhio.

```css
/* base avorio (pubblico, workspace) */
--canvas:#faf9f5; --area:#f1efe9; --surface:#fff; --hair:#dcd8ce; --hair-ui:#8f8878; /* 3.34:1 */
--ink:#0f1a2b;      /* 16.57:1 su canvas */
--ink-2:#46536a;    /*  7.37:1 */
--ink-3:#5f6b7c;    /*  5.14:1 (4.71 su area) */
--lum:#1f5fd6;      /*  5.44:1 su canvas, 4.98 su area, 5.73 su bianco; bianco su lum 5.73 */
--teal:#0f6b6e;     /*  5.95:1 — territorio, mai interattivo */
--royal:#163a6b;    /* 10.77:1 — istituzione */
--bronze:#7a4a1f;   /*  7.05:1 — formazione/attestati */
--rubric:#a4231b;   /*  7.03:1 — solo errore */
--warn:#7a4e00;     /*  6.83:1 */   --done:#1b6b4a; /* 6.14:1 */

/* capitolo inchiostro (hero, processo, barra e testata del fascicolo) */
--ink-0:#06121f; --ink-1:#0b1c30; --ink-2d:#132840; --ink-3d:#1a3350;
--hair-d:#274263 (decorativa); --hair-d-ui:#4f6d93; /* 3.54:1 su ink-0 */
--ivory:#f4f1ea;    /* 16.71:1 su ink-0, 13.25 su ink-2d */
--ivory-2:#b8c4d4;  /* 10.67:1 / 8.46 */
--ivory-3:#8fa0b5;  /*  7.06:1 / 5.60 */
--lum-d:#79b4ff;    /*  8.78:1 su ink-0, 6.96 su ink-2d, 5.99 su ink-3d — link, focus, linee */
--lum-d-btn:#2a63d4;/* avorio su di esso 4.86:1; contro ink-0 3.44:1 (UI) */
--teal-d:#7fd3d0;   /* 10.89:1 */  --sand-d:#e2c084; /* 10.87:1 */  --sage-d:#a9d5b1; /* 11.53:1 */

/* stati (fg/bg): todo 7.27, done 7.84, current 6.34, error 7.43, neutral 6.45 */
/* colori ufficiali, non token: #157A3C, #0F2547, #C4142B, #C39A2B (chiave su navy 5.80:1) */
```

Focus: anello 2 px `--lum` (5.44:1) + alone 6 px al 32 %; sul buio `--lum-d` (8.78:1). Nessun elemento porta il blu come decorazione salvo le linee della rete, che *sono* il soggetto.

## 4. Tipografia

| Voce | Prototipo (self-hosted) | Uso | Proposta di upgrade |
|---|---|---|---|
| Grotesk istituzionale | **Fira Sans** 400/500/600 | UI, corpo 17/28, etichette `.14–.18em` maiuscole, titolo bloccato dell'hero | Suisse Int'l + Suisse Int'l Arabic (stessa famiglia) |
| Serif display | **Newsreader** variabile, 300 per il display (`clamp(36px, 4.5vw, 66px)`, lh 1.04, −.012em), 400 per i titoli di sezione e il wordmark ufficiale (600, `.13em`) | Momenti firma: sottotitolo hero, titoli di sezione, «Prochaine étape», «Parcours pertinent» | Rhymes Display / Saol Display Light |
| Mono | **Fira Mono** 400 | Riferimento fascicolo `E46E03B461`, date, versioni regole, codici R1–R4, didascalia della porta | IBM Plex Mono |
| Arabo | IBM Plex Sans Arabic (UI), Noto Naskh Arabic (serif) | `[dir=rtl]` cambia i fallback e azzera il tracking | — |

Regole: pesi ≤ 600; tracking negativo solo sul display ≥ 36 px; righe ≤ 66 caratteri (`max-width: 58–66ch`); cifre tabellari (`font-feature-settings: "tnum"`).

## 5. Scala di profondità — sette livelli, un token per livello

| Livello | Chiaro | Inchiostro | Materiale |
|---|---|---|---|
| 0 canvas | `--canvas` | `--ink-0` | nessuno |
| 1 editoriale | `--area` (rail, thead) | `--ink-1` | hairline 1 px |
| 2 interattivo | `--surface` + `--hair` (card, righe, rotte) | `--ink-2d` + `--hair-d` | ombra solo in hover: `--sh-card-hover` |
| 3 elevato | pannelli mega-menu, popover | `--ink-3d` | `--sh-pop` (chiave + ambiente) |
| 4 focus | anello `--lum` + alone | `--lum-d` + alone | — |
| 5 overlay | drawer mobile | — | `--sh-overlay` |
| 6 immersivo | — | hero: porta con foto, scheda Forum in vetro, header scrollato in vetro | `backdrop-filter` solo qui e sull'header |

`box-shadow` compare con tre ruoli (hover card, popover, overlay) più gli aloni luminosi della porta/rail (segnale, non decorazione).

## 6. Vocabolario di moto

Curve: ingresso `cubic-bezier(.25,1,.5,1)`, uscita `cubic-bezier(.7,0,.3,1)`, standard `cubic-bezier(.4,0,.2,1)` — sono le **uniche tre** nel CSS. Durate di prodotto: 120 / 180 / 240 / 320 ms. Immersive (solo hero): 900 e 1200 ms. Loop ambientali: 24 s (pacchetto), 6 s (chiave), 4 s (alone), 2.8 s (sei-qui).

| Animazione | Funzione | Innesco | Durata / curva | Con «riduci movimento» |
|---|---|---|---|---|
| Titolo riga per riga (maschera) | gerarchia | load | 320 ms, stagger 60, ingresso | testo già in posizione |
| Porta: contorni che si tracciano | struttura legale | load +150 ms | 900 ms, ingresso | contorni completi |
| Foto dentro l'arco | profondità | +500 ms | 600 ms | visibile |
| Arco interno, chiave, alone | causalità (la procedura apre la porta) | +1.1 s | 320 ms | completi |
| Tre gradini dal basso | avanzamento | +1.4 s | 240 ms ×3, stagger 120 | completi |
| Percorso principale persona → porta → impresa | connessione | +1.45 s | 1200 ms | disegnato |
| Archi secondari, nodi, etichette | rete | dopo il percorso | 600/320/240 ms, stagger 35–40 | disegnati |
| Pacchetto lungo il percorso (`offset-path`) | l'unico oggetto vivo | dopo `is-live` | 24 s lineare, loop | assente |
| Chiave ±5 px, alone .7↔1 | delizia controllata | `is-live` | 6 s / 4 s alternate | fermi |
| Parallasse scena −40 px, foto −22 px | profondità | `scroll()` (ScrollTimeline) | lineare | assente |
| Header compatto + barra di lettura | orientamento | scroll | 240 ms standard; barra `scaleX` | header non si compatta, barra nascosta |
| Reveal di sezione | gerarchia | `inView` margine −8 % | 320 ms, stagger 50 | visibili |
| Processo: linea + stazioni | avanzamento | `scroll()` start 85 % → end 75 % | lineare | linea completa, tutte le stazioni accese |
| Stelo delle rotte | feedback | hover / `focus-within` | 240 ms standard | istantaneo |
| Rail 2.0 «sei qui» | stato | loop | 2.8 s | anello statico |
| Bottoni | feedback | hover | 180 ms ingresso, −1 px | — |

Nessuno scroll-jacking, nessun smooth-scroll; tutto interrompibile; solo `transform`, `opacity`, `stroke-dashoffset`.

## 7. I quattro componenti firma

**(a) Hero** — griglia 10/14: a sinistra eyebrow, titolo bloccato, display serif con «régulier» in corsivo blu, corpo prescritto, due CTA, due fatti legali (orientamento informativo; le decisioni spettano alle autorità), la scheda datata del Forum (fatto reale con data, § 15 dei principi). A destra la scena: rete (viewBox 1200×900) + porta ufficiale al centro; legenda in alto (attori · percorsi · la porta). Ordine di lettura e ordine di animazione coincidono.

**(b) Quattro vie di accesso** — non quattro card: un **bus** (una linea che parte dal nodo-hub col marchio ufficiale e si dirama in quattro steli). Ogni pannello ha glifo, codice mono R1–R4, titolo e bottone prescritti; la scala colore per via (blu/teal/navy reale/bronzo) colora solo glifo e stelo, mai il CTA. Hover e `focus-within` accendono lo stelo e il nodo. A < 640 px il bus è verticale a sinistra; a 640–1023 due colonne.

**(c) Processo NEED → INCLUSION** — capitolo inchiostro. Sei stazioni su una linea a onda (SVG `preserveAspectRatio: none`) che **si disegna con lo scroll**; ogni stazione porta numero, stadio (Besoin/Compétences/Formation/Parcours régulier/Entrée/Inclusion), il titolo con le otto voci **bloccate** della sequenza pilota (`FORMATION DANS LE PAYS D'ORIGINE` + `PRÉPARATION AVANT LE DÉPART` sotto Formazione; `ACCOMPAGNEMENT` + `SUIVI` sotto Inclusione), il **responsabile con glifo** e il territorio. Le stazioni si accendono quando la linea le raggiunge. Sotto: la frase bloccata sulle autorità competenti e la striscia di giurisdizione (anteprima del rail 2.0). Mobile: spina verticale con riempimento `scaleY` legato allo scroll.

**(d) Rail giurisdizione/responsabilità 2.0** — nella testata del fascicolo: sette segmenti (le sette tappe reali del percorso persona), ognuno con **texture + glifo + etichetta del responsabile** (Vous / Plateforme / Organisme de formation / Autorité compétente / Territoire d'accueil), stato *terminato* (pieno + spunta), *attuale* (anello luminoso + pillola «Vous êtes ici» + pulsazione), *a venire* (contorno); confine `MA → IT` tratteggiato tra 05 e 06; legenda testuale. Mai solo colore: texture, glifo, numero, testo nascosto per gli screen reader. Verticale sotto 1024 px.

## 8. Shell della piattaforma

Barra inchiostro 56 px: marchio ufficiale + wordmark avorio · contesto `E46E03B461` (mono) · ricerca con `Ctrl K` · Sito pubblico · account · lingua. Rail sinistro 248 px su `--area`, **comprimibile a 68 px** (bottone `aria-expanded`, `Ctrl/⌘ B`; le etichette restano nell'albero dell'accessibilità); voce attiva con filetto blu; in fondo il promemoria antifrode. Workspace: breadcrumb → **testata del fascicolo** (banda inchiostro con titolo serif, riferimento, quattro fatti, rail 2.0) → **Prochaine étape** come superficie di prima classe (serif, responsabile con glifo, «Cette étape ne dépend pas de vous», CTA) → checklist (elemento · stato · responsabile con glifo e nota · scadenza) → documenti + pre-valutazione (con la frase sul jeu de règles, verbatim) → messaggi/scadenze vuoti (glifo-porta) → account. Sotto 1024 px il rail diventa una striscia di tab scorrevole sotto la barra. Ispettore destro contestuale: non prototipato (vedi rischi).

## 9. Composizione mobile (320–767 px)

Header ≤ 72 px con lock-up compatto; drawer a tutta altezza su carta con sottoliste espanse. Hero: porta come copertina (scena quadrata, rete ritagliata, nessuna etichetta), poi eyebrow, titolo, display, corpo, CTA impilate (a 320 px il bottone va a capo, niente `nowrap`), scheda Forum. Quattro vie in lista con bus verticale. Processo con spina verticale. Fascicolo: fatti impilati, rail 2.0 verticale, checklist come schede con etichette `data-label`, documenti con nome mono a capo. Gutter 16 px, target ≥ 24 px, nessuno scroll orizzontale a 320/390/768 (verificato).

## 10. Note RTL

Solo proprietà logiche nel CSS nuovo (`inset-inline`, `margin-inline`, `padding-inline`, `border-inline-start`, `text-align: start`). Con `dir="rtl"`: famiglie arabe in testa allo stack, `letter-spacing: 0` su eyebrow/folio/titolo bloccato/stati; la rete e l'onda del processo si specchiano (`scaleX(-1)`) con le etichette ri-specchiate; frecce `.ic--arrow` specchiate; barra di progresso con origine a destra. La porta e la chiave **non** si specchiano (asset ufficiali). Da verificare a tre larghezze in AR prima dell'accettazione.

## 11. Rischi

1. **Peso della foto**: l'originale è 2400×1600, 949 KB; in produzione servono varianti AVIF/WebP ≤ 120 KB con `srcset` e `fetchpriority`, altrimenti l'LCP soffre.
2. **Responsabili del rail 2.0**: i proprietari per tappa sono *indicativi* nel prototipo; devono provenire dalle assegnazioni reali (Rule Engine / `responsible`) prima di qualunque pubblicazione — dire «autorité compétente» dove non è vero sarebbe un fatto legale sbagliato.
3. **Famiglia serif del wordmark**: il legacy usa `var(--display)` non recuperata; Newsreader 600 è un sostituto da validare con il committente.
4. **Marchio su fondo inchiostro**: il navy ufficiale contro `--ink-0` è 1.24:1; il marchio resta leggibile grazie ai piani e al tratto bianco, ma se il committente non lo gradisce l'alternativa coerente è una piastrina avorio 40 px dietro il marchio.
5. **Tagline a 8.5 px**: dimensione del committente; sotto 480 px è nascosta, sotto 360 px resta il solo marchio.
6. **Didascalia inglese** «A doorway, not a shortcut» su una pagina francese: tenuta come frase di marca (come «Digital Pathways to Italy»); da decidere se tradurre.
7. **Mega-menu**: Escape e click fuori funzionano; manca la navigazione con le frecce tra i pannelli.
8. **Il percorso passa «sotto» la porta**: voluto (la persona la attraversa), ma un lettore distratto può leggerlo come interruzione; la didascalia e la legenda disambiguano.
9. **Ispettore destro del fascicolo** non prototipato: la brief lo chiede per il fascicolo flagship; qui il dashboard usa una colonna sola più larga.

## 12. Candidati 21st.dev esaminati

Metodo: SEARCH ≥ 5 → PREVIEW → REVIEW → ADAPT. Codice recuperato con `get_component` per tre soli componenti (struttura), nessuna generazione AI, nessun pacchetto installato.

**Hero**

| Nome | URL | Presa / scarto |
|---|---|---|
| Hero Section (Animated Roadmap) — @ravikatiyar162 | https://21st.dev/@ravikatiyar162/components/hero-section-5 | **Codice studiato**: `useScroll` → `pathLength` su un path SVG, tappe che appaiono in vista. Presa: linea disegnata dallo scroll con tappe agganciate → il nostro processo. Scarto: tappe posizionate con `style` inline (CSP), framer-motion. |
| Path Drawing (esempi Motion) — @motiondotdev | https://21st.dev/@motiondotdev/components/motion-path-drawing | Presa: tecnica di rivelazione del tratto normalizzata (`pathLength="1"` + dashoffset), riscritta in Motion vanilla per contorni della porta e percorsi. |
| Line Draw SVG — @pulkitxm | https://21st.dev/@pulkitxm/components/line-draw-svg | Presa: modalità «on mount / on scroll» per lo stesso tratto. Scarto: preset (cuore, stella). |
| Path Drawing Portfolio Hero — @httpsdesign-layercomja | https://21st.dev/@httpsdesign-layercomja/components/path-drawing-portfolio-hero | Presa: il tratto che si disegna come «oggetto vivo» dell'hero. Scarto: tratto sfumato. |
| Hero Section — @reuno-ui | https://21st.dev/@reuno-ui/components/hero-section | Presa: ritmo del reveal riga per riga. Scarto: estetica generica. |
| Hero Section Dark — @kinfe123 | https://21st.dev/@kinfe123/components/hero-section-dark | Presa: canvas scuro con tipografia stratificata. Scarto: glow decorativo. |
| Shader Hero — @beratberkayg | https://21st.dev/@beratberkayg/components/shader-hero | Scartato: WebGL (principio 17). |
| Interactive Dot Grid Hero — @nexus-ui | https://21st.dev/@nexus-ui/components/dot-grid-hero | Scartato: particelle che seguono il cursore. |
| DataGridHero — @dhileepkumargm | https://21st.dev/@dhileepkumargm/components/data-grid-hero | Scartato: griglia generativa, glow che segue il mouse. |
| Grid Hero Animated — @minhxthanh | https://21st.dev/@minhxthanh/components/grid-hero-animated | Scartato: sfondo a griglia animata senza informazione. |

**Navigazione**

| Nome | URL | Presa / scarto |
|---|---|---|
| Morphing Scroll Navbar — @laziekiki | https://21st.dev/@laziekiki/components/morphing-scroll-navbar | **Codice studiato**: scroll con `requestAnimationFrame`, direzione, barra di progresso `scaleX`, `aria-current` sul link attivo. Presa: compattazione allo scroll + barra di lettura. Scarto: capsula fluttuante, curve overshoot `(.34,1.32,.5,1)`, `<style>` inline. |
| Navbar Section 2 (mega-menu) — @solaceui | https://21st.dev/@solaceui/components/navbar-section-2 | Presa: pannello con titolo + descrizione + lista a due colonne (pannello «Personnes» con gli otto percorsi reali). Scarto: barra scura (la nostra è carta per il lock-up). |
| Motion Navigation Menu — @unlumen | https://21st.dev/@unlumen/components/motion-navigation-menu | Presa: un solo contenitore per i pannelli. Scarto: transizioni spring direzionali. |
| Header 1 — @efferd | https://21st.dev/@efferd/components/header-1 | Presa: blur allo scroll, drawer mobile. |
| Header 3 — @efferd | https://21st.dev/@efferd/components/header-3 | Presa: sottoliste annidate espanse nel drawer. |
| Mega Menu — @ln-dev7 | https://21st.dev/@ln-dev7/components/mega-menu | Scartato: estetica shadcn di serie. |
| Navbar Menu — @manuarora700 | https://21st.dev/@manuarora700/components/navbar-menu | Scartato: solo hover, senza equivalente tastiera. |
| Liquid Morph Floating Menu — @aayush-duhan | https://21st.dev/@aayush-duhan/components/liquid-morph-floating-menu | Scartato: effetti letter-roll, pillola. |

**Shell e processo**

| Nome | URL | Presa / scarto |
|---|---|---|
| Animated Sidebar — @starc007 | https://21st.dev/@starc007/components/animated-sidebar | **Codice studiato**: rail a icone, sheet mobile con focus gestito, scorciatoia `⌘B`, etichette `aria-hidden` da compresso, gruppo che riapre il pannello. Presa: compressione a 68 px, `Ctrl/⌘ B`, nomi accessibili mantenuti. Scarto: spring, React. |
| Command Palette — @rafa-porto | https://21st.dev/@rafa-porto/components/command-palette | Presa: campo con suggerimento `kbd`; la palette non è stata costruita. |
| Dashboard Sidebar — @arunjdass | https://21st.dev/@arunjdass/components/dashboard-sidebar | Scartato: card promozionale, registro SaaS. |
| Sidebar with Search and Profile — @uiable | https://21st.dev/@uiable/components/sidebar-5 | Scartato: «pro upgrade». |
| Dashboard with Collapsible Sidebar — @uniquesonu | https://21st.dev/@uniquesonu/components/dashboard-with-collapsible-sidebar | Scartato: generico. |
| Vertical Titled Stepper — @sean0205 | https://21st.dev/@sean0205/components/c-stepper-15 | Presa: modalità verticale con linea di collegamento (processo mobile, rail 2.0 mobile). |
| Animated Progress Stepper — @shadcnspace | https://21st.dev/@shadcnspace/components/stepper-03 | Presa: il punto che viaggia → il pacchetto lungo il percorso. Scarto: spring, badge pulsante. |
| Segmented Progress Pill Stepper — @shadcnspace | https://21st.dev/@shadcnspace/components/stepper-04 | Presa: segmenti proporzionali → rail 2.0. Scarto: raggi a pillola ovunque. |
| Process Timeline — @shadcnui-blocks | https://21st.dev/@shadcnui-blocks/components/timeline-05 | Scartato: cerchi numerati generici. |
| Product Timeline — @hyperiux | https://21st.dev/@hyperiux/components/timeline | Scartato: Lenis + GSAP (smooth scroll su pagine di compito). |

## 13. Input UI-UX-Pro-Max (v2.13.0) consultato

| Query (dominio) | Risposta | Accettato / rifiutato |
|---|---|---|
| «institutional legal platform navy luminous blue network» (color) | Legal Services: navy `#1E3A8A`, accento oro `#B45309`, fondo `#F8FAFC`, grigi slate | Accettato il principio «navy d'autorità + un solo accento di fiducia» → inchiostro-navy + un solo blu luminoso. Rifiutati i grigi slate/zinc (anti-pattern § 1) e l'oro come accento UI: l'oro resta solo nella chiave ufficiale. |
| «institutional grotesk serif display authority» (typography) | Space Grotesk brutalista / Web3 | Rifiutato in blocco: registro sbagliato. |
| «dashboard progress status» (ux) | Indicatori di avanzamento «Step 2 of 4»; badge live con `role=status` atomico | Accettato: «0 sur 5 éléments complétés» come conteggio, stati del rail con testo per gli screen reader. |
| «navigation header sticky» (ux) | Compensare l'header fisso; tab order coerente; breadcrumb | Accettato: `scroll-padding-top`, breadcrumb nel fascicolo. |
| «focus keyboard accessibility contrast» (ux) | Indicatore ≥ 2 px con 3:1; focus mai coperto da UI persistente | Accettato: anello 2 px + alone, header 56 px scrollato + `scroll-padding`. |
| «svg path drawing scroll linked network nodes» (gsap) | Reveal 300–400 ms `power1.out` y 12; parallasse 5–15 % solo su layer decorativi; pinning con scrub | Accettato: reveal 320 ms y 14, parallasse solo su scena e foto. Rifiutato il pinning (scroll 1:1). |
| «hero headline reveal stagger» (gsap) | SplitText per caratteri, 400–700 ms `expo.out` | Rifiutato per caratteri; accettato a livello di riga (3 righe, stagger 60 ms, 320 ms). |
| «premium institutional network dark hero layered depth» (style) | Skeuomorfismo / glassmorfismo / parallax storytelling | Skeuomorfismo rifiutato; vetro solo su elementi fluttuanti; parallasse a ampiezza minima. |
| «dashboard case file responsibility next action», «line draw svg stroke» | nessun risultato nel database | dichiarato; nessun fallback preso da lì. |

## 14. Verifica

Script `check_a.py` (Chromium headless di Playwright, browser proprio): `home.html` e `dashboard.html` a 1440×900, 768×1024, 390×844, 320×640, con e senza `prefers-reduced-motion` → **0 errori di console, `scrollWidth ≤ clientWidth` ovunque**. Sonde: linea del processo `stroke-dashoffset` 0.67 a metà sezione e 0.15 in fondo (scroll-linked reale); sequenza hero completa a 3.2 s; mega-menu, drawer mobile, rail compresso, focus sulle rotte verificati con screenshot.

Screenshot: `shots/home_desktop_fold.png`, `home_desktop.png`, `home_desktop_reduced.png`, `home_mobile.png`, `home_mobile_fold.png`, `home_tablet.png`, `dashboard_desktop.png`, `dashboard_desktop_fold.png`, `dashboard_mobile.png`, `dashboard_tablet.png`, `probe_hero_t*.png`, `probe_process_mid.png`, `probe_nav_panel.png`, `probe_mobile_drawer.png`, `probe_dashboard_collapsed.png`, `probe_routes_focus.png`.
