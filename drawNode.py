import pygame, sys

class drawNode:
    def __init__(self, value, color, center, radius):
        value = str(value)
        self.value = value
        screen = pygame.Surface
        pygame.draw.circle(screen, color, center, radius)
        pygame.font.init()
        textImg = pygame.render(value, False, (000, 000, 000))
        screen.blit(textImg)
        pygame.font.quit()
        return screen