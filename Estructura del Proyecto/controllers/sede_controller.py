
#controlador para poder manejar diferentes sedes de estacionamiento

from flask import Blueprint, render_template, request, redirect, url_for
import models.sede_model as Sede

sede_bp = Blueprint("sede", __name__)

@sede_bp.route("/sedes")
def listar():
    sedes = Sede.listar_sedes()
    return render_template("sedes/listar.html", sedes=sedes)

@sede_bp.route("/sedes/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        nombre = request.form["nombre"]
        direccion = request.form["direccion"]
        telefono = request.form["telefono"]
        capacidad = request.form["capacidad"]
        Sede.crear_sede(nombre, direccion, telefono, capacidad)
        return redirect(url_for("sede.listar"))
    return render_template("sedes/nuevo.html")

@sede_bp.route("/sedes/eliminar/<int:id>")
def eliminar(id):
    Sede.eliminar_sede(id)
    return redirect(url_for("sede.listar"))
