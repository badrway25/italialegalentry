# DESIGN SYSTEM — Italy Legal Entry™

> **RITIRATO il 21 settembre 2026, sostituito da `docs/design/DESIGN_SYSTEM_2026.md`** (direzione artistica A, «Le Registre»): questo documento descrive il sistema a due inchiostri più bronzo su IBM Plex, che non esiste più; non è più tenuto allineato da test e va letto solo come storia.

Documentazione **di ciò che esiste nel codice**, non di ciò che si vorrebbe: ogni valore, contratto e
comportamento qui descritto è stato letto dai file sorgente e verificato in Chromium (Playwright) il
20 settembre 2026. Il codice resta la fonte di verità; questo documento è tenuto allineato da test.

| Campo | Valore |
|---|---|
| Data di riferimento | 20 settembre 2026 (Stage 1 committato; verifica visuale su `http://127.0.0.1:8793`, solo locale) |
| Revisione indipendente | 20 settembre 2026, sull'albero di lavoro dello Stage 2: le app `pages`, `ecosystem`, `portal` e i cataloghi `locale/` sono presenti ma non ancora committati. «Usato in», esempi reali, screenshot, §2.1 e le lacune G-08 / G-22 descrivono quell'albero; ogni misura è stata ripetuta in Chromium |
| Sorgenti documentate | `static/css/{main,fonts,tokens,base,layout,components}.css`, `static/js/{head,main}.js`, `static/img/icons.svg`, `static/img/illustrations/*`, `static/fonts/*`, `templates/base.html`, `templates/partials/*`, `templates/components/*`, `templates/errors/*`, `templates/allauth/**` |
| Seconda revisione indipendente | 20 settembre 2026, pomeriggio, mentre la QA in browser correggeva i file condivisi: G-01, G-02 e G-05 risultano **chiusi** dagli owner (verificato in Chromium); il breakpoint della navigazione è passato da 64rem a **80rem** (§6.2, §8); G-04 è stato rimisurato ed è più grave di quanto scritto alla prima stesura (§16). Catture e report rigenerati dopo quelle modifiche |
| Requisiti coperti | R-DES-001 … R-DES-009, R-ARC-007, R-ARC-011, R-P3-015, R-P3-017, R-I18N-002, R-A11Y-002 (`docs/REQUIREMENTS_MATRIX.md`) |
| Documento gemello | `docs/ACCESSIBILITY.md` (WCAG 2.2 AA, modello tastiera, lacune note **G-01 … G-23**) |
| Decisioni collegate | ADR-008 (tipografia IBM Plex), ADR-009 (server-rendered + progressive enhancement) |
| Test di veridicità | `tests/frontend/test_design_docs.py` — token e valori, famiglie, componenti, icone, tabella contrasti (± 0.05), font, moduli JS, breakpoint, keyframe, percorsi citati, inventario e conformità dei fogli delle app (§2.1) |
| Screenshot | `docs/qa/design/` — rigenerabili con `docs/qa/design/capture.py` (i PNG sono git-ignorati: `docs/qa/**/*.png`) |

> **Stato reale alla data di riferimento.** La prima verifica in browser aveva rilevato due difetti
> bloccanti nel design system committato: lo sprite delle icone non era XML ben formato (**G-01**: nessuna
> icona disegnata) e il drawer era schiacciato a 65 px dal `backdrop-filter` dell'header (**G-02**). Gli
> owner li hanno corretti il 20/09/2026 e la chiusura è stata verificata in Chromium (§10, §8.2, §16).
> Il difetto più grave ancora aperto è **G-04**: senza JavaScript, sotto 80rem, l'header sticky contiene
> l'intero menu (781 px) e copre il contenuto della pagina. I difetti aperti sono descritti in §16 e in
> `docs/ACCESSIBILITY.md` §13; i file coinvolti non appartengono a questo incarico e la correzione è
> richiesta ai rispettivi owner. Tutto il resto del documento descrive il comportamento *previsto e
> implementato*; dove la verifica lo contraddice, è scritto.

## Indice

1. Principi e anti-pattern · 2. Architettura CSS · 3. Token · 4. Contrasto WCAG misurato ·
5. Tipografia · 6. Layout · 7. Catalogo componenti · 8. Navigazione · 9. Motion · 10. Iconografia ·
11. Illustrazioni e fotografia · 12. RTL · 13. Moduli JS e progressive enhancement ·
14. Come estendere il sistema · 15. Screenshot QA · 16. Difetti noti

---

## 1. Principi e anti-pattern

### 1.1 Principi

1. **Istituzionale, non ministeriale.** Italy Legal Entry™ è un ecosistema di informazione e orientamento
   promosso da un'associazione (AGAMI), non un'autorità: nessuno stemma, nessun emblema, nessuna estetica
   che imiti gov.it o la Commissione (R-MP-002). L'identità è tipografica: wordmark in IBM Plex Serif,
   barra istituzionale blu profondo con il nome del promotore, filetto bronzo.
2. **Editoriale, guidato dal testo.** I testi prescritti (`{% locked %}`) sono il contenuto principale; il
   layout li serve con misura di lettura controllata (`--measure-prose: 68ch`), gerarchia serif/sans,
   filetti sottili e molto bianco. La home ammette al massimo quattro «riquadri»: i quattro accessi, che
   non sono nemmeno box ma colonne separate da filetti (R-P3-015, R-ECO-001).
3. **Token prima di tutto.** Nessun colore fuori da `tokens.css`: `base.css`, `layout.css` e
   `components.css` non contengono un solo valore esadecimale (test
   `tests/frontend/test_static_assets.py::test_no_hardcoded_colours_outside_tokens_and_fonts`; unica
   eccezione ammessa: lo chevron `data:` del `<select>`). La regola vale anche per i fogli di stile
   delle app (§2.1): tutti e cinque la rispettano (G-22 chiusa il 20 settembre 2026).
4. **Progressive enhancement reale.** Ogni pagina funziona senza JavaScript: `<details>` per dropdown e
   accordion, pannelli delle tab impilati, menu interamente visibile, dialog raggiungibile via `:target`,
   contenuti `.reveal` mai nascosti (la classe `js` viene messa su `<html>` da `static/js/head.js`).
5. **Accessibilità per costruzione.** Anello di focus a due toni su ogni superficie, controlli da 44 px
   (`--control-height`), contrasti misurati e bloccati da test, `prefers-reduced-motion` che azzera i token
   di durata, semantica nativa prima di ARIA. Dettagli in `docs/ACCESSIBILITY.md`.
6. **RTL nativo.** Solo proprietà logiche (`margin-inline-start`, `inset-inline-end`, `border-block-start`…);
   le regole `[dir="rtl"]` esistono unicamente dove la semantica lo richiede (frecce, traslazioni, chevron
   del `<select>`, isolamento bidi dei dati latini).
7. **Zero terze parti.** Font, icone, immagini e script sono self-hosted; la CSP è `default-src 'self'`
   (niente inline style, niente inline script, niente handler `on*`): per questo lo stato JS è in un file
   esterno e le barre di avanzamento usano `<progress>` invece di un attributo `style`.
8. **Sobrietà del movimento.** Durate 120–600 ms, una sola curva d'uscita, nessuna animazione in loop,
   nessun parallax, nessun autoplay.

### 1.2 Anti-pattern rifiutati

| Anti-pattern | Perché è rifiutato | Dove è impedito nel codice |
|---|---|---|
| Aspetto «template SaaS / ThemeForest» | toglie credibilità istituzionale (R-DES-001) | raggi minimi (`--radius-sm: 3px`; nessun raggio oltre 4 px salvo pill e cerchi), palette a due inchiostri + bronzo, nessuna illustrazione 3D/isometrica |
| «Card soup» (tutto dentro box con ombra) | Impl. §3.7: meno riquadri, più spazio bianco | `.card` dichiarata «sparingly»; liste editoriali (`.pathway-list`, `.entrances`, `.accordion`, `.timeline`) usano filetti, non box; `.card--flat` toglie il box |
| Gradienti gratuiti, neon, colori saturi | estetica commerciale; problemi di contrasto | nessun `gradient(` e nessun colore fuori token in `static/css/`. L'hero del Forum, che usava un `linear-gradient` e colori scritti a mano, è stato riportato a un fondo piatto su token (G-22, chiusa) |
| Glassmorphism | moda decorativa, leggibilità imprevedibile | nessun pannello traslucido. **Eccezioni dichiarate (§1.4)**: velo dell'header sticky e backdrop del dialog |
| Ombre giganti | effetto «floating UI» | quattro ombre soltanto; la più grande (`--shadow-lg`, 40 px di blur al 14 %) è riservata a mega-menu e dialog. `.forum-hero__figure img` usa ora `--shadow-lg` (G-22, chiusa) |
| Motion decorativo, parallax, carousel, autoplay | distrazione, WCAG 2.2.2, Core Web Vitals | nessun carousel nel sistema; reveal one-shot; `prefers-reduced-motion` globale |
| Hero fotografico con cliché migratori | Impl. §3.1: niente porte, frontiere, valigie, file, passaporti, aeroporti, griglie | hero tipografico (`components/hero.html`), illustrazioni line-art originali; test `test_illustrations_avoid_stereotyped_subjects` e `apps/cms/tests/test_media_assets.py` |
| Emoji o librerie di icone miste | incoerenza (R-DES-009) | un solo sprite originale, `{% svg_icon %}` |
| Tricolore come palette | «non bandiera italiana» (R-DES-003) | verde usato solo per gli stati «completato» e per tratti secondari delle illustrazioni; nessun rosso fuori dagli errori |
| Loghi/stemmi di enti | non autorizzati (gate G6) | `test_illustrations_avoid_stereotyped_subjects` vieta file con `veneto`, `rovigo`, `regione`, `comune` in `static/img/` |
| Popup, banner invadenti, cookie wall | nessun cookie non tecnico; il banner istituzionale è una fascia quieta | `components/institutional_banner.html` non è dismissibile e non è un overlay |

### 1.3 Benchmark (R-DES-001, R-A11Y-002)

Designers Italia / Bootstrap Italia, EU Immigration Portal, sito della Commissione e Your Europe sono stati
usati come riferimento di **usabilità** (navigazione prevedibile, breadcrumb, focus evidente, linguaggio
service-oriented, mobile-first), mai di identità: niente Titillium Web, niente header a doppia fascia con
stemma, niente componenti copiati. L'identità propria è data da: coppia IBM Plex Serif/Sans, blu profondo
`#0f2b52`, fondo bianco caldo `#fbfaf7`, accento bronzo `#9a7b2f` usato solo per filetti, numerazioni e
marcatori.

### 1.4 Eccezioni dichiarate

| Dove | Cosa | Motivazione e limite |
|---|---|---|
| `.site-header::before` (`components.css` §7) | `background: color-mix(in srgb, var(--surface-0) 94%, transparent)` + `backdrop-filter: saturate(140%) blur(8px)` | velo quasi opaco (94 %) per l'header sticky: il testo sottostante non è mai leggibile attraverso. Il velo sta su uno pseudo-elemento **di proposito**: un elemento con `backdrop-filter` diventa containing block dei discendenti `position: fixed`, e sull'header stesso schiacciava il drawer dentro i 72 px dell'header (difetto G-02, chiuso). Non riportarlo sull'elemento: `test_sticky_header_does_not_trap_fixed_drawer` lo impedisce. |
| `.dialog::backdrop` (`components.css` §21) | `background: var(--surface-overlay)` + `backdrop-filter: blur(2px)` | attenua la pagina dietro il modale; nessun contenuto è posto sopra il blur. |

---

## 2. Architettura CSS

