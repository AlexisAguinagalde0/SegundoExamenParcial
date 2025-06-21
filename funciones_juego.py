import pygame
import sys
import random

BLANCO = (255, 255, 255)
AZUL_OSCURO = (10, 40, 100)
AZUL_CLARO = (50, 100, 200)

nivel_actual = "Fácil"

fuente = None

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
    matriz = []
    for i in range(cantidad_filas):
        fila = [valor_inicial] * cantidad_columnas
        
        matriz += [fila]
    return matriz

def crear_matriz_facil():
    filas = 10
    columnas = 10
    matriz = inicializar_matriz(filas, columnas, 0)

    naves = {
        "submarinos": 4,    # 1 casillero
        "destructores": 3,  # 2 casilleros
        "cruceros": 2,      # 3 casilleros
        "acorazado": 1      # 4 casilleros
    }

    colocar_naves_en_matriz(matriz, naves)
    return matriz


def init_fuente():
    global fuente
    fuente = pygame.font.SysFont("arial", 36)



def crear_boton(pantalla, texto, x, y, ancho, alto, color=AZUL_CLARO):
    rect = pygame.Rect(x, y, ancho, alto)
    pygame.draw.rect(pantalla, color, rect)
    pygame.draw.rect(pantalla, BLANCO, rect, 3)
    texto_render = fuente.render(texto, True, BLANCO)
    texto_rect = texto_render.get_rect(center=rect.center)
    pantalla.blit(texto_render, texto_rect)
    return rect

