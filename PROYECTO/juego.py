import pygame
import sys
from gui.GUI_forn_prueba import *


# Inicializar Pygame
pygame.init()
pygame.mixer.init()

# Definir dimensiones de la pantalla
pantalla_width = 1000
pantalla_height = 600

# Crear ventana del juego
PANTALLA = pygame.display.set_mode((pantalla_width, pantalla_height))
pygame.display.set_caption('StarBattle')
FPS = 60
clock = pygame.time.Clock()


# Crear instancia del Form
form_prueba = FormPrueba(PANTALLA, 0, 0, 1000, 600, 'Gold', 'Cyan', 3, True)


# Bucle principal del juego
running = True
while running:
    lista_eventos = pygame.event.get()
    for event in lista_eventos:
        if event.type == pygame.QUIT: 
            running = False
            pygame.quit()
            sys.exit(0)
    PANTALLA.fill('Black')
    form_prueba.update(lista_eventos)
    
    pygame.display.flip()
    clock.tick(FPS)

# Salir de Pygame
pygame.quit()
