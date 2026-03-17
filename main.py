import pygame
from juego import Juego

def main():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("assets/sounds/musica.mp3")

    ancho, alto = 800, 600
    pantalla = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Pong con POO")

    juego = Juego(pantalla, ancho, alto)
    juego.iniciar()

if __name__ == "__main__":
    main()