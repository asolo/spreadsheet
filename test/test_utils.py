import unittest
from src import utils


class TestUtils(unittest.TestCase):

    def test_is_int(self):
        self.assertTrue(utils.is_float("1.01"))
        self.assertTrue(utils.is_float("101"))
        self.assertFalse(utils.is_float("A"))
        self.assertFalse(utils.is_float("A2"))
        self.assertTrue(utils.is_float('1'))

    def test_get_df_row_col(self):
        self.assertTrue(utils.get_df_row_col("A1"), (0, 0))
        self.assertTrue(utils.get_df_row_col("Z26"), (25, 25))
        self.assertTrue(utils.get_df_row_col("B26"), (25, 1))

    def test_is_evaluable(self):
        self.assertTrue(utils.is_evaluable("1.4+2"))
        self.assertFalse(utils.is_evaluable("A1+2"))
        self.assertTrue(utils.is_evaluable("-1-2"))
        self.assertFalse(utils.is_evaluable("A1-2"))
        self.assertFalse(utils.is_evaluable("A1-E10"))

    def test_round_standard_two_decimals(self):
        self.assertEqual(utils.round_standard_two_decimals(0), '0.00')
        self.assertEqual(utils.round_standard_two_decimals(1000.005), '1000.01')
        self.assertEqual(utils.round_standard_two_decimals(3.53893), '3.54')
        self.assertEqual(utils.round_standard_two_decimals(3.545), '3.55')
        self.assertEqual(utils.round_standard_two_decimals(3.544), '3.54')
        self.assertEqual(utils.round_standard_two_decimals(3.5445), '3.54')
        self.assertEqual(utils.round_standard_two_decimals(3.5449999999999), '3.54')


if __name__ == '__main__':
    unittest.main()
