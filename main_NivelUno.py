import pygame
import sys
from nivel_uno.personajeNU import Personaje
from nivel_uno.enemigoNU import Enemigo
from nivel_uno.plataforma import Plataforma
from main import Nivel

class NivelUno(Nivel):
    def __init__(self, pantalla: pygame.Surface):

        pantalla_width = pantalla.get_width
        pantalla_height = pantalla.get_height

        # Definir variables del juego
        last_count_update = pygame.time.get_ticks()
        score = [0, 0]  # Puntuaciones de los jugadores. [P1, P2]
        round_over = False
        ROUND_OVER_COOLDOWN = 2000

        # Definir variables de imagen
        WARRIOR_TAMAÑO = 162
        WARRIOR_ESCALA = 4
        WARRIOR_DESPLAZAMIENTO = [72, 56] #12 para el lado derecho y 92 lado izquierdo
        WARRIOR_DATA = [WARRIOR_TAMAÑO, WARRIOR_ESCALA, WARRIOR_DESPLAZAMIENTO]
        ESPADACHIN_TAMAÑO = 200
        ESPADACHIN_ESCALA = 3
        ESPADACHIN_DESPLAZAMIENTO = [81, 116]
        ESPADACHIN_DATA = [ESPADACHIN_TAMAÑO, ESPADACHIN_ESCALA, ESPADACHIN_DESPLAZAMIENTO]


        # Cargar imagen de fondo
        img_fondo = pygame.image.load('fondos/imagenes/69.webp')

        # Cargar spritesheets
        personaje_principal = pygame.image.load('sheets_personajes/warrior.png')
        enemigo = pygame.image.load('sheets_enemigo/espadachin.png')

        # Cargar imagen de victoria
        imagen_victoria = pygame.image.load("fondos/imagenes/victory.png")
        imagen_gameover = pygame.image.load('fondos/imagenes/endgame.png')

        # Definir número de pasos en cada animación
        WARRIOR_ANIMACION_PASOS = [10, 8, 1, 7, 7, 3, 7]
        ESPADACHIN_ANIMACION_PASOS = [4, 8, 1, 3, 4, 3, 7]

        # Definir fuente
        score_font = pygame.font.Font("fonts/turok.ttf", 30)

        # Crear dos instancias de personaje
        personaje_1 = Personaje(1, 200, 310, False, WARRIOR_DATA, personaje_principal, WARRIOR_ANIMACION_PASOS,)
        personaje_2 = Enemigo(2, 700, 310, True, ESPADACHIN_DATA, enemigo, ESPADACHIN_ANIMACION_PASOS,)

        lista_plataformas = [Plataforma(1, 280, 310, 10, (0, 0, 0, 0))]

        super().__init__(pantalla, personaje_principal, enemigo, lista_plataformas, img_fondo, round_over)
