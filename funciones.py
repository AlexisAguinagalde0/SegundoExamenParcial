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
    nombre = ""                                                                     #Inicializa la variable nombre como unstring vacio
    escribiendo = True                                                              #Bandera para mantener el bucle activo

    reloj = pygame.time.Clock()                                                     #Controla la velocidad de actulizacion de pantalla
    fuente_input = pygame.font.SysFont("arial", 48)                                 #Crea una fuente para mostrar el titulo y la entrada del jugador

    teclas_validas = {
        pygame.K_a: "A", pygame.K_b: "B", pygame.K_c: "C", pygame.K_d: "D", pygame.K_e: "E",
        pygame.K_f: "F", pygame.K_g: "G", pygame.K_h: "H", pygame.K_i: "I", pygame.K_j: "J",
        pygame.K_k: "K", pygame.K_l: "L", pygame.K_m: "M", pygame.K_n: "N", pygame.K_o: "O",
        pygame.K_p: "P", pygame.K_q: "Q", pygame.K_r: "R", pygame.K_s: "S", pygame.K_t: "T",
        pygame.K_u: "U", pygame.K_v: "V", pygame.K_w: "W", pygame.K_x: "X", pygame.K_y: "Y",        #Diccionario que convierte cada letra de pygame a texto 
        pygame.K_z: "Z", pygame.K_SPACE: " ", pygame.K_MINUS: "-", pygame.K_UNDERSCORE: "_",        #Solo se permiten letras, numeros, espacios y guiones
        pygame.K_0: "0", pygame.K_1: "1", pygame.K_2: "2", pygame.K_3: "3", pygame.K_4: "4",
        pygame.K_5: "5", pygame.K_6: "6", pygame.K_7: "7", pygame.K_8: "8", pygame.K_9: "9"
    }

    while escribiendo:                                                                                      #Se ejecuta mientras no se presione ENTER o se cierre la ventana
        pantalla.fill((10, 40, 100))                                                                        #Rellena la pantalla de un azul oscuro
        texto = fuente_input.render("Ingresá tu nombre y presioná ENTER:", True, (255, 255, 255))           #Crea el texto de instruccion 
        pantalla.blit(texto, (pantalla.get_width() // 2 - texto.get_width() // 2, 150))                     #Lo dibuja centrado horizontalmente, un poco hacia arriba de la pantalla

        entrada = fuente_input.render(nombre, True, (0, 255, 0))                                            #Renderiza el nombre que el jufador lleva escrito 
        pantalla.blit(entrada, (pantalla.get_width() // 2 - entrada.get_width() // 2, 250))                 #lo muestra mas abajo en la pantalla

        for evento in pygame.event.get():                                                       #Lee los eventos que ocurren
            if evento.type == pygame.QUIT:
                pygame.quit()                           #Si se cierra la ventana, se termina el programa
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN and nombre.strip() != "":              #Si el jugador presiona enter y el nombre no esta vacio, se termina el bucle
                    escribiendo = False
                elif evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]                            #Si se presiona borrar, se elimina el ultimo caracter del nombre
                elif evento.key in teclas_validas:
                    nombre += teclas_validas[evento.key]            #Si se presiona una tecla valida, se agrega la letra o numero al nombre

        pygame.display.flip()                                   #Actualiza la pantalla para que se vean los cambios
        reloj.tick(30)

    return nombre.strip()                   #Retorna el nombre escrito por el jugador, eliminando espacios en blanco al principio o final



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
    rect = pygame.Rect(x, y, ancho, alto)                           #Crea un rectangulo con las coordenadas y dimensiones dadas
    pygame.draw.rect(pantalla, color, rect)                         #Dibuja el fondo del boton con el color indicado
    pygame.draw.rect(pantalla, BLANCO, rect, 3)                     #Dibuja el borde blanco con un grosor de 3 pixeles
    texto_render = fuente.render(texto, True, BLANCO)               #Crea una superficie con el texto del boton en color blanco
    texto_rect = texto_render.get_rect(center=rect.center)          #Centra el texto dentro del rectangulo del boton
    pantalla.blit(texto_render, texto_rect)                         #Dibuja el texto sobre el boton
    return rect                                                     #Devuelve el rectangulo del boton para poder detectar clicks



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
    columnas = len(matriz[0])                                   #Obtiene dimensiones del tablero
    contador_naves = 1                                          #Inicializa un contador para asignar un numero unico a cada nave

    for tipo, cantidad in naves_por_tipo.items():           #Itera por cada tipo de nave y su cantidad
        if tipo == "submarinos":
            tamaño = 1
        elif tipo == "destructores":
            tamaño = 2                                      #Define el tamaño de nave segun su tipo
        elif tipo == "cruceros":
            tamaño = 3
        elif tipo == "acorazado":
            tamaño = 4

        for _ in range(cantidad):           #Repite para cada nace del mismo tipo
            colocada = False
            while not colocada:                                             #Intenta colocar la nave hasta que haya espacio, 
                orientacion = random.choice(["horizontal", "vertical"])     #Elige al azar si ira horizontal o vertical
                if orientacion == "horizontal":                         #Si es horizontal:
                    fila = random.randint(0, filas - 1)                 #Elige posiciones aleatorias
                    col = random.randint(0, columnas - tamaño)
                    if all(matriz[fila][col + i] == 0 for i in range(tamaño)):  #Verifica que haya espacio libre
                        for i in range(tamaño):
                            matriz[fila][col + i] = contador_naves              #Coloca la nave asignandole el numero contador_naves
                        colocada = True
                else:
                    fila = random.randint(0, filas - tamaño)
                    col = random.randint(0, columnas - 1)
                    if all(matriz[fila + i][col] == 0 for i in range(tamaño)):      #Aca hace lo mismo pero en direccion vertical
                        for i in range(tamaño):
                            matriz[fila + i][col] = contador_naves
                        colocada = True
            contador_naves += 1                 #Incrementa el numero para la proxima nave


def nave_hundida(matriz, valor_original):
    """
    Verifica si una nave ha sido completamente destruida.

    Argumentos:
        matriz (list): Matriz del juego.
        valor_original (int): Valor que representa a la nave en la matriz.

    Retorna:
        bool: True si la nave fue hundida, False en caso contrario.
    """
    for fila in matriz:                                 #Recorre toda la matriz
        for casilla in fila:
            if casilla == valor_original:               #Si encunetra al menos una parte de la nave sin disparar, retona false
                return False
    return True                         #Si no se encontro partes vivas, retorna True

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
        total += fila.count(valor_disparado)            #Suma cuantas veces aparece el valor de esa nave disparada en toda la matriz
    return total

def contar_naves_vivas(matriz):
    """
    Cuenta la cantidad de naves que aún no fueron completamente hundidas.

    Argumento:
        matriz (list): Matriz del juego.

    Retorna:
        int: Número de naves activas.
    """
    naves_vivas = set()                                             #Agrega cada numero de parte viva a un conjunto
    for fila in matriz:
        for casilla in fila:
            if 1 <= casilla < 100:  # Casilla con nave no tocada
                naves_vivas.add(casilla)                                                        
    return len(naves_vivas)                                        #Devuelve la cantidad de naves distintas vivas 


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
                                                                #Calcula el espacio disponivle 
    ancho_disp = pantalla.get_width() - 2 * margen
    alto_disp = pantalla.get_height() - 2 * margen

    tam_celda_horizontal = ancho_disp // columnas               #Divide por cantidad de filas/columnas
    tam_celda_vertical = alto_disp // filas

    return min(tam_celda_horizontal, tam_celda_vertical)        #Devuelve el tamaño mas pequeño entre ancho o alto, para que todo encaje


def mostrar_mejores_puntajes(pantalla):
    """
    Muestra en pantalla los 3 mejores puntajes guardados, ordenados de mayor a menor.

    Argumento:
        pantalla (Surface): Superficie donde se dibujan los puntajes.

    Retorna:
        No retorna. Muestra los datos en pantalla.
    """

    if os.path.exists("puntajes.json"):
        with open("puntajes.json", "r", encoding="utf-8") as f:
            puntajes = json.load(f)                                     #Si el archivo existe, lo carga. Si no, la lista queda vacia
    else:
        puntajes = []

    ordenar_por_puntaje(puntajes, descendente = True)

    top3 = puntajes[:3]                                 #Toma solo los mejores 3

    ejecutando = True
    fuente_titulo = pygame.font.SysFont("arial", 48)        #Prepara fuente para mostrar el titulo y la lista 
    fuente_lista = pygame.font.SysFont("arial", 36)

    while ejecutando:                           #Bucle hasta que el jugador decida volver 
        pantalla.fill(AZUL_OSCURO)                      #Rellena el fondo de azul

        texto_titulo = fuente_titulo.render("🏆 Mejores Puntajes", True, BLANCO)                            #Renderiza el texto del titulo en blanco 
        pantalla.blit(texto_titulo, (pantalla.get_width() // 2 - texto_titulo.get_width() // 2, 100))       #LO centra horizontalmente y lo posiciona a 100 piceles desde arriba
        
        for i, p in enumerate(top3):                            #Recorre el top 3 
            texto_p = fuente_lista.render(f"{i+1}. {p['nombre']} - {p['puntaje']:04}", True, (255, 255, 0))         #Renderiza cada linea de texto con nombre y puntaje
            pantalla.blit(texto_p, (pantalla.get_width() // 2 - texto_p.get_width() // 2, 200 + i * 50))            #Coloca cada linea separada verticalmente (50 pixeles entre linea)

        boton_volver = crear_boton(pantalla, "Volver", pantalla.get_width() // 2 - 100, 400, 200, 60)               #Crea el boton volver y lo posiciona centrado horizontalmente y 400 pixeles de la parte superior 
        boton_mute = dibujar_boton_mute(pantalla, 20, pantalla.get_height() - 80, 80, 60)
        
        for evento in pygame.event.get():             #Captura todos los eventos que ocurrieron
            if evento.type == pygame.QUIT:
                pygame.quit()                       #Si el jugador cierra la ventana, se cierra el juego 
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_volver.collidepoint(evento.pos):           #Si el jugador hace click en el boton volver, se sale del bucle y termina su funcion
                    ejecutando = False
                if boton_mute.collidepoint(evento.pos):
                    toggle_musica()

        


        pygame.display.flip()                   #Actualiza la ventana con los cambios realizados


def guardar_puntaje(nombre: str, puntaje: int):
    """
    Guarda el nombre y el puntaje del jugador en un archivo JSON.

    Argumentos:
        nombre (str): Nombre del jugador.
        puntaje (int): Puntaje final del jugador.

    Retorna:
        No retorna. Guarda los datos en archivo.
    """
    archivo = "puntajes.json"               #Define el nombre dek archivo donde se van a guardar los puntajes
    lista = []                              #Inicializa una lista vacia donde se guardaran los puntajes
    
    if os.path.exists(archivo):                                     #VErifica si el archivo existe
        with open(archivo, "r", encoding="utf-8") as f:             #Si existe, abre el archivo en modo lectura y lo carga como una lista de diccionarios usando json.load
            lista = json.load(f)

    lista.append({"nombre": nombre, "puntaje": puntaje})            #Agrega el nuevo puntaje como un diccionario a la lista     

    with open(archivo, "w", encoding="utf-8") as f:                 #Abre el archivo en modo escritura y escribe toda la lista de puntajes 
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

def toggle_musica():
    """
    Alterna entre silenciar y activar el volumen de la música de fondo.
    """
    if pygame.mixer.music.get_volume() > 0:
        pygame.mixer.music.set_volume(0)
    else:
        pygame.mixer.music.set_volume(0.2)

def color_por_valor(valor):
    """
    Devuelve el color correspondiente según el valor de la celda en la matriz.
    """
    color = (100, 100, 100)  # Valor por defecto (gris)

    if valor == 0:
        color = AZUL_CLARO
    elif valor == 200:
        color = (0, 0, 0)
    elif 1 <= valor < 100:
        color = AZUL_CLARO
    elif valor >= 100:
        color = (255, 0, 0)

    return color

def dibujar_boton_mute(pantalla, x, y, ancho, alto):
    """
    Dibuja el botón de mute/desmute con el símbolo correcto según el estado del volumen.
    """
    texto_mute = "🔇" if pygame.mixer.music.get_volume() > 0 else "🔊"
    return crear_boton(pantalla, texto_mute, x, y, ancho, alto)
