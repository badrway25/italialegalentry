# DESIGN SYSTEM V2 — «Due rive, una porta»

Stato: **FISSATO** il 24 settembre 2026 dalla decisione del Council (`COUNCIL_DECISION.md`) · Base:
direzione C · Trapianti obbligatori da A e B · Sostituisce `docs/design/ART_DIRECTION_A.md` e
`DESIGN_SYSTEM_2026.md` come fonte di verità visiva; quei documenti restano come storia.
Implementazione: `static/css/v2/` (fase 7) sostituisce `register.css` e il sistema editoriale, non
gli si somma. Ogni token ha una colonna «prove» (principio 18); ogni rapporto di contrasto è
calcolato, non stimato.

---

## 0. In una frase

Un'organizzazione internazionale del 2026 che unisce due rive: carta minerale per leggere,
mezzanotte-teal per i momenti immersivi, un sistema grafico cartografico proprio (graticola,
curve di livello, una rotta con stazioni), la porta del committente come firma, tre voci
tipografiche con i loro compagni arabi, profondità per scala di superfici, moto d'autore con un
solo oggetto vivo per pagina.

## 1. Colore

### 1.1 Token

```css
:root {
  /* Capitolo minerale — lettura */
  --min-0: #F4F3F0;  /* canvas */
  --min-1: #ECEBE6;  /* area: barra istituzionale, sfondi di sezione, rail di navigazione */
  --min-2: #FBFAF8;  /* foglio: card, pannelli, header */
  --min-3: #FFFFFF;  /* elevato: popover, menu */
  --ink:   #15222A;  --ink-2: #4A5A62;  --ink-3: #55646B;
  --hairline: #D3D2CC;  --hairline-strong: #7A868B;

  /* Capitolo mezzanotte — immersivo */
  --mid-0: #0A151C;  --mid-1: #0E1B23;  --mid-2: #14242E;  --mid-3: #1B2F3A;  --mid-4: #223A46;
  --on-dark: #EEF2F1;  --on-dark-2: #B7C3C4;  --on-dark-3: #8FA0A3;
  --hairline-dark: rgba(214,226,228,.14);  --hairline-dark-strong: rgba(214,226,228,.28);

  /* L'unico accento interattivo: link, CTA primaria, focus. Uno, in due luminosità. */
  --accent:       #0F6A72;  /* su chiaro */
  --accent-hover: #0B555C;
  --accent-dark:  #7FD1D8;  /* su scuro */
  --accent-ring:  #1D8A93;  /* anello di focus su chiaro (3.70:1 UI) */

  /* Territorio — grafica, mai testo, mai interazione */
  --terr-line:     #3FA6AF;  /* isoipse, tacche, rotta su scuro (6.07:1 UI) */
  --terr-line-lt:  #0F6A72;  /* le stesse linee su chiaro */
  --terr-wash:     #D9EEF0;

  /* Semantica — mai marca */
  --ok-700: #1E7A4D;   --ok-100: #DCEFE4;   --ok-300: #7CCFA0;
  --err-700: #B3261E;  --err-100: #F6DEDC;
  --seal-600: #8C6D4B; --seal-100: #EFE6DA; --seal-300: #C7A77E;   /* bronzo: solo sigilli (autorità, jeu de règles, attestati) */
  --pending-700: #705434;  /* ≥ 4.5:1 su --min-0, sostituisce il 3.2:1 rilevato in revisione */

  /* Marca ufficiale — mai alterata, mai usata altrove */
  --brand-green: #157A3C;  --brand-navy: #0F2547;  --brand-red: #C4142B;  --brand-gold: #C39A2B;

  /* Le quattro vie — sempre con indice + glifo + testo */
  --route-1: #0F6A72;  --route-2: #1C5F7C;  --route-3: #34506A;  --route-4: #2F6B5C;

  /* Responsabili (rail 2.0) — sempre con trama + glifo + testo */
  --owner-person: #0F6A72;  --owner-project: #34506A;  --owner-training: #1C5F7C;
  --owner-authority: #8C6D4B;  --owner-territory: #2F6B5C;
}
```

