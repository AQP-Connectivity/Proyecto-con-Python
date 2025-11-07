# controllers/backup_controller.py

from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask import current_app
import os
from utiles.backup import crear_backup

backup_bp = Blueprint("backup", __name__)


@backup_bp.route("/backup", methods=["POST"])  # Cambiado a POST por seguridad (evita ejecución accidental por GET)
def backup_manual():
    """
    Ejecuta un respaldo manual de la base de datos.
    - Si la solicitud es HTML (formulario), redirige con flash message.
    - Si la solicitud es AJAX/JSON (Content-Type: application/json), devuelve JSON.
    """
    try:
        # Opcional: verificar que el directorio de backups existe y es escribible
        backup_dir = current_app.config.get("BACKUP_DIR", "backups")
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir, exist_ok=True)
        if not os.access(backup_dir, os.W_OK):
            raise PermissionError(f"El directorio '{backup_dir}' no es escribible.")

        ruta = crear_backup()

        current_app.logger.info(f"Backup manual creado exitosamente: {ruta}")

        # Responder según el tipo de cliente
        if request.headers.get("Content-Type") == "application/json" or request.is_json:
            return jsonify({
                "success": True,
                "message": "Backup creado correctamente.",
                "path": ruta
            }), 200
        else:
            flash(f"Backup creado correctamente: {ruta}", "success")
            return redirect(url_for("dashboard"))

    except PermissionError as e:
        error_msg = f"Permiso denegado para escribir en el directorio de backups: {e}"
        current_app.logger.error(f"Backup fallido: {error_msg}")
        if request.is_json:
            return jsonify({"success": False, "error": error_msg}), 403
        else:
            flash(error_msg, "danger")
            return redirect(url_for("dashboard"))

    except OSError as e:
        error_msg = f"Error del sistema al crear el backup: {e}"
        current_app.logger.error(f"Backup fallido (OS): {error_msg}")
        if request.is_json:
            return jsonify({"success": False, "error": error_msg}), 500
        else:
            flash(error_msg, "danger")
            return redirect(url_for("dashboard"))

    except Exception as e:
        # Captura otros errores (ej. conexión DB, comando fallido en `crear_backup`)
        error_msg = f"Error inesperado al crear el backup: {str(e)}"
        current_app.logger.critical(f"Backup fallido (excepción no manejada): {error_msg}", exc_info=True)
        if request.is_json:
            return jsonify({"success": False, "error": error_msg}), 500
        else:
            flash(error_msg, "danger")
            return redirect(url_for("dashboard"))