`static/css/main.css` è l'unico foglio **applicato** da `templates/base.html` (`rel="stylesheet"`); i cinque
layer che importa sono anche dichiarati con `<link rel="preload" as="style">`, per non scoprirli in catena
solo dopo aver letto `main.css` (ritardo di rendering dell'LCP). `main.css` importa i layer in ordine di
cascata (`ManifestStaticFilesStorage` riscrive gli `@import` con i nomi con hash a `collectstatic`):

| Ordine | File | Peso (non compresso, indicativo) | Contenuto |
|---|---|---|---|
| 1 | `fonts.css` | 12.9 KB | 25 regole `@font-face` generate da `scripts/fetch_fonts.py` (non modificare a mano) |
| 2 | `tokens.css` | 9.1 KB | 162 custom property su `:root`, override `:lang(ar)`, override `prefers-reduced-motion` |
| 3 | `base.css` | 11.4 KB | reset, tipografia di base, link, focus, skip link, `.visually-hidden`, honeypot, `.prose`, helper bidi, stampa |
| 4 | `layout.css` | 5.6 KB | container, sezioni, griglia editoriale, layout a due colonne, utility di composizione |
| 5 | `components.css` | ≈ 70 KB | 29 sezioni numerate: controlli → feedback → shell di navigazione → pattern di contenuto → form → overlay → motion |

Convenzioni:

- **BEM-like**: `.block`, `.block__element`, `.block--modifier` (es. `.main-nav__sublink`, `.hero--inverse`).
  Stati tramite attributi, non classi: `[aria-current]`, `[aria-expanded="true"]`, `[aria-selected="true"]`,
  `[open]`, `[data-open="true"]`, `body[data-nav-open="true"]`. Uniche classi di stato: `.is-visible`
  (reveal) e `.is-active` (tag `{% active %}`).
- **Custom property di componente** (non sono token globali): `--btn-bg`, `--btn-fg`, `--btn-border`,
  `--btn-bg-hover`, `--btn-fg-hover` (varianti dei bottoni), `--notice-fg`, `--notice-bg`,
  `--notice-border` (varianti di notice/alert), `--timeline-line`, `--stack-gap` (utility `.stack`),
  `--reveal-index` (impostata da `main.js` per lo stagger), `--nav-drawer-top` (impostata da `main.js`
  all'apertura del drawer: bordo inferiore reale dell'header, 72 px quando è agganciato in alto, 112 px
  quando la barra istituzionale è ancora visibile; senza quel valore vale `--header-height`).
- **Hook JS** solo tramite `data-*` (`data-nav-toggle`, `data-dropdown`, `data-tabs`, `data-dialog-open`…),
  mai tramite classi di stile.
- **Classi di contesto**: `html.no-js` / `html.js` (progressive enhancement), `.on-inverse` /
  `.surface-inverse` (anello di focus chiaro su superfici blu), `body.is-rtl`, `:lang(ar)`.
- **Niente attributi `style`, niente `<style>` inline, niente handler inline**: la CSP è `style-src 'self'`,
  `script-src 'self'` (test `test_owned_templates_have_no_forbidden_strings_inline_styles_or_handlers`).

### 2.1 Fogli di stile e script delle app

`main.css` copre la shell e i componenti. Un'app che ha bisogno di layout propri aggiunge **un** foglio in
`apps/<app>/static/<app>/` e lo carica dal blocco `extra_head` (gli script dal blocco `extra_scripts`, sempre
`type="module"`, mai inline). Regole: classi con prefisso dell'app (`.home-*`, `.ecosystem-*`, `.portal-*`),
solo token di `tokens.css` (nessun esadecimale, nessun `rgb()`), solo proprietà logiche, nessun componente
del catalogo ridefinito, focus ereditato da `base.css`, movimento solo con i token di durata. Le soglie
locali (`40rem`, `88rem`, `90rem`) sono ammesse per un singolo layout e non diventano breakpoint di sistema
(§6.2). `test_conforming_app_stylesheets_use_only_design_tokens` applica queste regole a ogni foglio sotto
`apps/*/static/` (token inesistenti, colori letterali, gradienti), con la sola eccezione dei due fogli di
G-22, verificati da `test_stage1_app_stylesheets_use_only_design_tokens` (test vincolante dal 20 settembre 2026). Inventario
verificato alla data della revisione:

| File | Caricato da | Conformità al sistema |
|---|---|---|
| `apps/pages/static/pages/css/pages.css` | `templates/pages/home.html`, `templates/pages/institutional_base.html` | conforme: solo token, solo proprietà logiche, nessun gradiente |
| `apps/pages/static/pages/js/home.js` | `templates/pages/home.html` | modulo ES senza dipendenze: mostra il bottone «Masquer cette annonce» del banner della home (nascosto senza JS), ricorda la scelta in `sessionStorage` per la sola scheda corrente, porta il focus su `main` |
| `apps/ecosystem/static/ecosystem/ecosystem.css` | `templates/ecosystem/_layout.html` | conforme; movimento solo dentro `prefers-reduced-motion: no-preference` |
| `apps/portal/static/portal/portal.css` | `templates/portal/base_portal.html` | conforme |
| `apps/forum/static/forum/forum.css` (Stage 1) | `templates/forum/index.html`, `templates/forum/register.html`, `templates/forum/register_done.html` | conforme dal 20 settembre 2026 (G-22 chiusa): solo token reali, fondo piatto, `--shadow-lg`, focus di `base.css` |
| `apps/orientation/static/orientation/wizard.css` (Stage 1) | `templates/orientation/start.html`, `templates/orientation/step.html`, `templates/orientation/result.html`, `templates/orientation/resume.html`, `templates/orientation/save_unavailable.html` | conforme dal 20 settembre 2026 (G-22 chiusa): solo token reali, scala tipografica `--font-size-*`, focus del sistema |
| `apps/orientation/static/orientation/wizard.js` (Stage 1) | `templates/orientation/step.html`, `templates/orientation/result.html` | modulo ES: mostra il bottone di stampa (`.js-print`, nascosto senza JS) e, dopo uno swap HTMX, porta il focus sulla nuova domanda. HTMX non è incluso nel progetto: oggi quel ramo non scatta mai e il wizard funziona con ricariche complete |

---

## 3. Token (`static/css/tokens.css`)

162 custom property su `:root`. **Separazione deliberata dei prefissi**: la scala tipografica è
`--font-size-*`; i colori del testo sono `--text-*`; le rampe sono `--color-*`; le superfici `--surface-*`;
i bordi `--border-*`. Un token `--text-*` non è mai una dimensione e un token `--font-size-*` non è mai un
colore.

Colonne: *Valore* = dichiarazione letterale nel file; *Risolto* = valore finale (esadecimale per gli alias
`var()`, equivalente in px con `1rem = 16px` per le dimensioni). «riserva» = token definito che nessun foglio di `static/css/`
consuma (un foglio di un'app può già usarlo: una riserva serve a questo — non rimuovere, non duplicare). Il test
`test_reserve_labels_match_the_design_system_stylesheets` verifica l'etichetta nei due sensi.

### 3.1 Colore — primary, blu istituzionale profondo (`--color-primary-*`)

| Token | Valore | Risolto | Uso |
|---|---|---|---|
| `--color-primary-950` | `#08182f` | — | blu più profondo; testo della selezione; base di `--surface-inverse-deep` |
| `--color-primary-900` | `#0f2b52` | — | **blu del marchio**: bottone primario, wordmark, titoli dei componenti, anello di focus, superfici inverse |
| `--color-primary-800` | `#163a6b` | — | hover del bottone primario; link visitati |
| `--color-primary-700` | `#1e4a85` | — | link; hover del bordo dei campi e dei titoli di accordion |
| `--color-primary-600` | `#2a5c9e` | — | riserva (tono intermedio) |
| `--color-primary-500` | `#3b6fb3` | — | riserva (tono intermedio) |
| `--color-primary-300` | `#9db6d8` | — | bordo della card cliccabile su hover/focus |
| `--color-primary-200` | `#c9d3e2` | — | testo attenuato su superfici blu (`--text-on-inverse-muted`) |
| `--color-primary-100` | `#dce6f3` | — | sfondo della selezione di testo |
| `--color-primary-50` | `#eef3f9` | — | hover del bottone secondario e del primario inverso |

### 3.2 Colore — secondary, verde italiano sobrio (`--color-secondary-*`)

Il verde è volutamente marginale («non bandiera italiana»): allo Stage 1 solo `--color-secondary-800` è consumato.

| Token | Valore | Risolto | Uso |
|---|---|---|---|
| `--color-secondary-900` | `#12472f` | — | riserva |
| `--color-secondary-800` | `#1f6b48` | — | stato «completato» dello stepper; base di `--color-success-fg` |
| `--color-secondary-700` | `#237a53` | — | riserva |
| `--color-secondary-300` | `#8fc4a6` | — | riserva |
| `--color-secondary-100` | `#dcede3` | — | riserva |
| `--color-secondary-50` | `#eef6f1` | — | riserva |

### 3.3 Colore — accent, bronzo/oro controllato (`--color-accent-*`)

Il bronzo è un inchiostro di rifinitura: filetti, numeri, marcatori. Mai campiture, mai bottoni.

| Token | Valore | Risolto | Uso |
|---|---|---|---|
| `--color-accent-700` | `#7a6124` | — | **unico bronzo per il testo** (5.65:1): eyebrow, meta del banner, titoli di navigazione locale |
| `--color-accent-600` | `#9a7b2f` | — | filetti, numerazioni decorative, marcatori, icone d'accento (3.83:1: mai testo informativo) |
| `--color-accent-400` | `#c9b26f` | — | riserva |
| `--color-accent-200` | `#e3d6b4` | — | bronzo chiaro su blu: titoli del footer, icone del footer, anello di focus inverso |
| `--color-accent-100` | `#f1ead8` | — | riserva |

### 3.4 Colore — neutral, grigi caldo-freddi (`--color-neutral-*`, `--color-white`)

| Token | Valore | Risolto | Uso |
|---|---|---|---|
| `--color-neutral-950` | `#10161d` | — | base di `--text-strong`; testo in stampa |
| `--color-neutral-900` | `#1b2430` | — | base di `--text-body` |
| `--color-neutral-800` | `#2c3644` | — | riserva |
| `--color-neutral-700` | `#465263` | — | base di `--text-secondary` |
| `--color-neutral-600` | `#5b6779` | — | base di `--text-muted` |
| `--color-neutral-500` | `#77828f` | — | base di `--border-strong` |
| `--color-neutral-400` | `#9aa3ae` | — | riserva |
| `--color-neutral-300` | `#c4cad1` | — | base di `--border-subtle` |
| `--color-neutral-200` | `#dde1e5` | — | base di `--border-hairline` |
| `--color-neutral-100` | `#eef0f2` | — | riserva |
| `--color-white` | `#ffffff` | — | base di `--text-on-inverse` |

### 3.5 Colore — semantici (`--color-success-*`, `--color-info-*`, `--color-warning-*`, `--color-error-*`, `--color-pending-*`)

Ogni stato è una terna fg / bg / border: fg ≥ 4.5:1 sul proprio bg, border ≥ 3:1 sul fondo di pagina (§4).

| Token | Valore | Risolto | Uso |
|---|---|---|---|
| `--color-success-fg` | `#1f6b48` | — | testo/icona di esito positivo |
| `--color-success-bg` | `#e8f3ec` | — | fondo |
| `--color-success-border` | `#569d77` | — | bordo (≥ 3:1 sul fondo di pagina) |
| `--color-info-fg` | `#1e4a85` | — | testo/icona informativi |
| `--color-info-bg` | `#e7eef8` | — | fondo |
| `--color-info-border` | `#6d8fbf` | — | bordo |
| `--color-warning-fg` | `#7a4e00` | — | testo/icona di avvertenza |
| `--color-warning-bg` | `#fdf3e0` | — | fondo |
| `--color-warning-border` | `#b38934` | — | bordo |
| `--color-error-fg` | `#9b1c1c` | — | testo d'errore, asterisco dei campi obbligatori, bordo del campo in errore, bottone `--danger` |
| `--color-error-bg` | `#fbe9e9` | — | fondo |
| `--color-error-border` | `#d16a6a` | — | bordo |
| `--color-pending-fg` | `#5e4b14` | — | stato «in attesa» (form non disponibile, moderazione) |
| `--color-pending-bg` | `#f6f0df` | — | fondo |
| `--color-pending-border` | `#a58e48` | — | bordo |

### 3.6 Superfici (`--surface-*`)

| Token | Valore | Risolto | Uso |
|---|---|---|---|
| `--surface-0` | `#fbfaf7` | — | fondo di pagina — bianco caldo |
| `--surface-1` | `#ffffff` | — | superfici rialzate: card, campi, dialog, dropdown, drawer |
| `--surface-2` | `#f4f1ea` | — | fascia attenuata; hover dei controlli trasparenti; notice istituzionale |
| `--surface-3` | `#ece7dc` | — | fascia più scura; traccia di `<progress>` |
| `--surface-inverse` | `var(--color-primary-900)` | `#0f2b52` | barra istituzionale, footer, hero e CTA inversi, skip link |
| `--surface-inverse-deep` | `var(--color-primary-950)` | `#08182f` | riserva |
| `--surface-overlay` | `rgb(15 43 82 / 0.55)` | — | velo dietro drawer e dialog |

### 3.7 Testo — colori, non dimensioni (`--text-*`)

| Token | Valore | Risolto | Uso |
|---|---|---|---|
| `--text-strong` | `var(--color-neutral-950)` | `#10161d` | titoli, etichette dei campi |
| `--text-body` | `var(--color-neutral-900)` | `#1b2430` | testo corrente |
| `--text-secondary` | `var(--color-neutral-700)` | `#465263` | lead, descrizioni, testo di supporto |
| `--text-muted` | `var(--color-neutral-600)` | `#5b6779` | didascalie, note, metadati (minimo ammesso per testo: 5.50:1) |
| `--text-placeholder` | `#6b7683` | — | placeholder dei campi (4.62:1 su `--surface-1`) |
| `--text-on-inverse` | `var(--color-white)` | `#ffffff` | testo su superfici blu |
| `--text-on-inverse-muted` | `var(--color-primary-200)` | `#c9d3e2` | testo secondario su superfici blu |
| `--text-link` | `var(--color-primary-700)` | `#1e4a85` | link |
| `--text-link-hover` | `var(--color-primary-900)` | `#0f2b52` | link su hover |
| `--text-brand` | `var(--color-primary-900)` | `#0f2b52` | wordmark |

### 3.8 Bordi (`--border-*`)

| Token | Valore | Risolto | Uso |
|---|---|---|---|
| `--border-hairline` | `var(--color-neutral-200)` | `#dde1e5` | filetti editoriali (decorativi) |
| `--border-subtle` | `var(--color-neutral-300)` | `#c4cad1` | bordi di contenitori, dropdown, pill (decorativi) |
| `--border-strong` | `var(--color-neutral-500)` | `#77828f` | **perimetro dei campi** e dei marcatori dello stepper (≥ 3:1) |
| `--border-accent` | `var(--color-accent-600)` | `#9a7b2f` | filetto d'accento (`.rule--accent`, citazioni in `.prose`) |
| `--border-inverse` | `rgb(255 255 255 / 0.18)` | — | filetti su superfici blu |
| `--border-width` | `1px` | 1 px | spessore standard |
| `--border-width-strong` | `2px` | 2 px | filetti d'accento |

### 3.9 Focus (`--focus-ring-*`)

| Token | Valore | Risolto | Uso |
|---|---|---|---|
| `--focus-ring-color` | `var(--color-primary-900)` | `#0f2b52` | anello di focus su fondi chiari (13.52:1) |
| `--focus-ring-offset-color` | `var(--surface-0)` | `#fbfaf7` | alone interno dell'anello (seconda tonalità) |
| `--focus-ring-inverse` | `var(--color-accent-200)` | `#e3d6b4` | anello di focus dentro `.on-inverse` / `.surface-inverse` (9.78:1) |
| `--focus-ring-width` | `2px` | 2 px | spessore dell'outline |
| `--focus-ring-offset` | `2px` | 2 px | distanza dell'outline e spessore dell'alone |

### 3.10 Famiglie tipografiche (`--font-*`)

| Token | Valore | Risolto | Uso |
|---|---|---|---|
| `--font-display` | `"IBM Plex Serif", "Iowan Old Style", "Palatino Linotype", Georgia, serif` | — | titoli (serif) |
| `--font-body` | `"IBM Plex Sans", "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif` | — | testo e UI (sans) |
| `--font-arabic` | `"IBM Plex Sans Arabic", "Noto Sans Arabic", "Segoe UI", Tahoma, sans-serif` | — | arabo: sostituisce display e body sotto `:lang(ar)` |
| `--font-mono` | `"IBM Plex Mono", ui-monospace, Consolas, monospace` | — | codice, riferimenti tecnici (font non self-hosted: G-15) |

### 3.11 Scala tipografica (`--font-size-*`)

Cinque passi fluidi con `clamp()` (nessun salto ai breakpoint), gli altri fissi. Tutto in `rem`: rispetta la dimensione del testo scelta dall'utente e lo zoom.

| Token | Valore | Risolto | Uso |
|---|---|---|---|
| `--font-size-display` | `clamp(2.5rem, 1.9rem + 2.4vw, 4rem)` | 40–64 px (fluido tra viewport 400 e 1400 px) | titolo dell'hero |
| `--font-size-h1` | `clamp(2rem, 1.55rem + 1.8vw, 3rem)` | 32–48 px (fluido tra viewport 400 e 1289 px) | h1 |
| `--font-size-h2` | `clamp(1.5rem, 1.3rem + 0.9vw, 2.125rem)` | 24–34 px (fluido tra viewport 356 e 1467 px) | h2 |
| `--font-size-h3` | `clamp(1.25rem, 1.15rem + 0.4vw, 1.5rem)` | 20–24 px (fluido tra viewport 400 e 1400 px) | h3, sottotitoli, titoli di entrance/banner |
| `--font-size-h4` | `1.125rem` | 18 px | h4, titoli di card/accordion/pathway |
| `--font-size-lead` | `clamp(1.125rem, 1.05rem + 0.3vw, 1.3125rem)` | 18–21 px (fluido tra viewport 400 e 1400 px) | lead |
| `--font-size-body` | `1rem` | 16 px | testo corrente, campi |
| `--font-size-small` | `0.9375rem` | 15 px | navigazione, testo compatto |
| `--font-size-legal` | `0.875rem` | 14 px | note legali |
| `--font-size-caption` | `0.8125rem` | 13 px | didascalie, breadcrumb, barra istituzionale, badge |
| `--font-size-label` | `0.875rem` | 14 px | etichette dei campi, bottoni `--sm` |
| `--font-size-button` | `0.9375rem` | 15 px | bottoni |
| `--font-size-eyebrow` | `0.75rem` | 12 px | eyebrow maiuscolo spaziato |

### 3.12 Interlinea, spaziatura delle lettere, pesi, misure (`--leading-*`, `--tracking-*`, `--weight-*`, `--measure-*`)

| Token | Valore | Risolto | Uso |
|---|---|---|---|
| `--leading-display` | `1.05` | — | hero |
| `--leading-heading` | `1.15` | — | h1–h2 |
| `--leading-tight` | `1.3` | — | h3–h4, titoli dei componenti |
| `--leading-body` | `1.6` | — | testo |
| `--leading-relaxed` | `1.7` | — | lead e `.prose` |
| `--tracking-tight` | `-0.01em` | — | titoli |
| `--tracking-normal` | `0` | — | riserva |
| `--tracking-eyebrow` | `0.12em` | — | eyebrow (0 in arabo) |
| `--tracking-button` | `0.02em` | — | bottoni (0 in arabo) |
| `--weight-regular` | `400` | — | testo, hero |
| `--weight-medium` | `500` | — | titoli, bottoni, etichette |
| `--weight-semibold` | `600` | — | enfasi, h4, eyebrow |
| `--measure-prose` | `68ch` | — | larghezza di lettura |
| `--measure-lead` | `60ch` | — | lead, intestazioni di sezione |
| `--measure-narrow` | `44ch` | — | testi brevi centrati (stato vuoto) |

### 3.13 Spazio — griglia da 4 px (`--space-*`, `--section-gap`, `--stack-gap`, `--gutter`)

Scala: 4 · 8 · 12 · 16 · 20 · 24 · 32 · 40 · 48 · 64 · 80 · 96 · 128 px. I passi 7, 9, 11, 14… non esistono: è una scelta (scala corta, ritmo riconoscibile), non una dimenticanza.

| Token | Valore | Risolto | Uso |
|---|---|---|---|
| `--space-1` | `0.25rem` | 4 px | passo della griglia |
| `--space-2` | `0.5rem` | 8 px | passo della griglia |
| `--space-3` | `0.75rem` | 12 px | passo della griglia |
| `--space-4` | `1rem` | 16 px | passo della griglia |
| `--space-5` | `1.25rem` | 20 px | passo della griglia |
| `--space-6` | `1.5rem` | 24 px | passo della griglia |
| `--space-8` | `2rem` | 32 px | passo della griglia |
| `--space-10` | `2.5rem` | 40 px | passo della griglia |
| `--space-12` | `3rem` | 48 px | passo della griglia |
| `--space-16` | `4rem` | 64 px | passo della griglia |
| `--space-20` | `5rem` | 80 px | passo della griglia |
| `--space-24` | `6rem` | 96 px | passo della griglia |
| `--space-32` | `8rem` | 128 px | riserva |
| `--section-gap` | `clamp(var(--space-16), 6vw, var(--space-24))` | 64–96 px | distanza tra sezioni (64–96 px) |
| `--stack-gap` | `var(--space-4)` | `1rem` = 16 px | passo di `.stack` |
| `--gutter` | `clamp(var(--space-4), 4vw, var(--space-8))` | 16–32 px | margine laterale dei container e gap di colonna (16–32 px) |

### 3.14 Raggi (`--radius-*`)

Raggi deliberatamente piccoli — istituzionale, non SaaS. I cerchi (marcatori) usano `50%`.

| Token | Valore | Risolto | Uso |
|---|---|---|---|
| `--radius-none` | `0` | — | riserva |
| `--radius-xs` | `2px` | 2 px | badge, anello di focus, voci di menu |
| `--radius-sm` | `3px` | 3 px | **raggio standard**: bottoni, campi, card, notice, dialog |
| `--radius-md` | `4px` | 4 px | riserva (massimo ammesso per i box) |
| `--radius-pill` | `999px` | 999 px | pill della navigazione locale, barra di avanzamento |

### 3.15 Ombre (`--shadow-*`)

Ombre fredde (tinta del blu primario), a bassa opacità. `--shadow-lg` è il limite superiore.

| Token | Valore | Risolto | Uso |
|---|---|---|---|
| `--shadow-hairline` | `0 0 0 1px rgb(27 36 48 / 0.06)` | — | contorno leggerissimo di card e pagine account |
| `--shadow-sm` | `0 1px 2px rgb(15 43 82 / 0.06), 0 1px 1px rgb(15 43 82 / 0.04)` | — | card cliccabile su hover |
| `--shadow-md` | `0 4px 12px rgb(15 43 82 / 0.08), 0 1px 3px rgb(15 43 82 / 0.06)` | — | dropdown (lingua, account) |
| `--shadow-lg` | `0 16px 40px rgb(15 43 82 / 0.14), 0 2px 6px rgb(15 43 82 / 0.06)` | — | mega-menu e dialog — la più grande ammessa |

### 3.16 Motion (`--duration-*`, `--ease-*`, `--reveal-distance`)

Tutte le durate sono azzerate da `prefers-reduced-motion: reduce` (§3.18, §9).

| Token | Valore | Risolto | Uso |
|---|---|---|---|
| `--duration-fast` | `120ms` | — | hover di link, bottoni, campi |
| `--duration-base` | `200ms` | — | menu, drawer, dialog, frecce |
| `--duration-slow` | `360ms` | — | barra di avanzamento |
| `--duration-reveal` | `600ms` | — | comparsa allo scroll |
| `--ease-standard` | `cubic-bezier(0.2, 0, 0, 1)` | — | cambi di colore |
| `--ease-out` | `cubic-bezier(0.16, 1, 0.3, 1)` | — | ingressi e spostamenti |
| `--ease-in` | `cubic-bezier(0.7, 0, 0.84, 0)` | — | riserva (uscite) |
| `--reveal-distance` | `16px` | 16 px | spostamento verticale del reveal |

### 3.17 Livelli, contenitori, dimensioni dei controlli (`--z-*`, `--container-*`, `--control-height*`, `--icon-size*`, `--header-height`, `--utility-height`)

| Token | Valore | Risolto | Uso |
|---|---|---|---|
| `--z-below` | `-1` | — | riserva |
| `--z-base` | `0` | — | riserva |
| `--z-raised` | `10` | — | riserva |
| `--z-sticky` | `100` | — | sommario di pagina sticky |
| `--z-header` | `200` | — | header sticky |
| `--z-dropdown` | `300` | — | mega-menu, dropdown |
| `--z-drawer` | `400` | — | drawer della navigazione sotto 80rem (overlay = −1) |
| `--z-overlay` | `500` | — | riserva |
| `--z-modal` | `600` | — | dialog in modalità senza JS |
| `--z-skiplink` | `1000` | — | skip link, sopra tutto |
| `--container-max` | `75rem` | 1200 px | `.container` |
| `--container-wide` | `85rem` | 1360 px | `.container--wide` |
| `--container-narrow` | `46rem` | 736 px | `.container--narrow`, `.form`, stato vuoto |
| `--container-prose` | `52rem` | 832 px | `.container--prose`, pagine legali e d'errore |
| `--control-height` | `2.75rem` | 44 px | **altezza minima di ogni controllo** (WCAG 2.5.8, obiettivo 44 px) |
| `--control-height-sm` | `2.25rem` | 36 px | bottoni `--sm` |
| `--icon-size` | `1.25rem` | 20 px | icona standard |
| `--icon-size-sm` | `1rem` | 16 px | icona piccola |
| `--icon-size-lg` | `1.75rem` | 28 px | icona grande |
| `--header-height` | `4.5rem` | 72 px | altezza dell'header; base di `scroll-padding-block-start` e degli elementi sticky |
| `--utility-height` | `2.5rem` | 40 px | barra istituzionale |

### 3.18 Override contestuali

| Contesto | Token ridefiniti | Effetto |
|---|---|---|
| `:lang(ar)` | `--font-display` e `--font-body` → `var(--font-arabic)`; `--tracking-eyebrow: 0`; `--tracking-button: 0` | il serif non ha glifi arabi: titoli e testo usano IBM Plex Sans Arabic; la spaziatura delle lettere è azzerata perché in arabo spezza le legature. Le regole `:lang(ar) .eyebrow`, `.btn--upper`, `.entrance__cta`, `.timeline__label`, `.page-header__eyebrow`, `.hero__eyebrow`, `.local-nav__title`, `.site-footer__heading` tolgono anche `text-transform: uppercase`. |
| `@media (prefers-reduced-motion: reduce)` | `--duration-fast`, `--duration-base`, `--duration-slow`, `--duration-reveal` → `0ms`; `--reveal-distance` → `0px` | ogni transizione basata sui token diventa istantanea (misurato: `--duration-base` = `0ms`, `transition-duration` effettiva `1e-05s`, `scroll-behavior: auto`). Vedi §9. |

---

## 4. Contrasto WCAG misurato

Rapporti ricalcolati il 20/09/2026 dai valori di `tokens.css` con la formula di luminanza relativa WCAG 2.x
(stesso algoritmo di `tests/frontend/test_static_assets.py`). Requisito: **4.5** = testo normale (SC 1.4.3),
**3.0** = componenti UI e oggetti grafici (SC 1.4.11) o testo grande, **—** = elemento decorativo senza
requisito. Le prime 30 righe sono esattamente le coppie bloccate da `test_wcag_contrast`; le successive sono
coppie aggiuntive usate dai componenti. Il test `test_contrast_table_matches_recomputed_ratios` ricalcola
ogni riga con tolleranza ± 0.05.

<!-- contrast-table:start -->
| Coppia | Primo piano | Sfondo | Rapporto | Requisito | Esito |
|---|---|---|---|---|---|
| testo corrente sul fondo | `--text-body` #1b2430 | `--surface-0` #fbfaf7 | 15.00:1 | 4.5 | AAA |
| testo secondario sul fondo | `--text-secondary` #465263 | `--surface-0` #fbfaf7 | 7.60:1 | 4.5 | AAA |
| testo attenuato sul fondo | `--text-muted` #5b6779 | `--surface-0` #fbfaf7 | 5.50:1 | 4.5 | AA |
| testo attenuato su fascia attenuata | `--text-muted` #5b6779 | `--surface-2` #f4f1ea | 5.09:1 | 4.5 | AA |
| placeholder nel campo | `--text-placeholder` #6b7683 | `--surface-1` #ffffff | 4.62:1 | 4.5 | AA |
| link sul fondo | `--text-link` #1e4a85 | `--surface-0` #fbfaf7 | 8.48:1 | 4.5 | AAA |
| blu del marchio sul fondo | `--color-primary-900` #0f2b52 | `--surface-0` #fbfaf7 | 13.52:1 | 4.5 | AAA |
| bianco su blu (bottone primario) | `--color-white` #ffffff | `--color-primary-900` #0f2b52 | 14.12:1 | 4.5 | AAA |
| bianco su blu 800 (hover del bottone) | `--color-white` #ffffff | `--color-primary-800` #163a6b | 11.34:1 | 4.5 | AAA |
| testo attenuato su superficie blu | `--text-on-inverse-muted` #c9d3e2 | `--surface-inverse` #0f2b52 | 9.34:1 | 4.5 | AAA |
| bronzo chiaro su blu (titoli del footer) | `--color-accent-200` #e3d6b4 | `--surface-inverse` #0f2b52 | 9.78:1 | 4.5 | AAA |
| bronzo da testo sul fondo (eyebrow) | `--color-accent-700` #7a6124 | `--surface-0` #fbfaf7 | 5.65:1 | 4.5 | AA |
| verde 800 sul fondo | `--color-secondary-800` #1f6b48 | `--surface-0` #fbfaf7 | 6.18:1 | 4.5 | AA |
| bianco su verde 800 (passo completato) | `--color-white` #ffffff | `--color-secondary-800` #1f6b48 | 6.45:1 | 4.5 | AA |
| success: testo su fondo | `--color-success-fg` #1f6b48 | `--color-success-bg` #e8f3ec | 5.67:1 | 4.5 | AA |
| info: testo su fondo | `--color-info-fg` #1e4a85 | `--color-info-bg` #e7eef8 | 7.58:1 | 4.5 | AAA |
| warning: testo su fondo | `--color-warning-fg` #7a4e00 | `--color-warning-bg` #fdf3e0 | 6.54:1 | 4.5 | AA |
| error: testo su fondo | `--color-error-fg` #9b1c1c | `--color-error-bg` #fbe9e9 | 6.96:1 | 4.5 | AA |
| testo d'errore sul fondo di pagina | `--color-error-fg` #9b1c1c | `--surface-0` #fbfaf7 | 7.81:1 | 4.5 | AAA |
| pending: testo su fondo | `--color-pending-fg` #5e4b14 | `--color-pending-bg` #f6f0df | 7.40:1 | 4.5 | AAA |
| bordo del campo sul fondo | `--border-strong` #77828f | `--surface-0` #fbfaf7 | 3.74:1 | 3.0 | AA (1.4.11) |
| bordo del campo sul campo | `--border-strong` #77828f | `--surface-1` #ffffff | 3.91:1 | 3.0 | AA (1.4.11) |
| filetto bronzo sul fondo | `--color-accent-600` #9a7b2f | `--surface-0` #fbfaf7 | 3.83:1 | 3.0 | AA (1.4.11) |
| anello di focus sul fondo | `--focus-ring-color` #0f2b52 | `--surface-0` #fbfaf7 | 13.52:1 | 3.0 | AA (1.4.11) |
| anello di focus su blu | `--focus-ring-inverse` #e3d6b4 | `--surface-inverse` #0f2b52 | 9.78:1 | 3.0 | AA (1.4.11) |
| bordo success sul fondo | `--color-success-border` #569d77 | `--surface-0` #fbfaf7 | 3.10:1 | 3.0 | AA (1.4.11) |
| bordo info sul fondo | `--color-info-border` #6d8fbf | `--surface-0` #fbfaf7 | 3.18:1 | 3.0 | AA (1.4.11) |
| bordo warning sul fondo | `--color-warning-border` #b38934 | `--surface-0` #fbfaf7 | 3.07:1 | 3.0 | AA (1.4.11) |
| bordo error sul fondo | `--color-error-border` #d16a6a | `--surface-0` #fbfaf7 | 3.36:1 | 3.0 | AA (1.4.11) |
| bordo pending sul fondo | `--color-pending-border` #a58e48 | `--surface-0` #fbfaf7 | 3.07:1 | 3.0 | AA (1.4.11) |
| titoli sul fondo | `--text-strong` #10161d | `--surface-0` #fbfaf7 | 17.43:1 | 4.5 | AAA |
| testo corrente su superficie rialzata | `--text-body` #1b2430 | `--surface-1` #ffffff | 15.65:1 | 4.5 | AAA |
| testo corrente su fascia attenuata | `--text-body` #1b2430 | `--surface-2` #f4f1ea | 13.88:1 | 4.5 | AAA |
| testo secondario su fascia attenuata | `--text-secondary` #465263 | `--surface-2` #f4f1ea | 7.03:1 | 4.5 | AAA |
| link su hover sul fondo | `--text-link-hover` #0f2b52 | `--surface-0` #fbfaf7 | 13.52:1 | 4.5 | AAA |
| bianco su blu (footer, barra istituzionale) | `--text-on-inverse` #ffffff | `--surface-inverse` #0f2b52 | 14.12:1 | 4.5 | AAA |
| blu su primary-50 (hover del bottone secondario) | `--color-primary-900` #0f2b52 | `--color-primary-50` #eef3f9 | 12.65:1 | 4.5 | AAA |
| blu su fascia attenuata (hover ghost, titolo del banner) | `--color-primary-900` #0f2b52 | `--surface-2` #f4f1ea | 12.51:1 | 4.5 | AAA |
| bronzo da testo su fascia attenuata (meta del banner) | `--color-accent-700` #7a6124 | `--surface-2` #f4f1ea | 5.23:1 | 4.5 | AA |
| testo d'errore su superficie rialzata | `--color-error-fg` #9b1c1c | `--surface-1` #ffffff | 8.15:1 | 4.5 | AAA |
| filetto/icona bronzo su superficie rialzata (mega-menu) | `--color-accent-600` #9a7b2f | `--surface-1` #ffffff | 4.00:1 | 3.0 | AA (1.4.11) |
| bordo sottile sul fondo (decorativo) | `--border-subtle` #c4cad1 | `--surface-0` #fbfaf7 | 1.58:1 | — | n/a (decorativo) |
| filetto hairline sul fondo (decorativo) | `--border-hairline` #dde1e5 | `--surface-0` #fbfaf7 | 1.26:1 | — | n/a (decorativo) |
<!-- contrast-table:end -->

Regole d'uso che derivano dalla tabella:

- `--color-accent-600` (3.83:1 sul fondo) **non è un colore di testo**: solo filetti, marcatori, icone e
  numerazioni decorative `aria-hidden` (`.entrance__num`, `.pathway-list__num`, `.numeral`) o testo molto
  grande (`.error-page__code`, ≥ 64 px). Per il testo in bronzo si usa `--color-accent-700` (5.65:1). Vedi
  lacuna G-09 in `docs/ACCESSIBILITY.md`.
- `--border-hairline` e `--border-subtle` sono **decorativi** (1.26:1 e 1.58:1): non possono essere l'unico
  indicatore del perimetro di un controllo. I campi usano `--border-strong` (3.74:1 / 3.91:1).
- I bordi semantici (`--color-*-border`) superano 3:1 sul fondo di pagina: il perimetro di un notice resta
  percepibile anche senza il colore di riempimento.
- Su superfici blu (`.on-inverse`): testo `--text-on-inverse` (14.12:1) o `--text-on-inverse-muted`
  (9.34:1), titoli di colonna `--color-accent-200` (9.78:1), anello di focus `--focus-ring-inverse`.
- I controlli disabilitati (`.btn:disabled`, `opacity: 0.55`) sono esenti da SC 1.4.3.

---

## 5. Tipografia

### 5.1 Famiglie (ADR-008)

| Ruolo | Token | Famiglia | Uso |
|---|---|---|---|
| Display / titoli | `--font-display` | IBM Plex Serif → Iowan Old Style → Palatino Linotype → Georgia → serif | `h1`–`h3`, `.text-display`, wordmark, titoli di accordion/card/entrance, numerazioni, citazioni |
| Testo / UI | `--font-body` | IBM Plex Sans → Segoe UI → Roboto → Helvetica Neue → Arial → sans-serif | corpo, `h4`, bottoni, etichette, navigazione, eyebrow |
| Arabo | `--font-arabic` | IBM Plex Sans Arabic → Noto Sans Arabic → Segoe UI → Tahoma → sans-serif | sotto `:lang(ar)` sostituisce **sia** `--font-display` **sia** `--font-body` |
| Monospazio | `--font-mono` | IBM Plex Mono → ui-monospace → Consolas → monospace | `code`, `kbd`, `pre`, riferimento d'errore (`.error-page__ref`). **IBM Plex Mono non è self-hosted** (nessun file in `static/fonts/`, nessuna `@font-face`): il browser usa il monospazio di sistema — lacuna G-15, accettata finché il sito non pubblica codice. |

Pesi disponibili: 400, 500, 600 (+ corsivo 400 per Serif e Sans). `--weight-regular/medium/semibold`
mappano esattamente questi tre; non esiste un 700: `strong`/`b` usano 600.

### 5.2 File self-hosted (`static/fonts/`, 25 file woff2, ≈ 614 KB in totale)

Sottoinsiemi `latin`, `latin-ext`, `arabic`, selezionati dal browser tramite `unicode-range`: una pagina in
francese scarica tipicamente 3–4 file (Sans 400/500/600 latin + Serif 500 latin), una pagina in arabo i
file `arabic` di Plex Sans Arabic.

| File | Famiglia | Peso · stile | Sottoinsieme | KB |
|---|---|---|---|---|
| `ibm-plex-sans-400-italic-latin-ext.woff2` | IBM Plex Sans | 400 · corsivo | latin-ext | 16.6 |
| `ibm-plex-sans-400-italic-latin.woff2` | IBM Plex Sans | 400 · corsivo | latin | 23.8 |
| `ibm-plex-sans-400-normal-latin-ext.woff2` | IBM Plex Sans | 400 · tondo | latin-ext | 30.2 |
| `ibm-plex-sans-400-normal-latin.woff2` | IBM Plex Sans | 400 · tondo | latin | 44.6 |
| `ibm-plex-sans-500-normal-latin-ext.woff2` | IBM Plex Sans | 500 · tondo | latin-ext | 30.2 |
| `ibm-plex-sans-500-normal-latin.woff2` | IBM Plex Sans | 500 · tondo | latin | 44.6 |
| `ibm-plex-sans-600-normal-latin-ext.woff2` | IBM Plex Sans | 600 · tondo | latin-ext | 30.2 |
| `ibm-plex-sans-600-normal-latin.woff2` | IBM Plex Sans | 600 · tondo | latin | 44.6 |
| `ibm-plex-sans-arabic-400-normal-arabic.woff2` | IBM Plex Sans Arabic | 400 · tondo | arabic | 41.8 |
| `ibm-plex-sans-arabic-400-normal-latin-ext.woff2` | IBM Plex Sans Arabic | 400 · tondo | latin-ext | 6.5 |
| `ibm-plex-sans-arabic-400-normal-latin.woff2` | IBM Plex Sans Arabic | 400 · tondo | latin | 18.7 |
| `ibm-plex-sans-arabic-500-normal-arabic.woff2` | IBM Plex Sans Arabic | 500 · tondo | arabic | 44.2 |
| `ibm-plex-sans-arabic-500-normal-latin-ext.woff2` | IBM Plex Sans Arabic | 500 · tondo | latin-ext | 6.4 |
| `ibm-plex-sans-arabic-500-normal-latin.woff2` | IBM Plex Sans Arabic | 500 · tondo | latin | 19.6 |
| `ibm-plex-sans-arabic-600-normal-arabic.woff2` | IBM Plex Sans Arabic | 600 · tondo | arabic | 44.6 |
| `ibm-plex-sans-arabic-600-normal-latin-ext.woff2` | IBM Plex Sans Arabic | 600 · tondo | latin-ext | 6.5 |
| `ibm-plex-sans-arabic-600-normal-latin.woff2` | IBM Plex Sans Arabic | 600 · tondo | latin | 20.0 |
| `ibm-plex-serif-400-italic-latin-ext.woff2` | IBM Plex Serif | 400 · corsivo | latin-ext | 15.9 |
| `ibm-plex-serif-400-italic-latin.woff2` | IBM Plex Serif | 400 · corsivo | latin | 20.4 |
| `ibm-plex-serif-400-normal-latin-ext.woff2` | IBM Plex Serif | 400 · tondo | latin-ext | 15.1 |
| `ibm-plex-serif-400-normal-latin.woff2` | IBM Plex Serif | 400 · tondo | latin | 19.1 |
| `ibm-plex-serif-500-normal-latin-ext.woff2` | IBM Plex Serif | 500 · tondo | latin-ext | 15.1 |
| `ibm-plex-serif-500-normal-latin.woff2` | IBM Plex Serif | 500 · tondo | latin | 19.8 |
| `ibm-plex-serif-600-normal-latin-ext.woff2` | IBM Plex Serif | 600 · tondo | latin-ext | 15.2 |
| `ibm-plex-serif-600-normal-latin.woff2` | IBM Plex Serif | 600 · tondo | latin | 20.0 |

### 5.3 Licenza

IBM Plex (Serif, Sans, Sans Arabic) — © IBM Corp. — è distribuito con **SIL Open Font License 1.1**:
uso, incorporazione e ridistribuzione (anche in formato woff2 e in sottoinsiemi) sono consentiti; i font
non possono essere venduti da soli; il nome riservato «Plex» non può essere usato per versioni modificate.
I file sono i sottoinsiemi woff2 pubblicati dalla Google Fonts CSS API, scaricati **una sola volta** da
`scripts/fetch_fonts.py` (unico punto del repository in cui compaiono gli host di Google) e serviti dal
nostro dominio: nessuna richiesta a terzi in runtime (CSP `font-src 'self'`; lo scanner
`apps/cms/forbidden.py` vieta gli host dei font esterni nelle pagine; test
`tests/frontend/test_layout.py::test_fonts_css_references_only_local_files_that_exist` e
`tests/frontend/test_browser.py::test_fonts_are_self_hosted_and_loaded`).

### 5.4 Strategia di caricamento

- `font-display: swap` su tutte le 25 facce: il testo è subito leggibile nel fallback di sistema e viene
  ridisegnato all'arrivo del woff2 (nessun FOIT).
- **Preload mirato** in `templates/base.html`: pagine LTR → `ibm-plex-sans-400-normal-latin.woff2` +
  `ibm-plex-serif-500-normal-latin.woff2`; pagine RTL → `ibm-plex-sans-arabic-400-normal-arabic.woff2`
  (test `test_html_lang_and_dir_attributes`).
- `unicode-range` per sottoinsieme: `latin-ext` e `arabic` vengono scaricati solo se la pagina contiene quei
  caratteri.
- Stack di fallback metricamente vicini (Georgia per il serif, Segoe UI/Roboto/Arial per il sans) per
  contenere lo spostamento di layout allo swap.

### 5.5 Scala e classi

La scala è in §3 (`--font-size-*`). Mappatura in `base.css`:

| Elemento / classe | Dimensione | Famiglia, peso, interlinea |
|---|---|---|
| `.text-display`, `.hero__title` | `--font-size-display` | display, 400, `--leading-display` (1.05), tracking −0.01em |
| `h1`, `.text-h1` | `--font-size-h1` | display, 500, `--leading-heading` (1.15), `text-wrap: balance` |
| `h2`, `.text-h2` | `--font-size-h2` | display, 500, 1.15 |
| `h3`, `.text-h3` | `--font-size-h3` | display, 500, `--leading-tight` (1.3) |
| `h4`, `.text-h4` | `--font-size-h4` | **body** (sans), 600, 1.3 |
| `.lead`, `.text-lead` | `--font-size-lead` | body, 400, `--leading-relaxed` (1.7), `--text-secondary`, max `--measure-lead` |
| `body`, `p` | `--font-size-body` | body, 400, `--leading-body` (1.6) |
| `.text-small` | `--font-size-small` | — |
| `.text-legal` | `--font-size-legal` | interlinea 1.55, `--text-muted` |
| `.text-caption`, `small` | `--font-size-caption` | interlinea 1.5, `--text-muted` |
| `.text-label`, etichette dei campi | `--font-size-label` | 500 |
| `.btn` | `--font-size-button` | 500, tracking 0.02em |
| `.eyebrow` | `--font-size-eyebrow` | body, 600, maiuscolo, tracking 0.12em, `--color-accent-700` (in arabo: né maiuscolo né tracking) |
| `.numeral` | ereditata | display, `lining-nums tabular-nums`, `--color-accent-600` (decorativo) |

Contenuti lunghi: `.prose` (misura 68ch, interlinea 1.7, `h2` con filetto superiore, tabelle con `th`
allineati a `start`, `blockquote` con filetto bronzo sul lato `inline-start`).

---

## 6. Layout

### 6.1 Contenitori

| Classe | Larghezza massima | Uso |
|---|---|---|
| `.container` | `--container-max` (75rem = 1200 px) | default di ogni sezione |
| `.container--wide` | `--container-wide` (85rem = 1360 px) | fasce fotografiche, diagrammi |
| `.container--narrow` | `--container-narrow` (46rem = 736 px) | form, pagine account |
| `.container--prose` | `--container-prose` (52rem = 832 px) | lettura lunga (pagine legali, errori) |
| `.container--flush` | — | azzera il padding laterale |

Tutti: `inline-size: 100%`, `margin-inline: auto`, `padding-inline: var(--gutter)` con
`--gutter: clamp(1rem, 4vw, 2rem)` (16–32 px).

### 6.2 Breakpoint (mobile-first, in `rem`)

| Soglia | px | Cosa cambia |
|---|---|---|
| `48rem` | 768 | griglia a 12 colonne attiva (`.col-*`), `.entrances` 2 colonne, stepper orizzontale, timeline 4 + 4, footer 2 colonne, `.form-row--2` |
| `56rem` | 896 | `.split` testo/figura 7fr / 5fr |
| `64rem` | 1024 | `.layout-sidebar` a due colonne con aside sticky, navigazione locale in colonna, varianti `.lg:col-*`, footer 4 colonne, CTA panel e banner in riga, `.hide-mobile` / `.hide-desktop` |
| `72rem` | 1152 | `.entrances` 4 colonne |
| `80rem` | 1280 | **navigazione desktop** (mega-menu al posto del drawer, bottone «Menu» nascosto), timeline a 8 in riga; `.brand__tagline` visibile (classe predisposta: `header.html` oggi non la usa) |

Media query «solo sotto»: `max-width: 47.999rem` (etichetta del link «Espace réservé» solo per screen
reader, freccia della pathway list nascosta), `max-width: 63.999rem` (`.hide-mobile`, local nav a pill) e
`max-width: 79.999rem` (drawer). `.hide-mobile` nasconde sotto 64rem; `.hide-desktop` da 64rem in su.

**La navigazione ha un breakpoint proprio (80rem).** Con il menu completo di Fase 3 sette voci di primo
livello non entrano accanto al wordmark sotto 1280 px: il passaggio da drawer a mega-menu è stato spostato
da 64rem a 80rem dalla QA in browser del 20/09/2026. La soglia vive in tre punti che devono restare
allineati: `@media (min-width: 80rem)` e `@media (max-width: 79.999rem)` in `components.css` §7, e
`DESKTOP = window.matchMedia("(min-width: 80rem)")` in `static/js/main.js`
(`test_navigation_breakpoint_is_consistent_and_documented`). Conseguenze: un tablet in orizzontale e un
laptop da 1024–1279 px usano il drawer; «mobile» in `.hide-mobile` significa «sotto 64rem», non «modalità
drawer» (tra 64rem e 80rem gli elementi `.hide-mobile` sono visibili mentre il menu è ancora un drawer); a
1280 px qualunque zoom del browser oltre il 100 % riporta al drawer.

### 6.3 Griglia editoriale

`.grid` = 12 colonne `minmax(0, 1fr)`, gap `var(--space-6)` × `var(--gutter)`; ogni figlio occupa 12
colonne finché non riceve `.col-4 … .col-9` (≥ 48rem), `.col-start-2 … .col-start-4` (rientro editoriale)
o `.lg:col-3/4/6/8` (≥ 64rem). `.grid-auto` = `repeat(auto-fit, minmax(min(100%, 17rem), 1fr))` per liste
di elementi uguali. `.layout-sidebar` = 17rem + 1fr (aside sticky sotto l'header; `--end` inverte);
`.split` = testo + figura (`--even` per 1:1).

### 6.4 Ritmo verticale

| Livello | Valore | Classe / regola |
|---|---|---|
| Tra sezioni | `--section-gap` = `clamp(4rem, 6vw, 6rem)` (64–96 px) | `.section` (padding-block); `.section--tight` = 48 px; `.section--flush-top` |
| Intestazione di sezione → contenuto | 40 px | `.section__header` (`margin-block-end: var(--space-10)`) |
| Tra blocchi di testo | 16 px | `p`, `.flow > * + *`, `.stack` (`--stack-gap`), `.prose > * + *` |
| Pile | 8 / 16 / 32 px | `.stack--sm`, `.stack`, `.stack--lg` |
| Tra campi di un form | 24 px (20 px nelle pagine account) | `.form-field` |
| Dentro `.prose` | `h2` +48 px con filetto, `h3` +32 px | `base.css` |

Fasce: `.section--muted` (`--surface-2`), `.section--inverse` (blu, testo chiaro), `.section--rule`
(filetto superiore). Filetti: `.rule` (hairline), `.rule--accent` (3rem × 2 px bronzo). Contenuti larghi
(tabelle, diagrammi) vanno in `.scroll-x`, mai in overflow di pagina.

---

## 7. Catalogo componenti (`templates/components/`)

26 file. Ogni componente è un include Django senza logica di business: riceve variabili di contesto
(`{% include "components/x.html" with a=… b=… %}`) e produce markup BEM stilato da `components.css`.
Regole comuni:

- **Testi prescritti**: passare il valore ottenuto con `{% locked "chiave" as var %}` e, se la lingua
  effettiva differisce da quella della pagina, `lang=` con il risultato di `{% locked_lang "chiave" %}`
  (quasi tutti i componenti accettano `lang`). Mai copiare il testo nel template.
- **HTML nei parametri** (`body`, `text`, `meta`, `actions`): l'autoescape resta attivo; chi passa HTML
  deve marcarlo sicuro a monte (`format_html`, `mark_safe` su contenuto già sanificato).
- **Link verso altre app**: `{% safe_url 'ns:name' as u %}` e rendere il link solo se `u` non è vuoto.
- **Icone**: `{% svg_icon "nome" "classi" %}` — decorative per default (`aria-hidden="true"`).
- «Usato in» elenca file presenti nell'albero di lavoro alla data della revisione (il test verifica che
  esistano e che contengano l'include o il blocco CSS; «e almeno altri N» è un minimo contato alla
  revisione, non un totale, così i template aggiunti dopo non lo rendono falso): i template dello Stage 1 sono committati, quelli di
  `templates/pages/`, `templates/ecosystem/` e `templates/portal/` appartengono allo Stage 2 e non lo sono
  ancora. Restano senza consumatore `accordion.html` (solo markup diretto), `dialog.html`,
  `institutional_banner.html`, `metadata_row.html` (solo markup diretto) e `tabs.html`: per questi
  l'esempio è ricavato dal contratto ed è dichiarato come tale.

#### `accordion.html`

- **Scopo**: domande/risposte e sezioni richiudibili; `<details>`/`<summary>` nativi.
- **Blocco CSS**: `.accordion` (`.accordion__item`, `.accordion__summary`, `.accordion__body`).
- **Contratto**: `items` = lista di dict `{id, title, body (HTML sicuro), open (bool), lang}`; `single`
  (True → un solo pannello aperto: attributo `name` nativo + fallback JS `data-accordion="single"`);
  `group` (valore di `name` quando `single`, default `accordion`).
- **Varianti**: nessun modificatore; l'icona `plus` ruota di 45° quando `[open]`.
- **Accessibilità**: ruolo, stato espanso/chiuso e tastiera (Invio/Spazio) forniti dal browser; funziona
  senza JS; `summary` alto almeno 56 px; `id` per item → permalink `#id`.
- **Usato in**: `templates/faq/_item.html`, `templates/faq/index.html` (markup diretto; usa
  `.accordion__panel` al posto di `.accordion__body` — G-19).
- **Esempio (dal contratto — nessun `{% include %}` allo Stage 1)**:

```django
{% include "components/accordion.html" with items=faq_items single=True group="faq-general" %}
```

#### `account_menu.html`

- **Scopo**: menu dell'utente autenticato nella barra istituzionale.
- **Blocco CSS**: `.account-menu` (`__summary`, `__name`, `__list`, `__link`, `__sep`).
- **Contratto**: nessuna variabile; legge `user` dal contesto. Le voci compaiono solo se la route esiste:
  `portal:dashboard`, `accounts:profile`, `mfa_index`, `account_logout` (via `safe_url`).
- **Varianti**: nessuna.
- **Accessibilità**: `<details data-dropdown>`; `main.js` sincronizza `aria-expanded` sul `summary`, chiude
  con Esc (focus di ritorno al `summary`), al click esterno e alla perdita di focus. Il logout è un
  `<form method="post">` con CSRF e un vero `<button>`, non un link GET. Il nome lungo è troncato con
  ellissi (`max-inline-size: 14rem`).
- **Usato in**: `templates/partials/utility_bar.html`.
- **Esempio reale — `templates/partials/utility_bar.html`**:

```django
{% if user.is_authenticated %}
  {% include "components/account_menu.html" %}
```

#### `badge.html`

- **Scopo**: etichetta di stato compatta (una riga, `white-space: nowrap`).
- **Blocco CSS**: `.badge`.
- **Contratto**: `label`; `kind` ∈ `neutral | info | success | warning | error | pending | primary`
  (opzionale); `icon` (nome icona, opzionale).
- **Varianti**: `.badge--info`, `.badge--success`, `.badge--warning`, `.badge--error`, `.badge--pending`,
  `.badge--primary`. `neutral` non ha regola propria: è l'aspetto di base (`--surface-2`, bordo
  `--border-subtle`).
- **Accessibilità**: il significato è nel testo, mai nel solo colore; coppie fg/bg ≥ 5.67:1 (§4).
- **Usato in**: `templates/portal/documents.html`, `templates/portal/messages.html`,
  `templates/portal/requests.html` (include); `templates/accounts/profile.html`,
  `templates/community/discussion.html`, `templates/allauth/elements/badge.html` (markup diretto
  `<span class="badge …">`).
- **Esempio reale — `templates/portal/documents.html`**:

```django
<td>{% include "components/badge.html" with label=doc.scan_label kind=doc.scan_kind %}</td>
```

#### `blockquote.html`

- **Scopo**: citazione istituzionale (es. `p1.companies.quote`).
- **Blocco CSS**: `.blockquote-institutional`.
- **Contratto**: `text` (la frase, virgolette incluse quando prescritte); `cite` (opzionale); `lang`.
- **Varianti**: nessuna. Filetto bronzo da 2 px sul lato `inline-start`, serif a `--font-size-h3`.
- **Accessibilità**: `<blockquote>` + `<cite>` semantici; `lang` per il fallback francese.
- **Usato in**: `templates/ecosystem/companies.html` (il testo prescritto e la sua lingua effettiva sono
  risolti da `ecosystem.services` tramite il registro, mai copiati nel template).
- **Esempio reale — `templates/ecosystem/companies.html`**:

```django
{% include "components/blockquote.html" with text=quote.text lang=quote.lang_attr %}
```

#### `breadcrumbs.html`

- **Scopo**: filo d'Arianna sotto l'header (blocco `breadcrumbs` di `base.html`).
- **Blocco CSS**: `.breadcrumbs` (il componente include già `.container`).
- **Contratto**: `breadcrumbs` = lista di `{"label": str, "url": str | ""}` fornita dalla view; l'ultimo
  elemento è la pagina corrente. «Accueil» è aggiunto automaticamente (`pages:home`).
- **Varianti**: nessuna. I separatori sono chevron disegnati in CSS (bordi ruotati), specchiati in RTL.
- **Accessibilità**: `<nav aria-label="Fil d’Ariane">` + `<ol>`; ultimo elemento `aria-current="page"` e
  non linkato; i separatori non sono contenuto (nessuna lettura «maggiore di»).
- **Usato in**: `templates/accounts/profile.html`, `templates/faq/index.html`,
  `templates/forum/index.html`, `templates/pathways/index.html`, `templates/news/index.html` (e almeno altri 37
  template).
- **Esempio reale — `templates/accounts/profile.html`**:

```django
{% block breadcrumbs %}{% include "components/breadcrumbs.html" %}{% endblock %}
```

#### `card.html`

- **Scopo**: teaser (notizie, schede). Da usare con parsimonia (§1.2).
- **Blocco CSS**: `.card` (`__eyebrow`, `__title`, `__text`, `__meta`).
- **Contratto**: `title`; `url` (opzionale: l'intera card diventa cliccabile); `eyebrow`; `text`; `meta`
  (str o HTML sicuro); `lang`; `flat` (True → senza box, solo filetto superiore).
- **Varianti**: `.card--link` (automatica con `url`: bordo `--color-primary-300` + `--shadow-sm` su
  hover/focus-within), `.card--flat`.
- **Accessibilità**: «stretched link» — lo pseudo-elemento del link del titolo copre la card, quindi c'è
  **un solo tab stop** e il nome accessibile è il titolo. Il titolo è sempre `<h3>`: collocare la card sotto
  un `h2`.
- **Usato in**: `templates/ecosystem/institutions.html`, `templates/ecosystem/companies.html`,
  `templates/ecosystem/pilot.html`, `templates/ecosystem/universities.html`,
  `templates/pages/home/_news.html` (include); `templates/pathways/training.html` (markup diretto `.card`).
- **Esempio reale — `templates/ecosystem/institutions.html`**:

```django
{% if links.partners %}<li>{% include "components/card.html" with flat=True url=links.partners title=_("Partenaires") text=_("Les organisations qui participent à l’écosystème.") %}</li>{% endif %}
```

#### `cta_panel.html`

- **Scopo**: invito all'azione a fine pagina; fascia tra due filetti o fascia blu.
- **Blocco CSS**: `.cta-panel` (`__inner`, `__title`, `__text`, `__actions`).
- **Contratto**: `title`; `text` (opzionale); `primary_label` + `primary_url`; `secondary_label` +
  `secondary_url` (opzionali); `lang`; `variant` (`"inverse"` → fascia blu, aggiunge `.on-inverse`).
- **Varianti**: `.cta-panel--inverse`. Bottoni: primario `.btn--primary.btn--arrow` (freccia specchiata in
  RTL), secondario `.btn--secondary`; in variante inverse entrambi ricevono `.btn--inverse`.
- **Accessibilità**: `<section aria-labelledby="cta-<slug del titolo>">` con `<h2>`. L'`id` deriva da
  `title|slugify`: due pannelli con lo stesso titolo, o un titolo interamente non latino (slug vuoto),
  producono `id` duplicati o ambigui — G-13: al massimo un CTA panel per pagina finché non è corretto.
- **Usato in**: `templates/ecosystem/universities.html`, `templates/ecosystem/institutions.html`,
  `templates/ecosystem/pilot.html` (include, un solo pannello per pagina);
  `templates/pathways/_orientation_cta.html` (markup diretto `.cta-panel`).
- **Esempio reale — `templates/ecosystem/universities.html`** (l'etichetta del bottone è un testo
  prescritto, passato tramite `{% locked … as %}`):

```django
{% locked "p3.universities.button" as button_label %}
{% include "components/cta_panel.html" with title=_("Proposer un partenariat") text=_("Présentez votre établissement et votre proposition : chaque demande est lue par l’équipe du projet.") primary_label=button_label primary_url=links.university_proposal %}
```

#### `dialog.html`

- **Scopo**: finestra modale per conferme e dettagli brevi. Mai per contenuti obbligatori o pubblicità.
- **Blocco CSS**: `.dialog` (`__header`, `__title`, `__close`, `__body`, `__actions`).
- **Contratto**: `id` (obbligatorio); `title`; `body` (HTML sicuro); `actions` (HTML sicuro dei bottoni,
  opzionale); `light` (True → il click sul backdrop chiude).
- **Varianti**: nessuna. Larghezza `min(100% − 2 × gutter, 36rem)`, altezza massima `min(85dvh, 44rem)`.
- **Accessibilità**: `<dialog>` nativo aperto con `showModal()`: focus trap, Esc e sfondo inerte sono della
  piattaforma; `aria-labelledby` → titolo; bottone di chiusura 44 × 44 px con `aria-label="Fermer"`;
  `main.js` porta il focus su `[data-dialog-focus]` o sul primo elemento focusabile e lo **restituisce
  all'elemento che ha aperto**. Senza JS il link `href="#id"` mostra il dialog come pannello via `:target`
  (in quel caso il bottone di chiusura non agisce: si esce con «indietro»).
- **Usato in**: nessun consumatore allo Stage 1.
- **Esempio (dal commento di contratto del componente)**:

```django
<a class="btn" href="#confirm-delete" data-dialog-open="confirm-delete">…</a>
{% include "components/dialog.html" with id="confirm-delete" title=dialog_title body=dialog_body actions=dialog_actions %}
```

#### `empty_state.html`

- **Scopo**: stato vuoto di liste e ricerche.
- **Blocco CSS**: `.empty-state` (`__icon`, `__title`, `__text`).
- **Contratto**: `title`; `text` (opzionale); `action_label` + `action_url` (opzionali); `icon` (default
  `document`).
- **Varianti**: nessuna. Bordo tratteggiato `--border-subtle`, centrato, largo al massimo 46rem.
- **Accessibilità**: `role="status"`; il titolo è un `<p>` (non altera la gerarchia dei titoli).
- **Usato in**: `templates/accounts/profile.html`, `templates/news/index.html`,
  `templates/glossary/index.html`, `templates/partners/index.html` (e almeno altri 19 template).
- **Esempio reale — `templates/accounts/profile.html`**:

```django
{% include "components/empty_state.html" with title=_("Aucune organisation") text=_("Votre compte n’est rattaché à aucune organisation pour le moment.") %}
```

#### `entrances.html`

- **Scopo**: i **quattro accessi** dell'ecosistema (Persona, Impresa, Istituzione, Università) — componente
  di livello hero della home di Fase 3. Esattamente quattro, mai di più (R-ECO-001).
- **Blocco CSS**: `.entrances` + `.entrance` (`__num`, `__icon`, `__illustration`, `__title`, `__text`,
  `__cta`).
- **Contratto**: `entrances` (opzionale) = lista di 4 dict `{title, text, button, url, icon, illustration,
  lang}`; se omessa il componente rende i quattro blocchi prescritti dal registro (`p3.entrances.*`) con le
  illustrazioni `static/img/illustrations/entrance-*.svg` e i link `pathways:index`,
  `ecosystem:companies`, `ecosystem:institutions`, `ecosystem:universities` (via `safe_url`: un accesso
  senza route è reso senza CTA). `heading_level` = `"h2"` (default) o `"h3"`.
- **Gate**: i testi `p3.*` sono di Fase 3 — **chi include il componente senza `entrances` deve farlo solo
  con `gates.phase3_public` aperto**.
- **Varianti**: 1 colonna → 2 (≥ 48rem) → 4 (≥ 72rem); colonne separate da filetti, nessun box;
  numerazione `01`–`04` da contatore CSS.
- **Accessibilità**: `<ol aria-label="Les quatre accès de l’écosystème">`; numeri e illustrazioni
  decorativi (`aria-hidden`, `alt=""`); stretched link: tutta la colonna è cliccabile ma l'unico elemento
  focusabile è la CTA (anello con `outline-offset: 4px`); `lang` sul singolo testo in fallback.
- **Usato in**: `templates/pages/home/_entrances.html`. La home passa sempre la lista `entrances` costruita
  da `pages.services` (testi di Fase 3 dal registro solo a gate aperto, testi interinali altrimenti) e
  `heading_level="h3"` perché il titolo di sezione è l'`h2`. La forma senza parametri, da usare solo dentro
  un controllo del gate `gates.phase3_public`, resta disponibile.
- **Esempio reale — `templates/pages/home/_entrances.html`**:

```django
{% include "components/entrances.html" with entrances=d.entrances heading_level="h3" %}
```

#### `form_errors.html`

- **Scopo**: riepilogo degli errori in cima al form (WCAG 3.3.1).
- **Blocco CSS**: `.form-errors` (sopra `.notice.notice--error`).
- **Contratto**: `form` (Django Form). Rende gli errori non di campo e una lista di link
  `#<id_for_label>` verso ogni campo visibile in errore.
- **Varianti**: nessuna.
- **Accessibilità**: `role="alert"`, `tabindex="-1"`, `id="form-errors"`: al caricamento `main.js`
  (`initFormErrorFocus`) vi porta il focus e lo scorre al centro del viewport, così dopo il ricaricamento
  lato server tastiera e screen reader ripartono dagli errori (G-05, chiusa il 20/09/2026). Senza JS il
  riepilogo resta in cima al form, con `role="alert"`. I link portano direttamente al controllo.
- **Usato in**: `templates/allauth/elements/form.html`.
- **Esempio reale — `templates/allauth/elements/form.html`**:

```django
{% if attrs.form %}{% include "components/form_errors.html" with form=attrs.form %}{% endif %}
```

#### `form_field.html`

- **Scopo**: **unico** modo di rendere un campo: etichetta, controllo, aiuto, errori.
- **Blocco CSS**: `.form-field` (`__label`, `__required`, `__help`, `__check`, `__errors`).
- **Contratto**: `field` (BoundField); `help` (sostituisce `help_text`); `consent` (True → stile del
  consenso obbligatorio, mai pre-spuntato; attivato anche dalla classe widget `consent-checkbox` di
  `core.forms.ConsentBooleanField`).
- **Varianti**: `.form-field--error` (bordo e filetto laterale `--color-error-fg`), `--required`,
  `--consent` (riquadro `--surface-2`). I widget nascosti sono resi nudi; il campo honeypot `website_url`
  va nel wrapper fuori schermo `.hp-wrap` con `aria-hidden="true"`.
- **Accessibilità**: contratto completo in `docs/ACCESSIBILITY.md` §6. In breve: `<label for>` sempre
  presente; asterisco `aria-hidden` + attributo `required`; Django 5.2 aggiunge `aria-invalid="true"` e
  `aria-describedby="<auto_id>_helptext <auto_id>_error"` e il componente usa **esattamente quegli id**;
  lista errori con `role="alert"`; checkbox con etichetta cliccabile a fianco.
- **Usato in**: `templates/allauth/elements/fields.html`, `templates/accounts/profile.html`,
  `templates/forum/partials/registration_form.html`, `templates/documents/upload.html` (e almeno altri 9).
- **Esempio reale — `templates/accounts/profile.html`**:

```django
{% for field in form.visible_fields %}{% include "components/form_field.html" with field=field %}{% endfor %}
```

#### `form_unavailable.html`

- **Scopo**: sostituisce **ogni** form pubblico finché il gate G2 (`core.gates.public_forms_enabled()`) è
  chiuso, cioè finché i testi legali ufficiali italiani non sono pubblicati.
- **Blocco CSS**: `.form-unavailable` (sopra `.notice.notice--pending`).
- **Contratto**: nessuna variabile; usa `site.contact_email` (unico indirizzo pubblico).
- **Varianti**: nessuna.
- **Accessibilità**: `role="status"`; icona `clock` decorativa; il messaggio offre sempre l'alternativa
  e-mail. Hook di test: `data-gate="forms-closed"`.
- **Usato in**: `templates/enquiries/contact.html`, `templates/enquiries/collaboration_proposal.html`,
  `templates/forum/register.html`, `templates/news/_newsletter.html`, `templates/community/join.html` (e
  almeno altri 6).
- **Esempio reale — `templates/enquiries/contact.html`**:

```django
{% if not forms_open or not form %}
  {% include "components/form_unavailable.html" %}
```

#### `hero.html`

- **Scopo**: apertura tipografica di pagina. Nessuna fotografia di porte/frontiere/passaporti (Impl. §3.1).
- **Blocco CSS**: `.hero` (`__content`, `__eyebrow`, `__rule`, `__title`, `__subtitle`, `__body`,
  `__actions`, `__figure`).
- **Contratto**: `title` (obbligatorio); `eyebrow`, `subtitle`, `body`; `lang`; `primary_label` +
  `primary_url`; `secondary_label` + `secondary_url`; `illustration` (percorso statico di un SVG
  decorativo → layout `.split`); `variant`; `heading_level` (`"h1"` default, `"p"` quando la pagina ha già
  il suo `h1`).
- **Varianti**: `.hero--editorial` (default: fondo caldo, filetto bronzo da 4rem), `.hero--inverse` (blu,
  aggiunge `.on-inverse`, bottoni `.btn--inverse`), `.hero--muted` (`--surface-2`), `.hero--compact`.
- **Accessibilità**: `<section aria-labelledby="hero-title">` — `id` fisso: **un solo hero per pagina**
  (G-13); filetto `aria-hidden`; illustrazione `alt=""`, `loading="eager"`, dimensioni esplicite (niente
  CLS); titolo limitato a 18ch.
- **Usato in**: `templates/pages/home/_hero.html` (markup diretto con le stesse classi `.hero`,
  `.hero--editorial`, `.hero__*`: la home sostituisce l'illustrazione con una fotografia responsiva nello
  slot `.hero__figure` e sceglie tra variante interinale e variante di Fase 3);
  `templates/pathways/detail.html` (solo l'elemento `.hero__figure`). Nessun `{% include %}` alla data
  della revisione.
- **Esempio (dal contratto)**:

```django
{% include "components/hero.html" with title=hero.title subtitle=hero.subtitle lang=hero.lang primary_label=hero.button primary_url=hero.url variant="editorial" %}
```

#### `institutional_banner.html`

- **Scopo**: fascia informativa sotto l'header (es. banner del Forum fino al 2 ottobre 2026, gate
  `forum_banner_visible()`), nel blocco `banner` di `base.html`. Non è un popup e non è dismissibile.
- **Blocco CSS**: `.institutional-banner` (`__inner`, `__title`, `__meta`, `__quote`, `__actions`).
- **Contratto**: `title`; `meta` (data/luogo), `quote`, `button_label` + `button_url` (opzionali); `lang`;
  `label` (aria-label della regione, default = `title`).
- **Varianti**: nessuna. Una colonna → tre colonne (≥ 64rem).
- **Accessibilità**: `<section role="region" aria-label>`; titolo come `<p>` (non entra nella gerarchia dei
  titoli); citazione in `<blockquote>`.
- **Usato in**: nessun consumatore alla data della revisione. Il banner del Forum sulla home non usa questo
  componente: il partial `_banner.html` della home (app `pages`) avvolge il partial dell'app `forum` in un blocco
  `.home-banner` con un bottone «Masquer cette annonce» aggiunto solo da JavaScript (§2.1); resta una
  fascia in flusso, mai un overlay.
- **Esempio (dal contratto)**:

```django
{% block banner %}{% if gates.forum_banner_visible %}{% include "components/institutional_banner.html" with title=banner.title meta=banner.meta quote=banner.quote button_label=banner.button button_url=banner.url lang=banner.lang %}{% endif %}{% endblock %}
```

#### `language_switcher.html`

- **Scopo**: cambio lingua (it, fr, en, ar) nella barra istituzionale.
- **Blocco CSS**: `.lang-switcher` (`__summary`, `__current`, `__list`, `__link`, `__code`).
- **Contratto**: nessuna variabile; usa `site.languages` (`code`, `name`, `url` = `translate_url` della
  pagina corrente, `active`, `dir`).
- **Varianti**: nessuna.
- **Accessibilità**: `<details data-dropdown>` (funziona senza JS); prefisso «Langue :» solo per screen
  reader; ogni link ha `lang`, `hreflang` e `dir` propri (la sintesi vocale cambia voce); lingua attiva
  `aria-current="true"` + grassetto + punto bronzo (non solo colore); codice lingua `aria-hidden`. Sono
  link, non un `<select>`: nessun cambio di contesto su input (SC 3.2.2).
- **Usato in**: `templates/partials/utility_bar.html`.
- **Esempio reale — `templates/partials/utility_bar.html`**:

```django
{% include "components/language_switcher.html" %}
```

#### `local_nav.html`

- **Scopo**: navigazione locale di una sezione (colonna laterale).
- **Blocco CSS**: `.local-nav` (`__title`, `__list`, `__link`).
- **Contratto**: `items` = lista di dict `{label, url, current (bool), children (stessa forma)}`; `title`
  (opzionale); `label` (aria-label, default = `title`).
- **Varianti**: desktop = colonna con filetto e voce corrente marcata in bronzo (avvolgerla in
  `.layout-sidebar__aside` per renderla sticky); sotto 64rem = lista di pill su `--surface-2`.
- **Accessibilità**: `<nav aria-label>`; voce corrente `aria-current="page"` + grassetto + filetto.
- **Usato in**: `templates/ecosystem/_layout.html`, `templates/pages/institutional_base.html`,
  `templates/portal/base_portal.html` (include); `templates/allauth/layouts/manage.html` (markup diretto
  `.local-nav`).
- **Esempio reale — `templates/ecosystem/_layout.html`**:

```django
<div class="layout-sidebar__aside ecosystem-layout__aside">
  {% include "components/local_nav.html" with items=local_nav_items title=_("Les espaces de l’écosystème") %}
```

#### `metadata_row.html`

- **Scopo**: riga di metadati (data, luogo, categoria, ultima revisione).
- **Blocco CSS**: `.meta-row` (`__item`).
- **Contratto**: `items` = lista di dict `{label, value, icon, datetime (ISO → <time>), url}`.
- **Varianti**: nessuna.
- **Accessibilità**: `<dl>` con coppie `<dt>`/`<dd>`; date in `<time datetime>`. Il separatore « : » dopo
  `<dt>` è contenuto CSS con tipografia francese, non localizzato (G-14).
- **Usato in**: `templates/pathways/_metadata_row.html` (markup diretto `.meta-row`).
- **Esempio (dal contratto)**:

```django
{% include "components/metadata_row.html" with items=event_meta %}
```

#### `notice.html`

- **Scopo**: messaggi in pagina (informazione, esito, avvertenza, errore, attesa, nota istituzionale).
- **Blocco CSS**: `.notice` (`__icon`, `__title`, `__body`); alias `.alert` per i messaggi Django.
- **Contratto**: `kind` ∈ `info | success | warning | error | pending | institutional` (default `info`);
  `title` (opzionale); `text` (str o HTML sicuro); `icon` (default per tipo: `info`, `check`, `warning`,
  `clock`); `lang`.
- **Varianti**: `.notice--info/success/warning/error/pending` (terne fg/bg/border dei token semantici,
  bordo `inline-start` da 4 px) e `.notice--institutional` (fascia `--surface-2` con filetto bronzo: natura
  informativa dei contenuti, gate).
- **Accessibilità**: `role="alert"` solo per `error`, `role="status"` per tutti gli altri; icona + titolo +
  bordo: il tipo non è mai comunicato dal solo colore.
- **Usato in**: `templates/community/discussion.html`, `templates/accounts/delete_request.html`,
  `templates/glossary/term.html`, `templates/living/sheet.html` (e almeno altri 18).
- **Esempio reale — `templates/community/discussion.html`**:

```django
{% translate "Discussion fermée : il n’est plus possible de répondre." as closed_text %}
{% include "components/notice.html" with kind="info" text=closed_text %}
```

#### `page_header.html`

- **Scopo**: intestazione standard delle pagine interne; contiene **l'unico `<h1>`**.
- **Blocco CSS**: `.page-header` (`__eyebrow`, `__title`, `__lead`, `__meta`); include `.container`.
- **Contratto**: `title`; `eyebrow`, `lead` (opzionali); `lang`; `meta` (HTML sicuro, es. una metadata
  row); `align` (`"center"`).
- **Varianti**: `.page-header--center`.
- **Accessibilità**: `<header>` di contenuto; titolo limitato a 22ch, lead a 60ch.
- **Usato in**: `templates/accounts/profile.html`, `templates/faq/index.html`,
  `templates/glossary/index.html`, `templates/partners/index.html` (e almeno altri 28).
- **Esempio reale — `templates/accounts/delete_request.html`**:

```django
{% include "components/page_header.html" with title=_("Supprimer mon compte") %}
```

#### `pagination.html`

- **Scopo**: paginazione «precedente / pagina n su N / successivo».
- **Blocco CSS**: `.pagination` (`__list`, `__link`, `__status`).
- **Contratto**: `page_obj` (Django `Page`); `query` (stringa urlencoded degli altri parametri). Non rende
  nulla se c'è una sola pagina.
- **Varianti**: nessuna.
- **Accessibilità**: `<nav aria-label="Pagination">`; link da 44 px con `rel="prev"`/`rel="next"`; stato
  testuale `aria-current="page"`; frecce `.icon--flip-rtl`.
- **Usato in**: `templates/news/index.html`, `templates/community/room.html`.
- **Esempio reale — `templates/news/index.html`**:

```django
{% include "components/pagination.html" with page_obj=page_obj query=query %}
```

#### `pathway_list.html`

- **Scopo**: lista editoriale numerata (gli 8 percorsi regolari).
- **Blocco CSS**: `.pathway-list` (`__item`, `__num`, `__title`, `__desc`, `__arrow`).
- **Contratto**: `items` = lista di dict `{title, text, url, lang}`; `lang` (per l'intera lista).
- **Varianti**: nessuna. Numeri `01`–`08` da contatore CSS (`decimal-leading-zero`); freccia nascosta sotto
  48rem.
- **Accessibilità**: `<ol>` (l'ordine è semantico); numeri `aria-hidden`; stretched link con un solo tab
  stop; titoli `<h3>`.
- **Usato in**: `templates/pages/home/_pathways.html` (include); `templates/pathways/index.html` (markup
  diretto `.pathway-list`).
- **Esempio reale — `templates/pages/home/_pathways.html`**:

```django
{% include "components/pathway_list.html" with items=d.pathway_items %}
```

#### `section_header.html`

- **Scopo**: intestazione tipografica di sezione (senza box).
- **Blocco CSS**: `.section__header` (`.section__title`, `.section__lead`, `.eyebrow`) — in `layout.css`.
- **Contratto**: `title` (reso come `<h2>`); `eyebrow`, `lead` (opzionali); `lang`; `align` (`"center"`);
  `id` (ancora per la navigazione di pagina).
- **Varianti**: `.section__header--center`.
- **Accessibilità**: `id` sul contenitore per `aria-labelledby`/ancore; `scroll-padding-block-start` evita
  che l'header sticky copra il titolo raggiunto via ancora.
- **Usato in**: `templates/ecosystem/companies.html`, `templates/ecosystem/institutions.html`,
  `templates/ecosystem/universities.html`, `templates/ecosystem/pilot.html`,
  `templates/pages/partials/_section_header.html` (include); `templates/pathways/detail.html` (markup
  diretto `.section__header`).
- **Esempio reale — `templates/ecosystem/companies.html`** (l'`id` è quello a cui punta
  `aria-labelledby` della sezione):

```django
<section id="demarche" class="ecosystem-section ecosystem-moments" aria-labelledby="demarche-header">
  {% include "components/section_header.html" with id="demarche-header" eyebrow=_("La démarche") title=_("Trois temps, une même démarche") %}
```

#### `stepper.html`

- **Scopo**: indicatore di avanzamento dei flussi a più passi (wizard di orientamento).
- **Blocco CSS**: `.stepper` (`__item`, `__marker`, `__label`) + `progress.progress` + `.progress-label`.
- **Contratto**: `steps` = lista di str; `current` = indice **a base 1** del passo corrente.
- **Varianti**: `.stepper__item--done` (marcatore verde `--color-secondary-800` con segno di spunta),
  `.stepper__item--current` (bordo 2 px blu, grassetto); verticale → orizzontale (≥ 48rem).
- **Accessibilità**: `<ol aria-label="Progression">`; passo corrente `aria-current="step"`; testo «Étape n
  sur N» sempre visibile; `<progress>` nativo (nessuno stile inline: CSP) con `aria-hidden="true"` perché
  duplica il testo. Lo stato non dipende dal colore: numero → spunta, spessore del bordo, grassetto.
- **Usato in**: `templates/pages/home/_orientation.html`, come sequenza esplicativa: con `current=0` nessun
  passo è «corrente» o «completato» e il foglio dell'app nasconde la riga «Étape n sur N» e la barra,
  perché lì nulla è in corso. In un flusso reale `current` parte da 1. Il wizard di orientamento ha per
  ora un indicatore proprio (`apps/orientation/static/orientation/wizard.css`, G-22).
- **Esempio reale — `templates/pages/home/_orientation.html`**:

```django
{% include "components/stepper.html" with steps=d.steps current=0 %}
```

#### `tabs.html`

- **Scopo**: schede per contenuti paralleli brevi. Non usare per contenuti che l'utente deve confrontare.
- **Blocco CSS**: `.tabs__list`, `.tabs__tab`, `.tabs__panel`, `.tabs__panel-title` (radice `.tabs`).
- **Contratto**: `tabs` = lista di dict `{id, label, body (HTML sicuro)}`; `id` (id del widget, default
  `tabs`: obbligatorio se ce n'è più d'uno in pagina); `remember` (chiave `localStorage`).
- **Varianti**: nessuna.
- **Accessibilità**: pattern WAI-ARIA Tabs ad attivazione automatica: `role="tablist"`/`tab`/`tabpanel`,
  `aria-selected`, `aria-controls`, `aria-labelledby`, roving `tabindex`, pannelli `tabindex="0"`; frecce
  (invertite in RTL), Home, Fine. `#id-pannello` nell'URL apre quella scheda. **Senza JS** la tablist è
  nascosta e tutti i pannelli sono impilati con il proprio `<h3>` (con JS quel titolo è solo per screen
  reader). `remember` oggi **scrive** la scelta ma non la rilegge (G-21).
- **Usato in**: nessun consumatore allo Stage 1.
- **Esempio (dal contratto)**:

```django
{% include "components/tabs.html" with tabs=training_tabs id="formation" %}
```

#### `timeline.html`

- **Scopo**: sequenza di tappe (progetto pilota in 8 passi, fasi di un percorso).
- **Blocco CSS**: `.timeline` (`__item`, `__marker`, `__label`, `__text`).
- **Contratto**: `steps` = lista di str **oppure** di dict `{label, text}`; `lang`; `label` (aria-label).
- **Varianti**: verticale (mobile) → 4 + 4 (≥ 48rem) → 8 in riga (≥ 80rem); porta già
  `.reveal.reveal--stagger`.
- **Accessibilità**: `<ol>`; numeri da contatore CSS con marcatori `aria-hidden`; le linee sono
  pseudo-elementi decorativi.
- **Usato in**: `templates/ecosystem/partials/pilot_flow.html`, `templates/ecosystem/companies.html`,
  `templates/pages/home/_pilot.html` (include); `templates/pathways/detail.html` (markup diretto
  `.timeline`).
- **Esempio reale — `templates/ecosystem/partials/pilot_flow.html`** (le otto etichette prescritte arrivano
  dal registro tramite `ecosystem.services`, con la loro lingua effettiva):

```django
{% include "components/timeline.html" with steps=flow.steps lang=flow.lang_attr label=_("Séquence proposée du projet pilote, étape par étape") %}
```

### 7.1 Pattern CSS senza file template

| Pattern | Classi | Note |
|---|---|---|
| Bottoni | `.btn` + `--primary`, `--secondary`, `--ghost`, `--link`, `--danger`, `--inverse` (anche `--inverse.btn--primary`), `--sm`, `--lg`, `--block`, `--upper`, `--arrow` | altezza minima 44 px (`--sm` 36 px, `--lg` 52 px); `:disabled` / `[aria-disabled="true"]` → opacità 0.55 e `pointer-events: none`; `.btn--upper` non applica il maiuscolo in arabo |
| Link con freccia | `.link-arrow` | CTA secondaria nelle liste; freccia `.icon--flip-rtl`, traslazione di 3 px su hover (invertita in RTL) |
| Icone | `.icon`, `--sm`, `--lg`, `--xl`, `--accent`, `--flip-rtl` | §10 |
| Messaggi Django | `.messages` > `.alert.alert--{tag}` | resi da `base.html` in una regione `role="status" aria-live="polite"`; `error` → `role="alert"` |
| Form | `.form`, `.form__fieldset`, `.form__legend`, `.form__intro`, `.form__required-note`, `.form__actions`, `.form-row.form-row--2`, `.input`, `.search-form` | il form completo è descritto in `docs/ACCESSIBILITY.md` §6 |
| Avanzamento | `progress.progress`, `.progress-label` | `<progress>` nativo, 6 px, pill |
| Sommario di pagina | `.section-nav` (`__list`, `__link`) + `data-section-nav` | barra sticky sotto l'header; `main.js` marca la sezione in vista con `aria-current="true"` |
| Pagine d'errore | `.error-page` (`__code`, `__title`, `__text`, `__ref`, `__actions`, `__links`) | `templates/errors/{400,403,404,410,429,500}.html` su `base_error.html`: un `h1`, codice decorativo `aria-hidden`, azioni di recupero, `nav aria-label="Navigation de secours"`; «Page précédente» è `.js-only` |
| Pagine account | `.account-page` (`--entrance`, `--manage`), `.account-page__card`, `.account-panel`, `.account-table` | `templates/allauth/layouts/*` e `templates/allauth/elements/*` mappano ogni elemento di django-allauth sul design system (bottoni, campi, alert, badge, tabelle in `.scroll-x`) |
| Pagina legale | `.legal-page`, `.legal-page__meta`, `.legal-page__courtesy` | misura di lettura `--container-prose` |
| Contatore | `.counter` + `data-counter` | opzionale; senza JS resta il valore statico |
| Segnaposto di sviluppo | `.dev-placeholder` | mai nel markup di produzione |

### 7.2 Shell (`templates/base.html` + `templates/partials/`)

| File | Contenuto |
|---|---|
| `base.html` | `<html lang dir class="no-js">`; preload font per direzione; preload dei cinque layer CSS; `main.css`; `head.js` sincrono; skip link; `utility_bar` → `header` → blocco `banner` → `<main id="main-content" tabindex="-1">` (blocco `breadcrumbs`, regione messaggi, `main_content` ⊃ `content`) → `footer`; `main.js` come modulo. Blocchi: `title`, `page_title`, `meta_description`, `head_seo`, `extra_head`, `jsonld`, `body_class`, `banner`, `breadcrumbs`, `main_content`, `content`, `extra_scripts` |
| `partials/utility_bar.html` | fascia blu `role="region" aria-label="Barre institutionnelle"`: promotore, link «Espace réservé» (flag `reserved_area_public_link` + `SiteSettings.reserved_area_enabled`) oppure menu account, selettore lingua |
| `partials/header.html` | header sticky: wordmark `{% brand %}` (o logo immagine se configurato in `SiteSettings`), bottone `Menu` (`data-nav-toggle`), drawer `#nav-drawer` con `<nav aria-label="Navigation principale">`, overlay |
| `partials/main_nav.html` | voci da `cms.MenuItem` (fallback statico in `apps/cms/templatetags/cms_nav.py`), filtrate da gate/flag e da route risolvibili; link + bottone disclosure + pannello per voce con figli |
| `partials/footer.html` | fascia blu `.on-inverse`: identità (wordmark dal registro, promotore, e-mail, dicitura del marchio in lettere per FR/IT), `nav` «Informations légales» con **cinque link distinti**, `nav` «Navigation du site», blocco progetto con link anti-frode solo se `gates.phase3_public`; riga finale con © e versione. Sede, RUNTS e codice fiscale sono `CONTENT_PENDING_LEGAL_REVIEW` (appartengono alle «Mentions légales» ufficiali) |
| `partials/seo_head.html` | canonical, `hreflang` per le 4 lingue + `x-default`, Open Graph, Twitter card, `theme-color` |

---

## 8. Pattern di navigazione

Il modello tastiera completo, con i criteri WCAG, è in `docs/ACCESSIBILITY.md` §3. Qui il disegno.

### 8.1 Mega-menu (≥ 80rem) — pattern «disclosure navigation»

Non è un `role="menubar"`: è una lista di link con bottoni di apertura, il modello raccomandato per la
navigazione di un sito (nessuna cattura dei tasti freccia dentro i pannelli, Tab sempre prevedibile).

- **Markup** (`partials/main_nav.html`): per ogni voce con figli `li[data-nav-item]` contiene il link di
  sezione `a[data-nav-link]` (o `span.main-nav__label` se la voce non ha una URL risolvibile), un
  `button[data-nav-panel-toggle]` con `aria-expanded` e `aria-controls="<id>-panel"` (testo nascosto
  «Ouvrir le sous-menu « … »») e il pannello `div[data-nav-panel]`. Le voci senza figli sono link semplici.
- **Pannello**: due colonne (titolo + descrizione + «Voir l’espace» | sottovoci), larghezza minima 36rem,
  filetto superiore bronzo da 2 px, `--shadow-lg`; centrato sotto la voce, allineato a `inline-end` per
  l'ultima voce (`.main-nav__item--end`); sottovoci su due colonne quando sono più di quattro.
- **Stato**: `data-open="true"` sul `li` + `aria-expanded="true"` sul bottone; un solo pannello aperto.
- **Tastiera**: Tab percorre link e bottoni nell'ordine del DOM; Invio/Spazio sul bottone apre il pannello
  e porta il focus sul primo elemento del pannello; **Esc** chiude e restituisce il focus al bottone;
  **←/→** (invertite in RTL) spostano il focus tra le voci di primo livello *che hanno un pannello*, con
  ritorno circolare; **↓** su una di quelle voci apre il pannello ed entra; uscendo con Tab dalla voce il
  pannello si chiude (`focusout`); click esterno chiude.
- **Voce corrente**: `aria-current="page"` (URL identica) o `"true"` (sezione antenata) + barra bronzo.
- **Senza JS**: il pannello appare su `:hover` e `:focus-within`.
- Verificato da `tests/frontend/test_browser.py::test_mega_menu_is_keyboard_operable`; screenshot
  `docs/qa/design/state-megamenu-open-fr-1440.png`, `docs/qa/design/state-megamenu-open-ar-1440.png`.

### 8.2 Drawer (< 80rem: telefono, tablet, laptop fino a 1279 px)

- Lo **stesso markup** del menu diventa un pannello `position: fixed` sotto l'header (`#nav-drawer`),
  aperto dal bottone «Menu» (`data-nav-toggle`, `aria-controls="nav-drawer"`, `aria-expanded`; icona
  `menu` ↔ `close`). Stato: `body[data-nav-open="true"]` (blocca anche lo scroll della pagina). Il bordo
  superiore del pannello è `var(--nav-drawer-top, var(--header-height))`: all'apertura `main.js` misura il
  bordo inferiore reale dell'header e lo scrive in `--nav-drawer-top`, perché l'header è a 72 px
  dall'alto solo quando è agganciato, e a 112 px finché la barra istituzionale è visibile.
- All'apertura il focus va sul primo elemento del drawer; **Esc** chiude e torna al bottone; Tab
  dall'ultimo elemento e Shift+Tab dal primo riportano al bottone (ciclo semplice); il click sull'overlay
  chiude; il passaggio alla larghezza desktop chiude tutto.
- I sotto-pannelli si aprono in linea con gli stessi bottoni (bersagli da 52 px); le sottovoci sono alte
  almeno 44 px.
- **Senza JS**: il bottone «Menu» è nascosto e il menu è reso per intero, in flusso, sotto il wordmark
  (`docs/qa/design/a11y-nojs-fr-390.png`, `docs/qa/design/a11y-nojs-fr-1024.png`). **Difetto aperto G-04**:
  in questa modalità l'header resta `position: sticky` e, con il menu dello Stage 2, misura 781 px: a
  390 × 844 restano 63 px di contenuto visibile, a 1024 × 768 nessuno.
- **Difetto aperto G-23**: l'overlay `.nav-overlay` parte ancora da `var(--header-height)` (72 px dall'alto
  del viewport), mentre con la barra istituzionale visibile il bordo inferiore dell'header è a 113 px: a
  pagina non scrollata il velo copre la fascia bassa dell'header, wordmark e bottone «Menu» compresi
  (`--nav-drawer-top` è impostata sul solo drawer e l'overlay, che ne è fratello, non la eredita).
- **G-02 (chiusa il 20/09/2026)**: il `backdrop-filter` era su `.site-header`, che diventava containing
  block del drawer `position: fixed` (65 px di altezza, overlay 0 px). Spostato sullo pseudo-elemento
  `.site-header::before` (§1.4). Misura dopo la correzione: drawer alto 731 px su 731 px disponibili a
  390 × 844 e 655 px su 655 px a 1024 × 768, overlay a tutto schermo —
  `docs/qa/design/state-drawer-open-fr-390.png`, `docs/qa/design/state-drawer-open-ar-390.png`,
  `docs/qa/design/state-drawer-open-fr-1024.png`, `docs/qa/design/state-drawer-open-ar-1024.png`.

### 8.3 Selettore lingua e menu account

`<details data-dropdown>` nella barra istituzionale: si aprono e si chiudono senza JS; `main.js` aggiunge
`aria-expanded`, chiusura con Esc (focus al `summary`), chiusura al click esterno e alla perdita di focus,
e ne tiene aperto uno solo per volta. Le lingue sono link `translate_url` della pagina corrente, non un
`<select>`. Schede: §7 `language_switcher.html`, `account_menu.html`.

### 8.4 Breadcrumb, navigazione locale, sommario di pagina, paginazione

| Pattern | Dove | Regola |
|---|---|---|
| Breadcrumb | blocco `breadcrumbs` di `base.html`, prima del contenuto | ogni pagina interna lo rende; «Accueil» automatico; ultimo elemento = pagina corrente, non linkata |
| Navigazione locale | `.layout-sidebar__aside` | colonna sticky ≥ 64rem, pill sotto; `aria-current="page"` |
| Sommario di pagina | `.section-nav[data-section-nav]` | ancore alle sezioni di una pagina lunga; sticky sotto l'header; scorrimento orizzontale su mobile |
| Paginazione | fine lista | precedente / «Page n sur N» / successivo |
| Footer | ogni pagina | due `nav` etichettate: cinque link legali distinti + navigazione del sito (stesse voci gate-aware del menu) |
| Skip link | primo elemento di `<body>` | «Aller au contenu principal» → `#main-content` (`docs/qa/design/state-skiplink-fr-390.png`) |

---

## 9. Motion

Regola: il movimento **spiega un cambio di stato**; non decora. Tutte le durate vengono dai token, quindi
`prefers-reduced-motion: reduce` le azzera in blocco; in più `components.css` §29 forza
`transition-duration` e `animation-duration` a `0.01ms`, `animation-iteration-count: 1`,
`scroll-behavior: auto`, e disattiva i keyframe di mega-menu e dialog.

| Elemento | Cosa si anima | Durata · curva | Innesco | Con reduced motion |
|---|---|---|---|---|
| Link | `color`, `text-decoration-color` | `--duration-fast` · `--ease-standard` | hover | istantaneo |
| Bottoni `.btn` | sfondo, colore, bordo; `translateY(1px)` su `:active` | `--duration-fast` · `--ease-standard` | hover / pressione | istantaneo |
| Frecce (`.btn--arrow`, `.link-arrow`, `.entrance__cta`, `.pathway-list__arrow`) | `translateX(3–4px)` (negativo in RTL) | `--duration-base` · `--ease-out` | hover / focus | istantaneo |
| Voce del menu | barra bronzo `scaleX(0→1)` (il CSS dichiara `transform-origin: start`, valore non valido e quindi ignorato: la barra cresce dal centro) | `--duration-base` · `--ease-out` | hover / corrente / aperta | istantaneo |
| Chevron di menu, lingua | `rotate(180deg)` | `--duration-fast` · `--ease-standard` | apertura | istantaneo |
| Pannello mega-menu | keyframe `menu-in` / `menu-in-rtl` / `menu-in-end`: opacità + 6 px | `--duration-base` · `--ease-out` | apertura | `animation: none` |
| Drawer + overlay | `transform` (8 px), `opacity`, `visibility` | `--duration-base` · `--ease-out` | bottone Menu | istantaneo |
| Accordion | icona `plus` `rotate(45deg)` (il pannello non è animato) | `--duration-base` · `--ease-out` | apertura | istantaneo |
| Entrance, pathway item | `background-color` | `--duration-base` · `--ease-standard` | hover / focus-within | istantaneo |
| Card cliccabile | `border-color`, `box-shadow` | `--duration-base` · `--ease-standard` | hover / focus-within | istantaneo |
| Campi dei form | `border-color`, `box-shadow` | `--duration-fast` · `--ease-standard` | hover / focus | istantaneo |
| `<progress>` | larghezza del valore (solo WebKit/Blink) | `--duration-slow` · `--ease-out` | cambio passo | istantaneo |
| Dialog | keyframe `dialog-in`: opacità + 8 px | `--duration-base` · `--ease-out` | `showModal()` | `animation: none` |
| Skip link | `translateY(-200% → 0)` | `--duration-fast` · `--ease-out` | focus | istantaneo |
| `.reveal` | opacità 0→1 + `translateY(var(--reveal-distance))` | `--duration-reveal` · `--ease-out` | ingresso nel viewport (IntersectionObserver, soglia 0.08, una sola volta) | contenuto visibile da subito, nessuna transizione; `main.js` aggiunge `.is-visible` a tutti senza osservare |
| `.counter[data-counter]` | conteggio numerico in 900 ms (`requestAnimationFrame`, ease-out cubica) | fisso in JS | ingresso nel viewport | valore finale scritto subito |
| Scroll verso ancora | `scroll-behavior: smooth` | del browser | click su ancora | `auto` |
| Scroll verso il riepilogo errori | `scrollIntoView({ block: "center", behavior: "smooth" })` | del browser | caricamento di una pagina che contiene `#form-errors` | `behavior: "auto"` |

Garanzie di `.reveal`: si applica **solo** sotto `html.js`; senza JS il contenuto non è mai nascosto; se
`IntersectionObserver` manca tutto diventa visibile; rete di sicurezza a 2.5 s che rende visibile qualunque
elemento rimasto nascosto (stampa, zoom). `opacity: 0` non toglie il contenuto dall'albero di accessibilità:
per uno screen reader il testo c'è da subito. `test_no_horizontal_overflow_and_screenshots` pretende zero
`.reveal` a opacità 0 subito dopo `networkidle`: **un blocco `.reveal` sotto la piega non lo soddisfa**
(resta a opacità 0 finché non entra nel viewport o non scatta la rete di sicurezza). È successo durante lo
sviluppo della home dell'app `pages`; alla revisione il test passa e `docs/qa/design/capture-report.json`
registra 0 elementi nascosti al caricamento su tutte le 43 catture. Regola pratica: `.reveal` solo su
blocchi che al caricamento sono già nel viewport o subito sotto; mai su contenuto essenziale lontano
dalla piega. `.reveal--stagger` imposta `--reveal-index` (max 8) e un
`transition-delay` di 60 ms × indice sui figli: oggi il gruppo sfuma comunque come un blocco unico, perché i
figli non hanno una transizione di opacità propria (G-20).

Non esistono: animazioni in loop, parallax, autoplay, carousel, animazioni su scroll continuo, video di
sfondo.

---

## 10. Iconografia

- **Un solo set**: icone al tratto originali, griglia 24 × 24, tratto 1.5 (1.25 per `.icon--xl`, 1.1 per
  `.entrance__icon`), estremità e giunzioni arrotondate, nessun riempimento. Niente emoji, niente
  librerie di terzi, niente mescolanze (R-DES-009).
- **Uso**: `{% svg_icon "nome" %}` → `<svg class="icon" aria-hidden="true" focusable="false"><use
  href="/static/img/icons.svg#icon-nome"></use></svg>`. Secondo argomento = classi; terzo = etichetta
  (`role="img"` + `aria-label`, al posto di `aria-hidden`). Colore = `currentcolor`; dimensioni dai token
  `--icon-size` (20 px), `--icon-size-sm` (16 px), `--icon-size-lg` (28 px), `.icon--xl` 40 px.
- **Decorativa per default**: accanto a un testo l'icona è nascosta alle tecnologie assistive; un controllo
  con la sola icona deve avere testo `.visually-hidden` (bottoni del menu) o `aria-label` (chiusura del
  dialog).
- **Direzionalità**: `arrow` e `chevron-end` indicano «avanti» e ricevono `.icon--flip-rtl`
  (`transform: scaleX(-1)` sotto `[dir="rtl"]`). Non si specchiano: `chevron` (giù), `arrow-up-right`
  (uscita), `check`, `search`, `clock`, `quote` e ogni icona non direzionale.
- **Colore d'accento**: `.icon--accent` o il colore del contesto (`--color-accent-600`: 3.83:1 sul fondo,
  4.00:1 su `--surface-1`, sufficiente per oggetti grafici).

Elenco completo degli `id` dello sprite (`static/img/icons.svg`, prefisso `icon-`):

<!-- icon-list:start -->
36 icone.

| Gruppo | Icone |
|---|---|
| Accessi e soggetti | `person`, `user`, `building`, `institution`, `university`, `briefcase`, `handshake` |
| Direzione e navigazione | `arrow`, `arrow-up-right`, `chevron`, `chevron-end`, `menu`, `close`, `plus`, `minus`, `home`, `list`, `compass`, `map-pin`, `globe`, `search` |
| Stato e feedback | `check`, `warning`, `info`, `shield`, `clock`, `calendar` |
| Contatto e documenti | `mail`, `phone`, `document`, `download`, `quote` |
| Account e sicurezza | `lock`, `key`, `logout`, `settings` |
<!-- icon-list:end -->

> **G-01 (chiusa il 20/09/2026).** Alla prima stesura `static/img/icons.svg` non era XML ben formato: il
> commento iniziale conteneva la sequenza `--` (nel nome della classe `.icon--flip-rtl`), vietata dentro un
> commento XML. Il browser scaricava il file (HTTP 200, `image/svg+xml`) ma non lo interpretava e **nessuna
> icona veniva disegnata su nessuna pagina**. L'owner ha riformulato il commento; verifica in Chromium:
> `DOMParser` senza `parsererror` e, nel report `docs/qa/design/capture-report.json`, 546 icone disposte
> sulle 43 catture, 0 vuote (`emptyIcons`). Regressione impedita da
> `tests/frontend/test_design_docs.py::test_icon_sprite_is_well_formed_xml`, da
> `tests/frontend/test_svg_wellformed.py::test_svg_is_wellformed_xml` (ogni SVG sotto `static/`) e da
> `capture.py`, che esce con codice 1 se un'icona disposta non disegna nulla.

---

## 11. Illustrazioni e fotografia

### 11.1 Illustrazioni (`static/img/illustrations/`)

Sei SVG originali al tratto, coerenti con le icone: tratto 1.4 in `#0f2b52`, accenti `#9a7b2f` (bronzo) e
`#1f6b48` (verde), linea d'orizzonte bronzo, nessun riempimento salvo i nodi in `#fbfaf7`. Ogni file ha
`role="img"` e un `<title>`; nei componenti sono **decorativi** (`alt=""`) perché il testo accanto dice già
tutto.

| File | viewBox | Soggetto |
|---|---|---|
| `entrance-person.svg` | 160 × 120 | figura e percorso a tappe |
| `entrance-company.svg` | 160 × 120 | edifici e lista di fabbisogni |
| `entrance-institution.svg` | 160 × 120 | portico generico (nessun emblema) e due archi di dialogo |
| `entrance-university.svg` | 160 × 120 | libro aperto e tocco accademico |
| `orientation.svg` | 240 × 160 | domande, ramificazione, bussola |
| `pilot-flow.svg` | 640 × 160 | otto nodi su una linea ascendente tra due territori |

I colori sono scritti nei file SVG (sono immagini, non CSS): se i token `--color-primary-900`,
`--color-accent-600`, `--color-secondary-800` o `--surface-0` cambiano, le illustrazioni vanno aggiornate a
mano. `favicon.svg` segue la stessa regola; `og-default.png` (1200 × 630) è l'immagine di condivisione.

### 11.2 Fotografia

Registro, licenze e pipeline: `docs/IMAGE_LICENSES.md` (15 fotografie, Unsplash License, scaricate e
servite dal nostro dominio). Direzione artistica (Impl. §3.1 Note):

- **Soggetti ammessi**: imprese e luoghi di lavoro, persone in formazione, aule, università e biblioteche,
  sale istituzionali e di conferenza, cooperazione e riunioni di lavoro, workshop, professionisti,
  relazioni internazionali, Italia contemporanea. Luce naturale, inquadrature sobrie, nessuna posa da
  stock «stretta di mano in controluce».
- **Soggetti vietati**: porte e soglie, frontiere, valigie, file e code, passaporti, aeroporti, griglie e
  cancelli, iconografia stereotipata della migrazione, cliché turistici (Colosseo, gondole…), loghi o
  testi di terzi, prodotti riconoscibili. Il vocabolario vietato è verificato su slug, alt e titoli da
  `apps/cms/tests/test_media_assets.py`.
- **Slot d'uso** (`cms.MediaAsset.usage_slot`): `hero`, `entrance_person`, `entrance_company`,
  `entrance_institution`, `entrance_university`, `forum_event`, `training_classroom`, `university`,
  `workshop`, `news_default`, `orientation`, `living`, `reserved_area`, `cooperation`, `academic`.
- **Tecnica**: derivati WebP a 480 / 960 / 1440 / 1920 px (mai upscaling) + JPEG 1440 px di fallback,
  ciascuno ≤ 350 KB, metadati rimossi; `<picture>` con `<source type="image/webp" srcset>` e `<img>` con
  `width`/`height` espliciti, `loading="lazy"` sotto la piega, `decoding="async"`. Mai un host esterno
  (CSP `img-src 'self' data:`).
- **Testo alternativo**: `MediaAsset.alt(lang)`; la sorgente è `alt_fr`, le altre lingue restano vuote
  finché non arrivano dai traduttori (mai traduzione automatica) — in quel caso l'alt francese va marcato
  con `lang="fr"`. Immagini puramente decorative: `alt=""`.
- **Ruolo nel layout**: la fotografia accompagna il testo, non lo sostituisce. Sulla home la fotografia dello
  slot `hero` sta nella colonna `.hero__figure`, a fianco del titolo (layout `.split`, sotto il testo su
  mobile); le pagine interne aprono con `page_header.html`, senza immagine. Nessun testo è mai sovrapposto
  a una foto (contrasto non garantibile).

Esempio reale — `templates/news/detail.html`:

```django
<figure class="article__figure">
  <picture>
    <img class="article__image" src="{{ article.hero_image.file.url }}" alt="{{ hero_alt }}"{% if article.hero_image.width %} width="{{ article.hero_image.width }}" height="{{ article.hero_image.height }}"{% endif %} decoding="async" sizes="(min-width: 72rem) 72rem, 100vw">
  </picture>
```

---

## 12. RTL (arabo)

1. **Direzione dal server**: `<html lang="ar" dir="rtl">` e `body.is-rtl` (`core.context_processors.site`).
2. **Solo proprietà logiche**: `margin-inline-*`, `padding-inline-*`, `inset-inline-*`, `border-inline-*`,
   `inline-size` / `block-size`, `text-align: start | end`. Non esiste un solo `left` / `right` fisico in
   `base.css` e `layout.css`; in `components.css` compaiono unicamente nella posizione dello chevron del
   `<select>` (`background-position`, con la regola `[dir="rtl"]` speculare).
3. **Regole `[dir="rtl"]` esistenti** (tutte semantiche): `.icon--flip-rtl`; traslazioni su hover di
   `.btn--arrow`, `.link-arrow`, `.entrance__cta`, `.pathway-list__arrow`; centratura e keyframe del
   mega-menu (`menu-in-rtl`); ombra interna della sottovoce corrente; rotazione del separatore dei
   breadcrumb; chevron del `<select>`; helper bidi.
4. **Convenzione `.icon--flip-rtl`**: va messa su ogni icona che significa «avanti / indietro» (`arrow`,
   `chevron-end`). Non va messa su icone che non indicano una direzione di lettura.
5. **Dati latini dentro una pagina araba**: `direction: ltr; unicode-bidi: isolate` per `.ltr`,
   `.brand__wordmark`, `.email`, `.phone`, `code`, `time[datetime]` e per gli input `email`, `tel`, `url`,
   `number`, `password` (questi ultimi con `text-align: end`, così il cursore resta dal lato atteso).
6. **Tipografia**: IBM Plex Sans Arabic per titoli e testo; niente maiuscolo e niente `letter-spacing`
   (spezzerebbe le legature).
7. **Tastiera**: frecce ←/→ invertite nel mega-menu e nelle tab (`document.documentElement.dir`).
8. **Verifica**: `tests/frontend/test_browser.py` (nessun overflow orizzontale a 360 / 768 / 1440 in `ar`),
   `tests/compliance/test_public_pages.py::test_arabic_is_rtl_and_others_ltr`; screenshot
   `docs/qa/design/home-ar-390.png`, `docs/qa/design/login-ar-1440.png`, `docs/qa/design/404-ar-768.png`.
9. **Difetto aperto G-03**: le stringhe d'identità in caratteri latini che non portano `.brand__wordmark`
   (wordmark del footer, nome del promotore nella barra e nel footer, riga del ©) non sono isolate: in
   arabo il footer mostra «™Italy Legal Entry» e la barra tronca l'inizio del nome del promotore
   (`docs/qa/design/a11y-zoom400-ar-320.png`).

`docs/I18N_RTL.md`, citato nei commenti di `tokens.css` e `base.css` e nell'intestazione dei cataloghi
`locale/`, non esisteva ancora alla data della revisione (G-16; è in carico al flusso i18n). Finché manca,
questa sezione e `docs/ACCESSIBILITY.md` §10 sono il riferimento; quando arriva, per traduzioni e
procedure RTL prevale quel documento e qui restano le sole regole di disegno.

---

## 13. Moduli JS e progressive enhancement

Due file, nessuna dipendenza, nessun bundler, ≈ 18 KB non compressi in totale.

| File | Caricamento | Ruolo |
|---|---|---|
| `static/js/head.js` | `<script src>` sincrono in `<head>` | una riga: sostituisce `no-js` con `js` su `<html>` prima del primo paint. È un file esterno perché la CSP è `script-src 'self'` senza nonce. |
| `static/js/main.js` | `<script type="module">` a fine `<body>` | modulo ES senza `import`; esporta `init`; ogni comportamento si aggancia a un attributo `data-*`; nessun testo nel JS (tutte le stringhe restano nell'HTML tradotto dal server). |

Inventario di `main.js` (funzioni chiamate da `init()`):

| Funzione | Hook | Cosa aggiunge | Cosa funziona comunque senza JS |
|---|---|---|---|
| `initFormErrorFocus` | `#form-errors` (l'`id` reso da `components/form_errors.html`) | dopo un invio non valido porta il focus sul riepilogo degli errori (`focus({ preventScroll: true })`) e lo scorre al centro del viewport, senza animazione con reduced motion | il riepilogo è comunque in cima al form, con `role="alert"` e un link per ogni campo in errore |
| `initNavigation` | `data-nav-toggle`, `data-nav-drawer`, `data-nav-overlay`, `data-nav-item`, `data-nav-link`, `data-nav-panel-toggle`, `data-nav-panel` | drawer, mega-menu, `aria-expanded`, Esc, frecce, chiusura su `focusout`/click esterno, ciclo del focus nel drawer | menu interamente visibile sotto 80rem (in flusso dentro l'header: vedi G-04); pannelli su hover/focus-within da 80rem in su; tutti i link raggiungibili |
| `initDropdowns` | `details[data-dropdown]` | `aria-expanded`, Esc, click esterno, perdita di focus, uno aperto per volta | `<details>` si apre e si chiude nativamente |
| `initAccordions` | `data-accordion="single"` | esclusività per i browser senza `<details name>` | accordion pienamente funzionante (più pannelli aperti insieme) |
| `initTabs` | `data-tabs`, `data-tabs-remember` | tab ARIA, roving tabindex, frecce/Home/Fine, apertura da `#hash` | pannelli impilati con il proprio titolo; tablist nascosta |
| `initSteppers` | `data-stepper`, `data-step`, `data-step-marker`, `data-step-next`, `data-step-prev`, `data-step-current`, `data-step-focus` | pannelli lato client, `aria-current="step"`, focus sul titolo del passo | tutti i passi visibili in sequenza (il wizard di orientamento è comunque server-side) |
| `initReveal` | `.reveal`, `.reveal--stagger` | comparsa allo scroll | contenuto sempre visibile |
| `initDialogs` | `data-dialog-open`, `data-dialog-close`, `data-dialog-focus`, `data-dialog-light` | `showModal()`, focus iniziale, focus di ritorno, chiusura dal backdrop | il link `#id` mostra il dialog come pannello via `:target` |
| `initCounters` | `data-counter`, `data-counter-format` | conteggio animato | valore statico nell'HTML |
| `initMisc` | `data-history-back`, `form[data-single-submit]`, `data-section-nav` | «pagina precedente», blocco del doppio invio (`disabled` + `aria-disabled`), `aria-current` sul sommario di pagina | il link «indietro» è `.js-only`; il form si invia normalmente |

`localStorage` è usato solo da `initTabs` (chiave `tabs:<remember>`, indice numerico della scheda): nessun
dato personale, nessun identificatore; è memoria tecnica, non un cookie di tracciamento. Fuori da
`static/js/`, gli script delle app sono elencati in §2.1: `home.js` usa `sessionStorage` (chiave
`ile.dismissed.<id>`, valore `1`) per ricordare nella sola scheda corrente che il banner della home è stato
nascosto — stessa natura tecnica, nessun dato inviato al server.

Verifica senza JS: `docs/qa/design/a11y-nojs-fr-390.png` e `docs/qa/design/a11y-nojs-fr-1440.png`
(Playwright con `java_script_enabled=False`).

---

## 14. Come estendere il sistema

### 14.1 Aggiungere un token

1. Verificare che non esista già (molti token sono «riserva») e che il bisogno non sia locale: un valore
   usato da un solo componente è una custom property di componente (`--btn-bg`), non un token.
2. Aggiungerlo in `tokens.css` nella famiglia giusta, rispettando i prefissi (`--color-*`, `--text-*`,
   `--surface-*`, `--border-*`, `--font-size-*`, `--space-*`, …) e la griglia (spazi multipli di 4 px).
3. Se è un colore usato per testo o per il perimetro di un controllo: aggiungere la coppia a
   `CONTRAST_PAIRS` in `tests/frontend/test_static_assets.py` e una riga alla tabella di §4.
4. Documentarlo nella tabella di §3 (token, valore letterale, risolto, uso):
   `tests/frontend/test_design_docs.py` fallisce finché token e documento non coincidono.
5. Se dipende dalla lingua o dal movimento, aggiungere l'override in `:lang(ar)` o nel blocco
   `prefers-reduced-motion` e documentarlo in §3.18.

### 14.2 Aggiungere un componente

1. Prima cercare nel catalogo (§7) e nei pattern CSS (§7.1): estendere con un modificatore è quasi sempre
   meglio di un nuovo blocco. Un nuovo box va giustificato contro §1.2.
2. Creare `templates/components/<nome>.html` con un **commento di contratto** in testa (ogni variabile,
   obbligatoria o no, e cosa succede senza JS). Nessuna logica di business, nessun testo prescritto copiato,
   stringhe UI in francese dentro `{% translate %}`, link ad altre app via `safe_url`.
3. CSS in una nuova sezione numerata di `components.css`: BEM, solo token, solo proprietà logiche, stati via
   attributi ARIA, bersagli ≥ 44 px (`--control-height`), focus ereditato da `:focus-visible` (non
   ridefinirlo senza motivo), comportamento RTL pensato subito.
4. JS solo se migliora un markup che già funziona: nuova funzione `init…` in `main.js`, hook `data-*`,
   nessun handler inline, rispetto di `REDUCED_MOTION`.
5. Accessibilità: elemento nativo prima di ARIA; nome accessibile per ogni controllo; tastiera completa;
   testare a 320 px, in arabo e senza JS.
6. Documentare: scheda in §7 con lo stesso schema (scopo, blocco CSS, contratto, varianti, accessibilità,
   usato in, esempio) e riga nel modello tastiera di `docs/ACCESSIBILITY.md` §3 se è interattivo. Il test
   fallisce se un file in `templates/components/` non ha la sua scheda (e viceversa).

### 14.3 Aggiungere un'icona

Disegnarla sulla griglia 24 × 24 con tratto 1.5 e terminali arrotondati, senza `fill`/`stroke` nel file;
aggiungere `<symbol id="icon-<nome>" viewBox="0 0 24 24">` in `static/img/icons.svg`; **validare il file
come XML** (mai `--` dentro un commento); aggiungere il nome all'elenco di §10. Se indica una direzione di
lettura, usarla sempre con `.icon--flip-rtl`.

---

## 15. Screenshot QA (`docs/qa/design/`)

Generati il 20/09/2026 da `docs/qa/design/capture.py` (Playwright, Chromium, `device_scale_factor=1`) contro
il server di sviluppo locale con `DJANGO_DEBUG=False` (altrimenti Django mostra la propria pagina 404
tecnica), su un **database dedicato** (`DATABASE_URL` proprio, `migrate` + `seed_all`: il database di
sviluppo condiviso non va né migrato né popolato da chi cattura, e se non è allineato la home risponde 500);
data di sistema 20/09/2026, quindi gate di Fase 3 chiuso e form pubblici chiusi (G2). Rigenerati dal
revisore lo stesso giorno, dopo l'arrivo dei cataloghi `locale/` (le catture arabe mostrano l'interfaccia
tradotta) e di nuovo dopo le correzioni di G-01 e G-02 e lo spostamento del breakpoint della navigazione a
80rem: **le catture a 768 px mostrano quindi il bottone «Menu», non il mega-menu**. Il report
`docs/qa/design/capture-report.json` registra per ogni cattura stato HTTP, `dir`, numero di `h1`, overflow
orizzontale, richieste esterne, blocchi `.reveal` nascosti, icone disposte e icone vuote; le catture del
drawer aggiungono la geometria del pannello (`drawer`) e quelle senza JavaScript la geometria dell'header
(`header`, evidenza di G-04): **43 catture, stato HTTP atteso ovunque (200; 404 per la pagina
inesistente), 0 overflow, 0 richieste esterne, un solo `h1` per pagina, 0 blocchi `.reveal` nascosti al
caricamento, 0 icone vuote**. Lo script esce con codice 1 se una di queste condizioni non è rispettata
(compreso uno stato HTTP inatteso: una pagina d'errore non viene scambiata per una cattura valida). I PNG
sono git-ignorati: rigenerarli in locale.

| Pagina | Francese (LTR) | Arabo (RTL) |
|---|---|---|
| Home — stato dell'app `pages` (in sviluppo, non ancora committata) al momento della cattura: hero interinale con fotografia, banner del Forum, quattro accessi, orientamento, percorsi, trasparenza, promotore | `docs/qa/design/home-fr-390.png`, `docs/qa/design/home-fr-768.png`, `docs/qa/design/home-fr-1440.png` | `docs/qa/design/home-ar-390.png`, `docs/qa/design/home-ar-768.png`, `docs/qa/design/home-ar-1440.png` |
| `/privacy-policy/` — pagina legale bloccata (gate G1) | `docs/qa/design/privacy-fr-390.png`, `docs/qa/design/privacy-fr-768.png`, `docs/qa/design/privacy-fr-1440.png` | `docs/qa/design/privacy-ar-390.png`, `docs/qa/design/privacy-ar-768.png`, `docs/qa/design/privacy-ar-1440.png` |
| `/compte/login/` — allauth sul design system | `docs/qa/design/login-fr-390.png`, `docs/qa/design/login-fr-768.png`, `docs/qa/design/login-fr-1440.png` | `docs/qa/design/login-ar-390.png`, `docs/qa/design/login-ar-768.png`, `docs/qa/design/login-ar-1440.png` |
| `/page-inexistante/` — 404 | `docs/qa/design/404-fr-390.png`, `docs/qa/design/404-fr-768.png`, `docs/qa/design/404-fr-1440.png` | `docs/qa/design/404-ar-390.png`, `docs/qa/design/404-ar-768.png`, `docs/qa/design/404-ar-1440.png` |

| Stato / variante | File |
|---|---|
| Skip link con focus | `docs/qa/design/state-skiplink-fr-390.png`, `docs/qa/design/state-skiplink-ar-390.png` |
| Drawer aperto a 390 px e a 1024 px (sotto 80rem; G-02 chiusa: il pannello arriva in fondo allo schermo) | `docs/qa/design/state-drawer-open-fr-390.png`, `docs/qa/design/state-drawer-open-ar-390.png`, `docs/qa/design/state-drawer-open-fr-1024.png`, `docs/qa/design/state-drawer-open-ar-1024.png` |
| Mega-menu aperto da tastiera, focus nel pannello | `docs/qa/design/state-megamenu-open-fr-1440.png`, `docs/qa/design/state-megamenu-open-ar-1440.png` |
| Focus su un campo | `docs/qa/design/state-focus-field-fr-1440.png`, `docs/qa/design/state-focus-field-ar-1440.png` |
| Form con errori (riepilogo + errori di campo) | `docs/qa/design/state-form-errors-fr-390.png`, `docs/qa/design/state-form-errors-ar-390.png` |
| `prefers-reduced-motion: reduce` | `docs/qa/design/a11y-reduced-motion-fr-1440.png` |
| Zoom 200 % (1280 px → 640 px CSS) | `docs/qa/design/a11y-zoom200-fr-640.png` |
| Zoom 400 % (1280 px → 320 px CSS) | `docs/qa/design/a11y-zoom400-fr-320.png`, `docs/qa/design/a11y-zoom400-ar-320.png` |
| JavaScript disattivato (a 390 e 1024 px mostra G-04: il menu in flusso dentro l'header sticky) | `docs/qa/design/a11y-nojs-fr-390.png`, `docs/qa/design/a11y-nojs-fr-1024.png`, `docs/qa/design/a11y-nojs-fr-1440.png` |

Nella stessa cartella `tests/frontend/test_browser.py` scrive le proprie catture a 360 / 768 / 1440
(`<pagina>-<lingua>-{mobile,tablet,desktop}.png` e `nav-open-*`).

---

## 16. Difetti noti del design system

Rilevati il 20/09/2026 leggendo il codice e misurando in Chromium. L'elenco completo, con criterio WCAG,
evidenza, correzione proposta e modalità di verifica in QA, è in `docs/ACCESSIBILITY.md` §13; qui i difetti
che toccano il design system. Nessuno dei file coinvolti appartiene a questo incarico: le correzioni sono
state richieste agli owner. Una riga «chiusa» resta in tabella con la data e l'evidenza della chiusura.

| Id | Gravità | Difetto | File | Correzione proposta |
|---|---|---|---|---|
| G-01 | chiusa il 20/09/2026 (era bloccante) | sprite delle icone non ben formato (`--` in un commento XML): nessuna icona disegnata | `static/img/icons.svg` | fatto dall'owner: commento riformulato; 546 icone disposte e 0 vuote nel report delle catture (§10) |
| G-02 | chiusa il 20/09/2026 (era bloccante sotto il breakpoint della navigazione) | `backdrop-filter` su `.site-header` lo rendeva containing block di `.nav-drawer` e `.nav-overlay` (`position: fixed`): drawer alto 65 px, overlay 0 px | `static/css/components.css` §7 | fatto dall'owner: velo spostato su `.site-header::before` (§1.4); drawer alto quanto lo spazio disponibile a 390 e a 1024 px (§8.2) |
| G-03 | alta (RTL) | stringhe d'identità latine non isolate in arabo: «™Italy Legal Entry» nel footer, promotore troncato all'inizio nella barra | `static/css/base.css` (helper bidi), `apps/cms/templatetags/cms_nav.py` (`{% brand %}`) | emettere `dir="ltr"` nel tag `brand` ed estendere l'isolamento a `.site-footer__promoter`, `.utility-bar__identity strong` |
| G-04 | alta (bloccante senza JS sotto 80rem) | senza JS, sotto 80rem, l'header sticky contiene l'intero menu con i sotto-pannelli aperti: 781 px (erano ≈ 465 px con il menu dello Stage 1). A 390 × 844 restano 63 px di pagina visibili, a 1024 × 768 nessuno: il contenuto non si può leggere, contro il principio 4 (§1.1) e ADR-009 | `static/css/components.css` §7 | `html.no-js .site-header { position: static; }` dentro `@media (max-width: 79.999rem)` |
| G-13 | bassa | `id` derivato dal titolo in `cta_panel.html`; `id` fisso in `hero.html` | `templates/components/` | accettare un parametro `id` |
| G-14 | bassa | separatore « : » francese generato in CSS dopo `<dt>` in `.meta-row` | `static/css/components.css` §13 | spostare il separatore nel template, tradotto |
| G-15 | bassa | `--font-mono` nomina IBM Plex Mono, non self-hosted | `static/css/tokens.css` | togliere il nome dalla pila o aggiungere i file |
| G-16 | bassa | `docs/I18N_RTL.md` citato dai CSS ma inesistente | `docs/` | scrivere il documento o aggiornare i commenti |
| G-19 | bassa | le FAQ usano `.accordion__panel`, classe che il design system non definisce (il componente usa `.accordion__body`) | `templates/faq/_item.html` | usare `.accordion__body` |
| G-20 | bassa | `.reveal--stagger` non produce uno scaglionamento visibile e ritarda di 0–480 ms l'hover dei figli | `static/css/components.css` §29 | applicare opacità/transizione ai figli oppure rimuovere il modificatore |
| G-21 | bassa | `remember` delle tab scrive in `localStorage` ma non rilegge | `static/js/main.js` (`initTabs`) | leggere `tabs:<chiave>` all'inizializzazione oppure rimuovere l'opzione |
| G-22 | media — chiusa | due fogli di stile dello Stage 1 sono fuori sistema: nomi di token inesistenti con ripieghi esadecimali, `linear-gradient` e ombra pesante nell'hero del Forum, scala tipografica e anello di focus propri (3.01:1 e 3.05:1 sul fondo, contro 13.52:1 del sistema) | `apps/forum/static/forum/forum.css`, `apps/orientation/static/orientation/wizard.css` | riscriverli sui token reali (`--color-primary-900`, `--text-muted`, `--border-subtle`, `--font-size-h3`…), togliere gradiente e ombra, lasciare il focus a `base.css`, usare `components/stepper.html` nel wizard  **Chiusa il 20 settembre 2026**: i due fogli usano solo token reali, senza gradiente né ombre o anelli di focus propri; `test_stage1_app_stylesheets_use_only_design_tokens` e `tests/frontend/test_css_tokens_exist.py` lo verificano. |
| G-23 | media | a drawer aperto e pagina non scrollata l'overlay è dipinto sopra la fascia bassa dell'header (parte da 72 px, l'header finisce a 113 px): wordmark e bottone «Menu» velati, etichetta «Menu» a 3.92:1 | `static/css/components.css` §7, `static/js/main.js` (`initNavigation`) | impostare `--nav-drawer-top` su `#site-header` (o su `<html>`) invece che sul drawer e usare `inset-block-start: var(--nav-drawer-top, var(--header-height))` anche per `.nav-overlay` |
