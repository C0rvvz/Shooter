#--------------------------------------------------------------------
#Notas:

#Acuerdense de instalar pygame

#---------------------------------------------------------------------
#Importaciones:

#

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
interfaz = pygame.display.set_mode(WIDTH, HEIGTH)
pygame.display.set_caption("Call Of Dutty")
tiempo = pygame.time.Clock()

#----------------------------------------------------------------------
##Clases##

#falta buscar las imagenes para el juego

#----------------------------------------------------------------------
#Nave\Jugador:

#Falta buscar sobre como mover la nave

class Nave(pygame.sprite.Sprite):
    def _init_(self):
        super()._init_()
        self.imagen = pygame.imagen.load("aqui ira la imagen de la nave").convert()
        self.rect= self.rect.imagen.get_rect() #aqui se optiene la recta o el cuadro del sprite
        self.rect.centrox = WIDTH // 2 #aqui se pone en pantalla por asi decirlo, falta investigar mas sobre esto
        self.rect.abajo = HEIGTH - 10
        self.movimiento_en_x = 0

    def movimiento(self):
        self.velocidad_x = 0
        tecla_presionada = pygame.key.get_pressed()
        if tecla_presionada[pygame.K_LEFT]:
            self.speed_x = -5
        if tecla_presionada[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x


    def disparo(self):
        pass


#------------------------------------------------------------------------
#Meteoros:

#

class Meteoro(pygame.sprite.Sprite):
    def _init_(self):
        super()._init_()

    def movimiento(self):
        pass

#-------------------------------------------------------------------------
#Disparos:

#

class Disparo(pygame.sprite.Sprite):
    def _init_(self):
        super()._init_()


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

    pygame.display.flip() #Este metodo se utiliza para actualizar la ventana de
                          # visualización del juego

pygame.quit() #Este método se utiliza para cerrar y liberar todos los recursos utilizados
              # por la biblioteca Pygam