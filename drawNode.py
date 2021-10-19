import pygame

# Returns a pygame Surface that can then be drawn to show an individual node
# this does not include the arysts
class drawNode:
    def __init__(self):
        pass
    def draw(self, value, color, radius):
        value = str(value)
        self.value = value
        screen = pygame.Surface((radius*2, radius*2))
        pygame.draw.circle(screen, color, (radius/2, radius/2), radius)
        pygame.font.init()
        font = pygame.font.SysFont(None, 12)
        textImg = font.render(value, False, (000, 000, 000))
        pygame.Surface.blit(screen, textImg, (radius/2, radius/2))
        pygame.font.quit()
        return screen