"""Discrete-time susceptible–infected diffusion on an undirected graph.

Each adopted node attempts to transmit to each susceptible neighbor with
probability p in every round. Adoption is permanent; updates are synchronous.
This is a stylized SI model, not a fitted model of misinformation behavior.
"""
import random
import networkx as nx


def simulate_diffusion(G, p, num_rounds=10, seed=None, source=None):
    """Return the adopted fraction, including one initially adopted source.

    Repeated attempts are allowed across rounds, including rounds in which no
    new adoption occurs. A local RNG keeps callers' random state unchanged.
    """
    if G.is_directed() or G.is_multigraph():
        raise ValueError("Use an undirected simple graph")
    if len(G) == 0:
        raise ValueError("Graph must contain at least one node")
    if not 0 <= p <= 1:
        raise ValueError("p must be between 0 and 1")
    if not isinstance(num_rounds, int) or num_rounds < 0:
        raise ValueError("num_rounds must be a nonnegative integer")
    rng = random.Random(seed)
    nodes = list(G.nodes())
    if source is None:
        source = rng.choice(nodes)
    elif source not in G:
        raise ValueError("source must be a graph node")
    adopted = {source}
    # Traverse graph insertion order rather than unordered sets for replay.
    for _ in range(num_rounds):
        new_adopted = set()
        for node in nodes:
            if node not in adopted:
                continue
            for neighbor in G[node]:
                if neighbor not in adopted and rng.random() < p:
                    new_adopted.add(neighbor)
        adopted.update(new_adopted)
        if len(adopted) == len(G):
            break
    return len(adopted) / len(G)
