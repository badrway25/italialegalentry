# SERVICE BLUEPRINT — il servizio visto da davanti e da dietro

Versione 1.0 · 20 settembre 2026 · Fonte: Master Dossier v2.0 §3, §7 · Technical Blueprint v1.0 §5, §6

---

## 1. Il principio del servizio

Il modello rovescia la prospettiva tradizionale. Non parte da un'offerta indistinta di persone
disponibili all'estero, ma dai **bisogni effettivi dei territori italiani**.

```
BISOGNO DEL TERRITORIO → COMPETENZE → FORMAZIONE NEL PAESE D'ORIGINE
    → PERCORSO LEGALE → INGRESSO → INCLUSIONE
```

Questo non è uno slogan: è la struttura del servizio, e quindi la struttura del prodotto. Ogni
schermata deve poter essere collocata in uno di quei sei momenti.

## 2. Blueprint del percorso della persona

| | Prima | Durante | Dopo |
|---|---|---|---|
| **Momento** | Orientamento e preparazione | Percorso legale e amministrativo | Ingresso e inclusione |
| **Azione della persona** | Risponde, carica documenti, si forma | Attende, integra, rispetta le scadenze | Si inserisce, prosegue la formazione |
| **Superficie visibile** | Questionario, esito, checklist, Academy | Fascicolo, stato, scadenze, comunicazioni | Piano post-ingresso, servizi territoriali |
| **Dietro le quinte** | Rule Engine, snapshot, creazione del fascicolo | Transizioni di stato, assegnazioni, audit | Monitoraggio, follow-up |
| **Attori competenti** | Ente formativo, professionista | Autorità competenti, soggetto autorizzato, professionista | Datore di lavoro, servizi territoriali |
| **Sistemi** | Motore delle regole, gestione documentale | Fascicolo, notifiche, audit | Piano, task, indicatori |
| **Rischio principale** | Che la persona creda a una promessa | Che non sappia chi è responsabile | Che il percorso si interrompa |
| **Contromisura di prodotto** | Disclaimer, esiti neutri, fonti | Responsabile esplicito su ogni voce | Piano con scadenze e follow-up |

## 3. Blueprint del percorso dell'impresa

| | Rilevazione | Costruzione | Accompagnamento |
|---|---|---|---|
| **Momento** | Espressione del fabbisogno | Formazione e percorso | Arrivo e inserimento |
| **Azione dell'impresa** | Descrive mansioni, competenze, tempi | Segue l'avanzamento | Accoglie, forma, monitora |
| **Superficie visibile** | Form pubblico, poi fabbisogno gestito | Stato del fabbisogno, attori, formazione | Piano post-ingresso lato impresa |
| **Dietro le quinte** | Aggregazione territoriale | Skill gap, piano formativo, selezione autorizzata | Monitoraggio |
| **Attori competenti** | Associazioni di categoria, enti territoriali | Soggetto autorizzato, ente formativo | Datore di lavoro |
| **Rischio principale** | Che l'impresa creda di poter scegliere persone da un catalogo | Che l'attività riservata sia svolta da chi non è autorizzato | Che l'inserimento fallisca |
| **Contromisura di prodotto** | Nessun elenco di persone, mai | Attore autorizzato obbligatorio e sempre nominato | Piano e follow-up |

## 4. I punti di contatto e chi li presidia

| Punto di contatto | Chi lo presidia | Che cosa promette | Che cosa non promette |
|---|---|---|---|
| Sito pubblico | Redattore di contenuti | Informazione qualificata e orientamento | Nessun risultato amministrativo |
| Questionario | Rule Engine + Legal/Rule Editor | Una pre-valutazione informativa con fonti | Nessuna idoneità |
| Esito | Rule Engine | Percorsi pertinenti, requisiti, elementi mancanti | Nessun esito di una pratica |
| Fascicolo | Operatore, professionista | Traccia ordinata del percorso | Nessuna istruttoria pubblica |
| Documenti | Persona, professionista | Conservazione sicura e stati chiari | Nessuna validazione ufficiale |
| Academy | Ente formativo | Formazione accessibile | Nessun titolo abilitante, salvo dove lo sia davvero |
| Selezione | **Soggetto autorizzato** | Processo tracciato sotto la sua responsabilità | Italy Legal Entry non è intermediario |
| Sportello | Professionista | Revisione umana quando serve | Nessuna consulenza automatizzata |
| Forum | Segreteria del Forum | Cooperazione istituzionale tracciata | Nessun impegno delle istituzioni |

