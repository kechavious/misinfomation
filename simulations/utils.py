"""Small helpers for seeded probability sweeps."""
import random
import numpy as np
from simulations.run_diffusion import simulate_diffusion


def normalize(values):
    total = sum(values)
    if total <= 0:
        raise ValueError("Values must have a positive sum")
    return [v / total for v in values]


def sweep_probabilities(G, p_values, runs=20, sim_func=None, seed=42):
    if runs < 1:
        raise ValueError("runs must be positive")
    sim_func = sim_func or simulate_diffusion
    rng = random.Random(seed)
    return {p: float(np.mean([sim_func(G, p, seed=rng.randrange(2**32))
                            for _ in range(runs)])) for p in p_values}
