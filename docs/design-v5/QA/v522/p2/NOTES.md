# V5.22 lane P2 — Page Composition V2: system, trust and reading (label v522-p2-build)

Branch `v522-p2` from design-v5 `22b0ddd` (worktree `C:/tmp/ile_wt/v522-p2`). Scope: SECTION_SYSTEM_V2 §9.5 — §3.2
Le projet, §3.11 Réseau, §3.12 Contact, §3.13 FAQ, §3.14 Glossaire and the term page, §3.15 Vivre en Italie, §3.16
Forum, §3.17 AGAMI with the V5.23 Q9 identification block, §3.18 Attention aux fraudes. Built on lane S's library
(`docs/design-v5/QA/v522/s/NOTES.md`) and lane M's imagery (`docs/design-v5/QA/v522/m/NOTES.md`); no file another
lane owns was edited (§9.7) — the requests are in §9.

- Database lane l7 (`ile_v5_l7`, tests on `test_ile_v5_l7`, one pytest at a time).
- Lane server 8787: dev settings, `ILE_DESIGN_PREVIEW=1`, `ILE_REFERENCE_DATE=2026-10-03`, the WhatsApp number read
  privately by the launcher from the live environment (never written in a tracked file). Stopped at the end.
- Chromium slots, headed (`chromium-1234`) for the reviews, headless for the browser tests. Two holds ran past the
  25-minute bound: slot B 22:20–23:10 (probes until about 22:45, then held through the static suites by mistake) and
  slot B 23:10–23:44 (one pytest session of the browser suites ran 18 minutes). Slot A 23:47–23:54 for the last
  headed checks and 01:50–02:02 for the final browser run. Every hold was released.

## 1. What the owner sees, where

Lane server 8787 (on design-v5 once merged), every page in fr, it, en and ar. Evidence:
`C:/tmp/ile_v5_council/evidence/v522/p2/` (`<page>_<lang>_<width>_v<n>.png`, viewport by viewport, and `_full`).

- **Le projet** `/xx/le-projet/`
  - The head is kept (the arch, `project.hall`).
  - **C «il racconto»**: the three chapters are the steps of one story beside one figure. «En bref» (`p3.hero.body`,
    while gate G3 is open), «POURQUOI ITALY LEGAL ENTRY» (the locked text cut at render into its three sentences, the
    last set in place as the statement on a 2 px accent rule), «Qui porte le projet» (the FAQ's `faq_who` answer, or
    the promoter's line, and «En savoir plus sur le promoteur»). From 64 rem the figure is a sticky night plate: the
    threshold arch with its light, the improvised paths drawn dashed (Pourquoi), the route through the door, the
    foundations (Qui porte), the five actors' nodes — each layer draws as its step is read. Below 64 rem the figure
    stands once above the steps in its final drawing. Each step keeps its chapter's anchor (`#project-why-title`…).
  - **D «il panorama»**: `project.volumes` widens from the container to the full bleed.
  - **E «le porte»**: the four spaces as equal night doors (Personnes, Entreprises, Institutions, Universités), the
    actor's name and the way in; the actors' sentences stay on /reseau/.
  - The foot strip: three onward links and the trademark line, unchanged.
- **Réseau** `/xx/reseau/`
  - **H «la mappa» in the head**: the night ring looks as before; its five nodes are the map's controls. From desktop
    width they are tabs — the Arrows go round the ring in the reading direction (mirrored in Arabic), Home and End,
    Escape back to the hub; the light glides to the chosen node, its spoke and its two sides draw. The entry docks in
    the head's reading column: the hub's is «En bref» (only while G3 is open, exactly what the chapter said), each
    actor's its disc in its audience's ring, its name, its sentence and its space. The entries share one cell: no
    selection moves the page. On a phone (a ring under 300 px) the map is its list, every entry shown.
  - The register «Les acteurs de l'écosystème» left: the five actors are told once.
  - **K «l'approdo»** on stone: the Forum (its typographic night tile, Q4) and the promoter (its name as the line).
- **Contact** `/xx/contact/`
  - The head is kept; C1's sentence «Tous les formulaires du site sont acheminés vers cette adresse.» is the caption of
    the head's address, so the address is said once. The folio is typographic.
  - **E «il centralino»** on stone: one board titled by the channels the settings hold («Par téléphone, WhatsApp ou
    formulaire»; with no WhatsApp number «Par téléphone ou formulaire»), the Numéro vert and WhatsApp plates (the
    channel architecture unchanged: V5.19, option B), the form's plate (its link; with G2 closed the G2 notice in the
    same plate and the button secondary), the privacy link «Vos données» as the board's legal foot. The discs settle in
    turn; their fill answers the focus as the hover.
  - **E «le porte»**: «Une demande précise ?» on a drawn hub line, three night doors to the dedicated forms.
- **FAQ** `/xx/faq/`
  - The head is kept (the search seat: its plate's corner is now the plates' 6 px — §4.4, three corners a screen).
  - **L «l'indice», the explorer** for each category: from 64 rem the questions as a vertical tablist beside one sticky
    answer plate (the `ile-domande` seal in its corner); the address follows the question, so every permalink
    (`#faq_…`, the trust band's and the fraud page's) opens its answer; the fraud question is marked (`ile-scudo`, an ink
    rule). Below 64 rem each question's heading is its disclosure button, one open at a time. The answers' links are
    chips. Without script every answer is in the page, in order.
  - **«il rimando»**: the glossary, the fraud page, contact. A search's answers keep their open disclosures.
