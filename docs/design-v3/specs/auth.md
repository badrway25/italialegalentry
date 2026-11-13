# V3 — AUTENTICAZIONE («l'atrio»)

Superficie: login, iscrizione, reimpostazione password, conferma e-mail, MFA/TOTP, codici di recupero, riautenticazione.
Direttiva §84 (continuità sito → portale) e §85. Vincolanti: `DESIGN_SYSTEM_V2.md`, `MOTION_SYSTEM.md`, `BRAND_ASSETS.md` §1–2, `ANTI_PATTERNS.md`.

**Round 2 — riparazione dopo `docs/design-v3/reviews/auth.md`.** Il revisore ha dichiarato il round 1 non conforme e non
implementabile. Ogni VIOLAZIONE è rimossa o trasformata in un emendamento numerato al §0; ogni MUST-FIX è **FATTO** o
**CONTESTATO con la misura che lo prova**; ogni LACUNA è chiusa con il CSS, i selettori, il markup e i numeri; ogni segnale
«a buon mercato» è tolto o difeso. **Nessuna cifra qui è riportata dal round 1: tutte sono state ricalcolate o rimisurate.**

Prove prodotte per questa revisione — Chromium headless di Playwright lanciato da questa sessione (mai la porta 9222),
pagine reali di `:8771` copiate e ridipinte con il foglio candidato via `page.route()`, quindi stesso origin, stessi font,
stesso `main.css`. Viewport misurate: 1440×900 · 1280×800 · 1200×800 · 1199×800 · 1024×768 · 900×1200 · 768×1024 ·
767×900 · 390×844 · 360×740. Stati misurati: riposo, fuoco, `prefers-reduced-motion: reduce`, `forced-colors: active`,
`dir="rtl"`, zoom 200 % e 400 %. In
`…\scratchpad\auth2\`: `auth.css`, `auth.js`, `threshold.svg.html`, `measure.py`, `probe.py`, `measures.json`,
`probe.json`, `focus2.py`, `jstest.py`, `chart2.py`, `contrast.py`, `shot_1440.png`, `shot_rtl.png`, `shot_forced.png`,
`shot_otp.png`, `shot_js.png`, `login_{1440,1024,768,390}.png`, `signup_{1440,768,390}.png`.

---

## 0. RICHIESTE DI EMENDAMENTO

Cinque, tutte esplicite. Finché non sono accolte, il §0 è la sola deroga dichiarata di questo documento: **tutto il resto
sta dentro `DESIGN_SYSTEM_V2.md` e `MOTION_SYSTEM.md` senza deroghe.**

### EMENDAMENTO 1 — `MOTION_SYSTEM.md` §2, famiglia FOCUS: «alone 3 px al 30 %» → «alone 5 px al 30 %»

**Clausola.** `MOTION_SYSTEM.md` §2, riga FOCUS, colonna «Che cosa muove»: «anello 2 px + alone 3 px al 30 %».
**Conflitto.** `DESIGN_SYSTEM_V2.md` §2 livello 4 prescrive «anello 2 px `--accent-ring` + alone **5 px** al 30 %». I due
documenti vincolanti dicono due numeri diversi per lo stesso oggetto. Il round 1 ha scelto 5 senza dichiararlo: è la
LACUNA 13 del revisore, ed è un difetto.
**Richiesta.** Allineare MOTION_SYSTEM a 5 px. La misura dell'alone è una questione di superficie, e le superfici sono il
dominio di `DESIGN_SYSTEM_V2` §2; MOTION_SYSTEM è normativo sul *tempo*, non sulla geometria del livello 4.
**Costo.** Nessuno visivo: la sporgenza totale dell'anello resta quella misurata qui, **5 px** (§6.2). Cambia un numero in
una riga di `MOTION_SYSTEM.md` §2.
**Se respinto.** Si porta l'alone a 3 px in `auth.css` e si emenda invece `DESIGN_SYSTEM_V2` §2; la sporgenza scende a
4 px e tutte le tolleranze di §6.2 migliorano. Il documento non può restare con due numeri.

### EMENDAMENTO 2 — `DESIGN_SYSTEM_V2.md` §8.8, ultima frase: togliere «con la barra della piattaforma che scende in scena»

**Clausola.** «Transizione sito → portale: crossfade 320 ms con la barra della piattaforma che scende in scena.»
**Richiesta.** Cancellare «con la barra della piattaforma che scende in scena»; il crossfade di pagina migra a
`transitions.md` / `platform-shell.md`, che possiedono `@view-transition`.
**Ragione.** Due, entrambe verificabili. (a) Su questa superficie la barra **non entra**: l'atrio rende `.portal-bar`,
l'elemento del portale, con il foglio del portale, *prima* dell'accesso (§4.2). Animare l'ingresso di un elemento che non
cambia è moto senza funzione, cioè la regola 0 di MOTION_SYSTEM. (b) Una View Transition fra documenti richiede
`@view-transition { navigation: auto }` nel CSS del documento di partenza **e** di quello d'arrivo: il documento
d'arrivo è il portale, il cui foglio è `apps/portal/static/portal/portal.css`, che questa specifica non tocca
(MUST-FIX 6). Dichiararla solo qui produrrebbe una transizione che non scatta mai — una riga di specifica non
verificabile, che è esattamente ciò che il revisore chiama «aspirazionale».
**Costo.** Il momento dell'accesso non ha un gesto di pagina finché `transitions.md` non atterra. In cambio la continuità
§84 non è più affidata a un'animazione ma all'**identità dell'elemento**, che è più forte e si prova con un test statico
(§9).

### EMENDAMENTO 3 — `DESIGN_SYSTEM_V2.md` §8.8: il lock-up sta nella barra, non nel foglio

**Clausola.** «…a destra il foglio del modulo su `--min-2` **con lock-up**, campi a 48 px, errori inline, lingue.»
**Richiesta.** Il lock-up sta nella barra d'atrio; il foglio si apre sull'eyebrow.
**Ragione.** La barra dell'atrio **è** `.portal-bar` e `.portal-bar` porta già il marchio
(`templates/partials/portal_chrome.html`, riga 18–20). Un lock-up nel foglio sarebbe il marchio due volte sullo stesso
schermo, a 71 px di distanza — e `BRAND_ASSETS.md` §1 chiede che il marchio sia un oggetto, non un motivo.
**Costo.** Il marchio è 71 px più in alto del punto prescritto. Misurato: resta sopra la piega a **tutte** le viewport
della matrice, la più corta essendo 360×740 (barra a `y = 0`, altezza 123 px).

### EMENDAMENTO 4 — `DESIGN_SYSTEM_V2.md` §11: la carta dell'atrio non si specchia in RTL

**Clausola.** «`[dir="rtl"]` specchia gli SVG decorativi (`scaleX(-1)`) e le frecce, non il lock-up, il titolo bloccato,
i numeri, la chiave, la fotografia.» Precedente: `v2/hero.css:567` specchia `.hero__territory`.
**Richiesta.** Aggiungere alla lista dei **non** specchiati: «una carta proiettata con coordinate reali».
**Ragione.** La soglia dell'atrio non è una texture: è un foglio Mercator con due luoghi nominati e le loro coordinate
(§4.3). Specchiarlo mette il Marocco a est del Veneto. Le isoipse dell'hero sono un campo astratto e si specchiano
legittimamente; una carta no — è più vicina a «i numeri», che §11 già esclude.
**Costo.** In arabo la rotta corre verso il bordo esterno invece che verso il foglio. L'arrivo resta segnato dal filetto
`--accent` di 3 px sul bordo iniziale del foglio, che **si** specchia (misurato: `border-left 0px / border-right 3px` in
`dir="rtl"`, `probe.json/rtl`). Quel filetto è il gesto di §9.2, non la rotta.

### EMENDAMENTO 5 — `DESIGN_SYSTEM_V2.md` §7, riga RICH: esplicitare il loop ambientale (chiarimento, non deroga)

**Clausola.** §7, riga RICH — «Ammesso: un capitolo mezzanotte, reveal editoriali, grafici con dati reali. Vietato:
isoipse, marea.»
**Richiesta.** Aggiungere in «Ammesso»: «**un** loop ambientale ≥ 20 s che non sia la marea, oppure **un** oggetto
indicizzato allo scroll — mai entrambi».
**Perché è un chiarimento e non una deroga.** `MOTION_SYSTEM.md` §4 già concede alle pagine RICH «al massimo uno dei due»
fra il loop ambientale e l'oggetto legato allo scroll; §7 vieta per nome le **isoipse** e la **marea**, non la categoria.
L'oggetto ambientale dell'atrio (§5, AMB) non è la marea — non muove strati di isoipse, muove un marcatore di 3,5 unità
lungo la rotta — e l'atrio non spende l'altro dei due (non c'è nulla legato allo scroll). La colonna «Ammesso» di §7 non
è esaustiva altrove (per STANDARD dice solo «reveal 240 ms»), quindi l'argomento regge; lo si scrive perché **il prossimo
revisore non debba ricostruirlo**.
**Costo.** Nessuno. Se respinto, l'atrio resta senza oggetto vivo e il MUST-FIX 11 si chiude sulla sola seconda
alternativa offerta dal revisore (la graticola non uniforme, §4.3), che è comunque realizzata.

---

## 1. RISPOSTA PUNTO PER PUNTO ALLA REVISIONE

### 1.1 Violazioni

| # | Violazione | Esito |
|---|---|---|
| 1 | Testo bloccato antifrode + gate di pubblicazione sostituiti da «attention aux fraudes» | **RIMOSSA.** `_atrium_footer.html` (§7.3) rende `{% if gates.phase3_public %}{% safe_url 'pages:antifraud' %}{% locked "p3.antifraud.title" %}` verbatim. Nessuna parola francese inventata. A Fase 3 chiusa (:8770) il link non si rende, come nel piè di pagina pubblico |
| 2 | Consenso senza i documenti che nomina | **RIMOSSA.** Il piè di pagina d'atrio porta **tutti e cinque** i link legali del piè pubblico + promotore + © + etichetta di versione + data di verifica. Non si perde nulla: l'elenco è enumerato al §7.3 e confrontato riga per riga con `templates/partials/footer.html` |
| 3 | `--brand-gold` su `--brand-navy` (regola 4) | **RIMOSSA.** La chiave è cancellata. La riga di token è cancellata. Nessun `--brand-*` compare in `auth.css`: `grep -cE "var\(--brand-" auth.css` = **0**, verificato |
| 4 | La porta intera fuori dall'hero | **RIMOSSA.** Senza chiave restano arco e gradini, che §6 ammette esplicitamente nella piattaforma: «glifo arco+gradini». `BRAND_ASSETS.md` §1 enumera quattro parti (piani tricolore, arco, chiave, gradini): due su quattro, senza la chiave e senza i piani, non sono «la porta intera» |
| 5 | Stagger 90 ms, `delay .35`, 600 ms senza token | **RIMOSSE tutte e tre.** Stagger **50 ms** (banda 40–60 di MOTION_SYSTEM §1); A2 è **concatenata** ad A1 con `trace.finished.then(...)`, quindi nessun ritardo è un numero; A11 non esiste più. In `auth.js` i soli numeri temporali sono `0.9` (`--motion-draw`), `0.24` (`--motion-base`), `0.05` (stagger) e `0.4` s per il throttle di `aria-live` (che non è un'animazione: è la cadenza di un annuncio, vedi §6.4) |
| 6 | `step`/`steps` passati a un partial che nessuna vista alimenta | **RIMOSSA.** Nessun elemento di avanzamento, su nessuna delle dodici schermate. `_threshold.html` non riceve nessun contesto. La garanzia «nessuna vista, nessun contratto di dati» è ora vera e verificabile: l'unico file Python toccato è `apps/accounts/forms.py`, per **un attributo di widget**, dichiarato al §7 |

### 1.2 MUST-FIX

| # | Esito | Dove |
|---|---|---|
| 1 | **FATTO** — testo bloccato + gate verbatim, elenco legale esplicito e completo, nulla di tacitamente eliminato | §7.3 |
| 2 | **FATTO** — `components/form_field.html` **non è toccato**. I ganci sono selettori d'attributo (`[type="password"]`, `[name="password1"]`, `[autocomplete="one-time-code"]`) e i tre elementi aggiuntivi li crea `auth.js`, che è anche l'unica cosa che li fa funzionare | §4.5, §5, §7 |
| 3 | **FATTO** — `step`/`steps` e «Étape 2 sur 3» cancellati; nessun partial riceve contesto e nessun elemento di avanzamento esiste su nessuna delle dodici schermate | §1.4, §7.2 |
| 4 | **FATTO** — chiave, A11 e la riga `--brand-gold` cancellate | §4.2, §5 |
| 5 | **FATTO** — si sovrascrive `{% block main_content %}` in `allauth/layouts/entrance.html`; `{% block account_help %}` non viene perso ma **ri-reso con lo stesso testo e lo stesso `mailto:`** dentro il foglio; il gancio `data-mode` è un nuovo `{% block body_data %}` in `templates/base.html`, con il diff esatto | §7.1, §7.2 |
| 6 | **FATTO, in modo diverso da come è richiesto, e con le misure che lo giustificano** — `portal.css` non viene modificato affatto. `--entrance-bar-h` è cancellato: era una finzione. Vedi §1.3, disputa D1 | §4.2, §1.3 |
| 7 | **FATTO, con la fascia ridefinita** — lo split non collassa a 768 ma a **1024**, e la misura che lo impone è scritta. Padding inline minimo, sporgenza del fuoco e scorrimento del foglio: tutti misurati. Il foglio **non ha scorrimento proprio a nessuna larghezza** | §4.8, §6.2, appendice C |
| 8 | **FATTO** — regola `:-webkit-autofill` / `:autofill` scritta, con la variante al fuoco che compone i due `box-shadow` | §4.5 |
| 9 | **FATTO** — `<select>` di `account_type` specificato: 48 px, `appearance: none`, chevron, sei stati, comportamento RTL | §4.5 |
| 10 | **FATTO** — numeri di moto corretti; la proprietà di `scroll-padding` è risolta **eliminandone il bisogno** (la barra d'atrio non è appiccicata) e i bersagli portano `scroll-margin-block-start` | §5, §6.3 |
| 11 | **FATTO, e per intero: entrambe le alternative offerte dal revisore, non una** — graticola cartografica non uniforme (Mercator reale) **e** un oggetto ambientale, con la prova di costo. Le coordinate sono etichettate riusando il componente `.coord` dell'hero. Il blocco fiducia e i glifi sono cancellati | §4.3, §5 |
| 12 | **FATTO** — `cms.forbidden.scan()` eseguito sulle tre pagine prototipo renderizzate: **0 violazioni**. La nota HUMAN_QA è estesa | §6.6 |

### 1.3 Contestazioni — con la misura che le prova

**D1 — «`.portal-bar` non è 56 px».** Il revisore ha ragione, e il round 1 aveva torto; ma ha torto anche la sua
implicita richiesta («un test di frontend confronta l'altezza calcolata delle due barre»), e questo va detto con i numeri.

Misurato in Chromium headless, `.portal-bar` con `portal.css` reale, `getBoundingClientRect()` border-box:

| Barra | 1440 | 1024 | 390 | 360 | 320 |
|---|---:|---:|---:|---:|---:|
| **atrio** (marchio · «Site public» · lingue) | **71** | **71** | **71** | **123** (va a capo) | — |
| **portale** (marchio · contesto · menu conto · «Site public» · lingue) | **71** | **71** | **175** (va a capo) | — | **211** (va a capo) |

Border-box; content-box = border-box − 2 (il bordo inferiore `2px solid var(--rubric-on-navy)`, che **è** riprodotto
perché è la stessa regola). `padding: 12px 40px` a desktop, `12px 20px` sotto 768. `probe.json/bar_atrium_*`,
`probe.json/bar_portal_*`.

Conclusione: **le due barre non possono essere uguali in altezza, perché non portano lo stesso contenuto** — il portale
ha il contesto del fascicolo e il menu del conto, l'atrio no (non c'è ancora una sessione). Un test che confronta due
altezze fallirebbe a 390 px il giorno in cui viene scritto. Il token `--entrance-bar-h` è quindi **cancellato**, e con
esso la necessità di riscrivere `portal.css`. La continuità §84 non si ottiene con un numero condiviso ma con
**l'identità dell'elemento**: l'atrio rende `partials/portal_chrome.html` ridotto e carica
`apps/portal/static/portal/portal.css`, esattamente come fanno già `templates/portal/base_portal.html` riga 20 e
`templates/helpdesk/base_helpdesk.html` riga 11. La guardia che sostituisce il test d'altezza è statica e vera per
costruzione (§9). Coordinamento con `platform-shell.md`: **zero modifiche a `portal.css`**; l'unica dichiarazione
dell'atrio sulla barra vive in `auth.css` ed è `.page-atrium .portal-bar { position: static }` (§4.2).

**D2 — «un anello di fuoco che sporge di 9 px».** Contestato. Il revisore somma 2 (offset) + 2 (tratto) + 5 (alone) = 9.
I due non si sommano: l'alone è uno `spread` misurato **dal border-box**, l'anello ha il bordo esterno a offset + tratto,
anch'esso dal border-box. La sporgenza è il massimo, non la somma.

Misurato (`focus2.py`, fuoco da tastiera, dopo 500 ms perché la transizione di `components.css` sia conclusa —
letta prima si ottiene il valore interpolato `rgba(0,0,0,0) 0 0 0 0`, che è l'errore in cui si cade leggendo subito):
`outline-width 2px`, `outline-offset 2px`, `box-shadow rgba(29,138,147,0.3) 0 0 0 **5px**`.
→ bordo esterno dell'anello **4 px**, alone **5 px**, **sporgenza = 5 px** a 1440, 768, 390 e 360.

Spazio disponibile fra il campo e il bordo del foglio, misurato: **116,7 px** a 1440 · **103 px** a 1024 · **35 px** a
768 · **16 px** a 390 e 360. Margine minimo residuo: **11 px**. E il problema è comunque estinto alla radice, perché
`contain: paint` **non è più sul foglio** (§4.4): il foglio non ha nulla da contenere.

**D3 — «`ACCOUNT_RATE_LIMITS["login_failed"] = "5/5m"`».** Il revisore ha ragione: `config/settings/base.py:192` dice
`"5/5m/ip,5/5m/key"`. Il blocco fiducia che citava quella riga è cancellato (§1.4); la citazione sopravvive solo nello
stato «limite di tentativi» del §4.7, **nella forma esatta**.

**D4 — «il rapporto 5,88:1 del campo disabilitato».** Ricalcolato: 5,88:1 è `--ink-3` su `--min-2`. Il campo
disabilitato ha fondo `--min-1`, e lì `--ink-3` misura **5,14:1**. Passa AA lo stesso, ma la cifra del round 1 era
sbagliata e va corretta (§4.2).

### 1.4 Segnali «a buon mercato»

| # | Segnale | Esito |
|---|---|---|
| 1 | «Il layout è il default»: pannello scuro a sinistra, foglio a destra | **DIFESO E RICOSTRUITO.** §1.5 |
| 2 | Fondo piatto `--mid-1` + griglia 160 px + un tracciato che poi sta fermo per sempre | **RIMOSSO.** La graticola è una proiezione di Mercator reale, quindi **non uniforme**; l'arco è un'**apertura con una superficie propria** (`--mid-2`), non un contorno; e c'è un oggetto ambientale. §4.3 |
| 3 | Tre fatti di sicurezza con glifi (il blocco «badge SOC2» di `ANTI_PATTERNS` §1) | **CANCELLATO.** Nessun fatto di sicurezza sulla soglia, nessun glifo di fiducia, nessuna promessa |
| 4 | Coordinate decorative senza etichetta | **CANCELLATE come texture, RESTITUITE come legenda.** Si riusa `.coord` / `.coord__dot` di `v2/hero.css:415-436`, che rende già `Maroc 33.97° N · 6.85° W` e `Vénétie 45.41° N · 11.88° E` in `templates/pages/home/_hero.html:72,78`. Non sono un ornamento nuovo: sono il componente già in produzione, e ora nominano i due luoghi che la carta disegna |
| 5 | Misuratore di robustezza a quattro tacche | **CANCELLATO.** Al suo posto **l'unico fatto che un browser può provare**: la lunghezza. §4.5 |
| 6 | «Étape 2 sur 3» su una schermata di login | **CANCELLATO** |
| 7 | Rettangolo teal piatto a tutta larghezza come azione primaria | **DIFESO, e non più solo.** §1.6 |
| 8 | Il momento memorabile speso dove non c'è quasi nessuno | **SPOSTATO.** La chiave (tre schermate terminali a basso traffico) è cancellata; il tracciato dell'arco e l'oggetto ambientale stanno sulla schermata di login, che è quella che il committente apre |

### 1.5 Il layout non è più «login-03 con un arco» — e questa è la prova

Il test del revisore è giusto e va superato letteralmente: **coprire l'arco.** Quel che resta, a 1440×900, misurato:

1. **una carta**, non un fondo. Graticola di Mercator fra 30° e 49° N: i meridiani sono equidistanti (133,3 unità), i
   paralleli **no** — 86,2 unità fra 32 e 34° N, 106,0 fra 46 e 48° N, cioè un passo che cresce del **23 %** salendo
   verso nord. È la proprietà che definisce la proiezione, calcolata (`chart2.py`), non stilizzata. Una griglia regolare
   di 160 px non lo fa, e il revisore ha ragione a chiamarla «il fondo tecnico più economico possibile».
2. **una rotta con due estremi nominati**: un segmento retto da `(137,3 · 730,7)` a `(636,8 · 191,1)` in unità di
   tavola. Su Mercator una retta è una **lossodromia**, cioè la rotta a rotta costante: 51,4° di rilevamento, calcolato.
   I due estremi sono il Marocco e il Veneto, con le coordinate che il sito già pubblica.
3. **la legenda della tavola** in mono: `PROJECTION DE MERCATOR · 30°–49° N · 12° O – 18° E`, e i due punti con il loro
   pallino `--accent-dark`.
4. **il filetto `--accent` di 3 px** sul bordo iniziale del foglio — il gesto di §9.2 («Prochaine étape»: bordo iniziale
   `--accent` 3 px), che qui dice: *l'azione è di qua*.

Nessuno dei quattro appartiene a login-03, a sign-in-6, ad auth-section-2 o ad auth-section-3.

E quando l'arco si scopre, non è un ornamento sopra il fondo: è **un'apertura nel fondo**. La stessa graticola è
ridisegnata dentro la sagoma dell'arco, più chiara (`--terr-line` a .55 contro `--on-dark` a .09), su una superficie
propria `--mid-2` (§2 livello 1 del capitolo scuro). La rotta è disegnata **sotto** la tavola, quindi entra dietro lo
stipite iniziale a `t = 0,222` e riemerge oltre la volta a `t = 0,701` — che è testualmente ciò che `DESIGN_SYSTEM_V2`
§8.3 prescrive per la rotta («entra dietro la soglia della porta e riemerge oltre la volta»), qui per la prima volta
realizzato. Coprire l'arco toglie la composizione; scoprirlo dice che cos'è la porta: **il punto in cui il percorso
passa.**

### 1.6 Il bottone: perché a tutta larghezza, e perché non è più un rettangolo muto

Il revisore ha ragione su un punto e mezzo: il round 1 asseriva «l'unico posto dove è giusto» senza argomentare, e la
linea d'ormeggio di 16 px era invisibile nello screenshot che il committente guarda. Argomento e correzione:

- **A tutta larghezza perché la colonna è un modulo, non una scheda.** La misura del foglio è 432 px (27rem, misurati:
  `inner.w = 432` da 1200 a 1440, `sheetScrolls = false`). I campi sono larghi 432. Un bottone di 180 px sotto due campi
  di 432 legge come una nota a piè di modulo; a 432 legge come la conclusione della colonna. È la stessa ragione per cui
  §10 dà ai campi la larghezza piena e non ai bottoni **altrove**: altrove il bottone sta in una riga con altri; qui
  non c'è nessun altro. Sull'atrio c'è **una** azione per schermata, ed è l'unica ragione per cui la pagina esiste.
- **Non è più muto a riposo.** Il bottone porta a riposo l'etichetta **e la freccia** `icon--flip-rtl` già in sistema
  (`.btn--arrow` dell'hero), quindi nello screenshot è un'azione con una direzione. La linea d'ormeggio di §8.5
  (`.btn__rule`, 16 × 1 px, `transform: scaleX(0→1)`, origine logica via `--dir`) si traccia **fra** l'etichetta e la
  freccia in hover e in `:focus-visible`: è la firma, e resta un premio per chi interagisce, non un ornamento fisso.
- **E non è l'unico oggetto d'accento a riposo.** Il filetto `--accent` di 3 px sul bordo del foglio e il blocco
  `--accent` del bottone stanno sullo stesso asse verticale e leggono come una cosa sola: un bordo e un blocco dello
  stesso colore, a 116,7 px di distanza misurati. Quello è il colore interattivo, e non ce n'è un altro in pagina.

### 1.7 Due difetti che la revisione non ha trovato, e che questa riparazione corregge

**N1 — il namespace `.entrance` è già occupato.** `static/css/components.css:1390` definisce `.entrance` per il
componente «quattro ingressi» della home: `display: flex; flex-direction: column; gap: var(--space-4); padding:
var(--space-8) var(--space-6) var(--space-10); border-block-end: …`, con `.entrance__num`, `.entrance__icon`,
`.entrance__title`, `.entrance__text`, `.entrance__cta`, `.entrances`. Il round 1 proponeva `.entrance`,
`.entrance__threshold`, `.entrance__sheet`, `.entrance-bar`. **Verificato nel browser prima di accorgermene a
leggere**: il prototipo con `.entrance` ereditava `column-gap: 16px` e `padding: 32px 0 48px` dal componente della home,
e il divario di 16 px fra le due colonne era visibile nella prima misurazione (`diag.py`). Tutto il namespace è
rinominato **`.atrium`** — il nome che la specifica già usa in italiano. Verificato libero:
`grep -rho "\.atrium[a-zA-Z0-9_-]*" static/ apps/*/static/` → nessun risultato. Idem per `.threshold`, `.sheet__*`,
`.arch__*`, `.grat__*`, `.route__*`, `.atrium-footer`.

**N2 — la casella di consenso è dipinta con il navy del marchio.** `components.css:2272` dichiara
`accent-color: var(--color-primary-900)`; `_legacy-tokens.css:49` la punta su `--navy`; `v2/bridge.css:31` punta
`--navy` su `--brand-navy` `#0F2547`. È **lo stesso difetto** che `static/css/v3/buttons.css` ha corretto per
`.btn--primary` — regola 1 (un solo accento interattivo) e regola 4 (il tricolore vive solo nel marchio) — e vive sul
controllo che registra un consenso GDPR (`accept_terms`, `apps/accounts/forms.py:31`). Corretto qui, **scoped a
`.atrium`**: `accent-color: var(--accent)`. Il caso globale (ogni checkbox del prodotto) non appartiene a una specifica
d'autenticazione: va segnalato alla superficie dei moduli, come `buttons.css` ha fatto per i bottoni.

---

## 2. UI-UX-PRO-MAX — interrogazioni e verdetti

Invariato rispetto al round 1: il revisore non l'ha contestato. Si aggiornano due righe che il round 2 modifica.

| # | Query (verbatim) · dominio | Risposta (condensata) | Esito |
|---|---|---|---|
| 1 | `login sign-in screen split layout form UX` · ux | Etichette associate; gerarchia dei titoli; HTML semantico | **ACCETTATO** — conferma il contratto etichetta-visibile già in `form_field.html`. Nessuna opinione sul layout |
| 2 | `form validation inline error messaging password field` · ux | «Focusable Error Summary»: sommario in testa, fuoco dopo il submit fallito, link a ogni campo, inline conservati; più «validate on blur» | **ACCETTATO** per il sommario. **RESPINTO** il blur |
| 3 | `government portal authentication trust security` · product | «Accessible & Ethical + Swiss minimalism», «Professional blue», «Minimal & Direct» | **RESPINTO**: è il registro rifiutato dal committente, e «professional blue» è un secondo accento |
| 4 | `entrance animation stagger form reveal reduced motion` · gsap | Stagger 250–350 ms, 0,02–0,04 s per elemento, `matchMedia` → stato finale | **ACCETTATO, riportato ai token**: 240 ms `--motion-base`, stagger **50 ms** su ≤ 6 nodi, `--ease-out`. **RESPINTO** lo shimmer |
| 5 | `dark panel split screen contrast accessible` · color | Palette di catalogo (kiosk `#020617`, studio `#18181B`) | **RESPINTO**: `--mid-1` `#0E1B23` con i rapporti ricalcolati al §4.2 |
| 6 | `touch target size button minimum 24px WCAG 2.2` · ux | AA = 24 CSS px o eccezione; 44 pt iOS e 48 dp Android sono altra cosa | **ACCETTATO** — base del §6.1 |
| 7 | `one-time code input autocomplete otp two factor` · ux | Nessun risultato pertinente | **VUOTO**. Il pattern OTP è deciso al §4.7 sulle specifiche HTML e **misurato** |
| 8 | `RTL arabic bidirectional layout logical properties` · typography | Noto Naskh + Noto Sans Arabic dal CDN di Google | **RESPINTO nella consegna** (CDN = violazione CSP, e quel dominio è in `cms.forbidden`); **ACCETTATO nella scelta**: Noto Naskh è già la nostra voce araba, self-hosted |
| 9 | `institutional premium editorial authoritative interface style` · style | Skeuomorfismo, Editorial Grid, Anti-Polish Raw | **RESPINTO**: per lo strumento «premium» è texture e ombre. Per noi è **scala, superficie e tempo** |

Bilancio: **4 accettate, 4 respinte, 1 vuota.**

---

## 3. 21ST.DEV — confronto dei candidati

Invariato tranne dove il round 2 cambia la decisione. Nulla viene installato: React, Tailwind, shadcn e `motion/react`
non entrano.

| # | Componente | Che cosa prendo — round 2 |
|---|---|---|
| 1 | **Split Login** · `@hirael/login-03` | L'ossatura (aside/foglio, cascata per indice, attesa annunciata, chevron speculato in RTL). **Respinti** i 36 path infiniti e i blob radiali |
| 2 | **Auth Section 2** · `@solaceui/auth-section-2` | **NULLA.** Il round 1 ne prendeva «il lato scuro porta contenuto» e lo traduceva in tre fatti di sicurezza con glifi: è il blocco che `ANTI_PATTERNS.md` §1 nomina. Il lato scuro dell'atrio porta **una carta**, che è un disegno, non un elenco di promesse |
| 3 | **Sign In Split Screen** · `@felipemenezes098/sign-in-6` | Solo la conferma della proporzione; a 1440 misuriamo 777,6 / 662,4 = **54,0 / 46,0** |
| 4 | **Auth Section 3** · `@solaceui/auth-section-3` | Il consenso come campo di prima classe — vale per `accept_terms`, reso come pannello `--min-1` con bordo `--hairline-strong` (3,14:1 su `--min-1`) |
| 5 | **Login** · `@lavikatiyar/login` | La parametrizzazione: **un** partial `_threshold.html` riusato dalle dodici schermate, senza contesto |
| 6 | **OTP Input** · `@ddoemonn/otp-input` | La **grammatica a celle come disegno**, non come DOM. Ora è misurata: cella = 1,2 em = **26,4 px** a 22 px, avanzamento del glifo di Fira Mono = **0,6 em esatti** (misurato, `probe2.py`), quindi le cifre cadono al centro delle celle. **Respinti** il blur, la scossa d'errore e il cursore in loop |
| 7 | **OTP Verification Field** · `@cnippet-dev/v-field-20` | La struttura etichetta + descrizione + errore — già il nostro `form_field.html`, non toccato |
| 8 | **Login Page 1** · `@shadcnstore/login-page-1` | **RESPINTO nel round 2.** «Forgot password» sulla riga dell'etichetta richiede di spostare nel DOM un elemento che allauth rende come `help_text` del campo password (`PasswordField(show_reset_help=True)`, `allauth/account/forms.py:60`): visivamente sopra il controllo, nel DOM dopo — cioè l'ordine di tabulazione salterebbe all'indietro (WCAG 2.4.3). Il punto 2.5.8 si risolve invece **per geometria**: §6.1 |

---

## 4. LA PROPOSTA — «l'atrio»

Una **soglia**, non un modulo su una pagina. Chi arriva è già dentro la geometria del portale: l'entrata porta la barra
del portale, non l'header pubblico. Accedere non cambia prodotto, accende una luce.

### 4.1 Anatomia — con le misure

```
┌─ .portal-bar (di portal.css; 71px a 1440/1024/768, 123 a 360) ────────────────┐
│  [lock-up]                              [← Site public]  [FR IT EN ع]         │
├─ .atrium — grid 54fr / 46fr da 75rem ────────────────────────────────────────┤
│ .atrium__threshold (--mid-1)          │ .atrium__sheet (--min-2)              │
│  legenda della tavola (mono)          │  bordo iniziale --accent 3px          │
│  ┌ carta di Mercator 800×900 ─────┐   │  .sheet__inner 27rem = 432px          │
│  │ graticola NON uniforme         │   │  eyebrow «ESPACE RÉSERVÉ»             │
│  │ rotta lossodromica (sotto)     │   │  H1 --t-title · lede                  │
│  │ APERTURA: arco --mid-2 +       │   │  [sommario errori]                    │
│  │ graticola --terr-line + 3 grad.│   │  campi 48px · azione a tutta larghezza│
│  └────────────────────────────────┘   │  contatto d'aiuto                     │
│  legenda: Maroc · Vénétie · pausa     │                                       │
├───────────────────────────────────────┴───────────────────────────────────────┤
│ .atrium-footer (--mid-0, due righe): 6 link legali + promotore/©/versione/data │
└───────────────────────────────────────────────────────────────────────────────┘
```

Misurato a 1440×900 (`measures.json/login_1440x900`): barra 1440 × **71**; atrio 1440 × **773**; soglia **777,59** ×
773; foglio **662,39** × 773 (= 54,0 / 46,0 %); `.sheet__inner` **432** × 533, margini interni **116,69** e **113,70**
(l'asimmetria di 3 px è il bordo `--accent`, che `justify-items: center` non conta); piè di pagina 1440 × **56**;
**altezza del documento 900, scorrimento 0**. Niente scorrimento orizzontale a nessuna viewport della matrice
(`horizontalOverflow = false`, 10 su 10).

**Nessun piè di pagina pubblico a quattro colonne.** Al suo posto `_atrium_footer.html` (§7.3), che però **non taglia
nulla**: è lo stesso contenuto legale su due righe.

**L'arco non porta né fotografia né chiave.** §8.8 esclude la fotografia; la chiave è cancellata (EMENDAMENTO nessuno:
è semplicemente rimossa). Restano arco e gradini, cioè il «glifo arco+gradini» che §6 ammette nella piattaforma.
**Nessuna isoipsa**: sono IMMERSIVE-only (§1.3 regola 2). `data-mode="rich"`, **un solo** capitolo mezzanotte.

### 4.2 Token — rapporti ricalcolati (WCAG 2.x, luminanza relativa, composizione alfa esplicita)

Tutti i valori qui sotto sono stati ricalcolati in questa sessione (`contrast.py`); nessuno è riportato dal round 1. Dove
c'è un'opacità, il colore è **composto** sul fondo e poi confrontato.

**Testo**

| Ruolo | Token su fondo | Rapporto |
|---|---|---:|
| titolo, lede, corpo del foglio | `--ink` su `--min-2` | 15,56 |
| lede e aiuto | `--ink-2` su `--min-2` | 6,87 |
| eyebrow del foglio | `--ink-3` su `--min-2` | 5,88 |
| valore del campo | `--ink` su `--min-3` | 16,23 |
| **campo disabilitato** (corretto: il round 1 diceva 5,88) | `--ink-3` su `--min-1` | **5,14** |
| link nel foglio | `--accent` su `--min-2` | 6,05 |
| etichetta della CTA | `--min-0` su `--accent` | 5,69 |
| etichetta della CTA in hover | `--min-0` su `--accent-hover` | 7,67 |
| errore inline | `--err-700` su `--min-2` | 6,27 |
| titolo del sommario sul suo fondo | `--err-700` su `--err-100` | 5,10 |
| pannello «limite di tentativi» | `--pending-700` su `--min-2` | 6,70 |
| nomi delle due rive | `--on-dark` su `--mid-1` | 15,51 |
| legenda e folio della tavola | `--on-dark-3` su `--mid-1` | 6,44 |
| link del piè di pagina | `--accent-dark` su `--mid-0` | 10,57 |
| colophon del piè di pagina | `--on-dark-2` su `--mid-0` | 10,22 |

**UI non testuale (soglia 3:1)**

| Ruolo | Token su fondo | Rapporto |
|---|---|---:|
| bordo del campo | `--hairline-strong` su `--min-3` | **3,74** ✔ |
| bordo del campo in hover | `--ink-2` su `--min-3` | 7,17 |
| anello di fuoco sul campo / sul foglio | `--accent-ring` su `--min-3` / `--min-2` | **4,11 / 3,94** ✔ |
| bordo del campo in errore | `--err-700` su `--min-3` | 6,54 |
| filetto iniziale del foglio | `--accent` su `--min-2` | 6,05 |
| bordo del pannello di consenso | `--hairline-strong` su `--min-1` | **3,14** ✔ |

**Grafica della soglia** — decorativa (`aria-hidden="true"` su entrambe le tavole) e quindi fuori da 1.4.11; i valori si
dichiarano lo stesso, perché una specifica che tace su un numero è una specifica che lo inventa.

| Elemento | Composizione | Su | Colore composto | Rapporto |
|---|---|---|---|---:|
| superficie dell'apertura | `--mid-2` pieno | `--mid-1` | `#14242E` | 1,10 |
| graticola (fuori dall'apertura) | `--on-dark` @ .09 | `--mid-1` | `#222E36` | 1,26 |
| tacche della graticola | `--on-dark` @ .22 | `--mid-1` | `#3F4A50` | 1,92 |
| graticola dentro l'apertura | `--terr-line` @ .55 | `--mid-2` | `#2C6C75` | 2,66 |
| tacche dentro l'apertura | `--terr-line` @ .85 | `--mid-2` | `#39929C` | 4,36 |
| **l'arco** | `--accent-dark` pieno | `--mid-1` | `#7FD1D8` | **10,01** |
| gradino 1 / 2 / 3 | `--accent-dark` @ .90 / .62 / .40 | `--mid-1` | `#74BFC6` / `#548C93` / `#3B646B` | 8,34 / 4,63 / 2,68 |
| rotta | `--accent-dark` @ .55 | `--mid-1` | `#4C7F87` | 3,91 |
| pallini delle rive e marcatore | `--accent-dark` pieno | `--mid-1` | `#7FD1D8` | 10,01 |

Il disegno che **identifica** la composizione — l'arco — misura 10,01:1. Le tacche dentro l'apertura, che sono ciò che
fa leggere l'apertura come apertura, misurano 4,36:1. Nessun elemento che porta significato scende sotto 3:1.

**Token nuovi**, tutti in `static/css/v3/auth.css`, nessuno è un colore — la regola dell'accento unico resta intatta:
`--sheet-measure: 27rem` (432 px ≈ 58 caratteri in Fira Sans 17 px, sotto il limite di 75 di §3.2) ·
`--field-h: 48px` · `--field-rule: 2px` · `--otp-glyph: .6em` e `--otp-cell: 1.2em` (locali al campo codice) ·
`--dir: 1`, con `[dir="rtl"] { --dir: -1 }` **dichiarato in `auth.css`** — `tests/frontend/test_css_tokens_exist.py`
cerca `--nome:` in un foglio qualunque, non solo in `:root`, e la verifica è stata eseguita: **nessuna proprietà
personalizzata riferita da `auth.css` è indefinita** (LACUNA 10 chiusa e provata).

**Cancellato:** `--entrance-bar-h` (disputa D1) e la riga `--brand-gold` su `--brand-navy` (violazione 3).

### 4.3 La soglia — la tavola, l'apertura, la rotta, e l'unico oggetto vivo

**La tavola.** Un `viewBox="0 0 800 900"`, `preserveAspectRatio="xMidYMax slice"` — ancorato in basso, così arco e
gradini poggiano sempre sul bordo inferiore della tavola qualunque sia la proporzione della colonna. Finestra
geografica: longitudini da −12° a +18°, latitudini da 30° a 49° N.

Proiezione: `y = ln(tan(π/4 + φ/2))`, riscalata sull'altezza. Path generati (`chart2.py`, deterministici, nessun
`Math.random`, nessuna dipendenza da `scripts/territory.py`):

```
meridiani (ogni 5°, equidistanti):
  M53.3 0V900 M186.7 0V900 M320 0V900 M453.3 0V900 M586.7 0V900 M720 0V900
paralleli (ogni 2°, NON equidistanti — è la proiezione):
  M0 815.6H800 M0 729.4H800 M0 641.1H800 M0 550.6H800 M0 457.6H800
  M0 361.7H800 M0 262.9H800 M0 160.6H800 M0 54.6H800
passo fra paralleli, da sud a nord: 86.2 · 88.3 · 90.5 · 93.0 · 95.8 · 98.9 · 102.3 · 106.0
tacche: croce di 8 unità alle intersezioni dei paralleli PARI di 4° (32 · 36 · 40 · 44 · 48 N)
         con i sei meridiani → 30 croci, 807 byte di path. A ogni parallelo sarebbero 54 e la
         tavola leggerebbe come una griglia millimetrata invece che come una carta.
```

**L'apertura.** L'arco è la porta di `BRAND_ASSETS.md` §2 in proporzione 3:4, larghezza 288, raggio 144, centro
`x = 392`, base `y = 700`, imposta `y = 460`, chiave di volta `y = 316`:

```
arco   d="M248 700V460A144 144 0 0 1 536 460V700"      (pathLength="1", per A1)
clip   d="M248 700V460A144 144 0 0 1 536 460V700Z"      (<clipPath id="atr-aperture">)
gradini (proporzioni del marchio 56/68/80, smorzate):
  <rect x="332" y="706" width="120" height="10">
  <rect x="320" y="720" width="144" height="10">
  <rect x="308" y="734" width="168" height="10">
```

Dentro la sagoma: una superficie `--mid-2` (`.arch__ground`) e **la stessa graticola** ridisegnata più chiara via
`<use href="#atr-grat">` dentro un `<g clip-path="url(#atr-aperture)">`. Un solo `<g>` in `<defs>`, due `<use>`: la
graticola non è duplicata nel sorgente. L'arco non è un contorno sopra un fondo: è **un'apertura attraverso cui la carta
si vede meglio.** Nessun gradiente è coinvolto.

**La rotta.** `M137.3 730.7 L636.8 191.1` — la lossodromia fra le due rive, che su Mercator è una retta (rilevamento
costante 51,4°). Lunghezza 735,3 unità. È in **una seconda `<svg>`, disegnata PRIMA della tavola**, quindi la superficie
`--mid-2` dell'apertura la copre: la rotta entra dietro lo stipite iniziale a `x = 248, y = 611,2` (`t = 0,222`) e
riemerge oltre la volta a `x = 487,6, y = 352,3` (`t = 0,701`). `DESIGN_SYSTEM_V2` §8.3, alla lettera.

Due `<svg>` e non una sola, esattamente per la ragione già misurata dall'hero
(`v2/hero.css:23-28`: «A `<g>` moved inside one big SVG repaints it on every frame — measured at 27fps»): l'elemento
animato vive in una tavola che contiene una retta e tre cerchi, non le cinquanta linee della graticola.

**La legenda**, in `--f-mono` `--t-folio`: in alto `Projection de Mercator · 30°–49° N · 12° O – 18° E`; in basso, sopra
un filetto `--hairline-dark`, i due punti con il componente **già in produzione** `.coord` / `.coord__dot`
(`v2/hero.css:415`), e il controllo `.tide-toggle` (`v2/hero.css:438`), riusato senza una riga di CSS nuova salvo la
posizione. I valori numerici portano `dir="ltr"`: senza, in `dir="rtl"` l'algoritmo bidi riordina
`33.97° N · 6.85° W` in `N · 6.85° W 33.97°` — **osservato** nel primo giro RTL di questa sessione e corretto.

**L'oggetto vivo — «la veglia».** Un `<circle r="3.5">` `--accent-dark` che percorre la lossodromia da riva a riva in
`var(--motion-ambient)` = **28 s**, lineare, `transform: translate3d(499.5px, -539.6px, 0)` in unità utente SVG (che
scalano con la tavola), comparendo al 6 % e svanendo al 100 %, `infinite`. Attraversa la porta: fra `t = 0,222` e
`t = 0,701` scompare dietro l'apertura e riemerge oltre la volta, cioè **passa dalla porta**, che è l'unica cosa che
questa pagina ha da dire.

- Funzione dichiarata: **ORIENTAMENTO** (MOTION_SYSTEM §0: «da dove vengo, dove sono»).
- Perché è ammesso senza deroga: MOTION_SYSTEM §4 concede a RICH **uno** fra il loop ambientale (≥ 20 s) e l'oggetto
  legato allo scroll; l'atrio spende il primo e non il secondo. `DESIGN_SYSTEM_V2` §7 vieta a RICH «isoipse, marea»:
  questo non è né l'una né l'altra. Si chiede comunque il chiarimento al §0, EMENDAMENTO 5.
- Perché non è uno shimmer: 28 s su 735 unità significa **26 unità al secondo**, cioè ai limiti della percezione; è
  verticale-diagonale e non orizzontale; non tocca `filter`, non tocca `background-position`, non tocca `box-shadow`.
- Perché non è la chiave che levita: ha una direzione, una destinazione e un significato, e MOTION_SYSTEM §0 chiede
  esattamente questo.
- Pausa: `IntersectionObserver` (`.is-offscreen`) e il controllo «Suspendre le mouvement» (`.is-paused`), entrambi
  `animation-play-state: paused`. Il controllo **non è un vezzo**: WCAG 2.2.2 lo richiede per contenuto in movimento
  che parte da solo e dura più di cinque secondi.
- Stato ridotto: **nessuna animazione**, e il marcatore riposa a `t = 0,20`, cioè `translate3d(99.9px, -107.9px, 0)` —
  appena fuori dallo stipite, **visibile**, sulla soglia. Nulla è nascosto, nulla è a opacità 0.

**Costo, misurato** (`probe.py/motion_normal`, 1440×900, Chromium headless, 3 s di loop, 181 frame):
mediana **16,7 ms**, p95 **16,7 ms**, massimo **16,8 ms**, **0 frame oltre 20 ms**. 60 fps pieni.

### 4.4 Il foglio

`--min-2` su canvas `--min-0`; il contrasto di superficie è 1,06:1, quindi il confine non lo fa la tinta ma **il bordo
iniziale `--accent` di 3 px**, che è il gesto di §9.2. Misura `--sheet-measure` 27rem, contenuti centrati
verticalmente (`align-content: center`), `justify-items: center`.

**`contain` — e perché non è più un problema.** `contain: layout paint` sta **solo** su `.atrium__threshold`, dove
serve davvero (contiene due SVG in posizione assoluta e l'unica animazione della pagina). **Non sta sul foglio**: il
foglio non contiene nulla di assolutamente posizionato tranne il bottone di rivelazione, che è contenuto dal suo
`.form-field__control`, e non ha nulla da isolare. La LACUNA 9 è quindi chiusa togliendo la causa, non aggiungendo un
margine.

**Scorrimento.** Il foglio **non ha uno scorrimento proprio a nessuna larghezza.** C'è un solo contenitore di scroll su
questa superficie: il documento. Ragione: un modulo dentro uno scroller annidato rompe la ricerca nella pagina, la
navigazione da tastiera, la catena dello scroll e i link del sommario errori; e nel prototipo con il foglio scrollabile
il modulo d'iscrizione appariva troncato senza affordance visibile. Conseguenza misurata: login = **una viewport esatta**
a 1440, 1280, 1200, 1199, 1024, 900, 768 e 767 (`doc.h == viewport.h`, `pageScroll = 0`); a 390 la pagina scorre di
**94 px**, a 360 di **274 px**; iscrizione a 1440 scorre di **366 px** e a 390 di **617 px**. In tutti i casi
`sheetScrolls = false`.

E poiché la barra d'atrio **non è appiccicata** (`.page-atrium .portal-bar { position: static }`), nessun elemento
copre la cima del documento: `scroll-padding-block-start` non serve a nessuno. La LACUNA 7 è chiusa allo stesso modo
della 9 — togliendo la causa.

### 4.5 Il campo

Bianco (`--min-3`) su foglio `--min-2`: la differenza di superficie è 1,04:1, quindi **il confine lo fa il bordo, non la
tinta** — 1 px `--hairline-strong` più una **riga di base di 2 px** dello stesso colore. È un bordo, non un'ombra: non
introduce un quinto ruolo di `box-shadow` (§2).

**Specificità — questo è un dettaglio d'implementazione che è costato un giro di misura, e va scritto.**
`components.css` seleziona i campi con `.form-field input:not([type="checkbox"]):not([type="radio"]):focus-visible`,
specificità (0,4,1). Un `.atrium .form-field input:focus-visible` vale (0,3,1) e **perde**, anche caricando `auth.css`
dopo `main.css`: nel primo prototipo l'anello di fuoco non compariva affatto (`focus_1440.boxShadow = none`,
`outline-offset: 0px`). Ogni regola di campo in `auth.css` ripete quindi la catena `:not()`.

| Stato | Regola |
|---|---|
| riposo | `block-size: var(--field-h)`; `background: var(--min-3)`; `border: 1px solid var(--hairline-strong)`; `border-block-end-width: var(--field-rule)`; `border-radius: var(--radius-control)`; `padding-inline: var(--s-4)`; `--t-body`; `box-shadow: none` |
| hover (`@media (hover: hover)`) | `border-color: var(--ink-2)` (7,17:1) |
| focus-visible | `outline: 2px solid var(--accent-ring); outline-offset: 2px` + `box-shadow: 0 0 0 5px rgba(29,138,147,.30)` + `border-block-end-color: var(--accent)`. **Sporgenza misurata 5 px** (§1.3 D2) |
| riempito | invariato: nessuna etichetta flottante, mai il placeholder come etichetta |
| **riempimento automatico** | `:-webkit-autofill`, `:-webkit-autofill:hover`, `:autofill` → `-webkit-text-fill-color: var(--ink)`, `caret-color: var(--ink)`, `box-shadow: inset 0 0 0 100px var(--min-3)`, bordo invariato. Al fuoco i due `box-shadow` si **compongono** in una sola dichiarazione: `inset 0 0 0 100px var(--min-3), 0 0 0 5px rgba(29,138,147,.30)` — senza questo, l'anello scomparirebbe sul campo riempito automaticamente, cioè proprio sulla schermata di login |
| errore | bordo e riga di base `--err-700` (6,54:1), `box-shadow: none`, `aria-invalid="true"` di Django 5.2, errore inline sotto |
| disabilitato | `background: var(--min-1)`, testo `--ink-3` (**5,14:1**), bordo `--hairline` — **colore, mai opacità** |
| in attesa | il modulo prende `aria-busy="true"`; i campi restano leggibili, non si nascondono |

`box-shadow` compare in `auth.css` in **cinque** dichiarazioni, contate, e in nessun'altra: (1) `none` a riposo, esplicito
perché niente erediti l'anello di 1 px che `components.css:2241` mette al fuoco; (2) l'alone al fuoco, che lo sostituisce; (3) il riempimento `inset` del
riempimento automatico — che non è un'ombra ma una tinta, ed è l'unico modo di sovrascrivere il fondo imposto dal
browser sotto `style-src 'self'`; (4) la loro composizione al fuoco su un campo riempito automaticamente; (5) `none`
sullo stato d'errore. Nessun ruolo d'ombra nuovo: §2 ne conta quattro più il livello 4 di fuoco, e qui c'è solo il
livello 4. La guardia del §9 conta cinque e le enumera.

**Ordine del DOM: etichetta → controllo → aiuto → errore.** Invariato, perché è ciò che `components/form_field.html`
rende già e ciò che `DESIGN_SYSTEM_V2` §10 prescrive («etichetta visibile sopra, errore accanto, aiuto sotto»). Il
round 1 proponeva l'aiuto **sopra** il controllo: sarebbe una modifica a un partial condiviso da circa quaranta
template e una contraddizione con §10. **Ritirata.** `form_field.html` non viene toccato.

**Il `<select>` di `account_type`** (`apps/accounts/forms.py:28`, cinque scelte pubbliche, obbligatorio). Stessa
geometria del campo di testo — 48 px, stesso fondo, stesso bordo, stessa riga di base — più:

```css
.atrium .form-field select {
  appearance: none;
  padding-inline-end: calc(var(--s-4) * 2 + 20px);   /* 52px: 16 + glifo 20 + 16 */
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20' fill='none' stroke='%2315222A' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M5 8l5 5 5-5'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right var(--s-4) center;
  background-size: 20px 20px;
}
[dir="rtl"] .atrium .form-field select { background-position: left var(--s-4) center; }
```

Sei stati: riposo, hover, focus-visible, errore, disabilitato, aperto. I primi cinque sono **le stesse regole del campo
di testo** (il selettore le nomina insieme), quindi non c'è nulla da inventare; l'aperto è il popup nativo del sistema
operativo e non si stila — è una decisione, non un'omissione: un listbox disegnato a mano perderebbe la tastiera, la
ricerca per iniziale e il picker a rotella su mobile. Il glifo è a 1,5 px di tratto, 20 px, `currentColor` codificato
come `--ink` (§6 del sistema). `stroke` con `%23` e non `#`, altrimenti il `data:` URI si tronca all'ancora.
**In RTL il chevron non si specchia — si specchia la sua posizione**: un chevron che punta in basso non ha direzione di
lettura (§11 esclude dal ribaltamento ciò che non è direzionale), mentre il lato su cui sta è logico. Misurato in
`dir="rtl"`: `background-position` a sinistra, nessuno scorrimento orizzontale. `data:` in un foglio di stile è
consentito: `style-src 'self'` governa la provenienza del foglio, e `img-src 'self' data:` è già nella policy
(`config/settings/base.py:350`).

