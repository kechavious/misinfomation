import networkx as nx

def build_er_network(n=2000, p_edge=0.01, seed=None):
    """
    Build an Erdős–Rényi random graph G(n, p_edge).
    """
    return nx.erdos_renyi_graph(n, p_edge, seed=seed)


def build_ba_network(n=2000, m=3, seed=None):
    """
    Build a Barabási–Albert scale-free network.
    """
    return nx.barabasi_albert_graph(n, m, seed=seed)

