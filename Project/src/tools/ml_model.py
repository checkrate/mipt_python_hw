import numpy as np
import cv2
from sklearn.cluster import KMeans

class MLModel:
    def __init__(self, n_clusters: int = 2, min_contour_area: int = 100, max_contour_area: int = 1000):
        """Инициализация параметров модели кластеризации.

        Args:
            n_clusters: количество кластеров для KMeans.
            min_contour_area: минимальная площадь контура для учёта.
            max_contour_area: максимальная площадь контура для учёта.
        """
        self.n_clusters = n_clusters
        self.min_contour_area = min_contour_area
        self.max_contour_area = max_contour_area

    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(image, (5, 5), 0)
        return blurred

    def segment_cells(self, image: np.ndarray) -> np.ndarray:
        height, width = image.shape
        pixels = image.reshape(-1, 1).astype(np.float32)
        kmeans = KMeans(n_clusters=self.n_clusters, random_state=0).fit(pixels)
        centers = kmeans.cluster_centers_.squeeze()
        labels = kmeans.labels_.reshape(height, width)
        cell_cluster = int(np.argmin(centers))
        mask = np.uint8((labels == cell_cluster) * 255)
        kernel = np.ones((3, 3), np.uint8)
        opened = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        closed = cv2.morphologyEx(opened, cv2.MORPH_CLOSE, kernel)
        return closed

    def find_cells(self, mask: np.ndarray) -> list:
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        valid_contours = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if self.min_contour_area <= area <= self.max_contour_area:
                valid_contours.append(contour)
        return valid_contours

    def predict(self, image: np.ndarray) -> int:
        preprocessed = self.preprocess_image(image)
        mask = self.segment_cells(preprocessed)
        contours = self.find_cells(mask)
        return len(contours)
