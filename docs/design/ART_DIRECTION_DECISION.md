# ART DIRECTION DECISION

Decisione del direttore di prodotto e design · 20 settembre 2026 · **Vincolante**

---

## 1. La decisione

> **Direzione A — «Le Registre» (European Institutional Editorial) è la direzione scelta**,
> con tre innesti obbligatori da B e cinque da C, nominati e non negoziabili.

Non è un compromesso fra tre proposte. È una direzione, con correzioni specifiche a difetti
specifici che i giudici hanno saputo indicare.

---

## 2. Come si è votato

Quattro giudici indipendenti, ciascuno con un mandato diverso, nessuno dei quali aveva scritto una
direzione. Dieci criteri, punteggio su 100.

| Giudice | Mandato | Voto | A | B | C |
|---|---|:-:|:-:|:-:|:-:|
| Credibilità istituzionale | il rischio di sembrare un governo o una startup | **A** | **89** | 85 | 88,5 |
| Design indipendente | sofisticazione e originalità | **B** | 84 | **85** | 85 |
| Ingegneria | costruibilità su 169 template, quattro lingue, AA | **C** | 83 | 71 | **83** |
| Prodotto | serve i sei ruoli, incluso un fascicolo denso | **C** | 82 | 77 | **83** |
| **Totale** | | | **338** | **318** | **339,5** |

A e C distano **1,5 punti su 400**. Un pareggio. B resta indietro, e va detto che il suo documento è
arrivato troncato a metà: il giudice di prodotto ha annotato che quel 77 «riflette materiale visibile
forte e una metà illeggibile, non un giudizio che la metà mancante sia debole».

Un pareggio non si risolve con l'aritmetica. Si risolve leggendo che cosa hanno scritto i giudici.

---

## 3. Perché A, nonostante C abbia un punto e mezzo in più

### 3.1 Due dei tre giudici che non l'hanno scelta hanno scritto che è la migliore

Il giudice di ingegneria, che ha votato C:

> «A e C pareggiano a 83. Non fabbricherò un divario che non esiste. **A è la direzione meglio
> costruita e più originale** e vince l'aggregato su tono, invenzione e voce giuridica.»

Il giudice di prodotto, che ha votato C:

> «A è il documento migliore sull'apparato giuridico e **di parecchio la risposta più distintiva
> alla lamentela reale del committente**.»

Entrambi hanno votato C per una ragione tecnica circoscritta, non per una superiorità di
concezione. Le loro ragioni sono innestabili. Il giudizio sulla concezione no.

### 3.2 A vince il criterio che il committente ha dichiarato essere il test di accettazione

Il criterio numero uno della direttiva è: quando un interlocutore istituzionale apre la home, deve
pensare «progetto serio, maturo, credibile». Il giudice nominato esattamente su quel test ha scelto
A, assegnandole il punteggio più alto dato a qualunque direzione da qualunque giudice (89), e ha
motivato così:

> «Un registro è inequivocabilmente un soggetto privato che pubblica, non un portale dello Stato.
> C è un banco di servizio, e un banco di servizio è la forma della cosa che AGAMI non deve mai
> essere scambiata per. Non è un'ipotesi: le persone che questo sito protegge sono persone che sono
> già state avvicinate da qualcuno che diceva di agire per un'amministrazione.»

Questo è l'argomento più forte dell'intero Council. Il rischio del progetto non è sembrare noioso.
È sembrare un'autorità pubblica a chi è già stato truffato da qualcuno che fingeva di esserlo.

### 3.3 L'idea di A **è** il modello di dominio di questo prodotto

Questa è la ragione che ha deciso, e non compare in nessuna delle quattro schede di voto perché
nessun giudice aveva davanti il codice del dominio che abbiamo scritto oggi.

A dice: ogni cosa sul sito ha **una posizione** (un ordinale), **un'autorità** (un attore
responsabile nominato) e **una data o una fonte**.

Ora si guardi che cosa contiene realmente questa piattaforma:

