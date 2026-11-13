# DESIGN COUNCIL V2 — Parere del Direttore Creativo Esecutivo / Art Director Digitale

Data: 23 settembre 2026 · Oggetto: direzioni A (Rete luminosa), B (Profondità architettonica), C (Diplomazia
contemporanea) · Prove: `docs/design-v2/council/shots/cd/` (Chromium headless proprio; 1440×900 a 4,5 s,
pagina intera dopo scroll completo, 390×844; sonde a 400/1200/2400 ms, tab-focus, `reduced-motion` a 300 ms,
ritagli della porta, sezione processo a due profondità di scroll). Baseline respinta: `docs/design-v2/before/`.

Premessa di metodo. Ho giudicato quello che si vede, non quello che i DIRECTION.md promettono. Il mandato del
committente è chiaro: «istituzionale ≠ trattenuto». Ho quindi penalizzato la prudenza tanto quanto lo spettacolo
gratuito, e ho misurato ogni direzione su una domanda sola: **senza il logo, uno screenshot resta nostro?**
Contro la baseline (`before/home_desktop.png`: piastra navy + wordmark + sei sezioni numerate uguali;
`before/person_dashboard_desktop.png`: registro a sette sezioni con sidebar piatta) tutte e tre le direzioni sono
un salto reale. Nessuna delle tre è pronta a spedire.

Scala: 1–10. «n.g.» = non giudicabile dalle prove raccolte. ACCESSIBILITÀ è parziale ovunque: ho verificato
focus visibile (3/3), stato ridotto completo al primo paint (3/3), 0 errori console, 0 overflow; non ho eseguito
axe, lettore di schermo né RTL.

---

## Direzione A — «Rete luminosa»

| WOW | PREMIUM | MODERNITÀ | CRED. IST. | ORIGINALITÀ | MOTO | TIPOGRAFIA | COMPOSIZIONE | COERENZA | PLATFORM UX | MOBILE | A11Y |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 8 | 8 | 8 | 7 | 7 | 8 | 7 | 8 | 8 | 8 | 8 | 7 (parz.) |

**Porta e logo.** È la direzione che evolve davvero la porta: non la decora, la promuove a **nodo centrale** di
una rete di attori nominati (persona, organismo di formazione, università, impresa, istituzione, autorità
competente) con «Maroc» e «Italie» agli antipodi (`a_doorway_1440_crop.png`, `a_home_1440_fold.png`). La
fotografia al 50 % è finalmente leggibile — le statue della fontana danno il registro «monumento», cioè
istituzione — e i tre gradini in blu luminoso legano la porta alle linee. Il lock-up tricolore vive su carta,
intatto. La coreografia è giusta e già senza il difetto di primo paint: a 400 ms la porta è intera, a 1 200 ms
il percorso principale si sta tracciando, a 2 400 ms la rete è completa (`a_hero_t400/1200/2400.png`).

**Cinque punti di forza**
1. L'hero racconta il prodotto in un'immagine: *gli attori convergono sulla porta regolare*. È l'unico dei tre
   in cui la metafora (percorso · connessione · struttura legale · istituzioni · cooperazione) è tutta nel fold.
2. Il processo NEED → INCLUSION come onda che si disegna con lo scroll, con responsabile per tappa e territorio, e
   sotto la **striscia di giurisdizione** con texture e legenda (`a_process_1440_p2.png`): componente firma vero.
3. Il fascicolo apre con una **testata inchiostro** dentro il workspace avorio: titolo serif, riferimento mono,
   quattro fatti, e il **rail 2.0 più maturo** dei tre (texture per responsabile, glifo, «Vous êtes ici»,
   confine MA → IT tratteggiato, legenda) (`a_dashboard_1440_fold.png`).
4. La shell della piattaforma è la più completa: ricerca `Ctrl K`, rail comprimibile, badge, promemoria antifrode;
   su mobile diventa striscia di tab e rail verticale senza perdere nulla (`a_dashboard_390_full.png`).
5. Mobile: la porta come copertina con la rete ritagliata e senza etichette, poi il titolo — la scelta giusta
   (`a_home_390_fold.png`). Un solo capitolo inchiostro per pagina, un solo blu interattivo: la disciplina c'è.

**Cinque difetti**
1. Le quattro vie sono **card da catalogo**: icona in quadratino arrotondato, titolo, testo, link
   (`a_home_1440_s2.png`). Il bus con il marchio-hub le salva a metà; da sole leggono shadcn.
