# Italy Legal Entry™ — piattaforma Django

> **In English.** Italy Legal Entry™ is the multilingual (IT · FR · EN · AR) information and
> orientation platform of the project of the same name, promoted by AGAMI — Dialogo Giuridico
> Interculturale APS: a public website, a reserved area for people, companies and institutions, and
> an editorial back-office, built as a Django 5.2 modular monolith on PostgreSQL 17. This README is
> in Italian, like the rest of `docs/`; the code and its comments are in English.

Italy Legal Entry™ è la piattaforma web del progetto omonimo promosso da **AGAMI — Dialogo Giuridico
Interculturale APS**: un sito pubblico in quattro lingue (italiano, francese, inglese, arabo con RTL
reale) che informa e orienta sui percorsi regolari di mobilità verso l'Italia, un'area riservata per
persone, imprese, università e istituzioni, e un back-office editoriale con workflow di pubblicazione.
Italy Legal Entry **non** è un'autorità pubblica: orienta, informa e accompagna; non rilascia visti,
permessi, autorizzazioni né riconoscimenti di titoli, e nessuna pagina della piattaforma lo lascia
intendere.

## Stato e rami

| Ramo | Contenuto |
|---|---|
| `main` | versione stabile: design V4 (il riferimento di controllo) e documentazione |
| `design-v5` | design V5 in sviluppo; confluisce in `main` solo dopo le revisioni previste |

Lo stato di rilascio e ciò che manca per andare in produzione sono documentati in
`docs/DEPLOYMENT_READINESS.md`, `docs/PREPROD_REPORT.md` e `docs/FINAL_REPORT.md`. Il repository non
contiene credenziali né la configurazione di alcun ambiente di esercizio: tutto ciò che è specifico
di un server arriva dal suo ambiente (vedi *Deployment*).

## Architettura

Monolite Django **modulare**, **server-rendered** con *progressive enhancement*
(`docs/ARCHITECTURE_DECISION_RECORDS/ADR-009-server-rendered-progressive-enhancement.md`): HTML
generato dal server, CSS con design token, ES modules vanilla, nessuna SPA e nessun microservizio.
Dettagli e motivazioni in `docs/ARCHITECTURE.md` e negli ADR.

### Stack

| Livello | Scelta |
|---|---|
| Runtime | Python 3.13 · **Django 5.2 LTS** |
| Database | **PostgreSQL 17** (in sviluppo tramite `docker compose`) — nessun percorso SQLite, per scelta |
| Static | WhiteNoise (manifest + compressione) · font e immagini self-hosted, nessun CDN |
| Sicurezza | django-csp 4 (CSP `self`-only), header aggiuntivi, HSTS e redirect HTTPS in produzione |
| Account | django-allauth 65 (e-mail, verifica, rate limit, MFA TOTP) |
| Back-office | django.contrib.admin + django-unfold |
| Frontend | template Django, CSS con token, ES modules; bundle con esbuild |
| Test e qualità | pytest + pytest-django + freezegun + Playwright · ruff · bandit · pip-audit |

### Le app in breve

Ventotto app Django sotto `apps/`, raggruppate per responsabilità.