La colonna «che cosa non promette» non è difensiva: è il contenuto che il committente ha chiesto di
rendere esplicito nella sezione «che cosa fa e che cosa non fa».

## 5. Il momento più delicato: l'esito

È il punto in cui il prodotto rischia di più. Una persona che ha risposto a dieci domande sulla
propria vita riceve una risposta e le attribuirà più autorità di quella che ha.

**Contromisure obbligatorie nel prodotto:**

1. L'esito si chiama «pre-valutazione a carattere informativo», sempre, in tutte le lingue.
2. Ogni affermazione porta la sua fonte.
3. Ogni esito porta la data e la versione delle regole usate.
4. Uno `STOP` non presenta il percorso come praticabile: non lo nasconde, lo qualifica.
5. La possibilità di chiedere una revisione umana è visibile accanto all'esito, non in fondo.
6. Nessun punteggio, nessuna percentuale, nessuna stima di durata non fondata.

## 6. Escalation verso l'umano

```
orientamento automatico
   │
   ├── SOLA INFORMAZIONE            l'esito basta
   ├── CHIARIMENTO NECESSARIO       la persona non ha capito o il caso è ambiguo
   ├── REVISIONE PROFESSIONALE RICHIESTA   il Rule Engine ha prodotto REVIEW_REQUIRED
   │        │
   │        ├── ASSEGNATO           a un professionista competente
   │        ├── IN REVISIONE
   │        ├── RISPOSTA DISPONIBILE
   │        └── CHIUSO
   └──
```

La piattaforma **non è concepita come esclusivamente automatizzata**: lo dice il Dossier SIAE §10 e lo
ripete il Master Dossier. Lo sportello digitale è la componente che rende onesta questa affermazione.

## 7. Dove il servizio incontra i suoi limiti

| Limite | Conseguenza di prodotto |
|---|---|
| Le attività riservate spettano ai soggetti autorizzati | Nessun workflow di selezione senza attore autorizzato |
| Il riconoscimento dei titoli spetta alle autorità | L'area diplomi orienta, non riconosce |
| I visti e i permessi li rilasciano le autorità | Nessuna interfaccia che suggerisca il contrario |
| Le regole giuridiche cambiano | Validità temporale, snapshot, data visibile |
| La piattaforma non è un titolare di funzioni pubbliche | Nessun logo, nessun emblema, nessun registro ufficiale simulato |
| Nessuna integrazione istituzionale è attiva | Stati `NOT_CONFIGURED`, `PENDING_AGREEMENT`, `SANDBOX`, `MOCK` |

## 8. Indicatori di riuscita del servizio

Non sono metriche di vanità. Sono le domande a cui il Forum e le istituzioni chiederanno risposta.

| Indicatore | Come si misura | Dove |
|---|---|---|
| Fabbisogni espressi per territorio e settore | Conteggio dei `CompanyNeed` | Aggregato, mai nominativo |
| Percorsi formativi avviati e completati | `Enrollment` | Aggregato |
| Fascicoli per stato | `CaseFile.status` | Aggregato |
| Revisioni professionali richieste e concluse | Sportello | Aggregato |
| Proposte del Forum diventate progetti | `ForumProposal → ForumProject` | Relazione annuale |
| Tempo medio fra orientamento e fascicolo completo | Cronologia | Aggregato |

Ogni indicatore condiviso con un'istituzione è **aggregato**, mai individuale, e il perimetro è
definito dall'accordo.
