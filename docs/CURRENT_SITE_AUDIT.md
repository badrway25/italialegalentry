# Audit del sito attuale — legalitalentry.it / app.legalitalentry.it

**Data verifica:** 17 settembre 2026, 15:23–15:35 UTC (17:23–17:35 CEST)
**Modalità:** esclusivamente read-only (nessuna modifica al sito, al DNS, ai form o ai sistemi remoti)
**Autore:** team di audit (UX Architecture · Web Performance · Security · Accessibility · Legal Content)
**Evidenze:** `docs/audit/current-site/` (indice in `docs/audit/current-site/README.md`)

---

## 0. Sintesi esecutiva

Il sito pubblico è una **singola pagina WordPress** (tema custom `italy-template`) con navigazione ad ancore. La piattaforma `app.legalitalentry.it` **non è disponibile**: risponde 503 con certificato TLS errato. Il sito contiene **tutte** le formulazioni che il Documento di implementazione del 14 settembre 2026 impone di eliminare, non possiede **nessuna** delle cinque pagine legali, hotlinka 20 immagini Unsplash e 5 famiglie Google Fonts, carica uno script marketing di terze parti (Hostinger Reach) e presenta form che **simulano** una registrazione senza inviare nulla.

### Tabella di severità

| # | Area | Riscontro | Severità |
|---|------|-----------|----------|
| S1 | Legal | Le 5 pagine legali (Legal Notices, Privacy, Cookie, Terms, Disclaimers) sono tutte l'ancora `#apropos`; nessuna route autonoma; nessuna informativa privacy collegata ai form | **Critical** |
| S2 | Contenuti | Presenti "Recruit in Morocco, with Methodology", "Find Qualified Profiles", "MATCHING", "matching with Italian enterprises", "regulated enterprise matching", "Enterprise Area — Submit a Recruitment Request", "positions or requested profiles" | **Critical** |
| S3 | Piattaforma | `app.legalitalentry.it` → 503 "There is no SSL certificate configured for this domain", certificato TLS non valido per il nome; 8 link della homepage puntano lì (4 in `http://`) | **Critical** |
| S4 | Form | Form aziende senza consenso, senza backend: il click su "Express Interest" mostra "La richiesta è stata registrata con successo … entro 48 ore" ma **non invia nulla** (`main.js` r. 322–334) | **Critical** (UX ingannevole + GDPR) |
| S5 | Privacy | Script terzo `cdn-reach.hostinger.com/js/embed.js` (Hostinger Reach, marketing/newsletter) + Google Fonts + Unsplash: trasmissione IP a terzi in contrasto con la Cookie Policy prescritta ("esclusivamente cookie tecnici") | **High** |
| S6 | Responsive | Overflow orizzontale: `scrollWidth` 404 px con viewport 320/360/375/390 px; 1028 px a 1024 px; menu che va a capo su tre righe a 1024 px | **High** |
| S7 | Accessibility | Nessun skip link; 25 target < 24 px; 20 nodi di testo < 12 px; contenuti nascosti da `.rv` (opacity 0) fino all'intersezione; `alert()` nativo per la validazione | **High** |
| S8 | Performance | 9,7–23,4 s a `networkidle`; 1,1–1,6 MB trasferiti per una pagina di testo; immagine Unsplash bloccata (`ERR_BLOCKED_BY_ORB`) | **High** |
| S9 | SEO | `<title>` = "legalitalentry.it"; nessuna meta description, canonical, OG, hreflang, JSON-LD; sitemap con 1 pagina + "Hello world!" + pagina autore | **High** |
| S10 | Security headers | Intestazioni di sicurezza incomplete, superficie tecnica esposta e un rilievo sui dati personali del sito attuale. Dettagli nel registro privato | **High** |
| S11 | Marchio | Pagina senza "®" (corretto), ma il logo raster contiene tagline "DIGITAL PATHWAYS TO ITALY" e una porta, entrambi nell'elenco di rimozione della Fase 3 §3.1 | **Medium** (LOGO_PENDING_CLIENT_CONFIRMATION) |
| S12 | Multilingua | Traduzioni IT/FR/AR presenti ma via `?lang=` + cookie `ile_user_lang` senza URL localizzati, senza `hreflang`, `lang="en-US"` di default; RTL applicato con sole 6 regole `[dir="rtl"]` | **Medium** |
| S13 | Direzione artistica | Immagini stereotipate (porta monumentale, Colosseo, Fontana di Trevi, passaporti/visti) e uso "bandiera" del tricolore in header/hero; 8 sezioni con card equivalenti | **Medium** |
| S14 | Coerenza | Footer dichiara "GDPR · D.LGS. 196/2003 · LAW 09-08" e "Contents verified on 14.08.2026 — version 1.0" ma non esistono testi legali; blog WordPress di default ("Hello world!") indicizzato | **Medium** |
| S15 | Design system | 5 famiglie tipografiche (Cormorant Garamond, Source Sans 3, IBM Plex Mono, Amiri, Tajawal) e 11 breakpoint diversi (480…1020 px) | **Low** |

---

## 1. Metodologia e strumenti

| Strumento | Uso | Evidenza |
|-----------|-----|----------|
| `curl` 8.x (schannel) | Header HTTP, redirect, status, TLS, sitemap, robots, endpoint WordPress | `raw/*.html`, `raw/sitemap_urls.txt`; intestazioni HTTP grezze nel registro privato |
| `openssl s_client` | Ispezione certificato `app.legalitalentry.it` | riportato in §9 |
| `nslookup` | Risoluzione DNS dei due host | riportato in §9 |
| Python 3.13 + BeautifulSoup 4.14 | Estrazione testo, heading, link, form, meta, script, immagini; conteggio stringhe vietate | `raw/homepage_text.txt`; `homepage_analysis.json` nel registro privato |
| Playwright 1.58 (Chromium headless) | Screenshot fold + full-page a 320/360/375/390/412/768/1024/1280/1440/1920 px; varianti `?lang=ar` (390, 1440), `?lang=it`, `?lang=fr`; metriche DOM (overflow, landmark, tap target, font size, immagini senza alt, console, richieste fallite, `performance` API) | `screenshots/*.png`, `screenshots/metrics.json` |
| Analisi statica | `theme_main.js` (32 KB) e `theme_style.css` (51 KB) del tema | `raw/theme_main.js`, `raw/theme_style.css` |

Nessun test intrusivo, nessun invio di form, nessuna autenticazione tentata. Lo screenshot full-page rende "vuote" le sezioni sotto la piega perché il tema applica `opacity:0` alle classi `.rv` fino all'IntersectionObserver: è di per sé un riscontro (vedi §7).

---

## 2. Inventario reale del sito

### 2.1 Sitemap reale

`https://legalitalentry.it/sitemap.xml` → 301 → `wp-sitemap.xml` (indice generato da WordPress):

