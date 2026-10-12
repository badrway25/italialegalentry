# CONFLICT REGISTER — contraddizioni fra le fonti

Versione 1.0 · 20 settembre 2026 · Aggiornare a ogni nuova fonte o versione

Nessuna contraddizione significativa viene risolta in silenzio. Ogni riga dichiara cosa è stato
deciso, con quale motivazione, e se serve una conferma del committente.

Stato: **RISOLTO** deciso e implementabile · **RISOLTO CON RISERVA** implementato ma da confermare ·
**APERTO** serve una decisione del committente · **BLOCCATO** impossibile procedere.

---

## CR-01 — Stack tecnologico: Next.js/NestJS contro Django

| | |
|---|---|
| **Fonte A** | D2 Technical Blueprint §14: «Frontend: Next.js / React, TypeScript»; «Backend: NestJS/Node.js TypeScript oppure FastAPI/Python»; «Identity: Provider OIDC/OAuth2 o servizio dedicato con MFA». §15 propone una struttura di repository monorepo `apps/web`, `apps/api`, `apps/worker`, `packages/*`. |
| **Fonte B** | Direttiva del committente (prompt di rebase §42 e §50): «Use Django architecture already selected unless there is a documented critical reason to change it. Do NOT rewrite the whole system in Next.js/Nest/FastAPI just because a technical document mentions those as possible technology choices. Project directive remains: Django-based ecosystem.» |
| **Impatto** | Totale: riscrivere o conservare l'intera codebase. Circa 45 000 righe di Python, 169 template, 1 871 test. |
| **Interpretazione** | **Nessun conflitto reale.** D2 §14 si intitola «Stack tecnico raccomandato — **da validare da Badr**» e nel primo capoverso dichiara: «Lo stack seguente è una proposta pragmatica e **non un vincolo di titolarità**. Badr può confermarlo o sostituirlo motivando compatibilità, sicurezza, competenze e costi.» D2 §18 elenca fra le cose che Badr deve validare la «Scelta definitiva dello stack e motivazione di eventuali modifiche» e chiede una revisione puntuale APPROVATO / DA MODIFICARE / NON IMPLEMENTABILE. La scelta Django è quindi l'esito previsto dal documento stesso. |
| **Decisione** | **Django 5.2 LTS + PostgreSQL 17 confermato.** Motivazione registrata in `docs/ARCHITECTURE_DECISION_RECORDS/ADR-012-stack-validation.md`, redatta nella forma richiesta da D2 §18. La struttura del repository resta il monolite modulare `apps/<dominio>` già in essere; la corrispondenza con la struttura proposta da D2 §15 è mappata nell'ADR. |
| **Stato** | **RISOLTO** |

---

## CR-02 — API REST versionate contro rendering server-side

| | |
|---|---|
| **Fonte A** | D2 §11 specifica diciotto endpoint REST (`POST /auth/register`, `POST /assessments`, `GET /cases/{id}`, …) e §14 chiede «API REST versionate». |
| **Fonte B** | Il prodotto attuale è server-rendered con progressive enhancement; nessun client JavaScript consuma API. D0a impone budget di performance e assenza di dipendenze esterne. |
| **Impatto** | Medio: una superficie API non utilizzata è superficie d'attacco in più (D3 §16 chiede interfacce «documentate e controllate»). |
| **Interpretazione** | Gli endpoint di D2 §11 descrivono le **operazioni di dominio**, non impongono un trasporto HTTP pubblico. Ogni operazione esiste come servizio applicativo tipizzato; l'esposizione HTTP avviene oggi tramite viste Django con gli stessi controlli di autorizzazione. |
| **Decisione** | Implementare le diciotto operazioni come **servizi di dominio** con nomi corrispondenti e documentare la mappatura operazione → vista/servizio in `docs/platform/FEATURE_MATRIX.md`. Nessuna API pubblica finché non esiste un consumatore reale e un accordo che la giustifichi; quando servirà, si aggiunge un livello `/api/v1/` sopra gli stessi servizi. |
| **Stato** | **RISOLTO** |

