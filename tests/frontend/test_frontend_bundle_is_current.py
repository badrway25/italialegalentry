"""
The committed bundle is not older than the sources it was built from.

`static/js/dist/` is versioned because the production host runs `collectstatic`, not Node: what
the browser receives has to be in the repository already. That makes a forgotten `npm run
build:js` invisible — the sources say one thing, the served file says another, and nothing in a
Django test suite notices, because nothing in it executes JavaScript.

This test compares modification times, which is crude and sufficient: a source saved after the
bundle was written is a bundle that needs rebuilding. Git does not preserve mtimes on checkout, so
on a fresh clone every file is "new" and the comparison is vacuous — which is why the second test
exists: it reads the bundle and checks that it contains what the shared module exports. A stale
bundle from before an export was added fails that one whatever the clock says.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "static" / "js" / "src"
DIST = ROOT / "static" / "js" / "dist"


def _sources() -> list[Path]:
    found = list(SRC.rglob("*.js"))
    assert found, "no sources under static/js/src — the layout moved and this test did not"
    return found


def test_every_entry_point_has_a_bundle():
    for entry in SRC.glob("*.js"):
        assert (DIST / entry.name).exists(), f"{entry.name} has no bundle: run `npm run build:js`"


def test_no_source_is_newer_than_its_bundle():
    newest_source = max(p.stat().st_mtime for p in _sources())
    for bundle in DIST.glob("*.js"):
        assert bundle.stat().st_mtime >= newest_source - 1, (
            f"{bundle.name} is older than a source file: run `npm run build:js` and commit the result"
        )


def test_the_motion_bundle_carries_what_the_shared_module_exports():
    """
    Reads the OUTPUT, not the clock. The shared module re-exports a fixed list from Motion and
    adds two helpers of its own; a bundle built before either changed does not contain them.
    """
    source = (SRC / "motion.js").read_text(encoding="utf-8")
    # With code splitting the entry is a re-export and the library lives in a shared chunk; what
    # the browser receives is both, so both are read.
    bundle = (DIST / "motion.js").read_text(encoding="utf-8") + "".join(
        chunk.read_text(encoding="utf-8") for chunk in sorted((DIST / "chunks").glob("*.js"))
    )

    helpers = re.findall(r"^export function (\w+)", source, re.M)
    assert {"reducedMotion", "withMotion"} <= set(helpers)
    # Minified names survive for exports: esbuild keeps the export surface intact.
    exports = re.search(r"export\{([^}]*)\}", bundle)
    assert exports, "no export statement in the bundle — is it still an ES module?"
    exported = {name.split(" as ")[-1].strip() for name in exports.group(1).split(",")}
    for name in ("animate", "scroll", "inView", "stagger", *helpers):
        assert name in exported, f"{name} missing from the built bundle"

    # The one media query every animation must ask about.
    assert "prefers-reduced-motion" in bundle
