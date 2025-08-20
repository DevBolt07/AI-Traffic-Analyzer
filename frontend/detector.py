from ultralytics import YOLO
import cv2
import json

with open('config.json') as f:
    config = json.load(f)

model = YOLO(config['model_path'])

def detect_vehicles(image):
    results = model.predict(image, conf=config['confidence_threshold'])
    vehicle_count = 0
    annotated_frame = image.copy()

    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            if label in ["car", "truck", "bus", "motorbike"]:
                vehicle_count += 1
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(annotated_frame, label, (x1, y1-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    return vehicle_count, annotated_frame
