# CURRENT IMPLEMENTATION STATE — checkpoint prima del rebase

Rilevato il 20 settembre 2026, ore 21:50 · Questo è il **punto di ripartenza**, non un bilancio finale.

---

## 1. Checkpoint di sicurezza

| | |
|---|---|
| Branch | `main` |
| HEAD | `95002e3` — *fix(rtl): keep list markers of left-to-right fallback items inside mirrored lists; align brand tag test and documented CSS weight* |
| Albero di lavoro | pulito al momento del checkpoint |
| Commit totali | 9 |
| Ultimo commit sostanziale | `729db62` — Stage 2: homepage, spazi dell'ecosistema, area riservata, traduzioni, correzioni di QA browser |

Nessun reset, nessun checkout forzato, nessuna cancellazione. Il lavoro esistente è la base da
verificare e migliorare.

**Cronologia:**

```
95002e3  fix(rtl): list markers, brand tag test, documented CSS weight
729db62  feat(stage2): homepage, ecosystem spaces, reserved area, translations; browser-QA fixes
36ddeae  feat(cms): legacy WordPress URL middleware
a934cd9  fix(security): production guard rails, MFA middleware wiring, hardened JSON-LD escaping
ed5035a  feat(stage1): design system, content apps, forms, forum, orientation, portal foundations
23b6bf1  docs: 11 architecture decision records; core safe_url tag
4fceec9  docs: architecture, ADRs, agent conventions; core public-route registry
de043b9  feat: bootstrap Django 5.2 LTS architecture and foundation apps
26e6eb3  docs: discovery phase — audit, requirements matrix, content map, gates, phases
```

---

## 2. Stack effettivo

| Componente | Scelta | Note |
|---|---|---|
| Linguaggio | Python 3.13.5 | |
| Framework | Django 5.2.17 LTS | Monolite modulare, server-rendered |
| Database | PostgreSQL 17 | Docker, `127.0.0.1:5439`, volume `ile_pgdata` |
| Frontend | Template Django + CSS moderno + JavaScript progressivo | Nessuna SPA, nessun bundler |
| Autenticazione | django-allauth 65.19.4 con modulo MFA | Utente personalizzato, e-mail come identificativo |
| Back-office | django-unfold 0.107 | Su `django.contrib.admin` |
| Sicurezza | django-csp 4, WhiteNoise, middleware propri | CSP self-only sul pubblico |
| i18n | `i18n_patterns` su quattro lingue, catalogo gettext + traduzioni in database | `LANGUAGE_CODE = "fr"` |
| Test | pytest + pytest-django + Playwright | |
| Qualità | ruff, bandit, pip-audit | |

Lo stack è **confermato** contro la proposta Next.js/NestJS del Technical Blueprint: vedere CR-01 in
`docs/source-of-truth/CONFLICT_REGISTER.md` e l'ADR-012.

---

## 3. Dimensioni

| Metrica | Valore |
|---|---|
| App di dominio sotto `apps/` | 22 |
| Modelli | 94 |
| Righe di Python in `apps/` | 44 881 |
| Template HTML | 169 |
| Righe di CSS | 6 175 |
| File di test | 114 |
| Pattern URL | 572, di cui 491 con nome |
| Messaggi tradotti | 1 814 per lingua, quattro lingue, copertura 100 % |
| Documenti in `docs/` | 18 più 11 ADR |

---

## 4. Applicazioni e loro stato

