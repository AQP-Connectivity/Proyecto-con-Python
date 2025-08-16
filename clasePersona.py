class Persona:
    # Constructor de la clase (se llama __init__)
    def __init__(self, nombre, edad):
        self.nombre = nombre  # Atributo de la instancia
        self.edad = edad      # Atributo de la instancia

    # Método de la clase
    def saludar(self):
        print(f"¡Hola! Me llamo {self.nombre} y tengo {self.edad} años.")

# Crear una instancia (objeto) de la clase
persona1 = Persona("Juan", 30)

# Acceder a los atributos y métodos de la clase
print(persona1.nombre)  # Imprime: Juan
print(persona1.edad)    # Imprime: 30
persona1.saludar()      # Imprime: ¡Hola! Me llamo Juan y tengo 30 años.
