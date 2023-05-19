import pygame
from disparo import Disparo
class Nave(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("multimedia/nave.png").convert()
        self.image.set_colorkey(self.color_negro)
        self.rect = self.image.get_rect() #aqui se optiene la recta o el cuadro del sprite
        self.rect.centerx = self.ancho // 2 #aqui se pone en pantalla por asi decirlo, falta investigar mas sobre esto
        self.rect.bottom = self.alto - 10
        self.speed_x = 0
        self.speed_y = 0
        self.shield = 100

    def update(self):  #Movimiento
        self.speed_x = 0
        self.speed_y = 0
        tecla_presionada = pygame.key.get_pressed()
        if tecla_presionada[pygame.K_LEFT]:
            self.speed_x = -10
        if tecla_presionada[pygame.K_RIGHT]:
            self.speed_x = 10
        if tecla_presionada[pygame.K_UP]:
            self.speed_y = -10
        if tecla_presionada[pygame.K_DOWN]:
            self.speed_y = 10
        if self.rect.right > self.ancho:
            self.rect.right = self.ancho
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.alto:
            self.rect.bottom = self.alto
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def shoot(self):
        self.disparo = Disparo(self.rect.centerx, self.rect.top)
        self.todos_sprites.add(self.disparo)
        self.todos_disparos.add(self.disparo)
        self.sonido_laser.play()