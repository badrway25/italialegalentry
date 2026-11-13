# CRM INTEGRATION CONTRACT — Italy Legal Entry™

Stato: **implementato (foundation, nessun CRM collegato)** — riferimento 17 settembre 2026.
Codice: `apps/integrations/` (ADR-011: API interna minimale, nessun DRF). Nessuna chiamata di rete
avviene per default: il trasporto predefinito registra solo un log.

## 1. Perimetro (boundary)

```
DOMINIO (enquiries, forum, community, orientation, accounts)
   │  post_save / services.emit()          ← unico punto di contatto in uscita
   ▼
integrations.OutboundEvent (outbox idempotente, payload minimo)
   │                     │
   │ push (cron)         │ pull (API v1)
   ▼                     ▼
Transport (Logging|Http) GET /api/v1/events/ + POST …/ack/
   │
   ▼
CRM / sistema esterno ──► POST /api/v1/webhooks/<system>/ (HMAC)  ──► InboundWebhookLog (+ audit)
                       ──► ExternalReference (id esterno ↔ oggetto locale, stato di sync)
```

Regole di confine:
1. Nessun modello di dominio è esposto: l'API serializza solo `OutboundEvent` tramite
   `integrations.services.serialize_event`.
2. Le app di dominio **non importano** `integrations` (eccezione: `community`, stesso owner, chiama
   `emit()` dal proprio service layer). Gli altri modelli vengono osservati da `integrations/signals.py`
   con `apps.get_model()` lazy: se il modello non esiste ancora il receiver è saltato (nessun crash).
3. Ogni chiamata API e ogni webhook genera un `audit.AuditEvent` (`api.<azione>`, `webhook.received`,
   `webhook.rejected`).
4. I segreti non sono mai in database: si registra solo il **nome** della variabile d'ambiente e,
   facoltativamente, l'impronta SHA-256 per rilevare un ambiente mal configurato.

## 2. Entità

| Modello | Ruolo | Campi chiave |
|---|---|---|
| `ExternalSystem` | sistema esterno registrato | `key` (slug unico), `name`, `is_active`, `inbound_secret_env`, `inbound_secret_hash`, `note` |
| `ExternalReference` | mappa id esterno ↔ oggetto locale | `system`, `content_type`, `object_id`, `external_id`, `sync_status` (pending/synced/error), `last_synced_at`, `last_error`; **unique (system, content_type, object_id)**; indice (system, external_id) |
| `OutboundEvent` | evento in uscita (outbox) | `uuid`, `event_type`, `system` (null = broadcast), `content_type`/`object_id`, `occurred_at`, `payload` JSON, `idempotency_key` (unique), `status` (queued/delivered/failed/cancelled), `attempts`, `next_attempt_at`, `delivered_at`, `acknowledged_at`, `acknowledged_by`, `response_code`, `last_error` |
| `WebhookEndpoint` | destinazione push | `system`, `url`, `signing_secret_env`, `secret_hash`, `event_types` (lista vuota = tutti), `is_active` (default **False**), `last_*` |
| `InboundWebhookLog` | ogni chiamata ricevuta | `system`, `system_key`, `nonce`, `timestamp`, `signature_valid`, `status_code`, `event_type`, `payload` (solo identificativi), `error`, `request_id`; **unique parziale (system, nonce) where signature_valid** |
| `ApiKey` | chiave bearer | `name`, `prefix` (8 hex), `key_hash` (sha256, unique), `scopes` JSON, `system` (null = solo eventi broadcast), `is_active`, `expires_at`, `last_used_at`, `created_by` |

Servizi (`integrations/services.py`): `emit`, `sanitize_payload`, `serialize_event`, `deliver_pending`,
`cancel_event`, `requeue_event`, `events_for_key`, `acknowledge`, `create_api_key`, `hash_key`,
`link_external_id`, `external_id_of`, `mark_sync_error`.

## 3. Catalogo eventi

| `event_type` | Sorgente | Quando | `data` (payload minimo) |
|---|---|---|---|
| `enquiries.company_needs.created` | `enquiries.CompanyNeedsRequest` (post_save, created) | nuovo Recueil des besoins | `category`/`kind`/`status`/`language` se presenti come codici, `created_at` |
| `enquiries.collaboration_proposal.created` | `enquiries.CollaborationProposal` | nuova proposta istituzione/università | idem |
| `forum.registration.created` | `forum.ForumRegistration` | nuova iscrizione al Forum Vénétie–Maroc | idem (`category` = una delle 8 categorie) |
| `community.membership.requested` | `community.services.request_membership` | richiesta di accesso al Forum Virtuale | `category`, `created_at` |
| `community.membership.approved` | `community.services.approve_membership` | approvazione | `category` |

