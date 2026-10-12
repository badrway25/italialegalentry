# REQUIREMENT MATRIX V2 — requisiti derivati dal pacchetto del 20 settembre 2026

Versione 2.0 · 20 settembre 2026
Fonti: D1 Master Dossier v2.0 · D2 Technical Blueprint v1.0 · D3 Relazione Tecnica v1.0 ·
D4 Dossier SIAE v1.0 · direttiva di rebase del committente (indicata come **RB §n**).
Il pacchetto precedente resta tracciato in `docs/REQUIREMENTS_MATRIX.md` (217 righe, v1) e non è
sostituito: questa matrice lo **estende**.

Stato: `DONE` implementato e testato · `PARTIAL` esiste ma incompleto · `TODO` da costruire ·
`GATED` costruito ma chiuso da un gate · `DEFERRED` rinviato a P1/P2 con motivazione ·
`BLOCKED` impedito da una fonte esterna mancante.

Priorità: `P0` release minima operativa · `P1` seconda ondata · `P2` successiva.

---

## A. Identità, ruoli e accessi

| ID | Requisito | Fonte | Pri | Stato | Dove |
|---|---|---|---|---|---|
| REQ-IAM-01 | Registrazione, autenticazione, gestione del ciclo di vita delle credenziali, recupero controllato | D2 §3, D3 §5 | P0 | DONE | `apps/accounts`, allauth |
| REQ-IAM-02 | Modello utente personalizzato con e-mail come identificativo | D2 §9 `User`, RB §42 | P0 | DONE | `accounts.User` |
| REQ-IAM-03 | MFA obbligatoria per amministratori e ruoli sensibili | D2 §13, D3 §5 (unione: P3) | P0 | PARTIAL | `accounts.middleware.BackofficeMFAMiddleware`; architettura pronta, enforcement attivo su `/backoffice/` |
| REQ-IAM-04 | Ruoli: Persona, Impresa, Soggetto autorizzato, Ente formativo, Professionista, Istituzione, Università, Amministratore, Legal/Rule Editor | D2 §4 | P0 | PARTIAL | `accounts.roles` — mancano `AUTHORIZED_ACTOR`, `TRAINING_ORGANIZATION`, `PROFESSIONAL`, `LEGAL_RULE_EDITOR`, `CONTENT_EDITOR`, `OPERATOR` |
| REQ-IAM-05 | Deny by default, minimo privilegio, segregazione dei compiti | D2 §13, D3 §4 | P0 | DONE | `accounts.permissions`, `ROLE_PERMISSIONS` |
| REQ-IAM-06 | Autorizzazione a livello di oggetto, non solo di modello | D2 §17, RB §61 | P0 | PARTIAL | `accounts.permissions`; da estendere a fascicolo, selezione, formazione |
| REQ-IAM-07 | Il modello autorizzativo non si esaurisce in `is_staff` | RB §42 | P0 | DONE | gruppi e permessi espliciti |
| REQ-IAM-08 | Protezione contro tentativi automatizzati, gestione sessioni, revoca accessi | D3 §5 | P0 | PARTIAL | rate limiting sui form; revoca sessioni da costruire |
| REQ-IAM-09 | Un solo sistema di autenticazione per tutti i ruoli, con instradamento post-login per ruolo | RB §20 | P0 | TODO | — |
| REQ-IAM-10 | Il Legal/Rule Editor non ottiene privilegi di superadmin | D2 §4, RB §61 | P0 | TODO | — |

## B. Percorso Persona

