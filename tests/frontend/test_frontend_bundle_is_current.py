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

The Motion library (motion.dev) left with W4-B (V5.4 plan §1.5 «Engine», §2.3, §3.6 item 2; DL54-101 item 4): its
last callers moved onto the platform — the Web Animations API through motion.js's gate — so the shared module exports
the gate and its helpers only, and neither the package files nor any bundle carry the library.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "static" / "js" / "src"
DIST = ROOT / "static" / "js" / "dist"


def _sources() -> list[Path]:
    found = list(SRC.rglob("*.js"))
    assert found, "no sources under static/js/src — the layout moved and this test did not"
    return found


def _inlined() -> set[str]:
    """The top-level modules scripts/build_frontend.mjs inlines into their one importer instead of bundling them."""
    script = (ROOT / "scripts" / "build_frontend.mjs").read_text(encoding="utf-8")
    listed = re.search(r"const INLINED = new Set\(\[([^\]]*)\]\)", script)
    assert listed, "scripts/build_frontend.mjs no longer declares INLINED"
    return set(re.findall(r'"([^"]+\.js)"', listed.group(1)))


def test_every_entry_point_has_a_bundle():
    inlined = _inlined()
    for entry in SRC.glob("*.js"):
        if entry.name in inlined:
            continue
        assert (DIST / entry.name).exists(), f"{entry.name} has no bundle: run `npm run build:js`"


def test_a_module_one_entry_imports_is_inlined_into_it_not_split():
    """W4-B (plan §2.6's request ratchet; W2-C1's A11Y_PERF item 5): nav.js lives inside shell.js and hero.js inside
    home.js — no stub of their own, no chunk of theirs fetched before `load` — and each has exactly one importer, the
    entry that carries it."""

    def imports(path: Path, name: str) -> bool:
        pattern = rf"""(?:from|import)\s*["']\./{re.escape(name)}["']"""
        return bool(re.search(pattern, path.read_text(encoding="utf-8")))

    importers = {name: [p.name for p in _sources() if imports(p, name)] for name in _inlined()}
    assert importers == {"nav.js": ["shell.js"], "hero.js": ["home.js"]}, importers
    assert not (DIST / "nav.js").exists() and not (DIST / "hero.js").exists(), "an inlined module has a stub of its own"
    assert "data-portico-architrave" in (DIST / "shell.js").read_text(encoding="utf-8"), "nav.js is not in shell.js"
    assert "[data-replay]" in (DIST / "home.js").read_text(encoding="utf-8"), "hero.js is not in home.js"


def test_no_source_is_newer_than_its_bundle():
    newest_source = max(p.stat().st_mtime for p in _sources())
    for bundle in DIST.glob("*.js"):
        assert bundle.stat().st_mtime >= newest_source - 1, (
            f"{bundle.name} is older than a source file: run `npm run build:js` and commit the result"
        )


def test_the_motion_bundle_carries_what_the_shared_module_exports():
    """
    Reads the OUTPUT, not the clock. The shared module exports the gate and its helpers; a bundle built before one of
    them was added or renamed does not export it.
    """
    source = (SRC / "motion.js").read_text(encoding="utf-8")
    # With code splitting the entry is a re-export and the helpers live in a shared chunk; what the browser receives is
    # both, so both are read.
    entry = (DIST / "motion.js").read_text(encoding="utf-8")
    bundle = entry + "".join(chunk.read_text(encoding="utf-8") for chunk in sorted((DIST / "chunks").glob("*.js")))

    helpers = set(re.findall(r"^export function (\w+)", source, re.M))
    assert {
        "reducedMotion",
        "withMotion",
        "play",
        "nextFrame",
        "afterPaint",
        "tween",
        "settled",
        "durationToken",
    } <= helpers
    # Minified names survive for exports: esbuild keeps the export surface intact.
    exports = re.search(r"export\{([^}]*)\}", entry)
    assert exports, "no export statement in the bundle — is it still an ES module?"
    exported = {name.split(" as ")[-1].strip() for name in exports.group(1).split(",")}
    for name in helpers:
        assert name in exported, f"{name} missing from the built bundle"

    # The one media query every animation must ask about.
    assert "prefers-reduced-motion" in bundle


def test_the_motion_library_is_gone_from_the_sources_the_packages_and_every_bundle():
    """
    W4-B removed the Motion library (V5.4 plan §3.6 item 2): no source imports it, the shared module re-exports none of
    its functions, the package files no longer declare it — `npm ci` would not install it —, and no output file carries
    its code, recognised by identifiers only the library writes.
    """
    for path in _sources():
        assert not re.search(
            r"""from\s*["']motion(?:/[^"']*)?["']|import\(\s*["']motion""", path.read_text(encoding="utf-8")
        ), f"{path.relative_to(ROOT).as_posix()} imports the Motion library"
    entry = (DIST / "motion.js").read_text(encoding="utf-8")
    exported = {name.split(" as ")[-1].strip() for name in re.search(r"export\{([^}]*)\}", entry).group(1).split(",")}
    assert not exported & {
        "animate",
        "scroll",
        "inView",
        "stagger",
        "spring",
        "hover",
        "press",
        "SPRING_SOFT",
        "SPRING_SNAPPY",
    }, exported

    package = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))
    for group in ("dependencies", "devDependencies"):
        assert "motion" not in package.get(group, {}), f"package.json still declares motion in {group}"
    lock = json.loads((ROOT / "package-lock.json").read_text(encoding="utf-8"))
    assert not [
        name
        for name in lock.get("packages", {})
        if name.split("node_modules/")[-1] in {"motion", "motion-dom", "motion-utils", "framer-motion"}
    ], "package-lock.json still pins the Motion library or its parts"

    outputs = [*DIST.glob("*.js"), *(DIST / "chunks").glob("*.js")]
    assert outputs, "no bundle under static/js/dist"
    for bundle in outputs:
        code = bundle.read_text(encoding="utf-8")
        for signature in (
            "staggerChildren",
            "spring-duration-limit",
            "value-not-animatable",
            "resolveKeyframes",
            "transformPerspective",
        ):
            assert signature not in code, f"{bundle.name} carries the Motion library ({signature})"
