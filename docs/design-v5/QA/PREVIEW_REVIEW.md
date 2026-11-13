# Revisione indipendente dell'anteprima V5 — `/__design-v5/` (commit `806c429`)

| | |
|---|---|
| **Oggetto** | `design-v5: dev-only preview hub /__design-v5/ (V5.2 stream B kickoff)` — commit `806c429` su `design-v5`, base `c50d086` |
| **Ruolo** | Revisore indipendente dello stream B (non ha costruito nulla dell'anteprima) |
| **Data** | 1 ottobre 2026, sera |
| **Verdetto** | **PASS_WITH_FIXES** — nessun rilievo bloccante; **un rilievo maggiore** (§3, F1: gli alias 8.3 di Windows aggirano il rifiuto dei segmenti puntati) da chiudere prima di dichiarare PREVIEW READY al proprietario e prima dell'integrazione; quattro rilievi minori; tre osservazioni |
| **Strumenti** | server della worktree su `127.0.0.1:8781` (`DATABASE_URL=…/ile_v5`, `ILE_DESIGN_PREVIEW=1`, `--noreload`, spento a fine revisione); confronto con `main` su `127.0.0.1:8770`; corsia di test `ile_lane5`; Playwright 1.63 headless (Chromium) con profilo proprio `C:/tmp/ile_v5_council/.profiles/stream-b/chromium-review`; Django 5.2.17, django-csp 4.0, Python 3.13.5 |
| **Lucchetto** | `C:/tmp/ile_locks/PERFORMANCE_BENCHMARK_LOCK` assente a ogni controllo (prima dei test, prima del server, prima del browser) |
| **Prove** | script e catture fuori dal repository: `C:/tmp/ile_review_b/` (`check_a_absence.py`, `probe_b_c.py`, `probe_d_g.py`, `probe_misc.py`, `look_h.py`, `verify_fix.py`, `shots/*.png`, `lane5.out.log`) |

Nessuna sessione aperta, nessun modulo compilato, nessuna password digitata. Nessun browser su 9222 o 9223.

---

## 1. Che cosa è stato verificato, e come

| | Richiesta | Esito | Come |
|---|---|---|---|
| (a) | Irraggiungibile senza `DEBUG` + flag | **ok** | resolver e test client sotto `config.settings.test`, sotto `config.settings.prod` (chiave usa-e-getta di 64 caratteri, `ILE_DESIGN_PREVIEW=1`, `DJANGO_DEBUG=1`) e sotto `config.settings.dev` con `DJANGO_DEBUG=0` — §2.1 |
| (b) | Sicurezza dei percorsi | **un'eccezione (F1)** | 49 richieste grezze via `http.client` (nessuna normalizzazione lato client) — §2.2 |
| (c) | Intestazioni e CSP di produzione | **ok** | hub, selettore (200 e 400), file di prova (html e md); `/fr/`, `/fr/compte/login/`, `/ar/`, `/fr/espace-reserve/` su 8781 e 8770 — §2.3 |
| (d) | Pulizia CSP dei nuovi template | **ok** | sorgenti e pagine renderizzate (parser HTML): nessun `style=`, `<style>`, `<script>` inline, `on*=`, `javascript:` — §2.4 |
| (e) | Perimetro di proprietà, LF, segreti | **tre percorsi fuori riga (F2), LF ok, nessun segreto** | `git diff --name-only c50d086 806c429`, `git ls-files --eol`, conteggio dei byte CR, scansione dei segreti — §2.5 |
| (f) | I test passano quando li eseguo io | **ok: 652 passati, 1 xfail atteso** | corsia `ile_lane5` — §2.6 |
| (g) | L'hub elenca ogni superficie; il selettore commuta h0/ha/hb in fr e ar e in entrambe le fasi | **ok** | 38 file di prova richiesti + 3 voci del selettore + 4 pagine dal vivo, tutti con risposta 200; 12 combinazioni del selettore — §2.7 |
| (h) | Sguardo headless a 1440 e 390 | **ok** | nessun overflow orizzontale, nessun errore in console, nessuna richiesta fallita; font e token del sito; italiano — §2.8 |

---

## 2. Le prove

### 2.1 (a) Assenza senza `DEBUG` e flag

Script `check_a_absence.py` (resolver + `django.test.Client`), eseguito dalla radice della worktree. Il test client ha bisogno di una base dati perché `cms.LegacyURLMiddleware` interroga la tabella dei redirect su ogni 404: puntato alla copia `ile_v5` dello stream (sole GET). Sotto `prod` la pagina 404 non si renderizza senza `collectstatic` (manifest assente nella worktree): per leggere lo stato è stato sostituito in-process **solo** lo storage degli static con quello semplice; URLconf, `INSTALLED_APPS` e `DEBUG` intatti.

| Impostazioni | Ambiente | `hasattr(settings, "ILE_DESIGN_PREVIEW")` | app installata | `resolve()` sulle tre rotte | `GET` sulle tre rotte | `GET /fr/` |
|---|---|---|---|---|---|---|
| `config.settings.test` | `ILE_DESIGN_PREVIEW=1` | False | no | `Resolver404` ×3 | 404 ×3 | — |
| `config.settings.prod` | chiave 64 car., `ILE_DESIGN_PREVIEW=1`, `DJANGO_DEBUG=1` | False (`DEBUG` resta False) | no | `Resolver404` ×3 | 404 ×3 | 200 |
| `config.settings.dev` | `DJANGO_DEBUG=0`, `ILE_DESIGN_PREVIEW=1` | True, valore **False** | no | `Resolver404` ×3 | 404 ×3 | 200 |

Il flag da solo non accende nulla; `prod.py` e `test.py` non lo conoscono; il montaggio sta dentro `if settings.DEBUG:` e dietro un secondo `if getattr(settings, "ILE_DESIGN_PREVIEW", False)`. Le viste ricontrollano `DEBUG`, il flag e `REMOTE_ADDR` (loopback) a ogni richiesta: con intestazioni `X-Forwarded-For`/`X-Real-IP` false da 127.0.0.1 l'hub risponde 200, cioè la guardia legge il socket e non le intestazioni (giusto).

### 2.2 (b) Sicurezza dei percorsi — 49 richieste grezze su `127.0.0.1:8781`

Script `probe_b_c.py`; ogni request-target è inviato alla lettera. **45 su 49 rifiutate con 404**, nessun corpo trapelato:

- traversata semplice (`home/../../SIGNING_SHEET.md`, `../../../manage.py`, `../directives/…`) → 404;
- traversata percentuale (`%2e%2e/%2e%2e/manage.py`, `home%2f..%2f..%2fmanage.py`, `..%2f..%2f..%2fmanage.py`, doppia codifica `%252e%252e`) → 404;
- barre rovesciate grezze e codificate (`home\..\..\manage.py`, `..%5c..%5c..%5cmanage.py`, `%5c%5c127.0.0.1%5cc$%5c…`, `home\phase3.html`) → 404;
- segmenti puntati per nome lungo (`.work/`, `.work/photos/meta/14700179.json`, `.profiles/…`, `.ecd/…`, `.vendor/…`, `%2ework/…`, `home/options/.git-status-after.txt`, `.gitignore`, `.env`) → 404;
- file di lavoro (`tools/build_index.py`, `tools/shoot.py`, `shoot.PY`, `shoot.py::$DATA`, `shoot.py.`, `shoot.py%20`) → 404; cartelle (`tools/`, `home/`, `home`), segmento vuoto (`home//phase3.html`), barra finale su un file → 404;
- percorsi assoluti (`C:/Windows/win.ini`, `C%3A/…`, `C:%5cWindows%5cwin.ini`, `//etc/passwd`, `%2fetc%2fpasswd`, `//C:/tmp/ile_wt/design-v5/manage.py`, `C:/tmp/ile_v5_council/proof/index.html`) → 404.

**Le quattro eccezioni:**

| Richiesta | Risposta | Che cosa è |
|---|---|---|
| `/__design-v5/proof/WORK~1/photos/meta/14700179.json` | **200**, 506 byte | il contenuto di `.work/` attraverso l'alias 8.3 della cartella |
| `/__design-v5/proof/ECD~1/ar_rail_strings.json` | **200**, 1 524 byte | `.ecd/` attraverso l'alias |
| `/__design-v5/proof/VENDOR~1/package/package.json` | **200**, 1 699 byte | `.vendor/` attraverso l'alias |
| `/__design-v5/proof/home/options/GIT-ST~1.TXT` | **200**, 39 195 byte | **il file `.git-status-after.txt`** che il test dell'ingegnere rifiuta per nome lungo |
| `/__design-v5/proof/tools/shoot.py%00.html` | 500 | **non dell'anteprima**: vedi O2 — su `main` 8770 anche `/fr/nothing%00here/` risponde 500 |

`cmd /c dir /x C:\tmp\ile_v5_council\proof` mostra `ECD~1 .ecd`, `PROFIL~1 .profiles`, `VENDOR~1 .vendor`, `WORK~1 .work`; la stessa cosa per il file (`GIT-ST~1.TXT .git-status-after.txt`). Il controllo di `services.resolve_proof_file` guarda i segmenti della **stringa grezza** (`segment.startswith(".")`) e poi `safe_join` + `is_file()`: l'alias non comincia con un punto, `safe_join` lo accetta perché il percorso risolto resta sotto la radice, e Windows apre la cartella puntata. `.profiles/` oggi non contiene file (solo tre cartelle vuote) e `PROFIL~1/` risponde 404 per questo; `.work/` ha 291 file con suffisso servibile su 305, `.ecd/` 58 su 83, `.vendor/` 2 121 su 2 123. Nessun segreto nei file servibili (la chiave Pexels è letta dall'ambiente in `fetch.py`, che come `.py` resta rifiutato); i `.py`, `.ps1`, `.log` restano fuori dalla tabella dei tipi anche per alias. Nessuna maquette fa riferimento a `.vendor/`, `.work/` o `.ecd/` (`grep` su tutti gli `.html` del pacchetto: 0 occorrenze), quindi la correzione non rompe nulla.

