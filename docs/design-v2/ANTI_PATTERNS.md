# ANTI-PATTERN — cosa fa leggere un sito come generato, noioso o finto-premium

Ogni voce ha un segnale osservabile e, dove possibile, un caso reale visto il 23 settembre 2026.
Le fonti secondarie sono avoid-ai-design (GitHub), LogRocket ("Linear design"), select-interactive
(trend 2026 vs budget), utsubo (fintech), Emil Kowalski e Rauno Freiberg (motion).

## 1. "Generato / shadcn di serie / template" — come si riconosce

| Segnale | Come si vede | Caso |
|---|---|---|
| Gradiente viola→blu su bianco, titolo con `bg-clip-text` | hero con testo sfumato | avoid-ai-design; 21st.dev "Glow Horizon", "Aether Flow" |
| Palette zinc/slate non toccata | `theme-color #09090b`, grigi freddi neutri | 21st.dev stesso (#09090b) |
| Inter/Roboto/Poppins come voce unica | un solo `@font-face`, nessun display | Trenitalia (Poppins + Bootstrap), gov.sg (Inter), Sciences Po |
| Bootstrap 5 di serie | `--bs-blue:#0d6efd`, raggi .375 rem | u.ae (piattaforma governativa su Sitecore + Bootstrap), Polimi, EUI, Maroc.ma |
| Hero centrato + tre card di feature + CTA | simmetria totale, "zero asymmetry" | avoid-ai-design |
| `rounded-2xl shadow-lg` su tutto, icona in quadrato arrotondato | ogni card uguale | avoid-ai-design |
| Vetro per riflesso | `backdrop-filter` su card statiche | catalogo 21st.dev |
| Sfondi shader / particelle / vortici / lampade | "Animated Shader Hero", "Neural Vortex", "GLSL Hills", "Lamp" | 21st.dev |
| Stesso `fade-in-up` su ogni elemento, o nessun moto | reveal identici in cascata | avoid-ai-design |
| Icone lucide `Sparkles`/`Zap`/`ArrowRight`, emoji come bullet | "AI" = stellina | avoid-ai-design |
| Spaziatura uniforme `gap-4 / p-6` | nessuna gerarchia spaziale | avoid-ai-design |
| Avatar DiceBear, loghi finti, placeholder sfumati | social proof inventata | avoid-ai-design |
| Muro di loghi → card → carosello → metriche → badge SOC2 | ordine sezioni SaaS | Harvey, Legora (nonostante l'ottima tipografia) |
| Neobrutalismo come "anti-AI" | bordi neri 1 px, raggio 0, mono | Fireart/Bubble 2026: è una reazione, non una direzione istituzionale |

## 2. Perché i siti governativi sembrano noiosi (anche quando sono corretti)

- **Il design system preso come soffitto anziché come pavimento**: GOV.UK (GDS Transport, raggio 0,
  nessun moto), ECL (solo Arial, solo peso 400), Bootstrap Italia/Titillium. Sono ottimi standard
  minimi di leggibilità per una PA; usati come estetica finale producono il registro respinto.
- **Homepage-notiziario**: ECB ("In focus" + comunicati in ordine cronologico), ETH (lista notizie),
  Banca d'Italia, Esteri (Splide ×28), Nobel (Splide ×14). La notizia non è il compito dell'utente.
- **Carosello come hero**: IOM (banner rotante), Trenitalia, Esteri, EUIPO (Swiper ×32).
- **Mega-menu senza gerarchia**: ECB nove voci di primo livello; Harvey otto sottovoci in "Platform".
- **Un solo colore istituzionale su bianco**: blu #0066cc / #0E47CB / #164194 + bianco + grigio,
  senza scala di superfici né accento interattivo distinto.
- **Fotografia di cronaca**: IND (Ter Apel), IOM (crisi). Per un servizio di ingresso regolare
  comunica emergenza, non percorso.
- **Icone di libreria** (FontAwesome: BoE, EIB, Maroc.ma, Migrationsverket) e raggi misti
  (IND 5/6/10 px).
- **Zero profondità e zero moto**: nessun `cubic-bezier` proprio, nessun `prefers-reduced-motion`
  (ETH, MIT, BoE non lo dichiarano nel CSS), nessuna transizione di stato.
- **Tono procedurale senza voce**: "Learn about what happens next and what you need to do"
  (Migrationsverket) è chiaro ma non memorabile; e-Residency dimostra che si può avere voce.
- **Bandiere e colori nazionali come identità** (ECL giallo UE, ECB euro giallo): per noi vale il
  divieto esplicito di tricolore e insegne.

## 3. Perché i tentativi "premium" sembrano cheap

| Eccesso | Perché fallisce | Caso |
|---|---|---|
| 3D/WebGL senza funzione | select-interactive 2026: "heavy 3D and experimental navigation" sono i primi tagliati dai budget; INP peggiora | Lusion (legittimo per un'agenzia 3D, non per noi); Jeton "3D per tangibilità" |
| Particelle, shader, mesh-gradient animati | leggono "catalogo 21st.dev"; costano GPU sul mobile | 21st.dev |
| 20 gradienti | il gradiente arcobaleno appartiene a Stripe (#533afd → #da56ed → #ec8fff); ripetuto altrove è imitazione | utsubo: "gradient creates movement" solo se è **uno** |
| Vetro ovunque | Apple usa Liquid Glass su controlli e barre, non sul contenuto; il vetro su testo fallisce 1.4.11 sul peggior sfondo | Raycast lo limita alla palette comandi (backdrop-filter ×12, tutti su elementi fluttuanti) |
| Curve con overshoot | il rimbalzo è ludico, non istituzionale | BoE `(0.52,1.64,0.37,0.66)` ×10, Raycast/Wise `(.34,1.56,.64,1)` |
| Durate da un secondo nel prodotto | percepite come lentezza; Emil: < 300 ms | UC Investments 1 s ×26 (accettabile solo in un rapporto narrativo) |
| Smooth scroll globale (Lenis) su pagine di compito | scroll non 1:1, tastiera e lettori di schermo penalizzati | darkroom/Legora lo usano su siti vetrina |
| Scroll-jacking, tende, iris fra pagine | WCAG 2.3.3, INP, disorientamento | motion.dev "Curtains" (idioma da vetrina) |
| Autoplay di animazioni pesanti | Jeton lo ha evitato deliberatamente | — |
| Lottie decorativo | 49 riferimenti su Ironclad, 27 su Juro e makemepulse: peso senza informazione | Ironclad, Juro |
| Pillole e raggi 24 px su tutto | `border-radius:1.6rem` ×54: perde la gerarchia fra input e azione | Juro (Mercury distingue 4 px input / 32 px azione) |
| Dark mode come sinonimo di premium | LogRocket: "almost every SaaS website looks the same"; la scala conta, non il buio | Linear-cloni |
| Oro/giallo saturo, gradienti metallici | leggono bandiera (UE #FFCC00) o lusso di plastica | — |
| Muro di numeri e loghi | "Trusted by 35.000+" senza fonte e data è rumore | Brex/Ramp (utsubo) |
| Tre o quattro famiglie latine insieme | GT Walsheim + Cera Pro + Kazimir + Inferi; Manrope + Nunito + Montserrat + Cairo | Juro, Maroc.ma |
| Framer/Webflow come stack | incompatibili con CSP `script-src 'self'` e con Django | Legora, Luminance, Juro, Ramp |

## 4. La direzione respinta (ART_DIRECTION_A "editoriale / registro") — diagnosi

Cosa ha fatto, letto contro i benchmark:

1. **Ha ottimizzato "istituzionale = trattenuto"** prendendo GOV.UK/ECL/Designers Italia come
   riferimento estetico: tipografia corretta, colore unico, nessuna profondità, nessun moto. È il
   pavimento delle PA, non il soffitto di una piattaforma privata internazionale (vedi § 2).
2. **Sei sezioni editoriali uguali**: nessuna gerarchia di superficie (livelli 0–1 soltanto), nessun
   "oggetto vivo", stesso ritmo per ogni blocco — l'effetto homepage-notiziario di ECB/ETH.
3. **Hero H1 + paragrafo + bottone statico**: NBIM mette un numero vivo, Eurostar lo strumento,
   IND quattro ingressi, Legora video + pannelli, Stripe un'onda con fallback. Il nostro hero non
   faceva nulla e non mostrava nulla.
4. **Superfici piatte**: nessuna scala canvas/area/stroke (Snøhetta, Linear), nessuna ombra per ruolo
   (Vercel, Fluent 2), nessuna hairline: tutto sullo stesso piano.
5. **Nessun componente firma**: le quattro vie, il processo NEED → INCLUSION e il rail di
   giurisdizione non esistevano come oggetti riconoscibili.
6. **Nessuna parità di piattaforma**: il portale restava "form Django" mentre il pubblico era
   "editoriale": due registri, nessuno premium.
7. **Moto assente per prudenza**: la prudenza giusta è `prefers-reduced-motion` + budget, non
   l'assenza (Stripe, Mercury, Wise dichiarano reduced-motion e animano comunque).

Conclusione: la direzione non era sbagliata per eccesso di rigore ma per **assenza di autorialità**
(nessuna decisione che solo noi potevamo prendere). La correzione non è "aggiungere effetti" ma
scegliere tre voci tipografiche, una scala di superfici, un accento, quattro componenti firma e un
sistema di moto dichiarato.

## 5. Test in sessanta secondi (tutte le risposte devono essere "no")

1. Il colore primario è un blu 0d6efd / 0066cc / 0E47CB o simile, unico, su bianco?
2. C'è un gradiente viola→blu, un testo sfumato o un glow?
3. C'è un carosello nell'hero o una lista di notizie sopra la piega?
4. Le card hanno tutte lo stesso raggio, la stessa ombra e la stessa icona in quadrato?
5. Esiste un `backdrop-filter` su un elemento che non è fluttuante?
6. Esiste una `cubic-bezier` con valore > 1 o una durata ≥ 600 ms fuori dai capitoli immersivi?
7. Lo scroll non è 1:1 con la rotellina su una pagina DENSE o LEGAL?
8. Manca `prefers-reduced-motion` nel CSS o nel JS?
9. Si vedono aerei, passaporti, valigie, varchi, bandiere, tricolore, insegne di Stato?
10. Il portale usa font, accento, raggio o ombre diversi dal sito pubblico?
11. Un numero in pagina non ha fonte e data?
12. Il markup contiene Framer, Webflow o Bootstrap di serie?
