import pygame

class Plataforma():
    def __init__(self, x, y, width, height, color):
        self.rectangulo = pygame.Rect(x, y, width, height)
        self.color = (0, 0, 0, 0)
    
    def pintar(self, surface):
        if self.color[3] != 0:  # Verificar si el color no es transparente
            pygame.draw.rect(surface, self.color, self.rectangulo)