Il campo `object` dell'evento (`{"type": "enquiries.companyneedsrequest", "id": "42"}`) permette al CRM
di recuperare i dettagli tramite un **futuro endpoint autenticato** (decisione aperta §12).

Come far emettere eventi da un'altra app (senza modificare `integrations`):
```python
# opzione A — già attiva: post_save agganciato in integrations/signals.py (WATCHED_MODELS)
# opzione B — dal service layer dell'app, per eventi di stato (non solo creazione):
from integrations.services import emit
emit("enquiries.company_needs.status_changed", obj, {"status": obj.status})
```
Per aggiungere un modello osservato: aggiungere la coppia `("app.Model", "prefisso")` a
`integrations.signals.WATCHED_MODELS`.

## 4. Idempotenza

* `idempotency_key` default = `"<event_type>:<app_label>.<model>:<pk>"` (unique in DB). Un secondo
  `emit()` con la stessa chiave restituisce `None` senza errori (nessun duplicato, IntegrityError
  intercettata in savepoint).
* Per eventi ripetibili sullo stesso oggetto (cambi di stato) passare `idempotency_key` esplicito
  (es. `f"...status_changed:{obj.pk}:{obj.status}"`).
* L'`uuid` dell'evento è stabile: il CRM deve de-duplicare su `uuid`.
* `POST /events/<uuid>/ack/` è idempotente: la seconda chiamata restituisce lo stesso oggetto.

## 5. Consegna, retry e backoff

* `deliver_pending(limit)` (comando `manage.py deliver_outbound_events`, da cron) seleziona gli eventi
  `queued` non ancora acked con `next_attempt_at <= now` (`core.clock.now()`).
* Trasporto = `INTEGRATIONS_TRANSPORT` (dotted path). Default `integrations.transports.LoggingTransport`:
  **nessuna rete**; con `DEBUG=True` segna l'evento come consegnato (per vedere l'outbox svuotarsi in
  sviluppo), altrimenti restituisce *skipped* e l'evento resta `queued` per l'API pull.
* `HttpTransport` (opt-in): richiede `INTEGRATIONS_ALLOW_NETWORK=True` **e** endpoint attivi; firma il
  body con HMAC (`X-Signature`, `X-Timestamp`, `X-Nonce`) usando il segreto letto da
  `WebhookEndpoint.signing_secret_env`.
* Esito: successo → `delivered` (`delivered_at`, `response_code`); errore → `attempts += 1`,
  `next_attempt_at = now + min(60 s × 2^(attempts−1), 6 h)`; dopo `INTEGRATIONS_MAX_ATTEMPTS` (8) →
  `failed`. Dal back-office: "Rimetti in coda" (`requeue_event`) e "Annulla" (`cancel_event`).
* Un'eccezione del trasporto non interrompe il ciclo: viene registrata come errore dell'evento.

## 6. Regola di minimizzazione dei dati (vincolante)

Il payload di un evento contiene **solo**: identificativi (`id`, `uuid`), timestamp ISO-8601, codici di
vocabolario chiuso (`category`, `kind`, `status`, `language`). `sanitize_payload()` rifiuta
(`PayloadRejected`):
* chiavi in denylist (`email`, `phone`, `name`, `first_name`, `last_name`, `full_name`, `contact`,
  `address`, `body`, `notes`, `message`, `description`, `text`, `ip`, `user_agent`, …);
* stringhe > 64 caratteri, con a capo o contenenti `@`;
* valori non scalari (dict/list) e più di 20 chiavi.

Motivazione: Annexe 1 §1.5 (nessuna comunicazione a terzi senza consenso) e master prompt §50. Il
CRM ottiene i dati personali solo tramite un endpoint autenticato dedicato (decisione aperta), con
base giuridica e informativa aggiornate (gate G1).
Anche i webhook in ingresso sono minimizzati: `InboundWebhookLog.payload` conserva solo
`event`, `event_type`, `id`, `external_id`, `object_type`, `object_id`, `status`.

## 7. Sicurezza dei webhook in ingresso

`POST /api/v1/webhooks/<system>/` (CSRF-exempt, solo POST, body ≤ 256 KiB):

| Header | Regola |
|---|---|
| `X-Timestamp` | secondi Unix; tolleranza ±`INTEGRATIONS_WEBHOOK_TOLERANCE_SECONDS` (300) |
| `X-Nonce` | 8–64 caratteri `[A-Za-z0-9_-]`, unico per sistema (replay ⇒ 401 `replay`) |
| `X-Signature` | `sha256=` + HMAC-SHA256(secret, `timestamp + "." + nonce + "." + raw_body`) |

