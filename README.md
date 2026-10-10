<div align="center">

# Misinformation Diffusion

### How does network structure shape the spread of information?

A reproducible Python study of diffusion on random, scale-free and small-world networks.

[![Checks](https://github.com/kechavious/misinfomation/actions/workflows/checks.yml/badge.svg)](https://github.com/kechavious/misinfomation/actions/workflows/checks.yml)
![Python](https://img.shields.io/badge/Python-3.12-2563eb)
[![License: MIT](https://img.shields.io/badge/License-MIT-64748b.svg)](LICENSE)

[Quick start](#quick-start) · [Results](#reference-results) · [Methodology](docs/methodology.md) · [Paper (PDF)](docs/paper.pdf) · [Notebook](notebooks/misinformation_analysis.ipynb)

</div>

![ER and BA diffusion curves with uncertainty bands](results/plots/adoption_comparison.png)

## Research question

Can differences in network topology change the transmission probability needed
for widespread adoption within a fixed time horizon?

This project explores that question using synthetic networks and a discrete-time
susceptible–infected (SI) model. It provides inspectable simulation code,
independent graph replicates, uncertainty bands and per-trial records. It is a
study of a simplified diffusion mechanism, not a detector or calibrated predictor
of real-world misinformation.

## Research report

Read the [full paper](docs/paper.md) or download the [typeset PDF](docs/paper.pdf).
The report explains the SI model, experimental design, observed results and
limits of interpretation. Its tables are generated from verified result CSVs.
See [report build instructions](reports/README.md) to reproduce it.

## What the project demonstrates

- **Network simulation:** approximately degree-matched Erdős–Rényi (ER) and
  Barabási–Albert (BA) networks, plus a Watts–Strogatz (WS) rewiring comparison.
- **Reproducible experiments:** deterministic seeds for every graph and trial,
  a command-line runner and metadata with CSV integrity hashes.
- **Statistical analysis:** graph-level uncertainty, descriptive logistic fits
  and an explicit distinction between the fitted midpoint and 80% adoption.
- **Engineering:** an installable Python package, a notebook using the shared
  model, behavioral tests and automated GitHub Actions checks.

## Quick start

Python **3.12** is the tested runtime. From the repository root:

```bash
git clone https://github.com/kechavious/misinfomation.git
cd misinfomation
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install --no-deps -e .
```

Run a small experiment first:

```bash
misinformation-study --nodes 60 --runs 3 --graphs 2 --points 5 \
  --clustering --output /tmp/diffusion-smoke
```

Reproduce the published reference results:

```bash
misinformation-study --clustering --output results
```

Run tests:

```bash
python -m unittest discover -s tests -v
```

No credentials, downloaded datasets, external services or GPU are needed.
See [reproduction instructions](docs/reproduction.md) for larger sweeps and
notebook setup. On Windows, activate with `.venv\Scripts\activate` and choose a
writable output directory instead of `/tmp`.

## Reference results

The reference run uses **800 nodes**, **5 independent graphs** per configuration,
**30 diffusion trials** per graph and probability, **21 probabilities**, **10
rounds** and master seed **42**. Across seven configurations this produces
**22,050 trial outcomes**. ER and BA have approximately matched mean degree 8.

| Network | Fitted 50% midpoint | First sampled p reaching 80% | Mean clustering |
| --- | ---: | ---: | ---: |
| ER | 0.139 | 0.20 | 0.010 |
| BA | 0.111 | 0.20 | 0.041 |

BA has an earlier fitted midpoint in this experiment. Both topologies reach the
80% criterion at `p=0.20` on the sampled grid. These summaries answer different
questions; an earlier midpoint does not establish an earlier 80% threshold.
The curves use pointwise 95% Student-t intervals across graph-replicate means.
Five graph replicates provide a coarse uncertainty estimate.

![Illustrative ER and BA network structures](results/plots/network_topologies.png)

### A rewiring comparison

![Watts–Strogatz rewiring and the finite-horizon adoption threshold](results/plots/clustering_experiment.png)

The regular WS lattice (`β=0`) and lightly rewired setting (`β=0.01`) do not
reach 80% mean adoption within ten rounds anywhere on the sampled probability
grid. Other settings reach it at 0.35 (`β=0.1`) or 0.20 (`β=0.5, 1`). Rewiring
changes clustering **and** path lengths, so this comparison does not isolate a
causal effect of clustering.

Download [summary statistics](results/csv/summary.csv),
[all trial outcomes](results/csv/trials.csv) and
[experiment metadata](results/metadata.json). See the
[full paper](docs/paper.md) for interpretation.

## Model in brief

One random node starts adopted. In each round, adopted nodes independently
attempt to transmit to susceptible neighbors with probability `p` per edge.
Updates are synchronous; adoption is permanent and attempts repeat each round.
We measure the adopted fraction after the configured horizon.

The **empirical 80% threshold** is the first sampled probability with mean
adoption at least 0.8. The **logistic midpoint** is the fitted probability at 50%
adoption. It is a descriptive curve summary, not a replacement for the threshold.

Read the [full methodology](docs/methodology.md) for assumptions, uncertainty,
network parameters and limitations.

## Project map

```text
analysis/              Experiment runner, logistic fitting and metrics
simulations/           Seeded graph generation and one shared diffusion model
tests/                 Behavioral and end-to-end replay checks
notebooks/             Guided exploration of the model and reference results
results/               Current CSVs, figures and experiment metadata
docs/                  Current paper (Markdown/PDF), methods and reproduction guide
reports/               Paper template and build documentation
scripts/               Verified paper generation and PDF build
.github/workflows/     Automated tests and CLI smoke experiment
```

## Limitations and next steps

Synthetic static networks, uniform transmission probability and permanent
adoption simplify behavior. The model does not represent content truth,
recommendation algorithms, recovery, moderation or user heterogeneity. The
reference experiment does not establish universal platform behavior, a
thermodynamic phase transition, or causal clustering effects.

Useful extensions include more graph replicates, finer probability grids,
finite-horizon sensitivity, recovery dynamics and calibration against real
observations. Each would require new experiments and explicit assumptions.

## Background and attribution

Originally developed as coursework at New York University. The current paper
replaces the earlier writeup. Previous papers, slides and results remain
available in [Git history](docs/history.md); the current project tree contains
one published version of the study.

Related literature motivates the topic; these works do not validate this model:

- Watts, D. J. (2002). *A simple model of global cascades on random networks.*
  [PNAS](https://doi.org/10.1073/pnas.082090499).
- Centola, D. (2010). *The spread of behavior in an online social network experiment.*
  [Science](https://doi.org/10.1126/science.1185231).
- Daley, D. J., & Kendall, D. G. (1965). *Epidemics and rumours.*
  [Nature](https://doi.org/10.1038/2041118a0).

To cite the software, use [CITATION.cff](CITATION.cff) or GitHub's “Cite this repository” control. Include the experiment parameters when citing results.

MIT licensed. See [LICENSE](LICENSE). Contributions: [CONTRIBUTING.md](CONTRIBUTING.md).
