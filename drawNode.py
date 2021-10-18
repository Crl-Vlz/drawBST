import pygame

class drawNode:
    def __init__(self, value, color, radius):
        value = str(value)
        self.value = value
        screen = pygame.Surface
        pygame.draw.circle(screen, color, (radius/2, radius/2), radius)
        pygame.font.init()
        textImg = pygame.render(value, False, (000, 000, 000))
        screen.blit(textImg)
        pygame.font.quit()
        return screen