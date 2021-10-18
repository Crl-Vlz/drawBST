import pygame
from collections import namedtuple
from collections import deque
from pygame.locals import QUIT
from time import sleep

color=dict()
color["circle"] = "#A0F5F6"
color["line"] = "#ADF67C"
color["activeC"] = "#9F8BF5"
color["activeL"] = "#F5A0C1"

from dataclasses import dataclass
from math import inf

@dataclass #para no poner constructor --- es ponerle una etiqueta
class nodo:
    llave: int
    valor: str = ""
    padre: str = None
    izquierdo: str = None
    derecho: str = None



@dataclass
class bst:
    def __init__(self): #Infinito para que cualquier valor se vaya a la izq al ser menor a inf
        self.raiz = Nodo(inf, None)


    def insertar(self, llave, valor=""):
        actual = self.raiz
        while True:
            #Insertando los nodos            CONDICIONES DE PARO
            if llave < actual.llave and not actual.izquierdo:
                actual.izquierdo=Nodo(llave, valor)
                actual.izquierdo.padre = actual
                break
            if llave>= actual.llave and not actual.derecho:
                actual.derecho = Nodo(llave, valor)
                actual.derecho.padre = actual
                break
            #Recorriendo derecho o izq             ITERACIÓN
            if llave < actual.llave:
                actual = actual.izquierdo
            else:
                actual = actual.derecho


    def buscar(self, llave):
        actual = self.raiz
        while True:
            if llave == actual.llave:
                return actual
            if llave < actual.llave:
                if not actual.izquierdo:
                        return None
                actual = actual.izquierdo
            else:
                if not actual.derecho:
                        return None
                actual = actual.derecho

    def anterior(self, nodo):
        if nodo.izquierdo:
            return self.maximo(nodo.izquierdo)
        else:
            padre = nodo.padre
            if not padre : return None
            while padre.izquierdo == nodo:
                nodo = nodo.padre
                padre = padre.padre
                if not padre : return None
            return padre
    
    def maximo(self, nodo):
        while nodo.derecho:
            nodo = nodo.derecho
        return nodo

    def minimo(self, nodo):
        while nodo.izquierdo:
            nodo = nodo.izquierdo
        return nodo

    def intercambiar(self, nodo1, nodo2):
        nodo1.llave, nodo2.llave = nodo2.llave, nodo1.llave
        nodo1.valor, nodo2.valor = nodo2.valor, nodo1.valor
    
    def eliminar(self, nodo):
        if type(nodo) == int:
            nodo = self.buscar(nodo)
        #Caso 1: nodo sin hijos
        if not nodo.izquierdo and not nodo.derecho:
            padre = nodo.padre
            if padre.izquierdo==nodo:
                padre.izquierdo = None
            else:
                padre.derecho = None
        #Caso 2: nodo con 1 hijo
        elif not nodo.izquierdo or not nodo.derecho:
            if nodo.izquierdo:
                hijo = nodo.izquierdo
            else:
                hijo = nodo.derecho
            padre = nodo.padre
            if padre.izquierdo == nodo:
                padre.izquierdo = hijo
            else:
                padre.derecho = hijo
        #Caso 3: nodo con hijos
        else:
            anterior = self.anterior(nodo)
            self.intercambiar(anterior, nodo)
            self.eliminar(anterior)

    def preorden(self, nodo):
        if not nodo: return []
        return [nodo.valor] + self.preorden(nodo.izquierdo) + self.preorden(nodo.derecho)

    def inorden(self, nodo):
        if not nodo: return []
        return self.inorden(nodo.izquierdo) + [nodo.valor] + self.inorden(nodo.derecho)

    def postorden(self, nodo):
        if not nodo: return []
       return self.postorden(nodo.izquierdo) + self.postorden(nodo.derecho) + [nodo.valor]


def main():
	pygame.init()

	screenSize = 400
	pantalla = pygame.display.set_mode((screenSize, screenSize))
	pantalla.fill((255,255,255))

	#w = screenSize/i
	#h = screenSize/j
	

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
			pygame.display.update()
			sleep(.1)		
	


main()