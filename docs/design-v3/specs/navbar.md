# NAVBAR — SPECIFICA V3 · «IL FILO» (round 2)

Superficie: `templates/partials/{utility_bar,header,main_nav}.html` + `templates/components/language_switcher.html`
· `static/css/v2/shell.css` (blocchi navigazione/drawer/mega) + `static/css/components.css` §7
· `static/js/main.js` `initNavigation()` + nuovo `static/js/src/nav.js`.

Tutte le misure di questo documento sono state **rimisurate il 24/09/2026** nel Chromium headless di
Playwright del progetto (`.venv`, Chromium 153.0.8010.12), su `http://127.0.0.1:8771/` (fase 3 aperta,
sette voci) e `http://127.0.0.1:8770/` (fase 3 chiusa, quattro voci), in `fr it en ar`, a
1280 · 1366 · 1440 · 1536 · 1600 · 1920 × 900 e a 768×1024 · 390×844, DPR 1 e 2.
**Nessuna schermata è allegata a questa specifica e nessun nome di file PNG vi compare**: §2 pubblica
i numeri e la procedura che li riproduce (vedi la risposta al MUST-FIX 10).

---

## 0. RICHIESTE DI DEROGA (numerate, esplicite)

Tre sole. Ogni altra scelta di questo documento è conforme a `DESIGN_SYSTEM_V2.md` e
`MOTION_SYSTEM.md` alla lettera; dove il round 1 deviava senza dirlo, la deviazione è stata
**rimossa**, non sanata con una deroga (vedi §1).

### DEROGA 1 — `DESIGN_SYSTEM_V2.md` §8.2, riga 231
**Clausola.** «Barra `--min-1` 36 px: promotore, **«Espace réservé»**, lingue FR · IT · EN · ع come
segmenti (target ≥ 24 px).»
**Deroga richiesta.** «Espace réservé» **esce dalla barra istituzionale** ed entra nella riga
dell'header (≥ 48rem) e nel foglio del drawer (< 48rem). La barra conserva promotore e segmenti lingua.
**Motivo (misurato).** La barra non è `sticky`. A 1440, dopo `scrollTo(0,500)`, il rettangolo della
barra è `y = −900` (fuori dal documento visibile) mentre `.site-header` resta a `y = 0`: la porta della
piattaforma sparisce dopo il primo schermo e non torna più senza risalire. L'header è l'unico
elemento del cromo che accompagna il lettore per tutto il documento.
**Costo.** Un elemento prescritto per la barra cambia contenitore. Nessun elemento è soppresso,
nessun link duplicato, l'ordine DOM resta l'ordine di lettura. La barra perde 112,7 px di larghezza
occupata (misura attuale del link) e ne guadagna 0: i segmenti lingua (148 px) sostituiscono il
`<details>` (80,5 px) e restano ampiamente dentro lo spazio libero misurato (a 1280: riquadro 1096 px,
identità 405 px in inglese, il caso peggiore delle quattro lingue, segmenti 148 px → **543 px liberi**).

### DEROGA 2 — `DESIGN_SYSTEM_V2.md` §8.2, riga 232
**Clausola.** «Header `--min-2` 64 px: lock-up, otto voci, **CTA «Orientation» come bottone
secondario**.»
**Deroga richiesta.** L'header **non porta** la CTA «Orientation». La clausola è ritirata, non
ignorata.
**Motivo (misurato).** Un SECONDARY per §10 («bordo `--hairline-strong`, testo `--ink`») con
`padding-inline: 16px` e la spaziatura di riga `--s-6` costa `78,5 + 32 + 24 = 134,5 px` in FR/EN
(«Orientation» a `--t-ui` 15/500 misura **78,5 px**; «Orientamento» **95,0 px**, quindi 151,0 px in IT).
Il riquadro interno reale e il fabbisogno della riga (§4.4) danno:

| | 1280 | 1440 / 1536 | 1600 / 1920 |
|---|---:|---:|---:|
| riquadro interno disponibile | 1096,0 | 1240,0 | 1360,0 |
| riga senza CTA (FR) | 953,8 | 1218,8 | 1218,8 |
| riga **con** CTA (FR) | 1088,3 | **1353,3** | 1353,3 |
| margine con CTA (FR) | +7,7 | **−113,3** | +6,7 |
| margine con CTA (IT) | −9,5 | **−130,3** | +9,7 |

La CTA non entra a 1440–1599 in nessuna lingua, e a 1280 e 1600 entra con 7–10 px di margine, cioè
non entra: una singola parola più lunga in una traduzione futura la fa traboccare.
**Costo.** L'orientamento perde un ingresso permanente nel cromo. Dove resta raggiungibile **oggi,
senza che questa specifica tocchi la IA**: la CTA primaria dell'hero su HOME (misurata:
`«Découvrir le questionnaire d'orientation» → /fr/orientation/`) e la sezione `home-orientation`.
Se il Council vuole un ingresso permanente, l'unico posto con spazio misurato è la barra
istituzionale (543 px liberi a 1280): questa specifica **lascia quello slot libero** e non lo occupa.

### DEROGA 3 — `DESIGN_SYSTEM_V2.md` §2, livello 4
**Clausola.** «4 focus | anello 2 px `--accent-ring` + alone 5 px al 30 %.»
**Deroga richiesta.** Dentro `.site-header.is-scrolled` l'anello usa **`--accent-hover` (#0b555c)**;
l'alone resta `rgba(29,138,147,.30)` come altrove. Fuori da quello stato l'anello resta
`--accent-ring` ovunque.
**Motivo (calcolato, con `saturate()` incluso).** Il vetro scrollato è `rgba(251,250,248,.88)` su un
capitolo mezzanotte. `saturate(140%)` (matrice del filtro CSS su valori sRGB) porta `--mid-1`
`#0e1b23` a **`#0a1c27`**; la composizione all'88 % dà **`#dedfdf`**. Su quel fondo:
`--accent-ring` = **3,09 : 1**, `--accent-hover` = **6,39 : 1**. Su `--mid-0` (`#0a151c` →
`#061620`, composito `#dedfde`): 3,07 : 1 contro 6,35 : 1. La revisione misurava 3,08 : 1 ignorando
`saturate()`: **la misura è confermata, e `saturate()` non la muove di più di 0,01** perché la
mezzanotte è quasi neutra. 3,07–3,09 : 1 supera il minimo di 1.4.11 di 2–3 centesimi: non è un
margine su cui si firma un indicatore di focus.
**Costo.** L'anello di focus nel letterhead è di un gradino più scuro quando la pagina è scrollata.
È lo stesso accento (§1.3: «un solo accento interattivo»), nella luminosità che il fondo richiede —
la stessa logica con cui §1.1 affianca `--accent` e `--accent-dark`. Non si introduce alcun nuovo
valore: `--accent-hover` è già un token.

---

## 1. RISPOSTA PUNTO PER PUNTO ALLA REVISIONE

### 1.1 Violazioni dei vincoli non negoziabili — tutte rimosse, nessuna trasformata in deroga

| # | Violazione contestata | Esito |
|---|---|---|
| 1 | §8.1/§8.2 — `transform: scale(.842)` sul lock-up | **RIMOSSA.** Il lock-up non è animato, non è trasformato e non cambia allo scroll. Il suo unico comportamento resta quello del componente (`+1 px` in hover, `v2/shell.css:134`). Vedi §4.3 e §5. |
| 2 | `box-shadow` animata in `nav/header-settle` | **RIMOSSA.** L'elevazione è `opacity` su `.site-header::after`, che porta `--shadow-2` e non transisce mai l'ombra. Vedi §4.3 e §6.1. |
| 3 | 128 224 B di WebP 960 su un telefono DPR 2 | **RIMOSSA alla radice: la fotografia esce dal pannello.** Nessun `background-image` fotografico, nessun `image-set`, nessun `<picture>` nella navigazione. Costo immagini della navigazione: **0 B a qualunque DPR, in qualunque stato, su qualunque viewport** (§9). |
| 4 | Progressive enhancement: lo stato senza JS del mega-menu | **RIMOSSA.** §7.4 riscrive `html.no-js` per il pannello assoluto: apertura su `:hover` e `:focus-within`, più il segno di voce corrente in CSS puro. |
| 5 | La guardia a tre condizioni dell'area riservata | **RIMOSSA.** §8.2 riporta le tre condizioni verbatim, nella forma che `utility_bar.html:9-14` e `header.html:26-30` usano oggi. |

### 1.2 MUST-FIX — 18 fatti, 1 contestato con misura

| # | MUST-FIX | Esito | Dove |
|---|---|---|---|
| 1 | Blocco contenitore del pannello | **FATTO e misurato.** Nessun `position` su `.main-nav__list`. `.main-nav__item { position: static }` ≥ 80rem. La traccia vive dentro `.site-header__seam`, che **non è un antenato del pannello**. Verifica in browser: `panel.offsetParent === HEADER.site-header`; pannello `x = 0, w = 1280/1440/1600`, `y = 101` = bordo inferiore dell'header. | §4.5, §7.1 |
| 2 | Budget di larghezza sui token reali + banda 1536 | **FATTO.** `--container` 1176 → riquadro **1096** a 1280–1439; 1320 → **1240** a 1440–1599; 1440 → **1360** a ≥ 1600 (letti da `getComputedStyle` sul sito vivo, non dai token). Tabella completa a quattro lingue e sei viewport in §4.4; il test obbligatorio copre 1280 · 1366 · 1440 · **1536** · 1600 · 1920. | §4.4, §10 |
| 3 | Togliere `scale(.842)` dal lock-up | **FATTO**, senza deroga. | §4.3, §6 |
| 4 | Togliere `box-shadow` dalle proprietà animate | **FATTO.** `--shadow-2` su `::after`, si anima `opacity`. | §4.3, §6 |
| 5 | Scoping della visuale ≥ 80rem | **FATTO per soppressione**, e la soppressione è dichiarata: la fotografia esce dal pannello (§3.1). Nessuna immagine ⇒ nessun budget immagini da rispettare. | §4.5, §9 |
| 6 | Chiave della foto su `item.id` e non su `forloop.counter0` | **FATTO per soppressione**, dichiarata. Non esiste più alcuna mappa indice→asset, quindi non esiste il caso «sezione CMS senza mappatura»: **tutti i pannelli sono identici**, qualunque sia la loro origine (righe `cms.MenuItem` o `_FALLBACK_MAIN`) e qualunque sia lo stato dei gate. Misurato su :8770 (fase 3 chiusa): quattro voci di primo livello, tre pannelli; su :8771: sette voci, tre pannelli. Il disegno non dipende più dal conteggio. | §4.5 |
| 7 | Guardia completa dell'area riservata | **FATTO**, markup verbatim. | §8.2 |
| 8 | Regressione 768–1279 sulla porta | **FATTO.** La porta **non entra nel drawer** sopra 48rem: sta nella riga dell'header da 48rem in su, dove è visibile senza aprire nulla — e lì porta anche la sua etichetta. Sotto 48rem va nel drawer, come §8.2 prescrive per la barra. | §4.2 |
| 9 | Percorso senza JS | **FATTO**, regole scritte. | §7.4 |
| 10 | Pubblicare le prove | **FATTO nella seconda forma offerta dalla revisione**: i nove nomi di PNG e `measure.json` sono **cancellati** dall'intestazione e da ogni citazione. Al loro posto §2 pubblica la tabella delle misure e lo script esatto che le riproduce, così che ogni numero sia verificabile senza un file che non esiste. | §2 |
| 11 | Contrasto dell'anello sul vetro | **FATTO: 3,09 : 1**, ricalcolato con `saturate(140%)` incluso (backdrop `#0e1b23` → `#0a1c27`, composito `#dedfdf`). Poiché 3,09 non è un margine, **DEROGA 3** definisce un anello più scuro in `is-scrolled`: 6,39 : 1. | §0, §9 |
| 12 | Padding del pannello e griglia interna | **FATTO.** `padding-block: var(--s-8)` = 32 px, riquadro utile 224 px dentro `--nav-panel-h: 288px`. La griglia interna **riusa `.container`**: misurato, il bordo iniziale della colonna guida coincide al pixel con quello del lock-up (92 / 100 / 120 px a 1280 / 1440 / 1600). | §4.5 |
| 13 | Un solo nome per la porta | **FATTO: `.nav-door`** ovunque (anatomia, markup, CSS, JS, test). Nessun `.door` globale, nessuna collisione con la famiglia `.doorway` di `v2/hero.css`. | §4.2 |
| 14 | Righe che appaiono fuori dal proprio fondo | **FATTO, cambiando l'animazione invece di rattoppare il ritaglio.** Il fondo non si scala più: il pannello **intero** entra con `opacity` + `translateY(-8px → 0)` (famiglia OVERLAY di `MOTION_SYSTEM` §2). Non esiste più un frame in cui il contenuto stia fuori dal proprio fondo. `overflow: hidden` resta sul pannello per il contenuto, non per il fondo. | §4.5, §6 |
| 15 | Selettore `:has()` battuto da un messaggio Django | **FATTO: `:has()` è sparito.** La soglia carta/mezzanotte è una **classe server-side sul `<body>`** (`chapter-first-dark`), scritta dal template della pagina nel `{% block body_class %}` che `base.html:45` già espone, con un test che verifica la coerenza fra la classe e il primo `<section>` di `<main>`. Un messaggio flash non può batterla. | §4.8, §10 |
| 16 | Regole che la cancellazione si porta via | **FATTO.** `.main-nav__label` (riga di sezione senza URL, `cms.MenuItem`) e `.nav-overlay { display: none }` ≥ 80rem sono riscritte in `v3/nav.css`. | §7.2, §7.5 |
| 17 | Dichiarare ogni scostamento da §8.2 | **FATTO, e quattro dei cinque scostamenti sono stati eliminati invece che dichiarati.** Barra istituzionale: **`--min-1`** come prescritto (non `--min-0`). Lingue: **«FR · IT · EN · ع»** con la mappa glifo esplicita (`{{ l.code|upper }}` non può produrre ع, quindi non la si usa: §8.4). Righe del drawer: **52 px** come prescritto (non 56). Restano due scostamenti veri, dichiarati come **DEROGA 1** (la porta esce dalla barra) e **DEROGA 2** (la CTA «Orientation» è ritirata). | §0, §4.1, §4.7, §8.4 |
| 18 | «Far parlare la porta a 1440» | **RIMEDIO A CONTESTATO CON MISURA · RIMEDIO B ADOTTATO.** Vedi §1.3. | §1.3, §4.2 |
| 19 | Promuovere §4.8 a spina dorsale, togliere gli ordinali | **FATTO.** La soglia carta/mezzanotte non è più una regola in fondo al documento: è **il filo**, un elemento reale del markup che porta la linea dell'header, la graticola, la traccia della sezione corrente e il bordo da cui il pannello scende — quattro segni su un oggetto solo (§3.2, §4.3, §4.4, §4.5, §4.8). Gli ordinali mono `01 ─` sono cancellati (§3.1). | §3.2, §4 |

