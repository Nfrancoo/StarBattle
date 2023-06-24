import sys
import pygame
from nivel import Nivel
from plataforma import Plataforma
from personaje_2 import Personaje
from enemigo_2 import Enemigo

class NivelUno(Nivel):
    def __init__(self, pantalla: pygame.Surface):
        super().__init__(pantalla)
        # Crear ventana del juego
        pantalla_width = pantalla.get_width()
        pantalla_height = pantalla.get_height()

        # Definir variables del juego
        self.intro_count = 3
        self.last_count_update = pygame.time.get_ticks()
        self.score = [0, 0]  # Puntuaciones de los jugadores. [P1, P2]
        self.round_over = False
        self.ROUND_OVER_COOLDOWN = 2000

        # Cargar música y sonidos
        pygame.mixer.music.load("audio/music.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, 0.0, 5000)
        sword_fx = pygame.mixer.Sound("audio/sword.wav")
        sword_fx.set_volume(0.5)
        magic_fx = pygame.mixer.Sound("audio/magic.wav")
        magic_fx.set_volume(0.75)

        # Cargar imagen de fondo
        fondo = pygame.image.load('imagenes/69.webp')
        self.fondo = pygame.transform.scale(fondo, (pantalla_width,pantalla_height))

        # Cargar spritesheets
        warrior_sheet = pygame.image.load('warrior/Sprites/warrior.png')
        wizard_sheet = pygame.image.load('wizard/Sprites/espadachin.png')

        # Cargar imagen de victoria
        self.victory_img = pygame.image.load("imagenes/victory.png")

        # Definir número de pasos en cada animación
        WARRIOR_ANIMACION_PASOS = [10, 8, 1, 7, 7, 3, 7]
        ESPADACHIN_ANIMACION_PASOS = [4, 8, 1, 3, 4, 3, 7]

        # Definir fuente
        self.count_font = pygame.font.Font("fonts/turok.ttf", 80)
        self.score_font = pygame.font.Font("fonts/turok.ttf", 30)

        # Crear dos instancias de personaje
        self.personaje_1 = Personaje(1, 200, 310, False, [162, 4, [72, 56]], warrior_sheet, WARRIOR_ANIMACION_PASOS, sword_fx)
        self.personaje_2 = Enemigo(2, 700, 310, True, [200, 3, [81, 116]], wizard_sheet, ESPADACHIN_ANIMACION_PASOS, magic_fx)

        self.lista_plataformas = []

    def bucle_principal(self, warrior_sheet, wizard_sheet, sword_fx, magic_fx):
        while True:
            # WARRIOR_ANIMACION_PASOS = [10, 8, 1, 7, 7, 3, 7]
            # ESPADACHIN_ANIMACION_PASOS = [4, 8, 1, 3, 4, 3, 7]

            self.reloj.tick(self.FPS)

            # Dibujar fondo
            self.pantalla.blit(self.fondo, (0, 0))

            # Pintar las plataformas
            for plataforma in self.lista_plataformas:
                plataforma.pintar(self.pantalla)

            # Mostrar estadísticas de los jugadores
            self.draw_text("P1: " + str(self.score[0]), self.score_font, 'Red', 20, 60)
            self.draw_text("P2: " + str(self.score[1]), self.score_font, 'Red', 580, 60)

            # Actualizar cuenta regresiva
            if self.intro_count <= 0:
                # Mover personajes
                self.personaje_1.movimiento(self.pantalla.get_width(), self.pantalla.get_height(), self.pantalla, self.personaje_2, self.round_over, self.lista_plataformas)
                self.personaje_2.movimiento(self.pantalla.get_width(), self.pantalla.get_height(), self.pantalla, self.personaje_1, self.round_over, self.lista_plataformas)
            else:
                # Mostrar temporizador de cuenta regresiva
                self.draw_text(str(self.intro_count), self.count_font, 'Red', self.pantalla.get_width() / 2, self.pantalla.get_height() / 3)
                # Actualizar temporizador de cuenta regresiva
                if pygame.time.get_ticks() - self.last_count_update >= 1000:
                    self.intro_count -= 1
                    self.last_count_update = pygame.time.get_ticks()

            # Actualizar personajes
            self.personaje_1.update()
            self.personaje_2.update()

            # Dibujar personajes
            self.personaje_1.draw(self.pantalla)
            self.personaje_2.draw(self.pantalla)

            # Verificar derrota de los jugadores
            if not self.round_over:
                if not self.personaje_1.vivo:
                    self.score[1] += 1
                    self.round_over = True
                    self.round_over_time = pygame.time.get_ticks()
                elif not self.personaje_2.vivo:
                    self.score[0] += 1
                    self.round_over = True
                    self.round_over_time = pygame.time.get_ticks()
            else:
                # Mostrar imagen de victoria
                self.pantalla.blit(self.victory_img, (360, 150))
                if pygame.time.get_ticks() - self.round_over_time > self.ROUND_OVER_COOLDOWN:
                    self.round_over = False
                    self.intro_count = 3
                    self.personaje_1 = Personaje(1, 200, 310, False, [162, 4, [72, 56]], warrior_sheet, self.WARRIOR_ANIMACION_PASOS, sword_fx)
                    self.personaje_2 = Enemigo(2, 700, 310, True, [200, 3, [81, 116]], wizard_sheet, self.ESPADACHIN_ANIMACION_PASOS, magic_fx)

            # Debug: Dibujar rango de ataque del enemigo
            Nivel.pintar_rango_ataque(self.personaje_2)
            Nivel.pintar_rango_ataque(self.personaje_1)
            Nivel.pintar_rectangulo(self.personaje_1)
            Nivel.pintar_rectangulo(self.personaje_2)

            if self.personaje_1.rect.colliderect(self.personaje_2.rango_ataque) and self.personaje_2.vivo:
                self.personaje_2.ataque(self.personaje_1, self.pantalla)
              
            # Manejador de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                    
            # Actualizar pantalla
            pygame.display.update()