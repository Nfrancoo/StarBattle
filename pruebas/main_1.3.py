import pygame
from pygame import mixer
from nivel_uno.personajeNU import Personaje
from pruebas.enemigo import Enemigo
from nivel_uno.plataforma import Plataforma

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

#function for drawing text
def draw_text(text, font, text_col, x, y):
  img = font.render(text, True, text_col)
  PANTALLA.blit(img, (x, y))

#create game window
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
score = [0, 0]#player scores. [P1, P2]
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

#load background image
fondo = pygame.image.load('imagenes/69.webp')

#load spritesheets
warrior_sheet = pygame.image.load('warrior\Sprites\warrior.png')
wizard_sheet = pygame.image.load('wizard\Sprites\wizard.png')

#load vicory image
victory_img = pygame.image.load("imagenes/victory.png")

#define number of steps in each animation
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

#define font
count_font = pygame.font.Font("fonts/turok.ttf", 80)
score_font = pygame.font.Font("fonts/turok.ttf", 30)


#create two instances of fighters
personaje_1 = Personaje(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
personaje_2 = Enemigo(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)


plataformas = [
    Plataforma(200, 210, 600, 20, 'Gray'),
    Plataforma(100, 400, 200, 10, 'Gray'),
    Plataforma(700, 400, 200, 10, 'Gray')
]
#game loop
run = True
while run:

  reloj.tick(FPS)

  #draw background
  pintar_fondo()

  #show player stats
  pintar_vida_barra(personaje_1.vida, 20, 20)
  pintar_vida_barra(personaje_2.health, 580, 20)
  draw_text("P1: " + str(score[0]), score_font, 'Red', 20, 60)
  draw_text("P2: " + str(score[1]), score_font, 'Red', 580, 60)

  #update countdown
  if intro_count <= 0:
    #move fighters
    personaje_1.movimiento(pantalla_width, pantalla_height, PANTALLA, personaje_2, round_over,plataformas)
    personaje_2.move(pantalla_width, pantalla_height, PANTALLA, personaje_1, round_over)
  else:
    #display count timer
    draw_text(str(intro_count), count_font, 'Red', pantalla_width / 2, pantalla_height / 3)
    #update count timer
    if (pygame.time.get_ticks() - last_count_update) >= 1000:
      intro_count -= 1
      last_count_update = pygame.time.get_ticks()

  #update fighters
  personaje_1.update()
  personaje_2.update()

  #draw fighters
  personaje_1.draw(PANTALLA)
  personaje_2.draw(PANTALLA)


  #check for player defeat
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
      personaje_1 = Personaje(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
      personaje_2 = Enemigo(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)


  if personaje_2.alive == True:
    personaje_2.attack(PANTALLA, personaje_1)
  #event handler
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False

  for plataforma in plataformas:
    plataforma.pintar(PANTALLA)


  #update display
  pygame.display.update()

#exit pygame
pygame.quit()