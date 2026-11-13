# W3-F2 shipped — 12 October 2026

**Content, legal, error and account pages — the rest of the public interior in V5.** Tag **`v54/w3-f2`** (design-v5
`bfd2901`, the status commit, as for the earlier families); merge commit `9af0e1a`. The owner's preview on
http://127.0.0.1:8780 serves it: v5-live checked out at the tag, 8780 restarted at 02:40 and verified. Steward's merge,
label `w3-f2-merge`, under `DESIGN_V5_MERGE_LOCK` from 01:50 (after W2-A's merge released it). Reviewed once and fixed
(V5.5): `REVIEW.md` and `A11Y_PERF.md` are both SHIP_AFTER_FIXES with no P0; the fix pass (`NOTES.md`, «Review
fixes») closed the three majors (M1 the door at rest on the error pages, M2 the Latin heads on the Arabic reading edge,
M3 / A1 the refused newsletter seen and announced), ten of the twelve minors (m11 and m12 left, with their reasons),
and A2–A4; P1 — the content page type's CSS — was handed to the merge and is recorded here (DL54-99 item 6). No
reviewer has read the fix pass again.

## What shipped

- **«La lettura» — the content and legal pages** (`static/css/v5/_lettura.css` through the page sheet
  `cms/lettura.css`, loaded by those pages only): the FAQ (on the system's accordion, its search in the head's end
  seat), the glossary (a visible register, the letter index sticking under the letterhead) and a term, the partners,
  the news and the newsletter (a refusal now opens the form's error summary, the consent named in its own language),
  an article, «Vivre en Italie», a topic (its glyph with its title) and a sheet, the Forum Virtuel's pages (behind
  their flag), the contact, company-needs and collaboration forms and their answer, the five legal pages (the trail,
  the verification line, the official Italian text kept left to right on the Arabic page, the courtesy translation as
  a quote's box), the newsletter's confirmation and unsubscription. One interior grammar, value for value with the
  home's chapters: the trail, the head at the reading edge, chapters with the `ile-steps` device, registers on
  hairlines, a quiet foot; D26's slots (verification line, one inset, one action, «who can help me», the authority's
  host shown); no row arrow, no dashed box, ≤ 3 glyphs a page.
- **«Le pagine di servizio» — the error pages** (`templates/errors/**`, page sheet `cms/errori.css`): 400, 403, 404,
  410, 429 and 500, in fr, ar, it and en, one quiet page for every status — what happened, one primary, the way back,
  the way on, «who can help me» — that reveals nothing (no path, no stack; the 500 shows the request's correlation id),
  with **the door at rest** (the owner's door stage, the key out of the lock, nothing moving). The 400 and the 500 are
  **self-sufficient** (`apps/core/views.py`): drawn without the request's context processors, the session or the
  database, with a bare fallback if even the template fails. The anonymous 403's sign-in carries `?next=`.
- **The account pages** (page sheet `cms/servizio.css`): the profile (its personal fields with their input purposes),
  the e-mail addresses, the password, the second factor and the authenticator's set-up, the deletion request behind
  its own confirmation (and its answer), the sign-out's confirmation — one frame on the public shell (the trail, the
  account's sections in the chapter head's seat, the page in the body's eight columns), the login's form side (labels
  above, 52 px plates, one flat primary; allauth's manage pages with one primary each).
- **Arabic**: every page mirrors; every Latin head stands on its cell's reading edge; foreign runs keep their direction.

## The merge

- **The sync** (`f4f344e`): design-v5 at `abbabda` — 80 commits since the branch point (the static pipeline's record,
  W3-B's dashboards, W2-A's overlay system, their merges and shipped notes, the confidential-material guard) — merged
  into the branch. Four conflicts, both areas' work kept: `components.css` (W3-F2's §20 and W2-A's §21 both gone — the
  merged sheet is design-v5's plus exactly the family's diff, and the branch's plus exactly W2-A's), DS 2026 (§2's
  components row with both families' clauses; `doorway.html`'s «Usato in» naming W3-B's NowPanel and W3-F2's error
  pages), the decision log (design-v5's entries, then the family's), `dist/main.css` (rebuilt).
- **The numbering**: the family's entries are **DL54-96 … DL54-98** (written as DL54-77 … 79; `NOTES.md` «Merge step»
  gives the mapping); the steward's record of the merge is **DL54-99**.
- **The ten paths outside the slice** are the area's in the manifest (`0e290e9`): the two page partials, the three
  page sheets, `apps/cms/templatetags/lettura.py`, and slices of `apps/core/views.py`, `apps/living/catalogue.py`,
  `apps/accounts/profile_forms.py`, `apps/news/forms.py`; DS 2026's slice named as written. The check after it:
  57 inside, 8 slice, 19 generated, and the two steward-only paths the steward wrote (the manifest, the capture report).
- **The bundles** rebuilt from a clean dist on the branch (`bb8af88`) and again on design-v5 after the merge
  (`8d60073`): every CSS bundle byte for byte the tested one; the JS byte for byte design-v5's before the merge (the
  family changed no script; the shared chunks' names follow the worktree).
- **The shared CSS (the owner's V5.8)**, gzip -9: `dist/main.css` **42 152 → 41 464 B (−688 B on every page)**; the
  console page types 50 893 → 50 205 B (ceiling 50 927 B, kept); the interior, login and home page types each 688 B
  lighter and more than 1 KB under their ceilings, which are lowered to the measured totals (plan §2.6 item 3:
  41 464, 46 325, 56 115 B). The area's own CSS is in three page-only sheets, loaded only by its pages: a content page
  45 520 B (+ `lettura.css` 4 056 B), an account page 43 890 B (+ `servizio.css` 2 426 B), an error page 45 093 B
  (+ `errori.css` 3 629 B, the door included) — recorded as measured (DL54-99 item 6; §2.6 item 5 not applied, and said).
- **The inventory and the capture report**: DS 2026 §2's two stale figures regenerated (components.css 28.0 KB,
  14 sections; `bd96a2e`); `capture-report.json` regenerated on lane 4 (`ef98cad`) — 43 captures, all as expected;
  the privacy page one icon more (the trail), the 404 one fewer (the redrawn page), nothing else changed.
- **The tests** (`TEST_DATABASE_URL=…/test_ile_v5_l4`, one pytest at a time, no run crashed): on the branch,
  **1 390 passed** without the browser (tests/i18n, tests/compliance, tests/security, the error pages in four
  languages with the 429, apps/accounts and the content apps, test_layout, test_design_docs, the two bundle-current
  tests, the static pipeline, O14, the chips' register, and W2-A's overlay test, the loader rules, the icons, the
  comments' leak test, the ownership and inventory scripts) and **60 passed** in the browser (tests/i18n's four RTL
  files and the family's two; no skip); on design-v5 after the merge, **333 passed** (the bundles, the design docs,
  the static pipeline, tests/security, the scripts' tests, the family's unit files). `ruff check` clean.

## On http://127.0.0.1:8780 (checked after the restart, by request only — no browser on the owner's server)

- http://127.0.0.1:8780/fr/ · http://127.0.0.1:8780/ar/ · http://127.0.0.1:8780/__design-v5/ — the strip names
  `v54/w3-f2`; the index lists the family as passed, with its review
  (http://127.0.0.1:8780/__design-v5/decisioni/w3-f2/REVIEW.md), and its 21 surfaces as «V5».
- **Content and legal pages** (fr; the same paths under `/ar/`): http://127.0.0.1:8780/fr/faq/ ·
  http://127.0.0.1:8780/fr/glossaire/ · http://127.0.0.1:8780/fr/glossaire/permesso_di_soggiorno/ ·
  http://127.0.0.1:8780/fr/partenaires/ · http://127.0.0.1:8780/fr/actualites/ ·
  http://127.0.0.1:8780/fr/vivre-en-italie/ · http://127.0.0.1:8780/fr/vivre-en-italie/logement/ ·
  http://127.0.0.1:8780/fr/contact/formulaire/ · http://127.0.0.1:8780/fr/entreprises/recueil-des-besoins/ ·
  http://127.0.0.1:8780/fr/collaboration/institutions/ · http://127.0.0.1:8780/fr/collaboration/universites-formation/ ·
  http://127.0.0.1:8780/fr/demande-transmise/?k=contact · http://127.0.0.1:8780/fr/privacy-policy/ ·
  http://127.0.0.1:8780/fr/cookie-policy/ · http://127.0.0.1:8780/fr/note-legali/ ·
  http://127.0.0.1:8780/fr/condizioni-di-utilizzo/ · http://127.0.0.1:8780/fr/avvertenze/
- **Error pages**: http://127.0.0.1:8780/__design-v5/stati/404/?lang=fr (also `ar`, `it`, `en`) ·
  http://127.0.0.1:8780/__design-v5/stati/429/?lang=fr (also `ar`, `it`, `en`) · http://127.0.0.1:8780/hello-world/
  (410) · the DEBUG URLconf's http://127.0.0.1:8780/_errors/400/, `/_errors/403/`, `/_errors/404/`, `/_errors/500/` ·
  the signed-in 403: «Entreprise — Cantiere Adriatico» (qa-company) →
  http://127.0.0.1:8780/fr/espace-reserve/entreprise/analyse-territoriale/. (Under DEBUG a mistyped address shows
  Django's technical 404; the preview's state page shows the product's.)
- **Account pages**: `/__design-v5/` → «Personas» → «Entrer» (no password; the preview's sessions are read-only), then
  http://127.0.0.1:8780/fr/compte/profil/ · http://127.0.0.1:8780/fr/compte/email/ ·
  http://127.0.0.1:8780/fr/compte/password/change/ · http://127.0.0.1:8780/fr/compte/2fa/ ·
  http://127.0.0.1:8780/fr/compte/profil/suppression/ · http://127.0.0.1:8780/fr/compte/logout/ (and under `/ar/`).

Checked after the restart (`C:/tmp/ile_v5_council/evidence/v54/w3-f2/merge/verify_8780.log`, `verify_8780_more.log`):
72 checks, 0 failures — the roots, the preview, its index and the review 200; every content and legal page above
200 in fr and ar with `cms/lettura.css` in its markup; the error pages with their status and `cms/errori.css`; through
the preview's own persona switch (qa-doc-person, then qa-company; «Sortir» after each), the six account pages 200 in fr
and ar with `cms/servizio.css`, and qa-company's 403 with the door. The server's log
(`.work/servers/srv8780.log`) holds no application traceback: its only tracebacks are Django's WARNING records of the
deliberate `PermissionDenied` behind that 403, and its only 500 is the `/_errors/500/` request.

## Not done

- **REVIEW m11** — one interior grammar for three partials: `_lettura.css`, `_servizio.css` and W3-F1's `_interior.css`
  restate the chapter, register and D26 values; the extraction waits for W3-F1 on design-v5 (≈ 0.4 KB out of
  `lettura.css`, the lever DL54-99 item 6 names). The V5 empty state is W3-E's component to take.
- **REVIEW m12** — the CSRF failure page stays Django's English page: its sentence is B1 copy (the owner's packet, the
  translators for ar); the self-sufficient frame is ready for it.
- **The deletion's confirmation on W2-A's alertdialog**: W2-A is on design-v5 now; moving the confirmation onto
  `overlay.js` (the page staying as the no-script fallback) is a change of `accounts/delete_request.html` and the
  profile's button — not done in this merge.
- **Handed to other families** (`NOTES.md` «For the merge», «Left, and for others»): W3-F1 — m8's rule for a head's
  Latin paragraph on the Arabic page (its review's m7); W2-C1 — the letterhead footer's «Privacy Policy» / «Cookie
  Policy» with `lang="en"`, and the signed-in letterhead's shift at 1440 (O1, with W4's performance sweep); W3-E — the
  empty-state component; W4-D — §27's last rules (`.account-panel__title`, `.account-table`) with their readers.
- **Words waiting for the owner (B1)**: the question headings and «Qui peut m’aider ?» above the live line (step 1's
  proposal in `NOTES.md`). Nothing of it is shipped: every word on these pages is live copy or a catalogue string.
- **Not measured**: the door's photograph on the error pages was not timed on the twin (the check's timing precedes
  the fix pass; DL54-99 item 6). Not checked at the merge: no browser on 8780 (by rule); Safari, Firefox, a real phone
  and a screen reader were never run. The Forum Virtuel's pages answer 404 in the preview (its flag is off on
  `ile_v5`), so the «community» surface is not marked.
- **The full suite** was not run (V5.5: the integration checkpoint runs it).
