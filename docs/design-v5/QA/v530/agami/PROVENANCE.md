# AGAMI — provenance of the page's material (V5.30 §8; lane v530-agami-build)

Internal record. The page shows no credit: every asset below is the promoter's own published institutional asset.
No personal data is recorded here: the files that show people are described by kind and count, never by name.

## 1 · The source pass (once, 7 November 2026)

| Source | What was read | Rule |
|---|---|---|
| The AGAMI website project (local, read-only) | its image folders only (`foto/`, `assets/`, `core/static/core/img/` incl. `brand/`) and, for public copy, its `locale/` catalogues | nothing of the project enters this repository except the two selected images, re-encoded; no database, contact record, document, credential, configuration or video was opened |
| https://agamieuromed.org/ | the home page in Italian, French, English and Arabic (read-only), and the three logo files the site publishes (to compare with the local originals) | public facts and published wording only |

## 2 · Selected and skipped

| Asset (kind) | Decision | Why |
|---|---|---|
| The official logo, framed form (`foto/logo-agami2.png`, 2 172 × 724, RGB, no metadata) | **selected** — `agami-insegna` | the best original of the mark the website publishes (its header and footer lockups are 615 and 1 100 px renderings of the same mark); AGAMI's own published asset |
| The official logo, round seal (`core/static/core/img/brand/agami-admin-logo.png`, 353 × 356, RGBA, lossless) | **selected** — `agami-sigillo` | the same seal the website publishes as `logo-agami-mark` (there re-compressed); AGAMI's own published asset |
| The website's header and footer lockups (615 × 144, 1 100 × 264, transparent) | not copied — compared only | lower resolution than the local framed original; the seal and the framed form cover the page's two uses |
| Twelve portrait photographs of named professionals (`foto/`) | **skipped** | personal data of third parties (the repository is public; V5.30 orchestrator's AGAMI privacy rule) |
| Eight round-table event photographs (`foto/`) | **skipped** | every frame shows identifiable private individuals — faces and legible personal name cards on the table; the only face-free crops (an audience seen from behind, chairs, a projected video-call screen, a roll-up banner carrying other organisations' logos and event data) still show legible name cards or third parties' logos and carry no institutional quality (V5.13 Q5: «A strong typographic/institutional composition without a photo is preferable to an irrelevant image») |
| One video (`foto/`) | **skipped** | no video (V5.30 orchestrator's rule) |
| `assets/incoming/` (a flyer and a logo of the Italy Legal Entry project itself) | **skipped** | not AGAMI's institutional imagery; the project's own brand already lives in `static/brand/` |
| The website's photographs under `/static/img/pexels/` | **skipped** | stock photography (not AGAMI's own; never stock pretending to be AGAMI) |
| The website's people and community photographs, its news cover | **skipped** | identifiable people |

No AGAMI photograph remains after the pass: the page's one image is the official logo (head) and its seal
(identification plate) — never a stock frame, never a drawing standing in for one.

## 3 · Facts and published wording used on the page

| On the page | Source |
|---|---|
| The role panel «En bref»: promoter of Italy Legal Entry™ and of the Forum Vénétie–Maroc; legal dialogue Italy – Morocco; active since 2011 | ILE's tracked copy: `p2.forum.who.body` («Le Forum est promu par AGAMI … active depuis 2011 dans le dialogue juridique entre l’Italie et le Maroc»), `faq_who` («Le projet est promu par AGAMI …»), the page's description string |
| The head's lead — «Du dialogue juridique à la coopération internationale» | AGAMI's own tagline, as published on agamieuromed.org in Italian, French, English and Arabic (the catalogue carries those four versions word for word; never a team translation) |
| The relationship band's lead — «Connaître ses racines pour construire des ponts entre les cultures, les ordres juridiques et les générations.» | AGAMI's own motto, as published on agamieuromed.org in the same four languages, with its quotation marks (French guillemets with no-break spaces) |
| The identification plate | the owner's Q9 decision (V5.23), unchanged, from `apps/pages/identity.py` and the site's constants — no field added |

Not used: the local project's planning documents (internal, not a publication source); any other statement of the website
(programmes, partnerships, events, people) — the page restates nothing it cannot point to.

## 4 · Rights basis and treatment

- **Rights basis:** AGAMI's own published institutional asset (the promoter's official logo, published by AGAMI on its
  website in the same forms); no third party's licence, no visible credit.
- **Treatment:** `tools/build_derivatives.py --marks` — none of the photographic grade; never cropped, recoloured or
  upscaled; Lanczos down to each width; AVIF (speed 4, 4:4:4, so the ribbon's thin red, green and gold strokes never
  bleed) + WebP; the seal's alpha kept; EXIF, XMP and ICC left out. Framed form 480 / 800 / 1 200 / 1 600 px under 60 KB
  each (the landing LCP budget); seal 176 / 264 / 353 px under 30 KB each. `static/brand/agami/PROVENANCE.json` records
  each source's hash and every file's hash, size and quality.
- **Display:** drawn whole and never mirrored — in Arabic too (the ribbon carries the two national flags: V5.29, the owner's
  correction of 6 November); the head's frame is the page's one LCP image (eager, `fetchpriority="high"`), the seal lazy and
  decorative (`alt=""`: the plate's words name the association).

## 5 · Checks done

- Originals: no EXIF, no GPS, no XMP; the framed original carries no ICC; its background is white (253–255), so it meets
  the plate's white without a seam.
- Derivatives: `tests/compliance/test_agami_assets_v530.py` — no EXIF/XMP/ICC/GPS in the decoded image nor in the container
  (the WebP chunk list, the AVIF item and colour boxes), every file listed and hashed, both formats at every width, under
  its ceiling, never upscaled, never cropped; the only AGAMI assets are the two logo forms from their two recorded sources;
  no portrait- or round-table-shaped file name anywhere in `static/`, no template pointing into the project's folders.
- The Q9 block: the same test module pins every field to the owner's text and finds no other identifier on the page.
