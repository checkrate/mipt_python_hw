import cv2
import numpy as np

class ImageFilters:
    @staticmethod
    def blur(image):
        return cv2.GaussianBlur(image, (5, 5), 0)
    
    @staticmethod
    def sharpen(image):
        kernel = np.array([[-1,-1,-1],
                          [-1, 9,-1],
                          [-1,-1,-1]])
        return cv2.filter2D(image, -1, kernel)
    
    @staticmethod
    def gradient(image):
        sobelx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
        return np.sqrt(sobelx**2 + sobely**2)
    
    @staticmethod
    def contrast(image, alpha=1.5, beta=0):
        adjusted = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
        return adjusted