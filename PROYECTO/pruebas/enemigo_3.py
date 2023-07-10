import pygame

class Enemigo():
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound):
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.action = 0  # 0:idle, 1:run, 2:jump, 3:attack1, 4:attack2, 5:hit, 6:death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect(x, y, 80, 180)
        self.vel_y = 0
        self.running = False
        self.jump = False
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.attack_sound = sound
        self.hit = False
        self.health = 100
        self.alive = True
        self.attack_range = pygame.Rect(self.rect.centerx - 200, self.rect.y, 400, self.rect.height)
        self.speed_x = 5
        self.speed_y = 5

    def load_images(self, sprite_sheet, animation_steps):
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def move(self, screen_width, screen_height, surface, target, round_over):
        VELOCIDAD = 10
        GRAVEDAD = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0
        DISTANCIA_DE_ATAQUE = 195

        distancia = target.rect.x - self.rect.x
        if self.attacking == False and self.alive == True and round_over == False:
            if abs(distancia) > DISTANCIA_DE_ATAQUE:
                dx = VELOCIDAD * (distancia / abs(distancia))
                self.running = True

            # Aplicar gravedad
            self.vel_y += GRAVEDAD
            dy += self.vel_y

            # Asegurar que el enemigo permanezca en la pantalla
            if self.rect.left + dx < 0:
                dx = -self.rect.left
            if self.rect.right + dx > screen_width:
                dx = screen_width - self.rect.right
            if self.rect.bottom + dy > screen_height - 110:
                self.vel_y = 0
                self.jump = False
                dy = screen_height - 110 - self.rect.bottom

            if target.rect.centerx > self.rect.centerx:
                self.flip = False
            else:
                self.flip = True

            # Aplicar movimiento en las coordenadas del rectángulo
            self.rect.x += dx
            self.rect.y += dy

            # apply attack cooldown
            if self.attack_cooldown > 0:
                self.attack_cooldown -= 1

            if self.flip:
                self.attack_type = 1
            else:
                self.attack_type = 2
            self.attack(surface, target)

    def attack(self, surface, target):
        if self.attack_cooldown == 0:
            self.attacking = True
            attack_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip),
                                      self.rect.y, 2 * self.rect.width, self.rect.height)
            if attack_rect.colliderect(target.rect):
                target.vida -= 10
                target.hit = True
            pygame.draw.rect(surface, 'Green', attack_rect)
            self.attack_cooldown = 60  # Set cooldown time to 60 frames

        self.update()

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        surface.blit(img, (self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))

    def update(self):
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.update_action(6)
        if self.hit:
            self.update_action(5)
        if self.attacking:
            if self.attack_type == 1:
                self.update_action(3)
            elif self.attack_type == 2:
                self.update_action(4)
        elif self.jump:
            self.update_action(2)
        elif self.running:
            self.update_action(1)
        else:
            self.update_action(0)

        animation_cooldown = 50
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
            if self.action == 3 or self.action == 4:
                self.attacking = False
                self.attack_cooldown = 20
            if self.action == 5:
                self.hit = False
                self.attacking = False
                self.attack_cooldown = 20

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()