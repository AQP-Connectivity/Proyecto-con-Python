import cv2
import numpy as np
import pytesseract
import sqlite3
from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = "static"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Configuración Tesseract (asegúrate que esté instalado en tu PC)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Crear base de datos SQLite
def init_db():
    conn = sqlite3.connect("parking.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS placas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero TEXT,
            fecha_hora TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Página principal
@app.route("/", methods=["GET", "POST"])
def index():
    placa_text = None
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(filepath)

            # Procesar imagen con OpenCV
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
                    cv2.imwrite(os.path.join(app.config["UPLOAD_FOLDER"], "placa_recortada.jpg"), placa)
                    break

            if placa is not None:
                # Reconocer texto
                placa_text = pytesseract.image_to_string(placa, config="--psm 8").strip()

                # Guardar en base de datos
                conn = sqlite3.connect("parking.db")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO placas (numero, fecha_hora) VALUES (?, ?)", 
                               (placa_text, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                conn.commit()
                conn.close()

    return render_template("index.html", placa=placa_text)


# Ver registros guardados
@app.route("/registros")
def registros():
    conn = sqlite3.connect("parking.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM placas ORDER BY fecha_hora DESC")
    datos = cursor.fetchall()
    conn.close()
    return render_template("registros.html", registros=datos)


if __name__ == "__main__":
    app.run(debug=True)