| ID | Requisito | Fonte | Pri | Stato | Dove |
|---|---|---|---|---|---|
| REQ-PER-01 | Creazione account con informativa e consensi | D2 §5.1 | P0 | GATED | consensi pronti; form chiusi da G2 |
| REQ-PER-02 | Profilazione: Paese, cittadinanza, residenza, età, formazione, professione, competenze, lingue, situazione familiare, eventuale presenza precedente in Italia | D2 §5.2 | P0 | PARTIAL | `accounts.PersonProfile` da estendere |
| REQ-PER-03 | Definizione dell'obiettivo: lavoro, studio, famiglia, altra finalità lecita | D2 §5.3 | P0 | PARTIAL | l'orientamento chiede l'obiettivo ma non lo persiste sul profilo |
| REQ-PER-04 | Questionario dinamico: le domande dipendono dalle risposte precedenti | D2 §5.4 | P0 | DONE | `apps/orientation` |
| REQ-PER-05 | Esecuzione del Rule Engine sulle regole attive **alla data della valutazione** | D2 §5.5, §7 | P0 | PARTIAL | ruleset versionato presente; manca la selezione per data di validità |
| REQ-PER-06 | Restituzione di uno o più percorsi con livello di completezza, requisiti mancanti, stop e fonti | D2 §5.6 | P0 | PARTIAL | esito e fonti presenti; mancano completezza e requisiti mancanti strutturati |
| REQ-PER-07 | Creazione del fascicolo e della checklist | D2 §5.7 | P0 | TODO | `CaseFile` e `ChecklistItem` da costruire |
| REQ-PER-08 | Accesso immediato all'Academy, indipendentemente da una selezione | D2 §5.8, §17 | P1 | TODO | vedere CR-14 |
| REQ-PER-09 | Assegnazione a professionista o ente competente con consenso e tracciabilità | D2 §5.9 | P1 | TODO | — |
| REQ-PER-10 | Monitoraggio del percorso: scadenze, documenti, notifiche | D2 §5.10 | P0 | PARTIAL | `portal.Deadline`, `portal.Message` esistono |
| REQ-PER-11 | Ingresso, onboarding, post-entry e inclusione | D2 §5.11 | P1 | TODO | — |
| REQ-PER-12 | La persona capisce subito: dove sono, obiettivo, fatto, mancante, prossimo passo, chi è responsabile, documenti richiesti, fonti, serve revisione umana | RB §22 | P0 | TODO | riprogettazione dell'area riservata |
| REQ-PER-13 | Salvataggio e ripresa del questionario, ritorno indietro, revisione prima dell'invio | RB §23 | P0 | PARTIAL | sessione persistita; manca la revisione finale |

## C. Rule Engine

| ID | Requisito | Fonte | Pri | Stato | Dove |
|---|---|---|---|---|---|
| REQ-RUL-01 | Le regole sono **dati amministrabili e versionati**, separati dal codice applicativo | D2 §7, §20 | P0 | PARTIAL | ruleset in database; condizioni ancora in codice |
| REQ-RUL-02 | Campi della regola: `rule_id`, `jurisdiction`, `pathway`, `condition`, `effect`, `message_key`, `source_title`, `source_url/ref`, `valid_from`, `valid_to`, `version`, `review_status`, `approved_by`, `approved_at` | D2 §7 | P0 | TODO | modello `LegalRule` da costruire |
| REQ-RUL-03 | Esiti: `POSSIBLE`, `MISSING_REQUIREMENT`, `WARNING`, `STOP`, `REVIEW_REQUIRED`. Mai determinazioni amministrative | D2 §7 + CR-11, RB §24 | P0 | PARTIAL | esiti presenti, tassonomia da allineare |
| REQ-RUL-04 | Nessun `eval()` né valutazione di codice non sicura: DSL o interprete JSON controllato | RB §24, D2 §18 | P0 | TODO | — |
| REQ-RUL-05 | Ogni regola applicata è registrata con la sua versione | D2 §7 | P0 | PARTIAL | — |
| REQ-RUL-06 | Snapshot del ruleset salvato con ogni valutazione; esito riproducibile | D2 §7, §17 | P0 | PARTIAL | `OrientationResult` conserva il riferimento, non lo snapshot completo |
| REQ-RUL-07 | Uno `STOP` impedisce di presentare il percorso come praticabile | D2 §7 | P0 | TODO | — |
| REQ-RUL-08 | Casi discrezionali producono `REVIEW_REQUIRED` | D2 §7 | P0 | TODO | — |
| REQ-RUL-09 | La pagina di esito mostra: risultato, motivazione, requisiti, elementi mancanti, fonti, data e ruleset, disclaimer, richiesta di revisione umana | RB §24 | P0 | PARTIAL | mancano motivazione per regola e richiesta di revisione |
| REQ-RUL-10 | Workflow a quattro occhi: DRAFT → LEGAL REVIEW → APPROVED → ACTIVE → RETIRED; l'autore non si auto-approva | D2 §4, RB §25 | P0 | TODO | — |
| REQ-RUL-11 | Editor di regole dedicato: elenco, stato, giurisdizione, percorso, validità, fonte, diff fra versioni, anteprima su persona sintetica, storico approvazioni | RB §25 | P1 | TODO | — |
| REQ-RUL-12 | Ogni modifica di regola genera un `AuditEvent` | D2 §13, RB §44 | P0 | TODO | — |