### 1.3 L'unico punto contestato — MUST-FIX 18, primo rimedio

La revisione offre due rimedi: «abbassare la soglia dell'etichetta da 96rem a 90rem, **oppure** dare
alla porta a riposo un fondo pieno o lavato».

**Il primo rimedio è impossibile, e la misura lo prova.** A 1440 il riquadro interno è **1240,0 px**
(misurato su `.site-header__inner`, `--container: 1320px` meno `--grid-margin: 40px` × 2). La riga
chiede, in francese:

`lock-up 302,9 + gap 24 + navigazione 827,8 + gap 24 + porta 40,0 = 1218,8` → margine **+21,2 px**.

Con l'etichetta, la porta passa da 40,0 a **150,8 px** (misurato in browser: `padding 14 + glifo 20 +
gap 8 + «Espace réservé» a --t-small/500 = 94,8 + padding 14`). Totale **1329,6 px** contro 1240,0:
**−89,6 px**, cioè 89,6 px di traboccamento in FR a 1440. In EN («Reserved area», 90,4 px):
`1188,9 + 106,4 = 1295,3` contro 1240 → **−55,3**. In IT («Area riservata», 88,5 px):
`1167,3 + 104,5 = 1271,8` contro 1240 → **−31,8**. La soglia a 90rem traboccherebbe in tre lingue su
quattro. Contestato.

**Il secondo rimedio è adottato, e va oltre la lettera della richiesta.** La porta non è più un tasto
fantasma di 40×40 con un anello di 1 px: è una **lastra piena `--accent` di 40 × 64**, a filo con il
bordo finale della riga e alta quanto la riga stessa, raggio 0 — una porta tagliata nel muro del
letterhead, non un bottone posato sopra. È piena **sempre**, a ogni larghezza e a ogni posizione di
scroll: la costanza è il punto. Glifo `--min-0` su `--accent` = **5,69 : 1**; il bordo della lastra
contro la carta dell'header = **6,05 : 1**. Sotto 80rem, dove la riga è quasi vuota (misurato a 768:
riquadro 688, lock-up 302,9, toggle 91,3 → 294 px liberi), la lastra porta **anche l'etichetta**.
Regola unica, in una frase: **la porta tiene la sua parola finché la navigazione non arriva; da 80rem
in su, la navigazione è la parola.**

### 1.4 Segnali «cheap / generico / default»

| # | Accusa | Risposta |
|---|---|---|
| 1 | Mega-menu con foto nel rail destro = template SaaS | **Accolta. La foto è cancellata.** Le colonne 10–12 del pannello non sono un rail visivo: sono il **margine del foglio**, il vuoto dichiarato che `layout.css:37-40` già usa come principio («Column 10 is a fixed empty channel: it is what makes the margin read as a margin»). Nel margine, e solo lì, il glifo arco+gradini di `BRAND_ASSETS.md` §2 come **impressione a secco**: `--ink` al 10 % su `--min-3` = `#e8e9ea`, **1,22 : 1**, deliberatamente sotto ogni soglia perché non porta informazione (`aria-hidden`, soppresso in `forced-colors`). Un mega-menu che è un foglio di carta intestata con un vero margine non è un tema WordPress: è il registro istituzionale. |
| 2 | L'arco dell'hero riusato come decorazione di dropdown | **Accolta.** Nessun `border-start-start-radius: 120px` nella navigazione. L'unica forma del marchio che entra nel pannello è il **glifo** arco+gradini, che §6 del design system autorizza esplicitamente fuori dall'hero («glifo arco+gradini negli stati vuoti»), nella posizione più discreta possibile. La porta intera resta nell'hero. |
| 3 | Ordinali mono su una lista non ordinata | **Accolta. Cancellati.** La riga del pannello è: etichetta `--t-ui` `--ink`, chevron in coda, filetto sotto, linea d'ormeggio in hover. Niente numeri. Il progetto ha già un linguaggio ordinale vero (quattro vie, sei stazioni) e non lo si spende su un elenco alfabetico. |
| 4 | Tasto icona fantasma 40×40 = shadcn | **Accolta.** Vedi §1.3: lastra piena 40×64 a filo di riga, e l'etichetta sotto 80rem. |
| 5 | `blur(14px) saturate(140%)` = il più consumato dei segnali premium | **Parzialmente respinta, con la clausola in mano.** `DESIGN_SYSTEM_V2` §8.2 prescrive verbatim «carta all'88 % + `backdrop-filter`, `--shadow-2`»: toglierlo richiederebbe una quarta deroga, e non la chiedo. Quello che si può fare, e che si fa, è **smettere di contarlo come un segno**: §4.3 non vende più «quattro segni», ne dichiara tre, di cui il primo è geometria reale e misurata (36 px di barra che se ne vanno) e il terzo non esisteva (§1.4 nº7). |
| 6 | Sottolineatura che viaggia su molla = demo Framer | **Respinta, con un argomento che non è ingegneristico.** La traccia non è una pillola che insegue il puntatore su uno sfondo neutro: è **il filo stesso dell'header**, cioè la riga che chiude la carta intestata, marcata nel punto in cui si trova il lettore. Ha un compito causale, non decorativo: **il pannello scende esattamente da quel segmento**. `MOTION_SYSTEM` §1 riserva `SPRING_FOLLOW` a «indicatore attivo del menu», cioè a questo componente e a nessun altro. |
| 7 | Una delle tacche è invisibile (1,22 : 1) | **Accolta e corretta con la misura.** Le tacche non sono più `--hairline` al 55 % (composito `#e5e4e0`, 1,22 : 1) ma **`--terr-line-lt` al 70 %** (composito `#56959a`, **3,26 : 1** sulla carta). Sono la graticola cartografica di §6, non un filetto d'interfaccia sbiadito. |
| 8 | Le prove non esistono | **Accolta.** Vedi MUST-FIX 10 e §2. |

---

## 2. PROVE — i numeri, e come rifarli

Nessun PNG è citato da questa specifica. Ogni misura qui sotto è stata presa con lo script seguente,
che chiunque può rieseguire; nessuna cifra è stimata.

```python
# .venv/Scripts/python.exe — Chromium headless di Playwright, mai la porta 9222
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(headless=True)                 # 153.0.8010.12
    pg = b.new_page(viewport={"width": 1440, "height": 900}, device_scale_factor=1)
    pg.goto("http://127.0.0.1:8771/fr/", wait_until="load")
    print(pg.evaluate("""() => {
      const g = s => { const e = document.querySelector(s); if (!e) return null;
        const b = e.getBoundingClientRect(), c = getComputedStyle(e);
        return {w:+b.width.toFixed(1), h:+b.height.toFixed(1), x:+b.x.toFixed(1), y:+b.y.toFixed(1),
                fs:c.fontSize, color:c.color, bg:c.backgroundColor}; };
      return {header:g('.site-header'), lock:g('.site-header .lock'), link:g('.main-nav__link'),
              barLink:g('.utility-bar__link'), lang:g('.lang-switcher__summary'),
              panel:g('.main-nav__panel'), hero:g('.hero')};
    }"""))
```

**Misure di riferimento, 1440 × 900, FR, :8771.**

| Oggetto | A riposo | Dopo `scrollTo(0, 900)` |
|---|---|---|
| `.site-header` | `y 37 · h 65 · bg rgb(251,250,248) · shadow none` | `y 0 · h 65 · bg rgba(251,250,248,.88) · --shadow-2` |
| `.site-header .lock` | `302,9 × 38 · x 100` | `302,9 × 38 · x 100` — **identico** |
| `.utility-bar` | `y 0 · h 37` | `y −900` — la barra non è sticky |
| `.main-nav__link` (prima voce) | `84 × 40 · font-size 13,5px · color rgb(74,90,98)` | idem |
| `.utility-bar__link` («Espace réservé») | `112,7 × 36 · 12px · color rgb(74,90,98) · bg trasparente · border 0` | fuori campo |
| `.lang-switcher__summary` | `80,5 × 36 · 12px` | fuori campo |
| `.main-nav__panel` (Personnes, aperto) | `576 × 206 · top 90 · bg rgb(255,255,255) · border 1px #d3d2cc · radius 0 · cols 224px 254px · gap 32px · padding 24px 32px` | — |
| bordo inferiore dell'header | `y 102` | — |

Da queste, senza interpretazione:

* **(a)** Lo stato scrollato non ha compattazione: il lock-up misura `302,9 × 38` in entrambi
  gli stati, al pixel. L'unica differenza nel DOM è il fondo, l'ombra e la scomparsa della barra.
* **(b)** Il pannello **taglia** il filetto dell'header: bordo superiore del pannello a `y = 90`
  contro bordo inferiore dell'header a `y = 102` → **12 px di sovrapposizione**.
* **(c)** `font-size: 13,5px` non è nella scala di §3.2 (…15 / 14 / 13…): è un valore inventato.
  E si capisce perché esiste: a 1280 la riga di oggi misura `302,9 + 24 + 769,1 = 1096,03` dentro un
  riquadro di **1096,0**. **Lo stato attuale a 1280 in francese ha zero pixel di margine.** Il 13,5 px
  non è una scelta tipografica: è la conseguenza di una riga che non entra.
* **(d)** A 390 × 844, drawer aperto: `.drawer-utility` occupa `y 74 → 283` (**209 px**), la prima
  voce comincia a `y 299`, l'ultima finisce a `y 670`, restano **174 px** di carta.
