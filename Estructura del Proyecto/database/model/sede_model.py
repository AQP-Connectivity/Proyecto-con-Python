# models/sede_model.py
# Modelo para manejar las sedes del estacionamiento
# Realiza operaciones CRUD simples usando SQLite3

import sqlite3
import os

# 📂 Ruta de la base de datos (se crea automáticamente si no existe)
DB_PATH = os.path.join(os.path.dirname(__file__), "../data/estacionamiento.db")


def conectar():
    """Establece conexión con la base de datos."""
    return sqlite3.connect(DB_PATH)


def inicializar_bd():
    """
    Crea la tabla 'sedes' si no existe.
    Se recomienda llamar a esta función al iniciar la aplicación.
    """
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sedes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            direccion TEXT,
            telefono TEXT,
            capacidad INTEGER
        )
    """)
    conexion.commit()
    conexion.close()


def listar_sedes():
    """
    Retorna una lista de todas las sedes registradas.
    """
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, direccion, telefono, capacidad FROM sedes")
    sedes = cursor.fetchall()
    conexion.close()
    return sedes


def crear_sede(nombre, direccion, telefono, capacidad):
    """
    Inserta una nueva sede en la base de datos.
    """
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO sedes (nombre, direccion, telefono, capacidad)
        VALUES (?, ?, ?, ?)
    """, (nombre, direccion, telefono, capacidad))
    conexion.commit()
    conexion.close()


def eliminar_sede(id_sede):
    """
    Elimina una sede por su ID.
    """
    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM sedes WHERE id = ?", (id_sede,))
    conexion.commit()
    conexion.close()
