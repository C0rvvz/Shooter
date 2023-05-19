import pygame
from juego import Juego

class Marcador():
    def __init__(self, superficie, texto, tamaño, x, y):
        super().__init__()
        self.fuente = pygame.font.SysFont("serif", tamaño)
        self.texto_superficie = self.fuente.render(texto, True, Juego(self.color_blanco))
        self.texto_rect = self.texto_superficie.get_rect()
        self.texto_rect.midtop = (x, y)
        superficie.blit(self.texto_superficie, self.texto_rect)
