# PAGE ARCHETYPES — le forme di pagina, prima delle pagine

Versione 1.0 · 21 settembre 2026 · Direzione artistica **A — «Le Registre»**

Un archetipo è una **forma di pagina definita dalla domanda a cui risponde**, non dal contenuto che
porta. Sono nove. Ogni pagina del progetto è un'istanza di uno di essi, e una pagina che non rientra
in nessuno è un segnale che manca un archetipo o che la pagina non ha una domanda propria.

Perché prima delle pagine: senza questo elenco, ogni nuova pagina viene disegnata da capo, e
quarantasette pagine disegnate da capo sono quarantasette dialetti.

---

## Indice

| # | Archetipo | Domanda | Istanze |
|---|---|---|---|
| 1 | **Plate** | Che cos'è questo progetto? | home |
| 2 | **Exposé** | Che cosa devo sapere su questo tema? | le projet, AGAMI, réseau, vivre en Italie |
| 3 | **Registre** | Quali sono le cose di questa specie? | parcours, actualités, glossaire, FAQ, partenaires |
| 4 | **Entrée** | Che cosa riguarda me, fra queste? | entreprises, institutions, universités |
| 5 | **Séquence** | Quali passi, in quale ordine, a carico di chi? | orientation, projet pilote, parcours de formation |
| 6 | **Formulaire** | Che cosa mi si chiede e che cosa ne sarà? | contact, besoins, collaboration, inscription |
| 7 | **Dossier** | Dove sono e che cosa devo fare? | tableau de bord, dossier, espace entreprise, sélection |
| 8 | **Constat** | Che cosa mi è stato detto, e su che base? | pré-évaluation, pièce, rapport annuel |
| 9 | **Acte** | Che cosa sto per cambiare, e con quale effetto? | ma situation, déposer une pièce, transition d'état |

---

## 1. Plate

**La domanda.** Che cos'è questo progetto, chi lo promuove, e perché dovrei continuare a leggere?

Una sola istanza: la home. La *plate* è un frontespizio, non un hero: nessuna fotografia a piena
larghezza dietro un testo bianco, nessun pulsante centrato, nessuna promessa.

- Titolo alla dimensione `plate`, la sola occorrenza nel progetto.
- Sotto il titolo, l'**autorità**: chi promuove, con quale natura giuridica.
- Nessuna chiamata all'azione prima che il lettore sappia che cosa gli si propone.
- Il verso della *plate* (`.plate--verso`) porta la barra di giurisdizione: chi fa che cosa, in
  segmenti tratteggiati proporzionati alla responsabilità.

## 2. Exposé

**La domanda.** Che cosa devo sapere su questo tema, in prosa, senza dovermi orientare?

Una colonna di prosa con misura limitata, intertitoli di rango B, e figure con apparato completo —
luogo, data, didascalia, credito. Nessuna figura senza apparato: una fotografia senza didascalia in
un contesto istituzionale è decorazione, e il progetto ne vieta l'uso.

Regola strutturale: **ogni figura ha luogo, data, didascalia e credito**, verificata da
`tests/compliance/test_figure_caption.py`.

## 3. Registre

**La domanda.** Quali sono le cose di questa specie, in quale ordine, e che cosa distingue ciascuna?

L'archetipo più usato, e la ragione del nome della direzione artistica.

```
01  Travail salarié                                 8 pièces demandées   ÉTAT
02  Carte bleue européenne                          3 pièces demandées   ÉTAT
```

Ordinale, titolo, glossa, attore/stato. Mai una griglia di card: una card dice «sono un modulo
software», una voce di registro dice «sono una cosa con una posizione, un titolo e un responsabile».

## 4. Entrée

**La domanda.** Fra questi pubblici, quale sono io, e che cosa mi riguarda?

Quattro ingressi — persona, impresa, istituzione, università — ciascuno con la propria
illustrazione originale in SVG e la propria destinazione. Erano quattro card; sono un registro con
un'illustrazione per voce.

Vincolo di griglia imparato sul campo: l'area denominata `actor` va dichiarata **a ogni larghezza**.
Un elemento di griglia assegnato a un'area non dichiarata finisce in una riga implicita, e una riga
di ingressi si è così allungata a 821 px su un telefono.

## 5. Séquence

**La domanda.** Quali passi, in quale ordine, a carico di chi, e dove mi trovo adesso?

