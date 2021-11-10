from src.cell import Cell
from src.utils import *
import csv


class Sheet:
    """A class used to represent a spreadsheet.

    Attributes
        data (list of list of obj): represents the 2-dimensional array containing raw data or cell objects.
        rows (int): the count of rows of the sheet.
        cols (int): the count of columns in the sheet.
    """

    def __init__(self, data):
        self.data = data
        self.rows = len(self.data)
        self.cols = len(self.data[0]) if len(self.data) > 0 else 0
        self.convert_to_cells()

    def convert_to_cells(self):
        """A method used to convert raw input at each location and replace it with a Cell class object."""

        for row in range(self.rows):
            for col in range(self.cols):
                new_cell = Cell(self.data[row][col])
                self.data[row][col] = new_cell

    def evaluate_cell(self, row, col, visited):
        """A method used to attempt to evaluate the formula within a cell

        This method recursively calculates each reference within a formula, and returns the cell value.

        Args:
            row (int): The row of the cell.
            col (int): The column of the cell.
            visited (dict): A dictionary used to track which cell references have been used in evaluation.
                Note this is only passed as non-empty in recursive calls.

        Returns:
            float: the value of the cell once evaluated

        Raises:
            BaseException: If a formula evaluation results in a circular reference.
        """

        cell = self.data[row][col]

        if cell.value is not None:
            return cell.value
        else:
            value = 0

        if cell.string in visited:
            raise BaseException("Circular reference detected at row: " + str(row) + ", column: " + str(col))
        else:
            visited.update({cell.string: 1})

        # sum the positive elements
        for element in cell.pos_elements:
            if is_float(element):
                value += float(element)
            else:
                r, c = get_df_row_col(element)
                value += self.evaluate_cell(r, c, visited)

        # sum the negative elements
        for element in cell.neg_elements:
            if is_float(element):
                value -= float(element)
            else:
                r, c = get_df_row_col(element)
                value -= self.evaluate_cell(r, c, visited)

        return value

    def evaluate_all_cells(self):
        """A method used to evaluate all cells in a sheet and assign cell values in place."""

        for row in range(self.rows):
            for col in range(self.cols):
                self.data[row][col].value = self.evaluate_cell(row, col, visited={})

    def write_values_to_csv(self, output_path):
        """A method used to write the values of a sheet to a csv file

        Args:
            output_path (str): the path location of the output file relative to the Sheet class.

        Returns:
            csv: a csv file containing float values of the evaluated spreadsheet.

        Raises:
            FileNotFoundError: If the destination directory of the output file does not exist.
        """

        with open(output_path, 'w') as file:
            writer = csv.writer(file, delimiter=',', lineterminator='\n')

            for r in range(self.rows):
                row = []

                for c in range(self.cols):

                    # round each value to 2 decimal precision
                    rounded_value = round_standard_two_decimals(self.data[r][c].value)

                    # build each column in the row
                    row.append(rounded_value)

                writer.writerow(row)