### 1.2 Rapporti (WCAG 2.x, calcolati)

| Testo / UI | Su | Rapporto | Uso |
|---|---|---|---|
| `--ink` | `--min-0` | 14.62 | corpo |
| `--ink-2` | `--min-0` | 6.46 | secondario |
| `--ink-3` | `--min-0` | 5.48 | folio, didascalie |
| `--accent` | `--min-0` / `--min-2` | 5.69 / 6.05 | link, CTA |
| `--min-0` | `--accent` | 5.69 | testo del bottone primario |
| `--accent-ring` | `--min-0` | 3.70 | focus, bordi UI |
| `--hairline-strong` | `--min-0` | 3.37 | bordi di componenti |
| `--on-dark` / `-2` / `-3` | `--mid-1` | 15.51 / 9.68 / 6.44 | testo su scuro |
| `--accent-dark` | `--mid-1` / `--mid-3` | 10.01 / 7.93 | link su scuro |
| `--mid-1` | `--accent-dark` | 10.01 | testo del bottone primario su scuro |
| `--terr-line` | `--mid-1` | 6.07 | grafica |
| `--ok-700` / `--err-700` | `--min-0` | 4.80 / 5.89 | semantica |
| `--seal-600` | `--min-0` | 4.30 | icone sigillo (UI) |
| `--pending-700` | `--min-0` | ≥ 4.5 | stato «in attesa» |
| `--brand-gold` | `--brand-navy` | 5.80 | la chiave nella porta |
| `--brand-green` / `--brand-red` | `--min-2` | 5.19 / 5.78 | wordmark su carta |
| `--brand-green` / `--brand-red` | `--mid-1` | 3.23 / 2.90 | **non passa** → variante scura del lock-up (§ 8.1) |

### 1.3 Regole

1. **Un solo accento interattivo.** Link, CTA primaria e anello di focus condividono `--accent`
   (`--accent-dark` su scuro). Nessun titolo, icona o sfondo lo usa. Il Council ha discusso un
   «blu luminoso» distinto dal teal: **non si introduce** — sarebbe un secondo accento, e la
   regola è uno. La deriva fintech si evita restringendo il *territorio*, non aggiungendo colori.
2. **Il teal del territorio è grafica.** `--terr-line` disegna isoipse, graticola, rotta, glifi;
   mai testo, mai interazione. Isoipse **solo** in modalità IMMERSIVE (§ 7).
3. **Verde solo semantico** (regolare, terminato, valido); **rosso solo errore**; **bronzo solo
   sigilli**. Mai accostati come motivo.
4. **Il tricolore vive solo nel marchio.** Nessun altro elemento usa `--brand-*`.
5. **Un capitolo mezzanotte per pagina** fuori da HOME e FORUM (IMMERSIVE ne ammettono due:
   hero e processo). Il confine è un confine di sezione con transizione di sfondo, non un box.

## 2. Superfici e profondità — sette livelli

| Livello | Chiaro | Scuro | Materiale / ombra |
|---|---|---|---|
| 0 canvas | `--min-0` | `--mid-1` (`--mid-0` utility e piè di pagina) | nessuna |
| 1 area | `--min-1` | `--mid-2` | hairline 1 px |
| 2 interattivo (foglio, riga, pannello) | `--min-2` + hairline | `--mid-3` + hairline-dark | `--shadow-2` solo in hover |
| 3 elevato (popover, menu, inspector) | `--min-3` | `--mid-4` | `--shadow-3` |
| 4 focus | anello 2 px `--accent-ring` + alone 5 px al 30 % | `--accent-dark` | offset 2 px; `scroll-padding-block-start` ≥ header |
| 5 overlay (drawer, dialog, palette) | `--min-2` | `--mid-2` | `--shadow-5` + scrim; mai vetro sul contenuto |
| 6 immersivo (hero, porta, processo) | — | fotografia dentro l'arco, vignetta, isoipse | `backdrop-filter` **solo** sull'header scrollato |

