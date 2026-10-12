# ACCESSIBILITY — Italy Legal Entry™

Obiettivo, stato reale e procedura di verifica dell'accessibilità della piattaforma. Come
`docs/design/DESIGN_SYSTEM_2026.md`, questo documento descrive **ciò che è implementato e ciò che è stato misurato**,
non intenzioni: ogni riga della checklist rimanda a un file e a un selettore, ogni lacuna nota ha un
identificativo (**G-01 … G-27**), un'evidenza e un modo per verificarne la chiusura.

| Campo | Valore |
|---|---|
| Data di riferimento | 20 settembre 2026 |
| Revisione indipendente | 20 settembre 2026, sull'albero di lavoro dello Stage 2 (app `pages`, `ecosystem`, `portal` e cataloghi `locale/` presenti, non ancora committati): misure ripetute in Chromium, G-01, G-02, G-03 e G-05 confermati, G-08 ridimensionato, G-22 aggiunto |
| Seconda revisione indipendente | 20 settembre 2026, pomeriggio, mentre la QA in browser correggeva i file condivisi: G-01, G-02 e G-05 **chiusi** dagli owner e verificati in Chromium; breakpoint della navigazione passato da 64rem a **80rem** (il drawer vale ora anche per tablet e laptop fino a 1279 px); G-04 rimisurato e portato a gravità alta; G-23 aggiunto (overlay del drawer dipinto sopra l'header); bersagli a 390 px rimisurati (§9.1); catture e report rigenerati |
| Obiettivo | **WCAG 2.2, livello AA** (55 criteri A + AA), in italiano, francese, inglese e arabo (RTL) — requisito R-A11Y-001 |
| Riferimenti | EN 301 549 v3.2.1 cap. 9 (per allineamento), WAI-ARIA Authoring Practices (disclosure navigation, tabs, dialog), Designers Italia come benchmark di usabilità (R-A11Y-002) |
| Perimetro di questo documento | shell e design system: `templates/base.html`, `templates/partials/*`, `templates/components/*`, `templates/errors/*`, `templates/allauth/**`, `static/css/*`, `static/js/*`. Le pagine delle singole app ereditano questi contratti e vanno verificate nella fase QA |
| Come è stato verificato | lettura del codice; suite `tests/frontend` e `tests/compliance`; misure in Chromium via Playwright (ordine di tabulazione, anello di focus, dimensione dei bersagli, reduced motion, 320 px, JavaScript disattivato) su `http://127.0.0.1:8793`; screenshot in `docs/qa/design/` |
| Cosa **non** è ancora stato fatto | scansione axe-core (Stage 3 QA — G-18), test con screen reader reali (NVDA, VoiceOver, TalkBack), test con utenti |
| Test di veridicità | `tests/frontend/test_design_docs.py` (checklist completa dei 55 criteri, test citati esistenti, percorsi citati esistenti, lacune coerenti con il codice) |

> **Dichiarazione onesta dello stato.** Alla data di riferimento la piattaforma **non può ancora dichiararsi
> conforme**. I due difetti bloccanti della prima stesura (G-01 icone non disegnate, G-02 drawer
> schiacciato) e G-05 (riepilogo errori senza focus) sono stati chiusi dagli owner il 20/09/2026 e la
> chiusura è stata verificata in Chromium;
> restano aperte lacune di gravità alta (G-03, G-04, G-06) — G-04 rende illeggibili le pagine senza
> JavaScript sotto 80rem — e la scansione automatica completa non è ancora stata eseguita. L'impianto
> (semantica, focus, contrasto, tastiera, reduced motion, reflow) è solido e coperto da test.

---

## 1. Principi di lavoro

1. **HTML nativo prima di ARIA**: `<details>`, `<dialog>`, `<progress>`, `<nav>`, `<ol>`, `<dl>`, `<time>`,
   `<button>`; ARIA solo per stato (`aria-expanded`, `aria-current`, `aria-selected`) e nomi
   (`aria-label`, `aria-labelledby`).
2. **Funziona senza JavaScript** (ADR-009): nessun contenuto e nessuna funzione essenziale dipendono da
   `main.js`.
3. **Un solo `<h1>` per pagina**, landmark completi, ordine del DOM = ordine visivo = ordine di lettura.
4. **Nessuna informazione affidata al solo colore, al solo movimento o alla sola posizione.**
5. **Unità relative** (`rem`, `ch`, `clamp()`), nessuna altezza fissa sui contenitori di testo: zoom e
   spaziatura del testo non tagliano contenuti.
6. **Quattro lingue, una RTL**: `lang` e `dir` corretti a ogni livello, compresi i testi prescritti che
   restano in francese.

---

## 2. Checklist WCAG 2.2 — livelli A e AA

Stati: **Conforme** = implementato e verificato da test o misura; **Da confermare in QA** = implementato nel
design system, manca la verifica strumentale o sulle pagine delle app; **Parziale** = lacuna nota (§13);
**Non applicabile** = il tipo di contenuto non esiste nella piattaforma.

<!-- wcag-checklist:start -->
| SC | Criterio | Liv. | Stato | Implementazione (file → selettore / meccanismo) |
|---|---|---|---|---|
| 1.1.1 | Non-text Content | A | Da confermare in QA | `apps/core/templatetags/ile_core.py` → `svg_icon`: `aria-hidden="true" focusable="false"` per default, `role="img"` + `aria-label` se si passa un'etichetta; illustrazioni decorative `alt=""` (`templates/components/entrances.html`, `templates/components/hero.html`); fotografie con `cms.MediaAsset.alt(lang)`; controlli con sola icona nominati (`.main-nav__toggle` con testo `.visually-hidden`, `.dialog__close` con `aria-label`). Da verificare pagina per pagina gli alt delle foto |
| 1.2.1 | Audio-only and Video-only (Prerecorded) | A | Non applicabile | nessun audio o video nel design system; da riesaminare quando `forum` pubblicherà media |
| 1.2.2 | Captions (Prerecorded) | A | Non applicabile | nessun contenuto audio o video preregistrato nel design system (come 1.2.1) |
| 1.2.3 | Audio Description or Media Alternative (Prerecorded) | A | Non applicabile | nessun contenuto audio o video preregistrato nel design system (come 1.2.1) |
| 1.2.4 | Captions (Live) | AA | Non applicabile | nessuna trasmissione in diretta sulla piattaforma |
| 1.2.5 | Audio Description (Prerecorded) | AA | Non applicabile | nessun contenuto audio o video preregistrato nel design system (come 1.2.1) |
| 1.3.1 | Info and Relationships | A | Parziale (G-06) | landmark in `templates/base.html` (`header`, `nav`, `main`, `footer`, `role="region"` sulla barra istituzionale); liste ordinate per sequenze (`.entrances`, `.timeline`, `.stepper`, `.pathway-list`, `.breadcrumbs__list`); `<dl>` in `.meta-row`; `<label for>` in `templates/components/form_field.html`; `.form__fieldset` + `.form__legend`; tabelle `.prose th`. Lacuna: `aria-describedby` orfano nel form del Forum |
| 1.3.2 | Meaningful Sequence | A | Conforme | nessun `order`, nessun posizionamento che inverta la lettura; RTL ottenuto con `dir`, non con trucchi CSS; ordine di tabulazione misurato (§4.4) |
| 1.3.3 | Sensory Characteristics | A | Conforme | nessuna istruzione basata su forma, colore o posizione; obbligatorietà indicata da asterisco **e** attributo `required` **e** nota `.form__required-note` |
| 1.3.4 | Orientation | AA | Conforme | nessun blocco di orientamento; layout fluido 320 → 1920 px |
| 1.3.5 | Identify Input Purpose | AA | Da confermare in QA | django-allauth imposta `autocomplete` su login e password; `templates/allauth/elements/field.html` lo propaga; ogni form delle app deve dichiararlo sui campi personali (nome, e-mail, telefono, paese) |
| 1.4.1 | Use of Color | A | Conforme | link sottolineati (`static/css/base.css` → `a`); errori = icona + testo + filetto laterale; voce corrente = `aria-current` + barra/grassetto; lingua attiva = grassetto + punto; passo completato = segno di spunta (mai un colore: nessun colore di questo sistema significa «approvato»); tipo di notice = icona + titolo |
| 1.4.2 | Audio Control | A | Non applicabile | nessun contenuto audio, nessuna riproduzione automatica |
| 1.4.3 | Contrast (Minimum) | AA | Parziale (G-23) | 29 coppie bloccate da `tests/frontend/test_static_assets.py::test_wcag_contrast`; tabella misurata in `docs/design/DESIGN_SYSTEM_2026.md` §5 (minimo per testo: 5.91:1, marginalia sul fondo di processo). G-09 è chiusa: le numerazioni non sono più in bronzo a 3.83:1 ma in rubrica a 6.92:1, quindi nessuna esenzione serve più. Lacuna: a drawer aperto e pagina non scrollata l'overlay vela il bottone «Menu», la cui etichetta scende a 3.92:1 |
| 1.4.4 | Resize Text | AA | Conforme | scala in `rem`; verificato a 200 % (`docs/qa/design/a11y-zoom200-fr-640.png`): nessuna perdita di contenuto o funzione |
| 1.4.5 | Images of Text | AA | Conforme | il wordmark è testo vivo (`{% brand %}`); nessuna immagine di testo nei componenti; `og-default.png` non è mostrata in pagina |
| 1.4.10 | Reflow | AA | Conforme | nessuno scorrimento orizzontale a 320 px CSS (`docs/qa/design/a11y-zoom400-fr-320.png`, `docs/qa/design/a11y-zoom400-ar-320.png`; report `docs/qa/design/capture-report.json`) e a 360 px (`tests/frontend/test_browser.py::test_no_horizontal_overflow_and_screenshots`); contenuti larghi in `.scroll-x` |
| 1.4.11 | Non-text Contrast | AA | Parziale (G-22) | perimetro dei campi 3.50:1 sulla carta e 3.74:1 dentro il campo (`--rule-ink`), anello di focus 13.62:1 su fondo chiaro e 13.62:1 su navy, bordi di stato ≥ 3.16:1, filetto d'ordine 6.92:1. Le icone sono disegnate (G-01 chiusa: 0 icone vuote nel report delle catture), quindi i controlli con sola icona (`.main-nav__toggle`, `.dialog__close` e, sotto 48rem, il link «Espace réservé» `.utility-bar__link`, la cui etichetta è solo per screen reader) sono visibili. Lacuna: le pagine del Forum e del wizard usano un anello di focus proprio, al limite della soglia di 3:1 |
| 1.4.12 | Text Spacing | AA | Da confermare in QA | nessuna `height` fissa su contenitori di testo (solo `min-block-size`; dimensioni fisse soltanto per icone, filetti e marcatori circolari numerati); da provare con il bookmarklet di text spacing (§12.3) |
| 1.4.13 | Content on Hover or Focus | AA | Parziale (G-12) | con JS nessun contenuto appare al solo hover: il mega-menu si apre con click o tastiera e si chiude con Esc. Senza JS i pannelli appaiono su `:hover` / `:focus-within` e non sono chiudibili con Esc |
| 2.1.1 | Keyboard | A | Conforme | ogni controllo è un `a`, `button`, `summary` o campo nativo; modello in §3; `tests/frontend/test_browser.py::test_mega_menu_is_keyboard_operable` |
| 2.1.2 | No Keyboard Trap | A | Conforme | drawer: Esc chiude, il ciclo di Tab passa dal bottone «Menu»; dialog: focus trap nativo con Esc; dropdown: Esc |
| 2.1.4 | Character Key Shortcuts | A | Conforme | nessuna scorciatoia a carattere singolo in `static/js/main.js` |
| 2.2.1 | Timing Adjustable | A | Parziale (G-17) | nessun limite di tempo nell'interfaccia; l'anti-spam (`apps/core/forms.py` → `MAX_FILL_SECONDS`, 6 ore) scarta in silenzio un form compilato più lentamente: da valutare |
| 2.2.2 | Pause, Stop, Hide | A | Conforme | nessun contenuto in movimento automatico oltre 5 s: reveal 600 ms e contatori 900 ms, una sola volta; nessun carousel, nessun autoplay |
| 2.3.1 | Three Flashes or Below Threshold | A | Conforme | nessun lampeggio |
| 2.4.1 | Bypass Blocks | A | Conforme | `templates/base.html` → `a.skip-link[href="#main-content"]` + `main#main-content[tabindex="-1"]`; misurato: Tab → Invio porta il focus su `main-content`; `tests/frontend/test_layout.py::test_shell_landmarks_skip_link_and_single_h1` |
| 2.4.2 | Page Titled | A | Conforme | `templates/base.html` → `<title>{% block page_title %} · Italy Legal Entry™`; le pagine d'errore e account lo valorizzano |
| 2.4.3 | Focus Order | A | Parziale (G-11) | ordine del DOM; l'apertura di mega-menu, drawer e dialog sposta il focus nel pannello e lo restituisce alla chiusura (G-02 chiusa: il drawer è visibile per intero, il focus non finisce più su voci nascoste). Lacuna: a drawer aperto il resto della pagina non è inerte e il cursore virtuale di uno screen reader può uscirne |
| 2.4.4 | Link Purpose (In Context) | A | Conforme | testi dei link descrittivi; «Voir l’espace» è nel pannello che porta il nome della sezione; stretched link con il titolo come nome accessibile |
| 2.4.5 | Multiple Ways | AA | Da confermare in QA | menu principale + navigazione del footer + breadcrumb + ricerca interna di FAQ e glossario + `sitemap.xml`; manca una mappa del sito in HTML o una ricerca globale: da decidere in QA |
| 2.4.6 | Headings and Labels | AA | Conforme | un `h1` per pagina (test), `h2` di sezione (`templates/components/section_header.html`), `h3` negli elenchi; etichette dei campi sempre visibili |
| 2.4.7 | Focus Visible | AA | Conforme | `static/css/base.css` → `:focus-visible` (outline 2 px + alone 2 px); variante `.on-inverse`; misurato su 16 tappe (§4.4) |
| 2.4.11 | Focus Not Obscured (Minimum) | AA | Parziale (G-04) | `html { scroll-padding-block-start: calc(var(--header-height) + var(--space-4)) }` tiene il focus sotto l'header sticky; `.section-nav` sticky sotto l'header. Lacuna: senza JS, sotto 80rem, l'header sticky contiene l'intero menu, è alto 781 px e copre il contenuto (a 1024 × 768 per intero) |
| 2.5.1 | Pointer Gestures | A | Conforme | nessun gesto multipunto o a percorso |
| 2.5.2 | Pointer Cancellation | A | Conforme | solo eventi `click` (attivazione al rilascio) |
| 2.5.3 | Label in Name | A | Conforme | il nome accessibile contiene il testo visibile: il wordmark ha `aria-label="Italy Legal Entry™ — accueil"`, il bottone «Menu» ha il testo visibile |
| 2.5.4 | Motion Actuation | A | Conforme | nessuna funzione attivata dal movimento del dispositivo |
| 2.5.7 | Dragging Movements | AA | Conforme | nessun trascinamento |
| 2.5.8 | Target Size (Minimum) | AA | Da confermare in QA | `--control-height` (44 px) su bottoni, campi, voci di menu, tab, paginazione; misure e eccezioni in §9; un caso da verificare (G-10) |
| 3.1.1 | Language of Page | A | Conforme | `<html lang="{{ site.lang }}" dir="{{ site.dir }}">`; `tests/frontend/test_layout.py::test_html_lang_and_dir_attributes` |
| 3.1.2 | Language of Parts | AA | Parziale (G-08) | `{% locked %}` aggiunge `lang="fr"` quando il testo prescritto non ha versione nella lingua della pagina; i componenti accettano `lang`; i link del selettore lingua hanno `lang` e `hreflang`; le stringhe UI sono tradotte dai cataloghi `locale/` (Stage 2). Lacuna residua: i due titoli inglesi del footer senza `lang="en"`; le traduzioni vanno rilette da madrelingua |
| 3.2.1 | On Focus | A | Conforme | nessun cambio di contesto al focus |
| 3.2.2 | On Input | A | Conforme | il cambio lingua è una lista di link, non un `<select>` con invio automatico |
| 3.2.3 | Consistent Navigation | AA | Conforme | stessi partial su ogni pagina (`templates/partials/header.html`, `templates/partials/footer.html`, `templates/partials/utility_bar.html`) |
| 3.2.4 | Consistent Identification | AA | Conforme | un solo set di icone, un solo componente per funzione (catalogo in `docs/design/DESIGN_SYSTEM_2026.md` §10) |
| 3.2.6 | Consistent Help | A | Conforme | l'indirizzo di contatto è nella stessa posizione del footer in ogni pagina; le pagine account aggiungono «Besoin d’aide ?» sotto il form; `templates/components/form_unavailable.html` offre sempre l'e-mail |
| 3.3.1 | Error Identification | A | Parziale (G-06) | riepilogo `templates/components/form_errors.html` (`role="alert"`, link ai campi) che riceve il focus al caricamento (`static/js/main.js` → `initFormErrorFocus`; G-05 chiusa) + errori di campo con testo, `aria-invalid`, `aria-describedby`. Lacuna: nel form del Forum `aria-describedby` punta a un id inesistente |
| 3.3.2 | Labels or Instructions | A | Conforme | etichetta visibile per ogni campo, aiuto collegato, nota sui campi obbligatori; placeholder mai al posto dell'etichetta |
| 3.3.3 | Error Suggestion | AA | Da confermare in QA | i messaggi di validazione di Django indicano il formato atteso; da rivedere i messaggi personalizzati di ogni form |
| 3.3.4 | Error Prevention (Legal, Financial, Data) | AA | Da confermare in QA | invii verificati lato server e ripresentati con i dati inseriti; consenso esplicito mai pre-spuntato; la cancellazione dell'account ha una pagina di conferma (`templates/accounts/delete_request.html`) |
| 3.3.7 | Redundant Entry | A | Da confermare in QA | i form ripresentati conservano i valori; il wizard di orientamento conserva le risposte in sessione |
| 3.3.8 | Accessible Authentication (Minimum) | AA | Da confermare in QA | login con e-mail e password: incolla e gestori di password non ostacolati, nessun CAPTCHA (anti-spam con honeypot invisibile); il codice TOTP della MFA va verificato (incolla, `autocomplete="one-time-code"`) |
| 4.1.2 | Name, Role, Value | A | Parziale (G-06) | elementi nativi; stati ARIA sincronizzati da `static/js/main.js` (`aria-expanded`, `aria-selected`, `aria-current`); `dialog[aria-labelledby]`. Lacuna: riferimento `aria-describedby` orfano nel form del Forum |
| 4.1.3 | Status Messages | AA | Da confermare in QA (G-07) | `templates/base.html` → `.messages[role="status"][aria-live="polite"]`, `role="alert"` per gli errori; `templates/components/notice.html`, `templates/components/empty_state.html`, `templates/components/form_unavailable.html` con `role="status"`. Le regioni sono già popolate al caricamento: annuncio da verificare con screen reader |
<!-- wcag-checklist:end -->

Riepilogo: 55 criteri — 29 conformi, 10 parziali, 10 da confermare in QA, 6 non applicabili.

---

## 3. Modello tastiera dei componenti interattivi

Regola generale: **Tab / Shift+Tab** seguono l'ordine del DOM; **Invio** attiva link e bottoni; **Spazio**
attiva bottoni, `summary` e checkbox; **Esc** chiude ciò che si è aperto e restituisce il focus a chi lo ha
aperto. Le frecce orizzontali si invertono in arabo.

| Componente | Tasti | Focus e stato | Senza JS |
|---|---|---|---|
| Skip link (`templates/base.html`) | primo Tab della pagina; Invio | appare in alto a `inline-start`; porta il focus su `main#main-content` (`tabindex="-1"`) | identico |
| Selettore lingua, menu account (`details[data-dropdown]`) | Invio/Spazio sul `summary` apre e chiude; Tab entra nella lista; Esc chiude | `aria-expanded` sul `summary`; Esc riporta il focus al `summary`; si chiude alla perdita di focus e al click esterno; uno aperto per volta | `<details>` nativo: apre e chiude; resta aperto finché non lo si richiude |
| Mega-menu (≥ 80rem) | Tab tra link e bottoni; Invio/Spazio sul bottone apre; ↓ apre ed entra; ←/→ tra le voci con pannello (circolare); Esc chiude | focus sul primo elemento del pannello all'apertura; Esc → focus al bottone; `aria-expanded`, `aria-controls`; chiusura su `focusout` | pannelli su `:hover` / `:focus-within`: raggiungibili con Tab, non chiudibili con Esc (G-12) |
| Drawer (< 80rem: telefono, tablet, laptop fino a 1279 px) | Invio/Spazio su «Menu»; Tab dentro il drawer; Esc chiude | focus al primo elemento del drawer; Tab dall'ultimo e Shift+Tab dal primo → bottone «Menu»; `aria-expanded`; scroll della pagina bloccato | menu in flusso, tutto visibile, bottone nascosto |
| Breadcrumb, navigazione locale, sommario di pagina, footer | Tab, Invio | voce corrente `aria-current` (non linkata nel breadcrumb) | identico (il sommario non evidenzia la sezione in vista) |
| Tab (`templates/components/tabs.html`) | ←/→ scheda precedente/successiva con attivazione immediata; Home / Fine; Tab entra nel pannello | roving `tabindex`; `aria-selected`; pannello `tabindex="0"` | niente tablist: pannelli impilati con titolo `h3` |
| Accordion (`templates/components/accordion.html`) | Invio/Spazio sul `summary` | stato espanso annunciato dal browser; con `single` si chiudono gli altri | identico (senza esclusività nei browser privi di `<details name>`) |
| Stepper lato client (`[data-stepper]`) | Invio/Spazio su «successivo» / «precedente» | il focus va sul titolo del passo (`tabindex="-1"`); `aria-current="step"` | tutti i passi visibili |
| Dialog (`templates/components/dialog.html`) | Invio/Spazio sull'apertura; Tab ciclico dentro il dialog; Esc chiude | `showModal()`: sfondo inerte; focus su `[data-dialog-focus]` o sul primo focusabile; alla chiusura torna all'elemento che ha aperto; backdrop cliccabile solo con `light` | il link `#id` mostra il pannello via `:target`; si esce con «indietro» |
| Card, entrance, pathway item (stretched link) | Tab, Invio | **un solo** tab stop per elemento (il link del titolo o la CTA) | identico |
| Paginazione | Tab, Invio | «Page n sur N» con `aria-current="page"` | identico |
| Form (`templates/components/form_field.html`) | Tab tra i campi; Spazio sulle checkbox; Invio invia | dopo un invio non valido il focus è sul riepilogo degli errori (`#form-errors`); link del riepilogo → campo; `data-single-submit` disabilita il bottone dopo l'invio | invio normale; nessun focus automatico sul riepilogo; nessun blocco del doppio invio |
| Logout (`templates/components/account_menu.html`) | Invio/Spazio | `<button type="submit">` in un form POST con CSRF | identico |
| Pagine d'errore (`templates/errors/base_error.html`) | Tab, Invio | «Page précédente» usa `history.back()` | il bottone «Page précédente» è nascosto (`.js-only`) |

---

## 4. Gestione del focus

### 4.1 Anello di focus

`static/css/base.css`: `:focus { outline: none }` + `:focus-visible { outline: var(--focus-ring-width) solid
var(--focus-ring-color); outline-offset: var(--focus-ring-offset); box-shadow: 0 0 0 var(--focus-ring-offset)
var(--focus-ring-offset-color) }` — anello **a due toni**: 2 px navy `#0e2a47` (13.62:1 sul fondo) staccato
di 2 px, con alone del colore del fondo che lo separa da qualunque superficie. Dentro `.on-inverse` /
`.surface-inverse` (barra istituzionale, footer, fasce verso) l'anello diventa `--focus-ring-inverse`
`#faf7f0` (13.62:1 sul navy). I campi aggiungono bordo e alone blu (`.form-field …:focus-visible`). Gli
elementi con stretched link allargano l'offset (`.entrance__cta:focus-visible`, 4 px).

Misurato in Chromium: tutte le 16 prime tappe di `/fr/` mostrano `outline: solid 2px`, con colore
`rgb(250, 247, 240)` nella barra e nel footer e `rgb(14, 42, 71)` nell'header (misura ripetuta dopo la
redirezione: i due toni sono cambiati, il meccanismo no). Screenshot:
`docs/qa/design/state-skiplink-fr-390.png`, `docs/qa/design/state-focus-field-fr-1440.png`,
`docs/qa/design/state-megamenu-open-fr-1440.png`.