| App | Modelli | Che cosa fa oggi | Maturità |
|---|---|---|---|
| `core` | 2 | Flag, gate, orologio, registro rotte pubbliche, seed, sitemap, link consapevoli dei gate, middleware di sicurezza | **Solida** |
| `cms` | 5 | Registro dei testi vincolati, menu, banner, hero, redirect legacy, middleware URL | **Solida** |
| `accounts` | 4 | Utente personalizzato, profilo persona, organizzazione, appartenenza, ruoli, MFA back-office | **Fondamenta** |
| `consents` | 3 | Testi di consenso versionati, registrazioni, newsletter double opt-in | **Solida** |
| `audit` | 1 | `AuditEvent` | **Fondamenta** |
| `notifications` | 1 | Coda e-mail in uscita | Base |
| `legal` | 2 | Documenti giuridici e versioni, tutti `BLOCKED` | **Gate G1** |
| `pages` | 2 | Home componibile, pagine istituzionali | **Completa** |
| `ecosystem` | 3 | Quattro spazi di pubblico, progetto pilota | **Completa** |
| `enquiries` | 3 | Form pubblici: contatto, fabbisogni, collaborazione | **Gate G2** |
| `pathways` | 9 | Percorsi, passi, documenti, fonti, avvertenze | Contenuto |
| `orientation` | 12 | Questionario dinamico, ruleset v1, esiti, checklist | **Parziale** |
| `forum` | 11 | Evento, programma, interventi, partner, iscrizioni, esiti | **Completa** (parte pubblica) |
| `community` | 11 | Stanze, discussioni, post, moderazione | Non esposta |
| `news` | 3 | Articoli, categorie, traduzioni | Fase 3 |
| `faq` | 4 | Categorie e voci | Fase 3 |
| `glossary` | 2 | Termini | Fase 3 |
| `living` | 4 | Vivere in Italia: temi e schede | Fase 3 |
| `partners` | 2 | Partner con autorizzazione scritta | Gate G6 |
| `documents` | 1 | Documento privato con controllo accessi | **Fondamenta** |
| `portal` | 3 | Area riservata: avvisi, messaggi, scadenze | **Scheletro** |
| `integrations` | 6 | Confine CRM, webhook, chiavi API, eventi | Inerte per costruzione |

---

## 5. Meccanismi che funzionano e vanno conservati

**Registro dei testi vincolati** (`cms/locked_content.py`). Ogni frase prescritta dal committente sta
in un registro con chiave, con un file di hash sha256 e uno script che ne verifica la corrispondenza
verbatim con l'estrazione del PDF sorgente. Il red team ha verificato indipendentemente 236 frammenti:
tutti verbatim. Questo meccanismo è la garanzia contrattuale più importante del progetto.

**Gate e flag** (`core/flags.py`, `core/gates.py`, `core/clock.py`). La Fase 3 richiede flag attivo
**e** data raggiunta. I gate sono valutati lato server, non nascosti nel template. Un URL chiuso
risponde 404, non 403 e non una pagina civetta.

**Link consapevoli dei gate** (`core/links.py`). `public_url()` restituisce stringa vuota se la rotta
non è aperta: il sito non può linkare una pagina che risponderebbe 404.

**Content lock e formulazioni vietate.** Test di compliance impediscono la reintroduzione delle
diciture proibite in ogni lingua, template, seed e catalogo.

**Migrazione degli URL legacy** (`cms/middleware.py`). `?lang=xx` → 301, endpoint WordPress → 410,
tabella di redirect per i 404.

**Sicurezza di produzione.** `config/settings/prod.py` rifiuta di avviarsi senza HTTPS, HSTS di un
anno e una `SECRET_KEY` robusta. `check --deploy` pulito. Bandit senza rilievi alti. pip-audit pulito.

**Isolamento dei test.** `conftest.py` di radice resetta la lingua attiva prima e dopo ogni test,
eliminando i fallimenti dipendenti dall'ordine.

---

## 6. Stato dei test

Ultima esecuzione completa, 20 settembre ore 21:20, su PostgreSQL:

```
1 868 passati · 3 falliti · 27 min 15 s
```

I tre fallimenti sono stati corretti e verificati (commit `95002e3`):

1. Overflow orizzontale di 3 px sulla pagina «Mon parcours» in arabo a 390 px, causato dai puntini
   elenco di un testo francese di fallback dentro una lista specchiata.
2. Un test sul marchio che si aspettava l'HTML precedente all'aggiunta di `dir="ltr"`.
3. Il peso documentato di `base.css`, non più veritiero dopo le correzioni RTL.

