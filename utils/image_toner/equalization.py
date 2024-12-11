import cv2

def hist_eq(image):
    return cv2.equalizeHist(image)