## Word class implementation

import numpy as np


class Word:
    start = (0,0)
    length = 0
    orientation = 0 # 0 for Horizontal, 1 for Vertical
    linked_words = []  # TODO mirar d'utilitzar numpy per aquesta estructura
    def __init__(self, s, l, o):
        self.start = s
        self.length = l
        self.orientation = o

    def crosses(self, w):
        # TODO: finish this implementation
        if w.orientation is self.orientation:
            return False
        if self.orientation is 0: # Check for horizontal
            return
        else: # Check for vertical
            return
