# PLATFORM REQUIREMENTS V2 — la piattaforma autenticata

Versione 2.0 · 20 settembre 2026
Fonte primaria: D2 Technical Blueprint v1.0. Perimetro: tutto ciò che sta **dietro l'accesso**.

---

## 1. Che cos'è la piattaforma

Un **ambiente di servizio consapevole del ruolo**, non un cruscotto generico. Coordina informazioni,
documenti, fasi, autorizzazioni e interazioni fra soggetti diversi, senza sostituirsi a chi detiene
funzioni pubbliche o attività riservate (D1 §6, D2 §1).

Il criterio di riuscita, dalla direttiva di rebase §72: chi entra deve pensare
«capisco dove sono, qual è il mio percorso, che cosa devo fare adesso e chi è responsabile»,
non «ecco un altro dashboard».

## 2. Ruoli

| Ruolo | Accesso principale | Vincolo invalicabile |
|---|---|---|
| **Persona** | Proprio profilo, orientamento, fascicolo, Academy, notifiche | Nessun accesso a dati di terzi |
| **Impresa** | Proprio profilo aziendale, fabbisogni, percorsi assegnati | Visibilità di persone solo con base giuridica, consenso e workflow autorizzato |
| **Soggetto autorizzato** | Pratiche di ricerca, preselezione e selezione **assegnate** | Autorizzazione verificata e valida; audit completo |
| **Ente formativo** | Piani, corsi e coorti assegnati | Solo i dati necessari alla formazione |
| **Professionista** | Fascicoli espressamente assegnati | Mandato o abilitazione dove necessari |
| **Istituzione** | Dashboard, progetti e dati previsti dall'accordo | Perimetro definito da convenzione |
| **Università** | Programmi, progetti, mobilità, Forum | Nessun accesso generalizzato ai fascicoli |
| **Moderazione** | Community e contenuti segnalati | — |
| **Redattore di contenuti** | CMS, traduzioni, pubblicazione | Nessun accesso ai fascicoli |
| **Legal/Rule Editor** | Regole, fonti, validità, versioni | **Non può auto-approvare**; nessun privilegio di superadmin |
| **Operatore** | Lavorazione quotidiana assegnata | Perimetro ristretto |
| **Amministratore** | Configurazione tecnica e utenti | Separazione dei privilegi, log obbligatori, MFA |

Principi: deny by default, minimo privilegio, autorizzazione **a livello di oggetto**, il modello non
si esaurisce in `is_staff`, un solo sistema di autenticazione per tutti i ruoli con instradamento
post-login.

«Candidato» **non** è un ruolo: è uno stato della persona dentro un processo di selezione (CR-09).

## 3. Guscio applicativo

Il guscio della piattaforma è distinto da quello pubblico: stessa identità, densità e compiti diversi.
Non si riusa il mega-menu pubblico dopo l'accesso.

Elementi, dove pertinenti al ruolo: contesto corrente · **azione successiva prioritaria** · stato del
percorso o della pratica · task · scadenze · messaggi · documenti · notifiche · sportello digitale ·
account e sicurezza · lingua.

La navigazione si adatta ai permessi: un modulo non disponibile **non si mostra** solo perché esiste
nel codice.

## 4. Percorso della Persona (esperienza di riferimento)

```
account → informativa e consensi → profilo → obiettivo → domande dinamiche → Rule Engine
→ percorsi possibili → requisiti mancanti / avvisi / stop → fonti → fascicolo → checklist
→ Academy → revisione professionale se richiesta → monitoraggio
```

Dopo l'onboarding la persona deve capire senza sforzo: dove sono · qual è il mio obiettivo · che cosa
ho completato · che cosa manca · che cosa devo fare adesso · chi è responsabile · quali documenti
servono · quali fonti sostengono l'informazione · serve una revisione umana.

Aree: **il mio percorso** (timeline strutturata) · **prossima azione** (una sola priorità) ·
**orientamento** (ultima valutazione e fonti) · **il mio fascicolo** · **documenti** ·
**checklist** con attore responsabile · **formazione** · **scadenze** · **comunicazioni** ·
**sportello digitale** · **cronologia**.

Regole di interazione: un compito per momento cognitivo, divulgazione progressiva, spiegazioni
accanto alle domande, ritorno indietro, salvataggio e ripresa, avanzamento accessibile, validazione
chiara, revisione prima dell'invio finale.

## 5. Rule Engine

**Separato dal codice. Le regole sono dati amministrabili e versionati.**

Campi della regola: `rule_id`, `jurisdiction`, `pathway`, `condition` (leggibile dalla macchina),
`effect`, `message_key`, `source_title`, `source_url/ref`, `valid_from`, `valid_to`, `version`,
`review_status`, `approved_by`, `approved_at`.

Esiti ammessi — e nessun altro:

