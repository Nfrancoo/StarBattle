import pygame

class Enemigo():
    def __init__(self, player, x, y, flip, data, sprite_sheet, pasos_animacion, sound):
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
        self.sonido_ataque = sound
        self.hit = False
        self.vida = 100
        self.vivo = True
        self.attack_range = pygame.Rect(self.rect.centerx - 200, self.rect.y, 400, self.rect.height)
        self.speed_x = 5
        self.speed_y = 5

    def cargar_imagenes(self, sprite_sheet, pasos_animacion):
        lista_animaciones = []
        for y, animacion in enumerate(pasos_animacion):
            temp_img_list = []
            for x in range(animacion):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.imagen_escalada, self.size * self.imagen_escalada)))
            lista_animaciones.append(temp_img_list)
        return lista_animaciones

    def movimiento(self, screen_width, screen_height, surface, target, round_over, plataformas):
        VELOCIDAD = 10
        GRAVEDAD = 2
        dx = 0
        dy = 0
        self.corriendo = False
        self.tipo_ataque = 0
        DISTANCIA_DE_ATAQUE = 195

        distancia = target.rect.x - self.rect.x
        if self.golpeando == False and self.vivo == True and round_over == False:
            if abs(distancia) > DISTANCIA_DE_ATAQUE:
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
            if self.rect.bottom + dy > screen_height - 110:
                self.velocidad_y = 0
                self.salto = False
                dy = screen_height - 110 - self.rect.bottom

            if target.rect.centerx > self.rect.centerx:
                self.flip = False
            else:
                self.flip = True

            # Aplicar movimiento en las coordenadas del rectángulo
            self.rect.x += dx
            self.rect.y += dy

            # apply attack cooldown
            if self.cooldown_ataque > 0:
                self.cooldown_ataque -= 1

            if self.flip:
                self.tipo_ataque = 1
            else:
                self.tipo_ataque = 2

    def ataque(self, target):
        if self.rect.right >= target.rect.left and self.rect.left <= target.rect.right:
            if self.cooldown_ataque == 0:
                self.golpeando = True
                attack_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip),
                                        self.rect.y, 2 * self.rect.width, self.rect.height)
                if attack_rect.colliderect(target.rect):
                    target.vida -= 10
                    target.hit = True
                self.cooldown_ataque = 50  # Set cooldown time to 60 frames

            self.update()

    def draw(self, surface):
        img = pygame.transform.flip(self.imagen, self.flip, False)
        surface.blit(img, (self.rect.x - (self.desplazamiento[0] * self.imagen_escalada), self.rect.y - (self.desplazamiento[1] * self.imagen_escalada)))

    def update(self):
        if self.vida <= 0:
            self.vida = 0
            self.vivo = False
            self.update_accion(6)
        if self.hit:
            self.update_accion(5)
        if self.golpeando:
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
            self.frame_index = 0
            if self.accion == 3 or self.accion == 4:
                self.golpeando = False
                self.cooldown_ataque = 20
            if self.accion == 5:
                self.hit = False
                self.golpeando = False
                self.cooldown_ataque = 20

    def update_accion(self, new_accion):
        if new_accion != self.accion:
            self.accion = new_accion
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()