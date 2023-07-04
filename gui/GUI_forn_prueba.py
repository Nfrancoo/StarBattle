import pygame
from pygame.locals import *

from GUI_button import Button
from GUI_slider import Slider
from GUI_textbox import TextBox
from GUI_label import Label
from GUI_form import Form
from GUI_button_image import Button_Image
from GUI_form_menu_score import FormMenuScore
from GUI_form_menu_play import formNiveles
from GUI_picture_box import PictureBox

class FormPrueba(Form):
    def __init__(self, screen, x, y, w, h, color_background, color_border="Black", border_size=-1, active=True):
        super().__init__(screen, x, y, w, h, color_background, color_border, border_size, active)

        self.volumen = 0.2
        self.flag_play = True

        pygame.mixer.init()

        ######CONTROLES #####
        self.txtbox = TextBox(self._slave, x, y, 300, 50, 300, 30, "Gray", "White", "Red", "Blue", 2,
                              font="Comic Sans", font_size=15, font_color="Black")
        # self.btn_play = Button(self._slave, x, y, 100, 100, 100, 50, "Red", "Blue", self.btn_play_click, "Nombre",
        #                        "Pausa", font="Verdana", font_size=15, font_color="White")
        # self.label_volumen = Label(self._slave, 650, 190, 100, 50, "20%", "Comic Sans", 15, "White", "gui\Table.png")
        # self.slider_volumen = Slider(self._slave, x, y, 100, 200, 500, 15, self.volumen, "Blue", "White")
        self.btn_tabla = Button_Image(self._slave, x, y, 755, 50, 50, 50, "gui\Menu_BTN.png", self.btn_tabla_click,
                                      "lala")
        self.btn_niveles = Button_Image(self._slave, x, y, 830, 50, 50, 50, "gui\play_BTN.png", self.btn_imagen_click,
                                        "niveles")
        # self.btn_settings = Button_Image(self._slave,x,y,730,20,170,170,"zyro-image-PhotoRoom.png-PhotoRoom.png",self.btn_settings_click, "settings")
        self.picture_box = PictureBox(self._slave, 0, 0, 900, 720, "fondos/imagenes/fondo.png")
        ######

        # Agrego los controles a la lista
        self.lista_widgets.append(self.txtbox)
        # self.lista_widgets.append(self.btn_play)
        # self.lista_widgets.append(self.label_volumen)
        # self.lista_widgets.append(self.slider_volumen)
        self.lista_widgets.append(self.btn_tabla)
        self.lista_widgets.append(self.btn_niveles)
        # self.lista_widgets.append(self.btn_settings)
        self.lista_widgets.append(self.picture_box)

        pygame.mixer.music.load("gui\Vengeance (Loopable).wav")

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
                # self.update_volumen(lista_eventos)
        else:
            self.hijo.update(lista_eventos)

    def render(self):
        self._slave.fill(self._color_background)

    # def btn_play_click(self, texto):
    #     if self.flag_play:
    #         pygame.mixer.music.pause()
    #         self.btn_play._color_background = "Cyan"
    #         self.btn_play._font_color = "Red"
    #         self.btn_play.set_text("Play")
    #     else:
    #         pygame.mixer.music.unpause()
    #         self.btn_play._color_background = "Red"
    #         self.btn_play._font_color = "White"
    #         self.btn_play.set_text("Pause")

    #     self.flag_play = not self.flag_play

    # def update_volumen(self, lista_eventos):
    #     self.volumen = self.slider_volumen.value
    #     self.label_volumen.set_text(f"{round(self.volumen * 100)}%")
    #     pygame.mixer.music.set_volume(self.volumen)

    def btn_imagen_click(self,text):
        formulario_niveles = formNiveles(self._master,100,25,800,550,"Black","Black",True,"api_forms\contenedor_niveles.png")
        self.show_dialog(formulario_niveles)
        
    # def btn_settings_click(self,text):
    #     formulario_setting = formSettings(self._master,100,25,800,550,"Black","Black",True)
    #     self.show_dialog(formulario_setting)

    def btn_tabla_click(self, texto):
        dic_score = [{"jugador": "Franco", "Score": 1},
                     {"jugador": "Lili", "Score": 1220},
                     {"jugador": "Diego", "Score": 190}]

        form_puntaje = FormMenuScore(self._master,
                                     250,
                                     25,
                                     500,
                                     550,
                                     (220, 0, 220),
                                     "White",
                                     True,
                                     "gui\Window.png",
                                     dic_score,
                                     100,
                                     10,
                                     10)

        self.show_dialog(form_puntaje)