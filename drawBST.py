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