* **(e)** A 768, drawer aperto: `.nav-overlay` parte da `y 64`, il drawer da `y 102` → **38 px di
  header sotto un velo `rgba(14,22,29,.55)`**, lock-up ufficiale compreso.
* **(f)** Il gate cambia il menù ma non i pannelli: su :8771 sette voci e **tre** pannelli
  (Personnes 7 figli, Entreprises 2, Projet 4); su :8770 quattro voci e **tre** pannelli (1, 1, 4).
  La revisione ha ragione: la versione precedente di questa specifica era scritta per sette pannelli
  che non esistono in nessuna configurazione.

**Contrasti** (luminanza relativa WCAG 2.x, calcolati in Python sui token di `v2/tokens.css`,
composizioni alfa calcolate e non stimate — §9 li raccoglie tutti).

**Pesi** (`stat` + `gzip -9`, 24/09/2026): `main.js` 19 944 / **5 309** · `head.js` 233 / **206** ·
`dist/shell.js` 1 136 / **613** · `dist/motion.js` 242 / **189** · `dist/chunks/chunk-P4EHGXV4.js`
70 441 / **26 143** → totale attuale per pagina **32 460 B gzip** contro il tetto di 45 KB.
Catena CSS compilata: 205 579 B grezzi / **46 298 B gzip**.

---

## 3. LA DIREZIONE

### 3.1 Che cosa esce, e perché

Il round 1 aveva un'idea giusta (il pannello a tutta larghezza, ancorato alla testata) sepolta sotto
un vocabolario preso a prestito: la foto nel rail, l'arco riusato come decorazione, i numeri sulle
righe, il tasto fantasma, i «quattro segni» di cui tre non si vedevano. Escono tutti, e non tornano
in un'altra forma:

* **La fotografia esce dalla navigazione.** Non perché costa (costava: 128 224 B su un telefono
  DPR 2, misurato dai file reali), ma perché una foto di campus dietro un menù istituzionale legge
  come banca immagini in qualunque ritaglio, e perché la difesa di quella scelta — maschera ad arco
  e velo in gradiente — è esattamente ciò che fa ogni template. Il progetto ha fotografia
  art-directed, e il suo posto è l'hero e le pagine IMMERSIVE/RICH (§6 del design system), non il
  cromo che accompagna ogni pagina.
* **Gli ordinali mono escono.**
* **Il tasto fantasma esce.**
* **L'arco come decorazione esce**; resta il glifo, nel margine, come impressione a secco.

### 3.2 Che cosa resta, e che cos'è

**Il filo.** La carta intestata finisce da qualche parte, e quel «da qualche parte» è l'unico
elemento che questa superficie può possedere davvero. Oggi è una `border-block-end: 1px #d3d2cc`:
1,45 : 1 sulla carta, cioè niente, e sul capitolo mezzanotte che comincia 1 px sotto, niente di
nuovo. Nella V3 diventa **un elemento reale**, `.site-header__seam`, e porta quattro cose che prima
erano quattro decorazioni separate:

1. **la riga** che chiude il letterhead — `--hairline` sulla carta;
2. **la graticola** — le tacche cartografiche di §6, passo 160 px, `--terr-line-lt` al 70 %
   (3,26 : 1), che si ritirano quando il foglio si stacca dalla pagina;
3. **la traccia** — il segmento `--accent` di 2 px che marca la sezione in cui ti trovi e che si
   sposta, con l'unica molla che `MOTION_SYSTEM` §1 assegna a questo componente;
4. **la soglia** — quando sotto la testata comincia un capitolo mezzanotte, la riga non è più un
   filetto d'interfaccia invisibile: è **la linea del territorio**, `--terr-line`, 6,07 : 1 contro la
   mezzanotte sottostante (2,76 : 1 contro la carta sopra, cioè un tono, che è giusto così: la linea
   deve leggersi dal lato che ne ha bisogno). La carta intestata finisce dove comincia la carta
   geografica.

E il pannello scende **da** quel filo, a filo, per tutta la sua lunghezza. Un oggetto, quattro
compiti, nessun ornamento in più. Questa è la spina dorsale che la revisione chiedeva al MUST-FIX 19.

---

## 4. LA PROPOSTA

File nuovo **`static/css/v3/nav.css`**, importato da `static/css/main.css` dopo `v2/voyage.css` e
prima di `v3/buttons.css`. I blocchi di navigazione di `components.css` §7 (righe 484–1000) e di
`v2/shell.css` (righe 190–371, Desktop / Drawer / Mega) vengono **cancellati**, non sovrascritti:
nessun `!important`. La cancellazione è obbligatoria e non sostituibile da un override — misurato:
finché `[dir="rtl"] .main-nav__panel { transform: translateX(50%) }` (`components.css:811-813`)
esiste, in arabo il pannello a tutta larghezza si sposta di mezzo viewport (`x = 720` a 1440) perché
quella regola ha specificità maggiore di `.main-nav__panel`.

File nuovo **`static/js/src/nav.js`** → `static/js/dist/nav.js` (esbuild, sul chunk Motion già
caricato da `shell.js`). Template toccati: `partials/header.html`, `partials/utility_bar.html`,
`partials/main_nav.html`, `components/language_switcher.html`. **Nessuna vista, nessun contratto
dati**: `NavItem` (`id · label · url · description · children · new_tab · is_current · is_section`)
resta identico, e nessuna regola di questa specifica dipende dall'ordine, dal numero o
dall'identità delle voci.

### 4.1 Anatomia

```
.utility-bar            36 px · --min-1 · filetto inferiore dentro il container
  └ .utility-bar__inner (.container)
      [imprint 12/16 : «AGAMI … — promoteur du projet»]        [segmenti FR · IT · EN · ع]

.header-sentinel        (invariato — lo osserva shell.js)

header.site-header      64 px · --min-2 · sticky · nessun border-block-end
  ├ .site-header__inner (.container)
  │    [lock-up]   [.nav-drawer → nav.main-nav > ul.main-nav__list]   [a.nav-door]
  │                                    └ li > div.main-nav__panel
  │                                         position:absolute · inset-inline:0
  │                                         inset-block-start:100% · min-block-size:288px
  ├ span.site-header__seam          ← la riga, la graticola, la traccia, la soglia
  │    └ i.site-header__trace
  ├ ::after                         ← porta --shadow-2, si anima solo in opacity
  └ .nav-overlay                    (invariato)
```

**Il box dell'header non cambia mai altezza.** Comprimerlo 64 → 56 accorcerebbe il documento di 8 px
e farebbe saltare la pagina sotto il lettore, perché l'header è `sticky` **in flusso**, non `fixed`.
La compattazione reale esiste già ed è misurata: la barra istituzionale non è sticky, quindi il
cromo passa da **101 px a 65 px** (−35,6 %) appena si scorre. È la compattazione vera, e la V3 la
dichiara invece di simularne una con il marchio.

### 4.2 La porta — `.nav-door`

Un nodo solo, sempre lo stesso, in tre posizioni dettate dalla larghezza. **Nessuna duplicazione:
l'elemento è unico nel DOM e non esiste alcuna larghezza in cui due link verso l'area riservata siano
nell'albero di accessibilità.** Se l'utente è autenticato, nello stesso slot va
`components/account_menu.html`; se le tre condizioni di §8.2 non sono tutte vere, **il nodo non viene
reso affatto** (niente stato disabilitato grigio).

| Larghezza | Posizione | Disegno |
|---|---|---|
| **< 48rem** | ultima riga del foglio del drawer, dopo la navigazione, prima dell'imprint | riga piena a tutta larghezza, `min-block-size: 56px`, fondo `--accent`, glifo + etichetta `--min-0` a `--t-body` 17/28 (5,69 : 1) |
| **48–80rem** | riga dell'header, bordo finale | lastra `--accent`, `block-size: 64px` (`align-self: stretch`), `padding-inline: 14px`, glifo 20 px + `gap --s-2` + etichetta `--t-small` 14/20, tutto `--min-0`. Larghezza misurata: 150,8 (fr) · 144,5 (it) · 146,4 (en) · 133,4 (ar). Spazio libero misurato a 768: **294 px** |
| **≥ 80rem** | riga dell'header, bordo finale | lastra `--accent` **40 × 64**, raggio 0, glifo `key` 20 px `--min-0`; `.nav-door__label` prende le dichiarazioni di `.visually-hidden` — resta nel DOM, resta il nome accessibile, non diventa mai `aria-label` né `title` |

Stati (identici a ogni larghezza):

| Stato | Disegno | Contrasto |
|---|---|---|
| riposo | fondo `--accent`, contenuto `--min-0` | glifo/etichetta 5,69 : 1 · bordo lastra/carta 6,05 : 1 |
| hover | fondo `--accent-hover` | 8,16 : 1 sulla carta; contenuto 7,44 : 1 |
| focus-visible | anello 2 px + alone 5 px al 30 % (`--accent-ring`, oppure `--accent-hover` in `is-scrolled`, DEROGA 3), `outline-offset: 2px` | 3,94 : 1 su carta · 6,39 : 1 sul vetro |
| active | `translateY(1px)` — §10 del design system | — |
| `is-scrolled` | **nessun cambiamento.** La porta non «si arma»: è già armata | — |

**Ordine della riga, che è anche l'ordine DOM e l'ordine di tabulazione** (nessun `order` CSS, mai):
`lock-up` → `nav-toggle` → `nav-drawer` → `nav-door--row`. A 48–80rem il drawer è chiuso e invisibile
(`visibility: hidden`, quindi saltato dalla tastiera), quindi si percorre lock-up → hamburger → porta,
che è anche l'ordine visivo da sinistra a destra in LTR e da destra a sinistra in RTL. A ≥ 80rem
l'hamburger è `display: none` e si percorre lock-up → sette voci → porta.

La porta è cromo, non contenuto: 40 px di larghezza contro i ~350 px della CTA primaria dell'hero,
raggio 0 contro raggio 2, altezza di riga contro 48 px, nell'angolo finale del letterhead e non nella
colonna di lettura. Non compete con la CTA primaria perché non ne ha la forma, la misura, né il posto.

### 4.3 Stato scrollato — tre segni, e il primo è geometria

`.site-header.is-scrolled`:

1. **La barra se ne va.** Non è un effetto: è il documento. Misurato, `y 0 → −900`; il cromo passa da
   101 px a 65 px. È il segno più grande e non costa nulla.
2. **Il foglio si stacca.** Carta all'88 % + `backdrop-filter: blur(14px) saturate(140%)` (§8.2,
   verbatim) e `--shadow-2` portata da `.site-header::after` con `opacity: 0 → 1`. **Mai una
   transizione di `box-shadow`.**
3. **La graticola si ritira.** `.site-header__seam::before` passa da `scaleY(1)` a `scaleY(0)` con
   `transform-origin: 50% 100%`: le tacche rientrano nel filo. Un `transform`, zero paint aggiuntivi.

Il lock-up **non cambia**: non si scala, non trasla, non cambia colore, non cambia opacità
(§8.1 «Nessun effetto, nessuna animazione», §8.2 «il lock-up non cambia»). La porta non cambia.
La traccia resta dov'è, perché è sul filo e il filo è sempre al bordo inferiore dell'header.
Sotto 80rem il vetro resta disattivato (`background: var(--min-2)`), come oggi.

### 4.4 La riga, e il budget che la governa

Tipografia della navigazione: `--t-ui` **15 / 20**, `--f-sans` **500**, `--ink-2` (**6,87 : 1**),
`padding-inline: 6px`, `min-block-size: 44px`, `gap: var(--s-1)`. `.main-nav__toggle` passa da
32 × 40 a **24 × 44** (≥ 24 px, WCAG 2.5.8 AA). Il 13,5 px fuori scala sparisce. La voce corrente è
`--ink` (**15,56 : 1**) con `font-weight: 500` **e** la traccia: **il colore non è mai solo**.

**Il lock-up.** §8.1 fissa la scala come unità: «38/20 finché entra; poi **solo il marchio 38 px con
`aria-label`**». La misura dice dove sta quel «finché»:

