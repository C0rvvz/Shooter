#--------------------------------------------------------------------
#Notas:

#Acuerdense de instalar pygame

#---------------------------------------------------------------------
#Importaciones:

#

import pygame

#-----------------------------------------------------------------------
#Estadares para la interfaz:

#Falta buscar mas sobre como crearemos la interfaz

diametro_anchura = 1000
diametro_altura = 500
color_negro = (0, 0, 0)
color_blango = (255, 255, 255)

interfaz = pygame.display.set_mode(diametro_anchura, diametro_altura)

#-----------------------------------------------------------------------
#Variables globales:

#

pygame.init()

#----------------------------------------------------------------------
##Clases##

#falta buscar las imagenes para el juego

#----------------------------------------------------------------------
#Nave\Jugador:

#Falta buscar sobre como mover la nave

class Nave(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.imagen = pygame.imagen.load("aqui ira la imagen de la nave").convert()
        self.rect= self.rect.imagen.get_rect() #aqui se optiene la recta o el cuadro del sprite
        self.rect.centrox = diametro_anchura // 2 #aqui se pone en pantalla por asi decirlo, falta investigar mas sobre esto
        self.rect.abajo = diametro_altura - 10
        self.movimiento_en_x = 0

    def movimiento(self):
        pass

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
