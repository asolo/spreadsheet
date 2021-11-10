import csv
from math import trunc


def is_float(n):
    """A method used to determine if an object can be interpreted as a float.

    Args:
        n (object): An object.

    Returns:
        bool: true if the object can be interpreted as a float, otherwise false.
    """

    try:
        float(str(n))
    except ValueError:
        return False
    return True


def is_evaluable(expression):
    """A method used to determine if a string can be evaluated.

    Args:
        expression (string): A string representation of an expression.

    Returns:
        bool: true if the object can be evaluated (e.g. '1+1' = 2.0), otherwise false (e.g. 'A1')
    """

    try:
        eval(expression)
    except (NameError, ValueError, SyntaxError):
        return False
    return True


def get_df_row_col(input_str):
    """A method used to convert a string based alpha-numeric coordinate to a zero indexed row and column.

    Note:
        using ord, integers 65 -> 90 represent capital letters of the alphabet.

    Args:
        input_str (string): A string representation of a row and column location, e.g. 'A1' is column A, row 1.

    Returns:
        int, int: a row and column index.
    """

    # get the alpha and numeric parts of cell reference
    alpha = input_str[0]
    numeric = input_str[1:]

    # convert to 0 based index coordinates
    offset = 65
    col = ord(alpha)-offset
    row = int(numeric)-1
    return row, col


def read_values_from_csv(input_path):
    """A method used to read data from a csv file to an array representation.

    Args:
        input_path (str): the path location of the input file relative to the usage.

    Note:
        encoding = 'utf-8-sig' is used to not read in file with BOM.

    Returns:
        list of list of strings: A representation of the csv where the outer list contains rows and
        each inner list of rows contains raw input cell strings.

    Raises:
        FileNotFoundError: If the input path does not exist.
    """

    with open(input_path, 'r', encoding='utf-8-sig') as file:

        # datafile = open(input_path, 'r', encoding='utf-8-sig')
        data_reader = csv.reader(file, delimiter=',')
        data = []
        for row in data_reader:
            data.append(row)

    return data


def round_standard_two_decimals(input_float):
    """A custom rounding function to bypass python's round to nearest even value behavior.

    Note:
        This method matches the excel spreadsheet rounding function which always
        rounds (n).5 to (n+1).0 regardless of if n is even or odd.

    Args:
        input_float (float): the un-rounded number.

    Returns:
        str: the rounded value as a string to two decimals of accuracy.
    """

    rounding_val = (input_float * 100) % 1

    if rounding_val == 0:
        val = input_float
    elif rounding_val >= 0.5:
        val = trunc(input_float * 100)/100 + 0.01
    else:
        val = trunc(input_float * 100)/100

    # return as string with 2 decimal places
    return '%.2f' % val

