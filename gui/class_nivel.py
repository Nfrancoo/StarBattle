from plataforma import Plataforma
from personajeNU import Personaje
from Boss import Boss
from enemigoNU import Enemigo
from Donas import *
from animacion import *
import pygame
import json
import os
import sys
from GUI_formsetting import formSettings

class Nivel:
    def __init__(self, pantalla, personaje_principal, enemigo, lista_plataformas, img_fondo, round_over, jugador_data,
                 jugador_sheet, jugador_animacion_pasos, enemigo_data, enemigo_sheet, enemigo_animacion_pasos,
                 lista_donas, tick, all_sprites, dt, clock, FPS, background, imagen_victoria, imagen_gameover, nivel, sonido_per, sonido_ene):
        self._slave = pantalla
        self.jugador = personaje_principal
        self.enemigo = enemigo
        self.plataformas = lista_plataformas
        self.img_fondo = img_fondo
        self.round_over = False
        self.score = [0, 0]
        self.score_font = pygame.font.Font("fonts/turok.ttf", 30)
        self.pantalla_width = 1000
        self.pantalla_height = 600
        self.imagen_victoria = imagen_victoria
        self.imagen_gameover = imagen_gameover
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
        self.tiempo_transcurrido = 0
        self.nivel = nivel
        self.enemigo_2 = enemigo
        self.paused = False
        self.running = True
        self.personaje_sonido_ataque = sonido_per
        self.enemigo_sonido_ataque = sonido_ene
        self.timer_active = True


    def update(self, lista_eventos):
        
        if self.paused or not self.timer_active:  # Detener el temporizador si está en pausa o timer_active es False
            return
        # Calcular el tiempo transcurrido al inicio del método
        time = self.clock.tick(self.FPS) / 1000

        # Dibujar fondo
        if isinstance(self.all_sprites, pygame.sprite.Group):
            self.all_sprites.update(time)
            self.pintar_fondo_2()
        else:
            self.pintar_fondo()

        # Mostrar estadísticas de los jugadores
        if not self.round_over:
            self.tiempo_transcurrido += time

        self.pintar_vida_barra(self.jugador.vida, 20, 20)
        self.pintar_vida_barra(self.enemigo.vida, 580, 20)
        self.escribir_texto("P1: " + str(self.score[0]), self.score_font, 'Red', 20, 60)
        self.escribir_texto("P2: " + str(self.score[1]), self.score_font, 'Red', 580, 60)
        minutos = int(self.tiempo_transcurrido // 60)
        segundos = int(self.tiempo_transcurrido % 60)

        tiempo_formateado = f"{minutos}:{segundos:02}"  # Formatear cadena de tiempo

        self.escribir_texto(tiempo_formateado, self.score_font, 'White', 480, 20)

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
                    self._slave.blit(self.imagen_victoria, (295, 110))
                    duracion_partida = int(self.tiempo_transcurrido)
                    puntos_jugador = self.score[0]
                    puntos_enemigo = self.score[1]
                    self.guardar_datos_partida(duracion_partida, puntos_jugador, puntos_enemigo)
                else:
                    self._slave.blit(self.imagen_gameover, (115, 20))
            else:
                # Reiniciar el juego
                if pygame.time.get_ticks() - self.round_over_time > self.ROUND_OVER_COOLDOWN:
                    self.round_over = False
                    intro_count = 3
                    self.jugador = Personaje(200, 310, False, self.jugador_data, self.jugador_sheet, self.jugador_animacion_pasos, self.personaje_sonido_ataque)
        
                    if isinstance(self.enemigo, self.enemigo_tipo):  # Comprueba si el enemigo es del tipo original
                        self.enemigo = self.enemigo_tipo(700, 310, True, self.enemigo_data, self.enemigo_sheet, self.enemigo_animacion_pasos, self.enemigo_sonido_ataque)
                        
                    else:
                        self.enemigo = self.enemigo_tipo(700, 310, True, self.enemigo_data, self.enemigo_sheet, self.enemigo_animacion_pasos, self.enemigo_sonido_ataque)
                        
            
        
        
        for dona in self.lista_donas:
            self._slave.blit(dona['superficie'], dona['rectangulo'])

        for evento in lista_eventos:
            if evento.type == pygame.USEREVENT:
                if evento.type == self.tick:
                    update(self.lista_donas)
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.pause()

                    


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

    def guardar_datos_partida(self, duracion, puntos_jugador, puntos_enemigo):
        nombre_archivo = f'datos_partida_{self.nivel}.json'    
        datos = {
            'duracion': duracion,
            'puntos_jugador': puntos_jugador,
            'puntos_enemigo': puntos_enemigo
        }
        
        try:
            with open(nombre_archivo, 'w') as file:
                json.dump(datos, file, indent=4)
        except PermissionError:
            print('Completado todos los niveles, felicidades')

    # Función para pausar el juego
    def pause(self):
        self.paused = True
        while self.paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.paused = False
                    self.running = False
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.paused = False