| Oggetto del dominio | Posizione | Autorità | Data o fonte |
|---|---|---|---|
| `LegalRule` | `rule_id`, `version` | `approved_by` | `valid_from` / `valid_to`, `source_ref` |
| `ChecklistItem` | `order` | **`responsible_actor`** | `due_date`, `source_title` |
| `CaseFile` | `reference`, `status` | `assignments` | `status_since` |
| `PathwayAssessment` | `applied_rules` | ruleset approvato | `assessed_at`, `ruleset_snapshot` |
| Passo amministrativo | numero del passo | autorità competente | scadenza, norma |

Non è un'analogia. È la stessa tripletta, scritta due volte: una nel modello dati, una nella
grammatica visiva. Un sistema grafico che coincide con il modello di dominio **non va reinventato**
quando arrivano l'Academy, la governance del Forum o l'editor delle regole: si estende da solo.

C è eccellente come porta d'ingresso a un servizio. Ma la sua lettura della piattaforma — «lo stesso
banco visto da dietro» — è più debole della lettura di A — «lo stesso registro in forma di lavoro» —
proprio dove questo prodotto ha il suo peso: un fascicolo denso, datato, attribuito.

### 3.4 Il rosso come rubrica

A riserva il rosso a una sola cosa: marcare l'ordine. È ciò che il rosso significa nei registri
giuridici e amministrativi da prima della stampa. È una decisione colta, verificabile e propria: non
la si trova su nessun altro sito istituzionale contemporaneo perché richiede di sapere perché la si
prende.

---

## 4. Gli innesti obbligatori

Un giudice ha votato B per una sola ragione, e **tutti e quattro** hanno chiesto di innestarla.
Quando quattro revisori indipendenti nominano lo stesso elemento, quell'elemento entra.

### 4.1 Da B — la barra di giurisdizione **(obbligatoria)**

Il giudice di design:

> «Applicata a un ritaglio di 200 px: A mi dà un ordinale, un filetto e una nota marginale, e
> riconosco la categoria — editoria istituzionale — ma non il sito. C mi dà un segno di spunta
> verde-azzurro su un filetto calcareo, e riconosco la categoria — servizio pubblico contemporaneo
> — ma non il sito. B mi dà una striscia segmentata per responsabile, e **so esattamente quale sito
> è**. La barra di giurisdizione è l'unica invenzione autentica del pacchetto. A e C codificano
> entrambe la sequenza; ogni diagramma di processo sul web codifica la sequenza. B codifica la
> **giurisdizione** — chi risponde di ciascuna fase — che è il soggetto reale di questo progetto.»

Una banda segmentata con legenda che dichiara quale tratto di un processo appartiene all'**Italia**,
al **Marocco**, alla **piattaforma** e a un'**autorità competente**. Va sotto l'enunciato della home
e nell'intestazione del fascicolo nella piattaforma.

È anche la risposta grafica al requisito più importante del dominio: «chi è responsabile».

### 4.2 Da B — la lista di demolizione come primo sprint

Prima di scrivere un solo componente nuovo si cancella il vecchio: token morti, la famiglia bronzo,
`.site-header::before` con il suo `backdrop-filter`, `.reveal`, `.counter`, `.portal-card`,
`.pathway-pill`, `.empty-state__icon`, le quattro illustrazioni delle entrate, gli attributi HTMX
senza libreria. Cancellare costa meno che rifattorizzare e impedisce al sistema vecchio di filtrare
nel nuovo.

### 4.3 Da B — tre test meccanici e la guardia contro l'impersonificazione

| Test | Regola |
|---|---|
| T3 | `grep box-shadow` restituisce **solo** la dichiarazione dell'anello di fuoco |
| T4 | `border: 1px` corrisponde **solo** ai controlli di form e a `dialog` |
| T-grigio | Screenshot a 1440, conversione in scala di grigi, il rango di ogni sezione dev'essere riconoscibile a tre metri |

T4 è la garanzia anti-scheda più efficace proposta da chiunque: **una scheda è definita dalla sua
scatola, non dai suoi angoli.**

