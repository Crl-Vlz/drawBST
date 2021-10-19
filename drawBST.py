import pygame
from collections import namedtuple
from collections import deque
from pygame.locals import QUIT
from time import sleep
from dataclasses import dataclass
from math import inf

color=dict()
color["circle"] = "#A0F5F6"
color["line"] = "#ADF67C"
color["activeC"] = "#9F8BF5"
color["activeL"] = "#F5A0C1"

def inicializar():
    i = input()
    f = open(i + ".in")
    line = f.readline().split(" ")
    return line
    

@dataclass #para no poner constructor --- es ponerle una etiqueta
class Nodo:
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
            #Insertando los Nodos            CONDICIONES DE PARO
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


    def anterior(self, Nodo):
        if Nodo.izquierdo:
            return self.maximo(Nodo.izquierdo)
        else:
            padre = Nodo.padre
            if not padre : return None
            while padre.izquierdo == Nodo:
                Nodo = Nodo.padre
                padre = padre.padre
                if not padre : return None
            return padre
    

    def maximo(self, Nodo):
        while Nodo.derecho:
            Nodo = Nodo.derecho
        return Nodo


    def minimo(self, Nodo):
        while Nodo.izquierdo:
            Nodo = Nodo.izquierdo
        return Nodo


    def intercambiar(self, Nodo1, Nodo2):
        Nodo1.llave, Nodo2.llave = Nodo2.llave, Nodo1.llave
        Nodo1.valor, Nodo2.valor = Nodo2.valor, Nodo1.valor
    

    def eliminar(self, Nodo):
        if type(Nodo) == int:
            Nodo = self.buscar(Nodo)
        #Caso 1: Nodo sin hijos
        if not Nodo.izquierdo and not Nodo.derecho:
            padre = Nodo.padre
            if padre.izquierdo==Nodo:
                padre.izquierdo = None
            else:
                padre.derecho = None
        #Caso 2: Nodo con 1 hijo
        elif not Nodo.izquierdo or not Nodo.derecho:
            if Nodo.izquierdo:
                hijo = Nodo.izquierdo
            else:
                hijo = Nodo.derecho
            padre = Nodo.padre
            if padre.izquierdo == Nodo:
                padre.izquierdo = hijo
            else:
                padre.derecho = hijo
        #Caso 3: Nodo con hijos
        else:
            anterior = self.anterior(Nodo)
            self.intercambiar(anterior, Nodo)
            self.eliminar(anterior)


    def preorden(self, Nodo):
        if not Nodo: return []
        return [Nodo.valor] + self.preorden(Nodo.izquierdo) + self.preorden(Nodo.derecho)


    def inorden(self, Nodo):
        if not Nodo: return []
        return self.inorden(Nodo.izquierdo) + [Nodo.valor] + self.inorden(Nodo.derecho)


    def postorden(self, Nodo):
        if not Nodo:return []
        return self.postorden(Nodo.izquierdo) + self.postorden(Nodo.derecho) + [Nodo.valor]


def main():
    pygame.init()
    nodos = inicializar()
    arb = bst()
    for nodo in nodos:
        arb.insertar(int(nodo), int(nodo))
    preO = preorden(arb.raiz.hijo)
    print(arb)

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