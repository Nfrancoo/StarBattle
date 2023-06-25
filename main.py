import pygame
class Nivel:
    def __init__(self, pantalla, personaje_principal, lista_plataformas, img_fondo):
        self._slave = pantalla
        self.jugador = personaje_principal
        self.plataformas = lista_plataformas
        self.img_fondo = img_fondo
    
    def update(self, lista_eventos):
            # Dibujar fondo
        pintar_fondo()

        # Mostrar estadísticas de los jugadores
        pintar_vida_barra(personaje_1.vida, 20, 20)
        pintar_vida_barra(personaje_2.vida, 580, 20)
        escribir_texto("P1: " + str(score[0]), score_font, 'Red', 20, 60)
        escribir_texto("P2: " + str(score[1]), score_font, 'Red', 580, 60)

        # Actualizar cuenta regresiva
        
            # Mover personajes
        personaje_1.movimiento(pantalla_width, pantalla_height, PANTALLA, personaje_2, round_over, plataformas)
        personaje_2.movimiento(pantalla_width, pantalla_height, PANTALLA, personaje_1, round_over, plataformas)


        # Actualizar personajes
        personaje_1.update()
        personaje_2.update()

        # Dibujar personajes
        personaje_1.draw(PANTALLA)
        personaje_2.draw(PANTALLA)

        # Verificar derrota de los jugadores
        # Verificar derrota de los jugadores
        if round_over == False:
            if personaje_1.vivo == False:
                score[1] += 1
                if score[1] == 2:
                    round_over = True
                else:
                    round_over = True
                    round_over_time = pygame.time.get_ticks()
            elif personaje_2.vivo == False:
                score[0] += 1
                if score[0] == 2:
                    round_over = True
                else:
                    round_over = True
                    round_over_time = pygame.time.get_ticks()
        else:
            if score[0] == 2 or score[1] == 2:
                if score[0] == 2:
                    PANTALLA.blit(imagen_victoria, (360, 150))
                else:
                    PANTALLA.blit(imagen_gameover, (115, 20))
            else:
                # Reiniciar el juego
                if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                    round_over = False
                    intro_count = 3
                    personaje_1 = Personaje(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMACION_PASOS)
                    personaje_2 = Enemigo(2, 700, 310, True, ESPADACHIN_DATA, espadachin_sheet, ESPADACHIN_ANIMACION_PASOS)

        pygame.display.update()
        
    def pintar_fondo(self, W, H):
        fondo_escalado = pygame.transform.scale(self.img_fondo, (W, H))
        self._slave.blit(fondo_escalado, (0, 0))

    # Función para pintar la barra de vida en pantalla
    def pintar_vida_barra(self,vida, x, y):
        ratio = vida / 100
        pygame.draw.rect(self._slave, 'White', (x - 2, y - 2, 404, 34))
        pygame.draw.rect(self._slave, 'Red', (x, y, 400, 30))
        pygame.draw.rect(self._slave, 'Yellow', (x, y, 400 * ratio, 30))

    # Función para dibujar el rango de ataque del enemigo
    def pintar_rango_ataque(self,enemigo):
        pygame.draw.rect(self._slave, (0, 255, 0), enemigo.rango_ataque, 2)

    def pintar_rectangulo(self,personaje):
        pygame.draw.rect(self._slave, 'Red', personaje.rect, 2)

    # Función para dibujar texto
    def escribir_texto(self, text, font,color, x, y):
        img = font.render(text, True, color)
        self._slave.blit(img, (x, y))
        '''
        render toma el texto, un valor booleano que indica si se debe aplicar un suavizado al texto 
        (en este caso se establece en True)
    '''
