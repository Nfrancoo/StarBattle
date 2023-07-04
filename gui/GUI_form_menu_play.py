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
        aux_image = pygame.transform.scale(aux_image,(w,h))
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
        
        self.btn_nivel_uno = Button_Image(screen=self._slave,
                                          master_x= x,
                                          master_y= y,
                                          x = 200,
                                          y =120,
                                          w = 100,
                                          h = 100,
                                          path_image="fondos\imagenes/nivel_uno.png",
                                          onclick= self.entrar_nivel,
                                          onclick_param="nivel_uno",
                                          text="",
                                          font="Arial")
        
        self.btn_nivel_dos = Button_Image(screen=self._slave,
                                          master_x= x,
                                          master_y= y,
                                          x = 300,
                                          y =120,
                                          w = 100,
                                          h = 100,
                                          path_image="fondos\imagenes/nivel_dos.png",
                                          onclick= self.entrar_nivel,
                                          onclick_param="nivel_dos",
                                          text="",
                                          font="Arial")

        self.btn_nivel_tres = Button_Image(screen=self._slave,
                                          master_x= x,
                                          master_y= y,
                                          x = 400,
                                          y =120,
                                          w = 100,
                                          h = 100,
                                          color_background=(255,0,0),
                                          color_border=(255,0,255),
                                          path_image="fondos\imagenes/nivel_tres.png",
                                          onclick= self.entrar_nivel,
                                          onclick_param="nivel_tres",
                                          text="",
                                          font="Arial",
                                          font_size= 15,
                                          font_color=(0,255,0))
        
        self.btn_nivel_cuatro = Button_Image(screen=self._slave,
                                          master_x= x,
                                          master_y= y,
                                          x = 500,
                                          y =120,
                                          w = 100,
                                          h = 100,
                                          color_background=(255,0,0),
                                          color_border=(255,0,255),
                                          path_image="fondos\imagenes/nivel_cuatro.png",
                                          onclick= self.entrar_nivel,
                                          onclick_param="nivel_cuatro",
                                          text="",
                                          font="Arial",
                                          font_size= 15,
                                          font_color=(0,255,0))

        self.btn_home = Button_Image(screen=self._slave,
                                          master_x= x,
                                          master_y= y,
                                          x = 200,
                                          y =300,
                                          w = 100,
                                          h = 100,
                                          path_image="gui\home.png",
                                          onclick= self.btn_home_click,
                                          onclick_param="",
                                          text="",
                                          font="Arial",
                                          )
        
        self.lista_widgets.append(self.btn_nivel_uno)
        self.lista_widgets.append(self.btn_nivel_dos)
        self.lista_widgets.append(self.btn_nivel_tres)
        self.lista_widgets.append(self.btn_nivel_cuatro)
        self.lista_widgets.append(self.btn_home) 
        
    def on(self,parametro):
        print("hola",parametro)
        
    def update(self, lista_eventos):
        if self.verificar_dialog_result():
            for widget in self.lista_widgets:
                widget.update(lista_eventos)
            self.draw()
        else:
            self.hijo.update(lista_eventos)
    
    def entrar_nivel(self, nombre_nivel):
        nivel_completado = False
        nivel_actual = None
        
        if nombre_nivel == "nivel_uno" and self.nivel_uno_desbloqueado:
            nivel_actual = "nivel_uno"
            nivel = self.manejador_niveles.get_nivel(nombre_nivel)
            contenedor_nivel = ContenedorNivel(self._master, nivel)
            self.show_dialog(contenedor_nivel)
        elif nombre_nivel == "nivel_dos" and self.nivel_dos_desbloqueado:
            nivel_actual = "nivel_dos"
            nivel = self.manejador_niveles.get_nivel(nombre_nivel)
            contenedor_nivel = ContenedorNivel(self._master, nivel)
            self.show_dialog(contenedor_nivel)
        elif nombre_nivel == "nivel_tres" and self.nivel_tres_desbloqueado:
            nivel_actual = "nivel_tres"
            nivel = self.manejador_niveles.get_nivel(nombre_nivel)
            contenedor_nivel = ContenedorNivel(self._master, nivel)
            self.show_dialog(contenedor_nivel)
        elif nombre_nivel == "nivel_cuatro" and self.nivel_cuatro_desbloqueado:
            nivel_actual = "nivel_cuatro"
            nivel = self.manejador_niveles.get_nivel(nombre_nivel)
            contenedor_nivel = ContenedorNivel(self._master, nivel)
            self.show_dialog(contenedor_nivel)
        
        if nivel_actual is not None:
            # Verificar si el nivel actual completado es el último nivel disponible
            if nivel_actual == "nivel_cuatro":
                print("¡Felicidades! Has completado todos los niveles.")
                # Realizar acciones adicionales aquí, como mostrar un mensaje de victoria o regresar al menú principal
                
            # Desbloquear el siguiente nivel si no es el último
            if nivel_actual == "nivel_uno":
                self.nivel_dos_desbloqueado = True
            elif nivel_actual == "nivel_dos":
                self.nivel_tres_desbloqueado = True
            elif nivel_actual == "nivel_tres":
                self.nivel_cuatro_desbloqueado = True
            
    def btn_home_click(self,param):
        self.end_dialog()
        
        # Reiniciar variables de desbloqueo y completado de niveles
        self.nivel_uno_desbloqueado = True
        self.nivel_dos_desbloqueado = False
        self.nivel_tres_desbloqueado = False
        self.nivel_cuatro_desbloqueado = False
        self.nivel_uno_completado = False
        self.nivel_dos_completado = False
        self.nivel_tres_completado = False
        self.nivel_cuatro_completado = False
