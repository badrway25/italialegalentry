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
| Design V5, «Il portico» | 8 ottobre 2026 (W2-C1): la cromatura pubblica riscritta — barra istituzionale, testata, le quattro porte e i loro pannelli, la targa, il cassetto; G-04 e G-23 chiusi e misurati in Chromium; il modello tastiera di §3 e i test di §11 aggiornati |
| Design V5, il foglio e il popover della targa | 11 ottobre 2026 (W2-C2): il menu sotto 80rem è il drawer modale del sistema di overlay (la trappola, la pagina dietro fuori dall'albero, Esc e il fuoco di ritorno su «Menu»), la targa autenticata apre il popover del conto, il nome della sola chiave è il tooltip del sistema; G-11 chiusa; §3, §4.3, §9.1, §11 e le lacune aggiornati |
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
> restano aperte lacune di gravità alta (G-03, G-06) — G-04, che rendeva illeggibili le pagine senza
> JavaScript sotto 80rem, è chiusa dalla cromatura V5 (8 ottobre 2026) — e la scansione automatica completa non è ancora stata eseguita. L'impianto
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
| 1.4.3 | Contrast (Minimum) | AA | Conforme | 29 coppie bloccate da `tests/frontend/test_static_assets.py::test_wcag_contrast`; tabella misurata in `docs/design/DESIGN_SYSTEM_2026.md` §5 (minimo per testo: 5.91:1, marginalia sul fondo di processo). G-09 è chiusa: le numerazioni non sono più in bronzo a 3.83:1 ma in rubrica a 6.92:1, quindi nessuna esenzione serve più. G-23 è chiusa: il velo del cassetto parte dal piede reale dell'header e non copre più il bottone «Menu» |
| 1.4.4 | Resize Text | AA | Conforme | scala in `rem`; verificato a 200 % (`docs/qa/design/a11y-zoom200-fr-640.png`): nessuna perdita di contenuto o funzione |
| 1.4.5 | Images of Text | AA | Conforme | il wordmark è testo vivo (`{% brand %}`); nessuna immagine di testo nei componenti; `og-default.png` non è mostrata in pagina |
| 1.4.10 | Reflow | AA | Conforme | nessuno scorrimento orizzontale a 320 px CSS (`docs/qa/design/a11y-zoom400-fr-320.png`, `docs/qa/design/a11y-zoom400-ar-320.png`; report `docs/qa/design/capture-report.json`) e a 360 px (`tests/frontend/test_browser.py::test_no_horizontal_overflow_and_screenshots`); contenuti larghi in `.scroll-x`; sotto 30rem di altezza il foglio del menu non fissa il piede: a 320 × 256 la lista prende il 78 % della vista (prima il 31 %) e la targa si raggiunge alla fine, mai sotto la testa (W2-C2, `tests/frontend/test_browser_w2_c2.py::test_a_short_viewport_does_not_pin_the_foot`) |
| 1.4.11 | Non-text Contrast | AA | Parziale (G-22) | perimetro dei campi 3.50:1 sulla carta e 3.74:1 dentro il campo (`--rule-ink`), anello di focus 13.62:1 su fondo chiaro e 13.62:1 su navy, bordi di stato ≥ 3.16:1, filetto d'ordine 6.92:1. Le icone sono disegnate (G-01 chiusa: 0 icone vuote nel report delle catture), quindi i controlli con sola icona (`.main-nav__toggle`, `.dialog__close` e, sotto 48rem, il link «Espace réservé» `.utility-bar__link`, la cui etichetta è solo per screen reader) sono visibili. Il menu del conto aperto dal piede notturno del foglio disegna l'anello della carta (#1d8a93, 4,11 : 1): il piede non è più `on-inverse`, solo i suoi comandi prendono l'anello della notte (prima le righe ne disegnavano uno a 1,75 : 1 sul bianco; W2-C2, `tests/frontend/test_browser_w2_c2.py::test_the_account_menu_from_the_night_foot_draws_the_paper_ring`). Lacuna: le pagine del Forum e del wizard usano un anello di focus proprio, al limite della soglia di 3:1 |
| 1.4.12 | Text Spacing | AA | Conforme | nessuna `height` fissa su contenitori di testo (solo `min-block-size`; dimensioni fisse soltanto per icone, filetti e marcatori circolari numerati); col foglio standard (interlinea 1.5, lettere 0.12em, parole 0.16em) la barra del portico va a capo e la testata cresce di una riga, nulla della cromatura esce dal viewport e la pagina non scorre di lato — misurato in Chromium a 1024 / 1280 / 1440 in fr e ar (W2-C1, 9/10/2026; `tests/frontend/test_browser_w2_c1.py::test_the_bar_wraps_under_text_spacing_and_never_clips`); il bookmarklet di §12.3 resta la prova manuale sulle altre pagine |
| 1.4.13 | Content on Hover or Focus | AA | Parziale (G-12) | con JS il portico si apre dopo 120 ms di intenzione del puntatore: il pannello è sorvolabile (hoverable), si chiude con Esc (dismissible) e resta finché il puntatore non lo lascia, con una grazia di 250 ms (persistent); da tastiera e click porta lo scrim; il focus che lascia la navigazione chiude; il nome della targa (la sola chiave sotto 100rem) è il tooltip del livello superiore del sistema di overlay (`data-tip="layer"`): dopo l'attesa al passaggio del puntatore, subito al fuoco, sorvolabile, via con Esc o una pressione finché puntatore o focus restano (`overlay.js`; da 100rem rifiutato, la parola è sulla targa: `nav.js`, W2-C2). Senza JS i pannelli appaiono su `:hover` / `:focus-within` e non sono chiudibili con Esc |
| 2.1.1 | Keyboard | A | Conforme | ogni controllo è un `a`, `button`, `summary` o campo nativo; modello in §3; `tests/frontend/test_browser.py::test_mega_menu_is_keyboard_operable` |
| 2.1.2 | No Keyboard Trap | A | Conforme | il foglio sotto 80rem e ogni dialog del sistema di overlay: Tab gira dentro finché è aperto, Esc o «Fermer» lo chiudono e il fuoco torna all'apertura; popover e dropdown: Esc |
| 2.1.4 | Character Key Shortcuts | A | Conforme | nessuna scorciatoia a carattere singolo in `static/js/main.js` |
| 2.2.1 | Timing Adjustable | A | Parziale (G-17) | nessun limite di tempo nell'interfaccia; l'anti-spam (`apps/core/forms.py` → `MAX_FILL_SECONDS`, 6 ore) scarta in silenzio un form compilato più lentamente: da valutare |
| 2.2.2 | Pause, Stop, Hide | A | Conforme | nessun contenuto in movimento automatico oltre 5 s: reveal 600 ms e contatori 900 ms, una sola volta; nessun carousel, nessun autoplay |
| 2.3.1 | Three Flashes or Below Threshold | A | Conforme | nessun lampeggio |
| 2.4.1 | Bypass Blocks | A | Conforme | `templates/base.html` → `a.skip-link[href="#main-content"]` + `main#main-content[tabindex="-1"]`; misurato: Tab → Invio porta il focus su `main-content`; `tests/frontend/test_layout.py::test_shell_landmarks_skip_link_and_single_h1` |
| 2.4.2 | Page Titled | A | Conforme | `templates/base.html` → `<title>{% block page_title %} · Italy Legal Entry™`; le pagine d'errore e account lo valorizzano |
| 2.4.3 | Focus Order | A | Conforme | ordine del DOM; il portico è una disclosure: il focus resta sulla porta, ↓ entra nel pannello che segue la porta nel DOM, Esc lo restituisce; l'apertura del foglio e dei dialog sposta il focus nel pannello e lo restituisce alla chiusura; a foglio aperto la pagina dietro è `aria-hidden` e non prende il fuoco: il cursore virtuale non ne esce (G-11 chiusa, W2-C2) |
| 2.4.4 | Link Purpose (In Context) | A | Conforme | testi dei link descrittivi; «Voir l’espace» è nel pannello che porta il nome della sezione; stretched link con il titolo come nome accessibile |
| 2.4.5 | Multiple Ways | AA | Da confermare in QA | menu principale + navigazione del footer + breadcrumb + ricerca interna di FAQ e glossario + `sitemap.xml`; manca una mappa del sito in HTML o una ricerca globale: da decidere in QA |
| 2.4.6 | Headings and Labels | AA | Conforme | un `h1` per pagina (test), `h2` di sezione (`templates/components/section_header.html`), `h3` negli elenchi; etichette dei campi sempre visibili |
| 2.4.7 | Focus Visible | AA | Conforme | `static/css/base.css` → `:focus-visible` (outline 2 px + alone 2 px); variante `.on-inverse`; misurato su 16 tappe (§4.4) |
| 2.4.11 | Focus Not Obscured (Minimum) | AA | Conforme | `html { scroll-padding-block-start: calc(var(--chrome-block-size) + var(--s-4)) }` in `base.css` e, sotto la testata V5, `calc(var(--header-h) + var(--s-4))` in `v5/chrome.css` tengono il focus sotto l'header sticky (misurato: `tests/frontend/test_browser_w2_c1.py::test_focus_is_not_obscured_by_the_sticky_letterhead`); `.section-nav` sticky sotto l'header. G-04 è chiusa: senza JS, sotto 80rem, l'header non è più sticky |
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

Riepilogo: 55 criteri — 33 conformi, 7 parziali, 9 da confermare in QA, 6 non applicabili.

---

## 3. Modello tastiera dei componenti interattivi

Regola generale: **Tab / Shift+Tab** seguono l'ordine del DOM; **Invio** attiva link e bottoni; **Spazio**
attiva bottoni, `summary` e checkbox; **Esc** chiude ciò che si è aperto e restituisce il focus a chi lo ha
aperto. Le frecce orizzontali si invertono in arabo.

| Componente | Tasti | Focus e stato | Senza JS |
|---|---|---|---|
| Skip link (`templates/base.html`) | primo Tab della pagina; Invio | appare in alto a `inline-start`; porta il focus su `main#main-content` (`tabindex="-1"`) | identico |
| Menu `<details>` (`details[data-dropdown]`: la lingua della rail) | Invio/Spazio sul `summary` apre e chiude; Tab entra nella lista; Esc chiude | `aria-expanded` sul `summary`; Esc riporta il focus al `summary` e, dentro un pannello, chiude la lista prima del pannello (la lingua prima del cassetto); si chiude alla perdita di focus e al click esterno; uno aperto per volta — `static/js/src/overlay.js` dove la pagina lo carica (la console), altrimenti il ripiego di `main.js` | `<details>` nativo: apre e chiude; resta aperto finché non lo si richiude |
| Popover e menu (`templates/components/popover.html`: il conto — `templates/components/account_menu.html` con `popover` — nella barra della console, nella targa della testata e nel piede del foglio; il menu di ogni riga di «Mes documents») | Invio/Spazio sul comando apre e chiude; ↓ ↑ Home Fine fra le righe; Esc chiude | il fuoco sulla prima riga, di ritorno al comando dopo Esc o una scelta; il click fuori e il fuoco che esce lo chiudono senza spostare il fuoco; `aria-expanded` sul comando, il conto nominato «‹nome breve› — Mon compte»; ≤ 40rem uno sheet dal basso che resta un menu (né trappola né blocco dello scroll), sopra l'unico scrim che prende tutta la pressione che lo chiude — la pagina dietro non la riceve mai, nemmeno al tocco sopra il foglio del menu: lo scrim resta al suo posto finché la pressione dura (W2-C2, `tests/frontend/test_browser_w2_c2.py::test_a_tap_on_the_menu_sheets_scrim_reaches_nothing_beneath`) —, col suo nome in testa | `popover` nativo: si apre, si chiude al click fuori e con Esc |
| «Il portico» (≥ 64rem; `templates/partials/main_nav.html`, `static/js/src/nav.js`) | Tab fra le porte, i link e la targa; Invio/Spazio su una porta apre e chiude il pannello (il focus resta sulla porta); ↓ apre ed entra (prima voce); ↑ sulla prima voce torna alla porta, pannello aperto; ←/→ fra le voci di primo livello (circolari, invertite in arabo) — a pannello aperto la porta vicina si apre al loro posto, mai una chiusura; Home / Fine prima / ultima voce (della barra, o del pannello se il focus è lì); Esc chiude | `aria-expanded`, `aria-controls` sulla porta (disclosure, non `menubar`); Esc → focus alla porta; lo scrim solo da tastiera, click e tocco; il focus che lascia la navigazione chiude (1.4.13); «l'architrave» segue il focus senza viaggiare | pannelli su `:hover` / `:focus-within`: raggiungibili con Tab, non chiudibili con Esc (G-12) |
| Drawer (< 80rem: telefono, tablet, laptop fino a 1279 px) — il foglio, drawer modale del sistema di overlay (`templates/partials/main_nav.html`, W2-C2) | Invio/Spazio su «Menu» (un link che `overlay.js` fa bottone); Tab e Shift+Tab ciclici dentro il foglio; Invio/Spazio su una porta la apre o la chiude sul posto, una per volta; Esc chiude | il fuoco su «Fermer» all'apertura e di ritorno su «Menu» alla chiusura; `aria-modal`, `aria-expanded`; la pagina dietro `aria-hidden` e senza pressione, lo scroll bloccato senza scatto; la porta della sezione corrente aperta e marcata; la testa del foglio sopra lo scrim (G-23) | «Menu» è un link al foglio, che si mostra sul posto (`:target`); «Fermer» un link indietro; le porte si aprono nativamente (G-04 chiusa) |
| Breadcrumb, navigazione locale, sommario di pagina, footer | Tab, Invio | voce corrente `aria-current` (non linkata nel breadcrumb) | identico (il sommario non evidenzia la sezione in vista) |
| Tab (`templates/components/tabs.html`) | ←/→ scheda precedente/successiva con attivazione immediata; Home / Fine; Tab entra nel pannello | roving `tabindex`; `aria-selected`; pannello `tabindex="0"` | niente tablist: pannelli impilati con titolo `h3` |
| Accordion (`templates/components/accordion.html`) | Invio/Spazio sul `summary` | stato espanso annunciato dal browser; con `single` si chiudono gli altri | identico (senza esclusività nei browser privi di `<details name>`) |
| Stepper lato client (`[data-stepper]`) | Invio/Spazio su «successivo» / «precedente» | il focus va sul titolo del passo (`tabindex="-1"`); `aria-current="step"` | tutti i passi visibili |
| Dialog, alertdialog, drawer modale, sheet (`templates/components/dialog.html` e la sua famiglia; il cassetto della console) | Invio/Spazio sull'apertura (un link `href="#id"` che `overlay.js` fa bottone); Tab e Shift+Tab ciclici dentro il pannello; Esc chiude (in un alertdialog è la risposta sicura) | la trappola del sistema degli overlay (la regola INP del piano: `show()`, `aria-modal="true"`, l'unico scrim): la pagina dietro non prende né una pressione né il fuoco, un fuoco mandato fuori torna dentro, ed è `aria-hidden` finché il pannello è aperto (Chromium non pota nulla per il solo `aria-modal`); il fuoco entra su `[data-overlay-focus]`, la risposta sicura, la voce corrente o il primo controllo — portato nella vista del pannello —, ed esce verso l'apritore; un corpo che scorre senza nulla da mettere a fuoco è una fermata sua; lo scrim chiude solo se la pressione vi comincia e vi finisce, mai un alertdialog, mai con un campo scritto; «Fermer» sempre presente | il link `#id` mostra il pannello via `:target`, subito; «Fermer» è un link indietro |
| Card, entrance, pathway item (stretched link) | Tab, Invio | **un solo** tab stop per elemento (il link del titolo o la CTA) | identico |
| Hero V5.4 (`templates/pages/home/_hero.html`, W2-D): i quattro accessi e il bottone sopra la chiave d'oro | Tab tra le due azioni, i quattro accessi e il bottone «Rejouer l’animation de la porte»; Invio sui link; Invio/Spazio sul bottone | ogni accesso è un solo link, nominato dalla parola e descritto dalla frase e dall'invito; il focus mostra colore, invito, via e risposta della porta a 0 ms e manda la luce lungo il sentiero (`hero.js`); il bottone rimanda l'intera sequenza dalla porta chiusa; la scena della porta è decorativa (`aria-hidden`), il bottone sta fuori da essa, centrato sulla chiave (≥ 44 px); anello notturno di 2 px, e l'alone della chiave acceso al focus e al passaggio del puntatore; con `prefers-reduced-motion: reduce` e colori forzati il bottone non è disegnato. Sui telefoni il bottone prende il focus dopo le quattro tessere pur stando sopra di esse (ordine del DOM: accessi, poi nicchia; composizione: fascia, poi tessere): accettato — significato e operabilità restano (2.4.3; controllo di accessibilità W2-D, F7), `reading-flow` in un passaggio successivo. Dove nulla passa sopra (`hover: none`) l'alone della chiave resta acceso piano a riposo: è il segno del controllo per chi tocca (l'anello è della tastiera, l'alone al passaggio del puntatore fine). La pressione di un dito su un accesso si arma 100 ms dopo l'appoggio, o al sollevamento: uno scorrimento che parte da una tessera non mostra stato né luce | i link funzionano; il bottone non è disegnato (lo mostra `hero.js`) |
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

- **Dialog** (e alertdialog, drawer modale, sheet: il sistema degli overlay, `static/js/src/overlay.js`, W2-A):
  `<dialog>` nativo aperto con `show()`, `aria-modal="true"` e l'unico scrim, con la trappola in script — Tab e
  Shift+Tab girano dentro, un fuoco mandato fuori torna dentro, la pagina dietro non prende la pressione ed esce
  dall'albero dell'accessibilità (`aria-hidden` finché il pannello è aperto, mai `inert`: Chromium non pota nulla per
  il solo `aria-modal`, DL54-93) —, Esc, il blocco dello scroll; il fuoco iniziale nel compito dell'input, portato
  nella vista del pannello (la voce corrente in fondo a una lista lunga), e **restituito all'elemento di apertura** (o
  al suo successore). `showModal()` rendeva inerte e ristilava tutta la pagina a ogni apertura (la regola INP del
  piano V5.4 §1.14): resta per una pagina leggera (`data-overlay-modal="native"`). Il cassetto della console è
  uno di questi drawer modali.
