# VISUAL QA REPORT — che cosa è cambiato, e come lo si è verificato

Versione 1.0 · 21 settembre 2026 · Direzione artistica **A — «Le Registre»**

Il committente ha respinto il primo risultato con quattro frasi: «un sito generato da un'AI», «un
sito SaaS generico», «una collezione di card», «tecnicamente corretto ma esteticamente ordinario».
Questo documento riporta che cosa è stato fatto in risposta e **come è stato verificato**, non che
cosa si spera di aver ottenuto.

---

## 1. Il metodo

Il browser è la verità. Nessuna affermazione su una pagina è accettata qui se non è stata misurata
sulla pagina resa.

| Strumento | Che cosa misura | Copertura |
|---|---|---|
| `scripts/capture_baseline.py` | Campagna di screenshot, 10 viewport, fr + ar | ogni rotta pubblica registrata |
| `scripts/qa_browser_crawl.py` | Stato HTTP, `lang`/`dir`, `h1` unico, overflow, errori di console, richieste esterne e fallite, `alt` mancanti, bersagli sotto 24 px, testo sotto 12 px, **ogni link interno seguito** | 804 pagine, 276 link |
| `scripts/qa_rtl_check.py` | Direzione, scorrimento **reale**, `h1`, CSS di direzione fisica, regioni di scorrimento etichettate | 14 coppie pagina/viewport in arabo |
| `scripts/qa_person_journey.py` | Il percorso completo, **cliccando**, non costruendo URL | 1 percorso end-to-end |
| `scripts/qa_capture_platform.py` | Che cosa vede **ciascun ruolo** | 27 immagini, 5 account |
| `scripts/css_class_audit.py` | Classi nominate nei template senza regola | 962 classi esaminate |

---

## 2. I cambiamenti strutturali

| Prima | Dopo | Perché |
|---|---|---|
| Griglia di card con ombra e raggio | **Registro**: ordinale, titolo, glossa, attore | Una card dice «sono un modulo software»; una voce di registro dice «sono una cosa con una posizione, un titolo e un responsabile» |
| Eyebrow decorativo | **Folio**: la sezione ha una posizione | Una posizione è un'informazione; un occhiello no |
| Stepper orizzontale a pallini | **Sequenza** verticale con attraversamento visibile | Il passaggio di responsabilità dal paese d'origine all'Italia è il fatto strutturale del dominio |
| Pillole di percorso | Registro dei percorsi | Idem |
| Hero a tutta larghezza con testo bianco | **Plate**: frontespizio con l'autorità sotto il titolo | Un sito istituzionale afferma chi parla prima di che cosa offre |
| Riquadri vuoti tratteggiati con icona | Un filo e una frase che nomina chi riempie e quando | Un riquadro vuoto dice quali moduli ha il software |
| Sei sezioni di durata identica | Quattro ranghi: 96 / 48 / 24 / 12 px | `.page-home .section { padding-block: clamp(…) }` era la riga più responsabile del ritmo piatto |
| Area riservata dentro il guscio pubblico | Chrome, navigazione e footer propri | Il Design Council le ha dato 3/10 |

---

## 3. I difetti trovati **guardando**

Nessuno di questi sarebbe emerso da una lettura del codice.

> Un dodicesimo difetto di design è arrivato dopo, e non guardando: `--s-5` non esiste nella scala
> (1·2·3·4·6·8·12·16·24·32), quindi il `padding` del blocco di comunicazione della selezione non si
> applicava. Correggerlo ha scoperto il difetto vero: la stessa regola usava la scorciatoia
> `padding` a quattro valori accanto a `border-inline-start`, e il quarto valore della scorciatoia è
> **left**. In arabo lo spazio finiva dal lato opposto al filetto. Misurato in entrambe le direzioni
> sui fogli di stile serviti dal server: filetto e spazio maggiore ora stanno dalla stessa parte.
> Una scansione di ogni foglio non ha trovato un secondo caso.