```css
--shadow-2: 0 1px 2px rgba(10,21,28,.06), 0 4px 12px -6px rgba(10,21,28,.12);
--shadow-3: 0 2px 4px rgba(10,21,28,.06), 0 12px 28px -12px rgba(10,21,28,.18);
--shadow-5: 0 8px 16px -4px rgba(10,21,28,.14), 0 24px 48px -12px rgba(10,21,28,.24);
--shadow-door: 0 40px 64px -32px rgba(10,21,28,.6);
/* nel buio le opacità raddoppiano (Fluent 2) */
```

`grep box-shadow` sul CSS compilato restituisce solo questi quattro ruoli. Raggi: 0 sui
capitoli e sui fogli, 2 px sui controlli, 6 px sul tassello del marchio, 999 sulle pillole di
stato. Nessun altro.

## 3. Tipografia

### 3.1 Tre voci, con i compagni arabi

| Voce | Famiglia (self-hosted) | Pesi | Compagno arabo |
|---|---|---|---|
| Display e titoli | **Newsreader** variabile, `font-optical-sizing: auto` | 300 display, 400 titoli di sezione, 400 corsivo per il lead, 600 **solo** nel wordmark ufficiale | **Noto Naskh Arabic** 400/700 |
| Interfaccia e corpo | **Fira Sans** | 400 corpo, 500 UI, 600 solo etichette maiuscole spaziate | **IBM Plex Sans Arabic** 400/500/600 |
| Riferimenti, coordinate, folio | **Fira Mono** | 400 | numerali occidentali in tutte le lingue per i riferimenti di pratica |

Budget: tre famiglie latine + due arabe (rientra in `FRONTEND_DEPENDENCIES.md` § 3). Il corsivo di
Newsreader (147 KB per una riga) si carica **solo** sulle pagine IMMERSIVE che lo usano.
Proposta da licenziare, non prototipata: Neue Frutiger + Neue Frutiger Arabic, Signifier/Rhymes
Display Light, IBM Plex Mono — valutazione a parte, nessuna dipendenza da essa.

### 3.2 Scala e regole (da B)

Corpi: **100 / 64 / 48 / 32 / 22 / 20 / 17 / 15 / 14 / 13 / 12 px** — undici, nessun altro.
Interlinee in px multipli di 4. Misura ≤ 75 caratteri (`max-inline-size: 65ch` sul corpo).
Nessun peso sopra **500** nei titoli. Tracking negativo solo ≥ 40 px (−0.015em) e **0 in
arabo**. `text-transform: uppercase` solo su folio, eyebrow, stazioni e sui testi bloccati già
maiuscoli. **Cifre tabellari** (`font-variant-numeric: tabular-nums`) su ogni numero: riferimenti,
date, contatori, coordinate. Nessuna opacità sul testo (colore, non alfa).

| Token | px / lh | Uso |
|---|---|---|
| `--t-display` | 100 / 96 (clamp 52 → 100) | il titolo bloccato dell'hero |
| `--t-plate` | 64 / 64 | titoli di landing |
| `--t-title` | 48 / 52 | titoli di pagina (Tableau de bord, Dossier) |
| `--t-band` | 32 / 36 | titoli di sezione |
| `--t-entry` | 22 / 28 | titoli di scheda, «Prochaine étape» |
| `--t-lead` | 20 / 28 corsivo | lead |
| `--t-body` | 17 / 28 | corpo |
| `--t-ui` | 15 / 20 | interfaccia |
| `--t-small` | 14 / 20 | secondario |
| `--t-folio` | 13 / 16 mono, .08em | folio, coordinate, riferimenti |
| `--t-caption` | 12 / 16 | didascalie, tag |

`:lang(ar)`: famiglie compagne, `letter-spacing: 0` su **ogni** etichetta (folio, eyebrow, tag,
stazioni, riferimenti), interlinea 1.8 nel corpo e 1.25 nei titoli, `min-inline-size: 120px` sui
bottoni, `text-transform: none`.

## 4. Spazio, griglia, contenitori

