import pygame
from pygame.locals import *
import os
import json

from GUI_form import *
from GUI_form_contenedor_nivel import ContenedorNivel
from GUI_button_image import *
from manejador_niveles import ManejadorNiveles

class formNiveles(Form):
    def __init__(self, screen, x, y, w, h, color_background, color_border, active, path_image):
        super().__init__(screen, x, y, w, h, color_background, color_border, active)
        self.manejador_niveles = ManejadorNiveles(self._master)
        aux_image = pygame.image.load(path_image)
        aux_image = pygame.transform.scale(aux_image, (w, h))
        self._slave = aux_image
        # Banderas para verificar si los niveles están desbloqueados o completados
        self.nivel_uno_desbloqueado = True  # Siempre desbloqueado
        self.nivel_dos_desbloqueado = False
        self.nivel_tres_desbloqueado = False
        self.nivel_cuatro_desbloqueado = False
        self.nivel_uno_completado = os.path.exists("datos_partida_NivelUno.json")
        self.nivel_dos_completado = os.path.exists("datos_partida_NivelDos.json")
        self.nivel_tres_completado = os.path.exists("datos_partida_NivelTres.json")
        self.nivel_cuatro_completado = os.path.exists("datos_partida_NivelCuatro.json")

        # Agregar lógica para desbloquear el NivelDos si el NivelUno está completado
        if self.nivel_uno_completado:
            self.nivel_dos_desbloqueado = True
        if self.nivel_dos_completado:
            self.nivel_tres_desbloqueado = True
        if self.nivel_tres_completado:
            self.nivel_cuatro_desbloqueado = True

        self.niveles_imagenes = {
            "nivel_uno": "fondos\imagenes\primerpelea.png",
            "nivel_dos": "fondos\imagenes\peleados.png",
            "nivel_tres": "fondos\imagenes/tercerpelea.png",
            "nivel_cuatro": "fondos\imagenes\cuartonivel.png"
        }

        self.btn_nivel_uno = Button_Image(screen=self._slave,
                                          master_x=x,
                                          master_y=y,
                                          x=200,
                                          y=120,
                                          w=100,
                                          h=100,
                                          path_image="fondos\imagenes/nivel_uno.png",
                                          onclick=self.entrar_nivel,
                                          onclick_param="nivel_uno",
                                          text="",
                                          font="Arial")

        self.btn_nivel_dos = Button_Image(screen=self._slave,
                                          master_x=x,
                                          master_y=y,
                                          x=300,
                                          y=120,
                                          w=100,
                                          h=100,
                                          path_image="fondos\imagenes/nivel_dos.png",
                                          onclick=self.entrar_nivel,
                                          onclick_param="nivel_dos",
                                          text="",
                                          font="Arial")

        self.btn_nivel_tres = Button_Image(screen=self._slave,
                                          master_x=x,
                                          master_y=y,
                                          x=400,
                                          y=120,
                                          w=100,
                                          h=100,
                                          color_background=(255, 0, 0),
                                          color_border=(255, 0, 255),
                                          path_image="fondos\imagenes/nivel_tres.png",
                                          onclick=self.entrar_nivel,
                                          onclick_param="nivel_tres",
                                          text="",
                                          font="Arial",
                                          font_size=15,
                                          font_color=(0, 255, 0))

        self.btn_nivel_cuatro = Button_Image(screen=self._slave,
                                             master_x=x,
                                             master_y=y,
                                             x=500,
                                             y=120,
                                             w=100,
                                             h=100,
                                             color_background=(255, 0, 0),
                                             color_border=(255, 0, 255),
                                             path_image="fondos\imagenes/nivel_cuatro.png",
                                             onclick=self.entrar_nivel,
                                             onclick_param="nivel_cuatro",
                                             text="",
                                             font="Arial",
                                             font_size=15,
                                             font_color=(0, 255, 0))

        self.btn_home = Button_Image(screen=self._slave,
                                     master_x=x,
                                     master_y=y,
                                     x=200,
                                     y=300,
                                     w=100,
                                     h=100,
                                     path_image="gui/home.png",
                                     onclick=self.btn_home_click,
                                     onclick_param="",
                                     text="",
                                     font="Arial")

        self.lista_widgets.append(self.btn_nivel_uno)
        self.lista_widgets.append(self.btn_nivel_dos)
        self.lista_widgets.append(self.btn_nivel_tres)
        self.lista_widgets.append(self.btn_nivel_cuatro)
        self.lista_widgets.append(self.btn_home)

    
    def verificar_archivo_json(self, nombre_nivel):
        nombre_archivo = f"datos_partida_{nombre_nivel}.json"
        return os.path.exists(nombre_archivo)
    
        
    def update(self, lista_eventos):
        if self.verificar_dialog_result():
            for widget in self.lista_widgets:
                widget.update(lista_eventos)
            self.draw()
        else:
            self.hijo.update(lista_eventos)
    
    def actualizar_estado_niveles(self):
        # Verificar desbloqueo de niveles
        self.nivel_dos_desbloqueado = self.nivel_uno_completado
        self.nivel_tres_desbloqueado = self.nivel_dos_completado
        self.nivel_cuatro_desbloqueado = self.nivel_tres_completado

        # Actualizar estado de completado de niveles
        self.nivel_uno_completado = os.path.exists("datos_partida_NivelUno.json")
        self.nivel_dos_completado = os.path.exists("datos_partida_NivelDos.json")
        self.nivel_tres_completado = os.path.exists("datos_partida_NivelTres.json")
        self.nivel_cuatro_completado = os.path.exists("datos_partida_NivelCuatro.json")
    
    def entrar_nivel(self, nombre_nivel):
        nivel_actual = None

        if (
            (nombre_nivel == "nivel_uno" and self.nivel_uno_desbloqueado) or
            (nombre_nivel == "nivel_dos" and self.nivel_dos_desbloqueado) or
            (nombre_nivel == "nivel_tres" and self.nivel_tres_desbloqueado) or
            (nombre_nivel == "nivel_cuatro" and self.nivel_cuatro_desbloqueado)
        ):
            nivel_actual = nombre_nivel
            nivel = self.manejador_niveles.get_nivel(nombre_nivel)
            contenedor_nivel = ContenedorNivel(self._master, nivel)
            self.show_dialog(contenedor_nivel)
            imagen_nivel = self.niveles_imagenes[nombre_nivel]
            self.mostrar_imagen(imagen_nivel)

        self.actualizar_estado_niveles()


    def btn_home_click(self, param):
        from GUI_forn_prueba import FormPrueba
        self.form_prueba = FormPrueba(self._slave, 0, 0, 1000, 600, 'Gold', 'Cyan', 3, True)
        self.end_dialog()
    
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