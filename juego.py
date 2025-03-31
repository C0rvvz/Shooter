#--------------------------------------------------------------------
# Notas:
# Acuérdense de instalar pygame
#---------------------------------------------------------------------

# Importaciones:
import pygame, random

#-----------------------------------------------------------------------
# Variables globales:
puntos = 0
ancho = 1300
alto = 700
color_negro = (0, 0, 0)
color_blanco = (255, 255, 255)
color_verde = (0, 255, 0)
interfaz = pygame.display.set_mode((ancho, alto))
tiempo = pygame.time.Clock()

# Nueva variable global para el límite de objetos
max_objetos = 1000  # Número máximo de objetos activos en pantalla

# Nueva variable global para el límite dinámico de objetos
limite_objetos_actual = 5  # Límite inicial de objetos
limite_objetos_maximo = 30  # Límite máximo de objetos después de 100 puntos
incremento_objetos = 1  # Incremento progresivo de objetos
puntos_umbral = 10  # Puntos necesarios para aumentar el límite

# Nueva variable global para manejar la transición
transicion_activada = False  # Indica si la transición ya ocurrió
nuevo_fondo = None  # Variable para el nuevo fondo
nuevas_imagenes_objetos = []  # Lista para las nuevas imágenes de objetos

# Nueva variable global para manejar la transición progresiva
transicion_progresiva = False  # Indica si la transición progresiva está activa
altura_transicion = 0  # Altura inicial de la transición

# Nueva variable global para manejar la opacidad de la transición
opacidad_transicion = 0  # Opacidad inicial de la transición

# Nueva variable global para manejar los niveles
nivel = 1  # Nivel inicial

# Diccionario para almacenar los datos de cada nivel
niveles = {
    1: {
        "fondo": "multimedia/nubes.jpg",
        "objetos": [
            "multimedia/meteoro_mediano1.png", "multimedia/meteoro_mediano2.png",
            "multimedia/meteoro_pequeño1.png", "multimedia/meteoro_pequeño2.png",
            "multimedia/meteoro_muypequeño1.png", "multimedia/meteoro_muypequeño2.png"
        ]
    },
    2: {
        "fondo": "multimedia/espacio.jpg",
        "objetos": [
            "multimedia/meteoro_mediano1.png", "multimedia/meteoro_mediano2.png",
            "multimedia/meteoro_pequeño1.png", "multimedia/meteoro_pequeño2.png",
            "multimedia/meteoro_muypequeño1.png", "multimedia/meteoro_muypequeño2.png"
        ]
    }
}

# Nueva variable global para manejar la aparición progresiva de objetos
progresivo_objetos = False  # Indica si los objetos están apareciendo progresivamente
tiempo_ultimo_objeto = 0  # Tiempo del último objeto agregado
intervalo_objetos = 200  # Intervalo en milisegundos entre la aparición de objetos

# Nueva variable global para manejar el incremento de objetos en el nivel 2
incremento_objetos_nivel_2 = 10  # Incremento progresivo de objetos en el nivel 2

#-----------------------------------------------------------------------
# Inicialización de Pygame:
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("ECHO DEEP GALAXY")

try:
    sonido_final = pygame.mixer.Sound("multimedia/sonido_final.mp3")
    sonido_comienzo = pygame.mixer.Sound("multimedia/comienzo.mp3")
except pygame.error:
    print("Audio deshabilitado en este entorno.")
    sonido_final = None
    sonido_comienzo = None

# Inicialización de la variable `menu`
menu = True