### 4.2 Skip link

Primo elemento del `<body>`; nascosto con `transform: translateY(-200%)` (non con `display: none`), compare
al focus; `z-index: var(--z-skiplink)`, un nome che oggi non è dichiarato da nessun foglio (G-25): lo skip link
si appoggia all'ordine del documento finché la riga mancante non viene aggiunta allo shim. Destinazione `main#main-content` con `tabindex="-1"`, così il
focus si sposta davvero (misurato: `document.activeElement.id === "main-content"`).

### 4.3 Modale e drawer

- **Dialog**: `<dialog>` nativo con `showModal()` → focus trap, Esc e sfondo inerte gestiti dal browser;
  `main.js` sceglie il focus iniziale e lo **restituisce all'elemento di apertura** all'evento `close`.
- **Drawer**: non è un modale ARIA. Focus iniziale sul primo elemento, ciclo Tab che passa dal bottone
  «Menu», Esc, overlay cliccabile, `overflow: hidden` sul `body`. Il resto della pagina non è `inert`: uno
  screen reader può uscirne con il cursore virtuale (G-11). Il difetto G-02, che lo schiacciava a 65 px, è
  chiuso: il pannello occupa tutto lo spazio sotto l'header. Resta G-23: a pagina non scrollata l'overlay
  vela la fascia bassa dell'header, bottone «Menu» compreso.
