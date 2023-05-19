import pygame

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = self.lista_explosion[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0 #Es la que aumenta pa que cambie la imagen, es decir cuando fps sea 1, la imagen sera 1 y asi
        self.last_update = pygame.time.get_ticks() #Pausa el juego de alguna manera para nosotros poder ver los cambios que se estan realizando/cuanto tiempo a transcurrido cuando se esta iniciando
        self.frame_rate = 50 #Velocidad de la explosion

    def update(self):
        now = pygame.time.get_ticks() #Cuanto tiempo a transcurrido cuando se crea la ecplosion
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.lista_explosion):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.lista_explosion[self.frame] #Va iterando entre la lista
                self.rect = self.image.get_rect() #Marco de la imagen
                self.rect.center = center #Centra la imagen
