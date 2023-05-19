import pygame
from nave import Nave
from marcador import Marcador
from salud import Salud
from menu import Menu

class Inicio():
    def __init__(self):
        self.fps = True
        while self.fps:
            if self.menu:

                self.sonido_menu()
                Menu()

                self.menu = False
                pygame.mixer.music.stop()
                self.sonido_comienzo.play()
                self.sonido_juego()

                self.todos_sprites = pygame.sprite.Group()
                self.todos_meteoros = pygame.sprite.Group()
                self.todos_disparos = pygame.sprite.Group()

                self.nave = Nave()
                self.todos_sprites.add(self.nave)

                for i in range(15):
                    self.crear_meteoro()

            self.tiempo.tick(60)  # Estos son los frames por segundo
            for self.evento in pygame.event.get():
                if self.evento.type == pygame.QUIT:
                    self.fps = False

                elif self.evento.type == pygame.KEYDOWN:
                    if self.evento.key == pygame.K_SPACE:
                        self.nave.shoot()

            self.todos_sprites.update()

            self.coliciones = pygame.sprite.groupcollide(self.todos_meteoros, self.todos_disparos, True, True)  # Esto mira si hay colisiones entre laser y meteoros
            for self.colicion in self.coliciones:
                self.explosion()
                self.puntos += 10
                self.numeros = [500, 1000, 1500, 2000]
                for self.numero in self.numeros:
                    if self.puntos == self.numero:
                        self.cantidad = + 30
                        for i in range(self.cantidad):
                            self.crear_meteoro()
                self.crear_meteoro()
                self.sonido_explosion.play()

            self.coliciones = pygame.sprite.spritecollide(self.nave, self.todos_meteoros, True)  # Esto mira si hay colisiones en el jugador y meteoros
            for self.colicion in self.coliciones:
                self.nave.shield -= 25
                self.crear_meteoro()
                self.explosion()
                self.sonido_explosion.play()
                if self.nave.shield <= 0:
                    menu = True
                    self.sonido_final.play()
                    pygame.mixer.music.stop()
                    self.sonido_menu()
                    self.puntos = 0

            self.interfaz.blit(self.fondo, [0,0])  # Es un método que se utiliza para rellenar la superficie de la ventana de visualización del juego con un color específico o fondo si es este caso se le dara una posicion.

            self.todos_sprites.draw(self.interfaz)

            Marcador(self.interfaz, str(self.puntos), 25, self.ancho // 1.8, 10)  # Marcador
            Marcador(self.interfaz, str("Puntos:"), 25, self.ancho // 2, 10)

            Salud(self.interfaz, 5, 5, self.nave.shield)  # Coordenadas 5,5 y porcetange es nave.shield

            pygame.display.flip()  # Este metodo se utiliza para actualizar la ventana de visualización del juego

        pygame.quit()  # Este método se utiliza para cerrar y liberar todos los recursos utilizados por la biblioteca Pygame