# ADR-007 — Outbox e-mail in database invece di Celery/Redis

**Stato:** accettata

## Decisione
`notifications.EmailOutbox` + comando `send_queued_emails` (cron) e invio immediato opzionale. Nessun broker. Tutti i form scrivono verso `settings.ILE["FORMS_DESTINATION_EMAIL"]` (= contact@agamieuromed.org). In sviluppo backend console: **nessuna e-mail reale**.

## Motivazione
Volumi bassi, requisito di tracciabilità (ogni invio è una riga con stato/tentativi/errore), zero infrastruttura aggiuntiva. Celery/Redis restano un'opzione futura documentata (worker dietro la stessa interfaccia `deliver()`).