- **Glossaire** `/xx/glossaire/` and the term page `/xx/glossaire/<term>/`
  - The head is kept (its seat at 6 px, as the FAQ's).
  - From 64 rem **a thumb index at the reading edge**, sticky under the letterhead, its plate gliding to the letter in
    view (`aria-current`, announced on focus only); beside it **E «il lessico»**: large letters in the flow and term
    cards (two columns, three from 80 rem) — the Italian term, the prescribed definition whole, «Où le rencontrer»
    (the pathways that name the term, by their prescribed titles; a general term leads to the pathways). On a phone the
    letter band of before.
  - The term page: the compact frontispiece with the `ile-lessico` seal and the term as its h1, then **K «la scheda»**
    (the outlined initial, the definition plate with «Définition à caractère informatif.», the related terms and the
    pathways as chips, the way back).
- **Vivre en Italie** `/xx/vivre-en-italie/`
  - The band with the `ile-vivere` seal and the locked title; **D «il panorama»**: the street photograph (the LCP, never
    masked) scales once after the first paint, drifts, and one light crosses the façades as it leaves; the locked lead
    on an opaque paper plate over the frame's foot.
  - Q8: no theme card while no theme carries a reviewed sheet.
  - **«Pour s'installer»**: the training after the arrival (`/formation/#apres-l-arrivee`), «Permesso di soggiorno» and
    «Codice fiscale» (their prescribed definitions), the FAQ.
- **Forum** `/xx/forum/`
  - FO0: the head kept, the `ile-forum` T1 at display scale on the band's far side — the page's one seal — with the
    page index on a night plate over it.
  - FO1 **A, typographic**: «QUI SOMMES-NOUS» (the opening clause at the band size) | a hairline that draws | «POURQUOI
    …» (the last sentence set in place as the statement; one light passes across its column).
  - FO2a **I «dal dialogo ai progetti»**: «what» sticky beside the objectives as eight clause-stations (the locked
    sentence cut on its own « ; »), the arrival carrying the Forum's T2 mark.
  - FO2b **H on a night plate**: the nine actors of the locked sentence, its own spans, on a ring around the Forum (the
    mark's drawing), the four that name an ILE audience with their discs; a vertical constellation on a phone.
  - FO3 **K on stone**: two raised plates (the pilot interest, `building`; the collaboration, `institution`), the
    locked labels as their links, the help line at the foot, the mark's faint drawing behind.
- **AGAMI** `/xx/agami/` (V5.23, Q9 decision A)
  - The head is kept.
  - **A «la targa d'identità»**: a drawn colonnade plate (revealed from the reading edge, its line drawing) beside
    `p2.forum.who.body` whole, «depuis 2011» and «l'Italie et le Maroc» set in place; the FAQ's `faq_who` as a closed
    disclosure under it.
  - **K «la targa»** on night — «Identification et contact»: the association's name and legal form, its three
    registers (Code fiscal, RUNTS, the Region's registration decree — their designations in Italian), its two offices
    (siège social, siège opérationnel, each street and town in Italian, the country in the page's language), its
    official contact (the mailto) and its official website (as text: the one outbound link of the public pages is
    WhatsApp). Every field the owner gave on 30 October, once, from one source (`apps/pages/identity.py`, the values
    are there and nowhere else in this note); no other identifier; no link to the unpublished legal notice.
  - **K «l'approdo»** (the colonnade bookend): the Forum, Le projet, Le réseau.
- **Attention aux fraudes** `/xx/attention-aux-fraudes/`
  - The head with the locked notice kept (its folio the `ile-scudo` seal, lane S).
  - **A «segnalare · informarsi»**: the report plate (the sentence, then the address as its action, an ink rule that
    draws) beside three route tiles — the FAQ's locked question `faq_guaranteed_visa_offer` (`circle-help`), the
    regular pathways (`signpost`), the glossary (`book-a`). No authority, police, embassy or portal link.

## 2. Files

- **Views** (P2's): `apps/pages/views.py` (the story's steps, the doors, the map's entries, the contact doors, the
  fraud routes, the approdo tiles; every glyph from the icon registry), `apps/pages/identity.py` (new, the Q9 source),
  `apps/faq/views.py`, `apps/glossary/views.py`, `apps/living/views.py`, `apps/forum/templatetags/forum_v2.py` (new:
  the Forum's cuts, all text-preserving, or the text whole).
- **Templates**: `templates/pages/{project,network,contact,agami,antifraud}.html`, `pages/partials/projet/` (new),
  `pages/partials/agami/_colonnato.html` (new), `pages/partials/fronte/{_rete,_rete_pannelli,_contatto_azione}.html`,
  `templates/faq/{index,_risposta,_collegamenti}.html`, `templates/glossary/{index,_entry,term}.html`,
  `templates/living/index.html`, `templates/forum/partials/{hero,presentation,cta_row}.html`.
- **Sheets**: `pages/css/interior.css` (+ `_projet`, `_rete`, `_contatto`, `_agami`, `_frodi`; `_canali` focus parity;
  `_institutional` dead rules out), `cms/lettura.css` (+ `_lettura-v2.css`; `v5/_lettura.css` loses the glossary rules
  it no longer draws), `forum/forum.css` (+ `_sezioni`, `_sigillo`; `_forum.css`'s V5.12 pair, spread and band
  replaced). `main.css` untouched.

## 3. Budgets (gzip -9, the tests' method)

| Sheet / page | Measured | Ceiling |
|---|---|---|
| `main.css` | 32 718 | 32 718 (never above) |
| `pages/css/interior.css` | 10 431 | 11 264 |
| `cms/lettura.css` | 8 825 | 9 216 |
| `forum/forum.css` | 6 884 | 8 192 |
| interior page `/fr/contact/` (and le-projet, reseau, agami, fraudes: the same five sheets) | 55 832 | 56 320 |
| reading page `/fr/faq/` (and glossaire, the term page, vivre: the same five sheets) | 54 226 | 54 272 |
| forum page `/fr/forum/` | 46 144 | 54 272 |

The reading total is 46 B under its ceiling: a later rule on the reading pages needs a saving first. `_sec-mappa.css`
and `_sec-campata.css` are not imported: the network's ring is the frontispiece's own (v5/_fronte.css §8, its map
behaviour in `_rete.css`), and the AGAMI plate and the Forum pair compose with the shell's verbs alone.

## 4. Tests

**New**
- `apps/pages/tests/test_interior_v522.py` — 29 cases: the story's steps, anchors and figure (one register), the
  locked texts whole as one element, the panorama, doors and foot; the map's markup with and without G3, its register
  of five registry glyphs; the approdo (the Forum's tile bare, the others glyphed); the contact board, its anchors,
  its G2 plate and its one primary; AGAMI's identity plate and disclosure in four languages; the identification's one
  source; the fraud split and its three routes; the FAQ explorer and its permalinks; the glossary rail, cards and
  «Où le rencontrer»; the term page in four languages; Vivre's panorama (the LCP never masked), «Pour s'installer» and
  Q8; the family's imports; no page block shadowing a chrome class (the `.targa` collision, §5).
- `apps/forum/tests/test_forum_v522.py` — 6 cases: one seal a page; the pair's and the objectives' locked texts whole,
  the eight stations, the arrival mark; the nine actors one register with exactly the four registry glyphs; the two
  action plates with their locked labels.
- `tests/frontend/test_pages_browser_v522_p2.py` — 15 cases in Chromium: the Forum's ring round its hub, mirrored in
  Arabic (each actor's offset the French one's opposite); the map as a tablist (fr, ar: Arrows in the
  reading direction, Home, End, Escape, the stage's one height, a click), the phone's list; the explorer's permalink
  (the answer in the screen under the letterhead, the address in step, the stage's one height, the focus clear of the
  letterhead) and the phone's exclusive disclosures; the glossary rail (sticky, beside the cards, a letter landing
  under the letterhead and marked); the ten pages at eight widths in fr and ar (no overflow, one h1, the letterhead's
  height); reduced motion (no state, no running animation, the story not driven); no script (every entry in order).

**Updated under the strict rule** (V5.20: the old expectation conflicts with V5.22 / V5.23, the new behaviour is
intentional, the invariant is the same or stronger, the reason cited in the test):
- `apps/pages/tests/test_institutional.py` — the why/who bodies are one element whose text is the registry's (§3.2
  LP-2, §3.17 AG-1, instead of a contiguous escaped string); the Arabic `projet__perche` paragraph keeps `lang="fr"`;
  the AGAMI test now asserts the owner's verified identification, every field once, no other identifier, no outbound
  link, no notices link (V5.23 Q9, replacing «publishes no registry data»).
- `apps/pages/tests/test_contact_channels_v519.py` — the board's heading names the channels the settings hold, in the
  board's words (§3.12 C1+C2+C3): «Par téléphone, WhatsApp ou formulaire» / «Par téléphone ou formulaire».
- `apps/faq/tests/test_views.py` — the explorer's nine panels (h3 + date, ids = keys = permalinks, index hrefs) and
  their languages (§3.13 Q1).
- `apps/glossary/tests/test_views.py` — the term cards (h3 in Italian, ids, definitions with their languages) (§3.14
  G2).
- `apps/forum/tests/test_forum_page.py` — the four bodies re-composed at render, each one element, text whole; the
  eight clauses (§3.16).
- `tests/frontend/test_content_pages_browser_w3_f2.py` — the V2 plates and tiles admitted by name with their 1 px edge
  only (§2 K, §4.3); the letter index from 64 rem a rail beside the cards (a letter lands under the letterhead, beside
  the rail), the band of before at 768 still landing under the band (§3.14 G1); the FAQ's keyboard promise in both
  forms, tabs and disclosure buttons (§3.13 Q1); the explorer's French questions measured on the reading edge — the
  plate's headings, the index rows from 64 rem, a search's rows — all required now.
- `tests/frontend/test_interior_w3_f1.py` — the AGAMI question as the disclosure's summary (§3.17 AG-2); the contact
  address's 44 px target now the head's action (its 48 px disc, every pointer; §3.12 C0+C1); the approdo's Forum tile
  outside the all-or-none and required bare (§2 K «l'approdo», Q4); the forum and interior import lists (§3.16, §3.2
  …§3.18, S's request §8).
- `tests/frontend/test_frontispiece_v515_c.py` — the network diagram's nodes are the map's named links to five entries,
  the drawing still aria-hidden, the old register gone (§3.11); the capitals title tracked on the story's step by its
  kept anchor (§3.2 + F1).
- `tests/frontend/test_content_pages_w3_f2.py` — `lettura.css`'s imports (§3.13–§3.15, S's request §8).
- `tests/frontend/test_mobile_rtl_w4_a.py` — the stand-alone link measured on `/ar/le-projet/` is the same «En savoir
  plus sur le promoteur», now under the story step's class (§3.2 LP-3).
- `tests/frontend/test_browser_w1_c.py` — a permalink followed from another page lands on its answer in the explorer
  (selected, shown, the others not); the accordion's drawn plus/minus is measured where the accordion stays, the
  promoter's question on /agami/ (§3.13 Q1, §3.17 AG-2).
- `tests/i18n/test_rtl_browser.py` — the Arabic accordion measured on /agami/ (the FAQ's rows are the explorer's,
  measured by W3-F2's reading-edge test) (§3.13 Q1, §3.17 AG-2).
- `tests/i18n/test_ui_translations.py` — the search's plural heading read from the library's chapter head (its h2
  carries a class before its id; the same heading, the same sentence) (§3.13).

**Runs** (targeted, `test_ile_v5_l7`, one at a time):
- the lane's apps (`apps/pages`, `apps/faq`, `apps/glossary`, `apps/living`, `apps/forum`, non-browser): see §10.1;
- `tests/frontend` non-browser (2 530 passed in the first full run; the failures it showed are fixed or recorded
  below): see §10.1;
- browser: `test_pages_browser_v522_p2.py` 15 passed; `test_content_pages_browser_w3_f2.py` 13 passed; the other
  suites that visit the lane's pages (`apps/pages/tests/test_browser.py`, `test_browser_contact_channels_v519.py`,
  `test_browser_w3_f1.py`, `test_mobile_rtl_w4_a.py`, `test_seal_heads_browser_v522_s.py`, `tests/i18n/test_rtl_browser.py`,
  `test_browser_w1_b.py`, `test_browser_w1_c.py`, `test_browser_w2_c2.py`) 152 passed and 5 failed; the five were
  stale expectations (updated above) or a real defect (the French category's direction, fixed): rerun, 5 passed.

**Not the lane's** (fail on design-v5 `22b0ddd` as well, lane S's library):
`tests/i18n/test_rtl_static.py::test_every_horizontal_shift_has_its_rtl_twin` (`_sec-tracciato.css`,
`.tracciato__linea::after`),
`tests/frontend/test_loader_rules.py::test_l3_attaches_only_to_fragment_containers` (a comment of
`components/sezioni/mappa.html` names `data-seat`) and
`tests/frontend/test_state_chips_carry_a_register.py::test_data_register_is_written_by_the_partial_and_by_two_legends_only`
(`components/sezioni/approdo.html` writes `data-register`). Requests in §9.

## 5. Found and fixed in the headed reviews (1440, 768, 390; fr and ar; reduced motion)

- **The letterhead wrapped onto two rows on every interior page**: the AGAMI plate's block was named `.targa`, the
  letterhead's reserved-space plate. Renamed `agami-id`; a test now forbids a page block that shadows a chrome class.
- **A FAQ permalink landed past its answer** (the trust band's, the fraud page's): the browser jumped to the answer in
  the long no-script list, then the module folded the answers into one cell. The explorer is now drawn as the module
  draws it from the first paint when the address names an answer, so the jump lands on it.
- **The phone's FAQ rows on the Arabic page**: a short question's button shrank to its words (its chevron beside
  them, its words short of the reading edge); the row is the whole row, the words end on the reading edge, the
  chevron at the row's far end.
- **The explorer's French questions on the Arabic page** ended mid-cell (W3-F2's M2): the plate's headings and the
  index rows now end on the reading edge; the answers read from their own start.
- **Four corner values on the FAQ and the glossary** (12 · 4 · 6 · full): the search seat takes the plates' 6 px.
- The Forum drew its seal three times; the hub and the actions' drawing are the mark itself, the head's the one seal.
- **The Forum's ring was shifted on the Arabic page** (the actors stood 190 px right of the hub): the sentence is a
  French run, so its spans' logical offsets read left to right while their translate read right to left. The places
  now mirror by themselves (counter-clockwise), the translate one; a browser test holds the symmetry.
- **The FAQ's French category name on the Arabic page** was set right to left; it is a French run again (its
  punctuation in place), its row reversed so the rule stays on the reading edge. The marked and selected index rows'
  2 px marker stands on the Arabic reading edge too.
- **Latin text on the Arabic pages** (I18N-08): the AGAMI website's host carries its language, the Forum's first
  section is named by its two headings (`aria-labelledby`) instead of a French `aria-label`, RUNTS is marked Italian;
  the ten new labels are translated (§7).
- **AGAMI's legal-review marker** (`CONTENT_PENDING_LEGAL_REVIEW`) is back in the template's comment, now naming what
  stays pending (the official notices), as `test_templates_static` requires.
- **AGAMI's emphasis** set the promoter's name; it now sets what §3.17 AG-1 names: «depuis 2011» and «l'Italie et le
  Maroc».
- Seat and spacing fixes from the earlier passes: the FAQ seal's position (fronte.css after lettura.css), the RTL seal
  overlap in the answer plate, empty «moment» space on the FAQ, Vivre and the Forum's tablet ring, the contact doors
  at 768 (three across), the external website as text (compliance).

## 6. Recorded choices and deviations

- **The Forum's and Vivre's light sweeps** are drawn in the markup (an SVG paint, the colour the token's) instead of a
  CSS gradient: the app sheets hold tokens only (`test_design_docs`); the library paints its sweep only for strato and
  approdo.
- **The map keeps the frontispiece's ring** (v5/_fronte.css §8) rather than `_sec-mappa.css`'s: «At rest the ring
  looks exactly as today» (§3.11); the class `mappa__anello` sits on the nodes' layer, which has the ring's box.
- **The approdo's Forum tile** is typographic by the library's contract while the band is a register: the guard now
  exempts that tile by name and requires it bare (§4).
- **`#contact-email-title`** — the old «Par e-mail» chapter's anchor — now sits on the head's address, which carries
  that chapter's content (C0 + C1); the registry entry stays alive (request to S in §9 if it should retire instead).
- **`{% chapter_mark "faq" %}`** is kept in the FAQ (it draws nothing in V2) so the registry's `faq` concept stays
  carried; S can retire both together.
- **The FO2b actors** are one register (`data-register`) by §4.10 («the Forum's nine actors»), their glyphs the four
  FO2b names; the five others carry none (nothing invented).
- **«Qui porte le projet»** keeps the FAQ's answer when it exists; the promoter's line otherwise — no new text.

## 7. New user-facing strings (French source → it / en / ar; added to `locale/` and compiled)

The ten msgids are in `locale/{it,en,ar,fr}/LC_MESSAGES/django.po` (appended, nothing dropped or reordered; the five
catalogue msgids the sources no longer use are left in place) and compiled with `scripts/i18n_audit.py --compile`;
the audit reports 3 704 msgids, 100 % in the four languages. Arabic reviewed for RTL: each is a label or a heading, no
Latin run inside except the channel's name; the locked texts are never translated (their Arabic pages carry
`lang="fr"`).

| French (msgid) | Italiano | English | العربية |
|---|---|---|---|
| Par téléphone, WhatsApp ou formulaire | Per telefono, WhatsApp o modulo | By telephone, WhatsApp or form | عبر الهاتف أو واتساب أو النموذج |
| Par téléphone ou formulaire | Per telefono o modulo | By telephone or form | عبر الهاتف أو النموذج |
| Par WhatsApp ou formulaire | Tramite WhatsApp o modulo | By WhatsApp or form | عبر واتساب أو النموذج |
| Code fiscal | Codice fiscale | Tax code | الرمز الضريبي |
| Siège social | Sede legale | Registered office | المقر القانوني |
| Siège opérationnel | Sede operativa | Operational office | المقر التشغيلي |
| Site officiel | Sito ufficiale | Official website | الموقع الرسمي |
| Contact officiel | Contatto ufficiale | Official contact | جهة الاتصال الرسمية |
| Où le rencontrer | Dove lo si incontra | Where you will come across it | أين ستصادفه |
| Pour s’installer | Per stabilirsi | Settling in | للاستقرار |

Every other string the lane prints is an existing msgid with its three translations («En bref», «Qui porte le
projet», «Le promoteur», «Inscription», «Italie», «Tous les formulaires du site sont acheminés vers cette adresse.»,
«En savoir plus sur le promoteur», «Lien direct vers cette question», «Mis à jour le», «Les parcours réguliers vers
l’Italie», «Forum Vénétie–Maroc», «%(project)s est promu par %(promoter)s.» …), a locked text, or a registry label.

## 8. 21st.dev provenance (rows for `COMPONENT_PROVENANCE.md`; read for structure only, nothing copied)

| Page · section | 21st.dev reference | What it lent |
|---|---|---|
| AGAMI · «la targa» | Key Value List · 25162 | the term/value rows of one plate, labels quiet, values set |
| Contact · «il centralino» | Contact Cards · 23175 | the channels as one object, one plate per channel |
| FAQ · explorer | FAQ Drawer · 43033 | the native disclosure's lift on a phone (no animation library) |
| Le projet · C | Scroll Reveal Content A · 19203; Services Stack · 33309 | the steps beside one figure, its layers by step |
| Réseau · H; Forum · FO2b | Nodes · 40282; Relay Hub Diagram · 40264; Fluid Hover Highlight · 39507 | the hub-to-node route that lights, the gliding highlight |
| FAQ · L; Glossaire · rail | Feature List Showcase · 27506; Scroll Spy · 23554 | master–detail; the spy's last part lit at 60 % |
| Le projet · E; Contact · E | Hover Expand Gallery · 27010 | the doors' weight and their foot rule under the hand |
| Le projet · D; Vivre · D | Scroll Reveal Image · 24466; Parallax · 20023 | the frame that widens, the slow drift |
| AGAMI · K; Forum · FO3 | Spotlight · Corner Frame (lane S's K rows) | the plates on a ground, the formwork marks |

## 9. Requests to other lanes (§9.7: lane P2 edited none of their files)

- **S (library)**
  - `components/sezioni/approdo.html` writes `data-register` by hand and the Forum's typographic tile sits inside it:
    `test_state_chips_carry_a_register…` fails on design-v5; decide whether the approdo is a register (then keep the
    exemption P2 wrote in `test_interior_w3_f1.py`) or drop the attribute.
  - `components/sezioni/mappa.html`'s comment names `data-seat` (`test_loader_rules::test_l3…` fails on design-v5).
  - `indice.js`: follow `hashchange` (a same-document link to another question does not select it today — no FAQ
    page links one question to another yet, so P2's tests follow permalinks from another page); on a phone, open the
    panel the address names (today every panel closes at load); the explorer's
    no-script layout could carry P2's `:target` rule (`_lettura-v2.css` «a permalink lands on its answer») for every
    page; `.indice[data-mode="disclosure"] .indice__apri` needs `inline-size: 100%` (P2 sets it on the FAQ).
  - `.indice__sigillo`'s position loses to `_sigillo.css` when `fronte.css` loads after the page sheet (P2 raised the
    specificity on the FAQ).
  - A French index row on an Arabic page (`.indice__voce[lang="fr"]`) is a left-to-right row: its 2 px marker and its
    wider padding fall on the left, away from the reading edge; P2 mirrors both on the FAQ (`_lettura-v2.css`), the
    library could for every `[lang]` row.
  - A generic light-sweep paint for `[data-verb~="light"]` would let page sheets drop their own (§6).
  - `apps/core/icons.py`: the `contact-email-title` anchor and the `faq` concept are kept alive by P2 (§6); retire
    them if the registry should follow V2's removals.
  - The panorama's credit inset while the frame widens; `spia.js` measures `--spia-y` only (a horizontal band would
    need x and width).
- **P1**: keep `#apres-l-arrivee` on `/formation/` («Pour s'installer» links to it); if the pilot page's approdo
  meets the same all-or-none guard, P2's exemption in `test_interior_w3_f1.py` covers it.
- **Steward**: ownership rows for the new files (`apps/pages/identity.py`, `apps/forum/templatetags/forum_v2.py`,
  `apps/cms/static/cms/_lettura-v2.css`, `apps/pages/static/pages/css/_{projet,rete,contatto,agami,frodi}.css`,
  `templates/pages/partials/{projet,agami}/`, `fronte/_rete_pannelli.html`, `templates/faq/_{risposta,collegamenti}.html`);
  a review of the ten translations of §7 (added to `locale/` by P2, as the i18n audit requires); the provenance rows
  of §8.
- **Performance lead**: LCP, CLS and INP of the ten pages on the merged preview (the explorer, the map and the story are
  dynamic chunks after load; Vivre's LCP photograph is never masked).

## 10. Not done, or open

- The three library failures above (S's), each failing on design-v5 as well.
- The reading pages' CSS total is 66 B under its ceiling.

### 10.1 Final runs (`test_ile_v5_l7`, one pytest at a time)

- **Static, after the last change** — `apps/pages`, `apps/forum`, `apps/faq`, `apps/glossary`, `apps/living`,
  `tests/compliance`, 25 files of `tests/frontend` (frontispiece, interior W3-F1, chapter marks, icons, O14 lint,
  design docs, CSS bundle, content pages W3-F2, sezioni V5.22 S, imagery V5.22 M, static assets, SVG, template comments,
  CSS tokens, V5 tokens, motion rules, rm parity, reduced motion, script motion gate, layout, terminology, French
  typography, loader rules, state chips) and `tests/i18n/test_rtl_static.py`: **2 607 passed, 3 failed, 1 skipped** —
  the three are lane S's library failures that fail on design-v5 as well (§4).
- `tests/i18n/test_page_integrity.py` and `test_ui_translations.py` after the catalogue: **69 passed**.
- Earlier full runs on this branch: `tests/frontend` non-browser (2 530 passed; every failure it showed was fixed, or
  is S's), `apps/*` + `tests/compliance` + `tests/i18n` (1 324 passed; the i18n failures it showed were fixed).
- **Browser, final** — `test_pages_browser_v522_p2.py`, `test_content_pages_browser_w3_f2.py`,
  `tests/i18n/test_rtl_browser.py`, the stand-alone link targets of `test_mobile_rtl_w4_a.py`, the FAQ permalink of
  `test_browser_w1_c.py`, `test_browser_contact_channels_v519.py`, `apps/pages/tests/test_browser.py`: **86 passed**.
  Before the last fixes, the other browser suites that visit the lane's pages (`test_browser_w3_f1.py`,
  `test_seal_heads_browser_v522_s.py`, `test_browser_w1_b.py`, `test_browser_w2_c2.py`, the rest of
  `test_mobile_rtl_w4_a.py` and `test_browser_w1_c.py`) passed in the 152 of §4.
- `ruff check` and `ruff format --check` clean on every Python file the lane changed; `npm run build:css` current.

## Round 1 improvements (label v522-p2-improve1, 2 November 2026)

After QA round 1 (`evidence/v522/p2/QA_ROUND1.md`: not passed — 10 major, 14 minor). design-v5 had not moved from the
build's base `22b0ddd`: no merge. Lane server 8787 (DB `ile_v5_l7`, reference date 3 October 2026, the WhatsApp number
read by the launcher from the private environment). Headed chromium-1234 and the browser suites in the shared lock slots
A and B: 30 holds, the longest 10 min 6 s, each released (`.work/v522-p2-improve1/logs/locks.log`). Evidence in
`evidence/v522/p2/imp1/`: `imp1_before_*` the state at `87a85df`, `imp1_p2_*` · `imp1_p3_*` · `imp1_p7_*` · `imp1_p8_*`
· `imp1_p9_*` · `imp1_p12_*` the result, `imp1_probe1…18.json` the measures, `requests/` the two patches proposed to
lane S (`imp1_probe10.json` and `imp1_p10_*`: the patches run in the browser). Tools: `.work/v522-p2-improve1/tools/`.

### R1.1 The majors

- **M1 — FAQ permalinks below 64 rem (P2's half; S's half requested with a patch tested in the browser).** With script
  the phone's explorer is drawn from the first paint as `indice.js` draws it (`html.js` is set before the first paint):
  the index said by the panels, each question its 44 px row with the chevron's room kept, the answer plate's seal hidden
  (its 68 px were what every question jumped by), every answer folded but the one the address names; the letterhead's
  height is the page's scroll padding (`html:has(.faq-esploratore)`, WCAG 2.4.11). The browser's jump and the module now
  agree: a permalink followed from another page leaves its question 88 px from the top, under the 57 px letterhead, at
  390 and 768, fr and ar (it was 265–544 px above the screen, or in the footer). Opening the named answer on a phone and
  following `hashchange` are `sezioni/indice.js`'s — patch in R1.4, run in the browser through request interception:
  fresh permalink opened and under the letterhead (88 px), same-document links and the address bar opened and brought
  under it (72 px; at once from the keyboard), the desktop's same-document selection right, no errors. Held by
  `test_a_faq_permalink_followed_from_another_page_lands_on_its_question` (1440, 768, 390; the five anchors; fr, ar).
- **M2 — Réseau, Arabic lines.** `[dir="rtl"] .fronte-rete__lines { scale: -1 1 }`: the line layer mirrors with the
  logically placed nodes (the resting pentagon is symmetric). Entreprises in Arabic: spoke 189–396, disc at 189 (the
  spoke ended at 603). Held by `test_the_chosen_actor_s_spoke_ends_on_its_own_disc` (each actor, fr and ar).
- **M3 — CLS.** The map's entries stand in one cell from the first paint, the address's entry or the first one shown,
  wherever the module will build the tablist (from 20.75 rem; narrower the list stays the map, as `mappa.js` leaves it);
  the FAQ's phone form as in M1. Measured after the last change (`imp1_probe8.json`): 0 on Réseau (fr and ar at 1440, ar
  at 1024) and on the FAQ (fr and ar at 768 and 390), where it was 0.117–0.336. Held by
  `test_the_map_and_the_explorer_never_move_the_page_as_they_load` (≤ 0.1 at 1440, 1024, 768, 390).
- **M4 — Le projet's figure.** The plate is a size container — square from 64 rem (at most `min(32rem, 70vh)`), a 3:2
  panel below — and the figure the largest square inside it (`min(100cqi, 100cqb)`): 442 px at 1440, 382 at 1366 and
  1280, 312 at 1024, every disc inside the plate in fr and ar. With it m14: at 768 a 673 × 449 panel holds a 401 px
  drawing (it was a 190 px strip). Held by `test_the_story_s_figure_stays_inside_its_plate` (1440 → 390).
- **M5 — Contact's WhatsApp plate.** `.canali` is a wrapping flex row: each plate at least as wide as its own words (a
  flex item's automatic minimum — the number, never broken, cannot run past its plate), the two side by side only where
  both stand at ease (1440: 421 + 382 px), stacked at the board's width below (1366 → 360). Overflow 0 px at the eight
  widths, fr and ar. m7 with it: the plates at 6 px.
- **M6 — The address never breaks.** The report plate and AGAMI's contact column are inline-size containers; the
  address is set at the size its column holds on one line (`clamp(1rem, 7cqi, …)` on the report, `6.8cqi` for AGAMI),
  never broken (`.email` nowrap), its disc above it when the row cannot hold both; AGAMI's contact column stands beside
  the registers only from 80 rem (under them, after a hairline, below). One line at the eight widths, fr and ar (the
  report 20 → 16.9 px at 360; AGAMI 28 → 20.7 px). M5 and M6 held by
  `test_every_channel_holds_its_words_and_an_address_never_breaks` (eight widths, fr and ar).
- **M7 — Glossaire.** One register: the ten cards in one grid (two columns from 48 rem, three from 80) — four rows at
  1440, the page 2 802 px (it was 4 798). A letter's first card carries its letter as its heading (`h2#lettre-X`, before
  the cards' `h3`), large in the card's end corner: the anchor the rail spies, the marker the eye finds. Each card
  answers the hand and the focus (its letter takes the accent, its reading-edge rule grows from 40 % to its full
  height); the rail's indicator is a 2 px accent that glides. The rail still spies on the same anchors, now by rows:
  letters whose first cards share a row cross `spia.js`'s line together and the row's last one is marked (scrolling at
  1440 and 1280 lights D, N, R, V; a letter followed from the rail lights its row's — C → D, L → N — and, the register
  ending there, P–R → V: `imp1_probe15.json`). Each letter's box runs down its card, so a followed letter, landing under
  the letterhead above the spy's line, still updates the rail (it stayed on the letter read before); lighting the
  followed letter itself, and a row's letters together, is the module's (request in R1.4). The term page: the outlined
  initial on the free side in both directions (on the Arabic page the letter takes the page's direction: `main.css`
  turns an Italian run left to right, and the logical inset, resolved on the run's own direction, stood it behind the
  plate); the related terms' definitions disclosed in place (§1 rule 7) by the library's native exclusive disclosure,
  each with the way to its own page — the page's own interaction. Also fixed: on a touch screen the coarse pointer's
  target rule set `position: relative` on the term's link and held the card's stretched link inside the term.
- **M8 — Vivre en Italie.** (a) The LCP's scale runs (`.vivere-panorama__quadro .foto > picture`; `vivere-scala` among
  the page's animations at 1440 and 390, fr and ar). (b) «Pour s'installer» on stone in two rows of one kind each: the
  two terms as the glossary's own dictionary cards (the definition whole, «Où le rencontrer», the card's response), then
  the two ways on (the training after the arrival, the FAQ) as route tiles — no emptied lead tile. (c) The cards' and
  tiles' responses are the page's own interaction. m10: the lead's plate is no longer a `.page-header`, so its words no
  longer wait in the head's `rise-in`.
- **M9 — Forum.** (a) From 64 rem the page's index stands under the entrance's words (two columns of hairline rows, one
  link a cell — never a wrapped row, W3-F1 m3) and the `ile-forum` drawing has the end seat at display scale over its
  light. (b) The audience ring redrawn on its box's own proportions (`viewBox 0 0 160 95`, uniform scaling: the stroke
  verb's `pathLength` dash is exact — no fragments in motion): a dotted orbit through the places, each spoke solid from
  the hub to its actor, the hub mark at display scale (`clamp(6rem, 10vw, 9rem)`) on the night's light (an SVG paint:
  an app sheet holds tokens only). (c) The page has a state: the index is a scroll-spy (`sezioni/spia.js`,
  `aria-current="location"`: Pourquoi → Objectifs → À qui s'adresse-t-il as the reader scrolls), and the two action
  plates light the faint mark behind them (`data-azione`).
- **M10 — AGAMI and Attention aux fraudes.** AGAMI: the colonnade is a close architectural crop (`slice` on its foot —
  entablature and columns run off the plate, the pediment's slopes leave through the top), its stylobate the plate's
  foot; from 64 rem the plate stands the row's height and its sill continues across the gap into the text column's
  foundation line (it draws after the colonnade); the light between the two middle columns answers the band's action —
  the promoter's question, hovered, focused or open (the address the review named stands in the next band; its own
  response stays the disc and the underline). The second sweep left: the page reads MASK (the colonnade) → DRAW + NODE
  in sequence (the identification) → LIGHT (the approdo). Fraudes: the report plate takes the protection's idiom — a 3
  px ink top rule drawn from the reading edge, the `ile-scudo` mark at body scale (3 rem) standing on it; the address is
  the seal system's action (`data-azione`): its hover and focus deepen the keyhole; the plate stands the row's height,
  its action on a hairline at its foot (no empty band under it).

### R1.2 The minors

- **m1** — the same-document permalink is `indice.js`'s `hashchange`: in the patch of R1.4, with the assertion to
  restore in `test_browser_w1_c.py::test_a_link_to_an_faq_row_opens_it` (the build's sequence `/faq/` then
  `/faq/#second`, run against the patch: the second question selected and shown, the first not). P2 cannot restore it
  green without S's file (§9.7): **a merge condition**, with M1's second half.
- **m2** — `locale/**`: the build's ten msgids stay as committed (the i18n audit must stay at 100 % on the branch);
  recorded as an exception for the steward, who carries the catalogue at merge (lane M's precedent). This round adds no
  msgid.
- **m3** — the notes now say what phones do (R1.5): the map is a tablist wherever its ring is 300 px or more — every
  width from 332 px — and its list below; `test_a_phone_s_map_is_a_tablist_and_a_narrow_ring_its_list` exercises 390
  and 360 (tablist) and 320 (list): no `pragma: no cover` branch left.
- **m4** — a deep link `/reseau/#rete-<actor>` keeps the map in view from 64 rem (the entries'
  `scroll-margin-block-start: 100vh`: the page stays at its top with that actor chosen — scrollY 0). Bringing a phone's
  chosen entry into view is `mappa.js`'s: patch in R1.4, run in the browser (390, fr and ar, with and without reduced
  motion, pointer and keys: the entry ends inside the screen).
- **m5** — the approdo's Forum tile carries the Forum's own prescribed subtitle (`p2.forum.header.subtitle`, whole;
  marked French on the other languages' pages). Still without an arrow: the W3-F1 guard keeps a typographic tile
  without an icon (Q4).
- **m6** — the doors (Le projet, Contact) align their content to the top.
- **m7** — see M5.
- **m8** — AGAMI's offices: the Italian lines one left-to-right box hanging from the reading edge, the country under it.
  Vivre's definitions start-aligned as the glossary's (one component now). The Forum on the Arabic page: a column whose
  title is a French run is one left-to-right box (its title, words, list and station line on one edge — measured: the
  same left edge in the four columns at 1440, 1024 and 390); an action's French label hangs from the reading edge
  beside its disc.
- **m9** — the keyboard path animates nothing in the story (step inks, figure layers; the improvised arrows' loop is
  guarded too), the doors' arrows or the contact board (discs and plates): measured with `data-input="key"`, no
  transition left there; the pointer keeps its responses.
- **m10** — see M8.
- **m11** — each office reads «Via Sandrigo n. 29, 36061 Bassano del Grappa (VI), Italie» in the text and the
  accessibility tree (visually hidden commas — the owner's own punctuation, no new string).
- **m12** — a clause's last word and its punctuation never part (the `forum_coda` filter, markup only).
- **m13** — without script and with a hash every answer stays listed (the first-paint rules are `.js`-scoped): 9 of 9
  shown at 1440 and 390.
- **m14** — see M4.

### R1.3 Budgets (gzip -9, the tests' method; `main.css` untouched)

| Sheet / page | Build | Round 1 | Ceiling |
|---|---|---|---|
| `pages/css/interior.css` | 10 431 | 10 827 | 11 264 |
| `cms/lettura.css` | 8 825 | 8 871 | 9 216 |
| `forum/forum.css` | 6 890 | 7 238 | 8 192 |
| interior pages (`/fr/contact/` …) | 55 832 | 56 228 | 56 320 |
| reading pages (`/fr/faq/` …) | 54 226 | 54 272 | 54 272 |
| `/fr/forum/` | 46 150 | 46 498 | 54 272 |

Paid for by merging what the pages drew twice (the doors' arrows of Le projet and Contact, AGAMI's label styles, the two
chip families), removing dead or inert rules (`.glossary__letter`, a print rule made moot, two declarations without
effect), shorter equivalent selectors (`[lang]` on the explorer's foreign runs), and by dropping the first pass's lights
drawn with CSS gradients — an app sheet holds tokens only (`test_design_docs`): the shield's foot light and the address
light went, the Forum's lights are SVG paints in the markup. The reading pages stand at their ceiling (0 B left): lane
S-close can free `static/css/v5/_fronte.css`'s `.fronte__wide*` rules (they match nothing since the build) before
anything is added to them.

### R1.4 Requests to other lanes (§9.7: P2 edited none of their files)

- **S** — `static/js/src/sezioni/indice.js` (`evidence/v522/p2/imp1/requests/indice.js.patch`, `git apply -p1`):
  below 64 rem `mode()` opens the panel the address names (`open(named(), true)`, the others folded — what P2's first
  paint draws); a `hashchange` listener selects the named tab from 64 rem and, below, opens the named panel and brings
  its heading under the letterhead (`scrollIntoView`, the page's scroll padding; `instant` from the keyboard and under
  reduced motion through `motion.js`'s `reducedMotion()` — the one gate). Then restore the same-document step of
  `test_browser_w1_c.py::test_a_link_to_an_faq_row_opens_it` (m1) and tighten P2's
  `test_a_faq_permalink_followed_from_another_page_lands_on_its_question` below 64 rem from «no other answer open» to
  «its answer open» (`aria-expanded="true"`). Run in the browser: `imp1_probe10.json`.
- **S** — `static/js/src/sezioni/mappa.js` (`requests/mappa.js.patch`): a committed choice (click, keys) whose entry
  lies outside the screen brings it into view (`block: "nearest"`; `instant` from the keyboard and under reduced
  motion). Run in the browser: `imp1_probe10.json`.
- **S** — `static/js/src/sezioni/spia.js`, for a register laid as one grid (the glossary since M7): parts that cross
  the line in the same frame are one stop — mark them together (the indicator spanning their links, `aria-current`
  on the first) instead of the last of them; a followed link is current at once and stays so through the scroll it
  started (`scrollend`); the last part's rule («lit once most of it shows») only when the page can scroll no further.
  Today C, L, P and Q are never lit, and following P lights V.
- **S-close** — the `.fronte__wide*` rules of `static/css/v5/_fronte.css` (R1.3).
- **Steward** — the build's ten msgids in `locale/**` (m2): the catalogue at merge.

### R1.5 Corrections to the build's notes

- §1, Réseau: «on a phone (a ring under 300 px) the map is its list» — the ring is 300 px or more from a 332 px
  viewport: the map is a tablist on every phone width but the narrowest (320).
- §1, Vivre: the scale now runs (M8a); before this round it did not.
- §1, FAQ: «every permalink … opens its answer» holds from 64 rem; below, the question lands under the letterhead and
  its answer opens with S's patch (R1.4).

### R1.6 Found by this round's own runs, fixed before the commit

- `test_design_docs` (tokens only): the glossary rail's `--spia-y` / `--spia-h` had lost their declaration in a byte
  trim — declared again (0 until `spia.js` writes them); the Forum's actions band declares its resting `--light: 0`
  (the seal system's property, which `v5/_sigillo.css` raises to 1 on the section).
- `test_rtl_static` (logical properties only): the term page's initial is back on `inset-inline-end`; on the Arabic page
  the letter takes the page's direction instead of physical insets.
- `test_content_pages_browser_w3_f2` (three corners a screen): a byte trim had put the search seat's corner rule at the
  head's own specificity, and `fronte.css` loads after this sheet — the seat drew 12 px again on the FAQ and the
  glossary; it is `form.search-form` now (6 px). The suite's Vivre lead check follows m10 (the lead's plate is no longer
  a `.page-header`; the same measures).
- `test_pages_browser_v522_p2`: a letter followed from the rail left the rail on the letter read before — each
  letter's box now runs down its card (M7). Two of this round's new tests corrected, their invariants unchanged: the FAQ
  permalinks are each opened from another page (from `/faq/#a`, `/faq/#b` is the same document — the loop measured
  nothing new), and the spoke is measured after its draw with the pointer off the ring (while the head's entrance moves
  the nodes, one passing under a resting pointer previews itself — the fine pointer's hover: `data-sel` went back to
  the hub).
- The contact board's plates: their border and shadow transition is guarded on the keyboard path as the discs' (m9).

### R1.7 Final runs (`test_ile_v5_l7`, one pytest at a time; a Chromium lock slot held for each browser run)

- **Static, the full targeted set** (25 files of `tests/frontend`, `tests/compliance`, `tests/i18n`, `apps/cms`):
  2 083 passed, 5 failed — lane S's three library failures (they fail on design-v5 `22b0ddd` too: §4) and two of this
  round's, fixed (R1.6). After the fixes: `apps/pages`, `apps/glossary`, `apps/living`, `apps/forum`, `apps/faq`, W3-F1
  interior, W3-F2 content pages, sezioni V5.22 S, template comments, design docs, RTL static, CSS bundle, budgets:
  **1 288 passed, 1 skipped** (the WhatsApp number, set only in the private environment), 1 failed (S's); motion rules,
  O14 lint, rm parity, reduced motion, mobile RTL, CSS tokens, loader rules, state chips, script motion gate, motion
  V5.12: **389 passed**, 2 failed (S's — corrected in round 2, R2.2 m7: the two were this lane's, the motion
  module's FAQ test, QA_ROUND2 M4); after the last CSS change — design docs, RTL static, CSS bundle, budgets, CSS
  tokens, template comments: **393 passed**, 1 failed (S's).
- **Browser**: `test_pages_browser_v522_p2.py` **25 passed** (after the last change);
  `test_content_pages_browser_w3_f2.py` **13 passed**; `tests/i18n/test_rtl_browser.py`,
  `test_browser_contact_channels_v519.py`, `apps/pages/tests/test_browser.py`, `test_browser_w1_c.py` **66 passed**;
  `test_mobile_rtl_w4_a.py`, `test_browser_w3_f1.py`, `test_seal_heads_browser_v522_s.py` with `test_rtl_browser.py`
  again after the last change **97 passed**.
- `ruff check` and `ruff format --check` clean on every Python file this round changed; `npm run build:css` current
  (no JS source changed: S's modules untouched); every changed file LF.
- `test_browser_w1_b.py`, `test_browser_w2_c2.py` after the last change: **33 passed**.

### R1.8 Not done, or open

- M1's second half (a phone opens its permalink's answer), m1 (the same-document permalink) and m4's phone half (the
  chosen entry into view) are lane S's modules: patches in `requests/`, run in the browser (R1.4). m1's restored
  assertion is a merge condition.
- The glossary rail lights a row's last letter (R1.1 M7): the per-letter or per-row light is `spia.js`'s (R1.4).
- The reading pages' CSS stands at its ceiling (54 272 B): anything added to them needs a saving first — S-close's
  `.fronte__wide*` rules are the next one (R1.4).
- Lane S's three library failures (§4), unchanged.

## Round 2 improvements (label v522-p2-improve2, 2 November 2026)

After QA round 2 (`evidence/v522/p2/QA_ROUND2.md`: not passed — 8 major, 8 minor). design-v5 stood at `22b0ddd` when
the round started (no merge); lane P1 merged into it during the round (`dba97fa`, recorded `269cf39`) — not merged here
(R2.9). Lane server 8787 (DB `ile_v5_l7`, reference date 3 October 2026, the WhatsApp number read by the
launcher from the private environment). Headed chromium-1234 for every visual check, the browser suites headless, all
in the shared lock slots: B 08:17–08:27, B 08:34–08:56, A 09:05–09:07, B 09:24–09:39, A 09:39–09:46, A 09:47–09:55
and the later sessions of R2.7 (`.work/v522-p2-improve2/logs/locks.log`), each under 25 minutes, each released.
Evidence in `evidence/v522/p2/imp2/`: `imp2_before_*` the state at `0554cde`, `imp2_a_*` … `imp2_e_*` and `imp2_sw_*`
the result, `imp2_probe1…3.json`, `imp2_look2/3/6*.json`, `imp2_sweep1.json` the measures, `requests/` the patches for
lane S and the P2 half that goes with them. Tools: `.work/v522-p2-improve2/tools/`.

### R2.1 The majors

- **M1 — a FAQ permalink no longer moves the page as it lands.** From 64 rem the explorer is drawn from the first paint
  as the tabs draw it: every answer in the stage's one grid cell (the stage the tallest answer's height), the first
  shown, `:target` switching which one is *visible* — never `display` (`cms/_faq-v2.css`). Below 64 rem the first paint
  folds every answer, as `sezioni/indice.js` folds them today (its fold of the named answer was round 2's 0.10 at 768).
  Measured (`imp2_probe1_faq_permalinks.json`): 40 arrivals from another page — five anchors, fr and ar, 1440, 1024,
  768, 390 — CLS ≤ 0.0001; from 64 rem the named question selected and its answer shown 72–82 px from the top; below,
  the question 72 px from the top under the letterhead. Held by the new
  `test_a_faq_permalink_arrives_without_moving_the_page` (the same four widths, fr and ar, the five anchors, ≤ 0.1).
- **M2 — the phone's named answer and the same-document permalink (lane S's module; P2's half ready).** Opening the
  named answer and following `hashchange` stay `sezioni/indice.js`'s (round 1's patch, `requests/indice.js.patch`,
  still applies). P2's half is one patch to apply in the same commit (`requests/p2_with_lane_s.patch`): the phone's
  first paint shows the named answer again (`:not(:target)` back), W1-C's same-document step restored
  (`test_a_link_to_an_faq_row_opens_it`: `/faq/#a` then `/faq/#b`, the second selected and shown) and P2's permalink
  test tightened below 64 rem to «its answer open» (one `aria-expanded="true"`, its body the one shown). Run in the
  browser with both through request interception (`imp2_probe3_indice_patched.json`): from another page every named
  answer open on a phone (768 and 390, fr and ar), the question 88 px from the top; CLS 0–0.055 at arrival (under the
  gate); the same-document permalink selects (1440) or opens (768, 390) its answer. Until both land, the phone's
  permalink lands on its folded question with nothing moving — a merge condition, as the reviewer set it.
- **M3 — the scroll-spy (lane S's `spia.js`; the patch, run in the browser; P2 ready).** `requests/spia.js.patch`
  (`spia.js.proposed`, 808 B gzip, under its 1 024 B ceiling): parts that cross the band in one frame are one stop —
  marked from its first (`aria-current`), the indicator spanning their links, the others flagged `data-spia-con`; a
  followed link (a click, Enter) is current at once and stays so through the scroll it started; the last part's
  «lit once most of it shows» only while no part holds the band (it lit V ahead of the row being read). Measured with
  the module replaced by request interception (`imp2_probe2_spia_proposed.json`): the glossary — each of the eight
  letters followed lights itself (8 of 8) and a scroll-through lights all eight, fr and ar, 1440, 1280 and 1024 (today:
  3–4 of 8 followed, 4–5 lit by the scroll); the Forum — a scroll-through lights all five sections (today 3: QUI
  SOMMES-NOUS and QU'EST-CE QUE LE FORUM never). P2's sheets already colour a row stop's other links (`[data-spia-con]`
  on the rail and the sommaire); the assertions (`test_the_spy_lights_each_letter_followed_and_each_section_read`) are
  in `requests/p2_with_lane_s.patch`. Without S's module the glossary's own letters now say the row (M6). A merge
  condition with M2.
- **M4 — the red guard migrated; every browser module that visits the lane's pages run.**
  `tests/frontend/test_motion_v512_a_w2.py::test_the_head_s_hairline_draws_at_load_and_a_question_opens_its_height`
  (V5.20 strict rule, citing V5.22 §3.13 Q1 and §3.17 AG-2): the FAQ no longer meets its head with a chapter nor has
  accordion rows, so the two invariants are measured where they stand — the head's hairline on `/fr/orientation/` (a
  head meeting its first chapter, a page V5.22 does not recompose: draws once at load, still under reduced motion), the
  system's disclosure on `/fr/agami/` (opens its height on its tinted plate, at once under reduced motion). AGAMI's
  question now sits in its `.accordion` (it opened at once: the height motion of V5.12 M6 needs the wrapper's
  `interpolate-size`). Every module the reviewer listed was run on this round's tree (R2.7).
- **M5 — the Arabic term page's title on its reading edge.** The h1 takes the page's direction and holds the term as a
  `lang="it"` run (`apps/glossary/views.py`; `templates/glossary/term.html`): its words end on the reading edge beside
  the seal — gap 0 at 1440 and 390 (`imp2_look2.json`, `imp2_sw_glossaire_nulla_osta_ar_1440.png`). W3-F2's
  `test_the_latin_heads_of_the_arabic_pages_end_on_the_reading_edge` now visits `/ar/glossaire/nulla_osta/`.
- **M6 — the Glossaire moves, draws and answers.** The register's letters are drawn — outlined as the term page's
  initial (`-webkit-text-stroke`, the fill transparent; the h2 keeps its text) — and lit: each letter takes the accent
  while it crosses the reading line (scrubbed by the scroll, `animation-timeline: view()`, a third of the screen; a
  row's letters light together — the honest stop of a three-column register — and the light reverses with the scroll),
  on a phone as on a desktop; under the hand or the focus its card's letter fills. In view at load (the section
  runtime then writes no state, so S's STAGGER never played) the cards' reading-edge rules draw in the head's own
  sequence, column by column. Measured: L and N lit at the line, C and V grey (`imp2_look2.json`); rules animating at
  load. Held by `test_the_glossary_letters_are_drawn_and_light_as_they_cross_the_reading_line` (fr, ar). The rail's
  per-letter light is M3's.
- **M7 — Attention aux fraudes answers its own question, and the hand.** The FAQ's way is the page's disclosure: the
  prescribed question opens the prescribed answer in place (the system's accordion on a plate, closed; the question and
  the answer whole and once on the page, the FAQ's permalink under the answer — §1 rule 7), the two other ways stay
  route tiles. The report plate stands its own height (sticky beside the routes from 64 rem), the address right under
  its sentence (no empty band inside it). The address's response is seen: a light runs along the sill from the reading
  edge (an accent layer, `--light` 0 → 1) and the shield's keyhole fills (tone 0.14 → 0.80), hover equal to focus, at
  once from the keyboard (`imp2_d_fraudes_plate_rest.png` / `_hover.png`). In view at load on a desktop the sill draws,
  the shield strokes and the tiles' rules follow in the head's sequence (below the fold the runtime plays the same
  verbs). On the Arabic page the French question ends on the reading edge. Held by
  `test_the_fraud_page_answers_its_question_and_its_address_answers_the_hand` and the static test's new assertions.
- **M8 — Vivre en Italie: what carries its interaction.** The head's T1 `ile-vivere` draws in the head's own sequence
  (§4.9 n° 13: the roofline and the door, the sprout 300 ms later and rising its 2 units, the door's tone last — the
  frontispiece's seal draw, here on the band's seal); the title row ends on the band's action — «Pour s'installer»
  (the band's own title, an existing msgid), the way down to the band — whose hover and focus light the seal's door
  (tone 0.14 → 0.74, the threshold light 22 → 48 %: the seal system's `data-azione` on the head's scope). Then the
  band's dictionary cards and route tiles answer the hand and the focus. Held by
  `test_vivre_s_seal_draws_in_the_head_and_its_door_answers_the_band_s_action` (fr, ar; drawn at rest under reduced
  motion) and the static test (`imp2_c_vivre_fr_1440_head_rest.png` / `_hover.png`).

### R2.2 The minors

- **m1** (S) — `requests/mappa.js.patch` (round 1's, still applies): a phone's chosen entry brought into view.
- **m2** — below 64 rem the Forum's drawing stands under the page's index on the band's foot, framed to the mark's drawn
  band (the cavea's crown to under its sill; its empty sky cropped): the frame overlaps no link — 0 px² at 768 and 390,
  fr and ar (`imp2_look7.json`, `imp2_f_forum_*`) — and its arcs cross none at 1024, 768, 390 and 360
  (`test_the_forum_s_drawing_never_lies_under_its_index`).
- **m3** — AGAMI's portico is the plate's width on its own proportions, on the plate's foot: its scale follows the
  width only, so opening the question (the row grows, 416 → 551 px at 1440) shows more of the pediment and never
  re-scales the colonnade (490 × 408 before and after: `imp2_look2.json`;
  `test_the_portico_keeps_its_scale_when_the_question_opens`, 1440 / 1280 / 1024, fr and ar).
- **m4** — recorded deviation (§6): the term page keeps the term as the head's h1 at display size and opens its plate
  on the definition; §3.14 T1 sets the term at `--t-display` inside the plate too — in one screen that prints the term
  twice at display size, so the plate opens on the drawn rule and the definition. For the Director.
- **m5** — budgets: the route sheets (R2.3).
- **m6** — `locale/**`: unchanged this round (no new msgid: «Pour s’installer» and «Questions fréquentes» exist); the
  build's ten msgids stay the steward's catalogue at merge.
- **m7** — R1.7 corrected: the motion module's two red browser tests were this lane's (the FAQ's explorer removed what
  they waited for), not lane S's — M4; and R1.7's browser runs did not cover every module that visits the lane's pages —
  R2.7 does.
- **m8** — (the reviewer's process) nothing to do.

### R2.3 Budgets (gzip -9, the tests' method; `main.css` untouched) — the route sheets

The owner's V5.22 standing constraint asks for page-only sheets and route-specific bundles with their own budgets. The
reading pages stood at their ceiling and this round's work needed room: each page's own compositions now live in a
route sheet linked by that page only, between its shared sheet and the frontispiece's (the cascade order unchanged).
`cms/lettura.css` keeps what the reading pages share; `cms/faq.css` holds L «l'indice» and the explorer's own rules,
`cms/lessico.css` the glossary's, the term page's and Vivre's; `pages/css/interior.css` keeps what the institutional
pages share (Le projet's and Contact's partials share the doors and stay in it), `pages/css/rete.css`, `agami.css` and
`frodi.css` hold Réseau's, AGAMI's and the fraud page's. The term page's related definitions became the system's
accordion (main.css) so it needs no pattern sheet. Every other reading page (news, partners, the Forum virtuel, the
legal pages, the forms, the consents) no longer downloads the V2 compositions at all.

| Sheet / page | Round 1 | Round 2 | Ceiling |
|---|---|---|---|
| `cms/lettura.css` | 8 871 | 6 509 | 9 216 |
| `cms/faq.css` (new) | — | 1 925 | 2 048 |
| `cms/lessico.css` (new) | — | 2 336 | 2 560 |
| `pages/css/interior.css` | 10 827 | 8 799 | 11 264 |
| `pages/css/rete.css` (new) | — | 1 817 | 2 048 |
| `pages/css/agami.css` (new) | — | 1 667 | 2 048 |
| `pages/css/frodi.css` (new) | — | 1 200 | 1 536 |
| `forum/forum.css` | 7 238 | 7 336 | 8 192 |
| `/fr/faq/` | 54 272 | 53 835 | 54 272 |
| `/fr/glossaire/`, the term page, `/fr/vivre-en-italie/` | 54 272 | 54 246 | 54 272 |
| `/fr/contact/`, `/fr/le-projet/` | 56 228 | 54 200 | 56 320 |
| `/fr/reseau/` | 56 228 | 56 017 | 56 320 |
| `/fr/agami/` | 56 228 | 55 867 | 56 320 |
| `/fr/attention-aux-fraudes/` | 56 228 | 55 400 | 56 320 |
| `/fr/forum/` | 46 498 | 46 596 | 54 272 |

The five new sheets have ceilings and each route its type's total in `tests/frontend/test_frontispiece_v515_c.py`
(added — stronger invariants). The glossary family's 26 B left is the next round's limit: anything more there needs a
saving first (S-close's `.fronte__wide*`, or a Vivre-only sheet). `imp2_budgets.txt` holds the measure.

### R2.4 Tests changed (V5.20 strict rule: each cites V5.22 / QA_ROUND2 in the test)

- `tests/frontend/test_motion_v512_a_w2.py` — M4 (above).
- `apps/glossary/tests/test_views.py` (two cases) — the term is still marked Italian, as the run inside the h1 (M5).
- `apps/pages/tests/test_interior_v522.py` — the fraud page's disclosure (question and answer whole, once; the
  permalink under it; the two tiles) instead of the FAQ tile (M7); the term page's h1 (M5) and its related definitions
  as the system's accordion (m5); Vivre's head action in the seal's scope (M8); the family's sheets — the shared ones'
  imports, each route sheet's imports, linked by exactly its pages, never in `main.css`, between its shared sheet and
  the frontispiece's (new `test_a_route_sheet_sits_between_its_shared_sheet_and_the_frontispiece_s`).
- `tests/frontend/test_content_pages_w3_f2.py` — `lettura.css`'s imports without L (now the FAQ's route sheet's), and
  the two route sheets' imports; `tests/frontend/test_interior_w3_f1.py` — `interior.css`'s imports without
  `_rete`/`_agami`/`_frodi`, and the five route sheets as plain import lists (m5).
- `tests/frontend/test_content_pages_browser_w3_f2.py` — the Latin heads guard visits the Arabic term page (M5).
- `tests/frontend/test_frontispiece_v515_c.py` — five sheet ceilings and six route totals added (m5).
- `tests/frontend/test_pages_browser_v522_p2.py` — six new cases, fr and ar (M1, M6, M7, M8, m2, m3).
- Not reformatted: `test_motion_v512_a_w2.py`, `test_interior_w3_f1.py` and `test_frontispiece_v515_c.py` were not
  `ruff format`-clean at `0554cde`; only this round's lines changed in them (formatting another lane's module is not
  this lane's). `ruff check` clean on every changed Python file.

### R2.5 Found by this round's own runs, fixed before the commit

- A multi-line `{# … #}` comment printed itself on Vivre's head (Django's short comment is one line): removed, the
  note in the template's `{% comment %}`.
- The keyhole's tone lost to the seal system's own rule (`fronte.css` after the page sheet, the same specificity): the
  page's rule names the mark (`.frodi__scudo .sigillo__mark .sg-t`).
- The first route split (AGAMI and the fraud page alone) put AGAMI 571 B over: gzip loses the shared dictionary across
  files, and the pages still carried the other pages' partials — Réseau's partial left the shared sheet too.
- The keyboard rule of the fraud page named a pseudo-element inside `:is()` (an invalid selector drops the rule): split.
- The new glossary letters test compared the scrubbed colour exactly; it allows the keyframe's few units now.
- On the Arabic page Vivre's action pointed up (the arrow glyph mirrors in a right-to-left page, then turned): it is
  the chevron, which points down in both scripts.
- The design-docs token guard (an app sheet names only tokens it, or a sheet imported before it, declares) found the
  route sheets' partials naming the seal system's `--light`, the stagger's `--sez-i`, the arrival's `--rise-wait` and
  the seal's `--sg-tone`: the light and the rank are declared at rest on their scopes (the seal system and the
  library's `.sez-seq` raise them), the tone is its value (0.14, a paper seat), and the head-sequence delays are fixed
  (160–600 ms) instead of following the arrival's veil.
- The fraud page's disclosure plate clipped its own question's focus ring (`overflow: clip`): the open tint now follows
  the plate's corners (`border-radius: inherit`) and nothing is clipped (`imp2_f_fraudes_fr_1440_focus.png`).

### R2.6 Requests to other lanes (§9.7: P2 edited none of their files)

- **S** — apply together, in one commit: `requests/indice.js.patch` (M2: open the named answer on a phone, follow
  `hashchange`), `requests/spia.js.patch` (M3: row stops, followed links current, the last part's rule held while a row
  holds the band) and P2's `requests/p2_with_lane_s.patch` (the phone's first paint showing the named answer, W1-C's
  same-document step, P2's tightened permalink test, the spy assertions). All four apply with `git apply -p1` on this
  round's tree; `imp2_probe2`/`imp2_probe3` ran them in the browser. If S cannot before P2's merge, the steward.
- **S** — `requests/mappa.js.patch` (m1, round 1's).
- **S** — `_reveal.css` M1 keys the head's hairline to `:has(+ .chapter)`: no V2 head draws it (the FAQ, the glossary,
  Vivre, Le projet, Réseau, Contact, AGAMI, Fraudes). Decide whether V2 heads keep it (`:has(+ .sez)`, over a rule of
  their own, since a V2 section has no chapter rule to settle into); the migrated test measures it where it stands.
- **S** — the contact head's address (`.fronte-azione__text`) breaks onto two lines at 360, fr and ar (QA_ROUND2's
  observation).
- **S / steward** — `tests/frontend/test_motion_v512_a_w2.py`, `test_interior_w3_f1.py` and
  `test_frontispiece_v515_c.py` are in lane S's family: this round changed one case of the first (M4, the lane's own
  defect), the second's interior list and the third's tables, each under the strict rule.
- **Steward** — ownership rows for the new files: `apps/cms/static/cms/{faq,lessico}.css`, `_faq-v2.css`,
  `_lessico-v2.css`, `apps/pages/static/pages/css/{rete,agami,frodi}.css`; the build's ten msgids (m6).

### R2.7 Runs (`test_ile_v5_l7`, one pytest at a time; a Chromium slot held for each browser run)

- **Non-browser, targeted** — the lane's apps (`apps/pages`, `apps/faq`, `apps/glossary`, `apps/living`, `apps/forum`,
  `apps/cms`), `tests/compliance`, `tests/i18n` and 31 modules of `tests/frontend` (the frontispiece budgets, W3-F1,
  W3-F2, design docs, CSS bundle, sezioni V5.22 S, chapter marks, icons, motion V5.12, rm parity, reduced motion,
  motion rules, script motion gate, loader rules, state chips, template comments, CSS and V5 tokens, mobile RTL, O14
  lint, layout, terminology, French typography, static assets, SVG, imagery V5.22 M, orientation W3-F1), in two runs:
  **557 passed** and **2 052 passed**; four failures — lane S's three, red on design-v5 `22b0ddd` too
  (`test_every_horizontal_shift_has_its_rtl_twin`, `test_l3_attaches_only_to_fragment_containers`,
  `test_data_register_is_written_by_the_partial_and_by_two_legends_only`) and this round's token guard (R2.5, fixed:
  the CSS guards again, **279 passed**, S's one). `tests/frontend/test_design_preview.py` whole: **314 passed** (its five browser tests in a lock slot).
- **Browser** (headless, a lock slot each): `test_pages_browser_v522_p2.py` **37 passed** (after the last CSS change);
  `test_motion_v512_a_w2.py` (the migrated test, both cases) with `test_content_pages_browser_w3_f2.py` **17 passed**;
  `test_browser_w1_c.py`, `test_browser_w1_b.py`, `test_browser_w3_f1.py`, `test_orientation_browser_w3_f1.py`,
  `tests/i18n/test_rtl_browser.py` **71 passed**; `test_mobile_rtl_w4_a.py`, `test_browser_contact_channels_v519.py`,
  `apps/pages/tests/test_browser.py`, `apps/portal/tests/test_browser.py`, `test_lume_v512_a.py`, `test_lume_v515_a.py`
  **84 passed**; after the last CSS changes, `test_browser_w3_f1.py`, `test_mobile_rtl_w4_a.py`, `test_rtl_browser.py`
  and `apps/pages/tests/test_browser.py` again **105 passed** — every module the reviewer listed in M4.
- **Headed checks** (chromium-1234): the permalink arrivals (`imp2_probe1`), the spy and indice patches by
  interception (`imp2_probe2`, `imp2_probe3`), the ten pages at 1440 and 390 in fr and ar under reduced motion — no
  overflow, one h1, no console error or failed request (`imp2_sweep1.json`) —, the changed sections' stills
  (`imp2_a_*` … `imp2_f_*`), axe 4.13 at rest on eight pages × fr/ar × 1440/390 plus the fraud page's disclosure open and
  address focused: **0 violations in 36 runs** (`imp2_axe1.json`); reduced motion: nothing running 2.5 s after load and
  no section state on seven pages × fr/ar × 1440/390; without script the FAQ's nine answers listed, the fraud page's
  disclosure opening natively, the term page's three related definitions (`imp2_rmnojs1.json`).
- `ruff check` clean on every changed Python file, `ruff format --check` clean on the lane's own modules (R2.4);
  `npm run build:css` current; every changed file LF.

### R2.8 Not done, or open

- M2 and M3 wait for lane S's modules (R2.6): a merge condition. Until then a phone's permalink lands on its folded
  question with nothing moving, and the glossary's rail lights a row's last letter while the register's letters light
  the whole row.
- m4 recorded as a deviation for the Director.
- The glossary family has 17 B left under its total (R2.3).

### R2.9 design-v5 moved during the round

design-v5 moved during the round: lane P1's merge (`dba97fa`) and the steward's record of it (`269cf39`, DL54-183),
both landed while this round's runs were under way. Files both touched: `locale/{it,en,ar,fr}/LC_MESSAGES/django.{po,mo}` (P1's five msgids and its
stale-removal pass against the build's ten), `tests/frontend/test_interior_w3_f1.py` (P1's sheet lists beside this
round's interior and route-sheet lists) and `tests/frontend/test_mobile_rtl_w4_a.py`. The branch is not merged with it
in this round (every run above is on `22b0ddd` + this round): the merge, the catalogue's union (P1's five msgids and
the build's ten) and the re-run on the merged tree are the next round's setup — or the steward's, before P2's merge.

## Final fix round (label v522-p2-fix, 2 November 2026)

After QA round 3 (`evidence/v522/p2/QA_ROUND3.md`: passed with merge conditions — 0 major in the lane's files, 6 minor;
MC-1…MC-3 in lane S's modules, which S2 applies; MC-4, MC-5 the steward's). Branch head before the round `5b87441`.
Database lane l7 (`test_ile_v5_l7`, one pytest at a time), lane server 8787 (dev settings, `ile_v5_l7`, reference date
3 October 2026, G3 open, the WhatsApp number read by the launcher from the preview's untracked `.env`). Headed
chromium-1234 for every visual check, the suites headless as designed, every Chromium run in a lock slot
(`.work/v522-p2-fix/logs/locks.log`). Evidence: `evidence/v522/p2/fix/` (`fix_before_*` the state at the merge,
`fix_after_*` the result, `fix_*.json` the measures). Tools: `.work/v522-p2-fix/tools/`. No file of another lane edited
(§9.7); lane S's modules untouched (S2 applies the three patches).

### F.1 design-v5 merged into the branch (MC-4, surfaced before the merge)

`f32fa07` merges design-v5 `269cf39` (lane P1's merge `dba97fa` and its record): two conflicts, both resolved as the
union of the two lanes.
- `locale/{fr,it,en,ar}/LC_MESSAGES/django.po`: both lanes had appended their block at the catalogue's end — lane P1's
  five msgids (carried by its merge) and this lane's ten (§7), each block whole with its msgstr, design-v5's first. The
  four `.mo` recompiled (`scripts/i18n_audit.py --compile`): 3 707 msgids, 100 % in it/en/ar/fr, no error. The five
  msgids the lane's sources no longer use stay for the steward's sync at merge (the audit lists them as harmless).
- `tests/frontend/test_interior_w3_f1.py`: the base's coarse-pointer loop had two rows and each lane took one out with
  its markup — this lane `.contact-address__link` (the address is the contact head's action), lane P1
  `.termes__list .tag` (the pathway terms are disclosures) —, each replacing it by a 44 px floor under every pointer.
  Both replacement blocks kept; the loop, left with no row, goes, with a note citing the strict rule (the invariants
  only grew stronger).
- `test_mobile_rtl_w4_a.py` merged cleanly. `npm run build` reproduces the committed dist on the merged tree;
  `manage.py check`, `makemigrations --check`, `ruff check .` clean. On the merged tree: the conflict modules and their
  neighbours (`test_interior_w3_f1`, `test_mobile_rtl_w4_a`, `test_css_bundle_is_current`, `test_frontispiece_v515_c`,
  `test_content_pages_w3_f2`, `tests/i18n` `test_page_integrity`, `test_ui_translations`) **326 passed**;
  `test_catalogues`, `test_locked_texts`, `test_rtl_static` **229 passed** and lane S's known red (`_sec-tracciato.css`).

### F.2 m1 — Vivre: the moment meets its band

The paper strip under the street frame was the moment's own bottom padding (96 px at 1440, 82 at 1024, 64 at 768 and
390). The moment now has no block padding and its ground is the band's stone (`templates/living/index.html`,
`_lessico-v2.css` §3): on a desktop the frame fills the section, so the frame's foot is the band's edge; below 64 rem
the lead's plate overlaps the frame's foot and stands on that stone, which runs on into «Pour s'installer». Measured
(`fix_before_look1.json` → `fix_final_look1.json`, fr/ar/it/en × 1440/1280/1024/768/390): gap 96/96/82/64/64 → **0**
at every width and language; the moment's ground = the band's (`rgb(236 235 230)`). Stills
`fix_{before,after}_vivre_{fr,ar}_{1440,390}_seam.jpg`, `fix_after_vivre_band_{fr,ar}_{768,390}.jpg`,
`fix_after_vivre_band_fr_360.jpg`, `fix_after_vivre_band_en_1024.jpg`.
Recorded choice: the library's «two grounds of the same kind never touch» is kept in spirit — the moment shows no ground
of its own on a desktop, and below 64 rem its ground IS the band's, so the two read as one composition, not two blocks.

### F.3 m2 — Glossaire: the card rows on subgrid

A card's term, definition and «Où le rencontrer» stand on its row's three shared lines (`grid-row: span 3;
grid-template-rows: subgrid`, `align-items: start`; the dove's `margin-block-start: auto` gone): in a row the definitions
start together and the rules and chips align on one line under the row's longest definition, and a card with fewer
chips keeps its room at its foot. Measured (`fix_before_look1.json` → `fix_final_look1.json`, the reviewer's measure:
the blank between a card's definition and its «Où le rencontrer»): the largest blank **154 → 96 px** at 1440, **115–118
→ 96** at 1280 (dichiarazione: its two-line definition beside nulla osta's five), **136–142 → 68 px** at 1024 and 768
(legalizzazione beside nulla osta), 12 px at 390 (one column) — the same in the four languages. What remains above a
rule is only the row's longest definition's excess (held: ≤ that excess + the 12 px gap), the rules and the
definitions' first lines aligned to the pixel. Stills `fix_{before,after}_glossaire_{fr,ar}_{1440,1024}_row.jpg`,
`fix_after_glossaire_{ar_1440,it_1280,fr_1024,en_768}.jpg`, the search's answers `fix_after_ricerca_*.jpg`, the term page
`fix_after_terme_*.jpg`. The two chip rules became one (the same values: the bytes).

### F.4 m6 — Forum: the desktop head's drawing anchored

On the twin the head's drawing moved 44 px in one throttled load (CLS 0.019). The cause, reproduced here: from 64 rem
the drawing was centred on the head's height (`inset-block: 0; margin-block: auto`), and that height grows after the
first paint — on the twin the document arrives in parts (the reviewer's load: the head's inner 354 px at the first
paint, 89 px short — the index's two last rows —, then 443), and a late face would do the same; and its seat was an
inline grid on a line box whose descent is the face's (440 px for a 432 px drawing in French, 444 in Arabic). With the
metric-matched fallbacks a swap of faces alone re-wraps nothing here (`fix_before_fallback.json`: fallback = web faces
at six widths, four languages). Now (`_forum.css` FO0): the drawing hangs from the title's line, a fixed 72 px from the
head's top, its seat a block (`display: grid`: the box is the drawing's 432 × 432 at 1440), and the head is at least as
tall as the drawing asks (72 + drawing + 48 px; at 1440 the French head 547 → 552 px, the Arabic 531 → 552). Measured
(`fix_final_look1.json`): the drawing's top 72 px at 1920/1440/1280/1024 in the four languages (it was 54/87/128 in
French, 44/80/134 in Arabic); the index's last rows taken out and put back move nothing of it (the new browser test). On
the compressed twin 8797, the reviewer's rig — desk 1440 × 900, network A, CPU × 4, cold —, 10 loads, fr and ar: the
drawing never moved vertically; in one load the head first painted 220 px of its content and grew to 443 px as the
document arrived, the drawing staying at its 193 px while every centred box moved 8 px sideways when the page's
scrollbar appeared (0.003); CLS 0.0095–0.0179 in French, 0.0176–0.0217 in Arabic, every other shift the letterhead's
menu and lock-up settling and the Lume veil (the chrome's, preserved) — `fix_forum_cls_twin.json`; it was 0.075 in one
of five loads before. Stills `fix_{before,after}_forum_{fr,ar}_1440_head.jpg`, `fix_after_forum_{fr,ar}_1024.jpg`,
`fix_after_forum_fr_1280.jpg`, `fix_after_forum_fr_1920.jpg`, `fix_after_forum_ar_1440.jpg`.

### F.5 m3 — the route sheets: recorded deviation, with the twin measurements (for the Director)

**The deviation.** §7.2 allows «+1 CSS (`fronte.css`)» on three page types (the two form pages and the glossary term
page). Round 2's route sheets (R2.3, QA_ROUND2 m5) add one more render-blocking stylesheet on seven page types — the
FAQ (`cms/faq.css`), the Glossaire, the term page and Vivre (`cms/lessico.css`), Réseau (`pages/css/rete.css`), AGAMI
(`agami.css`) and Attention aux fraudes (`frodi.css`): five blocking sheets on a phone instead of four (six instead of
five from 64 rem, where `core/portico.css` applies). Why: the owner's V5.22 standing constraint — page-only sheets and
route-specific bundles with their own recorded budgets —, and the reading pages' shared sheet stood at its ceiling.

**Measured for the Director** (`fix_perf_ab_{fr,ar}*.json`, tool `.work/v522-p2-fix/tools/perf_ab.py`): two compressed,
DEBUG-off twins of this round's tree, built as the reviewer's 8797 — **A** the branch (8797) and **B** the same tree
folded (8798: each route sheet's partials appended to its shared sheet, after its rules and before `fronte.css`, so the
cascade is the same, and the seven links removed; built in a scratch copy outside the repository,
`.work/v522-p2-fix/twin/make_fold.py`) —, on the reviewer's rig (network A: 150 ms, 1.6 Mbit/s; CPU × 4; phone
412 × 823 @1.75; cold loads), A and B interleaved, two passes, **n = 10 a variant, a page and a language**:

| Page | Blocking A / B | FCP fr A − B | FCP ar A − B | LCP fr A − B | LCP ar A − B |
|---|---|---|---|---|---|
| FAQ | 5 / 4 | −56 ms | +34 | +26 | +50 |
| Glossaire | 5 / 4 | +10 | +28 | +238 | +132 |
| Term page | 5 / 4 | +42 | −18 | +222 | −180 |
| Vivre | 5 / 4 | +10 | −44 | +68 | −8 |
| Réseau | 5 / 4 | 0 | −32 | −30 | −108 |
| AGAMI | 5 / 4 | −6 | −8 | −22 | −162 |
| Fraudes | 5 / 4 | +18 | −6 | +146 | +54 |
| Contact (control: 4 / 4) | 4 / 4 | −8 | −20 | +18 | −30 |

- FCP: **−2 ms** on average over the fourteen page-languages (−56 … +42 ms); the last blocking stylesheet's response
  ends **0 ms** later on average (−44 … +26); LCP **+30 ms** on average (−180 … +238 ms). No page's difference is
  significant (Mann–Whitney on its 10 + 10 runs: every LCP p ≥ 0.05; the two FCPs under 0.05 — Vivre and Réseau in
  Arabic — favour the route sheets): the extra request costs nothing measurable on this rig, HTTP/1.1's six connections
  fetching it beside the others.
- Bytes: the same on both sides for these pages (±1 kB). What folding would cost instead: `cms/lettura.css` 6 509 →
  9 232 B gzip (over its 9 216 ceiling) and `pages/css/interior.css` 8 799 → 11 142 B, downloaded by every reading and
  interior page that draws none of these compositions (the news, the partners, the legal pages, the forms' pages,
  Contact, Le projet).
- The machine was loaded during these runs (other sessions' processes; three runaway `find /` searches held about three
  cores from 13:13): the absolute values are above the reviewer's — some phone LCP medians reach 2.4–2.6 s in both
  variants. For §5.3 the reviewer's twin stands (QA_ROUND3, `qa3/v/perf_twin.json`: phone LCP medians 1 260–2 256 ms,
  CLS 0); this comparison is the interleaved A − B difference.
- Recommendation: keep the route sheets and record the deviation; S-close's ratchet can fold one back where a page's
  total allows it.
- Observation for lane S: in 2 of 11 throttled AGAMI loads on A (0 of 11 on B) the head's decorative motif
  (`.fronte__motif`, `_fronte.css`: `inset-block: 0; block-size: 100%`) moved 128 px as the head grew with the
  arriving document (one shift of 0.042, under the 0.1 gate; `fix_cls_fr_agami_phone.json`) — the Forum drawing's
  mechanism (F.4); hung from the head's top it would hold.

### F.6 Found by this round's own sweep, fixed before the commit

- **The register overflowed a narrow phone.** Below about 400 px the register's one column took its widest card's
  min-content — «Ricongiungimento» at the band size beside a letter's room —, wider than the band: at 320 px the cards
  ran 45 px past the viewport's edge and the drawn letter was cut; at 360 px with a desktop scrollbar (345 px of
  viewport) the Arabic cards started 6 px off-screen, and the phone letter band followed the column out
  (`fix_before_narrow_glossaire_{fr,ar}_*.jpg`, `fix_azband_*.png`). Now the column is the band's width
  (`minmax(0, 1fr)`), the letter's room gives up to 13 px of its margin under 800 px (`min(var(--s-6), 3vw)`), so a
  360 px phone holds «Ricongiungimento» whole beside its R in both scripts, and a word longer than a 320 px line breaks
  inside its card (`overflow-wrap: anywhere`), never under its letter. Every card inside the viewport at 320/360/375/390
  in the four languages; the letter band inside it (`fix_after_narrow_glossaire_*`, `fix_after_phone_glossaire_*`).
  Held by `test_the_register_s_cards_stay_inside_a_narrow_phone` (320, 360, 375; fr, ar).

### F.7 Tests

- **New** (the lane's own module `tests/frontend/test_pages_browser_v522_p2.py`, fr and ar): `test_vivre_s_frame_meets_its_band`
  (1440, 1024, 768, 390: no gap, the plate in the frame from 64 rem, the moment's ground the band's);
  `test_a_glossary_row_holds_its_cards_parts_on_shared_lines` (1440, 1280, 1024, 768: definitions and rules aligned in
  each row, the blank above a rule never more than the row's definition excess + 12 px);
  `test_the_forum_s_drawing_hangs_from_the_title_s_line` (1920, 1440, 1280, 1024: the drawing's top on the title's,
  its box its own width, late rows in the head move nothing, the drawing never cut by the head's edge);
  `test_the_register_s_cards_stay_inside_a_narrow_phone` (F.6). Each fails on the round's starting state and passes
  with it: the first three 6 failed with the round's sheets and template stashed, the fourth 2 failed with the
  glossary's sheet stashed (fr and ar at 320 px).
- **Added to** `apps/pages/tests/test_interior_v522.py::test_living_opens_on_its_panorama_and_closes_on_what_exists`: the
  moment's ground is the band's and nothing stands between them (QA_ROUND3 m1, a stronger invariant).
- **Changed under the strict rule:** only the merge's `test_interior_w3_f1.py` (F.1).

**Runs** (`test_ile_v5_l7`, one pytest at a time; a lock slot for each browser run):
- Browser: the lane's module `test_pages_browser_v522_p2.py` **45 passed** (its 37 and the 8 new cases);
  `test_content_pages_browser_w3_f2`, `tests/i18n/test_rtl_browser`, `test_mobile_rtl_w4_a` **68 passed**;
  `test_browser_w3_f1`, `test_motion_v512_a_w2`, `apps/pages/tests/test_browser`, `test_browser_w2_c2`,
  `test_lume_v512_a` **86 passed**; `test_design_preview`'s browser cases **17 passed** — every browser module that
  visits the three changed pages.
- Non-browser, what this round touches or what guards it: `apps/pages/tests/test_interior_v522.py`, `apps/glossary`,
  `apps/living`, `apps/forum`, 26 modules of `tests/frontend` (design docs and token vocabulary, the CSS bundle, token
  existence, the frontispiece budgets, W3-F1, W3-F2, sezioni V5.22 S, template comments, static assets and pipeline, O14
  lint, layout, motion rules, reduced motion, the rm flag, the script motion gate, the V4 and V5 tokens, the loader
  rules, the state chips, mobile RTL, French typography, forced colours, SVG, chapter marks, icons), `tests/i18n`
  (RTL static, page integrity, UI translations, catalogues) and `tests/compliance`: **2 280 passed, 4 failed** — the
  four red guards of design-v5 (F.9).
- With the configured number and the private sentinel table: `test_contact_channels_v519.py` and
  `tests/security/test_confidential_material.py` **72 passed**, no skip.
- F.1's runs on the merged tree; after the last change `npm run build` reproduces the committed dist, `manage.py
  check`, `makemigrations --check` and `ruff check .` are clean, `ruff format --check` clean on the two changed test
  modules, every changed file LF, no telephone-number digit run in the diff.
- The reviewer's broad non-browser set (`apps/{pages,faq,glossary,living,forum,cms}`, `tests/compliance`, `tests/i18n`,
  `tests/frontend`) was started and stopped at 10 % (all passed so far) when the machine's load made it a four-hour
  run; the curated set above stands for it.

### F.8 Budgets (gzip -9, the tests' method; `main.css` untouched, 32 718)

| Sheet / page | Round 2 | Final | Ceiling |
|---|---|---|---|
| `cms/lessico.css` | 2 336 | 2 356 | 2 560 |
| `forum/forum.css` | 7 336 | 7 353 | 8 192 |
| `/fr/glossaire/`, the term page, `/fr/vivre-en-italie/` | 54 246 | 54 266 | 54 272 |
| `/fr/forum/` | 46 596 | 46 613 | 54 272 |

Every other sheet and page as in R2.3. The glossary family has 6 B left: the next rule there needs a saving first
(S-close's ratchet, or a Vivre-only sheet).

### F.9 Not done, or open

- MC-1…MC-3 are lane S's modules (S2 applies `indice.js`, `spia.js`, `mappa.js` with P2's half); MC-5 the steward's
  (ownership rows for the route sheets and the cited slices). The branch is not mergeable alone (QA_ROUND3).
- design-v5's four red guards stay red on this branch, all in lane S's files (S2 fixes them in the product):
  `test_every_horizontal_shift_has_its_rtl_twin` (`_sec-tracciato.css`), `test_l3_attaches_only_to_fragment_containers`
  (`components/sezioni/mappa.html`), `test_data_register_is_written_by_the_partial_and_by_two_legends_only` (the
  library's templates) and `test_a_tag_is_a_term_and_carries_neither_a_register_nor_a_mark` (red since P1's
  recomposition). On this branch they fail exactly as on design-v5 (F.7's curated run). One of them reaches this lane's
  files once S2's fix lands: S2 renames the library's bare register marker `data-register` → `data-registro` (the chip's
  valued `data-register` stays the chip partial's), in lane S's partials and lane P1's templates; this lane's three
  templates still write the bare marker — `templates/forum/partials/presentation.html` (the Forum's nine actors),
  `pages/partials/fronte/_rete_pannelli.html` (the map's entries), `pages/partials/projet/_figura.html` (the story's
  nodes) — with the lane's assertions on it (`apps/pages/tests/test_interior_v522.py` ×2,
  `apps/forum/tests/test_forum_v522.py` ×1). Not renamed here: on this branch the library and the shared register
  count (`test_interior_w3_f1.py`, lane S's) still read `data-register`, and S2's convention is not on design-v5 yet. The
  rename is mechanical and must go with S2's in the same integration (P2 on the branch as soon as S2 is on design-v5, or
  the steward at P2's merge), or the data-register guard stays red on these three files.
- m4 (ownership slices) and m5 (the request patch's line endings) are the steward's and S2's; nothing of them in this
  round's diff.
- The machine during this round: three `find /` searches started by other sessions at 13:13–13:20 held about three
  cores for the whole afternoon, and the system volume filled to 0 bytes for about a minute at 13:33 (it recovered by
  itself; this round's files were checked intact after it — the test module re-parsed, the bundles rebuilt byte for
  byte); a browser run in that minute errored at its setup and passed when re-run. One headless probe (a computed-style
  read of the Forum head, seconds) ran outside a lock slot at 13:23; every other Chromium run held a slot
  (`logs/locks.log`: 37 sessions, the longest 11 min 25 s, each released).

## Final improve round (label v522-p2-final-improve, 2–3 November 2026)

After the final review (`evidence/v522/finish/v522-p2-final-qa1.md`: **not passed** — 1 major, the integration gate of
§9.9 item 7, and 6 minor; the design passed, every owned page ≥ 4 on the six dimensions). Branch head before the round
`53c2996`. Database lane l7 (the test databases `test_ile_v5_l7`, `…_l7f`, `…_l7g`, `…_l7h`, one pytest per database),
lane server 8787 (dev settings, `ile_v5_l7`, reference date 3 October 2026, G3 open, the WhatsApp number read by the
launcher from the preview's untracked `.env`, never printed). Headed chromium-1234 for every visual check, the suites
headless as designed, every Chromium run in a lock slot (`.work/v522-p2-final-improve/logs/locks.log`). Evidence:
`evidence/v522/p2/final/` (`before_*` the merged branch before the fixes, `after_*` / `final_*` the result). Tools and
raw data: `.work/v522-p2-final-improve/` (`tools/`, `data/`, `logs/`). No file of another lane edited (§9.7) but the
one cited slice MC-1 asks of this lane in W1-C's browser module (`tests/frontend/test_browser_w1_c.py`, FI.2 — for the
steward's MC-5 rows); lane S's modules (`sezioni/*.js`, `_sezioni.css`, `_reveal.css`, `rise.js`, the shared guards)
untouched.

### FI.1 design-v5 merged into the branch

`b995367` merges design-v5 `28fa9fa` (lane S's follow-up `v522/s2` and its record, DL54-184) with `--no-ff`: no conflict
(`git merge-tree 53c2996 28fa9fa` → tree `53d5c2c`, as the final review found). `npm run build` rebuilds the four dist
sheets that bundle lane S's changed partials — `cms/faq.css`, `cms/lettura.css`, `forum/forum.css`,
`pages/css/interior.css` — carried in the merge commit, so the merged tree holds its own build; two builds identical (77
dist files, every hash equal); `manage.py check`, `makemigrations --check` and `ruff check .` clean.

### FI.2 M1 — the integration gate (§9.9 item 7)

- **The library's register marker.** `v522/s2` retired the bare `data-register` (the chip's attribute) for the
  library's own `data-registro`; this lane's three templates still wrote the old marker. The S2 review's patch
  (`.work/v522-s2-qa1/trees/p2_data_registro.lf.patch`, applied with `git apply --whitespace=error`): one attribute token
  each in `templates/forum/partials/presentation.html` (the Forum's nine actors), `pages/partials/fronte/_rete_pannelli.html`
  (the map's entries), `pages/partials/projet/_figura.html` (the story's nodes), and the lane's three test lines that
  read it (`apps/forum/tests/test_forum_v522.py`, `apps/pages/tests/test_interior_v522.py` ×2 — the same invariant on the
  library's marker). No visible change (the only rules that read the old marker are the chip's token re-pointings,
  which these lists never drew with). Guard (c)
  `test_data_register_is_written_by_the_partial_and_by_two_legends_only` green again, and the three icon-count cases of
  `test_interior_w3_f1.py::test_one_primary_action_and_at_most_six_icons_in_the_body` (`/fr/forum/`, `/fr/le-projet/`,
  `/fr/reseau/`: 9, 17 and 16 body icons read as loose) green — the readers see the registers again.
- **MC-1's P2 half** (`p2_with_lane_s.lf.patch`, `--whitespace=error`):
  - `apps/cms/static/cms/_faq-v2.css`: below 64 rem the explorer's first paint folds every answer **but the one the
    address names** (`.indice__pannello:not(:target) .indice__corpo`), which `sezioni/indice.js` now opens at arrival
    (lane S's MC-1, `v522/s2`); the rule's comment says so;
  - `tests/frontend/test_browser_w1_c.py::test_a_link_to_an_faq_row_opens_it`: W1-C's same-document step restored —
    the V5.22 build had to drop it «until `sezioni/indice.js` followed `hashchange`», which it does since `v522/s2`
    (V5.20 strict rule: the reason for the removal is gone, the invariant is back; cited in the test) — and, since the
    step names a third answer, the explorer's floor of answers 2 → 3 (stronger);
  - `tests/frontend/test_pages_browser_v522_p2.py`: the permalink test tightened below 64 rem («its answer open,
    alone, one button expanded» in place of «no other answer shown»), and MC-2's
    `test_the_spy_lights_each_letter_followed_and_each_section_read` added. Its Forum half now counts **the sommaire's
    own links** — every entry lit, at least five — instead of a constant 5 (the S2 review's m1: in the test database the
    event is ahead, so the sommaire lists seven entries, the programme and the registration with the five sections, and
    all seven light).
- `npm run build`: `cms/faq.css` 1 929 → 1 935 B gzip -9.

### FI.3 m2 — AGAMI's identity band plays its signature (§3.17 AG-1)

The band stands in view at load at 1440 and 390, in French and in Arabic, so the section runtime writes it no state and
drew it at rest: its specified signature — the plate revealed from the reading edge (MASK, 900 ms), the colonnade's lines
drawing — never played (measured: no animation on the plate, the colonnade or the connector through the first 2.4 s;
`data/agami_motion_before.json`). Now (`apps/pages/static/pages/css/_agami.css`), in view at load, the band plays it in the
head's own sequence, as the fraud page's sill and shield do: the plate's mask from 360 ms (900 ms, `--ease-enter`), the
colonnade's stroke from 680 ms (900 ms, `--ease-sine`; 320 ms after the mask, as the runtime's «in» state delays it), the
connector into the text column's foundation line from 1.56 s on a desktop; below the fold the runtime plays the same verbs
on its trigger, as before. Keyed like every load sequence of the lane: `:root.js:not(.rm):not([data-input="key"])`,
`.agami-identita:not([data-sec-state])`, inside `prefers-reduced-motion: no-preference`, fill `backwards` (nothing left
running; the keyboard, reduced motion and no-JS see the drawing at rest).
- The load made the draw's direction visible: on the Arabic page the lines ran from the far edge. The portico is
  symmetric about its middle (its crop centred, `xMid`), so it is now **drawn mirrored on the Arabic page**
  (`[dir="rtl"] .colonnato { scale: -1 1 }`): the same drawing at rest — 1 pixel of 207 693 differs at 1440, 0 of
  69 498 at 390, the mirror on and off under reduced motion (`tools/agami_rtl.py`) — and its lines draw from the reading
  edge, as the plate opens from it.
- Measured (`data/agami_motion_after.json`; stills `final_agami_{fr,ar}_{1440,390}_load_{500,900,1400,2600}ms.jpg`,
  `final_agami_ar_1440_load_sill_drawing.jpg`, `final_agami_ar_{1440,390}_rest_mirrored.png`): `sez-mask` and
  `sez-stroke` run on the band at 1440 and 390, fr and ar, `sez-draw` on the connector at 1440; under reduced motion 0
  animation in the band.

### FI.4 m3 — the words of two V2 disclosures never wait

AGAMI's question row (`#agami-faq`) and the term page's related terms are rows of the system's accordion, and
`static/js/src/rise.js` (lane S's) still holds every `.accordion` row that starts below the fold (`data-rise=""`: opacity
0, 18 px low, until it enters) — inside two V2 sections, against §1 rule 3 and the owner's §17. Measured before
(`data/agami_motion_before.json`): AGAMI's row held at opacity 0 at 1440 and 390 (fr, ar), the term page's rows at 390.
P2 cannot change the runtime's groups (§9.7), and `data-stagger` (the runtime's «own sequence») would have given these
rows the head's rise at load instead — a translateY + opacity again. So in these two sections a held row simply stands at
rest: `.agami-identita .accordion > [data-rise]` (`_agami.css`) and `.scheda .accordion > [data-rise]`
(`_lessico-v2.css`) set `opacity: 1; translate: none` — specificity (0,3,0) over the hold's (0,2,1); the runtime still
marks and releases the rows, nothing moves. The bands' motion stays their own (AGAMI: the plate, the colonnade, the
connector; the term page: the plate's depth, the hairlines' draw). S-close's removal of the legacy rise makes both rules
moot. Measured after (`data/agami_motion_after.json`): the rows held by the runtime at opacity 1 from the first frame.
The FAQ's search results (a plain `.sez` list, not a V2 pattern section) keep the legacy rise, as every plain list does
until S-close.

### FI.5 m1 — the glossary rail under a resting pointer

`sezioni/spia.js` (lane S's) makes one stop of the parts whose rendered tops are under 2 px apart, and the library's plate
lifts exactly 2 px under the hand (`.sez-plate:has(.sez-stretch):hover`), so in a read-through with the pointer resting on
the register — how a mouse reads — the hovered card left its row and that row's first letters were never current.
Measured before on the merged branch (`tools/spyhover.py`, the reviewer's method; `data/spyhover_before.json`): with the
pointer at the register's end side C, L, P, Q never lit at 1440 (fr and ar), P, R at 768 (fr) and L, P, R (ar); in the
margin all eight. The root (grouping a row by its layout position, `offsetTop` or the grid row) is lane S's — request
below. Lane P2's part, the reviewer's alternative: **a dictionary card answers the hand in place** — its letter fills,
its rule runs to its full height, its shadow deepens (the plate's pre-painted layer) — without the library's 2 px lift
(`.lessico__carta.sez-plate:hover`, in one rule with FI.4's term-page rows, `opacity: 1; translate: none`;
`_lessico-v2.css`, after the library in the cascade; the Vivre installer's cards are the same component).
Measured after (`data/spyhover_after.json`): all eight letters lit at 1440, 1024 and 768, fr and ar, the pointer on the
register's end side, its start side or the margin; the rows read as one stop (C·D, L·N, P·Q·R, V at 1440). Still
`final_glossaire_{fr,ar}_1440_rail_PQR_pointer_on_register.jpg`.

### FI.6 m4 — a FAQ arrival at 768: the cause, recorded

With MC-1's P2 half the explorer's first paint shows the address's answer, and most arrivals at 768 hold still. A residue
remains, and it is not the explorer's: traced in headed Chromium (`tools/faqtrace.py`, `data/faqtrace_{a,b}.json`), in the
loads that shift, Chromium draws one frame at `readyState` «interactive» — the parser done, the deferred scripts not yet
run — in which `:target` matches **nothing yet** (the element exists; Chromium sets the CSS target only when the parser's
end processes the fragment, after the deferred scripts) and the page still at the top: on a 768 × 1024 screen the first
three questions stand in that first viewport (the named panel at y 645–815), so the named answer appears a frame later
and pushes the rows under it (fr «visas» 0.055, «agence» 0.034, «pré-évaluation» 0.027; ar 0.052, 0.031, 0.024), in about
two loads in five (18 of 46 traced arrivals of those three anchors at 768). The two other anchors at 768, and all five at
1440, 1024 and 390 in French and Arabic (30 of 30), arrive at ≤ 0.0001 (`data/faq768_{a,widths}.json`). No CSS hook
knows the address before `:target` does; holding the explorer until the module runs would make its words wait, and a
render-blocking script is outside the lane's brief (no new JS; §7.2). Inside the 0.1 gate; recorded for the Director.

### FI.7 Not done here (other lanes', the steward's, the Director's)

- **m6 (lane S, S-close):** `test_interior_w3_f1.py:335` and `test_orientation_w3_f1.py:118` read
  `data-registr(?:o|er)` — `data-registro` and «data-registrer», never `data-register` — while their comment and the S2
  notes say they read both; `data-regist(?:ro|er)` is the intent (or the comment narrowed). Lane S's modules: untouched.
- **m1's root (lane S, S-close):** `spia.js` to group a row by its parts' layout position, not their transformed boxes —
  then the lexicon's cards may take the library's lift back.
- **m5:** no action asked (axe `target-size` «partially obscured» on the term page at 1024 in one interactive state).
- **The steward, at P2's merge:** MC-5 (the family `v522-p2`: `check_ownership` reports «unknown family 'v522-p2'»; P2's
  route sheets and partials, and the cited slices of S-family test modules — `test_browser_w1_c.py` gains this round's
  restored step); the catalogue pass for the lane's ten msgids (no new string this round: the catalogue +0 −0) and the
  five it no longer uses; the preview label «Page Composition V2».
- **S2's request 8.3, third bullet** (`_projet.css` `html[data-input="key"] :is(.projet-racconto *, …)`, a universal
  subject the first key restyles the whole document for): not in the final review's findings; the story's transitioning
  parts must be named one by one and measured on the twins — left for the lane's next pass or S-close, recorded.
- **The Director:** FI.6 (m4's residue); round 3's m3 (the route sheets' extra request, NOTES F.5) unchanged.

### FI.8 Budgets (gzip -9, the tests' method; `main.css` 32 716, untouched)

| Sheet / page | Final review (T1/T2) | This round | Ceiling |
|---|---|---|---|
| `cms/faq.css` | 1 929 / 1 935 | 1 935 | 2 048 |
| `cms/lettura.css` | 6 529 | **6 512** | 9 216 |
| `cms/lessico.css` | 2 356 | 2 384 | 2 560 |
| `pages/css/agami.css` | 1 667 | 1 760 | 2 048 |
| `/fr/faq/` | 53 834 / 53 840 | 53 823 | 54 272 |
| `/fr/glossaire/`, the term page, `/fr/vivre-en-italie/` | 54 261 | **54 272** | 54 272 |
| `/fr/agami/` | 55 870 | 55 963 | 56 320 |

Every other sheet and page as the final review measured them (`interior.css` 8 827, `forum.css` 7 369, `rete.css`
1 817, `frodi.css` 1 200; Réseau 56 020, Fraudes 55 403, Le projet and Contact 54 203, Forum 46 604). The glossary family
had 11 B. m1 and m3 there are one rule (the same values); `lessico.css` grows 28 B net of two savings in it — Vivre's two
adjacent reduced-motion blocks made one, the seal's tone delay written whole (`1360ms`: the minifier leaves
`calc(.16s + 1.2s)` unfolded) — and `lettura.css` gives back 17 B, a dead rule of the reading pages' shared partial
(`v5/_lettura.css` `.lettura .page-header__recipients`, written by no template, Python or script since P1 re-composed
the collaboration head): the family +11 B — **at its ceiling, 0 B left**; the next rule there needs a saving first
(S-close's ratchet, or a Vivre-only sheet).

### FI.9 Tests

- **Restored / tightened under the V5.20 strict rule** (each change cited in its test): `test_browser_w1_c.py`
  (W1-C's same-document step back, the answer floor 3 — stronger); `test_pages_browser_v522_p2.py` (the permalink test
  below 64 rem: one answer shown and open, one button expanded — stronger; the spy test compares with the sommaire's own
  links — every entry lit, a floor of five — instead of a constant); the lane's own `test_interior_v522.py` and
  `test_forum_v522.py` read the library's `data-registro` (the same invariant on the renamed marker).
- **New** (the lane's own module `tests/frontend/test_pages_browser_v522_p2.py`, fr and ar):
  `test_a_card_under_the_hand_keeps_its_row_and_the_rail_lights_every_letter` (1440, 768: the hovered card on its row;
  a read-through with the pointer on the register lights every letter of the rail),
  `test_agami_s_identity_band_plays_its_signature_in_view_at_load` (1440, 390: no state written, `sez-mask` and
  `sez-stroke` run and end, the Arabic portico mirrored; under reduced motion nothing runs),
  `test_a_v2_disclosure_s_rows_never_wait_for_the_legacy_rise` (AGAMI and the term page, 1440 and 390: every row at
  opacity 1, in place, the rise holding at least one at 390). **Each fails on the round's starting sheets** — run with
  `HEAD`'s `cms/lessico.css` and `pages/css/agami.css` swapped in: 6 failed (the card 2 px up, no animation in the band,
  the row at opacity 0, 18 px low) — and passes with them.

**Runs** (one pytest per test database; the browser runs headless as the suites launch, each inside a lock slot):
- The guards and their readers on the merged tree with M1's patches, before the minors (`test_state_chips_carry_a_register`,
  `test_interior_w3_f1`, `test_orientation_w3_f1`, `test_o14_lint`, the lane's `test_interior_v522` and
  `test_forum_v522`; `test_ile_v5_l7`): **374 passed** — guard (c) and the three icon-count cases green.
- Non-browser on the final tree, with the configured WhatsApp number and the private sentinel table (read in process,
  never printed): `tests/frontend` (`…_l7f`) **2 681 passed, 2 xfailed** (the two recorded debts), 0 failed, 0 skipped;
  `tests/i18n`, `tests/compliance`, `tests/security/test_confidential_material.py`, `apps/{pages,faq,glossary,living,forum,cms}`
  (`…_l7g`) **1 388 passed**, 0 skipped — **4 069 passed** in all, the budgets (`test_frontispiece_v515_c`: every route
  inside its total, the glossary family's three at 54 272 / 54 272), the CSS bundle's currency, the RTL, motion,
  reduced-motion and modality guards among them.
- Browser (`…_l7h`, headless as the suites launch, each batch inside a lock slot): batch 1 — `test_pages_browser_v522_p2`
  (54 cases), `test_browser_w1_c`, `test_browser_contact_channels_v519` (the configured number) — **68 passed** (16 min);
  batch 2 — `test_motion_v512_a_w2`, `tests/i18n/test_rtl_browser`, `test_sezioni_browser_v522_s2` (lane S's checks, on the
  merged pages), `test_content_pages_browser_w3_f2` — **56 passed**; batch 3 — `test_mobile_rtl_w4_a`,
  `apps/pages/tests/test_browser`, `test_browser_w3_f1`, `test_orientation_browser_w3_f1` — **93 passed**. **217 passed,
  0 failed**, every browser module that visits the lane's pages; W1-C's restored step and the spy test (all seven
  sommaire entries lit) among them.
- Headed sweep (`tools/sweep.py`, `data/sweep.json`): the ten pages in fr/it/en/ar at 1440, 1024, 768, 390 and in fr/ar
  at 1280, 430, 375, 360 — 240 runs under reduced motion: no horizontal scroll, one h1, 0 console error, 0 failed
  request. The tool's 14 flags are all Le projet's full-bleed panorama from 768 up: its frame stands 8 px past the
  client edges, under the scrollbar, clipped by its own section, and the page never scrolls sideways
  (`tools/pano.py`) — as designed, unchanged this round. axe 4.13 at rest on AGAMI, the glossary, the term page and the
  FAQ (fr/ar × 1440/390): **0 violations in 16 runs**. Stills: `final_*` (the band's load sequence, the Arabic
  portico, the rail under a resting pointer, the term page's rows on a phone as they enter and settled, a FAQ permalink
  open at 390 and 768).
- `npm run build` twice: 77 dist files, every hash equal; `manage.py check`, `makemigrations --check`, `ruff check .`
  clean; `ruff format --check` clean on the lane's changed modules (`test_browser_w1_c.py`, W1-C's, was not
  format-clean before the round — two long asserts outside the restored lines, left as they were); `git diff --check`
  clean; every changed file LF; no telephone-number digit run in the round's diff (the configured number searched in
  process: 0).
- Lock sessions (`logs/locks.log`): A and B, 23:00–00:27, the longest 16 min 28 s (browser batch 1), each released; the
  other slot often lane H's; no slot taken over.

### FI.10 Not done, or open

- FI.6 (m4's residue, recorded for the Director), FI.7 (other lanes', the steward's).
- The branch is mergeable on its own now: M1 fixed, `v522/s2` merged, the dist rebuilt; MC-5 and the catalogue pass are
  the steward's at the merge.
