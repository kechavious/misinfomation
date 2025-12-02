import numpy as np

def normalize(values):
    """
    Normalize a list of values to sum to 1.
    """
    s = sum(values)
    return [v / s for v in values]


def sweep_probabilities(G, p_values, runs=20, sim_func=None):
    """
    Sweep over multiple p-values and compute average adoption rate.

    Parameters:
    - G: graph
    - p_values: list of probabilities
    - runs: number of iterations per probability
    - sim_func: diffusion simulation function

    Returns:
    - dict mapping p -> mean adoption rate
    """
    results = {}

    for p in p_values:
        trials = [sim_func(G, p) for _ in range(runs)]
        results[p] = np.mean(trials)

    return results

