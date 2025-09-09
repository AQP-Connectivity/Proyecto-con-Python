# controllers/dashboard_controller.py
import sqlite3, json
from database.conexion import get_connection

def obtener_dashboard():
    conn = get_connection()
    conn.row_factory = sqlite3.Row

    # Total de placas
    total = conn.execute("SELECT COUNT(*) AS total FROM placas").fetchone()["total"]

    # Últimas 5 placas
    ultimas = conn.execute("""
        SELECT numero, fecha_hora
        FROM placas
        ORDER BY fecha_hora DESC
        LIMIT 5
    """).fetchall()

    # Registros por día
    por_dia = conn.execute("""
        SELECT DATE(fecha_hora) AS fecha, COUNT(*) AS cantidad
        FROM placas
        GROUP BY DATE(fecha_hora)
        ORDER BY fecha
    """).fetchall()

    conn.close()

    # Listas ya listas para Chart.js
    fechas = [r["fecha"] for r in por_dia]
    cantidades = [r["cantidad"] for r in por_dia]

    return {
        "total": total,
        "ultimas": [{"numero": u["numero"], "fecha_hora": u["fecha_hora"]} for u in ultimas],
        "fechas_json": json.dumps(fechas),         # <<<<<< ya en JSON
        "cantidades_json": json.dumps(cantidades)  # <<<<<< ya en JSON
    }

