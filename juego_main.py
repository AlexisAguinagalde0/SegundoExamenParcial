import pygame
from funciones_juego import *


pygame.init()


ANCHO, ALTO = 1280, 720
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Batalla Naval")


init_fuente()


menu_principal(pantalla)