**Affordance nuove — nessuna tocca il template, tutte le crea `auth.js`**, perché nessuna delle tre funziona senza JS e
un bottone che non fa nulla è peggio di nessun bottone:

- `.form-field__reveal` — bottone 44 × 44 dentro il campo password (`inset-inline-end: 2px`, quindi 2 px di margine
  dentro un campo di 48; misurato 44 × 44 a x = 1280,28 in un campo che finisce a 1326,28), `type="button"`,
  `aria-pressed`, nome accessibile che commuta fra «Afficher le mot de passe» e «Masquer le mot de passe». Il campo
  prende `padding-inline-end: 52px` per non scrivere sotto il glifo. Assente senza JS.
- `.form-field__caps` — avviso «Verrouillage des majuscules activé» da `getModifierState("CapsLock")`, `role="status"`,
  colore `--pending-700` (6,70:1) **più** la parola: il colore non è mai solo.
- `.form-field__count` — **al posto del misuratore di robustezza.** Il misuratore è cancellato: era un secondo parere
  sulla stessa password, e contraddiceva `CommonPasswordValidator` e `UserAttributeSimilarityValidator` ogni volta che
  diceva «Solide» su una password che il server poi rifiuta. Al suo posto **l'unico fatto che il browser può provare**:
  la lunghezza contro `ACCOUNT_PASSWORD_MIN_LENGTH = 12` (`config/settings/base.py:190`). `role="status"`, aggiornato
  al massimo una volta ogni 400 ms, due sole formulazioni («Il manque {n} caractères.» / «Longueur minimale
  atteinte.»), nessun colore, nessuna barra, nessun giudizio. Gli altri tre validatori restano dove sono: nel
  `help_text` che allauth già rende (`account/forms.py:433`) e nella risposta del server.
