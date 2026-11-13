"""
The static pipeline holds under the storage production runs `collectstatic` with.

config/settings/base.py stores static files with WhiteNoise's CompressedManifestStaticFilesStorage; dev.py and test.py
swap in StaticFilesStorage, so no local run ever post-processes anything. The manifest storage reads EVERY collected CSS
file, the raw source sheets as well as the dist the templates link, comments included, and resolves each url() and
@import from where that file lands in the collected tree. A reference written as a source-tree path
(`../../../../static/css/v5/_loader-light.css` from apps/portal/static/portal/console.css) climbs out of STATIC_ROOT
there, and collectstatic stops with SuspiciousFileOperation: a deployment that cannot finish. esbuild resolved the same
path without complaint, so the dist was right and nothing local noticed (steward, 11 October 2026).

The convention (DS 2026 §2, beside the `_` partial rule; scripts/build_css.mjs enforces it on the bundle): every @import
and url() of a source sheet is written as it resolves in the COLLECTED tree (static/<p> → <p>, apps/<app>/static/<p>
→ <p>), from the sheet's own collected path. A partial of static/css/v5/ is `../css/v5/_x.css` from an app's
<app>/<sheet>.css, `../../css/v5/_x.css` from pages/css/hero.css.

1. every reference of every source sheet lands, in the collected tree, on exactly one source file: no server, no
   database, milliseconds. This is the check that fails CI on the next cross-boundary import;
2. the check refuses the source-tree form and accepts the collected one;
3. one real `collectstatic` under the production storage, into a temporary directory, exits 0 and hashes every bundle.
   CI has no Node: it runs on the committed dist, as the production host does.
"""

from __future__ import annotations

import json
import os
import posixpath
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urldefrag, urlsplit

from django.contrib.staticfiles.storage import HashedFilesMixin

ROOT = Path(__file__).resolve().parents[2]
STATIC = ROOT / "static"

#: The CSS patterns the manifest storage rewrites, taken from the storage itself rather than copied: every url(…),
#: `@import url(…)` included, the bare `@import "…"`, and a source-map comment. They run on the raw text, comments
#: included, and Django compiles them case-insensitive.
_CSS_PATTERNS = [
    re.compile(entry if isinstance(entry, str) else entry[0], re.IGNORECASE)
    for entry in dict(HashedFilesMixin.patterns)["*.css"]
]


def _static_roots() -> list[Path]:
    """The project's directories that collectstatic merges, in the order Django's finders read them: STATICFILES_DIRS
    (static/), then each app's static/. Third-party apps add their own trees, which no sheet of ours draws on."""
    return [STATIC, *sorted(p for p in (ROOT / "apps").glob("*/static") if p.is_dir())]


def _collected_path(sheet: Path, roots: list[Path]) -> str:
    for root in roots:
        if sheet.is_relative_to(root):
            return sheet.relative_to(root).as_posix()
    raise AssertionError(f"{sheet} is under no static directory")


def _source_sheets(roots: list[Path]) -> list[Path]:
    """Every CSS file of those directories outside the build outputs (any `dist/`): the main cascade and its layers,
    the partials, the app entries, the development sheets. All of them are collected and post-processed."""
    return sorted(
        sheet for root in roots for sheet in root.rglob("*.css") if "dist" not in sheet.relative_to(root).parts
    )


def _references(css: str) -> list[str]:
    return [match.group("url") for pattern in _CSS_PATTERNS for match in pattern.finditer(css)]


def _problem(collected_from: str, url: str, roots: list[Path]) -> str | None:
    """Why `url`, written in the sheet collected at `collected_from`, does not hold in the collected tree, or None.
    What the storage's converter leaves alone (a scheme, `//`, a bare fragment) is left alone here too."""
    if re.match(r"^[a-z]+:", url) or url.startswith("//"):
        return None
    url_path = urldefrag(url)[0]
    if not url_path:
        return None
    if url_path.startswith("/"):
        return "an absolute path: write it relative to this sheet, as it resolves in the collected tree"
    joined = posixpath.join(posixpath.dirname(collected_from), url_path)
    target = posixpath.normpath(urlsplit(unquote(joined)).path.strip())
    if target == ".." or target.startswith("../"):
        return f"leaves the collected tree ({target}): a source-tree path, on which collectstatic stops"
    homes = [root for root in roots if (root / target).is_file()]
    if not homes:
        return f"nothing is collected at {target}"
    if len(homes) > 1:
        return f"{target} is collected from {len(homes)} static directories: give it one"
    return None


