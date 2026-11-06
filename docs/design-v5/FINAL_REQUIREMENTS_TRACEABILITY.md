# Final requirements traceability — V5.12

**Date:** 28 Oct 2026. **Candidate:** 0a9373e (design-v5): technically validated, **rejected as a product** by the owner.
`main` stays on its current release until the owner approves the final product.

**Sources, in order of authority.** The list numbers sources S1–S18. Where a number is missing (S2, S6, S18), that source supplies no row in this table.
- S1: the project's Implementation Document (FR, 14 Sept 2026). This is the prescribed public wording, from the legal lead.
- S2: Allegato 1, the official Italian legal texts. **Not received.**
- S3: the FR courtesy translation of the legal texts.
- S4: the owner's Master brief (17 Sept).
- S5: the owner's Design + Product + Platform rebase (20 Sept).
- S7–S9: the owner's asset addendum, the V3 corrective and the V4 directive (23–24 Sept).
- S10–S14: the owner's V5.0–V5.10 directives.
- S15: the owner's V5.12 directive, which is binding.
- S16–S17: the reserved product documents. They are used for terminology only and are never public copy.

Quotes are short paraphrases. Lanes: **A** motion, loader and 21st.dev · **B** icons, forms and components · **C** imagery,
composition and incomplete public surfaces · **D** terminology, content completeness and platform UX · **O** owner or legal-lead action.

Severity:
- **CRIT**: an owner-visible defect named in V5.12, or a missing original requirement.
- **MAJ**: a visible defect that weakens product or institutional quality.
- **MIN**: polish.
- **—**: no gap found.

Every FINAL EVIDENCE cell says how the evidence will be produced. The reviewer fills it.

## 1. Identity and legal guardrails

| ID | Requirement (source, short quote) | Current implementation | Gap (sev.) | Remediation (lane) | Final evidence |
|---|---|---|---|---|---|
| R01 | One Django ecosystem; React islands only where materially better (S4 §18; S15 §5) | Django templates, small ES modules, no SPA | — | Keep it. No library returns (A) | pending — bundle inventory in the review |
| R02 | ILE is not a Ministry or authority; no state-like claims (S4 §0; S15 §16) | The public footer carries the promoter line | The console has no promoter line and no «not an authority» sentence (MAJ) | Console foot: the promoter line and the locked «ne délivre pas de visas…» sentence (D) | pending — console screenshot, fr/ar |
| R03 | Orient, never decide; nothing is promised (S1 §3.3) | Locked texts are present | — | Keep them | pending — locked-content test green |
| R04 | No public recruitment or matching wording (S1 §1.1–1.2) | Forbidden-string tests exist | — | Keep them | pending — test green |
| R05 | ™ / «marque déposée»; never ® (S1 §1.3) | Footer is correct | — | — | pending — footer check |
| R06 | Every form goes to the AGAMI contact address only (S1 §1.1) | Correct | — | — | pending — form inventory |
| R07 | Five legal pages, Italian only, official text (S1 §1.4; S3) | «Page en cours de préparation» | Official text missing; the pages read as work in progress (CRIT, blocker) | Obtain Allegato 1 IT, or written confirmation of the FR courtesy copy. Gate G1 keeps the forms closed (O, then D) | pending — legal pages render the official text |
| R08 | Prescribed texts are verbatim and locked (S1; S4 §77) | Checksummed locked content | — | Locked text is never reworded; only hidden by state (C9) | pending — lock checksum test |
| R09 | Phase gating 1→2→3 (S1 p.1) | Phase 3 is live | — | — | — |
| R10 | Footer version updated each phase (S1 p.1) | «v2.0.0 — Fase 1» shown under Phase 3 content | Wrong phase, developer string, Italian on every language (MAJ) | Compose the footer label from the active phase gate, localised; no default literal (D) | pending — footer, 4 languages |
| R33 | EU hosting confirmed in writing (S1 §1.4) | Owner's deployment | Owner action | (O) | pending — owner |
| R70 | Confidential material never public (S5 §4) | Guard tests exist | — | Keep them | pending — guard green |
| R73 | Never touch production, DNS or the legacy site (S4 §2; S14) | Respected | — | — | — |
| R79 | SEO: hreflang, canonical, no governmental JSON-LD (S4 §64) | Present | Hidden routes must leave the sitemap (MIN) | Sitemap honours the hide gates (C) | pending — sitemap fetch |

