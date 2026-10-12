# QA REPORT — Italy Legal Entry™

Data di redazione: **21 settembre 2026** · Ambiente: **sviluppo locale** · Nessuna operazione su
produzione, nessun DNS modificato, nessuna e-mail reale inviata.

Questo documento riporta che cosa è stato verificato, **come**, e che cosa non lo è stato. Una
verifica che non dice come è stata fatta non è una verifica; una funzionalità che non è stata
esercitata non è dichiarata funzionante, per quanto completo ne sia il codice.

---

## 1. Il criterio adottato

Per ogni funzionalità, la domanda non è «esiste il codice?» ma **«qualcuno l'ha vista funzionare, e
che cosa esattamente?»**. Le prove ammesse, in ordine di forza:

| Livello | Che cosa prova | Esempio in questo progetto |
|---|---|---|
| **Browser reale** | La pagina rende ciò che il servizio produce | `scripts/qa_person_journey.py` apre il fascicolo cliccando la riga dell'elenco |
| **Test d'integrazione HTTP** | Vista, autorizzazione, template, redirect | `apps/cases/tests/test_views.py` |
| **Test di dominio** | L'invariante tiene comunque arrivi il cambiamento | `apps/cases/tests/test_lifecycle.py` |
| **Test unitario** | Una funzione fa ciò che dice | `apps/rules/tests/test_engine.py` |
| **Lettura del codice** | Nulla. Non è una prova. | — |

Un test che passa contro un *fixture* costruito a mano prova meno di uno che passa contro il
servizio che l'interfaccia chiama davvero. Dove è stato possibile si è scelto il secondo.

---

## 2. Percorso persona, verificato end-to-end nel browser

`scripts/qa_person_journey.py` esegue, in un Chromium reale, contro il server di sviluppo:

```
VISITATORE → ACCOUNT → SITUAZIONE → ORIENTAMENTO → RULE ENGINE → RISULTATO
           → FASCICOLO → CHECKLIST → FONTI
```

Esito dell'esecuzione del 21 settembre 2026:

| Passo | Risultato osservato |
|---|---|
| Pagina «Ma situation» | caricata, `h1` unico, form salvato |
| Questionario di orientamento | completato in 3 passi attraverso il servizio reale |
| Fascicolo aperto | riferimento **E12273C5DF** |
| Esito registrato | **«Exigence manquante»** — innalzato dalle regole in vigore, non dal questionario |
| Fonti mostrate | **5**, ciascuna con un riferimento puntuale |
| Righe di checklist | **8**, di cui **3** con il riferimento della regola che le ha prodotte |
| Elenco dei fascicoli → dettaglio | navigato **cliccando la riga**, non costruendo l'URL |
| Pagina di pre-valutazione | 5 fonti, 7 regole applicate, riproducibilità confermata |
| Errori di console | **0** |

L'autenticazione avviene creando la sessione lato server e consegnando il cookie al browser: nessuna
password viene digitata in un form. Lo script rifiuta di eseguire contro un host che non sia di
loopback.

### Perché questo conta più di un test

Prima di questo lavoro la stessa dashboard mostrava `sources: 0`. Era un comportamento onesto — il
ruleset di orientamento non ha citazioni e non ne sono state inventate — ma significava che
**l'elemento che la direzione artistica indica come quello che trasforma un risultato di
questionario in un accertamento istituzionale era vuoto.** Ora non lo è, e la differenza è visibile
in una pagina, non soltanto in un'asserzione.

---

## 2bis. Percorso impresa, verificato end-to-end nel browser

`scripts/qa_company_journey.py`, contro il server di sviluppo, con l'impresa dimostrativa creata da
`manage.py companies_demo --account … --verified`:

```
IMPRESA → ACCOUNT/VERIFICA → FABBISOGNO → COMPETENZE → ATTORI AUTORIZZATI → STATO
```

