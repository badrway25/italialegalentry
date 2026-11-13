# W2-C1 shipped — 9 October 2026

- Merge: design-v5 `a0d1982` (no-ff); bundles rebuilt in design-v5; steward files `a268785`; tag `v54/w2-c1`; v5-live at the tag; 8780 restarted and verified (/fr/, /ar/, /it/ 200 with the letterhead, the four door panels, «la targa», eight panel photographs served; 0 idle connections).
- Review once: REVIEW.md SHIP_AFTER_FIXES (4 major) + A11Y_PERF.md SHIP_AFTER_FIXES (2 major) — all six fixed in the fix pass (letterhead fit 1280–1510 px, WCAG 1.4.12 text spacing, the three short panels, the brand name at 360 px, the 64↔56 long task).
- Tests on the branch with design-v5 merged in: 53 browser passed (0 skipped) after a first run crashed on machine memory (Target crashed — re-run clean), 1 237 non-browser passed; after the merge and the rebuild on design-v5: 890 passed (bundle currency, design docs incl. the regenerated capture report, tokens, preview).
- Not done: W2-C2 (the phone/tablet sheet on the overlay system, the signed-in targa's account popover, the panel on overlay.js) waits for the overlay system; the explicit entry list in scripts/build_frontend.mjs (nav.js is its own request today); WebKit/Firefox not run.
