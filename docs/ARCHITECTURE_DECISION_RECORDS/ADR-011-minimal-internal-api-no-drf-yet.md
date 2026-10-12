# ADR-011 — API interna minimale versionata senza DRF (per ora)

**Stato:** accettata

## Decisione
`integrations` espone `/api/v1/` con autenticazione a chiave (hash in DB), throttling, errori JSON coerenti, audit e schema OpenAPI statico, implementata con view Django + `JsonResponse` e serializzatori espliciti nel service layer. Il contratto è in `docs/CRM_INTEGRATION_CONTRACT.md`. Nessun modello è esposto direttamente.

## Motivazione
Il CRM di destinazione non è specificato; l'obiettivo è il boundary (external ids, eventi idempotenti, webhook HMAC), non una REST completa. DRF (+ drf-spectacular) resta la scelta naturale quando l'API crescerà.