---

## CR-03 — «Ricerca e selezione» nella piattaforma contro divieto pubblico di intermediazione

| | |
|---|---|
| **Fonte A** | D2 §3 modulo «Ricerca e selezione»; §4 ruolo «Soggetto autorizzato»; §6 passi 5–6 del percorso impresa; §9 entità `SelectionProcess`; §16 epic P1 «Authorized selection». D1 §4: «Le attività di selezione, intermediazione, formazione regolamentata o altre attività riservate restano affidate ai soggetti autorizzati secondo la normativa applicabile.» |
| **Fonte B** | D0a vieta sul sito pubblico ogni formulazione di reclutamento, matching, ricerca di profili o area imprese per richieste di reclutamento. |
| **Impatto** | Alto: è il cuore del modello di business e insieme il rischio legale maggiore. |
| **Interpretazione** | Le due fonti non si contraddicono: **separano pubblico e interno**. Pubblicamente Italy Legal Entry rileva fabbisogni e organizza formazione; operativamente un soggetto autorizzato può condurre un processo di selezione tracciato sulla piattaforma, sotto la propria responsabilità. |
| **Decisione** | Catena obbligatoria `CompanyNeed → AuthorizedActor → SelectionProcess → CaseFile → AuditEvent`. Vincoli implementati: nessuna vista pubblica, nessun elenco di persone navigabile da un'impresa, `SelectionProcess` non creabile senza `AuthorizedActor` valido e non scaduto, ogni transizione genera un `AuditEvent`, l'interfaccia nomina sempre l'attore responsabile. Test in `tests/compliance/` impediscono la comparsa pubblica del modulo e la creazione senza attore. |
| **Stato** | **RISOLTO** |

---

## CR-04 — Visibilità dei candidati da parte dell'impresa

| | |
|---|---|
| **Fonte A** | D2 §4, riga Impresa, colonna Vincoli: «Visibilità candidati solo secondo base giuridica/consenso e workflow autorizzato». |
| **Fonte B** | D2 §17, criterio di accettazione: «Un'impresa può esprimere un fabbisogno senza accedere indiscriminatamente ai dati personali.» Direttiva di rebase §29: «No unrestricted people browser. No candidate profile cards by default.» |
| **Impatto** | Alto, privacy e conformità. |
| **Interpretazione** | La prima fonte ammette una visibilità **condizionata**; la seconda vieta quella **indiscriminata**. Sono compatibili se la visibilità è per singola persona, dentro un processo di selezione, con consenso specifico registrato. |
| **Decisione** | Deny by default. L'impresa vede dati personali solo attraverso un `SelectionProcess` attivo, solo per le persone che un attore autorizzato vi ha collegato, solo per i campi necessari al fabbisogno, e solo se esiste un `Consent` valido per la finalità «condivisione con impresa». Ogni accesso è tracciato. Nessuna ricerca libera, nessun elenco. In P0 la visibilità è **zero**: si abilita in P1 con il workflow autorizzato. |
| **Stato** | **RISOLTO** |

---

## CR-05 — Data del Forum: 25 settembre contro 2 ottobre

| | |
|---|---|
| **Fonte A** | D0a: «Phase 2 avant le 25 septembre, Phase 3 après le 2 octobre»; e nella scheda evento: «Rovigo — 2 octobre 2026 — Sala della Gran Guardia — 15h00–18h00». |
| **Fonte B** | D1 §8: «La prima edizione italiana, a Rovigo il 2 ottobre 2026, rappresenta l'avvio pubblico del percorso.» |
| **Impatto** | Alto se frainteso: una data sbagliata su un evento istituzionale. |
| **Interpretazione** | **Nessun conflitto.** Il 25 settembre è la scadenza di consegna della Fase 2, non la data dell'evento. Entrambe le fonti collocano il Forum il **2 ottobre 2026** a Rovigo. |
| **Decisione** | Data dell'evento 02/10/2026, 15:00–18:00, Sala della Gran Guardia, Rovigo, in tutte le lingue, nel JSON-LD e nelle e-mail. Il gate Fase 3 si apre il 2 ottobre. Verificato dal red team: coerente ovunque. |
| **Stato** | **RISOLTO** |

