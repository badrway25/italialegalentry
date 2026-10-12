# BENCHMARKS — riferimenti 2025–2026 per ITALY LEGAL ENTRY™

Ricerca del 23 settembre 2026. Ogni scheda riporta solo ciò che è stato osservato direttamente
(HTML e primi tre fogli di stile scaricati con `curl`, oppure pagina letta con WebFetch) o citato
da una fonte primaria (case study dell'agenzia, documentazione del design system). Nessun sito è
da copiare: ogni scheda separa ciò che si prende da ciò che si lascia.

## Metodo e limiti

- **Sonda tecnica** su ~95 URL: titolo, `theme-color`, `@font-face`, custom property colore, curve
  `cubic-bezier`, durate, `backdrop-filter`, raggi, `prefers-reduced-motion`. Librerie citate solo se
  inequivocabili nel markup (`lenis`, `gsap`, `lottie`, `splide`, `swiper`, `locomotive-scroll`,
  `govuk-frontend`, `bootstrap-italia`, `ecl-`). Struttura, copy e navigazione via WebFetch.
- **Non verificabili oggi** (Cloudflare/Akamai o solo JS): OECD, IOM, IMF, Clio, Fondazione Prada,
  ITA Airways, SNCF Connect, FT, systeme-de-design.gouv.fr (letto via GitHub), LUISS, Italia Domani,
  Consiglio d'Europa, Ramp (Webflow senza CSS), Apple HIG e Material 3. Citati solo con fonte chiara.
- Le gallerie premiano poco l'istituzionale: Awwwards *government* mostra ri.gov e austrade.gov.au;
  *law* solo Honorable Mention (Ario Law, maggio 2026: Helvetica + WordPress); *education* due
  scuole. Il livello che cerchiamo sta nei prodotti, non nei premi.

## Lettura trasversale (cosa hanno in comune i riferimenti migliori)

1. **Un solo accento cromatico per l'unica azione che conta** (Mercury #5266eb, Linear #5e6ad2,
   NBIM #0026ff, Vercel #0070f3): il resto è una scala di inchiostro/avorio.
2. **Font commissionati o famiglie complete** (Söhne, Arcadia, Wise Sans, Harvey Sans/Serif,
   Alfred Sans/Serif/Mono, NorgesBank, Aino, GDS Transport, Marianne): la tipografia è
   l'infrastruttura del marchio, non una scelta di template.
3. **Pesi intermedi di font variabili** (Mercury 480/420, Linear 590/510): autorevolezza senza
   grassetto.
4. **Ease-out corti**: 150–300 ms dominano ovunque (Adyen `.15s`×393, Wise `.3s`×198,
   ETH 80/160 ms); le curve sono `easeOutCubic/Quart/Expo`, non `ease-in-out`.
5. **Profondità per scala di superfici, non per ombre** (Linear "four-step ladder replaces
   shadows", Fluent 2 ombre solo per ruolo, Vercel ombre card/hover/popover/modal distinte).
6. **Hero con un oggetto vivo**: numero live (NBIM), video atmosferico + pannelli (Legora),
   onda ambientale con fallback statico (Stripe), oggetto indicizzato allo scroll (Jeton).

---

## A. Servizi digitali governativi

### 1. GOV.UK + GOV.UK Design System
URL: https://www.gov.uk/ · https://design-system.service.gov.uk/styles/type-scale/ — governo
- **Eccellenza**: GDS Transport, brand #1d70b8, focus giallo #ffdd00 su testo #0b0c0c; scala
  tipografica 80/48/36/27/24/19/16 px con interlinee sempre multiple di 5 px; raggio 0; nessun
  effetto; IA per compiti ("Visas and immigration" come categoria di primo livello).
- **Da prendere**: la disciplina della scala e dell'interlinea; lo stato di focus non negoziabile;
  i compiti come porta d'ingresso.
- **Da non prendere**: l'austerità totale (è esattamente il registro respinto), la piattezza delle
  tile, l'assenza di gerarchia di superficie.

### 2. Migrationsverket (Svezia, nuovo sito 5 marzo 2025)
URL: https://www.migrationsverket.se/en.html — governo, dominio identico al nostro
- **Eccellenza**: ingressi per fase del percorso — "You want to apply / You want to extend /
  You are waiting for a decision / You have received a decision / You have a permit in Sweden /
  Leave Sweden"; card in evidenza per i cambi normativi datati ("On 6 June 2026 the rules…");
  Inter Regular/Medium/SemiBold; icone Font Awesome *thin/sharp*.
- **Da prendere**: l'IA per stadi del percorso (mappa diretta su NEED→…→INCLUSION); le card
  normative datate; il glossario ("Word explanations").
- **Da non prendere**: la resa visiva piatta, Inter come voce unica.

### 3. IND — Immigratie- en Naturalisatiedienst (Paesi Bassi)
URL: https://ind.nl/en — governo
- **Eccellenza**: hero "How can we help you?" con quattro card di situazione (permessi,
  appuntamento, stato pratica, guida); "My IND" e portali per avvocati/imprese/comuni separati
  nell'header; RijksoverheidSans (font di Stato).
- **Da prendere**: l'hero task-first con quattro ingressi (nostre quattro vie di accesso);
  la separazione esplicita persona / professionista / impresa.
- **Da non prendere**: tono burocratico, foto di cronaca (Ter Apel), raggi 5/6/10 px misti.

### 4. Designers Italia — UI Kit Italia, Bootstrap Italia v3 (beta 15 maggio 2026), Dev Kit Italia
URL: https://designers.italia.it/design-system/fondamenti/tipografia/ · /colori/ — PA italiana
- **Eccellenza**: Titillium Web (H1 40/48 px bold), Lora per testi lunghi, Roboto Mono per dati;
  Blu Italia #0066cc (5.56:1), accento teal #089994, slate #17324d, success #008055,
  warning #cc7a00, alert #cc334d; regole: 75 caratteri/riga, max 4 livelli di titolo,
  token pre-verificati WCAG 1.4.3/1.4.11; Dev Kit su web component (2026).
- **Da prendere**: la scala semantica verificata; il teal come accento "italiano non tricolore";
  il ceiling di 75 caratteri; il modello a token.
- **Da non prendere**: Titillium (fa leggere il sito come PA), Bootstrap Italia, il blu #0066cc
  come colore di marca (siamo un soggetto privato istituzionale, non una PA).

### 5. DSFR — Système de Design de l'État (Francia)
URL: https://github.com/GouvernementFR/dsfr (il sito risponde 403) — governo
- **Eccellenza**: coppia serif+sans di Stato (Marianne + Spectral); "bleu France / rouge
  Marianne"; dark mode nativo via `data-fr-scheme="system|light|dark"`; BEM, moduli ES.
- **Da prendere**: sans istituzionale + serif editoriale come sistema; dark scheme come attributo
  di primo livello, non come tema aggiunto.
- **Da non prendere**: il DSFR stesso (uso vietato fuori da .gouv.fr), la bandiera.

### 6. e-Residency of Estonia
URL: https://www.e-resident.gov.ee/ — programma di Stato con marketing di prodotto
- **Eccellenza**: font proprietario Aino / Aino Headline; H1 "your digital id, your company,
  your freedom"; raggio 1 rem coerente; ease `cubic-bezier(.215,.61,.355,1)`, 200–300 ms.
- **Da prendere**: la prova che un servizio pubblico può avere voce e tipografia proprie senza
  perdere legittimità.
- **Da non prendere**: tono da startup, WordPress.

### 7. KERN UX-Standard (Germania, prodotto dell'IT-Planungsrat dal 1° gennaio 2027)
URL: https://www.kern-ux.de/ · https://docs.fitko.de/resources/kern/ — governo
- **Eccellenza**: "Barrierefreiheit by Design (WCAG, EN 301 549, BITV 2.0)"; colori e font
  scelti in co-creazione e **validati con un sondaggio rappresentativo della popolazione**
  (fonte: move-online.de, hamburg.de); 650+ esperti in community.
- **Da prendere**: il metodo — validare palette e font con utenti reali, non solo con il contrasto.
- **Da non prendere**: nulla di visivo (font/colori non esposti senza JS: non verificato).

## B. Istituzioni europee e internazionali

### 8. Europa Component Library (ECL v4) + european-union.europa.eu + ECB
URL: https://ec.europa.eu/component-library/eu/guidelines/typography/ · /colours/ ·
https://european-union.europa.eu/index_en · https://www.ecb.europa.eu/ — istituzioni UE
- **Eccellenza**: ECL: Arial, solo peso 400, base 16 px, interlinee "always divisible by 4",
  80 caratteri desktop / 40–60 mobile, Primary #0E47CB, Secondary #FFCC00, Dark-100 #262B38,
  success #00A174, error #D7003D; ECB: Open Sans + set icone proprietario `ECB-icon-set`,
  mega-menu, sezione "In focus", raggi 15/20 px.
- **Da prendere**: il ritmo a 4 px e i limiti di caratteri; il set icone come asset di marca;
  la gerarchia "In focus" per le novità normative.
- **Da non prendere**: Arial/peso unico (austerità), il giallo UE, la homepage-notiziario.

### 9. EUI — European University Institute (Firenze)
URL: https://www.eui.eu/ — istituzione europea in Italia
- **Eccellenza**: palette di territorio senza tricolore: blu #0E4876, verde oliva #8F942F,
  terracotta #C85826, giallo sabbia #F1C46F, nero #131516; Inter + Nunito Sans.
- **Da prendere**: oliva/terracotta/sabbia come "italianità" desaturata.
- **Da non prendere**: Bootstrap 5 di serie, quattro colori pieni sulla stessa pagina.

### 10. NBIM — Norges Bank Investment Management
URL: https://www.nbim.no/en/ — organizzazione finanziaria pubblica
- **Eccellenza**: hero con il valore del fondo come numero grande e vivo; canvas avorio caldo
  `--color-background:#faf9f5`; navy #03217f, blu elettrico #0026ff, cielo #3e9dff,
  #c5dfff; font proprietario "NorgesBank"; `prefers-reduced-motion` presente; raggi 4 px.
- **Da prendere**: avorio caldo + navy + un solo blu luminoso; il numero vivo come hero
  istituzionale (per noi: pratiche in corso, tempi, scadenze — non denaro).
- **Da non prendere**: quattro blu in scala (ne basta uno interattivo).

### 11. Banche centrali e organizzazioni (Bank of England, BIS, World Bank)
URL: https://www.bankofengland.co.uk/ · https://www.bis.org/ · https://www.worldbank.org/
- **Eccellenza**: BoE: Gilroy proprietario ("GilroyForBOE") su navy #12273f; BIS: Manrope
  display + Open Sans, accento #aa322f, ease `(0,0,.25,1)`×41; World Bank: Open Sans + Roboto
  Mono, scala indigo #f5f6ff→#0a1885 per dati.
- **Da prendere**: navy profondo come autorità; Manrope come display sobrio; scala indigo
  a 9 passi per dataviz.
- **Da non prendere**: BoE usa `cubic-bezier(0.52,1.64,0.37,0.66)` (overshoot) 10 volte:
  il rimbalzo è il contrario di istituzionale.

### 12. The Nobel Prize
URL: https://www.nobelprize.org/ — istituzione culturale
- **Eccellenza**: famiglia proprietaria a tre voci — Alfred Sans, Alfred Serif Text, Alfred
  Sans Mono (regular/bold/italic) — una sola identità per titoli, lettura e dati.
- **Da prendere**: il modello "una famiglia, tre voci" (sans / serif / mono) come base del
  sistema tipografico.
- **Da non prendere**: WordPress + Splide (carousel) come struttura di homepage.

## C. Legal-tech

### 13. Legora (rebrand 2026, identità Stockholm Design Lab, sito E&W Studio)
URL: https://www.legora.com/ · https://www.ew.studio/work/legora-2026 — legal-tech
- **Eccellenza**: nel markup Suisse Int'l (Book/Regular/Medium) + **Rhymes Display Thin/Regular**
  (serif display sottilissimo) + Inter; Lenis per lo scroll; costruito in Framer. Il case study
  descrive "layered hero background with parallax", "floating UI panels" in vetro smerigliato
  su fotografia atmosferica ("warm lighting, tan leather, stone"), video hero di ManvsMachine,
  vignette disegnate da Robert Leighton per "bilanciare l'identità digitale affilata".
  Hero: "Legal work, without limits." Navigazione: Product, Solutions, Security, Customers.
- **Da prendere**: serif display leggero + grotesk svizzero; materiali caldi (cuoio, pietra)
  invece di navy freddo; umorismo disegnato per umanizzare il rigore.
- **Da non prendere**: Framer (CSP `script-src 'self'`), vetro su ogni pannello, ordine sezioni
  "aOS → innovazioni → practice areas → ROI → founder → badge" (template SaaS).

### 14. Harvey
URL: https://www.harvey.ai/ — legal-tech
- **Eccellenza**: Harvey Sans (Diatype variabile) + Harvey Serif; `theme-color #1F1D1A`
  (quasi-nero caldo); scala grigi calda #fafaf9 → #f2f1f0 → #e5e5e3 → #cccac6 → #adaba5 →
  #8f8b85 → #706d66 → #524f49; accenti "dark-bronze #593d3a, dark-casal #333f40,
  dark-velvet #373340"; ease `(0,.7,.3,1)` / `(.7,0,.3,1)`, 150/300 ms;
  `prefers-reduced-motion` nel CSS. Hero: "Build a Frontier Legal Organization".
- **Da prendere**: inchiostro caldo + avorio + bronzo/velluto scuri = premium legale senza
  navy; una sola coppia di curve (out / in-out) usata ovunque.
- **Da non prendere**: la sequenza loghi → card → carosello → metriche → badge SOC2.

### 15. Luminance · Juro (secondo livello legal-tech)
URL: https://www.luminance.com/ · https://www.juro.com/
- **Eccellenza**: Luminance: PP Mori (Heavy/Regular/Bold) + Geist Mono per dati; Juro: GT
  Walsheim + Cera Pro + Kazimir (serif) su verde profondo #033f2f/#006853, raggi 1.6 rem.
- **Da prendere**: mono per numeri e riferimenti normativi; verde profondo come alternativa
  al navy (con cautela: vedi MOODBOARD).
- **Da non prendere**: tre famiglie sans insieme; raggi 24 px su tutto; Lottie decorativo.

## D. Fintech

### 16. Stripe + stripe.dev
URL: https://stripe.com/ · https://stripe.dev/ · https://designmd.cc/benchmarks/stripe
- **Eccellenza**: `sohne-var` + Source Code Pro; token `--hds-*`; display 48 px peso 300, H1
  32/400; testo #061b31, muted #50617a, superficie #f8fafd, bordo #e5edf5; ombra card
  `0 3px 6px rgba(23,23,23,.06)`, hover `0 15px 35px .08`; ease `(.25,1,.5,1)`×12;
  `prefers-reduced-motion` presente. L'onda-gradiente è **una** animazione ambientale con
  fallback statico (regola citata da utsubo.com: "one ambient animation plus one user-triggered
  interaction"). stripe.dev cambia registro: Times New Roman + token "W95" + evidenziatore
  #c4e817.
- **Da prendere**: la regola "un'animazione ambientale + un'interazione"; ombre per stato
  (riposo/hover) non per decorazione; un sotto-brand con registro diverso (per noi: Academy).
- **Da non prendere**: il gradiente arcobaleno #533afd→#da56ed→#ec8fff.

### 17. Mercury
URL: https://mercury.com/ · https://designmd.cc/benchmarks/mercury
- **Eccellenza**: Arcadia / Arcadia Display a **pesi 480 e 420**, Tiempos Headline/Fine per i
  momenti editoriali, IBM Plex Mono; canvas #171721 / #1e1e2a / #272735, inchiostro #ededf3,
  **un solo accento #5266eb** per "Open account"; tracking positivo +0.01/+0.02 em; raggi
  4 px input vs 32/40 px bottoni; ease `(.16,0,.13,1)`, `(.2,1,.4,1)`; GSAP nel markup;
  `prefers-reduced-motion`. Sezioni: hero → 4 capacità → 3 testimonianze → 4 demo → metriche.
- **Da prendere**: "un accento per l'unica azione"; pesi intermedi; serif solo nei momenti
  editoriali; buio cinematografico indaco (non nero).
- **Da non prendere**: pillole ovunque; dark-only; il modello bancario per un servizio legale.

### 18. Wise (rebrand Ragged Edge)
URL: https://wise.com/ · https://raggededge.com/partnerships/wise
- **Eccellenza**: Wise Sans Heavy (display, "ispirato a scritture di tutto il mondo", 960
  lingue) + Inter variabile; verde #9fe870 su foresta #1c3108/#111f06; "tapestries" grafiche;
  146 lingue, 200 opzioni colore testate, dichiarato oltre WCAG 3.0; ease `(.6,.2,.1,1)`×63,
  `(0,.94,.62,1)`×24; Lottie; Barba (transizioni) nel markup.
- **Da prendere**: accessibilità come claim di marca; un solo display face "firma"; sistema
  multilingua nativo.
- **Da non prendere**: verde acido (per noi legge "bandiera"), display heavy, tapestries.

### 19. Adyen
URL: https://www.adyen.com/ — fintech enterprise
- **Eccellenza**: famiglia proprietaria AdyenTPJ / AdyenSC / AdyenMono; scala "black" che è in
  realtà navy-inchiostro: #001222 → #0d1e2e → #1a2b3b → #2f3e4d → #5c6874 → #848d96 →
  #ecedef → #f4f5f6; raggio 8 px ×72; ease `(.33,1,.68,1)`, `(.19,1,.22,1)`; `.15s`×393.
  H1 "Fintech you can bank on".
- **Da prendere**: scala inchiostro-navy (mai nero puro) e un solo raggio dominante.
- **Da non prendere**: il ritmo a blocchi enterprise.

### 20. Jeton (Bürocratik, Awwwards Site of the Day)
URL: https://www.awwwards.com/case-study-jeton-by-burocratik.html
- **Eccellenza**: un solo oggetto-hero (dispositivo che si trasforma) **indicizzato allo scroll**
  con Rive; GSAP per il resto; Lenis; "almost ditched black from the CSS" per contrasto;
  hanno evitato "overwhelming autoplay animations"; 19 lingue.
- **Da prendere**: un oggetto narrativo legato allo scroll, senza autoplay; il rifiuto del nero.
- **Da non prendere**: Matter.js per bandiere che rimbalzano, 3D per "tangibilità".

### 21. Cash App Design (portale di marca)
URL: https://design.cash.app/ — fintech
- **Eccellenza**: portale in tre sezioni — Foundations (Logo, Color, Typography, **Motion**,
  Iconography, Voice), Expressions, Resources (Tokens, Components); Cash Sans; verde #00d533;
  transizioni di pagina via swup.
- **Da prendere**: Motion come *fondamento* documentato al pari di colore e tipografia.
- **Da non prendere**: `cubic-bezier(1,0,0,1)` e `(.86,0,.07,1)` (curve teatrali).

## E. SaaS enterprise e dev-tools

### 22. Linear
URL: https://linear.app/ · https://linear.app/now/how-we-redesigned-the-linear-ui ·
https://designmd.cc/benchmarks/linear
- **Eccellenza**: Inter Variable a pesi **590/510**, tracking display fino a −3 px; canvas
  #08090a con scala superfici #0f1011 → #141516 → #18191a e hairline #23252a → #34343a: "four-step
  ladder replaces shadows"; un solo accento lavanda #5e6ad2 "never decoratively"; active
  `scale(0.97)`; focus `0 0 0 3px rgba(94,106,210,.3)`; temi generati in **LCH** con
  "elevations for surfaces (background, foreground, panels, dialogs, modals)"; **variabili di
  contrasto** per temi ad altissimo contrasto; Inter Display per i titoli.
- **Da prendere**: scala superfici + hairline; LCH; variabili di contrasto; pesi intermedi.
- **Da non prendere**: il "Linear look" (LogRocket: "almost every SaaS website looks the
  same"), dark-first, sfumature lavanda nell'hero.

### 23. Vercel Geist
URL: https://vercel.com/geist/introduction · https://designmd.cc/benchmarks/vercel
- **Eccellenza**: Geist Sans/Mono + famiglia Geist Pixel (2025–26); "Materials — presets for
  radii, fills, strokes, shadows"; scala grigi `--accents-1…8`; ombre per ruolo: card
  `0 1px 2px .05`, hover `0 0 0 1px .1, 0 4px 12px .08`, popover, modal `0 8px 16px -4px…,
  0 24px 32px -8px…`; `.2s ease-out`, link `.15s`.
- **Da prendere**: i "materials" come preset unici; ombre nominate per ruolo, non per intensità.
- **Da non prendere**: monocromia bianco/nero totale (per noi troppo "dev").

### 24. Raycast · Clerk · Resend (dettagli da rubare, non modelli)
URL: https://www.raycast.com/ · https://clerk.com/ · https://resend.com/
- **Eccellenza**: Raycast: `backdrop-filter`×12 solo su superfici fluttuanti (palette comandi),
  Instrument Serif come accento, raggio 12 px; Clerk: Suisse Int'l + Söhne Mono + "Geist
  numbers" (font dedicato ai numeri tabellari); Resend: ABC Favorit + Domaine (serif) + Commit
  Mono, scale colore Radix con alfa (`--amber-a1…a12`).
- **Da prendere**: vetro **solo** su elementi fluttuanti; un font/feature per numeri tabellari;
  scale alfa per superfici scure.
- **Da non prendere**: Raycast usa `(.34,1.56,.64,1)` (overshoot) — no.

## F. Atenei e istituzioni culturali

### 25. ETH Zürich
URL: https://ethz.ch/en.html — università
- **Eccellenza**: DINPro; `theme-color #007894` (petrolio); **scale colore per dipartimento**
  (`--color-theme-10…120`: #e7f4f7→#00596d, #e9eff7→#08407e, #eff1e7→#365213,
  #f4f0e7→#704f12…); micro-durate 80/160 ms; raggi 0/2 px.
- **Da prendere**: teal-petrolio come accento istituzionale; scale tematiche per area
  (le nostre quattro vie: Orientamento / Formazione / Ingresso / Inclusione); durate brevi.
- **Da non prendere**: homepage-notiziario; nessun `prefers-reduced-motion` nel CSS.

### 26. MIT
URL: https://www.mit.edu/ — università
- **Eccellenza**: Neue Haas Grotesk Display/Text; **una sola curva** `(.215,.61,.355,1)`
  (easeOutCubic) ×126; durate .2/.3/.35 s; raggi 0.
- **Da prendere**: una curva, tre durate: coerenza cinetica totale.
- **Da non prendere**: assenza di reduced-motion.

### 27. Bocconi · Politecnico di Milano · Sciences Po
URL: https://www.unibocconi.it/en · https://www.polimi.it/en · https://www.sciencespo.fr/en/
- **Eccellenza**: Bocconi: Inter + Playfair Display, video hero "We Made It", "Key facts"
  (1 su 3 studenti finanziati, €55M); Polimi: Manrope 500/700; Sciences Po: Inter + Montserrat.
- **Da prendere**: il blocco "fatti chiave" con numeri; video muto come sfondo di hero.
- **Da non prendere**: Playfair/Montserrat (cliché), `ease-in-out-quad`×32 (Bocconi),
  TYPO3/Bootstrap, raggi 2 rem.

### 28. UC Investments (SiteInspire, 10 settembre 2026)
URL: https://invest.universityofcalifornia.edu/ — istituzione finanziaria universitaria
- **Eccellenza**: ABC Whyte / Whyte Inktrap + Lyon Display / Lyon Text + Söhne Schmal; hero
  ridotto a "Our Way — UC Investments 2023–2024 — Read the Report"; monocromia #222/#c7c7c7;
  `prefers-reduced-motion` presente; durate 1 s ×26 (lente, editoriali).
- **Da prendere**: un rapporto annuale trattato come oggetto editoriale premium; inktrap
  display + serif di testo.
- **Da non prendere**: durate di 1 s nel prodotto (solo in un rapporto narrativo).

## G. Mobilità e territorio marocchino

### 29. Eurostar (rebrand DesignStudio 2023)
URL: https://www.eurostar.com/uk-en — mobilità
- **Eccellenza**: ABC Social (Regular/Bold) + **La Pontaise** (Or Type, serif ad alto
  contrasto); widget di prenotazione persistente a tre tab come hero; ritaglio immagini con
  focal point (`fp-x/fp-y`); CMS Sanity; `prefers-reduced-motion` presente.
- **Da prendere**: serif ad alto contrasto + sans umanista; lo strumento (non il claim) come
  hero; focal point sulle foto.
- **Da non prendere**: densità promozionale ("from £39", "up to 50% off").

### 30. ONCF · Maroc.ma · Royal Air Maroc (lato marocchino)
URL: https://www.oncf.ma/ · https://www.maroc.ma/en · https://www.royalairmaroc.com/
- **Eccellenza**: ONCF dichiara `Helvetica-Neue-Roman-Arabic` e `Helvetica-Neue-Bold-Arabic`
  come compagni arabi; Maroc.ma usa Manrope/Nunito/Montserrat con **Cairo Bold** per l'arabo,
  ease `(0.19,1,0.22,1)`; RAM è Liferay su font di sistema.
- **Da prendere**: l'evidenza che il compagno arabo va dichiarato esplicitamente per ogni
  voce tipografica; Cairo/Helvetica Neue Arabic come riferimenti d'uso locale.
- **Da non prendere**: Georgia di ripiego (ONCF), quattro famiglie latine (Maroc.ma),
  raggi 10 px ×104.

## H. Architettura, editoria, dataviz

### 31. BIG · Snøhetta
URL: https://big.dk/ · https://snohetta.com/ — architettura
- **Eccellenza**: BIG: Everett, grigio #898989, ease `(0,0,.25,1)`, stringhe swup/barba
  nel markup (transizioni: non verificato a schermo); Snøhetta: Dovre Social Light
  (peso leggero come voce), **tema doppio a token** (`--color-background #000/#fff`,
  `--color-area-bg #1e1e1e/#f3f3f3`, `--color-stroke #404040/#dfdfdf`), accento #42ff00, Lottie.
- **Da prendere**: token di area (`area-bg`) e tratto (`stroke`) per il ritmo dark/light;
  display leggero.
- **Da non prendere**: accento fluo; assenza di reduced-motion.

### 32. The Pudding · Our World in Data · Monocle
URL: https://pudding.cool/ · https://ourworldindata.org/ · https://monocle.com/
- **Eccellenza**: Pudding: Atlas Grotesk + Atlas Typewriter + Tiempos Text + Gooper
  SemiCondensed, Svelte, scrollytelling; OWID: grafici dentro la prosa con "Explore the data"
  e contesto testuale **prima** del grafico; Monocle: Helvetica Neue + Plantin.
- **Da prendere**: scrollytelling per il processo NEED→INCLUSION; il grafico introdotto dal
  testo; serif classica + grotesk per l'Academy.
- **Da non prendere**: la palette Pudding (#4717f6, #3AE660) — è giornalismo, non istituzione.

## I. Agenzie contemporanee

### 33. Unseen Studio · Locomotive · Lusion · darkroom.engineering · Instrument
URL: https://unseen.co/ · https://locomotive.ca/en · https://lusion.co/ ·
https://darkroom.engineering/ · https://www.instrument.com/
- **Eccellenza**: Unseen (Studio of the Year Awwwards): Neue Montreal + Saol Display Light/
  Italic — grotesk + serif leggero; Locomotive: LocomotiveNew + Helvetica Now Display,
  locomotive-scroll, easeOutCubic ×43, `.3s`; Lusion: Aeonik + IBM Plex Mono, coppia
  `(.4,0,.1,1)` / `(.35,0,0,1)`, `.4s`; darkroom (autori di Lenis): Lenis + GSAP + three.js;
  Instrument: Instrument Sans/Serif/Mono (disponibili open) con tema doppio #070708/#fff.
- **Da prendere**: la coppia grotesk + serif leggero; due curve nominate (entrata/uscita) e
  basta; Instrument come trio open source di riserva.
- **Da non prendere**: WebGL 3D (Lusion), hover che diventano "esperienza" (Unseen), smooth
  scroll globale su pagine di compito (Lenis va limitato alle pagine IMMERSIVE).

## L. Librerie e cataloghi di componenti (idiomi correnti)

### 34. Motion — motion.dev/ui e motion.dev/examples
URL: https://motion.dev/ui/hero-sections · https://motion.dev/examples · https://motion.dev/docs/scroll
- **Eccellenza**: quattro hero canonici — *Editorial Stagger* (reveal riga per riga mascherato
  al load), *Parallax Layers* (titolo e card più veloci della finestra prodotto, scroll-linked),
  *Terminal*, *Split Text*; catalogo con Scroll (16), Text (43), Page transitions (25),
  Curtains (blinds/wipe/iris/doors); `scroll()` usa **ScrollTimeline** con accelerazione
  hardware; distinzione esplicita scroll-linked vs scroll-triggered (`inView`).
- **Da prendere**: Editorial Stagger e Parallax Layers come base dell'hero; ScrollTimeline
  per il rail; `inView` per i reveal.
- **Da non prendere**: curtains/iris tra pagine di compito; scramble text.

### 35. 21st.dev (catalogo da leggere in negativo)
URL: https://21st.dev/community/components/s/hero-section
- **Osservato**: 102 hero ("Glow Horizon", "Aether Flow", "Animated Shader Hero", "Neural Vortex",
  "GLSL Hills", "Lamp"); il sito stesso usa `theme-color #09090b` (zinc-950 shadcn) e General Sans.
- **Da prendere**: nulla di visivo. **Da non prendere**: shader, vortici, glow (vedi ANTI_PATTERNS).

## Fonti secondarie usate (verificate il 23/09/2026)
utsubo.com (fintech: "one ambient + one interaction") · blog.logrocket.com (omologazione "Linear")
· github.com/funboy322/avoid-ai-design ("AI slop") · select-interactive.com (trend 2026 vs budget)
· schoolofmotion.com (10 siti 2026) · rauno.me/craft/interaction-design ·
emilkowal.ski/ui/great-animations · designmd.cc (token di Linear, Mercury, Stripe, Vercel) ·
Design Week / Creative Review / It's Nice That (Eurostar, Wise) · W3C WCAG 2.2 Understanding
1.4.11, 2.3.3, 2.4.11, 2.5.8 · MDN prefers-reduced-motion · web.dev/articles/animations-guide ·
fluent2.microsoft.design/elevation · rtlstyling.com · apple.com/newsroom (Liquid Glass, 9/6/2025).
