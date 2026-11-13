# V3 — registro di ciò che è implementato, superficie per superficie

Questo file è la sezione D del rapporto richiesto dalla direttiva correttiva («superfici
effettivamente rifatte»). Una riga entra qui solo quando il codice è sul ramo, misurato in Google
Chrome Stable visibile, e i test passano. Le specifiche stanno in `specs/`; le revisioni in
`reviews/`; quello che *non* è ancora fatto sta in fondo, nominato.

## Perché il metodo è cambiato il 24 settembre

Sedici specifiche, due giri di riparazione con revisori indipendenti che applicavano il CSS di
ogni specifica al sito in esecuzione e campionavano i pixel. Esito del secondo giro: **tutte e
sedici ancora respinte**, 223 correzioni obbligatorie contro le 226 del primo, 118 violazioni
contro 108. Il ciclo documento → revisione → documento non converge, e un terzo giro avrebbe
prodotto un terzo elenco della stessa misura.

Quello che invece *converge* è il metodo dei revisori stessi: servire il CSS sul sito vero,
misurare, correggere ciò che si rompe. Da qui in avanti la specifica è la sorgente dell'intento e
l'elenco delle correzioni obbligatorie del revisore è la lista di accettazione; la prova è il
codice sul ramo più la misura in Chrome, non un altro documento.

---

## 1. Bottoni — `static/css/v3/buttons.css` · 24 settembre 2026

**Fonte:** `specs/buttons.md` round 2 + `reviews/` (12 correzioni obbligatorie).
**Sostituisce:** la correzione di una riga di `a79fbb2`; i blocchi bottone di `v2/hero.css` e di
`apps/forum/static/forum/forum.css`.

### Che cosa è entrato

| Elemento | Valore | Dove misurato |
|---|---|---|
| Lastra | 48 px; 40 `--sm`; 56 `--lg`; 24 in riga | vetrina, undici bersagli |
| Materiale | luce verticale 3 % bianco → 3 % inchiostro, invertita alla pressione; **nessuna ombra portata** | pixel: primario `#156d75` in alto, `#0f686f` in basso |
| Hover | il colore del fondo cambia; il bordo e la luce restano | secondario: bordo `#7a868b` a riposo **e** in hover; primario `#156d75 → #11595f` |
| Pressione | `translate: 0 1px`, luce invertita | — |
| Varianti | primary, secondary, danger (**contornato**), quiet/ghost, tertiary/link/text/inline, icon | vetrina |
| Mezzanotte | per contesto `.hero .chapter--dark .on-inverse .forum-cta .forum-hero .forum-banner`; `.btn--inverse` sinonimo | hero: `#7fd1d8 → #a5e0e5`; forum-cta: `#1b2f3a` bordo `#708087` |
| Disabled | colore e forma, mai opacità; `cursor: not-allowed`; nessun cambio in hover | vetrina: `#e3e2dd` / `#d3d2cc`, invariato sotto il puntatore |
| Focus | anello 2 px `--accent-ring` offset 2 px + alone 5 px al 30 %; `--accent-dark` in mezzanotte | tastiera: `:focus-visible` vero, `solid 2px rgb(29,138,147)`, alone `rgba(29,138,147,.3) 0 0 0 5px` |
| Freccia | 3 px nel verso di lettura, in hover **e** focus | RTL: `--dir -1`, `translate -3px`; LTR `+3px` |
| Moto | tutto e solo dentro `prefers-reduced-motion: no-preference` | preferenza attiva: 836 elementi, 0 animazioni residue |
| Colori forzati | primario con seconda linea interna, danger tratteggiato, in riga sottolineato | 61 comandi con bordo, 0 senza forma |
| Arabo | nessun tracking, nessun maiuscolo, minimo 120 px | — |

### Le sette differenze rispetto alla specifica, ciascuna con la misura che la impone