- Le formulazioni non stanno in JavaScript: vivono in `data-label-*` su `.atrium` (§7.2), rese e tradotte dal server.

**Nota d'implementazione trovata misurando:** su `account/signup`, `password1.help_text` è
`password_validation.password_validators_help_text_html()`, cioè un `<ul>` che `form_field.html` mette dentro un `<p>`.
Il browser lo recupera, ma `.form-field__help` deve stilare `ul` o l'elenco esce senza rientro. `auth.css` lo fa
(`.atrium .form-field__help ul { margin: var(--s-2) 0 0; padding-inline-start: var(--s-5) }`). Il `<p>` che contiene un
`<ul>` è un difetto di `form_field.html` che **non** appartiene a questa specifica: segnalato alla superficie dei
moduli.

### 4.6 Bottoni

**Ambito, prima di tutto.** `static/css/v3/buttons.css` è già in albero e possiede `.btn--primary`: dichiara
`--btn-bg: var(--accent)`, `--btn-fg: var(--min-0)`, `--btn-bg-hover: var(--accent-hover)`, e ha già corretto il difetto
per cui la CTA era il navy del marchio (il punto 2 dell'audit). **L'atrio non ridichiara nessuno di quei valori.** Il
colore della CTA viene da lì; qui si specificano soltanto la geometria e la firma, scoped a `.atrium`, perché la
riscrittura globale di `.btn` è di un'altra superficie e `components.css` non si tocca.

```css
.atrium .form__actions { margin-block-start: var(--s-8); }
.atrium .form__actions .btn--primary {
  inline-size: 100%;                 /* misurato: 432 px a >= 1200, 358 a 390 */
  min-block-size: 48px;              /* §10 */
  display: inline-flex; align-items: center; justify-content: center; gap: var(--s-3);
  border-radius: var(--radius-control);            /* 2px */
  font-family: var(--f-sans); font-size: var(--t-ui); font-weight: 500;
}
.btn__rule {                          /* la linea d'ormeggio di §8.5 */
  inline-size: 16px; block-size: 1px; background: currentColor;
  transform: scaleX(0);
  transform-origin: calc(50% - var(--dir) * 50%) 50%;   /* bordo iniziale, logico */
}
@media (prefers-reduced-motion: no-preference) {
  .btn__rule { transition: transform var(--motion-fast) var(--ease-out); }
}
.atrium .btn--primary:hover .btn__rule,
.atrium .btn--primary:focus-visible .btn__rule { transform: scaleX(1); }
```

**A riposo**, dentro il bottone: etichetta · `.btn__rule` a `scaleX(0)` · freccia `icon--flip-rtl`. Misurato a 1440:
**432 × 48**, fondo `rgb(15, 106, 114)` = `--accent`, etichetta `--min-0` a **5,69:1**. La ragione della larghezza
piena, e la ragione per cui il bottone non è più muto nello screenshot, sono al §1.6.

**Stati.** hover `--accent-hover` (7,67:1) 180 ms · active `translateY(1px)` 120 ms (entrambi da `components.css`, non
ridichiarati) · focus come §2 livello 4 (anello 2 px `--accent-ring`, sporgenza misurata 5 px) · disabilitato a colore,
mai a opacità · **attesa** `aria-busy="true"` sul modulo più lo scambio dell'etichetta con «Vérification en cours…»
(A6). **Nessuno spinner che ruota**: una rotazione è un loop, e il loop di questa pagina è già speso (AMB, §4.3). Il
round 1 ne aveva due.

`.btn--secondary` (presente su `password_reset_from_key_done`, `account_inactive`): 1 px `--hairline-strong`, testo
`--ink`, stessa altezza, **non** a larghezza piena — quando ci sono due azioni non c'è più «l'unica azione della
pagina» e l'argomento del §1.6 cade. Sulla soglia esiste un solo controllo oltre alla pausa, «← Site public», che è
`.portal-bar__link` di `portal.css` e non si ridichiara.

### 4.7 Il campo codice (MFA, conferma e-mail, codici di recupero)

**Un solo `<input>`**, mai sei. Nessuna modifica al template: allauth mette già
`autocomplete="one-time-code"` sul widget (`account/forms.py:771`, `mfa/base/forms.py:17`, `mfa/totp/forms.py:18`),
quindi il gancio è `[autocomplete="one-time-code"]` e basta.

Le sei celle sono **disegnate**, e ora sono **misurate** invece che asserite. Il round 1 le definiva in percentuale
(`16,6667 %` della larghezza del campo): a 432 px di campo la cella disegnata misurava **72 px** mentre l'avanzamento di
un carattere era **23 px** — le cifre non cadevano nelle celle. La correzione è metrica, non estetica:

```css
.atrium .form-field input[autocomplete="one-time-code"]:not([type="checkbox"]):not([type="radio"]) {
  block-size: 56px; min-block-size: 56px;
  font-family: var(--f-mono); font-variant-numeric: tabular-nums; font-size: 22px;
  --otp-glyph: .6em;   /* avanzamento di Fira Mono: MISURATO a 0,6000 em esatti */
  --otp-cell: 1.2em;   /* glifo + un glifo di spaziatura */
  letter-spacing: var(--otp-glyph);
  text-align: start; direction: ltr;
  inline-size: calc(var(--otp-cell) * 6);
  padding-inline: calc(var(--otp-cell) / 2 - var(--otp-glyph) / 2) 0;   /* centra il glifo nella cella */
  margin-inline: auto; display: block;
  background-image: repeating-linear-gradient(90deg, transparent 0, transparent calc(var(--otp-cell) - 1px),
                    var(--hairline-strong) calc(var(--otp-cell) - 1px), var(--hairline-strong) var(--otp-cell));
  background-repeat: no-repeat;
  background-size: calc(var(--otp-cell) * 6 - 1px) 100%;
  background-position: left top;
}
```

Misurato (`probe.json/otp`, `shot_otp.png`): campo **158,39 × 56**, cella **26,40 px**, `letter-spacing` calcolato
**13,2 px**, `1ch` di Fira Mono a 22 px = **13,1875 px**. Le quattro cifre del prototipo cadono una per cella, centrate.
`--f-mono` viene **precaricato** dall'atrio (`{% block extra_head %}`), perché `fonts.css` lo dichiara con
`font-display: swap` e senza precarico il campo cambierebbe larghezza al caricamento del font.

`inputmode="numeric"`, `pattern="[0-9]*"`, `maxlength="6"`, `dir="ltr"` sono già del widget allauth o si aggiungono via
JS senza toccare il contratto dei dati. **Nessun invio automatico**: al sesto carattere `role="status"` annuncia «Code
complet.» e il bottone resta abilitato — l'autorità è del server, sempre. Incolla e riempimento automatico funzionano da
soli; lo screen reader legge **un** campo, non sei. **Nessun cursore animato**: il round 1 prevedeva un marcatore
`SPRING_FOLLOW` che segue la cifra; è cancellato, perché il cursore nativo fa già quel lavoro, perché sarebbe un secondo
oggetto in moto su una pagina che ne ha già uno, e perché la sua posizione dipenderebbe da metriche di font che cambiano
prima che il font sia caricato.

### 4.8 Le tre larghezze — MUST-FIX 7, con la misura che sceglie il punto di rottura

Il round 1 legava lo split a «≥ 75rem» e la colonna singola a «sotto 768 px», lasciando **la fascia 768–1199 senza
definizione**. Non è un dimenticanza che si chiude scrivendo un terzo valore: la domanda vera è *a che larghezza la
tavola smette di leggersi*, e quella si misura.

**La misura.** `preserveAspectRatio="xMidYMax slice"` scala la tavola per coprire la colonna. Su una colonna alta e
stretta la scala la comanda l'altezza, e la tavola viene ritagliata in larghezza attorno all'asse centrale. Misurato,
larghezza della colonna della soglia e larghezza risultante dell'arco (che nella tavola è largo 288 unità su 800):

| viewport | colonna soglia | scala | arco reso | lo stipite finale (x = 536) è dentro il ritaglio? |
|---|---:|---:|---:|---|
| 1440 × 900 | 777,6 | 0,972 | **279,9** | sì |
| 1280 × 800 | 691,2 | 0,864 | 248,8 | sì |
| 1200 × 800 | 648,0 | 0,810 | 233,3 | sì |
| 1199 × 800 (38/62) | 455,6 | 0,717 | 206,4 | sì |
| 1024 × 768 (38/62) | 389,1 | 0,681 | 196,2 | sì, al limite |
| 900 × 1200 (38/62, prova) | 342,0 | 1,161 | 334,4 | **no — lo stipite iniziale esce dal ritaglio** |
| 768 × 1024 (38/62, prova) | 291,8 | 0,966 | 278,1 | **no — l'arco è tagliato a metà** |

Sotto una colonna di circa **380 px** la tavola si ritaglia oltre uno dei due stipiti e il disegno legge come rotto:
è il motivo, misurato, per cui lo split non può arrivare a 768. Da qui le tre larghezze:

| Banda | Layout | Colonne misurate | Padding inline del foglio | Misura |
|---|---|---|---|---|
| **≥ 75rem (1200)** | due colonne, la tavola intera | `minmax(0, 54fr) minmax(29rem, 46fr)` → 777,6 / 662,4 a 1440; 648 / 552 a 1200 | `var(--s-10)` = **40 px** | 432 |
| **64–74,999rem (1024–1199)** | due colonne, tavola più stretta ma integra | `minmax(0, 38fr) minmax(26rem, 62fr)` → 455,6 / 743,4 a 1199; 389,1 / 634,9 a 1024 | `var(--s-8)` = **32 px** | 432 |
| **< 64rem (1024)** | una colonna; la soglia diventa la **fascia di §8.8** | `1fr` con `grid-template-rows: auto 1fr` | `var(--s-8)` = 32 px fino a 30rem, poi `var(--s-4)` = **16 px** | 432, poi `100%` |

`minmax(29rem, …)` sulla colonna del foglio: 29rem = 464 px = misura 432 + 2 × 16 px di padding minimo assoluto. A
1200 px il 46 % vale 552 px, quindi il minimo non morde mai; è una rete, non una regola.

**La fascia sotto 1024.** Non è la tavola rimpicciolita: la tavola e la rotta **non vengono disegnate**, e al loro posto
c'è il **glifo arco+gradini** che §6 del sistema già prescrive per la piattaforma. È la lettura letterale di §8.8 («la
grammatica ridotta a una fascia di 120 px»). Misurata: **127 px** a 900, 768, 767, 390 e 360 — cioè 120 px di
`min-block-size` più il glifo di 95 px dentro `var(--s-4)` × 2 di padding, che arrotonda a 127. La legenda dei due
luoghi resta, allineata al bordo finale; il folio della proiezione e il controllo di pausa cadono, perché la proiezione
non è disegnata e non c'è moto da sospendere. **Conseguenza dichiarata: sotto 1024 questa superficie non ha oggetto
ambientale.** È corretto — il moto ambientale costa batteria dove serve di meno — ed è il motivo per cui
`prefers-reduced-motion` e la fascia si comportano allo stesso modo.

