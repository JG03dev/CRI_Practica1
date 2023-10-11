## Word class implementation

import numpy as np
from copy import copy, deepcopy


class Word:
    """
       Esta es una clase que representa a una palabra.

       Atributos:
            start (list): Coordenadas donde empieza la palabra.
            length (int): Longitud de la palabra.
            orientation (int): Orientacion en la que se escribe la palabra.
            linked_words (list of object word): Listado de palabras por las que se cruza en el tablero.
            value (string): Que palabra es.
    """
    start = [0, 0]
    length = 0
    orientation = 0  # 0 for Horizontal, 1 for Vertical
    linked_words = []  # TODO mirar d'utilitzar numpy per aquesta estructura
    value = ""

    def __init__(self, s, l, o, lw=None):
        """
           El constructor de la clase Word.

           Atributos:
                start (list): Coordenadas donde empieza la palabra.
                length (int): Longitud de la palabra.
                orientation (int): Orientacion en la que se escribe la palabra.
                linked_words (list of object word): Listado de palabras por las que se cruza en el tablero.
                value (string): Que palabra es.
        """
        self.start = s
        self.length = l
        self.orientation = o
        self.linked_words = copy(lw) if lw is not None else []
        self.value = ""

    def pertenece(self, casella):
        """
            A partir de una casilla miramos si esta pertenece a esta classe Word (self).

            Atributos:
                casilla (list): Una lista de listas que representa el tablero de juego.

            Return:
                (bool): Si la casilla esta dentro de la palabra devuelve True, en caso contrario devuelve False.

        """
        return ((self.orientation == 0 and self.start[1] <= casella[1] <= self.start[1] + self.length and self.start[0] == casella[0])
                    or (self.orientation == 1 and self.start[0] <= casella[0] <= self.start[0] + self.length and self.start[1] == casella[1]))

    def update_linked(self):
        """
            Actualizamos la lista de linked_words de las palabras las cuales sabemos que tenemos cruzamientos.

            Return:
                None

        """
        for w, c in self.linked_words:
            w.linked_words.append([self, c])