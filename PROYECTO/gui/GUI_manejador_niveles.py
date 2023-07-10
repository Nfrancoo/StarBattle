from pygame.locals import *
from niveles.NivelUno import NivelUno
from niveles.NivelDos import NivelDos
from niveles.NivelTres import NivelTres
from niveles.NivelCuatro import NivelCuatro

class ManejadorNiveles:
    def __init__(self,pantalla):
        self._slave = pantalla
        self.niveles = {"nivel_uno": NivelUno ,"nivel_dos": NivelDos, "nivel_tres": NivelTres, "nivel_cuatro": NivelCuatro}
           
        
    def get_nivel(self, nombre_nivel):
        return self.niveles[nombre_nivel](self._slave)
