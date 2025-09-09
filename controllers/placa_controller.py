import os
from datetime import datetime
from database.conexion import get_connection
from utils.image_processing import detectar_placa

UPLOAD_FOLDER = "static"

def procesar_placa(file):
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    placa_text = detectar_placa(filepath, UPLOAD_FOLDER)

    if placa_text:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO placas (numero, fecha_hora) VALUES (?, ?)", 
                       (placa_text, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()
    return placa_text

def obtener_registros():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM placas ORDER BY fecha_hora DESC")
    datos = cursor.fetchall()
    conn.close()
    return datos