| Gruppo | App | Che cosa fa |
|---|---|---|
| Fondamenta | `core` | orologio di riferimento, feature flag e gate di pubblicazione, throttle dei form, honeypot, hashing degli IP, request-id, header di sicurezza, registro dei seed |
| | `cms` | registro dei testi bloccati (con checksum sha256), scanner delle formulazioni vietate, workflow di pubblicazione, stato delle traduzioni, menu, banner, hero, libreria immagini con licenze, redirect dagli URL precedenti |
| | `accounts` | utente custom (login con e-mail), organizzazioni, ruoli (RBAC), policy a livello di oggetto *deny by default*, integrazione allauth e secondo fattore |
| | `consents` | testi di consenso versionati, registrazioni di consenso, newsletter con doppio opt-in |
| | `audit` | audit trail *append-only* |
| | `notifications` | outbox e-mail e scadenze (`send_queued_emails`, `notifications_scan_deadlines`) |
| | `integrations` | confine verso il CRM: identificativi esterni, eventi idempotenti, webhook, API v1 minimale |
| Sito pubblico | `pages` | home, progetto, AGAMI, rete, contatti, anti-frode |
| | `legal` | le cinque pagine legali ufficiali in italiano, pubblicabili solo con il testo ufficiale |
| | `ecosystem` | spazi Imprese · Istituzioni · Università · Progetto pilota |
| | `enquiries` | form pubblici (raccolta dei fabbisogni, proposte di collaborazione, contatto) |
| | `pathways` | Espace Personnes: percorsi regolari, titoli di studio, formazione |
| | `orientation` | questionario di orientamento su un rule engine versionato (`validate_ruleset`, `activate_ruleset`, import/export) |
| | `forum` | Forum Vénétie–Maroc: evento, iscrizioni, programma, modalità «Forum permanente» e governance |
| | `community` | Forum Virtuale (dietro feature flag) |
| | `news` · `faq` · `glossary` · `living` | contenuti editoriali: attualità, FAQ, glossario, «Vivre en Italie» |
| | `partners` | partner e istituzioni; loghi pubblicati solo se autorizzati |
| Area riservata | `portal` | Espace réservé: dashboard, «Ma situation», messaggi |
| | `cases` | fascicoli digitali e le loro pagine |
| | `documents` | documenti privati: upload validato, scansione, download solo autorizzato |
| | `companies` | spazio impresa e fabbisogni |
| | `selection` | selezione autorizzata |
| | `helpdesk` | sportello digitale |
| | `academy` | formazione |
| | `rules` | regole giuridiche **come dati**: grammatica JSON chiusa (nessun `eval`), approvazione a quattro occhi, finestre di validità, snapshot dell'intero ruleset e replay |

Tre scelte che si incontrano ovunque nel codice: l'autorizzazione vive **nel queryset** (la policy
sull'oggetto è la seconda difesa); ciò che il chiamante non può vedere risponde **404, mai 403**; un
fatto assente rende una condizione di regola **falsa, mai vera**.

## Requisiti

- **Python 3.13** (`pyproject.toml` dichiara `>= 3.12`; il `Dockerfile` e la CI usano 3.13)
- **Docker** (Docker Desktop o Docker Engine) per PostgreSQL 17 tramite `docker compose`
- **Node.js 18 o successivo** (LTS consigliata), solo per ricostruire i bundle del frontend
- Git

Nei comandi che seguono `python` è l'interprete del virtualenv (`.venv/Scripts/python` su Windows,
`.venv/bin/python` su Linux e macOS).

## Avvio in sviluppo

1. **Clona** il repository ed entra nella cartella.
2. **Virtualenv e dipendenze** (quelle di sviluppo includono quelle di runtime):
   `python -m venv .venv`, poi `python -m pip install -r requirements/dev.txt`.
3. **Database**: `docker compose up -d db` avvia PostgreSQL 17 su `127.0.0.1:5439` (porta scelta per
   non collidere con altre istanze locali; `up`, non `start`, perché il compose alza anche il
   limite di connessioni).
4. **Configurazione**: `cp .env.example .env`. I valori di esempio bastano per lo sviluppo; il file
   `.env` è ignorato da git.
5. **Schema**: `python manage.py migrate`.
6. **Contenuti**: `python manage.py seed_all` esegue ogni seed registrato, idempotente — testi
   bloccati, flag, menu, record iniziali; `python manage.py seed_legal_rules` scrive le regole
   giuridiche iniziali come *candidate* (idempotente; **nessuna** entra in vigore, vedi *Regole
   giuridiche*). I seed che creano *persone* sintetiche (account dimostrativi, fascicoli,
   richieste) partono solo se `ILE_SEED_DEMONSTRATION_DATA` è attivo (default: `DJANGO_DEBUG`);
   le impostazioni di test e di produzione lo fissano a spento. Un'impresa dimostrativa si crea
   con `python manage.py companies_demo` (solo dove quei dati sono ammessi).
7. **Accesso al back-office**: `python manage.py createsuperuser` (chiede e-mail e password: l'utente
   non ha username).
8. **Server**: `python manage.py runserver`.

