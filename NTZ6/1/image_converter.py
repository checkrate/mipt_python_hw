from binary_image import BinaryImage
from monochrome_image import MonochromeImage
from color_image import ColorImage
import numpy as np

class ImageConverter:
    @staticmethod
    def monochrome_to_monochrome(image):
        data = image.get_data()
        mean_value = np.mean(data)
        corrected_data = data + (128 - mean_value)
        corrected_data = np.clip(corrected_data, 0, 255)
        return MonochromeImage(corrected_data)

    @staticmethod
    def color_to_monochrome(image):
        data = image.get_data()
        grayscale_data = np.mean(data, axis=2)
        return MonochromeImage(grayscale_data)

    @staticmethod
    def monochrome_to_binary(image, threshold=128):
        data = image.get_data()
        binary_data = np.where(data >= threshold, 1, 0)
        return BinaryImage(binary_data)
