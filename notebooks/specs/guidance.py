TITLE = "Guidance moves the number more than the architecture does"

INTRO = """
The atlas refuses to publish a leaderboard, and this notebook is the argument for that decision made
runnable.

Papers routinely report a headline FID and attribute the gap to their contribution. But the sampler
setting alone moves that number by more than most of the architectural gaps being argued about. The
clearest published example is a single table in one paper reporting the identical model at 1.65,
1.49, 1.14 and 1.06 under four different guidance methods, a swing of 0.59 with the weights held
fixed.

We cannot retrain a diffusion transformer here. What we can do is hold one model completely fixed,
vary only the guidance, and watch how far the output moves. If a knob you set at sampling time
changes the image this much, a benchmark number quoted without it is not telling you what you think.

Runs in a couple of minutes on one GPU. Outputs below are from an NVIDIA A100 80GB.
"""

CREDITS = """
**What this notebook uses, and who made it**

| Component | Source |
|---|---|
| Stable Diffusion 1.5 | [runwayml/stable-diffusion-v1-5](https://huggingface.co/runwayml/stable-diffusion-v1-5) |
| Classifier-free guidance | [Ho and Salimans](https://arxiv.org/abs/2207.12598) |
| `diffusers` | [huggingface/diffusers](https://github.com/huggingface/diffusers) |
| CLIP, used here only as a prompt-adherence measure | [openai/clip-vit-base-patch32](https://huggingface.co/openai/clip-vit-base-patch32) |

Related atlas reading: [why the benchmark numbers cannot rank the approaches](/compare) and
[the guidance and sampling line](/lines/line-guidance-sampling).
"""

CELLS = [
    ("code", '''import torch, numpy as np, matplotlib.pyplot as plt
from diffusers import StableDiffusionPipeline

DEV = "cuda" if torch.cuda.is_available() else "cpu"
DTYPE = torch.float16 if DEV == "cuda" else torch.float32
print(f"device: {DEV}", f"| gpu: {torch.cuda.get_device_name(0)}" if DEV == "cuda" else "")

pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5", torch_dtype=DTYPE,
    safety_checker=None, local_files_only=True,
).to(DEV)
pipe.set_progress_bar_config(disable=True)

PROMPT = "a photograph of an astronaut riding a horse on a beach at sunset"
SEED = 1234
print("model, prompt and seed are fixed for everything below.")'''),

    ("md", """## One model, one prompt, one seed. Only the guidance scale changes.

Nothing about the network differs between these images. Same weights, same prompt, same noise. The
only variable is how far the sampler extrapolates away from the unconditional prediction."""),

    ("code", '''SCALES = [1.0, 2.0, 3.5, 5.0, 7.5, 12.0, 20.0]
images = []
for s in SCALES:
    g = torch.Generator(DEV).manual_seed(SEED)
    images.append(pipe(PROMPT, num_inference_steps=40, guidance_scale=s, generator=g).images[0])
    print(f"guidance {s:5.1f}: done")'''),

    ("code", '''fig, axes = plt.subplots(1, len(SCALES), figsize=(3 * len(SCALES), 3.6))
for ax, s, im in zip(axes, SCALES, images):
    ax.imshow(im); ax.set_title(f"guidance {s}", fontsize=11); ax.axis("off")
plt.suptitle("Identical weights, prompt and seed. Only the sampler setting differs.", fontsize=13)
plt.tight_layout(); plt.show()'''),

    ("md", """At guidance 1.0 the model essentially ignores the prompt. By 7.5 it follows it closely.
By 20 it is over-saturated and losing plausibility.

These are not small differences. If you were shown two of these images and told one came from a
better architecture, you would probably believe it."""),

    ("md", """## Now measure it

Judging by eye is what the field tries to avoid, so let us put numbers on it. We use two cheap
proxies: CLIP similarity between image and prompt, which stands in for prompt adherence, and the
distance from the guidance-1.0 image, which measures how far the sampler setting alone has moved the
output."""),

    ("code", '''from transformers import CLIPProcessor, CLIPModel

clip = CLIPModel.from_pretrained("openai/clip-vit-base-patch32", local_files_only=True).to(DEV).eval()
proc = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32", local_files_only=True)

@torch.no_grad()
def clip_score(img, text):
    inp = proc(text=[text], images=img, return_tensors="pt", padding=True).to(DEV)
    out = clip(**inp)
    i = out.image_embeds / out.image_embeds.norm(dim=-1, keepdim=True)
    t = out.text_embeds / out.text_embeds.norm(dim=-1, keepdim=True)
    return float((i @ t.T).squeeze())

base = np.asarray(images[0], np.float64)
scores = [clip_score(im, PROMPT) for im in images]
drift = [float(np.abs(np.asarray(im, np.float64) - base).mean()) for im in images]

print(f"{'guidance':>9} {'CLIP score':>11} {'pixel drift from g=1.0':>24}")
for s, c, d in zip(SCALES, scores, drift):
    print(f"{s:9.1f} {c:11.4f} {d:24.1f}")'''),

    ("code", '''fig, ax1 = plt.subplots(figsize=(9, 4.6))
ax1.plot(SCALES, scores, "o-", color="#3d5a99", label="CLIP score (prompt adherence)")
ax1.set_xlabel("guidance scale"); ax1.set_ylabel("CLIP score", color="#3d5a99")
ax1.tick_params(axis="y", labelcolor="#3d5a99")

ax2 = ax1.twinx()
ax2.plot(SCALES, drift, "s--", color="#b8546f", label="pixel drift from guidance 1.0")
ax2.set_ylabel("mean abs pixel difference", color="#b8546f")
ax2.tick_params(axis="y", labelcolor="#b8546f")

plt.title("One frozen model. The sampler setting alone drives both curves.", fontsize=12)
fig.tight_layout(); plt.show()

span = max(scores) - min(scores)
print(f"\\nCLIP score spans {span:.4f} across guidance settings, on a single frozen model.")'''),

    ("md", """## Why this decides how the atlas reports numbers

Prompt adherence rises steeply and then flattens or falls, while the image keeps moving. The peak
sits somewhere in the middle, and where exactly depends on the prompt, the sampler and the step
count.

Now consider what that means for a published comparison. A paper reports its method at its
best-tuned guidance against a baseline at that baseline's default. Both numbers are real. The gap
between them is not attributable to the method.

This is not hypothetical. In the ImageNet results the atlas tracks:

- One paper reports the same model at 1.65, 1.49, 1.14 and 1.06 under four guidance methods. That
  0.59 swing is larger than the gap between most competing architectures in the same table.
- The pixel-space result frequently cited as evidence that tokenizers are unnecessary uses roughly
  2B parameters against 675M to 839M for the latent models it is compared with, and a different
  guidance technique, so two confounds move at once.
- Three separate papers report the same public checkpoint at 0.66, 0.67 and 0.82 on the same
  text-to-image benchmark, purely from differences in prompt rewriting and sampler settings.

So the [comparison page](/compare) records the guidance method, training budget and parameter count
beside every number, and leads with what the numbers cannot support rather than with a ranking. Not
out of caution, but because a table that hides these columns is making a claim its own data does not
carry.

**The practical rule:** before believing a headline, check three columns. Guidance method, training
budget, parameter count. If any differs from the baseline, the gap is not evidence for the idea being
sold. The within-paper ablation, where those are held fixed, is almost always the more informative
number, and almost always smaller than the abstract implies."""),
]
