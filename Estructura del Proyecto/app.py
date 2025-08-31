from flask import Flask, render_template, request, redirect, url_for
from controllers.placa_controller import procesar_placa, obtener_registros
from database.conexion import init_db
from flask import send_file
from utils.pdf_utils import generar_pdf
from controllers.placa_controller import obtener_registros

app = Flask(__name__)
UPLOAD_FOLDER = "static"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Inicializar DB sQLITE
init_db()

@app.route("/")
def root():
    # Redirige a login
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    # Aquí puedes manejar el POST para validar usuario si quieres
    if request.method == "POST":
        # validación y lógica aquí
        pass
    return render_template("login.html")

@app.route("/index", methods=["GET", "POST"])
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
