import pygame
from jugador import Jugador
from pelota import Pelota

class Juego:

    def __init__(self, pantalla, ancho, alto):

        self.pantalla = pantalla
        self.ancho = ancho
        self.alto = alto
        self.reloj = pygame.time.Clock()
        self.fps = 60

        self.jugador1 = Jugador(40, alto//2 - 50)
        self.jugador2 = Jugador(ancho-60, alto//2 - 50)
        self.pelota = Pelota(ancho//2, alto//2)

        # 🔥 POLIMORFISMO
        self.entidades = [self.jugador1, self.jugador2, self.pelota]

        self.puntos1 = 0
        self.puntos2 = 0
        self.estado = "inicio"

    def manejar_eventos(self):
        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()

            if evento.type == pygame.KEYDOWN:

                if self.estado == "inicio" and evento.key == pygame.K_SPACE:
                    pygame.mixer.music.play(-1)  # 🔁 música en bucle
                    self.estado = "jugando"

                elif self.estado == "victoria" and evento.key == pygame.K_SPACE:
                    self.reiniciar_juego()
                    self.estado = "jugando"

    def actualizar_juego(self):

        teclas = pygame.key.get_pressed()

        self.jugador1.mover(teclas, pygame.K_w, pygame.K_s, self.alto)
        self.jugador2.mover(teclas, pygame.K_UP, pygame.K_DOWN, self.alto)

        # 🔥 POLIMORFISMO (solo pelota usa mover automático)
        for entidad in self.entidades:
            if isinstance(entidad, Pelota):
                entidad.mover()

        self.pelota.rebote_pared(self.alto)
        self.pelota.rebote_jugador(self.jugador1)
        self.pelota.rebote_jugador(self.jugador2)

        if self.pelota.x < 0:
            self.puntos2 += 1
            self.reiniciar_pelota()

        if self.pelota.x > self.ancho:
            self.puntos1 += 1
            self.reiniciar_pelota()

        if self.puntos1 == 5 or self.puntos2 == 5:
            self.estado = "victoria"

    def reiniciar_pelota(self):
        self.pelota.x = self.ancho//2
        self.pelota.y = self.alto//2

    def reiniciar_juego(self):
        self.puntos1 = 0
        self.puntos2 = 0
        self.reiniciar_pelota()

    def dibujar(self):
        # Fondo gradiente
        for i in range(self.alto):
            color_value = 20 + (i * 20 // self.alto)
            color = (color_value//2, color_value//2, color_value)
            pygame.draw.line(self.pantalla, color, (0, i), (self.ancho, i))

        # Línea central con efecto
        for i in range(0, self.alto, 20):
            pygame.draw.rect(self.pantalla, (80,80,100), (self.ancho//2 - 2, i, 4, 10))

        # 🔥 POLIMORFISMO REAL
        for entidad in self.entidades:
            if isinstance(entidad, Jugador):
                color = (255,120,120) if entidad == self.jugador1 else (120,170,255)
                entidad.dibujar(self.pantalla, color)
            else:
                entidad.dibujar(self.pantalla)

        # Marcador mejorado
        fuente = pygame.font.Font(None, 80)
        marcador = fuente.render(f"{self.puntos1}", True, (255,120,120))
        self.pantalla.blit(marcador, (self.ancho//2 - 100, 30))
        
        marcador2 = fuente.render(f"{self.puntos2}", True, (120,170,255))
        self.pantalla.blit(marcador2, (self.ancho//2 + 60, 30))

        pygame.display.flip()

    def dibujar_intro(self):
        # Fondo gradiente para intro
        for i in range(self.alto):
            color_value = 10 + (i * 30 // self.alto)
            color = (color_value//3, color_value//2, color_value)
            pygame.draw.line(self.pantalla, color, (0, i), (self.ancho, i))

        # Título principal
        fuente_titulo = pygame.font.Font(None, 120)
        titulo = fuente_titulo.render("PONG", True, (255,255,255))
        titulo_rect = titulo.get_rect(center=(self.ancho//2, 150))
        self.pantalla.blit(titulo, titulo_rect)

        # Subtítulo
        fuente_sub = pygame.font.Font(None, 40)
        subtitulo = fuente_sub.render("Clásico Arcade", True, (150,150,180))
        sub_rect = subtitulo.get_rect(center=(self.ancho//2, 220))
        self.pantalla.blit(subtitulo, sub_rect)

        # Instrucciones
        fuente_inst = pygame.font.Font(None, 50)
        texto = fuente_inst.render("Pulsa SPACE para jugar", True, (255,255,255))
        text_rect = texto.get_rect(center=(self.ancho//2, 350))
        self.pantalla.blit(texto, text_rect)

        # Controles
        fuente_controles = pygame.font.Font(None, 30)
        controles1 = fuente_controles.render("Jugador 1: W/S", True, (255,120,120))
        controles2 = fuente_controles.render("Jugador 2: ↑/↓", True, (120,170,255))
        self.pantalla.blit(controles1, (self.ancho//2 - 200, 420))
        self.pantalla.blit(controles2, (self.ancho//2 + 50, 420))

        # Efecto de parpadeo
        import time
        if int(time.time() * 2) % 2 == 0:
            pygame.draw.circle(self.pantalla, (255,255,255), (self.ancho//2, 350), 8)

    def dibujar_victoria(self):
        # Fondo gradiente para victoria
        for i in range(self.alto):
            color_value = 15 + (i * 25 // self.alto)
            color = (color_value//2, color_value//3, color_value//2)
            pygame.draw.line(self.pantalla, color, (0, i), (self.ancho, i))

        # Título de victoria
        fuente_titulo = pygame.font.Font(None, 100)
        titulo = fuente_titulo.render("¡VICTORIA!", True, (255,215,0))
        titulo_rect = titulo.get_rect(center=(self.ancho//2, 150))
        self.pantalla.blit(titulo, titulo_rect)

        # Ganador
        fuente_ganador = pygame.font.Font(None, 80)
        ganador = "Jugador 1" if self.puntos1 > self.puntos2 else "Jugador 2"
        color_ganador = (255,120,120) if self.puntos1 > self.puntos2 else (120,170,255)
        texto_ganador = fuente_ganador.render(f"Gana {ganador}", True, color_ganador)
        ganador_rect = texto_ganador.get_rect(center=(self.ancho//2, 250))
        self.pantalla.blit(texto_ganador, ganador_rect)

        # Puntuación final
        fuente_puntos = pygame.font.Font(None, 60)
        texto_puntos = fuente_puntos.render(f"{self.puntos1} - {self.puntos2}", True, (200,200,200))
        puntos_rect = texto_puntos.get_rect(center=(self.ancho//2, 330))
        self.pantalla.blit(texto_puntos, puntos_rect)

        # Instrucción para reiniciar
        fuente_inst = pygame.font.Font(None, 40)
        texto_inst = fuente_inst.render("Pulsa SPACE para jugar otra vez", True, (255,255,255))
        inst_rect = texto_inst.get_rect(center=(self.ancho//2, 420))
        self.pantalla.blit(texto_inst, inst_rect)

        # Efectos decorativos
        import time
        if int(time.time() * 3) % 2 == 0:
            pygame.draw.circle(self.pantalla, (255,215,0), (self.ancho//2, 420), 6)

    def iniciar(self):

        while True:

            self.manejar_eventos()

            if self.estado == "inicio":
                self.dibujar_intro()
                pygame.display.flip()

            elif self.estado == "jugando":
                self.actualizar_juego()
                self.dibujar()

            elif self.estado == "victoria":
                self.dibujar_victoria()
                pygame.display.flip()

            self.reloj.tick(self.fps)