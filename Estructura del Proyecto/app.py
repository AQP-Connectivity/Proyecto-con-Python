from flask import Flask, json, render_template, request, redirect, url_for, send_file, Response
from controllers.placa_controller import procesar_placa, obtener_registros
from database.conexion import init_db
from utils.pdf_utils import generar_pdf
from controllers.dashboard_controller import obtener_dashboard
import cv2
from controllers.salida_controller import registrar_salida


app = Flask(__name__)
UPLOAD_FOLDER = "static"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# 👉 Hacer disponible request en todos los templatess
@app.context_processor
def inject_request():
    return dict(request=request)

# Inicializar DB SQLite3
init_db()

# ✅ Redirección al login al iniciar el server
@app.route("/")
def root():
    return redirect(url_for("login"))

# ✅ Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # lógica de autenticación aquí
        return redirect(url_for("index"))
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template('registerUser.html')


# ✅ Página de inicio
@app.route("/index", methods=["GET", "POST"])
def index():
    placa_text = None
    if request.method == "POST":
        file = request.files["file"]
        if file:
            placa_text = procesar_placa(file)
    return render_template("index.html", placa=placa_text)

# ✅ Página de registros
@app.route("/registros")
def registros():
    datos = obtener_registros()
    return render_template("registros.html", registros=datos)

# ✅ Página de historial
@app.route("/historial")
def historial():
    datos = obtener_registros()
    return render_template("historial.html", registros=datos)

# ✅ Reporte PDF y descargar en .pdf
@app.route("/reporte_pdf")
def reporte_pdf():
    registros = obtener_registros()
    pdf = generar_pdf(registros)
    return send_file(
        pdf,
        as_attachment=True,
        download_name="reporte_placas.pdf",
        mimetype="application/pdf"
    )

# ✅ Dashboard con datos dinámicosssssss
@app.route("/dashboard")
def dashboard():
    fechas = ["2025-09-01", "2025-09-02", "2025-09-03", "2025-09-04"]
    cantidades = [3, 5, 7, 4]
    return render_template(
        "dashboard.html",
        fechas_json=json.dumps(fechas),
        cantidades_json=json.dumps(cantidades)
    )

# ✅ Mantenimiento
@app.route("/mantenimiento")
def mantenimiento():
    return render_template("mantenimiento.html")

# ✅ Se activa la Cámara
camera = cv2.VideoCapture(0)

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

@app.route("/camara")
def camara():
    return render_template("camara.html")

@app.route("/video_feed")
def video_feed():
    return Response(generar_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")

# ✅ Estacionamiento
@app.route("/estacionamiento", methods=["GET", "POST"])
def estacionamiento():
    mensaje = None
    if request.method == "POST":
        fecha = request.form.get("fecha")
        hora = request.form.get("hora")
        precio = request.form.get("precio")
        if fecha and hora and precio:
            mensaje = f"Estacionamiento guardado: {fecha} {hora} - S/. {precio}"
        else:
            mensaje = "Completa todos los campos."
    return render_template("estacionamiento.html", mensaje=mensaje)

# ✅ Pagos
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

# ✅ Usuarios
@app.route("/usuarios", methods=["GET", "POST"])
def usuarios():
    mensaje = None
    if request.method == "POST":
        nombre = request.form.get("nombre")
        correo = request.form.get("correo")
        rol = request.form.get("rol")
        if nombre and correo and rol:
            mensaje = f"Usuario registrado: {nombre} ({rol}) - {correo}"
        else:
            mensaje = "Completa todos los campos."
    return render_template("usuarios.html", mensaje=mensaje)



@app.route("/salida", methods=["POST"])
def salida():
    placa = request.form.get("placa")
    if placa:
        mensaje = registrar_salida(placa)
    else:
        mensaje = "Debes ingresar una placa."

    return render_template("salida.html", mensaje=mensaje)



# 🚀 Iniciar servidor (SOLO UNA VEZ al final)
if __name__ == "__main__":
    app.run(debug=True)