**Sporgenza del fuoco contro il padding**, misurata (sporgenza 5 px, §1.3 D2): 40 px a ≥ 1200, 32 px a 1024–1199 e da
480 a 1023, **16 px sotto 480**. Margine residuo minimo **11 px**. E `contain: paint` non è sul foglio (§4.4).

**Moduli lunghi.** L'iscrizione ha sei campi più il consenso e non entra in una viewport: le due colonne si allungano
insieme (la griglia le stira), e la tavola cresce con la colonna. Misurato a 1440 × 900: soglia e foglio **1139** px,
documento 1266, scorrimento 366, arco reso **365** px. È il comportamento dell'hero, non un'eccezione: la tavola è un
foglio che si estende, non un'immagine che si deforma. Nessuno scorrimento annidato, nessun troncamento (§4.4).

**Zoom.** A 200 % (720 px logici) e 400 % (360 px logici) si applica la terza banda: una colonna, nessuno scorrimento
orizzontale, `grid-template-columns` calcolato `720px` e `360px`.

### 4.9 Errori e stati eccezionali

`components/form_errors.html` **non viene toccato**: struttura, `role="alert"`, `tabindex="-1"`, i link a ogni campo e
il fuoco già spostato da `main.js:30` restano esattamente come sono. Il conteggio nel titolo («2 champs à corriger») del
round 1 è **ritirato**: richiederebbe di modificare un componente condiviso da circa quaranta moduli, e la formulazione
attuale è già passata dalla revisione. Cambia solo l'aspetto, da `auth.css`, scoped a `.atrium`: ground `--err-100`,
filetto iniziale 3 px `--err-700`, titolo `--err-700` (5,10:1 sul suo fondo), corpo `--ink` (12,67:1). Gli errori
inline restano sempre, mai sostituiti dal sommario.

`.atrium .form-errors` e `.atrium .form-field` portano `scroll-margin-block-start: var(--s-6)`, così i link del
sommario non depositano il campo a filo del bordo superiore della finestra.