---

## CR-06 — Nomi degli intervenienti e delle persone fisiche

| | |
|---|---|
| **Fonte A** | D1, D4, D5, D6 nominano ripetutamente le persone fisiche titolari e referenti del progetto; D1 §17 contiene una dichiarazione di paternità nominativa. |
| **Fonte B** | D0a: i nomi degli intervenienti saranno pubblicati solo con il programma definitivo; gate G5 chiuso. Direttiva di rebase §69: identità *Italy Legal Entry / AGAMI*. |
| **Impatto** | Medio: rischio di esporre dati personali e di attribuire pubblicamente ruoli non ancora confermati. |
| **Interpretazione** | I documenti di tutela nominano le persone **a fini probatori**; non sono copy del sito (SOURCE_HIERARCHY P1). |
| **Decisione** | Nessun nome di persona fisica sul sito pubblico, in nessuna lingua, nemmeno nei metadati, nel JSON-LD, negli autori degli articoli o nei commit dei contenuti. Il sito espone funzioni e organizzazioni. Test `tests/compliance/test_no_person_names.py`. |
| **Stato** | **RISOLTO** |

---

## CR-07 — Art. 23 del Testo Unico Immigrazione

| | |
|---|---|
| **Fonte A** | D4 §9: «possibile complementarità con i programmi di formazione finalizzati all'ingresso per lavoro previsti dalla normativa vigente, inclusi i percorsi riconducibili all'art. 23 del Testo Unico Immigrazione». |
| **Fonte B** | D0a vieta di presentare il pilota come autorizzato ai sensi dell'art. 23 del D.Lgs. 286/1998. |
| **Impatto** | Alto: una autorizzazione inesistente dichiarata pubblicamente. |
| **Interpretazione** | D4 parla di **complementarità possibile in prospettiva**, non di autorizzazione ottenuta. |
| **Decisione** | L'art. 23 non compare sul sito pubblico come base del pilota. Se un contenuto informativo dovrà citarlo, lo farà come norma di sistema, mai come titolo abilitante del progetto, e passerà per la revisione legale. Formulazione vietata già coperta da `tests/compliance/`. |
| **Stato** | **RISOLTO** |

---

## CR-08 — Hosting UE: requisito contro stato di fatto

| | |
|---|---|
| **Fonte A** | D3 §10: l'ambiente di produzione «dovrà essere collocato nello Spazio Economico Europeo»; il provider «dovrà essere verificato prima della messa in produzione». D2 §13: «Hosting preferibilmente in area UE/SEE con contratti e localizzazione documentati». |
| **Fonte B** | Nessuna attestazione di hosting è stata fornita. Gate G12 `PENDING_CLIENT`. |
| **Impatto** | Blocca il deploy, non lo sviluppo locale. |
| **Interpretazione** | È un requisito non ancora soddisfatto, non una contraddizione. |
| **Decisione** | G12 resta aperto come blocker di rilascio. `docs/DEPLOYMENT.md` richiede l'attestazione scritta prima del primo deploy. Nessuna affermazione pubblica sull'ubicazione dei server finché non è documentata. |
| **Stato** | **APERTO — conferma del committente necessaria** |

---

## CR-09 — «Candidato» come ruolo a sé

| | |
|---|---|
| **Fonte A** | D3 §4 elenca fra i profili logici «visitatore; utente/persona; **candidato**; impresa; operatore; professionista; amministratore; partner istituzionale». |
| **Fonte B** | D2 §4 elenca nove ruoli e **non** prevede «candidato»: Persona, Impresa, Soggetto autorizzato, Ente formativo, Professionista, Istituzione, Università, Amministratore, Legal/Rule Editor. |
| **Impatto** | Medio: un ruolo in più significa un perimetro di permessi in più da mantenere. |
| **Interpretazione** | D2 è più recente (20/09 contro 07/09) e più preciso. «Candidato» non è un ruolo di accesso: è uno **stato** della persona dentro un processo di selezione. Trattarlo come ruolo creerebbe per giunta una categoria di utenti «mercificabile», in tensione con il divieto di marketplace. |
| **Decisione** | Nessun ruolo `CANDIDATE`. La condizione di candidato è rappresentata da `SelectionProcess.stage` sul fascicolo della persona. |
| **Stato** | **RISOLTO** |

