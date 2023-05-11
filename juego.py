#--------------------------------------------------------------------
#Notas:

#Acuerdense de instalar pygame

#---------------------------------------------------------------------
#Importaciones:

import pygame, random

#-----------------------------------------------------------------------
#Estadares para la interfaz:

#Falta buscar mas sobre como crearemos la interfaz

WIDTH = 800
HEIGTH = 600
color_negro = (0, 0, 0)
color_blanco = (255, 255, 255)

#-----------------------------------------------------------------------
#Variables globales:

pygame.init()
pygame.mixer.init() #Esto se utiliza para poner musica en el juego
interfaz = pygame.display.set_mode((WIDTH, HEIGTH))
pygame.display.set_caption("Call Of Dutty")
tiempo = pygame.time.Clock()

#----------------------------------------------------------------------
##Clases##

#falta buscar las imagenes para el juego

#----------------------------------------------------------------------
#Nave\Jugador:

#Falta buscar sobre como mover la nave

class Nave(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("player.png").convert()
        self.image.set_colorkey(color_negro)
        self.rect = self.image.get_rect() #aqui se optiene la recta o el cuadro del sprite
        self.rect.centerx = WIDTH // 2 #aqui se pone en pantalla por asi decirlo, falta investigar mas sobre esto
        self.rect.bottom = HEIGTH - 10
        self.speed_x = 0
        self.speed_y = 0

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
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGTH:
            self.rect.bottom = HEIGTH
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y


    def disparo(self):
        pass


#------------------------------------------------------------------------
#Meteoros:

#

class Meteoro(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

    def movimiento(self):
        pass

#-------------------------------------------------------------------------
#Disparos:

#

class Disparo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()


# --------------------------------------------------------------------------

#Variables

todos_sprites = pygame.sprite.Group()

nave = Nave()
todos_sprites.add(nave)

# Bucle principal

fps = True
while fps:
    tiempo.tick(60) #Estos son los frames por segundo
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            fps = False

    todos_sprites.update()

    interfaz.fill(color_negro) #Es un método que se utiliza para rellenar la superficie de la ventana
                               # de visualización del juego con un color específico.

    todos_sprites.draw(interfaz)

    pygame.display.flip() #Este metodo se utiliza para actualizar la ventana de
                          # visualización del juego

pygame.quit() #Este método se utiliza para cerrar y liberar todos los recursos utilizados
              # por la biblioteca Pygam