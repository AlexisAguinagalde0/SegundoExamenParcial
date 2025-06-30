"""
Este archivo es el punto de entrada del juego Batalla Naval. Configura la ventana de Pygame,
carga imágenes de fondo, inicia la fuente y muestra el menú principal.
"""

import pygame
pygame.init()
from funciones import * 
init_fuente()
from pantallas import *

pygame.mixer.init()
pygame.mixer.music.load(r"E:\Nueva carpeta\SegundoExamenParcial\SegundoExamenParcial\archivos_multimedia\thunderstruck_fondo.mp3")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)  

ANCHO, ALTO = 1280, 720                                 #Dimensiones de la pantalla de juego
pantalla = pygame.display.set_mode((ANCHO, ALTO))       #Crea la ventana de juego con las dimensiones ya pasadas
pygame.display.set_caption("Batalla Naval")             #Agrega el titulo a la ventana

explosion_frames = cargar_animacion_explosion()                                         #Llama a la funcion para cargar los frames y guardarlos en una lista
fondo = pygame.image.load(r"E:\Nueva carpeta\SegundoExamenParcial\SegundoExamenParcial\archivos_multimedia\fondo_menu_inicial.png")
fondo = pygame.transform.scale(fondo, pantalla.get_size())                               #Carga la imagen del menu y la redimensiona

fondo_juego = pygame.image.load(r"E:\Nueva carpeta\SegundoExamenParcial\SegundoExamenParcial\archivos_multimedia\fondo_juego_naval.png")  
fondo_juego = pygame.transform.scale(fondo_juego, pantalla.get_size())                   #Carga la imagen del fondo de juego y la redimendiiona

menu_principal(pantalla, fondo, fondo_juego, explosion_frames)                  #Llama a la funcion del menu principal y le pasa la pantalla de juego, 
                                                                                #el fondo tanto de menu como de juego y los frames de explosiones para usarlos.
