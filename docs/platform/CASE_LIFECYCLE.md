# CASE LIFECYCLE — il fascicolo digitale e il suo ciclo di vita

Versione 1.0 · 20 settembre 2026 · Fonte: Technical Blueprint v1.0 §8, §9, §10 · Requisiti REQ-CAS-*

---

## 1. Che cos'è un fascicolo

Il `CaseFile` è l'oggetto attorno a cui ruota tutta la piattaforma. Rappresenta **un percorso di una
persona verso una finalità lecita**: lavoro, studio, formazione, famiglia, altra finalità prevista
dall'ordinamento.

Una persona può avere più fascicoli, per finalità diverse o in momenti diversi. Ogni fascicolo ha un
proprietario (la persona), può avere un assegnatario (un professionista, un operatore, un ente) e
conserva la propria storia.

Il fascicolo **non decide nulla**. Registra: che cosa è stato valutato, con quali regole, che cosa
manca, chi è responsabile di ciascun passo, quali documenti sono stati prodotti, che cosa è successo
e quando.

## 2. Anatomia

| Parte | Contenuto | Modello |
|---|---|---|
| Intestazione | Persona, finalità, percorso, stato, riferimento, date | `CaseFile` |
| Valutazione | Esito del Rule Engine con snapshot del ruleset, motivazione, fonti | `PathwayAssessment` |
| Checklist | Requisiti con stato, **attore responsabile**, scadenza | `ChecklistItem` |
| Documenti | Requisiti documentali con stato, versione, scadenza | `Document` |
| Scadenze | Date comunicate o calcolate | `Deadline` |
| Attori | Chi è assegnato, con quale mandato, da quando | `CaseAssignment` |
| Formazione | Piano formativo collegato | `TrainingPlan` |
| Comunicazioni | Messaggi scambiati nel contesto del fascicolo | `Message` |
| Consensi | Stato dei consensi e dell'eventuale mandato | `Consent` |
| Cronologia | Ogni evento rilevante, immutabile | `AuditEvent` |

## 3. Gli undici stati

```
                         ┌──────────────┐
                         │    DRAFT     │  profilo o fascicolo incompleto
                         └──────┬───────┘
                                │ valutazione eseguita
                         ┌──────▼───────┐
              ┌──────────│   ORIENTED   │──────────┐  orientamento iniziale completato
              │          └──────┬───────┘          │
              │                 │                  │
   caso       │         ┌───────▼────────┐         │  percorso formativo
   discrezionale        │ REVIEW_REQUIRED│         │  attivo
              │         └───────┬────────┘         │
              │                 │ esito della revisione
              │          ┌──────▼───────┐   ┌──────▼───────┐
              └─────────►│   TRAINING   │◄──┤              │
                         └──────┬───────┘   └──────────────┘
                                │ fabbisogno collegato + attore autorizzato
                         ┌──────▼───────┐
                         │  SELECTION   │  gestita da soggetto autorizzato
                         └──────┬───────┘
                                │
                         ┌──────▼─────────┐
                         │ ADMIN_PROCESS  │  procedura amministrativa presso le autorità
                         └──────┬─────────┘
                                │ requisiti principali completati
                         ┌──────▼─────────┐
                         │ PRE_DEPARTURE  │
                         └──────┬─────────┘
                                │ ingresso registrato
                         ┌──────▼───────┐
                         │   ENTERED    │
                         └──────┬───────┘
                                │
                         ┌──────▼───────┐
                         │  POST_ENTRY  │  accompagnamento e inclusione
                         └──────┬───────┘
                                │
                         ┌──────▼───────┐
                         │    CLOSED    │
                         └──────────────┘

  SUSPENDED: raggiungibile da qualunque stato attivo, con motivazione obbligatoria;
             si ritorna allo stato precedente o a CLOSED.
```

**Non tutti percorrono tutti gli stati.** Una persona che si orienta per studio non passa mai da
SELECTION. Una che scopre uno STOP resta in ORIENTED con un esito negativo motivato. Il diagramma
descrive le transizioni possibili, non un obbligo.

## 4. Tabella delle transizioni

| Da | A | Chi può | Condizione | Audit |
|---|---|---|---|---|
| — | DRAFT | persona | creazione account e consensi | sì |
| DRAFT | ORIENTED | sistema | valutazione completata con esito diverso da STOP | sì |
| DRAFT | SUSPENDED | persona, operatore | motivazione | sì |
| ORIENTED | REVIEW_REQUIRED | sistema, operatore | esito `REVIEW_REQUIRED` o richiesta dell'utente | sì |
| ORIENTED | TRAINING | operatore, ente formativo | piano formativo attivo | sì |
| REVIEW_REQUIRED | ORIENTED | professionista | revisione conclusa senza cambio di percorso | sì |
| REVIEW_REQUIRED | TRAINING | professionista | revisione conclusa con piano formativo | sì |
| TRAINING | SELECTION | **soggetto autorizzato** | fabbisogno collegato **e** attore autorizzato valido **e** consenso specifico | **sì, obbligatorio** |
| ORIENTED | ADMIN_PROCESS | operatore | percorso senza fase di selezione | sì |
| SELECTION | ADMIN_PROCESS | soggetto autorizzato | esito positivo della selezione | sì |
| ADMIN_PROCESS | PRE_DEPARTURE | operatore | requisiti principali completati | sì |
| PRE_DEPARTURE | ENTERED | operatore | ingresso registrato | sì |
| ENTERED | POST_ENTRY | sistema | automatica | sì |
| POST_ENTRY | CLOSED | operatore, persona | percorso concluso | sì |
| qualunque attivo | SUSPENDED | persona, operatore, amministratore | motivazione obbligatoria | sì |
| SUSPENDED | stato precedente | chi ha sospeso, o superiore | motivazione | sì |
| qualunque | CLOSED | persona, amministratore | su richiesta o per decadenza | sì |