La guardia contro l'impersonificazione di B è adottata integralmente: nessun lockup a tre bande in
stile `.italia`, nessuna convenzione «Sito ufficiale», nessun accostamento rosso/bianco/verde o
rosso/verde nel sistema delle giurisdizioni, nessun marchio di partner senza un campo
`authorisation_ref` sul componente.

### 4.4 Da C — nessuna marginalia, nessun layout a tre zone **(obbligatoria)**

È l'obiezione decisiva del giudice di ingegneria ad A, e si risolve con una riga:

> Se una pagina non ha marginalia reali, **non riceve** il layout a tre zone: riceve una colonna di
> lettura centrata dentro il contenitore.

A mitigava il problema allargando il contenuto da colonne 3–9 a 3–10, il che significa due layout
autorizzati e testati per fascia, in LTR e in RTL, su quattordici archetipi. La regola di C elimina
la classe di difetto invece di gestirla — ed è esattamente il difetto che ha prodotto la colonna da
576 px sola dentro 1 200 px nella build respinta.

### 4.5 Da C — nessun colore significa mai «approvato» **(obbligatoria)**

Si elimina lo stato verde di successo da tutto il sistema, pubblico e piattaforma. Un passo concluso
è **TRASMESSO** o **CHIUSO**: un fatto sul fascicolo, non un verdetto. Il verde significa
*bilaterale*, mai *sì*.

Non è una scelta estetica. È la stessa ragione per cui l'esito `eligible` non esiste nel dominio:
questa piattaforma non approva nulla, e nessun elemento dell'interfaccia deve poter essere letto
come un'approvazione.

### 4.6 Da C — le quattro entrate nella prima schermata

A colloca la prima entrata a y≈766 con la piega a 900: una su quattro visibile. Si alza il registro
perché tutte e quattro stiano nella prima schermata, conservando l'enunciato in tondo minuscolo di A
e la nota marginale sulle frodi.

### 4.7 Da C — il budget di altezza su telefono con l'aritmetica mostrata

Sette sezioni, altezze nominate, circa 2 640 px ≈ 3,1 schermate a 390 px, contro le 8,65 di oggi.
Un tetto con i conti è verificabile; un tetto senza conti è un auspicio.

### 4.8 Da C — URL localizzati

Segmenti di percorso tradotti con redirect 301. Una pagina araba servita su un percorso francese,
con gli slug dei percorsi in chiavi inglesi di database, è un indizio istituzionale che nessuna
tipografia corregge.

---

## 5. Che cosa di A resta esattamente com'è scritto

- L'apparato a tre zone: **rail** (ordinale, titolo corrente, indice locale), **colonna di lettura**
  (576 px), **margine** (nota, data, fonte, cautela), con la colonna 10 come canale vuoto fisso.
- I contenitori che crescono per fascia: 1176 / 1320 / 1440 sopra i 1200 px, invece di convertire
  tutto in margine.
- Nessun `clamp()` su display e contenitori: le dimensioni scattano ai breakpoint, così il rapporto
  è progettato a ogni larghezza.
- I sei cancelli di QA tipografica come bloccanti di rilascio, e la regola che un token di
  `font-feature` che non cambia misurabilmente i glifi si **cancella** invece di restare inerte.
- `font-synthesis: none` globale e divieto del peso 700 in arabo dove sono sottoinsiemati solo
  400/500/600.
- **Nessun dark mode.** Il budget va interamente al livello `@media (forced-colors: active)`, che
  oggi non esiste: `grep -n "forced-colors" static/css/*.css` non restituisce nulla.
- `<figure>` senza `<figcaption>` è un **errore di build**, con quattro campi obbligatori: luogo,
  data, una frase di fatto, credito. È ciò che rende la fotografia di repertorio strutturalmente
  impossibile invece che solo scoraggiata.
- I sette stati visibili del documento: MANCANTE · DEPOSITATO · IN ESAME · VALIDO · NON VALIDO ·
  SCADUTO · DA SOSTITUIRE.
- L'apparato completo dell'esito di regola, con l'elenco numerato delle fonti come regione di
  chiusura: ordinale in rubrica, titolo della fonte, riferimento normativo, data di consultazione.
