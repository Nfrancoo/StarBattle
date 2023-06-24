import pygame

class Personaje():
  def __init__(self, player, x, y, flip, data, sprite_sheet, animacion_pasos):
    self.player = player
    self.tamaño = data[0]
    self.imagen_escalada = data[1]
    self.desplazamiento = data[2]
    self.flip = flip
    self.lista_animaciones = self.cargar_imagenes(sprite_sheet, animacion_pasos)
    self.accion = 0#0:idle #1:run #2:salto #3:attack1 #4: attack2 #5:hit #6:death
    self.frame_index = 0
    self.imagen = self.lista_animaciones[self.accion][self.frame_index]
    self.update_time = pygame.time.get_ticks()
    self.rect = pygame.Rect((x, y, 80, 180))
    self.velocidad_y = 0
    self.corriendo = False
    self.salto = False
    self.atacando = False
    self.tipo_ataque = 0
    self.cooldown_ataque = 0
    self.hit = False
    self.vida = 100
    self.vivo = True
    self.rango_ataque = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
    self.en_plataforma = False


  def cargar_imagenes(self, sprite_sheet, animacion_pasos):
    #extract images from spritesheet
    lista_animaciones = []
    for y, animation in enumerate(animacion_pasos):
      temp_img_list = []
      for x in range(animation):
        temp_img = sprite_sheet.subsurface(x * self.tamaño, y * self.tamaño, self.tamaño, self.tamaño)
        temp_img_list.append(pygame.transform.scale(temp_img, (self.tamaño * self.imagen_escalada, self.tamaño * self.imagen_escalada)))
      lista_animaciones.append(temp_img_list)
    return lista_animaciones


  def movimiento(self, screen_width, screen_height, surface, target, round_over,plataformas):
    VELOCIDAD = 10
    GRAVEDAD = 2
    dx = 0
    dy = 0
    self.corriendo = False
    self.tipo_ataque = 0

    #get keypresses
    key = pygame.key.get_pressed()

    #can only perform other accions if not currently atacando
    if self.atacando == False and self.vivo == True and round_over == False:
      #check player 1 controls
      if self.player == 1:
        #movement
        if key[pygame.K_a]:
          dx = -VELOCIDAD
          self.corriendo = True
        if key[pygame.K_d]:
          dx = VELOCIDAD
          self.corriendo = True
        #salto
        if key[pygame.K_w] and self.salto == False and self.en_plataforma == False:
          self.velocidad_y = -30
          self.salto = True
          # self.en_plataforma = False  # Ya no está en una plataforma
        #attack
        if key[pygame.K_r] or key[pygame.K_t]:
          self.attack(target)
          #determine which attack type was used
          if key[pygame.K_r]:
            self.tipo_ataque = 1
          if key[pygame.K_t]:
            self.tipo_ataque = 2

    #apply gravity
    self.velocidad_y += GRAVEDAD
    dy += self.velocidad_y

    #ensure player stays on screen
    if self.rect.left + dx < 0:
      dx = -self.rect.left
    if self.rect.right + dx > screen_width:
      dx = screen_width - self.rect.right
    if self.rect.bottom + dy > screen_height - 110:
      self.velocidad_y = 0
      self.salto = False
      dy = screen_height - 110 - self.rect.bottom

    #ensure players face each other
    if target.rect.centerx > self.rect.centerx:
      self.flip = False
    else:
      self.flip = True

    #apply attack cooldown
    if self.cooldown_ataque > 0:
      self.cooldown_ataque -= 1


    for plataforma in plataformas:
      if self.rect.colliderect(plataforma.rectangulo):
          # Si está colisionando y no es por la parte inferior, detener el movimiento vertical
          if self.velocidad_y > 0 and self.rect.bottom < plataforma.rectangulo.bottom:
              self.rect.bottom = plataforma.rectangulo.top
              self.velocidad_y = 0
              self.salto = False
              self.en_plataforma = True
          elif self.velocidad_y < 0:
              self.rect.top = plataforma.rectangulo.bottom
              self.velocidad_y = 0
      else:
          self.en_plataforma = False
              

    #update player position
    self.rect.x += dx
    self.rect.y += dy


  #handle animation updates
  def update(self):
    #check what accion the player is performing
    if self.vida <= 0:
      self.vida = 0
      self.vivo = False
      self.update_accion(6)#6:death
    elif self.hit == True:
      self.update_accion(5)#5:hit
    elif self.atacando == True:
      if self.tipo_ataque == 1:
        self.update_accion(3)
      elif self.tipo_ataque == 2:
        self.update_accion(4)
    elif self.salto == True:
        if self.en_plataforma == True:
            self.salto = False
        else:
          self.update_accion(2)#2:salto
    elif self.corriendo == True:
      self.update_accion(1)#1:run
    else:
      self.update_accion(0)#0:idle
    self.rango_ataque.x = self.rect.centerx - (2 * self.rect.width * self.flip)
    self.rango_ataque.centery = self.rect.centery


    animation_cooldown = 50
    #update imagen
    self.imagen = self.lista_animaciones[self.accion][self.frame_index]
    #check if enough time has passed since the last update
    if pygame.time.get_ticks() - self.update_time > animation_cooldown:
      self.frame_index += 1
      self.update_time = pygame.time.get_ticks()
    #check if the animation has finished
    if self.frame_index >= len(self.lista_animaciones[self.accion]):
      #if the player is dead then end the animation
      if self.vivo == False:
        self.frame_index = len(self.lista_animaciones[self.accion]) - 1
      else:
        self.frame_index = 0
        #check if an attack was executed
        if self.accion == 3 or self.accion == 4:
          self.atacando = False
          self.cooldown_ataque = 20
        #check if damage was taken
        if self.accion == 5:
          self.hit = False
          #if the player was in the middle of an attack, then the attack is stopped
          self.atacando = False
          self.cooldown_ataque = 20


  def attack(self, target):
    if self.cooldown_ataque == 0:
      #execute attack
      self.atacando = True     
      attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 2 * self.rect.width, self.rect.height)
      if attacking_rect.colliderect(target.rect):
        target.vida -= 10
        target.hit = True


  def update_accion(self, new_accion):
    #check if the new accion is different to the previous one
    if new_accion != self.accion:
      self.accion = new_accion
      #update the animation settings
      self.frame_index = 0
      self.update_time = pygame.time.get_ticks()

  def draw(self, surface):
    img = pygame.transform.flip(self.imagen, self.flip, False)
    surface.blit(img, (self.rect.x - (self.desplazamiento[0] * self.imagen_escalada), self.rect.y - (self.desplazamiento[1] * self.imagen_escalada)))