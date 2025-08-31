from flask import Flask, render_template, request
from controllers.placa_controller import procesar_placa, obtener_registros
from database.conexion import init_db
from flask import send_file
from utils.pdf_utils import generar_pdf
from controllers.placa_controller import obtener_registros

app = Flask(__name__)
UPLOAD_FOLDER = "static"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Inicializar DB
init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    placa_text = None
    if request.method == "POST":
        file = request.files["file"]
        if file:
            placa_text = procesar_placa(file)
    return render_template("index.html", placa=placa_text)

@app.route("/registros")
def registros():
    datos = obtener_registros()
    return render_template("registros.html", registros=datos)

@app.route("/reporte_pdf")
def reporte_pdf():
    registros = obtener_registros()
    pdf = generar_pdf(registros)
    return send_file(pdf, as_attachment=True, download_name="reporte_placas.pdf", mimetype="application/pdf")

if __name__ == "__main__":
    app.run(debug=True)