## 2. Public content and pages

| ID | Requirement | Current | Gap (sev.) | Remediation (lane) | Final evidence |
|---|---|---|---|---|---|
| R11 | Company «Recueil des besoins» form: exact fields, order and button (S1 §1.1) | Present; 14 fields in one column | Reads as a raw form (CRIT, see R58) | 3 steps (Entreprise / Besoin / Contact & consent), «what happens next» aside; field order and locked button text kept (B) | pending — 1440/390 fr/ar screenshots |
| R12 | Forum page: S1 sections, functions not names, logo slots (S1 §2.1) | Present | 8 equal text chapters (MAJ) | Three movements: dateline hero, editorial spread, dark «Participer» band (C) | pending — screenshots |
| R13 | After 2 Oct the page becomes the Permanent Forum with media and outcomes (S1 §2.1 note) | Permanent title, but the pre-event future-tense blocks remain; no media | Visible pre-event copy after the event (CRIT) | In permanent mode, hide the locked PROGRAMME and INTERVIENNENT blocks; gallery, documents and dates render only from back-office records (C). Content from the legal lead (O) | pending — /fr/forum/ fetch: no «en cours de définition» |
| R14 | Homepage Forum banner until 2 Oct only (S1 §2.2) | — | — | Verify the date gate (C) | pending — home fetch |
| R15 | Phase 3 hero title and subtitle; images of enterprises, training, universities and cooperation (S1 §3.1) | Present, with the door (C1 resolved by the owner) | The hero shows both the lock-up and the title (C2) | Owner decision on C2 (O); keep the current hero until then | pending — owner answer |
| R16 | Exactly four entrances, verbatim (S1 §3.2) | Present | The audience glyph does not reach the entrances (MIN) | Audience icons on the entrances (B) | pending — home screenshot |
| R17 | Espace Personnes intro, 8 pathways, «Comment ça marche» (S1 §3.3) | Present; no image | Generic composition (MAJ) | Photo hero + two-column numbered index with a family filter + linea (C) | pending — screenshots |
| R18 | Pathway pages: overview → CTA; no invented criteria (S4 §33) | 3 placeholders «en cours de vérification» on each of the 8 pages | Visible work in progress (CRIT) | Render a chapter only if verified content exists; drop the review-meta row when there is no date; two-column sheet with a steps linea and an authorities diagram (C) | pending — 8 × 4 fetch: 0 WIP strings |
| R19 | Progressive orientation wizard; the result is always an informational pre-assessment (S4 §34–35; S9 §49) | Best public form: choice cards, progress, disclosure | Two choice-card systems; no motion on selection (MAJ) | Unified choice cards + selection motion (B); orientation band image (C) | pending — wizard clip 390 |
| R20 | Espace Institutions page + form + button (S1 §3.4) | Present, title + prose | Generic (CRIT, R60) | Split hero with photo + an editorial index of the recipients (C) | pending — screenshots |
| R21 | Espace Universités et Formation + button (S1 §3.5) | Present, generic | (CRIT, R60) | 7/5 hero + chip ribbon of the approved terms (C) | pending |
| R22 | Pilot page with the 8 steps; never presented as authorised (S1 §3.6) | Linea present; the «projet en construction» notice is legally required | Notice styled as a WIP banner (MAJ) | Formal status plate, text kept verbatim; diptych anchor (C) | pending — screenshot |
| R23 | Lighter homepage: fewer boxes, short texts (S1 §3.7) | 8 imageless sections below the hero | Too empty (CRIT, R54) | Pilot diptych + ecosystem photo; no new boxes (C) | pending |
| R24 | «Attention aux fraudes», verbatim, visible but not alarmist (S1 §3.8.1) | Present; the footer link stays FR on it/en/ar | Link label not localised (MIN) | The footer link uses the glossary label; the locked heading stays on the section (D) | pending |
| R25 | FAQ verbatim, categories, search, anchors (S1 §3.8.2) | Present; latent «prochainement» empty state | WIP sentence (MIN) | Grouped disclosure + side index; the empty state becomes a 404 (C) | pending |
| R26 | Glossary, alphabetical, searchable (S1 §3.8.3) | Present, generic | (MAJ, R60) | A–Z lexicon rail + definition plates (C) | pending |
| R27 | Vivre en Italie: approved intro + fiches from the back office, incl. health/SSN (S1 §3.8.4; S15 §14) | 10 themes, all «Fiches en préparation» | Health and every other theme visibly unfinished (CRIT) | **HIDE**: the index shows the approved intro only; a theme route is 404 and out of the sitemap until it has a reviewed sheet; health/SSN hidden. No content invented (C) | pending — 4-language fetch: 0 «en préparation» |
| R28 | Training before and after arrival; certificates carry no administrative value (S1 §3.8.5) | Present; «seront détaillées» sentence | WIP sentence (MAJ) | Drop the sentence; two-time diptych layout (C) | pending |
| R29 | News + newsletter with separate, never pre-ticked consent (S1 §3.8.6) | News index is empty but linked | Empty page in the menu and footer (MAJ) | **HIDE**: nav, footer, route and sitemap only when at least one item is published (C, footer D) | pending |
| R30 | Forum Virtuel: reserved, flagged, launched after the Morocco Forum (S1 §3.8.7) | Flag closed | Launch window opens after 30 Oct (owner) | Flag stays closed until the owner opens it (O) | pending — owner |
| R31 | Foreign diplomas page; never «reconnaît» (S1 §3.9) | Present; WIP review meta | (MAJ) | Remove the WIP meta; vertical linea + «Qui décide ?» aside (C) | pending |
| R32 | Reserved area: access text + CONNEXION; each category sees only its own data (S1 §3.10) | Present | Institutions and universities get the individual's console (CRIT, R42) | See R42 (D) | pending |
| — | Partners page (S1 ecosystem; publication only with written authorisation) | Empty, linked from 5 pages | Empty destination (MAJ) | **HIDE** every link and the route while no partner is authorised (C) | pending |

