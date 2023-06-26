from pygame.locals import *
from NivelUno import NivelUno
from NivelDos import NivelDos
from NivelTres import NivelTres

class ManejadorNiveles:
    def __init__(self,pantalla):
        self._slave = pantalla
        self.niveles = {"nivel_uno": NivelUno ,"nivel_dos": NivelDos, "nivel_tres": NivelTres}
           
        
    def get_nivel(self, nombre_nivel):
        return self.niveles[nombre_nivel](self._slave)
