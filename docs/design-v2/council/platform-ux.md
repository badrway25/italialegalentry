# DESIGN COUNCIL V2 — PLATFORM UX · LEGAL-TECH PRODUCT · INFORMATION ARCHITECTURE

Revisore: architetto UX di piattaforma. Data: 23 settembre 2026. Oggetto: `dashboard.html` e `home.html` delle
direzioni A / B / C, confrontati con la baseline rifiutata (`docs/design-v2/before/person_dashboard_desktop.png`,
`case_file_desktop.png`). Metodo: Chromium headless di Playwright (browser proprio), 1440×900 e 390×844, attesa 3 s,
piega + pagina intera + ritagli dei componenti; 30 stop di Tab per dashboard con misura di `:focus-visible`, anello,
copertura da header sticky; apertura di ogni toggle da tastiera. Evidenze in `docs/design-v2/council/shots/ux/`
(`<dir>_<pagina>_<desk|mob>_<fold|full>.png`, `*_clip_*.png`, `*_kbd_*.png`, `*_home_desk_routes*.png`, `*_process*.png`).
Nota: nei ritagli alti l'header sticky appare a metà immagine — artefatto della cattura, non un difetto.

## 0. La baseline: i fatti che devono sopravvivere (verificati riga per riga)

Barra: Italy Legal Entry™ · Contexte E46E03B461 · Site public · qa-person · Français. Breadcrumb Accueil › Espace réservé.
Fatti: DOSSIER E46E03B461 · OBJECTIF Travail · ÉTAT Orientation terminée depuis le 21.09.2026 · RESPONSABLE «Vous — aucun
intervenant n'est assigné à ce dossier» · AVANCEMENT «0 sur 5 éléments complétés». PROCHAINE ÉTAPE «Identifier les
interlocuteurs et les autorités compétents pour votre situation avant toute démarche» · RESPONSABLE L'autorité compétente ·
«Cette étape ne dépend pas de vous». Sette tappe 01–07 con 02 = ÉTAPE ACTUELLE (nessun responsabile per tappa nella
baseline). Checklist a 5 righe: élément · état (À FAIRE) · responsable (autorité compétente + nota «Selon l'autorité
compétente pour votre situation»; la personne ×3; l'équipe du projet + «Point d'attention signalé par l'équipe du projet»)
· échéance «—». Documenti: work_contract.pdf Contrat, language_certificate.pdf e diploma.pdf Diplôme ou titre, tutti NON
ANALYSÉ. Pré-évaluation «Parcours pertinent» con il paragrafo completo (compresa la frase «Prochaines étapes à caractère
informatif : …»), JEU DE RÈGLES v1 évaluée le 21.09.2026 + disclaimer «ne s'appuie sur aucune règle actuellement en
vigueur… jamais une décision» + «Voir le détail de la pré-évaluation». Messages e Dates à retenir vuoti. Compte (qa-person,
Personne, 21.09.2026 16:45, due bottoni). Footer Privacy · Conditions · Avertissement · contact@agamieuromed.org.
Nel fascicolo (non prototipato da nessuna direzione): colonna FONDEMENT, select «À faire» + «Mettre à jour» per le righe
della persona, «Intervenants: aucun intervenant n'est assigné… personne d'autre n'y a accès», modulo «Faire évoluer l'état».

## 1. Direzione A — «Rete luminosa»

| PLATFORM UX | CREDIBILITÀ | COERENZA | COMPOSIZIONE | MOBILE | ACCESSIBILITÀ (tastiera) | Sopravvivenza contenuti |
|---|---|---|---|---|---|---|
| 8 | 7 | 8 | 7 | 7 | 7 | **FAIL** |

Contenuti — fatti mancanti/alterati/inventati: (1) la frase «Prochaines étapes à caractère informatif : consulter la page
du parcours, préparer la documentation généralement requise et prendre contact avec les acteurs compétents» è **assente**
dalla pré-évaluation (`grep` = 0 occorrenze; `a_dashboard_desk_full.png`); (2) «0 en retard» sotto Avancement è una
metrica **inventata**, non presente in baseline; (3) responsabili per tappa **inventati e non marcati**: «La plateforme»
(02), «Organisme de formation», «Autorité compétente», «Territoire d'accueil» (07) — nessuna dicitura «indicatif» nel
dashboard (solo nella home); (4) «La plateforme» come *responsabile* della tappa 02 può essere letto come competenza
procedurale della piattaforma; (5) «Voir les interlocuteurs» è una CTA nuova che punta a `#`. Nessuna dicitura vietata.

Punti di forza: (1) la prima schermata a 1440×900 risponde alle cinque domande: «Vous êtes ici» su 02, prossimo atto con
responsabile e «ne dépend pas de vous», 0/5, frontiera **MA → IT** tratteggiata tra 05 e 06 (`a_dashboard_desk_fold.png`);
(2) il rail 2.0 è il migliore dei tre: texture + glifo + numero + parola di stato + legenda, mai solo colore, verticale a
390 con la frontiera conservata (`a_dashboard_mob_clip_rail.png`); (3) shell efficiente: barra inchiostro, rail
comprimibile a 68 px con Enter/Space e Ctrl+B, nomi accessibili mantenuti da compresso (`a_kbd_desk_rail_collapsed_focus.png`),
promemoria antifrode nel rail; (4) checklist come `<table>` con caption e `scope`, responsabile con glifo e nota, conteggio
«5 éléments · 0 complétés»; (5) stati vuoti con il glifo-porta, coerenti con la home; un solo blu per link/CTA/focus.

Difetti: (1) le etichette sotto i segmenti del rail hanno baseline sfalsate (01 a y≈495, 02 a y≈478, 05 a y≈505):
sembra un errore, non un ritmo (`a_dashboard_desk_fold.png`); (2) la banda scura occupa ~580 px della piega: il prossimo
atto entra per un pelo, a 1366×768 uscirebbe; (3) a 390 la scheda dei fatti spinge rail e prossimo atto alla 2ª–3ª
schermata (`a_dashboard_mob_fold.png`: solo i fatti); (4) nella checklist mobile l'etichetta ÉCHÉANCE è centrata e il
valore «—» va a capo a sinistra (`a_dashboard_mob_clip_check.png`); (5) il campo di ricerca «Ctrl K» e i menu account/lingua
sono finti: `aria-expanded="false"` che non cambia con Enter; a 390 i due bottoni account e lingua **non hanno nome
accessibile** (snapshot ARIA: `button` senza nome ×2); il rail non ha `aria-current="step"` (stato solo nel testo).

Must-fix A: ripristinare la frase mancante verbatim; togliere «0 en retard» o calcolarlo da dati reali con data; marcare
i responsabili per tappa «à titre indicatif» finché non arrivano dal Rule Engine, e non usare «La plateforme» come
responsabile; allineare le etichette del rail; dare nome ai bottoni mobile e collegare i menu; `aria-current="step"`;
`aria-controls` sul toggle del rail; cablare o rimuovere «Voir les interlocuteurs».

## 2. Direzione B — «Profondità architettonica»

| PLATFORM UX | CREDIBILITÀ | COERENZA | COMPOSIZIONE | MOBILE | ACCESSIBILITÀ (tastiera) | Sopravvivenza contenuti |
|---|---|---|---|---|---|---|
| 6 | 7 | 8 | 6 | 6 | 8 | **FAIL** (fatto aggiunto errato) |

Contenuti: tutti i fatti della baseline sono presenti e verbatim (pré-évaluation completa, note dei responsabili, «Aucune
échéance» per lo screen reader). È l'unica direzione che scrive «Le responsable de chaque étape est indiqué à titre
indicatif : les décisions relèvent uniquement des autorités compétentes». **Ma** il rail raggruppa 04 «Procédures auprès
des autorités compétentes» e 05 «Préparation du départ» sotto «ITALIE · PROCÉDURES ET INCLUSION»
(`b_dashboard_desk_fold.png`, `b_dashboard_mob_clip_rail.png`): una persona con un fascicolo legge che prepara la partenza
*in Italia*. Fatto di giurisdizione inventato ed errato; la frontiera va tra 05 e 06 (come in A e come nel processo della
home di A: 04 = MAROC ↔ ITALIE). Nessuna dicitura vietata.

Punti di forza: (1) la targa del dossier è la più leggibile: riferimento mono 30 px, chip di stato, misuratore a cinque
segmenti = conteggio, mai percentuale; (2) rail con «Étape 2 sur 7 · étape actuelle : pré-évaluation», parole di stato
TERMINÉE / ÉTAPE ACTUELLE / À VENIR con glifo, `aria-current="step"`, due `<ol>` etichettati; (3) menu account e lingua
come `<details>` nativi: Enter/Space/Escape funzionano senza JS; la tabella è una regione scorrevole focalizzabile con
nome; (4) checklist e documenti come registro calmo, hairline, nessuna ombra (DENSE rispettato); (5) versione mobile del
rail la più chiara dei tre (bordo colorato + parola di stato allineata a destra).

Difetti: (1) a 1440×900 «Prochaine étape» sta **sotto la piega** (inizia a y≈880): la prima schermata dice dove sono ma non
cosa viene dopo (`b_dashboard_desk_fold.png`); (2) la navigazione dell'app (10 destinazioni) sta a y≈870 su desktop e, a
390, dopo il rail e prima del prossimo atto (3ª schermata): l'indice numerato 01–10 è un ornamento, non uno shell
(`b_kbd_desk_stop16.png`, `b_dashboard_mob_clip_rail.png`); (3) la piega è spesa in titolo a 64 px + targa + rail; a 390
titolo 64 px e riferimento 30 px sono sproporzionati (`b_dashboard_mob_fold.png`); (4) l'inspector destro ospita tre stati
vuoti (Messages, Dates, Compte) mentre la pré-évaluation — l'unico contenuto sostantivo — è in fondo alla colonna centrale
(y≈2200, `b_dashboard_desk_full.png`); (5) nessun elemento interattivo nel prossimo atto e nei documenti: 24 stop di Tab in
tutto, il ciclo ricomincia dal body; le parole di stato nel rail non sono allineate tra colonne (01 a y 722, 04 a y 686).

Must-fix B: correggere la frontiera (05 in Marocco; 04 «MA ↔ IT» o senza territorio); portare «Prochaine étape» nella
piega (sopra o accanto al rail); indice di navigazione in cima al piano di lavoro o nella barra; pré-évaluation
nell'inspector, stati vuoti in coda; ridurre titolo e riferimento su mobile; allineare le righe di stato del rail.

## 3. Direzione C — «Diplomazia contemporanea»

| PLATFORM UX | CREDIBILITÀ | COERENZA | COMPOSIZIONE | MOBILE | ACCESSIBILITÀ (tastiera) | Sopravvivenza contenuti |
|---|---|---|---|---|---|---|
| 8 | 8 | 9 | 7 | 8 | 7 | **FAIL** (un solo punto, riparabile con una riga) |

Contenuti: tutti i fatti della baseline presenti e verbatim; pré-évaluation completa con «Jeu de règles v1 · évaluée le
21.09.2026» a sigillo e disclaimer; nota legale nel rail di navigazione «Les décisions relèvent uniquement des autorités
compétentes. Cet espace vous oriente ; il ne décide jamais». **Ma** i responsabili per tappa (L'équipe du projet ×2,
Organisme de formation, L'autorité compétente ×2) sono inventati e **non marcati** come indicativi nel dashboard
(DIRECTION.md lo ammette, l'interfaccia no). Inoltre lo stato «Terminée» di 01 esiste solo come testo per screen reader:
01 (terminata) e 05 (a venire), entrambe «La personne — plein», sono **visivamente identiche** (`c_dashboard_desk_fold.png`,
`c_dashboard_mob_clip_rail.png`). Nessuna dicitura vietata.

Punti di forza: (1) è l'unica direzione in cui la prima schermata risponde alle cinque domande **sia a 1440 sia a 390**:
prossimo atto per primo, «Étape 2 sur 7», responsabile, 0/5, pré-évaluation nell'inspector; a 390 il prossimo atto è già
nella piega (`c_dashboard_desk_fold.png`, `c_dashboard_mob_fold.png`); (2) shell a tre regioni conforme al brief (barra ·
case band · rail di navigazione · piano di lavoro · inspector contestuale): l'unica con l'inspector; (3) rail 2.0 con
texture per responsabile dichiarate in legenda («plein / hachures / points / lignes»), `aria-current="step"`, marcatore
ad anello, modalità verticale pulita; (4) continuità sito → piattaforma la più forte: il disegno territoriale dell'hero
ritorna nella case band, stesso teal, stessa serif, stessi raggi; (5) case band densa ma ordinata: titolo, riferimento in
teal, quattro fatti in colonne con misuratore a tacche.

Difetti: (1) **nessuna frontiera MA → IT** nel rail: la giurisdizione, metà del nome del componente, è assente
(`c_dashboard_desk_fold.png`); (2) stato terminato invisibile (vedi sopra) — colore/texture codificano il responsabile,
non lo stato, e lo stato «a venire» non è attenuato; (3) colonna centrale ~640 px: sette segmenti con etichette a 12 px
che vanno a capo su 3–4 righe e checklist con righe di 4–5 righe di testo — il componente firma è quello più stretto
(`c_dashboard_desk_full.png`); (4) checklist `<table>` **senza caption** e con un solo `scope`; a 390 l'etichetta «ÉLÉMENT»
ripetuta in ogni scheda è rumore (`c_dashboard_mob_clip_check.png`); (5) menu account e lingua con `aria-expanded` che
non cambia con Enter (finti); il paragrafo intero della pré-évaluation in una colonna di 320 px è lungo da leggere.

Must-fix C: aggiungere la frontiera MA → IT (tra 05 e 06) e la didascalia «à titre indicatif»; distinguere lo stato
(pieno/anello/contorno) dal responsabile (texture) e mostrare la parola «Terminée»; dare al rail la larghezza del piano di
lavoro (sopra le due colonne) e alla checklist una colonna «élément» più larga; caption + `scope="col"`; cablare i menu.

## 4. Tastiera — sintesi comparativa (30 stop a 1440×900, 12 a 390×844)

| | A | B | C |
|---|---|---|---|
| Skip link primo stop | sì (#main) | sì (#main) | sì (#main-content) |
| `:focus-visible` su tutti gli stop | 30/30 | 24/24 poi ciclo | 24/24 poi ciclo |
| Anello | 2 px + alone 6 px, blu chiaro sul buio | 2 px + alone 6 px | 2 px teal + alone 5 px |
| Coperto da header sticky | mai | mai | mai |
| Ordine | barra → rail nav → breadcrumb → contenuto | barra → breadcrumb → indice (sotto la piega) → tabella → link | barra → breadcrumb → rail nav → link |
| Toggle da tastiera | rail: Enter/Space/Ctrl+B ok; account/lingua: morti | `<details>`: nativi, ok | account/lingua: morti |
| Rail 2.0 | non focalizzabile, stato nel testo, senza `aria-current` | `aria-current="step"` | `aria-current="step"` + sr-only |
| Mobile | 2 bottoni senza nome; striscia di tab scorrevole | gruppi con nome; chip a capo | tutti con nome; striscia di tab |

## 5. Home: quattro vie, processo, transizione sito → piattaforma

Quattro vie. A: «bus» dal nodo-hub col marchio a quattro schede R1–R4; focus e hover accendono stelo e nodo
(`a_home_desk_routes_focus.png`); a 390 bus verticale a sinistra — leggibile, ma restano quattro schede uguali. B: quattro
soglie a gradoni con ordinali 01–04 a 64 px in serif 200: la scala **suggerisce una sequenza** (prima persona, poi
impresa…) che non esiste, e l'ordinale domina il titolo in serif maiuscolo sottile (`b_home_desk_routes.png`); focus =
anello sull'intera scheda. C: griglia 7/5 · 5/7 con indice, etichetta mono, glifo-isoipsa, titolo serif in minuscolo,
scheda «En ce moment · Forum» con data (fatto datato, principio 15) (`c_home_desk_routes.png`); a 390 lista verticale
pulita. IA migliore: C (asimmetria senza gerarchia falsa), poi A, poi B.

Processo. A: onda con sei stazioni, responsabile con glifo **e territorio per tappa** (ITALIE · VÉNÉTIE / MAROC /
MAROC ↔ ITALIE…), striscia «Qui est responsable, tout au long de la ligne» con «Répartition indicative ; la plateforme
n'exerce aucune compétence administrative» (`a_home_desk_process.png`): il più onesto e completo; ma le stazioni seguono
l'onda e i titoli non sono allineati, e l'ultimo tratto verso INCLUSION resta punteggiato: si legge come «incerto».
B: figura appuntata + sei capitoli da 54 vh = 3 835 px per sei paragrafi brevi, senza territorio (`b_home_desk_process.png`).
C: «d'une rive à l'autre», giurisdizione resa dallo spazio (rive sud → rive nord), responsabili in mono, scheda del
progetto pilota con le otto tappe bloccate, mai presentata come canale autorizzato (`c_home_desk_process.png`); manca
la dicitura «indicative». In A e C compare «la plateforme» tra i responsabili (02): da riformulare in «la personne, avec
l'orientation de la plateforme» o da omettere. Nessuna delle tre dice «reconnaît les diplômes», «garanti» (solo negato) o
«art. 23»; il pilota non è mai «autorisé».

Transizione. Le tre barre di piattaforma condividono font, accento e raggi con la home. C è la più continua (territorio
nell'hero e nella case band); A è coerente (rete → glifo-porta negli stati vuoti); B è coerente in tipografia ma la home
usa serif maiuscolo sottile dove il dashboard usa sans 500. In tutte, l'ingresso all'Espace réservé dalla home è un link di
utility bar (A, C) o «Connexion» (B): nessuna mette l'accesso al fascicolo tra le quattro vie — corretto.

## 6. Ranking — metà piattaforma

1. **C** — l'unica prima schermata completa su desktop e mobile, lo shell a tre regioni con inspector, la continuità
   più forte; i difetti (frontiera assente, stato terminato invisibile, dicitura indicativa) sono locali al rail.
2. **A** — il rail 2.0 migliore (frontiera, texture+glifo+testo, «Vous êtes ici», verticale) e lo shell più efficiente
   da tastiera; penalizzata da tre alterazioni di contenuto e dall'assenza dell'inspector.
3. **B** — la più onesta nelle parole e la più solida in semantica, ma la piega senza prossimo atto, la navigazione
   sotto la piega e la frontiera sbagliata la rendono la meno usabile come piattaforma.

## 7. L'ibrido consigliato: shell di C + rail di A + strato di onestà di B

- **Shell di C**: barra 56 px · case band con i quattro fatti · rail di navigazione a sinistra con la nota legale ·
  piano di lavoro con «Prochaine étape» **per primo** · inspector destro con pré-évaluation (jeu de règles a sigillo),
  poi Messages e Dates vuoti; a 390 la stessa sequenza (fatti → nav → prossimo atto → rail → checklist).
- **Rail 2.0 di A**, ma a tutta larghezza del piano di lavoro (sopra le due colonne) per non comprimerlo nei 640 px di
  C: sette segmenti con texture+glifo+numero+parola di stato, «Vous êtes ici», **frontiera MA → IT tra 05 e 06**, legenda
  testuale, modalità verticale con la frontiera; etichette allineate su una baseline.
- **Strato di B**: «Étape n sur 7 · étape actuelle : …», parole TERMINÉE / ÉTAPE ACTUELLE / À VENIR con glifo,
  `aria-current="step"`, didascalia «Le responsable de chaque étape est indiqué à titre indicatif : les décisions relèvent
  uniquement des autorités compétentes», misuratore a cinque segmenti = conteggio, menu `<details>` nativi, tabella con
  caption/scope come regione focalizzabile.
- **Contenuti**: paragrafo della pré-évaluation verbatim (frase «Prochaines étapes…» compresa); niente «0 en retard»
  né «La plateforme» come responsabile; responsabili per tappa solo dal Rule Engine / `cases.services`, altrimenti omessi;
  la CTA del prossimo atto esiste solo se punta a una pagina reale.
- **Fascicolo** (da prototipare, nessuna direzione l'ha fatto): stessa shell, checklist con FONDEMENT, select + «Mettre à
  jour» sulle righe della persona, sezione Intervenants con la frase sull'accesso, modulo «Faire évoluer l'état».
- **Home**: quattro vie di C (con la scheda Forum datata) + processo di A (territorio per tappa e «répartition indicative»)
  sulla geometria a due rive di C, con titoli allineati e ultimo tratto pieno.
