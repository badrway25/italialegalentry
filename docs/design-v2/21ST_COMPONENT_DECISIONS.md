# DECISIONI SUI COMPONENTI 21ST.DEV — design V2

Stato: **APERTO** · Accesso: chiave di sviluppo del committente, livello «paid» (ricerca e
recupero del codice illimitati; la generazione AI consuma i crediti del committente e si usa solo
quando il catalogo non ha nulla di abbastanza vicino). La chiave vive nella configurazione utente
di Claude Code, fuori dal repository, e viene ruotata a fine lavoro.

---

## 0. La regola

Mai «cerca → primo risultato → installa». Per ogni superficie importante:

```
SEARCH (≥ 5 candidati) → PREVIEW → REVIEW → ADAPT TO ILE → A11Y CHECK → PERF CHECK → IMPLEMENT
```

Un componente 21st non deve essere installato letteralmente: la sua struttura o la sua
interazione possono essere tradotte in un'implementazione nativa Django + CSS + Motion. Quando il
codice viene importato davvero, entra qui con licenza e dipendenze; quando serve solo da
ispirazione, entra qui lo stesso, con quella parola.

Vincoli che ogni candidato deve superare prima di essere considerato:

- **CSP** `script-src 'self'; style-src 'self'`: niente `<style>` inline, niente `style=`
  generati a runtime, niente CDN. Un componente Tailwind/shadcn va **rivestito** con i token ILE:
  primitive sì, estetica shadcn predefinita no (§ 71 della direttiva).
- **Dipendenze**: un componente che chiede pacchetti sproporzionati a un beneficio visivo
  piccolo si adatta a mano (§ 70). Ogni pacchetto accettato compare in
  `FRONTEND_DEPENDENCIES.md`.
- **Accessibilità**: WCAG 2.2 AA, equivalente tastiera/touch di ogni hover, reduced-motion,
  contrasto sotto il vetro, alternativa testuale ai grafici.
- **Server-rendered**: il contenuto pubblico resta nell'HTML di Django; il componente lo
  arricchisce, non lo sostituisce.

## 1. Tabella delle decisioni

| Superficie | Candidati esaminati (≥ 5) | Scelto | Fonte | Perché | Modifiche per ILE | Licenza / dipendenze | Codice importato o solo ispirazione |
|---|---|---|---|---|---|---|---|
| Navigazione pubblica | *(in corso)* | — | — | — | — | — | — |
| Hero | *(in corso)* | — | — | — | — | — | — |
| Visualizzazione del processo | *(in corso)* | — | — | — | — | — | — |
| Barra di giurisdizione / responsabilità 2.0 | *(in corso)* | — | — | — | — | — | — |
| Shell della piattaforma | *(in corso)* | — | — | — | — | — | — |
| Tabelle | *(in corso)* | — | — | — | — | — | — |
| Caricamento documenti | *(in corso)* | — | — | — | — | — | — |
| Stati vuoti | *(in corso)* | — | — | — | — | — | — |
| Pagine di autenticazione | *(in corso)* | — | — | — | — | — | — |
| Piè di pagina | *(in corso)* | — | — | — | — | — | — |

## 2. Candidati già localizzati (prima ricerca, 23 settembre 2026)

Metadati dal catalogo via MCP ufficiale (`search`); nessun codice ancora recuperato.

| Query | Risultato | URL |
|---|---|---|
| hero istituzionale, rete animata, scuro | Hero Section Dark (@kinfe123) | https://21st.dev/@kinfe123/components/hero-section-dark |
| | Shader Hero (@beratberkayg) | https://21st.dev/@beratberkayg/components/shader-hero |
| | Hero Section (@reuno-ui) | https://21st.dev/@reuno-ui/components/hero-section |
| navbar premium, mega-menu, blur, trasformazione allo scroll | Morphing Scroll Navbar (@laziekiki) | https://21st.dev/@laziekiki/components/morphing-scroll-navbar |
| | Scroll Navigation Menu (@spaceboydavey) | https://21st.dev/@spaceboydavey/components/scroll-navigation-menu |
| | Navbar Section 2 — mega-menu animato (@solaceui) | https://21st.dev/@solaceui/components/navbar-section-2 |
| timeline di processo, passi, attore responsabile | Activity Timeline (@7ovr) | https://21st.dev/@7ovr/components/timeline-3 |
| | Processing Timeline (@rmahammad) | https://21st.dev/@rmahammad/components/processing-timeline |
| | Process Timeline (@shadcnui-blocks/timeline-05) | https://21st.dev/@shadcnui-blocks/components/timeline-05 |

Il catalogo pubblico (21st.dev/community/components) è consultabile in Chrome senza accesso:
Heroes 1152, Navigation Menus 477, Backgrounds 365, Steppers 124, Scroll Areas 293, Shaders,
Gradients — usato come strumento di anteprima visiva prima di qualunque recupero di codice.

## 3. Generazione AI

Non usata. Se e quando lo sarà: prompt, `projectId`, take scelto, e perché il catalogo non
bastava, qui sotto.

## 4. Cronologia

| Data | Cambiamento |
|---|---|
| 2026-09-23 | Registro creato; regola fissata; MCP ufficiale collegato; prime nove voci del catalogo localizzate. |