Sito: <http://127.0.0.1:8000/> (redirect alla lingua: `/fr/`, `/it/`, `/en/`, `/ar/`). Back-office:
<http://127.0.0.1:8000/backoffice/>. Health check: `/healthz/`. In sviluppo il backend e-mail è la
**console**: nessuna e-mail reale parte dalla macchina.

<details>
<summary>Gli stessi passi, riga per riga (Git Bash e PowerShell)</summary>

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements/dev.txt   # Linux/macOS: .venv/bin/python
docker compose up -d db
cp .env.example .env
export PYTHONIOENCODING=utf-8
.venv/Scripts/python manage.py migrate
.venv/Scripts/python manage.py seed_all
.venv/Scripts/python manage.py seed_legal_rules
.venv/Scripts/python manage.py createsuperuser
.venv/Scripts/python manage.py runserver
```

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements\dev.txt
docker compose up -d db
Copy-Item .env.example .env
$env:PYTHONIOENCODING = "utf-8"
.\.venv\Scripts\python manage.py migrate
.\.venv\Scripts\python manage.py seed_all
.\.venv\Scripts\python manage.py seed_legal_rules
.\.venv\Scripts\python manage.py createsuperuser
.\.venv\Scripts\python manage.py runserver
```

</details>

**Docker completo (opzionale)**: `docker compose --profile full up --build` avvia `db` + `web`
(migrate → seed_all → runserver su `127.0.0.1:8000`, con il `.env` locale). Il `Dockerfile` produce
l'immagine gunicorn di riferimento; `docker-compose.staging.yml` è lo stack *staging-like* usato per
le misure di `docs/STAGING_PERFORMANCE.md`, con un database proprio.

## Variabili d'ambiente

`.env.example` elenca **ogni** variabile letta da `config/settings/base.py` e `prod.py`, con valori di
esempio innocui; `tests/test_env_example_is_complete.py` lo verifica in entrambe le direzioni (nulla
di letto manca, nulla di dichiarato è ignorato). In sintesi:

| Variabile | Scopo |
|---|---|
| `DJANGO_SETTINGS_MODULE` | `config.settings.dev` (default di `manage.py`), `.test` (pytest), `.prod` |
| `ILE_READ_ENV_FILE` | se leggere `.env`. Default sì, **tranne con le impostazioni di produzione**, dove il file è ignorato: un `.env` di sviluppo copiato su un server non indebolisce la configurazione, la *soddisfa* |
| `DJANGO_SECRET_KEY` · `DJANGO_ALLOWED_HOSTS` · `DJANGO_CSRF_TRUSTED_ORIGINS` | **obbligatorie in produzione, senza default**: `prod.py` non si avvia se una manca. La chiave deve avere almeno 50 caratteri e 5 distinti |
| `DJANGO_DEBUG` | debug (spento in test e produzione) |
| `DATABASE_URL` · `DB_CONN_MAX_AGE` | connessione PostgreSQL e durata del riuso (0 in sviluppo: `runserver` apre un thread per socket) |
| `REDIS_URL` | cache opzionale; vuoto = cache in memoria locale |
| `SECURE_SSL_REDIRECT` · `SECURE_HSTS_SECONDS` · `ILE_ALLOW_INSECURE_PROD` | irrigidimento TLS; in produzione i default sono già quelli giusti e `prod.py` rifiuta valori più deboli, salvo l'escape hatch esplicito |
| `BACKOFFICE_MFA_ENFORCED` | secondo fattore (TOTP) per chi legge i dati di altre persone; spento in locale, acceso per default in produzione |
| `IP_HASH_SALT` | sale dell'hash a senso unico degli IP: nessun indirizzo è mai registrato in chiaro |
| `EMAIL_BACKEND` · `EMAIL_HOST` · `EMAIL_PORT` · `EMAIL_HOST_USER` · `EMAIL_HOST_PASSWORD` · `EMAIL_USE_TLS` · `DEFAULT_FROM_EMAIL` | posta in uscita (console in sviluppo) |
| `NOTIFICATIONS_SEND_IMMEDIATELY` | invio durante la richiesta invece dell'outbox; comodo in sviluppo, sbagliato in produzione |
| `PUBLIC_CONTACT_EMAIL` · `FORMS_DESTINATION_EMAIL` | contatto pubblico e unica destinazione di tutti i form |
| `ILE_REFERENCE_DATE` | data di riferimento (ISO) per collaudare i gate datati; vuoto = orologio reale |
| `ILE_VERSION_LABEL` | etichetta di versione nel piè di pagina e nel back-office |
| `PRIVATE_MEDIA_ROOT` | cartella dei documenti privati, **fuori dalla radice web**; ogni download passa da una vista autorizzata |
| `ILE_SEED_DEMONSTRATION_DATA` | se un seed può inventare persone (vedi sopra) |
| `DOCUMENT_SCANNER` · `INTEGRATIONS_TRANSPORT` | agganci opzionali: scanner degli upload e trasporto degli eventi CRM (il default scrive solo nei log) |

