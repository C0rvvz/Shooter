import pygame
from marcador import Marcador

class Menu():
    def __init__(self):
        self.interfaz.blit(self.fondo, [0,0])
        Marcador(self.interfaz, "Deep Galaxy", 65, self.ancho // 2, self.alto // 2/3)
        Marcador(self.interfaz, "Destruye tantos meteoros como puedas", 19, self.ancho // 2, self.alto // 3)
        Marcador(self.interfaz, "Te mueves con las flechas y disparas con la barra espaciadora", 20, self.ancho // 2, self.alto // 2)
        Marcador(self.interfaz, "Presiona una tecla", 15, self.ancho // 2, self.alto * 3/4)
        pygame.display.flip()
        self.pausa = True
        while self.pausa:
            self.tiempo.tick(60)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                if evento.type == pygame.KEYDOWN:
                    self.pausa = False