def seleccionar_nivel(pantalla):
    global nivel_actual
    seleccionando = True

    while seleccionando:
        pantalla.fill(AZUL_OSCURO)
        ancho = pantalla.get_width()
        alto = pantalla.get_height()

        tam_fuente = max(24, alto // 25)
        fuente_dinamica = pygame.font.SysFont("arial", tam_fuente)

        texto = fuente_dinamica.render("Elegir nivel de dificultad", True, BLANCO)
        pantalla.blit(texto, (ancho // 2 - texto.get_width() // 2, alto // 8))

        ancho_boton = ancho // 4
        alto_boton = alto // 12
        x_boton = (ancho - ancho_boton) // 2
        espaciado = alto_boton + 20
        y_inicial = alto // 4

        boton_facil = crear_boton(pantalla, "Fácil (10x10)", x_boton, y_inicial + espaciado * 0, ancho_boton, alto_boton)
        boton_medio = crear_boton(pantalla, "Medio (20x20)", x_boton, y_inicial + espaciado * 1, ancho_boton, alto_boton)
        boton_dificil = crear_boton(pantalla, "Difícil (40x40)", x_boton, y_inicial + espaciado * 2, ancho_boton, alto_boton)
        boton_volver = crear_boton(pantalla, "Volver", x_boton, y_inicial + espaciado * 3, ancho_boton, alto_boton)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_facil.collidepoint(evento.pos):
                    nivel_actual = "Fácil"
                    seleccionando = False
                elif boton_medio.collidepoint(evento.pos):
                    nivel_actual = "Medio"
                    seleccionando = False
                elif boton_dificil.collidepoint(evento.pos):
                    nivel_actual = "Difícil"
                    seleccionando = False
                elif boton_volver.collidepoint(evento.pos):
                    seleccionando = False

        pygame.display.flip()

def get_parametros_por_nivel(nivel):
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
    for fila in matriz:
        for casilla in fila:
            if casilla == valor_original:
                return False
    return True

def contar_partes(matriz, valor_disparado):
    total = 0
    for fila in matriz:
        total += fila.count(valor_disparado)
    return total

def contar_naves_vivas(matriz):
    naves_vivas = set()
    for fila in matriz:
        for casilla in fila:
            if 1 <= casilla < 100:  # Casilla con nave no tocada
                naves_vivas.add(casilla)
    return len(naves_vivas)


def calcular_tam_casilla(pantalla, matriz, margen=40):
    filas = len(matriz)
    columnas = len(matriz[0])

    ancho_disp = pantalla.get_width() - 2 * margen
    alto_disp = pantalla.get_height() - 2 * margen

    tam_celda_horizontal = ancho_disp // columnas
    tam_celda_vertical = alto_disp // filas

    return min(tam_celda_horizontal, tam_celda_vertical)


def pantalla_juego(pantalla, matriz):
    ejecutando = True
    TAM_CASILLA = calcular_tam_casilla(pantalla, matriz)
    puntaje = 0
    mensaje = ""
    contador_mensaje = 0

    ancho_tablero = len(matriz[0]) * TAM_CASILLA
    alto_tablero = len(matriz) * TAM_CASILLA
    x_inicio = (pantalla.get_width() - ancho_tablero) // 2
    y_inicio = (pantalla.get_height() - alto_tablero) // 2

    filas = len(matriz)
    columnas = len(matriz[0])

    while ejecutando:
        pantalla.fill(AZUL_OSCURO)
        
        ancho_boton = pantalla.get_width() // 6
        alto_boton = pantalla.get_height() // 15
        x_boton = pantalla.get_width() - ancho_boton - 20
        y_boton = 20
        boton_reiniciar = crear_boton(pantalla, "Reiniciar", x_boton, y_boton, ancho_boton, alto_boton)


        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False

            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = evento.pos

                if boton_reiniciar.collidepoint((mouse_x, mouse_y)):
                    matriz = inicializar_matriz(filas, columnas, 0)
                    _, _, naves = get_parametros_por_nivel(nivel_actual)
                    colocar_naves_en_matriz(matriz, naves)
                    puntaje = 0
                    continue

                col = (mouse_x - x_inicio) // TAM_CASILLA
                fila = (mouse_y - y_inicio) // TAM_CASILLA

                if 0 <= fila < filas and 0 <= col < columnas:
                    valor = matriz[fila][col]

                    if valor == 0:
                        matriz[fila][col] = 200  # Agua disparada
                        puntaje -= 1

                    elif 1 <= valor < 100:
                        matriz[fila][col] = valor + 100  # Marcamos como disparado
                        puntaje += 5

                        if nave_hundida(matriz, valor):
                            partes = contar_partes(matriz, valor + 100)
                            puntaje += partes * 10
                            mensaje = "¡Nave hundida!"
                            contador_mensaje = 120

        for fila in range(len(matriz)):
            for col in range(len(matriz[0])):
                valor = matriz[fila][col]
                x = x_inicio + col * TAM_CASILLA
                y = y_inicio + fila * TAM_CASILLA

                if valor == 0:
                    color = AZUL_CLARO  # Agua no disparada
                elif valor == 200:
                    color = (0, 0, 0)  # Agua disparada
                elif 1 <= valor < 100:
                    color = AZUL_CLARO  # Parte de nave aún no descubierta
                elif valor >= 100:
                    color = (255, 0, 0)  # Parte de nave acertada
                else:
                    color = (100, 100, 100)  # Caso raro, gris

                pygame.draw.rect(pantalla, color, (x, y, TAM_CASILLA, TAM_CASILLA))
                pygame.draw.rect(pantalla, BLANCO, (x, y, TAM_CASILLA, TAM_CASILLA), 1)

        tam_fuente = max(24, pantalla.get_height() // 30)
        fuente_dinamica = pygame.font.SysFont("arial", tam_fuente)

                # Mostrar naves restantes
        naves_restantes = contar_naves_vivas(matriz)

        texto_naves = fuente_dinamica.render(f"Naves restantes: {naves_restantes}", True, (255, 255, 0))
        pantalla.blit(texto_naves, (20, 20 + tam_fuente + 10))

        texto_info = fuente_dinamica.render("Presione ESC para volver", True, BLANCO)
        pantalla.blit(texto_info, (20, 20 + tam_fuente * 2 + 20))

        # Mostrar mensaje temporal si existe
        if contador_mensaje > 0:
            texto_hundida = fuente.render(mensaje, True, (255, 255, 0))
            pantalla.blit(texto_hundida, (10, 90))
            contador_mensaje -= 1
                
        pygame.display.flip()


def menu_principal(pantalla):
    ejecutando = True
    while ejecutando:
        pantalla.fill(AZUL_OSCURO)

        ancho_pantalla = pantalla.get_width()
        alto_pantalla = pantalla.get_height()
        ancho_boton = ancho_pantalla // 5
        alto_boton = alto_pantalla // 12
        x_boton = (ancho_pantalla - ancho_boton) // 2

        espaciado = alto_boton + 20
        y_inicial = alto_pantalla // 3

        boton_nivel = crear_boton(pantalla, "Nivel", x_boton, y_inicial + espaciado * 0, ancho_boton, alto_boton)
        boton_jugar = crear_boton(pantalla, "Jugar", x_boton, y_inicial + espaciado * 1, ancho_boton, alto_boton)
        boton_puntajes = crear_boton(pantalla, "Ver Puntajes", x_boton, y_inicial + espaciado * 2, ancho_boton, alto_boton)
        boton_salir = crear_boton(pantalla, "Salir", x_boton, y_inicial + espaciado * 3, ancho_boton, alto_boton)


        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_nivel.collidepoint(evento.pos):
                    seleccionar_nivel(pantalla)
                elif boton_jugar.collidepoint(evento.pos):
                    filas, columnas, naves = get_parametros_por_nivel(nivel_actual)
                    matriz = inicializar_matriz(filas, columnas, 0)
                    colocar_naves_en_matriz(matriz, naves)
                    pantalla_juego(pantalla, matriz)
                elif boton_puntajes.collidepoint(evento.pos):
                    print("→ Ver puntajes (a implementar)")
                elif boton_salir.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()
        
        texto_nivel = fuente.render(f"Nivel: {nivel_actual}", True, BLANCO)
        pantalla.blit(texto_nivel, (10, 10))
        pygame.display.flip()


