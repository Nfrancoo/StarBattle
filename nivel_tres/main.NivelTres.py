import pygame
import os
import sys
from personajeNT import Personaje
from enemigoNT import Enemigo
from plataforma import Plataforma
from animacion import AnimatedBackground

pygame.init()

# Función para pintar el fondo
def pintar_vida_barra(vida, x, y):
    ratio = vida / 100
    pygame.draw.rect(PANTALLA, 'White', (x - 2, y - 2, 404, 34))
    pygame.draw.rect(PANTALLA, 'Red', (x, y, 400, 30))
    pygame.draw.rect(PANTALLA, 'Yellow', (x, y, 400 * ratio, 30))

def escribir_texto(text, font,color, x, y):
    img = font.render(text, True, color)
    PANTALLA.blit(img, (x, y))

def pintar_rango_ataque(enemigo):
    pygame.draw.rect(PANTALLA, (0, 255, 0), enemigo.rango_ataque, 2)

def pintar_rectangulo(personaje):
    pygame.draw.rect(PANTALLA, 'Red', personaje.rect, 2)

def load_images(path):
    images = [pygame.image.load(path + os.sep + file_name).convert() for file_name in sorted(os.listdir(path))]
    return images


def pintar_fondo():
    global PANTALLA, pantalla_width, pantalla_height
    fondo_escalado = pygame.transform.scale(background.image, (pantalla_width, pantalla_height))
    PANTALLA.blit(fondo_escalado, (0, 0))


pygame.init()
global PANTALLA, background, pantalla_width, pantalla_height

pantalla_width = 1000
pantalla_height = 600

PANTALLA = pygame.display.set_mode((pantalla_width, pantalla_height))
pygame.display.set_caption('StarBattle')
FPS = 60
clock = pygame.time.Clock()

    # Definir variables del juego
last_count_update = pygame.time.get_ticks()
score = [0, 0]  # Puntuaciones de los jugadores. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

# Definir variables de imagen
WARRIOR_TAMAÑO = 162
WARRIOR_ESCALA = 4
WARRIOR_DESPLAZAMIENTO = [72, 46] #12 para el lado derecho y 92 lado izquierdo
WARRIOR_DATA = [WARRIOR_TAMAÑO, WARRIOR_ESCALA, WARRIOR_DESPLAZAMIENTO]
ESPADACHIN_TAMAÑO = 180
ESPADACHIN_ESCALA = 3
ESPADACHIN_DESPLAZAMIENTO = [61, 106]
ESPADACHIN_DATA = [ESPADACHIN_TAMAÑO, ESPADACHIN_ESCALA, ESPADACHIN_DESPLAZAMIENTO]

# Cargar spritesheets
warrior_sheet = pygame.image.load('sheets_personajes/warrior.png')
espadachin_sheet = pygame.image.load('sheets_enemigo/futurista.png')


# Cargar imagen de victoria
imagen_victoria = pygame.image.load("fondos/imagenes/victory_blanco.png")
imagen_gameover = pygame.image.load('fondos/imagenes/endgame_blanco.png')

# Definir número de pasos en cada animación
WARRIOR_ANIMACION_PASOS = [10, 8, 1, 7, 7, 3, 7]
ESPADACHIN_ANIMACION_PASOS = [10, 8, 3, 7, 7, 4, 10]

# Definir fuente
score_font = pygame.font.Font("fonts/turok.ttf", 30)


fondo = load_images(path='fondos/lista_background')
background = AnimatedBackground(position=(0, 0), images=fondo, delay=0.1)
all_sprites = pygame.sprite.Group(background)

personaje_1 = Personaje(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMACION_PASOS)
personaje_2 = Enemigo(2, 700, 310, True, ESPADACHIN_DATA, espadachin_sheet, ESPADACHIN_ANIMACION_PASOS)

plataformas = []#Plataforma(1, 280, 310, 10, (0, 0, 0, 0))]

round_over = False
round_over_time = 0
score = [0, 0]

while True:
    dt = clock.tick(FPS) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    all_sprites.update(dt)
    personaje_1.movimiento(pantalla_width, pantalla_height, PANTALLA, personaje_2, round_over, plataformas)
    personaje_2.movimiento(pantalla_width, pantalla_height, PANTALLA, personaje_1, round_over, plataformas)

    pintar_fondo()


    # Mostrar estadísticas de los jugadores
    pintar_vida_barra(personaje_1.vida, 20, 20)
    pintar_vida_barra(personaje_2.vida, 580, 20)
    escribir_texto("P1: " + str(score[0]), score_font, 'Red', 20, 60)
    escribir_texto("P2: " + str(score[1]), score_font, 'Red', 580, 60)
    personaje_1.update()
    personaje_2.update()

    personaje_1.draw(PANTALLA)
    personaje_2.draw(PANTALLA)

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
                PANTALLA.blit(imagen_victoria, (265, 100))
            else:
                PANTALLA.blit(imagen_gameover, (115, 20))
        else:
            if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                round_over = False
                intro_count = 3
                personaje_1 = Personaje(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMACION_PASOS)
                personaje_2 = Enemigo(2, 700, 310, True, ESPADACHIN_DATA, espadachin_sheet, ESPADACHIN_ANIMACION_PASOS)

    # pintar_rango_ataque(personaje_2)
    # pintar_rango_ataque(personaje_1)
    # pintar_rectangulo(personaje_1)
    # pintar_rectangulo(personaje_2)

    if personaje_2.rango_ataque.colliderect(personaje_1.rect) and personaje_2.vivo:
        personaje_2.ataque(personaje_1, PANTALLA)

    for plataforma in plataformas:
        plataforma.pintar(PANTALLA)

    pygame.display.flip()

# Salir de pygame
pygame.quit()