Verifica (`integrations/webhooks.py`): sistema attivo → header ben formati → finestra temporale →
segreto da `os.environ[system.inbound_secret_env]` (impronta opzionale) → confronto in tempo costante
(`hmac.compare_digest`) → nonce mai usato (vincolo unico parziale in DB: robusto anche in concorrenza).
Ogni esito (anche negativo) è loggato in `InboundWebhookLog` e in audit. Un body JSON non valido con
firma valida risponde 400 **senza** consumare il nonce. Codici: `unknown_system`, `malformed_headers`,
`timestamp_out_of_range`, `secret_not_configured`, `invalid_signature`, `replay` (tutti 401),
`invalid_json` (400), `payload_too_large` (413). Risposta positiva: `202 {"data": {"accepted": true, "log_id": n}}`.

Il log accetta e registra: **nessuna elaborazione automatica** del contenuto del webhook è
implementata (decisione aperta §12).

## 8. API v1 — autenticazione, throttling, errori, schema

| Endpoint | Auth | Scope | Note |
|---|---|---|---|
| `GET /api/v1/health/` | no | — | liveness, `{"data": {"status": "ok", "version": "v1", "time": …}}` |
| `GET /api/v1/schema/` | no | — | OpenAPI 3.1 JSON scritto a mano (`integrations/openapi.py`) |
| `GET /api/v1/events/` | Bearer | `events:read` | `?status=queued|delivered|failed|all` (default `queued`), `?since=<ISO con offset>`, `?event_type=`, `?after=<id>` (keyset), `?limit=1..200` (50) |
| `POST /api/v1/events/<uuid>/ack/` | Bearer | `events:ack` | idempotente; 404 se non visibile alla chiave; gli eventi annullati non sono esposti |
| `POST /api/v1/webhooks/<system>/` | HMAC | — | §7 |

* **Autenticazione**: `Authorization: Bearer ile_<prefix>_<segreto>`; la chiave è creata da
  `manage.py create_api_key --name … [--system crm] [--scopes events:read,events:ack]` e stampata **una
  sola volta** (in DB solo `sha256`). Chiave assente/malformata/inattiva/scaduta ⇒ 401 + `WWW-Authenticate`.
* **Scoping**: una chiave legata a un `ExternalSystem` vede gli eventi broadcast (`system` nullo) e
  quelli destinati al suo sistema; una chiave senza sistema vede solo i broadcast. Ack di un evento
  non visibile ⇒ 404 (nessuna divulgazione di esistenza).
* **Throttling**: `core.throttle` con scope `api:<prefix>` (`INTEGRATIONS_API_THROTTLE`, default 120
  richieste/60 s) ⇒ 429 `rate_limited`.
* **Envelope**: successo `{"data": …, "request_id": "…"}` (+ `"pagination": {"limit", "has_more",
  "next_after"}`); errore `{"error": {"code", "message", "request_id"}}`; `Cache-Control: no-store`;
  `request_id` = header `X-Request-ID` (correlazione log/audit).
* **Audit**: ogni chiamata ⇒ `AuditEvent(action="api.<azione>", metadata={status, key_prefix, path, method})`.
* **Versioning**: prefisso `/api/v1/`; modifiche incompatibili ⇒ `/api/v2/` con schema separato.

## 9. Stato di sincronizzazione e mappatura degli id esterni

`ExternalReference` collega qualunque oggetto locale (GenericForeignKey) a un id del sistema esterno:
`link_external_id(system, obj, "CRM-42")` (upsert, `synced`), `external_id_of(system, obj)`,
`mark_sync_error(ref, "…")`. Stati: `pending` (id assegnato ma non confermato), `synced`, `error`
(con `last_error`). Il back-office espone filtro per sistema/stato e ricerca per id esterno.
`accounts.Organisation.external_reference` (campo legacy) può migrare a `ExternalReference` senza
cambiare il contratto.

## 10. Diagrammi di sequenza (testo)

**A. Recueil des besoins → CRM (pull)**
```
Impresa ─POST form─▶ enquiries.view ─save─▶ CompanyNeedsRequest
                                             │ post_save
                                             ▼
                              integrations.signals.on_watched_post_save
                                             │ emit("enquiries.company_needs.created", obj, {category, created_at})
                                             ▼
                                      OutboundEvent[queued]
CRM ─GET /api/v1/events/?status=queued (Bearer)─▶ API ─▶ [{uuid, event_type, object{type,id}, data}]
CRM ─POST /api/v1/events/{uuid}/ack/─▶ API ─▶ OutboundEvent[delivered, acknowledged_at]
CRM ─(futuro) GET /api/v1/objects/{type}/{id}/─▶ dettagli (endpoint da definire, §12)
```

