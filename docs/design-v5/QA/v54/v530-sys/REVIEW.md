# v530-sys — the Fast Visual Variety Correction (V5.30, 8 Nov 2026)

One audit, one implementation pass, one representative review, one fix round (the correction's §14), performed inline by the orchestrator. Scripts, JSON and stills outside the repository.

## What the audit found

Twenty public pages, measured and read at 1440 / 1024 / 390. The weakest surfaces: Entreprises (a skyline and a wavy measured curve on stalks), the home (a second arch and a bronze line right under the hero's arch, gold threads in the pilot), Institutions (an arc of discs over a photograph), Projet (an arch with rays under its arched hero), a compass drawing on three pages, circular icon containers everywhere, a teal dash above every section title, a miniature route in the pilot's tile.

## What changed

- **Shared primitives first.** Icon containers are tiles, not discs. Only a panel head keeps its rule. The route's origin seal has no arch of its own.
- **Home.** No line from the hero into the orientation; the orientation is a raised panel of four cells with its title beside it; the pilot opens on its photographs with no thread or seam.
- **Entreprises.** One process panel with no overlay (the measured curve and its script are gone); the head is words and a workplace photograph; the quotation, then the title, then the panel.
- **Institutions.** A split: the photograph at the reading edge, the recipients as a row of tiles on the night plate; no arc, no small hemicycle.
- **Universités and Formation.** The campus frame at its own 3:2, the stations as cards with no line joining them, the band's note under the frame; two raised cards at Formation.
- **Parcours pages.** The compass drawing and the authorities' arc are gone; the raccordi into the sheet's night and the diplomas' protection are gone. Only «Parcours» keeps its route's raccordo.
- **Vivre, Forum, Contact, Projet.** Their decorative lines and light drawings are gone. Projet's figure is one list of actors with their names.
- **Fraudes and Vivre titles.** A capital title at the page title's size.

## What stays on purpose

The hero's arch and Lume; Home's reserved door; Forum's hemicycle seal; Parcours' route head; Réseau's network; Projet's arched photograph as an identity surface; Fraudes' straight plate rule; the Italy and Morocco visuals. FAQ, Glossaire and AGAMI already read as product pages and were not recomposed.

## The review

Headed Chromium, 63 cells, §15's pages plus Universités, Projet, the sheet, Vivre, Fraudes, Contact and the pilot page; 1440 / 1024 / 390, fr, Arabic where the composition changed. Overflow 0, one h1, console 0, failed requests 0, flags never mirrored, axe serious/critical 0 after the fix round. Arches at 1440: the home 2, every other reviewed page 0. The stills were viewed.

The fix round: Projet's figure height (a real contrast finding), Entreprises' stacked statement, Contact's last line, Home's caption above the panel, hover equal to focus on the flow's cells, the Italy and Morocco drawings decorative for assistive technology, the campus frame's width.

## Honest limits

- 21st.dev: one targeted search per page family, pattern metadata only. No component code was retrieved or pasted; the patterns are adapted in this system's own CSS and HTML.
- `ui-ux-pro-max`: one short query. `figma-use-motion`: not used, it works only on a Figma file and there is none here; no motion was added.
- The audit and the review ran on more pages than §15 asks; nothing else went beyond §14's limits.

## Checks

See DL54-205; the final matrix and the fresh-clone gate follow on the merged tree.
