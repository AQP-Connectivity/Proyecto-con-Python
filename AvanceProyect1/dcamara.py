import cv2

# Cargar la imagen
imagen = cv2.imread("auto.png")

# Redimensionar si es muy grande (opcional)
imagen = cv2.resize(imagen, (800, 600))

# Convertir a escala de grises
gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

# Aplicar filtro para reducir ruido
filtro = cv2.bilateralFilter(gris, 11, 17, 17)

# Detectar bordes
bordes = cv2.Canny(filtro, 30, 200)

# Buscar contornos
contornos, _ = cv2.findContours(bordes.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Ordenar contornos por área (de mayor a menor)
contornos = sorted(contornos, key=cv2.contourArea, reverse=True)[:10]

placa = None

for c in contornos:
    # Aproximar el contorno
    perimetro = cv2.arcLength(c, True)
    aprox = cv2.approxPolyDP(c, 0.018 * perimetro, True)

    # Si el contorno tiene 4 lados, probablemente es una placa
    if len(aprox) == 4:
        x, y, w, h = cv2.boundingRect(aprox)
        placa = imagen[y:y+h, x:x+w]
        cv2.drawContours(imagen, [aprox], -1, (0, 255, 0), 3)
        break

# Mostrar resultados
if placa is not None:
    cv2.imshow("Placa detectada", placa)
    cv2.imwrite("placa_recortada.jpg", placa)
    print("✅ Placa detectada y guardada como placa_recortada.jpg")
else:
    print("❌ No se pudo detectar la placa.")

cv2.imshow("Resultado", imagen)
cv2.waitKey(0)
cv2.destroyAllWindows()

