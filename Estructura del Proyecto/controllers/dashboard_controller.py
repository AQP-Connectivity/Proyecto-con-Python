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

    # 4. Total de pagos realizados
    
    total_pagos = conn.execute(
        "SELECT COUNT(*) AS total FROM pagos"
    ).fetchone()["total"]

    # 5. Últimos 5 pagos
    
    ultimos_pagos = conn.execute("""
        SELECT id, monto, fecha_hora
        FROM pagos
        ORDER BY fecha_hora DESC
        LIMIT 5
    """).fetchall()

    conn.close()

    # Listas ya listas para Chart.js
    fechas = [r["fecha"] for r in por_dia]
    cantidades = [r["cantidad"] for r in por_dia]

    return {
        # Sección de placas
        "total_placas": total_placas,
        "ultimas_placas": [
            {"numero": u["numero"], "fecha_hora": u["fecha_hora"]} for u in ultimas_placas
        ],

        # Datos para gráficos
        "fechas_json": json.dumps(fechas),
        "cantidades_json": json.dumps(cantidades),

        # Sección de pagos
        "total_pagos": total_pagos,
        "ultimos_pagos": [
            {"id": p["id"], "monto": p["monto"], "fecha_hora": p["fecha_hora"]} for p in ultimos_pagos
        ],

        # Sección de notificaciones
        "total_notificaciones": total_notificaciones,

        # Sección de backups
        "total_backups": total_backups
    }

