# Notebooks

Runnable notebooks with real outputs, executed on an A100 80GB. Sources live in `specs/*.py`
as plain Python so they stay reviewable in a diff; `build.py` turns them into executed
`.ipynb`, and `publish.sh` renders those to HTML for the site.

```bash
python notebooks/build.py            # build + execute all
python notebooks/build.py latents    # just one
./notebooks/publish.sh               # render to site/public/notebooks/
```

## Third-party code

`rae.ipynb` needs the official RAE implementation, which is not vendored here. It is cloned
to `external/RAE` (gitignored) along with its released decoder checkpoints:

```bash
git clone https://github.com/bytetriper/RAE.git external/RAE
cd external/RAE && pip install omegaconf timm einops
python -c "
from huggingface_hub import hf_hub_download
for f in ['decoders/dinov2/wReg_base/ViTXL_n08/model.pt',
          'decoders/siglip2/base_p16_i256/ViTXL_n08/model.pt',
          'decoders/mae/base_p16/ViTXL_n08/model.pt',
          'stats/dinov2/wReg_base/imagenet1k/stat.pt',
          'stats/siglip2/base_p16_i256/ImageNet1k/stat.pt',
          'stats/mae/base_p16/ImageNet1k/stat.pt']:
    hf_hub_download('nyu-visionx/RAE-collections', f, local_dir='models')"
```
