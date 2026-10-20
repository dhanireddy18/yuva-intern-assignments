"""Regression metrics and bootstrap confidence intervals (NumPy only)."""
from __future__ import annotations

from typing import Callable

import numpy as np


def regression_report(y_true, y_pred) -> dict[str, float]:
    """Return RMSE, MAE, median absolute error and R-squared for a set of predictions.

    R-squared is 1 - SS_res / SS_tot, so it can be negative for a model that is worse
    than always predicting the mean.
    """
    y_true = np.asarray(y_true, dtype=float)
    y_pred = np.asarray(y_pred, dtype=float)
    if y_true.shape != y_pred.shape:
        raise ValueError(f"shape mismatch: {y_true.shape} vs {y_pred.shape}")
    if y_true.size == 0:
        raise ValueError("empty input")
    err = y_true - y_pred
    ss_res = float(np.sum(err ** 2))
    ss_tot = float(np.sum((y_true - y_true.mean()) ** 2))
    return {
        "rmse": float(np.sqrt(np.mean(err ** 2))),
        "mae": float(np.mean(np.abs(err))),
        "median_ae": float(np.median(np.abs(err))),
        "r2": float(1.0 - ss_res / ss_tot) if ss_tot > 0 else float("nan"),
    }


def bootstrap_ci(values, statistic: Callable = np.mean, n_boot: int = 2000, ci: float = 0.95, seed: int = 42) -> tuple[float, float]:
    """Percentile bootstrap confidence interval of ``statistic`` for a 1-D sample.

    Returns ``(low, high)``. The result is reproducible for a given ``seed``.
    """
    values = np.asarray(values, dtype=float)
    if values.ndim != 1 or values.size < 2:
        raise ValueError("values must be a 1-D array with at least 2 observations")
    if not 0 < ci < 1:
        raise ValueError("ci must be between 0 and 1")
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, values.size, size=(n_boot, values.size))
    stats = np.apply_along_axis(statistic, 1, values[idx])
    alpha = (1 - ci) / 2
    low, high = np.quantile(stats, [alpha, 1 - alpha])
    return float(low), float(high)
