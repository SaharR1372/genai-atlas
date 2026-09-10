#!/usr/bin/env bash
# Render the executed notebooks to static HTML for the site.
# Run after notebooks/build.py, from the repo root.
set -euo pipefail
PY=/home/exx/anaconda3/envs/dediffusion/bin/python
mkdir -p site/public/notebooks
for nb in notebooks/*.ipynb; do
  n=$(basename "$nb" .ipynb)
  "$PY" -m nbconvert --to html --template lab \
      --output-dir site/public/notebooks --output "$n.html" "$nb"
done
echo "published $(ls site/public/notebooks/*.html | wc -l) notebooks"
