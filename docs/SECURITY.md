# Sicurezza — Italy Legal Entry™

Aggiornato al **2026-09-21**. Riferimenti al codice reale del repository. Ogni controllo elencato
qui è implementato e verificato da un test; ciò che non lo è sta nel §12, con il suo nome.

## 1. Modello delle minacce (sintesi)

| Asset | Minaccia | Controllo principale |
|---|---|---|
| Dati dei form pubblici (imprese, iscrizioni Forum, proposte, contatti) | spam, scraping, furto via IDOR, invio a destinatari errati | honeypot + throttle, policy object-level, unica destinazione e-mail configurata |
| Account e area riservata | credential stuffing, sessioni rubate, escalation di privilegi | rate limit allauth, cookie Secure/HttpOnly/SameSite, RBAC, MFA staff |
| Documenti privati | upload malevoli, accesso non autorizzato via URL | allowlist + magic bytes, storage fuori dal web root, download autorizzato |
| Back-office | accesso non autorizzato, modifiche non tracciate | MFA per responsabilità, audit trail, permessi per ruolo |
| Integrità dei contenuti prescritti | modifica accidentale di testi legali/prescritti | registro bloccato + checksum + test |
| Infrastruttura | XSS, clickjacking, injection, MIME sniffing, downgrade TLS | CSP self-only, header, ORM, autoescape, HSTS |

## 2. Controlli implementati — mappa OWASP Top 10 (2021)

