# DATA CLASSIFICATION — Italy Legal Entry™

Versione 1.0 · 20 settembre 2026 · Requisito: **REQ-SEC-02**
Titolare del trattamento: **AGAMI — Dialogo Giuridico Interculturale APS** · contatto `contact@agamieuromed.org`
Owner del documento: referente tecnico · Revisione: a ogni nuovo modello che contenga dati di persone

Documenti correlati: `docs/PRIVACY_BY_DESIGN.md` (inventario per finalità e base giuridica) ·
`docs/source-of-truth/CONFIDENTIALITY_REGISTER.md` (classificazione delle **fonti documentali**) ·
`docs/security/THREAT_MODEL.md` · `docs/security/PERMISSION_MODEL.md` ·
`docs/security/DOCUMENT_SECURITY.md` · `docs/security/AUDIT_MODEL.md`.

> Questo documento classifica i **dati applicativi** (ciò che sta nel database, nello storage privato,
> nei log e nei backup). La classificazione dei **documenti sorgente** del committente resta in
> `CONFIDENTIALITY_REGISTER.md` e non è ripetuta qui.


> **Nota sulle citazioni dell'app `cases`.** I numeri di riga di `apps/cases/*` si riferiscono
> allo stato del **20 settembre 2026**: l'app è stata aggiunta a `INSTALLED_APPS`
> (`config/settings/base.py:67`) nella stessa giornata ed era in costruzione attiva. Le righe
> vanno riverificate alla prima revisione; i simboli citati (`readable_by`, `is_live`,
> `case_detail`, `record_assessment`, `reproduce`) sono il riferimento stabile.

---

## 1. Livelli

| Livello | Sigla | Definizione operativa | Se esce |
|---|---|---|---|
| **Pubblico** | `PUB` | Destinato alla pubblicazione; già leggibile da chiunque sul sito | Nessun danno |
| **Interno** | `INT` | Serve al funzionamento o alla governance; non pubblicabile ma non riferito a una persona identificabile | Danno reputazionale o vantaggio a un attaccante |
| **Confidenziale** | `CONF` | Segreti tecnici, materiale di governo del sistema, contenuti non ancora pubblicati | Compromissione del sistema o della strategia di tutela |
| **Dato personale** | `PD` | Qualunque informazione relativa a una persona fisica identificata o identificabile (art. 4(1) GDPR) | Violazione di dati: valutazione artt. 33-34 |
| **Categoria particolare** | `PD-9` | Dati dell'art. 9 GDPR (salute, religione o convinzioni, opinioni politiche, appartenenza sindacale, vita o orientamento sessuale, dati genetici, dati biometrici identificativi, origine razziale o etnica) | Rischio elevato: DPIA obbligatoria, notifica quasi certa |

**Oggi la piattaforma non raccoglie alcun dato di categoria particolare.** Vedi §5: è una scelta di
progetto, non un caso, ed è a un passo dall'essere violata da un campo libero mal governato.

Corrispondenza con il registro di riservatezza delle fonti (`CONFIDENTIALITY_REGISTER.md` §1):

| Registro fonti | Qui |
|---|---|
| **P** pubblico | `PUB` |
| **I** interno | `INT` |
| **R** riservato | `CONF` |
| **R+PD** riservato con dati personali | `CONF` + `PD` |

### 1.1 Regole per livello

