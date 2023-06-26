import pygame
import sys
from NivelUno import NivelUno
from personajeNU import Personaje
from enemigoNU import Enemigo

# Inicializar Pygame
pygame.init()

# Definir dimensiones de la pantalla
pantalla_width = 1000
pantalla_height = 600

# Crear ventana del juego
PANTALLA = pygame.display.set_mode((pantalla_width, pantalla_height))
pygame.display.set_caption('StarBattle')

# Crear instancia del NivelUno
nivel_uno = NivelUno(PANTALLA)


# Fuente para el texto
font = pygame.font.Font(None, 36)

# Bucle principal del juego
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    # Actualizar el nivel
    nivel_uno.actualizar()

    # Mover los personajes
    nivel_uno.jugador.movimiento(pantalla_width, pantalla_height, nivel_uno._slave, nivel_uno.enemigo, nivel_uno.round_over, nivel_uno.plataformas)
    nivel_uno.enemigo.movimiento(pantalla_width, pantalla_height, nivel_uno._slave, nivel_uno.jugador, nivel_uno.round_over, nivel_uno.plataformas)

    # Ataque del enemigo
    nivel_uno.ataque_enemigo()

    # Pintar el fondo
    nivel_uno.pintar_fondo()

    # Dibujar las plataformas
    nivel_uno.dibujar_plataformas()

    nivel_uno.escribir_texto("P1: " + str(nivel_uno.score[0]), nivel_uno.score_font, 'Red', 20, 60)
    nivel_uno.escribir_texto("P2: " + str(nivel_uno.score[1]), nivel_uno.score_font, 'Red', 580, 60)

    if nivel_uno.round_over == False:
        if nivel_uno.jugador.vivo == False:
            nivel_uno.score[1] += 1
            if nivel_uno.score[1] == 2:
                nivel_uno.round_over = True
            else:
                nivel_uno.round_over = True
                round_over_time = pygame.time.get_ticks()
        elif nivel_uno.enemigo.vivo == False:
            nivel_uno.score[0] += 1
            if nivel_uno.score[0] == 2:
                nivel_uno.round_over = True
            else:
                nivel_uno.round_over = True
                round_over_time = pygame.time.get_ticks()
    else:
        if nivel_uno.score[0] == 2 or nivel_uno.score[1] == 2:
            if nivel_uno.score[0] == 2:
                PANTALLA.blit(nivel_uno.imagen_victoria, (360, 150))
            else:
                PANTALLA.blit(nivel_uno.imagen_gameover, (115, 20))
        else:
            # Reiniciar el juego
            if pygame.time.get_ticks() - round_over_time > nivel_uno.ROUND_OVER_COOLDOWN:
                nivel_uno.round_over = False
                intro_count = 3
                nivel_uno.obtener_enemigo()
                nivel_uno.obtener_jugador()
    # Dibujar los personajes
    nivel_uno.dibujar_personajes()

    # Dibujar la barra de vida del jugador
    nivel_uno.pintar_vida_barra(nivel_uno.jugador.vida, 20, 20)

    # Dibujar la barra de vida del enemigo
    nivel_uno.pintar_vida_barra(nivel_uno.enemigo.vida, pantalla_width - 420, 20)

    # Actualizar la pantalla
    nivel_uno.actualizar_pantalla()

# Salir de pygame
pygame.quit()

