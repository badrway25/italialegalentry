# CURRENT PLATFORM AUDIT — la piattaforma autenticata allo stato attuale

Audit del 20 settembre 2026 · Riferimento: `docs/source-of-truth/PLATFORM_REQUIREMENTS_V2.md`
(derivato dal Technical Blueprint v1.0) · Prove: codice in `apps/`, screenshot `portal-*` in
`docs/qa/visual/before/`, navigazione reale su `127.0.0.1:8771` con gli account di QA.

---

## 1. Verdetto

Esiste un **portale di consultazione**. Non esiste ancora una **piattaforma operativa**.

La differenza non è di rifinitura. Un portale mostra all'utente ciò che il sistema sa di lui. Una
piattaforma gli fa fare il suo lavoro. Oggi l'area riservata risponde a «che cosa c'è nel mio
account», mentre il Technical Blueprint chiede che risponda a «dove sono nel mio percorso, che cosa
manca, che cosa devo fare adesso e chi ne è responsabile».

Copertura misurata sui requisiti di piattaforma: **24 DONE, 47 PARTIAL, 54 TODO** su 129. Il grosso
dei TODO è concentrato qui.

---

## 2. Che cosa esiste davvero

| Area | Stato | Dettaglio |
|---|---|---|
| Identità e account | **Solido** | Utente personalizzato con e-mail come identificativo, allauth, profilo, cancellazione su richiesta |
| Ruoli | **Parziale** | Nove gruppi con permessi di modello; mancano sei ruoli richiesti dal Blueprint |
| MFA | **Parziale** | Architettura pronta, imposta su `/backoffice/` |
| Area riservata | **Scheletro** | Cruscotto, richieste, percorso, documenti, scadenze, comunicazioni — in sola lettura |
| Questionario di orientamento | **Buono, ma monolingue** | Motore a regole proprio, deterministico, senza `eval()` |
| Documenti privati | **Fondamenta** | Storage privato, autorizzazione al download, validazione del caricamento |
| Audit | **Fondamenta** | `AuditEvent` esiste, copertura degli eventi parziale |
| Consensi | **Solido** | Testi versionati, registrazioni con finalità e base giuridica |
| Confine CRM | **Inerte per costruzione** | Nessuna chiamata di rete possibile con il trasporto predefinito |

### Il motore di orientamento merita una nota

`apps/orientation/engine.py` è la componente tecnicamente migliore della piattaforma: 619 righe di
Python puro, senza ORM, deterministico, con un DSL di condizioni in JSON
(`{"all": […]}`, `{"any": […]}`, `{"question_key": …, "op": "eq|in|not_in|is_true|is_false"}`),
una funzione di validazione che verifica domanda d'ingresso, riferimenti pendenti, condizioni
malformate e terminazione di ogni percorso di risposta.

**Nessun `eval()`.** Il requisito REQ-RUL-04, che il Blueprint considera critico, è già soddisfatto
a livello di meccanismo. Questo motore **non va riscritto**: va **esteso**.

Ciò che gli manca per diventare il Rule Engine giuridico descritto in D2 §7: giurisdizione, percorso,
intervallo di validità `valid_from`/`valid_to`, fonte con titolo e riferimento, `message_key`
multilingue, workflow di revisione a quattro occhi con `approved_by`/`approved_at`, e lo snapshot
completo del ruleset nell'esito.

Il modello `Ruleset` ha già `version` e `status`. È una base, non l'arrivo.

---

## 3. I nove difetti della piattaforma

### P-01 — Nessun fascicolo digitale
Il `CaseFile` non esiste. È l'entità centrale del Blueprint (§8, §9, §10) e l'oggetto attorno a cui
ruotano stati, checklist, documenti, scadenze, attori assegnati e cronologia. Senza di esso la
piattaforma non ha un soggetto: ha solo un utente con delle liste.

### P-02 — Nessun ciclo di vita
Gli undici stati del fascicolo — DRAFT, ORIENTED, REVIEW_REQUIRED, TRAINING, SELECTION,
ADMIN_PROCESS, PRE_DEPARTURE, ENTERED, POST_ENTRY, CLOSED, SUSPENDED — non sono rappresentati. Non
esistono transizioni, quindi non esistono validazioni di transizione, quindi non esistono eventi di
audit sulle transizioni sensibili.

### P-03 — Nessuna checklist con attore responsabile
`ChecklistItem` esiste in `orientation` come voce informativa dell'esito, non come impegno tracciato
con `responsible_actor` e `due_date` sul fascicolo. La domanda «chi è responsabile di questo passo»,
che il committente pone come criterio di accettazione, oggi non ha risposta nel prodotto.

### P-04 — Il Rule Engine non è ancora un dato governato
Le regole sono dati, ma senza validità temporale, senza giurisdizione, senza fonte strutturata e
senza approvazione a quattro occhi. Di conseguenza: l'esito non è riproducibile nel senso richiesto
da D2 §17 (manca lo snapshot integrale), e un editor giuridico non può lavorare senza uno
sviluppatore.

