import pygame

class Proyectil(pygame.sprite.Sprite):
    def __init__(self, x, y, flip):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill('Cyan')  # Color rojo para el proyectil
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5  # Velocidad del proyectil
        self.flip = flip  # Orientación del proyectil

    def update(self, screen_width):
        if self.flip:
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
        if self.rect.right < 0 or self.rect.left > screen_width:
            self.kill()