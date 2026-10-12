# CONFIDENTIAL MATERIAL POLICY — Italy Legal Entry™

Stato: ATTIVA dal 20 settembre 2026 · Owner: referente tecnico · Revisione: a ogni nuovo documento ricevuto

Questa policy governa il trattamento dei documenti riservati ricevuti dalla titolare del progetto
(Avv. K. B., ideatrice e titolare progettuale) e di ogni materiale da essi derivato. È vincolante per
ogni agente, sviluppatore o fornitore che lavori sul repository.

---

## 1. Perché esiste

Il pacchetto documentale consegnato il 20 settembre 2026, conservato fuori dal repository, in una
posizione privata, contiene:

- materiale marcato **RISERVATO — NON DESTINATO ALLA DIFFUSIONE** (Master Dossier v2.0);
- materiale marcato **SPECIFICA TECNICA RISERVATA — PRE-SVILUPPO** (Technical Blueprint v1.0);
- **dati personali comuni e identificativi** di una persona fisica (modulo di deposito SIAE compilato:
  codice fiscale, data e luogo di nascita, indirizzo di residenza, numero di cellulare, e-mail privata);
- **materiale probatorio di proprietà intellettuale** destinato al deposito SIAE prima della
  divulgazione pubblica del 2 ottobre 2026.

