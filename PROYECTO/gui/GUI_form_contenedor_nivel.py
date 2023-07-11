import pygame
import pygame.locals

from gui.GUI_form import *
from gui.GUI_button_image import *
from gui.GUI_FormPause import FormPausa


class ContenedorNivel(Form):
    def __init__(self, pantalla: pygame.Surface, nivel):
        super().__init__(pantalla, 0, 0, pantalla.get_width(), pantalla.get_height(), color_background='sakjs')
        nivel._slave = self._slave
        self.nivel = nivel
        self.setting = False
        self._btn_home = Button_Image(screen=self._slave,
                                        master_x = self._x,
                                        master_y = self._y,
                                        x = self._w - 100,
                                        y = self._h - 100,
                                        w = 50,
                                        h = 50,
                                        color_background= (250,0,0),
                                        color_border= (255,0,255),
                                        onclick= self.btn_home_click,
                                        onclick_param= "",
                                        text= "",
                                        font= "Verdana",
                                        font_size= 15,
                                        font_color= (0,255,0),
                                        path_image= 'proyecto/gui\home.png')


        self._btn_pause = Button_Image(screen=self._slave,
                                 master_x= self._x,
                                 master_y= self._y,
                                 x=470,
                                 y=50,
                                 w=60,
                                 h=60,
                                 path_image="PROYECTO/fondos\imagenes\pausa_logo.png",
                                 onclick=self.btn_settings_click,
                                 onclick_param="settings")
        
        self.lista_widgets.append(self._btn_pause)
        self.lista_widgets.append(self._btn_home)


    def update(self, lista_evento):
        if self.setting == False:
            self.nivel.update(lista_evento)
            for widget in self.lista_widgets:
                widget.update(lista_evento)
            self.draw()
        else:
            if self.verificar_dialog_result():
                for widget in self.lista_widgets:
                    widget.update(lista_evento)
                self.draw()
            else:
                self.hijo.update(lista_evento)


    def btn_settings_click(self, text):
        formulario_setting = FormPausa(self._master, 0, 0, 900, 700, "Black", "Black", True, self)
        self.setting = True
        self.show_dialog(formulario_setting)


    def btn_home_click(self, param):
        from gui.GUI_form_menu_play import formNiveles
        formulario_niveles = formNiveles(self._master, 100, 25, 800, 550, "Black", "Black", True, "proyecto/gui\Window.png")
        self.show_dialog(formulario_niveles)
        self.end_dialog()