- La regola che l'azione primaria di un flusso mantiene lo stesso rango su ogni superficie.
- Il contratto completo del wizard: risposte ricontrollate nel template, fuoco spostato sul
  `<legend>` dopo ogni scambio, regione live persistente fuori dal nodo scambiato.

---

## 6. Che cosa si cancella dalla direzione A

| Elemento di A | Sostituito da | Ragione |
|---|---|---|
| `--state-ok-fg #1B6B4A` (verde di successo) | TRASMESSO / CHIUSO, senza colore di verdetto | §4.5 — nessun colore significa approvato |
| Contenuto che si allarga a colonne 3–10 quando il margine è vuoto | Colonna di lettura centrata, layout a tre zone non applicato | §4.4 — elimina la classe di difetto |
| Il passaggio fra le due sponde marcato dal solo colore | Stacco strutturale di 6 px con marcatori MAROC / ITALIE | Fallisce in scala di grigi e a colori forzati, e contraddice la regola §5.4 di A stessa |
| Descrittore arabo nascosto sotto i 1280 px | Descrittore arabo presente a ogni breakpoint | Per un progetto Veneto–Marocco il segnale bilingue nel marchio vale più del descrittore latino |
| Tetto mobile di 5 schermate senza conti | Budget di C con l'aritmetica | §4.7 |
| Famiglia monospace dichiarata | Istanza ad asse di larghezza dell'interfaccia, cifre tabulari, zero barrato | Chiude `--font-mono`, dichiarato e mai caricato |

---

## 7. Sequenza di costruzione

Il monito operativo più acuto del Council, dal giudice di ingegneria:

> «Il linguaggio grafico proprio — marchio, folio, barra di giurisdizione, registro — si **spedisce
> presto**, non per ultimo. Senza di esso la build intermedia è austera senza essere ancora
> distintiva, che è il posto peggiore in cui mostrare qualcosa a un cliente.»

Ordine adottato:

1. **Demolizione** (§4.2). Nessun componente nuovo prima.
2. **Token e scala tipografica**, con i cancelli di QA attivi.
3. **Linguaggio grafico proprio**: ordinale, folio, filetti, **barra di giurisdizione**.
4. **Archetipi di pagina**, prima delle pagine.
5. **Home** e le quattro entrate.
6. **Guscio della piattaforma** e cruscotto della persona.
7. Il resto delle pagine, per archetipo.

---

## 8. Clausola degli asset protetti

Il Council ha nominato ciò che il rebase **non deve distruggere**. Vale come vincolo:

- `core/public_routes.py` e il registro delle rotte pubbliche;
- il modello di permessi a livello di oggetto;
- le annotazioni di contrasto per token e la parità d'inchiostro latino/arabo misurata al 3 %;
- l'ingegneria RTL con proprietà logiche, zero overflow su 50 misurazioni;
- `docs/IMAGE_LICENSES.md` e la disciplina di hosting locale;
- il registro dei testi vincolati e i test sulle formulazioni vietate;
- i gate di pubblicazione.

---

## 9. Criterio di accettazione della direzione

La direzione è implementata quando, sulla stessa batteria di screenshot:

1. Nessuna fascia ripete la larghezza di contenitore della fascia precedente più di due volte di seguito.
2. Nessun tipo di corpo compare due volte consecutive; ogni pagina usa almeno quattro dei sei tipi.
3. Lo screenshot a 1440 in scala di grigi rende riconoscibile il rango di ogni sezione a tre metri.
4. `grep box-shadow` restituisce solo l'anello di fuoco; `border: 1px` solo controlli e `dialog`.
5. La home a 390 px sta sotto 3,5 schermate e le quattro entrate sono nella prima.
6. Nessun `<figure>` senza `<figcaption>` con i suoi quattro campi.
7. Nessun verde di successo esiste nel sistema.
8. La barra di giurisdizione compare sulla home e nell'intestazione del fascicolo.
9. Su un ritaglio di 200 px un designer riconosce **questo** sito.
10. Alla domanda «sembra ancora un sito generato da un'AI?» la risposta è no, motivata.
