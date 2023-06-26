from plataforma import Plataforma
from personajeNU import Personaje
from enemigoNU import Enemigo
import pygame

class Nivel:
    def __init__(self, pantalla, personaje_principal, enemigo, lista_plataformas, img_fondo, round_over):
        self._slave = pantalla
        self.jugador = personaje_principal
        self.enemigo = enemigo
        self.plataformas = lista_plataformas
        self.img_fondo = img_fondo
        self.round_over = round_over

    def pintar_fondo(self):
        fondo_escalado = pygame.transform.scale(self.img_fondo, (self._slave.get_width(), self._slave.get_height()))
        self._slave.blit(fondo_escalado, (0, 0))

    def pintar_vida_barra(self, vida, x, y):
        ratio = vida / 100
        pygame.draw.rect(self._slave, 'White', (x - 2, y - 2, 404, 34))
        pygame.draw.rect(self._slave, 'Red', (x, y, 400, 30))
        pygame.draw.rect(self._slave, 'Yellow', (x, y, 400 * ratio, 30))

    def pintar_rectangulo(self, personaje):
        pygame.draw.rect(self._slave, 'Red', personaje.rect, 2)

    def escribir_texto(self, text, font, color, x, y):
        img = font.render(text, True, color)
        self._slave.blit(img, (x, y))

    def dibujar_plataformas(self):
        for plataforma in self.plataformas:
            plataforma.pintar(self._slave)

    def pintar_rango_ataque(self, personaje):
        pygame.draw.rect(self._slave, (0, 255, 0), personaje.rango_ataque, 2)

    def dibujar_personajes(self):
        self.jugador.draw(self._slave)
        self.enemigo.draw(self._slave)

    def verificar_derrota(self):
        if self.round_over == False:
            if self.jugador.vivo == False:
                return 2  # Jugador 2 gana la ronda
            elif self.enemigo.vivo == False:
                return 1  # Jugador 1 gana la ronda
        return 0  # La ronda no ha terminado

    def reiniciar_ronda(self):
        self.round_over = False
        self.jugador.reset()

    def actualizar(self):
        self.jugador.update()
        self.enemigo.update()

    def ataque_enemigo(self):
        if self.enemigo.rango_ataque.colliderect(self.jugador.rect) and self.enemigo.vivo:
            self.enemigo.ataque(self.jugador, self._slave)

    def actualizar_pantalla(self):
        pygame.display.update()