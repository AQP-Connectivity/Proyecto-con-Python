# controllers/backup_controller.py

from flask import Blueprint, render_template, redirect, url_for, flash
from utiles.backup import crear_backup

backup_bp = Blueprint("backup", __name__)

@backup_bp.route("/backup", methods=["GET"])
def backup_manual():
    """
    Ejecuta un respaldo manual de la base de datos y muestra un mensaje.
    """
    try:
        ruta = crear_backup()
        flash(f"Backup creado correctamente: {ruta}", "success")
    except Exception as e:
        flash(f"Error al crear el backup: {e}", "danger")
    return redirect(url_for("dashboard"))  
