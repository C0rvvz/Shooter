import pygame
import random

# -----------------------------------------------------------------------
# Configuración global
ancho = 1300
alto = 700
color_negro = (0, 0, 0)
color_blanco = (255, 255, 255)
color_verde = (0, 255, 0)

# Inicialización de Pygame
pygame.init()
pygame.mixer.init()
interfaz = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("ECHO DEEP GALAXY")
tiempo = pygame.time.Clock()

# -----------------------------------------------------------------------
# Cargar recursos
def cargar_recursos():
    global imagenes_objetos, lista_explosion, fondo_menu, fondo_juego, nuevas_imagenes_objetos
    imagenes_objetos = []
    lista_objetos = [
        "multimedia/meteoro_mediano1.png", "multimedia/meteoro_mediano2.png",
        "multimedia/meteoro_pequeño1.png", "multimedia/meteoro_pequeño2.png",
        "multimedia/meteoro_muypequeño1.png", "multimedia/meteoro_muypequeño2.png"
    ]
    for img in lista_objetos:
        imagenes_objetos.append(pygame.image.load(img).convert_alpha())

    lista_explosion = []
    for img in range(9):
        archivo = f"multimedia/regularExplosion0{img}.png"
        imagen_explosion = pygame.image.load(archivo).convert_alpha()
        imagen_escala = pygame.transform.scale(imagen_explosion, (70, 70))
        lista_explosion.append(imagen_escala)

    fondo_menu = pygame.image.load("multimedia/menu.jpg").convert()
    fondo_juego = pygame.image.load("multimedia/nubes.jpg").convert()

    nuevas_imagenes_objetos = []
    lista_nuevos_objetos = [
        "multimedia/meteoro_mediano1.png", "multimedia/meteoro_mediano2.png",
        "multimedia/meteoro_pequeño1.png", "multimedia/meteoro_pequeño2.png",
        "multimedia/meteoro_muypequeño1.png", "multimedia/meteoro_muypequeño2.png"
    ]
    for img in lista_nuevos_objetos:
        nuevas_imagenes_objetos.append(pygame.image.load(img).convert_alpha())

# -----------------------------------------------------------------------
# Cargar sonidos
def cargar_sonidos():
    global sonido_laser, sonido_explosion, sonido_final, sonido_comienzo, musica_menu, musica_nivel_1, musica_nivel_2
    try:
        sonido_laser = pygame.mixer.Sound("multimedia/laser_sonido.ogg")
        sonido_explosion = pygame.mixer.Sound("multimedia/explosion_sonido.wav")
        sonido_final = pygame.mixer.Sound("multimedia/sonido_final.mp3")
        sonido_comienzo = pygame.mixer.Sound("multimedia/comienzo.mp3")
        musica_menu = "multimedia/sonido_menu.mp3"
        musica_nivel_1 = "multimedia/sonido_nivel1.mp3"
        musica_nivel_2 = "multimedia/sonido_nivel2.mp3"
    except pygame.error:
        print("Error al cargar sonidos. Audio deshabilitado.")
        sonido_laser = None
        sonido_explosion = None
        sonido_final = None
        sonido_comienzo = None
        musica_menu = None
        musica_nivel_1 = None
        musica_nivel_2 = None

# -----------------------------------------------------------------------
# Función para reproducir la música del menú
def sonido_menu():
    if musica_menu:
        pygame.mixer.music.load(musica_menu)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(loops=-1)

# Función para reproducir la música del nivel 1
def sonido_nivel1():
    if musica_nivel_1:
        pygame.mixer.music.load(musica_nivel_1)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(loops=-1)

# Función para reproducir la música del nivel 2
def sonido_nivel2():
    if musica_nivel_2:
        pygame.mixer.music.load(musica_nivel_2)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(loops=-1)

