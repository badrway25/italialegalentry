# DESIGN SYSTEM V4 — token e componenti

Stato: **FISSATO** dal Creative Director il 24 settembre 2026 (dopo il chiarimento delle 20:58) ·
Direzione: `CREATIVE_DIRECTION.md` («Il portico e la console») · Destinazione: `static/css/v4/tokens.css`
(importato **dopo** `v2/tokens.css`, che resta come base e i cui nomi V4 ridefinisce dove indicato) ·
Prova: ogni rapporto di contrasto è calcolato (WCAG 2.x, luminanza relativa, `scratchpad/contrast.py`) e
ri-verificato da `tests/frontend/test_v4_tokens.py` (da scrivere insieme al file).

Regola di lettura: «conservato» = valore V2 identico; «ridefinito» = stesso nome, nuovo valore (i fogli
V2 lo ereditano); «nuovo» = nome nuovo. Nessun valore arbitrario nei componenti (§63): ciò che non è qui
non esiste.

---

## 1. Colore, superfici, gradienti

### 1.1 Carta minerale — conservata

`--min-0 #f4f3f0` canvas · `--min-1 #ecebe6` area · `--min-2 #fbfaf8` foglio · `--min-3 #ffffff`
elevato · `--ink #15222a` (14,62 su min-0) · `--ink-2 #4a5a62` (6,46) · `--ink-3 #55646b` (5,48) ·
`--hairline #d3d2cc` · `--hairline-strong #7a868b` (3,37 su min-0; 3,59 su min-2; 3,14 su min-1).

### 1.2 Navy-mezzanotte — ridefinito (evoluto da `--brand-navy #0f2547`)

```css
--mid-0: #071226;  /* utility, piè di pagina, scrim di base */
--mid-1: #0b1a33;  /* canvas dei capitoli scuri, rail, hero, processo */
--mid-2: #10233f;  /* area, hover della rail */
--mid-3: #16304f;  /* foglio, voce attiva, tooltip */
--mid-4: #1d3b5e;  /* elevato su scuro */
--on-dark: #eef1f6;   /* 15,33 su mid-1 · 13,90 mid-2 · 11,82 mid-3 · 10,08 mid-4 */
--on-dark-2: #b9c5d6; /*  9,94 · 9,01 · 7,66 · 6,53 */
--on-dark-3: #8a9bb3; /*  6,13 · 5,56 · 4,73 · 4,03 → testo SOLO su mid-1/mid-2 */
--hairline-dark: rgba(214,226,228,.14);        /* ritmo, decorativa */
--hairline-dark-strong: rgba(214,226,228,.28); /* separatori */
--edge-dark: rgba(214,226,228,.45);            /* 3,63 su mid-1: bordo di componente su scuro */
```

