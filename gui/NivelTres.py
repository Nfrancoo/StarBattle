import pygame
from class_nivel import Nivel
from plataforma import Plataforma
from personajeNU import Personaje
from enemigoNU import Enemigo
from animacion import *

class NivelTres(Nivel):
    def __init__(self, pantalla):
        self.enemigo_tipo = Enemigo
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
        WARRIOR_TAMAÑO = 162
        WARRIOR_ESCALA = 4
        WARRIOR_DESPLAZAMIENTO = [72, 46] #12 para el lado derecho y 92 lado izquierdo
        WARRIOR_DATA = [WARRIOR_TAMAÑO, WARRIOR_ESCALA, WARRIOR_DESPLAZAMIENTO]
        ENEMIGO_TAMAÑO = 155
        ENEMIGO_ESCALA = 2
        ENEMIGO_DESPLAZAMIENTO = [60, 41] #12 para el lado derecho y 92 lado izquierdo
        ENEMIGO_DATA = [ENEMIGO_TAMAÑO,ENEMIGO_ESCALA, ENEMIGO_DESPLAZAMIENTO]


        # Cargar imagen de victoria
        imagen_victoria = pygame.image.load("fondos/imagenes/victory_blanco.png")
        imagen_gameover = pygame.image.load('fondos/imagenes/endgame_blanco.png')

        img_fondo = load_images('fondos/lista_background')
        background = AnimatedBackground((0, 0), img_fondo, 0.1)
        all_sprites = pygame.sprite.Group(background)

        # Definir fuente
        score_font = pygame.font.Font("fonts/turok.ttf", 30)

        # Cargar spritesheets
        personaje_principal = pygame.image.load('sheets_personajes/warrior.png')
        enemigo_sheet = pygame.image.load('sheets_personajes/elRey.png')

        # Definir número de pasos en cada animación
        WARRIOR_ANIMACION_PASOS = [10, 8, 1, 7, 7, 3, 7]
        ENEMIGO_ANIMACION_PASOS = [6, 8, 2, 6, 6, 4, 10]


        # Crear instancias de personaje y enemigo
        jugador = Personaje(200, 310, False, WARRIOR_DATA, personaje_principal, WARRIOR_ANIMACION_PASOS)
        enemigo = Enemigo(700, 310, True, ENEMIGO_DATA, enemigo_sheet, ENEMIGO_ANIMACION_PASOS)

        # Crear lista de plataformas
        lista_plataformas = []
        
        lista_donas = []

        dt = clock.tick(FPS) / 1000

        super().__init__(pantalla, jugador, enemigo, lista_plataformas, img_fondo, round_over, WARRIOR_DATA, personaje_principal,
                        WARRIOR_ANIMACION_PASOS, ENEMIGO_DATA, enemigo_sheet, ENEMIGO_ANIMACION_PASOS, lista_donas ,
                        tick, all_sprites,dt, clock, FPS, background, imagen_victoria, imagen_gameover, 'NivelTres')