Scala di spazio invariata: `--s-1` 4 · `--s-2` 8 · `--s-3` 12 · `--s-4` 16 · `--s-6` 24 ·
`--s-8` 32 · `--s-12` 48 · `--s-16` 64 · `--s-24` 96 · `--s-32` 128. Griglia 12 colonne,
gutter 24, margine 40 (16 sotto 430). Contenitore 1176 a `lg`, 1320 a `xl`, 1440 a `xxl`.
Breakpoint della griglia come in `DESIGN_SYSTEM_2026.md` § 7.2 (`sm` 430, `md` 768, `lg` 1200,
`xl` 1440, `xxl` 1600); **navigazione**: drawer fino a 1279 px, mega-menu da 80rem — invariato,
perché il lock-up ufficiale e otto voci non convivono sotto (mobile-typography § 3).
Header pubblico: barra istituzionale 36 px + header 64 px a desktop; **56 px totali** sotto 768
(la barra istituzionale entra nel drawer). Ranghi verticali: A 96, B 64, C 48, D 32 a desktop;
metà sotto 768.

## 5. Moto

`MOTION_SYSTEM.md` è normativo. In sintesi: sette funzioni, durate {120, 180, 240, 320} + un
tracciato immersivo 600–900 ms, curve `--ease-out (.25,1,.5,1)` · `--ease-in (.7,0,.3,1)` ·
`--ease-standard (.4,0,.2,1)`, due molle senza rimbalzo, **un oggetto vivo per pagina** (in
IMMERSIVE: la marea ≥ 20 s in CSS `transform` su ≤ 2 strati, in pausa fuori viewport e con
reduced-motion, con il controllo «Suspendre le mouvement»), **la chiave si rivela una volta** e
non levita, nessun `filter` in loop, nessun overshoot, proprietà fisiche mai (RTL). Il catalogo
per componente (§ 6 di MOTION_SYSTEM) si compila con la vertical slice.

## 6. Iconografia, grafica, fotografia

- **Icone**: set proprio, tratto 1.5 px, 20 px, `currentColor`, ogni icona con `<title>` o
  `aria-hidden`. Glifi di ruolo (persona, équipe, formazione, autorità a sigillo, territorio,
  impresa, istituzione, università) e glifi delle vie (picco, doppio picco, terrazze, cresta).
- **Sistema cartografico**: graticola 160 px con tacche; isoipse generate a build time da
  `scripts/territory.py` (seed fisso, mai `Math.random`), maschera ellittica sotto il testo,
  ≤ 43 KB inline per pagina IMMERSIVE, `forced-colors: CanvasText`; **mai** su STANDARD/DENSE/LEGAL.
- **Grammatica della porta nella piattaforma**: tassello del marchio, glifo arco+gradini negli
  stati vuoti, misuratore a tacche. Mai la porta intera fuori dall'hero.
- **Fotografia**: la fotografia del titolare dentro l'arco (AVIF/WebP 480/800/1200 ≤ 120 KB,
  `<picture>` con `sizes`, poster `fetchpriority="high"`). Altre fotografie solo su IMMERSIVE e
  RICH, art-directed, mai di cronaca migratoria. Il prodotto resta riconoscibile senza (§ 9).

## 7. Modalità di pagina

| Modo | Pagine | Ammesso | Vietato |
|---|---|---|---|
| IMMERSIVE | HOME, FORUM pubblico, landing delle quattro vie | due capitoli mezzanotte, isoipse, porta, marea, fotografia, scroll-linked | — |
| RICH | hub Personnes, Academy, cruscotti, fabbisogno impresa | un capitolo mezzanotte, reveal editoriali, grafici con dati reali | isoipse, marea |
| STANDARD | informative, FAQ, glossario, news | reveal 240 ms | capitoli scuri, ombre oltre il ruolo 2 |
| DENSE | fascicolo, liste, tabelle, back-office | transizioni di stato, molla di layout | ombre, vetro, reveal |
| LEGAL | note legali, privacy, disclosure, avvertenze | nulla | qualunque moto decorativo; misura 65–75 |

Ogni template dichiara `data-mode`; un test lo verifica.

## 8. Componenti pubblici

