# Mappa di migrazione degli URL — preparazione (nessuna modifica in produzione)

Sorgente: `docs/CURRENT_SITE_AUDIT.md` (sito WordPress single-page con ancore, lingua via `?lang=`, sub-dominio
`app.legalitalentry.it` non raggiungibile — 503 e certificato TLS non valido per il nome). Destinazione: nuovo schema con
prefisso di lingua obbligatorio (`/it/`, `/fr/`, `/en/`, `/ar/`), `LocaleMiddleware` e `i18n_patterns`.

## 1. Schema URL della nuova piattaforma

| Area | URL (con `<lang>`) | Nome |
|---|---|---|
| Home | `/<lang>/` | `pages:home` |
| Progetto / AGAMI / Rete / Contatti | `/<lang>/projet/`, `/<lang>/agami/`, `/<lang>/reseau/`, `/<lang>/contact/` | `pages:*` |
| Anti-frode | `/<lang>/attention-aux-fraudes/` (Fase 3) | `pages:antifraud` |
| Espace Personnes | `/<lang>/parcours/`, `/<lang>/parcours/<key>/` (8 percorsi, Fase 3) | `pathways:index`, `pathways:detail` |
| Diplomi / Formazione | `/<lang>/diplomes-et-titres/`, `/<lang>/formation/` (Fase 3) | `pathways:diplomas`, `pathways:training` |
| Orientamento | `/<lang>/orientation/` | `orientation:start` |
| Espace Entreprises | `/<lang>/entreprises/` (Fase 1) | `ecosystem:companies` |
| Istituzioni / Università / Pilota | `/<lang>/institutions/`, `/<lang>/universites-et-formation/`, `/<lang>/projet-pilote/` (Fase 3) | `ecosystem:*` |
| Forum | `/<lang>/forum/` (Fase 2) | `forum:index` |
| Forum Virtuale | `/<lang>/forum-virtuel/` (flag) | `community:index` |
| Actualités / FAQ / Glossario / Vivere in Italia | `/<lang>/actualites/`, `/<lang>/faq/`, `/<lang>/glossaire/`, `/<lang>/vivre-en-italie/` | `news:*`, `faq:*`, `glossary:*`, `living:*` |
| Partner | `/<lang>/partenaires/` | `partners:index` |
| Area riservata / account | `/<lang>/espace-reserve/`, `/<lang>/compte/login/`, `/<lang>/compte/signup/` | `portal:*`, allauth |
| Pagine legali (slug italiani per tutte le lingue: testo ufficiale IT) | `/<lang>/privacy-policy/`, `/<lang>/cookie-policy/`, `/<lang>/note-legali/`, `/<lang>/condizioni-di-utilizzo/`, `/<lang>/avvertenze/` | `legal:*` |
| Tecnici (senza lingua) | `/sitemap.xml`, `/robots.txt`, `/healthz/`, `/backoffice/`, `/documents/<uuid>/`, `/api/v1/…` | — |

## 2. Mappa vecchio → nuovo

Legenda tipo: **301** permanente · **410** risorsa rimossa · **302** temporaneo · **—** nessun redirect (URL già valido).

