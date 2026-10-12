# Specimen boards — `templates/dev/designpreview/specimens/`

The foundation families' specimen boards (V5.4 plan `docs/design-v5/V5_4_EXECUTION_PLAN.md` §2.3
«Templates» and §3.1 item 6): the boards on which W1-A, W1-B, W1-C and W1-D are scored before their
propagation. Each board is one template in this folder, `<board>.html`, served in development only at
`/__design-v5/specimens/<board>/` by `designpreview.views.specimen`. A name without a template here
answers 404.

**No board exists yet.** W1-0 made the route and this folder; each family writes its own boards, in
its own slice of `docs/design-v5/OWNERSHIP_V54.json`:

| Board | Family | Template |
|---|---|---|
| the type specimen | W1-A | `type.html` |
| the colour register board | W1-A | `colour.html` |
| the corner and shadow board | W1-A | `corners.html` |
| the icon sheet | W1-B | `icons.html` |
| the loader filmstrips | W1-D | `loader.html` |
| the chip board | W1-C | `chips.html` |
| the button set | W1-C | `buttons.html` |
| the field set | W1-C | `fields.html` |

## What a board's template may rely on

- **Its name is a slug**: lower-case letters and digits, in words joined by single hyphens, at most
  64 characters (`type`, `colour`, `chip-board`). Anything else — capitals, underscores, dots, a
  doubled or trailing hyphen — is a 404, never a template path.
- **It is a standalone document.** The board is rendered without the request's context processors,
  so it reads nothing from the database: `request`, `user`, the site settings and the CMS menus are
  not there. It does not extend `base.html` (whose partials read the database); it writes its whole
  document and loads the product's own files with `{% static %}` — `css/dist/main.css`, the page or
  console sheet it demonstrates, the script entries it needs (`type="module"`). Its context holds one
  variable, `board`.
- **The chrome is Italian, the samples are real.** It renders under `translation.override("it")`,
  with `Content-Language: it`. Product text shown in French or Arabic carries its own `lang` — and
  `dir="rtl"` for Arabic — on the element that holds it. Locked copy stays verbatim.
- **The site's policy, unwidened.** The response carries the site's Content-Security-Policy as it is:
  no `style` attribute, no `<style>` or inline `<script>`, no `on…=` handler, nothing remote, no
  hotlinked font or image. A board frames nothing and cannot be framed. Like every preview page it
  answers with `X-Robots-Tag: noindex, nofollow` and `Cache-Control: no-store`.
- **Development only.** The route exists when `DEBUG` and `ILE_DESIGN_PREVIEW=1` both hold, answers
  the loopback interface only, GET and HEAD only, and never opens a transaction.

Files here are written with LF line endings. The route and its tests:
`apps/designpreview/views.py` (`specimen`), `tests/frontend/test_design_preview.py`.
