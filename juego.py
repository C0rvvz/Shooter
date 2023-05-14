#--------------------------------------------------------------------
#Notas:

#Acuerdense de instalar pygame

#---------------------------------------------------------------------
#Importaciones:

import pygame, random

#-----------------------------------------------------------------------
#variables globales:

puntos = 0
ancho = 800
alto = 600
color_negro = (0, 0, 0)
color_blanco = (255, 255, 255)
color_verde = (0, 255, 0)
interfaz = pygame.display.set_mode((ancho, alto))
tiempo = pygame.time.Clock()

#-----------------------------------------------------------------------
#libreria:

pygame.init()
pygame.mixer.init() #Esto se utiliza para poner musica en el juego
pygame.display.set_caption("Deep Galaxy")

#----------------------------------------------------------------------
##Notas##

#

#----------------------------------------------------------------------
#Texto en juego

def dibujar_texto(superficie, texto, tamaño, x, y):
    fuente = pygame.font.SysFont("serif", tamaño)
    texto_superficie = fuente.render(texto, True, color_blanco)
    texto_rect = texto_superficie.get_rect()
    texto_rect.midtop = (x, y)
    superficie.blit(texto_superficie, texto_rect)

def dibujar_barra_salud(superficie, x, y, porcentage):
    barra_longitud = 100
    barra_altura = 10
    relleno = (porcentage / 100) * barra_longitud
    borde = pygame.Rect(x, y, barra_longitud, barra_altura)
    relleno = pygame.Rect(x, y, relleno, barra_altura)
    pygame.draw.rect(superficie, color_verde, relleno)
    pygame.draw.rect(superficie, color_blanco, borde, 2)

#------------------------------------------------------------------
#Nave:

class Nave(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("nave.png").convert()
        self.image.set_colorkey(color_negro)
        self.rect = self.image.get_rect() #aqui se optiene la recta o el cuadro del sprite
        self.rect.centerx = ancho // 2 #aqui se pone en pantalla por asi decirlo, falta investigar mas sobre esto
        self.rect.bottom = alto - 10
        self.speed_x = 0
        self.speed_y = 0
        self.shield = 100

    def update(self):  #Movimiento
        self.speed_x = 0
        self.speed_y = 0
        tecla_presionada = pygame.key.get_pressed()
        if tecla_presionada[pygame.K_LEFT]:
            self.speed_x = -7
        if tecla_presionada[pygame.K_RIGHT]:
            self.speed_x = 7
        if tecla_presionada[pygame.K_UP]:
            self.speed_y = -7
        if tecla_presionada[pygame.K_DOWN]:
            self.speed_y = 7
        if self.rect.right > ancho:
            self.rect.right = ancho
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > alto:
            self.rect.bottom = alto
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y


    def shoot(self):
        disparo = Disparo(self.rect.centerx, self.rect.top)
        todos_sprites.add(disparo)
        todos_disparos.add(disparo)
        sonido_laser.play()


#------------------------------------------------------------------------
#Meteoros:

class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(imagenes_meteoros)
        self.image.set_colorkey(color_negro)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ancho - self.rect.width)
        self.rect.y = random.randrange(-140, -100)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-5, 5)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > alto + 10 or self.rect.left < -40or self.rect.right > ancho + 40:
            self.rect.x = random.randrange(ancho - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 10)

#-------------------------------------------------------------------------
#Disparos:

class Disparo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("laser1.png").convert()
        self.image.set_colorkey(color_negro)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

#-----------------------------------------------------------------------------
#Cargar imagenes

imagenes_meteoros = []
lista_meteoros = ["meteoro_grande1.png", "meteoro_grande2.png", "meteoro_grande3.png", "meteoro_grande4.png",
                  "meteoro_mediano1.png", "meteoro_mediano2.png", "meteoro_pequeño1.png", "meteoro_pequeño2.png",
                  "meteoro_alejandra1.png", "meteoro_alejandra2.png"]
for img in lista_meteoros:
    imagenes_meteoros.append(pygame.image.load(img).convert())

fondo = pygame.image.load("fondo.png").convert()

#---------------------------------------------------------------------------
#Sonidos

sonido_laser = pygame.mixer.Sound("laser_sonido.ogg")
sonido_explosion = pygame.mixer.Sound("explosion_sonido.wav")

pygame.mixer.music.load("music_sonido.ogg")
pygame.mixer.music.set_volume(0.4)

pygame.mixer.music.play(loops=-1) #queremos que se repita infinitamente, si le damos un valor positivo pues solo se repite ese numero de veces

#--------------------------------------------------------------------------
#Grupos de objetos movibles

todos_sprites = pygame.sprite.Group()
todos_meteoros = pygame.sprite.Group()
todos_disparos = pygame.sprite.Group()

#----------------------------------------------------------------------
#Variables

nave = Nave()
todos_sprites.add(nave)

#----------------------------------------------------------------------
#Cantidad de meteoros

def crear_meteoro():
    meteoro = Meteor()
    todos_sprites.add(meteoro)
    todos_meteoros.add(meteoro)

for i in range(8):
    crear_meteoro()

#----------------------------------------------------------------------
# Bucle principal

fps = True
while fps:
    tiempo.tick(60) #Estos son los frames por segundo
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            fps = False

        elif  evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                nave.shoot()

    todos_sprites.update()

    coliciones = pygame.sprite.groupcollide(todos_meteoros, todos_disparos, True, True) #Esto mira si hay colisiones entre laser y meteoros
    for colicion in coliciones:
        puntos += 10
        crear_meteoro()
        sonido_explosion.play()

    coliciones = pygame.sprite.spritecollide(nave, todos_meteoros, True) #Esto mira si hay colisiones en el jugador y meteoros
    for colicion in coliciones:
        nave.shield -= 25
        crear_meteoro()
        if nave.shield <= 0:
            fps = False
        sonido_explosion.play()


    interfaz.blit(fondo, [0 , 0]) #Es un método que se utiliza para rellenar la superficie de la ventana de visualización del juego con un color específico o fondo si es este caso se le dara una posicion.

    todos_sprites.draw(interfaz)

    dibujar_texto(interfaz, str(puntos), 25, ancho // 2, 10) #Marcador

    dibujar_barra_salud(interfaz, 5, 5, nave.shield) #Coordenadas 5,5 y porcetange es nave.shield

    pygame.display.flip() #Este metodo se utiliza para actualizar la ventana de visualización del juego

pygame.quit() #Este método se utiliza para cerrar y liberar todos los recursos utilizados por la biblioteca Pygame

#--------------------------------------------------------------