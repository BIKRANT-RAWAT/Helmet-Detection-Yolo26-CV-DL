import os
import cv2
from ultralytics import YOLO


class HelmetPredictor:
    def __init__(self, model_path: str):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at {model_path}")

        self.model = YOLO(model_path)

    def predict_frame(self, frame, conf_threshold=0.5):
        """
        Run inference on a frame with confidence filtering.
        Returns:
            annotated_frame,
            helmet_count,
            no_helmet_count
        """
    
        results = self.model(frame)
    
        helmet_count = 0
        no_helmet_count = 0
    
        for box in results[0].boxes:
            conf = float(box.conf[0])
            cls_id = int(box.cls[0])
    
            if conf < conf_threshold:
                continue
            
            if cls_id == 1:  # helmet
                helmet_count += 1
            elif cls_id == 0:  # no-helmet
                no_helmet_count += 1
    
        annotated_frame = results[0].plot()
    
        return annotated_frame, helmet_count, no_helmet_count

    def predict_and_save(self, image_path: str, output_path: str):
        results = self.model(image_path)

        # Plot annotated image
        annotated_frame = results[0].plot()

        # Save image
        cv2.imwrite(output_path, annotated_frame)

        detections = []
        for box in results[0].boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            xyxy = box.xyxy[0].tolist()

            detections.append({
                "class_id": cls_id,
                "confidence": round(conf, 4),
                "bbox": [round(x, 2) for x in xyxy]
            })

        return detections