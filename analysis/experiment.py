"""Reproduce comparison figures, per-trial records and experiment metadata."""
import argparse
import hashlib
import json
import platform
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from scipy.stats import t

from analysis.compute_metrics import empirical_threshold, mse
from analysis.fit_logistic import fit_logistic, logistic
from simulations.network import build_ba_network, build_er_network
from simulations.run_diffusion import simulate_diffusion

COLORS = {'ER': '#2563eb', 'BA': '#ea580c'}


def summarize(trials):
    """Student-t intervals across independent graph-replicate means.

    Diffusion runs within one graph are not treated as independent graphs.
    Intervals estimate mean adoption, not the spread of individual outcomes.
    """
    means = trials.groupby(['network', 'p', 'graph'], as_index=False).adoption.mean()
    records = []
    for (network, p), group in means.groupby(['network', 'p'], sort=False):
        y = group.adoption.to_numpy()
        half = float(t.ppf(0.975, len(y)-1) * np.std(y, ddof=1) / np.sqrt(len(y)))
        avg = float(np.mean(y))
        records.append({'network': network, 'p': p, 'mean': avg,
                        'ci_low': max(0, avg-half), 'ci_high': min(1, avg+half)})
    return pd.DataFrame(records)


def run_experiment(nodes=800, runs=30, graphs=5, points=21, rounds=10,
                   seed=42, clustering=False, output='results'):
    if nodes < 12 or runs < 2 or graphs < 2 or points < 3 or rounds < 1:
        raise ValueError('Require nodes >=12, runs/graphs >=2, points >=3 and rounds >=1')
    out = Path(output)
    (out/'csv').mkdir(parents=True, exist_ok=True)
    (out/'plots').mkdir(exist_ok=True)
    rng = np.random.default_rng(seed)
    probabilities = np.linspace(0, 1, points)
    builders = {
        'ER': lambda s: build_er_network(nodes, 8/(nodes-1), seed=s),
        'BA': lambda s: build_ba_network(nodes, 4, seed=s),
    }
    if clustering:
        for beta in [0, 0.01, 0.1, 0.5, 1]:
            builders[f'WS β={beta:g}'] = lambda s, b=beta: nx.watts_strogatz_graph(nodes, 8, b, seed=s)
    trials, properties = [], []
    for name, builder in builders.items():
        for rep in range(graphs):
            graph_seed = int(rng.integers(0, 2**32))
            G = builder(graph_seed)
            properties.append({'network': name, 'graph': rep, 'graph_seed': graph_seed,
                               'nodes': len(G), 'edges': G.number_of_edges(),
                               'mean_degree': 2*G.number_of_edges()/len(G),
                               'clustering': nx.average_clustering(G),
                               'largest_component_fraction': len(max(nx.connected_components(G), key=len))/len(G)})
            for p in probabilities:
                for trial in range(runs):
                    diffusion_seed = int(rng.integers(0, 2**32))
                    adoption = simulate_diffusion(G, float(p), rounds, seed=diffusion_seed)
                    trials.append({'network': name, 'graph': rep, 'graph_seed': graph_seed,
                                   'p': float(p), 'trial': trial, 'diffusion_seed': diffusion_seed,
                                   'adoption': adoption})
        print(f'Completed {name}: {graphs} graphs × {points} probabilities × {runs} runs', flush=True)
    trial_df, prop_df = pd.DataFrame(trials), pd.DataFrame(properties)
    curves = summarize(trial_df)
    rows = []
    for name in builders:
        curve = curves[curves.network == name].sort_values('p')
        try:
            alpha, midpoint = fit_logistic(curve.p, curve['mean'])
            error = mse(curve['mean'], logistic(curve.p, alpha, midpoint))
            fit_status = 'fitted'
        except (ValueError, RuntimeError) as exc:
            alpha = midpoint = error = None
            fit_status = str(exc)
        props = prop_df[prop_df.network == name]
        rows.append({'network': name, 'threshold_80': empirical_threshold(curve.p, curve['mean']),
                     'logistic_midpoint': midpoint, 'logistic_slope': alpha, 'fit_mse': error,
                     'fit_status': fit_status, 'mean_clustering': props.clustering.mean(),
                     'mean_degree': props.mean_degree.mean()})
    summary = pd.DataFrame(rows)
    for filename, frame in [('trials.csv', trial_df), ('network_properties.csv', prop_df),
                            ('adoption_curves.csv', curves), ('summary.csv', summary)]:
        frame.to_csv(out/'csv'/filename, index=False, float_format='%.10g')
    render(curves, summary, out, seed)
    hashes = {str(p.relative_to(out)): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted((out/'csv').glob('*.csv'))}
    metadata = {
        'generated_at_utc': datetime.now(timezone.utc).isoformat(),
        'model': 'synchronous SI; per-edge probability; repeated attempts; one random source',
        'parameters': dict(nodes=nodes, runs=runs, graphs=graphs, points=points,
                           rounds=rounds, seed=seed, clustering=clustering),
        'uncertainty': '95% Student-t CI across graph-replicate mean adoption; clipped to [0,1]',
        'threshold': 'first sampled p with mean adoption >=0.8; empty CSV value if not reached',
        'python': platform.python_version(),
        'packages': {p: version(p) for p in ['networkx', 'numpy', 'scipy', 'matplotlib', 'pandas']},
        'csv_sha256': hashes,
    }
    (out/'metadata.json').write_text(json.dumps(metadata, indent=2)+'\n')
    print(summary.to_string(index=False), flush=True)
    return curves, summary


