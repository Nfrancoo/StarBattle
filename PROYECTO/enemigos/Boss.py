import pygame
from extra_niveles.proyectil import Proyectil

class Boss():
    def __init__(self, x, y, flip, data, sprite_sheet, pasos_animacion, sonido):
        self.size = data[0]
        self.imagen_escalada = data[1]
        self.desplazamiento = data[2]
        self.flip = flip
        self.lista_animaciones = self.cargar_imagenes(sprite_sheet, pasos_animacion)
        self.accion = 0  # 0:idle, 1:run, 2:salto, 3:attack1, 4:attack2, 5:hit, 6:death
        self.frame_index = 0
        self.imagen = self.lista_animaciones[self.accion][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect(x, y, 80, 180)
        self.velocidad_y = 0
        self.corriendo = False
        self.salto = False
        self.golpeando = False
        self.tipo_ataque = 0
        self.cooldown_ataque = 0
        self.hit = False
        self.vida = 100
        self.vivo = True
        self.rango_ataque = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip), self.rect.y, 3 * self.rect.width, self.rect.height)
        self.puede_saltar = True
        self.proyectiles = pygame.sprite.Group()  # Grupo de proyectiles
        self.proyectil_cooldown = 500  # Tiempo de espera entre disparos (en milisegundos)
        self.last_proyectil_time = pygame.time.get_ticks()  # Tiempo del último disparo
        self.sonido_ataque = sonido

    def cargar_imagenes(self, sprite_sheet, animacion_pasos):
        #extraer imagenes del spritesheet
        lista_animaciones = []
        for y, animation in enumerate(animacion_pasos):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size* self.imagen_escalada, self.size * self.imagen_escalada)))
            lista_animaciones.append(temp_img_list)
        return lista_animaciones

    def movimiento(self, screen_width, screen_height, surface, target, round_over, plataformas):
        VELOCIDAD = 10
        GRAVEDAD = 2
        dx = 0
        dy = 0
        self.corriendo = False
        self.tipo_ataque = 0
        DISTANCIA_ENTRE_TARGET = 165
        distancia = target.rect.x - self.rect.x
        img = pygame.transform.flip(self.imagen, self.flip, False)

        if self.golpeando == False and self.vivo == True and round_over == False:
            if abs(distancia) > DISTANCIA_ENTRE_TARGET:
                dx = VELOCIDAD * (distancia / abs(distancia))
                self.corriendo = True

            # Aplicar gravedad
            self.velocidad_y += GRAVEDAD
            dy += self.velocidad_y

            # Asegurar que el enemigo permanezca en la pantalla
            if self.rect.left + dx < 0:
                dx = -self.rect.left
            if self.rect.right + dx > screen_width:
                dx = screen_width - self.rect.right
                if self.golpeando:
                    self.golpeando = False
            if self.rect.bottom + dy > screen_height - 110:
                self.velocidad_y = 0
                self.salto = False
                dy = screen_height - 110 - self.rect.bottom
                self.puede_saltar = True  # Permitir saltar nuevamente

            if target.rect.centerx > self.rect.centerx:
                self.flip = False
            else:
                self.flip = True

            if self.salto and self.rect.y > -30:
                surface.blit(img, (self.rect.x - (self.desplazamiento[0] * self.imagen_escalada),
                   self.rect.y - self.desplazamiento[1] * self.imagen_escalada - self.velocidad_y))
            # Aplicar movimiento en las coordenadas del rectángulo
            self.rect.x += dx
            self.rect.y += dy
            self.rango_ataque.center = self.rect.center

            # Lógica de salto
            if target.salto and self.velocidad_y == 0 and self.puede_saltar:
                self.velocidad_y = -30
                self.salto = True
                self.puede_saltar = False  # No permitir saltar nuevamente

            for plataforma in plataformas:
                if self.rect.colliderect(plataforma.rectangulo):
                    # Si está colisionando, detener el movimiento vertical y ajustar la posición
                    if self.velocidad_y > 0:
                        self.rect.bottom = plataforma.rectangulo.top
                        self.velocidad_y = 0
                        self.salto = False
                        self.puede_saltar = True  # Permitir saltar nuevamente
                    elif self.velocidad_y < 0:
                        self.rect.top = plataforma.rectangulo.bottom
                        self.velocidad_y = 0
                        
            # Aplicar cooldown al ataque
            if self.cooldown_ataque > 0:
                self.cooldown_ataque -= 1

            if self.flip:
                self.tipo_ataque = 1
            else:
                self.tipo_ataque = 2

            for proyectil in self.proyectiles:
                if proyectil.rect.colliderect(target.rect):
                    target.vida -= 70
                    self.proyectiles.remove(proyectil)
                    
            self.proyectiles.update(screen_width)
            self.proyectiles.draw(surface)

    def ataque(self, target):
        if self.salto:
            return  # Si el enemigo está saltando, no puede atacar

        current_time = pygame.time.get_ticks()
        if current_time - self.last_proyectil_time > self.proyectil_cooldown:
            self.golpeando = True
            proyectil = Proyectil(self.rect.centerx, self.rect.centery, self.flip)
            self.proyectiles.add(proyectil)
            self.last_proyectil_time = current_time

        if self.cooldown_ataque == 0:
            self.golpeando = True
            self.sonido_ataque.play()
            attack_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip),
                                      self.rect.y, 2 * self.rect.width, self.rect.height)
            if attack_rect.colliderect(target.rect):
                target.vida -= 10
                target.hit = True
            self.cooldown_ataque = 60  # Set cooldown time to 60 frames

        self.update()


    def draw(self, surface):
        img = pygame.transform.flip(self.imagen, self.flip, False)
        surface.blit(img, (self.rect.x - self.desplazamiento[0] * self.imagen_escalada,
                   self.rect.y - self.desplazamiento[1] * self.imagen_escalada))

    def update(self):
        if self.vida <= 0:
            self.vida = 0
            self.vivo = False
            self.update_accion(6)
        elif self.hit:
            self.update_accion(5)
        elif self.golpeando:
            if self.tipo_ataque == 1:
                self.update_accion(3)
            elif self.tipo_ataque == 2:
                self.update_accion(4)
        elif self.salto:
            self.update_accion(2)
        elif self.corriendo:
            self.update_accion(1)
        else:
            self.update_accion(0)

        animation_cooldown = 50
        self.imagen = self.lista_animaciones[self.accion][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

        if self.cooldown_ataque > 0:
            self.cooldown_ataque -= 1
        if self.frame_index >= len(self.lista_animaciones[self.accion]):
            if self.vivo == False:
                self.frame_index = len(self.lista_animaciones[self.accion]) - 1
            else:
                self.frame_index = 0
                if self.accion == 3 or self.accion == 4:
                    self.golpeando = False
                    self.cooldown_ataque = 50
                elif self.accion == 5:
                    self.hit = False
                    self.golpeando = False
                    self.cooldown_ataque = 50

    def update_accion(self, new_accion):
        if new_accion != self.accion:
            self.accion = new_accion
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()