def test_every_reference_of_every_source_sheet_resolves_in_the_collected_tree():
    roots = _static_roots()
    problems = []
    checked = 0
    for sheet in _source_sheets(roots):
        here = _collected_path(sheet, roots)
        for url in _references(sheet.read_text(encoding="utf-8")):
            checked += 1
            problem = _problem(here, url, roots)
            if problem:
                problems.append(f"{sheet.relative_to(ROOT).as_posix()}: {url!r}: {problem}")
    assert not problems, (
        "references that do not hold in the collected tree (DS 2026 §2: write each one as it resolves there, from the "
        "sheet's own collected path; comments count, the manifest storage reads them):\n" + "\n".join(problems)
    )
    main_imports = len(re.findall(r"@import", (STATIC / "css" / "main.css").read_text(encoding="utf-8")))
    assert checked > main_imports, "fewer references than main.css alone imports: the check is not reading the sheets"


def test_the_check_refuses_a_source_tree_path_and_accepts_the_collected_one():
    roots = _static_roots()
    # An app entry importing a partial of static/css/v5/ through the source tree (W2-B's entrance, as first written)
    refused = _problem("accounts/entrance.css", "../../../../static/css/v5/_door.css", roots)
    assert refused and refused.startswith("leaves the collected tree"), refused
    # the same import in the collected tree, from an app entry, from the home's page sheet, from the console entry
    assert _problem("accounts/entrance.css", "../css/v5/_loader-light.css", roots) is None
    assert _problem("pages/css/hero.css", "../../css/v5/_loader-light.css", roots) is None
    assert _problem("portal/console.css", "v5/_shell.css", roots) is None
    missing = _problem("portal/console.css", "v5/_absent.css", roots)
    assert missing == "nothing is collected at portal/v5/_absent.css", missing
    assert (_problem("css/v5/fonts.css", "/static/fonts/x.woff2", roots) or "").startswith("an absolute path")
    for left_alone in ("data:image/svg+xml,%3Csvg%3E", "https://example.invalid/x.css", "//cdn.invalid/x", "#mark"):
        assert _problem("css/main.css", left_alone, roots) is None, left_alone


def test_collectstatic_under_the_production_storage_exits_0(tmp_path):
    """The base settings, which carry production's storage exactly as base.py declares it, with STATIC_ROOT moved into
    the test's temporary directory. A subprocess, so that the swap test.py makes never reaches it."""
    static_root = tmp_path / "static_root"
    (tmp_path / "static_pipeline_settings.py").write_bytes(
        b'"""Written by tests/frontend/test_static_pipeline.py: base.py\'s storage, a temporary STATIC_ROOT."""\n'
        b"from config.settings.base import *  # noqa: F401,F403\n\n" + f"STATIC_ROOT = {str(static_root)!r}\n".encode()
    )
    env = {
        **os.environ,
        "DJANGO_SETTINGS_MODULE": "static_pipeline_settings",
        "PYTHONPATH": os.pathsep.join(filter(None, [str(tmp_path), str(ROOT), os.environ.get("PYTHONPATH")])),
        "PYTHONIOENCODING": "utf-8",
    }
    run = subprocess.run(
        [sys.executable, str(ROOT / "manage.py"), "collectstatic", "--noinput"],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=600,
        check=False,
    )
    assert run.returncode == 0, (
        f"collectstatic fails under the production storage:\n{(run.stdout + run.stderr)[-4000:]}"
    )
    manifest = json.loads((static_root / "staticfiles.json").read_text(encoding="utf-8"))["paths"]
    bundles = sorted(p.relative_to(STATIC).as_posix() for p in (STATIC / "css" / "dist").rglob("*.css"))
    assert "css/dist/main.css" in bundles and "css/dist/portal/console.css" in bundles, bundles
    for bundle in bundles:
        assert bundle in manifest and (static_root / manifest[bundle]).is_file(), f"{bundle} was not hashed"
