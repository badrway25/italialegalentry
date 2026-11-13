# W3-F2 · Content, legal, error and account pages — senior review (one pass)

Reviewer label `w3-f2-review` (built nothing). V5.5 delivery mode: one review, then fix, then ship. Branch `v54-w3-f2`
at `a420dad` (step 1 + step 2 and their notes), base `7d4ce79`. Looked at on the reviewer's own server from this
worktree (127.0.0.1:8884, `ile_v5_l4`, `ILE_REFERENCE_DATE=2026-10-03`, `DB_CONN_MAX_AGE=0`, `--noreload`,
`ILE_DESIGN_PREVIEW=1` only for the 429 / 404 states in four languages), headless Chromium with its own profile
(`.profiles/w3-f2-review/`), one browser at a time, no pytest (the a11y / perf lane holds `test_ile_v5_l4`). No run
ended on a crash; the server is stopped. Account pages through sessions minted with `Client.force_login` (qa-person,
seed-company, qa-fresh-person — no password used, typed or stored), revoked at the end (3 rows deleted). Evidence:
`C:/tmp/ile_v5_council/evidence/v54/w3-f2/review/` (`content/`, `account/`, `errors/`, `widths/`, `interact/`,
`ref/`, `crops/`, `metrics*.json`).

**Looked at.** The FAQ (+ results, + no result), the glossary and a term, the partners, the news (+ newsletter), «Vivre
en Italie» and a topic, the four enquiry forms and their answer, the five legal pages, the newsletter's confirmation
and unsubscription; the 400, 403 (anonymous and signed in), 404, 410, 429 and 500; the profile (person, company), the
e-mail addresses, the password, the second factor, the deletion request and its answer, the sign-out's confirmation.
fr and ar × 1440 × 900 and 390 × 844 (116 full pages), the errors also it and en (64), + 1366, 1024 and 360 for ten
fr and six ar pages (48). Interactions: the contact form, the newsletter and the deletion sent invalid (nothing
stored, nothing deleted), the FAQ by keyboard, the glossary's letter band, forced colours, reduced motion, the e-mail
removal's confirmation (dismissed: no POST). The full-text legal page, a sheet, an article and the Forum Virtuel for a
member were judged on the builder's TEST-content captures (`browser-test/`): the lane holds no legal version, no
sheet, no article and the Forum's flag is off. The home, the login and a door page captured as the reference.

## Verdict: **SHIP_AFTER_FIXES**

**The question — the same premium product as the hero, «Il portico» and the login, or V4 pages inside a V5 frame?**
Not V4 any more: the dashed boxes, the at-sign buttons, the 7rem numeral, the row arrows and the account menu floating
over its title are gone. The content and account pages speak the home's interior grammar — the trail, the head at the
reading edge, chapters with the `ile-steps` device, registers on hairlines, a quiet foot — and the account pages share
the login's form side (labels above, 52 px plates, one flat primary). They read as one calm, credible institutional
product, fr and ar, 1440 to 360, which is the right register for pages one reads and fills.

One family falls short of the bar: **the errors carry nothing of ILE** although the settled direction gives them the
brand's door (M1). Two defects must also go before shipping: Latin runs misaligned on the Arabic glossary and FAQ (M2)
and a newsletter refusal nobody sees (M3). All three are small, local fixes.

No P0: no broken page, no wrong direction, nothing unusable, no data or security problem.

## The gate, checked on the real pages

