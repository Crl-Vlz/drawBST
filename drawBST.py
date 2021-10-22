import pygame
from collections import namedtuple
from collections import deque
from pygame.locals import QUIT
from time import sleep
from dataclasses import dataclass
from math import inf
from drawNode import drawNode

color=dict()
color["circle"] = "#A0F5F6"
color["line"] = "#9F8BF5"
color["activeC"] = "#ADF67C"
color["activeL"] = "#F5A0C1"

def inicializar():
    i = input()
    f = open(i + ".in")

    line = f.readline().split()
    return line
    

@dataclass #para no poner constructor --- es ponerle una etiqueta
class Nodo:
    llave: int
    valor: str = ""
    padre: str = None
    izquierdo: str = None
    derecho: str = None


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

    def profundidad(self, nodo):
        conteo = 0
        while nodo!= self.raiz:
            conteo+=1
            nodo = nodo.padre
        return conteo -1

    def altura(self, nodo=None):
        cont1 = 0
        cont2 = 0
        cont = 0
        if nodo == None:
            nodo = self.raiz.izquierdo
        cont+=1
        if nodo.izquierdo != None :
            cont1 = cont + self.altura(nodo.izquierdo)    
        if nodo.derecho != None :
            cont2 = cont + self.altura(nodo.derecho)
        if cont1 > cont2 :
            return cont1
        else:
            return cont2

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
        return self.inorden(Nodo.izquierdo) + [Nodo] + self.inorden(Nodo.derecho)


    def postorden(self, Nodo):
        if not Nodo:return []
        return self.postorden(Nodo.izquierdo) + self.postorden(Nodo.derecho) + [Nodo.valor]

    def religar(self, padre, hijo, es_izquierdo) :
        if es_izquierdo:
            padre.izquierdo = hijo
        else :
            padre.derecho = hijo
        if hijo is not None :
            hijo.padre = padre

    def rotar(self, x) :
        y = x.padre #padre de x
        z = y.padre #abuelo de x
        self.religar(z,x,y==z.izquierdo)
        if x==y.izquierdo :
            self.religar(y,x.derecho,True)
            self.religar(x,y,False)
        if x==y.derecho :
            self.religar(y,x.izquierdo,False)
            self.religar(x,y,True)
    
    def doble_rotar(self,x) :
        y = x.padre
        z = y.padre
        if (x==y.derecho) == (y==z.derecho) :
            self.rotar(y)
        else :
            self.rotar(x)
            self.rotar(x)


def grid(width, height, w, h, pantalla):
    m = 1
    for row in range(height):
        for column in range(width):
            color = "#FFFFFF"
            pygame.draw.rect(pantalla, color, [(m + w) * column + m, (m + h) * row + m, w, h])
            print(column)

def cambiarColor (Nodo, x, y, xp, yp, pantalla, w, h, artist) :
    pygame.draw.line(pantalla, color["line"], (w*x+w*.5, h*y), (w*xp+w*.5, h*yp), 2)
    pygame.Surface.blit(pantalla, artist.draw(Nodo.valor, color["circle"], w/2, round(w/2)), (w*x, h*y))


def main():
    pygame.init()
    nodos = inicializar()
    arb = bst()
    coords = dict()

    for nodo in nodos:
        arb.insertar(int(nodo), int(nodo))
    inOrd = arb.inorden(arb.raiz.izquierdo)
    altura = arb.altura()
    width = 2**altura + 1
    height = altura+1

    screenSize = 500
    pantalla = pygame.display.set_mode((screenSize*2, screenSize))
    pantalla.fill((255,255,255))

    w = screenSize*2/width
    h = screenSize/height

    grid(width, height, w, h, pantalla)

    artist = drawNode()

    for i in range(len(inOrd)):
        x,y = (i, arb.profundidad(inOrd[i]))
        coords[inOrd[i].valor] = x, y

    for i in range(len(inOrd)):
        x, y = coords[inOrd[i].valor]
        if inOrd[i].padre.valor is not None:
            xp, yp = coords[inOrd[i].padre.valor]
            pygame.draw.line(pantalla, color["line"], (w*x+w*.5, h*y), (w*xp+w*.5, h*yp), 2)
    
    for i in range(len(inOrd)):
        x, y = coords[inOrd[i].valor]
        pygame.Surface.blit(pantalla, artist.draw(inOrd[i].valor, color["circle"], w/2, round(w/2)), (w*x, h*y))

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            pygame.display.update()
            sleep(.1)		


main()