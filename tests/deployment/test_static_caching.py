"""
Every file a page can load is cached by its content, or for minutes at most — never a plain name for a year.

The templates link each script, style and image through {% static %}, so the browser asks for its hashed name, and
WhiteNoise serves a hashed name as immutable for ten years. What a page loads next is not in a template: the ES modules
of static/js/dist import one another — the shared chunks, and the entries loaded on demand (loader.js from shell.js and
from a chunk, depot.js and piece-drawer.js from console.js) — and the stylesheets name their fonts and images. Until
16 October 2026 the manifest storage rewrote a stylesheet's url() but not a module's imports: the browser asked for ten
of the 48 files the templates reach under their plain names, and base.py's WHITENOISE_MAX_AGE served a plain name for a
year — after a release, a returning browser could run last release's modules with the new pages (the review of
integration checkpoint 3, «outside this branch»; the DevOps lane's second pass, item 1, docs/design-v5/QA/v54/devops).

One real collectstatic, as runbook step 8 runs it — the production settings with the runbook's environment, into an
empty STATIC_ROOT — then:

1. it exits 0 (DL54-44 recorded it failing under the production storage on 10 October);
2. from every file a template names, the import graph is followed through the collected tree as the browser receives
   it: every file reached is a hashed name, answered 200 by WhiteNoise under the production settings, `immutable`;
3. every import of every collected module is the hashed name of the file its source imports: each one rewritten, none
   left as written, none pointing at nothing — on the real minified dist; and no script outside static/js/dist is
   rewritten by the module patterns (core.storage.MODULES);
4. the plain name of each of those files — what a browser would receive if a specifier ever escaped the rewriting — is
   cached for minutes at most.

Then a release, as runbook step 15 runs it — collectstatic again into the same STATIC_ROOT, never --clear — on the
bundles of static/js/dist alone, loader.js changed in place: its importers are renamed and nothing else, every file of
the previous release survives byte for byte, and each release's graph holds hashed names of that release only (5).

And, with no collectstatic at all (milliseconds), from the files the finders list and the storage's own patterns (the
review of the second pass, REVIEW_2 m3 and m6): every reference the storage rewrites names a collected file (6), and in
no directory order does a chain of references need more passes than Django's post-processing runs (7) — the order
follows the directory listing, sorted on NTFS and in hash order on ext4, so a dist that collects here could otherwise
stop with «Max post-process passes exceeded» on the server.
"""

from __future__ import annotations

import json
import os
import posixpath
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urldefrag, urlsplit

import pytest
from django.apps import apps
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import HashedFilesMixin
from django.contrib.staticfiles.utils import matches_patterns

from core.storage import MODULES, CompressedManifestModulesStorage
from tests.deployment.test_production_checks import RUNBOOK_ENVIRONMENT, TEMPLATE_HSTS

ROOT = Path(__file__).resolve().parents[2]
DIST = ROOT / "static" / "js" / "dist"
STATIC_URL = "/static/"

#: The ceiling, in seconds, on the cache of a file whose name does not change with its content.
SHORT_MAX_AGE = 300

#: The passes after its first that a file's hashed name may need to settle: Django's post-processing runs
#: max_post_process_passes more and needs the last of them to change nothing (HashedFilesMixin.post_process).
PASSES_ALLOWED = HashedFilesMixin.max_post_process_passes - 1
#: The model's answer for a file on a cycle, or one importing a file on a cycle: its name never settles.
NEVER = 10**6

STATIC_TAG = re.compile(r"""\{%\s*static\s+["']([^"']+)["']""")
#: The specifiers of an ES module, minified (esbuild) or not: `import{a as b}from"./c.js"`, `export{a}from"./c.js"`,
#: `import"./c.js"` and the dynamic `import("./c.js")`.
JS_FROM = re.compile(r"""\b(?:import|export)\b[^;"'`()]*?\bfrom\s*(["'])(?P<spec>[^"'\n]+)\1""")
JS_BARE = re.compile(r"""\bimport\s*(["'])(?P<spec>[^"'\n]+)\1""")
JS_DYNAMIC = re.compile(r"""\bimport\s*\(\s*(["'`])(?P<spec>[^"'`\n]+)\1\s*\)""")
#: A dynamic import whose argument is not a string literal: no storage can rewrite it, no test can follow it.
JS_COMPUTED = re.compile(r"""\bimport\s*\((?!\s*["'`])""")
CSS_REF = re.compile(r"""url\(\s*(["']?)(?P<spec>[^"')]+?)\1\s*\)|@import\s+(["'])(?P<imp>[^"']+)\3""")


