# V3 — BADGE, CHIP, PASTIGLIE DI STATO, SIGILLI, CONTATORI

Superficie `badges` · Visual Design Lead + Legal-Tech UX · **round 3**, 24 settembre 2026 · Vincolanti: `docs/design-v2/{DESIGN_SYSTEM_V2,MOTION_SYSTEM,ANTI_PATTERNS}.md`, `apps/cms/forbidden.py`, `static/css/tokens.css:58-61`. **Ogni cifra di questo round è stata rimisurata**, nessuna riportata: Chromium headless di Playwright dal `.venv` (**mai** la 9222), il foglio candidato servito come risorsa `self` sull'origine reale del sito — così la CSP del progetto resta in vigore durante la misura — e letto con `getComputedStyle`, `getBoundingClientRect` e il **pixel** dello screenshot. Scratch: `b3/{chip.css,m1..m6.json,*.png}`. Le tre cose che il round 2 sbagliava sono corrette alla radice, non ritoccate: **il registro non nasce più dalla parola** (§ 4.3), **la scala interattiva nasce dal capitolo** (§ 4.8), **il modificatore batte il registro per specificità dichiarata** (§ 4.2).

## 0. RICHIESTE DI EMENDAMENTO

**1 — DESIGN_SYSTEM_V2 § 2, ultima riga: «Raggi: … 999 sulle pillole di stato. Nessun altro.»** Chiedo *2 px* (`--radius-control`) al posto di *999*. **Motivo:** la pillola è la firma SaaS che il committente ha respinto, e il portatore primario della pastiglia è un **filetto a filo di lettura** che un raggio 999 taglia in due archi. **Costo:** una riga in § 2. **Regressione: nulla** — oggi nessuna regola applica 999 px a uno stato (`.state` ha raggio 0, `register.css:702`; `.badge` usa `--radius-xs`, `components.css:235`): l'emendamento allinea il documento al codice. Se respinto il sistema regge, ma il filetto va staccato di 2 px dal corpo e perde il contatto col bordo.

**2 — DESIGN_SYSTEM_V2 § 1.1, blocco «Semantica»: due token nuovi.** `--pending-300: #D8BD8E` e `--err-300: #F0A49B`. **Motivo:** V2 dà la luminosità chiara per mezzanotte al verde (`--ok-300`) e al bronzo (`--seal-300`) ma **non** al rosso e al pending. **Misurato in questo round** (composizione alpha al 14 % sul fondo, poi WCAG 2.x): `--pending-700` su `--mid-3` = **1.99:1**, su `--mid-2` 2.28, su `--mid-1` 2.51, su `#0f2547` 2.19; `--err-700` su `--mid-3` = **2.12:1**. I registri *azione* e *rifiuto* non hanno marca legale (≥ 3:1) su fondo scuro. Coi due token: azione **7.65:1** su `--mid-3`, rifiuto **6.93:1**. **Costo:** due righe di token. **Non** è un accento nuovo: stessa tinta, seconda luminosità. Croma Lab rimisurata — `#D8BD8E` C\*=**27.47**, `#F0A49B` C\*=**31.44** — sotto `--ok-300` (38.91) e molto sotto `--brand-gold` (60.09) e il giallo UE (85.30): fuori dall'«oro/giallo saturo» di `ANTI_PATTERNS.md:64`.

**2 bis — che cosa succede se l'emendamento 2 è respinto.** Non resta un `var()` invalido: il foglio scrive il ripiego nella dichiarazione stessa, `var(--pending-300, var(--pending-700))` e `var(--err-300, var(--err-700))` (§ 4.2, righe 11-12). **Verificato** rendendo il foglio senza i due token: `--chip-mark` calcola `#705434` e `#b3261e`, il `border-inline-start` dello pseudo-elemento resta valido e **nessun filetto sparisce** su nessuna pastiglia di mezzanotte. **Il costo, dichiarato:** su fondo scuro le marche di *azione* e *rifiuto* scendono a 1.99–2.68:1 e **non soddisfano 1.4.11**; i due registri restano distinti per **spessore** (4 px contro 3), **filetti di chiusura** (§ 4.3) e **parola**, che sono i canali non cromatici, ma la riga «marca scura» della tabella di § 6 va letta come non conforme e va aperta una deroga documentata. **Nessun altro scostamento** in tutta la specifica: nessun verde, nessuna quinta ombra, nessuna curva nuova, nessuna durata nuova, zero byte di JavaScript, zero immagini nuove.

## 1. VERDETTO SULLO STATO ATTUALE

**E1 — Quindici valori su sedici senza regola CSS.** `cases/index.html:43` e `portal/partials/case_header.html:32` scrivono `state state--{{ case.status }}` col valore grezzo dell'enum, `portal/dashboard.html:110` e `cases/detail.html:95` con quello di `ChecklistStatus`; `register.css:723-744` definisce otto modificatori e solo `done` coincide. Misurato: `.state--training` calcola `color: rgb(74,90,98)`, cioè una didascalia. **E1 bis:** `helpdesk/models.py:146` mappa `TicketStatus.CLOSED` su `""`, quindi `queue.html:38` rende letteralmente `class="state state--"`. **E2 — Quattordici pastiglie, due trattamenti** (cruscotto persona); dieci e tre su quello impresa. **E3 — Quattro stati giuridici, un pixel:** `tokens.css:61` e `:64` dànno a `--state-done-fg` e `--state-info-fg` lo **stesso** `#1e4a85`. **Quell'identità è deliberata e resta** (§ 4.1): il difetto non è il colore condiviso, è che **nient'altro** distingue i quattro. **E4 — Nessun glifo:** `hasIcon: false` su 26 pastiglie su 26. **E5 — Nessun corpo:** `background-color: rgba(0,0,0,0)`, raggio 0, un `border-inline-start: 2px`, `block-size: 16px`; «PARCOURS DE FORMATION EN COURS» è tipograficamente **identico** all'etichetta di colonna «RESPONSABLE» ed è **più piccolo** di essa, perché `register.css:712-716` mette `text-transform: uppercase` + `--track-folio` su `.state`, che DESIGN_SYSTEM_V2 § 3.2 riserva a folio, eyebrow, stazioni e testi bloccati. **E6 — La colonna ÉTAT è una texture.** **E7 — Cifre proporzionali** dove sono conteggi. **E8 — Il sigillo non esiste** (`--seal-600` non è usato fuori da `--owner-authority`). **E9 — L'indicativo non esiste.** **E10 — Due sistemi:** `.badge` su 9 `{% include %}` e 5 usi diretti, `.state` su 66 punti. **E11 — Nessun hover, nessun focus proprio.** **E12 — In `forced-colors` i sette stati diventano uno** (`register.css:800-803`). **E13 — In AR resta solo la parola,** perché `:lang(ar) .state` toglie maiuscoletto e tracking.

**E14, nuovo e decisivo, trovato mentre riparavo § 4.3.** La parola `.state--*` **non è il valore dell'enum**: sette dizionari e tre `status_word` la normalizzano prima del DOM (`documents/requirements.py:48`, `companies/models.py:324` e `:394`, `helpdesk/models.py:139`, `forum/governance.py:211-243`, `selection/models.py:181/338/840`, `portal/services.py:1028`). Undici parole vive — `filed` `review` `missing` `replace` `valid` `invalid` `done` `expired` `withdrawn` `suspended` e la **stringa vuota** — devono coprire **cinquantatré** membri di enum. `MilestoneStatus.BLOCKED` e `ProposalStatus.REJECTED` producono la stessa parola `invalid`; `CommissionStatus.ACTIVE` e `RequirementState.VALID` la stessa `valid`; sette terminali diversi la stessa `expired`. **Una parola non può portare due registri:** finché il registro si deriva dalla parola, il sistema è falso per costruzione. È la causa di tutto ciò che la revisione ha elencato al punto 2, e si ripara solo spostando la derivazione in Python (§ 4.3).

## 2. UI-UX-PRO-MAX — che cosa è sopravvissuto