---

## CR-10 — Ruoli editoriali assenti dal Blueprint

| | |
|---|---|
| **Fonte A** | D2 §4 non prevede ruoli editoriali distinti oltre ad Amministratore e Legal/Rule Editor. |
| **Fonte B** | Direttiva di rebase §42 chiede esplicitamente `CONTENT_EDITOR`, `OPERATOR`, `MODERATOR`; D2 §20 impone che i testi multilingue siano gestiti via i18n/CMS, il che presuppone qualcuno che li gestisca senza avere i privilegi di amministratore. |
| **Impatto** | Medio: senza ruoli editoriali, ogni modifica di contenuto richiede un amministratore, contro il principio del minimo privilegio di D2 §13. |
| **Interpretazione** | Il Blueprint elenca i ruoli **principali**, non esaurisce il modello. La separazione dei compiti che esso stesso impone richiede questi ruoli. |
| **Decisione** | Aggiunti `CONTENT_EDITOR`, `OPERATOR`, `TRAINING_ORGANIZATION`, `AUTHORIZED_ACTOR`, `PROFESSIONAL`, `LEGAL_RULE_EDITOR` alla tassonomia dei ruoli esistente. Il Legal/Rule Editor non può auto-approvare: workflow a quattro occhi come prescritto da D2 §4. |
| **Stato** | **RISOLTO** |

---

## CR-11 — `effect: eligible` contro divieto di determinazioni amministrative

| | |
|---|---|
| **Fonte A** | D2 §7, tabella dei campi regola: «effect: **eligible** / possible / missing_requirement / stop / warning». |
| **Fonte B** | D2 §17: «Nessun testo dell'interfaccia promette rilascio di visto/permesso o attribuisce alla piattaforma funzioni pubbliche/riservate.» D2 §7 §8: l'esito «è orientativo». Direttiva di rebase §24: gli esiti ammessi sono POSSIBLE, MISSING_REQUIREMENT, WARNING, STOP, REVIEW_REQUIRED; «eligible» non compare. |
| **Impatto** | Alto: «eligible» letto da un utente significa «ho diritto di entrare». |
| **Interpretazione** | `eligible` è un nome tecnico interno del documento, non un testo da mostrare. Il suo significato reale coincide con `possible`. Mantenerlo aumenterebbe il rischio che affiori in interfaccia. |
| **Decisione** | Cinque esiti: `POSSIBLE`, `MISSING_REQUIREMENT`, `WARNING`, `STOP`, `REVIEW_REQUIRED`. `eligible` **non** esiste nel dominio. La documentazione registra l'equivalenza `eligible ≡ POSSIBLE` per tracciabilità verso D2. Nessuna etichetta pubblica usa «idoneo», «ammissibile» o «ha diritto». |
| **Stato** | **RISOLTO** |

---

## CR-12 — Retention: 24 mesi contro «configurabile»

| | |
|---|---|
| **Fonte A** | D0a fissa la conservazione a 24 mesi dall'ultimo contatto per i dati dei form pubblici. |
| **Fonte B** | D2 §20 e D3 §8 impongono che i tempi di retention siano **configurabili** secondo policy e base giuridica, non costanti nel codice. Direttiva di rebase §45: «Do not invent retention periods.» |
| **Impatto** | Medio. |
| **Interpretazione** | Compatibili: 24 mesi è il **valore configurato** per una specifica finalità, non l'unico periodo del sistema. |
| **Decisione** | La retention è un dato per finalità di trattamento, amministrabile dal back-office, con valore iniziale 24 mesi per le richieste dei form pubblici, come da D0a. Nessun altro periodo viene inventato: le finalità prive di indicazione restano senza scadenza automatica e sono elencate come questione aperta in `docs/PRIVACY_BY_DESIGN.md`. |
| **Stato** | **RISOLTO CON RISERVA** — i periodi delle finalità della piattaforma autenticata richiedono la policy del titolare |