Solo sviluppo e test, lette fuori da `config/settings/base.py`: `TEST_DATABASE_URL`
(`config/settings/test.py`, vedi *Test*), `ILE_SOURCE_DIR` (`scripts/verify_locked_against_source.py`,
cartella dei documenti sorgente **fuori** dal repository), `ILE_CONFIDENTIAL_SENTINELS`
(`tests/security/test_confidential_material.py`, tabella privata degli identificativi del depositante,
**fuori** dal repository: senza, il test dedicato risulta saltato e lo dice), `ILE_QA_PASSWORD` e, sul
ramo `design-v5`, `ILE_DESIGN_PREVIEW` e `ILE_DESIGN_PREVIEW_DB_CEILING` (vedi *Anteprima di design*).

`ILE_QA_PASSWORD` è **solo locale**: la password dei tre account QA sintetici che
`scripts/qa_prepare_env.py` crea nel database QA (e degli account dimostrativi dello sportello,
`apps/helpdesk/seeds.py`). Vive nel `.env` locale o nella shell, mai nel repository, mai su un
server; lo script non la stampa e si rifiuta di partire se è vuota. Nessun modulo di
`config/settings` la legge, di proposito: una password non diventa un'impostazione che una pagina
d'errore potrebbe mostrare.

## Migrazioni

`python manage.py migrate` applica lo schema. Ogni modifica a un modello deve avere la sua
migrazione: `tests/test_migration_drift.py` esegue `makemigrations --check --dry-run` su **tutte** le
app (anche una `choices` riformulata fa derivare lo stato del modello senza toccare una colonna), e
la CI lo ripete. Per verificarlo a mano:

```bash
python manage.py makemigrations --check --dry-run
```

## Test

La suite gira su PostgreSQL (il servizio `db` del compose) con `config.settings.test`, impostato in
`pyproject.toml` insieme a `--reuse-db` e `--strict-markers`.

```bash
python -m pytest                       # suite completa
python -m pytest -m "not browser"      # senza i test browser (è ciò che esegue la CI)
python -m pytest -m compliance         # conformità di contenuti e gate
python -m pytest -m security           # regressioni di sicurezza
python -m pytest --create-db           # ricrea il database dei test dopo una nuova migrazione
```

Marker dichiarati: `browser` (Playwright, Chromium), `compliance`, `security`.

**Test browser** (marker `browser`: `tests/frontend/test_browser.py`, `tests/i18n/test_rtl_browser.py`,
i `test_browser.py` di alcune app). Richiedono Chromium di Playwright (`python -m playwright install
chromium`) e **saltano** se manca; usano `live_server` di pytest-django, non un server avviato a
mano. Le catture PNG che producono (per esempio in `docs/qa/rtl/`) sono ignorate da git: sotto
`docs/qa/` restano versionati solo i report JSON e HTML. Gli script `scripts/qa_*.py` guidano invece
un server già in esecuzione (avviato con `--noreload`: il ricaricatore interrompe le connessioni a
ogni salvataggio) su un database QA separato, preparato da `scripts/qa_prepare_env.py` e mai
coincidente con quello di sviluppo; gli script `scripts/qa_chrome_*.py` leggono l'indirizzo del
server da `ILE_QA_BASE`.

