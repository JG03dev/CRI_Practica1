__authors__ = ['1638618, 1636517, 1633311']
__group__ = 'GM08:30_3'

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import math
import string

D = [
    "ACATAR",
    "AFERRISSAU",
    "AGUISSAVEU",
    "ALLOFONIES",
    "ALTA",
    "AMORTASSEN",
    "ANYOCASSIN",
    "APROFITASSEU",
    "ARRENGARA",
    "ASSOCIESSEM",
    "AUTENTIFICARIES",
    "BANALMENT",
    "BESCOLLEJAREN",
    "BORE",
    "BUFALAGA",
    "CARA",
    "CARNET",
    "CENTRACIONS",
    "CLAN",
    "COMPAGIN",
    "CONFORTESSIU",
    "CONTRAGIRAU",
    "COR",
    "CUPULAR",
    "DEJUNES",
    "DESAGERMANESSIN",
    "DESBOQUESSIM",
    "DESCOVAREM",
    "DESEMPASTASSIN",
    "DESENFETGEGAVA",
    "DESENVALISESSIN",
    "DESINFLAMEU",
    "DESPARAVA",
    "DESUNGLAS",
    "DIARI",
    "DIEM",
    "DO",
    "DORAT",
    "ELUIA",
    "EMBOVAVEU",
    "EMPANTANEGARA",
    "EMPRESONAU",
    "ENCASTESSIS",
    "ENDANYESSIS",
    "ENFREIXURARIA",
    "ENGUERXINASSEN",
    "ENRINXAVEU",
    "ENTERANYINESSIN",
    "ENUCLEESSEN",
    "ESBALAIXEN",
    "ESCAMOTEJARIEM",
    "ESCORNIFLAREM",
    "ESGRUMESSEU",
    "ESPENYADA",
    "ESQUERRARAS",
    "ESTRANGERITZANT",
    "EXCULPAREN",
    "FALDILLER",
    "FILTRAU",
    "FORFOLLAU",
    "FURGUESSEU",
    "GELATINITZASSIU",
    "GRATIFICAREN",
    "HEROISME",
    "IMMOLARES",
    "INEDUCABLES",
    "INTERFERIRIES",
    "JUGO",
    "LA",
    "MADRASSA",
    "MANS",
    "MENTISSIS",
    "MI",
    "MOBLIN",
    "MURMURI",
    "NOSTOCALS",
    "ODI",
    "ON",
    "PA",
    "PEDREGADES",
    "PI",
    "PIN",
    "PLANTOFES",
    "POSICIONASSIU",
    "PREMI",
    "PUDELASSIU",
    "RA",
    "RANCI",
    "RE",
    "RECENTMENT",
    "REESMERÇADA",
    "REJUNTESSIN",
    "REPLANTARIEN",
    "RETINGUEN",
    "ROBOTITZADA",
    "SALESSEN",
    "SEMPITERNITAT",
    "SOBREEIXIRIES",
    "SORRAMOLLS",
    "SUPERARIEM",
    "TALLER",
    "TOTAL",
    "TRANSVASARAS",
    "TRONXON",
    "VANAGLORIESSIN",
    "VISA",
    "XIPOLLESSIM"
]
# VARIABLES GLOBALES
dim = [0,0]         # DIMENSIONES DEL TABLERO
board = []          # TABLERO
boardAux = []
LVA = {}            # LLISTA VALORS ASSIGNATS
LVNA = []           # LLISTA VALORS NO ASSIGNATS
HORIZONTAL = '0'    # CODIGO PARA PALABRA HORIZONTAL
VERTICAL = '1'      # CODIGO PARA PALABRA VERTICAL

def horizontal(lista, cap):
    for fila in range(dim[0]):
        for columna in range(dim[1]):
            if board[fila][columna] == '0' and len(lista) < dim[0]:
                if cap == ['','','', 0]: #guardar l'inici de les paraules
                    cap = [fila, columna, HORIZONTAL, 0]
                lista.append('0')
            else:
                if len(lista) > 1: cap[3]=len(lista); LVNA.append(cap.copy())
                lista.clear()
                cap = ['','','', 0]
        
        if len(lista) > 1: cap[3]=len(lista); LVNA.append(cap.copy())
        lista.clear()
        cap = ['','','', 0]

def vertical(lista, cap):
    for columna in range(dim[1]):
        for fila in range(dim[0]):
            if board[fila][columna] == '0' and len(lista) < dim[1]:
                if cap == ['','','', 0]: #guardar l'inici de les paraules
                    cap = [fila, columna, VERTICAL, 0]
                lista.append('0')
            else:
                if len(lista) > 1: cap[3]=len(lista); LVNA.append(cap.copy())
                lista.clear()
                cap = ['','','', 0]
                
        if len(lista) > 1: cap[3]=len(lista); LVNA.append(cap.copy())
        lista.clear()
        cap = ['','','', 0]

def load_LVNA():
    lista = []
    cap = ['','','', 0] #fila , columna, direccion, longitud
    # TODO: poner longitud
    horizontal(lista, cap)
    vertical(lista, cap)

def load_puzzle_crossword(filename):
    with open(filename, 'r') as fileCW:
        # Obtain file content by rows.
        CW = fileCW.readlines()
    # Load text file into a NumPy matrix.
    for row in CW:
        row = [str(square) for square in row.strip().split('\t')]
        board.append(row)
        dim[0] = len(board)
        dim[1] = len(board[0]) #guardamos la dimension

def load_dictionary(filename):
    dictionary = []
    with open(filename, 'r') as fileDict:
        for line in fileDict:
            dictionary.append(line.strip())
    return dictionary

def satisfy_restriccions(assignWord, Var):
    # Coincidan las longitudes
    if len(assignWord) == Var[3]: 
        #Mirar si coinciden letras
        fila = int(Var[0])
        columna = int(Var[1])
        direccion = Var[2]
        hueco = []
        
        for i in range(Var[3]):
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
    boardAux.clear()
    if len(board) > 0: #COMO IMPLEMENTAR ESTO
        for fila in board:
            boardAux.append(fila.copy())
    Var = LVNA[0]
    for assignWord in D:
        if satisfy_restriccions(assignWord, Var):
            update_board(Var, assignWord)
            LVA[assignWord] = Var
            Res = backtracking(LVA, LVNA[1:], D)
            if Res is not None:
                return Res
            else:
                board.clear()
                for fila in boardAux:
                    board = fila.copy()
    return None

def update_board(Var, assignWord):
    fila = Var[0]
    columna = Var[1]
    for i in range(Var[3]):
        board[fila][columna] = assignWord[i]
        if Var[2] == HORIZONTAL:
            columna = columna + 1
        else:
            fila = fila + 1

if __name__ == '__main__':

    # Carga de tablero y diccionario.
    load_puzzle_crossword("crossword_CB_v3.txt") 
    load_LVNA()

    # TODO Arreglar diccionario.
    # dictionary = load_dictionary("diccionari_CB_v3.txt")
    
    # Function call.
    res = backtracking(LVA, LVNA, D)

    if res is not None:
      print(res)
    else:
        print("Incorrect result.")
