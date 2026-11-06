# V5.12 W2 — Senior final review of the four lanes, integrated (label v512-review-w2)

28 Oct 2026. One review of v512-a-w2 (e2fe36e), v512-b-w2 (0416862), v512-c-w2 (4425219) and v512-d-w2 (d6d5c6e), all
based on 6251475 (v512/w1). They were judged together as one product, against:

- V5.12;
- DECISIONS §0–§10, the W2 row of the Waves table, and §12–§15;
- the V5.15 bar for W2 items, as §15 requires. W3 items were not required.

**Q1–Q8.** The task text says the owner has not answered Q1–Q8. That is wrong. DECISIONS §12 records his binding
answers of 28 Oct, 11:35, and §13 records the Q2 privacy correction of 14:42. The lanes followed §12, and this review
judges against §12. Under §12:
- Q1: the hero carries the visible H1 and does not repeat the name;
- Q2: unpublished legal pages leave the navigation and are not reachable;
- Q7: there is a real organisation experience, not «minimal».

**Verdict: CHANGES_REQUIRED.** The fix pass is small: five majors, each a one-file or two-file change. The
combination is coherent and visibly better. The owner will see the visible H1, five new photographs, landing pages
with a real composition, a working Forum, a premium sign-up, forms inside the console, and a real Institution and
University space. But four W2 promises do not hold in the integrated product (M2/M3, the console foot, Q2's
unreachable pages, the person dashboard's empty wall). One new storage key also contradicts the privacy text that has
just been published.

## How it was checked

**Scratch merge.** I made a scratch worktree, `C:/tmp/ile_wt/v512-review`, at design-v5 HEAD **4d9ada5** (v514-p
merged). I merged A, B, C and D into it in that order with `--no-ff`. I resolved the conflicts by hand and ran
`npm run build` (installed packages only). The worktree has been removed since.

**Server.** I served the merge from the review launcher on 127.0.0.1:8787, on `ile_v5_l7`. I recreated that database
from `TEMPLATE ile_v5`, so the acceptance personas are in it. The launcher is the acceptance launcher with
TREE, DB and port changed, plus `ILE_DESIGN_PREVIEW_PORT=8787`. It is in
`C:/tmp/ile_v5_council/.work/v512-review-w2/` and has been stopped.

**Browser.** One headless Chromium ran under `C:/tmp/ile_locks/CHROMIUM_LOCK`, and the lock was released.

- Public pages: fr and ar, 1440 and 390, for home, institutions, universités, entreprises, parcours, forum, faq,
  sign-up and contact.
- Personas: qa-institution, qa-university, qa-company and qa-doc-person, each on its dashboard, Mon organisation, Mon
  compte, Mes documents and ma-situation.
- Also: reduced motion, the parcours filter, the FAQ accordion, and the e-mail error on blur.

The screenshots are in `shots/`, and the probes in `.work/v512-review-w2/shots.json`. The probes found no horizontal
overflow anywhere. CLS is at most 0.001.

**Tests.** I ran a targeted pytest (not browser) on the merge, with its own DB, covering the four lanes' new tests,
icons, design docs, components, layout, journey, the ecosystem compliance tests, the CSS bundle, the loader rules,
tests/i18n, cms_nav, chapter marks and O14. Result: **632 passed, 7 failed**. Every failure is a merge-step item, listed
under «Merge steps» below. I did not run the browser suites; the steward runs them (see the steward checklist).

## Major (fix before merge)

**M-1 · Integration (A owns the file; D delivered the partial).** The console still links the unpublished legal
pages.
- `templates/portal/base_portal.html` `{% block site_footer %}` still draws its inline footer.
- On every console page it links «Conditions d'utilisation» and «Avertissement». Both answer 200 with «Page en cours de
  préparation» (seen on qa-institution, qa-company and qa-doc-person). This breaks Q2 and V5.14 §13.
- Lane D's `portal/partials/console_foot.html` is never included, so the promoter line and the locked «not an
  authority» sentence never appear either.
- **Fix:** replace the inline footer with `{% include "portal/partials/console_foot.html" %}`. That is one line.

**M-2 · Integration Q2 (lane C, or lane P by agreement; W2 by §12).** Unpublished C/D legal pages can still be
reached by the public.
- `/fr/note-legali/`, `/fr/condizioni-di-utilizzo/` and `/fr/avvertenze/` answer **200** with «Page en cours de
  préparation». Q2 says this page is «never shown to the public (not reachable while unpublished)».
- Lane C passed the work to lane P, and no W2 lane did it.
- **Fix:**
  - in `apps/legal/views._legal_page`, raise `Http404` unless `services.document_available(kind)`, or unless the
    request comes through the preview's phase console;
  - move the unconditional links (`templates/community/join.html` legal:terms/privacy, `errors/_way_on.html`,
    `enquiries/partials/form_shell.html`) and the `safe_url 'legal:terms'` links (depot, `terms_required`) onto
    `{% legal_links %}`.
- The sitemap already omits these routes.

**M-3 · Integration A × C: M2 and M3 reach no element in the product.**
- Lane A's mask reveal (M2) and B/W hover (M3) key on `.figura` or `[data-reveal="mask"]` and on `[data-grade]`.
- Lane C's new photographs are `figure.foto`, without either attribute. No preview page has a curated `.figura`
  (0 found across 13 public pages).
- So the owner sees **no** masked image reveal anywhere. The only B/W→colour is lane C's own `.foto--develop`, a second
  scroll mechanism that also ignores the site's `html.rm` switch.
- **Fix (≈10 lines, A and C):**
  - in `templates/components/photo.html`, put `data-reveal="mask"` on the figure when `not p.eager` (never on the LCP
    frame);
  - map `treatment == "develop"` to `data-grade="bw-scroll"`;
  - delete `.foto--develop` and `@keyframes foto-develop` from `v5/_photo.css`.
- One mechanism, the one A measured and tested.

**M-4 · Lane A, privacy: the new storage key `ile.seen` contradicts the published cookie text.**
- `static/js/src/head/head.js` writes `sessionStorage["ile.seen"]`: the last 40 **paths** visited in the tab. In the
  console these include case-file references (`/fr/espace-reserve/dossiers/853DFACAA7/`).
- The cookie and technical-storage information (category B), published on the preview through lane P, lists every key
  and says these values «ne contiennent aucun identifiant». `ile.seen` is not in that list.
- **Fix:** store only what M5 needs. The journey's light plays on two surfaces, so keep two fixed tokens (for example
  `passage`, `journey`), not paths. Ask lane P to add the `ile.seen` row to B in it/fr/en/ar.