**Database dei test.** `config/settings/test.py` legge `TEST_DATABASE_URL` (default: il database di
sviluppo, da cui Django deriva `test_ile`). Due esecuzioni pytest **contemporanee** sullo stesso
database si bloccano a vicenda: assegnare a ciascuna il proprio.

```bash
TEST_DATABASE_URL=postgres://ile:ile-dev-password@127.0.0.1:5439/ile_t_mia python -m pytest -m "not browser"
```

**Qualità e sicurezza**:

```bash
python -m ruff check . && python -m ruff format --check .
python -m bandit -c pyproject.toml -r apps config
python -m pip_audit -r requirements/base.txt
python scripts/verify_locked_against_source.py        # richiede ILE_SOURCE_DIR
```

Verifica delle impostazioni di produzione senza un server (la chiave usa e getta deve superare i
controlli di `prod.py`):

```bash
DJANGO_SETTINGS_MODULE=config.settings.prod \
DJANGO_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(50))')" \
DJANGO_ALLOWED_HOSTS=localhost DJANGO_CSRF_TRUSTED_ORIGINS=https://localhost \
python manage.py check --deploy
```

**CI.** `.github/workflows/ci.yml` esegue, su ogni push e pull request verso `main` e `design-v5`:
`manage.py check`, `makemigrations --check --dry-run`, `ruff check` e `pytest -m "not browser"` su
Python 3.13 con un servizio PostgreSQL 17 usa e getta (le credenziali di sviluppo del compose) e
segnaposto dichiarati per le tre variabili obbligatorie in produzione. Nessun segreto, nessun
deployment, nessun test browser.

## Build del frontend

Le sorgenti stanno in `static/js/src/` e `static/css/` (più i fogli di stile di ciascuna app in
`apps/<app>/static/`); i bundle in `static/js/dist/` e `static/css/dist/` sono prodotti da esbuild
(`scripts/build_frontend.mjs`, `scripts/build_css.mjs`).

```bash
npm ci
npm run build          # build:js + build:css, minificati
npm run watch:js       # ricostruzione al salvataggio, con sourcemap (mai versionate)
npm run watch:css
```

**I bundle sono versionati**, perché il server di produzione esegue `collectstatic`, non Node: ciò
che il browser riceve deve essere già nel repository. Dopo una modifica alle sorgenti si ricostruisce
e si committa il risultato; `tests/frontend/test_frontend_bundle_is_current.py` e
`tests/frontend/test_css_bundle_is_current.py` rifiutano un bundle più vecchio delle sue sorgenti o
che ha perso qualcosa che le sorgenti definiscono. Il JS è caricato come ES module (`type="module"`),
niente è inlined nei template: la CSP resta `script-src 'self'`.

## Anteprima di design (solo sviluppo)

Con `DJANGO_DEBUG=1` le impostazioni di sviluppo montano la vetrina del design system su `/_design/`
e le pagine d'errore su `/_errors/400/`, `/_errors/403/`, `/_errors/404/`, `/_errors/500/`
(`config/urls.py`, dentro il blocco `DEBUG`: con il debug spento quel codice non è nemmeno
importato). Sul ramo `design-v5`, in aggiunta, `ILE_DESIGN_PREVIEW=1` insieme a `DEBUG` monta l'hub di
anteprima V5; la variabile esiste solo in `config/settings/dev.py`, mai in `test.py` né in `prod.py`,
e `ILE_DESIGN_PREVIEW_DB_CEILING` limita le connessioni al database che quel server può aprire.
L'anteprima risponde solo alle richieste il cui `Host` è `127.0.0.1` o `localhost` sulla propria
porta: è pensata per la macchina di chi sviluppa e non va esposta da un server.

## Deployment — cenni

Il modulo di produzione è `config.settings.prod`. Due guardrail:

- **non si avvia** senza `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS` e `DJANGO_CSRF_TRUSTED_ORIGINS`,
  che non hanno default, e ignora `.env` (salvo `ILE_READ_ENV_FILE=1`): la configurazione viene
  dall'ambiente del processo;
