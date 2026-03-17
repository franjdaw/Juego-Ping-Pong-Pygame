import pygame
from entidad import Entidad

class Obstaculo(Entidad):
    def __init__(self, x, y, ancho=60, alto=20):
        super().__init__(x, y)
        self.__ancho = ancho
        self.__alto = alto
        self.__activo = True
        self.__vidas = 3
    
    @property
    def ancho(self):
        return self.__ancho
    
    @property
    def alto(self):
        return self.__alto
    
    @property
    def activo(self):
        return self.__activo
    
    @property
    def vidas(self):
        return self.__vidas
    
    def recibir_golpe(self):
        self.__vidas -= 1
        if self.__vidas <= 0:
            self.__activo = False
    
    def dibujar(self, pantalla):
        if not self.__activo:
            return
        
        if self.__vidas == 3:
            color = (150, 75, 0)
        elif self.__vidas == 2:
            color = (200, 100, 0)
        else:
            color = (255, 150, 0)
        
        rect = pygame.Rect(self.x, self.y, self.__ancho, self.__alto)
        pygame.draw.rect(pantalla, color, rect)
        pygame.draw.rect(pantalla, (255, 255, 255), rect, 2)
    
    def verificar_colision(self, pelota):
        if not self.__activo:
            return False
        
        rect = pygame.Rect(self.x, self.y, self.__ancho, self.__alto)
        if rect.collidepoint(pelota.x, pelota.y):
            self.recibir_golpe()
            return True
        return False

class ObstaculoMovil(Obstaculo):
    def __init__(self, x, y, ancho=80, alto=15, velocidad=2):
        super().__init__(x, y, ancho, alto)
        self.__velocidad = velocidad
        self.__direccion = 1
    
    def mover(self, ancho_pantalla):
        self.x += self.__velocidad * self.__direccion
        
        if self.x <= 0 or self.x + self.ancho >= ancho_pantalla:
            self.__direccion *= -1
    
    def dibujar(self, pantalla):
        if not self.activo:
            return
        
        rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        pygame.draw.rect(pantalla, (100, 100, 200), rect)
        pygame.draw.rect(pantalla, (255, 255, 255), rect, 2)