| OWASP | Controllo | Dove |
|---|---|---|
| A01 Broken Access Control | ruoli `role:*` (gruppi), policy object-level **deny-by-default** (`can()` restituisce False se nessuna policy è registrata); `require()` nelle view; `is_staff` apre solo la porta del back-office | `apps/accounts/roles.py`, `apps/accounts/permissions.py` |
| A01 | download documenti solo tramite view autorizzata, mai da `/media/` | `apps/documents/`, `PRIVATE_MEDIA_ROOT` in `config/settings/base.py` |
| A02 Cryptographic Failures | password hasher PBKDF2 (default) + Argon2 disponibile; `SECRET_KEY` e sale solo da ambiente; IP mai in chiaro | `PASSWORD_HASHERS`, `IP_HASH_SALT` in `config/settings/base.py`; `apps/core/privacy.py` |
| A02 | TLS: `SECURE_SSL_REDIRECT`, `SECURE_PROXY_SSL_HEADER`, HSTS 1 anno + `includeSubDomains` + `preload`, cookie `Secure` | `config/settings/prod.py` |
| A03 Injection | ORM Django ovunque; template autoescape; nessun `mark_safe` su input utente (regola in `docs/AGENT_CONVENTIONS.md`); contenuti editoriali in testo semplice renderizzati con `linebreaks` | tutte le app |
| A04 Insecure Design | gate di pubblicazione reali (form chiusi senza informativa legale), consenso obbligatorio non preselezionato, data minimization | `apps/core/gates.py`, `apps/core/forms.py` |
| A05 Security Misconfiguration | settings split; `DEBUG=False` in prod; `ALLOWED_HOSTS`/`CSRF_TRUSTED_ORIGINS` obbligatori in prod; `check --deploy` nel pre-deploy | `config/settings/*.py`, `docs/DEPLOYMENT.md` |
| A05 | CSP `default-src 'self'`, `script-src 'self'`, `style-src 'self'`, `img-src 'self' data:`, `font-src 'self'`, `frame-ancestors 'none'`, `form-action 'self'`, `base-uri 'self'`, `object-src 'none'`, `upgrade-insecure-requests` | `CONTENT_SECURITY_POLICY` in `config/settings/base.py` (django-csp 4) |
| A05 | `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: strict-origin-when-cross-origin`, `Cross-Origin-Opener-Policy: same-origin` | `config/settings/base.py` |
| A05 | `Permissions-Policy` (camera, microphone, geolocation, payment, usb, interest-cohort disabilitati), `Cross-Origin-Resource-Policy: same-origin`, `X-Permitted-Cross-Domain-Policies: none` | `apps/core/middleware.py::ExtraSecurityHeadersMiddleware` |
| A06 Vulnerable Components | 9 dipendenze runtime pinnate; `pip-audit` nel pre-deploy; Django LTS | `requirements/base.txt`, ADR-001 |
| A07 Identification & Auth | allauth: login solo via e-mail, verifica e-mail **obbligatoria**, `ACCOUNT_RATE_LIMITS` (login fallito 5/5m per IP e per chiave, signup 10/h/IP, reset 5/h/IP + 3/h/chiave), lunghezza minima password 12, validatori Django (similarità, password comuni, numeriche), logout al cambio password | `config/settings/base.py` |
| A07 | MFA TOTP + recovery codes (`allauth.mfa`). Chi legge i dati di altre persone (`accounts.services.MFA_REQUIRED_ROLES`) deve attivare il TOTP prima del back-office, dell'area riservata e di `/documents/` quando `BACKOFFICE_MFA_ENFORCED` è acceso (in produzione lo è per default, e `prod.py` rifiuta di partire senza). Un dispositivo già attivato va presentato in ogni sessione, qualunque sia il valore: il flag rende obbligatoria l'attivazione, non accende né spegne il secondo fattore (F-5). Il modulo di accesso proprio del back-office non autentica nessuno: lo staff entra dall'accesso di allauth e dalla sua fase MFA | `MFA_SUPPORTED_TYPES`; `apps/accounts/middleware.py`, `apps/accounts/admin_site.py`, `accounts.services.second_factor_due` |
| A07 | sessioni: 8 ore, `HttpOnly`, `SameSite=Lax`, `Secure` in prod; CSRF cookie `HttpOnly`, `SameSite=Lax` | `SESSION_*`, `CSRF_*` in `config/settings/base.py` |
| A08 Software & Data Integrity | testi prescritti in codice con checksum sha256 e test; migrazioni verificate con `makemigrations --check`; nessuno script remoto | `apps/cms/locked_content.py`, `apps/cms/locked_content.sha256.json`, `tests/compliance/test_locked_content.py` |
| A09 Logging & Monitoring | log strutturati JSON con `request_id` (header `X-Request-ID`), logger `ile.security` / `ile.audit`, nessun dato personale nei log; audit trail append-only con mirror dei `LogEntry` admin | `apps/core/logging.py`, `apps/core/middleware.py::RequestIDMiddleware`, `apps/audit/` |
| A10 SSRF | nessuna richiesta HTTP verso URL forniti dall'utente; trasporto integrazioni predefinito «logging» che non chiama la rete | `apps/integrations/` implementato |

### Django deployment checklist

| Voce | Stato |
|---|---|
| `DEBUG=False` in prod | ✅ `config/settings/prod.py` |
| `SECRET_KEY` senza default in prod | ✅ `env("DJANGO_SECRET_KEY")` obbligatoria |
| `ALLOWED_HOSTS` / `CSRF_TRUSTED_ORIGINS` da ambiente | ✅ |
| `SECURE_SSL_REDIRECT`, HSTS, cookie Secure | ✅ prod |
| `SECURE_CONTENT_TYPE_NOSNIFF`, `X_FRAME_OPTIONS` | ✅ base |
| `ATOMIC_REQUESTS` | ✅ `DATABASES["default"]["ATOMIC_REQUESTS"] = True` |
| `DATA_UPLOAD_MAX_MEMORY_SIZE` / `FILE_UPLOAD_MAX_MEMORY_SIZE` 5 MB, `DATA_UPLOAD_MAX_NUMBER_FIELDS` 200 | ✅ |
| `check --deploy` | da eseguire nel pre-deploy (`docs/DEPLOYMENT.md`) |

## 3. Sicurezza dei form pubblici

Implementata in `apps/core/forms.py` e `apps/core/throttle.py`, usata da ogni form pubblico (regola 9 di
`docs/AGENT_CONVENTIONS.md`):

