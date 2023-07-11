import pygame
import sqlite3
import json
from pygame.locals import *

from gui.GUI_button import Button
from gui.GUI_slider import Slider
from gui.GUI_textbox import TextBox
from gui.GUI_label import Label
from gui.GUI_form import Form
from gui.GUI_button_image import Button_Image
from gui.GUI_form_menu_score import FormMenuScore
from gui.GUI_form_menu_play import formNiveles
from gui.GUI_picture_box import PictureBox
from gui.GUI_formsetting import formSettings

class FormPrueba(Form):
    def __init__(self, screen, x, y, w, h, color_background, color_border="Black", border_size=-1, active=True):
        super().__init__(screen, x, y, w, h, color_background, color_border, border_size, active)

        self.volumen = 0.2
        self.flag_play = True

        ######CONTROLES #####
        #self.txtbox = TextBox(self._slave, x, y, 300, 50, 300, 30, "Gray", "White", "Red", "Blue", 2,font="Comic Sans", font_size=15, font_color="Black")
        # self.btn_play = Button(self._slave, x, y, 100, 100, 100, 50, "Red", "Blue", self.btn_play_click, "Nombre",
        #                        "Pausa", font="Verdana", font_size=15, font_color="White")
        # self.label_volumen = Label(self._slave, 650, 190, 100, 50, "20%", "Comic Sans", 15, "White", "gui\Table.png")
        # self.slider_volumen = Slider(self._slave, x, y, 100, 200, 500, 15, self.volumen, "Blue", "White")
        self.btn_tabla = Button_Image(self._slave, x, y, 900, 50, 50, 50, "proyecto/gui\Menu_BTN.png", self.btn_tabla_click,
                                      "lala")
        self.btn_niveles = Button_Image(self._slave, x, y, 400, 300, 200, 200, "proyecto/fondos\imagenes\images.png", self.btn_imagen_click,
                                        "niveles")
        self.btn_settings = Button_Image(self._slave,x,y,100,50,50,50,"proyecto/fondos\imagenes\pngtree-icon-setting-game-png-image_6402361.png",self.btn_settings_click,
                                          "settings")
        self.picture_box = PictureBox(self._slave, 0, 0, 1000, 600, "proyecto/fondos\imagenes/fondo.png")
        ######

        # Agrego los controles a la lista
        self.lista_widgets.append(self.picture_box)
        #self.lista_widgets.append(self.txtbox)
        # self.lista_widgets.append(self.btn_play)
        # self.lista_widgets.append(self.label_volumen)
        # self.lista_widgets.append(self.slider_volumen)
        self.lista_widgets.append(self.btn_tabla)
        self.lista_widgets.append(self.btn_niveles)
        self.lista_widgets.append(self.btn_settings)


        pygame.mixer.music.load("proyecto/gui\Vengeance(Loopable).wav")
        
        pygame.mixer.music.set_volume(self.volumen)
        pygame.mixer.music.play(-1)
        self.render()

    def update(self, lista_eventos):
        if self.verificar_dialog_result():
            if self.active:
                self.draw()
                self.render()
                for widget in self.lista_widgets:
                    widget.update(lista_eventos)
                #self.update_volumen(lista_eventos)
        else:
            self.hijo.update(lista_eventos)

    def render(self):
        self._slave.fill(self._color_background)

    def btn_imagen_click(self, text):
        self.mostrar_imagen('proyecto/fondos\imagenes\mk1.png')
        formulario_niveles = formNiveles(self._master, 100, 25, 800, 550, "Black", "Black", True, "proyecto/gui\Window.png")
        self.show_dialog(formulario_niveles)

    def btn_settings_click(self,text):
        formulario_setting = formSettings(self._master,100,25,800,550,"Black","Black",True)
        self.show_dialog(formulario_setting)

    def btn_tabla_click(self, texto):
        dic_score = []

        try:
            with open("datos_partida_NivelUno.json", "r") as file:
                puntuacion = json.load(file)

            duracion_nivel_uno = puntuacion["duracion"]
            puntos_jugador_uno = puntuacion["puntos_jugador"]
            puntos_enemigo_uno = puntuacion["puntos_enemigo"]

            dic_score.append({"tiempo": duracion_nivel_uno, "Jugador": puntos_jugador_uno, "Enemigo": puntos_enemigo_uno})
        except FileNotFoundError:
            pass

        try:
            with open("datos_partida_NivelDos.json", "r") as file:
                puntuacion_dos = json.load(file)

            duracion_nivel_dos = puntuacion_dos["duracion"]
            puntos_jugador_dos = puntuacion_dos["puntos_jugador"]
            puntos_enemigo_dos = puntuacion_dos["puntos_enemigo"]

            dic_score.append({"tiempo": duracion_nivel_dos, "Jugador": puntos_jugador_dos, "Enemigo": puntos_enemigo_dos})
        except FileNotFoundError:
            pass

        try:
            with open("datos_partida_NivelTres.json", "r") as file:
                puntuacion_tres = json.load(file)

            duracion_nivel_tres = puntuacion_tres["duracion"]
            puntos_jugador_tres = puntuacion_tres["puntos_jugador"]
            puntos_enemigo_tres = puntuacion_tres["puntos_enemigo"]

            dic_score.append({"tiempo": duracion_nivel_tres, "Jugador": puntos_jugador_tres, "Enemigo": puntos_enemigo_tres})
        except FileNotFoundError:
            pass

        try:
            with open("datos_partida_NivelCuatro.json", "r") as file:
                puntuacion_cuatro = json.load(file)

            duracion_nivel_cuatro = puntuacion_cuatro["duracion"]
            puntos_jugador_cuatro = puntuacion_cuatro["puntos_jugador"]
            puntos_enemigo_cuatro = puntuacion_cuatro["puntos_enemigo"]

            dic_score.append({"tiempo": duracion_nivel_cuatro, "Jugador": puntos_jugador_cuatro, "Enemigo": puntos_enemigo_cuatro})
        except FileNotFoundError:
            pass

        form_puntaje = FormMenuScore(
            self._master,
            250,
            25,
            500,
            550,
            (220, 0, 220),
            "White",
            True,
            "PROYECTO\gui\Window.png",
            dic_score,
            100,
            10,
            10
        )

        self.show_dialog(form_puntaje)


    def mostrar_imagen(self, imagen):
        pantalla_completa = pygame.display.set_mode((self._master.get_width(), self._master.get_height()))
        imagen_cargada = pygame.image.load(imagen)
        imagen_redimensionada = pygame.transform.scale(imagen_cargada, (self._master.get_width(), self._master.get_height()))
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    running = False

            pantalla_completa.blit(imagen_redimensionada, (0, 0))
            pygame.display.flip()