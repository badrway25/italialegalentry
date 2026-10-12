# ASSET REGISTRY — ogni file servito, la sua provenienza e la sua licenza

Versione 1.0 · 21 settembre 2026

Regola generale: **niente hotlink**. Ogni carattere, immagine, icona e foglio di stile è scaricato,
ottimizzato e servito dal dominio del progetto. La CSP è `self` per gli script e `'self' data:` per
le immagini; `images.unsplash.com` e `fonts.googleapis.com` figurano nel registro delle stringhe
vietate, e un test fallisce se ricompaiono in un template.

Motivo, oltre alla privacy: un pubblico che accede in prevalenza da telefono, spesso su rete mobile,
paga ogni richiesta verso un terzo in latenza — e paga un carattere che non arriva con un salto di
disposizione.

---

## 1. Caratteri — 26 file, tutti OFL, tutti self-hosted

| Famiglia | Ruolo | Licenza | File |
|---|---|---|---|
| **Newsreader** (variabile, `opsz` 6–72) | Carattere di lettura latino: `plate`, `title`, `entry`, `prose` | SIL OFL 1.1 | 4 |
| **IBM Plex Sans** (400, 400 italic, 500, 600) | Carattere d'interfaccia latino da V4: `ui`, `gloss`, `caption`, la console | SIL OFL 1.1 | 8 |
| **IBM Plex Mono** (400) | Riferimenti e numerali tabulari: `numeral`, `t-ref`, `folio` | SIL OFL 1.1 | 2 |
| **Noto Naskh Arabic** | Carattere di lettura arabo | SIL OFL 1.1 | 3 |
| **IBM Plex Sans Arabic** (400, 500, 600) | Carattere d'interfaccia arabo | SIL OFL 1.1 | 9 |

**Sottoinsiemi.** `latin`, `latin-ext` e `arabic` sono file separati, dichiarati con `unicode-range`,
così una pagina francese non scarica l'arabo e viceversa.

**Precaricamento per scrittura.** `base.html` precarica soltanto i file della scrittura corrente:
precaricare tutti e ventisei sprecherebbe la banda che il sottoinsieme ha appena risparmiato.

**Pipeline:** `scripts/fetch_fonts.py`. Un carattere variabile dichiara un *intervallo* di peso
(`200 800`), non un numero: il costruttore dei nomi di file e l'ordinamento lo tengono in conto — un
`int("200 800")` è il difetto che questa pipeline ha già incontrato una volta.

---

## 2. Fotografie — 15 soggetti, derivati multipli

Registro completo, con autore, licenza, URL di origine e data di verifica:
**`docs/IMAGE_LICENSES.md`**. Ogni file sotto `static/img/photos/` deve avervi una riga, e
`apps/cms/tests/test_media_assets.py` lo verifica.