- **Honeypot privacy-friendly** (`HoneypotFormMixin`): campo nascosto `website_url` (mai compilato da umani,
  `tabindex=-1`, `aria-hidden`) + timestamp `form_started_at` con tempo minimo di compilazione (3 s) e massimo
  (6 h). Lo spam riceve la stessa risposta di successo ma **non viene salvato** (nessun segnale ai bot); evento
  di audit `*.spam_dropped`.
- **Normalizzazione** (`PublicFormMixin`): rimozione caratteri di controllo, collasso spazi, lunghezza massima.
- **Consenso** (`ConsentBooleanField`): obbligatorio, mai preselezionato, etichetta = testo prescritto.
- **Throttle** (`core.throttle.allow`): contatore in cache per scope e IP **hashato**; default 5 invii/10 minuti
  (`PUBLIC_FORM_THROTTLE`); superamento → pagina `errors/429.html` con stato 429.
- **Protezione duplicati**: hash delle chiavi normalizzate entro 24 h (app `enquiries`, `forum`) — risposta di
  successo senza seconda riga, evento di audit.
- **CSRF** su tutti i POST (`CsrfViewMiddleware`); validazione server-side sempre, JS solo come progressive
  enhancement.
- **Errori generici**: nessun dettaglio interno all'utente; log con `request_id`.
- **Destinazione unica**: `notifications.services.notify_forms_inbox` invia solo a
  `settings.ILE["FORMS_DESTINATION_EMAIL"]` (= `contact@agamieuromed.org`); nessun indirizzo
  `@legalitalentry.it` può essere pubblicato (`core.models.validate_public_email`).

## 4. Hashing degli IP e dati tecnici

`apps/core/privacy.py`: `hash_ip()` = SHA-256 di `IP_HASH_SALT:ip`, troncato a 32 caratteri; `client_ip()` legge
`X-Forwarded-For` **solo** quando `USE_X_FORWARDED_HOST` è attivo (dietro proxy fidato, prod). User agent
troncato a 160 caratteri. Nessun IP in chiaro viene mai persistito (consensi, form, audit, throttle).

## 5. Audit trail

`apps/audit/models.py::AuditEvent`: append-only (admin senza add/change/delete), campi actor, action, target,
metadata JSON, `ip_hash`, `request_id`. `apps/audit/services.py::record()` è chiamato per: cambi di feature
flag/gate, pubblicazione/ritiro di testi legali, invii form (spam/duplicati inclusi), download documenti, azioni
GDPR (anonimizzazione, export). `apps/audit/signals.py` rispecchia ogni `LogEntry` dell'admin.

## 6. Documenti privati (app `documents`)

Politica vincolante (vedi spec in `docs/IMPLEMENTATION_PHASES.md` e convenzioni):

- allowlist estensioni (`.pdf .jpg .jpeg .png`) e MIME con verifica dei **magic bytes**; immagini validate con
  Pillow; PDF rifiutati se contengono token `/JavaScript` o `/Launch`; nessun eseguibile/HTML/SVG;
- dimensione massima 10 MB per documento (5 MB in memoria per richiesta);
- nome di storage casuale (uuid), directory per proprietario, storage `PRIVATE_MEDIA_ROOT` **fuori** da
  `MEDIA_ROOT` e dal web root; nessuna URL diretta;
- download solo via `documents:download` (login + policy proprietario/organizzazione/staff), `FileResponse`
  con `Content-Disposition: attachment`, `X-Content-Type-Options: nosniff`, `Cache-Control: private, no-store`;
- hook antivirus (`DOCUMENT_SCANNER`, stato `pending|clean|infected|error`): file infetti mai scaricabili;
- soft delete, retention, audit di ogni download.

## 7. RBAC e policy object-level

- Ruoli: `role:person`, `role:company`, `role:institution`, `role:university`, `role:professional`,
  `role:moderator`, `role:staff`, `role:administrator`, `role:superadmin` (`apps/accounts/roles.py`);
  `ensure_roles()` sincronizza i permessi di modello per ruolo (`ROLE_PERMISSIONS`), seed idempotente.
