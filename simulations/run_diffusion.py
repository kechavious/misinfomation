import random

def simulate_diffusion(G, p, num_rounds=10, seed=None):
    """
    Simulate misinformation diffusion on graph G.

    Parameters:
    - G: social network graph (NetworkX)
    - p: probability of resharing when exposed
    - num_rounds: number of propagation rounds

    Returns:
    - adoption_rate: fraction of nodes that reshared
    """

    if seed is not None:
        random.seed(seed)

    # pick random seed node
    start = random.choice(list(G.nodes()))
    exposed = {start}
    adopted = {start}

    for _ in range(num_rounds):
        new_exposed = set()

        for node in exposed:
            # resharing event
            if random.random() < p:
                adopted.add(node)
                for nbr in G.neighbors(node):
                    new_exposed.add(nbr)

        exposed = new_exposed

        if len(exposed) == 0:
            break

    return len(adopted) / len(G.nodes())

