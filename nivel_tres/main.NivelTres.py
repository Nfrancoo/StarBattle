import pygame
import sys
from personajeNT import Personaje
from enemigoNT import Enemigo
from plataforma import Plataforma

pygame.init()

# Función para pintar el fondo
def pintar_fondo():
    global PANTALLA
    fondo_escalado = pygame.transform.scale(fondo, (pantalla_width, pantalla_height))
    PANTALLA.blit(fondo_escalado, (0, 0))

# Función para pintar la barra de vida en pantalla
def pintar_vida_barra(vida, x, y):
    ratio = vida / 100
    pygame.draw.rect(PANTALLA, 'White', (x - 2, y - 2, 404, 34))
    pygame.draw.rect(PANTALLA, 'Red', (x, y, 400, 30))
    pygame.draw.rect(PANTALLA, 'Yellow', (x, y, 400 * ratio, 30))

# Función para dibujar el rango de ataque del enemigo
def pintar_rango_ataque(enemigo):
    pygame.draw.rect(PANTALLA, (0, 255, 0), enemigo.rango_ataque, 2)

def pintar_rectangulo(personaje):
    pygame.draw.rect(PANTALLA, 'Red', personaje.rect, 2)

# Función para dibujar texto
def escribir_texto(text, font,color, x, y):
    img = font.render(text, True, color)
    PANTALLA.blit(img, (x, y))
    '''
    render toma el texto, un valor booleano que indica si se debe aplicar un suavizado al texto 
    (en este caso se establece en True)
    '''

# Crear ventana del juego
pantalla_width = 1000
pantalla_height = 600

PANTALLA = pygame.display.set_mode((pantalla_width, pantalla_height))
pygame.display.set_caption('StarBattle')

# Reloj
reloj = pygame.time.Clock()
FPS = 60

# Definir variables del juego
last_count_update = pygame.time.get_ticks()
score = [0, 0]  # Puntuaciones de los jugadores. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

# Definir variables de imagen
WARRIOR_TAMAÑO = 162
WARRIOR_ESCALA = 4
WARRIOR_DESPLAZAMIENTO = [72, 56] #12 para el lado derecho y 92 lado izquierdo
WARRIOR_DATA = [WARRIOR_TAMAÑO, WARRIOR_ESCALA, WARRIOR_DESPLAZAMIENTO]
ESPADACHIN_TAMAÑO = 200
ESPADACHIN_ESCALA = 3
ESPADACHIN_DESPLAZAMIENTO = [81, 116]
ESPADACHIN_DATA = [ESPADACHIN_TAMAÑO, ESPADACHIN_ESCALA, ESPADACHIN_DESPLAZAMIENTO]


# Cargar imagen de fondo
fondo = pygame.image.load('imagenes/aguita.gif')

# Cargar spritesheets
warrior_sheet = pygame.image.load('warrior\Sprites\warrior.png')
espadachin_sheet = pygame.image.load('wizard/Sprites/espadachin.png')

# Cargar imagen de victoria
imagen_victoria = pygame.image.load("imagenes/victory.png")
imagen_gameover = pygame.image.load('imagenes/endgame.png')

# Definir número de pasos en cada animación
WARRIOR_ANIMACION_PASOS = [10, 8, 1, 7, 7, 3, 7]
ESPADACHIN_ANIMACION_PASOS = [4, 8, 1, 3, 4, 3, 7]

# Definir fuente
score_font = pygame.font.Font("fonts/turok.ttf", 30)

# Crear dos instancias de personaje
personaje_1 = Personaje(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMACION_PASOS,)
personaje_2 = Enemigo(2, 700, 310, True, ESPADACHIN_DATA, espadachin_sheet, ESPADACHIN_ANIMACION_PASOS,)

plataformas = [Plataforma(1, 280, 310, 10, (0, 0, 0, 0))]

# Bucle principal del juego

while True:
    reloj.tick(FPS)

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


    # Debug: Dibujar rango de ataque del enemigo
    pintar_rango_ataque(personaje_2)
    pintar_rango_ataque(personaje_1)
    pintar_rectangulo(personaje_1)
    pintar_rectangulo(personaje_2)

    if personaje_2.rango_ataque.colliderect(personaje_1.rect) and personaje_2.vivo:
        personaje_2.ataque(personaje_1, PANTALLA)
      
    # Manejador de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)

    for plataforma in plataformas:
        plataforma.pintar(PANTALLA)

    # Actualizar pantalla
    pygame.display.flip()

# Salir de pygame
pygame.quit()