def _js_specifiers(text: str) -> list[str]:
    found = [(m.start(), m.group("spec")) for pattern in (JS_FROM, JS_BARE, JS_DYNAMIC) for m in pattern.finditer(text)]
    return [spec for _start, spec in sorted(found)]


def _css_references(text: str) -> list[str]:
    return [m.group("spec") or m.group("imp") for m in CSS_REF.finditer(text)]


def _local(spec: str) -> str | None:
    """The path part of a reference to a file of this site, or None (a scheme, `//`, a bare fragment)."""
    if re.match(r"^[a-z][a-z0-9+.-]*:", spec, flags=re.IGNORECASE) or spec.startswith("//"):
        return None
    return spec.split("#")[0].split("?")[0] or None


def _resolve(base: str, spec: str) -> str:
    """Where the browser goes: `spec` read from the file at path `base` (a URL path or a collected name)."""
    return spec if spec.startswith("/") else posixpath.normpath(posixpath.join(posixpath.dirname(base), spec))


def _templates() -> list[Path]:
    homes = [ROOT / "templates", *sorted((ROOT / "apps").glob("*/templates"))]
    return sorted(path for home in homes for path in home.rglob("*") if path.suffix in {".html", ".txt", ".xml"})


def _production_env(workdir: Path, settings_module: str) -> dict[str, str]:
    """The runbook's environment for a settings module written into `workdir` (a subprocess: the test settings of this
    process never reach it)."""
    env = {
        **os.environ,
        **RUNBOOK_ENVIRONMENT,
        **TEMPLATE_HSTS,
        # Nothing here needs a database: WhiteNoise answers a static URL before any view. A dead address makes sure of
        # it — a URL WhiteNoise did not know would reach the views and fail there, never read a real database.
        "DATABASE_URL": "postgres://unused:unused@127.0.0.1:9/no_database",
        "DJANGO_SETTINGS_MODULE": settings_module,
        "PYTHONPATH": os.pathsep.join(filter(None, [str(workdir), str(ROOT), os.environ.get("PYTHONPATH")])),
        "PYTHONIOENCODING": "utf-8",
    }
    for name in ("ILE_ALLOW_INSECURE_PROD", "ILE_READ_ENV_FILE", "SECURE_SSL_REDIRECT", "DJANGO_ALLOW_ASYNC_UNSAFE"):
        env.pop(name, None)
    return env


def _collectstatic(env: dict[str, str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(ROOT / "manage.py"), "collectstatic", "--noinput"],
        cwd=ROOT,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=900,
        check=False,
    )


def _manifest(root: Path) -> dict[str, str]:
    manifest_file = root / "staticfiles.json"
    return json.loads(manifest_file.read_text(encoding="utf-8"))["paths"] if manifest_file.is_file() else {}