| Riquadro interno misurato | 1280–1439 → **1096,0** | 1440–1599 → **1240,0** | ≥ 1600 → **1360,0** |
|---|---:|---:|---:|
| lock-up completo + 7 voci a 15 px + porta 40 | 1218,8 | 1218,8 | 1218,8 |
| margine | **−122,8** | +21,2 | +141,2 |
| **solo il marchio** (38) + 7 voci + porta 40 | 953,8 | — | — |
| margine | **+142,2** | — | — |

Quindi, senza inventare nulla e senza chiedere nulla: **a 1280–1439 la testata mostra il marchio da
solo** (il nome accessibile resta sull'`<a class="brand">`, che già porta `aria-label`), **e il
wordmark torna a 1440**. È la scala d'unità del design system applicata al punto in cui serve, non
una scorciatoia. L'alternativa — otto voci in un hamburger su un portatile da 1280 — è peggiore, e
la terza alternativa (un 13,5 px inventato) è ciò che questa specifica sta rimuovendo.

**Budget completo** (testi misurati in browser a `--t-ui` 15 px / peso 500 con la famiglia reale, non
riscalati; `padding` 6 × 2 per voce; `gap` 4 fra voci; toggle 24; `gap` di riga 24):

| | 1280 | 1366 | 1440 | 1536 | 1600 | 1920 |
|---|---:|---:|---:|---:|---:|---:|
| riquadro interno | 1096,0 | 1096,0 | 1240,0 | 1240,0 | 1360,0 | 1360,0 |
| lock-up | 38,0 | 38,0 | 302,9 | 302,9 | 302,9 | 302,9 |
| navigazione **FR** (7 voci) | 827,8 | 827,8 | 827,8 | 827,8 | 827,8 | 827,8 |
| porta | 40,0 | 40,0 | 40,0 | 40,0 | 40,0 | 40,0 |
| **totale FR / margine** | 953,8 / **+142,2** | 953,8 / **+142,2** | 1218,8 / **+21,2** | 1218,8 / **+21,2** | 1218,8 / **+141,2** | 1218,8 / **+141,2** |
| navigazione **IT** | 776,4 | 776,4 | 776,4 | 776,4 | 776,4 | 776,4 |
| **margine IT** | **+190,6** | **+190,6** | **+72,6** | **+72,6** | **+192,6** | **+192,6** |
| navigazione **EN** | 798,0 | 798,0 | 798,0 | 798,0 | 798,0 | 798,0 |
| **margine EN** | **+169,0** | **+169,0** | **+51,0** | **+51,0** | **+171,0** | **+171,0** |
| navigazione **AR** | 659,0 | 659,0 | 659,0 | 659,0 | 659,0 | 659,0 |
| **margine AR** | **+308,0** | **+308,0** | **+190,0** | **+190,0** | **+310,0** | **+310,0** |

Larghezze di testo misurate a 15 px / 500, per voce (FR): Personnes 71,1 · Entreprises 77,4 ·
Institutions 78,9 · Universités & Formation 164,8 · Forum Vénétie–Maroc 147,1 · Actualités 67,6 ·
Projet 40,9 → **647,8**; + 84 di padding + 24 di gap + 72 di toggle = **827,8**.

Il caso peggiore è **FR a 1440–1599: +21,2 px**. È positivo, ed è il numero che il test deve
difendere. **Valvole, nell'ordine, già scelte e misurate**: (1) `padding-inline: 6px → 4px` restituisce
`2 × 2 × 7 = 28 px` (margine FR a 1440 → +49,2); (2) `gap: var(--s-1) → 2px` restituisce 12 px;
(3) se e solo se una traduzione futura esaurisce entrambe, la soglia del solo marchio sale da 90rem a
100rem (margine FR a 1440 → +286,3). Nessuna valvola tocca il numero di voci: la IA è verità di
prodotto. Se l'immagine di logo del back-office è attiva (`site.settings.use_logo_image`) il lock-up
misura 160 px invece di 302,9 e ogni margine migliora di 142,9: il budget regge a fortiori.

**Test obbligatorio** (§10): `header.scrollWidth > header.clientWidth` **e** somma dei figli della
riga > riquadro interno, a 1280 · 1366 · 1440 · **1536** · 1600 · 1920, in `fr it en ar`, su **:8771
e :8770** (i gate cambiano il numero di voci: su :8770 la navigazione FR misura 516,0 invece di
827,8 e ogni margine cresce di 311,8).

### 4.5 Il pannello — il foglio che scende dal filo

`.main-nav__item { position: static }` a ≥ 80rem; `.main-nav__panel { position: absolute;
inset-inline: 0; inset-block-start: 100% }`. L'unico antenato posizionato è `.site-header`
(`position: sticky`, `z-index: 20`): `.container` non dichiara `position` (`layout.css:14-19`),
`.nav-drawer` non lo dichiara, `.main-nav` non lo dichiara, e **`.main-nav__list` non lo dichiara,
perché la traccia non vive più lì**. Verificato in browser a 1280 / 1440 / 1600, FR e AR:
`panel.offsetParent` è `HEADER.site-header`, il pannello misura `x = 0`, `w = 1280 / 1440 / 1600`,
`y = 101` — cioè esattamente il bordo inferiore dell'header, che non viene più tagliato (difetto §2 b).

Conseguenze: tutti i pannelli hanno la stessa geometria, qualunque sia la loro voce; spariscono
`main-nav__item--end`, i tre `@keyframes` `menu-in` / `menu-in-rtl` / `menu-in-end` e i due
`translateX(±50%)` da specchiare; e fra voce e pannello non resta varco, quindi non serve alcun
«triangolo sicuro» per l'hover.

```
┌ .main-nav__panel — --min-3 · --shadow-3 · raggio 0 · min-block-size 288 · padding-block 32 ────┐
│ .main-nav__panel-inner (.container) — 12 colonne, gutter 24, contenuto centrato, utile 224 px  │
│ ┌ guida 1–3 ─────────────┬ collegamenti 4–9 ─────────────────────────┬ margine 10–12 ────────┐ │
│ │ TITOLO serif 22/28     │ Votre parcours              ›             │                      │ │
│ │ descrizione 14/20      │ Diplômes et titres          ›             │      (glifo arco      │ │
│ │                        │ Formation                   ›             │       + gradini,      │ │
│ │ Voir l'espace →        │ Vivre en Italie             ›             │       --ink al 10 %)  │ │
│ └────────────────────────┴───────────────────────────────────────────┴──────────────────────┘ │
└ tacche --terr-line-lt sul filo inferiore, passo 160, opacità .7 ───────────────────────────────┘
```

* **Livello 3, non livello 2.** Ritiro esplicitamente l'affermazione del round 1 («fondo `--min-2`,
  non `--min-3`»): §2 del design system assegna «popover, **menu**» al livello 3, cioè `--min-3` con
  `--shadow-3`, e un `--min-2` con `--shadow-3` sarebbe stato un livello ibrido non dichiarato. La
  scatola di oggi non legge come scatola perché è bianca: legge come scatola perché è un rettangolo
  di 576 px che galleggia, taglia il filetto e ha un bordo. Tolti il rettangolo, il galleggiamento e
  il bordo, il bianco è il bianco del livello 3, e la differenza con la carta dell'header (#ffffff
  contro #fbfaf8) è esattamente l'elevazione per scala di superfici che §12 rivendica.
* **Altezza.** `min-block-size: var(--nav-panel-h)` con `--nav-panel-h: 288px`, `padding-block:
  var(--s-8)` (32 px) → **224 px utili**, contenuto centrato (`align-content: center`). Righe da
  48 px: una colonna fino a 4 figli (4 × 48 = 192 ≤ 224), due colonne da 5 figli in su
  (`main-nav__sublist--two`, già emesso dal template quando `children|length > 4`), quindi ≤ 8 figli
  restano 4 righe. **In ogni configurazione reale del prodotto l'altezza è costante**: misurato,
  288 px per Personnes (7 figli), Entreprises (2) e Projet (4) su :8771, e per (1, 1, 4) su :8770.
  Il pannello cresce **solo** da 9 figli in su (5 righe = 240 > 224): in quel caso, e solo in quello,
  lo scambio fra sezioni anima l'altezza con `SPRING_SETTLE` (famiglia LAYOUT, `MOTION_SYSTEM` §2).
* **Allineamento.** `.main-nav__panel-inner` è **la stessa `.container` dell'header**: nessuna griglia
  da 1320 ricostruita a mano. Misurato: il bordo iniziale della colonna guida coincide al pixel con
  quello del lock-up — 92 px a 1280, 100 px a 1440, 120 px a 1600.
* **Riga di collegamento.** `min-block-size: 48px`, etichetta `--t-ui` `--ink` (16,23 : 1 su
  `--min-3`), chevron `chevron-end` **in coda** (oggi è in testa) in `--ink-3` (6,14 : 1), filetto
  `--hairline` sotto ogni riga, mai doppio. Hover/focus: **linea d'ormeggio** di 2 px `--accent` che
  cresce dal bordo di lettura (`::before`, `scaleX`, `transform-origin` logica) e chevron che trasla
  di 4 px. `aria-current="page"`: ormeggio permanente + `font-weight: 500` (segnale non cromatico).
* **Il margine.** Colonne 10–12 vuote, con il glifo arco+gradini a `--ink` 10 % (composito `#e8e9ea`,
  1,22 : 1), `inline-size: 120px`, `aria-hidden="true"`, SVG inline dal set proprio, **0 richieste**.
  Quando la sezione ha 1 o 2 figli, `data-children` porta i collegamenti a 4 colonne (4–7) e il glifo
  a 9–12 a 160 px, così la griglia resta piena senza allargare le righe (guardia del rischio 2).
* **Nessuna stringa nuova.** Il pannello non introduce alcun testo che non venga da `NavItem`:
  nessun `alt`, nessun `aria-label`, nessun `title`, nessuna didascalia. Il glifo è `aria-hidden`.
  La superficie di rischio verso `apps/cms/forbidden.py` resta nulla, e la verifica resta dovuta
  (§9, HUMAN_QA d).

### 4.6 La traccia — un segmento del filo, non una pillola

La traccia è **dentro il filo**: `<i class="site-header__trace">` figlio di
`<span class="site-header__seam">`, che è figlio diretto di `<header>` e **non è un antenato del
pannello**. Il filo è `position: absolute` sul bordo inferiore dell'header e largo quanto l'header
(misurato: `x = 0`, `w = 1280 / 1440 / 1600`), quindi è lo spazio di misura naturale.

```css
.site-header__trace {
  position: absolute; inset-block-end: 0; inset-inline-start: 0;
  inline-size: 1px; block-size: 2px; background: var(--accent);
  transform-origin: 0 50%;
  transform: translate3d(calc(var(--trace-x, 0px) * var(--dir, 1)), 0, 0) scaleX(var(--trace-w, 0));
}
[dir="rtl"] .site-header__trace { --dir: -1; transform-origin: 100% 50%; }
```

`nav.js` scrive `--trace-x` e `--trace-w` con `element.style.setProperty()` — la stessa API CSSOM che
`main.js:132` già usa per `--nav-drawer-top`, ammessa da `style-src 'self'` (CSP3 esenta la CSSOM;
è il `style=""` nel markup che è vietato, e questa specifica non ne introduce nessuno).

La misura è **logica**, non fisica: `x = rtl ? seam.right − item.right : item.left − seam.left`.
Verificato in browser: FR a 1440, voce «Personnes» → `--trace-x 448,2`, `--trace-w 83,1`, traccia
renderizzata a `x 448,2 · w 83,1 · y 99`; AR a 1440, stessa voce → `--trace-x 622,3`, traccia
renderizzata a `x 771,7 · w 46,0`, cioè sul bordo di lettura corretto. Il segno vive in `--dir`, non
in un `if` nel JS.

Innesco: `pointerenter` sulla voce, `focusin` su una voce di primo livello, apertura di un pannello.
Riposo: la voce con `aria-current`; se non ce n'è, `scaleX(0)`. Molla: `SPRING_FOLLOW`
`{stiffness: 400, damping: 40}`, senza rimbalzo, la molla che `MOTION_SYSTEM` §1 assegna a questo
componente e a nessun altro.

### 4.7 Il drawer come foglio