### P-05 — Il questionario è solo in francese
Rilievo CL-01 del red team, gravità alta. Su `/it/`, `/en/` e `/ar/` ogni domanda, opzione, esito,
spiegazione e voce di checklist appare in francese, dentro una cornice di interfaccia tradotta. I
modelli di traduzione esistono (`QuestionTranslation`, `ChoiceTranslation`, `OutcomeTranslation`,
`ChecklistItemTranslation`): sono vuoti. Il pubblico principale del progetto legge arabo.

### P-06 — Il cruscotto non dà priorità
Cinque riquadri di pari peso, quattro dei quali vuoti. Nessuna «prossima azione», nessun percorso,
nessuno stato, nessuna scadenza imminente in evidenza. Un utente che entra non riceve alcuna
indicazione su che cosa fare.

### P-07 — Il guscio è quello pubblico
Barra di servizio, mega-menu con sette voci pubbliche e piè di pagina istituzionale completo restano
dopo l'accesso. La navigazione laterale dell'area riservata è un elenco di sei voci senza gerarchia,
senza stato, senza contatori, senza contesto.

### P-08 — Mancano interamente sei ambienti di ruolo
Impresa (fabbisogni gestibili, non un form pubblico), soggetto autorizzato, professionista, ente
formativo, istituzione, università. Il ruolo `role:company` esiste, ma un'impresa autenticata vede
oggi lo stesso cruscotto di una persona.

### P-09 — Mancano Academy, sportello digitale e Forum come governance
Tre moduli interi del Blueprint (§3) senza alcuna implementazione. L'Academy in particolare è un P1
con un vincolo di accettazione esplicito: deve essere accessibile senza selezione.

---

## 4. Verifica dei criteri di accettazione del Blueprint

| # | Criterio (D2 §17) | Oggi |
|---|---|---|
| 1 | Ogni accesso a un fascicolo è autorizzato e tracciato | **N/A** — non esistono fascicoli |
| 2 | Ogni esito è riproducibile con lo snapshot delle regole | **NO** — manca lo snapshot integrale |
| 3 | Nessun testo promette visti o attribuisce funzioni pubbliche | **SÌ** — verificato dal red team |
| 4 | Accesso all'Academy senza selezione | **N/A** — Academy assente |
| 5 | L'impresa esprime un fabbisogno senza accedere a dati personali | **SÌ** — per assenza di qualsiasi accesso |
| 6 | Ricerca e selezione identificano il soggetto responsabile | **N/A** — modulo assente |
| 7 | Il fascicolo conserva stato, checklist, documenti, cronologia | **NO** |
| 8 | Il Forum consente proposta → commissione → progetto → monitoraggio | **NO** |
| 9 | Interfaccia in IT, FR, predisposta AR/EN | **PARZIALE** — la cornice sì, il contenuto del questionario no |
| 10 | Backup, log, segreti, ambienti separati prima della produzione | **PARZIALE** — documentato, RPO/RTO da definire |

Tre criteri su dieci sono soddisfatti; quattro non sono nemmeno applicabili perché il modulo non
esiste.

---

## 5. Sicurezza e permessi: quello che il red team ha trovato qui

Su quattro rilievi dell'area permessi e sicurezza, il verificatore indipendente ha:

- **smentito** PS-01 e PS-04,
- **confermato** PS-03 (gravità bassa),
- **parzialmente confermato** PS-02 (gravità media).

Nessuna falla di autorizzazione grave nell'area riservata attuale. È un risultato onesto ma va letto
nel contesto: la superficie è piccola perché le funzioni sono poche. I test di permesso a livello di
oggetto richiesti dalla direttiva §61 diventeranno significativi solo quando esisteranno fascicoli,
processi di selezione e assegnazioni.

---

## 6. Che cosa conservare

| Componente | Perché |
|---|---|
| `orientation/engine.py` | DSL sicuro, deterministico, validato. Base del futuro Rule Engine |
| `accounts` | Utente personalizzato e ruoli corretti; va esteso, non rifatto |
| `consents` | Modello di consenso conforme: finalità, base giuridica, versione, provenienza |
| `documents` | Storage privato e autorizzazione al download già impostati correttamente |
| `audit.AuditEvent` | Struttura corretta; va esteso a più eventi e reso append-only |
| `portal.Message`, `portal.Deadline` | Entità utili; cambieranno posizione nel modello, non natura |
| Gate, flag e orologio | Meccanismo di pubblicazione che deve valere anche per i moduli nuovi |

---

## 7. Sequenza di costruzione proposta

1. **Fondamenta del dominio**: `CaseFile`, stati e transizioni validate, `ChecklistItem` con attore
   responsabile e scadenza, eventi di audit sulle transizioni.
2. **Rule Engine giuridico**: estensione del motore esistente con giurisdizione, validità, fonte,
   versione, workflow a quattro occhi e snapshot integrale nell'esito.
3. **Guscio della piattaforma**: navigazione per ruolo, contesto, prossima azione, separato dal
   pubblico.
4. **Esperienza della persona**: percorso visualizzato, prossima azione, esito con motivazione e
   fonti, documenti con requisiti e stati, checklist.
5. **Esperienza dell'impresa**: fabbisogni gestibili, profilo professionale, avanzamento.
6. **Traduzione del questionario** in italiano, inglese e arabo.
7. Poi P1: Academy, selezione autorizzata, skill gap, post-ingresso, workspace dei restanti ruoli,
   sportello digitale, Forum come governance.