def render(curves, summary, out, seed):
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 11,
                         'axes.spines.top': False, 'axes.spines.right': False,
                         'axes.titleweight': 'bold', 'figure.facecolor': '#ffffff',
                         'axes.labelcolor': '#334155', 'text.color': '#0f172a',
                         'savefig.dpi': 180})
    fig, ax = plt.subplots(figsize=(10, 6), layout='constrained')
    for name, color in COLORS.items():
        c = curves[curves.network == name].sort_values('p')
        ax.plot(c.p, c['mean'], color=color, linewidth=2.5, marker='o', markersize=4,
                label=f'{name} · mean adoption')
        ax.fill_between(c.p, c.ci_low, c.ci_high, color=color, alpha=0.12)
    ax.axhline(0.8, color='#64748b', linestyle='--', linewidth=1, label='80% adoption threshold')
    ax.set(xlabel='Per-edge transmission probability', ylabel='Adopted fraction after 10 rounds',
           ylim=(0, 1.03), xlim=(0, 1), title='How network structure shapes diffusion')
    ax.set_ylabel('Adopted fraction at the configured horizon')
    ax.grid(alpha=0.15)
    ax.legend(loc='lower right', frameon=False)
    fig.savefig(out/'plots'/'adoption_comparison.png')
    fig.savefig(out/'plots'/'adoption_comparison.svg')
    plt.close(fig)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), layout='constrained')
    for ax, (name, color) in zip(axes, COLORS.items()):
        # Show a seeded 100-node illustration, not the experiment graph.
        G = build_er_network(100, 8/99, seed) if name == 'ER' else build_ba_network(100, 4, seed)
        pos = nx.spring_layout(G, seed=seed)
        nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.13, width=0.7)
        nx.draw_networkx_nodes(G, pos, ax=ax, node_color=color,
                               node_size=[8+4*G.degree(v) for v in G])
        ax.set_title('ER · random connections' if name == 'ER' else 'BA · preferential attachment')
        ax.axis('off')
    fig.suptitle('Network illustrations · 100 nodes · size indicates degree', fontsize=12)
    fig.savefig(out/'plots'/'network_topologies.png')
    plt.close(fig)
    fig, ax = plt.subplots(figsize=(8, 5), layout='constrained')
    c = curves[curves.network == 'ER'].sort_values('p')
    row = summary[summary.network == 'ER'].iloc[0]
    ax.scatter(c.p, c['mean'], color=COLORS['ER'], label='Simulation mean')
    if pd.notna(row.logistic_midpoint):
        x = np.linspace(0, 1, 300)
        ax.plot(x, logistic(x, row.logistic_slope, row.logistic_midpoint), color='#0f172a', label='Descriptive logistic fit')
        ax.axvline(row.logistic_midpoint, color='#94a3b8', linestyle=':', label='Fitted midpoint (50%)')
    ax.axhline(0.8, color='#64748b', linestyle='--', label='80% threshold')
    ax.set(xlabel='Per-edge transmission probability', ylabel='Adopted fraction', title='Midpoint and adoption threshold measure different things')
    ax.legend(frameon=False, fontsize=9)
    fig.savefig(out/'plots'/'logistic_fit.png')
    plt.close(fig)
    ws = summary[summary.network.str.startswith('WS')]
    if len(ws):
        fig, ax = plt.subplots(figsize=(8, 5), layout='constrained')
        for _, row in ws.iterrows():
            if pd.notna(row.threshold_80):
                ax.scatter(row.mean_clustering, row.threshold_80, s=60, color='#7c3aed')
                ax.annotate(row.network, (row.mean_clustering, row.threshold_80), xytext=(5, 8), textcoords='offset points', fontsize=9)
        ax.set(xlabel='Mean clustering coefficient', ylabel='First sampled p reaching 80% adoption',
               title='Watts–Strogatz rewiring experiment')
        missing = ws.loc[ws.threshold_80.isna(), 'network'].tolist()
        if missing:
            ax.text(0.02, 0.95, '80% not reached: ' + ', '.join(missing), transform=ax.transAxes, va='top', fontsize=9)
        ax.text(0, -0.22, 'Rewiring also changes path lengths; this comparison does not isolate clustering causally.', transform=ax.transAxes, fontsize=9)
        fig.savefig(out/'plots'/'clustering_experiment.png', bbox_inches='tight')
        plt.close(fig)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--nodes', type=int, default=800)
    parser.add_argument('--runs', type=int, default=30, help='diffusion runs per graph and probability')
    parser.add_argument('--graphs', type=int, default=5, help='independent graphs per topology')
    parser.add_argument('--points', type=int, default=21)
    parser.add_argument('--rounds', type=int, default=10)
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--clustering', action='store_true', help='also compare five WS rewiring probabilities')
    parser.add_argument('--output', default='results')
    args = parser.parse_args()
    try:
        run_experiment(**vars(args))
    except ValueError as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    main()
