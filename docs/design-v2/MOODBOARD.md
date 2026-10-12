# MOODBOARD — il territorio estratto dai benchmark (23 settembre 2026)

Tesi in una riga: **uno studio legale internazionale del 2026, non un ministero e non una startup.**
Avorio caldo come carta, inchiostro tinto (navy o caldo) come voce, un solo blu luminoso per
l'interazione, teal-petrolio per il territorio mediterraneo; grotesk + serif leggero + mono, ognuno
con il proprio compagno arabo; profondità per scala di superfici; moto ease-out di 150–300 ms con
un solo oggetto vivo per pagina. I nomi tra parentesi rimandano a BENCHMARKS.md.

## 1. Tipografia — quattro direzioni candidate (tutte con compagno arabo)

Regole comuni, tutte osservate: tre voci (sans / serif / mono) come una famiglia (Nobel: Alfred
Sans/Serif/Mono; Instrument; Harvey Sans/Serif); pesi intermedi di font variabili (Mercury 480/420,
Linear 590/510) invece del bold; tracking negativo solo sui display (Linear −1…−3 px), corpo a
tracking neutro o lievemente positivo (Mercury +0.01/+0.02 em); scala fissa 64/48/32/24/18/16/14/13
con interlinee multiple di 4 px (ECL) o 5 px (GOV.UK); 75 caratteri per riga (Designers Italia);
numeri tabellari dedicati (Clerk "Geist numbers"). Per l'arabo (rtlstyling.com): `letter-spacing: 0`,
interlinea maggiore per i segni diacritici, niente opacità sul testo, `min-width` sui bottoni,
numerali coerenti (o arabi orientali o occidentali, mai misti).

| | Sans (UI e titoli) | Serif (editoriale) | Mono (dati/norme) | Compagno arabo | Evidenza | Rischio |
|---|---|---|---|---|---|---|
| **A. Svizzera istituzionale** | Suisse Int'l Book/Medium | Serif display leggero (classe Rhymes Display Thin / Saol Display Light / Lyon Display) | Söhne Mono o IBM Plex Mono | **Suisse Int'l Arabic** (29LT Kaff, stessa famiglia, Swiss Typefaces; in uso bilingue: El-Moez, Tasmeem Doha) + Noto Naskh Arabic per il serif | Legora (Suisse + Rhymes), Clerk (Suisse + Söhne Mono), Unseen (Saol), UC Investments (Lyon) | Licenza commerciale; Suisse è già in molti SaaS: il serif deve fare la differenza |
| **B. Plex istituzionale open** | IBM Plex Sans | IBM Plex Serif | IBM Plex Mono | **IBM Plex Sans Arabic** (Abbink, Bold Monday, Apelian, Morcos; OFL) — stessa famiglia | Mercury e Lusion usano Plex Mono; Plex Arabic è su Google/Adobe Fonts | Legge "IBM/enterprise" se usato bold; versioni variabili da verificare |
| **C. Umanista Frutiger (mobilità)** | Neue Frutiger Light/Book | Source Serif 4 (OFL) o Lyon Text | Source Code Pro (Stripe) | **Neue Frutiger Arabic** (Nadine Chahine, Monotype: "consistent tone of voice regardless of the language") | Eredità wayfinding/aeroporti = "percorso"; ONCF usa Helvetica Neue Arabic come compagno | Bold Frutiger legge segnaletica anni 2000: solo pesi leggeri |
| **D. Trio open Instrument** | Instrument Sans | Instrument Serif (solo accento) | Instrument Mono / Geist Mono | Readex Pro (variabile 160–700, OFL, con Nadine Chahine; **copertura araba da verificare sullo specimen Google**) oppure Noto Kufi + Noto Naskh Arabic | Instrument (agenzia), Raycast (Instrument Serif) | Instrument Serif è il "serif di moda 2025–26" dei SaaS: rischio template |

Da non usare come voce unica: Inter (è il default di Migrationsverket, gov.sg, Linear, Bocconi,
Banca d'Italia: non distingue), Titillium (PA), Playfair/Montserrat/Poppins (Bocconi, Sciences Po,
Trenitalia), Söhne (Stripe/Clerk; nessuna versione araba verificata).