### 8.1 Lock-up ufficiale
Marchio 38 px + 12 px + wordmark Newsreader 600 20 px `.13em` (ITALY verde · LEGAL navy · ENTRY
rosso). **Senza la tagline del sito attuale**: è una formulazione vietata dal documento
d'implementazione del committente e la direttiva §2 non consente a un ridisegno di riesumarla —
vedi `BRAND_ASSETS.md` §1, dove la decisione è scritta per esteso e resta reversibile. Scala
**come unità**: 38/20 finché entra; poi solo il marchio 38 px con `aria-label`. `direction: ltr` sempre. **Variante scura** (unica):
marchio identico su tassello `--min-0` 46 px raggio 6, wordmark monocromo `--on-dark`; solo su
barre e piè di pagina scuri. Nessun effetto, nessuna animazione (il marchio sale di 1 px in hover
e basta). Il favicon si allinea al marchio (arco + chiave semplificati a 16/32/48).

### 8.2 Letterhead (barra istituzionale + header)
Barra `--min-1` 36 px: promotore, «Espace réservé», lingue FR · IT · EN · ع come segmenti (target
≥ 24 px). Header `--min-2` 64 px: lock-up, otto voci, CTA «Orientation» come bottone secondario.
Scrollato: carta all'88 % + `backdrop-filter`, `--shadow-2`; il lock-up non cambia. Sotto 1280:
drawer a schermo intero su carta, voci a 52 px, CTA in fondo, Escape chiude, focus restituito.
Sotto 768: 56 px totali.

### 8.3 Hero «due rive, una porta»
Capitolo `--mid-1` a tutta altezza (≤ 100 vh a desktop, **≤ 110 % del viewport a 390**).
Graticola + isoipse (due rilievi: nord in alto a destra, sud in basso a sinistra) + **la rotta**
a sei stazioni con coordinate reali (33.97° N · 6.85° W → 45.41° N · 11.88° E) che **entra dietro
la soglia della porta e riemerge oltre la volta**; su di essa, da A, i **nodi degli attori** delle
due rive con etichette mono (persona · organismo di formazione · università · autorità competente
· impresa · istituzione) — la porta è l'hub. Colonna 7/5: eyebrow mono, **`ITALY LEGAL ENTRY™`
verbatim come H1** (`--t-display`, `dir="ltr"`, `translate="no"`), lead corsivo bloccato, corpo
bloccato, due CTA in riga; a destra la porta (§ 8.4); striscia di chiusura con le coordinate e
«Suspendre le mouvement». Mobile: porta prima, intera, 220 px; titolo 52 px; CTA in vista.

