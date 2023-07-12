import pygame
from pygame.locals import *
from gui.GUI_form import *
from gui.GUI_button_image import *
from gui.GUI_label import *
from gui.GUI_slider import *
from personaje.personajeNU import Personaje

# Variable para almacenar el volumen actual
current_volume = 0.2

class formSettings(Form):
    def __init__(self, screen, x, y, w, h, color_background, color_border, active, contenedor_nivel=None):
        super().__init__(screen, x, y, w, h, color_background, color_border, active)
        self.contenedor_nivel = contenedor_nivel
        self.volumen = current_volume  # Utiliza el volumen actual almacenado
        self.flag_play = True
        self.picture_box = PictureBox(self._slave, 0, 0, 800, 500, "proyecto/fondos\imagenes\settings.png")
        self.btn_play = Button_Image(self._slave,x,y,100,190,40,40,"PROYECTO/fondos\imagenes\music.png",self.btn_play_click, "hola")
        self.label_volumen = Label(self._slave, 590, 190, 100, 50, f"{round(self.volumen * 100)}%", "Comic Sans", 15, "White", "proyecto/gui\Table.png")
        self.slider_volumen = Slider(self._slave,x,y,150,200,400,15,self.volumen,"Blue","White")
        self.btn_home = Button_Image(screen=self._slave,
                                      master_x=self._x,
                                      master_y=self._y,
                                      x=self._w-180,
                                      y=self._h-230,
                                      w=80,
                                      h=80,
                                      path_image="proyecto/gui/home.png",
                                      onclick=self.btn_home_click,
                                      onclick_param="",
                                      text="",
                                      font="Arial",
                                      )

        self.lista_widgets.append(self.picture_box)
        self.lista_widgets.append(self.btn_home)           
        self.lista_widgets.append(self.btn_play)
        self.lista_widgets.append(self.label_volumen)
        self.lista_widgets.append(self.slider_volumen)
        
    def btn_play_click(self, texto):
        if self.flag_play:
            pygame.mixer.music.pause()
            off = pygame.image.load('PROYECTO/fondos/imagenes/music_off.png')
            pygame.transform.scale(off, (50, 50))
            self.btn_play._slave = off
            self.ejecutar_sonido = False  # Establecer en False cuando la música se pausa
        else:
            pygame.mixer.music.unpause()
            on = pygame.image.load('PROYECTO/fondos/imagenes/music.png')
            pygame.transform.scale(on, (50, 50))
            self.btn_play._slave = on
            self.ejecutar_sonido = True  # Establecer en True cuando la música se reanuda

        self.flag_play = not self.flag_play
        
                    
    def update_volumen(self,lista_eventos):
        self.volumen = self.slider_volumen.value
        self.label_volumen.set_text(f"{round(self.volumen * 100)}%")
        pygame.mixer.music.set_volume(self.volumen)
        
        # Actualiza la variable de volumen actual
        global current_volume
        current_volume = self.volumen
            
    def update(self,lista_eventos):
        if self.verificar_dialog_result():
            if self.active:
                self.draw()
                self.render()
                for widget in self.lista_widgets:
                    widget.update(lista_eventos)
                    self.update_volumen(lista_eventos)
        else:
            self.hijo.update(lista_eventos)

    def render(self):
        self._slave.fill(self._color_background)
    
    def btn_home_click(self, param):
        if self.contenedor_nivel != None:
            self.contenedor_nivel.setting = False  # Establecer self.setting en False
            self.end_dialog()
        self.end_dialog()