## 2. Colore — ogni territorio valutato con le prove

| Territorio | Evidenze | Verdetto | Ruolo proposto |
|---|---|---|---|
| **Midnight / inchiostro** | Linear #08090a ("faint blue tint is intentional"), Mercury #171721 (indaco), Harvey #1F1D1A (caldo), Adyen #001222 (navy-inchiostro), Instrument #070708 | SÌ, mai #000 (Jeton "almost ditched black") | Testo primario e canvas dei capitoli immersivi; scegliere **una** tinta: navy-inchiostro (#001222 → #0d1e2e) o caldo (#1F1D1A). Il navy-inchiostro lega meglio teal e blu luminoso |
| **Navy reale** | EUIPO #164194, ECL #0E47CB, NBIM #03217f, BoE #12273f, EUI #0E4876, Designers Italia slate #17324d | SÌ come autorità di superficie; NO come accento interattivo (rischia "banca legacy") | H1 nei capitoli chiari, rail giurisdizione/responsabilità, sfondo dell'header nel portale |
| **Verde italiano selettivo** | Designers Italia success #008055, EUI oliva #8F942F, Juro #033f2f, Wise #9fe870 | Solo semantico o desaturato; mai accanto a rosso; mai come marca | "Regolare / approvato / attivo" e oliva nelle fotografie |
| **Teal / Mediterraneo** | ETH #007894 (tema d'ateneo), Designers Italia accento #089994, Wise celebration #0e4242 / #a0e1e1 | SÌ come secondo accento **non** interattivo, territorio e Orientamento/Inclusione | Etichette, sfondi di sezione, scale per via d'accesso. Testo solo nelle varianti scure (#05615e, #00596d); #089994 è 3.5:1 (solo grafica/UI) |
| **Avorio caldo** | NBIM `#faf9f5`, Harvey `#fafaf9`, token beige Mercury; Vercel #fafafa (neutro), Stripe #f8fafd (freddo) | SÌ come canvas base pubblico: legge "carta, atto, contratto" | `canvas` #faf9f5; `area` #f2f1f0 per sezioni (Snøhetta `area-bg`) |
| **Grigio minerale** | Scala calda Harvey #e5e5e3 → #524f49; ECL Dark-100…5 #262B38 → #F4F5F5; Vercel accents-1…8 | SÌ, 8–10 passi tinti come l'inchiostro | Testo secondario, hairline, bordi; **mai** zinc/slate di shadcn |
| **Oro / bronzo** | Harvey dark-bronze #593d3a; EUI sabbia #F1C46F; ECL #FFCC00 e giallo ECB (bandiera/euro) | Solo bronzo scuro desaturato; mai giallo saturo, mai gradiente oro | Sigillo di certificazione/attestato in Academy, filetto dei documenti |
| **Blu/teal luminoso interattivo** | NBIM #0026ff (7.3:1 su avorio, calcolo da verificare), Vercel #0070f3, Mercury #5266eb, World Bank #2e43e0, Lusion #1a2ffb, Linear #5e6ad2 | SÌ, **uno solo**, riservato a link/CTA/focus | `blue-lum` con variante chiara per il buio (Linear hover #828fff) e anello di focus a 30 % (Linear) |
| Rosso | Designers Italia #cc334d, ECL #D7003D | Solo errore | Mai decorativo (tricolore) |

Contrasto: 4.5:1 per il testo, 3:1 per componenti e grafica (WCAG 1.4.11, "2.999:1 non passa"),
verificato con lo strumento e non a occhio (Designers Italia pubblica i rapporti per ogni token).

## 3. Superfici e profondità — la scala che sostituisce le ombre decorative