- **Il foglio del menu** (sotto 80rem; W2-C2): uno di questi drawer modali — la stessa trappola, la stessa pagina
  dietro fuori dall'albero (G-11 chiusa: il cursore virtuale non esce più dal menu aperto), Esc, lo scrim, «Fermer» o
  un link lo chiudono e il fuoco torna su «Menu». Possiede la sua riga di testa — il lock-up e «Fermer», che prende il
  primo fuoco —, così nessun velo copre mai l'uscita (G-23); sta fuori dall'header (G-02).
- **Il portico e i dropdown**: si chiudono alla perdita di focus; Esc restituisce il focus al controllo (alla porta,
  per il portico).
- **Riepilogo degli errori**: la validazione è lato server, quindi dopo un invio non valido la pagina si
  ricarica dall'inizio; `initFormErrorFocus` porta il focus su `#form-errors` (`tabindex="-1"`,
  `role="alert"`) e lo scorre al centro del viewport (misurato: `document.activeElement.id ===
  "form-errors"`; G-05 chiusa).

### 4.4 Ordine di tabulazione misurato (`/fr/`, 1440 px)

Misura ripetuta alla revisione sulla home dell'app `pages` (Stage 2, menu popolato da `seed_all`):

1 skip link → 2–5 le quattro lingue della barra istituzionale → 6 wordmark → 7–12 le sei voci del portico, una
fermata per porta (il pannello aperto segue la sua porta nel DOM) → 13 «Espace réservé» (la targa) → contenuto
(14–15 i due bottoni dell'hero, poi il banner del Forum e il primo accesso…) → e-mail del footer → cinque link
legali → navigazione del footer. L'ordine coincide con l'ordine visivo in LTR e, specchiato, in RTL (misura
ripetuta sulla cromatura V5, 8 ottobre 2026).

### 4.5 Focus non coperto

`scroll-padding-block-start` = altezza dell'header + 16 px; gli elementi sticky (`.site-header`,
`.section-nav`, `.layout-sidebar__aside`) non si sovrappongono tra loro perché usano `--header-height` come
origine. Sotto la testata V5 il padding vale `--header-h` + 16 px (`v5/chrome.css`), misurato da
`tests/frontend/test_browser_w2_c1.py::test_focus_is_not_obscured_by_the_sticky_letterhead`. G-04 è chiusa: senza JS,
sotto 80rem, la testata contiene solo la sua riga e il menu si mostra sul posto, a richiesta (W2-C2).

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
  <div class="form-field__help" id="id_email_helptext">…</div>
  <div class="form-field__errors" id="id_email_error" role="alert"><ul class="form-field__error-list"><li>…</li></ul></div>
