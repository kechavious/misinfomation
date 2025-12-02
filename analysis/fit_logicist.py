import numpy as np
from scipy.optimize import curve_fit

def logistic(x, alpha, p0):
    """
    Logistic function:
    A(p) = 1 / (1 + e^{-α(p - p0)})
    """
    return 1 / (1 + np.exp(-alpha * (x - p0)))


def fit_logistic(p_vals, adoption_vals):
    """
    Fit logistic curve to empirical adoption data.

    Returns:
    - alpha: slope parameter
    - p0: estimated tipping point (inflection)
    """
    p_vals = np.array(p_vals)
    adoption_vals = np.array(adoption_vals)

    initial_guess = [10, 0.2]  # slope, center

    params, _ = curve_fit(logistic, p_vals, adoption_vals, p0=initial_guess)
    alpha, p0 = params
    return alpha, p0
