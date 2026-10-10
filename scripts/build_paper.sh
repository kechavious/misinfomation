#!/usr/bin/env bash
# Run with the project Python environment activated. No simulation is rerun.
set -euo pipefail
cd "$(dirname "$0")/.."
python scripts/generate_paper.py
pandoc docs/paper.md \
  --from=markdown --standalone --number-sections \
  --lua-filter=scripts/paper.lua \
  --resource-path=docs --pdf-engine=pdflatex \
  -V documentclass=article -V fontsize=11pt -V geometry:margin=1in \
  -V colorlinks=true -V linkcolor=blue -V urlcolor=blue \
  -o docs/paper.pdf
printf '%s\n' 'Built docs/paper.pdf'
