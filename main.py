import unittest
from Bactracking_BFC import *
import time


class TestCrosswordSolver(unittest.TestCase):
    def setUp(self):

        # Tauler 1

        dim = [0, 0]  # Dimensions del taulell

        ## Test case backtracking

        self.board = []  # TABLERO
        self.LVNA = []  # LLISTA VALORS NO ASSIGNATS

        # Carga de tablero y diccionario
        cargarCrossword("crossword_CB_v3.txt", self.board, dim)
        cargarLVNA(self.board, dim, self.LVNA)
        self.dictionary = cargarDiccionario("diccionari_CB_v3.txt")

        ##########################################

        ## Test case fordwardchecking
        self.boardFC = []
        self.LVNAFC = []

        # Carga de tablero y diccionario
        cargarCrossword("crossword_CB_v3.txt", self.boardFC, dim)
        cargarLVNA(self.boardFC, dim, self.LVNAFC)
        self.DA = inicializarDA(self.LVNAFC, self.dictionary)

        ##########################################

        ## Test case backtracking contant nodes recorreguts
        self.boardN = []
        self.LVNAN = []

        # Carga de tablero y diccionario
        cargarCrossword("crossword_CB_v3.txt", self.boardN, dim)
        cargarLVNA(self.boardN, dim, self.LVNAN)

        ########################################


        ## Test case fordwardchecking contant nodes recorreguts
        self.boardFCN = []
        self.LVNAFCN = []

        # Carga de tablero y diccionario
        cargarCrossword("crossword_CB_v3.txt", self.boardFCN, dim)
        cargarLVNA(self.boardFCN, dim, self.LVNAFCN)
        self.DAN = inicializarDA(self.LVNAFCN, self.dictionary)

        # Tauler 2
        dim2 = [0, 0]  # Dimensions del taulell

        # Test A con nodos

        self.boardA = []
        self.LVNAA = []

        # Carga de tablero y diccionario
        cargarCrossword("crossword_A.txt", self.boardA, dim2)
        cargarLVNA(self.boardA, dim2, self.LVNAA)
        self.dictionaryA = cargarDiccionario("diccionari_A_test50k.txt")
        self.DA_dictA = inicializarDA(self.LVNAA, self.dictionaryA)

        ########################################

        self.boardAN = []
        self.LVNAAN = []

        # Carga de tablero y diccionario
        cargarCrossword("crossword_A.txt", self.boardAN, dim2)
        cargarLVNA(self.boardAN, dim2, self.LVNAAN)
        self.DA_dictAN = inicializarDA(self.LVNAAN, self.dictionaryA)


    def test_backtracking_sense_nodes(self):
        start_time = time.time()
        result1 = backtracking([], self.LVNA, self.dictionary)
        end_time = time.time()
        print("Time taken:", end_time - start_time, "seconds")
        print_board(self.board, result1)
        self.assertIsNotNone(result1)

    def test_backForwardChecking_sense_nodes(self):
        start_time = time.time()
        result2 = backForwardChecking([], self.LVNAFC, self.DA)
        end_time = time.time()
        print("Time taken:", end_time - start_time, "seconds")
        print_board(self.board, result2)
        self.assertIsNotNone(result2)

    def test_backtracking_amb_nodes(self):
        count = [0]
        result3 = backtrackingCountNodes([], self.LVNAN, self.dictionary, count)
        print(f"Total de nodes recorreguts en el backtracking es {count[0]}")
        print_board(self.board, result3)
        self.assertIsNotNone(result3)

    def test_backForwardChecking_amb_nodes(self):
        count = [0]
        result4 = backForwardCheckingCountNodes([], self.LVNAFCN, self.DAN, count)
        print(f"Total de nodes recorreguts en el Fordward Checking es {count[0]}")
        print_board(self.board, result4)
        self.assertIsNotNone(result4)

    def test_diff_A(self):
        start_time = time.time()
        result5 = backForwardChecking([], self.LVNAA, self.DA_dictA)
        end_time = time.time()
        print("Time taken:", end_time - start_time, "seconds")
        print_board(self.boardA, result5)
        self.assertIsNotNone(result5)

    def test_diff_A_node(self):
        count = [0]
        result6 = backForwardCheckingCountNodes([], self.LVNAAN, self.DA_dictAN, count)
        print(f"Total de nodes recorreguts en el Fordward Checking es {count[0]}")
        print_board(self.boardAN, result6)
        self.assertIsNotNone(result6)


if __name__ == '__main__':
    unittest.main()

