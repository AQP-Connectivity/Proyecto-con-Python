import sqlite3
from datetime import datetime

DB_PATH = "placas.db"  # Ajusta si está en otra ruta

# 👉 Función para registrar la salida
def registrar_salida(placa, tarifa_por_minuto=0.10):
    """
    Marca la salida de un vehículo, calcula tiempo y costo.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Buscar registro activo (sin salida registrada)
    cursor.execute("""
        SELECT id, hora_entrada FROM placas 
        WHERE numero = ? AND hora_salida IS NULL
        ORDER BY id DESC LIMIT 1
    """, (placa,))
    registro = cursor.fetchone()

    if not registro:
        conn.close()
        return f"No se encontró un ingreso activo para la placa {placa}"

    id_registro, hora_entrada = registro

    # Calcular hora de salida, tiempo total y costo
    hora_salida = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formato = "%Y-%m-%d %H:%M:%S"

    dt_entrada = datetime.strptime(hora_entrada, formato)
    dt_salida = datetime.strptime(hora_salida, formato)

    diferencia = dt_salida - dt_entrada
    minutos_totales = int(diferencia.total_seconds() // 60)

    costo = round(minutos_totales * tarifa_por_minuto, 2)

    # Actualizar registro en la BD
    cursor.execute("""
        UPDATE placas
        SET hora_salida = ?, tiempo_total = ?, costo = ?
        WHERE id = ?
    """, (hora_salida, minutos_totales, costo, id_registro))

    conn.commit()
    conn.close()

    return f"Salida registrada para {placa}. Tiempo: {minutos_totales} min - Costo: S/. {costo}"
