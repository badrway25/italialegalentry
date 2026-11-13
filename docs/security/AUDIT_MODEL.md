# AUDIT MODEL — che cosa è tracciato, perché, e come la traccia resiste

Versione 1.0 · 20 settembre 2026 · Requisiti: **REQ-SEC-05**, **REQ-SEC-06**, **REQ-SEC-07**, **REQ-RUL-12**, **REQ-CAS-03**, **REQ-DOC-06**
Owner: referente tecnico · Revisione: a ogni nuovo evento, a ogni nuovo modulo di dominio

Documenti correlati: `docs/security/THREAT_MODEL.md` (T-22, T-23, T-25, T-29) ·
`docs/security/DATA_CLASSIFICATION.md` (P-19, P-20, §7.1) ·
`docs/security/PERMISSION_MODEL.md` §5.9 · `docs/security/DOCUMENT_SECURITY.md`.


> **Nota sulle citazioni dell'app `cases`.** I numeri di riga di `apps/cases/*` si riferiscono
> allo stato del **20 settembre 2026**: l'app è stata aggiunta a `INSTALLED_APPS`
> (`config/settings/base.py:67`) nella stessa giornata ed era in costruzione attiva. Le righe
> vanno riverificate alla prima revisione; i simboli citati (`readable_by`, `is_live`,
> `case_detail`, `record_assessment`, `reproduce`) sono il riferimento stabile.

---

## 0. A che cosa serve l'audit

A rispondere, mesi dopo, a quattro domande, davanti a una persona che chiede conto del trattamento
dei propri dati o davanti a un'autorità:

1. **Chi** ha visto il fascicolo di questa persona, e quando?
2. **Chi** ha cambiato questa regola giuridica, e chi l'ha approvata?
3. **Perché** il sistema ha detto quello che ha detto, quel giorno, a quella persona?
4. **Che cosa** è successo in quella finestra di tempo in cui sospettiamo un incidente?

Il criterio di accettazione D2 §17.1 è netto: «ogni accesso a un fascicolo è **autorizzato e
tracciato**». Un audit che non risponde a queste domande non è un audit: è rumore.

Marcatura: **IMPLEMENTATO** (verificato nel codice, citato) · **PARZIALE** · **RICHIESTO** ·
**DESIGN ONLY**.

---

## 1. Il modello attuale

```python
# apps/audit/models.py:6-27
class AuditEvent(models.Model):
    """Append-only administrative / security audit trail. Never edited, never deleted from the UI."""
    created_at   = models.DateTimeField(auto_now_add=True, db_index=True)
    actor        = models.ForeignKey(AUTH_USER_MODEL, on_delete=SET_NULL, null=True, blank=True, ...)
    actor_label  = models.CharField(max_length=160, blank=True)
    action       = models.CharField(max_length=80, db_index=True)
    target_type  = models.CharField(max_length=80, blank=True, db_index=True)
    target_id    = models.CharField(max_length=64, blank=True)
    target_repr  = models.CharField(max_length=200, blank=True)
    metadata     = models.JSONField(default=dict, blank=True)
    ip_hash      = models.CharField(max_length=32, blank=True)
    request_id   = models.CharField(max_length=64, blank=True)
```

Un solo punto di scrittura: `audit.services.record()` `apps/audit/services.py:11-27`, che normalizza
l'attore (gli anonimi diventano `None` `:13-14`), calcola l'impronta IP `:23` e propaga il
`request_id` `:24`.

---

## 2. Tassonomia degli eventi

Convenzione di denominazione: `dominio.oggetto.azione` in minuscolo, con il dominio corrispondente
all'app. Il nome è un identificatore stabile: **non si rinomina un evento già emesso**, se ne
aggiunge uno nuovo.

### 2.1 Eventi di autenticazione e sicurezza dell'accesso — **RICHIESTI, oggi assenti**

