import pygame
import math

class Enemigo():
    def __init__(self, player, x, y, flip, data, sprite_sheet, animacion_pasos, sound):
        self.player = player
        self.tamaño = data[0]
        self.imagen_escalada = data[1]
        self.desplazamiento = data[2]
        self.flip = flip
        self.lista_animaciones = self.cargar_imagenes(sprite_sheet, animacion_pasos)
        self.accion = 0  # 0:idle #1:run #2:salto #3:attack1 #4: attack2 #5:hit #6:death
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
        self.sonido_ataque = sound
        self.hit = False
        self.vida = 100
        self.vivo = True

    def cargar_imagenes(self, sprite_sheet, animacion_pasos):
        # Extract images from spritesheet
        lista_animaciones = []
        for y, animation in enumerate(animacion_pasos):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(
                    x * self.tamaño, y * self.tamaño, self.tamaño, self.tamaño
                )
                temp_img_list.append(
                    pygame.transform.scale(
                        temp_img,
                        (self.tamaño * self.imagen_escalada, self.tamaño * self.imagen_escalada),
                    )
                )
            lista_animaciones.append(temp_img_list)
        return lista_animaciones

    def movimiento(self, screen_width, screen_height, surface, target, round_over, plataformas):
        VELOCIDAD = 5  # Ajusta la velocidad del enemigo según tus necesidades
        GRAVEDAD = 2
        dx = 0
        dy = 0
        self.corriendo = False
        self.tipo_ataque = 0

        # Calcula la dirección hacia el personaje
        direction_x = target.rect.centerx - self.rect.centerx
        direction_y = target.rect.centery - self.rect.centery
        distance = math.sqrt(direction_x ** 2 + direction_y ** 2)

        # Normaliza la dirección
        if distance != 0:
            direction_x /= distance
            direction_y /= distance

        # Calcula el desplazamiento del enemigo según la dirección y la velocidad
        dx = direction_x * VELOCIDAD
        dy = direction_y * VELOCIDAD

        # Aplica la gravedad
        self.velocidad_y += GRAVEDAD
        dy += self.velocidad_y

        # Ensure player stays on screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > screen_width:
            dx = screen_width - self.rect.right
        if self.rect.bottom + dy > screen_height - 110:
            self.velocidad_y = 0
            self.salto = False
            dy = screen_height - 110 - self.rect.bottom

        # Ensure players face each other
        if target.rect.centerx > self.rect.centerx:
            self.flip = False
        else:
            self.flip = True

        # Apply attack cooldown
        if self.cooldown_ataque > 0:
            self.cooldown_ataque -= 1

        for plataforma in plataformas:
            if self.rect.colliderect(plataforma.rectangulo):
                # Si está colisionando, detener el movimiento vertical y ajustar la posición
                if self.velocidad_y > 0:
                    self.rect.bottom = plataforma.rectangulo.top
                    self.velocidad_y = 0
                    self.salto = False
                elif self.velocidad_y < 0:
                    self.rect.top = plataforma.rectangulo.bottom
                    self.velocidad_y = 0

        # Update player position
        self.rect.x += dx
        self.rect.y += dy

    # Handle animation updates
    def update(self):
        # Check what accion the player is performing
        if self.vida <= 0:
            self.vida = 0
            self.vivo = False
            self.update_accion(6)  # 6:death
        elif self.hit == True:
            self.update_accion(5)  # 5:hit
        elif self.atacando == True:
            if self.tipo_ataque == 1:
                self.update_accion(3)  # 3:attack1
            elif self.tipo_ataque == 2:
                self.update_accion(4)  # 4:attack2
        elif self.salto == True:
            self.update_accion(2)  # 2:salto
        elif self.corriendo == True:
            self.update_accion(1)  # 1:run
        else:
            self.update_accion(0)  # 0:idle

        animation_cooldown = 50
        # Update imagen
        self.imagen = self.lista_animaciones[self.accion][self.frame_index]
        # Check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        # Check if the animation has finished
        if self.frame_index >= len(self.lista_animaciones[self.accion]):
            # If the player is dead then end the animation
            if self.vivo == False:
                self.frame_index = len(self.lista_animaciones[self.accion]) - 1
            else:
                self.frame_index = 0
                # Check if an attack was executed
                if self.accion == 3 or self.accion == 4:
                    self.atacando = False
                    self.cooldown_ataque = 20
                # Check if damage was taken
                if self.accion == 5:
                    self.hit = False
                    # If the player was in the middle of an attack, then the attack is stopped
                    self.atacando = False
                    self.cooldown_ataque = 20

    def attack(self, target):
        if self.cooldown_ataque == 0:
            # Execute attack
            self.atacando = True
            self.sonido_ataque.play()
            attacking_rect = pygame.Rect(
                self.rect.centerx - (2 * self.rect.width * self.flip),
                self.rect.y,
                2 * self.rect.width,
                self.rect.height,
            )
            if attacking_rect.colliderect(target.rect):
                target.vida -= 10
                target.hit = True

    def update_accion(self, new_accion):
        # Verifica si la nueva acción es diferente a la acción anterior
        if new_accion != self.accion:
            self.accion = new_accion
            # Actualiza la animación y el tiempo de actualización
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

            # Si la nueva acción es "correr", establece el estado de corriendo como verdadero
            if self.accion == 1:
                self.corriendo = True
            else:
                self.corriendo = False

    def draw(self, surface):
        img = pygame.transform.flip(
            self.imagen, self.flip, False
        )
        surface.blit(
            img,
            (
                self.rect.x - (self.desplazamiento[0] * self.imagen_escalada),
                self.rect.y - (self.desplazamiento[1] * self.imagen_escalada),
            ),
        )