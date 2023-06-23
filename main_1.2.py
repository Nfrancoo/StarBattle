import pygame
from pygame import mixer
from personaje_2 import Personaje
from enemigo_2 import Enemigo
from plataforma import Plataforma

mixer.init()
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
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    PANTALLA.blit(img, (x, y))

# Crear ventana del juego
pantalla_width = 1000
pantalla_height = 600

PANTALLA = pygame.display.set_mode((pantalla_width, pantalla_height))
pygame.display.set_caption('StarBattle')

# Reloj
reloj = pygame.time.Clock()
FPS = 60

# Definir variables del juego
intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]  # Puntuaciones de los jugadores. [P1, P2]
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

# Cargar música y sonidos
pygame.mixer.music.load("audio/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("audio/sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("audio/magic.wav")
magic_fx.set_volume(0.75)

# Cargar imagen de fondo
fondo = pygame.image.load('imagenes/69.webp')

# Cargar spritesheets
warrior_sheet = pygame.image.load('warrior/Sprites/warrior.png')
wizard_sheet = pygame.image.load('wizard/Sprites/wizard.png')

# Cargar imagen de victoria
victory_img = pygame.image.load("imagenes/victory.png")

# Definir número de pasos en cada animación
WARRIOR_ANIMACION_PASOS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMACION_PASOS = [8, 8, 1, 8, 8, 3, 7]

# Definir fuente
count_font = pygame.font.Font("fonts/turok.ttf", 80)
score_font = pygame.font.Font("fonts/turok.ttf", 30)

# Crear dos instancias de personaje
personaje_1 = Personaje(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMACION_PASOS, sword_fx)
personaje_2 = Enemigo(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMACION_PASOS, magic_fx)

plataformas = []

# Bucle principal del juego
run = True
while run:
    reloj.tick(FPS)

    # Dibujar fondo
    pintar_fondo()

    # Mostrar estadísticas de los jugadores
    pintar_vida_barra(personaje_1.vida, 20, 20)
    pintar_vida_barra(personaje_2.vida, 580, 20)
    draw_text("P1: " + str(score[0]), score_font, 'Red', 20, 60)
    draw_text("P2: " + str(score[1]), score_font, 'Red', 580, 60)

    # Actualizar cuenta regresiva
    if intro_count <= 0:
        # Mover personajes
        personaje_1.movimiento(pantalla_width, pantalla_height, PANTALLA, personaje_2, round_over, plataformas)
        personaje_2.movimiento(pantalla_width, pantalla_height, PANTALLA, personaje_1, round_over, plataformas)
    else:
        # Mostrar temporizador de cuenta regresiva
        draw_text(str(intro_count), count_font, 'Red', pantalla_width / 2, pantalla_height / 3)
        # Actualizar temporizador de cuenta regresiva
        if pygame.time.get_ticks() - last_count_update >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()

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
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif personaje_2.vivo == False:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        # Mostrar imagen de victoria
        PANTALLA.blit(victory_img, (360, 150))
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 3
            personaje_1 = Personaje(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMACION_PASOS, sword_fx)
            personaje_2 = Enemigo(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMACION_PASOS, magic_fx)

    # Debug: Dibujar rango de ataque del enemigo
    pintar_rango_ataque(personaje_2)
    pintar_rango_ataque(personaje_1)
    pintar_rectangulo(personaje_1)
    pintar_rectangulo(personaje_2)

    if personaje_1.rect.colliderect(personaje_2.rango_ataque) and personaje_2.vivo:
      personaje_2.ataque(personaje_1, PANTALLA)
    # Manejador de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for plataforma in plataformas:
        plataforma.pintar(PANTALLA)

    # Actualizar pantalla
    pygame.display.update()

# Salir de pygame
pygame.quit()