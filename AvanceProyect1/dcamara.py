import cv2
import numpy as np

def detectar_placa(ruta_imagen, guardar_placa=True, mostrar_resultados=True):
    # Cargar la imagen
    imagen = cv2.imread(ruta_imagen)
    if imagen is None:
        print("❌ Error: No se pudo cargar la imagen. Verifica la ruta.")
        return None

    # Redimensionar para procesamiento más rápido (opcional)
    imagen = cv2.resize(imagen, (800, 600))
    imagen_original = imagen.copy()

    # Convertir a escala de grises
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Aplicar filtro bilateral para reducir ruido manteniendo bordes
    filtrada = cv2.bilateralFilter(gris, 11, 17, 17)

    # Aplicar umbral adaptativo para mejorar contraste local
    umbral = cv2.adaptiveThreshold(filtrada, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # Aplicar Canny sobre la imagen umbralizada para destacar bordes
    bordes = cv2.Canny(umbral, 30, 200)

    # Operaciones morfológicas para cerrar huecos y reforzar contornos
    kernel = np.ones((3,3), np.uint8)
    bordes = cv2.morphologyEx(bordes, cv2.MORPH_CLOSE, kernel)

    # Buscar contornos
    contornos, _ = cv2.findContours(bordes.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Ordenar por área descendente
    contornos = sorted(contornos, key=cv2.contourArea, reverse=True)[:15]

    placa = None
    placa_contorno = None

    for c in contornos:
        perimetro = cv2.arcLength(c, True)
        aprox = cv2.approxPolyDP(c, 0.018 * perimetro, True)

        # Verificar que tenga 4 vértices (forma rectangular)
        if len(aprox) == 4:
            x, y, w, h = cv2.boundingRect(aprox)
            # Verificar proporción de aspecto típica de una placa (ancho/alto)
            proporcion = w / float(h)
            if 2.0 <= proporcion <= 6.0:  # Ajusta según el país (ej. Perú ≈ 3-4)
                placa = imagen_original[y:y+h, x:x+w]
                placa_contorno = aprox
                cv2.drawContours(imagen, [aprox], -1, (0, 255, 0), 3)
                break  # Tomar la primera coincidencia plausible

    # Mostrar resultados
    if placa is not None:
        if guardar_placa:
            cv2.imwrite("placa_recortada.jpg", placa)
            print("✅ Placa detectada y guardada como 'placa_recortada.jpg'")
        if mostrar_resultados:
            cv2.imshow("Placa detectada", placa)
    else:
        print("❌ No se detectó ninguna placa con forma y proporción válidas.")

    if mostrar_resultados:
        cv2.imshow("Resultado", imagen)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return placa

# Uso
if __name__ == "__main__":
    detectar_placa("auto.png")
