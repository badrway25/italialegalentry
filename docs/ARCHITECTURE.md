# Architettura — Italy Legal Entry™ (piattaforma Django)

Stato: **foundation implementata** (commit `feat: bootstrap`), aggiornato al 2026-09-17.
Decisioni motivate in `docs/ARCHITECTURE_DECISION_RECORDS/`.

## 1. Visione

```
PUBLIC WEBSITE (pages, ecosystem, pathways, forum, news, faq, glossary, living, legal)
        ↓
INFORMATION & ORIENTATION PLATFORM (orientation: rule engine + wizard)
        ↓
AUTHENTICATION (accounts: custom User, RBAC, allauth + MFA)
        ↓
RESERVED AREA (portal) — DOCUMENTS / REQUESTS / PATHWAYS (documents, enquiries, orientation)
        ↓
CRM / EXTERNAL INTEGRATION LAYER (integrations: external ids, outbound events, webhooks, API v1)
        ↓
EVENTS / FORUM (forum) — FORUM VIRTUALE (community, gated)
        ↓
PARTNERS / INSTITUTIONS / ENTERPRISES (partners, accounts.Organisation)
```

Monolite Django modulare, server-rendered, progressive enhancement (ADR-009). Nessun microservizio.

## 2. Stack

| Livello | Scelta | Motivo |
|---|---|---|
| Runtime | Python 3.13, **Django 5.2 LTS** (5.2.17) | LTS con security support fino ad aprile 2028 (ADR-001) |
| Database | **PostgreSQL 17** (docker compose, porta locale 5439) | integrità, JSONB, full-text; SQLite non previsto |
| Static | WhiteNoise (manifest + compressione) | nessun CDN esterno, header immutabili |
| Sicurezza | django-csp 4, SecurityMiddleware, header extra (Permissions-Policy, CORP) | CSP `self`-only: nessuna risorsa terza |
| Account | django-allauth 65 (`account` + `mfa` TOTP/recovery) | verifica e-mail, rate limit, MFA pronti (ADR-006) |
| Back-office | django.contrib.admin + **django-unfold** | UX editoriale moderna senza CMS esterno (ADR-005) |
| Immagini | Pillow (WebP/AVIF derivati) | self-hosting, niente hotlink |
| Frontend | CSS moderno con design token, ES modules vanilla, HTMX opzionale mirato | nessuna SPA (ADR-009) |
| Test | pytest + pytest-django + freezegun + Playwright | piramide unit/integration/browser/compliance |
| Qualità | ruff (lint+format), bandit, pip-audit, `manage.py check --deploy` | |

Dipendenze pin in `requirements/base.txt` (runtime, 9 pacchetti) e `requirements/dev.txt`.

## 3. Mappa delle app (`apps/`)

