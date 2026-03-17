import pygame
from entidad import Entidad

class Jugador(Entidad):
    def __init__(self, x, y, ancho=20, alto=100, velocidad=6):
        super().__init__(x, y)
        self.__ancho = ancho
        self.__alto = alto
        self.__velocidad = velocidad
        self.rect = pygame.Rect(self.x, self.y, ancho, alto)

    @property
    def ancho(self):
        return self.__ancho

    @property
    def alto(self):
        return self.__alto

    @property
    def velocidad(self):
        return self.__velocidad

    def mover(self, teclas, tecla_arriba, tecla_abajo, alto_pantalla):
        if teclas[tecla_arriba] and self.y > 0:
            self.y -= self.__velocidad
        if teclas[tecla_abajo] and self.y < alto_pantalla - self.__alto:
            self.y += self.__velocidad

        self.rect.topleft = (self.x, self.y)

    def dibujar(self, pantalla, color=(255,255,255)):

        pygame.draw.rect(pantalla, color, self.rect)
        pygame.draw.rect(pantalla, (255,255,255), self.rect, 2)