import pygame, sys
from personaje_2 import Personaje
from enemigo import Enemigo
from plataforma import Plataforma

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

pygame.init()

# Tamaño de pantalla
pantalla_width = 1000
pantalla_height = 600

PANTALLA = pygame.display.set_mode((pantalla_width, pantalla_height))
pygame.display.set_caption('StarBattle')

# Reloj
reloj = pygame.time.Clock()
FPS = 60

#define game variables
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]#jugadores scores. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

# Definir variables de imagen
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

#load music and sounds
pygame.mixer.music.load("audio\music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("audio\sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("audio\magic.wav")
magic_fx.set_volume(0.75)

# Cargar fondo
fondo = pygame.image.load('imagenes/69.webp')

# Cargar spritesheet
warrior_sheet = pygame.image.load('warrior\Sprites\warrior.png')
wizard_sheet = pygame.image.load('wizard\Sprites\wizard.png')

victory_img = pygame.image.load("imagenes/victory.png")

# Definir los pasos para animar los sprites
WARRIOR_ANIMACION_PASOS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMACION_PASOS = [8, 8, 1, 8, 8, 3, 7]

# Personajes
personaje_1 = Personaje(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMACION_PASOS, sword_fx)
personaje_2 = Enemigo(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMACION_PASOS, magic_fx)

# Crear una instancia de la plataforma
plataformas = [
    Plataforma(200, 210, 600, 20, 'Gray'),
    Plataforma(100, 400, 200, 10, 'Gray'),
    Plataforma(700, 400, 200, 10, 'Gray')
]

# Bucle principal
while True:
    reloj.tick(FPS)

    # Pintar fondo
    pintar_fondo()

    # Mostrar estadísticas de los personajes
    pintar_vida_barra(personaje_1.vida, 20, 20)
    pintar_vida_barra(personaje_2.vida, 580, 20)

    # Movimiento personajes
    personaje_1.movimiento(pantalla_width, pantalla_height, PANTALLA, personaje_2, round_over,plataformas)
    personaje_2.move(pantalla_width, pantalla_height, PANTALLA, personaje_1, plataformas)
    if personaje_2.attacking and personaje_2.frame_index == 0:
        personaje_2.attacking = False

    # Actualizar jugadores
    personaje_1.update()
    personaje_2.update()

    # Pintar personajes
    personaje_1.draw(PANTALLA)
    personaje_2.draw(PANTALLA)

    if round_over == False:
        if personaje_1.vivo == False:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif personaje_2.alive == False:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        #display victory image
        PANTALLA.blit(victory_img, (360, 150))
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 3
            fighter_1 = Personaje(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMACION_PASOS, sword_fx)
            fighter_2 = Enemigo(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMACION_PASOS, magic_fx)


    # Pintar las plataformas
    for plataforma in plataformas:
        plataforma.pintar(PANTALLA)

    # Ataque automático del personaje_2
    if not personaje_2.attacking and not personaje_2.hit and personaje_2.attack_cooldown == 0:
        personaje_2.attack(PANTALLA, personaje_1)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()

    pygame.display.flip()