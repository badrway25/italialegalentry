# Design V5 «La soglia» — index

**Status: PROPOSED (27 September 2026).** Nothing here is in force. The product owner signs pictures
before decisions: a gate 0 «La prova» (composed screens) comes before any of the decisions in
`CREATIVE_DIRECTION_V5.md` §24, except the four rulings the pictures need (O54, O55, O14, O57).

Origin: the owner's directives of 26 September 2026 — «Premium Visual Escalation V5» and «21st.dev
component-first design directive» — after gate A (V4) reached the performance budget (commit
`ac92427`). The backend, security, permissions, rule engine, case file, i18n and the QA already
validated are kept; the visual quality is what V5 replaces.

## What is here

| File | What it is |
|---|---|
| `CREATIVE_DIRECTION_V5.md` | The direction: concept, decisions per area with their reason, rejections, the four gate-A deviations, the arbitration of council conflicts, the owner's decisions (§24), limitations (§25), the revision after the red team (§26) |
| `DESIGN_SYSTEM_V5.md` | Tokens (primitive → semantic → component), type scale, spacing, radii, materials, motion tokens, component specifications and states, the component registry |
| `IMPLEMENTATION_PLAN.md` | Phase −1 (signatures), phase 0 «La prova», track T, the gate protocol, phase F (foundation), phase S (the eleven flagship surfaces in the owner's order), phase P (propagation), risks, effort |
| `21ST_COMPONENT_MATRIX.md` | Every component type reviewed against the 21st.dev catalogue: candidates, selection, adaptation route (A adapt / B Motion JS / C React island / D reject) |
| `21ST_SEARCH_LOG.md` | Every 21st.dev query, result counts, shortlists, selections and rejections |
| `ASSET_USAGE_MATRIX.md` | Every image and video: file, source, section, purpose, licence, reuse allowed |
| `ICON_SEMANTIC_MAP.md` | One concept, one icon: the semantic map and the rules |
| `RED_TEAM.md` | The independent challenge of the direction (4 blocking, 19 major, 18 minor issues) |
| `council/` | The fifteen specialist reports the direction was built from (inventory, captures and reference study, five 21st.dev families, typography, colour, icons, imagery, motion, mobile UX, public and platform UX) |
| `GATE_REPORTS/` | One report per gate as it closes. `GATE_0_LA_PROVA_2026-09-28.md`: the composed screens' three rounds, the verdicts verbatim, what stays open (first-render task, drawer INP, O67), the owner's next actions |

The council's working files — specimens, font builds with their OFL licences, the draft icon sprite,
the loader prototype, 317 captures of the current screens and of the two reference sites, Pexels
previews — live outside the repository in `C:\tmp\ile_v5_council\` (the screenshots and previews are
not licensed for publication and are not versioned).

## Tools used, and their limits

- **21st.dev**: paid tier, unlimited search and code retrieval. AI generation is enabled on the account
  but was not used, by the owner's earlier instruction (credits).
- **UI-UX-Pro-Max 2.13.0**: its search engine (typography, Google Fonts, colour, icons, motion, UX,
  landing, design-system) was run by the typography, colour, icon, motion and UX lanes.
- **Pexels**: API searches and previews only; nothing is curated or downloaded at full resolution
  until the owner rules on O54 (the scope of the editorial ban F15) and O55 (identifiable people).
- **Chrome**: the visible QA Chrome for the captures; headless profiles for every other probe.

## Process notes

The council's read-only phase was breached three times, all locally and all disclosed
(`CREATIVE_DIRECTION_V5.md` §25): a temporary `.playwright-mcp/` folder (gone), a QA session cookie,
seven session rows in the local `ile_qa` database. No tracked file was changed by the council.
