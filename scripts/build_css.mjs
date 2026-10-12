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
import { readdirSync, statSync, mkdirSync } from "node:fs";
import { join, resolve, dirname, relative, sep, posix } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const STATIC = join(ROOT, "static");
const DIST = join(STATIC, "css", "dist");
const watch = process.argv.includes("--watch");

/** The path a file has once collectstatic has merged every static directory: static/x → x,
 *  apps/<app>/static/x → x. */
function staticPath(absolute) {
  const parts = absolute.split(sep);
  const at = parts.lastIndexOf("static");
  if (at < 0) throw new Error(`not under a static directory: ${absolute}`);
  return parts.slice(at + 1).join("/");
}

function walk(dir, out = []) {
  for (const name of readdirSync(dir)) {
    const full = join(dir, name);
    if (statSync(full).isDirectory()) walk(full, out);
    else if (name.endsWith(".css")) out.push(full);
  }
  return out;
}

// Entry points: the main cascade, and every app sheet (none of them imports another).
const entries = [{ source: join(STATIC, "css", "main.css"), out: "main.css" }];
for (const app of readdirSync(join(ROOT, "apps"))) {
  const dir = join(ROOT, "apps", app, "static");
  try {
    if (!statSync(dir).isDirectory()) continue;
  } catch {
    continue;
  }
  for (const source of walk(dir)) entries.push({ source, out: staticPath(source) });
}

/** Keep fonts and images as files, with their path re-anchored on the output's location. */
function assetPaths(outfile) {
  const outDir = posix.dirname(staticPath(outfile));
  return {
    name: "static-asset-paths",
    setup(pluginBuild) {
      pluginBuild.onResolve({ filter: /.*/ }, (args) => {
        if (args.kind !== "url-token") return undefined; // @import is bundled normally
        if (/^(#|data:|https?:|\/\/)/.test(args.path)) return { path: args.path, external: true };
        const target = staticPath(resolve(args.resolveDir, args.path));
        return { path: posix.relative(outDir, target), external: true };
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
    plugins: [assetPaths(outfile)],
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
