"""Statistical helpers: multiple-testing corrections and a correlation confidence interval (NumPy only)."""
from __future__ import annotations

import numpy as np


def holm_adjust(p_values) -> np.ndarray:
    """Holm-Bonferroni adjusted p-values (controls the family-wise error rate), in the original order."""
    p = np.asarray(p_values, dtype=float)
    if p.ndim != 1 or p.size == 0 or np.any((p < 0) | (p > 1)):
        raise ValueError("p_values must be a non-empty 1-D array of probabilities")
    order = np.argsort(p)
    m = p.size
    adjusted = np.minimum(1.0, p[order] * (m - np.arange(m)))
    adjusted = np.maximum.accumulate(adjusted)                 # enforce monotonicity
    out = np.empty(m)
    out[order] = adjusted
    return out


def benjamini_hochberg(p_values) -> np.ndarray:
    """Benjamini-Hochberg adjusted p-values (controls the false discovery rate), in the original order."""
    p = np.asarray(p_values, dtype=float)
    if p.ndim != 1 or p.size == 0 or np.any((p < 0) | (p > 1)):
        raise ValueError("p_values must be a non-empty 1-D array of probabilities")
    order = np.argsort(p)
    m = p.size
    adjusted = np.minimum(1.0, p[order] * m / (np.arange(m) + 1))
    adjusted = np.minimum.accumulate(adjusted[::-1])[::-1]     # enforce monotonicity from the largest p downwards
    out = np.empty(m)
    out[order] = adjusted
    return out


def fisher_z_ci(r: float, n: int, z_crit: float = 1.959964) -> tuple[float, float]:
    """Approximate 95% confidence interval for a Pearson correlation using Fisher's z transformation."""
    if not -1 < r < 1:
        raise ValueError("r must be strictly between -1 and 1")
    if n < 4:
        raise ValueError("n must be at least 4")
    z, se = np.arctanh(r), 1.0 / np.sqrt(n - 3)
    return float(np.tanh(z - z_crit * se)), float(np.tanh(z + z_crit * se))
