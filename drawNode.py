import pygame
from time import sleep

class drawNode:
    def __init__(self):
        pass
    def draw(self, value, color, center, radius):
        value = str(value)
        self.value = value
        screen = pygame.Surface
        pygame.draw.circle(screen, color, center, radius)
        pygame.font.init()
        textImg = pygame.render(value, False, (000, 000, 000))
        screen.blit(textImg)
        pygame.font.quit()
        return screen
    def changeColor(self, surface, activeColor, passiveColor):
        pygame.Surface.fill(surface, activeColor)
        sleep(0.1)
        pygame.Surface.fill(surface, passiveColor)