Prove: Linear "four-step ladder replaces shadows" (#0f1011 → #141516 → #18191a + hairline
#23252a → #34343a) e temi generati in LCH con elevazioni per background/foreground/panels/
dialogs/modals; Vercel ombre **per ruolo** (card `0 1px 2px`, hover `0 0 0 1px + 0 4px 12px`, popover,
modal `0 8px 16px -4px + 0 24px 32px -8px`); Fluent 2 rampa 2/4/8/16/28/64 con ombra "key"
(direzionale) + "ambient" (diffusa) e opacità raddoppiata in dark (14 % → 28 %); Apple Liquid Glass
solo su "buttons, switches, sliders, tab bars and sidebars", mai sul contenuto; Raycast usa
`backdrop-filter` solo sulla palette comandi; Snøhetta token `area-bg` / `stroke` per tema.

| Livello | Chiaro (pubblico) | Scuro (capitoli / opzione portale) | Ombra / materiale |
|---|---|---|---|
| 0 canvas | #faf9f5 | #001222 | nessuna |
| 1 editoriale | `area` #f2f1f0 | #0d1e2e | nessuna, hairline 1 px |
| 2 interattivo (card, riga) | canvas + hairline | #1a2b3b + hairline #2f3e4d | shadow-2 solo in hover |
| 3 elevato (popover, menu) | bianco | #1a2b3b | shadow-8/16 key+ambient; vetro ammesso |
| 4 focus | anello 2 px `blue-lum` + alone 3 px al 30 % | idem, variante chiara | — |
| 5 overlay (modal, drawer) | bianco | #0d1e2e | shadow-64 + scrim; mai vetro sul contenuto |
| 6 immersivo | foto/video full-bleed, scena ScrollTimeline | idem | pannelli in vetro **solo** qui (Legora) |

## 4. Sistemi di hero — cinque idiomi osservati, da combinare

1. **Numero vivo** (NBIM: valore del fondo aggiornato) → pratiche attive, scadenze, giorni al
   decreto, per la piattaforma e per HOME in versione istituzionale (dati pubblici, con fonte).
2. **Lo strumento è l'hero** (Eurostar tab di prenotazione; IND quattro card; Migrationsverket sei
   fasi) → le quattro vie di accesso come pannelli, non come paragrafi.
3. **Editorial Stagger + Parallax Layers** (motion.dev/ui: titolo rivelato riga per riga con
   maschera; titolo e card più veloci della finestra di sfondo) su fotografia atmosferica con
   pannelli in vetro (Legora: "layered hero background", "floating UI panels").
4. **Una sola animazione ambientale con fallback statico** (Stripe: onda + immagine; utsubo:
   "one ambient + one user-triggered").
5. **Oggetto indicizzato allo scroll, senza autoplay** (Jeton/Rive) → per noi il percorso
   NEED → SKILLS → TRAINING → REGULAR PATHWAY → ENTRY → INCLUSION che avanza con lo scroll.

Combinazione per HOME: 3 (titolo) + 2 (quattro vie) + 5 (rail di processo sotto la piega) + un
solo elemento vivo (1). Mai H1 + paragrafo + bottone statici.

## 5. Idiomi di moto — curve e durate misurate

| Uso | Curva osservata | Dove | Durata |
|---|---|---|---|
| Entrata (reveal, hover) | `cubic-bezier(.25,1,.5,1)` easeOutQuart | Stripe ×12 | 180–240 ms |
| Entrata enfatica (overlay, palette) | `cubic-bezier(.16,1,.3,1)` easeOutExpo | Raycast, motion.dev, 21st | 240–320 ms |
| Standard bidirezionale | `cubic-bezier(.4,0,.2,1)` | Vercel, gov.sg, Snøhetta, Triennale | 120–200 ms |
| Uscita | `cubic-bezier(.7,0,.3,1)` | Harvey, Mercury | 120–180 ms |
| Unica curva di sistema | `cubic-bezier(.215,.61,.355,1)` easeOutCubic | MIT ×126, Locomotive ×43 | .2/.3/.35 s |
| Loop ambientali | lineari | Attio 30 s / 10 s | ≥ 20 s |
| **Da evitare** | overshoot `(.34,1.56,.64,1)`, `(0.52,1.64,0.37,0.66)`, `ease-in-out-quad` ×32 | Raycast, Wise, BoE, Bocconi | — |

