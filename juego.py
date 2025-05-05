import pygame
import random

ancho = 1300
alto = 700
color_negro = (0, 0, 0)
color_blanco = (255, 255, 255)
color_verde = (0, 255, 0)

pygame.init()
pygame.mixer.init()
interfaz = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("ECHO MISSION")
tiempo = pygame.time.Clock()

def cargar_recursos():
    global imagenes_objetos_1, imagenes_objetos_2, imagenes_objetos_3, imagenes_objetos_4, lista_explosion, fondo_menu, fondo_juego, lista_objetos_1, lista_objetos_2, lista_objetos_3, lista_objetos_4
    imagenes_objetos_1 = []
    lista_objetos_1 = [
        "multimedia/vidrio.png", "multimedia/vidrio_amarillo.png",
        "multimedia/vidrio_cafe.png", "multimedia/vidrio_rojo.png",
        "multimedia/vidrio_rojod.png"
    ]
    tamanos_nivel_1 = [(70, 70), (80, 80), (50, 50), (40, 40), (45, 45)]
    for img, tamano in zip(lista_objetos_1, tamanos_nivel_1):
        imagen = pygame.image.load(img).convert_alpha()
        imagen = pygame.transform.scale(imagen, tamano)
        imagenes_objetos_1.append(imagen)

    imagenes_objetos_2 = []
    lista_objetos_2 = [
        "multimedia/bolsa_carton.png", "multimedia/papel_higienico.png",
        "multimedia/periodico.png", "multimedia/periodiquito.png",
        "multimedia/sobre_carta.png"
    ]
    tamanos_nivel_2 = [(70, 70), (50, 50), (40, 40), (45, 45), (50,50), (40,40)]
    for img, tamano in zip(lista_objetos_2, tamanos_nivel_2):
        imagen = pygame.image.load(img).convert_alpha()
        imagen = pygame.transform.scale(imagen, tamano)
        imagenes_objetos_2.append(imagen)

    imagenes_objetos_3 = []
    lista_objetos_3 = [
        "multimedia/botella.png", "multimedia/champu.png",
        "multimedia/bolsa.png", "multimedia/jugo.png",
        "multimedia/atun.png", "multimedia/juguito.png",
        "multimedia/lata.png", "multimedia/leche.png",
        "multimedia/refresco.png", "multimedia/plastico.png","multimedia/tarro.png"
    ]
    tamanos_nivel_3 = [(70, 70), (60, 60), (50, 50), (40, 40), (45, 45),(70, 70), (80, 80), (60, 60), (50, 50), (40, 40), (45, 45)]
    for img, tamano in zip(lista_objetos_3, tamanos_nivel_3):
        imagen = pygame.image.load(img).convert_alpha()
        imagen = pygame.transform.scale(imagen, tamano)
        imagenes_objetos_3.append(imagen)

    imagenes_objetos_4 = []
    lista_objetos_4 = [
        "multimedia/botella.png", "multimedia/champu.png",
        "multimedia/bolsa.png", "multimedia/jugo.png",
        "multimedia/atun.png", "multimedia/juguito.png",
        "multimedia/lata.png", "multimedia/leche.png",
        "multimedia/refresco.png", "multimedia/plastico.png", 
        "multimedia/tarro.png", "multimedia/vidrio.png",
        "multimedia/vidrio_amarillo.png",
        "multimedia/vidrio_cafe.png", "multimedia/vidrio_rojo.png",
        "multimedia/vidrio_rojod.png",
        "multimedia/bolsa_carton.png", "multimedia/papel_higienico.png",
        "multimedia/periodico.png", "multimedia/periodiquito.png",
        "multimedia/sobre_carta.png", "multimedia/hoja_papel.png"
    ]
    tamanos_nivel_4 = [(70, 70), (80, 80), (40, 40), (45, 45), (50,50), (40,40),(70, 70), (80, 80), (50, 50), (40, 40), (45, 45),(70, 70), (80, 80), (60, 60), (40, 40), (45, 45), (70, 70), (80, 80), (60, 60), (50, 50), (40, 40), (45, 45)]
    for img, tamano in zip(lista_objetos_4, tamanos_nivel_4):
        imagen = pygame.image.load(img).convert_alpha()
        imagen = pygame.transform.scale(imagen, tamano)
        imagenes_objetos_4.append(imagen)

    lista_explosion = []
    for img in range(9):
        archivo = f"multimedia/regularExplosion0{img}.png"
        imagen_explosion = pygame.image.load(archivo).convert_alpha()
        imagen_escala = pygame.transform.scale(imagen_explosion, (70, 70))
        lista_explosion.append(imagen_escala)

    fondo_menu = pygame.image.load("multimedia/menu.jpg").convert()
    
    fondo_juego = pygame.image.load("multimedia/nivel_1.jpg").convert()
    fondo_juego = pygame.transform.scale(fondo_juego, (1300, 700))

    global fondo_nivel_2, fondo_nivel_3, fondo_nivel_4
    fondo_nivel_2 = pygame.image.load("multimedia/nivel_2.jpg").convert()
    fondo_nivel_2 = pygame.transform.scale(fondo_nivel_2, (1300, 700))

    fondo_nivel_3 = pygame.image.load("multimedia/nivel_3.jpg").convert()
    fondo_nivel_3 = pygame.transform.scale(fondo_nivel_3, (1300, 700))

    fondo_nivel_4 = pygame.image.load("multimedia/nivel_4.jpg").convert()
    fondo_nivel_4 = pygame.transform.scale(fondo_nivel_4, (1300, 700))

