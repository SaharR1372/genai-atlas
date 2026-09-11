import { defineConfig } from "astro/config";
import mdx from "@astrojs/mdx";
import baseHref from "./base-href.mjs";

// See docs/blueprint.md section 5 (Decision D002) for the stack rationale.
// Astro's own major version has moved past the "Astro 5" the blueprint assumed when
// written pre-release; we track current stable (see DECISIONS.md D011).
//
// Published as a GitHub Pages project site (D024), which serves from a sub-path. The
// source keeps writing root-absolute links; `baseHref` prefixes them at build time.
// Override both when moving to a custom domain: set site to the domain and base to "/".
export default defineConfig({
  site: process.env.SITE_URL ?? "https://saharr1372.github.io",
  base: process.env.SITE_BASE ?? "/genai-atlas",
  trailingSlash: "ignore",
  integrations: [mdx(), baseHref()],
});
