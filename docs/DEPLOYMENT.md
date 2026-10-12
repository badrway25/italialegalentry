# Deployment — preparazione (NON ESEGUITO)

> **Nessun deployment è stato effettuato.** Questo documento prepara la fase successiva, che avverrà solo su
> istruzione esplicita del committente. Nessuna modifica a DNS, hosting, database o caselle di produzione.

## 1. Topologia di riferimento

```
Internet ──TLS──▶ reverse proxy (nginx/Caddy: terminazione TLS, HTTP/2, compressione, rate limit L7)
                       │  X-Forwarded-Proto: https, X-Forwarded-Host
                       ▼
                 gunicorn (config.wsgi:application, 3–5 worker sync) ── PostgreSQL 17 (UE)
                       │
                       ├─ static: WhiteNoise (manifest, cache immutabile 1 anno) — nessun CDN esterno deciso
                       ├─ media pubblica (immagini CMS): MEDIA_ROOT servita dal proxy in sola lettura
                       ├─ PRIVATE_MEDIA_ROOT: disco FUORI dal web root, letto solo da Django (documents)
                       └─ cron: send_queued_emails (ogni 1–5 min), purge retention (giornaliero, dry-run → apply)
```

Opzioni: immagine Docker (`Dockerfile`, base `python:3.13-slim`, gunicorn) + `docker compose --profile full`
come riferimento; nessun provider cloud scelto. Redis è **opzionale** (`REDIS_URL`) per cache/throttle
condivisi tra più worker: con un solo host e LocMem il throttle è per-processo (documentato come limite).

## 2. Variabili d'ambiente

Base (`.env.example`):