| Passo | Risultato osservato |
|---|---|
| Spazio impresa | intestato con il nome dell'impresa stessa |
| Scheda impresa | dichiara che la **verifica è in corso** — dichiarare non concede nulla |
| Registro dei fabbisogni | raggiunto **cliccando**, 4 fabbisogni |
| Un fabbisogno in dettaglio | riferimento non sequenziale, **17 righe di competenze**, stato «VÉRIFIÉE», responsabile nominato |
| Analisi territoriale | **403**, deliberatamente |
| Formulazioni vietate | **nessuna**, su nessuna schermata |
| Elenchi di persone | **nessuno** |

**Il 403 è l'asserzione, non un guasto.** L'analisi territoriale aggrega i fabbisogni di *tutte* le
imprese e appartiene all'équipe del progetto. L'URL viene digitato di proposito, perché la
navigazione dell'impresa non lo offre mai: è l'unica pagina del percorso che **non deve** aprirsi.

Due cose che un test non avrebbe trovato: l'account impresa del seed ha un'organizzazione e
un'appartenenza ma **nessun `CompanyProfile`**, quindi il percorso si fermava a «dichiara la tua
impresa»; e il selettore del link ai fabbisogni intercettava il commutatore di lingua, che porta lo
stesso percorso in quattro lingue e compare prima nel documento.

---

## 3. Arabo e RTL

`scripts/qa_rtl_check.py` apre ogni pagina autenticata in arabo a **390 × 844** e a **1440 × 900** e
verifica sulla pagina renderizzata: direzione del documento e del corpo, scorrimento orizzontale
reale, numero di `h1`, proprietà CSS di direzione fisica, regioni di scorrimento raggiungibili da
tastiera ed etichettate, errori di console.

**14 coppie pagina/viewport, 0 problemi.**

Due difetti reali sono stati trovati e corretti da questa verifica:

1. **La dashboard non aveva alcun `h1`** appena la persona possedeva un fascicolo: l'intestazione
   prescritta è mostrata solo a chi non ne ha, e la fascia del fascicolo è fatta di `<p>` e `<dl>`.
   Nessun lettore di schermo poteva annunciare la pagina, in nessuna delle quattro lingue. Trovato
   dal passaggio arabo, vero ovunque.

2. **Una colonna di griglia non si restringeva.** La dimensione minima automatica di un elemento di
   griglia è il suo contenuto, non zero, quindi `minmax(0, 1fr)` sulla traccia non basta: una
   tabella a cinque colonne spingeva l'intera colonna oltre il viewport e **la pagina** scorreva
   lateralmente invece della tabella.

### Una nota di metodo

`documentElement.scrollWidth` **non è** un segnale attendibile di overflow in RTL: Chromium riporta
445 px contro un viewport di 390 px per una pagina che contiene uno scroller annidato che ritaglia
correttamente e che non scorre affatto. Il controllo è stato riscritto per verificare se il
documento **può** scorrere, e per ignorare gli elementi che stanno legittimamente fuori dal viewport
dentro il proprio contenitore di scorrimento. Il primo risultato era un falso positivo; il secondo
nascondeva un difetto vero.

---

## 4. Le tredici asserzioni di permesso (direttiva §61)

`tests/security/test_object_permissions.py`, marcatore `security`. Ogni asserzione è una frase su
qualcuno che **non deve** vedere qualcosa, scritta contro le queryset e i servizi reali.

| # | Asserzione | Stato |
|---|---|---|
| 1 | La persona A non accede alla persona B | passa |
| 2 | L'impresa A non accede all'impresa B | passa |
| 3 | L'impresa non vede persone arbitrarie | passa |
| 4 | Il professionista vede solo i casi assegnati | passa |
| 5 | L'ente formativo solo i dati di formazione autorizzati | passa |
| 6 | L'istituzione solo il perimetro di convenzione | passa |
| 7 | L'università nessun fascicolo privato | passa |
| 8 | I partecipanti del Forum nessuna informazione privata altrui | passa |
| 9 | Il personale senza permesso non modifica le regole | passa |
| 10 | Il Legal/Rule Editor non ottiene privilegi estranei | passa |
| 11 | Un identificativo scoperto a mano non aggira i permessi | passa |
| 12 | Un'assegnazione revocata o scaduta non dà più accesso | passa |
| 13 | La lista e il dettaglio danno la stessa risposta | passa **dopo una correzione** |