**Limite di tentativi** (`ACCOUNT_RATE_LIMITS["login_failed"] = "5/5m/ip,5/5m/key"`, `config/settings/base.py:192` —
citazione corretta, disputa D3): pannello `--pending-700` (6,70:1) con il tempo d'attesa e il link d'aiuto; una
schermata vera, non una scatola rossa anonima. La formulazione è **HUMAN_QA_REQUIRED** (§6.6).

---

## 5. MOTION — voci per `MOTION_SYSTEM.md` §6

Tutte da `static/js/src/auth.js` tramite `withMotion()`, tranne AMB e il filetto del bottone che sono CSS. **Un solo
oggetto vivo per pagina** (AMB); l'unica altra rotazione possibile è lo spinner del bottone, legato a un'operazione in
corso, che cessa con essa.

| # | Nome | Funzione | Innesco | Durata | Curva | Proprietà | Stato ridotto | Budget |
|---|---|---|---|---|---|---|---|---|
| A1 | L'arco si traccia | DELIZIA + ORIENTAMENTO | load, una volta | **900 ms `--motion-draw`** | `--ease-out` | `strokeDashoffset 1→0` su **un** path `pathLength="1"` | `strokeDashoffset: 0` dal primo frame | 1 elemento |
| A2 | I gradini si posano | GERARCHIA | **concatenata: `trace.finished.then(...)`** | **240 ms `--motion-base`, stagger 50 ms** | `--ease-out` | `opacity 0→1`, `translateY 6→0` | valori finali, fermi | 3 elementi |
| A3 | Il foglio entra | GERARCHIA | load | 240 ms `--motion-base`, stagger 50 ms su **≤ 6** nodi (`slice(0, 6)`) | `--ease-out` | `opacity`, `translateY 10→0` | tutto al valore finale | ≤ 6 elementi |
| A4 | La riga di base al fuoco | ORIENTAMENTO | `:focus-visible` (CSS, `components.css:2221`, `--duration-fast` → `--motion-fast`) | 180 ms `--motion-fast` | `--ease-standard` | `border-color`, `box-shadow` | **`transition: none`**, neutralizzata in `auth.css` | 0 |
| A5 | La pressione del bottone | FEEDBACK | `:active` (CSS, `components.css`) | 120 ms `--motion-instant` | `--ease-in` | `transform: translateY(1px)` | identico | 0 |
| A6 | Il bottone attende | FEEDBACK | `submit` (`data-single-submit`) | **finché `aria-busy`**, non una durata | — | scambio di parola + `aria-busy="true"` | identico: la parola cambia, nulla ruota | 0 |
| A7 | Il sommario errori prende il fuoco | CAUSALITÀ | risposta con errori | 240 ms `--motion-base` | `--ease-standard` | `opacity`, `translateY 8→0` | nessun moto, fuoco immediato (`main.js:30`) | 1 elemento |
| A8 | La linea d'ormeggio | DELIZIA | `:hover` / `:focus-visible` (CSS) | 180 ms `--motion-fast` | `--ease-out` | `transform: scaleX(0→1)`, origine `calc(50% - var(--dir) * 50%)` | assente; l'etichetta e la freccia sono già lì | 1 elemento |
| **AMB** | **La veglia** | **ORIENTAMENTO** | load | **28 s `--motion-ambient`**, `linear`, `infinite` | `linear` (ammesso solo nei loop) | `transform: translate3d` + `opacity` su **un** `<circle>` | **nessuna animazione; il marcatore riposa sulla soglia, `translate3d(99.9px, -107.9px, 0)`** | 1 elemento, **0 frame > 20 ms su 181 misurati** |

**Cancellate rispetto al round 1:** A6 come rotazione di uno spinner (una rotazione è un loop, e il loop di questa
pagina è AMB — l'attesa si dice con una parola e `aria-busy`); A9 (cursore del codice, §4.7); A10 (tacche di robustezza,
§4.5); A11 (la chiave, violazioni 3 e 4); A12 (View Transition, EMENDAMENTO 2).

**Numeri usati, tutti e soli:** 120, 180, 240, 900 ms e il loop a 28 000 ms. Nessun altro. Lo stagger è 50 ms, dentro la
banda 40–60 di MOTION_SYSTEM §1. Il ritardo fra A1 e A2 non è un numero: è la promessa `finished` dell'animazione
precedente. Il throttle di 400 ms del contatore di caratteri **non è un'animazione** — è la cadenza minima di un
annuncio `aria-live`, cioè una politica di accessibilità, e non entra nel conteggio delle durate.

**`auth.js` è stato compilato ed eseguito, non solo scritto.** Bundle esbuild 0.28.2 con `splitting: true`, servito al
prototipo e misurato in Chromium headless (`jstest.py`), sul modulo d'iscrizione **spogliato a mano** del bottone di
rivelazione e del contatore, per verificare che sia il JS a crearli: **2** bottoni di rivelazione **44 × 44** con
`aria-label` «Afficher le mot de passe», **2** `.form-field__control`, **2** avvisi BLOC MAJ (`hidden`, testo corretto),
**1** contatore che dice «Il manque 9 caractères.» a tre caratteri e «Longueur minimale atteinte.» a dodici; il clic
sulla rivelazione porta `input.type` a `text` e l'etichetta a «Masquer le mot de passe». **Zero errori di pagina e zero
errori di console.**

**Ogni `transition` e ogni `@keyframes` di `auth.css` sta dentro `@media (prefers-reduced-motion: no-preference)`**,
tranne il blocco `@media (prefers-reduced-motion: reduce)` che porta il marcatore alla sua posizione di riposo. Provato:
con `reduced_motion: "reduce"` il marcatore ha `getAnimations().length === 0`, `opacity: 1`,
`transform: matrix(1, 0, 0, 1, 99.9, -107.9)`.

---

## 6. ACCESSIBILITÀ E RTL

### 6.1 WCAG 2.2 — 2.5.8 Target Size, risolto per geometria

«Mot de passe oublié ?» misurava 112,48 × **13** px. Il round 1 proponeva di spostarlo sulla riga dell'etichetta
(pattern 8 di 21st.dev); **respinto**, perché allauth lo rende come `help_text` del campo password e spostarlo
visivamente sopra il controllo senza spostarlo nel DOM manda l'ordine di tabulazione all'indietro (WCAG 2.4.3).

Soluzione: `.atrium .form-field__help a { display: inline-block; min-block-size: 24px; line-height: 24px }`.
**Misurato: 121,14 × 24 px** a 1440, 1280, 1200, 1199, 1024, 900, 768, 767 e 390. ✔

Altri bersagli, misurati: casella di consenso **24 × 24**; bottone di rivelazione **44 × 44**; azione primaria
**432 × 48** (358 × 48 a 390); `.tide-toggle` **234,77 × 32** sopra 75rem e **44 × 32** sotto, dove l'etichetta passa
fuori schermo restando nel DOM (il nome accessibile non cambia); segmenti di lingua ≥ 24 px (invariati, di `portal.css`).

### 6.2 Fuoco

Anello 2 px `--accent-ring` + offset 2 px + alone 5 px al 30 % — **sporgenza misurata 5 px**, non 9 (§1.3 D2).
`--accent-ring` misura 4,11:1 sul campo bianco e 3,94:1 sul foglio. Spazio minimo fra il campo e il bordo del foglio:
16 px a 390 e 360, 32 px a 768, 103 px a 1024, 116,7 px a 1440 — **margine residuo minimo 11 px**, e comunque
`contain: paint` non è sul foglio (§4.4).

Il bottone di rivelazione usa `outline-offset: -2px`, perché è dentro il campo: a offset positivo il suo anello
toccherebbe il bordo del campo.

### 6.3 Percorso, scroll, annunci

Un solo contenitore di scroll: il documento (§4.4). La barra d'atrio non è appiccicata, quindi nessun
`scroll-padding-block-start` è necessario; i bersagli dei link del sommario portano `scroll-margin-block-start:
var(--s-6)`. Il fuoco sul sommario resta quello di `main.js:30`. `aria-describedby` / `aria-invalid` di Django 5.2
restano, e gli id `{{ field.auto_id }}_helptext` / `_error` sono quelli di sempre perché `form_field.html` non è
toccato.

### 6.4 Colore mai solo

Robustezza → **una frase, nessun colore** (§4.5). BLOC MAJ → parola `--pending-700` **più** la parola. Errore → bordo
`--err-700` **più** il testo inline **più** il sommario. Codice completo → `role="status"` con una parola. Stato del
bottone in attesa → scambio di etichetta **più** `aria-busy`, nessuna rotazione.

### 6.5 RTL, reduced motion, forced colors, zoom — tutti misurati

**RTL (`dir="rtl"`, `probe.json/rtl`, `shot_rtl.png`).** Soglia a destra (`x = 662,4`, larghezza 777,6), foglio a
sinistra (`x = 0`, larghezza 662,4), filetto `--accent` su `border-right: 3px` (cioè il bordo iniziale logico),
`--dir: -1`, **nessuno scorrimento orizzontale**. Si specchiano: la freccia del bottone (`icon--flip-rtl`), il chevron
di «← Site public», la posizione del chevron del `<select>`, l'origine della linea d'ormeggio (via `--dir`). **Non** si
specchiano: il lock-up (`direction: ltr`, §8.1), i valori delle coordinate (`dir="ltr"`, §4.3), il valore del codice,
e-mail e password (già `dir="ltr"`), **e la carta** (EMENDAMENTO 4). `:lang(ar)`: `letter-spacing: 0` su eyebrow, folio,
legenda e contatore; `text-transform: none`; interlinea 1,8 nel corpo; `min-inline-size: 120px` sui bottoni; la
spaziatura del campo OTP **resta**, perché il valore è numerico latino.

**Reduced motion come stato completo** (`probe.json/doc_normal` vs `doc_reduced`, 1440×900):
altezza del documento **900 in entrambi i casi**; elementi a `opacity: 0` o `visibility: hidden` dentro `.atrium`:
**0 in entrambi i casi**; il marcatore ha 0 animazioni e riposa sulla soglia.
**Una differenza, dichiarata:** `innerText` misura 598 caratteri a moto normale e **574** a moto ridotto. La differenza
è esattamente l'etichetta di `.tide-toggle`, che `v2/hero.css:468-470` nasconde con `display: none` sotto
`prefers-reduced-motion: reduce` — regola già in produzione. Un controllo per mettere in pausa un moto che non esiste
non è contenuto: è interfaccia per il moto. Si dichiara perché il revisore ha ragione a chiedere che una differenza si
scriva invece di nascondersi.

