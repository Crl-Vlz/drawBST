import pygame
from time import sleep

# Returns a pygame Surface that can then be drawn to show an individual node
# this does not include the arysts
class drawNode:
    def _init_(self):
        pass
    def draw(self, value, color, radius, f):
        value = str(value)
        self.value = value
        screen = pygame.Surface((radius*2, radius*2))
        screen.fill((255, 255, 255, 0))
        pygame.draw.circle(screen, color, (radius, radius), radius)
        pygame.font.init()
        font = pygame.font.SysFont(None, f)
        textImg = font.render(value, False, (000, 000, 000))
        pygame.Surface.blit(screen, textImg, (radius, radius))
        pygame.font.quit()
        return screen