**Accettati:** *Contextual Live Badge Updates* (un solo annuncio atomico per registro, mai una live region per pastiglia → § 6) e *Compact Label Overflow* (l'etichetta non si tronca e il valore intero resta raggiungibile da tastiera, puntatore **e** tocco → § 4.2, ed è la ragione per cui rifiuto `title=""`); *Dashboard Data* (mono per i dati, sans per le etichette) che conferma la coppia installata; *Patent / IP Database* (neutro formale come default, colore solo dove c'è un verdetto → § 4.1); il tier *Subtle* delle micro-interazioni (≤ 2 px, transform/opacity → § 5); «icona decorativa → `aria-hidden`» e **una sola famiglia visiva per superficie**, che è la regola che vieta un glifo disegnato a mano accanto allo sprite (§ 4.5). **Rifiutati:** *Status Page* col verde operativo (vietato da `tokens.css:58-61`); i tier *Standard* (anima `boxShadow`) e *Complex* (`elastic.out`, overshoot); Phosphor (CDN, peso); lo stile *Government Portal* «Flat Design» blu di servizio, che è il registro che il committente ha bocciato — ne prendo l'accessibilità, non l'estetica. La query `status icon glyph set verification seal` ha dato **0 risultati** ed è dichiarata: non serviva, perché `static/img/icons.svg` contiene già i sette simboli.

## 3. 21ST.DEV — che cosa resta dopo la revisione

Niente viene installato: estraggo il pattern e lo riscrivo in Django e nei nostri token. Studiati con `get_component`: #25395, #11357; mai `generate` / `iterate_generation`. **Status** (diceui): l'attributo `data-register` accanto alla classe, gancio stabile per CSS e test — *rifiutati* `rounded-full` e `animate-ping`. **Badge** (coss.com): lo pseudo-elemento che porta l'area di tocco a 44 px senza toccare il layout (§ 4.8) e la scala a tre misure ad altezza fissa — *rifiutati* il badge pieno d'accento e `transition-shadow`. **Pill** (haydenbleasel): il contatore come membro autonomo (§ 4.7) — *rifiutate* la pillola e le frecce delta. **Status Badge** (Tremor): fondo a bassissima croma, marca satura — *rifiutato* il pallino, che è colore e basta. **Stamp** (designali-in): un marchio d'autorità ha una **silhouette non rettangolare** (§ 4.6) — *rifiutati* raggiera e bordo dentellato. **Number Ticker**: la riserva di spazio per la cifra più larga (§ 4.7) — *rifiutato* il conteggio che scorre (§ 5).

## 4. LA PROPOSTA — «LA VIDIMAZIONE»

Una pastiglia di stato qui non è una *pill*: è una **vidimazione**, un'impronta apposta a margine di un registro. Nuovo file **`static/css/v3/chip.css`**, 100 righe, che il documento stampa **per intero** nei nove blocchi che seguono.

### 4.1 La decisione giuridica che governa tutto il resto: nessun verde

`static/css/tokens.css:58-61` porta una decisione scritta, che cito per esteso: *«No green means "approved". A finished step is TRANSMIS or CLOS: a fact about the file, never a verdict. Same reasoning as the absent `eligible` outcome in the domain — this platform approves nothing.»*

> **Il colore della pastiglia dice soltanto tre cose, ed è tutto ciò che questa piattaforma ha il diritto di affermare: «qualcuno deve agire» (`--pending-700`), «un atto è rifiutato o invalido» (`--err-700`), «questo fatto è emesso da un'autorità» (`--seal-600`). Tutto il resto — compresa la conformità — è portato dalla forma.**

Ne segue che **la parola non è mai colorata**: prende l'inchiostro del capitolo (`--ink`, o `--on-dark` in mezzanotte; `--ink-3` nel registro *nullo*). Il colore vive solo nella **marca**: filetto, glifo, tinta del corpo. È il principio della stampa — l'impronta è colorata, il testo è nero. `--ok-700` non compare in `chip.css`: la regola «verde solo semantico» resta intatta perché non la esercitiamo. Effetto misurato e non previsto: poiché `chip.css` è importato dopo `components.css`, `.badge{color:var(--chip-ink)}` batte `.badge--success{color:var(--color-success-fg)}` — **misurato `rgb(21,34,42)`** sul badge di successo, cioè il verde sparisce anche dai nove `{% include %}` di `components/badge.html` senza toccarli.

### 4.2 Anatomia, misure, la legge di specificità, e la regola comune scritta per intero

```
╓──────────────────────────────┐  filetto a filo di lettura: COLORE = marca, STILE = registro,
║ ⚠  Vérification prof…   │ 12 │  SPESSORE = 1/3/4 px, LUNGHEZZA = fase del dossier (§ 4.4)
╙──────────────────────────────┘  parola: Fira Sans 500, 14/20, MAI maiuscoletto, tracking 0
corpo: marca in alpha, 8 % carta / 14 % mezzanotte · raggio 2 px sul lato finale, 0 sul filetto · contatore: Fira Mono 400 tabulare, dietro un filetto 1 px, larghezza riservata in `ch`
```

**La legge di specificità, che è la riparazione del difetto centrale del round 2.** Il round 2 scriveva il registro come `.chip[data-register="…"]` **(0,2,0)** e il modificatore come `.chip--seal` **(0,1,0)**: su `class="chip chip--seal" data-register="conforme"` vinceva il registro e **il sigillo non diventava mai bronzeo**. La regola ora è dichiarata e non implicita: **il registro si scrive su un selettore d'attributo nudo `[data-register="…"]` (0,1,0); il modificatore si scrive `:is(.chip,.state,.badge).chip--x` (0,2,0) e vince sempre di una classe.** Rimisurato su quel markup esatto: `--chip-mark` calcola **`#8c6d4b`** su carta e **`#c7a77e`** in mezzanotte, `border-inline-start-style` dello pseudo-elemento **`double`**; e su `class="chip chip--indicative" data-register="attesa"` `--chip-gutter-style` calcola **`dotted`**, non `dashed`. Le due proprietà che la revisione chiedeva di rimisurare tornano i valori chiesti.

Tre misure, **misurate** a 1440 e a 390 px: `chip--s` **20 px**, default **24 px**, `chip--l` **30 px**, esatte anche coi filetti di chiusura (*conforme* 2+20+1+1 = 24; *rifiuto* 1+1+20+1+1 = 24; su `chip--s` 20 e su `chip--l` 30 in tutti e tre i casi).

```css
/* v3/chip.css — LA VIDIMAZIONE · docs/design-v3/specs/badges.md */
:root{
  --chip-neutral: var(--ink-2);   --chip-action: var(--pending-700);
  --chip-conform: var(--ink);     --chip-refuse: var(--err-700);
  --chip-void: var(--hairline-strong); --chip-seal: var(--seal-600);
  --chip-ink: var(--ink); --chip-ink-void: var(--ink-3); --chip-rest: var(--hairline);
  --chip-tint-base: 8%; --chip-tint-step: 5%;
  --chip-gutter: 3px; --chip-glyph: 14px; --chip-pad-b: 2px; --chip-track: 21px;
}
.on-inverse, .section--verso, .plate--verso, .site-footer{
  --chip-neutral: var(--on-dark-3); --chip-action: var(--pending-300, var(--pending-700));
  --chip-conform: var(--on-dark-2); --chip-refuse: var(--err-300, var(--err-700));
  --chip-void: var(--on-dark-3);    --chip-seal: var(--seal-300);
  --chip-ink: var(--on-dark); --chip-ink-void: var(--on-dark-3); --chip-rest: var(--hairline-dark);
  --chip-tint-base: 14%; --chip-tint-step: 7%;
}
.chip, .state, .badge{
  position: relative; display: inline-flex; align-items: center; gap: var(--s-2);
  min-block-size: 24px; padding-block: var(--chip-pad-b); padding-inline: var(--s-2);
  border: 0 solid var(--chip-rest); border-inline-start-width: var(--chip-gutter);
  border-start-start-radius: 0; border-end-start-radius: 0;
  border-start-end-radius: var(--radius-control); border-end-end-radius: var(--radius-control);
  background-color: color-mix(in oklab, var(--chip-mark) var(--chip-tint), transparent);
  color: var(--chip-ink); font-family: var(--f-sans); font-size: var(--t-small); font-weight: 500;
  line-height: var(--t-small-lh); letter-spacing: 0; text-transform: none; text-align: start;
  white-space: normal; font-variant-numeric: tabular-nums;
  --chip-mark: var(--chip-neutral); --chip-gutter-style: solid; --chip-tint: var(--chip-tint-base);
}
.chip::before, .state::before, .badge::before{
  content: ""; position: absolute; inset-block-start: 0; inline-size: 0; pointer-events: none;
  inset-inline-start: calc(-1 * var(--chip-gutter)); block-size: 100%;
  border-inline-start: var(--chip-gutter) var(--chip-gutter-style) var(--chip-mark);
}
.chip--s{ min-block-size:20px; font-size:var(--t-caption); line-height:var(--t-caption-lh); --chip-glyph:12px; --chip-track:15px; }
.chip--l{ min-block-size:30px; --chip-pad-b:5px; font-size:var(--t-ui); line-height:var(--t-ui-lh); --chip-glyph:16px; --chip-track:27px; }
```

