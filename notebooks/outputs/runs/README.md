# Model run outputs

Generated on this machine (3x A100 80GB) from the released weights. Same prompts, same seed 42,
across models, so the images are directly comparable within a prompt.

## Prompts

| key | prompt | what it tests |
|---|---|---|
| `text` | a storefront window with a hand-painted sign reading "GENERATIVE VISION ATLAS", morning light, photograph | text rendering, the capability Qwen-Image was built around |
| `compose` | three red cubes stacked on top of a blue sphere, to the left of a green cone, studio lighting | counting and spatial relations, what GenEval measures |
| `photo` | a close-up portrait of an elderly fisherman with a weathered face, soft window light, 85mm lens | plain photographic quality with no trick |

## Fairness note, which matters more than the images

Comparing a full model against a distilled one is the exact mistake this atlas argues against on
`/compare`. LLaDA ships both a base model and a 2-to-4-step distilled Turbo variant, and the Turbo
results here should be read as "what distillation costs", not as "what LLaDA is". The base model is
being run separately for the honest comparison.

Likewise, step count and guidance differ between these systems because each is being run at its own
recommended settings rather than at a forced common setting. That is the right choice for showing
what a user would actually get, and the wrong choice for attributing quality to architecture. Both
readings are recorded rather than one being presented as the answer.
