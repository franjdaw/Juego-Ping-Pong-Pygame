import pygame
import random
import math
from entidad import Entidad

class PowerUp(Entidad):
    def __init__(self, x, y, tipo="velocidad"):
        super().__init__(x, y)
        self.__tipo = tipo
        self.__radio = 15
        self.__activo = True
        self.__brillo = 0
        
        # Colores según tipo
        if tipo == "velocidad":
            self.__color = (255, 200, 0)  # Dorado
        elif tipo == "tamaño":
            self.__color = (0, 200, 255)  # Azul
        else:  # punto_extra
            self.__color = (255, 0, 255)  # Magenta
    
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
        if not self.__activo:
            return
        
        # Actualizar brillo
        self.__brillo = (self.__brillo + 5) % 360
        brillo_valor = abs(math.sin(math.radians(self.__brillo)))
        radio_brillo = self.__radio + int(brillo_valor * 3)
        
        # Dibujar anillos simples
        for i in range(2):
            radio_anillo = self.__radio + (i + 1) * 3
            color_anillo = tuple(int(c * 50 / 255) for c in self.__color)
            pygame.draw.circle(pantalla, color_anillo,
                             (int(self.x), int(self.y)), radio_anillo, 1)
        
        # Dibujar power-up principal
        pygame.draw.circle(pantalla, self.__color,
                         (int(self.x), int(self.y)), radio_brillo)
        pygame.draw.circle(pantalla, (255, 255, 255),
                         (int(self.x), int(self.y)), radio_brillo, 2)
        
        # Símbolo simple
        self._dibujar_simbolo_simple(pantalla)
    
    def _dibujar_simbolo_simple(self, pantalla):
        centro_x, centro_y = int(self.x), int(self.y)
        
        if self.__tipo == "velocidad":
            # Flecha simple
            pygame.draw.polygon(pantalla, (255, 255, 255), [
                (centro_x, centro_y - 8),
                (centro_x - 4, centro_y),
                (centro_x + 4, centro_y)
            ], 2)
        elif self.__tipo == "tamaño":
            # Círculos simples
            pygame.draw.circle(pantalla, (255, 255, 255),
                             (centro_x, centro_y), 4, 2)
            pygame.draw.circle(pantalla, (255, 255, 255),
                             (centro_x, centro_y), 7, 2)
        else:  # punto_extra
            # Estrella simple
            puntos = []
            for i in range(8):
                angulo = math.radians(i * 45 - 90)
                radio = 8 if i % 2 == 0 else 4
                x = centro_x + int(radio * math.cos(angulo))
                y = centro_y + int(radio * math.sin(angulo))
                puntos.append((x, y))
            pygame.draw.polygon(pantalla, (255, 255, 255), puntos, 2)
    
    def verificar_colision(self, pelota):
        if not self.__activo:
            return False
        
        distancia = ((self.x - pelota.x)**2 + (self.y - pelota.y)**2)**0.5
        if distancia < self.__radio + pelota.radio:
            self.desactivar()
            return True
        return False
