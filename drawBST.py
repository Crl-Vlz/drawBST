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

coords = dict()


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
    altura: int = 0
    visual: pygame.Surface = None
    line: pygame.Rect = None

    def alturaIzquierda(self):
        return self.izquierdo.altura if self.izquierdo else 0

    def alturaDerecha(self):
        return self.derecho.altura if self.derecho else 0

    def __repr__(self):
        return "Nodo: " + str(self.valor)



class bst:
    def __init__(self, pantalla, screenSize, artist): #Infinito para que cualquier valor se vaya a la izq al ser menor a inf
        self.raiz = Nodo(inf, None)
        self.pantalla = pantalla
        self.screenSize = screenSize
        self.artist = artist
       
    def __repr__(self):
        return f"Nodo {self.raiz}"

    def recalcular_altura(self, p: Nodo) -> None:
        p.altura = max(p.alturaIzquierda(), p.alturaDerecha()) + 1

    def estaBalanceado(self, p: Nodo) -> bool:
        return abs(p.alturaIzquierda() - p.alturaDerecha()) <= 1

    def hijoAlto(self, p: Nodo) -> Nodo:
        if p.alturaIzquierda() > p.alturaDerecha(): return p.izquierdo
        else: return p.derecho

    def nietoAlto(self, p: Nodo) -> Nodo:
        hijo = self.hijoAlto(p)
        return self.hijoAlto(hijo)

    def rebalancear(self, p: Nodo) -> None:
        while p!= self.raiz:
            alturaAnterior = p.altura
            if not self.estaBalanceado(p):
                p = self.doble_rotar(self.nietoAlto(p))
                if p.izquierdo: self.recalcular_altura(p.izquierdo)
                if p.derecho: self.recalcular_altura(p.derecho)
            self.recalcular_altura(p)
            if p.altura == alturaAnterior: p = self.raiz
            else: p = p.padre

    def insertar(self, llave, valor="") -> Nodo:
        actual= self.raiz
        while True:
            ## Condiciones de paro
            if llave< actual.llave and not actual.izquierdo:
                actual.izquierdo= Nodo(llave, valor)
                actual.izquierdo.padre= actual
                print(actual.izquierdo, end="--- Nodo Padre: ")
                break
            if llave>= actual.llave and not actual.derecho:
                actual.derecho = Nodo(llave, valor)
                actual.derecho.padre= actual
                break
            ## Condiciones de iteración
            if llave< actual.llave:
                actual= actual.izquierdo
            else: 
                actual= actual.derecho
        print(actual)
        return actual

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

    def buscar(self, llave: int):
        actual = self.raiz
        navList = []
        while True:
            sleep(0.1)
            if llave == actual.llave:
                self.dibujarBuscarNodo(navList)
                return actual
            if llave < actual.llave:
                if not actual.izquierdo:
                        return None
                actual = actual.izquierdo
                navList.append(actual)
            else:
                if not actual.derecho:
                        return None
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
    

    def eliminar(self, Nodo) -> Nodo:
        if type(Nodo) == int:
            Nodo = self.buscar(Nodo)

        padre = Nodo.padre

        #Caso 1: Nodo sin hijos
        if not Nodo.izquierdo and not Nodo.derecho:
            if padre.izquierdo==Nodo:
                padre.izquierdo = None
            else:
                padre.derecho = None
            Nodo.visual = None
            Nodo.line = None
        #Caso 2: Nodo con 1 hijo
        elif not Nodo.izquierdo or not Nodo.derecho:
            if Nodo.izquierdo:
                hijo = Nodo.izquierdo
            else:
                hijo = Nodo.derecho
            if padre.izquierdo == Nodo:
                padre.izquierdo = hijo
            else:
                padre.derecho = hijo
            hijo.padre = padre
        #Caso 3: Nodo con hijos
        else:
            anterior = self.anterior(Nodo)
            if anterior is not None:
                self.intercambiar(anterior, Nodo)
                self.eliminar(anterior)

        return padre

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

    def rotar(self, Nodo) :
        NodoY = Nodo.padre #padre de x
        NodoZ = NodoY.padre #abuelo de x
        self.religar(NodoZ, Nodo,NodoY==NodoZ.izquierdo)
        if Nodo==NodoY.izquierdo :
            self.religar(NodoY,Nodo.derecho,True)
            self.religar(Nodo,NodoY,False)
        if Nodo==NodoY.derecho :
            self.religar(NodoY,Nodo.izquierdo,False)
            self.religar(Nodo,NodoY,True)
    
    def doble_rotar(self,Nodo) :

        if type(Nodo) == int:
            Nodo = self.buscar(Nodo)

        NodoY = Nodo.padre
        NodoZ = NodoY.padre
        if (Nodo==NodoY.derecho) == (NodoY==NodoZ.derecho):
            self.rotar(NodoY)
        else :
            self.rotar(Nodo)
            self.rotar(Nodo)
        return Nodo

    def dibujarInsertarNodo(self):
        inOrd = self.inorden(self.raiz.izquierdo)
        for iter in range(len(inOrd)):
            x,y = (iter, self.profundidad(inOrd[iter]))
            coords[inOrd[iter].valor] = x, y
        altura = self.altura()
        width = 2**altura + 1
        height = altura+1
        w = self.screenSize*2/width
        h = self.screenSize/height
        for node in inOrd:
            if node.visual:
                x, y = coords[node.valor]
                node.visual = pygame.transform.scale(node.visual, (round(w), round(w)))
                if node.line:
                    xp, yp = 0, 0
                    if node.padre.valor in coords:
                        xp, yp = coords[node.padre.valor]
                    node.line = pygame.draw.line(self.pantalla, color["line"], (w*x+w*.5, h*y), (w*xp+w*.5, h*yp), 2)
                pygame.Surface.blit(self.pantalla, node.visual, (w*x, h*y))
            else:
                node.visual = self.artist.draw(node.valor, color["activeC"], w/2, round(w/2))
                x, y = coords[node.valor]
                pygame.Surface.blit(self.pantalla, node.visual, (w*x, h*y))
                if node.padre and node.padre.valor:
                    xp, yp = coords[node.padre.valor]
                    node.line = pygame.draw.line(self.pantalla, color["activeL"], (w*x+w*.5, h*y), (w*xp+w*.5, h*yp), 2)
            node.visual.fill((255, 255, 255))
            node.visual = self.artist.draw(node.valor, color["circle"], w/2, round(w/2))
            if node.line:
                node.line = pygame.draw.line(self.pantalla, color["line"], (w*x+w*.5, h*y), (w*xp+w*.5, h*yp), 2)

    def dibujarBuscarNodo(self, lista):
        inOrd = self.inorden(self.raiz.izquierdo)
        altura = self.altura()
        width = 2**altura + 1
        height = altura+1
        w = self.screenSize*2/width
        h = self.screenSize/height
        for node in inOrd:
            node.visual = pygame.transform.scale(node.visual, (round(w), round(w)))
            x, y = coords[node.valor]
            pygame.Surface.blit(self.pantalla, node.visual, (w*x, h*y))
            node.visual.fill((255, 255, 255))
            node.visual = self.artist.draw(node.valor, color["circle"], w/2, round(w/2))
            if node.line:
                xp, yp = 0, 0
                if node.padre.valor in coords:
                    xp, yp = coords[node.padre.valor]
                node.line = pygame.draw.line(self.pantalla, color["line"], (w*x+w*.5, h*y), (w*xp+w*.5, h*yp), 2)
        for node in lista:
            x, y = coords[node.valor]
            node.visual = self.artist.draw(node.valor, color["activeC"], w/2, round(w/2))
            if node.line:
                xp, yp = 0, 0
                if node.padre.valor in coords:
                    xp, yp = coords[node.padre.valor]
                node.line = pygame.draw.line(self.pantalla, color["activeL"], (w*x+w*.5, h*y), (w*xp+w*.5, h*yp), 2)
            pygame.Surface.blit(self.pantalla, node.visual, (w*x, h*y))
            pygame.display.update()
            sleep(1)
        for node in lista:
            node.visual = self.artist.draw(node.valor, color["circle"], w/2, round(w/2))
            x, y = coords[node.valor]
            if node.line:
                xp, yp = 0, 0
                if node.padre.valor in coords:
                    xp, yp = coords[node.padre.valor]
                node.line = pygame.draw.line(self.pantalla, color["line"], (w*x+w*.5, h*y), (w*xp+w*.5, h*yp), 2)
            pygame.Surface.blit(self.pantalla, node.visual, (w*x, h*y))

    def dibujarEliminarNodo(self):
        inOrd = self.inorden(self.raiz.izquierdo)
        altura = self.altura()
        width = 2**altura + 1
        height = altura+1
        w = self.screenSize*2/width
        h = self.screenSize/height
        for iter in range(len(inOrd)):
            x,y = (iter, self.profundidad(inOrd[iter]))
            coords[inOrd[iter].valor] = x, y
        altura = self.altura()
        width = 2**altura + 1
        height = altura+1
        w = self.screenSize*2/width
        h = self.screenSize/height
        for node in inOrd:
            if node.visual:
                node.visual = self.artist.draw(node.valor, color["circle"], w/2, round(w/2))
                x, y = coords[node.valor]
                pygame.Surface.blit(self.pantalla, node.visual, (w*x, h*y))
                if node.line:
                    xp, yp = 0, 0
                    if node.padre.valor in coords:
                        xp, yp = coords[node.padre.valor]
                    node.line = pygame.draw.line(self.pantalla, color["line"], (w*x+w*.5, h*y), (w*xp+w*.5, h*yp), 2)
            self.pantalla.fill((255, 255, 255))
            pygame.display.update()

