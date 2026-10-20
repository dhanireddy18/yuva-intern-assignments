"""Consistent, colour-blind-safe plotting style and a safe figure saver."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt

# Okabe-Ito palette: distinguishable for the most common forms of colour-vision deficiency
PALETTE = ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#E69F00", "#56B4E9", "#F0E442", "#000000"]


def set_portfolio_style() -> None:
    """Apply one house style to every chart."""
    plt.rcParams.update({
        "figure.dpi": 100, "savefig.dpi": 150, "figure.autolayout": False,
        "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.alpha": 0.25,
        "axes.titlesize": 12, "axes.titleweight": "bold", "axes.labelsize": 10,
        "axes.prop_cycle": plt.cycler(color=PALETTE),
        "legend.frameon": False, "font.size": 10,
    })


def save_figure(fig, path, dpi: int = 150) -> Path:
    """Save a figure, creating the folder if needed; returns the path."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=dpi, bbox_inches="tight")
    return path
