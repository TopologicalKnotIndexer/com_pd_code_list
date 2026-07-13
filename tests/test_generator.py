import unittest
from unittest.mock import patch

from data import get_pd_code_list as generator


class CompositePdGeneratorTests(unittest.TestCase):
    def tearDown(self):
        generator.get_pd_code_by_prime_knot_name.cache_clear()

    def test_prime_and_mirror_lookup(self):
        pd = [[1, 2, 2, 1]]
        with patch.object(generator, "get_prime_pd_codes", return_value={"K1a1": pd}), patch.object(
            generator, "get_mirror_code", return_value=[[2, 1, 1, 2]]
        ):
            self.assertEqual(generator.get_pd_code_by_prime_knot_name("K1a1"), pd)
            self.assertEqual(
                generator.get_pd_code_by_prime_knot_name("mK1a1"), [[2, 1, 1, 2]]
            )

    def test_composite_uses_connected_sum_in_order(self):
        with patch.object(
            generator, "get_pd_code_by_prime_knot_name", side_effect=lambda name: [name]
        ), patch.object(generator, "get_connected_sum", side_effect=lambda left, right: left + right):
            self.assertEqual(generator.get_pd_code_by_knot_name("A,B,C"), ["A", "B", "C"])

    def test_empty_component_is_rejected(self):
        with self.assertRaises(ValueError):
            generator.get_pd_code_by_knot_name("K3a1,")


if __name__ == "__main__":
    unittest.main()
