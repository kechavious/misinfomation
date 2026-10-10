"""Descriptive clustering and empirical adoption threshold."""
import networkx as nx
from simulations.utils import sweep_probabilities
from analysis.compute_metrics import empirical_threshold


def clustering_vs_tipping(G, p_values, runs=20, sim_func=None, seed=42):
    curve = sweep_probabilities(G, p_values, runs, sim_func=sim_func, seed=seed)
    return nx.average_clustering(G), empirical_threshold(list(curve), list(curve.values()))
