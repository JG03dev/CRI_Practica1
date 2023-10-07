__authors__ = ['1638618, 1636517, 1633311']
__group__ = 'GM08:30_3'

import numpy as np
import string
from word import Word
from copy import copy, deepcopy

# VARIABLES GLOBALES
HORIZONTAL = 0      # CODIGO PARA PALABRA HORIZONTAL
VERTICAL = 1        # CODIGO PARA PALABRA VERTICAL


def horizontal(board, dim, LVNA):
    for fila in range(dim[0]):
        lista = []
        for columna in range(dim[1]):
            if board[fila][columna] == '0':
                lista.append('0')
            else:
                if len(lista) > 1:
                    w = Word(s=[fila, columna - len(lista)], l=len(lista), o=HORIZONTAL)
                    LVNA.append(w)
                lista.clear()
        if len(lista) > 1:
            w = Word(s=[fila, dim[1] - len(lista)], l=len(lista), o=HORIZONTAL)
            LVNA.append(w)


def mirar_veins(casella, lw, n_horizontals, LVNA):
    for Hw in LVNA[:n_horizontals]:
        if ((Hw.pertany([casella[0], casella[1]+1]) or Hw.pertany([casella[0], casella[1]-1]))
                and Hw not in lw):
            lw.append([Hw, casella])


def vertical(board, dim, LVNA):
    n_horizontals = len(LVNA)
    for columna in range(dim[1]):
        lista = []
        lw = []
        for fila in range(dim[0]):
            if board[fila][columna] == '0':
                lista.append('0')
                mirar_veins([fila, columna], lw, n_horizontals, LVNA)
            else:
                if len(lista) > 1:
                    w = Word(s=[fila - len(lista), columna], l=len(lista), o=VERTICAL, lw=lw)
                    w.update_linked()
                    LVNA.append(w)
                lista.clear()
                lw.clear()
        if len(lista) > 1:
            w = Word(s=[dim[0] - len(lista), columna], l=len(lista), o=VERTICAL, lw=lw)
            w.update_linked()
            LVNA.append(w)


def load_LVNA(board, dim ,LVNA):
    horizontal(board, dim, LVNA)
    vertical(board, dim, LVNA)


def load_puzzle_crossword(filename, board, dim):
    with open(filename, 'r') as fileCW:
        # Obtain file content by rows.
        CW = fileCW.readlines()
    # Load text file into a NumPy matrix.
    for row in CW:
        row = [str(square) for square in row.strip().split('\t')]
        board.append(row)
        dim[0] = len(board)
        dim[1] = len(board[0])  # Guardamos la dimension


#TODO: Ordenar por longitud
def load_dictionary(filename):
    dictionary = []
    with open(filename, 'r', encoding='ISO-8859-1') as fileDict:
        for line in fileDict:
            dictionary.append(line.strip())
    return dictionary


def satisfy_restriccions(assignWord, Var):
    if len(assignWord) != Var.length:
        return False

    posFila = Var.start[0]
    posCol = Var.start[1]
    direction = Var.orientation
    for w, c in Var.linked_words:  # start[1] - c[1]
        if w.value != "":  # Lo mismo que no assignado
            if direction == HORIZONTAL:
                if assignWord[c[1] - posCol] != w.value[c[0] - w.start[0]]:
                    return False
            else:  # Vertical
                if assignWord[c[0] - posFila] != w.value[c[1] - w.start[1]]:
                    return False
    return True


def backtracking(LVA, LVNA, D):
    if not LVNA:
        return LVA

    Var = LVNA[0]  # Guardem el cap.

    for assignWord in D:
        if satisfy_restriccions(assignWord, Var):
            Var.value = assignWord
            Res = backtracking(LVA + [Var], LVNA[1:], D)
            if Res is not None:
                return Res

    # Si arribem aqui el valor de LVA deixa de tenir una assignació
    if LVA:
        LVA[-1].value = ""
    return None


def update_board(board, res):
    for w in res:
        if w.orientation == HORIZONTAL:
            for i in range(w.length):
                board[w.start[0]][w.start[1] + i] = w.value[i]
        else:
            for j in range(w.length):
                board[w.start[0] + j][w.start[1]] = w.value[j]
    return board


if __name__ == '__main__':
    dim = [0, 0]  # Dimensions del taulell
    board = []  # TABLERO
    LVA = []  # LLISTA VALORS ASSIGNATS
    LVNA = []  # LLISTA VALORS NO ASSIGNATS


    # Carga de tablero y diccionario
    load_puzzle_crossword("crossword_CB_v3.txt", board, dim)
    load_LVNA(board, dim, LVNA)
    dictionary = load_dictionary("diccionari_CB_v3.txt")

    # Function call.
    res = backtracking(LVA, LVNA, dictionary)

    if res is not None:
        update_board(board, res)
        for i in board:
            print(*i)
        print([w.value for w in res])
    else:
        print("Incorrect result.")
