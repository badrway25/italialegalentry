# RULE ENGINE GOVERNANCE — regole giuridiche come dati governati

Versione 1.0 · 20 settembre 2026 · Fonte: Technical Blueprint v1.0 §7 · Requisiti REQ-RUL-*
Conflitto risolto: CR-11 (l'esito `eligible` non esiste)

---

## 1. Principio

> Il Rule Engine non è un oracolo. È un registro di regole datate, con una fonte e un responsabile,
> che produce un esito **orientativo** e spiegabile.

Tre conseguenze operative:

1. **Le regole sono dati, non codice.** Un giurista deve poterle scrivere, rivedere e datare senza
   uno sviluppatore. Il Blueprint §20 lo impone: le regole giuridiche «devono essere versionate come
   dati/regole con fonti».
2. **Ogni esito è spiegabile.** Non «il sistema dice di no», ma «la regola R-2026-014, in vigore dal
   1° marzo 2026, fonte X, richiede Y, che nel tuo caso manca».
3. **Nessun esito è una determinazione amministrativa.** La piattaforma non attribuisce visti, nulla
   osta, permessi, riconoscimenti o autorizzazioni.

## 2. Gli esiti ammessi

| Esito | Significato | Come si mostra |
|---|---|---|
| `POSSIBLE` | Il percorso appare pertinente alla situazione descritta | «Questo percorso sembra pertinente alla tua situazione» |
| `MISSING_REQUIREMENT` | Pertinente, ma manca un elemento verificabile | «Manca: …» con la fonte del requisito |
| `WARNING` | Pertinente con un rischio o una condizione da conoscere | «Attenzione: …» |
| `STOP` | Un elemento impedisce di presentare il percorso come praticabile | Il percorso **non** viene proposto come praticabile |
| `REVIEW_REQUIRED` | Serve una valutazione discrezionale o professionale | Proposta di revisione umana |

**`eligible` non esiste.** Il Blueprint lo elenca fra gli effetti possibili, ma sarebbe letto
dall'utente come «ho diritto di entrare». Equivale a `POSSIBLE` e viene registrata l'equivalenza per
tracciabilità. Vedere CR-11.

Parole vietate nell'interfaccia in ogni lingua: «idoneo», «ammissibile», «hai diritto», «approvato»,
«garantito», e ogni formula che suggerisca una decisione amministrativa.

## 3. Anatomia di una regola

| Campo | Tipo | Obbligatorio | Nota |
|---|---|---|---|
| `rule_id` | identificativo stabile | sì | Non cambia fra le versioni |
| `jurisdiction` | ordinamento o Paese | sì | Es. `IT`, `MA` |
| `pathway` | percorso | sì | lavoro, studio, famiglia, formazione, altro |
| `condition` | JSON leggibile dalla macchina | sì | DSL ristretto, vedere §5 |
| `effect` | uno dei cinque esiti | sì | |
| `message_key` | chiave del messaggio multilingue | sì | Il testo sta nel sistema di traduzione, non nella regola |
| `source_title` | titolo della fonte | sì | |
| `source_ref` | riferimento ufficiale o interno | sì | Norma, circolare, pagina di un'autorità |
| `source_url` | collegamento | no | Se pubblico e stabile |
| `valid_from` | data | sì | |
| `valid_to` | data | no | Vuoto = ancora in vigore |
| `version` | intero | sì | Incrementa a ogni modifica sostanziale |
| `review_status` | stato del workflow | sì | vedere §4 |
| `created_by`, `created_at` | autore | sì | |
| `approved_by`, `approved_at` | approvatore | solo se `APPROVED` o `ACTIVE` | **Diverso dall'autore** |
| `retired_at`, `retired_by` | ritiro | solo se `RETIRED` | |
| `note` | motivazione interna | no | Non mostrata all'utente |

## 4. Workflow a quattro occhi

Aggiornato il 21 settembre 2026: due stati aggiunti, e il percorso non si salta più.

```
  LEGACY_CANDIDATE ─┐
                    ├─► SOURCE_VERIFIED ──► LEGAL_REVIEW ──► APPROVED ──► ACTIVE ──► RETIRED
       DRAFT ───────┘          │                  │              │
         ▲                     │                  │              │
         └─────────────────────┴──────────────────┘              │
                    rinviata con motivazione                      ▼
                                                    nuova versione in DRAFT
```

| Stato | Chi può portarla qui | Vincolo |
|---|---|---|
| `LEGACY_CANDIDATE` | il seed, o chi importa contenuto ereditato | Punto di partenza obbligato per il contenuto della piattaforma precedente. Non vincola nessuno |
| `DRAFT` | Legal/Rule Editor | Modificabile liberamente. Punto di partenza per una regola redatta dalla norma |
| `SOURCE_VERIFIED` | Legal/Rule Editor | **Ogni fonte deve portare data di consultazione, nome di chi ha verificato, e URL o autorità.** Rifiutato altrimenti, con l'elenco dei riferimenti che mancano |
| `LEGAL_REVIEW` | Legal/Rule Editor | Non più modificabile senza tornare in DRAFT. Raggiungibile **solo** da `SOURCE_VERIFIED` |
| `APPROVED` | **un secondo** Legal/Rule Editor o un revisore designato | **L'autore non può approvare la propria regola.** Vincolo applicato nel dominio, non nell'interfaccia. Registra `approved_by_label`, che sopravvive all'anonimizzazione dell'account |
| `ACTIVE` | Legal/Rule Editor | Solo con `valid_from` raggiunta, almeno una fonte, e un approvatore registrato. **Il database rifiuta la riga altrimenti** |
| `RETIRED` | Legal/Rule Editor | Resta consultabile e resta negli snapshot già prodotti |

### Perché sono stati aggiunti

`SOURCE_VERIFIED` esiste perché il passo che nomina veniva saltato. Tutte e quindici le fonti
seminate portavano un riferimento esatto — «D.Lgs. 286/1998, art. 22» — e **nessuna** portava una
data di consultazione, un nome o un URL. Quei riferimenti arrivavano a un giurista come se
qualcuno li avesse aperti. Un riferimento non è una verifica.

`LEGACY_CANDIDATE` esiste perché il contenuto della vecchia piattaforma è buono e la sua autorità
no. Gli elenchi documentali per tipo di visto sono precisi, scritti da chi conosce la materia — e
senza fonte, senza data, senza versione, approvati da chiunque avesse un permesso. Importare il
contenuto è giusto; importarne l'autorità no, e i due arrivano insieme se non c'è uno stato che li
separa.

### `provenance`: da dove viene il testo

| Valore | Significato |
|---|---|
| `drafted_from_source` | Redatta leggendo la norma |
| `legacy_platform` | Ripresa dalla piattaforma precedente |
| `legacy_derived` | Derivata da un contenuto della piattaforma precedente |

Viaggia nello snapshot di ogni pre-valutazione, insieme a `approved_by_label`. Le due rispondono a
una domanda che il resto dello snapshot non può: non «che cosa diceva la regola» ma «su quale
autorità». Un esito prodotto dal set dimostrativo porta un'etichetta che dice, a parole, che nessun
giurista l'ha approvato — e la porta **dentro la valutazione archiviata**, quindi la smentita
sopravvive a chi la rilegge fra sei mesi senza essere stato qui.

Il Blueprint §4 lo dice in una riga: «Workflow di approvazione a quattro occhi». Il Legal/Rule Editor
non ottiene privilegi estranei: non amministra utenti, non accede ai fascicoli, non modifica
configurazioni tecniche (REQ-IAM-10).

Ogni transizione di stato di una regola genera un `AuditEvent`.

## 5. Il DSL delle condizioni

**Nessun `eval()`. Nessun `exec()`. Nessuna importazione dinamica. Nessun template renderizzato su
input dell'utente.**

Il valutatore esiste già in `apps/orientation/engine.py`: Python puro, deterministico, senza ORM,
619 righe, con validazione di integrità. La grammatica attuale:

```json
{}                                                        // sempre vero
{"all": [<nodo>, ...]}                                    // congiunzione
{"any": [<nodo>, ...]}                                    // disgiunzione
{"question_key": "k", "op": "eq",       "value": "x"}     // uguaglianza
{"question_key": "k", "op": "in",       "value": ["a","b"]}
{"question_key": "k", "op": "not_in",   "value": ["a","b"]}
{"question_key": "k", "op": "is_true"}
{"question_key": "k", "op": "is_false"}
```

Semantica difensiva già implementata e da conservare: **una condizione che riferisce una domanda
senza risposta è falsa.** Nessuna informazione significa nessuna inferenza. Mai il contrario.

Estensioni previste per il Rule Engine giuridico, da aggiungere con la stessa disciplina:

```json
{"profile_field": "age",          "op": "gte", "value": 18}
{"profile_field": "nationality",  "op": "in",  "value": ["MA"]}
{"document": "passport",          "op": "valid_at", "value": "$assessment_date"}
{"not": <nodo>}
```

Regole del DSL: nessun operatore che esegua codice; nessun accesso a oggetti arbitrari; ogni campo
riferibile è dichiarato in una allowlist; la profondità di annidamento è limitata; ogni regola è
validata al salvataggio e rifiutata se malformata.

## 6. Esecuzione

```
input: profilo della persona + risposte + obiettivo + data di valutazione
 1. seleziona le regole ACTIVE per giurisdizione e percorso, con valid_from ≤ data ≤ valid_to
 2. valuta i prerequisiti e le condizioni
 3. registra ogni regola applicata con la sua versione
 4. genera gli esiti e i requisiti mancanti
 5. associa fonti e voci di checklist
 6. se esiste uno STOP, il percorso NON è presentato come praticabile
 7. se serve una valutazione discrezionale, produce REVIEW_REQUIRED
 8. salva lo snapshot completo dell'esito nel fascicolo
```

Il punto 1 è oggi il principale scarto rispetto all'implementazione: la selezione per data di
validità non esiste ancora.

Il punto 8 è il secondo: oggi si conserva il riferimento al ruleset, non il ruleset.

## 7. La pagina di esito

Deve contenere, sempre:

| Elemento | Perché |
|---|---|
| Il risultato, in parole neutre | Nessuna determinazione amministrativa |
| La motivazione, regola per regola | Spiegabilità |
| I requisiti pertinenti | Che cosa serve |
| Gli elementi mancanti | Che cosa manca, con il responsabile |
| Le fonti autorevoli | Da dove viene l'informazione |
| Data della valutazione e versione del ruleset | Riproducibilità e onestà temporale |
| Il disclaimer | La pre-valutazione ha carattere informativo |
| La richiesta di revisione umana | Quando serve o quando l'utente la vuole |

La pagina **non** deve contenere: punteggi, percentuali di probabilità, stime di tempo non fondate,
promesse, o la logica interna delle regole (che è materiale riservato: vedere la policy sui materiali
confidenziali).

## 8. L'editor delle regole

Un'interfaccia dedicata, non le righe grezze del back-office generico.

| Funzione | Descrizione |
|---|---|
| Elenco | Filtri per giurisdizione, percorso, stato, validità, fonte |
| Dettaglio | Tutti i campi, con l'editor delle condizioni assistito |
| Diff fra versioni | Che cosa è cambiato, quando, per mano di chi |
| Anteprima | Esecuzione su persone sintetiche predefinite, per vedere l'effetto prima di attivare |
| Workflow | Invio in revisione, approvazione, attivazione, ritiro |
| Storico | Tutte le versioni e tutte le approvazioni |
| Fonti | Anagrafica delle fonti riutilizzabili |

L'anteprima su persona sintetica è la funzione che rende il sistema realmente governabile: permette a
un giurista di verificare l'effetto di una modifica senza toccare dati reali.

## 9. Stato attuale, senza indulgenza

Aggiornato dopo l'implementazione di `apps/rules` (commit «feat(rules)»).

| Requisito | Oggi | Dove |
|---|---|---|
| Nessun `eval()`, DSL controllato | **FATTO** | `apps/rules/engine.py`, `apps/orientation/engine.py` |
| Elenco chiuso dei campi leggibili | **FATTO** | `engine.ALLOWED_FIELDS`, verificato al salvataggio |
| Un fatto assente non rende mai vera una condizione | **FATTO** | `engine.evaluate_condition`, 8 test parametrizzati |
| Validazione di integrità del ruleset | **FATTO** | `LegalRule.clean()` → `validate_condition` |
| Regole come dati amministrabili | **FATTO** | `LegalRule`, editor in `/backoffice/rules/` |
| Giurisdizione, percorso, fonte strutturata | **FATTO** | `LegalSource` + M2M obbligatoria per l'attivazione |
| Validità temporale e selezione per data | **FATTO** | `LegalRuleQuerySet.in_force(on_date)` — data della valutazione, non di oggi |
| Versione per regola e registrazione delle regole applicate | **FATTO** | `rule_id` + `version` unici; `PathwayAssessment.applied_rules` |
| Snapshot integrale nell'esito | **FATTO** | `as_snapshot()` congela condizione **e** fonti; `services.replay()` |
| Workflow a quattro occhi | **FATTO** | `services.transition` solleva `PermissionDenied` se autore = revisore |
| Editor dedicato con diff e anteprima | **FATTO** | `rules/admin.py`, viste `diff` e `preview` |
| Audit sulle modifiche delle regole | **FATTO** | `rule.transition`, `rule.new_version` |
| Ruoli distinti di redazione e validazione | **FATTO** | `role:legal_editor` / `role:legal_approver`, incompatibili |

### Che cosa resta, e non è un dettaglio

| Punto | Stato | Perché conta |
|---|---|---|
| **Revisione giuridica del contenuto** | **APERTO** | **Nessuna regola è in vigore.** Il seed scrive 16 candidate (`apps/rules/seeds.py`): 11 bozze redatte dalla norma e 5 candidate ereditate. Le undici che erano in vigore senza approvatore sono state riportate indietro dalla migrazione `rules.0002`, e il database ora rifiuta una regola approvata o in vigore senza approvatore registrato. Per vedere il motore funzionare in locale, `manage.py rules_activate_demonstration` percorre la catena vera con un approvatore dichiaratamente fittizio, e rifiuta di partire dove i dati dimostrativi non sono ammessi. |
| **Data di consultazione delle fonti** | **APERTO** | Nessuna `consulted_on` è valorizzata: i riferimenti sono corretti ma non sono stati verificati alla fonte ufficiale in questa sede. La citazione si mostra senza data finché non lo sono. |
| **5 regole in coda di revisione** | **ATTESO** | Sono inerti: il motore valuta solo ciò che è `ACTIVE`. La coda non è un arretrato, è il punto in cui il lavoro deve passare da chi costruisce a chi risponde. |
| **art. 23 D.Lgs. 286/1998** | **ESCLUSO** | CR-07: citabile come norma di sistema, mai come titolo abilitante del progetto. Non è nel seed. |
| **Copertura dei percorsi** | **PARZIALE** | 7 degli 8 percorsi hanno almeno una regola redatta dalla norma (nessuna è in vigore); `training_in_origin_country` ne ha una sola, in revisione, per la ragione sopra. |

### L'anteprima mostra al revisore la semantica che conta

Esercitata nel back-office su `R-WORK-003`, la regola che chiede un datore di lavoro identificato:

| Fatti digitati dal revisore | Esito |
|---|---|
| `{"has_job_offer": false}` | **la regola si attiva** |
| `{"has_job_offer": true}` | tace |
| `{}` — nessuna informazione | **tace** |

La terza riga è quella che vale la pena guardare due volte. Un fatto assente non rende vera la
condizione: «nessuna informazione» non è «no». Se fosse il contrario, una regola su un documento che
nessuno ha caricato scatterebbe come se lo fosse, e in questo dominio il costo è una persona a cui
si dice che una via è chiusa. La semantica è verificata da otto test parametrizzati e — ciò che
conta per chi approva — è **visibile sullo schermo su cui firma**.

### Il criterio per dire «fatto»

Una regola è *implementata e funzionante* quando: esiste come riga, ha almeno una fonte con un
riferimento puntuale, ha una finestra di validità, è passata per due persone distinte, compare fra le
`applied_rules` di una valutazione reale e la sua fonte compare nell'elenco numerato della pagina di
esito. Le prime cinque condizioni sono verificate dai test; l'ultima è stata verificata nel browser
(`scripts/qa_person_journey.py`: fascicolo E12273C5DF, esito «Exigence manquante», cinque fonti).

La sesta condizione — che un giurista abbia detto che la regola è giusta — non è verificabile dal
codice e non è soddisfatta. È la sola ragione per cui questo modulo non può essere dichiarato pronto
per la produzione, ed è una ragione sufficiente.
