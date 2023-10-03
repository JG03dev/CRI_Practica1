## Word class implementation

import numpy as np
from copy import copy, deepcopy


class Word:
    start = [0,0]
    length = 0
    orientation = 0  # 0 for Horizontal, 1 for Vertical
    linked_words = []  # TODO mirar d'utilitzar numpy per aquesta estructura
    value = ''

    def __init__(self):
        return

    def __init__(self, s, l, o):
        self.start = s
        self.length = l
        self.orientation = o

    def crosses(self, w):
        # TODO: finish this implementation
        # Check they have different orientation
        if w.orientation == self.orientation:
            return False
        # Horizontal case
        if (self.orientation == 0
                and self.start[0] <= w.start[0] <= self.start[0] + self.length
                and w.start[1] <= self.start[1] <= w.start[1] + w.length):
            self.linked_words.append(((w.start[0], self.start[1]), w))
            return True
        # Vertical case
        elif self.start[0] <= w.start[0] <= self.start[0] + self.length \
                and w.start[1] <= self.start[1] <= w.start[1] + w.length:
            self.linked_words.append(((w.start[0], self.start[1]), w))
            return True

        return False
