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
        # Sombra sutil
        shadow_rect = self.rect.inflate(6,6)
        shadow_rect.x += 3
        shadow_rect.y += 3
        pygame.draw.rect(pantalla, (10,10,20), shadow_rect, border_radius=3)
        
        # Borde exterior
        pygame.draw.rect(pantalla, (100,100,120), self.rect.inflate(4,4), border_radius=2)
        # Principal
        pygame.draw.rect(pantalla, color, self.rect, border_radius=2)
        # Brillo sutil
        highlight_rect = pygame.Rect(self.rect.x + 2, self.rect.y + 2, self.rect.width - 4, 10)
        pygame.draw.rect(pantalla, (*color, 50), highlight_rect, border_radius=2)