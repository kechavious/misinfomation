"""Descriptive logistic curve fitting; the midpoint is not an 80% threshold."""
import numpy as np
from scipy.optimize import curve_fit
from scipy.special import expit


def logistic(x, alpha, p0):
    return expit(alpha * (np.asarray(x) - p0))


def fit_logistic(p_vals, adoption_vals):
    x, y = np.asarray(p_vals, dtype=float), np.asarray(adoption_vals, dtype=float)
    if x.ndim != 1 or y.shape != x.shape or len(x) < 3:
        raise ValueError("Provide at least three paired one-dimensional samples")
    if not np.isfinite(x).all() or not np.isfinite(y).all():
        raise ValueError("Samples must be finite")
    if np.any((x < 0) | (x > 1)) or np.any((y < 0) | (y > 1)):
        raise ValueError("Probabilities and adoption must lie in [0, 1]")
    if np.ptp(y) < 1e-8:
        raise ValueError("A flat curve does not identify a logistic midpoint")
    if not np.min(y) < 0.5 < np.max(y):
        raise ValueError("Sampled curve does not bracket 50% adoption; midpoint not reported")
    params, _ = curve_fit(logistic, x, y, p0=[10, 0.2],
                          bounds=([0, 0], [1000, 1]), maxfev=10000)
    return tuple(float(v) for v in params)