- **Mega-menu e dropdown**: si chiudono alla perdita di focus; Esc restituisce il focus al controllo.
- **Riepilogo degli errori**: la validazione è lato server, quindi dopo un invio non valido la pagina si
  ricarica dall'inizio; `initFormErrorFocus` porta il focus su `#form-errors` (`tabindex="-1"`,
  `role="alert"`) e lo scorre al centro del viewport (misurato: `document.activeElement.id ===
  "form-errors"`; G-05 chiusa).

### 4.4 Ordine di tabulazione misurato (`/fr/`, 1440 px)

Misura ripetuta alla revisione sulla home dell'app `pages` (Stage 2, menu popolato da `seed_all`):

1 skip link → 2 «Espace réservé» → 3 selettore lingua → 4 wordmark → 5 «Personnes» → 6 bottone del
sottomenu «Personnes» → 7 «Entreprises» → 8 bottone del sottomenu «Entreprises» → 9 «Forum
Vénétie–Maroc» → 10 «Projet» → 11 bottone del sottomenu «Projet» → contenuto (12–13 i due bottoni
dell'hero, 14 bottone del banner del Forum, 15 «Masquer cette annonce», 16 primo accesso…) → e-mail del
footer → cinque link legali → navigazione del footer. L'ordine coincide con l'ordine visivo in LTR e,
specchiato, in RTL.

### 4.5 Focus non coperto

`scroll-padding-block-start` = altezza dell'header + 16 px; gli elementi sticky (`.site-header`,
`.section-nav`, `.layout-sidebar__aside`) non si sovrappongono tra loro perché usano `--header-height` come
origine. Eccezione grave: G-04 — senza JS, sotto 80rem, l'header sticky contiene l'intero menu ed è più alto
di molti viewport, quindi copre anche l'elemento che ha il focus.

