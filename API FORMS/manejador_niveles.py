from pygame.locals import *
from nivel_uno.main_NivelUno import *
from nivel_dos.main_NivelDos import *
from nivel_tres.main_NivelTres import *

class ManejadorNiveles:
    def __init__(self,pantalla):
        self._slave = pantalla
        self.niveles = {"nivel_uno": , "nivel_dos": NivelDos, "nivel_tres": NivelTres}
           
        
    def get_nivel(self, nombre_nivel):
        return self.niveles[nombre_nivel](self._slave)
