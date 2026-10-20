import unittest

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline

from dstoolkit import ClinicalFeatureAdder


def make_frame():
    return pd.DataFrame({
        "bmi": [24.9, 25.0, 29.9, 30.0, 18.0],
        "s2": [100.0, 120.0, 90.0, 150.0, 80.0],
        "s3": [50.0, 40.0, 45.0, 50.0, 40.0],
    })


class TestClinicalFeatureAdder(unittest.TestCase):
    def test_ratio_and_band_values(self):
        out = ClinicalFeatureAdder().fit_transform(make_frame())
        np.testing.assert_allclose(out["ldl_hdl_ratio"], [2.0, 3.0, 2.0, 3.0, 2.0])
        self.assertEqual(out["bmi_band"].tolist(), [0, 1, 1, 2, 0])      # boundaries: 25 -> 1, 30 -> 2

    def test_input_is_not_modified(self):
        df = make_frame()
        before = df.copy()
        ClinicalFeatureAdder().fit_transform(df)
        pd.testing.assert_frame_equal(df, before)

    def test_missing_column_raises(self):
        with self.assertRaises(ValueError):
            ClinicalFeatureAdder().fit(make_frame().drop(columns="s3"))

    def test_non_dataframe_raises(self):
        with self.assertRaises(TypeError):
            ClinicalFeatureAdder().fit(np.zeros((3, 3)))

    def test_custom_cutoffs_and_clone(self):
        t = ClinicalFeatureAdder(bmi_cutoffs=(20.0, 40.0))
        self.assertEqual(clone(t).get_params()["bmi_cutoffs"], (20.0, 40.0))
        self.assertEqual(t.fit_transform(make_frame())["bmi_band"].tolist(), [1, 1, 1, 1, 0])

    def test_feature_names(self):
        t = ClinicalFeatureAdder().fit(make_frame())
        self.assertEqual(list(t.get_feature_names_out())[-2:], ["ldl_hdl_ratio", "bmi_band"])

    def test_works_inside_a_pipeline(self):
        df = make_frame()
        y = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        pipe = Pipeline([("features", ClinicalFeatureAdder()), ("model", LinearRegression())]).fit(df, y)
        self.assertEqual(pipe.predict(df).shape, (5,))


if __name__ == "__main__":
    unittest.main()
