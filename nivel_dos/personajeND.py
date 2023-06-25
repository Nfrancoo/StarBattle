import pygame

class Personaje():
    def __init__(self, jugador, x, y, voltear, datos, hoja_sprites, animacion_pasos):
        self.jugador = jugador
        self.tamaño = datos[0]
        self.imagen_escalada = datos[1]
        self.desplazamiento = datos[2]
        self.voltear = voltear
        self.lista_animaciones = self.cargar_imagenes(hoja_sprites, animacion_pasos)
        self.accion = 0  # 0:idle, 1:run, 2:salto, 3:attack1, 4:attack2, 5:hit, 6:death
        self.indice_frame = 0
        self.imagen = self.lista_animaciones[self.accion][self.indice_frame]
        self.tiempo_actualizacion = pygame.time.get_ticks()
        self.rect = pygame.Rect((x, y, 80, 180))
        self.velocidad_y = 0
        self.corriendo = False
        self.salto = False
        self.atacando = False
        self.tipo_ataque = 0
        self.cooldown_ataque = 0
        self.golpe = False
        self.vida = 100
        self.vivo = True
        self.rango_ataque = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.voltear), self.rect.y, 2 * self.rect.width, self.rect.height)
        self.en_plataforma = False

    def cargar_imagenes(self, hoja_sprites, animacion_pasos):
        # Extraer imágenes de la hoja de sprites
        lista_animaciones = []
        for y, animacion in enumerate(animacion_pasos):
            temp_lista_img = []
            for x in range(animacion):
                temp_img = hoja_sprites.subsurface(x * self.tamaño, y * self.tamaño, self.tamaño, self.tamaño)
                temp_lista_img.append(pygame.transform.scale(temp_img, (self.tamaño * self.imagen_escalada, self.tamaño * self.imagen_escalada)))
            lista_animaciones.append(temp_lista_img)
        return lista_animaciones

    def movimiento(self, ancho_pantalla, alto_pantalla, superficie, objetivo, ronda_terminada, plataformas):
        VELOCIDAD = 10
        GRAVEDAD = 2
        dx = 0
        dy = 0
        self.corriendo = False
        self.tipo_ataque = 0

        # Obtener las teclas presionadas
        tecla = pygame.key.get_pressed()

        # Solo puede realizar otras acciones si no está atacando actualmente
        if not self.atacando and self.vivo and not ronda_terminada:
            # Verificar los controles del jugador 1
            if self.jugador == 1:
                # Movimiento
                if tecla[pygame.K_a]:
                    dx = -VELOCIDAD
                    self.corriendo = True
                if tecla[pygame.K_d]:
                    dx = VELOCIDAD
                    self.corriendo = True
                # Salto
                if tecla[pygame.K_w] and not self.salto and not self.en_plataforma:
                    self.velocidad_y = -30
                    self.salto = True
                # Ataque
                if tecla[pygame.K_r] or tecla[pygame.K_t]:
                    self.ataque(objetivo)
                    # Determinar qué tipo de ataque se usó
                    if tecla[pygame.K_r]:
                        self.tipo_ataque = 1
                    if tecla[pygame.K_t]:
                        self.tipo_ataque = 2

        # Aplicar gravedad
        self.velocidad_y += GRAVEDAD
        dy += self.velocidad_y

        # Asegurar que el jugador se mantenga en la pantalla
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > ancho_pantalla:
            dx = ancho_pantalla - self.rect.right
        if self.rect.bottom + dy > alto_pantalla - 110:
            self.velocidad_y = 0
            self.salto = False
            dy = alto_pantalla - 110 - self.rect.bottom

        # Asegurar que los jugadores se miren entre sí
        if objetivo.rect.centerx > self.rect.centerx:
            self.voltear = False
        else:
            self.voltear = True

        # Aplicar enfriamiento de ataque
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

        # Actualizar posición del jugador
        self.rect.x += dx
        self.rect.y += dy

    # Manejar actualizaciones de animación
    def update(self):
        # Verificar qué acción está realizando el jugador
        if self.vida <= 0:
            self.vida = 0
            self.vivo = False
            self.actualizar_accion(6)  # 6 death
        elif self.golpe:
            self.actualizar_accion(5)  # 5 hit
        elif self.atacando:
            if self.tipo_ataque == 1:
                self.actualizar_accion(3)
            elif self.tipo_ataque == 2:
                self.actualizar_accion(4)
        elif self.salto:
            if self.en_plataforma:
                self.salto = False
            else:
                self.actualizar_accion(2)  # 2 salto
        elif self.corriendo:
            self.actualizar_accion(1)  # 1 correr
        else:
            self.actualizar_accion(0)  # 0 reposo
        self.rango_ataque.x = self.rect.centerx - (2 * self.rect.width * self.voltear)
        self.rango_ataque.centery = self.rect.centery

        tiempo_actualizacion_animacion = 50
        # Actualizar imagen
        self.imagen = self.lista_animaciones[self.accion][self.indice_frame]
        # Verificar si ha pasado suficiente tiempo desde la última actualización
        if pygame.time.get_ticks() - self.tiempo_actualizacion > tiempo_actualizacion_animacion:
            self.indice_frame += 1
            self.tiempo_actualizacion = pygame.time.get_ticks()
        # Verificar si la animación ha terminado
        if self.indice_frame >= len(self.lista_animaciones[self.accion]):
            # Si el jugador está muerto, finalizar la animación
            if not self.vivo:
                self.indice_frame = len(self.lista_animaciones[self.accion]) - 1
            else:
                self.indice_frame = 0
                # Verificar si se ejecutó un ataque
                if self.accion == 3 or self.accion == 4:
                    self.atacando = False
                    self.cooldown_ataque = 20
                # Verificar si se recibió daño
                if self.accion == 5:
                    self.golpe = False
                    # Si el jugador estaba en medio de un ataque, se detiene el ataque
                    self.atacando = False
                    self.cooldown_ataque = 20

    def ataque(self, objetivo):
        if self.cooldown_ataque == 0:
            # Ejecutar ataque
            self.atacando = True
            rect_ataque = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.voltear), self.rect.y,
                                      2 * self.rect.width, self.rect.height)
            if rect_ataque.colliderect(objetivo.rect):
                objetivo.vida -= 10
                objetivo.golpe = True

    def actualizar_accion(self, nueva_accion):
        # Verificar si la nueva acción es diferente a la anterior
        if nueva_accion != self.accion:
            self.accion = nueva_accion
            # Actualizar la configuración de la animación
            self.indice_frame = 0
            self.tiempo_actualizacion = pygame.time.get_ticks()

    def draw(self, superficie):
        img = pygame.transform.flip(self.imagen, self.voltear, False)
        superficie.blit(img, (self.rect.x - (self.desplazamiento[0] * self.imagen_escalada),
                              self.rect.y - (self.desplazamiento[1] * self.imagen_escalada)))