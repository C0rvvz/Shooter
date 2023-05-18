#--------------------------------------------------------------------
#Notas:

#Acuerdense de instalar pygame

#---------------------------------------------------------------------
#Importaciones:

import pygame, random

#-----------------------------------------------------------------------
#variables globales:

puntos = 0
ancho = 1332
alto = 750
color_negro = (0, 0, 0)
color_blanco = (255, 255, 255)
color_verde = (0, 255, 0)
interfaz = pygame.display.set_mode((ancho, alto))
tiempo = pygame.time.Clock()

#-----------------------------------------------------------------------
#libreria:

pygame.init()
pygame.mixer.init() #Esto se utiliza para poner musica en el juego
pygame.display.set_caption("Deep Galaxy")

#----------------------------------------------------------------------
#Marcador

class Marcador():
    def __init__(self, superficie, texto, tamaño, x, y):
        super().__init__()
        fuente = pygame.font.SysFont("serif", tamaño)
        texto_superficie = fuente.render(texto, True, color_blanco)
        texto_rect = texto_superficie.get_rect()
        texto_rect.midtop = (x, y)
        superficie.blit(texto_superficie, texto_rect)

#_-------------------------------------------------------------------------
#Salud

class Salud():

    def __init__(self, superficie, x, y, porcentage):
        super().__init__()
        barra_longitud = 100
        barra_altura = 10
        relleno = (porcentage / 100) * barra_longitud
        borde = pygame.Rect(x, y, barra_longitud, barra_altura)
        relleno = pygame.Rect(x, y, relleno, barra_altura)
        pygame.draw.rect(superficie, color_verde, relleno)
        pygame.draw.rect(superficie, color_blanco, borde, 2)

#------------------------------------------------------------------
#Nave:

class Nave(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("multimedia/nave.png").convert()
        self.image.set_colorkey(color_negro)
        self.rect = self.image.get_rect() #aqui se optiene la recta o el cuadro del sprite
        self.rect.centerx = ancho // 2 #aqui se pone en pantalla por asi decirlo, falta investigar mas sobre esto
        self.rect.bottom = alto - 10
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
        if self.rect.right > ancho:
            self.rect.right = ancho
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > alto:
            self.rect.bottom = alto
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y


    def shoot(self):
        disparo = Disparo(self.rect.centerx, self.rect.top)
        todos_sprites.add(disparo)
        todos_disparos.add(disparo)
        sonido_laser.play()


#------------------------------------------------------------------------
#Disparos:

class Disparo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("multimedia/laser1.png").convert()
        self.image.set_colorkey(color_negro)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

#-------------------------------------------------------------------------
#Meteoros:

class Meteoro(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(imagenes_meteoros)
        self.image.set_colorkey(color_negro)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ancho - self.rect.width)
        self.rect.y = random.randrange(-140, -100)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-5, 5)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > alto + 10 or self.rect.left < -40or self.rect.right > ancho + 40:
            self.rect.x = random.randrange(ancho - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 10)
def crear_meteoro():
    meteoro = Meteoro()
    todos_sprites.add(meteoro)
    todos_meteoros.add(meteoro)

#----------------------------------------------------------------------------
#Explosion

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = lista_explosion[0]
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
            if self.frame == len(lista_explosion):
                self.kill()
            else:
                center = self.rect.center
                self.image = lista_explosion[self.frame] #Va iterando entre la lista
                self.rect = self.image.get_rect() #Marco de la imagen
                self.rect.center = center #Centra la imagen

def explosion():
    explosion = Explosion(colicion.rect.center)
    todos_sprites.add(explosion)

