from pygame.locals import *
from NivelUno import NivelUno
from NivelDos import NivelDos
from NivelTres import NivelTres
from NivelCuatro import NivelCuatro

class ManejadorNiveles:
    def __init__(self,pantalla):
        self._slave = pantalla
        self.niveles = {"nivel_uno": NivelUno ,"nivel_dos": NivelDos, "nivel_tres": NivelTres, "nivel_cuatro": NivelCuatro}
           
        
    def get_nivel(self, nombre_nivel):
        return self.niveles[nombre_nivel](self._slave)
