import pygame
import sqlite3
import json
from pygame.locals import *

from gui.GUI_form import *
from gui.GUI_button_image import *
from gui.GUI_label import *
from gui.GUI_slider import *
from gui.GUI_picture_box import *
from gui.GUI_formsetting import formSettings
from gui.GUI_form_menu_score import FormMenuScore




current_volume = 0.2

class FormPausa(Form):
    def __init__(self, screen, x, y, w, h, color_background, color_border, active, contenedor_nivel=None):
        super().__init__(screen, x, y, w, h, color_background, color_border, active)
        self.contenedor_nivel = contenedor_nivel
        self.volumen = current_volume  # Utiliza el volumen actual almacenado
        self.flag_play = True
        self.nivel = False
       
        self.fondo = PictureBox(self._slave, 0,0,1000,600,"proyecto/fondos\imagenes\pausa.png")
        self.btn_home = Button_Image(screen=self._slave,
                                      master_x=self._x,
                                      master_y=self._y,
                                      x= 370,
                                      y=350,
                                      w=250,
                                      h=100,
                                      path_image="proyecto/fondos\imagenes/resume.png",
                                      onclick=self.btn_home_click,
                                      onclick_param="",
                                      text="",
                                      font="Arial",
                                      )
        
        self._btn_settings = Button_Image(screen=self._slave,
                                 master_x= self._x,
                                 master_y= self._y,
                                 x=300,
                                 y=250,
                                 w=60,
                                 h=60,
                                 path_image="proyecto/fondos\imagenes\setting_logo.png",
                                 onclick=self.btn_settings_click,
                                 onclick_param="settings")

        self._btn_tabla = Button_Image(screen=self._slave,
                                 master_x= self._x,
                                 master_y= self._y,
                                 x=600,
                                 y=250,
                                 w=60,
                                 h=60,
                                 path_image="PROYECTO/fondos\imagenes\menu.png",
                                 onclick=self.btn_tabla_click,
                                 onclick_param="lala")

        self.lista_widgets.append(self.fondo)      
        self.lista_widgets.append(self.btn_home)           
        self.lista_widgets.append(self._btn_settings)
        self.lista_widgets.append(self._btn_tabla)

            
    def update(self,lista_eventos):
        if self.verificar_dialog_result():
            if self.active:
                self.draw()
                self.render()
                for widget in self.lista_widgets:
                    widget.update(lista_eventos)
        else:
            self.hijo.update(lista_eventos)

    def render(self):
        self._slave.fill(self._color_background)
    
    def btn_home_click(self,param):
        if self.contenedor_nivel != None:
            self.contenedor_nivel.setting = False  # Establecer self.setting en False
            self.end_dialog()
        self.end_dialog()

    def btn_settings_click(self,text):
        formulario_setting = formSettings(self._master,100,25,800,550,"Black","Black",True)
        self.setting = True 
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

        # Crear una conexión a la base de datos
        conn = sqlite3.connect('datos_partida.db')

        # Crear un cursor para ejecutar consultas SQL
        cursor = conn.cursor()

        # Crear la tabla
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS datos_partida (
                tiempo TEXT,
                jugador INTEGER,
                enemigo INTEGER
            )
        ''')

        # Eliminar los datos anteriores de la tabla
        cursor.execute('''
            DELETE FROM datos_partida
        ''')

        # Insertar los nuevos datos en la tabla
        for score in dic_score:
            cursor.execute('''
                INSERT INTO datos_partida (tiempo, jugador, enemigo)
                VALUES (?, ?, ?)
            ''', (score["tiempo"], score["Jugador"], score["Enemigo"]))

        # Guardar los cambios y cerrar la conexión
        conn.commit()
        conn.close()