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
        self.vida = 100
        self.alive = True
        self.attack_range = pygame.Rect(self.rect.centerx - 200, self.rect.y, 400, self.rect.height)
        self.speed_x = 5
        self.speed_y = 5
        self.distance = 0

    def load_images(self, sprite_sheet, animation_steps):
        animation_list = []
        for y, animation in enumerate(animation_steps):
            temp_img_list = []
            for x in range(animation):
                temp_img = sprite_sheet.subsurface(x * self.size, y * self.size, self.size, self.size)
                temp_img_list.append(pygame.transform.scale(temp_img, (self.size * self.image_scale, self.size * self.image_scale)))
            animation_list.append(temp_img_list)
        return animation_list

    def move(self, screen_width, screen_height, surface, target, plataformas):

        
        if not self.attack_range.colliderect(target.rect):
            # Move towards target (fighter_2) on the x-axis
            if self.rect.centerx < target.rect.centerx:
                self.direction_x = 1
                self.flip = False
            else:
                self.direction_x = -1
                self.flip = True
            self.rect.x += self.speed_x * self.direction_x
            self.running = True

            for plataforma in plataformas:
                if self.rect.colliderect(plataforma.rectangulo):
                    # Si está colisionando, detener el movimiento vertical y ajustar la posición
                    if self.vel_y > 0:
                        self.rect.bottom = plataforma.rect.top
                        self.vel_y = 0
                        self.jump = False
                    elif self.vel_y < 0:
                        self.rect.top = plataforma.rect.bottom
                        self.vel_y = 0
            
            # Move towards target (fighter_2) on the y-axis
            if self.rect.centery < target.rect.centery:
                self.direction_y = 1
            else:
                self.direction_y = -1
            self.rect.y += self.speed_y * self.direction_y
        else:
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
        if self.vida <= 0:
            self.vida = 0
            self.alive = False
            self.update_action(6)
        if self.hit:
            self.update_action(5)
        if self.attacking:
            if self.attack_type == 1:
                self.update_action(3)
            elif self.attack_type == 2:
                self.update_action(4)
            if self.frame_index == len(self.animation_list[self.action]) - 1:
                self.attacking = False
                self.attack_cooldown = 20
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
            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            if self.action != 3 and self.action != 4:  # No reiniciar frame_index para animaciones de ataque
                self.frame_index = 0
            self.update_time = pygame.time.get_ticks()