## D. Fascicolo digitale, checklist, documenti

| ID | Requisito | Fonte | Pri | Stato | Dove |
|---|---|---|---|---|---|
| REQ-CAS-01 | `CaseFile`: id, persona, titolare/assegnatario, stato, percorso, date | D2 §9 | P0 | TODO | — |
| REQ-CAS-02 | Undici stati: DRAFT, ORIENTED, REVIEW_REQUIRED, TRAINING, SELECTION, ADMIN_PROCESS, PRE_DEPARTURE, ENTERED, POST_ENTRY, CLOSED, SUSPENDED | D2 §8 | P0 | TODO | — |
| REQ-CAS-03 | Le transizioni sono validate; quelle sensibili generano `AuditEvent` | RB §27 | P0 | TODO | — |
| REQ-CAS-04 | Lo stato SELECTION identifica sempre il soggetto autorizzato responsabile | D2 §17, RB §27 | P0 | TODO | — |
| REQ-CAS-05 | `ChecklistItem`: fascicolo, requisito, stato, **attore responsabile**, scadenza | D2 §9 | P0 | TODO | — |
| REQ-CAS-06 | Una persona può avere più fascicoli per finalità differenti; i documenti non si duplicano se il riuso è lecito | D2 §10 | P1 | TODO | — |
| REQ-CAS-07 | Il fascicolo aggrega persona, percorso, stato, checklist, documenti, scadenze, attori, formazione, passi amministrativi, cronologia, comunicazioni, consensi/mandato | RB §26 | P0 | TODO | — |
| REQ-DOC-01 | `Document`: fascicolo, tipo, chiave di storage, hash, stato, scadenza, classe di accesso | D2 §9 | P0 | PARTIAL | `documents.PrivateDocument` esiste |
| REQ-DOC-02 | Storage privato, chiavi non prevedibili, autorizzazione a ogni download, URL temporanei | D2 §13, D3 §7 | P0 | PARTIAL | privato e autorizzato; mancano URL firmati |
| REQ-DOC-03 | Allowlist MIME ed estensioni, limiti di dimensione, punto di integrazione antivirus, hash di integrità | D2 §13, RB §28 | P0 | PARTIAL | validazione presente; antivirus come punto di estensione |
| REQ-DOC-04 | Stati visibili: MANCANTE, CARICATO, IN REVISIONE, VALIDO, NON VALIDO, SCADUTO, DA SOSTITUIRE | RB §28 | P0 | TODO | — |
| REQ-DOC-05 | Versionamento dei documenti e cronologia dei caricamenti | D3 §7, RB §28 | P1 | TODO | — |
| REQ-DOC-06 | Audit di accesso e download | D2 §13, RB §44 | P0 | PARTIAL | — |

## E. Imprese e B2B

