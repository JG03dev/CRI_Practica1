__authors__ = ['1638618, 1636517, 1633311']
__group__ = 'GM08:30_3'

import numpy as np
import string
from word import Word
from copy import copy, deepcopy
import time
import unittest

# VARIABLES GLOBALES
HORIZONTAL = 0  # CODIGO PARA PALABRA HORIZONTAL
VERTICAL = 1  # CODIGO PARA PALABRA VERTICAL


def horizontal(board, dim, LVNA):
    """
        Esta funcion busca las posiciones en las que se puede insertar una palabra de forma horizontal.

        Parametros:
            board (list): Una lista de listas que representa el tablero de juego.
            dim (tuple): Un par ordenado que representa las dimensiones del tablero.
            LVNA (list): Una lista que almacena las palabras no asignadas en el tablero.

        Return:
            None
    """
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


def mirar_veins(casilla, lw, n_horizontals, LVNA):
    """
        Esta funcion, dada una casilla especifica, examina las casillas adyacentes a los lados para identificar palabras que se
        crucen con la palabra formada por la casilla dada.

        Parametros:
            casilla (list): Una lista de listas que representa el tablero de juego.
            lw (list word): Una lista de objetos word.
            n_horizontals (int): Un numero entero que delimita el numero de objetos word queremos analizar.
            LVNA (list): Una lista que almacena las palabras no asignadas en el tablero.

        Return:
            None
    """
    for Hw in LVNA[:n_horizontals]:
        if ((Hw.pertany([casilla[0], casilla[1] + 1]) or Hw.pertany([casilla[0], casilla[1] - 1])) and Hw not in lw):
            lw.append([Hw, casilla])


def vertical(board, dim, LVNA):
    """
        Esta funcion busca las posiciones en las que se puede insertar una palabra de forma vertical.

        Parametros:
            board (list): Una lista de listas que representa el tablero de juego.
            dim (tuple): Un par ordenado que representa las dimensiones del tablero.
            LVNA (list): Una lista que almacena las palabras no asignadas en el tablero.

        Return:
            None
    """
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


def load_LVNA(board, dim, LVNA):
    """
        Esta función hace un llamamiento de las funciones horizontal y vertical.

        Parametros:
            board (list): Una lista de listas que representa el tablero de juego.
            dim (tuple): Un par ordenado que representa las dimensiones del tablero.
            LVNA (list): Una lista que almacena las palabras no asignadas en el tablero.

        Return:
            None
    """
    horizontal(board, dim, LVNA)
    vertical(board, dim, LVNA)


def load_puzzle_crossword(filename, board, dim):
    """
        Esta funcion se encarga de cargar el tablero en la variable board.

        Parametros:
            filename (file txt): Fichero que contiene el tablero en formato .txt.
            board (list): Una lista de listas que representa el tablero de juego.
            dim (tuple): Un par ordenado que representa las dimensiones del tablero.

        Return:
            None
    """
    with open(filename, 'r') as fileCW:
        # Obtain file content by rows.
        CW = fileCW.readlines()

    # Load text file into a NumPy matrix.
    for row in CW:
        row = [str(square) for square in row.strip().split('\t')]
        board.append(row)
        dim[0] = len(board)
        dim[1] = len(board[0])  # Guardamos la dimensiones


def load_dictionary(filename):
    """
        Esta funcion se encarga de cargar el diccionario.

        Parametros:
            filename (file txt): Fichero que contiene el diccionario en formato .txt.

        Return:
            word_dict (list): Contiene un listado del diccionario.
    """
    word_dict = {}
    with open(filename, 'r', encoding='ISO-8859-1') as fileDict:
        for line in fileDict:
            word = line.strip()
            length = len(word)
            if length not in word_dict:
                word_dict[length] = []
            word_dict[length].append(word)
    return word_dict


def satisfy_restriccions(assignWord, Var):
    """
        Esta funcion se comprobar las condiciones necesarias para poder insertar una palabra en el tablero.

        Parametros:
            assingWord (string): Posible palabra que pueda ser insertada en el tablero.
            Var (object word): Objeto de tipo word donde almacena las propiedades de las palabras.

        Return:
            True/False (bool): Si la palabra cumple las condiciones se duelve True de lo contrario se devuelve False.
    """

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


