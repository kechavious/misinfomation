"""Generate the current research report from verified reference artifacts."""
import argparse
import hashlib
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
REFERENCE = dict(nodes=800, runs=30, graphs=5, points=21, rounds=10, seed=42, clustering=True)


def load_reference(root=ROOT):
    results = root/'results'
    meta = json.loads((results/'metadata.json').read_text())
    if meta['model'] != 'synchronous SI; per-edge probability; repeated attempts; one random source':
        raise ValueError('This paper interprets the SI reference model; revise the template for a changed model')
    if meta['parameters'] != REFERENCE:
        raise ValueError('This paper interprets the reference design; revise the template for a changed experiment')
    expected_files = {'csv/trials.csv', 'csv/network_properties.csv', 'csv/adoption_curves.csv', 'csv/summary.csv'}
    if set(meta['csv_sha256']) != expected_files:
        raise ValueError('Reference metadata must identify all four CSV artifacts')
    for filename, expected in meta['csv_sha256'].items():
        if hashlib.sha256((results/filename).read_bytes()).hexdigest() != expected:
            raise ValueError(f'Reference integrity check failed: {filename}')
    trials = pd.read_csv(results/'csv/trials.csv')
    props = pd.read_csv(results/'csv/network_properties.csv')
    curves = pd.read_csv(results/'csv/adoption_curves.csv')
    summary = pd.read_csv(results/'csv/summary.csv')
    names = {'ER', 'BA', 'WS β=0', 'WS β=0.01', 'WS β=0.1', 'WS β=0.5', 'WS β=1'}
    for frame in [trials, props, curves, summary]:
        if set(frame.network) != names:
            raise ValueError('Reference data must contain all seven configurations')
    groups = trials.groupby(['network', 'graph', 'p'])
    if len(trials) != 7*REFERENCE['graphs']*REFERENCE['points']*REFERENCE['runs']:
        raise ValueError('Unexpected reference trial count')
    if len(groups) != 7*REFERENCE['graphs']*REFERENCE['points'] or not (groups.size() == REFERENCE['runs']).all():
        raise ValueError('Reference trial groups are incomplete')
    if len(props) != 7*REFERENCE['graphs'] or len(curves) != 7*REFERENCE['points'] or len(summary) != 7:
        raise ValueError('Reference summaries are incomplete')
    if not (props.nodes == REFERENCE['nodes']).all():
        raise ValueError('Reference node counts do not match metadata')
    for _, group in curves.groupby('network'):
        if not np.allclose(group.sort_values('p').p, np.linspace(0,1,REFERENCE['points'])):
            raise ValueError('Reference probability grid does not match metadata')
    return meta, trials, props, curves, summary


def generate(root=ROOT):
    meta, trials, props, curves, summary = load_reference(root)
    lookup = summary.set_index('network')
    params = meta['parameters']
    def curve(name, p):
        return curves[(curves.network == name) & np.isclose(curves.p, p)].iloc[0]
    def value(name, column, digits=3):
        return f'{lookup.loc[name,column]:.{digits}f}'
    rows = ['| Network | Mean degree | Clustering | Fitted midpoint | Sampled 80% threshold |',
            '| :--- | ---: | ---: | ---: | ---: |']
    for _, row in summary.iterrows():
        label = row.network if not row.network.startswith('WS') else 'WS ($\\beta='+row.network.split('=')[1]+'$)'
        midpoint = '-' if pd.isna(row.logistic_midpoint) else f'{row.logistic_midpoint:.3f}'
        threshold = 'NR' if pd.isna(row.threshold_80) else f'{row.threshold_80:.2f}'
        rows.append(f'| {label} | {row.mean_degree:.3f} | {row.mean_clustering:.3f} | {midpoint} | {threshold} |')
    adoption_rows = ['| Probability | ER mean [95% interval] | BA mean [95% interval] |',
                     '| ---: | ---: | ---: |']
    for p in [.10,.15,.20]:
        cells=[]
        for name in ['ER','BA']:
            c=curve(name,p)
            cells.append(f"{c['mean']*100:.1f} [{c.ci_low*100:.1f}, {c.ci_high*100:.1f}]")
        adoption_rows.append(f'| {p:.2f} | {cells[0]} | {cells[1]} |')
    values = {
        'DATE':meta['generated_at_utc'][:10], 'NODES':str(params['nodes']),
        'GRAPHS':str(params['graphs']), 'RUNS':str(params['runs']),
        'POINTS':str(params['points']), 'ROUNDS':str(params['rounds']),
        'SEED':str(params['seed']), 'TOTAL':f'{len(trials):,}',
        'GRID_STEP':f"{1/(params['points']-1):.2f}", 'PYTHON_VERSION':meta['python'],
        'ER_MIDPOINT':value('ER','logistic_midpoint'), 'BA_MIDPOINT':value('BA','logistic_midpoint'),
        'ER_THRESHOLD':value('ER','threshold_80',2),
        'ER_DEGREE':value('ER','mean_degree'), 'BA_DEGREE':value('BA','mean_degree'),
        'ER_COMPONENT':f"{props[props.network=='ER'].largest_component_fraction.mean():.5f}",
        'ER_P10':f"{curve('ER',.10)['mean']*100:.1f}%", 'BA_P10':f"{curve('BA',.10)['mean']*100:.1f}%",
        'ER_P15':f"{curve('ER',.15)['mean']*100:.1f}%", 'BA_P15':f"{curve('BA',.15)['mean']*100:.1f}%",
        'WS_ZERO_P1':f"{curve('WS β=0',1)['mean']:.5f}",
        'WS_LOW_P1':f"{curve('WS β=0.01',1)['mean']:.5f}",
        'WS_MED_THRESHOLD':value('WS β=0.1','threshold_80',2),
        'ER_SLOPE':value('ER','logistic_slope',2), 'BA_SLOPE':value('BA','logistic_slope',2),
        'ER_MSE':f"{lookup.loc['ER','fit_mse']:.6f}", 'BA_MSE':f"{lookup.loc['BA','fit_mse']:.6f}",
        'SUMMARY_TABLE':'\n'.join(rows), 'ADOPTION_TABLE':'\n'.join(adoption_rows),
    }
    template=(root/'reports/paper.md.in').read_text()
    def replace(match):
        key=match.group(1)
        if key not in values:
            raise ValueError(f'Unknown paper field: {key}')
        return values[key]
    return re.sub(r'\{\{([A-Z_0-9]+)\}\}',replace,template)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true',help='fail if generated Markdown is stale')
    args=parser.parse_args()
    content=generate()
    target=ROOT/'docs/paper.md'
    if args.check:
        if not target.exists() or target.read_text()!=content:
            parser.exit(1,'Paper is stale; run python scripts/generate_paper.py\n')
        print('PASS: paper matches verified reference data and template')
    else:
        target.write_text(content)
        print(f'Generated {target.relative_to(ROOT)} from verified reference CSVs')


if __name__=='__main__':
    main()
