import pygame

class Salud():
    def __init__(self, superficie, x, y, porcentage):
        super().__init__()
        self.barra_longitud = 100
        self.barra_altura = 10
        self.relleno = (porcentage / 100) * self.barra_longitud
        self.borde = pygame.Rect(x, y, self.barra_longitud, self.barra_altura)
        self.relleno = pygame.Rect(x, y, self.relleno, self.barra_altura)
        pygame.draw.rect(superficie, self.color_verde, self.relleno)
        pygame.draw.rect(superficie, self.color_blanco, self.borde, 2)

