import numpy as np
from scipy.optimize import curve_fit

def logistic(x, alpha, p0):
    """
    Logistic function for modeling nonlinear adoption A(p).
    """
    return 1 / (1 + np.exp(-alpha * (x - p0)))


def fit_logistic(p_vals, adoption_vals):
    """
    Fit logistic curve to empirical adoption data.

    Returns:
        alpha (float): steepness parameter
        p0 (float): tipping point estimate
    """
    p_vals = np.array(p_vals)
    adoption_vals = np.array(adoption_vals)

    initial_guess = [10, 0.2]  # alpha, p0

    params, _ = curve_fit(logistic, p_vals, adoption_vals, p0=initial_guess)
    alpha, p0 = params

    return alpha, p0
