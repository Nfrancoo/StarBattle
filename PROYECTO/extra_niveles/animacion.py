import itertools
import os
import pygame

class AnimatedBackground(pygame.sprite.Sprite):
    def __init__(self, position, images, delay):
        super(AnimatedBackground, self).__init__()

        self.images = itertools.cycle(images)
        self.image = next(self.images)
        self.rect = self.image.get_rect(topleft=position)

        self.animation_time = delay
        self.current_time = 0

    def update(self, dt):
        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.image = next(self.images)

def load_images(path):
    images = [pygame.image.load(path + os.sep + file_name).convert() for file_name in sorted(os.listdir(path))]
    return images
