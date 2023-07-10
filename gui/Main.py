import pygame
import sys
from pygame.locals import *
from gui.GUI_forn_prueba import FormPrueba

pygame.init()
W = 1200
H = 600
FPS = 60

reloj = pygame.time.Clock()
pantalla = pygame.display.set_mode((W,H))


form_prueba = FormPrueba(pantalla, 200, 100, 900, 350, 'Gold', 'Magenta', 5, True)

while True:
    reloj.tick(FPS)
    eventos = pygame.event.get()
    for event in eventos:
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pantalla.fill('Black')

    form_prueba.update(eventos)

    pygame.display.flip()
        