- Policy: `@policy(Model)` registra un predicato `(user, action, obj) -> bool`; `can()` nega per default,
  superadmin ammesso; `require()` solleva `PermissionDenied` (403 con pagina dedicata).
- Test obbligatori (marker `security`): impresa A non vede impresa B; persona A non vede persona B;
  partecipante al forum non vede dati altrui; staff limitato non accede alle sezioni superadmin; documenti
  privati inaccessibili conoscendo l'ID.

## 8. Gestione dei segreti

- Nessun segreto nel repository: `.env` è ignorato (`.gitignore`), `.env.example` contiene solo valori fittizi.
- Variabili sensibili: `DJANGO_SECRET_KEY`, `IP_HASH_SALT`, `DATABASE_URL`, `EMAIL_HOST_PASSWORD`,
  chiavi API (`integrations.ApiKey`: in DB solo l'hash, la chiave è mostrata una volta).
- Rotazione: cambiare `DJANGO_SECRET_KEY` invalida sessioni e token (reset password, conferme e-mail);
  cambiare `IP_HASH_SALT` rende non correlabili i vecchi hash (accettabile: sono usati solo per throttle/audit).
- Le credenziali di altri progetti presenti sulla macchina di sviluppo **non** sono state riutilizzate.

## 9. Logging

`config/settings/base.py::LOGGING`: filtro `RequestIDFilter`, formatter `StructuredFormatter` (JSON una riga:
ts, level, logger, request_id, message, event/actor/target/status) attivo in prod, formato semplice in dev.
Regola: nessun dato personale nei log (indirizzi e-mail, nomi, contenuti dei form); solo id, azione e
`request_id`.

## 10. Strumenti e test di sicurezza

| Strumento | Comando | Uso |
|---|---|---|
| bandit | `.venv/Scripts/python -m bandit -c pyproject.toml -r apps config` | analisi statica |
| pip-audit | `.venv/Scripts/python -m pip_audit -r requirements/base.txt` | vulnerabilità dipendenze |
| Django | `manage.py check --deploy` (settings prod) | configurazione |
| ruff | regole `S` (bandit-like) attive in `pyproject.toml` | lint |
| pytest | `-m security` | IDOR, CSRF, upload, rate limit, permessi, header |
| tests/compliance | `-m compliance` | header di sicurezza presenti, nessuna risorsa esterna, e-mail pubblica unica |

I test offensivi vengono eseguiti **solo** sull'ambiente locale creato da questo progetto; nessun test contro
sistemi di produzione.

## 11. Risposta agli incidenti (base)

1. Isolare: disattivare i form (gate `forms_override_without_legal` off, flag) o mettere il sito in
   manutenzione al reverse proxy.
2. Preservare: esportare log strutturati e `AuditEvent` del periodo (filtrando per `request_id`).
3. Ruotare: `DJANGO_SECRET_KEY`, chiavi API, password DB/SMTP; invalidare sessioni.
4. Valutare la notifica al Garante entro 72 h se dati personali sono coinvolti (vedi
   `docs/PRIVACY_BY_DESIGN.md`).
5. Correggere, ridistribuire, documentare nel `docs/QA_REPORT.md`.

## 12. Lacune note e lavori futuri

### 12.1 Chiuse dal 17 settembre

| Lacuna | Chiusura | Prova |
|---|---|---|
| Escalation di privilegio dall'admin (L-01) | Campi di privilegio nascosti **e** rifiutati; i gruppi protetti sono ripristinati dopo la scrittura della m2m | `tests/security/test_privilege_escalation.py`, 13 test |
| Ruolo auto-dichiarato alla registrazione (L-02) | Solo `role:person` è concesso su dichiarazione; ogni altro tipo apre una verifica umana e non concede nulla | `apps/accounts/tests/test_account_verification.py` |
| Sei ruoli mancanti (L-04) | Quindici ruoli; `legal_editor` e `legal_approver` **incompatibili**, applicato in `assign_role` e nel form dei gruppi | `apps/accounts/tests/test_identity_gaps.py` |
| Autorizzazione scaduta ancora valida (L-05) | `is_live` nella queryset, verificato al momento della lettura | `tests/security/test_object_permissions.py` §12 |
| Fetch-then-check nel portale (L-06) | L'autorizzazione è **nella query**; la riga non viene caricata per chi non può averla | `apps/portal/tests/test_security.py` |
| Risposte non uniformi (L-07) | **404 ovunque**, mai 403, per ciò che il chiamante non può vedere | idem, e §11 delle asserzioni |
| Nessuna revoca di sessione (L-08) | `roles.revoke_role` termina subito le sessioni aperte, con audit | `test_identity_gaps.py::TestSessionRevocation` |
| Nessun instradamento per ruolo (L-09) | Ogni ruolo arriva sulla superficie in cui lavora | `test_identity_gaps.py::TestPostLoginRouting` |
| MFA legata a `is_staff` (L-10) | `MFA_REQUIRED_ROLES`: la richiede chiunque legga dati di terzi, anche senza flag di staff | `test_identity_gaps.py::TestSecondFactor` |
| **L-13** *(non era nota)* | La policy di `CaseFile` concedeva a `role:staff` una vista che la queryset negava. Le due ora coincidono | `test_object_permissions.py::test_13_the_list_and_the_object_check_agree` |

**L-13 merita una riga a sé.** Non è stata trovata leggendo il codice: le due regole vivono in file
diversi e ciascuna, letta da sola, è ragionevole. È stata trovata dall'asserzione §61 numero 13, che
confronta la lista e il controllo sull'oggetto **per ogni ruolo**. La metà permissiva è sempre il
difetto, e qui era la policy: qualsiasi vista che l'avesse interrogata invece di passare per la
queryset avrebbe consegnato a un account di staff il fascicolo giuridico di una persona.

### 12.2 Aperte

| Lacuna | Gravità | Nota |
|---|---|---|
| `role:staff` cumula redazione editoriale e accesso ai dati delle imprese (L-03) | Media | `role:content_editor` esiste ora e può assumerne la metà editoriale: si chiude spostando permessi, non scrivendo codice. Non fatto qui perché ridurre `role:staff` richiede di verificare ogni chiamante, e la verifica vale più della fretta |
| Nessun modello di convenzione (`Agreement`) (L-11) | Media | Il perimetro istituzionale non è verificabile dal codice |
| Nessuna verifica del consenso alla lettura, impresa → persona (L-12) | Alta quando arriverà la Fase P1 | CR-04 |
| Nessun WAF/CDN deciso | — | Dipende dal prestatore di hosting UE da confermare (CR-08, aperto) |
| Scanner antivirus | Media | Solo il punto d'integrazione (`DOCUMENT_SCANNER`); nessun motore installato. **Conseguenza misurata:** ogni file risulta non analizzato, e finché la regola di consegna non lo dichiara, un revisore vede un link che risponde 403 |
| `BACKOFFICE_MFA_ENFORCED` | — | Il criterio è implementato e testato. In produzione il flag è acceso per default e `prod.py` rifiuta di partire senza; nessun primo deployment lo richiede spento, perché chi non ha un dispositivo è mandato ad attivarlo. Resta l'onboarding TOTP del personale (runbook, passo 8). Il flag rende obbligatoria l'attivazione; un dispositivo già attivato è chiesto a ogni sessione, qualunque sia il valore (F-5) |
| Nessun test d'intrusione | — | Vietato dal mandato sui sistemi di produzione, e privo di senso su `runserver` |

### 12.3 Fuori dal perimetro di questo repository

Ambiente legacy di test: solo riferimento, non fa parte di questo repository (decisione della titolarità, 11 ottobre 2026); dettagli nel registro privato.

Il nuovo modello `companies` non ha alcun campo di età e rifiuta un criterio di età digitato nel
testo libero (direttiva 2000/78/CE, D.lgs. 216/2003).
