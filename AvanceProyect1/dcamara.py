import cv2
import numpy as np
import os
from typing import Optional, Tuple, List

def detectar_placa(
    ruta_imagen: str,
    guardar_placa: bool = True,
    mostrar_resultados: bool = True,
    umbral_proporcion_min: float = 2.0,
    umbral_proporcion_max: float = 6.0,
    min_area_ratio: float = 0.005,  # 0.5% del área total de la imagen
    nombre_salida: str = "placa_recortada.jpg"
) -> Optional[np.ndarray]:
    """
    Detecta una placa vehicular en una imagen usando técnicas de procesamiento de imágenes.
    Está optimizado para placas rectangulares con proporciones típicas (ej. Perú: ~3.5–4.2).

    Args:
        ruta_imagen (str): Ruta a la imagen de entrada.
        guardar_placa (bool): Si True, guarda la placa recortada como archivo JPG.
        mostrar_resultados (bool): Si True, muestra la imagen con contorno y placa detectada.
        umbral_proporcion_min/max (float): Rango de proporción ancho/alto aceptable.
        min_area_ratio (float): Fracción mínima del área total de la imagen para considerar contornos grandes.
        nombre_salida (str): Nombre del archivo de salida si se guarda la placa.

    Returns:
        np.ndarray | None: Imagen de la placa recortada (BGR), o None si no se detectó.
    """
    # ───────────────────────────────────────────────────────────────────────────────
    # 1. Carga y validación de la imagen
    # ───────────────────────────────────────────────────────────────────────────────
    imagen = cv2.imread(ruta_imagen)
    if imagen is None:
        print(f"❌ Error: No se pudo cargar la imagen desde '{ruta_imagen}'. Verifica la ruta y formato.")
        return None

    # Redimensionar conservando aspecto (opcional, pero mejora velocidad y estabilidad)
    # NOTA: Usamos 800 de ancho como referencia; altura se ajusta proporcionalmente
    h, w = imagen.shape[:2]
    escala = 800 / w
    nuevo_ancho, nuevo_alto = int(w * escala), int(h * escala)
    imagen = cv2.resize(imagen, (nuevo_ancho, nuevo_alto), interpolation=cv2.INTER_AREA)
    imagen_original = imagen.copy()

    # ───────────────────────────────────────────────────────────────────────────────
    # 2. Preprocesamiento: realzar bordes y estructuras rectangulares
    # ───────────────────────────────────────────────────────────────────────────────
    # Convertir a escala de grises
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Reducir ruido manteniendo bordes (filtro bilateral: preserva bordes mejor que GaussianBlur)
    filtrada = cv2.bilateralFilter(gris, d=9, sigmaColor=75, sigmaSpace=75)

    # Realzar bordes con Sobel en X (placas suelen tener cambios bruscos horizontalmente)
    sobel_x = cv2.Sobel(filtrada, cv2.CV_8U, 1, 0, ksize=3)
    _, umbral_sobel = cv2.threshold(sobel_x, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Alternativa robusta: usar ambos umbral adaptativo + Sobel (combinación más estable)
    # Aquí usamos una combinación: Sobel + umbral binario Otsu
    umbral = umbral_sobel

    # Reforzar estructuras horizontales/verticales con operaciones morfológicas
    kernel_rect = cv2.getStructuringElement(cv2.MORPH_RECT, (17, 3))  # refuerza rectángulos
    umbral = cv2.morphologyEx(umbral, cv2.MORPH_CLOSE, kernel_rect)

    # Detección de bordes con Canny (usamos imagen umbralizada para mejor contraste)
    bordes = cv2.Canny(umbral, 50, 150, apertureSize=3)

    # Cierre para conectar bordes rotos
    kernel_cierre = np.ones((3, 3), np.uint8)
    bordes = cv2.morphologyEx(bordes, cv2.MORPH_CLOSE, kernel_cierre)

    # ───────────────────────────────────────────────────────────────────────────────
    # 3. Detección de contornos y filtrado por geometría
    # ───────────────────────────────────────────────────────────────────────────────
    contornos, _ = cv2.findContours(bordes, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Calcular área mínima (filtro por tamaño relativo)
    area_total = imagen.shape[0] * imagen.shape[1]
    area_min = area_total * min_area_ratio  # ej: 0.5% del área total → evita ruido pequeño

    candidatos = []
    for c in contornos:
        area = cv2.contourArea(c)
        if area < area_min:
            continue

        # Aproximar contorno a polígono con menor número de vértices
        perimetro = cv2.arcLength(c, True)
        aprox = cv2.approxPolyDP(c, 0.015 * perimetro, True)  # tolerancia ajustable (1.5%)

        # Solo considerar contornos con 4 vértices (forma rectangular)
        if len(aprox) == 4:
            x, y, w, h = cv2.boundingRect(aprox)
            proporcion = w / float(h) if h > 0 else 0

            # Validar proporción típica de placa (ajustable por región)
            if umbral_proporcion_min <= proporcion <= umbral_proporcion_max and h > 20:
                candidatos.append((c, aprox, x, y, w, h, area))

    # Ordenar candidatos por área descendente (el más grande plausible es prioridad)
    candidatos.sort(key=lambda x: x[-1], reverse=True)

    placa = None
    placa_contorno = None

    # ───────────────────────────────────────────────────────────────────────────────
    # 4. Validación adicional: buscar región con alto contraste/texto (opcional pero útil)
    # ───────────────────────────────────────────────────────────────────────────────
    # NOTA: Esto se podría expandir con análisis de textura (ej. usar Tesseract en ROI),
    # pero por ahora priorizamos geometría + proporción.
    for c, aprox, x, y, w, h, area in candidatos:
        # Recortar ROI y analizar desviación estándar (placas suelen tener alto contraste interno)
        roi_gris = gris[y:y+h, x:x+w]
        if roi_gris.size == 0:
            continue
        std_dev = np.std(roi_gris)
        # Umbral empírico: placas típicamente tienen std > 30-40 (depende de iluminación)
        if std_dev < 35:
            continue  # descartar regiones demasiado uniformes (falsos positivos)

        # Aceptar candidato válido
        placa = imagen_original[y:y+h, x:x+w]
        placa_contorno = aprox
        cv2.drawContours(imagen, [aprox], -1, (0, 255, 0), 3)
        cv2.putText(imagen, "Placa", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        break  # tomar el primer candidato válido *más grande y con suficiente contraste*

    # ───────────────────────────────────────────────────────────────────────────────
    # 5. Salida y visualización
    # ───────────────────────────────────────────────────────────────────────────────
    if placa is not None:
        if guardar_placa:
            salida_path = os.path.abspath(nombre_salida)
            cv2.imwrite(salida_path, placa)
            print(f"✅ Placa detectada y guardada como '{salida_path}'")
        if mostrar_resultados:
            cv2.imshow("Placa detectada", placa)
    else:
        print("❌ No se detectó ninguna placa válida (verifica iluminación, ángulo o resolución).")

    if mostrar_resultados:
        # Mostrar imagen original con contorno resaltado
        cv2.imshow("Detección de Placa — Resultado", imagen)
        print("ℹ️ Presiona cualquier tecla para cerrar las ventanas.")
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return placa


# ───────────────────────────────────────────────────────────────────────────────
# Ejemplo de uso y pruebas
# ───────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Parámetros ajustables para Perú (placas oficiales: ~30 cm × 15 cm → prop. ~2.0, pero perspectiva puede aumentarla)
    # Ej: placas peruanas vistas de frente ≈ 3.0–4.5; de costado pueden superar 5.0
    placa = detectar_placa(
        ruta_imagen="auto.png",
        guardar_placa=True,
        mostrar_resultados=True,
        umbral_proporcion_min=2.0,
        umbral_proporcion_max=6.0,
        min_area_ratio=0.004,  # ~0.4% del área total
        nombre_salida="placa_peru.jpg"
    )

    if placa is not None:
        print("💡 Sugerencia: ahora puedes aplicar OCR con `pytesseract.image_to_string(placa)`.")