**Regole invalicabili:**

1. Nessuna transizione verso `SELECTION` senza un `AuthorizedActor` valido, non scaduto e assegnato.
   Il nome dell'attore responsabile è visibile nell'interfaccia in ogni momento in cui il fascicolo è
   in questo stato.
2. Una transizione non dichiarata in questa tabella è rifiutata dal dominio, non solo nascosta
   nell'interfaccia.
3. Ogni transizione genera un `AuditEvent` con attore, stato di partenza, stato di arrivo, motivo e
   marca temporale.
4. `SUSPENDED` richiede sempre una motivazione testuale.
5. Un fascicolo `CLOSED` è in sola lettura. Si apre un nuovo fascicolo, non si riapre il vecchio.

La colonna «Chi può» è dichiarata come dati in `cases.models.TRANSITION_ACTORS` e applicata da `cases.services.transition`, da cui `transitions_available` deriva i comandi offerti (F-7, ottobre 2026). L'amministratore vi compare solo dove la tabella lo nomina; le sole capacità che i dati aggiungono alla tabella, ciascuna con la sua ragione e in attesa di decisione, sono elencate in `cases.models.BEYOND_SECTION_4`.

## 5. Checklist

Ogni voce di checklist ha:

| Campo | Ruolo |
|---|---|
| `requirement` | Che cosa serve, in forma comprensibile |
| `status` | `PENDING`, `IN_PROGRESS`, `DONE`, `NOT_APPLICABLE`, `BLOCKED` |
| `responsible_actor` | **Chi** deve farlo: la persona, l'impresa, un'autorità, un professionista, un ente formativo |
| `due_date` | Se nota |
| `source` | La fonte che stabilisce il requisito |
| `document` | Il documento collegato, se il requisito è documentale |
| `note` | Chiarimenti |

Il campo `responsible_actor` non è decorativo: è la risposta alla domanda che il committente pone
come criterio di accettazione. Una voce senza responsabile non si salva.

**Nessuna voce di checklist può dichiarare che Italy Legal Entry compie un atto amministrativo.**
Le voci che riguardano un'autorità indicano l'autorità come responsabile e la persona come chi deve
presentare l'istanza.

## 6. Valutazione e riproducibilità

Ogni `PathwayAssessment` conserva:

- l'input (risposte al questionario, alla data della valutazione);
- il **ruleset completo** usato, non solo il suo numero di versione;
- l'elenco delle regole applicate con la loro versione;
- l'esito, la motivazione per regola, i requisiti mancanti;
- le fonti;
- la data e l'ora.

Criterio di accettazione del Blueprint: «Ogni esito del Rule Engine è riproducibile usando lo
snapshot della versione delle regole». Riprodurre significa: dato lo snapshot e l'input, rieseguire
il motore e ottenere lo stesso esito, anche se nel frattempo le regole sono cambiate.

## 7. Accesso

| Chi | Che cosa vede |
|---|---|
| La persona | Il proprio fascicolo, interamente, tranne le note interne |
| Professionista assegnato | Il fascicolo assegnato, per la durata dell'assegnazione |
| Soggetto autorizzato | Solo i dati necessari al processo di selezione assegnato |
| Ente formativo | Solo i dati necessari alla formazione assegnata |
| Impresa | **Nulla** del fascicolo. Solo, attraverso un processo di selezione attivo e con consenso specifico, i campi necessari al proprio fabbisogno |
| Istituzione, università | **Nessun fascicolo.** Solo dati aggregati previsti dall'accordo |
| Operatore, amministratore | Secondo permesso esplicito, con audit su ogni accesso |

Ogni lettura di un fascicolo da parte di chi non ne è il titolare genera un evento di audit.

## 8. Che cosa esiste oggi

**Niente di tutto questo.** `CaseFile`, `ChecklistItem` con responsabile, `CaseAssignment` e
`PathwayAssessment` con snapshot integrale sono da costruire. Esistono `OrientationSession` e
`OrientationResult`, che ne sono il precursore, e `portal.Deadline` e `portal.Message`, che vi
confluiranno.

È il primo blocco di lavoro P0.
