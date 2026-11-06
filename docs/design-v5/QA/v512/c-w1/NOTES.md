# V5.12 · Lane C · W1: the hide gates (label v512-c-w1)

Branch `v512-c-w1`, cut from design-v5 `e047fae`.

**Scope.** DECISIONS.md §8 (public rows) and the W1 row of the «Waves» table for C:
- living;
- pathways;
- diplomas and training;
- news;
- partners;
- the Forum's pre-event blocks;
- the latent empty states.

**Out of scope here:**
- no image and no composition (those are W2/W3);
- no icon line: B's `ile-steps` lines in `living/topic.html` and `partners/index.html` are untouched;
- no locale file;
- no shared sheet (`main.css`, `tokens.css`).

## What changed

| Surface | Decision | Control |
|---|---|---|
| `/actualites/` | Hidden while no article is live. | `core.gates.news_public()`: true with at least one live article, or when the newsletter is open (its form lives on that page alone, so a subscription never redirects to a 404). The route is registered with `requires_gate="news_public"`. `news.views.index` answers 404. `NewsIndexSitemap` is empty. The «Aucune actualité publiée…» wall is removed. |
| `/partenaires/` and every «Voir les partenaires» link | Hidden while no partner is both live and authorised (G6). | `core.gates.partners_public()`. The route is registered with `requires_gate="partners_public"`. The view answers 404 and the sitemap is empty. `pages.services` and `ecosystem.services` build the link with `core.links.public_url`, which covers home, network, AGAMI, institutions and pilot. The empty-state branch of `partners/index.html` is removed. |
| Menu and footer | No link to a hidden page. | `cms_nav.resolve_url` now drops any destination whose registered route is closed (`core.links.path_is_open`). This applies to the static fallback and to back-office `MenuItem` rows alike. The footer (D's file) is built by `footer_menu`, so «Actualités» leaves it without a footer edit. |
| Home, «Un écosystème institutionnel» | The promoter stands alone. | The partners' bay renders only with an authorised partner. `home-ecosystem__grid--single` keeps the promoter on one column (page sheet `pages.css`). «Les partenaires sont présentés au fur et à mesure…» is removed. |
| `/reseau/` | No «partners to come» sentence. | With partners, the chapter is «Partenaires». Without them it is «Pour aller plus loin» (an existing msgid). The Forum and promoter links are kept. |
| `/vivre-en-italie/` and its 10 themes (health and SSN among them) | The index shows the approved introduction only. The themes are hidden. | `living.services.public_topics()` keeps only themes with `sheet_count > 0` (sheets live and `legal_review=REVIEWED`). The `topic` and `sheet` views go through it, so they answer 404, staff preview included. The sitemap lists only themes that have a sheet. The ten theme paths left the route registry: they are content-driven, not pages owed a 200 when G3 opens. «Fiches en préparation», «Thèmes en préparation» and «en cours de rédaction» are removed. |
| `/parcours/<slug>/` ×8 | The empty chapters are hidden. | `pathways.services.detail_context` builds the page index from the chapters that have content. `detail.html` draws «Aperçu» only with a context or the origin-country notice (kept verbatim, legal). «Étapes», «Documentation» and «Autorités» appear only with items. Removed: «publiés au fur et à mesure», «Contexte / Liste en cours de vérification», «Étapes en préparation», «Acteurs en cours d’identification». |
| Metadata row (pathways, diplomas, training) | No «being verified». | In `_review_meta.html`, the «Dernière vérification» row appears only when there is a date. Otherwise the row shows the nature alone. |
| `/diplomes-et-titres/` | The work-in-progress sentences are hidden. | The «publiés au fur et à mesure» fine print is removed. The steps lead («…elles seront détaillées après vérification…») is removed. This adds no new msgid, so the AR page never shows untranslated French. |
| `/parcours/` | Latent chip removed. | The «Fiche détaillée en préparation» chip is gone. An unpublished pathway is listed without a link. |
| `/forum/` (permanent mode) | The locked pre-event blocks are hidden (C9, default answer to Q4). | `forum/index.html` renders PROGRAMME and INTERVIENNENT only `{% if not is_permanent %}`. The page index drops their anchor. The launch dateline stays. Without a live edition the page answers 404; the «Cette page est en cours de préparation» empty state is gone. |
| FAQ and glossary (latent) | An empty index answers 404. | `faq.views.index` and `glossary.views.index` answer 404 to the public when there is no live entry. An editor's `?preview=1` still opens. The empty-state branches are removed. |

**Kept on purpose:**
- the pilot's «Un projet en cours de construction» notice and the origin-country «Parcours en construction…» notice (the art. 23 D.Lgs. 286/1998 caution);
- the locked living introduction («…progressivement enrichis…»);
- the locked Forum sentence «Au cours du Forum seront également présentés…»;
- the legal pages (Q2: owner action, G1).

## What the owner sees (8780, after the merge)

- `/fr/vivre-en-italie/`:
  - the approved title and introduction, with no list of ten «Fiches en préparation»;
  - every theme URL (`/vivre-en-italie/sante/`, `…/logement/`) is the 404 page;
  - the 21:9 image band comes in W2/W3.
- `/fr/forum/`: the permanent Forum without PROGRAMME or INTERVIENNENT. The page index lists the five presentation chapters.
- Pathway sheets:
  - only the chapters that have something to say (steps on the linea, authorities, warnings, resources, orientation);
  - the meta row reads only «Nature : Contenu informatif…».
- Diplomas and training: no «en cours de vérification», no «au fur et à mesure».
- Home ecosystem: AGAMI alone, with no partners' bay.
- Navigation: the «Projet» panel and the footer no longer show «Actualités».
- Hidden pages: `/fr/actualites/` and `/fr/partenaires/` answer 404.

**Checks on lane server 8785** (l5 database, dev settings, `ILE_DESIGN_PREVIEW=1`, `ILE_REFERENCE_DATE=2026-10-03`):
- Status codes were checked on 18 public URLs.
- `<main>` was scanned on 21 pages × fr/it/en/ar (84 pages). It found:
  - 0 occurrences of «en préparation / en cours de vérification / en cours de définition / prochainement / seront publié(e)s / au fur et à mesure / en cours de rédaction / seront détaillées / en cours d’identification»;
  - 0 links to `/actualites/`, `/partenaires/` or a hidden theme.
- `sitemap.xml` has 160 URLs. The only `vivre-en-italie` entries are the four index pages. There is no news or partners index.
- Screenshots were taken in Chromium, with the lock taken and released:
  - fr and ar at 1440 and at 390, the 390 pass with `reduced_motion=reduce`;
  - pages: home ecosystem, living, forum, network, pathway, origin pathway, diplomas, training.
- No page scrolls horizontally at either width.
- RTL is mirrored as before; there is no new layout.
- The shots and scripts are outside the repository: `C:/tmp/ile_v5_council/.work/v512-c-w1/` (`shots/`, `scan.py`, `shots.py`).

## Budgets

| Item | Change |
|---|---|
| `main.css` | Untouched (0 B). |
| Page-only `static/css/dist/pages/css/pages.css` | 3 779 → 3 795 B gzip (+16 B for the `--single` grid), well under 6 KB. |
| JS | None. |
| Queries | +1 cheap `EXISTS` per menu build, where a news or partners link is resolved. The home query-budget test (≤ 30) passes. |

## Tests

All runs used database lane l5 (`TEST_DATABASE_URL=…/test_ile_v5_l5`), one pytest process at a time.

**New compliance file:** `tests/compliance/test_hide_gates_v512.py`, 9 tests:
- both gates are closed on an empty site;
- no menu or footer link to a hidden page, in each of the 4 languages;
- a back-office menu row pointing to a hidden page is left out;
- an empty FAQ or glossary answers 404;
- health has no reachable route.

**New tests in the app suites:**
- news:
  - 404 while empty, with the links and the sitemap following;
  - the open newsletter keeps the page, without an empty wall.
- partners:
  - 404, no link, and the promoter alone;
  - the page and its links appear with an authorised partner.
- living:
  - only reviewed themes are listed;
  - a theme answers 404, including in preview;
  - the sitemap.
- forum:
  - permanent mode hides the programme, the speakers and their anchor;
  - event mode keeps them;
  - no event answers 404.
- pathways:
  - empty chapters and their index entries are not drawn;
  - the origin notice keeps the overview;
  - the meta row without a date.
- ecosystem, pages, network: no partners' link.

**Stale tests brought to the rule.** Assertions were kept or tightened; none was removed without a replacement.
- living: compliance, services, views.
- news: compliance, views.
- partner gate.
- forum: page, mode.
- pathways: services, views.
- ecosystem: gated pages, services.
- home and institutional.
- second-factor FAQ page: it now seeds one live question.
- nul-byte: the `?q=%2500` check moved to the home.
- content pages W3-F2:
  - the news filter is read over a live article;
  - the topic glyph is read over a theme that has a sheet.
- floors: the i18n routing floor went 30 → 27 and the page-integrity floor 55 → 54. The drop is exactly the routes removed (the ten themes, news, partners).

**Runs:**

| Suite | Result |
|---|---|
| apps living/news/partners/faq/glossary/forum/pathways | 521 passed |
| ecosystem/pages/cms/core/faq/glossary | 611 passed, plus the 5 fixed |
| compliance, i18n routing/integrity, content pages, css bundle, phase console | 297 passed, plus the 11 fixed |
| final consolidated run (19 files and suites, after every fix) | 776 passed |

Browser tests (`-m browser`) were not run; see the requests below.

## New and removed msgids (for D)

**New: none.** «Pour aller plus loin» already exists.

**No longer used.** D's makemessages will mark these obsolete:
- «Fiches en préparation»
- «Thèmes en préparation.»
- «Les fiches pratiques de ce thème sont en cours de rédaction et de vérification. Elles seront publiées progressivement.»
- «Voir tous les thèmes» (if unused elsewhere)
- «Contexte en cours de vérification»
- «Les conditions générales de ce parcours seront décrites après vérification…»
- «Les détails de chaque étape sont publiés au fur et à mesure…»
- «Étapes en préparation»
- «Liste en cours de vérification»
- «La documentation généralement requise pour ce parcours sera publiée après vérification.»
- «Acteurs en cours d’identification»
- «contenus détaillés en cours de vérification»
- «Les partenaires sont présentés au fur et à mesure de leurs autorisations écrites.»
- «Aucun partenaire n’est encore présenté.»
- «Les partenaires seront présentés au fur et à mesure des autorisations.»
- «Aucune actualité publiée pour le moment.»
- «Les nouveautés normatives… seront publiées ici.»
- «Cette page est en cours de préparation.»
- «Les informations sur le Forum seront publiées prochainement.»
- «Les questions fréquentes sont en cours de préparation.»
- «Le glossaire est en cours de préparation.»
- «Cette page sera enrichie progressivement.»
- «Fiche détaillée en préparation»
- the diplomas steps lead «Structure générale des démarches… elles seront détaillées après vérification avec les acteurs compétents.»

## Requests to other lanes

- **D, design preview (D's files):**
  - `apps/designpreview/live.py` still lists `living-topic` (`/fr/vivre-en-italie/logement/`), `news` (`/fr/actualites/`) and `partners` (`/fr/partenaires/`). They now answer 404 by design. Either annotate them as `community` is («404 finché…») or drop them from the hub.
  - `tests/frontend/test_design_preview.py` has the same three paths in `CENSUS_TYPES`. Check the census test after the merge.
- **D, Academy:** `templates/academy/course_detail.html:78` still carries a latent «prochainement» empty state (F-12). D owns the Academy templates.
- **D, footer:** nothing to consume. The footer's links come from `footer_menu`, which now honours `news_public` and `partners_public`. Any direct link added later should use `{% safe_url %}` or `core.links.public_url`.
- **Browser tests** (Chromium; not run here, given the machine's one-browser rule):
  - `tests/frontend/test_browser_w1_b.py::test_an_empty_state_draws_its_space…` and `…forced_colours…` read the empty states of `/fr/partenaires/` and `/fr/actualites/`, which no longer exist. B owns that file and the empty-state component. Point them at an empty state that remains: the news category's empty answer, or a FAQ/glossary search with no results.
  - `tests/frontend/test_content_pages_browser_w3_f2.py::_pages` lists `/partenaires/`, `/actualites/` and `/vivre-en-italie/logement/`. Fixing it falls to C's next wave or to the reviewer: seed an article, a partner and a sheet in that test's `content` fixture.
- **A:** none. No shared sheet or partial was touched.

## Not done in W1 (by the wave plan)

- Imagery, the compositions, the living 21:9 band and the network diagram are W2/W3.
- Pre-G3 latent sentences were left as they are, because they appear only while G3 is closed or the orientation route is absent, never in the release state:
  - «seront publiées progressivement» in `pathways/index_interim.html` and `pages/home/_pathways.html`;
  - the orientation «disponible prochainement» chip.
- **Observed, not changed:**
  - On `/forum/`, the «Institutions» door is marked current. Its panel's task link is the Forum (`cms_nav._mark_current`).
  - This predates this branch.
  - It is a one-line rule to settle with A/D if it reads wrong.

## Fixes after review (label v512-c-fix-w1)

Two minors from the W1 review, both fixed.

**1. The chapter mark kept the old drawing's shares** (`static/css/v5/_pagina.css`, `apps/pages/static/pages/css/pages.css`, `.chapter__mark`).
- Since B's W1, the heads draw Lucide-grid concept glyphs, whose live area is units 2–22 of the 24-unit box. The rule still pulled the box by the `ile-steps` shares (7 top, 5 bottom, 3 inline-start).
- Both copies now use B's 2-unit formula: `margin-block: calc(var(--mark) * -2 / 24) calc(var(--s-4) - var(--mark) * 2 / 24); margin-inline-start: calc(var(--mark) * -2 / 24);`. Both comments now describe the concept glyph, not `ile-steps`.
- Geometry with `--icon-lg` = 24 px (1 px per unit):
  - the drawing starts on the reading edge, at 0 px (it was 1 px outside);
  - it ends 14 + 2 = 16 px above the title (it was 13 px);
  - `margin-inline-start` mirrors in Arabic.
- The two sheets are page-level bundles, not `main.css`. The rebuilt dist got smaller in all 7 bundles that import them:
  - `pages.css` 3 785 → 3 782 B gzip;
  - `lettura` 4 113 → 4 110;
  - `ecosystem` 3 471 → 3 467;
  - `forum` 3 101 → 3 097;
  - `wizard` 4 178 → 4 175;
  - `interior` 2 301 → 2 297;
  - `pathways` 3 665 → 3 661.
- On this branch alone, the heads still draw `ile-steps` (B's `chapter_mark` tag is not merged here). The rule is written for the merged state. It was checked by arithmetic, not in the browser, because the glyph it is tuned for exists only after the merge. **Reviewer:** please measure one fr and one ar head after merging B and C.

**2. Forum and news gates.**
- **Forum.** `/forum/` already answered 404 without a live edition, but its route had no gate, so the menu kept the link. Changes:
  - New gate `core.gates.forum_public()`: true when `forum.services.current_event()` exists. It is registered in `core.links._GATES` and `cms_nav._GATE_FUNCTIONS`.
  - `forum/` is now registered with `requires_gate="forum_public"`. The menu, the footer, `{% safe_url %}` and back-office menu rows therefore drop the link.
  - `pages.services` (project, network, AGAMI, contact) and `ecosystem.services.related_links` build the Forum link with `public_url`. Their templates already guard empty links.
  - The registration page's breadcrumb and its empty-state «Retour à la page du Forum» use `public_url` too. Without an edition they show plain text and no button, never a link to a 404.
  - The two registration paths stay ungated, so their behaviour is unchanged.
- **News.** `news_public()` was also true on the newsletter flag alone. It now follows the DECISIONS §8 row («at least one published item»): `Article.objects.public().exists()` only.
  - The newsletter form and its success redirect live on the index alone. `newsletter_subscribe` therefore answers 404 until the first article as well, and never redirects to a missing page.
  - Checked: with the newsletter open and no article, `/fr/actualites/` and the subscribe POST answer 404, and the home has no link. With one live article, the page shows the list and the form.

**Tests (lane l5):**
- New in `apps/forum/tests/test_forum_page.py`:
  - `test_without_event_no_link_leads_to_the_forum`: the route's gate, and no `/xx/forum/` link on home, project, network, AGAMI or registration, in 4 languages;
  - `test_with_event_the_forum_link_comes_back`.
- Changed to the new rules:
  - `test_forum_routes_registered_as_public`: `forum/` is gated, registration is ungated;
  - news `test_the_open_newsletter_alone_does_not_reopen_an_empty_news` replaces the newsletter-keeps-the-page test.
- Seeded with one live article, because the form exists only on a live news page:
  - `apps/news/tests/test_newsletter.py`, through an autouse fixture;
  - `tests/compliance/test_gate_dependencies_w4_d.py`;
  - `tests/frontend/test_content_pages_w3_f2.py` (the two newsletter tests).
- Runs:
  - forum, news, gate compliance and content pages: 126 passed after the fixes;
  - wider selection (forum, pages, ecosystem, cms, core, partners, i18n routing and integrity, compliance; `-m "not browser"`): 884 passed;
  - CSS and JS bundle-is-current and token checks: passed.
