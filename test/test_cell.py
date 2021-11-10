import unittest
import sys
import os
sys.path.append(os.path.join(os.path.abspath(os.path.curdir), '../'))
from src.cell import Cell


class TestCell(unittest.TestCase):

    def test_init(self):
        mock_input = "A2+2"
        test_cell = Cell(mock_input)
        self.assertEqual(test_cell.string, mock_input)

    def test_get_elements_pos(self):
        mock_input = "A2+2"
        test_cell = Cell(mock_input)
        self.assertEqual(test_cell.pos_elements, ["A2", "2"])
        self.assertEqual(test_cell.neg_elements, [])

    def test_get_elements_neg(self):
        mock_input = "-A2-2"
        test_cell = Cell(mock_input)
        self.assertEqual(test_cell.neg_elements, ["A2", "2"])
        self.assertEqual(test_cell.pos_elements, [])

    def test_get_elements_mixed(self):
        mock_input = "-A2-2+B5+B6-A5-D20-17"
        test_cell = Cell(mock_input)
        self.assertEqual(test_cell.neg_elements, ["A2", "2", "A5", "D20", "17"])
        self.assertEqual(test_cell.pos_elements, ["B5", "B6"])


if __name__ == '__main__':
    unittest.main()