1. **L'hover è un colore, non uno strato.** La specifica dipingeva l'hover su `::before` a
   `inset: -1px`; misurato dal revisore, copriva il bordo del secondario (`#7A868B → #ECEBE6`,
   1,08:1) e la luce del primario (ΔL\* 0,00). Ora cambia `background-color` sull'elemento.
2. **Nessuna ombra sotto un bottone.** La specifica chiedeva un quinto ruolo d'ombra a V2 §2 e il
   revisore ne contava otto letterali nel foglio. §2 ne ammette quattro e §7 vieta le ombre in
   modalità DENSE, dove vive la maggior parte dei bottoni. `grep box-shadow` sul file restituisce
   solo l'alone di focus, che è il letterale di `v2/shell.css`.
3. **I fondi del forum sono mezzanotte.** `.forum-hero` e `.forum-banner` sono navy `#0f2547`;
   con la specifica servita il primario vi misurava 2,42:1. Entrano nei contesti scuri; il
   secondario vi porta un bordo composto `#708087`, 3,73:1 sul navy.
4. **Le varianti in riga vengono dopo le misure.** `btn--link btn--sm` misurava 177 × 40 con un
   filetto 12 px sotto il testo (`portal/messages.html`). L'ordine di sorgente decide.
5. **DANGER resta contornato.** La specifica lo trasformava, senza dirlo, in una lastra piena
   `--err-700` su ogni azione di cancellazione. Il rosso è «solo errore» (V2 §1.3 regola 3) e la
   conferma segue in una modale: la forma contornata che il sito spedisce oggi è mantenuta e
   dichiarata. `--err-700` su `--min-2` 6,27:1; in hover su `--err-100` 5,10:1.
6. **I colori forzati conservano una gerarchia.** Misurato: primario, secondario e danger
   diventavano tutti ButtonFace/ButtonText, identici. Il primario porta ora un secondo contorno
   interno, il danger un bordo tratteggiato: i bordi sopravvivono al contrasto elevato, i
   riempimenti no.
7. **Niente bottone asincrono.** Le facce busy/done e il misuratore di §4.5 chiamano tre funzioni
   di `button.js` che la specifica non scrive. È un componente, non uno stile; arriva col suo
   script.

### Un token nuovo, dichiarato

`--err-300: #f0a49b` — la luminosità chiara del rosso d'errore per un fondo di mezzanotte. V2 dà
al capitolo scuro un verde chiaro e un bronzo chiaro ma non un rosso: `--err-700` su `--mid-3` fa
2,12:1. Stessa tinta, seconda luminosità, come i due token che V2 ha già; 6,93:1 su `--mid-3`.
La specifica delle pastiglie propone lo stesso token per la stessa ragione.

### Contrasti (calcolati, WCAG 2.x)

| Coppia | Rapporto |
|---|---|
| primario: `--min-0` su `--accent` / su `--accent-hover` | 5,69 / 7,67 |
| secondario: `--ink` su `--min-2` · bordo `--hairline-strong` su `--min-0` | 15,56 · 3,37 |
| danger: `--err-700` su `--min-2` / su `--err-100` | 6,27 / 5,10 |
| ghost: `--ink-2` su `--min-0` | 6,46 |
| link: `--accent` su `--min-0` · filetto al 70 % `#549398` | 5,69 · 3,15 |
| mezzanotte primario: `--mid-1` su `--accent-dark` / su `#a5e0e5` | 10,01 / 12,00 |
| mezzanotte secondario: `--on-dark` su `--mid-3` · bordo composto su `--mid-1` | 12,29 · 3,68 |
| navy (forum): `--accent-dark` su `#0f2547` · bordo secondario su navy | 8,73 · 3,73 |
| disabled: `--ink-3` su `#e3e2dd` (esente, dichiarato) | 4,73 |

### Strumento

`scripts/qa_chrome_buttons.py` — stili calcolati **e** pixel, a riposo e sotto il puntatore, con
il puntatore vero (`Input.dispatchMouseEvent`). Tre difetti dello strumento corretti prima di
fidarsene: la cattura ritagliata sull'elemento invece del viewport moltiplicato per il DPR; lo
scorrimento istantaneo, perché quello fluido lasciava il puntatore dove il bottone *era*; la
colonna `:hover` che dice se il puntatore è davvero sull'elemento.

