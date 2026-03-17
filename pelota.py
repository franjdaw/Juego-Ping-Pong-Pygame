import pygame
import random
from entidad import Entidad

class Pelota(Entidad):
    def __init__(self, x, y, radio=10, velocidad=5):
        super().__init__(x, y)
        self.radio = radio
        self.velocidad = velocidad
        self.vel_x = random.choice([-1,1]) * velocidad
        self.vel_y = random.choice([-1,1]) * velocidad

    def mover(self):
        self.x += self.vel_x
        self.y += self.vel_y

    def dibujar(self, pantalla):
        # Sombra
        pygame.draw.circle(pantalla, (10,10,20), (int(self.x + 2), int(self.y + 2)), self.radio + 2)
        # Brillo exterior
        pygame.draw.circle(pantalla, (150,150,180), (int(self.x), int(self.y)), self.radio + 1)
        # Principal
        pygame.draw.circle(pantalla, (255,255,255), (int(self.x), int(self.y)), self.radio)
        # Brillo central
        pygame.draw.circle(pantalla, (255,255,255), (int(self.x - 3), int(self.y - 3)), 3)

    def rebote_pared(self, alto):
        if self.y <= 0 or self.y >= alto:
            self.vel_y *= -1

    def rebote_jugador(self, jugador):
        if pygame.Rect(jugador.x, jugador.y, jugador.ancho, jugador.alto).collidepoint(self.x, self.y):
            self.vel_x *= -1