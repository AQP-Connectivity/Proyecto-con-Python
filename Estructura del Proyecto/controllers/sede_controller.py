
#controlador para poder manejar diferentes sedes de estacionamiento

# controllers/sede_controller.py
# Controlador para manejar las sedes del estacionamiento (CRUD completo)

from flask import Blueprint, render_template, request, redirect, url_for, flash
from database.model import sede_model  as Sede

# Blueprint para modularizar las rutas relacionadas con "sedes"
sede_bp = Blueprint("sede", __name__)

# 🟢 LISTAR SEDES
@sede_bp.route("/sedes")
def listar():
    """
    Muestra todas las sedes registradas en el sistema.
    """
    sedes = Sede.listar_sedes()
    return render_template("sedes/listar.html", sedes=sedes)

# 🟢 CREAR NUEVA SEDE
@sede_bp.route("/sedes/nuevo", methods=["GET", "POST"])
def nuevo():
    """
    Permite registrar una nueva sede de estacionamiento.
    Si se accede por GET, muestra el formulario.
    Si se accede por POST, guarda la nueva sede en la base de datos.
    """
    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        direccion = request.form["direccion"].strip()
        telefono = request.form["telefono"].strip()
        capacidad = request.form["capacidad"].strip()

        # Validación simple antes de guardar
        if not nombre:
            flash("⚠️ El nombre de la sede es obligatorio.", "warning")
            return redirect(url_for("sede.nuevo"))

        try:
            Sede.crear_sede(nombre, direccion, telefono, capacidad)
            flash(f"✅ Sede '{nombre}' creada correctamente.", "success")
        except Exception as e:
            flash(f"❌ Error al crear la sede: {e}", "danger")

        return redirect(url_for("sede.listar"))

    # Renderiza el formulario si se accede por GET
    return render_template("sedes/nuevo.html")

# 🔴 ELIMINAR SEDE
@sede_bp.route("/sedes/eliminar/<int:id>")
def eliminar(id):
    """
    Elimina una sede por su ID.
    """
    try:
        Sede.eliminar_sede(id)
        flash("🗑️ Sede eliminada correctamente.", "info")
    except Exception as e:
        flash(f"❌ No se pudo eliminar la sede: {e}", "danger")

    return redirect(url_for("sede.listar"))