@dataclass
class Collected:
    root: Path
    manifest: dict[str, str]
    output: str
    returncode: int
    settings_module: str
    env: dict[str, str]

    def probe(self, urls: list[str], workdir: Path) -> dict[str, list]:
        """Each URL through the production middleware — WhiteNoise first — under the production settings: status and
        Cache-Control. A subprocess, so that the test settings of this process never reach it."""
        asked, answered = workdir / "urls.json", workdir / "answers.json"
        asked.write_bytes(json.dumps(sorted(set(urls))).encode())
        script = workdir / "probe_static.py"
        script.write_bytes(
            b'"""Written by tests/deployment/test_static_caching.py: WhiteNoise\'s answer to each URL."""\n'
            b"import json, sys\n\nimport django\n\ndjango.setup()\n"
            b"from django.conf import settings\nfrom django.test import Client\n\n"
            b"client, answers = Client(), {}\n"
            b"for url in json.loads(open(sys.argv[1], encoding='utf-8').read()):\n"
            b"    response = client.get(url, secure=True, HTTP_HOST='example.com')\n"
            b"    answers[url] = [response.status_code, response.get('Cache-Control', '')]\n"
            b"    response.close()\n"
            b"answers['WHITENOISE_MAX_AGE'] = settings.WHITENOISE_MAX_AGE\n"
            b"open(sys.argv[2], 'w', encoding='utf-8').write(json.dumps(answers))\n"
        )
        run = subprocess.run(
            [sys.executable, str(script), str(asked), str(answered)],
            cwd=ROOT,
            env=self.env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=600,
            check=False,
        )
        assert run.returncode == 0, (run.stdout + run.stderr)[-4000:]
        return json.loads(answered.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def collected(tmp_path_factory) -> Collected:
    """`collectstatic --noinput` under config.settings.prod with the runbook's environment, STATIC_ROOT moved into an
    empty temporary directory (runbook step 8)."""
    workdir = tmp_path_factory.mktemp("static_caching")
    root = workdir / "staticfiles"
    (workdir / "static_caching_settings.py").write_bytes(
        b'"""Written by tests/deployment/test_static_caching.py: the production settings, a temporary STATIC_ROOT."""\n'
        b"from config.settings.prod import *  # noqa: F401,F403\n\n" + f"STATIC_ROOT = {str(root)!r}\n".encode()
    )
    env = _production_env(workdir, "static_caching_settings")
    run = _collectstatic(env)
    return Collected(root, _manifest(root), run.stdout + run.stderr, run.returncode, "static_caching_settings", env)


@dataclass
class Walk:
    named: list[str]  # every file a template names
    unknown: list[str]  # named, and not collected
    reached: dict[str, str]  # URL -> the file (or template) it was reached from
    computed: list[str]  # modules holding a dynamic import that is not a string literal


def _walk(collected: Collected) -> Walk:
    named = sorted({name for path in _templates() for name in STATIC_TAG.findall(path.read_text(encoding="utf-8"))})
    unknown = [name for name in named if name not in collected.manifest]
    queue = [(STATIC_URL + collected.manifest[name], f"{{% static '{name}' %}}") for name in named]
    queue += [(STATIC_URL + name, f"{{% static '{name}' %}} (not collected)") for name in unknown]
    reached: dict[str, str] = {}
    computed: list[str] = []
    while queue:
        url, via = queue.pop()
        if url in reached or not url.startswith(STATIC_URL):
            continue
        reached[url] = via
        file = collected.root / url.removeprefix(STATIC_URL)
        if not file.is_file():
            continue  # answered 404 below
        if file.suffix == ".js":
            text = file.read_text(encoding="utf-8", errors="replace")
            references = _js_specifiers(text)
            if JS_COMPUTED.search(text):
                computed.append(url)
        elif file.suffix == ".css":
            references = _css_references(file.read_text(encoding="utf-8", errors="replace"))
        else:
            continue
        for spec in references:
            if (path := _local(spec)) is not None:
                queue.append((_resolve(url, path), url))
    return Walk(named, unknown, reached, computed)


def test_collectstatic_under_the_production_settings_succeeds_from_an_empty_static_root(collected):
    assert collected.returncode == 0, f"collectstatic failed:\n{collected.output[-4000:]}"
    for bundle in ("css/dist/main.css", "css/dist/portal/console.css", "js/dist/shell.js", "js/dist/console.js"):
        assert bundle in collected.manifest, f"{bundle} was not hashed"
        assert (collected.root / collected.manifest[bundle]).is_file(), bundle


def test_every_file_a_page_can_load_is_a_hashed_name_cached_as_immutable(collected, tmp_path):
    assert collected.returncode == 0, collected.output[-4000:]
    walk = _walk(collected)
    assert not walk.unknown, f"templates name static files that collectstatic does not produce: {walk.unknown}"
    assert not walk.computed, (
        "a module a page loads imports a computed specifier — import(<expression>) — which no storage can rewrite to a "
        f"hashed name and no test can follow; write the specifier as a string literal: {walk.computed}"
    )
    beyond = set(walk.reached) - {STATIC_URL + collected.manifest[name] for name in walk.named}
    assert beyond, "the walk reached nothing beyond the templates' own files: it is not following the imports"
    hashed = {STATIC_URL + name for name in collected.manifest.values()}
    answers = collected.probe(list(walk.reached), tmp_path)
    problems = []
    for url, via in sorted(walk.reached.items()):
        status, cache_control = answers[url]
        if status != 200:
            problems.append(f"{url}: {status} (from {via})")
        elif url not in hashed:
            problems.append(f"{url}: a plain name, «{cache_control}» (from {via})")
        elif "immutable" not in cache_control:
            problems.append(f"{url}: hashed, yet «{cache_control}» (from {via})")
    assert not problems, (
        f"{len(problems)} of the {len(walk.reached)} files the templates' entries reach are not hashed-and-immutable:\n"
        + "\n".join(problems)
    )


def test_every_import_of_every_module_is_rewritten_to_the_hashed_name_it_resolves_to(collected):
    assert collected.returncode == 0, collected.output[-4000:]
    modules = sorted(DIST.rglob("*.js"))
    assert modules, "no module in static/js/dist"
    problems, rewritten = [], 0
    for source in modules:
        name = source.relative_to(ROOT / "static").as_posix()
        written = _js_specifiers(source.read_text(encoding="utf-8"))
        served = _js_specifiers((collected.root / collected.manifest[name]).read_text(encoding="utf-8"))
        if len(written) != len(served):
            problems.append(f"{name}: {len(written)} imports written, {len(served)} served: {written} / {served}")
            continue
        for spec, as_served in zip(written, served, strict=True):
            target = _resolve(name, spec)
            if target not in collected.manifest:
                problems.append(f"{name}: {spec!r} resolves to {target}, which is not collected")
                continue
            expected = posixpath.join(posixpath.dirname(spec), posixpath.basename(collected.manifest[target]))
            if as_served != expected:
                problems.append(f"{name}: {spec!r} is served as {as_served!r}, not as the hashed {expected!r}")
            else:
                rewritten += 1
    assert not problems, "imports the collected modules do not hold by their hashed names:\n" + "\n".join(problems)
    assert rewritten, "no import found in static/js/dist: the parser is not reading the modules"


def test_no_script_outside_static_js_dist_is_rewritten_by_the_module_patterns(collected):
    """REVIEW_2 m6: the module patterns read only the bundles (core.storage.MODULES) — the sources of static/js/src keep
    their imports as written, and no third-party script is read for imports."""
    assert collected.returncode == 0, collected.output[-4000:]
    outside = sorted(name for name in collected.manifest if name.endswith(".js") and not name.startswith("js/dist/"))
    sources = [name for name in outside if name.startswith("js/src/")]
    assert sources and len(outside) > len(sources), "the walk lost the sources or the third-party scripts"
    changed, with_imports = [], 0
    for name in outside:
        written = _js_specifiers(Path(finders.find(name)).read_text(encoding="utf-8", errors="replace"))
        served = _js_specifiers(
            (collected.root / collected.manifest[name]).read_text(encoding="utf-8", errors="replace")
        )
        with_imports += bool(written)
        if served != written:
            changed.append(f"{name}: {written} written, {served} collected")
    assert with_imports, "no import found outside static/js/dist: the sources of static/js/src import one another"
    assert not changed, "scripts outside static/js/dist rewritten by the module patterns:\n" + "\n".join(changed)


def test_a_plain_name_is_cached_for_minutes_at_most(collected, tmp_path):
    assert collected.returncode == 0, collected.output[-4000:]
    walk = _walk(collected)
    by_hashed = {STATIC_URL + hashed: STATIC_URL + name for name, hashed in collected.manifest.items()}
    plain = sorted({by_hashed.get(url, url) for url in walk.reached})
    answers = collected.probe(plain, tmp_path)
    assert answers["WHITENOISE_MAX_AGE"] <= SHORT_MAX_AGE, answers["WHITENOISE_MAX_AGE"]
    problems = []
    for url in plain:
        status, cache_control = answers[url]
        age = re.search(r"max-age=(\d+)", cache_control)
        if status != 200 or "immutable" in cache_control or not age or int(age.group(1)) > SHORT_MAX_AGE:
            problems.append(f"{url}: {status} «{cache_control}»")
    assert not problems, (
        f"plain names cached beyond {SHORT_MAX_AGE} s — a release would leave returning browsers on the old file:\n"
        + "\n".join(problems)
    )


# --------------------------------------------------------------------------- a release over the previous one


@dataclass
class Release:
    manifest: dict[str, str]
    files: dict[str, bytes]  # every file under STATIC_ROOT after the collect, by its path from STATIC_ROOT
    output: str
    returncode: int


@pytest.fixture(scope="module")
def two_releases(tmp_path_factory) -> tuple[Release, Release, Path]:
    """
    Release N, then release N+1 collected over it into the same STATIC_ROOT, never --clear (runbook step 15), under the
    production settings: the bundles of static/js/dist alone (a copy), N+1 changing loader.js in place — the original
    bug's shape: its name and its importers' text stay the same, only its content changes.
    """
    workdir = tmp_path_factory.mktemp("static_release")
    source, root = workdir / "static", workdir / "staticfiles"
    shutil.copytree(DIST, source / "js" / "dist")
    (workdir / "static_release_settings.py").write_bytes(
        b'"""Written by tests/deployment/test_static_caching.py: the production settings, the bundles of static/js/dist'
        b' alone (a copy), a temporary STATIC_ROOT."""\n'
        b"from config.settings.prod import *  # noqa: F401,F403\n\n"
        + f"STATIC_ROOT = {str(root)!r}\nSTATICFILES_DIRS = [{str(source)!r}]\n".encode()
        + b'STATICFILES_FINDERS = ["django.contrib.staticfiles.finders.FileSystemFinder"]\n'
    )
    env = _production_env(workdir, "static_release_settings")
    releases = []
    for release in ("N", "N+1"):
        if release == "N+1":
            loader = source / "js" / "dist" / "loader.js"
            loader.write_bytes(loader.read_bytes() + b"\n/* release N+1 */\n")
            # Newer than its collected copy, as a checkout leaves a changed file: collectstatic skips a source that is not.
            later = time.time() + 60
            os.utime(loader, (later, later))
        run = _collectstatic(env)
        files = {path.relative_to(root).as_posix(): path.read_bytes() for path in root.rglob("*") if path.is_file()}
        releases.append(Release(_manifest(root), files, run.stdout + run.stderr, run.returncode))
    return releases[0], releases[1], source


def _importers(target: str, source: Path) -> set[str]:
    """The modules of the copied dist that import `target`, directly or through another module."""
    imports = {}
    for path in (source / "js" / "dist").rglob("*.js"):
        name = path.relative_to(source).as_posix()
        imports[name] = {_resolve(name, spec) for spec in _js_specifiers(path.read_text(encoding="utf-8"))}
    found, frontier = set(), {target}
    while frontier:
        frontier = {name for name, targets in imports.items() if targets & frontier} - found
        found |= frontier
    return found


def _graph_problems(manifest: dict[str, str], files: dict[str, bytes]) -> list[str]:
    """Every module of a release, followed through `files` from its hashed name: each import a hashed name of that
    release, present."""
    hashed = set(manifest.values())
    queue = [manifest[name] for name in manifest if name.endswith(".js")]
    seen, problems = set(), []
    while queue:
        name = queue.pop()
        if name in seen:
            continue
        seen.add(name)
        if name not in files:
            problems.append(f"{name}: not collected")
            continue
        for spec in _js_specifiers(files[name].decode("utf-8", errors="replace")):
            target = _resolve(name, spec)
            if target not in hashed:
                problems.append(f"{name} imports {spec!r}: {target} is not a hashed name of this release")
            else:
                queue.append(target)
    return problems


def test_a_release_collected_over_the_previous_one_renames_what_changed_and_keeps_the_previous(two_releases):
    """REVIEW_2 m5: runbook step 15's collectstatic, into the root that holds release N."""
    before, after, source = two_releases
    assert before.returncode == 0, before.output[-4000:]
    assert after.returncode == 0, after.output[-4000:]
    loader = "js/dist/loader.js"
    assert after.manifest[loader] != before.manifest[loader], "loader.js changed, and kept its hashed name"
    importers = _importers(loader, source)
    assert importers, "nothing imports loader.js: the test lost its subject"
    renamed = {name for name, hashed in before.manifest.items() if after.manifest.get(name) != hashed}
    assert renamed == {loader, *importers}, (
        f"a release that changes loader.js renames it and every module importing it, nothing else: renamed "
        f"{sorted(renamed)}, importers {sorted(importers)}"
    )
    gone = [
        path
        for hashed in before.manifest.values()
        for path in (hashed, hashed + ".gz")
        if path in before.files and after.files.get(path) != before.files[path]
    ]
    assert not gone, f"files of release N changed or vanished — a page opened before the release imports them: {gone}"
    for label, manifest in (("N", before.manifest), ("N+1", after.manifest)):
        problems = _graph_problems(manifest, after.files)
        assert not problems, f"release {label}, after the second collect:\n" + "\n".join(problems)


# --------------------------------------------------------------------------- the passes, in every directory order


def _collectable() -> dict[str, tuple]:
    """What collectstatic finds, as it finds it: {its path, built with os.path.join: (source storage, source path)},
    the first finder's file winning, the default ignore patterns (django.contrib.staticfiles' collectstatic)."""
    found: dict[str, tuple] = {}
    for finder in finders.get_finders():
        for path, source in finder.list(apps.get_app_config("staticfiles").ignore_patterns):
            prefixed = os.path.join(source.prefix, path) if getattr(source, "prefix", None) else path
            found.setdefault(prefixed, (source, path))
    return found


def _target(name: str, url: str) -> str | None:
    """The collected file `url`, written in the file collected as `name`, names — as HashedFilesMixin.url_converter and
    _stored_name resolve it — or None for what the converter leaves alone (a scheme, `//`, another site's absolute
    path, a bare fragment, a directory)."""
    if re.match(r"^[a-z]+:", url) or url.startswith("//"):
        return None
    if url.startswith("/") and not url.startswith(STATIC_URL):
        return None
    url_path = urldefrag(url)[0]
    if not url_path:
        return None
    if url_path.startswith("/"):
        target = url_path.removeprefix(STATIC_URL)
    else:
        target = posixpath.join(posixpath.dirname(name.replace(os.sep, "/")), url_path)
    clean = urldefrag(unquote(target))[0]
    if urlsplit(clean).path.endswith("/"):
        return None
    return urlsplit(unquote(posixpath.normpath(clean))).path.strip()


def _references(storage) -> tuple[dict[str, set[str]], list[str]]:
    """What `storage` rewrites in each file collectstatic would post-process: {file: the collected files it names}, by
    their paths from STATIC_ROOT, and every reference that names no collected file."""
    found = _collectable()
    collected = {name.replace(os.sep, "/") for name in found}
    references: dict[str, set[str]] = {}
    unresolved: list[str] = []
    for name, (source, path) in sorted(found.items()):
        if not matches_patterns(name, storage._patterns):
            continue
        with source.open(path) as handle:
            text = handle.read().decode("utf-8", errors="replace")
        targets = set()
        for extension, patterns in storage._patterns.items():
            if not matches_patterns(path, (extension,)):
                continue
            for pattern, _template in patterns:
                for match in pattern.finditer(text):
                    target = _target(name, match.group("url"))
                    if target is None:
                        continue
                    if target in collected:
                        targets.add(target)
                    else:
                        unresolved.append(f"{name.replace(os.sep, '/')}: {match.group('url')!r} names {target}")
        references[name.replace(os.sep, "/")] = targets
    return references, unresolved


def _settling_passes(references: dict[str, set[str]]) -> dict[str, int]:
    """
    For each file Django post-processes, the passes after its first that its hashed name needs to settle, in the worst
    directory order (HashedFilesMixin.post_process, Django 5.2).

    Every pass meets the files deepest directory first, and within one depth in the order the directories list them —
    sorted on NTFS, hash order on ext4: not this workstation's, so any. A file is rewritten with the names its references
    have at that moment. A reference to a file that its own rewriting never changes (an image, a module importing
    nothing) has its final name from the start: it costs nothing. A reference to a file that changes costs that file's
    passes, plus one when the file can be met later in the pass — shallower, or as deep. A cycle never settles.
    """
    depth = {name: name.count("/") + 1 for name in references}
    settled: dict[str, int] = {}

    def passes(name: str, stack: tuple[str, ...]) -> int:
        if name in stack:
            return NEVER
        if name not in settled:
            need = 0
            for target in references[name]:
                if references.get(target):
                    later = depth[target] <= depth[name]
                    need = max(need, passes(target, (*stack, name)) + later)
            settled[name] = need
        return settled[name]

    return {name: passes(name, ()) for name in references}


def test_the_model_of_the_passes_agrees_with_django_on_a_chain_of_modules():
    """
    The review's demonstration (REVIEW_2 m3, a real collectstatic): seven modules a → b → … → g in one directory, no
    cycle — «Max post-process passes exceeded» in the order where each module is listed before the one it imports,
    success in the other. The model gives that chain 5 passes (Django allows 4), six modules 4; the same chain down the
    directories settles in the first pass (a deeper file is always met first); a cycle never settles.
    """

    def chain(names: list[str]) -> dict[str, set[str]]:
        return {name: set(names[i + 1 : i + 2]) for i, name in enumerate(names)}

    one_directory = [f"js/chain/{letter}.js" for letter in "abcdefg"]
    assert max(_settling_passes(chain(one_directory)).values()) == 5 > PASSES_ALLOWED
    assert max(_settling_passes(chain(one_directory[1:])).values()) == 4 == PASSES_ALLOWED
    down_the_directories = ["/".join(["js", *["d"] * level, f"{level}.js"]) for level in range(7)]
    assert max(_settling_passes(chain(down_the_directories)).values()) == 0
    assert _settling_passes({"js/a.js": {"js/b.js"}, "js/b.js": {"js/a.js"}})["js/a.js"] >= NEVER


def test_every_reference_the_storage_rewrites_names_a_collected_file(tmp_path):
    """REVIEW_2 m6: a reference that names nothing stops collectstatic (MissingFileError) — here first, not inside a
    release window on the server."""
    _references_, unresolved = _references(CompressedManifestModulesStorage(location=str(tmp_path)))
    assert _references_, "nothing to post-process: the finders listed nothing"
    assert not unresolved, "references collectstatic would stop on:\n" + "\n".join(unresolved)


def test_no_directory_order_asks_django_for_more_passes_than_it_runs(tmp_path):
    """REVIEW_2 m3: the worst case over every directory order, from the files collectstatic would collect."""
    references, _unresolved = _references(CompressedManifestModulesStorage(location=str(tmp_path)))
    passes = _settling_passes(references)
    slowest = sorted(passes.items(), key=lambda item: (-item[1], item[0]))[:5]
    assert slowest and slowest[0][1] <= PASSES_ALLOWED, (
        f"in the worst directory order a hashed name needs {slowest[0][1]} passes after the first, and Django's "
        f"post-processing settles {PASSES_ALLOWED} («Max post-process passes exceeded» wherever the directories list "
        f"that way): shorten the chain of imports, or break the cycle. The slowest: {slowest}"
    )


def test_the_module_patterns_read_the_bundles_of_static_js_dist_only(tmp_path):
    """REVIEW_2 m3 and m6: Django's switch would run them on every collected script — the sources of static/js/src,
    which no page loads and whose chains cost passes, and the third-party scripts."""
    storage = CompressedManifestModulesStorage(location=str(tmp_path))
    assert storage.support_js_module_import_aggregation is False, "Django's switch puts them on every script"
    module_patterns = {pattern.pattern for pattern, _template in storage._patterns[MODULES]}
    assert module_patterns == {
        pattern if isinstance(pattern, str) else pattern[0]
        for pattern in HashedFilesMixin._js_module_import_aggregation_patterns[1]
    }, "not Django's four module patterns"
    found = _collectable()
    matched = sorted(name.replace(os.sep, "/") for name in found if matches_patterns(name, (MODULES,)))
    bundles = sorted(path.relative_to(ROOT / "static").as_posix() for path in DIST.rglob("*.js"))
    assert matched == bundles, f"the module patterns read {matched}, the bundles are {bundles}"
    for spelled in ("js/dist/loader.js", "js\\dist\\chunks\\chunk-A.js"):
        assert matches_patterns(spelled, (MODULES,)), spelled
    for other in ("js/src/console.js", "js\\src\\console.js", "admin/js/core.js", "js/dist/loader.js.map"):
        assert not matches_patterns(other, (MODULES,)), other
