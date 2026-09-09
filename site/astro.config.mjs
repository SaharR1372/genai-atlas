import { defineConfig } from "astro/config";
import mdx from "@astrojs/mdx";

// See docs/blueprint.md section 5 (Decision D002) for the stack rationale.
// Astro's own major version has moved past the "Astro 5" the blueprint assumed when
// written pre-release; we track current stable (see DECISIONS.md D011).
export default defineConfig({
  site: "https://example.com", // placeholder until a real domain/GitHub Pages URL is chosen (P8)
  integrations: [mdx()],
});
