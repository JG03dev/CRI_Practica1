__authors__ = ['1638618, 1636517, LUCIA-NIU']
__group__ = 'GM08:30_3'

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import math
import string

def load_puzzle_crossword(filename):
    with open(filename, 'r') as fileCW:
        # Obtain file content by rows.
        CW = fileCW.readlines()
    # Load text file into a NumPy matrix.
    crossword = []
    for row in CW:
        row = [str(square) for square in row.strip().split('\t')]
        crossword.append(row)
    return crossword

def load_dictionary(filename):
    dictionary = []
    with open(filename, 'r') as fileDict:
        for line in fileDict:
            dictionary.append(line.strip())
    return dictionary

def satisfy_restriccions(assignation, LVA, R):
    pass

def backtracking(LVA, LVNA, R, D):
    if not LVNA:
        return LVA

    Var = LVNA[0]

    for valor in D:
        if satisfy_restriccions(valor, LVA, R):
            # TODO: Make Insertar y Cua


            Res = backtracking()
            if Res is not None:
                return Res

    return None

if __name__ == '__main__':

    # Structures creation.
    LVA = [[]]
    LVNA = load_puzzle_crossword("crossword_CB_v3.txt")

    # Load up files.
    dictionary = load_dictionary("diccionari_CB_v3.txt")
    alphabet = list(string.ascii_uppercase)

    # Function call.
    res = backtracking(LVA, LVNA, dictionary, alphabet)

    if res is not None:
        print(res)
    else:
        print("Incorrect result.")



