import pygame
from pygame.locals import *

from gui.GUI_form import *
from gui.GUI_button_image import *
from gui.GUI_label import *
from gui.GUI_slider import *
from gui.GUI_picture_box import *
from gui.GUI_formsetting import formSettings



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
                                      x= 380,
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
                                 x=480,
                                 y=250,
                                 w=60,
                                 h=60,
                                 path_image="proyecto/fondos\imagenes\setting_logo.png",
                                 onclick=self.btn_settings_click,
                                 onclick_param="settings")

        self.lista_widgets.append(self.fondo)      
        self.lista_widgets.append(self.btn_home)           
        self.lista_widgets.append(self._btn_settings)

            
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