- **rifiuta una configurazione indebolita** — redirect HTTPS spento, HSTS sotto un anno, chiave
  corta o poco varia, secondo fattore disattivato — salvo `ILE_ALLOW_INSECURE_PROD=1`, l'unico escape
  hatch, da mettere a verbale quando si usa.

Il resto è Django ordinario: gunicorn (`config.wsgi:application`) dietro un reverse proxy che
termina TLS e passa `X-Forwarded-Proto`, `collectstatic` servito da WhiteNoise, `PRIVATE_MEDIA_ROOT`
su disco fuori dalla radice web, PostgreSQL 17, e i comandi periodici (`send_queued_emails`,
`deliver_outbound_events`, `notifications_scan_deadlines`, `purge_expired_submissions`,
`documents_purge_expired`, `purge_orientation_sessions`). Topologia di riferimento, checklist e stato
in `docs/DEPLOYMENT.md` e `docs/DEPLOYMENT_READINESS.md`. Questo repository non descrive alcuna
infrastruttura specifica.

## Struttura del repository

```
config/            settings (base/dev/test/prod), urls, wsgi/asgi
apps/              le ventotto app (tabella sopra), ciascuna con modelli, viste, template, static, tests
templates/         base, partials, components, errori
static/            css (token e fogli sorgente), js/src e js/dist, img, fonts, brand
locale/            cataloghi it/fr/en/ar (.po e .mo)
tests/             conftest, suite trasversali: compliance, security, frontend, i18n, backoffice
scripts/           build del frontend, lock e verifica dei testi, audit i18n, QA browser, scansione della storia
requirements/      base.txt (runtime, pinnato) e dev.txt (test e qualità)
docs/              documentazione di progetto (indice sotto)
.github/workflows  CI
```

## Fasi, gate e testi bloccati

Il progetto è stato consegnato in tre fasi (Fase 1 entro il 17/09/2026, Fase 2 entro il 25/09/2026,
Fase 3 dal 02/10/2026; `docs/IMPLEMENTATION_PHASES.md`). I gate sono meccanismi reali
(`apps/core/gates.py`, `apps/core/flags.py`), non note a margine:

| Flag / gate | Effetto |
|---|---|
| pagine legali pubblicate (G1) | senza il testo ufficiale italiano i form pubblici e la registrazione degli account restano **chiusi** (G2) |
| `forms_override_without_legal` | apertura amministrativa esplicita dei form, tracciata in audit (sconsigliata) |
| `phase3_public` | contenuti di Fase 3 visibili solo con il flag **e** la data ≥ 02/10/2026 |
| `forum_banner` | banner del Forum in home fino al 02/10/2026 |
| `forum_permanent_mode` | pagina Forum in modalità «Forum Permanent» dopo l'evento |
| `virtual_forum` | Forum Virtuale (dopo il Forum in Marocco, 29–30/10/2026) |
| `newsletter` | blocco newsletter con consenso separato e revocabile |
| `reserved_area_public_link` | link secondario all'area riservata |
| `analytics` | astrazione per analytics rispettosi della privacy — **non attiva** |

Dettaglio dei gate G0–G12 in `docs/LEGAL_AND_PUBLICATION_GATES.md`.

**Testi bloccati.** I testi prescritti dal documento di implementazione vivono in
`apps/cms/locked_content.py` (chiavi `p1.*`, `p2.*`, `p3.*`, `legal.*`) e sono resi nei template solo
tramite `{% locked "chiave" %}`. `apps/cms/locked_content.sha256.json` ne fissa i checksum;
`scripts/lock_content.py` li rigenera (solo dopo una trasmissione ufficiale) e
`scripts/verify_locked_against_source.py` dimostra che ogni frammento è una sottostringa dei
documenti sorgente, che stanno **fuori dal repository** (`ILE_SOURCE_DIR`).
`tests/compliance/test_locked_content.py` fallisce a ogni deriva.

**Regole giuridiche.** Nessuna regola è in vigore finché un giurista non l'ha approvata:
`python manage.py rules_pending_review --strict` elenca quelle in attesa (ed esce con 1), e la pagina
di valutazione lo dichiara. `rules_activate_demonstration` attiva le regole **solo** in modalità
dimostrativa, marcandole come tali.

