"""Prediction errors and an explicitly defined empirical threshold."""
import numpy as np


def _pairs(true, pred):
    a, b = np.asarray(true, dtype=float), np.asarray(pred, dtype=float)
    if a.ndim != 1 or a.size == 0 or a.shape != b.shape:
        raise ValueError("Provide nonempty paired one-dimensional values")
    if not np.isfinite(a).all() or not np.isfinite(b).all():
        raise ValueError("Values must be finite")
    return a, b


def mse(true, pred):
    a, b = _pairs(true, pred)
    return float(np.mean((a - b)**2))


def mae(true, pred):
    a, b = _pairs(true, pred)
    return float(np.mean(np.abs(a - b)))


def empirical_threshold(p_values, adoption, threshold=0.8):
    """First tested p reaching threshold; None means not reached on this grid."""
    p, a = _pairs(p_values, adoption)
    if not 0 <= threshold <= 1 or np.any(np.diff(p) <= 0):
        raise ValueError("Use an increasing grid and a threshold in [0, 1]")
    hits = np.flatnonzero(a >= threshold)
    return float(p[hits[0]]) if len(hits) else None
