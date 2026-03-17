import pygame
import random
from jugador import Jugador
from pelota import Pelota
from pelota_especial import PelotaRapida, PelotaGrande, PelotaZigZag
from powerup import PowerUp
from obstaculo import Obstaculo, ObstaculoMovil

class Juego:

    def __init__(self, pantalla, ancho, alto):

        self.pantalla = pantalla
        self.ancho = ancho
        self.alto = alto
        self.reloj = pygame.time.Clock()
        self.fps = 60
        
        # Cargar fuente personalizada
        try:
            self.fuente_personalizada = pygame.font.Font("assets/ASMAN.TTF", 60)
            self.fuente_pequena = pygame.font.Font("assets/ASMAN.TTF", 25)
            self.fuente_grande = pygame.font.Font("assets/ASMAN.TTF", 80)
            self.fuente_titulo = pygame.font.Font("assets/ASMAN.TTF", 100)
        except:
            # Si no se puede cargar, usar fuente por defecto
            self.fuente_personalizada = pygame.font.Font(None, 60)
            self.fuente_pequena = pygame.font.Font(None, 25)
            self.fuente_grande = pygame.font.Font(None, 80)
            self.fuente_titulo = pygame.font.Font(None, 100)

        self.jugador1 = Jugador(40, alto//2 - 50)
        self.jugador2 = Jugador(ancho-60, alto//2 - 50)
        self.pelota = Pelota(ancho//2, alto//2)

        #   Polimorfismo
        self.entidades = [self.jugador1, self.jugador2, self.pelota]

        # Sistema de vidas
        self.vidas1 = 3
        self.vidas2 = 3
        
        # Power-ups y obstáculos
        self.powerups = []
        self.obstaculos = []
        self.powerup_timer = 0
        self.obstaculo_timer = 0

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

        # Polimorfismo
        for entidad in self.entidades:
            if isinstance(entidad, Pelota):
                entidad.mover()

        self.pelota.rebote_pared(self.alto)
        self.pelota.rebote_jugador(self.jugador1)
        self.pelota.rebote_jugador(self.jugador2)

        # Generar power-ups periódicamente
        self.powerup_timer += 1
        if self.powerup_timer > 300:  # Cada 5 segundos
            self.generar_powerup()
            self.powerup_timer = 0

        # Generar obstáculos periódicamente
        self.obstaculo_timer += 1
        if self.obstaculo_timer > 600:  # Cada 10 segundos
            self.generar_obstaculo()
            self.obstaculo_timer = 0

        # Actualizar obstáculos móviles
        for obstaculo in self.obstaculos:
            if isinstance(obstaculo, ObstaculoMovil):
                obstaculo.mover(self.ancho)

        # Verificar colisiones con power-ups
        for powerup in self.powerups[:]:
            if powerup.verificar_colision(self.pelota):
                self.aplicar_powerup(powerup.tipo)
                self.powerups.remove(powerup)

        # Verificar colisiones con obstáculos
        for obstaculo in self.obstaculos:
            if obstaculo.verificar_colision(self.pelota):
                self.pelota.vel_x *= -1

        # Limpiar power-ups e obstáculos inactivos
        self.powerups = [p for p in self.powerups if p.activo]
        self.obstaculos = [o for o in self.obstaculos if o.activo]

        if self.pelota.x < 0:
            self.puntos2 += 1
            self.vidas1 -= 1
            if self.vidas1 <= 0:
                self.estado = "victoria"
            else:
                self.reiniciar_pelota()

        if self.pelota.x > self.ancho:
            self.puntos1 += 1
            self.vidas2 -= 1
            if self.vidas2 <= 0:
                self.estado = "victoria"
            else:
                self.reiniciar_pelota()

        if self.puntos1 == 5 or self.puntos2 == 5:
            self.estado = "victoria"

    def reiniciar_pelota(self):
        self.pelota.x = self.ancho//2
        self.pelota.y = self.alto//2

    def reiniciar_juego(self):
        self.puntos1 = 0
        self.puntos2 = 0
        self.vidas1 = 3
        self.vidas2 = 3
        self.powerups.clear()
        self.obstaculos.clear()
        self.powerup_timer = 0
        self.obstaculo_timer = 0
        self.reiniciar_pelota()

    def generar_powerup(self):
        if len(self.powerups) < 3:  # Máximo 3 power-ups
            tipos = ["velocidad", "tamaño", "punto_extra"]
            tipo = random.choice(tipos)
            x = random.randint(100, self.ancho - 100)
            y = random.randint(100, self.alto - 100)
            self.powerups.append(PowerUp(x, y, tipo))

    def generar_obstaculo(self):
        if len(self.obstaculos) < 2:  # Máximo 2 obstáculos
            if random.random() < 0.5:
                # Obstáculo estático
                x = random.randint(200, self.ancho - 200)
                y = random.randint(100, self.alto - 100)
                self.obstaculos.append(Obstaculo(x, y))
            else:
                # Obstáculo móvil
                x = random.randint(100, self.ancho - 100)
                y = random.randint(100, self.alto - 100)
                self.obstaculos.append(ObstaculoMovil(x, y))

    def aplicar_powerup(self, tipo):
        if tipo == "velocidad":
            # Cambiar a pelota rápida
            self.entidades.remove(self.pelota)
            self.pelota = PelotaRapida(self.pelota.x, self.pelota.y)
            self.entidades.append(self.pelota)
        elif tipo == "tamaño":
            # Cambiar a pelota grande
            self.entidades.remove(self.pelota)
            self.pelota = PelotaGrande(self.pelota.x, self.pelota.y)
            self.entidades.append(self.pelota)
        elif tipo == "punto_extra":
            # Cambiar a pelota zigzag
            self.entidades.remove(self.pelota)
            self.pelota = PelotaZigZag(self.pelota.x, self.pelota.y)
            self.entidades.append(self.pelota)

    def dibujar(self):
        # Fondo simple
        self.pantalla.fill((20, 20, 30))
        
        # Línea central simple
        pygame.draw.line(self.pantalla, (100, 100, 100), 
                        (self.ancho//2, 0), (self.ancho//2, self.alto), 2)

        # Dibujar obstáculos
        for obstaculo in self.obstaculos:
            obstaculo.dibujar(self.pantalla)

        # Dibujar power-ups
        for powerup in self.powerups:
            powerup.dibujar(self.pantalla)

        # Dibujar entidades
        for entidad in self.entidades:
            if isinstance(entidad, Jugador):
                color = (255, 120, 120) if entidad == self.jugador1 else (120, 170, 255)
                entidad.dibujar(self.pantalla, color)
            else:
                entidad.dibujar(self.pantalla)

        # Marcador con fuente personalizada
        marcador = self.fuente_grande.render(f"{self.puntos1} - {self.puntos2}", True, (255, 255, 255))
        self.pantalla.blit(marcador, (self.ancho//2 - 40, 20))

        # Sistema de vidas con fuente personalizada
        vidas1_texto = self.fuente_pequena.render(f"Vidas: {self.vidas1}", True, (255, 120, 120))
        vidas2_texto = self.fuente_pequena.render(f"Vidas: {self.vidas2}", True, (120, 170, 255))
        self.pantalla.blit(vidas1_texto, (20, 80))
        self.pantalla.blit(vidas2_texto, (self.ancho - 100, 80))

        pygame.display.flip()

    def dibujar_intro(self):
        self.pantalla.fill((20, 20, 30))
        
        # Título con fuente personalizada
        titulo = self.fuente_titulo.render("PONG", True, (255, 255, 255))
        titulo_rect = titulo.get_rect(center=(self.ancho//2, 200))
        self.pantalla.blit(titulo, titulo_rect)
        
        # Instrucciones con fuente personalizada
        texto = self.fuente_personalizada.render("Pulsa SPACE para jugar", True, (255, 255, 255))
        text_rect = texto.get_rect(center=(self.ancho//2, 300))
        self.pantalla.blit(texto, text_rect)
        
        # Controles con fuente personalizada
        controles1 = self.fuente_pequena.render("Jugador 1: W/S", True, (255, 120, 120))
        controles2 = self.fuente_pequena.render("Jugador 2: ↑/↓", True, (120, 170, 255))
        self.pantalla.blit(controles1, (self.ancho//2 - 150, 380))
        self.pantalla.blit(controles2, (self.ancho//2 + 30, 380))

    def dibujar_victoria(self):
        self.pantalla.fill((20, 20, 30))
        
        # Título con fuente personalizada
        titulo = self.fuente_titulo.render("¡VICTORIA!", True, (255, 215, 0))
        titulo_rect = titulo.get_rect(center=(self.ancho//2, 150))
        self.pantalla.blit(titulo, titulo_rect)
        
        # Ganador con fuente personalizada
        ganador = "Jugador 1" if self.puntos1 > self.puntos2 else "Jugador 2"
        color_ganador = (255, 120, 120) if self.puntos1 > self.puntos2 else (120, 170, 255)
        texto_ganador = self.fuente_grande.render(f"Gana {ganador}", True, color_ganador)
        ganador_rect = texto_ganador.get_rect(center=(self.ancho//2, 250))
        self.pantalla.blit(texto_ganador, ganador_rect)
        
        # Puntuación final con fuente personalizada
        texto_puntos = self.fuente_grande.render(f"{self.puntos1} - {self.puntos2}", True, (255, 255, 255))
        puntos_rect = texto_puntos.get_rect(center=(self.ancho//2, 330))
        self.pantalla.blit(texto_puntos, puntos_rect)
        
        # Instrucción para reiniciar con fuente personalizada
        texto_inst = self.fuente_pequena.render("Pulsa SPACE para jugar otra vez", True, (255, 255, 255))
        inst_rect = texto_inst.get_rect(center=(self.ancho//2, 400))
        self.pantalla.blit(texto_inst, inst_rect)

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