2. Nel bar della piattaforma il marchio sta nudo sull'inchiostro: l'arco navy sparisce (1,24:1), restano due
   piani verde/rosso e un tratto bianco (`a_dashboard_1440_fold.png`, in alto a sinistra).
3. Rete dell'hero: due nodi «Université» (uno per sponda?) senza distinzione e etichette a ~8 px
   (`a_home_1440_fold.png`). Chi non legge il DIRECTION.md legge un doppione.
4. Allineamenti: le stazioni del processo hanno baseline sfalsate (01/03/05 in alto, 02/04/06 in basso) e le
   etichette del rail 2.0 nel fascicolo non sono allineate in alto (`a_process_1440_p1.png`,
   `a_dashboard_1440_fold.png`). Legge come disordine, non come onda.
5. Il titolo bloccato **ITALY LEGAL ENTRY™** è retrocesso a riga grotesk di 24 px sotto un display serif che è
   in realtà il lead: gerarchia invertita rispetto alla baseline e a B/C. Il footer è una riga sola, sottile
   (`a_home_1440_full.png`, in fondo). Manca l'ispettore contestuale nel fascicolo. La scheda Forum in vetro
   sotto il fold aggiunge rumore all'hero. «A doorway, not a shortcut» resta in inglese.

**Must-fix prima di spedire**: marchio su tessera avorio nei bar scuri (come B/C) · glifi proprietari a tratto
1,5 px al posto delle icone in quadrato, mantenendo il bus · nodi distinti (Université · Maroc / · Italie) ed
etichette ≥ 10 px · baseline delle stazioni e delle tappe del rail allineate in alto · decisione sulla gerarchia
del titolo (vedi sintesi) · ispettore destro nel fascicolo · footer composto (lock-up, sede/coordinate, legale,
navigazione) · didascalia in francese · scheda Forum spostata in una banda di sezione · derivati AVIF/WebP della
fotografia (vale per tutte e tre).

---

## Direzione B — «Profondità architettonica»

| WOW | PREMIUM | MODERNITÀ | CRED. IST. | ORIGINALITÀ | MOTO | TIPOGRAFIA | COMPOSIZIONE | COERENZA | PLATFORM UX | MOBILE | A11Y |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 5 | 7 | 5 | 8 | 6 | 5 | 7 | 6 | 7 | 6 | 5 | 7 (parz.) |

**Porta e logo.** La più fedele all'originale (fondo sabbia → carta, doppio tracciato, gradini navy) e per questo
la meno evoluta: la fotografia al 34 % su avorio diventa una filigrana lattiginosa, i gradini quasi spariscono,
e le linee di piano della griglia **attraversano la didascalia** (`b_doorway_1440_crop.png`). Su mobile la
porta è **sotto il fold**: il primo schermo è titolo + lead + paragrafo + due bottoni, cioè la baseline
respinta in chiaro (`b_home_390_fold.png` vs `before/home_mobile.png`). Il lock-up su targhetta avorio nel bar
scuro è invece la soluzione corretta, da prendere.

**Cinque punti di forza**
1. Il sistema è il più rigoroso: sette piani con un token ciascuno, gradini tonali invece di ombre, tre curve,
   quattro durate. È il DS meglio scritto dei tre.
2. Le quattro vie come **soglie a gradoni** (0/32/64/96 px) con ordinale serif 200 a 64 px e architrave
   colorata: una scala, non quattro card (`b_home_1440_s2.png`). L'idea più forte di B.
3. Il processo come **disegno in sezione** appuntato — sei piani prospettici con la porta di ogni livello e
   la linea che li attraversa (`b_process_1440_p2.png`): concettualmente il più originale dei tre.
4. Il rail 2.0 letto in **due gruppi** — Maroc · avant le départ / Italie · procédures et inclusion — con
   «Étape 2 sur 7» in testo: la lettura semantica più chiara (`b_dashboard_1440_fold.png`).
5. Il piano di lavoro a tre colonne indice · main · ispettore, con la targa del dossier su due piani, è la
   struttura di fascicolo richiesta dalla brief.

**Cinque difetti**
1. **Il fold non fa niente.** Avorio, serif sottile, paragrafo, bottoni, porta sbiadita: è la direzione che il
   committente ha già respinto, con più gusto (`b_home_1440_fold.png`). Per 400 ms la colonna destra è un
   rettangolo beige vuoto; a 1 200 ms la porta è un fantasma grigio con un alone (`b_hero_t400.png`,
   `b_hero_t1200.png`): la «mise en registre» dura troppo e mostra stati brutti.