</div>
```

| Garanzia | Meccanismo |
|---|---|
| Etichetta sempre visibile e associata | `<label for="{{ field.id_for_label }}">`; per le checkbox l'etichetta è a fianco ed è cliccabile; il placeholder non sostituisce mai l'etichetta |
| Obbligatorietà | asterisco `aria-hidden` + attributo `required` sul controllo + nota «Champs obligatoires» (`.form__required-note`) |
| Aiuto collegato | `<div id="<auto_id>_helptext">` (un `<div>`: l'aiuto della password di Django è un elenco, che un `<p>` non può contenere — W1-C, review M1); Django 5.2 aggiunge `aria-describedby` con lo stesso id |
| Errore collegato | `<div id="<auto_id>_error" role="alert">` che contiene l'elenco `<ul>` (il ruolo sull'elenco ne toglieva la semantica: axe `listitem`, W1-C, A11Y A2); Django 5.2 aggiunge `aria-invalid="true"` e l'id dell'errore in `aria-describedby`. **Non impostare `aria-describedby` a mano sul widget**: sovrascrive quello di Django e rompe il collegamento (è ciò che accade in G-06) |
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

**Il movimento ridotto è uno stato, non un interruttore** (design V5 — piano V5.4 §1.5, famiglia W1-D, 5 ottobre
2026). Con `prefers-reduced-motion: reduce` ogni livello mostra il suo *fermo*: lo stesso stato finale che il moto
avrebbe raggiunto, senza il tragitto — ed è anche lo stato senza JavaScript. Quattro pezzi, tutti attivi insieme:

1. **I token.** `static/css/v5/tokens.css` azzera, nel blocco `prefers-reduced-motion: reduce`, ogni durata che
   dichiara — `--motion-fast`, `--motion-standard`, `--motion-emphasized`, `--motion-slow`, `--motion-draw`,
   `--motion-route-light`, `--motion-route-stagger`, `--motion-stagger`, `--motion-key`, `--motion-door`,
   `--motion-luce` e le tre durate delle molle (`--spring-soft-duration`, `--spring-snappy-duration`,
   `--spring-sheet-duration`) — perché nulla in V5 è in loop e un ciclo a 0 ms non gira. Restano la soglia
   `--motion-wait` (400 ms: un'attesa non è un movimento) e `--motion-reduced` (80 ms), l'unica dissolvenza
   d'opacità che un overlay può conservare, letta solo dentro un blocco di moto ridotto e solo su `opacity`
   (MS-O4). Il V1 `static/css/tokens.css` continua ad azzerare `--motion-fast`, `--motion-base` e `--motion-slow`, e
   lo shim li propaga ai nomi legacy `--duration-fast`, `--duration-base` e `--duration-slow`
   (`docs/design/DESIGN_SYSTEM_2026.md` §17).
2. **Nessuna rete di sicurezza universale.** La regola `* { transition-duration: 0.01ms !important; … }` di
   `static/css/components.css` §29 è stata rimossa: un `!important` universale copriva ogni transizione scritta fuori
   dai token e impediva di progettare lo stato. Ogni transizione e animazione è scritta sui token, quindi atterra
   subito; restano due guardie mirate (`.reveal` visibile; il keyframe di `dialog` spento). Il portico (W2-C1) è
   una transizione: a movimento ridotto un'unica opacità di 80 ms, `--motion-reduced`, `v5/chrome.css` §9 — la
   dissolvenza che MS-O4 concede a un overlay. `static/css/base.css` porta `scroll-behavior` ad `auto`.
3. **Un solo cancello per il moto via script.** In `static/js/src/motion.js`, `reducedMotion()` legge la preferenza
   dal vivo (può cambiare a pagina aperta) e la bandiera di revisione `html.rm`; nessun altro modulo di
   `static/js/src/` interroga la media query né chiama `element.animate()` o `requestAnimationFrame`: passano da
   `play()`, `nextFrame()`, `afterPaint()` e `tween()`, che chiedono prima al cancello e, sotto il moto ridotto, non
   creano nulla, non attendono nulla e lasciano lo stato finale. Nessuno script attende `transitionend` o
   `animationend` — una transizione da 0 s non emette l'evento, e l'attesa resterebbe appesa proprio sotto il moto
   ridotto: `settled()` attende le animazioni davvero in corso, con un timeout. `static/js/main.js` (V1) legge ancora
   la media query per `.reveal` e per i contatori, finché W4-B non li ritira.
4. **La tastiera non anima** (R-07, livello 0). `static/js/head.js` scrive `html[data-input]`: `key` dopo un tasto di
   navigazione (Tab, frecce, Home / End, Pagina su / giù, Invio, Spazio, Esc, i tasti del menu contestuale,
   Ctrl / ⌘ K), `pointer` dopo una pressione o un movimento del mouse; assente fino al primo input, mai toccato dalla
   digitazione di testo. Ogni famiglia aggiunge la propria regola `html[data-input="key"] <selettore>
   { transition-duration: 0ms; }` per i cambi di stato chiesti da tastiera.

**La bandiera non è la prova.** `html.rm` dichiara esattamente l'elenco del blocco media (quando i due divergono il
test stampa il blocco da incollare) e serve a chi rivede senza poter cambiare la preferenza; le prove di moto ridotto
si prendono con la preferenza emulata (Playwright `reduced_motion="reduce"`), mai con la sola bandiera.

Misurato (corsia 7, Chromium headless, preferenza emulata, 5 ottobre 2026): 138 caricamenti — pagine pubbliche,
account e console; fr e ar; 1440 × 900 e 390 × 844 — con 0 animazioni in corso a riposo e 0 elementi, pseudo-elementi
compresi, con una transizione o un'animazione più lunga di 0 s; sotto `html.rm` la radice riceve gli stessi token.
Rimisurato il 9 ottobre 2026 dopo l'arrivo del portico (20 caricamenti, stesse pagine e misure): 0 animazioni in corso,
0 elementi in movimento; le pagine con la cromatura pubblica portano 9 elementi — i cinque pannelli del portico e le
loro quattro fotografie — con la sola dissolvenza che MS-O4 concede (`opacity` per `--motion-reduced`, 80 ms, con la
compagna discreta `display`), la console nessuno: è l'unica durata che il controllo ammette, ogni altra lo fa fallire.
Senza la preferenza le stesse pagine portano transizioni (il controllo legge qualcosa). Screenshot
`docs/qa/design/a11y-reduced-motion-fr-1440.png`. Inventario dei token in `docs/design/DESIGN_SYSTEM_2026.md` §12. Non
esistono animazioni in loop, parallax o autoplay da mettere in pausa.

Test: `tests/frontend/test_v5_tokens.py::test_reduced_motion_is_a_state_every_duration_lands_at_zero`,
`tests/frontend/test_v5_tokens.py::test_no_sheet_forces_a_duration_and_motion_reduced_only_fades`,
`tests/frontend/test_rm_flag_parity.py::test_under_the_flag_every_custom_property_resolves_as_under_the_setting`,
`tests/frontend/test_rm_flag_parity.py::test_the_twin_is_the_media_block_and_nothing_else`,
`tests/frontend/test_script_motion_gate.py::test_no_animate_or_frame_loop_outside_the_gate`,
`tests/frontend/test_script_motion_gate.py::test_no_script_waits_on_a_transition_or_animation_event`,
`tests/frontend/test_design_docs.py::test_focus_and_motion_claims_match_the_stylesheets` e, in Chromium,
`tests/frontend/test_reduced_motion_w1_d.py` (`test_under_the_setting_nothing_moves_at_rest`,
`test_head_js_writes_the_input_modality`).

**Il loader «Lume» (8 ottobre 2026, W1-D; piano V5.4 §1.9).** Ogni livello ha il suo fermo, che è anche lo stato senza
JavaScript: il marchio verbatim, la chiave occupata ferma e attenuata, le righe al loro posto. **1.4.11**: la chiave è
l'unico indizio visivo dello stato occupato, quindi deve leggere 3 : 1 sul suo fondo — è all'80 % dell'inchiostro del
bottone: misurata sui pixel di un'attivazione vera (puntatore, tastiera, tocco; francese e arabo; 1440 e 390), 4,0 : 1
sul teal che ogni bottone occupato ha oggi (al 55 % leggeva 2,7 : 1) e 3,6 : 1 al suo pixel più debole; sull'inchiostro
e sul fondo propri di ogni variante non scende sotto 3,9 : 1. Sta al centro del padding di fine riga, mai contro
l'ultima lettera dell'etichetta (su un bottone piccolo ne distava 1,2 px, 0,3 in arabo: ora 5 e 3). Sotto
`prefers-reduced-motion: reduce` i token che il loader usa (`--motion-slow`, `--motion-emphasized`, `--motion-standard`,
`--motion-stagger`, `--motion-fast`, `--motion-door`) valgono 0 ms e `fill-mode: both` posa ogni strato sul fermo: il
rilascio della prima pagina della console mostra lo stato finale senza tragitto. **2.2.2**: nulla gira in loop e nulla si
muove per più di 1,6 s di seguito; **2.3.1**: la luce è un solo cambiamento, dentro la porta, una volta; **4.1.3**: lo
stato è nell'`aria-busy` del controllo e nelle parole di una riga `role="status"` (a 1 s, a 10 s con «Réessayer»), mai
nell'immagine, che è `aria-hidden` — e **nessuno stato annunciato dura per sempre**: un form la cui risposta è un file
porta `data-loader="none"` e non aspetta affatto (l'esportazione dei dati del conto teneva `aria-busy` e
`aria-disabled` finché la pagina non veniva ricaricata); una risposta che non sostituisce la pagina — un 204, un file
non dichiarato, una navigazione interrotta — lascia il controllo in attesa 10 s al massimo, più il tempo dei file che
il form porta, poi il form torna a riposo da solo e si può inviare di nuovo; una risposta data in pagina lo riposa nel
task seguente; una pagina che torna dalla cache è a riposo; un controllo d'invio che non è un `.btn` (l'uscita del
menu del conto) non dichiara alcuno stato; **focus**: un bottone occupato è `aria-disabled`, mai `disabled` — il focus
resta dove la persona l'ha lasciato, anche quando l'attesa finisce — e solo dove lo script rifiuta davvero il secondo
invio (`data-single-submit`): altrove dice soltanto `aria-busy`; «Réessayer» riporta il fuoco sul controllo d'invio
prima di nascondersi; **1.4.3 / 1.4.11, dove la chiave non ha posto**: un bottone-link o un bottone-icona non ha
padding, e la chiave era disegnata sopra le ultime lettere dell'etichetta (misurato su «Marquer comme lue»; «Supprimer»
nella tabella dei documenti, un `.btn--text`, è lo stesso caso) — quelle varianti aspettano con `aria-busy` e restano
come sono, senza chiave e senza la lastra di V4; **colori forzati**: il marchio tiene i suoi colori (`forced-color-adjust: none`, come l'`<img>` che
sostituisce), niente luce né inchiostro (lo strato d'inchiostro è nascosto da un selettore che vince sulla regola
degli strati), la chiave occupata in `ButtonText` all'80 % su `ButtonFace` (12,6 : 1). Test:
`tests/frontend/test_loader_rules.py` e `tests/frontend/test_loader_w1_d.py` (il rilascio una volta e il fermo sotto la
preferenza emulata; la chiave occupata nel task del clic, il focus che resta, nessuno spostamento dell'etichetta; la
chiave al centro del padding su ogni taglia, fr e ar, e 3 : 1 sui pixel; l'attesa che nessuna pagina chiude — la
risposta in pagina, il 204 e il file non dichiarato fino alla scadenza, il ritorno dalla cache; il form
dell'esportazione che non aspetta e non carica il modulo; «Marquer comme lue» in attesa senza chiave, fr e ar; niente
stanza né inchiostro sotto colori forzati). La cache del «indietro» vera è stata provata sulla corsia con un Chromium
completo (`docs/design-v5/QA/v54/w1-d/NOTES.md`): il test spedisce l'evento che la cache manda.
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
| Il foglio del menu (sotto 80rem; W2-C2) | le porte 64 px (`--drawer-row-h`); Forum e Projet 52 px; le voci 48 px; «Voir l'espace», le lingue col puntatore grosso, la ricerca, l'anti-frode e «Fermer» 44 px; nessun bersaglio sotto 44 px col puntatore grosso (`tests/frontend/test_browser_w2_c2.py::test_every_target_of_the_sheet_holds_44_px_under_a_finger`) |
| `summary` degli accordion | ≥ 56 px |
| Le quattro lingue nella barra istituzionale (design V5) | 24 px col puntatore fine, 44 col puntatore grosso (piano V5.4 §1.11) |
| «La targa» (Espace réservé) e il menu account nella testata | 32 px (44 col puntatore grosso); sotto 100rem la sola chiave — e, autenticati, il solo glifo della persona — 32 × 32 (44 × 44 col puntatore grosso); nel piede del foglio, su notte, 44 px a tutta larghezza |
| Le porte del portico | alte quanto la testata (64 px, 56 scrollata); voci del pannello 48 px; «Voir l'espace» 44 px; link del piede 24 px |
| Bottoni `--sm` | 36 px |
| Checkbox e radio | 24 × 24 px (`.form-field input[type="checkbox"]`, `1.5rem`; erano 20 × 20 alla prima stesura) **più** l'etichetta cliccabile a fianco |

Misura in Chromium a 390 px (`/fr/`, login, 404), ripetuta alla seconda revisione: gli unici bersagli sotto
24 px in una dimensione sono link di testo — link del footer (alti 19 px, passo verticale 27 px: i cerchi da
24 px non si intersecano → eccezione «spacing»), link in frase («enregistrer», e-mail di aiuto → eccezione
«inline»), link di recupero del 404 (alti 20 px) e le CTA dei quattro accessi (`.entrance__cta`: la riga di
testo è alta 22 px, ma il bersaglio reale è l'intera colonna, coperta dallo pseudo-elemento dello stretched
link). Il wordmark misura 186 × 44 px da quando `.brand` ha `min-block-size: var(--control-height)` (alla
prima stesura era 186 × 22); sotto 80rem «Espace réservé» è anche nel piede del foglio (da 48rem in quello laterale, sopra la targa della testata), un bersaglio a tutta larghezza alto 44 px (design V5, W2-C1, W2-C2).
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
- le frecce della tastiera seguono la direzione visiva (← e → invertite in `nav.js` per il portico e in `main.js`
  per le tab; `tests/i18n/test_rtl_browser_nav.py::test_the_arrows_follow_the_eye`);
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
| `main.js`: modulo senza dipendenze, reduced motion; nessun dialog né ripiego dei `<details>` — sono di `overlay.js`, che ogni pagina carica | `tests/frontend/test_static_assets.py::test_main_js_is_an_es_module_without_external_dependencies`, `tests/frontend/test_overlays.py::test_main_js_keeps_no_dialog_and_a_dropdown_fallback_that_steps_aside` |
| Nessun overflow orizzontale a 360 / 768 / 1440 in fr e ar; `.reveal` mai nascosto | `tests/frontend/test_browser.py::test_no_horizontal_overflow_and_screenshots` |
| «Il portico» da tastiera (Invio, ↓, Esc, ←/→, Home/Fine, ritorno del focus, chiusura alla perdita di focus), intenzione del puntatore e fissaggio, triangolo sicuro, fotografie (0 prima di `load`, 4 a idle da 80rem, 0 sul telefono), senza script, 2.4.11 | `tests/frontend/test_browser.py::test_mega_menu_is_keyboard_operable`, `tests/frontend/test_browser_w2_c1.py::test_the_keyboard_model_of_the_portico`, `tests/frontend/test_browser_w2_c1.py::test_hover_intent_and_the_pin`, `tests/frontend/test_browser_w2_c1.py::test_the_safe_triangle_holds_for_doors_two_to_four`, `tests/frontend/test_browser_w2_c1.py::test_the_photographs_follow_the_loading_policy`, `tests/frontend/test_browser_w2_c1.py::test_without_script_a_door_opens_on_hover_and_the_sheet_opens_in_place`, `tests/frontend/test_browser_w2_c1.py::test_focus_is_not_obscured_by_the_sticky_letterhead` |
| L'architrave sotto la porta aperta, le voci allineate alla prima porta e il pannello piano al bordo di chiusura, in arabo come in francese; le frecce seguono l'occhio | `tests/i18n/test_rtl_browser_nav.py::test_the_architrave_and_the_entries_follow_the_doors_in_both_directions`, `tests/i18n/test_rtl_browser_nav.py::test_the_arrows_follow_the_eye` |
| Drawer (apertura, Esc, `aria-expanded`) e selettore lingua | `tests/frontend/test_browser.py::test_mobile_drawer_and_language_switcher` |
| Il foglio del menu (W2-C2): la trappola, Esc e il fuoco di ritorno, la pagina dietro fuori dall'albero, la testa sulla riga della barra, i bersagli di 44 px e l'anello di «Italiano», le porte una per volta, l'uscita dal bordo d'entrata, il movimento ridotto, la fascia da 64rem; il popover della targa (bordo di chiusura, fuoco, frecce, Esc, fuoco che esce); nessuna fotografia sul telefono né con Save-Data; in arabo, da sinistra e senza viaggio laterale sul telefono | `tests/frontend/test_browser_w2_c2.py::test_the_sheet_opens_and_closes_on_the_overlay_system`, `tests/frontend/test_browser_w2_c2.py::test_every_target_of_the_sheet_holds_44_px_under_a_finger`, `tests/frontend/test_browser_w2_c2.py::test_the_side_sheet_slides_in_and_out_by_the_inline_end`, `tests/frontend/test_browser_w2_c2.py::test_reduced_motion_is_one_short_opacity_and_no_transform`, `tests/frontend/test_browser_w2_c2.py::test_signed_in_the_targa_opens_the_account_popover`, `tests/frontend/test_browser_w2_c2.py::test_no_photograph_on_a_phone_nor_with_save_data`, `tests/i18n/test_rtl_browser_w2_c2.py::test_in_arabic_the_side_sheet_comes_and_goes_by_the_left` |
| Font self-hosted effettivamente caricati, zero richieste esterne | `tests/frontend/test_browser.py::test_fonts_are_self_hosted_and_loaded` |
| Arabo RTL, altre lingue LTR | `tests/compliance/test_public_pages.py::test_arabic_is_rtl_and_others_ltr` |
| Fallback francese dei testi prescritti | `tests/compliance/test_locked_content.py::test_fallback_to_french_for_other_languages` |
| Questo documento e `docs/design/DESIGN_SYSTEM_2026.md` restano veritieri | `tests/frontend/test_design_docs.py::test_wcag_checklist_lists_every_a_and_aa_criterion`, `tests/frontend/test_design_docs.py::test_cited_tests_exist`, `tests/frontend/test_design_docs.py::test_form_field_contract_matches_accessibility_doc` |
| Fogli di stile delle app: solo token reali, nessun colore letterale, nessun gradiente (anello di focus e contrasti restano quelli del sistema) | `tests/frontend/test_design_docs.py::test_conforming_app_stylesheets_use_only_design_tokens` |
| Regressione dei difetti chiusi: sprite XML ben formato (G-01), nessun `backdrop-filter` sull'header che contiene il drawer (G-02), ogni SVG sotto `static/` ben formato | `tests/frontend/test_design_docs.py::test_icon_sprite_is_well_formed_xml`, `tests/frontend/test_design_docs.py::test_sticky_header_does_not_trap_fixed_drawer`, `tests/frontend/test_svg_wellformed.py::test_svg_is_wellformed_xml` |
| Difetto aperto tenuto in vista (xfail finché non corretto: G-22) | `tests/frontend/test_design_docs.py::test_stage1_app_stylesheets_use_only_design_tokens` |
| Breakpoint della navigazione identico in CSS, JS e documenti; stato delle lacune coerente tra i due documenti, i marcatori xfail e il report delle catture | `tests/frontend/test_design_docs.py::test_navigation_breakpoint_is_consistent_and_documented`, `tests/frontend/test_design_docs.py::test_gap_status_and_xfail_markers_stay_in_lockstep`, `tests/frontend/test_design_docs.py::test_capture_report_is_current_and_backs_the_documented_figures` |

Limite dei test browser: `test_mobile_drawer_and_language_switcher` controlla `is_visible()`, che era vero anche per
un drawer alto 65 px (per questo la suite non aveva intercettato G-02). Dal design V5 (W2-C1) un test browser gira
senza JavaScript (`test_without_script_a_door_opens_on_hover_and_the_sheet_opens_in_place`: G-04) e uno misura
2.4.11 sotto la testata sticky; la geometria del drawer e il rendering delle icone restano misurati da
`docs/qa/design/capture.py`, che va eseguito a mano. In QA va aggiunta a `tests/frontend/test_browser.py`
un'asserzione sul rendering delle icone (`getBBox()` non nullo).

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
4. A 390 px e a 1024 px (il foglio vale sotto 80rem): Invio su «Menu» → focus su «Fermer»; il foglio copre lo schermo fino in fondo (a 1024 px il
   suo lato, dal bordo di chiusura); Tab fino all'ultimo link → torna in testa al foglio; Esc → chiuso, focus su «Menu».
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
| G-02 | chiusa il 20/09/2026 (era bloccante) | 2.4.3, 2.4.7, 2.1.1 | `.site-header` aveva `backdrop-filter`, che lo rendeva containing block dei discendenti `position: fixed`: `#nav-drawer` misurava 65 px di altezza (atteso 732 px a 390 × 844) e `.nav-overlay` 0 px; si vedeva solo la prima voce del menu. Con il breakpoint della navigazione a 80rem il difetto toccava anche tablet e laptop fino a 1279 px. **Chiusa**: l'owner ha spostato il velo su `.site-header::before`; misurato alla seconda revisione: drawer alto 731 px su 731 px disponibili a 390 × 844 e 655 px su 655 px a 1024 × 768, overlay a tutto schermo; rimisurato col foglio del sistema di overlay (W2-C2, 11/10/2026, `capture-report.json`): alto 844 px su 844 px disponibili a 390 × 844 e 768 px su 768 px a 1024 × 768 (il foglio laterale), velo a tutto schermo e la testa del foglio sopra di lui (G-23); il foglio sta fuori dall'header | `static/css/components.css` §7 | fatto dall'owner | `test_sticky_header_does_not_trap_fixed_drawer` passa come test di regressione (non è più xfail); `test_capture_report_is_current_and_backs_the_documented_figures` pretende nel report un drawer alto quanto lo spazio disponibile; resta da aggiungere l'asserzione Playwright alla suite browser |
| G-03 | alta (RTL) | 1.3.2 | In arabo le stringhe d'identità latine non isolate vengono riordinate: footer «™Italy Legal Entry», riga «AGAMI … 2026 ©», punto finale spostato; nella barra il nome del promotore è troncato dall'inizio («…iuridico Interculturale APS») | `static/css/base.css` (helper bidi), `apps/cms/templatetags/cms_nav.py`, `templates/partials/footer.html`, `templates/partials/utility_bar.html` | `dir="ltr"` nel tag `{% brand %}`; `<bdi>` o classe `.ltr` su promotore e riga del © | confronto degli screenshot `ar`; lettura con screen reader arabo |
| G-04 | chiusa l'08/10/2026 (era alta) | 2.4.11, 2.4.7 | Senza JS, sotto 80rem, il menu era reso in flusso dentro un header `position: sticky` alto 781 px: a 390 × 844 restavano 63 px di pagina, a 1024 × 768 nessuno. **Chiusa** dalla cromatura V5 (W2-C1: l'header non sticky senza JS) e poi dal foglio (W2-C2): senza JS la testata contiene solo la sua riga — 57 px a 390 × 844 — e il menu è un foglio che si mostra sul posto (`:target`), a richiesta; misurato in Chromium con `java_script_enabled=False` | `static/css/v5/chrome.css` §7 | fatto (W2-C1, W2-C2) | `tests/frontend/test_browser_w2_c1.py::test_without_script_a_door_opens_on_hover_and_the_sheet_opens_in_place`; il report delle catture registra la testata alta quanto la sua riga |
| G-05 | chiusa il 20/09/2026 (era alta) | 3.3.1, 4.1.3 | `#form-errors` aveva `tabindex="-1"` ma nessuno script vi portava il focus dopo il ricaricamento: l'utente di screen reader ripartiva dall'inizio della pagina. **Chiusa**: l'owner ha aggiunto `initFormErrorFocus` a `static/js/main.js`; misurato alla seconda revisione: dopo un invio non valido del login `document.activeElement.id === "form-errors"` (campo `focus` del report delle catture) | `static/js/main.js` | fatto dall'owner | `test_capture_report_is_current_and_backs_the_documented_figures` pretende nel report il focus sul riepilogo; resta da aggiungere l'asserzione Playwright alla suite browser |
| G-06 | alta | 1.3.1, 4.1.2 | Nel form di iscrizione al Forum `aria-describedby="id_forum_email_errors"` non corrisponde ad alcun elemento (il componente rende `id="id_email_error"`): l'errore non è collegato al campo | `apps/forum/forms.py` (`is_valid`) | eliminare l'impostazione manuale di `aria-invalid` / `aria-describedby`: Django 5.2 li genera già con gli id usati dal componente | test: ogni id in `aria-describedby` esiste nella pagina; regola axe `aria-valid-attr-value` |
| G-07 | media | 4.1.3 | Le regioni `role="status"` sono già popolate al caricamento: dopo un redirect molti screen reader non annunciano il messaggio | `templates/base.html`, `static/js/main.js` | portare il focus sul messaggio, oppure reinserirne il testo dopo il caricamento | prova con NVDA e VoiceOver |
| G-08 | media (era alta) | 3.1.2 | Alla prima stesura non esisteva alcun catalogo `.po` e tutte le stringhe UI comparivano in francese, senza `lang`, nelle pagine `it` / `en` / `ar`. **Alla revisione i cataloghi `locale/{fr,it,en,ar}/LC_MESSAGES/django.po` esistono** (Stage 2, non ancora committati) e skip link, landmark, menu e footer risultano tradotti. Alla revisione ogni catalogo conta 1 792 voci, nessuna senza `msgstr`. Restano: «Privacy Policy» e «Cookie Policy», letterali inglesi senza `lang="en"`; il rischio che una stringa aggiunta senza aggiornare i cataloghi ricada sul francese senza `lang`; la rilettura da parte di madrelingua (i testi prescritti e legali restano fuori dai cataloghi e non si traducono mai automaticamente) | `templates/partials/footer.html`, `locale/` | `lang="en"` sui due titoli; tenere i cataloghi allineati a ogni nuova stringa; revisione linguistica IT / EN / AR | `scripts/i18n_audit.py` senza msgid non tradotti; controllo a campione con screen reader |
| G-09 | chiusa il 21/09/2026 (era bassa) | 1.4.3 | Le numerazioni decorative erano in `--color-accent-600` (bronzo, 3.83:1 sul fondo): `.entrance__num`, `.pathway-list__num`, `.numeral`. Erano `aria-hidden` e ridondanti rispetto a `<ol>`, ma piccole e sotto la soglia del testo. **Chiusa dalla redirezione**: il bronzo non esiste più, gli ordinali sono in `--rubric` e misurano 6.92:1 sulla carta e 6.23:1 sul fondo di processo, quindi sono sicuri anche se letti come testo | `static/css/tokens.css` | fatto: la coppia è bloccata da `test_wcag_contrast` | la riga «rubrica sulla carta» della tabella di `docs/design/DESIGN_SYSTEM_2026.md` §5, ricalcolata dal test |
| G-10 | bassa | 2.5.8 | «Mot de passe oublié ?» è alto 17 px e sta a circa 2 px dal campo password: il cerchio da 24 px interseca il campo | `templates/allauth/elements/field.html`, `static/css/components.css` (`.form-field__help a`) | `display: inline-block; padding-block: var(--space-1)` sui link nell'aiuto | misura dei bersagli in QA |
| G-11 | chiusa l'11/10/2026 (era media) | 2.4.3 | Il drawer non rendeva inerte il resto della pagina: il cursore virtuale poteva uscire dal menu aperto. **Chiusa** dal foglio (W2-C2), un drawer modale del sistema di overlay: a foglio aperto ogni elemento accanto al suo cammino fino al `body` è `aria-hidden`, `aria-modal`, la pressione e il fuoco restano dentro (la trappola di `overlay.js`, mai `inert`: la regola INP del piano) | `templates/partials/main_nav.html` («sheet»), `static/js/src/overlay.js` | fatto (W2-C2) | `tests/frontend/test_browser_w2_c2.py::test_the_sheet_opens_and_closes_on_the_overlay_system` (`main` fuori dall'albero, Tab che non esce); resta la prova con screen reader mobile |
| G-12 | bassa | 1.4.13 | Senza JS i pannelli del portico appaiono su `:hover` / `:focus-within` e non si possono chiudere con Esc (con JS: apertura dopo 120 ms di intenzione, pannello sorvolabile, Esc, grazia di 250 ms — conforme) | `static/css/v5/chrome.css` §5 | accettare (solo modalità senza JS) oppure mostrare i pannelli solo su `:focus-within` | decisione di QA |
| G-13 | bassa | 4.1.2 | `cta_panel.html` ricava l'`id` da `title` passato al filtro `slugify` (vuoto per titoli non latini, duplicato per titoli uguali); `hero.html` usa l'`id` fisso `hero-title` | `templates/components/cta_panel.html`, `templates/components/hero.html` | parametro `id` opzionale | validatore HTML: nessun id duplicato |
| G-14 | bassa | 3.1.2 | `.meta-row__item dt::after { content: " :" }` — punteggiatura francese generata in CSS, non tradotta | `static/css/v5/card.css` | separatore nel template, dentro `{% translate %}` | revisione linguistica |
| G-15 | chiusa il 21/09/2026 (era bassa) | — | `--font-mono` nominava IBM Plex Mono, che non era self-hosted: il registro tecnico era Consolas su Windows e Menlo su macOS, tre texture per un ruolo. **Chiusa dalla redirezione**: il ruolo era `--font-ref` (Fira Mono), i cui due file woff2 erano self-hosted; dal 5 ottobre 2026 (design V5, W1-A) è «ILE Mono», due file self-hosted (divisi per `unicode-range`) dichiarati in `static/css/v5/fonts.css`, e `static/css/v5/aliases.css` ripunta `--font-ref` e `--font-mono` su `--f-mono` | `static/css/tokens.css` | fatto | `tests/frontend/test_layout.py::test_fonts_css_references_only_local_files_that_exist` e la tabella dei file di `docs/design/DESIGN_SYSTEM_2026.md` §6.2 |
| G-16 | chiusa il 20/09/2026 (era bassa) | — | `docs/I18N_RTL.md` era citato nei commenti dei CSS e nell'intestazione dei cataloghi `locale/` ma non esisteva. **Chiusa**: il documento è stato scritto | `docs/` | fatto | il file esiste; `tests/frontend/test_design_docs.py::test_cited_paths_exist` non ha più eccezioni |
| G-17 | media | 2.2.1 | Un form pubblico compilato in più di 6 ore è trattato come spam e scartato in silenzio | `apps/core/forms.py` (`MAX_FILL_SECONDS`) | portare il limite oltre 20 ore o mostrare un messaggio che invita a reinviare | revisione con il responsabile sicurezza |
| G-18 | alta (processo) | tutti | axe-core non è ancora stato eseguito; nessun test con screen reader reali | `tests/` (Stage 3) | suite `a11y` con axe iniettato da Playwright su tutte le route pubbliche × 4 lingue | zero violazioni «serious» / «critical» |
| G-19 | chiusa il 09/10/2026 (era bassa) | — | Le FAQ usano `.accordion__panel`, che il design system non definiva (il componente usa `.accordion__body`): il corpo della risposta non riceveva padding né misura. **Chiusa** (W1-C): `static/css/v5/tabs.css` definisce `.accordion__panel` come `.accordion__body` | `static/css/v5/tabs.css` | fatto: misura di lettura, rientro della riga, 24 px prima del filetto | revisione visuale |
| G-20 | bassa | — | `.reveal--stagger` non produce scaglionamento visibile e ritarda l'hover dei figli fino a 480 ms | `static/css/components.css` §29 | animare i figli o rimuovere il modificatore | revisione visuale |
| G-21 | chiusa il 09/10/2026 (era bassa) | — | L'opzione `remember` delle tab scriveva in `localStorage` ma non rileggeva il valore. **Chiusa** (W1-C): l'opzione è tolta da `templates/components/tabs.html` e da `initTabs` | `static/js/main.js` (`initTabs`) | fatto: nessuna scrittura in `localStorage` da `main.js` | test Playwright |
| G-22 | media — chiusa | 2.4.7, 1.4.11 | Due fogli di stile dello Stage 1 non usano il design system: richiamano token che non esistono (`var(--color-focus, #d97706)`, `var(--color-primary, #0f2b52)`…), quindi valgono sempre i ripieghi scritti a mano. Effetti sull'accessibilità: nelle pagine del Forum e del wizard di orientamento l'anello di focus non è quello a due toni del sistema ma un contorno da 3 px oro `#b8893a` (3.01:1 sul fondo) o arancio `#d97706` (3.05:1), appena sopra la soglia di 3:1 e diverso dal resto del sito; colori e scala tipografica non seguono i token e non sono coperti da `test_wcag_contrast` | `apps/forum/static/forum/forum.css`, `apps/orientation/static/orientation/wizard.css` | riscrivere i due fogli sui token reali e lasciare il focus a `static/css/base.css`; dettagli in `docs/design/DESIGN_SYSTEM_2026.md` §2.1 | test: nessun `var(--…)` verso token inesistenti nei fogli delle app; axe `color-contrast`; percorso da tastiera su Forum e wizard  **Chiusa il 20 settembre 2026**: i due fogli usano solo token reali, senza gradiente né ombre o anelli di focus propri; `test_stage1_app_stylesheets_use_only_design_tokens` e `tests/frontend/test_css_tokens_exist.py` lo verificano. |
| G-23 | chiusa l'08/10/2026 (era media) | 1.4.3, 1.4.11 | A drawer aperto e pagina non scrollata `.nav-overlay` partiva da 72 px mentre l'header finiva a 113 px: il velo copriva wordmark e bottone «Menu» (etichetta a 3.92:1), perché `main.js` scriveva `--nav-drawer-top` sul solo drawer. **Chiusa** (W2-C1): velo e cassetto partivano dal piede reale dell'header (57 px a 390 × 844, 97 px a 1024 × 768). Dal foglio (W2-C2) il menu possiede la sua riga di testa, «Fermer» dov'era «Menu»: lo scrim è quello del modale e nessun velo copre l'uscita | `static/css/v5/chrome.css` §7, `templates/partials/main_nav.html` («sheet») | fatto (W2-C1, W2-C2) | nel report delle catture il foglio parte da 0 (`top`) e copre la testata; `tests/frontend/test_design_docs.py::test_capture_report_is_current_and_backs_the_documented_figures` |
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