---

## CR-13 — Forum: evento pubblico contro modulo di governance permanente

| | |
|---|---|
| **Fonte A** | D0a descrive una pagina evento che il 2 ottobre diventa «Forum Permanente Vénétie–Maroc». |
| **Fonte B** | D2 §12 descrive un **modulo applicativo autenticato**: forum virtuale, commissioni miste, tavoli digitali, proposte, progetti, monitoraggio, relazione annuale. D1 §8 descrive il Forum come «spazio stabile di dialogo», non un convegno. |
| **Impatto** | Alto sull'architettura informativa: sono due prodotti diversi con lo stesso nome. |
| **Interpretazione** | Sono due facce dello stesso programma: una vetrina pubblica e un motore di governance riservato ai partecipanti. |
| **Decisione** | Due superfici distinte con contenuto separato: sezione pubblica (evento, programma, contesto, esiti, prossime tappe) e workspace autenticato (profilo partecipante, commissioni configurabili, tavoli, proposte, progetti, milestone, monitoraggio, relazione annuale). Il workspace resta dietro il flag `virtual_forum`, chiuso fino a dopo il 30 ottobre e comunque subordinato a G1. La tassonomia delle commissioni è dato amministrabile, come impone D2 §20. |
| **Stato** | **RISOLTO** |

---

## CR-14 — Academy indipendente dalla selezione

| | |
|---|---|
| **Fonte A** | D2 §5 passo 8: «Accesso immediato all'Academy, indipendentemente dall'esistenza di una selezione lavorativa»; D2 §17 lo ripete come criterio di accettazione. |
| **Fonte B** | D1 §4 e D4 §6 legano la formazione ai fabbisogni rilevati dalle imprese: «evitare percorsi formativi scollegati dalla domanda di lavoro». |
| **Impatto** | Medio, riguarda l'architettura del prodotto formativo. |
| **Interpretazione** | La fonte B descrive come si **progetta il catalogo** (partendo dai fabbisogni); la fonte A descrive chi può **accedervi** (chiunque, senza essere selezionato). Non si escludono. |
| **Decisione** | Catalogo costruito a partire dai fabbisogni territoriali; accesso aperto a ogni persona autenticata senza `SelectionProcess`. Il collegamento fabbisogno → piano formativo esiste come percorso consigliato, non come condizione di accesso. Test di accettazione dedicato. |
| **Stato** | **RISOLTO** |

---

## CR-15 — Dati personali reali in sviluppo

| | |
|---|---|
| **Fonte A** | D2 §13: «Nessun dato personale reale negli ambienti di sviluppo/test salvo casi eccezionali governati.» D3 §11 idem. |
| **Fonte B** | Il pacchetto documentale D6 contiene dati personali reali ed è sul disco della macchina di sviluppo. |
| **Impatto** | Alto sul piano della conformità. |
| **Interpretazione** | Il documento sta fuori dal repository e non è un dato applicativo, ma il principio impone di trattarlo come tale. |
| **Decisione** | `docs/security/CONFIDENTIAL_MATERIAL_POLICY.md`; estrazione di lavoro redatta; nessun dato personale reale nelle fixture, nei seed o nei test; test automatico che cerca gli identificatori sentinella nel repository. |
| **Stato** | **RISOLTO** |

---

## Sintesi

| Stato | Conflitti |
|---|---|
| RISOLTO | CR-01, CR-02, CR-03, CR-04, CR-05, CR-06, CR-07, CR-09, CR-10, CR-11, CR-13, CR-14, CR-15 |
| RISOLTO CON RISERVA | CR-12 |
| APERTO | CR-08 (attestazione hosting UE) |
| BLOCCATO | nessuno |

Un solo elemento richiede una decisione del committente e riguarda il deploy, non lo sviluppo.
Il lavoro prosegue.