## 3. Platform and roles

| ID | Requirement | Current | Gap (sev.) | Remediation (lane) | Final evidence |
|---|---|---|---|---|---|
| R34 | Roles deny by default; each sees only authorised data (S16; S5 §42) | Present | — | Keep it | pending — authz tests green |
| R35 | The person sees: where am I, objective, missing, next, who is responsible (S5 §22) | NowPanel present | «Responsable : La personne», «Brouillon», «non analysé» are shown to the person (MAJ) | Show «Vous» to the person, the person-facing step instead of DRAFT, and the scan state only when a file is blocked (D) | pending — dashboard screenshot |
| R36 | Case file as a professional case workspace (S5 §26) | Static | No motion or timeline feeling (MAJ) | Timeline draw + status change motion (A) | pending |
| R37 | Document status set; private storage (S5 §28) | Present | Dead links to missing preview files; sizes shown in octets (MAJ) | Draw a document without a link when its file is absent; re-attach the preview files (D); file size formatted + download action (B) | pending — 0 links answering 404 |
| R38 | Company area focused on needs, never on candidates (S5 §29) | Present; «wrench» icon; inherits the person rail entries | Wrong icon, wrong rail entries (MAJ) | `briefcase-business` icon (B); company rail without the person entries (D) | pending |
| R39 | The authorised actor sees only assigned work, with the mandate visible (S5 §30) | Present | — | Keep it; the operator icon is `user-cog` (B) | pending — authz test |
| R40 | Academy independent of selection; certificates are never approvals (S5 §32) | Synthetic «(exemple)» catalogue seeded on every deploy | Dummy content in the release (CRIT) | Demonstration gate on the seed; unpublish the example rows; the Academy entry is hidden while no approved course is published (D) | pending — production-settings seed dry run |
| R41 | Help desk escalates to a human; no fake AI (S5 §35) | Present | — | — | — |
| R42 | Institution, university, training-body and professional workspaces, scoped (S5 §36–38) | Same rail as a person; «Ma situation» asks an institution for a birth date | Wrong audience (CRIT) | Organisation rail (Espace réservé, Mes demandes, Communications, Mon organisation, Profil); person routes redirect; bridge page with the approved CTA. The full convention workspace stays a declared gap (D, O) | pending — qa-institution / qa-university walkthrough |
| R43 | The Permanent Forum as a governance module (S5 §39) | Present behind flags | — | — | — |
| R44 | No fake data, KPIs or AI; intentional empty states (S5 §55) | Bare «… apparaîtront ici» walls | Unfinished admin look (MAJ) | Collapse empty modules into one sentence + one approved CTA; the empty-state component gets a glyph (D, B) | pending |
| R45 | The platform matches the public site's quality; no admin UI (S5 §54; S15 §17) | The account, security and 2FA pages fall into the public shell | Two products (CRIT) | Account area in the console shell; «Sécurité du compte» overview (B) | pending — /compte/* screenshots |
| R46 | Key tasks work on mobile (S5 §47) | Present | Covered by R74 | — | pending |

