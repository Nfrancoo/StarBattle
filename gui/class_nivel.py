from plataforma import Plataforma
from personajeNU import Personaje
from enemigoNU import Enemigo
from Donas import *
from animacion import *
import pygame

class Nivel:
    def __init__(self, pantalla, personaje_principal, enemigo, lista_plataformas, img_fondo, round_over,  jugador_data,
                 jugador_sheet, jugador_animacion_pasos, enemigo_data, enemigo_sheet, enemigo_animacion_pasos,
                 lista_donas, tick, all_sprites, dt, clock, FPS, background):
        self._slave = pantalla
        self.jugador = personaje_principal
        self.enemigo = enemigo
        self.plataformas = lista_plataformas
        self.img_fondo = img_fondo
        self.round_over = False
        self.score = score = [0, 0]
        self.score_font = pygame.font.Font("fonts/turok.ttf", 30)
        self.pantalla_width = 1000
        self.pantalla_height = 600
        self.imagen_victoria = pygame.image.load("fondos/imagenes/victory.png")
        self.imagen_gameover = pygame.image.load('fondos/imagenes/endgame.png')
        self.ROUND_OVER_COOLDOWN = 2000
        self.jugador_data = jugador_data
        self.jugador_sheet = jugador_sheet
        self.jugador_animacion_pasos = jugador_animacion_pasos
        self.enemigo_data = enemigo_data
        self.enemigo_sheet = enemigo_sheet
        self.enemigo_animacion_pasos = enemigo_animacion_pasos
        self.round_over_time = 0  # Asignar un valor inicial a round_over_time
        self.lista_donas = lista_donas
        self.tick = tick
        self.all_sprites = all_sprites
        self.dt = dt
        self.clock = clock
        self.FPS = FPS
        self.background = background

    def update(self, lista_eventos):
        # Dibujar fondo

        if isinstance(self.all_sprites, pygame.sprite.Group):
            self.dt = self.clock.tick(self.FPS) / 1000
            self.all_sprites.update(self.dt)
            self.pintar_fondo_2()
        else:
            self.pintar_fondo()

        # Mostrar estadísticas de los jugadores
        self.pintar_vida_barra(self.jugador.vida, 20, 20)
        self.pintar_vida_barra(self.enemigo.vida, 580, 20)
        self.escribir_texto("P1: " + str(self.score[0]), self.score_font, 'Red', 20, 60)
        self.escribir_texto("P2: " + str(self.score[1]), self.score_font, 'Red', 580, 60)

        # Actualizar cuenta regresiva
        
            # Mover personajes
        self.jugador.movimiento(self.pantalla_width, self.pantalla_height, self._slave, self.enemigo, self.round_over, self.plataformas)
        self.enemigo.movimiento(self.pantalla_width, self.pantalla_height, self._slave, self.jugador, self.round_over, self.plataformas)


        # Actualizar personajes
        self.jugador.update()
        self.enemigo.update()

        # Dibujar personajes
        self.jugador.draw(self._slave)
        self.enemigo.draw(self._slave)

        # Verificar derrota de los jugadores
        # Verificar derrota de los jugadores
        if self.round_over == False:
            if self.jugador.vivo == False:
                self.score[1] += 1
                if self.score[1] == 2:
                    self.round_over = True
                else:
                    self.round_over = True
                    self.round_over_time = pygame.time.get_ticks()
            elif self.enemigo.vivo == False:
                self.score[0] += 1
                if self.score[0] == 2:
                    self.round_over = True
                else:
                    self.round_over = True
                    self.round_over_time = pygame.time.get_ticks()
        else:
            if self.score[0] == 2 or self.score[1] == 2:
                if self.score[0] == 2:
                    self._slave.blit(self.imagen_victoria, (360, 150))
                else:
                    self._slave.blit(self.imagen_gameover, (115, 20))
            else:
                # Reiniciar el juego
                if pygame.time.get_ticks() - self.round_over_time > self.ROUND_OVER_COOLDOWN:
                    self.round_over = False
                    intro_count = 3
                    self.jugador = Personaje(1, 200, 310, False, self.jugador_data, self.jugador_sheet, self.jugador_animacion_pasos)
                    self.enemigo = Enemigo(2, 700, 310, True, self.enemigo_data, self.enemigo_sheet, self.enemigo_animacion_pasos)

        for dona in self.lista_donas:
            self._slave.blit(dona['superficie'], dona['rectangulo'])
        for evento in lista_eventos:
            if evento.type == pygame.USEREVENT:
                if evento.type == self.tick:
                    update(self.lista_donas)
        for dona in self.lista_donas:
                    self._slave.blit(dona['superficie'], dona['rectangulo'])

        for dona in self.lista_donas:
            if dona['rectangulo'].colliderect(self.jugador.rect):
                self.jugador.vida -= 5
                actualizar_pantalla(self.lista_donas, self.jugador, self._slave)
            elif dona['rectangulo'].colliderect(self.enemigo.rect):
                if self.enemigo.vida < 100:  # Permitir que la vida alcance 100
                    self.enemigo.vida += 5
                actualizar_pantalla(self.lista_donas, self.enemigo, self._slave)

            


        # Debug: Dibujar rango de ataque del enemigo
        # self.pintar_rango_ataque(self.enemigo)
        # self.pintar_rango_ataque(self.jugador)
        # self.pintar_rectangulo(self.jugador)
        # self.pintar_rectangulo(self.enemigo)

        if self.enemigo.rango_ataque.colliderect(self.jugador.rect) and self.enemigo.vivo:
            self.enemigo.ataque(self.jugador)

        for plataforma in self.plataformas:
            plataforma.pintar(self._slave)

    def pintar_fondo(self):
        fondo_escalado = pygame.transform.scale(self.img_fondo, (self.pantalla_width, self.pantalla_height))
        self._slave.blit(fondo_escalado, (0, 0))

    def pintar_fondo_2(self):
        fondo_escalado = pygame.transform.scale(self.background.image, (self.pantalla_width, self.pantalla_height))
        self._slave.blit(fondo_escalado, (0, 0))

    def pintar_vida_barra(self, vida, x, y):
        ratio = vida / 100
        pygame.draw.rect(self._slave, 'White', (x - 2, y - 2, 404, 34))
        pygame.draw.rect(self._slave, 'Red', (x, y, 400, 30))
        pygame.draw.rect(self._slave, 'Yellow', (x, y, 400 * ratio, 30))

    def pintar_rectangulo(self, personaje):
        pygame.draw.rect(self._slave, 'Red', personaje.rect, 2)

    def escribir_texto(self, text, font, color, x, y):
        img = font.render(text, True, color)
        self._slave.blit(img, (x, y))

    def pintar_rango_ataque(self, personaje):
        pygame.draw.rect(self._slave, (0, 255, 0), personaje.rango_ataque, 2)