def cargar_sonidos():
    global sonido_laser, sonido_explosion, sonido_final, sonido_comienzo, musica_menu, musica_nivel_1, musica_nivel_2, musica_nivel_3, musica_nivel_4
    try:
        sonido_laser = pygame.mixer.Sound("multimedia/laser_sonido.ogg")
        sonido_explosion = pygame.mixer.Sound("multimedia/explosion_sonido.wav")
        sonido_final = pygame.mixer.Sound("multimedia/sonido_final.mp3")
        sonido_comienzo = pygame.mixer.Sound("multimedia/comienzo.mp3")
        musica_menu = "multimedia/sonido_menu.mp3"
        musica_nivel_1 = "multimedia/sonido_nivel1.mp3"
        musica_nivel_2 = "multimedia/sonido_nivel2.mp3"
        musica_nivel_3 = "multimedia/sonido_nivel3.mp3"
        musica_nivel_4 = "multimedia/sonido_nivel4.mp3"

    except pygame.error:
        print("Error al cargar sonidos. Audio deshabilitado.")
        sonido_laser = None
        sonido_explosion = None
        sonido_final = None
        sonido_comienzo = None
        musica_menu = None
        musica_nivel_1 = None
        musica_nivel_2 = None
        musica_nivel_3 = None
        musica_nivel_4 = None

def sonido_menu():
    if musica_menu:
        pygame.mixer.music.load(musica_menu)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(loops=-1)

def sonido_nivel1():
    if musica_nivel_1:
        pygame.mixer.music.load(musica_nivel_1)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(loops=-1)

def sonido_nivel2():
    if musica_nivel_2:
        pygame.mixer.music.load(musica_nivel_2)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(loops=-1)

def sonido_nivel3():
    if musica_nivel_3:
        pygame.mixer.music.load(musica_nivel_3)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(loops=-1)

def sonido_nivel4():
    if musica_nivel_4:
        pygame.mixer.music.load(musica_nivel_4)
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(loops=-1)

