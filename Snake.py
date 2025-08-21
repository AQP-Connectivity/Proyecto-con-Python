import tkinter as tk            # Importa la librería estándar para GUI en Python y la alias 'tk'
import random                   # Importa funciones aleatorias (para colocar la comida)

# Configuración inicial
ANCHO = 400                     # Ancho de la ventana/canvas del juego en píxeles
ALTO = 400                      # Alto de la ventana/canvas del juego en píxeles
TAM_CUADRO = 20                 # Tamaño de cada celda/cuadrado de la cuadrícula
VEL = 100                       # Velocidad del juego en ms (cada cuánto se actualiza el movimiento)

class SnakeGame:                # Define una clase para encapsular todo el juego
    def __init__(self, root):   # Constructor; recibe la ventana principal de tkinter
        self.root = root
        self.root.title("🐍 Snake Game")  # Título de la ventana

        self.canvas = tk.Canvas(root, width=ANCHO, height=ALTO, bg="black")  # Área de dibujo
        self.canvas.pack()       # Agrega el canvas a la ventana

        # Dirección inicial
        self.direccion = "Right" # La serpiente comenzará moviéndose hacia la derecha

        # Crear serpiente (3 cuadros)
        self.serpiente = [(100, 100), (80, 100), (60, 100)]  # Lista de posiciones (x,y) de cada segmento (cabeza primero)
        self.cuadros = []        # Aquí guardaremos los IDs de los rectángulos dibujados en el canvas

        for x, y in self.serpiente:                                                   # Recorre cada segmento inicial
            cuadro = self.canvas.create_rectangle(x, y, x + TAM_CUADRO, y + TAM_CUADRO, fill="green")  # Dibuja segmento
            self.cuadros.append(cuadro)                                               # Guarda el ID del rectángulo

        # Comida
        self.comida = None        # ID del rectángulo de comida (inicia vacío)
        self.generar_comida()     # Coloca la primera comida en una posición aleatoria

        # Score
        self.score = 0            # Puntaje inicial
        self.label = tk.Label(root, text=f"Puntos: {self.score}", font=("Arial", 14)) # Etiqueta para mostrar puntos
        self.label.pack()         # Agrega la etiqueta a la ventana

        # Controles (teclas de flechas)
        self.root.bind("<Up>", lambda e: self.cambiar_direccion("Up"))       # Cambia dirección a arriba
        self.root.bind("<Down>", lambda e: self.cambiar_direccion("Down"))   # Cambia dirección a abajo
        self.root.bind("<Left>", lambda e: self.cambiar_direccion("Left"))   # Cambia dirección a izquierda
        self.root.bind("<Right>", lambda e: self.cambiar_direccion("Right")) # Cambia dirección a derecha

        # Iniciar loop
        self.mover()              # Comienza el ciclo de movimiento del juego

    def cambiar_direccion(self, nueva):                 # Maneja el cambio de dirección por el jugador
        # Evitar moverse en dirección contraria inmediata (para no chocarse al instante)
        opuestos = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}  # Direcciones opuestas
        if nueva != opuestos.get(self.direccion):       # Solo permite el cambio si no es la opuesta a la actual
            self.direccion = nueva                      # Actualiza la dirección

    def generar_comida(self):                           # Coloca la comida en una celda aleatoria
        if self.comida:                                 # Si ya existía comida,
            self.canvas.delete(self.comida)             # la borra del canvas
        x = random.randrange(0, ANCHO, TAM_CUADRO)      # Elige x aleatoria alineada a la cuadrícula
        y = random.randrange(0, ALTO, TAM_CUADRO)       # Elige y aleatoria alineada a la cuadrícula
        self.comida = self.canvas.create_rectangle(     # Dibuja la comida como un rect rojo
            x, y, x + TAM_CUADRO, y + TAM_CUADRO, fill="red"
        )
        self.pos_comida = (x, y)                        # Guarda su posición lógica (x,y)

    def mover(self):                                    # Un "tick" del juego: mueve la serpiente una celda
        x, y = self.serpiente[0]                        # Posición actual de la cabeza (primer elemento)
        if self.direccion == "Up":                      # Según la dirección,
            y -= TAM_CUADRO                             # mueve la cabeza una celda hacia arriba
        elif self.direccion == "Down":
            y += TAM_CUADRO
        elif self.direccion == "Left":
            x -= TAM_CUADRO
        elif self.direccion == "Right":
            x += TAM_CUADRO

        nueva_cabeza = (x, y)                           # Calcula la nueva posición de la cabeza

        # Verificar colisiones
        if (x < 0 or x >= ANCHO or y < 0 or y >= ALTO or nueva_cabeza in self.serpiente):
            # Si se sale del canvas o la cabeza cae sobre el cuerpo, fin del juego
            self.game_over()
            return                                      # Detiene este ciclo (no programa el siguiente)

        # Insertar nueva cabeza al inicio de la lista lógica
        self.serpiente.insert(0, nueva_cabeza)
        # Dibuja el nuevo segmento de cabeza y lo guarda
        cuadro = self.canvas.create_rectangle(x, y, x + TAM_CUADRO, y + TAM_CUADRO, fill="green")
        self.cuadros.insert(0, cuadro)

        # Verificar si comió (la cabeza coincide con la comida)
        if nueva_cabeza == self.pos_comida:
            self.score += 1                             # Suma punto
            self.label.config(text=f"Puntos: {self.score}")  # Actualiza la etiqueta
            self.generar_comida()                       # Genera nueva comida
            # Nota: no se borra la cola, así "crece" la serpiente
        else:
            # Si no comió, hay que mover la cola (eliminar el último segmento)
            self.canvas.delete(self.cuadros[-1])        # Borra el rectángulo del último segmento
            self.cuadros.pop()                          # Quita el ID de la lista gráfica
            self.serpiente.pop()                        # Quita la posición de la lista lógica

        self.root.after(VEL, self.mover)                # Programa la próxima actualización en VEL ms (loop del juego)

    def game_over(self):                                 # Muestra mensajes de fin de juego
        self.canvas.create_text(ANCHO/2, ALTO/2, text="GAME OVER", fill="white",
                                font=("Arial", 24, "bold"))  # Texto centrado "GAME OVER"
        self.canvas.create_text(ANCHO/2, ALTO/2+30, text=f"Puntos: {self.score}", fill="yellow",
                                font=("Arial", 16, "bold"))  # Muestra el puntaje final

# Ejecutar
if __name__ == "__main__":           # Este bloque se ejecuta solo si corres este archivo directamente
    root = tk.Tk()                    # Crea la ventana principal de tkinter
    juego = SnakeGame(root)           # Crea una instancia del juego y monta todo
    root.mainloop()                   # Inicia el loop de eventos de tkinter (ventana interactiva)
