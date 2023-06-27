import pygame
from class_nivel import Nivel
from plataforma import Plataforma
from personajeNU import Personaje
from enemigoNU import Enemigo
from Donas import *

class NivelDos(Nivel):
    def __init__(self, pantalla):
        tick = pygame.USEREVENT + 0 #evento propio
        pygame.time.set_timer(tick, 100)

        # Definir variables del juego
        last_count_update = pygame.time.get_ticks()
        score = [0, 0]  # Puntuaciones de los jugadores. [P1, P2]
        round_over = False
        ROUND_OVER_COOLDOWN = 2000
        FPS = 60
        clock = pygame.time.Clock()

        # Definir variables de imagen
        PERSONAJE_TAMAÑO = 155
        PERSONAJE_ESCALA = 2
        PERSONAJE_DESPLAZAMIENTO = [60, 51] #12 para el lado derecho y 92 lado izquierdo
        PERSONAJE_DATA = [PERSONAJE_TAMAÑO, PERSONAJE_ESCALA, PERSONAJE_DESPLAZAMIENTO]
        ENEMIGO_TAMAÑO = 250
        ENEMIGO_ESCALA = 3
        ENEMIGO_DESPLAZAMIENTO = [111, 100]
        ENEMIGO_DATA = [ENEMIGO_TAMAÑO, ENEMIGO_ESCALA, ENEMIGO_DESPLAZAMIENTO]


        # Cargar imagen de fondo
        img_fondo = pygame.image.load('fondos/imagenes/fondo(2).jpg')
        background = 'SA'
        all_sprites = 'SA'

        # Cargar spritesheets
        personaje_sheet = pygame.image.load('sheets_personajes/elRey.png')
        enemigo_sheet = pygame.image.load('sheets_enemigo/wizard.png')

        # Cargar imagen de victoria
        imagen_victoria = pygame.image.load("fondos/imagenes/victory.png")
        imagen_gameover = pygame.image.load('fondos/imagenes/endgame.png')

        # Definir número de pasos en cada animación
        PERSONAJE_ANIMACION_PASOS = [6, 8, 2, 6, 6, 4, 10]
        ENEMIGO_ANIMACION_PASOS = [8, 8, 1, 8, 8, 3, 7]

        # Definir fuente
        score_font = pygame.font.Font("fonts/turok.ttf", 30)

        # Crear dos instancias de personaje
        jugador = Personaje(200, 280, False, PERSONAJE_DATA, personaje_sheet, PERSONAJE_ANIMACION_PASOS,)
        enemigo = Enemigo(700, 310, True, ENEMIGO_DATA, enemigo_sheet, ENEMIGO_ANIMACION_PASOS,)

        lista_plataformas = []#Plataforma(1, 280, 330, 10, (0, 0, 0, 0))]

        lista_donas = crear_lista_donas(5)

        dt = clock.tick(FPS) / 1000
        super().__init__(pantalla, jugador, enemigo, lista_plataformas, img_fondo, round_over, PERSONAJE_DATA, personaje_sheet,
                        PERSONAJE_ANIMACION_PASOS, ENEMIGO_DATA, enemigo_sheet, ENEMIGO_ANIMACION_PASOS, lista_donas,
                        tick, all_sprites, dt, clock, FPS, background)

