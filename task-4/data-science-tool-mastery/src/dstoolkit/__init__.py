"""dstoolkit: small, tested helpers used throughout the Data Science Tool Mastery project."""
from .metrics import bootstrap_ci, regression_report
from .plotting import PALETTE, save_figure, set_portfolio_style
from .sql_helpers import df_to_sqlite, explain, run_query
from .stats_helpers import benjamini_hochberg, fisher_z_ci, holm_adjust
from .transformers import ClinicalFeatureAdder

__version__ = "1.0.0"
__all__ = [
    "ClinicalFeatureAdder", "regression_report", "bootstrap_ci",
    "df_to_sqlite", "run_query", "explain", "set_portfolio_style", "save_figure", "PALETTE",
    "holm_adjust", "benjamini_hochberg", "fisher_z_ci",
]
