import pygame, random

class Meteoro(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(self.imagenes_meteoros)
        self.image.set_colorkey(self.color_negro)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(self.ancho - self.rect.width)
        self.rect.y = random.randrange(-140, -100)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-5, 5)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > self.alto + 10 or self.rect.left < -40 or self.rect.right > self.ancho + 40:
            self.rect.x = random.randrange(self.ancho - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 10)

    def multimedia(self):
        self.imagenes_meteoros = []
        self.lista_meteoros = ["multimedia/meteoro_grande1.png", "multimedia/meteoro_grande2.png",
                          "multimedia/meteoro_grande3.png", "multimedia/meteoro_grande4.png",
                          "multimedia/meteoro_mediano1.png", "multimedia/meteoro_mediano2.png",
                          "multimedia/meteoro_pequeño1.png", "multimedia/meteoro_pequeño2.png",
                          "multimedia/meteoro_alejandra1.png", "multimedia/meteoro_alejandra2.png"]
        for img in self.lista_meteoros:
            self.imagenes_meteoros.append(pygame.image.load(img).convert())
