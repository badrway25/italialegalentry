"""
The committed CSS bundle is the one its sources produce (scripts/build_css.mjs, `npm run build:css`).

`static/css/dist/` is versioned for the same reason as `static/js/dist/`: the production host runs
`collectstatic`, not Node, so a forgotten build would ship an old stylesheet and no Django test
would notice. Four checks, from the crude to the exact:

1. every entry point has its output (main.css and every app sheet);
2. no source was saved after its output (mtime — vacuous on a fresh clone, hence 3 and 4);
3. the output carries every custom property its sources define, and keeps no comment;
4. every url() in the output resolves, in the static namespace collectstatic builds, to a file that
   exists — the build rewrites them relative to the OUTPUT, and a wrong rewrite is a missing font.

A `_`-prefixed sheet is a partial (design V5, V5.4 plan §2.3, DL54-15): the build never makes it an
entry, it has no output of its own, and at least one sheet imports it.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STATIC = ROOT / "static"
DIST = STATIC / "css" / "dist"


# A custom property DEFINITION: `--name:` not glued to a word, so a BEM modifier followed by a
# pseudo-class (`.chip--dark :focus`, `.x--dense:hover`) is not mistaken for one.
_DEFINITION = re.compile(r"(?<![\w-])(--[a-zA-Z0-9-]+)\s*:")


def _strip_comments(css: str) -> str:
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def _main_sources() -> list[Path]:
    main = STATIC / "css" / "main.css"
    imports = re.findall(r'@import url\("([^"]+)"\)', main.read_text(encoding="utf-8"))
    return [main, *(STATIC / "css" / name for name in imports)]


def _is_partial(path: Path) -> bool:
    return path.name.startswith("_")


def _app_sheets() -> dict[Path, Path]:
    """source → output, for every app sheet that is not a partial (apps/<app>/static/<path> →
    static/css/dist/<path>)."""
    pairs = {}
    for source in (ROOT / "apps").glob("*/static/**/*.css"):
        if _is_partial(source):
            continue
        static_path = source.as_posix().split("/static/", 1)[1]
        pairs[source] = DIST / static_path
    assert pairs, "no app sheet found — the layout moved and this test did not"
    return pairs


def _partials() -> list[Path]:
    """Every `_`-prefixed sheet of the project's sources (static/css outside dist/ and dev/, the apps)."""
    found = [
        p for p in (STATIC / "css").rglob("_*.css") if not {"dist", "dev"} & set(p.relative_to(STATIC / "css").parts)
    ]
    return sorted([*found, *(ROOT / "apps").glob("*/static/**/_*.css")])


def _static_file(static_path: str) -> Path | None:
    for base in [STATIC, *(ROOT / "apps").glob("*/static")]:
        candidate = base / static_path
        if candidate.exists():
            return candidate
    return None


def test_every_entry_point_has_its_output():
    assert (DIST / "main.css").exists(), "no static/css/dist/main.css: run `npm run build:css`"
    for source, output in _app_sheets().items():
        assert output.exists(), f"{source.relative_to(ROOT)} has no bundle: run `npm run build:css`"


def test_no_source_is_newer_than_its_output():
    bundle = DIST / "main.css"
    newest = max(p.stat().st_mtime for p in _main_sources())
    assert bundle.stat().st_mtime >= newest - 1, (
        "static/css/dist/main.css is older than a source: run `npm run build:css`"
    )
    for source, output in _app_sheets().items():
        assert output.stat().st_mtime >= source.stat().st_mtime - 1, (
            f"{output.name} is older than {source.name}: rebuild"
        )


def test_the_outputs_keep_every_custom_property_and_no_comment():
    bundle = (DIST / "main.css").read_text(encoding="utf-8")
    assert "/*" not in bundle, "a comment survived the build"
    defined = set()
    for source in _main_sources():
        defined |= set(_DEFINITION.findall(_strip_comments(source.read_text(encoding="utf-8"))))
    missing = sorted(name for name in defined if f"{name}:" not in bundle)
    assert not missing, f"custom properties defined in the sources but absent from the bundle: {missing[:10]}"
    for source, output in _app_sheets().items():
        out = output.read_text(encoding="utf-8")
        assert "/*" not in out, f"a comment survived in {output.name}"
        for name in set(_DEFINITION.findall(_strip_comments(source.read_text(encoding="utf-8")))):
            assert f"{name}:" in out, f"{name} lost from {output.name}"


def test_every_url_in_the_outputs_resolves_to_a_static_file():
    outputs = [DIST / "main.css", *_app_sheets().values()]
    checked = 0
    for output in outputs:
        base = output.relative_to(STATIC).parent.as_posix()
        for target in re.findall(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)", output.read_text(encoding="utf-8")):
            if target.startswith(("#", "data:", "http:", "https:", "//")):
                continue
            parts = [*base.split("/"), *target.split("/")]
            resolved: list[str] = []
            for part in parts:
                if part == "..":
                    resolved.pop()
                elif part not in ("", "."):
                    resolved.append(part)
            static_path = "/".join(resolved)
            assert _static_file(static_path), f"{output.name}: url({target}) → {static_path} does not exist"
            checked += 1
    faces = len(
        re.findall(r"url\(", _strip_comments((STATIC / "css" / "v5" / "fonts.css").read_text(encoding="utf-8")))
    )
    assert faces >= 5, "static/css/v5/fonts.css declares fewer faces than type «Una voce» has"
    assert checked >= faces, "fewer url()s than the fonts alone declare — the check is not reading the bundle"


def test_a_partial_is_never_an_entry_and_always_imported():
    """`scripts/build_css.mjs` skips `_`-prefixed sheets as entries; the entries that draw them import them."""
    script = (ROOT / "scripts" / "build_css.mjs").read_text(encoding="utf-8")
    assert 'startsWith("_")' in script and "isPartial" in script, "the build lost the `_` partial rule"
    partials = _partials()
    assert STATIC / "css" / "_legacy-tokens.css" in partials, "the rule's first partial is the legacy shim"
    importers = [
        STATIC / "css" / "main.css",
        *(p for p in (STATIC / "css").rglob("*.css") if "dist" not in p.relative_to(STATIC / "css").parts),
        *(ROOT / "apps").glob("*/static/**/*.css"),
    ]
    imports = " ".join(_strip_comments(p.read_text(encoding="utf-8")) for p in importers)
    for partial in partials:
        static_path = partial.as_posix().split("/static/", 1)[1]
        assert not (DIST / static_path).exists(), f"{static_path} is a partial and has an output of its own"
        assert re.search(r'@import url\("[^"]*' + re.escape(partial.name) + r'"\)', imports), (
            f"{static_path} is a partial that no sheet imports"
        )
