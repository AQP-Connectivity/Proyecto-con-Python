import cv2
import pytesseract
import os

# Configuración de Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def detectar_placa(filepath, upload_folder):
    imagen = cv2.imread(filepath)
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    filtro = cv2.bilateralFilter(gris, 11, 17, 17)
    bordes = cv2.Canny(filtro, 30, 200)

    contornos, _ = cv2.findContours(bordes.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contornos = sorted(contornos, key=cv2.contourArea, reverse=True)[:10]

    placa = None
    for c in contornos:
        perimetro = cv2.arcLength(c, True)
        aprox = cv2.approxPolyDP(c, 0.018 * perimetro, True)
        if len(aprox) == 4:
            x, y, w, h = cv2.boundingRect(aprox)
            placa = imagen[y:y+h, x:x+w]
            cv2.imwrite(os.path.join(upload_folder, "placa_recortada.jpg"), placa)
            break

    if placa is not None:
        return pytesseract.image_to_string(placa, config="--psm 8").strip()

    return None



