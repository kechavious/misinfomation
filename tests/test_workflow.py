"""Behavioral checks for the model, uncertainty and reproducible outputs."""
import random
import tempfile
import unittest
from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd

from analysis.compute_metrics import empirical_threshold, mae, mse
from analysis.experiment import run_experiment, summarize
from analysis.fit_logistic import fit_logistic, logistic
from analysis.clustering_effects import clustering_vs_tipping
from simulations.run_diffusion import simulate_diffusion
from simulations.utils import sweep_probabilities


class DiffusionTests(unittest.TestCase):
    def test_zero_probability_and_zero_rounds(self):
        G = nx.path_graph(5)
        self.assertEqual(simulate_diffusion(G, 0, source=0), 0.2)
        self.assertEqual(simulate_diffusion(G, 1, num_rounds=0, source=0), 0.2)

    def test_synchronous_updates(self):
        G = nx.path_graph(5)
        self.assertEqual(simulate_diffusion(G, 1, num_rounds=1, source=0), 0.4)
        self.assertEqual(simulate_diffusion(G, 1, num_rounds=4, source=0), 1)

    def test_disconnected_nodes_remain_unreachable(self):
        G = nx.path_graph(3)
        G.add_nodes_from([3, 4])
        self.assertEqual(simulate_diffusion(G, 1, source=0), 0.6)

    def test_attempts_continue_after_a_quiet_round(self):
        # Random(0): first draw .844 fails, second .758 succeeds at p=.8.
        G = nx.path_graph(2)
        self.assertEqual(simulate_diffusion(G, .8, num_rounds=1, seed=0, source=0), .5)
        self.assertEqual(simulate_diffusion(G, .8, num_rounds=2, seed=0, source=0), 1)

    def test_seed_replay_and_global_rng_isolation(self):
        G = nx.erdos_renyi_graph(50, .1, seed=3)
        state = random.getstate()
        a = simulate_diffusion(G, .2, seed=7)
        self.assertEqual(a, simulate_diffusion(G, .2, seed=7))
        self.assertEqual(state, random.getstate())
        self.assertEqual(sweep_probabilities(G, [0,.2,1], seed=7),
                         sweep_probabilities(G, [0,.2,1], seed=7))

    def test_regular_lattice_horizon_matches_geometry(self):
        G = nx.watts_strogatz_graph(800, 8, 0, seed=42)
        for source in [0, 399]:
            self.assertEqual(simulate_diffusion(G, 1, num_rounds=10, source=source), 81/800)

    def test_invalid_inputs(self):
        for G, p, rounds in [(nx.Graph(), .2, 10), (nx.path_graph(2), -1, 10),
                             (nx.path_graph(2), 1.1, 10), (nx.path_graph(2), .2, -1),
                             (nx.DiGraph([(0,1)]), .2, 10)]:
            with self.assertRaises(ValueError):
                simulate_diffusion(G, p, rounds)


class AnalysisTests(unittest.TestCase):
    def test_midpoint_is_not_empirical_threshold(self):
        x = np.linspace(0,1,101)
        y = logistic(x, 10, .2)
        alpha, midpoint = fit_logistic(x,y)
        self.assertAlmostEqual(alpha,10,places=5)
        self.assertAlmostEqual(midpoint,.2,places=5)
        self.assertEqual(empirical_threshold(x,y), .34)
        self.assertEqual(empirical_threshold([0,.5,1],[.1,.2,.7]),None)
        with self.assertRaises(ValueError):
            fit_logistic([0,.5,1],[.2,.2,.2])

    def test_unobserved_midpoint_is_not_reported(self):
        with self.assertRaises(ValueError):
            fit_logistic([0,.5,1],[.01,.1,.2])

    def test_metrics_do_not_silently_truncate(self):
        self.assertEqual(mse([0,1],[1,1]), .5)
        self.assertEqual(mae([0,1],[1,1]), .5)
        for a,b in [([],[]),([1,2],[1]),([float('nan')],[0])]:
            with self.assertRaises(ValueError):
                mse(a,b)

    def test_uncertainty_uses_graph_replicates(self):
        trials = pd.DataFrame([{'network':'ER','p':.5,'graph':g,'adoption':v}
                               for g,v in [(0,.1),(1,.9)] for _ in range(5)])
        a = summarize(trials).iloc[0]
        b = summarize(pd.concat([trials]*10)).iloc[0]
        self.assertEqual(a['mean'],.5)
        self.assertEqual(a.ci_low,b.ci_low)
        self.assertEqual(a.ci_high,b.ci_high)

    def test_clustering_helper_import_and_threshold(self):
        clustering, threshold = clustering_vs_tipping(nx.complete_graph(10), [0,.5,1],runs=2)
        self.assertEqual(clustering,1)
        self.assertIn(threshold,[.5,1])

    def test_end_to_end_replay(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            kwargs=dict(nodes=20,runs=2,graphs=2,points=3,rounds=3,seed=123,clustering=True)
            run_experiment(output=a,**kwargs)
            run_experiment(output=b,**kwargs)
            for name in ['trials.csv','adoption_curves.csv','network_properties.csv','summary.csv']:
                self.assertEqual((Path(a)/'csv'/name).read_bytes(),(Path(b)/'csv'/name).read_bytes())
            self.assertTrue((Path(a)/'plots'/'adoption_comparison.png').read_bytes().startswith(b'\x89PNG'))
            self.assertEqual(len(pd.read_csv(Path(a)/'csv'/'trials.csv')), 7*2*3*2)


if __name__ == '__main__':
    unittest.main()