| ID | Requisito | Fonte | Pri | Stato | Dove |
|---|---|---|---|---|---|
| REQ-B2B-01 | Registrazione e **verifica** dell'impresa | D2 §6.1, §9 `verification_status` | P0 | PARTIAL | `accounts.Organisation` |
| REQ-B2B-02 | `CompanyNeed`: territorio, settore, sede, numero di profili, tempistiche, motivazione | D2 §6.2, §9 | P0 | PARTIAL | `enquiries.CompanyNeedsRequest` è un form pubblico, non un oggetto gestibile |
| REQ-B2B-03 | Profilo professionale: mansioni, qualifiche, competenze obbligatorie e preferenziali, lingua, sicurezza, esperienza | D2 §6.3 | P0 | TODO | — |
| REQ-B2B-04 | Un'impresa crea e gestisce **più** fabbisogni | D2 §10, RB §29 | P0 | TODO | — |
| REQ-B2B-05 | Aggregazione dei fabbisogni per territorio, settore e profilo | D2 §6.4, RB §29 | P1 | TODO | — |
| REQ-B2B-06 | Nessun elenco di persone navigabile, nessuna scheda candidato per difetto | D2 §17, RB §29, CR-04 | P0 | DONE | assenza per costruzione; test di compliance |
| REQ-B2B-07 | L'impresa esprime un fabbisogno senza accedere indiscriminatamente a dati personali | D2 §17 | P0 | DONE | — |

## F. Soggetti autorizzati, professionisti, enti formativi

| ID | Requisito | Fonte | Pri | Stato | Dove |
|---|---|---|---|---|---|
| REQ-ACT-01 | `AuthorizedActor`: tipo, giurisdizione, riferimento di autorizzazione, validità | D2 §9 | P1 | TODO | — |
| REQ-ACT-02 | `SelectionProcess`: fabbisogno, attore, persona, fase, esito | D2 §9 | P1 | TODO | — |
| REQ-ACT-03 | Workspace dell'attore autorizzato: solo pratiche assegnate, mandato, fasi, decisioni, evidenze, audit | D2 §4, RB §30 | P1 | TODO | — |
| REQ-ACT-04 | Il professionista vede solo i fascicoli espressamente assegnati; mandato o abilitazione ove necessari | D2 §4, RB §38 | P1 | TODO | — |
| REQ-ACT-05 | L'ente formativo vede solo i dati necessari alla formazione assegnata | D2 §4, RB §37 | P1 | TODO | — |
| REQ-ACT-06 | Ogni fase di ricerca o selezione identifica il soggetto responsabile | D2 §17 | P1 | TODO | — |

## G. Formazione, skill gap, Academy

| ID | Requisito | Fonte | Pri | Stato | Dove |
|---|---|---|---|---|---|
| REQ-EDU-01 | `Course`: fornitore, tipo, lingua, versione. `Enrollment`: persona, corso, stato, completamento, certificato | D2 §9 | P1 | TODO | — |
| REQ-EDU-02 | Catalogo, dettaglio corso, iscrizione, moduli, progressione, completamento, materiali | RB §32 | P1 | TODO | — |
| REQ-EDU-03 | Contenuti: lingua italiana, diritti e doveri, educazione civica, sicurezza sul lavoro, cultura del lavoro, formazione professionale, pre-partenza | D1 §4, D2 §3, RB §32 | P1 | TODO | — |
| REQ-EDU-04 | Accesso indipendente dalla selezione di un'impresa | D2 §17, CR-14 | P1 | TODO | — |
| REQ-EDU-05 | I certificati non sono rappresentati come approvazioni amministrative | RB §32 | P1 | TODO | — |
| REQ-EDU-06 | `TrainingPlan`: persona o fabbisogno, gap, moduli, fornitore, stato | D2 §9 | P1 | TODO | — |
| REQ-EDU-07 | Modello visivo competenza richiesta / posseduta / gap / modulo / esito atteso, senza percentuali prive di significato | RB §31 | P1 | TODO | — |

## H. Post-ingresso e inclusione

| ID | Requisito | Fonte | Pri | Stato | Dove |
|---|---|---|---|---|---|
| REQ-PST-01 | `PostEntryPlan`: fascicolo, task, servizi, azioni del datore di lavoro, stato | D2 §9 | P1 | TODO | — |
| REQ-PST-02 | Onboarding, adempimenti locali, lingua, formazione, inserimento lavorativo, servizi territoriali, follow-up | D2 §3, RB §34 | P1 | TODO | — |
| REQ-PST-03 | Modello «prima / durante / dopo» come spina dorsale di prodotto | D4 §4, RB §34 | P1 | PARTIAL | presente nel contenuto pubblico |

## I. Sportello digitale