| Aspetto | Regola |
|---|---|
| Licenze ammesse | Unsplash License, Pexels License, CC0, CC BY 4.0 (con attribuzione), materiale del committente con autorizzazione scritta |
| Formati | WebP a 480/960/1440/1920 px + un JPEG di ripiego a 1440 |
| Metadati | rimossi (EXIF, GPS, nomi di file d'origine) |
| Manifest | `static/img/photos/manifest.json`, fonte di verità per `cms.MediaAsset` |
| Apparato | **ogni** figura porta luogo, data, didascalia e credito — `tests/compliance/test_figure_caption.py` |

**Soggetti vietati**, e non è una preferenza estetica: frontiere, valigie, file e code, passaporti,
aeroporti, porte e soglie, griglie e cancelli, iconografia stereotipata della migrazione, cliché
turistici (Colosseo, Ponte Vecchio, gondole). Il progetto parla di percorsi regolari e di
cooperazione; l'iconografia della frontiera dice il contrario di ciò che il testo afferma.

**Una fotografia non pubblicabile non viene resa.** `cms.MediaAsset.is_publishable` è falso finché
l'apparato è incompleto, e `pages.services.photo_from_asset` restituisce `None` invece di mostrarla
senza didascalia.

---

## 3. Illustrazioni — 6 file SVG originali

| File | Uso |
|---|---|
| `entrance-person.svg`, `entrance-company.svg`, `entrance-institution.svg`, `entrance-university.svg` | i quattro ingressi |
| `orientation.svg` | pagina di orientamento |
| `pilot-flow.svg` | diagramma del progetto pilota |

Originali del team, nessuna licenza di terzi. Costruite con i cinque colori dichiarati, senza
gradiente e senza ombra, per restare leggibili in `forced-colors`.

---

## 4. Icone — un solo sprite

`static/img/icons.svg`, uno sprite SVG referenziato con `<use>`. Nessuna libreria di icone, nessun
carattere di icone: un carattere di icone rende il testo dipendente da un download e si degrada in
quadratini quando non arriva.

Un'icona non sostituisce mai una parola. Accompagna una parola o è `aria-hidden`.

---

## 5. Fogli di stile — 5903 righe nel nucleo, 3545 per modulo

| File | Righe | Ruolo |
|---|---|---|
| `tokens.css` | 308 | I cinque mestieri del colore, i dieci ruoli tipografici, la spaziatura, i ranghi |
| `_legacy-tokens.css` | 338 | **Impalcatura di demolizione dichiarata.** Solo si riduce |
| `base.css` | 597 | Elementi, i dieci ruoli applicati, il carattere d'interfaccia sui controlli |
| `layout.css` | 392 | Contenitori, zone, ranghi di sezione |
| `register.css` | 944 | Il linguaggio grafico proprietario: folio, registro, sequenza, stato, esito, fonti |
| `components.css` | 3045 | Eredità del sito pubblico |
| `fonts.css` | 265 | `@font-face`, sottoinsiemi, `unicode-range` |
| `main.css` | 14 | Ordine di importazione |

Per modulo: `pages.css` 804, `portal.css` 703, `selection.css` 342, `documents.css`,
`helpdesk.css` 229, `academy.css`, `companies.css`, `forum.css`, `wizard.css` 107.

**`_legacy-tokens.css` è un'impalcatura, non un file.** La sua intestazione dice «QUESTO FILE SOLO SI
RIDUCE» e `tests/frontend/test_legacy_token_shim.py` ne fissa i tetti: 153 token, 14 classi, 1636
riferimenti. Un tetto che sale è un fallimento del test, non un aggiornamento.

**Classi senza regola: 382.** `scripts/css_class_audit.py` le elenca e ne fissa il tetto. Non sono
tutte difetti — un aggancio letto da JavaScript o da un test è legittimo — ma due lo erano, e nessuna
delle due era visibile come pagina rotta: `.gloss` (usata su quattordici pagine, nessuna regola, ogni
inciso reso a dimensione di prosa corrente) e `.faq-item__links` (nessuna regola, due link a 22 px di
distanza, sotto il minimo di WCAG 2.2 §2.5.8).

---

## 6. JavaScript — 567 righe in tutto

| File | Righe | Ruolo |
|---|---|---|
| `static/js/head.js` | — | Toglie `no-js`, prima della pittura |
| `static/js/main.js` | — | Navigazione, dialoghi, accordion |
| `apps/orientation/static/orientation/wizard.js` | — | Miglioramenti del questionario |
| `apps/pages/static/pages/js/home.js` | 41 | Homepage |

**Nessuna funzione dipende da JavaScript.** Ogni pagina ha un percorso senza script, e il progetto
non carica alcuna libreria di terzi: nessun framework, nessun analytics, nessun widget.

---

## 7. Ciò che il progetto non serve, deliberatamente

| Assente | Ragione |
|---|---|
| Analytics, tag manager, pixel | Nessun tracciamento. Registro delle stringhe vietate, con test |
| Caratteri da CDN | CSP e privacy; ogni carattere è locale |
| Immagini in hotlink | Idem; `images.unsplash.com` è una stringa vietata |
| Librerie JavaScript | 567 righe in tutto, nessuna dipendenza da terzi |
| Carattere di icone | Uno sprite SVG |
| Loghi di patrocinio | Gate G6: nessuno finché non sono forniti e autorizzati per iscritto |
| Nomi di persone istituzionali | Gate G5: nessuno prima del programma definitivo |

---

## 8. Verifiche

| Controllo | Dove |
|---|---|
| Ogni fotografia ha una riga nel registro delle licenze | `apps/cms/tests/test_media_assets.py` |
| Ogni figura ha luogo, data, didascalia, credito | `tests/compliance/test_figure_caption.py` |
| Nessun host esterno in un template | registro delle stringhe vietate |
| Il tetto dell'impalcatura legacy non sale | `tests/frontend/test_legacy_token_shim.py` |
| Il numero di classi senza regola non sale | `scripts/css_class_audit.py` |
| Nessuna richiesta esterna sulle pagine rese | `scripts/qa_browser_crawl.py` (richieste esterne registrate) |
