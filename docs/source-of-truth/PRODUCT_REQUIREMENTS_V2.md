# PRODUCT REQUIREMENTS V2 — il prodotto pubblico

Versione 2.0 · 20 settembre 2026
Perimetro: il **sito pubblico**, cioè la porta d'ingresso istituzionale dell'ecosistema.
Il prodotto autenticato è descritto in `PLATFORM_REQUIREMENTS_V2.md`.

---

## 1. Che cosa è Italy Legal Entry™ sul fronte pubblico

Un **ecosistema digitale per la mobilità regolare e la cooperazione internazionale**, promosso da
AGAMI — Dialogo Giuridico Interculturale APS, che parte dai fabbisogni dei territori italiani e
costruisce competenze nel Paese d'origine prima dell'ingresso.

La sequenza che il sito deve rendere immediatamente comprensibile (D1 §3):

> bisogno del territorio → competenze → formazione nel Paese d'origine → percorso legale → ingresso → inclusione

## 2. Che cosa **non** è, e non deve mai sembrare

| Non è | Perché conta |
|---|---|
| Un'agenzia per il lavoro | Attività riservata ai soggetti autorizzati (D1 §4) |
| Un intermediario del mercato del lavoro | Idem |
| Un marketplace di candidati | Divieto esplicito, D2 §17 e direttiva di rebase §3 |
| Una piattaforma di *matching* | Formulazione vietata da D0a in ogni lingua |
| Un fornitore di visti, nulla osta o permessi | «non attribuisce visti, nulla osta, permessi, riconoscimenti o autorizzazioni» (D2 §1) |
| Un ente che riconosce i titoli di studio | Il riconoscimento spetta alle autorità competenti |
| Un'autorità pubblica | Il sito deve avere la **qualità** di un portale istituzionale senza impersonarne uno (RB §69) |
| Un progetto autorizzato ex art. 23 D.Lgs. 286/1998 | Nessuna autorizzazione esiste (CR-07) |

Formulazioni vietate ovunque, in ogni lingua e in ogni traduzione: *Recruit in Morocco*, *matching*
come promessa di servizio, *Find Qualified Profiles*, *matching with Italian enterprises*,
*regulated enterprise matching*, *Enterprise Area — Submit a Recruitment Request*, *positions or
requested profiles*, *Registered trademark* / *Marque enregistrée* / *Marchio registrato* /
*علامة مسجلة*, il segno **®**.

Il marchio si scrive **Italy Legal Entry™**; a parole: francese « marque déposée », italiano
« marchio depositato ».

## 3. I quattro pubblici e il loro ingresso

| Pubblico | Che cosa cerca | Che cosa gli offriamo pubblicamente | Dove prosegue |
|---|---|---|---|
| **Persone** | Capire se e come esiste una via regolare per il proprio progetto | Orientamento informativo, percorsi, formazione pre-partenza, attenzione alle frodi, glossario, FAQ | Questionario e area riservata |
| **Imprese** | Trovare competenze che non trova sul territorio | Rilevazione dei fabbisogni professionali, spiegazione del metodo, progetto pilota | Area imprese autenticata |
| **Istituzioni** | Capire il modello e valutarne la cooperazione | Contesto istituzionale, Forum, progetto pilota, rete | Workspace istituzionale |
| **Università e formazione** | Partenariati, mobilità accademica, diritto comparato | Dimensione universitaria, Forum, programmi | Workspace di partenariato |

Le quattro entrate devono esistere **sempre**, in entrambi gli stati di pubblicazione, con un link
funzionante. Nessuna entrata può sparire perché un gate è chiuso: cambia la destinazione, non la
presenza.

## 4. Architettura informativa pubblica

```
BARRA DI SERVIZIO   lingua · accessibilità · identità del progetto · accesso alla piattaforma
NAVIGAZIONE         Persone · Imprese · Istituzioni · Università e Formazione · Forum · Risorse · Il progetto
```

**Home**, sequenza narrativa (RB §19) — non una landing di venticinque sezioni:

1. identità e proposta
2. avviso istituzionale in corso (il Forum, finché è temporalmente pertinente)
3. le quattro entrate dell'ecosistema
4. il metodo: bisogno → competenze → formazione → percorso regolare → inclusione
5. percorsi e orientamento
6. ecosistema di cooperazione
7. fiducia: che cosa la piattaforma fa e che cosa non fa
8. attenzione alle frodi
9. risorse e attualità recenti
10. accesso alla piattaforma
11. piè di pagina istituzionale