`POSSIBLE` · `MISSING_REQUIREMENT` · `WARNING` · `STOP` · `REVIEW_REQUIRED`

Mai «idoneo», «ammissibile», «visto approvato» o equivalenti (CR-11).

Esecuzione: selezionare le regole attive per giurisdizione, percorso e **data della valutazione**;
valutare le condizioni; registrare ogni regola applicata con la sua versione; generare esiti e
requisiti mancanti; associare fonti e checklist; uno `STOP` impedisce di presentare il percorso come
praticabile; i casi discrezionali producono `REVIEW_REQUIRED`; salvare uno **snapshot** dell'esito
nel fascicolo, così che l'esito sia riproducibile.

**Nessun `eval()`.** Interprete controllato su condizioni in JSON o DSL ristretto.

Governance a quattro occhi: `DRAFT → LEGAL_REVIEW → APPROVED → ACTIVE → RETIRED`. L'autore non
approva la propria regola. Ogni modifica genera un evento di audit.

La pagina di esito mostra: risultato · motivazione · requisiti pertinenti · elementi mancanti ·
fonti autorevoli · data e versione del ruleset · disclaimer · possibilità di chiedere revisione umana.

## 6. Fascicolo digitale

Spazio di lavoro di prima classe, più vicino a un'applicazione professionale di gestione pratiche che
a una pagina di amministrazione. Intestazione stabile e navigazione contestuale.

Aggrega: persona · percorso · stato · checklist · documenti · scadenze · attori assegnati · note ove
permesse · formazione · passi amministrativi · cronologia attività · comunicazioni · stato di
consensi e mandato.

**Stati** (D2 §8): `DRAFT` · `ORIENTED` · `REVIEW_REQUIRED` · `TRAINING` · `SELECTION` ·
`ADMIN_PROCESS` · `PRE_DEPARTURE` · `ENTERED` · `POST_ENTRY` · `CLOSED` · `SUSPENDED`.

Non tutti percorrono tutti gli stati. Le transizioni sono validate. Quelle sensibili generano audit.
`SELECTION` identifica **sempre** il soggetto autorizzato responsabile.

## 7. Documenti

Dati: tipo · caricamento · versione · stato · scadenza · requisito collegato · titolare · classe di
accesso · hash di integrità · cronologia dei caricamenti.

Sicurezza: storage privato · chiavi non prevedibili · autorizzazione a **ogni** download · URL
temporanei firmati dove applicabile · allowlist MIME ed estensioni · limiti di dimensione · punto di
integrazione antivirus · nessuna esposizione diretta via `/media/` · audit di accesso e download.

Stati visibili all'utente: MANCANTE · CARICATO · IN REVISIONE · VALIDO · NON VALIDO · SCADUTO ·
DA SOSTITUIRE.

## 8. Imprese

Il cruscotto dell'impresa ruota attorno ai **fabbisogni**, non alla ricerca di persone.

Sezioni: identità e verifica dell'impresa · fabbisogni · territorio · settore · profilo professionale ·
quantità · competenze · requisiti linguistici · esperienza · fabbisogni formativi · tempistiche ·
progetti · attori responsabili · comunicazioni · avanzamento.

Un'impresa crea e gestisce più fabbisogni. I fabbisogni si aggregano per analisi territoriale.
**Nessun elenco di persone navigabile. Nessuna scheda candidato per difetto.**

## 9. Soggetti autorizzati

Dove legalmente e tecnicamente abilitato, un workspace dedicato che mostra solo i workflow assegnati:
contesto del mandato · fabbisogno assegnato · persone assegnate · fase · decisioni e azioni ·
evidenze richieste · traccia di audit.

Catena obbligatoria, senza scorciatoie:

```
CompanyNeed → AuthorizedActor → SelectionProcess → CaseFile/Person → AuditEvent
```

## 10. Formazione e Academy

Catalogo · dettaglio corso · iscrizione · moduli · progressione · completamento · materiali.
Contenuti: lingua italiana, diritti e doveri, educazione civica, sicurezza sul lavoro, cultura del
lavoro, formazione professionale, preparazione pre-partenza.

**L'accesso non dipende dalla selezione di un'impresa** (D2 §17). I certificati non sono mai
rappresentati come approvazioni amministrative.

Skill gap: competenza richiesta → competenza posseduta → gap → modulo formativo → esito atteso.
Matrici di competenze, non percentuali prive di significato. Il piano formativo è tracciabile a
persona, fabbisogno, fornitore, moduli e stato.

## 11. Percorso legale e amministrativo

Per ogni passo rilevante: **passo · stato · attore responsabile · documenti richiesti · scadenza se
nota · fonte · azione dell'utente · note o avvertenze**.

Nulla deve far apparire Italy Legal Entry come l'autorità che decide.

## 12. Post-ingresso