I file veri sono serviti con il tipo scritto: `home/phase3.html`, `home/options/hb-phase3-ar.html`, `smoke/loader.html` → `text/html; charset=utf-8`; `SIGNING_SHEET.md` → `text/plain; charset=utf-8`; `index.html` → html. `HEAD` su un file di prova → 200 con le stesse intestazioni. `POST`/`PUT`/`DELETE` sull'hub → 403 (CSRF, prima della vista). `/__design-v5` senza barra → 301 su `/__design-v5/`.

### 2.3 (c) Intestazioni

Su **hub**, **selettore** (`?variant=hb`; `?variant=ha&lang=ar&phase=3`; `?variant=h0&lang=ar&phase=interim`; `?variant=zz` → 400) e **file di prova** (`home/phase3.html`, `SIGNING_SHEET.md`):

- `X-Robots-Tag: noindex, nofollow` — presente su tutti, compreso il 400 e lo streaming `FileResponse`;
- `Cache-Control: no-store` — presente su tutti;
- `script-src 'self'` e `style-src 'self'` — su tutti; nessun `unsafe` in nessuna policy;
- `<meta name="robots" content="noindex, nofollow">` — nell'hub (via `base.html`, contesto `noindex`) e nel selettore (200 e 400). È scritto con uno spazio dopo la virgola; equivale a `noindex,nofollow` per ogni crawler;
- `Content-Language: it` sulle pagine (il selettore e l'hub sono in italiano qualunque sia la lingua della richiesta);
- selettore: `frame-src 'self'` aggiunto, `frame-ancestors 'none'` e `X-Frame-Options: DENY` conservati (il selettore non è incorniciabile);
- file di prova: `frame-ancestors 'self'` al posto di `'none'`, `X-Frame-Options: SAMEORIGIN`, nessun `frame-src` aggiunto.

**La policy di produzione non si muove.** `/fr/` su 8781 (flag acceso) e su 8770 (`main`): stesse 11 direttive con gli stessi valori (`base-uri 'self'; connect-src 'self'; default-src 'self'; font-src 'self'; form-action 'self'; frame-ancestors 'none'; img-src 'self' data:; object-src 'none'; script-src 'self'; style-src 'self'; upgrade-insecure-requests`), stesso `X-Frame-Options: DENY`, nessun `X-Robots-Tag`, stesso `Cache-Control`. Lo stesso per `/fr/compte/login/`, `/ar/`, `/fr/espace-reserve/` (302 su entrambi). **Le stringhe grezze non sono identiche carattere per carattere, e non possono esserlo:** django-csp 4.0 costruisce l'intestazione iterando `set(chain(config, replace))` (`csp/utils.py`, `build_policy`), e l'ordine di un `set` di stringhe dipende dal seme di hash del processo. I tre server di `main` (8770, 8771, 8772) emettono tre ordini diversi delle stesse direttive. Il confronto corretto è per insieme di direttive, come fa già `test_the_production_policy_of_a_normal_page_is_unchanged`; il confronto è **uguale**.

### 2.4 (d) Pulizia CSP

Sorgenti (`templates/dev/designpreview/hub.html`, `frame.html`): l'unico `<script>` è `<script src="{% static 'js/dev/designpreview.js' %}" defer>`; nessun `style=`, `<style>`, `on*=`, `javascript:`, nessun riferimento `http(s)://`. Foglio `static/css/dev/designpreview.css`: nessun `url(`, `@import`, `!important`, colore letterale, URL esterno.

Pagine renderizzate (parser HTML su 6 pagine: hub; selettore h0, ha/ar/3, hb/fr/interim/w=390, hc, zz=400): 0 attributi `style`, 0 `<style>`, 0 script inline, 0 gestori `on*`, 0 URL `javascript:`, 0 riferimenti esterni, nessuna sintassi di template trapelata. Riflessione: `?variant=<script>alert(1)</script>` compare nel 400 come `variant=&#x27;&lt;script&gt;…` (autoescape); `?w=<b>1440` non produce classe né testo grezzo.

### 2.5 (e) Perimetro, LF, segreti

`git diff --name-only c50d086 806c429` — 12 file:

| File | Nella riga del Preview Engineer in `AGENT_OWNERSHIP.md`? |
|---|---|
| `apps/designpreview/{__init__,apps,services,urls,views}.py` | sì (`apps/designpreview/**`) |
| `config/settings/dev.py` (blocco `ILE_DESIGN_PREVIEW*`, 13 righe) | sì (il flag) |
| `config/urls.py` (5 righe dentro `if settings.DEBUG:`) | sì (il montaggio) |
| `tests/frontend/test_design_preview.py` | sì |
| `templates/dev/designpreview/hub.html`, `frame.html` | **no** — la riga dice `templates/designpreview/**` |
| `static/css/dev/designpreview.css` | **no** — non elencato |
| `static/js/dev/designpreview.js` | **no** — non elencato; la cartella `static/js/dev/` è nuova |

Verificata la ragione data nel messaggio di commit: `tests/frontend/test_design_docs.py::test_the_dev_stylesheet_stays_out_of_the_production_cascade` impone che ogni foglio sotto `static/css/dev/` sia caricato da un template sotto `templates/dev/` e da nient'altro, e la cascata esclude `dev/` da `main.css`. Le due cartelle esistevano già (`showcase.css`, `showcase.html`); è la convenzione del repository per le pagine DEBUG-only, e nessun'altra riga della tabella possiede quei percorsi. Resta un fatto: la tabella non dice ciò che l'ingegnere ha scritto (F2).

LF: `git ls-files --eol` → `i/lf w/lf` per i 12 file; 0 byte CR e nessun BOM nelle copie di lavoro. Segreti: scansione di chiavi, token, password, blocchi PEM, pattern AWS/OpenAI/GitHub sui 12 file → solo la parola «token» nel senso di design token. `.env` della worktree: non versionato, senza `ILE_DESIGN_PREVIEW`.

### 2.6 (f) I test, eseguiti dal revisore

Corsia `ile_lane5`, mai in parallelo con un'altra corsia del revisore:

```
TEST_DATABASE_URL=postgres://ile:ile-dev-password@127.0.0.1:5439/ile_lane5
.venv/Scripts/python -m pytest tests/frontend/test_design_preview.py tests/security tests/frontend
    apps/pages/tests/test_templates_static.py tests/i18n/test_rtl_static.py
    -m "not browser" -q -p no:randomly -rxXf
→ 652 passed, 12 deselected, 1 xfailed in 311.09s (0:05:11)
```

Il solo xfail è `test_legacy_token_shim.py::test_the_shim_is_gone` (il debito dello shim, atteso). I 50 test di `test_design_preview.py` passano, compreso `test_the_catalogue_is_current_against_the_real_package` sul pacchetto vero. La corsia è un soprainsieme di quella dichiarata dall'ingegnere (455 su `ile_lane4`): qui tutta `tests/frontend` tranne il file Playwright, più `tests/i18n/test_rtl_static.py`. Nota: il test dell'ingegnere `test_proof_refuses_what_it_must_with_a_404` copre i nomi lunghi e non gli alias 8.3 (F1).

### 2.7 (g) L'hub e il selettore

L'hub (`probe_d_g.py`) collega i **38 file richiesti** del pacchetto, ciascuno con risposta 200 attraverso `/__design-v5/proof/`: `home/phase3.html` (H-0), `phase3-ar`, `interim`, `interim-ar`; `home/options/ha-phase3.html` (H-A), `ha-phase3-ar`, `ha-interim`; `home/options/hb-phase3.html` (H-B), `hb-phase3-ar`, `hb-interim`; i quattro stati del menu (`phase3-menu`, `phase3-menu-ar`, `interim-menu`, `interim-menu-ar`); `login/` (index, error, ar, error-ar); `shell-dashboard/` (index, ar); `documents/` (index, ar, chips, depot, depot-ar); `journey/` (index, ar, hero-lights, hero-lights-ar); `phone-hero/index.html`; `smoke/` (index, console, chrome, icons, identity-small, loader); `index.html` e `SIGNING_SHEET.md`. Più le tre voci del selettore (h0, ha, hb → 200), le quattro pagine dal vivo del controllo V4 (`/fr/`, `/fr/compte/login/`, `/fr/espace-reserve/`, `/ar/`), H-C e H-D come segnaposto («non ancora disponibile» ×6 con le quattro superfici in arrivo), le otto larghezze (1440 … 360), l'avviso «Niente di ciò che è mostrato è approvato» come primo blocco. Nessun «manca»: ogni file catalogato è su disco. L'ordine dei dodici gruppi segue `SIGNING_SHEET.md` §1.2. Non è collegato `home/options/index.html` (il foglio O67 affiancato): non richiesto, ma utile (vedi F4, facoltativo).

Il selettore, 12 combinazioni:

| variante | fr · 3 | ar · 3 | fr · intérim | ar · intérim |
|---|---|---|---|---|
| h0 | `home/phase3.html`, `lang="fr"` | `home/phase3-ar.html`, `lang="ar"` | `home/interim.html` | `home/interim-ar.html` |
| ha | `home/options/ha-phase3.html` | `home/options/ha-phase3-ar.html` | `home/options/ha-interim.html` | nessun iframe, «non è nel pacchetto del gate 0» |
| hb | `home/options/hb-phase3.html` | `home/options/hb-phase3-ar.html` | `home/options/hb-interim.html` | nessun iframe, «non è nel pacchetto del gate 0» |

Ogni iframe punta al file giusto, il file risponde 200 e porta l'attributo `lang` della lingua scelta; la barra marca con `aria-current` variante, lingua e fase correnti; `w=1440|390` aggiunge `dp-stage--w…`, `w=999` no; `variant=hc` → messaggio senza iframe; valore sconosciuto → 400 con il messaggio e il ritorno a H-0.

### 2.8 (h) Lo sguardo headless (profilo proprio, 1440×900 e 390×844)

`look_h.py`, catture in `C:/tmp/ile_review_b/shots/` (`hub-1440.png` 1440×5325, `hub-390.png` 390×8528, `picker-*.png`).

- **Overflow orizzontale: nessuno** su hub e selettore a entrambe le larghezze (`scrollWidth == clientWidth`; nessun elemento oltre il bordo). 0 messaggi di errore/avviso in console, 0 richieste fallite o ≥ 400.
- **Tipografia e colore del sito:** titolo in Newsreader 52 px/500, titoli dei gruppi in Newsreader, testi in IBM Plex Sans, occhielli e folio in IBM Plex Mono; fondo `rgb(244, 243, 240)` (`--min-1`), inchiostro `rgb(21, 34, 42)`, accento `rgb(15, 106, 114)`. Il foglio parla solo per token (lo prova anche `test_the_dev_stylesheet_speaks_tokens_only`).
- **Quieta e di prodotto:** testata di una riga con il lock-up e la dicitura «ANTEPRIMA V5 · SVILUPPO · NON PUBBLICA», avviso istituzionale del sito (`components/notice.html`), indice numerato, gruppi con filetto, righe con pastiglie-link; niente gradienti, ombre, icone decorative, emoji o cartigli. Nessun «generic AI look».
- **Italiano:** tutte le etichette dell'hub e della barra (i nomi francesi — «Mes pièces», «Dépôt», «fr · intérim» — sono i nomi delle superfici francesi). Bersagli tattili: nessun link sotto 24 px a 390.
- **Selettore:** barra da 49 px a 1440 su una sola riga, iframe 1440×851; a 390 la barra va a capo su quattro righe (231 px, 27 % della finestra) e l'iframe resta 390×613: funziona, ma la larghezza di revisione su telefono è pensata per la barra dei dispositivi di Chrome, non per una finestra da 390 (F5, facoltativo).

---

## 3. Rilievi

### F1 — MAGGIORE · gli alias 8.3 di Windows aggirano il rifiuto dei segmenti puntati

**Fatto.** `GET /__design-v5/proof/WORK~1/photos/meta/14700179.json` → 200 (contenuto di `.work/`); `ECD~1/…` → 200; `VENDOR~1/package/package.json` → 200; `home/options/GIT-ST~1.TXT` → 200, cioè `.git-status-after.txt` (39 KB), il file che `test_proof_refuses_what_it_must_with_a_404` rifiuta per nome lungo. La regola dura dell'anteprima («mai un segmento puntato o un file di lavoro») e la frase del messaggio di commit sono false sul sistema su cui gira (il volume `C:` genera nomi 8.3). Esposizione contenuta — solo sviluppo, solo loopback, solo con il flag, nessun segreto nei file servibili, `.py`/`.ps1`/`.log` comunque fuori tabella, `.profiles/` oggi vuota — ma `.profiles/` è dove vivono i profili dei browser dei ruoli di cattura, e l'invariante va tenuto dove lo si dichiara.

**Correzione (verificata in `verify_fix.py` su copia della funzione: chiude i quattro alias, serve ancora `home/phase3.html`, `hb-phase3-ar.html`, `smoke/loader.html`, `SIGNING_SHEET.md`, `index.html`, `home/PHASE3.HTML`).** In `services.resolve_proof_file`, dopo `is_file()`, ricontrollare il percorso **reale**, perché la stringa grezza non è il nome del file:

```python
try:
    real = full.resolve(strict=True)
    relative = real.relative_to(root.resolve(strict=True))
except (OSError, ValueError) as exc:
    raise Http404 from exc
if any(part.startswith(".") or "~" in part for part in relative.parts) or relative.suffix.lower() != suffix:
    raise Http404
return real, content_type
```

e, cintura e bretelle, `"~" in segment` fra i rifiuti sulla stringa grezza (nessun file del pacchetto porta una tilde). Test di regressione: creare `.work/x.json` sotto `tmp_path`, ricavare l'alias con `ctypes.windll.kernel32.GetShortPathNameW` e chiedere l'alias → 404 (skip se il volume non genera nomi 8.3); e il caso di un link simbolico che punta fuori dalla radice → 404. Il messaggio di commit e la docstring di `services.py` vanno aggiornati di conseguenza.

### F2 — MINORE · tre percorsi fuori dalla riga di proprietà

`templates/dev/designpreview/**`, `static/css/dev/designpreview.css`, `static/js/dev/designpreview.js` non sono nella riga del Preview Engineer (`templates/designpreview/**`; nessun `static/`). La collocazione è quella imposta dai test del repository (§2.5) e nessun altro agente possiede quei percorsi: nessun conflitto reale. **Correzione:** il Merge Coordinator — unico proprietario di `AGENT_OWNERSHIP.md`, su `main` — aggiorna la riga con i percorsi effettivi; l'ingegnere non deve spostare nulla.

### F3 — MINORE · l'impronta di rimozione ha un settimo pezzo

La regola dell'anteprima enumera «un'app, un montaggio condizionale, un'impostazione dev, un foglio dev»; il commit aggiunge anche uno **script dev** (`static/js/dev/designpreview.js`, scorciatoie `0 a b · f r · 3 i`). È fuori dal bundle (`build_frontend.mjs`, `build_css.mjs`, `dist/`), caricato dal solo `frame.html`, senza rete né storage (`test_the_dev_script_is_a_classic_script_without_network_or_storage`), e la barra funziona senza di esso. **Correzione, una delle due:** togliere lo script e la frase sui tasti nell'hub (la barra è già fatta di link), oppure far registrare al Merge Coordinator che l'impronta ammessa comprende uno script dev. Resta «banalmente rimovibile» in entrambi i casi.

### F4 — MINORE · il selettore non dice che l'/ar/ di fase 3 è «da non firmare»

`?lang=ar&phase=3` incornicia le pagine `*-phase3-ar.html`, che sono la **copia bloccata non tradotta** (SIGNING_SHEET §1.2: striscia rosa «copie verrouillée NON TRADUITE — ne pas signer»). L'hub lo scrive accanto ai link («da non firmare come /ar/»); il selettore — lo strumento con cui il proprietario confronta — non lo dice nella barra, e la riga «PROVISIONAL» della maquette sta in fondo al documento, fuori dal primo schermo. Il titolo francese sotto la testata araba (`picker-hb-ar-3-1440.png`) si legge come un difetto se nessuno avverte. **Correzione:** quando `lang == "ar"` e `phase == "3"`, una nota nella barra (o sopra l'iframe) con il testo dell'hub; un `if` in `frame.html`, la frase in `services.hero_choice`. Facoltativo nello stesso passaggio: collegare `home/options/index.html` (il foglio O67 affiancato) dal gruppo 1 dell'hub.