## 4. Design system: loader, motion, 21st.dev, icons, forms, imagery, composition

| ID | Requirement | Current | Gap (sev.) | Remediation (lane) | Final evidence |
|---|---|---|---|---|---|
| R47 | Own institutional identity (S4 §12; S9) | V5 system | — | — | — |
| R48 | Palette: blue, green, warm white, bronze; never the flag (S4 §13) | V5 tokens | — | Tricolour only through the official mark (C6) | — |
| R49 | Self-hosted type; Arabic given equal care (S5 §13) | Present | — | — | pending — ar screenshots |
| R50 | Motion as a system; the homepage is not the only dynamic page (S4 §16; S15 §5) | Only the home, the entrance and the drawer move | Public pages and the platform are static (CRIT) | Motion system M1–M15 (scroll-driven CSS, tokens, reduced motion = still) (A; forms B) | pending — per-surface clips at 1440/390 |
| R51 | Branded loader: door + key + unlock + light; real waits only; reduced-motion variant (S10–S12; S15 §4) | Plays only on sign-in submit and a 24 px tile once per session; nothing under reduced motion | Not perceived (CRIT) | Cross-document View Transitions with the mark travelling; 400 ms navigation threshold (light line + key turn + status word); platform entry on a 40 px plate, once per space; async regions; lit still under reduced motion (A) | pending — throttled-network clip, reduced-motion screenshot |
| R52 | 21st.dev used for real, adapted, never a collage (S8–S11; S15 §6) | No per-family record | Under-used (CRIT) | Family-by-family selection in DECISIONS §3; a provenance table in docs (A, B, C) | pending — provenance table |
| R53 | One coherent icon system; Person ≠ Company ≠ Institution ≠ University (S9 §66; S15 §7) | `ile-steps` rendered 108 times as a universal section mark; concept maps not wired | Named defect (CRIT) | Semantic `CHAPTER` registry; `ile-steps` only for the journey; 12 Lucide (ISC) additions; sprite split; a test that forbids misuse (B) | pending — crawl: `ile-steps` only on journey surfaces |
| R54 | Licensed, optimised, non-repeated, non-cliché imagery; B/W → colour where meaningful (S4 §17; S15 §9) | 57 of 61 public pages carry no image; 3 frames repeated on the same page | Too empty (CRIT) | Slot registry + `photo` partial; about 17 Pexels frames per DECISIONS §6; 4 dedicated portico frames (C) | pending — page-by-page screenshots + licence register |
| R55 | Pexels video only on narrative surfaces, never on dashboards (S11 §41) | None | Decision: no video in V5.12 (no approved Forum footage; performance budget) | Revisit when the Forum's own footage is supplied (C, O) | pending — recorded decision |
| R56 | Official logo; doorway kept; one brand lock-up (S7; S8 §1; S13 §3) | Present | C2 is open | (O) | pending |
| R57 | Hero doorway: four routes, coloured steps, key turn, mobile first screen (S9 §31; V5.4) | Present | — | Keep it; the mark is the shared View Transition element (A) | pending |
| R58 | Premium forms with the full state model; never raw Django (S9 §28; S15 §8) | Good base; native selects and dates, single long columns, no warning or success state, 3 diverging partials | (CRIT) | One field partial; optional tag; warning and success states; inline validation; choice cards; combobox; segmented date; number stepper; multi-step for long forms; live password checklist (B) | pending — form-by-form screenshots, axe |
| R59 | Component set incl. toasts, skeletons, empty and error states (S9 §12–27) | Flash messages are static boxes | (MAJ) | Notice region with entrance motion; only success notices auto-dismiss (A) | pending |
| R60 | Intentional composition per page; not «title + paragraph + cards» (S5 §18; S15 §10) | About 45 inner pages share one chapter template | (CRIT) | One composition per page, per DECISIONS §7 (C) | pending — screenshots |
| R61 | Nothing technical, debug or fixture-like is visible (S9 §91) | Fixture names, red-team rows, version string | (CRIT) | See R72 and R76 (D) | pending |
| R62 | Calm institutional microcopy (S5 §56) | allauth default copy | (MAJ) | Override with glossary-governed strings (B templates, D catalogues) | pending |