| # | Difetto | Come è emerso | Misura |
|---|---|---|---|
| 1 | Una riga di ingressi alta **821 px** su telefono | Screenshot a 390 px | L'area di griglia `actor` era dichiarata solo sopra 768 px; un elemento assegnato a un'area non dichiarata finisce in una riga implicita. Dichiarata a ogni larghezza: la sezione è passata da 2305 a 1049 px |
| 2 | `--state-warn-br` a **2.998:1** sul nuovo ground | Test di contrasto sui token reali | Scurito a `#a88232` → 3.32:1 |
| 3 | La barra di giurisdizione resa in quattro segmenti uguali in produzione | Lettura della CSP | `style="flex-grow:…"` inline sarebbe stato scartato dalla CSP `self`. Sostituito con `data-share` |
| 4 | Sei proprietà personalizzate consumate e **dichiarate in nessun luogo** | Audit dei token | Ogni `var()` cadeva sul valore iniziale |
| 5 | L'ordinale del folio a **4.46:1** su navy | Test di contrasto | `--rubric-on-navy` è un colore di *filo*, non di testo |
| 6 | Un link di navigazione arabo reso nel carattere di lettura Naskh | Screenshot arabo | Rendere il serif il carattere corrente faceva ereditare il serif ai controlli |
| 7 | La dashboard **senza alcun `h1`** appena la persona possiede un fascicolo | `qa_rtl_check.py` | L'intestazione prescritta è mostrata solo a chi non ha fascicolo; la fascia del fascicolo è fatta di `<p>` e `<dl>`. Vero in tutte e quattro le lingue |
| 8 | Una colonna di griglia che non si restringe | `qa_rtl_check.py` a 390 px | La dimensione minima automatica di un elemento di griglia è il suo contenuto: una tabella a cinque colonne faceva scorrere **la pagina** invece della tabella |
| 9 | I termini del glossario a **17 px** di altezza | Crawl, 9 pagine, 3 lingue | Bersaglio autonomo sotto il minimo di WCAG 2.2 §2.5.8 |
| 10 | Due link della FAQ a **22 px** di distanza | Sonda mirata | Né 24 px di dimensione né 24 px di separazione: l'eccezione di spaziatura non era soddisfatta |
| 11 | `.gloss` usata su 14 pagine, **nessuna regola** | `css_class_audit.py` | Ogni inciso reso a dimensione di prosa corrente nel colore dell'inchiostro: leggeva come un secondo paragrafo dell'argomentazione |

---

## 4. Una nota di metodo che è costata tempo

`documentElement.scrollWidth` **non è** un segnale di overflow in RTL. Chromium riporta 445 px contro
un viewport di 390 px per una pagina il cui scroller annidato ritaglia correttamente e che **non
scorre affatto** (`canScrollDocument: false`, `body.scrollWidth: 390`).

Il primo risultato era un falso positivo. Il controllo è stato riscritto per verificare se il
documento **può** muoversi e per ignorare gli elementi che stanno legittimamente fuori dal viewport
dentro il proprio contenitore di scorrimento — e in quella forma ha trovato il difetto vero.

Allo stesso modo, una scansione eseguita **mentre si modificano file Python** ha riportato 770 pagine
su 804 «con problemi»: `runserver` si riavvia a ogni salvataggio e chiude le connessioni in corso.
Rieseguita contro server `--noreload`, a modifiche ferme, la stessa scansione ha riportato
**9 pagine con problemi e 0 link rotti** — tutte e nove lo stesso difetto, il numero 9 qui sopra.
Corretto quel difetto, la terza scansione ha riportato **804 pagine, 276 link, 0 problemi, 0 link
rotti**.

---

## 5. Risultati misurati

### 5.1 Scansione del sito pubblico (`--noreload`, Fase 3 aperta)

| Misura | Valore |
|---|---|
| Pagine visitate | 804 |
| Link interni seguiti | 276 |
| **Link rotti** | **0** |
| Pagine con un problema | 9 → **0**, riverificato con una seconda scansione completa |
| Errori di console | 0 |
| Richieste esterne | 0 |

### 5.2 Arabo e RTL

**14 coppie pagina/viewport, 0 problemi.** Direzione del documento e del corpo, scorrimento reale,
`h1` unico, nessuna proprietà CSS di direzione fisica, regioni di scorrimento etichettate e
raggiungibili da tastiera, nessun errore di console.

### 5.3 Percorso persona, end-to-end nel browser

| Passo | Risultato |
|---|---|
| «Ma situation» | caricata, `h1` unico, salvata |
| Questionario | completato in 3 passi |
| Fascicolo | **E12273C5DF** aperto |
| Esito | «Exigence manquante», innalzato dalle regole in vigore |
| Fonti | **5**, ciascuna con riferimento puntuale |
| Checklist | 8 righe, 3 con il riferimento della regola |
| Elenco → dettaglio | navigato **cliccando la riga** |
| Pre-valutazione | 5 fonti, 7 regole, riproducibilità confermata |
| Errori di console | 0 |

### 5.4 Screenshot

| Campagna | File |
|---|---|
| `docs/qa/visual/before` | 273 |
| `docs/qa/visual/after` | campagna rifatta il 21/09/2026 sui server `--noreload` |
| `docs/qa/platform` | 27, cinque account, due viewport, fr + ar |
| `docs/qa/design` | matrice di accessibilità: 404, senza JS, movimento ridotto, zoom 200 % e 400 % |

---

## 6. Che cosa resta

| Punto | Stato |
|---|---|
| Passaggio con un lettore di schermo reale da parte di una persona | **non fatto**, non sostituibile |
| 382 classi nominate nei template senza regola CSS | enumerate, con tetto; due erano difetti reali e sono corrette |
| `components.css` a 3045 righe | eredità; la piattaforma non vi aggiunge, `register.css` è il linguaggio nuovo |
| `_legacy-tokens.css` | impalcatura dichiarata, 338 righe, con tetti verificati; **solo si riduce** |
| Confronto visivo prima/dopo pagina per pagina | le due campagne esistono; la lettura comparata è un giudizio umano e non è stata automatizzata |
