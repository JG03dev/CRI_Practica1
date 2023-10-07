__authors__ = ['1638618, 1636517, 1633311']
__group__ = 'GM08:30_3'

import numpy as np
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


            
def mirar_veins(casella, lw):
    for Hw in LVNA:
        if Hw.pertany([casella[0]+1, casella[1]]) or Hw.pertany([casella[0]-1, casella[1]]):
            lw.append([Hw, casella])


def vertical():
    for columna in range(dim[1]):
        lista = []
        lw = []
        for fila in range(dim[0]):
            if board[fila][columna] == '0':
                lista.append('0')
                mirar_veins([fila, columna], lw)
            else:
                if len(lista) > 1:
                    w = Word([fila - len(lista), columna], len(lista), VERTICAL)
                    LVNA.append(copy(w))
                lista.clear()
        if len(lista) > 1:
            w = Word([dim[0] - len(lista), columna], len(lista), VERTICAL, lw)
            w.update_linked()
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
    with open(filename, 'r', encoding='ISO-8859-1') as fileDict:
        for line in fileDict:
            dictionary.append(line.strip())
    return dictionary


def satisfy_restriccions(assignWord, Var):

    if len(assignWord) == Var.length:
        posFila = Var.start[0]
        posCol = Var.start[1]
        direction = Var.orientation

        for w, c in Var.linked_words:  # start[1] - c[1]
            if w.value != "":  # Lo mismo que no assignado
                if direction == HORIZONTAL:
                    if assignWord[posCol - c[1]] != w.value[w.start[1] - c[1]]:
                        return False
                else:
                    if assignWord[posFila - c[0]] != w.value[w.start[0] - c[0]]:
                        return False
        return True

    return False

def backtracking(LVA, LVNA, D):
    if not LVNA: return LVA
    Var = LVNA[0]  # Guardem el cap.
    for assignWord in D:
        if satisfy_restriccions(assignWord, Var):
            LVA.append(Var)
            Res = backtracking(LVA, LVNA[1:], D)
            if Res is not None:
                return Res
    return None


# TODO MODIFICAR UPDATE_BOARD
def update_board():
    for w in LVA:
        if w.orientation == HORIZONTAL:
            for i in range(w.length):
                board[w.start[0] + i][w.start[1]] = w.value[i]
        else:
            for j in range(w.length):
                board[w.start[0]][w.start[1] + j] = w.value[j]
    return board


if __name__ == '__main__':
    # Carga de tablero y diccionario.
    load_puzzle_crossword("crossword_CB_v3.txt")
    load_LVNA()
    dictionary = load_dictionary("diccionari_CB_v3.txt")

    # Function call.
    res = backtracking(LVA, LVNA, dictionary)

    print(update_board())

    if res is not None:
        print(res)
    else:
        print("Incorrect result.")

