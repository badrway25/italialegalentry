# Evidenze audit sito attuale — indice

Raccolta read-only del 17 settembre 2026 (15:23–15:35 UTC). Report: `docs/CURRENT_SITE_AUDIT.md`.
Nessuna azione di scrittura è stata eseguita sui sistemi remoti.

> **Redazione dei dati personali.** Le catture sono state modificate dopo l'acquisizione per un solo
> motivo: i dati personali che contenevano sono sostituiti da `[REDATTO]`. Il rilievo sui dati
> personali del sito attuale è annotato nel registro privato; il dato personale non resta nel
> repository. Nessun'altra riga di `raw/` è stata toccata.

## `raw/` — risposte HTTP e sorgenti

> **Catture conservate fuori dal repository.** Le intestazioni HTTP grezze (`*.headers`),
> `wp_readme.html` e `homepage_analysis.json` descrivono versioni software, piattaforma di hosting
> e superficie tecnica esposta di un sito ancora in produzione: dal 9 ottobre 2026 sono conservate
> nel registro privato, fuori dal repository pubblico. Le righe marcate *(registro privato)* qui
> sotto restano come indice.

| File | Contenuto | Come è stato ottenuto |
|------|-----------|-----------------------|
| `legalitalentry_it_.html` | HTML (68 979 B) della homepage `https://legalitalentry.it/` (200); intestazioni nel registro privato | `curl -sS -L -D … -o …` UA "Mozilla/5.0 (audit read-only)" |
| `legalitalentry_it_sitemap_xml.html` | 301 `sitemap.xml` → `wp-sitemap.xml` + indice XML | idem |
| `sitemap_urls.txt` | Tutti gli URL dei sotto-sitemap (`/`, `/hello-world/`, `/category/uncategorized/`, `/author/[REDATTO]/`) | loop `curl` sui `<loc>` |
| `legalitalentry_it_robots_txt.html` | `robots.txt` | `curl` |
| *(registro privato)* `app_legalitalentry_it_.headers` | Vuoto: handshake TLS fallito (`SEC_E_WRONG_PRINCIPAL`, certificato di un altro dominio) | `curl` (verifica certificato attiva) |
| `app_insecure.html` | 503 "There is no SSL certificate configured for this domain"; intestazioni nel registro privato | `curl -k` |
| *(registro privato)* `homepage_analysis.json` | title, lang, meta, hreflang, canonical, script esterni, stylesheet, 20 immagini con alt, 41 heading, 36 link, 2 form con campi, conteggio stringhe vietate | Python + BeautifulSoup su `legalitalentry_it_.html` |
| `homepage_text.txt` | Testo renderizzato della homepage EN (9 680 caratteri) | idem |
| `theme_main.js` | JS del tema `italy-template` v1.0.0 (32 KB): reveal `.rv`, drawer, modali, form diagnostico con risposte precompilate, form imprese senza invio, cookie `ile_user_lang`, carosello | `curl` |
| `theme_style.css` | CSS del tema (51 KB): palette, 5 font, 11 breakpoint, 6 regole `[dir="rtl"]`, `prefers-reduced-motion`, `:focus-visible` | `curl` |
| `hello_world.html` | Post demo WordPress pubblico e indicizzato | `curl` |
| `wp_json_users.json` | `/wp-json/wp/v2/users` → risposta pubblica, utente id 1 | `curl` |
| *(registro privato)* `wp_readme.html` | `/readme.html` raggiungibile | `curl` |

## `screenshots/` — Playwright 1.58, Chromium headless, DPR 1

| File | Descrizione |
|------|-------------|
| `home_{320,360,375,390,412,768,1024,1280,1440,1920}_fold.png` | Above-the-fold, versione EN (default `lang=en-US`) |
| `home_{…}_full.png` | Pagina intera; le sezioni sotto la piega appaiono vuote perché il tema nasconde `.rv` con `opacity:0` fino all'IntersectionObserver (riscontro di accessibilità, §7 e §11 del report) |
| `home_ar_390_fold.png`, `home_ar_390_full.png`, `home_ar_1440_fold.png`, `home_ar_1440_full.png` | Versione araba `?lang=ar`, `dir="rtl"` |
| `home_it_1440_fold.png`, `home_fr_1440_fold.png` | Versioni italiana e francese |
| `metrics.json` | Per ogni viewport: status, tempo a `networkidle`, KB trasferiti, n. risorse, `scrollWidth`/`clientWidth` (overflow), altezza documento, font caricati, `dir`/`lang`, h1, pulsanti, link nav/footer, selettore lingua, presenza cookie banner, immagini senza alt, skip link, landmark, ancore vuote, n. form, testi < 12 px, target < 24 px, errori console, richieste fallite |

## Verifiche non archiviate come file (riportate nel report)

- `openssl s_client -connect app.legalitalentry.it:443 -servername app.legalitalentry.it` → certificato wildcard di un altro dominio, SAN che non include `app.legalitalentry.it` (soggetto, emittente e validità nel registro privato).
- `nslookup` dei due host → due hosting distinti (indirizzi IPv4 e fornitori nel registro privato).
- `curl -I http://app.legalitalentry.it/` → 403 Forbidden.
- Route: `/ar/`, `/fr/`, `/it/`, `/privacy-policy/` → 404; `/?lang=ar` → 200; endpoint tecnici del CMS verificati in sola lettura (esiti nel registro privato).

## Riproduzione

Gli script di acquisizione sono stati eseguiti inline (Python 3.13 + BeautifulSoup + Playwright) e non sono ancora consolidati in un comando del repository. Parametri essenziali per riprodurre: `PYTHONIOENCODING=utf-8`; UA `Mozilla/5.0 (audit read-only) Chrome/128`; Chromium headless, DPR 1; viewport 320/360/375/390/412/768/1024/1280/1440/1920 × 800–900 px; `page.goto(url, wait_until="networkidle", timeout=60000)`; attesa aggiuntiva 1,2–1,5 s prima dello screenshot; metriche via `page.evaluate` sul DOM (`performance.getEntriesByType`, `scrollWidth/clientWidth`, `getBoundingClientRect` per i target, `getComputedStyle().fontSize` per i testi).