## Riservatezza e dati personali

- Il materiale sorgente del committente (documenti, estrazioni, immagini) **non entra nel
  repository**: `.gitignore` lo esclude e `tests/security/test_confidential_material.py` e
  `tests/compliance/test_no_personal_data_in_repository.py` fanno fallire la suite se compare.
  Policy: `docs/security/CONFIDENTIAL_MATERIAL_POLICY.md`.
- La storia git è stata riscritta il 21 settembre 2026 per rimuovere materiale che non doveva
  esserci (`docs/security/HISTORY_REWRITE_2026-09-21.md`, `docs/security/HISTORY_SCAN_AFTER.md`);
  `scripts/history_secret_scan.py` esamina ogni blob di ogni ref.
- Gli indirizzi IP sono registrati solo come hash salato; i documenti privati non sono mai sotto
  `MEDIA_ROOT`; i seed non inventano persone dove ci sono dati reali.
- Accessibilità (obiettivo WCAG 2.2 AA), i18n/RTL e protezione dei dati sono documentati in
  `docs/ACCESSIBILITY.md`, `docs/I18N_RTL.md`, `docs/PRIVACY_BY_DESIGN.md` e `docs/SECURITY.md`;
  ciò che richiede una verifica umana è elencato in `docs/HUMAN_QA_CHECKLIST.md`.

## Documentazione

| File | Contenuto |
|---|---|
| `docs/ARCHITECTURE.md` · `docs/ARCHITECTURE_DECISION_RECORDS/` | architettura e ADR |
| `docs/AGENT_CONVENTIONS.md` | convenzioni di sviluppo vincolanti |
| `docs/REQUIREMENTS_MATRIX.md` | matrice dei requisiti (sorgente, fase, implementazione, test, stato) |
| `docs/CONTENT_SOURCE_MAP.md` | mappa dei testi bloccati e delle formulazioni vietate |
| `docs/LEGAL_AND_PUBLICATION_GATES.md` · `docs/IMPLEMENTATION_PHASES.md` | gate G0–G12, milestone, definition of done |
| `docs/platform/` | architettura informativa della piattaforma, ciclo di vita del fascicolo, governance del rule engine, journey per ruolo |
| `docs/DESIGN_SYSTEM.md` · `docs/design-v4/` · `docs/design-v5/` | design system e le sue versioni |
| `docs/ACCESSIBILITY.md` · `docs/I18N_RTL.md` | accessibilità, i18n e RTL |
| `docs/SECURITY.md` · `docs/PRIVACY_BY_DESIGN.md` · `docs/security/` | sicurezza, protezione dei dati, permessi, materiale riservato, storia del repository |
| `docs/CRM_INTEGRATION_CONTRACT.md` | contratto di integrazione CRM |
| `docs/IMAGE_LICENSES.md` | licenze di immagini e font |
| `docs/CURRENT_SITE_AUDIT.md` · `docs/URL_MIGRATION_MAP.md` | audit del sito precedente e mappa dei redirect |
| `docs/DEPLOYMENT.md` · `docs/DEPLOYMENT_READINESS.md` · `docs/STAGING_PERFORMANCE.md` | preparazione del deployment, prontezza, misure di staging |
| `docs/QA_REPORT.md` · `docs/PREPROD_REPORT.md` · `docs/FINAL_REPORT.md` · `docs/HUMAN_QA_CHECKLIST.md` | report di QA, pre-produzione e finale; verifiche umane richieste |

## Licenza

Il repository **non contiene** al momento un file di licenza: `package.json` dichiara `UNLICENSED` e
`pyproject.toml` non indica una licenza. La scelta spetta al titolare del progetto; fino ad allora il
codice è pubblicato **senza licenza**, e in assenza di una licenza non va presunto alcun permesso di
riuso. I componenti di terze parti restano sotto le rispettive licenze: le dipendenze Python in
`requirements/`, quelle Node in `package.json`, i font IBM Plex (SIL Open Font License 1.1) e le
fotografie, ciascuna registrata con provenienza e licenza in `docs/IMAGE_LICENSES.md`.