**B. Push tramite trasporto (opzionale)**
```
cron ─manage.py deliver_outbound_events─▶ deliver_pending()
   per evento queued e dovuto: transport.deliver(event, endpoints)
      LoggingTransport → log (DEBUG: delivered | prod: skipped, resta queued)
      HttpTransport (opt-in) → POST url firmato → 2xx: delivered | errore: retry con backoff
```

**C. Webhook in ingresso (CRM → piattaforma)**
```
CRM ─POST /api/v1/webhooks/crm/ + X-Timestamp/X-Nonce/X-Signature─▶ verify()
   ok → InboundWebhookLog[valid] + AuditEvent(webhook.received) → 202
   ko → InboundWebhookLog[invalid, error] + AuditEvent(webhook.rejected) → 401/400/413
```

**D. Forum Virtuale → CRM**
```
Utente ─POST /forum-virtuel/rejoindre/─▶ community.services.request_membership
   → ConsentRecord(COMMUNITY) → Membership[pending] → EmailOutbox(contact@agamieuromed.org)
   → emit("community.membership.requested", membership, {category, created_at})
Moderatore ─admin: Approva─▶ approve_membership → emit("community.membership.approved", …)
```

## 11. Configurazione (settings da aggiungere in `config/settings/base.py` — richiesta al team core)

```python
INTEGRATIONS_TRANSPORT = env("INTEGRATIONS_TRANSPORT", default="integrations.transports.LoggingTransport")
INTEGRATIONS_ALLOW_NETWORK = env.bool("INTEGRATIONS_ALLOW_NETWORK", default=False)  # mai True senza DPA
INTEGRATIONS_API_THROTTLE = {"limit": 120, "window_seconds": 60}
INTEGRATIONS_WEBHOOK_TOLERANCE_SECONDS = 300
INTEGRATIONS_MAX_ATTEMPTS = 8
INTEGRATIONS_MAX_BACKOFF_SECONDS = 6 * 3600
INTEGRATIONS_HTTP_TIMEOUT_SECONDS = 10
INTEGRATIONS_MAX_WEBHOOK_BODY_BYTES = 256 * 1024
INTEGRATIONS_API_PAGE_LIMIT = 200
COMMUNITY_POST_THROTTLE = {"limit": 10, "window_seconds": 600}
COMMUNITY_REPORT_THROTTLE = {"limit": 5, "window_seconds": 600}
COMMUNITY_JOIN_THROTTLE = {"limit": 3, "window_seconds": 600}
COMMUNITY_TRUSTED_POST_THRESHOLD = 3
COMMUNITY_MAX_POST_LENGTH = 8000
FORMS_URLFIELD_ASSUME_HTTPS = True  # facoltativo: rimuove la deprecazione Django 6.0 a livello globale
```
Tutti i valori hanno già un default sicuro in `integrations/conf.py` e `community/conf.py`: il codice
funziona anche senza queste righe. Variabili d'ambiente attese in produzione (nomi, mai valori nel
repo): `ILE_WEBHOOK_SECRET_<SYSTEM>` (ingresso), `ILE_SIGNING_SECRET_<SYSTEM>` (uscita), da
referenziare nei campi `*_secret_env`.

## 12. Decisioni aperte

| # | Tema | Stato |
|---|---|---|
| 1 | CRM di destinazione (prodotto, hosting UE, DPA art. 28) | `PENDING_CLIENT` — nessun trasporto HTTP attivabile prima (G12) |
| 2 | Endpoint autenticato di lettura dettagli (`GET /api/v1/objects/{type}/{id}/`) con dati personali | da progettare dopo la pubblicazione delle pagine legali (G1) e aggiornamento dell'informativa (Annexe §1.5) |
| 3 | Elaborazione automatica dei webhook in ingresso (es. aggiornare `ExternalReference` da `external_id`) | non implementata: oggi solo log + audit; proposta: handler per `event == "reference.assigned"` |
| 4 | Rotazione chiavi API / segreti | manuale (creare nuova chiave, disattivare la vecchia); `expires_at` disponibile |
| 5 | Retention di `OutboundEvent` consegnati e `InboundWebhookLog` | proposta 24 mesi (coerente con Annexe §1.7) tramite comando di purge da scrivere |
| 6 | Eventi di cambio stato (non solo creazione) per enquiries/forum | richiede chiamata `emit()` dai service layer di quelle app (opzione B, §3) |
| 7 | DRF + drf-spectacular quando l'API crescerà (ADR-011) | rinviato |