2. Newsreader 260 a 88 px legge rivista di moda, non diritto; i titoli delle soglie in serif leggero
   MAIUSCOLO sono deboli (`b_home_1440_s2.png`). Su ClearType peggiorerà (lo ammettono).
3. Piattaforma: sul desktop la navigazione **non è nel fold** (`b_dashboard_1440_fold.png`); su mobile
   compare a metà pagina come lista di chip, senza bottone Menu (`b_dashboard_390_full.png`). L'indice
   numerato 01–10 è l'eco del registro respinto.
4. Il disegno in sezione, per come è tracciato (parallelogrammi uguali, porte-rettangolino), legge «stack di
   livelli» da diagramma SaaS; e 6 × 54 vh di capitolo scuro sono metà della pagina di vuoto
   (`b_home_1440_full.png`).
5. Footer a quattro colonne generico; scaletta della porta 120 → 1 560 ms fuori dal budget «< 300 ms» del prodotto.

**Must-fix**: porta presente e leggibile nel fold (foto ≥ .5, sequenza ≤ 900 ms, nessuno stato-fantasma) ·
porta sopra il fold su mobile · navigazione della piattaforma nel fold su desktop e nel bar su mobile ·
Newsreader 300, titoli delle soglie in sentence case o sans 500 · linee di piano mai sotto il testo · disegno in
sezione con più mestiere (spessori, porte riconoscibili, luce) e capitoli più corti · footer composto.

---

## Direzione C — «Diplomazia contemporanea»

| WOW | PREMIUM | MODERNITÀ | CRED. IST. | ORIGINALITÀ | MOTO | TIPOGRAFIA | COMPOSIZIONE | COERENZA | PLATFORM UX | MOBILE | A11Y |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 8 | 8 | 9 | 6 | 7 | 7 | 8 | 8 | 8 | 7 | 8 | 7 (parz.) |

**Porta e logo.** Ben integrata: la porta è la **soglia fra due rive**, la rotta entra dietro la spalla sinistra
e riemerge oltre la volta; tracciato teal, gradini teal, foto al 50 % desaturata, didascalia finalmente in
francese («Une porte, pas un raccourci») (`c_doorway_1440_crop.png`). Letterhead su carta con lock-up intatto e
selettore FR · IT · EN · ع; marchio su tessera nei bar scuri. Il bagliore della chiave qui è il più discreto.
Nel fascicolo la banda di isoipse nella testata dà continuità sito → piattaforma (`c_dashboard_1440_fold.png`).

**Cinque punti di forza**
1. L'atmosfera più forte e il momento tipografico migliore dei tre: **ITALY LEGAL ENTRY™** in Newsreader 300
   a 100 px avorio su mezzanotte, lead corsivo, coordinate mono delle due rive in chiusura
   (`c_home_1440_fold.png`). Legge organizzazione internazionale del 2026.
2. Le quattro vie a **zig-zag 7/5 · 5/7** con ordinale serif, etichetta mono e glifi-isoipsa propri (picco,
   onda, terrazze, cresta): la soluzione più originale al «non quattro card» (`c_home_1440_s2.png`).
3. Hero già completo a 400 ms (`c_hero_t400.png`), porta visibile dal primo paint, «Suspendre le mouvement»
   come controllo reale del loop: è la direzione che prende il moto ridotto più sul serio.
4. Shell a tre regioni con **ispettore** (pré-évaluation, messaggi, scadenze, account) e case band con misuratore
   a cinque tacche; su mobile la striscia di tab resta nel fold (`c_dashboard_390_fold.png`).
5. Mobile home: porta-copertina intera con tracciato teal, poi titolo; il processo in lista con dorsale
   (`c_home_390_full.png`). Nessuno scroll orizzontale, ritmo pulito.

**Cinque difetti**
1. **Registro**: teal su mezzanotte + isoipse + graticola è il vocabolario dei siti dev-tool/crypto del 2025–26,
   e il layer nasce dichiaratamente da «Luminous Topography» di 21st.dev. Un occhio allenato lo riconosce.
   Con hero scuro + processo scuro + footer scuro la pagina è ~60 % buio (`c_home_1440_full.png`): viola il
   principio «un capitolo inchiostro» e scivola verso «dark mode = premium».
2. Le isoipse decorative passano **dietro il testo** dei pannelli via («Entreprise», righe 2–3)
   (`c_home_1440_s2.png`): contrasto e leggibilità.
3. Il processo come linea che sale da sinistra in basso a destra in alto è il **grafico di crescita** universale
   (`c_process_1440_p2.png`): bello, ma dice «trend», non «procedura».