**M-5 · Lane D: the empty-state wall is still on the person dashboard (D-20, a W2 item).**
- qa-doc-person's dashboard still shows «Mes échéances — Les dates qui vous sont communiquées … apparaîtront ici» and
  «Communications — Les messages … apparaîtront ici».
- `dashboard_context` filters the empty cards only on the bridge (organisation and company).
- **Fix:** apply the `registers_with_rows` rule (rows, «indisponible», or its own action) to the person's side column
  too, and keep the calm sentence. The D-22 rail layout can wait for W3. This cannot.

## Minor (fix during the merge, or in W3)

**Conflicts and merge steps** (scratch merge, A→B→C→D on 4d9ada5):
1. **DECISION_LOG.** A and v514-p both claim DL54-165 → renumber A's entry to DL54-166.
2. **DESIGN_SYSTEM_2026 component count.** The merge conflicts: A says 40, B says 45.
   - The real count is **47**: 39, plus A's `session_notice`, plus B's six files, plus C's `photo`.
   - `test_design_docs::test_every_component_file_has_a_section_and_vice_versa` fails until the count and the missing
     sections are fixed (C's `photo.html` has no section).
3. **Binary dist conflict on `static/js/dist/piece-drawer.js`** (A, B): re-run `npm run build`. Only that file
   differed after the rebuild.
4. **Catalogue.** `tests/i18n/test_catalogues.py` (it, en, ar, audit) and `test_page_integrity` (the French alt texts
   of C's photographs on the AR pages) fail until lane D's catalogue pass runs after the merges. The stale msgid «Les
   champs marqués d'un astérisque (*) sont obligatoires.» needs `--sync`.

**Lane D and lane P:**
5. **Legal links cache.** `legal_links` now goes through lane P's `document_available`, whose per-kind cache D's save
   signal does not clear. As a result `test_a_single_published_page_is_linked_alone` fails on the merge.
   - Fix: `_forget()` calls `legal.services.invalidate()`, or the test publishes through `publish()`.
   - The fallback path can go once P is merged.
6. **Footer grid.** `site-footer__inner--three` has no CSS rule; with no published legal page an empty fourth track
   remains. Add D's requested `chrome.css` line (A or the steward). It is not visible on the preview, where privacy and
   cookies are published.
7. **«Courriel».** The inline e-mail error reads «Saisissez une adresse de courriel valide.». That is Django's
   catalogue, against the glossary's «Adresse e-mail» (D-11). D: override msgid «Enter a valid email address.» in the
   four catalogues.
8. **Phone help.** On the profile the telephone help repeats «Facultatif — …» under the «facultatif» tag. This is D's
   pending msgid; B's notes ask for the shorter sentence.

**Lane D, organisation space:**
9. **Country.** The identity sheet shows the raw stored country («Italia») on fr and ar. Use `core.countries` names
   when the value is an ISO code.
10. **Breadcrumb root.** On the organisation pages the trail root is «Espace réservé» while the eyebrow and the rail
    head say «Espace Institutions». Use the space's name, as B's account shell already does.

**Lane A:**
11. **Budgets.**
    - `main.css` is 31 288 B gzip. That is inside DECISIONS' 31 414 cap, but +148 B over design-v5's 31 140. The
      standing rule says shared CSS only ratchets down, so the steward decides; A names the next candidate (the
      unused `.jurisdiction` rules in register.css).
    - The console shared bundle `portal/console.css` grew 7 759 → 8 134 B gzip (M11, M13, T4).
12. **Provenance.** `COMPONENT_PROVENANCE.md` lacks the rows B asked for (Floating Label 23566, Combobox 34726,
    Calendar 34713, Icon Card Radio 28351) and the rows C asked for (approdi tiles, families chips, develop reveal,
    which disappears with M-3). §12 asks for every adapted component.

**Lane B:**
13. **Message row.** It is an `aria-live` region that also contains `role="alert"` errors, so a server error can be
    announced twice when the field is reached. Keep one channel.
14. **Style injection.** `{% form_assets %}` places a `<link rel=stylesheet>` mid-body at the first field. That is
    acceptable, and CLS measured 0.001. But a field rendered inside a fragment fetched by the drawer brings a module
    `<script>` that importNode will not run. Document it, or keep form fields out of fragments.

**Lane C:**
15. **Parcours filter.** It hides rows with CSS and says nothing about the result count. Add a polite count line, or
    accept and record the gap.
    - Each pathway's family comes from substring tests in the template (`entry.key in '…'`). Move that to a tuple in
      the view or the registry.

**Preview data (orchestrator, outside the repo):**
16. Visible text still shows `qa-…@example.test` on the dashboards' account line, and the organisations' names end in
    «(prova)» in the persona labels. Lane D's acceptance 1 forbids «qa-», «prova» and «test» outside the hub metadata.
17. Add `Page("organisation", …)` to `_org_pages()` as D requested, then restart 8780 after the merge so the new .mo
    is loaded.

**Superseded in W3 (V5.15 §15; not a W2 finding):**
- the W1 header line as the only loader cue;
- the two-row navbar;
- /forum/ lighting the «Institutions» door (pre-existing on 8780).

**Owner policy, noted only:** the sign-up's consent still makes the person accept the unpublished «Conditions
d'utilisation».

## What the owner will see (integrated, after the majors)

- **Motion:**
  - page-head hairlines;
  - list marks and «la linea» drawing as they enter;
  - FAQ accordion height, a tinted plate, plus becoming minus (checked: about 242 px in the middle of opening, then
    249 px, plate rgb(242,244,243));
  - success toasts and errors that stay;
  - the console rail plate gliding;
  - the drawer's T4 region;
  - a 4 px scrim blur.
  - Reduced motion shows stills.
  - M2/M3 only after M-3.
- **Forms:**
  - five audience cards with distinct glyphs (person, building, institution, university, briefcase);
  - «facultatif» instead of asterisks;
  - e-mail and phone glyphs;
  - the message row on blur;
  - the country combobox;
  - Mon compte inside the console with «Sécurité du compte»;
  - form JS 4.4 KB gzip, loaded on form pages only.
- **Imagery and composition:**
  - home: H1 «ITALY LEGAL ENTRY™» visible, the mark alone in the header, the cedar and marble diptych, the working
    table;
  - institutions, universités, entreprises and parcours: 4:5 or 3:2 heroes as LCP, every derivative ≤ 43 KB at
    800 w, CLS ≤ 0.001;
  - Forum in three movements, with no stock photograph (Q4);
  - parcours numbered 01–08 with family chips (Famille → one row, checked);
  - RTL mirrored, and the photographs are never flipped.
- **Platform, Q7:**
  - qa-institution and qa-university get their own rail (Tableau de bord, then Coopération: Mon organisation and Mes
    demandes, then Échanges: Communications);
  - the space name at the rail head;
  - the identity sheet;
  - «Le projet» links with section glyphs;
  - a calm sentence and the approved CTA while G2 is open;
  - ma-situation redirects to the dashboard;
  - AR at 390 is clean.
- **Footer:** only Privacy and Cookie Policy are linked; the fraud link uses the glossary's words.
- **Security and secrets:** no secret, key or personal datum in the diffs. Every Pexels frame has a PROVENANCE row
  (author, licence, sha256), and the key is read from the environment only. No new npm runtime dependency and no
  animation library.

## Steward checklist for the W2 merge

1. Merge A → B → C → D on design-v5 (4d9ada5 or later). Resolve the merge steps 1–3.
2. Apply M-1 … M-5. If needed, A and C take one shared commit for M-3.
3. Run D's catalogue pass. Update DESIGN_SYSTEM §10 (47 files, the `photo` section), the provenance rows and the
   footer grid rule.
4. Run the browser suites the lanes name:
   - apps/pages/tests/test_browser.py (the hero geometry: the statement is now taller);
   - the ecosystem and interior browser tests;
   - test_motion_v512_a_w2 and test_form_system_v512_b in browser mode;
   - test_design_preview;
   - the hidden-route suites of DECISIONS §14.
5. Rebuild the dist bundles, restart 8780 on the merged tree, and re-probe the console foot, the legal routes (404)
   and a photo's mask.