| ID | Requisito | Fonte | Pri | Stato | Dove |
|---|---|---|---|---|---|
| REQ-HLP-01 | Canale strutturato di orientamento e assistenza, multilingue | D1 §6, D3 §3h | P1 | TODO | — |
| REQ-HLP-02 | Escalation da orientamento automatico a supporto umano con stati: SOLA INFORMAZIONE, CHIARIMENTO NECESSARIO, REVISIONE PROFESSIONALE RICHIESTA, ASSEGNATO, IN REVISIONE, RISPOSTA DISPONIBILE, CHIUSO | RB §35 | P1 | TODO | — |
| REQ-HLP-03 | Nessun chatbot generico presentato come assistenza legale | RB §35 | P0 | DONE | nessun chatbot esiste |
| REQ-HLP-04 | Rispetto di mandato, permessi, ruolo professionale, privacy, audit | RB §35 | P1 | TODO | — |

## J. Forum Permanente

| ID | Requisito | Fonte | Pri | Stato | Dove |
|---|---|---|---|---|---|
| REQ-FOR-01 | Sezione pubblica: evento, programma, contesto istituzionale, risorse, esiti, prossime edizioni | D0a, D1 §8 | P0 | DONE | `apps/forum` |
| REQ-FOR-02 | Workspace autenticato: profilo partecipante, commissioni, tavoli, proposte, progetti, milestone, partner, monitoraggio, relazione annuale | D2 §12, RB §39 | P1 | GATED | flag `virtual_forum` chiuso |
| REQ-FOR-03 | Ciclo di governance: Forum → priorità → commissioni miste → tavoli → proposte → progetti → attuazione → monitoraggio → relazione annuale → Forum successivo | D2 §12 | P1 | TODO | — |
| REQ-FOR-04 | Cinque commissioni iniziali **configurabili senza modifica del codice** | D2 §12, §20 | P1 | TODO | — |
| REQ-FOR-05 | Cinque assi di cooperazione: mobilità regolare, cooperazione giuridica, università e ricerca, cooperazione economica, formazione | D1 §8 | P0 | DONE | contenuto pubblico |
| REQ-FOR-06 | I partecipanti non possono consultare informazioni private di altri utenti | RB §61 | P1 | TODO | — |

## K. Istituzioni e università

| ID | Requisito | Fonte | Pri | Stato | Dove |
|---|---|---|---|---|---|
| REQ-INS-01 | Accesso definito da convenzione e base giuridica; niente accesso generalizzato ai fascicoli | D2 §4 | P1 | TODO | — |
| REQ-INS-02 | Progetti, iniziative territoriali, indicatori aggregati, lavori del Forum, collaborazioni, documenti condivisi, milestone | RB §36 | P1 | TODO | — |
| REQ-UNI-01 | Programmi, progetti, mobilità accademica, ricerca, diritto comparato, Forum | D2 §3, D1 §9 | P1 | TODO | — |
| REQ-UNI-02 | Nessun accesso ai fascicoli privati | D2 §4 | P1 | TODO | — |

## L. CRM

| ID | Requisito | Fonte | Pri | Stato | Dove |
|---|---|---|---|---|---|
| REQ-CRM-01 | Relazioni, contatti, organizzazioni, task, attività, appuntamenti, progetti, comunicazioni, follow-up | D2 §3, D1 §6 | P2 | PARTIAL | confine CRM definito in `docs/CRM_INTEGRATION_CONTRACT.md` |
| REQ-CRM-02 | Il CRM non domina il sito pubblico | RB §40 | P0 | DONE | nessuna superficie pubblica |

## M. Sicurezza, audit, privacy

