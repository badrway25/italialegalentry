# V5.12 — Lane B, wave W1 (label v512-b-w1): the chapter mark and the company's needs

28 Oct 2026. Branch `v512-b-w1`, from design-v5 `e047fae`. Scope, exactly the W1 row of DECISIONS.md «Waves» for B:
the `CHAPTER` registry and the end of the `ile-steps` misuse, with **existing symbols only**; `wrench` →
`briefcase-business`, vendored first. Nothing of W2 (the twelve new symbols, the sprite split, the field system, the
account shell) is in this branch.

## 1. What changed

| Where | Change |
|---|---|
| `apps/core/icons.py` | New concept domain **`CHAPTER`** (17 concepts → existing symbols) and **`CHAPTER_OF`** (28 section anchors → concept), plus `chapter_glyph(key)`. `CHAPTER` is registered in `DOMAINS`. `wrench` left the registry; **`briefcase-business`** (Lucide 1.48.0, ISC, floor 20, the seat of the wrench) took its place in `SYMBOLS`, in the sheet's group and in `COMPANY_NAV["needs"]`. New twin pair `{briefcase, briefcase-business}`. `SHARED` extended and reworded for the symbols a chapter head now shares with another map (`institution`, `briefcase`, `briefcase-business`, `ile-arch`, and the wording of `building`, `university`, `book-open`, `stamp`, `signpost`, `compass`, `document`). |
| `apps/core/templatetags/ile_core.py` | New tag **`{% chapter_mark key %}`**: the glyph of the section's concept (key = the anchor, or a concept), or nothing. Decorative (`aria-hidden`), through `svg_icon`, so the closed flip list still applies (`signpost` mirrors in AR). |
| `templates/pages/partials/_chapter_head.html`, `_section_header.html` | The hard-wired `svg_icon "ile-steps"` is replaced by `{% chapter_mark chapter_concept|default:title_id %}`. New optional argument `chapter_concept` for a head whose anchor does not say its concept. **No call site of lane C's templates was edited**: the 73 includes keep their `title_id`, and the registry reads it. |
| 16 literal sites (`community/{index,room,discussion}`, `enquiries/{contact,company_needs,collaboration_proposal}`, `faq/index` ×2, `living/topic`, `news/{detail,_newsletter}`, `pages/home/_pilot`, `partners/index`) | `svg_icon "ile-steps" "icon chapter__mark"` → `{% chapter_mark "<anchor or concept>" %}`. The collaboration form draws `institution` or `university` by its kind; a partners' group draws its audience by `PartnerKind`; the FAQ groups draw `circle-help`. |
| `static/icons/src/briefcase-business.svg` (new), `static/icons/src/wrench.svg` (deleted), `static/img/icons.svg` (rebuilt), `docs/design/DESIGN_SYSTEM_2026.md` (the generated icon list) | Built by `scripts/build_icons.py`; `--check` is current. The source carries the 12 % tone on the case and the ILE square dot (the donor's `h.01` dot, as in `ellipsis-vertical`). |
| `static/icons/LICENSE-lucide.txt` (new) | The package's `LICENSE` byte for byte (ISC + the Feather MIT notice): vendored geometry keeps its licence file next to the sources. |
| `docs/design-v5/ICON_LICENSES.md` | The `wrench` row replaced by `briefcase-business`; §3.3 names the licence file; §4 records the swap. |
| `apps/companies/services.py` | Comment only (the needs' glyph). |

### The chapter map (what each head now says)

| Concept | Symbol | Anchors |
|---|---|---|
| orientation | `compass` | home «Comment fonctionne l'orientation», orientation start «Comment se déroule le questionnaire», every closing «Orientation» chapter |
| pathways | `signpost` | home «Parcours réguliers», /parcours/ list, orientation result, fraud page «S'informer sur les voies régulières» |
| documents | `document` | pathway sheet «Documentation généralement requise» |
| authorities | `stamp` | pathway sheet «Autorités», /diplomes-et-titres/ «Qui décide ?» |
| training | `book-open` | orientation result «Formation avant le départ» (→ `presentation` in W2) |
| reserved-area | `ile-key` | «Dans l'Espace Personnes» |
| email | `at-sign` | /contact/ «Par e-mail», /agami/ «Identification et contact», the newsletter |
| news | `newspaper` | home news, «À lire aussi» |
| faq | `circle-help` | each FAQ group, the FAQ search results |
| company-needs | `briefcase-business` | /entreprises/ form chapter, /entreprises/recueil-des-besoins/ |
| forum-agenda | `calendar-range` | Forum «Prochains rendez-vous» / programme, community agenda |
| forum-rooms | `table` | community «Salles thématiques» |
| institutions / companies / universities / professionals | `institution` / `building` / `university` / `briefcase` | the collaboration forms by kind; the partners' groups by kind |
| italy | `ile-arch` | home «Écosystème institutionnel» (DECISIONS §4: Italy, the arrival) |

Deliberately **no glyph** (the title is the device): «En bref», «Pourquoi», «Pour aller plus loin», «Le promoteur»,
the pilot chapters, the home's four entrances and trust chapter, «Avertissements» (its notices already carry
`warning` and the anti-fraud callout `shield-alert`), the Forum's who/why/what/objectives/audience/outcomes/media,
the network page. And — until W2 vendors their symbols — «Étapes» (`list-checks`), «Ressources» (`book-text`), the
contact form (`message-square-text`), the speakers (`mic`), the discussions (`messages-square`); each is one line in
`CHAPTER` when the symbol arrives. /institutions/ «Destinataires» draws none: the door card above it already shows the
institution glyph (never the audience a door already shows).

## 2. What the owner sees in the preview (once merged)

- **Every public page**: the stair above the section titles is gone. 0 `#icon-ile-steps` on the 26 public pages the
  new crawl test reads (fr/ar). Heads that name a concept draw it: /fr/contact/ the at-sign; a pathway sheet the
  document, the stamp and the compass; /fr/diplomes-et-titres/ stamp, key, compass; /fr/entreprises/ the business
  case; /fr/faq/ the question mark; the home compass, signpost, newspaper (when news exist), arch.
- **Console**: «Mon parcours» keeps the stair (the one seat it has; test). The **company rail and dashboard** draw
  `briefcase-business` for «Mes besoins» / «Mes besoins en compétences» / «Votre prochaine action» instead of the wrench.
- AR: the marks sit on the reading edge (right); `signpost` mirrors (the flip list), nothing else does.

Measured on the lane server 8784 (Chromium, one at a time, under the lock), fr/ar × 1440/390, reduced motion:
`C:/tmp/ile_v5_council/evidence/v512/b-w1/` (24 section crops, 2 company dashboards, `measure.json`). Every mark is
24 px, sits on the head's reading edge and 11 px above the title's box; company rail fr 1440 and ar 390: needs = 
`briefcase-business`, wrench 0, stair 0.

## 3. Budgets

| Asset | Before | After |
|---|---|---|
| `static/img/icons.svg` raw | 31 049 B | **30 878 B** (−171; ceiling 32 768) |
| `static/img/icons.svg` gzip −9 | 6 412 B | 6 363 B |
| Shared CSS (`main.css` and imports) | — | unchanged (no CSS edited) |
| JS | — | unchanged |

Symbols: 110 → 110 (−`wrench`, +`briefcase-business`); Lucide donors 64 → 64.

## 4. Tests

New:
- `tests/frontend/test_icons.py` +4: `test_ile_steps_is_the_journeys_mark_and_nothing_elses` (the stair only at
  `NAV["pathways"]`; no product template writes it; no chapter mark is a literal);
  `test_every_chapter_anchor_names_a_concept_a_template_really_carries` (no dead anchor, every concept used);
  `test_the_chapter_mark_tag_draws_the_concept_or_nothing`; `test_the_company_needs_are_the_business_case_never_a_wrench`
  (+ the licence file).
- `tests/frontend/test_chapter_marks.py` (new, 2): renders 26 public pages (fr + ar samples) — no stair, marks only
  from `CHAPTER`, no concept twice on a page (FAQ groups apart), no two twins on a page, the expected concepts where the
  owner named the defect; and the person's console still draws the stair for «Mon parcours».

Updated (stale after the change, guard kept): `apps/pages/tests/test_home.py` (the home chapters' marks are the
registry's concepts, not `ile-steps` × n — now also asserts the stair is absent and compass + signpost present);
`tests/frontend/test_interior_w3_f1.py` and `test_orientation_w3_f1.py` (the six-icon ceiling now excludes the chapter
marks by their class instead of by the name `ile-steps`, and asserts the stair is absent).

Runs (TEST_DATABASE_URL `test_ile_v5_l4`, one pytest at a time):
- `test_icons.py test_chapter_marks.py test_interior_w3_f1.py test_orientation_w3_f1.py apps/pages/tests/test_home.py
  test_static_assets.py` — **263 passed**;
- `test_design_docs.py test_v5_tokens.py tests/test_regen_design_inventory.py apps/companies/tests
  apps/enquiries/tests/test_views.py apps/faq apps/community apps/partners apps/news` — **871 passed**;
- `apps/forum apps/pathways apps/ecosystem apps/orientation apps/living` — **633 passed**;
- after the lint fixes: `test_icons.py test_chapter_marks.py` — **26 passed**. `ruff check apps tests` clean;
  `scripts/build_icons.py --check` current.

## 5. New translatable strings

**None.** No msgid was added or changed (the templates lost an icon call and gained a tag; no text).

## 6. Requests to other lanes

- **Lane C** (owner of `static/css/v5/_pagina.css` and `apps/pages/static/pages/css/pages.css`): the `.chapter__mark`
  rule pulls its box by the shares of the `ile-steps` drawing (7 units top, 5 bottom, 3 inline-start). The heads now draw
  Lucide-grid glyphs (live area 2–22): please retune both copies of the rule to the 2-unit share —
  `margin-block: calc(var(--mark) * -2 / 24) calc(var(--s-4) - var(--mark) * 2 / 24); margin-inline-start:
  calc(var(--mark) * -2 / 24);` — so the drawing stands exactly on the reading edge (today ≈1 px outside it) and
  16 px above the title (today ≈13 px). Also update the two comments that still describe the mark as `ile-steps`
  (`_pagina.css:193`, `pages.css:110`). No other CSS is needed: a head without a glyph already reads well.
- **Lane C**: when you compose a page and want a concept mark on a head whose anchor is not in `CHAPTER_OF`, pass
  `chapter_concept="<concept>"` to the include, or ask B to add the anchor — never a literal `svg_icon` with
  `chapter__mark` (the test refuses it).
- **Lane D** (owner of `templates/dev/designpreview/**`): `templates/dev/designpreview/specimens/icons.html` names
  `wrench` for «Mes besoins» (section 2, paper and night panels): it now draws nothing (the tag logs `no icon called
  'wrench'`). Please replace `"wrench"` with `"briefcase-business"` in both panels.
- **Lane A** (owner of `COMPONENT_PROVENANCE.md`): no 21st.dev row from B in W1.
- **Orchestrator**: the evidence folder above is outside the repository.

## 7. Not done (by scope)

W2/W3 items of lane B: the 12 new symbols and the sprite split (so «Étapes», «Ressources», the forms, the speakers
and the discussions still draw no mark), the field system, the account shell, multi-step forms, document rows and
filters.

## Fixes after review (v512-b-fix-w1)

- **Major — role-word leak on `/fr/compte/profil/`.** `templates/accounts/profile.html`: the «Type de compte :
  Personne» row (`get_account_type_display`) is replaced by `{% translate "Votre espace" %}` → `{{ space_label }}`.
  The row renders only when the view passes `space_label`; that context key comes from lane D's branch
  (`apps/accounts/views.py` → `roles.space_label(user)`, D owns the view). On this branch alone the row is therefore
  absent (no leak either way); once D's branch is merged it shows the space.
- **Minor — visible WIP phrase.** `templates/community/discussion.html`: an attachment without a download URL is now
  omitted instead of showing «téléchargement bientôt disponible»; an attachment with one shows «label — Télécharger».
  (Edge case left: a post whose attachments all lack a URL keeps an empty `<ul>`; no current data produces it.)

New translatable string (for lane D, owner of `locale/**`): `"Votre espace"` (EN/AR provisional per Q3, flagged).
The msgid «téléchargement bientôt disponible» is no longer used by any template — D may drop it at the next
`makemessages`.

Runs (TEST_DATABASE_URL `test_ile_v5_l4`): `apps/accounts apps/community tests/i18n/test_page_integrity.py
tests/frontend/test_console_shell_w3_a.py` — **335 passed**.
