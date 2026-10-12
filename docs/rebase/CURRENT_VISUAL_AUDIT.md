# CURRENT VISUAL AUDIT — perché il risultato non è accettato

Audit del direttore di prodotto e design · 20 settembre 2026
Prove: `docs/qa/visual/before/` — 272 screenshot, 25 pagine, dieci viewport da 320 a 1920 px,
francese e arabo. Le critiche indipendenti del Design Council sono in `docs/design/DESIGN_COUNCIL_REVIEW.md`.

---

## 1. Il verdetto

Il sito **non è brutto. È generico.** È la distinzione che conta, perché determina la cura.

Un sito brutto si aggiusta con il gusto: colori, spaziature, ombre. Un sito generico non ha un
problema di gusto, ha un **problema di idea**. Nessuna quantità di ritocchi lo salverà, perché ciò
che manca non è nella pagina: manca una decisione su che cosa questa pagina voglia essere.

Il committente lo ha detto con precisione: «technically correct but aesthetically ordinary». È esatto.

Punteggio onesto della mia valutazione iniziale, prima delle critiche indipendenti:

| Dimensione | /10 | Motivo in una riga |
|---|---|---|
| Credibilità istituzionale | 6 | Sobrio e non offensivo, ma anonimo |
| Tipografia | 4 | Leggibile, non espressiva: non porta il progetto |
| Composizione | 3 | Una sola colonna ripetuta per undici sezioni |
| Spaziatura | 5 | Abbondante ma indifferenziata |
| Originalità | 2 | Riconoscibile solo dal logotipo |
| Gerarchia informativa | 4 | Tutto pesa uguale, quindi niente pesa |
| Qualità delle immagini | 3 | Una foto di repertorio, un cliché |
| Interazione | 5 | Corretta, senza carattere |
| Responsive | 6 | Funziona; non è progettata per il telefono |
| Accessibilità | 7 | Curata, con difetti noti |
| Coerenza | 7 | Molto coerente — è parte del problema |
| Usabilità della piattaforma | 2 | Un elenco di moduli, non un servizio |

---

## 2. I dodici difetti strutturali

### D-01 — La pagina ha un solo ritmo, ripetuto undici volte
**Prova:** `home__1440x900__fr.png`. Dalla sezione 3 alla sezione 9 la struttura è identica:
occhiello in maiuscoletto oro · titolo serif · paragrafo di lancio · contenuto · filetto di
separazione. Stessa larghezza di contenitore, stesso allineamento a sinistra, stessa distanza
verticale, stesso peso visivo.

**Perché conta:** è letteralmente il pattern che il committente ha vietato («repetitive eyebrow + H2
+ paragraph + 3 cards», «identical container width for every section»). L'effetto è che il lettore
non ha idea di quale sezione sia importante. Una pagina in cui tutto è ugualmente importante è una
pagina in cui nulla lo è.

### D-02 — L'hero non è un hero
**Prova:** `home__1920x1080__fr.png`, primi 900 px. Un blocco di testo piccolo a sinistra, una foto
di repertorio a destra dentro una cornice bianca sfalsata. Il titolo occupa una frazione minima della
superficie. A 1920 px lo spazio vuoto sopra e sotto è maggiore del contenuto.

**Perché conta:** è il primo e talvolta unico momento in cui il progetto può dire chi è. Oggi dice:
«un sito».

### D-03 — La fotografia è un cliché
**Prova:** stessa immagine. Mani su un tavolo, penna, documento, riunione. È la fotografia
«business generico» che compare su centomila siti. Il committente ha vietato esplicitamente la
fotografia di repertorio non curata.

**Perché conta:** una sola immagine sbagliata nell'hero costa più credibilità di dieci sezioni ben
scritte.

### D-04 — Quattro schede con quattro icone
**Prova:** `home__1440x900__fr.png`, sezione «Quattro accessi all'ecosistema». Quattro colonne
identiche, ognuna con una piccola illustrazione a tratto, numerata 01–04, titolo, descrizione, link.

**Perché conta:** è «section of identical cards» più «every card containing an icon». Peggio: le
quattro entrate sono l'elemento più importante del sito — sono le porte dell'ecosistema — e sono
trattate come una griglia di servizi qualsiasi.

### D-05 — L'avviso istituzionale più importante è l'elemento meno visibile
**Prova:** la fascia del Forum Vénétie–Maroc è una striscia beige alta circa 60 px, con testo piccolo
e una croce di chiusura.

**Perché conta:** il Forum del 2 ottobre a Rovigo, sotto il patrocinio della Regione del Veneto e del
Comune di Rovigo, è l'evento fondativo del progetto. Visivamente è un cookie banner.

### D-06 — La tipografia non porta il design
**Prova:** i titoli di sezione e il testo di lancio hanno scala troppo ravvicinata; i titoli non
dominano mai. Nessun uso espressivo del serif: è solo «il font dei titoli». Nessun maiuscoletto
strutturale, nessuna numerazione tipografica, nessun contrasto di peso significativo.

**Perché conta:** il committente ha chiesto esplicitamente che «typography must carry the design». In
un progetto istituzionale con molto testo giuridico, la tipografia **è** il design.

### D-07 — Il colore non significa nulla
**Prova:** il blu istituzionale compare solo su testata, piè di pagina e pulsanti. L'oro solo sugli
occhielli minuscoli. Il resto è crema e grigio.

**Perché conta:** in un prodotto che deve distinguere informazione, attenzione, limite giuridico e
azione richiesta, il colore dovrebbe essere un sistema di significato. Oggi è decorazione.

