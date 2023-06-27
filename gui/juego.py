import pygame
import sys
from NivelUno import NivelUno
from NivelDos import NivelDos
from NivelTres import NivelTres
from GUI_forn_prueba import *
from animacion import *

# Inicializar Pygame
pygame.init()

# Definir dimensiones de la pantalla
pantalla_width = 1000
pantalla_height = 600

# Crear ventana del juego
PANTALLA = pygame.display.set_mode((pantalla_width, pantalla_height))
pygame.display.set_caption('StarBattle')
FPS = 60
clock = pygame.time.Clock()


# Crear instancia del NivelUno
# nivel_uno = NivelDos(PANTALLA)
form_prueba = FormPrueba(PANTALLA, 50, 100, 900, 350, 'Gold', 'Magenta', 5, True)


# Bucle principal del juego
while True:
    lista_eventos = pygame.event.get()
    for event in lista_eventos:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
            
    PANTALLA.fill('Black')
    form_prueba.update(lista_eventos)
    

    pygame.display.update()

# Salir de pygame
pygame.quit()

