# ADR-009 — Server-rendered + progressive enhancement, niente SPA

**Stato:** accettata

## Decisione
HTML reso da Django; CSS moderno con custom properties (design token), layout grid/flex con proprietà logiche; JavaScript in ES modules vanilla per navigazione, accordion, tabs, stepper, reveal (con `prefers-reduced-motion`). HTMX ammesso solo dove migliora concretamente l'UX (wizard di orientamento, ricerca FAQ/glossario) e servito localmente. Nessun React/Vue, nessun Tailwind runtime.

## Motivazione
Portale istituzionale: SEO, accessibilità, performance (LCP/INP), sicurezza (CSP self-only) e manutenibilità premiano il server rendering.
