# ADR-008 — Tipografia: superfamiglia IBM Plex (Serif / Sans / Sans Arabic), self-hosted

**Stato:** accettata

## Contesto
Serve una voce tipografica istituzionale ed europea, distinta da gov.it (Titillium) e dal sito attuale (Cormorant / Source Sans), con un compagno arabo progettato per armonizzarsi (RTL reale).

## Decisione
- Display / titoli: **IBM Plex Serif**
- Testo / UI: **IBM Plex Sans**
- Arabo: **IBM Plex Sans Arabic**

Licenza SIL OFL 1.1; file woff2 self-hosted in `static/fonts/` (subset latin / latin-ext / arabic), `font-display: swap`, nessuna richiesta a Google Fonts in runtime (vietata anche dallo scanner di conformità).

## Conseguenze
Coerenza cross-script, metriche compatibili, zero dipendenze esterne. Licenze registrate in `docs/IMAGE_LICENSES.md` (sezione font).
