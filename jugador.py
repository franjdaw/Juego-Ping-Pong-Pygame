import pygame
from entidad import Entidad

class Jugador(Entidad):
    def __init__(self, x, y, ancho=20, alto=100, velocidad=6):
        super().__init__(x, y)
        self.ancho = ancho
        self.alto = alto
        self.velocidad = velocidad
        self.rect = pygame.Rect(self.x, self.y, ancho, alto)

    def mover(self, teclas, tecla_arriba, tecla_abajo, alto_pantalla):
        if teclas[tecla_arriba] and self.y > 0:
            self.y -= self.velocidad
        if teclas[tecla_abajo] and self.y < alto_pantalla - self.alto:
            self.y += self.velocidad

        self.rect.topleft = (self.x, self.y)

    def dibujar(self, pantalla, color=(255,255,255)):
        pygame.draw.rect(pantalla, (200,200,200), self.rect.inflate(4,4))
        pygame.draw.rect(pantalla, color, self.rect)