I nomi V2 restano (`hero.css`, `shell.css`, il piè di pagina ereditano l'evoluzione senza modifiche);
`--navy-*` non esiste come secondo nome. `--brand-navy` resta **solo** nel marchio e nell'arco interno
della porta (chiave oro su navy 5,80).

### 1.3 L'accento — famiglia, non dogma

```css
--accent: #0f6a72;        /* testo e link: 5,69 su min-0 · 6,05 su min-2 · 5,29 su min-1 */
--accent-2: #12777f;      /* la luce: icone, stop alto del gradiente: 4,77 su min-0 · 5,07 su min-2 */
--accent-3: #15808a;      /* stop alto in hover (mai testo su chiaro) */
--accent-hover: #0b555c;  /* 7,67 su min-0 */
--accent-dark: #7fd1d8;   /* su scuro: 9,93 su mid-1 · 7,65 su mid-3 */
--accent-dark-2: #8fd8de; /* stop alto del gradiente scuro: mid-1 su di esso 10,78 */
--accent-dark-hover: #a5e0e5; /* mid-1 su di esso 11,90 */
--accent-ring: #1d8a93;   /* anello di focus: 3,70 min-0 · 3,94 min-2 · 3,44 min-1 · 4,11 bianco · 3,41 wash */
--accent-wash: #d9eef0;   /* fondo BRAND, SOFT, selezione */
--accent-wash-2: #c7e4e7; /* hover del SOFT */
--accent-glow: rgba(15,106,114,.35);
--grad-primary: linear-gradient(180deg, #12777f, #0f6a72);        /* bianco su di esso: 5,29 → 6,32 */
--grad-primary-hover: linear-gradient(180deg, #15808a, #12777f);  /* bianco: 4,68 → 5,29 */
--grad-primary-dark: linear-gradient(180deg, #8fd8de, #7fd1d8);   /* mid-1 su di esso: 10,78 → 9,93 */
--grad-brand: linear-gradient(135deg, #d9eef0, #eef6f7);
--grad-brand-dark: linear-gradient(135deg, #1b344e, #10233f);     /* on-dark 11,26 · accent-dark 7,29 */
--grad-primary-press: linear-gradient(180deg, #0f6a72, #12777f);       /* la luce invertita alla pressione */
--grad-primary-dark-hover: linear-gradient(180deg, #a5e0e5, #8fd8de);  /* mid-1 su di esso 11,90 → 10,78 */
--grad-primary-dark-press: linear-gradient(180deg, #7fd1d8, #8fd8de);
```

### 1.4 Le sette famiglie di sfondo (§37) — recipe

| Recipe | CSS | Dove è ammesso |
|---|---|---|
| **NEUTRAL** | `background: var(--min-0)` | default di ogni schermata operativa e delle pagine STANDARD/LEGAL |
| **SOFT** | `background: var(--min-1)`; pubblico: `+ url(grid-160.svg)` graticola 160 px al 4 % | grounds di sezione (vie, pilota), track dei controlli, intestazioni di tabella |
| **DARK** | `background: var(--mid-1); background-image: var(--mesh-dark)` con `--mesh-dark: radial-gradient(70% 60% at 15% 0%, rgba(31,74,138,.22), transparent 60%), radial-gradient(50% 50% at 100% 100%, rgba(63,166,175,.08), transparent 60%)` — punto più chiaro `#132f4e`: on-dark 12,01 · on-dark-2 7,78 · accent-dark 7,78 | capitoli pubblici, pannello sinistro del login, piè di pagina (`--mid-0`), **rail** (mesh al 12 %) |
| **BRAND** | `background: var(--grad-brand)`; bordo 1 px `--accent-ring` al 40 %; testo `--ink` (13,48 su #d9eef0 · 14,81 su #eef6f7), link `--accent` (5,24 / 5,76) | **una volta per pagina**: orientation, «Espace réservé» (variante `--grad-brand-dark`), callout |
| **IMMERSIVE** | DARK + fotografia con `--grad-photo-dark: linear-gradient(180deg, rgba(11,26,51,0) 40%, rgba(11,26,51,.45))` + ≤ 2 isoipse ≤ 8 % + grana `grain.svg` 3 % | hero, processo, forum pubblico, hero delle landing; l'unico luogo con un oggetto vivo |
| **DATA** | `background: var(--min-2)`; righe con `--hairline`; intestazioni `--min-1`; cifre tabellari | fogli di collezione (DocumentCollection, Table, HealthStrip, Timeline), skeleton |
| **FOCUS** | `background: var(--min-0); background-image: var(--light-focus)` con `--light-focus: radial-gradient(80% 60% at 50% 0%, #ffffff, transparent 70%)`; il pannello del compito a L2 | login (lato modulo), wizard, corpo delle modali, pagina risultato |

Tecniche ammesse (§37): mesh radiale (DARK), luce radiale (FOCUS), grana (IMMERSIVE), campo di tracciati
SVG **solo** le quattro vie e la rotta del processo, isoipse (IMMERSIVE), griglia (SOFT pubblico),
forma architettonica = l'arco. Nessun blob.

### 1.5 Semantica — conservata, con due promozioni

`--ok-700 #1e7a4d` / `--ok-100` / `--ok-300` (regolare, terminato — **mai** «approvato») · `--err-700
#b3261e` / `--err-100` (6,27 su min-2) · `--seal-600 #8c6d4b` (4,57 su min-2) / `--seal-100` /
`--seal-300` (7,65 su mid-1) · `--pending-700 #705434` (6,70 su min-2) · **promossi da v3 a token**:
`--pending-300 #d8bd8e` (9,58 su mid-1), `--err-300 #f0a49b` (8,67 su mid-1).

### 1.6 Le quattro vie — chiaro conservato, scuro nuovo

`--route-1 #0f6a72` (5,29 su min-1) · `--route-2 #1c5f7c` (5,91) · `--route-3 #34506a` (7,03) ·
`--route-4 #2f6b5c` (5,21); su navy: `--route-1-dark #7fd1d8` (9,93) · `--route-2-dark #8fbfe8` (8,92) ·
`--route-3-dark #aab7cc` (8,56) · `--route-4-dark #a8cfc0` (10,21); attenuate al 50 % restano ≥ 3,08.
Mai da sole: indice o nodo + glifo attore + parola. Gli attori (`--owner-*`) restano come V2.

### 1.7 Superfici di stato — nuove

```css
--surface-hover: color-mix(in oklab, var(--accent) 4%, var(--min-2)); /* ≈ #f2f4f3: ink 14,69 · ink-2 6,49 · accent 5,72 · err 5,92 · pending 6,32 · ring 3,72 */
--surface-selected: var(--accent-wash);
--surface-disabled: #e3e2dd;      /* ink-3 su di esso 4,73 */
--surface-soft-dark: rgba(127,209,216,.14); /* su mid-1 → #1b344a: accent-dark 7,34 */
--scrim: rgba(7,18,38,.50);
--glass-light: rgba(251,250,248,.85); /* composito peggiore su carta #faf9f7: ink 15,42 · ink-2 6,81 · accent 6,00 · hairline-strong 3,56 */
--glass-light-over-dark: rgba(251,250,248,.92); /* sopra un capitolo navy → #e8e8e7: ink 13,23 · accent 5,15 · hairline-strong 3,05 */
--glass-dark: rgba(11,26,51,.55);  /* sopra il mesh → #0f233f: on-dark 13,92 · on-dark-2 9,02 · accent-dark 9,02 */
```

### 1.8 Marchio — conservato, intoccabile

`--brand-green #157a3c` · `--brand-navy #0f2547` · `--brand-red #c4142b` · `--brand-gold #c39a2b`: solo
nel marchio, nella chiave e nell'arco interno. Il tricolore non esiste altrove.

### 1.9 Tavola dei rapporti nuovi (tutti calcolati)

| Coppia | Rapporto | Soglia |
|---|---|---|
| bianco su `#12777f` / `#0f6a72` (primario) | 5,29 / 6,32 | ≥ 4,5 ✓ |
| bianco su `#15808a` (hover, stop alto) | 4,68 | ≥ 4,5 ✓ |
| `--accent-2` su min-0 / min-2 | 4,77 / 5,07 | ≥ 4,5 ✓ |
| `--accent-hover` su `--accent-wash` / `--accent-wash-2` (SOFT) | 7,07 / 6,35 | ≥ 4,5 ✓ |
| `--accent-ring` su wash / wash-2 | 3,41 / 3,07 | ≥ 3 ✓ |
| `--hairline-strong` su wash | 3,11 | ≥ 3 ✓ |
| `--on-dark` / `-2` / `-3` su mid-1 | 15,33 / 9,94 / 6,13 | ✓ |
| `--on-dark-3` su mid-4 | 4,03 | testo **no**, glifo ✓ |
| `--accent-dark` su mid-1 / mid-3 / mesh / vetro scuro / soft-dark | 9,93 / 7,65 / 7,78 / 9,02 / 7,34 | ✓ |
| `--edge-dark` su mid-1 | 3,63 | ≥ 3 ✓ |
| vie scure su mid-1 (min) / mesh (min) | 8,56 / 6,70 | ✓ |
| vie scure attenuate 50 % su mid-1 (min) | 3,08 | ≥ 3 ✓ |
| ink / accento / bordo su vetro chiaro (peggiore) | 15,21 / 5,92 / 3,51 | ✓ |
| ink / accento / bordo su vetro chiaro sopra navy (92 %) | 13,23 / 5,15 / 3,05 | ✓ |
| marca dei chip su corpo 8 %: pending / err / ink / seal | 5,98 / 5,51 / 13,36 / 4,16 | ≥ 3 ✓ |
| marca dei chip piena su min-2: ink-2 / pending / err / seal / void | 6,87 / 6,70 / 6,27 / 4,57 / 3,59 | ≥ 3 ✓ |
| `--brand-gold` su mid-1 / brand-navy | 6,59 / 5,80 | ✓ |

## 2. Profondità 0–4 (§39)

| L | Ruolo | Chiaro: superficie · bordo · ombra | Scuro | Blur | Dove |
|---|---|---|---|---|---|
| **0** | flat / base | ground del recipe · nessuno · nessuna | idem | — | righe, celle, testo, header di pagina, JourneyRail, legenda mobile |
| **1** | interattivo | `--min-2` · 1 px `--hairline` · `--shadow-1` | `--mid-2` · `--hairline-dark` · `--shadow-1-dark` | — | pannelli, OptionCard, DocumentCard, dropzone, foglio DATA, schede news, riga in hover |
| **2** | elevato | `--min-2` (o `--min-3` su SOFT) · 1 px `--hairline` · `--shadow-2` | `--mid-3` · `--shadow-2-dark` | — | pannello «Prochaine étape», pannello del wizard, foglio del login, pannello in hover (da L1), OptionCard selezionata, ContextHeader compatto |
| **3** | flottante | `--min-3` · 1 px `--hairline` · `--shadow-3` | `--mid-3` · `--edge-dark` · `--shadow-3-dark` | **12 px** solo sulle barre appiccicose (vetro), **16 px** sui pannelli in vetro dell'hero/login | popover, dropdown, tooltip (scuro), mega-menu, notifiche, toast, header scrollato, barra di contesto, barre mobili, legenda in vetro |
| **4** | modale | `--min-2` · nessuno · `--shadow-4` + `--scrim` | `--mid-2` | **6 px** sullo scrim | dialog, drawer, command menu, cassetto mobile |

```css
--shadow-1: 0 1px 2px rgba(7,18,38,.06);
--shadow-2: 0 1px 2px rgba(7,18,38,.06), 0 8px 24px -8px rgba(7,18,38,.14);
--shadow-3: 0 4px 8px -2px rgba(7,18,38,.08), 0 16px 40px -12px rgba(7,18,38,.20);
--shadow-4: 0 12px 24px -6px rgba(7,18,38,.16), 0 32px 64px -16px rgba(7,18,38,.30);
--shadow-glow: 0 4px 12px -4px var(--accent-glow);   /* solo il primario in hover */
--shadow-glow-dark: 0 4px 12px -4px rgba(127,209,216,.35); /* il primario scuro in hover */
--shadow-door: 0 40px 64px -32px rgba(7,18,38,.60);  /* conservato: la porta */
--drop-door: drop-shadow(0 32px 40px rgba(7,18,38,.60)); /* lo stesso ruolo, per la porta disegnata in SVG */
/* nel navy le alfa raddoppiano: --shadow-1-dark … --shadow-4-dark (stessi offset) */
--blur-nav: 12px; --blur-panel: 16px; --blur-scrim: 6px;
```

**Riconciliazione con V2 §7 («DENSE vieta ombre, vetro, reveal»).** La regola è **abrogata** (chiarimento
20:58) e sostituita da: le pagine operative usano L0–L2 a riposo, L3 per ciò che flotta (barre in vetro,
popover, toast), L4 per le modali; il moto è MICRO/INTERACTIVE (§7). Ciò che V4 tiene di V2 §7: LEGAL
resta senza moto decorativo e senza capitoli scuri; nessuna pagina ha più di **un** capitolo scuro
fuori da IMMERSIVE. Il test `grep box-shadow` sul CSS compilato accetta **sei** ruoli + l'alone di
focus (`test_v2_tokens.py` aggiornato in `test_v4_tokens.py`). Le modalità `data-mode` restano come
dichiarazione, con la tabella riscritta: IMMERSIVE (oggetto vivo, scroll-linked, fotografia), RICH
(reveal, fotografia), STANDARD (reveal), DENSE (moto causale, molle di layout, L3/L4 ammessi), LEGAL
(nulla).

## 3. Raggi (§40)

```css
--radius-xs: 4px;  --radius-sm: 6px;  --radius-md: 10px;  --radius-lg: 14px;  --radius-xl: 20px;
--radius-full: 999px;
--radius-control: var(--radius-md); /* V2 ridefinito: era 2px */
--radius-tile: var(--radius-md);    /* V2 ridefinito: era 6px */
```

Assegnazione: Button/Input/Select/Textarea **md** · Chip/Badge/Avatar/indicatore della rail/track del
segmentato/tacche del misuratore **full** · Panel/OptionCard/DocumentCard/Popover/Dropdown/Toast/
dropzone/schede immagine **lg** · Modal/Drawer (bordo interno)/mega-menu (angoli inferiori)/pannello
del wizard/foglio del login/legenda in vetro **xl** · Tooltip/Checkbox/Skeleton **sm** · disco del
glifo **full** · **riga di tabella e DocumentRow: 0** (il foglio che le contiene ha `lg`) · voce della
rail **md** · tassello del marchio **md**.

## 4. Tipografia (§87–88)

### 4.1 Famiglie — una superfamiglia per l'interfaccia

| Voce | Famiglia (self-hosted) | Pesi | Compagno arabo |
|---|---|---|---|
| Display pubblico | **Newsreader** variabile (opsz auto) — conservata | 300 display, 400 titoli, 400 corsivo lead | Noto Naskh Arabic 400/700 |
| Interfaccia e corpo | **IBM Plex Sans** — **nuova** | 400, 500, 600 (+ 400 corsivo) | **IBM Plex Sans Arabic** 400/500/600 (già vendorizzata) |
| Riferimenti | **IBM Plex Mono** — **nuova** | 400 | numerali occidentali in tutte le lingue |

Perché Plex e non Fira: (1) IBM Plex Sans Arabic è **già** il compagno arabo vendorizzato; con Plex Sans
il latino e l'arabo diventano **la stessa superfamiglia** — stessa altezza di x, stessa logica dei pesi,
stesse cifre — e la parità RTL (§62) smette di essere un accostamento di due disegni diversi; (2) i
terminali squadrati e le cifre tabellari (`tnum`) di Plex leggono «strumento» a 13–15 px, dove Fira
legge «documentazione»; (3) non è Inter/Roboto (il segnale «template»), è OFL, self-hostabile.
Perché non Garamond, Inter, Geist, Manrope, Plus Jakarta: Garamond come UI accentua l'editoriale
respinto; gli altri non hanno un compagno arabo della stessa famiglia. Costo: sei file woff2 Plex Sans
(latin/latin-ext × 400/500/600 ≈ 150 KB) + corsivo 400 + due Plex Mono (≈ 40 KB); i sette file Fira si
ritirano nella stessa fase (≈ −150 KB): budget netto ≈ +40 KB. `--f-sans`, `--f-mono`, `--font-ui`,
`--font-ref` ridefiniti; `fonts.css` aggiornato; `docs/IMAGE_LICENSES.md`/`FRONTEND_DEPENDENCIES.md`
registrano la licenza OFL.

```css
--f-serif: "Newsreader", "Noto Naskh Arabic", "Iowan Old Style", Georgia, serif;
--f-sans: "IBM Plex Sans", "IBM Plex Sans Arabic", "Segoe UI", system-ui, sans-serif;
--f-mono: "IBM Plex Mono", ui-monospace, "Cascadia Mono", Consolas, monospace;
--f-arabic-sys: "Segoe UI", "Noto Sans Arabic", "Geeza Pro", system-ui, sans-serif;
--texture-hatch: repeating-linear-gradient(45deg, transparent 0 3px, rgba(255, 255, 255, 0.45) 3px 5px);
--texture-dots: radial-gradient(circle, rgba(255, 255, 255, 0.6) 1.2px, transparent 1.5px);
--motion-stagger: 60ms;
--mask-fade-end: linear-gradient(to right, #000 calc(100% - 40px), transparent);
--mask-fade-end-rtl: linear-gradient(to left, #000 calc(100% - 40px), transparent);
--focus-ring-color: var(--accent-ring);
--focus-ring-width: 2px;
--focus-ring-offset: 2px;
```

### 4.2 Scala pubblica (portico)

| Token | px / lh · peso · famiglia | Uso |
|---|---|---|
| `--t-display` | clamp(44px, 1.5rem + 3.6vw, 76px) / 0.96 · 300 · serif · −0.015em | solo l'H1 dell'hero (era 52→100) |
| `--t-plate` | 52 / 56 · 400 · serif | titoli delle landing (era 64) |
| `--t-title` | 40 / 44 · 400 · serif | H1 delle pagine pubbliche (era 48) |
| `--t-band` | 32 / 36 · 400 · serif | titoli di sezione pubblici |
| `--t-entry` | 22 / 28 · **600 · sans** | titoli di pannello/scheda pubblici (era serif) |
| `--t-lead` | 20 / 28 · 400 corsivo · serif | lead dell'hero soltanto |
| `--t-body` | 17 / 28 · 400 · sans | corpo pubblico, misura 65ch |
| `--t-ui` | 15 / 20 · 500 · sans | navigazione, controlli pubblici |
| `--t-small` | 14 / 20 · 400 · sans | secondario |
| `--t-caption` | 12 / 16 · 500 · sans | didascalie |
| `--t-folio` | 13 / 16 · 400 · mono · .06em | riferimenti pubblici (mai coordinate) |

Il serif compare: H1 pubblici, titoli di sezione pubblici, lead dell'hero, titoli del forum e
dell'Academy pubblici, il wordmark. **Non** compare: schermate operative, mega-menu, bottoni, chip,
moduli, notice, piè di pagina (eccetto il wordmark).

### 4.3 Scala della console (Plex Sans soltanto)

| Token | px / lh · peso · tracking | Uso |
|---|---|---|
| `--u-title` | 28 / 36 · 600 · −0.01em (24/32 sotto 768) | titolo di pagina (ContextHeader) |
| `--u-section` | 20 / 28 · 600 | titolo di pannello / sezione |
| `--u-card` | 17 / 24 · 600 | titolo di scheda, riga in evidenza |
| `--u-body` | 15 / 24 · 400 | testo della console, aiuti lunghi |
| `--u-ui` | 14 / 20 · 500 | controlli, righe, etichette, chip `l` |
| `--u-small` | 13 / 20 · 400 | meta, secondario |
| `--u-caption` | 12 / 16 · 500 | qualificatori, timestamp |
| `--u-eyebrow` | 11 / 16 · 600 · .06em · maiuscolo | DOSSIER, OBJECTIF, gruppi della rail |
| `--u-numeral` | 28 / 32 · 500 · `tabular-nums` | conteggi della HealthStrip, misuratore |
| `--u-ref` | 13 / 20 · 400 · mono | riferimenti (`E46E03B461`), hash |

`font-variant-numeric: tabular-nums` su **ogni** data, conteggio, riferimento, colonna numerica.
Peso 600 ammesso **solo** ai titoli ≤ 28 px (abroga V2 «nessun peso sopra 500 nei titoli» per la
console; resta per il serif). `:lang(ar)`: famiglie compagne, `letter-spacing: 0` su ogni etichetta,
interlinea 1.8 nel corpo, `text-transform: none`, `min-inline-size: 120px` sui bottoni.

## 5. Spazio, controlli, icone, bordi, z-index

```css
/* spazio: scala V2 conservata */ --s-1: 4px … --s-32: 128px; --s-5: 20px; --s-10: 40px; --s-20: 80px;
/* layout console */
--rail-w: 64px; --rail-w-open: 248px; --ctx-h: 56px; --bottom-bar-h: 56px;
--workspace-max: 1320px; --inspector-w: 320px; --page-pad: 32px; /* 16px sotto 768 */
--container-lg: 1176px; --container-xl: 1320px; --container-xxl: 1440px; /* il gutter resta --grid-gutter di tokens.css: 16/24 per fascia */
/* breakpoint: sm 430 · md 768 · lg 1024 (rail) · xl 1280 (mega-menu, hero 6/6) · xxl 1440 (rail aperta) */
/* altezze dei controlli */
--control-sm: 36px; --control-md: 44px; --control-lg: 52px; --control-icon: 40px; --hit-min: 44px;
--input-h: 44px; --textarea-min: 96px; --chip-h: 24px; --chip-h-s: 20px; --chip-h-l: 28px;
--segmented-h: 36px; --rail-item-h: 44px; --row-min-h: 64px; --table-row-h: 48px;
--utility-h: 32px; --header-h: 64px; --header-h-scrolled: 56px;
/* icone */
--icon-xs: 14px; --icon-sm: 16px; --icon-md: 20px; --icon-lg: 24px; --icon-xl: 32px; --icon-hero: 48px;
--glyph-disc-sm: 24px; --glyph-disc-md: 32px; --glyph-disc-lg: 40px;
/* bordi */
/* --line-*, non --border-*: --border-strong e --border-accent sono COLORI nello shim (_legacy-tokens.css)
   e una scorciatoia con lo stesso nome renderebbe invalido ogni `border: 1px solid var(--border-strong)` */
--line-hair: 1px solid var(--hairline); --line-strong: 1px solid var(--hairline-strong);
--line-accent: 2px solid var(--accent); --line-dash: 1.5px dashed var(--hairline-strong);
--line-grad: linear-gradient(135deg, var(--accent-2), transparent 70%); /* via mask, 1px, pannelli in hover */
/* z-index */
--z-base: 0; --z-raised: 1; --z-sticky: 10; --z-rail: 15; --z-header: 20; --z-popover: 30;
--z-drawer: 40; --z-modal: 50; --z-toast: 60; --z-tooltip: 70;
```

## 6. Focus, hover, press (§41–43)

**FOCUS** (branded, identico a V2/V3 nei valori, esteso a ogni componente): `outline: 2px solid
var(--accent-ring); outline-offset: 2px; box-shadow: 0 0 0 5px rgba(29,138,147,.30)`; su scuro
`--accent-dark` + `rgba(127,209,216,.30)`; nelle righe e nelle celle `outline-offset: -2px`
(inset). Mai rimosso senza sostituzione; `scroll-padding-block-start` ≥ altezza delle barre.

**HOVER** — un linguaggio per famiglia, 120 ms `--ease-enter` in entrata, 120 ms `--ease-exit` in
uscita, solo con `(hover: hover)`:
| Famiglia | Hover |
|---|---|
| Button PRIMARY | gradiente più chiaro + `--shadow-1` → `--shadow-glow`; freccia +3 px |
| SECONDARY / OUTLINE | fondo `--min-1`; bordo `--hairline-strong` → `--ink-3` |
| SOFT | `--accent-wash` → `--accent-wash-2` |
| GHOST / ICON | fondo `--min-1` (scuro: `--mid-2`) |
| LINK | la linea d'ormeggio si traccia (V3, conservata) |
| Panel L1 | sale a L2 (`--shadow-2`) + bordo a gradiente (`--line-grad`) su pannelli pubblici; sulla console solo l'ombra |
| DocumentRow / riga di tabella | fondo `--surface-hover` + `--shadow-1` (la riga «si stacca» dal foglio) |
| Voce della rail | fondo `--mid-2`, glifo −1 px |
| Voce del mega-menu | fondo `--min-1`, glifo nel disco `--accent-wash` → `--accent-wash-2` |
| Chip filtro | tinta +5 % (V3) |
| OptionCard | L2 + bordo `--hairline-strong` |
| Immagine | `scale(1.02)` 320 ms |
| Pannelli delle vie (home) | + spotlight `radial-gradient(240px at var(--mx) var(--my), rgba(15,106,114,.06), transparent)` |
Touch: nessun hover; lo stato alternativo è il press.

**PRESS**: bottoni `translate: 0 1px` + luce invertita (0 ms giù, 120 ms su); OptionCard e schede
`scale(.99)`; voce della rail fondo `--mid-3`; chip tinta +10 %; riga fondo `--surface-selected` per la
durata della pressione. Reduced-motion: solo il cambio di colore.

## 7. Motion V4 (§11, §67)

```css
--motion-fast: 120ms;        /* feedback, hover, uscite */
--motion-standard: 200ms;    /* pannelli, tab, tooltip, cambi di stato */
--motion-emphasized: 320ms;  /* modali, drawer, reveal, strip, immagini */
--motion-slow: 480ms;        /* page enter pubblico, capitoli, titolo dell'hero */
--motion-draw: 900ms;        /* arco, vie, JourneyRail — una volta */
--motion-ambient: 28s;       /* la corrente delle vie — l'unico loop */
--ease-enter: cubic-bezier(.25, 1, .5, 1);
--ease-exit: cubic-bezier(.7, 0, .3, 1);
--ease-layout: cubic-bezier(.4, 0, .2, 1);
/* alias V2, per i fogli non ancora migrati */
--motion-instant: var(--motion-fast); --motion-base: var(--motion-standard);
--ease-out: var(--ease-enter); --ease-in: var(--ease-exit); --ease-standard: var(--ease-layout);
```
`--motion-slow` V2 (320) è ridefinito a 480: i suoi undici siti (drawer, dialog, palette, header) sono
ri-tokenizzati a `--motion-emphasized` nello stesso commit; `tests/frontend/test_v4_tokens.py` accetta le sei
durate e le tre curve (le curve sono **le stesse tre** di V2, rinominate).

Molle (`static/js/src/motion.js`, Motion 13.4 `spring()`): `SPRING_SOFT = { stiffness: 260, damping: 30 }`
(ζ ≈ 0,93, nessun rimbalzo — layout, altezze, riordini), `SPRING_SNAPPY = { stiffness: 400, damping:
40 }` (ζ = 1,0 — indicatori, thumb, elementi che seguono). Nessuna molla con `damping < 25`.

### 7.1 I quindici pattern

| # | Pattern | Durata · curva | Proprietà | Reduced-motion |
|---|---|---|---|---|
| 1 | **page enter** — console | 200 `--ease-enter` | `<main>` opacity 0→1; pannelli stagger 40 ms (max 6) opacity + translateY 4→0 | nessuna |
| 1b | **page enter** — pubblico | 480 `--ease-enter`, uscita 120 `--ease-exit` | View Transitions dove supportate (`view-transition-name` sull'header/ContextHeader), altrimenti crossfade del `<main>`; mai a schermo intero; la navigazione non aspetta | nessuna |
| 2 | **panel enter** (inView, una volta) | pubblico 320 · console 200, `--ease-enter` | opacity 0→1, translateY 12→0 (console 4→0); immagini `clip-path inset(0 0 12% 0)→inset(0)` | stato finale |
| 3 | **panel swap** (tab, filtro, wizard) | uscita 120 `--ease-exit`; entrata 200 `--ease-enter`; altezza `SPRING_SOFT` | opacity; translateX 16·dir→0; height via misura + transform | swap immediato |
| 4 | **modal** | scrim 200; pannello 320 `--ease-enter`; uscita 120 `--ease-exit` | scrim opacity 0→1 + blur 6; pannello `scale(.96)→1` + opacity; ≤ 640 px foglio inferiore translateY 100 %→0 | appare/sparisce |
| 5 | **drawer** | 320 `--ease-enter`; uscita 200 `--ease-exit` | translateX(100 %·dir)→0; scrim come 4 | idem |
| 6 | **nav** | header 200 `--ease-layout`; mega-menu 200 in / 120 out; indicatore `SPRING_SNAPPY`; cassetto 320 | altezza 64→56 + vetro + hairline opacity; menu opacity + translateY −8→0 + clip-path; voci stagger 40; indicatore translateX/width | stati finali, menu appare |
| 7 | **hover** | 120 in / 120 out | §6 | identico (colore) |
| 8 | **press** | 0 giù / 120 su | translate 1 px, scale .99, luce | colore |
| 9 | **list insert / remove / reorder** | `SPRING_SOFT` + opacity 200 | FLIP su transform dei fratelli; height misurata; mai su liste > 40 | salto |
| 10 | **status change** (chip) | uscita 120 / entrata 200 `--ease-layout` | crossfade della parola + glifo; stile del bordo cambia subito; **un** annuncio `aria-live` per registro | testo aggiornato |
| 11 | **wizard** | come 3 + barra dello Stepper 320 `--ease-layout` + nodo 200 | translateX nel verso di lettura (indietro = verso opposto) | immediato |
| 12 | **file upload** | dropzone 120; progresso reale; riga = 9; stato = 10; spunta di successo 320 `pathLength` | bordo dashed→solid + fondo wash; `<progress>`; nessuno shake sull'errore | stati |
| 13 | **loading** | skeleton **statico** (nessuno shimmer); bottone busy = misuratore a 3 tacche 1200 ms lineare **solo mentre è occupato**, ≤ 1 per vista; `aria-busy` | opacity delle tacche | testo «…» |
| 14 | **tooltip** | ritardo 400; 120 `--ease-enter`; chiusura 0 | opacity + translateY 4→0 dal lato dell'ancora | appare |
| 15 | **tab transition** | indicatore `SPRING_SNAPPY`; pannello = 3 | translateX/width dell'indicatore | salto |
| + | **draw** (arco, vie, JourneyRail, Timeline ultimo nodo) | 900 `--ease-enter`, stagger 120, una volta dopo LCP | `pathLength`/`stroke-dashoffset`, opacity | completo |
| + | **scroll-linked** (rotta del processo, foto della porta, capitoli) | legato allo scroll, mai temporale | `scroll()`/`animation-timeline`: stroke-dashoffset, translateY ≤ 3 %, background del capitolo | valore finale |
| + | **ambient** (corrente delle vie) | 28 s lineare, pausa fuori viewport | stroke-dashoffset di un secondo tracciato | fermo e nascosto |

Budget (§67): IMMERSIVE ≤ 2 elementi chiave animati per vista + 1 oggetto vivo; RICH ≤ 2; console
MICRO/INTERACTIVE, 0 ambiente. Prova: 0 layout/paint oltre il primo frame in Performance, INP < 200 ms.

## 8. Inventario dei componenti (§64)

Formato: **struttura · livello · raggio · classe di moto** — e che cosa cambia rispetto a ciò che esiste.

| # | Componente | Definizione V4 | Esiste? → cambia |
|---|---|---|---|
| 1 | **Button** | varianti PRIMARY (`--grad-primary`, testo `#fff`, bordo `--accent-hover`, luce interna 1 px bianco 12 %, `--shadow-1`, hover glow) · SECONDARY (min-2, bordo hairline-strong) · SOFT (wash, testo accent-hover) · OUTLINE (trasparente, bordo hairline-strong) · GHOST · LINK (linea d'ormeggio) · DESTRUCTIVE (outline `--err-700`, hover `--err-100`) · ICON · FLOATING (L3, solo mobile per l'azione primaria del fascicolo); misure 36/44/52; stati hover/press/focus/loading (misuratore)/success (spunta 320 poi ritorno)/disabled (colore, mai opacità); scuro per contesto (`.on-inverse`) · L1 (primario) / L0 · **md** · MICRO | V3 → raggio 2→10, altezze 48/40/56→44/36/52, gradiente e ombra, SOFT nuovo, `button.js` per busy/success |
| 2 | **IconButton** | 40 × 40 visibile, hit 44 via `::after inset -2px`, glifo 20, nome accessibile, tooltip · L0 · **md** · MICRO | V3 `btn--icon` 44 → 40 + hit |
| 3 | **Chip** | pillola `full`, altezze 20/24/28, padding 4/10, glifo 16 (14 in `s`) per registro (clock=attesa · warning=azione · check=conforme · close=rifiuto · minus=nullo · shield=sigillo · nessuno=neutro), corpo = marca all'8 % (14 % su scuro), **bordo 1 px della marca piena** con stile per registro (solid neutro/azione/conforme · dashed attesa · double rifiuto · dotted nullo e non mappato), parola `--ink` Plex 13/20 500, **mai colorata** · L0 · **full** · MICRO (status change) | V3 «vidimazione» → forma (pillola, glifo, bordo) cambia; registri, `data-register` da Python, legge di specificità, `chip--seal` (taglio d'angolo conservato), `chip--indicative`, contatore `chip__n` restano |
| 4 | **Badge** | contatore numerico 18 px `full`, `--ink` su `--min-1` (scuro: `--on-dark` su `--mid-3`), `tabular-nums`, larghezza riservata in `ch`; **solo dati reali** · L0 · full · MICRO | nuovo (V2 `.badge` = chip) |
| 5 | **Status** | = Chip con `data-register` + `data-stage` (misuratore di fase conservato come lunghezza del bordo inferiore) · MICRO | V3 → come Chip |
| 6 | **Avatar / Glyph** | disco 24/32/40 `full`, fondo `--min-1` (scuro `--mid-3`), glifo attore 14/16/20 (`person`, `building`, `institution`, `university`, `shield` autorità, marchio ILE); tipo attore + nome reale accanto; **nessuna fotografia di persona**; attore assente = disco tratteggiato · L0 · full · STATIC | nuovo |
| 7 | **Input** | 44 px, `--min-3`, bordo `--border-strong` (3,74 su bianco), raggio **md**, padding 0 14, etichetta sopra 14/20 500, hint sotto 13/20, errore inline `--err-700` + bordo, `aria-describedby`; icona a inizio riga solo se utile; focus ring · L0 · md · MICRO | `form_field.html` esiste → misure e materiale |
| 8 | **Select** | `<select>` nativo stilato come Input + `icon-chevron` 16 a fine riga · md · MICRO | esiste grezzo → V4 |
| 9 | **Textarea** | come Input, min 96 px, ridimensionabile in verticale · md | idem |
| 10 | **Checkbox** | 20 px, raggio **sm**, bordo strong, spuntato = `--accent` pieno + `icon-check` bianco (spunta 120 ms) · MICRO | nuovo stile |
| 11 | **Radio** | 20 px `full`, spuntato = anello `--accent` 2 px + disco 8 · MICRO | idem |
| 12 | **Switch** | track 44 × 24 `full` (`--hairline-strong` → `--accent`), thumb 20 `--min-3` + ombra 1, `SPRING_SNAPPY`; **solo** impostazioni binarie · MICRO | nuovo |
| 13 | **Tabs** | WAI-ARIA (esiste) + indicatore 2 px `--accent` che trasla (`SPRING_SNAPPY`), voce 44 px Plex 14/20 500, pannello = panel swap · L0 · INTERACTIVE | `tabs.html` esiste → indicatore + moto |
| 14 | **SegmentedControl** | `<fieldset>` di radio, track `--min-1` **full** 36 px, thumb `--min-2` + `--shadow-1` che trasla (`SPRING_SNAPPY`), conteggi reali, reflow sotto 480, stato nell'URL · L1 (thumb) · full · INTERACTIVE | nuovo |
| 15 | **Tooltip** | `--mid-3`, `--on-dark` 13/20, padding 6 10, raggio **sm**, `--shadow-3`, max 280, freccia no; ritardo 400 · L3 · sm · MICRO | nuovo |
| 16 | **Popover** | Popover API (`popover` + `anchor`), `--min-3`, hairline, `--shadow-3`, raggio **lg**, padding 8; `<details>` come ripiego · L3 · lg · MICRO | nuovo |
| 17 | **Dropdown / Menu** | Popover con voci 36 px (glifo 16 + etichetta 14/20 + scorciatoia mono), gruppi con hairline, distruttiva separata; mobile → foglio inferiore · L3 · lg · MICRO | `account_menu.html` esiste → V4 |
| 18 | **Modal** | `<dialog>` nativo: testata (glifo contestuale in disco 40 + titolo 20/28 600 + chiusura 40), corpo scorrevole, piede con azioni a fine riga; 560/720 px; raggio **xl**; scrim + blur 6; ≤ 640 foglio inferiore · L4 · xl · INTERACTIVE | `dialog.html` esiste → composizione, moto, foglio mobile |
| 19 | **Drawer** | stesso `<dialog>` a fine riga, 420 px, altezza intera, raggio xl sul bordo interno; per anteprima documento, filtri, attività · L4 · xl · INTERACTIVE | nuovo |
| 20 | **Toast** | pila in basso a fine riga, 360 px, `--min-3`, hairline, `--shadow-3`, raggio **lg**, chip di registro come glifo, chiusura, timeout 6 s con pausa; `role="status"`/`alert`; i messaggi Django diventano toast; gli esiti legali restano `notice` in pagina · L3 · lg · MICRO | nuovo |
| 21 | **Breadcrumb** | Plex 13/20, `--ink-2`, `icon-chevron-end` 16, ultimo 500 `--ink`; nella barra di contesto · L0 · STATIC | `breadcrumbs.html` esiste → misure |
| 22 | **Pagination** | bottoni GHOST 36, corrente SOFT, `tabular-nums` · L0 · MICRO | `pagination.html` esiste → V4 |
| 23 | **Table** | `<table>` semantica (`caption`, `scope`), intestazione appiccicosa `--min-1` 44 px 12/16 600 .06em, righe 48, celle 14/20, hover `--surface-hover` + ombra 1, riga a fuoco anello inset, chip, azione come bottone/menu, ordinamento come layout (FLIP, ≤ 40 righe), `.scroll-x` sotto 768 **solo per lo staff** · L1 (foglio) · lg (foglio) / 0 (righe) · INTERACTIVE | esiste in `register.css` → V4 |
| 24 | **DocumentRow** | griglia a sette zone (CD §3.5.4), min 64, hover sollevata, `<details>` per motivo/versioni con `SPRING_SOFT` · L0 in foglio L1 · 0 · INTERACTIVE | nuovo |
| 25 | **DocumentCard** | L1, raggio lg, padding 16: titolo · chip · glifo + responsabile · scadenza · bottone a tutta larghezza; menu nel piede; < 768 · lg · MICRO | nuovo |
| 26 | **Upload** | dropzone L1 `--border-dash`, min 160, raggio lg, glifo `download` ruotato 48, «Parcourir» SECONDARY; drag: bordo `--accent` pieno + fondo wash; lista file con chip di stato (in coda · in carico · analisi · accettato · errore), `<progress>` reale, sostituzione, versioni in `<details>`; niente anteprime immagine per i PDF · INTERACTIVE | esiste grezzo (`documents`) → flagship |
| 27 | **Timeline** | verticale, spina hairline, nodo 12 `full` (corrente `--accent` con alone), data tabellare 13/20, responsabile con Glyph, append-only; l'ultimo nodo si accende 320 · L0 · STATIC/MICRO | `timeline.html` esiste → V4 |
| 28 | **JourneyRail** | sette tappe bloccate; orizzontale ≥ 1024 (nodo 28, linea 2 px, etichetta 13/20), verticale sotto e nel fascicolo (descrittivo: responsabile, stato, data); corrente = anello `--accent` 2 px + alone 6 px wash + «Vous êtes ici»; frontiera MA→IT con glifo; `aria-current="step"`; si disegna una volta · L0 · INTERACTIVE (draw) | `stepper.html` esiste → nuovo componente |
| 29 | **ResponsibilityBar** | Glyph attore + tipo + nome; trame V2 §9.3 conservate come canale non cromatico (pieno · hachures · punti · linee · tratteggio) su barra 6 px `full`; «à titre indicatif» dove il dato non è del Rule Engine · L0 · STATIC | `jurisdiction.html` esiste → V4 |
| 30 | **EmptyState** | L0 con `--border-dash`, raggio lg, padding 40, glifo 48 in disco 80 `--min-1`, titolo 17/24 600, una frase 15/24, un'azione; sei varianti nominate (vuoto · ricerca · pagina · accesso · errore di rete · in preparazione) · lg · STATIC | `empty_state.html` esiste → V4 |
| 31 | **Skeleton** | blocchi `--min-1` su `--min-2`, raggio sm, **statici**, `aria-busy`, annuncio al completamento; solo dove il caricamento è reale · L1 · sm · STATIC | nuovo |
| 32 | **PageHeader** (pubblico) | eyebrow 11/16 + titolo serif `--t-title` + lead 17/28; su STANDARD/LEGAL · L0 · STATIC | `page_header.html` esiste → serif solo qui |
| 33 | **ContextHeader** (console) | eyebrow + titolo `--u-title` + riga meta (riferimento mono · chip · responsabile · misuratore a cinque tacche `full` che si riempiono 320 stagger 60) + **una** azione primaria a fine riga; allo scroll: barra L3 in vetro 56 px con `view-transition-name` · L0/L3 · xl (compatta) · MICRO | `case_header.html` esiste → nuovo componente |
| 34 | **Search** | Input 44 con `icon-search` 20, cancellazione; console: nel `ctx`; pubblico: nel mega-menu con autocomplete accessibile (`role="combobox"`) · L0/L3 · md · MICRO | nuovo |
| 35 | **CommandMenu** | `<dialog>` L4 640 px, Ctrl/⌘ K **solo staff**, campo 52, risultati raggruppati per tipo con glifo, frecce/Invio/Esc, **permission-aware** (stessa queryset delle viste; 404, mai 403) · L4 · xl · INTERACTIVE | nuovo |
| + | **NavigationRail / ContextBar / BottomBar** | CD §3.9 · L0 (rail, DARK) / L3 vetro · md (voci) · INTERACTIVE | nuovi (sostituiscono `local_nav.html` sulla console) |
| + | **HealthStrip** | barra 10 px `full` a sei segmenti proporzionali, gap 2, si riempie 320, segmento = filtro, cifre `--u-numeral` · L1 · lg · INTERACTIVE | nuovo |
| + | **OptionCard** | `<label>` + radio/checkbox nativi, L1 lg, glifo 24 in disco 40, titolo 15/24 500, spiegazione 14/20, hover L2, selezionata bordo accento 2 px + wash + spunta 200, ≥ 48 px · INTERACTIVE | nuovo |
| + | **Panel** | L1 lg padding 24 (20 sotto 768), titolo `--u-section`, azione a fine testata; hover L2 solo se interattivo · MICRO | `card.html` esiste → V4 |

## 9. Che cosa V4 rimuove

- **Dalla home**: la striscia sotto l'hero con «33.97° N · 6.85° W», «45.41° N · 11.88° E», «svg» e
  «Suspendre le mouvement»; la marea (`--motion-ambient` resta, per la corrente delle vie); la graticola
  dietro la porta; i «landform» delle vie (`_route_glyph.html` → glifi attore); il display a 100 px.
- **Dalla console**: la barra superiore navy con il wordmark serif (→ rail + barra di contesto); la
  sidebar di soli link con la riga verticale (`local_nav.html` sulla console → NavigationRail); i titoli
  di pagina in Newsreader; i numerali «01/02» serif e le intestazioni «PIÈCES DU DOSSIER» a filetto; la
  fascia dei quattro fatti in `dl` (→ ContextHeader); la citazione «Prochaine étape» a filetto (→
  pannello L2); la tabella per la collezione documenti della persona (→ DocumentCollection); i link
  sottolineati come azioni; il chip «Bloqué» nella colonna ACTION; il `<select>` nudo per il cambio di
  stato; i radio nudi del wizard; la barra di progresso nativa.
- **Dai token**: V2 §2 «raggi 0/2/6/999, nessun altro» (→ scala a sei); V2 §7 «DENSE vieta ombre e
  vetro» (→ §2); V2 §3.2 «nessun peso sopra 500» per la console; `--radius-control 2px`; i quattro
  ruoli d'ombra (→ sei); `--motion-slow 320` (→ 480, con ri-tokenizzazione); le tre `--t-*` serif
  usate sulla console; Fira Sans e Fira Mono (→ IBM Plex, dopo la migrazione dei sette file).
- **Da V3**: il raggio 2 dei bottoni, le altezze 48/40/56, «nessuna ombra sui bottoni»; il filetto a
  filo di lettura del chip (→ bordo a pillola con stile), il raggio 2 sul lato finale. Restano di V3:
  la luce verticale, la linea d'ormeggio del LINK, il disabilitato per colore, il forced-colors con
  gerarchia, i registri e la legge di specificità dei chip, il misuratore di fase.
- **Ovunque**: `<ul>` nudi nelle superfici principali; `style=""` (CSP); coordinate; etichette di
  debug; nomi tecnici; emoji; illustrazioni infantili; avatar di persone finte; KPI, grafici, mappe e
  contatori non calcolati.
