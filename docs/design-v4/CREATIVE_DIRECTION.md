# CREATIVE DIRECTION V4 — «Il portico e la console»

Stato: **DIREZIONE UNICA, DECISA** · 24 settembre 2026, rivista dopo il chiarimento del committente delle
20:58 · Executive Creative Director (§6 della direttiva)
Vincoli assoluti (immutati): testi bloccati e `apps/cms/forbidden.py` · responsabilità degli attori,
workflow, IAM, privacy, sicurezza · WCAG 2.2 AA · prestazioni · Django come cuore · marchio ufficiale e
arco della porta (`docs/design-v2/BRAND_ASSETS.md`) · «nessun colore significa mai approvato»
(`static/css/tokens.css` §STATE, regola **legale**) · nessuna funzione o dato inventati · CSP
`script-src 'self'; style-src 'self'`.
Non più vincolanti (chiarimento 20:58): la direzione editoriale, il serif dominante, folio/registro, la
palette V2 come dogma, i bottoni V3, sidebar/navbar/superfici precedenti, il livello di moto V2, il
divieto V2 di vetro/gradienti/raggi, «DENSE vieta le ombre», «raggio 2 px».
Materiale distillato: `21ST_RESEARCH.md` (21 categorie, riletto dopo le 20:58), `UI_UX_PRO_MAX_AUDIT.md`
(§11: analisi elemento per elemento), i BEFORE `docs/qa/chrome/design-v4/before/01…08.png`.
Fondazione tecnica: `DESIGN_SYSTEM_V4.md` — ogni numero qui è coerente con quel file, e ogni coppia
di colori nuova ha il rapporto WCAG 2.x calcolato e stampato là (§1.9).

Questo documento non offre opzioni.

---

## 1. L'idea

Italy Legal Entry è **un portico e una console**. Il **portico** è il sito pubblico: una soglia
architettonica — l'arco del committente, la chiave, i gradini — attraverso la quale quattro pubblici
(persona, impresa, istituzione, università/formazione) entrano in un ecosistema regolare. Qui vivono la
luce a strati (mesh navy + teal), la fotografia curata, il display Newsreader nei momenti scelti, il
moto immersivo, il racconto per capitoli. La **console** è la piattaforma: uno strumento operativo del
2026 — rail di navigazione a icone su navy, barra di contesto in vetro, pannelli di lavoro con
profondità reale, righe che sono righe e azioni che sono bottoni, pastiglie a pillola che dicono la
verità senza emettere verdetti, una tipografia UI digitale (IBM Plex Sans) stretta e tabellare, moto
micro e causale con molle. Le due metà sono lo stesso prodotto perché condividono **una** materia
(carta minerale + navy-mezzanotte evoluto dal navy del marchio), **un** accento interattivo in due
luminosità e un gradiente (`--accent #0f6a72` → `--accent-2 #12777f`, `--accent-dark #7fd1d8`),
**una** scala di raggi (4/6/10/14/20/full), **una** scala di profondità (0–4 con ombre a due strati),
**un** sistema di moto (4 durate, 2 molle, 3 curve, 15 pattern) e **una** famiglia di segni (lo
sprite ILE + l'arco). Un team senior internazionale nel 2026 costruirebbe esattamente questo per un
ecosistema legal-tech istituzionale Italia↔Marocco: un'identità architettonica propria (non un logo su
un template), un prodotto operativo che compete con Linear, Mercury e Attio in grammatica
d'interazione, e una disciplina legale che nessun SaaS ha (il colore non giudica, il testo bloccato
è intoccabile, nessun dato finto).

Perché **non è editoriale**: il serif compare solo nel display pubblico (hero, titoli di sezione,
titoli del forum); nessuna schermata operativa lo usa, neppure per il titolo di pagina; spariscono
folio, numerali «01/02» in Newsreader, filetti di registro, tavole da documento amministrativo, link
sottolineati come azioni, barre laterali di solo testo. Perché **non è SaaS generico**: carta
minerale e navy del marchio, non zinc/slate su bianco; Newsreader + IBM Plex, non Inter; un accento
teal con il suo gradiente, nessun viola; nessuna card-con-icona-in-quadrato; nessun KPI finto; la
porta a quattro vie come oggetto firma che nessun altro ha. Perché **non è shadcn**: nessun componente
installato; ogni pattern 21st è distillato e riscritto in HTML Django + CSS del sistema + Motion
vanilla; le pastiglie portano il registro nella forma, non nel colore; le superfici si sollevano per
ruolo, con ombre disegnate e non con `shadow-lg` su tutto.

## 2. I sette pilastri visivi