| Sotto-sitemap | URL contenuti |
|---------------|---------------|
| `wp-sitemap-posts-post-1.xml` | `https://legalitalentry.it/hello-world/` (post di default WordPress, **indicizzato**) |
| `wp-sitemap-posts-page-1.xml` | `https://legalitalentry.it/` |
| `wp-sitemap-taxonomies-category-1.xml` | `/category/uncategorized/` |
| `wp-sitemap-users-1.xml` | `/author/[REDATTO]/` (pagina autore) |

Route testate: `/ar/`, `/fr/`, `/it/`, `/privacy-policy/` → **404**. `/?lang=ar` → 200 (75 KB). Gli endpoint tecnici del CMS sono stati verificati in sola lettura: esiti nel registro privato.

**Perché è un problema:** il sito è un'unica pagina lunga 8 455 px (desktop) / 14 154–15 823 px (mobile) senza URL di secondo livello. Nessun contenuto ha una URL propria: impossibile linkare una pagina legale, un percorso o il Forum; impossibile per un motore di ricerca indicizzare sezioni; impossibile misurare o versionare singole pagine.

### 2.2 Struttura della homepage (ordine reale)

1. Utility bar (tricolore, "ITALY · MOROCCO — LEGAL MOBILITY", Enterprise Area, IT/FR/EN/AR)
2. Header con logo raster + tagline "DIGITAL PATHWAYS TO ITALY" + 6 voci + CTA "Access the Platform →" (→ `http://app.legalitalentry.it`)
3. Hero "Cross the doorway to Italy, legally." + immagine porta + 2 CTA + 3 bullet "◆"
4. Carosello "Explore Italian Opportunities" (5 slide regionali: Milano, Roma, Bologna, Torino, Firenze)
5. "Choose Your Pathway" (4 card: Work, Family, Study, Foreign Degrees)
6. "Short-Stay Visas" (4 card: Tourism, Family Visit, Business, Invitation)
7. "Four Steps, One Clear Logic" (4 step)
8. "Prepare Before Departure" (training)
9. "Recruit in Morocco, with Methodology" (3 step: State Your Needs / **MATCHING — Find Qualified Profiles** / Prepare & Monitor)
10. "What the Platform Does — and What It Does Not"
11. "An Italy – Morocco Axis" (network)
12. "AGAMI — Dialogo Giuridico Interculturale APS"
13. Legal disclaimer inline ("Contents verified on 14.08.2026 — version 1.0")
14. Footer (4 colonne, 15 link, 5 "legali" verso `#apropos`)
15. Modal "Entry Profile Assessment" (form `ile-diagnostic-form`)
16. Modal "Enterprise Area — Submit a Recruitment Request" (form `ile-enterprise-form`)

Heading: 1 `h1`, 10 `h2`, 27 `h3`, 3 `h4` (footer) — 41 heading per una sola pagina.

---

## 3. Navigazione, header, footer

**Header.** 6 voci (`Pathways`, `Short-Stay Visas`, `Training`, `Enterprises`, `Network`, `About`) tutte ancore interne; CTA primaria verso un host non funzionante. A 1024 px la voce "Short-Stay Visas" va a capo su tre righe (`screenshots/home_1024_fold.png`) perché la nav usa `flex` senza `flex-wrap` controllato né breakpoint tra 1020 e 1280 px; il CSS ha breakpoint a 1000 e 1020 px ma nessuna regola per lo spazio residuo. Nessun mega-menu, nessuna gerarchia: "Persone / Imprese / Istituzioni / Università" non esistono come ingressi.

**Utility bar.** Barra alta 48 px con bordo superiore a tre colori (verde/bianco/rosso), ripetuto anche come bordi laterali del hero: la pagina "diventa la bandiera" (vedi §8.3).

**Mobile nav.** Drawer con `aria-hidden`/`aria-expanded` gestiti correttamente (`main.js` r. 50–90), ma `document.body.style.overflow='hidden'` senza gestione del focus trap né `Escape`. A 320–390 px la utility bar spezza "ITALY · MOROCCO — LEGAL MOBILITY" su due righe e la tab "Enterprise Area" si sovrappone (`home_390_fold.png`).

**Footer.** 4 colonne, 15 link. **Tutti e 5 i link "Legal Information" puntano a `#apropos`** (stessa ancora di "About" e "The Project"): `Legal Notices`, `Privacy Policy`, `Cookie Policy`, `Terms of Use`, `Disclaimers`. "Contact" → `http://app.legalitalentry.it` (protocollo `http`, host in 503). Riga finale "GDPR · D.LGS. 196/2003 · LAW 09-08" senza alcun testo a supporto.

**Perché è un problema:** la navigazione non rappresenta l'ecosistema richiesto (quattro ingressi + Forum + Risorse + Progetto), non supporta contenuti profondi (nessuna breadcrumb, nessuna navigazione locale) e i link legali sono decorativi. Il documento §1.4 dispone esplicitamente: "pointent actuellement vers une ancre vide. Créer cinq pages autonomes".

---

## 4. Hero e CTA

| Elemento | Attuale | Documento |
|----------|---------|-----------|
| H1 | "Cross the doorway to Italy, legally." | Fase 3 §3.1: **da eliminare** |
| Overline | "A doorway, not a shortcut" (nel hero) | **da eliminare** |
| Tagline logo | "Digital Pathways to Italy" (2 occorrenze nel testo + raster nel logo) | **da eliminare** |
| Immagine | porta monumentale + Fontana di Trevi + chiave dorata (Unsplash hotlink) | **da eliminare**, senza sostituirla con immagini stereotipate |
| CTA 1 | "Start My Pathway →" → `https://app.legalitalentry.it/join` (503) | — |
| CTA 2 | "I am an Enterprise" → `https://app.legalitalentry.it/register/company` (503) | — |

Il sottotitolo attuale promette "connects you with enterprises and training bodies": formulazione di intermediazione che i Termini d'uso (Annexe art. 1) escludono ("n'exerce pas d'activité d'intermédiation … au sens de l'art. 4 du D.Lgs. 276/2003").

Bullet "No fees for initial guidance" e "Your documents remain protected" sono claim non documentati.

**Perché è un problema:** il hero comunica "porta/chiave/attraversare" — metafora di accesso fisico che il documento vieta perché evoca frontiere; il testo prescritto (§3.1 "Le parcours régulier vers l'Italie, de l'orientation à l'intégration.") è assente. Le due CTA principali del sito portano a un host non raggiungibile: il funnel primario è interrotto.

---

## 5. Form e modali

### 5.1 Form "Entry Profile Assessment" (`#ile-diagnostic-form`)

- 2 domande radio (`ile_goal` 4 opzioni, `ile_lang_lvl` 3 opzioni), nessun `action`/`method`.
- Il pulsante `#btn-submit-diagnostic` legge la scelta e mostra **risposte precompilate** hard-coded in `main.js` (r. 174–279) in 4 lingue, ad esempio "Orientamento: Ingresso per Lavoro Subordinato (Decreto Flussi / **Formazione art. 23**)" e "Consigliato: completare il modulo … per valorizzare la tua candidatura verso le aziende partner".
- Nessun salvataggio, nessun versioning delle regole, nessun disclaimer contestuale. Il riferimento all'art. 23 come canale disponibile contraddice la nota §3.3 ("ne doit jamais être présenté comme un canal déjà autorisé").
- CTA finale "Generate My Personalised Orientation →" → `http://app.legalitalentry.it` (503, `http`).

