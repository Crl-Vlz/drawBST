import pygame
from collections import namedtuple
from collections import deque
from pygame.locals import QUIT
from time import sleep
from dataclasses import dataclass
from math import inf
from drawNode import drawNode
from pygame import Color, Surface

color=dict()
color["circle"] = "#A0F5F6"
color["line"] = "#9F8BF5"
color["activeC"] = "#ADF67C"
color["activeL"] = "#F5A0C1"

def inicializar():
    i = input()
    f = open(i + ".in")
    lines = f.readlines()

    instrucciones = list()

    for line in lines:
        line = line.rstrip("\n")
        line = line.split()
        instrucciones.append(line)
    return instrucciones
    

@dataclass
class Nodo:
    pass

@dataclass #para no poner constructor --- es ponerle una etiqueta
class Nodo:
    llave: int
    valor: str = ""
    padre: Nodo = None
    izquierdo: Nodo = None
    derecho: Nodo = None
    visual: pygame.Surface = None
    line: pygame.Rect = None


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
        navList = []
        while True:
            sleep(0.1)
            if llave == actual.llave:
                return actual, navList
            if llave < actual.llave:
                if not actual.izquierdo:
                        return None, []
                actual = actual.izquierdo
                navList.append(actual)
            else:
                if not actual.derecho:
                        return None, []
                actual = actual.derecho
                navList.append(actual)

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
            Nodo, uselessList = self.buscar(Nodo)
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


def main():
    pygame.init()
    instrucciones = inicializar()
    arb = bst()
    coords = dict()
    screenSize = 500
    pantalla = pygame.display.set_mode((screenSize*2, screenSize))
    artist = drawNode()
    searchNodes = []

    w = 0
    h = 0

    pantalla.fill((255,255,255))


    pygame.display.update()

    for i in instrucciones:
        pantalla.fill((255,255,255))
        nodo = int(i[1])
        print(nodo)
        if i[0] == "INSERTAR":
            arb.insertar(nodo, nodo)
            inOrd = arb.inorden(arb.raiz.izquierdo)
            for iter in range(len(inOrd)):
                x,y = (iter, arb.profundidad(inOrd[iter]))
                coords[inOrd[iter].valor] = x, y
            altura = arb.altura()
            width = 2**altura + 1
            height = altura+1
            w = screenSize*2/width
            h = screenSize/height
            pantalla.fill((255, 255, 255))
            for node in inOrd:
                if node.visual:
                    x, y = coords[node.valor]
                    node.visual = pygame.transform.scale(node.visual, (w, w))
                    if node.line:
                        xp, yp = coords[node.padre.valor]
                        node.line = pygame.draw.line(pantalla, color["line"], (w*x+w*.5, h*y), (w*xp+w*.5, h*yp), 2)
                        #pygame.Surface.blit(pantalla, node.line, (w*x, h*y))
                    pygame.Surface.blit(pantalla, node.visual, (w*x, h*y))
                else:
                    node.visual = artist.draw(node.valor, color["activeC"], w/2, round(w/2))
                    x, y = coords[node.valor]
                    pygame.Surface.blit(pantalla, node.visual, (w*x, h*y))
                    if node.padre and node.padre.valor:
                        xp, yp = coords[node.padre.valor]
                        node.line = pygame.draw.line(pantalla, color["activeL"], (w*x+w*.5, h*y), (w*xp+w*.5, h*yp), 2)
                sleep(0.1)
                node.visual.fill((255, 255, 255))
                node.visual = artist.draw(node.valor, color["circle"], w/2, round(w/2))
                if node.line:
                    node.line = pygame.draw.line(pantalla, color["line"], (w*x+w*.5, h*y), (w*xp+w*.5, h*yp), 2)
                pygame.display.update()

        if i[0] == "BUSCAR":
            encontrado, lista = arb.buscar(nodo)
            inOrd = arb.inorden(arb.raiz.izquierdo)
            for node in inOrd:
                node.visual = pygame.transform.scale(node.visual, (w, w))
                x, y = coords[node.valor]
                pygame.Surface.blit(pantalla, node.visual, (w*x, h*y))
                node.visual.fill((255, 255, 255))
                node.visual = artist.draw(node.valor, color["circle"], w/2, round(w/2))
            for node in lista:
                x, y = coords[node.valor]
                node.visual = artist.draw(node.valor, color["activeC"], w/2, round(w/2))
                pygame.Surface.blit(pantalla, node.visual, (w*x, h*y))
                pygame.display.update()
                sleep(1)
            for node in lista:
                node.visual.fill((255, 255, 255))
                node.visual = artist.draw(node.valor, color["circle"], w/2, round(w/2))
                x, y = coords[node.valor]
                pygame.Surface.blit(pantalla, node.visual, (w*x, h*y))
            pygame.display.update()
        if i[0] == "ELIMINAR":
            arb.eliminar(nodo)
            inOrd = arb.inorden(arb.raiz.izquierdo)
            for iter in range(len(inOrd)):
                x,y = (iter, arb.profundidad(inOrd[iter]))
                coords[inOrd[iter].valor] = x, y
            altura = arb.altura()
            width = 2**altura + 1
            height = altura+1
            w = screenSize*2/width
            h = screenSize/height
            for node in inOrd:
                if node.visual:
                    #Add this
                    node.visual = pygame.transform.scale(node.visual, (w, w))
                    x, y = coords[node.valor]
                    pygame.Surface.blit(pantalla, node.visual, (w*x, h*y))
                    #pantalla.blit(node.visual, (w*x, h*y))
                else:
                    node.visual = artist.draw(node.valor, color["activeC"], w/2, round(w/2))
                    x, y = coords[node.valor]
                    pygame.Surface.blit(pantalla, node.visual, (w*x, h*y))
                    #pantalla.blit(node.visual, (w*x, h*y))
                sleep(0.1)
                node.visual.fill(color["circle"])
        if i[0] == "ROTAR":
            pass
            #arb.doble_rotar(nodo)

        altura = arb.altura()
        width = 2**altura + 1
        height = altura+1
        w = screenSize*2/width
        h = screenSize/height

        #for i in range(len(inOrd)):
        #    x, y = coords[inOrd[i].valor]
        #    if inOrd[i].valor == nodo and inOrd[i].padre.valor is not None :
        #        xp, yp = coords[inOrd[i].padre.valor]
        #        pygame.draw.line(pantalla, color["activeL"], (w*x+w*.5, h*y), (w*xp+w*.5, h*yp), 2)
        #    else :  
        #        if inOrd[i].padre.valor is not None:
        #            xp, yp = coords[inOrd[i].padre.valor]
        #            pygame.draw.line(pantalla, color["line"], (w*x+w*.5, h*y), (w*xp+w*.5, h*yp), 2)

        pygame.display.update()
        #sleep(.1)	

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            pygame.display.update()
            sleep(.1)		


main()