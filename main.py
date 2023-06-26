import pygame

class Nivel:
    def __init__(self, pantalla, personaje_principal, enemigo,  lista_plataformas, img_fondo, round_over):
        self._slave = pantalla
        self.jugador = personaje_principal
        self.enemigo = enemigo
        self.plataformas = lista_plataformas
        self.img_fondo = img_fondo
        self.round_over = False

    def update(self, lista_eventos, W, H, score, score_font):
        # Dibujar fondo
        self.pintar_fondo(W, H)

        # Mostrar estadísticas de los jugadores
        self.pintar_vida_barra(self.jugador.vida, 20, 20)
        self.pintar_vida_barra(self.jugador.vida, 580, 20)
        self.escribir_texto("P1: " + str(score[0]), score_font, 'Red', 20, 60)
        self.escribir_texto("P2: " + str(score[1]), score_font, 'Red', 580, 60)

        # Actualizar cuenta regresiva

        # Mover personajes
        self.jugador.movimiento(W, H, self._slave, self.enemigo, self.round_over, self.plataformas)
        self.enemigo.movimiento(W, H, self._slave, self.jugador, self.round_over, self.plataformas)

        # Actualizar personajes
        self.jugador.update()
        self.enemigo.update()

        # Dibujar personajes
        self.jugador.draw(self._slave)
        self.enemigo.draw(self._slave)

        # Verificar derrota de los jugadores

        
    def pintar_fondo(self, W, H):
        fondo_escalado = pygame.transform.scale(self.img_fondo, (W, H))
        self._slave.blit(fondo_escalado, (0, 0))

    # Función para pintar la barra de vida en pantalla
    def pintar_vida_barra(self, vida, x, y):
        ratio = vida / 100
        pygame.draw.rect(self._slave, 'White', (x - 2, y - 2, 404, 34))
        pygame.draw.rect(self._slave, 'Red', (x, y, 400, 30))
        pygame.draw.rect(self._slave, 'Yellow', (x, y, 400 * ratio, 30))

    # Función para dibujar el rango de ataque del enemigo
    def pintar_rango_ataque(self, enemigo):
        pygame.draw.rect(self._slave, (0, 255, 0), enemigo.rango_ataque, 2)

    def pintar_rectangulo(self, personaje):
        pygame.draw.rect(self._slave, 'Red', personaje.rect, 2)

    # Función para dibujar texto
    def escribir_texto(self, text, font, color, x, y):
        img = font.render(text, True, color)
        self._slave.blit(img, (x, y))

        '''
        render toma el texto, un valor booleano que indica si se debe aplicar un suavizado al texto 
        (en este caso se establece en True)
    '''
