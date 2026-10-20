"""Custom scikit-learn transformers."""
from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class ClinicalFeatureAdder(BaseEstimator, TransformerMixin):
    """Add domain-knowledge features to the diabetes data frame.

    The transformer is stateless (nothing is learned from the data), so it cannot leak
    information from the test set. It never modifies its input.

    Parameters
    ----------
    bmi_cutoffs : tuple of float, default=(25.0, 30.0)
        BMI limits for ``bmi_band`` (the WHO overweight and obese limits).

    Notes
    -----
    Two columns are added: ``ldl_hdl_ratio`` (s2 divided by s3, a common cardiovascular risk
    ratio) and ``bmi_band`` (0 = below the first cutoff, 1 = between the cutoffs, 2 = at or
    above the second cutoff).
    """

    REQUIRED = ("bmi", "s2", "s3")

    def __init__(self, bmi_cutoffs: tuple = (25.0, 30.0)):
        self.bmi_cutoffs = bmi_cutoffs

    def fit(self, X: pd.DataFrame, y=None) -> "ClinicalFeatureAdder":
        """Validate the input columns and remember their names; nothing is learned from the data."""
        self._check(X)
        self.feature_names_in_ = np.asarray(X.columns, dtype=object)
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Return a copy of ``X`` with the ``ldl_hdl_ratio`` and ``bmi_band`` columns added."""
        self._check(X)
        out = X.copy()
        out["ldl_hdl_ratio"] = out["s2"] / out["s3"]
        out["bmi_band"] = np.digitize(out["bmi"], self.bmi_cutoffs)
        return out

    def get_feature_names_out(self, input_features=None) -> np.ndarray:
        """Names of the output columns: the input columns followed by the two new ones."""
        return np.append(self.feature_names_in_, ["ldl_hdl_ratio", "bmi_band"])

    def _check(self, X):
        if not isinstance(X, pd.DataFrame):
            raise TypeError("ClinicalFeatureAdder expects a pandas DataFrame")
        missing = [c for c in self.REQUIRED if c not in X.columns]
        if missing:
            raise ValueError(f"missing required columns: {missing}")