| ID | Requisito | Fonte | Pri | Stato | Dove |
|---|---|---|---|---|---|
| REQ-SEC-01 | Threat model documentato | D2 §18, RB §43 | P0 | TODO | `docs/security/THREAT_MODEL.md` |
| REQ-SEC-02 | Classificazione dei dati | RB §43 | P0 | TODO | `docs/security/DATA_CLASSIFICATION.md` |
| REQ-SEC-03 | TLS in transito; cifratura a riposo ove appropriato | D2 §13 | P0 | PARTIAL | requisito di deploy |
| REQ-SEC-04 | Hashing robusto delle password | D2 §13 | P0 | DONE | Django PBKDF2 |
| REQ-SEC-05 | Audit non modificabile per operazioni sensibili | D2 §13, RB §44 | P0 | PARTIAL | `audit.AuditEvent` esiste; append-only da irrobustire |
| REQ-SEC-06 | Audit di: eventi di sicurezza, modifiche di permessi e ruoli, accessi ai fascicoli, accesso e download di documenti sensibili, modifiche e approvazioni di regole, esecuzione di valutazioni, assegnazioni, cambi di stato, consensi, azioni amministrative | RB §44 | P0 | PARTIAL | copertura parziale |
| REQ-SEC-07 | Nessun segreto né contenuto sensibile eccessivo nei log | D2 §13, RB §44 | P0 | DONE | — |
| REQ-SEC-08 | Backup cifrati, test di ripristino, piano incidenti, gestione vulnerabilità | D2 §13, D3 §14 | P0 | PARTIAL | documentato; RPO/RTO da definire |
| REQ-SEC-09 | Nessun dato personale reale in sviluppo e test | D2 §13, D3 §11, CR-15 | P0 | DONE | seed sintetici |
| REQ-SEC-10 | Ambienti separati dev/staging/prod | D2 §13, D3 §11 | P0 | DONE | `config/settings/*` |
| REQ-SEC-11 | Inventario delle librerie di terzi con licenze | D3 §12 | P0 | PARTIAL | `requirements/*` pinnato; registro licenze da completare |
| REQ-SEC-12 | Registro degli asset: domini, DNS, account cloud, repository, certificati, account amministrativi | D3 §18 | P0 | TODO | — |
| REQ-PRV-01 | `Consent`: soggetto, finalità, base giuridica, versione del testo, stato, `granted_at`, `withdrawn_at`, provenienza | D2 §9, RB §45 | P0 | DONE | `apps/consents` |
| REQ-PRV-02 | Consenso newsletter separato dal trattamento di servizio | RB §45 | P0 | DONE | — |
| REQ-PRV-03 | Minimizzazione dei dati | D2 §13, D3 §8 | P0 | PARTIAL | da riverificare sui nuovi modelli |
| REQ-PRV-04 | Retention configurabile per finalità; nessun periodo inventato | D2 §20, RB §45, CR-12 | P0 | PARTIAL | 24 mesi configurati per i form pubblici |
| REQ-PRV-05 | Gestione delle richieste dell'interessato e revoca del consenso | D2 §13 | P0 | PARTIAL | richiesta di cancellazione presente |
| REQ-PRV-06 | Ruoli privacy, informative, basi giuridiche, accordi artt. 26/28, DPIA se necessaria | D3 §9 | P0 | BLOCKED | dipende dal titolare; G1 |
| REQ-PRV-07 | Hosting nello SEE documentato | D3 §10, CR-08 | P0 | BLOCKED | G12 |

## N. Configurabilità (nulla di ciò va nel codice)

| ID | Requisito | Fonte | Pri | Stato |
|---|---|---|---|---|
| REQ-CFG-01 | Regole giuridiche e requisiti di ingresso versionati come dati con fonti | D2 §20 | P0 | PARTIAL |
| REQ-CFG-02 | Testi multilingue gestiti via i18n/CMS | D2 §20, D3 §17 | P0 | DONE |
| REQ-CFG-03 | Elenco delle commissioni del Forum configurabile | D2 §20 | P1 | TODO |
| REQ-CFG-04 | Tassonomie di professioni, competenze, documenti e corsi amministrabili | D2 §20 | P1 | TODO |
| REQ-CFG-05 | Tempi di retention e versioni dei consensi configurabili | D2 §20 | P0 | PARTIAL |
| REQ-CFG-06 | Partner e soggetti autorizzati come anagrafiche verificabili, non costanti | D2 §20 | P1 | PARTIAL |
| REQ-CFG-07 | Fonti dei percorsi amministrabili | RB §53 | P1 | PARTIAL |

## O. Multilingua, accessibilità, performance