| Variabile | Valore in produzione |
|---|---|
| `DJANGO_SETTINGS_MODULE` | `config.settings.prod` |
| `DJANGO_SECRET_KEY` | segreto lungo, generato, mai nel repo (obbligatorio: nessun default) |
| `DJANGO_DEBUG` | `0` |
| `DJANGO_ALLOWED_HOSTS` | `legalitalentry.it,www.legalitalentry.it` (obbligatorio) |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | `https://legalitalentry.it,https://www.legalitalentry.it` (obbligatorio) |
| `DATABASE_URL` | `postgres://user:pass@host:5432/ile` (server UE) |
| `REDIS_URL` | opzionale |
| `EMAIL_BACKEND` | `django.core.mail.backends.smtp.EmailBackend` (solo dopo autorizzazione all'invio reale) |
| `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `EMAIL_USE_TLS` | SMTP del titolare |
| `DEFAULT_FROM_EMAIL` | mittente autorizzato (nessun `@legalitalentry.it` finché le caselle non sono attivate) |
| `PUBLIC_CONTACT_EMAIL`, `FORMS_DESTINATION_EMAIL` | `contact@agamieuromed.org` |
| `IP_HASH_SALT` | segreto lungo |
| `PRIVATE_MEDIA_ROOT` | percorso fuori dal web root (es. `/srv/ile/private_media`) |
| `SECURE_SSL_REDIRECT` | `1` |
| `SECURE_HSTS_SECONDS` | `31536000` |
| `NOTIFICATIONS_SEND_IMMEDIATELY` | `0` (invio via cron) oppure `1` |
| `ILE_VERSION_LABEL` | es. `v2.0.0 — Fase 1` (aggiornare a ogni fase, come richiesto dal documento) |
| `ILE_REFERENCE_DATE` | vuoto (ignorato quando `DEBUG=0`) |

Da aggiungere ai settings in Stage 1/3 (richieste degli agent): `BACKOFFICE_MFA_ENFORCED=1`,
`DOCUMENT_SCANNER` (dotted path), `INTEGRATIONS_TRANSPORT`.

## 3. Checklist pre-deploy

1. `git status` pulito sul tag di release; `docs/QA_REPORT.md` con stato `CONDITIONALLY_READY` o superiore.
2. `manage.py check --deploy` con settings prod → nessun warning non giustificato.
3. `manage.py makemigrations --check --dry-run` → nessuna migrazione mancante.
4. `pip-audit -r requirements/base.txt` e `bandit -c pyproject.toml -r apps config` → nessuna vulnerabilità aperta.
5. Suite completa `pytest` verde (incluse `-m compliance` e `-m security`).
6. `manage.py collectstatic --noinput` (manifest WhiteNoise).
7. Backup del database esistente (se presente) — `pg_dump -Fc`.
8. **Conferma scritta dell'hosting UE** (prestatore + localizzazione) registrata in `SiteSettings`
   (`hosting_provider`, `hosting_location`) e nel documento del titolare (richiesta §1.4).
9. Stato delle pagine legali: se l'Allegato 1 IT non è ancora pubblicato, i form restano chiusi (gate G2) — il
   documento §1.4 lo prescrive espressamente; **non** attivare `forms_override_without_legal`.
10. Feature flag coerenti con la data:
    - **prima del 02/10/2026**: `forum_banner` on (scade automaticamente il 02/10), `phase3_public` off
      (`enabled_from` = 02/10/2026, attivazione solo con autorizzazione scritta), `forum_permanent_mode` off,
      `virtual_forum` off, `newsletter` off;
    - **dal 02/10/2026 (autorizzazione ricevuta)**: `phase3_public` on, `forum_permanent_mode` on dopo le 18:00
      di Rovigo, `virtual_forum` on solo dopo il Forum in Marocco (29–30/10/2026).
11. `manage.py seed_all` eseguito (idempotente).
12. Superuser creato con MFA TOTP attivata; ruoli assegnati agli editor (`role:staff`, `role:administrator`).

## 4. Rilascio

```
1. tag git (es. v2.0.0-phase1)
2. build immagine / pull sul server; installare requirements/base.txt
3. migrate --noinput
4. collectstatic --noinput
5. seed_all
6. riavvio gunicorn (graceful) e verifica /healthz/ → {"status":"ok","database":true}
7. smoke test §7
```

Rollback: ridistribuire il tag precedente; le migrazioni sono additive (nessun rollback di schema previsto senza
analisi); ripristino DB da `pg_dump` in caso di corruzione.

## 5. Backup e ripristino

- `pg_dump -Fc ile > ile_YYYYMMDD.dump` giornaliero, conservazione secondo policy del titolare, cifratura a riposo.
- `PRIVATE_MEDIA_ROOT` e `MEDIA_ROOT` inclusi nel backup (contengono dati personali → stessa protezione del DB).
- Ripristino: `pg_restore -d ile ile_YYYYMMDD.dump`, poi `migrate` e verifica `/healthz/`.

## 6. Monitoraggio e log

- Log strutturati JSON su stdout (gunicorn → journald/file), correlati da `X-Request-ID`.
- `/healthz/` (DB check) per il monitor esterno; `/robots.txt` e `/sitemap.xml` generati dall'app.
- Nessun servizio SaaS di error tracking collegato: l'astrazione è pronta ma disattivata (privacy).
- Metriche minime da osservare: errori 5xx, tempi di risposta, coda `EmailOutbox` in stato `failed`, eventi
  `audit` anomali (throttle superati, download negati).

## 7. Verifica post-deploy

```
curl -sI https://legalitalentry.it/fr/ | grep -iE "strict-transport|content-security|x-frame|x-content-type|referrer|permissions-policy|x-request-id"
curl -s https://legalitalentry.it/sitemap.xml | head
curl -s https://legalitalentry.it/robots.txt
for l in it fr en ar; do curl -s -o /dev/null -w "$l %{http_code}\n" https://legalitalentry.it/$l/; done
curl -s https://legalitalentry.it/ar/ | grep -o '<html[^>]*>'      # dir="rtl"
```

Controllare inoltre: le 5 pagine legali (200, testo ufficiale IT o avviso di preparazione), form chiusi/aperti
secondo il gate, banner Forum, versione nel footer, nessuna risorsa esterna nel sorgente, login/MFA back-office.

## 8. DNS e cutover (placeholder)

Nessuna modifica è stata fatta. Piano: mantenere il sito WordPress finché il nuovo non è verificato in staging;
switch DNS con TTL ridotto; redirect delle vecchie URL secondo `docs/URL_MIGRATION_MAP.md`; decisione separata
per `app.legalitalentry.it` (attualmente 503 con certificato errato).

## 9. Da confermare dal committente prima del go-live

- Allegato 1 — Testi legali (IT) e autorizzazione a pubblicare la traduzione di cortesia FR.
- Prestatore e localizzazione UE dell'hosting (conferma scritta).
- Attivazione SMTP e mittente; eventuali caselle `@legalitalentry.it`.
- Loghi autorizzati Regione del Veneto e Comune di Rovigo; programma definitivo e nomi dei relatori.
- Versioni IT/EN/AR dei nuovi contenuti.
- Logo del progetto (tagline/porta) oppure conferma del marchio tipografico.
- Data e autorizzazione per l'attivazione dei contenuti Fase 3 e del Forum Virtuale.
- Nomina dei responsabili del trattamento (art. 28) per hosting e gestione tecnica.
