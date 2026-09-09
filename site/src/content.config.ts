import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

// Long-form MDX narratives live at the repo root under content/, not duplicated inside
// site/src/content/ — see docs/blueprint.md section 6 (Decision D003). The glob loader's
// `base` is resolved relative to this Astro project's root (site/).
const transitions = defineCollection({
  loader: glob({ pattern: "**/*.mdx", base: "../content/transitions" }),
  schema: z.object({
    id: z.string(),
    title: z.string(),
  }),
});

export const collections = { transitions };