### 8.4 La porta (`enhanced-v2`)
Da `BRAND_ASSETS.md` § 2: arco (aspect 3/4, raggio 190/190/0/0, filetto `--terr-line` al 60 %,
arco interno offset 16 px), fotografia del titolare dentro l'arco (opacità .50, saturazione .8,
vignetta `--mid-1` con velo teal in alto), **arco interno navy pieno `--brand-navy`** (52 %,
aspect 1/1.55), **la chiave verbatim** (34 % dell'arco interno) con alone pre-renderizzato
(`radial-gradient` oro alfa ≤ .26), tre gradini `--accent-dark` a tre opacità. Nessuna didascalia: lo slogan del sito
attuale è anch'esso vietato (`BRAND_ASSETS.md` §1). **Completa dal primo frame** in ogni stato.
Coreografia: arco tracciato 900 ms → gradini posati (stagger 100) → la chiave si assesta di 8 px
**una volta** e si ferma. Scroll: la fotografia scorre di 18 px. Hover: l'insieme sale 4 px, il
primo gradino diventa oro. `aria-hidden` sul blocco, `alt=""` sull'immagine.

### 8.5 Le quattro vie — «un molo di quattro pontili»
Griglia a zig-zag 7/5 · 5/7: pannelli livello 2 con indice serif, etichetta mono, glifo
proprietario, titolo e bottone bloccati, scala `--route-n` mai da sola, **linea d'ormeggio** che
si traccia in hover/focus e (da B) la «soglia che si apre». 6/6 sotto 1024, lista sotto 720.
Target ≥ 44 px; l'intero pannello è il target.

### 8.6 Il processo — la rotta fra due rive
Capitolo `--mid-1` (secondo capitolo ammesso in IMMERSIVE). SVG con due rive e sei nodi, rotta
`stroke-dashoffset` legata allo scroll; sotto, `<ol>` delle sei stazioni BESOIN → COMPÉTENCES →
FORMATION → PARCOURS RÉGULIER → ENTRÉE → INCLUSION con responsabile e glifo (autorità con anello
bronzo). **Alternativa da B** se in revisione la linea che sale «legge come un grafico di
crescita»: il disegno di sezione a sei livelli. Didascalia = testo bloccato
`p3.persons.how_it_works`; il progetto pilota è una scheda a lato, mai «canale autorizzato».
Sotto 1024 tre colonne con dorsale; sotto 720 lista verticale. Alternativa testuale sempre presente.

### 8.7 Piè di pagina
`--mid-0`, due righe: identità (lock-up variante scura, promotore, contatto unico
`contact@agamieuromed.org`) e navigazione + legale + lingue; **mai** quattro colonne da diciotto
link. Il glifo arco+gradini come chiusura.

### 8.8 Autenticazione
Non una card bianca centrata: pagina a due colonne — a sinistra il capitolo `--mid-1` con la
grammatica della porta (arco tracciato, gradini, nessuna fotografia) e la frase di fiducia; a
destra il foglio del modulo su `--min-2` con lock-up, campi a 48 px, errori inline, lingue.
Sotto 768: una colonna, la grammatica ridotta a una fascia di 120 px. Transizione sito → portale:
crossfade 320 ms con la barra della piattaforma che scende in scena.

### 8.9 Pagine di errore
403 / 404 / 429 / 500 con lo stesso letterhead, la grammatica della porta (una porta senza chiave
per 404, con gradini interrotti per 500) e un'azione. Nessuna animazione oltre il reveal.

## 9. Componenti di piattaforma

### 9.1 Shell — «la scrivania»
(1) **Barra** 56 px `--mid-1`: lock-up variante scura, contesto in mono (`E46E03B461`), per i
ruoli **operatore / professionista / redattore / admin** la palette comandi `Ctrl K` (da A), azioni
account e lingua come `<details>` nativi (da B). (2) **Case band** `--mid-2` con la banda
territoriale al margine finale: breadcrumb, titolo, riferimento in `--accent-dark`, i quattro fatti
(objectif, état come pillola con glifo, responsable, avancement come **misuratore a cinque
tacche** = conteggio). (3) **Spazio di lavoro** 224 / 1fr / 320: rail di navigazione appiccicoso
con glifi e nota legale, colonna centrale, **inspector** appiccicoso a destra. Sotto 1024: rail →
striscia orizzontale scorrevole 36 px; inspector in coda. Nessuna porta.

### 9.2 Prochaine étape
Primo foglio della colonna centrale, bordo iniziale `--accent` 3 px, titolo `--t-entry` serif,
responsabile con glifo a sigillo, «Cette étape ne dépend pas de vous» quando è così, un'azione.

### 9.3 Rail giurisdizione / responsabilità 2.0 (da A + B)
`<ol>` di N segmenti a tutta larghezza sopra le colonne. Ogni segmento: barra 10 px in **trama per
responsabile** (pieno = persona · hachures 45° = équipe · punti = formazione · linee = autorità
· tratteggio = territorio), stato in **parola** (Terminée · Étape actuelle · À venir) e in forma
(pieno / bordo `--accent` 2 px + marcatore / attenuato), numero, etichetta, responsabile con glifo,
«**Vous êtes ici**», **frontiera MA → IT** con glifo logico fra le tappe che cambiano riva,
`aria-current="step"`, «Étape n sur N», legenda testuale, testo nascosto per lo screen reader.
Multi-attore: due trame affiancate. **Verticale sotto 1024** (barra a lato, etichette a destra).
I responsabili vengono da `cases.services` / Rule Engine; dove non c'è dato, «à titre indicatif»
in chiaro. Tastiera: segmenti focalizzabili, Enter apre il dettaglio.

### 9.4 Checklist e tabelle
Tabella reale sopra 768 con `caption`, `scope`, cifre tabellari, riga in hover livello 2, stato
come pillola con glifo + parola; **pop-in** sotto 768 con `data-label` (già in produzione); azioni
contestuali inline; «Aucune échéance» per lo screen reader; molla di layout per inserimento e
rimozione; mai animazioni su liste lunghe.

### 9.5 Documenti
Riga: nome in mono, tipo, stato scanner a una parola con glifo, azione. Zona di caricamento: bordo
tratteggiato `--hairline-strong` che diventa `--accent` al drag, stati NEEDED → UPLOADING
(progresso reale) → PROCESSING → UNDER REVIEW → VALID / REJECTED / EXPIRING / EXPIRED con parola +
glifo; nessuna animazione sul contenuto sensibile; anteprima solo dove la policy lo consente.

### 9.6 Stati vuoti e di caricamento
Vuoto: una hairline, il glifo arco+gradini a tratto, una frase che dice chi riempie la regione e
quando, l'azione inline. Caricamento: skeleton di livello 1 con `aria-busy`, mai solo uno spinner;
annuncio `aria-live="polite"` al completamento.

### 9.7 Inspector
Livello 3, appiccicoso: pré-évaluation («Parcours pertinent», jeu de règles con sigillo, la
frase «Prochaines étapes à caractère informatif…» **sempre presente**), messaggi e scadenze
(vuoti con la grammatica), account. Mai una decisione, mai un numero non calcolato.

### 9.8 Fascicolo (flagship, da disegnare per primo dopo il cruscotto)
Context header (case band) + rail 2.0 + spazio di lavoro con: «Où en est votre demande» (lista
ordinata append-only con stato, responsabile, data), «Ce qui vous est demandé» (checklist con
FONDEMENT, azioni inline, cambio di stato come **form a pagina** con conferma, non `<select>` nudo),
intervenants, documenti, «Faire évoluer l'état» come pannello di livello 2 su carta (non un box
navy con input bianchi), inspector con storico. Mobile: sezioni come `<details>` con la rail
verticale in testa.

