
from ultralytics import YOLO
import cv2

# 1. Cargar modelo YOLO preentrenado (COCO dataset)

model = YOLO("yolov8n.pt")

# 2. Abrir cámara
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 3. Detección
    results = model(frame)

    # 4. Dibujar resultados
    annotated_frame = results[0].plot()

    cv2.imshow("Detección de placas", annotated_frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC para salir
        break

cap.release()
cv2.destroyAllWindows()