Onboarding · adempimenti locali · lingua · formazione · inserimento lavorativo · servizi territoriali ·
azioni del datore di lavoro · follow-up · avanzamento. Spina dorsale «prima / durante / dopo».

## 13. Sportello digitale

Escalation dall'orientamento automatico al supporto umano. Stati: SOLA INFORMAZIONE ·
CHIARIMENTO NECESSARIO · REVISIONE PROFESSIONALE RICHIESTA · ASSEGNATO · IN REVISIONE ·
RISPOSTA DISPONIBILE · CHIUSO. Rispetta mandato, permessi, ruolo professionale, privacy e audit.

**Nessun chatbot generico presentato come assistenza legale.**

## 14. Forum come modulo di governance

Profilo partecipante · commissioni miste · tavoli digitali · proposte · progetti · milestone ·
partner · monitoraggio · dati della relazione annuale.

Ciclo: Forum → priorità → commissioni → tavoli → proposte e progetti → attuazione → monitoraggio →
relazione annuale → Forum successivo.

La tassonomia delle commissioni è **configurabile**, non cablata.

## 15. Ricerca

Pubblica: guide, percorsi, FAQ, glossario, attualità, risorse ufficiali.
Di piattaforma: rigorosamente limitata dai permessi. Un utente non deve **mai** scoprire l'esistenza
di un oggetto non autorizzato attraverso i risultati. L'autorizzazione si applica **durante** la
valutazione della query, non dopo.

## 16. Audit

Eventi da tracciare: eventi di sicurezza dell'accesso · modifiche di permessi e ruoli · accessi ai
fascicoli · accesso e download di documenti sensibili · modifiche e approvazioni di regole ·
esecuzione di valutazioni · cambi di assegnazione · cambi di stato del fascicolo · consensi ·
azioni amministrative.

L'audit è orientato all'append e protetto dalla mutazione ordinaria. Nessun segreto nei log.

## 17. Configurabilità obbligatoria (D2 §20)

Non possono stare nel codice: regole giuridiche e loro validità · testi multilingue · elenco delle
commissioni · tassonomie di professioni, competenze, documenti e corsi · tempi di retention e
versioni dei consensi · partner e soggetti autorizzati · fonti dei percorsi.

## 18. Nessuna integrazione fittizia

Nessuna connessione dichiarata con ministeri, prefettura, questura, consolati, registri pubblici,
sistemi di immigrazione, fornitori di identità, università o CRM di partner senza disponibilità
tecnica e giuridica. Stati interni ammessi: `NOT_CONFIGURED`, `PENDING_AGREEMENT`, `SANDBOX`, `MOCK`.

## 19. Priorità di consegna

**P0 — deve funzionare davvero**
Identità e ruoli · onboarding della persona · Rule Engine v1 come dati versionati · pagina di esito ·
fascicolo digitale · checklist · fondamenta sicure dei documenti · fabbisogni delle imprese ·
fondamenta dell'audit · guscio di piattaforma consapevole del ruolo.

**P1** Academy · workflow di selezione autorizzata · skill gap e piano formativo · post-ingresso ·
workspace del Forum · workspace di istituzioni, università, enti formativi e professionisti ·
sportello digitale.

**P2** CRM esteso · dashboard avanzate · integrazioni esterne.

Un P0 eccellente vale più di quindici moduli simulati. L'architettura dei dati, però, deve già
prevedere pulitamente le fasi successive.

## 20. Criteri di accettazione (D2 §17)

1. Ogni accesso a un fascicolo è autorizzato e tracciato.
2. Ogni esito del Rule Engine è riproducibile con lo snapshot della versione delle regole.
3. Nessun testo dell'interfaccia promette visti o permessi né attribuisce funzioni pubbliche.
4. Una persona accede all'Academy senza essere selezionata da un'impresa.
5. Un'impresa esprime un fabbisogno senza accedere indiscriminatamente ai dati personali.
6. Le fasi di ricerca e selezione identificano sempre il soggetto responsabile.
7. Il fascicolo conserva stato, checklist, documenti e cronologia.
8. Il Forum consente il passaggio proposta → commissione → progetto → monitoraggio.
9. Interfaccia almeno IT e FR, predisposta per AR ed EN — nel nostro caso tutte e quattro.
10. Backup, logging, gestione dei segreti e separazione degli ambienti attivi prima della produzione.

E, dalla direttiva di rebase §61, i test di permesso a livello di oggetto:
persona A non accede a persona B · impresa A non accede a impresa B · l'impresa non vede persone
arbitrarie · il professionista vede solo i casi assegnati · l'ente formativo solo i dati di
formazione autorizzati · l'istituzione solo il perimetro di convenzione · l'università nessun
fascicolo privato · i partecipanti del Forum nessuna informazione privata altrui · il personale senza
permesso non modifica le regole · il Legal/Rule Editor non ottiene privilegi estranei · un
identificativo scoperto a mano non aggira mai i permessi.
