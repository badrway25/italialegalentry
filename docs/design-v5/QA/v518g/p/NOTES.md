# V5.18 green suite — group P, the public/RTL browser family (label v518g-p)

Branch `v518g-p` from design-v5 `900372a` (tag `v518/stabilisation`), worktree `C:/tmp/ile_wt/v518g-p`, database
lane l7 (`test_ile_v5_l7`). Binding: V5.18 (`V5_18_FINAL_VISUAL_ACCEPTANCE_GATE.md`), V5.12 §22 («technical tests
remain green»), DECISIONS §8, §15, §16, Q1, DL54-170…175. Source of the failures:
`evidence/v518/REGRESSION_BROWSER.md` (21 of its 41 are this group's). No visual redesign, no locked copy touched, no
msgid added, nothing machine-translated; every stale guard re-pointed at the owner-approved behaviour with the same
strength, none deleted, none loosened.

## Each failure

| Test | Verdict | What was done |
|---|---|---|
| `test_rtl_browser::test_trademark_sign_stays_on_the_right_of_the_name_in_every_wordmark` | Stale test (Q1) **and a candidate defect it hid** | Stale: on `/ar/` the header shows the mark alone (Q1, `hero.css`), so only the footer's wordmark is drawn. The guard now counts the header and the footer on `/ar/le-projet/` (≥ 2) and the footer on `/ar/` (≥ 1). Re-pointed, it found a **real I18N-06 defect**: «Le projet»'s trademark line (`templates/pages/project.html`, `p.page-trademark`) set the name in `<span translate="no">` with no direction, so in Arabic «™» painted on the LEFT of the name. **Fixed at the root:** `dir="ltr" lang="en"` on that span, as every other wordmark has; `apps/pages/tests/test_institutional.py::test_project_page_trademark_line` pins the isolate. |
| `test_browser_chips_w1_c::test_the_cards_sit_on_their_levels_with_one_radius` | Stale test (V5.15 lane A motion, M15; cb252091/b9098210; DL54-170) | Was «no shadow moves (SH-4)». Now: under a fine pointer a link card lifts **onto exactly `--shadow-3`** (resolved from the token, distinct from levels 1 and 2) **and by exactly 3 px** (`translate: 0px -3px`), read after its transitions have finished (not after a fixed 300 ms). The hairline and the underline checks unchanged. |
| `test_browser_w1_c::test_a_public_field_is_la_lastra_and_its_focus_is_the_one_system` | Stale test (V5.15 lane B formwork, 7788ca38; DL54-173) | The contact form stands in `.formwork`, which sets `--field-radius: var(--radius-md)`: the radius is asserted **6 px** (was 4), with a new assertion that the form IS in its formwork. |
| `test_browser_w1_c::test_a_link_to_an_faq_row_opens_it` | Stale test (V5.12 lane A W2, Accordion-09, e2fe36ec) | The rotating chevron is gone; the mark is the drawn plus/minus. Asserted exactly: a closed row `background-size: 100% 1.5px, 1.5px 100%` (the plus), the opened row `100% 1.5px, 1.5px 0px` (the minus), no transform on either. The permalink part unchanged. |
| `test_browser_w2_c2::test_the_sheet_opens_and_closes_on_the_overlay_system[fr]`, `[ar]` | Stale test (Q1, 44252192) | On the home the bar's lock-up is the mark alone. Now asserted: the bar draws no words and the sheet's head does; both lock-ups stand on one row (same top and bottom) from the same inline start; the marks share the row; in French the mark does not move at all. In Arabic the lock-up is the wordmark's LTR isolate, so the whole name grows from the row's start and its mark is the isolate's left end (observation below). |
| `test_header_fits_the_narrowest_viewport::test_the_name_and_the_menu_button_share_the_phone_row[fr]`, `[ar]` | Stale test (Q1) | The name's 329 px threshold is measured on `/{lang}/parcours/`; the home is also swept at the same nine widths and must show **no** name at any width (Q1), with the same «Menu» column and no-scroll checks on both. The probe now reads `.site-header .lock__text`, not the first lock-up in the document. |
| `test_rtl_browser::test_every_arabic_public_page_fits_the_viewport[390]`, `[1440]` | Stale test (DECISIONS §8 «complete or hide»; V5.12 §8) | The floor `served >= 55` is replaced by the **exact** set: every one of the 56 registered paths (57 registrations: one path is registered twice) answers 200 except `actualites/`, `partenaires/` and `forum-virtuel/`, which must answer 404 — read from their own gates (`gates.news_public`, `gates.partners_public`, `gates.virtual_forum_enabled`, all closed in this fixture: no article, no partner, the flag off). The overflow and one-h1 sweep still covers every route, the 404s included. Stronger than the floor: a fourth route going dark now fails. |
| `test_rtl_browser_nav::test_the_architrave_and_the_entries_follow_the_doors_in_both_directions[ar]`, `[fr]` | Stale test (V5.15 lane A floating mega panel; cb252091/b9098210; DL54-170) | W2-C1's N2 («the entries column starts at the first door's inline start») replaced by the panel's geometry, measured in inline terms so the same assertions hold mirrored: the sheet on the panel's inline start, «la lunetta» flush on its inline end, the sheet ending where the lunetta starts; the lede (eyebrow, gloss) on the sheet's start; the entries 32 px (`--s-8`, the column gap) after the gloss and before the lunetta. N19 (the architrave), the panel's edges and the plain panel unchanged. |
| `test_mobile_rtl_w4_a::test_every_stand_alone_link_answers_on_44px_under_a_finger_and_24_under_a_pointer[finger]`, `[pointer]` | Stale test (V5.15 lane B steps engine; DL54-173) | `/fr/entreprises/` no longer draws an «aiuto» line, and the companies' consent link stands in the form's consent step, `hidden` until reached. The two door-page entries became `STEPPED_TARGETS` (`/fr/entreprises/`, `/ar/entreprises/` and `/fr/entreprises/recueil-des-besoins/`): the step holding the link is painted as `steps.js` paints a reached step (that one shown, the others hidden), then measured with the same 44/24 px rules. (Measuring with script disabled was tried and rejected: Playwright's evaluate never returns in such a context.) |
| `test_mobile_rtl_w4_a::test_a_notices_address_answers_on_its_targets_while_the_legal_texts_are_awaited[finger]`, `[pointer]` | Stale test (C-W3 M-2, DECISIONS §16) | An unpublished C/D legal page now answers 404; asserted for `/ar/condizioni-di-utilizzo/` and `/fr/note-legali/`. The pending notice is measured where it is still drawn — the public privacy and cookie pages: `/ar/privacy-policy/` and `/ar/cookie-policy/` join `/fr/privacy-policy/`. |
| `test_orientation_browser_w3_f1::test_no_overflow_three_corners_and_no_raised_shadow_at_rest[1440-900-fr/ar, 390-844-fr/ar]` | **Ruling** (DL54-178) | Isolated: the one raised element on `/diplomes-et-titres/` is the head's photograph in its passe-partout (`img.foto__img`, `0 28px 56px -24px`, `_fronte.css` «the photograph in its passe-partout»); once admitted, `/attention-aux-fraudes/` showed the head's notice panel on `--shadow-3` (`_fronte.css` «notice: the page's one notice is the head's panel»). Both are lane C's designed V5.15 surfaces. **Ruled: admitted by name** (`ADMITTED_RAISED`), exactly as w3-f2's `V515_RAISED` admits `.foto__img` (V5.18 T3); any other raised surface at rest still fails. Not «fixed at rest»: removing the drop would undo lane C's scored composition (a visual redesign). |
| `test_content_pages_browser_w3_f2::test_every_content_page_holds_the_grammar_in_both_directions` | **Ruling** (DL54-178; closes the guard DL54-173 left open) | Measured: on the three formwork pages every corner beyond the targa's is inside `.formwork` (12 frame/panel, 8 consent box, 6 fields/tiles, 4 action, 999 «optional» pill, 6.4 the 32 px glyph tile at 0.2 × its side, 1 the 2 px step bar). **Ruled:** the formwork is one composed object with its own designed corner set; inside `.formwork` corners must lie in exactly that set (`FORMWORK_CORNERS`; a new value fails, and a formwork page must draw its formwork); outside it §1.3's three corners with the targa still apply unchanged to every page. |
| Review polish 1 — the Parcours CTA inside the first screen at ar 375 × 667 | Already closed upstream (e522cb1, v518-c-refix), **verified** | Measured on this branch: ar 375 × 667 `.via__action` 586–638 against 667 (fr 558–610). The guard `test_browser_w3_f1::test_the_door_card_carries_its_way_in_the_first_screen…[375-667]` (lane C's tightened bottom ≤ viewport height) passes. Nothing to change. |

## Rulings (as the Director, per DECISIONS §15; recorded in DECISION_LOG_V54 as DL54-178, the number the steward gave «DL54-G-P» at the merge)

1. **Formwork corners.** The V5.15 Premium Forms formwork is a composed object (owner's V5.15 override, lane B, scored
   4, merged as DL54-173). §1.3's «three corners a screen» governs a reading page's own surfaces; the formwork carries
   its own token-derived set and is pinned to it exactly. Ratchet, not release: no corner outside the set, none
   outside the formwork beyond §1.3.
2. **Raised surfaces in a page head.** The photograph's passe-partout and the fraud page's notice panel are lane C's
   designed V5.15 head surfaces (DL54-172); admitted by name, nothing else. SH-8 stands for every other element.

## Observation for the owner's review (not changed: no redesign in a green-suite step)

- On the Arabic **home**, opening «Menu» on a phone: the bar shows the mark alone at the row's start (right); the
  sheet's head shows the whole Latin wordmark, an LTR isolate, starting at the same right edge — so its mark sits at
  the wordmark's left end, about 183 px to the left of where the bar's mark was. On every other Arabic page the two
  lock-ups are identical. A design call for lane A if the owner finds the jump visible.

## Files

- Product: `templates/pages/project.html` (the trademark line's LTR isolate).
- Tests: `tests/frontend/test_browser_chips_w1_c.py`, `test_browser_w1_c.py`, `test_browser_w2_c2.py`,
  `test_header_fits_the_narrowest_viewport.py`, `test_mobile_rtl_w4_a.py`, `test_orientation_browser_w3_f1.py`,
  `test_content_pages_browser_w3_f2.py`, `tests/i18n/test_rtl_browser.py`, `test_rtl_browser_nav.py`,
  `apps/pages/tests/test_institutional.py` (one assertion).
- Shared file touched: `docs/design-v5/DECISION_LOG_V54.md` (one appended entry).

## Runs

Lane l7, CI-style environment (no `.env`, the CI placeholders, `PYTHONIOENCODING=utf-8`), Chromium under
`C:/tmp/ile_locks/CHROMIUM_LOCK` (taken 23:22, released at the end).

- **Final, after merging design-v5 `4817520` (lane K's v519-k landed):** `pytest -m browser --create-db` on the nine
  files — `test_content_pages_browser_w3_f2`, `test_orientation_browser_w3_f1`, `test_browser_chips_w1_c`,
  `test_browser_w1_c`, `test_browser_w2_c2`, `test_header_fits_the_narrowest_viewport`, `tests/i18n/test_rtl_browser`,
  `test_rtl_browser_nav`, `test_mobile_rtl_w4_a` — plus `test_browser_w3_f1::test_the_door_card_carries_its_way…`
  (polish 1): **149 passed**, 0 failed, 992 s.
- Non-browser tests of the same files plus `apps/pages/tests/test_institutional.py`: 60 passed, 1 failed —
  `test_mobile_rtl_w4_a::test_the_500_keeps_its_semicolon_with_its_words`, the known candidate defect «the 400/500
  pages query the database» (REGRESSION_NONBROWSER rows 16–18), another group's; red at 900372a too.
- `ruff check` on every touched Python file: clean.