| Gate item | Result |
|---|---|
| FAQ on the system's accordion | yes — W1-C's `.accordion` on native `<details>`; Enter / Space open and close, the ring drawn, forced colours keep rules and chevrons, the chevron 0.2 s → 0 s under reduced motion. The glossary is a definition register (a `<dl>`, as in V4), not an accordion: the definitions stay visible — right for ten short entries |
| D26 slots, headings verbatim | the verification line only where a date exists (legal meta, sheet, term, article); one inset (the courtesy translation or the pending notice; the sheet's caution); one action; the authority's host beside its link («integrazionemigranti.gov.it»); «who can help me» in live words; headings verbatim, the reader's questions proposed for B1 only. Legal pages: see m3 |
| RH-1 … RH-8 | line-heights on the 4 px line; one section device at the reading edge; dense, then quiet (the quiet foot). RH-3 / RH-4 concern the home and the doors |
| Forms | typed text 16 px everywhere (contact, needs, collaboration, newsletter, profile, password, deletion); labels above; one primary; an error said by the 2 px edge, the drawn mark and the words, `aria-invalid` + `aria-describedby`; the system summary focused on the contact form and the deletion. The newsletter: M3 |
| Errors in four languages | 400 / 403 / 404 / 410 / 429 / 500 in fr, it, en, ar at 1440 and 390: the right status, one h1 in the request's language, one primary («Se connecter» for an anonymous 403), the way back, the way on, the help line; nothing revealed (no path, no stack; the 500's correlation id only, as before); the Arabic arrow mirrored. Identity: M1 |
| The 500 self-sufficient | yes — 400 and 500 render without the request (no context processor, no session; the recovery links are ungated routes and `flags` falls back to defaults on a `DatabaseError`), in a frame of static files; a bare page of the same words if the template fails |
| Account pages | one frame (trail, sections, page); the danger action behind its own page (password + mandatory box, «Annuler» first, the garnet button last; the profile's button is a link to it); allauth's address removal still asks (localized `confirm()`, nothing posted when dismissed); `noindex` |
| ≤ 3 corners a screen | 4 · 6 · full on every page and width (the 8 counted on account pages is the letterhead's closed account menu) |
| ≤ 6 glyphs in an editorial body | ≤ 3 (chapter mark, empty-state disc, the topic's glyph) |
| Health | 0 horizontal overflow, 0 CSP report, 0 console error (an error page's own status line apart) on ≈ 280 loads; no Arabic text under 14 px (only the lock-up's ™ is small); 0 animations and 0 `will-change` at rest |
| Security | the forms' processing, CSRF, honeypot / timing, throttles and recipients untouched (`enquiries/partials/form_shell.html` unchanged; every `csrf_token`, `action`, `name` kept); `button__manage.html` keeps every attribute of allauth's button; the one Python behaviour change is the 400 / 500 render (`apps/core/views.py`) |

**Shared payload (V5.8), measured on the merged tree** (design-v5 `d40f209` + this branch, built from clean in a
scratch worktree, removed): `dist/main.css` **41 817 → 41 155 B gzip (−662 B on every page)**; `console.css` and
`portal.css` byte-identical. Page-only sheets: `cms/lettura.css` 3 718 B (content pages), `cms/servizio.css` 2 340 B
(service pages).

## Blocking

None.

## Major — fix before the merge

**M1 · The error pages carry nothing of ILE, where the settled direction gives them the door.** The six errors are a
well-made typographic page (label, title, sentence, two buttons, links, help line) that any site could own — they
fail the swap test, and they are the one place of this area where the Creative Direction seats a brand act: «*The
door* (the owner's photograph inside the arch) lives on the hero, the login and the error pages» (CD §0 item 2;
brand act 1 «La porta … home hero, login, error pages (static)»; §1.4 law 5, the arch's allow-list; §20 «**Error
pages.** The door at rest with the key out of the lock, the message, three ways back»; DS V5 PX21 «Custom ILE»).
DL54-78 records no departure from it. **Fix (one direction):** the door at rest in the error head — the arch, the
owner's photograph as served, the key out of the lock, the three steps — from the assets that exist (W2-B's
`_door.css` stage, or `components/doorway.html` in its compact crop), imported by `_servizio.css` only (nothing on
`main.css`); static (no light, no motion — reduced motion is the same picture); never mirrored in Arabic; in the head's
end seat from 64rem, compact above the label on phones; the same markup in `errors/standalone.html` with static files
only, so the 500 stays self-sufficient (the bare fallback stays text). The message and the three ways back unchanged.

**M2 · Latin runs on the Arabic pages are aligned by accident of layout.** The glossary's Italian terms — Italian on
every language, so this outlives the translations — sit left-aligned inside the term column, 100–140 px off the
reading edge at 1024–1440 (`crops/gloss_ar_1440_register.png`, `gloss_ar_1024.png`), and at the far left of the
screen on phones under letters set on the right (`gloss_ar_390_top.png`). The FAQ's French questions zig-zag on
phones: one-line questions flush right, two-line questions flush left (`faq_ar_360_list.png`). The Forum Virtuel's
French-only room titles stand on the left under Arabic meta on the right (the builder's `forum-virtuel_member_ar_390`,
`crops/forum_member_ar_390_rooms.png`). Cause: `_lettura.css` gives every `[lang="fr"|"it"]` block `direction: ltr;
text-align: start` (l. 1298–1303) and restores the «end on the reading edge» rule only for `.page-header` and
`.chapter__head` heads (l. 1308). **Fix:** extend that head rule to the area's other heads — `.glossary-entry__term`,
`.faq-item__question`, `.registro__title` (`text-align: end`, the run keeping its own direction), or use the h1's run
pattern (the block keeps the page's direction, the words in `<span dir="ltr" lang>`); bodies keep their own start.
Add the browser assertion (Arabic, 1440 and 390: each term's and room title's inline-end edge on its cell's; each
question's on its row's).

**M3 · A newsletter refusal is invisible.** Sent without the consent, the view renders `/actualites/` again at the
top: no message there, the error sits under the fold (≈ 990 px at 1440, far lower on a phone), nothing is focused,
and a `role="alert"` present at load is not announced (`interact/nl-err2_fr_1440__top.png`, `nl-err2_ar_390*`). The
contact form and the deletion land on the system summary (`#form-errors`, focused and scrolled by `main.js`
`initFormErrorFocus`); `news/_newsletter.html` has no summary (V4 had none either, but the form is in this family's
gate). **Fix:** `{% include "components/form_errors.html" with form=newsletter_form %}` at the top of the newsletter
form — the system's pattern, so the page lands on the refusal in every language; keep the field's error. A test: an
invalid POST renders `id="form-errors"` inside `#newsletter`.

## Minor — polish

- **m1** The glossary's letter band wraps at 390 and 360 with «V» alone on a second line (fr, ar): eight 44 px
  targets fit 358 px — tighten the gap, or set the band as equal cells so a longer alphabet wraps by design.
- **m2** Rows whose whole surface is a link read as static text at rest on a touch screen — «Vivre en Italie»'s topics,
  the Forum Virtuel's rooms, the account's «Sécurité» rows: ink, no underline (the cue comes on hover only), while the
  glossary's terms and the quiet foot's links in the same area are underlined teal. Give a row's title the link's
  resting cue (no glyph: the six-icon ceiling stands).
- **m3** The legal pages have no trail (every other page of the area has one), and in the full-text state the
  verification line hugs the h1 (≈ 8 px): give them the trail and the `.verifica` spacing of the sheets and terms.
  When the official texts arrive, a long text wants «Sur cette page» (PX24).
- **m4** The newsletter's confirmation and unsubscription answers are dead ends — a title and one sentence («Inscription
  confirmée.»), no way on, no «who can help me»: add «Retour à l'accueil» and the help line (live strings).
- **m5** Double rules: a group's closing hairline, an empty band, the next group's opening rule — the glossary's letter
  groups, the profile's «Sécurité» list → «Organisations». Keep one. On `/compte/email/` at 1440 (fr) the three plates
  wrap with «Enlever» alone on a second line: let the action row take the body's width or set the danger apart on
  purpose.
- **m6** The contact form shows two titles in a row — the chapter's «Votre message», then the legend «Vos coordonnées
  et votre message» (stark at 390 / 360): one of them is enough on screen (the legend can stay for assistive
  technology).
- **m7** The news' category filter is drawn over an empty news index (four filters, zero articles): hide it while there
  is no article at all.
- **m8** On the Arabic pages a long French lead (fallback) is end-aligned and ragged on the left — «Vivre en Italie» 7
  lines at 1440, the Forum Virtuel. Heads keep the end; a lead longer than two lines keeps its own start, as bodies do —
  the same rule W3-F1's review asks (its m7): one rule for both families, through the steward.
- **m9** The anonymous 403's «Se connecter» drops the refused address: add `?next=` (allauth checks it is local) so the
  person lands back where they were going.
- **m10** On a topic page the topic's glyph sits beside the eyebrow «Vivre en Italie», where a house reads as «home» for
  the section: set it with the topic's title or drop it.
- **m11** The interior grammar is drawn three times — W3-F1's `_interior.css`, `_lettura.css`, and `_servizio.css`'s
  restated trail, empty state and help line. Page-only, so the shared payload is safe, but V5.8 asks for no duplicated
  families: once W3-F1 is on design-v5, extract the common part into one page-only partial the three entries import
  (the builder's own follow-up), and hand the V5 empty state to W3-E's component.
- **m12** The CSRF failure (Django's English default page) is still the one error a person can meet outside this family:
  the builder parked it as B1 copy — keep it on the owner's packet.

## What holds — keep it through the fixes

- One interior grammar for twenty-odd page types, coherent with the home's chapters and the login's form side; no V4
  left.
- The forms: 16 px, labels above, 52 px plates, one primary, errors in edge + mark + words, the summary focused.
- The FAQ on the system's accordion; the glossary's register and its sticky letter band (a letter lands under it).
- D26's slots built for real; headings verbatim; nothing new promised.
- The errors: calm, useful, four languages, nothing revealed; 400 / 500 truly self-sufficient, with a bare fallback.
- The account frame: one list of sections, the danger action behind its own confirmation, allauth's flows intact.
- The Arabic composition of heads, trails, registers, forms and errors (apart from M2).
- −0.66 KB on every page, the area's own CSS in page-only sheets.

## For the merge (the steward)

- `docs/design-v5/DECISION_LOG_V54.md`: DL54-78 collides with W3-B's DL54-78 … 87 on design-v5 — renumber (the
  merge conflicts there and on the binary `dist/main.css`, rebuilt from clean).
- `check_ownership.py w3-f2 design-v5`: 48 inside, 4 slice, 3 generated, **7 outside**, all justified in NOTES:
  `static/css/v5/_lettura.css`, `_servizio.css`, `apps/cms/static/cms/{lettura,servizio}.css`,
  `apps/cms/templatetags/lettura.py`, `apps/living/catalogue.py`, and `apps/core/views.py` — assign the last one
  knowingly: it changes how the 400 and 500 handlers render.
- Page-type CSS after the merge: a content page 41 155 + 3 718 = **44 873 B**, 387 B over the Wave-1 interior ceiling
  (44 486 B) while the shared payload falls by 662 B — the page-only sheet is where V5.8 wants it; record it (as
  DL54-44, -73, -76). A service page 43 495 B, under.

## Other areas, seen on the way

- `/fr/contact/` (W3-F1's `templates/pages/contact.html`, still V4's grammar on this branch: row arrows, the at-sign, a
  side list) is the door to this family's `/fr/contact/formulaire/`: judge the pair together once W3-F1 lands.
- The portico marks «Personnes» current on the FAQ, the glossary and «Vivre en Italie», «Projet» on the news and the
  contact pages (W2-C1's mapping; W3-F1's review m8 covers its double marks).

## Runs

| Run | Result |
|---|---|
| Content pages: 21 × fr, ar × 1440, 390 | 84 loads: 0 overflow, 0 CSP, 0 console error; ≤ 3 radii; fields 16 px |
| Account pages (minted sessions, revoked): 8 × fr, ar × 1440, 390 | 32 loads: the same; one primary or one danger a page |
| Errors: 400, 403 ×2, 404 ×2, 410, 429, 500 × fr, it, en, ar × 1440, 390 | 64 loads: right status and language, one h1, nothing revealed |
| Widths: 10 fr + 6 ar pages × 1366, 1024, 360 | 48 loads: 0 overflow, 0 CSP |
| Interactions (contact, newsletter after the 3-s floor, deletion — invalid; FAQ keyboard; letter band; forced colours) | M2, M3, m1, m5, m6 |
| Probes: small text (14 loads), motion at rest and reduced (12), e-mail removal confirm (2) | Arabic ≥ 14 px; 0 animations; the confirm shown, 0 POST |
| Merged tree built from clean in a scratch worktree (removed) | `main.css` 41 817 → 41 155 B gzip; console bundles byte-identical |
| `check_ownership.py w3-f2 design-v5` | 7 paths outside the slice, justified (above) |

The scratch scripts are in `C:/tmp/ile_v5_council/.work/w3-f2/w3-f2-review/`.
