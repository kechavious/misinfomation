"""Network constructors with comparable expected mean degree."""
import networkx as nx


def build_er_network(n=800, p_edge=0.01, seed=None):
    return nx.erdos_renyi_graph(n, p_edge, seed=seed)


def build_ba_network(n=800, m=4, seed=None):
    return nx.barabasi_albert_graph(n, m, seed=seed)