| # | Pilastro | Regola concreta | Anti-regola |
|---|---|---|---|
| 1 | **Materia minerale, luce navy** | Capitoli chiari su carta minerale (`--min-*` V2 conservati); capitoli scuri su **navy-mezzanotte evoluto dal marchio** (`--mid-1 #0b1a33`, scala in DS §1.2) con mesh radiale navy 22 % + teal 8 %; profondità 0–4 con ombre a due strati (chiave + ambiente), vetro su barre appiccicose, scrim e un pannello hero. | Nessuna ombra fuori dai sei ruoli; vetro mai su card statiche o sul contenuto; nessun blob, nessun mesh saturo, nessun gradiente viola. |
| 2 | **Una porta, quattro vie** | L'arco (`doorway__arch`, viewBox 380×507, raggio 189,25) resta la sola grafica firma; in V4 spiega le quattro vie (§4). L'arco intero compare **solo** nell'hero e nel pannello sinistro del login. | Nessun campo di tracciati casuali, nessuna coordinata, nessun «svg», nessun «Suspendre le mouvement»; niente porta nel cruscotto. |
| 3 | **Due registri tipografici, una superfamiglia** | Pubblico: Newsreader (display, titoli di sezione) + IBM Plex Sans; piattaforma: **solo IBM Plex Sans** (400/500/600), scala UI 28/20/17/15/14/13/12/11, cifre tabellari su ogni dato; riferimenti in IBM Plex Mono; arabo in IBM Plex Sans Arabic — **la stessa superfamiglia** (DS §3.1). Icone: `static/img/icons.svg`, tratto 1,5 px, 16/20/24. | Serif su cruscotto, documenti, wizard, fascicolo, B2B, auth: **mai** (eccetto il wordmark). Nessuna emoji, nessuna icona di libreria estranea, nessun Garamond come UI. |
| 4 | **Il colore non giudica** | Un accento per link/CTA/focus, in gradiente sulle superfici primarie. Stato = parola + glifo + stile del bordo; il colore della marca dice solo «qualcuno deve agire» (`--pending-700`), «rifiutato/invalido» (`--err-700`), «emesso da un'autorità» (`--seal-600`). `conforme` è inchiostro senza croma. | Nessun verde = approvato; rosso solo errore; bronzo solo sigilli; nessun titolo con l'accento. |
| 5 | **Il moto è informazione, e ce n'è** | Quattro durate (120/200/320/480), due molle, tre curve, quindici pattern (DS §7); IMMERSIVE alto su hero, vie, processo, forum: disegno dei tracciati, capitoli che cambiano fondo allo scroll, reveal a maschera, corrente ambientale; console MICRO/INTERACTIVE: molle di layout, indicatori che traslano, chip che cambiano parola. ≤ 2 elementi chiave animati per vista; reduced-motion = completo e fermo. | Nessun overshoot, nessun `fade-in-up` a tappeto, nessuno scroll-jacking, nessun loop su un indicatore di stato. |
| 6 | **Superfici che lavorano** | Informazione e azione separate nello spazio: identità a inizio riga, stato al centro, azione a fine riga come bottone; ogni lista principale è un componente (DocumentRow, Table, Timeline); ogni pagina operativa ha un ContextHeader con **una** azione primaria. | Nessun link sottolineato come azione; nessuna tabella per la collezione documenti della persona; nessuna pagina con otto card uguali; nessun `<ul>` nudo. |
| 7 | **Le immagini sono documento, non decoro** | Una libreria (§5): un grading, tre rapporti, raggio `lg` o a filo di capitolo, ≤ 5 fotografie nel corpo della home, 0 sulle schermate operative. | Niente strette di mano, valigie, aeroporti, bandiere, barche, sorrisi in posa, stock evidente. |

## 3. Le otto pagine campione — composizione

Convenzioni: «L0…L4» = livelli di profondità (DS §2); recipe di sfondo NEUTRAL/SOFT/DARK/BRAND/
IMMERSIVE/DATA/FOCUS (DS §1.4); «21st n» = categoria di `21ST_RESEARCH.md`; «UIUX» = decisione
accettata in `UI_UX_PRO_MAX_AUDIT.md`. Griglia pubblica 12 colonne, gutter 24, contenitore 1176/1320/
1440. Console: rail 64 (248 aperta) + workspace max 1320 + inspector 320.

### 3.1 Homepage pubblica (`/fr/`, gate A) — IMMERSIVE

Livelli d'intensità (§33): hero **alto** → vie **alto** → processo **alto** → spiegazione **calma** →
forum/ecosistema **alto** → news **medio** → piè di pagina **rifinito**. Scroll: il fondo dei capitoli
transisce (navy → carta → navy) con `animation-timeline: scroll()` sul confine di sezione (DS §7,
pattern «page enter» pubblico); la barra cambia stato a 24 px.

1. **Hero** (IMMERSIVE: `--mid-1` + `--mesh-dark` + grana 3 %, ≤ 100 vh desktop, ≤ 110 % del viewport
   a 390): griglia **6/6** da 1280 px (era 7/5: il palcoscenico della porta ha bisogno di 560–640 px).
   Sinistra: eyebrow bloccata «ORIENTATION · FORMATION · MOBILITÉ RÉGULIÈRE» (Plex 11/16 600, .06em,
   `--accent-dark`), H1 bloccato in Newsreader 300 `--t-display` (**clamp 44→76**, non più 100: il
   titolo è co-protagonista, non padrone) che si rivela riga per riga (stagger 60 ms, 480 ms), lead
   corsivo bloccato, due CTA bloccate: PRIMARY a gradiente scuro 44 px + SECONDARY. Destra: **il
   palcoscenico della porta** (§4) con la **legenda in vetro** (`--glass-dark` + blur 16, L3). Sotto
   l'hero **sparisce la striscia** con coordinate, «svg» e «Suspendre le mouvement» (§5): nessun
   sostituto. Isoipse: al massimo due rilievi, opacità ≤ 8 %, dietro il testo. Moto: arco tracciato una
   volta 900 ms → quattro vie disegnate 900 ms con stagger 120 → legenda 200; oggetto vivo della
   pagina = la corrente lungo le vie (28 s, §4.4). Reduced: tutto completo dal primo frame.
2. **Le quattro vie** (`_entrances.html`, 21st 18 + 13; SOFT `--min-1`): quattro pannelli L1 in griglia
   **2×2** a ≥ 1024, non zig-zag, ognuno con glifo attore dallo sprite in un disco 40 px `--accent-wash`
   (person/building/institution/university; i «landform» V2 sono ritirati), titolo bloccato
   `p3.entrances.{actor}.title` in Plex 22/28 600, gloss bloccata 15/24, CTA bloccata come bottone
   SOFT 36 px con freccia; l'intero pannello è il target. Hover: sollevamento L1→L2 (ombra 2) +
   **bordo a gradiente** (`--accent-2` → trasparente, via mask, 1 px) + **spotlight** radiale 6 %
   dell'accento che segue il puntatore (unico luogo del sito con spotlight) + linea di via 2 px nel
   colore di via (`--route-n`, mai da sola). Sotto 720: lista verticale. Quando l'hero evidenzia una
   via (§4.3), il pannello corrispondente riceve `is-related` (stesso stato hover).
3. **Il processo** (`_pathways.html`, DARK + mesh, secondo capitolo scuro): rotta a sette stazioni (le
   sette tappe bloccate di `apps/portal/services.py:JOURNEY_STEPS`) `stroke-dashoffset` legata allo
   scroll (`scroll()`/`animation-timeline`, mai temporale), frontiera MA→IT fra la 3ª e la 4ª tappa
   (campo `side`), stazioni come nodi con anello che si accende al passaggio, `<ol>` reale sotto l'SVG
   con responsabile e glifo. Sotto 720 verticale.
