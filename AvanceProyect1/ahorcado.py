import random

# Lista de palabras
palabras = ["python", "programacion", "ahorcado", "tecnologia", "juego", "computadora"]

def elegir_palabra():
    return random.choice(palabras)

def jugar():
    print("🎯 Bienvenido al Juego del Ahorcado 🎯\n")
    palabra = elegir_palabra()
    letras_adivinadas = []
    intentos = 6
    acertado = False

    while intentos > 0 and not acertado:
        # Mostrar estado actual
        palabra_mostrada = "".join([letra if letra in letras_adivinadas else "_" for letra in palabra])
        print("\nPalabra:", palabra_mostrada)
        print("Intentos restantes:", intentos)
        print("Letras usadas:", " ".join(letras_adivinadas))

        # Pedir letra
        letra = input("👉 Ingresa una letra: ").lower()

        if letra in letras_adivinadas:
            print("⚠️ Ya usaste esa letra, intenta otra.")
            continue

        letras_adivinadas.append(letra)

        if letra in palabra:
            print("✅ ¡Bien hecho! La letra está en la palabra.")
        else:
            print("❌ Incorrecto. Pierdes un intento.")
            intentos -= 1

        if all(l in letras_adivinadas for l in palabra):
            acertado = True

    # Fin del juego
    if acertado:
        print(f"\n🎉 ¡Ganaste! La palabra era '{palabra}'.")
    else:
        print(f"\n💀 Te quedaste sin intentos. La palabra era '{palabra}'.")

if __name__ == "__main__":
    jugar()