# -----------------------------------------------------------------------
# Clases del juego
class Nave(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("multimedia/nave.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = ancho // 2
        self.rect.bottom = alto - 10
        self.speed_x = 0
        self.speed_y = 0
        self.shield = 100

    def update(self):
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
        self.rect.x = max(0, min(ancho - self.rect.width, self.rect.x + self.speed_x))
        self.rect.y = max(0, min(alto - self.rect.height, self.rect.y + self.speed_y))

    def shoot(self):
        disparo = Disparo(self.rect.centerx, self.rect.top)
        juego.todos_sprites.add(disparo)
        juego.todos_disparos.add(disparo)
        if sonido_laser:
            sonido_laser.play()

class Disparo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("multimedia/laser1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        self.speedy = -50

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Objeto(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(imagenes_objetos)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ancho - self.rect.width)
        self.rect.y = random.randrange(-140, -100)
        self.speedy = random.randrange(5, 10)
        self.speedx = random.uniform(-2, 2)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > alto + 10 or self.rect.left < -40 or self.rect.right > ancho + 40:
            self.rect.x = random.randrange(ancho - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(5, 10)
            self.speedx = random.uniform(-2, 2)

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = lista_explosion[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(lista_explosion):
                self.kill()
            else:
                center = self.rect.center
                self.image = lista_explosion[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Marcador:
    def __init__(self, superficie, texto, tamaño, x, y):
        fuente = pygame.font.SysFont("serif", tamaño)
        texto_superficie = fuente.render(texto, True, color_blanco)
        texto_rect = texto_superficie.get_rect()
        texto_rect.midtop = (x, y)
        superficie.blit(texto_superficie, texto_rect)

class Salud:
    def __init__(self, superficie, x, y, porcentaje):
        barra_longitud = 100
        barra_altura = 10
        relleno = (porcentaje / 100) * barra_longitud
        borde = pygame.Rect(x, y, barra_longitud, barra_altura)
        relleno = pygame.Rect(x, y, relleno, barra_altura)
        pygame.draw.rect(superficie, color_verde, relleno)
        pygame.draw.rect(superficie, color_blanco, borde, 2)

# -----------------------------------------------------------------------
# Clase principal del juego
class Juego:
    def __init__(self):
        self.reset()

    def reset(self):
        global fondo_juego, imagenes_objetos
        self.todos_sprites = pygame.sprite.Group()
        self.todos_objetos = pygame.sprite.Group()
        self.todos_disparos = pygame.sprite.Group()
        self.nave = Nave()
        self.todos_sprites.add(self.nave)
        self.limite_objetos_actual = 5
        self.puntos = 0
        self.nivel = 1
        self.puntos_umbral = 10
        self.transicion_activada = False
        self.transicion_progresiva = False
        self.altura_transicion = 0
        self.opacidad_transicion = 0
        self.progresivo_objetos = False
        self.tiempo_ultimo_objeto = pygame.time.get_ticks()
        self.intervalo_objetos = 200
        self.colisiones_activas = True

        # Reset the background and object images to level 1
        fondo_juego = pygame.image.load("multimedia/nubes.jpg").convert()
        imagenes_objetos = [
            pygame.image.load("multimedia/meteoro_mediano1.png").convert_alpha(),
            pygame.image.load("multimedia/meteoro_mediano2.png").convert_alpha(),
            pygame.image.load("multimedia/meteoro_pequeño1.png").convert_alpha(),
            pygame.image.load("multimedia/meteoro_pequeño2.png").convert_alpha(),
            pygame.image.load("multimedia/meteoro_muypequeño1.png").convert_alpha(),
            pygame.image.load("multimedia/meteoro_muypequeño2.png").convert_alpha(),
        ]

        # Create initial objects for level 1
        for _ in range(self.limite_objetos_actual):
            self.crear_objeto()

    def crear_objeto(self):
        if len(self.todos_objetos) < self.limite_objetos_actual:
            objeto = Objeto()
            self.todos_sprites.add(objeto)
            self.todos_objetos.add(objeto)

    def manejar_colisiones(self):
        if not self.colisiones_activas:
            return  # Desactiva las colisiones si están deshabilitadas

        # Colisiones entre disparos y objetos
        colisiones = pygame.sprite.groupcollide(self.todos_objetos, self.todos_disparos, True, True)
        for colision in colisiones:
            explosion = Explosion(colision.rect.center)
            self.todos_sprites.add(explosion)
            self.puntos += 5
            self.crear_objeto()
            if sonido_explosion:  # Reproducir sonido de explosión
                sonido_explosion.play()
            if self.puntos >= self.puntos_umbral:
                self.incrementar_objetos()

        # Activar la transición al nivel 2 si el jugador alcanza 30 puntos
        if self.puntos >= 30 and not self.transicion_activada and not self.transicion_progresiva:
            self.transicion_progresiva = True
            self.colisiones_activas = False  # Desactiva las colisiones
            self.nave.speed_y = -5  # Mueve la nave hacia arriba

        # Colisiones entre la nave y los objetos
        colisiones = pygame.sprite.spritecollide(self.nave, self.todos_objetos, True)
        for colision in colisiones:
            self.nave.shield -= 25
            explosion = Explosion(colision.rect.center)
            self.todos_sprites.add(explosion)
            self.crear_objeto()
            if sonido_explosion:  # Reproducir sonido de explosión
                sonido_explosion.play()
            if self.nave.shield <= 0:
                self.perder()

    def incrementar_objetos(self):
        if self.nivel == 1 and self.limite_objetos_actual < 30:
            self.limite_objetos_actual += 1
            self.puntos_umbral += 10

    def perder(self):
        pygame.mixer.music.stop()
        if sonido_final:
            sonido_final.play()

        # Congelar la pantalla y mostrar el mensaje de puntos
        self.mostrar_pantalla_congelada()

        # Volver al menú al presionar "Enter"
        Menu.mostrar_menu()
        Menu.esperar_entrada()
        self.reset()
        sonido_nivel1()

    def mostrar_pantalla_congelada(self):
        """
        Congela la pantalla y muestra los puntos finales con un mensaje.
        """
        interfaz.blit(fondo_juego, [0, 0])
        self.todos_sprites.draw(interfaz)
        Marcador(interfaz, f"Puntos finales: {self.puntos}", 50, ancho // 2, alto // 3)
        Marcador(interfaz, "Presiona 'Enter' para volver al menú", 30, ancho // 2, alto // 2)
        sonido_menu()
        pygame.display.flip()

        esperando = True
        while esperando:
            tiempo.tick(60)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:  # Tecla "Enter"
                        esperando = False

    def manejar_transicion(self):
        if self.transicion_progresiva:
            # Mover la nave hacia arriba
            self.nave.rect.y -= 5
            if self.nave.rect.bottom <= 0:  # Si la nave sale de la pantalla
                self.nave.rect.bottom = 0

            # Crear una pantalla negra que baja lentamente
            self.altura_transicion += 20  # Velocidad de la transición
            superficie_transicion = pygame.Surface((ancho, self.altura_transicion))
            superficie_transicion.fill(color_negro)
            interfaz.blit(superficie_transicion, (0, 0))

            # Si la pantalla negra cubre toda la interfaz
            if self.altura_transicion >= alto:
                self.transicion_progresiva = False
                self.transicion_activada = True
                self.nivel += 1
                self.cargar_nivel(self.nivel)

    def cargar_nivel(self, nivel):
        global fondo_juego, imagenes_objetos
        if nivel == 2:
            # Detener la música del nivel 1
            pygame.mixer.music.stop()

            # Reproducir la música del nivel 2
            sonido_nivel2()

            # Cambiar el fondo y las imágenes de los objetos
            fondo_juego = pygame.image.load("multimedia/espacio.jpg").convert()
            imagenes_objetos = nuevas_imagenes_objetos

            # Centrar la nave en la parte inferior
            self.nave.rect.centerx = ancho // 2
            self.nave.rect.bottom = alto

            # Mostrar la pantalla negra saliendo lentamente
            self.mostrar_salida_pantalla_negra()

            # Mostrar la cuenta regresiva
            self.mostrar_cuenta_regresiva()

            # Eliminar todos los objetos del nivel 1
            self.todos_objetos.empty()
            self.todos_sprites = pygame.sprite.Group(self.nave)  # Reiniciar sprites con solo la nave

            # Generar nuevos objetos para el nivel 2
            self.respawn_objetos()

            # Reactivar las colisiones
            self.colisiones_activas = True

    def respawn_objetos(self):
        """
        Genera nuevos objetos desde la parte superior de la pantalla.
        """
        for _ in range(self.limite_objetos_actual):
            objeto = Objeto()
            objeto.image = random.choice(imagenes_objetos)  # Asegurarse de usar las imágenes correctas
            objeto.rect.y = random.randrange(-140, -100)  # Posición inicial fuera de la pantalla
            self.todos_sprites.add(objeto)
            self.todos_objetos.add(objeto)

    def mostrar_salida_pantalla_negra(self):
        # Crear una pantalla negra que sube lentamente
        for altura in range(alto, 0, -20):  # Velocidad de la transición
            superficie_transicion = pygame.Surface((ancho, altura))
            superficie_transicion.fill(color_negro)
            interfaz.blit(fondo_juego, [0, 0])  # Dibuja el fondo del nivel 2
            interfaz.blit(superficie_transicion, (0, alto - altura))
            pygame.display.flip()
            pygame.time.delay(50)  # Controlar la velocidad de la transición

    def mostrar_cuenta_regresiva(self):
        fuente = pygame.font.SysFont("serif", self.nave.rect.height)
        for numero in range(3, -1, -1):
            # Mostrar el fondo del nivel 2
            interfaz.blit(fondo_juego, [0, 0])
            texto = fuente.render(str(numero), True, color_blanco)
            texto_rect = texto.get_rect(center=(ancho // 2, alto // 2))
            interfaz.blit(texto, texto_rect)
            pygame.display.flip()
            pygame.time.delay(1000)  # Espera 1 segundo

    def manejar_nivel_2(self):
        if self.nivel == 2 and self.progresivo_objetos:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_ultimo_objeto >= self.intervalo_objetos:
                if len(self.todos_objetos) < self.limite_objetos_actual:
                    self.crear_objeto()
                    self.tiempo_ultimo_objeto = tiempo_actual
                else:
                    self.progresivo_objetos = False

# Clase Menu
class Menu:
    @staticmethod
    def mostrar_menu():
        interfaz.blit(fondo_menu, [0, 0])
        Marcador(interfaz, "ECHO DEEP GALAXY", 65, ancho // 2, alto // 2 / 3)
        Marcador(interfaz, "Destruye tantos desperdicios como puedas", 19, ancho // 2, alto // 3)
        Marcador(interfaz, "Te mueves con las flechas y disparas con la barra espaciadora", 20, ancho // 2, alto // 2)
        Marcador(interfaz, "Presiona 'Enter' para comenzar", 15, ancho // 2, alto * 3 / 4)
        pygame.display.flip()

    @staticmethod
    def esperar_entrada():
        esperando = True
        while esperando:
            tiempo.tick(60)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:  # Tecla "Enter"
                        esperando = False

# -----------------------------------------------------------------------
# Función principal
def main():
    global juego
    cargar_recursos()
    cargar_sonidos()

    # Mostrar el menú inicial
    sonido_menu()
    Menu.mostrar_menu()
    Menu.esperar_entrada()
    pygame.mixer.music.stop()

    # Iniciar el juego
    juego = Juego()
    if sonido_comienzo:
        sonido_comienzo.play()
    sonido_nivel1()

    fps = True
    while fps:
        tiempo.tick(60)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                fps = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    juego.nave.shoot()

        juego.todos_sprites.update()
        juego.manejar_colisiones()
        juego.incrementar_objetos()
        juego.manejar_transicion()
        juego.manejar_nivel_2()

        interfaz.blit(fondo_juego, [0, 0])
        juego.todos_sprites.draw(interfaz)
        Marcador(interfaz, f"Puntos: {juego.puntos}", 25, ancho // 2, 10)
        Salud(interfaz, 5, 5, juego.nave.shield)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()