## Word class implementation

import numpy as np
from copy import copy, deepcopy


class Word:
    start = [0,0]
    length = 0
    orientation = 0  # 0 for Horizontal, 1 for Vertical
    linked_words = []  # TODO mirar d'utilitzar numpy per aquesta estructura
    value = ""

    def __init__(self, s=0, l=0, o=0, lw=[]):
        self.start = s
        self.length = l
        self.orientation = o
        self.linked_words = lw
        return

    def pertany(self, casella):
        return ((self.orientation == 0 and self.start[1] <= casella[1] <= self.start[1] + self.length and self.start[0] == casella[0])
                    or (self.orientation == 1 and self.start[0] <= casella[0] <= self.start[0] + self.length and self.start[1] == casella[1]))
    def update_linked(self):
        for w, c in self.linked_words:
            w.linked_words.append([self, c])