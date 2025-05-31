import os
import cv2
from ultralytics import YOLO
import numpy as np

class CNNModel:
    """Модель обнаружения и подсчёта клеток крови с использованием YOLOv8."""
    def __init__(self, weights_filename: str = "best.pt"):
        current_dir = os.path.dirname(__file__)
        weights_dir = os.path.join(current_dir, "weights")
        weights_path = os.path.join(weights_dir, weights_filename)
        self.model = YOLO(weights_path)

    def predict(self, image: np.ndarray) -> int:
        resized = cv2.resize(image, (640, 640))
        results = self.model(resized)
        total_boxes = 0
        for r in results:
            total_boxes += len(r.boxes)
        return total_boxes

    def train(self, data_yaml: str, epochs: int = 50, imgsz: int = 640) -> None:
        self.model.train(data=data_yaml, epochs=epochs, imgsz=imgsz)