Ordine DOM **e** visivo **e** di tabulazione: `.main-nav` → `.nav-door` → `.drawer-utility`.
Nessun `order` CSS. Materiale: fondo `--min-2`, filetto superiore `--hairline`, **`--shadow-5`**
(livello 5, oggi assente: misurato `box-shadow: none`). Righe: `min-block-size: 52px` (§8.2),
etichetta `--t-entry` 22/28 `--f-sans` 500 `--ink`; il `border-block-end` resta **solo su
`.main-nav__item`** e viene tolto da `.main-nav__link` — cura del difetto dei filetti doppi da 366 e
314 px. `.main-nav__toggle` 52 × 52. Sottopannello aperto: fondo `--min-1`, barra di 2 px `--accent`
sul bordo di lettura, righe 48 px, altezza animata con `SPRING_SETTLE`.

Scrim: `.nav-overlay { inset-block-start: var(--nav-drawer-top, var(--header-height)) }` — la stessa
variabile che `main.js:132` già scrive sul drawer, letta anche dall'overlay. Serve **una riga** in
`main.js`, accanto a quella che esiste: `overlay.style.setProperty("--nav-drawer-top", ...)`. Cura
del difetto §2 e (38 px di header sotto il velo a 768). `touch-action: manipulation` su righe,
toggle e porta.

Aritmetica del foglio a 390 × 844, drawer aperto (oggi → V3): prima voce a `y 299` → **`y 73`**
(−226 px); navigazione 7 × 52 + filetti ≈ 371 px; porta 56 px; imprint + segmenti ≈ 96 px; il foglio
finisce a ≈ `y 636` e lascia ≈ 208 px di carta in fondo — che è il margine del foglio, non un buco
fra un preambolo e un elenco.

### 4.8 La soglia — dove la carta incontra la mezzanotte

```css
:root { --seam: var(--hairline); }
body.chapter-first-dark .site-header:not(.is-scrolled) { --seam: var(--terr-line); }
.site-header__seam { background: var(--seam); }
```

La classe `chapter-first-dark` è **server-side**, scritta dal template della pagina nel
`{% block body_class %}` che `base.html:45` già espone (oggi: `templates/pages/home.html:10`, che
apre su `.hero.chapter--dark`). Niente `:has()`: `{% block breadcrumbs %}` e il `{% if messages %}`
di `base.html:55-61` non possono batterla, perché non c'è selettore strutturale da battere. Un test
la tiene onesta (§10 nº6): `body.chapter-first-dark` ⟺ il primo `<section>` dentro `<main>` ha
`chapter--dark`.