4. Il rail 2.0 è schiacciato nella colonna centrale: sette tappe a 13 px su tre righe, marcatore «attuale»
   minuscolo (`c_dashboard_1440_fold.png`). Stati vuoti e nota legale con bordo tratteggiato leggono wireframe.
5. I titoli delle quattro vie sono in sentence case nel markup, mentre baseline, A e B li rendono MAIUSCOLI:
   da verificare contro la stringa bloccata. Tagline a 8,5 px nell'header mobile (illeggibile); nav a otto voci
   + bottone «Orientation» già stretta a 1 240 px.

**Must-fix**: un solo capitolo scuro (processo su minerale con SVG in teal-700, come già propongono; footer
chiaro) · teal solo territorio oppure inchiostro più caldo per allontanarsi dal dark-SaaS · isoipse mai sotto
testo · rail 2.0 a piena larghezza nel case band o sopra il workspace · profilo del processo non monotono
crescente (le due rive con una fascia-mare in mezzo) · bordi tratteggiati → hairline · casing delle vie
verificato · tagline nascosta < 480 px · nav ridotta o mega-menu.

---

## Classifica

**1. A — Rete luminosa · 2. C — Diplomazia contemporanea · 3. B — Profondità architettonica.**

A vince perché è l'unica in cui i quattro componenti firma esistono *tutti* come oggetti riconoscibili e la
porta del committente diventa il centro di gravità della composizione invece di un'illustrazione a lato: senza
logo, l'hero e il fascicolo restano nostri. Sui quattro assi che la brief vieta di mediare — premium,
modernità, credibilità istituzionale, platform UX — A tiene 8/8/7/8, C 8/9/6/7, B 7/5/8/6. C è la più
memorabile e tipograficamente la più bella, ma la sua credibilità istituzionale è la più fragile: il suo
vocabolario è preso in prestito dalla tecnologia e la pagina è troppo buia. B è il sistema più rigoroso e il
concetto più originale (soglie, sezione), ma il risultato visibile rientra esattamente nel «trattenuto» che il
committente ha respinto, e ha i difetti di navigazione più gravi. Non premio A perché è sicura — non lo è:
il rischio «grafo di rete = tech» e «shell = SaaS» esiste — la premio perché è la più completa e la più
correggibile con interventi di mestiere, non di concetto.

## Sintesi raccomandata

Base: **A** — capitolo inchiostro con la porta-hub e la rete di attori, un solo blu luminoso su avorio, il
processo a onda con responsabili e la striscia di giurisdizione, la testata-fascicolo inchiostro con il rail 2.0
a texture, la shell con ricerca e rail comprimibile. Da **C**: il letterhead con selettore FR · IT · EN · ع, la
didascalia in francese, il controllo «Suspendre le mouvement» come pattern per ogni loop, le **quattro vie a
zig-zag con glifi proprietari** al posto delle card di A (il bus resta), l'**ispettore contestuale** e la banda di
continuità sito → piattaforma (un frammento della rete nella testata del fascicolo), la scheda del progetto
pilota accanto al processo, le coordinate delle due rive come etichette degli estremi dell'onda. Da **B**: la
lettura del rail in **due gruppi MA / IT** fusa con le texture di A, la targa del dossier con riferimento mono a
30 px, il marchio su tessera avorio nei bar scuri, il workspace a tre colonne, e la «soglia che si apre» come
micro-interazione di hover delle vie. Decisione per il committente: gerarchia dell'hero — la mia
raccomandazione è **ITALY LEGAL ENTRY™** in serif 300 grande (trattamento C, avorio su inchiostro) come H1
e «Le parcours *régulier*…» di A come lead a ~36 px: con la porta-hub, un secondo display compete e diluisce.
Vietato in sintesi: teal interattivo, secondo capitolo scuro, isoipse dietro testo, icone in quadrato,
Newsreader sotto 300, loop senza funzione dichiarata.

## Le tre frasi

1. A è l'unica direzione in cui la porta del committente smette di essere un'illustrazione e diventa il centro di
   gravità dell'intero sistema: tutti i percorsi vi convergono, e questo è una firma.
2. B ha il sistema più rigoroso e il concetto più originale, ma il suo fold è la baseline respinta con più gusto:
   il committente lo rifiuterebbe una seconda volta per la stessa ragione.
3. C è la più memorabile e la più bella tipograficamente, ma il suo vocabolario è preso in prestito dalla
   tecnologia: va tenuto per le vie, il letterhead, l'ispettore e la didascalia, non per il registro cromatico.
