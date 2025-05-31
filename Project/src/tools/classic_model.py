import cv2
import numpy as np

class ClassicModel:
    def __init__(self, dp: float = 1.2, min_dist: float = 20, param1: int = 50, param2: int = 30, min_radius: int = 10, max_radius: int = 30):
        """Инициализация параметров HoughCircles.

        Args:
            dp: отношение разрешения входного изображения к разрешению аккумулятора (inverse ratio).
            min_dist: минимальное расстояние между центрами обнаруженных кругов.
            param1: порог Canny-детектора краёв.
            param2: порог для центра окружности в детекторе Хафа.
            min_radius: минимальный радиус круга.
            max_radius: максимальный радиус круга.
        """
        self.dp = dp
        self.min_dist = min_dist
        self.param1 = param1
        self.param2 = param2
        self.min_radius = min_radius
        self.max_radius = max_radius

    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()
        blurred = cv2.GaussianBlur(gray, (9, 9), 2)
        return blurred

    def detect_cells(self, image: np.ndarray) -> np.ndarray:
        circles = cv2.HoughCircles(
            image,
            cv2.HOUGH_GRADIENT,
            dp=self.dp,
            minDist=self.min_dist,
            param1=self.param1,
            param2=self.param2,
            minRadius=self.min_radius,
            maxRadius=self.max_radius
        )
        return circles

    def predict(self, image: np.ndarray) -> int:
        preprocessed = self.preprocess_image(image)
        circles = self.detect_cells(preprocessed)
        if circles is None:
            return 0
        return circles.shape[1]