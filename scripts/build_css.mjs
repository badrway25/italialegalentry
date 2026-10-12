/**
 * Bundle and minify the stylesheets with esbuild — the same binary as the JS build, nothing new.
 *
 *     npm run build:css         — once: static/css/dist/ is rewritten from the sources
 *     npm run watch:css         — rebuild on save, sourcemaps beside the output (never committed)
 *
 * Why (Gate A, 26/09/2026, approved by the product owner): main.css pulled 21 sheets with @import,
 * 95 KB gzip of which half was comments, over 21 requests that held the six HTTP/1.1 connections
 * for ≈ 1.3 s while the LCP photograph waited in the queue. One bundle, minified, is ≈ 35 KB gzip.
 *
 * What it does, and what it must not do:
 *   - static/css/main.css → static/css/dist/main.css: the @import chain resolved IN ORDER, so the
 *     cascade is the one main.css declares; comments removed; whitespace and numbers minified.
 *   - every app sheet (apps/<app>/static/**.css) → static/css/dist/<its static path>: minified,
 *     one file each, loaded by the templates that loaded the source.
 *   - a `_`-prefixed sheet is a PARTIAL, wherever it is: never an entry, never an output of its own;
 *     the entries that draw it import it and carry it in their bundle (design V5, V5.4 plan §2.3 «the
 *     one build change», DL54-15). static/css/_legacy-tokens.css was already one, inside main.css.
 *   - every @import and url() of a source sheet is written as it resolves in the COLLECTED tree
 *     (static/x → x, apps/<app>/static/x → x), from the sheet's own collected path: production's
 *     manifest storage post-processes every collected CSS file, raw sources included, and resolves
 *     them there. A partial of static/css/v5/ is `../css/v5/_x.css` from apps/<app>/static/<app>/
 *     <sheet>.css, never `../../../../static/css/v5/_x.css` — that path exists only in the source
 *     tree and stops collectstatic. The plugin below bundles each @import from the one source file
 *     collected at that path (static/ first, then each app's static/, the order of Django's finders)
 *     and refuses a path that climbs out (DS 2026 §2; tests/frontend/test_static_pipeline.py).
 *   - NO syntax lowering: no `target`, so esbuild rewrites no property for older browsers and the
 *     cascade is not reinterpreted. Minification only.
 *   - url() to fonts and images stay files served by collectstatic, never inlined or copied: the
 *     plugin below rewrites each path relative to the OUTPUT, in the static namespace (the tree
 *     collectstatic builds), which is where ManifestStaticFilesStorage resolves and hashes them.
 *     url(#…) (SVG fragments) and data: URLs are left alone.
 *
 * static/css/dist/ is versioned, like static/js/dist/: the production host runs collectstatic, not
 * Node. tests/frontend/test_css_bundle_is_current.py refuses a dist older than its sources and one
 * that lost a source's custom properties or kept a comment.
 */

import { build, context } from "esbuild";
import { existsSync, readdirSync, statSync, mkdirSync } from "node:fs";
import { join, resolve, dirname, relative, isAbsolute, sep, posix } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const STATIC = join(ROOT, "static");
const DIST = join(STATIC, "css", "dist");
const watch = process.argv.includes("--watch");

/** The directories collectstatic merges, in the order Django's two default finders read them:
 *  STATICFILES_DIRS (static/), then each app's static/ (AppDirectoriesFinder). */
const STATIC_DIRS = [STATIC];
for (const app of readdirSync(join(ROOT, "apps"))) {
  const dir = join(ROOT, "apps", app, "static");
  if (existsSync(dir) && statSync(dir).isDirectory()) STATIC_DIRS.push(dir);
}

/** The path a file has once collectstatic has merged every static directory: static/x → x,
 *  apps/<app>/static/x → x. */
function staticPath(absolute) {
  for (const dir of STATIC_DIRS) {
    const rel = relative(dir, absolute);
    if (rel && rel !== ".." && !rel.startsWith(`..${sep}`) && !isAbsolute(rel)) return rel.split(sep).join("/");
  }
  throw new Error(`not under a static directory: ${absolute}`);
}

/** Where a reference written in a source sheet lands once collected: read from the sheet's OWN
 *  collected path, never through the source tree. `null` for a path that climbs above the collected
 *  root (or starts at it): it only exists in the source tree, and collectstatic stops on it. */
function collectedTarget(importer, ref) {
  if (ref.startsWith("/")) return null;
  const target = posix.normalize(posix.join(posix.dirname(staticPath(importer)), ref));
  return target === ".." || target.startsWith("../") ? null : target;
}

function walk(dir, out = []) {
  for (const name of readdirSync(dir)) {
    const full = join(dir, name);
    if (statSync(full).isDirectory()) walk(full, out);
    else if (name.endsWith(".css")) out.push(full);
  }
  return out;
}

/** A `_`-prefixed file is a partial: its importers bundle it (V5.4 plan §2.3, DL54-15). */
const isPartial = (file) => file.split(sep).pop().startsWith("_");

// Entry points: the main cascade, and every app sheet that is not a partial.
const entries = [{ source: join(STATIC, "css", "main.css"), out: "main.css" }];
for (const dir of STATIC_DIRS.slice(1)) {
  for (const source of walk(dir)) if (!isPartial(source)) entries.push({ source, out: staticPath(source) });
}

/** @import and url() resolved in the collected tree, as the manifest storage resolves them in
 *  production: an @import is bundled from the one source file collected at its path; a font or an
 *  image stays a file, its path re-anchored on the output's location. */
function collectedPaths(outfile) {
  const outDir = posix.dirname(staticPath(outfile));
  return {
    name: "collected-paths",
    setup(pluginBuild) {
      pluginBuild.onResolve({ filter: /.*/ }, (args) => {
        if (args.kind !== "import-rule" && args.kind !== "url-token") return undefined;
        if (/^(#|data:|https?:|\/\/)/.test(args.path)) return { path: args.path, external: true };
        const where = `${relative(ROOT, args.importer).split(sep).join("/")}: "${args.path}"`;
        const target = collectedTarget(args.importer, args.path);
        if (target === null) {
          const text = `${where} is not a path of the collected static tree: write it as it resolves there, from this sheet's collected path (DS 2026 §2)`;
          return { errors: [{ text }] };
        }
        if (args.kind === "url-token") return { path: posix.relative(outDir, target), external: true };
        const sources = STATIC_DIRS.map((dir) => join(dir, ...target.split("/"))).filter((file) => existsSync(file));
        if (sources.length === 1) return { path: sources[0] };
        const text = sources.length
          ? `${where}: ${target} is collected from ${sources.length} static directories — give it one`
          : `${where}: nothing is collected at ${target}`;
        return { errors: [{ text }] };
      });
    },
  };
}

function options({ source, out }) {
  const outfile = join(DIST, ...out.split("/"));
  mkdirSync(dirname(outfile), { recursive: true });
  return {
    entryPoints: [source],
    outfile,
    bundle: true,
    minify: true,
    legalComments: "none",
    sourcemap: watch,
    logLevel: "warning",
    metafile: true,
    plugins: [collectedPaths(outfile)],
  };
}

if (watch) {
  for (const entry of entries) {
    const ctx = await context(options(entry));
    await ctx.watch();
  }
  console.log(`watching ${entries.length} stylesheets …`);
} else {
  for (const entry of entries) {
    const result = await build(options(entry));
    for (const [file, meta] of Object.entries(result.metafile.outputs)) {
      if (file.endsWith(".css")) console.log(`${relative(ROOT, file).split(sep).join("/")}  ${(meta.bytes / 1024).toFixed(1)} KB (min)`);
    }
  }
}