**`white-space: normal` è nella regola base, e non è un dettaglio: è la garanzia di § 2.** La revisione ha ragione che senza di essa `nowrap` sopravvive per eredità da `register.css:206` (`.entry__actor`) e per dichiarazione da `components.css:237` (`.badge`), e che la promessa «va a capo, non si tronca» era irraggiungibile su 17 `.entry__actor` e su tutti i badge. Rimisurato **con** la riga, in una colonna da 180 px (178 px di contenuto), sui **sedici** valori reali in francese: `<span class="entry__actor state">` calcola `white-space: normal`, `text-transform: none`, `letter-spacing: normal`, 14 px/500, e manda a capo a **64 px**; stessa cosa per `.state` annidato dentro `.entry__actor` e per `.badge`; `scrollWidth == clientWidth == 178`, **nessuno scroll orizzontale**. Distribuzione misurata: **11 etichette su 16 restano su una riga** (24 px), 3 vanno a due righe (44 px), 2 a tre (64 px) — nessuna eccede la colonna, nessuna si tronca. A piena larghezza la più lunga, «Vérification professionnelle nécessaire», misura **266.20 px** (non 288.2: cifra del round 2 **corretta**), le altre da 59.58 a 247.75: perché tutte e sedici stiano su una riga la colonna ÉTAT deve avere almeno **268 px** — numero che consegno a `data-surfaces.md`. Sotto 768 px la tabella è in pop-in e la cella misura 358 px a 390: entra senza andare a capo.

### 4.3 Il registro non nasce dalla parola: nasce dall'enum, in Python, già in fase 1

E14 chiude la strada che il round 2 aveva preso. Delle cinquanta `.state--*` che il round 2 enumerava, **venticinque non potevano essere emesse da nessun percorso di codice**, e le venticinque vive portavano ciascuna due o tre significati. Ritiro quelle cinquanta righe e con esse l'affermazione «fase 1 a zero Python»: **il registro è calcolato dal membro dell'enum, non dalla stringa**, in un modulo nuovo `apps/core/chips.py` nella forma dei dizionari che il codice ha già, e raggiunge il DOM come `data-register` (e `data-stage` dove esiste una fase). Costo onesto del cambio: **un modulo, un filtro, 66 punti di template che guadagnano un attributo** — e il CSS scende da **50 selettori a 6**. Un valore che il modulo non conosce non riceve l'attributo: `chips.register_for()` restituisce `""` e il template scrive l'attributo solo se non vuoto, così la regola `.state:not([data-register])` lo dipinge col filetto **`dotted` «stato non mappato»**, visibile e testabile (R7). **Misurato: `dotted`.**

| Registro | Che cosa afferma | Marca | Filetto | Secondo canale non cromatico |
|---|---|---|---|---|
| **neutro** | un fatto è registrato; nessuno deve agire, nessuno giudica | `--chip-neutral`, senza croma | 3 px `solid` | — (è la riga di base) |
| **attesa** | qualcosa è dovuto, da qualcuno, e non è in ritardo | `--chip-neutral`, senza croma | 3 px `dashed` | il tratteggio · `icon-clock` |
| **azione** | il dossier non avanza finché un attore nominato non agisce, **ora** | `--chip-action` | **4 px** `solid` | lo spessore · `icon-warning` |
| **conforme** | il pezzo ricevuto è il pezzo chiesto / la tappa è compiuta come fatto | `--chip-conform`, senza croma | 3 px `solid` | **filetto di chiusura 1 px sotto** · `icon-check` |
| **rifiuto** | un atto è stato rifiutato, o il pezzo è invalido | `--chip-refuse` | 3 px `solid` | **filetti 1 px sopra *e* sotto**: la voce è sbarrata · `icon-close` |
| **nullo** | ritirato, non applicabile, archiviato: non porta nulla | `--chip-void` | **1 px** `solid` | corpo **assente**, parola in `--chip-ink-void` (→ `GrayText`) · `icon-minus` |

Il secondo canale di *rifiuto* è nuovo ed è la risposta alla revisione: il round 2 non gliene dava nessuno, e in `forced-colors` *neutro* e *rifiuto* erano identici. I due filetti orizzontali sono la **sbarratura di registro**, il gesto con cui si annulla una voce in un libro — l'opposto esatto del filetto singolo che *chiude* una voce compiuta. Rimisurato in `forced-colors: active`: *neutro* 3 px `solid`; *attesa* 3 px `dashed`; *azione* 4 px `solid`; *conforme* 3 px + `border-block-end` 1 px; *rifiuto* 3 px + `border-block-start` **e** `border-block-end` 1 px; *nullo* 1 px + parola `GrayText`; *sigillo* 3 px `double` + `outline` 1 px. **Sette forme distinte, zero colori d'autore.** Modificatori ortogonali: **sigillo** (§ 4.6) e **indicativo** (§ 4.7). `nullo` **non** è un rifiuto: un bisogno ritirato non è un rigetto, e disegnarlo in rosso sarebbe una falsità giuridica.

**La derivazione, produttore per produttore, membro per membro.** L'apice è la fase del misuratore (§ 4.4). In **grassetto** le undici correzioni che la revisione chiedeva come minimo, più le tre che ho trovato applicando la stessa lettura.

