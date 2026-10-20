import unittest

import numpy as np

from dstoolkit import bootstrap_ci, regression_report


class TestRegressionReport(unittest.TestCase):
    def test_perfect_prediction(self):
        r = regression_report([1, 2, 3, 4], [1, 2, 3, 4])
        self.assertAlmostEqual(r["rmse"], 0.0)
        self.assertAlmostEqual(r["mae"], 0.0)
        self.assertAlmostEqual(r["r2"], 1.0)

    def test_known_values(self):
        # errors are 0, 0, -1  ->  MSE = 1/3, MAE = 1/3, SS_res = 1, SS_tot = 2
        r = regression_report([1, 2, 3], [1, 2, 4])
        self.assertAlmostEqual(r["rmse"], (1 / 3) ** 0.5)
        self.assertAlmostEqual(r["mae"], 1 / 3)
        self.assertAlmostEqual(r["r2"], 0.5)

    def test_mean_predictor_has_zero_r2(self):
        y = np.array([2.0, 4.0, 6.0, 8.0])
        self.assertAlmostEqual(regression_report(y, np.full(4, y.mean()))["r2"], 0.0)

    def test_shape_mismatch_and_empty_raise(self):
        with self.assertRaises(ValueError):
            regression_report([1, 2], [1, 2, 3])
        with self.assertRaises(ValueError):
            regression_report([], [])


class TestBootstrapCI(unittest.TestCase):
    def setUp(self):
        self.x = np.random.default_rng(0).normal(10, 2, 200)

    def test_reproducible_with_seed(self):
        self.assertEqual(bootstrap_ci(self.x, seed=1), bootstrap_ci(self.x, seed=1))

    def test_interval_contains_sample_mean_and_is_ordered(self):
        low, high = bootstrap_ci(self.x)
        self.assertLess(low, high)
        self.assertLessEqual(low, self.x.mean())
        self.assertGreaterEqual(high, self.x.mean())

    def test_wider_confidence_gives_wider_interval(self):
        l90, h90 = bootstrap_ci(self.x, ci=0.90)
        l99, h99 = bootstrap_ci(self.x, ci=0.99)
        self.assertGreater(h99 - l99, h90 - l90)

    def test_invalid_input_raises(self):
        with self.assertRaises(ValueError):
            bootstrap_ci([1.0])
        with self.assertRaises(ValueError):
            bootstrap_ci(self.x, ci=1.5)


if __name__ == "__main__":
    unittest.main()