4. **Orientation** (`_orientation.html`, **BRAND**, l'unico recipe brand della pagina): pannello L2 su
   `--grad-brand` (135°, `#d9eef0` → `#eef6f7`), titolo Plex 22/28 600, testo bloccato, CTA primaria a
   gradiente. Nessuna fotografia.
5. **Ecosistema / spiegazione lunga** (`_ecosystem.html`, NEUTRAL, calmo): testo bloccato a 65ch,
   **due** fotografie 3:2 (dialogo istituzionale; formazione professionale) raggio `lg`, reveal a
   maschera 320 ms una volta, scala 1,02 in hover; nessuna card.
6. **Progetto pilota** (`_pilot.html`, SOFT): scheda L1 a lato, chip `chip--seal` per la fonte
   d'autorità; mai «canale autorizzato».
7. **Fiducia / promotore** (`_trust.html`, NEUTRAL): lock-up promotore, sigilli; nessun muro di numeri.
8. **Espace réservé** (`_reserved.html`, BRAND-dark: `--grad-brand-dark`): accesso alla console, bottone
   primario scuro; qui il registro cambia verso la console (anticipa il login).
9. **News** (`_news.html`, NEUTRAL, medio): tre schede L1 con immagine 3:2, data tabellare, titolo
   Plex 17/24 600; hover: L2 + scala immagine 1,02.
10. **Antifrode + banner** (NEUTRAL, notice): testi invariati; notice con la pastiglia V4 `azione`.
11. **Piè di pagina** (`--mid-0`): due righe come V2 §8.7; glifo arco+gradini come chiusura, 24 px.

Azione primaria della pagina: la prima CTA bloccata dell'hero. Immagini: porta + 2 + 3 = entro il tetto.

### 3.2 Navbar / mega-navigazione (gate A) — signature component (§13; 21st 5, 21)

- **Barra istituzionale** 32 px (era 36) `--min-1`: **solo** il promotore. Lingua e accesso
  **scendono nell'header**.
- **Header** 64 px `--min-2`, hairline sotto: lock-up ufficiale 38/20 a inizio riga; voci **Personnes ·
  Entreprises · Forum Vénétie–Maroc · Projet** (Plex 15/20 500) con **indicatore attivo** = barra 2 px
  `--accent` che **trasla** fra le voci (`spring-snappy`); a fine riga: **controllo lingua segmentato**
  FR · IT · EN · ع (track `--min-1` raggio full 32 px, thumb `--min-2` + ombra 1), **«Espace réservé»**
  come bottone SECONDARY 36 px con `icon-lock`, ricerca come IconButton 40 (`icon-search`) che apre il
  pannello.
- **Scroll > 24 px**: la barra istituzionale esce; l'header passa a **56 px** con fondo
  `--glass-light` `rgba(251,250,248,.85)` + `backdrop-filter: blur(12px) saturate(1.2)` e hairline
  che appare in opacità; il lock-up scala **come unità** 38→32; transizione 200 ms `--ease-layout`.
  Contrasto sul caso peggiore (composito su carta `#faf9f7`): inchiostro 15,42, accento 6,00, bordo
  secondario 3,56. Sul capitolo navy la barra resta **carta** (non si scurisce): il composito
  `#e8e8e7` a 92 % dà inchiostro 13,23, accento 5,15, bordo 3,05 — l'header usa 92 % quando sta sopra
  un capitolo scuro (classe impostata dallo `IntersectionObserver` del capitolo).
- **Mega-menu**: si **espande dal bordo inferiore** della barra a tutta larghezza: superficie L3
  `--min-3`, ombra 3, raggio `xl` agli angoli inferiori, altezza auto ≤ 420 px, tre colonne 4/5/3:
  (a) voci con glifo 20 px in disco 32 `--accent-wash` e descrizione 14/20, voci a stagger 40 ms;
  (b) titolo Plex 22/28 600 + testo bloccato + «Voir l'espace →» come bottone LINK; (c) **una**
  fotografia 3:2 curata per sezione (lazy), raggio `lg`. Entrata 200 ms `--ease-enter` (opacity +
  translateY −8→0 + `clip-path` inset dal bordo), uscita 120 ms `--ease-exit`. Frecce fra le voci, Esc
  chiude, focus restituito.
- **Pannello ricerca** (21st 21): nel mega-menu, campo 44 px con autocomplete sui titoli delle pagine
  pubbliche (JSON statico al build), gruppi per sezione; niente overlay a schermo intero.
- **Mobile ≤ 1279**: cassetto a schermo intero L4 su `--min-2` (translateX dal lato di lettura,
  320 ms `--ease-enter`, scrim + blur 6): lingua segmentata in testa, voci 52 px con sezioni
  `<details>` (chevron che ruota 200 ms), CTA in fondo, Esc chiude.

### 3.3 Login (`/compte/login/`, gate B) — DARK + FOCUS (§46; 21st 6; UIUX toggle password)

Composizione **divisa 5/7** da 1024 px. Sinistra (5 colonne, IMMERSIVE: `--mid-1` + `--mesh-dark` +
grana): lock-up variante scura in alto; al centro **la porta completa** (arco tracciato una volta
900 ms, **fotografia del titolare dentro l'arco** a opacità .5, chiave che si assesta, gradini) a
320 px; in basso, su una **striscia in vetro** (`--glass-dark`, blur 16, hairline-dark-strong) la sola
riga di testo bloccato esistente sul sostegno («Besoin d'aide ? Écrivez-nous : contact@…»). Nessuna
tagline, nessuna citazione, nessun volto. Destra (7 colonne, FOCUS: `--min-0` + `--light-focus`):
**foglio L2** 480 px max, raggio `xl`, padding 40, hairline: titolo **Plex 28/36 600** «Connexion»
(non più serif), testo bloccato di invito 15/24, campi V4 44 px raggio `md` (`Courriel`,
`Mot de passe` con toggle mostra/nascondi **con etichetta**), «Mot de passe oublié ?» come LINK,
bottone PRIMARY a gradiente **52 px** (`lg`, l'unico della pagina) con stato in carico (misuratore a
tacche) e stato successo (spunta 320 ms) prima del redirect. Sotto 1024: fascia navy 120 px con mesh e
il glifo arco+gradini (non la porta intera), poi il foglio a tutta larghezza. Dopo l'accesso:
crossfade 480 ms del `<main>` con la rail che entra dal lato di lettura (pattern «page enter»
pubblico→console).

### 3.4 Dashboard Persona (`/fr/espace-reserve/`, gate C) — NEUTRAL (§47; 21st 1, 11, 20)

Shell §3.9. Workspace `--min-0`, griglia 12, gutter 24, padding 32.

1. **ContextHeader** (L0): riga di saluto Plex 15/24 `--ink-2` («Bonjour» è previsto da §47; passa
   dalla revisione copy §92, altrimenti il nome dell'account) · titolo **«Tableau de bord»** Plex
   28/36 600 · riga meta: riferimento `E46E03B461` in Plex Mono 13/20, chip «Orientation terminée»
   (registro da `apps/core/chips.py`), «depuis le 21.09.2026» 13/20 tabellare · a fine riga
   **l'azione primaria** della prossima tappa (PRIMARY 44), se esiste.
2. **Riga 1 — 8/4**: pannello **«Prochaine étape»** L2 raggio `lg` (l'unico L2 a riposo; **bordo a
   gradiente** 1 px `--accent-2`→trasparente sul lato iniziale invece del filetto V2) con titolo Plex
   20/28 600, testo bloccato, ResponsibilityBar («L'autorité compétente» + glifo `shield` + trama
   «linee», «Cette étape ne dépend pas de vous» 14/20 `--ink-2`); a destra pannello **«Dossier»** L1:
   OBJECTIF · ÉTAT · RESPONSABLE · AVANCEMENT con il **misuratore a cinque tacche** («0 sur 5 éléments
   complétés», dato reale), tacche raggio full che si riempiono 320 ms con stagger 60 al caricamento.
3. **Riga 2 — 12**: **JourneyRail** orizzontale (sette tappe bloccate, nodo corrente con anello
   `--accent` 2 px + alone 6 px `--accent-wash` e «Vous êtes ici», frontiera MA→IT, responsabile per
   tappa); la linea si disegna una volta (900 ms), poi ferma. Sostituisce «01 MON PARCOURS / Où j'en
   suis».
4. **Riga 3 — 7/5**: **«Mes documents»** come HealthStrip + le tre pièce più urgenti come DocumentRow
   compatte + LINK «Mes documents»; **«Mes échéances»**: le tre scadenze più vicine con urgenza
   progressiva, oppure EmptyState.
5. **Riga 4 — 6/6**: **Communications** (ultimi messaggi/helpdesk, o EmptyState) · **Academy**
   (progresso reale se iscritto, altrimenti EmptyState con azione).
Tre misure di pannello: nessuna «griglia di otto card uguali», nessuna tessera KPI. Moto: MICRO — page
enter 200, pannelli con stagger 40 (max 6), hover di pannello L1→L2, chip che cambiano parola.

### 3.5 Mes Documents (`/fr/espace-reserve/mes-documents/`, gate C) — **pagina pilota e di controllo** (§16, §85; 21st 8, 14, 20, 4, 15; UIUX nowrap, schede mobile, reflow filtri, filtro in URL)

Da «pagina editoriale + tabella» a **DOCUMENT WORKSPACE**. Il BEFORE deve sembrare ovviamente
obsoleto: la rail a icone al posto della lista di link; la barra di contesto in vetro al posto della
barra navy con il wordmark serif; un titolo UI e una striscia di salute al posto del titolo da rivista;
un foglio di lavoro con righe sollevabili al posto della tabella con filetti; bottoni al posto dei link
sottolineati; pillole con glifo al posto dei rettangoli grigi.

1. **Workspace header** (L0): titolo **«Mes pièces»** (bloccato) Plex 28/36 600 · la frase di contesto
   bloccata 15/24 `--ink-2` a 65ch · riferimento dossier in mono a fine riga · **azione primaria** a
   fine riga: l'azione di deposito esistente per la prima pièce in MANQUANT/À REMPLACER, con
   l'etichetta che ha oggi; se non ce n'è, nessun bottone.
2. **HealthStrip** (L1, raggio `lg`, padding 20): barra segmentata **10 px** raggio full con **sei
   registri** (conforme · neutro · attesa · azione · rifiuto · nullo) a larghezze proporzionali dai
   conteggi reali di `RequirementState`, gap 2 px, segmenti che si riempiono 320 ms `--ease-layout` al
   caricamento; ogni segmento **è un filtro** (hover: +2 px di altezza, tooltip con il conteggio);
   sotto, la didascalia bloccata «7 pièces demandées · 1 sur 7 validées · 4 en attente» con le cifre
   28/32 500 tabellari.
3. **SegmentedControl** (`<fieldset>` di radio nativi, track `--min-1` raggio full 36 px, thumb
   `--min-2` + ombra 1 che trasla `spring-snappy`): **Tous** + le etichette dell'enum
   `apps/documents/models.py` (Manquant · Déposé · En examen · Valide · Non valide · Expiré · À
   remplacer) con conteggio; stato nel query string (`?état=`). La lista di sei parole di §16
   («À fournir», «Validé») contiene parole assenti dall'enum: registrata come richiesta del committente,
   entra nel DOM solo dopo una decisione copy. Sotto 480 il segmentato va a capo. A fine riga: campo di
   ricerca 44 px sul registro.
4. **DocumentCollection** (foglio DATA L1 `--min-2`, raggio `lg`, hairline; righe L0 separate da
   hairline, min 64 px): ogni **DocumentRow** in griglia a sette zone
   `[identità 4fr] [stato 1.5fr] [responsabile 2fr] [scadenza 1.5fr] [salute 1fr] [azione auto] [menu 40px]`:
   - identità: glifo `document` 20 px in disco 32 `--min-1`, titolo Plex 15/24 500 `--ink` (**non più
     link sottolineato**), «version n» 13/20 `--ink-3`;
   - stato: chip V4 pillola con glifo e registro (Manquant = azione, Déposé = neutro, En examen =
     attesa, Valide = conforme, Non valide/Expiré = rifiuto, À remplacer = azione) — mappatura in
     `apps/core/chips.py`, non nel template;
   - responsabile: **Avatar/Glyph** 24 px raggio full (person/building/institution/university/shield/
     marchio) + tipo attore 14/20 + nome reale se c'è; nessun volto finto;
   - scadenza: data tabellare 14/20 + urgenza (NORMAL nessuna · UPCOMING `icon-calendar` · SOON
     `--pending-700` + `icon-clock` · OVERDUE `--err-700` + `icon-warning`);
   - salute: «expire dans n j» / «en révision» quando il dato esiste;
   - azione primaria: bottone `btn--sm` 36 px — PRIMARY a gradiente per l'atto dovuto dalla persona,
     SECONDARY «Consulter» per le pièce in esame/depositate/valide; la pièce bloccata dalle CGU mostra
     il bottone PRIMARY **«Accepter les Conditions d'utilisation»** (testo esistente) e la parola
     «Bloqué» passa nella zona stato come qualificatore mono 12 px accanto al chip;
   - menu: IconButton 40 `icon-menu` → popover L3 con cronologia versioni, download, sostituzione.
   Riga: hover **L1 sollevata** (`--surface-hover` + ombra 1, 120 ms), focus-within anello inset,
   `<details>` per il motivo di rifiuto (testo esistente) e le versioni: apertura con `spring-soft`.
5. **Mobile < 768**: **DocumentCard** impilate (L1, raggio `lg`, padding 16): titolo · chip · glifo +
   responsabile · scadenza · bottone a tutta larghezza; menu nel piede. Nessuna tabella.
6. **Stati**: EmptyState per filtro senza risultati (glifo `search` 48, frase, azione «Tous»); errore di
   rete come notice con riprova; deposito con `Upload` flagship (dropzone L1 tratteggiata → piena e
   `--accent-wash` al drag, progresso reale, chip di stato che cambia parola).
Moto: INTERACTIVE — thumb del segmentato, righe che si riordinano al filtro (`spring-soft`, FLIP su
transform, mai su liste > 40), chip che cambia parola, `<details>`, strip che si riempie.

### 3.6 Fascicolo digitale (`/fr/espace-reserve/dossiers/<id>/`, gate D) — NEUTRAL + DATA (§48; 21st 11, 8, 9)

Workspace **diviso 8/4** da 1280 px (12 sotto, inspector in coda).

1. **ContextHeader** con eyebrow `DOSSIER`, riferimento mono, titolo **«Dossier»** 28/36 600, riga meta
   (objectif · chip état · responsable con glifo · misuratore a cinque tacche) e **una** azione
   primaria; scrollando diventa una barra **in vetro** L3 compatta 56 px appiccicosa (titolo + chip +
   azione) con `view-transition-name` condiviso.
2. **Colonna 8** — quattro pannelli con titoli 20/28 600, nell'ordine delle domande di §48: *Dove
   sono* → **JourneyRail verticale descrittivo** (tappa · responsabile · stato · data; nodo corrente con
   anello e alone; frontiera MA→IT; `aria-current="step"`, ancore per tappa); *Cosa viene dopo* →
   pannello «Prochaine étape» L2; *Cosa manca* → checklist «Ce qui vous est demandé» come **Table**
   semantica (fondamento, chip, azione come bottone; cambio di stato via form a pagina con conferma) +
   HealthStrip; *Chi è responsabile* → ResponsibilityBar per tappa e intervenants con Avatar/Glyph.
3. **Inspector 4** (L1, appiccicoso): «Où en est votre demande» come **Timeline** append-only (nodo
   12 px, spina hairline, date tabellari, responsabile; l'ultimo nodo si accende 320 ms al
   caricamento), pré-évaluation con `chip--seal` e la frase informativa bloccata **sempre presente**,
   messaggi e scadenze (EmptyState compatto). Mai una decisione, mai un numero non calcolato.
4. **Mobile**: sezioni `<details>` aperte alla prima; JourneyRail verticale in testa; inspector in
   coda; azione primaria in una barra inferiore appiccicosa.
Sparisce: l'indice serif «01 PARCOURS», la fascia dei quattro fatti in `dl` piatta, il titolo serif.

### 3.7 Orientation wizard — «Ma situation» (`templates/portal/situation.html`, gate D) — FOCUS (§49–51; 21st 17, 14; UIUX target ≥ 48, `touch-action`, redundant entry)

«Ma situation» è un modulo unico di 7 domande facoltative, salvato in un POST: **il flusso legale non
cambia** (§89). Diventa un **modulo guidato**: (a) a inizio riga (3 colonne da 1024) uno **Stepper**
verticale con le 7 domande (nodo pieno se renseignée, linea che avanza 320 ms), contatore bloccato
«n question(s) renseignée(s) sur 7…» 14/20; (b) al centro (6 colonne) **una domanda alla volta** su
pannello L2 raggio `xl` (recipe FOCUS: `--light-focus` dietro il pannello): domanda Plex 20/28 600,
aiuto 14/20 `--ink-2`, controllo = **OptionCard** (`<label>` intorno a radio/checkbox nativi, L1,
raggio `lg`, glifo 24 in disco 40, titolo 15/24 500, spiegazione 14/20; hover L2; selezionata = bordo
`--accent` 2 px + fondo `--accent-wash` + spunta che si disegna 200 ms; ≥ 48 px; `touch-action:
manipulation`) oppure campo 44 px; (c) piede appiccicoso 64 px in vetro L3: «Précédent» (SECONDARY) ·
«Continuer» (PRIMARY) — etichette esistenti del wizard `_step.html` — e il submit del modulo con la
sua etichetta attuale. Senza JavaScript, le sette sezioni si mostrano in sequenza: il pannello è un
miglioramento progressivo. Transizione fra domande = pattern «wizard» (uscita 120, entrata 200
traslata 16 px nel verso di lettura, altezza `spring-soft`). Il wizard pubblico
`templates/orientation/_step.html` («Question n · x %», htmx) adotta gli stessi OptionCard, Stepper e
piede. **Pagina risultato** (§51): cinque pannelli distinti — percorso potenziale (L2, chip
`--indicative` con «à titre indicatif»), elementi mancanti (Table con chip azione), avvertenze
(notice `azione`), verifica richiesta (chip `chip--seal` attesa), fonti (lista con glifo `document`) —
«Enregistrer dans mon espace» come PRIMARY. Nessuna barra nativa, nessun radio nudo, nessuna
pagina-lenzuolo.

### 3.8 Company dashboard (`/fr/espace-reserve/entreprise/`, gate E) — NEUTRAL + DATA (§52; 21st 2)

1. **ContextHeader**: eyebrow `ENTREPRISE`, ragione sociale **Plex 28/36 600**, riga meta: chip
   **«Vérifiée»** (registro conforme — un fatto, non un sigillo d'autorità), SECTEUR, ÉTABLISSEMENT,
   BESOINS OUVERTS «4 besoins en cours» con cifra tabellare; azione primaria a fine riga = «Ouvrir le
   besoin →» quando esiste.
2. **Riga 1 — 8/4**: pannello **«Votre prochaine action»** L2 (testo esistente, ResponsibilityBar
   «aucun intervenant désigné» con glifo tratteggiato) · pannello **«Mon entreprise»** L1 con i fatti in
   griglia 2 colonne e glifo `building` in disco 40.
3. **Riga 2 — 12**: **«Mes besoins en compétences»** come **Table** semantica (desktop): Besoin (titolo
   15/24 500 + riferimento mono + regione · settore · «n profils» 13/20) · État (chip: Brouillon /
   Transmis au projet = neutro) · Intervenant (Avatar/Glyph o «aucun intervenant désigné») · Timeline
   (date tabellari) · Azione (`btn--sm` SECONDARY «Ouvrir»); intestazione appiccicosa `--min-1`; riga
   hover sollevata; sotto 768 schede.
4. **Riga 3 — 6/6**: Formazione collegata (se dati) · Communications (o EmptyState).
Nessuna estetica da marketplace: nessun «profilo candidato», nessun conteggio di talenti, nessuna foto.

### 3.9 Il platform shell (gate B, condiviso da 3.4–3.8) — §14–15; 21st 1, 10, 16

- **Rail** a inizio riga (fine riga in RTL) **64 px** collassata / **248 px** aperta, `--mid-1` con
  `--mesh-dark` attenuato (navy 12 %), `z-rail`; testa: tassello del marchio 40 px raggio `md` su
  `--min-0` (variante scura V2 §8.1) e, aperta, il wordmark monocromo; voci 44 px raggio `md` con glifo
  20 px `--on-dark-2` + etichetta Plex 14/20 500 (aperta) o tooltip L3 (collassata); **gruppi
  semantici** con separatori hairline-dark e titolo 11/16 600 .06em `--on-dark-3` — proposta per la
  revisione copy §92: *Parcours* (Tableau de bord · Ma situation · Mon parcours), *Dossier* (Mes
  dossiers · Mes demandes · Mes documents · Mes échéances), *Échanges* (Communications · Guichet
  numérique), poi *Academy*; se i titoli sono respinti, restano i separatori. Voce attiva: superficie
  `--mid-3`, testo `--on-dark`, **indicatore** 3 px `--accent-dark` raggio full a inizio riga che
  **trasla** fra le voci (`spring-snappy`); hover `--mid-2` con il glifo che sale di 1 px. Contatori
  **solo** da dati reali come Badge 18 px. Collasso persistito in `localStorage` (try/catch); da 1440
  aperta di default. Tastiera: frecce, Home/End, Enter; `aria-current="page"`.
- **Barra di contesto** 56 px **in vetro** (`--glass-light` + blur 12) + hairline, `z-header`,
  appiccicosa: breadcrumb 13/20 a inizio riga; a fine riga: ricerca (persona: campo 44 px; staff:
  CommandMenu Ctrl/⌘ K, permission-aware), campanello con Badge reale → pannello notifiche L3
  «visto/trattato» (21st 16), «Site public» come LINK, account (`<details>` nativo) con Avatar/Glyph
  24, lingua segmentata compatta.
- **Workspace**: `--min-0`, max 1320, padding 32; **inspector** 320 opzionale (fascicolo).
- **Mobile ≤ 1023**: barra superiore 56 px in vetro (tassello, titolo pagina, IconButton menu, account)
  + **barra inferiore** 56 px in vetro con quattro voci + «Menu» (etichetta esistente): Tableau de bord ·
  Mes dossiers · Mes documents · Communications · Menu → cassetto L4 con la rail intera. Impresa:
  Tableau de bord · Mes besoins · Mon entreprise · Communications · Menu.
- RTL: rail a fine riga, indicatore a fine riga, chevron specchiati, non il marchio.

## 4. La porta V4 — quattro vie attraverso l'arco (§31–32; 21st 13)

### 4.1 Geometria (desktop ≥ 1280)

Palcoscenico SVG `viewBox="0 0 640 520"`, colonna 6/12 (560–640 px reali). L'arco ufficiale resta
identico nelle proporzioni: **300 × 400** (aspect 3/4, raggio 150 = 189,25 × 300/380), a x 170–470,
y 100–500; fotografia dentro l'arco (opacità .50, vignetta `--grad-photo-dark`), arco interno navy
`--brand-navy` al 52 % (156 × 242, x 242–398, y 258–500), chiave verbatim al 34 % dell'arco interno,
tre gradini come oggi. **Quattro nodi d'origine** a x = 48, y = 140 · 240 · 340 · 440 (disco 6 px +
anello 12 px al 40 %). **Quattro tracciati** cubici `stroke-width 1.75`, `stroke-linecap round`, dal
nodo verso la soglia: convergono nell'**apertura dell'arco interno** (x 242–398, y 470) — sul navy
pieno, contrasto ≥ 8,7:1 — passano la soglia come **una treccia** (a 6 px di distanza) e riemergono a
destra dell'arco verso **tre uscite** a x = 600, y = 200 · 300 · 400, etichettate con le tre parole
bloccate dell'eyebrow: ORIENTATION · FORMATION · MOBILITÉ RÉGULIÈRE (testo SVG 12/16 500
`--on-dark-2`). Colori di via su navy (DS §1.2): `--route-1-dark #7fd1d8` (9,93:1), `--route-2-dark
#8fbfe8` (8,92), `--route-3-dark #aab7cc` (8,56), `--route-4-dark #a8cfc0` (10,21); mai da soli: nodo +
glifo attore + parola nella legenda. Nessuna coordinata, nessun testo «svg», nessuna graticola. Il
blocco SVG è `aria-hidden`; l'informazione è nella legenda HTML (4.2).

### 4.2 Etichettatura integrata — la legenda in vetro

Le etichette **non** stanno nell'SVG. Un `<ol class="doorway-legend">` **HTML** è posizionato (CSS
grid sovrapposta al palcoscenico, nessun `style` inline) in basso a inizio riga, su un **pannello in
vetro** L3 (`--glass-dark` rgba(11,26,51,.55) + blur 16 + hairline-dark-strong, raggio `xl`, 264 px):
quattro righe da 44 px, ognuna con il **disco-nodo** nel colore di via (12 px), il glifo attore 16 px,
la parola (Plex 14/20 500 `--on-dark`) — PERSONNE · ENTREPRISE · INSTITUTION · UNIVERSITÉ / FORMATION,
parole della direttiva §31 (se la revisione copy preferisce i titoli bloccati
`p3.entrances.*.title`, sostituzione 1:1) — e il gloss bloccato `p3.entrances.{actor}.text` (13/20
`--on-dark-2`) rivelato dall'interazione. Dal pannello partono le **linee di richiamo** SVG (1 px,
`--hairline-dark-strong`) ai quattro nodi d'origine: i callout sono ancorati per costruzione. Ogni voce
è un `<a>` verso la landing della via (`pathways:index`, `ecosystem:companies`,
`ecosystem:institutions`, `ecosystem:universities`). Contrasto sul vetro (composito peggiore
`#0f233f`): parola 13,92, gloss 9,02, accento 9,02.

### 4.3 Interazione

Hover / focus-visible su una voce della legenda → il palcoscenico riceve `data-route="{actor}"`
(`home.js`): la via attiva passa a `stroke-width 2.5` e opacità 1, le altre tre a **opacità .50**
(≥ 3,08:1 su `--mid-1`: restano leggibili), il nodo attivo riceve un anello 2 px `--accent-dark`, la
riga della legenda si solleva (fondo `--mid-3` a 60 %), il gloss si apre (altezza `spring-soft`,
opacità 200 ms `--ease-enter`), e il pannello della via in `_entrances` riceve `is-related` (stesso
stato hover: la CTA relativa si evidenzia). Uscita 120 ms `--ease-exit`. Touch: **tap = navigazione**
(`:active` dà l'enfasi immediata per la durata della pressione); nessun secondo tap (§89). Tastiera:
Tab fra le quattro voci, Enter naviga.

### 4.4 Moto

1. **Disegno iniziale** (una volta, dopo LCP, `withMotion`): arco `pathLength` 0→1 in 900 ms
   `--ease-enter` → le quattro vie 0→1 in 900 ms con stagger 120 → nodi, legenda e uscite opacità 0→1
   in 200 ms → gradini posati (stagger 100) → chiave si assesta 8 px una volta. Totale ≈ 2,3 s; con
   reduced-motion tutto è allo stato finale dal primo frame.
2. **Ambiente sottile** — **l'unico oggetto vivo della home** (sostituisce la marea V2): su ogni via un
   secondo tracciato `stroke-dasharray: .06 .94` (`pathLength=1`), opacità .55, `stroke-dashoffset`
   che scorre di −1 in **28 s lineari** (`--motion-ambient`), in pausa fuori viewport
   (`IntersectionObserver` → classe), fermo e nascosto con reduced-motion. Solo `transform`/`opacity`/
   `stroke-dashoffset`.
3. **Enfasi interattiva** — 4.3. Nessun rimbalzo, nessun bagliore in loop, nessun `filter` animato.
4. **Scroll**: la fotografia dentro l'arco scorre di 18 px (≈ 2 %) via `scroll()`; il palcoscenico
   scala a .96 e sfuma a .6 mentre l'hero esce, così il capitolo successivo entra su un fondo quieto.

### 4.5 Mobile (< 1024)

La porta **da sola** a 220 px (arco, fotografia, chiave, gradini), prima del titolo. Le quattro vie
sono la **legenda** subito sotto, senza vetro (fondo `--mid-2`, raggio `lg`): quattro righe da 52 px,
ognuna con un tratto di via 24 × 2 px nel suo colore, disco-nodo, glifo, parola, gloss sempre visibile;
il diagramma è implicato, non schiacciato. Tra 1024 e 1279: palcoscenico `viewBox 0 0 480 520` senza le
tre uscite (le tre parole restano nell'eyebrow).

## 5. Direzione dell'immagine (Image Art Director) — §34–36, §81–83

**Una libreria**, scelta da una sola persona, self-hosted via `scripts/fetch_images.py` (Pexels, licenza
registrata in `docs/IMAGE_LICENSES.md`), mai un hotlink (`forbidden.py` lo blocca).

### 5.1 Temi e frasi di ricerca (Pexels)

| Tema (§34) | Frasi da usare | Dove |
|---|---|---|
| cooperazione universitaria/accademica | `university lecture hall students listening`, `campus library reading`, `research lab team notes` | home ecosistema, mega-menu Personnes, landing università |
| formazione professionale | `vocational training workshop apprentice`, `welding apprentice safety`, `technical school machine training`, `cold storage logistics worker` (i settori reali dei fabbisogni: metallurgia, logistica, BTP) | landing formazione, Academy, mega-menu Entreprises |
| dialogo istituzionale | `conference room meeting documents`, `institutional round table discussion`, `city hall meeting room empty morning` | home ecosistema, forum |
| luogo di lavoro moderno | `construction site engineer dawn helmet`, `architecture office team drawings`, `warehouse logistics morning` | landing imprese |
| consulenza professionale | `advisor desk consultation documents`, `office one to one meeting notes` | Personnes, landing persona |
| formazione prima della partenza | `adult language classroom`, `evening class adults whiteboard` | Personnes |
| integrazione / apprendimento | `students walking arcade portico`, `library study group` | forum, Academy |
| Italia / Marocco autentiche | `Padova portico arcade`, `Venice calle morning quiet`, `Rovigo street`, `Rabat modern architecture`, `Casablanca office building facade`, `Fes university courtyard` | hero delle landing, forum |

**Rifiutare** (§83): strette di mano, passaporti, valigie, aeroporti, gondole, bandiere, barche e
frontiere (cliché migratorio), sorrisi rivolti alla camera, gruppi in posa, risoluzione < 2400 px sul
lato lungo, dominanti cromatiche forti, filtri, testo in primo piano, loghi riconoscibili.

### 5.2 Sistema di crop

Tre rapporti, e un quarto solo per l'Academy: **3:2** (schede, mega-menu, news), **4:5** (ritratto di
luogo nelle landing delle vie e nel forum), **21:9** (bande di capitolo, ecosistema), **16:10**
(copertine corso). Punto focale per immagine (`data-focus` → nove classi `.img--focus-{tl,t,tr,l,c,r,bl,
b,br}` su `object-position`; nessun `style` inline). Varianti 480/800/1200/1600 AVIF + WebP, ≤ 120 KB
a 1200, `<picture>` con `sizes`, lazy sotto la piega.

### 5.3 Grading — un trattamento

In pipeline (Pillow, deterministico): contrasto **+8 %**, saturazione **−15 %**, curva a S morbida,
**neri sollevati** verso `--mid-1` (`#0b1a33`, L* ≈ 9), luci **+4 %** verso il caldo, nitidezza 0,5.
In pagina: su fondi scuri `--grad-photo-dark` (`rgba(11,26,51,0) 40% → rgba(11,26,51,.45)`); su carta
un velo `--accent` al **6 %** + hairline interna `inset 0 0 0 1px rgba(21,34,42,.08)`; su IMMERSIVE la
**grana** `static/img/grain.svg` (asset vendorizzato, 3 %, `mix-blend-mode: multiply`). Due immagini
affiancate devono sembrare scattate dalla stessa persona.

### 5.4 Bordi, maschere, raggi

Raggio **`lg` (14 px)** in schede e pannelli; **0** quando l'immagine tocca il bordo del capitolo
(bande 21:9); **arco** (190/190/0/0) **solo** nella porta — mai come maschera altrove. Nessuna maschera
organica, nessun blob.

### 5.5 Moto delle immagini

Hover: `scale(1.02)` in 320 ms `--ease-enter` (**≤ 3 %**), ritorno 120 ms. Crossfade fra due immagini:
320 ms. Reveal allo scroll: `clip-path: inset(0 0 12% 0)` → `inset(0)` + opacità in 320 ms, una volta.
Parallasse: solo la fotografia della porta (18 px) e le bande 21:9 (≤ 3 %, `scroll()`). Reduced-motion:
tutto fermo, tutto visibile.

### 5.6 Quantità per pagina

Home: **porta + 5** (2 ecosistema, 3 news); mega-menu: 1 per pannello (3, lazy); landing di via: 1 hero
4:5 + 1 di contenuto; forum pubblico: ≤ 4; Academy: 1 copertina per corso; **login: la porta**; cruscotti,
documenti, fascicolo, wizard, B2B: **0**.

## 6. I quattro test, applicati a questa direzione

1. **«Potrebbe essere scambiato per un template generico Claude/AI?»** Rischio reale: rail a icone +
   barra in vetro + pannelli + pillole è il vocabolario 2026 che anche una dashboard shadcn usa. Ciò che
   lo impedisce, se rispettato: carta minerale e navy del marchio (non zinc/bianco), Newsreader sul
   pubblico, IBM Plex (non Inter), un accento teal con il suo gradiente e nessun viola, la porta a
   quattro vie, pastiglie a registro nella forma, nessuna card-con-icona. Il punto fragile è il
   **cruscotto persona**: costruito come «quattro tessere KPI» fallisce — per questo 3.4 impone tre
   misure di pannello e vieta le tessere. Verdetto onesto: **passa solo se il gate C verifica
   l'assenza di tessere e la presenza del JourneyRail**.
2. **«Sembra ancora una pubblicazione editoriale/legale?»** Pubblico: nelle pagine lunghe sì, per scelta
   (§4 della direttiva lo ammette). Operativo: **no** — zero serif, zero folio, zero filetti di
   registro, zero tavole da documento; la risposta deve restare NO a ogni gate C–E.
3. **«Nascosto il logo, competerebbe con prodotti premium del 2026?»** Sì **se** il moto e la profondità
   sono eseguiti: ogni elemento interattivo con hover/focus/press, ogni pannello al suo livello, la
   rail che risponde con la molla, i chip che cambiano parola con transizione, il primario con il suo
   gradiente e il suo alone. Senza, resta un «sito Django ben ordinato» con raggi più grandi — che è
   esattamente ciò che §2 vieta. La scorecard chiede la prova per ogni stato.
4. **«Abbiamo aggiunto effetti inutili?»** Tre candidati al taglio, dichiarati in ordine: lo
   **spotlight** sui pannelli delle vie, il **bordo a gradiente** sui pannelli, la **corrente
   ambientale** sulle vie. Se un revisore indipendente segna «troppo», si toglie nell'ordine; la
   direzione regge senza tutti e tre. Il vetro resta dov'è (barre appiccicose, scrim, legenda, striscia
   del login): è materiale delle superfici flottanti, non effetto. La console non ha nulla da tagliare:
   zero ambiente, moto solo causale.

## 7. Che cosa ha cambiato il chiarimento delle 20:58

| Decisione | Prima (bozza conservativa) | Ora |
|---|---|---|
| Capitolo scuro | `--mid-*` teal-nero V2 | **navy-mezzanotte** evoluto dal navy del marchio (`#0b1a33` e scala), mesh navy + teal, grana |
| Accento | un solo `#0f6a72` piatto | famiglia: `--accent` (testo) · `--accent-2 #12777f` (luce, icone) · gradiente primario `#12777f → #0f6a72` con alone in hover |
| Tipografia UI | Fira Sans «perché c'è» | **IBM Plex Sans + Plex Mono**, stessa superfamiglia di IBM Plex Sans Arabic già vendorizzata (parità Latin/Arabo); Fira ritirata |
| Bottoni | V3 con raggio 8 e senza ombra | sistema V4: raggio 10, gradiente, ombra 1 + alone, SOFT nuovo, loading/success |
| Vetro | solo header scrollato | header scrollato, barra di contesto, barre mobili, scrim, legenda dell'hero, striscia del login |
| Ombre | 1 hairline + V2 | sei ruoli a due strati (chiave + ambiente), più intense nel navy |
| Raggi | 2/4/8/12/16 | **4/6/10/14/20/full** |
| Display hero | clamp 52→88 | clamp 44→76, riga per riga, co-protagonista della porta |
| Login | porta senza foto | porta completa con la fotografia del titolare, striscia in vetro |
| Etichette della porta | testo SVG inline | legenda HTML in vetro con linee di richiamo |
| Moto | budget prudente | stesso budget (≤ 2 per vista), livello più alto sul pubblico: capitoli che transiscono allo scroll, reveal a maschera, corrente, molle sulla console |

Non è cambiato: testi bloccati, `forbidden.py`, «nessun colore significa mai approvato», marchio e arco,
nessun dato finto, WCAG 2.2 AA con ogni coppia calcolata.