Una sequenza verticale con ordinale a due cifre, un filo continuo, e un **attraversamento** visibile
dove la responsabilità passa dal paese d'origine all'Italia. La tappa corrente è marcata dal filo
più spesso e dal titolo in peso 600, mai da un colore soltanto.

Non è una barra di avanzamento. Non c'è percentuale.

## 6. Formulaire

**La domanda.** Che cosa mi si chiede, perché, e che cosa ne sarà?

- Ogni campo dice **che cosa legge quell'informazione**. Un campo il cui valore nessuno legge è un
  dato personale raccolto senza ragione.
- Il consenso è reso dal registro dei testi bloccati, mai ridigitato.
- Ciò che **non** si chiede è dichiarato: la pagina «Ma situation» elenca esplicitamente che non
  chiede numeri di documento, nomi di istituti, diplomi o nomi d'impresa.
- Se un gate chiude il form, la pagina dice **perché** e **da che cosa dipende**, non «indisponibile».

## 7. Dossier

**La domanda.** Dove sono, che cosa devo fare, chi è responsabile, che cosa succede dopo?

Le quattro domande di accettazione del committente, in quest'ordine. Struttura:

1. intestazione del fascicolo (contesto stabile)
2. azione successiva (**una**)
3. percorso come sequenza
4. i registri del dominio, in ordine di utilità

La pagina non decide nulla e non mostra percentuali.

## 8. Constat

**La domanda.** Che cosa mi è stato detto, su quale base, e posso verificarlo?

L'archetipo che distingue un orientamento da un oracolo. Tre blocchi, in quest'ordine, perché è
l'ordine in cui un lettore costruisce fiducia:

1. **l'esito**, come parola, mai come decisione — e non esiste «eleggibile»;
2. **le regole** che l'hanno prodotto, ciascuna con identificativo e versione;
3. **le fonti** su cui quelle regole poggiano, numerate, con riferimento puntuale e data di
   consultazione quando c'è.

Un elenco di fonti vuoto è **dichiarato**, non nascosto: un esito che non può citare nulla resta un
esito onesto; uno che non mostra fonti invita il lettore a supporre che esistano.

Il *constat* porta anche la **riproducibilità**: se lo snapshot congelato, rieseguito, dà un esito
diverso da quello registrato, la pagina lo dice — è uno scarto che la persona ha diritto di conoscere
prima di agire.

## 9. Acte

**La domanda.** Che cosa sto per cambiare, chi può cambiarlo, e con quale effetto?

- Non viene mai offerto un controllo che il dominio rifiuterebbe: l'elenco delle transizioni è
  calcolato dalla tabella dichiarata e filtrato dalla policy sull'oggetto.
- La policy viene interrogata **di nuovo** al POST: un controllo nascosto non è una porta chiusa.
- Ciò che l'atto comporta è scritto **prima** del pulsante. «Enregistrer et recalculer» dice che cosa
  fa; «Enregistrer» non lo direbbe.
- Ogni atto lascia una traccia di audit, e la pagina lo dice quando la traccia è visibile ad altri.

---

## Regole comuni a tutti gli archetipi

| Regola | Verifica |
|---|---|
| Esattamente un `h1` per pagina | `scripts/qa_rtl_check.py`, test di pagina |
| Nessuno scorrimento orizzontale a 390 px | idem, a due viewport |
| Nessuna percentuale, nessun contatore animato | revisione + assenza di componente |
| Ogni stato è una parola + un filo, mai il colore da solo | `register.css`, `@media (forced-colors)` |
| Ogni regione vuota è un filo e una frase che nomina chi la riempie | revisione |
| Ogni stringa passa dal catalogo di traduzione | `test_ui_strings_are_wrapped_for_translation` |
| Nessun testo prescritto ridigitato | `scripts/i18n_audit.py` (rilevamento di frammenti bloccati) |
| Nessun dato finto per popolare una schermata | `core.seeds.demonstration_data_allowed()` |

---

## Come si aggiunge una pagina

1. Individuare l'archetipo dalla **domanda**, non dal contenuto.
2. Se nessuno corrisponde, fermarsi: o manca un archetipo — e va discusso — o la pagina non ha una
   domanda propria e appartiene a un'altra.
3. Riusare le componenti dell'archetipo. Non aggiungere CSS: in sedici pagine di piattaforma è stata
   aggiunta **una** regola nuova (`.table-region`), e perché WCAG la richiedeva.
4. Verificare a 390 px e in arabo prima di considerarla finita.
