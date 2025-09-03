from flask import Flask, render_template, request, redirect, url_for, send_file
from controllers.placa_controller import procesar_placa, obtener_registros
from database.conexion import init_db
from utils.pdf_utils import generar_pdf
import cv2
from flask import Response



app = Flask(_name_)
UPLOAD_FOLDER = "static"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# 👉 Hacer disponible request en todos los templates
@app.context_processor
def inject_request():
    return dict(request=request)

# Inicializar DB SQLite
init_db()

@app.route("/")
def root():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # lógica de autenticación aquí
        pass
    return render_template("login.html")

@app.route("/mantenimiento")
def mantenimiento():
    return render_template("mantenimiento.html")


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
@app.route("/historial")
def historial():
    datos = obtener_registros()
    return render_template("historial.html", registros=datos)


@app.route("/reporte_pdf")
def reporte_pdf():
    registros = obtener_registros()
    pdf = generar_pdf(registros)
    return send_file(pdf, as_attachment=True, download_name="reporte_placas.pdf", mimetype="application/pdf")

camera = cv2.VideoCapture(0)  # Cámara predeterminada

def generar_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            
# ✅ Ruta del Estacionamiento
@app.route("/estacionamiento", methods=["GET", "POST"])
def estacionamiento():
    mensaje = None
    if request.method == "POST":
        fecha = request.form.get("fecha")
        hora = request.form.get("hora")
        precio = request.form.get("precio")

        # Aquí luego guardamos en SQLite; por ahora solo confirmamos en pantalla
        if fecha and hora and precio:
            mensaje = f"Estacionamiento guardado: {fecha} {hora} - S/. {precio}"
        else:
            mensaje = "Completa todos los campos."

    return render_template("estacionamiento.html", mensaje=mensaje)


# ✅ Ruta de Pagos
@app.route("/pagos", methods=["GET", "POST"])
def pagos():
    mensaje = None
    if request.method == "POST":
        monto = request.form.get("monto")
        metodo = request.form.get("metodo")
        fecha = request.form.get("fecha")

        if monto and metodo and fecha:
            mensaje = f"Pago registrado: {monto} soles con {metodo} el {fecha}"
        else:
            mensaje = "Completa todos los campos."

    return render_template("pagos.html", mensaje=mensaje)


@app.route("/camara")
def camara():
    return render_template("camara.html")

@app.route("/video_feed")
def video_feed():
    return Response(generar_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")

if _name_ == "_main_":
    app.run(debug=True)
