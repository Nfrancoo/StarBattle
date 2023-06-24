import pygame
import sys
from pygame import mixer
from personaje_2 import Personaje
from enemigo_2 import Enemigo
from plataforma import Plataforma

# ...

class Nivel:
    def __init__(self, pantalla, personaje_data, personaje_sheet, enemigo_data, enemigo_sheet, other_variables):
        self.pantalla = pantalla
        self.personaje_1 = Personaje(1, 200, 310, False, warrior_data, warrior_sheet, WARRIOR_ANIMACION_PASOS, sword_fx)
        self.personaje_2 = Enemigo(2, 700, 310, True, espadachin_data, espadachin_sheet, ESPADACHIN_ANIMACION_PASOS, magic_fx)
        self.plataformas = []

        # Crea las plataformas del nivel
        # ...

    def actualizar(self):
        # Actualiza el estado de los elementos del nivel
        self.personaje_1.movimiento(pantalla_width, pantalla_height, self.pantalla, self.personaje_2, round_over, self.plataformas)
        self.personaje_2.movimiento(pantalla_width, pantalla_height, self.pantalla, self.personaje_1, round_over, self.plataformas)
        self.personaje_1.update()
        self.personaje_2.update()

    def dibujar(self):
        # Dibuja los elementos del nivel en la pantalla
        pintar_fondo()
        pintar_vida_barra(self.personaje_1.vida, 20, 20)
        pintar_vida_barra(self.personaje_2.vida, 580, 20)
        draw_text("P1: " + str(score[0]), score_font, 'Red', 20, 60)
        draw_text("P2: " + str(score[1]), score_font, 'Red', 580, 60)
        self.personaje_1.draw(self.pantalla)
        self.personaje_2.draw(self.pantalla)
        pintar_rango_ataque(self.personaje_2)
        pintar_rango_ataque(self.personaje_1)
        pintar_rectangulo(self.personaje_1)
        pintar_rectangulo(self.personaje_2)
        for plataforma in self.plataformas:
            plataforma.pintar(self.pantalla)