## 10. Bottoni e controlli

PRIMARY (`--accent` pieno, testo `--min-0`, 48 px, raggio 2) · SECONDARY (bordo
`--hairline-strong`, testo `--ink`) · TERTIARY (testo `--accent`, sottolineatura che si traccia)
· QUIET (solo testo, hover livello 1) · DANGER (`--err-700`) · ICON (44 × 44, nome accessibile)
· INLINE ACTION (mono 13 px con freccia). Stati: hover 180 ms, focus anello, active `translateY
1px`, loading con spinner a tratto + testo, disabled a colore (mai opacità sul testo). Niente pillole
oltre le pillole di stato. Campi: 48 px, etichetta visibile sopra, errore accanto, aiuto sotto,
`aria-describedby`.

## 11. Arabo e forced-colors

Solo proprietà logiche; `[dir="rtl"]` specchia gli SVG decorativi (`scaleX(-1)`) e le frecce, non
il lock-up, il titolo bloccato, i numeri, la chiave, la fotografia; il rail avanza da destra; le
etichette SVG con `text-anchor` scambiato. `forced-colors: active`: trame e glifi restano
(`forced-color-adjust: none` **solo** sui segmenti a trama), isoipse `GrayText` o nascoste,
focus con `outline` di sistema.

## 12. Prove

| Decisione | Prove (benchmark) | Contro-riferimento |
|---|---|---|
| avorio/minerale + inchiostro tinto | NBIM, Harvey, Adyen | shadcn zinc/slate |
| un solo accento | Mercury, Linear, NBIM | Bootstrap Italia (blu ovunque) |
| scala di superfici, non ombre | Linear, Vercel, Fluent 2 | Material elevation ovunque |
| tre voci + compagni arabi | Nobel, Harvey, ONCF, Maroc.ma | Inter-everything |
| pesi ≤ 500, asse ottico | Mercury 480/420, Linear 590/510 | Playfair 700 |
| rail con trama + glifo | Migrationsverket, Designers Italia | barre colorate sole |
| un oggetto vivo per pagina | Stripe, NBIM, Attio | Lusion, particelle |
| porta come firma | il sito attuale del committente | hero shader da catalogo |
