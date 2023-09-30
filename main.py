__authors__ = ['1638618, 1636517, 1633311']
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

def domini(Var, D):
    possible_assignation = []
    if '#' not in Var:
        for word in D:
            if len(word) == len(Var):
                possible_assignation.append(word)

    # QUITAR PALABRAS QUE YA ESTAN EN LVA
    return possible_assignation

def backtracking(LVA, LVNA, R, D):
    if not LVNA:
        return LVA

    Var = LVNA[0]
    possible_assignation = domini(Var, D)

    for valor in D:
        if satisfy_restriccions(valor, LVA, R):
            # Miramos si es fin de palabra
                # Encontramos palabra generada
                # Eliminamos palabra del diccionario
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
    alphabet.append('Ç')

    # Function call.
    res = backtracking(LVA, LVNA, dictionary, alphabet)

    if res is not None:
        print(res)
    else:
        print("Incorrect result.")
