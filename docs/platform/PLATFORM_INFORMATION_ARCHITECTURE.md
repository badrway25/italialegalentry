# PLATFORM INFORMATION ARCHITECTURE

Versione 1.0 · 20 settembre 2026 · Direttiva di rebase §20, §21, §58

---

## 1. Due superfici, una identità

| | Sito pubblico | Piattaforma |
|---|---|---|
| Scopo | Scoperta e comprensione | Completamento di compiti |
| Voce | Editoriale, istituzionale, narrativa | Operativa, precisa, di servizio |
| Densità | Generosa | Intelligente |
| Navigazione | Sette sezioni tematiche, scoperta | Orientata al compito, filtrata dai permessi |
| Unità | La pagina | Il compito e l'oggetto di lavoro |
| Stato | Nessuno | Ovunque: contesto, avanzamento, responsabilità |

Condividono: marchio, colore, tipografia, iconografia, tono, regole di accessibilità e comportamento
RTL. **Non condividono il guscio.**

Il mega-menu pubblico non compare dopo l'accesso. Il piè di pagina istituzionale integrale non
compare dopo l'accesso. La piattaforma ha una sua testata, una sua navigazione e un suo piè di pagina
ridotto.

## 2. Il passaggio fra le due

### Ingresso permanente

Un accesso stabile nella barra di servizio pubblica, con l'etichetta della lingua corrente:
`Accedi` · `Espace réservé` · `Sign in` · `الدخول`.

### Ingressi contestuali

| Contesto pubblico | Invito | Destinazione dopo l'accesso |
|---|---|---|
| Persone | Iniziare o riprendere l'orientamento | Cruscotto persona, sul percorso in corso |
| Imprese | Accedere all'area imprese, segnalare un fabbisogno | Cruscotto impresa, sui fabbisogni |
| Istituzioni | Proporre una collaborazione | Workspace istituzionale |
| Università e formazione | Proporre un partenariato | Workspace di partenariato |
| Forum | Iscriversi, partecipare | Workspace del Forum |

**Un solo sistema di autenticazione.** Dopo l'accesso l'instradamento dipende dai ruoli dell'utente,
non dalla porta da cui è entrato. Un utente con più ruoli sceglie il contesto, e la scelta è
ricordata.

### Ritorno

Dalla piattaforma si torna al sito pubblico con un collegamento esplicito, mai per smarrimento.

## 3. Guscio della piattaforma

```
┌──────────────────────────────────────────────────────────────────────┐
│ marchio    │ contesto corrente          │ ricerca │ notifiche │ conto │  testata
├────────────┼─────────────────────────────────────────────────────────┤
│            │                                                         │
│ navigazione│   ZONA DI LAVORO                                        │
│ per ruolo  │   ┌───────────────────────────────────────────────┐     │
│            │   │ intestazione dell'oggetto (stabile)           │     │
│ · sezione  │   ├───────────────────────────────────────────────┤     │
│ · sezione  │   │ prossima azione                               │     │
│ · sezione  │   ├───────────────────────────────────────────────┤     │
│            │   │ contenuto                                     │     │
│ ---------- │   │                                               │     │
│ sportello  │   └───────────────────────────────────────────────┘     │
│ aiuto      │                                                         │
└────────────┴─────────────────────────────────────────────────────────┘
```

**Regole del guscio**

1. La navigazione laterale mostra **solo** ciò a cui l'utente ha accesso. Un modulo esistente ma non
   autorizzato non compare, nemmeno disabilitato: la sua esistenza è essa stessa un'informazione.
2. Il contesto corrente è sempre visibile nella testata: quale fascicolo, quale fabbisogno, quale
   coorte.
3. L'intestazione dell'oggetto resta stabile mentre si naviga dentro l'oggetto.
4. La prossima azione è un elemento di prima classe, non un pulsante fra gli altri.
5. Su telefono la navigazione laterale diventa un menu di compiti, non una copia ridotta.

## 4. Architettura per ruolo

### Persona

