# Privacy by design — Italy Legal Entry™

Aggiornato al 2026-09-17. Titolare del trattamento (dai testi legali, Annexe 1 §1): **AGAMI — Dialogo
Giuridico Interculturale APS**, contatto `contact@agamieuromed.org`. Le durate, le basi giuridiche e le
finalità riportate qui sono **quelle dei testi legali trasmessi** (traduzione di cortesia FR, versione ufficiale
IT non ancora disponibile): il team tecnico non ne ha inventata alcuna.

## 1. Inventario dei dati per modello e finalità

| Trattamento | Modello | Dati raccolti (minimizzati) | Base giuridica (Annexe 1 §3) | Metadati tecnici |
|---|---|---|---|---|
| Recueil des besoins (imprese) | `enquiries.CompanyNeedsRequest` | i 14 campi prescritti (ragione sociale, settore, sede, nome e funzione del referente, e-mail, telefono, profili, numero indicativo, qualifiche, esperienza, esigenze linguistiche, bisogni formativi, calendario, note) | misure precontrattuali su richiesta dell'interessato, art. 6(1)(b) | consenso (FK), lingua, `ip_hash`, user agent troncato, hash duplicati |
| Proposte di collaborazione (istituzioni / università) | `enquiries.CollaborationProposal` | organismo, tipo, referente, e-mail, telefono, paese, testo della proposta | art. 6(1)(b) | idem |
| Richiesta di contatto | `enquiries.ContactRequest` | nome, e-mail, oggetto, messaggio | art. 6(1)(b) | idem |
| Iscrizione al Forum | `forum.ForumRegistration` | prénom, nom, organisme/entreprise, fonction, e-mail, téléphone, pays, catégorie, secteur d'intérêt | art. 6(1)(b) («inscriptions aux événements») | consenso, stato, lingua, `ip_hash` |
| Newsletter | `consents.NewsletterSubscription` | e-mail, lingua | **consenso** espresso e revocabile, art. 6(1)(a) | consenso separato, token di conferma/disiscrizione, timestamp |
| Account / area riservata | `accounts.User`, `PersonProfile`, `Organisation`, `Membership` | e-mail, nome, lingua, tipo di account; profilo: paese di residenza, telefono (facoltativi) | art. 6(1)(b) (servizio richiesto) | accettazione condizioni (`terms_accepted_at`, `terms_consent`), audit |
| Orientamento | `orientation.OrientationSession`, `OrientationResult` | risposte al questionario (obiettivo del percorso, livello linguistico, titoli — come elencato in Annexe 1 §2), esito informativo | art. 6(1)(b) («demandes d'orientation») | versione ruleset, versione disclaimer, timestamp, `ip_hash`, token di ripresa |
| Documenti privati | `documents.PrivateDocument` | file caricato dall'utente (PDF/JPG/PNG), descrizione | art. 6(1)(b) | hash, stato scansione, audit download |
| Forum Virtuale | `community.Membership`, `Post`, … | categoria, organizzazione, contenuti pubblicati; nome/organizzazione visibili ad altri **solo** con opt-in (`show_name`, `show_organisation` default False) | art. 6(1)(b) + accettazione condizioni | consenso `COMMUNITY`, moderazione |
| Sicurezza del sito | `audit.AuditEvent`, throttle in cache, log | `ip_hash`, `request_id`, azione | interesse legittimo del titolare, art. 6(1)(f) | nessun IP in chiaro |
| Obblighi di legge | conservazione registrazioni di consenso, audit | — | art. 6(1)(c) | — |

**Nessun processo decisionale automatizzato con effetti giuridici (art. 22 RGPD)**: i risultati
dell'orientamento sono pre-valutazioni a carattere esclusivamente informativo (Annexe 1 §4); ogni decisione
amministrativa spetta alle autorità pubbliche. Il template dei risultati lo dichiara e salva la versione del
disclaimer mostrata.

## 2. Scelte di minimizzazione

- I form raccolgono **solo** i campi prescritti dal documento (ordine e etichette fissi); nessun campo
  facoltativo aggiunto "per completezza".
- Nessun IP in chiaro: `core.privacy.hash_ip` (SHA-256 salato, troncato). User agent troncato a 160 caratteri.
- Nessun cookie di terzi, nessun analytics, nessun pixel, nessuna risorsa esterna (CSP `self`-only): nessun
  trasferimento di IP a fornitori terzi durante la navigazione (miglioramento rispetto al sito attuale, che
  hotlinka Google Fonts e Unsplash e carica uno script marketing).
- I campi liberi mostrano l'invito a non inserire categorie particolari di dati (art. 9): stringa UI da
  aggiungere nei template dei form (Stage 1) — il testo legale lo prevede (Annexe 1 §2).
- Payload verso il CRM (integrazioni): solo id, timestamp e categoria; nessun dato personale nell'evento
  (`docs/CRM_INTEGRATION_CONTRACT.md`).
- Log senza dati personali.

## 3. Consenso versionato

`apps/consents/models.py`:

- `ConsentText(purpose, version, language, text, locked_key, effective_from, is_current)`: ogni modifica del
  testo crea una **nuova versione**; i testi prescritti (`p1.companies.form.consent`,
  `p2.forum.registration.consent`, `p3.news.newsletter_consent`) sono read-only in admin.
- `ConsentRecord(purpose, consent_text, email, user, given_at, ip_hash, user_agent, language, withdrawn_at,
  withdrawal_note)`: prova del consenso che punta alla versione effettivamente mostrata.
- La revoca (`consents.services.withdraw`) non cancella la prova; l'azione admin «Registra la revoca» è
  disponibile per ogni record.
- Newsletter: consenso **separato**, mai preselezionato, double opt-in (`confirm_token`) e disiscrizione con
  link (`unsubscribe_token`), revoca registrata.
- Finalità senza testo prescritto (proposte di collaborazione, contatto, orientamento): riuso del testo §1.1
  («… pour le suivi de la présente demande»), segnalato `CONTENT_PENDING_LEGAL_REVIEW` in
  `docs/CONTENT_SOURCE_MAP.md` per conferma dell'Avv. Badrane.

## 4. Conservazione

Dai testi legali (Annexe 1 §7), unica fonte ammessa:

| Categoria | Durata | Strumento |
|---|---|---|
| Dati raccolti tramite i form | il tempo necessario a rispondere e comunque **non oltre 24 mesi dall'ultimo contatto**, salvi obblighi legali e tutela dei diritti del titolare | `settings.ILE["RETENTION_MONTHS_FORMS"] = 24`; comandi `purge_expired_submissions` (enquiries) e purge documenti/sessioni (dry-run per default) |
| Dati di navigazione | solo per le durate tecniche strettamente necessarie | throttle in cache con TTL; log ruotati dal prestatore di hosting |

Nessun'altra durata è stata inventata. Ogni comando di purge esegue prima un **dry-run** e registra un evento di
audit quando applicato.

## 5. Esercizio dei diritti (art. 15–22)

Canale: `contact@agamieuromed.org` (Annexe 1 §8). Flusso operativo nel back-office:

| Diritto | Strumento |
|---|---|
| Accesso / portabilità | azione admin «export single submission JSON» (enquiries), export CSV per categoria, `accounts:export_data` per l'utente autenticato (solo i propri dati) |
| Rettifica | modifica nel back-office con audit (`LogEntry` → `AuditEvent`) |
| Cancellazione | azioni «anonimizza» (sostituzione dei campi personali con `[anonimizzato]`, prova del consenso conservata), `accounts.services.anonymise_user` (disattiva, anonimizza, revoca consensi) |
| Opposizione / revoca | «Registra la revoca del consenso», link di disiscrizione newsletter |
| Reclamo | Garante per la protezione dei dati personali (art. 77) — indicato nella Privacy Policy |

Utenti che accedono dal Regno del Marocco: si applicano, ove necessario, le tutele della legge marocchina
**09-08** (Annexe 1 §6) — nessuna implementazione tecnica aggiuntiva, ma il canale dei diritti è lo stesso.

## 6. Localizzazione e trasferimenti

- Requisito: server nell'**Unione europea**, nessun trasferimento verso paesi terzi (Annexe 1 §6). Il documento
  di implementazione §1.4 chiede conferma scritta di prestatore e localizzazione: **PENDING_CLIENT**.
  Campi `hosting_provider` / `hosting_location` in `core.SiteSettings` per registrarla.
- Nessun servizio SaaS esterno (analytics, error tracking, CDN font) è collegato: l'astrazione di error tracking
  e analytics resta disattivata (`FEATURE_FLAG_DEFAULTS["analytics"]["enabled"] = False`).
- Responsabili del trattamento (art. 28): prestatore di hosting e gestione tecnica — **placeholder**, da
  compilare con l'atto di nomina al momento del deploy.

## 7. Cookie e tracciamento

Coerente con la Cookie Policy (solo cookie tecnici):

| Cookie | Tipo | Scopo | Durata |
|---|---|---|---|
| `sessionid` | tecnico | sessione (area riservata, wizard di orientamento, messaggi) | 8 ore (`SESSION_COOKIE_AGE`), HttpOnly, SameSite=Lax, Secure in prod |
| `csrftoken` | tecnico | protezione CSRF dei form | 1 anno (default Django), HttpOnly, SameSite=Lax |
| `ile_language` | tecnico | memorizzazione della lingua scelta | default Django, SameSite=Lax |

Nessun cookie di profilazione, nessun cookie di terzi, nessun banner di consenso necessario. **Vietato**
introdurre Google Analytics, Meta Pixel, Hotjar, TikTok, embed video con cookie, mappe con cookie o lo script
Hostinger Reach senza revisione della Cookie Policy e consenso (nota operativa interna dell'Annexe 1, non
pubblicata). Lo scanner `apps/cms/forbidden.py` e i test di conformità bloccano tali inserimenti.

## 8. DPIA "leggera" — questionario di orientamento

| Aspetto | Valutazione |
|---|---|
| Natura | domande progressive su situazione generale (obiettivo, tipo di profilo, presenza di familiari, interesse alla formazione) |
| Rischio | profilazione percepita; aspettative di esito |
| Mitigazioni | nessuna decisione automatizzata (art. 22); esito etichettato «pré-évaluation à caractère informatif» con il testo bloccato `p3.persons.how_it_works`; nessuna richiesta di e-mail per usare il wizard; sessioni anonime con scadenza 30 giorni; token di ripresa segreto; accesso vincolato alla sessione/utente; nessuna categoria particolare richiesta; ruleset versionato e auditabile (versione salvata nel risultato) |
| Trasparenza | pagina di avvio con avvertenza; risultato con versione delle regole e data |

## 9. Violazioni di dati (outline)

1. Rilevazione (log/audit, segnalazione) → registrazione interna con `request_id` e periodo.
2. Contenimento (vedi `docs/SECURITY.md` §11).
3. Valutazione del rischio per gli interessati; notifica al Garante entro 72 ore se dovuta (art. 33) e agli
   interessati se rischio elevato (art. 34).
4. Registro delle violazioni (documento interno del titolare).

## 10. Checklist per gli editor del back-office

- Non inserire categorie particolari di dati (salute, opinioni, religione, ecc.) nei campi liberi e nelle note.
- Non pubblicare nomi di persone fisiche senza autorizzazione (relatori, partecipanti, membri del Forum Virtuale).
- Non modificare i testi di consenso bloccati; una nuova formulazione = nuova versione approvata dal titolare.
- Usare le azioni «anonimizza» / «export» per le richieste degli interessati; annotare la data nella scheda.
- Non esportare CSV su dispositivi non gestiti; gli export contengono dati personali.
- Prima di attivare newsletter, analytics o strumenti esterni: revisione della Privacy/Cookie Policy con il titolare.
