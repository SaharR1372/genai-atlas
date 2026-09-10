# Claims checked against primary sources and refuted

Verified 2026-09-10. The atlas's rule is that nothing enters without a primary source, meaning the
vendor's own site, documentation, model card, or an arXiv paper. Aggregator blogs and roundups are
not primary, however consistent they are with each other.

These were all circulating in secondary coverage and are recorded here so nobody re-chases them.

| Claim | Verdict | What the primary source actually shows |
|---|---|---|
| **Qwen-Image-3.0**, claimed GA 2026-08-05 | **Refuted** | Not present on qwenlm.github.io, in the Qwen Hugging Face organisation, in the QwenLM GitHub organisation, or on the Alibaba Cloud blog. The most recent Qwen image releases are Qwen-Image-Edit-2511 and Qwen-Image-2512. The claimed GA date has passed. |
| **MAI-Image-2.6** (Microsoft) | **Refuted** | Microsoft's own Azure AI Foundry catalogue lists MAI-Image-2.5 and MAI-Image-2.5-Flash, both in preview. There is no 2.6. The circulating leaderboard rating attached to it cannot be tied to any Microsoft source. |
| **Stable Diffusion 4** | **Refuted** | Stability AI's own news feed through 2026-08-25 contains no such announcement, and their Hugging Face organisation's most recent image models remain the Stable Diffusion 3.5 family. Their recent releases are audio models. |
| **FLUX 3 open weights / image API** | **Partly refuted** | The 2026-07-23 announcement on the vendor's blog is real, but as of 2026-09-10 only FLUX 3 Video is in early access, the vendor's documentation still directs production image work to FLUX.2, and no FLUX 3 repository exists in their Hugging Face organisation. The promised open-weight release has no committed date. |

## Confirmed in the same pass

| Claim | Verdict | Primary source |
|---|---|---|
| **GPT-Image 2.5** | Confirmed, 2026-09-08 | OpenAI's API changelog and model documentation. Two ids: `gpt-image-2.5-sunburst` and `gpt-image-2.5-flare`. API only. |
| **Nano Banana 2 Lite** | Model confirmed, date not | Google's developer documentation confirms `gemini-3.1-flash-lite-image` and its availability. No dated announcement post could be found, so the July 2026 date remains unverified. |
| **Krea 2** | Confirmed | Krea's own blog and Hugging Face organisation. 13B text-to-image, open weights under a gated community licence rather than a permissive one. |
| **Kroma v0.2** | Confirmed, but reclassified | The creator's own model card shows it is a community fine-tune built on Krea 2 by an independent user, not a vendor base model. Recorded as a downstream fine-tune rather than a peer entry. |
