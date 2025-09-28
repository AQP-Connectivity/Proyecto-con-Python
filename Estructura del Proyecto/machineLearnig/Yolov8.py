
from ultralytics import YOLO
import cv2
import os
from utils.image_processing import detectar_placa
from database.conexion import get_connection
from datetime import datetime

# 1. Cargar modelo YOLO preentrenado 

model = YOLO("yolov8n.pt")

# 2. Abrir cámara
cap = cv2.VideoCapture(0)

UPLOAD_FOLDER = "static/uploads"

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 3. Detección
    results = model(frame)

    # 4. Dibujar resultados
    annotated_frame = results[0].plot()

    # Filtrar detecciones solo de autos
    for box in results[0].boxes:
        cls = int(box.cls[0])
        if model.names[cls] in ["car", "truck"]:
            
            # Guardar frame si detecta un vehículo
            filename = f"auto_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            cv2.imwrite(filepath, frame)

    # Pasar a OCR
            
            placa_text = detectar_placa(filepath, UPLOAD_FOLDER)

    # Guardar en DB

    if placa_text:
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO placas (numero, hora_entrada) VALUES (?, ?)",
                    (placa_text, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                )
                conn.commit()
                conn.close()

    cv2.imshow("Detección de placas", annotated_frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC para salir
        break

cap.release()
cv2.destroyAllWindows()