### 5.2 Form "Enterprise Area — Submit a Recruitment Request" (`#ile-enterprise-form`)

Campi reali: `Company Name *`, `Industry Sector *`, `Corporate Email / Phone *` (un solo campo per e-mail e telefono), `Estimated number of positions or requested profiles` (textarea `ent_slots`, placeholder "Descrizione delle mansioni, numero di lavoratori richiesti…").

Comportamento (`main.js` r. 305–334): validazione client con `alert()` nativo; poi `resultBox.innerHTML = "Grazie. La richiesta di contatto è stata registrata con successo. Il team … vi ricontatterà entro 48 ore lavorative."` e `form.reset()`. **Nessuna richiesta di rete.** I dati non vengono né inviati né salvati.

Assenze: nessuna casella di consenso, nessun link a informativa (che non esiste), nessun CSRF, nessuna protezione anti-spam, nessun `<form action>`.

**Perché è un problema:** (a) il form promette una presa in carico che non avviene: pratica ingannevole verso le imprese; (b) chiede "profili da reclutare" — campo vietato dal §1.1; (c) mancano tutti i campi prescritti (ragione sociale, settore, sede, referente e funzione, e-mail, telefono, profili di cui l'impresa ha bisogno, numero indicativo, qualifiche, esperienza, esigenze linguistiche, bisogni formativi, calendario, note, consenso obbligatorio); (d) il titolo contiene "Recruitment Request" da eliminare.

### 5.3 Modali

Apertura via `[data-open-modal]`, chiusura via `[data-close-modal]`; `preventDefault` corretto; nessun `role="dialog"`, `aria-modal`, focus trap o ritorno del focus all'elemento scatenante (`main.js` r. 86–130). Il pulsante "❚❚" (pausa carosello) è un glifo testuale senza etichetta accessibile.

---

## 6. Link

36 link unici nella homepage:

| Categoria | N. | Dettaglio |
|-----------|----|-----------|
| Ancore interne | 17 | `#apropos` ×7, `#parcours` ×5, `#entreprises` ×2, `#formation`, `#reseau`, `#visas` |
| Verso `app.legalitalentry.it` (503) | 14 | di cui **4 in `http://`** ("Generate My Personalised Orientation", "Contact", "Submit Contact Request", "Access the Platform") → redirect/mixed content e 403 Apache su `http` |
| Selettore lingua | 4 | `/?lang=it|fr|en|ar` (query string, non URL localizzate) |
| Logo | 1 | `https://legalitalentry.it/?lang=en` |

Link "vuoti" (`href="#"`): 0. Link legali autonomi: 0. Link a fonti ufficiali (Ministeri, Questure, EU Immigration Portal): 0.

---

## 7. Responsive, mobile, tablet, desktop

Metriche da `screenshots/metrics.json` (Chromium, DPR 1, `networkidle`):

| Viewport | `scrollWidth` | Overflow | Altezza pagina | Trasferito | Risorse | Tempo `networkidle` |
|----------|---------------|----------|----------------|------------|---------|---------------------|
| 320 | 404 | **sì (+84 px)** | 15 823 px | 1 347 KB | 13 | 23,4 s |
| 360 | 404 | **sì (+44 px)** | 15 056 px | 1 380 KB | 14 | 13,2 s |
| 375 | 404 | **sì (+29 px)** | 14 637 px | 1 422 KB | 15 | 9,7 s |
| 390 | 404 | **sì (+14 px)** | 14 579 px | 1 422 KB | 15 | 13,2 s |
| 412 | 412 | no | 14 336 px | 1 422 KB | 15 | 15,2 s |
| 768 | 768 | no | 10 687 px | 1 536 KB | 17 | 13,4 s |
| 1024 | 1028 | **sì (+4 px)** | 8 524 px | 1 595 KB | 21 | 19,6 s |
| 1280 | 1280 | no | 8 455 px | 1 137 KB | 20 | 13,2 s |
| 1440 | 1440 | no | 8 455 px | 1 137 KB | 20 | 9,9 s |
| 1920 | 1920 | no | 8 455 px | 1 595 KB | 21 | 13,1 s |

Costanti su tutti i viewport: 20 immagini (0 senza alt), 2 form, 25 target interattivi con larghezza o altezza < 24 px, 20 nodi testuali < 12 px, skip link assente, 1 `main`/`nav`/`header`/`footer`.

**Analisi tecnica.**
- L'overflow a 320–390 px deriva da un elemento a larghezza fissa ~404 px (carosello `slide-card` / hero art con `min-width`): la pagina scorre lateralmente, l'utente vede una banda bianca a destra e i pulsanti possono uscire dal viewport.
- L'overflow a 1024 px (+4 px) deriva dal CTA "Access the Platform" a larghezza fissa più il menu a 6 voci: il tema ha breakpoint 1000/1020 ma non gestisce 1024–1279.
- Altezza mobile 14–15 k px = circa **18–20 schermate** di scroll per una singola pagina: costo cognitivo elevato, nessun sommario, nessuna navigazione locale.
- Il tema usa 11 breakpoint distinti (`480, 520, 560, 640, 680, 760, 768, 820, 1000, 1020`): assenza di una scala di layout coerente, sintomo di correzioni puntuali "desktop-first".

Evidenze: `home_320_fold.png`, `home_390_fold.png`, `home_768_full.png`, `home_1024_fold.png`.

---

## 8. Contenuti, immagini, tipografia, palette, spaziatura

### 8.1 Formulazioni vietate (conteggio nel testo renderizzato EN)

| Stringa | Occorrenze | Riferimento documento |
|---------|-----------:|-----------------------|
| `Recruit in Morocco` | 1 (h2 "Recruit in Morocco, with Methodology") | §1.1 |
| `Find Qualified Profiles` | 1 (h3) | §1.1 |
| `MATCHING` | 1 (etichetta "02 — MATCHING") + `matching` 3 (minuscolo) | §1.1 "toutes les occurrences" |
| `matching with Italian enterprises` | 1 (card Work in Italy) | §1.2 |
| `regulated enterprise matching` | 1 (step 04 Pre-Departure Support) | §1.2 |
| `Enterprise Area` | 3 (utility bar, footer, titolo modal) | §1.1 |
| `Submit a Recruitment Request` | 1 (h3 modal) | §1.1 |
| `positions or requested profiles` | 1 (label form) | §1.1 |
| `Cross the doorway to Italy` | 1 (h1) | §3.1 |
| `A doorway, not a shortcut` | 1 | §3.1 |
| `Digital Pathways to Italy` | 2 testo + raster nel logo | §3.1 |
| `Explore Italian Opportunities` | 1 (carosello) | §3.7 (spostare/ridurre) |
| `Registered trademark` / `Marchio registrato` / `Marque enregistrée` / `®` | 0 | §1.3 — conforme; da mantenere sotto test |
| `™` | 0 | §1.3 richiede "Italy Legal Entry™" ovunque sia citato il marchio: **assente** |
| `@legalitalentry.it` | 0 indirizzi e-mail | §1.1 nota — conforme |
| `contact@agamieuromed.org` | 0 | l'unico canale di contatto è un host in 503 |

Altri contenuti problematici: "connects you with employers, with your consent", "Ranked results … with scores justified line by line" (descrizione di un sistema di selezione e classificazione candidati), "Anonymized profiles by default", "One listing per offer, one cohort per project", "Recommended: complete the … modules to strengthen your application with partner companies". Sono descrizioni di intermediazione di manodopera incompatibili con Termini art. 1.

Contenuti assenti richiesti dal documento: testo Espace Entreprises §1.1, Espace Personnes §3.3, Institutions §3.4, Universités §3.5, Projet pilote §3.6, Attention aux fraudes §3.8.1, FAQ §3.8.2, Glossaire §3.8.3, Vivre en Italie §3.8.4, Formation après l'arrivée §3.8.5, Actualités §3.8.6, Forum Virtuel §3.8.7, Diplômes §3.9, Espace réservé §3.10, Forum Vénétie–Maroc (intera Fase 2).

### 8.2 Immagini

20 `<img>`, **tutte** hotlinkate da `images.unsplash.com` con parametri `auto=format&fit=crop&w=…`. Una (`photo-1563276326…`, Bologna) fallisce con `net::ERR_BLOCKED_BY_ORB`. Soggetti: porta monumentale (hero), Duomo di Milano, Colosseo, portici di Bologna, Torino, Ponte Vecchio, "Visto Turismo — Venezia", "Visto Visita familiare", "Visto Affari — Milano Business", "Visto Invito", quattro immagini "Passo 1–4", "Imprese italiane e selezione qualificata", "Casablanca e Rabat sportelli", "Roma e Milano rete", "Dialogo Giuridico".

**Perché è un problema:** (a) ogni visita trasmette l'IP dell'utente a Unsplash (fornitore USA) senza informativa; (b) nessuna licenza/attribuzione registrata; (c) immagini a 1400 px caricate anche a 320 px (nessun `srcset`/`sizes`, nessun `loading="lazy"` rilevato nel markup, nessun WebP/AVIF self-hosted); (d) l'immaginario "porta / monumenti-cartolina / visti" è esattamente quello che la Fase 3 esclude (frontiere, porte, passaporti) e non comunica imprese, formazione, università, cooperazione.

### 8.3 Tipografia e palette

Font: 5 famiglie da `fonts.googleapis.com` (Amiri, Cormorant Garamond, IBM Plex Mono, Source Sans 3, Tajawal) con `display=swap`: richiesta esterna a Google a ogni visita (IP → Google, rilevante per la Cookie Policy prescritta e per la giurisprudenza tedesca/italiana sui Google Fonts), FOUT sistematico, nessun `preload`, nessun self-hosting. `IBM Plex Mono` è usato in **28 regole** per etichette/overline (stile "terminale"), poco leggibile in arabo e incoerente con un registro istituzionale.

Palette dichiarata nel CSS: `#0F2547` / `#16325C` (navy), `#157A3C` (verde), `#C4142B` (rosso), `#C39A2B` / `#E3C871` (oro), `#FCFBF8` / `#F3F0E9` / `#DDD8CC` (fondi), `#5D6472` (grigio). La combinazione verde+bianco+rosso è applicata come **bordi tricolori** (utility bar, lati del hero, logo, sottolineatura del logo): il sito "è" la bandiera, effetto che il master prompt e il documento chiedono di evitare. Il rosso `#C4142B` è usato come colore di marca nel wordmark ("ENTRY"): sul navy scuro il contrasto stimato è < 4.5:1 per testo piccolo. L'oro `#E3C871` su fondo chiaro (`#FCFBF8`) per bullet e overline ha contrasto ≈ 1.8:1 — fallisce WCAG 1.4.3 e 1.4.11.

Spaziatura: sezioni alternate navy/avorio a piena larghezza senza ritmo verticale definito; ogni sezione contiene 3–5 card equivalenti (`.card`, `.slide-card`, `.visa-media`, `.step-media`, `.pole-media`): nessuna gerarchia tra "ingressi" e "informazione secondaria".

### 8.4 Coerenza

- Footer: "GDPR · D.LGS. 196/2003 · LAW 09-08" senza testi; "Contents verified on 14.08.2026 — version 1.0" senza indicazione di cosa sia stato verificato.
- Blog WordPress con "Hello world!" pubblico e indicizzato, con la sua pagina autore.
- Mix di lingue nella versione EN: "Lavoro & Industria", "PARTNERSHIP INDUSTRIALE ITALIA-MAROCCO", "ETICA & LEGALITÀ", "AULA & DIGITALE" restano in italiano.
- Il logo mostra "DIGITAL PATHWAYS TO ITALY" in EN/IT/FR, tradotto solo nella versione AR (raster diverso).

---

## 9. app.legalitalentry.it — stato verificato

| Verifica | Risultato (2026-09-17 15:24 UTC) |
|----------|----------------------------------|
| DNS | `app.legalitalentry.it` → CNAME verso un hosting terzo, diverso da quello di `legalitalentry.it` (indirizzi IPv4 e fornitori nel registro privato) |
| HTTPS | `curl` → `SEC_E_WRONG_PRINCIPAL`: certificato wildcard di un altro dominio (soggetto, emittente e validità nel registro privato), SAN non include `app.legalitalentry.it` |
| HTTPS con `-k` | **503 Service Temporarily Unavailable**, body "SSL Error — There is no SSL certificate configured for this domain" |
| HTTP | **403 Forbidden** |
| Conclusione | **NON DISPONIBILE.** Il sottodominio è parcheggiato su un hosting diverso senza certificato né applicazione. Conferma l'ipotesi "502/non disponibile" del brief. 14 link della homepage (comprese entrambe le CTA del hero e "Contact") sono quindi rotti. |

Evidenza: `raw/app_insecure.html`; intestazioni HTTP grezze nel registro privato.

---

## 10. Multilingua e RTL

**Meccanismo.** Il tema serve la lingua tramite query `?lang=xx` e cookie `ile_user_lang` (365 giorni, `main.js` r. 337–349); di default `lang="en-US"`. `/?lang=it` → `lang="it-IT"`, `/?lang=fr` → `lang="fr-FR"`, `/?lang=ar` → `lang="ar"`, `dir="rtl"`. Le traduzioni IT/FR/AR sono complete per il testo (h1 "Varcare la porta dell'Italia, legalmente." / "Franchir la porte de l'Italie, légalement." / "عبور بوابة إيطاليا، بشكل قانوني.").

**Problemi strutturali.**
- Nessuna URL localizzata (`/it/…`, `/fr/…`), nessun `<link rel="alternate" hreflang>`, nessun `canonical`: per i motori esiste una sola pagina inglese; le versioni sono duplicati parametrici.
- Il cookie di lingua è "tecnico" (ammesso dalla Cookie Policy), ma il selettore usa `?lang=` senza `Vary` sulla cache del server (`hit` anche sulle varianti): rischio di servire la lingua sbagliata dalla cache.
- Nessun workflow di traduzione: i testi vivono nel tema PHP/JS (i messaggi dei form sono in `main.js`).

**RTL.** `dir="rtl"` a livello di `html`; `scrollWidth` = `clientWidth` a 390/1440 px in arabo (nessun overflow, `home_ar_390_full.png`, `home_ar_1440_fold.png`). Il CSS contiene **6 sole regole** `[dir="rtl"]` (r. 2001, 2099, 2313, 2409, 2458, 2644), tutte su badge/numeri delle card: le frecce nei pulsanti sono caratteri Unicode "→/←" scelti in template, il layout si specchia per flusso naturale (`flex`) ma non esistono proprietà logiche (`margin-inline-start`, `inset-inline`) né gestione di icone direzionali, carosello (frecce prev/next), stepper, numerazione "01 / 05". Il carattere Amiri (display) per i titoli arabi ha ottima resa ma il corpo Tajawal a 15–16 px con interlinea del corpo latino risulta compresso; il logo raster in arabo è un'immagine diversa (tagline tradotta) non allineata alla baseline del wordmark.

---

## 11. Accessibilità (WCAG 2.2 AA)

| Criterio | Riscontro | Evidenza |
|----------|-----------|----------|
| 2.4.1 Bypass Blocks | Nessun skip link (`skipLink:false`) | metrics.json |
| 1.3.1 / landmark | 1 `main`, 1 `nav`, 1 `header`, 1 `footer`: OK come base | metrics.json |
| 2.5.8 Target Size (min 24 px) | **25** target < 24 px (selettore lingua, "❚❚", frecce carosello, dot slider) | metrics.json |
| 1.4.4 / leggibilità | **20** nodi di testo < 12 px (overline mono 10–11 px, footer legal) | metrics.json |
| 1.4.3 Contrast | oro `#E3C871`/`#C39A2B` su avorio per overline e bullet; rosso su navy | theme_style.css |
| 2.4.7 Focus Visible | `:focus-visible` con outline oro 2.5 px definito (r. 184–186): **positivo**, ma su fondo avorio l'oro ha contrasto insufficiente | theme_style.css |
| 2.2.2 / 2.3.3 Motion | `prefers-reduced-motion` gestito per `.rv` (r. 1799–1804): **positivo**; il carosello autoplay non espone controllo accessibile (pulsante "❚❚" senza `aria-label`) | theme_style.css, DOM |
| 4.1.2 Name/Role | Modali senza `role="dialog"`/`aria-modal`; nessun focus trap; nessun ritorno del focus | main.js |
| 3.3.1 Error Identification | Validazione con `alert()` nativo, senza `aria-describedby` né messaggi inline | main.js r. 327 |
| 1.1.1 Alt | 20/20 immagini con alt (**positivo**), ma alt descrittivi di immagini decorative ("Porta monumentale d'Italia") | `homepage_analysis.json` (registro privato) |
| Contenuto nascosto | Classi `.rv` con `opacity:0; transform` fino all'intersezione: con JS disabilitato o `IntersectionObserver` lento il contenuto resta invisibile; gli screen reader leggono contenuto che l'utente vedente non vede; la stampa e gli screenshot full-page risultano vuoti | `home_1440_full.png` |
| Lingua | `lang="en-US"` corretto per EN; blocchi in italiano nella versione EN privi di `lang="it"` | DOM |
| Zoom 200/400 % | L'overflow già presente a 320 px implica fallimento del reflow (1.4.10) a 400 % su 1280 px | metrics.json |

---

## 12. Performance

| Metrica | Valore | Budget target nuovo sito |
|---------|--------|--------------------------|
| Tempo a `networkidle` | 9,7 s (375/1440) – 23,4 s (320) | — |
| Byte trasferiti | 1 137 – 1 595 KB | < 600 KB home |
| Richieste | 13–21 | < 25 |
| Font esterni | 5 famiglie, 13 pesi, Google Fonts | 2 famiglie self-hosted, `font-display: swap`, subset |
| Immagini | 20 hotlink Unsplash 400–1400 px, nessun `srcset`, 1 bloccata da ORB | WebP/AVIF locali, `srcset`, lazy below-the-fold |
| Script terzi | `cdn-reach.hostinger.com/js/embed.js` + `hostinger-reach/…/subscription-view.js` (blocco newsletter Hostinger Reach: script di marketing con identificazione del sito, caricato su ogni pagina) | 0 script terzi |
| CSS | 51 KB non minificato, 1 file, no critical CSS | token + CSS modulare < 60 KB minificato |
| Cache | cache del server in `hit` (positivo), ma senza `Vary` per lingua | — |

La lentezza a `networkidle` deriva dalle immagini Unsplash (dimensioni non ottimizzate, connessioni a terzi) e dallo script Hostinger Reach; il tempo DOMContentLoaded non è rappresentativo perché il contenuto è nascosto dalle animazioni `.rv`. LCP reale è l'immagine hero remota: dipende da un dominio esterno non preconnesso.

---

## 13. SEO e metadata

| Elemento | Stato |
|----------|-------|
| `<title>` | "legalitalentry.it" (nome host, nessun valore semantico) |
| `meta description` | assente |
| `canonical` | assente (le 4 varianti `?lang=` sono duplicati) |
| `hreflang` | assente (solo `rel=alternate` verso feed RSS) |
| OpenGraph / Twitter | assenti |
| JSON-LD | assente (nessun `Organization`, `Event`, `Article`, `BreadcrumbList`) |
| `meta generator` | presente: espone la versione del CMS (valore nel registro privato) |
| `robots.txt` | standard WordPress, sitemap dichiarata |
| Sitemap | 1 pagina reale + 3 URL spuri (post demo, categoria "uncategorized", autore) |
| URL | nessuna URL leggibile di secondo livello |
| Heading | 41 heading in una pagina, `h4` usati nel footer come etichette di colonna |

---

## 14. Sicurezza osservabile

Intestazioni di sicurezza e superficie esposta rilevate; dettagli nel registro privato.
Tra gli endpoint WordPress di default, `/wp-json/wp/v2/users` è leggibile pubblicamente. Nelle catture ogni valore tolto è sostituito da `[REDATTO]`.
Nessuna azione intrusiva è stata eseguita (nessun tentativo di login, nessun brute force, nessuna scansione plugin).

---

## 15. Perché il design attuale è "basic" — spiegazione tecnica

1. **Assenza di architettura dell'informazione.** Un solo documento HTML con 16 sezioni sequenziali: non esistono gerarchie di navigazione, pagine di secondo livello, breadcrumb, navigazione locale. L'utente "persona", "impresa", "istituzione", "università" trova gli stessi blocchi nello stesso ordine.
2. **Card-driven layout omogeneo.** 5 sezioni consecutive con 3–5 card identiche (regioni, percorsi, visti, step, aziende): la ripetizione del modulo annulla la gerarchia visiva; nessun elemento dice all'occhio "questo è più importante". Il documento §3.7 chiede l'opposto ("réduire les encadrés, augmenter les espaces blancs").
3. **Palette applicata come decorazione.** Tricolore in bordi e wordmark; oro su avorio con contrasto 1.8:1; navy a piena larghezza alternato ad avorio. Il colore non codifica funzione (primario/secondario/semantico) ma identità nazionale letterale.
4. **Tipografia non sistematica.** 5 famiglie, mono per overline, display serif per titoli, sans per corpo, due famiglie arabe: nessuna scala modulare, dimensioni < 12 px per etichette, 11 breakpoint che rompono il ritmo verticale.
5. **Immaginario stock.** 20 immagini Unsplash di monumenti, porte e "visti" a giustificare card testuali: comunicano turismo, non cooperazione istituzionale né formazione.
6. **Interazioni a metà.** Reveal-on-scroll che nasconde il contenuto, carosello con autoplay, modali senza semantica dialog, form che simulano l'invio, `alert()`: gli elementi "dinamici" penalizzano accessibilità e fiducia invece di rafforzarle.
7. **Nessuna infrastruttura.** Nessun back-office per contenuti, nessun versioning dei testi, nessun modello dati per form/eventi/percorsi, nessun sistema di traduzione: ogni modifica richiesta dal documento comporterebbe editing manuale di PHP/JS in 4 lingue.
8. **Metadata e superficie tecnica trascurate.** Titolo = hostname, nessun canonical/hreflang/OG, header di sicurezza assenti, endpoint WordPress di default esposti, blog demo indicizzato.

Il risultato è un "sito-vetrina di presentazione" (one-pager con template custom) e non una piattaforma: ogni requisito del documento (pagine autonome, form conformi, Forum con programma editabile, FAQ/glossario/fiches gestibili, area riservata, RTL verificato) richiede un'architettura che oggi non esiste.

---

## 16. Matrice requisiti — stato attuale vs stato richiesto

Legenda stato: **ASSENTE** (da creare) · **NON CONFORME** (da trasformare) · **DA RIMUOVERE** · **CONFORME** · **GATED** (implementato ma non pubblicabile fino a condizione). App Django pianificate: `core, cms, pages, legal, accounts, consents, enquiries, ecosystem, pathways, orientation, forum, community, news, faq, glossary, living, partners, portal, documents, notifications, audit, integrations`.

### 16.1 Fase 1 (entro 17 settembre 2026)

| Requirement | Current site | Required state | Implementation (app/modulo) | Test | Status |
|---|---|---|---|---|---|
| §1.1 Rimuovere "Recruit in Morocco, with Methodology" | Presente (h2) | Assente ovunque | `ecosystem` pagina Imprese riscritta | `tests/compliance/test_forbidden_strings.py::test_no_recruit_in_morocco` | DA RIMUOVERE |
| §1.1 Rimuovere "Find Qualified Profiles" + descrizione selezione/classificazione | Presente (h3 + "Ranked results…") | Assente | `ecosystem` | `…::test_no_find_qualified_profiles` | DA RIMUOVERE |
| §1.1 Rimuovere "MATCHING" (tutte le occorrenze, tutte le pagine) | 1 MATCHING + 3 matching | Assente | tutte le app; template lint | `…::test_no_matching` (scan di tutte le route pubbliche in 4 lingue) | DA RIMUOVERE |
| §1.1 Rimuovere "Enterprise Area — Submit a Recruitment Request" | Presente (modal) | Assente | `ecosystem`/`enquiries` | `…::test_no_recruitment_request` | DA RIMUOVERE |
| §1.1 Rimuovere campo "positions or requested profiles" e ogni campo che chieda candidati | Presente (`ent_slots`) | Assente | `enquiries.forms.CompanyNeedsForm` | `tests/enquiries/test_company_form.py::test_no_candidate_fields` | DA RIMUOVERE |
| §1.1 Inserire titolo/intro/messaggio centrale Imprese (testo esatto) | Assente | Testo letterale FR (IT/AR da trasmettere) | `ecosystem` + `cms` content lock | `tests/compliance/test_locked_content.py::test_company_intro_exact` | ASSENTE |
| §1.1 Form "Recueil des besoins" con 15 campi nell'ordine prescritto + consenso obbligatorio | 4 campi, nessun consenso | 15 campi + checkbox testo esatto | `enquiries.CompanyNeedsRequest`, `consents` | `tests/enquiries/test_company_form.py::test_field_order`, `::test_consent_required` | NON CONFORME |
| §1.1 CTA "MANIFESTEZ VOTRE INTÉRÊT POUR LE PROJET" | "Express Interest →" | Testo esatto | `ecosystem` template | `…::test_company_cta_exact` | NON CONFORME |
| §1.1 nota — form instradati solo a `contact@agamieuromed.org`; nessun `@legalitalentry.it` pubblico | Nessun invio; nessun indirizzo | Config centralizzata `FORMS_RECIPIENT_EMAIL`; test su output pubblico | `core.settings`, `notifications` | `tests/compliance/test_public_email.py` | NON CONFORME |
| §1.2 Sostituire "matching with Italian enterprises" con testo prescritto | Presente | "orientation vers des parcours de formation et de mobilité régulière, construits avec les acteurs compétents" | `pathways` | `…::test_person_replacement_1` | NON CONFORME |
| §1.2 Sostituire "regulated enterprise matching" con testo prescritto | Presente | "recueil des besoins des entreprises et construction de parcours réguliers de formation et de mobilité" | `pathways` | `…::test_person_replacement_2` | NON CONFORME |
| §1.3 Mai "Marchio registrato / Registered trademark / Marque enregistrée"; mai "®" | Assenti (0) | Assenti + test permanente | `core` templatetag `brand` | `tests/compliance/test_trademark.py::test_no_registered_symbol` | CONFORME (da proteggere) |
| §1.3 "Italy Legal Entry™" ovunque sia citato il marchio; "marque déposée"/"marchio depositato" in lettere | "™" assente (0) | Presente in header, footer, hero, legal | `core` templatetag `brand` | `…::test_tm_present` | NON CONFORME |
| §1.4 Cinque pagine legali autonome (IT ufficiale, FR/EN/AR rinviano all'italiano) | 5 link → `#apropos` | 5 route autonome `/legal/…`; testo IT da Allegato 1 | `legal` (modello `LegalDocument` versionato) | `tests/legal/test_routes.py::test_five_distinct_routes` | ASSENTE — **BLOCKED_BY_MISSING_OFFICIAL_SOURCE** (Allegato 1 italiano non presente tra le fonti ricevute) |
| §1.4 Non pubblicare la nota operativa interna della Cookie Policy | n/a | Esclusa | `legal` fixture | `tests/legal/test_cookie_policy_no_internal_note.py` | ASSENTE |
| §1.4 Gate: form attivi solo se le pagine legali sono online | Form "attivi" senza informativa | Publication gate `legal_pages_published()` che disattiva i form pubblici | `legal.gates`, `enquiries`, `forum` | `tests/legal/test_publication_gate.py` | ASSENTE |
| §1.4 Conferma scritta hosting UE (prestatore + localizzazione) | due fornitori di hosting distinti per sito e app (nomi nel registro privato): localizzazione non dichiarata | Da documentare in `docs/DEPLOYMENT.md` prima del deploy | `docs` | — | ASSENTE (blocco esterno) |
| Indicazione di versione a piè di pagina aggiornata a fine fase | "version 1.0 — 14.08.2026" | Versione gestita da CMS (`SiteSettings.content_version`) | `cms` | `tests/cms/test_footer_version.py` | NON CONFORME |

### 16.2 Fase 2 (entro 25 settembre 2026)

| Requirement | Current site | Required state | Implementation | Test | Status |
|---|---|---|---|---|---|
| §2.1 Pagina "Forum Vénétie–Maroc" con header esatto (titolo, sottotitolo, Rovigo — 2 ottobre 2026 — Sala della Gran Guardia — 15h00–18h00, patrocinio) | Assente | Pagina evento premium | `forum.ForumEvent` + template | `tests/forum/test_event_page.py::test_header_exact` | ASSENTE |
| §2.1 Spazi per loghi Regione Veneto e Comune di Rovigo (senza inventarli) | Assente | Slot `ForumPartner` con placeholder solo in admin | `forum.ForumPartner`, `partners` | `tests/forum/test_partners.py::test_no_fake_logos_public` | ASSENTE |
| §2.1 Sezioni QUI SOMMES-NOUS, POURQUOI, QU'EST-CE QUE, OBJECTIFS, À QUI S'ADRESSE-T-IL (testi esatti) | Assenti | Content lock | `forum` + `cms` | `tests/compliance/test_locked_content.py::test_forum_sections` | ASSENTE |
| §2.1 PROGRAMME modificabile dal back-office (8 voci + nota) | Assente | `ForumProgramItem` inline in admin | `forum` | `tests/forum/test_program.py::test_admin_editable`, `::test_default_items_exact` | ASSENTE |
| §2.1 INTERVIENNENT: solo funzioni, nessun nome | Assente | `SpeakerRole` senza campo nome pubblicato finché non autorizzato | `forum.SpeakerRole` | `tests/forum/test_speakers.py::test_no_names_public` | ASSENTE |
| §2.1 INSCRIPTION: 9 campi nell'ordine + 8 categorie esatte + consenso + CTA "PARTICIPEZ AU FORUM" | Assente | `ForumRegistrationForm` | `forum`, `consents` | `tests/forum/test_registration.py::test_field_order`, `::test_categories_exact`, `::test_consent_required`, `::test_rate_limit`, `::test_duplicate` | ASSENTE |
| §2.1 CTA secondarie → form Imprese (§1.1) e "PROPOSEZ UNE COLLABORATION" | Assente | Link a `ecosystem:company`, `ecosystem:institution` | `forum` template | `…::test_secondary_ctas` | ASSENTE |
| §2.1 nota — dopo il 2 ottobre la pagina diventa FORUM PERMANENT: foto, video, documenti, interventi, accordi, convenzioni, partner, risultati, prossimi appuntamenti | Assente | Modelli `ForumMedia/Document/Agreement/Outcome/NextEvent` + `phase` switch da admin | `forum` | `tests/forum/test_permanent_mode.py` | ASSENTE |
| §2.1 nota — link informativa → Privacy Policy italiana | Assente | Link a `legal:privacy` (gated) | `forum` | `tests/forum/test_registration.py::test_privacy_link_it` | ASSENTE |
| §2.2 Banner Forum in homepage fino al 2 ottobre (testo esatto + pulsante "DÉCOUVREZ LE FORUM") | Assente | `cms.Announcement` con `publish_from/publish_until` | `cms` | `tests/cms/test_forum_banner.py::test_visible_before_oct_2`, `::test_hidden_after` | ASSENTE |

### 16.3 Fase 3 (dopo il 2 ottobre 2026 — implementare ora, gated)

| Requirement | Current site | Required state | Implementation | Test | Status |
|---|---|---|---|---|---|
| §3.1 Rimuovere immagine porta, "Cross the doorway…", "A doorway, not a shortcut", "Digital Pathways to Italy" | Tutti presenti | Assenti; hero nuovo con testo esatto | `pages` Home + `cms.HeroVariant` (scheduled) | `tests/compliance/test_forbidden_strings.py::test_no_phase3_hero_legacy` | DA RIMUOVERE / GATED |
| §3.1 Nessuna immagine stereotipata; immagini imprese/formazione/università/cooperazione | Monumenti, porta, visti | Immagini locali licenziate | `static/img` + `docs/IMAGE_LICENSES.md` | `tests/compliance/test_no_hotlinked_images.py` | NON CONFORME |
| §3.2 Esattamente 4 accessi (Persona, Impresa, Istituzione, Università) con testi e pulsanti esatti | 4 card "pathway" + 4 "visa" + 4 step… | 4 blocchi, nessun altro riquadro | `pages` Home | `tests/pages/test_home.py::test_four_entrances_exact` | ASSENTE |
| §3.3 Espace Personnes: intro esatta, 8 percorsi con descrizioni esatte, riquadro "Comment ça marche", accesso al questionario | 4 card + 4 visti | Pagina + 8 pagine percorso | `pathways` | `tests/pathways/test_persons.py::test_intro_exact`, `::test_eight_pathways_exact` | ASSENTE |
| §3.3 nota — nessuna promessa di visto/tempi; art. 23 mai presentato come canale autorizzato | Diagnostic form cita "Formazione art. 23" come esito | Disclaimer + lint su "garantit/garantito/guaranteed" | `orientation` | `tests/compliance/test_no_promises.py` | NON CONFORME |
| §3.4 Espace Institutions (testo + pulsante esatti) | Assente | Pagina + form collaborazione | `ecosystem`, `enquiries.InstitutionProposal` | `tests/ecosystem/test_institutions.py` | ASSENTE |
| §3.5 Espace Universités et Formation (testo + pulsante esatti) | Assente | Pagina + form partenariato | `ecosystem`, `enquiries.UniversityPartnership` | `tests/ecosystem/test_universities.py` | ASSENTE |
| §3.6 Progetto Pilota Vénétie–Maroc con sequenza grafica 8 tappe; mai "autorizzato" | Assente | Pagina + diagramma SVG responsive | `pages`/`ecosystem` | `tests/pages/test_pilot.py::test_sequence_exact`, `::test_no_authorized_wording` | ASSENTE |
| §3.7 Meno riquadri, più bianco, carosello "Explore Italian Opportunities" spostato/ridotto nello spazio Persone; verifica RTL; versione a piè di pagina | Carosello in home | Design system + RTL QA | `core` design tokens; `docs/I18N_RTL.md` | `tests/e2e/test_rtl.py` | NON CONFORME |
| §3.8.1 "Attention aux fraudes" (testo esatto) in Espace Personnes e footer | Assente | Sezione + richiami | `pathways`, `core` footer | `tests/compliance/test_locked_content.py::test_antifraud_exact` | ASSENTE |
| §3.8.2 FAQ (9 domande/risposte esatte) | Assente | `faq.FAQItem` con contenuto bloccato | `faq` | `tests/faq/test_locked_faq.py` | ASSENTE |
| §3.8.3 Glossario (10 termini esatti) | Assente | `glossary.Term` | `glossary` | `tests/glossary/test_locked_terms.py` | ASSENTE |
| §3.8.4 "Vivre en Italie" (testo esatto) + fiches tematiche da back-office | Assente | `living.Sheet` per categoria | `living` | `tests/living/test_intro_exact.py` | ASSENTE |
| §3.8.5 "Formation après l'arrivée" (testo esatto), accanto a formazione pre-partenza; attestazioni senza valore amministrativo | Sezione training generica con "CERTIFICATES" | Due sezioni collegate | `pathways`/`pages` | `tests/compliance/test_locked_content.py::test_training_after_arrival` | ASSENTE |
| §3.8.6 Actualités + newsletter con consenso separato non preselezionato (testo esatto) | Blocco Hostinger Reach (newsletter di terzi) | `news.Article` workflow + `consents.NewsletterConsent` | `news`, `consents` | `tests/news/test_newsletter_consent.py::test_not_prechecked` | NON CONFORME |
| §3.8.7 Forum Virtuale (testo esatto, pulsante; riservato, autenticato, moderato, profili per categoria; lancio dopo 29–30 ottobre) | Assente | `community` dietro feature flag | `community`, `accounts` | `tests/community/test_feature_flag.py`, `::test_privacy_default` | ASSENTE / GATED |
| §3.9 Diplômes et titres étrangers (testo esatto; mai "riconosce") | Card "Foreign Degrees" con "Academic recognition, equivalence" | Pagina dedicata | `pathways` | `tests/compliance/test_no_recognition_claims.py` | NON CONFORME |
| §3.10 Espace réservé (testo esatto + "CONNEXION"); CRM non protagonista; ogni categoria vede solo i propri dati | "Access the Platform" verso host in 503 | `portal` + RBAC deny-by-default | `accounts`, `portal` | `tests/portal/test_permissions.py::test_company_isolation`, `::test_person_isolation`, `::test_idor` | ASSENTE |
| §3.11 Elementi da trasmettere (programma definitivo, loghi, nomi, IT/AR dei nuovi contenuti, traduzioni legali, caselle e-mail) | — | Tracciati come blocchi esterni | `docs/LEGAL_AND_PUBLICATION_GATES.md` | — | GATED (esterno) |

### 16.4 Verifiche del master prompt (§8)

| Requirement | Current site | Required state | Implementation | Test | Status |
|---|---|---|---|---|---|
| Link Legal Notices / Privacy / Cookie / Terms / Disclaimers con route autonome, non alias | 5 × `#apropos` | 5 route distinte, contenuti distinti | `legal` | `tests/legal/test_routes.py::test_not_aliases` | NON CONFORME |
| Nessun `®` | 0 | 0 + test | `core` | `tests/compliance/test_trademark.py` | CONFORME |
| Nessuna e-mail `@legalitalentry.it` pubblica | 0 | 0 + test | `core` | `tests/compliance/test_public_email.py` | CONFORME |
| Nessun analytics/tracking di terzi | Hostinger Reach embed.js + Google Fonts + Unsplash | 0 richieste a terzi | `core` CSP + test statico | `tests/compliance/test_no_third_party.py` | NON CONFORME |
| app.legalitalentry.it funzionante | 503 + cert errato | Fuori ambito locale; documentare | `docs/DEPLOYMENT.md` | — | NON DISPONIBILE |

---

## 17. Classificazione degli interventi

**Da rimuovere (mai reintrodurre, coperto da test):** "Recruit in Morocco, with Methodology"; "Find Qualified Profiles" e il sistema di ranking; "MATCHING"/"matching"; "Enterprise Area — Submit a Recruitment Request"; campo "positions or requested profiles"; "matching with Italian enterprises"; "regulated enterprise matching"; "Cross the doorway to Italy, legally"; "A doorway, not a shortcut"; "Digital Pathways to Italy"; immagine della porta; carosello "Explore Italian Opportunities" in homepage; blocco "Short-Stay Visas" come sezione di primo livello (diventa "Altri percorsi/visti brevi" nell'Espace Personnes); script Hostinger Reach; Google Fonts remoti; immagini Unsplash hotlinkate; blog demo "Hello world!"; link `http://` verso `app.`.

**Da trasformare:** sezione Imprese → "Recueil des besoins" (testo e form prescritti); card percorsi → Espace Personnes con 8 percorsi e questionario; "Four Steps" → "Comment ça marche" (testo prescritto); training → "Formation avant le départ / après l'arrivée"; "What we do / do not do" → mantenere come trust block riallineato ai Termini; "AGAMI" block → ecosistema istituzionale; footer → 5 pagine legali reali + anti-frode + versione da CMS; selettore lingua → URL localizzate con `hreflang`; palette tricolore → sistema di token istituzionale; logo → wordmark tipografico "Italy Legal Entry™" con logo raster caricabile da CMS solo dopo conferma (LOGO_PENDING_CLIENT_CONFIRMATION).

**Nuovo:** Forum Vénétie–Maroc (pagina, programma, iscrizioni, partner, modalità permanente); banner homepage schedulato; quattro accessi; Espace Institutions; Espace Universités; Progetto pilota con diagramma; Attention aux fraudes; FAQ; Glossario; Vivere in Italia; Diplomi e titoli; News + newsletter; Espace réservé con RBAC; Forum Virtuale (flag); CMS con workflow e scheduling; test di conformità contenuti; header di sicurezza; sitemap/metadata/JSON-LD.

**Temporaneamente gated:** pagine legali (BLOCKED_BY_MISSING_OFFICIAL_SOURCE → form pubblici disattivati dal gate); hero e contenuti Fase 3 (scheduled ≥ 2 ottobre 2026 / autorizzazione); Forum Virtuale (feature flag, lancio post 29–30 ottobre 2026); loghi Regione/Comune (placeholder solo in admin); nomi degli intervenenti (solo funzioni); versioni IT/AR dei nuovi testi (FR fa fede nel frattempo; IT/AR marcati `TRANSLATION_PENDING`).

---

## 18. Nota sul logo

Il file fornito (`logoItalyLegalEntry.jpeg`, 1536×1024; variante quadrata usata dal sito AGAMI) contiene la tagline raster "DIGITAL PATHWAYS TO ITALY" e l'icona di una porta con chiave fra due ante tricolori. Entrambi gli elementi rientrano nell'elenco di rimozione della Fase 3 §3.1 (testo) e nella nota "sans la remplacer par des images stéréotypées : … portes". Poiché un logo non può essere ridisegnato dal team tecnico senza mandato, il nuovo sito userà un **wordmark tipografico "Italy Legal Entry™"** come identità di default e prevedrà nel CMS un campo `logo` caricabile: stato **LOGO_PENDING_CLIENT_CONFIRMATION**, da sciogliere con l'Avv. Badrane.

---

## 19. Elenco evidenze

Vedi `docs/audit/current-site/README.md`.
