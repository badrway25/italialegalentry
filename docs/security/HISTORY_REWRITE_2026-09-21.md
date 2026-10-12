# RISCRITTURA DELLA CRONOLOGIA GIT — 21 settembre 2026

Stato: **ESEGUITA** · Autorizzazione: direttiva «PRE-PRODUCTION HARDENING», P0 Repository
confidentiality · Ambito: locale, nessun remote è mai esistito

---

## 0. Perché

Il repository non ha mai avuto un remote e non è mai stato pubblicato. Finché è così, nulla è
esposto. Ma la working tree pulita non dice nulla sulla cronologia: `git ls-files` vede un commit,
`git rev-list --objects --all` vede tutti i blob mai esistiti, compresi quelli il cui percorso è
stato cancellato o riscritto. Il secondo è l'unico che risponde alla domanda «questo repository si
può pubblicare».

La risposta, prima di questa operazione, era **no**.

---

## 1. Che cosa è stato scansionato

`scripts/history_secret_scan.py` legge **ogni blob raggiungibile da ogni ref**, non la working tree.

| Misura | Valore |
|---|---:|
| Blob totali in cronologia | 2124 |
| Blob di testo scansionati | 1311 |
| Blob binari (non ispezionabili con una regex) | 171 |
| Commit | 65 |
| Ref | 1 (`main`), nessun tag, nessun remote |

Sedici famiglie di pattern: indirizzi e-mail, numeri di telefono in formato internazionale e
nazionale marocchino, chiavi AWS, blocchi di chiave privata, token GitHub/Slack/Google/Stripe, JWT,
credenziali assegnate a una variabile, URL di connessione con password, digest a 64 esadecimali,
riferimenti a documenti d'identità, codice fiscale italiano, IBAN.

I blob binari **non** sono stati grepati, perché una regex su un PNG non significa nulla. Sono stati
trattati per percorso e tipo, e i 26 screenshot del sito di produzione sono stati **guardati**.

---

## 2. Che cosa è stato rimosso, e perché

### 2.1 Documenti sorgente del committente — 4 file, ogni versione

2 PDF e le loro 2 estrazioni testuali **integrali**, tutti sotto `docs/source/`: il Documento
d'implementazione (15 pagine, 14 settembre 2026) e l'Annexe 1 — testi giuridici (7 pagine), con
le rispettive estrazioni.

**Questa rimozione ribalta una decisione scritta.** `docs/security/CONFIDENTIAL_MATERIAL_POLICY.md`
§2 li esentava esplicitamente, con una motivazione ragionevole: sono istruzioni di pubblicazione i
cui testi sono destinati al sito pubblico, a differenza del pacchetto del 20 settembre che è
materiale di tutela interna.

La motivazione resta vera per i **testi**, non per i **documenti**. Un PDF del committente, con la
sua autrice, la sua versione e le sue istruzioni interne, non diventa un artefatto pubblico per il
fatto che alcune sue frasi finiranno su una pagina. E l'estrazione integrale in `.txt` è la stessa
cosa in forma greppabile.

Il costo della rimozione è nullo: gli originali sono fuori dal repository, in una posizione privata,
e un solo script li leggeva.

### 2.2 Dati personali di un terzo — 3 valori, in 6 file, ogni versione

Le catture dell'audit read-only del sito attuale contenevano dati personali di un terzo, committati
come evidenza. Il rilievo sui dati personali del sito attuale è annotato nel registro privato; nel
repository restano soltanto i segnaposto che hanno sostituito i valori. Dal 12 ottobre 2026 il
segnaposto è uno solo, `[REDATTO]`, e non dice quale dato sostituisce.

File interessati: `docs/CURRENT_SITE_AUDIT.md`, `docs/REQUIREMENTS_MATRIX.md`,
`docs/URL_MIGRATION_MAP.md`, `docs/audit/current-site/README.md`,
`docs/audit/current-site/raw/sitemap_urls.txt`, `docs/audit/current-site/raw/wp_json_users.json`,
`tests/compliance/test_no_personal_data_in_repository.py`.

La working tree era già redatta dal commit `21448db`; la cronologia no. La sostituzione porta i
commit precedenti allo stesso stato di HEAD, quindi **l'albero di HEAD non cambia** per questi file.

Il rilievo non sparisce: è annotato nel registro privato, e `docs/URL_MIGRATION_MAP.md` chiede un
410 sulla pagina autore. Sparisce il **valore**.

### 2.3 Quattordici screenshot committati per errore — 5,4 MB

`entreprises-*.png`, `institutions-*.png`, `projet-pilote-*.png`,
`universites-et-formation-*.png`, alla radice del repository, aggiunti da `729db62` e rimossi poco
dopo. Sono catture del **nostro** sito, non contengono dati di terzi, e non sono state rimosse per
riservatezza ma perché sono spazzatura che nessuno rileggerà.

---

## 3. Che cosa NON è stato rimosso, e perché

Una riscrittura che porta via anche il contenuto legittimo è un danno, non una bonifica.