`--terr-line` (#3fa6af) misura **6,07 : 1** contro la mezzanotte che comincia 1 px sotto e
**2,76 : 1** contro la carta che finisce 1 px sopra: si legge dal lato che ne ha bisogno, e dall'altro
è un tono. Solo a riposo: quando la testata è scrollata, ciò che le sta sotto non è più noto, e il
filo torna `--hairline`. In `forced-colors` il filo è `CanvasText`.

---

## 5. 21ST.DEV E UI-UX-PRO-MAX — che cosa resta delle interrogazioni del round 1

Nulla è installato; zero dipendenze npm aggiunte. Resta quanto segue, e solo quanto segue.

| Fonte | Che cosa sopravvive al round 2 |
|---|---|
| **Navbar Section 2** (@solaceui) | L'espansione del pannello a tutta larghezza della barra: geometria identica per ogni sezione, e cadono `main-nav__item--end`, i tre `@keyframes` e i due `translateX(±50%)` speculari. È l'idea portante di §4.5. |
| **Dither Sweep Navbar** (@kedhareswer) | «Adjacent cells never double up into a 2px line»: è la cura del difetto dei filetti doppi nel drawer (§4.7). Il resto (144 `<i>` per voce, `<style>` inline, unità `vw`) resta rifiutato: CSP `style-src 'self'` e ~1000 nodi per barra. |
| **Rich Navigation Menu** (@shadcnui-blocks) | Un solo contenitore condiviso che si rimodella fra le sezioni, invece di sette scatole: qui diventa un pannello per voce ma con **box identico e altezza costante**, quindi lo scambio è un crossfade del solo contenuto (§6, `nav/panel-switch`). Rifiutati la griglia `w-[900px]` ancorata alla voce, le icone Lucide (il progetto ha un set proprio, tratto 1.5) e l'intera catena React/Radix. |
| **Navbar 5** (@shadcnblockscom) | Il drawer che entra dall'alto con sottomenu ad accordion: è il modello che il progetto ha già e va tenuto — nessun cambio di modello mentale. |
| **Segmented Control** (@ddoemonn) | Il modello a segmenti per la lingua, **senza** `role="radio"`: la lingua è navigazione (`<a>` + `aria-current`), non uno stato di modulo (§8.4). |
| **Morphing Scroll Navbar** (@laziekiki) | Lo stato scrollato come trasformazione dichiarata e non come opacità. **Il filetto di avanzamento di lettura è ritirato**: `MOTION_SYSTEM` §4 dice che STANDARD, DENSE e LEGAL non hanno né un oggetto vivo né un oggetto indicizzato allo scroll, e il round 1 lo ammetteva proprio lì. Era una violazione non dichiarata, e si toglie. |
| **Navbar Menu** (Aceternity) · **Floating Header** (@efferd) | Niente: controprove. Molla elastica con overshoot (vietata da `MOTION_SYSTEM` §1), apertura solo a hover (inaccessibile da tastiera), angoli arrotondati e margini laterali sulla testata (qui il foglio è una carta intestata, raggio 0). |
| **ui-ux-pro-max** (ux · style · gsap) | Accettati: ordine di tabulazione = ordine visivo (§4.7); hover come acceleratore con il clic che resta il contratto e `aria-expanded` sempre veritiero; `touch-action: manipulation`; il vincolo di contrasto sul vetro (§9); lo stagger 40 ms (dentro i 40–60 ms di `MOTION_SYSTEM` §1). Rifiutati: GSAP e `power1.out` (la libreria è Motion 13.4.1 e le curve ammesse sono tre); la ricetta glassmorphism (blur 10–20, fondo 10–30 %) perché §8.2 fissa l'88 %; e la direzione «government ⇒ evita gli effetti di moto», che è esattamente il registro bocciato il 24/09. |

---

## 6. MOTION — voci per `MOTION_SYSTEM.md` §6

Nessun loop ambientale: la navigazione **non** consuma l'unico oggetto vivo della pagina. Nessun
oggetto indicizzato allo scroll. Nessuna durata fuori dai quattro token. Nessuna curva fuori dalle
tre. Nessun overshoot. Ogni `transition` e ogni `@keyframes` di `v3/nav.css` sta dentro
`@media (prefers-reduced-motion: no-preference)`; fuori da quel blocco il valore è quello finale, e
**nulla resta a opacità 0 o invisibile**.

| Nome | Funzione | Innesco | Durata / molla | Curva | Proprietà | Stato ridotto | Budget |
|---|---|---|---|---|---|---|---|
| `nav/trace-follow` | ORIENTAMENTO | `pointerenter` voce · `focusin` voce · apertura pannello | `SPRING_FOLLOW` 400/40 | — | `transform` (`translate3d` + `scaleX`) su `.site-header__trace` | `transform` assegnato senza animazione | `will-change: transform` su `pointerenter` della lista, tolto su `pointerleave` e a molla ferma |
| `nav/panel-open` | PROFONDITÀ | clic sul toggle, o hover con intento 120 ms sotto `(hover:hover) and (pointer:fine)` | `--motion-base` 240 ms | `--ease-out` | `opacity 0→1` + `translateY(-8px→0)` sul **pannello intero** | pannello completo e fermo all'apertura | un solo elemento, 0 layout, 0 paint oltre il primo frame; nessun `clip-path`, nessun fondo che si scala |
| `nav/panel-switch` | CAUSALITÀ | apertura di una sezione mentre un'altra è aperta | `--motion-instant` 120 ms uscita → `--motion-fast` 180 ms entrata | `--ease-in` → `--ease-out` | `opacity` su `.main-nav__panel-inner`; il box del pannello **non si muove** | cambio immediato del contenuto | altezza costante (§4.5) ⇒ nessuna animazione di `height` |
| `nav/panel-close` | ORIENTAMENTO | `Escape`, clic fuori, `focusout` | `--motion-fast` 180 ms | `--ease-in` | `opacity 1→0` + `translateY(0→-8px)` | chiusura immediata | — |
| `nav/header-settle` | ORIENTAMENTO | `IntersectionObserver` su `.header-sentinel` (invariato) | `--motion-slow` 320 ms | `--ease-standard` | `background-color` sull'header · `opacity` su `.site-header::after` (che porta `--shadow-2`) · `transform: scaleY(1→0)` su `.site-header__seam::before` | stati finali senza transizione | **nessuna transizione di `box-shadow`**; due compositing, un colore |
| `nav/door-state` | FEEDBACK | hover / focus / active sulla porta | 180 ms in · 120 ms out | `--ease-out` / `--ease-in` | `background-color` (`--accent` ⇄ `--accent-hover`); active `translateY(1px)` (§10) | colori finali immediati | box di 40 × 64 |
| `nav/row-mooring` | FEEDBACK | hover / focus su una riga di pannello o di drawer | 180 ms in · 120 ms out | `--ease-out` / `--ease-in` | `::before` `scaleX 0→1` (origine logica di lettura) · chevron `translateX 0→4px` | identico, senza transizione | 2 px × altezza riga, compositato |
| `nav/drawer-sheet` | PROFONDITÀ | `[data-nav-toggle]` | `--motion-slow` 320 ms | `--ease-out` / `--ease-in` | foglio `translateY(-12px→0)` + `opacity`; scrim `opacity` | apertura immediata, scrim fermo | il foglio è già `position: fixed` |
| `nav/drawer-rows` | GERARCHIA | apertura del drawer, **senza ritardo d'ingresso** | `--motion-base` 240 ms, `stagger(0.04)` | `--ease-out` | righe `opacity 0→1` + `translateY(8px→0)` | tutte le righe al valore finale | 7–8 nodi, un solo `animate()` |
| `nav/accordion` | LAYOUT | toggle di sezione nel drawer | `SPRING_SETTLE` 260/30 | — | `height` su valore misurato + `transform` sui fratelli | salto immediato | famiglia LAYOUT, `MOTION_SYSTEM` §2 |

**Rispetto al round 1 sono state cancellate due voci**: `nav/door-arm` (la porta non cambia più allo
scroll) e il filetto di avanzamento di lettura (vietato da `MOTION_SYSTEM` §4 su STANDARD e LEGAL).
Il ritardo d'ingresso di 80 ms di `nav/drawer-rows` è sparito perché 80 ms non è né una durata token
né uno stagger di 40–60 ms. Ogni voce passa da `withMotion(fn, settle)` di
`static/js/src/motion.js`, con `matchMedia` letto dal vivo a ogni chiamata.

---

## 7. IL CSS — `static/css/v3/nav.css`

Ordine del file: token locali → filo → riga → porta → pannello (≥ 80rem) → drawer (< 80rem) →
lingua → stati senza JS → `forced-colors` → moto. Ogni selettore qui sotto è normativo.

### 7.1 Token locali, filo, elevazione

```css
:root {
  --nav-panel-h: 288px;
  --nav-tick: 160px;          /* passo della graticola, §6 del design system */
  --seam: var(--hairline);
}

.site-header { border-block-end: 0; }            /* il filetto diventa un elemento */

.site-header::after {                            /* porta --shadow-2; si anima solo in opacity */
  content: ""; position: absolute; inset: 0; z-index: -1;
  box-shadow: var(--shadow-2); opacity: 0; pointer-events: none;
}
.site-header.is-scrolled::after { opacity: 1; }

.site-header__seam {
  position: absolute; inset-inline: 0; inset-block-end: 0; z-index: 2;
  block-size: 1px; background: var(--seam); pointer-events: none;
}
.site-header__seam::before {                     /* la graticola */
  content: ""; position: absolute; inset-inline: 0; inset-block-end: 0; block-size: 6px;
  background: repeating-linear-gradient(to right,
              var(--terr-line-lt) 0 1px, transparent 1px var(--nav-tick));
  opacity: .7; transform-origin: 50% 100%;
}
.site-header.is-scrolled .site-header__seam::before { transform: scaleY(0); }

.site-header__trace {
  position: absolute; inset-block-end: 0; inset-inline-start: 0;
  inline-size: 1px; block-size: 2px; background: var(--accent);
  transform-origin: 0 50%;
  transform: translate3d(calc(var(--trace-x, 0px) * var(--dir, 1)), 0, 0) scaleX(var(--trace-w, 0));
}
[dir="rtl"] .site-header__trace { --dir: -1; transform-origin: 100% 50%; }

body.chapter-first-dark .site-header:not(.is-scrolled) { --seam: var(--terr-line); }

.site-header.is-scrolled { --accent-ring: var(--accent-hover); }   /* DEROGA 3 */
```

**Impilamento locale.** `.site-header` è già un contesto di impilamento (`position: sticky` +
`z-index: 20`), quindi i valori qui sotto valgono solo fra i suoi figli e non toccano il resto della
pagina: `::after` (portatore dell'ombra) **−1**, `.site-header__inner` auto, `.main-nav__panel` **1**,
`.site-header__seam` **2** — così il filo e la traccia non vengono mai coperti dal pannello che ne
scende. Non si usa `--z-dropdown`: è definito in `_legacy-tokens.css:181`, il ponteggio di
demolizione, e un file V3 non deve dipenderne.

### 7.2 La riga (≥ 80rem)

```css
@media (min-width: 80rem) {
  .site-header__inner { gap: var(--s-6); align-items: center; }
  .nav-toggle { display: none; }
  .nav-drawer { display: block; flex: 1 1 auto; min-inline-size: 0; }   /* nessun position */
  .nav-overlay { display: none; }                                        /* ripreso da components.css:829 */

  .main-nav__list { display: flex; justify-content: flex-end; align-items: stretch;
                    gap: var(--s-1); margin: 0; padding: 0; list-style: none; }
  .main-nav__item { position: static; display: flex; align-items: center; }

  .main-nav__link,
  .main-nav__label {
    display: inline-flex; align-items: center; min-block-size: 44px; padding-inline: 6px;
    font-family: var(--f-sans); font-size: var(--t-ui); line-height: var(--t-ui-lh);
    font-weight: 500; color: var(--ink-2); text-decoration: none; white-space: nowrap;
    border-radius: 0;
  }
  .main-nav__label { color: var(--ink-3); cursor: default; }   /* sezione CMS senza URL */
  .main-nav__link:hover,
  .main-nav__link:focus-visible,
  .main-nav__link[aria-current] { color: var(--ink); }
  .main-nav__link[aria-current] { font-weight: 500; }

  .main-nav__toggle {
    display: inline-flex; align-items: center; justify-content: center;
    inline-size: 24px; min-block-size: 44px; color: var(--ink-3);
    background: none; border: 0; border-radius: 0;
  }
  .main-nav__toggle .icon { inline-size: 16px; block-size: 16px; }
  .main-nav__toggle[aria-expanded="true"] .icon { transform: rotate(180deg); }

  .site-header .lock__text { display: grid; }
}
@media (min-width: 80rem) and (max-width: 89.999rem) {
  .site-header .lock__text { display: none; }    /* §8.1: «poi solo il marchio 38 px con aria-label» */
}
```

### 7.3 La porta

```css
.nav-door {
  display: inline-flex; align-items: center; justify-content: center; gap: var(--s-2);
  flex: none; background: var(--accent); color: var(--min-0);
  text-decoration: none; border: 0; border-radius: 0;
}
/* Una sola istanza è mai nell'albero di accessibilità: display:none, non visibility. */
@media (min-width: 48rem)   { .nav-door--drawer { display: none; } }
@media (max-width: 47.999rem) { .nav-door--row  { display: none; } }
.nav-door .icon { inline-size: 20px; block-size: 20px; flex: none; }
.nav-door:hover { background: var(--accent-hover); color: var(--min-0); }
.nav-door:active { transform: translateY(1px); }
.nav-door:focus-visible { outline: 2px solid var(--accent-ring); outline-offset: 2px;
                          box-shadow: 0 0 0 5px rgb(29 138 147 / .30); }

@media (min-width: 48rem) {                 /* nella riga dell'header, etichettata */
  .nav-door { align-self: stretch; block-size: var(--header-height);
              padding-inline: 14px;
              font-family: var(--f-sans); font-size: var(--t-small);
              line-height: var(--t-small-lh); font-weight: 500; white-space: nowrap; }
}
@media (min-width: 80rem) {                 /* nella riga dell'header, glifo solo */
  .nav-door { inline-size: 40px; padding-inline: 0; }
  .nav-door__label {                        /* resta nel DOM: è il nome accessibile */
    position: absolute; inline-size: 1px; block-size: 1px; overflow: hidden;
    clip-path: inset(50%); white-space: nowrap; border: 0; padding: 0; margin: -1px;
  }
}
@media (max-width: 47.999rem) {             /* riga piena in fondo al foglio del drawer */
  .nav-door { display: flex; min-block-size: 56px; inline-size: 100%;
              justify-content: flex-start; padding-inline: var(--s-4);
              font-size: var(--t-body); line-height: var(--t-body-lh); font-weight: 500;
              touch-action: manipulation; }
}
```

### 7.4 Il pannello (≥ 80rem) e lo stato senza JS

```css
@media (min-width: 80rem) {
  .main-nav__panel {
    position: absolute; inset-inline: 0; inset-block-start: 100%;
    z-index: 1;                       /* vedi la nota sull'impilamento locale, sotto */
    display: grid; min-block-size: var(--nav-panel-h);
    padding-block: var(--s-8); padding-inline: 0;
    background: var(--min-3); box-shadow: var(--shadow-3);
    border: 0; border-radius: 0; overflow: hidden;
    opacity: 0; visibility: hidden; transform: translateY(-8px);
  }
  .main-nav__item[data-open="true"] > .main-nav__panel,
  html.no-js .main-nav__item:hover > .main-nav__panel,
  html.no-js .main-nav__item:focus-within > .main-nav__panel {
    opacity: 1; visibility: visible; transform: none;
  }

  .main-nav__panel-inner {               /* è la .container dell'header, riusata */
    display: grid; grid-template-columns: repeat(12, minmax(0, 1fr));
    column-gap: var(--grid-gutter); align-content: center; min-block-size: 224px;
  }
  .main-nav__panel-lead { grid-column: 1 / span 3; display: flex; flex-direction: column;
                          gap: var(--s-3); border: 0; padding: 0; }
  .main-nav__panel-title { margin: 0; font-family: var(--f-serif); font-size: var(--t-entry);
                           line-height: var(--t-entry-lh); font-weight: 400; color: var(--ink); }
  .main-nav__panel-desc  { margin: 0; font-size: var(--t-small); line-height: var(--t-small-lh);
                           color: var(--ink-2); max-inline-size: 28ch; }

  .main-nav__sublist { grid-column: 4 / span 6; display: grid; gap: 0; align-content: start;
                       margin: 0; padding: 0; list-style: none; }
  .main-nav__sublist--two { grid-template-columns: repeat(2, minmax(0, 1fr));
                            column-gap: var(--s-8); }
  .main-nav__panel[data-children="1"] .main-nav__sublist,
  .main-nav__panel[data-children="2"] .main-nav__sublist { grid-column: 4 / span 4; }

  .main-nav__sublink {
    position: relative; display: flex; align-items: center; justify-content: space-between;
    gap: var(--s-3); min-block-size: 48px; padding-inline: var(--s-3);
    font-size: var(--t-ui); line-height: var(--t-ui-lh); color: var(--ink);
    text-decoration: none; border-block-end: 1px solid var(--hairline); border-radius: 0;
  }
  .main-nav__sublink .icon { order: 2; inline-size: 16px; block-size: 16px; color: var(--ink-3); }
  .main-nav__sublink::before {                       /* la linea d'ormeggio */
    content: ""; position: absolute; inset-block: 0; inset-inline-start: 0; inline-size: 2px;
    background: var(--accent); transform: scaleX(0); transform-origin: 0 50%;
  }
  [dir="rtl"] .main-nav__sublink::before { transform-origin: 100% 50%; }
  .main-nav__sublink:hover::before,
  .main-nav__sublink:focus-visible::before,
  .main-nav__sublink[aria-current]::before { transform: scaleX(1); }
  .main-nav__sublink[aria-current] { font-weight: 500; }

  .main-nav__mark { grid-column: 10 / span 3; justify-self: end; align-self: center;
                    inline-size: 120px; block-size: 120px; opacity: .10; color: var(--ink); }
  .main-nav__panel[data-children="1"] .main-nav__mark,
  .main-nav__panel[data-children="2"] .main-nav__mark { grid-column: 9 / span 4; inline-size: 160px; }

  /* senza JS la voce corrente conserva il suo segno, perché la traccia è progressive enhancement */
  html.no-js .main-nav__link[aria-current]::after {
    content: ""; position: absolute; inset-inline: 6px; inset-block-end: 4px;
    block-size: 2px; background: var(--accent);
  }
  html.no-js .main-nav__link { position: relative; }
  html.no-js .site-header__trace { display: none; }
}
@media (max-width: 79.999rem) {
  html.no-js .main-nav__panel { display: block; }    /* tutto visibile nel drawer */
}
```

### 7.5 Drawer, barra, lingua, forced-colors

```css
@media (max-width: 79.999rem) {
  .nav-drawer { background: var(--min-2); border-block-start: 1px solid var(--hairline);
                box-shadow: var(--shadow-5); }
  .main-nav__list { display: grid; }
  .main-nav__item { flex-wrap: wrap; border-block-end: 1px solid var(--hairline); }
  .main-nav__link, .main-nav__label {
    flex: 1 1 auto; min-block-size: 52px; padding-inline: var(--s-1);
    font-family: var(--f-sans); font-size: var(--t-entry); line-height: var(--t-entry-lh);
    font-weight: 500; color: var(--ink); border-block-end: 0;   /* mai il secondo filetto */
    white-space: normal; touch-action: manipulation;
  }
  .main-nav__toggle { inline-size: 52px; min-block-size: 52px; touch-action: manipulation; }
  .main-nav__panel { flex-basis: 100%; background: var(--min-1); padding: 0 0 var(--s-4); }
  .main-nav__panel-title { display: none; }
  .main-nav__sublink { min-block-size: 48px; padding-inline-start: var(--s-4);
                       border-block-end: 0; }
  .main-nav__mark { display: none; }
  .nav-overlay { inset-block-start: var(--nav-drawer-top, var(--header-height)); }
}

.utility-bar { background: var(--min-1); block-size: var(--utility-height); }   /* §8.2: --min-1 */
.utility-bar__identity { font-size: var(--t-caption); line-height: var(--t-caption-lh);
                         color: var(--ink-2); margin: 0; }   /* 6,00:1 su --min-1 */

.lang-seg { display: flex; align-items: center; gap: var(--s-1); }
.lang-seg__link { display: inline-flex; align-items: center; justify-content: center;
                  min-inline-size: 28px; min-block-size: 28px;
                  font-family: var(--f-mono); font-size: var(--t-folio);
                  letter-spacing: var(--track-folio); color: var(--ink-2);
                  text-decoration: none; }
.lang-seg__link[aria-current] { color: var(--ink); font-weight: 500;
                                box-shadow: inset 0 -2px 0 var(--accent); }
.lang-seg__sep { color: var(--hairline-strong); }      /* 3,59:1, aria-hidden */
.lang-seg__link:lang(ar) { letter-spacing: 0; }
@media (max-width: 47.999rem) { .lang-seg__link { min-inline-size: 44px; min-block-size: 44px; } }

@media (forced-colors: active) {
  .site-header__seam, .site-header__trace { background: CanvasText; }
  .site-header__seam::before { display: none; }
  .main-nav__panel { background: Canvas; border: 1px solid CanvasText; box-shadow: none; }
  .main-nav__sublink::before { background: Highlight; }
  .main-nav__mark { display: none; }
  .nav-door { background: Canvas; color: CanvasText; border: 1px solid CanvasText; }
  .lang-seg__link[aria-current] { box-shadow: inset 0 -2px 0 Highlight; }
}
```

### 7.6 Moto — tutto dentro un blocco solo

```css
@media (prefers-reduced-motion: no-preference) {
  .site-header { transition: background-color var(--motion-slow) var(--ease-standard); }
  .site-header::after { transition: opacity var(--motion-slow) var(--ease-standard); }
  .site-header__seam::before { transition: transform var(--motion-slow) var(--ease-standard); }
  .main-nav__panel { transition: opacity var(--motion-base) var(--ease-out),
                                 transform var(--motion-base) var(--ease-out),
                                 visibility 0s linear var(--motion-base); }
  .main-nav__item[data-open="true"] > .main-nav__panel { transition-delay: 0s; }
  .main-nav__sublink::before { transition: transform var(--motion-fast) var(--ease-out); }
  .main-nav__sublink:not(:hover)::before { transition: transform var(--motion-instant) var(--ease-in); }
  .main-nav__sublink .icon { transition: transform var(--motion-fast) var(--ease-out); }
  .main-nav__sublink:hover .icon, .main-nav__sublink:focus-visible .icon { transform: translateX(4px); }
  [dir="rtl"] .main-nav__sublink:hover .icon { transform: translateX(-4px); }
  .main-nav__toggle .icon { transition: transform var(--motion-fast) var(--ease-standard); }
  .nav-door { transition: background-color var(--motion-fast) var(--ease-out); }
}
```

Fuori da quel blocco: il pannello aperto è opaco, completo e fermo; la graticola è al valore finale
del proprio stato; la traccia è posizionata senza molla (`nav.js` chiama `withMotion` e la funzione
di assestamento scrive direttamente `--trace-x` / `--trace-w`); il chevron non trasla. **Nessun
contenuto sparisce, nessun elemento resta a opacità 0, nessuna informazione è veicolata solo dal
moto.** Nessuna dichiarazione `transition` o `@keyframes` di `v3/nav.css` esiste fuori da questo
blocco: §7.1–§7.5 non ne contengono nemmeno una, e il test 8 lo verifica sul CSS compilato.

---

## 8. I TEMPLATE

### 8.1 `partials/header.html` — due nodi nuovi, nient'altro

```django
<header class="site-header" id="site-header">
  <div class="container site-header__inner">
    <a class="brand brand--lockup" href="{% url 'pages:home' %}"
       aria-label="{{ site.project_name }} — {% translate 'accueil' %}">…</a>   {# invariato #}
    <button class="nav-toggle" type="button" data-nav-toggle
            aria-controls="nav-drawer" aria-expanded="false">…</button>          {# invariato #}
    <div class="nav-drawer" id="nav-drawer" data-nav-drawer>
      <nav class="main-nav" aria-label="{% translate 'Navigation principale' %}">
        {% include "partials/main_nav.html" %}
      </nav>
      {% include "partials/_reserved_door.html" with door_class="nav-door--drawer" %}   {# < 48rem #}
      <div class="drawer-utility">                        {# < 48rem : imprint + lingue #}
        <p class="drawer-utility__identity"><strong>{{ site.promoter }}</strong> — {% translate "promoteur du projet" %}</p>
        {% include "components/language_switcher.html" with variant="segments" %}
      </div>
    </div>
    {% include "partials/_reserved_door.html" with door_class="nav-door--row" %}        {# >= 48rem #}
  </div>
  <span class="site-header__seam" aria-hidden="true"><i class="site-header__trace"></i></span>
  <div class="nav-overlay" data-nav-overlay></div>
</header>
```

`_reserved_door.html` è incluso due volte **ma esposto una volta sola**, e la selezione è CSS, non
logica di vista: le due inclusioni passano `door_class` (`{% include "partials/_reserved_door.html"
with door_class="nav-door--drawer" %}` dentro il foglio, `door_class="nav-door--row"` nella riga) e
le due regole sono esclusive per larghezza:

```css
@media (min-width: 48rem) { .nav-door--drawer { display: none; } }
@media (max-width: 47.999rem) { .nav-door--row { display: none; } }
```

`display: none` **toglie il nodo dall'albero di accessibilità**, quindi a qualunque larghezza esiste
esattamente un ingresso all'area riservata per lo screen reader e per la tastiera. È l'unico punto
della specifica in cui un nodo è duplicato nel DOM, ed è duplicato perché il suo posto nell'ordine di
lettura cambia con la larghezza e nessuna proprietà CSS può spostare un nodo fra due genitori senza
rompere `order` = ordine di tabulazione (§4.7 vieta `order`).

### 8.2 `partials/_reserved_door.html` — la guardia, verbatim

```django
{% load i18n %}{# flag · safe_url · svg_icon sono builtins: config/settings/base.py:143 #}
{% flag "reserved_area_public_link" as reserved_link %}
{% if user.is_authenticated %}
  {% include "components/account_menu.html" %}
{% elif reserved_link and site.settings.reserved_area_enabled %}
  {% safe_url 'account_login' as login_url %}
  {% if login_url %}
  <a class="nav-door {{ door_class }}" href="{{ login_url }}">
    <span class="nav-door__glyph">{% svg_icon "key" "icon" %}</span>
    <span class="nav-door__label">{% translate "Espace réservé" %}</span>
  </a>
  {% endif %}
{% endif %}
```

Le tre condizioni sono quelle che `utility_bar.html:9-14` e `header.html:26-30` portano oggi —
`{% flag "reserved_area_public_link" %}` **e** `site.settings.reserved_area_enabled` **e** un
`{% safe_url 'account_login' %}` non vuoto — nello stesso ordine, con lo stesso ramo
`user.is_authenticated` verso `account_menu.html`. Nessuna condizione è aggiunta, nessuna è tolta.
Il round 1 ne lasciava cadere due: quel markup è cancellato.

### 8.3 `partials/utility_bar.html`

```django
<div class="utility-bar" role="region" aria-label="{% translate 'Barre institutionnelle' %}">
  <div class="container utility-bar__inner">
    <p class="utility-bar__identity"><strong>{{ site.promoter }}</strong><span class="hide-mobile"> — {% translate "promoteur du projet" %}</span></p>
    {% include "components/language_switcher.html" with variant="segments" %}
  </div>
</div>
```

**Il qualificatore «— promoteur du projet» resta** (MUST-FIX 16 della lista lacune): è una frase di
attribuzione, non un'etichetta, e `hide-mobile` continua a governarla come oggi. La classe
`on-inverse` sparisce insieme al fondo scuro che non c'è più. Misura: identità 387 (fr) · 404 (it) ·
405 (en) · 377 (ar) px a `--t-caption` 12/16; segmenti 148 px; riquadro 1096 px a 1280 → **543 px
liberi nel caso peggiore**.

### 8.4 `components/language_switcher.html` — `variant`, e il glifo arabo

Il partial prende un parametro `variant`. **`variant` assente ⇒ comportamento identico a oggi**
(`<details>`), perché `portal_chrome.html:32` — la shell della piattaforma autenticata — include
questo stesso file e **non è toccata da questa specifica**. Il round 1 non lo diceva; ora è detto, e
il default è la non-regressione.

```django
{% if variant == "segments" %}
<nav class="lang-seg" aria-label="{% translate 'Choisir la langue' %}">
  {% for l in site.languages %}
    {% if not forloop.first %}<span class="lang-seg__sep" aria-hidden="true">·</span>{% endif %}
    <a class="lang-seg__link" href="{{ l.url }}" lang="{{ l.code }}" hreflang="{{ l.code }}"
       dir="{{ l.dir }}"{% if l.active %} aria-current="true"{% endif %}>
      <span aria-hidden="true">{% if l.code == "ar" %}ع{% elif l.code == "fr" %}FR{% elif l.code == "it" %}IT{% elif l.code == "en" %}EN{% else %}{{ l.code|upper }}{% endif %}</span>
      <span class="visually-hidden">{{ l.name }}</span>
    </a>
  {% endfor %}
</nav>
{% else %}
  … il <details> di oggi, invariato …
{% endif %}
```

La mappa dei glifi è esplicita perché `{{ l.code|upper }}` non può produrre «ع» (produrrebbe «AR»),
e §8.2 prescrive «FR · IT · EN · ع». Il ramo `{% else %}` finale copre una lingua futura. Il nome
completo resta nel DOM in `.visually-hidden`, quindi ogni segmento ha un nome accessibile leggibile
(«Français», «العربية»), mai il solo codice. La lingua è **navigazione**: `<a>` + `aria-current`,
nessun `role="radio"`, nessuno stato di modulo. Misure: segmento mono 13 px = 17,7 px di glifo
(«FR»/«IT»/«EN») e 7,1 px («ع») dentro un target di 28 × 28 (≥ 24 px, WCAG 2.5.8), 44 × 44 nel drawer;
larghezza totale `4 × 28 + 3 × 4 + 6 × 4 = 148 px`.

### 8.5 `partials/main_nav.html`

Due sole modifiche: `main-nav__item--end` sparisce (il pannello non è più ancorato alla voce), e il
pannello porta `data-children` per la griglia di §7.4. Il resto — `data-nav-item`, `data-nav-panel`,
`data-nav-panel-toggle`, `aria-expanded`, `aria-controls="{{ item.id }}-panel"`, `aria-current`,
`main-nav__label` per la sezione senza URL — è **invariato**, perché è il contratto che il modello
tastiera di `main.js` già usa.

```django
<ul class="main-nav__list">
{% for item in menu %}
  <li class="main-nav__item"{% if item.children %} data-nav-item{% endif %}>
    {% if item.url %}<a class="main-nav__link" href="{{ item.url }}" data-nav-link …>{{ item.label }}</a>
    {% else %}<span class="main-nav__label">{{ item.label }}</span>{% endif %}
    {% if item.children %}
    <button class="main-nav__toggle" type="button" data-nav-panel-toggle aria-expanded="false"
            aria-controls="{{ item.id }}-panel">…</button>
    <div class="main-nav__panel" id="{{ item.id }}-panel" data-nav-panel
         data-children="{{ item.children|length }}">
      <div class="container main-nav__panel-inner">
        <div class="main-nav__panel-lead">…</div>
        <ul class="main-nav__sublist{% if item.children|length > 4 %} main-nav__sublist--two{% endif %}">…</ul>
        <span class="main-nav__mark" aria-hidden="true">{% svg_icon "arch-steps" "icon" %}</span>
      </div>
    </div>
    {% endif %}
  </li>
{% endfor %}
</ul>
```

`arch-steps` è l'unico simbolo nuovo richiesto a `static/img/icons.svg` (il set contiene oggi
`person user building institution university briefcase arrow arrow-up-right check warning shield
calendar clock document globe menu close chevron chevron-end plus minus search mail phone lock key
info map-pin download home logout settings quote list handshake compass`). Il disegno è quello di
`BRAND_ASSETS.md` §2, tratto 1.5, `currentColor`, `aria-hidden`.

---

## 9. ACCESSIBILITÀ, RTL, CONTRASTI

**Resta identico**: il modello tastiera di `main.js` (frecce fra le voci di primo livello,
`ArrowDown` apre e porta il focus al primo elemento, `Escape` chiude il più interno e restituisce il
focus, `focusout` chiude su desktop, trappola di focus nel drawer), `aria-expanded`, `aria-current`,
`aria-controls`, il breakpoint 80rem, le regole del lock-up (`direction: ltr`, scala come unità,
nessuna tagline). `nav.js` **non duplica nulla di tutto questo**.

**Cambia**: l'hover apre il pannello *in aggiunta* al clic e scrive lo stesso `aria-expanded`, quindi
stato visivo e stato annunciato non divergono mai. La porta ha un nome accessibile permanente
(`.nav-door__label` resta nel DOM anche quando è visivamente nascosta: mai `display:none` su di essa,
mai un `aria-label` che sostituisca il testo). La lingua passa da `<details>` a quattro link con
`aria-current="true"`, `lang`, `hreflang`, `dir`.

**Target**: voci 44 px (desktop) e 52 px (drawer); toggle 24 × 44 e 52 × 52; segmenti 28 × 28 e
44 × 44; porta 40 × 64, 150,8 × 64 e 56 px a tutta larghezza. Tutti ≥ 24 px (WCAG 2.5.8 AA), la
maggior parte ≥ 44.

**Il colore non è mai solo**: voce corrente = traccia **+** `--ink` **+** peso 500; riga corrente =
linea d'ormeggio **+** peso 500; lingua attiva = filetto **+** peso **+** `aria-current`; porta =
glifo **+** nome accessibile **+** forma (lastra piena a filo di riga), non solo il teal.

**Contrasti** (WCAG 2.x, calcolati sui token di `v2/tokens.css`; le composizioni alfa sono calcolate,
non stimate):

| Coppia | Rapporto | Ruolo |
|---|---:|---|
| `--ink-2` / `--min-2` | **6,87** | voci della navigazione a riposo |
| `--ink` / `--min-2` | **15,56** | voce corrente |
| `--ink-2` / vetro scrollato `#dedfdf` | **5,38** | voci sul vetro (caso peggiore: capitolo mezzanotte sotto) |
| `--ink` / `--min-3` | **16,23** | righe del pannello |
| `--ink-3` / `--min-3` | **6,14** | chevron del pannello |
| `--accent` / `--min-2` | **6,05** | traccia, bordo della lastra della porta |
| `--accent` / `--min-3` | **6,32** | linea d'ormeggio |
| `--min-0` / `--accent` | **5,69** | glifo ed etichetta della porta |
| `--min-0` / `--accent-hover` | **7,44** | porta in hover |
| `--accent-ring` / `--min-2` | **3,94** | anello di focus su carta (≥ 3 : 1, non testo) |
| `--accent-ring` / vetro scrollato | **3,09** | **insufficiente come margine → DEROGA 3** |
| `--accent-hover` / vetro scrollato | **6,39** | anello di focus in `is-scrolled` |
| `--terr-line` / `--mid-1` | **6,07** | la soglia, letta dal lato mezzanotte |
| `--terr-line` / `--min-2` | **2,76** | la soglia, letta dal lato carta (tono, dichiarato) |
| `--terr-line-lt` al 70 % / `--min-2` (`#56959a`) | **3,26** | la graticola (era 1,22 : 1 nel round 1) |
| `--ink-2` / `--min-1` | **6,00** | imprint della barra istituzionale |
| `--hairline-strong` / `--min-1` | **3,59** | separatore «·» fra i segmenti lingua |
| `--ink` al 10 % / `--min-3` (`#e8e9ea`) | **1,22** | il glifo a secco nel margine — **deliberatamente sotto soglia, non porta informazione**, `aria-hidden`, soppresso in `forced-colors` |
| carta all'**82 %** su mezzanotte (`#d0d2d2`) | ink-2 **4,72** · accent **4,16** | il pavimento che si rifiuta: **88 % è il minimo**, da inchiodare in `tests/frontend/` |

**Nessun testo su alfa.** Le uniche opacità del file sono su grafica (`::after` dell'ombra, graticola,
glifo a secco) e sul pannello durante la transizione.

**RTL**: tutte le proprietà sono logiche (`inset-inline`, `padding-inline`, `inset-block-*`,
`border-block-end`, `transform-origin` logica dove serve). La traccia non ha segno da invertire nel
JS perché il segno vive in `--dir` nel CSS e la misura è logica (verificato: AR a 1440, `--trace-x
622,3`, traccia resa a `x 771,7`, larghezza 46,0). Il pannello a tutta larghezza cancella i due
`@keyframes` speculari e i due `translateX(±50%)`, **che vanno cancellati e non sovrascritti**
(§4: misurato, `[dir="rtl"] .main-nav__panel { transform: translateX(50%) }` vince per specificità e
sposta il pannello a `x = 720` su 1440). `:lang(ar)` azzera `letter-spacing` sui codici lingua; il
lock-up conserva il suo `.13em` e la sua `direction: ltr`.

**`forced-colors`**: §7.5. Il pannello prende `Canvas` e `1px solid CanvasText`; filo e traccia
`CanvasText`; l'ormeggio `Highlight`; graticola e glifo spariscono e **il pannello resta completo**,
perché nessuno dei due porta informazione.

**HUMAN_QA_REQUIRED**: (a) lettura NVDA/VoiceOver dell'apertura a hover e del cambio di sezione senza
chiusura intermedia; (b) verifica che il solo marchio a 1280–1439 sia accettato dal committente come
applicazione di §8.1 e non come perdita (è l'unica scelta di questa specifica che tocca la
presentazione del marchio, e non ne altera il disegno); (c) prova a 320 px con porta e toggle;
(d) rilettura di `apps/cms/forbidden.py` contro tutte le etichette rese (questa specifica non
introduce alcuna stringa nuova, ma la verifica è dovuta); (e) giudizio sul glifo a secco a 1,22 : 1
su uno schermo reale e su un pannello Windows ad alto contrasto.

---

## 10. PRESTAZIONI E TEST

| Voce | Costo |
|---|---|
| `static/css/v3/nav.css` | ≤ **12 000 B grezzi / ≤ 2 900 B gzip** (cap, non stima; asserito dal test 7) |
| Cancellazioni (`components.css` 484–1000 + `v2/shell.css` 190–371) | **−16 753 B grezzi / −3 318 B gzip**, misurati ricomprimendo la catena intera prima e dopo (205 579 / 46 298 → 188 826 / 42 980) |
| **Netto CSS** | **≤ −418 B gzip: la catena CSS si accorcia** |
| `static/js/dist/nav.js` | ≈ 6 000 B grezzi / ≈ **1 900 B gzip**, cap a 2 500 B (base di stima: `dist/shell.js` 1 136 / 613 per ~80 righe; `main.js` 19 944 / 5 309 per ~560 righe). Nessuna importazione nuova: siede sul chunk Motion già caricato (70 441 / 26 143) |
| **Totale JS per pagina** | 32 460 → **≤ 34 960 B gzip** contro il tetto di **45 KB** |
| Immagini della navigazione | **0 B**, a ogni DPR, in ogni stato, su ogni viewport |
| Graticola, tacche, ormeggi, glifo | 0 B di asset (`repeating-linear-gradient` + un simbolo nello sprite già caricato) |

**Paint e layout.** Le animazioni sono `transform` e `opacity`, più due transizioni di colore su box
piccoli (header e porta): **0 layout e 0 paint oltre il primo frame** attesi nel pannello Performance.
L'altezza costante del pannello elimina l'unica animazione di `height` che il disegno avrebbe potuto
richiedere in configurazione reale. `--shadow-2` non transisce mai: transisce l'`opacity` del suo
portatore. Il `backdrop-filter` resta **uno solo per pagina**, sull'header, come §2 livello 6
prescrive. Nessun `filter`, nessun loop.

**Test obbligatori** (`tests/frontend/`, `tests/i18n/`):

1. **Larghezza della riga** — a 1280 · 1366 · 1440 · **1536** · 1600 · 1920, in `fr it en ar`, su
   :8771 **e** :8770: fallisce se `header.scrollWidth > header.clientWidth`, o se la somma dei figli
   della riga supera il riquadro interno, o se il margine FR a 1440 scende sotto **+16 px**.
2. **Ancoraggio del pannello** — `panel.offsetParent === document.querySelector('.site-header')`,
   `panel.getBoundingClientRect().width === header.getBoundingClientRect().width`,
   `panel.top === header.bottom`, in LTR e RTL.
3. **Allineamento** — il bordo di lettura di `.main-nav__panel-lead` coincide con quello di `.lock`
   entro 0,5 px, a 1280 · 1440 · 1600, in LTR e RTL.
4. **Pavimento del vetro** — `getComputedStyle('.site-header.is-scrolled').backgroundColor` ha alfa
   ≥ 0,88; fallisce sotto.
5. **Il lock-up non si muove** — rettangolo e `transform` di `.site-header .lock` identici prima e
   dopo `scrollTo(0, 900)`, a 1440 e a 1600.
6. **Soglia coerente** — `body.chapter-first-dark` ⟺ il primo `<section>` dentro `<main>` ha
   `chapter--dark`, su ogni rotta pubblica e in ogni lingua.
7. **Pesi** — `v3/nav.css` ≤ 2 900 B gzip; `dist/nav.js` ≤ 2 500 B gzip; totale JS di pagina
   ≤ 45 000 B gzip.
8. **Moto** — nessun `cubic-bezier` oltre i tre token nel CSS compilato; nessuna `transition` o
   `@keyframes` di `v3/nav.css` fuori da `prefers-reduced-motion: no-preference`; nessuna
   dichiarazione che animi `box-shadow`, `filter`, `width`, `height`, `top` o `left`.
9. **Senza JS** — con `html.no-js`, il pannello è raggiungibile su `:hover` e `:focus-within` a
   ≥ 80rem ed è aperto nel drawer sotto, e `.main-nav__link[aria-current]` ha un segno visibile.
10. **Un solo ingresso riservato** — a 390 · 768 · 1280 · 1600, esattamente un elemento corrispondente
    a `a.nav-door` è nell'albero di accessibilità; e con `reserved_area_enabled = False` oppure il
    flag spento oppure la rotta non risolvibile, **zero**.
11. **Target** — ogni controllo della navigazione misura ≥ 24 px sui due assi, a 390 · 768 · 1440.
12. **Wording** — `apps/cms/forbidden.scan()` su ogni rotta pubblica in `fr it en ar` resta vuoto
    (invariato, ma la navigazione è ora nel percorso di rendering di ogni pagina).

---

## 11. RISCHI E GUARDIE

1. **Il solo marchio a 1280–1439 legge come una perdita.** *Guardia*: è la scala d'unità di §8.1
   applicata dove la misura la richiede (1218,8 px richiesti contro 1096,0 disponibili), e le tre
   alternative sono peggiori e documentate: un 13,5 px fuori scala (ciò che esiste oggi, con zero
   pixel di margine), un hamburger a 1280, o una deroga sul breakpoint di navigazione che §4 del
   design system dichiara invariato. Decisione da confermare in HUMAN_QA (b).
2. **Il margine FR a 1440 è di 21,2 px.** *Guardia*: il test 1 fallisce sotto +16 px; due valvole
   misurate (padding 4 px → +49,2; gap 2 px → +61,2) sono già scelte e ordinate. Nessuna riduce il
   numero di voci.
3. **La porta piena compete con la CTA primaria dell'hero.** *Guardia*: forma diversa (raggio 0 contro
   2), misura diversa (40 contro ~350 px), altezza di riga contro 48 px, posizione fuori dalla colonna
   di lettura, e costanza assoluta — è cromo, come il lock-up. Verificabile con uno screenshot a
   `scrollY = 0` su HOME.
