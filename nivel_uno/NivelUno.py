import pygame
from class_nivel import Nivel
from plataforma import Plataforma
from personajeNU import Personaje
from enemigoNU import Enemigo

class NivelUno(Nivel):
    def __init__(self, pantalla):
        # Definir variables específicas del nivel uno
        self.last_count_update = pygame.time.get_ticks()
        self.score = [0, 0]  # Puntuaciones de los jugadores. [P1, P2]
        self.round_over = False
        self.ROUND_OVER_COOLDOWN = 2000

        # Definir variables de imagen
        self.WARRIOR_TAMAÑO = 162
        self.WARRIOR_ESCALA = 4
        self.WARRIOR_DESPLAZAMIENTO = [72, 56]  # 12 para el lado derecho y 92 lado izquierdo
        self.WARRIOR_DATA = [self.WARRIOR_TAMAÑO, self.WARRIOR_ESCALA, self.WARRIOR_DESPLAZAMIENTO]
        self.ESPADACHIN_TAMAÑO = 200
        self.ESPADACHIN_ESCALA = 3
        self.ESPADACHIN_DESPLAZAMIENTO = [81, 116]
        self.ESPADACHIN_DATA = [self.ESPADACHIN_TAMAÑO, self.ESPADACHIN_ESCALA, self.ESPADACHIN_DESPLAZAMIENTO]

        # Cargar imagen de fondo
        self.img_fondo = pygame.image.load('fondos/imagenes/69.webp')

        # Definir fuente
        self.score_font = pygame.font.Font("fonts/turok.ttf", 30)

        # Cargar imagen de victoria
        self.imagen_victoria = pygame.image.load("fondos/imagenes/victory.png")
        self.imagen_gameover = pygame.image.load('fondos/imagenes/endgame.png')

        # Cargar spritesheets
        self.personaje_principal = pygame.image.load('sheets_personajes/warrior.png')
        self.enemigo = pygame.image.load('sheets_enemigo/espadachin.png')

        # Definir número de pasos en cada animación
        self.WARRIOR_ANIMACION_PASOS = [10, 8, 1, 7, 7, 3, 7]
        self.ESPADACHIN_ANIMACION_PASOS = [4, 8, 1, 3, 4, 3, 7]

        # Crear instancias de personaje y enemigo
        jugador = Personaje(1, 200, 310, False, self.WARRIOR_DATA, self.personaje_principal, self.WARRIOR_ANIMACION_PASOS)
        enemigo = Enemigo(2, 700, 310, True, self.ESPADACHIN_DATA, self.enemigo, self.ESPADACHIN_ANIMACION_PASOS)

        # Crear lista de plataformas
        lista_plataformas = [Plataforma(1, 280, 310, 10, (0, 0, 0, 0))]

        super().__init__(pantalla, jugador, enemigo, lista_plataformas, self.img_fondo, False)

    def actualizar_pantalla(self):
        pygame.display.update()

    def actualizar(self):
        super().actualizar()
        # Lógica de actualización específica del nivel uno

    def dibujar(self):
        super().dibujar_personajes()
        super().dibujar_plataformas()
        # Lógica de dibujado específica del nivel uno

    def reiniciar_juego(self):
        # Reiniciar variables y configuraciones del juego
        self.round_over = False
        self.score = [0, 0]
        self.round_over_time = pygame.time.get_ticks()

        # Reiniciar personaje y enemigo
        self.obtener_jugador()
        self.obtener_enemigo()

    def obtener_jugador(self):
        return self.jugador

    def obtener_enemigo(self):
        return self.enemigo


    def reiniciar_ronda(self):
        self.round_over = False

    def actualizar_pantalla(self):
        pygame.display.update()
