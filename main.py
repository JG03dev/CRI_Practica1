__authors__ = ['1638618, 1636517, LUCIA-NIU']
__group__ = 'GM08:30_3'

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import math

def load_puzzle_crossword(filename):
    with open(filename, 'r') as fileCW:
        # Obtain file content by rows.
        CW = fileCW.readlines()

    # Load text file into a NumPy matrix.
    crossword = []
    for row in CW:
        row = [str(square) for square in row.strip().split('\t')]
        crossword.append(row)
    return np.matrix(crossword)

def load_dictionary(filename):
    pass

def backtracking(LVA, LVNA, R, D):
    pass

def satisfy_restriccions(asignation, LVA, R):
    pass

if __name__ == '__main__':
    LVNA = load_puzzle_crossword("crossword_CB_v3.txt")
    print(LVNA)


