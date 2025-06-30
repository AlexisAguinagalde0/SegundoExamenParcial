import pygame
import sys
import random
import json
import os

BLANCO = (255, 255, 255)
AZUL_OSCURO = (10, 40, 100)                                                      #Se define los colores para llamarlos en las diferentes funciones
AZUL_CLARO = (50, 100, 200)

nivel_actual = "Fácil"                                                  #Inicia el nivel actual por defecto en facil

fuente = None                                                   #Se utiliza como fuente global 

def inicializar_matriz(cantidad_filas:int, cantidad_columnas:int, valor_inicial:any) -> list:
    """
    Crea una matriz con un valor inicial definido en todas sus posiciones.

    Argumentos:
        cantidad_filas (int): Número de filas de la matriz.
        cantidad_columnas (int): Número de columnas de la matriz.
        valor_inicial (any): Valor con el que se inicializa cada celda de la matriz.

    Retorna:
        Matriz de tamaño cantidad_filas x cantidad_columnas con todos los elementos inicializados.    
    """
    matriz = []                                                 #Crea una lista vacia
    for i in range(cantidad_filas):                             #Itera la cantidad de filas que corresponde
        fila = [valor_inicial] * cantidad_columnas              # Crea la lista vacia con la cantidad de columnas y el valor inicial
        matriz += [fila]                                        # Agrega la fila a la matriz    
    return matriz                                               #Retorna la matriz completa con los datos pasados


def init_fuente():
    """
    Inicializa la fuente global utilizada para mostrar texto en pantalla.              

    No recibe argumentos ni retorna valores.
    """
    global fuente                                              
    fuente = pygame.font.SysFont("arial", 36)           #Inicia la variable global fuente para usar el texto 



