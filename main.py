__authors__ = ['1638618, 1636517, 1633311']
__group__ = 'GM08:30_3'

import numpy as np
import math
import string
from word import Word
from copy import copy

# VARIABLES GLOBALES
dim = [0, 0]        # Dimensions del taulell
board = []          # TABLERO
LVA = []            # LLISTA VALORS ASSIGNATS
LVNA = []           # LLISTA VALORS NO ASSIGNATS
HORIZONTAL = 0      # CODIGO PARA PALABRA HORIZONTAL
VERTICAL = 1        # CODIGO PARA PALABRA VERTICAL



def horizontal():
    for fila in range(dim[0]):
        lista = []
        for columna in range(dim[1]):
            if board[fila][columna] == '0':
                lista.append('0')
            else:
                if len(lista) > 1:
                    w = Word([fila, columna - len(lista)], len(lista), HORIZONTAL)
                    LVNA.append(copy(w))
                lista.clear()
        if len(lista) > 1:
            w = Word([fila, dim[1] - len(lista)], len(lista), HORIZONTAL)
            LVNA.append(copy(w))


            


def vertical():
    # TODO: antes de hacer el append en LVNA llenar los crosses
    for columna in range(dim[1]):
        lista = []
        for fila in range(dim[0]):
            if board[fila][columna] == '0':
                lista.append('0')
            else:
                if len(lista) > 1:
                    w = Word([fila - len(lista), columna], len(lista), VERTICAL)
                    LVNA.append(copy(w))
                lista.clear()
        if len(lista) > 1:
            w = Word([dim[0] - len(lista), columna], len(lista), VERTICAL)
            LVNA.append(copy(w))


def load_LVNA():
    horizontal()
    vertical()


def load_puzzle_crossword(filename):
    with open(filename, 'r') as fileCW:
        # Obtain file content by rows.
        CW = fileCW.readlines()
    # Load text file into a NumPy matrix.
    for row in CW:
        row = [str(square) for square in row.strip().split('\t')]
        board.append(row)
        dim[0] = len(board)
        dim[1] = len(board[0])  # Guardamos la dimension


def load_dictionary(filename):
    dictionary = []
    with open(filename, 'r') as fileDict:
        for line in fileDict:
            dictionary.append(line.strip())
    return dictionary


def satisfy_restriccions(assignWord, Var):
    # Coincidan las longitudes
    if len(assignWord) == Var.length:
        # Mirar si coinciden letras
        fila = Var.start[0]
        columna = Var.start[1]
        direccion = Var.orientation
        hueco = []

        for i in range(Var.length):
            if board[fila][columna] == '#':
                return False
            hueco.append(board[fila][columna])
            if direccion == HORIZONTAL:
                columna = columna + 1
            else:
                fila = fila + 1

        for l1, l2 in zip(hueco, assignWord):
            if l1 != l2 and l1 != '0':
                return False

    return True

def backtracking(LVA, LVNA, D):
    if not LVNA: return LVA
    Var = LVNA[0]  # Guardem el cap.
    for assignWord in D:
        if satisfy_restriccions(assignWord, Var):
            update_board(Var, assignWord)
            Res = backtracking(LVA.append(Var), LVNA[1:], D)
            if Res is not None:
                return Res
            else:
                board.clear()
    return None


# TODO MODIFICAR UPDATE_BOARD
def update_board(Var, assignWord):
    fila = Var.start[0]
    columna = Var.start[1]
    for i in range(Var.length):
        board[fila][columna] = assignWord[i]
        if Var.orientation == HORIZONTAL:
            columna += 1
        else:
            fila += 1


if __name__ == '__main__':
    # Carga de tablero y diccionario.
    load_puzzle_crossword("crossword_CB_v3.txt")
    load_LVNA()

    # TODO Arreglar diccionario.
    dictionary = load_dictionary("diccionari_CB_v3.txt")

    # Function call.
    res = backtracking(LVA, LVNA, dictionary)

    if res is not None:
        print(res)
    else:
        print("Incorrect result.")
