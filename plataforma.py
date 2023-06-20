import pygame

class Plataforma():
    def __init__(self, x, y, width, height, color):
        self.rectangulo = pygame.Rect(x, y, width, height)
        self.color = color
    
    def pintar(self, surface):
        pygame.draw.rect(surface, self.color, self.rectangulo)
