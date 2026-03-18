import pygame
import random
import math
from entidad import Entidad

class Pelota(Entidad):
    def __init__(self, x, y, radio=10, velocidad=5):
        super().__init__(x, y)
        self.__radio = radio
        self.__velocidad = velocidad
        self.__vel_x = random.choice([-1,1]) * velocidad
        self.__vel_y = random.choice([-1,1]) * velocidad
        
        # Efectos simples
        self.__estela = []
        self.__brillo = 0
    
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
        # Guardar estela
        self.__estela.append((self.x, self.y))
        if len(self.__estela) > 5:
            self.__estela.pop(0)
        
        # Mover
        self.x += self.__vel_x
        self.y += self.__vel_y
        
        # Actualizar brillo
        self.__brillo = (self.__brillo + 5) % 360

    def dibujar(self, pantalla):
        # Estela simple
        for i, (pos_x, pos_y) in enumerate(self.__estela):
            alpha = int(50 * (i + 1) / len(self.__estela))
            color = (alpha, alpha, alpha)
            radio = int(self.__radio * 0.5 * (i + 1) / len(self.__estela))
            pygame.draw.circle(pantalla, color, (int(pos_x), int(pos_y)), radio)
        
        # Efecto de brillo
        brillo_valor = abs(math.sin(math.radians(self.__brillo)))
        radio_brillo = self.__radio + int(brillo_valor * 2)
        color = (255, 255, 255)
        
        # Dibujar pelota
        pygame.draw.circle(pantalla, color, (int(self.x), int(self.y)), radio_brillo)
        pygame.draw.circle(pantalla, (255, 255, 255), (int(self.x), int(self.y)), self.__radio // 2)

    def rebote_pared(self, alto):
        if self.y <= self.__radio or self.y >= alto - self.__radio:
            self.__vel_y *= -1

    def rebote_jugador(self, jugador):
        rect_jugador = pygame.Rect(jugador.x, jugador.y, jugador.ancho, jugador.alto)
        rect_pelota = pygame.Rect(self.x - self.__radio, self.y - self.__radio, 
                                 self.__radio * 2, self.__radio * 2)
        
        if rect_jugador.colliderect(rect_pelota):
            self.__vel_x *= -1
            
            # Spin simple
            centro_jugador = jugador.y + jugador.alto // 2
            impacto = (self.y - centro_jugador) / (jugador.alto // 2)
            self.__vel_y += impacto * 2
            self.__vel_y = max(-6, min(6, self.__vel_y))