| Produttore (file) | Membro → registro |
|---|---|
| `cases.CaseStatus` (grezzo, `cases/index.html:43`, `case_header.html:32`) | `draft`→attesa¹ · `oriented`→neutro¹ · `review_required`→**azione**¹ · `training`·`selection`·`admin_process`·`pre_departure`→neutro² · `entered`·`post_entry`→neutro³ · `closed`→**neutro**³ (`tokens.css:59`: CLOS è un fatto, mai un verdetto) · `suspended`→**azione**¹ (`Case.clean()` impone una `suspension_reason` scritta) |
| `cases.ChecklistStatus` (grezzo, `dashboard.html:110`, `detail.html:95`) | `pending`→attesa · `in_progress`→neutro · `done`→conforme · `not_applicable`→nullo · `blocked`→**attesa** (dipendenza, non rifiuto) |
| `documents.RequirementState` (`requirements.py:48`) | `missing`→attesa · `filed`→neutro · `in_review`→neutro · `valid`→conforme · `invalid`→rifiuto · `expired`→**azione** (una pièce scaduta va ridepositata) · `to_replace`→attesa (non è ancora in ritardo) |
| `documents.ScanStatus` (`portal/services.py:1028`) | `not_configured`→neutro · `pending`→attesa · `clean`→**neutro** (l'antivirus non emette conformità) · `infected`→rifiuto · `error`→**azione** |
| `companies.NeedStatus` (`companies/models.py:394`) | `draft`→attesa · `submitted`·`under_review`·`in_progress`→neutro · `on_hold`→attesa · `closed`→**neutro** · `withdrawn`→**nullo** |
| `accounts.VerificationStatus` (`companies/models.py:324`) | `approved`→conforme *(unico punto dove nasce un `chip--seal`)* · `pending`→attesa · `rejected`→rifiuto · `not_required`→neutro |
| `helpdesk.TicketStatus` (`helpdesk/models.py:139`) | `information_only`→neutro · `needs_clarification`→**azione** · `professional_review_required`→**azione** (esito CR-11: richiede un atto) · `assigned`·`in_review`→neutro · `response_available`→**azione** (le sole transizioni possibili sono atti della persona) · `closed`→neutro *(oggi produce `state--`, E1 bis)* |
| `forum.ProposalStatus` (`governance.py:211`) | `draft`→attesa · `submitted`·`under_review`→neutro · `accepted`→conforme · `rejected`→rifiuto · `withdrawn`→**nullo** |
| `forum.ProjectStatus` (`:219`) | `preparation`·`active`→neutro · `suspended`→**azione** · `completed`→conforme · `discontinued`→**nullo** |
| `forum.MilestoneStatus` (`:226`) | `pending`→attesa · `in_progress`→neutro · `done`→conforme · `blocked`→**attesa** · `not_applicable`→**nullo** |
| `forum.CommissionStatus` (`:233`) | `active`→**neutro** · `dormant`→attesa · `closed`→**nullo** |
| `forum.TableStatus` (`:238`) | `open`→**neutro** · `consolidating`→neutro · `closed`→**nullo** |
| `forum.EditionStatus` (`:243`) | `planned`→neutro · `open`→**neutro** · `closed`→**neutro** (l'edizione chiusa alimenta la successiva col suo rapporto: non è nulla) · `archived`→**nullo** |
| `selection` `status_word` (`:181` attore, `:338` mandato, `:840` consenso) | attore: `valid`→conforme, `suspended`→azione, `expired`→**azione** (serve una nuova autorizzazione), `withdrawn`→nullo · mandato: `valid`→conforme, `expired`·`withdrawn`→**nullo** · consenso: `valid`→conforme, `missing`→attesa, `expired`→**nullo**, `invalid`→rifiuto |

**I letterali scritti a mano nei template** (ventidue punti) ricevono l'attributo al valore che il testo già dice; i sei che cambiano senso sono nominati qui perché nessuno li indovini: `case_header.html:59` e `selection/process.html:193` («n en retard») → **azione**, non più `state--expired`; `forum/participation.html:85` («échu») → **nullo**; `helpdesk/detail.html:78` («mandat terminé») → **nullo**; `documents/partials/register.html:67` («Bloqué») → **attesa**; `selection/process.html:215` (`blocked`) → **attesa**, non `invalid`. `components/badge.html` traduce il suo `kind` una volta per tutti e nove gli `{% include %}`: `neutral`·`info`·`primary`→neutro, `success`→conforme, `warning`→azione, `error`→rifiuto, `pending`→attesa; i cinque `.badge--*` scritti a mano (`accounts/profile.html:35`, `allauth/elements/badge.html:1`, `pathways/index.html:38`, `pathways/_orientation_cta.html:17`) ricevono l'attributo allo stesso modo.

```css
[data-register="neutro"]{ --chip-mark: var(--chip-neutral); }
[data-register="attesa"]{ --chip-mark: var(--chip-neutral); --chip-gutter-style: dashed; }
[data-register="azione"]{ --chip-mark: var(--chip-action); --chip-gutter: 4px; }
[data-register="conforme"]{ --chip-mark: var(--chip-conform);
  border-block-end: 1px solid var(--chip-mark); padding-block-end: calc(var(--chip-pad-b) - 1px); }
[data-register="rifiuto"]{ --chip-mark: var(--chip-refuse);
  border-block: 1px solid var(--chip-mark); padding-block: calc(var(--chip-pad-b) - 1px); }
[data-register="nullo"]{ --chip-mark: var(--chip-void); --chip-tint-base: 0%;
  --chip-ink: var(--chip-ink-void); --chip-gutter: 1px; }
.state:not([data-register]){ --chip-mark: var(--chip-void); --chip-gutter-style: dotted; }
```

### 4.4 Il filetto è un misuratore, e il misuratore non finisce mai col filetto

La progressione entra senza un colore in più: la **lunghezza** del tratto marcato è la fase, su una **pista** (`--chip-rest`) che resta sempre visibile. Tre fasi — «prima del percorso» · «in corso» · «entrato e dopo» — perché undici tacche su 24 px sarebbero 2.2 px l'una. La pista è **più lunga della corsa**: `--chip-track` vale 21 px su un corpo da 24, 15 su 20, 27 su 30, **quindi la fase 3 lascia comunque 3 px (5 su `chip--s`) di pista scoperta** e un misuratore pieno non si confonde mai con un filetto pieno. **Misurato:** fase 1/2/3 = **7 / 14 / 21 px** sul corpo da 24, **5 / 10 / 15** su `chip--s`, **9 / 18 / 27** su `chip--l`; una pastiglia **senza** fase (checklist, documenti, forum) ha il filetto a **24 px**, pieno, e si distingue dalla fase 3 di 3 px. È la risposta puntuale alla revisione: `chip--s` non asserisce più che ogni dossier di un registro lungo è entrato in Italia, perché su `chip--s` il misuratore **funziona** invece di essere disattivato. Il misuratore è decorativo per l'accessibilità — la parola nomina già la fase — e non aggiunge nessun `aria-*`.

```css
[data-stage="1"]{ --chip-stage:1 } [data-stage="2"]{ --chip-stage:2 } [data-stage="3"]{ --chip-stage:3 }
:is(.chip,.state)[data-stage]::before{ block-size: calc(var(--chip-stage) * var(--chip-track) / 3); }
```

### 4.5 Il glifo — lo sprite che esiste già, e i nove badge che davvero non cambiano

Lo sprite contiene `icon-check`, `icon-warning`, `icon-info`, `icon-clock`, `icon-minus`, `icon-close`, `icon-shield`, e `apps/core/templatetags/ile_core.py:65-73` li inietta già come `<svg class="…"><use href="…icons.svg#icon-X"></use></svg>` con `aria-hidden="true"`. I cinque glifi disegnati a bordi del round 1 restano ritirati: erano una seconda famiglia visiva sulla stessa riga della prima. **La revisione ha però ragione sul round 2:** scrivere `.chip__g, .badge > .icon` dava a `.badge > .icon` **(0,2,0)** la vittoria su `.icon--sm` **(0,1,0)**, e i badge cambiavano glifo senza che il documento lo dicesse. **La regola è ora scoped al solo `.chip__g`**, e ho rimisurato il glifo dentro un `{% include %}` reale: `inline-size` e `block-size` **16 px** (`--icon-size-sm`), `stroke-width` **1.5 px**, `stroke` **`currentcolor`** = `rgb(21,34,42)` — **invariato**. Ciò che nei nove badge cambia, e lo dico per intero perché è deliberato, è la **scatola**: altezza 24.19 → **24.00 px**, fondo dalle tinte `--color-*-bg` alla marca in alpha, bordo dal contorno pieno al solo filetto, parola dal colore semantico a `--chip-ink` (§ 4.1), `white-space` da `nowrap` a `normal`. Mappa registro → simbolo: attesa `clock` · azione `warning` · conforme `check` · rifiuto `close` · nullo `minus` · sigillo `shield` · **neutro: nessun glifo** — un fatto registrato è la riga di base, e metterci un pallino sarebbe l'anti-pattern respinto in § 3. Nessun glifo è direzionale: in `dir="rtl"` non si specchia nulla.

### 4.6 `.chip--seal` — il bronzo dell'autorità, senza il teatro

Tre portatori, nessuno dei quali è il colore: la **silhouette** (angolo tagliato di 7 px sul lato di lettura finale), il **filetto doppio** — il filetto che in tipografia chiude un atto — e il glifo `shield`. Il guilloche a 58° del round 1 resta cancellato: era il tratto più riconoscibilmente «premium istituzionale generato» e ricadeva in `ANTI_PATTERNS.md:64`. **`.chip--seal` non è mai interattivo** — un sigillo afferma una provenienza, non offre un'azione, e il `clip-path` ritaglierebbe l'anello di focus: per questo `::after` resta libero per l'area di tocco (§ 4.8) e non c'è nessun bersaglio da riparare sul sigillo.

```css
:is(.chip,.state,.badge).chip--seal{
  --chip-mark: var(--chip-seal); --chip-gutter-style: double; --chip-gutter: 3px;
  padding-inline-end: 14px;
  clip-path: polygon(0 0, calc(100% - 7px) 0, 100% 7px, 100% 100%, 0 100%);
  background-image: linear-gradient(45deg, transparent 0 3.95px, var(--chip-mark) 3.95px 4.95px, transparent 4.95px);
  background-repeat: no-repeat; background-position: right 0 top 0; background-size: 7px 7px; }
[dir="rtl"] :is(.chip,.state,.badge).chip--seal{
  clip-path: polygon(7px 0, 100% 0, 100% 100%, 0 100%, 0 7px);
  background-image: linear-gradient(-45deg, transparent 0 3.95px, var(--chip-mark) 3.95px 4.95px, transparent 4.95px);
  background-position: left 0 top 0; }
:is(.chip,.state,.badge).chip--indicative{ --chip-tint-base: 0%; --chip-gutter-style: dotted; }
```

**Il filetto che chiude il taglio: la geometria, rifatta e misurata.** In una piastrella 7 × 7 la lunghezza di un gradiente a 45° è 7·√2 = 9.8995 px e la linea di taglio (dall'angolo alto-sinistro all'angolo basso-destro della piastrella) cade **esattamente a t = 4.9497 px**. La revisione ha ragione che la banda del round 2, `4.45px → 5.45px`, è centrata su quel taglio e ne perde metà. **Ma l'asse del gradiente cresce verso il triangolo rimosso**, quindi la banda va collocata **prima** del taglio, non dopo: `3.95px → 4.95px`. Verificato sui pixel, a 20 px di corpo, leggendo l'ipotenusa colonna per colonna (`m3.json`): banda `3.95–4.95` → il pixel dell'ipotenusa misura **R = 140**, cioè `#8c6d4b` **al 100 % di copertura**, sei pixel pieni a 1× e **venticinque** a 2× (= 1 px CSS per riga), fra un corpo a R = 235 e un fondo a R = 244.

### 4.7 `.chip--indicative`, `.chip__q` e `.chip__n`

**Indicativo** — tutto ciò che non viene dal Rule Engine (pre-valutazione, orientamento): due portatori, e il secondo è una parola. Il filetto diventa `dotted` **(misurato `dotted` anche sopra un registro `attesa`, che è la seconda riparazione di specificità)**, il corpo sparisce (`--chip-tint-base: 0%`, **misurato `rgba(0,0,0,0)`**) e la parola è seguita dal suffisso **visibile** « à titre indicatif » in mono 12 px — la formula già prescritta in chiaro da DESIGN_SYSTEM_V2 § 9.3. Niente corsivo, niente contorno tratteggiato, nessun fondo.

```css
.chip__g{ inline-size: var(--chip-glyph); block-size: var(--chip-glyph); flex: none; fill: none;
  stroke: var(--chip-mark); stroke-width: 2.6; stroke-linecap: round; stroke-linejoin: round; }
.chip__q{ font-family: var(--f-mono); font-size: var(--t-caption); color: var(--chip-ink-void); }
.chip__n{ font-family: var(--f-mono); font-weight: 400; font-variant-numeric: tabular-nums;
  box-sizing: content-box; padding-inline-start: var(--s-2); margin-inline-start: auto; text-align: end;
  min-inline-size: calc(var(--digits, 2) * 1ch);
  border-inline-start: 1px solid color-mix(in oklab, var(--chip-mark) 34%, transparent); }
[data-digits="3"]{ --digits: 3 } [data-digits="4"]{ --digits: 4 } [data-digits="5"]{ --digits: 5 }
```

**La colonna che saltava di 8.40 px, riparata e rimisurata.** La revisione ha ragione: il round 2 scriveva `[data-digits="1"]{--digits:1}` e la riserva scendeva a 1 `ch`, per cui fra 9 e 10 la pastiglia cresceva di una cifra intera; e `min-inline-size` cadeva sulla scatola di bordo, quindi non riservava nemmeno le cifre. **Due correzioni:** `box-sizing: content-box`, così la riserva è di cifre e non di scatola; e **nessuna regola per una cifra sola**, così 1 e 2 cifre riservano entrambe 2 `ch`. Misurato sulla stessa pastiglia con 9, 10, 99 e 100: larghezza **93.47 → 93.48 → 93.48 → 101.87 px**. Fra 9 e 10 lo scarto è **0.02 px** (arrotondamento dell'avanzamento del glifo), non 8.40. A 100 la colonna cresce di una cifra, ed è voluto e segnalato: l'attributo si calcola **sul massimo del blocco, non sulla riga**, `data-digits="{{ block.counts.max|stringformat:'s'|length }}"`, così tutta la colonna cresce insieme. Oltre cinque cifre non c'è regola, `--digits` resta 2 e `min-inline-size` è un minimo: il contenuto non viene mai tagliato.

### 4.8 Stati interattivi — la scala viene dal capitolo, non da un numero assoluto

Il round 2 scriveva `--chip-tint` in valori assoluti (8 → 12 → 14 %), e poiché mezzanotte parte da 14 % **l'hover schiariva di meno del riposo e il selezionato era byte-identico al riposo**. La riparazione è strutturale: la tinta di riposo e il **passo** sono due token di capitolo, e ogni stato è un'**offesa dal riposo del proprio capitolo**, mai un numero.

| Stato | Che cosa cambia | Misurato (carta / mezzanotte) |
|---|---|---|
| **rest** | `--chip-tint: var(--chip-tint-base)` | 8 % / 14 % |
| **hover** (`:is(a,button)`, `@media (hover: hover)`) | `base + 1 passo`, più `translate: 0 -1px` **dentro** il blocco motion | 13 % / 21 % · corpo contro riposo **1.077:1 / 1.137:1** |
| **active** | `base + 2 passi`, `translate: 0 0` | 18 % / 28 % · contro riposo **1.166:1 / 1.302:1** |
| **selected** (`[aria-pressed="true"]`) | `base + 2 passi` **e due filetti di chiusura**, 1 px sotto e 1 px sul lato di lettura: la pastiglia si **chiude** | altezza invariata **24 px**, `border-block-end` e `border-inline-end` **1 px**; in fase 2 anche il glifo `check` |
| **disabled** (solo pastiglia-filtro, `aria-disabled="true"`, mai `disabled`: resta focalizzabile e annunciata) | corpo assente, passo azzerato, parola in `--chip-ink-void`, marca in `--chip-void`, `cursor: default`, **mai** `opacity` | corpo **identico al fondo** su entrambi i capitoli, parola `rgb(85,100,107)` |
| **loading** `.is-pending` | il misuratore va a **zero**: la pista c'è, la corsa no — «non ancora noto». Nessuno spinner, nessun loop | `::before` `block-size` **0 px**, corpo assente |
| **focus-visible** | **nessuna regola propria**: vale `base.css:384-389` | misurato `2px solid rgb(29,138,147)`, offset 2 px, alone 5 px |
| **error** | non è uno stato della pastiglia: è il registro *rifiuto*. Un errore di rete si dice con `.notice` accanto | — |

Una tinta non è uno stato: a 1.077:1 e 1.302:1 nessuno di questi scarti reggerebbe da solo, ed è per questo che **selected porta due filetti** e disabled/loading portano la sparizione di un canale intero. La tinta è il *feedback*, la forma è lo *stato*.

```css
.register--dense :is(.chip,.state){ min-block-size:20px; font-size:var(--t-caption);
  line-height:var(--t-caption-lh); --chip-glyph:12px; --chip-track:15px; }

:is(a,button):is(.chip,.state):hover{ --chip-tint: calc(var(--chip-tint-base) + var(--chip-tint-step)); }
:is(a,button):is(.chip,.state):active{ --chip-tint: calc(var(--chip-tint-base) + 2 * var(--chip-tint-step)); }
:is(.chip,.state)[aria-pressed="true"]{ --chip-tint: calc(var(--chip-tint-base) + 2 * var(--chip-tint-step));
  border-block-end: 1px solid var(--chip-mark); border-inline-end: 1px solid var(--chip-mark);
  padding-block-end: calc(var(--chip-pad-b) - 1px); padding-inline-end: calc(var(--s-2) - 1px); }
:is(.chip,.state)[aria-disabled="true"]{ --chip-tint-base: 0%; --chip-tint-step: 0%;
  --chip-ink: var(--chip-ink-void); --chip-mark: var(--chip-void); cursor: default; }
:is(.chip,.state).is-pending{ --chip-tint-base: 0%; --chip-ink: var(--chip-ink-void); }
:is(.chip,.state).is-pending::before{ block-size: 0; }
@media (pointer: coarse){ :is(a,button):is(.chip,.state)::after{ content: ""; position: absolute;
  inset: 50% auto auto 50%; translate: -50% -50%; min-inline-size: 44px; min-block-size: 44px; } }
```

`chip--s` (20 px) è **vietata** su `a` e `button`: sta sotto i 24 px di WCAG 2.2 § 2.5.8 su puntatore fine, e l'ingrandimento `::after` vale solo su `pointer: coarse` — **misurato 44 × 44 px** in contesto touch. Le pastiglie non interattive non sono soggette a 2.5.8. Il test R9 fa fallire la build se un `a`/`button` porta `chip--s` o `chip--seal`. La regola `.register--dense` è la **meccanica** della guardia R1, che il round 2 dichiarava senza darla: la vista passa `register--dense` al contenitore quando il registro supera dodici righe — `{% if rows|length > 12 %}register--dense{% endif %}`, zero Python — e **tutte** le pastiglie del blocco passano insieme alla misura piccola, misuratore compreso (**misurato**: 20 px, 12 px di corpo tipografico, misuratore a 10 px in fase 2). Un cambio di misura a metà tabella non esiste.

### 4.9 Fasi, markup, e i due punti da convertire a mano

**Fase 1a** — `chip.css` + `apps/core/chips.py` + l'attributo. Il modulo esporta `REGISTER: dict[str, dict[str, str]]` (una chiave per enum, come nella tabella di § 4.3), `STAGE: dict[str, int]` per le undici di `CaseStatus`, `GLYPH: dict[str, str]`, e `def register_for(enum: str, value: str) -> str`, che restituisce `""` se non conosce il valore. Un filtro in `apps/core/templatetags/ile_core.py`, `@register.filter def chip_register(obj)`, legge `obj.status` e il nome dell'enum. Niente cambia di posto: la classe `.state--*` resta dov'è e smette semplicemente di significare qualcosa. **Fase 1b** — `templates/components/chip.html`, contratto `label · register · stage · count · seal · indicative · size · glyph`, che rende `<span class="chip chip--seal" data-register="conforme"><svg class="chip__g" aria-hidden="true"><use href="…#icon-shield"></use></svg><span class="chip__w">Vérifiée</span><span class="visually-hidden"> — …</span></span>`; `components/badge.html` diventa un `{% include %}` verso di esso, contratto `label`/`kind`/`icon` invariato; e **nello stesso commit** si cancellano `register.css:702-744` e `components.css:223-244`. Due punti vanno convertiti a mano perché la cifra sta **dentro** il `blocktranslate`: `documents/partials/register.html:26` e `portal/partials/case_header.html:59`.

### 4.10 Caricamento

Il round 1 diceva «caricato in `templates/base.html` dopo `css/v2/voyage.css` (riga 38)». È **falso**: la riga 38 è un `<link rel="preload" … as="style">` e non applica nessuno stile; l'unico foglio applicato è la riga 39, `main.css`, che fa gli `@import` in ordine di cascata. **L'istruzione corretta è una riga sola**, in coda a `static/css/main.css` dopo `@import url("v3/buttons.css");` — `@import url("v3/chip.css");` — più, facoltativo, un `<link rel="preload" href="{% static 'css/v3/chip.css' %}" as="style">` dopo la riga 38 di `base.html`.

## 5. MOTION — voci per `MOTION_SYSTEM.md` § 6

**Due voci restano cancellate, e la cancellazione è la proposta.** `chip.seal-reveal` inventava una durata di 600 ms inesistente, dichiarava due funzioni dove la regola è una, nominava «DELIZIA» fra le famiglie dove non c'è, e animava `clip-path: inset()` su un elemento che porta già `clip-path: polygon()`. Ma il difetto vero sta a monte: **rivelare un sigillo afferma che l'atto viene apposto adesso**, che è una bugia di causalità su un fatto emesso in passato. `chip.state-swap` pretendeva `view-transition-name: chip-<pk>`: un valore per chiave primaria raggiunge l'elemento solo da un attributo `style` (vietato dalla CSP) o da CSS generato per PK, e mancava l'opt-in `@view-transition`. La causalità del cambio di stato è la famiglia PAGINA e appartiene a `transitions.md`.

| Nome | Funzione | Innesco | Durata | Curva | Proprietà | Stato ridotto | Budget |
|---|---|---|---|---|---|---|---|
| **`chip.hover`** | FEEDBACK | puntatore, solo `@media (hover: hover)`, solo `a`/`button` | `--motion-fast` 180 ms in / `--motion-instant` 120 ms out | `--ease-out` / `--ease-in` | `translate` 0 → −1 px, `background-color` | **la tinta cambia, il sollevamento no** | CSS puro, 0 byte |
| **`chip.press`** | FEEDBACK | `:active` | `--motion-instant` 120 ms | `--ease-in` | `translate` −1 px → 0 | nessuna | CSS puro, 0 byte |

```css
@media (prefers-reduced-motion: no-preference){
  :is(a,button):is(.chip,.state){ transition: background-color var(--motion-instant) var(--ease-in),
    translate var(--motion-instant) var(--ease-in); }
  @media (hover: hover){ :is(a,button):is(.chip,.state):hover{ translate: 0 -1px;
    transition-duration: var(--motion-fast); transition-timing-function: var(--ease-out); } }
  :is(a,button):is(.chip,.state):active{ translate: 0 0; }
}
```

**Il `translate` è dentro il blocco, e lo stato ridotto è dichiarato per quello che fa.** La revisione ha ragione: al round 2 `translate: 0 -1px` stava fuori e sotto `reduce` la pastiglia si sollevava lo stesso. Ora ogni `transition` **e** ogni `translate` stanno dentro `@media (prefers-reduced-motion: no-preference)`. **Rimisurato sotto `reduced_motion: reduce`, in hover reale:** `translate` calcola **`none`** e `transition-property` non contiene né `background-color` né `translate`. E correggo la formula del round 2: lo stato ridotto **non** è «identico al riposo». Il corpo cambia lo stesso — **misurato, alpha 0.13 contro 0.08** — perché una tinta è uno *stato* e non un *movimento*, e toglierla lascerebbe un comando senza feedback, cioè un contenuto in meno; ciò che sparisce è solo il sollevamento di 1 px, istantaneamente. Nulla resta invisibile, nulla resta a metà. Due durate su quattro, due curve su tre, una funzione per voce, nessun overshoot, nessuna molla, nessun `@keyframes`, nessun loop: la pastiglia non consuma il momento firmato della pagina. **Il contatore non scorre**: animare «3» perché è un numero è il «numero che scorre» che MOTION_SYSTEM § 2 ammette solo per un totale calcolato.

## 6. ACCESSIBILITÀ, RTL, FORCED-COLORS, STAMPA

**I tre canali non cromatici, nominati con precisione perché il round 2 li aveva nominati male.** Sono, e sono soltanto: (1) la **parola**, mai abbreviata, mai troncata, mai sostituita; (2) lo **stile** del filetto — `solid` neutro/conforme/rifiuto · `dashed` attesa · `double` sigillo · `dotted` indicativo e non-mappato; (3) la **geometria** del filetto — spessore 1/3/4 px e i filetti di chiusura orizzontali (nessuno in *neutro* e *attesa*, uno sotto in *conforme*, uno sopra **e** uno sotto in *rifiuto*). In fase 2 il glifo è il quarto e la silhouette del sigillo il quinto. **Che cosa non è un canale, e lo dico perché la revisione li contava fra i tre:** la **tinta del corpo** — misurata 1.09–1.17:1 su carta e 1.25–1.36:1 in mezzanotte contro il proprio fondo — è la *silhouette* della vidimazione, cioè ciò che le dà un corpo invece di una parola nuda, e non porta nessun significato da sola; la **pista** del misuratore — misurata 1.27–1.52:1 su carta contro il fondo — non porta significato neppure lei, perché ciò che si legge è la **corsa contro la pista**, misurata 4.61–4.73:1 su carta e 2.86–4.97:1 in mezzanotte sui soli registri che portano una fase. Il misuratore è inoltre **ridondante per dichiarazione** (la parola nomina già la fase) e resta fuori da 1.4.11. I due registri colorati che un daltonico potrebbe confondere — *azione* bruno e *rifiuto* rosso — hanno spessore diverso (4 px contro 3), filetti di chiusura diversi, glifo diverso e parola diversa; **misurato**, ΔE2000 fra le due marche = **22.63** su chiaro e **21.69** su scuro. **Bronzo e pending** sono vicini in V2 (stessa tinta, h ≈ 72°): **misurato**, ΔE2000 = **9.56** su chiaro e **6.26** su scuro. Sopra la soglia percettiva ma non largo, quindi la separazione è **strutturale e dura** — e ora la CSS la produce davvero (§ 4.2): il bronzo non compare mai su una pastiglia che non sia un sigillo, e un sigillo porta **sempre** l'angolo tagliato e il filetto doppio.

**Contrasti — tutti ricomposti e riletti dai pixel in questo round**, otto fondi (i sette del round 2 **più `--min-2`, `--mid-2` e `#0f2547`**, che la revisione chiedeva). `#0f2547` è `--brand-navy`: è il fondo reale di `.section--verso` e `.plate--verso` (`layout.css:149` + `v2/bridge.css:31`), quindi del pannello ÉTAT di `cases/detail.html:190`, e **non** `--mid-1/2/3`. Metodo: rendo la pastiglia sul fondo, leggo col contagocce il pixel del corpo e il pixel della marca, e calcolo il rapporto WCAG 2.x su quei pixel. Colonna «parola» = inchiostro del capitolo sul corpo composto; colonna «marca» = pixel della marca sul fondo.

| Registro | marca chiara | parola / marca su `min-0` | su `min-1` (peggiore) | su `min-2` | su `min-3` | marca scura | su `mid-1` | su `mid-2` | su `mid-3` (peggiore) | su `#0f2547` |
|---|---|---|---|---|---|---|---|---|---|---|
| neutro · attesa | `--ink-2` `#4a5a62` | 13.08 / 6.46 | **12.15** / 6.00 | 13.85 / 6.87 | 14.48 / 7.17 | `--on-dark-3` `#8fa0a3` | 12.37 / 6.44 | 11.23 / 5.85 | **9.76** / 5.10 | 10.84 / 5.61 |
| azione | `--pending-700` `#705434` | 13.12 / 6.29 | **12.19** / 5.85 | 13.90 / 6.70 | 14.52 / 6.98 | `--pending-300` `#d8bd8e` | 11.62 / 9.66 | 10.52 / 8.77 | **9.12** / 7.65 | 10.21 / 8.42 |
| conforme | `--ink` `#15222a` | 12.59 / 14.62 | **11.69** / 13.59 | 13.35 / 15.56 | 13.96 / 16.23 | `--on-dark-2` `#b7c3c4` | 11.51 / 9.68 | 10.40 / 8.79 | **9.01** / 7.67 | 10.05 / 8.44 |
| rifiuto | `--err-700` `#b3261e` | 12.90 / 5.89 | **11.98** / 5.48 | 13.66 / 6.27 | 14.28 / 6.54 | `--err-300` `#f0a49b` | 11.95 / 8.74 | 10.83 / 7.94 | **9.42** / 6.93 | 10.52 / 7.62 |
| nullo (corpo assente) | `--hairline-strong` `#7a868b` | 5.53 / 3.37 | **5.14** / **3.14** | 5.88 / 3.59 | 6.14 / 3.74 | `--on-dark-3` `#8fa0a3` | 6.44 / 6.44 | 5.85 / 5.85 | **5.10** / 5.10 | 5.61 / 5.61 |
| sigillo | `--seal-600` `#8c6d4b` | 13.37 / 4.30 | **12.43** / 3.99 | 14.15 / 4.57 | 14.78 / 4.77 | `--seal-300` `#c7a77e` | 12.09 / 7.72 | 10.96 / 7.00 | **9.52** / 6.11 | 10.63 / 6.73 |

**Peggior parola: 5.10:1** — *nullo* su `--mid-3` — dove 1.4.3 chiede 4.5. La revisione ha ragione: il titolo del round 2, «peggior parola 9.01:1», era contraddetto dalla riga *nullo* della sua stessa tabella (5.53 / 5.14 / 5.10). Il 9.01 è il minimo delle **sole** righe con corpo, non il minimo della tabella; il minimo è **5.10**, e lo scrivo come tale. **Peggior marca: 3.14:1** — *nullo* su `--min-1` — dove 1.4.11 chiede 3.0; sul *nullo* il corpo è assente, quindi il filetto confina solo col fondo. **Semantica.** Il glifo è sempre `aria-hidden="true"`. La pastiglia **non** è un `role="status"`: l'annuncio, dove serve, è **uno solo** a livello di registro, atomico, con la frase intera, mai la cifra nuda. Il sigillo aggiunge al nome accessibile uno `<span class="visually-hidden">` — la classe reale è **`.visually-hidden`** (`base.css:421`). Le due stringhe nuove, con msgid in italiano come tutto il catalogo, da aggiungere a `locale/{fr,it,en,ar}/LC_MESSAGES/django.po`:

| msgid (it) | fr | en | ar |
|---|---|---|---|
| `atto emesso da un'autorità competente` | acte émis par une autorité compétente | act issued by a competent authority | إجراء صادر عن سلطة مختصة |
| `a titolo indicativo` | à titre indicatif | for information only | على سبيل الإرشاد |

Passate entrambe, in tutte e quattro le lingue, attraverso `apps/cms/forbidden.py`: nessuna `FORBIDDEN_PHRASES`, nessun `FORBIDDEN_PATTERNS`, nessun `®`. La prima è nascosta, la seconda è **visibile** (§ 4.7). **`forced-colors`.** Verificato sotto `forced_colors: active` (Chromium emula la media query; **non** ridipinge coi colori di sistema, quindi il ridipinto resta HUMAN_QA). Sopravvivono stile, spessore, altezza del misuratore, i filetti di chiusura e il `clip-path`. Non sopravvive `background-image`: **misurato `none`**, quindi la diagonale del sigillo sparisce e l'`outline` la sostituisce. E va **cancellata** `register.css:800-803`, che oggi appiattisce tutto.

```css
@media (forced-colors: active){
  .chip,.state,.badge{ border-inline-start-color: GrayText; }
  .chip::before,.state::before,.badge::before{ border-inline-start-color: CanvasText; }
  [data-register="nullo"]{ color: GrayText; }
  :is(.chip,.state,.badge).chip--seal{ outline: 1px solid CanvasText; outline-offset: 1px; }
}
@media print{ .chip,.state,.badge{ break-inside: avoid } }
```

**Stampa.** I fondi non si stampano per impostazione predefinita: restano filetto, glifo, parola, filetti di chiusura e angolo tagliato — il sistema regge, ed è per questo che lo stato non sta mai nel colore. Nessun `print-color-adjust`: un px CSS in stampa vale 1/96 di pollice ≈ 0.26 mm, indipendente dalla risoluzione, e un filetto da 0.79 mm è ben visibile. **RTL.** Tutto è in proprietà logiche, quindi filetto, misuratore, contatore e suo filetto si specchiano da soli; si specchia **solo** ciò che è direzionale: il poligono del sigillo e la sua diagonale, che hanno la loro regola `[dir="rtl"]` — **verificato**: `clip-path` mirror, gradiente `-45deg`, `background-position` a sinistra. Non si specchiano glifi, cifre, misuratore. In AR la parola non perde nulla, perché **non le è mai stato tolto nulla**: `text-transform` calcola `none` e `letter-spacing` `normal` in ogni lingua, quindi `:lang(ar) .state` non ha più niente da disattivare. E13 non è mitigata, è **eliminata**. **HUMAN_QA_REQUIRED.** (a) Windows HCM reale, temi *High Contrast Black* e *White*: l'emulazione conserva i colori d'autore, il sistema vero no. (b) NVDA + Chrome e VoiceOver + Safari sul registro documenti: che la colonna ÉTAT non sia annunciata due volte. (c) Stampa reale di `case_file` in A4, FR e AR. (d) Lettura del sigillo e del registro *azione* da parte di un utente daltonico, su carta e su mezzanotte: bronzo contro bruno vanno visti, non simulati (ΔE2000 = 6.26 su scuro).

## 7. PRESTAZIONI

| Voce | Grezzo | Gzip | Nota |
|---|---|---|---|
| `static/css/v3/chip.css` | **6 922 B** | **1 941 B** | `gzip -9` sul foglio **esatto** che questo documento stampa nei nove blocchi, riga di intestazione compresa: 100 righe. Il round 2 dichiarava 6 702 / 2 035 per un foglio che ne misurava 8 213 / 2 552: la cifra era falsa, e la causa era la stessa che rendeva falso § 4.3 — cinquanta selettori `.state--*`. Portandoli a sei il foglio **cala** davvero. In fase 1b cancella `register.css:702-744` e `components.css:223-244`, ≈ 1.4 KB grezzi |
| JavaScript | **0 B** | **0 B** | nessun `chip.js` (§ 5) |
| Immagini / font | **0 B** | — | nessuna icona nuova, nessuno sprite nuovo, nessun URI dati: i sette simboli sono già in `icons.svg`; `--f-mono` e `--f-sans` 400/500 sono già in `static/fonts/` |

**Layout e paint.** «0 layout, 0 paint» era falso e resta ritirato: l'hover transisce `background-color`, che ridipinge. Il numero onesto è **0 layout** — la pastiglia è un `inline-flex` a dimensioni intrinseche, `translate` non riflette, e il contatore riserva la larghezza in `ch` prima di cambiare cifra — e **paint confinato alla scatola della sola pastiglia sotto il puntatore**, misurata al massimo **266.20 × 24 px** a 1440 e 164 × 64 px in colonna stretta. Quel ridipinto è ammesso esplicitamente dalla famiglia HOVER di MOTION_SYSTEM § 2. Non esistono animazioni fuori dal viewport perché non esiste nessuna animazione innescata dallo scroll. Corpo, filetto e misuratore sono **una sola area dipinta**; il `clip-path` del sigillo è statico e non forza un livello di composizione.

## 8. RISCHI E GUARDIE

| # | Che cosa lo farebbe sembrare economico | La guardia |
|---|---|---|
| R1 | **L'arcobaleno**: registri × tinte su una colonna lunga dànno l'aria del gestionale del 2012. | Quattro registri su sei **non hanno croma** (§ 4.1); la tinta è in alpha; oltre dodici righe il contenitore riceve `register--dense` dalla vista e **tutto** il blocco passa insieme alla misura piccola (§ 4.8) — meccanica scritta, non dichiarata. E la regola dura: **una sola colonna di pastiglie per tabella**. |
| R2 | **Il sigillo ovunque**: bronzo su ogni riga smette di significare autorità. | `chip--seal` solo su un fatto **emesso** da un'autorità o da un attore autorizzato — nel codice esiste **un solo** produttore, `VerificationStatus.APPROVED` (§ 4.3) — e **al massimo una volta per riga**, coperto dal test R9. |
| R3 | **Il verde che diventa un'approvazione.** | Risolto alla radice: non c'è verde (§ 4.1), e `chip.css` lo toglie anche a `.badge--success`. |
| R4 | **Il moiré del guilloche.** | Eliminato insieme al guilloche (§ 4.6): non resta nessuna trama periodica. Il solo tratto obliquo è il filetto di chiusura, verificato al pixel a 1× e 2× (§ 4.6). |
| R5 | **Il numero che scorre su un dato che non è un totale.** | Eliminato insieme a `chip.count` (§ 5). |
| R6 | **Due sistemi che convivono per sempre.** | La fase 1a è un **alias**; la 1b cancella `register.css:702-744` e `components.css:223-244` nello stesso commit che introduce `components/chip.html`. La guardia è **numerica**: `scripts/css_class_audit.py` riporta le classi dei template che nessun foglio definisce e fallisce sopra un tetto; il tetto (`CEILING = 382`, riga 39) **scende** nello stesso commit, e il file dichiara «THIS ONLY GOES DOWN». |
| R7 | **Il divario fra classe ed enum torna.** | (a) `.state:not([data-register])` dipinge il filetto `dotted` «stato non mappato», visibile (§ 4.3). (b) **`tests/frontend/test_chip_registers.py`**: importa `core.chips.REGISTER`, itera **tutti** i `TextChoices` dei sette moduli produttori più le tre `status_word`, e asserisce che ogni membro ha un registro fra i sei; legge i registri dal CSS con `re.findall(r'\[data-register="([a-z]+)"\]', (ROOT/"static/css/v3/chip.css").read_text())` e asserisce `set(CSS) == set(REGISTER.values())`; asserisce `"999px" not in css` e `".state--" not in css`. |
| R8 | **L'indicativo scambiato per un difetto.** | Due portatori, non quattro, e il secondo è una parola in chiaro (§ 4.7). |
| R9 | **Il bersaglio che non c'è.** | Test di template in `tests/frontend/test_browser.py`, che già rende le pagine: nessun `a`/`button` porta `chip--s`; nessun `chip--seal` è `a` o `button`; ogni `<tr>` conta al massimo un `.chip--seal`; ogni `.state` reso porta `data-register`. |

## 9. REGISTRO DELLE CORREZIONI DEL ROUND 2

**Fatto.** (1) **La specificità**: registro su `[data-register]` (0,1,0), modificatori su `:is(.chip,.state,.badge).chip--x` (0,2,0) — misurato `#8c6d4b` / `#c7a77e` e `dotted` sull'indicativo in *attesa* (§ 4.2). (2) **La derivazione**: rifatta dai membri degli enum in Python, non dalle parole; le venticinque selettrici morte cancellate con le venticinque vive; tutte le correzioni minime della revisione applicate e nominate, più `RequirementState.EXPIRED`, `ScanStatus.CLEAN` e `ScanStatus.ERROR` (§ 4.3). (3) **La scala interattiva**: riposo e passo per capitolo, hover/active/selected come offese, più le tre righe che non avevano CSS — `[aria-pressed]`, `.is-pending`, il filtro disabilitato — e selected non è più solo tinta (§ 4.8). (4) **`translate`** dentro `prefers-reduced-motion`, misurato `none` sotto `reduce`, e lo stato ridotto riscritto per quello che fa (§ 5). (5) **`white-space: normal`** nella regola base, misurato sui 17 `.entry__actor` e sui badge (§ 4.2). (6) **Secondo canale a *rifiuto***: i due filetti di sbarratura, misurati in `forced-colors` (§ 4.3). (7) **Le tre cifre sbagliate**: peggior parola **5.10:1**, non 9.01; foglio **6 922 / 1 941 B**; contatore **0.02 px** fra 9 e 10 (§ 6, § 7, § 4.7). (8) **Il filetto del sigillo**: banda a `3.95–4.95px`, misurata R = 140, copertura piena (§ 4.6). (9) **L'emendamento 2 respinto**: ripiego `var(--pending-300, var(--pending-700))`, verificato che nessun filetto sparisce, costo dichiarato (§ 0). (10) **I fondi mancanti**: `--min-2`, `--mid-2` e `#0f2547` in tabella, otto fondi (§ 6). (11) **R1**: meccanica `register--dense`; **`chip--s`**: il misuratore funziona e la pista resta sempre scoperta, 5 / 10 / 15 px (§ 4.4, § 4.8). (12) **§ 4.5**: regola ristretta a `.chip__g`, glifo del badge rimisurato invariato (16 px, 1.5, `currentcolor`), e detto per intero che cosa cambia nella scatola dei nove badge.

**Contestato, con la misura.** **Una voce, ed è la prescrizione del rimedio, non la diagnosi.** La revisione prescrive «start the band at 4.95px for a full 1px inside the clip». **Misurato: a `4.95px → 5.95px` il filetto non esiste affatto.** Ho rese le tre varianti fianco a fianco sullo stesso sigillo e letto l'ipotenusa al pixel (`m3.json`, `s3_1.png`, `s3_2.png`): `4.95–5.95` dà R = **235** a 1× e a 2×, cioè il colore del corpo, **zero** pixel di marca — la banda cade per intero dentro il triangolo che il `clip-path` rimuove, perché l'asse del gradiente a 45° cresce **verso** l'angolo tagliato. `4.45–5.45` (round 2) dà R = **189**, cioè **48.4 %** di copertura, non 39 %: la diagnosi della revisione è giusta, la sua cifra è bassa di nove punti e la sua correzione va nella direzione sbagliata. La banda corretta è `3.95–4.95`, che misura R = **140** = `#8c6d4b` pieno. **Seconda contestazione, parziale.** «Due dei tre portatori dichiarati sono sotto la soglia percettiva»: i tre portatori dichiarati sono la parola, lo **stile** e la **geometria** del filetto, e nessuno dei tre è la tinta del corpo o la pista del misuratore. Misurato: parola **5.10–14.78:1**, marca contro fondo **3.14–16.23:1**, corsa contro pista **2.86–4.97:1**. Accetto però la sostanza: il round 2 non diceva che cosa **non** fosse un canale, e § 6 ora lo scrive, con le cifre di entrambi.
