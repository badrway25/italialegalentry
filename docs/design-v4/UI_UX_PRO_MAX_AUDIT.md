# UI-UX-Pro-Max — audit per pagina campione (V4)

Data: 24 settembre 2026 · Strumento: plugin `ui-ux-pro-max-skill` **2.13.0** (utente), script locale
`scripts/search.py`, 119 linee guida UX + tassonomie di stile/colore/tipografia/moto · 28 interrogazioni,
grezzo in sessione (`uiux_mes_documents.txt`, `uiux_pages.txt`).

## 0. Che cosa lo strumento è, e come va letto — riscritto dopo il chiarimento delle 20:58

È un **archivio locale di competenza UX** con una ricerca testuale per dominio: 119 linee guida,
79 stili, 192 palette con profili di ragionamento, 74 abbinamenti tipografici, 17 preset di moto.
Non guarda la pagina e non misura; risponde a parole chiave con la voce più vicina. Il committente
ha chiarito come usarlo: **fonte di competenza, non design system da accettare o respingere in
blocco**. Percorso: SKILL RECOMMENDATION → EXPERT ANALYSIS → PROJECT ADAPTATION → LIVE PROTOTYPE →
CHROME REVIEW.

Quindi la sua prima proposta («Trust & Authority», navy `#1E3A8A` + oro `#B45309`, EB Garamond/Lato,
Google Fonts) **non è respinta in blocco**; è analizzata elemento per elemento in §11, insieme a
undici analisi per superficie con problem statement specifici. In sintesi: il **navy** entra in V4
come colore di sistema dei capitoli scuri, evoluto dal navy ufficiale del marchio; **Garamond no**
come UI (accentua l'estetica editoriale rifiutata), al più un uso display che il Creative Director
può decidere; le **Google Fonts** non si collegano in rete — un font open-source valido si
self-hosta, come già Fira e Newsreader.

Dove una risposta è fuori tema (la ricerca testuale ha restituito «breadcrumbs» per «gerarchia delle
azioni», «bulk actions» per «wizard», «Claymorphism — toy-like» per un wizard istituzionale) è
annotato come tale: un'interrogazione che non trova nulla di pertinente non è una raccomandazione.

Legenda: **ACCETTATA** = entra nel Design System V4 o nella pagina · **RESPINTA** = con la ragione ·
**GIÀ** = era già così, la regola conferma · **IMPLEMENTATA** = riferimento al commit quando c'è.

---

## 1. Mes Documents — pagina pilota e di controllo

**CURRENT PROBLEM** (Chrome visibile, 1440 e 390, BEFORE `05_mes_documents.png`): titolo serif da
rivista che domina; sidebar di soli link con una riga verticale; tabella da documento amministrativo;
azioni come link sottolineati («Consulter», «Accepter les Conditions d'utilisation»); «Bloqué» come
chip nella colonna ACTION invece che come controllo disabilitato con spiegazione; nessuna gerarchia
fra documento, stato, scadenza e azione; nessun filtro; nessun riepilogo di salute; nessun hover, focus
di riga, moto; a 390 px la tabella scorre lateralmente (`.scroll-x`), l'azione principale non è
raggiungibile senza scorrere.

| Tema | SKILL RECOMMENDATION (query → regola) | Esito | Decisione V4 |
|---|---|---|---|
| gerarchia dell'informazione | `document list rows status actions workspace` → «Submit Feedback: loading poi success/error» | **fuori tema** per la gerarchia; **ACCETTATA** per il caricamento file | l'azione di deposito mostra in carico → accettato / errore, mai silenzio |
| pattern di workspace | nessuna regola di «document workspace» nell'archivio | — | dalla direttiva §16 e da 21st (riga documento, categoria 8) |
| gerarchia delle azioni | `primary secondary action hierarchy row menu` → «Breadcrumbs: usali con 3+ livelli» | **fuori tema** | primaria = bottone, secondaria = menu, bloccata = controllo disabilitato + spiegazione (§20) |
| trattamento degli stati | `status badge chip semantic color icon label` → «Compact Label Overflow: nowrap, etichetta comprimibile, testo intero operabile» (High) | **ACCETTATA — e già misurata**: «À faire» andava a capo a 44 px | chip senza ritorno a capo nelle celle; testo intero sempre visibile (`d657264`) |
| strategia responsive | `table responsive mobile cards stacked` → «Table Handling: scorrimento orizzontale **o** schede» | **ACCETTATA nella seconda metà**: schede impilate su mobile (§61); lo scorrimento resta solo per le tabelle dello staff | `DocumentCard` sotto 768 px |
| stati vuoto/errore | `empty state guidance action` → «messaggio utile + azione, mai schermo bianco» | **GIÀ** (componente `empty_state`), forma da rifare in V4 | `EmptyState` V4 con glifo, frase, azione |
| filtro | `filter segmented control tabs selection` → «Chip Collection Reflow: le collezioni di chip vanno a capo o mostrano +n» (High) | **ACCETTATA** per i filtri; il segmentato va a capo sotto 480 px | `SegmentedControl` con reflow |
| scadenze | `deadline urgency progressive indicator` → «Focus States» | **fuori tema** | urgenza progressiva da §19: normale · prossima · imminente · scaduta, con parola + glifo + tono, mai solo colore |
| sidebar | `sidebar navigation rail icons collapse active` → «Active State: evidenzia la voce corrente» (Medium) | **GIÀ** (`aria-current` + barra); insufficiente per §15 | rail con icone e indicatore che trasla (21st cat. 1) |
| moduli | `form field validation inline error hint` → «errore specifico sotto il campo, `aria-describedby`» (High) | **GIÀ** (`form_field.html`, Django 5.2) | conservato in V4 |

**IMPLEMENTATA:** una voce (nowrap nelle celle, `d657264`). Il resto attende il Design System V4 e
la ricostruzione della pagina come workspace (passo 10).

## 2. Homepage pubblica

**CURRENT PROBLEM** (BEFORE `01_home.png`): coordinate «33.97° N · 6.85° W» e «45.41° N · 11.88° E»,
il testo «svg» e il comando «Suspendre le mouvement» visibili nella striscia sotto l'hero — decorazione
pseudo-tecnica senza valore (§5); l'hero non spiega ancora le quattro vie; sezioni a densità uniforme;
nessuna fotografia.

| SKILL RECOMMENDATION | Esito | Decisione |
|---|---|---|
| `hero primary action clarity above fold` → «Heading Clarity: differenza netta di corpo/peso» | **GIÀ** | il titolo bloccato resta l'H1 |
| `scroll reveal animation motion meaning reduced motion` → «Reduced Motion» (High) · «**Excessive Motion: anima 1–2 elementi chiave per vista al massimo**» (High) · «Motion Sensitivity» | **ACCETTATA** — diventa il budget di §67: IMMERSIVE ≤ 2 elementi animati per vista, dashboard MICRO | Motion System V4, «due per vista» |
| `landing hero storytelling` (`--domain landing`) → nessun risultato | — | dalla direttiva §33: tre livelli d'intensità |

**Decisioni non dallo skill:** rimozione di coordinate, «svg», «Suspendre le mouvement» (§5); il
tracciato delle quattro vie (21st cat. 13); fotografie curate (§34–36).

## 3. Navbar / mega-navigation

**CURRENT PROBLEM** (BEFORE `02_navbar_megamenu.png`): barra piatta; pannello del sottomenu come
rettangolo che spunta; nessuno stato di scroll; lingua e accesso nella barra utilitaria sopra, poco
raggiungibili; nessuna ricerca.

| SKILL RECOMMENDATION | Esito | Decisione |
|---|---|---|
| `mega menu navigation predictable back deep linking` → «Deep Linking: aggiorna l'URL sui cambi di vista» · «Back Button: conserva la cronologia» (High) | **ACCETTATA** per i filtri della piattaforma (stato del filtro nella query string); per il mega-menu non si applica (non è una vista) | filtro documenti in `?état=` |
| `sticky header scroll blur navigation` → «Sticky Navigation: padding pari all'altezza della barra» · «Smooth Scroll» (High) | **GIÀ** (`scroll-padding-block-start`, `scroll-behavior` sotto `no-preference`) | conservato |

**Decisioni non dallo skill:** barra che si compatta e sfuma allo scroll, mega-menu che si espande a
tutta larghezza, indicatore attivo che trasla, ricerca nel pannello (21st cat. 5 e 21).

## 4. Login

**CURRENT PROBLEM** (BEFORE `03_login.png`): carta centrata generica; nessun elemento di marca oltre
il lock-up; nessuna percezione di sicurezza o modernità; campi standard.

| SKILL RECOMMENDATION | Esito | Decisione |
|---|---|---|
| `accessible authentication login form` → «**Accessible Authentication (Minimum)**: consenti gestori di password e incolla; offri un metodo non cognitivo» (Critical) · «Submit Feedback» · «Form Labels» | **ACCETTATA come verifica**: il modulo non deve bloccare l'incolla; passkey fuori scopo; feedback di invio → bottone in stato «in carico» | verifica sul modulo allauth in fase B |
| `password field show hide visibility` → «Password Visibility: toggle mostra/nascondi» (Medium) · «Error Placement» (High) | **ACCETTATA** (toggle, senza icona-only: con etichetta) · **GIÀ** (errore inline) | `PasswordField` V4 |

**Decisioni non dallo skill:** composizione a due pannelli con la porta ad arco a sinistra (21st cat. 6).

## 5. Dashboard Persona

**CURRENT PROBLEM** (BEFORE `04_person_dashboard.png`): titolo serif enorme; fascia contesto dossier
con quattro fatti in fila; prossima tappa come citazione; sequenza «Mon parcours» come indice
editoriale; nessuna visualizzazione del percorso; card assenti dove servirebbero, testo dove
servirebbe una superficie.

| SKILL RECOMMENDATION | Esito | Decisione |
|---|---|---|
| `dashboard cards hierarchy overload` → «Breadcrumbs» · «Heading Hierarchy: livelli sequenziali» · «Font Size Scale» | **fuori tema** il primo; **GIÀ** il secondo | tipografia UI per la piattaforma (§87–88) |
| `next action primary task first` → «Mobile First» · «Render Blocking: inline critical CSS» | **fuori tema**; «inline critical CSS» **RESPINTA** (CSP `style-src 'self'`; i layer sono in preload) | — |

**Decisioni non dallo skill:** testata «Bonjour / contesto / prossima azione», binario del percorso,
composizione asimmetrica invece di otto card uguali (§47).

## 6. Fascicolo digitale

**CURRENT PROBLEM** (BEFORE `06_fascicolo.png`): stessa impostazione editoriale del cruscotto;
sequenza come indice; responsabilità come testo; nessun workspace diviso.

| SKILL RECOMMENDATION | Esito | Decisione |
|---|---|---|
| `progress indicator steps current position` → «Progress Indicators: indicatori di tappa» · «Active State» · «Deep Linking» | **ACCETTATA** (binario con tappa corrente e ancora per tappa) | `JourneyRail` con `aria-current="step"` e ancore |
| `responsibility ownership who does what` → nessun risultato | — | `ResponsibilityBar` da §18: glifo attore + tipo + nome reale |

## 7. Orientation wizard

**CURRENT PROBLEM** (BEFORE `07_orientation_wizard.png`): modulo lungo su una pagina; opzioni come
radio nudi; progresso come barra nativa; nessuna transizione; riepilogo assente.

| SKILL RECOMMENDATION | Esito | Decisione |
|---|---|---|
| `wizard one question per step progress save` → «Progress Indicators» · «Bulk Actions» · «Redundant Entry» | **ACCETTATA** la prima; «Bulk Actions» **fuori tema**; «Redundant Entry» **ACCETTATA** (non richiedere due volte ciò che il profilo sa) | una domanda per schermo, progresso «Étape n sur 7» già bloccato, riepilogo vivo |
| `option cards radio large tap target` → «Touch Target Size» (High) · «Tap Delay: `touch-action`» · «Hover vs Tap» | **ACCETTATA** (`OptionCard` ≥ 48 px, `touch-action: manipulation`, stato di tocco ≠ hover) | `OptionCard` V4 |

## 8. Company dashboard

**CURRENT PROBLEM** (BEFORE `08_company_dashboard.png`): titolo con la ragione sociale in serif;
fatti in dl; bisogni come elenco; nessun senso di prodotto B2B.

| SKILL RECOMMENDATION | Esito | Decisione |
|---|---|---|
| `b2b enterprise dashboard table density` → «Table Handling» | **ACCETTATA** (schede su mobile, tabella semantica su desktop per il registro dei bisogni) | — |

## 9. Trasversali

| Dominio | SKILL RECOMMENDATION | Esito | Decisione |
|---|---|---|---|
| tipografia | `ui typography scale dashboard readable density` (`--domain typography`) → nessun risultato | — | scala UI V4 da §88, decisa dal Design System Lead |
| colore | `institutional trust palette semantic tokens` (`--domain color`) → nessun risultato; `--design-system` → navy/oro da studio legale | **RESPINTA** | palette V2 conservata (un accento, mezzanotte, carta), token semantici estesi |
| moto | `micro interaction timing hover press context aware` → «**Duration Timing: token di moto condivisi**, nessun taglio universale a 150–300 ms» · «Active States» · «Hover States» | **ACCETTATA** — è la struttura di §11 | Motion System V4 con token nominati |
| transizioni di pagina | `page transition` (`--domain gsap`) → «non bloccare la navigazione; **uscita ≤ 250 ms**; precarica; un solo elemento condiviso; indicatore leggero se i dati tardano» | **ACCETTATA** (con Motion/View Transitions, non GSAP: GSAP non è nel progetto) | §45: dissolvenza del contenuto ≤ 250 ms, mai schermo intero |

## 10. Bilancio

- **Decisioni cambiate o fissate dallo skill:** 11 (nowrap dei chip, schede su mobile, reflow dei
  filtri, budget «1–2 elementi animati per vista», stato di carico del deposito, filtro nell'URL,
  toggle password con etichetta, verifica incolla/gestori di password, bersagli ≥ 48 px con
  `touch-action`, token di moto condivisi, uscita di pagina ≤ 250 ms).
- **Confermate (già così):** 6.
- **Respinte con ragione:** 3 (design system generico, inline critical CSS, bulk actions).
- **Fuori tema:** 7 interrogazioni su 28 — il costo di una ricerca testuale su un archivio di regole.

Lo skill non ha prodotto una direzione visiva, e non poteva: la direzione la fissa il Creative
Director (`CREATIVE_DIRECTION.md`) sui vincoli del progetto e sul materiale di 21st.


---

## 11. Analisi per superficie con problem statement (chiarimento delle 20:58)

Undici interrogazioni `--design-system`, ciascuna con un problem statement specifico (es. «premium
2026 legal-tech document workspace… sophisticated, dynamic, contemporary, not editorial or
bureaucratic… avoid generic SaaS and default shadcn»). Lo strumento restituisce per ogni superficie
un pattern di pagina, uno stile, una palette e una coppia tipografica. Ogni elemento è analizzato
separatamente: **EVOLVE** (entra, adattato), **KEEP** (già così), **NO** (con la ragione).

| Superficie | Pattern | Stile | Palette proposta | Analisi esperta → adattamento ILE |
|---|---|---|---|---|
| Document workspace | Enterprise Gateway | Minimalism & Swiss (clean, spacious, functional, high contrast) | navy `#1E3A5F`, CTA **verde** `#16A34A`, fondo `#F8FAFC` | Pattern **EVOLVE**: «gateway» = una testata di workspace con contesto e azione primaria, poi la collezione — è §16. Stile: **EVOLVE** la disciplina svizzera (griglia, densità funzionale) **ma non** il minimalismo bianco: V4 vuole profondità e superfici (§39). Navy: **EVOLVE** come fondo dei capitoli scuri, derivato dal navy del marchio `#0F2547`. CTA verde: **NO** — il verde significherebbe «approvato» (regola legale). Fondo `#F8FAFC` (freddo): **NO**, la carta ILE resta calda; le superfici di livello 1–2 salgono verso il bianco. |
| Navbar | Hero-Centric | Minimalism & Swiss | primario **rosso** `#DC2626`, accento `#1E40AF` | Rosso primario: **NO** (rosso = solo errore, e leggerebbe «bandiera» col verde del marchio). Il pattern «hero-centric» dice una cosa giusta: la barra deve **appartenere all'hero** — trasparente sul capitolo scuro, poi sfumata e compatta allo scroll (**EVOLVE**, coerente con 21st cat. 5). |
| Hero | **Scroll-Triggered Storytelling** | **Liquid Glass** (materiale dinamico, traslucenza) | `#1C1917` quasi nero, accento ambra `#A16207`, fondo `#FAFAF9` | Storytelling a scroll: **EVOLVE** — è §44 (progressione a capitoli, rivelazioni, sfondi che cambiano, nessun hijacking). Liquid Glass: **EVOLVE con limiti** — vetro solo su barra appiccicosa, overlay, pannello dell'hero, controlli flottanti (§38), mai sulle card. Ambra come accento caldo: **da valutare dal Creative Director** come secondo accento per CTA e momenti «attivi», accanto al teal (contrasto da calcolare: `#A16207` su carta ≈ 4,6:1). |
| Bottoni | Hero + Features + CTA | **Glassmorphism** | blu `#2563EB`, arancio `#EA580C` | Vetro sui bottoni: **NO** (§38); ma la lezione «stratificazione + luce» **EVOLVE** come luce verticale già in V3 più ombra di livello 1 e raggio `md`. Blu shadcn `#2563EB`: **NO** — è il blu «AI generico» (§75). Arancio come CTA secondaria calda: **da valutare** insieme all'ambra dell'hero (uno solo dei due). |
| Login | Scroll-Triggered Storytelling | Liquid Glass | come hero | Sul login lo storytelling a scroll è **NO** (una schermata, nessuno scroll); il vetro sul pannello di marca **EVOLVE** (§38 ammette «selected hero panel»): il modulo su superficie di livello 2, il pannello sinistro con la porta e un leggero velo. |
| Dashboard | Scroll-Triggered Storytelling | Liquid Glass | come hero | **NO** su entrambi: il cruscotto è MICRO/INTERACTIVE (§67), niente spettacolo di scroll né vetro sulle card. Resta valida l'idea di **capitoli**: testata scura di contesto (navy evoluto) sopra il workspace chiaro — profondità senza vetro. |
| Case workspace | Trust & Authority | Accessible & Ethical | navy `#1E3A8A`, oro `#B45309` | «Trust & Authority» come **struttura** (credibilità, prova, percorso chiaro): **EVOLVE** — il fascicolo mostra fatti, responsabili e fonti reali (§48), mai prove sociali inventate. Stile accessibile: **KEEP** (già AA). Oro: **NO** come decorazione (l'oro è la chiave del marchio; il bronzo resta ai sigilli); navy: **EVOLVE** come sopra. |
| Wizard | Hero-Centric | **Claymorphism** (soft 3D, chunky, **playful, toy-like**) | terracotta `#9A3412`, verde `#059669` | Claymorphism: **NO** — «toy-like» è l'opposto di §31 «never childish» e di un percorso di mobilità regolare. Verde: **NO** (approvazione). Ciò che vale: le **option card** grandi con stato di selezione netto (§50), in superfici arrotondate `lg`, senza spessori di plastilina. |
| Company | Trust & Authority | Accessible & Ethical | `#0F172A`, accento `#0369A1` | Struttura di fiducia: **EVOLVE** (stato del progetto, responsabile, timeline reali); `#0F172A` è lo slate di shadcn: **NO** come identità, ma conferma che il B2B regge un capitolo scuro di contesto. |
| Academy | Feature-Rich Showcase | Claymorphism | indaco `#4F46E5`, arancio | «Showcase ricco» **EVOLVE**: copertine con art direction, progresso, moduli (§53). Claymorphism e indaco shadcn: **NO** (giocoso; blu AI generico). |
| Forum | Scroll-Triggered Storytelling | Liquid Glass | come hero | Forum pubblico **EVOLVE** come l'hero (immersivo, §54); forum autenticato = workspace, MICRO/INTERACTIVE. |

**Che cosa lo skill ha fissato, in positivo, con questa seconda passata:**
1. lo storytelling a scroll come lingua dei capitoli pubblici (home, forum): progressione,
   rivelazioni, sfondi che transitano — con il budget «due elementi animati per vista»;
2. il vetro **controllato** sulla barra appiccicosa, sugli overlay e sul pannello dell'hero/login;
3. la struttura «gateway»: testata di workspace con contesto + azione primaria, poi la collezione;
4. il navy come colore di sistema dei capitoli scuri, evoluto dal marchio e non da shadcn;
5. l'idea di un **secondo accento caldo** (ambra o arancio, uno solo) per CTA e stati attivi — da
   decidere dal Creative Director con i contrasti;
6. la conferma che tre volte su undici il motore propone «Claymorphism» o palette shadcn: il
   giudizio senior resta necessario, e la §10 della direttiva ha ragione a chiederlo.

**Che cosa resta NO, con la ragione:** verde come CTA (legale); rosso come primario (errore/
bandiera); blu `#2563EB`/indaco `#4F46E5`/slate `#0F172A` come identità (AI generico, §75);
claymorphism (infantile, §31); vetro sulle card (§38); storytelling a scroll sui cruscotti (§67).