def update_domain(Var, assignWord, LVNA, DA, LVA):
    DA_aux = {k: list(v) for k, v in DA.items()}

    DA_aux[Var] = [assignWord]

    for lw, c in Var.linked_words:
        if lw in LVA:
            continue
        # Actualizar dominio de linked words.
        words_to_remove = []
        for word_D in DA_aux[lw]:
            if Var.orientation == HORIZONTAL:
                if assignWord[c[1] - Var.start[1]] != word_D[c[0] - lw.start[0]]:
                    words_to_remove.append(word_D)
            else:  # Vertical
                if assignWord[c[0] - Var.start[0]] != word_D[c[1] - lw.start[1]]:
                    words_to_remove.append(word_D)
        for word in words_to_remove:
            DA_aux[lw].remove(word)
        if not DA_aux[lw]:  # Si está vacio devolvemos false.
            return False

    return DA_aux

def backtracking(LVA, LVNA, D):
    """
        Esta funcion implementa backtracking sobre el conjunto LVNA de forma que obtenemos como resultado LVA.

        Parametros:
            LVA (list): Una lista que almacena las palabras asignadas en el tablero.
            LVNA (list): Una lista que almacena las palabras no asignadas en el tablero.
            D (string list): Lista que contiene el diccionario de palabras.

        Return:
            Res (list of object word): Devuelve LVA con la solucion definitiva
    """

    if not LVNA:
        return LVA

    Var = LVNA[0]  # Guardem el cap.
    for assignWord in D[Var.length]:
        if satisfy_restriccions(assignWord, Var):
            Var.value = assignWord
            Res = backtracking(LVA + [Var], LVNA[1:], D)
            if Res is not None:
                return Res

    # Si arribem aqui el valor de LVA deixa de tenir una assignació
    if LVA:
        LVA[-1].value = ""
    return None

def backtrackingCountNodes(LVA, LVNA, D, count):
    """
        Esta funcion implementa backtracking sobre el conjunto LVNA de forma que obtenemos como resultado LVA.

        Parametros:
            LVA (list): Una lista que almacena las palabras asignadas en el tablero.
            LVNA (list): Una lista que almacena las palabras no asignadas en el tablero.
            D (string list): Lista que contiene el diccionario de palabras.

        Return:
            Res (list of object word): Devuelve LVA con la solucion definitiva
    """
    # TODO: fix count update
    count += 1
    if not LVNA:
        return LVA

    Var = LVNA[0]  # Guardem el cap.
    for assignWord in D[Var.length]:
        if satisfy_restriccions(assignWord, Var):
            Var.value = assignWord
            Res = backtrackingCountNodes(LVA + [Var], LVNA[1:], D, count)
            if Res is not None:
                return Res

    # Si arribem aqui el valor de LVA deixa de tenir una assignació
    if LVA:
        LVA[-1].value = ""
    return None

def backForwardChecking(LVA, LVNA, DA):
    # TODO Cambiar descripcion
    """
        Esta funcion implementa backtracking sobre el conjunto LVNA de forma que obtenemos como resultado LVA.

        Parametros:
            LVA (list): Una lista que almacena las palabras asignadas en el tablero.
            LVNA (list): Una lista que almacena las palabras no asignadas en el tablero.
            D (string list): Lista que contiene el diccionario de palabras.

        Return:
            Res (list of object word): Devuelve LVA con la solucion definitiva
    """
    if not LVNA:
        return LVA

    Var = LVNA[0]  # Guardem el cap.

    for assignWord in DA[Var]:
        if satisfy_restriccions(assignWord, Var):
            # Update domain
            DA2 = update_domain(Var, assignWord, LVNA, DA, LVA)
            if DA2 is False:
                continue
            Var.value = assignWord
            Res = backForwardChecking(LVA + [Var], LVNA[1:], DA2)
            if Res is not None:
                return Res

    # Si arribem aqui el valor de LVA deixa de tenir una assignació
    if LVA:
        LVA[-1].value = ""
    return None

def backForwardCheckingCountNodes(LVA, LVNA, DA, count):
    # TODO Cambiar descripcion
    """
        Esta funcion implementa backtracking sobre el conjunto LVNA de forma que obtenemos como resultado LVA.

        Parametros:
            LVA (list): Una lista que almacena las palabras asignadas en el tablero.
            LVNA (list): Una lista que almacena las palabras no asignadas en el tablero.
            D (string list): Lista que contiene el diccionario de palabras.

        Return:
            Res (list of object word): Devuelve LVA con la solucion definitiva
    """
    # TODO: fix count update
    count += 1
    if not LVNA:
        return LVA

    Var = LVNA[0]  # Guardem el cap.

    for assignWord in DA[Var]:
        if satisfy_restriccions(assignWord, Var):
            # Update domain
            DA2 = update_domain(Var, assignWord, LVNA, DA, LVA)
            if DA2 is False:
                continue
            Var.value = assignWord
            Res = backForwardCheckingCountNodes(LVA + [Var], LVNA[1:], DA2, count)
            if Res is not None:
                return Res

    # Si arribem aqui el valor de LVA deixa de tenir una assignació
    if LVA:
        LVA[-1].value = ""
    return None


