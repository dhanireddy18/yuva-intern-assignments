import unittest

import numpy as np

from dstoolkit import benjamini_hochberg, fisher_z_ci, holm_adjust

P = [0.01, 0.04, 0.03, 0.005]          # hand-calculated expectations below


class TestHolm(unittest.TestCase):
    def test_known_values_in_original_order(self):
        # sorted p: .005 .01 .03 .04 -> x4, x3, x2, x1 = .02 .03 .06 .04 -> cumulative max = .02 .03 .06 .06
        np.testing.assert_allclose(holm_adjust(P), [0.03, 0.06, 0.06, 0.02])

    def test_never_smaller_than_raw_and_capped_at_one(self):
        adj = holm_adjust([0.2, 0.5, 0.9])
        self.assertTrue(np.all(adj >= [0.2, 0.5, 0.9]) and np.all(adj <= 1.0))

    def test_invalid_input_raises(self):
        for bad in ([], [1.5], [-0.1]):
            with self.assertRaises(ValueError):
                holm_adjust(bad)


class TestBenjaminiHochberg(unittest.TestCase):
    def test_known_values_in_original_order(self):
        # sorted p: .005 .01 .03 .04 -> x4/1, x4/2, x4/3, x4/4 = .02 .02 .04 .04 (already monotone)
        np.testing.assert_allclose(benjamini_hochberg(P), [0.02, 0.04, 0.04, 0.02])

    def test_less_conservative_than_holm(self):
        p = np.random.default_rng(1).uniform(0, 0.05, 30)
        self.assertTrue(np.all(benjamini_hochberg(p) <= holm_adjust(p) + 1e-12))

    def test_single_p_value_is_unchanged(self):
        np.testing.assert_allclose(benjamini_hochberg([0.03]), [0.03])


class TestFisherZ(unittest.TestCase):
    def test_known_interval(self):
        lo, hi = fisher_z_ci(0.5, 100)
        self.assertAlmostEqual(lo, 0.3366, places=3)
        self.assertAlmostEqual(hi, 0.6341, places=3)

    def test_interval_shrinks_with_sample_size(self):
        small, large = fisher_z_ci(0.4, 30), fisher_z_ci(0.4, 3000)
        self.assertGreater(small[1] - small[0], large[1] - large[0])

    def test_invalid_input_raises(self):
        with self.assertRaises(ValueError):
            fisher_z_ci(1.0, 50)
        with self.assertRaises(ValueError):
            fisher_z_ci(0.5, 3)


if __name__ == "__main__":
    unittest.main()
