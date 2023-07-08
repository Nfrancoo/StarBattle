import pygame
from class_nivel import Nivel
from plataforma import Plataforma
from personajeNU import Personaje
from enemigoNU import Enemigo
from animacion import *

class NivelUno(Nivel):
    def __init__(self, pantalla):
        self.enemigo_tipo = Enemigo
        tick = pygame.USEREVENT + 0 #evento propio
        pygame.time.set_timer(tick, 100)
        # Definir variables específicas del nivel uno
        last_count_update = pygame.time.get_ticks()
        score = [0, 0]  # Puntuaciones de los jugadores. [P1, P2]
        round_over = False
        ROUND_OVER_COOLDOWN = 2000
        FPS = 60
        clock = pygame.time.Clock()


        # Cargar musica
        pygame.mixer.music.load("audio\musica\music.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, 0.0, 5000)

        # Definir variables de imagen
        WARRIOR_TAMAÑO = 162
        WARRIOR_ESCALA = 4
        WARRIOR_DESPLAZAMIENTO = [72, 56]  # 12 para el lado derecho y 92 lado izquierdo
        WARRIOR_DATA = [WARRIOR_TAMAÑO, WARRIOR_ESCALA, WARRIOR_DESPLAZAMIENTO]
        ESPADACHIN_TAMAÑO = 200
        ESPADACHIN_ESCALA = 3
        ESPADACHIN_DESPLAZAMIENTO = [81, 116]
        ESPADACHIN_DATA = [ESPADACHIN_TAMAÑO, ESPADACHIN_ESCALA, ESPADACHIN_DESPLAZAMIENTO]

        # Cargar imagen de fondo
        img_fondo = pygame.image.load('fondos/imagenes/69.webp')
        background = 'SA'
        all_sprites = 'SA'

        # Definir fuente
        score_font = pygame.font.Font("fonts/turok.ttf", 30)

        # Cargar imagen de victoria
        imagen_victoria = pygame.image.load("fondos/imagenes/victory.png")
        imagen_gameover = pygame.image.load('fondos/imagenes/endgame.png')

        # Cargar spritesheets
        personaje_principal = pygame.image.load('sheets_personajes/warrior.png')
        enemigo_sheet = pygame.image.load('sheets_enemigo/espadachin.png')

        # Cargar sonidos golpes
        warrior_son = pygame.mixer.Sound("audio\efecto de sonido\sword.wav")
        warrior_son.set_volume(0.5)
        espadachin_son = pygame.mixer.Sound("audio\efecto de sonido\sword.wav")
        espadachin_son.set_volume(0.75)

        # Definir número de pasos en cada animación
        WARRIOR_ANIMACION_PASOS = [10, 8, 1, 7, 7, 3, 7]
        ESPADACHIN_ANIMACION_PASOS = [4, 8, 1, 3, 4, 3, 7]

        # Crear instancias de personaje y enemigo
        jugador = Personaje(200, 310, False, WARRIOR_DATA, personaje_principal, WARRIOR_ANIMACION_PASOS, espadachin_son )
        enemigo = Enemigo(700, 310, True, ESPADACHIN_DATA, enemigo_sheet, ESPADACHIN_ANIMACION_PASOS, espadachin_son)

        # Crear lista de plataformas
        lista_plataformas = [Plataforma(1, 280, 310, 10, (0, 0, 0, 0))]
        
        lista_donas = []

        dt = clock.tick(FPS) / 1000
        super().__init__(pantalla, jugador, enemigo, lista_plataformas, img_fondo, round_over, WARRIOR_DATA, personaje_principal,
                         WARRIOR_ANIMACION_PASOS, ESPADACHIN_DATA, enemigo_sheet, ESPADACHIN_ANIMACION_PASOS, 
                         lista_donas , tick, all_sprites, dt, clock, FPS, background, imagen_victoria, imagen_gameover, 'NivelUno')