| App | Responsabilità | Dipende da |
|---|---|---|
| `core` | clock di progetto, feature flag + **gate di pubblicazione**, throttle, honeypot, hashing IP, request-id, header, template tag built-in (`locked`, `flag`, `svg_icon`), `SiteSettings`, registro sitemap/seed/route pubbliche, error pages | — |
| `cms` | **registro testi bloccati** (`locked_content.py` + sha256), scanner formulazioni vietate, `PublishableModel` (draft→review→scheduled→published→archived, versione), `TranslationBase` (status missing/draft/reviewed/approved/published), menu, banner, hero, media library con licenze, redirect | core |
| `accounts` | `User` (e-mail), `Organisation`, `Membership`, `PersonProfile`, **ruoli** (gruppi `role:*`), **policy object-level deny-by-default**, adapter allauth (signup gated), form signup con consenso | core, consents |
| `consents` | testi di consenso versionati, `ConsentRecord` (timestamp, versione testo, IP hash), newsletter double opt-in, revoca | core, cms |
| `audit` | audit trail append-only + mirror dei LogEntry admin | core |
| `notifications` | outbox e-mail (`EmailOutbox`), invio verso l'unica destinazione `contact@agamieuromed.org`, comando `send_queued_emails` | core |
| `legal` | 5 documenti legali ufficiali IT (BLOCKED finché manca l'Allegato 1), versioni immutabili, gate G1 | core, cms |
| `pages` | home (hero interim/Fase 3, banner, 4 accessi, sezioni), progetto/AGAMI/network/contatti, anti-frode, sitemap statica, JSON-LD Organization | tutte le app pubbliche |
| `ecosystem` | Espace Entreprises (Fase 1), Institutions, Universités & Formation, Projet Pilote (diagramma) | enquiries, pathways |
| `enquiries` | form pubblici: Recueil des besoins (Fase 1), proposte istituzioni/università, contatto; anti-spam, throttle, consenso, audit, export CSV | core, consents, notifications |
| `pathways` | Espace Personnes: 8 percorsi regolari (overview, steps, documenti, autorità, avvertenze), diplomi esteri, formazione prima/dopo | cms, orientation |
| `orientation` | rule engine versionato (Ruleset/Question/Choice/Condition/PathwayMapping/Checklist), wizard, sessioni anonime/autenticate, risultati con versione regole + disclaimer | cms, pathways, accounts |
| `forum` | Forum Vénétie–Maroc: evento, programma editabile, ruoli relatori (nomi gated), iscrizioni, partner (loghi gated), media/documenti/accordi/risultati/prossimi appuntamenti, modalità permanente | core, consents, notifications, partners |
| `community` | Forum Virtuale (gated): stanze, discussioni, post, allegati, moderazione, segnalazioni, calendario, iniziative | accounts, documents |
| `news` | Actualités: articoli con workflow, categorie, SEO/social, correlati; blocco newsletter | cms, consents |
| `faq`, `glossary`, `living` | FAQ (categorie, ricerca, FAQPage JSON-LD), glossario (indice, permalink, correlati), fiches "Vivre en Italie" | cms |
| `partners` | partner/istituzioni con loghi **solo se autorizzati** | cms |
| `documents` | upload privato (allowlist MIME/estensioni, nomi casuali, storage fuori da MEDIA_ROOT), download autorizzato, hook antivirus | accounts, audit |
| `portal` | Espace réservé: dashboard, richieste, percorsi, comunicazioni, documenti, scadenze (foundation) | enquiries, orientation, documents |
| `integrations` | contratto CRM: `ExternalReference`, `OutboundEvent` (idempotenza), webhook HMAC, API v1 minimale | core, audit |

Regola: **nessuna logica di business nei template**; le view sono sottili e delegano a `services.py`.

## 4. Meccanismi trasversali

### 4.1 Testi bloccati
`cms.locked_content.get(key, lang)` → `(valore, lingua_effettiva)`; il tag `{% locked "chiave" %}` aggiunge `lang="fr"` quando la lingua corrente non ha versione ufficiale. Le chiavi sono documentate in `docs/CONTENT_SOURCE_MAP.md`. Modifica = nuovo checksum via `scripts/lock_content.py` + revisione git.

### 4.2 Gate
`core.gates`: `legal_pages_available()` (G1), `public_forms_enabled()` (G2), `phase3_public()` (G3, flag **e** data ≥ 2026-10-02), `forum_banner_visible()`, `forum_permanent_mode()`, `virtual_forum_enabled()`, `newsletter_enabled()`. Le view dei form pubblici restituiscono la pagina "form non disponibile" quando G2 è chiuso; il signup allauth è chiuso dallo stesso gate.

### 4.3 Pubblicazione e traduzioni
`PublishableModel.objects.live()` filtra per stato e finestra temporale (`core.clock.now()`); `cms.translation.resolve(obj, lang)` restituisce solo traduzioni `PUBLISHED`, con fallback FR marcato.

### 4.4 Privacy by design
IP mai in chiaro (`core.privacy.hash_ip`), consenso con versione testo e timestamp, retention 24 mesi (dai testi legali), export/cancellazione via admin action (in `enquiries`), audit append-only.

### 4.5 i18n
`i18n_patterns` con prefisso obbligatorio; `LANGUAGE_CODE="fr"` come lingua sorgente/fallback (ADR-004); stringhe UI via gettext (sorgente FR, traduzioni IT/EN/AR nei `.po`); testi bloccati e legali **mai** tradotti automaticamente. RTL: proprietà logiche CSS, `dir` sul root, icone direzionali specchiate semanticamente.

## 5. Sicurezza (sintesi — dettagli in docs/SECURITY.md)
CSRF, template autoescape, ORM, `X-Frame-Options: DENY`, CSP self-only, HSTS/HTTPS redirect in prod, cookie Secure/HttpOnly/SameSite, Argon2/PBKDF2, validatori password (min 12), rate limit login/signup/reset, MFA TOTP, honeypot + throttle sui form, nessun segreto in repo (`.env.example`).

## 6. Sviluppo locale
```
docker compose up -d db
python -m venv .venv && .venv/Scripts/pip install -r requirements/dev.txt
copy .env.example .env
.venv/Scripts/python manage.py migrate && .venv/Scripts/python manage.py seed_all
.venv/Scripts/python manage.py runserver
.venv/Scripts/python -m pytest
```
Percorso Docker completo: `docker compose --profile full up` (web + db).
