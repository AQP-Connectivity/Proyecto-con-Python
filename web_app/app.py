import os
import cv2
import re
import pytesseract
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

# Ruta al ejecutable de Tesseract en tu PC
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\LAB-USR-AREQUIPA\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)

# Carpeta para guardar las imágenes subidas
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Crear la carpeta si no existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/reconocer_placa', methods=['POST'])
def reconocer_placa():
    if 'imagen' not in request.files:
        return "No se encontró ninguna imagen en la solicitud."

    file = request.files['imagen']
    if file.filename == '':
        return "No se seleccionó ningún archivo."

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    imagen = cv2.imread(filepath)
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    # Mejora del contraste con CLAHE (opcional)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    gris_mejorado = clahe.apply(gris)

    _, binaria = cv2.threshold(gris_mejorado, 150, 255, cv2.THRESH_BINARY)

    texto_detectado = pytesseract.image_to_string(binaria, lang='eng')

    print("=== Texto detectado ===")
    print(texto_detectado)
    print("======================")

    # Limpiar texto para dejar solo letras y números en mayúsculas
    texto_limpio = re.sub(r'[^A-Z0-9]', '', texto_detectado.upper())

    if len(texto_limpio) >= 4:
        placa = texto_limpio[:10]  # Ajusta según formato esperado
        resultado = f"Placa detectada: {placa}"
    else:
        resultado = "No se detectó una placa válida."

    return render_template('resultado.html', resultado=resultado, texto_completo=texto_detectado)

if __name__ == '__main__':
    app.run(debug=True)
