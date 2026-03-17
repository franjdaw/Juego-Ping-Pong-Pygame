import pygame
import random
from entidad import Entidad

class Pelota(Entidad):
    def __init__(self, x, y, radio=10, velocidad=5):
        super().__init__(x, y)
        self.__radio = radio
        self.__velocidad = velocidad
        self.__vel_x = random.choice([-1,1]) * velocidad
        self.__vel_y = random.choice([-1,1]) * velocidad

    @property
    def radio(self):
        return self.__radio

    @property
    def velocidad(self):
        return self.__velocidad

    @property
    def vel_x(self):
        return self.__vel_x

    @vel_x.setter
    def vel_x(self, value):
        self.__vel_x = value

    @property
    def vel_y(self):
        return self.__vel_y

    @vel_y.setter
    def vel_y(self, value):
        self.__vel_y = value

    def mover(self):
        self.x += self.__vel_x
        self.y += self.__vel_y

    def dibujar(self, pantalla):
        # Pelota simple
        pygame.draw.circle(pantalla, (255,255,255), (int(self.x), int(self.y)), self.__radio)

    def rebote_pared(self, alto):
        if self.y <= 0 or self.y >= alto:
            self.__vel_y *= -1

    def rebote_jugador(self, jugador):
        if pygame.Rect(jugador.x, jugador.y, jugador.ancho, jugador.alto).collidepoint(self.x, self.y):
            self.__vel_x *= -1