#--------------------------------------------------------------------
#Funcion menu
class Menu():
    def __init__(self):
        interfaz.blit(fondo, [0,0])
        Marcador(interfaz, "Deep Galaxy", 65, ancho // 2, alto // 2/3)
        Marcador(interfaz, "Destruye tantos meteoros como puedas", 19, ancho // 2, alto // 3)
        Marcador(interfaz, "Te mueves con las flechas y disparas con la barra espaciadora", 20, ancho // 2, alto // 2)
        Marcador(interfaz, "Presiona una tecla", 15, ancho // 2, alto * 3/4)
        pygame.display.flip()
        pausa = True
        while pausa:
            tiempo.tick(60)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                if evento.type == pygame.KEYDOWN:
                    pausa = False
menu = True

#-----------------------------------------------------------------------------
#Cargar imagenes



imagenes_meteoros = []
lista_meteoros = ["multimedia/meteoro_grande1.png", "multimedia/meteoro_grande2.png", "multimedia/meteoro_grande3.png", "multimedia/meteoro_grande4.png",
                  "multimedia/meteoro_mediano1.png", "multimedia/meteoro_mediano2.png", "multimedia/meteoro_pequeño1.png", "multimedia/meteoro_pequeño2.png",
                  "multimedia/meteoro_alejandra1.png", "multimedia/meteoro_alejandra2.png"]
for img in lista_meteoros:
    imagenes_meteoros.append(pygame.image.load(img).convert())

lista_explosion = []
for img in range(9):
    archivo = "multimedia/regularExplosion0{}.png".format(img)
    imagen_explosion = pygame.image.load(archivo).convert()
    imagen_explosion.set_colorkey(color_negro)
    imagen_escala = pygame.transform.scale(imagen_explosion, (70,70))
    lista_explosion.append(imagen_escala)

fondo = pygame.image.load("multimedia/espacio.jpg").convert()

#---------------------------------------------------------------------------
#Sonidos

sonido_laser = pygame.mixer.Sound("multimedia/laser_sonido.ogg")
sonido_explosion = pygame.mixer.Sound("multimedia/explosion_sonido.wav")

sonido_final = pygame.mixer.Sound("multimedia/final.mp3")
sonido_comienzo = pygame.mixer.Sound("multimedia/comienzo.mp3")


def sonido_menu():
    pygame.mixer.music.load("multimedia/sonido_menu.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(loops=-1)  # queremos que se repita infinitamente, si le damos un valor positivo pues solo se repite ese numero de veces

def sonido_juego():
    pygame.mixer.music.load("multimedia/sonido_juego.mp3")
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(loops=-1)

#----------------------------------------------------------------------
# Bucle principal

fps = True
while fps:
    if menu:

        sonido_menu()
        Menu()

        menu = False
        pygame.mixer.music.stop()
        sonido_comienzo.play()
        sonido_juego()

        todos_sprites = pygame.sprite.Group()
        todos_meteoros = pygame.sprite.Group()
        todos_disparos = pygame.sprite.Group()

        nave = Nave()
        todos_sprites.add(nave)

        for i in range(15):
            crear_meteoro()

    tiempo.tick(60) #Estos son los frames por segundo
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            fps = False

        elif  evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                nave.shoot()

    todos_sprites.update()

    coliciones = pygame.sprite.groupcollide(todos_meteoros, todos_disparos, True, True) #Esto mira si hay colisiones entre laser y meteoros
    for colicion in coliciones:
        explosion()
        puntos += 10
        numeros = [500, 1000, 1500, 2000]
        for numero in numeros:
            if puntos == numero:
                cantidad =+ 30
                for i in range(cantidad):
                    crear_meteoro()
        crear_meteoro()
        sonido_explosion.play()

    coliciones = pygame.sprite.spritecollide(nave, todos_meteoros, True) #Esto mira si hay colisiones en el jugador y meteoros
    for colicion in coliciones:
        nave.shield -= 25
        crear_meteoro()
        explosion()
        sonido_explosion.play()
        if nave.shield <= 0:
            menu = True
            sonido_final.play()
            pygame.mixer.music.stop()
            sonido_menu()
            puntos = 0

    interfaz.blit(fondo, [0 , 0]) #Es un método que se utiliza para rellenar la superficie de la ventana de visualización del juego con un color específico o fondo si es este caso se le dara una posicion.

    todos_sprites.draw(interfaz)

    Marcador(interfaz, str(puntos), 25, ancho // 1.8, 10) #Marcador
    Marcador(interfaz, str("Puntos:"), 25, ancho // 2, 10)


    Salud(interfaz, 5, 5, nave.shield) #Coordenadas 5,5 y porcetange es nave.shield

    pygame.display.flip() #Este metodo se utiliza para actualizar la ventana de visualización del juego

pygame.quit() #Este método se utiliza para cerrar y liberar todos los recursos utilizados por la biblioteca Pygame

#--------------------------------------------------------------