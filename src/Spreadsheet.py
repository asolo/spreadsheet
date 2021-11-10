import os
import sys
sys.path.append(os.path.join(os.path.abspath(os.path.curdir), '../'))
from src.utils import read_values_from_csv
from src.sheet import Sheet


class Spreadsheet:
    """A module that reads in a csv, evaluates it, and returns two decimal precision results.

    Example:
        This module can be executed as follows:

            $ python3 Spreadsheet.py
    """

    @staticmethod
    def main():

        # import data as a list of lists
        data_list = read_values_from_csv("../data/input.csv")

        # convert the data to a sheet object
        sheet = Sheet(data_list)

        # attempt to evaluate the sheet, exit if circular reference found
        try:
            sheet.evaluate_all_cells()
        except BaseException as e:
            print("\nError with data sheet: " + e.__str__())
            exit()

        # write back to a csv
        sheet.write_values_to_csv("../data/output.csv")

        # log we were successful
        print("\noutput.csv successfully created")


if __name__ == "__main__":
    runner = Spreadsheet()
    runner.main()
