import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

// Long-form MDX lives at the repo root under content/, not duplicated inside
// site/src/content/ — see docs/blueprint.md section 6 (Decision D003). The glob loader's
// `base` is resolved relative to this Astro project's root (site/).
const mdxSchema = z.object({ id: z.string(), title: z.string() });

const transitions = defineCollection({
  loader: glob({ pattern: "**/*.mdx", base: "../content/transitions" }),
  schema: mdxSchema,
});

const lines = defineCollection({
  loader: glob({ pattern: "**/*.mdx", base: "../content/lines" }),
  schema: mdxSchema,
});

const concepts = defineCollection({
  loader: glob({ pattern: "**/*.mdx", base: "../content/concepts" }),
  schema: mdxSchema,
});

export const collections = { transitions, lines, concepts };
