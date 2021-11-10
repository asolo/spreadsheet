import re
from src.utils import *


class Cell:
    """A class used to represent a spreadsheet cell.

    Attributes
        string (str): the string representation of a value or a formula, e.g. 'A1+1' or '1'.
        value (float): the value of the cell, once it is evaluated.
        pos_elements(list of str): the elements in the formula that should be summed.
        neg_elements(list of str): the elements in the formula that should be subtracted.
    """

    def __init__(self, input_str):
        self.string = str(input_str)
        self.value = None
        self.pos_elements = []
        self.neg_elements = []
        self.visited = {}
        self.get_elements()

    def get_elements(self):
        """A method used to parse the input string and persist attributes of the cell.

        This method also checks if the input string can be directly evaluated to a value,
        and assigns the value if so.
        """

        if is_evaluable(self.string):
            self.value = float(eval(self.string))
            return

        # use regex to split on + and - signs
        split = re.split("([+-])", self.string.replace(" ", ""))

        # in the case of a leading neg sign, remove empty string at start
        if split[0] == "":
            split.pop(0)

        position = 0
        length = len(split)

        # assign each of the parsed elements based on the sign that precedes it
        while position < length:
            if split[position] == "+":
                self.pos_elements.append(split[position+1])
                position += 2
            elif split[position] == "-":
                self.neg_elements.append(split[position+1])
                position += 2
            else:
                # case where first element in the list is positive (i.e. no preceding sign)
                self.pos_elements.append(split[position])
                position += 1






