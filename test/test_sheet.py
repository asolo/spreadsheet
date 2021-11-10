import unittest
import sys
import os
sys.path.append(os.path.join(os.path.abspath(os.path.curdir), '../'))
from src.sheet import Sheet
from src.cell import Cell
from src.utils import *


class TestSheet(unittest.TestCase):

    def test_init(self):
        mock_input = [["1", "2"], ["3", "4"]]
        test_sheet = Sheet(mock_input)

        self.assertEqual(test_sheet.cols, 2)
        self.assertEqual(test_sheet.rows, 2)
        self.assertEqual(test_sheet.data[0][0].value, 1)

    def test_init_and_convert_to_cells(self):
        mock_input = [["1", "B2"], ["3", "A1"]]
        test_sheet = Sheet(mock_input)

        expected_cell = Cell("1")

        self.assertEqual(test_sheet.data[0][0].string, expected_cell.string)
        self.assertEqual(test_sheet.data[0][0].pos_elements, expected_cell.pos_elements)
        self.assertEqual(test_sheet.data[0][0].neg_elements, expected_cell.neg_elements)
        self.assertEqual(test_sheet.data[0][0].value, 1)

    def test_evaluate_cell_when_no_circular_and_no_math(self):
        mock_input = [["1.5", "B2"], ["3", "A1"]]
        test_sheet = Sheet(mock_input)
        self.assertEqual(test_sheet.evaluate_cell(0, 0, {}), 1.5)
        self.assertEqual(test_sheet.evaluate_cell(1, 1, {}), 1.5)
        self.assertEqual(test_sheet.evaluate_cell(0, 1, {}), 1.5)
        self.assertEqual(test_sheet.evaluate_cell(1, 0, {}), 3)

    def test_evaluate_cell_when_no_circular_and_evaluable_input(self):
        mock_input = [["1+2", "B2"], ["5", "A1"]]
        test_sheet = Sheet(mock_input)
        self.assertEqual(test_sheet.evaluate_cell(0, 0, {}), 3)
        self.assertEqual(test_sheet.evaluate_cell(1, 1, {}), 3)
        self.assertEqual(test_sheet.evaluate_cell(0, 1, {}), 3)
        self.assertEqual(test_sheet.evaluate_cell(1, 0, {}), 5)

    def test_evaluate_cell_when_no_circular_and_non_evaulable_input(self):
        mock_input = [["1+2", "B2-1"], ["5", "A1"]]
        test_sheet = Sheet(mock_input)
        self.assertEqual(test_sheet.evaluate_cell(0, 0, {}), 3)
        self.assertEqual(test_sheet.evaluate_cell(1, 1, {}), 3)
        self.assertEqual(test_sheet.evaluate_cell(0, 1, {}), 2)
        self.assertEqual(test_sheet.evaluate_cell(1, 0, {}), 5)

    def test_evaluate_cell_when_no_circular_and_three_leg_calculation(self):
        mock_input = [["1", "A1"], ["B1+1", "A2+1"]]
        test_sheet = Sheet(mock_input)
        self.assertEqual(test_sheet.evaluate_cell(0, 0, {}), 1)
        self.assertEqual(test_sheet.evaluate_cell(1, 1, {}), 3)
        self.assertEqual(test_sheet.evaluate_cell(0, 1, {}), 1)
        self.assertEqual(test_sheet.evaluate_cell(1, 0, {}), 2)

    def test_evaluate_cell_when_no_circular(self):
        mock_input = [["B2+2", "A1+A2"], ["B2-3", "7+5"]]
        test_sheet = Sheet(mock_input)
        self.assertEqual(test_sheet.evaluate_cell(0, 0, {}), 14)
        self.assertEqual(test_sheet.evaluate_cell(1, 1, {}), 12)
        self.assertEqual(test_sheet.evaluate_cell(1, 0, {}), 9)
        self.assertEqual(test_sheet.evaluate_cell(0, 1, {}), 23)

    def test_evaluate_cell_when_circular_calls_itself_then_throws(self):
        mock_input = [["A1", "2+A1"]]
        test_sheet = Sheet(mock_input)
        self.assertRaises(BaseException, test_sheet.evaluate_cell, 0, 0, {})

    def test_evaluate_cell_when_circular_calls_neighbors_then_throws(self):
        mock_input = [["B1", "A1"]]
        test_sheet = Sheet(mock_input)
        self.assertRaises(BaseException, test_sheet.evaluate_cell, 0, 0, {})

    def test_evaluate_all_cells(self):
        mock_input = [["B2+2", "A1+A2"], ["B2-3", "7+5"]]
        test_sheet = Sheet(mock_input)
        test_sheet.evaluate_all_cells()
        self.assertEqual(test_sheet.data[0][0].value,  14)
        self.assertEqual(test_sheet.data[1][1].value,  12)
        self.assertEqual(test_sheet.data[0][1].value,  23)
        self.assertEqual(test_sheet.data[1][0].value,  9)

    def test_evaluate_all_cells_with_csv_input(self):
        mock_input = read_values_from_csv("mock_data/mock_input.csv")
        mock_output = read_values_from_csv("mock_data/mock_output.csv")

        test_sheet = Sheet(mock_input)
        test_sheet.evaluate_all_cells()

        self.assertResultsEqual(test_sheet, mock_output)

    def test_evaluate_all_cells_with_csv_input_blank(self):
        mock_input = read_values_from_csv("mock_data/mock_input_blank.csv")

        test_sheet = Sheet(mock_input)
        test_sheet.evaluate_all_cells()

        # no values to compare, validate a blank sheet is created
        output_path = "mock_data/mock_output_blank.csv"
        test_sheet.write_values_to_csv(output_path)
        output_data = read_values_from_csv(output_path)
        output_sheet = Sheet(output_data)
        self.assertEqual(output_sheet.rows, 0)
        self.assertEqual(output_sheet.cols, 0)

        # clean up the test
        os.remove(output_path)

    def assertResultsEqual(self, test_sheet, mock_output):
        rows, cols = test_sheet.rows, test_sheet.cols
        for r in range(rows):
            for c in range(cols):
                self.assertEqual(round_standard_two_decimals(test_sheet.data[r][c].value), mock_output[r][c])


if __name__ == '__main__':
    unittest.main()