class Tanque(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("multimedia/tanque.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 150)) 
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
        if tecla_presionada[pygame.K_LEFT] or tecla_presionada[pygame.K_a]:  
            self.speed_x = -10
        if tecla_presionada[pygame.K_RIGHT] or tecla_presionada[pygame.K_d]:  
            self.speed_x = 10
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

class Juego:
    def __init__(self):
        self.reset()

    def reset(self):
        global fondo_juego, imagenes_objetos
        self.todos_sprites = pygame.sprite.Group()
        self.todos_objetos = pygame.sprite.Group()
        self.todos_disparos = pygame.sprite.Group()
        self.tanque = Tanque()  
        self.todos_sprites.add(self.tanque)  
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
        self.disparo_activo = True

        fondo_juego = pygame.image.load("multimedia/nivel_1.jpg").convert()
        imagenes_objetos = imagenes_objetos_1 

        for _ in range(self.limite_objetos_actual):
            self.crear_objeto()

    def crear_objeto(self):
        if len(self.todos_objetos) < self.limite_objetos_actual:
            objeto = Objeto()
            self.todos_sprites.add(objeto)
            self.todos_objetos.add(objeto)

    def manejar_colisiones(self):
        if not self.colisiones_activas: 
            return  

        colisiones = pygame.sprite.groupcollide(self.todos_objetos, self.todos_disparos, True, True)
        for colision in colisiones:
            explosion = Explosion(colision.rect.center)
            self.todos_sprites.add(explosion)
            self.puntos += 5
            self.crear_objeto()
            if sonido_explosion: 
                sonido_explosion.play()
            if self.puntos >= self.puntos_umbral:
                self.incrementar_objetos()

        if self.puntos >= 30 and self.nivel == 1 and not self.transicion_progresiva:
            self.transicion_progresiva = True  
        elif self.puntos >= 100 and self.nivel == 2 and not self.transicion_progresiva:
            self.transicion_progresiva = True  
        elif self.puntos >= 200 and self.nivel == 3 and not self.transicion_progresiva:
            self.transicion_progresiva = True  

        colisiones = pygame.sprite.spritecollide(self.tanque, self.todos_objetos, True)  
        for colision in colisiones:
            self.tanque.shield -= 25  
            explosion = Explosion(colision.rect.center)
            self.todos_sprites.add(explosion)
            self.crear_objeto()
            if sonido_explosion:  
                sonido_explosion.play()
            if self.tanque.shield <= 0:  
                self.perder()

    def incrementar_objetos(self):
        if self.nivel == 1 and self.limite_objetos_actual < 30:
            self.limite_objetos_actual += 1
            self.puntos_umbral += 10

    def perder(self):
        pygame.mixer.music.stop()
        if sonido_final:
            sonido_final.play()

        self.mostrar_pantalla_congelada()

        Menu.mostrar_menu()
        Menu.esperar_entrada()
        self.reset()
        sonido_nivel1()

    def mostrar_pantalla_congelada(self):
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
                    if evento.key == pygame.K_RETURN:  
                        esperando = False

    def manejar_transicion(self):
        if self.transicion_progresiva and not self.transicion_activada:  
            self.colisiones_activas = False  
            self.disparo_activo = False  

            self.altura_transicion += 20  
            superficie_transicion = pygame.Surface((ancho, self.altura_transicion))
            superficie_transicion.fill(color_negro)
            interfaz.blit(superficie_transicion, (0, 0))

            if self.altura_transicion >= alto:
                self.transicion_progresiva = False 
                self.transicion_activada = True
                if self.nivel == 1 and self.puntos >= 30:  
                    self.nivel = 2  
                elif self.nivel == 2 and self.puntos >= 100:  
                    self.nivel = 3  
                elif self.nivel == 3 and self.puntos >= 200:  
                    self.nivel = 4  
                self.cargar_nivel(self.nivel)
                self.altura_transicion = 0  
                self.transicion_activada = False

    def cargar_nivel(self, nivel):
        global fondo_juego, imagenes_objetos
        if nivel == 2:
            pygame.mixer.music.stop()
            sonido_nivel2()
            fondo_juego = fondo_nivel_2
            imagenes_objetos = imagenes_objetos_2
            self.tanque.rect.centerx = ancho // 2 
            self.tanque.rect.bottom = alto  
            self.mostrar_salida_pantalla_negra()
            self.mostrar_cuenta_regresiva()
            self.todos_objetos.empty()
            self.todos_sprites = pygame.sprite.Group(self.tanque)
            self.limite_objetos_actual = 10  
            self.respawn_objetos()
            self.colisiones_activas = True  
            self.disparo_activo = True  

        if nivel == 3:
            pygame.mixer.music.stop()
            sonido_nivel3()
            fondo_juego = fondo_nivel_3
            imagenes_objetos = imagenes_objetos_3
            self.tanque.rect.centerx = ancho // 2  
            self.tanque.rect.bottom = alto  
            self.mostrar_salida_pantalla_negra()
            self.mostrar_cuenta_regresiva()
            self.todos_objetos.empty()
            self.todos_sprites = pygame.sprite.Group(self.tanque)
            self.limite_objetos_actual = 20  
            self.respawn_objetos()
            self.colisiones_activas = True  
            self.disparo_activo = True  

        if nivel == 4:
            pygame.mixer.music.stop()
            sonido_nivel3()  
            try:
                fondo_juego = fondo_nivel_4  
            except pygame.error as e:
                print(f"Error loading image: {e}")
                pygame.quit()
                exit()
            imagenes_objetos = imagenes_objetos_4
            self.tanque.rect.centerx = ancho // 2  
            self.tanque.rect.bottom = alto  
            self.mostrar_salida_pantalla_negra()
            self.mostrar_cuenta_regresiva()
            self.todos_objetos.empty()
            self.todos_sprites = pygame.sprite.Group(self.tanque)
            self.limite_objetos_actual = 60 
            self.respawn_objetos()
            self.colisiones_activas = True  
            self.disparo_activo = True

    def respawn_objetos(self):
        for _ in range(self.limite_objetos_actual):
            objeto = Objeto()
            objeto.image = random.choice(imagenes_objetos) 
            objeto.rect.y = random.randrange(-140, -100) 
            self.todos_sprites.add(objeto)
            self.todos_objetos.add(objeto)

    def mostrar_salida_pantalla_negra(self):
        for altura in range(alto, 0, -20):  
            superficie_transicion = pygame.Surface((ancho, altura))
            superficie_transicion.fill(color_negro)
            interfaz.blit(fondo_juego, [0, 0]) 
            interfaz.blit(superficie_transicion, (0, alto - altura))
            pygame.display.flip()
            pygame.time.delay(50)  

    def mostrar_cuenta_regresiva(self):
        fuente = pygame.font.SysFont("serif", self.tanque.rect.height)  
        
        interfaz.blit(fondo_juego, [0, 0])
        Marcador(interfaz, "Siguiente Nivel, ¡DALO TODO!", 50, ancho // 2, alto // 3)
        pygame.display.flip()
        pygame.time.delay(2000) 

        for numero in range(3, -1, -1):
            interfaz.blit(fondo_juego, [0, 0])
            texto = fuente.render(str(numero), True, color_blanco)
            texto_rect = texto.get_rect(center=(ancho // 2, alto // 2))
            interfaz.blit(texto, texto_rect)
            pygame.display.flip()
            pygame.time.delay(1000)

    def manejar_nivel_2(self):
        if self.nivel == 2 and self.progresivo_objetos:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_ultimo_objeto >= self.intervalo_objetos:
                if len(self.todos_objetos) < self.limite_objetos_actual:
                    self.crear_objeto()
                    self.tiempo_ultimo_objeto = tiempo_actual
                else:
                    self.progresivo_objetos = False

    def manejar_nivel_3(self):
        if self.nivel == 3 and self.progresivo_objetos:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_ultimo_objeto >= self.intervalo_objetos:
                if len(self.todos_objetos) < self.limite_objetos_actual:
                    self.crear_objeto()
                    self.tiempo_ultimo_objeto = tiempo_actual
                else:
                    self.progresivo_objetos = False

    
    def manejar_nivel_4(self):
        if self.nivel == 4 and self.progresivo_objetos:
            tiempo_actual = pygame.time.get_ticks()
            if tiempo_actual - self.tiempo_ultimo_objeto >= self.intervalo_objetos:
                if len(self.todos_objetos) < self.limite_objetos_actual:
                    self.crear_objeto()
                    self.tiempo_ultimo_objeto = tiempo_actual
                else:
                    self.progresivo_objetos = False

class Menu:
    @staticmethod
    def mostrar_menu():
        interfaz.blit(fondo_menu, [0, 0])
        Marcador(interfaz, "Te mueves con las FLECHAS o A,W,S,D y disparas con la BARRA ESPACIADORA o CLICK IZQ, PRESIONA ENTER", 25, ancho // 2, alto * 4.4 / 5)
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
                    if evento.key == pygame.K_RETURN: 
                        esperando = False

def main():
    global juego
    cargar_recursos()
    cargar_sonidos()

    sonido_menu()
    Menu.mostrar_menu()
    Menu.esperar_entrada()
    pygame.mixer.music.stop()

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
            elif not juego.transicion_progresiva:  
                if evento.type == pygame.KEYDOWN and juego.disparo_activo:  
                    if evento.key == pygame.K_SPACE:  
                        juego.tanque.shoot() 
                elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1 and juego.disparo_activo:  
                    juego.tanque.shoot()  

        juego.todos_sprites.update()
        juego.manejar_colisiones()
        juego.incrementar_objetos()
        juego.manejar_transicion()
        juego.manejar_nivel_2()
        juego.manejar_nivel_3()
        juego.manejar_nivel_4()

        interfaz.blit(fondo_juego, [0, 0])
        juego.todos_sprites.draw(interfaz)
        Marcador(interfaz, f"Puntos: {juego.puntos}", 25, ancho // 2, 10)
        Salud(interfaz, 5, 5, juego.tanque.shield) 
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()