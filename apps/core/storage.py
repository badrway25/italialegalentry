"""
The storage collectstatic writes the static files with in production (config/settings/base.py, STORAGES).

WhiteNoise's CompressedManifestStaticFilesStorage — every file copied under a name that carries a hash of its content,
a `.gz` beside it — with one addition: the import specifiers of the ES modules are rewritten to those hashed names too.

Why. The templates link each entry through {% static %}, so the browser asks for `shell.<hash>.js`, and WhiteNoise
serves a hashed name as immutable for ten years. But the bundles of static/js/dist are ES modules that import one
another by relative specifiers — the shared chunks, and the entries loaded on demand (loader.js from shell.js and from a
chunk, depot.js and piece-drawer.js from console.js) — and by default the manifest storage rewrites a stylesheet's url()
and @import, never a script's import. From the hashed entry the browser went on to ask for the chunks and the on-demand
entries under their plain names, and a plain name says nothing about its content: with a year of cache on it, a
returning browser could run the previous release's module beside the new pages (measured on a real collectstatic,
16 October 2026: 10 of the files the templates reach; docs/design-v5/QA/v54/devops/NOTES.md, second pass, item 1).

Django rewrites `import … from "…"`, `export … from "…"`, `import "…"` and the dynamic `import("…")` the way it rewrites
url() (its module patterns, documented as experimental since Django 4.2 behind `support_js_module_import_aggregation`;
read in the 5.2 this project pins, django/contrib/staticfiles/storage.py). Every module a page loads is then a hashed
name, cached as immutable, and one page load is always one release: a page opened before a release keeps importing the
files of its own release, which stay collected (collectstatic never runs with --clear, runbook step 8).

The patterns run on the bundles of static/js/dist only (MODULES), not on every collected script as Django's switch would
have them (the review of the second pass, REVIEW_2 m3 and m6): the sources of static/js/src are collected but no page
loads them, and a third-party script whose text merely looks like an import — a comment, a string — naming no file
would stop collectstatic inside a release window.

What it asks of the bundles, both met by esbuild's output today:

* a specifier is a string literal — a computed `import(x)` cannot be rewritten;
* the chains of imports stay short. A file's hashed name depends on the names it imports, so each pass of Django's
  post-processing settles one more link of a chain whose files it meets in the wrong order — and that order follows the
  directory listing (sorted on NTFS, hash order on ext4), not this workstation's. After its first pass Django runs at
  most five more and needs the last to change nothing, so a name may take four to settle: one that takes five, or a
  cycle, which never settles, stops collectstatic with «Max post-process passes exceeded» — loud, never a stale page,
  but inside the release window if only the server's order needs it. tests/deployment/test_static_caching.py computes
  the worst case over every directory order from the files themselves, in milliseconds (today: 2 of the 4).

tests/deployment/test_static_caching.py also runs a real collectstatic under the production settings — twice into one
STATIC_ROOT, as a release does — and holds every file a page can load to a hashed, immutable name; base.py's
WHITENOISE_MAX_AGE caps at a minute whatever would escape it.
"""

from __future__ import annotations

from django.contrib.staticfiles.storage import HashedFilesMixin
from whitenoise.storage import CompressedManifestStaticFilesStorage

#: The modules whose imports are rewritten: the bundles esbuild writes into static/js/dist, chunks/ included (fnmatch's
#: `*` crosses directories). Django matches it against collectstatic's own path, which os.path.join builds — a backslash
#: on Windows, a slash on the server — hence the bracket.
MODULES = r"js[/\]dist[/\]*.js"


class CompressedManifestModulesStorage(CompressedManifestStaticFilesStorage):
    """WhiteNoise's compressed manifest storage, with the imports of static/js/dist rewritten to the hashed names."""

    patterns = (
        *CompressedManifestStaticFilesStorage.patterns,
        (MODULES, HashedFilesMixin._js_module_import_aggregation_patterns[1]),
    )