| Regola | `PUB` | `INT` | `CONF` | `PD` | `PD-9` |
|---|---|---|---|---|---|
| Può comparire in una pagina pubblica | sì | no | no | no | no |
| Può comparire in un log applicativo | sì | identificatori | **mai** | **mai** (nemmeno l'e-mail) | **mai** |
| Può comparire in una pagina di errore | sì | no | no | no | no |
| Può comparire in analytics | — (non esistono) | no | no | no | no |
| Può comparire in fixture, seed, test | sì | sì (sintetico) | **mai** | **mai** — solo sintetico (**CR-15**) | **mai** |
| Presente nei backup | sì | sì | sì, cifrato | sì, cifrato | n/a |
| Cifratura a riposo richiesta | no | no | **sì** | **sì** (volume/DB) | **sì** (campo) |
| Serve una base giuridica | no | no | no | **sì** | **sì** + condizione art. 9(2) |
| Serve una durata di conservazione | no | sì | sì | **sì** | **sì** |
| Esportabile su richiesta dell'interessato | — | — | — | **sì** (artt. 15/20) | sì |

**Cifratura a riposo — decisione.** Non è implementata a livello applicativo e **non deve essere
dichiarata come esistente**. La decisione è: cifratura a livello di volume (database e storage
privato) fornita dall'hosting, da attestare per iscritto prima del deploy insieme alla localizzazione
SEE (**CR-08**, gate G12, REQ-SEC-03). La cifratura per singolo campo è prevista **solo** se e quando
un dato `PD-9` dovesse essere introdotto (§5), e in tal caso con gestione di chiave separata.

---

## 2. Inventario — dati pubblici e interni

| ID | Categoria | Dove vive | Livello | Legge | Scrive | Conservazione |
|---|---|---|---|---|---|---|
| C-01 | Contenuti editoriali (pagine, sezioni home, attualità, FAQ, glossario, «vivere in Italia», partner, percorsi) | `pages`, `news`, `faq`, `glossary`, `living`, `partners`, `pathways`, `ecosystem` + tabelle `*Translation` | `PUB` | chiunque | `role:staff`, `role:administrator` | permanente, con versioni di pubblicazione |
| C-02 | Testi prescritti e bloccati | `apps/cms/locked_content.py` + checksum `locked_content.sha256.json` | `PUB` | chiunque | **nessuno a runtime** (solo modifica di codice, con test) | permanente |
| C-03 | Testi legali (privacy, cookie, condizioni, note legali) | `legal.LegalDocument`, `legal.LegalDocumentVersion` | `PUB` una volta pubblicati, `INT` finché `BLOCKED` | chiunque (se pubblicati) | `role:administrator` + audit `legal.published` | permanente, versionato |
| C-04 | Programma, partner, esiti e documenti del Forum | `forum.ForumEvent`, `ForumProgramItem`, `ForumPartner`, `ForumMedia`, `ForumDocument`, `ForumAgreement`, `ForumOutcome` | `PUB` | chiunque | `role:staff`/`administrator` | permanente |
| C-05 | Libreria immagini e licenze | `cms.MediaAsset` (file sotto `MEDIA_ROOT`) | `PUB` | chiunque | `role:staff`/`administrator` | permanente |
| C-06 | Navigazione, banner, redirect | `cms.MenuItem`, `SiteBanner`, `HomeHero`, `Redirect` | `PUB` | chiunque | `role:staff`/`administrator` | permanente |
| C-07 | Impostazioni di sito | `core.SiteSettings` (compresi `hosting_provider`, `hosting_location`) | `INT` | back-office | `role:administrator` | permanente |
| C-08 | Feature flag e gate | `core.FeatureFlag` + `FEATURE_FLAG_DEFAULTS` `config/settings/base.py` | `INT` | back-office | `role:administrator`, audit `feature_flag.changed` | permanente |
| C-09 | **Regole di orientamento** (ruleset, domande, scelte, esiti, checklist, regole) | `orientation.Ruleset`, `Question`, `Choice`, `Outcome`, `ChecklistItem`, `Rule` + traduzioni | `INT` (la **logica** non è pubblicabile: `CONFIDENTIAL_MATERIAL_POLICY.md` §4) | esito reso pubblico in forma di testo; la condizione no | oggi `role:administrator`; domani `LEGAL_RULE_EDITOR` con quattro occhi | permanente, versionato, mai cancellato |
| C-10 | Anagrafica dei sistemi esterni e degli endpoint | `integrations.ExternalSystem`, `WebhookEndpoint`, `ExternalReference` | `INT` | `role:administrator` (view) | superadmin | durata dell'accordo |
| C-11 | Log dei webhook in ingresso | `integrations.InboundWebhookLog` (payload dichiarato «solo identificativi») | `INT` | `role:administrator` | sistema | da definire con la policy dei log |
| C-12 | Eventi in uscita verso il CRM | `integrations.OutboundEvent.payload` — solo id, timestamp, categoria (`docs/CRM_INTEGRATION_CONTRACT.md`) | `INT` | `role:administrator` | sistema | fino all'ack + finestra tecnica |

---

## 3. Inventario — dati personali (`PD`)

«Legge» indica il perimetro **previsto**; ciò che è davvero applicato è in
`docs/security/PERMISSION_MODEL.md`. Stato: **IMPL** = il modello esiste e la regola è applicata ·
**PARZ** = il modello esiste, la regola non copre tutto · **DESIGN** = il modello non esiste ancora.

| ID | Categoria | Modello / campi | Livello | Legge | Scrive | Conservazione | Stato |
|---|---|---|---|---|---|---|---|
| P-01 | **Account** | `accounts.User`: `email`, `full_name`, `preferred_language`, `account_type`, `date_joined`, `last_login`, `terms_accepted_at` | `PD` | l'interessato; `role:administrator` (back-office) | l'interessato (profilo); admin | fino alla cancellazione dell'account → anonimizzazione immediata `apps/accounts/services.py:178-236` | IMPL |
| P-02 | **Credenziali** | `User.password` (PBKDF2, Argon2 disponibile `config/settings/base.py:194-197`) | `CONF`+`PD` | **nessuno** (hash non reversibile) | l'interessato | come P-01 | IMPL |
| P-03 | **Secondo fattore** | `allauth.mfa.Authenticator` (segreto TOTP, codici di recupero) | `CONF`+`PD` | **nessuno** | l'interessato | come P-01; cancellato all'anonimizzazione `services.py:211` | IMPL |
| P-04 | **Profilo persona** | `accounts.PersonProfile`: `country_of_residence`, `phone` | `PD` | l'interessato; admin | l'interessato | come P-01 | IMPL |
| P-05 | **Appartenenza a un'organizzazione** | `accounts.Membership`, `accounts.Organisation` | `PD` (il legame persona-organizzazione) | membri dell'organizzazione; admin | admin, creazione | come P-01 | IMPL |
| P-06 | **Prove di consenso** | `consents.ConsentRecord`: `email`, `user`, `given_at`, `ip_hash`, `user_agent`, `language`, `withdrawn_at` | `PD` | l'interessato (nel proprio export); `role:staff` (view), `role:administrator` | sistema alla raccolta; revoca registrata, **mai cancellata** | conservata come prova anche dopo la revoca; e-mail sostituita all'anonimizzazione `services.py:194-199` | IMPL |
| P-07 | **Iscrizione newsletter** | `consents.NewsletterSubscription`: `email`, token di conferma e disiscrizione | `PD` | l'interessato; admin | l'interessato (double opt-in) | fino alla disiscrizione + prova del consenso | IMPL (flag `newsletter` chiuso) |
| P-08 | **Richieste dai form pubblici** | `enquiries.CompanyNeedsRequest` (14 campi prescritti), `CollaborationProposal`, `ContactRequest` + base `PublicSubmission` (`ip_hash`, `user_agent`, `source_path`, `admin_notes`) | `PD` | `role:staff`, `role:administrator`; l'interessato autenticato solo per le proprie `apps/enquiries/policies.py:18-21` | pubblico (invio); staff (stato, note) | **24 mesi dall'ultimo contatto** (§6) | IMPL |
| P-09 | **Iscrizioni al Forum** | `forum.ForumRegistration`: nome, cognome, organismo, funzione, e-mail, telefono, paese, categoria, settore d'interesse, `admin_notes`, `ip_hash` | `PD` | `role:staff`/`administrator`; l'iscritto per la propria `apps/forum/permissions.py:10-21` | pubblico (invio); staff (stato) | 24 mesi (§6); anonimizzazione disponibile | IMPL |
| P-10 | **Sessioni di orientamento** | `orientation.OrientationSession`: `state.answers` (chiavi di scelta), `language`, `ip_hash`, `resume_token_hash` | `PD` se legata a un account; pseudonima se anonima | il browser di origine, l'utente proprietario, o chi ha il token `apps/orientation/services.py:266-276` | l'interessato | anonime: 30 giorni (`ANONYMOUS_SESSION_TTL_DAYS`); legate a un account: come P-01 | IMPL |
| P-11 | **Esiti di orientamento** | `orientation.OrientationResult`: `answers_snapshot`, `ruleset_version`, `disclaimer_version` | `PD` | come P-10 `apps/orientation/policies.py:16-18` | sistema (immutabile) | come la sessione | IMPL |
| P-12 | **Documenti privati — metadati** | `documents.PrivateDocument`: `original_name`, `kind`, `size`, `sha256`, `scan_status`, `description`, `uploaded_ip_hash` | `PD` | proprietario; responsabile dell'organizzazione; `role:staff`/`administrator` `apps/documents/policies.py:26-38` | proprietario | `retention_until` per riga; purge con tombstone `services.py:304-333` | IMPL |
| P-13 | **Documenti privati — contenuto** | File sotto `PRIVATE_MEDIA_ROOT` (PDF/JPEG/PNG) | `PD`, **potenzialmente `PD-9` per contenuto** (§5.3) | solo via `documents:download` con autorizzazione `apps/documents/views.py:97-115` | proprietario | come P-12; file rimosso, riga conservata | IMPL |
| P-14 | **Messaggi dell'area riservata** | `portal.Message`: `subject`, `body` (testo semplice), destinatario, mittente | `PD` | destinatario `apps/portal/services.py:112-118`; staff via back-office | staff / sistema | da definire con il titolare (§6, aperto) | IMPL |
| P-15 | **Scadenze personali** | `portal.Deadline`: `title`, `description`, `due_on`, proprietario | `PD` | proprietario; staff | staff / sistema | da definire (§6, aperto) | IMPL |
| P-16 | **Forum Virtuale — partecipante** | `community.Membership`: categoria, organizzazione, `show_name`/`show_organisation` (default **False**), `trusted`, stato | `PD` | moderazione; gli altri membri **solo** se l'opt-in è attivo | l'interessato; moderazione | durata della partecipazione | IMPL (dietro flag) |
| P-17 | **Forum Virtuale — contenuti** | `community.Discussion`, `Post`, `Report`, `ModerationAction`, `Attachment` | `PD` (l'autore è identificabile per i membri) | membri della stanza `apps/community/policies.py:56-100` | l'autore; moderazione | durata della partecipazione | IMPL (dietro flag) |
| P-18 | **Coda e-mail** | `notifications.EmailOutbox`: `to_email`, `subject`, `body_text`, `body_html` — **contiene il contenuto dei form** | `PD` | `role:staff` (view), `role:administrator` | sistema | **lacuna: nessuna purga automatica** (§6) | IMPL |
| P-19 | **Traccia di audit** | `audit.AuditEvent`: `actor`, `actor_label` (= e-mail), `target_repr`, `metadata`, `ip_hash`, `request_id` | `PD` (pseudonimo dopo l'anonimizzazione) | `role:administrator` (sola lettura) `apps/audit/admin.py:13-22` | solo il sistema, in append | vedi `AUDIT_MODEL.md` §6 | IMPL |
| P-20 | **Log applicativi** | stdout → raccolta dell'hosting, formato JSON `apps/core/logging.py:16-32` | **dichiarato `INT`, oggi di fatto `PD`** (§7) | operazioni tecniche | sistema | durata tecnica del prestatore | **LACUNA** |
| P-21 | **Fascicolo digitale** | `cases.CaseFile`, `ChecklistItem`, `CaseAssignment`, `PathwayAssessment` (`answers`, `ruleset_snapshot`, `missing_requirements`) | `PD`, con **rischio `PD-9` per contenuto** (§5.3) | la persona titolare; assegnatari vivi; `role:staff` (view), `role:administrator` `apps/cases/policies.py:49-68` | la persona (limitatamente); assegnatari; servizi di dominio | da definire con il titolare (§6, aperto) | PARZ — app installata il 20/09/2026, nessuna vista, regole da esercitare |
| P-22 | **Processo di selezione** | `SelectionProcess`, `AuthorizedActor` | `PD` | solo l'attore autorizzato assegnato e le parti previste da CR-04 | attore autorizzato | da definire | DESIGN |
| P-23 | **Formazione** | `Course`, `Enrollment`, `TrainingPlan` | `PD` | la persona; l'ente formativo **solo** per i dati della formazione assegnata | ente formativo | da definire | DESIGN |
| P-24 | **Sportello digitale** | richieste di assistenza e risposte | `PD`, alto rischio di `PD-9` in testo libero (§5.3) | la persona; il professionista assegnato | entrambi | da definire | DESIGN |
| P-25 | **Chiavi API** | `integrations.ApiKey`: `key_hash` (mai il segreto), `prefix`, `created_by` | `CONF` | `role:administrator` (view) | superadmin, mostrata una sola volta | fino a revoca/scadenza | IMPL |
| P-26 | **Segreti di ambiente** | `DJANGO_SECRET_KEY`, `IP_HASH_SALT`, `DATABASE_URL`, `EMAIL_HOST_PASSWORD`, segreti dei webhook | `CONF` | nessuno (solo il processo) | operazioni | rotazione secondo `docs/SECURITY.md` §8 | IMPL |

### 3.1 Dati tecnici che sembrano innocui e non lo sono

| Dato | Perché è un dato personale | Trattamento adottato |
|---|---|---|
| Indirizzo IP | Identificatore online (considerando 30 GDPR) | **Mai conservato in chiaro**: `hash_ip` = SHA-256 salato troncato a 32 caratteri `apps/core/privacy.py:19-27`. Usato in `ConsentRecord`, `PublicSubmission`, `ForumRegistration`, `OrientationSession`, `PrivateDocument`, `AuditEvent` e nelle chiavi di throttle |
| User agent | Contribuisce al fingerprint | Troncato a 160 caratteri `apps/core/privacy.py:30-31` |
| `request_id` | Correla azioni della stessa richiesta | Casuale per richiesta; accettato dal client solo se alfanumerico e ≤ 64 caratteri `apps/core/middleware.py:22-23` |
| Token di ripresa dell'orientamento | Dà accesso alla sessione e alle risposte | In database **solo l'hash** con il `SECRET_KEY` `apps/orientation/services.py:200`; confronto a tempo costante `:275` |
| `CaseFile.reference` | Riferimento leggibile del fascicolo | Non deve essere usato come chiave d'accesso né essere indovinabile (vedi T-26) |

---

## 4. Chi legge, chi scrive — sintesi per ruolo

Il dettaglio è in `PERMISSION_MODEL.md`. Qui la regola di classificazione:

| Ruolo | `PUB` | `INT` | `CONF` | `PD` |
|---|---|---|---|---|
| Visitatore anonimo | lettura | — | — | — |
| Persona | lettura | — | — | **solo i propri** |
| Impresa | lettura | i propri fabbisogni | — | i propri dati; dati di persone **solo** via CR-04 (oggi: zero) |
| Soggetto autorizzato | lettura | — | — | solo le pratiche assegnate, entro il mandato valido |
| Professionista | lettura | — | — | solo i fascicoli assegnati |
| Ente formativo | lettura | — | — | solo i dati di formazione assegnati |
| Istituzione | lettura | indicatori aggregati | — | nessuno fuori dal perimetro di convenzione |
| Università | lettura | programmi, progetti | — | **nessun fascicolo privato** |
| Moderazione | lettura | contenuti segnalati | — | dati del Forum Virtuale, per la moderazione |
| Redattore di contenuti | lettura | scrittura editoriale | — | **nessuno** (oggi non è vero: vedi T-06) |
| Legal/Rule Editor | lettura | regole e fonti | — | **nessuno** |
| Operatore | lettura | lavorazione assegnata | — | solo il perimetro assegnato |
| Amministratore | lettura | scrittura | configurazione | accesso amministrativo tracciato |

---

## 5. Categorie particolari (art. 9 GDPR)

### 5.1 Stato attuale: nessuna

**Nessun campo del modello dati raccoglie oggi dati di categoria particolare.** Verificato campo per
campo sull'inventario §2-§3. In particolare:

- il questionario di orientamento pone **cinque** domande — `objective`, `work_profile`,
  `study_type`, `family_member_status`, `training_interest` (`apps/orientation/seeds.py:62-130`) —
  e nessuna riguarda salute, religione, opinioni, sindacato, origine etnica o dati biometrici;
- i form pubblici raccolgono solo i campi prescritti dai testi legali
  (`docs/PRIVACY_BY_DESIGN.md` §1); nessun campo è stato aggiunto «per completezza»;
- il profilo persona è volutamente minimo: paese di residenza e telefono, entrambi facoltativi
  (`apps/accounts/models.py:134-140`).

### 5.2 Nazionalità e paese di origine

**Non sono dati dell'art. 9.** Non lo sono nemmeno il paese di residenza, la cittadinanza, la lingua
madre o lo stato familiare. Vanno però trattati come **sensibili nel contesto**: in un sistema di
mobilità, la combinazione «nazionalità + stato del fascicolo + datore di lavoro + scadenza del
permesso» descrive una situazione che espone la persona a discriminazione e, in casi limite, a
pericolo. Conseguenze operative:

- questi campi non compaiono mai in una pagina pubblica, in una notifica, in un oggetto di e-mail,
  in un log o in un export non necessario;
- non si usano come criterio di filtro in interfacce di ricerca accessibili a ruoli diversi dalla
  persona interessata;
- gli aggregati per istituzioni si pubblicano solo con soglia minima di numerosità (mai valori che
  permettano di re-identificare una persona).

> **Attenzione**: l'origine **razziale o etnica** è invece dell'art. 9. Un campo «etnia», «gruppo di
> appartenenza» o una foto usata per inferirla trasformerebbe il trattamento. Non si aggiunge.

### 5.3 Dove il rischio art. 9 entrerebbe davvero

| Vettore | Che cosa creerebbe | Regola |
|---|---|---|
| Campo libero (`admin_notes`, `description` dei documenti, `notes` dei fabbisogni, messaggi, post del Forum, sportello digitale) | Un operatore o la persona stessa scrive «problema di salute», «motivi religiosi», «iscritto al sindacato» | Avviso accanto a ogni campo libero (previsto da Annexe 1 §2, **da completare nei template**); formazione degli editor (`docs/PRIVACY_BY_DESIGN.md` §10); nessuna indicizzazione full-text di questi campi |
| **Documento caricato** | Un certificato medico, un attestato di ente religioso, un certificato di matrimonio con dati sensibili | È il rischio più concreto: il contenuto del file non è ispezionato. Mitigazione: tipi di documento **espliciti** (`DocumentKind`), nessun tipo che implichi salute, e istruzione chiara a non caricare certificati sanitari |
| Motivo di sospensione / revisione | «Sospeso per ricovero» | Motivi da **elenco chiuso**, mai testo libero, su `CaseFile.suspension_reason` |
| Regole del rule engine | Una condizione «se ha una disabilità allora…» | Una condizione del genere richiede una base giuridica art. 9(2) e una DPIA: vietata senza decisione formale del titolare |
| Ricongiungimento familiare | Relazioni familiari e, indirettamente, orientamento sessuale (coniuge dello stesso sesso) | Nessun campo che qualifichi la relazione oltre il necessario; mai usato come criterio di segmentazione |
| Motivi di protezione | Asilo, protezione internazionale: implicano opinioni politiche o origine etnica | **Fuori perimetro**: la piattaforma riguarda la mobilità regolare. Se entrasse, servono DPIA e riprogettazione |

### 5.4 Se un dato `PD-9` dovesse essere introdotto

Condizioni cumulative, nessuna negoziabile:

1. decisione scritta del titolare con individuazione della condizione dell'art. 9(2);
2. **DPIA** (art. 35) prima di scrivere il codice;
3. minimizzazione estrema: nessuna copia, nessun indice, nessun export di massa;
4. cifratura a livello di campo con chiave separata dal database;
5. autorizzazione dedicata (non basta il ruolo: serve l'assegnazione puntuale) e **audit di ogni
   lettura**, non solo di ogni scrittura;
6. retention più breve del resto del fascicolo e cancellazione verificabile;
7. aggiornamento di questo documento, del threat model e del modello dei permessi **prima** del rilascio.

---

## 6. Conservazione

### 6.1 Quel che è deciso

| Categoria | Durata | Fonte | Strumento |
|---|---|---|---|
| Dati dei form pubblici (P-08, P-09) | Il tempo necessario a rispondere e comunque **non oltre 24 mesi dall'ultimo contatto** | Testi legali Annexe 1 §7, ripresa in **CR-12** | `settings.ILE["RETENTION_MONTHS_FORMS"] = 24` `config/settings/base.py:270`; comando `purge_expired_submissions` (dry-run per difetto) `apps/enquiries/management/commands/purge_expired_submissions.py` |
| Sessioni di orientamento anonime (P-10) | 30 giorni | Decisione tecnica documentata in `PRIVACY_BY_DESIGN.md` §8 | `expires_at` + purga |
| Documenti privati (P-12, P-13) | Per riga, `retention_until`; purga dei soft-deleted | Decisione tecnica | `documents.services.purge_expired` `apps/documents/services.py:322-333` |
| Dati di navigazione (throttle, log) | Solo le durate tecniche strettamente necessarie | Annexe 1 §7 | TTL della cache; rotazione dei log presso l'hosting |
| Prove di consenso (P-06) | Conservate anche dopo la revoca, come prova | Obbligo di dimostrabilità, art. 7(1) | `consents.services.withdraw` non cancella |
| Audit (P-19) | Vedi `AUDIT_MODEL.md` §6 | — | — |

**CR-12 è rispettato nella sostanza e non nella forma.** La decisione registrata dice: «La retention
è un dato **per finalità di trattamento, amministrabile dal back-office**, con valore iniziale 24
mesi per le richieste dei form pubblici». Oggi il valore è una **costante di configurazione**
(`base.py:270`), non una riga amministrabile: REQ-PRV-04 e REQ-CFG-05 restano `PARTIAL`.

**Da costruire** (nessuna durata nuova va inventata nel frattempo): un modello
`RetentionPolicy(purpose, months, legal_basis, source, updated_by)` amministrabile, letto dai comandi
di purga; finché non esiste, l'unica durata applicata resta quella dei form pubblici.

### 6.2 Quel che è aperto — e resta aperto

Le finalità della piattaforma autenticata **non hanno una durata**: fascicolo, checklist,
assegnazioni, valutazioni, messaggi, scadenze, formazione. La regola qui è esplicita e va rispettata:

> **Non si inventano periodi di conservazione** (direttiva di rebase §45, CR-12). Finché il titolare
> non fornisce la policy, queste categorie restano **senza scadenza automatica** e sono elencate come
> questione aperta qui e in `docs/PRIVACY_BY_DESIGN.md`.

| Categoria | Perché è difficile | Chi decide |
|---|---|---|
| Fascicolo e checklist (P-21) | Un percorso migratorio dura anni; la prova di ciò che è stato detto serve anche dopo | Titolare, con parere legale |
| Valutazioni e snapshot (P-21) | Sono la prova della riproducibilità (D2 §17.2): vanno conservate almeno quanto il fascicolo | Titolare |
| Messaggi e scadenze (P-14, P-15) | Oggi senza scadenza | Titolare |
| Coda e-mail (P-18) | **Contiene il testo integrale dei form**: è una seconda copia dei dati personali senza purga | Decisione tecnica urgente: purgare il corpo dopo l'invio riuscito |
| Log applicativi (P-20) | Durata fissata dal prestatore di hosting, non ancora scelto (**CR-08**) | Operazioni + titolare |
| Forum Virtuale (P-16, P-17) | Contenuti collettivi: la cancellazione di un membro non deve distruggere la discussione | Titolare + moderazione |

---

## 7. Dove i dati **non** devono comparire

### 7.1 Nei log — regola e violazione attuale

Regola: nei log vanno **identificatori opachi**, mai etichette umane. Nessuna e-mail, nessun nome,
nessun nome di file, nessun contenuto di form, nessun segreto, nessun token, nessun IP in chiaro.

Controlli presenti: formatter a campi chiusi `apps/core/logging.py:16-32`; `hash_ip`
`apps/core/privacy.py:19-27`; nessun dato di form passato ai logger delle app.

**Violazione verificata (T-25).** `audit.services.record` scrive sul logger `ile.audit` gli extra
`actor` e `target` `apps/audit/services.py:26`; `actor_label` è `str(actor)`, cioè **l'indirizzo
e-mail** `:17`, e `target_repr` è `str(target)`, che per un documento privato è **il nome del file
caricato** (`apps/documents/models.py:97-98`). Il formatter strutturato — attivo in produzione
`config/settings/prod.py:34` — copia entrambi nel JSON `apps/core/logging.py:27-29`.

Conseguenze: l'affermazione «nessun dato personale nei log» di `docs/SECURITY.md` §9 e lo stato
`DONE` di REQ-SEC-07 **non sono esatti** e vanno corretti. Correzione tecnica: loggare `actor_id`,
`target_type`, `target_id`; lasciare le etichette umane solo nella riga di `AuditEvent`.

### 7.2 Nelle pagine di errore

Le pagine 400/403/404/429/500 sono template statici senza contesto di dominio
`apps/core/views.py:47-68`; `DEBUG=False` in produzione impedisce il traceback con le settings
`config/settings/prod.py:15`. Nessun messaggio deve rivelare l'esistenza di un oggetto (vedi T-26).

### 7.3 In analytics

**Non esistono analytics.** `FEATURE_FLAG_DEFAULTS["analytics"]["enabled"] = False`; nessuna risorsa
esterna è caricata (CSP `self`-only `config/settings/base.py:319-333`); lo scanner
`apps/cms/forbidden.py:32-43` e i test di conformità impediscono l'introduzione di Google Analytics,
Meta Pixel, Hotjar, TikTok, Hostinger Reach, Google Fonts e hotlink di immagini. Se un giorno
esisteranno: solo metriche aggregate, nessun identificatore personale, nessun trasferimento fuori
dallo SEE, revisione della Cookie Policy prima dell'attivazione.

### 7.4 In fixture, seed e test

**Nessun dato personale reale** in dev e test (**CR-15**, REQ-SEC-09). I seed sono sintetici; il test
`tests/security/test_confidential_material.py` cerca gli identificatori sentinella del pacchetto
riservato in tutto il repository; `tests/compliance/test_no_person_names.py` impedisce nomi di persone
fisiche in template, seed e cataloghi. Regola aggiuntiva: **nessun dump di produzione** in sviluppo,
nemmeno «anonimizzato in fretta»; se servisse un volume realistico, si genera.

### 7.5 Nei backup

| Regola | Stato |
|---|---|
| Backup cifrati | **DESIGN ONLY** — dipende dall'hosting (CR-08, REQ-SEC-08) |
| Localizzazione SEE | **APERTO** — gate G12 `PENDING_CLIENT` |
| Test di ripristino documentato | **DESIGN ONLY** — RPO/RTO da definire |
| I backup contengono `PD` e `CONF` | sì per definizione: stessa classificazione del dato più alto contenuto |
| La cancellazione di un interessato si propaga ai backup | **no**: si applica la prassi «il backup non si modifica, il dato ricompare solo in caso di ripristino, e in quel caso l'anonimizzazione va rieseguita». Da documentare nella procedura di ripristino |
| Accesso ai backup | Solo operazioni, nominativo, tracciato |

### 7.6 Verso l'esterno

- **Form pubblici**: unica destinazione `settings.ILE["FORMS_DESTINATION_EMAIL"]`
  (`apps/notifications/services.py:45-53`); nessun indirizzo `@legalitalentry.it` è pubblicabile.
- **CRM / integrazioni**: solo id, timestamp e categoria (`docs/CRM_INTEGRATION_CONTRACT.md`); il
  trasporto predefinito non apre socket `apps/integrations/transports.py:46-61`.
- **Nessun servizio SaaS** di analytics, error tracking, font o CDN è collegato.
- **Nessun documento riservato** del committente entra nel repository
  (`CONFIDENTIAL_MATERIAL_POLICY.md` §2).

---

## 8. Diritti degli interessati e classificazione

| Diritto | Che cosa copre | Strumento oggi |
|---|---|---|
| Accesso / portabilità (artt. 15, 20) | Tutti i `PD` dell'interessato | `accounts.services.export_user_data` — account, profilo, e-mail, appartenenze, consensi + sezioni registrate dalle app `apps/accounts/services.py:107-159`; per i documenti `documents.services.documents_export_section` `apps/documents/services.py:345-359` |
| Rettifica (art. 16) | Profilo, richieste | Profilo dall'interessato; back-office con audit |
| Cancellazione (art. 17) | Account e dati collegati | `anonymise_user` `apps/accounts/services.py:178-236`: consensi revocati, profilo e appartenenze rimossi, MFA cancellata, e-mail sostituita, password resa inutilizzabile, file privati purgati via segnale `apps/documents/receivers.py:12-15`; **le prove di consenso e le righe di audit restano, pseudonimizzate** |
| Opposizione / revoca | Consensi, newsletter | `consents.services.withdraw`; link di disiscrizione |
| Reclamo | — | Garante (art. 77), indicato nella Privacy Policy |

**Lacuna di copertura dell'export**: quando esisteranno fascicolo, checklist, valutazioni, messaggi e
scadenze, ciascuna app dovrà registrare la propria sezione con
`accounts.services.register_export_section` `apps/accounts/services.py:89-96`. Oggi `portal` e
`cases` non lo fanno: un export non è completo.

---

## 9. Questioni aperte

| # | Questione | Blocco | Chi decide |
|---|---|---|---|
| Q-01 | Durate di conservazione delle finalità della piattaforma autenticata | Nessuna durata inventata (CR-12) | Titolare |
| Q-02 | `RetentionPolicy` amministrabile per finalità | REQ-PRV-04, REQ-CFG-05 `PARTIAL` | Tecnico, su policy del titolare |
| Q-03 | Attestazione di hosting SEE e cifratura a riposo | **CR-08**, gate G12 | Committente |
| Q-04 | Purga del corpo dei messaggi in `EmailOutbox` dopo l'invio | Seconda copia dei dati dei form senza scadenza | Tecnico |
| Q-05 | Dati personali nei log strutturati | **T-25**: correzione del codice e della documentazione | Tecnico |
| Q-06 | Responsabili del trattamento (art. 28): hosting, manutenzione | `PRIVACY_BY_DESIGN.md` §6 «placeholder» | Titolare |
| Q-07 | Avviso «non inserire dati particolari» accanto a ogni campo libero | Previsto da Annexe 1 §2, non ancora nei template | Tecnico + contenuti |
| Q-08 | Soglia minima di numerosità per gli aggregati istituzionali | Rischio di re-identificazione | Titolare + tecnico |

---

Classificazione di questo documento: **interno**
(`docs/source-of-truth/CONFIDENTIALITY_REGISTER.md` §2).
