import cv2
import numpy as np
import random

class ImageAugmentor:
    def __init__(self):
        self.methods = {
            "Add Noise": self.add_noise,
            "Denoise": self.denoise,
            "Gaussian Blur": self.gaussian_blur,
            "Histogram Equalization": self.histogram_equalization,
            "Rotation": self.rotation,
            "Glass Effect": self.glass_effect,
            "Motion Blur": self.motion_blur,
        }

    def add_noise(self, image):
        noise = np.random.normal(0, 25, image.shape).astype(np.uint8)
        return cv2.add(image, noise)

    def denoise(self, image):
        return cv2.fastNlMeansDenoising(image, None, 30, 7, 21)

    def gaussian_blur(self, image):
        return cv2.GaussianBlur(image, (5, 5), 0)

    def histogram_equalization(self, image):
        if len(image.shape) == 2:  # Grayscale image
            return cv2.equalizeHist(image)
        else:  # Color image
            ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
            ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])
            return cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)

    def rotation(self, image, angle):
        height, width = image.shape[:2]
        center = (width // 2, height // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1)
        return cv2.warpAffine(image, M, (width, height))

    def glass_effect(self, image, power):
        height, width = image.shape[:2]
        dst = np.zeros(image.shape, np.uint8)
        for m in range(height - power):
            for n in range(width - power):
                index = random.randint(1, power)
                dst[m, n] = image[m + index, n + index]
        return dst

    def motion_blur(self, image, degree, angle):
        M = cv2.getRotationMatrix2D((degree / 2, degree / 2), angle, 1)
        motion_blur_kernel = np.diag(np.ones(degree))
        motion_blur_kernel = cv2.warpAffine(motion_blur_kernel, M, (degree, degree))
        motion_blur_kernel /= degree
        blurred = cv2.filter2D(image, -1, motion_blur_kernel)
        return cv2.normalize(blurred, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