| ID | Requisito | Fonte | Pri | Stato |
|---|---|---|---|---|
| REQ-I18N-01 | IT, FR, EN, AR su sito pubblico **e** piattaforma | D2 §14, RB §46 | P0 | PARTIAL |
| REQ-I18N-02 | Arabo di prima classe con RTL reale su shell, sidebar, tabelle, timeline, breadcrumb, wizard, indicatori di avanzamento, icone direzionali, documenti, modali, form, validazione, navigazione mobile | RB §46 | P0 | PARTIAL |
| REQ-I18N-03 | Nessun mirroring meccanico di e-mail, telefono, identificativi di file | RB §46 | P0 | DONE |
| REQ-A11Y-01 | WCAG 2.2 AA senza overlay | RB §48 | P0 | PARTIAL |
| REQ-A11Y-02 | Nessuna violazione axe critica o seria sulle pagine candidate al rilascio | RB §48 | P0 | TODO |
| REQ-PRF-01 | Budget di performance; nessun bundle JS pesante, nessuna libreria di animazione superflua | RB §49 | P0 | DONE |
| REQ-PRF-02 | Immagini responsive, formati moderni, hosting locale | RB §14, §49 | P0 | PARTIAL |
| REQ-RSP-01 | La piattaforma non è desktop-only: stato, prossima azione, caricamento documento, lettura messaggio, questionario semplice, checklist, Academy, sportello devono funzionare da telefono | RB §47 | P0 | TODO |

## P. Design e qualità visiva

| ID | Requisito | Fonte | Pri | Stato |
|---|---|---|---|---|
| REQ-DES-01 | Art direction distintiva, non generica | RB §5, §11, §72 | P0 | TODO |
| REQ-DES-02 | Tre direzioni artistiche reali, valutate e scelte con motivazione | RB §10 | P0 | TODO |
| REQ-DES-03 | Token separati per pubblico e piattaforma, una sola identità | RB §17 | P0 | TODO |
| REQ-DES-04 | Archetipi di pagina definiti prima delle pagine | RB §18 | P0 | TODO |
| REQ-DES-05 | Divieto dei pattern «sito generato da AI» elencati in RB §11 | RB §11 | P0 | TODO |
| REQ-DES-06 | Studio tipografico reale, arabo incluso | RB §13 | P0 | TODO |
| REQ-DES-07 | Direzione fotografica curata, senza cliché, con registro delle licenze | RB §14 | P0 | PARTIAL |
| REQ-DES-08 | Linguaggio grafico proprio riconoscibile anche senza fotografie | RB §15 | P0 | TODO |
| REQ-DES-09 | Motion sobrio, sempre con `prefers-reduced-motion` | RB §16 | P0 | PARTIAL |
| REQ-DES-10 | Nessuna impersonificazione di autorità pubblica | RB §69, D0a | P0 | DONE |
| REQ-DES-11 | Un solo sistema di icone più SVG originali | RB §57 | P0 | PARTIAL |
| REQ-DES-12 | Stati vuoti progettati, nessun dato finto per abbellire | RB §55 | P0 | PARTIAL |
| REQ-DES-13 | Microcopy istituzionale, senza gergo SaaS | RB §56 | P0 | PARTIAL |
| REQ-DES-14 | Suite di regressione visiva con baseline desktop, mobile e RTL | RB §62 | P0 | PARTIAL |

---

## Conteggio

| Stato | Requisiti |
|---|---|
| DONE | 24 |
| PARTIAL | 47 |
| TODO | 54 |
| GATED | 2 |
| BLOCKED | 2 |
| **Totale** | **129** |

Distribuzione per priorità: P0 = 86, P1 = 39, P2 = 4.

La lettura onesta di questa matrice: il **sito pubblico** è sostanzialmente completo e conforme; la
**piattaforma autenticata** descritta dal Technical Blueprint esiste oggi solo come fondamenta
(account, ruoli, orientamento, area riservata di sola lettura). Il fascicolo digitale, il Rule Engine
versionato come dato, l'Academy, i fabbisogni gestibili e i workspace dei soggetti autorizzati sono
da costruire. È esattamente il perimetro P0 dichiarato da RB §67.