Dopo la correzione sono state rieseguite le suite interessate: 46 test di frontend e 8 di browser
dell'area riservata, tutti verdi. **La suite completa non è stata rieseguita dopo quella correzione**;
lo sarà a valle del rebase.

---

## 7. Qualità verificata prima del rebase

| Verifica | Esito |
|---|---|
| `ruff check .` | pulito |
| `makemigrations --check` | nessuna modifica da generare |
| `manage.py check --deploy` | 0 rilievi |
| bandit | 0 rilievi di gravità alta |
| pip-audit | nessuna vulnerabilità nota |
| Copertura traduzioni it/en/ar/fr | 100 % su 1 814 messaggi |
| Lighthouse mobile (Forum, Imprese, home araba) | 100/100/100 |
| LCP su rete lenta simulata con CPU rallentata 4× | 1,8 s · CLS 0 |
| Scansione in ampiezza | 804 caricamenti, 128 link, 0 link rotti |

---

## 8. Audit ostile già svolto

Un red team indipendente in sola lettura ha esaminato quattro aree prima del rebase e prodotto
**48 rilievi**. Le aree completate: contenuto e conformità legale (14), permessi e sicurezza (4),
form e consensi (15), gate e metadati (15). Cinque aree non sono state completate per esaurimento
della quota del modello e sono ripianificate: WCAG, mobile e design, RTL e i18n, link ed errori e
prestazioni, coerenza fra documentazione e realtà.

I rilievi confermati più gravi:

- **CL-01** Il questionario di orientamento, che è contenuto del team e non testo prescritto, è
  **solo in francese**: su `/it/`, `/en/` e `/ar/` ogni domanda, opzione, esito e checklist appare in
  francese. È il cuore dell'esperienza delle persone e il pubblico principale legge arabo.
- **CL-02, GM-01…04** Difetti su date, gate e metadati da verificare uno per uno.
- **FC-01…06** Sei rilievi di gravità alta su form e consensi.
- **PS-03** confermato, **PS-02** parzialmente confermato, **PS-01** e **PS-04** smentiti dal
  verificatore indipendente.

L'elenco integrale è conservato e sarà lavorato nel rebase.

---

## 9. Che cosa manca, detto senza attenuanti

Il **sito pubblico** è sostanzialmente completo e conforme. La **piattaforma autenticata** descritta
dal Technical Blueprint **non esiste ancora**: ci sono le fondamenta (account, ruoli, questionario,
area riservata di sola lettura) ma mancano il fascicolo digitale, il Rule Engine come dato versionato
con workflow di approvazione, la checklist con attore responsabile, i documenti con stati e
requisiti, l'Academy, i fabbisogni gestibili dall'impresa, i workspace dei soggetti autorizzati, dei
professionisti, delle istituzioni e delle università, lo sportello digitale e il Forum come modulo di
governance.

Sul piano visivo, il committente ha respinto il risultato. La diagnosi è nel documento
`CURRENT_VISUAL_AUDIT.md`: non è brutto, è **generico**.

---

## 10. Come si avvia oggi

```bash
cd /c/tmp/italylegalentry
docker compose up -d db                      # PostgreSQL 17 su 127.0.0.1:5439
export PYTHONIOENCODING=utf-8
.venv/Scripts/python manage.py migrate
.venv/Scripts/python manage.py seed_all
.venv/Scripts/python manage.py runserver 127.0.0.1:8770
```

Stato «Fase 3 aperta» per la verifica, con data simulata:

```bash
DATABASE_URL=postgres://ile:ile-dev-password@127.0.0.1:5439/ile_qa \
ILE_REFERENCE_DATE=2026-10-05 \
.venv/Scripts/python manage.py runserver 127.0.0.1:8771
```

Suite completa:

```bash
TEST_DATABASE_URL=postgres://ile:ile-dev-password@127.0.0.1:5439/ile_orch \
.venv/Scripts/python -m pytest -q -p no:cacheprovider
```
