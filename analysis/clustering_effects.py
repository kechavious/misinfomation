import networkx as nx
from simulation.utils import sweep_probabilities
from analysis.fit_logistic import fit_logistic

def clustering_vs_tipping(G, p_values, runs=20, sim_func=None):
    """
    Compute:
        - average clustering coefficient
        - tipping point from logistic fit

    Returns:
        (clustering_coefficient, tipping_point)
    """

    clustering = nx.average_clustering(G)

    curve = sweep_probabilities(G, p_values, runs, sim_func=sim_func)
    p_list = list(curve.keys())
    adoption_list = list(curve.values())

    _, p0 = fit_logistic(p_list, adoption_list)

    return clustering, p0