Verificato: nessun ricevitore per `user_logged_in`, `user_logged_out`, `user_login_failed` esiste nel
repository. È la lacuna più grave della copertura (REQ-SEC-06 elenca «eventi di sicurezza
dell'accesso» al primo posto).

| Evento | Quando | Metadata minimi | Stato |
|---|---|---|---|
| `auth.login` | Accesso riuscito | metodo (password/TOTP), `mfa_used` | **RICHIESTO** |
| `auth.login_failed` | Credenziali errate | motivo generico, **mai la password né l'e-mail provata in chiaro** | **RICHIESTO** |
| `auth.logout` | Disconnessione | — | **RICHIESTO** |
| `auth.rate_limited` | Limite di allauth superato | scope | **RICHIESTO** |
| `auth.password_changed` | Cambio password | origine (self / admin) | **RICHIESTO** |
| `auth.password_reset_requested` / `auth.password_reset_completed` | Reset | — | **RICHIESTO** |
| `auth.email_verified` | Verifica e-mail | — | **RICHIESTO** |
| `auth.mfa_enabled` / `auth.mfa_disabled` / `auth.mfa_recovery_used` | Secondo fattore | tipo | **RICHIESTO** |
| `auth.session_revoked` | Revoca di sessione | motivo | **RICHIESTO** (la funzione stessa non esiste, REQ-IAM-08) |

### 2.2 Permessi e ruoli — **PARZIALE**

| Evento | Quando | Stato |
|---|---|---|
| `iam.role_granted` / `iam.role_revoked` | Un gruppo `role:*` è assegnato o tolto | **RICHIESTO** — oggi `roles.assign_role` `apps/accounts/roles.py:96-99` non traccia nulla, nemmeno quando la registrazione assegna un ruolo `apps/accounts/forms.py:49-50` |
| `iam.superuser_granted` / `iam.staff_granted` | Concessione di `is_superuser` / `is_staff` | **RICHIESTO** — è il controllo che rende visibile T-04 |
| `iam.permission_changed` | Modifica di `ROLE_PERMISSIONS` applicata da `ensure_roles()` | **RICHIESTO** |
| `admin.add` / `admin.change` / `admin.delete` | Qualunque scrittura dal back-office | **IMPLEMENTATO** — mirror di `LogEntry` `apps/audit/signals.py:12-24`, con `change_message` troncato a 500 caratteri |

La copertura odierna è indiretta: se un amministratore cambia i gruppi di un utente dal back-office,
esiste una riga `admin.change` su `user` con un messaggio generico. **Non basta**: non dice quale
privilegio è stato concesso né qual era il valore precedente.

### 2.3 Accesso ai fascicoli — **PARZIALE**

| Evento | Quando | Metadata | Stato |
|---|---|---|---|
| `case.opened` | Apertura di un fascicolo | `purpose`, `pathway` | **IMPLEMENTATO** `apps/cases/services.py:68` |
| `case.transition` | Cambio di stato | `from`, `to`, `reason` (500 car.) | **IMPLEMENTATO** `:114-121` |
| `case.assessment` | Esecuzione di una valutazione | `outcome`, `ruleset_version`, `assessment_id` | **IMPLEMENTATO** `:176-181` |
| `case.checklist.status` | Cambio di stato di un requisito | `item`, `from`, `to` | **IMPLEMENTATO** `:248-255` |
| `case.assigned` | Nuova assegnazione | `assignee`, `role`, `authorisation` (bool) | **IMPLEMENTATO** `:312-319` |
| `case.assignment.revoked` | Revoca | `assignment` | **IMPLEMENTATO** `:326-333` |
| **`case.viewed`** | **Lettura** di un fascicolo da parte di chi non ne è titolare | ruolo dell'accesso, assegnazione usata | **RICHIESTO** — è letteralmente il criterio D2 §17.1 e oggi **non esiste** |
| `case.exported` | Export del fascicolo | formato, destinatario | **RICHIESTO** |

> **La lacuna decisiva.** Oggi si traccia ciò che *modifica* il fascicolo, non ciò che lo *legge*.
> «Ogni accesso a un fascicolo è autorizzato e tracciato» resta vero solo per metà. La lettura da
> parte del titolare può essere esclusa (sono i suoi dati, e tracciarla creerebbe volume inutile);
> **ogni lettura da parte di chiunque altro** — professionista, operatore, staff, amministratore,
> superadmin — dev'essere un evento.

### 2.4 Documenti — **PARZIALE**

| Evento | Stato | Dove |
|---|---|---|
| `documents.uploaded` (`kind`, `size`, `scan_status`) | **IMPLEMENTATO** | `apps/documents/services.py:272-278` |
| `documents.downloaded` (`scan_status`) | **IMPLEMENTATO** | `apps/documents/views.py:114` |
| `documents.scan_result` (`status`, `note`) | **IMPLEMENTATO** | `services.py:218-224` |
| `documents.deleted` | **IMPLEMENTATO** | `services.py:300` |
| `documents.purged` (`file_removed`, `reason`) | **IMPLEMENTATO** | `services.py:313-319` |
| `documents.viewed` (apertura della scheda senza download) | **RICHIESTO** | — |
| `documents.status_changed` (stati di dominio: VALIDO, NON VALIDO, SCADUTO…) | **RICHIESTO** | gli stati non esistono (`DOCUMENT_SECURITY.md` §8) |
| `documents.version_added` | **RICHIESTO** | versionamento assente |
| `documents.exported` (CSV di back-office) | **RICHIESTO** | `apps/documents/admin.py:135-157` esporta e-mail e nomi di file **senza** evento |
| `documents.link_issued` (URL firmata) | **RICHIESTO** | la funzione non esiste |

### 2.5 Regole giuridiche — **PARZIALE**

| Evento | Stato |
|---|---|
| `orientation.ruleset.activated` | **IMPLEMENTATO** `apps/orientation/services.py:125` |
| `rules.rule_created` / `rules.rule_changed` (con diff) | **RICHIESTO** (REQ-RUL-12) |
| `rules.submitted_for_review` | **RICHIESTO** |
| `rules.approved` / `rules.rejected` (con il **secondo** paio d'occhi) | **RICHIESTO** — è la prova che l'autore non si è auto-approvato |
| `rules.retired` | **RICHIESTO** |
| `rules.source_changed` | **RICHIESTO** |

Oggi un amministratore con `orientation: change` `apps/accounts/roles.py:65` può modificare una
condizione e lasciare come unica traccia una riga `admin.change` generica. Per un sistema che
produce orientamento giuridico, non è sufficiente.

### 2.6 Valutazioni — **IMPLEMENTATO (con snapshot)**

`case.assessment` è emesso da `cases.services.record_assessment`, che **rifiuta** di registrare una
valutazione senza snapshot integrale `apps/cases/services.py:158-161`. Vedi §7.

Per l'orientamento pubblico: `orientation.session.started`, `.saved`, `.resumed`, `.completed`,
`.deleted`, `.anonymised` sono **IMPLEMENTATI** (`apps/orientation/services.py`).

### 2.7 Consensi e privacy — **IMPLEMENTATO in parte**

| Evento | Stato |
|---|---|
| `account.profile_updated` (elenco dei campi cambiati) | **IMPLEMENTATO** `apps/accounts/services.py:78` |
| `account.export` (art. 15/20) | **IMPLEMENTATO** `apps/accounts/views.py:64` |
| `account.deletion_requested`, `account.anonymised` | **IMPLEMENTATO** `services.py:225-231,247` |
| `portal.account_data_erased` | **IMPLEMENTATO** |
| `enquiries.anonymised`, `forum.registration.anonymised`, `orientation.session.anonymised` | **IMPLEMENTATO** |
| `consent.granted` / `consent.withdrawn` | **RICHIESTO** — la prova sta in `ConsentRecord` (che è essa stessa un registro), ma l'evento di audit correlato manca |

### 2.8 Azioni amministrative e di pubblicazione — **IMPLEMENTATO**

`feature_flag.changed` `apps/core/admin.py:28` · `legal.published` / `legal.unpublished`
`apps/legal/services.py:69-83` · `news.article.*`, `living.sheet.*`, `forum.programme.reset` ·
`enquiries.handled`, `enquiries.export_csv`, `enquiries.export_json`, `enquiries.purged` ·
`forum.registration.status`, `forum.registration.export` · `admin.add/change/delete` (mirror).

### 2.9 Eventi di sicurezza dei form pubblici — **IMPLEMENTATO**

`enquiries.submitted`, `enquiries.spam_dropped`, `enquiries.duplicate`,
`forum.registration.created/duplicate/spam_rejected/throttled`. Servono a dimostrare che un invio è
stato ricevuto e perché non è stato salvato.

### 2.10 Integrazioni — **IMPLEMENTATO**

`webhooks.inbound` (con esito della verifica di firma), `events.list`, `events.ack` — ogni chiamata
API passa dal decoratore che registra l'azione `apps/integrations/api.py:59-79`.

### 2.11 Copertura rispetto a REQ-SEC-06

| Categoria richiesta | Copertura |
|---|---|
| Eventi di sicurezza dell'accesso | **0 %** — §2.1 |
| Modifiche di permessi e ruoli | **~30 %** — solo via mirror dell'admin, senza dettaglio |
| Accessi ai fascicoli | **scritture sì, letture no** |
| Accesso e download di documenti sensibili | **download sì, lettura della scheda no, export CSV no** |
| Modifiche e approvazioni di regole | **solo l'attivazione del ruleset** |
| Esecuzione di valutazioni | **sì**, con snapshot |
| Cambi di assegnazione | **sì** |
| Cambi di stato del fascicolo | **sì** |
| Consensi | **parziale** (il registro esiste, l'evento no) |
| Azioni amministrative | **sì** |

---

## 3. Campi di un evento

### 3.1 Campi attuali

| Campo | Tipo | Significato | Note |
|---|---|---|---|
| `created_at` | datetime, indicizzato | Quando. `auto_now_add`, ora del server (UTC in DB, `Europe/Rome` per la lettura) | Non modificabile dal chiamante |
| `actor` | FK utente, `SET_NULL` | Chi. `NULL` per anonimo o per utente rimosso | `SET_NULL` conserva l'evento se l'utente sparisce |
| `actor_label` | char(160) | Etichetta leggibile dell'attore | **Contiene l'e-mail** (`str(user)`): vedi §5 |
| `action` | char(80), indicizzato | Che cosa | Vocabolario controllato §2 |
| `target_type` | char(80), indicizzato | Su quale tipo di oggetto | Nome della classe Python |
| `target_id` | char(64) | Su quale oggetto | PK come stringa (regge interi e UUID) |
| `target_repr` | char(200) | Etichetta leggibile dell'oggetto | **Può contenere dati personali**: vedi §5 |
| `metadata` | JSON | Il contesto specifico dell'evento | Deve restare piccolo e privo di contenuti |
| `ip_hash` | char(32) | Impronta dell'IP, mai l'indirizzo | `hash_ip` `apps/core/privacy.py:19-27` |
| `request_id` | char(64) | Correlazione con i log applicativi | `apps/core/middleware.py:15-31` |

Indici: `created_at`, `action`, `target_type` e un indice composto `(target_type, target_id)`
`apps/audit/models.py:26` — quest'ultimo è ciò che rende praticabile la domanda «tutto quello che è
successo a questo fascicolo».

### 3.2 Campi richiesti

| Campo | Perché | Stato |
|---|---|---|
| `outcome` (`success` / `denied` / `error`) | Un tentativo **negato** è più interessante di uno riuscito. Oggi non si distingue | **RICHIESTO** |
| `actor_roles` | I ruoli **al momento dell'azione**: i ruoli cambiano, la riga no | **RICHIESTO** |
| `on_behalf_of` / `authorisation_ref` | Con quale mandato o assegnazione l'attore ha agito | **RICHIESTO** |
| `previous_hash` + `row_hash` | Catena di integrità (§4.3) | **RICHIESTO** |
| `sequence` | Numero progressivo per rilevare i buchi | **RICHIESTO** |
| `source` (`web` / `admin` / `api` / `command`) | Da dove è arrivata l'azione | **RICHIESTO** |

### 3.3 Regole sui `metadata`

- solo identificatori, enumerazioni, booleani, conteggi e timestamp;
- i testi liberi sono troncati (già fatto: `reason[:500]` `apps/cases/services.py:120`,
  `note[:200]` `apps/documents/services.py:223`, `change_message[:500]` `apps/audit/signals.py:23`);
- **mai** il contenuto di un documento, di un messaggio, di una risposta del questionario o di un
  campo libero di un form;
- mai valori che, uniti, ricostruiscano un dato personale non necessario all'evento;
- lo schema di `metadata` per ciascun `action` va documentato qui quando l'evento viene introdotto.

---

## 4. Come la traccia resiste alla manomissione

### 4.1 Quello che c'è oggi

| Difesa | Stato | Dove |
|---|---|---|
| Nessuna aggiunta, modifica o cancellazione dall'interfaccia di amministrazione | **IMPLEMENTATO** | `has_add_permission`, `has_change_permission`, `has_delete_permission` → `False`; tutti i campi readonly `apps/audit/admin.py:13-22` |
| Solo `view` concesso al ruolo amministratore | **IMPLEMENTATO** | `apps/accounts/roles.py:72` |
| Nessun'altra vista scrive su `AuditEvent` | **IMPLEMENTATO** | Unico scrittore: `audit.services.record` `:15-25` (più il mirror `signals.py:16`) |
| Le azioni dell'admin sono rispecchiate automaticamente | **IMPLEMENTATO** | `apps/audit/signals.py:12-24` |
| L'evento sopravvive alla cancellazione dell'attore | **IMPLEMENTATO** | `on_delete=SET_NULL` `models.py:10-12` |

### 4.2 Quello che manca, detto senza attenuazioni

> **«Append-only» è oggi una convenzione dell'interfaccia, non una proprietà dello storage.**

L'utente di database dell'applicazione può eseguire `UPDATE` e `DELETE` sulla tabella, e **il codice
stesso lo fa**: l'anonimizzazione di un account riscrive le etichette delle righe esistenti

```python
# apps/accounts/services.py:233-234
AuditEvent.objects.filter(actor_id=user_id).update(actor_label=label)
AuditEvent.objects.filter(target_type="User", target_id=str(user_id)).update(target_repr=label)
```

Questa scrittura è **legittima e voluta** (pseudonimizzazione per l'art. 17, senza distruggere la
traccia), ma dimostra che nulla impedisce una scrittura **illegittima** dello stesso tipo. Chi
compromette un amministratore o l'account di database può riscrivere la storia. REQ-SEC-05 è
correttamente `PARTIAL`.

### 4.3 La strategia richiesta

Quattro misure, in ordine di rapporto valore/costo:

**1. Privilegi di database (la misura decisiva)** — **RICHIESTO**

Un ruolo PostgreSQL applicativo con `INSERT` e `SELECT` sulla tabella `audit_auditevent` e **senza**
`UPDATE` né `DELETE`; le migrazioni girano con un ruolo diverso.

```sql
REVOKE UPDATE, DELETE, TRUNCATE ON audit_auditevent FROM ile_app;
GRANT INSERT, SELECT ON audit_auditevent TO ile_app;
```

Conseguenza operativa: la pseudonimizzazione di §4.2 va spostata in una funzione con privilegi
elevati (`SECURITY DEFINER`), limitata ai due soli campi di etichetta e **essa stessa tracciata** con
un evento `audit.pseudonymised`.

**2. Trigger di rifiuto** — **RICHIESTO**

Un trigger `BEFORE UPDATE OR DELETE` che solleva un'eccezione: difesa in profondità se i privilegi
venissero riconcessi per errore.

**3. Catena di hash** — **RICHIESTO**

`row_hash = SHA256(previous_hash || created_at || actor_id || action || target_type || target_id ||
metadata_canonico)`, con `previous_hash` dell'ultima riga. Una verifica periodica ricalcola la catena
e segnala il primo punto di rottura. Non impedisce la manomissione: la rende **rilevabile**, che è
l'unica proprietà ottenibile quando l'attaccante ha il database.

**4. Copia fuori host** — **RICHIESTO**

Spedizione continua verso un archivio append-only presso un altro fornitore, o almeno un export
firmato giornaliero. Senza questo, chi controlla il server controlla anche la prova. Vincolato alla
scelta dell'hosting SEE (**CR-08**, gate G12).

### 4.4 Continuità della scrittura

`ATOMIC_REQUESTS = True` `config/settings/base.py:134`: l'evento di audit **partecipa alla
transazione** dell'azione che descrive. Conseguenze da conoscere:

- se l'azione fallisce, l'evento non viene scritto — **coerente** per le scritture;
- per i tentativi **negati** (403), l'audit deve essere scritto **fuori** dalla transazione fallita
  (una transazione separata), altrimenti il tentativo non lascia traccia. Oggi i 403 non sono
  tracciati affatto (§3.2, campo `outcome`);
- un errore nella scrittura dell'audit fa fallire l'azione: è la scelta giusta per le operazioni
  sensibili («nessuna azione senza traccia»), ma va resa **esplicita** e verificata.

---

## 5. Che cosa non deve mai entrare nell'audit

| Mai | Perché | Stato |
|---|---|---|
| Password, hash di password, token di sessione, token di reset, chiavi API, segreti dei webhook | Il log di audit è leggibile da più persone del database | **IMPLEMENTATO**: nessun percorso li passa a `record()` |
| Contenuto di un documento privato | Duplicherebbe il dato più sensibile in un archivio più esposto | **IMPLEMENTATO** |
| Corpo di un messaggio, risposte del questionario, testo dei form | Idem | **IMPLEMENTATO** |
| **Dati di categoria particolare (art. 9)** | Oggi non esistono (`DATA_CLASSIFICATION.md` §5). Se esistessero, l'audit registra «documento sanitario consultato», **mai** il contenuto | **IMPLEMENTATO per assenza** |
| Indirizzo IP in chiaro | Dato personale; basta l'impronta | **IMPLEMENTATO**: `ip_hash` `apps/audit/services.py:23` |
| Dati personali di terzi non pertinenti all'azione | Minimizzazione | **PARZIALE** |

### 5.1 Il caso `actor_label` / `target_repr`

Questi due campi contengono **deliberatamente** un'etichetta umana: `actor_label = str(actor)`, cioè
l'indirizzo e-mail `apps/audit/services.py:17`, e `target_repr = str(target)`, che per un documento
privato è il **nome del file caricato** (`PrivateDocument.__str__` `apps/documents/models.py:97-98`).

**Dentro la tabella è accettabile**: l'audit deve restare leggibile anche se la riga di origine è
stata anonimizzata, e l'accesso alla tabella è riservato (§6). La pseudonimizzazione
all'anonimizzazione dell'account (§4.2) è la contropartita corretta.

**Fuori dalla tabella non lo è.** La stessa funzione scrive sul logger:

```python
# apps/audit/services.py:26
log.info("audit %s", action, extra={"event": action, "actor": event.actor_label, "target": event.target_repr})
```

e il formatter strutturato — attivo in produzione `config/settings/prod.py:34` — copia `actor` e
`target` nel JSON `apps/core/logging.py:27-29`. **Risultato: e-mail degli utenti e nomi dei file
caricati finiscono nei log applicativi**, che sono raccolti e conservati dal prestatore di hosting.

Questo contraddice `docs/SECURITY.md` §9 («nessun dato personale nei log») e lo stato `DONE` di
REQ-SEC-07. **Correzione richiesta**: nel log strutturato passare `actor_id`, `target_type`,
`target_id` e `request_id`; le etichette umane restano solo nella riga di database. È la stessa
lacuna T-25 del threat model.

---

## 6. Chi legge l'audit, e per quanto si conserva

### 6.1 Lettura

| Soggetto | Accesso | Stato |
|---|---|---|
| `role:administrator` | Sola lettura di tutto, da `/backoffice/` con MFA | **IMPLEMENTATO** `apps/accounts/roles.py:72`, `apps/audit/admin.py` |
| `superadmin` | Sola lettura di tutto | **IMPLEMENTATO** |
| DPO / revisore esterno | Sola lettura, accesso nominativo e a termine | **DESIGN ONLY** — non esiste un ruolo dedicato |
| **La persona interessata** | La cronologia delle attività **sul proprio fascicolo** (chi ha visto, chi ha deciso, quando) | **DESIGN ONLY** — previsto da D2 §9 («cronologia attività» nel fascicolo). È anche la forma più concreta di trasparenza verso l'interessato |
| `role:legal_approver` | Sola lettura della traccia delle regole giuridiche e delle loro fonti, ciò che revisiona — nient'altro | **IMPLEMENTATO** (F-8: fino a ottobre 2026 leggeva ogni evento) `apps/audit/admin.py` |
| Tutti gli altri ruoli | Nessun accesso | **IMPLEMENTATO** (deny by default) |

**La lettura dell'audit dovrebbe essere essa stessa tracciata** (`audit.read`, `audit.exported`),
soprattutto quando è massiva: oggi non lo è. **RICHIESTO.**

Nessuna esportazione dell'audit è prevista dall'interfaccia: se verrà aggiunta, va tracciata e
limitata (T-29).

### 6.2 Conservazione

| Categoria di evento | Durata proposta | Motivazione | Stato |
|---|---|---|---|
| Eventi di sicurezza dell'accesso (§2.1) | 12 mesi | Rilevazione di intrusioni, indagini | **DA CONFERMARE** dal titolare |
| Accessi e download di documenti e fascicoli | **quanto il fascicolo** | Serve a rispondere «chi ha visto i miei dati» finché i dati esistono | **DA CONFERMARE** |
| Modifiche e approvazioni di regole | **permanente** | È la prova della governance giuridica; la regola può essere invocata anni dopo | **DA CONFERMARE** |
| Valutazioni (`case.assessment`) | quanto il fascicolo, mai meno della valutazione stessa | Riproducibilità (§7) | **DA CONFERMARE** |
| Consensi | quanto la prova di consenso | Dimostrabilità, art. 7(1) | **DA CONFERMARE** |
| Azioni amministrative | 24 mesi | Allineato alla retention più lunga oggi decisa | **DA CONFERMARE** |
| Eventi dei form pubblici | 24 mesi | Coerente con **CR-12** e la retention dei dati descritti | **DA CONFERMARE** |

> **Nessuna di queste durate è stata inventata come definitiva**: sono proposte, coerenti con
> l'unica durata esistente (24 mesi per i form pubblici, **CR-12**) e con il principio «non inventare
> periodi di conservazione» (RB §45). Vanno confermate dal titolare insieme alle durate della
> piattaforma autenticata (`DATA_CLASSIFICATION.md` §6.2, questione Q-01).

Finché non sono confermate, **l'audit non viene purgato**: conservare un dato tecnico in eccesso è
un rischio minore che distruggere la prova di un accesso. La purga, quando arriverà, sarà per
categoria di `action`, con un evento `audit.purged` che ne conserva il riepilogo (quante righe, quale
intervallo, quale regola applicata).

---

## 7. Ricostruire l'esito del rule engine

È il criterio di accettazione D2 §17.2: **«ogni esito del Rule Engine è riproducibile con lo snapshot
della versione delle regole»**. Non «tracciabile»: **riproducibile**.

### 7.1 Che cosa viene congelato

`PathwayAssessment` `apps/cases/models.py:377-405` conserva, per ogni esecuzione:

| Campo | Contenuto |
|---|---|
| `assessed_at` | Quando è stata eseguita |
| `outcome` | `POSSIBLE`, `MISSING_REQUIREMENT`, `WARNING`, `STOP`, `REVIEW_REQUIRED` (i cinque di **CR-11**; `eligible` non esiste) |
| `pathway_key` | Il percorso considerato |
| `ruleset_version` | La versione del ruleset |
| **`ruleset_snapshot`** | **L'intero ruleset**, non un riferimento |
| `answers` | Le risposte esatte usate |
| `applied_rules` | Le regole che hanno effettivamente inciso |
| `missing_requirements` | I requisiti mancanti prodotti |
| `sources` | Le fonti associate |
| `rationale` | La motivazione mostrata alla persona |

Il servizio **rifiuta** di registrare una valutazione senza snapshot:

```python
# apps/cases/services.py:158-161
if not ruleset_snapshot:
    raise ValidationError({"ruleset_snapshot": _("Lo snapshot del ruleset è obbligatorio.")})
```

con la motivazione scritta nel docstring `:155-156`: «*a pointer stops being reproducible the moment
the rules change*». È la differenza fra questo modello e `orientation.OrientationResult`, che conserva
`answers_snapshot` e `ruleset_version` **ma non il ruleset** (`apps/orientation/models.py:413-428`):
per l'orientamento pubblico, REQ-RUL-06 resta quindi `PARTIAL`.

### 7.2 Come un revisore ricostruisce un esito

1. **Trovare l'evento**: `AuditEvent` con `action = "case.assessment"`,
   `target_type = "CaseFile"`, `target_id = <id>`. I `metadata` danno `assessment_id`, `outcome`,
   `ruleset_version` `apps/cases/services.py:176-181`. Con `request_id` si correlano i log della
   stessa richiesta.
2. **Aprire la valutazione**: `PathwayAssessment` con quell'`assessment_id`.
3. **Rieseguire**:

```python
# apps/cases/services.py:197-207
def reproduce(assessment: PathwayAssessment) -> dict:
    spec = spec_from_dict(assessment.ruleset_snapshot)
    return evaluate(spec, assessment.answers)
```

`spec_from_dict` ricostruisce il ruleset congelato `apps/orientation/engine.py:556` ed `evaluate` lo
esegue `:359`. Il motore è **puro, deterministico e senza ORM** (nessuna lettura di database durante
la valutazione, nessun `eval()`): a parità di snapshot e risposte, l'esito è identico oggi e fra
cinque anni.

4. **Confrontare** l'esito ricalcolato con `assessment.outcome` e `applied_rules`. Una differenza
   significa una delle tre cose, tutte gravi e tutte rilevabili: lo snapshot è stato manomesso, le
   risposte sono state manomesse, o il motore è cambiato in modo non retrocompatibile.
5. **Spiegare**: `applied_rules` e `rationale` dicono *perché*; `sources` con quali fonti;
   `missing_requirements` che cosa mancava; il disclaimer mostrato è versionato
   (`OrientationResult.disclaimer_version` per l'orientamento pubblico).

### 7.3 Che cosa serve perché la ricostruzione sia completa

| Elemento | Stato |
|---|---|
| Snapshot integrale del ruleset sulla valutazione | **IMPLEMENTATO** `apps/cases/services.py:158-175` |
| Funzione di riesecuzione | **IMPLEMENTATO** `:195-205` |
| Motore deterministico, senza `eval()` | **IMPLEMENTATO** `apps/orientation/engine.py:183-216` |
| Test che dimostri la riproducibilità su un caso reale | **RICHIESTO** — è la prova che il criterio D2 §17.2 è soddisfatto |
| Versione del **motore** registrata accanto allo snapshot | **RICHIESTO**: lo snapshot congela i dati, non il codice che li interpreta |
| `valid_from` / `valid_to` e **data di valutazione** nel ruleset | **RICHIESTO** (REQ-RUL-05): oggi non si può dimostrare che erano quelle le regole *vigenti* quel giorno |
| Storia di approvazione della regola (chi, quando, con quale fonte) | **RICHIESTO** (REQ-RUL-10/12) |
| Snapshot integrale anche per l'orientamento pubblico | **RICHIESTO** (REQ-RUL-06) |
| Accesso in lettura del revisore a tutto ciò | **DESIGN ONLY** |

> **La catena completa, quando sarà chiusa:**
> «questa persona, quel giorno, ha ricevuto questo esito, perché **queste** regole — approvate da
> **quella** persona il **quel** giorno, vigenti in **quella** data, basate su **quelle** fonti —
> applicate a **queste** risposte, producono **questo** risultato; e chiunque può rieseguirlo.»
> Oggi mancano i tre pezzi in corsivo che riguardano la **governance** della regola; il pezzo
> tecnico — snapshot e riesecuzione — **è già in piedi**.

---

## 8. Lacune, in ordine di priorità

| # | Lacuna | Gravità | Requisito |
|---|---|---|---|
| 1 | Nessun evento di autenticazione (login, fallimento, logout, reset, MFA) | **Alta** | REQ-SEC-06 |
| 2 | Append-only non applicato dallo storage; nessuna catena di hash; nessuna copia fuori host | **Alta** | REQ-SEC-05 |
| 3 | Nessun evento sulla **lettura** di un fascicolo da parte di un non titolare | **Alta** | D2 §17.1, REQ-SEC-06 |
| 4 | Nessun evento su concessione/revoca di ruoli e privilegi | **Alta** | REQ-IAM-05, T-04 |
| 5 | Dati personali (e-mail, nomi di file) nei log strutturati | **Alta** | REQ-SEC-07, T-25 |
| 6 | Nessun evento sulle modifiche e approvazioni di regole | **Alta** | REQ-RUL-12 |
| 7 | I tentativi **negati** non sono tracciati (manca `outcome`) | Media | REQ-SEC-06 |
| 8 | Export CSV dei documenti senza evento | Media | REQ-DOC-06 |
| 9 | Ruoli dell'attore non congelati sulla riga | Media | — |
| 10 | Durate di conservazione dell'audit non confermate dal titolare | Media | CR-12 |
| 11 | Nessun accesso dell'interessato alla cronologia del proprio fascicolo | Media | D2 §9 |
| 12 | La lettura e l'export dell'audit non sono tracciati | Bassa | REQ-SEC-06 |
| 13 | Nessuno strumento di consultazione oltre l'admin (nessuna vista per incidente, nessuna correlazione) | Bassa | REQ-SEC-08 |

### Le quattro da fare per prime

1. **Eventi di autenticazione** (`auth.*`): ricevitori sui segnali di Django/allauth. Poche ore di
   lavoro, chiude la lacuna più visibile.
2. **`iam.role_granted` / `iam.superuser_granted`** con valore precedente e successivo: è il
   controllo che rende rilevabile T-04, la minaccia numero uno del threat model.
3. **Append-only a livello di database**: privilegi, trigger, e spostamento della pseudonimizzazione
   in una funzione privilegiata e tracciata.
4. **`case.viewed`**: senza questo evento, il criterio di accettazione D2 §17.1 non è soddisfatto,
   qualunque cosa dica l'interfaccia.

---

Classificazione di questo documento: **interno**
(`docs/source-of-truth/CONFIDENTIALITY_REGISTER.md` §2).