## 5. Languages, accessibility, performance, process

| ID | Requirement | Current | Gap (sev.) | Remediation (lane) | Final evidence |
|---|---|---|---|---|---|
| R63 | Real RTL across navigation, forms, drawers and steppers (S4 §52; S15 §18) | Mirroring correct | New work must hold it | Logical properties only; the threshold line runs right to left (all) | pending — ar 390/1440 |
| R64 | No machine translation of locked or legal content; FR authoritative (S4 §53; S1 §3.11) | FR fallbacks on it/en/ar, marked `lang="fr"` | IT, EN and AR versions missing (MAJ, dependency) | Request them (O). Layouts never enlarge FR fallbacks in display type (C) | pending — owner |
| R65 | Readable, localised URLs (S4 §65) | English snake_case slugs on FR pages | (MIN) | Deferred until after owner acceptance: localised slugs with 301s. Recorded, not dropped (C) | pending — post-acceptance |
| R66 | WCAG 2.2 AA (S4 §61; S15 §8) | Present | New components must keep it | axe, keyboard and 400 % zoom on every new component (all) | pending — axe report |
| R67 | Performance budget; route-specific assets; shared bundles ratchet down (S4 §63; V5.8) | Within budget | New work must stay within budget | Budgets in DECISIONS §10 (all) | pending — size report + Lighthouse mobile |
| R68 | No trackers; self-hosted assets (S4 §54) | Present | — | Images downloaded and self-hosted (C) | pending |
| R69 | Security and privacy by design (S4 §47–60) | Present | — | — | pending — CI green |
| R71 | The team decides; the owner approves results; no A/B/C/D options (S14; S15 §24) | — | — | This document + DECISIONS | — |
| R72 | Preview labels the owner understands (S15 §12) | «Personas», «council-passed», keys and hashes | (CRIT) | Italian acceptance labels; keys and commits in small metadata (D) | pending — hub screenshot |
| R74 | Mobile-first; 390 px is not a simplified version (S4 §81) | — | New work must hold it | Every acceptance item checked at 390 (all) | pending |
| R75 | No WIP, «coming soon», dummy or dead CTA: complete or hide (S15 §13–15) | See R07, R13, R18, R27–R29, R31, R40 | (CRIT) | DECISIONS §8 ledger (C, D) | pending — 4-language WIP string scan = 0 (except R07) |
| R76 | Approved terminology per language, never invented (S15 §11) | «Personne / Persona» used as an identity word; two names for the documents section; Italian strings in the FR catalogue | (CRIT) | Terminology table in DECISIONS §9. EN/AR labels are provisional until the owner confirms them (C13) (D, O) | pending — catalogue test + console fetch |
| R77 | Never invent legal content (S4 §91) | — | — | Hide instead of filling (C, D) | pending |
| R78 | Content governance and versioning (S4 §44) | Present | — | — | — |
| R80 | Tests green ≠ finished; screenshot review (S15 §0, §21–22) | — | — | One final reviewer; headed walkthrough of the S15 §21 list (review) | pending — walkthrough report |

**Open owner items (not team-solvable):** R07 legal texts · R13/R29 Forum post-event content and photographs · R15 C2 ·
R30 Forum Virtuel launch · R42 scope of the organisation workspaces · R64/R76 IT, EN and AR texts and labels · R33 hosting.