### D-08 — Nessun linguaggio grafico proprio
**Prova:** togliendo la fotografia e il logotipo, non resta nulla di riconoscibile. Nessun motivo
cartografico, nessuna linea territoriale, nessun diagramma di percorso, nessuna indicizzazione
tipografica.

**Perché conta:** il committente ha chiesto che «the site should be recognizable even if all
photography is temporarily removed». Oggi non lo è.

### D-09 — La piattaforma riusa il guscio pubblico
**Prova:** `portal-dashboard__1440x900__fr.png`. Dopo l'accesso restano la barra di servizio
pubblica, il mega-menu completo con sette voci pubbliche e il piè di pagina istituzionale integrale.

**Perché conta:** divieto esplicito («Do not reuse the entire public mega-menu after login»). Ma
soprattutto: chi è entrato nel proprio spazio non sta cercando «Il progetto», sta cercando la sua
prossima azione.

### D-10 — Il cruscotto è una griglia di scatole vuote
**Prova:** stessa immagine. Cinque riquadri con bordo tratteggiato, ognuno con un'icona centrata e
un testo di stato vuoto. «Nessun documento», «Nessuna scadenza», «Nessuna comunicazione»,
«Nessuna pre-valutazione».

**Perché conta:** è l'anti-pattern «empty KPI widgets». E non risponde a nessuna delle domande che il
committente ha posto come criterio di accettazione: dove sono, qual è il mio obiettivo, che cosa ho
fatto, che cosa manca, che cosa devo fare adesso, chi è responsabile.

### D-11 — Il titolo dell'area riservata è trattato come una pagina pubblica
**Prova:** «ESPACE RÉSERVÉ» in serif maiuscolo enorme, con paragrafo di lancio, come una qualsiasi
pagina editoriale.

**Perché conta:** un'applicazione non si presenta, si usa. Quel titolo consuma il terzo superiore
dello schermo per dire all'utente dove ha appena scelto di andare.

### D-12 — Il mobile è il desktop compresso
**Prova:** la home a 390 px è alta quasi 9 000 px. Le quattro entrate arrivano dopo tre schermate.
L'ordine dei contenuti è quello del desktop, impilato.

**Perché conta:** il pubblico principale di questo progetto accede da telefono. Il mobile non è una
riduzione: è il caso d'uso primario.

---

## 3. Che cosa invece funziona e va difeso

Sarebbe un errore buttare via tutto.

- **Il contegno.** Nessun gradiente viola, nessun glassmorphism, nessuna animazione decorativa,
  nessun contatore da startup. Il punto di partenza è sobrio, e la sobrietà è la direzione giusta.
- **Il blu profondo e la carta calda** sono una base cromatica corretta per il registro istituzionale.
- **I filetti sottili** come separatori sono una scelta matura.
- **Il piè di pagina** è ben organizzato e informativo.
- **La sezione «che cosa fa e che cosa non fa»** è un'idea di contenuto eccellente, mal presentata.
- **Il maiuscoletto degli occhielli** funziona come segnale, va solo usato con più intenzione.
- **La leggibilità del testo lungo** è buona.
- **L'assenza di rumore.** Non c'è nulla da togliere: c'è tutto da costruire.

---

## 4. La diagnosi in una frase

> Il sito ha buone maniere ma nessuna voce.

Il rebase non deve renderlo più bello. Deve dargli **una tesi visiva**: una decisione su come questo
progetto guarda il mondo, applicata con disciplina a ogni pagina, in quattro lingue, su dieci
larghezze, per due prodotti distinti che condividono una sola identità.

---

## 5. Che cosa deve cambiare, in ordine di impatto

| # | Cambiamento | Impatto | Costo |
|---|---|---|---|
| 1 | Una art direction scelta e motivata, con un'idea portante | Decisivo | Alto |
| 2 | Sistema tipografico espressivo, arabo incluso | Decisivo | Medio |
| 3 | Architettura compositiva: archetipi di pagina, gerarchia di sezioni, rottura della monotonia | Decisivo | Alto |
| 4 | Guscio della piattaforma separato, orientato al compito | Decisivo | Alto |
| 5 | Cruscotto della persona riprogettato attorno a percorso, prossima azione e responsabilità | Decisivo | Alto |
| 6 | Colore come sistema di significato | Alto | Basso |
| 7 | Linguaggio grafico proprio non fotografico | Alto | Medio |
| 8 | Direzione fotografica: meno immagini, più forti, senza cliché | Alto | Medio |
| 9 | Trattamento dell'avviso istituzionale proporzionato alla sua importanza | Medio | Basso |
| 10 | Mobile progettato per primo sulle pagine chiave | Alto | Medio |
| 11 | Arabo progettato, non tradotto | Alto | Medio |
| 12 | Motion sobrio e significante | Basso | Basso |

---

## 6. Metodo di verifica dopo il rebase

Lo stesso di questo audit, per confronto diretto:

1. Ricattura con `scripts/capture_baseline.py --label after --out docs/qa/visual/after`.
2. Confronto a coppie prima/dopo alle stesse dieci larghezze, nelle due lingue.
3. Nuova valutazione indipendente del Design Council sulle stesse dodici dimensioni.
4. Criterio di accettazione: nessuna dimensione sotto 7, nessuno dei pattern vietati presente,
   e alla domanda «sembra ancora un sito generato da un'AI?» la risposta deve essere no, motivata.