def pedir_nombre(pantalla):
    """
    Permite al usuario ingresar su nombre mediante el teclado y lo muestra en pantalla.

    Argumento:
        pantalla (Surface): Superficie donde se renderiza la entrada del nombre.

    Retorna:
        str: Nombre ingresado por el jugador.
    """
    nombre = ""
    escribiendo = True

    reloj = pygame.time.Clock()
    fuente_input = pygame.font.SysFont("arial", 48)

    teclas_validas = {
        pygame.K_a: "A", pygame.K_b: "B", pygame.K_c: "C", pygame.K_d: "D", pygame.K_e: "E",
        pygame.K_f: "F", pygame.K_g: "G", pygame.K_h: "H", pygame.K_i: "I", pygame.K_j: "J",
        pygame.K_k: "K", pygame.K_l: "L", pygame.K_m: "M", pygame.K_n: "N", pygame.K_o: "O",
        pygame.K_p: "P", pygame.K_q: "Q", pygame.K_r: "R", pygame.K_s: "S", pygame.K_t: "T",
        pygame.K_u: "U", pygame.K_v: "V", pygame.K_w: "W", pygame.K_x: "X", pygame.K_y: "Y",
        pygame.K_z: "Z", pygame.K_SPACE: " ", pygame.K_MINUS: "-", pygame.K_UNDERSCORE: "_",
        pygame.K_0: "0", pygame.K_1: "1", pygame.K_2: "2", pygame.K_3: "3", pygame.K_4: "4",
        pygame.K_5: "5", pygame.K_6: "6", pygame.K_7: "7", pygame.K_8: "8", pygame.K_9: "9"
    }

    while escribiendo:
        pantalla.fill((10, 40, 100))
        texto = fuente_input.render("Ingresá tu nombre y presioná ENTER:", True, (255, 255, 255))
        pantalla.blit(texto, (pantalla.get_width() // 2 - texto.get_width() // 2, 150))

        entrada = fuente_input.render(nombre, True, (0, 255, 0))
        pantalla.blit(entrada, (pantalla.get_width() // 2 - entrada.get_width() // 2, 250))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nombre.strip() != "":
                    escribiendo = False
                elif evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                elif evento.key in teclas_validas:
                    nombre += teclas_validas[evento.key]

        pygame.display.flip()
        reloj.tick(30)

    return nombre.strip()



def crear_boton(pantalla, texto, x, y, ancho, alto, color=AZUL_CLARO):
    """
    Dibuja un botón interactivo en la pantalla con el texto proporcionado.

    Argumentos:
        pantalla (Surface): Superficie donde se dibuja el botón.
        texto (str): Texto a mostrar en el botón.
        x (int): Coordenada X del botón.
        y (int): Coordenada Y del botón.
        ancho (int): Ancho del botón.
        alto (int): Alto del botón.
        color (tuple): Color de fondo del botón.

    Retorna:
        Rect: Rectángulo que representa el botón, útil para detectar clics.
    """
    rect = pygame.Rect(x, y, ancho, alto)
    pygame.draw.rect(pantalla, color, rect)
    pygame.draw.rect(pantalla, BLANCO, rect, 3)
    texto_render = fuente.render(texto, True, BLANCO)
    texto_rect = texto_render.get_rect(center=rect.center)
    pantalla.blit(texto_render, texto_rect)
    return rect



def get_parametros_por_nivel(nivel):
    """
    Devuelve las dimensiones del tablero y la cantidad de naves según el nivel seleccionado.

    Argumento:
        nivel (str): Nivel de dificultad ("Fácil", "Medio" o "Difícil").

    Retorna:
        tuple: (filas, columnas, diccionario de naves por tipo).
    """
    if nivel == "Fácil":
        return 10, 10, {
            "submarinos": 4,
            "destructores": 3,
            "cruceros": 2,
            "acorazado": 1
        }
    elif nivel == "Medio":
        return 20, 20, {
            "submarinos": 8,
            "destructores": 6,
            "cruceros": 4,
            "acorazado": 2
        }
    elif nivel == "Difícil":
        return 40, 40, {
            "submarinos": 12,
            "destructores": 9,
            "cruceros": 6,
            "acorazado": 3
        }

def colocar_naves_en_matriz(matriz, naves_por_tipo):
    """
    Coloca naves en la matriz aleatoriamente según los tipos y cantidades indicadas.

    Argumentos:
        matriz (list): Matriz donde se colocan las naves.
        naves_por_tipo (dict): Diccionario con la cantidad de cada tipo de nave.

    Retorna:
        No retorna nada. Modifica la matriz directamente.
    """
    filas = len(matriz)
    columnas = len(matriz[0])
    contador_naves = 1  # Cada nave (aunque sea del mismo tipo) tiene valor único

    for tipo, cantidad in naves_por_tipo.items():
        if tipo == "submarinos":
            tamaño = 1
        elif tipo == "destructores":
            tamaño = 2
        elif tipo == "cruceros":
            tamaño = 3
        elif tipo == "acorazado":
            tamaño = 4

        for _ in range(cantidad):
            colocada = False
            while not colocada:
                orientacion = random.choice(["horizontal", "vertical"])
                if orientacion == "horizontal":
                    fila = random.randint(0, filas - 1)
                    col = random.randint(0, columnas - tamaño)
                    if all(matriz[fila][col + i] == 0 for i in range(tamaño)):
                        for i in range(tamaño):
                            matriz[fila][col + i] = contador_naves
                        colocada = True
                else:
                    fila = random.randint(0, filas - tamaño)
                    col = random.randint(0, columnas - 1)
                    if all(matriz[fila + i][col] == 0 for i in range(tamaño)):
                        for i in range(tamaño):
                            matriz[fila + i][col] = contador_naves
                        colocada = True
            contador_naves += 1


def nave_hundida(matriz, valor_original):
    """
    Verifica si una nave ha sido completamente destruida.

    Argumentos:
        matriz (list): Matriz del juego.
        valor_original (int): Valor que representa a la nave en la matriz.

    Retorna:
        bool: True si la nave fue hundida, False en caso contrario.
    """
    for fila in matriz:
        for casilla in fila:
            if casilla == valor_original:
                return False
    return True

def contar_partes(matriz, valor_disparado):
    """
    Cuenta cuántas partes de una nave disparada hay en la matriz.

    Argumentos:
        matriz (list): Matriz del juego.
        valor_disparado (int): Valor que representa a una parte de nave impactada.

    Retorna:
        int: Cantidad de partes encontradas con ese valor.
    """
    total = 0
    for fila in matriz:
        total += fila.count(valor_disparado)
    return total

def contar_naves_vivas(matriz):
    """
    Cuenta la cantidad de naves que aún no fueron completamente hundidas.

    Argumento:
        matriz (list): Matriz del juego.

    Retorna:
        int: Número de naves activas.
    """
    naves_vivas = set()
    for fila in matriz:
        for casilla in fila:
            if 1 <= casilla < 100:  # Casilla con nave no tocada
                naves_vivas.add(casilla)
    return len(naves_vivas)


def calcular_tam_casilla(pantalla, matriz, margen=40):
    """
    Calcula el tamaño óptimo de cada casilla para que el tablero se ajuste a la pantalla.

    Argumentos:
        pantalla (Surface): Superficie de juego.
        matriz (list): Matriz de juego.
        margen (int): Margen alrededor del tablero.

    Retorna:
        int: Tamaño en píxeles de cada casilla.
    """
    filas = len(matriz)
    columnas = len(matriz[0])

    ancho_disp = pantalla.get_width() - 2 * margen
    alto_disp = pantalla.get_height() - 2 * margen

    tam_celda_horizontal = ancho_disp // columnas
    tam_celda_vertical = alto_disp // filas

    return min(tam_celda_horizontal, tam_celda_vertical)

def cargar_animacion_explosion():
    """
    Carga los frames de animación de explosión.

    Retorna:
        list: Lista de imágenes (Surface) que representan la animación.
    """
    frames = []
    for i in range(6):  # ajustá el rango según la cantidad de frames
        img = pygame.image.load(f"explosiones/explosion_{i}.jpg").convert_alpha()
        img = pygame.transform.scale(img, (40, 40))  # Ajustar tamaño al casillero
        frames.append(img)
    return frames

def animar_explosion_en_casillas(pantalla, matriz, valor_hundido, tam_casilla, x_inicio, y_inicio, frames):
    """
    Reproduce una animación de explosión en todas las casillas correspondientes a una nave hundida.

    Argumentos:
        pantalla (Surface): Superficie donde se dibuja.
        matriz (list): Matriz del juego.
        valor_hundido (int): Valor que representa la nave hundida.
        tam_casilla (int): Tamaño de cada casilla.
        x_inicio (int): Coordenada X inicial del tablero.
        y_inicio (int): Coordenada Y inicial del tablero.
        frames (list): Lista de imágenes para la animación.

    Retorna:
        No retorna. Dibuja directamente sobre la pantalla.
    """
    posiciones = []
    for fila in range(len(matriz)):
        for col in range(len(matriz[0])):
            if matriz[fila][col] == valor_hundido:
                x = x_inicio + col * tam_casilla
                y = y_inicio + fila * tam_casilla
                posiciones.append((x, y))

    for frame in frames:
        for x, y in posiciones:
            pantalla.blit(frame, (x, y))
        pygame.display.flip()
        pygame.time.wait(60)


def mostrar_mejores_puntajes(pantalla):
    """
    Muestra en pantalla los 3 mejores puntajes guardados, ordenados de mayor a menor.

    Argumento:
        pantalla (Surface): Superficie donde se dibujan los puntajes.

    Retorna:
        No retorna. Muestra los datos en pantalla.
    """

    # Leer el archivo de puntajes
    if os.path.exists("puntajes.json"):
        with open("puntajes.json", "r", encoding="utf-8") as f:
            puntajes = json.load(f)
    else:
        puntajes = []

    # Ordenar manualmente de mayor a menor
    for i in range(len(puntajes) - 1):
        for j in range(i + 1, len(puntajes)):
            if puntajes[i]["puntaje"] < puntajes[j]["puntaje"]:
                puntajes[i], puntajes[j] = puntajes[j], puntajes[i]

    # Tomar solo los 3 mejores
    top3 = puntajes[:3]

    ejecutando = True
    fuente_titulo = pygame.font.SysFont("arial", 48)
    fuente_lista = pygame.font.SysFont("arial", 36)

    while ejecutando:
        pantalla.fill(AZUL_OSCURO)

        # Título
        texto_titulo = fuente_titulo.render("🏆 Mejores Puntajes", True, BLANCO)
        pantalla.blit(texto_titulo, (pantalla.get_width() // 2 - texto_titulo.get_width() // 2, 100))

        # Lista de puntajes
        for i, p in enumerate(top3):
            texto_p = fuente_lista.render(f"{i+1}. {p['nombre']} - {p['puntaje']:04}", True, (255, 255, 0))
            pantalla.blit(texto_p, (pantalla.get_width() // 2 - texto_p.get_width() // 2, 200 + i * 50))

        # Botón Volver
        boton_volver = crear_boton(pantalla, "Volver", pantalla.get_width() // 2 - 100, 400, 200, 60)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_volver.collidepoint(evento.pos):
                    ejecutando = False
                if boton_mute.collidepoint(evento.pos):
                    if pygame.mixer.music.get_volume() > 0:
                        pygame.mixer.music.set_volume(0)
                    else:
                        pygame.mixer.music.set_volume(0.2)


        boton_mute = crear_boton(pantalla, "🔇" if pygame.mixer.music.get_volume() > 0 else "🔊", 20, pantalla.get_height() - 80, 80, 60)

        pygame.display.flip()


def guardar_puntaje(nombre: str, puntaje: int):
    """
    Guarda el nombre y el puntaje del jugador en un archivo JSON.

    Argumentos:
        nombre (str): Nombre del jugador.
        puntaje (int): Puntaje final del jugador.

    Retorna:
        No retorna. Guarda los datos en archivo.
    """
    archivo = "puntajes.json"
    lista = []

    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            lista = json.load(f)

    lista.append({"nombre": nombre, "puntaje": puntaje})

    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=4)

def ordenar_por_puntaje(lista_puntajes: list, descendente=True):
    """
    Ordena una lista de puntajes de mayor a menor por defecto.

    Argumentos:
        lista_puntajes (list): Lista de diccionarios con claves "nombre" y "puntaje".
        descendente (bool): True para ordenar de mayor a menor, False para orden ascendente.

    Retorna:
        No retorna. Ordena la lista en el lugar.
    """
    for i in range(len(lista_puntajes) - 1):
        for j in range(i + 1, len(lista_puntajes)):
            p_i = lista_puntajes[i]["puntaje"]
            p_j = lista_puntajes[j]["puntaje"]
            if (p_i < p_j and descendente) or (p_i > p_j and not descendente):
                lista_puntajes[i], lista_puntajes[j] = lista_puntajes[j], lista_puntajes[i]

def borrar_puntajes():
    """
    Elimina el archivo de puntajes si existe.

    Retorna:
        No retorna. Borra archivo si está presente.
    """
    if os.path.exists("puntajes.json"):
        os.remove("puntajes.json")
        print("✅ Puntajes eliminados correctamente.")
    else:
        print("⚠️ No hay puntajes guardados.")
