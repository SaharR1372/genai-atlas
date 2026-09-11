import { readdirSync, readFileSync, statSync, writeFileSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

/**
 * GitHub Pages serves a project repo from a sub-path (/genai-atlas/), but this atlas
 * writes root-absolute links everywhere: ~30 in .astro components and ~150 more inside
 * MDX prose, where `import.meta.env.BASE_URL` is not available at all.
 *
 * Rewriting all of them by hand would mean 180 edit sites and a permanent trap for
 * anyone writing new prose. Instead the source keeps writing plain "/papers/x" and this
 * integration prefixes the base once, in the emitted HTML, at `astro:build:done`.
 *
 * Astro has already prefixed its own generated asset URLs by the time this runs, so
 * anything that starts with the base is skipped rather than prefixed twice.
 */
export default function baseHref() {
  // `astro:build:done` is not given the resolved config, so capture the base earlier.
  // Reading it from the config hook rather than hardcoding keeps the SITE_BASE override
  // working, and means a move to a custom domain (base "/") disables this cleanly.
  let base = "/";
  return {
    name: "atlas-base-href",
    hooks: {
      "astro:config:done": ({ config }) => {
        base = config.base ?? "/";
      },
      "astro:build:done": ({ dir, logger }) => {
        const prefix = base.replace(/\/$/, "");
        if (!prefix) return;

        // href/src/action, double or single quoted, starting with a single slash.
        // `//example.com` is protocol-relative and must not be touched.
        const attr = new RegExp(
          `(\\s(?:href|src|action)=)(["'])/(?!/)(?!${prefix.slice(1)}(?:/|["']))`,
          "g"
        );

        let files = 0;
        let edits = 0;
        const walk = (d) => {
          for (const name of readdirSync(d)) {
            const p = join(d, name);
            if (statSync(p).isDirectory()) walk(p);
            else if (name.endsWith(".html")) {
              const before = readFileSync(p, "utf8");
              const after = before.replace(attr, (_m, a, q) => {
                edits++;
                return `${a}${q}${prefix}/`;
              });
              if (after !== before) {
                writeFileSync(p, after);
                files++;
              }
            }
          }
        };
        walk(fileURLToPath(dir));
        logger.info(`rewrote ${edits} root-absolute links across ${files} pages to "${prefix}/"`);
      },
    },
  };
}
