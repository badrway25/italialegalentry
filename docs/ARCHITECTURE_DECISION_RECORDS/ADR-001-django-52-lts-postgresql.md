# ADR-001 — Django 5.2 LTS + PostgreSQL

**Stato:** accettata (2026-09-17)

## Contesto
Al 17/09/2026 PyPI espone Django 6.1.1 (ultima), 6.0.x e 5.2.17 (LTS). Il progetto è una piattaforma istituzionale destinata a durare anni, con dipendenze terze (allauth, unfold, csp) che devono restare compatibili.

## Decisione
Django **5.2 LTS** (security support fino ad aprile 2028) con PostgreSQL 17 come unico database supportato (sviluppo via docker compose, porta 5439 per non collidere con istanze locali su 5432/5434).

## Conseguenze
- Massima compatibilità delle dipendenze e ciclo di patch lungo.
- Migrazione alla prossima LTS (6.2, attesa 2027) pianificabile.
- Alcune novità 6.x (CSP nativo, template partials) non disponibili: CSP fornito da django-csp 4.
