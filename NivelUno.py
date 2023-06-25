import sys
import pygame
from nivel import Nivel
from nivel_uno.plataforma import Plataforma
from nivel_uno.personajeNU import Personaje
from nivel_uno.enemigoNU import Enemigo

class NivelUno(Nivel):
    def __init__(self, pantalla: pygame.Surface):