class AVL(bst):

    def insertar(self, llave: int, valor: str ="") -> None:
        p = super().insertar(llave, valor)
        self.rebalancear(p)

    def eliminar(self, Nodo: Nodo) -> None:
        p =  super().eliminar(Nodo)
        self.rebalancear(p)
    


def grid(width, height, w, h, pantalla):
    m = 1
    for row in range(height):
        for column in range(width):
            color = "#FFFFFF"
            pygame.draw.rect(pantalla, color, [(m + w) * column + m, (m + h) * row + m, w, h])


def main():
    pygame.init()
    instrucciones = inicializar()
    screenSize = 500
    pantalla = pygame.display.set_mode((screenSize*2, screenSize))
    artist = drawNode()
    arb = AVL(pantalla, screenSize, artist)

    w = 0
    h = 0

    for i in instrucciones:
        pantalla.fill((255,255,255))
        nodo = int(i[1])
        if i[0] == "INSERTAR":
            pygame.display.set_caption('INSERTANDO '+ str(nodo))
            arb.insertar(nodo, nodo)
            arb.dibujarInsertarNodo()
            pygame.display.update()
            sleep(0.6)

        if i[0] == "BUSCAR":
            pygame.display.set_caption('BUSCANDO '+ str(nodo))
            arb.buscar(nodo)
        if i[0] == "ELIMINAR":
            pygame.display.set_caption('ELIMINANDO '+ str(nodo))
            arb.eliminar(nodo)
            arb.dibujarEliminarNodo()

            
        if i[0] == "ROTAR":
            pygame.display.set_caption('ROTANDO '+ str(nodo))
            arb.doble_rotar(nodo)
            pantalla.fill((255, 255, 255))
            arb.dibujarInsertarNodo()
            pygame.display.update()
            sleep(0.6)

        altura = arb.altura()
        width = 2**altura + 1
        height = altura+1
        w = screenSize*2/width
        h = screenSize/height


    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            pygame.display.update()	

#NO SE ACTUALIZA EL PADRE AL MODIFICAR NODOS

main()