Regole derivate: < 300 ms per tutto ciò che è di prodotto (Emil Kowalski); nessuna animazione sulle
azioni ripetute da tastiera; interrompibile sempre; la frequenza riduce il valore dell'animazione
(Rauno Freiberg); stagger 40–60 ms per riga nel reveal editoriale; scroll-linked solo con
`scroll()`/ScrollTimeline (accelerazione hardware, motion.dev), scroll-triggered con `inView`.
Transizioni di pagina: crossfade breve con header condiviso (swup/Barba: Cash App, Wise), mai
tende/iris tra pagine di compito.

## 6. Idiomi di navigazione

- Header a due livelli: utilità (lingua IT/FR/EN/AR, accesso "La mia area" come "My page"/"My IND")
  e primario (quattro vie, Academy, Piattaforma). Persona / professionista / impresa separati come IND.
- Ingressi per **situazione o fase** (IND "How can we help you?", Migrationsverket sei stadi,
  GOV.UK "Visas and immigration"), non per organigramma.
- Sezione "In focus" (ECB) per novità normative datate (Migrationsverket "On 6 June 2026…").
- Rail giurisdizione/responsabilità sempre visibile nelle pagine RICH/LEGAL: chi decide (IT/MA/UE).
- Portale: barra superiore snella + palette comandi (Linear/Raycast), sidebar 256 → 64 px.
- Mobile: header ≤ 56 px, menu a pannello con le quattro vie in lista verticale; target ≥ 24 px.

## 7. Idiomi di dashboard e fascicolo

- **Superficie di lavoro prima di tutto** (Linear: navigazione ridotta a barra, quasi tutti i pixel
  al contenuto); scala di superfici e hairline al posto delle ombre.
- **Il riepilogo è una superficie di prima classe** (Attio: sintesi e azioni suggerite, non un widget
  chat) → "Stato della pratica" in cima al fascicolo: fase attuale del percorso, prossimo atto,
  responsabile, scadenza.
- **Il fascicolo letto come un atto** (Mercury: saldi e movimenti "come un rendiconto ben composto";
  Tiempos per i momenti editoriali) → intestazione con numero vivo (giorni, documenti mancanti),
  cronologia con date allineate in mono.
- Eventi di vita e sezioni personali (LifeSG: "key moments", benefici, finanze) → per persona:
  Orientamento → Formazione → Ingresso → Inclusione come tab di stato.
- Divulgazione progressiva (schema 4–6 KPI + griglia 12 colonne/24 px: fonte secondaria adminlte,
  da prendere come ipotesi non come regola).

## 8. Fotografia, illustrazione, iconografia

- Fotografia: interni e architettura con luce naturale, materiali (pietra, cuoio, legno chiaro:
  Legora), ritratti degli attori reali con consenso (Mercury, Harvey), uso reale del servizio
  (Monzo, via utsubo). Ritaglio con focal point (Eurostar). **Mai** foto di cronaca migratoria (IOM,
  IND/Ter Apel), mai aerei/passaporti/valigie/bandiere.
- Illustrazione: vignette disegnate a mano per stemperare il rigore (Legora/Robert Leighton);
  astrazioni geometriche piatte per i concetti (Mercury); schemi di processo a linea.
- Icone: set proprietario come asset (ECB `ECB-icon-set`), tratto 1.5 px, stile "thin/sharp"
  (Migrationsverket); niente lucide/FontAwesome di serie (avoid-ai-design; BoE, EIB, Maroc.ma).

## 9. Ritmo dark / light

- Pubblico: avorio come base; al massimo **un capitolo** inchiostro per pagina (Harvey chiaro,
  Legora scuro: la differenza è di capitolo, non di modalità), con transizione di sfondo al confine.
- Piattaforma: chiaro per default, schema scuro via attributo di documento (DSFR
  `data-fr-scheme`), token doppi `canvas/area/stroke` (Snøhetta, Instrument), opacità delle ombre
  raddoppiata nel buio (Fluent 2).
- Il buio non è un proxy di "premium" (LogRocket sull'omologazione "Linear"): lo è la scala.
