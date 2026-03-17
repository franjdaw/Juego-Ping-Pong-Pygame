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

        self.pantalla.fill((30,30,40))

        pygame.draw.line(self.pantalla,(200,200,200),(self.ancho//2,0),(self.ancho//2,self.alto),3)

        # 🔥 POLIMORFISMO REAL
        for entidad in self.entidades:
            if isinstance(entidad, Jugador):
                color = (255,120,120) if entidad == self.jugador1 else (120,170,255)
                entidad.dibujar(self.pantalla, color)
            else:
                entidad.dibujar(self.pantalla)

        fuente = pygame.font.Font(None, 60)
        marcador = fuente.render(f"{self.puntos1} - {self.puntos2}", True, (255,255,255))
        self.pantalla.blit(marcador, (self.ancho//2 - 70, 20))

        pygame.display.flip()

    def iniciar(self):

        while True:

            self.manejar_eventos()

            if self.estado == "inicio":
                self.pantalla.fill((20,20,30))

                fuente = pygame.font.Font(None, 70)
                texto = fuente.render("Pulsa SPACE para jugar", True, (255,255,255))
                self.pantalla.blit(texto, (200, 250))

                pygame.display.flip()

            elif self.estado == "jugando":
                self.actualizar_juego()
                self.dibujar()

            elif self.estado == "victoria":
                self.pantalla.fill((20,20,30))

                fuente = pygame.font.Font(None, 70)
                ganador = "Jugador 1" if self.puntos1 > self.puntos2 else "Jugador 2"
                texto = fuente.render(f"Gana {ganador}", True, (255,255,255))

                self.pantalla.blit(texto, (250, 250))
                pygame.display.flip()

            self.reloj.tick(self.fps)