### F5 — MINORE (facoltativo) · a 390 la barra del selettore occupa un quarto della finestra

231 px su 844. Non è il modo previsto di guardare il telefono (si sceglie la larghezza dalla barra a finestra piena, o dalla barra dei dispositivi di Chrome), e nulla trabocca. Se si vuole: sotto 48rem nascondere la riga delle larghezze o ridurla a un `<details>`.

---

## 4. Osservazioni (nessuna azione per l'anteprima)

- **O1 — CSP «identica»:** le stringhe differiscono solo nell'ordine delle direttive, per il `set` di django-csp 4.0; i tre server di `main` differiscono tra loro allo stesso modo. Confrontare per insieme, come già fa il test dell'ingegnere (§2.3).
- **O2 — `%00` → 500, preesistente su `main`:** `GET /fr/nothing%00here/` e `GET /fr/compte/login/%00` rispondono 500 su 8770 come su 8781 (`cms.LegacyURLMiddleware` interroga `Redirect.old_path__in` con un NUL nella stringa; psycopg rifiuta). `/static/x%00.css` → 404 perché WhiteNoise risponde prima. Non è dell'anteprima — il resolver dell'anteprima rifiuta il NUL (`"\x00" in raw`) e non viene mai raggiunto — ma merita un biglietto per chi possiede `apps/cms/middleware.py`: con `DEBUG` acceso la pagina di errore è quella tecnica di Django.
- **O3 — dettagli non bloccanti:** `from django.utils._os import safe_join` è un modulo privato di Django (lo usa anche `django.views.static.serve`; accettabile, da sapere); `POST`/`PUT` sull'hub ricevono il 403 del CSRF **senza** `X-Robots-Tag`/`no-store` (richiesta rifiutata, irrilevante); il default `ILE_DESIGN_PREVIEW_PROOF_DIR="C:/tmp/ile_v5_council/proof"` è un percorso locale scritto nel repository — in un'impostazione dev-only va bene, e `.env` può sovrascriverlo.

