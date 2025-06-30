import pygame
import sys
from funciones import *
import os
RUTA_MEDIA = os.path.join(os.path.dirname(__file__), "archivos_multimedia")


BLANCO = (255, 255, 255)
AZUL_OSCURO = (10, 40, 100)                 #Se define los colores para llamarlos en las diferentes funciones
AZUL_CLARO = (50, 100, 200)

def dibujar_tablero_con_textos(pantalla, matriz, x_inicio, y_inicio, TAM_CASILLA, fondo_juego, puntaje, mensaje, contador_mensaje, nombre, imagen_misil, boton_reiniciar, boton_mute):
    if fondo_juego:
        pantalla.blit(fondo_juego, (0, 0))
    else:
        pantalla.fill(AZUL_OSCURO)

    # Dibujar el tablero
    for fila in range(len(matriz)):
        for col in range(len(matriz[0])):
            valor = matriz[fila][col]
            x = x_inicio + col * TAM_CASILLA
            y = y_inicio + fila * TAM_CASILLA

            color = color_por_valor(valor)

            pygame.draw.rect(pantalla, color, (x, y, TAM_CASILLA, TAM_CASILLA))
            pygame.draw.rect(pantalla, BLANCO, (x, y, TAM_CASILLA, TAM_CASILLA), 1)

    # Texto: naves restantes
    naves_restantes = contar_naves_vivas(matriz)
    tam_fuente = max(24, pantalla.get_height() // 30)
    fuente_dinamica = pygame.font.SysFont("arial", tam_fuente)

    texto_naves = fuente_dinamica.render(f"Naves restantes: {naves_restantes}", True, (255, 255, 0))
    pantalla.blit(texto_naves, (20, 20 + tam_fuente + 10))

    # Texto: info
    texto_info = fuente_dinamica.render("Presione ESC para volver", True, BLANCO)
    pantalla.blit(texto_info, (20, 20 + tam_fuente * 2 + 20))

    # Texto: puntaje
    texto_puntaje = fuente_dinamica.render(f"Puntaje: {puntaje:04}", True, (0, 255, 0))
    pantalla.blit(texto_puntaje, (20, 20))

    # Texto: mensaje temporal (nave hundida)
    if contador_mensaje > 0:
        texto_hundida = fuente.render(mensaje, True, (255, 255, 0))
        pantalla.blit(texto_hundida, (10, 90))

    # Si todas las naves fueron hundidas (mostrar mensaje final, en caso de que quieras usar desde animación)
    if naves_restantes == 0:
        mensaje_final = f"¡Has hundido todas las naves, {nombre}! Puntaje final: {puntaje:04}"
        texto_final = fuente_dinamica.render(mensaje_final, True, (255, 255, 255))
        pantalla.blit(texto_final, (pantalla.get_width() // 2 - texto_final.get_width() // 2,
                                    pantalla.get_height() // 2))
    # Dibujar botón Reiniciar
    crear_boton(pantalla, "Reiniciar", boton_reiniciar.x, boton_reiniciar.y, boton_reiniciar.width, boton_reiniciar.height)

    # Dibujar botón Mute
    texto_mute = "🔇" if pygame.mixer.music.get_volume() > 0 else "🔊"
    crear_boton(pantalla, texto_mute, boton_mute.x, boton_mute.y, boton_mute.width, boton_mute.height)

    # Dibujar cursor (misil)
    pos_mouse = pygame.mouse.get_pos()
    pantalla.blit(imagen_misil, (pos_mouse[0] - 16, pos_mouse[1] - 16))



def cargar_animacion_explosion():
    """
    Carga los frames de la animación de explosión desde archivos de imagen.

    Retorna:
        list: Lista de superficies (imagenes) que componen la animación.
    """
    frames = []                                                                                                 #Se inicia una lista que guarda las imagenes
    for i in range(6):                                                                                           # itera segun la cantidad de imagenes pasadas
        ruta = os.path.join(RUTA_MEDIA, "explosiones", f"explosion_{i + 1}.jpg")
        frame = pygame.image.load(ruta).convert_alpha()          #Carga la imagen y mantiene la transparencia
        frame = pygame.transform.scale(frame, (40, 40))          #Ajustá el tamaño a segun cada casillero
        frames.append(frame)                                     #Guarda cada frame en la lista
    return frames                                                #Retorna la lista con los frames para usar como animacion

def animar_explosion_en_casillas(pantalla, matriz, valor_hundido, tam_casilla, x_inicio, y_inicio, frames, fondo_juego, puntaje, mensaje, contador_mensaje, nombre, imagen_misil, boton_reiniciar, boton_mute):
    """
    Reproduce la animación de explosión en las casillas que coinciden con un valor hundido.

    Argumentos:
        pantalla (Surface): Superficie de juego.
        matriz (list): Matriz del juego.
        valor_hundido (int): Valor representando partes hundidas de una nave.
        tam_casilla (int): Tamaño de cada casilla.
        x_inicio (int): Posición inicial en X del tablero.
        y_inicio (int): Posición inicial en Y del tablero.
        frames (list): Lista de imágenes para la animación.
        fondo_juego (Surface): Imagen de fondo (opcional).

    Retorna:
        No retorna. Dibuja en pantalla.
    """
    posiciones = []                                                                 #Crea una lista para guardar las coordenadas de cada parte de nave hundida
    for fila in range(len(matriz)):
        for col in range(len(matriz[0])):                                           #Recorre filas por columnas de la matriz
            if matriz[fila][col] == valor_hundido:                                  #Pregutna casillas que tengan partes de nave hundida
                x = x_inicio + col * tam_casilla                                    #Calcula la posicion en pixeles usando el tamaño de la casilla y la posicion de inicio
                y = y_inicio + fila * tam_casilla
                posiciones.append((x, y))                                           #Guarda las coordenadas en la lista posiciones

    for frame in frames:
        dibujar_tablero_con_textos(pantalla, matriz, x_inicio, y_inicio, tam_casilla, fondo_juego, puntaje, mensaje, contador_mensaje, nombre, imagen_misil, boton_reiniciar, boton_mute)
                                                                # Dibujar la explosión encima
        for x, y in posiciones:
            frame_ancho, frame_alto = frame.get_size()
            x_centrado = x + (tam_casilla - frame_ancho) // 2           #Centra la imagen dentro de cada casilla y la dibuja encima del tablero con el blit
            y_centrado = y + (tam_casilla - frame_alto) // 2
            pantalla.blit(frame, (x_centrado, y_centrado))


        pygame.display.flip()                                   #Actualiza la pantalla 
        pygame.time.wait(70)                                    #espera 70 milisegundos para pasar al sig frame creando la animacion


def seleccionar_nivel(pantalla):                                #Muestra en pantalla el menu de Nivel (Facil, medio, dificil o volver)
    """
    Permite al jugador seleccionar el nivel de dificultad del juego.

    Argumento:
        pantalla (Surface): Superficie donde se renderiza la selección.

    Retorna:
        No retorna. Modifica la variable global "nivel_actual".
    """
    global nivel_actual                                         #Se modifica la variable que defini en funciones.py
    seleccionando = True                                        #Bandera para mantener el bucle de seleccion 

    while seleccionando:
        pantalla.fill(AZUL_OSCURO)                              #Rellena la pantalla con Azul oscuro
        ancho = pantalla.get_width()                            #Calcula el ancoh y alto de la pantalla 
        alto = pantalla.get_height()

        tam_fuente = max(24, alto // 25)                                #Ajusta el tamañode la fuente segun el alto
        fuente_dinamica = pygame.font.SysFont("arial", tam_fuente)

        texto = fuente_dinamica.render("Elegir nivel de dificultad", True, BLANCO)          #Mustra el titulo centrado segun el tamaño de pantalla
        pantalla.blit(texto, (ancho // 2 - texto.get_width() // 2, alto // 8))

        ancho_boton = ancho // 4
        alto_boton = alto // 12                                     #Se define el tamaño y la posicion de los botones 
        x_boton = (ancho - ancho_boton) // 2                        #Los botones se centran horizontalmente y estan espaciados verticalmente
        espaciado = alto_boton + 20
        y_inicial = alto // 4

        boton_facil = crear_boton(pantalla, "Fácil (10x10)", x_boton, y_inicial + espaciado * 0, ancho_boton, alto_boton)
        boton_medio = crear_boton(pantalla, "Medio (20x20)", x_boton, y_inicial + espaciado * 1, ancho_boton, alto_boton)           #Crea y dibuja 4 botones usando la funcion crear boton
        boton_dificil = crear_boton(pantalla, "Difícil (40x40)", x_boton, y_inicial + espaciado * 2, ancho_boton, alto_boton)
        boton_volver = crear_boton(pantalla, "Volver", x_boton, y_inicial + espaciado * 3, ancho_boton, alto_boton)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()                                  #Si se cierra la ventana, se cierra el juego DUH
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_facil.collidepoint(evento.pos):
                    nivel_actual = "Fácil"
                    seleccionando = False
                elif boton_medio.collidepoint(evento.pos):          #Si se hce click con el mouse, se detecta donde se hizo click
                    nivel_actual = "Medio"                          #Si es en un boton de nivel, actualiza la variable nivel actual y sale del bucle
                    seleccionando = False                           #Si se presiona volver, sale del bucle
                elif boton_dificil.collidepoint(evento.pos):        
                    nivel_actual = "Difícil"
                    seleccionando = False
                elif boton_volver.collidepoint(evento.pos):
                    seleccionando = False

        pygame.display.flip()                                       #Actualiza la pantalla mostrando todos los cambios

def pantalla_juego(pantalla, matriz, nombre, fondo_juego = None, explosion_frames = None):              #Se encarga de mostrar tablero, gestiona clicks, dibuja celdas, dispara nave
    """                                                                                                 #reprodice sonidos, muestra mensajes, controla puntajes y detecta cuando termina la partida
    Lógica principal del juego: renderiza el tablero, gestiona eventos y actualiza puntajes.

    Argumentos:
        pantalla (Surface): Pantalla donde se juega.
        matriz (list): Matriz del juego.
        nombre (str): Nombre del jugador.
        fondo_juego (Surface): Imagen de fondo (opcional).
        explosion_frames (list): Animación de explosión (opcional).

    Retorna:
        No retorna. Maneja el bucle principal del juego.
    """
    ejecutando = True                                                               #Controla el bucle principal del juego 
    TAM_CASILLA = calcular_tam_casilla(pantalla, matriz)                            #Calcula el tamaño de las casillas para el tablero
    puntaje = 0                                                                     #Lleva la cuenta del puntaje del jugador
    mensaje = ""                                                                    
    contador_mensaje = 0                                                            #Se usa para mostrar msj temporales, como "Nave Hundida"

    ancho_tablero = len(matriz[0]) * TAM_CASILLA                                    #Calcula el ancho y alto en pixeles del tablero completo
    alto_tablero = len(matriz) * TAM_CASILLA
    x_inicio = (pantalla.get_width() - ancho_tablero) // 2                          #Centra el tablero en la pantalla 
    y_inicio = (pantalla.get_height() - alto_tablero) // 2

    filas = len(matriz)                                                             #Guarda cuantas filas, columnas tiene la matriz
    columnas = len(matriz[0])
    pygame.mouse.set_visible(False)  # Ocultar cursor al entrar a la pantalla de juego usando la imagen

    imagen_misil = pygame.image.load(os.path.join(RUTA_MEDIA, "misil_cursor.png")).convert_alpha()              #Carga la imagen del misil
    imagen_misil = pygame.transform.scale(imagen_misil, (32, 32))                                                                   #La ajusta al tamaño especificado

    sonido_explosion = pygame.mixer.Sound(os.path.join(RUTA_MEDIA, "explosion_barco.wav"))#Carga el sonido de explosion
    sonido_explosion.set_volume(0.3)  # Ajusta el volumen a un 30%

    
    while ejecutando:                                   #Bucle principal del juego 
        
        if fondo_juego:
            pantalla.blit(fondo_juego, (0, 0))          #Dibuja el fondo del juego, si no hay, pinta uno de azul oscuro
        else:
            pantalla.fill(AZUL_OSCURO)
                
        ancho_boton = pantalla.get_width() // 6
        alto_boton = pantalla.get_height() // 15                    #calcula el tamaño y posicion del boton reiniciar y lo dibuja en pantalla
        x_boton = pantalla.get_width() - ancho_boton - 20
        y_boton = 20
        boton_reiniciar = crear_boton(pantalla, "Reiniciar", x_boton, y_boton, ancho_boton, alto_boton)
        boton_mute = dibujar_boton_mute(pantalla, 20, pantalla.get_height() - 80, 80, 60)



        for evento in pygame.event.get():               #Procesamiento de lo que hace el jugador
            if evento.type == pygame.QUIT:
                pygame.quit()                           #Cierra el juego si se cierra la ventana
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.mouse.set_visible(True)          #Si se presiona ESC, se termina el juego y se guarda el puntaje
                    guardar_puntaje(nombre, puntaje)
                    ejecutando = False

            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = evento.pos                   #Si se hace click con el mouse en la pantalla, captura la posicion
                if boton_mute.collidepoint(evento.pos):
                    toggle_musica()

                
                if boton_reiniciar.collidepoint((mouse_x, mouse_y)):
                    matriz = inicializar_matriz(filas, columnas, 0)             #Si se clickea en el boton reiniciar, se reinicia completamente el juego
                    _, _, naves = get_parametros_por_nivel(nivel_actual)        #Se crea una nueva matriz vacia
                    colocar_naves_en_matriz(matriz, naves)                      #Se colocan nuevas naves
                    puntaje = 0                                                 #El puntaje se vuelve a cero
                    continue

                col = (mouse_x - x_inicio) // TAM_CASILLA
                fila = (mouse_y - y_inicio) // TAM_CASILLA                                  #Convierte coordenadas del clic a indices de matriz

                if 0 <= fila < filas and 0 <= col < columnas:                           #Verifica si el clic esta dentro del tablero
                    valor = matriz[fila][col]                                           #Giarda el valor de la celda disparada

                    if valor == 0:                                                      #Si el valor es 0, significa que era agua 
                        matriz[fila][col] = 200  # Agua disparada                       #Se cambia a 200 para marcarla como disparada
                        puntaje -= 1                                                    #El puntaje baja a menos uno

                    elif 1 <= valor < 100:                                                  #Si el valor es entre 1 a 99, es una parte de nave sin tocar
                        matriz[fila][col] = valor + 100  # Marcamos como disparado          #Se suma 100 para marcar que fue impactada
                        puntaje += 5                                                        #Se suma 5 puntos por parte

                        if nave_hundida(matriz, valor):                                    #Si todas las partes de la nave fueron impactadas                          
                            partes = contar_partes(matriz, valor + 100)                     #Se cuentan cuantas partes tenia 
                            puntaje += partes * 10                                          #Se suma 10 puntos por parte
                            animar_explosion_en_casillas(pantalla, matriz, valor + 100, TAM_CASILLA, x_inicio, y_inicio, explosion_frames, fondo_juego, puntaje, mensaje, contador_mensaje, nombre, imagen_misil, boton_reiniciar, boton_mute)
                            for _ in range(partes):                                 #Reproduce el sonido por cada parte hundida
                                sonido_explosion.play()
                                pygame.time.wait(100)                               #Espera 100 milisegundos por sonido para que se note
                            mensaje = "¡Nave hundida!"                             
                            contador_mensaje = 120                                  #Muestra el mensaje por 2 segundos

        for fila in range(len(matriz)):
            for col in range(len(matriz[0])):                                       #Recorre nuevamente la matriz para redibujarla
                valor = matriz[fila][col]                                           #Calcula coordenadas X, Y para cada celda    
                x = x_inicio + col * TAM_CASILLA
                y = y_inicio + fila * TAM_CASILLA

                if valor == 0:
                    color = AZUL_CLARO  # Agua no disparada
                elif valor == 200:
                    color = (0, 0, 0)  # Agua disparada                                 #Decide el color segun su valor 
                elif 1 <= valor < 100:
                    color = AZUL_CLARO  # Parte de nave aún no descubierta
                elif valor >= 100:
                    color = (255, 0, 0)  # Parte de nave acertada
                else:
                    color = (100, 100, 100)  # Caso raro, gris

                pygame.draw.rect(pantalla, color, (x, y, TAM_CASILLA, TAM_CASILLA))                 #Dibuja el rectangulo de fondo de cada celda 
                pygame.draw.rect(pantalla, BLANCO, (x, y, TAM_CASILLA, TAM_CASILLA), 1)             #Dibuja un borde blanco alrededor

        tam_fuente = max(24, pantalla.get_height() // 30)                               #Define una funente adaptable al tamaño de la pantalla 
        fuente_dinamica = pygame.font.SysFont("arial", tam_fuente)

        naves_restantes = contar_naves_vivas(matriz)                            # Mostrar naves restantes

        if naves_restantes == 0:                                                                                    #Si no hay naves, muestra el mensaje de victoria 
            mensaje = f"¡Has hundido todas las naves, {nombre}! Puntaje final: {puntaje:04}"                        
            texto_final = fuente_dinamica.render(mensaje, True, (255, 255, 255))                            
            pantalla.blit(texto_final, (pantalla.get_width() // 2 - texto_final.get_width() // 2,
                                        pantalla.get_height() // 2))
            guardar_puntaje(nombre, puntaje)                        #Guarda el puntaje 
            pygame.display.flip()
            pygame.time.wait(4000)                                  #Espera 4 sgundo
            ejecutando = False                                      #Finaliza el juego 
            pygame.mouse.set_visible(True)      

            continue

        texto_naves = fuente_dinamica.render(f"Naves restantes: {naves_restantes}", True, (255, 255, 0))        #Muestra las naves restantes 
        pantalla.blit(texto_naves, (20, 20 + tam_fuente + 10))

        texto_info = fuente_dinamica.render("Presione ESC para volver", True, BLANCO)                   #Muestra un texto de ayuda ESC para volver
        pantalla.blit(texto_info, (20, 20 + tam_fuente * 2 + 20))
        
        if contador_mensaje > 0:
            texto_hundida = fuente.render(mensaje, True, (255, 255, 0))                #Si hay un mensaje activo, lo muestra y disminuye el contador
            pantalla.blit(texto_hundida, (10, 90))
            contador_mensaje -= 1
        
        texto_puntaje = fuente_dinamica.render(f"Puntaje: {puntaje:04}", True, (0, 255, 0))                             #Muestra el puntaje furante el juego
        pantalla.blit(texto_puntaje, (20, 20))
        
        pos_mouse = pygame.mouse.get_pos()                                                                  
        pantalla.blit(imagen_misil, (pos_mouse[0] - 16, pos_mouse[1] - 16))                                         #Dibuja la imagen del misil como cursor del mouse centrado

        pygame.display.flip()                               #Muestra todo el contenido en pantalla 


def menu_principal(pantalla, fondo, fondo_juego, explosion_frames):                                         # Muestra el menu inicial del juego
    """
    Muestra el menú principal con botones para iniciar el juego, ver puntajes o salir.

    Argumentos:
        pantalla (Surface): Pantalla principal del juego.
        fondo (Surface): Imagen de fondo para el menú.
        fondo_juego (Surface): Imagen de fondo para el juego.
        explosion_frames (list): Animaciones de explosión.

    Retorna:
        No retorna. Ejecuta el menú.
    """
    ejecutando = True                                               #Bandera para mantener activo el bucle del menu principal
    
    while ejecutando:                                               #Queda en bucle hasta que el jugador elije salir o jugar
        
        pantalla.blit(fondo, (0,0))                                 #Dibuja el fondo del menu completo
        ancho_pantalla = pantalla.get_width()                           
        alto_pantalla = pantalla.get_height()                           
        ancho_boton = ancho_pantalla // 5                                   #calcula el tamaño de los botones segun el tamaño de pantalla 
        alto_boton = alto_pantalla // 12
        x_boton = (ancho_pantalla - ancho_boton) // 2                        #Los botones se centran horizontalmente y espaciados verticalmente        

        espaciado = alto_boton + 20
        y_inicial = alto_pantalla // 3
        
        boton_nivel = crear_boton(pantalla, "Nivel", x_boton, y_inicial + espaciado * 0, ancho_boton, alto_boton)               #Crea y dibuja los 4 botones del menu
        boton_jugar = crear_boton(pantalla, "Jugar", x_boton, y_inicial + espaciado * 1, ancho_boton, alto_boton)
        boton_puntajes = crear_boton(pantalla, "Ver Puntajes", x_boton, y_inicial + espaciado * 2, ancho_boton, alto_boton)
        boton_salir = crear_boton(pantalla, "Salir", x_boton, y_inicial + espaciado * 3, ancho_boton, alto_boton)
        boton_mute = dibujar_boton_mute(pantalla, 20, pantalla.get_height() - 80, 80, 60)


        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:                              #SI se cierra la ventana, se termina el programa 
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                
                if boton_nivel.collidepoint(evento.pos):                #SI se hace click, muestra el selector de dificultad
                    seleccionar_nivel(pantalla)
                
                elif boton_jugar.collidepoint(evento.pos):  
                    nombre = pedir_nombre(pantalla)                                     # Solicita nombre al iniciar
                    filas, columnas, naves = get_parametros_por_nivel(nivel_actual)    
                    matriz = inicializar_matriz(filas, columnas, 0)                     #Prepara el tablero
                    colocar_naves_en_matriz(matriz, naves)
                    pantalla_juego(pantalla, matriz, nombre, fondo_juego, explosion_frames)      #Empieza el juego 
                
                elif boton_puntajes.collidepoint(evento.pos):
                    mostrar_mejores_puntajes(pantalla)                           #Muestra los mejores puntajes guardados 
                
                elif boton_salir.collidepoint(evento.pos):
                    pygame.quit()                                                #Cierra el juego 
                    sys.exit()
                
                if boton_mute.collidepoint(evento.pos):
                    toggle_musica()

            if evento.type == pygame.KEYDOWN:
                                                                                            #Ctrl + R para borrar puntajes guardados del archivo 
                if evento.key == pygame.K_r and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    borrar_puntajes()

        
        texto_nivel = fuente.render(f"Nivel: {nivel_actual}", True, BLANCO)           #Muestra el nivel actual seleccionado     
        pantalla.blit(texto_nivel, (10, 10))                                           
        
        pygame.display.flip()          #Muestra en pantalla 