**Forced colors** (`probe.json/forced_colors`, `shot_forced.png`). La graticola **non viene disegnata**: in modalità
forzata `GrayText` la rendeva rosso acceso e dominante, e §6 del sistema ammette «isoipse `GrayText` **o nascoste**».
Restano in `CanvasText` l'arco (`stroke` misurato `rgb(0,0,0)`), i gradini, la rotta, i due pallini e il marcatore; la
superficie dell'apertura diventa `Canvas`; la cucitura fra le due colonne diventa `border-inline-end: 1px solid
CanvasText`, perché senza di essa i due capitoli collassano entrambi su `Canvas`; il filetto del foglio diventa 3 px
`CanvasText`; i campi prendono `Field` / `FieldText` / `ButtonBorder` con `forced-color-adjust: none`; **le celle del
codice sono ridisegnate con `border-inline-end`**, perché il gradiente sparisce.

**Zoom.** A 200 % (720 px logici) e a 400 % (360 px logici): una colonna, `grid-template-columns` calcolato `720px` e
`360px`, **nessuno scorrimento orizzontale**.

### 6.6 HUMAN_QA_REQUIRED

1. Il titolo e il corpo dello stato «limite di tentativi» — affermazione pubblica, revisione legale prima della messa in
   opera.
2. Le due formulazioni del contatore di caratteri e i tre nomi accessibili nuovi (rivelazione, BLOC MAJ, codice
   completo).
3. `cms.forbidden.scan()` su tutte e dodici le schermate in quattro lingue, `alt`, `aria-label`, `title` e testi fuori
   schermo compresi. **Già eseguito su tre pagine prototipo renderizzate (login, iscrizione, codice): 0 violazioni.**
   Nota aggiunta su richiesta del revisore (MUST-FIX 12): `scan()` fa `re.search` di
   `google-analytics\.com|googletagmanager\.com|\bgtag\(`, `\bfbq\(`, `hotjar\.com`, `fonts\.googleapis\.com` sulla
   pagina **renderizzata** — quindi **nessun testo di questa superficie può nominare un tracciatore per dominio**,
   nemmeno per negarlo. È una delle ragioni per cui il blocco «nessun tracciatore» è cancellato e non riformulato.
4. La resa dell'arco a 200 % e 400 % sulla fascia di 120 px.
5. Il riempimento automatico dell'SMS nel campo codice su un Android reale, e NVDA/VoiceOver sul campo codice: **un**
   campo annunciato, non sei.
6. Percorso da tastiera sulle dodici schermate: la barra d'atrio non intrappola il fuoco, il commutatore di lingua
   resta un `<details>` nativo (Escape chiude, fuoco restituito).

---

## 7. FILE E TEMPLATE

**Quattro template, un file Python, due file nuovi. Nessuna vista, nessun contratto di dati, nessun componente
condiviso.**

| File | Natura | Che cosa cambia |
|---|---|---|
| `templates/base.html` | **modifica di una riga** | aggiunge `{% block body_data %}` all'apertura di `<body>` |
| `templates/allauth/layouts/entrance.html` | **riscritto** (3 righe → ~30) | la griglia dell'atrio |
| `templates/allauth/partials/_atrium_chrome.html` | **nuovo** | la barra, con le classi di `portal.css` |
| `templates/allauth/partials/_threshold.html` | **nuovo** | la tavola, l'apertura, la rotta, il glifo, la legenda |
| `templates/allauth/partials/_atrium_footer.html` | **nuovo** | il piè di pagina legale, due righe |
| `apps/accounts/forms.py` | **un attributo di widget** | `full_name` prende `autocomplete="name"` |
| `static/css/v3/auth.css` | **nuovo** | 16 511 byte grezzi · 11 734 minificati · **3 011 byte gzip** |
| `static/js/src/auth.js` → `dist/auth.js` | **nuovo** | 4 128 byte minificati · **1 622 byte gzip** |

**NON toccati, e questo è il punto:** `templates/allauth/layouts/base.html`, `templates/allauth/layouts/manage.html`,
`templates/allauth/elements/*` (le mappature esistono già e bastano: `h1.html` → `.account-page__title`, `p.html` →
`.account-page__text`, `form.html` → `.form` con il sommario, `fields.html` → `components/form_field.html`),
`templates/components/form_field.html`, `templates/components/form_errors.html`, `static/css/components.css`,
`static/css/main.css`, `apps/portal/static/portal/portal.css`.

`main.css` non cambia perché `auth.css` **non è un quindicesimo `@import` in catena**: è un `<link>` per pagina in
`{% block extra_head %}`, come `portal.css` in `templates/portal/base_portal.html:20` e come `helpdesk.css` in
`templates/helpdesk/base_helpdesk.html:11`. LACUNA 8 chiusa con un pattern già in produzione due volte.

### 7.1 `templates/base.html` — il gancio `data-mode` (diff esatto)

```diff
-<body class="{% block body_class %}{% endblock %}{% if site.is_rtl %} is-rtl{% endif %}">
+<body class="{% block body_class %}{% endblock %}{% if site.is_rtl %} is-rtl{% endif %}"{% block body_data %}{% endblock %}>
```

È additivo: ogni pagina che non sovrascrive il blocco rende esattamente il markup di oggi. §7 del sistema impone
`data-mode` a **ogni** template, quindi questo gancio serve a tutte le superfici, non solo a questa: **coordinamento
con `platform-shell.md`, che possiede `templates/base.html`.** Se `platform-shell.md` lo aggiunge per primo, questa
specifica non tocca `base.html` affatto. Nota di onestà: il test che §7 promette («un test lo verifica») **non esiste**
oggi — `grep -rn "data-mode" templates apps static tests` non restituisce nulla. La guardia è al §9 e va scritta.

### 7.2 `templates/allauth/layouts/entrance.html` (riscritto per intero)

```django
{% extends "allauth/layouts/base.html" %}{% load i18n static %}
{% comment %}
L'atrio — docs/design-v3/specs/auth.md.

Si sovrascrive `main_content`, non `body`: `body` vive DENTRO
`<section class="container account-page">`, e un contenitore con max-width non può portare una
griglia a tutta altezza. `manage.html` continua a usare quella sezione e non cambia di una riga.

`{% block account_help %}` di allauth/layouts/base.html non viene reso qui; il suo testo e il suo
mailto sono ri-resi in fondo al foglio, parola per parola.

La barra e il piè di pagina sono BLOCCHI di templates/base.html, non include fissi: qui l'entrata
prende la barra della piattaforma (§84) e un piè di pagina legale completo.
{% endcomment %}
{% block body_class %}page-account page-atrium{% endblock %}
{% block body_data %} data-mode="rich"{% endblock %}

{% block extra_head %}
<link rel="stylesheet" href="{% static 'portal/portal.css' %}">
<link rel="stylesheet" href="{% static 'css/v3/auth.css' %}">
{# Fira Mono è dichiarato font-display: swap; senza precarico il campo codice cambia larghezza. #}
<link rel="preload" href="{% static 'fonts/fira-mono-400-normal-latin.woff2' %}" as="font" type="font/woff2" crossorigin>
{% endblock %}

{% block chrome %}{% include "allauth/partials/_atrium_chrome.html" %}{% endblock %}
{% block site_footer %}{% include "allauth/partials/_atrium_footer.html" %}{% endblock %}

{% block main_content %}
<div class="atrium" data-atrium
     data-label-show="{% translate 'Afficher le mot de passe' %}"
     data-label-hide="{% translate 'Masquer le mot de passe' %}"
     data-label-caps="{% translate 'Verrouillage des majuscules activé' %}"
     data-label-count-short="{% translate 'Il manque {n} caractères.' %}"
     data-label-count-done="{% translate 'Longueur minimale atteinte.' %}"
     data-label-otp-complete="{% translate 'Code complet.' %}"
     data-label-busy="{% translate 'Vérification en cours…' %}">
  {% include "allauth/partials/_threshold.html" %}
  <div class="atrium__sheet">
    <div class="sheet__inner">
      <p class="sheet__eyebrow">{% translate "Espace réservé" %}</p>
      {% block content %}{% endblock content %}
      <p class="account-page__text sheet__help">{% translate "Besoin d’aide ? Écrivez-nous :" %}
        <a class="email" href="mailto:{{ site.contact_email }}">{{ site.contact_email }}</a></p>
    </div>
  </div>
</div>
{% endblock main_content %}

{% block extra_scripts %}{{ block.super }}
<script type="module" src="{% static 'js/dist/auth.js' %}"></script>{% endblock %}
```

Le dodici schermate che ereditano questo layout, verificate nel pacchetto installato
(`grep -rl "base_entrance.html" .venv/…/allauth/templates/{account,mfa}`): `account/login`, `account/signup`,
`account/signup_closed`, `account/password_reset`, `account/password_reset_done`, `account/password_reset_from_key`,
`account/password_reset_from_key_done`, `account/email_confirm`, `account/verification_sent`,
`account/base_confirm_code` (codice di verifica e-mail), `account/base_reauthenticate`, `account/account_inactive`,
`mfa/authenticate`, `mfa/trust`. Nessuna riceve né richiede contesto nuovo.

### 7.3 `templates/allauth/partials/_atrium_footer.html` (nuovo) — MUST-FIX 1

Confronto riga per riga con `templates/partials/footer.html`, **nulla è eliminato in silenzio**:

| Voce del piè pubblico | Nel piè d'atrio |
|---|---|
| Mentions légales · Privacy Policy · Cookie Policy · Conditions d'utilisation · Avertissement | **sì, tutte e cinque** |
| link antifrode, con `gates.phase3_public` e `{% locked "p3.antifraud.title" %}` | **sì, verbatim, con il gate** |
| promotore, ©, etichetta di versione, data di verifica dei contenuti | **sì, seconda riga** |
| lock-up variante scura | **no** — sta nella barra, a 71 px di distanza (EMENDAMENTO 3) |
| `{% brand_words %}` («marque déposée») | **no** — è una menzione di marchio, e sta nel piè pubblico dove sta il lock-up |
| navigazione del sito (7 sezioni) + «Le projet» | **no** — a chi sta firmando l'accesso non si offrono sette vie d'uscita (è il punto 13 dell'audit) |

```django
{% load i18n ile_core %}{% comment %}
Il piè dell'atrio. NON è la riga a tre voci del round 1: il consenso di `accept_terms`
(apps/accounts/forms.py:31, CONTENT_PENDING_LEGAL_REVIEW, §3.8.7/§3.10) nomina la Privacy Policy e
le Conditions d’utilisation per titolo, e una pagina non può chiedere di accettare due documenti
che non linka. Il testo antifrode è BLOCCATO e il suo gate di pubblicazione è quello del piè
pubblico, copiato carattere per carattere.
{% endcomment %}
<footer class="atrium-footer">
  <div class="atrium-footer__inner">
    <p class="atrium-footer__legal">
      <a href="{% url 'legal:notices' %}">{% translate "Mentions légales" %}</a>
      <a href="{% url 'legal:privacy' %}">Privacy Policy</a>
      <a href="{% url 'legal:cookies' %}">Cookie Policy</a>
      <a href="{% url 'legal:terms' %}">{% translate "Conditions d’utilisation" %}</a>
      <a href="{% url 'legal:disclaimer' %}">{% translate "Avertissement" %}</a>
      {% if gates.phase3_public %}{% safe_url 'pages:antifraud' as antifraud_url %}{% if antifraud_url %}<a href="{{ antifraud_url }}">{% locked "p3.antifraud.title" %}</a>{% endif %}{% endif %}
    </p>
    <p class="atrium-footer__colophon">
      {{ site.promoter }} · © {% now "Y" %} · {{ site.version_label }}{% if site.content_verified_on %}
      — {% translate "contenus vérifiés le" %} <time datetime="{{ site.content_verified_on|date:'Y-m-d' }}">{{ site.content_verified_on|date:"d.m.Y" }}</time>{% endif %}
    </p>
  </div>
</footer>
```

Misurato: **56 px** a 1440 (una riga), **84 px** da 768 a 1280 (due righe), **128 px** a 390. Link a
`--accent-dark` su `--mid-0` = 10,57:1, altezza di ogni link **24 px** (2.5.8).

### 7.4 `templates/allauth/partials/_atrium_chrome.html` (nuovo)

Le classi vengono da `portal.css`; **nessuna regola nuova**, quindi le due barre non possono divergere per costruzione.
Rispetto a `partials/portal_chrome.html` cadono il contesto del fascicolo e il menu del conto, che senza sessione non
hanno dati: è la ragione misurata per cui le due barre non hanno la stessa altezza sotto 768 (disputa D1).

```django
{% load i18n cms_nav %}
<div class="portal-bar">
  <div class="portal-bar__inner">
    <a class="portal-bar__brand" href="{% url 'pages:home' %}">{% brand "portal-bar__wordmark" %}</a>
    <nav class="portal-bar__account" aria-label="{% translate 'Langue et site public' %}">
      <a class="portal-bar__link" href="{% url 'pages:home' %}">{% svg_icon "chevron-start" "icon icon--sm icon--flip-rtl" %}{% translate "Site public" %}</a>
      {% include "components/language_switcher.html" %}
    </nav>
  </div>
</div>
```

### 7.5 `templates/allauth/partials/_threshold.html` (nuovo)

Due `<svg>` per la tavola (vedi §4.3 per la ragione misurata), un terzo `<svg>` per il glifo sotto 1024, la legenda.
Tutte e tre `aria-hidden="true" focusable="false"`: sono disegno, e il loro contenuto informativo — i due luoghi — è
nella legenda, in testo.

**I numeri della tavola sono riproducibili, non copiati.** Diciotto righe di Python li rigenerano; se la finestra
geografica cambia, si rigenerano e basta — nessuno li ritocca a mano.

```python
import math
W, H = 800.0, 900.0
LON0, LON1, LAT0, LAT1 = -12.0, 18.0, 30.0, 49.0
merc = lambda lat: math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))
Y0, Y1 = merc(LAT0), merc(LAT1)
X = lambda lon: (lon - LON0) / (LON1 - LON0) * W
Y = lambda lat: H - (merc(lat) - Y0) / (Y1 - Y0) * H

meridians = " ".join(f"M{X(lo):.1f} 0V{H:.0f}" for lo in range(-10, 16, 5))
parallels = " ".join(f"M0 {Y(la):.1f}H{W:.0f}" for la in range(32, 49, 2))
ticks = " ".join(f"M{X(lo)-4:.1f} {Y(la):.1f}h8M{X(lo):.1f} {Y(la)-4:.1f}v8"      # 30 croci
                 for lo in range(-10, 16, 5) for la in range(32, 49, 4))
shores = (X(-6.85), Y(33.97)), (X(11.88), Y(45.41))       # Maroc, Vénétie
route = "M{:.1f} {:.1f} L{:.1f} {:.1f}".format(*shores[0], *shores[1])
```

Eseguito, questo riproduce i path del partial carattere per carattere, salvo gli zeri finali (`320.0` contro `320` su
due meridiani): geometricamente identici. `route` restituisce `M137.3 730.7 L636.8 191.1`, che è la rotta scritta sopra.

```html
<div class="atrium__threshold">
  <svg class="threshold__route" viewBox="0 0 800 900" preserveAspectRatio="xMidYMax slice" aria-hidden="true" focusable="false">
    <path class="route__line" pathLength="1" d="M137.3 730.7 L636.8 191.1"/>
    <circle class="route__shore" cx="137.3" cy="730.7" r="4"/>
    <circle class="route__shore" cx="636.8" cy="191.1" r="4"/>
    <circle class="route__watch" cx="137.3" cy="730.7" r="3.5"/>
  </svg>
  <svg class="threshold__chart" viewBox="0 0 800 900" preserveAspectRatio="xMidYMax slice" aria-hidden="true" focusable="false">
    <defs>
      <g id="atr-grat">
        <path class="grat__mer" d="M53.3 0V900 M186.7 0V900 M320 0V900 M453.3 0V900 M586.7 0V900 M720 0V900"/>
        <path class="grat__par" d="M0 815.6H800 M0 729.4H800 M0 641.1H800 M0 550.6H800 M0 457.6H800 M0 361.7H800 M0 262.9H800 M0 160.6H800 M0 54.6H800"/>
        <path class="grat__tick"
              d="M49.3 815.6h8M53.3 811.6v8 M49.3 641.1h8M53.3 637.1v8 M49.3 457.6h8M53.3 453.6v8 M49.3 262.9h8M53.3
           258.9v8 M49.3 54.6h8M53.3 50.6v8 M182.7 815.6h8M186.7 811.6v8 M182.7 641.1h8M186.7 637.1v8 M182.7
           457.6h8M186.7 453.6v8 M182.7 262.9h8M186.7 258.9v8 M182.7 54.6h8M186.7 50.6v8 M316 815.6h8M320 811.6v8
           M316 641.1h8M320 637.1v8 M316 457.6h8M320 453.6v8 M316 262.9h8M320 258.9v8 M316 54.6h8M320 50.6v8 M449.3
           815.6h8M453.3 811.6v8 M449.3 641.1h8M453.3 637.1v8 M449.3 457.6h8M453.3 453.6v8 M449.3 262.9h8M453.3
           258.9v8 M449.3 54.6h8M453.3 50.6v8 M582.7 815.6h8M586.7 811.6v8 M582.7 641.1h8M586.7 637.1v8 M582.7
           457.6h8M586.7 453.6v8 M582.7 262.9h8M586.7 258.9v8 M582.7 54.6h8M586.7 50.6v8 M716 815.6h8M720 811.6v8
           M716 641.1h8M720 637.1v8 M716 457.6h8M720 453.6v8 M716 262.9h8M720 258.9v8 M716 54.6h8M720 50.6v8"/>
      </g>
      <clipPath id="atr-aperture"><path d="M248 700V460A144 144 0 0 1 536 460V700Z"/></clipPath>
    </defs>
    <use href="#atr-grat"/>
    <path class="arch__ground" d="M248 700V460A144 144 0 0 1 536 460V700Z"/>
    <g class="grat--lit" clip-path="url(#atr-aperture)"><use href="#atr-grat"/></g>
    <path class="arch__line" pathLength="1" d="M248 700V460A144 144 0 0 1 536 460V700"/>
    <rect class="arch__step arch__step--1" x="332" y="706" width="120" height="10"/>
    <rect class="arch__step arch__step--2" x="320" y="720" width="144" height="10"/>
    <rect class="arch__step arch__step--3" x="308" y="734" width="168" height="10"/>
  </svg>
  <svg class="threshold__glyph" viewBox="0 0 72 104" aria-hidden="true" focusable="false">
    <path class="arch__ground" d="M9 80V35A27 27 0 0 1 63 35V80Z"/>
    <path class="arch__line" pathLength="1" d="M9 80V35A27 27 0 0 1 63 35V80"/>
    <rect class="arch__step arch__step--1" x="19" y="84" width="34" height="4"/>
    <rect class="arch__step arch__step--2" x="15" y="91" width="42" height="4"/>
    <rect class="arch__step arch__step--3" x="11" y="98" width="50" height="4"/>
  </svg>
  <p class="threshold__folio">Projection de Mercator <span dir="ltr">· 30°–49° N · 12° O – 18° E</span></p>
  <div class="threshold__legend">
    <p class="coord"><span class="coord__dot" aria-hidden="true"></span><strong>Maroc</strong> <span dir="ltr">33.97° N · 6.85° W</span></p>
    <button class="tide-toggle" type="button" data-atrium-pause aria-pressed="false"
            data-label-pause="Suspendre le mouvement" data-label-resume="Reprendre le mouvement">
      <svg class="icon icon--pause" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2"><path d="M8 5v14M16 5v14"/></svg>
      <svg class="icon icon--play" viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M7 5l12 7-12 7z"/></svg>
      <span data-atrium-pause-label>Suspendre le mouvement</span>
    </button>
    <p class="coord"><span class="coord__dot" aria-hidden="true"></span><strong>Vénétie</strong> <span dir="ltr">45.41° N · 11.88° E</span></p>
  </div>
</div>
```

(I testi francesi passano da `{% translate %}` come ovunque; sono scritti in chiaro qui per leggibilità.)

### 7.6 `apps/accounts/forms.py` — un attributo (WCAG 1.3.5)

L'audit, punto 14: `autocomplete` di `full_name` è `null`. È un attributo di widget, non una regola di prodotto:

```diff
-    full_name = forms.CharField(label=_("Nome e cognome"), max_length=160)
+    full_name = forms.CharField(
+        label=_("Nome e cognome"),
+        max_length=160,
+        widget=forms.TextInput(attrs={"autocomplete": "name"}),
+    )
```

Nessuna etichetta, nessuna validazione, nessun ruolo, nessun consenso cambia.

### 7.7 Selettori

`.atrium`, `.atrium__{threshold,sheet}`, `.threshold__{chart,route,glyph,folio,legend}`,
`.grat__{mer,par,tick}`, `.grat--lit`, `.arch__{ground,line,step}`, `.route__{line,shore,watch}`,
`.sheet__{inner,eyebrow,help}`, `.atrium-footer{,__inner,__legal,__colophon}`,
`.form-field__{control,reveal,caps,count}`, `.btn__rule`,
`.page-atrium`, e `.atrium` come prefisso per tutto ciò che corregge `components.css`.
Riusati senza una riga nuova: `.portal-bar*` (da `portal.css`), `.coord`, `.coord__dot`, `.tide-toggle`
(da `v2/hero.css`), `.form-field*`, `.form-errors`, `.btn--primary`, `.account-page__{title,text}`.
Verificato libero da collisioni: nessuno dei nuovi nomi esiste in `static/` o `apps/*/static/` (§1.7, N1).

---

## 8. PRESTAZIONI

**Oggi sulla pagina di login, rimisurato** (gzip -9 sui file realmente serviti):
`head.js` 206 B · `main.js` 5 293 B · `dist/shell.js` 613 B · `dist/chunks/chunk-P4EHGXV4.js` **26 120 B** =
**32 232 B = 31,48 KiB**. Il chunk di Motion è già scaricato e **non serve a nulla su questa pagina**.

| Voce aggiunta | Grezzo | gzip |
|---|---:|---:|
| `static/css/v3/auth.css` (minificato con esbuild 0.28.2) | 11 734 B | **3 011 B** |
| `apps/portal/static/portal/portal.css` (già esistente, ora caricato anche qui) | 24 115 B | **6 615 B** |
| `static/js/dist/auth.js` (bundle esbuild 0.28.2, `splitting: true`) | 4 128 B | **1 622 B** |
| chunk di Motion | — | **+0** — è già lì, e `auth.js` non importa nessun export che `shell.js` non importi già (`animate`, `stagger`, `withMotion`) |
| SVG della soglia, inline nel partial | 3 935 B | **1 240 B** |
| Immagini | **0** | **0** su un budget di 120 KB per viewport |

**Totale JS: 33 854 B = 33,06 KiB**, cioè **11,9 KiB sotto il budget di 45 KB** — e per la prima volta il chunk di
Motion viene usato su questa pagina invece che soltanto scaricato.

Il costo onesto è `portal.css`: **6,46 KiB gzip per una barra**. Si accetta, con il numero scritto, perché l'alternativa
è duplicarne le regole e riaprire esattamente il rischio §84 che la disputa D1 chiude. La correzione strutturale —
estrarre il blocco `.portal-bar` (portal.css righe 20–100) in un foglio proprio caricato da entrambe le superfici —
**appartiene a `platform-shell.md`**, che possiede quel file; questa specifica non la esegue e non la chiede come
condizione.

**Paint e layout.** Solo `transform`, `opacity` e `stroke-dashoffset`; nessun `filter`, nessuna animazione di
`box-shadow`, `width`, `height`, `top`/`left`. Tre `linear-gradient`/`repeating-linear-gradient` in tutto il foglio, ed
è l'elenco completo: le celle del campo codice; e nessun altro — `radial-gradient` non compare. `contain: layout paint`
solo su `.atrium__threshold`. `will-change: transform` sul solo marcatore. L'arco è **un** path `pathLength="1"`.
Prova d'accettazione eseguita: 181 frame durante AMB, mediana 16,7 ms, **0 frame oltre 20 ms**.

---

## 9. RISCHI E GUARDIE

Le guardie del round 1 citavano `tests/frontend/test_motion_system.py`, che **non esiste**
(`ls tests/frontend/` → `test_browser · test_cms_nav · test_css_tokens_exist · test_design_docs · test_favicon ·
test_frontend_bundle_is_current · test_header_fits_the_narrowest_viewport · test_layout · test_legacy_token_shim ·
test_static_assets · test_svg_wellformed · test_template_comments_do_not_leak`). LACUNA 11: ogni guardia qui sotto è
**o** un test che esiste oggi, **o** un test nuovo che questa specifica si impegna a scrivere, e lo dice.

| Rischio | Come diventerebbe «a buon mercato» | Guardia | Esiste? |
|---|---|---|---|
| Il pannello scuro come cartolina | Mezzanotte + una frase centrata | Il test del §1.5: coprire l'arco e vedere che resta una carta con una rotta e due luoghi nominati. E la guardia dura: **nessuna frase** sulla soglia che non sia un dato (legenda della proiezione, nomi e coordinate, etichetta del controllo di pausa) | revisione umana |
| Il gradiente arriva di soppiatto | «Manca profondità» → un blob radiale | `grep -E "radial-gradient|linear-gradient" static/css/v3/auth.css` deve restituire **esattamente una** riga, le celle del codice | **nuovo test**, una riga |
| Un quinto ruolo di ombra | Un'ombra interna sul campo «per farlo sembrare vero» | `grep -c box-shadow static/css/v3/auth.css` = **5**, e sono quelle enumerate al §4.5; nessuna è un ruolo di superficie | **nuovo test** |
| Il tricolore rientra | Un token `--brand-*` per «dare carattere» | `grep -cE "var\(--brand-" static/css/v3/auth.css` = **0** (verificato) | **nuovo test** |
| L'ingresso diventa un carosello | A3 esteso a ogni nodo | Il limite sta nel codice: `.slice(0, 6)` in `auth.js` | codice |
| Un secondo oggetto vivo | «Anche il foglio potrebbe respirare» | `grep -c "animation:" static/css/v3/auth.css` = **1** e `grep -c "@keyframes"` = **1** (verificati). Ogni altra animazione è in `auth.js`, una tantum, mai `infinite` | **nuovo test** |
| Numeri di moto inventati | 90 ms, 350 ms, 600 ms | I soli letterali temporali ammessi in `auth.js` sono `0.9`, `0.24`, `0.05` e `0.4` (throttle `aria-live`); tutto il resto è `var(--motion-*)` | **nuovo test**, e sarebbe la prima parte di `test_motion_system.py` |
| La barra d'atrio diverge da quella del portale | Due file, due valori, §84 si rompe in silenzio | **Non un confronto di altezze** (disputa D1: non sono uguali e non possono esserlo), ma un test statico: `_atrium_chrome.html` non deve contenere nessuna classe che non esista in `portal.css`, e `auth.css` non deve dichiarare nessuna regola il cui selettore contenga `.portal-bar` all'infuori di `.page-atrium .portal-bar { position: static }` | **nuovo test** |
| Il campo OTP torna a sei input | In un mockup statico sembra più premium | La motivazione al §4.7 + la misura (cella 26,4 px = avanzamento) + la prova NVDA obbligatoria prima della fusione | §6.6 |
| Le parole vietate rientrano dalla porta di servizio | Una tagline sotto il marchio, uno slogan sotto l'arco, o la sua traduzione francese | `apps/pages/tests/test_institutional.py` gira già `cms.forbidden` su ogni pagina pubblica in ogni lingua; esteso alle dodici schermate d'atrio | **esiste**, da estendere |
| `data-mode` senza test | §7 dice «un test lo verifica» e il test non c'è | Un test che asserisce `data-mode` su ogni template di pagina; comincia dall'atrio | **nuovo test**, dovuto a `platform-shell.md` |
| Collisione con la superficie «bottoni» | Due riscritture di `.btn` nello stesso rilascio | Tutto è scoped a `.atrium`, `components.css` non si tocca, e `v3/buttons.css` resta la sola sede di `.btn--primary`. Alla fusione, le regole d'atrio si cancellano se quelle globali le coprono | revisione di merge |
| La casella di consenso resta navy altrove | Si corregge qui e si dimentica il prodotto | §1.7 N2 è **segnalato** alla superficie dei moduli con il numero di riga; questa specifica corregge solo il caso `.atrium` | segnalazione scritta |


---

## APPENDICE A — `static/css/v3/auth.css`, per intero

```css
/* ============================================================================
   ATRIUM V3 — «l'atrio» · docs/design-v3/specs/auth.md
   DESIGN_SYSTEM_V2.md §1.3, §2, §8.8, §9.2, §10 · MOTION_SYSTEM.md §0-§5

   Loaded as a per-page <link> from allauth/layouts/entrance.html, after main.css
   and after portal.css — never as a 15th serial @import.

   Namespace: `.atrium`, NOT `.entrance`. components.css:1390 already owns
   `.entrance` for the home page's four access ways, gap and padding included.

   Every selector that corrects components.css repeats its :not() chain: the
   project's own field selector is (0,4,1) and a plain `.atrium .form-field
   input:focus-visible` is (0,3,1) — it loses, and the focus ring vanishes.
   Measured, not assumed.
   ========================================================================== */
:root {
  --sheet-measure: 27rem;
  --field-h: 48px;
  --field-rule: 2px;
  --dir: 1;
}
[dir="rtl"] { --dir: -1; }

.page-atrium { background: var(--min-0); }
body.page-atrium { min-block-size: 100svh; display: grid; grid-template-rows: auto 1fr auto; }
/* ONE scroll container on this surface: the document. The sheet has no scroll of its own, so an
   error-summary link, find-in-page and the keyboard all move the same thing — and the bar does not
   stick, so nothing needs scroll-padding to clear it. */
.page-atrium .portal-bar { position: static; }
body.page-atrium > .skip-link { position: absolute; }
.page-atrium #main-content { display: flex; flex-direction: column; min-block-size: 0; }
.page-atrium .messages { flex: none; }

.atrium {
  flex: 1 1 auto;
  min-block-size: 0;
  display: grid;
  grid-template-columns: minmax(0, 54fr) minmax(29rem, 46fr);
}

/* ---- the threshold ------------------------------------------------------- */
.atrium__threshold {
  position: relative;
  isolation: isolate;
  overflow: clip;
  background: var(--mid-1);
  color: var(--on-dark);
  display: grid;
  grid-template-rows: auto 1fr;
  padding: var(--s-8) var(--s-10);
  contain: layout paint;
}
.threshold__glyph { display: none; }
.threshold__chart,
.threshold__route { position: absolute; inset: 0; inline-size: 100%; block-size: 100%; z-index: -1; pointer-events: none; }
.grat__mer, .grat__par { fill: none; stroke: var(--on-dark); stroke-opacity: .09; stroke-width: 1; vector-effect: non-scaling-stroke; }
.grat__tick { fill: none; stroke: var(--on-dark); stroke-opacity: .22; stroke-width: 1; vector-effect: non-scaling-stroke; }
.grat--lit .grat__mer, .grat--lit .grat__par { stroke: var(--terr-line); stroke-opacity: .55; }
.grat--lit .grat__tick { stroke: var(--terr-line); stroke-opacity: .85; }
.arch__ground { fill: var(--mid-2); }
.arch__line { fill: none; stroke: var(--accent-dark); stroke-width: 1.5; vector-effect: non-scaling-stroke; }
.arch__step { fill: var(--accent-dark); }
.arch__step--1 { fill-opacity: .90; }
.arch__step--2 { fill-opacity: .62; }
.arch__step--3 { fill-opacity: .40; }
.route__line { fill: none; stroke: var(--accent-dark); stroke-opacity: .55; stroke-width: 1.5; vector-effect: non-scaling-stroke; }
.route__shore { fill: var(--accent-dark); }
.route__watch { fill: var(--accent-dark); }

@media (prefers-reduced-motion: no-preference) {
  .route__watch { animation: atrium-watch var(--motion-ambient) linear infinite; will-change: transform; }
  .atrium.is-offscreen .route__watch,
  .atrium.is-paused .route__watch { animation-play-state: paused; }
}
@media (prefers-reduced-motion: reduce) {
  /* t = 0.20 of the rhumb line: on the threshold, just outside the leading jamb. Visible, still. */
  .route__watch { transform: translate3d(99.9px, -107.9px, 0); }
  /* components.css:2221 transitions the field's border and shadow OUTSIDE a reduced-motion guard
     — a pre-existing global defect. MOTION_SYSTEM §3 says every transition lives inside
     `no-preference`. Neutralised here for this surface; the global case belongs to the forms
     surface, with the line number. */
  .atrium .form-field input,
  .atrium .form-field select,
  .atrium .form-field textarea,
  .atrium .btn { transition: none; }
}
@keyframes atrium-watch {
  0%   { transform: translate3d(0,0,0); opacity: 0; }
  6%   { opacity: 1; }
  88%  { opacity: 1; }
  100% { transform: translate3d(499.5px, -539.6px, 0); opacity: 0; }
}

.threshold__folio {
  margin: 0; font-family: var(--f-mono); font-size: var(--t-folio); line-height: var(--t-folio-lh);
  letter-spacing: var(--track-folio); text-transform: uppercase; color: var(--on-dark-3);
}
.threshold__legend {
  align-self: end;
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: end;
  gap: var(--s-2) var(--s-4);
  padding-block-start: var(--s-4);
  border-block-start: 1px solid var(--hairline-dark);
  font-family: var(--f-mono); font-size: var(--t-folio); line-height: var(--t-folio-lh);
  letter-spacing: var(--track-folio); text-transform: uppercase; color: var(--on-dark-3);
}
.threshold__legend p { margin: 0; grid-column: 1; }
.threshold__legend .tide-toggle { grid-column: 2; grid-row: 1 / span 2; align-self: end; }
/* The label is a word below 75rem, where the column is too narrow to carry it. The accessible
   name does not change: the span stays in the DOM, off screen. */
@media (max-width: 74.999rem) {
  .threshold__legend .tide-toggle [data-atrium-pause-label] {
    position: absolute; inline-size: 1px; block-size: 1px;
    margin: -1px; padding: 0; overflow: hidden; clip-path: inset(50%); white-space: nowrap;
  }
  .threshold__legend .tide-toggle { min-inline-size: 44px; min-block-size: 32px; justify-content: center; }
}

/* ---- the sheet ----------------------------------------------------------- */
.atrium__sheet {
  background: var(--min-2);
  color: var(--ink);
  border-inline-start: 3px solid var(--accent);
  display: grid;
  align-content: center;
  justify-items: center;
  padding: var(--s-12) var(--s-10);
}
.sheet__inner { inline-size: 100%; max-inline-size: var(--sheet-measure); }
.sheet__eyebrow { margin: 0 0 var(--s-4); font-family: var(--f-mono); font-size: var(--t-folio); line-height: var(--t-folio-lh); letter-spacing: var(--track-folio); text-transform: uppercase; color: var(--ink-3); }
.atrium .account-page__title { font-family: var(--f-serif); font-size: var(--t-title); line-height: var(--t-title-lh); font-weight: 400; margin: 0 0 var(--s-4); letter-spacing: var(--track-display); }
.atrium .account-page__text { font-size: var(--t-body); line-height: var(--t-body-lh); color: var(--ink-2); margin: 0 0 var(--s-8); }
.atrium .account-page__text a { color: var(--accent); }

/* ---- fields --------------------------------------------------------------- */
.atrium .form-field { margin-block-end: var(--s-6); scroll-margin-block-start: var(--s-6); }
.atrium .form-errors { scroll-margin-block-start: var(--s-6); }
.atrium .form-field__label { font-family: var(--f-sans); font-size: var(--t-ui); line-height: var(--t-ui-lh); font-weight: 500; color: var(--ink); margin-block-end: var(--s-2); }
.atrium .form-field input:not([type="checkbox"]):not([type="radio"]):not([type="file"]),
.atrium .form-field select {
  block-size: var(--field-h);
  min-block-size: var(--field-h);
  background: var(--min-3);
  color: var(--ink);
  border: 1px solid var(--hairline-strong);
  border-block-end-width: var(--field-rule);
  border-radius: var(--radius-control);
  padding-block: 0;
  padding-inline: var(--s-4);
  font-family: var(--f-sans);
  font-size: var(--t-body);
  line-height: normal;
  box-shadow: none;
}
.atrium .form-field select {
  appearance: none;
  padding-inline-end: calc(var(--s-4) * 2 + 20px);
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20' fill='none' stroke='%2315222A' stroke-width='1.5' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M5 8l5 5 5-5'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right var(--s-4) center;
  background-size: 20px 20px;
}
[dir="rtl"] .atrium .form-field select { background-position: left var(--s-4) center; }
.atrium .form-field input[type="password"]:not([type="checkbox"]):not([type="radio"]) { padding-inline-end: 52px; }
.atrium .form-field__help { font-size: var(--t-small); line-height: var(--t-small-lh); color: var(--ink-2); margin: var(--s-2) 0 0; max-inline-size: none; }
.atrium .form-field__help a { color: var(--accent); display: inline-block; min-block-size: 24px; line-height: 24px; }
.atrium .form-field__help ul { margin: var(--s-2) 0 0; padding-inline-start: var(--s-5); }

@media (hover: hover) {
  .atrium .form-field input:not([type="checkbox"]):not([type="radio"]):hover,
  .atrium .form-field select:hover { border-color: var(--ink-2); }
}
.atrium .form-field input:not([type="checkbox"]):not([type="radio"]):focus-visible,
.atrium .form-field select:focus-visible {
  outline: 2px solid var(--accent-ring);
  outline-offset: 2px;
  box-shadow: 0 0 0 5px rgba(29,138,147,.30);
  border-block-end-color: var(--accent);
}
.atrium .form-field input:not([type="checkbox"]):not([type="radio"]):-webkit-autofill,
.atrium .form-field input:not([type="checkbox"]):not([type="radio"]):-webkit-autofill:hover,
.atrium .form-field input:not([type="checkbox"]):not([type="radio"]):autofill {
  -webkit-text-fill-color: var(--ink);
  caret-color: var(--ink);
  box-shadow: inset 0 0 0 100px var(--min-3);
  border-color: var(--hairline-strong);
  border-block-end-width: var(--field-rule);
}
.atrium .form-field input:not([type="checkbox"]):not([type="radio"]):-webkit-autofill:focus-visible,
.atrium .form-field input:not([type="checkbox"]):not([type="radio"]):autofill:focus-visible {
  box-shadow: inset 0 0 0 100px var(--min-3), 0 0 0 5px rgba(29,138,147,.30);
}
.atrium .form-field--error input:not([type="checkbox"]):not([type="radio"]),
.atrium .form-field--error select { border-color: var(--err-700); box-shadow: none; }
.atrium .form-field input:not([type="checkbox"]):not([type="radio"]):disabled,
.atrium .form-field select:disabled { background: var(--min-1); color: var(--ink-3); border-color: var(--hairline); }

/* The checked consent box takes the ONE interactive accent. components.css draws it from
   --color-primary-900, which _legacy-tokens.css points at --navy and bridge.css at the mark's own
   navy, on the control that records a GDPR consent. Same defect, same fix as v3/buttons.css.
   Scoped here; the global case belongs to the forms surface. */
.atrium .form-field input[type="checkbox"] { accent-color: var(--accent); }
.atrium .form-field--consent .form-field__check {
  background: var(--min-1);
  border: 1px solid var(--hairline-strong);
  padding: var(--s-4);
}

/* ---- reveal / caps / counter ---------------------------------------------- */
.form-field__control { position: relative; display: block; }
.form-field__reveal {
  position: absolute; inset-block-start: 50%; inset-inline-end: 2px; translate: 0 -50%;
  inline-size: 44px; block-size: 44px; display: grid; place-items: center;
  background: none; border: 0; color: var(--ink-2); cursor: pointer; border-radius: var(--radius-control);
}
.form-field__reveal:focus-visible { outline: 2px solid var(--accent-ring); outline-offset: -2px; }
.form-field__caps, .form-field__count { font-size: var(--t-small); line-height: var(--t-small-lh); margin: var(--s-2) 0 0; color: var(--ink-2); }
.form-field__caps { color: var(--pending-700); }

/* ---- the action ----------------------------------------------------------- */
.atrium .form__actions { margin-block-start: var(--s-8); }
.atrium .form__actions .btn--primary {
  inline-size: 100%;
  min-block-size: 48px;
  display: inline-flex; align-items: center; justify-content: center; gap: var(--s-3);
  border-radius: var(--radius-control);
  font-family: var(--f-sans); font-size: var(--t-ui); font-weight: 500;
}
.btn__rule { inline-size: 16px; block-size: 1px; background: currentColor; transform: scaleX(0); transform-origin: calc(50% - var(--dir) * 50%) 50%; }
@media (prefers-reduced-motion: no-preference) {
  .btn__rule { transition: transform var(--motion-fast) var(--ease-out); }
}
.atrium .btn--primary:hover .btn__rule,
.atrium .btn--primary:focus-visible .btn__rule { transform: scaleX(1); }

/* ---- the OTP field --------------------------------------------------------- */
.atrium .form-field input[autocomplete="one-time-code"]:not([type="checkbox"]):not([type="radio"]) {
  block-size: 56px; min-block-size: 56px;
  font-family: var(--f-mono); font-variant-numeric: tabular-nums;
  font-size: 22px;
  /* Fira Mono advances exactly 0.6em per glyph (measured). Cell = glyph + one glyph of tracking. */
  --otp-glyph: .6em;
  --otp-cell: 1.2em;
  letter-spacing: var(--otp-glyph);
  text-align: start;
  direction: ltr;
  inline-size: calc(var(--otp-cell) * 6);
  padding-inline: calc(var(--otp-cell) / 2 - var(--otp-glyph) / 2) 0;
  margin-inline: auto;
  display: block;
  background-image: repeating-linear-gradient(90deg, transparent 0, transparent calc(var(--otp-cell) - 1px), var(--hairline-strong) calc(var(--otp-cell) - 1px), var(--hairline-strong) var(--otp-cell));
  background-repeat: no-repeat;
  background-size: calc(var(--otp-cell) * 6 - 1px) 100%;
  background-position: left top;
}

/* ---- the legal footer ------------------------------------------------------ */
.atrium-footer { background: var(--mid-0); color: var(--on-dark-2); }
.atrium-footer__inner { display: flex; flex-wrap: wrap; gap: var(--s-2) var(--s-6); align-items: baseline; padding: var(--s-4) var(--grid-margin); max-inline-size: var(--container); margin-inline: auto; }
.atrium-footer p { margin: 0; font-size: var(--t-small); line-height: var(--t-small-lh); }
.atrium-footer a { color: var(--accent-dark); min-block-size: 24px; display: inline-block; line-height: 24px; }

/* ---- 1024-1199: the split narrows; the plate still reads (measured at 1199 and 1024) ------- */
@media (min-width: 64rem) and (max-width: 74.999rem) {
  .atrium { grid-template-columns: minmax(0, 38fr) minmax(26rem, 62fr); }
  .atrium__threshold { padding: var(--s-6); }
  .atrium__sheet { padding: var(--s-10) var(--s-8); }
}

/* ---- below 1024: one column and the band of DESIGN_SYSTEM_V2 §8.8 ------------------------- */
/* Measured: below a 380px threshold column the 800x900 plate crops past the arch's trailing jamb
   and reads as a broken drawing. So the plate stops at 64rem and the grammar continues alone —
   the arch and its three steps, the glyph the system already uses for empty states (§6). */
@media (max-width: 63.999rem) {
  .atrium { grid-template-columns: 1fr; grid-template-rows: auto 1fr; }
  .atrium__threshold {
    display: flex; align-items: center; gap: var(--s-6);
    min-block-size: 120px; block-size: auto; padding: var(--s-4) var(--s-8);
  }
  .threshold__chart, .threshold__route, .threshold__folio { display: none; }
  .threshold__glyph { display: block; inline-size: 66px; block-size: 95px; flex: none; }
  .threshold__legend {
    border-block-start: 0; padding-block-start: 0;
    grid-template-columns: minmax(0, 1fr); margin-inline-start: auto;
  }
  .threshold__legend .tide-toggle { display: none; }
  .atrium__sheet {
    border-inline-start: 0; border-block-start: 3px solid var(--accent);
    padding: var(--s-10) var(--s-8); align-content: start;
  }
  .atrium .account-page__title { font-size: var(--t-band); line-height: var(--t-band-lh); }
}

/* ---- below 480: the folio is plate metadata for a plate that is not drawn -------------------- */
@media (max-width: 29.999rem) {
  .atrium__threshold { padding: var(--s-4); gap: var(--s-4); }
  .atrium__sheet { padding: var(--s-8) var(--s-4); }
}

/* ---- forced-colors: the drawing survives, the ground does not lie ----------- */
@media (forced-colors: active) {
  .atrium__threshold { border-inline-end: 1px solid CanvasText; }
  /* The graticule is texture, and texture in forced colours is noise: it is not drawn
     (DESIGN_SYSTEM_V2 §6 — «isoipse GrayText o nascoste»). The drawing that carries meaning —
     the arch, the steps, the route and its two shores — stays, in CanvasText. */
  .threshold__chart use, .grat--lit { display: none; }
  .arch__line, .route__line { stroke: CanvasText; stroke-opacity: 1; }
  .arch__step, .route__shore, .route__watch { fill: CanvasText; fill-opacity: 1; }
  .arch__ground { fill: Canvas; }
  .coord__dot { background: CanvasText; forced-color-adjust: none; }
  .atrium__sheet { border-inline-start: 3px solid CanvasText; }
  .atrium .form-field input:not([type="checkbox"]):not([type="radio"]):not([type="file"]),
  .atrium .form-field select { border-color: ButtonBorder; forced-color-adjust: none; background: Field; color: FieldText; }
  .atrium .form-field input[autocomplete="one-time-code"]:not([type="checkbox"]):not([type="radio"]) {
    background-image: none;
    border-inline-end: 1px solid ButtonBorder;
  }
  .atrium .form-field input:not([type="checkbox"]):not([type="radio"]):focus-visible { outline-color: Highlight; }
}
```

---

## APPENDICE B — `static/js/src/auth.js`, per intero

```js
/**
 * The atrium — docs/design-v3/specs/auth.md §5.
 *
 * Everything here enhances markup that already works without it: the form submits, the password is
 * typed, the code is pasted, the plate is drawn and complete on the first frame. No inline handler
 * and no inline style (CSP: script-src 'self'; style-src 'self'). No string is written here: every
 * word comes from `data-label-*` on [data-atrium], rendered and translated by the server.
 *
 * Function of each animation, per docs/design-v2/MOTION_SYSTEM.md §0:
 *   A1  arch traces        DELIGHT + ORIENTATION   900ms  --motion-draw
 *   A2  steps settle       HIERARCHY               240ms  --motion-base, stagger 50ms, CHAINED to A1
 *   A3  sheet arrives      HIERARCHY               240ms  --motion-base, stagger 50ms, <= 6 nodes
 *   A6  button waits       FEEDBACK                no duration: it lasts as long as the request
 *   A7  error summary      CAUSALITY               240ms  --motion-base
 *   AMB the watch          ORIENTATION             28s    --motion-ambient — in CSS, not here
 */
import { animate, stagger, withMotion } from "./motion.js";

const EASE_OUT = [0.25, 1, 0.5, 1];
const EASE_STANDARD = [0.4, 0, 0.2, 1];
const DRAW = 0.9;   // --motion-draw
const BASE = 0.24;  // --motion-base
const STEP = 0.05;  // stagger, inside MOTION_SYSTEM §1's 40-60ms band
const SAY_EVERY = 400; // ms between aria-live announcements — a policy, not an animation

const atrium = document.querySelector("[data-atrium]");
const qsa = (s, r = document) => Array.from(r.querySelectorAll(s));
const label = (name) => (atrium && atrium.dataset[name]) || "";

if (atrium) {
  /* ---- 1. The plate: the arch traces, then the three steps settle ------------------------- */
  {
    const arch = atrium.querySelector(".threshold__chart .arch__line");
    const steps = qsa(".threshold__chart .arch__step", atrium);
    const settle = () => {
      if (arch) arch.style.strokeDashoffset = "0";
      steps.forEach((s) => { s.style.opacity = ""; s.style.transform = ""; });
    };
    withMotion(() => {
      if (!arch) return settle();
      arch.style.strokeDasharray = "1";
      arch.style.strokeDashoffset = "1";
      arch.style.willChange = "stroke-dashoffset";
      animate(arch, { strokeDashoffset: [1, 0] }, { duration: DRAW, ease: EASE_OUT })
        .finished.then(() => {
          arch.style.willChange = "";
          // Chained, not delayed: A2 starts when A1 ends, so no new duration is invented.
          if (steps.length) {
            animate(steps,
              { opacity: [0, 1], transform: ["translateY(6px)", "translateY(0)"] },
              { duration: BASE, ease: EASE_OUT, delay: stagger(STEP) });
          }
        });
    }, settle);
  }

  /* ---- 2. The sheet arrives — at most six nodes, one stagger ------------------------------ */
  {
    const nodes = qsa(".sheet__inner > *, .sheet__inner .form > *", atrium).slice(0, 6);
    const settle = () => nodes.forEach((n) => { n.style.opacity = ""; n.style.transform = ""; });
    withMotion(() => {
      if (!nodes.length) return;
      animate(nodes,
        { opacity: [0, 1], transform: ["translateY(10px)", "translateY(0)"] },
        { duration: BASE, ease: EASE_OUT, delay: stagger(STEP) });
    }, settle);
  }

  /* ---- 3. The error summary: main.js already moves focus; this gives it a cause ----------- */
  {
    const summary = atrium.querySelector("#form-errors");
    if (summary) {
      withMotion(() => animate(summary,
        { opacity: [0, 1], transform: ["translateY(8px)", "translateY(0)"] },
        { duration: BASE, ease: EASE_STANDARD }), () => {});
    }
  }

  /* ---- 4. The ambient watch: paused off screen and on request ----------------------------- */
  {
    const pause = atrium.querySelector("[data-atrium-pause]");
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(
        ([e]) => atrium.classList.toggle("is-offscreen", !e.isIntersecting),
        { threshold: 0 },
      ).observe(atrium);
    }
    if (pause) {
      const text = pause.querySelector("[data-atrium-pause-label]");
      pause.addEventListener("click", () => {
        const paused = atrium.classList.toggle("is-paused");
        pause.setAttribute("aria-pressed", String(paused));
        if (text) text.textContent = pause.dataset[paused ? "labelResume" : "labelPause"];
      });
    }
  }

  /* ---- 5. Show / hide the password — the button is CREATED here -------------------------- */
  // It exists only where it works: without JavaScript there is no button that does nothing.
  const EYE = '<svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor"'
    + ' stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    + '<path d="M1 10s3.5-5 9-5 9 5 9 5-3.5 5-9 5-9-5-9-5Z"/><circle cx="10" cy="10" r="2.5"/></svg>';
  const EYE_OFF = '<svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor"'
    + ' stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    + '<path d="M1 10s3.5-5 9-5 9 5 9 5-3.5 5-9 5-9-5-9-5Z"/><path d="M3 17 17 3"/></svg>';

  for (const input of qsa('.form-field input[type="password"]', atrium)) {
    const wrap = document.createElement("span");
    wrap.className = "form-field__control";
    input.replaceWith(wrap);
    wrap.append(input);

    const button = document.createElement("button");
    button.type = "button";
    button.className = "form-field__reveal";
    button.setAttribute("aria-pressed", "false");
    button.setAttribute("aria-label", label("labelShow"));
    button.innerHTML = EYE;
    wrap.append(button);

    button.addEventListener("click", () => {
      const shown = input.type === "text";
      input.type = shown ? "password" : "text";
      button.setAttribute("aria-pressed", String(!shown));
      button.setAttribute("aria-label", label(shown ? "labelShow" : "labelHide"));
      button.innerHTML = shown ? EYE : EYE_OFF;
      input.focus({ preventScroll: true });
    });

    /* ---- 6. Caps lock — the warning is created here too --------------------------------- */
    const caps = document.createElement("p");
    caps.className = "form-field__caps";
    caps.setAttribute("role", "status");
    caps.hidden = true;
    caps.textContent = label("labelCaps");
    wrap.after(caps);
    const read = (e) => { caps.hidden = !(e.getModifierState && e.getModifierState("CapsLock")); };
    input.addEventListener("keyup", read);
    input.addEventListener("focus", read);
    input.addEventListener("blur", () => { caps.hidden = true; });
  }

  /* ---- 7. The one thing a browser can prove about a password: its length ------------------ */
  // Not a strength meter: a meter that reads "Solide" on a password CommonPasswordValidator then
  // rejects is a second, contradictory opinion. Only the length is computable here.
  for (const input of qsa('.form-field input[name="password1"]', atrium)) {
    const min = 12; // ACCOUNT_PASSWORD_MIN_LENGTH, config/settings/base.py:190
    const out = document.createElement("p");
    out.className = "form-field__count";
    out.setAttribute("role", "status");
    (input.closest(".form-field__control") || input).after(out);
    let queued = null;
    const say = () => {
      const n = input.value.length;
      out.textContent = n === 0 ? ""
        : n >= min ? label("labelCountDone")
        : label("labelCountShort").replace("{n}", String(min - n));
    };
    input.addEventListener("input", () => {
      clearTimeout(queued);
      queued = setTimeout(say, SAY_EVERY);
    });
  }

  /* ---- 8. The code field: six drawn cells, one value, one announcement -------------------- */
  for (const input of qsa('.form-field input[autocomplete="one-time-code"]', atrium)) {
    input.setAttribute("inputmode", "numeric");
    input.setAttribute("pattern", "[0-9]*");
    input.setAttribute("maxlength", "6");
    input.setAttribute("dir", "ltr");
    const status = document.createElement("p");
    status.className = "form-field__count";
    status.setAttribute("role", "status");
    input.after(status);
    input.addEventListener("input", () => {
      const cleaned = input.value.replace(/\D/g, "").slice(0, 6);
      if (cleaned !== input.value) input.value = cleaned;
      // Never blocks and never auto-submits: the server is the authority.
      status.textContent = cleaned.length === 6 ? label("labelOtpComplete") : "";
    });
  }

  /* ---- 9. The submit says it is working — a word, not a spinner --------------------------- */
  for (const form of qsa("form[data-single-submit]", atrium)) {
    form.addEventListener("submit", () => {
      const button = form.querySelector('[type="submit"]');
      if (!button) return;
      form.setAttribute("aria-busy", "true");
      const busy = label("labelBusy");
      const slot = button.querySelector("span:not(.btn__rule)");
      if (slot && busy) slot.textContent = busy;
    });
  }
}
```

---

## APPENDICE C — la matrice di misura

Tutte le cifre di questo documento vengono da `measures.json` e `probe.json`, prodotti in questa sessione da
`measure.py` e `probe.py` con il Chromium di Playwright in headless, lanciato da
`C:	mp\italylegalentry\.venv\Scripts\python.exe`. Metodo: si scarica la pagina reale di `:8771`, se ne riscrive una
**copia** con il markup dell'atrio, e la si serve alla stessa URL con `page.route()` — stesso origin, stessi font,
stesso `main.css`, stesso `portal.css`. Nessun file del repository è stato modificato per misurare.

| viewport | doc | scroll | soglia | foglio | misura | margine interno | barra | overflow orizz. |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1440 × 900 | 900 | **0** | 777,6 | 662,4 | 432 | 116,7 / 113,7 | 71 | no |
| 1280 × 800 | 800 | **0** | 691,2 | 588,8 | 432 | 79,9 / 76,9 | 71 | no |
| 1200 × 800 | 800 | **0** | 648,0 | 552,0 | 432 | 61,5 / 58,5 | 71 | no |
| 1199 × 800 | 800 | **0** | 455,6 | 743,4 | 432 | 157,2 / 154,2 | 71 | no |
| 1024 × 768 | 768 | **0** | 389,1 | 634,9 | 432 | 102,9 / 100,0 | 71 | no |
| 900 × 1200 | 1200 | **0** | fascia 127 | 900 | 432 | 234 / 234 | 71 | no |
| 768 × 1024 | 1024 | **0** | fascia 127 | 768 | 432 | 168 / 168 | 71 | no |
| 767 × 900 | 900 | **0** | fascia 127 | 767 | 432 | 167,5 / 167,5 | 71 | no |
| 390 × 844 | 938 | 94 | fascia 127 | 390 | 358 | 16 / 16 | 71 | no |
| 360 × 740 | 1014 | 274 | fascia 127 | 360 | 328 | 16 / 16 | 123 | no |

Iscrizione (il modulo più lungo, sei campi + consenso): documento 1266 a 1440 × 900 (scorrimento 366) · 1278 a
1024 × 768 · 1298 a 768 × 1024 · 1461 a 390 × 844. Nessuno scorrimento orizzontale, `sheetScrolls = false` ovunque.

Bersagli 2.5.8, misurati: «Mot de passe oublié ?» **121,14 × 24** · rivelazione **44 × 44** · consenso **24 × 24** ·
azione **432 × 48** (358 × 48 a 390) · pausa **234,77 × 32** sopra 75rem, **44 × 32** sotto.

Fuoco, misurato dopo 500 ms (prima si legge il valore interpolato della transizione di `components.css`):
`outline 2px`, `outline-offset 2px`, `box-shadow rgba(29,138,147,0.3) 0 0 0 5px`, `border-block-end-color
rgb(15,106,114)` = `--accent`. **Sporgenza 5 px.**

Moto, 1440 × 900, 3 s, 181 frame: mediana **16,7 ms**, p95 **16,7 ms**, massimo **16,8 ms**, **0 frame oltre 20 ms**.
Moto ridotto: `getAnimations().length === 0`, `opacity: 1`, `transform: matrix(1,0,0,1,99.9,-107.9)`, documento 900 px
in entrambi gli stati, **0** elementi a opacità 0 o nascosti in entrambi.

`auth.js`, compilato con esbuild e caricato nel prototipo: **0 errori di pagina, 0 errori di console**; i tre elementi
che crea (rivelazione, BLOC MAJ, contatore) esistono, hanno le misure e i testi previsti, e il contatore risponde alla
digitazione. `shot_js.png`.

`cms.forbidden.scan()` sulle tre pagine renderizzate (login, iscrizione, codice): **0 violazioni**.
`tests/frontend/test_css_tokens_exist.py`, regola applicata a mano ad `auth.css`: **nessuna proprietà personalizzata
indefinita**.
