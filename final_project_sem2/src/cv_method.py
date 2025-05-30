import cv2
import numpy as np

class CellCounterCV:
    def __init__(self, threshold_block=51, min_area=100):
        self.threshold_block = threshold_block
        self.min_area = min_area

    def count_cells(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        th = cv2.adaptiveThreshold(gray, 255,
                                   cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV,
                                   self.threshold_block, 2)

        kernel = np.ones((3,3), np.uint8)
        opening = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel, iterations=2)

        sure_bg = cv2.dilate(opening, kernel, iterations=3)
        dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
        _, sure_fg = cv2.threshold(dist_transform,
                                   0.7 * dist_transform.max(),
                                   255, 0)
        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(sure_bg, sure_fg)

        _, markers = cv2.connectedComponents(sure_fg)
        markers = markers + 1
        markers[unknown==255] = 0
        markers = cv2.watershed(img, markers)

        count = len(np.unique(markers)) - 2
        return count, markers