import pygame
import random
from entidad import Entidad

class PowerUp(Entidad):
    def __init__(self, x, y, tipo="velocidad"):
        super().__init__(x, y)
        self.__tipo = tipo
        self.__radio = 15
        self.__activo = True
        
        if tipo == "velocidad":
            self.__color = (255, 200, 0)
        elif tipo == "tamaño":
            self.__color = (0, 200, 255)
        else:
            self.__color = (255, 0, 255)
    
    @property
    def tipo(self):
        return self.__tipo
    
    @property
    def radio(self):
        return self.__radio
    
    @property
    def activo(self):
        return self.__activo
    
    def desactivar(self):
        self.__activo = False
    
    def dibujar(self, pantalla):
        if self.__activo:
            pygame.draw.circle(pantalla, self.__color, (int(self.x), int(self.y)), self.__radio)
            pygame.draw.circle(pantalla, (255, 255, 255), (int(self.x), int(self.y)), self.__radio, 2)
    
    def verificar_colision(self, pelota):
        if not self.__activo:
            return False
        
        distancia = ((self.x - pelota.x)**2 + (self.y - pelota.y)**2)**0.5
        if distancia < self.__radio + pelota.radio:
            self.desactivar()
            return True
        return False