### Che cosa resta aperto sui bottoni

- il bottone asincrono (§4.5) e il suo `button.js`;
- `.forum-hero .btn--primary` non è renderizzato su nessuno dei due server (iscrizione non aperta):
  la regola c'è, la misura sul posto no;
- la pagina di accesso (`/compte/login/`) non è ancora stata misurata con il sistema nuovo.

---

## 2. Pastiglie di stato — `static/css/v3/chip.css` + `apps/core/chips.py` · 24 settembre 2026

**Fonte:** `specs/badges.md` round 3 — la specifica più matura del giro: dodici correzioni chiuse
con misure a pixel, e la sola che avesse già ritirato da sé l'errore del verde (§4.1).
**Fase:** 1a (`.badge`: nove `{% include %}` + il badge di allauth) e **1b** (`.state`: 63
siti su 32 template, ognuno con `data-register` derivato dal produttore; le regole `.state--*` di
`register.css` e il suo blocco a colori forzati ritirati nello stesso commit). I due passi sono
separati apposta: con `.state` nella regola base prima dell'attributo, ogni pastiglia non
convertita si sarebbe dipinta «non mappata» finché durava la conversione.

### L'idea, in una riga

La pastiglia è un timbro di registro: **la parola è sempre nell'inchiostro del capitolo**, il
colore vive solo nella marca (filetto + corpo all'8 %), e il significato è portato tre volte
senza colore — parola, **stile** del filetto, **geometria** del filetto. *Conforme* non ha croma:
filetto d'inchiostro, un filetto di chiusura sotto, e nessun verde, perché questa piattaforma non
approva nulla.

### Il registro nasce dall'enum, non dalla parola

Undici parole CSS coprivano cinquantatré membri di enum: `expired` è «pezzo da ridepositare» per
un requisito documentale e «edizione archiviata, non porta nulla» per il forum. `apps/core/chips.py`
mappa **per produttore e per membro** — sedici produttori, tutti i membri — e il DOM riceve
`data-register`. Un valore sconosciuto non riceve l'attributo e la CSS lo dipinge **puntinato**:
visibile, e testato.

`tests/frontend/test_chips_registry.py` importa le tredici enum reali e verifica la tabella nei
due versi (membro senza registro; riga per un membro che non esiste più), più il vocabolario dei
tre `status_word()` della selezione, più la regola legale: `closed` è sempre *neutro* o *nullo*,
mai *conforme*.

### Misurato in Chrome, vetrina, sette `kind`

| kind | registro | filetto | marca | altezza | sopra/sotto | parola |
|---|---|---|---|---:|---|---|
| neutral · info · primary | neutro | solid 3 px | `--ink-2` | 24,00 | 0 / 0 | `--ink` |
| pending | attesa | **dashed** 3 px | `--ink-2` | 24,00 | 0 / 0 | `--ink` |
| warning | azione | solid **4 px** | `--pending-700` | 24,00 | 0 / 0 | `--ink` |
| success | conforme | solid 3 px | `--ink` | 24,00 | 0 / **1** | `--ink` |
| error | rifiuto | solid 3 px | `--err-700` | 24,00 | **1 / 1** | `--ink` |

Altezza esatta a 24 px anche con i filetti di chiusura (compensati nel padding). `white-space`
`normal`, `text-transform` `none`. Corpo: `oklab(… / 0.08)`, cioè la marca all'8 %.
**Colori forzati:** cinque forme distinte sulle sei visibili — solid 3, dashed 3, solid 4, 3 + 1
sotto, 3 + 1 sopra e sotto — con marca e parola in `CanvasText`. Il sesto (*nullo*, 1 px +
`GrayText`) e il sigillo (doppio + `outline`) sono in vetrina scritti a mano.

### Fase 1b — i 63 siti `.state`, misurati sulla piattaforma con la sessione QA

Quattro produttori in più rispetto alla tabella della specifica, trovati camminando i siti:
`academy.EnrolmentStatus` (completato → *conforme*: un fatto di frequenza, la docstring dell'enum
dice che nessuno dei quattro stati è un'approvazione), `academy.gap` (coperto → conforme, parziale
→ attesa, mancante → azione), `selection.EvidenceStatus` (bloccato → attesa, come vuole la
specifica per «bloqué»), `selection.SelectionStage` (sospeso → azione, concluso → neutro). I
letterali seguono la regola parola → registro della specifica e le sue sei eccezioni nominate;
**tre scostamenti** dichiarati, tutti etichette che non sono stati: «étape actuelle» (una
posizione, non un compimento) → neutro invece di conforme; «Nouveau» e «note interne» (tipi, non
stati) → neutro invece di attesa.

Sessione creata lato server e cookie consegnato al browser via CDP (`scripts/qa_chrome_signin.py`,
portato sul client proprio): nessuna credenziale digitata. Misurato su 8771, `qa-person`:

| Pagina | Pastiglie | Registri visti | Non mappate | Altezza |
|---|---:|---|---:|---|
| cruscotto | 10 | attesa ×5, neutro ×4, neutro **fase 1** (corsa 7 px) | 0 | tutte 24 |
| fascicolo | 7 | attesa ×5, neutro, neutro fase 1 | 0 | tutte 24 |
| registro documenti | 11 | attesa ×6, azione («Expiré», 4 px), conforme («Valide»), rifiuto («Non valide», sbarrato), neutro ×2 | 0 | tutte 24 |

**Uno scostamento dalla specifica, imposto dalla misura:** nelle celle di tabella la pastiglia non
va a capo. Il `white-space: normal` della specifica è la garanzia per una colonna stretta e fissa
(la voce di registro a 180 px va a capo invece di troncarsi); ma una tabella a larghezza automatica
comprime in proporzione ogni cella che può andare a capo, e «À faire» sul cruscotto misurava
**44 px** — due righe da 20 più il padding. Con `nowrap` dentro `td`/`th` il min-content della
cella è l'etichetta intera e la tabella dà alla colonna ciò che serve; sul telefono la tabella
scorre già dentro `.scroll-x`. Rimisurato: 24 px.

**Preferenze sulle pagine della piattaforma** (le superfici che `ACCESSIBILITY.md` G-26 nomina):
cruscotto, registro documenti e fascicolo — 246–252 elementi ciascuno con movimento ridotto,
nessuno invisibile; 11–14 pseudo-elementi ciascuno sotto colori forzati, **nessuno perduto**,
compresa la guida `aria-current` del binario di navigazione.

### Che cosa chiude, della vetrina

- §3.4 — `badge--primary` non è più dipinto col navy del marchio: `primary` → *neutro*.
- §3.1 — la classe `badge--success` resta nel markup ma non porta più colore: il registro
  `conforme` è distinguibile da `info` per geometria, non per tinta, e la regola resta intera.
- §3.8 — il raggio 999 delle «pillole» di V2 §2 è superato dalla decisione della specifica: 2 px
  sul lato finale, 0 sul filetto. Non è un timbro tondo, è una vidimazione.

### Che cosa resta aperto sulle pastiglie

- **Fase 2**: `templates/components/chip.html` (glifo, contatore, sigillo, qualificatore), le due
  stringhe nuove nei quattro cataloghi, `register--dense` nelle viste.
- Token: `--pending-300` e `--err-300` sono dichiarati nei fogli V3; vanno in `v2/tokens.css`
  quando la palette viene riconciliata (§3.2 della vetrina: il verde `--ok-*` da decidere).

---

## Non ancora implementato

Navbar · hero-doorway (le quattro traiettorie) · overlays (modale, tiroir) · pastiglie fase 2
(sopra) · backgrounds · scroll ·
transitions · imagery (Pexels) · public-sections · auth · platform-shell · person-dashboard ·
case-file · data-surfaces · company-forum-academy.