```
Cruscotto
├── Il mio percorso          timeline del fascicolo
├── Orientamento             ultima valutazione, fonti, rifare la valutazione
├── Il mio fascicolo
│   ├── Checklist            requisiti, responsabili, scadenze
│   ├── Documenti            requisiti documentali e stati
│   └── Cronologia
├── Formazione               catalogo, iscrizioni, avanzamento
├── Scadenze
├── Comunicazioni
├── Sportello digitale       chiedere una revisione umana
└── Il mio conto             profilo, consensi, sicurezza, lingua, dati personali
```

### Impresa

```
Cruscotto
├── I miei fabbisogni        elenco e stato
│   └── Fabbisogno           profilo professionale, competenze, tempi, formazione, attori, avanzamento
├── La mia impresa           identità, verifica, referenti
├── Comunicazioni
└── Il mio conto
```

### Soggetto autorizzato

```
Coda delle pratiche
├── Pratica                  mandato, fabbisogno, persone, fase, decisioni, evidenze
├── Il mio mandato           tipo, giurisdizione, riferimento, validità
├── Audit                    le proprie azioni
└── Il mio conto
```

### Professionista

```
Richieste assegnate
├── Fascicolo assegnato      dati, documenti, nota professionale, risposta
├── Scadenze
└── Il mio conto
```

### Ente formativo

```
Coorti e corsi
├── Coorte                   iscritti, avanzamento, completamenti
├── Catalogo                 i propri corsi
└── Il mio conto
```

### Istituzione e università

```
Perimetro della convenzione
├── Progetti
├── Iniziative territoriali
├── Indicatori aggregati
├── Forum                    commissioni, tavoli, proposte
├── Documenti condivisi
└── Il mio conto
```

### Back-office (Legal/Rule Editor, redattore, operatore, amministratore)

```
/backoffice/
├── Regole giuridiche        elenco, versioni, diff, anteprima, workflow di approvazione
├── Contenuti                CMS, traduzioni, pubblicazione programmata
├── Tassonomie               professioni, competenze, documenti, corsi, commissioni
├── Anagrafiche              partner, soggetti autorizzati, fonti
├── Configurazione           flag, gate, consensi, retention
├── Utenti e ruoli           con separazione dei privilegi
└── Audit                    consultazione per utenti autorizzati
```

## 5. Archetipi di pagina della piattaforma

| # | Archetipo | Esempi |
|---|---|---|
| 10 | Cruscotto di ruolo | Persona, impresa, ente formativo |
| 11 | Spazio di lavoro del caso | Fascicolo digitale |
| 12 | Spazio documentale | Documenti del fascicolo |
| 13 | Procedura guidata | Questionario, creazione di un fabbisogno |
| 14 | Timeline e percorso | Il mio percorso, cronologia |
| 15 | Elenco di dati | Coda delle pratiche, elenco delle regole, iscritti |
| 16 | Dettaglio e ispettore | Dettaglio regola, dettaglio fabbisogno |
| 17 | Spazio formativo | Catalogo, corso, modulo |
| 18 | Comunicazioni e compiti | Messaggi, scadenze, sportello |
| 19 | Amministrazione ed editor di regole | Back-office |

Gli archetipi 1–9 sono quelli del sito pubblico, definiti in `docs/design/PAGE_ARCHETYPES.md`.

## 6. Ricerca

| | Pubblica | Di piattaforma |
|---|---|---|
| Indice | Guide, percorsi, FAQ, glossario, attualità, risorse | Oggetti del proprio perimetro |
| Autorizzazione | Nessuna | **Durante la valutazione della query**, non dopo |
| Regola | — | Un utente non deve mai scoprire l'esistenza di un oggetto non autorizzato attraverso i risultati |

Conseguenza tecnica: il filtro dei permessi si applica al queryset, non alla lista dei risultati.
Un conteggio, un suggerimento di completamento o un messaggio «nessun risultato» diverso a seconda
dell'esistenza dell'oggetto sono già una fuga di informazione.

## 7. Comportamento su telefono

La direttiva §47 impone che questi compiti siano possibili da telefono:

- consultare lo stato e la prossima azione;
- caricare un documento;
- leggere un messaggio;
- completare un questionario semplice;
- consultare la checklist;
- accedere alla formazione;
- contattare lo sportello.

Le operazioni amministrative complesse possono privilegiare lo schermo grande, ma non devono
rompersi su quello piccolo.
