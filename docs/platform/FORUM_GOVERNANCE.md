# FORUM GOVERNANCE — dal convegno all'infrastruttura permanente

Versione 1.0 · 20 settembre 2026
Fonti: Master Dossier v2.0 §8 · Technical Blueprint v1.0 §12 · Documento di implementazione (parte pubblica)
Conflitto risolto: CR-13

---

## 1. Due prodotti, un nome

Il Forum Permanente Giuridico-Economico Italia–Marocco è, nello stesso momento:

**A. Un programma istituzionale pubblico.** Ha una data, un luogo, un programma, un patrocinio, degli
esiti. Vive sul sito pubblico ed è visibile a chiunque.

**B. Un modulo di governance autenticato.** Ha membri, commissioni, tavoli, proposte, progetti,
milestone e una relazione annuale. Vive nella piattaforma ed è visibile ai partecipanti.

Il Master Dossier è esplicito: «Non è concepito come un singolo convegno, ma come uno spazio stabile
di dialogo». La prima edizione italiana, a **Rovigo il 2 ottobre 2026**, è l'avvio pubblico del
percorso, non il percorso.

## 2. Il ciclo di governance

```
   FORUM ANNUALE
        │  raccoglie contributi e individua le priorità
        ▼
   PRIORITÀ
        │  ciascuna priorità è affidata a una commissione
        ▼
   COMMISSIONI MISTE  ◄──────────────────────────────┐
        │  ogni commissione apre tavoli tematici     │
        ▼                                            │
   TAVOLI DIGITALI                                   │
        │  i tavoli elaborano proposte               │
        ▼                                            │
   PROPOSTE                                          │
        │  una proposta accolta diventa progetto     │
        ▼                                            │
   PROGETTI                                          │
        │  con partner, milestone, responsabili      │
        ▼                                            │
   ATTUAZIONE                                        │
        │                                            │
        ▼                                            │
   MONITORAGGIO                                      │
        │                                            │
        ▼                                            │
   RELAZIONE ANNUALE ─────────────────────────────►  │
        │  alimenta il Forum successivo              │
        └────────────────────────────────────────────┘
```

Il ciclo è il prodotto. Una proposta che non può diventare progetto, o un progetto senza
monitoraggio, è un tavolo di discussione: precisamente ciò che il Master Dossier dice che il Forum
non deve essere.

## 3. Le commissioni

Il Blueprint ne elenca cinque e aggiunge: «Ulteriori commissioni settoriali **configurabili senza
modifica del codice**».

| Commissione | Ambito |
|---|---|
| Mobilità Regolare, Lavoro e Inclusione | Percorsi legali, fabbisogni, formazione, inclusione |
| Giuridica e Diritto Comparato | Professionisti, ordini, istituzioni, formazione giuridica |
| Imprese, Investimenti e Cooperazione Economica | Sistemi camerali, imprese, territori, partenariati |
| Università, Ricerca e Mobilità Accademica | Partenariati, mobilità di studenti e docenti, ricerca |
| Formazione e Competenze | Percorsi coerenti con bisogni territoriali e professionali |

**Requisito tecnico vincolante (REQ-CFG-03):** queste cinque righe sono **dati di seed**, non
costanti nel codice. Aggiungere una sesta commissione è un'operazione di back-office.

Corrispondenza con i cinque assi di cooperazione pubblici del Master Dossier §8: mobilità regolare,
cooperazione giuridica, università e ricerca, cooperazione economica, formazione. Gli assi sono la
faccia pubblica, le commissioni sono l'organo di lavoro.

## 4. Modello dati

| Entità | Campi principali | Note |
|---|---|---|
| `ForumEdition` | anno, luogo, date, stato | La prima è Rovigo 2026 |
| `ForumProfile` | organizzazione o utente, categoria, interessi, edizione | Profilo di partecipazione |
| `Commission` | chiave, tema, governance, stato, edizione | **Configurabile** |
| `CommissionMember` | commissione, profilo, ruolo, da, a | Membro con mandato datato |
| `Table` | commissione, tema, stato, referente | Tavolo digitale |
| `ForumProposal` | proponente, tema, testo, stato, commissione, tavolo | Stati: `DRAFT`, `SUBMITTED`, `UNDER_REVIEW`, `ACCEPTED`, `REJECTED`, `WITHDRAWN` |
| `ForumProject` | proposta di origine, partner, responsabile, stato | Nasce da una proposta accolta |
| `ProjectMilestone` | progetto, titolo, scadenza, stato, responsabile | |
| `MonitoringEntry` | progetto, periodo, indicatori, note | Alimenta la relazione |
| `AnnualReport` | edizione, sezioni, stato di pubblicazione | Generata dai dati, non scritta a mano |

## 5. Ruoli nel Forum

| Ruolo | Può |
|---|---|
| Partecipante | Vedere le commissioni di cui è membro, i tavoli aperti, proporre |
| Referente di tavolo | Moderare il tavolo, consolidare le proposte |
| Segreteria del Forum | Gestire edizioni, commissioni, membri, stati, relazione annuale |
| Osservatore istituzionale | Consultare secondo il perimetro dell'accordo |

**Vincolo:** i partecipanti non possono consultare informazioni private di altri utenti. Il Forum non
è una rubrica di contatti. I profili mostrano organizzazione, categoria e interessi dichiarati, non
dati personali.

## 6. Superficie pubblica

| Contenuto | Prima del 2 ottobre 2026 | Dopo |
|---|---|---|
| Pagina | Evento: data, luogo, orario, patrocinio, programma, iscrizione | **Forum Permanente Vénétie–Maroc** |
| Interventi | Solo le funzioni, mai i nomi (gate G5) | Nomi solo con il programma definitivo |
| Loghi dei patrocinatori | Nessuno finché non forniti e autorizzati (gate G6) | Idem |
| Banner in home | Visibile fino al 2 ottobre | Rimosso automaticamente |
| Esiti | — | Esiti dell'edizione, prossime tappe |
| Risorse | — | Documenti pubblici, relazione annuale |

La transizione è governata da flag e data, gestibile dal back-office senza intervento tecnico.

## 7. Superficie autenticata

Dietro il flag `virtual_forum`, **chiuso** fino a dopo il 30 ottobre 2026 e comunque subordinato al
gate G1 sulle pagine giuridiche.

```
Forum
├── La mia partecipazione     profilo, commissioni di appartenenza
├── Commissioni               elenco, membri, mandato
│   └── Commissione
│       ├── Tavoli
│       │   └── Tavolo        discussione, documenti, proposte in elaborazione
│       └── Proposte
├── Progetti                  partner, milestone, responsabili, stato
│   └── Progetto
│       ├── Milestone
│       └── Monitoraggio
├── Documenti condivisi
└── Relazione annuale
```

## 8. Stato attuale

| Componente | Stato |
|---|---|
| Pagina pubblica dell'evento | **FATTO** — programma, interventi per funzione, partner, iscrizione, JSON-LD |
| Modalità permanente dopo il 2 ottobre | **FATTO** — governata da flag e data |
| Banner in home fino al 2 ottobre | **FATTO** — da riproporzionare visivamente (difetto D-05) |
| Iscrizione all'evento | **FATTO**, soggetta al gate G2 |
| Edizioni, commissioni, tavoli | **DA COSTRUIRE** |
| Proposte, progetti, milestone, monitoraggio | **DA COSTRUIRE** |
| Relazione annuale | **DA COSTRUIRE** |
| Configurabilità delle commissioni | **DA COSTRUIRE** |

Priorità P1, dopo il completamento del nucleo P0.
