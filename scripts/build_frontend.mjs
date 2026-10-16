/**
 * Bundle the frontend sources with esbuild.
 *
 *     npm run build:js          — once, minified, sourcemaps beside the output
 *     npm run watch:js          — rebuild on save, for the CODE → CHROME → OBSERVE loop
 *
 * Sources live in static/js/src/ and the bundles land in static/js/dist/. The dist IS versioned:
 * the production host runs `collectstatic`, not Node, so what the browser receives has to be in
 * the repository already. tests/frontend/test_frontend_bundle_is_current.py refuses a dist that is
 * older than its sources, which is the only way a forgotten build gets noticed before a deploy.
 *
 * Why esbuild and not Vite: there is no React to serve in development, no plugin is needed, and
 * one binary that does tree-shaking, minification and sourcemaps is the whole requirement. Vite
 * is reconsidered the day a React island justifies itself in writing — not before.
 *
 * Every entry point is an ES module loaded with `type="module"`, so it is deferred by definition
 * and never blocks the first paint. Nothing here is inlined into a template: the CSP is
 * `script-src 'self'` and stays that way.
 */

import { build, context } from "esbuild";
import { readdirSync, mkdirSync } from "node:fs";
import { join, resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const SRC = join(ROOT, "static", "js", "src");
const DIST = join(ROOT, "static", "js", "dist");

// One bundle per top-level source file. Shared code (the motion gate, helpers) lives in subdirectories or in
// shared chunks and is pulled into whichever bundles import it — a page loads what it uses.
// EXCEPT the modules that one entry alone imports, statically: as entries of their own their code went into a
// chunk and a stub nobody loads, one more request before `load` on every page that loads their importer (the
// request ratchet of plan §2.6). Not entries, they are inlined into that importer: nav.js into shell.js (every
// public page; W2-C1's A11Y_PERF item 5), hero.js into home.js (the home) — W4-B. A module a second entry starts
// importing simply becomes a shared chunk again. tests/frontend/test_frontend_bundle_is_current.py reads this list.
const INLINED = new Set(["nav.js", "hero.js"]);
const entryPoints = readdirSync(SRC)
  .filter((name) => name.endsWith(".js") && !INLINED.has(name))
  .map((name) => join(SRC, name));

mkdirSync(DIST, { recursive: true });

const options = {
  entryPoints,
  outdir: DIST,
  bundle: true,
  format: "esm",
  // Shared chunks: without splitting every page-level bundle would inline what it shares with the others (the
  // overlay system, the motion gate, the loader) — the same code twice on a page that loads two entries. With it,
  // a shared module is one chunk fetched once and cached across pages. (Motion, the reason this was first set,
  // left the dependencies with W4-B.)
  splitting: true,
  chunkNames: "chunks/[name]-[hash]",
  target: ["es2022"],
  minify: true,
  // Sourcemaps only while watching. A committed map is 400+ KB per bundle per change, and the
  // production host serves the dist as-is; debugging happens against `watch:js` on a developer's
  // machine, where the map is written and never committed (static/js/dist/*.map is ignored).
  sourcemap: process.argv.includes("--watch"),
  legalComments: "linked",   // licences go in a .LEGAL.txt beside the bundle, not in it
  logLevel: "info",
  metafile: true,
};

const watch = process.argv.includes("--watch");

if (watch) {
  const ctx = await context(options);
  await ctx.watch();
  console.log("watching static/js/src/ …");
} else {
  const result = await build(options);
  // The number that the budget in docs/design-v2/FRONTEND_DEPENDENCIES.md is written against.
  for (const [file, meta] of Object.entries(result.metafile.outputs)) {
    if (file.endsWith(".js")) console.log(`${file}  ${(meta.bytes / 1024).toFixed(1)} KB (min)`);
  }
}