| Trovato | Verdetto | Motivo |
|---|---|---|
| **«Avv. Kaoutar Badrane»**, 21 file | **RESTA** | È la titolare dei diritti, non un dato personale esposto per errore. Il suo nome è dentro un **testo prescritto destinato al sito pubblico** (`locked_content.py`, attribuzione del marchio) e il sito di produzione lo pubblica già. Rimuoverlo romperebbe un testo bloccato e cancellerebbe un'attribuzione voluta. |
| `postgres://ile:ile-dev-password@…`, 84 occorrenze | **RESTA** | Password del database **di sviluppo locale**, dichiarata in `.env.example` e in `docker-compose.yml`, mai usata in produzione: `config/settings/prod.py` esige `DATABASE_URL` dall'ambiente. È nell'inventario dei segreti come debito, non come incidente. |
| 26 password sintetiche di test (`Str0ng-Passw0rd-2026!` e simili) | **RESTA** | Credenziali di fixture, riconoscibilmente finte, su account `@example.test`. |
| `SECRET_KEY = "test-only-secret-key-not-for-production"` | **RESTA** | Solo in `config/settings/test.py`. `prod.py` rifiuta l'avvio se la chiave di produzione è corta o poco casuale. |
| 21 numeri di telefono | **RESTA** | Tutti sintetici: `+212600000000`, `+39 049 0000000`, `+39 0000 000000`. Nessuno è instradabile. |
| 119 valori a 64 esadecimali | **RESTA** *(tranne uno)* | Digest d'integrità di `apps/cms/locked_content.sha256.json` e di `tests/security/test_confidential_material.py`. L'unico rimosso è uno dei tre valori di §2.2. |
| «numero di passaporto» | **RESTA** | Etichetta d'interfaccia nel catalogo italiano, non un numero. |
| 26 screenshot del sito di produzione | **RESTA** | Guardati, non solo elencati: sono la homepage pubblica di marketing. Nessun dato personale. Sono la prova su cui poggia `docs/CURRENT_SITE_AUDIT.md`. |
| `docs/qa/lighthouse/*.json.gz` | **RESTA** | Verificata: unico host `127.0.0.1`, nessun indirizzo, nessun percorso utente. |

---

## 4. Copia probatoria

Prima della riscrittura, cronologia completa in un bundle Git conservato **fuori dal repository**,
in una posizione privata; il suo sha256 è annotato nel registro privato.

`git bundle verify` conferma «a complete history». Il ripristino è stato **provato**, non supposto:
clonato in una directory temporanea, HEAD `53d9b46`, 65 commit, 4 file sotto `docs/source/`, copia
cancellata.

> Il bundle contiene tutto ciò che questa operazione rimuove. È materiale riservato: resta locale,
> in una posizione privata, non diventa un remote, non si copia su un servizio di condivisione, e chi
> non ha titolo a leggere i documenti del committente non ha titolo a riceverlo.

---

## 5. Strumento

`git filter-branch --index-filter`, incluso in Git, nessuna installazione.

`git filter-repo` è lo strumento che la documentazione di Git raccomanda ed è più adatto
all'operazione in generale, ma richiede un'installazione da rete. Le avvertenze note di
`filter-branch` riguardano repository con molti ref, tag firmati, grafts e remote già pubblicati:
qui c'è **un ramo, nessun tag, nessun remote e 65 commit**, quindi nessuna si applica. Alla
lentezza si preferisce l'assenza di una dipendenza nuova su una macchina che ne vieta l'aggiunta
disinvolta.

Dopo la riscrittura: `refs/original` cancellato, reflog scaduto, `git gc --prune=now --aggressive`.

### 5.1 Lo strumento non nomina ciò che rimuove

La prima versione di `scripts/history_rewrite_index_filter.py` portava i valori da redigere scritti
dentro di sé. Ha funzionato: dopo la riscrittura i valori erano spariti da ogni file della
cronologia tranne uno, **lo script stesso**, che nel frattempo era stato committato.

È lo stesso errore, nella stessa sessione, già commesso dalla guardia in `tests/compliance/`, che
cercava come letterale il valore da proteggere e quindi corrispondeva a se stessa. Due volte è una
regola: **uno strumento di redazione non nomina ciò che redige.**

La tabella dei valori sta ora fuori dal repository, in una posizione privata, accanto al bundle e
sotto le stesse regole. Lo script la legge da `ILE_REDACTION_TABLE` e **si rifiuta di partire** se non la trova o se
la tabella è vuota: una tabella mancante renderebbe ogni commit un'operazione nulla, `filter-branch`
riporterebbe successo su tutti, e il risultato sarebbe una cronologia intatta che tutti credono
bonificata.

Questo ha richiesto una **seconda passata** di `filter-branch`, per togliere dalla cronologia la
versione dello script che conteneva i valori.

### 5.2 La prova generale ha trovato un difetto nel piano

La riscrittura è stata provata prima su un clone usa e getta, non direttamente sul repository. È
servito: uno dei valori esisteva in cronologia in **tre lunghezze**, non una. Il valore completo a
64 esadecimali nella cattura; un prefisso di 33 caratteri nella prima versione della guardia; un
frammento di 14 caratteri nel letterale spezzato che l'aveva sostituita. La prova ha sostituito il
primo e ha lasciato gli altri due intatti.

Da qui due conseguenze. La lista di sostituzione procede **dal più lungo al più corto**, altrimenti
il frammento corto consuma l'inizio del valore lungo e lascia il resto degli esadecimali orfani. E
la guardia in `tests/compliance/` è stata riscritta per **forma** prima della riscrittura: non
contiene più alcun letterale, perché una guardia che custodisce il segreto per riconoscerlo non è
una guardia.

---

## 6. Verifica successiva

La stessa scansione, rieseguita sulla cronologia risultante. Esito in
`docs/security/HISTORY_SCAN_AFTER.md`.

---

## 7. Conseguenza da non dimenticare

**Tutti gli hash sono cambiati.** Ogni commit citato in un documento, in un report o in un messaggio
prima del 21 settembre 2026 non esiste più. I riferimenti nei documenti del repository sono stati
aggiornati; i riferimenti in materiale già consegnato fuori dal repository no, e non possono esserlo.

Il vecchio HEAD era `53d9b46`. Il nuovo è indicato in `docs/FINAL_REPORT.md` §17.