| URL / ancora attuale | Nuovo URL | Tipo | Note |
|---|---|---|---|
| `/` | `/<lang>/` (lingua da `Accept-Language`, default `fr`) | 302 | `core.views.root_redirect`; già implementato |
| `/?lang=it` · `/?lang=fr` · `/?lang=en` · `/?lang=ar` | `/it/` · `/fr/` · `/en/` · `/ar/` | 301 | middleware redirect (Stage 3) che legge `lang` dalla query e reindirizza; il cookie `ile_language` sostituisce quello WordPress |
| `/#parcours` | `/<lang>/parcours/` | 301 (ancora non visibile al server → regola per `/` + documentazione) | prima della Fase 3 la pagina è interim (200) |
| `/#visas` (Short-Stay Visas) | `/<lang>/parcours/other_regular_routes/` | 301 | i visti brevi non sono un percorso prescritto: confluiscono in «Autres voies régulières» (da confermare con il committente) |
| `/#formation` | `/<lang>/formation/` | 301 | Fase 3 (404 finché gated → usare `/<lang>/parcours/` come destinazione interim) |
| `/#entreprises` | `/<lang>/entreprises/` | 301 | Fase 1 |
| `/#reseau` | `/<lang>/reseau/` | 301 | |
| `/#apropos` (About e i cinque link «legali») | `/<lang>/projet/` per About; i link legali → le 5 pagine autonome | 301 | il sito attuale usa la stessa ancora per Legal Notices, Privacy, Cookie, Terms, Disclaimers: nella nuova piattaforma sono 5 route distinte (test `test_five_legal_routes_are_distinct_pages`) |
| `/hello-world/` | — | 410 | post WordPress di default |
| `/category/uncategorized/` | — | 410 | tassonomia WordPress |
| `/author/*` | — | 410 | pagina autore |
| `/wp-sitemap.xml`, `/wp-sitemap-*.xml` | `/sitemap.xml` | 301 | sitemap Django (registro `core.sitemaps`) |
| `/wp-json/`, `/wp-json/wp/v2/*` | — | 410 | API WordPress: nessun equivalente pubblico; l'API della piattaforma è `/api/v1/` con chiave |
| `/wp-login.php`, `/wp-admin/`, `/xmlrpc.php`, `/readme.html` | — | 410 (o 404) | endpoint WordPress; il back-office è `/backoffice/` |
| `/wp-content/…` (tema, plugin Hostinger Reach) | — | 410 | nessun asset riutilizzato |
| `/feed/`, `/comments/feed/` | — | 410 | eventuale feed news futuro: `/<lang>/actualites/feed/` (non implementato) |
| `http://app.legalitalentry.it/` · `https://app.legalitalentry.it/` | `/<lang>/espace-reserve/` | **decisione pendente** | oggi 503 + certificato errato; opzioni: (a) redirect 301 al nuovo sub-path, (b) dismissione del sub-dominio. Richiede DNS/certificato: fuori dal perimetro locale |
| `https://app.legalitalentry.it/join` | `/<lang>/orientation/` | pendente | «Start My Pathway» del sito attuale |
| `https://app.legalitalentry.it/register/company` | `/<lang>/entreprises/` | pendente | «I am an Enterprise» → Recueil des besoins |
| link «Contact» → `http://app.legalitalentry.it` | `/<lang>/contact/` | 301 | |
| `robots.txt` | `/robots.txt` | — | generato da `core.views.robots_txt` (disallow back-office, api, documents, area riservata, sessioni di orientamento) |

## 3. Gestione dei redirect

- Modello `cms.Redirect(old_path, new_path, permanent, note)` già presente (`apps/cms/models.py`).
- **Middleware `cms.middleware.RedirectMiddleware`** (Stage 3, da aggiungere dopo `CommonMiddleware`): su 404,
  cerca `old_path` (con e senza slash finale, query `lang` normalizzata) e risponde 301/302 verso `new_path`;
  sostituisce `<lang>` con la lingua della richiesta; le righe con `new_path` vuoto e `permanent=False`
  possono esprimere 410 Gone (convenzione: `new_path="410"`). Seed delle righe di questa tabella in
  `cms.seeds` al momento della migrazione.
- Le ancore (`#…`) non raggiungono il server: la mappa serve per aggiornare link esterni, materiali stampati e
  la comunicazione; il redirect di `/` porta comunque alla home nella lingua giusta.
- I redirect dal sub-dominio `app.` richiedono un vhost/certificato: decisione del committente.

## 4. Canonical e hreflang

- Ogni pagina emette `<link rel="canonical">` con il proprio URL localizzato e `hreflang` per `it`, `fr`, `en`,
  `ar` + `x-default` (→ `fr`, lingua sorgente) — `templates/partials/seo_head.html`.
- Le pagine legali hanno lo stesso slug in tutte le lingue e mostrano il testo ufficiale italiano (con
  `lang="it"`): canonical per lingua, contenuto identico dichiarato tramite `hreflang`.
- Pagine gated (Fase 3) non compaiono nelle sitemap finché il gate è chiuso; le sitemap sono `i18n = True`.
- Nessun parametro `?lang=` è più canonico: viene reindirizzato.

## 5. Piano di test del cutover (da eseguire in staging, mai in produzione senza istruzione)

1. Tabella §2 trasformata in test automatico (`tests/migration/test_redirects.py`): per ogni riga, richiesta
   con `Accept-Language` in 4 lingue → stato atteso e `Location` corretta.
2. Verifica che nessun redirect crei catene > 1 salto né loop (`/` → `/fr/` → 200).
3. `/sitemap.xml` valido (XML), tutte le URL rispondono 200, nessuna URL gated se il gate è chiuso.
4. `robots.txt` blocca back-office/api/documents/area riservata.
5. Header di sicurezza presenti su ogni risposta di redirect e 410.
6. Controllo link esterni conosciuti (materiali AGAMI, social) verso le vecchie ancore → nuova destinazione.
7. Dopo lo switch DNS: monitor 404 per 30 giorni; aggiungere righe `cms.Redirect` per le URL non previste.
