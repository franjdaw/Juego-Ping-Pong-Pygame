import pygame
import random
from entidad import Entidad

class Obstaculo(Entidad):
    def __init__(self, x, y, ancho=60, alto=20):
        super().__init__(x, y)
        self.__ancho = ancho
        self.__alto = alto
        self.__activo = True
        self.__vidas = 3
        self.__brillo = 0
    
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
        
        # Actualizar brillo
        self.__brillo = (self.__brillo + 3) % 360
        brillo_valor = abs(pygame.math.Vector2(1, 0).rotate(self.__brillo).x)
        
        # Color según vidas
        if self.__vidas == 3:
            color = (180, 100, 50)
        elif self.__vidas == 2:
            color = (220, 150, 80)
        else:
            color = (255, 200, 100)
        
        # Aplicar brillo
        color = tuple(min(255, c + int(brillo_valor * 20)) for c in color)
        
        # Dibujar
        rect = pygame.Rect(self.x, self.y, self.__ancho, self.__alto)
        pygame.draw.rect(pantalla, color, rect)
        pygame.draw.rect(pantalla, (255, 255, 255), rect, 2)
    
    def verificar_colision(self, pelota):
        if not self.__activo:
            return False
        
        rect_obstaculo = pygame.Rect(self.x, self.y, self.__ancho, self.__alto)
        rect_pelota = pygame.Rect(pelota.x - pelota.radio, pelota.y - pelota.radio, 
                                 pelota.radio * 2, pelota.radio * 2)
        
        if rect_obstaculo.colliderect(rect_pelota):
            # Solo hacer rebotar, no quitar vidas
            
            # Calcular desde qué lado viene la pelota
            centro_obstaculo_x = self.x + self.__ancho // 2
            centro_obstaculo_y = self.y + self.__alto // 2
            
            dx = pelota.x - centro_obstaculo_x
            dy = pelota.y - centro_obstaculo_y
            
            # Rebote según el lado de impacto
            if abs(dx) > abs(dy):  # Golpe lateral
                pelota.vel_x *= -1
                # Empujar pelota fuera del obstáculo
                if dx > 0:
                    pelota.x = self.x + self.__ancho + pelota.radio
                else:
                    pelota.x = self.x - pelota.radio
            else:  # Golpe superior/inferior
                pelota.vel_y *= -1
                # Empujar pelota fuera del obstáculo
                if dy > 0:
                    pelota.y = self.y + self.__alto + pelota.radio
                else:
                    pelota.y = self.y - pelota.radio
            
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
        
        # Color azul brillante
        rect = pygame.Rect(self.x, self.y, self.ancho, self.alto)
        pygame.draw.rect(pantalla, (100, 150, 255), rect)
        pygame.draw.rect(pantalla, (255, 255, 255), rect, 2)
