# static/img/flags — the language control's flags

Four plates — three flags and, for Arabic, a language mark (see below) — drawn by the project team as original SVG code for the header's language control and the phone sheet's
(V5.31 final precision pass, 11 Nov 2026). No file was downloaded or copied: each is a few paths written from the
public specification of a national flag (a flag's design is not a copyrightable work; no third-party artwork is used).
One 3:2 box for the four so the control reads as one set; shown at 21 x 14 px with a hairline ring and a 3 px radius
given by the stylesheet (`.flag`, static/css/v5/chrome.css). Never mirrored in a right-to-left page (an `<img>`).

| file   | flag           | used for | drawn from |
|--------|----------------|----------|------------|
| fr.svg | France         | Français | three equal vertical bands, #000091 / #fff / #e1000f (the State's 2020 colours) |
| it.svg | Italy          | Italiano | three equal vertical bands, #008c45 / #f4f5f0 / #cd212a (Presidency of the Council, 2006) |
| gb.svg | United Kingdom | English  | the Union Flag's standard 60 x 30 construction (#012169, #fff, #c8102e), its central 45 x 30 shown so it takes the same 3:2 box |
| ma.svg | Morocco        | العربية  | red field #c1272d, the green (#006233) five-pointed star as an outlined pentagram, drawn a little larger than the specification's circle (17/90 of the length for 1/6) so it still reads at 21 px; the interlacing of the star's branches is not drawn at this size |

| ar.svg | — (a language mark, not a flag) | العربية | a mineral plate #e9e5dd, the letter ʿayn «ع» drawn as one stroked path (#1d2a3a, round caps) in the flags' 30 x 20 frame; drawn by the project team, no font or third-party artwork embedded |

`ma.svg` stays in the folder (the drawing is correct) but no language uses it any more.

THE MAPPING language -> flag is ONE place: `LANGUAGE_FLAGS` in apps/core/context_processors.py.

## Which languages are a country? (V5.31 art pass, 11 Nov 2026, B6 — the evidence)

A flag names a country; a language page earns one only when the page is written for that country. Checked:

| page | locale (config/settings/base.py `LANGUAGES`) | written as (docs/I18N_RTL.md §4.2, the catalogues) | treatment |
|------|------|------|------|
| /it/ | `it`, «Italiano» | Italian institutional register (PA usage) — the language of the country the platform serves | Italy's flag |
| /fr/ | `fr`, «Français» | the source language of every supplied text (ADR-004), French of France | France's flag |
| /en/ | `en` (no region), «English» | «britannico istituzionale sobrio» — British spelling throughout the catalogue (`organisation`, `authorised`, `authorisation`, `anonymised`) | the United Kingdom's flag: its spelling is the UK's |
| /ar/ | `ar` (no region — not `ar-MA`), «العربية» (not «الدارجة» or a Moroccan name) | «arabo standard moderno» (Modern Standard Arabic), an institutional register that borrows Moroccan administrative words (`التكوين`, `المسطرة`) — readable by every Arabic reader, not a Moroccan dialect | a NEUTRAL language mark («ع»): Arabic is the language of many countries and the page is not written for one; equating it with Morocco would tell an Arabic reader from elsewhere the page is not for them |

The earlier choice (precision pass, 11 Nov 2026: Arabic -> Morocco, «the Arabic audience is Moroccan») was a product
assumption, not something the locale or the text declares; it is withdrawn. If the owner decides the Arabic pages ARE
for Morocco (and says so, e.g. an `ar-MA` locale or a Moroccan-dialect register), the one mapping line points back to
`ma`. Flags and the mark are `<img>`s: never mirrored in a right-to-left page.