### L'asserzione 13 ha trovato un difetto che nessuno aveva notato

La queryset dei fascicoli non restituiva nulla a `role:staff` — comportamento corretto, introdotto
per chiudere la lacuna L-05. La **policy** sullo stesso oggetto rispondeva però di sì allo stesso
account e allo stesso fascicolo. Due regole di autorizzazione in vigore su un oggetto solo, e la più
permissiva è sempre il difetto: qualsiasi vista che avesse interrogato la policy invece di passare
per la queryset avrebbe consegnato a un account di staff il fascicolo giuridico di una persona.

Questo è precisamente ciò per cui l'asserzione esiste, e non sarebbe stato trovato leggendo il
codice: le due regole sono in due file diversi e ciascuna, letta da sola, è ragionevole.

---

## 5. Che cosa NON è stato verificato, e perché

| Area | Stato | Ragione |
|---|---|---|
| **Contenuto giuridico delle regole** | **NON VERIFICATO** | Nessun giurista ha validato le 11 regole in vigore. `manage.py rules_pending_review --strict` le elenca ed esce con codice 1. È l'unica ragione sufficiente per non dichiarare pronto il modulo. |
| **Date di consultazione delle fonti** | **NON VERIFICATE** | I riferimenti normativi sono corretti ma non sono stati verificati alla fonte ufficiale in questa sede; la citazione si mostra senza data finché non lo sono. |
| **Testi legali italiani ufficiali** | `BLOCKED_BY_MISSING_OFFICIAL_SOURCE` | L'Allegato 1 italiano non è disponibile. Le cinque pagine legali non sono pubblicate, e di conseguenza i form pubblici restano chiusi dal gate G2. Nessun testo è stato tradotto o inventato. |
| **Prestazioni sotto carico** | **NON VERIFICATE** | Nessun test di carico è stato eseguito: l'ambiente è un singolo PostgreSQL in Docker su una macchina di sviluppo, e un numero misurato lì non direbbe nulla sulla produzione. |
| **Penetration test** | **NON ESEGUITO** | Vietato dal mandato su sistemi di produzione, e privo di senso su `runserver`. Le verifiche di sicurezza qui sono test di regressione, non un test d'intrusione. |
| **Accessibilità con lettore di schermo reale** | **PARZIALE** | Struttura, ruoli, etichette e contrasto sono verificati automaticamente; un passaggio con NVDA o VoiceOver da parte di una persona non è stato fatto e non è sostituibile. |
| **Rilettura umana delle traduzioni** | **NON FATTA** | I 1664 msgid dei nuovi moduli sono stati tradotti da corsie automatiche e verificati da un audit: segnaposto, marcatori inline, forme plurali, scrittura, cifre, formulazioni vietate, marchio, termini del glossario. L'audit controlla la **forma**, non la resa. Per un testo istituzionale in arabo, in italiano e in inglese serve una rilettura umana prima della pubblicazione. Le pagine legali non sono interessate: non sono tradotte affatto, e restano bloccate alla fonte. |

---

## 6. Il server di sviluppo e la scansione del sito pubblico

Una scansione completa (`scripts/qa_browser_crawl.py`) eseguita **mentre modificavo file Python** ha
riportato 770 pagine su 804 «con problemi». Non è un risultato di prodotto: `runserver` si riavvia a
ogni salvataggio e chiude le connessioni in corso. La scansione va eseguita contro server avviati
con `--noreload`, a modifiche ferme. Rifatta in quelle condizioni:

| Misura | Valore |
|---|---|
| Pagine visitate | **804** |
| Link interni seguiti | **276** |
| Link rotti | **0** |
| Pagine con un problema | **0** |

La prima esecuzione pulita ne aveva riportate 9, tutte lo stesso difetto: i termini del glossario a
17 px di altezza, sotto il minimo di WCAG 2.2 §2.5.8 per un bersaglio autonomo. Corretto quello, e
un secondo difetto trovato con una sonda mirata (due link della FAQ a 22 px di distanza, che non
soddisfacevano né la dimensione né l'eccezione di spaziatura), la terza esecuzione è pulita.

Lo script aveva inoltre un difetto proprio: stampava un carattere `→` sulla console Windows in
cp1252 e moriva **all'ultima riga** dopo quaranta minuti di lavoro. Corretto forzando UTF-8 sullo
stdout. Il dato non era mai stato il problema; lo era chi lo scriveva.

---

## 6bis. 80 database di test da cancellare quando si vuole

Ogni corsia concorrente ha richiesto il proprio `TEST_DATABASE_URL` (§7 spiega perché non è
facoltativo). Il risultato è che il contenitore PostgreSQL porta **80 database `test_*` per 1828 MB**,
più `ile_review2_design_docs_capture` lasciato da una corsia di cattura. Sono usa e getta: pytest li
ricrea da solo, e tenerli rende `--reuse-db` istantaneo.

Non sono stati cancellati qui, perché cancellare database non è una pulizia che vada fatta per
iniziativa propria su una macchina altrui. Il comando, quando si vuole lo spazio:

```bash
# Genera le istruzioni (non cancella nulla) e le esegue. Verificato: la prima riga prodotta è
# `drop database "test_ile";`.
docker exec italylegalentry-db-1 psql -U ile -d postgres -tAc "select 'drop database \"'||datname||'\";' from pg_database where datname like 'test\_%'" | docker exec -i italylegalentry-db-1 psql -U ile -d postgres
```

Da eseguire a pytest fermo: un database in uso non si lascia cancellare, e il comando lo dirà.

## 7. Deadlock del database di test — una nota operativa

Due esecuzioni di pytest simultanee si bloccano a vicenda: `--reuse-db` le porta entrambe su
`test_ile`, una resta inattiva dentro una transazione tenendo un lock di riga su `auth_group` e
l'altra si blocca per sempre inserendo `role:person`. Osservato due volte, per più di un'ora
ciascuna, senza alcun timeout.

Rimedio: ogni esecuzione concorrente riceve il proprio database.

```
TEST_DATABASE_URL=postgres://ile:ile-dev-password@127.0.0.1:5439/ile_t_<corsia> \
  .venv/Scripts/python.exe -m pytest <percorsi> -q -p no:randomly
```

La seconda collisione è nata da un errore di shell che vale la pena registrare: `ruff check ... |
tail -5 && pytest ...` non si ferma quando ruff fallisce, perché lo stato d'uscita di una pipeline è
quello dell'ultimo stadio. Un'esecuzione che credevo non fosse mai partita teneva il lock.

---

## 8. Riassunto

| Verifica | Risultato |
|---|---|
| Scansione del sito pubblico (`--noreload`, Fase 3 aperta) | **804 pagine, 276 link, 0 problemi, 0 link rotti** |
| Arabo e RTL, pagine autenticate | **14 coppie pagina/viewport, 0 problemi** |
| Percorso persona end-to-end nel browser | completato, 5 fonti numerate, 0 errori di console |
| Le tredici asserzioni di permesso §61 | **tutte passano**, dopo una correzione che l'asserzione 13 ha fatto emergere |
| Test raccolti nel progetto | **2976** |
| `manage.py check` | pulito |
| `makemigrations --check` | nessuna modifica — **non era così**: mancava una migrazione, ed è ora un test su tutte e 28 le app |
| Percorso impresa end-to-end nel browser | 4 fabbisogni, 17 competenze, attore responsabile nominato, analisi territoriale rifiutata all'impresa |
| Ogni app e ogni suite eseguita sul codice finale | sì, in corsie separate; dettaglio in `docs/FINAL_REPORT.md` §14 |
| `ruff check apps tests scripts config` | pulito |
| Screenshot | **704**, contati per cartella: 272 `qa/visual/before` + 269 `qa/visual/after` (pubbliche, prima e dopo la nuova direzione artistica) + 73 `qa/design` + 27 `qa/platform` (per ruolo) + 23 `qa/rtl` + 14 `qa/browser` (i due percorsi end-to-end) + 26 dell'audit del sito attuale |

## 8bis. Campagna di pre-produzione — 21/22 settembre 2026

Una seconda campagna, dopo che la fase funzionale era chiusa. Criterio diverso: non «funziona» ma
«si può pubblicare».

| Verifica | Risultato |
|---|---|
| Scansione della **cronologia Git**, non della working tree | 2131 blob, **0 indirizzi e-mail di terzi**, 0 documenti riservati, 0 credenziali |
| Riscrittura della cronologia | due passate, copia probatoria fuori dal repository, ripristino **provato** |
| Ambiente legacy di test | verificato in sola lettura; solo riferimento, non fa parte di questo repository (decisione della titolarità, 11 ottobre 2026); dettagli nel registro privato |
| Regole giuridiche | **0 in vigore**; 13 bozze + 3 candidate ereditate; il database rifiuta una regola approvata senza approvatore |
| Audit di autorizzazione per forma d'attacco | **56 test**, dieci ruoli × sei forme |
| Impostazioni di produzione | rifiutano l'avvio su TLS debole, chiave corta, **secondo fattore spento**, e ignorano un `.env` di sviluppo |
| `manage.py check --deploy` con ambiente corretto | **nessun avviso** — prima ne aveva uno |
| Prestazioni su stack simil-produzione | peggior LCP **712 ms**, peggior CLS **0,0046** |
| Arabo e RTL, dopo tutte le modifiche | **14 coppie, 0 problemi** |

### I quattro difetti trovati in questa campagna

1. **Uno strumento di redazione che nominava ciò che redige.** Dopo la prima riscrittura i valori
   personali erano spariti da ogni file tranne lo script che li rimuove, committato con i valori
   dentro. Stesso errore, nello stesso giorno, già commesso dalla guardia in `tests/compliance/`
   che cercava l'hash come letterale e corrispondeva a se stessa. Due volte è una regola.
2. **Un `.env` di sviluppo non indeboliva la produzione: la soddisfaceva.** Tre variabili sono
   obbligatorie senza default *proprio perché* il deployment debba fornirle — e un file copiato su
   un host le forniva, con valori di sviluppo, lasciando il controllo di coerenza senza nulla da
   obiettare. Trovato scrivendo il test che doveva dimostrare che quelle tre fermano l'avvio: due
   su tre non lo facevano, e la terza «passava» per la ragione sbagliata.
3. **Nessun ruolo poteva cancellare una comunicazione notificata.** Una relazione in cascata
   dichiarata in un'altra applicazione negava un permesso che il modello concedeva. Segnale: un 403
   nudo, senza pulsante mancante e senza testo.
4. **Un risultato di dimostrazione sembrava autorevole quanto uno vero.** Fonti numerate,
   riferimenti precisi, date di consultazione, riproduzione verificabile — e nessuna delle regole
   dietro era stata approvata da un giurista. Il database lo sapeva, i report lo sapevano, lo
   schermo no.

Il quarto è il più istruttivo. Gli altri tre sono difetti di sistema; il quarto è un difetto di
**onestà dell'interfaccia**, e nessun test di funzionamento lo avrebbe mai segnalato, perché la
pagina funzionava perfettamente.

---

### I difetti trovati da questa campagna di QA

Undici, elencati in `docs/design/VISUAL_QA_REPORT.md` §3, più tredici emersi da controlli non
visivi:

1. La policy del fascicolo concedeva a `role:staff` una vista che la queryset negava — **trovato
   dall'asserzione §61 numero 13**, non leggibile nel codice perché le due regole vivono in file
   diversi e ciascuna, letta da sola, è ragionevole.
2. `_label()` dell'audit scriveva un **id utente sbagliato** per un oggetto non-utente che portava
   l'indirizzo anonimizzato.
3. `rules/facts.py` chiedeva all'app documenti due nomi mai esistiti e **inghiottiva** entrambi i
   fallimenti: il fatto `documents_present` era permanentemente vuoto e silenzioso.
4. `ILE_SEED_DEMONSTRATION_DATA` era **documentato ma non dichiarato**, e una volta dichiarato
   risultava **True sotto le impostazioni di test** perché deriva da `DEBUG` al momento
   dell'importazione di `base`.
5. Cinque **testi prescritti ridigitati** in sorgente, che sarebbero entrati nei cataloghi di
   traduzione.
6. **1664 stringhe d'interfaccia mai entrate nei cataloghi**: i nuovi moduli erano partiti in solo
   francese e la copertura era scesa dal 100 % al 54 %. Tradotte, una corsia per lingua, con l'audit
   come criterio d'accettazione; i quattro cataloghi sono ora al **100 %**.
7. La politica del secondo fattore era stata **allargata senza allargarne l'applicazione**: il
   middleware sorvegliava `/backoffice/`, dove un professionista non entra mai. Trovata da
   `manage.py check --deploy`.
8. Gli **endonimi** delle lingue («Français», «العربية») erano resi in un `<select>` senza attributo
   `lang`: una parola francese dentro una pagina inglese, che un lettore di schermo pronuncia con la
   voce sbagliata.
9. **Nessun ruolo poteva più cancellare una comunicazione.** `notifications.Notification` è legata a
   `portal.Message` da un `OneToOneField` in `CASCADE`, e l'admin di Django rifiuta una
   cancellazione la cui cascata tocca un modello su cui l'account non ha il diritto di cancellare.
   Poiché l'invio crea sempre la riga compagna, il divieto valeva per ogni messaggio. Esito: 403
   nudo, nessun pulsante mancante, nulla nell'interfaccia che lo spiegasse. Il permesso ora è
   **per modello**, non per applicazione: si ferma alla notifica e lascia intoccabile `EmailOutbox`,
   che è il registro di ciò che è stato davvero inviato.
10. **`makemigrations --check` non era pulito.** La riformulazione di un'etichetta di `choices` —
    fatta proprio per non ridigitare un testo prescritto — aveva lasciato lo stato del modello senza
    migrazione. Nessuna colonna cambia, quindi nessun test e nessuna pagina lo mostrava. Il controllo
    esisteva già, ma su **una sola app su 28**.
11. **`--s-5` non esiste.** La scala è 1·2·3·4·6·8·12·16·24·32: il padding non si applicava. La
    correzione ha scoperto il difetto peggiore — la stessa regola usava la scorciatoia `padding` a
    quattro valori insieme a `border-inline-start`, e il quarto valore della scorciatoia è **LEFT**:
    in arabo lo spazio finiva dal lato opposto al filetto.
12. **Tre affermazioni del design system erano scadute**: un consumatore citato che non usa più il
    componente, e due soglie «e almeno altri N» superate dal consolidamento dei template.
13. **Un dato personale reale era committato** come evidenza d'audit, in sei file. Il valore non
    resta nel repository; il rilievo sui dati personali del sito attuale è annotato nel registro
    privato.

Nessuno dei tredici era visibile come pagina rotta. È il motivo per cui questa sezione esiste.

### Che cosa resta, in una riga

Le pagine legali italiane ufficiali non esistono nel materiale fornito, e nessun giurista ha
validato le regole in vigore. Finché non cambiano queste due cose, lo stato non può essere
`LOCAL_RELEASE_READY`.