4. **Un pannello con due figli sembra vuoto.** *Guardia*: `data-children` porta i collegamenti a 4
   colonne e il glifo a 160 px; verifica obbligatoria su «Entreprises» (2 figli su :8771, 1 su :8770)
   prima del merge.
5. **L'apertura a hover fa sfarfallare il menù.** *Guardia*: intento 120 ms in ingresso, grazia 180 ms
   in uscita, solo sotto `(hover: hover) and (pointer: fine)`; e poiché il pannello è a filo della
   barra non esiste il varco diagonale che costringe al «triangolo sicuro».
6. **Il vetro viene reso più trasparente «perché è più bello».** *Guardia*: all'82 % le voci scendono
   a 4,72 : 1 e l'accento a 4,16 : 1. **88 % è il pavimento**, inchiodato dal test 4.
7. **La cancellazione di `components.css` §7 e di `v2/shell.css` 190–371 viene rimandata e si
   sovrascrive «per sicurezza».** *Guardia*: misurato, in arabo il pannello finisce a mezzo viewport
   di distanza finché `[dir="rtl"] .main-nav__panel { transform: translateX(50%) }` esiste. La
   cancellazione è parte della specifica, non una pulizia successiva; il test 2 la sorveglia.
8. **La classe `chapter-first-dark` si scorda su una pagina nuova.** *Guardia*: il test 6 la confronta
   con la realtà del DOM su ogni rotta pubblica, in ogni lingua.
9. **`portal_chrome.html` regredisce.** *Guardia*: `language_switcher.html` senza `variant` rende
   esattamente il `<details>` di oggi; la shell autenticata non è toccata e nessun test suo cambia.
