import os
from datetime import datetime
from database.conexion import get_connection
from utils.image_processing import detectar_placa

UPLOAD_FOLDER = "static"

def procesar_placa(file):
    # Guardar la imagen en la carpeta static
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Detectar el texto de la placa desde la imagen
    placa_text = detectar_placa(filepath, UPLOAD_FOLDER)

    if placa_text:
        conn = get_connection()
        cursor = conn.cursor()

        # Insertar con las columnas correctas
        cursor.execute("""
            INSERT INTO placas (numero, hora_entrada, hora_salida, costo) 
            VALUES (?, ?, ?, ?)
        """, (
            placa_text,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # hora_entrada
            None,   # hora_salida aún no se registra
            0.0     # costo inicial por defecto
        ))

        conn.commit()
        conn.close()

    return placa_text


def obtener_registros():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, numero, hora_entrada, hora_salida, costo
        FROM placas
        ORDER BY hora_entrada DESC
    """)
    datos = cursor.fetchall()
    conn.close()

    registros = []
    formato = "%Y-%m-%d %H:%M:%S"

    for id_, numero, entrada, salida, costo in datos:
        if salida:
            # Calcular diferencia entre entrada y salida
            t_entrada = datetime.strptime(entrada, formato)
            t_salida = datetime.strptime(salida, formato)
            tiempo_total = str(t_salida - t_entrada)
        else:
            tiempo_total = "En curso"  # si aún no hay salida

        registros.append((id_, numero, entrada, salida, tiempo_total, costo))

    return registros