La pubblicazione, anche accidentale, di questo materiale prima del deposito comprometterebbe la
strategia di tutela descritta nel Master Dossier §13 (il deposito SIAE tutela l'opera **inedita**) e
costituirebbe una violazione del GDPR rispetto ai dati personali contenuti nel Mod. 350.

---

## 2. Regola fondamentale

> **I documenti sorgente riservati non entrano nel repository. Mai.**

Nessun file del pacchetto, né una sua copia, né una sua estrazione testuale integrale, può essere
copiato nel repository.

Questo vale anche per `docs/`, anche per sottocartelle che sembrano private, anche per file
`.gitignore`-ati: il repository può diventare pubblico o essere consegnato a un fornitore, e un file
ignorato resta comunque sul disco di chiunque riceva la cartella.

### Aggiornamento del 21 settembre 2026 — la regola non ammette più l'eccezione

Fino al 21 settembre questa sezione conteneva un'eccezione: i due PDF del 17 settembre
(`ILE_Document_Implementation_FR.pdf`, `ILE_Annexe_1_Textes_Juridiques_FR.pdf`) stavano in
`docs/source/` «perché sono istruzioni di pubblicazione i cui testi sono destinati al sito
pubblico», a differenza del pacchetto del 20 settembre, che è materiale di tutela interna.

**L'eccezione è ritirata.** La motivazione vale per i *testi*, non per i *documenti*. Un PDF del
committente — con la sua autrice, la sua versione, le sue istruzioni interne e la sua storia
redazionale — non diventa un artefatto pubblico perché alcune sue frasi finiranno su una pagina. E
l'estrazione testuale integrale è la stessa cosa in forma ancora più comoda da leggere.

I quattro file sono stati rimossi dalla working tree e da **ogni commit** il 21 settembre 2026.
Vivono ora accanto al resto del materiale sorgente fuori dal repository.
`scripts/verify_locked_against_source.py` li legge da lì tramite `ILE_SOURCE_DIR`, e dichiara
«non verificato» invece di fingere un esito positivo quando non li trova.

La regola §2 ora non ha eccezioni: **nessun documento sorgente del committente entra nel
repository.**

---

## 3. Dove stanno i file

| Cosa | Dove | Nel repo? |
|---|---|---|
| Documenti originali (docx/pdf) | fuori dal repository, in una posizione privata | NO |
| Estrazioni testuali di lavoro | fuori dal repository, in una posizione privata | NO |
| Manifest con SHA-256 e metadati | `docs/source-of-truth/DOCUMENT_MANIFEST.md` | SÌ |
| Requisiti derivati, identificati da ID | `docs/source-of-truth/REQUIREMENT_MATRIX_V2.md` | SÌ |
| Note di implementazione sanificate | `docs/platform/*`, `docs/security/*` | SÌ |

Il manifest cita **titolo, versione, data, hash e finalità**, mai il contenuto riservato.

---

## 4. Cosa non deve mai comparire da nessuna parte

**Vietato nel repository, nei commit, nei log, nei test, nelle fixture, nei messaggi di errore, nei
commenti di codice e in qualunque documentazione pubblica o interna:**

- codice fiscale, data e luogo di nascita, indirizzo di residenza, numero di telefono privato,
  estremi di documenti d'identità, e-mail personali o di studio professionale di qualunque persona
  fisica citata nei documenti di deposito;
- il testo integrale del Master Dossier, del Technical Blueprint, della Relazione Tecnica, del
  Dossier SIAE, della Scheda Mod. 350 e del Mod. 350 compilato;
- diagrammi interni completi dell'architettura;
- la logica dettagliata del Rule Engine (condizioni, alberi decisionali, DSL delle regole) in forma
  pubblicamente accessibile;
- schemi di database, nomi di tabelle e relazioni in pagine pubbliche o in documentazione API pubblica;
- l'architettura di sicurezza interna (threat model, controlli, segreti, topologia) in forma pubblica;
- riferimenti a tariffe, pagamenti, numeri di pratica o corrispondenza con SIAE;
- i nomi delle persone fisiche titolari o referenti del progetto **sul sito pubblico** (gate G5 e §69
  della direttiva di rebase: il sito espone l'identità *Italy Legal Entry™ / AGAMI*, non persone).

**Vietato pubblicare via web:**

- qualunque percorso servito da `/static/` o `/media/` che punti a questo materiale;
- allegati del Forum o documenti dell'area riservata che contengano materiale di deposito;
- pagine CMS, articoli o FAQ che riproducano interi paragrafi dei documenti riservati.

---

## 5. Cosa è invece consentito

- **Derivare requisiti**: leggere il Blueprint e implementarne il modello dati, i ruoli, gli stati del
  fascicolo e i workflow. Il software realizzato **è** l'esito atteso di quei documenti.
- **Citare identificatori**: `REQ-PLT-014` è un riferimento legittimo in un commit o in un test.
- **Scrivere documentazione derivata e sanificata**: per esempio `docs/platform/CASE_LIFECYCLE.md`
  descrive gli stati del fascicolo perché sono necessari a chi sviluppa, ma non riproduce il documento.
- **Parafrasare a fini tecnici** in documentazione interna, evitando la riproduzione estesa della
  forma espressiva dell'opera, che è precisamente l'oggetto della tutela (Master Dossier §12).

---

## 6. Controlli automatici

| Controllo | Dove | Cosa impedisce |
|---|---|---|
| `tests/security/test_confidential_material.py` | suite | Presenza nel repo di file con i nomi o gli hash del pacchetto riservato; presenza, in qualunque file versionato, delle marcature di riservatezza e dei riferimenti pubblici del modulo di deposito. Gli identificativi privati del depositante non sono scritti nel test né altrove nel repository: il test li legge da una tabella privata fuori dal repository, indicata dalla variabile `ILE_CONFIDENTIAL_SENTINELS` (`.env` locale), e li cerca in ogni file versionato. Senza la variabile un test dedicato risulta **saltato** e lo dichiara; con la variabile ma la tabella mancante, illeggibile o vuota, i test **falliscono** |
| `.gitignore` | repo | `docs/source-of-truth/_raw/`, `*.docx`, `mod_350*`, `*RISERVATO*` |
| `tests/compliance/test_no_person_names.py` | suite | Nomi di persone fisiche in template, seed, locale e pagine renderizzate |
| Revisione manuale | ogni PR che tocca `docs/` | Riproduzione estesa di materiale riservato |

Gli hash SHA-256 nel manifest servono anche a questo: un test può verificare che nessun file del
repository corrisponda a un documento riservato, senza doverne conoscere il contenuto.

---

## 7. Accesso e contratti

Il Master Dossier §16 e il Blueprint §19 prescrivono che **prima** dell'accesso ai repository e alle
specifiche complete siano disciplinati per iscritto riservatezza, proprietà intellettuale,
disponibilità del codice, credenziali e obblighi alla cessazione del rapporto.

Finché tale accordo non è documentato, vale la regola operativa più prudente:

- accesso al repository nominativo e limitato;
- nessuna condivisione del pacchetto documentale con terzi, fornitori o servizi esterni;
- nessun caricamento dei documenti su servizi di terze parti (traduttori online, convertitori PDF,
  archiviazione cloud non governata, strumenti di analisi esterni);
- marcatura `RISERVATO` conservata su ogni copia di lavoro.

---

## 8. In caso di esposizione accidentale

1. Non riscrivere la storia di Git di propria iniziativa: annotare commit, file e orario.
2. Informare immediatamente la titolare del progetto e il referente tecnico.
3. Se il repository è stato pubblicato: considerare il materiale compromesso ai fini del requisito di
   «opera inedita» e segnalarlo prima di qualunque deposito o rinnovo SIAE.
4. Se sono stati esposti dati personali: valutare la notifica ex artt. 33–34 GDPR con il titolare del
   trattamento; il termine di 72 ore decorre dalla conoscenza.
5. Documentare l'incidente in `docs/security/` con causa, impatto e misura correttiva.

---

## 9. Riferimenti

- `docs/source-of-truth/DOCUMENT_MANIFEST.md` — inventario con hash
- `docs/source-of-truth/CONFIDENTIALITY_REGISTER.md` — classificazione documento per documento
- `docs/source-of-truth/SOURCE_HIERARCHY.md` — quale documento governa quale decisione
- `docs/PRIVACY_BY_DESIGN.md` — trattamento dei dati degli utenti della piattaforma
- `docs/security/DATA_CLASSIFICATION.md` — classificazione dei dati applicativi
