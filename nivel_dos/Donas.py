import pygame, random

def crear(x, y, ancho, alto, path):
    imagen_dona = pygame.image.load(path)
    imagen_dona = pygame.transform.scale(imagen_dona,(ancho, alto))
    rectangulo = imagen_dona.get_rect()
    rectangulo.x = x
    rectangulo.y = y
    diccionario_dona = {}
    diccionario_dona['superficie'] = imagen_dona
    diccionario_dona['rectangulo'] = rectangulo
    diccionario_dona['velocidad'] = random.randrange(10, 20, 1)

    return diccionario_dona

def crear_lista_donas(cantidad):
    lista_donas = []
    for i in range(cantidad):
        x = random.randrange(0, 740, 60 )
        y = random.randrange(-1000, 0, 60)
        diccionario = crear(x, y, 60,60,'imagenes/bomba.png')
        lista_donas.append(diccionario)
    return lista_donas

def update(lista_donas):
    for dona in lista_donas:
        rect = dona['rectangulo']
        rect.y += dona['velocidad']

def actualizar_pantalla(lista_donas, personaje, ventana):
    for dona in lista_donas:
        if personaje.rect.colliderect(dona['rectangulo']):
            # personaje['puntaje'] += 100
            desaparecer_dona(dona,personaje)
        elif dona['rectangulo'].y > 800:
            desaparecer_dona(dona,personaje)

def desaparecer_dona(dona,personaje):
    dona['rectangulo'].x = random.randrange(0, 740, 60)
    dona['rectangulo'].y = random.randrange(-1000, 0, 60)
    


    
