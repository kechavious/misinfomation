# Reproduce the study

Use Python 3.12 in a virtual environment from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install --no-deps -e .
python -m unittest discover -s tests -v
```

Quick functional check (small graphs, limited replication):

```bash
misinformation-study --nodes 60 --runs 3 --graphs 2 --points 5 \
  --clustering --output /tmp/diffusion-smoke
```

Reproduce the checked-in reference experiment:

```bash
misinformation-study --clustering --output results
```

Prefer a separate directory for exploratory runs:

```bash
misinformation-study --nodes 1000 --graphs 10 --runs 50 --points 41 \
  --seed 42 --clustering --output local-results
```

Runs execute sequentially on CPU. Costs scale with graph count, probability
count, trial count, horizon and graph size. Start small before large sweeps. No
API keys, datasets, external services or GPU are required. Plotting uses a
headless Matplotlib backend. Results include all graph and trial seeds.

## Notebook

```bash
python -m pip install '.[notebook]'
python -m ipykernel install --user --name misinformation \
  --display-name 'Python (misinformation)'
```

Open `notebooks/misinformation_analysis.ipynb` in a notebook-capable editor and
select that kernel. The notebook reads the current result CSVs and uses the same
simulation and analysis modules as the CLI; it does not contain a second model.
Its examples use fixed seeds and do not overwrite reference results.

## Outputs

| File | Contents |
| --- | --- |
| `csv/trials.csv` | Every graph/probability/trial outcome and random seeds |
| `csv/network_properties.csv` | Degree, clustering and component coverage |
| `csv/adoption_curves.csv` | Mean adoption and pointwise graph-level intervals |
| `csv/summary.csv` | 80% thresholds, logistic midpoints and fit errors |
| `metadata.json` | Parameters, model, versions and CSV integrity hashes |
| `plots/` | Comparison, topology illustrations, fit and optional WS plot |

To replay an individual row, build the corresponding network with its recorded
`graph_seed` and call `simulate_diffusion` with its `p`, `diffusion_seed` and the
recorded horizon. See `docs/methodology.md` for network parameters.