---

## 5. Semantica per screen reader

- **Landmark** (`templates/base.html`): barra istituzionale `role="region"` con `aria-label="Barre
  institutionnelle"`; `header`; `nav` «Navigation principale»; `main`; `footer` con due `nav` etichettate
  («Informations légales», «Navigation du site»); `nav` «Fil d’Ariane»; nelle pagine d'errore `nav`
  «Navigation de secours»; nelle pagine account `nav` «Gestion du compte». Ogni `nav` ha un nome distinto.
- **Titoli**: un solo `h1` (in `page_header.html`, `hero.html`, `base_error.html`, elemento `h1` di
  allauth); `h2` per le sezioni; `h3` per card, pathway, pannelli delle tab. Banner, stato vuoto e titoli di
  notice sono `<p>` per non inquinare la gerarchia.
- **Nomi**: controlli con sola icona sempre nominati; icone accanto a testo `aria-hidden`; numerazioni CSS
  e marcatori `aria-hidden` (l'ordine è dato da `<ol>`).
- **Stati**: `aria-expanded` (menu, drawer, dropdown), `aria-current` (`page`, `step`, `true`),
  `aria-selected` (tab), `aria-invalid` (campi), `[open]` (accordion, dropdown).
- **Regioni live**: messaggi Django in `.messages[role="status"][aria-live="polite"]`, con `role="alert"` sul
  singolo messaggio d'errore; `notice.html` → `role="alert"` solo per `error`, altrimenti `role="status"`;
  `empty_state.html` e `form_unavailable.html` → `role="status"`; riepilogo errori e liste di errori di
  campo → `role="alert"`. Limite noto: sono popolate già al caricamento (G-07).
- **Testo solo per screen reader**: `.visually-hidden` / `.sr-only` (clip, non `display: none`). L'honeypot
  è l'opposto: `.hp-wrap` fuori schermo **con** `aria-hidden="true"` e `tabindex="-1"`, invisibile anche
  alle tecnologie assistive.
- **Marchio**: `<span translate="no">` sul wordmark, così i traduttori automatici del browser non lo
  alterano.

---

## 6. Contratto di accessibilità dei form (`templates/components/form_field.html`)

Ogni campo pubblico passa da questo componente (allauth compreso, tramite
`templates/allauth/elements/fields.html`). Output verificato rendendo il componente con un form non valido:

```html
<div class="form-field form-field--error form-field--required" id="wrap_id_email">
  <label class="form-field__label" for="id_email">Adresse e-mail <span class="form-field__required" aria-hidden="true">*</span></label>
  <input type="email" name="email" required aria-invalid="true" aria-describedby="id_email_helptext id_email_error" id="id_email">
  <p class="form-field__help" id="id_email_helptext">…</p>
  <ul class="form-field__errors" id="id_email_error" role="alert"><li>…</li></ul>
</div>
```

| Garanzia | Meccanismo |
|---|---|
| Etichetta sempre visibile e associata | `<label for="{{ field.id_for_label }}">`; per le checkbox l'etichetta è a fianco ed è cliccabile; il placeholder non sostituisce mai l'etichetta |
| Obbligatorietà | asterisco `aria-hidden` + attributo `required` sul controllo + nota «Champs obligatoires» (`.form__required-note`) |
| Aiuto collegato | `<p id="<auto_id>_helptext">`; Django 5.2 aggiunge `aria-describedby` con lo stesso id |
| Errore collegato | `<ul id="<auto_id>_error" role="alert">`; Django 5.2 aggiunge `aria-invalid="true"` e l'id dell'errore in `aria-describedby`. **Non impostare `aria-describedby` a mano sul widget**: sovrascrive quello di Django e rompe il collegamento (è ciò che accade in G-06) |
| Errore non affidato al colore | testo + pallino + filetto laterale da 3 px + bordo del campo + etichetta rossa (`--color-error-fg`, che risolve a `--state-error-fg`, 8.31:1 sulla carta) |
| Riepilogo in cima | `templates/components/form_errors.html`: `role="alert"`, `tabindex="-1"`, link `#id_campo` per ogni errore; al caricamento `main.js` vi porta il focus (G-05 chiusa) |
| Consenso | `core.forms.ConsentBooleanField`: obbligatorio, mai pre-spuntato, etichetta = testo prescritto dal registro; riquadro `.form-field--consent` |
| Anti-spam senza barriere | honeypot invisibile a tutti + tempo minimo; nessun CAPTCHA (SC 3.3.8) |
| Campi latini in arabo | `dir="ltr"` / isolamento bidi su `email`, `tel`, `url`, `number`, `password` |
| Dimensioni | controlli alti 44 px, testo 16 px (nessuno zoom automatico su iOS), `textarea` ridimensionabile in verticale |
| Doppio invio | `form[data-single-submit]`: dopo l'invio i bottoni ricevono `disabled` e `aria-disabled="true"` |
| Form chiuso dal gate G2 | `templates/components/form_unavailable.html` (`role="status"`) con alternativa e-mail: mai un form monco |
| Validazione | lato server; i form del design system usano `novalidate` per mostrare messaggi coerenti, tradotti e collegati invece dei fumetti del browser |

Screenshot: `docs/qa/design/state-form-errors-fr-390.png`, `docs/qa/design/state-form-errors-ar-390.png`.

---

## 7. Movimento ridotto

Tre livelli, tutti attivi con `prefers-reduced-motion: reduce`:

1. `static/css/tokens.css` azzera `--motion-fast`, `--motion-base` e `--motion-slow`, e lo shim li
   propaga ai nomi legacy `--duration-fast`, `--duration-base` e `--duration-slow`
   (`--duration-reveal` e `--reveal-distance` valgono già `0ms` e `0`);
2. `static/css/components.css` §29 forza `transition-duration` e `animation-duration` a `0.01ms`, una sola
   iterazione, `scroll-behavior: auto`, e disattiva i keyframe di mega-menu e dialog;
3. `static/js/main.js` legge la stessa media query: `.reveal` diventa visibile subito senza observer, i
   contatori scrivono il valore finale, e un cambio della preferenza a pagina aperta viene rispettato.

Misurato: con la preferenza attiva `--duration-base` = `0ms`, `transition-duration` effettiva `1e-05s`,
`scroll-behavior: auto`; senza, `200ms` / `0.12s` / `smooth`. Screenshot
`docs/qa/design/a11y-reduced-motion-fr-1440.png`. Inventario completo in `docs/design/DESIGN_SYSTEM_2026.md` §12. Non
esistono animazioni in loop, parallax o autoplay da mettere in pausa.

---

## 8. Zoom, reflow, spaziatura del testo

| Prova | Equivalente | Esito |
|---|---|---|
| Zoom 200 % | finestra 1280 px → 640 px CSS | contenuto e funzioni integri, navigazione in modalità drawer (il mega-menu vale solo da 80rem: a 1280 px qualunque zoom oltre il 100 % porta al drawer) — `docs/qa/design/a11y-zoom200-fr-640.png` |
| Zoom 400 % (SC 1.4.10) | 1280 px → 320 × 256 px CSS | nessuno scorrimento orizzontale in francese e in arabo — `docs/qa/design/a11y-zoom400-fr-320.png`, `docs/qa/design/a11y-zoom400-ar-320.png` |
| 360 / 768 / 1440 px, fr + ar, 4 pagine | — | `scrollWidth ≤ clientWidth` — `tests/frontend/test_browser.py::test_no_horizontal_overflow_and_screenshots` |
| 390 / 768 / 1440 px, fr + ar, 4 pagine + stati | — | 43 catture, 0 overflow — `docs/qa/design/capture-report.json` |

Perché regge: tipografia e spazi in `rem`; `clamp()` per titoli e margini; griglie `minmax(0, 1fr)` con
`min-inline-size: 0` sui figli; `overflow-wrap: break-word` sul `body`; `flex-wrap` su gruppi di bottoni e
metadati; tabelle e diagrammi dentro `.scroll-x` (l'unico scorrimento orizzontale ammesso, focusabile);
`min-block-size` invece di `height`. Limiti: a 320 px il nome del promotore nella barra istituzionale è
troncato con ellissi (in arabo dal lato sbagliato — G-03); con l'header sticky a 400 % resta poco spazio
verticale (256 px): da valutare in QA se rendere l'header non sticky sotto una certa altezza.

---

## 9. Dimensione dei bersagli e indipendenza dal colore

### 9.1 Bersagli (SC 2.5.8, minimo 24 × 24 px; obiettivo interno 44 px)

| Controllo | Dimensione |
|---|---|
| Bottoni, campi, `select`, voci del menu, tab, link di paginazione, chiusura del dialog, bottone «Menu» | ≥ 44 px (`--control-height`, dichiarato `44px`) |
| Voci e bottoni del menu nel drawer | 52 px; sottovoci ≥ 44 px |
| `summary` degli accordion | ≥ 56 px |
| Selettore lingua, menu account, link «Espace réservé» | 32 px (`--utility-height`, che risolve a `--chrome-utility`: la barra istituzionale si è abbassata da 40 a 32 px con la nuova cromatura) |
| Bottone del sottomenu su desktop | 32 × 44 px |
| Bottoni `--sm` | 36 px |
| Checkbox e radio | 24 × 24 px (`.form-field input[type="checkbox"]`, `1.5rem`; erano 20 × 20 alla prima stesura) **più** l'etichetta cliccabile a fianco |

Misura in Chromium a 390 px (`/fr/`, login, 404), ripetuta alla seconda revisione: gli unici bersagli sotto
24 px in una dimensione sono link di testo — link del footer (alti 19 px, passo verticale 27 px: i cerchi da
24 px non si intersecano → eccezione «spacing»), link in frase («enregistrer», e-mail di aiuto → eccezione
«inline»), link di recupero del 404 (alti 20 px) e le CTA dei quattro accessi (`.entrance__cta`: la riga di
testo è alta 22 px, ma il bersaglio reale è l'intera colonna, coperta dallo pseudo-elemento dello stretched
link). Il wordmark misura 186 × 44 px da quando `.brand` ha `min-block-size: var(--control-height)` (alla
prima stesura era 186 × 22); sotto 48rem «Espace réservé» è un bersaglio di 24 × 40 px con la sola icona.
Un caso da verificare: «Mot de passe oublié ?» (17 px) subito sotto il campo password (G-10).

### 9.2 Colore

Nessuno stato è comunicato dal solo colore: vedi riga 1.4.1 della checklist. In scala di grigi restano
distinguibili link (sottolineatura), voce corrente (barra / grassetto), errori (icona, pallino, filetto),
passi completati (spunta), tipo di notice (icona + titolo), lingua attiva (grassetto + punto). Il bronzo non esiste più: `--color-accent-600` risolve alla rubrica, il cui unico compito è marcare
l'ordine, e a 6.92:1 sulla carta è sicura anche come testo.

---

## 10. Lingua, RTL e bidi

### 10.1 Attributi di lingua

- `<html lang dir>` dal context processor `core.context_processors.site` (`fr`, `it`, `en` → `ltr`;
  `ar` → `rtl`), più `body.is-rtl`.
- **Testi prescritti non ancora tradotti**: i testi del registro `cms.locked_content` esistono in francese
  (ADR-004) e **non vengono mai tradotti automaticamente**. `{% locked "chiave" %}` confronta la lingua
  effettiva con quella della pagina e, se differiscono, emette `lang="fr"` sull'elemento
  (`{% locked "k" "h2" "classe" %}`) o su uno `<span lang="fr">`. Per passare il testo a un componente si
  usa `{% locked_lang "chiave" as l %}` e il parametro `lang=l`. Effetto: in una pagina italiana, inglese o
  araba lo screen reader legge quei passaggi con la voce francese invece di storpiarli; in arabo il
  frammento francese resta un'isola LTR corretta. Verifica:
  `tests/compliance/test_locked_content.py::test_fallback_to_french_for_other_languages`.
- Contenuti CMS con traduzione mancante: `cms.translation.resolve(obj, lang)` restituisce il francese
  marcato come fallback e i template mettono `lang` sul blocco (es. `templates/faq/_item.html`).
- Selettore lingua: ogni link ha `lang`, `hreflang`, `dir`
  (`tests/frontend/test_layout.py::test_language_switcher_lists_every_language_with_hreflang`); `<head>`:
  `hreflang` per le quattro lingue + `x-default`
  (`tests/compliance/test_public_pages.py::test_hreflang_alternates_present`).
- Stringhe UI: sorgente francese in `{% translate %}` / `gettext_lazy`, tradotte dai cataloghi
  `locale/<lingua>/LC_MESSAGES/django.po` (fr, it, en, ar — arrivati con lo Stage 2, non ancora committati
  alla revisione). I testi prescritti e le pagine legali **non** fanno parte dei cataloghi. Verificato alla
  revisione: su `/ar/`, `/it/` e `/en/` skip link, landmark, menu e footer sono nella lingua della pagina.
- Lacuna G-08 (residua): i due titoli inglesi del footer («Privacy Policy», «Cookie Policy») compaiono
  senza `lang="en"` nelle pagine `fr` / `it` / `ar`; ogni stringa aggiunta senza aggiornare i cataloghi
  ricade sul francese senza `lang`; le traduzioni vanno rilette da madrelingua prima della pubblicazione.

### 10.2 RTL e bidi

Regole di disegno in `docs/design/DESIGN_SYSTEM_2026.md` §15. Per l'accessibilità contano:

- l'ordine del DOM non cambia tra LTR e RTL: cambia solo `dir`, quindi ordine di lettura e di tabulazione
  restano coerenti con ciò che si vede;
- le frecce della tastiera seguono la direzione visiva (← e → invertite in `main.js` per mega-menu e tab);
- le icone direzionali sono specchiate (`.icon--flip-rtl`), quelle non direzionali no;
- dati latini (e-mail, telefono, URL, codici, date ISO, wordmark dell'header) sono isolati con
  `direction: ltr; unicode-bidi: isolate`; gli input corrispondenti allineano il testo a `end`;
- in arabo niente maiuscolo forzato e niente `letter-spacing`;
- difetto aperto G-03: wordmark del footer, nome del promotore e riga del © non sono isolati.

Verifica: `tests/compliance/test_public_pages.py::test_arabic_is_rtl_and_others_ltr`,
`tests/frontend/test_layout.py::test_login_page_in_arabic_is_rtl`,
`tests/frontend/test_browser.py::test_mobile_drawer_and_language_switcher`; screenshot
`docs/qa/design/home-ar-1440.png`, `docs/qa/design/login-ar-390.png`, `docs/qa/design/privacy-ar-768.png`,
`docs/qa/design/404-ar-1440.png`.

---

## 11. Controlli automatici esistenti

Nessuno di questi sostituisce axe-core o un test manuale: bloccano le regressioni dei contratti.

| Cosa protegge | Test |
|---|---|
| Landmark, skip link, `main` focusabile, un solo `h1` (5 pagine) | `tests/frontend/test_layout.py::test_shell_landmarks_skip_link_and_single_h1` |
| Nessuna risorsa esterna, nessuno stile o script inline | `tests/frontend/test_layout.py::test_no_external_resources_or_inline_styles`, `tests/compliance/test_public_pages.py::test_no_external_scripts_fonts_or_images` |
| `lang` / `dir` e preload dei font per direzione | `tests/frontend/test_layout.py::test_html_lang_and_dir_attributes` |
| Selettore lingua con `lang` / `hreflang` / `dir` | `tests/frontend/test_layout.py::test_language_switcher_lists_every_language_with_hreflang` |
| Cinque link legali distinti, identità, e-mail unica | `tests/frontend/test_layout.py::test_footer_has_five_distinct_legal_links_identity_and_version` |
| Pagine d'errore con shell, un `h1`, navigazione di recupero | `tests/frontend/test_layout.py::test_error_pages_render_with_shell`, `tests/frontend/test_layout.py::test_404_page_offers_recovery_navigation` |
| Login sul design system (campi, etichette, un `h1`), anche in arabo | `tests/frontend/test_layout.py::test_login_page_uses_design_system_form`, `tests/frontend/test_layout.py::test_login_page_in_arabic_is_rtl` |
| Regione live dei messaggi e blocchi di `base.html` | `tests/frontend/test_layout.py::test_messages_region_present` |
| Menu reso dal tag, voci gate-aware | `tests/frontend/test_cms_nav.py::test_main_menu_tag_renders_in_template` |
| Contrasto di 29 coppie di token | `tests/frontend/test_static_assets.py::test_wcag_contrast` |
| Token completi, nessun colore fuori dai token | `tests/frontend/test_static_assets.py::test_tokens_file_is_complete`, `tests/frontend/test_static_assets.py::test_no_hardcoded_colours_outside_tokens_and_fonts` |
| Ogni icona usata esiste nello sprite | `tests/frontend/test_static_assets.py::test_every_icon_used_in_templates_exists_in_sprite` |
| Nessuno stile inline né handler `on*` nei template del design system | `tests/frontend/test_static_assets.py::test_owned_templates_have_no_forbidden_strings_inline_styles_or_handlers` |
| `main.js`: modulo senza dipendenze, reduced motion, `showModal`, `aria-expanded`, Esc | `tests/frontend/test_static_assets.py::test_main_js_is_an_es_module_without_external_dependencies` |
| Nessun overflow orizzontale a 360 / 768 / 1440 in fr e ar; `.reveal` mai nascosto | `tests/frontend/test_browser.py::test_no_horizontal_overflow_and_screenshots` |
| Mega-menu da tastiera (Invio, Esc, ↓, →, ritorno del focus) | `tests/frontend/test_browser.py::test_mega_menu_is_keyboard_operable` |
| Drawer (apertura, Esc, `aria-expanded`) e selettore lingua | `tests/frontend/test_browser.py::test_mobile_drawer_and_language_switcher` |
| Font self-hosted effettivamente caricati, zero richieste esterne | `tests/frontend/test_browser.py::test_fonts_are_self_hosted_and_loaded` |
| Arabo RTL, altre lingue LTR | `tests/compliance/test_public_pages.py::test_arabic_is_rtl_and_others_ltr` |
| Fallback francese dei testi prescritti | `tests/compliance/test_locked_content.py::test_fallback_to_french_for_other_languages` |
| Questo documento e `docs/design/DESIGN_SYSTEM_2026.md` restano veritieri | `tests/frontend/test_design_docs.py::test_wcag_checklist_lists_every_a_and_aa_criterion`, `tests/frontend/test_design_docs.py::test_cited_tests_exist`, `tests/frontend/test_design_docs.py::test_form_field_contract_matches_accessibility_doc` |
| Fogli di stile delle app: solo token reali, nessun colore letterale, nessun gradiente (anello di focus e contrasti restano quelli del sistema) | `tests/frontend/test_design_docs.py::test_conforming_app_stylesheets_use_only_design_tokens` |
| Regressione dei difetti chiusi: sprite XML ben formato (G-01), nessun `backdrop-filter` sull'header che contiene il drawer (G-02), ogni SVG sotto `static/` ben formato | `tests/frontend/test_design_docs.py::test_icon_sprite_is_well_formed_xml`, `tests/frontend/test_design_docs.py::test_sticky_header_does_not_trap_fixed_drawer`, `tests/frontend/test_svg_wellformed.py::test_svg_is_wellformed_xml` |
| Difetto aperto tenuto in vista (xfail finché non corretto: G-22) | `tests/frontend/test_design_docs.py::test_stage1_app_stylesheets_use_only_design_tokens` |
| Breakpoint della navigazione identico in CSS, JS e documenti; stato delle lacune coerente tra i due documenti, i marcatori xfail e il report delle catture | `tests/frontend/test_design_docs.py::test_navigation_breakpoint_is_consistent_and_documented`, `tests/frontend/test_design_docs.py::test_gap_status_and_xfail_markers_stay_in_lockstep`, `tests/frontend/test_design_docs.py::test_capture_report_is_current_and_backs_the_documented_figures` |

Limite dei test browser attuali: `test_mobile_drawer_and_language_switcher` controlla `is_visible()`, che era
vero anche per un drawer alto 65 px (per questo la suite non aveva intercettato G-02), e nessun test browser
gira senza JavaScript (per questo non intercetta G-04). Oggi la geometria del drawer, quella dell'header
senza JS e il rendering delle icone sono misurati solo da `docs/qa/design/capture.py`, che va eseguito a
mano. In QA vanno aggiunte a `tests/frontend/test_browser.py` un'asserzione sull'altezza del drawer, una sul
rendering delle icone (`getBBox()` non nullo) e una sull'altezza dell'header con
`java_script_enabled=False`.

---

## 12. Procedura di test manuale

Da eseguire per ogni pagina nuova e, per intero, nella fase QA (Stage 3), in `fr` e in `ar`.

### 12.1 Percorso da tastiera (senza mouse)

1. Ricaricare la pagina e premere Tab: deve comparire lo skip link; Invio → il Tab successivo è dentro
   `main`.
2. Percorrere tutta la pagina con Tab: ogni tappa ha l'anello visibile (blu su chiaro, bronzo chiaro su
   blu), l'ordine segue la lettura, nessuna tappa è invisibile o fuori schermo.
3. Mega-menu: Invio sul bottone di una sezione → focus nel pannello; Esc → focus sul bottone; ←/→ tra le
   sezioni; ↓ apre; Tab oltre la voce → il pannello si chiude.
4. A 390 px e a 1024 px (il drawer vale sotto 80rem): Invio su «Menu» → focus nel drawer; il drawer copre lo schermo fino in fondo; Tab fino
   all'ultimo link → torna a «Menu»; Esc → chiuso, focus su «Menu».
5. Selettore lingua: Invio apre, Tab entra, Esc chiude; scegliere «العربية» → la pagina è RTL e il focus
   resta gestibile.
6. Form: inviare vuoto → compare il riepilogo e riceve il focus; ogni link del riepilogo porta al campo;
   correggere e reinviare.
7. Dialog, tab, accordion dove presenti: tasti della tabella di §3.
8. Ripetere i punti 1–4 con JavaScript disattivato, a 390 px e a 1024 px: scorrere la pagina e verificare
   che il contenuto resti leggibile sotto l'header (G-04).

### 12.2 Screen reader (controlli a campione)

NVDA + Firefox e Chrome (Windows), VoiceOver + Safari (macOS, iOS), TalkBack + Chrome (Android).

1. Elenco dei landmark: barra istituzionale, header, navigazione principale, main, footer, con nomi
   distinti e tradotti.
2. Elenco dei titoli: un `h1`, nessun salto di livello.
3. Menu: il bottone annuncia «sous-menu … , compresso/espanso»; le voci correnti annunciano «pagina
   corrente».
4. Form con errori: il riepilogo è annunciato; su ogni campo si sentono etichetta, «obbligatorio», «non
   valido», aiuto ed errore.
5. Pagina in italiano o arabo con testi prescritti in francese: il passaggio cambia voce.
6. Pagina araba: e-mail, date e wordmark letti correttamente; ordine di lettura coerente.
7. Messaggio dopo un invio riuscito (redirect): viene annunciato? (G-07)
8. Icone decorative non annunciate; controlli con sola icona annunciati con il loro nome.

### 12.3 Zoom, reflow, spaziatura

1. Zoom del browser al 200 % e al 400 % a 1280 px: nessuno scorrimento orizzontale, nessun testo tagliato o
   sovrapposto, menu utilizzabile.
2. Solo testo al 200 % (Firefox → Zoom solo testo).
3. Bookmarklet «text spacing» (interlinea 1.5, paragrafi 2em, lettere 0.12em, parole 0.16em): nessun testo
   tagliato in bottoni, badge, voci di menu, tab.
4. Rotazione del dispositivo: il layout segue.

### 12.4 Movimento ridotto e preferenze

1. Attivare «riduci movimento» nel sistema: nessuna animazione di comparsa, menu e dialog istantanei,
   ancore senza scroll animato.
2. Modalità contrasto elevato / colori forzati di Windows: bordi dei campi, focus e icone restano
   visibili (da verificare: le icone usano `currentcolor`, i filetti sono bordi reali).
3. Stampa: header, footer di navigazione, breadcrumb e skip link nascosti; URL dei link esterni esplicitati.

### 12.5 Strumenti

axe-core (iniettato da Playwright — Stage 3, zero violazioni «serious» e «critical» su tutte le pagine
pubbliche nelle quattro lingue), Lighthouse Accessibility ≥ 95, controllo del contrasto sui componenti
reali (non solo sui token), validatore HTML (id duplicati, riferimenti ARIA orfani), validazione XML dello
sprite delle icone.

---

## 13. Lacune note e verifica in QA

Gravità: **bloccante** = impedisce l'uso a una parte degli utenti; **alta** = violazione probabile di un
criterio AA; **media / bassa** = rischio o difetto minore. «File» indica dove va fatta la correzione: nessuno
di questi file appartiene all'incarico di documentazione, le correzioni sono state richieste agli owner.

| Id | Gravità | Criterio | Descrizione ed evidenza | File | Correzione proposta | Verifica in QA |
|---|---|---|---|---|---|---|
| G-01 | chiusa il 20/09/2026 (era bloccante) | 1.4.11, 1.1.1 | Lo sprite non era XML ben formato (`--` dentro il commento iniziale, nella parola `.icon--flip-rtl`): `DOMParser` restituiva `parsererror`, `getBBox()` di ogni `<use>` era 0 × 0 e **nessuna icona era disegnata**; i controlli con sola icona risultavano vuoti alla vista. **Chiusa**: l'owner ha riformulato il commento; verificato in Chromium alla seconda revisione (`DOMParser` senza `parsererror`; 546 icone disposte e 0 vuote nel report delle catture) | `static/img/icons.svg` | fatto dall'owner: commento senza doppio trattino; validare lo sprite come XML a ogni modifica | `test_icon_sprite_is_well_formed_xml` passa come test di regressione (non è più xfail); `capture.py` esce con codice 1 se un'icona disposta non disegna nulla |
| G-02 | chiusa il 20/09/2026 (era bloccante) | 2.4.3, 2.4.7, 2.1.1 | `.site-header` aveva `backdrop-filter`, che lo rendeva containing block dei discendenti `position: fixed`: `#nav-drawer` misurava 65 px di altezza (atteso 732 px a 390 × 844) e `.nav-overlay` 0 px; si vedeva solo la prima voce del menu. Con il breakpoint della navigazione a 80rem il difetto toccava anche tablet e laptop fino a 1279 px. **Chiusa**: l'owner ha spostato il velo su `.site-header::before`; misurato alla seconda revisione: drawer alto 731 px su 731 px disponibili a 390 × 844 e 655 px su 655 px a 1024 × 768, overlay a tutto schermo | `static/css/components.css` §7 | fatto dall'owner | `test_sticky_header_does_not_trap_fixed_drawer` passa come test di regressione (non è più xfail); `test_capture_report_is_current_and_backs_the_documented_figures` pretende nel report un drawer alto quanto lo spazio disponibile; resta da aggiungere l'asserzione Playwright alla suite browser |
| G-03 | alta (RTL) | 1.3.2 | In arabo le stringhe d'identità latine non isolate vengono riordinate: footer «™Italy Legal Entry», riga «AGAMI … 2026 ©», punto finale spostato; nella barra il nome del promotore è troncato dall'inizio («…iuridico Interculturale APS») | `static/css/base.css` (helper bidi), `apps/cms/templatetags/cms_nav.py`, `templates/partials/footer.html`, `templates/partials/utility_bar.html` | `dir="ltr"` nel tag `{% brand %}`; `<bdi>` o classe `.ltr` su promotore e riga del © | confronto degli screenshot `ar`; lettura con screen reader arabo |
| G-04 | alta (bloccante senza JS sotto 80rem) | 2.4.11, 2.4.7 | Senza JS, sotto 80rem, il menu è reso in flusso dentro l'header, che resta `position: sticky`: con il menu dello Stage 2 (sotto-pannelli aperti) l'header misura 781 px (erano ≈ 465 px con il menu dello Stage 1) e resta agganciato in alto durante lo scroll. A 390 × 844 restano 63 px di pagina visibili; a 1024 × 768 l'header è più alto del viewport e **il contenuto non è mai visibile** (`docs/qa/design/a11y-nojs-fr-390.png`, `docs/qa/design/a11y-nojs-fr-1024.png`). Contraddice la garanzia «funziona senza JavaScript» (§1, ADR-009) | `static/css/components.css` §7 | `html.no-js .site-header { position: static }` dentro `@media (max-width: 79.999rem)` | il report delle catture registra, senza JS, un header alto meno di metà viewport; screenshot senza JS dopo scroll; test browser con `java_script_enabled=False` |
| G-05 | chiusa il 20/09/2026 (era alta) | 3.3.1, 4.1.3 | `#form-errors` aveva `tabindex="-1"` ma nessuno script vi portava il focus dopo il ricaricamento: l'utente di screen reader ripartiva dall'inizio della pagina. **Chiusa**: l'owner ha aggiunto `initFormErrorFocus` a `static/js/main.js`; misurato alla seconda revisione: dopo un invio non valido del login `document.activeElement.id === "form-errors"` (campo `focus` del report delle catture) | `static/js/main.js` | fatto dall'owner | `test_capture_report_is_current_and_backs_the_documented_figures` pretende nel report il focus sul riepilogo; resta da aggiungere l'asserzione Playwright alla suite browser |
| G-06 | alta | 1.3.1, 4.1.2 | Nel form di iscrizione al Forum `aria-describedby="id_forum_email_errors"` non corrisponde ad alcun elemento (il componente rende `id="id_email_error"`): l'errore non è collegato al campo | `apps/forum/forms.py` (`is_valid`) | eliminare l'impostazione manuale di `aria-invalid` / `aria-describedby`: Django 5.2 li genera già con gli id usati dal componente | test: ogni id in `aria-describedby` esiste nella pagina; regola axe `aria-valid-attr-value` |
| G-07 | media | 4.1.3 | Le regioni `role="status"` sono già popolate al caricamento: dopo un redirect molti screen reader non annunciano il messaggio | `templates/base.html`, `static/js/main.js` | portare il focus sul messaggio, oppure reinserirne il testo dopo il caricamento | prova con NVDA e VoiceOver |
| G-08 | media (era alta) | 3.1.2 | Alla prima stesura non esisteva alcun catalogo `.po` e tutte le stringhe UI comparivano in francese, senza `lang`, nelle pagine `it` / `en` / `ar`. **Alla revisione i cataloghi `locale/{fr,it,en,ar}/LC_MESSAGES/django.po` esistono** (Stage 2, non ancora committati) e skip link, landmark, menu e footer risultano tradotti. Alla revisione ogni catalogo conta 1 792 voci, nessuna senza `msgstr`. Restano: «Privacy Policy» e «Cookie Policy», letterali inglesi senza `lang="en"`; il rischio che una stringa aggiunta senza aggiornare i cataloghi ricada sul francese senza `lang`; la rilettura da parte di madrelingua (i testi prescritti e legali restano fuori dai cataloghi e non si traducono mai automaticamente) | `templates/partials/footer.html`, `locale/` | `lang="en"` sui due titoli; tenere i cataloghi allineati a ogni nuova stringa; revisione linguistica IT / EN / AR | `scripts/i18n_audit.py` senza msgid non tradotti; controllo a campione con screen reader |
| G-09 | chiusa il 21/09/2026 (era bassa) | 1.4.3 | Le numerazioni decorative erano in `--color-accent-600` (bronzo, 3.83:1 sul fondo): `.entrance__num`, `.pathway-list__num`, `.numeral`. Erano `aria-hidden` e ridondanti rispetto a `<ol>`, ma piccole e sotto la soglia del testo. **Chiusa dalla redirezione**: il bronzo non esiste più, gli ordinali sono in `--rubric` e misurano 6.92:1 sulla carta e 6.23:1 sul fondo di processo, quindi sono sicuri anche se letti come testo | `static/css/tokens.css` | fatto: la coppia è bloccata da `test_wcag_contrast` | la riga «rubrica sulla carta» della tabella di `docs/design/DESIGN_SYSTEM_2026.md` §5, ricalcolata dal test |
| G-10 | bassa | 2.5.8 | «Mot de passe oublié ?» è alto 17 px e sta a circa 2 px dal campo password: il cerchio da 24 px interseca il campo | `templates/allauth/elements/field.html`, `static/css/components.css` (`.form-field__help a`) | `display: inline-block; padding-block: var(--space-1)` sui link nell'aiuto | misura dei bersagli in QA |
| G-11 | media | 2.4.3 | Il drawer non rende inerte il resto della pagina: il cursore virtuale può uscire dal menu aperto | `static/js/main.js` (`initNavigation`) | attributo `inert` su `main` e `footer` mentre il drawer è aperto | prova con screen reader mobile |
| G-12 | bassa | 1.4.13 | Senza JS i pannelli del mega-menu appaiono su hover e non si possono chiudere con Esc | `static/css/components.css` §7 | accettare (solo modalità senza JS) oppure mostrare i pannelli solo su `:focus-within` | decisione di QA |
| G-13 | bassa | 4.1.2 | `cta_panel.html` ricava l'`id` da `title` passato al filtro `slugify` (vuoto per titoli non latini, duplicato per titoli uguali); `hero.html` usa l'`id` fisso `hero-title` | `templates/components/cta_panel.html`, `templates/components/hero.html` | parametro `id` opzionale | validatore HTML: nessun id duplicato |
| G-14 | bassa | 3.1.2 | `.meta-row__item dt::after { content: " :" }` — punteggiatura francese generata in CSS, non tradotta | `static/css/components.css` §13 | separatore nel template, dentro `{% translate %}` | revisione linguistica |
| G-15 | chiusa il 21/09/2026 (era bassa) | — | `--font-mono` nominava IBM Plex Mono, che non era self-hosted: il registro tecnico era Consolas su Windows e Menlo su macOS, tre texture per un ruolo. **Chiusa dalla redirezione**: il ruolo è ora `--font-ref` (Fira Mono), i cui due file woff2 sono in `static/fonts/` e dichiarati in `static/css/fonts.css`; lo shim fa risolvere `--font-mono` a `--font-ref` | `static/css/tokens.css` | fatto | `tests/frontend/test_layout.py::test_fonts_css_references_only_local_files_that_exist` e la tabella dei file di `docs/design/DESIGN_SYSTEM_2026.md` §6.2 |
| G-16 | chiusa il 20/09/2026 (era bassa) | — | `docs/I18N_RTL.md` era citato nei commenti dei CSS e nell'intestazione dei cataloghi `locale/` ma non esisteva. **Chiusa**: il documento è stato scritto | `docs/` | fatto | il file esiste; `tests/frontend/test_design_docs.py::test_cited_paths_exist` non ha più eccezioni |
| G-17 | media | 2.2.1 | Un form pubblico compilato in più di 6 ore è trattato come spam e scartato in silenzio | `apps/core/forms.py` (`MAX_FILL_SECONDS`) | portare il limite oltre 20 ore o mostrare un messaggio che invita a reinviare | revisione con il responsabile sicurezza |
| G-18 | alta (processo) | tutti | axe-core non è ancora stato eseguito; nessun test con screen reader reali | `tests/` (Stage 3) | suite `a11y` con axe iniettato da Playwright su tutte le route pubbliche × 4 lingue | zero violazioni «serious» / «critical» |
| G-19 | bassa | — | Le FAQ usano `.accordion__panel`, non definita dal design system (il componente usa `.accordion__body`): il corpo della risposta non riceve padding né misura | `templates/faq/_item.html` | usare `.accordion__body` | revisione visuale |
| G-20 | bassa | — | `.reveal--stagger` non produce scaglionamento visibile e ritarda l'hover dei figli fino a 480 ms | `static/css/components.css` §29 | animare i figli o rimuovere il modificatore | revisione visuale |
| G-21 | bassa | — | L'opzione `remember` delle tab scrive in `localStorage` ma non rilegge il valore | `static/js/main.js` (`initTabs`) | leggere la chiave all'inizializzazione o rimuovere l'opzione | test Playwright |
| G-22 | media — chiusa | 2.4.7, 1.4.11 | Due fogli di stile dello Stage 1 non usano il design system: richiamano token che non esistono (`var(--color-focus, #d97706)`, `var(--color-primary, #0f2b52)`…), quindi valgono sempre i ripieghi scritti a mano. Effetti sull'accessibilità: nelle pagine del Forum e del wizard di orientamento l'anello di focus non è quello a due toni del sistema ma un contorno da 3 px oro `#b8893a` (3.01:1 sul fondo) o arancio `#d97706` (3.05:1), appena sopra la soglia di 3:1 e diverso dal resto del sito; colori e scala tipografica non seguono i token e non sono coperti da `test_wcag_contrast` | `apps/forum/static/forum/forum.css`, `apps/orientation/static/orientation/wizard.css` | riscrivere i due fogli sui token reali e lasciare il focus a `static/css/base.css`; dettagli in `docs/design/DESIGN_SYSTEM_2026.md` §2.1 | test: nessun `var(--…)` verso token inesistenti nei fogli delle app; axe `color-contrast`; percorso da tastiera su Forum e wizard  **Chiusa il 20 settembre 2026**: i due fogli usano solo token reali, senza gradiente né ombre o anelli di focus propri; `test_stage1_app_stylesheets_use_only_design_tokens` e `tests/frontend/test_css_tokens_exist.py` lo verificano. |
| G-23 | media | 1.4.3, 1.4.11 | A drawer aperto, con la pagina non scrollata, `.nav-overlay` (`position: fixed; inset-block-start: var(--header-height)`) parte da 72 px dall'alto del viewport, ma la barra istituzionale è ancora visibile e l'header finisce a 113 px: il velo `--surface-overlay` è dipinto sopra la fascia bassa dell'header e copre wordmark e bottone «Menu» (che a drawer aperto è il controllo di chiusura). Sotto il velo l'etichetta «Menu» scende a 3.92:1 (`--color-primary-900` su fondo velato `#79889c`), sotto la soglia di 4.5:1. Emerso con la correzione di G-02 (prima l'overlay misurava 0 px): `main.js` scrive `--nav-drawer-top` sul solo drawer e l'overlay, che ne è fratello, non la eredita (`docs/qa/design/state-drawer-open-fr-390.png`, `docs/qa/design/state-drawer-open-fr-1024.png`) | `static/css/components.css` §7, `static/js/main.js` (`initNavigation`) | impostare `--nav-drawer-top` su `#site-header` (o su `<html>`) e usare `inset-block-start: var(--nav-drawer-top, var(--header-height))` anche per `.nav-overlay` | nel report delle catture `overlayTop` ≥ `headerBottom`; confronto degli screenshot del drawer aperto |
| G-24 | chiusa il 21/09/2026 (era media) | 1.4.5, prestazioni | `templates/base.html` precaricava per le pagine LTR due woff2 che non esistevano più — `ibm-plex-sans-400-normal-latin.woff2` e `ibm-plex-serif-500-normal-latin.woff2` — perché la redirezione aveva cambiato le famiglie e il preload era rimasto quello vecchio: due 404 per pagina e nessun preload utile, quindi il testo restava più a lungo nel fallback di sistema. **Chiusa**: le pagine LTR precaricano ora il serif di lettura e l'interfaccia, le pagine RTL il Naskh e il sans arabo | `templates/base.html` | fatto | `tests/frontend/test_design_docs.py::test_listed_font_files_exist_and_every_font_file_is_listed` confronta ogni preload con i file su disco; nessun 404 di font nei log |
| G-25 | chiusa il 21/09/2026 (era media) | 1.4.11, 2.4.7 | Sei custom property erano consumate e non erano dichiarate da nessun foglio: lo shim di demolizione non le aveva mappate. --ease-standard (in `base.css`, `components.css`, `ecosystem.css`, `pages.css`) faceva perdere la curva a ogni transizione che la nominava; --measure-narrow toglieva il tetto di misura ai testi brevi centrati; --z-below, --z-dropdown, --z-modal e --z-skiplink valevano `auto`, quindi skip link, dropdown e dialog senza JS perdevano il loro livello dichiarato. **Chiusa**: le sei righe sono state aggiunte allo shim, mappate sui token reali, e lo skip link risolve al livello del dialog, il più alto della lista nominata | `static/css/_legacy-tokens.css` | fatto | `tests/frontend/test_css_tokens_exist.py::test_every_referenced_custom_property_is_defined` passa su tutti i fogli; `tests/frontend/test_design_docs.py::test_conforming_app_stylesheets_use_only_design_tokens` controlla ora tutti e cinque i fogli delle app senza eccezioni |
| G-26 | media (processo) | 1.4.11, 1.4.3 | I cancelli meccanici della direzione non sono ancora soddisfatti da `components.css`: `box-shadow` compare ancora su otto selettori (tutti con token che valgono `none`, quindi senza effetto visivo, ma la regola è «nessuna dichiarazione fuori da `.nav-drawer` e `dialog`»), `border: 1px` non è ancora ristretto ai controlli e a `dialog`, e il livello `@media (forced-colors: active)` esiste in `static/css/register.css` ma non copre la shell né i componenti: sotto contrasto elevato di Windows le barre `aria-current`, i punti d'errore e i filetti dipinti come sfondo di uno pseudo-elemento spariscono. Manca anche la cattura a colori forzati nella matrice degli screenshot. **Rimisurato il 24 settembre 2026** (`scripts/qa_chrome_media.py`, `docs/design-v3/QA_PREFERENZE.md`): su sei pagine pubbliche e tre della piattaforma con sessione, nessun indicatore disegnato come sfondo di uno pseudo-elemento sparisce sotto `forced-colors: active` (49 esaminati, 0 perduti), compresa la guida `aria-current`; i `.state` e i `.badge` hanno ora un proprio blocco a colori forzati in `v3/chip.css`. Resta aperta la parte sulle ombre e la prova su Windows reale | `static/css/components.css`, `docs/qa/design/capture.py`, `tests/frontend/` | estendere a `components.css` il livello a colori forzati di `register.css` durante la sua migrazione; aggiungere i tre test meccanici | una cattura a colori forzati per archetipo; prova manuale §12.4.2 |
| G-27 | chiusa il 21/09/2026 (era bassa) | 1.4.3 | `static/css/register.css` dipingeva l'ordinale del folio dentro una fascia verso con `--rubric-on-navy` (`.plate--verso .folio__ordinal { color: … }`), che misura **4.46:1** sul navy. A `xl` il numerale è di 44 px e ricade nella soglia del testo grande (3:1); a `xs` e `sm` è di 22 e 24 px, sotto i 24 px, quindi gli si applicava 4.5:1 e mancava per 0.04. **Chiusa**: il numerale è ora `--paper-on-navy` (13.62:1) e `--rubric-on-navy` è rimasto il solo filetto, come dice il commento del token | `static/css/register.css` | fatto | le cinque dichiarazioni che consumano `--rubric-on-navy` in `static/css/` sono tutte bordi; controllo del contrasto sul componente reale |

### 13.1 Come verrà chiusa la verifica (Stage 3 QA)

1. Correzione di G-04 (una regola CSS) e di G-03 e G-06, poi nuova cattura con
   `docs/qa/design/capture.py` (G-01, G-02 e G-05 sono già chiuse e verificate).
2. Suite `a11y`: axe-core locale (nessun CDN) iniettato da Playwright su ogni route registrata in
   `core.public_routes`, nelle quattro lingue, a 390 e 1440 px, con gate di Fase 3 aperto e chiuso; soglia:
   zero violazioni «serious» / «critical»; le altre elencate nel report QA.
3. Asserzioni Playwright aggiuntive: altezza del drawer, icone disegnate, focus sul riepilogo errori, id di
   `aria-describedby` esistenti, nessun id duplicato, bersagli ≥ 24 px o eccezione documentata.
4. Percorso manuale di §12 su home, uno spazio, un form aperto (fixture `legal_published`), wizard di
   orientamento, login, 404 — in francese e in arabo.
5. Aggiornamento di questa tabella: una lacuna si chiude solo con l'evidenza indicata nell'ultima colonna.
