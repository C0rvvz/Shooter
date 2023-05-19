import pygame
from meteoro import Meteoro
from explosion import Explosion
from inicio import Inicio

class Juego():
    def __init__(self):
        self.puntos = 0
        self.ancho = 1332
        self.alto = 750
        self.color_negro = (0, 0, 0)
        self.color_blanco = (255, 255, 255)
        self.color_verde = (0, 255, 0)
        self.interfaz = pygame.display.set_mode((self.ancho, self.alto))
        self.tiempo = pygame.time.Clock()

        pygame.init()
        pygame.mixer.init() #Esto se utiliza para poner musica en el juego
        pygame.display.set_caption("Deep Galaxy")

        self.menu = True

        self.lista_explosion = []
        for img in range(9):
            self.archivo = "multimedia/regularExplosion0{}.png".format(img)
            self.imagen_explosion = pygame.image.load(self.archivo).convert()
            self.imagen_explosion.set_colorkey(self.color_negro)
            imagen_escala = pygame.transform.scale(self.imagen_explosion, (70,70))
            self.lista_explosion.append(imagen_escala)

        self.fondo = pygame.image.load("multimedia/espacio.jpg").convert()

        self.sonido_laser = pygame.mixer.Sound("multimedia/laser_sonido.ogg")
        self.sonido_explosion = pygame.mixer.Sound("multimedia/explosion_sonido.wav")

        self.sonido_final = pygame.mixer.Sound("multimedia/final.mp3")
        self.sonido_comienzo = pygame.mixer.Sound("multimedia/comienzo.mp3")

    def crear_meteoro(self):
        self.meteoro = Meteoro()
        self.todos_sprites.add(self.meteoro)
        self.todos_meteoros.add(self.meteoro)

    def explosion(self):
        self.explosion = Explosion(self.colicion.rect.center)
        self.todos_sprites.add(self.explosion)

    def sonido_menu(self):
        pygame.mixer.music.load("multimedia/sonido_menu.mp3")
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(loops=-1)  # queremos que se repita infinitamente, si le damos un valor positivo pues solo se repite ese numero de veces

    def sonido_juego(self):
        pygame.mixer.music.load("multimedia/sonido_juego.mp3")
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(loops=-1)