---

## 5. Ciò che la revisione conferma

- La produzione non sa che l'anteprima esiste: `prod.py` e `test.py` non definiscono il flag, l'app non è installata, le rotte non si risolvono, `/fr/` tiene la stessa policy di `main`, `main.css` e gli script di build non sono toccati.
- Tutte le risposte dell'anteprima — hub, selettore (200 e 400), file di prova in streaming, `HEAD` — portano `X-Robots-Tag: noindex, nofollow` e `Cache-Control: no-store`; le pagine portano il meta robots; `Content-Language: it`.
- La CSP stretta vale anche dentro l'anteprima (`script-src 'self'; style-src 'self'`, nessun `unsafe`); i due allargamenti (`frame-src 'self'` sul selettore, `frame-ancestors 'self'` + `SAMEORIGIN` sui file) sono decoratori per vista, assenti altrove.
- 652 test verdi sulla corsia del revisore; LF ovunque; nessun segreto.
- L'hub mostra tutte le superfici del gate 0 nell'ordine della scheda di firma, con l'avviso di non approvazione in testa; il selettore commuta le dodici combinazioni e dice la verità sulle due che il pacchetto non ha.

**Verdetto: PASS_WITH_FIXES.** F1 va chiuso (sei righe e un test) prima del «PREVIEW READY» al proprietario e prima dell'integrazione; F2 è un'annotazione del Merge Coordinator; F3–F5 si chiudono nel passaggio successivo o si registrano come decisione.