Le sezioni non competono tutte allo stesso livello: la gerarchia visiva deve far emergere
l'identità, l'avviso in corso e le quattro entrate.

## 5. Fasi e gate di pubblicazione

| Fase | Quando | Contenuto |
|---|---|---|
| Fase 1 | consegna entro il 17 settembre 2026 | Base istituzionale, imprese, progetto, contatto |
| Fase 2 | consegna entro il 25 settembre 2026 | Forum Vénétie–Maroc: evento del **2 ottobre 2026**, Rovigo, Sala della Gran Guardia, 15:00–18:00 |
| Fase 3 | pubblicabile **dopo il 2 ottobre 2026** | Contenuti estesi: percorsi, diplomi, formazione, vivere in Italia, FAQ, glossario, attualità, progetto pilota, area riservata |

La Fase 3 richiede **flag attivo E data raggiunta**. Le transizioni si governano dal back-office,
senza intervento di uno sviluppatore. Dopo il 2 ottobre la pagina dell'evento diventa quella del
**Forum Permanente Vénétie–Maroc**.

Gate chiusi che condizionano il prodotto pubblico:

- **G1** pagine giuridiche: manca l'Allegato 1 in **italiano** → `BLOCKED_BY_MISSING_OFFICIAL_SOURCE`
- **G2** form pubblici che raccolgono dati personali: chiusi finché G1 è chiuso
- **G5** nomi degli intervenienti: solo cariche, nessun nome
- **G6** loghi ufficiali: nessun logo di Regione o Comune finché non sono forniti e autorizzati
- **G9** analytics e tracker: **nessuno**
- **G12** attestazione di hosting UE: blocca il deploy

## 6. Contenuto e voce

- I testi prescritti dal committente si copiano **alla lettera**, senza riformulazioni, senza
  troncamenti, senza parafrasi in una meta description.
- Dove nessun testo è prescritto, il team scrive in tono **calmo, preciso, rispettoso, istituzionale,
  chiaro, umano**. Nessun gergo da SaaS, nessun entusiasmo di marketing.
- Ogni avviso distingue: informazione · attenzione · limite giuridico o procedurale · azione richiesta.
- Gli errori spiegano come rimediare.
- Nessun nome di persona fisica, in nessuna lingua, in nessun metadato.
- Un solo indirizzo pubblico: **contact@agamieuromed.org**. Nessun indirizzo `@legalitalentry.it`.

## 7. Lingue

Quattro lingue: **italiano, francese, inglese, arabo**. L'arabo è di prima classe, con RTL reale.
Il francese è la lingua sorgente e il fallback: un testo prescritto non ancora tradotto ufficialmente
si mostra in francese, marcato `lang="fr"`, mai tradotto d'iniziativa.

Il questionario di orientamento, i suoi esiti e le checklist sono contenuto del team, non testo
prescritto: **devono essere tradotti** in italiano, inglese e arabo. È oggi il difetto più grave del
fronte pubblico (rilievo CL-01 del red team).

## 8. Qualità non negoziabili

| Dimensione | Requisito |
|---|---|
| Accessibilità | WCAG 2.2 AA, senza overlay, verificata da tastiera e con lettore di schermo |
| Prestazioni | LCP < 2,5 s, CLS < 0,1, Lighthouse ≥ 90/95/95/95 |
| Privacy | Nessun tracker, nessun cookie non necessario, nessuna risorsa esterna, nessun font o immagine in hotlink |
| Sicurezza | CSP self-only sul pubblico, nessun contenuto inline non necessario |
| Responsive | Da 320 px a 1920 px; nessuno scorrimento orizzontale; la navigazione funziona senza JavaScript |
| Design | Art direction propria e riconoscibile; nessuno dei pattern vietati da RB §11 |

## 9. Criteri di accettazione del prodotto pubblico

1. Un interlocutore istituzionale che apre la home pensa: «progetto serio, maturo, credibile».
2. Nessuna interfaccia lascia intendere rilascio di visti, autorità pubblica, risultato garantito o
   intermediazione non autorizzata.
3. Le quattro entrate sono presenti e funzionanti in entrambi gli stati di pubblicazione.
4. Nessun contenuto di Fase 3 è raggiungibile o anche solo intuibile prima del 2 ottobre.
5. Nessun testo prescritto è alterato; nessun testo giuridico è inventato.
6. Le quattro lingue sono complete per l'interfaccia; il fallback francese è dichiarato e corretto.
7. Zero violazioni axe critiche o serie sulle pagine candidate al rilascio.
8. Il sito è riconoscibile anche togliendo tutte le fotografie.