def print_board(board, res):
    """
        Esta funcion imprime la solución final en el tablero.

        Parametros:
            board (list): Una lista de listas que representa el tablero de juego.
            res (list of object word): LVA con la solucion definitiva.

        Return:
            board (list): Devuelve el tablero actualizado.
    """
    if res is None:
        print("Incorrect result.")
        return
    # Update board based on res
    for w in res:
        if w.orientation == HORIZONTAL:
            for i in range(w.length):
                board[w.start[0]][w.start[1] + i] = w.value[i]
        else:
            for j in range(w.length):
                board[w.start[0] + j][w.start[1]] = w.value[j]
    # Print board
    for i in board:
        print(*i)
    print([w.value for w in res])

    return



def inicializarDA(LVNA, dictionary):
    # TODO HACER DESCRIPCION
    DA = {}
    for obj_palabra in LVNA:
        DA[obj_palabra] = []
        for palabra in dictionary[obj_palabra.length]:
            DA[obj_palabra].append(palabra)
    return DA


class TestCrosswordSolver(unittest.TestCase):
    def setUp(self):

        # Tauler 1

        dim = [0, 0]  # Dimensions del taulell

        ## Test case backtracking

        self.board = []  # TABLERO
        self.LVNA = []  # LLISTA VALORS NO ASSIGNATS
        self.LVA = []   # LLISTA VALORS ASSIGNATS

        # Carga de tablero y diccionario
        load_puzzle_crossword("crossword_CB_v3.txt", self.board, dim)
        load_LVNA(self.board, dim, self.LVNA)
        self.dictionary = load_dictionary("diccionari_CB_v3.txt")

        ##########################################

        ## Test case fordwardchecking
        self.boardFC = []
        self.LVNAFC = []
        self.LVAFC = []

        # Carga de tablero y diccionario
        load_puzzle_crossword("crossword_CB_v3.txt", self.boardFC, dim)
        load_LVNA(self.boardFC, dim, self.LVNAFC)
        self.DA = inicializarDA(self.LVNAFC, self.dictionary)

        ##########################################

        ## Test case backtracking contant nodes recorreguts
        self.boardN = []
        self.LVNAN = []
        self.LVAN = []

        # Carga de tablero y diccionario
        load_puzzle_crossword("crossword_CB_v3.txt", self.boardN, dim)
        load_LVNA(self.boardN, dim, self.LVNAN)

        ########################################


        ## Test case fordwardchecking contant nodes recorreguts
        self.boardFCN = []
        self.LVNAFCN = []
        self.LVAFCN = []

        # Carga de tablero y diccionario
        load_puzzle_crossword("crossword_CB_v3.txt", self.boardFCN, dim)
        load_LVNA(self.boardFCN, dim, self.LVNAFCN)
        self.DAN = inicializarDA(self.LVNAFCN, self.dictionary)

        # Tauler 2
        dim2 = [0, 0]  # Dimensions del taulell

        ## Test case dificultat A

        self.boardA = []
        self.LVNAA = []
        self.LVAA = []

        # Carga de tablero y diccionario
        load_puzzle_crossword("crossword_A.txt", self.boardA, dim2)
        load_LVNA(self.boardA, dim2, self.LVNAA)
        self.dictionaryA = load_dictionary("diccionari_A.txt")
        self.DA_dictA = inicializarDA(self.LVNAA, self.dictionaryA)

    def test_backtracking_sense_nodes(self):
        result1 = backtracking([], self.LVNA, self.dictionary)
        print_board(self.board, result1)
        self.assertIsNotNone(result1)

    def test_backForwardChecking_sense_nodes(self):
        result2 = backForwardChecking([], self.LVNAFC, self.DA)
        print_board(self.board, result2)
        self.assertIsNotNone(result2)

    def test_backtracking_amb_nodes(self):
        count = 0
        result3 = backtrackingCountNodes([], self.LVNAN, self.dictionary, count)
        print(f"Total de nodes recorreguts en el backtracking es {count}")
        print_board(self.board, result3)
        self.assertIsNotNone(result3)

    def test_backForwardChecking_amb_nodes(self):
        count = 0
        result4 = backForwardCheckingCountNodes([], self.LVNAFCN, self.DAN, count)
        print(f"Total de nodes recorreguts en el Fordward Checking es {count}")
        print_board(self.board, result4)
        self.assertIsNotNone(result4)

    def test_diff_A(self): # De moment no implementarem aquest
        return
        result5 = backForwardChecking([], self.LVNAA, self.DA_dictA)
        print_board(self.board, result5)
        self.assertIsNotNone(result5)

if __name__ == '__main__':
    unittest.main()






