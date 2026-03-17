import pygame
import random
from pelota import Pelota

class PelotaRapida(Pelota):
    def __init__(self, x, y):
        super().__init__(x, y, radio=8, velocidad=8)
    
    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, (255, 255, 100), (int(self.x), int(self.y)), self.radio)

class PelotaGrande(Pelota):
    def __init__(self, x, y):
        super().__init__(x, y, radio=15, velocidad=3)
    
    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, (100, 255, 100), (int(self.x), int(self.y)), self.radio)

class PelotaZigZag(Pelota):
    def __init__(self, x, y):
        super().__init__(x, y, radio=10, velocidad=5)
        self.__contador = 0
    
    def mover(self):
        super().mover()
        self.__contador += 1
        if self.__contador % 30 == 0:
            self.vel_y *= -1
    
    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, (255, 100, 255), (int(self.x), int(self.y)), self.radio)