#----------------------------------------------------------------------
# Clase Nave:
class Nave(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("multimedia/nave.png").convert()
        self.image.set_colorkey(color_negro)
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
        todos_sprites.add(disparo)
        todos_disparos.add(disparo)
        if sonido_laser:
            sonido_laser.play()

#------------------------------------------------------------------------
# Clase Disparo:
class Disparo(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("multimedia/laser1.png").convert()
        self.image.set_colorkey(color_negro)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        self.speedy = -50

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

#--------------------------------------------------------------------------
# Clase Marcador:
class Marcador():
    def __init__(self, superficie, texto, tamaño, x, y):
        fuente = pygame.font.SysFont("serif", tamaño)
        texto_superficie = fuente.render(texto, True, color_blanco)
        texto_rect = texto_superficie.get_rect()
        texto_rect.midtop = (x, y)
        superficie.blit(texto_superficie, texto_rect)

#-------------------------------------------------------------------------
# Clase Objeto:
class Objeto(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(imagenes_objetos)
        # No se necesita set_colorkey porque las imágenes con transparencia ya usan convert_alpha
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ancho - self.rect.width)  # Posición inicial aleatoria en el eje X
        self.rect.y = random.randrange(-140, -100)  # Posición inicial fuera de la pantalla en el eje Y
        self.speedy = random.randrange(5, 10)  # Velocidad vertical (más rápida para trayectorias verticales)
        self.speedx = random.uniform(-2, 2)  # Velocidad horizontal (pequeña inclinación)

    def update(self):
        self.rect.y += self.speedy  # Movimiento vertical
        self.rect.x += self.speedx  # Movimiento horizontal con inclinación
        # Si el objeto sale de la pantalla, se reposiciona para regenerarse
        if self.rect.top > alto + 10 or self.rect.left < -40 or self.rect.right > ancho + 40:
            self.rect.x = random.randrange(ancho - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(5, 10)
            self.speedx = random.uniform(-2, 2)

# Modifica la función `crear_objeto` para garantizar la generación progresiva
def crear_objeto():
    """
    Crea un nuevo objeto si el número actual de objetos en pantalla es menor que `limite_objetos_actual`.
    """
    if len(todos_objetos) < limite_objetos_actual:  # Verifica si no se ha alcanzado el límite actual
        objeto = Objeto()
        if transicion_activada:  # Usa las nuevas imágenes si la transición ocurrió
            objeto.image = random.choice(nuevas_imagenes_objetos)
        todos_sprites.add(objeto)  # Agrega el objeto al grupo de todos los sprites
        todos_objetos.add(objeto)  # Agrega el objeto al grupo de objetos activos

# --------------------------------------------------------------
# Clase Salud:
class Salud():
    def __init__(self, superficie, x, y, porcentaje):
        barra_longitud = 100
        barra_altura = 10
        relleno = (porcentaje / 100) * barra_longitud
        borde = pygame.Rect(x, y, barra_longitud, barra_altura)
        relleno = pygame.Rect(x, y, relleno, barra_altura)
        pygame.draw.rect(superficie, color_verde, relleno)
        pygame.draw.rect(superficie, color_blanco, borde, 2)

#----------------------------------------------------------------------------
# Clase Explosion:
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

def explosion(colicion):
    explosion = Explosion(colicion.rect.center)
    todos_sprites.add(explosion)

#--------------------------------------------------
# Clase Menu:
class Menu():
    def __init__(self):
        interfaz.blit(fondo_menu, [0, 0])
        Marcador(interfaz, "ECHO DEEP GALAXY", 65, ancho // 2, alto // 2 / 3)
        Marcador(interfaz, "Destruye tantos desperdicios como puedas", 19, ancho // 2, alto // 3)
        Marcador(interfaz, "Te mueves con las flechas y disparas con la barra espaciadora", 20, ancho // 2, alto // 2)
        Marcador(interfaz, "Presiona una tecla", 15, ancho // 2, alto * 3 / 4)
        pygame.display.flip()
        pausa = True
        while pausa:
            tiempo.tick(60)
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()  # Asegura que el programa se cierre correctamente
                if evento.type == pygame.KEYDOWN:
                    pausa = False

#-----------------------------------------------------------------------------
# Cargar imágenes:
imagenes_objetos = []
lista_objetos = ["multimedia/meteoro_mediano1.png", "multimedia/meteoro_mediano2.png", "multimedia/meteoro_pequeño1.png", "multimedia/meteoro_pequeño2.png",
                 "multimedia/meteoro_muypequeño1.png", "multimedia/meteoro_muypequeño2.png"]
for img in lista_objetos:
    imagenes_objetos.append(pygame.image.load(img).convert())

lista_explosion = []
for img in range(9):
    archivo = "multimedia/regularExplosion0{}.png".format(img)
    imagen_explosion = pygame.image.load(archivo).convert()
    imagen_explosion.set_colorkey(color_negro)
    imagen_escala = pygame.transform.scale(imagen_explosion, (70, 70))
    lista_explosion.append(imagen_escala)

fondo_menu = pygame.image.load("multimedia/fondo_menu.jpg").convert()
fondo_juego = pygame.image.load("multimedia/nubes.jpg").convert()

# Cargar imágenes para la transición
nuevo_fondo = pygame.image.load("multimedia/espacio.jpg").convert()
lista_nuevos_objetos = ["multimedia/meteoro_mediano1.png", "multimedia/meteoro_mediano2.png", "multimedia/meteoro_pequeño1.png", "multimedia/meteoro_pequeño2.png",
                 "multimedia/meteoro_muypequeño1.png", "multimedia/meteoro_muypequeño2.png"]
for img in lista_nuevos_objetos:
    nuevas_imagenes_objetos.append(pygame.image.load(img).convert())

# Función para cargar los datos de un nivel
def cargar_nivel(nivel_actual):
    """
    Carga el fondo y las imágenes de los objetos para el nivel especificado.
    """
    global fondo_juego, imagenes_objetos
    datos_nivel = niveles[nivel_actual]
    fondo_juego = pygame.image.load(datos_nivel["fondo"]).convert()
    imagenes_objetos = []
    for img in datos_nivel["objetos"]:
        # Usa convert_alpha() para todas las imágenes de objetos para soportar transparencia
        imagenes_objetos.append(pygame.image.load(img).convert_alpha())

#---------------------------------------------------------------------------
# Cargar sonidos:
try:
    sonido_laser = pygame.mixer.Sound("multimedia/laser_sonido.ogg")
    sonido_explosion = pygame.mixer.Sound("multimedia/explosion_sonido.wav")
    musica_menu = "multimedia/sonido_menu.mp3"
    musica_nivel_1 = "multimedia/sonido_nivel1.mp3"
    musica_nivel_2 = "multimedia/sonido_nivel2.mp3"
except pygame.error:
    print("Error al cargar sonidos. Audio deshabilitado.")
    sonido_laser = None
    sonido_explosion = None
    musica_menu = None
    musica_nivel_1 = None
    musica_nivel_2 = None

def sonido_menu():
    pygame.mixer.music.load(musica_menu)
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(loops=-1)

def sonido_nivel1():
    pygame.mixer.music.load(musica_nivel_1)
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(loops=-1)

def sonido_nivel2():
    pygame.mixer.music.load(musica_nivel_2)
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(loops=-1)

#----------------------------------------------------------------------
# Bucle principal:
fps = True
while fps:
    # Variables iniciales para reiniciar el juego
    valores_iniciales = {
        "limite_objetos_actual": 5,
        "limite_objetos_maximo": 30,
        "puntos_umbral": 10,
        "incremento_objetos": 1,
        "nivel": 1,
        "puntos": 0,
        "altura_transicion": 0,
        "opacidad_transicion": 0,
    }

    # Reiniciar correctamente el juego
    if menu and not transicion_progresiva and not transicion_activada:
        sonido_menu()
        Menu()
        menu = False
        pygame.mixer.music.stop()
        if sonido_comienzo:
            sonido_comienzo.play()
        sonido_nivel1()

        # Reiniciar grupos de sprites
        todos_sprites = pygame.sprite.Group()
        todos_objetos = pygame.sprite.Group()
        todos_disparos = pygame.sprite.Group()

        # Reiniciar variables del juego usando los valores iniciales
        nave = Nave()
        todos_sprites.add(nave)
        limite_objetos_actual = valores_iniciales["limite_objetos_actual"]
        limite_objetos_maximo = valores_iniciales["limite_objetos_maximo"]
        puntos_umbral = valores_iniciales["puntos_umbral"]
        incremento_objetos = valores_iniciales["incremento_objetos"]
        nivel = valores_iniciales["nivel"]
        puntos = valores_iniciales["puntos"]
        altura_transicion = valores_iniciales["altura_transicion"]
        opacidad_transicion = valores_iniciales["opacidad_transicion"]
        transicion_activada = False
        transicion_progresiva = False
        cargar_nivel(nivel)  # Carga los datos del nivel 1

        # Generar los objetos iniciales
        for i in range(limite_objetos_actual):
            crear_objeto()

    tiempo.tick(60)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            fps = False
        elif evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                nave.shoot()
    todos_sprites.update()
    # Detener el conteo de puntos si la transición está activa
    if not transicion_progresiva and not transicion_activada:
        # Manejo de colisiones entre disparos y objetos
        coliciones = pygame.sprite.groupcollide(todos_objetos, todos_disparos, True, True)
        for colicion in coliciones:
            explosion(colicion)
            puntos += 5
            crear_objeto()  # Generar un nuevo objeto al destruir uno
            if sonido_explosion:
                sonido_explosion.play()
        # Manejo de colisiones entre la nave y los objetos
        coliciones = pygame.sprite.spritecollide(nave, todos_objetos, True)
        for colicion in coliciones:
            nave.shield -= 25
            explosion(colicion)
            crear_objeto()  # Generar un nuevo objeto al colisionar con la nave
            if sonido_explosion:
                sonido_explosion.play()
            if nave.shield <= 0:
                menu = True
                if sonido_final:
                    sonido_final.play()
                pygame.mixer.music.stop()
                sonido_menu()
                puntos = 0
    # Incrementar progresivamente el límite de objetos
    if puntos >= puntos_umbral and limite_objetos_actual < limite_objetos_maximo:
        limite_objetos_actual += incremento_objetos
        puntos_umbral += 5  # Aumenta el umbral para el siguiente incremento

    # Asegurar que siempre haya `limite_objetos_actual` en pantalla
    while len(todos_objetos) < limite_objetos_actual:
        crear_objeto()

    # Dibujar el fondo actual y los sprites
    interfaz.blit(fondo_juego, [0, 0])
    todos_sprites.draw(interfaz)

    # Mostrar el número actual de objetos en pantalla
    Marcador(interfaz, f"Objetos en pantalla: {len(todos_objetos)}", 25, ancho // 2, 40)

    # Manejar la transición progresiva
    if transicion_progresiva:
        altura_transicion += 30  # Incrementa la altura del rectángulo negro más rápido
        opacidad_transicion = min(opacidad_transicion + 15, 255)  # Incrementa la opacidad más rápido
        # Crear una superficie negra semi-transparente
        superficie_transicion = pygame.Surface((ancho, altura_transicion))
        superficie_transicion.set_alpha(opacidad_transicion)  # Establece la opacidad
        superficie_transicion.fill(color_negro)  # Llena la superficie con negro
        interfaz.blit(superficie_transicion, (0, 0))  # Dibuja la superficie en la pantalla
        # Cambiar la música progresivamente
        if altura_transicion == 30:  # Inicia el fadeout de la música actual al comienzo de la transición
            pygame.mixer.music.fadeout(2000)  # Desvanece la música actual en 2 segundos
        if altura_transicion >= alto:  # Si el rectángulo cubre toda la pantalla
            transicion_progresiva = False
            transicion_activada = True
            nivel += 1  # Cambia al siguiente nivel
            cargar_nivel(nivel)  # Carga los datos del nuevo nivel
            # Eliminar todos los objetos del nivel 1
            todos_objetos.empty()  # Vaciar el grupo de objetos
            limite_objetos_actual = 0  # Reiniciar el límite de objetos
            puntos_umbral = 5  # Reiniciar el umbral de puntos para el nivel 2
            # Configurar la aparición progresiva de objetos
            progresivo_objetos = True
            tiempo_ultimo_objeto = pygame.time.get_ticks()  # Reinicia el temporizador
            sonido_comienzo.play()
            pygame.mixer.music.load(musica_nivel_2)  # Carga la música del nivel 2
            pygame.mixer.music.play(loops=-1, fade_ms=2000)  # Inicia la música con un fade-in de 2 segundos

    # Manejar la aparición progresiva de objetos al inicio del nivel 2
    if progresivo_objetos:
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - tiempo_ultimo_objeto >= intervalo_objetos:
            if len(todos_objetos) < limite_objetos_actual:  # Agregar objetos progresivamente
                crear_objeto()
                tiempo_ultimo_objeto = tiempo_actual  # Actualizar el tiempo del último objeto agregado
            else:
                progresivo_objetos = False  # Finalizar la aparición progresiva cuando se alcance el límite

    # Incrementar progresivamente el límite de objetos en el nivel 2
    if nivel == 2 and puntos >= puntos_umbral and limite_objetos_actual < limite_objetos_maximo:
        limite_objetos_actual += incremento_objetos_nivel_2
        puntos_umbral += 5  # Aumenta el umbral para el siguiente incremento

    # Manejo de colisiones entre disparos y objetos
    coliciones = pygame.sprite.groupcollide(todos_objetos, todos_disparos, True, True)
    for colicion in coliciones:
        explosion(colicion)
        if not transicion_progresiva and not transicion_activada:  # Solo contar puntos fuera de la transición
            puntos += 5
        crear_objeto()  # Generar un nuevo objeto al destruir uno
        if sonido_explosion:
            sonido_explosion.play()

    # Manejo de colisiones entre la nave y los objetos
    coliciones = pygame.sprite.spritecollide(nave, todos_objetos, True)
    for colicion in coliciones:
        nave.shield -= 25
        explosion(colicion)
        crear_objeto()  # Generar un nuevo objeto al colisionar con la nave
        if sonido_explosion:
            sonido_explosion.play()
        if nave.shield <= 0:
            menu = True
            if sonido_final:
                sonido_final.play()
            pygame.mixer.music.stop()
            sonido_menu()
            puntos = 0

    # Activar la transición progresiva al alcanzar 1000 puntos y cambiar al nivel 2
    if puntos >= 1000 and nivel == 1 and not transicion_activada and not transicion_progresiva:
        transicion_progresiva = True

    Marcador(interfaz, str(puntos), 25, ancho // 1.8, 10)
    Marcador(interfaz, str("Puntos:"), 25, ancho // 2, 10)
    Salud(interfaz, 5, 5, nave.shield)
    pygame.display.flip()

pygame.quit()